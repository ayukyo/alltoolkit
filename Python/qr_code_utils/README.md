# Qr Code Utils


AllToolkit - Python QR Code Utilities

A zero-dependency, production-ready QR Code generation utility module.
Supports QR Code encoding with multiple error correction levels and versions.
Can output as text (ASCII art), SVG, or raw data matrix.

Author: AllToolkit
License: MIT


## 功能

### 类

- **ErrorCorrectionLevel**: QR Code error correction levels
- **QRMode**: QR Code encoding modes
- **QRCodeUtils**: QR Code generation utilities
  方法: encode, validate, get_capacity, is_valid_qr_string
- **QRCode**: Represents an encoded QR Code
  方法: to_ascii, to_compact_ascii, to_unicode, to_svg, to_bitmap ... (7 个方法)

### 函数

- **encode(data, ec_level, version**) - Encode data into a QR Code.
- **validate(data**) - Check if data can be encoded as QR Code.
- **get_capacity(version, ec_level**) - Get the maximum data capacity for a given version and error correction level.
- **is_valid_qr_string(qr_string**) - Check if a string is a valid QR Code representation.
- **encode(data, ec_level, version**) - Encode data into a QR Code.
- **validate(data**) - Check if data can be encoded as QR Code.
- **get_capacity(version, ec_level**) - Get the maximum data capacity for a given version and error correction level.
- **is_valid_qr_string(qr_string**) - Check if a string is a valid QR Code representation.
- **to_ascii(self, border, black**, ...) - Convert QR Code to ASCII art string.
- **to_compact_ascii(self, border**) - Convert QR Code to compact ASCII art (using half blocks).

... 共 15 个函数

## 使用示例

```python
from mod import encode

# 使用 encode
result = encode()
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
