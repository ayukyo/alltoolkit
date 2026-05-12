#!/usr/bin/env python3
"""
ISBN Utilities - Usage Examples

This script demonstrates how to use the isbn_utils module for:
- Validating ISBN-10 and ISBN-13
- Parsing ISBN components
- Converting between ISBN formats
- Formatting ISBN strings
- Generating test ISBNs
- Finding ISBNs in text
"""

import sys
import os

# Add isbn_utils directory to path
mod_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, mod_dir)

from mod import (
    clean, validate, validate_isbn10, validate_isbn13,
    calculate_check_digit_isbn10, calculate_check_digit_isbn13,
    isbn10_to_isbn13, isbn13_to_isbn10,
    parse, format, get_type, is_isbn10, is_isbn13,
    generate_isbn10, generate_isbn13, batch_validate,
    normalize, find_isbns, compare, get_group_name, analyze, repair
)


def example_validation():
    """Example: Validate ISBNs."""
    print("\n" + "=" * 50)
    print("Validation Examples")
    print("=" * 50)
    
    isbns = [
        '978-0-306-40615-7',  # Valid ISBN-13
        '0-306-40615-2',       # Valid ISBN-10
        '080442957X',          # Valid ISBN-10 with X check digit
        '9780140283297',       # Valid ISBN-13
        'invalid-isbn',        # Invalid
        '123456789',           # Invalid (too short)
    ]
    
    for isbn in isbns:
        result = "✓ Valid" if validate(isbn) else "✗ Invalid"
        isbn_type = get_type(isbn) or "Unknown"
        print(f"  {isbn:20} → {result} ({isbn_type})")


def example_parsing():
    """Example: Parse ISBN details."""
    print("\n" + "=" * 50)
    print("Parsing Examples")
    print("=" * 50)
    
    isbns = [
        '978-0-306-40615-7',
        '080442957X',
    ]
    
    for isbn in isbns:
        print(f"\n  Original: {isbn}")
        result = parse(isbn)
        
        if result['valid']:
            print(f"  Type: {result['type']}")
            print(f"  Cleaned: {result['cleaned']}")
            print(f"  Check Digit: {result['check_digit']}")
            if result['isbn10']:
                print(f"  ISBN-10: {result['isbn10']}")
            if result['isbn13']:
                print(f"  ISBN-13: {result['isbn13']}")
        else:
            print(f"  Invalid ISBN")


def example_conversion():
    """Example: Convert between ISBN-10 and ISBN-13."""
    print("\n" + "=" * 50)
    print("Conversion Examples")
    print("=" * 50)
    
    # ISBN-10 to ISBN-13
    isbn10 = '0306406152'
    isbn13 = isbn10_to_isbn13(isbn10)
    print(f"\n  ISBN-10 → ISBN-13:")
    print(f"    {isbn10} → {isbn13}")
    
    # ISBN-13 to ISBN-10 (978 prefix only)
    isbn13 = '9780306406157'
    isbn10 = isbn13_to_isbn10(isbn13)
    print(f"\n  ISBN-13 → ISBN-10 (978 prefix):")
    print(f"    {isbn13} → {isbn10}")
    
    # ISBN-13 with 979 prefix cannot convert to ISBN-10
    isbn13_979 = '9790306406156'
    isbn10_result = isbn13_to_isbn10(isbn13_979)
    print(f"\n  ISBN-13 → ISBN-10 (979 prefix):")
    print(f"    {isbn13_979} → {isbn10_result} (None - cannot convert)")


def example_check_digit():
    """Example: Calculate check digits."""
    print("\n" + "=" * 50)
    print("Check Digit Calculation")
    print("=" * 50)
    
    # ISBN-10 check digit
    base10 = '030640615'
    check10 = calculate_check_digit_isbn10(base10)
    print(f"\n  ISBN-10:")
    print(f"    Base: {base10}")
    print(f"    Check Digit: {check10}")
    print(f"    Complete: {base10}{check10}")
    
    # ISBN-10 with X check digit
    base10_x = '080442957'
    check10_x = calculate_check_digit_isbn10(base10_x)
    print(f"\n  ISBN-10 (X check digit):")
    print(f"    Base: {base10_x}")
    print(f"    Check Digit: {check10_x}")
    print(f"    Complete: {base10_x}{check10_x}")
    
    # ISBN-13 check digit
    base13 = '978030640615'
    check13 = calculate_check_digit_isbn13(base13)
    print(f"\n  ISBN-13:")
    print(f"    Base: {base13}")
    print(f"    Check Digit: {check13}")
    print(f"    Complete: {base13}{check13}")


def example_formatting():
    """Example: Format ISBN strings."""
    print("\n" + "=" * 50)
    print("Formatting Examples")
    print("=" * 50)
    
    isbn10 = '0306406152'
    isbn13 = '9780306406157'
    
    print(f"\n  ISBN-10 formats:")
    print(f"    Clean:      {format(isbn10, 'clean')}")
    print(f"    Hyphenated: {format(isbn10, 'hyphenated')}")
    print(f"    Spaced:     {format(isbn10, 'spaced')}")
    
    print(f"\n  ISBN-13 formats:")
    print(f"    Clean:      {format(isbn13, 'clean')}")
    print(f"    Hyphenated: {format(isbn13, 'hyphenated')}")
    print(f"    Spaced:     {format(isbn13, 'spaced')}")


