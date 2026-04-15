const std = @import("std");

/// String operation errors
pub const StringError = error{
    OutOfMemory,
    InvalidUtf8,
    InvalidIndex,
    BufferTooSmall,
};

// ============================================================================
// Trimming Functions
// ============================================================================

/// Remove leading and trailing whitespace
pub fn trim(allocator: std.mem.Allocator, input: []const u8) StringError![]u8 {
    return trimChars(allocator, input, " \t\n\r");
}

/// Remove leading and trailing specified characters
pub fn trimChars(allocator: std.mem.Allocator, input: []const u8, chars_to_trim: []const u8) StringError![]u8 {
    const start = findFirstNotOf(input, chars_to_trim) orelse return allocator.dupe(u8, "");
    const end = findLastNotOf(input, chars_to_trim) orelse return allocator.dupe(u8, "");
    
    if (start > end) {
        return allocator.dupe(u8, "");
    }
    
    return allocator.dupe(u8, input[start .. end + 1]);
}

/// Remove leading whitespace
pub fn trimLeft(allocator: std.mem.Allocator, input: []const u8) StringError![]u8 {
    return trimLeftChars(allocator, input, " \t\n\r");
}

/// Remove leading specified characters
pub fn trimLeftChars(allocator: std.mem.Allocator, input: []const u8, chars_to_trim: []const u8) StringError![]u8 {
    const start = findFirstNotOf(input, chars_to_trim) orelse return allocator.dupe(u8, "");
    return allocator.dupe(u8, input[start..]);
}

/// Remove trailing whitespace
pub fn trimRight(allocator: std.mem.Allocator, input: []const u8) StringError![]u8 {
    return trimRightChars(allocator, input, " \t\n\r");
}

/// Remove trailing specified characters
pub fn trimRightChars(allocator: std.mem.Allocator, input: []const u8, chars_to_trim: []const u8) StringError![]u8 {
    const end = findLastNotOf(input, chars_to_trim) orelse return allocator.dupe(u8, "");
    return allocator.dupe(u8, input[0 .. end + 1]);
}

// ============================================================================
// Case Conversion
// ============================================================================

/// Convert string to uppercase (ASCII only)
pub fn toUpper(allocator: std.mem.Allocator, input: []const u8) StringError![]u8 {
    const result = allocator.alloc(u8, input.len) catch return StringError.OutOfMemory;
    
    for (input, 0..) |c, i| {
        result[i] = if (c >= 'a' and c <= 'z') c - 32 else c;
    }
    
    return result;
}

/// Convert string to lowercase (ASCII only)
pub fn toLower(allocator: std.mem.Allocator, input: []const u8) StringError![]u8 {
    const result = allocator.alloc(u8, input.len) catch return StringError.OutOfMemory;
    
    for (input, 0..) |c, i| {
        result[i] = if (c >= 'A' and c <= 'Z') c + 32 else c;
    }
    
    return result;
}

/// Capitalize first character (ASCII only)
pub fn capitalize(allocator: std.mem.Allocator, input: []const u8) StringError![]u8 {
    if (input.len == 0) {
        return allocator.dupe(u8, "");
    }
    
    const result = allocator.alloc(u8, input.len) catch return StringError.OutOfMemory;
    
    result[0] = if (input[0] >= 'a' and input[0] <= 'z') input[0] - 32 else input[0];
    for (input[1..], 0..) |c, i| {
        result[i + 1] = c;
    }
    
    return result;
}

/// Title case - capitalize first letter of each word (ASCII only)
pub fn title(allocator: std.mem.Allocator, input: []const u8) StringError![]u8 {
    if (input.len == 0) {
        return allocator.dupe(u8, "");
    }
    
    const result = allocator.alloc(u8, input.len) catch return StringError.OutOfMemory;
    
    var capitalize_next = true;
    for (input, 0..) |c, i| {
        if (c == ' ') {
            result[i] = c;
            capitalize_next = true;
        } else if (capitalize_next) {
            result[i] = if (c >= 'a' and c <= 'z') c - 32 else c;
            capitalize_next = false;
        } else {
            result[i] = if (c >= 'A' and c <= 'Z') c + 32 else c;
        }
    }
    
    return result;
}

