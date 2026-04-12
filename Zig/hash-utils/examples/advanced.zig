const std = @import("std");
const hash = @import("hash-utils");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    const allocator = std.heap.page_allocator;

    try stdout.print("=== Hash Utils - Advanced Examples ===\n\n", .{});

    // Incremental hashing
    try stdout.print("--- Incremental Hashing ---\n", .{});
    {
        var ctx = hash.Sha256.init();
        ctx.update("Hello");
        ctx.update(", ");
        ctx.update("World!");
        var digest: [32]u8 = undefined;
        ctx.final(&digest);
        
        const hex = try hash.toHex(allocator, &digest);
        defer allocator.free(hex);
        try stdout.print("Incremental SHA256: {s}\n", .{hex});

        // Verify it matches one-shot hash
        const one_shot = try hash.Sha256.hashHex(allocator, "Hello, World!");
        defer allocator.free(one_shot);
        try stdout.print("One-shot SHA256:     {s}\n", .{one_shot});
        try stdout.print("Match: {}\n", .{std.mem.eql(u8, hex, one_shot)});
    }

    // HMAC
    try stdout.print("\n--- HMAC ---\n", .{});
    {
        const key = "secret_key";
        const message = "Important message to authenticate";
        
        const hmac_sha256 = try hash.HmacSha256.hashHex(allocator, key, message);
        defer allocator.free(hmac_sha256);
        try stdout.print("HMAC-SHA256(key, message) = {s}\n", .{hmac_sha256});

        const hmac_sha512 = try hash.HmacSha512.hashHex(allocator, key, message);
        defer allocator.free(hmac_sha512);
        try stdout.print("HMAC-SHA512(key, message) = {s}\n", .{hmac_sha512});
    }

    // PBKDF2
    try stdout.print("\n--- PBKDF2 Key Derivation ---\n", .{});
    {
        const password = "user_password_123";
        const salt = "random_salt_value";
        const iterations: u32 = 10000;
        const key_len: usize = 32;

        const derived = try hash.pbkdf2Sha256Hex(allocator, password, salt, iterations, key_len);
        defer allocator.free(derived);
        try stdout.print("PBKDF2-SHA256(password, salt, 10000, 32) = {s}\n", .{derived});
    }

    // Hex conversion
    try stdout.print("\n--- Hex Conversion ---\n", .{});
    {
        const bytes = [_]u8{ 0xde, 0xad, 0xbe, 0xef, 0xca, 0xfe, 0xba, 0xbe };
        
        const hex_lower = try hash.toHex(allocator, &bytes);
        defer allocator.free(hex_lower);
        try stdout.print("Lowercase hex: {s}\n", .{hex_lower});

        const hex_upper = try hash.toHexUpper(allocator, &bytes);
        defer allocator.free(hex_upper);
        try stdout.print("Uppercase hex: {s}\n", .{hex_upper});

        const decoded = try hash.fromHex(allocator, hex_lower);
        defer allocator.free(decoded);
        try stdout.print("Decoded back: ", .{});
        for (decoded) |b| {
            try stdout.print("{x:0>2} ", .{b});
        }
        try stdout.print("\n", .{});

        try stdout.print("isValidHex('{s}'): {}\n", .{ hex_lower, hash.isValidHex(hex_lower) });
        try stdout.print("isValidHex('invalid!'): {}\n", .{hash.isValidHex("invalid!")});
    }

    // Buffer operations
    try stdout.print("\n--- Buffer Operations ---\n", .{});
    {
        var buffer: [64]u8 = undefined;
        const len = try hash.hashInto(&buffer, "test data", .sha256);
        
        const hex = try hash.toHex(allocator, buffer[0..len]);
        defer allocator.free(hex);
        try stdout.print("hashInto (SHA-256): {s}\n", .{hex});

        var hex_buffer: [128]u8 = undefined;
        const hex_len = try hash.hashHexInto(&hex_buffer, "test data", .sha256);
        try stdout.print("hashHexInto (SHA-256): {s}\n", .{hex_buffer[0..hex_len]});
    }

    // Algorithm info
    try stdout.print("\n--- Algorithm Info ---\n", .{});
    inline for (.{
        .{ hash.HashAlgorithm.md5, "MD5" },
        .{ hash.HashAlgorithm.sha1, "SHA-1" },
        .{ hash.HashAlgorithm.sha256, "SHA-256" },
        .{ hash.HashAlgorithm.sha512, "SHA-512" },
    }) |item| {
        const algo = item[0];
        const name = item[1];
        try stdout.print("{s}: digest_size={}, hex_length={}\n", .{
            name,
            algo.digestSize(),
            algo.hexLen(),
        });
    }

    // File hashing simulation
    try stdout.print("\n--- File Hashing Simulation ---\n", .{});
    {
        const file_content = "This is the content of a file.\nIt has multiple lines.\n";
        
        var sha256_ctx = hash.Sha256.init();
        sha256_ctx.update(file_content);
        var digest: [32]u8 = undefined;
        sha256_ctx.final(&digest);
        
        const hex = try hash.toHex(allocator, &digest);
        defer allocator.free(hex);
        try stdout.print("SHA-256 of file content: {s}\n", .{hex});
    }

    try stdout.print("\n=== All tests completed ===\n", .{});
}