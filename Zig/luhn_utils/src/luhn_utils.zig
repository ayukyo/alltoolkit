const std = @import("std");

/// Luhn algorithm errors
pub const LuhnError = error{
    OutOfMemory,
    InvalidCharacter,
    EmptyInput,
    InvalidLength,
    CheckDigitMismatch,
};

/// Card type enumeration
pub const CardType = enum {
    visa,
    mastercard,
    amex,
    discover,
    diners_club,
    jcb,
    unionpay,
    maestro,
    mir,
    unknown,

    /// Get human-readable card name
    pub fn name(self: CardType) []const u8 {
        return switch (self) {
            .visa => "Visa",
            .mastercard => "Mastercard",
            .amex => "American Express",
            .discover => "Discover",
            .diners_club => "Diners Club",
            .jcb => "JCB",
            .unionpay => "UnionPay",
            .maestro => "Maestro",
            .mir => "Mir",
            .unknown => "Unknown",
        };
    }

    /// Check if card type is valid (not unknown)
    pub fn isValid(self: CardType) bool {
        return self != .unknown;
    }
};

/// Luhn validation result
pub const ValidationResult = struct {
    is_valid: bool,
    card_type: CardType,
    check_digit: u8,
    computed_check_digit: u8,
    formatted_number: []const u8,

    pub fn deinit(self: *ValidationResult, allocator: std.mem.Allocator) void {
        allocator.free(self.formatted_number);
    }
};

/// Password strength levels (for general password strength checking)
pub const StrengthLevel = enum {
    very_weak,
    weak,
    fair,
    good,
    strong,
    very_strong,

    pub fn score(self: StrengthLevel) u8 {
        return switch (self) {
            .very_weak => 0,
            .weak => 1,
            .fair => 2,
            .good => 3,
            .strong => 4,
            .very_strong => 5,
        };
    }

    pub fn fromScore(value: u8) StrengthLevel {
        return switch (value) {
            0 => .very_weak,
            1 => .weak,
            2 => .fair,
            3 => .good,
            4 => .strong,
            else => .very_strong,
        };
    }
};

// ============================================================================
// Core Luhn Algorithm Functions
// ============================================================================

/// Calculate the Luhn check digit for a number string (without the check digit)
/// Returns the check digit that would make the number valid
pub fn calculateCheckDigit(number: []const u8) LuhnError!u8 {
    if (number.len == 0) {
        return LuhnError.EmptyInput;
    }

    var sum: u32 = 0;
    var is_even = true; // Will be false for the rightmost digit after we process

    // Process from right to left
    var i: usize = number.len;
    while (i > 0) {
        i -= 1;
        const c = number[i];

        if (c < '0' or c > '9') {
            return LuhnError.InvalidCharacter;
        }

        var digit: u32 = @as(u32, c - '0');

        if (is_even) {
            digit *= 2;
            if (digit > 9) {
                digit -= 9;
            }
        }

        sum += digit;
        is_even = !is_even;
    }

    // The check digit is (10 - (sum mod 10)) mod 10
    const check_digit: u8 = @as(u8, @intCast((10 - (sum % 10)) % 10));
    return check_digit;
}

/// Validate a number using the Luhn algorithm
/// Returns true if the number passes the Luhn check
pub fn validate(number: []const u8) LuhnError!bool {
    if (number.len == 0) {
        return LuhnError.EmptyInput;
    }

    var sum: u32 = 0;
    var is_even = false;

    // Process from right to left
    var i: usize = number.len;
    while (i > 0) {
        i -= 1;
        const c = number[i];

        if (c < '0' or c > '9') {
            return LuhnError.InvalidCharacter;
        }

        var digit: u32 = @as(u32, c - '0');

        if (is_even) {
            digit *= 2;
            if (digit > 9) {
                digit -= 9;
            }
        }

        sum += digit;
        is_even = !is_even;
    }

    return sum % 10 == 0;
}

/// Validate with detailed result
pub fn validateWithDetails(allocator: std.mem.Allocator, number: []const u8) LuhnError!ValidationResult {
    if (number.len == 0) {
        return LuhnError.EmptyInput;
    }

    // Check for invalid characters
    for (number) |c| {
        if (c < '0' or c > '9') {
            return LuhnError.InvalidCharacter;
        }
    }

    const is_valid = try validate(number);
    const card_type = detectCardType(number);

    // Extract check digit (last digit)
    const check_digit: u8 = number[number.len - 1] - '0';

    // Calculate what check digit should be
    const number_without_check = number[0 .. number.len - 1];
    const computed_check_digit = try calculateCheckDigit(number_without_check);

    // Format the number
    var formatted = std.ArrayList(u8).init(allocator);
    errdefer formatted.deinit();

    const format_config = getCardFormatConfig(card_type);
    var pos: usize = 0;
    var group_idx: usize = 0;

    for (number, 0..) |c, i| {
        if (group_idx < format_config.group_sizes.len) {
            if (pos == format_config.group_sizes[group_idx] and i > 0) {
                try formatted.append(' ');
                pos = 0;
                group_idx += 1;
            }
        }
        try formatted.append(c);
        pos += 1;
    }

    return ValidationResult{
        .is_valid = is_valid,
        .card_type = card_type,
        .check_digit = check_digit,
        .computed_check_digit = computed_check_digit,
        .formatted_number = try formatted.toOwnedSlice(),
    };
}

