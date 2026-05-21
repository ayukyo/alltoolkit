# Genetic Algorithm Utilities

A comprehensive, zero-dependency implementation of genetic algorithms for optimization problems.

## Features

- **Core Components**
  - `Chromosome` - Gene container with fitness tracking
  - `GeneticAlgorithm` - Main GA implementation with configurable parameters

- **Selection Methods**
  - Roulette Wheel (Fitness Proportionate)
  - Tournament Selection
  - Rank Selection
  - Stochastic Universal Sampling
  - Elitism

- **Crossover Methods**
  - Single-Point Crossover
  - Two-Point Crossover
  - Uniform Crossover
  - Arithmetic Crossover (for real values)
  - Order Crossover (for permutations)

- **Mutation Methods**
  - Bit Flip (for binary)
  - Random Reset
  - Gaussian (for real values)
  - Swap (for permutations)
  - Insert
  - Inversion
  - Scramble

- **Built-in Solvers**
  - Function Optimization
  - Traveling Salesman Problem (TSP)
  - 0/1 Knapsack Problem
  - N-Queens Problem
  - Task Scheduling

## Installation

No external dependencies required. Simply copy the `mod.py` file.

## Quick Start

### Basic Usage

```python
from mod import GeneticAlgorithm, Chromosome
import random

# Define fitness function
def fitness(chromosome):
    return sum(chromosome.genes)

# Create and run GA
ga = GeneticAlgorithm(
    fitness_func=fitness,
    gene_generator=lambda: random.uniform(0, 1),
    chromosome_length=10,
    population_size=50,
    maximize=True
)

best = ga.run(generations=100)
print(f"Best solution: {best.genes}")
print(f"Best fitness: {best.fitness}")
```

### Function Optimization

```python
from mod import optimize_function

# Minimize sphere function
def sphere(x):
    return sum(xi ** 2 for xi in x)

solution, fitness = optimize_function(
    func=sphere,
    dimensions=5,
    bounds=(-10.0, 10.0),
    maximize=False
)
print(f"Solution: {solution}")
print(f"Fitness: {fitness}")
```

### TSP Solver

```python
from mod import solve_tsp

# Distance matrix
distances = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

route, total_distance = solve_tsp(distances)
print(f"Route: {route}")
print(f"Total distance: {total_distance}")
```

### Knapsack Problem

```python
from mod import solve_knapsack

weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 5

selected, total_value = solve_knapsack(weights, values, capacity)
print(f"Selected items: {selected}")
print(f"Total value: {total_value}")
```

### N-Queens Problem

```python
from mod import solve_n_queens

solution = solve_n_queens(8)
if solution:
    print(f"Solution found: {solution}")
    # Each index represents a row, value is column position
```

## Advanced Configuration

```python
ga = GeneticAlgorithm(
    fitness_func=my_fitness,
    gene_generator=lambda: random.randint(0, 100),
    chromosome_length=20,
    population_size=100,
    elite_count=2,              # Number of elites to preserve
    selection_method='tournament',
    crossover_method='two_point',
    mutation_method='swap',
    crossover_rate=0.8,
    mutation_rate=0.1,
    tournament_size=3,
    maximize=True,
    gene_range=(0, 100)
)

# Run with early stopping
best = ga.run(
    generations=500,
    early_stop=50,  # Stop if no improvement for 50 generations
    callback=lambda gen, ga: print(f"Gen {gen}: {ga.best_ever.fitness}")
)

# Get statistics
stats = ga.get_statistics()
print(f"Best: {stats['best']}")
print(f"Average: {stats['average']}")
print(f"Std Dev: {stats['std_dev']}")
```

## Custom Selection/Crossover/Mutation

```python
from mod import Chromosome, Selection, Crossover, Mutation

# Create chromosome
chrom = Chromosome([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Apply mutation
mutated = Mutation.swap(chrom, mutation_rate=1.0)

# Apply crossover
parent1 = Chromosome([1, 2, 3, 4, 5])
parent2 = Chromosome([5, 4, 3, 2, 1])
child1, child2 = Crossover.uniform(parent1, parent2)
```

## API Reference

### Chromosome

```python
Chromosome(genes: List[Any], fitness: float = 0.0)
```

### Selection Methods

- `Selection.roulette_wheel(population)` - Fitness proportionate selection
- `Selection.tournament(population, tournament_size=3)` - Tournament selection
- `Selection.rank(population)` - Rank-based selection
- `Selection.stochastic_universal(population)` - SUS
- `Selection.elitism(population, elite_count=1)` - Select top individuals

### Crossover Methods

- `Crossover.single_point(p1, p2, rate=0.8)` - Single-point crossover
- `Crossover.two_point(p1, p2, rate=0.8)` - Two-point crossover
- `Crossover.uniform(p1, p2, rate=0.8, swap_prob=0.5)` - Uniform crossover
- `Crossover.arithmetic(p1, p2, rate=0.8, alpha=None)` - Arithmetic crossover
- `Crossover.order_crossover(p1, p2, rate=0.8)` - Order crossover (permutations)

### Mutation Methods

- `Mutation.bit_flip(chrom, rate=0.01)` - Flip bits
- `Mutation.random_reset(chrom, rate=0.01, range=None)` - Random replacement
- `Mutation.gaussian(chrom, rate=0.01, sigma=0.1)` - Gaussian perturbation
- `Mutation.swap(chrom, rate=0.01)` - Swap two genes
- `Mutation.insert(chrom, rate=0.01)` - Move gene to new position
- `Mutation.inversion(chrom, rate=0.01)` - Reverse segment
- `Mutation.scramble(chrom, rate=0.01)` - Shuffle segment

## License

MIT License