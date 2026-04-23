# AVL Tree Utils

A self-balancing Binary Search Tree (BST) implementation using the AVL algorithm with **zero external dependencies**.

## Features

- **Self-balancing**: Automatically maintains O(log n) height after insertions and deletions
- **Full CRUD**: Insert, delete, search operations
- **Multiple traversals**: In-order, pre-order, post-order, level-order
- **Range queries**: Query values within a specified range
- **Predecessor/Successor**: Find the previous/next value efficiently
- **Min/Max**: Retrieve minimum and maximum values
- **Type safe**: Generic implementation works with any `Ord` type
- **Verified**: Built-in verification to ensure tree properties

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
avl_tree_utils = { path = "path/to/avl_tree_utils" }
```

## Usage

### Basic Operations

```rust
use avl_tree_utils::AVLTree;

// Create a new tree
let mut tree = AVLTree::new();

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
let mut tree = AVLTree::new();
for i in 1..=100 {
    tree.insert(i);
}

// Get all values between 20 and 30 (inclusive)
let range = tree.range(&20, &30);
assert_eq!(range.len(), 11);
```

### Predecessor and Successor

```rust
let mut tree = AVLTree::new();
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

let mut people: AVLTree<Person> = AVLTree::new();
people.insert(Person { id: 1, name: "Alice".into(), age: 30 });
people.insert(Person { id: 2, name: "Bob".into(), age: 25 });
```

### From Iterator

```rust
let tree: AVLTree<i32> = vec![5, 3, 7, 1, 9].into_iter().collect();
```

## Performance

| Operation | Time Complexity |
|-----------|-----------------|
| Insert    | O(log n)        |
| Delete    | O(log n)        |
| Search    | O(log n)        |
| Min/Max   | O(log n)        |
| Predecessor/Successor | O(log n) |
| Range Query | O(k + log n)  |
| Traversal | O(n)            |

## Implementation Details

The AVL tree maintains balance by ensuring the height difference between left and right subtrees of any node is at most 1. When this balance is violated after an insert or delete, rotations are performed:

- **Left Rotation**: Used when the right subtree is too heavy
- **Right Rotation**: Used when the left subtree is too heavy
- **Left-Right Rotation**: Combination for double imbalance
- **Right-Left Rotation**: Combination for double imbalance

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