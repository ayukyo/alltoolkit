const std = @import("std");

/// Number operation errors
pub const NumberError = error{
    OutOfMemory,
    InvalidFormat,
    Overflow,
    InvalidBase,
    InvalidPrecision,
};

// ============================================================================
// Number Parsing
// ============================================================================

/// Parse unsigned integer from string with specified base (2-36)
pub fn parseU64(input: []const u8, base: u8) NumberError!u64 {
    if (base < 2 or base > 36) return NumberError.InvalidBase;
    if (input.len == 0) return NumberError.InvalidFormat;
    
    var result: u64 = 0;
    
    for (input) |c| {
        const digit_u8 = charToDigit(c, base) catch return NumberError.InvalidFormat;
        
        const mul_result = std.math.mul(u64, result, base) catch return NumberError.Overflow;
        const add_result = std.math.add(u64, mul_result, digit_u8) catch return NumberError.Overflow;
        result = add_result;
    }
    
    return result;
}

/// Parse signed integer from string with specified base (2-36)
pub fn parseI64(input: []const u8, base: u8) NumberError!i64 {
    if (base < 2 or base > 36) return NumberError.InvalidBase;
    if (input.len == 0) return NumberError.InvalidFormat;
    
    var start: usize = 0;
    var negative = false;
    
    if (input.len > 1) {
        if (input[0] == '-') {
            negative = true;
            start = 1;
        } else if (input[0] == '+') {
            start = 1;
        }
    }
    
    if (start >= input.len) return NumberError.InvalidFormat;
    
    const unsigned_val = try parseU64(input[start..], base);
    
    if (unsigned_val > std.math.maxInt(i64)) {
        return NumberError.Overflow;
    }
    
    const signed_val: i64 = @intCast(unsigned_val);
    return if (negative) -signed_val else signed_val;
}

/// Parse float from string (f64)
pub fn parseFloat64(input: []const u8) NumberError!f64 {
    if (input.len == 0) return NumberError.InvalidFormat;
    
    var result: f64 = 0.0;
    var decimal_place: f64 = 0.1;
    var in_decimal = false;
    var negative = false;
    var start: usize = 0;
    var found_digit = false;
    
    if (input[0] == '-') {
        negative = true;
        start = 1;
    } else if (input[0] == '+') {
        start = 1;
    }
    
    for (input[start..]) |c| {
        if (c == '.') {
            if (in_decimal) return NumberError.InvalidFormat;
            in_decimal = true;
        } else if (c >= '0' and c <= '9') {
            found_digit = true;
            const digit: f64 = @floatFromInt(c - '0');
            if (in_decimal) {
                result += digit * decimal_place;
                decimal_place /= 10.0;
            } else {
                result = result * 10.0 + digit;
            }
        } else {
            return NumberError.InvalidFormat;
        }
    }
    
    if (!found_digit) return NumberError.InvalidFormat;
    
    return if (negative) -result else result;
}

// ============================================================================
// Number Formatting
// ============================================================================

/// Format u64 with thousands separator
pub fn formatU64WithSeparator(
    allocator: std.mem.Allocator,
    value: u64,
    separator: []const u8,
) NumberError![]u8 {
    var buf: [32]u8 = undefined;
    const formatted = std.fmt.bufPrint(&buf, "{}", .{value}) catch return NumberError.Overflow;
    
    const digits = formatted.len;
    const groups = (digits + 2) / 3;
    
    if (groups <= 1) {
        return allocator.dupe(u8, formatted) catch return NumberError.OutOfMemory;
    }
    
    const sep_len = separator.len;
    const result_len = formatted.len + (groups - 1) * sep_len;
    const result = allocator.alloc(u8, result_len) catch return NumberError.OutOfMemory;
    
    var pos: usize = 0;
    var src_pos: usize = 0;
    const first_group = digits % 3;
    
    if (first_group > 0) {
        @memcpy(result[pos .. pos + first_group], formatted[0..first_group]);
        pos += first_group;
        src_pos = first_group;
        
        if (src_pos < digits) {
            @memcpy(result[pos .. pos + sep_len], separator);
            pos += sep_len;
        }
    }
    
    while (src_pos < digits) {
        const end = @min(src_pos + 3, digits);
        @memcpy(result[pos .. pos + (end - src_pos)], formatted[src_pos..end]);
        pos += end - src_pos;
        src_pos = end;
        
        if (src_pos < digits) {
            @memcpy(result[pos .. pos + sep_len], separator);
            pos += sep_len;
        }
    }
    
    return result;
}

