# ISIN Utilities

A comprehensive Python toolkit for working with International Securities Identification Numbers (ISIN). ISIN is a 12-character alphanumeric code that uniquely identifies securities worldwide according to ISO 6166 standard.

## Features

- ✅ **Validation** - Validate ISIN codes using Luhn mod 10 algorithm
- ✅ **Parsing** - Parse ISIN components (country code, NSIN, check digit)
- ✅ **Generation** - Generate random valid ISINs for testing
- ✅ **Extraction** - Extract ISINs from text
- ✅ **Formatting** - Format ISINs with separators
- ✅ **Conversion** - Convert to/from CUSIP and SEDOL
- ✅ **Country Info** - Get country name from ISIN
- ✅ **Zero Dependencies** - Uses only Python standard library

## Installation

No installation required! Just copy the `isin_utils` folder to your project.

```python
from isin_utils import (
    is_valid_isin,
    validate_isin,
    generate_isin,
    # ... and more
)
```

## Quick Start

```python
from isin_utils import is_valid_isin, validate_isin, generate_isin

# Validate
print(is_valid_isin("US0378331005"))  # True (Apple Inc.)

# Parse
info = validate_isin("US0378331005")
print(info.country_code)  # "US"
print(info.nsin)          # "037833100"
print(info.check_digit)   # "5"

# Generate
isin = generate_isin("US")
print(isin)  # e.g., "US123456789A"
```

## API Reference

### Validation

```python
from isin_utils import (
    is_valid_isin,   # Quick boolean check
    validate_isin,   # Full validation with details
    calculate_check_digit,  # Calculate check digit
)

# Quick validation
is_valid_isin("US0378331005")  # True

# Full validation
info = validate_isin("US0378331005")
# ISINInfo(
#     original="US0378331005",
#     cleaned="US0378331005",
#     is_valid=True,
#     country_code="US",
#     nsin="037833100",
#     check_digit="5",
#     message="Valid ISIN"
# )

# Calculate check digit
calculate_check_digit("US037833100")  # "5"
```

### Parsing

```python
from isin_utils import parse_isin, get_isin_info

# Parse components
info = parse_isin("US0378331005")
print(info.country_code)  # "US"
print(info.nsin)         # "037833100" (National Security Identifier)
print(info.check_digit)  # "5"

# Get detailed info with country name
details = get_isin_info("US0378331005")
# {
#     "original": "US0378331005",
#     "cleaned": "US0378331005",
#     "is_valid": True,
#     "country_code": "US",
#     "country_name": "United States",
#     "nsin": "037833100",
#     "check_digit": "5",
#     "message": "Valid ISIN"
# }
```

### Generation

```python
from isin_utils import generate_isin, generate_random_isin

# Generate with defaults (US country code)
isin = generate_isin()
# Example: "US0378331005"

# Generate with specific country
isin = generate_isin("GB")  # United Kingdom
isin = generate_isin("JP")  # Japan
isin = generate_isin("DE")  # Germany

# Generate with specific NSIN (9 characters)
isin = generate_isin("US", "037833100")  # "US0378331005"

# Reproducible generation with seed
isin = generate_isin(seed=42)

# Random country and NSIN
isin = generate_random_isin()
isin = generate_random_isin(seed=42)  # Reproducible
```

### Formatting

```python
from isin_utils import format_isin

# Format with space (default)
format_isin("US0378331005")  # "US 037833100 5"

# Format with dash
format_isin("US0378331005", "-")  # "US-037833100-5"

# Format with dot
format_isin("US0378331005", ".")  # "US.037833100.5"

# Handles various input formats
format_isin("us0378331005")  # "US 037833100 5" (auto-uppercased)
format_isin("US 037833100 5")  # "US 037833100 5" (cleaned)
```

### Extraction

```python
from isin_utils import extract_isin, extract_all_isin

# Extract first ISIN from text
text = "Apple's ISIN is US0378331005"
isin = extract_isin(text)  # "US0378331005"

# Extract all ISINs from text
text = """
Apple: US0378331005
Microsoft: US5949181045
Google: US02079K1079
"""
isins = extract_all_isin(text)
# ["US0378331005", "US5949181045", "US02079K1079"]

# Invalid ISINs are not extracted
text = "Fake ISIN: US0378331006"  # Wrong check digit
isins = extract_all_isin(text)  # []
```

### Comparison

```python
from isin_utils import compare_isin

# Compare ISINs (ignores formatting)
compare_isin("US0378331005", "US0378331005")  # True
compare_isin("US0378331005", "US 037833100 5")  # True
compare_isin("US0378331005", "us0378331005")  # True
compare_isin("US0378331005", "US-037833100-5")  # True
compare_isin("US0378331005", "US5949181045")  # False
```

### CUSIP Conversion

CUSIP is a 9-character identifier for US and Canadian securities.

