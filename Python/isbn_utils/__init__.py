"""
ISBN Utilities - ISBN-10/ISBN-13 Validation, Generation and Conversion

A comprehensive toolkit for working with International Standard Book Numbers (ISBN).
Supports ISBN-10 (legacy) and ISBN-13 (current standard) formats.

Features:
- Validate ISBN-10 and ISBN-13 numbers
- Convert between ISBN-10 and ISBN-13 formats
- Generate random valid ISBN numbers for testing
- Extract ISBN from various text formats
- Calculate check digits
- Format ISBN with proper hyphens

Zero external dependencies - uses only Python standard library.
"""

from .validator import (
    validate_isbn,
    validate_isbn10,
    validate_isbn13,
    is_valid_isbn,
    is_valid_isbn10,
    is_valid_isbn13,
    calculate_check_digit_isbn10,
    calculate_check_digit_isbn13,
)

from .converter import (
    isbn10_to_isbn13,
    isbn13_to_isbn10,
    convert_isbn,
    normalize_isbn,
)

from .generator import (
    generate_isbn10,
    generate_isbn13,
    generate_random_isbn,
)

from .formatter import (
    format_isbn,
    format_isbn10,
    format_isbn13,
    extract_isbn,
    extract_all_isbn,
)

from .parser import (
    parse_isbn,
    get_isbn_info,
    ISBNType,
    ISBNInfo,
)

__version__ = "1.0.0"
__all__ = [
    # Validation
    "validate_isbn",
    "validate_isbn10",
    "validate_isbn13",
    "is_valid_isbn",
    "is_valid_isbn10",
    "is_valid_isbn13",
    "calculate_check_digit_isbn10",
    "calculate_check_digit_isbn13",
    # Conversion
    "isbn10_to_isbn13",
    "isbn13_to_isbn10",
    "convert_isbn",
    "normalize_isbn",
    # Generation
    "generate_isbn10",
    "generate_isbn13",
    "generate_random_isbn",
    # Formatting
    "format_isbn",
    "format_isbn10",
    "format_isbn13",
    "extract_isbn",
    "extract_all_isbn",
    # Parsing
    "parse_isbn",
    "get_isbn_info",
    "ISBNType",
    "ISBNInfo",
]