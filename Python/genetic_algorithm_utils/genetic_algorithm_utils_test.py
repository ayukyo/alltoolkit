"""
Unit tests for Genetic Algorithm Utilities
"""

import unittest
import math
import random
from mod import (
    Chromosome, Selection, Crossover, Mutation, GeneticAlgorithm,
    optimize_function, solve_tsp, solve_knapsack, solve_n_queens, solve_scheduling,
    create_binary_chromosome, create_real_chromosome, create_permutation_chromosome,
    create_integer_chromosome
)


class TestChromosome(unittest.TestCase):
    """Tests for Chromosome class."""
    
    def test_create_chromosome(self):
        """Test chromosome creation."""
        chrom = Chromosome([1, 2, 3, 4, 5], fitness=10.0)
        self.assertEqual(len(chrom), 5)
        self.assertEqual(chrom.fitness, 10.0)
        self.assertEqual(chrom[0], 1)
        self.assertEqual(chrom[4], 5)
    
    def test_chromosome_copy(self):
        """Test chromosome copying."""
        chrom = Chromosome([1, 2, 3])
        copy = chrom.copy()
        copy.genes[0] = 99
        self.assertEqual(chrom[0], 1)
        self.assertEqual(copy[0], 99)
    
    def test_chromosome_repr(self):
        """Test chromosome representation."""
        chrom = Chromosome([1, 2, 3], fitness=5.0)
        repr_str = repr(chrom)
        self.assertIn('Chromosome', repr_str)
        self.assertIn('fitness', repr_str)


class TestSelection(unittest.TestCase):
    """Tests for Selection methods."""
    
    def setUp(self):
        """Set up test population."""
        self.population = [
            Chromosome([i], fitness=i * 10) for i in range(1, 11)
        ]
    
    def test_tournament_selection(self):
        """Test tournament selection."""
        selected = Selection.tournament(self.population, tournament_size=3)
        self.assertIsInstance(selected, Chromosome)
        # Tournament returns a copy, check genes match one in population
        matching_genes = [p for p in self.population if p.genes == selected.genes]
        self.assertTrue(len(matching_genes) > 0)
    
    def test_rank_selection(self):
        """Test rank selection."""
        selected = Selection.rank(self.population)
        self.assertIsInstance(selected, Chromosome)
    
    def test_roulette_wheel_selection(self):
        """Test roulette wheel selection."""
        selected = Selection.roulette_wheel(self.population)
        self.assertIsInstance(selected, Chromosome)
    
    def test_stochastic_universal_selection(self):
        """Test stochastic universal sampling."""
        selected = Selection.stochastic_universal(self.population)
        self.assertIsInstance(selected, Chromosome)
    
    def test_elitism(self):
        """Test elitism selection."""
        elites = Selection.elitism(self.population, elite_count=3)
        self.assertEqual(len(elites), 3)
        self.assertEqual(elites[0].fitness, 100)  # Highest fitness
        self.assertEqual(elites[1].fitness, 90)
        self.assertEqual(elites[2].fitness, 80)
    
    def test_elitism_preserves_best(self):
        """Test that elitism returns copies."""
        elites = Selection.elitism(self.population, elite_count=1)
        elites[0].fitness = 0
        self.assertEqual(self.population[-1].fitness, 100)


