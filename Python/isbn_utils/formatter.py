"""
ISBN Formatter Module

Provides functions to format and extract ISBN numbers from text.
"""

import re
from typing import Optional, List, Tuple
from .validator import (
    is_valid_isbn10,
    is_valid_isbn13,
    is_valid_isbn,
    validate_isbn,
    ISBNType,
)


def format_isbn10(isbn: str, separator: str = "-") -> str:
    """
    Format an ISBN-10 with standard hyphenation.
    
    Standard format: X-XXXXX-XXX-X (group-publisher-title-check)
    Note: This is a simplified formatting that uses common patterns.
    Accurate hyphenation requires the official ISBN ranges database.
    
    Args:
        isbn: The ISBN-10 string to format
        separator: The separator character (default: "-")
        
    Returns:
        Formatted ISBN-10 string
    """
    # Clean the ISBN
    cleaned = re.sub(r'[^0-9X]', '', isbn.upper())
    
    if len(cleaned) != 10:
        return isbn  # Return original if invalid
    
    # Common format: 0 or 1 as group identifier for English
    # Simplified format: X-XXXXX-XXX-X
    return separator.join([
        cleaned[0],      # Group (simplified)
        cleaned[1:6],   # Publisher + Title
        cleaned[6:9],   # Title continued
        cleaned[9]      # Check digit
    ])


def format_isbn13(isbn: str, separator: str = "-") -> str:
    """
    Format an ISBN-13 with standard hyphenation.
    
    Standard format: XXX-X-XXXXX-XXX-X (prefix-group-publisher-title-check)
    Note: This is a simplified formatting that uses common patterns.
    Accurate hyphenation requires the official ISBN ranges database.
    
    Args:
        isbn: The ISBN-13 string to format
        separator: The separator character (default: "-")
        
    Returns:
        Formatted ISBN-13 string
    """
    # Clean the ISBN
    cleaned = re.sub(r'[^0-9]', '', isbn)
    
    if len(cleaned) != 13:
        return isbn  # Return original if invalid
    
    # Simplified format: XXX-X-XXXXX-XXX-X
    return separator.join([
        cleaned[0:3],    # Prefix (978 or 979)
        cleaned[3],      # Group (simplified)
        cleaned[4:9],    # Publisher + Title
        cleaned[9:12],   # Title continued
        cleaned[12]      # Check digit
    ])


def format_isbn(isbn: str, separator: str = "-") -> str:
    """
    Format an ISBN with standard hyphenation.
    
    Automatically detects ISBN-10 or ISBN-13 format.
    
    Args:
        isbn: The ISBN string to format
        separator: The separator character (default: "-")
        
    Returns:
        Formatted ISBN string
    """
    # Clean the ISBN
    cleaned = re.sub(r'[^0-9X]', '', isbn.upper())
    
    if len(cleaned) == 10:
        return format_isbn10(cleaned, separator)
    elif len(cleaned) == 13:
        return format_isbn13(cleaned, separator)
    else:
        return isbn  # Return original if invalid


def extract_isbn(text: str) -> Optional[str]:
    """
    Extract the first valid ISBN from a text string.
    
    Supports various formats:
    - 10 or 13 consecutive digits
    - ISBN with hyphens
    - ISBN with spaces
    - ISBN prefixed with "ISBN" or "ISBN-10" or "ISBN-13"
    
    Args:
        text: The text to search for ISBN
        
    Returns:
        The first valid ISBN found, or None
    """
    # Pattern to match potential ISBNs
    # Matches: ISBN, ISBN-10, ISBN-13, or just digits with optional separators
    patterns = [
        # ISBN-13 with prefix
        r'ISBN[-\s]?13[:\s]*([0-9]{1,5}[-\s]?[0-9]{1,7}[-\s]?[0-9]{1,7}[-\s]?[0-9X])',
        # ISBN-10 with prefix
        r'ISBN[-\s]?10[:\s]*([0-9]{1,5}[-\s]?[0-9]{1,7}[-\s]?[0-9]{1,7}[-\s]?[0-9X])',
        # ISBN with prefix (any)
        r'ISBN[:\s]*([0-9]{1,5}[-\s]?[0-9]{1,7}[-\s]?[0-9]{1,7}[-\s]?[0-9X])',
        # ISBN-13 without prefix (13 digits with optional hyphens)
        r'\b([0-9]{3}[-\s]?[0-9][-\s]?[0-9]{2,6}[-\s]?[0-9]{2,6}[-\s]?[0-9X])\b',
        # ISBN-10 without prefix (10 chars with optional hyphens)
        r'\b([0-9][-\s]?[0-9]{2,6}[-\s]?[0-9]{2,6}[-\s]?[0-9X])\b',
        # Plain digits (10 or 13 consecutive)
        r'\b([0-9X]{10,13})\b',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            candidate = match.group(1)
            # Clean and validate
            cleaned = re.sub(r'[^0-9X]', '', candidate.upper())
            if is_valid_isbn(cleaned):
                return cleaned
    
    return None


def extract_all_isbn(text: str) -> List[str]:
    """
    Extract all valid ISBNs from a text string.
    
    Args:
        text: The text to search for ISBNs
        
    Returns:
        List of all valid ISBNs found (unique, in order of appearance)
    """
    found = []
    seen = set()
    
    # Pattern to match potential ISBNs (various formats)
    patterns = [
        # ISBN with prefix
        r'ISBN[-\s]?1[03]?[:\s]*([0-9]{1,5}[-\s]?[0-9]{1,7}[-\s]?[0-9]{1,7}[-\s]?[0-9X])',
        # ISBN without prefix (with hyphens/spaces)
        r'\b([0-9][-\s]?[0-9]{2,6}[-\s]?[0-9]{2,6}[-\s]?[0-9X])\b',
        # Plain digits (10 or 13 consecutive)
        r'\b([0-9X]{10,13})\b',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            candidate = match.group(1)
            # Clean and validate
            cleaned = re.sub(r'[^0-9X]', '', candidate.upper())
            if is_valid_isbn(cleaned) and cleaned not in seen:
                found.append(cleaned)
                seen.add(cleaned)
    
    return found