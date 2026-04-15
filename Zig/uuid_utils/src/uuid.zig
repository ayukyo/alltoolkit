const std = @import("std");

/// UUID version
pub const Version = enum(u4) {
    v1 = 1, // Time-based
    v2 = 2, // DCE Security
    v3 = 3, // MD5 hash
    v4 = 4, // Random
    v5 = 5, // SHA-1 hash
};

/// UUID variant
pub const Variant = enum(u2) {
    /// Reserved, NCS backward compatibility
    ncs = 0,
    /// Standard (RFC 4122)
    rfc4122 = 2,
    /// Microsoft Corporation backward compatibility
    microsoft = 1,
    /// Reserved for future definition
    future = 3,
};

/// UUID representation
pub const UUID = struct {
    bytes: [16]u8,

    /// Parse a UUID string (with or without hyphens)
    pub fn parse(input: []const u8) UUIDError!UUID {
        if (input.len != 36 and input.len != 32) {
            return UUIDError.InvalidFormat;
        }

        var uuid = UUID{ .bytes = undefined };

        if (input.len == 36) {
            // Format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
            // Validate hyphen positions
            if (input[8] != '-' or input[13] != '-' or input[18] != '-' or input[23] != '-') {
                return UUIDError.InvalidFormat;
            }

            uuid.bytes[0] = try parseHexByte(input[0..2]);
            uuid.bytes[1] = try parseHexByte(input[2..4]);
            uuid.bytes[2] = try parseHexByte(input[4..6]);
            uuid.bytes[3] = try parseHexByte(input[6..8]);
            // Skip hyphen at 8
            uuid.bytes[4] = try parseHexByte(input[9..11]);
            uuid.bytes[5] = try parseHexByte(input[11..13]);
            // Skip hyphen at 13
            uuid.bytes[6] = try parseHexByte(input[14..16]);
            uuid.bytes[7] = try parseHexByte(input[16..18]);
            // Skip hyphen at 18
            uuid.bytes[8] = try parseHexByte(input[19..21]);
            uuid.bytes[9] = try parseHexByte(input[21..23]);
            // Skip hyphen at 23
            uuid.bytes[10] = try parseHexByte(input[24..26]);
            uuid.bytes[11] = try parseHexByte(input[26..28]);
            uuid.bytes[12] = try parseHexByte(input[28..30]);
            uuid.bytes[13] = try parseHexByte(input[30..32]);
            uuid.bytes[14] = try parseHexByte(input[32..34]);
            uuid.bytes[15] = try parseHexByte(input[34..36]);
        } else {
            // Format: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (no hyphens)
            var i: usize = 0;
            while (i < 16) : (i += 1) {
                uuid.bytes[i] = try parseHexByte(input[i * 2 .. i * 2 + 2]);
            }
        }

        return uuid;
    }

    /// Convert UUID to string (with hyphens)
    pub fn toString(self: UUID, allocator: std.mem.Allocator) UUIDError![]u8 {
        const result = allocator.alloc(u8, 36) catch return UUIDError.OutOfMemory;
        errdefer allocator.free(result);

        formatInto(result, &self.bytes);
        return result;
    }

    /// Convert UUID to string without hyphens
    pub fn toCompactString(self: UUID, allocator: std.mem.Allocator) UUIDError![]u8 {
        const result = allocator.alloc(u8, 32) catch return UUIDError.OutOfMemory;
        errdefer allocator.free(result);

        for (self.bytes, 0..) |byte, i| {
            result[i * 2] = toHexChar(byte >> 4);
            result[i * 2 + 1] = toHexChar(byte & 0x0F);
        }

        return result;
    }

    /// Write UUID string to buffer (with hyphens)
    pub fn toStringInto(self: UUID, buffer: []u8) usize {
        if (buffer.len < 36) return 0;
        formatInto(buffer, &self.bytes);
        return 36;
    }

    /// Get UUID version
    pub fn version(self: UUID) Version {
        return @enumFromInt((self.bytes[6] >> 4) & 0x0F);
    }

    /// Get UUID variant
    pub fn variant(self: UUID) Variant {
        // RFC 4122 variant detection based on clock_seq_hi_and_reserved byte
        // Layout: 
        // - 0xxxxxxx (0x00-0x7F) = NCS backward compatibility
        // - 10xxxxxx (0x80-0xBF) = RFC 4122
        // - 110xxxxx (0xC0-0xDF) = Microsoft
        // - 111xxxxx (0xE0-0xFF) = Future/Reserved
        const byte = self.bytes[8];
        if ((byte & 0x80) == 0) {
            // 0xxxxxxx - NCS
            return Variant.ncs;
        } else if ((byte & 0x40) == 0) {
            // 10xxxxxx - RFC 4122
            return Variant.rfc4122;
        } else if ((byte & 0x20) == 0) {
            // 110xxxxx - Microsoft
            return Variant.microsoft;
        } else {
            // 111xxxxx - Future
            return Variant.future;
        }
    }

    /// Check if UUID is nil (all zeros)
    pub fn isNil(self: UUID) bool {
        for (self.bytes) |byte| {
            if (byte != 0) return false;
        }
        return true;
    }

    /// Compare two UUIDs for equality
    pub fn eql(self: UUID, other: UUID) bool {
        return std.mem.eql(u8, &self.bytes, &other.bytes);
    }

    /// Compare two UUIDs (for sorting)
    pub fn lessThan(self: UUID, other: UUID) bool {
        return std.mem.lessThan(u8, &self.bytes, &other.bytes);
    }

    /// Get hash of UUID (for use in hash maps)
    pub fn hash(self: UUID) u64 {
        var hasher = std.hash.Wyhash.init(0);
        hasher.update(&self.bytes);
        return hasher.final();
    }

    /// Convert nibble to lowercase hex character
    fn toHexChar(nibble: u8) u8 {
        const HEX_CHARS = "0123456789abcdef";
        return HEX_CHARS[nibble & 0x0F];
    }

    /// Format bytes into hex string with hyphens
    fn formatInto(buffer: []u8, bytes: *const [16]u8) void {
        // time_low (4 bytes)
        buffer[0] = toHexChar(bytes[0] >> 4);
        buffer[1] = toHexChar(bytes[0] & 0x0F);
        buffer[2] = toHexChar(bytes[1] >> 4);
        buffer[3] = toHexChar(bytes[1] & 0x0F);
        buffer[4] = toHexChar(bytes[2] >> 4);
        buffer[5] = toHexChar(bytes[2] & 0x0F);
        buffer[6] = toHexChar(bytes[3] >> 4);
        buffer[7] = toHexChar(bytes[3] & 0x0F);
        buffer[8] = '-';
        // time_mid (2 bytes)
        buffer[9] = toHexChar(bytes[4] >> 4);
        buffer[10] = toHexChar(bytes[4] & 0x0F);
        buffer[11] = toHexChar(bytes[5] >> 4);
        buffer[12] = toHexChar(bytes[5] & 0x0F);
        buffer[13] = '-';
        // time_hi_and_version (2 bytes)
        buffer[14] = toHexChar(bytes[6] >> 4);
        buffer[15] = toHexChar(bytes[6] & 0x0F);
        buffer[16] = toHexChar(bytes[7] >> 4);
        buffer[17] = toHexChar(bytes[7] & 0x0F);
        buffer[18] = '-';
        // clock_seq_hi_and_reserved + clock_seq_low (2 bytes)
        buffer[19] = toHexChar(bytes[8] >> 4);
        buffer[20] = toHexChar(bytes[8] & 0x0F);
        buffer[21] = toHexChar(bytes[9] >> 4);
        buffer[22] = toHexChar(bytes[9] & 0x0F);
        buffer[23] = '-';
        // node (6 bytes)
        buffer[24] = toHexChar(bytes[10] >> 4);
        buffer[25] = toHexChar(bytes[10] & 0x0F);
        buffer[26] = toHexChar(bytes[11] >> 4);
        buffer[27] = toHexChar(bytes[11] & 0x0F);
        buffer[28] = toHexChar(bytes[12] >> 4);
        buffer[29] = toHexChar(bytes[12] & 0x0F);
        buffer[30] = toHexChar(bytes[13] >> 4);
        buffer[31] = toHexChar(bytes[13] & 0x0F);
        buffer[32] = toHexChar(bytes[14] >> 4);
        buffer[33] = toHexChar(bytes[14] & 0x0F);
        buffer[34] = toHexChar(bytes[15] >> 4);
        buffer[35] = toHexChar(bytes[15] & 0x0F);
    }
};

