#!/usr/bin/env python3
"""
ISBN Utilities - Examples

This script demonstrates various use cases of the isbn_utils module.
Run from the isbn_utils directory: python examples/basic_usage.py
"""

import sys
import os

# Add the parent Python directory to path for imports
# When running from isbn_utils directory, we need to go up two levels
current_dir = os.path.dirname(os.path.abspath(__file__))
python_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, python_dir)

from isbn_utils import (
    # Validation
    is_valid_isbn,
    is_valid_isbn10,
    is_valid_isbn13,
    validate_isbn,
    validate_isbn10,
    validate_isbn13,
    calculate_check_digit_isbn10,
    calculate_check_digit_isbn13,
    # Conversion
    isbn10_to_isbn13,
    isbn13_to_isbn10,
    convert_isbn,
    normalize_isbn,
    # Generation
    generate_isbn10,
    generate_isbn13,
    generate_random_isbn,
    # Formatting
    format_isbn,
    format_isbn10,
    format_isbn13,
    # Extraction
    extract_isbn,
    extract_all_isbn,
    # Parsing
    parse_isbn,
    get_isbn_info,
    ISBNType,
)


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def example_validation():
    """Demonstrate ISBN validation."""
    print_section("Validation Examples")
    
    test_isbns = [
        "0306406152",           # Valid ISBN-10
        "0-306-40615-2",        # Valid ISBN-10 with hyphens
        "080442957X",           # Valid ISBN-10 with X check digit
        "9780306406157",        # Valid ISBN-13
        "978-0-306-40615-7",    # Valid ISBN-13 with hyphens
        "9798700839847",        # Valid ISBN-13 with 979 prefix
        "0306406153",           # Invalid ISBN-10 (wrong check digit)
        "9780306406158",        # Invalid ISBN-13 (wrong check digit)
        "not-an-isbn",          # Invalid
    ]
    
    for isbn in test_isbns:
        valid, cleaned, isbn_type, msg = validate_isbn(isbn)
        status = "✓" if valid else "✗"
        print(f"{status} {isbn:20} → {isbn_type.value:8} | {msg}")
        if valid:
            print(f"  Cleaned: {cleaned}")


def example_check_digits():
    """Demonstrate check digit calculation."""
    print_section("Check Digit Calculation")
    
    # ISBN-10 check digits
    print("ISBN-10 Check Digits:")
    bases = [
        "030640615",    # Should be 2
        "080442957",    # Should be X
        "013110362",    # Should be 8
    ]
    
    for base in bases:
        check = calculate_check_digit_isbn10(base)
        print(f"  {base} → check digit: {check} → full: {base}{check}")
    
    # ISBN-13 check digits
    print("\nISBN-13 Check Digits:")
    bases = [
        "978030640615",     # Should be 7
        "978013110362",     # Should be 4
        "979870083984",     # Should be 7
    ]
    
    for base in bases:
        check = calculate_check_digit_isbn13(base)
        print(f"  {base} → check digit: {check} → full: {base}{check}")


def example_conversion():
    """Demonstrate ISBN conversion."""
    print_section("Conversion Examples")
    
    # ISBN-10 to ISBN-13
    print("ISBN-10 → ISBN-13:")
    isbn10s = [
        "0306406152",
        "080442957X",
        "0131103628",
    ]
    
    for isbn10 in isbn10s:
        isbn13 = isbn10_to_isbn13(isbn10)
        print(f"  {isbn10} → {isbn13}")
    
    # ISBN-13 to ISBN-10
    print("\nISBN-13 → ISBN-10:")
    isbn13s = [
        "9780306406157",
        "9780804429573",  # Correct ISBN-13
        "9780131103627",  # Correct ISBN-13
        "9798700839846",  # 979 prefix - cannot convert
    ]
    
    for isbn13 in isbn13s:
        isbn10 = isbn13_to_isbn10(isbn13)
        result = isbn10 if isbn10 else "N/A (979 prefix)"
        print(f"  {isbn13} → {result}")
    
    # Auto-convert
    print("\nAuto-detect and convert:")
    test_isbns = [
        "0306406152",      # ISBN-10 → ISBN-13
        "9780306406157",   # ISBN-13 → ISBN-10
    ]
    
    for isbn in test_isbns:
        converted = convert_isbn(isbn)
        print(f"  {isbn} → {converted}")


def example_generation():
    """Demonstrate ISBN generation."""
    print_section("Generation Examples")
    
    # Generate random ISBN-10
    print("Random ISBN-10 numbers:")
    for _ in range(5):
        isbn = generate_isbn10()
        print(f"  {isbn} (valid: {is_valid_isbn10(isbn)})")
    
    # Generate random ISBN-13
    print("\nRandom ISBN-13 numbers:")
    for _ in range(5):
        isbn = generate_isbn13()
        print(f"  {isbn} (valid: {is_valid_isbn13(isbn)})")
    
    # Generate with prefix
    print("\nWith prefix '9781':")
    for _ in range(3):
        isbn = generate_isbn13(prefix="9781")
        print(f"  {isbn}")
    
    # Generate with seed (reproducible)
    print("\nReproducible generation (seed=42):")
    isbn1 = generate_isbn10(seed=42)
    isbn2 = generate_isbn10(seed=42)
    print(f"  First:  {isbn1}")
    print(f"  Second: {isbn2}")
    print(f"  Same: {isbn1 == isbn2}")


