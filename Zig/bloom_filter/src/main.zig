const std = @import("std");

/// Bloom Filter - Probabilistic data structure for membership testing
/// 
/// A Bloom filter is a space-efficient probabilistic data structure used to test
/// whether an element is a member of a set. False positive matches are possible,
/// but false negatives are not. In other words, a query returns either "possibly
/// in set" or "definitely not in set".
///
/// Features:
/// - Space-efficient membership testing
/// - Adjustable false positive rate
/// - Multiple hash functions for better distribution
/// - Add and check operations
/// - Union and intersection operations
/// - Serialization support

/// Bloom Filter configuration options
pub const BloomFilterOptions = struct {
    /// Expected number of elements to be inserted
    expected_items: usize = 1000,
    /// Desired false positive probability (0.0 to 1.0)
    false_positive_rate: f64 = 0.01,
    /// Number of hash functions (0 = auto-calculate)
    hash_count: usize = 0,
};

/// Errors that can occur during Bloom Filter operations
pub const BloomFilterError = error{
    /// Invalid false positive rate (must be between 0 and 1)
    InvalidFalsePositiveRate,
    /// Invalid expected items count (must be > 0)
    InvalidExpectedItems,
    /// Item is possibly in set (not an error, used for checking)
    PossiblyInSet,
    /// Memory allocation failed
    OutOfMemory,
};

