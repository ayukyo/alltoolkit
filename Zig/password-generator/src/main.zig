const std = @import("std");

/// Character sets for password generation
pub const CharSets = struct {
    pub const lowercase: []const u8 = "abcdefghijklmnopqrstuvwxyz";
    pub const uppercase: []const u8 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    pub const digits: []const u8 = "0123456789";
    pub const symbols: []const u8 = "!@#$%^&*()_+-=[]{}|;:,.<>?";
    pub const similar: []const u8 = "il1Lo0O";

    /// Get alphanumeric characters (letters + digits)
    pub fn alphanumeric() []const u8 {
        return lowercase ++ uppercase ++ digits;
    }

    /// Get all characters including symbols
    pub fn all() []const u8 {
        return lowercase ++ uppercase ++ digits ++ symbols;
    }

    /// Get all characters excluding similar-looking ones
    pub fn noSimilar() []const u8 {
        return "abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789";
    }
};

/// Password generation options
pub const PasswordOptions = struct {
    length: usize = 16,
    include_lowercase: bool = true,
    include_uppercase: bool = true,
    include_digits: bool = true,
    include_symbols: bool = false,
    exclude_similar: bool = false,
    custom_charset: ?[]const u8 = null,
};

/// Password analysis result
pub const PasswordStrength = struct {
    score: u8, // 0-100
    entropy: f64,
    length: usize,
    has_lowercase: bool,
    has_uppercase: bool,
    has_digits: bool,
    has_symbols: bool,
    rating: []const u8,

    pub fn format(
        self: PasswordStrength,
        comptime fmt: []const u8,
        options: std.fmt.FormatOptions,
        writer: anytype,
    ) !void {
        _ = fmt;
        _ = options;
        try writer.print(
            \\Password Strength Analysis:
            \\  Score: {}/100
            \\  Entropy: {d:.2} bits
            \\  Length: {}
            \\  Contains: {s}{s}{s}{s}
            \\  Rating: {s}
        , .{
            self.score,
            self.entropy,
            self.length,
            if (self.has_lowercase) "lowercase " else "",
            if (self.has_uppercase) "uppercase " else "",
            if (self.has_digits) "digits " else "",
            if (self.has_symbols) "symbols" else "",
            self.rating,
        });
    }
};

/// Generate a cryptographically secure random password
pub fn generate(allocator: std.mem.Allocator, options: PasswordOptions) ![]u8 {
    if (options.length == 0) {
        return error.ZeroLength;
    }
    if (options.length > 1024) {
        return error.TooLong;
    }

    // Build character set
    var charset_buf: [256]u8 = undefined;
    var charset_len: usize = 0;

    if (options.custom_charset) |custom| {
        // Use custom charset directly
        const result = try allocator.alloc(u8, options.length);
        errdefer allocator.free(result);

        for (result) |*c| {
            const idx = std.crypto.random.intRangeAtMost(usize, 0, custom.len - 1);
            c.* = custom[idx];
        }
        return result;
    }

    // Build charset from options
    if (options.exclude_similar) {
        if (options.include_lowercase) {
            const set = "abcdefghjkmnpqrstuvwxyz";
            @memcpy(charset_buf[charset_len..][0..set.len], set);
            charset_len += set.len;
        }
        if (options.include_uppercase) {
            const set = "ABCDEFGHJKMNPQRSTUVWXYZ";
            @memcpy(charset_buf[charset_len..][0..set.len], set);
            charset_len += set.len;
        }
        if (options.include_digits) {
            const set = "23456789";
            @memcpy(charset_buf[charset_len..][0..set.len], set);
            charset_len += set.len;
        }
    } else {
        if (options.include_lowercase) {
            @memcpy(charset_buf[charset_len..][0..CharSets.lowercase.len], CharSets.lowercase);
            charset_len += CharSets.lowercase.len;
        }
        if (options.include_uppercase) {
            @memcpy(charset_buf[charset_len..][0..CharSets.uppercase.len], CharSets.uppercase);
            charset_len += CharSets.uppercase.len;
        }
        if (options.include_digits) {
            @memcpy(charset_buf[charset_len..][0..CharSets.digits.len], CharSets.digits);
            charset_len += CharSets.digits.len;
        }
    }

    if (options.include_symbols) {
        @memcpy(charset_buf[charset_len..][0..CharSets.symbols.len], CharSets.symbols);
        charset_len += CharSets.symbols.len;
    }

    if (charset_len == 0) {
        return error.EmptyCharSet;
    }

    const charset = charset_buf[0..charset_len];
    const password = try allocator.alloc(u8, options.length);
    errdefer allocator.free(password);

    for (password) |*c| {
        const idx = std.crypto.random.intRangeAtMost(usize, 0, charset.len - 1);
        c.* = charset[idx];
    }

    return password;
}

