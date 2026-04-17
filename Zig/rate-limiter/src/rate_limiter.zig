const std = @import("std");
const time = std.time;
const math = std.math;

/// Rate limiter errors
pub const RateLimiterError = error{
    /// Operation would exceed rate limit
    RateLimitExceeded,
    /// Invalid configuration
    InvalidConfig,
    /// Memory allocation failed
    OutOfMemory,
};

/// Time units for rate configuration
pub const TimeUnit = enum {
    milliseconds,
    seconds,
    minutes,
    hours,

    /// Convert to nanoseconds
    pub fn toNanos(self: TimeUnit, value: u64) u64 {
        return switch (self) {
            .milliseconds => value * time.ns_per_ms,
            .seconds => value * time.ns_per_s,
            .minutes => value * time.ns_per_min,
            .hours => value * time.ns_per_hour,
        };
    }
};

// =============================================================================
// Token Bucket Rate Limiter
// =============================================================================

/// Token Bucket Rate Limiter
/// Allows bursts up to bucket capacity, refills tokens over time
pub const TokenBucket = struct {
    const Self = @This();

    capacity: u64,
    tokens: f64,
    refill_rate: f64, // tokens per nanosecond
    last_refill: i128,

    /// Initialize a new Token Bucket rate limiter
    /// capacity: maximum number of tokens (burst size)
    /// refill_amount: number of tokens to add per interval
    /// interval: time interval in nanoseconds
    pub fn init(capacity: u64, refill_amount: u64, interval_ns: u64) Self {
        return .{
            .capacity = capacity,
            .tokens = @floatFromInt(capacity),
            .refill_rate = if (interval_ns > 0) @as(f64, @floatFromInt(refill_amount)) / @as(f64, @floatFromInt(interval_ns)) else 0,
            .last_refill = time.nanoTimestamp(),
        };
    }

    /// Initialize with time unit
    pub fn initWithUnit(capacity: u64, refill_amount: u64, value: u64, unit: TimeUnit) Self {
        return init(capacity, refill_amount, unit.toNanos(value));
    }

    /// Refill tokens based on elapsed time
    fn refill(self: *Self) void {
        const now = time.nanoTimestamp();
        const elapsed = @as(f64, @floatFromInt(@as(u64, @intCast(now - self.last_refill))));
        self.tokens = @min(@as(f64, @floatFromInt(self.capacity)), self.tokens + elapsed * self.refill_rate);
        self.last_refill = now;
    }

    /// Try to consume tokens (returns true if allowed)
    pub fn tryConsume(self: *Self, tokens: u64) bool {
        self.refill();
        const requested: f64 = @floatFromInt(tokens);
        if (self.tokens >= requested) {
            self.tokens -= requested;
            return true;
        }
        return false;
    }

    /// Consume tokens (returns error if rate limit exceeded)
    pub fn consume(self: *Self, tokens: u64) RateLimiterError!void {
        if (!self.tryConsume(tokens)) {
            return RateLimiterError.RateLimitExceeded;
        }
    }

    /// Try to consume a single token
    pub fn tryAcquire(self: *Self) bool {
        return self.tryConsume(1);
    }

    /// Get current token count
    pub fn availableTokens(self: *Self) u64 {
        self.refill();
        return @intFromFloat(@floor(self.tokens));
    }

    /// Get time until tokens are available (in nanoseconds)
    pub fn timeUntilAvailable(self: *Self, tokens: u64) u64 {
        self.refill();
        const requested: f64 = @floatFromInt(tokens);
        if (self.tokens >= requested) {
            return 0;
        }
        const needed = requested - self.tokens;
        if (self.refill_rate > 0) {
            const nanos = needed / self.refill_rate;
            return @intFromFloat(@ceil(nanos));
        }
        return math.maxInt(u64);
    }

    /// Reset to full capacity
    pub fn reset(self: *Self) void {
        self.tokens = @floatFromInt(self.capacity);
        self.last_refill = time.nanoTimestamp();
    }
};