/// Format i64 with thousands separator
pub fn formatI64WithSeparator(
    allocator: std.mem.Allocator,
    value: i64,
    separator: []const u8,
) NumberError![]u8 {
    if (value >= 0) {
        return formatU64WithSeparator(allocator, @as(u64, @intCast(value)), separator);
    }
    
    const abs_val = @as(u64, @intCast(-value));
    const unsigned_formatted = try formatU64WithSeparator(allocator, abs_val, separator);
    defer allocator.free(unsigned_formatted);
    
    const result = allocator.alloc(u8, unsigned_formatted.len + 1) catch return NumberError.OutOfMemory;
    result[0] = '-';
    @memcpy(result[1..], unsigned_formatted);
    return result;
}

/// Format float with precision (f64)
pub fn formatFloat64(
    allocator: std.mem.Allocator,
    value: f64,
    precision: usize,
) NumberError![]u8 {
    if (precision > 20) return NumberError.InvalidPrecision;
    
    var buf: [128]u8 = undefined;
    const formatted = std.fmt.bufPrint(&buf, "{d}", .{value}) catch return NumberError.Overflow;
    
    // Find decimal point
    const dot_pos = for (formatted, 0..) |c, i| {
        if (c == '.') break i;
    } else formatted.len;
    
    // Handle scientific notation
    const e_pos = for (formatted, 0..) |c, i| {
        if (c == 'e' or c == 'E') break i;
    } else formatted.len;
    
    if (e_pos < formatted.len) {
        return allocator.dupe(u8, formatted) catch return NumberError.OutOfMemory;
    }
    
    const result_len = if (precision == 0)
        dot_pos
    else if (dot_pos == formatted.len)
        formatted.len + 1 + precision  // Need to add decimal point
    else
        dot_pos + 1 + precision;
    
    const result = allocator.alloc(u8, result_len) catch return NumberError.OutOfMemory;
    
    if (precision == 0) {
        @memcpy(result[0..dot_pos], formatted[0..dot_pos]);
        return result;
    }
    
    @memcpy(result[0..dot_pos], formatted[0..dot_pos]);
    result[dot_pos] = '.';
    
    const after_dot = if (dot_pos < formatted.len) formatted[dot_pos + 1 ..] else "";
    const copy_len = @min(after_dot.len, precision);
    @memcpy(result[dot_pos + 1 .. dot_pos + 1 + copy_len], after_dot[0..copy_len]);
    
    if (copy_len < precision) {
        @memset(result[dot_pos + 1 + copy_len ..], '0');
    }
    
    return result;
}

/// Format u64 as hexadecimal
pub fn formatHex(allocator: std.mem.Allocator, value: u64, uppercase: bool) NumberError![]u8 {
    const hex_chars = if (uppercase) "0123456789ABCDEF" else "0123456789abcdef";
    
    const max_len = 16 + 2;
    const result = allocator.alloc(u8, max_len) catch return NumberError.OutOfMemory;
    
    result[0] = '0';
    result[1] = 'x';
    
    var pos: usize = 2;
    var started = false;
    
    var shift: usize = 60;
    while (true) {
        const nibble = @as(u4, @intCast((value >> @intCast(shift)) & 0xF));
        if (started or nibble != 0 or shift == 0) {
            result[pos] = hex_chars[nibble];
            pos += 1;
            started = true;
        }
        if (shift == 0) break;
        shift -= 4;
    }
    
    return allocator.realloc(result, pos) catch result[0..pos];
}

/// Format u64 as binary
pub fn formatBinary(allocator: std.mem.Allocator, value: u64) NumberError![]u8 {
    const max_len = 64 + 2;
    const result = allocator.alloc(u8, max_len) catch return NumberError.OutOfMemory;
    
    result[0] = '0';
    result[1] = 'b';
    
    var pos: usize = 2;
    var started = false;
    
    var shift: usize = 63;
    while (true) {
        const bit = (value >> @intCast(shift)) & 1;
        if (started or bit != 0 or shift == 0) {
            result[pos] = if (bit == 1) '1' else '0';
            pos += 1;
            started = true;
        }
        if (shift == 0) break;
        shift -= 1;
    }
    
    return allocator.realloc(result, pos) catch result[0..pos];
}

