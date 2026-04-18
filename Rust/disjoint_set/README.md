# Disjoint Set (Union-Find) 🔗

A high-performance implementation of the disjoint-set (union-find) data structure with path compression and union by rank/size optimizations.

## Features

- **Path Compression**: Near O(α(n)) amortized time complexity where α is the inverse Ackermann function
- **Union Strategies**: Both union by rank and union by size supported
- **Connected Components**: Automatic tracking of connected component count
- **Set Size Queries**: Efficiently query the size of any set
- **Element Iteration**: Retrieve all elements within a set
- **Labeled Variant**: Support for arbitrary element types (strings, etc.)
- **Batch Operations**: Efficient bulk union operations
- **Zero External Dependencies**: Pure Rust standard library implementation

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
disjoint_set = { path = "./disjoint_set" }
```

## Quick Start

```rust
use disjoint_set::DisjointSet;

// Create a disjoint set with 10 elements (0-9)
let mut ds = DisjointSet::new(10);

// Initially, each element is in its own set
assert_eq!(ds.set_count(), 10);

// Union elements together
ds.union(0, 1); // Combine sets containing 0 and 1
ds.union(2, 3);
ds.union(1, 2); // Now {0,1,2,3} are in one set

// Check connectivity
assert!(ds.connected(0, 3));  // true: 0 and 3 are connected
assert!(!ds.connected(0, 4)); // false: 0 and 4 are not connected

// Query set size
assert_eq!(ds.set_size(0), 4);

// Get all elements in a set
let elements = ds.elements_in_set(0);
assert_eq!(elements.len(), 4);
```

## Union Strategies

```rust
use disjoint_set::{DisjointSet, UnionStrategy};

// Use union by rank (default, uses tree height)
let ds_rank = DisjointSet::with_strategy(100, UnionStrategy::ByRank);

// Use union by size (balances by number of elements)
let ds_size = DisjointSet::with_strategy(100, UnionStrategy::BySize);
```

## Labeled DisjointSet

For non-numeric element types:

```rust
use disjoint_set::LabeledDisjointSet;

let mut ds = LabeledDisjointSet::from_elements(vec!["Alice", "Bob", "Charlie", "David"]);

// Union by string labels
ds.union(&"Alice", &"Bob");
ds.union(&"Bob", &"Charlie");

// Check connectivity
assert!(ds.connected(&"Alice", &"Charlie"));
assert!(!ds.connected(&"Alice", &"David"));

// Get all sets
let groups = ds.all_sets();
// groups: [{"Alice", "Bob", "Charlie"}, {"David"}]
```

## Batch Operations

```rust
use disjoint_set::DisjointSet;

let mut ds = DisjointSet::new(100);

// Union many pairs at once
let pairs = vec![(0, 1), (2, 3), (1, 2), (4, 5)];
let merged_count = ds.batch_union(pairs);
// merged_count = 4 (successful merges)
```

## Creating from Edges

```rust
use disjoint_set::DisjointSet;

// Create directly from graph edges
let edges = vec![(0, 1), (1, 2), (3, 4), (4, 5)];
let mut ds = DisjointSet::from_edges(6, edges);

// Find connected components
let components = ds.all_sets();
// components: [{0,1,2}, {3,4,5}]
```

## Kruskal's MST Algorithm

```rust
use disjoint_set::DisjointSet;

fn kruskal_mst(n: usize, edges: &mut Vec<(usize, usize, u32)>) -> Vec<(usize, usize, u32)> {
    edges.sort_by_key(|e| e.2); // Sort by weight
    let mut ds = DisjointSet::new(n);
    let mut mst = Vec::new();
    
    for (u, v, w) in edges.iter() {
        if ds.union(*u, *v) {
            mst.push((*u, *v, *w));
        }
    }
    mst
}
```

## API Summary

### DisjointSet

| Method | Description |
|--------|-------------|
| `new(n)` | Create with n elements |
| `with_strategy(n, strategy)` | Create with specific union strategy |
| `from_edges(n, edges)` | Create from edge list |
| `from_components(n, components)` | Create from component groups |
| `find(x)` | Find root of element x |
| `connected(x, y)` | Check if x and y are connected |
| `union(x, y)` | Union sets containing x and y |
| `set_size(x)` | Get size of set containing x |
| `elements_in_set(x)` | Get all elements in x's set |
| `all_sets()` | Get all disjoint sets |
| `set_count()` | Number of disjoint sets |
| `reset()` | Reset to initial state |
| `batch_union(pairs)` | Union multiple pairs |
| `roots()` | Get all root elements |
| `isolated_elements()` | Get elements in singleton sets |
| `largest_set_size()` | Size of largest set |

### LabeledDisjointSet<T>

| Method | Description |
|--------|-------------|
| `new()` | Create empty labeled set |
| `from_elements(elements)` | Create from element list |
| `add_element(label)` | Add new element |
| `union(a, b)` | Union sets containing a and b |
| `connected(a, b)` | Check if a and b are connected |
| `set_size(label)` | Get size of set containing label |
| `elements_in_set(label)` | Get all elements in label's set |
| `all_sets()` | Get all disjoint sets |

## Time Complexity

| Operation | Complexity |
|-----------|------------|
| `find` | O(α(n)) amortized |
| `union` | O(α(n)) amortized |
| `connected` | O(α(n)) amortized |
| `set_size` | O(α(n)) amortized |
| `elements_in_set` | O(n) |
| `all_sets` | O(n) |

α(n) is the inverse Ackermann function, which is ≤ 5 for all practical values of n.

## Test Coverage

- 70 total tests (22 unit tests + 33 integration tests + 15 doc tests)
- Covers all major operations and edge cases
- Tests for path compression correctness
- Tests for large-scale operations (10,000+ elements)

## License

MIT