// =============================================================================
// Sliding Window Rate Limiter
// =============================================================================

/// Sliding Window Rate Limiter
/// Uses precise time-based tracking for smooth rate limiting
pub const SlidingWindow = struct {
    const Self = @This();

    allocator: std.mem.Allocator,
    max_requests: u64,
    window_ns: u64,
    timestamps: std.ArrayList(u64),

    /// Initialize a new Sliding Window rate limiter
    pub fn init(allocator: std.mem.Allocator, max_requests: u64, window_ns: u64) Self {
        return .{
            .allocator = allocator,
            .max_requests = max_requests,
            .window_ns = window_ns,
            .timestamps = std.ArrayList(u64).init(allocator),
        };
    }

    /// Initialize with time unit
    pub fn initWithUnit(allocator: std.mem.Allocator, max_requests: u64, value: u64, unit: TimeUnit) Self {
        return init(allocator, max_requests, unit.toNanos(value));
    }

    /// Deinitialize and free resources
    pub fn deinit(self: *Self) void {
        self.timestamps.deinit();
    }

    /// Remove expired timestamps
    fn cleanExpired(self: *Self) void {
        const now = @as(u64, @intCast(time.nanoTimestamp()));
        const cutoff = if (now > self.window_ns) now - self.window_ns else 0;

        // Find first non-expired timestamp
        var i: usize = 0;
        while (i < self.timestamps.items.len) {
            if (self.timestamps.items[i] >= cutoff) {
                break;
            }
            i += 1;
        }

        // Remove expired entries (they're sorted, so remove from start)
        if (i > 0) {
            _ = self.timestamps.orderedRemove(0);
            // Remove remaining expired
            while (self.timestamps.items.len > 0 and self.timestamps.items[0] < cutoff) {
                _ = self.timestamps.orderedRemove(0);
            }
        }
    }

    /// Try to make a request (returns true if allowed)
    pub fn tryAcquire(self: *Self) bool {
        return self.tryAcquireN(1);
    }

    /// Try to make N requests (returns true if allowed)
    pub fn tryAcquireN(self: *Self, count: u64) bool {
        self.cleanExpired();

        if (self.timestamps.items.len + count <= self.max_requests) {
            const now = @as(u64, @intCast(time.nanoTimestamp()));
            for (0..count) |_| {
                self.timestamps.append(now) catch return false;
            }
            return true;
        }
        return false;
    }

    /// Make a request (returns error if rate limit exceeded)
    pub fn acquire(self: *Self) RateLimiterError!void {
        if (!self.tryAcquire()) {
            return RateLimiterError.RateLimitExceeded;
        }
    }

    /// Get current request count in window
    pub fn currentCount(self: *Self) u64 {
        self.cleanExpired();
        return @intCast(self.timestamps.items.len);
    }

    /// Get remaining requests allowed
    pub fn remaining(self: *Self) u64 {
        self.cleanExpired();
        const current = self.timestamps.items.len;
        if (current >= self.max_requests) {
            return 0;
        }
        return self.max_requests - @as(u64, @intCast(current));
    }

    /// Get time until next request is available (in nanoseconds)
    pub fn timeUntilAvailable(self: *Self) u64 {
        self.cleanExpired();

        if (self.timestamps.items.len < self.max_requests) {
            return 0;
        }

        if (self.timestamps.items.len == 0) {
            return 0;
        }

        const now = @as(u64, @intCast(time.nanoTimestamp()));
        const oldest = self.timestamps.items[0];
        const expiry = oldest + self.window_ns;

        if (now >= expiry) {
            return 0;
        }

        return expiry - now;
    }

    /// Reset the rate limiter
    pub fn reset(self: *Self) void {
        self.timestamps.clearRetainingCapacity();
    }
};

// =============================================================================
// Fixed Window Rate Limiter
// =============================================================================

