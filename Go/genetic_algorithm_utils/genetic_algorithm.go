// Package genetica provides a genetic algorithm implementation for optimization problems.
// Genetic algorithms are inspired by natural selection and use techniques such as
// selection, crossover, and mutation to evolve solutions.
package genetica

import (
	"errors"
	"fmt"
	"math"
	"math/rand"
	"sort"
)

// Individual represents a candidate solution in the population.
type Individual struct {
	Genes    []float64 // The genetic representation of the solution
	Fitness  float64   // The fitness score (higher is better)
	Age      int       // Age of the individual (for aging mechanisms)
	Elite    bool      // Whether this individual is an elite
}

// Population is a collection of individuals.
type Population []*Individual

// FitnessFunc calculates the fitness of an individual.
// Higher fitness values indicate better solutions.
type FitnessFunc func(genes []float64) float64

// CrossoverFunc performs crossover between two parents to produce offspring.
type CrossoverFunc func(parent1, parent2 *Individual, crossoverRate float64) (*Individual, *Individual)

// MutationFunc mutates an individual's genes.
type MutationFunc func(individual *Individual, mutationRate float64, bounds []Bound)

// SelectionFunc selects individuals from the population for reproduction.
type SelectionFunc func(population Population, tournamentSize int) *Individual

// Bound defines the allowed range for a gene.
type Bound struct {
	Min float64
	Max float64
}

// Config holds the genetic algorithm configuration.
type Config struct {
	PopulationSize   int       // Number of individuals in the population
	GeneCount        int       // Number of genes per individual
	Generations      int       // Maximum number of generations
	CrossoverRate    float64   // Probability of crossover (0-1)
	MutationRate     float64   // Probability of mutation per gene (0-1)
	EliteCount       int       // Number of elite individuals to preserve
	TournamentSize   int       // Tournament size for selection
	Bounds           []Bound   // Bounds for each gene (optional, will use GeneBounds if empty)
	GeneBounds       Bound     // Default bounds for all genes if Bounds is empty
	ConvergenceGen   int       // Stop if no improvement for this many generations (0 = disabled)
	MinFitness       float64   // Stop if this fitness is reached (optional)
	Verbose          bool      // Print progress information
	RandomSeed       int64     // Random seed for reproducibility (0 = use time)
}

// Result holds the result of the genetic algorithm.
type Result struct {
	BestIndividual   *Individual   // Best individual found
	BestFitness       float64       // Fitness of the best individual
	BestGeneration    int           // Generation where best was found
	TotalGenerations  int           // Total generations run
	FitnessHistory    []float64     // Best fitness per generation
	AvgFitnessHistory []float64     // Average fitness per generation
	Population        Population    // Final population
	Converged         bool          // Whether the algorithm converged
}

// GeneticAlgorithm implements the genetic algorithm.
type GeneticAlgorithm struct {
	Config         Config
	FitnessFunc    FitnessFunc
	CrossoverFunc  CrossoverFunc
	MutationFunc   MutationFunc
	SelectionFunc  SelectionFunc
	population     Population
	generation     int
	bestEver       *Individual
	stagnantGens   int
	rng            *rand.Rand
}

// New creates a new GeneticAlgorithm with the given configuration and fitness function.
func New(config Config, fitnessFunc FitnessFunc) (*GeneticAlgorithm, error) {
	if err := validateConfig(&config); err != nil {
		return nil, err
	}

	seed := config.RandomSeed
	if seed == 0 {
		seed = rand.Int63()
	}

	ga := &GeneticAlgorithm{
		Config:        config,
		FitnessFunc:   fitnessFunc,
		CrossoverFunc: UniformCrossover,
		MutationFunc:  GaussianMutation,
		SelectionFunc: TournamentSelection,
		rng:           rand.New(rand.NewSource(seed)),
	}

	ga.initializePopulation()
	return ga, nil
}

