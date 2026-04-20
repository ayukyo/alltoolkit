# SkipList - Skip List Implementation in Rust

A complete skip list implementation with ordered map, concurrent support, rank queries, and range queries. Zero external dependencies.

## Overview

A skip list is a probabilistic data structure that provides O(log n) average time complexity for search, insert, and delete operations. It serves as an elegant alternative to balanced trees with simpler implementation.

## Features

- **Zero external dependencies** - Pure Rust standard library implementation
- **Generic types** - Supports any `Ord + Clone` key type and any value type
- **Three variants**:
  - `SkipList` - Basic ordered key-value map
  - `IndexedSkipList` - Supports rank queries (get by rank, get rank of key)
  - `ConcurrentSkipList` - Thread-safe version using RwLock
- **Range queries** - Efficient iteration over key ranges
- **Iterator support** - Forward iteration with keys(), values(), iter()
- **Configurable** - Custom probability and max level settings
- **Clone and FromIterator** - Standard trait implementations

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
skiplist = { path = "path/to/skiplist" }
```

## Quick Start

### Basic SkipList

```rust
use skiplist::SkipList;

let mut list = SkipList::new();

// Insert values
list.insert(1, "one");
list.insert(2, "two");
list.insert(3, "three");

// Get values (keys are sorted)
assert_eq!(list.get(&2), Some(&"two"));

// Iterate in order
for (key, value) in list.iter() {
    println!("{}: {}", key, value);
}

// Remove
list.remove(&2);
```

### IndexedSkipList (Rank Queries)

```rust
use skiplist::IndexedSkipList;

let mut list = IndexedSkipList::new();
list.insert(10, "ten");
list.insert(30, "thirty");
list.insert(20, "twenty");

// Get element by rank (0-indexed)
assert_eq!(list.get_by_rank(0), Some((&10, &"ten")));  // First (smallest)
assert_eq!(list.get_by_rank(2), Some((&30, &"thirty"))); // Last (largest)

// Get rank of a key
assert_eq!(list.rank_of(&20), Some(1));  // 20 is the second element

// Count elements less than/greater than
assert_eq!(list.count_less_than(&20), 1);  // Only 10 is less than 20
```

### ConcurrentSkipList (Thread-safe)

```rust
use skiplist::ConcurrentSkipList;
use std::sync::Arc;
use std::thread;

let list = Arc::new(ConcurrentSkipList::new());

// Multiple threads can read and write
let list_clone = Arc::clone(&list);
thread::spawn(move || {
    list_clone.insert(1, "one");
});

// Read from another thread
let list_clone = Arc::clone(&list);
thread::spawn(move || {
    if let Some(v) = list_clone.get(&1) {
        println!("Got: {}", v);
    }
});
```

### Range Queries

```rust
use skiplist::SkipList;

let mut list = SkipList::new();
for i in 0..20 {
    list.insert(i, i * 2);
}

// Range from 5 to 10 (exclusive)
for (k, v) in list.range(5..10) {
    println!("{}: {}", k, v);
}

// Range from 15 to end
for (k, v) in list.range(15..) {
    println!("{}: {}", k, v);
}
```

## API Reference

### SkipList

| Method | Description | Complexity |
|--------|-------------|------------|
| `new()` | Create empty list | O(1) |
| `with_config(config)` | Create with custom config | O(1) |
| `with_capacity(n)` | Optimized for n elements | O(1) |
| `insert(key, value)` | Insert/update key-value | O(log n) avg |
| `get(&key)` | Get value by key | O(log n) avg |
| `get_mut(&key)` | Get mutable value | O(log n) avg |
| `remove(&key)` | Remove key-value | O(log n) avg |
| `contains_key(&key)` | Check if key exists | O(log n) avg |
| `first_key_value()` | Get smallest key | O(1) |
| `last_key_value()` | Get largest key | O(log n) |
| `iter()` | Forward iterator | O(1) per step |
| `keys()` / `values()` | Key/value iterators | O(1) per step |
| `range(bounds)` | Range iterator | O(log n) start |
| `len()` | Element count | O(1) |
| `clear()` | Remove all elements | O(n) |
| `clone()` | Clone the list | O(n) |

### IndexedSkipList

| Method | Description | Complexity |
|--------|-------------|------------|
| `get_by_rank(rank)` | Get element at rank | O(log n) |
| `rank_of(&key)` | Get rank of key | O(log n) |
| `count_less_than(&key)` | Count smaller keys | O(log n) |
| `count_greater_than(&key)` | Count larger keys | O(log n) |

### ConcurrentSkipList

Thread-safe wrapper using `RwLock`. All operations return cloned values for safety.

### SkipListConfig

```rust
let config = SkipListConfig {
    probability: 0.25,  // Level promotion probability (0.1-0.5)
    max_level: 16,      // Maximum levels (min 4)
};

// Or use optimal config for expected size
let config = SkipListConfig::optimal_for_size(100_000);
```

## Examples

Run examples with:

```bash
cargo run --example basic_operations
cargo run --example ordered_map
cargo run --example range_queries
cargo run --example rank_queries
cargo run --example concurrent
cargo run --example performance
cargo run --example leaderboard
```

## Time Complexity

| Operation | Average | Worst |
|-----------|---------|-------|
| Insert | O(log n) | O(n) |
| Search | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| First/Last | O(1) / O(log n) | O(1) / O(n) |
| Iteration | O(1) per step | - |
| Range query start | O(log n) | O(n) |
| Get by rank | O(log n) | O(n) |
| Get rank of key | O(log n) | O(n) |

Note: Worst case O(n) is extremely rare (probability ~1/2^max_level).

## Memory Usage

Average memory overhead per element is approximately `1/(1-p)` pointers, where `p` is the promotion probability. With default `p=0.25`:

- Expected pointers per node: 1.33
- Overhead ratio: 33%

Use `config.expected_overhead()` to calculate.

## Testing

Run all tests:

```bash
cargo test
```

The test suite includes:
- Basic operations tests
- Range query tests
- IndexedSkipList rank tests
- ConcurrentSkipList thread tests
- Edge case tests (negative keys, duplicates, etc.)
- Stress tests (large scale operations)

## License

MIT License