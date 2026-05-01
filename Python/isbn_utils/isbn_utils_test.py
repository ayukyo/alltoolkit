#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - ISBN Utilities Test Suite
======================================
Comprehensive tests for the ISBN utilities module.

Run with: python -m pytest isbn_utils_test.py -v
Or: python isbn_utils_test.py
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    clean_isbn,
    is_isbn10,
    is_isbn13,
    is_valid_isbn,
    get_isbn_type,
    calculate_isbn10_check_digit,
    calculate_isbn13_check_digit,
    isbn10_to_isbn13,
    isbn13_to_isbn10,
    convert_isbn,
    format_isbn,
    format_isbn_compact,
    parse_isbn,
    generate_isbn10,
    generate_isbn13,
    generate_isbn,
    validate_isbns,
    find_isbns_in_text,
    compare_isbns,
    get_isbn_variants,
)


class TestCleanISBN(unittest.TestCase):
    """Tests for clean_isbn function."""
    
    def test_clean_with_hyphens(self):
        self.assertEqual(clean_isbn("978-0-306-40615-7"), "9780306406157")
        self.assertEqual(clean_isbn("0-306-40615-2"), "0306406152")
    
    def test_clean_with_spaces(self):
        self.assertEqual(clean_isbn("978 0 306 40615 7"), "9780306406157")
        self.assertEqual(clean_isbn("ISBN 0-306-40615-2"), "0306406152")
    
    def test_clean_with_x(self):
        self.assertEqual(clean_isbn("0-306-40615-x"), "030640615X")
        self.assertEqual(clean_isbn("0-306-40615-X"), "030640615X")
    
    def test_clean_empty(self):
        self.assertEqual(clean_isbn(""), "")
    
    def test_clean_already_clean(self):
        self.assertEqual(clean_isbn("9780306406157"), "9780306406157")


class TestISBN10Validation(unittest.TestCase):
    """Tests for ISBN-10 validation."""
    
    def test_valid_isbn10_simple(self):
        self.assertTrue(is_isbn10("0306406152"))
        self.assertTrue(is_isbn10("0471958697"))
        self.assertTrue(is_isbn10("0596007973"))  # Correct check digit
    
    def test_valid_isbn10_with_x(self):
        self.assertTrue(is_isbn10("080442957X"))  # Valid ISBN-10 with X check digit
        self.assertTrue(is_isbn10("156881111X"))  # Another valid X check digit
    
    def test_valid_isbn10_with_hyphens(self):
        self.assertTrue(is_isbn10("0-306-40615-2"))
        self.assertTrue(is_isbn10("0-471-95869-7"))
    
    def test_invalid_isbn10_wrong_length(self):
        self.assertFalse(is_isbn10("030640615"))  # Too short
        self.assertFalse(is_isbn10("03064061522"))  # Too long
    
    def test_invalid_isbn10_wrong_check_digit(self):
        self.assertFalse(is_isbn10("0306406153"))  # Wrong check digit
    
    def test_invalid_isbn10_x_in_wrong_position(self):
        self.assertFalse(is_isbn10("X306406152"))  # X at start
    
    def test_isbn13_not_isbn10(self):
        self.assertFalse(is_isbn10("9780306406157"))


class TestISBN13Validation(unittest.TestCase):
    """Tests for ISBN-13 validation."""
    
    def test_valid_isbn13_simple(self):
        self.assertTrue(is_isbn13("9780306406157"))
        self.assertTrue(is_isbn13("9780471958697"))
        self.assertTrue(is_isbn13("9780596007973"))  # Correct check digit
    
    def test_valid_isbn13_with_hyphens(self):
        self.assertTrue(is_isbn13("978-0-306-40615-7"))
        self.assertTrue(is_isbn13("978-0-471-95869-7"))
    
    def test_valid_isbn13_979_prefix(self):
        self.assertTrue(is_isbn13("9790306406156"))  # 979 prefix with correct check digit
    
    def test_invalid_isbn13_wrong_length(self):
        self.assertFalse(is_isbn13("978030640615"))  # Too short
        self.assertFalse(is_isbn13("97803064061577"))  # Too long
    
    def test_invalid_isbn13_wrong_check_digit(self):
        self.assertFalse(is_isbn13("9780306406158"))  # Wrong check digit
    
    def test_invalid_isbn13_wrong_prefix(self):
        self.assertFalse(is_isbn13("9770306406157"))  # Invalid prefix
    
    def test_isbn10_not_isbn13(self):
        self.assertFalse(is_isbn13("0306406152"))


