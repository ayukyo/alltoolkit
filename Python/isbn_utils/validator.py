"""
ISBN Validator Module

Provides validation functions for ISBN-10 and ISBN-13 formats.
"""

import re
from enum import Enum
from typing import Tuple, Optional


class ISBNType(Enum):
    """ISBN type enumeration."""
    ISBN10 = "ISBN-10"
    ISBN13 = "ISBN-13"
    INVALID = "Invalid"


def _clean_isbn(isbn: str) -> str:
    """
    Clean ISBN string by removing hyphens, spaces and other formatting.
    
    Args:
        isbn: The ISBN string to clean
        
    Returns:
        Cleaned ISBN string containing only digits and 'X'
    """
    return re.sub(r'[^0-9X]', '', isbn.upper())


def calculate_check_digit_isbn10(isbn: str) -> Optional[str]:
    """
    Calculate the check digit for an ISBN-10 number.
    
    ISBN-10 check digit is calculated using:
    (10*d1 + 9*d2 + 8*d3 + 7*d4 + 6*d5 + 5*d6 + 4*d7 + 3*d8 + 2*d9 + 1*d10) mod 11 = 0
    
    The check digit can be 0-10, where 10 is represented as 'X'.
    
    Args:
        isbn: The first 9 digits of an ISBN-10 (or full ISBN-10)
        
    Returns:
        The check digit character ('0'-'9' or 'X'), or None if invalid input
    """
    cleaned = _clean_isbn(isbn)
    
    # Need at least 9 digits
    if len(cleaned) < 9:
        return None
    
    # Use first 9 digits
    digits = cleaned[:9]
    
    if not digits.isdigit():
        return None
    
    # Calculate weighted sum
    total = sum((10 - i) * int(d) for i, d in enumerate(digits))
    
    # Calculate check digit
    check = (11 - (total % 11)) % 11
    
    return 'X' if check == 10 else str(check)


def calculate_check_digit_isbn13(isbn: str) -> Optional[str]:
    """
    Calculate the check digit for an ISBN-13 number.
    
    ISBN-13 uses the EAN-13 check digit algorithm:
    Sum of digits at odd positions + 3 * sum of digits at even positions
    Check digit = (10 - (sum % 10)) % 10
    
    Args:
        isbn: The first 12 digits of an ISBN-13 (or full ISBN-13)
        
    Returns:
        The check digit character ('0'-'9'), or None if invalid input
    """
    cleaned = _clean_isbn(isbn)
    
    # Need at least 12 digits
    if len(cleaned) < 12:
        return None
    
    # Use first 12 digits
    digits = cleaned[:12]
    
    if not digits.isdigit():
        return None
    
    # Calculate weighted sum (odd positions weight 1, even positions weight 3)
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits))
    
    # Calculate check digit
    check = (10 - (total % 10)) % 10
    
    return str(check)


def validate_isbn10(isbn: str) -> Tuple[bool, Optional[str], str]:
    """
    Validate an ISBN-10 number.
    
    Args:
        isbn: The ISBN-10 string to validate
        
    Returns:
        Tuple of (is_valid, normalized_isbn, message)
    """
    cleaned = _clean_isbn(isbn)
    
    if len(cleaned) != 10:
        return False, None, f"ISBN-10 must have 10 digits, got {len(cleaned)}"
    
    # Check first 9 characters are digits
    if not cleaned[:9].isdigit():
        return False, None, "First 9 characters must be digits"
    
    # Check last character (can be digit or X)
    if not (cleaned[9].isdigit() or cleaned[9] == 'X'):
        return False, None, "Check digit must be 0-9 or X"
    
    # Validate check digit
    expected = calculate_check_digit_isbn10(cleaned)
    actual = cleaned[9]
    
    if expected is None:
        return False, None, "Failed to calculate check digit"
    
    if actual != expected:
        return False, cleaned, f"Invalid check digit: expected {expected}, got {actual}"
    
    return True, cleaned, "Valid ISBN-10"


def validate_isbn13(isbn: str) -> Tuple[bool, Optional[str], str]:
    """
    Validate an ISBN-13 number.
    
    Args:
        isbn: The ISBN-13 string to validate
        
    Returns:
        Tuple of (is_valid, normalized_isbn, message)
    """
    cleaned = _clean_isbn(isbn)
    
    if len(cleaned) != 13:
        return False, None, f"ISBN-13 must have 13 digits, got {len(cleaned)}"
    
    if not cleaned.isdigit():
        return False, None, "ISBN-13 must contain only digits"
    
    # Validate check digit
    expected = calculate_check_digit_isbn13(cleaned)
    actual = cleaned[12]
    
    if expected is None:
        return False, None, "Failed to calculate check digit"
    
    if actual != expected:
        return False, cleaned, f"Invalid check digit: expected {expected}, got {actual}"
    
    return True, cleaned, "Valid ISBN-13"


def validate_isbn(isbn: str) -> Tuple[bool, Optional[str], ISBNType, str]:
    """
    Validate an ISBN number (automatically detect ISBN-10 or ISBN-13).
    
    Args:
        isbn: The ISBN string to validate
        
    Returns:
        Tuple of (is_valid, normalized_isbn, isbn_type, message)
    """
    cleaned = _clean_isbn(isbn)
    
    if len(cleaned) == 10:
        valid, normalized, msg = validate_isbn10(cleaned)
        return valid, normalized, ISBNType.ISBN10 if valid else ISBNType.INVALID, msg
    elif len(cleaned) == 13:
        valid, normalized, msg = validate_isbn13(cleaned)
        return valid, normalized, ISBNType.ISBN13 if valid else ISBNType.INVALID, msg
    else:
        return False, None, ISBNType.INVALID, f"ISBN must have 10 or 13 digits, got {len(cleaned)}"


def is_valid_isbn(isbn: str) -> bool:
    """
    Check if a string is a valid ISBN (10 or 13 digit format).
    
    Args:
        isbn: The ISBN string to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid, _, _, _ = validate_isbn(isbn)
    return valid


def is_valid_isbn10(isbn: str) -> bool:
    """
    Check if a string is a valid ISBN-10.
    
    Args:
        isbn: The ISBN string to validate
        
    Returns:
        True if valid ISBN-10, False otherwise
    """
    valid, _, _ = validate_isbn10(isbn)
    return valid


def is_valid_isbn13(isbn: str) -> bool:
    """
    Check if a string is a valid ISBN-13.
    
    Args:
        isbn: The ISBN string to validate
        
    Returns:
        True if valid ISBN-13, False otherwise
    """
    valid, _, _ = validate_isbn13(isbn)
    return valid