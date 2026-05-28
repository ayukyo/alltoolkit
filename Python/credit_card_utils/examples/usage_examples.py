#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Credit Card Utilities Examples
=============================================
Usage examples for the credit_card_utils module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    validate_luhn,
    detect_card_type,
    get_card_type_name,
    clean_card_number,
    format_card_number,
    mask_card_number,
    validate_cvv,
    validate_expiry,
    parse_expiry_string,
    get_card_info,
    validate_card,
    generate_test_card,
    generate_test_cards,
    get_iin_info,
)


def example_luhn_validation():
    """Example: Luhn algorithm validation."""
    print("\n" + "=" * 60)
    print("Luhn Algorithm Validation")
    print("=" * 60)
    
    cards = [
        '4111111111111111',  # Valid Visa (test card)
        '4111111111111112',  # Invalid (wrong check digit)
        '5555555555554444',  # Valid Mastercard (test card)
        '378282246310005',   # Valid Amex (test card)
    ]
    
    for card in cards:
        is_valid = validate_luhn(card)
        status = "✓ Valid" if is_valid else "✗ Invalid"
        print(f"  {card}: {status}")


def example_card_type_detection():
    """Example: Detecting card types."""
    print("\n" + "=" * 60)
    print("Card Type Detection")
    print("=" * 60)
    
    cards = [
        '4111111111111111',  # Visa
        '5555555555554444',  # Mastercard
        '378282246310005',   # American Express
        '6011111111111117',  # Discover
        '3566002020360505',  # JCB
        '6221261234567890',  # UnionPay
        '5018000000000000',  # Maestro
        '2200123456789012',  # Mir
    ]
    
    for card in cards:
        card_type, info = detect_card_type(card)
        name = info.get('name', 'Unknown') if info else 'Unknown'
        lengths = info.get('lengths', []) if info else []
        cvv_len = info.get('cvv_length', 0) if info else 0
        
        print(f"  {card}")
        print(f"    Type: {name}")
        print(f"    Valid lengths: {lengths}")
        print(f"    CVV length: {cvv_len}")


def example_formatting():
    """Example: Card number formatting and masking."""
    print("\n" + "=" * 60)
    print("Formatting and Masking")
    print("=" * 60)
    
    cards = [
        ('4111111111111111', 'Visa'),
        ('5555555555554444', 'Mastercard'),
        ('378282246310005', 'Amex'),
    ]
    
    for card, expected_type in cards:
        clean = clean_card_number(card)
        formatted = format_card_number(card)
        masked = mask_card_number(card)
        masked_custom = mask_card_number(card, mask_char='#', visible_start=2, visible_end=2)
        
        print(f"\n  Original: {card} ({expected_type})")
        print(f"  Cleaned:  {clean}")
        print(f"  Formatted: {formatted}")
        print(f"  Masked:   {masked}")
        print(f"  Custom:   {masked_custom}")


def example_expiry_validation():
    """Example: Expiry date validation."""
    print("\n" + "=" * 60)
    print("Expiry Date Validation")
    print("=" * 60)
    
    test_dates = [
        (12, 2025),  # Valid future date
        (6, 2026),   # Valid future date
        (1, 2020),   # Expired
        (13, 2025),  # Invalid month
        (6, 2050),   # Too far in future
    ]
    
    now_year = 2024  # For display purposes
    for month, year in test_dates:
        result = validate_expiry(month, year)
        print(f"\n  {month:02d}/{str(year)[-2:]}")
        print(f"    Valid: {result.is_valid}")
        print(f"    Expired: {result.is_expired}")
        if result.days_until_expiry is not None:
            print(f"    Days until expiry: {result.days_until_expiry}")
        if result.error:
            print(f"    Error: {result.error}")
    
    # Parse expiry strings
    print("\n  Parsing expiry strings:")
    strings = ['12/25', '06/2026', '1225', '062026']
    for s in strings:
        month, year = parse_expiry_string(s)
        if month and year:
            print(f"    '{s}' -> {month:02d}/{year}")


