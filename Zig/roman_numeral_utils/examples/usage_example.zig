const std = @import("std");
const roman = @import("../mod.zig");

/// 演示罗马数字工具的各种用法
pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("\n", .{});
    std.debug.print("=" ++ "=" ** 50 ++ "\n", .{});
    std.debug.print("   Roman Numeral Utils - 使用示例\n", .{});
    std.debug.print("=" ++ "=" ** 50 ++ "\n\n", .{});

    // ==================== 1. 基本转换 ====================
    std.debug.print("【1. 基本转换】\n\n", .{});

    std.debug.print("  整数转罗马数字:\n", .{});
    const numbers = [_]u32{ 1, 4, 9, 49, 99, 2024, 3999 };
    for (numbers) |num| {
        const r = try roman.intToRoman(allocator, num);
        defer allocator.free(r);
        std.debug.print("    {} -> {s}\n", .{ num, r });
    }

    std.debug.print("\n  罗马数字转整数:\n", .{});
    const romans = [_][]const u8{ "I", "IV", "IX", "XLIX", "XCIX", "MMXXIV", "MMMCMXCIX" };
    for (romans) |r| {
        const v = try roman.romanToInt(r);
        std.debug.print("    {s} -> {}\n", .{ r, v });
    }

    // ==================== 2. 验证功能 ====================
    std.debug.print("\n【2. 验证功能】\n\n", .{});

    const test_romans = [_][]const u8{ "IV", "IIII", "ABC", "MMXXIV", "MCMLXXXIV" };
    std.debug.print("  验证结果:\n", .{});
    for (test_romans) |r| {
        const valid = roman.isValidRoman(r);
        const status = if (valid) "有效 ✓" else "无效 ✗";
        std.debug.print("    '{s}' -> {s}\n", .{ r, status });
    }

    // ==================== 3. 算术运算 ====================
    std.debug.print("\n【3. 算术运算】\n\n", .{});

    // 加法
    std.debug.print("  加法:\n", .{});
    const add1 = try roman.romanAdd(allocator, "X", "V");
    defer allocator.free(add1);
    std.debug.print("    X + V = {s}\n", .{add1});

    const add2 = try roman.romanAdd(allocator, "IV", "VI");
    defer allocator.free(add2);
    std.debug.print("    IV + VI = {s}\n", .{add2});

    const add3 = try roman.romanAdd(allocator, "C", "C");
    defer allocator.free(add3);
    std.debug.print("    C + C = {s}\n", .{add3});

    // 减法
    std.debug.print("\n  减法:\n", .{});
    const sub1 = try roman.romanSubtract(allocator, "X", "V");
    defer allocator.free(sub1);
    std.debug.print("    X - V = {s}\n", .{sub1});

    const sub2 = try roman.romanSubtract(allocator, "X", "I");
    defer allocator.free(sub2);
    std.debug.print("    X - I = {s}\n", .{sub2});

    // 乘法
    std.debug.print("\n  乘法:\n", .{});
    const mul1 = try roman.romanMultiply(allocator, "V", "II");
    defer allocator.free(mul1);
    std.debug.print("    V × II = {s}\n", .{mul1});

    const mul2 = try roman.romanMultiply(allocator, "X", "X");
    defer allocator.free(mul2);
    std.debug.print("    X × X = {s}\n", .{mul2});

    // 除法
    std.debug.print("\n  除法:\n", .{});
    const div1 = try roman.romanDivide(allocator, "X", "III");
    defer allocator.free(div1[0]);
    defer allocator.free(div1[1]);
    std.debug.print("    X ÷ III = {s} 余 {s}\n", .{ div1[0], if (div1[1].len > 0) div1[1] else "0" });

    const div2 = try roman.romanDivide(allocator, "X", "II");
    defer allocator.free(div2[0]);
    defer allocator.free(div2[1]);
    std.debug.print("    X ÷ II = {s} 余 {s}\n", .{ div2[0], if (div2[1].len > 0) div2[1] else "0" });

    // ==================== 4. 比较功能 ====================
    std.debug.print("\n【4. 比较功能】\n\n", .{});

    const pairs = [_]struct { r1: []const u8, r2: []const u8 }{
        .{ .r1 = "V", .r2 = "X" },
        .{ .r1 = "X", .r2 = "X" },
        .{ .r1 = "X", .r2 = "V" },
        .{ .r1 = "I", .r2 = "M" },
    };

    std.debug.print("  比较结果:\n", .{});
    for (pairs) |pair| {
        const cmp = try roman.romanCompare(pair.r1, pair.r2);
        const symbol = if (cmp < 0) "<" else if (cmp > 0) ">" else "=";
        std.debug.print("    {s} {s} {s}\n", .{ pair.r1, symbol, pair.r2 });
    }

    // ==================== 5. 历史年份 ====================
    std.debug.print("\n【5. 历史年份】\n\n", .{});

    const years = [_]struct { year: u32, event: []const u8 }{
        .{ .year = 753, .event = "罗马建城" },
        .{ .year = 1776, .event = "美国独立" },
        .{ .year = 1789, .event = "法国大革命" },
        .{ .year = 1914, .event = "一战开始" },
        .{ .year = 1945, .event = "二战结束" },
        .{ .year = 1969, .event = "人类登月" },
        .{ .year = 2024, .event = "当前年份" },
    };

    std.debug.print("  历史年份转换:\n", .{});
    for (years) |y| {
        const r = try roman.intToRoman(allocator, y.year);
        defer allocator.free(r);
        std.debug.print("    {} ({s}) = {s}\n", .{ y.year, y.event, r });
    }

    // ==================== 6. 信息获取 ====================
    std.debug.print("\n【6. 信息获取】\n\n", .{});

    var info = try roman.getRomanInfo(allocator, "MMXXIV");
    defer info.deinit();

    std.debug.print("  'MMXXIV' 详细信息:\n", .{});
    std.debug.print("    原始输入: {s}\n", .{info.original});
    std.debug.print("    数值: {}\n", .{info.value});
    std.debug.print("    有效: {}\n", .{info.valid});
    std.debug.print("    长度: {}\n", .{info.length});
    if (info.components) |comp| {
        std.debug.print("    规范化组件: {s}\n", .{comp});
    }

    // ==================== 7. 范围生成 ====================
    std.debug.print("\n【7. 范围生成】\n\n", .{});

    std.debug.print("  1-10 的罗马数字:\n", .{});
    const range = try roman.findRomanRange(allocator, 1, 10);
    defer {
        for (range) |entry| {
            allocator.free(entry[1]);
        }
        allocator.free(range);
    }

    std.debug.print("    ", .{});
    for (range, 0..) |entry, i| {
        std.debug.print("{}={s}", .{ entry[0], entry[1] });
        if (i < range.len - 1) std.debug.print(", ", .{});
    }
    std.debug.print("\n", .{});

    // ==================== 8. 大小写不敏感 ====================
    std.debug.print("\n【8. 大小写不敏感】\n\n", .{});

    const cases = [_][]const u8{ "mmxxiv", "MMXXIV", "MmXxIv" };
    std.debug.print("  不同大小写输入:\n", .{});
    for (cases) |c| {
        const v = try roman.romanToInt(c);
        std.debug.print("    '{s}' -> {}\n", .{ c, v });
    }

    // ==================== 9. 错误处理 ====================
    std.debug.print("\n【9. 错误处理】\n\n", .{});

    std.debug.print("  边界值测试:\n", .{});

    // 超出范围
    const under = roman.intToRoman(allocator, 0);
    if (under) |_| {
        std.debug.print("    0: 不应成功\n", .{});
    } else |err| {
        std.debug.print("    0: 正确返回错误 - {}\n", .{err});
    }

    const over = roman.intToRoman(allocator, 4000);
    if (over) |_| {
        std.debug.print("    4000: 不应成功\n", .{});
    } else |err| {
        std.debug.print("    4000: 正确返回错误 - {}\n", .{err});
    }

    // 无效罗马数字
    std.debug.print("\n  无效输入测试:\n", .{});
    const invalid_inputs = [_][]const u8{ "", "IIII", "VV", "ABC", "IM" };
    for (invalid_inputs) |input| {
        const result = roman.romanToInt(input);
        if (result) |_| {
            std.debug.print("    '{s}': 不应成功\n", .{input});
        } else |err| {
            std.debug.print("    '{s}': 正确返回错误 - {}\n", .{ input, err });
        }
    }

    // ==================== 10. 实用示例 ====================
    std.debug.print("\n【10. 实用示例】\n\n", .{});

    std.debug.print("  时钟数字 (1-12):\n", .{});
    const clock_range = try roman.findRomanRange(allocator, 1, 12);
    defer {
        for (clock_range) |entry| {
            allocator.free(entry[1]);
        }
        allocator.free(clock_range);
    }

    std.debug.print("    ", .{});
    for (clock_range, 0..) |entry, i| {
        std.debug.print("{s}", .{entry[1]});
        if (i < clock_range.len - 1) std.debug.print(", ", .{});
    }
    std.debug.print("\n", .{});

    std.debug.print("\n  书籍章节编号示例:\n", .{});
    const chapters = [_]u32{ 1, 5, 10, 15, 20 };
    for (chapters) |ch| {
        const ch_roman = try roman.intToRoman(allocator, ch);
        defer allocator.free(ch_roman);
        std.debug.print("    第{}章 = 第{s}章\n", .{ ch, ch_roman });
    }

    std.debug.print("\n" ++ "=" ** 52 ++ "\n", .{});
    std.debug.print("  示例演示完成！\n", .{});
    std.debug.print("=" ++ "=" ** 50 ++ "\n\n", .{});
}