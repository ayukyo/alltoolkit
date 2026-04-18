"""
ISBN Parser Module

Provides functions to parse and get information about ISBN numbers.
"""

from dataclasses import dataclass
from typing import Optional
from .validator import (
    validate_isbn,
    ISBNType,
    calculate_check_digit_isbn10,
    calculate_check_digit_isbn13,
)
from .converter import isbn10_to_isbn13, isbn13_to_isbn10


@dataclass
class ISBNInfo:
    """Information about an ISBN number."""
    original: str           # Original input string
    cleaned: str            # Cleaned ISBN (no hyphens/spaces)
    isbn_type: ISBNType     # ISBN-10, ISBN-13, or Invalid
    is_valid: bool          # Whether the ISBN is valid
    check_digit: str        # The check digit
    prefix: Optional[str]   # ISBN-13 prefix (978 or 979), None for ISBN-10
    isbn10: Optional[str]   # ISBN-10 representation (if convertible)
    isbn13: Optional[str]   # ISBN-13 representation (if convertible)
    formatted_hyphen: str   # Hyphen-formatted ISBN
    formatted_space: str    # Space-formatted ISBN
    
    def __repr__(self) -> str:
        if not self.is_valid:
            return f"ISBNInfo(invalid='{self.original}')"
        return f"ISBNInfo({self.isbn_type.value}='{self.cleaned}')"


def parse_isbn(isbn: str) -> ISBNInfo:
    """
    Parse an ISBN string and return detailed information.
    
    Args:
        isbn: The ISBN string to parse
        
    Returns:
        ISBNInfo object with detailed information
    """
    import re
    from .formatter import format_isbn
    
    # Clean the ISBN
    cleaned = re.sub(r'[^0-9X]', '', isbn.upper())
    original = isbn
    
    # Validate
    is_valid, normalized, isbn_type, message = validate_isbn(isbn)
    
    if not is_valid or normalized is None:
        return ISBNInfo(
            original=original,
            cleaned=cleaned,
            isbn_type=ISBNType.INVALID,
            is_valid=False,
            check_digit="",
            prefix=None,
            isbn10=None,
            isbn13=None,
            formatted_hyphen=cleaned,
            formatted_space=cleaned,
        )
    
    # Get check digit
    check_digit = cleaned[-1]
    
    # Get prefix for ISBN-13
    prefix = None
    if isbn_type == ISBNType.ISBN13:
        prefix = cleaned[:3]
    
    # Get ISBN-10 and ISBN-13 representations
    isbn10 = None
    isbn13 = None
    
    if isbn_type == ISBNType.ISBN10:
        isbn10 = cleaned
        isbn13 = isbn10_to_isbn13(cleaned)
    elif isbn_type == ISBNType.ISBN13:
        isbn13 = cleaned
        isbn10 = isbn13_to_isbn10(cleaned)
    
    # Format ISBN
    formatted_hyphen = format_isbn(cleaned, "-")
    formatted_space = format_isbn(cleaned, " ")
    
    return ISBNInfo(
        original=original,
        cleaned=normalized,
        isbn_type=isbn_type,
        is_valid=True,
        check_digit=check_digit,
        prefix=prefix,
        isbn10=isbn10,
        isbn13=isbn13,
        formatted_hyphen=formatted_hyphen,
        formatted_space=formatted_space,
    )


def get_isbn_info(isbn: str) -> dict:
    """
    Get a dictionary of information about an ISBN number.
    
    This is a convenience function that returns the ISBNInfo as a dict.
    
    Args:
        isbn: The ISBN string to analyze
        
    Returns:
        Dictionary with ISBN information
    """
    info = parse_isbn(isbn)
    
    return {
        "original": info.original,
        "cleaned": info.cleaned,
        "type": info.isbn_type.value,
        "is_valid": info.is_valid,
        "check_digit": info.check_digit,
        "prefix": info.prefix,
        "isbn10": info.isbn10,
        "isbn13": info.isbn13,
        "formatted_hyphen": info.formatted_hyphen,
        "formatted_space": info.formatted_space,
    }


def detect_isbn_type(isbn: str) -> ISBNType:
    """
    Detect the type of an ISBN (ISBN-10, ISBN-13, or Invalid).
    
    Args:
        isbn: The ISBN string to check
        
    Returns:
        ISBNType enum value
    """
    _, _, isbn_type, _ = validate_isbn(isbn)
    return isbn_type


def get_prefix(isbn: str) -> Optional[str]:
    """
    Get the prefix of an ISBN-13 (978 or 979).
    
    Args:
        isbn: The ISBN string
        
    Returns:
        The prefix string, or None if not an ISBN-13
    """
    info = parse_isbn(isbn)
    return info.prefix


def get_equivalent_isbn10(isbn: str) -> Optional[str]:
    """
    Get the ISBN-10 equivalent of an ISBN.
    
    Args:
        isbn: The ISBN string
        
    Returns:
        ISBN-10 string, or None if not convertible
    """
    info = parse_isbn(isbn)
    return info.isbn10


def get_equivalent_isbn13(isbn: str) -> Optional[str]:
    """
    Get the ISBN-13 equivalent of an ISBN.
    
    Args:
        isbn: The ISBN string
        
    Returns:
        ISBN-13 string, or None if not valid
    """
    info = parse_isbn(isbn)
    return info.isbn13