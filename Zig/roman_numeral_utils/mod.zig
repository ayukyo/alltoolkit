const std = @import("std");

/// 罗马数字错误类型
pub const RomanError = error{
    InvalidRomanNumeral,
    OutOfRange,
    EmptyInput,
    InvalidCharacter,
    DivisionByZero,
    OutOfMemory,
};

/// 基本罗马数字映射表（按值降序排列）
const ROMAN_VALUES = [_]struct { value: u32, numeral: []const u8 }{
    .{ .value = 1000, .numeral = "M" },
    .{ .value = 900, .numeral = "CM" },
    .{ .value = 500, .numeral = "D" },
    .{ .value = 400, .numeral = "CD" },
    .{ .value = 100, .numeral = "C" },
    .{ .value = 90, .numeral = "XC" },
    .{ .value = 50, .numeral = "L" },
    .{ .value = 40, .numeral = "XL" },
    .{ .value = 10, .numeral = "X" },
    .{ .value = 9, .numeral = "IX" },
    .{ .value = 5, .numeral = "V" },
    .{ .value = 4, .numeral = "IV" },
    .{ .value = 1, .numeral = "I" },
};

/// 单字符罗马数字值映射
const ROMAN_CHARS = [_]struct { char: u8, value: u32 }{
    .{ .char = 'I', .value = 1 },
    .{ .char = 'V', .value = 5 },
    .{ .char = 'X', .value = 10 },
    .{ .char = 'L', .value = 50 },
    .{ .char = 'C', .value = 100 },
    .{ .char = 'D', .value = 500 },
    .{ .char = 'M', .value = 1000 },
};

/// 获取单个罗马数字字符的值
fn getCharValue(char: u8) ?u32 {
    for (ROMAN_CHARS) |entry| {
        if (entry.char == char) {
            return entry.value;
        }
    }
    return null;
}

/// 将整数转换为罗马数字
/// 支持范围：1-3999
pub fn intToRoman(allocator: std.mem.Allocator, num: u32) RomanError![]u8 {
    if (num < 1) {
        return RomanError.OutOfRange;
    }
    if (num > 3999) {
        return RomanError.OutOfRange;
    }

    var result = std.ArrayList(u8).init(allocator);
    defer result.deinit();

    var remaining = num;

    for (ROMAN_VALUES) |entry| {
        while (remaining >= entry.value) {
            try result.appendSlice(entry.numeral);
            remaining -= entry.value;
        }
    }

    return result.toOwnedSlice();
}

/// 将罗马数字转换为整数
pub fn romanToInt(roman: []const u8) RomanError!u32 {
    if (roman.len == 0) {
        return RomanError.EmptyInput;
    }

    // 转换为大写
    var upper_buf: [64]u8 = undefined;
    if (roman.len > upper_buf.len) {
        return RomanError.InvalidRomanNumeral;
    }

    for (roman, 0..) |c, i| {
        upper_buf[i] = std.ascii.toUpper(c);
    }
    const upper = upper_buf[0..roman.len];

    // 验证并转换
    var result: u32 = 0;
    var prev_value: u32 = 0;
    var repeat_count: u32 = 1;

    var i: usize = upper.len;
    while (i > 0) {
        i -= 1;
        const char = upper[i];

        const current_value = getCharValue(char) orelse return RomanError.InvalidCharacter;

        // 检查重复规则（I, X, C, M 可重复3次，V, L, D 不可重复）
        if (i > 0 and upper[i - 1] == char) {
            repeat_count += 1;
            const max_repeat: u32 = switch (char) {
                'I', 'X', 'C', 'M' => 3,
                'V', 'L', 'D' => 1,
                else => 3,
            };
            if (repeat_count > max_repeat) {
                return RomanError.InvalidRomanNumeral;
            }
        } else {
            repeat_count = 1;
        }

        if (current_value < prev_value) {
            // 减法原则：检查合法性
            // 只有 I, X, C 可以用于减法
            // I 只能减 V 和 X
            // X 只能减 L 和 C
            // C 只能减 D 和 M
            const prev_char = upper[i + 1];
            const is_valid_subtraction = switch (char) {
                'I' => prev_char == 'V' or prev_char == 'X',
                'X' => prev_char == 'L' or prev_char == 'C',
                'C' => prev_char == 'D' or prev_char == 'M',
                else => false,
            };
            if (!is_valid_subtraction) {
                return RomanError.InvalidRomanNumeral;
            }
            result -= current_value;
        } else {
            result += current_value;
        }

        prev_value = current_value;
    }

    return result;
}

