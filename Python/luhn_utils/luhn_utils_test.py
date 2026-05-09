#!/usr/bin/env python3
"""Luhn Utils Tests"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    luhn_checksum, calculate_check_digit, validate,
    generate_with_check_digit, format_card_number,
    mask_card_number, identify_card_type, validate_card,
    generate_test_card, validate_imei, generate_imei,
    extract_luhn_info
)


class TestOutcomeCollector:
    """收集测试结果"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, name):
        self.passed += 1
        print(f"✓ {name}")
    
    def add_fail(self, name, msg):
        self.failed += 1
        self.errors.append((name, msg))
        print(f"✗ {name}: {msg}")
    
    def report(self):
        print(f"\n{'='*60}")
        print(f"Luhn Utils Tests: {self.passed} passed, {self.failed} failed")
        if self.errors:
            print(f"\nFailed tests:")
            for name, msg in self.errors:
                print(f"  - {name}: {msg}")
        print(f"{'='*60}")
        return self.failed == 0


def run_tests():
    results = TestOutcomeCollector()
    
    # Test 1: Luhn checksum calculation
    try:
        checksum = luhn_checksum("7992739871")
        # The checksum depends on implementation
        assert isinstance(checksum, int)
        assert 0 <= checksum <= 9
        results.add_pass("Luhn checksum calculation")
    except Exception as e:
        results.add_fail("Luhn checksum calculation", str(e))
    
    # Test 2: Calculate check digit
    try:
        check = calculate_check_digit("7992739871")
        # For the example "7992739871x", check digit should be 3
        assert check == 3
        results.add_pass("Calculate check digit")
    except Exception as e:
        results.add_fail("Calculate check digit", str(e))
    
    # Test 3: Validate - valid number
    try:
        # Known valid Visa test number
        assert validate("4532015112830366") == True
        results.add_pass("Validate valid number")
    except Exception as e:
        results.add_fail("Validate valid number", str(e))
    
    # Test 4: Validate - invalid number
    try:
        assert validate("4532015112830367") == False  # Changed last digit
        results.add_pass("Validate invalid number")
    except Exception as e:
        results.add_fail("Validate invalid number", str(e))
    
    # Test 5: Validate - with spaces/dashes
    try:
        assert validate("4532-0151-1283-0366") == True
        assert validate("4532 0151 1283 0366") == True
        results.add_pass("Validate with spaces/dashes")
    except Exception as e:
        results.add_fail("Validate with spaces/dashes", str(e))
    
    # Test 6: Validate - too short
    try:
        assert validate("1") == False
        results.add_pass("Validate too short")
    except Exception as e:
        results.add_fail("Validate too short", str(e))
    
    # Test 7: Generate with check digit
    try:
        full = generate_with_check_digit("7992739871")
        assert len(full) == 11
        assert validate(full) == True
        assert full[-1] == '3'
        results.add_pass("Generate with check digit")
    except Exception as e:
        results.add_fail("Generate with check digit", str(e))
    
    # Test 8: Format card number
    try:
        formatted = format_card_number("4532015112830366")
        assert formatted == "4532 0151 1283 0366"
        
        formatted_dash = format_card_number("4532015112830366", "-")
        assert formatted_dash == "4532-0151-1283-0366"
        results.add_pass("Format card number")
    except Exception as e:
        results.add_fail("Format card number", str(e))
    
    # Test 9: Mask card number
    try:
        masked = mask_card_number("4532015112830366")
        assert masked.startswith("4532")
        assert masked.endswith("0366")
        assert "*" in masked
        
        masked_custom = mask_card_number("4532015112830366", show_first=6, show_last=2)
        assert masked_custom.startswith("453201")
        assert masked_custom.endswith("66")
        results.add_pass("Mask card number")
    except Exception as e:
        results.add_fail("Mask card number", str(e))
    
    # Test 10: Identify card type - Visa
    try:
        card_type = identify_card_type("4532015112830366")
        assert card_type == "Visa"
        results.add_pass("Identify card type Visa")
    except Exception as e:
        results.add_fail("Identify card type Visa", str(e))
    
    # Test 11: Identify card type - MasterCard
    try:
        card_type = identify_card_type("5555555555554444")
        assert card_type == "MasterCard"
        results.add_pass("Identify card type MasterCard")
    except Exception as e:
        results.add_fail("Identify card type MasterCard", str(e))
    
    # Test 12: Identify card type - American Express
    try:
        card_type = identify_card_type("378282246310005")
        assert card_type == "American Express"
        results.add_pass("Identify card type American Express")
    except Exception as e:
        results.add_fail("Identify card type American Express", str(e))
    
    # Test 13: Identify card type - Discover
    try:
        card_type = identify_card_type("6011111111111117")
        assert card_type == "Discover"
        results.add_pass("Identify card type Discover")
    except Exception as e:
        results.add_fail("Identify card type Discover", str(e))
    
    # Test 14: Identify card type - JCB
    try:
        card_type = identify_card_type("3530111333300000")
        assert card_type == "JCB"
        results.add_pass("Identify card type JCB")
    except Exception as e:
        results.add_fail("Identify card type JCB", str(e))
    
    # Test 15: Identify card type - unknown
    try:
        card_type = identify_card_type("1234567890123456")
        assert card_type is None
        results.add_pass("Identify card type unknown")
    except Exception as e:
        results.add_fail("Identify card type unknown", str(e))
    
    # Test 16: Validate card - complete validation
    try:
        is_valid, card_type, formatted = validate_card("4532015112830366")
        assert is_valid == True
        assert card_type == "Visa"
        assert formatted == "4532 0151 1283 0366"
        results.add_pass("Validate card complete validation")
    except Exception as e:
        results.add_fail("Validate card complete validation", str(e))
    
    # Test 17: Validate card - invalid card
    try:
        is_valid, card_type, formatted = validate_card("4532015112830367")
        assert is_valid == False
        assert card_type is None
        results.add_pass("Validate card invalid card")
    except Exception as e:
        results.add_fail("Validate card invalid card", str(e))
    
    # Test 18: Generate test card - Visa
    try:
        test_card = generate_test_card("Visa")
        assert len(test_card) == 16
        assert validate(test_card) == True
        assert identify_card_type(test_card) == "Visa"
        results.add_pass("Generate test card Visa")
    except Exception as e:
        results.add_fail("Generate test card Visa", str(e))
    
    # Test 19: Generate test card - MasterCard
    try:
        test_card = generate_test_card("MasterCard")
        assert len(test_card) == 16
        assert validate(test_card) == True
        results.add_pass("Generate test card MasterCard")
    except Exception as e:
        results.add_fail("Generate test card MasterCard", str(e))
    
    # Test 20: Generate test card - American Express
    try:
        test_card = generate_test_card("American Express")
        # AmEx prefix is 14 chars, +1 check digit = 15 chars
        assert len(test_card) >= 14
        assert validate(test_card) == True
        results.add_pass("Generate test card American Express")
    except Exception as e:
        results.add_fail("Generate test card American Express", str(e))
    
    # Test 21: Validate IMEI - valid
    try:
        # Known valid IMEI
        assert validate_imei("490154203237518") == True
        results.add_pass("Validate IMEI valid")
    except Exception as e:
        results.add_fail("Validate IMEI valid", str(e))
    
    # Test 22: Validate IMEI - invalid
    try:
        assert validate_imei("490154203237519") == False
        results.add_pass("Validate IMEI invalid")
    except Exception as e:
        results.add_fail("Validate IMEI invalid", str(e))
    
    # Test 23: Validate IMEI - wrong length
    try:
        assert validate_imei("1234567890") == False  # Not 15 digits
        results.add_pass("Validate IMEI wrong length")
    except Exception as e:
        results.add_fail("Validate IMEI wrong length", str(e))
    
    # Test 24: Generate IMEI
    try:
        imei = generate_imei()
        assert len(imei) == 15
        assert validate_imei(imei) == True
        results.add_pass("Generate IMEI")
    except Exception as e:
        results.add_fail("Generate IMEI", str(e))
    
    # Test 25: Generate IMEI with custom TAC
    try:
        imei = generate_imei(tac="01234567", serial="123456")
        assert imei.startswith("01234567123456")
        assert validate_imei(imei) == True
        results.add_pass("Generate IMEI with custom TAC")
    except Exception as e:
        results.add_fail("Generate IMEI with custom TAC", str(e))
    
    # Test 26: Extract Luhn info
    try:
        info = extract_luhn_info("4532015112830366")
        assert info['valid'] == True
        assert info['length'] == 16
        assert info['card_type'] == "Visa"
        assert info['formatted'] == "4532 0151 1283 0366"
        assert 'masked' in info
        results.add_pass("Extract Luhn info")
    except Exception as e:
        results.add_fail("Extract Luhn info", str(e))
    
    # Test 27: Extract Luhn info - invalid
    try:
        info = extract_luhn_info("invalid")
        assert info['valid'] == False
        assert 'error' in info
        results.add_pass("Extract Luhn info invalid")
    except Exception as e:
        results.add_fail("Extract Luhn info invalid", str(e))
    
    # Test 28: Check digit correctness
    try:
        info = extract_luhn_info("4532015112830366")
        assert info['check_digit_correct'] == True
        
        info2 = extract_luhn_info("4532015112830367")
        assert info2['check_digit_correct'] == False
        results.add_pass("Check digit correctness")
    except Exception as e:
        results.add_fail("Check digit correctness", str(e))
    
    # Test 29: Empty input handling
    try:
        info = extract_luhn_info("")
        assert info['valid'] == False
        results.add_pass("Empty input handling")
    except Exception as e:
        results.add_fail("Empty input handling", str(e))
    
    # Test 30: Non-digit handling
    try:
        # Should extract digits from non-digit characters
        info = extract_luhn_info("abc4532def0151ghi1283jkl0366")
        assert info['valid'] == True
        assert info['number'] == "4532015112830366"
        results.add_pass("Non-digit handling")
    except Exception as e:
        results.add_fail("Non-digit handling", str(e))
    
    return results.report()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)