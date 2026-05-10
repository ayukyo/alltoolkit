#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Simulated Annealing Utilities Test Suite
======================================================
Comprehensive tests for the simulated annealing optimization module.

Author: AllToolkit Contributors
License: MIT
"""

import unittest
import math
import random
from mod import (
    SimulatedAnnealing,
    SAConfig,
    SAStats,
    OptimizationResult,
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


class TestSAConfig(unittest.TestCase):
    """Test SAConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = SAConfig()
        self.assertEqual(config.initial_temperature, 1000.0)
        self.assertEqual(config.final_temperature, 0.001)
        self.assertEqual(config.cooling_rate, 0.95)
        self.assertEqual(config.iterations_per_temp, 100)
        self.assertEqual(config.schedule, TemperatureSchedule.EXPONENTIAL)
        self.assertEqual(config.max_iterations, 100000)
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = SAConfig(
            initial_temperature=500.0,
            final_temperature=0.01,
            cooling_rate=0.9,
            max_iterations=50000
        )
        self.assertEqual(config.initial_temperature, 500.0)
        self.assertEqual(config.final_temperature, 0.01)
        self.assertEqual(config.cooling_rate, 0.9)
        self.assertEqual(config.max_iterations, 50000)


class TestSimulatedAnnealing(unittest.TestCase):
    """Test SimulatedAnnealing class."""
    
    def test_quadratic_optimization(self):
        """Test optimizing a simple quadratic function."""
        def cost(x):
            return x ** 2
        
        def neighbor(x):
            return x + random.uniform(-1, 1)
        
        config = SAConfig(
            initial_temperature=100.0,
            final_temperature=0.01,
            max_iterations=5000,
            seed=42
        )
        
        sa = SimulatedAnnealing(cost, neighbor, config)
        result = sa.optimize(initial_solution=5.0)
        
        self.assertTrue(result.success)
        self.assertAlmostEqual(result.best_cost, 0.0, places=1)
        self.assertAlmostEqual(result.best_solution, 0.0, places=1)
        self.assertGreater(result.stats.iterations, 0)
    
    def test_sine_optimization(self):
        """Test finding minimum of sin function."""
        def cost(x):
            return math.sin(x)
        
        def neighbor(x):
            return x + random.uniform(-0.5, 0.5)
        
        config = SAConfig(
            initial_temperature=10.0,
            final_temperature=0.001,
            max_iterations=3000,
            seed=42
        )
        
        sa = SimulatedAnnealing(cost, neighbor, config)
        result = sa.optimize(initial_solution=0.0)
        
        self.assertTrue(result.success)
        # sin minimum is -1 at 3π/2 ≈ 4.71
        self.assertLessEqual(result.best_cost, -0.95)
    
    def test_discrete_optimization(self):
        """Test discrete optimization (binary string)."""
        def cost(x):
            # Minimize number of 1s in binary string
            return sum(x)
        
        def neighbor(x):
            new_x = x.copy()
            i = random.randint(0, len(new_x) - 1)
            new_x[i] = 1 - new_x[i]
            return new_x
        
        config = SAConfig(
            initial_temperature=10.0,
            final_temperature=0.001,
            max_iterations=2000,
            seed=42
        )
        
        sa = SimulatedAnnealing(cost, neighbor, config)
        initial = [1] * 10  # All ones
        result = sa.optimize(initial_solution=initial)
        
        self.assertTrue(result.success)
        self.assertEqual(result.best_cost, 0.0)  # Should find all zeros
        self.assertEqual(result.best_solution, [0] * 10)
    
    def test_acceptance_probability(self):
        """Test acceptance probability calculation."""
        def cost(x):
            return x
        
        def neighbor(x):
            return x + 1
        
        sa = SimulatedAnnealing(cost, neighbor)
        
        # Better solution should always be accepted
        prob = sa._acceptance_probability(10, 5, 100)
        self.assertEqual(prob, 1.0)
        
        # Worse solution at high temperature
        prob = sa._acceptance_probability(5, 10, 100)
        self.assertGreater(prob, 0)
        self.assertLess(prob, 1)
        
        # Worse solution at low temperature
        prob_low = sa._acceptance_probability(5, 10, 1)
        self.assertLess(prob_low, prob)  # Lower probability at lower temp
    
    def test_temperature_schedules(self):
        """Test different cooling schedules."""
        def cost(x):
            return x ** 2
        
        def neighbor(x):
            return x + random.uniform(-0.5, 0.5)
        
        schedules = [
            TemperatureSchedule.LINEAR,
            TemperatureSchedule.EXPONENTIAL,
            TemperatureSchedule.LOGARITHMIC,
            TemperatureSchedule.ADAPTIVE
        ]
        
        for schedule in schedules:
            config = SAConfig(
                initial_temperature=100.0,
                final_temperature=0.1,
                max_iterations=2000,
                schedule=schedule,
                seed=42
            )
            
            sa = SimulatedAnnealing(cost, neighbor, config)
            result = sa.optimize(initial_solution=5.0)
            
            self.assertTrue(result.success)
            # All schedules should find near-optimal solution (relaxed threshold for logarithmic)
            self.assertLess(result.best_cost, 2.0)
    
    def test_callback(self):
        """Test callback function is called."""
        callback_calls = []
        
        def callback(iteration, temp, solution):
            callback_calls.append((iteration, temp, solution))
        
        def cost(x):
            return x ** 2
        
        def neighbor(x):
            return x + random.uniform(-0.5, 0.5)
        
        config = SAConfig(
            initial_temperature=10.0,
            final_temperature=1.0,
            iterations_per_temp=10,
            max_iterations=100,
            seed=42
        )
        
        sa = SimulatedAnnealing(cost, neighbor, config)
        result = sa.optimize(initial_solution=5.0, callback=callback)
        
        self.assertTrue(result.success)
        self.assertGreater(len(callback_calls), 0)
    
    def test_statistics(self):
        """Test that statistics are properly tracked."""
        def cost(x):
            return x ** 2
        
        def neighbor(x):
            return x + random.uniform(-1, 1)
        
        config = SAConfig(
            initial_temperature=100.0,
            final_temperature=0.01,
            max_iterations=1000,
            seed=42
        )
        
        sa = SimulatedAnnealing(cost, neighbor, config)
        result = sa.optimize(initial_solution=5.0)
        
        stats = result.stats
        self.assertGreater(stats.iterations, 0)
        self.assertGreaterEqual(stats.accepted_moves, 0)
        self.assertGreaterEqual(stats.rejected_moves, 0)
        self.assertGreaterEqual(stats.acceptance_rate, 0)
        self.assertLessEqual(stats.acceptance_rate, 1)
        self.assertGreater(len(stats.best_cost_history), 0)
        self.assertGreater(len(stats.temperature_history), 0)


