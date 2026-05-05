#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - ISSN Utilities Module Tests
=========================================
Comprehensive test suite for ISSN validation, conversion, and utilities.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from issn_utils.mod import (
    clean_issn,
    is_issn8,
    is_issn13,
    is_valid_issn,
    get_issn_type,
    calculate_issn_check_digit,
    calculate_issn13_check_digit,
    issn8_to_issn13,
    issn13_to_issn8,
    convert_issn,
    format_issn,
    format_issn_compact,
    is_issn_l,
    format_issn_l,
    extract_issn_l,
    parse_issn,
    generate_issn,
    generate_issn13,
    generate_issn_l,
    validate_issns,
    find_issns_in_text,
    compare_issns,
    get_issn_variants,
    is_print_issn,
    get_check_digit_info,
)

# Real ISSNs with their correct ISSN-13 equivalents
ISSN_NATURE = "0028-0836"
ISSN_NATURE_13 = "9770028083002"
ISSN_CACM = "0001-0782"  # Communications of the ACM
ISSN_CACM_13 = "9770001078001"
ISSN_IEEE = "0018-9448"  # IEEE Transactions on Information Theory
ISSN_IEEE_13 = "9770018944009"
ISSN_X_CHECK = "2434-561X"  # ISSN with X check digit
ISSN_X_CHECK_13 = "9772434561006"


class TestCleanISSN(unittest.TestCase):
    """Test ISSN cleaning functions."""
    
    def test_clean_standard(self):
        self.assertEqual(clean_issn(ISSN_NATURE), "00280836")
    
    def test_clean_with_prefix(self):
        self.assertEqual(clean_issn("ISSN " + ISSN_NATURE), "00280836")
    
    def test_clean_with_x(self):
        self.assertEqual(clean_issn(ISSN_X_CHECK), "2434561X")
        self.assertEqual(clean_issn("2434-561x"), "2434561X")
    
    def test_clean_issn13(self):
        self.assertEqual(clean_issn(ISSN_NATURE_13), "9770028083002")
    
    def test_clean_empty(self):
        self.assertEqual(clean_issn(""), "")
        self.assertEqual(clean_issn(None), "")
    
    def test_clean_spaces(self):
        self.assertEqual(clean_issn("0028 0836"), "00280836")


class TestISSN8Validation(unittest.TestCase):
    """Test ISSN-8 validation."""
    
    def test_valid_standard(self):
        self.assertTrue(is_issn8(ISSN_NATURE))
        self.assertTrue(is_issn8("00280836"))
    
    def test_valid_with_x(self):
        self.assertTrue(is_issn8(ISSN_X_CHECK))
        self.assertTrue(is_issn8("2434561X"))
    
    def test_invalid_length(self):
        self.assertFalse(is_issn8("0028-08"))
        self.assertFalse(is_issn8("0028083612"))
    
    def test_invalid_chars(self):
        self.assertFalse(is_issn8("0028-083A"))
    
    def test_invalid_x_position(self):
        self.assertFalse(is_issn8("002X-0836"))  # X not at end
    
    def test_invalid_check_digit(self):
        self.assertFalse(is_issn8("0028-0837"))  # Wrong check digit
    
    def test_real_world_examples(self):
        # Real ISSNs
        self.assertTrue(is_issn8(ISSN_CACM))  # Communications of the ACM
        self.assertTrue(is_issn8(ISSN_IEEE))  # IEEE Transactions
        self.assertTrue(is_issn8(ISSN_NATURE))  # Nature
        self.assertTrue(is_issn8("0036-8075"))  # Science


class TestISSN13Validation(unittest.TestCase):
    """Test ISSN-13 validation."""
    
    def test_valid_standard(self):
        self.assertTrue(is_issn13(ISSN_NATURE_13))
    
    def test_valid_with_hyphens(self):
        self.assertTrue(is_issn13("977-0028-0830-02"))
    
    def test_invalid_prefix(self):
        self.assertFalse(is_issn13("9780028083002"))  # Wrong prefix (978 is for ISBN)
    
    def test_invalid_length(self):
        self.assertFalse(is_issn13("977002808300"))
        self.assertFalse(is_issn13("97700280830022"))
    
    def test_invalid_check_digit(self):
        self.assertFalse(is_issn13("9770028083003"))
    
    def test_issn8_not_issn13(self):
        self.assertFalse(is_issn13(ISSN_NATURE))