/// Fixed Window Rate Limiter
/// Simple counter-based rate limiting with fixed time windows
pub const FixedWindow = struct {
    const Self = @This();

    max_requests: u64,
    window_ns: u64,
    count: u64,
    window_start: u64,

    /// Initialize a new Fixed Window rate limiter
    pub fn init(max_requests: u64, window_ns: u64) Self {
        return .{
            .max_requests = max_requests,
            .window_ns = window_ns,
            .count = 0,
            .window_start = @intCast(time.nanoTimestamp()),
        };
    }

    /// Initialize with time unit
    pub fn initWithUnit(max_requests: u64, value: u64, unit: TimeUnit) Self {
        return init(max_requests, unit.toNanos(value));
    }

    /// Check and update window if needed
    fn checkWindow(self: *Self) void {
        const now = @as(u64, @intCast(time.nanoTimestamp()));
        if (now - self.window_start >= self.window_ns) {
            self.count = 0;
            self.window_start = now;
        }
    }

    /// Try to make a request (returns true if allowed)
    pub fn tryAcquire(self: *Self) bool {
        return self.tryAcquireN(1);
    }

    /// Try to make N requests (returns true if allowed)
    pub fn tryAcquireN(self: *Self, count: u64) bool {
        self.checkWindow();

        if (self.count + count <= self.max_requests) {
            self.count += count;
            return true;
        }
        return false;
    }

    /// Make a request (returns error if rate limit exceeded)
    pub fn acquire(self: *Self) RateLimiterError!void {
        if (!self.tryAcquire()) {
            return RateLimiterError.RateLimitExceeded;
        }
    }

    /// Get current request count in window
    pub fn currentCount(self: *Self) u64 {
        self.checkWindow();
        return self.count;
    }

    /// Get remaining requests allowed
    pub fn remaining(self: *Self) u64 {
        self.checkWindow();
        if (self.count >= self.max_requests) {
            return 0;
        }
        return self.max_requests - self.count;
    }

    /// Get time until window resets (in nanoseconds)
    pub fn timeUntilReset(self: *Self) u64 {
        self.checkWindow();
        const now = @as(u64, @intCast(time.nanoTimestamp()));
        const elapsed = now - self.window_start;
        if (elapsed >= self.window_ns) {
            return 0;
        }
        return self.window_ns - elapsed;
    }

    /// Reset the rate limiter
    pub fn reset(self: *Self) void {
        self.count = 0;
        self.window_start = @intCast(time.nanoTimestamp());
    }
};

// =============================================================================
// Leaky Bucket Rate Limiter
// =============================================================================

