#!/usr/bin/env lua
---
-- Binary Utilities Test Suite
-- 二进制工具函数测试套件
--
-- 覆盖场景:
-- - 验证函数 (is_valid_binary, is_valid_hex, is_valid_octal)
-- - 进制转换 (binary_to_decimal, decimal_to_binary, binary_to_hex, etc.)
-- - 字符串操作 (strip_leading_zeros, pad_binary, reverse_binary, etc.)
-- - 位运算 (AND, OR, XOR, NOT, shifts, rotates)
-- - 算术运算 (add, sub, mul, div, mod)
-- - 统计计算 (count_bits, hamming_weight, hamming_distance)
-- - 模式匹配 (find_first_one, find_pattern, etc.)
-- - 特殊功能 (is_even, is_odd, is_power_of_two)
-- - 字节操作 (to_byte_array, string_to_binary, etc.)
--
-- Author: AllToolkit
-- Version: 1.0.0

local path = arg and arg[0] and arg[0]:match("(.*/)") or ""
local mod_path = path .. "mod.lua"

-- 加载模块
local BinaryUtils = dofile(mod_path)

-- 测试统计
local tests_run = 0
local tests_passed = 0
local tests_failed = 0
local failures = {}

--- 断言函数
local function assert_eq(actual, expected, message)
    tests_run = tests_run + 1
    if actual == expected then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or ("Expected %s, got %s"):format(tostring(expected), tostring(actual))
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 断言数值相等
local function assert_num_eq(actual, expected, message)
    tests_run = tests_run + 1
    if actual == expected then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or ("Expected %s, got %s"):format(tostring(expected), tostring(actual))
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 断言真值
local function assert_true(condition, message)
    tests_run = tests_run + 1
    if condition then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or "Expected true"
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 断言假值
local function assert_false(condition, message)
    tests_run = tests_run + 1
    if not condition then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or "Expected false"
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 断言nil值
local function assert_nil(value, message)
    tests_run = tests_run + 1
    if value == nil then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or ("Expected nil, got %s"):format(tostring(value))
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 断言非nil值
local function assert_not_nil(value, message)
    tests_run = tests_run + 1
    if value ~= nil then
        tests_passed = tests_passed + 1
        return true
    else
        tests_failed = tests_failed + 1
        local msg = message or "Expected non-nil value"
        table.insert(failures, msg)
        print("  ❌ FAIL: " .. msg)
        return false
    end
end

--- 打印测试组标题
local function test_group(name)
    print("\n📋 " .. name)
    print(string.rep("-", 50))
end

-------------------------------------------------------------------------------
-- 测试：验证函数
-------------------------------------------------------------------------------
test_group("验证函数 (Validation)")

assert_true(BinaryUtils.is_valid_binary("0"), "is_valid_binary('0')")
assert_true(BinaryUtils.is_valid_binary("1"), "is_valid_binary('1')")
assert_true(BinaryUtils.is_valid_binary("101"), "is_valid_binary('101')")
assert_true(BinaryUtils.is_valid_binary("11111111"), "is_valid_binary('11111111')")
assert_false(BinaryUtils.is_valid_binary(""), "is_valid_binary('')")
assert_false(BinaryUtils.is_valid_binary("2"), "is_valid_binary('2')")
assert_false(BinaryUtils.is_valid_binary("102"), "is_valid_binary('102')")
assert_false(BinaryUtils.is_valid_binary("abc"), "is_valid_binary('abc')")
assert_false(BinaryUtils.is_valid_binary(nil), "is_valid_binary(nil)")

assert_true(BinaryUtils.is_valid_hex("0"), "is_valid_hex('0')")
assert_true(BinaryUtils.is_valid_hex("F"), "is_valid_hex('F')")
assert_true(BinaryUtils.is_valid_hex("FF"), "is_valid_hex('FF')")
assert_true(BinaryUtils.is_valid_hex("a1b2c3"), "is_valid_hex('a1b2c3')")
assert_false(BinaryUtils.is_valid_hex("GH"), "is_valid_hex('GH')")
assert_false(BinaryUtils.is_valid_hex(nil), "is_valid_hex(nil)")

assert_true(BinaryUtils.is_valid_octal("0"), "is_valid_octal('0')")
assert_true(BinaryUtils.is_valid_octal("7"), "is_valid_octal('7')")
assert_true(BinaryUtils.is_valid_octal("77"), "is_valid_octal('77')")
assert_false(BinaryUtils.is_valid_octal("8"), "is_valid_octal('8')")
assert_false(BinaryUtils.is_valid_octal("9"), "is_valid_octal('9')")

