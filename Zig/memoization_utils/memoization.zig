const std = @import("std");
const Allocator = std.mem.Allocator;
const time = std.time;

/// Cache entry with optional TTL
pub fn CacheEntry(comptime V: type) type {
    return struct {
        value: V,
        created_at: i64,
        ttl_ms: ?u64,

        const Self = @This();

        pub fn init(value: V, ttl_ms: ?u64) Self {
            return .{
                .value = value,
                .created_at = @as(i64, @intCast(time.milliTimestamp())),
                .ttl_ms = ttl_ms,
            };
        }

        pub fn isExpired(self: *const Self) bool {
            if (self.ttl_ms) |ttl| {
                const now = @as(i64, @intCast(time.milliTimestamp()));
                const elapsed = @as(u64, @intCast(now - self.created_at));
                return elapsed > ttl;
            }
            return false;
        }

        pub fn remainingTtl(self: *const Self) ?u64 {
            if (self.ttl_ms) |ttl| {
                const now = @as(i64, @intCast(time.milliTimestamp()));
                const elapsed = @as(u64, @intCast(now - self.created_at));
                return if (elapsed < ttl) ttl - elapsed else 0;
            }
            return null;
        }
    };
}

/// Cache statistics
pub const CacheStats = struct {
    hits: u64 = 0,
    misses: u64 = 0,
    evictions: u64 = 0,
    expirations: u64 = 0,
    sets: u64 = 0,
    deletes: u64 = 0,

    pub fn hitRatio(self: *const CacheStats) f64 {
        const total = self.hits + self.misses;
        if (total == 0) return 0.0;
        return @as(f64, @floatFromInt(self.hits)) / @as(f64, @floatFromInt(total));
    }

    pub fn reset(self: *CacheStats) void {
        self.* = .{};
    }
};

/// Options for MemoCache
pub const CacheOptions = struct {
    max_size: ?usize = null,
    default_ttl_ms: ?u64 = null,
    enable_stats: bool = true,
};

