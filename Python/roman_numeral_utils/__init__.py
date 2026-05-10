"""
Roman Numeral Utilities
=======================

A comprehensive library for converting between Arabic numerals and Roman numerals.
"""

from .mod import (
    to_roman,
    from_roman,
    is_valid_roman,
    parse_roman_in_text,
    roman_range,
    add_roman,
    subtract_roman,
    compare_roman,
    get_roman_info,
    format_with_ordinal,
    ROMAN_ONES,
    ROMAN_TENS,
    ROMAN_HUNDREDS,
)

__all__ = [
    'to_roman',
    'from_roman',
    'is_valid_roman',
    'parse_roman_in_text',
    'roman_range',
    'add_roman',
    'subtract_roman',
    'compare_roman',
    'get_roman_info',
    'format_with_ordinal',
    'ROMAN_ONES',
    'ROMAN_TENS',
    'ROMAN_HUNDREDS',
]

__version__ = '1.0.0'