// validateConfig validates the genetic algorithm configuration.
func validateConfig(config *Config) error {
	if config.PopulationSize < 2 {
		return errors.New("population size must be at least 2")
	}
	if config.GeneCount < 1 {
		return errors.New("gene count must be at least 1")
	}
	if config.Generations < 1 {
		return errors.New("generations must be at least 1")
	}
	if config.CrossoverRate < 0 || config.CrossoverRate > 1 {
		return errors.New("crossover rate must be between 0 and 1")
	}
	if config.MutationRate < 0 || config.MutationRate > 1 {
		return errors.New("mutation rate must be between 0 and 1")
	}
	if config.EliteCount < 0 || config.EliteCount >= config.PopulationSize {
		return errors.New("elite count must be between 0 and population size - 1")
	}
	if config.TournamentSize < 1 {
		config.TournamentSize = 3
	}
	if config.TournamentSize > config.PopulationSize {
		config.TournamentSize = config.PopulationSize
	}
	if config.Bounds == nil || len(config.Bounds) == 0 {
		config.Bounds = make([]Bound, config.GeneCount)
		for i := 0; i < config.GeneCount; i++ {
			config.Bounds[i] = config.GeneBounds
		}
	}
	if len(config.Bounds) != config.GeneCount {
		return errors.New("bounds length must match gene count")
	}
	return nil
}

// initializePopulation creates the initial random population.
func (ga *GeneticAlgorithm) initializePopulation() {
	ga.population = make(Population, ga.Config.PopulationSize)

	for i := 0; i < ga.Config.PopulationSize; i++ {
		individual := &Individual{
			Genes: make([]float64, ga.Config.GeneCount),
		}
		for j := 0; j < ga.Config.GeneCount; j++ {
			bound := ga.Config.Bounds[j]
			individual.Genes[j] = bound.Min + ga.rng.Float64()*(bound.Max-bound.Min)
		}
		ga.population[i] = individual
	}

	ga.evaluatePopulation()
	ga.bestEver = ga.findBest()
}

// evaluatePopulation calculates fitness for all individuals.
func (ga *GeneticAlgorithm) evaluatePopulation() {
	for _, individual := range ga.population {
		individual.Fitness = ga.FitnessFunc(individual.Genes)
	}
}

// findBest returns the individual with the highest fitness.
func (ga *GeneticAlgorithm) findBest() *Individual {
	if len(ga.population) == 0 {
		return nil
	}
	best := ga.population[0]
	for _, individual := range ga.population[1:] {
		if individual.Fitness > best.Fitness {
			best = individual
		}
	}
	return best
}

// Run executes the genetic algorithm and returns the result.
func (ga *GeneticAlgorithm) Run() *Result {
	result := &Result{
		FitnessHistory:    make([]float64, 0, ga.Config.Generations),
		AvgFitnessHistory: make([]float64, 0, ga.Config.Generations),
	}

	for gen := 0; gen < ga.Config.Generations; gen++ {
		ga.generation = gen

		// Record statistics
		best := ga.findBest()
		avgFitness := ga.calculateAverageFitness()
		result.FitnessHistory = append(result.FitnessHistory, best.Fitness)
		result.AvgFitnessHistory = append(result.AvgFitnessHistory, avgFitness)

		// Update best ever
		if best.Fitness > ga.bestEver.Fitness {
			ga.bestEver = &Individual{
				Genes:   make([]float64, len(best.Genes)),
				Fitness: best.Fitness,
			}
			copy(ga.bestEver.Genes, best.Genes)
			result.BestGeneration = gen
			ga.stagnantGens = 0
		} else {
			ga.stagnantGens++
		}

		if ga.Config.Verbose && gen%10 == 0 {
			fmt.Printf("Generation %d: Best=%.6f, Avg=%.6f\n", gen, best.Fitness, avgFitness)
		}

		// Check stopping conditions
		if ga.Config.MinFitness != 0 && ga.bestEver.Fitness >= ga.Config.MinFitness {
			result.Converged = true
			break
		}
		if ga.Config.ConvergenceGen > 0 && ga.stagnantGens >= ga.Config.ConvergenceGen {
			result.Converged = true
			break
		}

		// Create next generation
		ga.evolve()
	}

	result.BestIndividual = &Individual{
		Genes:   make([]float64, len(ga.bestEver.Genes)),
		Fitness: ga.bestEver.Fitness,
	}
	copy(result.BestIndividual.Genes, ga.bestEver.Genes)
	result.BestFitness = ga.bestEver.Fitness
	result.TotalGenerations = ga.generation + 1
	result.Population = ga.population

	return result
}