// ============================================================================
// Card Type Detection
// ============================================================================

const CardFormatConfig = struct {
    group_sizes: []const usize,
    expected_lengths: []const usize,
};

fn getCardFormatConfig(card_type: CardType) CardFormatConfig {
    return switch (card_type) {
        .visa => .{ .group_sizes = &.{ 4, 4, 4, 4 }, .expected_lengths = &.{ 13, 16, 19 } },
        .mastercard => .{ .group_sizes = &.{ 4, 4, 4, 4 }, .expected_lengths = &.{ 16 } },
        .amex => .{ .group_sizes = &.{ 4, 6, 5 }, .expected_lengths = &.{ 15 } },
        .discover => .{ .group_sizes = &.{ 4, 4, 4, 4 }, .expected_lengths = &.{ 16, 19 } },
        .diners_club => .{ .group_sizes = &.{ 4, 6, 4 }, .expected_lengths = &.{ 14, 16, 19 } },
        .jcb => .{ .group_sizes = &.{ 4, 4, 4, 4 }, .expected_lengths = &.{ 16, 19 } },
        .unionpay => .{ .group_sizes = &.{ 4, 4, 4, 4 }, .expected_lengths = &.{ 16, 19 } },
        .maestro => .{ .group_sizes = &.{ 4, 4, 4, 4 }, .expected_lengths = &.{ 12, 13, 14, 15, 16, 17, 18, 19 } },
        .mir => .{ .group_sizes = &.{ 4, 4, 4, 4 }, .expected_lengths = &.{ 16 } },
        .unknown => .{ .group_sizes = &.{ 4, 4, 4, 4 }, .expected_lengths = &.{} },
    };
}

/// Detect card type from card number
pub fn detectCardType(number: []const u8) CardType {
    if (number.len < 2) return .unknown;

    // Get first digits for pattern matching
    const first_digit = number[0];
    const first_two = if (number.len >= 2) @as(u32, @as(u32, number[0] - '0') * 10 + @as(u32, number[1] - '0')) else 0;
    const first_three = if (number.len >= 3) @as(u32, @as(u32, number[0] - '0') * 100 + @as(u32, number[1] - '0') * 10 + @as(u32, number[2] - '0')) else 0;
    const first_four = if (number.len >= 4) @as(u32, @as(u32, number[0] - '0') * 1000 + @as(u32, number[1] - '0') * 100 + @as(u32, number[2] - '0') * 10 + @as(u32, number[3] - '0')) else 0;
    const first_six = if (number.len >= 6) @as(u32, @as(u32, number[0] - '0') * 100000 + @as(u32, number[1] - '0') * 10000 + @as(u32, number[2] - '0') * 1000 + @as(u32, number[3] - '0') * 100 + @as(u32, number[4] - '0') * 10 + @as(u32, number[5] - '0')) else 0;

    // Visa: starts with 4
    if (first_digit == '4') {
        if (number.len >= 13 and number.len <= 19) {
            return .visa;
        }
    }

    // Mastercard: 51-55 or 2221-2720
    if (first_two >= 51 and first_two <= 55) {
        return .mastercard;
    }
    if (first_four >= 2221 and first_four <= 2720) {
        return .mastercard;
    }

    // American Express: 34 or 37
    if (first_two == 34 or first_two == 37) {
        if (number.len == 15) {
            return .amex;
        }
    }

    // Discover: 6011, 644-649, 65, or 622126-622925
    if (first_four == 6011) return .discover;
    if (first_two == 65) return .discover;
    if (first_three >= 644 and first_three <= 649) return .discover;
    if (first_six >= 622126 and first_six <= 622925) return .discover;

    // Diners Club: 300-305, 36, 38, 39
    if (first_three >= 300 and first_three <= 305) return .diners_club;
    if (first_two == 36 or first_two == 38 or first_two == 39) return .diners_club;

    // JCB: 3528-3589
    if (first_four >= 3528 and first_four <= 3589) return .jcb;

    // UnionPay: 62
    if (first_two == 62) return .unionpay;

    // Maestro: 50, 56-69
    if (first_two == 50) return .maestro;
    if (first_two >= 56 and first_two <= 69) return .maestro;

    // Mir: 2200-2204
    if (first_four >= 2200 and first_four <= 2204) return .mir;

    return .unknown;
}

