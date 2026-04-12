# Data Structures (Zig)

A comprehensive generic data structures library for Zig, providing implementations of common container types with zero external dependencies.

## Features

- **Stack**: LIFO (Last In, First Out) stack with dynamic resizing
- **Queue**: FIFO (First In, First Out) queue using ring buffer
- **LinkedList**: Doubly-linked list with bidirectional iteration
- **Deque**: Double-ended queue with efficient front/back operations
- **PriorityQueue**: Binary heap implementation (min-heap or max-heap)
- **HashSet**: Hash set using Zig's built-in AutoHashMap

## Design Principles

- **Zero external dependencies**: Uses only Zig's standard library
- **Generic**: All structures are generic over element type `T`
- **Allocator-aware**: All memory managed through explicit allocator
- **Ownership-transparent**: Caller owns all memory, must call `deinit()`
- **Error-explicit**: Uses Zig's error sets for allocation failures

## Installation

Add to your `build.zig.zon`:

```zig
dependencies = .{
    .data_structures = .{
        .path = "path/to/data-structures",
    },
},
```

Then in your `build.zig`:

```zig
const ds = b.dependency("data-structures", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.addImport("data-structures", ds.module("data-structures"));
```

## Usage

### Stack (LIFO)

```zig
const std = @import("std");
const ds = @import("data-structures");

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    
    var stack = ds.Stack(i32).init(allocator);
    defer stack.deinit();
    
    try stack.push(10);
    try stack.push(20);
    try stack.push(30);
    
    std.debug.print("Top: {}\n", .{stack.peek()});
    std.debug.print("Pop: {}\n", .{stack.pop()});
    std.debug.print("Pop: {}\n", .{stack.pop()});
}
```

### Queue (FIFO)

```zig
var queue = ds.Queue(i32).init(allocator);
defer queue.deinit();

try queue.enqueue(1);
try queue.enqueue(2);
try queue.enqueue(3);

std.debug.print("Dequeue: {}\n", .{queue.dequeue()}); // 1
std.debug.print("Dequeue: {}\n", .{queue.dequeue()}); // 2
```

### LinkedList

```zig
var list = ds.LinkedList(i32).init(allocator);
defer list.deinit();

try list.pushBack(2);
try list.pushFront(1);
try list.pushBack(3);

// Iteration
var iter = list.iterator();
while (iter.next()) |item| {
    std.debug.print("{} ", .{item});
}
// Output: 1 2 3

// Remove by value
list.remove(2);

// Find index
const idx = list.indexOf(3); // returns 1
```

### Deque (Double-ended Queue)

```zig
var deque = ds.Deque(i32).init(allocator);
defer deque.deinit();

try deque.pushFront(1);
try deque.pushBack(3);
try deque.pushFront(0);

// Random access
std.debug.print("Index 1: {}\n", .{deque.get(1)}); // 1

// Pop from either end
std.debug.print("Front: {}\n", .{deque.popFront()});
std.debug.print("Back: {}\n", .{deque.popBack()});
```

### PriorityQueue

```zig
// Min-heap (smallest element at top)
var min_heap = ds.PriorityQueue(i32, true).init(allocator);
defer min_heap.deinit();

try min_heap.insert(50);
try min_heap.insert(10);
try min_heap.insert(30);

std.debug.print("Min: {}\n", .{min_heap.pop()}); // 10

// Max-heap (largest element at top)
var max_heap = ds.PriorityQueue(i32, false).init(allocator);
defer max_heap.deinit();

try max_heap.insert(50);
try max_heap.insert(10);
try max_heap.insert(30);

std.debug.print("Max: {}\n", .{max_heap.pop()}); // 50
```

### HashSet

```zig
var set = ds.HashSet(i32).init(allocator);
defer set.deinit();

const newly_inserted = try set.insert(1); // true
const already_exists = try set.insert(1); // false

std.debug.print("Contains 1: {}\n", .{set.contains(1)});
std.debug.print("Remove 1: {}\n", .{set.remove(1)});
```

## API Reference

### Stack(T)

| Method | Description | Return |
|--------|-------------|--------|
| `init(allocator)` | Create empty stack | `Self` |
| `initWithCapacity(allocator, cap)` | Create with capacity | `Allocator.Error!Self` |
| `deinit()` | Free memory | `void` |
| `push(item)` | Push to top | `Allocator.Error!void` |
| `pop()` | Pop from top | `?T` |
| `peek()` | View top | `?T` |
| `len()` | Get size | `usize` |
| `isEmpty()` | Check empty | `bool` |
| `clear()` | Remove all | `void` |

### Queue(T)

