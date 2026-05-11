package genetica

import (
	"math"
	"math/rand"
	"testing"
)

// ===== Configuration Tests =====

func TestValidateConfig(t *testing.T) {
	tests := []struct {
		name      string
		config    Config
		wantError bool
	}{
		{
			name: "valid config",
			config: Config{
				PopulationSize: 100,
				GeneCount:      10,
				Generations:    50,
				CrossoverRate:  0.8,
				MutationRate:   0.1,
				EliteCount:     2,
			},
			wantError: false,
		},
		{
			name: "population too small",
			config: Config{
				PopulationSize: 1,
				GeneCount:      10,
				Generations:    50,
				CrossoverRate:  0.8,
				MutationRate:   0.1,
				EliteCount:     0,
			},
			wantError: true,
		},
		{
			name: "invalid crossover rate",
			config: Config{
				PopulationSize: 100,
				GeneCount:      10,
				Generations:    50,
				CrossoverRate:  1.5,
				MutationRate:   0.1,
				EliteCount:     2,
			},
			wantError: true,
		},
		{
			name: "invalid mutation rate",
			config: Config{
				PopulationSize: 100,
				GeneCount:      10,
				Generations:    50,
				CrossoverRate:  0.8,
				MutationRate:   -0.1,
				EliteCount:     2,
			},
			wantError: true,
		},
		{
			name: "elite count too large",
			config: Config{
				PopulationSize: 100,
				GeneCount:      10,
				Generations:    50,
				CrossoverRate:  0.8,
				MutationRate:   0.1,
				EliteCount:     100,
			},
			wantError: true,
		},
		{
			name: "bounds length mismatch",
			config: Config{
				PopulationSize: 100,
				GeneCount:      10,
				Generations:    50,
				CrossoverRate:  0.8,
				MutationRate:   0.1,
				EliteCount:     2,
				Bounds:         []Bound{{0, 1}, {0, 1}},
			},
			wantError: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := validateConfig(&tt.config)
			if (err != nil) != tt.wantError {
				t.Errorf("validateConfig() error = %v, wantError %v", err, tt.wantError)
			}
		})
	}
}

// ===== Individual Tests =====

func TestIndividualClone(t *testing.T) {
	original := &Individual{
		Genes:   []float64{1.0, 2.0, 3.0},
		Fitness: 0.5,
		Age:     3,
		Elite:   true,
	}

	clone := original.Clone()

	// Check all fields are copied
	if len(clone.Genes) != len(original.Genes) {
		t.Errorf("Clone() genes length = %d, want %d", len(clone.Genes), len(original.Genes))
	}

	for i := range original.Genes {
		if clone.Genes[i] != original.Genes[i] {
			t.Errorf("Clone() gene[%d] = %f, want %f", i, clone.Genes[i], original.Genes[i])
		}
	}

	if clone.Fitness != original.Fitness {
		t.Errorf("Clone() fitness = %f, want %f", clone.Fitness, original.Fitness)
	}

	if clone.Age != original.Age {
		t.Errorf("Clone() age = %d, want %d", clone.Age, original.Age)
	}

	if clone.Elite != original.Elite {
		t.Errorf("Clone() elite = %v, want %v", clone.Elite, original.Elite)
	}

	// Modify clone and check original is unchanged
	clone.Genes[0] = 999.0
	if original.Genes[0] == 999.0 {
		t.Error("Clone() did not create independent copy of genes")
	}
}

// ===== Selection Tests =====

func TestTournamentSelection(t *testing.T) {
	population := Population{
		{Genes: []float64{1.0}, Fitness: 0.1},
		{Genes: []float64{2.0}, Fitness: 0.9},
		{Genes: []float64{3.0}, Fitness: 0.5},
		{Genes: []float64{4.0}, Fitness: 0.7},
	}

	// Run multiple times to check selection happens
	selectedCount := make(map[int]int)
	for i := 0; i < 1000; i++ {
		selected := TournamentSelection(population, 2)
		for idx, ind := range population {
			if selected == ind {
				selectedCount[idx]++
				break
			}
		}
	}

	// Higher fitness individuals should be selected more often
	// Individual 1 (fitness 0.9) should be selected more than individual 0 (fitness 0.1)
	if selectedCount[1] <= selectedCount[0] {
		t.Error("TournamentSelection() should favor higher fitness individuals")
	}
}

