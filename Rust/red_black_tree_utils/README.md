# Red-Black Tree Utils

A self-balancing Binary Search Tree (BST) implementation using the Red-Black Tree algorithm with **zero external dependencies**.

## What is a Red-Black Tree?

A Red-Black Tree is a self-balancing binary search tree that maintains O(log n) height by enforcing five properties:

1. Every node is either red or black
2. The root is always black
3. All leaves (NIL nodes) are black
4. If a node is red, both its children must be black (no two consecutive red nodes)
5. Every path from root to leaves contains the same number of black nodes

These properties guarantee that the longest path is at most twice the length of the shortest path, ensuring O(log n) operations.

## Features

- **Self-balancing**: Automatically maintains O(log n) height after insertions and deletions
- **Full CRUD**: Insert, delete, search operations
- **Multiple traversals**: In-order, pre-order, post-order, level-order
- **Range queries**: Query values within a specified range
- **Predecessor/Successor**: Find the previous/next value efficiently
- **Min/Max**: Retrieve minimum and maximum values
- **Verification**: Built-in verification to ensure red-black properties
- **Color statistics**: Analyze the distribution of red and black nodes
- **Type safe**: Generic implementation works with any `Ord + Clone` type

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
red_black_tree_utils = { path = "path/to/red_black_tree_utils" }
```

## Usage

### Basic Operations

```rust
use red_black_tree_utils::RedBlackTree;

// Create a new tree
let mut tree = RedBlackTree::new();

// Insert values
tree.insert(50);
tree.insert(25);
tree.insert(75);
tree.insert(10);
tree.insert(30);

// Search
assert!(tree.contains(&25));
assert!(!tree.contains(&100));

// Min/Max
assert_eq!(tree.min(), Some(&10));
assert_eq!(tree.max(), Some(&75));

// Size and height
println!("Size: {}", tree.len());
println!("Height: {}", tree.height()); // O(log n)

// Verify tree properties
assert!(tree.verify());
```

### Traversals

```rust
// In-order (sorted output)
let sorted: Vec<_> = tree.iter().collect();

// Pre-order
let pre_order: Vec<_> = tree.iter_pre_order().collect();

// Post-order
let post_order: Vec<_> = tree.iter_post_order().collect();

// Level-order (BFS)
let level_order: Vec<_> = tree.iter_level_order().collect();
```

### Range Queries

```rust
let mut tree = RedBlackTree::new();
for i in 1..=100 {
    tree.insert(i);
}

// Get all values between 20 and 30 (inclusive)
let range = tree.range(&20, &30);
assert_eq!(range.len(), 11);
```

### Predecessor and Successor

```rust
let mut tree = RedBlackTree::new();
tree.insert(50);
tree.insert(25);
tree.insert(75);

// Largest value less than 50
assert_eq!(tree.predecessor(&50), Some(&25));

// Smallest value greater than 50
assert_eq!(tree.successor(&50), Some(&75));
```

### Remove and Clear

```rust
// Remove a value
tree.remove(&50);

// Clear all values
tree.clear();
```

### Custom Types

```rust
#[derive(Debug, Clone, Eq, PartialEq)]
struct Person {
    id: u32,
    name: String,
    age: u32,
}

impl Ord for Person {
    fn cmp(&self, other: &Self) -> Ordering {
        self.age.cmp(&other.age)
            .then_with(|| self.id.cmp(&other.id))
    }
}

impl PartialOrd for Person {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

let mut people: RedBlackTree<Person> = RedBlackTree::new();
people.insert(Person { id: 1, name: "Alice".into(), age: 30 });
people.insert(Person { id: 2, name: "Bob".into(), age: 25 });
```

### From Iterator

```rust
let tree: RedBlackTree<i32> = vec![5, 3, 7, 1, 9].into_iter().collect();
```

### Color Statistics

```rust
let mut tree = RedBlackTree::new();
for i in 1..=100 {
    tree.insert(i);
}

let (red, black) = tree.color_stats();
println!("Red nodes: {}, Black nodes: {}", red, black);

// Black height (number of black nodes on any root-to-leaf path)
println!("Black height: {}", tree.black_height());
```

## Performance

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Insert    | O(log n)       | O(1)            |
| Delete    | O(log n)       | O(1)            |
| Search    | O(log n)       | O(1)            |
| Min/Max   | O(log n)       | O(1)            |
| Predecessor/Successor | O(log n) | O(1)          |
| Range Query | O(k + log n)  | O(k)            |
| Traversal | O(n)           | O(h)            |

Where:
- n = number of nodes
- k = number of elements in range query result
- h = height of tree (≤ 2 log₂(n+1))

## Comparison with AVL Trees

| Feature | Red-Black Tree | AVL Tree |
|---------|---------------|----------|
| Balance | Less strict | More strict |
| Height | ≤ 2 log₂(n+1) | ≤ 1.44 log₂(n+2) |
| Lookup | Slightly slower | Faster |
| Insert/Delete | Faster (fewer rotations) | Slower (more rotations) |
| Use case | Frequent updates | Frequent lookups |

## Implementation Details

### Insertion

1. Perform standard BST insertion
2. Color the new node red
3. Fix violations by recoloring and rotating as needed
4. Ensure root is black

### Deletion

1. Perform standard BST deletion
2. Fix double-black violations if the deleted node was black
3. Rebalance using rotations and recoloring
4. Ensure root is black

### Rotations

- **Left Rotation**: Used when right child is red and left is black
- **Right Rotation**: Used when left child is red and left-left grandchild is red
- **Color Flip**: Used when both children are red

## Running Examples

```bash
# Basic usage
cargo run --example basic_usage

# Advanced usage
cargo run --example advanced_usage
```

## Running Tests

```bash
cargo test
```

## License

MIT License