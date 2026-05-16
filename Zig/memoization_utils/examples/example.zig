const std = @import("std");
const memoization = @import("memoization");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Memoization Utils Example ===\n\n", .{});

    // Basic cache usage
    try basicExample(allocator);

    // TTL example
    try ttlExample(allocator);

    // LRU eviction example
    try lruExample(allocator);

    // Statistics example
    try statsExample(allocator);

    // Function memoization
    try memoizeExample(allocator);

    // Composite key example
    try compositeKeyExample(allocator);
}

fn basicExample(allocator: std.mem.Allocator) !void {
    std.debug.print("1. Basic Cache Operations\n", .{});
    std.debug.print("--------------------------\n", .{});

    var cache = memoization.MemoCache(i32, i32).init(allocator, .{});
    defer cache.deinit();

    // Set values
    try cache.set(1, 100);
    try cache.set(2, 200);
    try cache.set(3, 300);

    std.debug.print("  Set key 1 = 100\n", .{});
    std.debug.print("  Set key 2 = 200\n", .{});
    std.debug.print("  Set key 3 = 300\n", .{});

    // Get values
    if (cache.get(1)) |value| {
        std.debug.print("  Get key 1: {}\n", .{value});
    }
    if (cache.get(2)) |value| {
        std.debug.print("  Get key 2: {}\n", .{value});
    }

    // Check existence
    std.debug.print("  Contains key 1: {}\n", .{cache.contains(1)});
    std.debug.print("  Contains key 99: {}\n", .{cache.contains(99)});

    // Size
    std.debug.print("  Cache size: {}\n", .{cache.size()});

    // Remove
    const removed = cache.remove(2);
    std.debug.print("  Removed key 2: {}\n", .{removed});
    std.debug.print("  Cache size after remove: {}\n", .{cache.size()});

    std.debug.print("\n", .{});
}

fn ttlExample(allocator: std.mem.Allocator) !void {
    std.debug.print("2. TTL (Time-To-Live) Example\n", .{});
    std.debug.print("------------------------------\n", .{});

    var cache = memoization.MemoCache(i32, i32).init(allocator, .{});
    defer cache.deinit();

    // Set with TTL of 500ms
    try cache.setWithTtl(1, 100, 500);
    std.debug.print("  Set key 1 = 100 with TTL 500ms\n", .{});

    if (cache.getEntry(1)) |entry| {
        std.debug.print("  Value: {}, Remaining TTL: {}ms\n", .{ entry.value, entry.remainingTtl().? });
    }

    std.debug.print("  Sleeping 200ms...\n", .{});
    std.time.sleep(200 * std.time.ns_per_ms);

    if (cache.get(1)) |value| {
        std.debug.print("  After 200ms, key 1 still exists: {}\n", .{value});
    }

    std.debug.print("  Sleeping another 400ms (total 600ms)...\n", .{});
    std.time.sleep(400 * std.time.ns_per_ms);

    if (cache.get(1)) |value| {
        std.debug.print("  Key 1 still exists: {}\n", .{value});
    } else {
        std.debug.print("  Key 1 has expired and been removed\n", .{});
    }

    std.debug.print("\n", .{});
}

fn lruExample(allocator: std.mem.Allocator) !void {
    std.debug.print("3. LRU Eviction Example\n", .{});
    std.debug.print("-----------------------\n", .{});

    // Create cache with max size of 3
    var cache = memoization.MemoCache(i32, i32).init(allocator, .{ .max_size = 3 });
    defer cache.deinit();

    std.debug.print("  Created cache with max_size = 3\n", .{});

    // Fill cache
    try cache.set(1, 100);
    try cache.set(2, 200);
    try cache.set(3, 300);
    std.debug.print("  Added keys: 1, 2, 3\n", .{});
    std.debug.print("  Cache size: {}\n", .{cache.size()});

    // Access key 1 to make it recently used
    _ = cache.get(1);
    std.debug.print("  Accessed key 1 (now most recently used)\n", .{});

    // Add fourth item - should evict key 2 (least recently used)
    try cache.set(4, 400);
    std.debug.print("  Added key 4, triggering LRU eviction\n", .{});

    std.debug.print("  Key 1 exists: {} (was accessed recently)\n", .{cache.contains(1)});
    std.debug.print("  Key 2 exists: {} (should be evicted - LRU)\n", .{cache.contains(2)});
    std.debug.print("  Key 3 exists: {}\n", .{cache.contains(3)});
    std.debug.print("  Key 4 exists: {}\n", .{cache.contains(4)});

    std.debug.print("  Evictions: {}\n", .{cache.getStats().evictions});

    std.debug.print("\n", .{});
}

