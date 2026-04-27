# Crc Utils


AllToolkit - CRC (Cyclic Redundancy Check) Utilities Module
============================================================
A comprehensive CRC computation and validation utility module for Python
with zero external dependencies.

Features:
    - CRC-8, CRC-16, CRC-32, CRC-64 computation
    - Multiple standard CRC algorithms
    - Custom CRC polynomial support
    - File CRC computation
    - Data integrity verification
    - CRC table generation for performance
    - Bit reflection utilities
    - Hex and integer CRC output

Supported Algorithms:
    - CRC-8 (poly 0x07)
    - CRC-8-CCITT (poly 0x07)
    - CRC-8-MAXIM (poly 0x31)
    - CRC-16-IBM (poly 0x8005)
    - CRC-16-CCITT (poly 0x1021)
    - CRC-16-MODBUS (poly 0x8005)
    - CRC-32 (poly 0x04C11DB7) - same as zlib.crc32
    - CRC-32C (poly 0x1EDC6F41) - Castagnoli
    - CRC-64-ECMA (poly 0x42F0E1EBA9EA3693)
    - CRC-64-ISO (poly 0x000000000000001B)

Author: AllToolkit Contributors
License: MIT


## 功能

### 类

- **CRC**: CRC calculator class supporting multiple algorithms
  方法: width, algorithm, polynomial, update, value ... (17 个方法)

### 函数

- **reflect_bits(value, width**) - Reflect (reverse) the bits in a value.
- **reflect_bits_fast(value, width**) - Fast bit reflection using byte table.
- **crc32(data**) - Compute CRC-32 checksum (compatible with zlib.crc32).
- **crc16_ccitt(data**) - Compute CRC-16-CCITT checksum (reflected variant).
- **crc16_modbus(data**) - Compute CRC-16-MODBUS checksum.
- **crc16(data, poly, init**) - Compute CRC-16 checksum (non-reflected).
- **crc8(data**) - Compute CRC-8 checksum.
- **crc64(data**) - Compute CRC-64-ECMA checksum.
- **file_crc(file_path, algorithm, chunk_size**) - Compute CRC of a file.
- **verify_file_crc(file_path, expected, algorithm**) - Verify file CRC against expected value.

... 共 34 个函数

## 使用示例

```python
from mod import reflect_bits

# 使用 reflect_bits
result = reflect_bits()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