-------------------------------------------------------------------------------
-- 测试：二进制转十进制
-------------------------------------------------------------------------------
test_group("二进制转十进制 (Binary to Decimal)")

assert_num_eq(BinaryUtils.binary_to_decimal("0"), 0, "binary_to_decimal('0')")
assert_num_eq(BinaryUtils.binary_to_decimal("1"), 1, "binary_to_decimal('1')")
assert_num_eq(BinaryUtils.binary_to_decimal("10"), 2, "binary_to_decimal('10')")
assert_num_eq(BinaryUtils.binary_to_decimal("11"), 3, "binary_to_decimal('11')")
assert_num_eq(BinaryUtils.binary_to_decimal("1010"), 10, "binary_to_decimal('1010')")
assert_num_eq(BinaryUtils.binary_to_decimal("1111"), 15, "binary_to_decimal('1111')")
assert_num_eq(BinaryUtils.binary_to_decimal("10000"), 16, "binary_to_decimal('10000')")
assert_num_eq(BinaryUtils.binary_to_decimal("11111111"), 255, "binary_to_decimal('11111111')")
assert_num_eq(BinaryUtils.binary_to_decimal("100000000"), 256, "binary_to_decimal('100000000')")

-------------------------------------------------------------------------------
-- 测试：十进制转二进制
-------------------------------------------------------------------------------
test_group("十进制转二进制 (Decimal to Binary)")

assert_eq(BinaryUtils.decimal_to_binary(0), "0", "decimal_to_binary(0)")
assert_eq(BinaryUtils.decimal_to_binary(1), "1", "decimal_to_binary(1)")
assert_eq(BinaryUtils.decimal_to_binary(2), "10", "decimal_to_binary(2)")
assert_eq(BinaryUtils.decimal_to_binary(10), "1010", "decimal_to_binary(10)")
assert_eq(BinaryUtils.decimal_to_binary(255), "11111111", "decimal_to_binary(255)")
assert_eq(BinaryUtils.decimal_to_binary(0, 8), "00000000", "decimal_to_binary(0, 8)")
assert_eq(BinaryUtils.decimal_to_binary(5, 8), "00000101", "decimal_to_binary(5, 8)")

-------------------------------------------------------------------------------
-- 测试：二进制转十六进制
-------------------------------------------------------------------------------
test_group("二进制转十六进制 (Binary to Hex)")

assert_eq(BinaryUtils.binary_to_hex("0"), "0", "binary_to_hex('0')")
assert_eq(BinaryUtils.binary_to_hex("1"), "1", "binary_to_hex('1')")
assert_eq(BinaryUtils.binary_to_hex("1111"), "F", "binary_to_hex('1111')")
assert_eq(BinaryUtils.binary_to_hex("1010"), "A", "binary_to_hex('1010')")
assert_eq(BinaryUtils.binary_to_hex("11111111"), "FF", "binary_to_hex('11111111')")
assert_eq(BinaryUtils.binary_to_hex("100000001"), "101", "binary_to_hex('100000001')")

-------------------------------------------------------------------------------
-- 测试：十六进制转二进制
-------------------------------------------------------------------------------
test_group("十六进制转二进制 (Hex to Binary)")

assert_eq(BinaryUtils.hex_to_binary("0"), "0000", "hex_to_binary('0')")
assert_eq(BinaryUtils.hex_to_binary("F"), "1111", "hex_to_binary('F')")
assert_eq(BinaryUtils.hex_to_binary("A"), "1010", "hex_to_binary('A')")
assert_eq(BinaryUtils.hex_to_binary("FF"), "11111111", "hex_to_binary('FF')")
assert_eq(BinaryUtils.hex_to_binary("10"), "00010000", "hex_to_binary('10')")

-------------------------------------------------------------------------------
-- 测试：二进制转八进制
-------------------------------------------------------------------------------
test_group("二进制转八进制 (Binary to Octal)")

assert_eq(BinaryUtils.binary_to_octal("0"), "0", "binary_to_octal('0')")
assert_eq(BinaryUtils.binary_to_octal("111"), "7", "binary_to_octal('111')")
assert_eq(BinaryUtils.binary_to_octal("11111111"), "377", "binary_to_octal('11111111')")

-------------------------------------------------------------------------------
-- 测试：八进制转二进制
-------------------------------------------------------------------------------
test_group("八进制转二进制 (Octal to Binary)")

