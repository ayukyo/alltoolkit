const std = @import("std");

/// Base64 encoding table (standard RFC 4648)
const ENCODE_TABLE: [64]u8 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".*;

/// Base64 decoding table
const DECODE_TABLE: [256]i8 = init: {
    var table: [256]i8 = undefined;
    @memset(&table, -1);
    var i: usize = 0;
    while (i < 64) : (i += 1) {
        table[ENCODE_TABLE[i]] = @intCast(i);
    }
    break :init table;
};

/// Base64 encoding options
pub const EncodeOptions = struct {
    /// Use URL-safe encoding (replace +/ with -_)
    url_safe: bool = false,
    /// Add padding (= characters)
    padding: bool = true,
};

/// Base64 decoding options
pub const DecodeOptions = struct {
    /// Expect URL-safe encoding (replace -_ with +/)
    url_safe: bool = false,
    /// Validate padding
    strict_padding: bool = true,
};

/// Errors that can occur during Base64 operations
pub const Base64Error = error{
    /// Invalid character in input
    InvalidCharacter,
    /// Invalid padding
    InvalidPadding,
    /// Output buffer too small
    BufferTooSmall,
    /// Memory allocation failed
    OutOfMemory,
};

/// Calculate the encoded length for a given input length
pub fn encodedLen(input_len: usize, options: EncodeOptions) usize {
    const base = (input_len + 2) / 3 * 4;
    if (options.padding) {
        return base;
    }
    // Without padding, calculate actual length
    const remainder = input_len % 3;
    if (remainder == 0) {
        return base;
    }
    return base - (3 - remainder);
}

/// Calculate the decoded length for a given input length
pub fn decodedLen(input_len: usize) usize {
    return input_len / 4 * 3;
}

/// Encode bytes to Base64 string
/// Caller owns the returned memory
pub fn encode(allocator: std.mem.Allocator, input: []const u8, options: EncodeOptions) Base64Error![]u8 {
    const output_len = encodedLen(input.len, options);
    const output = allocator.alloc(u8, output_len) catch return Base64Error.OutOfMemory;
    errdefer allocator.free(output);

    var in_idx: usize = 0;
    var out_idx: usize = 0;

    // Process 3 bytes at a time
    while (in_idx + 3 <= input.len) : (in_idx += 3) {
        const b0 = input[in_idx];
        const b1 = input[in_idx + 1];
        const b2 = input[in_idx + 2];

        output[out_idx] = encodeChar(@intCast((b0 >> 2) & 0x3F), options);
        output[out_idx + 1] = encodeChar(@intCast(((b0 & 0x03) << 4) | ((b1 >> 4) & 0x0F)), options);
        output[out_idx + 2] = encodeChar(@intCast(((b1 & 0x0F) << 2) | ((b2 >> 6) & 0x03)), options);
        output[out_idx + 3] = encodeChar(@intCast(b2 & 0x3F), options);

        out_idx += 4;
    }

    // Handle remaining bytes
    const remainder = input.len % 3;
    if (remainder > 0) {
        const b0 = input[in_idx];
        output[out_idx] = encodeChar(@intCast((b0 >> 2) & 0x3F), options);

        if (remainder == 1) {
            output[out_idx + 1] = encodeChar(@intCast((b0 & 0x03) << 4), options);
            out_idx += 2;

            if (options.padding) {
                output[out_idx] = '=';
                output[out_idx + 1] = '=';
                out_idx += 2;
            }
        } else {
            const b1 = input[in_idx + 1];
            output[out_idx + 1] = encodeChar(@intCast(((b0 & 0x03) << 4) | ((b1 >> 4) & 0x0F)), options);
            output[out_idx + 2] = encodeChar(@intCast((b1 & 0x0F) << 2), options);
            out_idx += 3;

            if (options.padding) {
                output[out_idx] = '=';
                out_idx += 1;
            }
        }
    }

    return output[0..out_idx];
}