func TestRouletteWheelSelection(t *testing.T) {
	population := Population{
		{Genes: []float64{1.0}, Fitness: 0.1},
		{Genes: []float64{2.0}, Fitness: 0.4},
		{Genes: []float64{3.0}, Fitness: 0.5},
	}

	selectedCount := make(map[int]int)
	for i := 0; i < 1000; i++ {
		selected := RouletteWheelSelection(population, 0)
		for idx, ind := range population {
			if selected == ind {
				selectedCount[idx]++
				break
			}
		}
	}

	// Higher fitness should have higher selection probability
	if selectedCount[2] <= selectedCount[0] {
		t.Error("RouletteWheelSelection() should favor higher fitness individuals")
	}
}

func TestRankSelection(t *testing.T) {
	population := Population{
		{Genes: []float64{1.0}, Fitness: 0.1},
		{Genes: []float64{2.0}, Fitness: 0.9},
		{Genes: []float64{3.0}, Fitness: 0.5},
	}

	selectedCount := make(map[int]int)
	for i := 0; i < 1000; i++ {
		selected := RankSelection(population, 0)
		for idx, ind := range population {
			if selected == ind {
				selectedCount[idx]++
				break
			}
		}
	}

	// Higher fitness should have higher selection probability
	if selectedCount[1] <= selectedCount[0] {
		t.Error("RankSelection() should favor higher fitness individuals")
	}
}

func TestSelectionEmptyPopulation(t *testing.T) {
	population := Population{}

	if TournamentSelection(population, 2) != nil {
		t.Error("TournamentSelection() should return nil for empty population")
	}

	if RouletteWheelSelection(population, 0) != nil {
		t.Error("RouletteWheelSelection() should return nil for empty population")
	}

	if RankSelection(population, 0) != nil {
		t.Error("RankSelection() should return nil for empty population")
	}
}

// ===== Crossover Tests =====

func TestSinglePointCrossover(t *testing.T) {
	parent1 := &Individual{Genes: []float64{1, 1, 1, 1, 1}}
	parent2 := &Individual{Genes: []float64{2, 2, 2, 2, 2}}

	child1, child2 := SinglePointCrossover(parent1, parent2, 1.0)

	// Verify children have correct gene count
	if len(child1.Genes) != 5 || len(child2.Genes) != 5 {
		t.Error("SinglePointCrossover() children have wrong gene count")
	}

	// Run multiple times to verify crossover produces valid results
	for i := 0; i < 100; i++ {
		c1, c2 := SinglePointCrossover(parent1, parent2, 1.0)
		if len(c1.Genes) != 5 || len(c2.Genes) != 5 {
			t.Error("SinglePointCrossover() children have wrong gene count")
		}
		// Verify genes are from parents (either 1 or 2)
		for j := 0; j < 5; j++ {
			if c1.Genes[j] != 1 && c1.Genes[j] != 2 {
				t.Errorf("child1 gene[%d] = %f, should be 1 or 2", j, c1.Genes[j])
			}
			if c2.Genes[j] != 1 && c2.Genes[j] != 2 {
				t.Errorf("child2 gene[%d] = %f, should be 1 or 2", j, c2.Genes[j])
			}
		}
	}
}

func TestTwoPointCrossover(t *testing.T) {
	parent1 := &Individual{Genes: []float64{1, 1, 1, 1, 1}}
	parent2 := &Individual{Genes: []float64{2, 2, 2, 2, 2}}

	for i := 0; i < 100; i++ {
		child1, child2 := TwoPointCrossover(parent1, parent2, 1.0)
		if len(child1.Genes) != 5 || len(child2.Genes) != 5 {
			t.Error("TwoPointCrossover() children have wrong gene count")
		}
	}
}

func TestUniformCrossover(t *testing.T) {
	parent1 := &Individual{Genes: []float64{1, 1, 1, 1, 1}}
	parent2 := &Individual{Genes: []float64{2, 2, 2, 2, 2}}

	child1, child2 := UniformCrossover(parent1, parent2, 1.0)

	if len(child1.Genes) != 5 || len(child2.Genes) != 5 {
		t.Error("UniformCrossover() children have wrong gene count")
	}
}

