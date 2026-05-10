#!/usr/bin/env python3
"""
Example: Parsing Roman Numerals in Text
========================================

Demonstrates finding and parsing Roman numerals in text.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from roman_numeral_utils.mod import (
    parse_roman_in_text,
    is_valid_roman,
    get_roman_info,
    format_with_ordinal,
)


def main():
    print("=" * 60)
    print("Parsing Roman Numerals in Text")
    print("=" * 60)
    
    # Example texts
    texts = [
        "King Henry VIII had six wives. His son Edward VI succeeded him.",
        "Chapter IV: The Journey Begins. See page XIX for details.",
        "World War I (1914-1918) and World War II (1939-1945) were major conflicts.",
        "Super Bowl LVII was held in 2023. The previous was Super Bowl LVI.",
        "Star Wars Episodes IV, V, and VI form the original trilogy.",
    ]
    
    for text in texts:
        print(f"\nText: {text}")
        print("-" * 60)
        
        parsed = parse_roman_in_text(text)
        if parsed:
            for roman, value, start, end in parsed:
                print(f"  Found '{roman}' ({value}) at position {start}-{end}")
        else:
            print("  No Roman numerals found.")
    
    # Validation examples
    print("\n" + "=" * 60)
    print("Validation Examples:")
    print("-" * 60)
    
    test_cases = ['I', 'IV', 'IIII', 'IX', 'VV', 'MCMXCIV', 'ABC', 'XLIX']
    for roman in test_cases:
        valid = is_valid_roman(roman)
        status = "Valid" if valid else "Invalid"
        print(f"  {roman:10} -> {status}")
    
    # Detailed info
    print("\n" + "=" * 60)
    print("Detailed Roman Numeral Information:")
    print("-" * 60)
    
    for roman in ['IV', 'XLIX', 'MCMXCIV']:
        info = get_roman_info(roman)
        print(f"\n{roman}:")
        print(f"  Value: {info['value']}")
        print(f"  Length: {info['length']}")
        print(f"  Characters: {info['characters']}")
        print(f"  Breakdown:")
        for item in info['breakdown']:
            print(f"    {item['symbol']}: {item['value']} × {item['count']}")
    
    # Formatting with ordinal
    print("\n" + "=" * 60)
    print("Formatting Options:")
    print("-" * 60)
    
    for i in [1, 2, 3, 4, 11, 21, 22, 23, 100]:
        roman_fmt = format_with_ordinal(i, use_roman=True)
        ordinal_fmt = format_with_ordinal(i, use_roman=False)
        print(f"  {i:3}: Roman = {roman_fmt:8} | Ordinal = {ordinal_fmt}")


if __name__ == '__main__':
    main()