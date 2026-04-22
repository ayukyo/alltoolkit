# Luhn Algorithm Utilities

A comprehensive implementation of the Luhn algorithm (also known as the "modulus 10" or "mod 10" algorithm) for validating and generating check digits.

## Features

- **Validate numbers** using Luhn algorithm
- **Calculate check digits** for partial numbers
- **Generate valid test numbers** with custom prefixes
- **Format and parse numbers** with flexible formatting options
- **Identify card types** by number prefix
- **Find digit errors** in invalid numbers
- **Class-based API** for convenient usage

## Use Cases

The Luhn algorithm is used for validating:
- Credit card numbers
- IMEI numbers (International Mobile Equipment Identity)
- National Provider Identifier numbers (US healthcare)
- Canadian Social Insurance Numbers
- Greek Social Security Numbers (AMKA)
- South African ID numbers
- And many other identification numbers

## Installation

No external dependencies required. Pure Python implementation.

```python
from luhn_utils.mod import validate, generate_valid_number
```

## Quick Start

### Validation

```python
from luhn_utils.mod import validate

# Valid Visa card
validate("4532015112830366")  # True

# Invalid number
validate("4532015112830367")  # False

# With formatting
validate("4532-0151-1283-0366")  # True
```

### Check Digit Calculation

```python
from luhn_utils.mod import calculate_check_digit, add_check_digit

# Calculate check digit
check_digit = calculate_check_digit("453201511283036")  # 6

# Add check digit to get full valid number
full_number = add_check_digit("453201511283036")  # "4532015112830366"
```

### Generate Test Numbers

```python
from luhn_utils.mod import generate_valid_number, generate_test_credit_cards

# Generate Visa-like number
visa = generate_valid_number("4", 16)

# Generate MasterCard-like number
mc = generate_valid_number("55", 16)

# Generate test cards for all major card types
cards = generate_test_credit_cards(count=3)
for card_type, number in cards:
    print(f"{card_type}: {number}")
```

### Formatting

```python
from luhn_utils.mod import format_number, strip_formatting

# Format with default spacing
format_number("4532015112830366")  # "4532 0151 1283 0366"

# Format with dashes
format_number("4532015112830366", separator="-")  # "4532-0151-1283-0366"

# Strip formatting
strip_formatting("4532-0151-1283-0366")  # "4532015112830366"
```

### Card Type Identification

```python
from luhn_utils.mod import identify_card_type

identify_card_type("4111111111111111")  # "visa"
identify_card_type("5500000000000004")  # "mastercard"
identify_card_type("378282246310005")   # "amex"
```

### Class-Based API

```python
from luhn_utils.mod import LuhnValidator

validator = LuhnValidator()

# Validate
validator.validate("4532015112830366")  # True

# Generate
validator.generate("4", 16)  # Returns valid Visa-like number

# Format
validator.format("4532015112830366")  # "4532 0151 1283 0366"

# Batch generation
numbers = validator.generate_batch("4", 10, 16)
```

## API Reference

### Functions

| Function | Description |
|----------|-------------|
| `validate(number)` | Validate a number using Luhn algorithm |
| `calculate_check_digit(number)` | Calculate the Luhn check digit |
| `add_check_digit(number)` | Append check digit to a number |
| `strip_formatting(number)` | Remove non-digit characters |
| `format_number(number, group_size, separator)` | Format number with grouping |
| `generate_valid_number(prefix, length)` | Generate valid Luhn number |
| `generate_test_credit_cards(count)` | Generate test credit cards |
| `identify_card_type(number)` | Identify card type by prefix |
| `find_check_digit_errors(number)` | Find potential error positions |
| `calculate_luhn_sum(number)` | Calculate Luhn sum and validity |

### Classes

| Class | Description |
|-------|-------------|
| `LuhnValidator` | Class-based validator with convenient methods |

### Constants

| Constant | Description |
|----------|-------------|
| `CARD_PREFIXES` | Dictionary of known card type prefixes |

## Testing

Run the test suite:

```bash
cd Python && python luhn_utils/luhn_utils_test.py
```

Run the examples:

```bash
cd Python && python luhn_utils/examples/usage_examples.py
```

## License

MIT License - Part of AllToolkit project.