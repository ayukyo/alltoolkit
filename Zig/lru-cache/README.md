# LRU Cache - Zig Implementation

A zero-dependency LRU (Least Recently Used) Cache implementation in Zig.

## Features

- **Generic**: Works with any key and value types
- **Memory efficient**: O(1) get and put operations
- **Automatic eviction**: Removes least recently used items when capacity is exceeded
- **Thread-safe considerations**: Designed for single-threaded use (wrap with mutex for multi-threaded)
- **Iterator support**: Iterate over entries in order from most to least recently used

## Building

```bash
# Run tests
zig build test

# Build the example
zig build

# Run the example
zig build run
```

## Quick Start

```zig
const std = @import("std");
const LruCache = @import("lru_cache.zig").LruCache;

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    
    // Create cache with capacity 3
    var cache = try LruCache(u32, []const u8).init(allocator, 3);
    defer cache.deinit();
    
    // Put values
    try cache.put(1, "Alice");
    try cache.put(2, "Bob");
    try cache.put(3, "Charlie");
    
    // Get values (returns null if not found)
    if (cache.get(1)) |value| {
        std.debug.print("Found: {s}\n", .{value});
    }
    
    // Check if key exists
    if (cache.contains(2)) {
        std.debug.print("Key 2 exists\n", .{});
    }
    
    // Add fourth item - evicts least recently used
    try cache.put(4, "David");
}
```

## API Reference

### Initialization

```zig
var cache = try LruCache(K, V).init(allocator, capacity);
defer cache.deinit();
```

Creates a new LRU cache with the specified capacity. `K` is the key type and `V` is the value type.

### Operations

| Method | Description | Return Type |
|--------|-------------|-------------|
| `put(key, value)` | Insert or update an entry | `!void` |
| `get(key)` | Get value by key, returns null if not found | `?V` |
| `contains(key)` | Check if key exists | `bool` |
| `remove(key)` | Remove an entry by key | `bool` (was removed) |
| `clear()` | Remove all entries | `void` |
| `getSize()` | Get current number of entries | `usize` |
| `getCapacity()` | Get maximum capacity | `usize` |

### Iterator

```zig
var iter = cache.iterator();
while (iter.next()) |entry| {
    std.debug.print("Key: {}, Value: {}\n", .{ entry.key, entry.value });
}
```

Iterates over entries from most to least recently used.

## How It Works

1. **Doubly Linked List**: Maintains order with most recently used at the head
2. **Hash Map**: Provides O(1) lookup to any node
3. **Eviction**: When capacity is exceeded, removes the tail (least recently used)

### Access Pattern

```
Initial state after puts: [1, 2, 3]  (1 = LRU, 3 = MRU)
After get(1): [2, 3, 1]               (1 becomes MRU)
After put(4): [2, 3, 4, evict 1]      (1 was evicted, 4 is MRU)
```

## Use Cases

- **Caching**: Store frequently accessed data
- **Memoization**: Cache function results
- **Resource Management**: Limit memory usage
- **Rate Limiting**: Track recent requests

## Complexity

| Operation | Time | Space |
|-----------|------|-------|
| `put` | O(1) | O(1) |
| `get` | O(1) | O(1) |
| `remove` | O(1) | O(1) |
| `contains` | O(1) | O(1) |
| Overall Space | - | O(capacity) |

## Example: Web Cache

```zig
const HttpResult = struct {
    status: u16,
    body: []const u8,
    timestamp: i64,
};

var http_cache = try LruCache([]const u8, HttpResult).init(allocator, 100);

// Cache HTTP responses
fn cachedFetch(url: []const u8) ?HttpResult {
    if (http_cache.get(url)) |result| {
        // Check if still valid
        const now = std.time.timestamp();
        if (now - result.timestamp < 3600) { // 1 hour TTL
            return result;
        }
        _ = http_cache.remove(url);
    }
    return null;
}
```

## License

MIT License