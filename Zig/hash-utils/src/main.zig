const std = @import("std");
const crypto = std.crypto;
const fmt = std.fmt;

/// Hash algorithm types
pub const HashAlgorithm = enum {
    md5,
    sha1,
    sha256,
    sha512,

    /// Get the digest size in bytes for this algorithm
    pub fn digestSize(self: HashAlgorithm) usize {
        return switch (self) {
            .md5 => 16,
            .sha1 => 20,
            .sha256 => 32,
            .sha512 => 64,
        };
    }

    /// Get the hex string length for this algorithm
    pub fn hexLen(self: HashAlgorithm) usize {
        return self.digestSize() * 2;
    }
};

/// Errors that can occur during hash operations
pub const HashError = error{
    /// Output buffer too small
    BufferTooSmall,
    /// Memory allocation failed
    OutOfMemory,
    /// Invalid hex string
    InvalidHex,
};

// --- MD5 Implementation ---

/// MD5 hash context
pub const Md5 = struct {
    const Self = @This();
    const digest_len = 16;
    
    ctx: crypto.hash.Md5,

    /// Initialize a new MD5 context
    pub fn init() Self {
        return .{
            .ctx = crypto.hash.Md5.init(.{}),
        };
    }

    /// Update the hash with additional data
    pub fn update(self: *Self, data: []const u8) void {
        self.ctx.update(data);
    }

    /// Finalize and get the digest
    pub fn final(self: *Self, out: *[digest_len]u8) void {
        self.ctx.final(out);
    }

    /// Compute MD5 hash of data in one call
    pub fn hash(data: []const u8) [digest_len]u8 {
        var result: [digest_len]u8 = undefined;
        crypto.hash.Md5.hash(data, &result, .{});
        return result;
    }

    /// Compute MD5 hash and return as hex string
    pub fn hashHex(allocator: std.mem.Allocator, data: []const u8) HashError![]u8 {
        const digest = hash(data);
        return toHex(allocator, &digest);
    }
};

// --- SHA-1 Implementation ---

/// SHA-1 hash context
pub const Sha1 = struct {
    const Self = @This();
    const digest_len = 20;
    
    ctx: crypto.hash.Sha1,

    /// Initialize a new SHA-1 context
    pub fn init() Self {
        return .{
            .ctx = crypto.hash.Sha1.init(.{}),
        };
    }

    /// Update the hash with additional data
    pub fn update(self: *Self, data: []const u8) void {
        self.ctx.update(data);
    }

    /// Finalize and get the digest
    pub fn final(self: *Self, out: *[digest_len]u8) void {
        self.ctx.final(out);
    }

    /// Compute SHA-1 hash of data in one call
    pub fn hash(data: []const u8) [digest_len]u8 {
        var result: [digest_len]u8 = undefined;
        crypto.hash.Sha1.hash(data, &result, .{});
        return result;
    }

    /// Compute SHA-1 hash and return as hex string
    pub fn hashHex(allocator: std.mem.Allocator, data: []const u8) HashError![]u8 {
        const digest = hash(data);
        return toHex(allocator, &digest);
    }
};

// --- SHA-256 Implementation ---

/// SHA-256 hash context
pub const Sha256 = struct {
    const Self = @This();
    const digest_len = 32;
    
    ctx: crypto.hash.sha2.Sha256,

    /// Initialize a new SHA-256 context
    pub fn init() Self {
        return .{
            .ctx = crypto.hash.sha2.Sha256.init(.{}),
        };
    }

    /// Update the hash with additional data
    pub fn update(self: *Self, data: []const u8) void {
        self.ctx.update(data);
    }

    /// Finalize and get the digest
    pub fn final(self: *Self, out: *[digest_len]u8) void {
        self.ctx.final(out);
    }

    /// Compute SHA-256 hash of data in one call
    pub fn hash(data: []const u8) [digest_len]u8 {
        var result: [digest_len]u8 = undefined;
        crypto.hash.sha2.Sha256.hash(data, &result, .{});
        return result;
    }

    /// Compute SHA-256 hash and return as hex string
    pub fn hashHex(allocator: std.mem.Allocator, data: []const u8) HashError![]u8 {
        const digest = hash(data);
        return toHex(allocator, &digest);
    }
};

