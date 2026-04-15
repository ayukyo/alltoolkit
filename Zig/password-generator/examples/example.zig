const std = @import("std");
const password_generator = @import("password-generator");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    const stdout = std.io.getStdOut().writer();

    try stdout.print("=== Zig Password Generator Examples ===\n\n", .{});

    // Example 1: Basic password
    try stdout.print("1. Basic 16-character password:\n", .{});
    const basic = try password_generator.generate(allocator, .{});
    defer allocator.free(basic);
    try stdout.print("   {s}\n\n", .{basic});

    // Example 2: Password with symbols
    try stdout.print("2. Password with symbols (20 chars):\n", .{});
    const with_symbols = try password_generator.generate(allocator, .{
        .length = 20,
        .include_symbols = true,
    });
    defer allocator.free(with_symbols);
    try stdout.print("   {s}\n\n", .{with_symbols});

    // Example 3: Digits only
    try stdout.print("3. Digits only (8 chars):\n", .{});
    const digits_only = try password_generator.generate(allocator, .{
        .length = 8,
        .include_lowercase = false,
        .include_uppercase = false,
        .include_digits = true,
        .include_symbols = false,
    });
    defer allocator.free(digits_only);
    try stdout.print("   {s}\n\n", .{digits_only});

    // Example 4: Excluding similar characters
    try stdout.print("4. Password without similar chars (i,l,1,L,o,O,0):\n", .{});
    const no_similar = try password_generator.generate(allocator, .{
        .length = 16,
        .exclude_similar = true,
    });
    defer allocator.free(no_similar);
    try stdout.print("   {s}\n\n", .{no_similar});

    // Example 5: Custom character set
    try stdout.print("5. Custom character set (hex): 0-9, a-f\n", .{});
    const hex_password = try password_generator.generate(allocator, .{
        .length = 16,
        .custom_charset = "0123456789abcdef",
    });
    defer allocator.free(hex_password);
    try stdout.print("   {s}\n\n", .{hex_password});

    // Example 6: Generate multiple passwords
    try stdout.print("6. Generate 5 passwords:\n", .{});
    const passwords = try password_generator.generateMultiple(allocator, 5, .{
        .length = 12,
        .include_symbols = true,
    });
    defer {
        for (passwords) |pwd| allocator.free(pwd);
        allocator.free(passwords);
    }
    for (passwords, 1..) |pwd, i| {
        try stdout.print("   {}. {s}\n", .{ i, pwd });
    }
    try stdout.print("\n", .{});

    // Example 7: Generate passphrase
    try stdout.print("7. Passphrase (4 words):\n", .{});
    const passphrase = try password_generator.generatePassphrase(allocator, 4, "-");
    defer allocator.free(passphrase);
    try stdout.print("   {s}\n\n", .{passphrase});

    // Example 8: Generate PIN
    try stdout.print("8. Generate PIN codes:\n", .{});
    inline for ([_]usize{ 4, 6, 8 }) |pin_len| {
        const pin = try password_generator.generatePin(allocator, pin_len);
        defer allocator.free(pin);
        try stdout.print("   {}-digit PIN: {s}\n", .{ pin_len, pin });
    }
    try stdout.print("\n", .{});

    // Example 9: Analyze password strength
    try stdout.print("9. Password strength analysis:\n\n", .{});
    const test_passwords = [_][]const u8{
        "password",
        "Password1",
        "MyP@ssw0rd!2024",
        "Tr0ub4dor&3",
        "correct-horse-battery-staple",
    };

    for (test_passwords) |pwd| {
        const analysis = password_generator.analyze(pwd);
        try stdout.print("   '{s}':\n", .{pwd});
        try stdout.print("     Score: {}/100 ({s})\n", .{ analysis.score, analysis.rating });
        try stdout.print("     Entropy: {d:.2} bits\n", .{analysis.entropy});
        try stdout.print("     Contains: {s}{s}{s}{s}\n\n", .{
            if (analysis.has_lowercase) "lowercase " else "",
            if (analysis.has_uppercase) "uppercase " else "",
            if (analysis.has_digits) "digits " else "",
            if (analysis.has_symbols) "symbols" else "",
        });
    }

    // Example 10: Pattern detection
    try stdout.print("10. Common pattern detection:\n", .{});
    const pattern_tests = [_][]const u8{
        "abc123",
        "aaa111",
        "x7Km9P",
        "qwerty",
    };

    for (pattern_tests) |pwd| {
        const has_pattern = password_generator.hasCommonPatterns(pwd);
        try stdout.print("   '{s}': {s}\n", .{
            pwd,
            if (has_pattern) "has patterns" else "no patterns",
        });
    }

    try stdout.print("\n=== Examples Complete ===\n", .{});
}