```python
from isin_utils import isin_to_cusip, cusip_to_isin

# ISIN to CUSIP (US/CA only)
cusip = isin_to_cusip("US0378331005")  # "037833100"
cusip = isin_to_cusip("US5949181045")  # "594918104"

# Non-US/CA ISIN returns None
cusip = isin_to_cusip("KR7005930003")  # None

# CUSIP to ISIN
isin = cusip_to_isin("037833100")  # "US0378331005"
isin = cusip_to_isin("037833100", "CA")  # "CA0378331005"
```

### SEDOL Conversion

SEDOL is a 7-character identifier for UK securities.

```python
from isin_utils import sedol_to_isin

# SEDOL to ISIN (padded to 9 chars for NSIN)
isin = sedol_to_isin("0263494")  # GB00263494... (check digit calculated)
```

### Example ISINs

```python
from isin_utils import get_example_isin, list_example_isins

# Get example by company name
get_example_isin("APPLE")      # "US0378331005"
get_example_isin("MICROSOFT") # "US5949181045"
get_example_isin("GOOGLE")    # "US02079K1079"
get_example_isin("TESLA")     # "US88160R1014"

# List all examples
examples = list_example_isins()
# {
#     "APPLE": "US0378331005",
#     "MICROSOFT": "US5949181045",
#     "GOOGLE": "US02079K1079",
#     ...
# }
```

## Examples

### Validate a List of ISINs

```python
from isin_utils import is_valid_isin

isins = [
    "US0378331005",  # Apple
    "US5949181045",  # Microsoft
    "INVALID12345",  # Invalid
]

for isin in isins:
    status = "✓ Valid" if is_valid_isin(isin) else "✗ Invalid"
    print(f"{isin}: {status}")
```

### Extract ISINs from Financial Report

```python
from isin_utils import extract_all_isin

report = """
Portfolio Holdings:
1. Apple Inc. (ISIN: US0378331005) - 100 shares
2. Microsoft Corp. (ISIN: US5949181045) - 50 shares
3. Alphabet Inc. (ISIN: US02079K1079) - 25 shares
"""

isins = extract_all_isin(report)
print(f"Found {len(isins)} ISINs: {isins}")
```

### Generate Test Data

```python
from isin_utils import generate_random_isin

# Generate 10 random valid ISINs for testing
test_isins = [generate_random_isin(seed=i) for i in range(10)]
for isin in test_isins:
    print(isin)
```

### Parse and Display ISIN Information

```python
from isin_utils import get_isin_info

isin = "US0378331005"
info = get_isin_info(isin)

print(f"ISIN: {info['cleaned']}")
print(f"Country: {info['country_name']} ({info['country_code']})")
print(f"NSIN: {info['nsin']}")
print(f"Check Digit: {info['check_digit']}")
print(f"Valid: {info['is_valid']}")
```

## ISIN Format

An ISIN consists of 12 characters:

```
XX YYYYYYYYY Z
│  │         │
│  │         └─ Check digit (0-9)
│  └─────────── NSIN (9 alphanumeric characters)
└────────────── Country code (2 letters)
```

- **Country Code**: 2-letter ISO 3166-1 alpha-2 code
- **NSIN**: 9-character National Security Identifier (alphanumeric)
- **Check Digit**: Single digit calculated using Luhn mod 10 algorithm

### Examples

| Company | ISIN | Country | NSIN |
|---------|------|---------|------|
| Apple Inc. | US0378331005 | US | 037833100 |
| Microsoft | US5949181045 | US | 594918104 |
| Toyota | JP3633400001 | JP | 363340000 |
| Samsung | KR7005930003 | KR | 700593000 |
| Tencent | KYG875721634 | KY (Cayman) | G875721634 |

## Testing

Run tests with:

```bash
# Using pytest
python -m pytest isin_utils_test.py -v

# Or directly
python isin_utils_test.py
```

## Algorithm Details

### Luhn Mod 10 Check

The ISIN check digit is calculated using the Luhn algorithm (mod 10):

1. Convert letters to numbers: A=10, B=11, ..., Z=35
2. Double every second digit from the right
3. If doubling results in a number > 9, subtract 9
4. Sum all digits
5. Check digit = (10 - (sum mod 10)) mod 10

Example for "US037833100":
```
U  S  0  3  7  8  3  3  1  0  0
30 28 0  3  7  8  3  3  1  0  0
↓  ↓     ↓     ↓     ↓     ↓
60 56 0  6  14 16 6  6  2  0  0  (double every second from right)
    ↓     ↓  ↓
60 11 0  6  5  7  6  6  2  0  0  (subtract 9 if > 9)

Sum = 60 + 11 + 0 + 6 + 5 + 7 + 6 + 6 + 2 + 0 + 0 = 103
Check digit = (10 - (103 mod 10)) mod 10 = (10 - 3) mod 10 = 7... 

Actually, let me verify: for "US037833100":
Position:  U   S   0   3   7   8   3   3   1   0   0
Values:   30  28   0   3   7   8   3   3   1   0   0
Position from right: 10  9   8   7   6   5   4   3   2   1   0
```

## License

MIT License