/// 验证罗马数字是否有效
pub fn isValidRoman(roman: []const u8) bool {
    if (roman.len == 0) return false;
    _ = romanToInt(roman) catch return false;
    return true;
}

/// 两个罗马数字相加
pub fn romanAdd(allocator: std.mem.Allocator, roman1: []const u8, roman2: []const u8) RomanError![]u8 {
    const num1 = try romanToInt(roman1);
    const num2 = try romanToInt(roman2);
    const sum = num1 + num2;
    return intToRoman(allocator, sum);
}

/// 两个罗马数字相减
pub fn romanSubtract(allocator: std.mem.Allocator, roman1: []const u8, roman2: []const u8) RomanError![]u8 {
    const num1 = try romanToInt(roman1);
    const num2 = try romanToInt(roman2);
    if (num2 >= num1) {
        return RomanError.OutOfRange;
    }
    return intToRoman(allocator, num1 - num2);
}

/// 两个罗马数字相乘
pub fn romanMultiply(allocator: std.mem.Allocator, roman1: []const u8, roman2: []const u8) RomanError![]u8 {
    const num1 = try romanToInt(roman1);
    const num2 = try romanToInt(roman2);
    const product = num1 * num2;
    return intToRoman(allocator, product);
}

/// 两个罗马数字相除，返回商和余数

pub fn romanDivide(allocator: std.mem.Allocator, roman1: []const u8, roman2: []const u8) RomanError!struct { []u8, []u8 } {
    const num1 = try romanToInt(roman1);
    const num2 = try romanToInt(roman2);
    if (num2 == 0) {
        return RomanError.DivisionByZero;
    }

    const quotient = num1 / num2;
    const remainder = num1 % num2;

    if (quotient == 0) {
        return RomanError.OutOfRange;
    }

    const quotient_roman = try intToRoman(allocator, quotient);
    errdefer allocator.free(quotient_roman);

    const remainder_roman = if (remainder > 0)
        try intToRoman(allocator, remainder)
    else
        try allocator.dupe(u8, "");

    return .{ quotient_roman, remainder_roman };
}

/// 比较两个罗马数字
/// 返回 -1 表示 roman1 < roman2
/// 返回 0 表示相等
/// 返回 1 表示 roman1 > roman2
pub fn romanCompare(roman1: []const u8, roman2: []const u8) RomanError!i32 {
    const num1 = try romanToInt(roman1);
    const num2 = try romanToInt(roman2);
    if (num1 < num2) return -1;
    if (num1 > num2) return 1;
    return 0;
}

/// 罗马数字信息结构
pub const RomanInfo = struct {
    original: []const u8,
    value: u32,
    valid: bool,
    length: usize,
    allocator: ?std.mem.Allocator = null,
    components: ?[]const u8 = null,

    pub fn deinit(self: *RomanInfo) void {
        if (self.allocator) |allocator| {
            if (self.components) |components| {
                allocator.free(components);
            }
        }
    }
};

/// 获取罗马数字的详细信息
pub fn getRomanInfo(allocator: std.mem.Allocator, roman: []const u8) RomanError!RomanInfo {
    const value = romanToInt(roman) catch {
        return RomanInfo{
            .original = roman,
            .value = 0,
            .valid = false,
            .length = roman.len,
        };
    };

    // 计算组件
    const components = try intToRoman(allocator, value);

    return RomanInfo{
        .original = roman,
        .value = value,
        .valid = true,
        .length = roman.len,
        .allocator = allocator,
        .components = components,
    };
}

/// 生成范围内的罗马数字列表
pub fn findRomanRange(allocator: std.mem.Allocator, start: u32, end: u32) RomanError![]struct { u32, []u8 } {
    if (start < 1 or end > 3999) {
        return RomanError.OutOfRange;
    }

    const actual_start = @min(start, end);
    const actual_end = @max(start, end);
    const count = actual_end - actual_start + 1;

    var result = try allocator.alloc(struct { u32, []u8 }, count);

    for (0..count) |i| {
        const num = actual_start + @as(u32, @intCast(i));
        result[i][0] = num;
        result[i][1] = try intToRoman(allocator, num);
    }

    return result;
}