| Method | Description | Return |
|--------|-------------|--------|
| `init(allocator)` | Create empty queue | `Self` |
| `initWithCapacity(allocator, cap)` | Create with capacity | `Allocator.Error!Self` |
| `deinit()` | Free memory | `void` |
| `enqueue(item)` | Add to back | `Allocator.Error!void` |
| `dequeue()` | Remove from front | `?T` |
| `peek()` | View front | `?T` |
| `len()` | Get size | `usize` |
| `isEmpty()` | Check empty | `bool` |
| `clear()` | Remove all | `void` |

### LinkedList(T)

| Method | Description | Return |
|--------|-------------|--------|
| `init(allocator)` | Create empty list | `Self` |
| `deinit()` | Free memory | `void` |
| `pushFront(item)` | Add to front | `Allocator.Error!void` |
| `pushBack(item)` | Add to back | `Allocator.Error!void` |
| `popFront()` | Remove from front | `?T` |
| `popBack()` | Remove from back | `?T` |
| `peekFront()` | View front | `?T` |
| `peekBack()` | View back | `?T` |
| `iterator()` | Get forward iterator | `Iterator` |
| `indexOf(item)` | Find index | `?usize` |
| `remove(item)` | Remove by value | `bool` |
| `len()` | Get size | `usize` |
| `isEmpty()` | Check empty | `bool` |

### Deque(T)

| Method | Description | Return |
|--------|-------------|--------|
| `init(allocator)` | Create empty deque | `Self` |
| `initWithCapacity(allocator, cap)` | Create with capacity | `Allocator.Error!Self` |
| `deinit()` | Free memory | `void` |
| `pushFront(item)` | Add to front | `Allocator.Error!void` |
| `pushBack(item)` | Add to back | `Allocator.Error!void` |
| `popFront()` | Remove from front | `?T` |
| `popBack()` | Remove from back | `?T` |
| `peekFront()` | View front | `?T` |
| `peekBack()` | View back | `?T` |
| `get(index)` | Random access | `?T` |
| `len()` | Get size | `usize` |
| `isEmpty()` | Check empty | `bool` |
| `clear()` | Remove all | `void` |

### PriorityQueue(T, is_min_heap)

| Method | Description | Return |
|--------|-------------|--------|
| `init(allocator)` | Create empty | `Self` |
| `initWithCapacity(allocator, cap)` | Create with capacity | `Allocator.Error!Self` |
| `deinit()` | Free memory | `void` |
| `insert(item)` | Add item | `Allocator.Error!void` |
| `pop()` | Remove top | `?T` |
| `peek()` | View top | `?T` |
| `len()` | Get size | `usize` |
| `isEmpty()` | Check empty | `bool` |
| `clear()` | Remove all | `void` |

### HashSet(T)

| Method | Description | Return |
|--------|-------------|--------|
| `init(allocator)` | Create empty set | `Self` |
| `deinit()` | Free memory | `void` |
| `insert(item)` | Add item | `Allocator.Error!bool` |
| `remove(item)` | Remove item | `bool` |
| `contains(item)` | Check existence | `bool` |
| `iterator()` | Get iterator | `Iterator` |
| `len()` | Get size | `usize` |
| `isEmpty()` | Check empty | `bool` |
| `clear()` | Remove all | `void` |

## Performance Characteristics

| Structure | Push | Pop | Peek | Access | Memory |
|-----------|------|-----|------|--------|--------|
| Stack | O(1)* | O(1) | O(1) | N/A | O(n) |
| Queue | O(1)* | O(1) | O(1) | N/A | O(n) |
| LinkedList | O(1) | O(1) | O(1) | O(n) | O(n) + pointers |
| Deque | O(1)* | O(1) | O(1) | O(1) | O(n) |
| PriorityQueue | O(log n) | O(log n) | O(1) | N/A | O(n) |
| HashSet | O(1)* | O(1) | O(1) | N/A | O(n) |

*Amortized - may trigger resize

## Building

```bash
# Build library
zig build

# Run tests
zig build test

# Run examples
zig build run-basic
zig build run-advanced
```

## Test Coverage

- Basic operations for all structures
- Large-scale operations (1000+ items)
- Edge cases (empty structures, single item)
- Memory management (init/deinit cycles)
- Ring buffer wraparound (Queue, Deque)
- Heap property verification (PriorityQueue)
- Iterator correctness

## Notes

- All structures require the caller to provide an allocator
- The caller must call `deinit()` to free memory
- Generic types work with any Zig type (primitives, structs, pointers)
- For types requiring custom equality, use `std.meta.eql` (default)

## License

MIT License - Part of the AllToolkit project.