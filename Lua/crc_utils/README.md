# crc_utils.lua

CRC (Cyclic Redundancy Check) calculation library for Lua with zero external dependencies.

## Features

- **CRC-8 variants**: CCITT, Dallas/Maxim, SAE-J1850
- **CRC-16 variants**: CCITT, Modbus, USB, XModem
- **CRC-32**: IEEE 802.3 standard
- **CRC-64 variants**: ECMA-182, ISO/IEC 3309
- **String or byte array input**
- **Verification helper**
- **Hex formatting**

## Usage

```lua
local crc = require("crc_utils")

-- CRC-32 (most common)
local data = "Hello, World!"
local hash = crc.crc32(data)
print(crc.to_hex(hash, 32))  -- "0x8C251F71"

-- CRC-16 with variant
local hash16 = crc.crc16(data, "CCITT")
print(crc.to_hex(hash16, 16))  -- "0xB4E6"

-- CRC-8 with variant
local hash8 = crc.crc8(data, "DALLAS")
print(crc.to_hex(hash8, 8))  -- "0x15"

-- CRC-64
local hash64 = crc.crc64(data, "ECMA")
print(crc.to_hex(hash64, 64))  -- "0xB47E8C43D4C0F6A3"

-- Verify data integrity
local expected = 0x8C251F71
local valid = crc.verify(data, expected, "crc32")
print(valid and "OK" or "Corrupted")
```

## Supported Variants

| Type | Variants |
|------|----------|
| CRC-8 | CCITT, DALLAS, SAE_J1850 |
| CRC-16 | CCITT, MODBUS, USB, XMODEM |
| CRC-32 | IEEE 802.3 (default) |
| CRC-64 | ECMA, ISO |

## License

MIT