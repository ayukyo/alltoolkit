"""
Unit tests for IMEI Utilities

Tests cover:
- Validation using Luhn algorithm
- Parsing IMEI structure
- Check digit calculation
- Formatting
- Random generation
- Extraction from text

Note: IMEI test values have been verified to have correct check digits.
Example: 490154203237518 is a valid IMEI (Luhn verified).
"""

import unittest
import sys
import os
sys.path.insert(0, '..')
from mod import (
    validate, parse, format_imei, generate_random, generate_batch,
    calculate_check_digit, luhn_checksum, get_tac_info, compare_imei,
    extract_digits, IMEIValidator
)


# Verified valid IMEI: 490154203237518
# Let's generate a few valid IMEIs for testing
def make_valid_imei(tac, snr):
    """Helper to create a valid IMEI with correct check digit."""
    imei14 = tac + snr
    cd = calculate_check_digit(imei14)
    return imei14 + str(cd)


# Test IMEIs (verified correct)
VALID_IMEI_1 = "490154203237518"  # Verified correct
VALID_IMEI_2 = make_valid_imei("35209900", "176148")  # Will generate correct check digit


class TestLuhnChecksum(unittest.TestCase):
    """Tests for Luhn checksum calculation."""
    
    def test_known_checksum(self):
        """Test checksum for known IMEI body."""
        # IMEI body: 49015420323751, check digit is 8
        checksum = luhn_checksum("49015420323751")
        self.assertEqual(checksum, 2)  # (10 - 8) % 10 = 2, so checksum = 2
    
    def test_verify_check_digit(self):
        """Verify that checksum calculation produces correct check digit."""
        cd = calculate_check_digit("49015420323751")
        self.assertEqual(cd, 8)


class TestCheckDigitCalculation(unittest.TestCase):
    """Tests for check digit calculation."""
    
    def test_calculate_known_check_digit(self):
        """Test calculation for verified IMEI."""
        cd = calculate_check_digit("49015420323751")
        self.assertEqual(cd, 8)
    
    def test_calculate_generates_valid_imei(self):
        """Test that calculated check digit produces valid IMEI."""
        imei14 = "35209900176148"
        cd = calculate_check_digit(imei14)
        full_imei = imei14 + str(cd)
        self.assertTrue(validate(full_imei))
    
    def test_invalid_length(self):
        """Test that invalid length raises error."""
        with self.assertRaises(ValueError):
            calculate_check_digit("12345")
    
    def test_non_digits(self):
        """Test that non-digits raise error."""
        with self.assertRaises(ValueError):
            calculate_check_digit("35209900abcdef")


class TestValidation(unittest.TestCase):
    """Tests for IMEI validation."""
    
    def test_valid_imei(self):
        """Test validation of verified valid IMEI."""
        self.assertTrue(validate(VALID_IMEI_1))
    
    def test_valid_imei_generated(self):
        """Test validation of generated valid IMEI."""
        self.assertTrue(validate(VALID_IMEI_2))
    
    def test_valid_imei_with_separators(self):
        """Test validation with different separators."""
        self.assertTrue(validate("49-015420-323751-8"))
        self.assertTrue(validate("49 015420 323751 8"))
    
    def test_invalid_check_digit(self):
        """Test that wrong check digit fails."""
        # Take valid IMEI and change check digit
        invalid_imei = VALID_IMEI_1[:14] + "9"  # Wrong check digit
        self.assertFalse(validate(invalid_imei))
    
    def test_wrong_length(self):
        """Test that wrong length fails."""
        self.assertFalse(validate("49015420323751"))  # 14 digits
        self.assertFalse(validate("4901542032375180"))  # 16 digits
    
    def test_empty_string(self):
        """Test empty string."""
        self.assertFalse(validate(""))
    
    def test_random_generated_valid(self):
        """Test that random generated IMEIs are valid."""
        for _ in range(10):
            imei = generate_random()
            self.assertTrue(validate(imei))


class TestParse(unittest.TestCase):
    """Tests for IMEI parsing."""
    
    def test_parse_valid_imei(self):
        """Test parsing valid IMEI."""
        result = parse(VALID_IMEI_1)
        self.assertEqual(result['tac'], "49015420")
        self.assertEqual(result['snr'], "323751")
        self.assertEqual(result['cd'], "8")
        self.assertTrue(result['valid'])
    
    def test_parse_with_separators(self):
        """Test parsing with separators."""
        result = parse("49-015420-323751-8")
        self.assertEqual(result['tac'], "49015420")
        self.assertEqual(result['cd'], "8")
    
    def test_parse_invalid_length(self):
        """Test that wrong length raises error."""
        with self.assertRaises(ValueError):
            parse("49015420323751")
    
    def test_parse_invalid_chars(self):
        """Test that invalid characters raise error."""
        with self.assertRaises(ValueError):
            parse("49015420abcdefg")