class TestGeneralValidation(unittest.TestCase):
    """Tests for general ISBN validation."""
    
    def test_valid_isbn_accepts_both(self):
        self.assertTrue(is_valid_isbn("0306406152"))
        self.assertTrue(is_valid_isbn("9780306406157"))
    
    def test_invalid_isbn_rejected(self):
        self.assertFalse(is_valid_isbn("invalid"))
        self.assertFalse(is_valid_isbn("123456789"))
        self.assertFalse(is_valid_isbn(""))
    
    def test_get_isbn_type(self):
        self.assertEqual(get_isbn_type("0306406152"), "ISBN-10")
        self.assertEqual(get_isbn_type("9780306406157"), "ISBN-13")
        self.assertIsNone(get_isbn_type("invalid"))


class TestCheckDigits(unittest.TestCase):
    """Tests for check digit calculation."""
    
    def test_calculate_isbn10_check_digit(self):
        self.assertEqual(calculate_isbn10_check_digit("030640615"), "2")
        self.assertEqual(calculate_isbn10_check_digit("047195869"), "7")
    
    def test_calculate_isbn10_check_digit_x(self):
        # ISBN ending in X
        self.assertEqual(calculate_isbn10_check_digit("080442957"), "X")
    
    def test_calculate_isbn10_check_digit_invalid(self):
        with self.assertRaises(ValueError):
            calculate_isbn10_check_digit("03064061")  # Too short
    
    def test_calculate_isbn13_check_digit(self):
        self.assertEqual(calculate_isbn13_check_digit("978030640615"), "7")
        self.assertEqual(calculate_isbn13_check_digit("978047195869"), "7")
    
    def test_calculate_isbn13_check_digit_invalid(self):
        with self.assertRaises(ValueError):
            calculate_isbn13_check_digit("97803064061")  # Too short


class TestConversion(unittest.TestCase):
    """Tests for ISBN conversion functions."""
    
    def test_isbn10_to_isbn13(self):
        self.assertEqual(isbn10_to_isbn13("0306406152"), "9780306406157")
        self.assertEqual(isbn10_to_isbn13("0471958697"), "9780471958697")
    
    def test_isbn10_to_isbn13_with_hyphens(self):
        self.assertEqual(isbn10_to_isbn13("0-306-40615-2"), "9780306406157")
    
    def test_isbn10_to_isbn13_invalid(self):
        with self.assertRaises(ValueError):
            isbn10_to_isbn13("invalid")
    
    def test_isbn13_to_isbn10(self):
        self.assertEqual(isbn13_to_isbn10("9780306406157"), "0306406152")
        self.assertEqual(isbn13_to_isbn10("9780471958697"), "0471958697")
    
    def test_isbn13_to_isbn10_979_prefix(self):
        # 979 prefix ISBN-13 cannot be converted to ISBN-10
        self.assertIsNone(isbn13_to_isbn10("9790306406156"))  # Valid 979 ISBN
    
    def test_isbn13_to_isbn10_invalid(self):
        with self.assertRaises(ValueError):
            isbn13_to_isbn10("invalid")
    
    def test_convert_isbn(self):
        self.assertEqual(convert_isbn("0306406152", "ISBN-13"), "9780306406157")
        self.assertEqual(convert_isbn("9780306406157", "ISBN-10"), "0306406152")
        self.assertEqual(convert_isbn("0306406152", "ISBN-10"), "0306406152")
    
    def test_convert_isbn_invalid(self):
        self.assertIsNone(convert_isbn("invalid", "ISBN-13"))


