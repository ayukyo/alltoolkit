"""
Genetic Algorithm Utilities

A comprehensive, zero-dependency implementation of genetic algorithms for optimization problems.
Includes multiple selection, crossover, and mutation strategies.
"""

import random
import math
import copy
from typing import Any, Callable, List, Optional, Tuple, TypeVar, Generic, Union

T = TypeVar('T')


class Chromosome(Generic[T]):
    """Represents a single chromosome in the population."""
    
    def __init__(self, genes: List[T], fitness: float = 0.0):
        self.genes = genes
        self.fitness = fitness
        self.age = 0
    
    def __len__(self) -> int:
        return len(self.genes)
    
    def __getitem__(self, index: int) -> T:
        return self.genes[index]
    
    def __setitem__(self, index: int, value: T):
        self.genes[index] = value
    
    def copy(self) -> 'Chromosome[T]':
        return Chromosome(self.genes.copy(), self.fitness)
    
    def __repr__(self) -> str:
        return f"Chromosome(genes={self.genes[:10]}{'...' if len(self.genes) > 10 else ''}, fitness={self.fitness:.4f})"


class Selection:
    """Selection strategy implementations."""
    
    @staticmethod
    def roulette_wheel(population: List[Chromosome]) -> Chromosome:
        """
        Roulette wheel selection (fitness proportionate).
        Better for maximization problems with positive fitness.
        """
        total_fitness = sum(max(0, ind.fitness) for ind in population)
        if total_fitness == 0:
            return random.choice(population).copy()
        
        pick = random.uniform(0, total_fitness)
        current = 0
        for ind in population:
            current += max(0, ind.fitness)
            if current >= pick:
                return ind.copy()
        return population[-1].copy()
    
    @staticmethod
    def tournament(population: List[Chromosome], tournament_size: int = 3) -> Chromosome:
        """Tournament selection - select best from random subset."""
        tournament = random.sample(population, min(tournament_size, len(population)))
        return max(tournament, key=lambda x: x.fitness).copy()
    
    @staticmethod
    def rank(population: List[Chromosome]) -> Chromosome:
        """Rank selection - selection probability based on rank, not fitness."""
        sorted_pop = sorted(population, key=lambda x: x.fitness)
        n = len(sorted_pop)
        total_rank = n * (n + 1) / 2
        pick = random.uniform(0, total_rank)
        current = 0
        for i, ind in enumerate(sorted_pop):
            current += (i + 1)
            if current >= pick:
                return ind.copy()
        return sorted_pop[-1].copy()
    
    @staticmethod
    def stochastic_universal(population: List[Chromosome]) -> Chromosome:
        """Stochastic universal sampling - reduces selection bias."""
        total_fitness = sum(max(0, ind.fitness) for ind in population)
        if total_fitness == 0:
            return random.choice(population).copy()
        
        n = len(population)
        distance = total_fitness / n
        start = random.uniform(0, distance)
        pointers = [start + i * distance for i in range(n)]
        
        for ind in population:
            if pointers[0] <= max(0, ind.fitness):
                return ind.copy()
            pointers = [p - max(0, ind.fitness) for p in pointers]
        
        return random.choice(population).copy()
    
    @staticmethod
    def elitism(population: List[Chromosome], elite_count: int = 1) -> List[Chromosome]:
        """Select top individuals for guaranteed survival."""
        sorted_pop = sorted(population, key=lambda x: x.fitness, reverse=True)
        return [ind.copy() for ind in sorted_pop[:elite_count]]


