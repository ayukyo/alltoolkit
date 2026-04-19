# Priority Queue Utils (Zig)

A high-performance, zero-dependency priority queue implementation using a binary heap in Zig.

## Features

- **Generic Implementation**: Works with any type via Zig's comptime generics
- **Min-Heap & Max-Heap**: Built-in comparators for both ordering strategies
- **Zero External Dependencies**: Pure Zig implementation using only the standard library
- **Memory Efficient**: Dynamic growth with customizable initial capacity
- **Type Safe**: Compile-time type checking for all operations

## Installation

### Using Zig Package Manager

Add to your `build.zig.zon`:

```zig
.dependencies = .{
    .priority_queue_utils = .{
        .url = "https://github.com/ayukyo/alltoolkit/archive/refs/heads/main.tar.gz",
        .hash = "...", // Run `zig build` to get the hash
    },
},
```

### Manual Installation

Copy the `src/priority_queue.zig` file to your project.

## Quick Start

```zig
const std = @import("std");
const PriorityQueue = @import("priority_queue").PriorityQueue;
const minCompare = @import("priority_queue").minCompare;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    
    // Create a min-heap
    var pq = PriorityQueue(i32).init(allocator, minCompare(i32));
    defer pq.deinit();
    
    // Insert elements
    try pq.insert(42);
    try pq.insert(10);
    try pq.insert(7);
    
    // Remove elements in priority order
    while (!pq.isEmpty()) {
        const item = pq.remove().?;
        std.debug.print("{}\n", .{item});
    }
    // Output: 7, 10, 42 (ascending order for min-heap)
}
```

## API Reference

### Initialization

```zig
// Basic initialization
var pq = PriorityQueue(T).init(allocator, compareFn);

// With pre-allocated capacity
var pq = try PriorityQueue(T).initCapacity(allocator, 100, compareFn);
```

### Core Methods

| Method | Description | Complexity |
|--------|-------------|------------|
| `insert(item)` | Add an element | O(log n) |
| `remove()` | Remove and return top element | O(log n) |
| `peek()` | View top element without removing | O(1) |
| `count()` | Get number of elements | O(1) |
| `isEmpty()` | Check if queue is empty | O(1) |
| `clear()` | Remove all elements | O(1) |
| `ensureCapacity(n)` | Pre-allocate memory | O(n) |
| `deinit()` | Free all memory | O(1) |

### Comparison Functions

```zig
// Min-heap: smaller values have higher priority
const minCmp = minCompare(i32);

// Max-heap: larger values have higher priority
const maxCmp = maxCompare(i32);

// Custom comparator
fn myCompare(a: MyType, b: MyType) std.math.Order {
    return std.math.order(a.priority, b.priority);
}
```

## Examples

### Task Scheduler

```zig
const Task = struct {
    priority: u32,
    name: []const u8,
    
    fn compare(a: Task, b: Task) std.math.Order {
        return std.math.order(a.priority, b.priority);
    }
};

var scheduler = PriorityQueue(Task).init(allocator, Task.compare);
defer scheduler.deinit();

try scheduler.insert(.{ .priority = 1, .name = "Urgent task" });
try scheduler.insert(.{ .priority = 5, .name = "Normal task" });
try scheduler.insert(.{ .priority = 10, .name = "Low priority" });

// Tasks are processed by priority (lowest number first)
while (!scheduler.isEmpty()) {
    const task = scheduler.remove().?;
    std.debug.print("{s}\n", .{task.name});
}
```

### Dijkstra's Algorithm

Priority queues are essential for efficient pathfinding algorithms:

```zig
const Node = struct {
    distance: u32,
    vertex: usize,
    
    fn compare(a: Node, b: Node) std.math.Order {
        return std.math.order(a.distance, b.distance);
    }
};

var pq = PriorityQueue(Node).init(allocator, Node.compare);
defer pq.deinit();

try pq.insert(.{ .distance = 0, .vertex = start });
```

## Performance

Binary heap operations have the following time complexities:

- **Insert**: O(log n)
- **Remove (extract min/max)**: O(log n)
- **Peek**: O(1)
- **Build heap from array**: O(n)

Memory grows dynamically with amortized O(1) cost per insertion.

## Running Tests

```bash
zig build test
```

## Running Examples

```bash
zig build example-basic      # Basic usage demo
zig build example-scheduler  # Task scheduler demo
zig build example-dijkstra   # Dijkstra's algorithm demo
```

## License

MIT License - Part of the AllToolkit project.