/// Generate multiple passwords at once
pub fn generateMultiple(
    allocator: std.mem.Allocator,
    count: usize,
    options: PasswordOptions,
) ![][]u8 {
    if (count == 0) return error.ZeroCount;
    if (count > 10000) return error.TooMany;

    const passwords = try allocator.alloc([]u8, count);
    errdefer allocator.free(passwords);

    for (passwords, 0..) |*pwd, i| {
        _ = i;
        pwd.* = try generate(allocator, options);
    }

    return passwords;
}

/// Generate a memorable passphrase using word lists
pub fn generatePassphrase(
    allocator: std.mem.Allocator,
    word_count: usize,
    separator: []const u8,
) ![]u8 {
    // Simplified word list (in real usage, would load from file)
    const words = [_][]const u8{
        "apple",   "banana", "cherry", "dragon", "eagle",
        "forest",  "garden", "harbor", "island", "jungle",
        "kitchen", "lemon",  "market", "night",  "ocean",
        "planet",  "queen",  "river",  "summer", "tower",
        "unity",   "valley", "winter", "yellow", "zebra",
        "anchor",  "bridge", "cloud",  "dream",  "earth",
        "flame",   "grain",  "heart",  "light",  "music",
        "noble",   "peace",  "quick",  "robin",  "storm",
        "tiger",   "vivid",  "water",  "youth",  "azure",
    };

    if (word_count == 0) return error.ZeroWordCount;
    if (word_count > 20) return error.TooManyWords;

    // Calculate total length needed
    var total_len: usize = 0;
    var chosen_words = try allocator.alloc([]const u8, word_count);
    defer allocator.free(chosen_words);

    for (0..word_count) |i| {
        const idx = std.crypto.random.intRangeAtMost(usize, 0, words.len - 1);
        chosen_words[i] = words[idx];
        total_len += words[idx].len;
    }
    total_len += separator.len * (word_count - 1);

    var result = try allocator.alloc(u8, total_len);
    var pos: usize = 0;

    for (chosen_words, 0..) |word, i| {
        @memcpy(result[pos..][0..word.len], word);
        pos += word.len;
        if (i < word_count - 1) {
            @memcpy(result[pos..][0..separator.len], separator);
            pos += separator.len;
        }
    }

    return result;
}