class Crossover:
    """Crossover operation implementations."""
    
    @staticmethod
    def single_point(parent1: Chromosome, parent2: Chromosome, 
                      crossover_rate: float = 0.8) -> Tuple[Chromosome, Chromosome]:
        """Single-point crossover."""
        if random.random() > crossover_rate or len(parent1) < 2:
            return parent1.copy(), parent2.copy()
        
        point = random.randint(1, len(parent1) - 1)
        child1 = Chromosome(parent1.genes[:point] + parent2.genes[point:])
        child2 = Chromosome(parent2.genes[:point] + parent1.genes[point:])
        return child1, child2
    
    @staticmethod
    def two_point(parent1: Chromosome, parent2: Chromosome,
                  crossover_rate: float = 0.8) -> Tuple[Chromosome, Chromosome]:
        """Two-point crossover."""
        if random.random() > crossover_rate or len(parent1) < 3:
            return parent1.copy(), parent2.copy()
        
        points = sorted(random.sample(range(1, len(parent1)), 2))
        child1 = Chromosome(
            parent1.genes[:points[0]] + 
            parent2.genes[points[0]:points[1]] + 
            parent1.genes[points[1]:]
        )
        child2 = Chromosome(
            parent2.genes[:points[0]] + 
            parent1.genes[points[0]:points[1]] + 
            parent2.genes[points[1]:]
        )
        return child1, child2
    
    @staticmethod
    def uniform(parent1: Chromosome, parent2: Chromosome,
                crossover_rate: float = 0.8, gene_swap_prob: float = 0.5) -> Tuple[Chromosome, Chromosome]:
        """Uniform crossover - each gene swapped independently."""
        if random.random() > crossover_rate:
            return parent1.copy(), parent2.copy()
        
        child1_genes = []
        child2_genes = []
        for g1, g2 in zip(parent1.genes, parent2.genes):
            if random.random() < gene_swap_prob:
                child1_genes.append(g2)
                child2_genes.append(g1)
            else:
                child1_genes.append(g1)
                child2_genes.append(g2)
        
        return Chromosome(child1_genes), Chromosome(child2_genes)
    
    @staticmethod
    def arithmetic(parent1: Chromosome, parent2: Chromosome,
                   crossover_rate: float = 0.8, alpha: float = None) -> Tuple[Chromosome, Chromosome]:
        """
        Arithmetic crossover for real-valued genes.
        Uses blend crossover (BLX-alpha) if alpha is provided.
        """
        if random.random() > crossover_rate:
            return parent1.copy(), parent2.copy()
        
        if alpha is None:
            alpha = random.random()
        
        child1_genes = []
        child2_genes = []
        for g1, g2 in zip(parent1.genes, parent2.genes):
            if isinstance(g1, (int, float)) and isinstance(g2, (int, float)):
                child1_genes.append(alpha * g1 + (1 - alpha) * g2)
                child2_genes.append((1 - alpha) * g1 + alpha * g2)
            else:
                child1_genes.append(g1)
                child2_genes.append(g2)
        
        return Chromosome(child1_genes), Chromosome(child2_genes)
    
    @staticmethod
    def order_crossover(parent1: Chromosome, parent2: Chromosome,
                        crossover_rate: float = 0.8) -> Tuple[Chromosome, Chromosome]:
        """
        Order crossover (OX) for permutation problems like TSP.
        Preserves relative order of genes.
        """
        if random.random() > crossover_rate or len(parent1) < 2:
            return parent1.copy(), parent2.copy()
        
        n = len(parent1)
        points = sorted(random.sample(range(n), 2))
        
        def ox(p1, p2):
            child = [None] * n
            child[points[0]:points[1]] = p1.genes[points[0]:points[1]]
            fill_values = [g for g in p2.genes if g not in child[points[0]:points[1]]]
            idx = 0
            for i in range(n):
                if child[i] is None:
                    child[i] = fill_values[idx]
                    idx += 1
            return Chromosome(child)
        
        return ox(parent1, parent2), ox(parent2, parent1)