/// Errors that can occur during UUID operations
pub const UUIDError = error{
    /// Invalid UUID format
    InvalidFormat,
    /// Invalid hex character
    InvalidHexCharacter,
    /// Memory allocation failed
    OutOfMemory,
    /// Random number generation failed
    RandomError,
};

/// UUID generator
pub const Generator = struct {
    prng: std.rand.DefaultPrng,

    /// Initialize generator with a seed
    pub fn init(seed: u64) Generator {
        return .{ .prng = std.rand.DefaultPrng.init(seed) };
    }

    /// Initialize generator with a random seed
    pub fn initRandom() UUIDError!Generator {
        var seed: u64 = undefined;
        std.crypto.random.bytes(std.mem.asBytes(&seed));
        return .{ .prng = std.rand.DefaultPrng.init(seed) };
    }

    /// Generate a new UUID v4 (random)
    pub fn generate(self: *Generator) UUID {
        var uuid = UUID{ .bytes = undefined };
        self.prng.random().bytes(&uuid.bytes);

        // Set version to 4 (random)
        uuid.bytes[6] = (uuid.bytes[6] & 0x0F) | 0x40;

        // Set variant to RFC 4122 (10xxxxxx)
        uuid.bytes[8] = (uuid.bytes[8] & 0x3F) | 0x80;

        return uuid;
    }

    /// Generate a nil UUID (all zeros)
    pub fn nil() UUID {
        return UUID{ .bytes = [_]u8{0} ** 16 };
    }
};