/// Swap case (ASCII only)
pub fn swapCase(allocator: std.mem.Allocator, input: []const u8) StringError![]u8 {
    const result = allocator.alloc(u8, input.len) catch return StringError.OutOfMemory;
    
    for (input, 0..) |c, i| {
        if (c >= 'a' and c <= 'z') {
            result[i] = c - 32;
        } else if (c >= 'A' and c <= 'Z') {
            result[i] = c + 32;
        } else {
            result[i] = c;
        }
    }
    
    return result;
}

// ============================================================================
// String Manipulation
// ============================================================================

/// Reverse a string
pub fn reverse(allocator: std.mem.Allocator, input: []const u8) StringError![]u8 {
    const result = allocator.alloc(u8, input.len) catch return StringError.OutOfMemory;
    
    for (input, 0..) |c, i| {
        result[input.len - 1 - i] = c;
    }
    
    return result;
}

/// Repeat a string n times
pub fn repeat(allocator: std.mem.Allocator, input: []const u8, n: usize) StringError![]u8 {
    if (n == 0) {
        return allocator.dupe(u8, "");
    }
    
    const total_len = input.len * n;
    const result = allocator.alloc(u8, total_len) catch return StringError.OutOfMemory;
    
    var offset: usize = 0;
    for (0..n) |_| {
        @memcpy(result[offset .. offset + input.len], input);
        offset += input.len;
    }
    
    return result;
}

/// Replace all occurrences of old with new
pub fn replace(allocator: std.mem.Allocator, input: []const u8, old: []const u8, new: []const u8) StringError![]u8 {
    if (old.len == 0) {
        return allocator.dupe(u8, input);
    }
    
    // Count occurrences
    var occurrence_count: usize = 0;
    var pos: usize = 0;
    while (pos <= input.len - old.len) {
        if (std.mem.eql(u8, input[pos .. pos + old.len], old)) {
            occurrence_count += 1;
            pos += old.len;
        } else {
            pos += 1;
        }
    }
    
    // Calculate new length
    const new_len = input.len + occurrence_count *| (new.len -| old.len);
    const result = allocator.alloc(u8, new_len) catch return StringError.OutOfMemory;
    
    // Build result
    var src_pos: usize = 0;
    var dst_pos: usize = 0;
    while (src_pos < input.len) {
        if (src_pos <= input.len - old.len and std.mem.eql(u8, input[src_pos .. src_pos + old.len], old)) {
            @memcpy(result[dst_pos .. dst_pos + new.len], new);
            dst_pos += new.len;
            src_pos += old.len;
        } else {
            result[dst_pos] = input[src_pos];
            dst_pos += 1;
            src_pos += 1;
        }
    }
    
    return result;
}

/// Replace first n occurrences
pub fn replaceN(allocator: std.mem.Allocator, input: []const u8, old: []const u8, new: []const u8, n: usize) StringError![]u8 {
    if (old.len == 0 or n == 0) {
        return allocator.dupe(u8, input);
    }
    
    // Count occurrences (up to n)
    var occurrence_count: usize = 0;
    var pos: usize = 0;
    while (occurrence_count < n and pos <= input.len - old.len) {
        if (std.mem.eql(u8, input[pos .. pos + old.len], old)) {
            occurrence_count += 1;
            pos += old.len;
        } else {
            pos += 1;
        }
    }
    
    // Calculate new length
    const new_len = input.len + occurrence_count * (new.len - old.len);
    const result = allocator.alloc(u8, new_len) catch return StringError.OutOfMemory;
    
    // Build result
    var src_pos: usize = 0;
    var dst_pos: usize = 0;
    var replaced: usize = 0;
    while (src_pos < input.len) {
        if (replaced < n and src_pos <= input.len - old.len and std.mem.eql(u8, input[src_pos .. src_pos + old.len], old)) {
            @memcpy(result[dst_pos .. dst_pos + new.len], new);
            dst_pos += new.len;
            src_pos += old.len;
            replaced += 1;
        } else {
            result[dst_pos] = input[src_pos];
            dst_pos += 1;
            src_pos += 1;
        }
    }
    
    return result;
}