class TestGeneralValidation(unittest.TestCase):
    """Test general ISSN validation."""
    
    def test_valid_issn8(self):
        self.assertTrue(is_valid_issn(ISSN_NATURE))
    
    def test_valid_issn13(self):
        self.assertTrue(is_valid_issn(ISSN_NATURE_13))
    
    def test_invalid(self):
        self.assertFalse(is_valid_issn("invalid"))
        self.assertFalse(is_valid_issn("0028-08"))
    
    def test_get_type(self):
        self.assertEqual(get_issn_type(ISSN_NATURE), "ISSN-8")
        self.assertEqual(get_issn_type(ISSN_NATURE_13), "ISSN-13")
        self.assertIsNone(get_issn_type("invalid"))


class TestCheckDigits(unittest.TestCase):
    """Test check digit calculation."""
    
    def test_calculate_issn8_check_digit(self):
        # Nature: 00280836 -> check digit 6
        self.assertEqual(calculate_issn_check_digit("0028083"), "6")
        # Communications of ACM: 00010782 -> check digit 2
        self.assertEqual(calculate_issn_check_digit("0001078"), "2")
        # X check digit case
        self.assertEqual(calculate_issn_check_digit("2434561"), "X")
    
    def test_calculate_issn13_check_digit(self):
        # Nature ISSN-13: 9770028083002 -> check digit 2
        self.assertEqual(calculate_issn13_check_digit("977002808300"), "2")
        # Communications of ACM: check digit 1
        self.assertEqual(calculate_issn13_check_digit("977000107800"), "1")
    
    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            calculate_issn_check_digit("0028")
        with self.assertRaises(ValueError):
            calculate_issn13_check_digit("977002")


class TestConversion(unittest.TestCase):
    """Test ISSN conversion functions."""
    
    def test_issn8_to_issn13(self):
        self.assertEqual(issn8_to_issn13(ISSN_NATURE), ISSN_NATURE_13)
        self.assertEqual(issn8_to_issn13("00280836"), ISSN_NATURE_13)
        self.assertEqual(issn8_to_issn13(ISSN_X_CHECK), ISSN_X_CHECK_13)
    
    def test_issn13_to_issn8(self):
        self.assertEqual(issn13_to_issn8(ISSN_NATURE_13), "00280836")
        self.assertEqual(issn13_to_issn8(ISSN_X_CHECK_13), "2434561X")
    
    def test_conversion_roundtrip(self):
        issn8 = "00280836"
        issn13 = issn8_to_issn13(issn8)
        back_to_issn8 = issn13_to_issn8(issn13)
        self.assertEqual(issn8, back_to_issn8)
    
    def test_convert_issn(self):
        self.assertEqual(convert_issn(ISSN_NATURE, "ISSN-13"), ISSN_NATURE_13)
        self.assertEqual(convert_issn(ISSN_NATURE_13, "ISSN-8"), "00280836")
    
    def test_convert_invalid(self):
        self.assertIsNone(convert_issn("invalid", "ISSN-13"))
    
    def test_convert_same_format(self):
        self.assertEqual(convert_issn(ISSN_NATURE, "ISSN-8"), "00280836")


class TestFormatting(unittest.TestCase):
    """Test ISSN formatting functions."""
    
    def test_format_issn8(self):
        self.assertEqual(format_issn("00280836"), "0028-0836")
        self.assertEqual(format_issn("2434561X"), "2434-561X")
    
    def test_format_issn13(self):
        self.assertEqual(format_issn(ISSN_NATURE_13), "977-0028-0830-02")
    
    def test_format_with_custom_separator(self):
        self.assertEqual(format_issn("00280836", " "), "0028 0836")
    
    def test_format_invalid_raises(self):
        with self.assertRaises(ValueError):
            format_issn("invalid")
    
    def test_format_compact(self):
        self.assertEqual(format_issn_compact("0028-0836"), "00280836")
        self.assertEqual(format_issn_compact("977-0028-0830-02"), ISSN_NATURE_13)