/// Leaky Bucket Rate Limiter
/// Smooths traffic at a constant rate
pub const LeakyBucket = struct {
    const Self = @This();

    capacity: u64,
    water: f64,
    leak_rate: f64, // drops per nanosecond
    last_leak: i128,

    /// Initialize a new Leaky Bucket rate limiter
    /// capacity: maximum bucket size (burst tolerance)
    /// leak_amount: drops to leak per interval
    /// interval_ns: time interval in nanoseconds
    pub fn init(capacity: u64, leak_amount: u64, interval_ns: u64) Self {
        return .{
            .capacity = capacity,
            .water = 0,
            .leak_rate = if (interval_ns > 0) @as(f64, @floatFromInt(leak_amount)) / @as(f64, @floatFromInt(interval_ns)) else 0,
            .last_leak = time.nanoTimestamp(),
        };
    }

    /// Initialize with time unit
    pub fn initWithUnit(capacity: u64, leak_amount: u64, value: u64, unit: TimeUnit) Self {
        return init(capacity, leak_amount, unit.toNanos(value));
    }

    /// Leak water based on elapsed time
    fn leak(self: *Self) void {
        const now = time.nanoTimestamp();
        const elapsed = @as(f64, @floatFromInt(@as(u64, @intCast(now - self.last_leak))));
        self.water = @max(0, self.water - elapsed * self.leak_rate);
        self.last_leak = now;
    }

    /// Try to add water (make a request)
    pub fn tryPour(self: *Self, drops: u64) bool {
        self.leak();
        const requested: f64 = @floatFromInt(drops);
        if (self.water + requested <= @as(f64, @floatFromInt(self.capacity))) {
            self.water += requested;
            return true;
        }
        return false;
    }

    /// Add water (returns error if bucket overflows)
    pub fn pour(self: *Self, drops: u64) RateLimiterError!void {
        if (!self.tryPour(drops)) {
            return RateLimiterError.RateLimitExceeded;
        }
    }

    /// Try to add a single drop
    pub fn tryAcquire(self: *Self) bool {
        return self.tryPour(1);
    }

    /// Get current water level
    pub fn currentLevel(self: *Self) u64 {
        self.leak();
        return @intFromFloat(@floor(self.water));
    }

    /// Get remaining capacity
    pub fn remainingCapacity(self: *Self) u64 {
        self.leak();
        const current: f64 = @floatFromInt(self.currentLevel());
        const remaining = @as(f64, @floatFromInt(self.capacity)) - current;
        return @intFromFloat(@floor(@max(0, remaining)));
    }

    /// Get time until bucket drains to accept drops (in nanoseconds)
    pub fn timeUntilAvailable(self: *Self, drops: u64) u64 {
        self.leak();
        const requested: f64 = @floatFromInt(drops);
        const capacity_f: f64 = @floatFromInt(self.capacity);

        if (self.water + requested <= capacity_f) {
            return 0;
        }

        const excess = self.water + requested - capacity_f;
        if (self.leak_rate > 0) {
            const nanos = excess / self.leak_rate;
            return @intFromFloat(@ceil(nanos));
        }
        return math.maxInt(u64);
    }

    /// Reset the bucket
    pub fn reset(self: *Self) void {
        self.water = 0;
        self.last_leak = time.nanoTimestamp();
    }
};

// =============================================================================
// Convenience Functions
// =============================================================================

/// Create a Token Bucket limiter for requests per second
pub fn tokenBucketPerSecond(capacity: u64, refill_rate: u64) TokenBucket {
    return TokenBucket.initWithUnit(capacity, refill_rate, 1, .seconds);
}

/// Create a Token Bucket limiter for requests per minute
pub fn tokenBucketPerMinute(capacity: u64, refill_rate: u64) TokenBucket {
    return TokenBucket.initWithUnit(capacity, refill_rate, 1, .minutes);
}

/// Create a Fixed Window limiter for requests per second
pub fn fixedWindowPerSecond(max_requests: u64) FixedWindow {
    return FixedWindow.initWithUnit(max_requests, 1, .seconds);
}

/// Create a Fixed Window limiter for requests per minute
pub fn fixedWindowPerMinute(max_requests: u64) FixedWindow {
    return FixedWindow.initWithUnit(max_requests, 1, .minutes);
}

/// Create a Sliding Window limiter for requests per second
pub fn slidingWindowPerSecond(allocator: std.mem.Allocator, max_requests: u64) SlidingWindow {
    return SlidingWindow.initWithUnit(allocator, max_requests, 1, .seconds);
}

/// Create a Sliding Window limiter for requests per minute
pub fn slidingWindowPerMinute(allocator: std.mem.Allocator, max_requests: u64) SlidingWindow {
    return SlidingWindow.initWithUnit(allocator, max_requests, 1, .minutes);
}

/// Create a Leaky Bucket limiter with rate per second
pub fn leakyBucketPerSecond(capacity: u64, leak_rate: u64) LeakyBucket {
    return LeakyBucket.initWithUnit(capacity, leak_rate, 1, .seconds);
}

/// Create a Leaky Bucket limiter with rate per minute
pub fn leakyBucketPerMinute(capacity: u64, leak_rate: u64) LeakyBucket {
    return LeakyBucket.initWithUnit(capacity, leak_rate, 1, .minutes);
}