// ============================================================================
// Split and Join
// ============================================================================

/// Split string by delimiter
pub fn split(allocator: std.mem.Allocator, input: []const u8, delimiter: []const u8) StringError![][]u8 {
    if (delimiter.len == 0) {
        // Return array of single characters
        const result = allocator.alloc([]u8, input.len) catch return StringError.OutOfMemory;
        for (input, 0..) |c, i| {
            result[i] = allocator.alloc(u8, 1) catch return StringError.OutOfMemory;
            result[i][0] = c;
        }
        return result;
    }
    
    // Count parts
    var part_count: usize = 1;
    var pos: usize = 0;
    while (pos <= input.len - delimiter.len) {
        if (std.mem.eql(u8, input[pos .. pos + delimiter.len], delimiter)) {
            part_count += 1;
            pos += delimiter.len;
        } else {
            pos += 1;
        }
    }
    
    // Allocate result
    const result = allocator.alloc([]u8, part_count) catch return StringError.OutOfMemory;
    
    // Split
    var part_idx: usize = 0;
    var start: usize = 0;
    pos = 0;
    
    while (pos <= input.len - delimiter.len) {
        if (std.mem.eql(u8, input[pos .. pos + delimiter.len], delimiter)) {
            result[part_idx] = allocator.dupe(u8, input[start..pos]) catch return StringError.OutOfMemory;
            part_idx += 1;
            start = pos + delimiter.len;
            pos += delimiter.len;
        } else {
            pos += 1;
        }
    }
    
    // Last part
    result[part_idx] = allocator.dupe(u8, input[start..]) catch return StringError.OutOfMemory;
    
    return result;
}

/// Split string by whitespace
pub fn splitWhitespace(allocator: std.mem.Allocator, input: []const u8) StringError![][]u8 {
    var word_count: usize = 0;
    var in_word = false;
    
    for (input) |c| {
        if (c == ' ' or c == '\t' or c == '\n' or c == '\r') {
            in_word = false;
        } else if (!in_word) {
            in_word = true;
            word_count += 1;
        }
    }
    
    const result = allocator.alloc([]u8, word_count) catch return StringError.OutOfMemory;
    
    var part_idx: usize = 0;
    var start: usize = 0;
    in_word = false;
    
    for (input, 0..) |c, i| {
        if (c == ' ' or c == '\t' or c == '\n' or c == '\r') {
            if (in_word) {
                result[part_idx] = allocator.dupe(u8, input[start..i]) catch return StringError.OutOfMemory;
                part_idx += 1;
                in_word = false;
            }
        } else if (!in_word) {
            start = i;
            in_word = true;
        }
    }
    
    if (in_word) {
        result[part_idx] = allocator.dupe(u8, input[start..]) catch return StringError.OutOfMemory;
    }
    
    return result;
}

/// Join strings with delimiter
pub fn join(allocator: std.mem.Allocator, parts: []const []const u8, delimiter: []const u8) StringError![]u8 {
    if (parts.len == 0) {
        return allocator.dupe(u8, "");
    }
    
    // Calculate total length
    var total_len: usize = 0;
    for (parts) |part| {
        total_len += part.len;
    }
    total_len += delimiter.len * (parts.len - 1);
    
    const result = allocator.alloc(u8, total_len) catch return StringError.OutOfMemory;
    
    var pos: usize = 0;
    for (parts, 0..) |part, i| {
        @memcpy(result[pos .. pos + part.len], part);
        pos += part.len;
        if (i < parts.len - 1) {
            @memcpy(result[pos .. pos + delimiter.len], delimiter);
            pos += delimiter.len;
        }
    }
    
    return result;
}

