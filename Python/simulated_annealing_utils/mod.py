#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Simulated Annealing Utilities Module
==================================================
A comprehensive simulated annealing optimization utility module for Python with zero external dependencies.

Features:
    - Generic simulated annealing algorithm implementation
    - Multiple temperature schedule strategies (linear, exponential, logarithmic, adaptive)
    - Configurable cooling rates and acceptance criteria
    - Support for custom solution spaces and neighbor functions
    - Built-in optimization problems (TSP, function optimization, scheduling)
    - Convergence tracking and statistics
    - Restart and adaptive mechanisms

Author: AllToolkit Contributors
License: MIT
"""

import math
import random
from typing import Callable, List, Tuple, Optional, Any, Dict, TypeVar
from dataclasses import dataclass, field
from enum import Enum
from copy import deepcopy

# Generic type for solution representation
T = TypeVar('T')


class TemperatureSchedule(Enum):
    """Temperature schedule strategies."""
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"
    ADAPTIVE = "adaptive"


@dataclass
class SAConfig:
    """Configuration for simulated annealing algorithm."""
    initial_temperature: float = 1000.0
    final_temperature: float = 0.001
    cooling_rate: float = 0.95
    iterations_per_temp: int = 100
    schedule: TemperatureSchedule = TemperatureSchedule.EXPONENTIAL
    adaptive_alpha: float = 0.9  # For adaptive schedule
    adaptive_beta: float = 1.05  # For adaptive schedule
    reheat_threshold: int = 0  # Reheat after N iterations without improvement (0 = disabled)
    reheat_factor: float = 0.5  # Reheat to this fraction of initial temp
    max_iterations: int = 100000
    seed: Optional[int] = None
    verbose: bool = False


@dataclass
class SAStats:
    """Statistics from simulated annealing run."""
    best_cost: float
    best_solution: Any
    iterations: int
    accepted_moves: int
    rejected_moves: int
    temperature_history: List[float] = field(default_factory=list)
    cost_history: List[float] = field(default_factory=list)
    best_cost_history: List[float] = field(default_factory=list)
    acceptance_rate: float = 0.0
    final_temperature: float = 0.0
    reheats: int = 0


@dataclass
class OptimizationResult:
    """Result of an optimization run."""
    best_solution: Any
    best_cost: float
    stats: SAStats
    success: bool
    message: str = ""


class SimulatedAnnealing:
    """
    Generic Simulated Annealing optimizer.
    
    Simulated annealing is a probabilistic optimization technique inspired by
    the annealing process in metallurgy. It's particularly useful for finding
    approximate solutions to optimization problems with large search spaces.
    
    Example:
        >>> def cost_func(x):
        ...     return x ** 2
        >>> def neighbor_func(x):
        ...     return x + random.uniform(-1, 1)
        >>> sa = SimulatedAnnealing(cost_func, neighbor_func)
        >>> result = sa.optimize(initial_solution=10.0)
        >>> print(f"Best solution: {result.best_solution}, cost: {result.best_cost}")
    """
    
    def __init__(
        self,
        cost_function: Callable[[T], float],
        neighbor_function: Callable[[T], T],
        config: Optional[SAConfig] = None
    ):
        """
        Initialize simulated annealing optimizer.
        
        Args:
            cost_function: Function that computes the cost of a solution.
                          Lower cost means better solution.
            neighbor_function: Function that generates a neighboring solution
                              from the current solution.
            config: Configuration parameters (optional).
        """
        self.cost_function = cost_function
        self.neighbor_function = neighbor_function
        self.config = config or SAConfig()
        
        if self.config.seed is not None:
            random.seed(self.config.seed)
        
        # State tracking
        self.current_solution: Optional[T] = None
        self.current_cost: float = float('inf')
        self.best_solution: Optional[T] = None
        self.best_cost: float = float('inf')
        self.temperature: float = self.config.initial_temperature
        self.iterations: int = 0
        self.accepted_moves: int = 0
        self.rejected_moves: int = 0
        self.reheats: int = 0
        self.iterations_since_improvement: int = 0
        
        # History tracking
        self.temperature_history: List[float] = []
        self.cost_history: List[float] = []
        self.best_cost_history: List[float] = []
    
    def _acceptance_probability(self, current_cost: float, new_cost: float, 
                                 temperature: float) -> float:
        """
        Calculate acceptance probability for a move.
        
        Args:
            current_cost: Cost of current solution.
            new_cost: Cost of new solution.
            temperature: Current temperature.
            
        Returns:
            Probability of accepting the move (0 to 1).
        """
        if new_cost < current_cost:
            return 1.0
        if temperature <= 0:
            return 0.0
        return math.exp(-(new_cost - current_cost) / temperature)
    
    def _cool_temperature(self, temperature: float, iteration: int) -> float:
        """
        Calculate new temperature based on cooling schedule.
        
        Args:
            temperature: Current temperature.
            iteration: Current iteration number.
            
        Returns:
            New temperature.
        """
        schedule = self.config.schedule
        
        if schedule == TemperatureSchedule.LINEAR:
            # Linear cooling: T = T0 - alpha * iteration
            return max(
                self.config.final_temperature,
                temperature - (self.config.initial_temperature - self.config.final_temperature) / 
                (self.config.max_iterations / self.config.iterations_per_temp) * 
                self.config.cooling_rate
            )
        
        elif schedule == TemperatureSchedule.EXPONENTIAL:
            # Exponential cooling: T = T0 * alpha^k
            return max(self.config.final_temperature, temperature * self.config.cooling_rate)
        
        elif schedule == TemperatureSchedule.LOGARITHMIC:
            # Logarithmic cooling: T = T0 / (1 + alpha * log(k + 1))
            k = iteration // self.config.iterations_per_temp + 1
            alpha = 1.0  # Scaling factor
            new_temp = self.config.initial_temperature / (1 + alpha * math.log(k + 1))
            return max(self.config.final_temperature, new_temp)
        
        elif schedule == TemperatureSchedule.ADAPTIVE:
            # Adaptive cooling based on acceptance rate
            if self.accepted_moves + self.rejected_moves > 0:
                acceptance_rate = self.accepted_moves / (self.accepted_moves + self.rejected_moves)
                if acceptance_rate > 0.8:
                    return temperature * self.config.adaptive_alpha
                elif acceptance_rate < 0.2:
                    return temperature * self.config.adaptive_beta
            return temperature * self.config.cooling_rate
        
        return temperature * self.config.cooling_rate
    
    def _reheat(self) -> None:
        """Reheat the temperature for exploration."""
        self.temperature = self.config.initial_temperature * self.config.reheat_factor
        self.iterations_since_improvement = 0
        self.reheats += 1
        if self.config.verbose:
            print(f"Reheating to temperature {self.temperature:.4f}")
    
    def _step(self) -> Tuple[T, float, bool]:
        """
        Perform one step of simulated annealing.
        
        Returns:
            Tuple of (new solution, new cost, was accepted).
        """
        # Generate neighbor
        new_solution = self.neighbor_function(self.current_solution)
        new_cost = self.cost_function(new_solution)
        
        # Calculate acceptance probability
        prob = self._acceptance_probability(self.current_cost, new_cost, self.temperature)
        
        # Accept or reject
        if random.random() < prob:
            self.current_solution = new_solution
            self.current_cost = new_cost
            self.accepted_moves += 1
            accepted = True
            
            # Update best if improved
            if new_cost < self.best_cost:
                self.best_solution = new_solution
                self.best_cost = new_cost
                self.iterations_since_improvement = 0
        else:
            self.rejected_moves += 1
            accepted = False
        
        return new_solution, new_cost, accepted
    
    def optimize(self, initial_solution: T, callback: Optional[Callable[[int, float, T], None]] = None) -> OptimizationResult:
        """
        Run the simulated annealing optimization.
        
        Args:
            initial_solution: Starting solution.
            callback: Optional callback function called after each temperature level.
                      Receives (iteration, temperature, best_solution).
            
        Returns:
            OptimizationResult containing best solution and statistics.
        """
        # Initialize
        self.current_solution = initial_solution
        self.current_cost = self.cost_function(initial_solution)
        self.best_solution = initial_solution
        self.best_cost = self.current_cost
        self.temperature = self.config.initial_temperature
        self.iterations = 0
        self.accepted_moves = 0
        self.rejected_moves = 0
        self.reheats = 0
        self.iterations_since_improvement = 0
        self.temperature_history = []
        self.cost_history = []
        self.best_cost_history = []
        
        # Main loop
        while (self.temperature > self.config.final_temperature and 
               self.iterations < self.config.max_iterations):
            
            # Perform iterations at current temperature
            for _ in range(self.config.iterations_per_temp):
                if self.iterations >= self.config.max_iterations:
                    break
                
                self._step()
                self.iterations += 1
                
                # Track history
                if self.iterations % 100 == 0:
                    self.temperature_history.append(self.temperature)
                    self.cost_history.append(self.current_cost)
                    self.best_cost_history.append(self.best_cost)
                
                # Check for reheat
                if self.config.reheat_threshold > 0:
                    self.iterations_since_improvement += 1
                    if self.iterations_since_improvement >= self.config.reheat_threshold:
                        self._reheat()
            
            # Cool temperature
            self.temperature = self._cool_temperature(self.temperature, self.iterations)
            
            # Callback
            if callback:
                callback(self.iterations, self.temperature, self.best_solution)
            
            if self.config.verbose and self.iterations % 1000 == 0:
                print(f"Iteration {self.iterations}: Temp={self.temperature:.4f}, "
                      f"Best Cost={self.best_cost:.6f}, "
                      f"Acceptance Rate={self.accepted_moves/(self.accepted_moves+self.rejected_moves):.2%}")
        
        # Calculate final statistics
        total_moves = self.accepted_moves + self.rejected_moves
        acceptance_rate = self.accepted_moves / total_moves if total_moves > 0 else 0.0
        
        stats = SAStats(
            best_cost=self.best_cost,
            best_solution=self.best_solution,
            iterations=self.iterations,
            accepted_moves=self.accepted_moves,
            rejected_moves=self.rejected_moves,
            temperature_history=self.temperature_history,
            cost_history=self.cost_history,
            best_cost_history=self.best_cost_history,
            acceptance_rate=acceptance_rate,
            final_temperature=self.temperature,
            reheats=self.reheats
        )
        
        return OptimizationResult(
            best_solution=self.best_solution,
            best_cost=self.best_cost,
            stats=stats,
            success=True,
            message="Optimization completed successfully"
        )


# ============================================================================
# Built-in Problem Solvers
# ============================================================================

def solve_tsp(
    distances: List[List[float]],
    config: Optional[SAConfig] = None
) -> OptimizationResult:
    """
    Solve Traveling Salesman Problem using simulated annealing.
    
    Args:
        distances: Distance matrix where distances[i][j] is distance from city i to j.
        config: SA configuration (optional).
        
    Returns:
        OptimizationResult with best tour found.
        
    Example:
        >>> distances = [[0, 10, 15, 20], [10, 0, 35, 25],
        ...               [15, 35, 0, 30], [20, 25, 30, 0]]
        >>> result = solve_tsp(distances)
        >>> print(f"Best tour: {result.best_solution}")
        >>> print(f"Total distance: {result.best_cost}")
    """
    n = len(distances)
    if n == 0:
        return OptimizationResult([], 0.0, SAStats(0.0, [], 0, 0, 0), False, "Empty distance matrix")
    
    # Cost function: total tour distance
    def tour_cost(tour: List[int]) -> float:
        if len(tour) < 2:
            return 0.0
        total = sum(distances[tour[i]][tour[i+1]] for i in range(len(tour) - 1))
        total += distances[tour[-1]][tour[0]]  # Return to start
        return total
    
    # Neighbor function: swap two cities
    def swap_cities(tour: List[int]) -> List[int]:
        new_tour = tour.copy()
        if len(new_tour) < 2:
            return new_tour
        i, j = random.sample(range(len(new_tour)), 2)
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        return new_tour
    
    # 2-opt neighbor: reverse a segment
    def two_opt(tour: List[int]) -> List[int]:
        new_tour = tour.copy()
        if len(new_tour) < 2:
            return new_tour
        i, j = sorted(random.sample(range(len(new_tour)), 2))
        new_tour[i:j+1] = reversed(new_tour[i:j+1])
        return new_tour
    
    # Combined neighbor function
    def neighbor(tour: List[int]) -> List[int]:
        if random.random() < 0.5:
            return swap_cities(tour)
        return two_opt(tour)
    
    # Initial solution: random permutation
    initial_tour = list(range(n))
    random.shuffle(initial_tour)
    
    sa = SimulatedAnnealing(tour_cost, neighbor, config)
    return sa.optimize(initial_tour)


def optimize_function(
    func: Callable[[float], float],
    bounds: Tuple[float, float],
    minimize: bool = True,
    config: Optional[SAConfig] = None
) -> OptimizationResult:
    """
    Optimize a 1D continuous function using simulated annealing.
    
    Args:
        func: Function to optimize.
        bounds: (lower, upper) bounds for the search space.
        minimize: If True, minimize the function; otherwise maximize.
        config: SA configuration (optional).
        
    Returns:
        OptimizationResult with best x value found.
        
    Example:
        >>> def f(x):
        ...     return x ** 2 - 4 * x + 4
        >>> result = optimize_function(f, (-10, 10), minimize=True)
        >>> print(f"Minimum at x={result.best_solution:.4f}")
        >>> print(f"Function value: {result.best_cost:.4f}")
    """
    lower, upper = bounds
    
    # Cost function wrapper
    def cost(x: float) -> float:
        return func(x) if minimize else -func(x)
    
    # Neighbor function: add random Gaussian noise
    def neighbor(x: float) -> float:
        step = (upper - lower) * 0.1  # 10% of range
        new_x = x + random.gauss(0, step)
        return max(lower, min(upper, new_x))  # Clamp to bounds
    
    # Initial solution: middle of bounds
    initial_x = (lower + upper) / 2
    
    sa = SimulatedAnnealing(cost, neighbor, config)
    return sa.optimize(initial_x)


def optimize_nd_function(
    func: Callable[[List[float]], float],
    bounds: List[Tuple[float, float]],
    minimize: bool = True,
    config: Optional[SAConfig] = None
) -> OptimizationResult:
    """
    Optimize an N-dimensional continuous function using simulated annealing.
    
    Args:
        func: Function taking a list of N floats and returning a float.
        bounds: List of (lower, upper) bounds for each dimension.
        minimize: If True, minimize the function; otherwise maximize.
        config: SA configuration (optional).
        
    Returns:
        OptimizationResult with best N-dimensional vector found.
        
    Example:
        >>> def rosenbrock(x):
        ...     return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2
        >>> bounds = [(-5, 5), (-5, 5)]
        >>> result = optimize_nd_function(rosenbrock, bounds)
        >>> print(f"Minimum at {result.best_solution}")
    """
    n = len(bounds)
    
    # Cost function wrapper
    def cost(x: List[float]) -> float:
        return func(x) if minimize else -func(x)
    
    # Neighbor function
    def neighbor(x: List[float]) -> List[float]:
        new_x = x.copy()
        for i in range(n):
            step = (bounds[i][1] - bounds[i][0]) * 0.1
            new_x[i] += random.gauss(0, step)
            new_x[i] = max(bounds[i][0], min(bounds[i][1], new_x[i]))
        return new_x
    
    # Initial solution: center of bounds
    initial = [(bounds[i][0] + bounds[i][1]) / 2 for i in range(n)]
    
    sa = SimulatedAnnealing(cost, neighbor, config)
    return sa.optimize(initial)


def solve_job_scheduling(
    jobs: List[Dict[str, Any]],
    machines: int,
    config: Optional[SAConfig] = None
) -> OptimizationResult:
    """
    Solve job scheduling problem using simulated annealing.
    
    Args:
        jobs: List of job dictionaries, each with 'duration' and optionally 'deadline'.
        machines: Number of available machines.
        config: SA configuration (optional).
        
    Returns:
        OptimizationResult with best schedule found.
        
    Example:
        >>> jobs = [{'id': 0, 'duration': 3}, {'id': 1, 'duration': 5},
        ...         {'id': 2, 'duration': 2}]
        >>> result = solve_job_scheduling(jobs, machines=2)
        >>> print(f"Schedule: {result.best_solution}")
        >>> print(f"Makespan: {result.best_cost}")
    """
    if not jobs:
        return OptimizationResult([], 0.0, SAStats(0.0, [], 0, 0, 0), False, "No jobs to schedule")
    
    n = len(jobs)
    
    # Schedule representation: list of (job_idx, machine_idx, start_time)
    # We'll use a simpler representation: assignment of jobs to machines
    # then compute start times
    
    # Cost function: makespan (maximum completion time)
    def makespan(assignment: List[int]) -> float:
        """Assignment is a list mapping each job to a machine."""
        machine_times = [0.0] * machines
        for i, machine in enumerate(assignment):
            machine_times[machine] += jobs[i].get('duration', 1)
        return max(machine_times)
    
    # Neighbor: reassign a random job to a different machine
    def reassign(assignment: List[int]) -> List[int]:
        new_assignment = assignment.copy()
        if machines < 2:
            return new_assignment
        job_idx = random.randint(0, n - 1)
        new_machine = random.randint(0, machines - 1)
        while new_machine == assignment[job_idx]:
            new_machine = random.randint(0, machines - 1)
        new_assignment[job_idx] = new_machine
        return new_assignment
    
    # Initial solution: round-robin assignment
    initial = [i % machines for i in range(n)]
    
    sa = SimulatedAnnealing(makespan, reassign, config)
    return sa.optimize(initial)


def solve_bin_packing(
    items: List[float],
    bin_capacity: float,
    config: Optional[SAConfig] = None
) -> OptimizationResult:
    """
    Solve bin packing problem using simulated annealing.
    
    Args:
        items: List of item sizes.
        bin_capacity: Capacity of each bin.
        config: SA configuration (optional).
        
    Returns:
        OptimizationResult with bin assignments (item -> bin mapping).
        
    Example:
        >>> items = [4, 8, 1, 4, 2, 1, 8]
        >>> result = solve_bin_packing(items, bin_capacity=10)
        >>> print(f"Number of bins needed: {result.best_cost}")
    """
    if not items:
        return OptimizationResult([], 0.0, SAStats(0.0, [], 0, 0, 0), False, "No items to pack")
    
    n = len(items)
    
    # Cost function: number of bins used
    def count_bins(assignment: List[int]) -> float:
        """Count number of bins needed, with capacity constraints."""
        bins = {}
        for i, bin_idx in enumerate(assignment):
            if bin_idx not in bins:
                bins[bin_idx] = 0.0
            bins[bin_idx] += items[i]
            if bins[bin_idx] > bin_capacity:
                return float('inf')  # Invalid solution
        return float(len(bins))
    
    # Neighbor: move an item to a different bin
    def move_item(assignment: List[int]) -> List[int]:
        new_assignment = assignment.copy()
        i = random.randint(0, n - 1)
        # Try to find a bin that would still be valid
        max_bin = max(assignment) if assignment else 0
        new_bin = random.randint(0, max_bin + 1)  # Allow new bin
        new_assignment[i] = new_bin
        return new_assignment
    
    # Initial solution: first-fit
    initial = []
    bin_loads = [0.0]
    for item in items:
        placed = False
        for b, load in enumerate(bin_loads):
            if load + item <= bin_capacity:
                initial.append(b)
                bin_loads[b] += item
                placed = True
                break
        if not placed:
            initial.append(len(bin_loads))
            bin_loads.append(item)
    
    sa = SimulatedAnnealing(count_bins, move_item, config)
    return sa.optimize(initial)


def solve_graph_coloring(
    edges: List[Tuple[int, int]],
    num_nodes: int,
    max_colors: Optional[int] = None,
    config: Optional[SAConfig] = None
) -> OptimizationResult:
    """
    Solve graph coloring problem using simulated annealing.
    
    Args:
        edges: List of edges as (node1, node2) tuples.
        num_nodes: Total number of nodes.
        max_colors: Maximum number of colors allowed (optional).
        config: SA configuration (optional).
        
    Returns:
        OptimizationResult with color assignments (node -> color mapping).
        
    Example:
        >>> edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
        >>> result = solve_graph_coloring(edges, num_nodes=4)
        >>> print(f"Number of colors used: {result.best_cost}")
    """
    if num_nodes == 0:
        return OptimizationResult([], 0.0, SAStats(0.0, [], 0, 0, 0), False, "Empty graph")
    
    # Build adjacency list
    adj = [[] for _ in range(num_nodes)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    # Use degree + 1 as default max colors
    max_degree = max(len(neighbors) for neighbors in adj) if adj else 0
    if max_colors is None:
        max_colors = max_degree + 1
    
    # Cost function: number of colors used + penalty for conflicts
    def coloring_cost(colors: List[int]) -> float:
        conflicts = 0
        for u, v in edges:
            if colors[u] == colors[v]:
                conflicts += 1
        num_colors = len(set(colors))
        return num_colors + conflicts * 1000  # Heavy penalty for conflicts
    
    # Neighbor: change one node's color
    def recolor(colors: List[int]) -> List[int]:
        new_colors = colors.copy()
        node = random.randint(0, num_nodes - 1)
        new_color = random.randint(0, max_colors - 1)
        new_colors[node] = new_color
        return new_colors
    
    # Initial solution: greedy coloring
    initial = [0] * num_nodes
    for node in range(num_nodes):
        neighbor_colors = set(initial[neighbor] for neighbor in adj[node] if initial[neighbor] is not None)
        for c in range(num_nodes):  # Worst case: need at most num_nodes colors
            if c not in neighbor_colors:
                initial[node] = c
                break
    
    sa = SimulatedAnnealing(coloring_cost, recolor, config)
    return sa.optimize(initial)


# ============================================================================
# Utility Functions
# ============================================================================

def calculate_temperature_schedule(
    initial_temp: float,
    final_temp: float,
    num_steps: int,
    schedule: TemperatureSchedule = TemperatureSchedule.EXPONENTIAL,
    cooling_rate: float = 0.95
) -> List[float]:
    """
    Generate a temperature schedule.
    
    Args:
        initial_temp: Starting temperature.
        final_temp: Ending temperature.
        num_steps: Number of temperature steps.
        schedule: Type of cooling schedule.
        cooling_rate: Cooling rate for exponential schedule.
        
    Returns:
        List of temperatures.
    """
    temperatures = []
    temp = initial_temp
    
    for k in range(num_steps):
        temperatures.append(temp)
        
        if schedule == TemperatureSchedule.LINEAR:
            temp = initial_temp - (initial_temp - final_temp) * (k + 1) / num_steps
        elif schedule == TemperatureSchedule.EXPONENTIAL:
            temp *= cooling_rate
        elif schedule == TemperatureSchedule.LOGARITHMIC:
            alpha = 1.0
            temp = initial_temp / (1 + alpha * math.log(k + 1))
        
        if temp < final_temp:
            break
    
    return temperatures


def estimate_initial_temperature(
    cost_function: Callable[[T], float],
    neighbor_function: Callable[[T], T],
    initial_solution: T,
    target_acceptance_rate: float = 0.8,
    num_samples: int = 1000
) -> float:
    """
    Estimate a good initial temperature based on desired acceptance rate.
    
    Args:
        cost_function: Cost function.
        neighbor_function: Neighbor generation function.
        initial_solution: Starting solution.
        target_acceptance_rate: Desired acceptance rate (0 to 1).
        num_samples: Number of samples to use for estimation.
        
    Returns:
        Estimated initial temperature.
    """
    costs = []
    solution = initial_solution
    
    for _ in range(num_samples):
        new_solution = neighbor_function(solution)
        costs.append(cost_function(new_solution))
        solution = new_solution
    
    # Estimate temperature based on average positive cost differences
    if not costs:
        return 1000.0
    
    cost_std = math.sqrt(sum((c - sum(costs)/len(costs))**2 for c in costs) / len(costs))
    
    # Temperature that gives target acceptance rate for average positive difference
    # P = exp(-delta/T) => T = -delta / ln(P)
    if cost_std > 0:
        return -cost_std / math.log(target_acceptance_rate)
    return 1000.0


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Demo: Optimize a simple quadratic function
    print("Simulated Annealing Demo")
    print("=" * 50)
    
    # Example 1: 1D Function Optimization
    print("\n1. 1D Function Optimization (finding minimum of x^2 - 4x + 4)")
    
    def quadratic(x):
        return x ** 2 - 4 * x + 4
    
    result = optimize_function(quadratic, bounds=(-10, 10), minimize=True)
    print(f"   Best x: {result.best_solution:.4f}")
    print(f"   Best cost: {result.best_cost:.4f}")
    print(f"   Iterations: {result.stats.iterations}")
    print(f"   Acceptance rate: {result.stats.acceptance_rate:.2%}")
    
    # Example 2: TSP
    print("\n2. Traveling Salesman Problem (4 cities)")
    
    distances = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    
    result = solve_tsp(distances)
    print(f"   Best tour: {result.best_solution}")
    print(f"   Total distance: {result.best_cost:.2f}")
    print(f"   Iterations: {result.stats.iterations}")
    
    # Example 3: Job Scheduling
    print("\n3. Job Scheduling (3 jobs, 2 machines)")
    
    jobs = [
        {'id': 0, 'duration': 3},
        {'id': 1, 'duration': 5},
        {'id': 2, 'duration': 2}
    ]
    
    result = solve_job_scheduling(jobs, machines=2)
    print(f"   Assignment (job -> machine): {result.best_solution}")
    print(f"   Makespan: {result.best_cost:.2f}")
    print(f"   Iterations: {result.stats.iterations}")
    
    print("\n" + "=" * 50)
    print("Demo completed!")