class Mutation:
    """Mutation operation implementations."""
    
    @staticmethod
    def bit_flip(chromosome: Chromosome, mutation_rate: float = 0.01) -> Chromosome:
        """Bit flip mutation for binary genes."""
        result = chromosome.copy()
        for i in range(len(result)):
            if random.random() < mutation_rate:
                if isinstance(result[i], bool):
                    result[i] = not result[i]
                elif isinstance(result[i], int):
                    result[i] = 1 - result[i]
                elif isinstance(result[i], (float, complex)):
                    result[i] = -result[i]
        return result
    
    @staticmethod
    def random_reset(chromosome: Chromosome, mutation_rate: float = 0.01,
                    gene_range: Tuple[Any, Any] = None) -> Chromosome:
        """Random reset mutation - replace gene with random value."""
        result = chromosome.copy()
        for i in range(len(result)):
            if random.random() < mutation_rate:
                if gene_range:
                    low, high = gene_range
                    if isinstance(result[i], int):
                        result[i] = random.randint(low, high)
                    elif isinstance(result[i], float):
                        result[i] = random.uniform(low, high)
                else:
                    result[i] = random.random()
        return result
    
    @staticmethod
    def gaussian(chromosome: Chromosome, mutation_rate: float = 0.01,
                 sigma: float = 0.1) -> Chromosome:
        """Gaussian mutation for real-valued genes."""
        result = chromosome.copy()
        for i in range(len(result)):
            if random.random() < mutation_rate:
                if isinstance(result[i], (int, float)):
                    result[i] += random.gauss(0, sigma)
        return result
    
    @staticmethod
    def swap(chromosome: Chromosome, mutation_rate: float = 0.01) -> Chromosome:
        """Swap mutation - exchange two random genes (good for permutations)."""
        result = chromosome.copy()
        if random.random() < mutation_rate and len(result) >= 2:
            i, j = random.sample(range(len(result)), 2)
            result.genes[i], result.genes[j] = result.genes[j], result.genes[i]
        return result
    
    @staticmethod
    def insert(chromosome: Chromosome, mutation_rate: float = 0.01) -> Chromosome:
        """Insert mutation - move gene to new position."""
        result = chromosome.copy()
        if random.random() < mutation_rate and len(result) >= 2:
            i, j = random.sample(range(len(result)), 2)
            gene = result.genes.pop(i)
            result.genes.insert(j, gene)
        return result
    
    @staticmethod
    def inversion(chromosome: Chromosome, mutation_rate: float = 0.01) -> Chromosome:
        """Inversion mutation - reverse a segment of genes."""
        result = chromosome.copy()
        if random.random() < mutation_rate and len(result) >= 2:
            i, j = sorted(random.sample(range(len(result)), 2))
            result.genes[i:j] = reversed(result.genes[i:j])
        return result
    
    @staticmethod
    def scramble(chromosome: Chromosome, mutation_rate: float = 0.01) -> Chromosome:
        """Scramble mutation - randomly shuffle a segment of genes."""
        result = chromosome.copy()
        if random.random() < mutation_rate and len(result) >= 2:
            i, j = sorted(random.sample(range(len(result)), 2))
            segment = result.genes[i:j]
            random.shuffle(segment)
            result.genes[i:j] = segment
        return result