fn statsExample(allocator: std.mem.Allocator) !void {
    std.debug.print("4. Statistics Example\n", .{});
    std.debug.print("---------------------\n", .{});

    var cache = memoization.MemoCache(i32, i32).init(allocator, .{ .enable_stats = true });
    defer cache.deinit();

    // Generate some activity
    _ = cache.get(1); // Miss
    try cache.set(1, 100); // Set
    _ = cache.get(1); // Hit
    _ = cache.get(1); // Hit
    _ = cache.get(2); // Miss
    try cache.set(2, 200); // Set
    _ = cache.get(2); // Hit
    _ = cache.remove(1); // Delete

    const stats = cache.getStats();
    std.debug.print("  Hits: {}\n", .{stats.hits});
    std.debug.print("  Misses: {}\n", .{stats.misses});
    std.debug.print("  Sets: {}\n", .{stats.sets});
    std.debug.print("  Deletes: {}\n", .{stats.deletes});
    std.debug.print("  Hit ratio: {d:.2}\n", .{stats.hitRatio()});

    // Reset stats
    cache.resetStats();
    std.debug.print("  After reset - Hits: {}, Misses: {}\n", .{ cache.getStats().hits, cache.getStats().misses });

    std.debug.print("\n", .{});
}

fn memoizeExample(allocator: std.mem.Allocator) !void {
    std.debug.print("5. Function Memoization Example\n", .{});
    std.debug.print("--------------------------------\n", .{});

    var cache = memoization.MemoCache(i32, i64).init(allocator, .{});
    defer cache.deinit();

    var compute_count: u32 = 0;

    // Simulate expensive computation
    const expensiveCompute = struct {
        var count: *u32 = undefined;
        fn run(n: i32) i64 {
            count.* += 1;
            var result: i64 = 1;
            var i: i32 = 1;
            while (i <= n) : (i += 1) {
                result *= i;
            }
            return result;
        }
    };
    expensiveCompute.count = &compute_count;

    // First call - should compute
    const result1 = try cache.memoizeError(5, struct {
        fn call() anyerror!i64 {
            return expensiveCompute.run(5);
        }
    }.call);
    std.debug.print("  First call memoize(5): {} (computed)\n", .{result1});

    // Second call - should use cache
    const result2 = try cache.memoizeError(5, struct {
        fn call() anyerror!i64 {
            return expensiveCompute.run(5);
        }
    }.call);
    std.debug.print("  Second call memoize(5): {} (cached)\n", .{result2});

    std.debug.print("  Compute count: {} (should be 1)\n", .{compute_count});
    std.debug.print("  Cache hits: {}\n", .{cache.getStats().hits});
    std.debug.print("  Cache misses: {}\n", .{cache.getStats().misses});

    std.debug.print("\n", .{});
}

fn compositeKeyExample(allocator: std.mem.Allocator) !void {
    std.debug.print("6. Composite Key Example\n", .{});
    std.debug.print("-------------------------\n", .{});

    // Use a composite key for complex lookup scenarios
    const Key = struct {
        category: i32,
        id: i32,
    };

    var cache = memoization.MemoCache(Key, i64).init(allocator, .{ .max_size = 5 });
    defer cache.deinit();

    // Store results by composite keys
    try cache.set(.{ .category = 1, .id = 10 }, 55);
    try cache.set(.{ .category = 1, .id = 20 }, 6765);
    try cache.set(.{ .category = 2, .id = 5 }, 120);
    try cache.set(.{ .category = 2, .id = 10 }, 3628800);

    std.debug.print("  Stored computed results:\n", .{});
    if (cache.get(.{ .category = 1, .id = 10 })) |v| {
        std.debug.print("    fibonacci(10) = {}\n", .{v});
    }
    if (cache.get(.{ .category = 1, .id = 20 })) |v| {
        std.debug.print("    fibonacci(20) = {}\n", .{v});
    }
    if (cache.get(.{ .category = 2, .id = 5 })) |v| {
        std.debug.print("    factorial(5) = {}\n", .{v});
    }
    if (cache.get(.{ .category = 2, .id = 10 })) |v| {
        std.debug.print("    factorial(10) = {}\n", .{v});
    }

    std.debug.print("  Cache size: {}\n", .{cache.size()});

    std.debug.print("\n", .{});
}