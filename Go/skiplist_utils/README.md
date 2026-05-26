# Skip List Utilities

A thread-safe Skip List implementation in Go with O(log n) average time complexity for search, insert, and delete operations.

## Overview

A Skip List is a probabilistic data structure that combines the simplicity of linked lists with the efficiency of balanced trees. It maintains multiple levels of forward pointers, allowing fast traversal and search operations.

### Features

- **O(log n)** average time complexity for search, insert, and delete
- **Thread-safe** operations with read/write locks
- **Generic** implementation supporting any comparable key type
- **Sorted iteration** in ascending order
- **Range queries** for efficient range retrieval
- **Ranking operations** for order statistics
- **Zero external dependencies**

## Installation

```go
import skiplist "github.com/ayukyo/alltoolkit/Go/skiplist_utils"
```

## Quick Start

### Basic Usage

```go
package main

import (
    "fmt"
    skiplist "github.com/ayukyo/alltoolkit/Go/skiplist_utils"
)

func main() {
    // Create a skip list with int keys
    sl := skiplist.NewInt[string]()
    
    // Insert elements
    sl.Insert(3, "three")
    sl.Insert(1, "one")
    sl.Insert(4, "four")
    
    // Search
    val, found := sl.Search(1)
    fmt.Printf("Found: %v, Value: %s\n", found, val) // Found: true, Value: one
    
    // Delete
    sl.Delete(3)
}
```

### Pre-built Constructors

```go
// Integer keys
slInt := skiplist.NewInt[string]()

// String keys
slStr := skiplist.NewString[int]()

// Float64 keys
slFloat := skiplist.NewFloat64[string]()

// Custom comparison function
slCustom := skiplist.New[MyType, string](func(a, b MyType) int {
    // Return -1 if a < b, 1 if a > b, 0 if a == b
    return compareMyTypes(a, b)
})
```

## API Reference

### Core Operations

| Method | Description | Time Complexity |
|--------|-------------|-----------------|
| `Insert(key, value)` | Add or update a key-value pair | O(log n) |
| `Search(key)` | Find value by key | O(log n) |
| `Delete(key)` | Remove a key-value pair | O(log n) |
| `Contains(key)` | Check if key exists | O(log n) |
| `GetOrInsert(key, value)` | Get existing or insert new | O(log n) |

### Query Operations

| Method | Description |
|--------|-------------|
| `Min()` | Get minimum key and value |
| `Max()` | Get maximum key and value |
| `Range(start, end)` | Get all elements in range [start, end] |
| `LowerBound(key)` | Find first element >= key |
| `UpperBound(key)` | Find first element > key |

### Ranking Operations

| Method | Description |
|--------|-------------|
| `Rank(key)` | Get 0-based rank of a key |
| `GetByRank(rank)` | Get element at given rank |

### Iteration

| Method | Description |
|--------|-------------|
| `ForEach(fn)` | Iterate over all elements in sorted order |
| `ToSlice()` | Convert to sorted slice |

### Utility

| Method | Description |
|--------|-------------|
| `Length()` | Number of elements |
| `IsEmpty()` | Check if empty |
| `Level()` | Current maximum level |
| `Clear()` | Remove all elements |
| `Count(predicate)` | Count elements matching predicate |
| `FindFirst(predicate)` | Find first matching element |

## Examples

### Range Query

```go
sl := skiplist.NewInt[string]()
for i := 0; i < 20; i++ {
    sl.Insert(i, string(rune('a'+i)))
}

results := sl.Range(5, 10)
// Returns elements with keys 5, 6, 7, 8, 9, 10
```

### Sorted Iteration

```go
sl := skiplist.NewInt[string]()
sl.Insert(5, "five")
sl.Insert(2, "two")
sl.Insert(8, "eight")

sl.ForEach(func(key int, value string) bool {
    fmt.Printf("%d: %s\n", key, value)
    return true // Continue iteration
})
// Output:
// 2: two
// 5: five
// 8: eight
```

### Ranking

```go
sl := skiplist.NewInt[string]()
sl.Insert(100, "hundred")
sl.Insert(200, "two-hundred")
sl.Insert(300, "three-hundred")

rank, _ := sl.Rank(200)        // Returns 1
key, val, _ := sl.GetByRank(2) // Returns (300, "three-hundred")
```

### String Keys (Sorted Dictionary)

```go
dict := skiplist.NewString[int]()
dict.Insert("banana", 1)
dict.Insert("apple", 2)
dict.Insert("cherry", 3)

// Iteration yields keys in lexicographic order
dict.ForEach(func(key string, value int) bool {
    fmt.Printf("%s: %d\n", key, value)
    return true
})
// Output:
// apple: 2
// banana: 1
// cherry: 3
```

### Custom Sort Order

```go
// Descending order
sl := skiplist.New[int, string](func(a, b int) int {
    if a > b {
        return -1
    } else if a < b {
        return 1
    }
    return 0
})

sl.Insert(1, "one")
sl.Insert(5, "five")
sl.Insert(3, "three")
// Elements are sorted: 5, 3, 1
```

### Filtering

```go
sl := skiplist.NewInt[int]()
for i := 0; i <= 20; i++ {
    sl.Insert(i, i)
}

// Count even numbers
evenCount := sl.Count(func(key int, value int) bool {
    return key%2 == 0
})

// Find first element > 10
key, val, _ := sl.FindFirst(func(k int, v int) bool {
    return k > 10
})
```

### Thread Safety

```go
sl := skiplist.NewInt[int]()
var wg sync.WaitGroup

// Concurrent writes
for i := 0; i < 100; i++ {
    wg.Add(1)
    go func(val int) {
        defer wg.Done()
        sl.Insert(val, val*10)
    }(i)
}

// Concurrent reads
for i := 0; i < 100; i++ {
    wg.Add(1)
    go func(val int) {
        defer wg.Done()
        sl.Search(val)
    }(i)
}

wg.Wait()
```

## Performance

Benchmarks on a standard machine:

| Operation | Time (approx) |
|-----------|---------------|
| Insert | ~200-500 ns/op |
| Search | ~100-300 ns/op |
| Delete | ~200-500 ns/op |
| Range (1000 elements) | ~50 µs/op |

Time complexity:
- **Average case**: O(log n) for search, insert, delete
- **Worst case**: O(n) (rare, with probability ~1/2^n)
- **Space**: O(n) with ~2x average overhead

## Algorithm Details

The skip list uses probabilistic leveling:
- Each new node has a 50% chance of being promoted to the next level
- Maximum 16 levels by default
- Double hashing for deterministic level generation

The implementation includes:
- Read-write mutex for thread safety
- Memory-efficient node allocation
- Optimized range queries using level skipping

## When to Use

**Use Skip List when you need:**
- Sorted data with fast insertion/deletion
- Range queries
- Order statistics (rank, select)
- A simpler alternative to balanced trees

**Consider alternatives when:**
- You need O(1) access by index (use slice/array)
- You need O(1) average insert/delete at known positions (use linked list)
- Memory is extremely constrained

## License

MIT License