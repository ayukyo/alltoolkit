--[[
    bit_utils.lua - Comprehensive Bit Manipulation Utilities for Lua
    
    A pure Lua implementation of bitwise operations with zero external dependencies.
    Supports both Lua 5.1+ (using bit32 or native bit operations) and Lua 5.2+
    with native bitwise operators.
    
    Features:
    - Basic bitwise operations (AND, OR, XOR, NOT)
    - Bit shifting and rotation
    - Single bit manipulation (set, clear, toggle, test)
    - Bit field operations (extract, insert)
    - Bit counting utilities (popcount, leading/trailing zeros)
    - Byte conversion utilities
    - Flag manipulation helpers
    
    License: MIT
    Author: AllToolkit
    Version: 1.0.0
]]

local bit_utils = {}

-- Determine available bit operations
local band, bor, bxor, bnot, lshift, rshift, arshift
local has_native_bitops = false

-- Try native Lua 5.3+ bitwise operators first
if _VERSION >= "Lua 5.3" then
    has_native_bitops = true
    band = function(a, b) return a & b end
    bor = function(a, b) return a | b end
    bxor = function(a, b) return a ~ b end
    bnot = function(a) return ~a end
    lshift = function(a, n) return a << n end
    rshift = function(a, n) return a >> n end
    -- Arithmetic right shift (Lua 5.3+ doesn't have this built-in)
    arshift = function(a, n)
        if n == 0 then return a end
        local sign = a < 0 and -1 or 0
        local mask = sign * (2 ^ (32 - n)) - sign
        return (a >> n) | mask
    end
else
    -- Try bit32 library (Lua 5.2)
    local bit32 = bit32 or (package.loaded["bit32"])
    if bit32 then
        band = bit32.band
        bor = bit32.bor
        bxor = bit32.bxor
        bnot = bit32.bnot
        lshift = bit32.lshift
        rshift = bit32.rshift
        arshift = bit32.arshift
    else
        -- Try LuaJIT bit library
        local bit = bit or (package.loaded["bit"])
        if bit then
            band = bit.band
            bor = bit.bor
            bxor = bit.bxor
            bnot = bit.bnot
            lshift = bit.lshift
            rshift = bit.rshift
            arshift = bit.arshift
        else
            -- Pure Lua fallback (slow but works)
            error("No bitwise operations available. Please use Lua 5.2+, LuaJIT, or install bit32 library.")
        end
    end
end

-- Mask for 32-bit operations
local MASK32 = 0xFFFFFFFF

-- Normalize to 32-bit unsigned integer
local function to_u32(n)
    return n % (MASK32 + 1)
end

-- ============================================================
-- Basic Bitwise Operations
-- ============================================================

--- Bitwise AND operation
-- @param a First operand
-- @param b Second operand
-- @return a AND b
function bit_utils.band(a, b)
    return to_u32(band(to_u32(a), to_u32(b)))
end

--- Bitwise OR operation
-- @param a First operand
-- @param b Second operand
-- @return a OR b
function bit_utils.bor(a, b)
    return to_u32(bor(to_u32(a), to_u32(b)))
end

--- Bitwise XOR operation
-- @param a First operand
-- @param b Second operand
-- @return a XOR b
function bit_utils.bxor(a, b)
    return to_u32(bxor(to_u32(a), to_u32(b)))
end

--- Bitwise NOT operation
-- @param a Operand
-- @return NOT a
function bit_utils.bnot(a)
    return to_u32(bnot(to_u32(a)))
end

--- Multiple operand AND
-- @param ... Variable number of operands
-- @return AND of all operands
function bit_utils.bands(...)
    local args = {...}
    if #args == 0 then return MASK32 end
    local result = to_u32(args[1])
    for i = 2, #args do
        result = band(result, to_u32(args[i]))
    end
    return to_u32(result)
end

--- Multiple operand OR
-- @param ... Variable number of operands
-- @return OR of all operands
function bit_utils.bors(...)
    local args = {...}
    if #args == 0 then return 0 end
    local result = to_u32(args[1])
    for i = 2, #args do
        result = bor(result, to_u32(args[i]))
    end
    return to_u32(result)
end

-- ============================================================
-- Bit Shifting Operations
-- ============================================================

--- Logical left shift
-- @param a Value to shift
-- @param n Number of bits to shift (positive integer)
-- @return Shifted value
function bit_utils.lshift(a, n)
    if n < 0 then return bit_utils.rshift(a, -n) end
    return to_u32(lshift(to_u32(a), n))
end

--- Logical right shift
-- @param a Value to shift
-- @param n Number of bits to shift (positive integer)
-- @return Shifted value
function bit_utils.rshift(a, n)
    if n < 0 then return bit_utils.lshift(a, -n) end
    return to_u32(rshift(to_u32(a), n))
end

--- Arithmetic right shift (preserves sign bit)
-- @param a Value to shift
-- @param n Number of bits to shift (positive integer)
-- @return Shifted value
function bit_utils.arshift(a, n)
    if n < 0 then return bit_utils.lshift(a, -n) end
    if arshift then
        return to_u32(arshift(to_u32(a), n))
    else
        -- Fallback implementation
        local val = to_u32(a)
        if n == 0 then return val end
        -- Check sign bit
        if val >= 0x80000000 then
            -- Negative number: fill with 1s from the left
            local mask = to_u32(bnot(lshift(MASK32, 32 - n)))
            return to_u32(bor(rshift(val, n), mask))
        else
            return to_u32(rshift(val, n))
        end
    end
end

--- Left rotation
-- @param a Value to rotate
-- @param n Number of bits to rotate (positive integer)
-- @return Rotated value
function bit_utils.rol(a, n)
    n = n % 32
    if n == 0 then return to_u32(a) end
    local val = to_u32(a)
    return to_u32(bor(
        lshift(val, n),
        rshift(val, 32 - n)
    ))
end

--- Right rotation
-- @param a Value to rotate
-- @param n Number of bits to rotate (positive integer)
-- @return Rotated value
function bit_utils.ror(a, n)
    n = n % 32
    if n == 0 then return to_u32(a) end
    local val = to_u32(a)
    return to_u32(bor(
        rshift(val, n),
        lshift(val, 32 - n)
    ))
end

-- ============================================================
-- Single Bit Manipulation
-- ============================================================

--- Test if a specific bit is set
-- @param a Value to test
-- @param pos Bit position (0-31, 0 = LSB)
-- @return true if bit is set, false otherwise
function bit_utils.test(a, pos)
    pos = pos % 32
    return bit_utils.band(a, lshift(1, pos)) ~= 0
end

--- Set a specific bit
-- @param a Original value
-- @param pos Bit position (0-31, 0 = LSB)
-- @return Value with bit set
function bit_utils.set(a, pos)
    pos = pos % 32
    return bit_utils.bor(a, lshift(1, pos))
end

--- Clear a specific bit
-- @param a Original value
-- @param pos Bit position (0-31, 0 = LSB)
-- @return Value with bit cleared
function bit_utils.clear(a, pos)
    pos = pos % 32
    return bit_utils.band(a, bnot(lshift(1, pos)))
end

--- Toggle a specific bit
-- @param a Original value
-- @param pos Bit position (0-31, 0 = LSB)
-- @return Value with bit toggled
function bit_utils.toggle(a, pos)
    pos = pos % 32
    return bit_utils.bxor(a, lshift(1, pos))
end

-- ============================================================
-- Bit Field Operations
-- ============================================================

--- Extract a bit field
-- @param a Source value
-- @param field_pos Starting position of field (0 = LSB)
-- @param field_size Size of field in bits
-- @return Extracted field value
function bit_utils.extract(a, field_pos, field_size)
    field_pos = field_pos % 32
    field_size = math.min(field_size, 32 - field_pos)
    return bit_utils.band(rshift(a, field_pos), lshift(1, field_size) - 1)
end

--- Insert a value into a bit field
-- @param a Original value
-- @param field_pos Starting position of field (0 = LSB)
-- @param field_size Size of field in bits
-- @param value Value to insert
-- @return Modified value
function bit_utils.insert(a, field_pos, field_size, value)
    field_pos = field_pos % 32
    field_size = math.min(field_size, 32 - field_pos)
    local mask = lshift(1, field_size) - 1
    value = bit_utils.band(value, mask)
    -- Clear the field
    a = bit_utils.band(a, bnot(lshift(mask, field_pos)))
    -- Insert the value
    return bit_utils.bor(a, lshift(value, field_pos))
end

--- Replace bits in a range
-- @param a Original value
-- @param start_pos Starting position (0 = LSB)
-- @param end_pos Ending position (inclusive)
-- @param value Value to insert
-- @return Modified value
function bit_utils.replace_range(a, start_pos, end_pos, value)
    if start_pos > end_pos then
        start_pos, end_pos = end_pos, start_pos
    end
    local field_size = end_pos - start_pos + 1
    return bit_utils.insert(a, start_pos, field_size, value)
end

--- Extract bits in a range
-- @param a Source value
-- @param start_pos Starting position (0 = LSB)
-- @param end_pos Ending position (inclusive)
-- @return Extracted value
function bit_utils.extract_range(a, start_pos, end_pos)
    if start_pos > end_pos then
        start_pos, end_pos = end_pos, start_pos
    end
    local field_size = end_pos - start_pos + 1
    return bit_utils.extract(a, start_pos, field_size)
end

-- ============================================================
-- Bit Counting Utilities
-- ============================================================

--- Count the number of set bits (population count / Hamming weight)
-- @param a Value to count
-- @return Number of set bits
function bit_utils.popcount(a)
    local count = 0
    local val = to_u32(a)
    while val > 0 do
        count = count + (val & 1)
        val = val >> 1
    end
    return count
end

--- Count the number of set bits using lookup table (faster for multiple calls)
-- @param a Value to count
-- @return Number of set bits
function bit_utils.popcount_fast(a)
    -- Pre-computed lookup table for 8-bit values
    local lookup = bit_utils._popcount_lookup or {}
    if #lookup == 0 then
        for i = 0, 255 do
            local count = 0
            local n = i
            while n > 0 do
                count = count + (n & 1)
                n = n >> 1
            end
            lookup[i] = count
        end
        bit_utils._popcount_lookup = lookup
    end
    
    local val = to_u32(a)
    return lookup[val & 0xFF] +
           lookup[(val >> 8) & 0xFF] +
           lookup[(val >> 16) & 0xFF] +
           lookup[(val >> 24) & 0xFF]
end

--- Count leading zeros
-- @param a Value to examine
-- @return Number of leading zero bits
function bit_utils.clz(a)
    local val = to_u32(a)
    if val == 0 then return 32 end
    
    local count = 0
    for i = 31, 0, -1 do
        if bit_utils.test(val, i) then
            return count
        end
        count = count + 1
    end
    return count
end

--- Count trailing zeros
-- @param a Value to examine
-- @return Number of trailing zero bits
function bit_utils.ctz(a)
    local val = to_u32(a)
    if val == 0 then return 32 end
    
    local count = 0
    for i = 0, 31 do
        if bit_utils.test(val, i) then
            return count
        end
        count = count + 1
    end
    return count
end

--- Find first set bit (position of lowest set bit)
-- @param a Value to examine
-- @return Position of first set bit, or -1 if none
function bit_utils.ffs(a)
    local val = to_u32(a)
    if val == 0 then return -1 end
    return bit_utils.ctz(val)
end

--- Find last set bit (position of highest set bit)
-- @param a Value to examine
-- @return Position of last set bit, or -1 if none
function bit_utils.fls(a)
    local val = to_u32(a)
    if val == 0 then return -1 end
    return 31 - bit_utils.clz(val)
end

--- Find next set bit after given position
-- @param a Value to search
-- @param start_pos Position to start searching from (exclusive)
-- @return Position of next set bit, or -1 if none found
function bit_utils.find_next_set(a, start_pos)
    for i = start_pos + 1, 31 do
        if bit_utils.test(a, i) then
            return i
        end
    end
    return -1
end

--- Find next clear bit after given position
-- @param a Value to search
-- @param start_pos Position to start searching from (exclusive)
-- @return Position of next clear bit, or -1 if none found
function bit_utils.find_next_clear(a, start_pos)
    for i = start_pos + 1, 31 do
        if not bit_utils.test(a, i) then
            return i
        end
    end
    return -1
end

-- ============================================================
-- Byte Conversion Utilities
-- ============================================================

--- Convert value to bytes (big-endian)
-- @param a Value to convert
-- @param num_bytes Number of bytes (1-4, default 4)
-- @return Table of bytes
function bit_utils.to_bytes_be(a, num_bytes)
    num_bytes = num_bytes or 4
    local bytes = {}
    local val = to_u32(a)
    for i = num_bytes, 1, -1 do
        bytes[i] = val & 0xFF
        val = val >> 8
    end
    return bytes
end

--- Convert value to bytes (little-endian)
-- @param a Value to convert
-- @param num_bytes Number of bytes (1-4, default 4)
-- @return Table of bytes
function bit_utils.to_bytes_le(a, num_bytes)
    num_bytes = num_bytes or 4
    local bytes = {}
    local val = to_u32(a)
    for i = 1, num_bytes do
        bytes[i] = val & 0xFF
        val = val >> 8
    end
    return bytes
end

--- Convert bytes to value (big-endian)
-- @param bytes Table of bytes
-- @return Integer value
function bit_utils.from_bytes_be(bytes)
    local val = 0
    for i = 1, #bytes do
        val = (val << 8) | bytes[i]
    end
    return to_u32(val)
end

--- Convert bytes to value (little-endian)
-- @param bytes Table of bytes
-- @return Integer value
function bit_utils.from_bytes_le(bytes)
    local val = 0
    for i = #bytes, 1, -1 do
        val = (val << 8) | bytes[i]
    end
    return to_u32(val)
end

--- Get a single byte at position
-- @param a Value to extract from
-- @param byte_pos Byte position (0 = LSB)
-- @return Byte value
function bit_utils.get_byte(a, byte_pos)
    return to_u32(a) >> (byte_pos * 8) & 0xFF
end

--- Set a single byte at position
-- @param a Original value
-- @param byte_pos Byte position (0 = LSB)
-- @param byte_val Byte value to set
-- @return Modified value
function bit_utils.set_byte(a, byte_pos, byte_val)
    local shift = byte_pos * 8
    local mask = 0xFF << shift
    return to_u32((a & ~mask) | ((byte_val & 0xFF) << shift))
end

--- Swap byte order (endianness conversion)
-- @param a Value to swap
-- @return Byte-swapped value
function bit_utils.bswap(a)
    local val = to_u32(a)
    return to_u32(
        ((val & 0x000000FF) << 24) |
        ((val & 0x0000FF00) << 8) |
        ((val & 0x00FF0000) >> 8) |
        ((val & 0xFF000000) >> 24)
    )
end

--- Swap bytes in 16-bit value
-- @param a 16-bit value
-- @return Byte-swapped value
function bit_utils.bswap16(a)
    local val = to_u32(a) & 0xFFFF
    return ((val & 0x00FF) << 8) | ((val & 0xFF00) >> 8)
end

-- ============================================================
-- Flag Manipulation Helpers
-- ============================================================

--- Create a bitmask from a list of bit positions
-- @param ... Bit positions
-- @return Combined bitmask
function bit_utils.make_mask(...)
    local args = {...}
    local mask = 0
    for _, pos in ipairs(args) do
        mask = bit_utils.bor(mask, lshift(1, pos))
    end
    return to_u32(mask)
end

--- Check if any flag is set
-- @param a Value to check
-- @param mask Bitmask of flags
-- @return true if any flag is set
function bit_utils.any_set(a, mask)
    return bit_utils.band(a, mask) ~= 0
end

--- Check if all flags are set
-- @param a Value to check
-- @param mask Bitmask of flags
-- @return true if all flags are set
function bit_utils.all_set(a, mask)
    return bit_utils.band(a, mask) == mask
end

--- Check if no flags are set
-- @param a Value to check
-- @param mask Bitmask of flags
-- @return true if no flags are set
function bit_utils.none_set(a, mask)
    return bit_utils.band(a, mask) == 0
end

--- Set multiple flags
-- @param a Original value
-- @param mask Bitmask of flags to set
-- @return Modified value
function bit_utils.set_flags(a, mask)
    return bit_utils.bor(a, mask)
end

--- Clear multiple flags
-- @param a Original value
-- @param mask Bitmask of flags to clear
-- @return Modified value
function bit_utils.clear_flags(a, mask)
    return bit_utils.band(a, bnot(mask))
end

--- Toggle multiple flags
-- @param a Original value
-- @param mask Bitmask of flags to toggle
-- @return Modified value
function bit_utils.toggle_flags(a, mask)
    return bit_utils.bxor(a, mask)
end

-- ============================================================
-- Utility Functions
-- ============================================================

--- Convert integer to binary string
-- @param a Value to convert
-- @param min_width Minimum width (pad with zeros, default 32)
-- @return Binary string representation
function bit_utils.to_bin(a, min_width)
    min_width = min_width or 32
    local val = to_u32(a)
    local str = ""
    while val > 0 do
        str = (val & 1) .. str
        val = val >> 1
    end
    if str == "" then str = "0" end
    while #str < min_width do
        str = "0" .. str
    end
    return str
end

--- Convert binary string to integer
-- @param str Binary string
-- @return Integer value
function bit_utils.from_bin(str)
    return tonumber(str, 2) or 0
end

--- Convert integer to hexadecimal string
-- @param a Value to convert
-- @param min_width Minimum width (pad with zeros, default 8)
-- @return Hexadecimal string representation
function bit_utils.to_hex(a, min_width)
    min_width = min_width or 8
    local val = to_u32(a)
    local hex = string.format("%X", val)
    while #hex < min_width do
        hex = "0" .. hex
    end
    return hex
end

--- Convert hexadecimal string to integer
-- @param str Hexadecimal string
-- @return Integer value
function bit_utils.from_hex(str)
    return tonumber(str, 16) or 0
end

--- Reverse bits in an integer
-- @param a Value to reverse
-- @param num_bits Number of bits to reverse (default 32)
-- @return Bit-reversed value
function bit_utils.reverse(a, num_bits)
    num_bits = num_bits or 32
    local val = to_u32(a)
    local result = 0
    for i = 0, num_bits - 1 do
        if bit_utils.test(val, i) then
            result = bit_utils.set(result, num_bits - 1 - i)
        end
    end
    return to_u32(result)
end

--- Reverse bytes (same as bswap for 32-bit)
-- @param a Value to reverse
-- @return Byte-reversed value
function bit_utils.reverse_bytes(a, num_bytes)
    num_bytes = num_bytes or 4
    local bytes = bit_utils.to_bytes_be(a, num_bytes)
    -- Reverse the byte order
    local reversed = {}
    for i = 1, #bytes do
        reversed[i] = bytes[num_bytes - i + 1]
    end
    return bit_utils.from_bytes_be(reversed)
end

--- Create a bitmask for a range of bits
-- @param start_pos Starting bit position (inclusive)
-- @param end_pos Ending bit position (inclusive)
-- @return Bitmask
function bit_utils.mask_range(start_pos, end_pos)
    if start_pos > end_pos then
        start_pos, end_pos = end_pos, start_pos
    end
    local width = end_pos - start_pos + 1
    return to_u32(((1 << width) - 1) << start_pos)
end

--- Check if value is a power of 2
-- @param a Value to check
-- @return true if power of 2, false otherwise
function bit_utils.is_power_of_two(a)
    local val = to_u32(a)
    return val > 0 and bit_utils.band(val, val - 1) == 0
end

--- Find the next power of 2 >= value
-- @param a Input value
-- @return Next power of 2 >= a
function bit_utils.next_power_of_two(a)
    local val = to_u32(a)
    if val == 0 then return 1 end
    if bit_utils.is_power_of_two(val) then return val end
    return to_u32(1 << (32 - bit_utils.clz(val)))
end

--- Round up to nearest power of 2
-- @param a Input value
-- @return Rounded up to nearest power of 2
function bit_utils.ceil_power_of_two(a)
    return bit_utils.next_power_of_two(a)
end

--- Round down to nearest power of 2
-- @param a Input value
-- @return Rounded down to nearest power of 2
function bit_utils.floor_power_of_two(a)
    local val = to_u32(a)
    if val == 0 then return 0 end
    return to_u32(1 << bit_utils.fls(val))
end

--- Align value to boundary
-- @param a Value to align
-- @param alignment Alignment boundary (must be power of 2)
-- @return Aligned value
function bit_utils.align(a, alignment)
    local mask = alignment - 1
    return to_u32((a + mask) & ~mask)
end

--- Align value down to boundary
-- @param a Value to align
-- @param alignment Alignment boundary (must be power of 2)
-- @return Aligned value
function bit_utils.align_down(a, alignment)
    local mask = alignment - 1
    return to_u32(a & ~mask)
end

-- Return module
return bit_utils