const std = @import("std");
const base64 = @import("base64");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Base64 Utils - Basic Usage ===\n\n", .{});

    // Basic encoding
    const text = "Hello, World!";
    const encoded = try base64.encode(allocator, text, .{});
    defer allocator.free(encoded);
    std.debug.print("Input: {s}\n", .{text});
    std.debug.print("Encoded: {s}\n\n", .{encoded});

    // Basic decoding
    const decoded = try base64.decode(allocator, encoded, .{});
    defer allocator.free(decoded);
    std.debug.print("Decoded: {s}\n\n", .{decoded});

    // URL-safe encoding
    const binary_data = "\xFF\xFE\xFD\xFC\xFB\xFA";
    const url_safe_encoded = try base64.encode(allocator, binary_data, .{ .url_safe = true });
    defer allocator.free(url_safe_encoded);
    std.debug.print("Binary data (hex): {s}\n", .{std.fmt.fmtSliceHexLower(binary_data)});
    std.debug.print("URL-safe encoded: {s}\n\n", .{url_safe_encoded});

    // Encoding without padding
    const no_padding = try base64.encode(allocator, text, .{ .padding = false });
    defer allocator.free(no_padding);
    std.debug.print("Without padding: {s}\n\n", .{no_padding});

    // Validate Base64 string
    const is_valid = base64.isValid(encoded, .{});
    std.debug.print("'{s}' is valid Base64: {}\n", .{encoded, is_valid});

    const invalid = "Not@Valid!";
    const is_invalid = base64.isValid(invalid, .{});
    std.debug.print("'{s}' is valid Base64: {}\n\n", .{invalid, is_invalid});

    // Calculate lengths
    const enc_len = base64.encodedLen(text.len, .{});
    const dec_len = base64.decodedLen(encoded.len);
    std.debug.print("Text length: {}\n", .{text.len});
    std.debug.print("Encoded length: {} (calculated: {})\n", .{encoded.len, enc_len});
    std.debug.print("Decoded length: {} (calculated: {})\n", .{decoded.len, dec_len});
}