class TestISSNL(unittest.TestCase):
    """Test ISSN-L (Linking ISSN) functions."""
    
    def test_is_issn_l_valid(self):
        self.assertTrue(is_issn_l("ISSN-L: " + ISSN_NATURE))
        self.assertTrue(is_issn_l(ISSN_NATURE))
    
    def test_is_issn_l_invalid(self):
        self.assertFalse(is_issn_l("ISSN-L: invalid"))
    
    def test_format_issn_l(self):
        self.assertEqual(format_issn_l(ISSN_NATURE), "ISSN-L: 0028-0836")
        self.assertEqual(format_issn_l("00280836"), "ISSN-L: 0028-0836")
    
    def test_extract_issn_l(self):
        self.assertEqual(extract_issn_l("ISSN-L: " + ISSN_NATURE), "00280836")
        self.assertEqual(extract_issn_l("ISSN-L: 00280836"), "00280836")
        self.assertEqual(extract_issn_l(ISSN_NATURE), "00280836")
    
    def test_extract_issn_l_invalid(self):
        self.assertIsNone(extract_issn_l("ISSN-L: invalid"))


class TestParsing(unittest.TestCase):
    """Test ISSN parsing."""
    
    def test_parse_valid_issn8(self):
        result = parse_issn(ISSN_NATURE)
        self.assertTrue(result['valid'])
        self.assertEqual(result['type'], 'ISSN-8')
        self.assertEqual(result['clean'], '00280836')
        self.assertEqual(result['check_digit'], '6')
        self.assertEqual(result['issn8'], '00280836')
        self.assertEqual(result['issn13'], ISSN_NATURE_13)
    
    def test_parse_valid_issn13(self):
        result = parse_issn(ISSN_NATURE_13)
        self.assertTrue(result['valid'])
        self.assertEqual(result['type'], 'ISSN-13')
        self.assertEqual(result['check_digit'], '2')
        self.assertEqual(result['issn8'], '00280836')
    
    def test_parse_invalid(self):
        result = parse_issn("invalid")
        self.assertFalse(result['valid'])
        self.assertIsNone(result['type'])


class TestGeneration(unittest.TestCase):
    """Test ISSN generation."""
    
    def test_generate_issn_valid(self):
        issn = generate_issn()
        self.assertTrue(is_issn8(issn))
        self.assertEqual(len(issn), 8)
    
    def test_generate_issn13_valid(self):
        issn = generate_issn13()
        self.assertTrue(is_issn13(issn))
        self.assertEqual(len(issn), 13)
    
    def test_generate_issn_l_valid(self):
        issn_l = generate_issn_l()
        self.assertTrue(is_issn_l(issn_l))
    
    def test_generate_with_prefix(self):
        issn = generate_issn("002")
        self.assertTrue(issn.startswith("002"))
        self.assertTrue(is_issn8(issn))
    
    def test_generate_multiple_unique(self):
        issns = [generate_issn() for _ in range(10)]
        # Most should be unique
        unique_count = len(set(issns))
        self.assertGreater(unique_count, 8)


