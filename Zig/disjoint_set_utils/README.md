# Disjoint Set (Union-Find) for Zig

A high-performance **Disjoint Set Union (Union-Find)** data structure implementation in Zig with zero external dependencies.

## Features

- **Path Compression**: Optimizes `find()` by flattening the tree structure
- **Union by Rank**: Keeps trees balanced for optimal performance
- **O(α(n))** amortized time complexity (inverse Ackermann function - effectively constant time)
- **Generic Implementation**: Works with any type via Zig's comptime generics
- **Memory Efficient**: Single allocation for all nodes
- **Comprehensive API**: Get set members, count sets, reset, and more

## Installation

Add to your `build.zig.zon`:

```zig
.dependencies = .{
    .disjoint_set = .{
        .path = "path/to/disjoint_set_utils",
    },
},
```

Or use directly in your project:

```zig
const DisjointSet = @import("disjoint_set").DisjointSet;
```

## Usage

### Basic Operations

```zig
const std = @import("std");
const DisjointSet = @import("disjoint_set").DisjointSet;

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    // Initialize with elements
    var ds = try DisjointSet(i32).init(allocator, &[_]i32{ 1, 2, 3, 4, 5 });
    defer ds.deinit();

    // Union operations
    _ = ds.unionSets(0, 1); // Union elements at index 0 and 1
    _ = ds.unionSets(2, 3);

    // Check connectivity
    const connected = ds.connected(0, 1); // true
    const not_connected = ds.connected(0, 2); // false

    // Find root of an element
    const root = ds.find(0);

    // Count sets
    const num_sets = ds.countSets();
}
```

### With Indices Only

```zig
const USizeDisjointSet = @import("disjoint_set").USizeDisjointSet;

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    // Create disjoint set with indices 0..n
    var ds = try USizeDisjointSet.initRange(allocator, 100);
    defer ds.deinit();

    // Use as normal
    _ = ds.unionSets(0, 50);
    _ = ds.unionSets(50, 99);

    // Now 0, 50, and 99 are in the same set
}
```

### Get Set Members

```zig
// Get all members of the set containing element at index 2
const members = try ds.getSetMembers(allocator, 2);
defer allocator.free(members);

for (members) |val| {
    std.debug.print("{} ", .{val});
}
```

### Get All Sets

```zig
const sets = try ds.getAllSets(allocator);
defer {
    for (sets) |set| {
        allocator.free(set);
    }
    allocator.free(sets);
}

for (sets, 1..) |set, i| {
    std.debug.print("Set {}: ", .{i});
    for (set) |val| {
        std.debug.print("{} ", .{val});
    }
    std.debug.print("\n", .{});
}
```

### Reset

```zig
// Reset all elements to individual sets
ds.reset();
```

## API Reference

### Construction

| Function | Description |
|----------|-------------|
| `init(allocator, elements)` | Initialize with slice of elements |
| `initRange(allocator, size)` | Initialize with indices 0..size |

### Core Operations

| Function | Description |
|----------|-------------|
| `find(index) usize` | Find root of element (with path compression) |
| `findConst(index) usize` | Find root without path compression |
| `unionSets(a, b) bool` | Union two sets, returns true if merged |
| `connected(a, b) bool` | Check if two elements are in same set |

### Information

| Function | Description |
|----------|-------------|
| `size() usize` | Get total number of elements |
| `countSets() usize` | Get number of distinct sets |
| `getSetSize(index) usize` | Get size of set containing element |
| `getValue(index) T` | Get value at index |
| `getSetMembers(allocator, index) []T` | Get all members of a set |
| `getAllSets(allocator) [][]T` | Get all sets |

### Modification

| Function | Description |
|----------|-------------|
| `reset()` | Reset all elements to individual sets |
| `deinit()` | Free allocated memory |

## Use Cases

1. **Graph Algorithms**: Detect cycles, find connected components
2. **Kruskal's MST**: Efficiently check if adding edge creates cycle
3. **Network Connectivity**: Track connected components in networks
4. **Image Processing**: Connected component labeling
5. **Dynamic Connectivity**: Maintain connectivity under edge insertions

## Performance

- **Time**: O(α(n)) per operation (amortized), where α is the inverse Ackermann function
- **Space**: O(n) for n elements
- **Path Compression**: Makes subsequent finds O(1) in practice
- **Union by Rank**: Keeps tree height logarithmic

## Testing

```bash
zig build test
```

## Examples

Build and run examples:

```bash
zig build run-basic
zig build run-network
zig build run-components
```

## License

MIT