/// Format u64 as octal
pub fn formatOctal(allocator: std.mem.Allocator, value: u64) NumberError![]u8 {
    const max_len = 22 + 2;
    const result = allocator.alloc(u8, max_len) catch return NumberError.OutOfMemory;
    
    result[0] = '0';
    result[1] = 'o';
    
    var pos: usize = 2;
    var started = false;
    
    var shift: usize = 60;
    while (true) {
        const digit = @as(u8, @intCast((value >> @intCast(shift)) & 0o7));
        if (started or digit != 0 or shift == 0) {
            result[pos] = '0' + digit;
            pos += 1;
            started = true;
        }
        if (shift == 0) break;
        shift -= 3;
    }
    
    return allocator.realloc(result, pos) catch result[0..pos];
}

// ============================================================================
// Number Range Operations
// ============================================================================

/// Clamp i64 value between min and max
pub fn clampI64(value: i64, min_val: i64, max_val: i64) i64 {
    if (value < min_val) return min_val;
    if (value > max_val) return max_val;
    return value;
}

/// Clamp u64 value between min and max
pub fn clampU64(value: u64, min_val: u64, max_val: u64) u64 {
    if (value < min_val) return min_val;
    if (value > max_val) return max_val;
    return value;
}

/// Check if value is in range (inclusive)
pub fn inRangeI64(value: i64, min_val: i64, max_val: i64) bool {
    return value >= min_val and value <= max_val;
}

pub fn inRangeU64(value: u64, min_val: u64, max_val: u64) bool {
    return value >= min_val and value <= max_val;
}

/// Linear interpolation between two values
pub fn lerp(a: f64, b: f64, t: f64) f64 {
    return a + (b - a) * t;
}

/// Map value from one range to another
pub fn mapRange(value: f64, in_min: f64, in_max: f64, out_min: f64, out_max: f64) f64 {
    return (value - in_min) / (in_max - in_min) * (out_max - out_min) + out_min;
}

/// Wrap value within range
pub fn wrapI64(value: i64, min_val: i64, max_val: i64) i64 {
    const range = max_val - min_val;
    if (range == 0) return min_val;
    
    var result = value;
    while (result < min_val) result += range;
    while (result > max_val) result -= range;
    return result;
}

// ============================================================================
// Number Utilities
// ============================================================================

/// Check if integer is even
pub fn isEven(value: i64) bool {
    return @rem(value, 2) == 0;
}

/// Check if integer is odd
pub fn isOdd(value: i64) bool {
    return @rem(value, 2) != 0;
}

/// Check if integer is power of 2
pub fn isPowerOfTwo(value: u64) bool {
    return value > 0 and (value & (value - 1)) == 0;
}

/// Get the next power of 2
pub fn nextPowerOfTwo(value: u64) u64 {
    if (value == 0) return 1;
    
    var v: u64 = value - 1;
    var shift: usize = 1;
    
    while (shift < 64) : (shift <<= 1) {
        v |= v >> @intCast(shift);
    }
    
    return v + 1;
}

/// Get the previous power of 2
pub fn prevPowerOfTwo(value: u64) u64 {
    if (value <= 1) return 1;
    return nextPowerOfTwo(value >> 1);
}

/// Count trailing zeros
pub fn countTrailingZeros(value: u64) usize {
    if (value == 0) return 64;
    var count: usize = 0;
    var v = value;
    while (v & 1 == 0) : (count += 1) {
        v >>= 1;
    }
    return count;
}

/// Count leading zeros
pub fn countLeadingZeros(value: u64) usize {
    if (value == 0) return 64;
    var count: usize = 0;
    var shift: u6 = 63;
    while (shift > 0 and (value >> shift & 1) == 0) : (count += 1) {
        shift -= 1;
    }
    return count;
}

/// Count set bits (popcount)
pub fn popcount(value: u64) usize {
    var count: usize = 0;
    var v = value;
    while (v > 0) : (count += 1) {
        v &= v - 1;
    }
    return count;
}

/// Get the number of digits in an integer
pub fn digitCountU64(value: u64) usize {
    if (value == 0) return 1;
    var count: usize = 0;
    var v = value;
    while (v > 0) : (count += 1) {
        v /= 10;
    }
    return count;
}

