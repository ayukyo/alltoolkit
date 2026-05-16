const std = @import("std");
const memoization = @import("memoization");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Memoization Utils Benchmark ===\n\n", .{});

    try benchmarkBasicOps(allocator);
    try benchmarkLruEviction(allocator);
    try benchmarkTtlCheck(allocator);
    try benchmarkMemoization(allocator);
}

fn benchmarkBasicOps(allocator: std.mem.Allocator) !void {
    std.debug.print("1. Basic Operations Benchmark\n", .{});
    std.debug.print("------------------------------\n", .{});

    var cache = memoization.MemoCache(i32, i64).init(allocator, .{});
    defer cache.deinit();

    const iterations = 100000;

    // Benchmark set
    const set_start = std.time.nanoTimestamp();
    for (0..iterations) |i| {
        try cache.set(@intCast(i), @intCast(i * i));
    }
    const set_end = std.time.nanoTimestamp();
    const set_time_ns = @as(u64, @intCast(set_end - set_start));
    const set_time_us = @as(f64, @floatFromInt(set_time_ns)) / 1000.0;
    std.debug.print("  Set {} items: {d:.2} us ({d:.0} ns/op)\n", .{ iterations, set_time_us, set_time_ns / iterations });

    // Benchmark get (hit)
    const get_start = std.time.nanoTimestamp();
    for (0..iterations) |i| {
        _ = cache.get(@intCast(i));
    }
    const get_end = std.time.nanoTimestamp();
    const get_time_ns = @as(u64, @intCast(get_end - get_start));
    const get_time_us = @as(f64, @floatFromInt(get_time_ns)) / 1000.0;
    std.debug.print("  Get {} items (hit): {d:.2} us ({d:.0} ns/op)\n", .{ iterations, get_time_us, get_time_ns / iterations });

    // Benchmark contains
    const contains_start = std.time.nanoTimestamp();
    for (0..iterations) |i| {
        _ = cache.contains(@intCast(i));
    }
    const contains_end = std.time.nanoTimestamp();
    const contains_time_ns = @as(u64, @intCast(contains_end - contains_start));
    const contains_time_us = @as(f64, @floatFromInt(contains_time_ns)) / 1000.0;
    std.debug.print("  Contains {} items: {d:.2} us ({d:.0} ns/op)\n", .{ iterations, contains_time_us, contains_time_ns / iterations });

    // Benchmark remove
    const remove_start = std.time.nanoTimestamp();
    for (0..iterations) |i| {
        _ = cache.remove(@intCast(i));
    }
    const remove_end = std.time.nanoTimestamp();
    const remove_time_ns = @as(u64, @intCast(remove_end - remove_start));
    const remove_time_us = @as(f64, @floatFromInt(remove_time_ns)) / 1000.0;
    std.debug.print("  Remove {} items: {d:.2} us ({d:.0} ns/op)\n", .{ iterations, remove_time_us, remove_time_ns / iterations });

    std.debug.print("\n", .{});
}

fn benchmarkLruEviction(allocator: std.mem.Allocator) !void {
    std.debug.print("2. LRU Eviction Benchmark\n", .{});
    std.debug.print("-------------------------\n", .{});

    var cache = memoization.MemoCache(i32, i64).init(allocator, .{ .max_size = 1000 });
    defer cache.deinit();

    const iterations = 100000;

    const start = std.time.nanoTimestamp();
    for (0..iterations) |i| {
        try cache.set(@intCast(i), @intCast(i));
    }
    const end = std.time.nanoTimestamp();

    const time_ns = @as(u64, @intCast(end - start));
    const time_ms = @as(f64, @floatFromInt(time_ns)) / 1_000_000.0;

    std.debug.print("  Inserted {} items with LRU eviction: {d:.2} ms\n", .{ iterations, time_ms });
    std.debug.print("  Evictions: {}\n", .{cache.getStats().evictions});
    std.debug.print("  Final cache size: {}\n", .{cache.size()});

    std.debug.print("\n", .{});
}

fn benchmarkTtlCheck(allocator: std.mem.Allocator) !void {
    std.debug.print("3. TTL Check Benchmark\n", .{});
    std.debug.print("----------------------\n", .{});

    var cache = memoization.MemoCache(i32, i64).init(allocator, .{ .default_ttl_ms = 60000 });
    defer cache.deinit();

    const iterations = 50000;

    // Set items with TTL
    for (0..iterations) |i| {
        try cache.set(@intCast(i), @intCast(i));
    }

    // Benchmark get with TTL check
    const start = std.time.nanoTimestamp();
    for (0..iterations) |i| {
        _ = cache.get(@intCast(i));
    }
    const end = std.time.nanoTimestamp();

    const time_ns = @as(u64, @intCast(end - start));
    const time_us = @as(f64, @floatFromInt(time_ns)) / 1000.0;

    std.debug.print("  Get {} items with TTL check: {d:.2} us ({d:.0} ns/op)\n", .{ iterations, time_us, time_ns / iterations });

    std.debug.print("\n", .{});
}

fn benchmarkMemoization(allocator: std.mem.Allocator) !void {
    std.debug.print("4. Function Memoization Benchmark\n", .{});
    std.debug.print("----------------------------------\n", .{});

    var cache = memoization.MemoCache(i32, i64).init(allocator, .{});
    defer cache.deinit();

    const iterations = 10000;
    const unique_keys = 100;

    // Without memoization
    const no_memo_start = std.time.nanoTimestamp();
    for (0..iterations) |_| {
        for (0..unique_keys) |k| {
            // Simulate expensive computation
            var result: i64 = 0;
            var i: i32 = 0;
            while (i < @as(i32, @intCast(k)) * 100) : (i += 1) {
                result +%= i;
            }
        }
    }
    const no_memo_end = std.time.nanoTimestamp();
    const no_memo_ns = @as(u64, @intCast(no_memo_end - no_memo_start));
    const no_memo_ms = @as(f64, @floatFromInt(no_memo_ns)) / 1_000_000.0;

    // With memoization - first populate cache
    for (0..unique_keys) |k| {
        var result: i64 = 0;
        var i: i32 = 0;
        while (i < @as(i32, @intCast(k)) * 100) : (i += 1) {
            result +%= i;
        }
        try cache.set(@intCast(k), result);
    }

    const memo_start = std.time.nanoTimestamp();
    for (0..iterations) |_| {
        for (0..unique_keys) |k| {
            _ = cache.get(@intCast(k));
        }
    }
    const memo_end = std.time.nanoTimestamp();
    const memo_ns = @as(u64, @intCast(memo_end - memo_start));
    const memo_ms = @as(f64, @floatFromInt(memo_ns)) / 1_000_000.0;

    std.debug.print("  Without memoization: {d:.2} ms ({} computations)\n", .{ no_memo_ms, iterations * unique_keys });
    std.debug.print("  With memoization: {d:.2} ms ({} initial computations + {} cached reads)\n", .{ memo_ms, unique_keys, iterations * unique_keys - unique_keys });
    std.debug.print("  Cache hits: {}, misses: {}\n", .{ cache.getStats().hits, cache.getStats().misses });
    std.debug.print("  Speedup: {d:.1}x\n", .{no_memo_ms / memo_ms});

    std.debug.print("\n", .{});
}