// evolve creates the next generation.
func (ga *GeneticAlgorithm) evolve() {
	newPopulation := make(Population, 0, ga.Config.PopulationSize)

	// Sort by fitness (descending) for elitism
	sort.Slice(ga.population, func(i, j int) bool {
		return ga.population[i].Fitness > ga.population[j].Fitness
	})

	// Preserve elite individuals
	for i := 0; i < ga.Config.EliteCount; i++ {
		elite := &Individual{
			Genes:  make([]float64, len(ga.population[i].Genes)),
			Fitness: ga.population[i].Fitness,
			Age:     ga.population[i].Age + 1,
			Elite:   true,
		}
		copy(elite.Genes, ga.population[i].Genes)
		newPopulation = append(newPopulation, elite)
	}

	// Generate offspring
	for len(newPopulation) < ga.Config.PopulationSize {
		parent1 := ga.SelectionFunc(ga.population, ga.Config.TournamentSize)
		parent2 := ga.SelectionFunc(ga.population, ga.Config.TournamentSize)

		var child1, child2 *Individual
		if ga.rng.Float64() < ga.Config.CrossoverRate {
			child1, child2 = ga.CrossoverFunc(parent1, parent2, ga.Config.CrossoverRate)
		} else {
			child1 = &Individual{Genes: make([]float64, len(parent1.Genes))}
			child2 = &Individual{Genes: make([]float64, len(parent2.Genes))}
			copy(child1.Genes, parent1.Genes)
			copy(child2.Genes, parent2.Genes)
		}

		ga.MutationFunc(child1, ga.Config.MutationRate, ga.Config.Bounds)
		ga.MutationFunc(child2, ga.Config.MutationRate, ga.Config.Bounds)

		newPopulation = append(newPopulation, child1)
		if len(newPopulation) < ga.Config.PopulationSize {
			newPopulation = append(newPopulation, child2)
		}
	}

	ga.population = newPopulation
	ga.evaluatePopulation()
}

// calculateAverageFitness returns the average fitness of the population.
func (ga *GeneticAlgorithm) calculateAverageFitness() float64 {
	var sum float64
	for _, individual := range ga.population {
		sum += individual.Fitness
	}
	return sum / float64(len(ga.population))
}

// ===== Selection Methods =====

// TournamentSelection selects an individual using tournament selection.
func TournamentSelection(population Population, tournamentSize int) *Individual {
	if len(population) == 0 {
		return nil
	}

	best := population[rand.Intn(len(population))]
	for i := 1; i < tournamentSize; i++ {
		contender := population[rand.Intn(len(population))]
		if contender.Fitness > best.Fitness {
			best = contender
		}
	}
	return best
}

// RouletteWheelSelection selects an individual using fitness-proportionate selection.
func RouletteWheelSelection(population Population, _ int) *Individual {
	if len(population) == 0 {
		return nil
	}

	// Calculate total fitness
	var totalFitness float64
	for _, individual := range population {
		totalFitness += individual.Fitness
	}

	if totalFitness == 0 {
		return population[rand.Intn(len(population))]
	}

	// Spin the wheel
	spin := rand.Float64() * totalFitness
	var cumulative float64
	for _, individual := range population {
		cumulative += individual.Fitness
		if cumulative >= spin {
			return individual
		}
	}

	return population[len(population)-1]
}

// RankSelection selects an individual using rank-based selection.
func RankSelection(population Population, _ int) *Individual {
	if len(population) == 0 {
		return nil
	}

	// Sort by fitness
	sorted := make(Population, len(population))
	copy(sorted, population)
	sort.Slice(sorted, func(i, j int) bool {
		return sorted[i].Fitness > sorted[j].Fitness
	})

	// Calculate rank probabilities
	n := len(sorted)
	totalRank := n * (n + 1) / 2
	spin := rand.Intn(totalRank)

	cumulative := 0
	for i, individual := range sorted {
		cumulative += (n - i)
		if cumulative >= spin {
			return individual
		}
	}

	return sorted[0]
}

// ===== Crossover Methods =====

// SinglePointCrossover performs single-point crossover.
func SinglePointCrossover(parent1, parent2 *Individual, _ float64) (*Individual, *Individual) {
	n := len(parent1.Genes)
	if n == 0 {
		return &Individual{Genes: []float64{}}, &Individual{Genes: []float64{}}
	}

	point := rand.Intn(n)

	child1 := &Individual{Genes: make([]float64, n)}
	child2 := &Individual{Genes: make([]float64, n)}

	copy(child1.Genes, parent1.Genes[:point])
	copy(child1.Genes[point:], parent2.Genes[point:])

	copy(child2.Genes, parent2.Genes[:point])
	copy(child2.Genes[point:], parent1.Genes[point:])

	return child1, child2
}