// --- SHA-512 Implementation ---

/// SHA-512 hash context
pub const Sha512 = struct {
    const Self = @This();
    const digest_len = 64;
    
    ctx: crypto.hash.sha2.Sha512,

    /// Initialize a new SHA-512 context
    pub fn init() Self {
        return .{
            .ctx = crypto.hash.sha2.Sha512.init(.{}),
        };
    }

    /// Update the hash with additional data
    pub fn update(self: *Self, data: []const u8) void {
        self.ctx.update(data);
    }

    /// Finalize and get the digest
    pub fn final(self: *Self, out: *[digest_len]u8) void {
        self.ctx.final(out);
    }

    /// Compute SHA-512 hash of data in one call
    pub fn hash(data: []const u8) [digest_len]u8 {
        var result: [digest_len]u8 = undefined;
        crypto.hash.sha2.Sha512.hash(data, &result, .{});
        return result;
    }

    /// Compute SHA-512 hash and return as hex string
    pub fn hashHex(allocator: std.mem.Allocator, data: []const u8) HashError![]u8 {
        const digest = hash(data);
        return toHex(allocator, &digest);
    }
};

// --- Generic Hash Function ---

/// Compute hash using specified algorithm
pub fn hashWith(allocator: std.mem.Allocator, data: []const u8, algorithm: HashAlgorithm) HashError![]u8 {
    return switch (algorithm) {
        .md5 => Md5.hashHex(allocator, data),
        .sha1 => Sha1.hashHex(allocator, data),
        .sha256 => Sha256.hashHex(allocator, data),
        .sha512 => Sha512.hashHex(allocator, data),
    };
}

/// Compute hash into a buffer using specified algorithm
pub fn hashInto(out: []u8, data: []const u8, algorithm: HashAlgorithm) HashError!usize {
    const required_len = algorithm.digestSize();
    if (out.len < required_len) {
        return HashError.BufferTooSmall;
    }

    switch (algorithm) {
        .md5 => {
            const digest = Md5.hash(data);
            @memcpy(out[0..required_len], &digest);
        },
        .sha1 => {
            const digest = Sha1.hash(data);
            @memcpy(out[0..required_len], &digest);
        },
        .sha256 => {
            const digest = Sha256.hash(data);
            @memcpy(out[0..required_len], &digest);
        },
        .sha512 => {
            const digest = Sha512.hash(data);
            @memcpy(out[0..required_len], &digest);
        },
    }

    return required_len;
}

/// Compute hash as hex string into a buffer
pub fn hashHexInto(out: []u8, data: []const u8, algorithm: HashAlgorithm) HashError!usize {
    const required_len = algorithm.hexLen();
    if (out.len < required_len) {
        return HashError.BufferTooSmall;
    }

    var digest: [64]u8 = undefined;
    const digest_len = try hashInto(&digest, data, algorithm);
    
    _ = fmt.bufPrint(out[0..required_len], "{}", .{fmt.fmtSliceHexLower(digest[0..digest_len])}) catch {
        return HashError.BufferTooSmall;
    };

    return required_len;
}

// --- Utility Functions ---

/// Convert bytes to lowercase hex string
pub fn toHex(allocator: std.mem.Allocator, data: []const u8) HashError![]u8 {
    const hex_len = data.len * 2;
    const result = allocator.alloc(u8, hex_len) catch return HashError.OutOfMemory;
    
    _ = fmt.bufPrint(result, "{}", .{fmt.fmtSliceHexLower(data)}) catch {
        allocator.free(result);
        return HashError.BufferTooSmall;
    };
    
    return result;
}

/// Convert bytes to uppercase hex string
pub fn toHexUpper(allocator: std.mem.Allocator, data: []const u8) HashError![]u8 {
    const hex_len = data.len * 2;
    const result = allocator.alloc(u8, hex_len) catch return HashError.OutOfMemory;
    
    _ = fmt.bufPrint(result, "{}", .{fmt.fmtSliceHexUpper(data)}) catch {
        allocator.free(result);
        return HashError.BufferTooSmall;
    };
    
    return result;
}