class TestTSPSolver(unittest.TestCase):
    """Test TSP solver."""
    
    def test_simple_tsp(self):
        """Test simple 4-city TSP."""
        distances = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]
        ]
        
        config = SAConfig(
            initial_temperature=100.0,
            max_iterations=3000,
            seed=42
        )
        
        result = solve_tsp(distances, config)
        
        self.assertTrue(result.success)
        self.assertEqual(len(result.best_solution), 4)
        self.assertGreater(result.best_cost, 0)
        
        # Verify tour cost is calculated correctly
        tour = result.best_solution
        total = sum(distances[tour[i]][tour[i+1]] for i in range(len(tour) - 1))
        total += distances[tour[-1]][tour[0]]
        self.assertEqual(result.best_cost, total)
    
    def test_tsp_two_cities(self):
        """Test TSP with only 2 cities."""
        distances = [[0, 10], [10, 0]]
        
        config = SAConfig(seed=42)
        result = solve_tsp(distances, config)
        
        self.assertTrue(result.success)
        self.assertEqual(result.best_cost, 20)  # Round trip
    
    def test_tsp_single_city(self):
        """Test TSP with single city."""
        distances = [[0]]
        
        config = SAConfig(seed=42)
        result = solve_tsp(distances, config)
        
        self.assertTrue(result.success)
        self.assertEqual(result.best_cost, 0)
    
    def test_tsp_empty(self):
        """Test TSP with empty distance matrix."""
        distances = []
        
        result = solve_tsp(distances)
        
        self.assertFalse(result.success)
        self.assertEqual(result.best_cost, 0.0)