class GeneticAlgorithm:
    """
    Main genetic algorithm implementation.
    Configurable selection, crossover, and mutation strategies.
    """
    
    def __init__(
        self,
        fitness_func: Callable[[Chromosome], float],
        gene_generator: Callable[[], Any],
        chromosome_length: int,
        population_size: int = 100,
        elite_count: int = 2,
        selection_method: str = 'tournament',
        crossover_method: str = 'single_point',
        mutation_method: str = 'gaussian',
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.1,
        tournament_size: int = 3,
        maximize: bool = True,
        gene_range: Optional[Tuple[Any, Any]] = None
    ):
        self.fitness_func = fitness_func
        self.gene_generator = gene_generator
        self.chromosome_length = chromosome_length
        self.population_size = population_size
        self.elite_count = elite_count
        self.selection_method = selection_method
        self.crossover_method = crossover_method
        self.mutation_method = mutation_method
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.maximize = maximize
        self.gene_range = gene_range
        
        self.population: List[Chromosome] = []
        self.generation = 0
        self.best_ever: Optional[Chromosome] = None
        self.history: List[dict] = []
    
    def initialize_population(self):
        """Create initial random population."""
        self.population = []
        for _ in range(self.population_size):
            genes = [self.gene_generator() for _ in range(self.chromosome_length)]
            chromosome = Chromosome(genes)
            chromosome.fitness = self.fitness_func(chromosome)
            self.population.append(chromosome)
        
        self._update_best()
        self.generation = 0
    
    def _select(self, population: List[Chromosome]) -> Chromosome:
        """Select a chromosome using configured method."""
        if self.selection_method == 'roulette':
            return Selection.roulette_wheel(population)
        elif self.selection_method == 'tournament':
            return Selection.tournament(population, self.tournament_size)
        elif self.selection_method == 'rank':
            return Selection.rank(population)
        elif self.selection_method == 'stochastic_universal':
            return Selection.stochastic_universal(population)
        else:
            return Selection.tournament(population, self.tournament_size)
    
    def _crossover(self, parent1: Chromosome, parent2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        """Apply crossover using configured method."""
        if self.crossover_method == 'single_point':
            return Crossover.single_point(parent1, parent2, self.crossover_rate)
        elif self.crossover_method == 'two_point':
            return Crossover.two_point(parent1, parent2, self.crossover_rate)
        elif self.crossover_method == 'uniform':
            return Crossover.uniform(parent1, parent2, self.crossover_rate)
        elif self.crossover_method == 'arithmetic':
            return Crossover.arithmetic(parent1, parent2, self.crossover_rate)
        elif self.crossover_method == 'order':
            return Crossover.order_crossover(parent1, parent2, self.crossover_rate)
        else:
            return Crossover.single_point(parent1, parent2, self.crossover_rate)
    
    def _mutate(self, chromosome: Chromosome) -> Chromosome:
        """Apply mutation using configured method."""
        if self.mutation_method == 'bit_flip':
            return Mutation.bit_flip(chromosome, self.mutation_rate)
        elif self.mutation_method == 'random_reset':
            return Mutation.random_reset(chromosome, self.mutation_rate, self.gene_range)
        elif self.mutation_method == 'gaussian':
            return Mutation.gaussian(chromosome, self.mutation_rate)
        elif self.mutation_method == 'swap':
            return Mutation.swap(chromosome, self.mutation_rate)
        elif self.mutation_method == 'insert':
            return Mutation.insert(chromosome, self.mutation_rate)
        elif self.mutation_method == 'inversion':
            return Mutation.inversion(chromosome, self.mutation_rate)
        elif self.mutation_method == 'scramble':
            return Mutation.scramble(chromosome, self.mutation_rate)
        else:
            return Mutation.gaussian(chromosome, self.mutation_rate)
    
    def _update_best(self):
        """Update the best-ever individual."""
        if not self.population:
            return
        
        if self.maximize:
            current_best = max(self.population, key=lambda x: x.fitness)
            if self.best_ever is None or current_best.fitness > self.best_ever.fitness:
                self.best_ever = current_best.copy()
        else:
            current_best = min(self.population, key=lambda x: x.fitness)
            if self.best_ever is None or current_best.fitness < self.best_ever.fitness:
                self.best_ever = current_best.copy()
    
    def evolve(self, generations: int = 1) -> 'GeneticAlgorithm':
        """Run evolution for specified generations."""
        if not self.population:
            self.initialize_population()
        
        for gen in range(generations):
            # Evaluate fitness
            for ind in self.population:
                ind.fitness = self.fitness_func(ind)
                ind.age += 1
            
            # Sort by fitness
            self.population.sort(key=lambda x: x.fitness, reverse=self.maximize)
            
            # Record history
            best = self.population[0].fitness
            worst = self.population[-1].fitness
            avg = sum(ind.fitness for ind in self.population) / len(self.population)
            self.history.append({
                'generation': self.generation,
                'best': best,
                'worst': worst,
                'average': avg
            })
            
            # Elitism
            new_population = Selection.elitism(self.population, self.elite_count)
            
            # Generate offspring
            while len(new_population) < self.population_size:
                parent1 = self._select(self.population)
                parent2 = self._select(self.population)
                
                child1, child2 = self._crossover(parent1, parent2)
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)
                
                new_population.extend([child1, child2])
            
            self.population = new_population[:self.population_size]
            self._update_best()
            self.generation += 1
        
        return self
    
    def run(self, generations: int = 100, 
            early_stop: Optional[int] = None,
            callback: Optional[Callable[[int, 'GeneticAlgorithm'], bool]] = None) -> Chromosome:
        """
        Run the genetic algorithm.
        
        Args:
            generations: Maximum number of generations
            early_stop: Stop if no improvement for N generations (None to disable)
            callback: Optional callback(gen, ga) -> bool, return True to stop
        
        Returns:
            Best chromosome found
        """
        if not self.population:
            self.initialize_population()
        
        last_best = None
        stagnant_generations = 0
        
        for i in range(generations):
            self.evolve(1)
            
            # Check for early stopping
            if early_stop:
                if last_best is None or self.best_ever.fitness != last_best:
                    last_best = self.best_ever.fitness
                    stagnant_generations = 0
                else:
                    stagnant_generations += 1
                    if stagnant_generations >= early_stop:
                        break
            
            # Check callback
            if callback and callback(self.generation, self):
                break
        
        return self.best_ever
    
    def get_statistics(self) -> dict:
        """Get current population statistics."""
        if not self.population:
            return {}
        
        fitnesses = [ind.fitness for ind in self.population]
        return {
            'generation': self.generation,
            'population_size': len(self.population),
            'best': max(fitnesses) if self.maximize else min(fitnesses),
            'worst': min(fitnesses) if self.maximize else max(fitnesses),
            'average': sum(fitnesses) / len(fitnesses),
            'std_dev': math.sqrt(sum((f - sum(fitnesses)/len(fitnesses))**2 for f in fitnesses) / len(fitnesses)),
            'best_ever': self.best_ever.fitness if self.best_ever else None
        }


