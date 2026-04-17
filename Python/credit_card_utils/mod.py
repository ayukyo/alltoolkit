#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Credit Card Utilities Module
==========================================
A comprehensive credit card utility module for Python with zero external dependencies.

Features:
    - Credit card number validation using Luhn algorithm
    - Card type detection (Visa, MasterCard, Amex, Discover, etc.)
    - Card number formatting and masking
    - Test card number generation
    - CVV and expiry date validation
    - BIN/IIN lookup support

Author: AllToolkit Contributors
License: MIT
"""

import re
from typing import Optional, Tuple, Dict, List, Union
from datetime import datetime
from random import randint, choice

# ============================================================================
# Card Type Definitions
# ============================================================================

CARD_PATTERNS: Dict[str, Dict] = {
    'visa': {
        'pattern': r'^4[0-9]{12,18}$',
        'name': 'Visa',
        'lengths': [13, 16, 19],
        'cvv_length': 3,
        'prefixes': ['4']
    },
    'mastercard': {
        'pattern': r'^(?:5[1-5][0-9]{2}|2[2-7][0-9]{2})[0-9]{12}$',
        'name': 'MasterCard',
        'lengths': [16],
        'cvv_length': 3,
        'prefixes': ['51', '52', '53', '54', '55', '2221', '2222', '2223', '2224', '2225',
                    '2226', '2227', '2228', '2229', '223', '224', '225', '226', '227',
                    '228', '229', '23', '24', '25', '26', '270', '271', '2720']
    },
    'amex': {
        'pattern': r'^3[47][0-9]{13}$',
        'name': 'American Express',
        'lengths': [15],
        'cvv_length': 4,
        'prefixes': ['34', '37']
    },
    'discover': {
        'pattern': r'^6(?:011|5[0-9]{2})[0-9]{12}$',
        'name': 'Discover',
        'lengths': [16, 19],
        'cvv_length': 3,
        'prefixes': ['6011', '644', '645', '646', '647', '648', '649', '65']
    },
    'jcb': {
        'pattern': r'^(?:2131|1800|35\d{3})\d{11}$',
        'name': 'JCB',
        'lengths': [16, 19],
        'cvv_length': 3,
        'prefixes': ['2131', '1800', '35']
    },
    'diners_club': {
        'pattern': r'^3(?:0[0-5]|[68][0-9])[0-9]{11,14}$',
        'name': 'Diners Club',
        'lengths': [14, 16, 17, 18, 19],
        'cvv_length': 3,
        'prefixes': ['300', '301', '302', '303', '304', '305', '36', '38', '39']
    },
    'unionpay': {
        'pattern': r'^62[0-9]{14,17}$',
        'name': 'UnionPay',
        'lengths': [16, 17, 18, 19],
        'cvv_length': 3,
        'prefixes': ['62']
    },
    'mir': {
        'pattern': r'^220[0-4][0-9]{12,15}$',
        'name': 'Mir',
        'lengths': [16],
        'cvv_length': 3,
        'prefixes': ['2200', '2201', '2202', '2203', '2204']
    },
    'maestro': {
        'pattern': r'^(?:5[0678]\d\d|6\d\d)[0-9]{10,17}$',
        'name': 'Maestro',
        'lengths': [12, 13, 14, 15, 16, 17, 18, 19],
        'cvv_length': 3,
        'prefixes': ['5018', '5020', '5038', '5893', '6304', '6759', '6761', '6762', '6763']
    }
}

# Test card numbers for development (these are standard test cards)
TEST_CARDS: Dict[str, List[str]] = {
    'visa': ['4111111111111111', '4012888888881881', '4222222222222'],
    'mastercard': ['5555555555554444', '2223000048400011', '5105105105105100'],
    'amex': ['378282246310005', '371449635398431'],
    'discover': ['6011111111111117', '6011000990139424'],
    'jcb': ['3530111333300000', '3566002020360505'],
    'diners_club': ['3056930009020004', '36006666333344'],
    'unionpay': ['6200000000000005', '6216651000000000'],
    'mir': ['2200123456789012'],
    'maestro': ['6759649826438453', '5641820000000005']
}


# ============================================================================
# Validation Functions
# ============================================================================

def luhn_check(card_number: str) -> bool:
    """
    Validate a card number using the Luhn algorithm.
    
    The Luhn algorithm is a simple checksum formula used to validate
    a variety of identification numbers, especially credit card numbers.
    
    Args:
        card_number: The card number to validate (digits only or with spaces/dashes)
    
    Returns:
        True if the card number passes the Luhn check, False otherwise
    
    Example:
        >>> luhn_check('4111111111111111')
        True
        >>> luhn_check('4111111111111112')
        False
    """
    # Remove non-digit characters
    digits = re.sub(r'\D', '', card_number)
    
    if not digits or len(digits) < 2:
        return False
    
    # Luhn algorithm
    total = 0
    reverse_digits = digits[::-1]
    
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        # Double every second digit (starting from the right)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    
    return total % 10 == 0


def calculate_luhn_check_digit(partial_number: str) -> int:
    """
    Calculate the Luhn check digit for a partial card number.
    
    Args:
        partial_number: The card number without check digit
    
    Returns:
        The check digit (0-9)
    
    Example:
        >>> calculate_luhn_check_digit('411111111111111')
        1
    """
    digits = re.sub(r'\D', '', partial_number)
    
    total = 0
    reverse_digits = digits[::-1]
    
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        # Position offset: we're adding a check digit at the end
        if i % 2 == 0:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    
    return (10 - (total % 10)) % 10


def validate_card(card_number: str) -> Dict:
    """
    Comprehensive validation of a credit card number.
    
    Args:
        card_number: The card number to validate
    
    Returns:
        Dictionary with validation results:
        - valid: Overall validity
        - luhn_valid: Luhn check result
        - card_type: Detected card type or None
        - card_name: Human-readable card name
        - length_valid: Whether length is valid for card type
        - formatted: Formatted card number
        - message: Validation message
    
    Example:
        >>> result = validate_card('4111111111111111')
        >>> result['valid']
        True
        >>> result['card_type']
        'visa'
    """
    # Clean the card number
    clean_number = re.sub(r'\D', '', card_number)
    
    result = {
        'valid': False,
        'luhn_valid': False,
        'card_type': None,
        'card_name': None,
        'length_valid': False,
        'formatted': format_card(clean_number),
        'message': ''
    }
    
    # Basic validation
    if not clean_number:
        result['message'] = 'Empty card number'
        return result
    
    if not clean_number.isdigit():
        result['message'] = 'Card number contains non-digit characters'
        return result
    
    if len(clean_number) < 13 or len(clean_number) > 19:
        result['message'] = 'Invalid card number length'
        return result
    
    # Luhn check
    result['luhn_valid'] = luhn_check(clean_number)
    if not result['luhn_valid']:
        result['message'] = 'Failed Luhn checksum'
        return result
    
    # Detect card type
    card_type = detect_card_type(clean_number)
    result['card_type'] = card_type
    
    if card_type:
        card_info = CARD_PATTERNS[card_type]
        result['card_name'] = card_info['name']
        result['length_valid'] = len(clean_number) in card_info['lengths']
        
        if result['length_valid'] and result['luhn_valid']:
            result['valid'] = True
            result['message'] = f'Valid {card_info["name"]} card'
        else:
            result['message'] = f'Invalid length for {card_info["name"]}'
    else:
        # Unknown card type but passes Luhn
        result['length_valid'] = True
        result['valid'] = result['luhn_valid']
        result['message'] = 'Valid card (unknown type)'
    
    return result


def is_valid_card(card_number: str) -> bool:
    """
    Quick check if a card number is valid.
    
    Args:
        card_number: The card number to validate
    
    Returns:
        True if valid, False otherwise
    
    Example:
        >>> is_valid_card('4111111111111111')
        True
    """
    return validate_card(card_number)['valid']


# ============================================================================
# Card Type Detection
# ============================================================================

def detect_card_type(card_number: str) -> Optional[str]:
    """
    Detect the card type from a card number.
    
    Args:
        card_number: The card number (can contain spaces/dashes)
    
    Returns:
        Card type key (e.g., 'visa', 'mastercard') or None if unknown
    
    Example:
        >>> detect_card_type('4111111111111111')
        'visa'
        >>> detect_card_type('5555555555554444')
        'mastercard'
    """
    clean_number = re.sub(r'\D', '', card_number)
    
    for card_type, info in CARD_PATTERNS.items():
        if re.match(info['pattern'], clean_number):
            return card_type
    
    return None


def get_card_info(card_type: str) -> Optional[Dict]:
    """
    Get detailed information about a card type.
    
    Args:
        card_type: The card type key (e.g., 'visa', 'mastercard')
    
    Returns:
        Dictionary with card type information or None if not found
    
    Example:
        >>> get_card_info('visa')
        {'name': 'Visa', 'lengths': [13, 16, 19], 'cvv_length': 3, ...}
    """
    return CARD_PATTERNS.get(card_type)


def get_all_card_types() -> List[str]:
    """
    Get a list of all supported card types.
    
    Returns:
        List of card type keys
    
    Example:
        >>> 'visa' in get_all_card_types()
        True
    """
    return list(CARD_PATTERNS.keys())


# ============================================================================
# Formatting Functions
# ============================================================================

def format_card(card_number: str, separator: str = ' ') -> str:
    """
    Format a card number with separators for readability.
    
    Automatically detects card type and applies appropriate formatting.
    
    Args:
        card_number: The card number to format
        separator: The separator to use (default: space)
    
    Returns:
        Formatted card number
    
    Example:
        >>> format_card('4111111111111111')
        '4111 1111 1111 1111'
        >>> format_card('378282246310005')
        '3782 822463 10005'
    """
    clean_number = re.sub(r'\D', '', card_number)
    
    if not clean_number:
        return ''
    
    # Detect card type for special formatting
    card_type = detect_card_type(clean_number)
    
    if card_type == 'amex':
        # American Express: 4-6-5 format
        if len(clean_number) >= 15:
            return separator.join([
                clean_number[:4],
                clean_number[4:10],
                clean_number[10:15]
            ])
    elif card_type == 'diners_club' and len(clean_number) == 14:
        # Diners Club: 4-6-4 format
        return separator.join([
            clean_number[:4],
            clean_number[4:10],
            clean_number[10:14]
        ])
    
    # Default: groups of 4
    chunks = [clean_number[i:i+4] for i in range(0, len(clean_number), 4)]
    return separator.join(chunks)


def mask_card(card_number: str, show_first: int = 4, show_last: int = 4, 
              mask_char: str = '*') -> str:
    """
    Mask a card number for secure display.
    
    Args:
        card_number: The card number to mask
        show_first: Number of digits to show at start (default: 4)
        show_last: Number of digits to show at end (default: 4)
        mask_char: Character to use for masking (default: '*')
    
    Returns:
        Masked card number
    
    Example:
        >>> mask_card('4111111111111111')
        '4111************1111'
        >>> mask_card('378282246310005', show_first=0, show_last=4)
        '***********0005'
    """
    clean_number = re.sub(r'\D', '', card_number)
    
    if not clean_number:
        return ''
    
    length = len(clean_number)
    
    if show_first + show_last >= length:
        # If we're showing more than we have, just show the number
        return clean_number
    
    first_part = clean_number[:show_first] if show_first > 0 else ''
    last_part = clean_number[-show_last:] if show_last > 0 else ''
    middle_length = length - show_first - show_last
    
    return first_part + (mask_char * middle_length) + last_part


def mask_card_formatted(card_number: str, show_first: int = 4, 
                        show_last: int = 4, mask_char: str = '*', 
                        separator: str = ' ') -> str:
    """
    Mask a card number with formatting.
    
    Combines masking with formatting for a readable but secure display.
    
    Args:
        card_number: The card number to mask and format
        show_first: Number of digits to show at start
        show_last: Number of digits to show at end
        mask_char: Character to use for masking
        separator: Separator character between groups
    
    Returns:
        Masked and formatted card number
    
    Example:
        >>> mask_card_formatted('4111111111111111')
        '4111 **** **** 1111'
    """
    clean_number = re.sub(r'\D', '', card_number)
    
    if not clean_number:
        return ''
    
    length = len(clean_number)
    
    # Build the masked number with formatting in mind
    # For standard 16-digit cards with show_first=4, show_last=4:
    # Result should be like '4111 **** **** 1111'
    
    # Detect card type for special formatting
    card_type = detect_card_type(clean_number)
    
    if card_type == 'amex' and length == 15:
        # Amex format: 4-6-5
        first = clean_number[:show_first] if show_first > 0 else ''
        last = clean_number[-show_last:] if show_last > 0 else ''
        middle_count = length - show_first - show_last
        
        # For Amex, the middle part spans positions 4-10 (6 digits)
        # Mask those positions
        if show_first >= 4:
            middle_mask = mask_char * 6
            return first + separator + middle_mask + separator + last
        else:
            return mask_card(clean_number, show_first, show_last, mask_char)
    
    # For standard cards (16 digits), format as groups of 4
    # Show first 4 digits, mask middle 8, show last 4
    if length == 16 and show_first == 4 and show_last == 4:
        first_part = clean_number[:4]
        middle_mask = mask_char * 4
        last_part = clean_number[-4:]
        return first_part + separator + middle_mask + separator + middle_mask + separator + last_part
    
    # General case: mask and format with groups of 4
    first_part = clean_number[:show_first] if show_first > 0 else ''
    last_part = clean_number[-show_last:] if show_last > 0 else ''
    middle_count = length - show_first - show_last
    
    # Build the full masked string
    masked_full = first_part + (mask_char * middle_count) + last_part
    
    # Now format it in groups of 4, preserving mask characters
    chunks = []
    for i in range(0, len(masked_full), 4):
        chunks.append(masked_full[i:i+4])
    
    return separator.join(chunks)


# ============================================================================
# CVV and Expiry Validation
# ============================================================================

def is_valid_cvv(cvv: str, card_type: Optional[str] = None) -> bool:
    """
    Validate a CVV/CVC code.
    
    Args:
        cvv: The CVV to validate
        card_type: Optional card type for specific length validation
    
    Returns:
        True if valid, False otherwise
    
    Example:
        >>> is_valid_cvv('123')
        True
        >>> is_valid_cvv('1234', 'amex')
        True
    """
    if not cvv or not cvv.isdigit():
        return False
    
    # Get expected CVV length for card type
    expected_length = None
    if card_type and card_type in CARD_PATTERNS:
        expected_length = CARD_PATTERNS[card_type]['cvv_length']
    
    if expected_length:
        return len(cvv) == expected_length
    
    # Default: 3 or 4 digits
    return len(cvv) in [3, 4]


def is_valid_expiry(month: int, year: int) -> bool:
    """
    Check if an expiry date is valid and not expired.
    
    Args:
        month: Expiry month (1-12)
        year: Expiry year (4-digit or 2-digit)
    
    Returns:
        True if valid and not expired, False otherwise
    
    Example:
        >>> is_valid_expiry(12, datetime.now().year + 1)
        True
        >>> is_valid_expiry(1, 2020)  # Past date
        False
    """
    # Convert 2-digit year to 4-digit
    if year < 100:
        current_year = datetime.now().year
        century = (current_year // 100) * 100
        year = century + year
        # Handle Y2K-style rollover
        if year < current_year - 10:
            year += 100
    
    # Validate month
    if month < 1 or month > 12:
        return False
    
    # Check if expired
    now = datetime.now()
    expiry_date = datetime(year, month, 1)
    
    # Card is valid until the end of the expiry month
    # So if current month/year <= expiry month/year, it's valid
    return (year > now.year) or (year == now.year and month >= now.month)


def validate_expiry(month: Union[str, int], year: Union[str, int]) -> Dict:
    """
    Comprehensive expiry date validation.
    
    Args:
        month: Expiry month (string or int)
        year: Expiry year (string or int, 2 or 4 digits)
    
    Returns:
        Dictionary with validation results
    
    Example:
        >>> result = validate_expiry('12', '25')
        >>> result['valid']
        True
    """
    try:
        month = int(str(month).strip())
        year = int(str(year).strip())
    except ValueError:
        return {
            'valid': False,
            'month': None,
            'year': None,
            'expired': False,
            'message': 'Invalid month or year format'
        }
    
    # Convert 2-digit year
    if year < 100:
        current_year = datetime.now().year
        century = (current_year // 100) * 100
        year = century + year
        if year < current_year - 10:
            year += 100
    
    if month < 1 or month > 12:
        return {
            'valid': False,
            'month': month,
            'year': year,
            'expired': False,
            'message': 'Month must be between 1 and 12'
        }
    
    now = datetime.now()
    is_expired = (year < now.year) or (year == now.year and month < now.month)
    
    return {
        'valid': not is_expired,
        'month': month,
        'year': year,
        'expired': is_expired,
        'message': 'Card expired' if is_expired else 'Valid expiry date'
    }


# ============================================================================
# Card Number Generation (for testing)
# ============================================================================

def generate_test_card(card_type: str = 'visa') -> str:
    """
    Generate a valid test card number for a specific card type.
    
    Note: These are standard test card numbers used in development.
    They will NOT work for real transactions.
    
    Args:
        card_type: The type of card to generate (default: 'visa')
    
    Returns:
        A test card number
    
    Example:
        >>> card = generate_test_card('visa')
        >>> is_valid_card(card)
        True
    """
    card_type = card_type.lower()
    
    if card_type in TEST_CARDS:
        return choice(TEST_CARDS[card_type])
    
    # Fallback to Visa
    return choice(TEST_CARDS['visa'])


def generate_random_card(card_type: str = 'visa', length: Optional[int] = None) -> str:
    """
    Generate a random valid card number for testing.
    
    Uses proper prefix for card type and valid Luhn checksum.
    WARNING: For testing only! These are NOT real card numbers.
    
    Args:
        card_type: The type of card to generate (default: 'visa')
        length: Desired length (uses card type default if not specified)
    
    Returns:
        A valid-looking card number (for testing only!)
    
    Example:
        >>> card = generate_random_card('mastercard')
        >>> is_valid_card(card)
        True
    """
    card_type = card_type.lower()
    
    if card_type not in CARD_PATTERNS:
        card_type = 'visa'
    
    info = CARD_PATTERNS[card_type]
    
    # Choose length
    if length is None:
        length = choice(info['lengths'])
    elif length not in info['lengths']:
        length = info['lengths'][0]
    
    # Choose a prefix
    prefix = choice(info['prefixes'])
    
    # Generate random digits for remaining length (minus 1 for check digit)
    remaining = length - len(prefix) - 1
    random_digits = ''.join(str(randint(0, 9)) for _ in range(remaining))
    
    # Combine prefix and random digits
    partial = prefix + random_digits
    
    # Calculate check digit
    check_digit = calculate_luhn_check_digit(partial)
    
    return partial + str(check_digit)


# ============================================================================
# BIN/IIN Utilities
# ============================================================================

def get_bin(card_number: str, length: int = 6) -> str:
    """
    Extract the BIN (Bank Identification Number) from a card number.
    
    The BIN (also called IIN) identifies the issuer of the card.
    
    Args:
        card_number: The card number
        length: Length of BIN to extract (default: 6)
    
    Returns:
        The BIN digits
    
    Example:
        >>> get_bin('4111111111111111')
        '411111'
        >>> get_bin('4111111111111111', length=8)
        '41111111'
    """
    clean_number = re.sub(r'\D', '', card_number)
    return clean_number[:length]


def is_issuer(card_number: str, issuer: str) -> bool:
    """
    Check if a card number belongs to a specific issuer.
    
    Args:
        card_number: The card number to check
        issuer: The issuer to check for (case-insensitive)
    
    Returns:
        True if the card belongs to the issuer
    
    Example:
        >>> is_issuer('4111111111111111', 'visa')
        True
        >>> is_issuer('4111111111111111', 'mastercard')
        False
    """
    return detect_card_type(card_number) == issuer.lower()


# ============================================================================
# Utility Functions
# ============================================================================

def clean_card_number(card_number: str) -> str:
    """
    Remove all non-digit characters from a card number.
    
    Args:
        card_number: The card number (may contain spaces, dashes, etc.)
    
    Returns:
        Clean card number with only digits
    
    Example:
        >>> clean_card_number('4111-1111-1111-1111')
        '4111111111111111'
    """
    return re.sub(r'\D', '', card_number)


def get_card_length_range() -> Tuple[int, int]:
    """
    Get the valid length range for card numbers.
    
    Returns:
        Tuple of (min_length, max_length)
    
    Example:
        >>> get_card_length_range()
        (13, 19)
    """
    min_len = min(min(info['lengths']) for info in CARD_PATTERNS.values())
    max_len = max(max(info['lengths']) for info in CARD_PATTERNS.values())
    return (min_len, max_len)


def summarize_card(card_number: str) -> Dict:
    """
    Get a comprehensive summary of a card number.
    
    Args:
        card_number: The card number to analyze
    
    Returns:
        Dictionary with all card information
    
    Example:
        >>> summary = summarize_card('4111111111111111')
        >>> summary['type']
        'visa'
        >>> summary['valid']
        True
    """
    clean_number = clean_card_number(card_number)
    validation = validate_card(clean_number)
    
    return {
        'number': mask_card(clean_number),
        'formatted': format_card(clean_number),
        'bin': get_bin(clean_number),
        'type': validation['card_type'],
        'name': validation['card_name'],
        'valid': validation['valid'],
        'luhn_valid': validation['luhn_valid'],
        'length': len(clean_number),
        'length_valid': validation['length_valid'],
        'message': validation['message']
    }


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == '__main__':
    # Demo usage
    print("Credit Card Utilities Demo")
    print("=" * 50)
    
    # Test cards
    test_cards = [
        '4111111111111111',  # Visa
        '5555555555554444',  # MasterCard
        '378282246310005',   # Amex
        '6011111111111117',  # Discover
    ]
    
    for card in test_cards:
        summary = summarize_card(card)
        print(f"\nCard: {format_card(card)}")
        print(f"  Type: {summary['name'] or 'Unknown'}")
        print(f"  Valid: {summary['valid']}")
        print(f"  Masked: {mask_card_formatted(card)}")
    
    # Generate test cards
    print("\n" + "=" * 50)
    print("Generated Test Cards:")
    for card_type in ['visa', 'mastercard', 'amex']:
        card = generate_random_card(card_type)
        print(f"  {card_type}: {format_card(card)}")