def example_cvv_validation():
    """Example: CVV validation."""
    print("\n" + "=" * 60)
    print("CVV Validation")
    print("=" * 60)
    
    test_cvvs = [
        ('123', None),        # Generic 3-digit
        ('1234', None),       # Generic 4-digit
        ('123', 'visa'),      # Visa (needs 3 digits)
        ('1234', 'amex'),     # Amex (needs 4 digits)
        ('123', 'amex'),      # Amex with wrong length
        ('12', None),         # Too short
    ]
    
    for cvv, card_type in test_cvvs:
        is_valid = validate_cvv(cvv, card_type)
        status = "✓" if is_valid else "✗"
        type_str = f" ({card_type})" if card_type else ""
        print(f"  {status} CVV '{cvv}'{type_str}")


def example_comprehensive_validation():
    """Example: Comprehensive card validation."""
    print("\n" + "=" * 60)
    print("Comprehensive Card Validation")
    print("=" * 60)
    
    test_cards = [
        ('4111111111111111', '123', 12, 2026),   # Valid Visa
        ('4111111111111112', '123', 12, 2026),   # Invalid Luhn
        ('4111111111111111', '12', 12, 2026),    # Invalid CVV
        ('4111111111111111', '123', 12, 2020),   # Expired
        ('378282246310005', '1234', 12, 2026),   # Valid Amex
    ]
    
    for card, cvv, month, year in test_cards:
        is_valid, errors = validate_card(card, cvv, month, year)
        card_type = get_card_type_name(card)
        status = "✓ Valid" if is_valid else "✗ Invalid"
        
        print(f"\n  Card: {mask_card_number(card)} ({card_type})")
        print(f"  Status: {status}")
        if errors:
            for error in errors:
                print(f"    - {error}")


def example_card_info():
    """Example: Getting detailed card info."""
    print("\n" + "=" * 60)
    print("Detailed Card Information")
    print("=" * 60)
    
    cards = [
        '4111111111111111',
        '378282246310005',
        '6011111111111117',
    ]
    
    for card in cards:
        info = get_card_info(card)
        print(f"\n  Card: {card}")
        print(f"    Type: {info.card_type_name}")
        print(f"    Valid: {info.is_valid}")
        print(f"    Luhn: {'✓' if info.is_valid_luhn else '✗'}")
        print(f"    Length: {info.is_length_valid} (expected: {info.expected_lengths})")
        print(f"    Formatted: {info.formatted_number}")
        print(f"    Masked: {info.masked_number}")
        print(f"    CVV length: {info.cvv_length}")


def example_test_card_generation():
    """Example: Generating test card numbers."""
    print("\n" + "=" * 60)
    print("Test Card Generation")
    print("=" * 60)
    
    # Generate single cards
    print("\n  Single card per type:")
    for card_type in ['visa', 'mastercard', 'amex', 'discover']:
        try:
            card = generate_test_card(card_type)
            info = get_card_info(card)
            print(f"    {card_type}: {info.formatted_number} (Luhn: {'✓' if info.is_valid_luhn else '✗'})")
        except Exception as e:
            print(f"    {card_type}: Error - {e}")
    
    # Generate multiple cards
    print("\n  Generated test cards (variety):")
    cards = generate_test_cards(6)
    for card in cards:
        info = get_card_info(card)
        print(f"    {info.formatted_number} -> {info.card_type_name}")


def example_iin_lookup():
    """Example: BIN/IIN lookup."""
    print("\n" + "=" * 60)
    print("BIN/IIN Lookup")
    print("=" * 60)
    
    iins = ['411111', '555555', '378282', '601111', '356600', '622126']
    
    for iin in iins:
        info = get_iin_info(iin)
        print(f"\n  IIN: {iin}")
        print(f"    Card type: {info.get('card_type_name', 'Unknown')}")
        print(f"    Expected lengths: {info.get('expected_lengths', [])}")
        print(f"    CVV length: {info.get('cvv_length', 'N/A')}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("CREDIT CARD UTILITIES - USAGE EXAMPLES")
    print("=" * 60)
    
    example_luhn_validation()
    example_card_type_detection()
    example_formatting()
    example_expiry_validation()
    example_cvv_validation()
    example_comprehensive_validation()
    example_card_info()
    example_test_card_generation()
    example_iin_lookup()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()