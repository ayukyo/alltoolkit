"""
ISBN Generator Module

Provides functions to generate random valid ISBN numbers for testing purposes.
"""

import random
from typing import Optional, List
from .validator import calculate_check_digit_isbn10, calculate_check_digit_isbn13


def generate_isbn10(prefix: str = "", seed: Optional[int] = None) -> str:
    """
    Generate a random valid ISBN-10 number.
    
    Args:
        prefix: Optional prefix for the first few digits (1-8 digits)
        seed: Optional random seed for reproducible generation
        
    Returns:
        A valid ISBN-10 string
    """
    if seed is not None:
        random.seed(seed)
    
    # Clean prefix (remove non-digits)
    clean_prefix = ''.join(c for c in prefix if c.isdigit())
    
    # Limit prefix to 8 digits (need 1 digit for random generation)
    clean_prefix = clean_prefix[:8]
    
    # Generate remaining random digits
    remaining = 9 - len(clean_prefix)
    random_digits = ''.join(str(random.randint(0, 9)) for _ in range(remaining))
    
    # Build base (9 digits)
    base = clean_prefix + random_digits
    
    # Calculate check digit
    check_digit = calculate_check_digit_isbn10(base)
    
    if check_digit is None:
        # Fallback if calculation fails (shouldn't happen)
        check_digit = str(random.randint(0, 9))
    
    return base + check_digit


def generate_isbn13(prefix: str = "978", seed: Optional[int] = None) -> str:
    """
    Generate a random valid ISBN-13 number.
    
    Args:
        prefix: Optional prefix for the first few digits (default: "978")
                Use "979" for newer ISBNs
        seed: Optional random seed for reproducible generation
        
    Returns:
        A valid ISBN-13 string
    """
    if seed is not None:
        random.seed(seed)
    
    # Clean prefix (remove non-digits)
    clean_prefix = ''.join(c for c in prefix if c.isdigit())
    
    # Ensure prefix starts with 978 or 979
    if not clean_prefix.startswith(('978', '979')):
        clean_prefix = '978' + clean_prefix
    
    # Limit prefix to 12 digits (need 1 digit for check digit)
    clean_prefix = clean_prefix[:12]
    
    # Generate remaining random digits
    remaining = 12 - len(clean_prefix)
    random_digits = ''.join(str(random.randint(0, 9)) for _ in range(remaining))
    
    # Build base (12 digits)
    base = clean_prefix + random_digits
    
    # Calculate check digit
    check_digit = calculate_check_digit_isbn13(base)
    
    if check_digit is None:
        # Fallback if calculation fails (shouldn't happen)
        check_digit = str(random.randint(0, 9))
    
    return base + check_digit


def generate_random_isbn(format: str = "13", prefix: str = "", seed: Optional[int] = None) -> str:
    """
    Generate a random valid ISBN number.
    
    Args:
        format: ISBN format - "10" or "13" (default: "13")
        prefix: Optional prefix for the first few digits
        seed: Optional random seed for reproducible generation
        
    Returns:
        A valid ISBN string
    """
    format = format.lower()
    
    if format == "10":
        return generate_isbn10(prefix, seed)
    elif format == "13":
        return generate_isbn13(prefix, seed)
    else:
        raise ValueError(f"Invalid format: {format}. Must be '10' or '13'.")


def generate_isbn10_batch(count: int, prefix: str = "", seed: Optional[int] = None) -> List[str]:
    """
    Generate a batch of random valid ISBN-10 numbers.
    
    Args:
        count: Number of ISBNs to generate
        prefix: Optional prefix for the first few digits
        seed: Optional random seed for reproducible generation
        
    Returns:
        List of valid ISBN-10 strings
    """
    if seed is not None:
        random.seed(seed)
    
    return [generate_isbn10(prefix) for _ in range(count)]


def generate_isbn13_batch(count: int, prefix: str = "978", seed: Optional[int] = None) -> List[str]:
    """
    Generate a batch of random valid ISBN-13 numbers.
    
    Args:
        count: Number of ISBNs to generate
        prefix: Optional prefix for the first few digits
        seed: Optional random seed for reproducible generation
        
    Returns:
        List of valid ISBN-13 strings
    """
    if seed is not None:
        random.seed(seed)
    
    return [generate_isbn13(prefix) for _ in range(count)]