const std = @import("std");

/// ISBN validation errors
pub const IsbnError = error{
    InvalidLength,
    InvalidCharacter,
    InvalidChecksum,
    EmptyInput,
    OutOfMemory,
};

/// ISBN type enumeration
pub const IsbnType = enum {
    isbn10,
    isbn13,
    unknown,
};

/// ISBN structure
pub const Isbn = struct {
    type: IsbnType,
    digits: []const u8,
    check_digit: u8,
    allocator: ?std.mem.Allocator = null,

    const Self = @This();

    /// Parse and validate an ISBN string
    pub fn parse(allocator: std.mem.Allocator, input: []const u8) IsbnError!Self {
        if (input.len == 0) return IsbnError.EmptyInput;

        // Remove hyphens and spaces
        var clean = std.ArrayList(u8).init(allocator);
        defer clean.deinit();

        for (input) |c| {
            if (c >= '0' and c <= '9') {
                clean.append(c) catch return IsbnError.OutOfMemory;
            } else if (c == 'X' or c == 'x') {
                clean.append('X') catch return IsbnError.OutOfMemory;
            }
            // Skip hyphens and spaces
        }

        const digits = clean.items;

        if (digits.len == 10) {
            return parseIsbn10(allocator, digits);
        } else if (digits.len == 13) {
            return parseIsbn13(allocator, digits);
        }

        return IsbnError.InvalidLength;
    }

    /// Parse without allocator (returns static reference)
    pub fn parseStatic(input: []const u8) IsbnError!Self {
        if (input.len == 0) return IsbnError.EmptyInput;

        // Extract digits
        var digits_arr: [13]u8 = undefined;
        var digit_count: usize = 0;
        var has_x_at_end: bool = false;

        for (input) |c| {
            if (c >= '0' and c <= '9') {
                if (digit_count < 13) {
                    digits_arr[digit_count] = c;
                    digit_count += 1;
                }
            } else if (c == 'X' or c == 'x') {
                if (digit_count < 13) {
                    digits_arr[digit_count] = 'X';
                    digit_count += 1;
                    has_x_at_end = true;
                }
            }
        }

        if (digit_count == 10) {
            // Validate ISBN-10: X can only be at the end
            if (has_x_at_end and digit_count == 10) {
                // X is valid as check digit
            }
            
            // Validate characters (first 9 must be digits)
            for (digits_arr[0..9]) |c| {
                if (c < '0' or c > '9') return IsbnError.InvalidCharacter;
            }
            
            // Last can be X
            const last = digits_arr[9];
            if ((last < '0' or last > '9') and last != 'X') {
                return IsbnError.InvalidCharacter;
            }

            // Calculate and verify checksum
            var sum: usize = 0;
            for (digits_arr[0..9], 0..) |c, i| {
                sum += @as(usize, @intCast(c - '0')) * (10 - i);
            }
            const check_value: usize = if (last == 'X') 10 else @as(usize, @intCast(last - '0'));
            sum += check_value;

            if (sum % 11 != 0) return IsbnError.InvalidChecksum;

            return Self{
                .type = .isbn10,
                .digits = input,
                .check_digit = last,
            };
        } else if (digit_count == 13) {
            // Validate ISBN-13: all must be digits (no X allowed)
            if (has_x_at_end) return IsbnError.InvalidCharacter;
            
            for (digits_arr[0..13]) |c| {
                if (c < '0' or c > '9') return IsbnError.InvalidCharacter;
            }

            // Calculate and verify checksum
            var sum: usize = 0;
            for (digits_arr[0..12], 0..) |c, i| {
                const digit = @as(usize, @intCast(c - '0'));
                sum += digit * (if (i % 2 == 0) @as(usize, 1) else @as(usize, 3));
            }
            const expected_check = (10 - (sum % 10)) % 10;
            const actual_check = @as(usize, @intCast(digits_arr[12] - '0'));

            if (expected_check != actual_check) return IsbnError.InvalidChecksum;

            return Self{
                .type = .isbn13,
                .digits = input,
                .check_digit = digits_arr[12],
            };
        }

        return IsbnError.InvalidLength;
    }

    fn parseIsbn10(allocator: std.mem.Allocator, digits: []const u8) IsbnError!Self {
        // Validate characters (first 9 must be digits, last can be X)
        for (digits[0..9]) |c| {
            if (c < '0' or c > '9') return IsbnError.InvalidCharacter;
        }
        const last = digits[9];
        if ((last < '0' or last > '9') and last != 'X') {
            return IsbnError.InvalidCharacter;
        }

        // Calculate checksum
        var sum: usize = 0;
        for (digits[0..9], 0..) |c, i| {
            sum += @as(usize, @intCast(c - '0')) * (10 - i);
        }
        const check_value: usize = if (last == 'X') 10 else @as(usize, @intCast(last - '0'));
        sum += check_value;

        if (sum % 11 != 0) return IsbnError.InvalidChecksum;

        const owned_digits = allocator.dupe(u8, digits) catch return IsbnError.OutOfMemory;
        return Self{
            .type = .isbn10,
            .digits = owned_digits,
            .check_digit = last,
            .allocator = allocator,
        };
    }

    fn parseIsbn13(allocator: std.mem.Allocator, digits: []const u8) IsbnError!Self {
        // Validate all characters must be digits
        for (digits) |c| {
            if (c < '0' or c > '9') return IsbnError.InvalidCharacter;
        }

        // Calculate checksum
        var sum: usize = 0;
        for (digits[0..12], 0..) |c, i| {
            const digit = @as(usize, @intCast(c - '0'));
            sum += digit * (if (i % 2 == 0) @as(usize, 1) else @as(usize, 3));
        }
        const expected_check = (10 - (sum % 10)) % 10;
        const actual_check = @as(usize, @intCast(digits[12] - '0'));

        if (expected_check != actual_check) return IsbnError.InvalidChecksum;

        const owned_digits = allocator.dupe(u8, digits) catch return IsbnError.OutOfMemory;
        return Self{
            .type = .isbn13,
            .digits = owned_digits,
            .check_digit = digits[12],
            .allocator = allocator,
        };
    }

    /// Free allocated memory
    pub fn deinit(self: Self) void {
        if (self.allocator) |alloc| {
            alloc.free(self.digits);
        }
    }

    /// Get clean digits (no hyphens/spaces)
    pub fn getCleanDigits(self: Self, allocator: std.mem.Allocator) IsbnError![]u8 {
        var result = std.ArrayList(u8).init(allocator);
        errdefer result.deinit();

        for (self.digits) |c| {
            if (c >= '0' and c <= '9') {
                result.append(c) catch return IsbnError.OutOfMemory;
            } else if (c == 'X') {
                result.append(c) catch return IsbnError.OutOfMemory;
            }
        }

        return result.toOwnedSlice() catch return IsbnError.OutOfMemory;
    }

    /// Format ISBN with hyphens
    pub fn formatHyphens(self: Self, allocator: std.mem.Allocator) IsbnError![]u8 {
        var result = std.ArrayList(u8).init(allocator);
        errdefer result.deinit();

        // Get clean digits
        var clean: [13]u8 = undefined;
        var idx: usize = 0;
        for (self.digits) |c| {
            if ((c >= '0' and c <= '9') or c == 'X') {
                if (idx < 13) {
                    clean[idx] = c;
                    idx += 1;
                }
            }
        }

        switch (self.type) {
            .isbn10 => {
                // ISBN-10 format: X-XXXX-XX-X (group-publisher-title-check)
                if (idx == 10) {
                    result.append(clean[0]) catch return IsbnError.OutOfMemory;
                    result.append('-') catch return IsbnError.OutOfMemory;
                    for (clean[1..5]) |c| result.append(c) catch return IsbnError.OutOfMemory;
                    result.append('-') catch return IsbnError.OutOfMemory;
                    for (clean[5..7]) |c| result.append(c) catch return IsbnError.OutOfMemory;
                    result.append('-') catch return IsbnError.OutOfMemory;
                    for (clean[7..10]) |c| result.append(c) catch return IsbnError.OutOfMemory;
                }
            },
            .isbn13 => {
                // ISBN-13 format: XXX-X-XXXX-XXX-X (prefix-group-publisher-title-check)
                if (idx == 13) {
                    for (clean[0..3]) |c| result.append(c) catch return IsbnError.OutOfMemory;
                    result.append('-') catch return IsbnError.OutOfMemory;
                    result.append(clean[3]) catch return IsbnError.OutOfMemory;
                    result.append('-') catch return IsbnError.OutOfMemory;
                    for (clean[4..9]) |c| result.append(c) catch return IsbnError.OutOfMemory;
                    result.append('-') catch return IsbnError.OutOfMemory;
                    for (clean[9..12]) |c| result.append(c) catch return IsbnError.OutOfMemory;
                    result.append('-') catch return IsbnError.OutOfMemory;
                    result.append(clean[12]) catch return IsbnError.OutOfMemory;
                }
            },
            .unknown => {},
        }

        return result.toOwnedSlice() catch return IsbnError.OutOfMemory;
    }

    /// Convert ISBN-10 to ISBN-13
    pub fn toIsbn13(self: Self, allocator: std.mem.Allocator) IsbnError!Self {
        if (self.type == .isbn13) {
            const clean = try self.getCleanDigits(allocator);
            return Self{
                .type = .isbn13,
                .digits = clean,
                .check_digit = self.check_digit,
                .allocator = allocator,
            };
        }

        if (self.type != .isbn10) {
            return IsbnError.InvalidChecksum;
        }

        // Extract clean digits from ISBN-10
        var clean: [10]u8 = undefined;
        var idx: usize = 0;
        for (self.digits) |c| {
            if (c >= '0' and c <= '9') {
                if (idx < 10) {
                    clean[idx] = c;
                    idx += 1;
                }
            } else if (c == 'X') {
                if (idx < 10) {
                    clean[idx] = 'X';
                    idx += 1;
                }
            }
        }
        if (idx != 10) return IsbnError.InvalidLength;

        var isbn13_digits: [13]u8 = undefined;
        // Add prefix 978
        isbn13_digits[0] = '9';
        isbn13_digits[1] = '7';
        isbn13_digits[2] = '8';

        // Copy first 9 digits from ISBN-10 (skip X check digit if present)
        for (clean[0..9], 0..) |c, i| {
            isbn13_digits[3 + i] = c;
        }

        // Calculate new checksum
        var sum: usize = 0;
        for (isbn13_digits[0..12], 0..) |c, i| {
            const digit = @as(usize, @intCast(c - '0'));
            sum += digit * (if (i % 2 == 0) @as(usize, 1) else @as(usize, 3));
        }
        const check = @as(u8, @intCast((10 - (sum % 10)) % 10 + '0'));
        isbn13_digits[12] = check;

        const owned = allocator.dupe(u8, &isbn13_digits) catch return IsbnError.OutOfMemory;
        return Self{
            .type = .isbn13,
            .digits = owned,
            .check_digit = check,
            .allocator = allocator,
        };
    }

    /// Convert ISBN-13 to ISBN-10 (only works for 978 prefix)
    pub fn toIsbn10(self: Self, allocator: std.mem.Allocator) IsbnError!Self {
        if (self.type == .isbn10) {
            const clean = try self.getCleanDigits(allocator);
            return Self{
                .type = .isbn10,
                .digits = clean,
                .check_digit = self.check_digit,
                .allocator = allocator,
            };
        }

        if (self.type != .isbn13) {
            return IsbnError.InvalidChecksum;
        }

        // Extract clean digits from ISBN-13
        var clean: [13]u8 = undefined;
        var idx: usize = 0;
        for (self.digits) |c| {
            if (c >= '0' and c <= '9') {
                if (idx < 13) {
                    clean[idx] = c;
                    idx += 1;
                }
            }
        }
        if (idx != 13) return IsbnError.InvalidLength;

        // Only 978-prefix ISBN-13s can be converted to ISBN-10
        if (!std.mem.eql(u8, clean[0..3], "978")) {
            return IsbnError.InvalidChecksum;
        }

        var isbn10_digits: [10]u8 = undefined;
        // Copy digits 3-12 from ISBN-13
        for (clean[3..12], 0..) |c, i| {
            isbn10_digits[i] = c;
        }

        // Calculate ISBN-10 checksum
        var sum: usize = 0;
        for (isbn10_digits[0..9], 0..) |c, i| {
            sum += @as(usize, @intCast(c - '0')) * (10 - i);
        }
        const check_value = (11 - (sum % 11)) % 11;
        isbn10_digits[9] = if (check_value == 10) 'X' else @as(u8, @intCast(check_value + '0'));

        const owned = allocator.dupe(u8, &isbn10_digits) catch return IsbnError.OutOfMemory;
        return Self{
            .type = .isbn10,
            .digits = owned,
            .check_digit = isbn10_digits[9],
            .allocator = allocator,
        };
    }

    /// Check if ISBN is valid
    pub fn isValid(self: Self) bool {
        return self.type != .unknown;
    }
};