/// Check if number has valid length for its card type
pub fn hasValidLength(number: []const u8) bool {
    const card_type = detectCardType(number);
    const config = getCardFormatConfig(card_type);

    for (config.expected_lengths) |len| {
        if (number.len == len) {
            return true;
        }
    }

    return false;
}

// ============================================================================
// Utility Functions
// ============================================================================

/// Clean a number string (remove spaces and dashes)
pub fn cleanNumber(allocator: std.mem.Allocator, input: []const u8) LuhnError![]u8 {
    var result = std.ArrayList(u8).init(allocator);
    errdefer result.deinit();

    for (input) |c| {
        switch (c) {
            '0'...'9' => try result.append(c),
            ' ', '-' => {}, // Skip spaces and dashes
            else => return LuhnError.InvalidCharacter,
        }
    }

    if (result.items.len == 0) {
        return LuhnError.EmptyInput;
    }

    return result.toOwnedSlice();
}

/// Format a number with spaces for readability
pub fn formatNumber(allocator: std.mem.Allocator, number: []const u8, group_size: usize) LuhnError![]u8 {
    var result = std.ArrayList(u8).init(allocator);
    errdefer result.deinit();

    for (number, 0..) |c, i| {
        if (i > 0 and i % group_size == 0) {
            try result.append(' ');
        }
        try result.append(c);
    }

    return result.toOwnedSlice();
}

/// Generate a random valid Luhn number (for testing)
pub fn generateTestNumber(allocator: std.mem.Allocator, prefix: []const u8, length: usize) ![]u8 {
    if (length < prefix.len + 1) {
        return LuhnError.InvalidLength;
    }

    var result = std.ArrayList(u8).init(allocator);
    errdefer result.deinit();

    // Add prefix
    try result.appendSlice(prefix);

    // Fill with random digits (except last one)
    var rng = std.Random.DefaultPrng.init(@as(u64, @intCast(std.time.timestamp())));
    const random = rng.random();

    while (result.items.len < length - 1) {
        const digit = random.int(u8) % 10;
        try result.append('0' + digit);
    }

    // Calculate and append check digit
    const check_digit = try calculateCheckDigit(result.items);
    try result.append('0' + check_digit);

    return result.toOwnedSlice();
}

// ============================================================================
// IMEI Validation (uses Luhn)
// ============================================================================

/// Validate IMEI (International Mobile Equipment Identity)
/// IMEI is 15 digits, uses Luhn algorithm
pub fn validateIMEI(imei: []const u8) LuhnError!bool {
    if (imei.len != 15) {
        return LuhnError.InvalidLength;
    }

    // Check all digits
    for (imei) |c| {
        if (c < '0' or c > '9') {
            return LuhnError.InvalidCharacter;
        }
    }

    return validate(imei);
}

/// Validate IMEISV (IMEI with Software Version)
/// IMEISV is 16 digits, does NOT use Luhn (last 2 digits are software version)
pub fn validateIMEISV(imeisv: []const u8) LuhnError!bool {
    if (imeisv.len != 16) {
        return LuhnError.InvalidLength;
    }

    // Check all digits
    for (imeisv) |c| {
        if (c < '0' or c > '9') {
            return LuhnError.InvalidCharacter;
        }
    }

    // IMEISV first 14 digits + check digit should be valid IMEI
    // So we validate first 15 digits with Luhn
    return validate(imeisv[0..15]);
}

// ============================================================================
// National Identifier Validation (National ID numbers using Luhn)
// ============================================================================

/// Validate South African ID number (13 digits, uses Luhn)
pub fn validateSouthAfricanID(id: []const u8) LuhnError!bool {
    if (id.len != 13) {
        return LuhnError.InvalidLength;
    }

    for (id) |c| {
        if (c < '0' or c > '9') {
            return LuhnError.InvalidCharacter;
        }
    }

    return validate(id);
}

/// Validate Canadian SIN (Social Insurance Number, 9 digits, uses Luhn)
pub fn validateCanadianSIN(sin: []const u8) LuhnError!bool {
    if (sin.len != 9) {
        return LuhnError.InvalidLength;
    }

    for (sin) |c| {
        if (c < '0' or c > '9') {
            return LuhnError.InvalidCharacter;
        }
    }

    return validate(sin);
}

// ============================================================================
// Tests
// ============================================================================

test "calculateCheckDigit" {
    // Test cases: number without check digit -> expected check digit
    try std.testing.expectEqual(@as(u8, 3), try calculateCheckDigit("7992739871"));
    try std.testing.expectEqual(@as(u8, 6), try calculateCheckDigit("4992739871"));
}

