"""
ISBN Converter Module

Provides conversion functions between ISBN-10 and ISBN-13 formats.
"""

from typing import Optional
from .validator import (
    validate_isbn10,
    validate_isbn13,
    is_valid_isbn10,
    is_valid_isbn13,
    calculate_check_digit_isbn13,
    calculate_check_digit_isbn10,
)


def isbn10_to_isbn13(isbn10: str) -> Optional[str]:
    """
    Convert an ISBN-10 to ISBN-13 format.
    
    Conversion process:
    1. Remove the ISBN-10 check digit (last character)
    2. Prepend "978" (the bookland prefix)
    3. Calculate and append the new ISBN-13 check digit
    
    Args:
        isbn10: The ISBN-10 string to convert
        
    Returns:
        The ISBN-13 string, or None if conversion failed
    """
    valid, cleaned, _ = validate_isbn10(isbn10)
    
    if not valid or not cleaned:
        return None
    
    # Remove check digit, prepend 978
    isbn13_base = "978" + cleaned[:9]
    
    # Calculate new check digit
    check_digit = calculate_check_digit_isbn13(isbn13_base)
    
    if check_digit is None:
        return None
    
    return isbn13_base + check_digit


def isbn13_to_isbn10(isbn13: str) -> Optional[str]:
    """
    Convert an ISBN-13 to ISBN-10 format.
    
    Note: Only ISBN-13 numbers starting with "978" can be converted to ISBN-10.
    ISBN-13 numbers starting with "979" are not convertible.
    
    Conversion process:
    1. Verify the ISBN-13 starts with "978"
    2. Remove the "978" prefix and the ISBN-13 check digit
    3. Calculate and append the new ISBN-10 check digit
    
    Args:
        isbn13: The ISBN-13 string to convert
        
    Returns:
        The ISBN-10 string, or None if conversion failed
    """
    valid, cleaned, _ = validate_isbn13(isbn13)
    
    if not valid or not cleaned:
        return None
    
    # Can only convert 978-prefix ISBN-13s
    if not cleaned.startswith("978"):
        return None
    
    # Remove 978 prefix and check digit
    isbn10_base = cleaned[3:12]
    
    # Calculate new check digit
    check_digit = calculate_check_digit_isbn10(isbn10_base)
    
    if check_digit is None:
        return None
    
    return isbn10_base + check_digit


def convert_isbn(isbn: str) -> Optional[str]:
    """
    Convert an ISBN to the opposite format.
    
    - ISBN-10 -> ISBN-13
    - ISBN-13 -> ISBN-10 (only if it starts with 978)
    
    Args:
        isbn: The ISBN string to convert
        
    Returns:
        The converted ISBN string, or None if conversion failed
    """
    # Try ISBN-10 to ISBN-13
    if is_valid_isbn10(isbn):
        return isbn10_to_isbn13(isbn)
    
    # Try ISBN-13 to ISBN-10
    if is_valid_isbn13(isbn):
        return isbn13_to_isbn10(isbn)
    
    return None


def normalize_isbn(isbn: str, format: str = "13") -> Optional[str]:
    """
    Normalize an ISBN to a standard format.
    
    Args:
        isbn: The ISBN string to normalize
        format: Target format - "10" or "13" (default: "13")
        
    Returns:
        The normalized ISBN string, or None if normalization failed
    """
    from .validator import validate_isbn
    
    format = format.lower()
    
    if format not in ("10", "13"):
        return None
    
    # Validate input
    valid, cleaned, isbn_type, _ = validate_isbn(isbn)
    
    if not valid or not cleaned:
        return None
    
    # Determine current format
    is_10digit = len(cleaned) == 10
    is_13digit = len(cleaned) == 13
    
    if format == "13":
        if is_13digit:
            return cleaned
        elif is_10digit:
            return isbn10_to_isbn13(cleaned)
    elif format == "10":
        if is_10digit:
            return cleaned
        elif is_13digit:
            return isbn13_to_isbn10(cleaned)
    
    return None