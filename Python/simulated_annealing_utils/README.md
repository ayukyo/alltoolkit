# Simulated Annealing Utilities

A comprehensive simulated annealing optimization module for Python with zero external dependencies.

## Features

- **Generic Simulated Annealing Algorithm**: Flexible implementation that works with any problem domain
- **Multiple Cooling Schedules**: Linear, exponential, logarithmic, and adaptive temperature schedules
- **Built-in Problem Solvers**: Pre-configured solutions for common optimization problems
  - Traveling Salesman Problem (TSP)
  - Function Optimization (1D and N-Dimensional)
  - Job Scheduling
  - Bin Packing
  - Graph Coloring
- **Zero Dependencies**: Pure Python implementation using only standard library
- **Comprehensive Testing**: Full test suite with edge case coverage
- **Rich Examples**: 10 practical examples demonstrating various use cases

## Installation

No installation required! Simply copy the `mod.py` file to your project.

```python
from simulated_annealing_utils.mod import SimulatedAnnealing, SAConfig
```

## Quick Start

### Basic Usage

```python
from mod import SimulatedAnnealing, SAConfig

# Define your cost function (lower is better)
def cost_function(x):
    return x ** 2  # Minimize x^2

# Define how to generate neighbor solutions
def neighbor_function(x):
    import random
    return x + random.uniform(-1, 1)

# Configure and run
config = SAConfig(initial_temperature=100.0, max_iterations=5000)
sa = SimulatedAnnealing(cost_function, neighbor_function, config)
result = sa.optimize(initial_solution=10.0)

print(f"Best solution: {result.best_solution}")
print(f"Best cost: {result.best_cost}")
```

### Using Built-in Solvers

#### Traveling Salesman Problem

```python
from mod import solve_tsp, SAConfig

distances = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

result = solve_tsp(distances)
print(f"Best tour: {result.best_solution}")
print(f"Total distance: {result.best_cost}")
```

#### Function Optimization

```python
from mod import optimize_function

def my_function(x):
    return (x - 3) ** 2  # Find minimum at x=3

result = optimize_function(my_function, bounds=(-10, 10), minimize=True)
print(f"Minimum at x={result.best_solution:.4f}")
```

#### N-Dimensional Optimization

```python
from mod import optimize_nd_function

def rosenbrock(x):
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

bounds = [(-5, 5), (-5, 5)]
result = optimize_nd_function(rosenbrock, bounds)
print(f"Minimum at {result.best_solution}")
```

#### Job Scheduling

```python
from mod import solve_job_scheduling

jobs = [
    {'id': 'A', 'duration': 3},
    {'id': 'B', 'duration': 5},
    {'id': 'C', 'duration': 2}
]

result = solve_job_scheduling(jobs, machines=2)
print(f"Assignment: {result.best_solution}")
print(f"Makespan: {result.best_cost}")
```

#### Bin Packing

```python
from mod import solve_bin_packing

items = [4, 8, 1, 4, 2, 1, 8]
result = solve_bin_packing(items, bin_capacity=10)
print(f"Bins needed: {result.best_cost}")
```

#### Graph Coloring

```python
from mod import solve_graph_coloring

edges = [(0, 1), (1, 2), (2, 3), (0, 2)]
result = solve_graph_coloring(edges, num_nodes=4)
print(f"Colors used: {result.best_cost}")
print(f"Coloring: {result.best_solution}")
```

## Configuration Options

```python
from mod import SAConfig, TemperatureSchedule

config = SAConfig(
    initial_temperature=1000.0,      # Starting temperature
    final_temperature=0.001,          # Stopping temperature
    cooling_rate=0.95,                # Cooling multiplier (for exponential)
    iterations_per_temp=100,          # Iterations at each temperature
    schedule=TemperatureSchedule.EXPONENTIAL,  # Cooling strategy
    max_iterations=100000,            # Maximum total iterations
    seed=42,                          # Random seed for reproducibility
    reheat_threshold=500,             # Reheat after N iterations without improvement
    reheat_factor=0.5,                # Reheat to this fraction of initial temp
    verbose=False                     # Print progress
)
```

### Cooling Schedules

- **LINEAR**: `T = T0 - alpha * iteration`
- **EXPONENTIAL**: `T = T0 * alpha^k` (most common)
- **LOGARITHMIC**: `T = T0 / log(k + 1)` (slow cooling)
- **ADAPTIVE**: Adjusts based on acceptance rate

## How Simulated Annealing Works

Simulated annealing is inspired by the metallurgical process of annealing:

1. **Start with a high temperature**: The algorithm accepts worse solutions with high probability, allowing exploration of the solution space.

2. **Cool down gradually**: As temperature decreases, the algorithm becomes more selective, accepting only better or slightly worse solutions.

3. **Acceptance probability**: For a new solution with cost `c_new` and current solution with cost `c_current`:
   - If `c_new < c_current`: Always accept (better solution)
   - If `c_new > c_current`: Accept with probability `exp(-(c_new - c_current) / T)`

4. **Convergence**: At low temperatures, the algorithm converges to a near-optimal solution.

## Tips for Good Results

1. **Choose appropriate initial temperature**: Should be high enough to accept most moves initially
2. **Balance exploration vs exploitation**: More iterations at each temperature for better local search
3. **Good neighbor function**: Small, meaningful changes usually work better than large random jumps
4. **Multiple runs**: Run multiple times with different seeds for better coverage
5. **Use reheat**: Enable reheat for complex landscapes to escape local optima

## Testing

Run the test suite:

```bash
python simulated_annealing_utils_test.py
```

## Examples

Run the examples:

```bash
cd examples
python usage_examples.py
```

## API Reference

### Classes

- **SimulatedAnnealing**: Main optimizer class
- **SAConfig**: Configuration dataclass
- **SAStats**: Statistics dataclass
- **OptimizationResult**: Result dataclass

### Functions

- **solve_tsp(distances, config)**: Solve TSP
- **optimize_function(func, bounds, minimize, config)**: Optimize 1D function
- **optimize_nd_function(func, bounds, minimize, config)**: Optimize N-D function
- **solve_job_scheduling(jobs, machines, config)**: Solve scheduling
- **solve_bin_packing(items, bin_capacity, config)**: Solve bin packing
- **solve_graph_coloring(edges, num_nodes, max_colors, config)**: Solve graph coloring
- **calculate_temperature_schedule(...)**: Generate temperature schedule
- **estimate_initial_temperature(...)**: Estimate good initial temperature

## License

MIT License

## Author

AllToolkit Contributors