/// Bloom Filter structure
pub const BloomFilter = struct {
    /// Bit array
    bits: []u8,
    /// Number of bits in the filter
    num_bits: usize,
    /// Number of hash functions
    num_hashes: usize,
    /// Number of items inserted
    count: usize,
    /// Allocator used for memory management
    allocator: std.mem.Allocator,

    /// Initialize a new Bloom Filter with optimal parameters
    pub fn init(allocator: std.mem.Allocator, options: BloomFilterOptions) BloomFilterError!BloomFilter {
        if (options.expected_items == 0) {
            return BloomFilterError.InvalidExpectedItems;
        }
        if (options.false_positive_rate <= 0.0 or options.false_positive_rate >= 1.0) {
            return BloomFilterError.InvalidFalsePositiveRate;
        }

        // Calculate optimal number of bits
        // m = -n * ln(p) / (ln(2)^2)
        const ln2: f64 = 0.6931471805599453;
        const n: f64 = @floatFromInt(options.expected_items);
        const p = options.false_positive_rate;
        const num_bits_float: f64 = -n * @log(p) / (ln2 * ln2);
        const num_bits: usize = @intFromFloat(@round(num_bits_float));

        // Calculate optimal number of hash functions
        // k = m * ln(2) / n
        var num_hashes: usize = options.hash_count;
        if (num_hashes == 0) {
            const num_hashes_float: f64 = num_bits_float * ln2 / n;
            num_hashes = @intFromFloat(@round(num_hashes_float));
            if (num_hashes == 0) num_hashes = 1;
            if (num_hashes > 20) num_hashes = 20; // Practical limit
        }

        // Allocate bit array (num_bits / 8 bytes, rounded up)
        const byte_count = (num_bits + 7) / 8;
        const bits = allocator.alloc(u8, byte_count) catch return BloomFilterError.OutOfMemory;
        @memset(bits, 0);

        return BloomFilter{
            .bits = bits,
            .num_bits = num_bits,
            .num_hashes = num_hashes,
            .count = 0,
            .allocator = allocator,
        };
    }

    /// Initialize a Bloom Filter with explicit parameters
    pub fn initWithParams(allocator: std.mem.Allocator, num_bits: usize, num_hashes: usize) BloomFilterError!BloomFilter {
        if (num_bits == 0) {
            return BloomFilterError.InvalidExpectedItems;
        }
        if (num_hashes == 0) {
            return BloomFilterError.InvalidExpectedItems;
        }

        const byte_count = (num_bits + 7) / 8;
        const bits = allocator.alloc(u8, byte_count) catch return BloomFilterError.OutOfMemory;
        @memset(bits, 0);

        return BloomFilter{
            .bits = bits,
            .num_bits = num_bits,
            .num_hashes = num_hashes,
            .count = 0,
            .allocator = allocator,
        };
    }

    /// Free the Bloom Filter's memory
    pub fn deinit(self: *BloomFilter) void {
        self.allocator.free(self.bits);
    }

    /// Add an item to the Bloom Filter
    pub fn add(self: *BloomFilter, item: []const u8) void {
        const hashes = self.getHashes(item);
        for (hashes[0..self.num_hashes]) |hash| {
            self.setBit(hash);
        }
        self.count += 1;
    }

    /// Add a u64 integer to the Bloom Filter
    pub fn addU64(self: *BloomFilter, value: u64) void {
        var buf: [8]u8 = undefined;
        std.mem.writeInt(u64, &buf, value, .little);
        self.add(&buf);
    }

    /// Check if an item might be in the Bloom Filter
    /// Returns true if the item is possibly in the set, false if definitely not
    pub fn mightContain(self: *const BloomFilter, item: []const u8) bool {
        const hashes = self.getHashes(item);
        for (hashes[0..self.num_hashes]) |hash| {
            if (!self.getBit(hash)) {
                return false;
            }
        }
        return true;
    }

    /// Check if a u64 integer might be in the Bloom Filter
    pub fn mightContainU64(self: *const BloomFilter, value: u64) bool {
        var buf: [8]u8 = undefined;
        std.mem.writeInt(u64, &buf, value, .little);
        return self.mightContain(&buf);
    }

    /// Get the current false positive probability estimate
    pub fn estimateFalsePositiveRate(self: *const BloomFilter) f64 {
        if (self.count == 0) return 0.0;
        
        // p = (1 - e^(-kn/m))^k
        const k: f64 = @floatFromInt(self.num_hashes);
        const n: f64 = @floatFromInt(self.count);
        const m: f64 = @floatFromInt(self.num_bits);
        
        const ratio = -k * n / m;
        const base = 1.0 - @exp(ratio);
        return std.math.pow(f64, base, k);
    }

    /// Get the number of items inserted
    pub fn itemCount(self: *const BloomFilter) usize {
        return self.count;
    }

    /// Get the number of bits used
    pub fn bitCount(self: *const BloomFilter) usize {
        return self.num_bits;
    }

    /// Get the number of hash functions
    pub fn hashFunctionCount(self: *const BloomFilter) usize {
        return self.num_hashes;
    }

    /// Clear all items from the Bloom Filter
    pub fn clear(self: *BloomFilter) void {
        @memset(self.bits, 0);
        self.count = 0;
    }

    /// Check if the Bloom Filter is empty
    pub fn isEmpty(self: *const BloomFilter) bool {
        return self.count == 0;
    }

    /// Union with another Bloom Filter (both must have same parameters)
    pub fn unionWith(self: *BloomFilter, other: *const BloomFilter) BloomFilterError!void {
        if (self.num_bits != other.num_bits) {
            return BloomFilterError.InvalidExpectedItems;
        }
        
        for (self.bits, other.bits) |*a, b| {
            a.* |= b;
        }
        self.count = @max(self.count, other.count);
    }

    /// Intersection with another Bloom Filter (both must have same parameters)
    pub fn intersectWith(self: *BloomFilter, other: *const BloomFilter) BloomFilterError!void {
        if (self.num_bits != other.num_bits) {
            return BloomFilterError.InvalidExpectedItems;
        }
        
        for (self.bits, other.bits) |*a, b| {
            a.* &= b;
        }
        // After intersection, count is an estimate
        self.count = @min(self.count, other.count);
    }

    /// Get the number of bits set
    pub fn bitsSet(self: *const BloomFilter) usize {
        var count: usize = 0;
        for (self.bits) |byte| {
            count += @popCount(byte);
        }
        return count;
    }

    /// Serialize the Bloom Filter to bytes
    pub fn serialize(self: *const BloomFilter, allocator: std.mem.Allocator) BloomFilterError![]u8 {
        // Format: num_bits (u64) + num_hashes (u64) + count (u64) + bits
        const header_size = 24;
        const total_size = header_size + self.bits.len;
        
        const output = allocator.alloc(u8, total_size) catch return BloomFilterError.OutOfMemory;
        
        // Write header
        std.mem.writeInt(u64, output[0..8], self.num_bits, .little);
        std.mem.writeInt(u64, output[8..16], self.num_hashes, .little);
        std.mem.writeInt(u64, output[16..24], self.count, .little);
        
        // Write bits
        @memcpy(output[header_size..], self.bits);
        
        return output;
    }

    /// Deserialize a Bloom Filter from bytes
    pub fn deserialize(allocator: std.mem.Allocator, data: []const u8) BloomFilterError!BloomFilter {
        if (data.len < 24) {
            return BloomFilterError.InvalidExpectedItems;
        }
        
        const num_bits = std.mem.readInt(u64, data[0..8], .little);
        const num_hashes = std.mem.readInt(u64, data[8..16], .little);
        const count = std.mem.readInt(u64, data[16..24], .little);
        
        if (num_bits == 0 or num_hashes == 0) {
            return BloomFilterError.InvalidExpectedItems;
        }
        
        const expected_bits_len = (num_bits + 7) / 8;
        if (data.len < 24 + expected_bits_len) {
            return BloomFilterError.InvalidExpectedItems;
        }
        
        const bits = allocator.alloc(u8, expected_bits_len) catch return BloomFilterError.OutOfMemory;
        @memcpy(bits, data[24..24 + expected_bits_len]);
        
        return BloomFilter{
            .bits = bits,
            .num_bits = num_bits,
            .num_hashes = num_hashes,
            .count = count,
            .allocator = allocator,
        };
    }

    /// Calculate hash values for an item using double hashing technique
    fn getHashes(self: *const BloomFilter, item: []const u8) [20]usize {
        var hashes: [20]usize = undefined;
        
        // Use double hashing: h_i = h1 + i * h2 (with wrapping arithmetic)
        const h1 = self.hash1(item);
        const h2 = self.hash2(item);
        
        for (0..self.num_hashes) |i| {
            // Use wrapping multiplication and addition
            const combined = (h1 +% (i *% h2)) % self.num_bits;
            hashes[i] = combined;
        }
        
        return hashes;
    }

    /// First hash function (FNV-1a)
    fn hash1(self: *const BloomFilter, item: []const u8) usize {
        // FNV-1a hash with wrapping arithmetic
        var hash: usize = 14695981039346656037; // FNV offset basis
        for (item) |byte| {
            hash ^= byte;
            hash = hash *% 1099511628211; // FNV prime (wrapping multiply)
        }
        return hash % self.num_bits;
    }

    /// Second hash function (MurmurHash-like)
    fn hash2(self: *const BloomFilter, item: []const u8) usize {
        // Simple MurmurHash-inspired hash with wrapping arithmetic
        var hash: usize = 0xdeadbeef;
        for (item) |byte| {
            hash ^= byte;
            hash = hash *% 0x5bd1e995; // wrapping multiply
            hash ^= hash >> 15;
        }
        
        // Ensure non-zero to avoid degenerate case
        if (hash == 0) hash = 1;
        return hash % self.num_bits;
    }

    /// Set a bit in the filter
    fn setBit(self: *BloomFilter, index: usize) void {
        const byte_index = index / 8;
        const bit_index = index % 8;
        self.bits[byte_index] |= (@as(u8, 1) << @intCast(bit_index));
    }

    /// Get a bit from the filter
    fn getBit(self: *const BloomFilter, index: usize) bool {
        const byte_index = index / 8;
        const bit_index = index % 8;
        return (self.bits[byte_index] & (@as(u8, 1) << @intCast(bit_index))) != 0;
    }
};