// =============================================================================
// Tests
// =============================================================================

test "TokenBucket basic operations" {
    var bucket = TokenBucket.init(10, 5, time.ns_per_s);
    _ = &bucket;

    // Should start with full capacity
    try std.testing.expectEqual(@as(u64, 10), bucket.availableTokens());

    // Should be able to consume tokens
    try std.testing.expect(bucket.tryAcquire());
    try std.testing.expectEqual(@as(u64, 9), bucket.availableTokens());

    // Should be able to consume multiple tokens
    try std.testing.expect(bucket.tryConsume(5));
    try std.testing.expectEqual(@as(u64, 4), bucket.availableTokens());

    // Should fail when not enough tokens
    try std.testing.expect(!bucket.tryConsume(10));

    // Reset should restore capacity
    bucket.reset();
    try std.testing.expectEqual(@as(u64, 10), bucket.availableTokens());
}

test "TokenBucket rate limiting" {
    var bucket = TokenBucket.init(5, 1, 100_000_000); // 1 token per 100ms

    // Consume all tokens
    try std.testing.expect(bucket.tryConsume(5));
    try std.testing.expectEqual(@as(u64, 0), bucket.availableTokens());

    // Should fail immediately
    try std.testing.expect(!bucket.tryAcquire());

    // Wait for refill (150ms)
    time.sleep(150 * time.ns_per_ms);

    // Should have ~1 token
    try std.testing.expect(bucket.availableTokens() >= 1);
}

test "TokenBucket convenience functions" {
    var per_second = tokenBucketPerSecond(100, 10);
    _ = &per_second;
    try std.testing.expectEqual(@as(u64, 100), per_second.availableTokens());

    var per_minute = tokenBucketPerMinute(1000, 100);
    _ = &per_minute;
    try std.testing.expectEqual(@as(u64, 1000), per_minute.availableTokens());
}

test "FixedWindow basic operations" {
    var window = FixedWindow.init(10, time.ns_per_s);

    // Should start empty
    try std.testing.expectEqual(@as(u64, 0), window.currentCount());
    try std.testing.expectEqual(@as(u64, 10), window.remaining());

    // Should allow requests
    for (0..10) |_| {
        try std.testing.expect(window.tryAcquire());
    }

    // Should be at limit
    try std.testing.expectEqual(@as(u64, 10), window.currentCount());
    try std.testing.expectEqual(@as(u64, 0), window.remaining());
    try std.testing.expect(!window.tryAcquire());

    // Reset should clear
    window.reset();
    try std.testing.expectEqual(@as(u64, 0), window.currentCount());
    try std.testing.expectEqual(@as(u64, 10), window.remaining());
}

test "FixedWindow tryAcquireN" {
    var window = FixedWindow.init(10, time.ns_per_s);

    // Should allow batch
    try std.testing.expect(window.tryAcquireN(5));
    try std.testing.expectEqual(@as(u64, 5), window.currentCount());

    // Should allow another batch
    try std.testing.expect(window.tryAcquireN(3));
    try std.testing.expectEqual(@as(u64, 8), window.currentCount());

    // Should fail if exceeds limit
    try std.testing.expect(!window.tryAcquireN(5));

    // Should allow small batch
    try std.testing.expect(window.tryAcquireN(2));
    try std.testing.expectEqual(@as(u64, 10), window.currentCount());
}

test "FixedWindow window reset" {
    var window = FixedWindow.init(5, 100_000_000); // 100ms window

    // Use all requests
    for (0..5) |_| {
        try std.testing.expect(window.tryAcquire());
    }
    try std.testing.expect(!window.tryAcquire());

    // Wait for window reset
    time.sleep(110 * time.ns_per_ms);

    // Should work again
    try std.testing.expect(window.tryAcquire());
}

