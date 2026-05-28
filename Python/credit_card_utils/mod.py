#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Credit Card Utilities Module
==========================================
A comprehensive credit card processing utility module for Python with zero external dependencies.

Features:
    - Luhn algorithm validation
    - Credit card type detection (Visa, Mastercard, Amex, etc.)
    - Card number formatting and masking
    - CVV validation
    - Expiry date validation
    - Card number generation for testing (valid Luhn)
    - IIN/BIN range lookup

Author: AllToolkit Contributors
License: MIT
"""

import re
from typing import Optional, Tuple, List, Dict
from dataclasses import dataclass
from datetime import datetime, date
from random import randint


# ============================================================================
# Constants
# ============================================================================

# Card type patterns (IIN ranges)
CARD_PATTERNS = {
    'visa': {
        'patterns': [r'^4'],
        'lengths': [13, 16, 19],
        'cvv_length': 3,
        'name': 'Visa',
    },
    'mastercard': {
        'patterns': [r'^5[1-5]', r'^2[2-7][1-9]'],
        'lengths': [16],
        'cvv_length': 3,
        'name': 'Mastercard',
    },
    'amex': {
        'patterns': [r'^3[47]'],
        'lengths': [15],
        'cvv_length': 4,
        'name': 'American Express',
    },
    'discover': {
        'patterns': [r'^6011', r'^65', r'^64[4-9]', r'^622(?:12[6-9]|1[3-9][0-9]|[2-8][0-9]{2}|9[0-1][0-9]|92[0-5])'],
        'lengths': [16, 19],
        'cvv_length': 3,
        'name': 'Discover',
    },
    'diners_club': {
        'patterns': [r'^3(?:0[0-5]|[68][0-9])'],
        'lengths': [14, 16, 19],
        'cvv_length': 3,
        'name': 'Diners Club',
    },
    'jcb': {
        'patterns': [r'^(?:2131|1800|35(?:2[8-9]|[3-8][0-9]))'],
        'lengths': [16, 17, 18, 19],
        'cvv_length': 3,
        'name': 'JCB',
    },
    'unionpay': {
        'patterns': [r'^62', r'^81'],
        'lengths': [16, 17, 18, 19],
        'cvv_length': 3,
        'name': 'UnionPay',
    },
    'maestro': {
        'patterns': [r'^(?:5018|5020|5038|56[0-9]{2}|67[0-9]{2})'],
        'lengths': [12, 13, 14, 15, 16, 17, 18, 19],
        'cvv_length': 3,
        'name': 'Maestro',
    },
    'mir': {
        'patterns': [r'^220[0-4]'],
        'lengths': [16],
        'cvv_length': 3,
        'name': 'Mir',
    },
}

# Card type display names
CARD_TYPE_NAMES = {
    'visa': 'Visa',
    'mastercard': 'Mastercard',
    'amex': 'American Express',
    'discover': 'Discover',
    'diners_club': 'Diners Club',
    'jcb': 'JCB',
    'unionpay': 'UnionPay',
    'maestro': 'Maestro',
    'mir': 'Mir',
    'unknown': 'Unknown',
}


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class CardInfo:
    """Credit card information."""
    card_type: str
    card_type_name: str
    is_valid: bool
    is_valid_luhn: bool
    formatted_number: str
    masked_number: str
    cvv_length: int
    expected_lengths: List[int]
    is_length_valid: bool


@dataclass
class ExpiryCheck:
    """Expiry date validation result."""
    is_valid: bool
    is_expired: bool
    is_future: bool
    days_until_expiry: Optional[int]
    formatted: str
    error: Optional[str] = None


# ============================================================================
# Luhn Algorithm
# ============================================================================

def luhn_checksum(card_number: str) -> int:
    """
    Calculate the Luhn checksum digit for a partial card number.
    
    This computes what the check digit should be for the given
    partial card number (without the check digit).
    
    Args:
        card_number: The card number string without check digit (digits only)
    
    Returns:
        The Luhn check digit (0-9)
    
    Example:
        >>> luhn_checksum('45320151128303')
        6
    """
    digits = [int(d) for d in card_number]
    total = 0
    
    # Process from right to left, doubling every second digit
    # Since we're computing checksum for the number without check digit,
    # we double digits at even positions from the right
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 0:  # Double digits at positions 0, 2, 4... from right
            doubled = d * 2
            total += doubled if doubled < 10 else doubled - 9
        else:
            total += d
    
    return (10 - (total % 10)) % 10


def validate_luhn(card_number: str) -> bool:
    """
    Validate a card number using the Luhn algorithm.
    
    Args:
        card_number: The card number string (can include spaces/dashes)
    
    Returns:
        True if the card number passes Luhn validation
    
    Example:
        >>> validate_luhn('4532015112830366')
        True
        >>> validate_luhn('4532015112830367')
        False
    """
    # Clean the card number
    clean_number = re.sub(r'[^0-9]', '', card_number)
    
    if not clean_number or len(clean_number) < 2:
        return False
    
    # Standard Luhn algorithm: sum all digits, doubling every second digit from right
    digits = [int(d) for d in clean_number]
    total = 0
    
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:  # Double every second digit from the right
            doubled = d * 2
            total += doubled if doubled < 10 else doubled - 9
        else:
            total += d
    
    return total % 10 == 0


# ============================================================================
# Card Type Detection
# ============================================================================

def detect_card_type(card_number: str) -> Tuple[str, dict]:
    """
    Detect the credit card type from the card number.
    
    Args:
        card_number: The card number string (can include spaces/dashes)
    
    Returns:
        Tuple of (card_type_key, card_info_dict)
        Returns ('unknown', {}) if type cannot be determined
    
    Example:
        >>> detect_card_type('4532015112830366')
        ('visa', {'patterns': [...], 'lengths': [13, 16, 19], ...})
    """
    clean_number = re.sub(r'[^0-9]', '', card_number)
    
    if not clean_number:
        return ('unknown', {})
    
    for card_type, info in CARD_PATTERNS.items():
        for pattern in info['patterns']:
            if re.match(pattern, clean_number):
                return (card_type, info)
    
    return ('unknown', {})


def get_card_type_name(card_number: str) -> str:
    """
    Get the display name for a card number's type.
    
    Args:
        card_number: The card number string
    
    Returns:
        The card type display name (e.g., 'Visa', 'Mastercard')
    
    Example:
        >>> get_card_type_name('4532015112830366')
        'Visa'
    """
    card_type, _ = detect_card_type(card_number)
    return CARD_TYPE_NAMES.get(card_type, 'Unknown')


# ============================================================================
# Card Number Operations
# ============================================================================

def clean_card_number(card_number: str) -> str:
    """
    Remove all non-digit characters from a card number.
    
    Args:
        card_number: The card number string
    
    Returns:
        Clean card number with only digits
    
    Example:
        >>> clean_card_number('4532-0151-1283-0366')
        '4532015112830366'
    """
    return re.sub(r'[^0-9]', '', card_number)


def format_card_number(card_number: str, card_type: Optional[str] = None) -> str:
    """
    Format a card number with appropriate spacing.
    
    Args:
        card_number: The card number string
        card_type: Optional card type hint (auto-detected if not provided)
    
    Returns:
        Formatted card number string
    
    Example:
        >>> format_card_number('4532015112830366')
        '4532 0151 1283 0366'
        >>> format_card_number('378282246310005')  # Amex
        '3782 822463 10005'
    """
    clean_number = clean_card_number(card_number)
    
    if not card_type:
        card_type, _ = detect_card_type(clean_number)
    
    # American Express: 4-6-5 format
    if card_type == 'amex' and len(clean_number) == 15:
        return f"{clean_number[:4]} {clean_number[4:10]} {clean_number[10:]}"
    
    # Diners Club (14 digits): 4-6-4 format
    if card_type == 'diners_club' and len(clean_number) == 14:
        return f"{clean_number[:4]} {clean_number[4:10]} {clean_number[10:]}"
    
    # Default: 4-digit groups
    groups = [clean_number[i:i+4] for i in range(0, len(clean_number), 4)]
    return ' '.join(groups)


def mask_card_number(card_number: str, mask_char: str = '*', visible_start: int = 4, 
                      visible_end: int = 4) -> str:
    """
    Mask a card number, showing only the first and last few digits.
    
    Args:
        card_number: The card number string
        mask_char: Character to use for masking (default '*')
        visible_start: Number of digits to show at start (default 4)
        visible_end: Number of digits to show at end (default 4)
    
    Returns:
        Masked card number string
    
    Example:
        >>> mask_card_number('4532015112830366')
        '4532********0366'
    """
    clean_number = clean_card_number(card_number)
    
    if len(clean_number) <= visible_start + visible_end:
        return clean_number
    
    masked_length = len(clean_number) - visible_start - visible_end
    masked = mask_char * masked_length
    
    return clean_number[:visible_start] + masked + clean_number[-visible_end:]


def validate_card_length(card_number: str) -> Tuple[bool, List[int]]:
    """
    Validate if the card number has a valid length for its type.
    
    Args:
        card_number: The card number string
    
    Returns:
        Tuple of (is_valid, expected_lengths)
    
    Example:
        >>> validate_card_length('4532015112830366')
        (True, [13, 16, 19])
    """
    clean_number = clean_card_number(card_number)
    card_type, info = detect_card_type(clean_number)
    
    if card_type == 'unknown':
        # Unknown types: accept 13-19 digits
        return (13 <= len(clean_number) <= 19, list(range(13, 20)))
    
    expected_lengths = info.get('lengths', [16])
    is_valid = len(clean_number) in expected_lengths
    
    return (is_valid, expected_lengths)


# ============================================================================
# CVV Validation
# ============================================================================

def validate_cvv(cvv: str, card_type: Optional[str] = None) -> bool:
    """
    Validate a CVV/CVC code.
    
    Args:
        cvv: The CVV string
        card_type: Optional card type to check expected length
    
    Returns:
        True if the CVV appears valid
    
    Example:
        >>> validate_cvv('123')
        True
        >>> validate_cvv('1234', 'amex')
        True
    """
    clean_cvv = re.sub(r'[^0-9]', '', cvv)
    
    if not clean_cvv:
        return False
    
    # Check if all digits
    if not clean_cvv.isdigit():
        return False
    
    # Without card type, accept 3 or 4 digits
    if not card_type:
        return len(clean_cvv) in [3, 4]
    
    # Check against expected length for card type
    if card_type in CARD_PATTERNS:
        expected_length = CARD_PATTERNS[card_type]['cvv_length']
        return len(clean_cvv) == expected_length
    
    return len(clean_cvv) in [3, 4]


# ============================================================================
# Expiry Date Validation
# ============================================================================

def validate_expiry(month: int, year: int) -> ExpiryCheck:
    """
    Validate a credit card expiry date.
    
    Args:
        month: Expiry month (1-12)
        year: Expiry year (2-digit or 4-digit)
    
    Returns:
        ExpiryCheck dataclass with validation results
    
    Example:
        >>> result = validate_expiry(12, 2025)
        >>> result.is_valid
        True
    """
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    
    # Normalize year
    if year < 100:
        year += 2000 if year < 50 else 1900
    
    errors = []
    
    # Validate month
    if month < 1 or month > 12:
        errors.append("Invalid month (must be 1-12)")
    
    # Check if expired
    is_expired = False
    if year < current_year or (year == current_year and month < current_month):
        is_expired = True
    
    # Check if too far in future (more than 20 years)
    is_future = year > current_year + 20
    
    # Calculate days until expiry
    days_until_expiry = None
    if not is_expired and month >= 1 and month <= 12:
        try:
            # Last day of expiry month
            if month == 12:
                expiry_date = date(year + 1, 1, 1)
            else:
                expiry_date = date(year, month + 1, 1)
            days_until_expiry = (expiry_date - date.today()).days
        except ValueError:
            pass
    
    formatted = f"{month:02d}/{str(year)[-2:]}"
    
    is_valid = len(errors) == 0 and not is_expired and not is_future
    
    return ExpiryCheck(
        is_valid=is_valid,
        is_expired=is_expired,
        is_future=is_future,
        days_until_expiry=days_until_expiry,
        formatted=formatted,
        error='; '.join(errors) if errors else None
    )


def parse_expiry_string(expiry_str: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Parse an expiry date string (MM/YY or MM/YYYY format).
    
    Args:
        expiry_str: Expiry date string
    
    Returns:
        Tuple of (month, year) or (None, None) if parsing fails
    
    Example:
        >>> parse_expiry_string('12/25')
        (12, 2025)
    """
    # Clean the string
    expiry_str = expiry_str.strip().replace(' ', '')
    
    # Try different formats
    patterns = [
        (r'^(\d{1,2})/(\d{2})$', 2),   # MM/YY
        (r'^(\d{1,2})/(\d{4})$', 4),   # MM/YYYY
        (r'^(\d{2})(\d{2})$', 2),      # MMYY
        (r'^(\d{2})(\d{4})$', 4),      # MMYYYY
    ]
    
    for pattern, year_digits in patterns:
        match = re.match(pattern, expiry_str)
        if match:
            month = int(match.group(1))
            year = int(match.group(2))
            if year_digits == 2:
                year += 2000 if year < 50 else 1900
            return (month, year)
    
    return (None, None)


