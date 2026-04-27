# Iban Utils


IBAN (International Bank Account Number) Utilities
==================================================

A comprehensive implementation for validating, parsing, and formatting
IBAN (International Bank Account Number) used in international banking.

IBAN is an internationally agreed system for identifying bank accounts
across national borders. It consists of:
- 2-letter country code
- 2 check digits
- Basic Bank Account Number (BBAN) - country-specific format

Features:
- Validate IBAN format and check digits
- Parse IBAN into components (country, check digits, BBAN)
- Extract country-specific bank information
- Format IBAN with different display formats
- Generate valid test IBANs
- Zero external dependencies

Reference: ISO 13616 / SWIFT IBAN Registry


## 功能

### 类

- **IBANValidator**: A class-based validator for IBAN numbers
  方法: validate, parse, format, strip, get_country ... (7 个方法)

### 函数

- **strip_formatting(iban**) - Remove all non-alphanumeric characters from an IBAN.
- **validate(iban**) - Validate an IBAN (format and check digits).
- **validate_check_digits(iban**) - Validate IBAN check digits using the MOD-97 algorithm.
- **calculate_check_digits(country_code, bban**) - Calculate the check digits for an IBAN given country code and BBAN.
- **parse(iban**) - Parse an IBAN into its components.
- **format_iban(iban, group_size, separator**) - Format an IBAN by grouping characters.
- **get_country_info(country_code**) - Get IBAN structure information for a country.
- **get_supported_countries(**) - Get a list of all supported country codes.
- **generate_test_iban(country_code**) - Generate a valid test IBAN for a given country.
- **generate_batch_test_ibans(country_code, count**) - Generate multiple test IBANs for a country.

... 共 18 个函数

## 使用示例

```python
from mod import strip_formatting

# 使用 strip_formatting
result = strip_formatting()
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