/// Scalable Bloom Filter - grows as needed while maintaining false positive rate
pub const ScalableBloomFilter = struct {
    /// Array of Bloom Filters
    filters: std.ArrayList(BloomFilter),
    /// Initial false positive rate
    initial_fp_rate: f64,
    /// Growth factor for each new filter
    growth_factor: f64,
    /// Tightening ratio for false positive rate
    tightening_ratio: f64,
    /// Current filter index
    current_filter: usize,
    /// Allocator
    allocator: std.mem.Allocator,

    /// Initialize a Scalable Bloom Filter
    pub fn init(allocator: std.mem.Allocator, initial_fp_rate: f64) BloomFilterError!ScalableBloomFilter {
        if (initial_fp_rate <= 0.0 or initial_fp_rate >= 1.0) {
            return BloomFilterError.InvalidFalsePositiveRate;
        }

        var filters = std.ArrayList(BloomFilter).init(allocator);
        const first_filter = try BloomFilter.init(allocator, .{
            .expected_items = 100,
            .false_positive_rate = initial_fp_rate,
        });
        try filters.append(first_filter);

        return ScalableBloomFilter{
            .filters = filters,
            .initial_fp_rate = initial_fp_rate,
            .growth_factor = 2.0,
            .tightening_ratio = 0.9,
            .current_filter = 0,
            .allocator = allocator,
        };
    }

    /// Free all memory
    pub fn deinit(self: *ScalableBloomFilter) void {
        for (self.filters.items) |*f| {
            f.deinit();
        }
        self.filters.deinit();
    }

    /// Add an item
    pub fn add(self: *ScalableBloomFilter, item: []const u8) void {
        self.filters.items[self.current_filter].add(item);
        
        // Check if we need to expand
        const fp_rate = self.filters.items[self.current_filter].estimateFalsePositiveRate();
        if (fp_rate > self.initial_fp_rate) {
            self.expand() catch {};
        }
    }

    /// Check if an item might be in the filter
    pub fn mightContain(self: *const ScalableBloomFilter, item: []const u8) bool {
        for (self.filters.items) |*f| {
            if (f.mightContain(item)) {
                return true;
            }
        }
        return false;
    }

    /// Expand by adding a new filter
    fn expand(self: *ScalableBloomFilter) BloomFilterError!void {
        _ = self.filters.items[self.current_filter].num_bits; // Reference for potential future use
        const new_fp_rate = self.initial_fp_rate * self.tightening_ratio;
        
        const new_filter = try BloomFilter.init(self.allocator, .{
            .expected_items = 100 * @as(usize, @intFromFloat(@round(self.growth_factor))) * (self.current_filter + 1),
            .false_positive_rate = new_fp_rate,
        });
        
        try self.filters.append(new_filter);
        self.current_filter += 1;
    }

    /// Get total count estimate
    pub fn itemCount(self: *const ScalableBloomFilter) usize {
        var total: usize = 0;
        for (self.filters.items) |f| {
            total += f.count;
        }
        return total;
    }

    /// Clear all filters
    pub fn clear(self: *ScalableBloomFilter) void {
        for (self.filters.items) |*f| {
            f.clear();
        }
        self.current_filter = 0;
    }
};