/// Generate a UUID v4 using a random seed
pub fn generateV4() UUIDError!UUID {
    var generator = try Generator.initRandom();
    return generator.generate();
}

/// Generate a UUID v4 using a provided seed
pub fn generateV4WithSeed(seed: u64) UUID {
    var generator = Generator.init(seed);
    return generator.generate();
}

/// Generate a nil UUID (all zeros)
pub fn nil() UUID {
    return UUID{ .bytes = [_]u8{0} ** 16 };
}

/// Check if a string is a valid UUID format
pub fn isValid(input: []const u8) bool {
    if (input.len != 36 and input.len != 32) return false;

    if (input.len == 36) {
        // Check hyphen positions
        if (input[8] != '-' or input[13] != '-' or input[18] != '-' or input[23] != '-') {
            return false;
        }
    }

    // Check hex characters
    for (input) |c| {
        if (c == '-') continue;
        if (!std.ascii.isHex(c)) return false;
    }

    return true;
}

/// Parse a hex character to its value
fn parseHexChar(c: u8) UUIDError!u8 {
    return switch (c) {
        '0'...'9' => c - '0',
        'A'...'F' => c - 'A' + 10,
        'a'...'f' => c - 'a' + 10,
        else => UUIDError.InvalidHexCharacter,
    };
}

/// Parse two hex characters to a byte
fn parseHexByte(input: []const u8) UUIDError!u8 {
    if (input.len < 2) return UUIDError.InvalidFormat;
    const high = try parseHexChar(input[0]);
    const low = try parseHexChar(input[1]);
    return (high << 4) | low;
}

// --- Tests ---

test "generate v4 uuid" {
    const uuid = try generateV4();

    // Check version
    try std.testing.expectEqual(Version.v4, uuid.version());

    // Check variant is RFC 4122
    try std.testing.expectEqual(Variant.rfc4122, uuid.variant());

    // Check not nil
    try std.testing.expect(!uuid.isNil());
}

test "parse uuid with hyphens" {
    const input = "550e8400-e29b-41d4-a716-446655440000";
    const uuid = try UUID.parse(input);

    try std.testing.expectEqual(@as(u8, 0x55), uuid.bytes[0]);
    try std.testing.expectEqual(@as(u8, 0x0e), uuid.bytes[1]);
    try std.testing.expectEqual(@as(u8, 0x84), uuid.bytes[2]);
    try std.testing.expectEqual(@as(u8, 0x00), uuid.bytes[3]);
}

test "parse uuid without hyphens" {
    const input = "550e8400e29b41d4a716446655440000";
    const uuid = try UUID.parse(input);

    try std.testing.expectEqual(@as(u8, 0x55), uuid.bytes[0]);
    try std.testing.expectEqual(@as(u8, 0x0e), uuid.bytes[1]);
}

test "uuid to string" {
    const allocator = std.testing.allocator;

    const input = "550e8400-e29b-41d4-a716-446655440000";
    const uuid = try UUID.parse(input);

    const str = try uuid.toString(allocator);
    defer allocator.free(str);

    try std.testing.expectEqualStrings(input, str);
}