/// A generic memoization cache with TTL, LRU eviction, and statistics
/// Uses AutoHashMap for automatic hash/eql handling
pub fn MemoCache(comptime K: type, comptime V: type) type {
    const EntryType = CacheEntry(V);

    return struct {
        const Node = struct {
            key: K,
            prev: ?*Node,
            next: ?*Node,
        };

        allocator: Allocator,
        cache: std.AutoHashMap(K, EntryType),
        lru_head: ?*Node,
        lru_tail: ?*Node,
        lru_map: std.AutoHashMap(K, *Node),
        max_size: ?usize,
        default_ttl_ms: ?u64,
        stats: CacheStats,
        enable_stats: bool,

        const Self = @This();

        /// Initialize a new MemoCache
        pub fn init(allocator: Allocator, options: CacheOptions) Self {
            return .{
                .allocator = allocator,
                .cache = std.AutoHashMap(K, EntryType).init(allocator),
                .lru_head = null,
                .lru_tail = null,
                .lru_map = std.AutoHashMap(K, *Node).init(allocator),
                .max_size = options.max_size,
                .default_ttl_ms = options.default_ttl_ms,
                .stats = .{},
                .enable_stats = options.enable_stats,
            };
        }

        /// Free all resources
        pub fn deinit(self: *Self) void {
            // Free all LRU nodes
            var iter = self.lru_map.valueIterator();
            while (iter.next()) |node_ptr| {
                self.allocator.destroy(node_ptr.*);
            }
            self.lru_map.deinit();
            self.cache.deinit();
        }

        /// Get a value from the cache
        pub fn get(self: *Self, key: K) ?V {
            // First, clean expired entries
            self.cleanExpired();

            if (self.cache.getPtr(key)) |entry| {
                if (entry.isExpired()) {
                    _ = self.remove(key);
                    if (self.enable_stats) self.stats.expirations += 1;
                    if (self.enable_stats) self.stats.misses += 1;
                    return null;
                }

                // Update LRU - move to front
                self.moveToFront(key);

                if (self.enable_stats) self.stats.hits += 1;
                return entry.value;
            }

            if (self.enable_stats) self.stats.misses += 1;
            return null;
        }

        /// Get cache entry with metadata
        pub fn getEntry(self: *Self, key: K) ?EntryType {
            self.cleanExpired();

            if (self.cache.getPtr(key)) |entry| {
                if (entry.isExpired()) {
                    _ = self.remove(key);
                    if (self.enable_stats) self.stats.expirations += 1;
                    return null;
                }

                self.moveToFront(key);
                if (self.enable_stats) self.stats.hits += 1;
                return entry.*;
            }

            if (self.enable_stats) self.stats.misses += 1;
            return null;
        }

        /// Set a value in the cache
        pub fn set(self: *Self, key: K, value: V) !void {
            try self.setWithTtl(key, value, null);
        }

        /// Set a value with a specific TTL
        pub fn setWithTtl(self: *Self, key: K, value: V, ttl_ms: ?u64) !void {
            const effective_ttl = ttl_ms orelse self.default_ttl_ms;
            const entry = EntryType.init(value, effective_ttl);

            // Check if we need to evict
            if (self.max_size) |max| {
                if (self.cache.count() >= max and !self.cache.contains(key)) {
                    try self.evictOne();
                }
            }

            // If key already exists, remove old LRU node
            if (self.lru_map.get(key)) |old_node| {
                self.removeLruNode(old_node);
                self.allocator.destroy(old_node);
                _ = self.lru_map.remove(key);
            }

            // Create new LRU node
            const lru_node = try self.allocator.create(Node);
            lru_node.* = .{
                .key = key,
                .prev = null,
                .next = null,
            };

            // Insert into cache and LRU tracking
            try self.cache.put(key, entry);
            try self.lru_map.put(key, lru_node);

            // Add to front of LRU list
            self.addToFront(lru_node);

            if (self.enable_stats) self.stats.sets += 1;
        }

        /// Check if a key exists (and is not expired)
        pub fn contains(self: *Self, key: K) bool {
            self.cleanExpired();

            if (self.cache.getPtr(key)) |entry| {
                if (entry.isExpired()) {
                    _ = self.remove(key);
                    return false;
                }
                return true;
            }
            return false;
        }

        /// Remove a key from the cache
        pub fn remove(self: *Self, key: K) bool {
            if (self.cache.remove(key)) {
                if (self.lru_map.get(key)) |node| {
                    self.removeLruNode(node);
                    self.allocator.destroy(node);
                    _ = self.lru_map.remove(key);
                }
                if (self.enable_stats) self.stats.deletes += 1;
                return true;
            }
            return false;
        }

        /// Clear all entries
        pub fn clear(self: *Self) void {
            var iter = self.lru_map.valueIterator();
            while (iter.next()) |node_ptr| {
                self.allocator.destroy(node_ptr.*);
            }
            self.lru_map.clearRetainingCapacity();
            self.cache.clearRetainingCapacity();
            self.lru_head = null;
            self.lru_tail = null;
        }

        /// Get current size
        pub fn size(self: *const Self) usize {
            return self.cache.count();
        }

        /// Get statistics
        pub fn getStats(self: *const Self) CacheStats {
            return self.stats;
        }

        /// Reset statistics
        pub fn resetStats(self: *Self) void {
            self.stats.reset();
        }

        /// Get all keys
        pub fn keys(self: *Self, allocator: Allocator) ![]K {
            var result = std.ArrayList(K).init(allocator);
            var iter = self.cache.keyIterator();
            while (iter.next()) |key| {
                try result.append(key.*);
            }
            return result.toOwnedSlice();
        }

        /// Get all values
        pub fn values(self: *Self, allocator: Allocator) ![]V {
            self.cleanExpired();

            var result = std.ArrayList(V).init(allocator);
            var iter = self.cache.valueIterator();
            while (iter.next()) |entry| {
                if (!entry.isExpired()) {
                    try result.append(entry.value);
                }
            }
            return result.toOwnedSlice();
        }

        /// Memoize a function call
        pub fn memoize(self: *Self, key: K, comptime func: fn () V) !V {
            if (self.get(key)) |cached| {
                return cached;
            }
            const result = func();
            try self.set(key, result);
            return result;
        }

        /// Memoize with error handling
        pub fn memoizeError(self: *Self, key: K, comptime func: fn () anyerror!V) anyerror!V {
            if (self.get(key)) |cached| {
                return cached;
            }
            const result = try func();
            try self.set(key, result);
            return result;
        }

        // Private methods

        fn evictOne(self: *Self) !void {
            if (self.lru_tail) |tail| {
                const key_to_remove = tail.key;
                _ = self.remove(key_to_remove);
                if (self.enable_stats) self.stats.evictions += 1;
            }
        }

        fn cleanExpired(self: *Self) void {
            var keys_to_remove = std.ArrayList(K).init(self.allocator);
            defer keys_to_remove.deinit();

            var iter = self.cache.iterator();
            while (iter.next()) |entry| {
                if (entry.value_ptr.isExpired()) {
                    keys_to_remove.append(entry.key_ptr.*) catch {};
                }
            }

            for (keys_to_remove.items) |key| {
                _ = self.remove(key);
                if (self.enable_stats) self.stats.expirations += 1;
            }
        }

        fn moveToFront(self: *Self, key: K) void {
            if (self.lru_map.get(key)) |node| {
                self.removeLruNode(node);
                self.addToFront(node);
            }
        }

        fn addToFront(self: *Self, node: *Node) void {
            node.prev = null;
            node.next = self.lru_head;

            if (self.lru_head) |head| {
                head.prev = node;
            }

            self.lru_head = node;

            if (self.lru_tail == null) {
                self.lru_tail = node;
            }
        }

        fn removeLruNode(self: *Self, node: *Node) void {
            if (node.prev) |prev| {
                prev.next = node.next;
            } else {
                self.lru_head = node.next;
            }

            if (node.next) |next| {
                next.prev = node.prev;
            } else {
                self.lru_tail = node.prev;
            }
        }
    };
}