/// Convert hex string to bytes
pub fn fromHex(allocator: std.mem.Allocator, hex: []const u8) HashError![]u8 {
    if (hex.len % 2 != 0) {
        return HashError.InvalidHex;
    }

    const result_len = hex.len / 2;
    const result = allocator.alloc(u8, result_len) catch return HashError.OutOfMemory;
    errdefer allocator.free(result);

    for (0..result_len) |i| {
        const hi = charToNibble(hex[i * 2]) catch return HashError.InvalidHex;
        const lo = charToNibble(hex[i * 2 + 1]) catch return HashError.InvalidHex;
        result[i] = (hi << 4) | lo;
    }

    return result;
}

/// Check if a character is a hex digit
fn isHexDigit(c: u8) bool {
    return switch (c) {
        '0'...'9', 'a'...'f', 'A'...'F' => true,
        else => false,
    };
}

/// Check if a string is a valid hex string
pub fn isValidHex(hex: []const u8) bool {
    if (hex.len % 2 != 0) {
        return false;
    }

    for (hex) |c| {
        if (!isHexDigit(c)) {
            return false;
        }
    }

    return true;
}

// --- HMAC Implementation ---

/// HMAC-SHA256
pub const HmacSha256 = struct {
    const Self = @This();
    const digest_len = 32;
    
    ctx: crypto.auth.hmac.sha2.HmacSha256,

    /// Initialize a new HMAC-SHA256 context
    pub fn init(key: []const u8) Self {
        return .{
            .ctx = crypto.auth.hmac.sha2.HmacSha256.init(key),
        };
    }

    /// Update the HMAC with additional data
    pub fn update(self: *Self, data: []const u8) void {
        self.ctx.update(data);
    }

    /// Finalize and get the digest
    pub fn final(self: *Self, out: *[digest_len]u8) void {
        self.ctx.final(out);
    }

    /// Compute HMAC-SHA256 in one call
    pub fn hash(key: []const u8, data: []const u8) [digest_len]u8 {
        var result: [digest_len]u8 = undefined;
        crypto.auth.hmac.sha2.HmacSha256.create(&result, data, key);
        return result;
    }

    /// Compute HMAC-SHA256 and return as hex string
    pub fn hashHex(allocator: std.mem.Allocator, key: []const u8, data: []const u8) HashError![]u8 {
        const digest = hash(key, data);
        return toHex(allocator, &digest);
    }
};

/// HMAC-SHA512
pub const HmacSha512 = struct {
    const Self = @This();
    const digest_len = 64;
    
    ctx: crypto.auth.hmac.sha2.HmacSha512,

    /// Initialize a new HMAC-SHA512 context
    pub fn init(key: []const u8) Self {
        return .{
            .ctx = crypto.auth.hmac.sha2.HmacSha512.init(key),
        };
    }

    /// Update the HMAC with additional data
    pub fn update(self: *Self, data: []const u8) void {
        self.ctx.update(data);
    }

    /// Finalize and get the digest
    pub fn final(self: *Self, out: *[digest_len]u8) void {
        self.ctx.final(out);
    }

    /// Compute HMAC-SHA512 in one call
    pub fn hash(key: []const u8, data: []const u8) [digest_len]u8 {
        var result: [digest_len]u8 = undefined;
        crypto.auth.hmac.sha2.HmacSha512.create(&result, data, key);
        return result;
    }

    /// Compute HMAC-SHA512 and return as hex string
    pub fn hashHex(allocator: std.mem.Allocator, key: []const u8, data: []const u8) HashError![]u8 {
        const digest = hash(key, data);
        return toHex(allocator, &digest);
    }
};

// --- PBKDF2 Implementation ---

