# AVL Tree Utils

A zero-dependency Go implementation of a self-balancing AVL Tree data structure.

## Features

- **Self-balancing**: Automatically maintains balance after insertions and deletions
- **O(log n) operations**: All operations (insert, delete, search) are logarithmic
- **Generic**: Supports any comparable type using Go generics
- **Zero dependencies**: Pure Go standard library implementation
- **Full-featured**: Range queries, k-th element, predecessor/successor, and more

## Installation

```bash
go get avl_tree_utils
```

## Usage

### Basic Operations

```go
package main

import "avl_tree_utils"

func main() {
    // Create a new AVL tree for integers
    tree := avl_tree_utils.NewInt()
    
    // Insert elements
    tree.Insert(50)
    tree.Insert(30)
    tree.Insert(70)
    
    // Search
    if tree.Contains(30) {
        println("Found 30!")
    }
    
    // Delete
    tree.Delete(30)
    
    // Get size and height
    println("Size:", tree.Size())
    println("Height:", tree.Height())
}
```

### Creating Trees for Different Types

```go
// Integer tree
intTree := avl_tree_utils.NewInt()

// String tree
strTree := avl_tree_utils.NewString()

// Float64 tree
floatTree := avl_tree_utils.NewFloat64()

// Custom comparator
type Person struct {
    Name string
    Age  int
}

personTree := avl_tree_utils.New(func(a, b Person) int {
    if a.Age < b.Age {
        return -1
    } else if a.Age > b.Age {
        return 1
    }
    return 0
})
```

### Traversals

```go
tree := avl_tree_utils.NewInt()
tree.FromSlice([]int{50, 30, 70, 20, 40, 60, 80})

// In-order (sorted)
tree.InOrder()  // [20 30 40 50 60 70 80]

// Pre-order
tree.PreOrder()  // [50 30 20 40 70 60 80]

// Post-order
tree.PostOrder()  // [20 40 30 60 80 70 50]

// Level-order (breadth-first)
tree.LevelOrder()  // [50 30 70 20 40 60 80]
```

### Range Queries

```go
tree := avl_tree_utils.NewInt()
tree.FromSlice([]int{10, 20, 30, 40, 50, 60, 70})

// Get all keys in range [25, 55]
tree.Range(25, 55)  // [30 40 50]

// Count keys in range
tree.Count(25, 55)  // 3

// Lower bound (first key >= target)
tree.LowerBound(35)  // 40

// Upper bound (first key > target)
tree.UpperBound(35)  // 40
```

### K-th Element and Rank

```go
tree := avl_tree_utils.NewInt()
tree.FromSlice([]int{50, 30, 70, 20, 40, 60, 80})

// K-th smallest (1-indexed)
tree.KthSmallest(1)  // 20 (smallest)
tree.KthSmallest(4)  // 50

// K-th largest (1-indexed)
tree.KthLargest(1)   // 80 (largest)

// Rank of an element (1-indexed position in sorted order)
tree.Rank(40)  // 3
```

### Predecessor and Successor

```go
tree := avl_tree_utils.NewInt()
tree.FromSlice([]int{10, 30, 50, 70})

// Predecessor (largest key < target)
tree.Predecessor(50)  // 30

// Successor (smallest key > target)
tree.Successor(50)    // 70
```

### Validation and Balance Check

```go
tree := avl_tree_utils.NewInt()
tree.FromSlice([]int{50, 30, 70, 20, 40, 60, 80})

// Check if tree is balanced
tree.IsBalanced()  // true

// Validate all AVL properties
err := tree.Validate()  // nil if valid
```

### Iteration

```go
tree := avl_tree_utils.NewInt()
tree.FromSlice([]int{10, 20, 30, 40, 50})

// Iterate in sorted order
tree.ForEach(func(key int) bool {
    println(key)
    return true  // continue iteration
})
```

## API Reference

### Tree Creation

| Function | Description |
|----------|-------------|
| `New[T](comparator)` | Creates a new AVL tree with custom comparator |
| `NewInt()` | Creates a new integer AVL tree |
| `NewString()` | Creates a new string AVL tree |
| `NewFloat64()` | Creates a new float64 AVL tree |

### Basic Operations

| Method | Description |
|--------|-------------|
| `Insert(key) bool` | Inserts a key, returns false if duplicate |
| `Delete(key) bool` | Deletes a key, returns false if not found |
| `Search(key) *Node` | Returns node if found, nil otherwise |
| `Contains(key) bool` | Checks if key exists |
| `Size() int` | Returns number of elements |
| `IsEmpty() bool` | Returns true if empty |
| `Clear()` | Removes all elements |

### Min/Max

| Method | Description |
|--------|-------------|
| `Min() (T, bool)` | Returns minimum key |
| `Max() (T, bool)` | Returns maximum key |

### Traversals

| Method | Description |
|--------|-------------|
| `InOrder() []T` | Returns keys in ascending order |
| `PreOrder() []T` | Returns keys in pre-order |
| `PostOrder() []T` | Returns keys in post-order |
| `LevelOrder() []T` | Returns keys in level-order |
| `ForEach(func(T) bool)` | Iterates in sorted order |

### Range Queries

| Method | Description |
|--------|-------------|
| `Range(start, end) []T` | Returns keys in [start, end] |
| `Count(start, end) int` | Counts keys in [start, end] |
| `LowerBound(target) (T, bool)` | First key >= target |
| `UpperBound(target) (T, bool)` | First key > target |

### Order Statistics

| Method | Description |
|--------|-------------|
| `KthSmallest(k) (T, bool)` | k-th smallest key (1-indexed) |
| `KthLargest(k) (T, bool)` | k-th largest key (1-indexed) |
| `Rank(key) int` | Position in sorted order (1-indexed) |

### Navigation

| Method | Description |
|--------|-------------|
| `Predecessor(key) (T, bool)` | Largest key < target |
| `Successor(key) (T, bool)` | Smallest key > target |

### Validation

| Method | Description |
|--------|-------------|
| `Height() int` | Returns tree height |
| `IsBalanced() bool` | Checks AVL balance property |
| `Validate() error` | Validates all tree properties |

### Utility

| Method | Description |
|--------|-------------|
| `ToSlice() []T` | Returns all keys (alias for InOrder) |
| `FromSlice([]T) int` | Inserts all keys, returns count |
| `String() string` | String representation |

## Time Complexity

| Operation | Average | Worst |
|-----------|---------|-------|
| Insert | O(log n) | O(log n) |
| Delete | O(log n) | O(log n) |
| Search | O(log n) | O(log n) |
| Min/Max | O(log n) | O(log n) |
| Range | O(log n + k) | O(log n + k) |
| KthSmallest | O(n) | O(n) |

## Space Complexity

O(n) for storing n elements.

## License

MIT License