pub fn digitCountI64(value: i64) usize {
    if (value == 0) return 1;
    const abs_val: u64 = if (value < 0) @intCast(-value) else @intCast(value);
    return digitCountU64(abs_val);
}

/// Get digit at position (0 = rightmost)
pub fn digitAtU64(value: u64, position: usize) ?u8 {
    var v = value;
    var pos: usize = 0;
    while (v > 0 and pos <= position) {
        if (pos == position) return @intCast(v % 10);
        v /= 10;
        pos += 1;
    }
    return null;
}

// ============================================================================
// Random Number Utilities
// ============================================================================

/// Simple linear congruential generator
pub const SimpleRandom = struct {
    state: u64,
    
    pub fn init(seed: u64) SimpleRandom {
        return .{ .state = seed };
    }
    
    pub fn next(self: *SimpleRandom) u64 {
        self.state = self.state *% 1103515245 +% 12345;
        return (self.state >> 16) & 0x7FFF_FFFF;
    }
    
    pub fn nextU64(self: *SimpleRandom, min_val: u64, max_val: u64) u64 {
        const range = max_val - min_val + 1;
        return min_val + (self.next() % range);
    }
    
    pub fn nextI64(self: *SimpleRandom, min_val: i64, max_val: i64) i64 {
        const range = max_val - min_val + 1;
        return min_val + @as(i64, @intCast(self.next() % @as(u64, @intCast(range))));
    }
    
    pub fn nextFloat64(self: *SimpleRandom) f64 {
        return @as(f64, @floatFromInt(self.next())) / @as(f64, @floatFromInt(@as(u64, 1) << 31));
    }
    
    pub fn nextFloat64Range(self: *SimpleRandom, min_val: f64, max_val: f64) f64 {
        return min_val + (max_val - min_val) * self.nextFloat64();
    }
    
    pub fn shuffle(self: *SimpleRandom, comptime T: type, items: []T) void {
        if (items.len == 0) return;
        var i: usize = items.len - 1;
        while (i > 0) : (i -= 1) {
            const j = @as(usize, @intCast(self.next() % @as(u64, i + 1)));
            const tmp = items[i];
            items[i] = items[j];
            items[j] = tmp;
        }
    }
};

// ============================================================================
// Math Utilities
// ============================================================================

/// Greatest common divisor
pub fn gcd(a: u64, b: u64) u64 {
    var x = a;
    var y = b;
    while (y != 0) {
        const temp = y;
        y = x % y;
        x = temp;
    }
    return x;
}

/// Least common multiple
pub fn lcm(a: u64, b: u64) u64 {
    if (a == 0 or b == 0) return 0;
    return (a / gcd(a, b)) * b;
}

/// Factorial (returns null if too large)
pub fn factorial(n: usize) ?u64 {
    if (n > 20) return null;
    var result: u64 = 1;
    for (1..n + 1) |i| {
        result *= @intCast(i);
    }
    return result;
}

/// Fibonacci number
pub fn fibonacci(n: usize) u64 {
    if (n == 0) return 0;
    if (n == 1) return 1;
    
    var prev: u64 = 0;
    var curr: u64 = 1;
    for (2..n + 1) |_| {
        const next = prev + curr;
        prev = curr;
        curr = next;
    }
    return curr;
}

/// Check if number is prime
pub fn isPrime(n: u64) bool {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    if (n == 3) return true;
    if (n % 3 == 0) return false;
    
    var i: u64 = 5;
    while (i * i <= n) : (i += 6) {
        if (n % i == 0 or n % (i + 2) == 0) return false;
    }
    return true;
}

/// Integer square root
pub fn isqrt(n: u64) u64 {
    if (n == 0) return 0;
    
    var x: u64 = n;
    var y: u64 = (x + 1) / 2;
    
    while (y < x) {
        x = y;
        y = (x + n / x) / 2;
    }
    
    return x;
}

/// Sum of digits
pub fn sumOfDigits(n: i64) i64 {
    const abs_val: u64 = if (n < 0) @intCast(-n) else @intCast(n);
    var result: i64 = 0;
    var v = abs_val;
    while (v > 0) {
        result += @as(i64, @intCast(v % 10));
        v /= 10;
    }
    return result;
}