test "validate basic" {
    // Known valid numbers
    try std.testing.expect(try validate("79927398713"));
    try std.testing.expect(try validate("49927398716"));
    try std.testing.expect(try validate("4242424242424242")); // Visa test
    try std.testing.expect(try validate("5555555555554444")); // Mastercard test

    // Invalid numbers
    try std.testing.expect(!try validate("79927398710"));
    try std.testing.expect(!try validate("79927398711"));
    try std.testing.expect(!try validate("79927398712"));
    try std.testing.expect(!try validate("4242424242424241")); // Wrong check digit
}

test "validate with invalid character" {
    _ = validate("7992a398713") catch |err| {
        try std.testing.expectEqual(LuhnError.InvalidCharacter, err);
    };
}

test "validate empty" {
    _ = validate("") catch |err| {
        try std.testing.expectEqual(LuhnError.EmptyInput, err);
    };
}

test "detectCardType Visa" {
    try std.testing.expectEqual(CardType.visa, detectCardType("4242424242424242"));
    try std.testing.expectEqual(CardType.visa, detectCardType("4000000000000002"));
    try std.testing.expectEqual(CardType.visa, detectCardType("4111111111111111"));
}

test "detectCardType Mastercard" {
    try std.testing.expectEqual(CardType.mastercard, detectCardType("5555555555554444"));
    try std.testing.expectEqual(CardType.mastercard, detectCardType("2221000000000009"));
    try std.testing.expectEqual(CardType.mastercard, detectCardType("2720990000000006"));
}

test "detectCardType Amex" {
    try std.testing.expectEqual(CardType.amex, detectCardType("378282246310005"));
    try std.testing.expectEqual(CardType.amex, detectCardType("371449635398431"));
}

test "detectCardType Discover" {
    try std.testing.expectEqual(CardType.discover, detectCardType("6011111111111117"));
    try std.testing.expectEqual(CardType.discover, detectCardType("6011000990139424"));
}

test "detectCardType JCB" {
    try std.testing.expectEqual(CardType.jcb, detectCardType("3530111333300000"));
    try std.testing.expectEqual(CardType.jcb, detectCardType("3566002020360505"));
}

test "detectCardType Unknown" {
    try std.testing.expectEqual(CardType.unknown, detectCardType("1234567890123456"));
}

test "cleanNumber" {
    const allocator = std.testing.allocator;

    const result1 = try cleanNumber(allocator, "4242 4242 4242 4242");
    defer allocator.free(result1);
    try std.testing.expectEqualSlices(u8, "4242424242424242", result1);

    const result2 = try cleanNumber(allocator, "4242-4242-4242-4242");
    defer allocator.free(result2);
    try std.testing.expectEqualSlices(u8, "4242424242424242", result2);
}

test "formatNumber" {
    const allocator = std.testing.allocator;

    const result = try formatNumber(allocator, "4242424242424242", 4);
    defer allocator.free(result);
    try std.testing.expectEqualSlices(u8, "4242 4242 4242 4242", result);
}

test "validateIMEI" {
    // Valid IMEI (Luhn valid)
    try std.testing.expect(try validateIMEI("490154203237518"));

    // Invalid IMEI
    try std.testing.expect(!try validateIMEI("490154203237519"));

    // Wrong length
    _ = validateIMEI("49015420323751") catch |err| {
        try std.testing.expectEqual(LuhnError.InvalidLength, err);
    };
}

test "validateCanadianSIN" {
    // Valid Canadian SIN
    try std.testing.expect(try validateCanadianSIN("046454286"));

    // Invalid SIN
    try std.testing.expect(!try validateCanadianSIN("046454287"));
}

test "generateTestNumber" {
    const allocator = std.testing.allocator;

    const number = try generateTestNumber(allocator, "4242", 16);
    defer allocator.free(number);

    try std.testing.expectEqual(@as(usize, 16), number.len);
    try std.testing.expectEqualSlices(u8, "4242", number[0..4]);
    try std.testing.expect(try validate(number));
}

test "validateWithDetails" {
    const allocator = std.testing.allocator;

    var result = try validateWithDetails(allocator, "4242424242424242");
    defer result.deinit(allocator);

    try std.testing.expect(result.is_valid);
    try std.testing.expectEqual(CardType.visa, result.card_type);
}

test "CardType name" {
    try std.testing.expectEqualSlices(u8, "Visa", CardType.visa.name());
    try std.testing.expectEqualSlices(u8, "Mastercard", CardType.mastercard.name());
    try std.testing.expectEqualSlices(u8, "Unknown", CardType.unknown.name());
}

test "hasValidLength" {
    try std.testing.expect(hasValidLength("4242424242424242")); // Visa 16
    try std.testing.expect(hasValidLength("378282246310005")); // Amex 15
    try std.testing.expect(!hasValidLength("424242424")); // Too short
}