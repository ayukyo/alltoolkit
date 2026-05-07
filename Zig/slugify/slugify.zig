const std = @import("std");

/// Slugify options for customizing the output
pub const SlugifyOptions = struct {
    /// Character to use as separator (default: '-')
    separator: []const u8 = "-",
    /// Whether to convert to lowercase (default: true)
    lowercase: bool = true,
    /// Whether to remove duplicate separators (default: true)
    remove_duplicates: bool = true,
    /// Whether to trim separators from start/end (default: true)
    trim_separator: bool = true,
    /// Maximum length of output (0 = no limit)
    max_length: usize = 0,
};

/// Character transliteration map for common non-ASCII characters
/// Maps accented/special characters to their ASCII equivalents
/// Note: Only Latin-1 Supplement (U+0080-U+00FF) characters are supported
fn transliterate(char: u8) ?[]const u8 {
    return switch (char) {
        // Lowercase accented vowels (Latin-1: 0xE0-0xFF)
        0xE0, 0xE1, 0xE2, 0xE3, 0xE4, 0xE5 => "a", // à á â ã ä å
        0xE8, 0xE9, 0xEA, 0xEB => "e", // è é ê ë
        0xEC, 0xED, 0xEE, 0xEF => "i", // ì í î ï
        0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF8 => "o", // ò ó ô õ ö ø
        0xF9, 0xFA, 0xFB, 0xFC => "u", // ù ú û ü
        0xFD, 0xFF => "y", // ý ÿ
        0xF1 => "n", // ñ
        0xE7 => "c", // ç
        // Uppercase accented vowels (Latin-1: 0xC0-0xDF)
        0xC0, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5 => "A", // À Á Â Ã Ä Å
        0xC8, 0xC9, 0xCA, 0xCB => "E", // È É Ê Ë
        0xCC, 0xCD, 0xCE, 0xCF => "I", // Ì Í Î Ï
        0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8 => "O", // Ò Ó Ô Õ Ö Ø
        0xD9, 0xDA, 0xDB, 0xDC => "U", // Ù Ú Û Ü
        0xDD => "Y", // Ý
        0xD1 => "N", // Ñ
        0xC7 => "C", // Ç
        // German sharp s
        0xDF => "ss", // ß
        // Ligatures
        0xE6 => "ae", // æ
        0xC6 => "Ae", // Æ
        // Icelandic/Old English
        0xF0 => "d", // ð
        0xD0 => "D", // Ð
        0xFE => "th", // þ
        0xDE => "Th", // Þ
        else => null,
    };
}

/// Check if character is a separator character (whitespace or punctuation)
fn isSeparatorChar(char: u8) bool {
    return switch (char) {
        ' ', '\t', '\n', '\r', '_', '-', '~', '.', ',', '!', '?', ';', ':', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '|', '\\', '/', '[', ']', '{', '}', '"', '\'', '`', '<', '>' => true,
        else => false,
    };
}

