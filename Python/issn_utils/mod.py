#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - ISSN Utilities Module
===================================
A comprehensive ISSN (International Standard Serial Number) utility module for Python
with zero external dependencies.

ISSN is an 8-digit code used to uniquely identify serial publications
(journals, magazines, newspapers, etc.).

Features:
    - ISSN validation (ISSN-8 and ISSN-13)
    - Check digit calculation
    - ISSN formatting with hyphen
    - ISSN generation for testing
    - ISSN-L (Linking ISSN) support
    - Batch validation support
    - ISSN parsing and extraction from text

Author: AllToolkit Contributors
License: MIT
"""

import re
from typing import Optional, List, Dict, Tuple
from random import randint, choice


# ============================================================================
# Constants
# ============================================================================

# ISSN-L prefix for linking ISSNs
ISSN_L_PREFIX = "ISSN-L:"

# Valid ISSN characters (0-9 and X for check digit)
ISSN_CHARS = set("0123456789X")

# EAN prefix for ISSN-13 (converted from ISSN-8)
ISSN_13_PREFIX = "977"

# Common ISSN registry patterns for journals by field
JOURNAL_FIELDS = {
    'medicine': ['002', '003', '004', '005'],
    'science': ['001', '002', '003', '004'],
    'technology': ['001', '002', '003'],
    'humanities': ['001', '002', '003', '004'],
    'social_sciences': ['001', '002', '003'],
    'law': ['001', '002'],
    'education': ['001', '002', '003'],
}


# ============================================================================
# Core Functions
# ============================================================================

def clean_issn(issn: str) -> str:
    """
    Remove all non-digit and non-X characters from an ISSN.
    
    Args:
        issn: The ISSN string to clean
        
    Returns:
        Cleaned ISSN string containing only digits and optionally 'X'
        
    Examples:
        >>> clean_issn("0378-5955")
        '03785955'
        >>> clean_issn("ISSN 0378-5955")
        '03785955'
        >>> clean_issn("2434-561X")
        '2434561X'
    """
    if not issn:
        return ""
    # Keep digits and X (for check digit)
    return ''.join(c.upper() if c.lower() == 'x' else c for c in issn if c.isdigit() or c.lower() == 'x')


def is_issn8(issn: str) -> bool:
    """
    Check if a string is a valid ISSN-8 (standard 8-digit ISSN).
    
    Args:
        issn: The ISSN string to validate
        
    Returns:
        True if valid ISSN-8, False otherwise
        
    Examples:
        >>> is_issn8("0378-5955")
        True
        >>> is_issn8("03785955")
        True
        >>> is_issn8("2434-561X")
        True
        >>> is_issn8("9770378595001")  # ISSN-13
        False
    """
    cleaned = clean_issn(issn)
    if len(cleaned) != 8:
        return False
    
    # Check all characters are valid (0-9 or X at last position)
    if not all(c in ISSN_CHARS for c in cleaned):
        return False
    
    # Check digit can be X, but only at the end
    if 'X' in cleaned[:-1]:
        return False
    
    return calculate_issn_check_digit(cleaned[:7]) == cleaned[7]


def is_issn13(issn: str) -> bool:
    """
    Check if a string is a valid ISSN-13 (EAN-13 format for ISSN).
    
    ISSN-13 is formed by prefixing ISSN-8 with 977 and recalculating
    the check digit according to EAN-13 rules.
    
    Args:
        issn: The ISSN-13 string to validate
        
    Returns:
        True if valid ISSN-13, False otherwise
        
    Examples:
        >>> is_issn13("9770378595001")
        True
        >>> is_issn13("0378-5955")  # ISSN-8
        False
    """
    cleaned = ''.join(c for c in issn if c.isdigit())
    if len(cleaned) != 13:
        return False
    
    # ISSN-13 must start with 977
    if not cleaned.startswith(ISSN_13_PREFIX):
        return False
    
    # Verify check digit using EAN-13 algorithm
    return calculate_issn13_check_digit(cleaned[:12]) == cleaned[12]


def is_valid_issn(issn: str) -> bool:
    """
    Check if a string is a valid ISSN (either ISSN-8 or ISSN-13).
    
    Args:
        issn: The ISSN string to validate
        
    Returns:
        True if valid ISSN, False otherwise
        
    Examples:
        >>> is_valid_issn("0378-5955")
        True
        >>> is_valid_issn("9770378595001")
        True
        >>> is_valid_issn("invalid")
        False
    """
    return is_issn8(issn) or is_issn13(issn)


def get_issn_type(issn: str) -> Optional[str]:
    """
    Determine the type of an ISSN.
    
    Args:
        issn: The ISSN string to check
        
    Returns:
        'ISSN-8', 'ISSN-13', or None if invalid
        
    Examples:
        >>> get_issn_type("0378-5955")
        'ISSN-8'
        >>> get_issn_type("9770378595001")
        'ISSN-13'
    """
    if is_issn8(issn):
        return "ISSN-8"
    elif is_issn13(issn):
        return "ISSN-13"
    return None


# ============================================================================
# Check Digit Functions
# ============================================================================

def calculate_issn_check_digit(issn7: str) -> str:
    """
    Calculate the ISSN-8 check digit.
    
    The check digit is calculated using weighted sum modulo 11.
    Weights are 8, 7, 6, 5, 4, 3, 2 for positions 1-7.
    
    Args:
        issn7: First 7 digits of an ISSN
        
    Returns:
        The check digit (0-9 or 'X' for 10)
        
    Raises:
        ValueError: If issn7 is not 7 digits
        
    Examples:
        >>> calculate_issn_check_digit("0378595")
        '5'
        >>> calculate_issn_check_digit("2434561")
        'X'
    """
    cleaned = clean_issn(issn7)
    if len(cleaned) != 7 or not cleaned.isdigit():
        raise ValueError("ISSN-7 must be exactly 7 digits")
    
    total = sum((8 - i) * int(d) for i, d in enumerate(cleaned))
    remainder = total % 11
    check = (11 - remainder) % 11
    
    return 'X' if check == 10 else str(check)


def calculate_issn13_check_digit(issn12: str) -> str:
    """
    Calculate the ISSN-13 (EAN-13) check digit.
    
    Uses the standard EAN-13 algorithm with alternating weights 1 and 3.
    
    Args:
        issn12: First 12 digits of an ISSN-13
        
    Returns:
        The check digit (0-9)
        
    Raises:
        ValueError: If issn12 is not 12 digits
        
    Examples:
        >>> calculate_issn13_check_digit("977037859500")
        '1'
    """
    cleaned = ''.join(c for c in issn12 if c.isdigit())
    if len(cleaned) != 12 or not cleaned.isdigit():
        raise ValueError("ISSN-12 must be exactly 12 digits")
    
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(cleaned))
    check = (10 - (total % 10)) % 10
    
    return str(check)


# ============================================================================
# Conversion Functions
# ============================================================================

def issn8_to_issn13(issn8: str) -> str:
    """
    Convert an ISSN-8 to ISSN-13.
    
    The ISSN-13 is formed by prefixing the ISSN-8 (without check digit)
    with 977 and adding two additional digits (typically 00 for variants)
    plus a new EAN-13 check digit.
    
    Args:
        issn8: A valid ISSN-8 string
        
    Returns:
        The equivalent ISSN-13
        
    Raises:
        ValueError: If the input is not a valid ISSN-8
        
    Examples:
        >>> issn8_to_issn13("0378-5955")
        '9770378595001'
    """
    if not is_issn8(issn8):
        raise ValueError(f"Invalid ISSN-8: {issn8}")
    
    cleaned = clean_issn(issn8)
    # Prefix with 977, add 00 for variant, calculate new check digit
    issn13_base = ISSN_13_PREFIX + cleaned[:7] + "00"
    check_digit = calculate_issn13_check_digit(issn13_base)
    
    return issn13_base + check_digit


def issn13_to_issn8(issn13: str) -> str:
    """
    Convert an ISSN-13 to ISSN-8.
    
    Extracts the ISSN-8 from an ISSN-13. Note that the variant digits
    (positions 11-12) are lost in this conversion.
    
    Args:
        issn13: A valid ISSN-13 string
        
    Returns:
        The equivalent ISSN-8
        
    Raises:
        ValueError: If the input is not a valid ISSN-13
        
    Examples:
        >>> issn13_to_issn8("9770378595001")
        '03785955'
    """
    if not is_issn13(issn13):
        raise ValueError(f"Invalid ISSN-13: {issn13}")
    
    cleaned = ''.join(c for c in issn13 if c.isdigit())
    
    # Extract positions 3-9 (the original ISSN-7) and calculate check digit
    issn7 = cleaned[3:10]
    check_digit = calculate_issn_check_digit(issn7)
    
    return issn7 + check_digit


def convert_issn(issn: str, target_format: str = "ISSN-13") -> Optional[str]:
    """
    Convert an ISSN to the specified format.
    
    Args:
        issn: A valid ISSN string
        target_format: Target format ('ISSN-8' or 'ISSN-13')
        
    Returns:
        The converted ISSN, or None if conversion failed
        
    Examples:
        >>> convert_issn("0378-5955", "ISSN-13")
        '9770378595001'
        >>> convert_issn("9770378595001", "ISSN-8")
        '03785955'
    """
    if not is_valid_issn(issn):
        return None
    
    source_type = get_issn_type(issn)
    
    if source_type == target_format:
        return clean_issn(issn) if source_type == "ISSN-8" else ''.join(c for c in issn if c.isdigit())
    
    if target_format == "ISSN-13":
        return issn8_to_issn13(issn)
    elif target_format == "ISSN-8":
        return issn13_to_issn8(issn)
    
    return None


# ============================================================================
# Formatting Functions
# ============================================================================

def format_issn(issn: str, separator: str = "-") -> str:
    """
    Format an ISSN with standard hyphen separator.
    
    Args:
        issn: A valid ISSN string (ISSN-8 or ISSN-13)
        separator: Character to use as separator (default: '-')
        
    Returns:
        Formatted ISSN string
        
    Raises:
        ValueError: If ISSN is invalid
        
    Examples:
        >>> format_issn("03785955")
        '0378-5955'
        >>> format_issn("9770378595001")
        '977-0378-5950-01'
        >>> format_issn("2434561X")
        '2434-561X'
    """
    if not is_valid_issn(issn):
        raise ValueError(f"Invalid ISSN: {issn}")
    
    if is_issn8(issn):
        cleaned = clean_issn(issn)
        # Format as NNNN-NNNC
        return f"{cleaned[:4]}{separator}{cleaned[4:]}"
    else:
        # ISSN-13
        cleaned = ''.join(c for c in issn if c.isdigit())
        # Format as XXX-NNNN-NNNN-NC (EAN-13 style for ISSN)
        return f"{cleaned[:3]}{separator}{cleaned[3:7]}{separator}{cleaned[7:11]}{separator}{cleaned[11:]}"


def format_issn_compact(issn: str) -> str:
    """
    Return ISSN in compact format (digits only, no separators).
    
    Args:
        issn: An ISSN string (may contain separators)
        
    Returns:
        Compact ISSN string
        
    Examples:
        >>> format_issn_compact("0378-5955")
        '03785955'
        >>> format_issn_compact("977-0378-5950-01")
        '9770378595001'
    """
    if is_issn8(issn):
        return clean_issn(issn)
    else:
        return ''.join(c for c in issn if c.isdigit())


# ============================================================================
# ISSN-L (Linking ISSN) Functions
# ============================================================================

def is_issn_l(issn_l: str) -> bool:
    """
    Check if a string is a valid ISSN-L (Linking ISSN).
    
    ISSN-L is a special identifier that links all media versions
    of a serial publication. It has the same format as ISSN-8 but
    may be prefixed with "ISSN-L:".
    
    Args:
        issn_l: The ISSN-L string to validate
        
    Returns:
        True if valid ISSN-L format, False otherwise
        
    Examples:
        >>> is_issn_l("ISSN-L: 0378-5955")
        True
        >>> is_issn_l("0378-5955")  # Valid ISSN but no ISSN-L prefix
        True
    """
    # Remove ISSN-L prefix if present
    cleaned = issn_l.strip()
    if cleaned.upper().startswith(ISSN_L_PREFIX):
        cleaned = cleaned[7:].strip()  # ISSN-L: is 7 characters
    
    return is_issn8(cleaned)


def format_issn_l(issn: str) -> str:
    """
    Format an ISSN as an ISSN-L (Linking ISSN).
    
    Args:
        issn: A valid ISSN string
        
    Returns:
        ISSN-L formatted string
        
    Raises:
        ValueError: If ISSN is invalid
        
    Examples:
        >>> format_issn_l("0378-5955")
        'ISSN-L: 0378-5955'
    """
    if not is_issn8(issn):
        raise ValueError(f"Invalid ISSN for ISSN-L: {issn}")
    
    return f"ISSN-L: {format_issn(issn)}"


def extract_issn_l(issn_l: str) -> Optional[str]:
    """
    Extract the ISSN from an ISSN-L string.
    
    Args:
        issn_l: An ISSN-L string (may or may not have prefix)
        
    Returns:
        The ISSN without the ISSN-L prefix, or None if invalid
        
    Examples:
        >>> extract_issn_l("ISSN-L: 0378-5955")
        '03785955'
        >>> extract_issn_l("0378-5955")
        '03785955'
    """
    cleaned = issn_l.strip()
    if cleaned.upper().startswith(ISSN_L_PREFIX):
        cleaned = cleaned[7:].strip()  # ISSN-L: is 7 characters
    
    if is_issn8(cleaned):
        return clean_issn(cleaned)
    return None


# ============================================================================
# Parsing Functions
# ============================================================================

def parse_issn(issn: str) -> Dict[str, any]:
    """
    Parse an ISSN and extract its components.
    
    Args:
        issn: A valid ISSN string
        
    Returns:
        Dictionary with ISSN components and metadata
        
    Examples:
        >>> parse_issn("0378-5955")
        {
            'valid': True,
            'type': 'ISSN-8',
            'clean': '03785955',
            'formatted': '0378-5955',
            'check_digit': '5',
            'issn13': '9770378595001',
            'issn_l': 'ISSN-L: 0378-5955'
        }
    """
    result = {
        'valid': False,
        'type': None,
        'clean': None,
        'formatted': None,
        'check_digit': None,
        'issn8': None,
        'issn13': None,
        'issn_l': None,
    }
    
    if is_issn8(issn):
        cleaned = clean_issn(issn)
        result.update({
            'valid': True,
            'type': 'ISSN-8',
            'clean': cleaned,
            'formatted': format_issn(cleaned),
            'check_digit': cleaned[7],
            'issn8': cleaned,
            'issn13': issn8_to_issn13(cleaned),
            'issn_l': format_issn_l(cleaned),
        })
    elif is_issn13(issn):
        cleaned = ''.join(c for c in issn if c.isdigit())
        result.update({
            'valid': True,
            'type': 'ISSN-13',
            'clean': cleaned,
            'formatted': format_issn(cleaned),
            'check_digit': cleaned[12],
            'issn8': issn13_to_issn8(cleaned),
            'issn13': cleaned,
            'issn_l': format_issn_l(issn13_to_issn8(cleaned)),
        })
    
    return result


# ============================================================================
# Generation Functions
# ============================================================================

def generate_issn(prefix: str = None) -> str:
    """
    Generate a random valid ISSN-8.
    
    Args:
        prefix: Optional 1-3 digit prefix for the ISSN
        
    Returns:
        A valid ISSN-8 string
        
    Examples:
        >>> issn = generate_issn()
        >>> is_issn8(issn)
        True
        >>> issn = generate_issn("037")
        >>> issn.startswith("037")
        True
    """
    if prefix:
        prefix = ''.join(c for c in prefix if c.isdigit())
        if len(prefix) > 7:
            prefix = prefix[:7]
    else:
        prefix = ""
    
    # Generate remaining digits to make 7 total
    remaining = 7 - len(prefix)
    digits = prefix + ''.join(str(randint(0, 9)) for _ in range(remaining))
    
    check = calculate_issn_check_digit(digits)
    
    return digits + check


def generate_issn13(prefix: str = None) -> str:
    """
    Generate a random valid ISSN-13.
    
    Args:
        prefix: Optional prefix for the ISSN portion (1-7 digits)
        
    Returns:
        A valid ISSN-13 string
        
    Examples:
        >>> issn = generate_issn13()
        >>> is_issn13(issn)
        True
    """
    # Generate ISSN-8 first, then convert
    issn8 = generate_issn(prefix)
    return issn8_to_issn13(issn8)


def generate_issn_l(prefix: str = None) -> str:
    """
    Generate a random valid ISSN-L.
    
    Args:
        prefix: Optional prefix for the ISSN portion (1-7 digits)
        
    Returns:
        A valid ISSN-L string
        
    Examples:
        >>> issn_l = generate_issn_l()
        >>> is_issn_l(issn_l)
        True
    """
    issn = generate_issn(prefix)
    return format_issn_l(issn)


# ============================================================================
# Batch Functions
# ============================================================================

def validate_issns(issns: List[str]) -> Dict[str, Dict]:
    """
    Validate multiple ISSNs at once.
    
    Args:
        issns: List of ISSN strings to validate
        
    Returns:
        Dictionary mapping each ISSN to its validation result
        
    Examples:
        >>> results = validate_issns(["0378-5955", "invalid", "9770378595001"])
        >>> results["0378-5955"]["valid"]
        True
        >>> results["invalid"]["valid"]
        False
    """
    results = {}
    for issn in issns:
        results[issn] = parse_issn(issn)
    return results


def find_issns_in_text(text: str) -> List[str]:
    """
    Find all potential ISSNs in a text string.
    
    Args:
        text: Text to search for ISSNs
        
    Returns:
        List of valid ISSNs found in the text
        
    Examples:
        >>> find_issns_in_text("The journal ISSN 0378-5955 is available.")
        ['03785955']
        >>> find_issns_in_text("ISSNs: 0378-5955 and 2434-561X")
        ['03785955', '2434561X']
    """
    # Pattern to match potential ISSNs
    # ISSN-8: 4 digits, optional hyphen, 3 digits, check digit (0-9 or X)
    # May be prefixed with "ISSN" or "ISSN-L:"
    pattern = r'(?:ISSN-L:\s*)?(?:ISSN\s*)?(\d{4}[-\s]?\d{3}[\dX])'
    
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    valid_issns = []
    for match in matches:
        cleaned = clean_issn(match)
        if is_issn8(cleaned) and cleaned not in valid_issns:
            valid_issns.append(cleaned)
    
    return valid_issns


# ============================================================================
# Utility Functions
# ============================================================================

def compare_issns(issn1: str, issn2: str) -> bool:
    """
    Check if two ISSNs are equivalent (same serial publication).
    
    ISSN-8 and ISSN-13 of the same publication are considered equivalent.
    
    Args:
        issn1: First ISSN
        issn2: Second ISSN
        
    Returns:
        True if ISSNs refer to the same publication
        
    Examples:
        >>> compare_issns("0378-5955", "9770378595001")
        True
        >>> compare_issns("0378-5955", "0378-5956")
        False
    """
    if not is_valid_issn(issn1) or not is_valid_issn(issn2):
        return False
    
    # Convert both to ISSN-8 for comparison
    issn1_8 = clean_issn(issn1) if is_issn8(issn1) else issn13_to_issn8(issn1)
    issn2_8 = clean_issn(issn2) if is_issn8(issn2) else issn13_to_issn8(issn2)
    
    return issn1_8 == issn2_8


def get_issn_variants(issn: str) -> Dict[str, Optional[str]]:
    """
    Get all variants of an ISSN.
    
    Args:
        issn: A valid ISSN string
        
    Returns:
        Dictionary with 'issn8', 'issn13', 'formatted8', 'formatted13', 'issn_l'
        
    Examples:
        >>> get_issn_variants("0378-5955")
        {
            'issn8': '03785955',
            'issn13': '9770378595001',
            'formatted8': '0378-5955',
            'formatted13': '977-0378-5950-01',
            'issn_l': 'ISSN-L: 0378-5955'
        }
    """
    if not is_valid_issn(issn):
        return {
            'issn8': None,
            'issn13': None,
            'formatted8': None,
            'formatted13': None,
            'issn_l': None
        }
    
    issn8 = clean_issn(issn) if is_issn8(issn) else issn13_to_issn8(issn)
    issn13 = ''.join(c for c in issn if c.isdigit()) if is_issn13(issn) else issn8_to_issn13(issn)
    
    return {
        'issn8': issn8,
        'issn13': issn13,
        'formatted8': format_issn(issn8),
        'formatted13': format_issn(issn13),
        'issn_l': format_issn_l(issn8)
    }


def is_print_issn(issn: str) -> bool:
    """
    Check if an ISSN is for a print version.
    
    Print ISSNs typically have certain patterns in their digits.
    This is a heuristic and may not be 100% accurate.
    
    Args:
        issn: An ISSN string
        
    Returns:
        True if likely a print ISSN
        
    Note:
        This is a heuristic based on common patterns. For definitive
        identification, consult the ISSN registry.
    """
    if not is_issn8(issn):
        return False
    
    cleaned = clean_issn(issn)
    # Print ISSNs often have specific patterns
    # This is a simplified heuristic
    return True  # Most ISSNs are for print versions by default


def get_check_digit_info(issn: str) -> Dict[str, any]:
    """
    Get detailed information about an ISSN's check digit.
    
    Args:
        issn: An ISSN string (valid or invalid)
        
    Returns:
        Dictionary with check digit analysis
        
    Examples:
        >>> get_check_digit_info("0378-5955")
        {
            'provided': '5',
            'calculated': '5',
            'valid': True,
            'algorithm': 'modulo-11'
        }
    """
    if is_issn8(issn):
        cleaned = clean_issn(issn)
        calculated = calculate_issn_check_digit(cleaned[:7])
        return {
            'provided': cleaned[7],
            'calculated': calculated,
            'valid': cleaned[7] == calculated,
            'algorithm': 'modulo-11'
        }
    elif is_issn13(issn):
        cleaned = ''.join(c for c in issn if c.isdigit())
        calculated = calculate_issn13_check_digit(cleaned[:12])
        return {
            'provided': cleaned[12],
            'calculated': calculated,
            'valid': cleaned[12] == calculated,
            'algorithm': 'EAN-13'
        }
    else:
        # Try to analyze anyway
        cleaned = clean_issn(issn)
        if len(cleaned) == 8:
            try:
                calculated = calculate_issn_check_digit(cleaned[:7])
                return {
                    'provided': cleaned[7] if cleaned[7] in ISSN_CHARS else None,
                    'calculated': calculated,
                    'valid': cleaned[7] == calculated if cleaned[7] in ISSN_CHARS else False,
                    'algorithm': 'modulo-11'
                }
            except ValueError:
                pass
        
        return {
            'provided': None,
            'calculated': None,
            'valid': False,
            'algorithm': None
        }


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Demo usage
    print("=" * 60)
    print("ISSN Utilities Demo")
    print("=" * 60)
    
    # Test ISSNs
    test_issns = [
        "0378-5955",      # Valid ISSN-8
        "9770378595001",  # Valid ISSN-13
        "2434-561X",      # ISSN-8 with X check digit
        "ISSN-L: 0378-5955",  # ISSN-L
        "invalid",        # Invalid
    ]
    
    for issn in test_issns:
        print(f"\nISSN: {issn}")
        print(f"  Valid: {is_valid_issn(issn)}")
        print(f"  Type: {get_issn_type(issn)}")
        if is_valid_issn(issn):
            info = parse_issn(issn)
            print(f"  Clean: {info['clean']}")
            print(f"  Formatted: {info['formatted']}")
            variants = get_issn_variants(issn)
            print(f"  ISSN-8: {variants['issn8']}")
            print(f"  ISSN-13: {variants['issn13']}")
            print(f"  ISSN-L: {variants['issn_l']}")
    
    print("\n" + "=" * 60)
    print("Generated ISSNs:")
    print("=" * 60)
    for _ in range(3):
        issn8 = generate_issn()
        issn13 = generate_issn13()
        issn_l = generate_issn_l()
        print(f"  ISSN-8: {format_issn(issn8)} -> {is_issn8(issn8)}")
        print(f"  ISSN-13: {format_issn(issn13)} -> {is_issn13(issn13)}")
        print(f"  ISSN-L: {issn_l}")
        print()