test "SlidingWindow basic operations" {
    const allocator = std.testing.allocator;
    var window = SlidingWindow.init(allocator, 10, time.ns_per_s);
    defer window.deinit();

    // Should start empty
    try std.testing.expectEqual(@as(u64, 0), window.currentCount());
    try std.testing.expectEqual(@as(u64, 10), window.remaining());

    // Should allow requests
    for (0..10) |_| {
        try std.testing.expect(window.tryAcquire());
    }

    // Should be at limit
    try std.testing.expectEqual(@as(u64, 10), window.currentCount());
    try std.testing.expectEqual(@as(u64, 0), window.remaining());
    try std.testing.expect(!window.tryAcquire());

    // Reset should clear
    window.reset();
    try std.testing.expectEqual(@as(u64, 0), window.currentCount());
    try std.testing.expectEqual(@as(u64, 10), window.remaining());
}

test "SlidingWindow sliding behavior" {
    const allocator = std.testing.allocator;
    var window = SlidingWindow.init(allocator, 5, 150_000_000); // 150ms window
    defer window.deinit();

    // Use all requests
    for (0..5) |_| {
        try std.testing.expect(window.tryAcquire());
    }
    try std.testing.expect(!window.tryAcquire());

    // Wait for some to expire
    time.sleep(100 * time.ns_per_ms);

    // Still should be limited
    try std.testing.expect(!window.tryAcquire());

    // Wait for full expiration
    time.sleep(100 * time.ns_per_ms);

    // Should work again
    try std.testing.expect(window.tryAcquire());
}

test "SlidingWindow tryAcquireN" {
    const allocator = std.testing.allocator;
    var window = SlidingWindow.init(allocator, 10, time.ns_per_s);
    defer window.deinit();

    // Should allow batch
    try std.testing.expect(window.tryAcquireN(5));
    try std.testing.expectEqual(@as(u64, 5), window.currentCount());

    // Should allow another batch
    try std.testing.expect(window.tryAcquireN(3));
    try std.testing.expectEqual(@as(u64, 8), window.currentCount());

    // Should fail if exceeds limit
    try std.testing.expect(!window.tryAcquireN(5));

    // Should allow exact fit
    try std.testing.expect(window.tryAcquireN(2));
    try std.testing.expectEqual(@as(u64, 10), window.currentCount());
}

test "LeakyBucket basic operations" {
    var bucket = LeakyBucket.init(10, 5, time.ns_per_s);

    // Should start empty
    const initial_level = bucket.currentLevel();
    try std.testing.expectEqual(@as(u64, 0), initial_level);
    try std.testing.expectEqual(@as(u64, 10), bucket.remainingCapacity());

    // Should be able to add water
    try std.testing.expect(bucket.tryAcquire());
    
    // Check level immediately after pour (before any leak)
    // Note: currentLevel() calls leak() which may reduce water over time
    const level_after_acquire = bucket.currentLevel();
    try std.testing.expect(level_after_acquire >= 0);
    try std.testing.expect(level_after_acquire <= 1);

    // Should be able to add multiple drops
    try std.testing.expect(bucket.tryPour(5));
    const level_after_pour = bucket.currentLevel();
    try std.testing.expect(level_after_pour <= 6);

    // Should fail when over capacity
    try std.testing.expect(!bucket.tryPour(10));

    // Reset should drain
    bucket.reset();
    try std.testing.expectEqual(@as(u64, 0), bucket.currentLevel());
}

test "LeakyBucket leak behavior" {
    var bucket = LeakyBucket.init(10, 1, 100_000_000); // 1 drop per 100ms

    // Fill the bucket
    try std.testing.expect(bucket.tryPour(10));
    const initial_level = bucket.currentLevel();
    try std.testing.expect(initial_level <= 10);

    // Should fail when full
    try std.testing.expect(!bucket.tryAcquire());

    // Wait for some to leak (150ms)
    time.sleep(150 * time.ns_per_ms);

    // Level should have decreased
    const leaked_level = bucket.currentLevel();
    try std.testing.expect(leaked_level < 10);

    // Should be able to add more
    try std.testing.expect(bucket.tryAcquire());
}

