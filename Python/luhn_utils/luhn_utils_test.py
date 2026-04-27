"""
Luhn Algorithm Utilities - Unit Tests
=====================================

Comprehensive tests for the Luhn algorithm implementation.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    validate,
    calculate_check_digit,
    add_check_digit,
    strip_formatting,
    format_number,
    generate_valid_number,
    generate_test_credit_cards,
    find_check_digit_errors,
    calculate_luhn_sum,
    get_luhn_digit_transformations,
    LuhnValidator,
    identify_card_type,
    CARD_PREFIXES,
)


class TestLuhnValidation(unittest.TestCase):
    """Test Luhn validation functionality."""
    
    def test_valid_visa_card(self):
        """Test validation of valid Visa card number."""
        self.assertTrue(validate("4532015112830366"))
    
    def test_valid_mastercard(self):
        """Test validation of valid MasterCard number."""
        self.assertTrue(validate("5500000000000004"))
    
    def test_valid_amex(self):
        """Test validation of valid American Express number."""
        self.assertTrue(validate("378282246310005"))
    
    def test_valid_discover(self):
        """Test validation of valid Discover card number."""
        self.assertTrue(validate("6011111111111117"))
    
    def test_invalid_card(self):
        """Test validation of invalid card number."""
        self.assertFalse(validate("4532015112830367"))
    
    def test_invalid_wrong_length(self):
        """Test validation with too short number."""
        self.assertFalse(validate("123"))
    
    def test_invalid_empty(self):
        """Test validation with empty string."""
        self.assertFalse(validate(""))
    
    def test_invalid_all_zeros(self):
        """Test validation with all zeros (still passes Luhn)."""
        # All zeros pass Luhn (sum = 0)
        self.assertTrue(validate("0000000000000000"))
    
    def test_with_formatting_spaces(self):
        """Test validation with spaces."""
        self.assertTrue(validate("4532 0151 1283 0366"))
    
    def test_with_formatting_dashes(self):
        """Test validation with dashes."""
        self.assertTrue(validate("4532-0151-1283-0366"))
    
    def test_with_formatting_mixed(self):
        """Test validation with mixed formatting."""
        self.assertTrue(validate("4532-0151 1283.0366"))


class TestCheckDigitCalculation(unittest.TestCase):
    """Test check digit calculation."""
    
    def test_calculate_visa_check_digit(self):
        """Test check digit calculation for Visa."""
        # Visa: 453201511283036 + check digit 6
        self.assertEqual(calculate_check_digit("453201511283036"), 6)
    
    def test_calculate_mastercard_check_digit(self):
        """Test check digit calculation for MasterCard."""
        # MasterCard: 550000000000000 + check digit 4
        self.assertEqual(calculate_check_digit("550000000000000"), 4)
    
    def test_calculate_amex_check_digit(self):
        """Test check digit calculation for Amex."""
        # Amex: 37828224631000 + check digit 5
        self.assertEqual(calculate_check_digit("37828224631000"), 5)
    
    def test_check_digit_zero(self):
        """Test when check digit should be 0."""
        # Number with sum 0 results in check digit 0
        self.assertEqual(calculate_check_digit("000000000000000"), 0)
    
    def test_add_check_digit(self):
        """Test adding check digit to number."""
        result = add_check_digit("453201511283036")
        self.assertEqual(result, "4532015112830366")
        self.assertTrue(validate(result))
    
    def test_invalid_input_raises(self):
        """Test that invalid input raises ValueError."""
        with self.assertRaises(ValueError):
            calculate_check_digit("")


class TestFormatting(unittest.TestCase):
    """Test number formatting functions."""
    
    def test_strip_formatting_spaces(self):
        """Test stripping spaces."""
        self.assertEqual(strip_formatting("4532 0151 1283 0366"), "4532015112830366")
    
    def test_strip_formatting_dashes(self):
        """Test stripping dashes."""
        self.assertEqual(strip_formatting("4532-0151-1283-0366"), "4532015112830366")
    
    def test_strip_formatting_dots(self):
        """Test stripping dots."""
        self.assertEqual(strip_formatting("4532.0151.1283.0366"), "4532015112830366")
    
    def test_strip_formatting_mixed(self):
        """Test stripping mixed characters."""
        self.assertEqual(strip_formatting("4532-0151 1283.0366"), "4532015112830366")
    
    def test_format_default(self):
        """Test default formatting."""
        self.assertEqual(format_number("4532015112830366"), "4532 0151 1283 0366")
    
    def test_format_custom_separator(self):
        """Test formatting with custom separator."""
        self.assertEqual(format_number("4532015112830366", separator="-"), "4532-0151-1283-0366")
    
    def test_format_custom_group_size(self):
        """Test formatting with custom group size."""
        self.assertEqual(format_number("4532015112830366", group_size=2), "45 32 01 51 12 83 03 66")
    
    def test_format_already_formatted(self):
        """Test formatting already formatted number."""
        self.assertEqual(format_number("4532-0151-1283-0366"), "4532 0151 1283 0366")
    
    def test_strip_empty(self):
        """Test stripping empty string."""
        self.assertEqual(strip_formatting(""), "")
    
    def test_format_empty(self):
        """Test formatting empty string."""
        self.assertEqual(format_number(""), "")


class TestNumberGeneration(unittest.TestCase):
    """Test number generation functions."""
    
    def test_generate_visa_number(self):
        """Test generating valid Visa-like number."""
        number = generate_valid_number("4", 16)
        self.assertEqual(len(number), 16)
        self.assertTrue(number.startswith("4"))
        self.assertTrue(validate(number))
    
    def test_generate_mastercard_number(self):
        """Test generating valid MasterCard-like number."""
        number = generate_valid_number("55", 16)
        self.assertEqual(len(number), 16)
        self.assertTrue(number.startswith("55"))
        self.assertTrue(validate(number))
    
    def test_generate_amex_number(self):
        """Test generating valid Amex-like number."""
        number = generate_valid_number("34", 15)
        self.assertEqual(len(number), 15)
        self.assertTrue(number.startswith("34"))
        self.assertTrue(validate(number))
    
    def test_generate_multiple_unique(self):
        """Test that generated numbers are unique."""
        numbers = [generate_valid_number("4", 16) for _ in range(100)]
        unique_numbers = set(numbers)
        # Most should be unique (random generation)
        self.assertGreater(len(unique_numbers), 90)
    
    def test_generate_invalid_length_raises(self):
        """Test that generating with invalid length raises error."""
        with self.assertRaises(ValueError):
            generate_valid_number("4", 1)  # Length <= prefix length
    
    def test_generate_empty_prefix_raises(self):
        """Test that empty prefix raises error."""
        with self.assertRaises(ValueError):
            generate_valid_number("", 16)
    
    def test_generate_test_credit_cards(self):
        """Test generating test credit cards."""
        cards = generate_test_credit_cards(2)
        self.assertGreater(len(cards), 0)
        
        for card_type, number in cards:
            self.assertTrue(validate(number), f"Invalid card: {card_type} {number}")
    
    def test_generate_test_cards_valid_length(self):
        """Test that generated cards have correct lengths."""
        cards = generate_test_credit_cards(2)
        
        for card_type, number in cards:
            if card_type == "American Express":
                self.assertEqual(len(number), 15)
            elif card_type == "Diners Club":
                self.assertEqual(len(number), 14)
            else:
                self.assertEqual(len(number), 16)


class TestErrorDetection(unittest.TestCase):
    """Test error detection functions."""
    
    def test_find_errors_valid_number(self):
        """Test that valid number has no error positions."""
        errors = find_check_digit_errors("4532015112830366")
        self.assertEqual(errors, [])
    
    def test_find_errors_invalid_number(self):
        """Test finding errors in invalid number."""
        # Take a valid number and change one digit
        errors = find_check_digit_errors("4532015112830367")  # Changed last digit
        self.assertGreater(len(errors), 0)
    
    def test_find_errors_empty(self):
        """Test finding errors in empty string."""
        errors = find_check_digit_errors("")
        self.assertEqual(errors, [])


class TestLuhnSum(unittest.TestCase):
    """Test Luhn sum calculation."""
    
    def test_valid_sum(self):
        """Test sum calculation for valid number."""
        total, valid = calculate_luhn_sum("4532015112830366")
        self.assertEqual(total % 10, 0)
        self.assertTrue(valid)
    
    def test_invalid_sum(self):
        """Test sum calculation for invalid number."""
        total, valid = calculate_luhn_sum("4532015112830367")
        self.assertNotEqual(total % 10, 0)
        self.assertFalse(valid)
    
    def test_sum_empty(self):
        """Test sum calculation for empty string."""
        total, valid = calculate_luhn_sum("")
        self.assertEqual(total, 0)
        self.assertFalse(valid)


class TestDigitTransformations(unittest.TestCase):
    """Test digit transformation calculations."""
    
    def test_transformation_valid_input(self):
        """Test transformation with valid input."""
        transformations = get_luhn_digit_transformations(5, 0, 16)
        self.assertIsInstance(transformations, list)
        # All transformations should be valid digits
        for t in transformations:
            self.assertGreaterEqual(t, 0)
            self.assertLessEqual(t, 9)
    
    def test_transformation_invalid_digit(self):
        """Test transformation with invalid digit."""
        with self.assertRaises(ValueError):
            get_luhn_digit_transformations(10, 0, 16)
    
    def test_transformation_negative_digit(self):
        """Test transformation with negative digit."""
        with self.assertRaises(ValueError):
            get_luhn_digit_transformations(-1, 0, 16)


class TestLuhnValidator(unittest.TestCase):
    """Test LuhnValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = LuhnValidator()
    
    def test_validate(self):
        """Test class validate method."""
        self.assertTrue(self.validator.validate("4532015112830366"))
        self.assertFalse(self.validator.validate("4532015112830367"))
    
    def test_calculate_check_digit(self):
        """Test class check digit calculation."""
        self.assertEqual(self.validator.calculate_check_digit("453201511283036"), 6)
    
    def test_add_check_digit(self):
        """Test class add check digit method."""
        result = self.validator.add_check_digit("453201511283036")
        self.assertEqual(result, "4532015112830366")
    
    def test_format(self):
        """Test class format method."""
        self.assertEqual(self.validator.format("4532015112830366"), "4532 0151 1283 0366")
    
    def test_strip(self):
        """Test class strip method."""
        self.assertEqual(self.validator.strip("4532-0151-1283-0366"), "4532015112830366")
    
    def test_generate(self):
        """Test class generate method."""
        number = self.validator.generate("4", 16)
        self.assertEqual(len(number), 16)
        self.assertTrue(validate(number))
    
    def test_generate_batch(self):
        """Test class batch generation."""
        numbers = self.validator.generate_batch("4", 10, 16)
        self.assertEqual(len(numbers), 10)
        for number in numbers:
            self.assertTrue(validate(number))
    
    def test_custom_formatting(self):
        """Test validator with custom formatting."""
        validator = LuhnValidator(group_size=2, separator="-")
        formatted = validator.format("4532015112830366")
        self.assertEqual(formatted, "45-32-01-51-12-83-03-66")