test "uuid to compact string" {
    const allocator = std.testing.allocator;

    const input = "550e8400-e29b-41d4-a716-446655440000";
    const uuid = try UUID.parse(input);

    const str = try uuid.toCompactString(allocator);
    defer allocator.free(str);

    try std.testing.expectEqualStrings("550e8400e29b41d4a716446655440000", str);
}

test "uuid roundtrip" {
    const allocator = std.testing.allocator;

    const uuid1 = try generateV4();
    const str = try uuid1.toString(allocator);
    defer allocator.free(str);

    const uuid2 = try UUID.parse(str);

    try std.testing.expect(uuid1.eql(uuid2));
}

test "nil uuid" {
    const uuid = nil();

    try std.testing.expect(uuid.isNil());

    for (uuid.bytes) |byte| {
        try std.testing.expectEqual(@as(u8, 0), byte);
    }
}

test "uuid equality" {
    const uuid1 = try generateV4();
    const uuid2 = try generateV4();

    try std.testing.expect(uuid1.eql(uuid1));
    try std.testing.expect(!uuid1.eql(uuid2));
}

test "uuid version" {
    const input = "550e8400-e29b-41d4-a716-446655440000";
    const uuid = try UUID.parse(input);

    try std.testing.expectEqual(Version.v4, uuid.version());
}

test "isValid" {
    try std.testing.expect(isValid("550e8400-e29b-41d4-a716-446655440000"));
    try std.testing.expect(isValid("550e8400e29b41d4a716446655440000"));
    try std.testing.expect(!isValid("550e8400-e29b-41d4-a716"));
    try std.testing.expect(!isValid("550e8400-e29b-41d4-a716-44665544000g"));
}

test "invalid parse" {
    try std.testing.expectError(UUIDError.InvalidFormat, UUID.parse("too-short"));
    try std.testing.expectError(UUIDError.InvalidHexCharacter, UUID.parse("550e8400-xxxx-41d4-a716-446655440000"));
}

test "uuid hash" {
    const allocator = std.testing.allocator;

    const uuid1 = try generateV4();
    const str = try uuid1.toString(allocator);
    defer allocator.free(str);
    const uuid2 = try UUID.parse(str);

    try std.testing.expectEqual(uuid1.hash(), uuid2.hash());
}

test "uuid lessThan" {
    const uuid1 = try UUID.parse("00000000-0000-4000-8000-000000000001");
    const uuid2 = try UUID.parse("00000000-0000-4000-8000-000000000002");

    try std.testing.expect(uuid1.lessThan(uuid2));
    try std.testing.expect(!uuid2.lessThan(uuid1));
}

test "toStringInto" {
    const uuid = try UUID.parse("550e8400-e29b-41d4-a716-446655440000");

    var buffer: [36]u8 = undefined;
    const len = uuid.toStringInto(&buffer);

    try std.testing.expectEqual(@as(usize, 36), len);
    try std.testing.expectEqualStrings("550e8400-e29b-41d4-a716-446655440000", buffer[0..len]);
}

test "multiple unique uuids" {
    var uuids: [100]UUID = undefined;

    for (0..100) |i| {
        uuids[i] = try generateV4();
    }

    // Check all are unique
    for (0..100) |i| {
        for (i + 1..100) |j| {
            try std.testing.expect(!uuids[i].eql(uuids[j]));
        }
    }
}

test "variant detection" {
    // RFC 4122 variant: clock_seq_hi starts with 10xxxxxx (0x80-0xBF)
    const rfc_uuid = try UUID.parse("550e8400-e29b-41d4-a716-446655440000");
    try std.testing.expectEqual(Variant.rfc4122, rfc_uuid.variant());

    // Microsoft variant: clock_seq_hi starts with 110xxxxx (0xC0-0xDF)
    const ms_uuid = try UUID.parse("550e8400-e29b-41d4-c716-446655440000");
    try std.testing.expectEqual(Variant.microsoft, ms_uuid.variant());

    // NCS variant: clock_seq_hi starts with 0xxxxxxx (0x00-0x7F)
    const ncs_uuid = try UUID.parse("550e8400-e29b-41d4-0716-446655440000");
    try std.testing.expectEqual(Variant.ncs, ncs_uuid.variant());
}

test "generator with seed" {
    // Same seed should produce same UUID
    const uuid1 = generateV4WithSeed(12345);
    const uuid2 = generateV4WithSeed(12345);

    try std.testing.expect(uuid1.eql(uuid2));

    // Different seed should produce different UUID
    const uuid3 = generateV4WithSeed(12346);
    try std.testing.expect(!uuid1.eql(uuid3));
}