/// PBKDF2-HMAC-SHA256
pub fn pbkdf2Sha256(allocator: std.mem.Allocator, password: []const u8, salt: []const u8, iterations: u32, key_len: usize) HashError![]u8 {
    const result = allocator.alloc(u8, key_len) catch return HashError.OutOfMemory;
    errdefer allocator.free(result);

    crypto.pwhash.pbkdf2(result, password, salt, iterations, crypto.auth.hmac.sha2.HmacSha256) catch {
        return HashError.OutOfMemory;
    };

    return result;
}

/// PBKDF2-HMAC-SHA256 returning hex string
pub fn pbkdf2Sha256Hex(allocator: std.mem.Allocator, password: []const u8, salt: []const u8, iterations: u32, key_len: usize) HashError![]u8 {
    const derived = try pbkdf2Sha256(allocator, password, salt, iterations, key_len);
    defer allocator.free(derived);
    return toHex(allocator, derived);
}

// --- Helper Functions ---

fn charToNibble(c: u8) HashError!u8 {
    return switch (c) {
        '0'...'9' => c - '0',
        'a'...'f' => c - 'a' + 10,
        'A'...'F' => c - 'A' + 10,
        else => HashError.InvalidHex,
    };
}

// --- Tests ---

test "MD5 basic" {
    const allocator = std.testing.allocator;

    // Test vectors from RFC 1321
    const test_cases = [_]struct {
        input: []const u8,
        expected: []const u8,
    }{
        .{ .input = "", .expected = "d41d8cd98f00b204e9800998ecf8427e" },
        .{ .input = "a", .expected = "0cc175b9c0f1b6a831c399e269772661" },
        .{ .input = "abc", .expected = "900150983cd24fb0d6963f7d28e17f72" },
        .{ .input = "message digest", .expected = "f96b697d7cb7938d525a2f31aaf161d0" },
        .{ .input = "abcdefghijklmnopqrstuvwxyz", .expected = "c3fcd3d76192e4007dfb496cca67e13b" },
    };

    for (test_cases) |tc| {
        const result = try Md5.hashHex(allocator, tc.input);
        defer allocator.free(result);
        try std.testing.expectEqualStrings(tc.expected, result);
    }
}

test "SHA-1 basic" {
    const allocator = std.testing.allocator;

    const test_cases = [_]struct {
        input: []const u8,
        expected: []const u8,
    }{
        .{ .input = "", .expected = "da39a3ee5e6b4b0d3255bfef95601890afd80709" },
        .{ .input = "a", .expected = "86f7e437faa5a7fce15d1ddcb9eaeaea377667b8" },
        .{ .input = "abc", .expected = "a9993e364706816aba3e25717850c26c9cd0d89d" },
        .{ .input = "hello world", .expected = "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed" },
    };

    for (test_cases) |tc| {
        const result = try Sha1.hashHex(allocator, tc.input);
        defer allocator.free(result);
        try std.testing.expectEqualStrings(tc.expected, result);
    }
}