/// Product of digits
pub fn productOfDigits(n: i64) i64 {
    const abs_val: u64 = if (n < 0) @intCast(-n) else @intCast(n);
    if (abs_val == 0) return 0;
    
    var result: i64 = 1;
    var v = abs_val;
    while (v > 0) {
        result *= @as(i64, @intCast(v % 10));
        v /= 10;
    }
    return result;
}

/// Reverse digits
pub fn reverseDigits(n: i64) i64 {
    const is_neg = n < 0;
    const abs_val: u64 = if (is_neg) @intCast(-n) else @intCast(n);
    
    var result: i64 = 0;
    var v = abs_val;
    while (v > 0) {
        result = result * 10 + @as(i64, @intCast(v % 10));
        v /= 10;
    }
    
    return if (is_neg) -result else result;
}

// ============================================================================
// Helper Functions
// ============================================================================

fn charToDigit(c: u8, base: u8) NumberError!u8 {
    const digit: u8 = switch (c) {
        '0'...'9' => c - '0',
        'a'...'z' => c - 'a' + 10,
        'A'...'Z' => c - 'A' + 10,
        else => return NumberError.InvalidFormat,
    };
    if (digit >= base) return NumberError.InvalidFormat;
    return digit;
}

// ============================================================================
// Tests
// ============================================================================

test "parseU64 decimal" {
    try std.testing.expectEqual(@as(u64, 12345), try parseU64("12345", 10));
    try std.testing.expectEqual(@as(u64, 255), try parseU64("255", 10));
}

test "parseU64 binary" {
    try std.testing.expectEqual(@as(u64, 0b10101010), try parseU64("10101010", 2));
    try std.testing.expectEqual(@as(u64, 255), try parseU64("11111111", 2));
}

test "parseU64 hex" {
    try std.testing.expectEqual(@as(u64, 255), try parseU64("FF", 16));
    try std.testing.expectEqual(@as(u64, 0xDEAD), try parseU64("DEAD", 16));
    try std.testing.expectEqual(@as(u64, 0xBEEF), try parseU64("beef", 16));
}

test "parseU64 octal" {
    try std.testing.expectEqual(@as(u64, 255), try parseU64("377", 8));
    try std.testing.expectEqual(@as(u64, 0o777), try parseU64("777", 8));
}

test "parseI64" {
    try std.testing.expectEqual(@as(i64, 12345), try parseI64("12345", 10));
    try std.testing.expectEqual(@as(i64, -12345), try parseI64("-12345", 10));
    try std.testing.expectEqual(@as(i64, 42), try parseI64("+42", 10));
}

test "parseFloat64" {
    try std.testing.expectApproxEqAbs(@as(f64, 3.14159), try parseFloat64("3.14159"), 0.00001);
    try std.testing.expectApproxEqAbs(@as(f64, -123.456), try parseFloat64("-123.456"), 0.0001);
    try std.testing.expectApproxEqAbs(@as(f64, 0.0), try parseFloat64("0"), 0.0001);
}

test "formatU64WithSeparator" {
    const allocator = std.testing.allocator;
    
    const result1 = try formatU64WithSeparator(allocator, 1234567, ",");
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("1,234,567", result1);
    
    const result2 = try formatU64WithSeparator(allocator, 123, ",");
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("123", result2);
}

test "formatI64WithSeparator" {
    const allocator = std.testing.allocator;
    
    const result1 = try formatI64WithSeparator(allocator, 1234567, ",");
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("1,234,567", result1);
    
    const result2 = try formatI64WithSeparator(allocator, -1234567, ",");
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("-1,234,567", result2);
}

test "formatFloat64" {
    const allocator = std.testing.allocator;
    
    const result1 = try formatFloat64(allocator, 3.14159, 2);
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("3.14", result1);
    
    const result2 = try formatFloat64(allocator, 3.14159, 0);
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("3", result2);
    
    const result3 = try formatFloat64(allocator, 3.0, 5);
    defer allocator.free(result3);
    try std.testing.expectEqualStrings("3.00000", result3);
}

test "formatHex" {
    const allocator = std.testing.allocator;
    
    const result1 = try formatHex(allocator, 255, false);
    defer allocator.free(result1);
    try std.testing.expectEqualStrings("0xff", result1);
    
    const result2 = try formatHex(allocator, 0xDEAD, true);
    defer allocator.free(result2);
    try std.testing.expectEqualStrings("0xDEAD", result2);
}

