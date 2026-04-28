# VIN Decoder Utilities

A comprehensive VIN (Vehicle Identification Number) decoder module with zero external dependencies.

## Features

- **VIN Validation**: Format validation and check digit verification
- **WMI Decoding**: World Manufacturer Identifier lookup
- **Region/Country Identification**: Determine vehicle origin
- **Manufacturer Lookup**: Identify vehicle manufacturer
- **Model Year Decoding**: Extract model year from VIN
- **VIN Generation**: Generate valid VINs for testing
- **Full VIN Information Extraction**: Complete decoding with all details

## Installation

This module is part of AllToolkit and has zero external dependencies.

```python
from vin_decoder_utils.mod import decode_vin, validate_vin, generate_vin
```

## Quick Start

### Validate a VIN

```python
from vin_decoder_utils.mod import validate_vin, validate_vin_format, validate_check_digit

# Format validation
result = validate_vin_format("1HGBH41JXMN109186")
print(f"Valid: {result.valid}, Errors: {result.errors}")

# Check digit validation
is_valid = validate_check_digit("1HGBH41JXMN109186")
print(f"Check digit valid: {is_valid}")

# Full validation
result = validate_vin("1HGBH41JXMN109186")
print(f"Valid: {result.valid}")
```

### Decode a VIN

```python
from vin_decoder_utils.mod import decode_vin, format_vin

vin = "1HGBH41JXMN109186"
info = decode_vin(vin)

print(f"WMI: {info.wmi}")                # 1HG
print(f"Manufacturer: {info.manufacturer}") # Honda
print(f"Country: {info.country}")          # Japan
print(f"Region: {info.region}")            # North America
print(f"Model Year: {info.model_year}")    # Based on year code
print(f"Check Digit: {info.check_digit}")  # 9th character
print(f"Valid: {info.valid}")              # Overall validity

# Format for readability
formatted = format_vin(vin, '-')
print(formatted)  # 1HG-BH41-JXM-N109186
```

### Extract VINs from Text

```python
from vin_decoder_utils.mod import extract_vin_from_text

text = "Found VINs: 1HGBH41JXMN109186, JHMFA16586S012345 in the document"
vins = extract_vin_from_text(text)
print(vins)  # ['1HGBH41JXMN109186', 'JHMFA16586S012345']
```

### Generate Test VINs

```python
from vin_decoder_utils.mod import generate_vin

# Generate with default parameters
vin = generate_vin()
print(f"Generated: {vin}")

# Generate with specific parameters
vin = generate_vin(
    wmi="WB",         # BMW Germany
    model_year=2020,  # Year
    plant_code="A"    # Plant code
)
print(f"BMW VIN: {vin}")
```

### Get Year Code

```python
from vin_decoder_utils.mod import get_year_code, get_possible_years

# Get year code for a specific year
code = get_year_code(2020)
print(f"Year 2020 code: {code}")  # L

# Get all possible years from a VIN (handles 30-year cycle)
vin = generate_vin("1HG", model_year=2020)
years = get_possible_years(vin)
print(f"Possible years: {years}")  # [1990, 2020] or [2020, 2050]
```

## VIN Structure

A VIN consists of 17 characters divided into three sections:

| Position | Section | Description |
|----------|---------|-------------|
| 1-3 | WMI | World Manufacturer Identifier |
| 4-8 | VDS | Vehicle Descriptor Section |
| 9 | Check Digit | Validation digit (0-9 or X) |
| 10 | Year Code | Model year indicator |
| 11 | Plant Code | Manufacturing plant |
| 12-17 | Sequential | Unique vehicle number |

### Year Codes (Cycle every 30 years)

| Code | Year(s) |
|------|---------|
| A | 1980, 2010 |
| B | 1981, 2011 |
| C | 1982, 2012 |
| ... | ... |
| L | 1990, 2020 |
| ... | ... |
| Y | 2000, 2030 |
| 1-9 | 2001-2009, 2031-2039 |

### Region Codes

| First Character | Region |
|-----------------|--------|
| A-H | Africa |
| J-R | Asia |
| S-Z | Europe |
| 1-5 | North America |
| 6-7 | Oceania |
| 8-9 | South America |

### Invalid Characters

VINs cannot contain:
- **I** (confused with 1)
- **O** (confused with 0)
- **Q** (confused with 0)

## API Reference

### Validation Functions

- `validate_vin_format(vin)` - Check VIN format (length, characters)
- `validate_check_digit(vin)` - Verify check digit
- `validate_vin(vin)` - Full validation
- `calculate_check_digit(vin)` - Calculate expected check digit

### Decoding Functions

- `decode_vin(vin)` - Full VIN decoding, returns `VINInfo`
- `get_region(vin)` - Get region from VIN
- `get_country(vin)` - Get country of manufacture
- `get_manufacturer(vin)` - Get manufacturer name
- `get_model_year(vin)` - Get model year
- `get_possible_years(vin)` - Get all possible years (handles cycle)
- `decode_wmi(wmi)` - Decode WMI code

### Utility Functions

- `format_vin(vin, separator)` - Format VIN with separators
- `extract_vin_from_text(text)` - Extract VINs from text
- `compare_vins(vin1, vin2)` - Compare two VINs
- `get_year_code(year)` - Get year code for a year

### Generation Functions

- `generate_vin(wmi, vds, model_year, plant_code, sequential)` - Generate valid VIN

### Data Structures

```python
VINInfo(
    vin,              # Full VIN
    valid,            # Overall validity
    check_digit,      # 9th character
    check_digit_valid,# Check digit status
    wmi,              # World Manufacturer Identifier
    vds,              # Vehicle Descriptor Section
    vis,              # Vehicle Identifier Section
    manufacturer,     # Manufacturer name
    country,          # Country of manufacture
    region,           # Region name
    model_year,       # Model year
    model_years,      # All possible years
    plant_code,       # Plant code
    sequential_number # Sequential number
)
```

## Examples

```python
from vin_decoder_utils.mod import decode_vin, generate_vin, compare_vins

# Decode a Honda VIN
info = decode_vin("1HGBH41JXMN109186")
print(f"{info.manufacturer} {info.model_year} from {info.country}")

# Generate test VINs for different manufacturers
honda = generate_vin("JHM", model_year=2020)   # Honda Japan
bmw = generate_vin("WB", model_year=2018)      # BMW Germany
toyota = generate_vin("JT", model_year=2015)   # Toyota Japan
volvo = generate_vin("YV", model_year=2020)    # Volvo Sweden

# Compare VINs
comparison = compare_vins(honda, bmw)
print(f"Same manufacturer: {comparison['same_manufacturer']}")
print(f"Same region: {comparison['same_region']}")
```

## Test Coverage

Run tests with:

```bash
python vin_decoder_utils_test.py
```

Test suites include:
- Format validation
- Check digit calculation
- Region/country identification
- Manufacturer lookup
- Model year decoding
- VIN generation
- Edge cases and error handling
- Year code cycle handling

## Standards

- ISO 3779: Road vehicles — Vehicle identification number (VIN) content and structure
- ISO 3780: Road vehicles — World manufacturer identifier (WMI) code

## License

MIT License - Part of AllToolkit