// TwoPointCrossover performs two-point crossover.
func TwoPointCrossover(parent1, parent2 *Individual, _ float64) (*Individual, *Individual) {
	n := len(parent1.Genes)
	if n < 2 {
		return SinglePointCrossover(parent1, parent2, 0)
	}

	point1 := rand.Intn(n)
	point2 := rand.Intn(n)
	if point1 > point2 {
		point1, point2 = point2, point1
	}

	child1 := &Individual{Genes: make([]float64, n)}
	child2 := &Individual{Genes: make([]float64, n)}

	for i := 0; i < n; i++ {
		if i >= point1 && i < point2 {
			child1.Genes[i] = parent2.Genes[i]
			child2.Genes[i] = parent1.Genes[i]
		} else {
			child1.Genes[i] = parent1.Genes[i]
			child2.Genes[i] = parent2.Genes[i]
		}
	}

	return child1, child2
}

// UniformCrossover performs uniform crossover.
func UniformCrossover(parent1, parent2 *Individual, _ float64) (*Individual, *Individual) {
	n := len(parent1.Genes)

	child1 := &Individual{Genes: make([]float64, n)}
	child2 := &Individual{Genes: make([]float64, n)}

	for i := 0; i < n; i++ {
		if rand.Float64() < 0.5 {
			child1.Genes[i] = parent1.Genes[i]
			child2.Genes[i] = parent2.Genes[i]
		} else {
			child1.Genes[i] = parent2.Genes[i]
			child2.Genes[i] = parent1.Genes[i]
		}
	}

	return child1, child2
}

// ArithmeticCrossover performs arithmetic crossover (blend of parents).
func ArithmeticCrossover(parent1, parent2 *Individual, _ float64) (*Individual, *Individual) {
	n := len(parent1.Genes)
	alpha := rand.Float64()

	child1 := &Individual{Genes: make([]float64, n)}
	child2 := &Individual{Genes: make([]float64, n)}

	for i := 0; i < n; i++ {
		child1.Genes[i] = alpha*parent1.Genes[i] + (1-alpha)*parent2.Genes[i]
		child2.Genes[i] = (1-alpha)*parent1.Genes[i] + alpha*parent2.Genes[i]
	}

	return child1, child2
}

// SBXCrossover performs simulated binary crossover (SBX).
func SBXCrossover(parent1, parent2 *Individual, _ float64) (*Individual, *Individual) {
	n := len(parent1.Genes)
	eta := 2.0 // Distribution index

	child1 := &Individual{Genes: make([]float64, n)}
	child2 := &Individual{Genes: make([]float64, n)}

	for i := 0; i < n; i++ {
		u := rand.Float64()
		var beta float64

		if u <= 0.5 {
			beta = math.Pow(2*u, 1/(eta+1))
		} else {
			beta = math.Pow(1/(2*(1-u)), 1/(eta+1))
		}

		x1 := parent1.Genes[i]
		x2 := parent2.Genes[i]

		child1.Genes[i] = 0.5 * ((1 + beta) * x1 + (1 - beta) * x2)
		child2.Genes[i] = 0.5 * ((1 - beta) * x1 + (1 + beta) * x2)
	}

	return child1, child2
}

// ===== Mutation Methods =====

// GaussianMutation performs Gaussian mutation.
func GaussianMutation(individual *Individual, mutationRate float64, bounds []Bound) {
	for i := 0; i < len(individual.Genes); i++ {
		if rand.Float64() < mutationRate {
			// Gaussian mutation with standard deviation proportional to range
			range_ := bounds[i].Max - bounds[i].Min
			stdDev := range_ * 0.1
			mutation := rand.NormFloat64() * stdDev
			individual.Genes[i] += mutation

			// Clamp to bounds
			if individual.Genes[i] < bounds[i].Min {
				individual.Genes[i] = bounds[i].Min
			}
			if individual.Genes[i] > bounds[i].Max {
				individual.Genes[i] = bounds[i].Max
			}
		}
	}
}

// UniformMutation performs uniform random mutation.
func UniformMutation(individual *Individual, mutationRate float64, bounds []Bound) {
	for i := 0; i < len(individual.Genes); i++ {
		if rand.Float64() < mutationRate {
			individual.Genes[i] = bounds[i].Min + rand.Float64()*(bounds[i].Max-bounds[i].Min)
		}
	}
}