assert_eq(BinaryUtils.octal_to_binary("0"), "000", "octal_to_binary('0')")
assert_eq(BinaryUtils.octal_to_binary("7"), "111", "octal_to_binary('7')")
assert_eq(BinaryUtils.octal_to_binary("77"), "111111", "octal_to_binary('77')")
assert_eq(BinaryUtils.octal_to_binary("377"), "011111111", "octal_to_binary('377')")

-------------------------------------------------------------------------------
-- 测试：字符串操作
-------------------------------------------------------------------------------
test_group("字符串操作 (String Operations)")

assert_eq(BinaryUtils.strip_leading_zeros("0000"), "0", "strip_leading_zeros('0000')")
assert_eq(BinaryUtils.strip_leading_zeros("000101"), "101", "strip_leading_zeros('000101')")
assert_eq(BinaryUtils.strip_leading_zeros("101"), "101", "strip_leading_zeros('101')")

assert_eq(BinaryUtils.pad_binary("101", 8), "00000101", "pad_binary('101', 8)")
assert_eq(BinaryUtils.pad_binary("1010", 8), "00001010", "pad_binary('1010', 8)")
assert_eq(BinaryUtils.pad_binary("11111111", 8), "11111111", "pad_binary('11111111', 8)")

assert_eq(BinaryUtils.reverse_binary("1010"), "0101", "reverse_binary('1010')")
assert_eq(BinaryUtils.reverse_binary("1100"), "0011", "reverse_binary('1100')")

assert_num_eq(BinaryUtils.get_bit("1010", 1), 1, "get_bit('1010', 1)")
assert_num_eq(BinaryUtils.get_bit("1010", 2), 0, "get_bit('1010', 2)")
assert_num_eq(BinaryUtils.get_bit("1010", 3), 1, "get_bit('1010', 3)")
assert_num_eq(BinaryUtils.get_bit("1010", 4), 0, "get_bit('1010', 4)")

assert_eq(BinaryUtils.set_bit("0000", 1, 1), "1000", "set_bit('0000', 1, 1)")
assert_eq(BinaryUtils.set_bit("0000", 4, 1), "0001", "set_bit('0000', 4, 1)")
assert_eq(BinaryUtils.clear_bit("1111", 1), "0111", "clear_bit('1111', 1)")

-------------------------------------------------------------------------------
-- 测试：位运算
-------------------------------------------------------------------------------
test_group("位运算 (Bitwise Operations)")

assert_eq(BinaryUtils.binary_and("1010", "1100"), "1000", "binary_and('1010', '1100')")
assert_eq(BinaryUtils.binary_and("1111", "1010"), "1010", "binary_and('1111', '1010')")

assert_eq(BinaryUtils.binary_or("1010", "1100"), "1110", "binary_or('1010', '1100')")
assert_eq(BinaryUtils.binary_or("0000", "1111"), "1111", "binary_or('0000', '1111')")

assert_eq(BinaryUtils.binary_xor("1010", "1100"), "0110", "binary_xor('1010', '1100')")
assert_eq(BinaryUtils.binary_xor("1111", "1111"), "0000", "binary_xor('1111', '1111')")

assert_eq(BinaryUtils.binary_not("1010"), "0101", "binary_not('1010')")
assert_eq(BinaryUtils.binary_not("0000"), "1111", "binary_not('0000')")
assert_eq(BinaryUtils.binary_not("1111"), "0000", "binary_not('1111')")

assert_eq(BinaryUtils.left_shift("1010", 2), "101000", "left_shift('1010', 2)")
assert_eq(BinaryUtils.left_shift("1", 3), "1000", "left_shift('1', 3)")

assert_eq(BinaryUtils.right_shift("1010", 2), "10", "right_shift('1010', 2)")
assert_eq(BinaryUtils.right_shift("1000", 3), "1", "right_shift('1000', 3)")

assert_eq(BinaryUtils.rotate_left("1010", 1), "0101", "rotate_left('1010', 1)")
assert_eq(BinaryUtils.rotate_left("1100", 2), "0011", "rotate_left('1100', 2)")

assert_eq(BinaryUtils.rotate_right("1010", 1), "0101", "rotate_right('1010', 1)")
assert_eq(BinaryUtils.rotate_right("1100", 2), "0011", "rotate_right('1100', 2)")

-------------------------------------------------------------------------------
-- 测试：算术运算
-------------------------------------------------------------------------------
test_group("算术运算 (Arithmetic Operations)")