func TestArithmeticCrossover(t *testing.T) {
	parent1 := &Individual{Genes: []float64{0, 0, 0, 0, 0}}
	parent2 := &Individual{Genes: []float64{10, 10, 10, 10, 10}}

	for i := 0; i < 100; i++ {
		child1, child2 := ArithmeticCrossover(parent1, parent2, 1.0)

		// Children should be between parents
		for j := 0; j < 5; j++ {
			if child1.Genes[j] < 0 || child1.Genes[j] > 10 {
				t.Errorf("ArithmeticCrossover() child1 gene[%d] = %f, out of bounds", j, child1.Genes[j])
			}
			if child2.Genes[j] < 0 || child2.Genes[j] > 10 {
				t.Errorf("ArithmeticCrossover() child2 gene[%d] = %f, out of bounds", j, child2.Genes[j])
			}
		}
	}
}

func TestSBXCrossover(t *testing.T) {
	parent1 := &Individual{Genes: []float64{0, 0, 0, 0, 0}}
	parent2 := &Individual{Genes: []float64{10, 10, 10, 10, 10}}

	child1, child2 := SBXCrossover(parent1, parent2, 1.0)

	if len(child1.Genes) != 5 || len(child2.Genes) != 5 {
		t.Error("SBXCrossover() children have wrong gene count")
	}
}

// ===== Mutation Tests =====

func TestGaussianMutation(t *testing.T) {
	individual := &Individual{Genes: []float64{5, 5, 5, 5, 5}}
	bounds := []Bound{{0, 10}, {0, 10}, {0, 10}, {0, 10}, {0, 10}}

	mutated := &Individual{Genes: make([]float64, 5)}
	copy(mutated.Genes, individual.Genes)

	GaussianMutation(mutated, 1.0, bounds)

	// At least some genes should be different
	changes := 0
	for i := range individual.Genes {
		if mutated.Genes[i] != individual.Genes[i] {
			changes++
		}
		// Check bounds
		if mutated.Genes[i] < 0 || mutated.Genes[i] > 10 {
			t.Errorf("GaussianMutation() gene[%d] = %f, out of bounds", i, mutated.Genes[i])
		}
	}

	if changes == 0 {
		t.Error("GaussianMutation() should mutate genes with mutation rate 1.0")
	}
}

func TestUniformMutation(t *testing.T) {
	individual := &Individual{Genes: []float64{5, 5, 5, 5, 5}}
	bounds := []Bound{{0, 10}, {0, 10}, {0, 10}, {0, 10}, {0, 10}}

	mutated := &Individual{Genes: make([]float64, 5)}
	copy(mutated.Genes, individual.Genes)

	UniformMutation(mutated, 1.0, bounds)

	// All genes should be different (with mutation rate 1.0)
	for i := range mutated.Genes {
		if mutated.Genes[i] < 0 || mutated.Genes[i] > 10 {
			t.Errorf("UniformMutation() gene[%d] = %f, out of bounds", i, mutated.Genes[i])
		}
	}
}

func TestPolynomialMutation(t *testing.T) {
	individual := &Individual{Genes: []float64{5, 5, 5, 5, 5}}
	bounds := []Bound{{0, 10}, {0, 10}, {0, 10}, {0, 10}, {0, 10}}

	mutated := &Individual{Genes: make([]float64, 5)}
	copy(mutated.Genes, individual.Genes)

	PolynomialMutation(mutated, 1.0, bounds)

	for i := range mutated.Genes {
		if mutated.Genes[i] < 0 || mutated.Genes[i] > 10 {
			t.Errorf("PolynomialMutation() gene[%d] = %f, out of bounds", i, mutated.Genes[i])
		}
	}
}

func TestSwapMutation(t *testing.T) {
	individual := &Individual{Genes: []float64{1, 2, 3, 4, 5}}
	bounds := []Bound{}

	// Run multiple times to see swaps
	swapped := false
	for i := 0; i < 100; i++ {
		mutated := &Individual{Genes: make([]float64, 5)}
		copy(mutated.Genes, individual.Genes)
		SwapMutation(mutated, 1.0, bounds)

		// Check that genes are permuted (same values, different order possibly)
		values := make(map[float64]int)
		for _, g := range mutated.Genes {
			values[g]++
		}
		if len(values) != 5 {
			t.Error("SwapMutation() changed gene values instead of swapping")
		}

		// Check if any swap occurred
		for j := range mutated.Genes {
			if mutated.Genes[j] != individual.Genes[j] {
				swapped = true
				break
			}
		}
	}

	if !swapped {
		t.Error("SwapMutation() should swap genes")
	}
}

