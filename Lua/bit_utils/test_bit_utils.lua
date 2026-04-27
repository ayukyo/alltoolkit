--[[
    test_bit_utils.lua - Test Suite for bit_utils module
    
    Run with: lua test_bit_utils.lua
]]

-- Load the module
local bit_utils = dofile("bit_utils.lua")

-- Test result tracking
local tests_passed = 0
local tests_failed = 0
local failures = {}

local function test(name, condition)
    if condition then
        tests_passed = tests_passed + 1
        print("✓ " .. name)
    else
        tests_failed = tests_failed + 1
        print("✗ " .. name)
        table.insert(failures, name)
    end
end

local function test_equal(name, expected, actual)
    test(name, expected == actual)
    if expected ~= actual then
        print("  Expected: " .. tostring(expected) .. " (" .. type(expected) .. ")")
        print("  Actual: " .. tostring(actual) .. " (" .. type(actual) .. ")")
    end
end

print("========================================")
print("  bit_utils Test Suite")
print("========================================\n")

-- ========================================
-- Basic Bitwise Operations
-- ========================================
print("--- Basic Bitwise Operations ---")

test_equal("band(0xFF, 0x0F) = 0x0F", 0x0F, bit_utils.band(0xFF, 0x0F))
test_equal("band(0xFFFF, 0xFF00) = 0xFF00", 0xFF00, bit_utils.band(0xFFFF, 0xFF00))
test_equal("band(0, 1) = 0", 0, bit_utils.band(0, 1))
test_equal("band(1, 1) = 1", 1, bit_utils.band(1, 1))

test_equal("bor(0xF0, 0x0F) = 0xFF", 0xFF, bit_utils.bor(0xF0, 0x0F))
test_equal("bor(0, 0xFF) = 0xFF", 0xFF, bit_utils.bor(0, 0xFF))
test_equal("bor(0xAA, 0x55) = 0xFF", 0xFF, bit_utils.bor(0xAA, 0x55))

test_equal("bxor(0xFF, 0xFF) = 0", 0, bit_utils.bxor(0xFF, 0xFF))
test_equal("bxor(0xAA, 0x55) = 0xFF", 0xFF, bit_utils.bxor(0xAA, 0x55))
test_equal("bxor(0, 0xFF) = 0xFF", 0xFF, bit_utils.bxor(0, 0xFF))

test_equal("bnot(0) = 0xFFFFFFFF", 0xFFFFFFFF, bit_utils.bnot(0))
test_equal("bnot(0xFF) = 0xFFFFFF00", 0xFFFFFF00, bit_utils.bnot(0xFF))

-- Multi-operand operations
test_equal("bands(0xFF, 0xF0, 0x0F) = 0", 0, bit_utils.bands(0xFF, 0xF0, 0x0F))
test_equal("bors(1, 2, 4, 8) = 15", 15, bit_utils.bors(1, 2, 4, 8))

-- ========================================
-- Bit Shifting Operations
-- ========================================
print("\n--- Bit Shifting Operations ---")

test_equal("lshift(1, 4) = 16", 16, bit_utils.lshift(1, 4))
test_equal("lshift(0xFF, 8) = 0xFF00", 0xFF00, bit_utils.lshift(0xFF, 8))
test_equal("lshift(1, 0) = 1", 1, bit_utils.lshift(1, 0))

test_equal("rshift(0xFF00, 8) = 0xFF", 0xFF, bit_utils.rshift(0xFF00, 8))
test_equal("rshift(16, 4) = 1", 1, bit_utils.rshift(16, 4))
test_equal("rshift(0xFF, 0) = 0xFF", 0xFF, bit_utils.rshift(0xFF, 0))

-- Negative shift (should reverse direction)
test_equal("lshift(16, -4) = 1", 1, bit_utils.lshift(16, -4))
test_equal("rshift(1, -4) = 16", 16, bit_utils.rshift(1, -4))

-- Rotation
test_equal("rol(0x80000001, 1) = 0x00000003", 0x00000003, bit_utils.rol(0x80000001, 1))
test_equal("rol(0x00000001, 4) = 0x00000010", 0x00000010, bit_utils.rol(1, 4))
test_equal("ror(0x00000003, 1) = 0x80000001", 0x80000001, bit_utils.ror(0x00000003, 1))
test_equal("ror(0x00000010, 4) = 0x00000001", 0x00000001, bit_utils.ror(0x10, 4))

