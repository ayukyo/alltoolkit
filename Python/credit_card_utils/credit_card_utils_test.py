#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Credit Card Utilities Tests
=========================================
Comprehensive tests for the credit card utilities module.

Run with: python -m pytest credit_card_utils_test.py -v
Or simply: python credit_card_utils_test.py
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    luhn_check,
    calculate_luhn_check_digit,
    validate_card,
    is_valid_card,
    detect_card_type,
    get_card_info,
    get_all_card_types,
    format_card,
    mask_card,
    mask_card_formatted,
    is_valid_cvv,
    is_valid_expiry,
    validate_expiry,
    generate_test_card,
    generate_random_card,
    get_bin,
    is_issuer,
    clean_card_number,
    get_card_length_range,
    summarize_card,
    CARD_PATTERNS,
    TEST_CARDS
)


class TestLuhnCheck:
    """Tests for Luhn algorithm validation."""
    
    def test_valid_visa(self):
        """Test valid Visa card."""
        assert luhn_check('4111111111111111') is True
    
    def test_valid_mastercard(self):
        """Test valid MasterCard."""
        assert luhn_check('5555555555554444') is True
    
    def test_valid_amex(self):
        """Test valid American Express card."""
        assert luhn_check('378282246310005') is True
    
    def test_invalid_card(self):
        """Test invalid card (wrong check digit)."""
        assert luhn_check('4111111111111112') is False
    
    def test_empty_string(self):
        """Test empty string."""
        assert luhn_check('') is False
    
    def test_single_digit(self):
        """Test single digit."""
        assert luhn_check('4') is False
    
    def test_with_spaces(self):
        """Test card with spaces."""
        assert luhn_check('4111 1111 1111 1111') is True
    
    def test_with_dashes(self):
        """Test card with dashes."""
        assert luhn_check('4111-1111-1111-1111') is True
    
    def test_zero_card(self):
        """Test all zeros (should pass Luhn but is not a real card)."""
        assert luhn_check('0000000000000000') is True
    
    def test_non_digit_input(self):
        """Test with non-digit characters."""
        assert luhn_check('abcd1234efgh5678') is False


class TestCalculateLuhnCheckDigit:
    """Tests for Luhn check digit calculation."""
    
    def test_visa_check_digit(self):
        """Test Visa check digit calculation."""
        # 411111111111111 + check_digit = 4111111111111111
        assert calculate_luhn_check_digit('411111111111111') == 1
    
    def test_mastercard_check_digit(self):
        """Test MasterCard check digit calculation."""
        assert calculate_luhn_check_digit('555555555555444') == 4
    
    def test_amex_check_digit(self):
        """Test Amex check digit calculation."""
        assert calculate_luhn_check_digit('37828224631000') == 5


class TestValidateCard:
    """Tests for comprehensive card validation."""
    
    def test_valid_visa_validation(self):
        """Test full validation of valid Visa."""
        result = validate_card('4111111111111111')
        assert result['valid'] is True
        assert result['luhn_valid'] is True
        assert result['card_type'] == 'visa'
        assert result['card_name'] == 'Visa'
    
    def test_valid_mastercard_validation(self):
        """Test full validation of valid MasterCard."""
        result = validate_card('5555555555554444')
        assert result['valid'] is True
        assert result['card_type'] == 'mastercard'
    
    def test_valid_amex_validation(self):
        """Test full validation of valid Amex."""
        result = validate_card('378282246310005')
        assert result['valid'] is True
        assert result['card_type'] == 'amex'
    
    def test_invalid_card_validation(self):
        """Test validation of invalid card."""
        result = validate_card('4111111111111112')
        assert result['valid'] is False
        assert result['luhn_valid'] is False
    
    def test_empty_card_validation(self):
        """Test validation of empty card."""
        result = validate_card('')
        assert result['valid'] is False
    
    def test_too_short_card(self):
        """Test validation of too short card."""
        result = validate_card('123456789012')
        assert result['valid'] is False


class TestIsValidCard:
    """Tests for quick card validity check."""
    
    def test_valid_cards(self):
        """Test known valid cards."""
        assert is_valid_card('4111111111111111') is True
        assert is_valid_card('5555555555554444') is True
        assert is_valid_card('378282246310005') is True
    
    def test_invalid_cards(self):
        """Test invalid cards."""
        assert is_valid_card('1234567890123456') is False
        assert is_valid_card('0000000000000001') is False