class TestFormat(unittest.TestCase):
    """Tests for IMEI formatting."""
    
    def test_format_standard(self):
        """Test standard format."""
        result = format_imei(VALID_IMEI_1, "standard")
        self.assertEqual(result, "49-015420-323751-8")
    
    def test_format_compact(self):
        """Test compact format."""
        result = format_imei(VALID_IMEI_1, "compact")
        self.assertEqual(result, VALID_IMEI_1)
    
    def test_format_dashed(self):
        """Test dashed format (same as standard)."""
        result = format_imei(VALID_IMEI_1, "dashed")
        self.assertEqual(result, "49-015420-323751-8")
    
    def test_format_spaced(self):
        """Test spaced format."""
        result = format_imei(VALID_IMEI_1, "spaced")
        self.assertEqual(result, "49 015420 323751 8")
    
    def test_format_with_input_separators(self):
        """Test formatting input with separators."""
        result = format_imei("49-015420-323751-8", "compact")
        self.assertEqual(result, VALID_IMEI_1)
    
    def test_format_invalid_length(self):
        """Test that wrong length raises error."""
        with self.assertRaises(ValueError):
            format_imei("49015420323751", "standard")
    
    def test_format_invalid_style(self):
        """Test that invalid style raises error."""
        with self.assertRaises(ValueError):
            format_imei(VALID_IMEI_1, "invalid")


class TestGenerate(unittest.TestCase):
    """Tests for IMEI generation."""
    
    def test_generate_random_valid(self):
        """Test that random IMEI is valid."""
        imei = generate_random()
        self.assertEqual(len(imei), 15)
        self.assertTrue(validate(imei))
    
    def test_generate_with_tac(self):
        """Test generation with specific TAC."""
        imei = generate_random("35209900")
        self.assertTrue(imei.startswith("35209900"))
        self.assertTrue(validate(imei))
    
    def test_generate_invalid_tac(self):
        """Test that invalid TAC raises error."""
        with self.assertRaises(ValueError):
            generate_random("3520990")  # 7 digits
    
    def test_generate_batch(self):
        """Test batch generation."""
        imeis = generate_batch(10)
        self.assertEqual(len(imeis), 10)
        for imei in imeis:
            self.assertTrue(validate(imei))
    
    def test_generate_batch_unique(self):
        """Test that batch generates unique IMEIs."""
        imeis = generate_batch(100)
        self.assertEqual(len(set(imeis)), 100)
    
    def test_generate_batch_with_tac(self):
        """Test batch generation with specific TAC."""
        imeis = generate_batch(5, "35209900")
        for imei in imeis:
            self.assertTrue(imei.startswith("35209900"))
            self.assertTrue(validate(imei))


class TestTACInfo(unittest.TestCase):
    """Tests for TAC information lookup."""
    
    def test_get_tac_info(self):
        """Test TAC info extraction."""
        info = get_tac_info("49015420")
        self.assertEqual(info['tac'], "49015420")
        self.assertEqual(info['reporting_body_identifier'], "49")
    
    def test_gsm_tac(self):
        """Test GSM TAC classification."""
        info = get_tac_info("35123456")
        self.assertEqual(info['type'], 'gsm_standard')
    
    def test_invalid_tac(self):
        """Test that invalid TAC raises error."""
        with self.assertRaises(ValueError):
            get_tac_info("3520990")


class TestCompare(unittest.TestCase):
    """Tests for IMEI comparison."""
    
    def test_compare_same_imei(self):
        """Test comparing same IMEI."""
        result = compare_imei(VALID_IMEI_1, VALID_IMEI_1)
        self.assertTrue(result['match'])
        self.assertTrue(result['same_tac'])
        self.assertTrue(result['same_snr'])
        self.assertTrue(result['valid1'])
        self.assertTrue(result['valid2'])
    
    def test_compare_different_check_digit(self):
        """Test comparing with different check digit."""
        invalid_imei = VALID_IMEI_1[:14] + "9"
        result = compare_imei(VALID_IMEI_1, invalid_imei)
        self.assertFalse(result['match'])
        self.assertTrue(result['same_tac'])
        self.assertTrue(result['same_snr'])
        self.assertTrue(result['valid1'])
        self.assertFalse(result['valid2'])
    
    def test_compare_different_tac(self):
        """Test comparing with different TAC."""
        imei2 = generate_random("12345678")  # Different TAC
        result = compare_imei(VALID_IMEI_1, imei2)
        self.assertFalse(result['match'])
        self.assertFalse(result['same_tac'])
    
    def test_compare_invalid_length(self):
        """Test comparing with invalid length."""
        result = compare_imei("49015420323751", VALID_IMEI_1)
        self.assertFalse(result['match'])
        self.assertIn('error', result)