// PolynomialMutation performs polynomial mutation.
func PolynomialMutation(individual *Individual, mutationRate float64, bounds []Bound) {
	eta := 20.0 // Distribution index

	for i := 0; i < len(individual.Genes); i++ {
		if rand.Float64() < mutationRate {
			u := rand.Float64()
			delta := 0.0

			if u < 0.5 {
				delta = math.Pow(2*u, 1/(eta+1)) - 1
			} else {
				delta = 1 - math.Pow(2*(1-u), 1/(eta+1))
			}

			x := individual.Genes[i]
			range_ := bounds[i].Max - bounds[i].Min
			individual.Genes[i] = x + delta * range_

			// Clamp to bounds
			if individual.Genes[i] < bounds[i].Min {
				individual.Genes[i] = bounds[i].Min
			}
			if individual.Genes[i] > bounds[i].Max {
				individual.Genes[i] = bounds[i].Max
			}
		}
	}
}

// SwapMutation swaps two randomly selected genes.
func SwapMutation(individual *Individual, mutationRate float64, _ []Bound) {
	if rand.Float64() < mutationRate && len(individual.Genes) >= 2 {
		i := rand.Intn(len(individual.Genes))
		j := rand.Intn(len(individual.Genes))
		individual.Genes[i], individual.Genes[j] = individual.Genes[j], individual.Genes[i]
	}
}

// BoundaryMutation replaces a gene with either its minimum or maximum bound.
func BoundaryMutation(individual *Individual, mutationRate float64, bounds []Bound) {
	for i := 0; i < len(individual.Genes); i++ {
		if rand.Float64() < mutationRate {
			if rand.Float64() < 0.5 {
				individual.Genes[i] = bounds[i].Min
			} else {
				individual.Genes[i] = bounds[i].Max
			}
		}
	}
}

// ===== Utility Functions =====

// Clone creates a deep copy of an individual.
func (ind *Individual) Clone() *Individual {
	clone := &Individual{
		Genes:   make([]float64, len(ind.Genes)),
		Fitness: ind.Fitness,
		Age:     ind.Age,
		Elite:   ind.Elite,
	}
	copy(clone.Genes, ind.Genes)
	return clone
}

// String returns a string representation of an individual.
func (ind *Individual) String() string {
	return fmt.Sprintf("Individual{Fitness: %.6f, Genes: %v}", ind.Fitness, ind.Genes)
}

// GetBestIndividual returns the best individual from a population.
func GetBestIndividual(population Population) *Individual {
	if len(population) == 0 {
		return nil
	}
	best := population[0]
	for _, ind := range population[1:] {
		if ind.Fitness > best.Fitness {
			best = ind
		}
	}
	return best
}

// GetWorstIndividual returns the worst individual from a population.
func GetWorstIndividual(population Population) *Individual {
	if len(population) == 0 {
		return nil
	}
	worst := population[0]
	for _, ind := range population[1:] {
		if ind.Fitness < worst.Fitness {
			worst = ind
		}
	}
	return worst
}

// CalculateDiversity calculates the diversity of the population.
func CalculateDiversity(population Population) float64 {
	if len(population) < 2 {
		return 0
	}

	var totalDistance float64
	count := 0

	for i := 0; i < len(population); i++ {
		for j := i + 1; j < len(population); j++ {
			distance := EuclideanDistance(population[i].Genes, population[j].Genes)
			totalDistance += distance
			count++
		}
	}

	if count == 0 {
		return 0
	}
	return totalDistance / float64(count)
}

// EuclideanDistance calculates the Euclidean distance between two gene vectors.
func EuclideanDistance(a, b []float64) float64 {
	var sum float64
	for i := 0; i < len(a) && i < len(b); i++ {
		diff := a[i] - b[i]
		sum += diff * diff
	}
	return math.Sqrt(sum)
}

// ===== Benchmark Functions =====

// SphereFunction is a simple benchmark function (minimize).
func SphereFunction(genes []float64) float64 {
	var sum float64
	for _, gene := range genes {
		sum += gene * gene
	}
	return -sum // Negate for maximization
}

// RastriginFunction is a challenging multimodal benchmark function (minimize).
func RastriginFunction(genes []float64) float64 {
	var sum float64
	a := 10.0
	for _, gene := range genes {
		sum += gene*gene - a*math.Cos(2*math.Pi*gene)
	}
	return -(a*float64(len(genes)) + sum) // Negate for maximization
}

// RosenbrockFunction is a classic optimization benchmark (minimize).
func RosenbrockFunction(genes []float64) float64 {
	var sum float64
	for i := 0; i < len(genes)-1; i++ {
		sum += 100*math.Pow(genes[i+1]-genes[i]*genes[i], 2) + math.Pow(genes[i]-1, 2)
	}
	return -sum // Negate for maximization
}