test "formatBinary" {
    const allocator = std.testing.allocator;
    
    const result = try formatBinary(allocator, 0b10101010);
    defer allocator.free(result);
    try std.testing.expectEqualStrings("0b10101010", result);
}

test "formatOctal" {
    const allocator = std.testing.allocator;
    
    const result = try formatOctal(allocator, 255);
    defer allocator.free(result);
    try std.testing.expectEqualStrings("0o377", result);
}

test "clamp and inRange" {
    try std.testing.expectEqual(@as(i64, 5), clampI64(3, 5, 10));
    try std.testing.expectEqual(@as(i64, 7), clampI64(7, 5, 10));
    try std.testing.expectEqual(@as(i64, 10), clampI64(15, 5, 10));
    
    try std.testing.expect(inRangeI64(7, 5, 10));
    try std.testing.expect(inRangeI64(5, 5, 10));
    try std.testing.expect(!inRangeI64(4, 5, 10));
}

test "lerp" {
    try std.testing.expectApproxEqAbs(@as(f64, 5.0), lerp(0, 10, 0.5), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 0.0), lerp(0, 10, 0.0), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 10.0), lerp(0, 10, 1.0), 0.001);
}

test "mapRange" {
    try std.testing.expectApproxEqAbs(@as(f64, 50.0), mapRange(5, 0, 10, 0, 100), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 0.0), mapRange(0, 0, 10, 0, 100), 0.001);
    try std.testing.expectApproxEqAbs(@as(f64, 100.0), mapRange(10, 0, 10, 0, 100), 0.001);
}

test "isEven and isOdd" {
    try std.testing.expect(isEven(4));
    try std.testing.expect(!isEven(5));
    try std.testing.expect(isOdd(5));
    try std.testing.expect(!isOdd(4));
}

test "isPowerOfTwo" {
    try std.testing.expect(isPowerOfTwo(1));
    try std.testing.expect(isPowerOfTwo(2));
    try std.testing.expect(isPowerOfTwo(4));
    try std.testing.expect(isPowerOfTwo(8));
    try std.testing.expect(isPowerOfTwo(1024));
    try std.testing.expect(!isPowerOfTwo(3));
    try std.testing.expect(!isPowerOfTwo(0));
}

test "nextPowerOfTwo" {
    try std.testing.expectEqual(@as(u64, 1), nextPowerOfTwo(0));
    try std.testing.expectEqual(@as(u64, 1), nextPowerOfTwo(1));
    try std.testing.expectEqual(@as(u64, 4), nextPowerOfTwo(3));
    try std.testing.expectEqual(@as(u64, 8), nextPowerOfTwo(5));
    try std.testing.expectEqual(@as(u64, 8), nextPowerOfTwo(8));
}

test "popcount" {
    try std.testing.expectEqual(@as(usize, 4), popcount(0b10101010));
    try std.testing.expectEqual(@as(usize, 0), popcount(0));
    try std.testing.expectEqual(@as(usize, 8), popcount(255));
}

test "digitCount" {
    try std.testing.expectEqual(@as(usize, 1), digitCountU64(0));
    try std.testing.expectEqual(@as(usize, 1), digitCountU64(5));
    try std.testing.expectEqual(@as(usize, 2), digitCountU64(15));
    try std.testing.expectEqual(@as(usize, 5), digitCountU64(12345));
    try std.testing.expectEqual(@as(usize, 5), digitCountI64(-12345));
}

test "digitAt" {
    try std.testing.expectEqual(@as(u8, 5), digitAtU64(12345, 0).?);
    try std.testing.expectEqual(@as(u8, 4), digitAtU64(12345, 1).?);
    try std.testing.expectEqual(@as(u8, 1), digitAtU64(12345, 4).?);
    try std.testing.expectEqual(@as(?u8, null), digitAtU64(12345, 5));
}

test "SimpleRandom" {
    var rng = SimpleRandom.init(42);
    
    const v1 = rng.next();
    const v2 = rng.next();
    try std.testing.expect(v1 != v2);
    
    // Reset with same seed should produce same sequence
    rng = SimpleRandom.init(42);
    try std.testing.expectEqual(v1, rng.next());
    try std.testing.expectEqual(v2, rng.next());
    
    // Range test
    const in_range = rng.nextI64(0, 10);
    try std.testing.expect(in_range >= 0 and in_range <= 10);
}

