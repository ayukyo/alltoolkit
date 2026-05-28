#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Credit Card Utilities Test Suite
==============================================
Comprehensive tests for credit_card_utils module.

Run with: python -m pytest credit_card_utils_test.py -v
Or directly: python credit_card_utils_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Luhn functions
    luhn_checksum, validate_luhn,
    
    # Card type detection
    detect_card_type, get_card_type_name,
    
    # Card number operations
    clean_card_number, format_card_number, mask_card_number,
    validate_card_length,
    
    # CVV validation
    validate_cvv,
    
    # Expiry validation
    validate_expiry, parse_expiry_string,
    
    # Comprehensive validation
    get_card_info, validate_card,
    
    # Test card generation
    generate_test_card, generate_test_cards,
    
    # BIN/IIN lookup
    get_iin_info,
    
    # Utilities
    compare_cards, card_to_int, int_to_card,
    
    # Data classes
    CardInfo, ExpiryCheck,
    
    # Constants
    CARD_PATTERNS, CARD_TYPE_NAMES
)

import unittest
from datetime import datetime, timedelta


class TestLuhnAlgorithm(unittest.TestCase):
    """Test Luhn algorithm implementation."""
    
    def test_luhn_checksum(self):
        """Test Luhn checksum calculation."""
        # Known test cases: checksum for number without check digit
        self.assertEqual(luhn_checksum('411111111111111'), 1)  # Visa 4111111111111111
        self.assertEqual(luhn_checksum('424242424242424'), 2)  # Visa 4242424242424242
        self.assertEqual(luhn_checksum('555555555555444'), 4)  # MC 5555555555554444
    
    def test_validate_luhn_valid_cards(self):
        """Test Luhn validation with valid card numbers."""
        valid_cards = [
            '4111111111111111',  # Visa (known test card)
            '4242424242424242',  # Visa (known test card)
            '5555555555554444',  # Mastercard (known test card)
            '378282246310005',   # Amex (known test card)
            '371449635398431',   # Amex (known test card)
            '6011111111111117',  # Discover (known test card)
        ]
        for card in valid_cards:
            with self.subTest(card=card):
                self.assertTrue(validate_luhn(card))
    
    def test_validate_luhn_invalid_cards(self):
        """Test Luhn validation with invalid card numbers."""
        invalid_cards = [
            '4111111111111112',  # Wrong check digit
            '4242424242424243',  # Wrong check digit
            '5555555555554445',  # Wrong check digit
            '1234567890123456',  # Invalid
        ]
        for card in invalid_cards:
            with self.subTest(card=card):
                self.assertFalse(validate_luhn(card))
    
    def test_validate_luhn_with_formatting(self):
        """Test Luhn validation with formatted card numbers."""
        self.assertTrue(validate_luhn('4111-1111-1111-1111'))
        self.assertTrue(validate_luhn('4111 1111 1111 1111'))
        self.assertTrue(validate_luhn('  4111111111111111  '))
    
    def test_validate_luhn_edge_cases(self):
        """Test Luhn validation edge cases."""
        self.assertFalse(validate_luhn(''))
        self.assertFalse(validate_luhn('1'))
        self.assertFalse(validate_luhn('abc'))
        self.assertFalse(validate_luhn('1234abcd5678'))


