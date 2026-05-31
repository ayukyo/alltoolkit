/// Nanoid Utils - Compact, URL-friendly unique ID generator
/// 
/// A tiny, URL-safe unique ID generator similar to YouTube video IDs.
/// 
/// Features:
/// - Zero external dependencies
/// - Configurable alphabet and ID length
/// - URL-safe (uses alphanumeric characters by default)
/// - Efficient random bytes utilization

const std = @import("std");

/// Default alphabet: URL-safe characters (no + / or =)
pub const DEFAULT_ALPHABET: []const u8 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";

/// Default ID length
pub const DEFAULT_LENGTH: u8 = 21;

/// Configuration for NanoidGenerator
pub const NanoidConfig = struct {
    alphabet: []const u8 = DEFAULT_ALPHABET,
    length: u8 = DEFAULT_LENGTH,
};

/// Nanoid Generator
pub fn NanoidGenerator(comptime T: type) type {
    return struct {
        allocator: std.mem.Allocator,
        rng: *T,
        config: NanoidConfig,
        alphabet_bytes: []u8,

        const Self = @This();

        pub fn init(allocator: std.mem.Allocator, rng: *T, config: NanoidConfig) !Self {
            if (config.alphabet.len < 1 or config.alphabet.len > 255) {
                return error.InvalidAlphabet;
            }
            if (config.length == 0) {
                return error.InvalidLength;
            }

            const alphabet_bytes = try allocator.alloc(u8, config.alphabet.len);
            @memcpy(alphabet_bytes, config.alphabet);

            return Self{
                .allocator = allocator,
                .rng = rng,
                .config = config,
                .alphabet_bytes = alphabet_bytes,
            };
        }

        pub fn generate(self: *Self) ![]u8 {
            const id = try self.allocator.alloc(u8, self.config.length);
            errdefer self.allocator.free(id);

            const alphabet_len = self.alphabet_bytes.len;
            for (id) |*c| {
                var v = self.rng.*.next();
                while (v >= @as(u64, alphabet_len) * (@as(u64, 256) / @as(u64, alphabet_len))) {
                    v = self.rng.*.next();
                }
                c.* = self.alphabet_bytes[@as(usize, v % @as(u64, alphabet_len))];
            }
            return id;
        }

        pub fn generateWithSize(self: *Self, size: u8) ![]u8 {
            if (size == 0) return error.InvalidLength;
            const id = try self.allocator.alloc(u8, size);
            errdefer self.allocator.free(id);

            const alphabet_len = self.alphabet_bytes.len;
            for (id) |*c| {
                var v = self.rng.*.next();
                while (v >= @as(u64, alphabet_len) * (@as(u64, 256) / @as(u64, alphabet_len))) {
                    v = self.rng.*.next();
                }
                c.* = self.alphabet_bytes[@as(usize, v % @as(u64, alphabet_len))];
            }
            return id;
        }

        pub fn getAlphabet(self: *const Self) []const u8 {
            return self.config.alphabet;
        }

        pub fn getLength(self: *const Self) u8 {
            return self.config.length;
        }

        pub fn deinit(self: *Self) void {
            self.allocator.free(self.alphabet_bytes);
        }
    };
}

/// Simple helper to generate a nanoid
pub fn generateNanoid(allocator: std.mem.Allocator, rng: anytype, alphabet: []const u8, length: u8) ![]u8 {
    const config = NanoidConfig{ .alphabet = alphabet, .length = length };
    const T = @TypeOf(rng.*);
    var generator = try NanoidGenerator(T).init(allocator, rng, config);
    defer generator.deinit();
    return generator.generate();
}

/// Generate with default alphabet
pub fn generateDefaultNanoid(allocator: std.mem.Allocator, rng: anytype, length: u8) ![]u8 {
    return generateNanoid(allocator, rng, DEFAULT_ALPHABET, length);
}

test "NanoidGenerator basic generation" {
    var rng = std.rand.Xoshiro256.init(12345);
    var gen = try NanoidGenerator(@TypeOf(rng)).init(std.testing.allocator, &rng, .{});
    defer gen.deinit();
    const id = try gen.generate();
    defer std.testing.allocator.free(id);
    try std.testing.expectEqual(@as(usize, 21), id.len);
    for (id) |c| {
        try std.testing.expect(std.mem.indexOfScalar(u8, DEFAULT_ALPHABET, c) != null);
    }
}

test "NanoidGenerator custom alphabet" {
    var rng = std.rand.Xoshiro256.init(67890);
    var gen = try NanoidGenerator(@TypeOf(rng)).init(std.testing.allocator, &rng, .{
        .alphabet = "ABC123",
        .length = 10,
    });
    defer gen.deinit();
    const id = try gen.generate();
    defer std.testing.allocator.free(id);
    try std.testing.expectEqual(@as(usize, 10), id.len);
    for (id) |c| {
        try std.testing.expect(std.mem.indexOfScalar(u8, "ABC123", c) != null);
    }
}

test "NanoidGenerator uniqueness" {
    var rng = std.rand.Xoshiro256.init(11111);
    var gen = try NanoidGenerator(@TypeOf(rng)).init(std.testing.allocator, &rng, .{
        .length = 8,
    });
    defer gen.deinit();
    
    var ids: [10][]u8 = undefined;
    var count: usize = 0;
    while (count < 10) : (count += 1) {
        const id = try gen.generate();
        for (ids[0..count]) |prev| {
            try std.testing.expect(!std.mem.eql(u8, id, prev));
        }
        ids[count] = id;
    }
    for (ids) |id| std.testing.allocator.free(id);
}

test "generateDefaultNanoid helper" {
    var rng = std.rand.Xoshiro256.init(99999);
    const id = try generateDefaultNanoid(std.testing.allocator, &rng, 16);
    defer std.testing.allocator.free(id);
    try std.testing.expectEqual(@as(usize, 16), id.len);
}