/// 常见罗马数字预定义
pub const COMMON_ROMANS = .{
    .{ 1, "I" },
    .{ 2, "II" },
    .{ 3, "III" },
    .{ 4, "IV" },
    .{ 5, "V" },
    .{ 6, "VI" },
    .{ 7, "VII" },
    .{ 8, "VIII" },
    .{ 9, "IX" },
    .{ 10, "X" },
    .{ 20, "XX" },
    .{ 30, "XXX" },
    .{ 40, "XL" },
    .{ 50, "L" },
    .{ 60, "LX" },
    .{ 70, "LXX" },
    .{ 80, "LXXX" },
    .{ 90, "XC" },
    .{ 100, "C" },
    .{ 200, "CC" },
    .{ 300, "CCC" },
    .{ 400, "CD" },
    .{ 500, "D" },
    .{ 600, "DC" },
    .{ 700, "DCC" },
    .{ 800, "DCCC" },
    .{ 900, "CM" },
    .{ 1000, "M" },
    .{ 1984, "MCMLXXXIV" },
    .{ 1999, "MCMXCIX" },
    .{ 2000, "MM" },
    .{ 2024, "MMXXIV" },
    .{ 2025, "MMXXV" },
    .{ 3000, "MMM" },
    .{ 3999, "MMMCMXCIX" },
};

/// 打印罗马数字信息
pub fn printRomanInfo(roman: []const u8) void {
    std.debug.print("Roman Numeral: {s}\n", .{roman});
    if (romanToInt(roman)) |value| {
        std.debug.print("  Value: {}\n", .{value});
        std.debug.print("  Valid: true\n", .{});
        std.debug.print("  Length: {}\n", .{roman.len});
    } else |_| {
        std.debug.print("  Valid: false (invalid roman numeral)\n", .{});
    }
}

/// 打印整数到罗马数字的转换
pub fn printIntToRoman(num: u32) void {
    std.debug.print("Integer: {}\n", .{num});
    if (intToRoman(std.heap.page_allocator, num)) |roman| {
        defer std.heap.page_allocator.free(roman);
        std.debug.print("  Roman: {s}\n", .{roman});
    } else |_| {
        std.debug.print("  Error: Out of range (1-3999)\n", .{});
    }
}

// ============== 测试 ==============

test "intToRoman - basic conversions" {
    const allocator = std.testing.allocator;

    const cases = [_]struct { num: u32, expected: []const u8 }{
        .{ .num = 1, .expected = "I" },
        .{ .num = 4, .expected = "IV" },
        .{ .num = 5, .expected = "V" },
        .{ .num = 9, .expected = "IX" },
        .{ .num = 10, .expected = "X" },
        .{ .num = 40, .expected = "XL" },
        .{ .num = 50, .expected = "L" },
        .{ .num = 90, .expected = "XC" },
        .{ .num = 100, .expected = "C" },
        .{ .num = 400, .expected = "CD" },
        .{ .num = 500, .expected = "D" },
        .{ .num = 900, .expected = "CM" },
        .{ .num = 1000, .expected = "M" },
        .{ .num = 2024, .expected = "MMXXIV" },
        .{ .num = 3999, .expected = "MMMCMXCIX" },
    };

    for (cases) |case| {
        const result = try intToRoman(allocator, case.num);
        defer allocator.free(result);
        try std.testing.expectEqualSlices(u8, case.expected, result);
    }
}

test "intToRoman - out of range" {
    const allocator = std.testing.allocator;

    try std.testing.expectError(RomanError.OutOfRange, intToRoman(allocator, 0));
    try std.testing.expectError(RomanError.OutOfRange, intToRoman(allocator, 4000));
    try std.testing.expectError(RomanError.OutOfRange, intToRoman(allocator, 10000));
}

test "romanToInt - basic conversions" {
    const cases = [_]struct { roman: []const u8, expected: u32 }{
        .{ .roman = "I", .expected = 1 },
        .{ .roman = "IV", .expected = 4 },
        .{ .roman = "V", .expected = 5 },
        .{ .roman = "IX", .expected = 9 },
        .{ .roman = "X", .expected = 10 },
        .{ .roman = "XL", .expected = 40 },
        .{ .roman = "L", .expected = 50 },
        .{ .roman = "XC", .expected = 90 },
        .{ .roman = "C", .expected = 100 },
        .{ .roman = "CD", .expected = 400 },
        .{ .roman = "D", .expected = 500 },
        .{ .roman = "CM", .expected = 900 },
        .{ .roman = "M", .expected = 1000 },
        .{ .roman = "MMXXIV", .expected = 2024 },
        .{ .roman = "MMMCMXCIX", .expected = 3999 },
    };

    for (cases) |case| {
        const result = try romanToInt(case.roman);
        try std.testing.expectEqual(case.expected, result);
    }
}

