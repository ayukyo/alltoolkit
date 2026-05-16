# Deque Utils - Double-Ended Queue for Go

A comprehensive Go library implementing a generic double-ended queue (deque) with efficient operations for insertion and removal at both ends.

## Features

### Core Operations
- **PushFront** - Add element to the front
- **PushBack** - Add element to the back
- **PopFront** - Remove and return front element
- **PopBack** - Remove and return back element
- **Front/Back** - Peek at front/back without removal

### Collection Properties
- **Len** - Get number of elements
- **IsEmpty** - Check if deque is empty
- **Clear** - Remove all elements
- **Cap** - Get current capacity

### Random Access
- **Get** - Get element at index
- **Set** - Set element at index

### Bulk Operations
- **PushFrontAll** - Add multiple elements to front
- **PushBackAll** - Add multiple elements to back
- **PopFrontN** - Pop n elements from front
- **PopBackN** - Pop n elements from back

### Search Operations
- **Contains** - Check if element exists
- **IndexOf/LastIndexOf** - Find element indices
- **Find/FindAll** - Find elements by predicate
- **Count** - Count elements matching predicate

### Modification Operations
- **InsertAt** - Insert element at index
- **RemoveAt** - Remove element at index
- **Remove/RemoveAll** - Remove by predicate

### Transformation Operations
- **Map** - Apply function to all elements
- **Filter** - Filter elements by predicate
- **Reduce** - Reduce to single value
- **ForEach** - Apply action to all elements
- **Reverse/Reversed** - Reverse order
- **RotateLeft/RotateRight** - Rotate elements

### Slice Operations
- **ToSlice** - Convert to slice
- **SubDeque** - Get sub-deque
- **Take/TakeLast/Skip** - Take or skip elements

### Utility Functions
- **Clone** - Create copy
- **Append/Prepend** - Combine deques
- **Swap** - Swap elements
- **Min/Max** - Find min/max element
- **All/Any** - Check all/any match predicate
- **First/Last** - Find first/last matching element
- **Iterator/ReverseIterator** - Iterate over elements

## Installation

```go
import deque "deque_utils"
```

## Usage Examples

### Basic Usage

```go
// Create a new deque
d := deque.NewDeque[int]()

// Add elements
d.PushBack(1)
d.PushBack(2)
d.PushFront(0)  // deque: [0, 1, 2]

// Remove elements
front, _ := d.PopFront()  // returns 0
back, _ := d.PopBack()    // returns 2

// Peek without removing
first, _ := d.Front()  // returns 1
last, _ := d.Back()    // returns 1
```

### From Slice

```go
slice := []int{1, 2, 3, 4, 5}
d := deque.NewDequeFromSlice(slice)
```

### Search Operations

```go
d := deque.NewDequeFromSlice([]int{1, 2, 3, 4, 5})

// Find by predicate
val, err := d.Find(func(x int) bool { return x > 3 })
// val = 4

// Find all matching elements
evens := d.FindAll(func(x int) bool { return x % 2 == 0 })
// evens = [2, 4]

// Check if exists
equals := func(a, b int) bool { return a == b }
exists := d.Contains(3, equals)  // true
```

### Transformation

```go
d := deque.NewDequeFromSlice([]int{1, 2, 3, 4, 5})

// Map: double all values
doubled := deque.Map(d, func(x int) int { return x * 2 })
// doubled = [2, 4, 6, 8, 10]

// Filter: keep even numbers
evens := d.Filter(func(x int) bool { return x % 2 == 0 })
// evens = [2, 4]

// Reduce: sum all values
sum := deque.Reduce(d, 0, func(acc, x int) int { return acc + x })
// sum = 15
```

### Rotation

```go
d := deque.NewDequeFromSlice([]int{1, 2, 3, 4, 5})

d.RotateLeft(2)   // [3, 4, 5, 1, 2]
d.RotateRight(1)  // [5, 1, 2, 3, 4]
```

### String Deque

```go
d := deque.NewDeque[string]()
d.PushBack("hello")
d.PushBack("world")

fmt.Println(d.String())  // Deque[hello, world]
```

### Custom Type

```go
type Person struct {
    Name string
    Age  int
}

d := deque.NewDeque[Person]()
d.PushBack(Person{"Alice", 30})
d.PushBack(Person{"Bob", 25})

// Find person by age
person, _ := d.Find(func(p Person) bool { return p.Age == 25 })
// person = {Name: "Bob", Age: 25}
```

### Iterator

```go
d := deque.NewDequeFromSlice([]int{1, 2, 3, 4, 5})

// Iterate from front to back
for val := range d.Iterator() {
    fmt.Println(val)
}

// Iterate from back to front
for val := range d.ReverseIterator() {
    fmt.Println(val)
}
```

## Applications

- **Sliding Window Algorithms** - Efficient window operations
- **BFS/Graph Algorithms** - Level-order traversal
- **Palindrome Checking** - Compare from both ends
- **Expression Evaluation** - Stack/queue hybrid operations
- **Task Scheduling** - Priority-based scheduling
- **Undo/Redo** - History management

## Time Complexity

| Operation | Time | Notes |
|-----------|------|-------|
| PushFront | O(n) | Due to slice prepend |
| PushBack | O(1)* | Amortized |
| PopFront | O(n) | Due to slice shift |
| PopBack | O(1) | Direct removal |
| Front/Back | O(1) | Direct access |
| Get/Set | O(1) | Index access |
| Len/IsEmpty | O(1) | Direct property |

Note: The slice-based implementation has O(n) cost for front operations.
For high-performance scenarios with many front operations, consider
a ring buffer or linked list implementation.

## Test Coverage

60+ unit tests covering:
- Basic operations
- Edge cases (empty, single element)
- Large scale operations (10000+ elements)
- Custom types (structs, strings)
- All search and transformation functions
- Iterator behavior

Run tests:
```bash
go test -v
```

Run benchmarks:
```bash
go test -bench=.
```

## License

MIT License