/// Encode bytes to Base64 string into a provided buffer
pub fn encodeInto(output: []u8, input: []const u8, options: EncodeOptions) Base64Error!usize {
    const expected_len = encodedLen(input.len, options);
    if (output.len < expected_len) {
        return Base64Error.BufferTooSmall;
    }

    var in_idx: usize = 0;
    var out_idx: usize = 0;

    while (in_idx + 3 <= input.len) : (in_idx += 3) {
        const b0 = input[in_idx];
        const b1 = input[in_idx + 1];
        const b2 = input[in_idx + 2];

        output[out_idx] = encodeChar(@intCast((b0 >> 2) & 0x3F), options);
        output[out_idx + 1] = encodeChar(@intCast(((b0 & 0x03) << 4) | ((b1 >> 4) & 0x0F)), options);
        output[out_idx + 2] = encodeChar(@intCast(((b1 & 0x0F) << 2) | ((b2 >> 6) & 0x03)), options);
        output[out_idx + 3] = encodeChar(@intCast(b2 & 0x3F), options);

        out_idx += 4;
    }

    const remainder = input.len % 3;
    if (remainder > 0) {
        const b0 = input[in_idx];
        output[out_idx] = encodeChar(@intCast((b0 >> 2) & 0x3F), options);

        if (remainder == 1) {
            output[out_idx + 1] = encodeChar(@intCast((b0 & 0x03) << 4), options);
            out_idx += 2;

            if (options.padding) {
                output[out_idx] = '=';
                output[out_idx + 1] = '=';
                out_idx += 2;
            }
        } else {
            const b1 = input[in_idx + 1];
            output[out_idx + 1] = encodeChar(@intCast(((b0 & 0x03) << 4) | ((b1 >> 4) & 0x0F)), options);
            output[out_idx + 2] = encodeChar(@intCast((b1 & 0x0F) << 2), options);
            out_idx += 3;

            if (options.padding) {
                output[out_idx] = '=';
                out_idx += 1;
            }
        }
    }

    return out_idx;
}

/// Decode Base64 string to bytes
/// Caller owns the returned memory
pub fn decode(allocator: std.mem.Allocator, input: []const u8, options: DecodeOptions) Base64Error![]u8 {
    // Strip whitespace
    var clean_input = std.ArrayList(u8).init(allocator);
    defer clean_input.deinit();

    for (input) |c| {
        if (!std.ascii.isWhitespace(c)) {
            clean_input.append(c) catch return Base64Error.OutOfMemory;
        }
    }

    const data = clean_input.items;

    if (data.len == 0) {
        return allocator.dupe(u8, &[_]u8{}) catch return Base64Error.OutOfMemory;
    }

    // Validate length
    if (data.len % 4 != 0) {
        return Base64Error.InvalidPadding;
    }

    // Calculate output length
    var padding_count: usize = 0;
    if (data.len >= 2) {
        if (data[data.len - 1] == '=') padding_count += 1;
        if (data[data.len - 2] == '=') padding_count += 1;
    }

    const output_len = data.len / 4 * 3 - padding_count;
    const output = allocator.alloc(u8, output_len) catch return Base64Error.OutOfMemory;
    errdefer allocator.free(output);

    var in_idx: usize = 0;
    var out_idx: usize = 0;

    while (in_idx < data.len) : (in_idx += 4) {
        const v0: u8 = @intCast(try decodeChar(data[in_idx], options));
        const v1: u8 = @intCast(try decodeChar(data[in_idx + 1], options));

        output[out_idx] = (v0 << 2) | (v1 >> 4);
        out_idx += 1;

        if (data[in_idx + 2] != '=') {
            const v2: u8 = @intCast(try decodeChar(data[in_idx + 2], options));
            output[out_idx] = ((v1 & 0x0F) << 4) | (v2 >> 2);
            out_idx += 1;

            if (data[in_idx + 3] != '=') {
                const v3: u8 = @intCast(try decodeChar(data[in_idx + 3], options));
                output[out_idx] = ((v2 & 0x03) << 6) | v3;
                out_idx += 1;
            }
        }
    }

    return output[0..out_idx];
}

