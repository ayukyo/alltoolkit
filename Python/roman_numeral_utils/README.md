# Roman Numeral Utilities

A comprehensive Python library for converting between Arabic numerals and Roman numerals. Zero external dependencies.

## Features

- **Integer to Roman**: Convert integers (1-3999) to Roman numeral strings
- **Roman to Integer**: Parse Roman numerals back to integers
- **Validation**: Check if strings are valid Roman numerals
- **Text Parsing**: Extract Roman numerals from text
- **Arithmetic**: Add, subtract, and compare Roman numerals
- **Range Generation**: Generate Roman numeral sequences

## Installation

No installation required - just copy the `mod.py` file to your project.

## Quick Start

```python
from roman_numeral_utils.mod import to_roman, from_roman

# Convert to Roman
print(to_roman(1994))  # 'MCMXCIV'

# Convert from Roman
print(from_roman('MCMXCIV'))  # 1994
```

## API Reference

### Core Functions

#### `to_roman(num: int) -> str`
Convert an integer to a Roman numeral (1-3999).

```python
to_roman(1)      # 'I'
to_roman(4)      # 'IV'
to_roman(1994)   # 'MCMXCIV'
```

#### `from_roman(roman: str) -> int`
Convert a Roman numeral to an integer.

```python
from_roman('I')        # 1
from_roman('IV')        # 4
from_roman('MCMXCIV')   # 1994
```

### Validation

#### `is_valid_roman(roman: str) -> bool`
Check if a string is a valid Roman numeral.

```python
is_valid_roman('IV')    # True
is_valid_roman('IIII')  # False (invalid notation)
```

### Text Parsing

#### `parse_roman_in_text(text: str) -> List[Tuple[str, int, int, int]]`
Find and parse all Roman numerals in text. Returns list of (roman, value, start, end).

```python
text = "King Henry VIII ruled England"
parsed = parse_roman_in_text(text)
# [('VIII', 8, 12, 16)]
```

### Arithmetic

#### `add_roman(roman1: str, roman2: str) -> str`
Add two Roman numerals.

```python
add_roman('X', 'V')   # 'XV'
add_roman('IV', 'I')  # 'V'
```

#### `subtract_roman(roman1: str, roman2: str) -> str`
Subtract two Roman numerals.

```python
subtract_roman('X', 'V')  # 'V'
subtract_roman('V', 'I')  # 'IV'
```

#### `compare_roman(roman1: str, roman2: str) -> int`
Compare two Roman numerals. Returns -1, 0, or 1.

```python
compare_roman('I', 'V')   # -1 (I < V)
compare_roman('V', 'V')   # 0  (V == V)
compare_roman('X', 'V')   # 1  (X > V)
```

### Utilities

#### `roman_range(start: int, end: int, step: int = 1) -> Generator[str]`
Generate Roman numerals in a range.

```python
list(roman_range(1, 6))  # ['I', 'II', 'III', 'IV', 'V']
```

#### `get_roman_info(roman: str) -> dict`
Get detailed information about a Roman numeral.

```python
info = get_roman_info('MCMXCIV')
# {
#     'roman': 'MCMXCIV',
#     'valid': True,
#     'value': 1994,
#     'length': 7,
#     'characters': ['M', 'C', 'M', 'X', 'C', 'I', 'V'],
#     'breakdown': [...]
# }
```

#### `format_with_ordinal(num: int, use_roman: bool = True) -> str`
Format a number as Roman numeral or with ordinal suffix.

```python
format_with_ordinal(1)                 # 'I'
format_with_ordinal(1, use_roman=False)  # '1st'
format_with_ordinal(3, use_roman=False)  # '3rd'
```

## Constants

- `ROMAN_ONES`: Roman numerals for 1-10 (I, II, III, IV, V, VI, VII, VIII, IX, X)
- `ROMAN_TENS`: Roman numerals for 10-100 by tens
- `ROMAN_HUNDREDS`: Roman numerals for 100-1000 by hundreds

## Examples

Run the example files:

```bash
python examples/basic_conversion.py
python examples/arithmetic.py
python examples/text_parsing.py
```

## Testing

Run the test suite:

```bash
python roman_numeral_utils_test.py
```

## Roman Numeral Rules

Standard Roman numerals use the following symbols:
- I = 1
- V = 5
- X = 10
- L = 50
- C = 100
- D = 500
- M = 1000

Subtractive notation:
- IV = 4 (not IIII)
- IX = 9
- XL = 40
- XC = 90
- CD = 400
- CM = 900

Valid range: 1 to 3999 (MMMCMXCIX)

## License

MIT License - Free to use and modify.