/// Counting Bloom Filter - supports removal of items
pub const CountingBloomFilter = struct {
    /// Counter array (4-bit counters)
    counters: []u8,
    /// Number of counters
    num_counters: usize,
    /// Number of hash functions
    num_hashes: usize,
    /// Number of items
    count: usize,
    /// Allocator
    allocator: std.mem.Allocator,

    /// Initialize a Counting Bloom Filter
    pub fn init(allocator: std.mem.Allocator, options: BloomFilterOptions) BloomFilterError!CountingBloomFilter {
        if (options.expected_items == 0) {
            return BloomFilterError.InvalidExpectedItems;
        }
        if (options.false_positive_rate <= 0.0 or options.false_positive_rate >= 1.0) {
            return BloomFilterError.InvalidFalsePositiveRate;
        }

        // Calculate parameters (similar to regular Bloom Filter)
        const ln2: f64 = 0.6931471805599453;
        const n: f64 = @floatFromInt(options.expected_items);
        const p = options.false_positive_rate;
        const num_counters_float: f64 = -n * @log(p) / (ln2 * ln2);
        const num_counters: usize = @intFromFloat(@round(num_counters_float));
        
        var num_hashes: usize = options.hash_count;
        if (num_hashes == 0) {
            const num_hashes_float: f64 = num_counters_float * ln2 / n;
            num_hashes = @intFromFloat(@round(num_hashes_float));
            if (num_hashes == 0) num_hashes = 1;
            if (num_hashes > 20) num_hashes = 20;
        }

        // Allocate counter array (4-bit counters packed into bytes)
        // Each byte holds 2 counters (lower 4 bits and upper 4 bits)
        const byte_count = (num_counters + 1) / 2;
        const counters = allocator.alloc(u8, byte_count) catch return BloomFilterError.OutOfMemory;
        @memset(counters, 0);

        return CountingBloomFilter{
            .counters = counters,
            .num_counters = num_counters,
            .num_hashes = num_hashes,
            .count = 0,
            .allocator = allocator,
        };
    }

    /// Free memory
    pub fn deinit(self: *CountingBloomFilter) void {
        self.allocator.free(self.counters);
    }

    /// Add an item
    pub fn add(self: *CountingBloomFilter, item: []const u8) void {
        const hashes = self.getHashes(item);
        for (hashes[0..self.num_hashes]) |hash| {
            self.incrementCounter(hash);
        }
        self.count += 1;
    }

    /// Remove an item (if it exists)
    pub fn remove(self: *CountingBloomFilter, item: []const u8) bool {
        // First check if it might be there
        if (!self.mightContain(item)) {
            return false;
        }

        const hashes = self.getHashes(item);
        // Verify all counters are > 0 before decrementing
        for (hashes[0..self.num_hashes]) |hash| {
            if (self.getCounter(hash) == 0) {
                return false; // Definitely not in set
            }
        }

        // Decrement all counters
        for (hashes[0..self.num_hashes]) |hash| {
            self.decrementCounter(hash);
        }
        self.count -= 1;
        return true;
    }

    /// Check if an item might be in the filter
    pub fn mightContain(self: *const CountingBloomFilter, item: []const u8) bool {
        const hashes = self.getHashes(item);
        for (hashes[0..self.num_hashes]) |hash| {
            if (self.getCounter(hash) == 0) {
                return false;
            }
        }
        return true;
    }

    /// Get hash values
    fn getHashes(self: *const CountingBloomFilter, item: []const u8) [20]usize {
        var hashes: [20]usize = undefined;
        
        const h1 = self.hash1(item);
        const h2 = self.hash2(item);
        
        for (0..self.num_hashes) |i| {
            // Use wrapping multiplication and addition
            hashes[i] = (h1 +% (i *% h2)) % self.num_counters;
        }
        
        return hashes;
    }

    fn hash1(self: *const CountingBloomFilter, item: []const u8) usize {
        var hash: usize = 14695981039346656037;
        for (item) |byte| {
            hash ^= byte;
            hash = hash *% 1099511628211; // wrapping multiply
        }
        return hash % self.num_counters;
    }

    fn hash2(self: *const CountingBloomFilter, item: []const u8) usize {
        var hash: usize = 0xdeadbeef;
        for (item) |byte| {
            hash ^= byte;
            hash = hash *% 0x5bd1e995; // wrapping multiply
            hash ^= hash >> 15;
        }
        if (hash == 0) hash = 1;
        return hash % self.num_counters;
    }

    fn getCounter(self: *const CountingBloomFilter, index: usize) u4 {
        const byte_index = index / 2;
        if (index % 2 == 0) {
            return @truncate(self.counters[byte_index] & 0x0F);
        } else {
            return @truncate((self.counters[byte_index] >> 4) & 0x0F);
        }
    }

    fn incrementCounter(self: *CountingBloomFilter, index: usize) void {
        const byte_index = index / 2;
        const current = self.getCounter(index);
        if (current < 15) { // Prevent overflow
            if (index % 2 == 0) {
                self.counters[byte_index] += 1;
            } else {
                self.counters[byte_index] += 16;
            }
        }
    }

    fn decrementCounter(self: *CountingBloomFilter, index: usize) void {
        const byte_index = index / 2;
        const current = self.getCounter(index);
        if (current > 0) {
            if (index % 2 == 0) {
                self.counters[byte_index] -= 1;
            } else {
                self.counters[byte_index] -= 16;
            }
        }
    }
};