class TestBatchFunctions(unittest.TestCase):
    """Test batch operations."""
    
    def test_validate_issns(self):
        results = validate_issns([ISSN_NATURE, "invalid", ISSN_NATURE_13])
        self.assertTrue(results[ISSN_NATURE]["valid"])
        self.assertFalse(results["invalid"]["valid"])
        self.assertTrue(results[ISSN_NATURE_13]["valid"])
    
    def test_find_issns_in_text(self):
        text = "期刊 ISSN " + ISSN_NATURE + " 可订阅。另见 " + ISSN_X_CHECK + "。"
        found = find_issns_in_text(text)
        self.assertEqual(len(found), 2)
        self.assertIn("00280836", found)
        self.assertIn("2434561X", found)
    
    def test_find_issns_with_prefix(self):
        text = "ISSN: " + ISSN_NATURE + " 和 ISSN-L: " + ISSN_X_CHECK
        found = find_issns_in_text(text)
        self.assertEqual(len(found), 2)
    
    def test_find_issns_empty(self):
        found = find_issns_in_text("No ISSNs here")
        self.assertEqual(len(found), 0)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_compare_issns_equivalent(self):
        self.assertTrue(compare_issns(ISSN_NATURE, ISSN_NATURE_13))
        self.assertTrue(compare_issns("00280836", ISSN_NATURE))
    
    def test_compare_issns_different(self):
        self.assertFalse(compare_issns(ISSN_NATURE, ISSN_CACM))
    
    def test_compare_issns_invalid(self):
        self.assertFalse(compare_issns("invalid", ISSN_NATURE))
    
    def test_get_issn_variants(self):
        variants = get_issn_variants(ISSN_NATURE)
        self.assertEqual(variants['issn8'], '00280836')
        self.assertEqual(variants['issn13'], ISSN_NATURE_13)
        self.assertEqual(variants['formatted8'], '0028-0836')
        self.assertEqual(variants['formatted13'], '977-0028-0830-02')
        self.assertEqual(variants['issn_l'], 'ISSN-L: 0028-0836')
    
    def test_get_issn_variants_invalid(self):
        variants = get_issn_variants("invalid")
        self.assertIsNone(variants['issn8'])
        self.assertIsNone(variants['issn13'])
    
    def test_is_print_issn(self):
        self.assertTrue(is_print_issn(ISSN_NATURE))
        self.assertFalse(is_print_issn("invalid"))
    
    def test_get_check_digit_info_valid(self):
        info = get_check_digit_info(ISSN_NATURE)
        self.assertEqual(info['provided'], '6')
        self.assertEqual(info['calculated'], '6')
        self.assertTrue(info['valid'])
        self.assertEqual(info['algorithm'], 'modulo-11')
    
    def test_get_check_digit_info_invalid_check(self):
        info = get_check_digit_info("0028-0837")  # Wrong check digit
        self.assertEqual(info['provided'], '7')
        self.assertEqual(info['calculated'], '6')
        self.assertFalse(info['valid'])
    
    def test_get_check_digit_info_issn13(self):
        info = get_check_digit_info(ISSN_NATURE_13)
        self.assertEqual(info['provided'], '2')
        self.assertTrue(info['valid'])
        self.assertEqual(info['algorithm'], 'EAN-13')


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_x_check_digit(self):
        # ISSN with X as check digit (value 10)
        self.assertTrue(is_issn8(ISSN_X_CHECK))
        self.assertEqual(calculate_issn_check_digit("2434561"), "X")
    
    def test_uppercase_x(self):
        self.assertTrue(is_issn8("2434-561x"))
        self.assertEqual(clean_issn("2434-561x"), "2434561X")
    
    def test_all_zeros(self):
        # 0000-0000 would have check digit 0
        check = calculate_issn_check_digit("0000000")
        self.assertEqual(check, "0")
    
    def test_whitespace_handling(self):
        self.assertTrue(is_issn8("  " + ISSN_NATURE + "  "))
        self.assertEqual(clean_issn("  " + ISSN_NATURE + "  "), "00280836")
    
    def test_unicode_handling(self):
        # Should handle ASCII only
        self.assertTrue(is_valid_issn(ISSN_NATURE))
    
    def test_empty_string(self):
        self.assertFalse(is_valid_issn(""))
        self.assertEqual(clean_issn(""), "")
    
    def test_issn_l_various_formats(self):
        formats = [
            "ISSN-L: " + ISSN_NATURE,
            "ISSN-L:" + ISSN_NATURE,
            "ISSN-L:  " + ISSN_NATURE,
            "issn-l: " + ISSN_NATURE,
        ]
        for fmt in formats:
            self.assertTrue(is_issn_l(fmt))
            self.assertEqual(extract_issn_l(fmt), "00280836")


class TestRealWorldISSNs(unittest.TestCase):
    """Test with real-world ISSN examples."""
    
    def test_nature(self):
        # Nature journal
        self.assertTrue(is_issn8(ISSN_NATURE))
        issn13 = issn8_to_issn13(ISSN_NATURE)
        self.assertTrue(is_issn13(issn13))
        self.assertEqual(issn13, ISSN_NATURE_13)
    
    def test_communications_acm(self):
        # Communications of the ACM
        self.assertTrue(is_issn8(ISSN_CACM))
        self.assertEqual(issn8_to_issn13(ISSN_CACM), ISSN_CACM_13)
    
    def test_science(self):
        # Science magazine
        self.assertTrue(is_issn8("0036-8075"))
    
    def test_ieee_transactions(self):
        # IEEE Transactions on Information Theory
        self.assertTrue(is_issn8(ISSN_IEEE))
        self.assertEqual(issn8_to_issn13(ISSN_IEEE), ISSN_IEEE_13)


if __name__ == "__main__":
    unittest.main(verbosity=2)