func TestBoundaryMutation(t *testing.T) {
	individual := &Individual{Genes: []float64{5, 5, 5, 5, 5}}
	bounds := []Bound{{0, 10}, {0, 10}, {0, 10}, {0, 10}, {0, 10}}

	mutated := &Individual{Genes: make([]float64, 5)}
	copy(mutated.Genes, individual.Genes)

	BoundaryMutation(mutated, 1.0, bounds)

	// All genes should be either 0 or 10
	for i := range mutated.Genes {
		if mutated.Genes[i] != 0 && mutated.Genes[i] != 10 {
			t.Errorf("BoundaryMutation() gene[%d] = %f, should be 0 or 10", i, mutated.Genes[i])
		}
	}
}

// ===== Benchmark Function Tests =====

func TestSphereFunction(t *testing.T) {
	tests := []struct {
		genes     []float64
		wantMin   bool // Should be at minimum
	}{
		{[]float64{0, 0, 0}, true},
		{[]float64{1, 1, 1}, false},
		{[]float64{-1, -1, -1}, false},
		{[]float64{0, 0, 0, 0, 0}, true},
	}

	for _, tt := range tests {
		fitness := SphereFunction(tt.genes)
		if tt.wantMin && fitness != 0 {
			t.Errorf("SphereFunction(%v) = %f, want 0", tt.genes, fitness)
		}
		if !tt.wantMin && fitness >= 0 {
			t.Errorf("SphereFunction(%v) = %f, should be negative", tt.genes, fitness)
		}
	}
}

func TestRastriginFunction(t *testing.T) {
	// Global minimum at origin
	origin := []float64{0, 0, 0}
	fitness := RastriginFunction(origin)

	// Should be 0 at origin (negated for maximization)
	if fitness != 0 {
		t.Errorf("RastriginFunction(origin) = %f, want 0", fitness)
	}

	// Non-optimal point should have negative fitness
	nonOptimal := []float64{1, 1, 1}
	fitness2 := RastriginFunction(nonOptimal)
	if fitness2 >= 0 {
		t.Errorf("RastriginFunction(%v) = %f, should be negative", nonOptimal, fitness2)
	}
}

func TestRosenbrockFunction(t *testing.T) {
	// Global minimum at (1, 1, ...)
	optimal := []float64{1, 1}
	fitness := RosenbrockFunction(optimal)

	// Should be 0 at optimal (negated for maximization)
	if fitness != 0 {
		t.Errorf("RosenbrockFunction(optimal) = %f, want 0", fitness)
	}
}

func TestAckleyFunction(t *testing.T) {
	// Global minimum at origin
	origin := []float64{0, 0, 0}
	fitness := AckleyFunction(origin)

	// Should be approximately 0 at origin (negated)
	// The function returns -result, so at origin it should be close to 0
	if fitness < -1e-10 || fitness > 1e-10 {
		t.Errorf("AckleyFunction(origin) = %f, should be approximately 0", fitness)
	}
}

func TestGriewankFunction(t *testing.T) {
	// Global minimum at origin
	origin := []float64{0, 0, 0}
	fitness := GriewankFunction(origin)

	// Should be 0 at origin (negated)
	if fitness != 0 {
		t.Errorf("GriewankFunction(origin) = %f, want 0", fitness)
	}
}

func TestSchwefelFunction(t *testing.T) {
	// Just test it runs and produces reasonable values
	// Schwefel's optimal is at ~420.9687 where the value is about -n*418.9829
	genes := []float64{420.9687, 420.9687, 420.9687}
	fitness := SchwefelFunction(genes)

	// The function should return a finite value
	if math.IsNaN(fitness) || math.IsInf(fitness, 0) {
		t.Errorf("SchwefelFunction() returned invalid value: %f", fitness)
	}
}

// ===== Utility Function Tests =====