class TestCardTypeIdentification(unittest.TestCase):
    """Test card type identification."""
    
    def test_identify_visa(self):
        """Test Visa identification."""
        self.assertEqual(identify_card_type("4111111111111111"), "visa")
    
    def test_identify_mastercard(self):
        """Test MasterCard identification."""
        self.assertEqual(identify_card_type("5500000000000004"), "mastercard")
    
    def test_identify_amex(self):
        """Test Amex identification."""
        self.assertEqual(identify_card_type("378282246310005"), "amex")
    
    def test_identify_discover(self):
        """Test Discover identification."""
        self.assertEqual(identify_card_type("6011111111111117"), "discover")
    
    def test_identify_jcb(self):
        """Test JCB identification."""
        self.assertEqual(identify_card_type("3530111333300000"), "jcb")
    
    def test_identify_unknown(self):
        """Test unknown card type."""
        self.assertIsNone(identify_card_type("9999999999999999"))
    
    def test_identify_empty(self):
        """Test empty card number."""
        self.assertIsNone(identify_card_type(""))
    
    def test_identify_with_formatting(self):
        """Test identification with formatting."""
        self.assertEqual(identify_card_type("4111-1111-1111-1111"), "visa")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_single_digit_number(self):
        """Test handling of single digit number."""
        self.assertFalse(validate("5"))
    
    def test_two_digit_valid(self):
        """Test minimum valid number (2 digits)."""
        # 00 passes Luhn
        self.assertTrue(validate("00"))
    
    def test_all_same_digits(self):
        """Test number with all same digits."""
        # 1111111111111117 is valid
        self.assertTrue(validate("1111111111111117"))
    
    def test_long_number(self):
        """Test very long number."""
        long_number = "4" + "0" * 100 + "4"  # 102 digit number ending with valid check
        # Just check it doesn't crash
        strip_formatting(long_number)
    
    def test_non_numeric_characters(self):
        """Test number with only non-numeric characters."""
        self.assertEqual(strip_formatting("----  ..."), "")
        self.assertFalse(validate("----"))
    
    def test_unicode_digits(self):
        """Test handling of unicode digit characters."""
        # Unicode full-width digits should be handled
        result = strip_formatting("４５３２０１５１１２８３０３６６")
        # These are full-width digits, they should be stripped or handled
        self.assertIsInstance(result, str)


class TestKnownValidNumbers(unittest.TestCase):
    """Test with known valid test card numbers."""
    
    def test_known_visa_numbers(self):
        """Test known valid Visa test numbers."""
        visa_numbers = [
            "4111111111111111",
            "4012888888881881",
            "4222222222222",
        ]
        for number in visa_numbers:
            self.assertTrue(validate(number), f"Visa number {number} should be valid")
    
    def test_known_mastercard_numbers(self):
        """Test known valid MasterCard test numbers."""
        mc_numbers = [
            "5555555555554444",
            "5105105105105100",
            "2221000000000009",
        ]
        for number in mc_numbers:
            self.assertTrue(validate(number), f"MC number {number} should be valid")
    
    def test_known_amex_numbers(self):
        """Test known valid Amex test numbers."""
        amex_numbers = [
            "378282246310005",
            "371449635398431",
        ]
        for number in amex_numbers:
            self.assertTrue(validate(number), f"Amex number {number} should be valid")
    
    def test_known_discover_numbers(self):
        """Test known valid Discover test numbers."""
        discover_numbers = [
            "6011111111111117",
            "6011000990139424",
        ]
        for number in discover_numbers:
            self.assertTrue(validate(number), f"Discover number {number} should be valid")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)