# Go Stack Utils 📚

A comprehensive Go package providing generic stack implementations and algorithms with zero external dependencies.

## Features

- **Generic Stack** - LIFO (Last In, First Out) data structure with generics support (Go 1.18+)
- **Bounded Stack** - Stack with fixed maximum capacity
- **Min Stack** - Stack that supports O(1) minimum queries
- **Max Stack** - Stack that supports O(1) maximum queries
- **Stack Algorithms** - Common algorithms using stack data structure

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/stack_utils
```

## Quick Start

```go
package main

import (
    "fmt"
    stack_utils "github.com/ayukyo/alltoolkit/Go/stack_utils"
)

func main() {
    // Create a new stack
    s := stack_utils.NewStack[int]()
    
    // Push items
    s.Push(1)
    s.Push(2)
    s.Push(3)
    
    // Peek top item
    top, _ := s.Peek()
    fmt.Println("Top:", top) // Top: 3
    
    // Pop items
    item, _ := s.Pop()
    fmt.Println("Popped:", item) // Popped: 3
    
    // Check size
    fmt.Println("Size:", s.Size()) // Size: 2
}
```

## Stack Types

### Basic Stack

```go
// Create an empty stack
s := stack_utils.NewStack[int]()

// Create a stack with pre-allocated capacity
s := stack_utils.NewStackWithCapacity[int](100)

// Create a stack from a slice
s := stack_utils.FromSlice([]int{1, 2, 3, 4, 5})
```

**Methods:**
- `Push(item T)` - Add item to top
- `Pop() (T, error)` - Remove and return top item
- `Peek() (T, error)` - Return top item without removing
- `IsEmpty() bool` - Check if stack is empty
- `Size() int` - Get number of items
- `Clear()` - Remove all items
- `ToSlice() []T` - Get all items as slice (bottom to top)
- `String() string` - String representation

### Bounded Stack

```go
// Create a stack with maximum capacity of 10
s := stack_utils.NewBoundedStack[int](10)

s.Push(1)  // OK
s.Push(2)  // OK
// ...
err := s.Push(11) // Returns ErrStackFull if capacity exceeded

// Check if full
if s.IsFull() {
    fmt.Println("Stack is at capacity")
}

// Get capacity
fmt.Println("Capacity:", s.Capacity())
```

**Additional Methods:**
- `IsFull() bool` - Check if stack is at capacity
- `Capacity() int` - Get maximum capacity

### Min Stack (O(1) Minimum)

```go
s := stack_utils.NewMinStack[int]()

s.Push(5)
s.Push(3)
s.Push(7)
s.Push(2)

min, _ := s.Min()
fmt.Println("Minimum:", min) // Minimum: 2

s.Pop() // Removes 2
min, _ = s.Min()
fmt.Println("Minimum:", min) // Minimum: 3
```

### Max Stack (O(1) Maximum)

```go
s := stack_utils.NewMaxStack[int]()

s.Push(2)
s.Push(7)
s.Push(3)
s.Push(5)

max, _ := s.Max()
fmt.Println("Maximum:", max) // Maximum: 7

s.Pop() // Removes 5
max, _ = s.Max()
fmt.Println("Maximum:", max) // Maximum: 7
```

## Algorithms

### Parentheses Balancing

```go
// Check if parentheses are balanced
stack_utils.IsBalancedParentheses("()[]{}")      // true
stack_utils.IsBalancedParentheses("([{}])")     // true
stack_utils.IsBalancedParentheses("([)]")       // false
stack_utils.IsBalancedParentheses("(((")        // false

// Check if quotes are balanced
stack_utils.IsBalancedQuotes(`"hello"`)         // true
stack_utils.IsBalancedQuotes(`"hello`)          // false
```

### Expression Evaluation

```go
// Evaluate postfix (RPN) expression
result, _ := stack_utils.EvaluatePostfix("3 4 + 2 *")
fmt.Println(result) // 14

// Evaluate with array of tokens
result, _ := stack_utils.EvaluateRPN([]string{"2", "1", "+", "3", "*"})
fmt.Println(result) // 9

// Convert infix to postfix
postfix := stack_utils.InfixToPostfix("A+B*C")
fmt.Println(postfix) // "A B C * +"
```

### String Operations

```go
// Reverse a string
reversed := stack_utils.ReverseString("hello")
fmt.Println(reversed) // "olleh"

// Remove adjacent duplicates
result := stack_utils.RemoveAdjacentDuplicates("deeedbbcccbdaa", 3)
fmt.Println(result) // "aa"
```

### Array Algorithms

```go
// Next Greater Element (-1 means no greater element)
arr := []int{4, 5, 2, 25}
result := stack_utils.NextGreaterElement(arr)
// result: [5, 25, 25, -1]

// Previous Smaller Element (-1 means no smaller element)
arr := []int{1, 3, 0, 2, 5}
result := stack_utils.PreviousSmallerElement(arr)
// result: [-1, 1, -1, 0, 2]

// Daily Temperatures (days until warmer)
temps := []int{73, 74, 75, 71, 69, 72, 76, 73}
result := stack_utils.DailyTemperatures(temps)
// result: [1, 1, 4, 2, 1, 1, 0, 0]

// Largest Rectangle in Histogram
heights := []int{2, 1, 5, 6, 2, 3}
area := stack_utils.LargestRectangleInHistogram(heights)
// area: 10
```

### HTML Validation

```go
// Check if HTML tags are properly nested
stack_utils.IsValidHTML("<div></div>")                    // true
stack_utils.IsValidHTML("<div><p></p></div>")             // true
stack_utils.IsValidHTML("<div class='test'>content</div>") // true
stack_utils.IsValidHTML("<div><p></div></p>")             // false
stack_utils.IsValidHTML("<div>")                          // false
```

## Error Handling

```go
s := stack_utils.NewStack[int]()

// Pop from empty stack
_, err := s.Pop()
if err == stack_utils.ErrStackEmpty {
    fmt.Println("Stack is empty!")
}

// Bounded stack overflow
bs := stack_utils.NewBoundedStack[int](2)
bs.Push(1)
bs.Push(2)
err := bs.Push(3)
if err == stack_utils.ErrStackFull {
    fmt.Println("Stack is full!")
}
```

## Performance

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Push      | O(1) amortized | O(1)             |
| Pop       | O(1)           | O(1)             |
| Peek      | O(1)           | O(1)             |
| Min/Max   | O(1)           | O(n) extra       |
| IsEmpty   | O(1)           | O(1)             |

## Test Coverage

- **30+ test cases** covering:
  - Basic stack operations (push, pop, peek, clear)
  - Bounded stack capacity limits
  - MinStack minimum tracking
  - MaxStack maximum tracking
  - Parentheses and quote balancing
  - Expression evaluation (postfix, RPN)
  - String reversal
  - Next/previous element algorithms
  - HTML validation
  - Histogram algorithms
  - Edge cases and error handling
  - Benchmarks for performance

## License

MIT License - See [LICENSE](../../LICENSE) for details.

## Contributing

Contributions are welcome! Please read the [contributing guidelines](../../docs/contributing.md) first.