/// Quick validation function
pub fn isValidIsbn(input: []const u8) bool {
    return (Isbn.parseStatic(input) catch return false).isValid();
}

/// Detect ISBN type
pub fn detectIsbnType(input: []const u8) IsbnType {
    return (Isbn.parseStatic(input) catch return .unknown).type;
}

/// Calculate expected checksum for ISBN-10 from 9-digit base
pub fn calculateIsbn10CheckDigit(base: []const u8) IsbnError!u8 {
    var digits: [9]u8 = undefined;
    var idx: usize = 0;

    for (base) |c| {
        if (c >= '0' and c <= '9') {
            if (idx >= 9) return IsbnError.InvalidLength;
            digits[idx] = c;
            idx += 1;
        }
    }

    if (idx != 9) return IsbnError.InvalidLength;

    var sum: usize = 0;
    for (digits[0..9], 0..) |c, i| {
        sum += @as(usize, @intCast(c - '0')) * (10 - i);
    }

    const check = (11 - (sum % 11)) % 11;
    return if (check == 10) 'X' else @as(u8, @intCast(check + '0'));
}

/// Calculate expected checksum for ISBN-13 from 12-digit base
pub fn calculateIsbn13CheckDigit(base: []const u8) IsbnError!u8 {
    var digits: [12]u8 = undefined;
    var idx: usize = 0;

    for (base) |c| {
        if (c >= '0' and c <= '9') {
            if (idx >= 12) return IsbnError.InvalidLength;
            digits[idx] = c;
            idx += 1;
        }
    }

    if (idx != 12) return IsbnError.InvalidLength;

    var sum: usize = 0;
    for (digits[0..12], 0..) |c, i| {
        const digit = @as(usize, @intCast(c - '0'));
        sum += digit * (if (i % 2 == 0) @as(usize, 1) else @as(usize, 3));
    }

    const check = (10 - (sum % 10)) % 10;
    return @as(u8, @intCast(check + '0'));
}

