const std = @import("std");
const rate_limiter = @import("rate_limiter");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    try stdout.print("=== Rate Limiter Advanced Examples ===\n\n", .{});

    // Example 1: API Rate Limiting Simulation
    try stdout.print("1. API Rate Limiting Simulation\n", .{});
    try stdout.print("   Simulating multiple API clients with different rate limits\n\n", .{});

    var api_limiter = rate_limiter.TokenBucket.init(100, 10, std.time.ns_per_s);
    try stdout.print("   API Rate Limit: 100 burst, 10 req/s refill\n", .{});

    // Simulate burst traffic
    try stdout.print("   Simulating burst of 50 requests...\n", .{});
    var success_count: u64 = 0;
    for (0..50) |_| {
        if (api_limiter.tryAcquire()) {
            success_count += 1;
        }
    }
    try stdout.print("   Accepted: {}/50 requests\n", .{success_count});
    try stdout.print("   Remaining tokens: {}\n\n", .{api_limiter.availableTokens()});

    // Example 2: Multi-tier Rate Limiting
    try stdout.print("2. Multi-tier Rate Limiting\n", .{});
    try stdout.print("   Implementing per-second and per-minute limits\n\n", .{});

    var second_limit = rate_limiter.FixedWindow.init(10, std.time.ns_per_s);
    var minute_limit = rate_limiter.FixedWindow.init(100, std.time.ns_per_min);

    try stdout.print("   Limits: 10/sec, 100/min\n", .{});
    try stdout.print("   Processing 15 simulated requests...\n", .{});

    for (0..15) |i| {
        const second_ok = second_limit.tryAcquire();
        const minute_ok = minute_limit.tryAcquire();

        if (second_ok and minute_ok) {
            try stdout.print("   Request {:2}: ✓ accepted\n", .{i + 1});
        } else if (!second_ok) {
            try stdout.print("   Request {:2}: ✗ second limit exceeded\n", .{i + 1});
        } else {
            try stdout.print("   Request {:2}: ✗ minute limit exceeded\n", .{i + 1});
        }
    }
    try stdout.print("\n", .{});

    // Example 3: Graceful Degradation with Queuing
    try stdout.print("3. Graceful Degradation\n", .{});
    try stdout.print("   Handling rate-limited requests gracefully\n\n", .{});

    var graceful_limiter = rate_limiter.SlidingWindow.init(allocator, 5, std.time.ns_per_s);
    defer graceful_limiter.deinit();

    try stdout.print("   Limit: 5 requests/second\n", .{});

    const requests = [_][]const u8{ "GET /api/users", "POST /api/users", "GET /api/orders", "PUT /api/orders/1", "DELETE /api/orders/1", "GET /api/products", "POST /api/products" };

    for (requests, 0..) |req, i| {
        if (graceful_limiter.tryAcquire()) {
            try stdout.print("   [{d}] ✓ {s} - processed immediately\n", .{ i + 1, req });
        } else {
            const wait_ns = graceful_limiter.timeUntilAvailable();
            const wait_ms = wait_ns / std.time.ns_per_ms;
            try stdout.print("   [{d}] ⏳ {s} - retry after {}ms\n", .{ i + 1, req, wait_ms });
        }
    }
    try stdout.print("\n", .{});

    // Example 4: Token Bucket for Bandwidth Limiting
    try stdout.print("4. Bandwidth Limiting\n", .{});
    try stdout.print("   Simulating bandwidth throttle (1 MB/s with 500KB burst)\n\n", .{});

    // 1 MB/s = 1,000,000 bytes, refill every 100ms
    var bandwidth_limiter = rate_limiter.TokenBucket.init(500_000, 100_000, 100_000_000);

    const transfers = [_]struct { name: []const u8, size: u64 }{
        .{ .name = "image.jpg", .size = 300_000 },
        .{ .name = "document.pdf", .size = 250_000 },
        .{ .name = "video.mp4", .size = 500_000 },
        .{ .name = "archive.zip", .size = 100_000 },
    };

    for (transfers) |transfer| {
        if (bandwidth_limiter.tryConsume(transfer.size)) {
            try stdout.print("   ✓ {s}: {} bytes transferred\n", .{ transfer.name, transfer.size });
        } else {
            const wait_ns = bandwidth_limiter.timeUntilAvailable(transfer.size);
            const wait_ms = wait_ns / std.time.ns_per_ms;
            try stdout.print("   ⏳ {s}: {} bytes - wait {}ms\n", .{ transfer.name, transfer.size, wait_ms });
        }
    }
    try stdout.print("\n", .{});

    // Example 5: Comparing Algorithms
    try stdout.print("5. Algorithm Comparison\n", .{});
    try stdout.print("   Testing same scenario with different limiters\n\n", .{});

    const config = struct {
        limit: u64,
        window_ns: u64,
        burst: u64,
        requests: u64,
    }{
        .limit = 10,
        .window_ns = std.time.ns_per_s,
        .burst = 10,
        .requests = 15,
    };

    // Token Bucket
    var tb = rate_limiter.TokenBucket.init(config.burst, config.limit, config.window_ns);
    var tb_allowed: u64 = 0;
    for (0..config.requests) |_| {
        if (tb.tryAcquire()) tb_allowed += 1;
    }
    try stdout.print("   Token Bucket:     {}/{} allowed (burst first)\n", .{ tb_allowed, config.requests });

    // Fixed Window
    var fw = rate_limiter.FixedWindow.init(config.limit, config.window_ns);
    var fw_allowed: u64 = 0;
    for (0..config.requests) |_| {
        if (fw.tryAcquire()) fw_allowed += 1;
    }
    try stdout.print("   Fixed Window:     {}/{} allowed (hard limit)\n", .{ fw_allowed, config.requests });

    // Sliding Window
    var sw = rate_limiter.SlidingWindow.init(allocator, config.limit, config.window_ns);
    defer sw.deinit();
    var sw_allowed: u64 = 0;
    for (0..config.requests) |_| {
        if (sw.tryAcquire()) sw_allowed += 1;
    }
    try stdout.print("   Sliding Window:   {}/{} allowed (precise)\n", .{ sw_allowed, config.requests });

    // Leaky Bucket
    var lb = rate_limiter.LeakyBucket.init(config.burst, config.limit, config.window_ns);
    var lb_allowed: u64 = 0;
    for (0..config.requests) |_| {
        if (lb.tryAcquire()) lb_allowed += 1;
    }
    try stdout.print("   Leaky Bucket:     {}/{} allowed (smooth drain)\n\n", .{ lb_allowed, config.requests });

    // Example 6: Time Until Available
    try stdout.print("6. Rate Limit Recovery Timing\n", .{});
    try stdout.print("   Calculating wait times for rate-limited clients\n\n", .{});

    var timing_limiter = rate_limiter.TokenBucket.init(3, 1, std.time.ns_per_s);
    try stdout.print("   Capacity: 3 tokens, Refill: 1/sec\n", .{});

    // Exhaust tokens
    _ = timing_limiter.tryConsume(3);
    try stdout.print("   Exhausted all tokens\n", .{});

    for (0..5) |i| {
        const tokens_needed = i + 1;
        const wait_ns = timing_limiter.timeUntilAvailable(tokens_needed);
        const wait_ms = wait_ns / std.time.ns_per_ms;

        if (wait_ns == 0) {
            try stdout.print("   {} token(s): available now\n", .{tokens_needed});
        } else {
            try stdout.print("   {} token(s): wait ~{}ms\n", .{ tokens_needed, wait_ms });
        }
    }
    try stdout.print("\n", .{});

    // Example 7: Batch Operations
    try stdout.print("7. Batch Operations\n", .{});
    try stdout.print("   Handling batch requests efficiently\n\n", .{});

    var batch_limiter = rate_limiter.FixedWindow.init(100, std.time.ns_per_s);

    const batch_sizes = [_]u64{ 30, 25, 40, 20, 15 };
    for (batch_sizes, 0..) |size, i| {
        if (batch_limiter.tryAcquireN(size)) {
            try stdout.print("   Batch {}: ✓ {} requests accepted (total: {}/100)\n", .{ i + 1, size, batch_limiter.currentCount() });
        } else {
            try stdout.print("   Batch {}: ✗ {} requests rejected (remaining: {})\n", .{ i + 1, size, batch_limiter.remaining() });
        }
    }
    try stdout.print("\n", .{});

    try stdout.print("=== Advanced Examples Complete ===\n", .{});
}