class TestFormatting(unittest.TestCase):
    """Tests for ISBN formatting."""
    
    def test_format_isbn10(self):
        formatted = format_isbn("0306406152")
        self.assertIn("0", formatted)
        self.assertIn("306", formatted)
        self.assertIn("40615", formatted)
        self.assertIn("2", formatted)
    
    def test_format_isbn13(self):
        formatted = format_isbn("9780306406157")
        self.assertIn("978", formatted)
        self.assertIn("7", formatted)  # Check digit
    
    def test_format_isbn_custom_separator(self):
        formatted = format_isbn("9780306406157", separator=" ")
        self.assertIn(" ", formatted)
    
    def test_format_isbn_invalid(self):
        with self.assertRaises(ValueError):
            format_isbn("invalid")
    
    def test_format_isbn_compact(self):
        self.assertEqual(format_isbn_compact("978-0-306-40615-7"), "9780306406157")
        self.assertEqual(format_isbn_compact("0-306-40615-2"), "0306406152")


class TestParsing(unittest.TestCase):
    """Tests for ISBN parsing."""
    
    def test_parse_isbn10(self):
        result = parse_isbn("0306406152")
        self.assertTrue(result['valid'])
        self.assertEqual(result['type'], 'ISBN-10')
        self.assertEqual(result['clean'], '0306406152')
        self.assertEqual(result['isbn13'], '9780306406157')
        self.assertEqual(result['check_digit'], '2')
    
    def test_parse_isbn13(self):
        result = parse_isbn("9780306406157")
        self.assertTrue(result['valid'])
        self.assertEqual(result['type'], 'ISBN-13')
        self.assertEqual(result['clean'], '9780306406157')
        self.assertEqual(result['prefix'], '978')
        self.assertEqual(result['isbn10'], '0306406152')
        self.assertEqual(result['check_digit'], '7')
    
    def test_parse_invalid(self):
        result = parse_isbn("invalid")
        self.assertFalse(result['valid'])
        self.assertIsNone(result['type'])
    
    def test_parse_with_group_name(self):
        result = parse_isbn("0306406152")
        self.assertEqual(result['group'], '0')
        self.assertEqual(result['group_name'], 'English')


class TestGeneration(unittest.TestCase):
    """Tests for ISBN generation."""
    
    def test_generate_isbn10(self):
        isbn = generate_isbn10()
        self.assertTrue(is_isbn10(isbn))
        self.assertEqual(len(isbn), 10)
    
    def test_generate_isbn13(self):
        isbn = generate_isbn13()
        self.assertTrue(is_isbn13(isbn))
        self.assertEqual(len(isbn), 13)
    
    def test_generate_isbn13_979_prefix(self):
        isbn = generate_isbn13(prefix="979")
        self.assertTrue(isbn.startswith("979"))
        self.assertTrue(is_isbn13(isbn))
    
    def test_generate_isbn_with_group(self):
        isbn = generate_isbn10(group="7")  # Chinese group
        self.assertTrue(isbn.startswith("7"))
        self.assertTrue(is_isbn10(isbn))
    
    def test_generate_isbn_type_selection(self):
        isbn10 = generate_isbn("ISBN-10")
        isbn13 = generate_isbn("ISBN-13")
        self.assertTrue(is_isbn10(isbn10))
        self.assertTrue(is_isbn13(isbn13))
    
    def test_generated_isbns_unique(self):
        isbns = [generate_isbn10() for _ in range(100)]
        # Should generate different ISBNs (highly unlikely to get duplicates)
        unique_count = len(set(isbns))
        self.assertGreater(unique_count, 90)  # Allow some tolerance


class TestBatchFunctions(unittest.TestCase):
    """Tests for batch ISBN operations."""
    
    def test_validate_isbns(self):
        isbns = ["0306406152", "invalid", "9780306406157"]
        results = validate_isbns(isbns)
        
        self.assertEqual(len(results), 3)
        self.assertTrue(results["0306406152"]["valid"])
        self.assertFalse(results["invalid"]["valid"])
        self.assertTrue(results["9780306406157"]["valid"])
    
    def test_find_isbns_in_text(self):
        text = "Check out ISBN 978-0-306-40615-7 and also 0306406152."
        found = find_isbns_in_text(text)
        
        self.assertEqual(len(found), 2)
        self.assertIn("9780306406157", found)
        self.assertIn("0306406152", found)
    
    def test_find_isbns_in_text_no_duplicates(self):
        text = "ISBN 0306406152 and 0306406152 again."
        found = find_isbns_in_text(text)
        
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0], "0306406152")