# ============================================================================
# Comprehensive Validation
# ============================================================================

def get_card_info(card_number: str) -> CardInfo:
    """
    Get comprehensive information about a card number.
    
    Args:
        card_number: The card number string
    
    Returns:
        CardInfo dataclass with all validation results
    
    Example:
        >>> info = get_card_info('4532015112830366')
        >>> info.card_type
        'visa'
        >>> info.is_valid
        True
    """
    clean_number = clean_card_number(card_number)
    card_type, card_info = detect_card_type(clean_number)
    
    is_valid_luhn = validate_luhn(clean_number)
    is_length_valid, expected_lengths = validate_card_length(clean_number)
    
    cvv_length = card_info.get('cvv_length', 3) if card_info else 3
    
    formatted = format_card_number(clean_number, card_type)
    masked = mask_card_number(clean_number)
    
    is_valid = is_valid_luhn and is_length_valid
    
    return CardInfo(
        card_type=card_type,
        card_type_name=CARD_TYPE_NAMES.get(card_type, 'Unknown'),
        is_valid=is_valid,
        is_valid_luhn=is_valid_luhn,
        formatted_number=formatted,
        masked_number=masked,
        cvv_length=cvv_length,
        expected_lengths=expected_lengths,
        is_length_valid=is_length_valid
    )


