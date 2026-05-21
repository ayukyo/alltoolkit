"""
Genetic Algorithm Examples

This file demonstrates various use cases of the genetic algorithm utilities.
"""

import sys
sys.path.insert(0, '..')

import math
import random
from mod import (
    GeneticAlgorithm, Chromosome, Selection, Crossover, Mutation,
    optimize_function, solve_tsp, solve_knapsack, solve_n_queens,
    solve_scheduling, create_binary_chromosome, create_real_chromosome,
    create_permutation_chromosome
)


def example_basic_optimization():
    """Basic optimization: maximize sum of genes."""
    print("=" * 60)
    print("Example 1: Basic Optimization")
    print("=" * 60)
    
    def fitness(chromosome):
        return sum(chromosome.genes)
    
    ga = GeneticAlgorithm(
        fitness_func=fitness,
        gene_generator=lambda: random.uniform(0, 10),
        chromosome_length=5,
        population_size=50,
        maximize=True,
        mutation_method='gaussian'
    )
    
    best = ga.run(generations=50)
    print(f"Best genes: {[f'{g:.2f}' for g in best.genes]}")
    print(f"Best fitness: {best.fitness:.2f}")
    print()


def example_function_minimization():
    """Minimize the Rastrigin function (multi-modal optimization)."""
    print("=" * 60)
    print("Example 2: Rastrigin Function Minimization")
    print("=" * 60)
    
    def rastrigin(x):
        """Rastrigin function - highly multi-modal."""
        A = 10
        n = len(x)
        return A * n + sum(xi**2 - A * math.cos(2 * math.pi * xi) for xi in x)
    
    solution, fitness = optimize_function(
        func=rastrigin,
        dimensions=3,
        bounds=(-5.12, 5.12),
        population_size=100,
        generations=200,
        maximize=False
    )
    
    print(f"Solution found: {[f'{x:.4f}' for x in solution]}")
    print(f"Fitness (lower is better): {fitness:.4f}")
    print(f"Global minimum is at origin with value 0")
    print()


def example_tsp():
    """Solve a Traveling Salesman Problem."""
    print("=" * 60)
    print("Example 3: Traveling Salesman Problem")
    print("=" * 60)
    
    # 6 cities with random coordinates
    cities = {
        0: (0, 0),
        1: (10, 0),
        2: (10, 10),
        3: (0, 10),
        4: (5, 5),
        5: (15, 5)
    }
    
    # Create distance matrix
    n = len(cities)
    distances = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                x1, y1 = cities[i]
                x2, y2 = cities[j]
                distances[i][j] = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    print("Cities:")
    for city, (x, y) in cities.items():
        print(f"  City {city}: ({x}, {y})")
    
    route, total_distance = solve_tsp(distances, population_size=100, generations=300)
    
    print(f"\nBest route: {' -> '.join(map(str, route + [route[0]]))}")
    print(f"Total distance: {total_distance:.2f}")
    print()


def example_knapsack():
    """Solve a 0/1 Knapsack Problem."""
    print("=" * 60)
    print("Example 4: 0/1 Knapsack Problem")
    print("=" * 60)
    
    items = [
        {"name": "Laptop", "weight": 3, "value": 2000},
        {"name": "Camera", "weight": 1, "value": 1500},
        {"name": "Headphones", "weight": 0.5, "value": 300},
        {"name": "Water Bottle", "weight": 0.8, "value": 50},
        {"name": "Snacks", "weight": 1, "value": 100},
        {"name": "Book", "weight": 1.5, "value": 80},
        {"name": "Phone Charger", "weight": 0.3, "value": 50},
        {"name": "Tablet", "weight": 0.7, "value": 800},
    ]
    
    weights = [item["weight"] for item in items]
    values = [item["value"] for item in items]
    capacity = 5.0
    
    print(f"Capacity: {capacity}")
    print("Items:")
    for item in items:
        print(f"  {item['name']}: weight={item['weight']}, value={item['value']}")
    
    selected, total_value = solve_knapsack(
        weights, values, capacity,
        population_size=100,
        generations=200
    )
    
    print(f"\nSelected items:")
    total_weight = 0
    for item, is_selected in zip(items, selected):
        if is_selected:
            print(f"  ✓ {item['name']} (weight={item['weight']}, value={item['value']})")
            total_weight += item['weight']
    
    print(f"\nTotal weight: {total_weight:.1f}/{capacity}")
    print(f"Total value: {total_value}")
    print()


def example_n_queens():
    """Solve the N-Queens problem."""
    print("=" * 60)
    print("Example 5: 8-Queens Problem")
    print("=" * 60)
    
    solution = solve_n_queens(8, population_size=100, generations=500)
    
    if solution:
        print("Solution found!")
        print("\nBoard:")
        for row in range(8):
            line = ""
            for col in range(8):
                if solution[row] == col:
                    line += "Q "
                else:
                    line += ". "
            print(f"  {line}")
        print(f"\nPositions (row: column): {list(enumerate(solution))}")
    else:
        print("No solution found within the generation limit.")
    print()