// ============================================================================
// Padding
// ============================================================================

/// Pad string on the left
pub fn padLeft(allocator: std.mem.Allocator, input: []const u8, pad_char: u8, total_len: usize) StringError![]u8 {
    if (input.len >= total_len) {
        return allocator.dupe(u8, input);
    }
    
    const pad_len = total_len - input.len;
    const result = allocator.alloc(u8, total_len) catch return StringError.OutOfMemory;
    
    @memset(result[0..pad_len], pad_char);
    @memcpy(result[pad_len..], input);
    
    return result;
}

/// Pad string on the right
pub fn padRight(allocator: std.mem.Allocator, input: []const u8, pad_char: u8, total_len: usize) StringError![]u8 {
    if (input.len >= total_len) {
        return allocator.dupe(u8, input);
    }
    
    const result = allocator.alloc(u8, total_len) catch return StringError.OutOfMemory;
    
    @memcpy(result[0..input.len], input);
    @memset(result[input.len..], pad_char);
    
    return result;
}

/// Center string with padding
pub fn center(allocator: std.mem.Allocator, input: []const u8, pad_char: u8, total_len: usize) StringError![]u8 {
    if (input.len >= total_len) {
        return allocator.dupe(u8, input);
    }
    
    const total_pad = total_len - input.len;
    const left_pad = total_pad / 2;
    
    const result = allocator.alloc(u8, total_len) catch return StringError.OutOfMemory;
    
    @memset(result[0..left_pad], pad_char);
    @memcpy(result[left_pad .. left_pad + input.len], input);
    @memset(result[left_pad + input.len ..], pad_char);
    
    return result;
}

// ============================================================================
// Prefix/Suffix
// ============================================================================

/// Check if string starts with prefix
pub fn startsWith(input: []const u8, prefix: []const u8) bool {
    if (prefix.len > input.len) return false;
    return std.mem.eql(u8, input[0..prefix.len], prefix);
}

/// Check if string ends with suffix
pub fn endsWith(input: []const u8, suffix: []const u8) bool {
    if (suffix.len > input.len) return false;
    return std.mem.eql(u8, input[input.len - suffix.len ..], suffix);
}

/// Remove prefix if present
pub fn removePrefix(allocator: std.mem.Allocator, input: []const u8, prefix: []const u8) StringError![]u8 {
    if (startsWith(input, prefix)) {
        return allocator.dupe(u8, input[prefix.len..]);
    }
    return allocator.dupe(u8, input);
}

/// Remove suffix if present
pub fn removeSuffix(allocator: std.mem.Allocator, input: []const u8, suffix: []const u8) StringError![]u8 {
    if (endsWith(input, suffix)) {
        return allocator.dupe(u8, input[0 .. input.len - suffix.len]);
    }
    return allocator.dupe(u8, input);
}

// ============================================================================
// Counting
// ============================================================================

/// Count occurrences of a substring
pub fn count(input: []const u8, sub: []const u8) usize {
    if (sub.len == 0) return 0;
    
    var result: usize = 0;
    var pos: usize = 0;
    
    while (pos <= input.len - sub.len) {
        if (std.mem.eql(u8, input[pos .. pos + sub.len], sub)) {
            result += 1;
            pos += sub.len;
        } else {
            pos += 1;
        }
    }
    
    return result;
}

/// Count occurrences of a character
pub fn countChar(input: []const u8, c: u8) usize {
    var result: usize = 0;
    for (input) |ch| {
        if (ch == c) result += 1;
    }
    return result;
}

// ============================================================================
// Character Classification
// ============================================================================