test "romanToInt - case insensitive" {
    try std.testing.expectEqual(@as(u32, 10), try romanToInt("x"));
    try std.testing.expectEqual(@as(u32, 10), try romanToInt("X"));
    try std.testing.expectEqual(@as(u32, 2024), try romanToInt("mmxxiv"));
    try std.testing.expectEqual(@as(u32, 2024), try romanToInt("MmXxIv"));
}

test "romanToInt - invalid inputs" {
    try std.testing.expectError(RomanError.EmptyInput, romanToInt(""));
    try std.testing.expectError(RomanError.InvalidCharacter, romanToInt("ABC"));
    try std.testing.expectError(RomanError.InvalidRomanNumeral, romanToInt("IIII"));
    try std.testing.expectError(RomanError.InvalidRomanNumeral, romanToInt("VV"));
    try std.testing.expectError(RomanError.InvalidRomanNumeral, romanToInt("IC"));
    try std.testing.expectError(RomanError.InvalidRomanNumeral, romanToInt("IM"));
}

test "round-trip conversion" {
    const allocator = std.testing.allocator;

    var i: u32 = 1;
    while (i <= 100) : (i += 1) {
        const roman = try intToRoman(allocator, i);
        defer allocator.free(roman);
        const back = try romanToInt(roman);
        try std.testing.expectEqual(i, back);
    }

    // 抽样测试更大的数字
    const samples = [_]u32{ 500, 999, 1000, 1999, 2024, 2500, 3999 };
    for (samples) |num| {
        const roman = try intToRoman(allocator, num);
        defer allocator.free(roman);
        const back = try romanToInt(roman);
        try std.testing.expectEqual(num, back);
    }
}

test "isValidRoman" {
    try std.testing.expect(isValidRoman("I"));
    try std.testing.expect(isValidRoman("IV"));
    try std.testing.expect(isValidRoman("MMXXIV"));
    try std.testing.expect(isValidRoman("MMMCMXCIX"));
    try std.testing.expect(!isValidRoman(""));
    try std.testing.expect(!isValidRoman("IIII"));
    try std.testing.expect(!isValidRoman("ABC"));
    try std.testing.expect(!isValidRoman("VV"));
}

test "romanAdd" {
    const allocator = std.testing.allocator;

    const result1 = try romanAdd(allocator, "X", "V");
    defer allocator.free(result1);
    try std.testing.expectEqualSlices(u8, "XV", result1);

    const result2 = try romanAdd(allocator, "IV", "VI");
    defer allocator.free(result2);
    try std.testing.expectEqualSlices(u8, "X", result2);

    const result3 = try romanAdd(allocator, "C", "C");
    defer allocator.free(result3);
    try std.testing.expectEqualSlices(u8, "CC", result3);
}

test "romanSubtract" {
    const allocator = std.testing.allocator;

    const result1 = try romanSubtract(allocator, "X", "V");
    defer allocator.free(result1);
    try std.testing.expectEqualSlices(u8, "V", result1);

    const result2 = try romanSubtract(allocator, "X", "I");
    defer allocator.free(result2);
    try std.testing.expectEqualSlices(u8, "IX", result2);

    const result3 = try romanSubtract(allocator, "C", "L");
    defer allocator.free(result3);
    try std.testing.expectEqualSlices(u8, "L", result3);
}

test "romanMultiply" {
    const allocator = std.testing.allocator;

    const result1 = try romanMultiply(allocator, "V", "II");
    defer allocator.free(result1);
    try std.testing.expectEqualSlices(u8, "X", result1);

    const result2 = try romanMultiply(allocator, "X", "X");
    defer allocator.free(result2);
    try std.testing.expectEqualSlices(u8, "C", result2);

    const result3 = try romanMultiply(allocator, "V", "V");
    defer allocator.free(result3);
    try std.testing.expectEqualSlices(u8, "XXV", result3);
}

test "romanDivide" {
    const allocator = std.testing.allocator;

    const result1 = try romanDivide(allocator, "X", "III");
    defer allocator.free(result1[0]);
    defer allocator.free(result1[1]);
    try std.testing.expectEqualSlices(u8, "III", result1[0]);
    try std.testing.expectEqualSlices(u8, "I", result1[1]);

    const result2 = try romanDivide(allocator, "X", "II");
    defer allocator.free(result2[0]);
    defer allocator.free(result2[1]);
    try std.testing.expectEqualSlices(u8, "V", result2[0]);
    try std.testing.expectEqualSlices(u8, "", result2[1]);

    // DivisionByZero is impossible to test with roman numerals since 0 cannot be represented
    // Empty input is caught before DivisionByZero check
    try std.testing.expectError(RomanError.EmptyInput, romanDivide(allocator, "X", ""));
}