test "SHA-256 basic" {
    const allocator = std.testing.allocator;

    const test_cases = [_]struct {
        input: []const u8,
        expected: []const u8,
    }{
        .{ .input = "", .expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" },
        .{ .input = "a", .expected = "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb" },
        .{ .input = "abc", .expected = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" },
        .{ .input = "hello world", .expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9" },
    };

    for (test_cases) |tc| {
        const result = try Sha256.hashHex(allocator, tc.input);
        defer allocator.free(result);
        try std.testing.expectEqualStrings(tc.expected, result);
    }
}

test "SHA-512 basic" {
    const allocator = std.testing.allocator;

    const test_cases = [_]struct {
        input: []const u8,
        expected: []const u8,
    }{
        .{ .input = "", .expected = "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e" },
        .{ .input = "a", .expected = "1f40fc92da241694750979ee6cf582f2d5d7d28e18335de05abc54d0560e0f5302860c652bf08d560252aa5e74210546f369fbbbce8c12cfc7957b2652fe9a75" },
        .{ .input = "abc", .expected = "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f" },
    };

    for (test_cases) |tc| {
        const result = try Sha512.hashHex(allocator, tc.input);
        defer allocator.free(result);
        try std.testing.expectEqualStrings(tc.expected, result);
    }
}

test "incremental hashing" {
    const allocator = std.testing.allocator;

    // Test incremental MD5
    var md5_ctx = Md5.init();
    md5_ctx.update("hello");
    md5_ctx.update(" ");
    md5_ctx.update("world");
    var md5_digest: [16]u8 = undefined;
    md5_ctx.final(&md5_digest);

    const expected_md5 = try Md5.hashHex(allocator, "hello world");
    defer allocator.free(expected_md5);

    const result_md5 = try toHex(allocator, &md5_digest);
    defer allocator.free(result_md5);

    try std.testing.expectEqualStrings(expected_md5, result_md5);

    // Test incremental SHA-256
    var sha256_ctx = Sha256.init();
    sha256_ctx.update("hello");
    sha256_ctx.update(" ");
    sha256_ctx.update("world");
    var sha256_digest: [32]u8 = undefined;
    sha256_ctx.final(&sha256_digest);

    const expected_sha256 = try Sha256.hashHex(allocator, "hello world");
    defer allocator.free(expected_sha256);

    const result_sha256 = try toHex(allocator, &sha256_digest);
    defer allocator.free(result_sha256);

    try std.testing.expectEqualStrings(expected_sha256, result_sha256);
}

test "hashWith generic function" {
    const allocator = std.testing.allocator;

    const data = "test";

    const md5_result = try hashWith(allocator, data, .md5);
    defer allocator.free(md5_result);
    try std.testing.expectEqualStrings("098f6bcd4621d373cade4e832627b4f6", md5_result);

    const sha1_result = try hashWith(allocator, data, .sha1);
    defer allocator.free(sha1_result);
    try std.testing.expectEqualStrings("a94a8fe5ccb19ba61c4c0873d391e987982fbbd3", sha1_result);

    const sha256_result = try hashWith(allocator, data, .sha256);
    defer allocator.free(sha256_result);
    try std.testing.expectEqualStrings("9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08", sha256_result);

    const sha512_result = try hashWith(allocator, data, .sha512);
    defer allocator.free(sha512_result);
    try std.testing.expectEqualStrings("ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff", sha512_result);
}

test "HMAC-SHA256" {
    const allocator = std.testing.allocator;

    // Test vectors from RFC 4231
    const key = "key";
    const data = "The quick brown fox jumps over the lazy dog";
    const expected = "f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8";

    const result = try HmacSha256.hashHex(allocator, key, data);
    defer allocator.free(result);

    try std.testing.expectEqualStrings(expected, result);
}

test "HMAC-SHA512" {
    const allocator = std.testing.allocator;

    const key = "secret key";
    const data = "test data";
    const result = try HmacSha512.hashHex(allocator, key, data);
    defer allocator.free(result);

    // Result should be 128 hex characters (64 bytes)
    try std.testing.expectEqual(@as(usize, 128), result.len);
}

test "toHex and fromHex roundtrip" {
    const allocator = std.testing.allocator;

    const bytes = [_]u8{ 0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef };

    const hex = try toHex(allocator, &bytes);
    defer allocator.free(hex);

    try std.testing.expectEqualStrings("0123456789abcdef", hex);

    const decoded = try fromHex(allocator, hex);
    defer allocator.free(decoded);

    try std.testing.expectEqualSlices(u8, &bytes, decoded);
}

test "toHexUpper" {
    const allocator = std.testing.allocator;

    const bytes = [_]u8{ 0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef };

    const hex = try toHexUpper(allocator, &bytes);
    defer allocator.free(hex);

    try std.testing.expectEqualStrings("0123456789ABCDEF", hex);
}

test "isValidHex" {
    try std.testing.expect(isValidHex("0123456789abcdef"));
    try std.testing.expect(isValidHex("0123456789ABCDEF"));
    try std.testing.expect(isValidHex(""));
    try std.testing.expect(!isValidHex("invalid"));
    try std.testing.expect(!isValidHex("01234")); // Odd length
    try std.testing.expect(!isValidHex("0123 g567")); // Space in middle
}

test "hashInto buffer operations" {
    var buffer: [64]u8 = undefined;

    const sha256_len = try hashInto(&buffer, "test", .sha256);
    try std.testing.expectEqual(@as(usize, 32), sha256_len);

    const sha512_len = try hashInto(&buffer, "test", .sha512);
    try std.testing.expectEqual(@as(usize, 64), sha512_len);
}

test "hashHexInto buffer operations" {
    var buffer: [128]u8 = undefined;

    const sha256_len = try hashHexInto(&buffer, "test", .sha256);
    try std.testing.expectEqual(@as(usize, 64), sha256_len);

    const sha512_len = try hashHexInto(&buffer, "test", .sha512);
    try std.testing.expectEqual(@as(usize, 128), sha512_len);
}

test "HashAlgorithm enum" {
    try std.testing.expectEqual(@as(usize, 16), HashAlgorithm.md5.digestSize());
    try std.testing.expectEqual(@as(usize, 20), HashAlgorithm.sha1.digestSize());
    try std.testing.expectEqual(@as(usize, 32), HashAlgorithm.sha256.digestSize());
    try std.testing.expectEqual(@as(usize, 64), HashAlgorithm.sha512.digestSize());

    try std.testing.expectEqual(@as(usize, 32), HashAlgorithm.md5.hexLen());
    try std.testing.expectEqual(@as(usize, 40), HashAlgorithm.sha1.hexLen());
    try std.testing.expectEqual(@as(usize, 64), HashAlgorithm.sha256.hexLen());
    try std.testing.expectEqual(@as(usize, 128), HashAlgorithm.sha512.hexLen());
}

test "PBKDF2-SHA256" {
    const allocator = std.testing.allocator;

    // RFC 6070 test vector
    const password = "password";
    const salt = "salt";
    const iterations: u32 = 1;
    const key_len: usize = 20;

    const derived = try pbkdf2Sha256(allocator, password, salt, iterations, key_len);
    defer allocator.free(derived);

    const hex = try toHex(allocator, derived);
    defer allocator.free(hex);

    // Verify length and format
    try std.testing.expectEqual(@as(usize, 20), derived.len);
    try std.testing.expectEqual(@as(usize, 40), hex.len);
}

test "large data hashing" {
    const allocator = std.testing.allocator;

    // Create a larger test input
    var input: [1024]u8 = undefined;
    for (0..1024) |i| {
        input[i] = @intCast(i % 256);
    }

    // All algorithms should handle large data
    const md5 = try Md5.hashHex(allocator, &input);
    defer allocator.free(md5);
    try std.testing.expectEqual(@as(usize, 32), md5.len);

    const sha1 = try Sha1.hashHex(allocator, &input);
    defer allocator.free(sha1);
    try std.testing.expectEqual(@as(usize, 40), sha1.len);

    const sha256 = try Sha256.hashHex(allocator, &input);
    defer allocator.free(sha256);
    try std.testing.expectEqual(@as(usize, 64), sha256.len);

    const sha512 = try Sha512.hashHex(allocator, &input);
    defer allocator.free(sha512);
    try std.testing.expectEqual(@as(usize, 128), sha512.len);
}

test "binary data hashing" {
    const allocator = std.testing.allocator;

    // Test with all byte values
    var input: [256]u8 = undefined;
    for (0..256) |i| {
        input[i] = @intCast(i);
    }

    // Should handle binary data correctly
    const md5 = try Md5.hashHex(allocator, &input);
    defer allocator.free(md5);

    // Verify roundtrip with fromHex
    const md5_bytes = try fromHex(allocator, md5);
    defer allocator.free(md5_bytes);

    try std.testing.expectEqual(@as(usize, 16), md5_bytes.len);
}

test "buffer too small error" {
    var small_buffer: [10]u8 = undefined;
    const result = hashInto(&small_buffer, "test", .sha256);
    try std.testing.expectError(HashError.BufferTooSmall, result);
}

test "fromHex invalid input" {
    const allocator = std.testing.allocator;

    const result1 = fromHex(allocator, "xyz");
    try std.testing.expectError(HashError.InvalidHex, result1);

    const result2 = fromHex(allocator, "invalid_hex");
    try std.testing.expectError(HashError.InvalidHex, result2);
}