class TestCardTypeDetection(unittest.TestCase):
    """Test card type detection."""
    
    def test_detect_visa(self):
        """Test Visa card detection."""
        visa_cards = [
            '4111111111111111',
            '4242424242424242',
            '4012888888881881',
        ]
        for card in visa_cards:
            card_type, info = detect_card_type(card)
            with self.subTest(card=card):
                self.assertEqual(card_type, 'visa')
    
    def test_detect_mastercard(self):
        """Test Mastercard detection."""
        mc_cards = [
            '5555555555554444',
            '2223000048400011',  # New Mastercard range
        ]
        for card in mc_cards:
            card_type, info = detect_card_type(card)
            with self.subTest(card=card):
                self.assertEqual(card_type, 'mastercard')
    
    def test_detect_amex(self):
        """Test American Express detection."""
        amex_cards = [
            '378282246310005',
            '371449635398431',
        ]
        for card in amex_cards:
            card_type, info = detect_card_type(card)
            with self.subTest(card=card):
                self.assertEqual(card_type, 'amex')
    
    def test_detect_discover(self):
        """Test Discover card detection."""
        discover_cards = [
            '6011111111111117',
            '6011000990139424',
        ]
        for card in discover_cards:
            card_type, info = detect_card_type(card)
            with self.subTest(card=card):
                self.assertEqual(card_type, 'discover')
    
    def test_detect_unknown(self):
        """Test unknown card type detection."""
        unknown_cards = [
            '9999999999999999',
            '1234567890123456',
        ]
        for card in unknown_cards:
            card_type, info = detect_card_type(card)
            with self.subTest(card=card):
                self.assertEqual(card_type, 'unknown')
    
    def test_get_card_type_name(self):
        """Test card type name retrieval."""
        self.assertEqual(get_card_type_name('4111111111111111'), 'Visa')
        self.assertEqual(get_card_type_name('5555555555554444'), 'Mastercard')
        self.assertEqual(get_card_type_name('378282246310005'), 'American Express')


class TestCardNumberOperations(unittest.TestCase):
    """Test card number cleaning and formatting."""
    
    def test_clean_card_number(self):
        """Test card number cleaning."""
        self.assertEqual(clean_card_number('4111-1111-1111-1111'), '4111111111111111')
        self.assertEqual(clean_card_number('4111 1111 1111 1111'), '4111111111111111')
        self.assertEqual(clean_card_number('  4111111111111111  '), '4111111111111111')
        self.assertEqual(clean_card_number('4111.1111.1111.1111'), '4111111111111111')
    
    def test_format_card_number_visa(self):
        """Test Visa card formatting."""
        self.assertEqual(format_card_number('4111111111111111'), '4111 1111 1111 1111')
    
    def test_format_card_number_amex(self):
        """Test Amex card formatting (4-6-5 format)."""
        self.assertEqual(format_card_number('378282246310005'), '3782 822463 10005')
    
    def test_mask_card_number(self):
        """Test card number masking."""
        masked = mask_card_number('4111111111111111')
        self.assertEqual(masked, '4111********1111')
        self.assertTrue(masked.startswith('4111'))
        self.assertTrue(masked.endswith('1111'))
    
    def test_mask_card_number_custom(self):
        """Test card number masking with custom options."""
        masked = mask_card_number('4111111111111111', mask_char='#', visible_start=2, visible_end=2)
        self.assertEqual(masked, '41############11')
    
    def test_mask_short_number(self):
        """Test masking of short numbers."""
        masked = mask_card_number('123456')
        self.assertEqual(masked, '123456')  # No mask for short numbers
    
    def test_validate_card_length(self):
        """Test card length validation."""
        # Valid Visa
        is_valid, lengths = validate_card_length('4111111111111111')
        self.assertTrue(is_valid)
        self.assertIn(16, lengths)
        
        # Invalid length for Visa
        is_valid, _ = validate_card_length('411111111111111')
        self.assertFalse(is_valid)
        
        # Valid Amex (15 digits)
        is_valid, lengths = validate_card_length('378282246310005')
        self.assertTrue(is_valid)
        self.assertIn(15, lengths)