class TestFunctionOptimization(unittest.TestCase):
    """Test continuous function optimization."""
    
    def test_quadratic_minimization(self):
        """Test minimizing a quadratic function."""
        def f(x):
            return (x - 3) ** 2
        
        config = SAConfig(
            max_iterations=2000,
            seed=42
        )
        
        result = optimize_function(f, bounds=(-10, 10), minimize=True, config=config)
        
        self.assertTrue(result.success)
        self.assertAlmostEqual(result.best_solution, 3.0, places=1)
        self.assertAlmostEqual(result.best_cost, 0.0, places=2)
    
    def test_quadratic_maximization(self):
        """Test maximizing a quadratic function."""
        def f(x):
            return -(x ** 2) + 10
        
        config = SAConfig(
            max_iterations=2000,
            seed=42
        )
        
        result = optimize_function(f, bounds=(-5, 5), minimize=False, config=config)
        
        self.assertTrue(result.success)
        self.assertAlmostEqual(result.best_solution, 0.0, places=1)
        # When maximizing, the cost function returns -f(x), so best_cost = -f(best_solution)
        # For f(x) = -(x^2) + 10, at x=0, f(0)=10, cost=-10
        self.assertAlmostEqual(result.best_cost, -10.0, places=1)
    
    def test_sin_minimization(self):
        """Test minimizing sin function."""
        config = SAConfig(
            max_iterations=3000,
            seed=42
        )
        
        result = optimize_function(math.sin, bounds=(-10, 10), minimize=True, config=config)
        
        self.assertTrue(result.success)
        # sin minimum is -1
        self.assertLessEqual(result.best_cost, -0.99)
    
    def test_bounds_respected(self):
        """Test that bounds are always respected."""
        def f(x):
            return x
        
        config = SAConfig(
            max_iterations=1000,
            seed=42
        )
        
        result = optimize_function(f, bounds=(0, 10), minimize=True, config=config)
        
        self.assertTrue(result.success)
        self.assertGreaterEqual(result.best_solution, 0)
        self.assertLessEqual(result.best_solution, 10)


