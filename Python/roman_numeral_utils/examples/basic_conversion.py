#!/usr/bin/env python3
"""
Example: Basic Roman Numeral Conversions
=========================================

Demonstrates basic conversion between Arabic and Roman numerals.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from roman_numeral_utils.mod import to_roman, from_roman


def main():
    print("=" * 50)
    print("Basic Roman Numeral Conversions")
    print("=" * 50)
    
    # Numbers to convert
    numbers = [1, 4, 9, 27, 49, 99, 202, 449, 999, 1492, 1776, 1994, 2024, 3999]
    
    print("\nArabic -> Roman:")
    print("-" * 30)
    for num in numbers:
        roman = to_roman(num)
        print(f"{num:6} -> {roman}")
    
    print("\n" + "=" * 50)
    print("Roman -> Arabic:")
    print("-" * 30)
    
    romans = ['I', 'IV', 'IX', 'XL', 'XC', 'CD', 'CM', 'MCMXCIV', 'MMXXIV', 'MMMCMXCIX']
    for roman in romans:
        num = from_roman(roman)
        print(f"{roman:12} -> {num}")
    
    print("\n" + "=" * 50)
    print("Case Insensitive:")
    print("-" * 30)
    test_cases = ['iv', 'IV', 'mcmxciv', 'MCMXCIV']
    for roman in test_cases:
        print(f"'{roman}' -> {from_roman(roman)}")


if __name__ == '__main__':
    main()