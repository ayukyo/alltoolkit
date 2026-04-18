# Red-Black Tree

A complete, zero-dependency implementation of the Red-Black Tree data structure in Go.

## Overview

A Red-Black Tree is a self-balancing binary search tree that guarantees O(log n) time complexity for insert, delete, and search operations. This implementation follows the standard Red-Black Tree properties:

1. Every node is either red or black
2. The root is black
3. All leaves (NIL) are black
4. Red nodes have black children
5. All paths from a node to its descendant leaves contain the same number of black nodes

## Features

### Core Operations
- **Insert** - Add elements with automatic rebalancing
- **Delete** - Remove elements while maintaining balance
- **Search** - Find elements by key
- **Contains** - Check if key exists

### Ordered Operations
- **Min/Max** - Get minimum and maximum keys
- **LowerBound** - Find first key >= target
- **UpperBound** - Find first key > target

### Range Operations
- **Range** - Get all keys in a range
- **Count** - Count keys in a range

### Traversal
- **InOrder** - Keys in ascending order
- **PreOrder** - Root, left, right order
- **PostOrder** - Left, right, root order
- **ForEach** - Iterate with callback (supports early termination)

### Utility
- **Size** - Number of elements
- **Height** - Tree height (O(log n) guaranteed)
- **Validate** - Verify Red-Black Tree properties
- **Clear** - Remove all elements
- **ToSlice/FromSlice** - Bulk operations

## Usage

### Basic Integer Tree

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/go/red_black_tree"
)

func main() {
    tree := red_black_tree.NewInt()
    
    // Insert elements
    tree.Insert(5)
    tree.Insert(3)
    tree.Insert(7)
    
    // Search
    fmt.Println(tree.Contains(5))  // true
    
    // Traversal
    fmt.Println(tree.InOrder())    // [3, 5, 7]
    
    // Min/Max
    min, _ := tree.Min()  // 3
    max, _ := tree.Max()  // 7
}
```

### String Tree

```go
tree := red_black_tree.NewString()
tree.Insert("banana")
tree.Insert("apple")
tree.Insert("cherry")

fmt.Println(tree.InOrder())  // [apple, banana, cherry]
```

### Custom Comparator

```go
// Descending order tree
tree := red_black_tree.New(func(a, b int) int {
    if a > b {
        return -1
    } else if a < b {
        return 1
    }
    return 0
})
```

### Range Queries

```go
tree := red_black_tree.NewInt()
for i := 1; i <= 20; i++ {
    tree.Insert(i)
}

// Get keys in range
fmt.Println(tree.Range(5, 10))  // [5, 6, 7, 8, 9, 10]

// Count in range
fmt.Println(tree.Count(5, 15))  // 11

// LowerBound: first key >= target
key, found := tree.LowerBound(5)  // 5, true

// UpperBound: first key > target
key, found := tree.UpperBound(5)  // 6, true
```

### Validation

```go
tree := red_black_tree.NewInt()
tree.Insert(5)
tree.Insert(3)
tree.Insert(7)

// Verify tree properties
if err := tree.Validate(); err != nil {
    fmt.Println("Invalid tree:", err)
} else {
    fmt.Println("Tree is valid")
}
```

## Performance

| Operation | Time Complexity |
|-----------|-----------------|
| Insert    | O(log n)        |
| Delete    | O(log n)        |
| Search    | O(log n)        |
| Min/Max   | O(log n)        |
| Range     | O(k + log n)    |
| InOrder   | O(n)            |

Where k is the number of elements in the range.

## Zero Dependencies

This implementation uses only Go standard library, making it:
- Easy to deploy
- No version conflicts
- Fully testable

## Files

- `mod.go` - Main implementation
- `red_black_tree_test.go` - Comprehensive tests
- `examples/usage_examples.go` - Usage examples
- `go.mod` - Go module definition
- `README.md` - This documentation