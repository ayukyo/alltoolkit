# Weighted Random Selector

A high-performance weighted random selector implementation using the **Alias Method** (Vose's algorithm). Provides O(1) time complexity for random selection after O(n) preprocessing.

## Features

- **O(1) Selection**: Constant time random selection after initial setup
- **Zero Dependencies**: Uses only Rust standard library (no external crates)
- **Generic Support**: Works with any type via Rust generics
- **Multiple Selection Methods**:
  - Single selection (with replacement)
  - Multiple selections (with replacement)
  - Unique selections (without replacement)
- **Builder Pattern**: Convenient way to build selectors
- **XorShift RNG**: Built-in fast random number generator
- **Interior Mutability**: Uses RefCell for safe mutation through shared references

## Quick Start

```rust
use weighted_random::{Selector, WeightedItem};

fn main() {
    // Create weighted items
    let items = vec![
        WeightedItem::new("common", 70.0),
        WeightedItem::new("rare", 20.0),
        WeightedItem::new("epic", 8.0),
        WeightedItem::new("legendary", 2.0),
    ];

    // Create selector
    let selector = Selector::new(items).unwrap();

    // Select random items based on weights
    println!("{}", selector.select()); // Weighted random selection
}
```

## API

### Creating a Selector

```rust
// Basic creation with WeightedItem
let items = vec![
    WeightedItem::new("a", 1.0),
    WeightedItem::new("b", 2.0),
];
let selector = Selector::new(items)?;

// With separate vectors
let selector = Selector::from_vectors(vec!["a", "b"], vec![1.0, 2.0])?;

// From a slice (uniform weights)
let items = vec!["a", "b", "c"];
let selector = Selector::from_slice(&items)?;

// Builder pattern
let selector = SelectorBuilder::new()
    .add("a", 1.0)
    .add("b", 2.0)
    .add("c", 3.0)
    .build()?;

// With seed for reproducible results
let selector = SelectorBuilder::new()
    .add("a", 1.0)
    .add("b", 2.0)
    .seed(42)
    .build()?;
```

### Selection Methods

```rust
// Single selection (O(1))
let item = selector.select();      // Returns reference
let item = selector.select_cloned(); // Returns cloned value
let index = selector.select_index(); // Returns index only

// Multiple selections with replacement
let items = selector.select_n_cloned(10);
let indices = selector.select_indices(10);

// Unique selections (without replacement)
let unique = selector.select_unique_cloned(3)?;
let unique_indices = selector.select_unique_indices(3)?;
```

### Utility Methods

```rust
// Get all items
let all = selector.items();      // Returns slice
let all = selector.items_cloned(); // Returns cloned Vec

// Get item count
let count = selector.len();

// Get total weight
let total = selector.total_weight();

// Check if empty
let empty = selector.is_empty();

// Get weight of specific item
let weights = selector.weights();

// Get probability of specific index
let prob = selector.probability(i);

// Get individual item
let item = selector.get(i);  // Option<&T>
```

## How It Works

The Alias Method works by:

1. **Preprocessing (O(n))**: Creating probability and alias tables that represent the weighted distribution
2. **Selection (O(1))**: Using two random numbers to select an item in constant time

### Algorithm Details (Vose's Method)

1. Normalize all weights and scale by n (number of items)
2. Partition items into "small" (< 1) and "large" (≥ 1) groups
3. Build alias table by pairing small and large items
4. During selection:
   - Pick a random index i
   - Generate a random probability r
   - If r < prob[i], return items[i]
   - Otherwise, return items[alias[i]]

## Examples

Run the included examples:

```bash
# Basic usage
cargo run --example basic

# Load balancer simulation
cargo run --example load_balancer

# Game loot table
cargo run --example loot_table
```

## Use Cases

- **Load Balancing**: Distribute requests based on server capacity
- **Game Mechanics**: Loot tables, gacha systems, weighted spawns
- **A/B Testing**: Assign users to variants with different weights
- **Ad Serving**: Select ads based on bid/campaign weights
- **Sampling**: Statistical sampling from weighted populations

## Testing

Run tests:

```bash
cargo test
```

## Performance

- Selection: O(1) - constant time
- Initialization: O(n) - linear time
- Memory: O(n) - stores items, probabilities, and aliases

## License

MIT License