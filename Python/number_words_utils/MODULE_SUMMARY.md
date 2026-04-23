# Number Words Utils Module Summary

## Module Information
- **Module Name:** number_words_utils
- **Language:** Python
- **Created:** 2026-04-24
- **Dependencies:** Zero (pure Python standard library)

## Core Functions

### Number to Words Conversion
| Function | Description |
|----------|-------------|
| `number_to_words(number, language, ordinal)` | Convert number to word representation |
| `to_words(number, language, ordinal)` | Convenience alias for number_to_words |

### Words to Number Conversion
| Function | Description |
|----------|-------------|
| `words_to_number(words, language)` | Convert word representation to number |
| `from_words(words, language)` | Convenience alias for words_to_number |

### Currency Conversion
| Function | Description |
|----------|-------------|
| `number_to_currency_words(amount, currency, language)` | Convert currency amount to words |

### Utility Functions
| Function | Description |
|----------|-------------|
| `is_valid_number_word(word, language)` | Check if word is valid number word |
| `get_number_words_list(language)` | Get all valid number words for language |

## Supported Languages
- English (`Language.ENGLISH` or `"en"`)
- Chinese (`Language.CHINESE` or `"zh"`)

## Supported Currencies
- USD (US Dollars)
- EUR (Euros)
- GBP (British Pounds)
- CNY (Chinese Yuan)
- JPY (Japanese Yen)

## Features
1. **Number to Words**: Convert any integer/float to words
2. **Words to Number**: Parse words back to numbers
3. **Ordinal Numbers**: Convert to ordinal form (1 → "first", 第123)
4. **Decimal Handling**: Support for floating-point numbers
5. **Negative Numbers**: Handle negative values with "minus"/"负" prefix
6. **Large Numbers**: Support up to quintillion (10^18)
7. **Currency Format**: Convert monetary amounts with proper singular/plural
8. **Round-trip Accuracy**: Number → words → number preserves value

## Test Coverage
- 69 unit tests covering:
  - Basic conversions (0, ones, teens, tens)
  - Hundreds, thousands, millions, billions
  - Large numbers (up to quintillion)
  - Negative numbers
  - Decimal/floating-point numbers
  - Ordinal numbers (simple and compound)
  - Chinese number conversions
  - Currency conversions
  - Round-trip accuracy tests
  - Edge cases and error handling

## Example Usage

```python
from number_words_utils.mod import number_to_words, words_to_number, Language

# English
number_to_words(1234567)  # "one million two hundred thirty-four thousand five hundred sixty-seven"
number_to_words(21, ordinal=True)  # "twenty-first"
words_to_number("one hundred twenty-three")  # 123

# Chinese
number_to_words(12345, Language.CHINESE)  # "一万二千三百四十五"
number_to_words(100, Language.CHINESE, ordinal=True)  # "第一百"
words_to_number("一百二十三", Language.CHINESE)  # 123

# Currency
number_to_currency_words(123.45, "USD")  # "one hundred twenty-three dollars and forty-five cents"
number_to_currency_words(123.45, "CNY", Language.CHINESE)  # "一百二十三元四十五分"
```

## Implementation Notes
- Uses Python standard library only (no external dependencies)
- Handles floating-point precision issues by formatting decimals
- Supports both hyphenated and space-separated number words
- Implements Chinese number conventions (十 vs 一十)
- Language enum for type-safe language selection