# Convenience functions for common problems

def optimize_function(
    func: Callable[[List[float]], float],
    dimensions: int,
    bounds: Tuple[float, float],
    population_size: int = 50,
    generations: int = 100,
    maximize: bool = False
) -> Tuple[List[float], float]:
    """
    Optimize a real-valued function using genetic algorithm.
    
    Args:
        func: Function to optimize, takes list of floats, returns fitness
        dimensions: Number of dimensions/variables
        bounds: (min, max) bounds for each variable
        population_size: Population size
        generations: Number of generations
        maximize: True to maximize, False to minimize
    
    Returns:
        Tuple of (best_solution, best_fitness)
    """
    def fitness(chromosome):
        return func(chromosome.genes)
    
    def gene_gen():
        return random.uniform(bounds[0], bounds[1])
    
    ga = GeneticAlgorithm(
        fitness_func=fitness,
        gene_generator=gene_gen,
        chromosome_length=dimensions,
        population_size=population_size,
        maximize=maximize,
        mutation_method='gaussian',
        gene_range=bounds
    )
    
    best = ga.run(generations, early_stop=20)
    return best.genes, best.fitness


def solve_tsp(
    distances: List[List[float]],
    population_size: int = 100,
    generations: int = 500
) -> Tuple[List[int], float]:
    """
    Solve Traveling Salesman Problem using genetic algorithm.
    
    Args:
        distances: Distance matrix, distances[i][j] is distance from city i to j
        population_size: Population size
        generations: Maximum generations
    
    Returns:
        Tuple of (best_route, best_distance)
    """
    n_cities = len(distances)
    
    def fitness(chromosome):
        route = chromosome.genes
        total = 0
        for i in range(len(route)):
            total += distances[route[i]][route[(i + 1) % len(route)]]
        return -total  # Negative because we maximize fitness
    
    def gene_gen():
        return random.randint(0, n_cities - 1)
    
    def create_valid_chromosome():
        genes = list(range(n_cities))
        random.shuffle(genes)
        return Chromosome(genes)
    
    ga = GeneticAlgorithm(
        fitness_func=fitness,
        gene_generator=gene_gen,
        chromosome_length=n_cities,
        population_size=population_size,
        maximize=True,
        crossover_method='order',
        mutation_method='swap'
    )
    
    # Initialize with valid permutations
    ga.population = [create_valid_chromosome() for _ in range(population_size)]
    for ind in ga.population:
        ind.fitness = fitness(ind)
    
    best = ga.run(generations, early_stop=50)
    return best.genes, -best.fitness


def solve_knapsack(
    weights: List[float],
    values: List[float],
    capacity: float,
    population_size: int = 100,
    generations: int = 200
) -> Tuple[List[bool], float]:
    """
    Solve 0/1 Knapsack Problem using genetic algorithm.
    
    Args:
        weights: Weight of each item
        values: Value of each item
        capacity: Maximum capacity
        population_size: Population size
        generations: Maximum generations
    
    Returns:
        Tuple of (selected_items, total_value)
    """
    n_items = len(weights)
    
    def fitness(chromosome):
        total_weight = sum(w for w, s in zip(weights, chromosome.genes) if s)
        total_value = sum(v for v, s in zip(values, chromosome.genes) if s)
        
        if total_weight > capacity:
            return 0  # Infeasible solution
        return total_value
    
    def gene_gen():
        return random.random() < 0.5
    
    ga = GeneticAlgorithm(
        fitness_func=fitness,
        gene_generator=gene_gen,
        chromosome_length=n_items,
        population_size=population_size,
        maximize=True,
        mutation_method='bit_flip'
    )
    
    best = ga.run(generations, early_stop=30)
    total_weight = sum(w for w, s in zip(weights, best.genes) if s)
    total_value = sum(v for v, s in zip(values, best.genes) if s)
    
    return [bool(g) for g in best.genes], total_value


