# Credit Card Utils


AllToolkit - Credit Card Utilities Module
==========================================
A comprehensive credit card utility module for Python with zero external dependencies.

Features:
    - Credit card number validation using Luhn algorithm
    - Card type detection (Visa, MasterCard, Amex, Discover, etc.)
    - Card number formatting and masking
    - Test card number generation
    - CVV and expiry date validation
    - BIN/IIN lookup support

Author: AllToolkit Contributors
License: MIT


## 功能

### 函数

- **luhn_check(card_number**) - Validate a card number using the Luhn algorithm.
- **calculate_luhn_check_digit(partial_number**) - Calculate the Luhn check digit for a partial card number.
- **validate_card(card_number**) - Comprehensive validation of a credit card number.
- **is_valid_card(card_number**) - Quick check if a card number is valid.
- **detect_card_type(card_number**) - Detect the card type from a card number.
- **get_card_info(card_type**) - Get detailed information about a card type.
- **get_all_card_types(**) - Get a list of all supported card types.
- **format_card(card_number, separator**) - Format a card number with separators for readability.
- **mask_card(card_number, show_first, show_last**, ...) - Mask a card number for secure display.
- **mask_card_formatted(card_number, show_first, show_last**, ...) - Mask a card number with formatting.

... 共 20 个函数

## 使用示例

```python
from mod import luhn_check

# 使用 luhn_check
result = luhn_check()
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