def validate_card(card_number: str, cvv: Optional[str] = None, 
                   expiry_month: Optional[int] = None, 
                   expiry_year: Optional[int] = None) -> Tuple[bool, List[str]]:
    """
    Comprehensive card validation.
    
    Args:
        card_number: The card number string
        cvv: Optional CVV to validate
        expiry_month: Optional expiry month
        expiry_year: Optional expiry year
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    
    Example:
        >>> validate_card('4532015112830366')
        (True, [])
        >>> validate_card('1234567890123456')
        (False, ['Invalid Luhn checksum'])
    """
    errors = []
    clean_number = clean_card_number(card_number)
    
    # Check card number
    if not clean_number:
        errors.append("Empty card number")
        return (False, errors)
    
    if not clean_number.isdigit():
        errors.append("Card number contains non-digit characters")
        return (False, errors)
    
    card_type, card_info = detect_card_type(clean_number)
    
    # Validate Luhn
    if not validate_luhn(clean_number):
        errors.append("Invalid Luhn checksum")
    
    # Validate length
    is_length_valid, expected_lengths = validate_card_length(clean_number)
    if not is_length_valid:
        errors.append(f"Invalid length. Expected: {expected_lengths}, got: {len(clean_number)}")
    
    # Validate CVV if provided
    if cvv:
        if not validate_cvv(cvv, card_type):
            expected_cvv_length = card_info.get('cvv_length', 3) if card_info else 3
            errors.append(f"Invalid CVV. Expected {expected_cvv_length} digits for {card_type}")
    
    # Validate expiry if provided
    if expiry_month and expiry_year:
        expiry_check = validate_expiry(expiry_month, expiry_year)
        if expiry_check.is_expired:
            errors.append("Card is expired")
        if expiry_check.is_future:
            errors.append("Expiry date is too far in the future")
        if expiry_check.error:
            errors.append(expiry_check.error)
    
    return (len(errors) == 0, errors)