// ==================== Tests ====================

test "ISBN-10 validation - valid" {
    const isbn_result = try Isbn.parseStatic("0-306-40615-2");
    try std.testing.expect(isbn_result.type == .isbn10);
    try std.testing.expect(isbn_result.isValid());
}

test "ISBN-10 validation - valid with X" {
    const isbn_result = try Isbn.parseStatic("0-8044-2957-X");
    try std.testing.expect(isbn_result.type == .isbn10);
    try std.testing.expect(isbn_result.isValid());
}

test "ISBN-10 validation - invalid checksum" {
    const result = Isbn.parseStatic("0-306-40615-3");
    try std.testing.expectError(IsbnError.InvalidChecksum, result);
}

test "ISBN-13 validation - valid" {
    const isbn_result = try Isbn.parseStatic("978-0-306-40615-7");
    try std.testing.expect(isbn_result.type == .isbn13);
    try std.testing.expect(isbn_result.isValid());
}

test "ISBN-13 validation - invalid checksum" {
    const result = Isbn.parseStatic("978-0-306-40615-8");
    try std.testing.expectError(IsbnError.InvalidChecksum, result);
}

test "isValidIsbn function" {
    try std.testing.expect(isValidIsbn("0-306-40615-2"));
    try std.testing.expect(isValidIsbn("978-0-306-40615-7"));
    try std.testing.expect(!isValidIsbn("0-306-40615-3"));
    try std.testing.expect(!isValidIsbn("invalid"));
}

