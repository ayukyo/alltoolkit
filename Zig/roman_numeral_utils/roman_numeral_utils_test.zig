const std = @import("std");
const roman = @import("mod.zig");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("\n", .{});
    std.debug.print("=" ++ "=" ** 60 ++ "\n", .{});
    std.debug.print("     Roman Numeral Utils - 罗马数字工具测试套件\n", .{});
    std.debug.print("=" ++ "=" ** 60 ++ "\n\n", .{});

    var passed: usize = 0;
    var failed: usize = 0;

    // ==================== 基本转换测试 ====================
    std.debug.print("【基本转换测试】\n", .{});
    std.debug.print("-" ++ "-" ** 60 ++ "\n", .{});

    const basic_tests = [_]struct { num: u32, expected: []const u8 }{
        .{ .num = 1, .expected = "I" },
        .{ .num = 2, .expected = "II" },
        .{ .num = 3, .expected = "III" },
        .{ .num = 4, .expected = "IV" },
        .{ .num = 5, .expected = "V" },
        .{ .num = 6, .expected = "VI" },
        .{ .num = 7, .expected = "VII" },
        .{ .num = 8, .expected = "VIII" },
        .{ .num = 9, .expected = "IX" },
        .{ .num = 10, .expected = "X" },
        .{ .num = 14, .expected = "XIV" },
        .{ .num = 19, .expected = "XIX" },
        .{ .num = 40, .expected = "XL" },
        .{ .num = 44, .expected = "XLIV" },
        .{ .num = 49, .expected = "XLIX" },
        .{ .num = 50, .expected = "L" },
        .{ .num = 90, .expected = "XC" },
        .{ .num = 99, .expected = "XCIX" },
        .{ .num = 100, .expected = "C" },
        .{ .num = 400, .expected = "CD" },
        .{ .num = 500, .expected = "D" },
        .{ .num = 900, .expected = "CM" },
        .{ .num = 1000, .expected = "M" },
        .{ .num = 1984, .expected = "MCMLXXXIV" },
        .{ .num = 1999, .expected = "MCMXCIX" },
        .{ .num = 2000, .expected = "MM" },
        .{ .num = 2024, .expected = "MMXXIV" },
        .{ .num = 2025, .expected = "MMXXV" },
        .{ .num = 3000, .expected = "MMM" },
        .{ .num = 3999, .expected = "MMMCMXCIX" },
    };

    for (basic_tests) |test_case| {
        const result = roman.intToRoman(allocator, test_case.num) catch |err| {
            std.debug.print("  ✗ {} -> 错误: {}\n", .{ test_case.num, err });
            failed += 1;
            continue;
        };
        defer allocator.free(result);

        if (std.mem.eql(u8, result, test_case.expected)) {
            std.debug.print("  ✓ {} -> {s}\n", .{ test_case.num, result });
            passed += 1;
        } else {
            std.debug.print("  ✗ {} -> {s} (期望: {s})\n", .{ test_case.num, result, test_case.expected });
            failed += 1;
        }
    }

    // ==================== 反向转换测试 ====================
    std.debug.print("\n【反向转换测试】\n", .{});
    std.debug.print("-" ++ "-" ** 60 ++ "\n", .{});

    const reverse_tests = [_]struct { roman: []const u8, expected: u32 }{
        .{ .roman = "I", .expected = 1 },
        .{ .roman = "II", .expected = 2 },
        .{ .roman = "III", .expected = 3 },
        .{ .roman = "IV", .expected = 4 },
        .{ .roman = "V", .expected = 5 },
        .{ .roman = "VI", .expected = 6 },
        .{ .roman = "IX", .expected = 9 },
        .{ .roman = "X", .expected = 10 },
        .{ .roman = "XIV", .expected = 14 },
        .{ .roman = "XIX", .expected = 19 },
        .{ .roman = "XL", .expected = 40 },
        .{ .roman = "XLIV", .expected = 44 },
        .{ .roman = "XLIX", .expected = 49 },
        .{ .roman = "L", .expected = 50 },
        .{ .roman = "XC", .expected = 90 },
        .{ .roman = "XCIX", .expected = 99 },
        .{ .roman = "C", .expected = 100 },
        .{ .roman = "CD", .expected = 400 },
        .{ .roman = "D", .expected = 500 },
        .{ .roman = "CM", .expected = 900 },
        .{ .roman = "M", .expected = 1000 },
        .{ .roman = "MCMLXXXIV", .expected = 1984 },
        .{ .roman = "MCMXCIX", .expected = 1999 },
        .{ .roman = "MM", .expected = 2000 },
        .{ .roman = "MMXXIV", .expected = 2024 },
        .{ .roman = "MMMCMXCIX", .expected = 3999 },
    };

    for (reverse_tests) |test_case| {
        const result = roman.romanToInt(test_case.roman) catch |err| {
            std.debug.print("  ✗ {s} -> 错误: {}\n", .{ test_case.roman, err });
            failed += 1;
            continue;
        };

        if (result == test_case.expected) {
            std.debug.print("  ✓ {s} -> {}\n", .{ test_case.roman, result });
            passed += 1;
        } else {
            std.debug.print("  ✗ {s} -> {} (期望: {})\n", .{ test_case.roman, result, test_case.expected });
            failed += 1;
        }
    }

    // ==================== 大小写不敏感测试 ====================
    std.debug.print("\n【大小写不敏感测试】\n", .{});
    std.debug.print("-" ++ "-" ** 60 ++ "\n", .{});

    const case_tests = [_]struct { roman: []const u8, expected: u32 }{
        .{ .roman = "i", .expected = 1 },
        .{ .roman = "iv", .expected = 4 },
        .{ .roman = "x", .expected = 10 },
        .{ .roman = "MmXxIv", .expected = 2024 },
        .{ .roman = "mmxxiv", .expected = 2024 },
    };

    for (case_tests) |test_case| {
        const result = roman.romanToInt(test_case.roman) catch |err| {
            std.debug.print("  ✗ {s} -> 错误: {}\n", .{ test_case.roman, err });
            failed += 1;
            continue;
        };

        if (result == test_case.expected) {
            std.debug.print("  ✓ {s} -> {}\n", .{ test_case.roman, result });
            passed += 1;
        } else {
            std.debug.print("  ✗ {s} -> {} (期望: {})\n", .{ test_case.roman, result, test_case.expected });
            failed += 1;
        }
    }

    // ==================== 无效输入测试 ====================
    std.debug.print("\n【无效输入测试】\n", .{});
    std.debug.print("-" ++ "-" ** 60 ++ "\n", .{});

    const invalid_tests = [_]struct { roman: []const u8, desc: []const u8 }{
        .{ .roman = "", .desc = "空字符串" },
        .{ .roman = "ABC", .desc = "无效字符" },
        .{ .roman = "IIII", .desc = "I重复超过3次" },
        .{ .roman = "VV", .desc = "V重复" },
        .{ .roman = "LL", .desc = "L重复" },
        .{ .roman = "DD", .desc = "D重复" },
        .{ .roman = "IL", .desc = "I不能减L" },
        .{ .roman = "IC", .desc = "I不能减C" },
        .{ .roman = "ID", .desc = "I不能减D" },
        .{ .roman = "IM", .desc = "I不能减M" },
        .{ .roman = "XD", .desc = "X不能减D" },
        .{ .roman = "XM", .desc = "X不能减M" },
    };

    for (invalid_tests) |test_case| {
        const result = roman.romanToInt(test_case.roman);
        if (result) |_| {
            std.debug.print("  ✗ {s} ({s}) - 应该失败但成功了\n", .{ test_case.roman, test_case.desc });
            failed += 1;
        } else |_| {
            std.debug.print("  ✓ {s} ({s}) - 正确拒绝\n", .{ test_case.roman, test_case.desc });
            passed += 1;
        }
    }

    // ==================== 验证函数测试 ====================
    std.debug.print("\n【验证函数测试】\n", .{});
    std.debug.print("-" ++ "-" ** 60 ++ "\n", .{});

    const valid_romans = [_][]const u8{ "I", "IV", "V", "IX", "X", "XL", "L", "XC", "C", "CD", "D", "CM", "M", "MMXXIV", "MMMCMXCIX" };
    const invalid_romans = [_][]const u8{ "", "IIII", "VV", "ABC", "IL", "IC", "IM", "XM" };

    for (valid_romans) |r| {
        if (roman.isValidRoman(r)) {
            std.debug.print("  ✓ {s} - 有效\n", .{r});
            passed += 1;
        } else {
            std.debug.print("  ✗ {s} - 应该有效\n", .{r});
            failed += 1;
        }
    }

    for (invalid_romans) |r| {
        if (!roman.isValidRoman(r)) {
            std.debug.print("  ✓ {s} - 正确识别为无效\n", .{r});
            passed += 1;
        } else {
            std.debug.print("  ✗ {s} - 应该无效\n", .{r});
            failed += 1;
        }
    }

    // ==================== 算术运算测试 ====================
    std.debug.print("\n【算术运算测试】\n", .{});
    std.debug.print("-" ++ "-" ** 60 ++ "\n", .{});

    // 加法测试
    std.debug.print("  加法:\n", .{});
    const add_tests = [_]struct { r1: []const u8, r2: []const u8, expected: []const u8 }{
        .{ .r1 = "I", .r2 = "I", .expected = "II" },
        .{ .r1 = "IV", .r2 = "I", .expected = "V" },
        .{ .r1 = "X", .r2 = "V", .expected = "XV" },
        .{ .r1 = "IV", .r2 = "VI", .expected = "X" },
        .{ .r1 = "C", .r2 = "C", .expected = "CC" },
        .{ .r1 = "M", .r2 = "M", .expected = "MM" },
    };

    for (add_tests) |test_case| {
        const result = roman.romanAdd(allocator, test_case.r1, test_case.r2) catch |err| {
            std.debug.print("    ✗ {s} + {s} -> 错误: {}\n", .{ test_case.r1, test_case.r2, err });
            failed += 1;
            continue;
        };
        defer allocator.free(result);

        if (std.mem.eql(u8, result, test_case.expected)) {
            std.debug.print("    ✓ {s} + {s} = {s}\n", .{ test_case.r1, test_case.r2, result });
            passed += 1;
        } else {
            std.debug.print("    ✗ {s} + {s} = {s} (期望: {s})\n", .{ test_case.r1, test_case.r2, result, test_case.expected });
            failed += 1;
        }
    }

    // 减法测试
    std.debug.print("  减法:\n", .{});
    const sub_tests = [_]struct { r1: []const u8, r2: []const u8, expected: []const u8 }{
        .{ .r1 = "II", .r2 = "I", .expected = "I" },
        .{ .r1 = "V", .r2 = "I", .expected = "IV" },
        .{ .r1 = "X", .r2 = "I", .expected = "IX" },
        .{ .r1 = "X", .r2 = "V", .expected = "V" },
        .{ .r1 = "C", .r2 = "L", .expected = "L" },
    };

    for (sub_tests) |test_case| {
        const result = roman.romanSubtract(allocator, test_case.r1, test_case.r2) catch |err| {
            std.debug.print("    ✗ {s} - {s} -> 错误: {}\n", .{ test_case.r1, test_case.r2, err });
            failed += 1;
            continue;
        };
        defer allocator.free(result);

        if (std.mem.eql(u8, result, test_case.expected)) {
            std.debug.print("    ✓ {s} - {s} = {s}\n", .{ test_case.r1, test_case.r2, result });
            passed += 1;
        } else {
            std.debug.print("    ✗ {s} - {s} = {s} (期望: {s})\n", .{ test_case.r1, test_case.r2, result, test_case.expected });
            failed += 1;
        }
    }

    // 乘法测试
    std.debug.print("  乘法:\n", .{});
    const mul_tests = [_]struct { r1: []const u8, r2: []const u8, expected: []const u8 }{
        .{ .r1 = "I", .r2 = "I", .expected = "I" },
        .{ .r1 = "V", .r2 = "II", .expected = "X" },
        .{ .r1 = "X", .r2 = "X", .expected = "C" },
        .{ .r1 = "V", .r2 = "V", .expected = "XXV" },
        .{ .r1 = "II", .r2 = "II", .expected = "IV" },
    };

    for (mul_tests) |test_case| {
        const result = roman.romanMultiply(allocator, test_case.r1, test_case.r2) catch |err| {
            std.debug.print("    ✗ {s} × {s} -> 错误: {}\n", .{ test_case.r1, test_case.r2, err });
            failed += 1;
            continue;
        };
        defer allocator.free(result);

        if (std.mem.eql(u8, result, test_case.expected)) {
            std.debug.print("    ✓ {s} × {s} = {s}\n", .{ test_case.r1, test_case.r2, result });
            passed += 1;
        } else {
            std.debug.print("    ✗ {s} × {s} = {s} (期望: {s})\n", .{ test_case.r1, test_case.r2, result, test_case.expected });
            failed += 1;
        }
    }

    // 除法测试
    std.debug.print("  除法:\n", .{});
    const div_tests = [_]struct { r1: []const u8, r2: []const u8, exp_quotient: []const u8, exp_remainder: []const u8 }{
        .{ .r1 = "X", .r2 = "II", .exp_quotient = "V", .exp_remainder = "" },
        .{ .r1 = "X", .r2 = "III", .exp_quotient = "III", .exp_remainder = "I" },
        .{ .r1 = "C", .r2 = "X", .exp_quotient = "X", .exp_remainder = "" },
        .{ .r1 = "XX", .r2 = "III", .exp_quotient = "VI", .exp_remainder = "II" },
    };

    for (div_tests) |test_case| {
        const result = roman.romanDivide(allocator, test_case.r1, test_case.r2) catch |err| {
            std.debug.print("    ✗ {s} ÷ {s} -> 错误: {}\n", .{ test_case.r1, test_case.r2, err });
            failed += 1;
            continue;
        };
        defer allocator.free(result[0]);
        defer allocator.free(result[1]);

        if (std.mem.eql(u8, result[0], test_case.exp_quotient) and std.mem.eql(u8, result[1], test_case.exp_remainder)) {
            std.debug.print("    ✓ {s} ÷ {s} = {s} 余 {s}\n", .{ test_case.r1, test_case.r2, result[0], if (result[1].len > 0) result[1] else "0" });
            passed += 1;
        } else {
            std.debug.print("    ✗ {s} ÷ {s} = {s} 余 {s} (期望: {s} 余 {s})\n", .{ test_case.r1, test_case.r2, result[0], result[1], test_case.exp_quotient, test_case.exp_remainder });
            failed += 1;
        }
    }

    // ==================== 比较测试 ====================
    std.debug.print("\n【比较测试】\n", .{});
    std.debug.print("-" ++ "-" ** 60 ++ "\n", .{});

    const cmp_tests = [_]struct { r1: []const u8, r2: []const u8, expected: i32 }{
        .{ .r1 = "I", .r2 = "V", .expected = -1 },
        .{ .r1 = "V", .r2 = "I", .expected = 1 },
        .{ .r1 = "X", .r2 = "X", .expected = 0 },
        .{ .r1 = "I", .r2 = "M", .expected = -1 },
        .{ .r1 = "MMM", .r2 = "I", .expected = 1 },
        .{ .r1 = "IV", .r2 = "V", .expected = -1 },
    };

    for (cmp_tests) |test_case| {
        const result = roman.romanCompare(test_case.r1, test_case.r2) catch |err| {
            std.debug.print("  ✗ 比较 {s} 和 {s} -> 错误: {}\n", .{ test_case.r1, test_case.r2, err });
            failed += 1;
            continue;
        };

        const symbol = if (result < 0) "<" else if (result > 0) ">" else "=";
        if (result == test_case.expected) {
            std.debug.print("  ✓ {s} {s} {s}\n", .{ test_case.r1, symbol, test_case.r2 });
            passed += 1;
        } else {
            std.debug.print("  ✗ {s} {s} {s} (期望不同结果)\n", .{ test_case.r1, symbol, test_case.r2 });
            failed += 1;
        }
    }

    // ==================== 历史年份测试 ====================
    std.debug.print("\n【历史年份测试】\n", .{});
    std.debug.print("-" ++ "-" ** 60 ++ "\n", .{});

    const years = [_]struct { year: u32, roman: []const u8, event: []const u8 }{
        .{ .year = 753, .roman = "DCCLIII", .event = "罗马建城" },
        .{ .year = 1066, .roman = "MLXVI", .event = "诺曼征服" },
        .{ .year = 1215, .roman = "MCCXV", .event = "大宪章" },
        .{ .year = 1492, .roman = "MCDXCII", .event = "哥伦布发现新大陆" },
        .{ .year = 1776, .roman = "MDCCLXXVI", .event = "美国独立" },
        .{ .year = 1789, .roman = "MDCCLXXXIX", .event = "法国大革命" },
        .{ .year = 1914, .roman = "MCMXIV", .event = "一战开始" },
        .{ .year = 1945, .roman = "MCMXLV", .event = "二战结束" },
        .{ .year = 1969, .roman = "MCMLXIX", .event = "登月" },
    };

    for (years) |y| {
        const result = roman.intToRoman(allocator, y.year) catch |err| {
            std.debug.print("  ✗ {} -> 错误: {}\n", .{ y.year, err });
            failed += 1;
            continue;
        };
        defer allocator.free(result);

        if (std.mem.eql(u8, result, y.roman)) {
            std.debug.print("  ✓ {} = {s} ({s})\n", .{ y.year, result, y.event });
            passed += 1;
        } else {
            std.debug.print("  ✗ {} = {s} (期望: {s}, {s})\n", .{ y.year, result, y.roman, y.event });
            failed += 1;
        }
    }

    // ==================== 往返转换测试 ====================
    std.debug.print("\n【往返转换测试 (1-100)】\n", .{});
    std.debug.print("-" ++ "-" ** 60 ++ "\n", .{});

    var i: u32 = 1;
    var round_passed: usize = 0;
    var round_failed: usize = 0;
    while (i <= 100) : (i += 1) {
        const r = roman.intToRoman(allocator, i) catch {
            round_failed += 1;
            continue;
        };
        defer allocator.free(r);

        const back = roman.romanToInt(r) catch {
            round_failed += 1;
            continue;
        };

        if (back == i) {
            round_passed += 1;
        } else {
            round_failed += 1;
        }
    }

    std.debug.print("  通过: {}/100\n", .{round_passed});
    if (round_failed == 0) {
        std.debug.print("  ✓ 全部往返转换正确\n", .{});
        passed += 1;
    } else {
        std.debug.print("  ✗ {} 个往返转换失败\n", .{round_failed});
        failed += 1;
    }

    // ==================== 边界值测试 ====================
    std.debug.print("\n【边界值测试】\n", .{});
    std.debug.print("-" ++ "-" ** 60 ++ "\n", .{});

    // 最小值
    const min_result = roman.intToRoman(allocator, 1) catch |err| {
        std.debug.print("  ✗ 最小值测试失败: {}\n", .{err});
        failed += 1;
        return;
    };
    defer allocator.free(min_result);
    if (std.mem.eql(u8, min_result, "I")) {
        std.debug.print("  ✓ 最小值: 1 = I\n", .{});
        passed += 1;
    } else {
        std.debug.print("  ✗ 最小值: 1 = {s} (期望: I)\n", .{min_result});
        failed += 1;
    }

    // 最大值
    const max_result = roman.intToRoman(allocator, 3999) catch |err| {
        std.debug.print("  ✗ 最大值测试失败: {}\n", .{err});
        failed += 1;
        return;
    };
    defer allocator.free(max_result);
    if (std.mem.eql(u8, max_result, "MMMCMXCIX")) {
        std.debug.print("  ✓ 最大值: 3999 = MMMCMXCIX\n", .{});
        passed += 1;
    } else {
        std.debug.print("  ✗ 最大值: 3999 = {s} (期望: MMMCMXCIX)\n", .{max_result});
        failed += 1;
    }

    // 超出范围
    const under_result = roman.intToRoman(allocator, 0);
    if (under_result) |_| {
        std.debug.print("  ✗ 0 应该返回错误\n", .{});
        failed += 1;
    } else |_| {
        std.debug.print("  ✓ 0 正确返回越界错误\n", .{});
        passed += 1;
    }

    const over_result = roman.intToRoman(allocator, 4000);
    if (over_result) |_| {
        std.debug.print("  ✗ 4000 应该返回错误\n", .{});
        failed += 1;
    } else |_| {
        std.debug.print("  ✓ 4000 正确返回越界错误\n", .{});
        passed += 1;
    }

    // ==================== 信息获取测试 ====================
    std.debug.print("\n【信息获取测试】\n", .{});
    std.debug.print("-" ++ "-" ** 60 ++ "\n", .{});

    var info = roman.getRomanInfo(allocator, "MMXXIV") catch |err| {
        std.debug.print("  ✗ 获取信息失败: {}\n", .{err});
        failed += 1;
        return;
    };
    defer info.deinit();

    if (info.valid and info.value == 2024 and info.length == 6) {
        std.debug.print("  ✓ MMXXIV: 值={}, 长度={}, 有效={}\n", .{ info.value, info.length, info.valid });
        passed += 1;
    } else {
        std.debug.print("  ✗ 信息不正确\n", .{});
        failed += 1;
    }

    // ==================== 范围生成测试 ====================
    std.debug.print("\n【范围生成测试 (1-10)】\n", .{});
    std.debug.print("-" ++ "-" ** 60 ++ "\n", .{});

    const range = roman.findRomanRange(allocator, 1, 10) catch |err| {
        std.debug.print("  ✗ 范围生成失败: {}\n", .{err});
        failed += 1;
        return;
    };

    std.debug.print("  ", .{});
    for (range, 0..) |entry, idx| {
        defer allocator.free(entry[1]);
        std.debug.print("{}={s}", .{ entry[0], entry[1] });
        if (idx < range.len - 1) std.debug.print(", ", .{});
    }
    std.debug.print("\n", .{});
    allocator.free(range);

    std.debug.print("  ✓ 范围生成成功\n", .{});
    passed += 1;

    // ==================== 测试总结 ====================
    std.debug.print("\n" ++ "=" ** 62 ++ "\n", .{});
    std.debug.print("  测试结果: {} 通过, {} 失败\n", .{ passed, failed });
    std.debug.print("=" ++ "=" ** 60 ++ "\n\n", .{});

    if (failed == 0) {
        std.debug.print("  🎉 所有测试通过！\n\n", .{});
    } else {
        std.debug.print("  ⚠️  部分测试失败\n\n", .{});
    }
}