# ============================================================================
# Test Card Generation
# ============================================================================

def generate_test_card(card_type: str = 'visa', length: Optional[int] = None) -> str:
    """
    Generate a valid test card number for the specified type.
    Note: These are for testing purposes only and are not real card numbers.
    
    Args:
        card_type: The card type to generate (visa, mastercard, amex, etc.)
        length: Desired length (must be valid for the card type)
    
    Returns:
        A valid Luhn test card number
    
    Example:
        >>> card = generate_test_card('visa')
        >>> validate_luhn(card)
        True
    """
    card_type = card_type.lower()
    
    if card_type not in CARD_PATTERNS:
        raise ValueError(f"Unknown card type: {card_type}")
    
    info = CARD_PATTERNS[card_type]
    valid_lengths = info['lengths']
    
    if length and length not in valid_lengths:
        raise ValueError(f"Invalid length {length} for {card_type}. Valid lengths: {valid_lengths}")
    
    target_length = length or valid_lengths[0]
    
    # Get the IIN prefix pattern
    pattern = info['patterns'][0]
    
    # Generate prefix based on pattern
    if card_type == 'visa':
        prefix = '4'
    elif card_type == 'mastercard':
        prefix = '5' + str(randint(1, 5))
    elif card_type == 'amex':
        prefix = '3' + ('4' if randint(0, 1) else '7')
    elif card_type == 'discover':
        prefix = '6011'
    elif card_type == 'diners_club':
        prefix = '300'
    elif card_type == 'jcb':
        prefix = '35'
    elif card_type == 'unionpay':
        prefix = '62'
    elif card_type == 'maestro':
        prefix = '5018'
    elif card_type == 'mir':
        prefix = '220' + str(randint(0, 4))
    else:
        prefix = '4'  # Default to Visa-like
    
    # Generate random digits to fill the rest (except check digit)
    remaining_length = target_length - len(prefix) - 1
    random_digits = ''.join(str(randint(0, 9)) for _ in range(remaining_length))
    
    # Combine prefix and random digits
    card_without_check = prefix + random_digits
    
    # Calculate and append check digit
    check_digit = luhn_checksum(card_without_check)
    
    return card_without_check + str(check_digit)