test "LeakyBucket convenience functions" {
    var per_second = leakyBucketPerSecond(100, 10);
    try std.testing.expectEqual(@as(u64, 0), per_second.currentLevel());
    try std.testing.expectEqual(@as(u64, 100), per_second.remainingCapacity());

    var per_minute = leakyBucketPerMinute(1000, 100);
    try std.testing.expectEqual(@as(u64, 0), per_minute.currentLevel());
}

test "TimeUnit conversions" {
    try std.testing.expectEqual(@as(u64, 1_000_000), TimeUnit.milliseconds.toNanos(1));
    try std.testing.expectEqual(@as(u64, 1_000_000_000), TimeUnit.seconds.toNanos(1));
    try std.testing.expectEqual(@as(u64, 60_000_000_000), TimeUnit.minutes.toNanos(1));
    try std.testing.expectEqual(@as(u64, 3_600_000_000_000), TimeUnit.hours.toNanos(1));
}

test "RateLimiterError" {
    var bucket = TokenBucket.init(1, 1, time.ns_per_s);

    // Consume the token
    try bucket.consume(1);

    // Should error on next attempt
    try std.testing.expectError(RateLimiterError.RateLimitExceeded, bucket.consume(1));
}

test "timeUntilAvailable calculations" {
    var bucket = TokenBucket.init(5, 1, 100_000_000); // 1 token per 100ms

    // Use all tokens
    try std.testing.expect(bucket.tryConsume(5));

    // Should need time for next token
    const wait_time = bucket.timeUntilAvailable(1);
    try std.testing.expect(wait_time > 0);
    try std.testing.expect(wait_time <= 100_000_000);
}

test "FixedWindow convenience functions" {
    var per_second = fixedWindowPerSecond(100);
    try std.testing.expectEqual(@as(u64, 100), per_second.remaining());

    var per_minute = fixedWindowPerMinute(1000);
    try std.testing.expectEqual(@as(u64, 1000), per_minute.remaining());
}

test "SlidingWindow convenience functions" {
    const allocator = std.testing.allocator;

    var per_second = slidingWindowPerSecond(allocator, 100);
    defer per_second.deinit();
    try std.testing.expectEqual(@as(u64, 100), per_second.remaining());

    var per_minute = slidingWindowPerMinute(allocator, 1000);
    defer per_minute.deinit();
    try std.testing.expectEqual(@as(u64, 1000), per_minute.remaining());
}

test "concurrent usage simulation" {
    const allocator = std.testing.allocator;
    var window = SlidingWindow.init(allocator, 100, time.ns_per_s);
    defer window.deinit();

    // Simulate burst of requests
    var allowed: u64 = 0;
    var denied: u64 = 0;

    for (0..150) |_| {
        if (window.tryAcquire()) {
            allowed += 1;
        } else {
            denied += 1;
        }
    }

    try std.testing.expectEqual(@as(u64, 100), allowed);
    try std.testing.expectEqual(@as(u64, 50), denied);
}

test "edge cases" {
    // Zero capacity should never allow
    var zero_bucket = TokenBucket.init(0, 1, time.ns_per_s);
    try std.testing.expect(!zero_bucket.tryAcquire());

    // Single request limit
    var single_window = FixedWindow.init(1, time.ns_per_s);
    try std.testing.expect(single_window.tryAcquire());
    try std.testing.expect(!single_window.tryAcquire());

    // Very small window
    const allocator = std.testing.allocator;
    var small_window = SlidingWindow.init(allocator, 5, 1_000_000); // 1ms
    defer small_window.deinit();

    for (0..5) |_| {
        try std.testing.expect(small_window.tryAcquire());
    }
    try std.testing.expect(!small_window.tryAcquire());
}