func TestEuclideanDistance(t *testing.T) {
	tests := []struct {
		a, b     []float64
		expected float64
	}{
		{[]float64{0, 0, 0}, []float64{0, 0, 0}, 0},
		{[]float64{1, 0, 0}, []float64{0, 0, 0}, 1},
		{[]float64{0, 3, 4}, []float64{0, 0, 0}, 5},
		{[]float64{1, 1, 1}, []float64{2, 2, 2}, math.Sqrt(3)},
	}

	for _, tt := range tests {
		result := EuclideanDistance(tt.a, tt.b)
		if math.Abs(result-tt.expected) > 1e-10 {
			t.Errorf("EuclideanDistance(%v, %v) = %f, want %f", tt.a, tt.b, result, tt.expected)
		}
	}
}

func TestCalculateDiversity(t *testing.T) {
	// Uniform population
	uniform := Population{
		{Genes: []float64{0, 0, 0}, Fitness: 1},
		{Genes: []float64{10, 10, 10}, Fitness: 1},
		{Genes: []float64{5, 5, 5}, Fitness: 1},
	}

	// Clustered population
	clustered := Population{
		{Genes: []float64{4.9, 4.9, 4.9}, Fitness: 1},
		{Genes: []float64{5.0, 5.0, 5.0}, Fitness: 1},
		{Genes: []float64{5.1, 5.1, 5.1}, Fitness: 1},
	}

	diversityUniform := CalculateDiversity(uniform)
	diversityClustered := CalculateDiversity(clustered)

	if diversityUniform <= diversityClustered {
		t.Error("CalculateDiversity() should show higher diversity for uniform population")
	}

	// Empty population
	empty := Population{}
	if CalculateDiversity(empty) != 0 {
		t.Error("CalculateDiversity() should return 0 for empty population")
	}

	// Single individual
	single := Population{{Genes: []float64{1, 1, 1}}}
	if CalculateDiversity(single) != 0 {
		t.Error("CalculateDiversity() should return 0 for single individual")
	}
}

func TestGetBestIndividual(t *testing.T) {
	population := Population{
		{Genes: []float64{1}, Fitness: 0.1},
		{Genes: []float64{2}, Fitness: 0.9},
		{Genes: []float64{3}, Fitness: 0.5},
	}

	best := GetBestIndividual(population)
	if best.Fitness != 0.9 {
		t.Errorf("GetBestIndividual() fitness = %f, want 0.9", best.Fitness)
	}

	// Empty population
	empty := Population{}
	if GetBestIndividual(empty) != nil {
		t.Error("GetBestIndividual() should return nil for empty population")
	}
}

func TestGetWorstIndividual(t *testing.T) {
	population := Population{
		{Genes: []float64{1}, Fitness: 0.1},
		{Genes: []float64{2}, Fitness: 0.9},
		{Genes: []float64{3}, Fitness: 0.5},
	}

	worst := GetWorstIndividual(population)
	if worst.Fitness != 0.1 {
		t.Errorf("GetWorstIndividual() fitness = %f, want 0.1", worst.Fitness)
	}

	// Empty population
	empty := Population{}
	if GetWorstIndividual(empty) != nil {
		t.Error("GetWorstIndividual() should return nil for empty population")
	}
}

// ===== Multi-Objective Tests =====

func TestDominates(t *testing.T) {
	// a dominates b (better in all objectives)
	a := &MultiObjectiveIndividual{Objectives: []float64{1, 2}}
	b := &MultiObjectiveIndividual{Objectives: []float64{2, 3}}

	if !a.Dominates(b) {
		t.Error("a should dominate b (all objectives better)")
	}
	if b.Dominates(a) {
		t.Error("b should not dominate a")
	}

	// a does not dominate c (mixed objectives)
	c := &MultiObjectiveIndividual{Objectives: []float64{0.5, 4}}
	if a.Dominates(c) {
		t.Error("a should not dominate c (mixed objectives)")
	}
	if c.Dominates(a) {
		t.Error("c should not dominate a (mixed objectives)")
	}

	// Equal objectives
	d := &MultiObjectiveIndividual{Objectives: []float64{1, 2}}
	if a.Dominates(d) || d.Dominates(a) {
		t.Error("Equal solutions should not dominate each other")
	}
}