/// Simple function memoization helper
pub fn Memoize(comptime K: type, comptime V: type) type {
    return struct {
        cache: MemoCache(K, V),

        const Self = @This();

        pub fn init(allocator: Allocator) Self {
            return .{
                .cache = MemoCache(K, V).init(allocator, .{}),
            };
        }

        pub fn initWithOptions(allocator: Allocator, options: CacheOptions) Self {
            return .{
                .cache = MemoCache(K, V).init(allocator, options),
            };
        }

        pub fn deinit(self: *Self) void {
            self.cache.deinit();
        }

        pub fn call(self: *Self, key: K, comptime func: fn () V) !V {
            return self.cache.memoize(key, func);
        }

        pub fn callError(self: *Self, key: K, comptime func: fn () anyerror!V) anyerror!V {
            return self.cache.memoizeError(key, func);
        }

        pub fn get(self: *Self, key: K) ?V {
            return self.cache.get(key);
        }

        pub fn set(self: *Self, key: K, value: V) !void {
            return self.cache.set(key, value);
        }

        pub fn clear(self: *Self) void {
            self.cache.clear();
        }

        pub fn stats(self: *const Self) CacheStats {
            return self.cache.getStats();
        }
    };
}

// Tests
test "MemoCache basic operations" {
    const allocator = std.testing.allocator;

    var cache = MemoCache(i32, i32).init(allocator, .{});
    defer cache.deinit();

    // Test set and get
    try cache.set(1, 100);
    try std.testing.expectEqual(@as(?i32, 100), cache.get(1));

    // Test missing key
    try std.testing.expectEqual(@as(?i32, null), cache.get(999));

    // Test overwrite
    try cache.set(1, 200);
    try std.testing.expectEqual(@as(?i32, 200), cache.get(1));

    // Test remove
    try std.testing.expect(cache.remove(1));
    try std.testing.expectEqual(@as(?i32, null), cache.get(1));
}

test "MemoCache contains and size" {
    const allocator = std.testing.allocator;

    var cache = MemoCache(i32, i32).init(allocator, .{});
    defer cache.deinit();

    try std.testing.expectEqual(@as(usize, 0), cache.size());
    try std.testing.expect(!cache.contains(1));

    try cache.set(1, 100);
    try std.testing.expectEqual(@as(usize, 1), cache.size());
    try std.testing.expect(cache.contains(1));

    try cache.set(2, 200);
    try std.testing.expectEqual(@as(usize, 2), cache.size());

    _ = cache.remove(1);
    try std.testing.expectEqual(@as(usize, 1), cache.size());
}

test "MemoCache statistics" {
    const allocator = std.testing.allocator;

    var cache = MemoCache(i32, i32).init(allocator, .{ .enable_stats = true });
    defer cache.deinit();

    // Miss
    _ = cache.get(1);
    try std.testing.expectEqual(@as(u64, 1), cache.getStats().misses);

    // Set
    try cache.set(1, 100);
    try std.testing.expectEqual(@as(u64, 1), cache.getStats().sets);

    // Hit
    _ = cache.get(1);
    try std.testing.expectEqual(@as(u64, 1), cache.getStats().hits);

    // Hit ratio
    try std.testing.expectApproxEqAbs(@as(f64, 0.5), cache.getStats().hitRatio(), 0.001);

    // Delete
    _ = cache.remove(1);
    try std.testing.expectEqual(@as(u64, 1), cache.getStats().deletes);
}