assert_eq(BinaryUtils.binary_add("1", "1"), "10", "binary_add('1', '1')")
assert_eq(BinaryUtils.binary_add("10", "10"), "100", "binary_add('10', '10')")
assert_eq(BinaryUtils.binary_add("1010", "1010"), "10100", "binary_add('1010', '1010')")
assert_eq(BinaryUtils.binary_add("1111", "1"), "10000", "binary_add('1111', '1')")

assert_eq(BinaryUtils.binary_sub("10", "1"), "1", "binary_sub('10', '1')")
assert_eq(BinaryUtils.binary_sub("100", "10"), "10", "binary_sub('100', '10')")
assert_eq(BinaryUtils.binary_sub("1111", "1111"), "0", "binary_sub('1111', '1111')")

assert_eq(BinaryUtils.binary_mul("10", "10"), "100", "binary_mul('10', '10')")
assert_eq(BinaryUtils.binary_mul("1010", "10"), "10100", "binary_mul('1010', '10')")

assert_eq(BinaryUtils.binary_div("100", "10"), "10", "binary_div('100', '10')")
assert_eq(BinaryUtils.binary_div("1000", "100"), "10", "binary_div('1000', '100')")

assert_eq(BinaryUtils.binary_mod("10", "1"), "0", "binary_mod('10', '1') - mod 2 by 1")
assert_eq(BinaryUtils.binary_mod("111", "10"), "1", "binary_mod('111', '10') - mod 7 by 2")

-------------------------------------------------------------------------------
-- 测试：统计计算
-------------------------------------------------------------------------------
test_group("统计计算 (Statistics)")

assert_num_eq(BinaryUtils.count_bits("0000"), 0, "count_bits('0000')")
assert_num_eq(BinaryUtils.count_bits("1111"), 4, "count_bits('1111')")
assert_num_eq(BinaryUtils.count_bits("1010"), 2, "count_bits('1010')")
assert_num_eq(BinaryUtils.count_bits("10101010"), 4, "count_bits('10101010')")

assert_num_eq(BinaryUtils.count_zeros("0000"), 4, "count_zeros('0000')")
assert_num_eq(BinaryUtils.count_zeros("1111"), 0, "count_zeros('1111')")
assert_num_eq(BinaryUtils.count_zeros("1010"), 2, "count_zeros('1010')")

assert_num_eq(BinaryUtils.hamming_weight("1010"), 2, "hamming_weight('1010')")

assert_num_eq(BinaryUtils.hamming_distance("1010", "1010"), 0, "hamming_distance('1010', '1010')")
assert_num_eq(BinaryUtils.hamming_distance("1010", "1111"), 2, "hamming_distance('1010', '1111')")
assert_num_eq(BinaryUtils.hamming_distance("0000", "1111"), 4, "hamming_distance('0000', '1111')")

-------------------------------------------------------------------------------
-- 测试：模式匹配
-------------------------------------------------------------------------------
test_group("模式匹配 (Pattern Matching)")

assert_num_eq(BinaryUtils.find_first_one("0001"), 4, "find_first_one('0001')")
assert_num_eq(BinaryUtils.find_first_one("0010"), 3, "find_first_one('0010')")
assert_nil(BinaryUtils.find_first_one("0000"), "find_first_one('0000')")

assert_num_eq(BinaryUtils.find_last_one("1000"), 1, "find_last_one('1000')")
assert_num_eq(BinaryUtils.find_last_one("1100"), 2, "find_last_one('1100')")

assert_num_eq(BinaryUtils.find_first_zero("1110"), 4, "find_first_zero('1110')")
assert_num_eq(BinaryUtils.find_first_zero("1101"), 3, "find_first_zero('1101')")

assert_num_eq(BinaryUtils.find_pattern("10101010", "101"), 1, "find_pattern('10101010', '101')")
assert_num_eq(BinaryUtils.find_pattern("11111111", "11"), 1, "find_pattern('11111111', '11')")

-------------------------------------------------------------------------------
-- 测试：特殊功能
-------------------------------------------------------------------------------
test_group("特殊功能 (Special Functions)")

assert_true(BinaryUtils.is_even("10"), "is_even('10')")
assert_true(BinaryUtils.is_even("100"), "is_even('100')")
assert_false(BinaryUtils.is_even("11"), "is_even('11')")