test "detectIsbnType function" {
    try std.testing.expectEqual(IsbnType.isbn10, detectIsbnType("0-306-40615-2"));
    try std.testing.expectEqual(IsbnType.isbn13, detectIsbnType("978-0-306-40615-7"));
    try std.testing.expectEqual(IsbnType.unknown, detectIsbnType("invalid"));
}

test "calculateIsbn10CheckDigit" {
    const check = try calculateIsbn10CheckDigit("030640615");
    try std.testing.expectEqual(@as(u8, '2'), check);
}

test "calculateIsbn13CheckDigit" {
    const check = try calculateIsbn13CheckDigit("978030640615");
    try std.testing.expectEqual(@as(u8, '7'), check);
}

test "ISBN-10 with X check digit" {
    const check = try calculateIsbn10CheckDigit("080442957");
    try std.testing.expectEqual(@as(u8, 'X'), check);
}

test "ISBN parsing with various formats" {
    // Without hyphens
    const isbn1 = try Isbn.parseStatic("0306406152");
    try std.testing.expect(isbn1.type == .isbn10);

    // With spaces
    const isbn2 = try Isbn.parseStatic("0 306 40615 2");
    try std.testing.expect(isbn2.type == .isbn10);

    // Mixed
    const isbn3 = try Isbn.parseStatic("978 0-306-40615-7");
    try std.testing.expect(isbn3.type == .isbn13);
}