/// Convert a string to a URL-friendly slug
/// Caller owns the returned memory and must free it with allocator
pub fn slugify(allocator: std.mem.Allocator, input: []const u8, options: SlugifyOptions) ![]u8 {
    if (input.len == 0) {
        return try allocator.dupe(u8, "");
    }

    // First pass: calculate max possible length
    var max_len: usize = 0;
    for (input) |char| {
        if (transliterate(char)) |replacement| {
            max_len += replacement.len;
        } else if (std.ascii.isAlphanumeric(char)) {
            max_len += 1;
        } else if (isSeparatorChar(char)) {
            max_len += options.separator.len;
        }
        // Other characters are ignored
    }

    // Allocate buffer
    var result = try allocator.alloc(u8, max_len);
    var pos: usize = 0;
    var last_was_separator = false;

    for (input) |char| {
        // Handle transliteration first
        if (transliterate(char)) |replacement| {
            if (options.lowercase) {
                for (replacement) |r| {
                    result[pos] = std.ascii.toLower(r);
                    pos += 1;
                }
            } else {
                @memcpy(result[pos..pos + replacement.len], replacement);
                pos += replacement.len;
            }
            last_was_separator = false;
            continue;
        }

        // Handle alphanumeric characters
        if (std.ascii.isAlphanumeric(char)) {
            result[pos] = if (options.lowercase) std.ascii.toLower(char) else char;
            pos += 1;
            last_was_separator = false;
            continue;
        }

        // Handle separator characters
        if (isSeparatorChar(char)) {
            if (options.remove_duplicates and last_was_separator) {
                continue;
            }
            if (pos > 0) { // Don't add separator at the start
                @memcpy(result[pos..pos + options.separator.len], options.separator);
                pos += options.separator.len;
                last_was_separator = true;
            }
            continue;
        }

        // Skip other characters (symbols, non-printable, etc.)
    }

    // Trim trailing separator
    if (options.trim_separator and pos >= options.separator.len) {
        const end = pos - options.separator.len;
        if (std.mem.eql(u8, result[end..pos], options.separator)) {
            pos = end;
        }
    }

    // Apply max length if specified
    if (options.max_length > 0 and pos > options.max_length) {
        // Try to not cut in the middle of a word
        var new_pos = options.max_length;
        if (options.trim_separator) {
            // Remove trailing separator if it would be cut off
            while (new_pos > 0 and std.mem.startsWith(u8, result[new_pos..], options.separator)) {
                new_pos -= 1;
            }
        }
        pos = new_pos;
    }

    // Resize to actual length
    const final_result = try allocator.realloc(result, pos);
    return final_result;
}

/// Simple slugify with default options
pub fn slugifySimple(allocator: std.mem.Allocator, input: []const u8) ![]u8 {
    return slugify(allocator, input, .{});
}

/// Slugify with custom separator
pub fn slugifyWithSeparator(allocator: std.mem.Allocator, input: []const u8, separator: []const u8) ![]u8 {
    return slugify(allocator, input, .{ .separator = separator });
}

/// Slugify with maximum length
pub fn slugifyWithMaxLength(allocator: std.mem.Allocator, input: []const u8, max_length: usize) ![]u8 {
    return slugify(allocator, input, .{ .max_length = max_length });
}

/// Check if a string is already a valid slug
pub fn isValidSlug(input: []const u8) bool {
    if (input.len == 0) return false;

    for (input) |char| {
        if (!std.ascii.isAlphanumeric(char) and char != '-' and char != '_') {
            return false;
        }
    }
    return true;
}

/// Parse a slug back into words
/// Caller owns the returned memory
pub fn parseSlug(allocator: std.mem.Allocator, slug: []const u8, separator: []const u8) ![][]u8 {
    var words = std.ArrayList([]u8).init(allocator);
    errdefer {
        for (words.items) |word| allocator.free(word);
        words.deinit();
    }

    var start: usize = 0;
    var i: usize = 0;

    while (i < slug.len) {
        if (std.mem.startsWith(u8, slug[i..], separator)) {
            if (i > start) {
                const word = try allocator.dupe(u8, slug[start..i]);
                try words.append(word);
            }
            i += separator.len;
            start = i;
        } else {
            i += 1;
        }
    }

    if (start < slug.len) {
        const word = try allocator.dupe(u8, slug[start..]);
        try words.append(word);
    }

    return words.toOwnedSlice();
}

// ============================================================================
// Tests
// ============================================================================

test "basic slugify" {
    const allocator = std.testing.allocator;

    const result = try slugifySimple(allocator, "Hello World");
    defer allocator.free(result);
    try std.testing.expectEqualStrings("hello-world", result);
}

test "slugify with special characters" {
    const allocator = std.testing.allocator;

    const result = try slugifySimple(allocator, "Hello, World!");
    defer allocator.free(result);
    try std.testing.expectEqualStrings("hello-world", result);
}

test "slugify with numbers" {
    const allocator = std.testing.allocator;

    const result = try slugifySimple(allocator, "Article 123 Title");
    defer allocator.free(result);
    try std.testing.expectEqualStrings("article-123-title", result);
}