assert_true(BinaryUtils.is_odd("1"), "is_odd('1')")
assert_true(BinaryUtils.is_odd("11"), "is_odd('11')")
assert_false(BinaryUtils.is_odd("10"), "is_odd('10')")

assert_true(BinaryUtils.is_power_of_two("1"), "is_power_of_two('1')")
assert_true(BinaryUtils.is_power_of_two("10"), "is_power_of_two('10')")
assert_true(BinaryUtils.is_power_of_two("100"), "is_power_of_two('100')")
assert_true(BinaryUtils.is_power_of_two("1000"), "is_power_of_two('1000')")
assert_false(BinaryUtils.is_power_of_two("11"), "is_power_of_two('11')")
assert_false(BinaryUtils.is_power_of_two("101"), "is_power_of_two('101')")

assert_num_eq(BinaryUtils.bit_length("1010"), 4, "bit_length('1010')")
assert_num_eq(BinaryUtils.bit_length("11111111"), 8, "bit_length('11111111')")

assert_eq(BinaryUtils.format_as_bytes("10101010"), "10101010", "format_as_bytes('10101010')")
assert_eq(BinaryUtils.format_as_bytes("1010101010101010"), "10101010 10101010", "format_as_bytes(16 bits)")

-------------------------------------------------------------------------------
-- 测试：字节操作
-------------------------------------------------------------------------------
test_group("字节操作 (Byte Operations)")

local bytes = BinaryUtils.to_byte_array("1111111100000000")
assert_num_eq(bytes[1], 255, "to_byte_array first byte")
assert_num_eq(bytes[2], 0, "to_byte_array second byte")

local binary_from_bytes = BinaryUtils.from_byte_array({255, 0})
assert_eq(binary_from_bytes, "1111111100000000", "from_byte_array")

assert_eq(BinaryUtils.char_to_binary("A"), "01000001", "char_to_binary('A')")
assert_eq(BinaryUtils.char_to_binary("a"), "01100001", "char_to_binary('a')")

assert_eq(BinaryUtils.binary_to_char("01000001"), "A", "binary_to_char('01000001')")
assert_eq(BinaryUtils.binary_to_char("01100001"), "a", "binary_to_char('01100001')")

assert_eq(BinaryUtils.string_to_binary("AB"), "0100000101000010", "string_to_binary('AB')")
assert_eq(BinaryUtils.binary_to_string("0100000101000010"), "AB", "binary_to_string for 'AB'")

-------------------------------------------------------------------------------
-- 测试：随机与工厂
-------------------------------------------------------------------------------
test_group("随机与工厂 (Random and Factory)")

local random_bin = BinaryUtils.random_binary(8)
assert_true(BinaryUtils.is_valid_binary(random_bin), "random_binary is valid")
assert_num_eq(#random_bin, 8, "random_binary length is 8")

-- 测试工厂函数
local bin_obj = BinaryUtils.create(10)
assert_num_eq(bin_obj.to_decimal(), 10, "create from decimal")
assert_eq(bin_obj.to_hex(), "A", "create().to_hex()")

local bin_obj2 = BinaryUtils.create("1010")
assert_num_eq(bin_obj2.to_decimal(), 10, "create from binary string")

local hex_obj = BinaryUtils.create("A")
assert_true(BinaryUtils.is_valid_binary(hex_obj.binary), "create from hex string")

-- 测试工厂对象方法
local obj1 = BinaryUtils.create("1010")
local obj2 = BinaryUtils.create("1100")
assert_eq(obj1.and_(obj2).binary, "1000", "factory and_()")
assert_eq(obj1.or_(obj2).binary, "1110", "factory or_()")
assert_eq(obj1.xor_(obj2).binary, "0110", "factory xor_()")
assert_eq(obj1.not_().binary, "0101", "factory not_()")

-------------------------------------------------------------------------------
-- 测试总结
-------------------------------------------------------------------------------
print("\n" .. string.rep("=", 50))
print("📊 测试总结 (Test Summary)")
print(string.rep("=", 50))
print(string.format("✅ 通过: %d", tests_passed))
print(string.format("❌ 失败: %d", tests_failed))
print(string.format("📝 总数: %d", tests_run))
print(string.format("📈 通过率: %.1f%%", (tests_passed / tests_run) * 100))

if tests_failed > 0 then
    print("\n❌ 失败详情:")
    for i, failure in ipairs(failures) do
        print(string.format("  %d. %s", i, failure))
    end
    os.exit(1)
else
    print("\n🎉 所有测试通过!")
    os.exit(0)
end