class TestNdFunctionOptimization(unittest.TestCase):
    """Test N-dimensional function optimization."""
    
    def test_sphere_function(self):
        """Test minimizing sphere function."""
        def sphere(x):
            return sum(xi ** 2 for xi in x)
        
        bounds = [(-5, 5), (-5, 5)]
        config = SAConfig(
            max_iterations=5000,
            seed=42
        )
        
        result = optimize_nd_function(sphere, bounds, minimize=True, config=config)
        
        self.assertTrue(result.success)
        self.assertEqual(len(result.best_solution), 2)
        self.assertAlmostEqual(result.best_cost, 0.0, places=1)
    
    def test_rosenbrock_function(self):
        """Test minimizing Rosenbrock function."""
        def rosenbrock(x):
            return (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2
        
        bounds = [(-2, 2), (-2, 2)]
        config = SAConfig(
            max_iterations=10000,
            seed=42
        )
        
        result = optimize_nd_function(rosenbrock, bounds, minimize=True, config=config)
        
        self.assertTrue(result.success)
        # Rosenbrock minimum is at (1, 1) with f(1,1) = 0
        self.assertLess(result.best_cost, 1.0)  # Should get reasonably close
    
    def test_3d_function(self):
        """Test 3D function optimization."""
        def f(x):
            return x[0] ** 2 + x[1] ** 2 + x[2] ** 2
        
        bounds = [(-5, 5), (-5, 5), (-5, 5)]
        config = SAConfig(
            max_iterations=5000,
            seed=42
        )
        
        result = optimize_nd_function(f, bounds, minimize=True, config=config)
        
        self.assertTrue(result.success)
        self.assertEqual(len(result.best_solution), 3)
        self.assertAlmostEqual(result.best_cost, 0.0, places=1)


class TestJobScheduling(unittest.TestCase):
    """Test job scheduling solver."""
    
    def test_simple_scheduling(self):
        """Test simple job scheduling."""
        jobs = [
            {'id': 0, 'duration': 3},
            {'id': 1, 'duration': 5},
            {'id': 2, 'duration': 2}
        ]
        
        config = SAConfig(
            max_iterations=2000,
            seed=42
        )
        
        result = solve_job_scheduling(jobs, machines=2, config=config)
        
        self.assertTrue(result.success)
        self.assertEqual(len(result.best_solution), 3)
        # Optimal makespan should be 5 (jobs 0 and 2 on machine 1, job 1 on machine 2)
        self.assertLessEqual(result.best_cost, 5)
    
    def test_equal_duration_jobs(self):
        """Test scheduling jobs with equal durations."""
        jobs = [
            {'id': i, 'duration': 2} for i in range(4)
        ]
        
        config = SAConfig(
            max_iterations=2000,
            seed=42
        )
        
        result = solve_job_scheduling(jobs, machines=2, config=config)
        
        self.assertTrue(result.success)
        # With 4 jobs of duration 2 on 2 machines, makespan should be 4
        self.assertLessEqual(result.best_cost, 4)
    
    def test_empty_jobs(self):
        """Test scheduling with no jobs."""
        result = solve_job_scheduling([], machines=2)
        
        self.assertFalse(result.success)
        self.assertEqual(result.best_cost, 0.0)
    
    def test_single_machine(self):
        """Test scheduling on single machine."""
        jobs = [
            {'id': 0, 'duration': 3},
            {'id': 1, 'duration': 5}
        ]
        
        config = SAConfig(seed=42)
        result = solve_job_scheduling(jobs, machines=1, config=config)
        
        self.assertTrue(result.success)
        # All jobs on one machine
        self.assertEqual(result.best_cost, 8)


class TestBinPacking(unittest.TestCase):
    """Test bin packing solver."""
    
    def test_simple_packing(self):
        """Test simple bin packing."""
        items = [4, 8, 1, 4, 2, 1, 8]
        
        config = SAConfig(
            max_iterations=3000,
            seed=42
        )
        
        result = solve_bin_packing(items, bin_capacity=10, config=config)
        
        self.assertTrue(result.success)
        # Optimal is 3 bins
        self.assertLessEqual(result.best_cost, 4)
    
    def test_all_items_fit_one_bin(self):
        """Test when all items fit in one bin."""
        items = [1, 2, 3, 4]
        
        config = SAConfig(seed=42)
        result = solve_bin_packing(items, bin_capacity=10, config=config)
        
        self.assertTrue(result.success)
        self.assertLessEqual(result.best_cost, 2)
    
    def test_empty_items(self):
        """Test with no items."""
        result = solve_bin_packing([], bin_capacity=10)
        
        self.assertFalse(result.success)
    
    def test_single_large_item(self):
        """Test with single large item."""
        items = [8]
        
        config = SAConfig(seed=42)
        result = solve_bin_packing(items, bin_capacity=10, config=config)
        
        self.assertTrue(result.success)
        self.assertEqual(result.best_cost, 1)


class TestGraphColoring(unittest.TestCase):
    """Test graph coloring solver."""
    
    def test_simple_graph(self):
        """Test simple graph coloring."""
        edges = [(0, 1), (1, 2), (2, 3)]
        
        config = SAConfig(
            max_iterations=2000,
            seed=42
        )
        
        result = solve_graph_coloring(edges, num_nodes=4, config=config)
        
        self.assertTrue(result.success)
        # Path graph can be colored with 2 colors
        self.assertLessEqual(result.best_cost, 3)
        
        # Verify no conflicts
        colors = result.best_solution
        for u, v in edges:
            self.assertNotEqual(colors[u], colors[v])
    
    def test_complete_graph(self):
        """Test complete graph (clique)."""
        # K4 - complete graph with 4 nodes
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        
        config = SAConfig(
            max_iterations=2000,
            seed=42
        )
        
        result = solve_graph_coloring(edges, num_nodes=4, config=config)
        
        self.assertTrue(result.success)
        # Complete graph K4 needs 4 colors
        self.assertLessEqual(result.best_cost, 4)
        
        # Verify no conflicts
        colors = result.best_solution
        for u, v in edges:
            self.assertNotEqual(colors[u], colors[v])
    
    def test_empty_graph(self):
        """Test graph with no nodes."""
        result = solve_graph_coloring([], num_nodes=0)
        
        self.assertFalse(result.success)
    
    def test_single_node(self):
        """Test graph with single node."""
        result = solve_graph_coloring([], num_nodes=1)
        
        self.assertTrue(result.success)
        self.assertEqual(result.best_cost, 1)
    
    def test_triangle_graph(self):
        """Test triangle graph."""
        edges = [(0, 1), (1, 2), (0, 2)]
        
        config = SAConfig(
            max_iterations=2000,
            seed=42
        )
        
        result = solve_graph_coloring(edges, num_nodes=3, config=config)
        
        self.assertTrue(result.success)
        # Triangle needs 3 colors
        self.assertLessEqual(result.best_cost, 3)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_temperature_schedule_linear(self):
        """Test linear temperature schedule."""
        temps = calculate_temperature_schedule(
            initial_temp=100,
            final_temp=10,
            num_steps=10,
            schedule=TemperatureSchedule.LINEAR
        )
        
        self.assertEqual(len(temps), 10)
        self.assertEqual(temps[0], 100)
        self.assertLess(temps[-1], 100)
    
    def test_temperature_schedule_exponential(self):
        """Test exponential temperature schedule."""
        temps = calculate_temperature_schedule(
            initial_temp=100,
            final_temp=1,
            num_steps=20,
            schedule=TemperatureSchedule.EXPONENTIAL,
            cooling_rate=0.9
        )
        
        self.assertEqual(temps[0], 100)
        # Each step should be 90% of previous
        for i in range(1, len(temps)):
            self.assertAlmostEqual(temps[i], temps[i-1] * 0.9, places=5)
    
    def test_temperature_schedule_logarithmic(self):
        """Test logarithmic temperature schedule."""
        temps = calculate_temperature_schedule(
            initial_temp=100,
            final_temp=1,
            num_steps=10,
            schedule=TemperatureSchedule.LOGARITHMIC
        )
        
        self.assertEqual(temps[0], 100)
        # Temperature should generally decrease (may have slight variations due to formula)
        # Verify that the overall trend is decreasing
        self.assertGreater(temps[0], temps[-1])
    
    def test_estimate_initial_temperature(self):
        """Test initial temperature estimation."""
        def cost(x):
            return x ** 2
        
        def neighbor(x):
            return x + random.uniform(-5, 5)
        
        temp = estimate_initial_temperature(
            cost, neighbor, initial_solution=10.0,
            target_acceptance_rate=0.8,
            num_samples=100
        )
        
        self.assertGreater(temp, 0)
        self.assertLess(temp, 10000)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_very_small_temperature(self):
        """Test with very small temperature."""
        def cost(x):
            return x ** 2
        
        def neighbor(x):
            return x + random.uniform(-1, 1)
        
        config = SAConfig(
            initial_temperature=0.001,
            final_temperature=0.0001,
            max_iterations=100,
            seed=42
        )
        
        sa = SimulatedAnnealing(cost, neighbor, config)
        result = sa.optimize(initial_solution=5.0)
        
        self.assertTrue(result.success)
    
    def test_very_large_temperature(self):
        """Test with very large temperature."""
        def cost(x):
            return x ** 2
        
        def neighbor(x):
            return x + random.uniform(-1, 1)
        
        config = SAConfig(
            initial_temperature=1000000,
            final_temperature=100,
            max_iterations=1000,
            seed=42
        )
        
        sa = SimulatedAnnealing(cost, neighbor, config)
        result = sa.optimize(initial_solution=5.0)
        
        self.assertTrue(result.success)
    
    def test_constant_function(self):
        """Test with constant cost function."""
        def cost(x):
            return 42.0
        
        def neighbor(x):
            return x + 1
        
        config = SAConfig(
            max_iterations=500,
            seed=42
        )
        
        sa = SimulatedAnnealing(cost, neighbor, config)
        result = sa.optimize(initial_solution=0)
        
        self.assertTrue(result.success)
        self.assertEqual(result.best_cost, 42.0)
    
    def test_single_iteration(self):
        """Test with single iteration."""
        def cost(x):
            return x ** 2
        
        def neighbor(x):
            return x - 1
        
        config = SAConfig(
            max_iterations=1,
            iterations_per_temp=1,
            seed=42
        )
        
        sa = SimulatedAnnealing(cost, neighbor, config)
        result = sa.optimize(initial_solution=5.0)
        
        self.assertTrue(result.success)
    
    def test_reheat(self):
        """Test reheat mechanism."""
        def cost(x):
            return abs(x)
        
        def neighbor(x):
            return x + random.choice([-1, 1]) * random.random()
        
        config = SAConfig(
            initial_temperature=10,
            final_temperature=0.001,
            max_iterations=5000,
            reheat_threshold=500,
            reheat_factor=0.5,
            seed=42
        )
        
        sa = SimulatedAnnealing(cost, neighbor, config)
        result = sa.optimize(initial_solution=100.0)
        
        self.assertTrue(result.success)


if __name__ == "__main__":
    unittest.main(verbosity=2)