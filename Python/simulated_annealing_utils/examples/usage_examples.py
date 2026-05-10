#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Simulated Annealing Usage Examples
=================================================
Practical examples demonstrating simulated annealing optimization.

Author: AllToolkit Contributors
License: MIT
"""

import sys
sys.path.insert(0, '..')

from mod import (
    SimulatedAnnealing,
    SAConfig,
    TemperatureSchedule,
    solve_tsp,
    optimize_function,
    optimize_nd_function,
    solve_job_scheduling,
    solve_bin_packing,
    solve_graph_coloring,
    calculate_temperature_schedule,
    estimate_initial_temperature
)


def example_1_basic_quadratic_optimization():
    """
    Example 1: Basic Quadratic Function Optimization
    
    Find the minimum of f(x) = x^2 - 4x + 4 (which is 0 at x = 2).
    """
    print("=" * 60)
    print("Example 1: Basic Quadratic Function Optimization")
    print("=" * 60)
    
    def quadratic(x):
        """Quadratic function: f(x) = (x - 2)^2"""
        return (x - 2) ** 2
    
    # Custom neighbor function for continuous optimization
    def neighbor(x):
        """Generate neighboring solution by adding small random step."""
        import random
        step_size = 1.0  # Adjust based on your problem
        return x + random.uniform(-step_size, step_size)
    
    # Configure simulated annealing
    config = SAConfig(
        initial_temperature=100.0,
        final_temperature=0.001,
        cooling_rate=0.95,
        iterations_per_temp=100,
        max_iterations=5000,
        seed=42,
        verbose=False
    )
    
    # Create optimizer
    sa = SimulatedAnnealing(quadratic, neighbor, config)
    
    # Run optimization starting from x = 10
    result = sa.optimize(initial_solution=10.0)
    
    print(f"\nStarting point: x = 10.0")
    print(f"Best solution found: x = {result.best_solution:.4f}")
    print(f"Best cost: f(x) = {result.best_cost:.4f}")
    print(f"Expected minimum: x = 2.0, f(x) = 0.0")
    print(f"\nStatistics:")
    print(f"  - Total iterations: {result.stats.iterations}")
    print(f"  - Accepted moves: {result.stats.accepted_moves}")
    print(f"  - Rejected moves: {result.stats.rejected_moves}")
    print(f"  - Acceptance rate: {result.stats.acceptance_rate:.2%}")
    print(f"  - Final temperature: {result.stats.final_temperature:.4f}")
    print()


def example_2_tsp_traveling_salesman():
    """
    Example 2: Traveling Salesman Problem (TSP)
    
    Find the shortest tour visiting all cities exactly once.
    """
    print("=" * 60)
    print("Example 2: Traveling Salesman Problem")
    print("=" * 60)
    
    # Distance matrix for 5 cities
    # distances[i][j] = distance from city i to city j
    distances = [
        [0,  10, 15, 20, 25],
        [10, 0,  35, 25, 30],
        [15, 35, 0,  30, 10],
        [20, 25, 30, 0,  15],
        [25, 30, 10, 15, 0]
    ]
    
    print("\nDistance Matrix:")
    print("     0    1    2    3    4")
    for i, row in enumerate(distances):
        print(f"{i}: {row}")
    
    # Configure solver
    config = SAConfig(
        initial_temperature=1000.0,
        final_temperature=0.001,
        cooling_rate=0.98,
        iterations_per_temp=200,
        max_iterations=10000,
        seed=42
    )
    
    # Solve TSP
    result = solve_tsp(distances, config)
    
    print(f"\nBest tour found: {result.best_solution}")
    print(f"Total tour length: {result.best_cost:.2f}")
    print(f"Iterations: {result.stats.iterations}")
    
    # Show tour order
    tour = result.best_solution
    print("\nTour order:")
    for i in range(len(tour)):
        current = tour[i]
        next_city = tour[(i + 1) % len(tour)]
        dist = distances[current][next_city]
        print(f"  City {current} -> City {next_city} (distance: {dist})")
    print(f"  Total: {result.best_cost:.2f}")
    print()


def example_3_job_scheduling():
    """
    Example 3: Job Scheduling Problem
    
    Schedule jobs across machines to minimize makespan.
    """
    print("=" * 60)
    print("Example 3: Job Scheduling Problem")
    print("=" * 60)
    
    # Define jobs with processing times
    jobs = [
        {'id': 'Job A', 'duration': 8},
        {'id': 'Job B', 'duration': 5},
        {'id': 'Job C', 'duration': 3},
        {'id': 'Job D', 'duration': 7},
        {'id': 'Job E', 'duration': 4},
    ]
    
    machines = 3
    
    print(f"\nJobs:")
    for job in jobs:
        print(f"  {job['id']}: duration = {job['duration']}")
    print(f"\nNumber of machines: {machines}")
    
    # Configure solver
    config = SAConfig(
        initial_temperature=100.0,
        max_iterations=5000,
        seed=42
    )
    
    # Solve scheduling
    result = solve_job_scheduling(jobs, machines, config)
    
    print(f"\nBest schedule found:")
    assignment = result.best_solution
    for i, machine in enumerate(assignment):
        print(f"  {jobs[i]['id']} -> Machine {machine}")
    
    print(f"\nMakespan: {result.best_cost:.2f}")
    
    # Calculate load on each machine
    machine_loads = [0.0] * machines
    for i, machine in enumerate(assignment):
        machine_loads[machine] += jobs[i]['duration']
    
    print("\nMachine loads:")
    for m in range(machines):
        print(f"  Machine {m}: {machine_loads[m]}")
    print()


def example_4_bin_packing():
    """
    Example 4: Bin Packing Problem
    
    Pack items into minimum number of bins.
    """
    print("=" * 60)
    print("Example 4: Bin Packing Problem")
    print("=" * 60)
    
    # Items to pack
    items = [7, 3, 5, 4, 2, 8, 1, 6, 4, 3]
    bin_capacity = 10
    
    print(f"\nItems: {items}")
    print(f"Bin capacity: {bin_capacity}")
    print(f"Total item weight: {sum(items)}")
    
    # Configure solver
    config = SAConfig(
        initial_temperature=100.0,
        max_iterations=8000,
        seed=42
    )
    
    # Solve bin packing
    result = solve_bin_packing(items, bin_capacity, config)
    
    print(f"\nBins needed: {result.best_cost:.0f}")
    
    # Show bin contents
    assignment = result.best_solution
    bins = {}
    for i, bin_idx in enumerate(assignment):
        if bin_idx not in bins:
            bins[bin_idx] = []
        bins[bin_idx].append(items[i])
    
    print("\nBin contents:")
    for bin_idx in sorted(bins.keys()):
        items_in_bin = bins[bin_idx]
        total = sum(items_in_bin)
        print(f"  Bin {bin_idx}: items {items_in_bin} (total: {total}/{bin_capacity})")
    print()


def example_5_graph_coloring():
    """
    Example 5: Graph Coloring Problem
    
    Color graph vertices so adjacent vertices have different colors.
    """
    print("=" * 60)
    print("Example 5: Graph Coloring Problem")
    print("=" * 60)
    
    # Define graph edges
    # A graph with 6 vertices
    edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 2), (1, 4),
        (2, 3), (2, 5),
        (3, 5),
        (4, 5)
    ]
    num_nodes = 6
    
    print(f"\nGraph with {num_nodes} vertices")
    print(f"Edges: {edges}")
    
    # Configure solver
    config = SAConfig(
        initial_temperature=50.0,
        max_iterations=5000,
        seed=42
    )
    
    # Solve graph coloring
    result = solve_graph_coloring(edges, num_nodes, max_colors=4, config=config)
    
    print(f"\nColors used: {result.best_cost:.0f}")
    print(f"Color assignment:")
    colors = result.best_solution
    for i, color in enumerate(colors):
        print(f"  Vertex {i}: Color {color}")
    
    # Verify solution
    print("\nVerification (no adjacent vertices should share color):")
    valid = True
    for u, v in edges:
        if colors[u] == colors[v]:
            print(f"  CONFLICT: Vertices {u} and {v} both have color {colors[u]}")
            valid = False
        else:
            print(f"  OK: Vertices {u} (color {colors[u]}) and {v} (color {colors[v]})")
    
    print(f"\nSolution valid: {valid}")
    print()


def example_6_nd_optimization():
    """
    Example 6: N-Dimensional Function Optimization
    
    Optimize multi-dimensional functions like Rosenbrock.
    """
    print("=" * 60)
    print("Example 6: N-Dimensional Function Optimization")
    print("=" * 60)
    
    # Rosenbrock function: f(x, y) = (1-x)^2 + 100*(y-x^2)^2
    # Minimum is at (1, 1) with f(1,1) = 0
    def rosenbrock(x):
        return (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2
    
    print("\nRosenbrock function:")
    print("  f(x, y) = (1-x)^2 + 100*(y-x^2)^2")
    print("  Known minimum: f(1, 1) = 0")
    
    # Search bounds
    bounds = [(-3, 3), (-3, 3)]
    
    # Configure solver
    config = SAConfig(
        initial_temperature=1000.0,
        max_iterations=15000,
        seed=42
    )
    
    # Solve
    result = optimize_nd_function(rosenbrock, bounds, minimize=True, config=config)
    
    print(f"\nBest solution: ({result.best_solution[0]:.4f}, {result.best_solution[1]:.4f})")
    print(f"Best cost: {result.best_cost:.4f}")
    print(f"Iterations: {result.stats.iterations}")
    print()


def example_7_different_schedules():
    """
    Example 7: Comparing Different Cooling Schedules
    
    Compare effectiveness of different temperature schedules.
    """
    print("=" * 60)
    print("Example 7: Comparing Cooling Schedules")
    print("=" * 60)
    
    def rastrigin(x):
        """Rastrigin function - highly multimodal."""
        import math
        return 10 * len(x) + sum(xi ** 2 - 10 * math.cos(2 * math.pi * xi) for xi in x)
    
    print("\nRastrigin function (multimodal optimization)")
    print("  f(x) = 10*n + Σ(x_i^2 - 10*cos(2πx_i))")
    print("  Minimum: f(0, 0, ..., 0) = 0")
    
    bounds = [(-5, 5), (-5, 5)]
    
    schedules = [
        TemperatureSchedule.LINEAR,
        TemperatureSchedule.EXPONENTIAL,
        TemperatureSchedule.LOGARITHMIC,
        TemperatureSchedule.ADAPTIVE
    ]
    
    print("\nResults for different schedules:")
    for schedule in schedules:
        config = SAConfig(
            initial_temperature=500.0,
            max_iterations=5000,
            schedule=schedule,
            seed=42
        )
        
        result = optimize_nd_function(rastrigin, bounds, minimize=True, config=config)
        
        print(f"\n{schedule.value.upper}:")
        print(f"  Best solution: ({result.best_solution[0]:.4f}, {result.best_solution[1]:.4f})")
        print(f"  Best cost: {result.best_cost:.4f}")
        print(f"  Acceptance rate: {result.stats.acceptance_rate:.2%}")
    print()


def example_8_custom_problem():
    """
    Example 8: Custom Optimization Problem
    
    Use simulated annealing for a custom problem.
    """
    print("=" * 60)
    print("Example 8: Custom Optimization Problem")
    print("=" * 60)
    
    # Custom problem: find string closest to target
    target = "hello world"
    alphabet = "abcdefghijklmnopqrstuvwxyz "
    
    def string_cost(s):
        """Cost = number of differing characters."""
        cost = 0
        for i, c in enumerate(target):
            if i < len(s):
                cost += (c != s[i])
            else:
                cost += 1  # Missing character
        cost += max(0, len(s) - len(target))  # Extra characters
        return cost
    
    def string_neighbor(s):
        """Generate neighbor by changing one character."""
        import random
        if len(s) == 0:
            return alphabet[0]
        
        new_s = list(s)
        i = random.randint(0, len(new_s) - 1)
        new_s[i] = random.choice(alphabet)
        
        # Occasionally add or remove character
        if random.random() < 0.1:
            if len(new_s) < len(target) + 2:
                new_s.append(random.choice(alphabet))
        elif random.random() < 0.1:
            if len(new_s) > 1:
                new_s.pop(random.randint(0, len(new_s) - 1))
        
        return ''.join(new_s)
    
    # Initial random string
    import random
    initial = ''.join(random.choice(alphabet) for _ in range(len(target)))
    
    print(f"\nTarget string: '{target}'")
    print(f"Initial string: '{initial}'")
    
    # Configure
    config = SAConfig(
        initial_temperature=50.0,
        final_temperature=0.001,
        max_iterations=8000,
        seed=42
    )
    
    # Optimize
    sa = SimulatedAnnealing(string_cost, string_neighbor, config)
    result = sa.optimize(initial_solution=initial)
    
    print(f"\nBest string found: '{result.best_solution}'")
    print(f"Cost (differences): {result.best_cost:.0f}")
    print(f"Match: {result.best_solution == target}")
    print()


def example_9_temperature_estimation():
    """
    Example 9: Estimating Good Initial Temperature
    
    Automatically estimate a good initial temperature.
    """
    print("=" * 60)
    print("Example 9: Temperature Estimation")
    print("=" * 60)
    
    def cost(x):
        return (x - 50) ** 2
    
    def neighbor(x):
        import random
        return x + random.uniform(-10, 10)
    
    print("\nFunction: f(x) = (x - 50)^2")
    print("Estimating initial temperature for 80% acceptance rate...")
    
    estimated_temp = estimate_initial_temperature(
        cost, neighbor,
        initial_solution=0.0,
        target_acceptance_rate=0.8,
        num_samples=500
    )
    
    print(f"\nEstimated initial temperature: {estimated_temp:.2f}")
    
    # Use estimated temperature
    config = SAConfig(
        initial_temperature=estimated_temp,
        max_iterations=3000,
        seed=42
    )
    
    sa = SimulatedAnnealing(cost, neighbor, config)
    result = sa.optimize(initial_solution=0.0)
    
    print(f"\nOptimization result:")
    print(f"  Best solution: {result.best_solution:.4f}")
    print(f"  Best cost: {result.best_cost:.4f}")
    print(f"  Acceptance rate: {result.stats.acceptance_rate:.2%}")
    print()


def example_10_callback_progress():
    """
    Example 10: Using Callbacks for Progress Tracking
    
    Monitor optimization progress with callbacks.
    """
    print("=" * 60)
    print("Example 10: Progress Tracking with Callbacks")
    print("=" * 60)
    
    def cost(x):
        return x ** 2
    
    def neighbor(x):
        import random
        return x + random.uniform(-1, 1)
    
    progress = []
    
    def callback(iteration, temp, solution):
        progress.append((iteration, temp, cost(solution)))
    
    config = SAConfig(
        initial_temperature=100.0,
        final_temperature=1.0,
        iterations_per_temp=50,
        max_iterations=2000,
        seed=42
    )
    
    sa = SimulatedAnnealing(cost, neighbor, config)
    result = sa.optimize(initial_solution=10.0, callback=callback)
    
    print("\nOptimization progress (sample):")
    print("Iteration | Temperature | Cost")
    print("-" * 30)
    for i in range(0, len(progress), 10):
        iteration, temp, cost_val = progress[i]
        print(f"{iteration:8d} | {temp:11.4f} | {cost_val:.6f}")
    
    print(f"\nFinal result:")
    print(f"  Best solution: {result.best_solution:.4f}")
    print(f"  Best cost: {result.best_cost:.4f}")
    print()


def main():
    """Run all examples."""
    examples = [
        example_1_basic_quadratic_optimization,
        example_2_tsp_traveling_salesman,
        example_3_job_scheduling,
        example_4_bin_packing,
        example_5_graph_coloring,
        example_6_nd_optimization,
        example_7_different_schedules,
        example_8_custom_problem,
        example_9_temperature_estimation,
        example_10_callback_progress,
    ]
    
    print("\n" + "=" * 60)
    print("Simulated Annealing Examples")
    print("=" * 60)
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\nError in {example.__name__}: {e}")
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()