def solve_n_queens(
    n: int,
    population_size: int = 100,
    generations: int = 500
) -> Optional[List[int]]:
    """
    Solve N-Queens problem using genetic algorithm.
    
    Args:
        n: Board size (n x n)
        population_size: Population size
        generations: Maximum generations
    
    Returns:
        List of column positions for each row, or None if no solution found
    """
    def fitness(chromosome):
        conflicts = 0
        for i in range(len(chromosome.genes)):
            for j in range(i + 1, len(chromosome.genes)):
                if chromosome.genes[i] == chromosome.genes[j]:
                    conflicts += 1  # Same column
                if abs(chromosome.genes[i] - chromosome.genes[j]) == j - i:
                    conflicts += 1  # Same diagonal
        return -conflicts
    
    def create_valid_chromosome():
        genes = list(range(n))
        random.shuffle(genes)
        return Chromosome(genes)
    
    ga = GeneticAlgorithm(
        fitness_func=fitness,
        gene_generator=lambda: random.randint(0, n - 1),
        chromosome_length=n,
        population_size=population_size,
        maximize=True,
        crossover_method='order',
        mutation_method='swap'
    )
    
    # Initialize with valid permutations for order crossover
    ga.population = [create_valid_chromosome() for _ in range(population_size)]
    for ind in ga.population:
        ind.fitness = fitness(ind)
    ga._update_best()
    
    best = ga.run(generations, early_stop=100)
    
    if best.fitness == 0:
        return best.genes
    return None


def solve_scheduling(
    tasks: List[dict],
    workers: int,
    population_size: int = 100,
    generations: int = 200
) -> Tuple[List[int], float]:
    """
    Solve a simple task scheduling problem.
    
    Args:
        tasks: List of dicts with 'duration' and 'priority' keys
        workers: Number of available workers
        population_size: Population size
        generations: Maximum generations
    
    Returns:
        Tuple of (worker_assignments, total_weighted_completion)
    """
    n_tasks = len(tasks)
    
    def fitness(chromosome):
        worker_times = [0.0] * workers
        weighted_completion = 0.0
        
        # Sort tasks by assignment order (genes represent worker assignment)
        for task_idx, worker in enumerate(chromosome.genes):
            worker = int(worker) % workers
            duration = tasks[task_idx]['duration']
            priority = tasks[task_idx].get('priority', 1)
            
            completion_time = worker_times[worker] + duration
            worker_times[worker] = completion_time
            weighted_completion += completion_time * priority
        
        return -weighted_completion  # Minimize weighted completion time
    
    def gene_gen():
        return random.randint(0, workers - 1)
    
    ga = GeneticAlgorithm(
        fitness_func=fitness,
        gene_generator=gene_gen,
        chromosome_length=n_tasks,
        population_size=population_size,
        maximize=True,
        mutation_method='random_reset',
        gene_range=(0, workers - 1)
    )
    
    best = ga.run(generations, early_stop=30)
    return [int(g) % workers for g in best.genes], -best.fitness


# Population initialization utilities

def create_binary_chromosome(length: int) -> Chromosome:
    """Create a random binary chromosome."""
    return Chromosome([random.choice([0, 1]) for _ in range(length)])


def create_real_chromosome(length: int, low: float = 0.0, high: float = 1.0) -> Chromosome:
    """Create a random real-valued chromosome."""
    return Chromosome([random.uniform(low, high) for _ in range(length)])


def create_permutation_chromosome(length: int) -> Chromosome:
    """Create a random permutation chromosome."""
    genes = list(range(length))
    random.shuffle(genes)
    return Chromosome(genes)


def create_integer_chromosome(length: int, low: int, high: int) -> Chromosome:
    """Create a random integer chromosome."""
    return Chromosome([random.randint(low, high) for _ in range(length)])