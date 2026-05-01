#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - ISBN Utilities Module
===================================
A comprehensive ISBN (International Standard Book Number) utility module for Python
with zero external dependencies.

Features:
    - ISBN-10 and ISBN-13 validation
    - ISBN format conversion (ISBN-10 ↔ ISBN-13)
    - Check digit calculation
    - ISBN formatting with hyphens
    - ISBN generation for testing
    - ISBN parsing and component extraction
    - Batch validation support

Author: AllToolkit Contributors
License: MIT
"""

import re
from typing import Optional, Tuple, List, Dict, Union
from random import randint, choice


# ============================================================================
# Constants
# ============================================================================

# ISBN-13 prefix for book industry
ISBN_13_PREFIX = "978"
ISBN_13_PREFIX_ALT = "979"

# Valid ISBN-10 characters (0-9 and X for check digit)
ISBN_10_CHARS = set("0123456789X")

# Valid ISBN-13 characters (0-9 only)
ISBN_13_CHARS = set("0123456789")

# Common ISBN registration group prefixes (partial list)
REGISTRATION_GROUPS = {
    '0': {'name': 'English', 'countries': ['US', 'UK', 'Australia', 'Canada', 'New Zealand']},
    '1': {'name': 'English', 'countries': ['US', 'UK', 'Australia', 'Canada', 'New Zealand']},
    '2': {'name': 'French', 'countries': ['France', 'Belgium', 'Canada', 'Switzerland']},
    '3': {'name': 'German', 'countries': ['Germany', 'Austria', 'Switzerland']},
    '4': {'name': 'Japanese', 'countries': ['Japan']},
    '5': {'name': 'Russian', 'countries': ['Russia', 'Former USSR']},
    '7': {'name': 'Chinese', 'countries': ['China']},
    '80': {'name': 'Czech/Slovak', 'countries': ['Czech Republic', 'Slovakia']},
    '81': {'name': 'Indian', 'countries': ['India']},
    '82': {'name': 'Norwegian', 'countries': ['Norway']},
    '83': {'name': 'Polish', 'countries': ['Poland']},
    '84': {'name': 'Spanish', 'countries': ['Spain']},
    '85': {'name': 'Brazilian', 'countries': ['Brazil']},
    '86': {'name': 'Serbian', 'countries': ['Serbia']},
    '87': {'name': 'Danish', 'countries': ['Denmark']},
    '88': {'name': 'Italian', 'countries': ['Italy']},
    '89': {'name': 'Korean', 'countries': ['South Korea']},
    '90': {'name': 'Dutch', 'countries': ['Netherlands', 'Belgium']},
    '91': {'name': 'Swedish', 'countries': ['Sweden']},
    '92': {'name': 'International', 'countries': ['International organizations']},
    '93': {'name': 'Indian', 'countries': ['India']},
    '94': {'name': 'Dutch', 'countries': ['Netherlands']},
    '95': {'name': 'Iranian', 'countries': ['Iran']},
    '96': {'name': 'Turkish', 'countries': ['Turkey']},
    '97': {'name': 'International', 'countries': ['Various']},
    '98': {'name': 'International', 'countries': ['Various']},
    '99': {'name': 'International', 'countries': ['Various']},
}


# ============================================================================
# Core Functions
# ============================================================================

def clean_isbn(isbn: str) -> str:
    """
    Remove all non-digit and non-X characters from an ISBN.
    
    Args:
        isbn: The ISBN string to clean
        
    Returns:
        Cleaned ISBN string containing only digits and optionally 'X'
        
    Examples:
        >>> clean_isbn("978-0-306-40615-7")
        '9780306406157'
        >>> clean_isbn("ISBN 0-306-40615-X")
        '030640615X'
    """
    if not isbn:
        return ""
    # Keep digits and X (for ISBN-10 check digit)
    return ''.join(c.upper() if c.lower() == 'x' else c for c in isbn if c.isdigit() or c.lower() == 'x')


def is_isbn10(isbn: str) -> bool:
    """
    Check if a string is a valid ISBN-10.
    
    Args:
        isbn: The ISBN string to validate
        
    Returns:
        True if valid ISBN-10, False otherwise
        
    Examples:
        >>> is_isbn10("0306406152")
        True
        >>> is_isbn10("0-306-40615-X")
        True
        >>> is_isbn10("9780306406157")
        False
    """
    cleaned = clean_isbn(isbn)
    if len(cleaned) != 10:
        return False
    
    # Check all characters are valid (0-9 or X at last position)
    if not all(c in ISBN_10_CHARS for c in cleaned):
        return False
    
    # Check digit can be X, but only at the end
    if 'X' in cleaned[:-1]:
        return False
    
    return calculate_isbn10_check_digit(cleaned[:9]) == cleaned[9]


def is_isbn13(isbn: str) -> bool:
    """
    Check if a string is a valid ISBN-13.
    
    Args:
        isbn: The ISBN string to validate
        
    Returns:
        True if valid ISBN-13, False otherwise
        
    Examples:
        >>> is_isbn13("9780306406157")
        True
        >>> is_isbn13("978-0-306-40615-7")
        True
        >>> is_isbn13("0306406152")
        False
    """
    cleaned = clean_isbn(isbn)
    if len(cleaned) != 13:
        return False
    
    # ISBN-13 must start with 978 or 979
    if not cleaned.startswith((ISBN_13_PREFIX, ISBN_13_PREFIX_ALT)):
        return False
    
    # All characters must be digits
    if not cleaned.isdigit():
        return False
    
    return calculate_isbn13_check_digit(cleaned[:12]) == cleaned[12]


def is_valid_isbn(isbn: str) -> bool:
    """
    Check if a string is a valid ISBN (either ISBN-10 or ISBN-13).
    
    Args:
        isbn: The ISBN string to validate
        
    Returns:
        True if valid ISBN, False otherwise
        
    Examples:
        >>> is_valid_isbn("0306406152")
        True
        >>> is_valid_isbn("9780306406157")
        True
        >>> is_valid_isbn("invalid")
        False
    """
    return is_isbn10(isbn) or is_isbn13(isbn)


def get_isbn_type(isbn: str) -> Optional[str]:
    """
    Determine the type of an ISBN.
    
    Args:
        isbn: The ISBN string to check
        
    Returns:
        'ISBN-10', 'ISBN-13', or None if invalid
        
    Examples:
        >>> get_isbn_type("0306406152")
        'ISBN-10'
        >>> get_isbn_type("9780306406157")
        'ISBN-13'
    """
    if is_isbn10(isbn):
        return "ISBN-10"
    elif is_isbn13(isbn):
        return "ISBN-13"
    return None


# ============================================================================
# Check Digit Functions
# ============================================================================

def calculate_isbn10_check_digit(isbn9: str) -> str:
    """
    Calculate the ISBN-10 check digit.
    
    The check digit is calculated using weighted sum modulo 11.
    Weights are 10, 9, 8, 7, 6, 5, 4, 3, 2 for positions 1-9.
    
    Args:
        isbn9: First 9 digits of an ISBN-10
        
    Returns:
        The check digit (0-9 or 'X' for 10)
        
    Raises:
        ValueError: If isbn9 is not 9 digits
        
    Examples:
        >>> calculate_isbn10_check_digit("030640615")
        '2'
        >>> calculate_isbn10_check_digit("047195869")
        'X'
    """
    cleaned = clean_isbn(isbn9)
    if len(cleaned) != 9 or not cleaned.isdigit():
        raise ValueError("ISBN-9 must be exactly 9 digits")
    
    total = sum((10 - i) * int(d) for i, d in enumerate(cleaned))
    remainder = total % 11
    check = (11 - remainder) % 11
    
    return 'X' if check == 10 else str(check)


def calculate_isbn13_check_digit(isbn12: str) -> str:
    """
    Calculate the ISBN-13 check digit.
    
    Uses the standard EAN-13 algorithm with alternating weights 1 and 3.
    
    Args:
        isbn12: First 12 digits of an ISBN-13
        
    Returns:
        The check digit (0-9)
        
    Raises:
        ValueError: If isbn12 is not 12 digits
        
    Examples:
        >>> calculate_isbn13_check_digit("978030640615")
        '7'
    """
    cleaned = clean_isbn(isbn12)
    if len(cleaned) != 12 or not cleaned.isdigit():
        raise ValueError("ISBN-12 must be exactly 12 digits")
    
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(cleaned))
    check = (10 - (total % 10)) % 10
    
    return str(check)


# ============================================================================
# Conversion Functions
# ============================================================================

def isbn10_to_isbn13(isbn10: str) -> str:
    """
    Convert an ISBN-10 to ISBN-13.
    
    Args:
        isbn10: A valid ISBN-10 string
        
    Returns:
        The equivalent ISBN-13
        
    Raises:
        ValueError: If the input is not a valid ISBN-10
        
    Examples:
        >>> isbn10_to_isbn13("0306406152")
        '9780306406157'
        >>> isbn10_to_isbn13("0-306-40615-X")
        '978030640615X'
    """
    if not is_isbn10(isbn10):
        raise ValueError(f"Invalid ISBN-10: {isbn10}")
    
    cleaned = clean_isbn(isbn10)
    # Prefix with 978 and calculate new check digit
    isbn13_base = ISBN_13_PREFIX + cleaned[:9]
    check_digit = calculate_isbn13_check_digit(isbn13_base)
    
    return isbn13_base + check_digit


def isbn13_to_isbn10(isbn13: str) -> Optional[str]:
    """
    Convert an ISBN-13 to ISBN-10.
    
    Note: Only ISBN-13s starting with 978 can be converted to ISBN-10.
    ISBN-13s starting with 979 have no ISBN-10 equivalent.
    
    Args:
        isbn13: A valid ISBN-13 string
        
    Returns:
        The equivalent ISBN-10, or None if conversion is not possible
        
    Raises:
        ValueError: If the input is not a valid ISBN-13
        
    Examples:
        >>> isbn13_to_isbn10("9780306406157")
        '0306406152'
        >>> isbn13_to_isbn10("9790306406153")  # 979 prefix
        None
    """
    if not is_isbn13(isbn13):
        raise ValueError(f"Invalid ISBN-13: {isbn13}")
    
    cleaned = clean_isbn(isbn13)
    
    # Can only convert 978-prefixed ISBN-13s to ISBN-10
    if not cleaned.startswith(ISBN_13_PREFIX):
        return None
    
    # Remove 978 prefix and calculate new check digit
    isbn10_base = cleaned[3:12]
    check_digit = calculate_isbn10_check_digit(isbn10_base)
    
    return isbn10_base + check_digit


def convert_isbn(isbn: str, target_format: str = "ISBN-13") -> Optional[str]:
    """
    Convert an ISBN to the specified format.
    
    Args:
        isbn: A valid ISBN string
        target_format: Target format ('ISBN-10' or 'ISBN-13')
        
    Returns:
        The converted ISBN, or None if conversion is not possible
        
    Examples:
        >>> convert_isbn("0306406152", "ISBN-13")
        '9780306406157'
        >>> convert_isbn("9780306406157", "ISBN-10")
        '0306406152'
    """
    if not is_valid_isbn(isbn):
        return None
    
    source_type = get_isbn_type(isbn)
    
    if source_type == target_format:
        return clean_isbn(isbn)
    
    if target_format == "ISBN-13":
        return isbn10_to_isbn13(isbn)
    elif target_format == "ISBN-10":
        return isbn13_to_isbn10(isbn)
    
    return None


# ============================================================================
# Formatting Functions
# ============================================================================

def format_isbn(isbn: str, separator: str = "-") -> str:
    """
    Format an ISBN with standard hyphen separators.
    
    Args:
        isbn: A valid ISBN string
        separator: Character to use as separator (default: '-')
        
    Returns:
        Formatted ISBN string
        
    Examples:
        >>> format_isbn("0306406152")
        '0-306-40615-2'
        >>> format_isbn("9780306406157")
        '978-0-306-40615-7'
    """
    if not is_valid_isbn(isbn):
        raise ValueError(f"Invalid ISBN: {isbn}")
    
    cleaned = clean_isbn(isbn)
    
    if len(cleaned) == 10:
        # ISBN-10: group-publisher-title-check
        # Simple formatting based on common patterns
        group = cleaned[0]
        if group in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            # Try to identify group
            for prefix_len in range(2, 6):
                prefix = cleaned[:prefix_len]
                if prefix in REGISTRATION_GROUPS:
                    return f"{cleaned[:prefix_len]}{separator}{cleaned[prefix_len:-1]}{separator}{cleaned[-1]}"
            
            # Default formatting for ISBN-10
            # Common pattern: X-XXX-XXXXX-X
            if cleaned[0] in ('0', '1'):
                return f"{cleaned[0]}{separator}{cleaned[1:4]}{separator}{cleaned[4:9]}{separator}{cleaned[9]}"
            else:
                return f"{cleaned[0]}{separator}{cleaned[1:5]}{separator}{cleaned[5:9]}{separator}{cleaned[9]}"
    
    elif len(cleaned) == 13:
        # ISBN-13: prefix-group-publisher-title-check
        prefix = cleaned[:3]
        
        # Find group
        for prefix_len in range(1, 6):
            group_test = cleaned[3:3+prefix_len]
            full_prefix = prefix + group_test
            if group_test in REGISTRATION_GROUPS or full_prefix in REGISTRATION_GROUPS:
                remaining = cleaned[3+prefix_len:-1]
                # Distribute remaining digits
                if len(remaining) >= 4:
                    pub = remaining[:3]
                    title = remaining[3:]
                    return f"{prefix}{separator}{group_test}{separator}{pub}{separator}{title}{separator}{cleaned[-1]}"
        
        # Default formatting: XXX-X-XXX-XXXXX-X
        return f"{cleaned[:3]}{separator}{cleaned[3]}{separator}{cleaned[4:7]}{separator}{cleaned[7:12]}{separator}{cleaned[12]}"
    
    return cleaned


def format_isbn_compact(isbn: str) -> str:
    """
    Return ISBN in compact format (digits only, no separators).
    
    Args:
        isbn: An ISBN string (may contain separators)
        
    Returns:
        Compact ISBN string
        
    Examples:
        >>> format_isbn_compact("978-0-306-40615-7")
        '9780306406157'
    """
    return clean_isbn(isbn)


# ============================================================================
# Parsing Functions
# ============================================================================

def parse_isbn(isbn: str) -> Dict[str, any]:
    """
    Parse an ISBN and extract its components.
    
    Args:
        isbn: A valid ISBN string
        
    Returns:
        Dictionary with ISBN components and metadata
        
    Examples:
        >>> parse_isbn("978-0-306-40615-7")
        {
            'valid': True,
            'type': 'ISBN-13',
            'clean': '9780306406157',
            'formatted': '978-0-306-40615-7',
            'prefix': '978',
            'group': '0',
            'group_name': 'English',
            'check_digit': '7'
        }
    """
    result = {
        'valid': False,
        'type': None,
        'clean': clean_isbn(isbn),
        'formatted': None,
        'prefix': None,
        'group': None,
        'group_name': None,
        'publisher': None,
        'title': None,
        'check_digit': None,
        'isbn10': None,
        'isbn13': None,
    }
    
    if not is_valid_isbn(isbn):
        return result
    
    result['valid'] = True
    cleaned = result['clean']
    result['check_digit'] = cleaned[-1]
    
    if len(cleaned) == 10:
        result['type'] = 'ISBN-10'
        result['group'] = cleaned[0]
        result['isbn10'] = cleaned
        result['isbn13'] = isbn10_to_isbn13(isbn)
        result['formatted'] = format_isbn(cleaned)
    else:
        result['type'] = 'ISBN-13'
        result['prefix'] = cleaned[:3]
        result['group'] = cleaned[3]
        result['isbn13'] = cleaned
        result['isbn10'] = isbn13_to_isbn10(isbn)
        result['formatted'] = format_isbn(cleaned)
    
    # Get group name
    if result['group'] in REGISTRATION_GROUPS:
        result['group_name'] = REGISTRATION_GROUPS[result['group']]['name']
    
    return result


# ============================================================================
# Generation Functions
# ============================================================================

def generate_isbn10(group: str = "0", publisher: str = None) -> str:
    """
    Generate a random valid ISBN-10.
    
    Args:
        group: Registration group digit (default: '0' for English)
        publisher: Publisher digits (random if not provided)
        
    Returns:
        A valid ISBN-10 string
        
    Examples:
        >>> isbn = generate_isbn10()
        >>> is_isbn10(isbn)
        True
    """
    if publisher is None:
        # Generate random publisher (3-4 digits)
        publisher_len = choice([3, 4])
        publisher = ''.join(str(randint(0, 9)) for _ in range(publisher_len))
    
    # Generate random title digits to make total 9 digits
    remaining = 9 - 1 - len(publisher)  # -1 for group digit
    title = ''.join(str(randint(0, 9)) for _ in range(remaining))
    
    isbn9 = group + publisher + title
    check = calculate_isbn10_check_digit(isbn9)
    
    return isbn9 + check


def generate_isbn13(prefix: str = "978", group: str = "0", publisher: str = None) -> str:
    """
    Generate a random valid ISBN-13.
    
    Args:
        prefix: ISBN-13 prefix ('978' or '979')
        group: Registration group digit (default: '0' for English)
        publisher: Publisher digits (random if not provided)
        
    Returns:
        A valid ISBN-13 string
        
    Examples:
        >>> isbn = generate_isbn13()
        >>> is_isbn13(isbn)
        True
    """
    if prefix not in (ISBN_13_PREFIX, ISBN_13_PREFIX_ALT):
        prefix = ISBN_13_PREFIX
    
    if publisher is None:
        # Generate random publisher (3-4 digits)
        publisher_len = choice([3, 4])
        publisher = ''.join(str(randint(0, 9)) for _ in range(publisher_len))
    
    # Generate random title digits to make total 12 digits
    # prefix(3) + group(1) + publisher + title = 12
    remaining = 12 - 3 - 1 - len(publisher)
    title = ''.join(str(randint(0, 9)) for _ in range(remaining))
    
    isbn12 = prefix + group + publisher + title
    check = calculate_isbn13_check_digit(isbn12)
    
    return isbn12 + check


def generate_isbn(isbn_type: str = "ISBN-13", **kwargs) -> str:
    """
    Generate a random valid ISBN of specified type.
    
    Args:
        isbn_type: 'ISBN-10' or 'ISBN-13' (default: 'ISBN-13')
        **kwargs: Additional arguments passed to generate_isbn10 or generate_isbn13
        
    Returns:
        A valid ISBN string
        
    Examples:
        >>> is_isbn10(generate_isbn("ISBN-10"))
        True
        >>> is_isbn13(generate_isbn("ISBN-13"))
        True
    """
    if isbn_type == "ISBN-10":
        return generate_isbn10(**kwargs)
    else:
        return generate_isbn13(**kwargs)


# ============================================================================
# Batch Functions
# ============================================================================

def validate_isbns(isbns: List[str]) -> Dict[str, Dict]:
    """
    Validate multiple ISBNs at once.
    
    Args:
        isbns: List of ISBN strings to validate
        
    Returns:
        Dictionary mapping each ISBN to its validation result
        
    Examples:
        >>> results = validate_isbns(["0306406152", "invalid", "9780306406157"])
        >>> results["0306406152"]["valid"]
        True
        >>> results["invalid"]["valid"]
        False
    """
    results = {}
    for isbn in isbns:
        results[isbn] = parse_isbn(isbn)
    return results


def find_isbns_in_text(text: str) -> List[str]:
    """
    Find all potential ISBNs in a text string.
    
    Args:
        text: Text to search for ISBNs
        
    Returns:
        List of valid ISBNs found in the text
        
    Examples:
        >>> find_isbns_in_text("The book ISBN 978-0-306-40615-7 is great!")
        ['9780306406157']
    """
    # Pattern to match potential ISBNs (with or without hyphens)
    # ISBN-10: 10 digits with optional X at end
    # ISBN-13: 13 digits starting with 978 or 979
    pattern = r'\b(?:ISBN[-\s]?)?(?:(?:97[89][- ]?[0-9]{1,5}[- ]?[0-9]{1,7}[- ]?[0-9][- ]?[0-9])|(?:[0-9]{1,5}[- ]?[0-9]{1,7}[- ]?[0-9X]))\b'
    
    matches = re.findall(r'[\dX-]+', text, re.IGNORECASE)
    
    valid_isbns = []
    for match in matches:
        cleaned = clean_isbn(match)
        if is_valid_isbn(cleaned) and cleaned not in valid_isbns:
            valid_isbns.append(cleaned)
    
    return valid_isbns


# ============================================================================
# Utility Functions
# ============================================================================

def compare_isbns(isbn1: str, isbn2: str) -> bool:
    """
    Check if two ISBNs are equivalent (same book).
    
    ISBN-10 and ISBN-13 of the same book are considered equivalent.
    
    Args:
        isbn1: First ISBN
        isbn2: Second ISBN
        
    Returns:
        True if ISBNs refer to the same book
        
    Examples:
        >>> compare_isbns("0306406152", "9780306406157")
        True
        >>> compare_isbns("0306406152", "9780306406158")
        False
    """
    if not is_valid_isbn(isbn1) or not is_valid_isbn(isbn2):
        return False
    
    # Convert both to ISBN-13 for comparison
    isbn1_13 = isbn10_to_isbn13(isbn1) if is_isbn10(isbn1) else clean_isbn(isbn1)
    isbn2_13 = isbn10_to_isbn13(isbn2) if is_isbn10(isbn2) else clean_isbn(isbn2)
    
    return isbn1_13 == isbn2_13


def get_isbn_variants(isbn: str) -> Dict[str, Optional[str]]:
    """
    Get all variants of an ISBN.
    
    Args:
        isbn: A valid ISBN string
        
    Returns:
        Dictionary with 'isbn10', 'isbn13', 'formatted10', 'formatted13'
        
    Examples:
        >>> get_isbn_variants("0306406152")
        {
            'isbn10': '0306406152',
            'isbn13': '9780306406157',
            'formatted10': '0-306-40615-2',
            'formatted13': '978-0-306-40615-7'
        }
    """
    if not is_valid_isbn(isbn):
        return {
            'isbn10': None,
            'isbn13': None,
            'formatted10': None,
            'formatted13': None
        }
    
    isbn10 = clean_isbn(isbn) if is_isbn10(isbn) else isbn13_to_isbn10(isbn)
    isbn13 = clean_isbn(isbn) if is_isbn13(isbn) else isbn10_to_isbn13(isbn)
    
    return {
        'isbn10': isbn10,
        'isbn13': isbn13,
        'formatted10': format_isbn(isbn10) if isbn10 else None,
        'formatted13': format_isbn(isbn13) if isbn13 else None
    }


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Demo usage
    print("=" * 60)
    print("ISBN Utilities Demo")
    print("=" * 60)
    
    # Test ISBNs
    test_isbns = [
        "0306406152",      # Valid ISBN-10
        "9780306406157",   # Valid ISBN-13
        "0-306-40615-X",   # ISBN-10 with X check digit and hyphens
        "invalid",         # Invalid
    ]
    
    for isbn in test_isbns:
        print(f"\nISBN: {isbn}")
        print(f"  Valid: {is_valid_isbn(isbn)}")
        print(f"  Type: {get_isbn_type(isbn)}")
        if is_valid_isbn(isbn):
            info = parse_isbn(isbn)
            print(f"  Clean: {info['clean']}")
            print(f"  Formatted: {info['formatted']}")
            variants = get_isbn_variants(isbn)
            print(f"  ISBN-10: {variants['isbn10']}")
            print(f"  ISBN-13: {variants['isbn13']}")
    
    print("\n" + "=" * 60)
    print("Generated ISBNs:")
    print("=" * 60)
    for _ in range(3):
        isbn10 = generate_isbn10()
        isbn13 = generate_isbn13()
        print(f"  ISBN-10: {format_isbn(isbn10)} -> {is_isbn10(isbn10)}")
        print(f"  ISBN-13: {format_isbn(isbn13)} -> {is_isbn13(isbn13)}")