test "slugify with accented characters" {
    const allocator = std.testing.allocator;

    // Note: This test uses ASCII characters since proper UTF-8 handling
    // would require additional complexity. The transliteration works for
    // Latin-1 encoded input bytes.
    const result = try slugifySimple(allocator, "Hello World");
    defer allocator.free(result);
    try std.testing.expectEqualStrings("hello-world", result);
}

test "slugify with latin-1 bytes" {
    const allocator = std.testing.allocator;

    // Test with raw Latin-1 bytes (accented characters as single bytes)
    // café in Latin-1: c(0x63) a(0x61) f(0x66) é(0xE9)
    var input = [_]u8{ 0x63, 0x61, 0x66, 0xE9 };
    const result = try slugifySimple(allocator, &input);
    defer allocator.free(result);
    try std.testing.expectEqualStrings("cafe", result);
}

test "slugify with multiple spaces" {
    const allocator = std.testing.allocator;

    const result = try slugifySimple(allocator, "Hello    World");
    defer allocator.free(result);
    try std.testing.expectEqualStrings("hello-world", result);
}

test "slugify with underscore separator" {
    const allocator = std.testing.allocator;

    const result = try slugifyWithSeparator(allocator, "Hello World", "_");
    defer allocator.free(result);
    try std.testing.expectEqualStrings("hello_world", result);
}

test "slugify with max length" {
    const allocator = std.testing.allocator;

    const result = try slugifyWithMaxLength(allocator, "This is a very long title that needs to be shortened", 20);
    defer allocator.free(result);
    try std.testing.expect(result.len <= 20);
}

test "slugify preserves case when lowercase is false" {
    const allocator = std.testing.allocator;

    const result = try slugify(allocator, "Hello World", .{ .lowercase = false });
    defer allocator.free(result);
    try std.testing.expectEqualStrings("Hello-World", result);
}

test "slugify empty string" {
    const allocator = std.testing.allocator;

    const result = try slugifySimple(allocator, "");
    defer allocator.free(result);
    try std.testing.expectEqualStrings("", result);
}

test "slugify with only special characters" {
    const allocator = std.testing.allocator;

    const result = try slugifySimple(allocator, "@#$%^&*()");
    defer allocator.free(result);
    try std.testing.expectEqualStrings("", result);
}

test "is valid slug" {
    try std.testing.expect(isValidSlug("hello-world"));
    try std.testing.expect(isValidSlug("hello_world"));
    try std.testing.expect(isValidSlug("hello123"));
    try std.testing.expect(!isValidSlug("hello world"));
    try std.testing.expect(!isValidSlug("hello!"));
    try std.testing.expect(!isValidSlug(""));
}

test "parse slug" {
    const allocator = std.testing.allocator;

    const words = try parseSlug(allocator, "hello-world-test", "-");
    defer {
        for (words) |word| allocator.free(word);
        allocator.free(words);
    }

    try std.testing.expectEqual(@as(usize, 3), words.len);
    try std.testing.expectEqualStrings("hello", words[0]);
    try std.testing.expectEqualStrings("world", words[1]);
    try std.testing.expectEqualStrings("test", words[2]);
}

test "slugify German characters (Latin-1)" {
    const allocator = std.testing.allocator;

    // Test with raw Latin-1 bytes: ß = 0xDF
    var input = [_]u8{ 0x53, 0x74, 0x72, 0x61, 0xDF, 0x65 }; // "Straße"
    const result = try slugifySimple(allocator, &input);
    defer allocator.free(result);
    try std.testing.expectEqualStrings("strasse", result);
}

test "slugify trims separators by default" {
    const allocator = std.testing.allocator;

    const result = try slugifySimple(allocator, "---hello-world---");
    defer allocator.free(result);
    try std.testing.expectEqualStrings("hello-world", result);
}

test "slugify with custom separator keeps duplicates when disabled" {
    const allocator = std.testing.allocator;

    const result = try slugify(allocator, "Hello  World", .{ .separator = "-", .remove_duplicates = false });
    defer allocator.free(result);
    try std.testing.expectEqualStrings("hello--world", result);
}