-- Full rotation should return same value
test_equal("rol(0x12345678, 32) = 0x12345678", 0x12345678, bit_utils.rol(0x12345678, 32))
test_equal("ror(0x12345678, 32) = 0x12345678", 0x12345678, bit_utils.ror(0x12345678, 32))

-- ========================================
-- Single Bit Manipulation
-- ========================================
print("\n--- Single Bit Manipulation ---")

test("test(8, 3) = true", bit_utils.test(8, 3))          -- 8 = 0b1000
test("test(8, 2) = false", not bit_utils.test(8, 2))    -- 8 = 0b1000
test("test(0, 0) = false", not bit_utils.test(0, 0))

test_equal("set(0, 0) = 1", 1, bit_utils.set(0, 0))
test_equal("set(0, 4) = 16", 16, bit_utils.set(0, 4))
test_equal("set(1, 0) = 1 (already set)", 1, bit_utils.set(1, 0))

test_equal("clear(1, 0) = 0", 0, bit_utils.clear(1, 0))
test_equal("clear(0xFF, 4) = 0xEF", 0xEF, bit_utils.clear(0xFF, 4))
test_equal("clear(0, 0) = 0 (already clear)", 0, bit_utils.clear(0, 0))

test_equal("toggle(0, 0) = 1", 1, bit_utils.toggle(0, 0))
test_equal("toggle(1, 0) = 0", 0, bit_utils.toggle(1, 0))
test_equal("toggle(0xF0, 4) = 0xE0", 0xE0, bit_utils.toggle(0xF0, 4))  -- 0xF0 has bit 4 set, toggle clears it to 0xE0

-- ========================================
-- Bit Field Operations
-- ========================================
print("\n--- Bit Field Operations ---")

-- Extract
test_equal("extract(0x00F0, 4, 4) = 0xF", 0xF, bit_utils.extract(0x00F0, 4, 4))
test_equal("extract(0x1234, 0, 8) = 0x34", 0x34, bit_utils.extract(0x1234, 0, 8))
test_equal("extract(0x1234, 8, 8) = 0x12", 0x12, bit_utils.extract(0x1234, 8, 8))

-- Insert
test_equal("insert(0x0000, 4, 4, 0xF) = 0xF0", 0xF0, bit_utils.insert(0x0000, 4, 4, 0xF))
test_equal("insert(0x1200, 0, 8, 0x34) = 0x1234", 0x1234, bit_utils.insert(0x1200, 0, 8, 0x34))

-- Range operations
test_equal("extract_range(0x0FF0, 4, 7) = 0xF", 0xF, bit_utils.extract_range(0x0FF0, 4, 7))  -- 0x0FF0 = bits 4-11 set, so bits 4-7 = 0xF
test_equal("replace_range(0, 4, 7, 0xFF) = 0xF0", 0xF0, bit_utils.replace_range(0, 4, 7, 0xFF))

-- ========================================
-- Bit Counting Utilities
-- ========================================
print("\n--- Bit Counting Utilities ---")

test_equal("popcount(0) = 0", 0, bit_utils.popcount(0))
test_equal("popcount(1) = 1", 1, bit_utils.popcount(1))
test_equal("popcount(0xFF) = 8", 8, bit_utils.popcount(0xFF))
test_equal("popcount(0xFFFFFFFF) = 32", 32, bit_utils.popcount(0xFFFFFFFF))
test_equal("popcount(0xAAAAAAAA) = 16", 16, bit_utils.popcount(0xAAAAAAAA))

-- Fast popcount should give same results
test_equal("popcount_fast(0xFF) = 8", 8, bit_utils.popcount_fast(0xFF))
test_equal("popcount_fast(0xAAAAAAAA) = 16", 16, bit_utils.popcount_fast(0xAAAAAAAA))

test_equal("clz(0) = 32", 32, bit_utils.clz(0))
test_equal("clz(1) = 31", 31, bit_utils.clz(1))
test_equal("clz(0x80000000) = 0", 0, bit_utils.clz(0x80000000))
test_equal("clz(0x00800000) = 8", 8, bit_utils.clz(0x00800000))

test_equal("ctz(0) = 32", 32, bit_utils.ctz(0))
test_equal("ctz(1) = 0", 0, bit_utils.ctz(1))
test_equal("ctz(0x80000000) = 31", 31, bit_utils.ctz(0x80000000))
test_equal("ctz(0x0100) = 8", 8, bit_utils.ctz(0x0100))

test_equal("ffs(0) = -1", -1, bit_utils.ffs(0))
test_equal("ffs(1) = 0", 0, bit_utils.ffs(1))
test_equal("ffs(0x100) = 8", 8, bit_utils.ffs(0x100))