def example_formatting():
    """Demonstrate ISBN formatting."""
    print_section("Formatting Examples")
    
    test_isbns = [
        ("0306406152", "ISBN-10"),
        ("9780306406157", "ISBN-13"),
        ("080442957X", "ISBN-10 with X"),
    ]
    
    for isbn, desc in test_isbns:
        formatted = format_isbn(isbn)
        formatted_space = format_isbn(isbn, separator=" ")
        print(f"{desc}:")
        print(f"  Original:  {isbn}")
        print(f"  Hyphens:   {formatted}")
        print(f"  Spaces:    {formatted_space}")
        print()


def example_extraction():
    """Demonstrate ISBN extraction from text."""
    print_section("Extraction Examples")
    
    texts = [
        "The book's ISBN is 978-0-306-40615-7.",
        "ISBN: 0306406152 - Classic text",
        "ISBN-10: 0-8044-2957-X\nISBN-13: 978-0-8044-2957-0",
        "Check out ISBN 9780131103624 and ISBN 0 306 40615 2",
        "No ISBN here, just regular text.",
    ]
    
    for text in texts:
        print(f"Text: {text}")
        extracted = extract_isbn(text)
        print(f"  First ISBN: {extracted}")
        
        all_isbns = extract_all_isbn(text)
        if all_isbns:
            print(f"  All ISBNs: {all_isbns}")
        print()


def example_parsing():
    """Demonstrate ISBN parsing."""
    print_section("Parsing Examples")
    
    test_isbns = [
        "0-306-40615-2",
        "978-0-306-40615-7",
        "979-8-7008-3984-7",
        "invalid-isbn",
    ]
    
    for isbn in test_isbns:
        info = parse_isbn(isbn)
        print(f"Input: {isbn}")
        print(f"  Valid: {info.is_valid}")
        print(f"  Type: {info.isbn_type.value}")
        
        if info.is_valid:
            print(f"  Cleaned: {info.cleaned}")
            print(f"  Check digit: {info.check_digit}")
            print(f"  ISBN-10: {info.isbn10}")
            print(f"  ISBN-13: {info.isbn13}")
            print(f"  Formatted: {info.formatted_hyphen}")
        print()


def example_real_world():
    """Demonstrate real-world use cases."""
    print_section("Real-World Use Cases")
    
    # Use case 1: Validate and clean user input
    print("1. Validate and clean user input:")
    user_input = "  0-306-40615-2  "
    cleaned = user_input.strip()
    if is_valid_isbn(cleaned):
        formatted = format_isbn(cleaned)
        isbn13 = normalize_isbn(cleaned, "13")
        print(f"  Input: '{user_input}'")
        print(f"  Valid! Formatted: {formatted}")
        print(f"  ISBN-13: {isbn13}")
    else:
        print(f"  Invalid ISBN: {cleaned}")
    
    # Use case 2: Convert ISBNs in a database
    print("\n2. Convert legacy ISBN-10s to ISBN-13:")
    legacy_isbns = ["0306406152", "080442957X", "0131103628"]
    modern_isbns = [isbn10_to_isbn13(isbn) for isbn in legacy_isbns]
    print(f"  Legacy: {legacy_isbns}")
    print(f"  Modern: {modern_isbns}")
    
    # Use case 3: Extract ISBNs from a document
    print("\n3. Extract ISBNs from a document:")
    document = """
    Book Catalog:
    - The C Programming Language (ISBN: 0-13-110362-8)
    - Design Patterns (ISBN-13: 978-0-201-63361-0)
    - Clean Code (ISBN: 0132350882)
    """
    isbns = extract_all_isbn(document)
    print(f"  Found {len(isbns)} ISBNs:")
    for isbn in isbns:
        info = parse_isbn(isbn)
        print(f"    - {info.formatted_hyphen} ({info.isbn_type.value})")
    
    # Use case 4: Generate test data
    print("\n4. Generate test ISBNs:")
    test_isbns = [generate_random_isbn() for _ in range(5)]
    print(f"  Generated: {test_isbns}")
    print(f"  All valid: {all(is_valid_isbn(isbn) for isbn in test_isbns)}")


def main():
    """Run all examples."""
    print("="*60)
    print("  ISBN UTILITIES - EXAMPLES")
    print("="*60)
    
    example_validation()
    example_check_digits()
    example_conversion()
    example_generation()
    example_formatting()
    example_extraction()
    example_parsing()
    example_real_world()
    
    print("\n" + "="*60)
    print("  Done!")
    print("="*60)


if __name__ == "__main__":
    main()