class TestDetectCardType:
    """Tests for card type detection."""
    
    def test_detect_visa(self):
        """Test Visa detection."""
        assert detect_card_type('4111111111111111') == 'visa'
        assert detect_card_type('4012888888881881') == 'visa'
    
    def test_detect_mastercard(self):
        """Test MasterCard detection."""
        assert detect_card_type('5555555555554444') == 'mastercard'
        assert detect_card_type('2223000048400011') == 'mastercard'
    
    def test_detect_amex(self):
        """Test American Express detection."""
        assert detect_card_type('378282246310005') == 'amex'
        assert detect_card_type('371449635398431') == 'amex'
    
    def test_detect_discover(self):
        """Test Discover detection."""
        assert detect_card_type('6011111111111117') == 'discover'
    
    def test_detect_jcb(self):
        """Test JCB detection."""
        assert detect_card_type('3530111333300000') == 'jcb'
    
    def test_detect_diners_club(self):
        """Test Diners Club detection."""
        assert detect_card_type('3056930009020004') == 'diners_club'
    
    def test_detect_unionpay(self):
        """Test UnionPay detection."""
        assert detect_card_type('6200000000000005') == 'unionpay'
    
    def test_detect_unknown(self):
        """Test unknown card type."""
        # Valid Luhn but unknown prefix
        assert detect_card_type('0000000000000000') is None


class TestGetCardInfo:
    """Tests for card info retrieval."""
    
    def test_get_visa_info(self):
        """Test getting Visa card info."""
        info = get_card_info('visa')
        assert info is not None
        assert info['name'] == 'Visa'
        assert 16 in info['lengths']
        assert info['cvv_length'] == 3
    
    def test_get_amex_info(self):
        """Test getting Amex card info."""
        info = get_card_info('amex')
        assert info['name'] == 'American Express'
        assert info['cvv_length'] == 4
    
    def test_get_unknown_info(self):
        """Test getting unknown card info."""
        assert get_card_info('unknown') is None


class TestGetAllCardTypes:
    """Tests for getting all card types."""
    
    def test_get_all_types(self):
        """Test getting all card types."""
        types = get_all_card_types()
        assert 'visa' in types
        assert 'mastercard' in types
        assert 'amex' in types
        assert len(types) >= 8  # At least 8 card types


class TestFormatCard:
    """Tests for card number formatting."""
    
    def test_format_visa(self):
        """Test Visa formatting."""
        assert format_card('4111111111111111') == '4111 1111 1111 1111'
    
    def test_format_amex(self):
        """Test Amex formatting (4-6-5)."""
        assert format_card('378282246310005') == '3782 822463 10005'
    
    def test_format_with_dashes(self):
        """Test formatting with dashes."""
        assert format_card('4111111111111111', '-') == '4111-1111-1111-1111'
    
    def test_format_with_spaces_input(self):
        """Test formatting card that already has spaces."""
        assert format_card('4111 1111 1111 1111') == '4111 1111 1111 1111'
    
    def test_format_short_number(self):
        """Test formatting short number."""
        assert format_card('1234') == '1234'


class TestMaskCard:
    """Tests for card number masking."""
    
    def test_default_mask(self):
        """Test default masking."""
        # 16 digits: show 4 first + 4 last = 8 middle masked
        assert mask_card('4111111111111111') == '4111********1111'
    
    def test_custom_mask_char(self):
        """Test masking with custom character."""
        assert mask_card('4111111111111111', mask_char='X') == '4111XXXXXXXX1111'
    
    def test_no_first(self):
        """Test masking without showing first digits."""
        assert mask_card('4111111111111111', show_first=0) == '************1111'
    
    def test_no_last(self):
        """Test masking without showing last digits."""
        assert mask_card('4111111111111111', show_last=0) == '4111************'
    
    def test_mask_formatted(self):
        """Test formatted masking."""
        masked = mask_card_formatted('4111111111111111')
        # 16 digits: show first 4 + last 4, mask middle 8
        # Formatted as 4 groups of 4: 4111 **** **** 1111
        assert masked == '4111 **** **** 1111'