func TestFastNonDominatedSort(t *testing.T) {
	// Create a simple population with known Pareto front
	population := []*MultiObjectiveIndividual{
		{Genes: []float64{1}, Objectives: []float64{1, 5}}, // Front 1
		{Genes: []float64{2}, Objectives: []float64{2, 4}}, // Front 1
		{Genes: []float64{3}, Objectives: []float64{3, 3}}, // Front 1
		{Genes: []float64{4}, Objectives: []float64{4, 4}}, // Front 2
		{Genes: []float64{5}, Objectives: []float64{5, 2}}, // Front 1
		{Genes: []float64{6}, Objectives: []float64{6, 1}}, // Front 1
	}

	fronts := FastNonDominatedSort(population)

	if len(fronts) == 0 {
		t.Fatal("FastNonDominatedSort() returned empty fronts")
	}

	// First front should have the non-dominated solutions
	for _, ind := range fronts[0] {
		if ind.Rank != 0 {
			t.Errorf("First front individual has rank %d, want 0", ind.Rank)
		}
	}

	// Check that individuals in front 1 have rank 0
	if len(fronts[0]) < 3 {
		t.Errorf("First front should have at least 3 individuals, got %d", len(fronts[0]))
	}
}

func TestCalculateCrowdingDistance(t *testing.T) {
	front := ParetoFront{
		{Objectives: []float64{1, 5}},
		{Objectives: []float64{2, 4}},
		{Objectives: []float64{3, 3}},
		{Objectives: []float64{4, 2}},
		{Objectives: []float64{5, 1}},
	}

	CalculateCrowdingDistance(front)

	// Boundary solutions should have infinite crowding distance
	if !math.IsInf(front[0].Crowding, 1) {
		t.Errorf("First individual crowding = %f, want +Inf", front[0].Crowding)
	}
	if !math.IsInf(front[4].Crowding, 1) {
		t.Errorf("Last individual crowding = %f, want +Inf", front[4].Crowding)
	}

	// Middle solutions should have finite crowding distance
	for i := 1; i < 4; i++ {
		if math.IsInf(front[i].Crowding, 0) {
			t.Errorf("Middle individual %d crowding should be finite", i)
		}
	}
}

// ===== Integration Tests =====

