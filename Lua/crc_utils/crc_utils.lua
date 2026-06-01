--[[
    crc_utils.lua - CRC (Cyclic Redundancy Check) Implementation for Lua
    
    A pure Lua implementation of CRC calculations with zero external dependencies.
    Supports common CRC variants: CRC-8, CRC-16, CRC-32, CRC-64.
    
    Features:
    - CRC-8 (CCITT, Dallas/Maxim, SAE-J1850)
    - CRC-16 (CCITT, Modbus, USB, XModem)
    - CRC-32 (IEEE 802.3)
    - CRC-64 (ECMA-182, ISO/IEC 3309)
    - String and byte array input support
    - Verification and hex formatting helpers
    
    License: MIT
    Author: AllToolkit
    Version: 1.0.0
]]

local crc_utils = {}

-- CRC-32 using direct calculation (no lookup table for simplicity)
function crc_utils.crc32(data)
    local poly = 0xEDB88320
    local crc = 0xFFFFFFFF
    local bytes
    
    if type(data) == "string" then
        bytes = {}
        for i = 1, #data do
            bytes[i] = string.byte(data, i)
        end
    else
        bytes = data
    end
    
    for _, byte in ipairs(bytes) do
        crc = crc ~ byte
        for _ = 1, 8 do
            if crc % 2 == 1 then
                crc = math.floor(crc / 2) ~ poly
            else
                crc = math.floor(crc / 2)
            end
        end
    end
    
    return crc ~ 0xFFFFFFFF
end

-- CRC-16-CCITT (standard)
function crc_utils.crc16(data, variant)
    variant = variant or "CCITT"
    local poly, init
    
    if variant == "MODBUS" then
        poly = 0x8005
        init = 0xFFFF
    elseif variant == "USB" then
        poly = 0x8005
        init = 0xFFFF
    elseif variant == "XMODEM" then
        poly = 0x1021
        init = 0x0000
    else -- CCITT
        poly = 0x1021
        init = 0xFFFF
    end
    
    local crc = init
    local bytes
    
    if type(data) == "string" then
        bytes = {}
        for i = 1, #data do
            bytes[i] = string.byte(data, i)
        end
    else
        bytes = data
    end
    
    for _, byte in ipairs(bytes) do
        crc = crc ~ byte
        for _ = 1, 8 do
            if crc % 2 == 1 then
                crc = math.floor(crc / 2) ~ poly
            else
                crc = math.floor(crc / 2)
            end
        end
    end
    
    if variant == "USB" then
        crc = crc ~ 0xFFFF
    end
    
    return crc % 0x10000
end

-- CRC-8
function crc_utils.crc8(data, variant)
    variant = variant or "CCITT"
    local poly, init
    
    if variant == "DALLAS" then
        poly = 0x31
        init = 0x00
    elseif variant == "SAE_J1850" then
        poly = 0x1D
        init = 0xFF
    else -- CCITT
        poly = 0x07
        init = 0x00
    end
    
    local crc = init
    local bytes
    
    if type(data) == "string" then
        bytes = {}
        for i = 1, #data do
            bytes[i] = string.byte(data, i)
        end
    else
        bytes = data
    end
    
    for _, byte in ipairs(bytes) do
        crc = crc ~ byte
        for _ = 1, 8 do
            if crc % 2 == 1 then
                crc = math.floor(crc / 2) ~ poly
            else
                crc = math.floor(crc / 2)
            end
        end
    end
    
    return crc % 0x100
end

-- CRC-64
function crc_utils.crc64(data, variant)
    variant = variant or "ECMA"
    local poly = variant == "ISO" and 0x1B or 0x42F0E1EBA9EA3693
    
    local crc = 0
    local bytes
    
    if type(data) == "string" then
        bytes = {}
        for i = 1, #data do
            bytes[i] = string.byte(data, i)
        end
    else
        bytes = data
    end
    
    for _, byte in ipairs(bytes) do
        crc = crc ~ byte
        for _ = 1, 8 do
            if crc % 2 == 1 then
                crc = math.floor(crc / 2) ~ poly
            else
                crc = math.floor(crc / 2)
            end
        end
    end
    
    return crc
end

-- Generic checksum
function crc_utils.checksum(data, algorithm)
    algorithm = algorithm or "crc32"
    if algorithm == "crc8" then return crc_utils.crc8(data)
    elseif algorithm == "crc16" then return crc_utils.crc16(data)
    elseif algorithm == "crc32" then return crc_utils.crc32(data)
    elseif algorithm == "crc64" then return crc_utils.crc64(data)
    else error("Unknown algorithm: " .. algorithm) end
end

-- Verify data against expected CRC
function crc_utils.verify(data, expected, algorithm)
    return crc_utils.checksum(data, algorithm) == expected
end

-- Format CRC as hex string
function crc_utils.to_hex(crc, width)
    width = width or 32
    if width == 8 then return string.format("%02X", crc % 0x100)
    elseif width == 16 then return string.format("%04X", crc % 0x10000)
    elseif width == 32 then return string.format("%08X", crc)
    else return string.format("%016X", crc) end
end

return crc_utils