"""
Roman Numeral Utilities
=======================

A comprehensive library for converting between Arabic numerals and Roman numerals.

Features:
- Arabic to Roman numeral conversion (1-3999 standard, up to 3999999 extended)
- Roman to Arabic numeral conversion
- Validation and detailed error messages
- RomanNumeral class with arithmetic operations
- Chain builder for fluent API
- Sorting, summing, and range generation
"""

from .mod import (
    to_roman,
    from_roman,
    is_valid_roman,
    validate_roman,
    RomanNumeral,
    RomanNumeralError,
    InvalidRomanNumeralError,
    OutOfRangeError,
    roman_sort,
    roman_range,
    roman_sum,
    roman_list,
    RomanNumeralBuilder,
    roman,
)

__all__ = [
    'to_roman',
    'from_roman',
    'is_valid_roman',
    'validate_roman',
    'RomanNumeral',
    'RomanNumeralError',
    'InvalidRomanNumeralError',
    'OutOfRangeError',
    'roman_sort',
    'roman_range',
    'roman_sum',
    'roman_list',
    'RomanNumeralBuilder',
    'roman',
]

__version__ = '2.0.0'