/// Check if string is all alphabetic (ASCII only)
pub fn isAlpha(input: []const u8) bool {
    if (input.len == 0) return false;
    for (input) |c| {
        if (!((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'))) return false;
    }
    return true;
}

/// Check if string is all digits (ASCII only)
pub fn isDigit(input: []const u8) bool {
    if (input.len == 0) return false;
    for (input) |c| {
        if (c < '0' or c > '9') return false;
    }
    return true;
}

/// Check if string is all alphanumeric (ASCII only)
pub fn isAlnum(input: []const u8) bool {
    if (input.len == 0) return false;
    for (input) |c| {
        if (!((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c >= '0' and c <= '9'))) return false;
    }
    return true;
}

/// Check if string is all whitespace
pub fn isWhitespace(input: []const u8) bool {
    if (input.len == 0) return false;
    for (input) |c| {
        if (c != ' ' and c != '\t' and c != '\n' and c != '\r') return false;
    }
    return true;
}

/// Check if string is all lowercase (ASCII only)
pub fn isLower(input: []const u8) bool {
    if (input.len == 0) return false;
    for (input) |c| {
        if (c >= 'A' and c <= 'Z') return false;
    }
    return true;
}

/// Check if string is all uppercase (ASCII only)
pub fn isUpper(input: []const u8) bool {
    if (input.len == 0) return false;
    for (input) |c| {
        if (c >= 'a' and c <= 'z') return false;
    }
    return true;
}

/// Check if string is empty or all whitespace
pub fn isBlank(input: []const u8) bool {
    for (input) |c| {
        if (c != ' ' and c != '\t' and c != '\n' and c != '\r') return false;
    }
    return true;
}

// ============================================================================
// Word Wrap
// ============================================================================

/// Word wrap at specified width
pub fn wordWrap(allocator: std.mem.Allocator, input: []const u8, width: usize) StringError![]u8 {
    if (width == 0) {
        return allocator.dupe(u8, input);
    }
    
    // Calculate result size (worst case: every char becomes newline)
    const result = allocator.alloc(u8, input.len * 2) catch return StringError.OutOfMemory;
    
    var src_pos: usize = 0;
    var dst_pos: usize = 0;
    var line_start: usize = 0;
    var last_space: ?usize = null;
    
    while (src_pos < input.len) {
        const c = input[src_pos];
        
        if (c == '\n') {
            result[dst_pos] = c;
            dst_pos += 1;
            src_pos += 1;
            line_start = dst_pos;
            last_space = null;
        } else if (c == ' ' or c == '\t') {
            last_space = dst_pos;
            result[dst_pos] = c;
            dst_pos += 1;
            src_pos += 1;
        } else {
            result[dst_pos] = c;
            dst_pos += 1;
            src_pos += 1;
            
            const line_len = dst_pos - line_start;
            if (line_len >= width) {
                if (last_space) |space_pos| {
                    // Insert newline at last space
                    result[space_pos] = '\n';
                    line_start = space_pos + 1;
                    last_space = null;
                }
            }
        }
    }
    
    return allocator.realloc(result, dst_pos) catch result[0..dst_pos];
}

// ============================================================================
// Helper Functions
// ============================================================================

/// Find first character not in set
fn findFirstNotOf(input: []const u8, chars: []const u8) ?usize {
    for (input, 0..) |c, i| {
        var found = false;
        for (chars) |ch| {
            if (c == ch) {
                found = true;
                break;
            }
        }
        if (!found) return i;
    }
    return null;
}

/// Find last character not in set
fn findLastNotOf(input: []const u8, chars: []const u8) ?usize {
    var i: usize = input.len;
    while (i > 0) {
        i -= 1;
        const c = input[i];
        var found = false;
        for (chars) |ch| {
            if (c == ch) {
                found = true;
                break;
            }
        }
        if (!found) return i;
    }
    return null;
}

/// Free a slice of strings
pub fn freeSlice(allocator: std.mem.Allocator, slice: [][]u8) void {
    for (slice) |s| {
        allocator.free(s);
    }
    allocator.free(slice);
}

// ============================================================================
// Tests
// ============================================================================

test "trim" {
    const allocator = std.testing.allocator;
    
    const result1 = try trim(allocator, "  hello  ");
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("hello", result1);
    
    const result2 = try trim(allocator, "\t\nhello\n\t");
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("hello", result2);
    
    const result3 = try trim(allocator, "hello");
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("hello", result3);
}

test "trimLeft and trimRight" {
    const allocator = std.testing.allocator;
    
    const left = try trimLeft(allocator, "  hello  ");
    defer allocator.free(left);
    try std.testing.expectEqualStrings("hello  ", left);
    
    const right = try trimRight(allocator, "  hello  ");
    defer allocator.free(right);
    try std.testing.expectEqualStrings("  hello", right);
}

test "toUpper and toLower" {
    const allocator = std.testing.allocator;
    
    const upper = try toUpper(allocator, "hello WORLD 123");
    defer allocator.free(upper);
    try std.testing.expectEqualStrings("HELLO WORLD 123", upper);
    
    const lower = try toLower(allocator, "hello WORLD 123");
    defer allocator.free(lower);
    try std.testing.expectEqualStrings("hello world 123", lower);
}

test "capitalize" {
    const allocator = std.testing.allocator;
    
    const result1 = try capitalize(allocator, "hello");
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("Hello", result1);
    
    const result2 = try capitalize(allocator, "HELLO");
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("HELLO", result2);
    
    const result3 = try capitalize(allocator, "");
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("", result3);
}

test "title" {
    const allocator = std.testing.allocator;
    
    const result = try title(allocator, "hello world");
    defer allocator.free(result);
    try std.testing.expectEqualStrings("Hello World", result);
}

test "swapCase" {
    const allocator = std.testing.allocator;
    
    const result = try swapCase(allocator, "Hello World");
    defer allocator.free(result);
    try std.testing.expectEqualStrings("hELLO wORLD", result);
}

test "reverse" {
    const allocator = std.testing.allocator;
    
    const result = try reverse(allocator, "hello");
    defer allocator.free(result);
    try std.testing.expectEqualStrings("olleh", result);
}

test "repeat" {
    const allocator = std.testing.allocator;
    
    const result = try repeat(allocator, "ab", 3);
    defer allocator.free(result);
    try std.testing.expectEqualStrings("ababab", result);
    
    const result2 = try repeat(allocator, "x", 0);
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("", result2);
}

test "replace" {
    const allocator = std.testing.allocator;
    
    const result1 = try replace(allocator, "hello world world", "world", "there");
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("hello there there", result1);
    
    const result2 = try replace(allocator, "hello", "x", "y");
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("hello", result2);
}

test "replaceN" {
    const allocator = std.testing.allocator;
    
    const result = try replaceN(allocator, "a b a b a", "a", "X", 2);
    defer allocator.free(result);
    try std.testing.expectEqualStrings("X b X b a", result);
}

test "split" {
    const allocator = std.testing.allocator;
    
    const parts = try split(allocator, "a,b,c", ",");
    defer freeSlice(allocator, parts);
    
    try std.testing.expectEqual(@as(usize, 3), parts.len);
    try std.testing.expectEqualStrings("a", parts[0]);
    try std.testing.expectEqualStrings("b", parts[1]);
    try std.testing.expectEqualStrings("c", parts[2]);
}

test "splitWhitespace" {
    const allocator = std.testing.allocator;
    
    const parts = try splitWhitespace(allocator, "  hello   world  ");
    defer freeSlice(allocator, parts);
    
    try std.testing.expectEqual(@as(usize, 2), parts.len);
    try std.testing.expectEqualStrings("hello", parts[0]);
    try std.testing.expectEqualStrings("world", parts[1]);
}

test "join" {
    const allocator = std.testing.allocator;
    
    const parts = [_][]const u8{ "a", "b", "c" };
    const result = try join(allocator, &parts, ",");
    defer allocator.free(result);
    
    try std.testing.expectEqualStrings("a,b,c", result);
}

test "padLeft" {
    const allocator = std.testing.allocator;
    
    const result = try padLeft(allocator, "42", '0', 5);
    defer allocator.free(result);
    try std.testing.expectEqualStrings("00042", result);
}

test "padRight" {
    const allocator = std.testing.allocator;
    
    const result = try padRight(allocator, "42", '-', 5);
    defer allocator.free(result);
    try std.testing.expectEqualStrings("42---", result);
}

test "center" {
    const allocator = std.testing.allocator;
    
    const result = try center(allocator, "hi", '-', 6);
    defer allocator.free(result);
    try std.testing.expectEqualStrings("--hi--", result);
}

test "startsWith and endsWith" {
    try std.testing.expect(startsWith("hello world", "hello"));
    try std.testing.expect(!startsWith("hello world", "world"));
    try std.testing.expect(endsWith("hello world", "world"));
    try std.testing.expect(!endsWith("hello world", "hello"));
}

test "removePrefix and removeSuffix" {
    const allocator = std.testing.allocator;
    
    const result1 = try removePrefix(allocator, "hello world", "hello ");
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("world", result1);
    
    const result2 = try removeSuffix(allocator, "hello world", " world");
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("hello", result2);
    
    const result3 = try removePrefix(allocator, "hello", "x");
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("hello", result3);
}

test "count" {
    try std.testing.expectEqual(@as(usize, 2), count("hello hello", "hello"));
    try std.testing.expectEqual(@as(usize, 2), countChar("hello", 'l'));
    try std.testing.expectEqual(@as(usize, 0), count("hello", "x"));
}

test "isAlpha" {
    try std.testing.expect(isAlpha("hello"));
    try std.testing.expect(isAlpha("HELLO"));
    try std.testing.expect(isAlpha("HelloWorld"));
    try std.testing.expect(!isAlpha("hello123"));
    try std.testing.expect(!isAlpha("hello world"));
    try std.testing.expect(!isAlpha(""));
}

test "isDigit" {
    try std.testing.expect(isDigit("12345"));
    try std.testing.expect(!isDigit("123a5"));
    try std.testing.expect(!isDigit(""));
}

test "isAlnum" {
    try std.testing.expect(isAlnum("hello123"));
    try std.testing.expect(!isAlnum("hello 123"));
    try std.testing.expect(!isAlnum(""));
}

test "isWhitespace" {
    try std.testing.expect(isWhitespace("   "));
    try std.testing.expect(isWhitespace("\t\n\r"));
    try std.testing.expect(!isWhitespace("  x  "));
    try std.testing.expect(!isWhitespace(""));
}

test "isLower and isUpper" {
    try std.testing.expect(isLower("hello"));
    try std.testing.expect(!isLower("Hello"));
    try std.testing.expect(isUpper("HELLO"));
    try std.testing.expect(!isUpper("Hello"));
}

test "isBlank" {
    try std.testing.expect(isBlank(""));
    try std.testing.expect(isBlank("   "));
    try std.testing.expect(isBlank("\t\n"));
    try std.testing.expect(!isBlank("  x  "));
}

test "wordWrap" {
    const allocator = std.testing.allocator;
    
    const result = try wordWrap(allocator, "hello world this is a test", 10);
    defer allocator.free(result);
    // Should wrap at "hello world" -> "hello\nworld this is a test" -> etc.
    try std.testing.expect(result.len > 0);
}

test "trimChars" {
    const allocator = std.testing.allocator;
    
    const result = try trimChars(allocator, "xxhelloxx", "x");
    defer allocator.free(result);
    try std.testing.expectEqualStrings("hello", result);
}

test "freeSlice" {
    const allocator = std.testing.allocator;
    
    const parts = try split(allocator, "a,b,c", ",");
    freeSlice(allocator, parts);
    // No memory leak should occur
}