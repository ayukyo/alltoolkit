#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - ISBN Utilities Usage Examples
============================================
Practical examples demonstrating ISBN utilities functionality.

Run with: python usage_examples.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    clean_isbn,
    is_isbn10,
    is_isbn13,
    is_valid_isbn,
    get_isbn_type,
    calculate_isbn10_check_digit,
    calculate_isbn13_check_digit,
    isbn10_to_isbn13,
    isbn13_to_isbn10,
    convert_isbn,
    format_isbn,
    format_isbn_compact,
    parse_isbn,
    generate_isbn10,
    generate_isbn13,
    generate_isbn,
    validate_isbns,
    find_isbns_in_text,
    compare_isbns,
    get_isbn_variants,
)


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print('=' * 60)


def example_basic_validation():
    """Basic ISBN validation examples."""
    print_section("Basic ISBN Validation")
    
    test_isbns = [
        "0306406152",      # Valid ISBN-10
        "9780306406157",   # Valid ISBN-13
        "0-306-40615-2",   # ISBN-10 with hyphens
        "978-0-306-40615-7",  # ISBN-13 with hyphens
        "030640615X",      # ISBN-10 with X check digit
        "invalid",         # Invalid
        "123456789",       # Too short
    ]
    
    for isbn in test_isbns:
        print(f"\nISBN: {isbn}")
        print(f"  Valid: {is_valid_isbn(isbn)}")
        print(f"  Type: {get_isbn_type(isbn)}")
        print(f"  Clean: {clean_isbn(isbn)}")


def example_check_digit_calculation():
    """Check digit calculation examples."""
    print_section("Check Digit Calculation")
    
    # ISBN-10 check digit
    print("\nISBN-10 Check Digit:")
    isbn9 = "030640615"
    check = calculate_isbn10_check_digit(isbn9)
    print(f"  Base: {isbn9}")
    print(f"  Check digit: {check}")
    print(f"  Full ISBN-10: {isbn9}{check}")
    
    # ISBN-10 with X check digit
    isbn9_x = "080442957"
    check_x = calculate_isbn10_check_digit(isbn9_x)
    print(f"\n  Base: {isbn9_x}")
    print(f"  Check digit: {check_x} (X = 10)")
    print(f"  Full ISBN-10: {isbn9_x}{check_x}")
    
    # ISBN-13 check digit
    print("\nISBN-13 Check Digit:")
    isbn12 = "978030640615"
    check13 = calculate_isbn13_check_digit(isbn12)
    print(f"  Base: {isbn12}")
    print(f"  Check digit: {check13}")
    print(f"  Full ISBN-13: {isbn12}{check13}")


def example_conversion():
    """ISBN conversion examples."""
    print_section("ISBN Conversion")
    
    # ISBN-10 to ISBN-13
    isbn10 = "0306406152"
    isbn13 = isbn10_to_isbn13(isbn10)
    print(f"\nISBN-10 → ISBN-13:")
    print(f"  {isbn10} → {isbn13}")
    
    # ISBN-13 to ISBN-10
    isbn13_input = "9780306406157"
    isbn10_output = isbn13_to_isbn10(isbn13_input)
    print(f"\nISBN-13 → ISBN-10:")
    print(f"  {isbn13_input} → {isbn10_output}")
    
    # 979 prefix cannot convert to ISBN-10
    isbn13_979 = "9790306406156"  # Valid 979 ISBN
    isbn10_from_979 = isbn13_to_isbn10(isbn13_979)
    print(f"\n979 Prefix (cannot convert to ISBN-10):")
    print(f"  {isbn13_979} → {isbn10_from_979}")
    
    # Using convert_isbn function
    print(f"\nUsing convert_isbn():")
    print(f"  convert_isbn('0306406152', 'ISBN-13') = {convert_isbn('0306406152', 'ISBN-13')}")
    print(f"  convert_isbn('9780306406157', 'ISBN-10') = {convert_isbn('9780306406157', 'ISBN-10')}")