class TestCVVValidation(unittest.TestCase):
    """Test CVV validation."""
    
    def test_valid_cvv_3_digit(self):
        """Test valid 3-digit CVV."""
        self.assertTrue(validate_cvv('123'))
        self.assertTrue(validate_cvv('999'))
        self.assertTrue(validate_cvv('000'))
    
    def test_valid_cvv_4_digit(self):
        """Test valid 4-digit CVV."""
        self.assertTrue(validate_cvv('1234'))
        self.assertTrue(validate_cvv('9999'))
    
    def test_invalid_cvv(self):
        """Test invalid CVV."""
        self.assertFalse(validate_cvv('12'))     # Too short
        self.assertFalse(validate_cvv('12345'))   # Too long
        self.assertFalse(validate_cvv('abc'))    # Non-numeric
        self.assertFalse(validate_cvv(''))       # Empty
    
    def test_cvv_for_card_type(self):
        """Test CVV validation with card type."""
        # Amex requires 4-digit CVV
        self.assertTrue(validate_cvv('1234', 'amex'))
        self.assertFalse(validate_cvv('123', 'amex'))
        
        # Visa uses 3-digit CVV
        self.assertTrue(validate_cvv('123', 'visa'))
        self.assertFalse(validate_cvv('1234', 'visa'))


class TestExpiryValidation(unittest.TestCase):
    """Test expiry date validation."""
    
    def test_valid_future_expiry(self):
        """Test valid future expiry date."""
        future_year = datetime.now().year + 1
        result = validate_expiry(12, future_year)
        self.assertTrue(result.is_valid)
        self.assertFalse(result.is_expired)
    
    def test_expired_date(self):
        """Test expired date detection."""
        past_year = datetime.now().year - 1
        result = validate_expiry(1, past_year)
        self.assertTrue(result.is_expired)
        self.assertFalse(result.is_valid)
    
    def test_invalid_month(self):
        """Test invalid month detection."""
        result = validate_expiry(13, datetime.now().year + 1)
        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.error)
    
    def test_expiry_formatting(self):
        """Test expiry date formatting."""
        result = validate_expiry(5, 2026)
        self.assertEqual(result.formatted, '05/26')
    
    def test_days_until_expiry(self):
        """Test days until expiry calculation."""
        future_year = datetime.now().year + 1
        result = validate_expiry(12, future_year)
        self.assertIsNotNone(result.days_until_expiry)
        self.assertGreater(result.days_until_expiry, 0)
    
    def test_parse_expiry_string(self):
        """Test expiry string parsing."""
        month, year = parse_expiry_string('12/25')
        self.assertEqual(month, 12)
        self.assertEqual(year, 2025)
        
        month, year = parse_expiry_string('06/2026')
        self.assertEqual(month, 6)
        self.assertEqual(year, 2026)
        
        month, year = parse_expiry_string('1225')
        self.assertEqual(month, 12)
        self.assertEqual(year, 2025)
    
    def test_parse_invalid_expiry(self):
        """Test parsing invalid expiry strings."""
        month, year = parse_expiry_string('invalid')
        self.assertIsNone(month)
        self.assertIsNone(year)


class TestComprehensiveValidation(unittest.TestCase):
    """Test comprehensive card validation."""
    
    def test_get_card_info(self):
        """Test comprehensive card info retrieval."""
        info = get_card_info('4111111111111111')
        
        self.assertIsInstance(info, CardInfo)
        self.assertEqual(info.card_type, 'visa')
        self.assertEqual(info.card_type_name, 'Visa')
        self.assertTrue(info.is_valid)
        self.assertTrue(info.is_valid_luhn)
        self.assertTrue(info.is_length_valid)
        self.assertEqual(info.cvv_length, 3)
    
    def test_get_card_info_amex(self):
        """Test Amex card info."""
        info = get_card_info('378282246310005')
        
        self.assertEqual(info.card_type, 'amex')
        self.assertEqual(info.cvv_length, 4)
        self.assertIn(15, info.expected_lengths)
    
    def test_validate_card_valid(self):
        """Test valid card validation."""
        is_valid, errors = validate_card('4111111111111111')
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_card_invalid_luhn(self):
        """Test invalid Luhn detection."""
        is_valid, errors = validate_card('4111111111111112')
        self.assertFalse(is_valid)
        self.assertIn('Luhn', errors[0])
    
    def test_validate_card_with_cvv(self):
        """Test card validation with CVV."""
        is_valid, _ = validate_card('4111111111111111', cvv='123')
        self.assertTrue(is_valid)
        
        is_valid, errors = validate_card('4111111111111111', cvv='12')
        self.assertFalse(is_valid)
    
    def test_validate_card_empty(self):
        """Test validation of empty card number."""
        is_valid, errors = validate_card('')
        self.assertFalse(is_valid)