class TestExtract(unittest.TestCase):
    """Tests for IMEI extraction from text."""
    
    def test_extract_single(self):
        """Test extracting single IMEI."""
        text = f"Device IMEI: {VALID_IMEI_1}"
        imeis = extract_digits(text)
        self.assertEqual(len(imeis), 1)
        self.assertEqual(imeis[0], VALID_IMEI_1)
    
    def test_extract_multiple(self):
        """Test extracting multiple IMEIs."""
        imei2 = generate_random("12345678")
        text = f"IMEI1: {VALID_IMEI_1}, IMEI2: {imei2}"
        imeis = extract_digits(text)
        self.assertEqual(len(imeis), 2)
    
    def test_extract_invalid_check_digit(self):
        """Test that invalid check digits are filtered out."""
        invalid = VALID_IMEI_1[:14] + "0"  # Wrong check digit
        text = f"IMEI: {invalid}"
        imeis = extract_digits(text)
        self.assertEqual(len(imeis), 0)
    
    def test_extract_no_imei(self):
        """Test text with no IMEI."""
        text = "This is just text with numbers 12345"
        imeis = extract_digits(text)
        self.assertEqual(len(imeis), 0)


class TestIMEIValidator(unittest.TestCase):
    """Tests for IMEIValidator class."""
    
    def test_validator_valid(self):
        """Test validator with valid IMEI."""
        validator = IMEIValidator(VALID_IMEI_1)
        self.assertTrue(validator.is_valid)
        self.assertEqual(validator.tac, "49015420")
        self.assertEqual(validator.snr, "323751")
        self.assertEqual(validator.check_digit, "8")
    
    def test_validator_with_separators(self):
        """Test validator with separators."""
        validator = IMEIValidator("49-015420-323751-8")
        self.assertTrue(validator.is_valid)
        self.assertEqual(str(validator), VALID_IMEI_1)
    
    def test_validator_invalid(self):
        """Test validator with invalid IMEI."""
        invalid = VALID_IMEI_1[:14] + "0"
        validator = IMEIValidator(invalid)
        self.assertFalse(validator.is_valid)
    
    def test_validator_format(self):
        """Test validator format method."""
        validator = IMEIValidator(VALID_IMEI_1)
        self.assertEqual(validator.format("standard"), "49-015420-323751-8")
        self.assertEqual(validator.format("compact"), VALID_IMEI_1)
    
    def test_validator_format_invalid(self):
        """Test format raises error for invalid IMEI."""
        validator = IMEIValidator("invalid")
        with self.assertRaises(ValueError):
            validator.format("standard")
    
    def test_validator_repr(self):
        """Test string representation."""
        validator = IMEIValidator(VALID_IMEI_1)
        repr_str = repr(validator)
        self.assertIn("valid", repr_str)
    
    def test_validator_properties_invalid(self):
        """Test properties return None for invalid IMEI."""
        validator = IMEIValidator("invalid")
        self.assertIsNone(validator.tac)
        self.assertIsNone(validator.snr)
        self.assertIsNone(validator.check_digit)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_all_zeros_tac(self):
        """Test IMEI with zero TAC."""
        imei = generate_random("00000000")
        self.assertTrue(imei.startswith("00000000"))
        self.assertTrue(validate(imei))
    
    def test_all_nines_tac(self):
        """Test IMEI with all nines TAC."""
        imei = generate_random("99999999")
        self.assertTrue(imei.startswith("99999999"))
        self.assertTrue(validate(imei))
    
    def test_check_digit_zero(self):
        """Test IMEI where check digit is 0."""
        # Generate until we find one with check digit 0
        for _ in range(1000):
            imei = generate_random()
            if imei[-1] == '0':
                self.assertTrue(validate(imei))
                return
        # If we didn't find one, generate manually
        # Try different SNR combinations
        for i in range(100):
            snr = str(i).zfill(6)
            imei14 = "00000000" + snr
            cd = calculate_check_digit(imei14)
            if cd == 0:
                self.assertTrue(validate(imei14 + "0"))
                return
    
    def test_very_long_imei_body(self):
        """Test that 14-digit body is required."""
        with self.assertRaises(ValueError):
            calculate_check_digit("12345678901234567")


if __name__ == "__main__":
    unittest.main(verbosity=2)