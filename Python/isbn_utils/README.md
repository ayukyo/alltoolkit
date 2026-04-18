# ISBN Utilities

A comprehensive Python toolkit for working with International Standard Book Numbers (ISBN). Supports both ISBN-10 (legacy) and ISBN-13 (current standard) formats with zero external dependencies.

## Features

- ✅ **Validation** - Validate ISBN-10 and ISBN-13 numbers
- ✅ **Conversion** - Convert between ISBN-10 and ISBN-13 formats
- ✅ **Generation** - Generate random valid ISBNs for testing
- ✅ **Extraction** - Extract ISBNs from text
- ✅ **Formatting** - Format ISBNs with proper hyphens/spaces
- ✅ **Parsing** - Get detailed information about an ISBN
- ✅ **Zero Dependencies** - Uses only Python standard library

## Installation

No installation required! Just copy the `isbn_utils` folder to your project.

```python
from isbn_utils import (
    is_valid_isbn,
    validate_isbn,
    format_isbn,
    # ... and more
)
```

## Quick Start

```python
from isbn_utils import is_valid_isbn, format_isbn, isbn10_to_isbn13

# Validate
print(is_valid_isbn("0306406152"))        # True (ISBN-10)
print(is_valid_isbn("9780306406157"))    # True (ISBN-13)

# Convert
print(isbn10_to_isbn13("0306406152"))     # 9780306406157

# Format
print(format_isbn("0306406152"))          # 0-306-40615-2
```

## API Reference

### Validation

```python
from isbn_utils import (
    is_valid_isbn,      # Check if valid ISBN (10 or 13)
    is_valid_isbn10,    # Check if valid ISBN-10
    is_valid_isbn13,    # Check if valid ISBN-13
    validate_isbn,      # Full validation with details
    validate_isbn10,    # Full validation for ISBN-10
    validate_isbn13,    # Full validation for ISBN-13
)

# Simple boolean check
is_valid_isbn("0306406152")     # True
is_valid_isbn10("0306406152")   # True
is_valid_isbn13("9780306406157") # True

# Full validation with details
valid, cleaned, isbn_type, msg = validate_isbn("0-306-40615-2")
# valid=True, cleaned="0306406152", isbn_type=ISBNType.ISBN10, msg="Valid ISBN-10"
```

### Check Digit Calculation

```python
from isbn_utils import (
    calculate_check_digit_isbn10,
    calculate_check_digit_isbn13,
)

# Calculate ISBN-10 check digit (can be 0-9 or X)
calculate_check_digit_isbn10("030640615")  # "2"

# Calculate ISBN-13 check digit (0-9)
calculate_check_digit_isbn13("978030640615")  # "7"
```

### Conversion

```python
from isbn_utils import (
    isbn10_to_isbn13,   # Convert ISBN-10 to ISBN-13
    isbn13_to_isbn10,   # Convert ISBN-13 to ISBN-10 (978 prefix only)
    convert_isbn,       # Auto-detect and convert
    normalize_isbn,     # Normalize to specific format
)

# ISBN-10 to ISBN-13
isbn10_to_isbn13("0306406152")  # "9780306406157"

# ISBN-13 to ISBN-10 (only works for 978 prefix)
isbn13_to_isbn10("9780306406157")  # "0306406152"
isbn13_to_isbn10("9798700839847")  # None (979 prefix not convertible)

# Auto-detect and convert
convert_isbn("0306406152")      # "9780306406157"
convert_isbn("9780306406157")   # "0306406152"

# Normalize to specific format
normalize_isbn("0306406152", "13")  # "9780306406157"
normalize_isbn("9780306406157", "10")  # "0306406152"
```

### Generation

```python
from isbn_utils import (
    generate_isbn10,      # Generate random ISBN-10
    generate_isbn13,      # Generate random ISBN-13
    generate_random_isbn, # Generate random ISBN (any format)
)

# Generate random ISBN-10
isbn10 = generate_isbn10()
# Example: "123456789X"

# Generate with prefix
isbn10 = generate_isbn10(prefix="123")
# Example: "123456789X"

# Reproducible generation (with seed)
isbn10 = generate_isbn10(seed=42)

# Generate random ISBN-13
isbn13 = generate_isbn13()  # Default prefix: 978
isbn13 = generate_isbn13(prefix="979")  # With 979 prefix

# Generate either format
isbn = generate_random_isbn(format="10")  # ISBN-10
isbn = generate_random_isbn(format="13")  # ISBN-13
```

### Formatting

```python
from isbn_utils import (
    format_isbn,    # Format any ISBN
    format_isbn10,  # Format ISBN-10
    format_isbn13,  # Format ISBN-13
)

# Format with hyphens
format_isbn("0306406152")       # "0-306-40615-2"
format_isbn("9780306406157")    # "978-0-306-40615-7"

# Format with spaces
format_isbn("0306406152", separator=" ")  # "0 306 40615 2"
```

### Extraction

```python
from isbn_utils import (
    extract_isbn,      # Extract first ISBN from text
    extract_all_isbn,  # Extract all ISBNs from text
)

# Extract single ISBN
text = "The book's ISBN is 978-0-306-40615-7."
isbn = extract_isbn(text)  # "9780306406157"

# Extract all ISBNs
text = "Book 1: ISBN 0306406152, Book 2: ISBN 9780131103624"
isbns = extract_all_isbn(text)  # ["0306406152", "9780131103624"]

# Handles various formats
extract_isbn("ISBN: 0-306-40615-2")       # "0306406152"
extract_isbn("ISBN-13: 9780306406157")    # "9780306406157"
extract_isbn("ISBN-10: 0 306 40615 2")     # "0306406152"
```

### Parsing

```python
from isbn_utils import (
    parse_isbn,      # Get detailed ISBN info
    get_isbn_info,   # Get info as dictionary
    ISBNType,        # Enum for ISBN types
)

# Parse ISBN
info = parse_isbn("0-306-40615-2")
# ISBNInfo(ISBN-10='0306406152')

info.is_valid        # True
info.isbn_type       # ISBNType.ISBN10
info.cleaned         # "0306406152"
info.check_digit     # "2"
info.prefix          # None (ISBN-10 has no prefix)
info.isbn10          # "0306406152"
info.isbn13          # "9780306406157"
info.formatted_hyphen # "0-306-40615-2"

# Get as dictionary
d = get_isbn_info("9780306406157")
# {
#     "original": "9780306406157",
#     "cleaned": "9780306406157",
#     "type": "ISBN-13",
#     "is_valid": True,
#     "check_digit": "7",
#     "prefix": "978",
#     "isbn10": "0306406152",
#     "isbn13": "9780306406157",
#     ...
# }
```

## Examples

See `examples/` folder for more usage examples.

## Testing

Run tests with:

```bash
# Using pytest
python -m pytest isbn_utils_test.py -v

# Or directly
python isbn_utils_test.py
```

## ISBN Format Reference

### ISBN-10
- 10 characters (digits 0-9, or X for check digit)
- Format: `X-XXXXX-XXX-X` (group-publisher-title-check)
- Check digit: weighted sum mod 11 (X = 10)
- Example: `0-306-40615-2`

### ISBN-13
- 13 digits
- Format: `XXX-X-XXXXX-XXX-X` (prefix-group-publisher-title-check)
- Prefix: 978 or 979
- Check digit: EAN-13 algorithm (weighted sum mod 10)
- Example: `978-0-306-40615-7`

## License

MIT License