/// Decode Base64 string into a provided buffer
pub fn decodeInto(output: []u8, input: []const u8, options: DecodeOptions) Base64Error!usize {
    var clean_len: usize = 0;
    for (input) |c| {
        if (!std.ascii.isWhitespace(c)) {
            clean_len += 1;
        }
    }

    if (clean_len == 0) {
        return 0;
    }

    if (clean_len % 4 != 0) {
        return Base64Error.InvalidPadding;
    }

    // Strip whitespace and decode
    var clean_input: [4096]u8 = undefined;
    var idx: usize = 0;
    for (input) |c| {
        if (!std.ascii.isWhitespace(c)) {
            if (idx >= clean_input.len) {
                return Base64Error.BufferTooSmall;
            }
            clean_input[idx] = c;
            idx += 1;
        }
    }

    const data = clean_input[0..idx];

    var padding_count: usize = 0;
    if (data.len >= 2) {
        if (data[data.len - 1] == '=') padding_count += 1;
        if (data[data.len - 2] == '=') padding_count += 1;
    }

    const expected_output_len = data.len / 4 * 3 - padding_count;
    if (output.len < expected_output_len) {
        return Base64Error.BufferTooSmall;
    }

    var in_idx: usize = 0;
    var out_idx: usize = 0;

    while (in_idx < data.len) : (in_idx += 4) {
        const v0: u8 = @intCast(try decodeChar(data[in_idx], options));
        const v1: u8 = @intCast(try decodeChar(data[in_idx + 1], options));

        output[out_idx] = (v0 << 2) | (v1 >> 4);
        out_idx += 1;

        if (data[in_idx + 2] != '=') {
            const v2: u8 = @intCast(try decodeChar(data[in_idx + 2], options));
            output[out_idx] = ((v1 & 0x0F) << 4) | (v2 >> 2);
            out_idx += 1;

            if (data[in_idx + 3] != '=') {
                const v3: u8 = @intCast(try decodeChar(data[in_idx + 3], options));
                output[out_idx] = ((v2 & 0x03) << 6) | v3;
                out_idx += 1;
            }
        }
    }

    return out_idx;
}

/// Check if a string is valid Base64
pub fn isValid(input: []const u8, options: DecodeOptions) bool {
    var clean_len: usize = 0;
    for (input) |c| {
        if (!std.ascii.isWhitespace(c)) {
            clean_len += 1;
        }
    }

    if (clean_len == 0) return true;
    if (clean_len % 4 != 0) return false;

    var padding_started = false;

    for (input) |c| {
        if (std.ascii.isWhitespace(c)) continue;

        if (c == '=') {
            padding_started = true;
        } else if (padding_started) {
            // Character after padding
            return false;
        } else {
            _ = decodeChar(c, options) catch return false;
        }
    }

    return true;
}

// --- Internal Helper Functions ---

fn encodeChar(value: u6, options: EncodeOptions) u8 {
    const char = ENCODE_TABLE[value];
    if (options.url_safe) {
        return switch (char) {
            '+' => '-',
            '/' => '_',
            else => char,
        };
    }
    return char;
}

fn decodeChar(char: u8, options: DecodeOptions) Base64Error!u6 {
    var c = char;
    if (options.url_safe) {
        c = switch (char) {
            '-' => '+',
            '_' => '/',
            else => char,
        };
    }

    const value = DECODE_TABLE[c];
    if (value < 0) {
        return Base64Error.InvalidCharacter;
    }
    return @intCast(value);
}

// --- Tests ---

test "encode basic" {
    const allocator = std.testing.allocator;

    // RFC 4648 test vectors
    const test_cases = [_]struct {
        input: []const u8,
        expected: []const u8,
    }{
        .{ .input = "", .expected = "" },
        .{ .input = "f", .expected = "Zg==" },
        .{ .input = "fo", .expected = "Zm8=" },
        .{ .input = "foo", .expected = "Zm9v" },
        .{ .input = "foob", .expected = "Zm9vYg==" },
        .{ .input = "fooba", .expected = "Zm9vYmE=" },
        .{ .input = "foobar", .expected = "Zm9vYmFy" },
    };

    for (test_cases) |tc| {
        const result = try encode(allocator, tc.input, .{});
        defer allocator.free(result);
        try std.testing.expectEqualStrings(tc.expected, result);
    }
}

test "decode basic" {
    const allocator = std.testing.allocator;

    const test_cases = [_]struct {
        input: []const u8,
        expected: []const u8,
    }{
        .{ .input = "", .expected = "" },
        .{ .input = "Zg==", .expected = "f" },
        .{ .input = "Zm8=", .expected = "fo" },
        .{ .input = "Zm9v", .expected = "foo" },
        .{ .input = "Zm9vYg==", .expected = "foob" },
        .{ .input = "Zm9vYmE=", .expected = "fooba" },
        .{ .input = "Zm9vYmFy", .expected = "foobar" },
    };

    for (test_cases) |tc| {
        const result = try decode(allocator, tc.input, .{});
        defer allocator.free(result);
        try std.testing.expectEqualStrings(tc.expected, result);
    }
}