/// Analyze password strength
pub fn analyze(password: []const u8) PasswordStrength {
    var has_lowercase: bool = false;
    var has_uppercase: bool = false;
    var has_digits: bool = false;
    var has_symbols: bool = false;

    for (password) |c| {
        if (c >= 'a' and c <= 'z') has_lowercase = true
        else if (c >= 'A' and c <= 'Z') has_uppercase = true
        else if (c >= '0' and c <= '9') has_digits = true
        else has_symbols = true;
    }

    // Calculate charset size
    var charset_size: usize = 0;
    if (has_lowercase) charset_size += 26;
    if (has_uppercase) charset_size += 26;
    if (has_digits) charset_size += 10;
    if (has_symbols) charset_size += 25;

    // Calculate entropy: log2(charset_size^length) = length * log2(charset_size)
    const entropy: f64 = if (charset_size > 0)
        @as(f64, @floatFromInt(password.len)) * std.math.log2(@as(f64, @floatFromInt(charset_size)))
    else
        0;

    // Calculate score (0-100)
    var score: u8 = 0;

    // Length scoring (up to 40 points)
    score += if (password.len >= 16) 40
    else if (password.len >= 12) 32
    else if (password.len >= 8) 24
    else if (password.len >= 6) 16
    else @intCast(password.len * 4);

    // Diversity scoring (up to 40 points)
    if (has_lowercase) score += 10;
    if (has_uppercase) score += 10;
    if (has_digits) score += 10;
    if (has_symbols) score += 10;

    // Entropy bonus (up to 20 points)
    if (entropy >= 80) score += 20
    else if (entropy >= 60) score += 15
    else if (entropy >= 40) score += 10
    else if (entropy >= 20) score += 5;

    // Cap at 100
    if (score > 100) score = 100;

    const rating: []const u8 = if (score >= 80) "Very Strong"
    else if (score >= 60) "Strong"
    else if (score >= 40) "Moderate"
    else if (score >= 20) "Weak"
    else
        "Very Weak";

    return .{
        .score = score,
        .entropy = entropy,
        .length = password.len,
        .has_lowercase = has_lowercase,
        .has_uppercase = has_uppercase,
        .has_digits = has_digits,
        .has_symbols = has_symbols,
        .rating = rating,
    };
}

/// Generate a PIN code
pub fn generatePin(allocator: std.mem.Allocator, length: usize) ![]u8 {
    if (length == 0) return error.ZeroLength;
    if (length > 20) return error.TooLong;

    const pin = try allocator.alloc(u8, length);
    for (pin) |*c| {
        c.* = @as(u8, std.crypto.random.intRangeAtMost(u4, 0, 9)) + '0';
    }
    return pin;
}

/// Check if password contains common patterns
pub fn hasCommonPatterns(password: []const u8) bool {
    if (password.len < 3) return false;

    // Check for sequential characters
    for (0..password.len - 2) |i| {
        const c1 = password[i];
        const c2 = password[i + 1];
        const c3 = password[i + 2];

        // Ascending sequences (abc, 123)
        if (c2 == c1 + 1 and c3 == c2 + 1) return true;
        // Descending sequences (cba, 321)
        if (c2 == c1 - 1 and c3 == c2 - 1) return true;
        // Repeated characters (aaa, 111)
        if (c1 == c2 and c2 == c3) return true;
    }

    return false;
}

test "generate basic password" {
    const allocator = std.testing.allocator;
    const password = try generate(allocator, .{ .length = 16 });
    defer allocator.free(password);

    try std.testing.expectEqual(@as(usize, 16), password.len);
}

test "generate password with custom charset" {
    const allocator = std.testing.allocator;
    const password = try generate(allocator, .{
        .length = 10,
        .custom_charset = "abc123",
    });
    defer allocator.free(password);

    try std.testing.expectEqual(@as(usize, 10), password.len);
    for (password) |c| {
        try std.testing.expect(c == 'a' or c == 'b' or c == 'c' or
            c == '1' or c == '2' or c == '3');
    }
}

test "generate passphrase" {
    const allocator = std.testing.allocator;
    const passphrase = try generatePassphrase(allocator, 4, "-");
    defer allocator.free(passphrase);

    try std.testing.expect(passphrase.len > 0);
}

test "analyze password strength" {
    const result = analyze("MyP@ssw0rd!2024");
    try std.testing.expect(result.has_lowercase);
    try std.testing.expect(result.has_uppercase);
    try std.testing.expect(result.has_digits);
    try std.testing.expect(result.has_symbols);
    try std.testing.expect(result.score > 60);
}

test "generate pin" {
    const allocator = std.testing.allocator;
    const pin = try generatePin(allocator, 6);
    defer allocator.free(pin);

    try std.testing.expectEqual(@as(usize, 6), pin.len);
    for (pin) |c| {
        try std.testing.expect(c >= '0' and c <= '9');
    }
}

test "detect common patterns" {
    try std.testing.expect(hasCommonPatterns("abc123"));
    try std.testing.expect(hasCommonPatterns("aaa111"));
    try std.testing.expect(!hasCommonPatterns("x7Km9P"));
}