def example_formatting():
    """ISBN formatting examples."""
    print_section("ISBN Formatting")
    
    isbns = [
        "0306406152",
        "9780306406157",
        "0471958697",
    ]
    
    for isbn in isbns:
        print(f"\nISBN: {isbn}")
        print(f"  Formatted: {format_isbn(isbn)}")
        print(f"  Compact: {format_isbn_compact(isbn)}")
        print(f"  Custom separator: {format_isbn(isbn, ' ')}")


def example_parsing():
    """ISBN parsing examples."""
    print_section("ISBN Parsing")
    
    test_isbns = [
        "0306406152",      # English ISBN-10
        "9780306406157",   # English ISBN-13
        "4771958697",      # Different group
        "9790306406153",   # 979 prefix
    ]
    
    for isbn in test_isbns:
        info = parse_isbn(isbn)
        print(f"\nISBN: {isbn}")
        print(f"  Valid: {info['valid']}")
        print(f"  Type: {info['type']}")
        print(f"  Group: {info['group']} ({info['group_name']})")
        print(f"  Check Digit: {info['check_digit']}")
        print(f"  ISBN-10: {info['isbn10']}")
        print(f"  ISBN-13: {info['isbn13']}")
        print(f"  Formatted: {info['formatted']}")


def example_generation():
    """ISBN generation examples."""
    print_section("ISBN Generation")
    
    print("\nGenerating random ISBN-10s:")
    for i in range(5):
        isbn = generate_isbn10()
        print(f"  {format_isbn(isbn)} (valid: {is_isbn10(isbn)})")
    
    print("\nGenerating random ISBN-13s:")
    for i in range(5):
        isbn = generate_isbn13()
        print(f"  {format_isbn(isbn)} (valid: {is_isbn13(isbn)})")
    
    print("\nGenerating with specific parameters:")
    print(f"  ISBN-10 (English group): {format_isbn(generate_isbn10(group='0'))}")
    print(f"  ISBN-10 (Chinese group): {format_isbn(generate_isbn10(group='7'))}")
    print(f"  ISBN-10 (Japanese group): {format_isbn(generate_isbn10(group='4'))}")
    print(f"  ISBN-13 (978 prefix): {format_isbn(generate_isbn13(prefix='978'))}")
    print(f"  ISBN-13 (979 prefix): {format_isbn(generate_isbn13(prefix='979'))}")


def example_batch_operations():
    """Batch ISBN operations examples."""
    print_section("Batch Operations")
    
    # Validate multiple ISBNs
    print("\nValidating multiple ISBNs:")
    isbns = [
        "0306406152",
        "9780306406157",
        "invalid-isbn",
        "0471958697",
        "12345",
    ]
    
    results = validate_isbns(isbns)
    for isbn, result in results.items():
        status = "✓" if result['valid'] else "✗"
        print(f"  {status} {isbn}: {result['type'] or 'Invalid'}")


def example_text_extraction():
    """Extract ISBNs from text."""
    print_section("Extract ISBNs from Text")
    
    text = """
    Book Catalog:
    - The Hitchhiker's Guide to the Galaxy (ISBN: 0-345-39180-2)
    - Another Book referenced as ISBN 978-0-306-40615-7
    - Classic: ISBN 0471958697
    - Fake ISBN: 1234567890
    - Invalid entry: not-an-isbn
    """
    
    print("Text:")
    print(text)
    
    found = find_isbns_in_text(text)
    print("\nFound ISBNs:")
    for isbn in found:
        info = parse_isbn(isbn)
        print(f"  {isbn} ({info['type']})")


def example_comparison():
    """ISBN comparison examples."""
    print_section("ISBN Comparison")
    
    # Compare equivalent ISBNs
    print("\nComparing equivalent ISBNs:")
    isbn10 = "0306406152"
    isbn13 = "9780306406157"
    print(f"  {isbn10} == {isbn13}: {compare_isbns(isbn10, isbn13)}")
    
    # Compare with formatting
    print("\nComparing with different formats:")
    formatted = "0-306-40615-2"
    print(f"  {isbn10} == {formatted}: {compare_isbns(isbn10, formatted)}")
    
    # Compare different books
    print("\nComparing different books:")
    other_isbn = "0471958697"
    print(f"  {isbn10} == {other_isbn}: {compare_isbns(isbn10, other_isbn)}")