def example_scheduling():
    """Solve a simple task scheduling problem."""
    print("=" * 60)
    print("Example 6: Task Scheduling")
    print("=" * 60)
    
    tasks = [
        {"name": "Task A", "duration": 3, "priority": 2},
        {"name": "Task B", "duration": 2, "priority": 3},
        {"name": "Task C", "duration": 4, "priority": 1},
        {"name": "Task D", "duration": 1, "priority": 4},
        {"name": "Task E", "duration": 3, "priority": 2},
        {"name": "Task F", "duration": 2, "priority": 1},
    ]
    
    workers = 2
    
    print(f"Workers available: {workers}")
    print("Tasks:")
    for task in tasks:
        print(f"  {task['name']}: duration={task['duration']}, priority={task['priority']}")
    
    assignments, score = solve_scheduling(
        tasks, workers,
        population_size=50,
        generations=100
    )
    
    print(f"\nAssignments:")
    for w in range(workers):
        worker_tasks = [tasks[i]['name'] for i, a in enumerate(assignments) if a == w]
        worker_duration = sum(tasks[i]['duration'] for i, a in enumerate(assignments) if a == w)
        print(f"  Worker {w}: {', '.join(worker_tasks)} (total: {worker_duration})")
    
    print(f"\nWeighted completion score: {score:.2f} (lower is better)")
    print()


def example_binary_chromosome():
    """Binary chromosome for OneMax problem."""
    print("=" * 60)
    print("Example 7: OneMax Problem (Binary)")
    print("=" * 60)
    
    def onemax(chromosome):
        return sum(chromosome.genes)
    
    ga = GeneticAlgorithm(
        fitness_func=onemax,
        gene_generator=lambda: random.randint(0, 1),
        chromosome_length=20,
        population_size=50,
        maximize=True,
        mutation_method='bit_flip',
        mutation_rate=0.01
    )
    
    best = ga.run(generations=100)
    print(f"Best chromosome: {''.join(map(str, best.genes))}")
    print(f"Ones count: {best.fitness}/{len(best.genes)}")
    print()


def example_permutation():
    """Permutation-based GA for ordering problem."""
    print("=" * 60)
    print("Example 8: Permutation Ordering")
    print("=" * 60)
    
    # Find ordering where adjacent numbers have maximum sum of products
    def fitness(chromosome):
        total = 0
        for i in range(len(chromosome) - 1):
            total += chromosome[i] * chromosome[i + 1]
        return total
    
    ga = GeneticAlgorithm(
        fitness_func=fitness,
        gene_generator=lambda: random.randint(1, 10),
        chromosome_length=8,
        population_size=100,
        maximize=True,
        crossover_method='order',
        mutation_method='swap'
    )
    
    # Initialize with permutations
    ga.population = [create_permutation_chromosome(8) for _ in range(100)]
    for ind in ga.population:
        ind.fitness = fitness(ind)
    
    best = ga.run(generations=200, early_stop=30)
    print(f"Best ordering: {best.genes}")
    print(f"Fitness: {best.fitness}")
    print()


def example_custom_callback():
    """Using callbacks to monitor evolution."""
    print("=" * 60)
    print("Example 9: Custom Callback Monitoring")
    print("=" * 60)
    
    def sphere(x):
        return sum(xi ** 2 for xi in x)
    
    generations_log = []
    
    def callback(gen, ga):
        generations_log.append({
            'gen': gen,
            'best': ga.best_ever.fitness if ga.best_ever else 0
        })
        if gen % 20 == 0:
            stats = ga.get_statistics()
            print(f"  Gen {gen}: best={stats['best']:.4f}, avg={stats['average']:.4f}")
        return False  # Don't stop
    
    ga = GeneticAlgorithm(
        fitness_func=lambda c: -sphere(c.genes),  # Negative for maximization
        gene_generator=lambda: random.uniform(-5, 5),
        chromosome_length=3,
        population_size=50,
        maximize=True
    )
    
    print("Evolution progress:")
    best = ga.run(generations=100, callback=callback)
    
    print(f"\nFinal solution: {[f'{g:.4f}' for g in best.genes]}")
    print(f"Final fitness: {best.fitness:.6f}")
    print()


def example_statistics():
    """Detailed statistics tracking."""
    print("=" * 60)
    print("Example 10: Statistics and History")
    print("=" * 60)
    
    def quadratic(x):
        # Minimize (x - 3)^2 + (y - 5)^2 + (z - 2)^2
        return (x[0] - 3)**2 + (x[1] - 5)**2 + (x[2] - 2)**2
    
    ga = GeneticAlgorithm(
        fitness_func=lambda c: -quadratic(c.genes),
        gene_generator=lambda: random.uniform(0, 10),
        chromosome_length=3,
        population_size=60,
        maximize=True,
        mutation_method='gaussian'
    )
    
    ga.run(generations=50)
    
    stats = ga.get_statistics()
    print(f"Generation: {stats['generation']}")
    print(f"Population size: {stats['population_size']}")
    print(f"Best fitness: {stats['best']:.4f}")
    print(f"Worst fitness: {stats['worst']:.4f}")
    print(f"Average fitness: {stats['average']:.4f}")
    print(f"Std deviation: {stats['std_dev']:.4f}")
    print(f"Best ever: {stats['best_ever']:.4f}")
    
    # Show improvement over generations
    if len(ga.history) >= 3:
        print(f"\nProgress (every 10 generations):")
        for i, h in enumerate(ga.history[::10]):
            print(f"  Gen {h['generation']}: best={h['best']:.4f}, avg={h['average']:.4f}")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("   GENETIC ALGORITHM UTILITIES - EXAMPLES")
    print("=" * 60 + "\n")
    
    example_basic_optimization()
    example_function_minimization()
    example_tsp()
    example_knapsack()
    example_n_queens()
    example_scheduling()
    example_binary_chromosome()
    example_permutation()
    example_custom_callback()
    example_statistics()
    
    print("=" * 60)
    print("   All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()