class TestCardGeneration(unittest.TestCase):
    """Test card number generation."""
    
    def test_generate_visa(self):
        """Test Visa card generation."""
        card = generate_test_card('visa')
        self.assertTrue(validate_luhn(card))
        card_type, _ = detect_card_type(card)
        self.assertEqual(card_type, 'visa')
    
    def test_generate_mastercard(self):
        """Test Mastercard generation."""
        card = generate_test_card('mastercard')
        self.assertTrue(validate_luhn(card))
        card_type, _ = detect_card_type(card)
        self.assertEqual(card_type, 'mastercard')
    
    def test_generate_amex(self):
        """Test Amex generation."""
        card = generate_test_card('amex')
        self.assertTrue(validate_luhn(card))
        card_type, _ = detect_card_type(card)
        self.assertEqual(card_type, 'amex')
        self.assertEqual(len(card), 15)
    
    def test_generate_multiple(self):
        """Test generating multiple cards."""
        cards = generate_test_cards(10)
        self.assertEqual(len(cards), 10)
        for card in cards:
            self.assertTrue(validate_luhn(card))
    
    def test_generate_specific_length(self):
        """Test generating card with specific length."""
        card = generate_test_card('visa', length=16)
        self.assertEqual(len(card), 16)
    
    def test_generate_invalid_type(self):
        """Test generating with invalid card type."""
        with self.assertRaises(ValueError):
            generate_test_card('invalid_type')
    
    def test_generate_invalid_length(self):
        """Test generating with invalid length."""
        with self.assertRaises(ValueError):
            generate_test_card('visa', length=15)  # Visa doesn't support 15-digit


class TestIINLookup(unittest.TestCase):
    """Test BIN/IIN lookup."""
    
    def test_get_iin_info_visa(self):
        """Test Visa IIN lookup."""
        info = get_iin_info('411111')
        self.assertEqual(info['card_type'], 'visa')
        self.assertEqual(info['card_type_name'], 'Visa')
    
    def test_get_iin_info_amex(self):
        """Test Amex IIN lookup."""
        info = get_iin_info('378282')
        self.assertEqual(info['card_type'], 'amex')
    
    def test_get_iin_info_too_short(self):
        """Test IIN lookup with too short input."""
        info = get_iin_info('12345')
        self.assertIn('error', info)


class TestUtilities(unittest.TestCase):
    """Test utility functions."""
    
    def test_compare_cards(self):
        """Test card comparison."""
        self.assertEqual(compare_cards('4000000000000001', '4000000000000001'), 0)
        self.assertEqual(compare_cards('4000000000000001', '4000000000000002'), -1)
        self.assertEqual(compare_cards('4000000000000002', '4000000000000001'), 1)
    
    def test_card_to_int(self):
        """Test card to integer conversion."""
        self.assertEqual(card_to_int('4111111111111111'), 4111111111111111)
        self.assertEqual(card_to_int('4111-1111-1111-1111'), 4111111111111111)
    
    def test_int_to_card(self):
        """Test integer to card conversion."""
        self.assertEqual(int_to_card(4111111111111111), '4111111111111111')


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_empty_string(self):
        """Test handling of empty strings."""
        self.assertEqual(clean_card_number(''), '')
        self.assertEqual(card_to_int(''), 0)
    
    def test_non_digit_characters(self):
        """Test handling of non-digit characters."""
        self.assertEqual(clean_card_number('abcd'), '')
    
    def test_card_info_unknown_type(self):
        """Test card info for unknown type."""
        info = get_card_info('9999999999999999')
        self.assertEqual(info.card_type, 'unknown')
        self.assertEqual(info.card_type_name, 'Unknown')


if __name__ == '__main__':
    unittest.main(verbosity=2)