class TestIsValidCVV:
    """Tests for CVV validation."""
    
    def test_valid_cvv_3_digit(self):
        """Test valid 3-digit CVV."""
        assert is_valid_cvv('123') is True
        assert is_valid_cvv('999') is True
    
    def test_valid_cvv_4_digit(self):
        """Test valid 4-digit CVV."""
        assert is_valid_cvv('1234') is True
    
    def test_invalid_cvv_too_short(self):
        """Test CVV too short."""
        assert is_valid_cvv('12') is False
    
    def test_invalid_cvv_too_long(self):
        """Test CVV too long."""
        assert is_valid_cvv('12345') is False
    
    def test_cvv_with_letters(self):
        """Test CVV with letters."""
        assert is_valid_cvv('abc') is False
    
    def test_amex_cvv(self):
        """Test Amex CVV (4 digits)."""
        assert is_valid_cvv('1234', 'amex') is True
        assert is_valid_cvv('123', 'amex') is False
    
    def test_visa_cvv(self):
        """Test Visa CVV (3 digits)."""
        assert is_valid_cvv('123', 'visa') is True
        assert is_valid_cvv('1234', 'visa') is False


class TestIsValidExpiry:
    """Tests for expiry date validation."""
    
    def test_valid_future_expiry(self):
        """Test valid future expiry."""
        future_year = datetime.now().year + 1
        assert is_valid_expiry(12, future_year) is True
    
    def test_valid_current_month(self):
        """Test valid current month."""
        now = datetime.now()
        assert is_valid_expiry(now.month, now.year) is True
    
    def test_expired_date(self):
        """Test expired date."""
        assert is_valid_expiry(1, 2020) is False
    
    def test_invalid_month(self):
        """Test invalid month."""
        future_year = datetime.now().year + 1
        assert is_valid_expiry(13, future_year) is False
        assert is_valid_expiry(0, future_year) is False
    
    def test_two_digit_year(self):
        """Test 2-digit year conversion."""
        current_year = datetime.now().year
        two_digit = current_year % 100
        future_month = ((datetime.now().month + 1) % 12) or 12
        assert is_valid_expiry(future_month, two_digit + 1) is True


class TestValidateExpiry:
    """Tests for comprehensive expiry validation."""
    
    def test_valid_expiry_string(self):
        """Test validation with string inputs."""
        # Use a future year (2027+)
        result = validate_expiry('12', '28')
        assert result['valid'] is True
        assert result['month'] == 12
        assert result['year'] == 2028
    
    def test_invalid_format(self):
        """Test validation with invalid format."""
        result = validate_expiry('ab', 'cd')
        assert result['valid'] is False
    
    def test_expired_expiry(self):
        """Test expired expiry."""
        result = validate_expiry(1, 2020)
        assert result['valid'] is False
        assert result['expired'] is True


class TestGenerateTestCard:
    """Tests for test card generation."""
    
    def test_generate_visa(self):
        """Test Visa test card generation."""
        card = generate_test_card('visa')
        assert is_valid_card(card) is True
        assert detect_card_type(card) == 'visa'
    
    def test_generate_mastercard(self):
        """Test MasterCard test card generation."""
        card = generate_test_card('mastercard')
        assert is_valid_card(card) is True
        assert detect_card_type(card) == 'mastercard'
    
    def test_generate_amex(self):
        """Test Amex test card generation."""
        card = generate_test_card('amex')
        assert is_valid_card(card) is True
        assert detect_card_type(card) == 'amex'


class TestGenerateRandomCard:
    """Tests for random card generation."""
    
    def test_generate_random_visa(self):
        """Test random Visa generation."""
        card = generate_random_card('visa')
        assert is_valid_card(card) is True
        assert detect_card_type(card) == 'visa'
        assert len(card) in CARD_PATTERNS['visa']['lengths']
    
    def test_generate_random_mastercard(self):
        """Test random MasterCard generation."""
        card = generate_random_card('mastercard')
        assert is_valid_card(card) is True
        assert detect_card_type(card) == 'mastercard'
    
    def test_generate_random_amex(self):
        """Test random Amex generation."""
        card = generate_random_card('amex')
        assert is_valid_card(card) is True
        assert detect_card_type(card) == 'amex'
        assert len(card) == 15
    
    def test_generate_with_length(self):
        """Test generation with specific length."""
        card = generate_random_card('visa', length=16)
        assert len(card) == 16
    
    def test_generate_multiple_unique(self):
        """Test multiple generations produce different cards."""
        cards = [generate_random_card('visa') for _ in range(10)]
        # Very unlikely to get duplicates
        assert len(set(cards)) > 5


class TestGetBin:
    """Tests for BIN extraction."""
    
    def test_default_bin(self):
        """Test default BIN length."""
        assert get_bin('4111111111111111') == '411111'
    
    def test_custom_bin_length(self):
        """Test custom BIN length."""
        assert get_bin('4111111111111111', length=8) == '41111111'
    
    def test_short_card(self):
        """Test BIN with short card."""
        assert get_bin('123456', length=8) == '123456'