def example_variants():
    """Get all variants of an ISBN."""
    print_section("ISBN Variants")
    
    isbn = "0306406152"
    variants = get_isbn_variants(isbn)
    
    print(f"\nVariants for {isbn}:")
    print(f"  ISBN-10: {variants['isbn10']}")
    print(f"  ISBN-13: {variants['isbn13']}")
    print(f"  Formatted ISBN-10: {variants['formatted10']}")
    print(f"  Formatted ISBN-13: {variants['formatted13']}")


def example_real_world_scenario():
    """Real-world use case: Book database cleanup."""
    print_section("Real-World Scenario: Book Database Cleanup")
    
    # Simulated book database with inconsistent ISBN formats
    books = [
        {"title": "Book A", "isbn": "0-306-40615-2"},
        {"title": "Book B", "isbn": "9780306406157"},
        {"title": "Book C", "isbn": "ISBN 0471958697"},
        {"title": "Book D", "isbn": "invalid"},
        {"title": "Book E", "isbn": "  0-345-39180-2  "},  # With spaces
    ]
    
    print("\nOriginal database:")
    for book in books:
        print(f"  {book['title']}: '{book['isbn']}'")
    
    # Clean up and standardize
    print("\nCleaned and standardized:")
    cleaned_books = []
    for book in books:
        clean = clean_isbn(book['isbn'])
        if is_valid_isbn(clean):
            standardized = isbn10_to_isbn13(clean) if is_isbn10(clean) else clean
            cleaned_books.append({
                "title": book["title"],
                "isbn10": isbn13_to_isbn10(standardized),
                "isbn13": standardized,
                "formatted": format_isbn(standardized)
            })
            print(f"  {book['title']}: {format_isbn(standardized)}")
        else:
            print(f"  {book['title']}: INVALID (removed)")
    
    # Find duplicates (same book with different ISBN formats)
    print("\nChecking for duplicates...")
    seen = {}
    duplicates = []
    for book in cleaned_books:
        if book["isbn13"] in seen:
            duplicates.append((book["title"], seen[book["isbn13"]]))
        else:
            seen[book["isbn13"]] = book["title"]
    
    if duplicates:
        print("  Found duplicates:")
        for dup, orig in duplicates:
            print(f"    '{dup}' is a duplicate of '{orig}'")
    else:
        print("  No duplicates found.")


def example_library_integration():
    """Example: Integration with library systems."""
    print_section("Library System Integration")
    
    # Search query normalization
    def normalize_isbn_search(query: str) -> dict:
        """Normalize ISBN search query for library lookup."""
        clean = clean_isbn(query)
        if not is_valid_isbn(clean):
            return {"valid": False, "error": "Invalid ISBN format"}
        
        return {
            "valid": True,
            "isbn10": isbn13_to_isbn10(clean) if is_isbn13(clean) else clean,
            "isbn13": isbn10_to_isbn13(clean) if is_isbn10(clean) else clean,
            "search_terms": [
                clean,
                format_isbn(clean),
                format_isbn(clean, " "),
            ]
        }
    
    # Test with various inputs
    queries = [
        "0306406152",
        "978-0-306-40615-7",
        "ISBN 0471958697",
        "invalid",
    ]
    
    print("\nSearch query normalization:")
    for query in queries:
        result = normalize_isbn_search(query)
        print(f"\n  Query: '{query}'")
        if result["valid"]:
            print(f"    ISBN-10: {result['isbn10']}")
            print(f"    ISBN-13: {result['isbn13']}")
            print(f"    Search terms: {result['search_terms']}")
        else:
            print(f"    Error: {result['error']}")


def main():
    """Run all examples."""
    print("=" * 60)
    print(" ISBN Utilities - Usage Examples")
    print("=" * 60)
    
    example_basic_validation()
    example_check_digit_calculation()
    example_conversion()
    example_formatting()
    example_parsing()
    example_generation()
    example_batch_operations()
    example_text_extraction()
    example_comparison()
    example_variants()
    example_real_world_scenario()
    example_library_integration()
    
    print("\n" + "=" * 60)
    print(" All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()