test_equal("fls(0) = -1", -1, bit_utils.fls(0))
test_equal("fls(1) = 0", 0, bit_utils.fls(1))
test_equal("fls(0x100) = 8", 8, bit_utils.fls(0x100))
test_equal("fls(0xFFFFFFFF) = 31", 31, bit_utils.fls(0xFFFFFFFF))

test_equal("find_next_set(10, -1) = 1", 1, bit_utils.find_next_set(10, -1))          -- 10 = 0b1010
test_equal("find_next_set(10, 1) = 3", 3, bit_utils.find_next_set(10, 1))
test_equal("find_next_set(10, 3) = -1", -1, bit_utils.find_next_set(10, 3))

test_equal("find_next_clear(5, -1) = 1", 1, bit_utils.find_next_clear(5, -1))          -- 5 = 0b0101
test_equal("find_next_clear(5, 1) = 3", 3, bit_utils.find_next_clear(5, 1))

-- ========================================
-- Byte Conversion Utilities
-- ========================================
print("\n--- Byte Conversion Utilities ---")

local bytes_be = bit_utils.to_bytes_be(0x12345678, 4)
test_equal("to_bytes_be(0x12345678)[1] = 0x12", 0x12, bytes_be[1])
test_equal("to_bytes_be(0x12345678)[4] = 0x78", 0x78, bytes_be[4])

local bytes_le = bit_utils.to_bytes_le(0x12345678, 4)
test_equal("to_bytes_le(0x12345678)[1] = 0x78", 0x78, bytes_le[1])
test_equal("to_bytes_le(0x12345678)[4] = 0x12", 0x12, bytes_le[4])

test_equal("from_bytes_be({0x12, 0x34, 0x56, 0x78}) = 0x12345678", 
    0x12345678, bit_utils.from_bytes_be({0x12, 0x34, 0x56, 0x78}))
test_equal("from_bytes_le({0x78, 0x56, 0x34, 0x12}) = 0x12345678", 
    0x12345678, bit_utils.from_bytes_le({0x78, 0x56, 0x34, 0x12}))

test_equal("get_byte(0x12345678, 0) = 0x78", 0x78, bit_utils.get_byte(0x12345678, 0))
test_equal("get_byte(0x12345678, 1) = 0x56", 0x56, bit_utils.get_byte(0x12345678, 1))
test_equal("get_byte(0x12345678, 3) = 0x12", 0x12, bit_utils.get_byte(0x12345678, 3))

test_equal("set_byte(0x12345678, 0, 0xAA) = 0x123456AA", 
    0x123456AA, bit_utils.set_byte(0x12345678, 0, 0xAA))

test_equal("bswap(0x12345678) = 0x78563412", 0x78563412, bit_utils.bswap(0x12345678))
test_equal("bswap16(0x1234) = 0x3412", 0x3412, bit_utils.bswap16(0x1234))

-- ========================================
-- Flag Manipulation
-- ========================================
print("\n--- Flag Manipulation ---")

local flag1 = 1 << 0  -- 0x01
local flag2 = 1 << 1  -- 0x02
local flag3 = 1 << 2  -- 0x04
local mask = bit_utils.make_mask(0, 1, 2)  -- 0x07

test_equal("make_mask(0, 1, 2) = 0x07", 0x07, mask)
test_equal("make_mask(4, 5) = 0x30", 0x30, bit_utils.make_mask(4, 5))

test("any_set(0x07, 0x02) = true", bit_utils.any_set(0x07, 0x02))
test("any_set(0x00, 0x02) = false", not bit_utils.any_set(0x00, 0x02))
test("any_set(0x08, 0x02) = false", not bit_utils.any_set(0x08, 0x02))

test("all_set(0x07, 0x07) = true", bit_utils.all_set(0x07, 0x07))
test("all_set(0x03, 0x07) = false", not bit_utils.all_set(0x03, 0x07))

test("none_set(0x00, 0x07) = true", bit_utils.none_set(0x00, 0x07))
test("none_set(0x01, 0x07) = false", not bit_utils.none_set(0x01, 0x07))

test_equal("set_flags(0x00, 0x07) = 0x07", 0x07, bit_utils.set_flags(0x00, 0x07))
test_equal("set_flags(0x01, 0x06) = 0x07", 0x07, bit_utils.set_flags(0x01, 0x06))

test_equal("clear_flags(0x07, 0x02) = 0x05", 0x05, bit_utils.clear_flags(0x07, 0x02))
test_equal("clear_flags(0x07, 0x07) = 0x00", 0x00, bit_utils.clear_flags(0x07, 0x07))