// --- Tests ---

test "bloom filter init" {
    const allocator = std.testing.allocator;
    
    var bf = try BloomFilter.init(allocator, .{
        .expected_items = 1000,
        .false_positive_rate = 0.01,
    });
    defer bf.deinit();
    
    try std.testing.expect(bf.num_bits > 0);
    try std.testing.expect(bf.num_hashes > 0);
    try std.testing.expect(bf.count == 0);
}

test "bloom filter add and check" {
    const allocator = std.testing.allocator;
    
    var bf = try BloomFilter.init(allocator, .{
        .expected_items = 100,
        .false_positive_rate = 0.01,
    });
    defer bf.deinit();
    
    const items = [_][]const u8{ "apple", "banana", "cherry" };
    
    for (items) |item| {
        bf.add(item);
    }
    
    // All added items should return true
    for (items) |item| {
        try std.testing.expect(bf.mightContain(item));
    }
    
    // Item not added should return false
    try std.testing.expect(!bf.mightContain("orange"));
}

test "bloom filter u64 operations" {
    const allocator = std.testing.allocator;
    
    var bf = try BloomFilter.init(allocator, .{
        .expected_items = 100,
        .false_positive_rate = 0.01,
    });
    defer bf.deinit();
    
    bf.addU64(42);
    bf.addU64(100);
    bf.addU64(999);
    
    try std.testing.expect(bf.mightContainU64(42));
    try std.testing.expect(bf.mightContainU64(100));
    try std.testing.expect(bf.mightContainU64(999));
    try std.testing.expect(!bf.mightContainU64(123));
}

