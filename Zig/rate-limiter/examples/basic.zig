const std = @import("std");
const rate_limiter = @import("rate_limiter");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();

    try stdout.print("=== Rate Limiter Basic Examples ===\n\n", .{});

    // Example 1: Token Bucket - allows bursts
    try stdout.print("1. Token Bucket Rate Limiter\n", .{});
    try stdout.print("   Good for: allowing bursts while maintaining average rate\n\n", .{});

    var token_bucket = rate_limiter.TokenBucket.init(10, 5, std.time.ns_per_s);
    try stdout.print("   Capacity: 10 tokens, Refill: 5 tokens/second\n", .{});
    try stdout.print("   Available tokens: {}\n", .{token_bucket.availableTokens()});

    // Try to consume 7 tokens at once
    if (token_bucket.tryConsume(7)) {
        try stdout.print("   ✓ Consumed 7 tokens (burst allowed)\n", .{});
    }
    try stdout.print("   Remaining: {}\n", .{token_bucket.availableTokens()});

    // Try to consume more than available
    if (!token_bucket.tryConsume(10)) {
        try stdout.print("   ✗ Cannot consume 10 tokens (not enough)\n", .{});
    }

    // Reset and show
    token_bucket.reset();
    try stdout.print("   After reset: {} tokens\n\n", .{token_bucket.availableTokens()});

    // Example 2: Fixed Window - simple counter
    try stdout.print("2. Fixed Window Rate Limiter\n", .{});
    try stdout.print("   Good for: simple API rate limiting with clear windows\n\n", .{});

    var fixed_window = rate_limiter.FixedWindow.init(5, std.time.ns_per_s);
    try stdout.print("   Max requests: 5 per second\n", .{});

    for (0..6) |i| {
        if (fixed_window.tryAcquire()) {
            try stdout.print("   Request {d}: ✓ allowed\n", .{i + 1});
        } else {
            try stdout.print("   Request {d}: ✗ rate limited\n", .{i + 1});
        }
    }

    try stdout.print("   Current count: {}/{}\n\n", .{ fixed_window.currentCount(), fixed_window.max_requests });

    // Example 3: Sliding Window - precise limiting
    try stdout.print("3. Sliding Window Rate Limiter\n", .{});
    try stdout.print("   Good for: precise rate limiting without burst spikes\n\n", .{});

    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var sliding_window = rate_limiter.SlidingWindow.init(allocator, 3, std.time.ns_per_s);
    defer sliding_window.deinit();

    try stdout.print("   Max requests: 3 per second\n", .{});

    for (0..5) |i| {
        if (sliding_window.tryAcquire()) {
            try stdout.print("   Request {d}: ✓ allowed (count: {})\n", .{ i + 1, sliding_window.currentCount() });
        } else {
            try stdout.print("   Request {d}: ✗ rate limited\n", .{i + 1});
        }
    }

    try stdout.print("   Remaining: {} requests\n\n", .{sliding_window.remaining()});

    // Example 4: Leaky Bucket - smooth traffic
    try stdout.print("4. Leaky Bucket Rate Limiter\n", .{});
    try stdout.print("   Good for: smoothing out traffic bursts\n\n", .{});

    var leaky_bucket = rate_limiter.LeakyBucket.init(10, 3, std.time.ns_per_s);
    try stdout.print("   Capacity: 10, Leak rate: 3/second\n", .{});

    // Fill the bucket
    if (leaky_bucket.tryPour(8)) {
        try stdout.print("   Added 8 drops (burst accepted)\n", .{});
    }
    try stdout.print("   Current level: {}/{}\n", .{ leaky_bucket.currentLevel(), leaky_bucket.capacity });

    // Try to overflow
    if (!leaky_bucket.tryPour(10)) {
        try stdout.print("   ✗ Cannot add 10 drops (would overflow)\n", .{});
    }

    try stdout.print("   Remaining capacity: {}\n\n", .{leaky_bucket.remainingCapacity()});

    // Example 5: Convenience functions
    try stdout.print("5. Convenience Functions\n", .{});
    try stdout.print("   Quick setup for common use cases\n\n", .{});

    var per_second = rate_limiter.tokenBucketPerSecond(100, 10);
    try stdout.print("   TokenBucket: 100 capacity, 10 tokens/sec\n", .{});
    try stdout.print("   Available: {}\n", .{per_second.availableTokens()});

    var per_minute = rate_limiter.fixedWindowPerMinute(60);
    try stdout.print("   FixedWindow: 60 requests/minute\n", .{});
    try stdout.print("   Remaining: {}\n", .{per_minute.remaining()});

    try stdout.print("\n=== Examples Complete ===\n", .{});
}