def example_generation():
    """Example: Generate test ISBNs."""
    print("\n" + "=" * 50)
    print("ISBN Generation (for testing)")
    print("=" * 50)
    
    print("\n  Generated ISBN-10s:")
    for i in range(5):
        isbn = generate_isbn10()
        print(f"    {isbn} ({'valid' if validate_isbn10(isbn) else 'invalid'})")
    
    print("\n  Generated ISBN-13s (978 prefix):")
    for i in range(5):
        isbn = generate_isbn13(prefix='978')
        print(f"    {isbn} ({'valid' if validate_isbn13(isbn) else 'invalid'})")
    
    print("\n  Generated ISBN-13s (979 prefix):")
    for i in range(5):
        isbn = generate_isbn13(prefix='979')
        print(f"    {isbn} ({'valid' if validate_isbn13(isbn) else 'invalid'})")


def example_batch_validation():
    """Example: Batch validate ISBNs."""
    print("\n" + "=" * 50)
    print("Batch Validation")
    print("=" * 50)
    
    isbns = [
        '978-0-306-40615-7',  # Valid ISBN-13
        '0-306-40615-2',       # Valid ISBN-10
        '080442957X',          # Valid ISBN-10 (X check digit)
        '9780140283297',       # Valid ISBN-13
        'invalid-isbn',        # Invalid
        '123456789',           # Invalid (too short)
        '9790306406156',       # Valid ISBN-13 (979 prefix)
    ]
    
    result = batch_validate(isbns)
    
    print(f"\n  Total: {result['total']}")
    print(f"  Valid: {result['valid_count']}")
    print(f"  Invalid: {result['invalid_count']}")
    print(f"  ISBN-10: {result['isbn10_count']}")
    print(f"  ISBN-13: {result['isbn13_count']}")
    
    print(f"\n  Details:")
    for detail in result['details']:
        status = "✓" if detail['valid'] else "✗"
        print(f"    {status} {detail['original']:25} → {detail['type'] or 'Invalid'}")


def example_finding():
    """Example: Find ISBNs in text."""
    print("\n" + "=" * 50)
    print("Finding ISBNs in Text")
    print("=" * 50)
    
    text = """
    Here are some books I recommend:
    - "To Kill a Mockingbird" - ISBN: 978-0-14-028329-7
    - "1984" by Orwell - ISBN 0451524934
    - "The Great Gatsby" (ISBN: 978-074327356-5)
    - Another edition: 0-7432-7356-7
    
    These are all great reads!
    """
    
    isbns = find_isbns(text)
    
    print(f"\n  Text: {text.strip()[:50]}...")
    print(f"\n  Found {len(isbns)} ISBNs:")
    for isbn in isbns:
        print(f"    - {isbn}")


def example_comparison():
    """Example: Compare ISBNs."""
    print("\n" + "=" * 50)
    print("ISBN Comparison")
    print("=" * 50)
    
    pairs = [
        ('0306406152', '9780306406157'),  # Same book
        ('0306406152', '0471958697'),      # Different books
        ('9780306406157', '9780306406157'),  # Same ISBN
    ]
    
    for isbn1, isbn2 in pairs:
        result = compare(isbn1, isbn2)
        print(f"\n  Compare: {isbn1} vs {isbn2}")
        print(f"    ISBN1: {result['isbn1_type']}")
        print(f"    ISBN2: {result['isbn2_type']}")
        print(f"    Same Book: {result['same_book']}")
        print(f"    Same ISBN: {result['same_isbn']}")


def example_analysis():
    """Example: Comprehensive ISBN analysis."""
    print("\n" + "=" * 50)
    print("ISBN Analysis")
    print("=" * 50)
    
    isbns = [
        '978-0-306-40615-7',
        '080442957X',
        '9780743273565',
    ]
    
    for isbn in isbns:
        result = analyze(isbn)
        
        if result['valid']:
            print(f"\n  Original: {result['original']}")
            print(f"  Type: {result['type']}")
            print(f"  Cleaned: {result['cleaned']}")
            print(f"  Group: {result['group']} ({result['group_name']})")
            print(f"  Check Digit: {result['check_digit']}")
            if result['isbn10']:
                print(f"  ISBN-10: {result['isbn10']}")
            if result['isbn13']:
                print(f"  ISBN-13: {result['isbn13']}")
            print(f"  Formats:")
            for style, formatted in result['formats'].items():
                print(f"    {style}: {formatted}")
        else:
            print(f"\n  {isbn}: Invalid")


def example_repair():
    """Example: Repair malformed ISBNs."""
    print("\n" + "=" * 50)
    print("ISBN Repair")
    print("=" * 50)
    
    malformed = [
        '030640615',      # Missing check digit
        '978030640615',   # Missing check digit
        '03064061523',    # Extra digit
        '0306406152',     # Already valid
    ]
    
    for isbn in malformed:
        repaired = repair(isbn)
        status = "Repaired" if repaired and repaired != clean(isbn) else "Already valid" if repaired else "Unrepairable"
        print(f"  {isbn:15} → {repaired or 'N/A':15} ({status})")


def example_normalization():
    """Example: Normalize ISBNs to different formats."""
    print("\n" + "=" * 50)
    print("ISBN Normalization")
    print("=" * 50)
    
    isbns = [
        '978-0-306-40615-7',
        '0-306-40615-2',
        '080442957X',
    ]
    
    for isbn in isbns:
        print(f"\n  Original: {isbn}")
        print(f"    → ISBN-13: {normalize(isbn, 'isbn13')}")
        print(f"    → ISBN-10: {normalize(isbn, 'isbn10')}")
        print(f"    → Clean: {normalize(isbn, 'clean')}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("ISBN Utilities - Comprehensive Examples")
    print("=" * 60)
    
    example_validation()
    example_parsing()
    example_conversion()
    example_check_digit()
    example_formatting()
    example_generation()
    example_batch_validation()
    example_finding()
    example_comparison()
    example_analysis()
    example_repair()
    example_normalization()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()