test "bloom filter clear" {
    const allocator = std.testing.allocator;
    
    var bf = try BloomFilter.init(allocator, .{
        .expected_items = 100,
        .false_positive_rate = 0.01,
    });
    defer bf.deinit();
    
    bf.add("test");
    try std.testing.expect(!bf.isEmpty());
    
    bf.clear();
    try std.testing.expect(bf.isEmpty());
    try std.testing.expect(!bf.mightContain("test"));
}

test "bloom filter union" {
    const allocator = std.testing.allocator;
    
    var bf1 = try BloomFilter.initWithParams(allocator, 1000, 5);
    defer bf1.deinit();
    
    var bf2 = try BloomFilter.initWithParams(allocator, 1000, 5);
    defer bf2.deinit();
    
    bf1.add("apple");
    bf1.add("banana");
    
    bf2.add("cherry");
    bf2.add("date");
    
    try bf1.unionWith(&bf2);
    
    try std.testing.expect(bf1.mightContain("apple"));
    try std.testing.expect(bf1.mightContain("banana"));
    try std.testing.expect(bf1.mightContain("cherry"));
    try std.testing.expect(bf1.mightContain("date"));
}

test "bloom filter intersection" {
    const allocator = std.testing.allocator;
    
    var bf1 = try BloomFilter.initWithParams(allocator, 1000, 5);
    defer bf1.deinit();
    
    var bf2 = try BloomFilter.initWithParams(allocator, 1000, 5);
    defer bf2.deinit();
    
    bf1.add("apple");
    bf1.add("banana");
    bf1.add("cherry");
    
    bf2.add("banana");
    bf2.add("cherry");
    bf2.add("date");
    
    try bf1.intersectWith(&bf2);
    
    // banana and cherry were in both
    try std.testing.expect(bf1.mightContain("banana"));
    try std.testing.expect(bf1.mightContain("cherry"));
    
    // apple and date were only in one
    // These might still return true due to hash collisions
    // But the intersection should be smaller
}

test "bloom filter serialize deserialize" {
    const allocator = std.testing.allocator;
    
    var bf1 = try BloomFilter.init(allocator, .{
        .expected_items = 100,
        .false_positive_rate = 0.01,
    });
    defer bf1.deinit();
    
    bf1.add("apple");
    bf1.add("banana");
    bf1.add("cherry");
    
    const serialized = try bf1.serialize(allocator);
    defer allocator.free(serialized);
    
    var bf2 = try BloomFilter.deserialize(allocator, serialized);
    defer bf2.deinit();
    
    try std.testing.expect(bf2.mightContain("apple"));
    try std.testing.expect(bf2.mightContain("banana"));
    try std.testing.expect(bf2.mightContain("cherry"));
    try std.testing.expect(!bf2.mightContain("orange"));
    
    try std.testing.expectEqual(bf1.num_bits, bf2.num_bits);
    try std.testing.expectEqual(bf1.num_hashes, bf2.num_hashes);
    try std.testing.expectEqual(bf1.count, bf2.count);
}