class TestIsIssuer:
    """Tests for issuer checking."""
    
    def test_is_visa(self):
        """Test Visa issuer check."""
        assert is_issuer('4111111111111111', 'visa') is True
        assert is_issuer('4111111111111111', 'VISA') is True  # Case insensitive
    
    def test_is_not_visa(self):
        """Test non-Visa check."""
        assert is_issuer('5555555555554444', 'visa') is False


class TestCleanCardNumber:
    """Tests for card number cleaning."""
    
    def test_clean_spaces(self):
        """Test removing spaces."""
        assert clean_card_number('4111 1111 1111 1111') == '4111111111111111'
    
    def test_clean_dashes(self):
        """Test removing dashes."""
        assert clean_card_number('4111-1111-1111-1111') == '4111111111111111'
    
    def test_clean_mixed(self):
        """Test removing mixed characters."""
        assert clean_card_number('4111-1111 1111.1111') == '4111111111111111'


class TestGetCardLengthRange:
    """Tests for card length range."""
    
    def test_length_range(self):
        """Test getting length range."""
        min_len, max_len = get_card_length_range()
        # Maestro has 12 digits minimum, maximum is 19
        assert min_len == 12
        assert max_len == 19


class TestSummarizeCard:
    """Tests for card summary."""
    
    def test_summarize_visa(self):
        """Test Visa summary."""
        summary = summarize_card('4111111111111111')
        assert summary['type'] == 'visa'
        assert summary['name'] == 'Visa'
        assert summary['valid'] is True
        assert summary['luhn_valid'] is True
        assert summary['length'] == 16
        assert summary['bin'] == '411111'
    
    def test_summarize_masked(self):
        """Test that summary shows masked number."""
        summary = summarize_card('4111111111111111')
        assert '4111' in summary['number']
        assert '1111' in summary['number']
        assert '********' in summary['number']


class TestAllTestCards:
    """Tests to verify all test cards are valid."""
    
    def test_all_visa_test_cards(self):
        """Test all Visa test cards are valid."""
        for card in TEST_CARDS['visa']:
            assert is_valid_card(card), f"Visa test card {card} should be valid"
    
    def test_all_mastercard_test_cards(self):
        """Test all MasterCard test cards are valid."""
        for card in TEST_CARDS['mastercard']:
            assert is_valid_card(card), f"MasterCard test card {card} should be valid"
    
    def test_all_amex_test_cards(self):
        """Test all Amex test cards are valid."""
        for card in TEST_CARDS['amex']:
            assert is_valid_card(card), f"Amex test card {card} should be valid"


def run_tests():
    """Run all tests and print results."""
    print("=" * 60)
    print("Credit Card Utilities - Test Suite")
    print("=" * 60)
    
    test_classes = [
        TestLuhnCheck,
        TestCalculateLuhnCheckDigit,
        TestValidateCard,
        TestIsValidCard,
        TestDetectCardType,
        TestGetCardInfo,
        TestGetAllCardTypes,
        TestFormatCard,
        TestMaskCard,
        TestIsValidCVV,
        TestIsValidExpiry,
        TestValidateExpiry,
        TestGenerateTestCard,
        TestGenerateRandomCard,
        TestGetBin,
        TestIsIssuer,
        TestCleanCardNumber,
        TestGetCardLengthRange,
        TestSummarizeCard,
        TestAllTestCards,
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    for test_class in test_classes:
        instance = test_class()
        test_methods = [m for m in dir(instance) if m.startswith('test_')]
        
        print(f"\n{test_class.__name__}:")
        
        for method_name in test_methods:
            total_tests += 1
            try:
                getattr(instance, method_name)()
                print(f"  ✓ {method_name}")
                passed_tests += 1
            except AssertionError as e:
                print(f"  ✗ {method_name}: {e}")
                failed_tests.append(f"{test_class.__name__}.{method_name}")
            except Exception as e:
                print(f"  ✗ {method_name}: {type(e).__name__}: {e}")
                failed_tests.append(f"{test_class.__name__}.{method_name}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed_tests}/{total_tests} tests passed")
    
    if failed_tests:
        print(f"\nFailed tests:")
        for test in failed_tests:
            print(f"  - {test}")
        return 1
    else:
        print("\n✓ All tests passed!")
        return 0


if __name__ == '__main__':
    sys.exit(run_tests())