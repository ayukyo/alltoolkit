const std = @import("std");
const base64 = @import("base64");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Base64 Utils - Advanced Usage ===\n\n", .{});

    // Example 1: Encoding into a pre-allocated buffer
    std.debug.print("1. Pre-allocated buffer encoding:\n", .{});
    const input = "The quick brown fox jumps over the lazy dog";
    var buffer: [100]u8 = undefined;
    const written = try base64.encodeInto(&buffer, input, .{});
    std.debug.print("   Input: {s}\n", .{input});
    std.debug.print("   Encoded (into buffer): {s}\n", .{buffer[0..written]});
    std.debug.print("   Bytes written: {}\n\n", .{written});

    // Example 2: Streaming-like encoding (chunk by chunk)
    std.debug.print("2. Chunk-by-chunk encoding simulation:\n", .{});
    const chunks = [_][]const u8{ "Hello ", "World ", "from ", "Zig!" };
    var all_encoded = std.ArrayList(u8).init(allocator);
    defer all_encoded.deinit();

    for (chunks) |chunk| {
        const encoded_chunk = try base64.encode(allocator, chunk, .{ .padding = false });
        defer allocator.free(encoded_chunk);
        // Note: This is just a demonstration - real streaming requires more complex handling
        // as Base64 encoding crosses chunk boundaries
    }
    std.debug.print("   Note: For real streaming, use a streaming encoder\n\n", .{});

    // Example 3: URL-safe encoding for tokens/URLs
    std.debug.print("3. URL-safe encoding:\n", .{});
    const binary_token = "\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR";
    const token_standard = try base64.encode(allocator, binary_token, .{});
    defer allocator.free(token_standard);
    const token_urlsafe = try base64.encode(allocator, binary_token, .{ .url_safe = true });
    defer allocator.free(token_urlsafe);
    std.debug.print("   Standard: {s}\n", .{token_standard});
    std.debug.print("   URL-safe: {s}\n", .{token_urlsafe});
    std.debug.print("   (Notice +/ replaced with -_)\n\n", .{});

    // Example 4: Decoding with options
    std.debug.print("4. Decoding URL-safe strings:\n", .{});
    const url_safe_input = "YQ-_YQ";
    const decoded_standard = base64.decode(allocator, url_safe_input, .{}) catch |err| blk: {
        std.debug.print("   Standard decode failed: {}\n", .{err});
        break :blk null;
    };
    if (decoded_standard) |d| {
        allocator.free(d);
    }

    const decoded_urlsafe = try base64.decode(allocator, url_safe_input, .{ .url_safe = true });
    defer allocator.free(decoded_urlsafe);
    std.debug.print("   URL-safe decoded: {s}\n\n", .{decoded_urlsafe});

    // Example 5: Binary data (all byte values)
    std.debug.print("5. Binary data handling:\n", .{});
    var all_bytes: [256]u8 = undefined;
    for (0..256) |i| {
        all_bytes[i] = @intCast(i);
    }
    const all_bytes_encoded = try base64.encode(allocator, &all_bytes, .{});
    defer allocator.free(all_bytes_encoded);
    std.debug.print("   All 256 byte values encoded to {} chars\n", .{all_bytes_encoded.len});

    const all_bytes_decoded = try base64.decode(allocator, all_bytes_encoded, .{});
    defer allocator.free(all_bytes_decoded);
    std.debug.print("   Roundtrip verification: {}\n\n", .{std.mem.eql(u8, &all_bytes, all_bytes_decoded)});

    // Example 6: Validation before decoding
    std.debug.print("6. Validation example:\n", .{});
    const test_strings = [_][]const u8{
        "SGVsbG8gV29ybGQ=",
        "Invalid@String",
        "Also===Invalid",
        "",
        "YWJjZA==",
    };
    for (test_strings) |s| {
        const valid = base64.isValid(s, .{});
        std.debug.print("   '{s}' - Valid: {}\n", .{ s, valid });
    }
    std.debug.print("\n", .{});

    // Example 7: Working with files (conceptual)
    std.debug.print("7. File encoding concept:\n", .{});
    std.debug.print("   // Encode a file's contents\n", .{});
    std.debug.print("   const file_data = try cwd.readFileAlloc(allocator, \"input.bin\", max_size);\n", .{});
    std.debug.print("   const encoded = try base64.encode(allocator, file_data, .{{}});\n", .{});
    std.debug.print("   try cwd.writeFile(.{{ .sub_path = \"output.b64\", .data = encoded }});\n", .{});
    std.debug.print("   // Decode back\n", .{});
    std.debug.print("   const decoded = try base64.decode(allocator, encoded, .{{}});\n", .{});
    std.debug.print("   try cwd.writeFile(.{{ .sub_path = \"output.bin\", .data = decoded }});\n", .{});
}