// AckleyFunction is a multimodal benchmark function (minimize).
func AckleyFunction(genes []float64) float64 {
	d := float64(len(genes))
	var sum1, sum2 float64

	for _, gene := range genes {
		sum1 += gene * gene
		sum2 += math.Cos(2 * math.Pi * gene)
	}

	result := -20*math.Exp(-0.2*math.Sqrt(sum1/d)) - math.Exp(sum2/d) + 20 + math.E
	return -result // Negate for maximization
}

// GriewankFunction is another multimodal benchmark (minimize).
func GriewankFunction(genes []float64) float64 {
	var sum float64
	var prod float64 = 1.0

	for i, gene := range genes {
		sum += gene * gene
		prod *= math.Cos(gene / math.Sqrt(float64(i+1)))
	}

	result := sum/4000 - prod + 1
	return -result // Negate for maximization
}

// SchwefelFunction is a highly multimodal benchmark (minimize).
func SchwefelFunction(genes []float64) float64 {
	var sum float64
	for _, gene := range genes {
		sum -= gene * math.Sin(math.Sqrt(math.Abs(gene)))
	}
	return sum // Already framed for maximization
}

// ===== Multi-Objective Support (NSGA-II basics) =====

// MultiObjectiveIndividual represents a solution for multi-objective optimization.
type MultiObjectiveIndividual struct {
	Genes      []float64
	Objectives []float64
	Rank       int
	Crowding   float64
}

// ParetoFront represents a Pareto-optimal front.
type ParetoFront []*MultiObjectiveIndividual

// Dominates checks if individual a dominates individual b.
func (a *MultiObjectiveIndividual) Dominates(b *MultiObjectiveIndividual) bool {
	dominates := false
	for i := 0; i < len(a.Objectives); i++ {
		if a.Objectives[i] > b.Objectives[i] {
			return false // a is worse in at least one objective
		}
		if a.Objectives[i] < b.Objectives[i] {
			dominates = true // a is better in at least one objective
		}
	}
	return dominates
}

// FastNonDominatedSort performs non-dominated sorting (NSGA-II).
func FastNonDominatedSort(population []*MultiObjectiveIndividual) []ParetoFront {
	n := len(population)
	dominationCount := make([]int, n)
	dominatedSet := make([][]int, n)
	for i := range dominatedSet {
		dominatedSet[i] = make([]int, 0)
	}

	// First front
	front := make(ParetoFront, 0)

	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if population[i].Dominates(population[j]) {
				dominatedSet[i] = append(dominatedSet[i], j)
				dominationCount[j]++
			} else if population[j].Dominates(population[i]) {
				dominatedSet[j] = append(dominatedSet[j], i)
				dominationCount[i]++
			}
		}
		if dominationCount[i] == 0 {
			population[i].Rank = 0
			front = append(front, population[i])
		}
	}

	fronts := []ParetoFront{front}
	frontIdx := 0

	for len(fronts[frontIdx]) > 0 {
		nextFront := make(ParetoFront, 0)
		for _, p := range fronts[frontIdx] {
			for idx, q := range population {
				if p == q {
					for _, dIdx := range dominatedSet[idx] {
						dominationCount[dIdx]--
						if dominationCount[dIdx] == 0 {
							population[dIdx].Rank = frontIdx + 1
							nextFront = append(nextFront, population[dIdx])
						}
					}
					break
				}
			}
		}
		frontIdx++
		fronts = append(fronts, nextFront)
	}

	return fronts
}

// CalculateCrowdingDistance calculates crowding distance for NSGA-II.
func CalculateCrowdingDistance(front ParetoFront) {
	if len(front) == 0 {
		return
	}

	n := len(front)
	m := len(front[0].Objectives)

	for i := range front {
		front[i].Crowding = 0
	}

	for obj := 0; obj < m; obj++ {
		// Sort by objective
		sort.Slice(front, func(i, j int) bool {
			return front[i].Objectives[obj] < front[j].Objectives[obj]
		})

		// Boundary solutions have infinite crowding distance
		front[0].Crowding = math.Inf(1)
		front[n-1].Crowding = math.Inf(1)

		// Calculate crowding distance
		objRange := front[n-1].Objectives[obj] - front[0].Objectives[obj]
		if objRange == 0 {
			continue
		}

		for i := 1; i < n-1; i++ {
			front[i].Crowding += (front[i+1].Objectives[obj] - front[i-1].Objectives[obj]) / objRange
		}
	}
}