test "gcd and lcm" {
    try std.testing.expectEqual(@as(u64, 6), gcd(12, 18));
    try std.testing.expectEqual(@as(u64, 1), gcd(7, 11));
    try std.testing.expectEqual(@as(u64, 36), lcm(12, 18));
}

test "factorial" {
    try std.testing.expectEqual(@as(u64, 1), factorial(0).?);
    try std.testing.expectEqual(@as(u64, 1), factorial(1).?);
    try std.testing.expectEqual(@as(u64, 120), factorial(5).?);
    try std.testing.expectEqual(@as(u64, 2432902008176640000), factorial(20).?);
    try std.testing.expectEqual(@as(?u64, null), factorial(21));
}

test "fibonacci" {
    try std.testing.expectEqual(@as(u64, 0), fibonacci(0));
    try std.testing.expectEqual(@as(u64, 1), fibonacci(1));
    try std.testing.expectEqual(@as(u64, 1), fibonacci(2));
    try std.testing.expectEqual(@as(u64, 5), fibonacci(5));
    try std.testing.expectEqual(@as(u64, 55), fibonacci(10));
}

test "isPrime" {
    try std.testing.expect(!isPrime(0));
    try std.testing.expect(!isPrime(1));
    try std.testing.expect(isPrime(2));
    try std.testing.expect(isPrime(3));
    try std.testing.expect(!isPrime(4));
    try std.testing.expect(isPrime(5));
    try std.testing.expect(!isPrime(100));
    try std.testing.expect(isPrime(97));
}

test "isqrt" {
    try std.testing.expectEqual(@as(u64, 0), isqrt(0));
    try std.testing.expectEqual(@as(u64, 1), isqrt(1));
    try std.testing.expectEqual(@as(u64, 1), isqrt(2));
    try std.testing.expectEqual(@as(u64, 1), isqrt(3));
    try std.testing.expectEqual(@as(u64, 2), isqrt(4));
    try std.testing.expectEqual(@as(u64, 10), isqrt(100));
    try std.testing.expectEqual(@as(u64, 10), isqrt(120));
}

test "sumOfDigits" {
    try std.testing.expectEqual(@as(i64, 15), sumOfDigits(12345));
    try std.testing.expectEqual(@as(i64, 15), sumOfDigits(-12345));
    try std.testing.expectEqual(@as(i64, 0), sumOfDigits(0));
}

test "productOfDigits" {
    try std.testing.expectEqual(@as(i64, 120), productOfDigits(12345));
    try std.testing.expectEqual(@as(i64, 0), productOfDigits(12305));
    try std.testing.expectEqual(@as(i64, 0), productOfDigits(0));
}

test "reverseDigits" {
    try std.testing.expectEqual(@as(i64, 54321), reverseDigits(12345));
    try std.testing.expectEqual(@as(i64, -54321), reverseDigits(-12345));
    try std.testing.expectEqual(@as(i64, 0), reverseDigits(0));
}

test "countTrailingZeros and countLeadingZeros" {
    try std.testing.expectEqual(@as(usize, 3), countTrailingZeros(0b00001000));
    try std.testing.expectEqual(@as(usize, 0), countTrailingZeros(0b00001001));
    try std.testing.expectEqual(@as(usize, 64), countTrailingZeros(0));
    
    try std.testing.expectEqual(@as(usize, 60), countLeadingZeros(0b00001000));
    try std.testing.expectEqual(@as(usize, 0), countLeadingZeros(@as(u64, 0x8000000000000000)));
    try std.testing.expectEqual(@as(usize, 64), countLeadingZeros(0));
}

test "wrap" {
    try std.testing.expectEqual(@as(i64, 5), wrapI64(5, 0, 10));
    try std.testing.expectEqual(@as(i64, 1), wrapI64(11, 0, 10));
    try std.testing.expectEqual(@as(i64, 9), wrapI64(-1, 0, 10));
}

test "shuffle" {
    var rng = SimpleRandom.init(42);
    var arr = [_]i32{ 1, 2, 3, 4, 5 };
    rng.shuffle(i32, &arr);
    
    // Check array is still valid (all elements present)
    var sum: i32 = 0;
    for (arr) |v| sum += v;
    try std.testing.expectEqual(@as(i32, 15), sum);
}