test_equal("toggle_flags(0x05, 0x02) = 0x07", 0x07, bit_utils.toggle_flags(0x05, 0x02))
test_equal("toggle_flags(0x07, 0x02) = 0x05", 0x05, bit_utils.toggle_flags(0x07, 0x02))

-- ========================================
-- Utility Functions
-- ========================================
print("\n--- Utility Functions ---")

test_equal("to_bin(0xF0, 8) = '11110000'", "11110000", bit_utils.to_bin(0xF0, 8))
test_equal("to_bin(0, 4) = '0000'", "0000", bit_utils.to_bin(0, 4))
test_equal("to_bin(1) = 32 chars", 32, #bit_utils.to_bin(1))

test_equal("from_bin('11110000') = 0xF0", 0xF0, bit_utils.from_bin("11110000"))
test_equal("from_bin('1010') = 10", 10, bit_utils.from_bin("1010"))

test_equal("to_hex(0xDEADBEEF) = 'DEADBEEF'", "DEADBEEF", bit_utils.to_hex(0xDEADBEEF))
test_equal("to_hex(0, 4) = '0000'", "0000", bit_utils.to_hex(0, 4))

test_equal("from_hex('DEADBEEF') = 0xDEADBEEF", 0xDEADBEEF, bit_utils.from_hex("DEADBEEF"))
test_equal("from_hex('ff') = 0xFF", 0xFF, bit_utils.from_hex("ff"))

test_equal("reverse(0xF0F0F0F0) = 0x0F0F0F0F", 0x0F0F0F0F, bit_utils.reverse(0xF0F0F0F0))
test_equal("reverse(0x01, 8) = 0x80", 0x80, bit_utils.reverse(0x01, 8))

test_equal("mask_range(4, 7) = 0xF0", 0xF0, bit_utils.mask_range(4, 7))
test_equal("mask_range(0, 3) = 0x0F", 0x0F, bit_utils.mask_range(0, 3))

test("is_power_of_two(1) = true", bit_utils.is_power_of_two(1))
test("is_power_of_two(2) = true", bit_utils.is_power_of_two(2))
test("is_power_of_two(4) = true", bit_utils.is_power_of_two(4))
test("is_power_of_two(256) = true", bit_utils.is_power_of_two(256))
test("is_power_of_two(0) = false", not bit_utils.is_power_of_two(0))
test("is_power_of_two(3) = false", not bit_utils.is_power_of_two(3))
test("is_power_of_two(100) = false", not bit_utils.is_power_of_two(100))

test_equal("next_power_of_two(0) = 1", 1, bit_utils.next_power_of_two(0))
test_equal("next_power_of_two(1) = 1", 1, bit_utils.next_power_of_two(1))
test_equal("next_power_of_two(5) = 8", 8, bit_utils.next_power_of_two(5))
test_equal("next_power_of_two(100) = 128", 128, bit_utils.next_power_of_two(100))

test_equal("floor_power_of_two(100) = 64", 64, bit_utils.floor_power_of_two(100))
test_equal("floor_power_of_two(128) = 128", 128, bit_utils.floor_power_of_two(128))
test_equal("floor_power_of_two(1) = 1", 1, bit_utils.floor_power_of_two(1))
test_equal("floor_power_of_two(0) = 0", 0, bit_utils.floor_power_of_two(0))

test_equal("align(100, 16) = 112", 112, bit_utils.align(100, 16))
test_equal("align(112, 16) = 112", 112, bit_utils.align(112, 16))
test_equal("align(0, 8) = 0", 0, bit_utils.align(0, 8))
test_equal("align(17, 32) = 32", 32, bit_utils.align(17, 32))

test_equal("align_down(100, 16) = 96", 96, bit_utils.align_down(100, 16))
test_equal("align_down(112, 16) = 112", 112, bit_utils.align_down(112, 16))
test_equal("align_down(17, 32) = 0", 0, bit_utils.align_down(17, 32))

-- ========================================
-- Summary
-- ========================================
print("\n========================================")
print("  Test Summary")
print("========================================")
print(string.format("  Passed: %d", tests_passed))
print(string.format("  Failed: %d", tests_failed))
print("========================================")

if tests_failed > 0 then
    print("\nFailed tests:")
    for _, name in ipairs(failures) do
        print("  - " .. name)
    end
    os.exit(1)
else
    print("\nAll tests passed!")
    os.exit(0)
end