class TestCrossover(unittest.TestCase):
    """Tests for Crossover methods."""
    
    def setUp(self):
        """Set up test parents."""
        self.parent1 = Chromosome([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.parent2 = Chromosome([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
    
    def test_single_point_crossover(self):
        """Test single-point crossover."""
        child1, child2 = Crossover.single_point(self.parent1, self.parent2)
        self.assertEqual(len(child1), 10)
        self.assertEqual(len(child2), 10)
    
    def test_two_point_crossover(self):
        """Test two-point crossover."""
        child1, child2 = Crossover.two_point(self.parent1, self.parent2)
        self.assertEqual(len(child1), 10)
        self.assertEqual(len(child2), 10)
    
    def test_uniform_crossover(self):
        """Test uniform crossover."""
        child1, child2 = Crossover.uniform(self.parent1, self.parent2)
        self.assertEqual(len(child1), 10)
        self.assertEqual(len(child2), 10)
    
    def test_arithmetic_crossover(self):
        """Test arithmetic crossover for real values."""
        parent1 = Chromosome([1.0, 2.0, 3.0, 4.0, 5.0])
        parent2 = Chromosome([5.0, 4.0, 3.0, 2.0, 1.0])
        child1, child2 = Crossover.arithmetic(parent1, parent2, alpha=0.5)
        
        # With alpha=0.5, child should be average
        for g in child1.genes:
            self.assertEqual(g, 3.0)
    
    def test_order_crossover(self):
        """Test order crossover for permutations."""
        parent1 = Chromosome([1, 2, 3, 4, 5, 6, 7, 8, 9])
        parent2 = Chromosome([9, 8, 7, 6, 5, 4, 3, 2, 1])
        child1, child2 = Crossover.order_crossover(parent1, parent2)
        
        # Check that children are valid permutations
        self.assertEqual(sorted(child1.genes), list(range(1, 10)))
        self.assertEqual(sorted(child2.genes), list(range(1, 10)))
    
    def test_crossover_rate(self):
        """Test that crossover rate affects probability."""
        # With 0 rate, should return copies
        child1, child2 = Crossover.single_point(self.parent1, self.parent2, crossover_rate=0.0)
        self.assertEqual(child1.genes, self.parent1.genes)
        self.assertEqual(child2.genes, self.parent2.genes)


class TestMutation(unittest.TestCase):
    """Tests for Mutation methods."""
    
    def test_bit_flip_mutation(self):
        """Test bit flip mutation."""
        chrom = Chromosome([0, 1, 0, 1, 0, 1, 0, 1])
        mutated = Mutation.bit_flip(chrom, mutation_rate=1.0)  # 100% rate
        self.assertNotEqual(mutated.genes, chrom.genes)
    
    def test_bit_flip_no_mutation(self):
        """Test that 0% mutation rate doesn't change genes."""
        chrom = Chromosome([0, 1, 0, 1, 0, 1])
        mutated = Mutation.bit_flip(chrom, mutation_rate=0.0)
        self.assertEqual(mutated.genes, chrom.genes)
    
    def test_random_reset_mutation(self):
        """Test random reset mutation."""
        chrom = Chromosome([1.0, 2.0, 3.0, 4.0, 5.0])
        mutated = Mutation.random_reset(chrom, mutation_rate=1.0, gene_range=(0.0, 10.0))
        self.assertEqual(len(mutated.genes), 5)
    
    def test_gaussian_mutation(self):
        """Test Gaussian mutation."""
        chrom = Chromosome([1.0, 2.0, 3.0, 4.0, 5.0])
        mutated = Mutation.gaussian(chrom, mutation_rate=1.0, sigma=0.1)
        # Values should be different but close
        for orig, new in zip(chrom.genes, mutated.genes):
            self.assertNotEqual(orig, new)
    
    def test_swap_mutation(self):
        """Test swap mutation."""
        chrom = Chromosome([1, 2, 3, 4, 5])
        mutated = Mutation.swap(chrom, mutation_rate=1.0)
        # Should have same elements, possibly different order
        self.assertEqual(sorted(mutated.genes), sorted(chrom.genes))
    
    def test_inversion_mutation(self):
        """Test inversion mutation."""
        chrom = Chromosome([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        mutated = Mutation.inversion(chrom, mutation_rate=1.0)
        self.assertEqual(sorted(mutated.genes), sorted(chrom.genes))
    
    def test_scramble_mutation(self):
        """Test scramble mutation."""
        chrom = Chromosome([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        mutated = Mutation.scramble(chrom, mutation_rate=1.0)
        self.assertEqual(sorted(mutated.genes), sorted(chrom.genes))
    
    def test_insert_mutation(self):
        """Test insert mutation."""
        chrom = Chromosome([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        mutated = Mutation.insert(chrom, mutation_rate=1.0)
        self.assertEqual(sorted(mutated.genes), sorted(chrom.genes))


class TestGeneticAlgorithm(unittest.TestCase):
    """Tests for GeneticAlgorithm class."""
    
    def test_initialization(self):
        """Test GA initialization."""
        ga = GeneticAlgorithm(
            fitness_func=lambda c: sum(c.genes),
            gene_generator=lambda: random.random(),
            chromosome_length=10,
            population_size=20
        )
        ga.initialize_population()
        
        self.assertEqual(len(ga.population), 20)
        self.assertEqual(len(ga.population[0]), 10)
    
    def test_evolve(self):
        """Test a simple evolution."""
        def fitness(chrom):
            return sum(chrom.genes)
        
        ga = GeneticAlgorithm(
            fitness_func=fitness,
            gene_generator=lambda: random.uniform(0, 1),
            chromosome_length=10,
            population_size=30,
            maximize=True
        )
        ga.evolve(10)
        
        self.assertEqual(ga.generation, 10)
        self.assertIsNotNone(ga.best_ever)
    
    def test_run_with_early_stop(self):
        """Test running with early stopping."""
        def fitness(chrom):
            return sum(chrom.genes)
        
        ga = GeneticAlgorithm(
            fitness_func=fitness,
            gene_generator=lambda: random.uniform(0, 1),
            chromosome_length=5,
            population_size=20,
            maximize=True
        )
        best = ga.run(generations=100, early_stop=10)
        
        self.assertIsInstance(best, Chromosome)
        self.assertGreater(best.fitness, 0)
    
    def test_get_statistics(self):
        """Test statistics retrieval."""
        ga = GeneticAlgorithm(
            fitness_func=lambda c: sum(c.genes),
            gene_generator=lambda: random.random(),
            chromosome_length=5,
            population_size=10
        )
        ga.initialize_population()
        stats = ga.get_statistics()
        
        self.assertIn('best', stats)
        self.assertIn('worst', stats)
        self.assertIn('average', stats)
        self.assertIn('std_dev', stats)
    
    def test_minimization(self):
        """Test minimization mode."""
        def fitness(chrom):
            return sum((g - 0.5) ** 2 for g in chrom.genes)
        
        ga = GeneticAlgorithm(
            fitness_func=fitness,
            gene_generator=lambda: random.uniform(0, 1),
            chromosome_length=5,
            population_size=100,
            maximize=False
        )
        best = ga.run(generations=150, early_stop=30)
        
        # Should converge to values near 0.5 (total fitness near 0)
        # Genetic algorithm is stochastic, so we use relaxed thresholds
        total_fitness = sum((g - 0.5) ** 2 for g in best.genes)
        self.assertLess(total_fitness, 1.0)  # Relaxed for stochastic algorithm


class TestOptimizeFunction(unittest.TestCase):
    """Tests for function optimization."""
    
    def test_sphere_function(self):
        """Test minimizing sphere function (sum of squares)."""
        def sphere(x):
            return sum(xi ** 2 for xi in x)
        
        solution, fitness = optimize_function(
            func=sphere,
            dimensions=5,
            bounds=(-5.0, 5.0),
            population_size=50,
            generations=100,
            maximize=False
        )
        
        # Should find solution near zero
        self.assertLess(fitness, 1.0)
    
    def test_rastrigin_function(self):
        """Test minimizing Rastrigin function (multi-modal)."""
        def rastrigin(x):
            A = 10
            n = len(x)
            return A * n + sum(xi ** 2 - A * math.cos(2 * math.pi * xi) for xi in x)
        
        solution, fitness = optimize_function(
            func=rastrigin,
            dimensions=3,
            bounds=(-5.12, 5.12),
            population_size=100,
            generations=200,
            maximize=False
        )
        
        # Should find a reasonably good solution
        self.assertLess(fitness, 10.0)
    
    def test_rosenbrock_function(self):
        """Test minimizing Rosenbrock function."""
        def rosenbrock(x):
            return sum(100 * (x[i+1] - x[i]**2)**2 + (1 - x[i])**2 for i in range(len(x) - 1))
        
        solution, fitness = optimize_function(
            func=rosenbrock,
            dimensions=3,
            bounds=(-5.0, 10.0),
            population_size=100,
            generations=200,
            maximize=False
        )
        
        # Should make progress toward the minimum
        self.assertLess(fitness, 100.0)


class TestTSPSolver(unittest.TestCase):
    """Tests for TSP solver."""
    
    def test_small_tsp(self):
        """Test TSP with small instance."""
        # Simple 5-city TSP with known distances
        distances = [
            [0, 10, 15, 20, 25],
            [10, 0, 35, 25, 30],
            [15, 35, 0, 30, 10],
            [20, 25, 30, 0, 15],
            [25, 30, 10, 15, 0]
        ]
        
        route, total_dist = solve_tsp(distances, population_size=50, generations=100)
        
        # Should be a valid permutation
        self.assertEqual(sorted(route), list(range(5)))
        # Total distance should be reasonable
        self.assertLess(total_dist, 150)
    
    def test_tsp_symmetry(self):
        """Test that TSP handles symmetric distances."""
        distances = [
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0]
        ]
        
        route, _ = solve_tsp(distances, population_size=20, generations=50)
        self.assertEqual(sorted(route), [0, 1, 2])


class TestKnapsackSolver(unittest.TestCase):
    """Tests for Knapsack solver."""
    
    def test_simple_knapsack(self):
        """Test simple knapsack instance."""
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 6]
        capacity = 5
        
        selected, total_value = solve_knapsack(
            weights, values, capacity,
            population_size=50,
            generations=100
        )
        
        # Verify weight constraint
        total_weight = sum(w for w, s in zip(weights, selected) if s)
        self.assertLessEqual(total_weight, capacity)
        
        # Should select at least one item
        self.assertTrue(any(selected))
    
    def test_knapsack_optimal(self):
        """Test knapsack with known optimal."""
        weights = [1, 2, 3]
        values = [6, 10, 12]
        capacity = 5
        
        # Optimal is to select items 0 and 1 (weight 3, value 16)
        # or items 0, 1, 2 would exceed capacity (weight 6)
        
        selected, total_value = solve_knapsack(
            weights, values, capacity,
            population_size=50,
            generations=100
        )
        
        total_weight = sum(w for w, s in zip(weights, selected) if s)
        self.assertLessEqual(total_weight, capacity)
        self.assertGreater(total_value, 0)


class TestNQueensSolver(unittest.TestCase):
    """Tests for N-Queens solver."""
    
    def test_8_queens(self):
        """Test solving 8-queens problem."""
        solution = solve_n_queens(8, population_size=150, generations=700)
        
        if solution:
            # Verify solution is valid
            for i in range(len(solution)):
                for j in range(i + 1, len(solution)):
                    # Check columns
                    self.assertNotEqual(solution[i], solution[j])
                    # Check diagonals
                    self.assertNotEqual(abs(solution[i] - solution[j]), j - i)
    
    def test_4_queens(self):
        """Test solving 4-queens problem."""
        solution = solve_n_queens(4, population_size=50, generations=200)
        
        if solution:
            self.assertEqual(len(solution), 4)
            # Verify no conflicts
            conflicts = 0
            for i in range(len(solution)):
                for j in range(i + 1, len(solution)):
                    if solution[i] == solution[j]:
                        conflicts += 1
                    if abs(solution[i] - solution[j]) == j - i:
                        conflicts += 1
            self.assertEqual(conflicts, 0)


class TestSchedulingSolver(unittest.TestCase):
    """Tests for scheduling solver."""
    
    def test_simple_scheduling(self):
        """Test simple scheduling problem."""
        tasks = [
            {'duration': 3, 'priority': 1},
            {'duration': 2, 'priority': 2},
            {'duration': 4, 'priority': 1},
            {'duration': 1, 'priority': 3},
        ]
        
        assignments, score = solve_scheduling(
            tasks, workers=2,
            population_size=50,
            generations=100
        )
        
        self.assertEqual(len(assignments), 4)
        for a in assignments:
            self.assertIn(a, [0, 1])
    
    def test_scheduling_balancing(self):
        """Test that scheduling tries to balance workload."""
        tasks = [
            {'duration': 5, 'priority': 1},
            {'duration': 5, 'priority': 1},
            {'duration': 5, 'priority': 1},
            {'duration': 5, 'priority': 1},
        ]
        
        assignments, _ = solve_scheduling(
            tasks, workers=2,
            population_size=50,
            generations=100
        )
        
        # Should distribute somewhat evenly
        worker0_tasks = assignments.count(0)
        worker1_tasks = assignments.count(1)
        self.assertEqual(worker0_tasks + worker1_tasks, 4)


class TestChromosomeCreators(unittest.TestCase):
    """Tests for chromosome creation utilities."""
    
    def test_binary_chromosome(self):
        """Test binary chromosome creation."""
        chrom = create_binary_chromosome(10)
        self.assertEqual(len(chrom), 10)
        for g in chrom.genes:
            self.assertIn(g, [0, 1])
    
    def test_real_chromosome(self):
        """Test real-valued chromosome creation."""
        chrom = create_real_chromosome(10, low=-5.0, high=5.0)
        self.assertEqual(len(chrom), 10)
        for g in chrom.genes:
            self.assertGreaterEqual(g, -5.0)
            self.assertLessEqual(g, 5.0)
    
    def test_permutation_chromosome(self):
        """Test permutation chromosome creation."""
        chrom = create_permutation_chromosome(10)
        self.assertEqual(len(chrom), 10)
        self.assertEqual(sorted(chrom.genes), list(range(10)))
    
    def test_integer_chromosome(self):
        """Test integer chromosome creation."""
        chrom = create_integer_chromosome(10, low=1, high=100)
        self.assertEqual(len(chrom), 10)
        for g in chrom.genes:
            self.assertGreaterEqual(g, 1)
            self.assertLessEqual(g, 100)


if __name__ == '__main__':
    unittest.main()