test "encode decode roundtrip" {
    const allocator = std.testing.allocator;

    const test_inputs = [_][]const u8{
        "Hello, World!",
        "The quick brown fox jumps over the lazy dog",
        "1234567890",
        "Binary\x00Data\xFFHere",
    };

    for (test_inputs) |input| {
        const encoded = try encode(allocator, input, .{});
        defer allocator.free(encoded);

        const decoded = try decode(allocator, encoded, .{});
        defer allocator.free(decoded);

        try std.testing.expectEqualStrings(input, decoded);
    }
}

test "url safe encoding" {
    const allocator = std.testing.allocator;

    // Input that would produce +/ in standard encoding
    const input = "\xFF\xFE\xFD\xFC\xFB\xFA";

    const standard = try encode(allocator, input, .{ .url_safe = false });
    defer allocator.free(standard);

    const url_safe = try encode(allocator, input, .{ .url_safe = true });
    defer allocator.free(url_safe);

    // URL-safe should have - and _ instead of + and /
    try std.testing.expect(std.mem.indexOf(u8, standard, "+") != null or std.mem.indexOf(u8, standard, "/") != null or std.mem.eql(u8, standard, url_safe));
    try std.testing.expect(std.mem.indexOf(u8, url_safe, "+") == null);
    try std.testing.expect(std.mem.indexOf(u8, url_safe, "/") == null);
}

test "no padding" {
    const allocator = std.testing.allocator;

    const input = "foo";
    const encoded = try encode(allocator, input, .{ .padding = false });
    defer allocator.free(encoded);

    // Without padding, should not contain =
    try std.testing.expect(std.mem.indexOf(u8, encoded, "=") == null);
}

test "decode with whitespace" {
    const allocator = std.testing.allocator;

    const input = "Zm9v\nYmFy";
    const result = try decode(allocator, input, .{});
    defer allocator.free(result);

    try std.testing.expectEqualStrings("foobar", result);
}

test "isValid" {
    try std.testing.expect(isValid("", .{}));
    try std.testing.expect(isValid("Zm9v", .{}));
    try std.testing.expect(isValid("Zm9vYg==", .{}));
    try std.testing.expect(!isValid("Zm9vYg=", .{}));
    try std.testing.expect(!isValid("Zm9!Yg==", .{}));
}

test "encodedLen" {
    try std.testing.expectEqual(@as(usize, 0), encodedLen(0, .{}));
    try std.testing.expectEqual(@as(usize, 4), encodedLen(1, .{}));
    try std.testing.expectEqual(@as(usize, 4), encodedLen(2, .{}));
    try std.testing.expectEqual(@as(usize, 4), encodedLen(3, .{}));
    try std.testing.expectEqual(@as(usize, 8), encodedLen(4, .{}));
    try std.testing.expectEqual(@as(usize, 8), encodedLen(6, .{}));
}

test "decodedLen" {
    try std.testing.expectEqual(@as(usize, 0), decodedLen(0));
    try std.testing.expectEqual(@as(usize, 3), decodedLen(4));
    try std.testing.expectEqual(@as(usize, 6), decodedLen(8));
    try std.testing.expectEqual(@as(usize, 9), decodedLen(12));
}

test "encodeInto buffer too small" {
    var buffer: [2]u8 = undefined;
    const input = "foobar";
    const result = encodeInto(&buffer, input, .{});
    try std.testing.expectError(Base64Error.BufferTooSmall, result);
}

test "decodeInto buffer too small" {
    var buffer: [2]u8 = undefined;
    const input = "Zm9vYmFy";
    const result = decodeInto(&buffer, input, .{});
    try std.testing.expectError(Base64Error.BufferTooSmall, result);
}

test "decode invalid character" {
    const allocator = std.testing.allocator;
    const input = "Zm9!YmFy";
    const result = decode(allocator, input, .{});
    try std.testing.expectError(Base64Error.InvalidCharacter, result);
}

test "decode invalid padding" {
    const allocator = std.testing.allocator;
    const input = "Zm9vYmF"; // Missing padding
    const result = decode(allocator, input, .{});
    try std.testing.expectError(Base64Error.InvalidPadding, result);
}

test "binary data roundtrip" {
    const allocator = std.testing.allocator;

    // Test with all byte values
    var input: [256]u8 = undefined;
    for (0..256) |i| {
        input[i] = @intCast(i);
    }

    const encoded = try encode(allocator, &input, .{});
    defer allocator.free(encoded);

    const decoded = try decode(allocator, encoded, .{});
    defer allocator.free(decoded);

    try std.testing.expectEqualSlices(u8, &input, decoded);
}