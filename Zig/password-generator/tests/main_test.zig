const std = @import("std");
const password_generator = @import("password-generator");

test "generate password with all options" {
    const allocator = std.testing.allocator;
    const password = try password_generator.generate(allocator, .{
        .length = 20,
        .include_lowercase = true,
        .include_uppercase = true,
        .include_digits = true,
        .include_symbols = true,
    });
    defer allocator.free(password);

    try std.testing.expectEqual(@as(usize, 20), password.len);
}

test "generate password digits only" {
    const allocator = std.testing.allocator;
    const password = try password_generator.generate(allocator, .{
        .length = 8,
        .include_lowercase = false,
        .include_uppercase = false,
        .include_digits = true,
        .include_symbols = false,
    });
    defer allocator.free(password);

    try std.testing.expectEqual(@as(usize, 8), password.len);
    for (password) |c| {
        try std.testing.expect(c >= '0' and c <= '9');
    }
}

test "generate password exclude similar" {
    const allocator = std.testing.allocator;
    const password = try password_generator.generate(allocator, .{
        .length = 16,
        .include_lowercase = true,
        .include_uppercase = true,
        .include_digits = true,
        .exclude_similar = true,
    });
    defer allocator.free(password);

    try std.testing.expectEqual(@as(usize, 16), password.len);
    // Should not contain similar characters
    for (password) |c| {
        try std.testing.expect(c != 'i' and c != 'l' and c != '1' and
            c != 'L' and c != 'o' and c != 'O' and c != '0');
    }
}

test "generate multiple passwords" {
    const allocator = std.testing.allocator;
    const passwords = try password_generator.generateMultiple(allocator, 5, .{
        .length = 12,
    });
    defer {
        for (passwords) |pwd| allocator.free(pwd);
        allocator.free(passwords);
    }

    try std.testing.expectEqual(@as(usize, 5), passwords.len);
    for (passwords) |pwd| {
        try std.testing.expectEqual(@as(usize, 12), pwd.len);
    }
}

test "generate passphrase" {
    const allocator = std.testing.allocator;
    const passphrase = try password_generator.generatePassphrase(allocator, 4, "-");
    defer allocator.free(passphrase);

    // Should contain 3 hyphens (separator between 4 words)
    var hyphen_count: usize = 0;
    for (passphrase) |c| {
        if (c == '-') hyphen_count += 1;
    }
    try std.testing.expectEqual(@as(usize, 3), hyphen_count);
}

test "generate passphrase with space separator" {
    const allocator = std.testing.allocator;
    const passphrase = try password_generator.generatePassphrase(allocator, 3, " ");
    defer allocator.free(passphrase);

    try std.testing.expect(passphrase.len > 0);
}

test "analyze empty password" {
    const result = password_generator.analyze("");
    try std.testing.expectEqual(@as(usize, 0), result.length);
    try std.testing.expectEqual(@as(u8, 0), result.score);
}

test "analyze weak password" {
    const result = password_generator.analyze("abc");
    try std.testing.expect(result.has_lowercase);
    try std.testing.expect(!result.has_uppercase);
    try std.testing.expect(!result.has_digits);
    try std.testing.expect(!result.has_symbols);
    try std.testing.expect(result.score < 50);
}

test "analyze strong password" {
    const result = password_generator.analyze("MyStr0ng!Pass#2024");
    try std.testing.expect(result.has_lowercase);
    try std.testing.expect(result.has_uppercase);
    try std.testing.expect(result.has_digits);
    try std.testing.expect(result.has_symbols);
    try std.testing.expect(result.score >= 80);
}

test "analyze entropy calculation" {
    // Password with all character types should have high entropy
    const result = password_generator.analyze("Aa1!Bb2@Cc3#");
    try std.testing.expect(result.entropy > 0);
}

test "generate pin" {
    const allocator = std.testing.allocator;
    const pin = try password_generator.generatePin(allocator, 4);
    defer allocator.free(pin);

    try std.testing.expectEqual(@as(usize, 4), pin.len);
    for (pin) |c| {
        try std.testing.expect(c >= '0' and c <= '9');
    }
}

test "generate pin 6 digits" {
    const allocator = std.testing.allocator;
    const pin = try password_generator.generatePin(allocator, 6);
    defer allocator.free(pin);

    try std.testing.expectEqual(@as(usize, 6), pin.len);
}

test "common pattern detection - ascending" {
    try std.testing.expect(password_generator.hasCommonPatterns("abc123"));
    try std.testing.expect(password_generator.hasCommonPatterns("xyz789"));
    try std.testing.expect(password_generator.hasCommonPatterns("123abc"));
}

test "common pattern detection - repeated" {
    try std.testing.expect(password_generator.hasCommonPatterns("aaa111"));
    try std.testing.expect(password_generator.hasCommonPatterns("passwordddd"));
}

test "common pattern detection - none" {
    try std.testing.expect(!password_generator.hasCommonPatterns("x7Km9P"));
    try std.testing.expect(!password_generator.hasCommonPatterns("randomPass!"));
}

test "charset constants" {
    try std.testing.expectEqual(@as(usize, 26), password_generator.CharSets.lowercase.len);
    try std.testing.expectEqual(@as(usize, 26), password_generator.CharSets.uppercase.len);
    try std.testing.expectEqual(@as(usize, 10), password_generator.CharSets.digits.len);
}

test "error handling - zero length" {
    const allocator = std.testing.allocator;
    const result = password_generator.generate(allocator, .{ .length = 0 });
    try std.testing.expectError(error.ZeroLength, result);
}

test "error handling - empty charset" {
    const allocator = std.testing.allocator;
    const result = password_generator.generate(allocator, .{
        .length = 10,
        .include_lowercase = false,
        .include_uppercase = false,
        .include_digits = false,
        .include_symbols = false,
    });
    try std.testing.expectError(error.EmptyCharSet, result);
}

test "password uniqueness" {
    const allocator = std.testing.allocator;
    const password1 = try password_generator.generate(allocator, .{ .length = 16 });
    defer allocator.free(password1);
    const password2 = try password_generator.generate(allocator, .{ .length = 16 });
    defer allocator.free(password2);

    // Two generated passwords should be different (extremely unlikely to be same)
    try std.testing.expect(!std.mem.eql(u8, password1, password2));
}