class TestCompareISBNs(unittest.TestCase):
    """Tests for ISBN comparison."""
    
    def test_compare_same_isbn10(self):
        self.assertTrue(compare_isbns("0306406152", "0306406152"))
    
    def test_compare_same_isbn13(self):
        self.assertTrue(compare_isbns("9780306406157", "9780306406157"))
    
    def test_compare_isbn10_and_isbn13(self):
        self.assertTrue(compare_isbns("0306406152", "9780306406157"))
        self.assertTrue(compare_isbns("9780306406157", "0306406152"))
    
    def test_compare_different_isbns(self):
        self.assertFalse(compare_isbns("0306406152", "0471958697"))
    
    def test_compare_invalid_isbns(self):
        self.assertFalse(compare_isbns("invalid", "0306406152"))
        self.assertFalse(compare_isbns("0306406152", "invalid"))


class TestGetISBNVariants(unittest.TestCase):
    """Tests for get_isbn_variants function."""
    
    def test_get_variants_from_isbn10(self):
        variants = get_isbn_variants("0306406152")
        
        self.assertEqual(variants['isbn10'], "0306406152")
        self.assertEqual(variants['isbn13'], "9780306406157")
        self.assertIsNotNone(variants['formatted10'])
        self.assertIsNotNone(variants['formatted13'])
    
    def test_get_variants_from_isbn13(self):
        variants = get_isbn_variants("9780306406157")
        
        self.assertEqual(variants['isbn10'], "0306406152")
        self.assertEqual(variants['isbn13'], "9780306406157")
    
    def test_get_variants_979_prefix(self):
        variants = get_isbn_variants("9790306406156")  # Valid 979 ISBN
        
        self.assertIsNone(variants['isbn10'])  # Can't convert 979 to ISBN-10
        self.assertEqual(variants['isbn13'], "9790306406156")
    
    def test_get_variants_invalid(self):
        variants = get_isbn_variants("invalid")
        
        self.assertIsNone(variants['isbn10'])
        self.assertIsNone(variants['isbn13'])
        self.assertIsNone(variants['formatted10'])
        self.assertIsNone(variants['formatted13'])


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and special scenarios."""
    
    def test_isbn_with_x_check_digit(self):
        # ISBN-10 with X as check digit
        isbn = "156881111X"
        # Verify it's valid (if it is) or test the handling
        clean = clean_isbn(isbn)
        self.assertEqual(clean[-1], 'X')
    
    def test_chinese_isbn(self):
        # Test Chinese group ISBN
        isbn = generate_isbn10(group="7")
        self.assertTrue(isbn.startswith("7"))
        self.assertTrue(is_isbn10(isbn))
    
    def test_empty_string(self):
        self.assertFalse(is_valid_isbn(""))
    
    def test_none_handling(self):
        # Functions should handle empty string gracefully
        self.assertEqual(clean_isbn(""), "")
    
    def test_isbn_with_only_hyphens(self):
        self.assertEqual(clean_isbn("---"), "")
    
    def test_multiple_isbn_formats(self):
        # Same ISBN in different formats
        formats = [
            "0306406152",
            "0-306-40615-2",
            "ISBN 0-306-40615-2",
            "ISBN0306406152",
        ]
        cleaned = [clean_isbn(f) for f in formats]
        self.assertTrue(all(c == "0306406152" for c in cleaned))


class TestRoundTrip(unittest.TestCase):
    """Tests for ISBN conversion round trips."""
    
    def test_isbn10_to_isbn13_and_back(self):
        original = "0306406152"
        isbn13 = isbn10_to_isbn13(original)
        back_to_10 = isbn13_to_isbn10(isbn13)
        
        self.assertEqual(original, back_to_10)
    
    def test_isbn13_to_isbn10_and_back(self):
        original = "9780306406157"
        isbn10 = isbn13_to_isbn10(original)
        back_to_13 = isbn10_to_isbn13(isbn10)
        
        self.assertEqual(original, back_to_13)


if __name__ == "__main__":
    unittest.main(verbosity=2)