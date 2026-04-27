--[[
    examples.lua - Usage Examples for bit_utils module
    
    Run with: lua examples.lua
]]

print([[
========================================
  bit_utils Usage Examples
========================================
]])

local bit = dofile("bit_utils.lua")

-- Example 1: Basic bitwise operations
print("--- Example 1: Basic Bitwise Operations ---")
print("Setting up permission flags:")
local READ = 1 << 0    -- 0x01
local WRITE = 1 << 1   -- 0x02
local EXECUTE = 1 << 2 -- 0x04
local DELETE = 1 << 3  -- 0x08

local permissions = 0
permissions = bit.set_flags(permissions, READ)
permissions = bit.set_flags(permissions, WRITE)
print(string.format("Permissions: %s (binary: %s)", 
    bit.to_hex(permissions), bit.to_bin(permissions, 4)))

print("Has READ permission:", bit.test(permissions, 0))
print("Has EXECUTE permission:", bit.test(permissions, 2))
print()

-- Example 2: Bit field extraction/insertion
print("--- Example 2: Bit Field Operations ---")
print("Working with a 32-bit color value:")
local color = 0xFF8040 -- RGB: R=255, G=128, B=64

local red = bit.extract(color, 16, 8)
local green = bit.extract(color, 8, 8)
local blue = bit.extract(color, 0, 8)
print(string.format("Original color: #%s", bit.to_hex(color, 6)))
print(string.format("  Red: %d, Green: %d, Blue: %d", red, green, blue))

-- Modify green channel
color = bit.insert(color, 8, 8, 200)
print(string.format("After changing green to 200: #%s", bit.to_hex(color, 6)))
print()

-- Example 3: Flag manipulation with masks
print("--- Example 3: Flag Manipulation ---")
print("File attributes example:")
local FILE_ATTRIBUTE_READONLY  = 0x01
local FILE_ATTRIBUTE_HIDDEN     = 0x02
local FILE_ATTRIBUTE_SYSTEM     = 0x04
local FILE_ATTRIBUTE_DIRECTORY  = 0x10
local FILE_ATTRIBUTE_ARCHIVE    = 0x20

local attrs = bit.bors(FILE_ATTRIBUTE_ARCHIVE, FILE_ATTRIBUTE_READONLY)
print(string.format("Initial attributes: %s", bit.to_bin(attrs, 8)))

print("Is archived?", bit.test(attrs, 5))  -- bit 5
print("Is hidden?", bit.test(attrs, 1))     -- bit 1

attrs = bit.set_flags(attrs, FILE_ATTRIBUTE_HIDDEN)
print(string.format("After setting hidden: %s", bit.to_bin(attrs, 8)))

attrs = bit.clear_flags(attrs, FILE_ATTRIBUTE_READONLY)
print(string.format("After clearing readonly: %s", bit.to_bin(attrs, 8)))
print()

-- Example 4: Bit counting and finding
print("--- Example 4: Bit Counting ---")
local values = {0, 1, 0xFF, 0xAAAA, 0xFFFFFFFF}
for _, v in ipairs(values) do
    print(string.format("popcount(0x%08X) = %d", v, bit.popcount(v)))
end
print()

print("Finding set bits in 0b10110100:")
local val = 0xB4
local pos = -1
while true do
    pos = bit.find_next_set(val, pos)
    if pos < 0 then break end
    print(string.format("  Bit %d is set (value: %d)", pos, 1 << pos))
end
print()

-- Example 5: Byte manipulation
print("--- Example 5: Byte Operations ---")
local num = 0x12345678
print(string.format("Original: 0x%08X", num))

print("Bytes (little-endian):")
for i = 0, 3 do
    print(string.format("  Byte %d: 0x%02X", i, bit.get_byte(num, i)))
end

print("Bytes (big-endian):")
local be_bytes = bit.to_bytes_be(num, 4)
for i, b in ipairs(be_bytes) do
    print(string.format("  Byte %d: 0x%02X", i-1, b))
end

print("Byte-swap (endianness conversion):")
print(string.format("  bswap(0x%08X) = 0x%08X", num, bit.bswap(num)))
print()

-- Example 6: Power of two operations
print("--- Example 6: Power of Two Operations ---")
for _, v in ipairs({3, 4, 5, 100, 128, 255}) do
    local is_pow2 = bit.is_power_of_two(v)
    local next_pow2 = bit.next_power_of_two(v)
    local floor_pow2 = bit.floor_power_of_two(v)
    print(string.format("%3d: is_pow2=%s, next_pow2=%3d, floor_pow2=%3d",
        v, tostring(is_pow2), next_pow2, floor_pow2))
end
print()

-- Example 7: Memory alignment
print("--- Example 7: Memory Alignment ---")
local sizes = {1, 17, 32, 33, 100, 128}
print("Aligning to 16-byte boundary:")
for _, size in ipairs(sizes) do
    local aligned = bit.align(size, 16)
    print(string.format("  %3d -> %3d", size, aligned))
end
print()

-- Example 8: Bit rotation
print("--- Example 8: Bit Rotation ---")
local rot_val = 0x80000001
print(string.format("Original: %s", bit.to_bin(rot_val)))
print(string.format("ROL by 1: %s", bit.to_bin(bit.rol(rot_val, 1))))
print(string.format("ROR by 1: %s", bit.to_bin(bit.ror(rot_val, 1))))
print()

-- Example 9: Creating and using bitmasks
print("--- Example 9: Bitmask Creation ---")
local mask1 = bit.make_mask(0, 1, 2, 3)  -- bits 0-3
print(string.format("make_mask(0,1,2,3) = 0x%02X (binary: %s)", 
    mask1, bit.to_bin(mask1, 8)))

local mask2 = bit.mask_range(4, 7)  -- bits 4-7
print(string.format("mask_range(4,7) = 0x%02X (binary: %s)", 
    mask2, bit.to_bin(mask2, 8)))
print()

-- Example 10: Practical use - parsing network packet
print("--- Example 10: Network Packet Header Parsing ---")
-- Simulated IPv4 header field extraction
local ip_header = 0x4500003C -- Version=4, IHL=5, TOS=0, Total Length=60

local version = bit.extract(ip_header, 28, 4)
local ihl = bit.extract(ip_header, 24, 4)
local tos = bit.extract(ip_header, 16, 8)
local total_length = bit.extract(ip_header, 0, 16)

print("Parsing IPv4 header word 0x4500003C:")
print(string.format("  Version: %d", version))
print(string.format("  IHL (Header Length): %d (words) = %d bytes", ihl, ihl * 4))
print(string.format("  TOS: 0x%02X", tos))
print(string.format("  Total Length: %d bytes", total_length))
print()

-- Example 11: Converting between binary/hex strings
print("--- Example 11: String Conversion ---")
local test_val = 0xDEADBEEF
print(string.format("Value: 0x%08X", test_val))
print(string.format("  Binary: %s", bit.to_bin(test_val)))
print(string.format("  Hex: %s", bit.to_hex(test_val)))
print(string.format("From bin: %s -> 0x%X", "1111000011110000", bit.from_bin("1111000011110000")))
print(string.format("From hex: %s -> 0x%X", "CAFEBABE", bit.from_hex("CAFEBABE")))
print()

print([[
========================================
  Examples completed!
========================================
]])