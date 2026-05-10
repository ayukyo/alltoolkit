#!/usr/bin/env python3
"""
Example: Roman Numeral Arithmetic
==================================

Demonstrates arithmetic operations with Roman numerals.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from roman_numeral_utils.mod import (
    add_roman,
    subtract_roman,
    compare_roman,
    roman_range,
)


def main():
    print("=" * 50)
    print("Roman Numeral Arithmetic")
    print("=" * 50)
    
    # Addition
    print("\nAddition:")
    print("-" * 30)
    additions = [
        ('I', 'I'),
        ('III', 'VII'),
        ('X', 'X'),
        ('IV', 'I'),
        ('XL', 'X'),
        ('C', 'D'),
        ('CM', 'C'),
    ]
    for a, b in additions:
        result = add_roman(a, b)
        print(f"{a} + {b} = {result}")
    
    # Subtraction
    print("\n" + "=" * 50)
    print("Subtraction:")
    print("-" * 30)
    subtractions = [
        ('II', 'I'),
        ('X', 'I'),
        ('V', 'I'),
        ('X', 'V'),
        ('C', 'X'),
        ('M', 'D'),
    ]
    for a, b in subtractions:
        result = subtract_roman(a, b)
        print(f"{a} - {b} = {result}")
    
    # Comparison
    print("\n" + "=" * 50)
    print("Comparison:")
    print("-" * 30)
    comparisons = [
        ('I', 'V'),
        ('V', 'V'),
        ('X', 'V'),
        ('MCMXCIV', 'MMXXIV'),
    ]
    for a, b in comparisons:
        result = compare_roman(a, b)
        symbol = '<' if result < 0 else ('=' if result == 0 else '>')
        print(f"{a} {symbol} {b}")
    
    # Range generation
    print("\n" + "=" * 50)
    print("Range Generation (1-20):")
    print("-" * 30)
    numerals = list(roman_range(1, 21))
    for i, numeral in enumerate(numerals, 1):
        print(f"{i:2}: {numeral}")
    
    # Olympic Games example
    print("\n" + "=" * 50)
    print("Modern Olympic Games (Roman Numerals):")
    print("-" * 30)
    for i in range(1, 35):
        roman = list(roman_range(i, i + 1))[0]
        year = 1896 + (i - 1) * 4
        print(f"Games {roman:6} - {year}")


if __name__ == '__main__':
    main()