test "romanCompare" {
    try std.testing.expectEqual(@as(i32, -1), try romanCompare("V", "X"));
    try std.testing.expectEqual(@as(i32, 0), try romanCompare("X", "X"));
    try std.testing.expectEqual(@as(i32, 1), try romanCompare("X", "V"));
    try std.testing.expectEqual(@as(i32, -1), try romanCompare("I", "M"));
    try std.testing.expectEqual(@as(i32, 1), try romanCompare("MMM", "I"));
}

test "getRomanInfo" {
    const allocator = std.testing.allocator;

    var info = try getRomanInfo(allocator, "MMXXIV");
    defer info.deinit();

    try std.testing.expectEqual(@as(u32, 2024), info.value);
    try std.testing.expect(info.valid);
    try std.testing.expectEqual(@as(usize, 6), info.length);
    if (info.components) |comp| {
        try std.testing.expectEqualSlices(u8, "MMXXIV", comp);
    }

    var invalid_info = try getRomanInfo(allocator, "ABC");
    defer invalid_info.deinit();
    try std.testing.expect(!invalid_info.valid);
}

test "findRomanRange" {
    const allocator = std.testing.allocator;

    const range = try findRomanRange(allocator, 1, 10);
    defer {
        for (range) |entry| {
            allocator.free(entry[1]);
        }
        allocator.free(range);
    }

    try std.testing.expectEqual(@as(usize, 10), range.len);
    try std.testing.expectEqual(@as(u32, 1), range[0][0]);
    try std.testing.expectEqualSlices(u8, "I", range[0][1]);
    try std.testing.expectEqual(@as(u32, 10), range[9][0]);
    try std.testing.expectEqualSlices(u8, "X", range[9][1]);
}

test "historical years" {
    const allocator = std.testing.allocator;

    const years = [_]struct { num: u32, roman: []const u8 }{
        .{ .num = 1776, .roman = "MDCCLXXVI" }, // 美国独立
        .{ .num = 1789, .roman = "MDCCLXXXIX" }, // 法国大革命
        .{ .num = 1914, .roman = "MCMXIV" }, // 一战开始
        .{ .num = 1945, .roman = "MCMXLV" }, // 二战结束
        .{ .num = 1969, .roman = "MCMLXIX" }, // 登月
    };

    for (years) |year| {
        const result = try intToRoman(allocator, year.num);
        defer allocator.free(result);
        try std.testing.expectEqualSlices(u8, year.roman, result);

        const back = try romanToInt(year.roman);
        try std.testing.expectEqual(year.num, back);
    }
}

test "all valid roman numerals" {
    const allocator = std.testing.allocator;

    // 测试所有 1-3999 的转换
    var i: u32 = 1;
    while (i <= 3999) : (i += 1) {
        const roman = try intToRoman(allocator, i);
        const back = try romanToInt(roman);
        allocator.free(roman);
        try std.testing.expectEqual(i, back);
    }
}

test "subtraction rule validation" {
    // 测试减法规则的验证
    try std.testing.expect(isValidRoman("IV")); // I = 1, V = 5, 5-1 = 4
    try std.testing.expect(isValidRoman("IX")); // I = 1, X = 10, 10-1 = 9
    try std.testing.expect(isValidRoman("XL")); // X = 10, L = 50, 50-10 = 40
    try std.testing.expect(isValidRoman("XC")); // X = 10, C = 100, 100-10 = 90
    try std.testing.expect(isValidRoman("CD")); // C = 100, D = 500, 500-100 = 400
    try std.testing.expect(isValidRoman("CM")); // C = 100, M = 1000, 1000-100 = 900

    // 无效的减法组合
    try std.testing.expect(!isValidRoman("IL")); // I 不能减 L
    try std.testing.expect(!isValidRoman("IC")); // I 不能减 C
    try std.testing.expect(!isValidRoman("ID")); // I 不能减 D
    try std.testing.expect(!isValidRoman("IM")); // I 不能减 M
    try std.testing.expect(!isValidRoman("XD")); // X 不能减 D
    try std.testing.expect(!isValidRoman("XM")); // X 不能减 M
}