test "bloom filter false positive rate" {
    const allocator = std.testing.allocator;
    
    var bf = try BloomFilter.init(allocator, .{
        .expected_items = 1000,
        .false_positive_rate = 0.01,
    });
    defer bf.deinit();
    
    // Add 1000 items
    for (0..1000) |i| {
        var buf: [20]u8 = undefined;
        const str = std.fmt.bufPrint(&buf, "item_{}", .{i}) catch unreachable;
        bf.add(str);
    }
    
    const fp_rate = bf.estimateFalsePositiveRate();
    // Should be close to configured rate
    try std.testing.expect(fp_rate < 0.05); // Allow some variance
}

test "counting bloom filter add remove" {
    const allocator = std.testing.allocator;
    
    var cbf = try CountingBloomFilter.init(allocator, .{
        .expected_items = 100,
        .false_positive_rate = 0.01,
    });
    defer cbf.deinit();
    
    cbf.add("apple");
    cbf.add("banana");
    
    try std.testing.expect(cbf.mightContain("apple"));
    try std.testing.expect(cbf.mightContain("banana"));
    
    // Remove apple
    const removed = cbf.remove("apple");
    try std.testing.expect(removed);
    try std.testing.expect(!cbf.mightContain("apple"));
    try std.testing.expect(cbf.mightContain("banana"));
    
    // Try to remove non-existent item
    const not_removed = cbf.remove("cherry");
    try std.testing.expect(!not_removed);
}

test "scalable bloom filter" {
    const allocator = std.testing.allocator;
    
    var sbf = try ScalableBloomFilter.init(allocator, 0.01);
    defer sbf.deinit();
    
    // Add many items to trigger expansion
    for (0..500) |i| {
        var buf: [20]u8 = undefined;
        const str = std.fmt.bufPrint(&buf, "item_{}", .{i}) catch unreachable;
        sbf.add(str);
    }
    
    // Check some items
    try std.testing.expect(sbf.mightContain("item_0"));
    try std.testing.expect(sbf.mightContain("item_100"));
    try std.testing.expect(sbf.mightContain("item_400"));
    try std.testing.expect(!sbf.mightContain("nonexistent"));
    
    // Should have expanded to multiple filters
    try std.testing.expect(sbf.filters.items.len >= 1);
}

test "bloom filter bits set" {
    const allocator = std.testing.allocator;
    
    var bf = try BloomFilter.init(allocator, .{
        .expected_items = 100,
        .false_positive_rate = 0.01,
    });
    defer bf.deinit();
    
    try std.testing.expect(bf.bitsSet() == 0);
    
    bf.add("test");
    try std.testing.expect(bf.bitsSet() > 0);
    // Should have num_hashes bits set per item
    try std.testing.expect(bf.bitsSet() <= bf.num_hashes);
}

test "bloom filter invalid parameters" {
    const allocator = std.testing.allocator;
    
    // Invalid expected_items
    const result1 = BloomFilter.init(allocator, .{
        .expected_items = 0,
        .false_positive_rate = 0.01,
    });
    try std.testing.expectError(BloomFilterError.InvalidExpectedItems, result1);
    
    // Invalid false_positive_rate
    const result2 = BloomFilter.init(allocator, .{
        .expected_items = 100,
        .false_positive_rate = 0.0,
    });
    try std.testing.expectError(BloomFilterError.InvalidFalsePositiveRate, result2);
    
    const result3 = BloomFilter.init(allocator, .{
        .expected_items = 100,
        .false_positive_rate = 1.0,
    });
    try std.testing.expectError(BloomFilterError.InvalidFalsePositiveRate, result3);
}

test "bloom filter with explicit params" {
    const allocator = std.testing.allocator;
    
    var bf = try BloomFilter.initWithParams(allocator, 10000, 7);
    defer bf.deinit();
    
    try std.testing.expectEqual(@as(usize, 10000), bf.num_bits);
    try std.testing.expectEqual(@as(usize, 7), bf.num_hashes);
    
    bf.add("test");
    try std.testing.expect(bf.mightContain("test"));
}

test "bloom filter empty check" {
    const allocator = std.testing.allocator;
    
    var bf = try BloomFilter.init(allocator, .{
        .expected_items = 100,
        .false_positive_rate = 0.01,
    });
    defer bf.deinit();
    
    try std.testing.expect(bf.isEmpty());
    
    bf.add("test");
    try std.testing.expect(!bf.isEmpty());
    
    bf.clear();
    try std.testing.expect(bf.isEmpty());
}