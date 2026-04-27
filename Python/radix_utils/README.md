# Radix Utils


AllToolkit - Python Radix (Base) Conversion Utilities

A zero-dependency, production-ready radix conversion utility module.
Supports conversion between arbitrary bases (2-36), including binary,
octal, decimal, and hexadecimal, with support for fractions and negative numbers.

Author: AllToolkit
License: MIT


## 功能

### 类

- **RadixUtils**: Radix (base) conversion utilities
  方法: validate_base, validate_digits, to_decimal, from_decimal, convert ... (21 个方法)

### 函数

- **to_decimal(number_str, from_base**) - Convert a number from any base to decimal.
- **from_decimal(decimal, to_base, precision**) - Convert a decimal number to any base.
- **convert(number_str, from_base, to_base**, ...) - Convert a number from one base to another.
- **to_binary(number_str, from_base**) - Convert a number to binary.
- **from_binary(binary_str, to_base**) - Convert a binary number to another base.
- **to_octal(number_str, from_base**) - Convert a number to octal.
- **from_octal(octal_str, to_base**) - Convert an octal number to another base.
- **to_hex(number_str, from_base, uppercase**) - Convert a number to hexadecimal.
- **from_hex(hex_str, to_base**) - Convert a hexadecimal number to another base.
- **to_base36(number_str, from_base**) - Convert a number to base 36.

... 共 35 个函数

## 使用示例

```python
from mod import to_decimal

# 使用 to_decimal
result = to_decimal()
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
