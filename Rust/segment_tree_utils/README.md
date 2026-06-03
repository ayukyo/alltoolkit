# segment_tree_utils

**Segment Tree with Lazy Propagation** — zero-dependency Rust library for fast range queries and updates.

## Features

- **Range queries** — sum, min, max, product, or any custom monoid
- **Range updates** — add, set, multiply with lazy propagation
- **Point updates** — modify single elements
- **O(log n)** per query and update
- **Zero external dependencies** — pure `no_std` Rust

## Complexity

| Operation | Time | Space |
|---|---|---|
| Build | O(n) | O(n) |
| Point update | O(log n) | — |
| Range update | O(log n) | — |
| Range query | O(log n) | — |

## Usage

```rust
use segment_tree_utils::{SegmentTree, SegmentTreeOps};

// Sum tree
let arr = [1, 3, 2, 7, 5, 9, 4];
let mut seg = SegmentTree::from_slice(&arr, segment_tree_utils::Sum {});

assert_eq!(seg.query(0..4), 13);   // 1+3+2+7
seg.update_range(1..4, 10);       // add 10 to [1,4)
assert_eq!(seg.query(0..4), 43);  // 1+13+12+17
seg.point_set(2, 100);            // set index 2 to 100
assert_eq!(seg.query(0..4), 121);

// Min tree
let arr2 = [5, 2, 8, 1, 9, 3, 7];
let seg_min = SegmentTree::from_slice(&arr2, segment_tree_utils::Min {});
assert_eq!(seg_min.query(0..7), 1); // minimum element

// Max tree
let seg_max = SegmentTree::from_slice(&arr2, segment_tree_utils::Max {});
assert_eq!(seg_max.query(4..7), 9);
```

## Adding to your project

```toml
[dependencies]
segment_tree_utils = { path = "path/to/segment_tree_utils" }
```

## Run tests

```bash
cargo test
```

## Run examples

```bash
cargo run --example basic
```