def generate_test_cards(count: int = 5, card_type: Optional[str] = None) -> List[str]:
    """
    Generate multiple test card numbers.
    
    Args:
        count: Number of cards to generate
        card_type: Optional specific card type
    
    Returns:
        List of valid Luhn test card numbers
    
    Example:
        >>> cards = generate_test_cards(3)
        >>> all(validate_luhn(c) for c in cards)
        True
    """
    if card_type:
        return [generate_test_card(card_type) for _ in range(count)]
    
    # Generate variety of card types
    card_types = list(CARD_PATTERNS.keys())
    cards = []
    for i in range(count):
        ct = card_types[i % len(card_types)]
        cards.append(generate_test_card(ct))
    
    return cards


# ============================================================================
# BIN/IIN Lookup
# ============================================================================

def get_iin_info(iin: str) -> Dict:
    """
    Get information about an Issuer Identification Number (IIN/BIN).
    The IIN is the first 6-8 digits of a card number.
    
    Args:
        iin: The IIN (6-8 digits)
    
    Returns:
        Dictionary with IIN information
    
    Example:
        >>> info = get_iin_info('453201')
        >>> info['card_type']
        'visa'
    """
    clean_iin = re.sub(r'[^0-9]', '', str(iin))[:8]
    
    if len(clean_iin) < 6:
        return {'error': 'IIN must be at least 6 digits'}
    
    card_type, info = detect_card_type(clean_iin)
    
    return {
        'iin': clean_iin,
        'card_type': card_type,
        'card_type_name': CARD_TYPE_NAMES.get(card_type, 'Unknown'),
        'expected_lengths': info.get('lengths', []) if info else [],
        'cvv_length': info.get('cvv_length', 3) if info else 3,
    }


# ============================================================================
# Card Number Comparison and Utilities
# ============================================================================

def compare_cards(card1: str, card2: str) -> int:
    """
    Compare two card numbers numerically.
    
    Args:
        card1: First card number
        card2: Second card number
    
    Returns:
        -1 if card1 < card2, 0 if equal, 1 if card1 > card2
    
    Example:
        >>> compare_cards('4000000000000001', '4000000000000002')
        -1
    """
    num1 = int(clean_card_number(card1) or '0')
    num2 = int(clean_card_number(card2) or '0')
    
    if num1 < num2:
        return -1
    elif num1 > num2:
        return 1
    return 0


def card_to_int(card_number: str) -> int:
    """
    Convert a card number to an integer for numeric operations.
    
    Args:
        card_number: The card number string
    
    Returns:
        Integer representation of the card number
    
    Example:
        >>> card_to_int('4532015112830366')
        4532015112830366
    """
    clean = clean_card_number(card_number)
    return int(clean) if clean else 0


def int_to_card(num: int) -> str:
    """
    Convert an integer to a card number string.
    
    Args:
        num: Integer card number
    
    Returns:
        Card number string
    
    Example:
        >>> int_to_card(4532015112830366)
        '4532015112830366'
    """
    return str(num)


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    # Demo
    print("Credit Card Utilities Demo")
    print("=" * 50)
    
    # Test known card numbers
    test_cards = [
        ('4532015112830366', 'Visa'),
        ('5425233430109903', 'Mastercard'),
        ('374245455400126', 'Amex'),
        ('6011000990139424', 'Discover'),
    ]
    
    print("\nCard Validation Tests:")
    for card, expected_type in test_cards:
        info = get_card_info(card)
        status = "✓" if info.is_valid else "✗"
        print(f"  {status} {card} -> {info.card_type_name} (Luhn: {info.is_valid_luhn})")
    
    print("\nGenerated Test Cards:")
    for card in generate_test_cards(5):
        info = get_card_info(card)
        print(f"  {info.formatted_number} -> {info.card_type_name}")
    
    print("\nCard Masking:")
    print(f"  {mask_card_number('4532015112830366')}")
    print(f"  {mask_card_number('378282246310005')}")