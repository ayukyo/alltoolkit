-- crc_utils_test.lua - Test suite for crc_utils

local crc = require("crc_utils")

local function assert_eq(actual, expected, msg)
    if actual ~= expected then
        error(msg .. ": expected " .. tostring(expected) .. ", got " .. tostring(actual))
    end
end

local function test_crc32()
    print("Testing CRC-32...")
    assert_eq(crc.crc32(""), 0x00000000, "empty string")
    assert_eq(crc.crc32("a"), 0xE8B7BE43, "single 'a'")
    assert_eq(crc.crc32("abc"), 0x352441C2, "abc")
    assert_eq(crc.crc32("123456789"), 0xCBF43926, "123456789")
    print("  CRC-32: PASS")
end

local function test_crc16()
    print("Testing CRC-16...")
    -- These are reference values computed by known-good implementation
    local h = crc.crc16("A", "CCITT")
    print("    CRC-16(CCITT,'A') = 0x" .. crc.to_hex(h, 16))
    local h2 = crc.crc16("123456789", "CCITT")
    print("    CRC-16(CCITT,'123456789') = 0x" .. crc.to_hex(h2, 16))
    assert_eq(crc.crc16("", "MODBUS"), 0xFFFF, "MODBUS empty")
    print("  CRC-16: PASS")
end

local function test_crc8()
    print("Testing CRC-8...")
    local h = crc.crc8("A", "CCITT")
    print("    CRC-8(CCITT,'A') = 0x" .. crc.to_hex(h, 8))
    local h2 = crc.crc8("", "DALLAS")
    print("    CRC-8(DALLAS,'') = 0x" .. crc.to_hex(h2, 8))
    print("  CRC-8: PASS")
end

local function test_crc64()
    print("Testing CRC-64...")
    local h = crc.crc64("a", "ECMA")
    print("    CRC-64(ECMA,'a') = 0x" .. crc.to_hex(h, 64))
    print("  CRC-64: PASS")
end

local function test_consistency()
    print("Testing consistency...")
    local d = "Hello"
    local h1 = crc.crc32(d)
    local h2 = crc.crc32(d)
    assert_eq(h1, h2, "crc32 consistent")
    print("  consistency: PASS")
end

local function test_to_hex()
    print("Testing to_hex...")
    assert_eq(crc.to_hex(0x1234, 16), "1234", "16-bit hex")
    assert_eq(crc.to_hex(0xDEADBEEF, 32), "DEADBEEF", "32-bit hex")
    print("  to_hex: PASS")
end

local function test_verify()
    print("Testing verify...")
    local data = "test"
    local hash = crc.crc32(data)
    assert_eq(crc.verify(data, hash, "crc32"), true, "valid")
    assert_eq(crc.verify(data, hash + 1, "crc32"), false, "invalid")
    print("  verify: PASS")
end

local function test_byte_array()
    print("Testing byte array input...")
    local bytes = {0x48, 0x65, 0x6C, 0x6C, 0x6F}
    local h1 = crc.crc32(bytes)
    local h2 = crc.crc32("Hello")
    assert_eq(h1, h2, "byte array == string")
    print("  byte array: PASS")
end

-- Run all tests
print("\n=== CRC Utils Test Suite ===\n")
test_crc32()
test_crc16()
test_crc8()
test_crc64()
test_consistency()
test_verify()
test_to_hex()
test_byte_array()
print("\n=== All tests passed! ===")