func TestGeneticAlgorithmSphere(t *testing.T) {
	config := Config{
		PopulationSize:  50,
		GeneCount:        5,
		Generations:      100,
		CrossoverRate:    0.8,
		MutationRate:     0.1,
		EliteCount:       2,
		TournamentSize:   3,
		GeneBounds:       Bound{Min: -5, Max: 5},
		ConvergenceGen:   20,
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, err := New(config, SphereFunction)
	if err != nil {
		t.Fatalf("Failed to create genetic algorithm: %v", err)
	}

	result := ga.Run()

	// Should find solution close to 0 (negated fitness close to 0)
	// The fitness is negative (negated sphere function), so we check absolute value
	if math.Abs(result.BestFitness) > 0.5 {
		t.Errorf("Sphere optimization: best fitness = %f, should be close to 0", result.BestFitness)
	}

	// Check genes are reasonably close to 0
	for i, gene := range result.BestIndividual.Genes {
		if math.Abs(gene) > 1.0 {
			t.Errorf("Sphere optimization: gene[%d] = %f, should be reasonably close to 0", i, gene)
		}
	}
}

func TestGeneticAlgorithmRastrigin(t *testing.T) {
	config := Config{
		PopulationSize:  100,
		GeneCount:        2,
		Generations:      200,
		CrossoverRate:    0.9,
		MutationRate:     0.05,
		EliteCount:       5,
		TournamentSize:   4,
		GeneBounds:       Bound{Min: -5.12, Max: 5.12},
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, err := New(config, RastriginFunction)
	if err != nil {
		t.Fatalf("Failed to create genetic algorithm: %v", err)
	}

	result := ga.Run()

	// Rastrigin is harder, but should find a reasonable solution
	if result.BestFitness < -30 {
		t.Errorf("Rastrigin optimization: best fitness = %f, should be better", result.BestFitness)
	}
}

func TestGeneticAlgorithmWithCustomCrossoverMutation(t *testing.T) {
	config := Config{
		PopulationSize:  30,
		GeneCount:        3,
		Generations:      50,
		CrossoverRate:    0.8,
		MutationRate:     0.1,
		EliteCount:       2,
		TournamentSize:   3,
		GeneBounds:       Bound{Min: -5, Max: 5},
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, err := New(config, SphereFunction)
	if err != nil {
		t.Fatalf("Failed to create genetic algorithm: %v", err)
	}

	// Use custom crossover and mutation
	ga.CrossoverFunc = ArithmeticCrossover
	ga.MutationFunc = PolynomialMutation

	result := ga.Run()

	// Should find a reasonable solution
	if math.Abs(result.BestFitness) > 1.0 {
		t.Errorf("Custom crossover/mutation: best fitness = %f, should be better", result.BestFitness)
	}
}

func TestGeneticAlgorithmMinFitness(t *testing.T) {
	config := Config{
		PopulationSize:  50,
		GeneCount:        5,
		Generations:      1000, // High generation count
		CrossoverRate:    0.8,
		MutationRate:     0.1,
		EliteCount:       2,
		TournamentSize:   3,
		GeneBounds:       Bound{Min: -5, Max: 5},
		MinFitness:       -0.01, // Stop early when this fitness is reached
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, err := New(config, SphereFunction)
	if err != nil {
		t.Fatalf("Failed to create genetic algorithm: %v", err)
	}

	result := ga.Run()

	// Should have stopped early
	if result.TotalGenerations >= 1000 {
		t.Error("Should have stopped early due to MinFitness")
	}

	if result.BestFitness < config.MinFitness {
		t.Errorf("Best fitness = %f, should have reached MinFitness = %f", result.BestFitness, config.MinFitness)
	}
}

func TestGeneticAlgorithmFitnessHistory(t *testing.T) {
	config := Config{
		PopulationSize:  20,
		GeneCount:        2,
		Generations:      10,
		CrossoverRate:    0.8,
		MutationRate:     0.1,
		EliteCount:       1,
		TournamentSize:   2,
		GeneBounds:       Bound{Min: -5, Max: 5},
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, err := New(config, SphereFunction)
	if err != nil {
		t.Fatalf("Failed to create genetic algorithm: %v", err)
	}

	result := ga.Run()

	if len(result.FitnessHistory) != config.Generations {
		t.Errorf("Fitness history length = %d, want %d", len(result.FitnessHistory), config.Generations)
	}

	if len(result.AvgFitnessHistory) != config.Generations {
		t.Errorf("Average fitness history length = %d, want %d", len(result.AvgFitnessHistory), config.Generations)
	}

	// Fitness should generally improve (not strictly monotonic due to randomness)
	finalFitness := result.FitnessHistory[len(result.FitnessHistory)-1]
	initialFitness := result.FitnessHistory[0]

	if finalFitness < initialFitness {
		t.Errorf("Final fitness = %f should be >= initial fitness = %f", finalFitness, initialFitness)
	}
}

// ===== Edge Case Tests =====

func TestGeneticAlgorithmSmallPopulation(t *testing.T) {
	config := Config{
		PopulationSize:  5, // Small population
		GeneCount:        2,
		Generations:      20,
		CrossoverRate:    0.8,
		MutationRate:     0.1,
		EliteCount:       1,
		TournamentSize:   2,
		GeneBounds:       Bound{Min: -5, Max: 5},
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, err := New(config, SphereFunction)
	if err != nil {
		t.Fatalf("Failed to create genetic algorithm: %v", err)
	}

	result := ga.Run()

	if result == nil {
		t.Error("Should return a result even with small population")
	}
}

func TestGeneticAlgorithmSingleGene(t *testing.T) {
	config := Config{
		PopulationSize:  20,
		GeneCount:        1, // Single gene
		Generations:      30,
		CrossoverRate:    0.8,
		MutationRate:     0.1,
		EliteCount:       1,
		TournamentSize:   2,
		GeneBounds:       Bound{Min: -5, Max: 5},
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, err := New(config, SphereFunction)
	if err != nil {
		t.Fatalf("Failed to create genetic algorithm: %v", err)
	}

	result := ga.Run()

	if len(result.BestIndividual.Genes) != 1 {
		t.Errorf("Should have 1 gene, got %d", len(result.BestIndividual.Genes))
	}
}

func TestGeneticAlgorithmZeroMutation(t *testing.T) {
	config := Config{
		PopulationSize:  20,
		GeneCount:        2,
		Generations:      10,
		CrossoverRate:    0.8,
		MutationRate:     0, // No mutation
		EliteCount:       1,
		TournamentSize:   2,
		GeneBounds:       Bound{Min: -5, Max: 5},
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, err := New(config, SphereFunction)
	if err != nil {
		t.Fatalf("Failed to create genetic algorithm: %v", err)
	}

	result := ga.Run()

	if result == nil {
		t.Error("Should return a result even with zero mutation rate")
	}
}

func TestGeneticAlgorithmNoCrossover(t *testing.T) {
	config := Config{
		PopulationSize:  20,
		GeneCount:        2,
		Generations:      10,
		CrossoverRate:    0, // No crossover
		MutationRate:     0.1,
		EliteCount:       1,
		TournamentSize:   2,
		GeneBounds:       Bound{Min: -5, Max: 5},
		Verbose:         false,
		RandomSeed:      42,
	}

	ga, err := New(config, SphereFunction)
	if err != nil {
		t.Fatalf("Failed to create genetic algorithm: %v", err)
	}

	result := ga.Run()

	if result == nil {
		t.Error("Should return a result even with zero crossover rate")
	}
}

func TestGeneticAlgorithmAllElites(t *testing.T) {
	// This should error - can't have all individuals as elites
	config := Config{
		PopulationSize:  20,
		GeneCount:        2,
		Generations:      10,
		CrossoverRate:    0.8,
		MutationRate:     0.1,
		EliteCount:       20, // All individuals
		TournamentSize:   2,
		GeneBounds:       Bound{Min: -5, Max: 5},
		Verbose:         false,
		RandomSeed:      42,
	}

	_, err := New(config, SphereFunction)
	if err == nil {
		t.Error("Should error when elite count equals population size")
	}
}

func TestGeneticAlgorithmPerGeneBounds(t *testing.T) {
	config := Config{
		PopulationSize:  20,
		GeneCount:        3,
		Generations:      10,
		CrossoverRate:    0.8,
		MutationRate:     0.5, // High mutation to test bounds
		EliteCount:       1,
		TournamentSize:   2,
		Bounds: []Bound{
			{Min: -10, Max: -5}, // Negative range
			{Min: 0, Max: 10},   // Positive range
			{Min: -5, Max: 5},   // Mixed range
		},
		Verbose:    false,
		RandomSeed: 42,
	}

	ga, err := New(config, SphereFunction)
	if err != nil {
		t.Fatalf("Failed to create genetic algorithm: %v", err)
	}

	result := ga.Run()

	// Check all genes are within bounds
	for i, gene := range result.BestIndividual.Genes {
		if gene < config.Bounds[i].Min || gene > config.Bounds[i].Max {
			t.Errorf("Gene[%d] = %f, out of bounds [%f, %f]", i, gene, config.Bounds[i].Min, config.Bounds[i].Max)
		}
	}
}

// Benchmark tests
func BenchmarkGeneticAlgorithmSphere(b *testing.B) {
	config := Config{
		PopulationSize:  100,
		GeneCount:        10,
		Generations:      50,
		CrossoverRate:    0.8,
		MutationRate:     0.1,
		EliteCount:       2,
		TournamentSize:   3,
		GeneBounds:       Bound{Min: -5, Max: 5},
		Verbose:         false,
		RandomSeed:      42,
	}

	for i := 0; i < b.N; i++ {
		ga, _ := New(config, SphereFunction)
		ga.Run()
	}
}

func BenchmarkTournamentSelection(b *testing.B) {
	population := make(Population, 100)
	for i := range population {
		population[i] = &Individual{
			Genes:   []float64{rand.Float64(), rand.Float64()},
			Fitness: rand.Float64(),
		}
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		TournamentSelection(population, 3)
	}
}

func BenchmarkUniformCrossover(b *testing.B) {
	parent1 := &Individual{Genes: []float64{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}
	parent2 := &Individual{Genes: []float64{10, 9, 8, 7, 6, 5, 4, 3, 2, 1}}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		UniformCrossover(parent1, parent2, 0.5)
	}
}

func BenchmarkGaussianMutation(b *testing.B) {
	individual := &Individual{Genes: []float64{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}
	bounds := make([]Bound, 10)
	for i := range bounds {
		bounds[i] = Bound{Min: -10, Max: 10}
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		GaussianMutation(individual, 0.1, bounds)
	}
}