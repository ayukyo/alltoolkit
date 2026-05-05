"""
Test suite for ISIN Utilities

Run with: python isin_utils_test.py
Or: python -m pytest isin_utils_test.py -v
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    is_valid_isin,
    validate_isin,
    parse_isin,
    get_isin_info,
    format_isin,
    generate_isin,
    generate_random_isin,
    extract_isin,
    extract_all_isin,
    compare_isin,
    calculate_check_digit,
    isin_to_cusip,
    cusip_to_isin,
    sedol_to_isin,
    get_example_isin,
    list_example_isins,
    ISINValidationError,
    ISINInfo,
    COUNTRY_CODES,
    EXAMPLE_ISINS,
)


class TestISINValidation(unittest.TestCase):
    """Test ISIN validation."""
    
    def test_valid_isins(self):
        """Test valid ISINs."""
        # Apple Inc.
        self.assertTrue(is_valid_isin("US0378331005"))
        self.assertTrue(is_valid_isin("us0378331005"))  # lowercase
        self.assertTrue(is_valid_isin("US 037833100 5"))  # with spaces
        self.assertTrue(is_valid_isin("US-037833100-5"))  # with dashes
        
        # Microsoft
        self.assertTrue(is_valid_isin("US5949181045"))
        
        # Google (Alphabet)
        self.assertTrue(is_valid_isin("US02079K1079"))
        
        # Tesla
        self.assertTrue(is_valid_isin("US88160R1014"))
        
        # Tencent (Hong Kong)
        self.assertTrue(is_valid_isin("KYG875721634"))
        
        # Samsung (Korea)
        self.assertTrue(is_valid_isin("KR7005930003"))
        
        # Toyota (Japan)
        self.assertTrue(is_valid_isin("JP3633400001"))
    
    def test_invalid_isins(self):
        """Test invalid ISINs."""
        # Wrong check digit
        self.assertFalse(is_valid_isin("US0378331006"))
        
        # Too short
        self.assertFalse(is_valid_isin("US037833100"))
        
        # Too long
        self.assertFalse(is_valid_isin("US0378331005123"))
        
        # Invalid country code (numbers instead of letters)
        self.assertFalse(is_valid_isin("120378331005"))
        
        # Empty
        self.assertFalse(is_valid_isin(""))
        self.assertFalse(is_valid_isin(None))
        
        # Invalid characters
        self.assertFalse(is_valid_isin("US037833100@"))
    
    def test_validate_isin_returns_info(self):
        """Test that validate_isin returns ISINInfo."""
        info = validate_isin("US0378331005")
        
        self.assertTrue(info.is_valid)
        self.assertEqual(info.cleaned, "US0378331005")
        self.assertEqual(info.country_code, "US")
        self.assertEqual(info.nsin, "037833100")
        self.assertEqual(info.check_digit, "5")
        self.assertEqual(info.message, "Valid ISIN")
    
    def test_validate_invalid_isin_returns_info(self):
        """Test that invalid ISIN returns ISINInfo with error."""
        info = validate_isin("US0378331006")  # Wrong check digit
        
        self.assertFalse(info.is_valid)
        self.assertIn("check digit", info.message.lower())


class TestCheckDigitCalculation(unittest.TestCase):
    """Test check digit calculation."""
    
    def test_calculate_check_digit(self):
        """Test check digit calculation."""
        # Apple Inc.
        self.assertEqual(calculate_check_digit("US037833100"), "5")
        
        # Microsoft
        self.assertEqual(calculate_check_digit("US594918104"), "5")
        
        # Google
        self.assertEqual(calculate_check_digit("US02079K107"), "9")
        
        # Tesla
        self.assertEqual(calculate_check_digit("US88160R101"), "4")
    
    def test_calculate_with_12_chars(self):
        """Test calculation with 12-char ISIN (ignores last digit)."""
        self.assertEqual(calculate_check_digit("US0378331005"), "5")
        self.assertEqual(calculate_check_digit("US0378331006"), "5")  # Wrong check ignored
    
    def test_calculate_raises_on_invalid_input(self):
        """Test that calculation raises on invalid input."""
        with self.assertRaises(ISINValidationError):
            calculate_check_digit("SHORT")
        
        with self.assertRaises(ISINValidationError):
            calculate_check_digit("12INVALID12")  # Numbers for country code


class TestISINParsing(unittest.TestCase):
    """Test ISIN parsing."""
    
    def test_parse_isin(self):
        """Test parsing ISIN components."""
        info = parse_isin("US0378331005")
        
        self.assertEqual(info.country_code, "US")
        self.assertEqual(info.nsin, "037833100")
        self.assertEqual(info.check_digit, "5")
    
    def test_get_isin_info(self):
        """Test getting detailed ISIN info."""
        info = get_isin_info("US0378331005")
        
        self.assertEqual(info["country_code"], "US")
        self.assertEqual(info["country_name"], "United States")
        self.assertEqual(info["nsin"], "037833100")
        self.assertEqual(info["check_digit"], "5")
        self.assertTrue(info["is_valid"])
    
    def test_get_isin_info_unknown_country(self):
        """Test getting info for unknown country."""
        info = get_isin_info("XX1234567890")
        
        # This ISIN has invalid format but let's test with valid format
        # Generate a valid ISIN with ZZ code (reserved)
        isin = generate_isin("ZZ", "123456789")
        info = get_isin_info(isin)
        
        self.assertEqual(info["country_name"], "Unknown")


class TestISINFormatting(unittest.TestCase):
    """Test ISIN formatting."""
    
    def test_format_with_space(self):
        """Test formatting with space separator."""
        self.assertEqual(format_isin("US0378331005"), "US 037833100 5")
        self.assertEqual(format_isin("US0378331005", " "), "US 037833100 5")
    
    def test_format_with_dash(self):
        """Test formatting with dash separator."""
        self.assertEqual(format_isin("US0378331005", "-"), "US-037833100-5")
    
    def test_format_with_dot(self):
        """Test formatting with dot separator."""
        self.assertEqual(format_isin("US0378331005", "."), "US.037833100.5")
    
    def test_format_invalid_length(self):
        """Test formatting ISIN with invalid length."""
        self.assertEqual(format_isin("SHORT"), "SHORT")


class TestISINGeneration(unittest.TestCase):
    """Test ISIN generation."""
    
    def test_generate_isin_default(self):
        """Test generating ISIN with defaults."""
        isin = generate_isin()
        
        self.assertEqual(len(isin), 12)
        self.assertTrue(isin.startswith("US"))
        self.assertTrue(is_valid_isin(isin))
    
    def test_generate_isin_with_country(self):
        """Test generating ISIN with specific country."""
        isin = generate_isin("GB")
        
        self.assertTrue(isin.startswith("GB"))
        self.assertTrue(is_valid_isin(isin))
    
    def test_generate_isin_with_nsin(self):
        """Test generating ISIN with specific NSIN."""
        isin = generate_isin("US", "037833100")
        
        self.assertEqual(isin, "US0378331005")
        self.assertTrue(is_valid_isin(isin))
    
    def test_generate_isin_with_seed(self):
        """Test reproducible generation with seed."""
        isin1 = generate_isin(seed=42)
        isin2 = generate_isin(seed=42)
        
        self.assertEqual(isin1, isin2)
    
    def test_generate_isin_invalid_country(self):
        """Test generating ISIN with invalid country."""
        with self.assertRaises(ISINValidationError):
            generate_isin("USA")  # Too long
        
        with self.assertRaises(ISINValidationError):
            generate_isin("12")  # Numbers
    
    def test_generate_random_isin(self):
        """Test generating random ISIN."""
        isin = generate_random_isin()
        
        self.assertEqual(len(isin), 12)
        self.assertTrue(is_valid_isin(isin))
    
    def test_generate_random_isin_reproducible(self):
        """Test reproducible random generation."""
        isin1 = generate_random_isin(seed=123)
        isin2 = generate_random_isin(seed=123)
        
        self.assertEqual(isin1, isin2)


class TestISINExtraction(unittest.TestCase):
    """Test ISIN extraction from text."""
    
    def test_extract_single_isin(self):
        """Test extracting single ISIN from text."""
        text = "Apple's ISIN is US0378331005"
        isin = extract_isin(text)
        
        self.assertEqual(isin, "US0378331005")
    
    def test_extract_multiple_isins(self):
        """Test extracting multiple ISINs from text."""
        text = "Apple: US0378331005, Microsoft: US5949181045, Google: US02079K1079"
        isins = extract_all_isin(text)
        
        self.assertEqual(len(isins), 3)
        self.assertIn("US0378331005", isins)
        self.assertIn("US5949181045", isins)
        self.assertIn("US02079K1079", isins)
    
    def test_extract_no_isin(self):
        """Test extracting when no ISIN present."""
        text = "This text has no ISIN codes."
        isin = extract_isin(text)
        
        self.assertIsNone(isin)
    
    def test_extract_invalid_isin(self):
        """Test that invalid ISINs are not extracted."""
        text = "Fake ISIN: US0378331006"  # Wrong check digit
        isins = extract_all_isin(text)
        
        self.assertEqual(len(isins), 0)
    
    def test_extract_with_formatting(self):
        """Test extracting ISINs with formatting."""
        text = "ISIN: US-037833100-5"
        isin = extract_isin(text)
        
        # Note: The regex won't match with dashes inside
        # This tests that clean ISINs are extracted
        self.assertIsNone(isin)  # Regex won't match with internal dashes


class TestISINComparison(unittest.TestCase):
    """Test ISIN comparison."""
    
    def test_compare_same_isin(self):
        """Test comparing same ISIN."""
        self.assertTrue(compare_isin("US0378331005", "US0378331005"))
    
    def test_compare_with_formatting(self):
        """Test comparing ISINs with different formatting."""
        self.assertTrue(compare_isin("US0378331005", "US 037833100 5"))
        self.assertTrue(compare_isin("US-037833100-5", "US0378331005"))
        self.assertTrue(compare_isin("us0378331005", "US0378331005"))
    
    def test_compare_different_isin(self):
        """Test comparing different ISINs."""
        self.assertFalse(compare_isin("US0378331005", "US5949181045"))


class TestCUSIPConversion(unittest.TestCase):
    """Test CUSIP conversion."""
    
    def test_isin_to_cusip(self):
        """Test converting ISIN to CUSIP."""
        # Apple Inc.
        cusip = isin_to_cusip("US0378331005")
        self.assertEqual(cusip, "037833100")
        
        # Microsoft
        cusip = isin_to_cusip("US5949181045")
        self.assertEqual(cusip, "594918104")
    
    def test_isin_to_cusip_non_us(self):
        """Test converting non-US ISIN to CUSIP returns None."""
        # Samsung (Korea)
        cusip = isin_to_cusip("KR7005930003")
        self.assertIsNone(cusip)
    
    def test_isin_to_cusip_invalid(self):
        """Test converting invalid ISIN to CUSIP."""
        cusip = isin_to_cusip("INVALID")
        self.assertIsNone(cusip)
    
    def test_cusip_to_isin(self):
        """Test converting CUSIP to ISIN."""
        isin = cusip_to_isin("037833100")
        self.assertEqual(isin, "US0378331005")
        
        isin = cusip_to_isin("594918104")
        self.assertEqual(isin, "US5949181045")
    
    def test_cusip_to_isin_with_country(self):
        """Test converting CUSIP to ISIN with country code."""
        isin = cusip_to_isin("037833100", "CA")
        # Check digit is calculated based on country code
        self.assertTrue(is_valid_isin(isin))
        self.assertEqual(isin, "CA0378331007")  # Correct check digit for CA
    
    def test_cusip_to_isin_invalid(self):
        """Test converting invalid CUSIP raises error."""
        with self.assertRaises(ISINValidationError):
            cusip_to_isin("SHORT")


class TestSEDOLConversion(unittest.TestCase):
    """Test SEDOL conversion."""
    
    def test_sedol_to_isin(self):
        """Test converting SEDOL to ISIN."""
        # Note: SEDOL check digit is not validated here
        # We just pad and generate ISIN
        isin = sedol_to_isin("0263494")  # Example SEDOL
        self.assertEqual(len(isin), 12)
        self.assertTrue(isin.startswith("GB"))
    
    def test_sedol_to_isin_invalid(self):
        """Test converting invalid SEDOL raises error."""
        with self.assertRaises(ISINValidationError):
            sedol_to_isin("SHORT")


class TestExamples(unittest.TestCase):
    """Test example ISINs."""
    
    def test_get_example_isin(self):
        """Test getting example ISINs."""
        self.assertEqual(get_example_isin("APPLE"), "US0378331005")
        self.assertEqual(get_example_isin("apple"), "US0378331005")  # case insensitive
        self.assertEqual(get_example_isin("MICROSOFT"), "US5949181045")
        self.assertEqual(get_example_isin("GOOGLE"), "US02079K1079")
        self.assertIsNone(get_example_isin("UNKNOWN"))
    
    def test_list_example_isins(self):
        """Test listing all example ISINs."""
        examples = list_example_isins()
        
        self.assertIsInstance(examples, dict)
        self.assertIn("APPLE", examples)
        self.assertIn("MICROSOFT", examples)
    
    def test_all_examples_are_valid(self):
        """Test that all example ISINs are valid."""
        for name, isin in EXAMPLE_ISINS.items():
            with self.subTest(name=name):
                self.assertTrue(is_valid_isin(isin), 
                    f"Example {name} ISIN {isin} is not valid")


class TestISINInfo(unittest.TestCase):
    """Test ISINInfo class."""
    
    def test_to_dict(self):
        """Test converting ISINInfo to dictionary."""
        info = validate_isin("US0378331005")
        d = info.to_dict()
        
        self.assertIn("original", d)
        self.assertIn("cleaned", d)
        self.assertIn("is_valid", d)
        self.assertIn("country_code", d)
        self.assertIn("nsin", d)
        self.assertIn("check_digit", d)
        self.assertIn("message", d)


class TestCountryCodes(unittest.TestCase):
    """Test country codes."""
    
    def test_country_codes_exist(self):
        """Test that common country codes are defined."""
        self.assertIn("US", COUNTRY_CODES)
        self.assertIn("GB", COUNTRY_CODES)
        self.assertIn("DE", COUNTRY_CODES)
        self.assertIn("JP", COUNTRY_CODES)
        self.assertIn("CN", COUNTRY_CODES)
    
    def test_country_names(self):
        """Test that country codes map to correct names."""
        self.assertEqual(COUNTRY_CODES["US"], "United States")
        self.assertEqual(COUNTRY_CODES["GB"], "United Kingdom")
        self.assertEqual(COUNTRY_CODES["JP"], "Japan")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_isin_with_letter_in_nsin(self):
        """Test ISIN with letters in NSIN (valid)."""
        # Google's ISIN has 'K' in NSIN
        self.assertTrue(is_valid_isin("US02079K1079"))
    
    def test_isin_with_all_letters(self):
        """Test ISIN with many letters (edge case)."""
        # Generate an ISIN with letters in NSIN
        isin = generate_isin("US", "ABCDEFGHI")
        self.assertTrue(is_valid_isin(isin))
    
    def test_empty_string(self):
        """Test handling empty string."""
        self.assertFalse(is_valid_isin(""))
    
    def test_whitespace_only(self):
        """Test handling whitespace only."""
        self.assertFalse(is_valid_isin("   "))


def run_tests():
    """Run all tests."""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()