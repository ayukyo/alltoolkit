# heap_utils - Heap Data Structures for Go

A comprehensive heap utilities package providing easy-to-use heap data structures for Go. Wraps the standard library's `container/heap` interface with a simpler, type-safe API using generics.

## Features

- **MinHeap**: Minimum value at root, pops smallest first
- **MaxHeap**: Maximum value at root, pops largest first
- **PriorityQueue**: Priority-based queue with custom priorities
- **GenericHeap**: Custom comparator for any type
- **TopK/BottomK**: Efficient selection of extreme values
- **MergeKSorted**: Merge multiple sorted sequences
- **HeapSort**: In-place heap sort utilities
- **NthElement**: Find nth smallest/largest, median

## Time Complexity

| Operation | Complexity |
|-----------|------------|
| Push | O(log n) |
| Pop | O(log n) |
| Peek | O(1) |
| TopK | O(n log k) |
| MergeKSorted | O(n log k) |
| HeapSort | O(n log n) |

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/heap_utils
```

## Quick Start

### MinHeap

```go
package main

import (
    "fmt"
    heap_utils "github.com/ayukyo/alltoolkit/Go/heap_utils"
)

func main() {
    // Create a min-heap
    h := heap_utils.NewMinHeap(5, 3, 8, 1, 9)
    
    // Peek at minimum
    top, _ := h.Peek()  // 1
    
    // Pop elements in ascending order
    for !h.IsEmpty() {
        fmt.Println(h.Pop())  // 1, 3, 5, 8, 9
    }
}
```

### MaxHeap

```go
// Create a max-heap
h := heap_utils.NewMaxHeap(5, 3, 8, 1, 9)

top, _ := h.Peek()  // 9

// Pop elements in descending order
for !h.IsEmpty() {
    fmt.Println(h.Pop())  // 9, 8, 5, 3, 1
}
```

### PriorityQueue

```go
type Task struct {
    Name string
}

func main() {
    // Higher priority first
    pq := heap_utils.NewPriorityQueue[Task](true)
    
    pq.Push(Task{Name: "low"}, 1)
    pq.Push(Task{Name: "high"}, 10)
    pq.Push(Task{Name: "medium"}, 5)
    
    for !pq.IsEmpty() {
        item := pq.Pop()
        fmt.Printf("%s (priority %.0f)\n", item.Value.Name, item.Priority)
    }
    // Output: high (10), medium (5), low (1)
}
```

### Custom Comparator (GenericHeap)

```go
type Person struct {
    Name string
    Age  int
}

// Sort by age (youngest first)
h := heap_utils.NewGenericHeap(func(a, b Person) bool {
    return a.Age < b.Age
}, Person{"Alice", 30}, Person{"Bob", 25})

h.Pop()  // {Bob, 25}
```

### TopK / BottomK

```go
data := []int{3, 1, 4, 1, 5, 9, 2, 6, 5, 3}

// Find 3 largest
top3 := heap_utils.TopK(data, 3)  // [9, 6, 5]

// Find 3 smallest
bottom3 := heap_utils.BottomK(data, 3)  // [1, 1, 2]
```

### Merge K Sorted Arrays

```go
s1 := []int{1, 4, 7}
s2 := []int{2, 5, 8}
s3 := []int{3, 6, 9}

merged := heap_utils.MergeKSorted(s1, s2, s3)
// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Heap Sort

```go
data := []int{3, 1, 4, 1, 5, 9}

asc := heap_utils.HeapSort(data)      // [1, 1, 3, 4, 5, 9]
desc := heap_utils.HeapSortDesc(data) // [9, 5, 4, 3, 1, 1]
```

### Find Nth Element

```go
data := []int{3, 1, 4, 1, 5, 9, 2, 6}

// Find 3rd smallest
val, _ := heap_utils.NthSmallest(data, 3)  // 2

// Find 2nd largest
val, _ := heap_utils.NthLargest(data, 2)   // 6

// Find median
med, _ := heap_utils.Median(data)          // 3
```

## Examples

See the `examples/` directory for complete working examples:

- `basic/` - MinHeap and MaxHeap basics
- `priority_queue/` - Task scheduling with priorities
- `topk/` - Finding top/bottom K elements
- `merge/` - Merging sorted sequences
- `sort/` - Heap sort implementation
- `custom/` - Custom comparators
- `stream/` - Real-time data stream processing

## Running Tests

```bash
cd Go/heap_utils
go test -v
```

Run benchmarks:
```bash
go test -bench=.
```

## API Reference

### MinHeap[T Ordered]

| Method | Description |
|--------|-------------|
| `NewMinHeap[T](elements...)` | Create new min-heap |
| `Push(x T)` | Add element |
| `Pop() T` | Remove and return minimum |
| `Peek() (T, bool)` | View minimum without removing |
| `Len() int` | Get element count |
| `IsEmpty() bool` | Check if empty |
| `Clear()` | Remove all elements |
| `ToSlice() []T` | Copy all elements |
| `Values() []T` | Get all elements sorted (consumes heap) |

### MaxHeap[T Ordered]

Same methods as MinHeap, but returns maximum values first.

### PriorityQueue[T any]

| Method | Description |
|--------|-------------|
| `NewPriorityQueue[T](higher bool)` | Create queue (higher=true: max priority first) |
| `Push(value T, priority float64) *Item` | Add with priority |
| `Pop() *Item` | Remove and return top item |
| `Peek() *Item` | View top item |
| `Update(item *Item, priority float64)` | Change item priority |
| `Len() int` | Get count |
| `IsEmpty() bool` | Check if empty |
| `Clear()` | Remove all items |

### GenericHeap[T any]

| Method | Description |
|--------|-------------|
| `NewGenericHeap[T](less func(a,b T) bool, elements...)` | Create with custom comparator |
| `Push(x T)` | Add element |
| `Pop() T` | Remove and return top |
| `Peek() (T, bool)` | View top element |
| `Len() int` | Get count |
| `IsEmpty() bool` | Check if empty |
| `Clear()` | Remove all elements |

### Utility Functions

| Function | Description |
|----------|-------------|
| `TopK[T](data []T, k int) []T` | Find k largest elements |
| `BottomK[T](data []T, k int) []T` | Find k smallest elements |
| `MergeKSorted[T](slices ...[]T) []T` | Merge sorted slices |
| `HeapSort[T](data []T) []T` | Sort ascending |
| `HeapSortDesc[T](data []T) []T` | Sort descending |
| `NthSmallest[T](data []T, n int) (T, bool)` | Find nth smallest |
| `NthLargest[T](data []T, n int) (T, bool)` | Find nth largest |
| `Median[T](data []T) (T, bool)` | Find median |

## License

MIT License - Part of AllToolkit