test "MemoCache LRU eviction" {
    const allocator = std.testing.allocator;

    var cache = MemoCache(i32, i32).init(allocator, .{ .max_size = 3 });
    defer cache.deinit();

    try cache.set(1, 100);
    try cache.set(2, 200);
    try cache.set(3, 300);

    try std.testing.expectEqual(@as(usize, 3), cache.size());

    // Add fourth item - should evict LRU (1)
    try cache.set(4, 400);

    try std.testing.expectEqual(@as(usize, 3), cache.size());
    try std.testing.expectEqual(@as(?i32, null), cache.get(1)); // Evicted
    try std.testing.expectEqual(@as(?i32, 200), cache.get(2)); // Still there
    try std.testing.expectEqual(@as(?i32, 300), cache.get(3)); // Still there
    try std.testing.expectEqual(@as(?i32, 400), cache.get(4)); // New item

    try std.testing.expectEqual(@as(u64, 1), cache.getStats().evictions);
}

test "MemoCache clear" {
    const allocator = std.testing.allocator;

    var cache = MemoCache(i32, i32).init(allocator, .{});
    defer cache.deinit();

    try cache.set(1, 100);
    try cache.set(2, 200);
    try cache.set(3, 300);

    try std.testing.expectEqual(@as(usize, 3), cache.size());

    cache.clear();

    try std.testing.expectEqual(@as(usize, 0), cache.size());
    try std.testing.expectEqual(@as(?i32, null), cache.get(1));
}

test "MemoCache TTL expiration" {
    const allocator = std.testing.allocator;

    var cache = MemoCache(i32, i32).init(allocator, .{});
    defer cache.deinit();

    // Set with very short TTL (1ms)
    try cache.setWithTtl(1, 100, 1);

    // Should exist immediately
    try std.testing.expectEqual(@as(?i32, 100), cache.get(1));

    // Wait for expiration
    std.time.sleep(10 * std.time.ns_per_ms);

    // Should be expired now
    try std.testing.expectEqual(@as(?i32, null), cache.get(1));
}

test "MemoCache default TTL" {
    const allocator = std.testing.allocator;

    var cache = MemoCache(i32, i32).init(allocator, .{ .default_ttl_ms = 5 });
    defer cache.deinit();

    // Set without explicit TTL - should use default
    try cache.set(1, 100);

    try std.testing.expectEqual(@as(?i32, 100), cache.get(1));

    // Wait for default TTL to expire
    std.time.sleep(10 * std.time.ns_per_ms);

    try std.testing.expectEqual(@as(?i32, null), cache.get(1));
}

test "CacheEntry TTL" {
    const entry = CacheEntry(i32).init(42, 1000); // 1 second TTL

    try std.testing.expect(!entry.isExpired());
    try std.testing.expect(entry.remainingTtl() != null);
    try std.testing.expect(entry.remainingTtl().? > 0);
}

test "CacheEntry no TTL" {
    const entry = CacheEntry(i32).init(42, null);

    try std.testing.expect(!entry.isExpired());
    try std.testing.expect(entry.remainingTtl() == null);
}

test "CacheStats hit ratio" {
    var stats = CacheStats{};

    // Zero case
    try std.testing.expectEqual(@as(f64, 0.0), stats.hitRatio());

    // All misses
    stats.misses = 10;
    try std.testing.expectEqual(@as(f64, 0.0), stats.hitRatio());

    // Half hits
    stats.hits = 10;
    try std.testing.expectApproxEqAbs(@as(f64, 0.5), stats.hitRatio(), 0.001);

    // All hits
    stats.misses = 0;
    try std.testing.expectEqual(@as(f64, 1.0), stats.hitRatio());
}

test "Memoize helper" {
    const allocator = std.testing.allocator;

    var memo = Memoize(i32, i32).init(allocator);
    defer memo.deinit();

    const expensiveFunc = struct {
        var count: u32 = 0;
        fn call() i32 {
            count += 1;
            return @as(i32, @intCast(count * 10));
        }
    };

    // First call
    const result1 = try memo.call(1, expensiveFunc.call);
    try std.testing.expectEqual(@as(i32, 10), result1);

    // Second call - should return cached
    const result2 = try memo.call(1, expensiveFunc.call);
    try std.testing.expectEqual(@as(i32, 10), result2);

    // Function should only be called once
    try std.testing.expectEqual(@as(u32, 1), expensiveFunc.count);
}

test "MemoCache getEntry with metadata" {
    const allocator = std.testing.allocator;

    var cache = MemoCache(i32, i32).init(allocator, .{});
    defer cache.deinit();

    try cache.setWithTtl(1, 100, 60000);

    if (cache.getEntry(1)) |entry| {
        try std.testing.expectEqual(@as(i32, 100), entry.value);
        try std.testing.expect(!entry.isExpired());
        try std.testing.expect(entry.remainingTtl() != null);
    } else {
        return error.UnexpectedNull;
    }
}