test "ISBN-10 to ISBN-13 conversion" {
    const allocator = std.testing.allocator;
    const isbn10 = try Isbn.parse(allocator, "0-306-40615-2");
    defer isbn10.deinit();

    const isbn13 = try isbn10.toIsbn13(allocator);
    defer isbn13.deinit();

    try std.testing.expect(isbn13.type == .isbn13);
    const clean = try isbn13.getCleanDigits(allocator);
    defer allocator.free(clean);
    try std.testing.expect(std.mem.eql(u8, clean, "9780306406157"));
}

test "ISBN-13 to ISBN-10 conversion" {
    const allocator = std.testing.allocator;
    const isbn13 = try Isbn.parse(allocator, "978-0-306-40615-7");
    defer isbn13.deinit();

    const isbn10 = try isbn13.toIsbn10(allocator);
    defer isbn10.deinit();

    try std.testing.expect(isbn10.type == .isbn10);
    const clean = try isbn10.getCleanDigits(allocator);
    defer allocator.free(clean);
    try std.testing.expect(std.mem.eql(u8, clean, "0306406152"));
}

test "Format ISBN with hyphens" {
    const allocator = std.testing.allocator;
    const isbn10 = try Isbn.parse(allocator, "0306406152");
    defer isbn10.deinit();

    const formatted = try isbn10.formatHyphens(allocator);
    defer allocator.free(formatted);

    try std.testing.expect(std.mem.containsAtLeast(u8, formatted, 1, "-"));
}

test "Empty input error" {
    const result = Isbn.parseStatic("");
    try std.testing.expectError(IsbnError.EmptyInput, result);
}

test "Invalid length error" {
    const result = Isbn.parseStatic("12345");
    try std.testing.expectError(IsbnError.InvalidLength, result);
}