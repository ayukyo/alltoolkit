# Disjoint Set Union (Union-Find) Utils

A comprehensive Python implementation of the Disjoint Set Union (DSU) data structure, also known as Union-Find. This data structure efficiently manages a partition of elements into disjoint subsets.

## Features

- **Path Compression**: O(α(n)) amortized find operations
- **Union by Rank/Size**: Balanced tree structure for optimal performance
- **Generic Type Support**: Works with any hashable type (int, str, tuple, etc.)
- **Undo Support**: Backtrack operations with `DisjointSetWithUndo`
- **Weighted Unions**: Track component weights with `WeightedDisjointSet`
- **Algorithm Helpers**: Connected components, cycle detection, Kruskal's MST

## Installation

No external dependencies! Pure Python implementation.

```bash
# Just copy the module to your project
cp -r disjoint_set_utils/ your_project/
```

## Quick Start

### Basic Usage

```python
from disjoint_set_utils import DisjointSet

# Create a disjoint set
ds = DisjointSet[int]()

# Create singleton sets
ds.make_sets([1, 2, 3, 4, 5])

# Unite sets
ds.union(1, 2)
ds.union(2, 3)

# Check connectivity
print(ds.connected(1, 3))  # True
print(ds.connected(1, 4))  # False

# Find representative (root)
print(ds.find(3))  # Same as ds.find(1)

# Get component size
print(ds.get_size(1))  # 3 (elements 1, 2, 3)

# Count disjoint sets
print(ds.count_sets())  # 3 (one with {1,2,3}, {4}, {5})
```

### String Elements

```python
from disjoint_set_utils import DisjointSet

ds = DisjointSet[str]()
ds.make_sets(['apple', 'banana', 'cherry'])

ds.union('apple', 'banana')
print(ds.connected('apple', 'banana'))  # True
print(ds.connected('apple', 'cherry'))  # False
```

### Grid/Coordinate Elements

```python
from disjoint_set_utils import DisjointSet

# Useful for maze/pathfinding problems
ds = DisjointSet[tuple]()
grid_size = 10

# Create cells
for i in range(grid_size):
    for j in range(grid_size):
        ds.make_set((i, j))

# Connect adjacent cells
for i in range(grid_size):
    for j in range(grid_size):
        if i + 1 < grid_size:
            ds.union((i, j), (i + 1, j))
        if j + 1 < grid_size:
            ds.union((i, j), (i, j + 1))

print(ds.count_sets())  # 1 (all connected)
```

### Weighted Disjoint Set

```python
from disjoint_set_utils import WeightedDisjointSet

wds = WeightedDisjointSet[str]()
wds.make_sets(['A', 'B', 'C', 'D'])

# Union with weights
wds.union_weighted('A', 'B', 5.0)
wds.union_weighted('B', 'C', 3.0)
wds.union_weighted('C', 'D', 2.0)

print(wds.get_component_weight('A'))  # 10.0
print(wds.same_component('A', 'D'))   # True
```

### Undo Support

```python
from disjoint_set_utils import DisjointSetWithUndo

ds = DisjointSetWithUndo[int]()
ds.make_sets([1, 2, 3, 4])

ds.union(1, 2)
ds.union(3, 4)
print(ds.count_sets())  # 2

ds.undo()  # Undo last union
print(ds.count_sets())  # 3

ds.undo()  # Undo another
print(ds.count_sets())  # 4
```

## Algorithm Helpers

### Count Connected Components

```python
from disjoint_set_utils import count_connected_components

# Graph with 5 vertices and edges
n = 5
edges = [(0, 1), (1, 2), (3, 4)]

components = count_connected_components(n, edges)
print(components)  # 2 (one component with {0,1,2}, another with {3,4})
```

### Detect Cycle in Undirected Graph

```python
from disjoint_set_utils import detect_cycle_undirected

# Graph with cycle: 0-1-2-0
has_cycle = detect_cycle_undirected(3, [(0, 1), (1, 2), (2, 0)])
print(has_cycle)  # True

# Graph without cycle
has_cycle = detect_cycle_undirected(3, [(0, 1), (1, 2)])
print(has_cycle)  # False
```

### Kruskal's MST Algorithm

```python
from disjoint_set_utils import kruskal_mst

# Graph with weighted edges (u, v, weight)
edges = [
    (0, 1, 4.0),
    (0, 2, 1.0),
    (1, 2, 2.0),
    (1, 3, 1.0),
    (2, 3, 5.0)
]

mst_edges, total_weight = kruskal_mst(4, edges)
print(f"MST weight: {total_weight}")  # 4.0
print(f"MST edges: {mst_edges}")     # [(0,2,1.0), (1,3,1.0), (1,2,2.0)]
```

### Find Redundant Connection

```python
from disjoint_set_utils import find_redundant_connection

# Graph where (2,3) creates a cycle
redundant = find_redundant_connection(3, [(1, 2), (1, 3), (2, 3)])
print(redundant)  # (2, 3)

# No redundant edge
redundant = find_redundant_connection(3, [(1, 2), (2, 3)])
print(redundant)  # None
```

## API Reference

### DisjointSet[T]

| Method | Description | Time Complexity |
|--------|-------------|-----------------|
| `make_set(x)` | Create singleton set | O(1) |
| `make_sets(elements)` | Create multiple singleton sets | O(n) |
| `find(x)` | Find representative with path compression | O(α(n))* |
| `union(x, y)` | Unite sets by rank | O(α(n))* |
| `union_by_size(x, y)` | Unite sets by size | O(α(n))* |
| `connected(x, y)` | Check if same set | O(α(n))* |
| `get_size(x)` | Get component size | O(α(n))* |
| `count_sets()` | Number of disjoint sets | O(1) |
| `get_sets()` | Get all sets as dict | O(n) |
| `get_members(x)` | Get all members of x's set | O(n) |

*α(n) is the inverse Ackermann function, effectively ≤ 4 for practical inputs.

### WeightedDisjointSet[T]

| Method | Description |
|--------|-------------|
| `union_weighted(x, y, weight)` | Union with associated weight |
| `get_component_weight(x)` | Total weight of component |
| `same_component(x, y)` | Check connectivity |

### DisjointSetWithUndo[T]

| Method | Description |
|--------|-------------|
| `undo()` | Undo last operation |
| `history_size()` | Number of undoable operations |

### Helper Functions

| Function | Description |
|----------|-------------|
| `count_connected_components(n, edges)` | Count graph components |
| `detect_cycle_undirected(n, edges)` | Detect cycle in undirected graph |
| `kruskal_mst(n, weighted_edges)` | Find minimum spanning tree |
| `find_redundant_connection(n, edges)` | Find edge creating cycle |

## Testing

```bash
cd disjoint_set_utils
python -m pytest test_disjoint_set.py -v
```

Or run directly:
```bash
python test_disjoint_set.py
```

## Use Cases

1. **Graph Algorithms**: Connected components, MST, cycle detection
2. **Image Processing**: Connected component labeling
3. **Network Analysis**: Finding network clusters
4. **Social Networks**: Group detection
5. **Maze Generation**: Kruskal's maze algorithm
6. **Dynamic Connectivity**: Online connectivity queries

## Time Complexity

| Operation | Worst Case | Amortized |
|-----------|------------|-----------|
| Find | O(log n) | O(α(n)) |
| Union | O(log n) | O(α(n)) |
| Make Set | O(1) | O(1) |

Where α(n) is the inverse Ackermann function, which grows extremely slowly. For all practical values of n, α(n) ≤ 4.

## License

MIT License - Part of AllToolkit

## Author

AllToolkit - 2026-05-20