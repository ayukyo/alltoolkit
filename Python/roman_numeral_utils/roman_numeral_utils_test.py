"""
Tests for Roman Numeral Utilities
==================================

Comprehensive test suite for the roman_numeral_utils module.
"""

import unittest
import sys
sys.path.insert(0, '.')

from roman_numeral_utils.mod import (
    to_roman,
    from_roman,
    is_valid_roman,
    parse_roman_in_text,
    roman_range,
    add_roman,
    subtract_roman,
    compare_roman,
    get_roman_info,
    format_with_ordinal,
    ROMAN_ONES,
    ROMAN_TENS,
    ROMAN_HUNDREDS,
)


class TestToRoman(unittest.TestCase):
    """Test to_roman function."""
    
    def test_basic_conversions(self):
        """Test basic number to Roman conversions."""
        self.assertEqual(to_roman(1), 'I')
        self.assertEqual(to_roman(5), 'V')
        self.assertEqual(to_roman(10), 'X')
        self.assertEqual(to_roman(50), 'L')
        self.assertEqual(to_roman(100), 'C')
        self.assertEqual(to_roman(500), 'D')
        self.assertEqual(to_roman(1000), 'M')
    
    def test_subtractive_notation(self):
        """Test subtractive notation (4, 9, 40, etc.)."""
        self.assertEqual(to_roman(4), 'IV')
        self.assertEqual(to_roman(9), 'IX')
        self.assertEqual(to_roman(40), 'XL')
        self.assertEqual(to_roman(90), 'XC')
        self.assertEqual(to_roman(400), 'CD')
        self.assertEqual(to_roman(900), 'CM')
    
    def test_complex_numbers(self):
        """Test complex number conversions."""
        self.assertEqual(to_roman(49), 'XLIX')
        self.assertEqual(to_roman(99), 'XCIX')
        self.assertEqual(to_roman(449), 'CDXLIX')
        self.assertEqual(to_roman(999), 'CMXCIX')
        self.assertEqual(to_roman(1994), 'MCMXCIV')
        self.assertEqual(to_roman(2024), 'MMXXIV')
        self.assertEqual(to_roman(3999), 'MMMCMXCIX')
    
    def test_boundary_values(self):
        """Test boundary values."""
        self.assertEqual(to_roman(1), 'I')
        self.assertEqual(to_roman(3999), 'MMMCMXCIX')
    
    def test_out_of_range(self):
        """Test out of range values raise ValueError."""
        with self.assertRaises(ValueError):
            to_roman(0)
        with self.assertRaises(ValueError):
            to_roman(-1)
        with self.assertRaises(ValueError):
            to_roman(4000)
        with self.assertRaises(ValueError):
            to_roman(10000)
    
    def test_non_integer_input(self):
        """Test non-integer input raises TypeError."""
        with self.assertRaises(TypeError):
            to_roman(1.5)
        with self.assertRaises(TypeError):
            to_roman("X")
        with self.assertRaises(TypeError):
            to_roman(None)


class TestFromRoman(unittest.TestCase):
    """Test from_roman function."""
    
    def test_basic_conversions(self):
        """Test basic Roman to number conversions."""
        self.assertEqual(from_roman('I'), 1)
        self.assertEqual(from_roman('V'), 5)
        self.assertEqual(from_roman('X'), 10)
        self.assertEqual(from_roman('L'), 50)
        self.assertEqual(from_roman('C'), 100)
        self.assertEqual(from_roman('D'), 500)
        self.assertEqual(from_roman('M'), 1000)
    
    def test_subtractive_notation(self):
        """Test subtractive notation parsing."""
        self.assertEqual(from_roman('IV'), 4)
        self.assertEqual(from_roman('IX'), 9)
        self.assertEqual(from_roman('XL'), 40)
        self.assertEqual(from_roman('XC'), 90)
        self.assertEqual(from_roman('CD'), 400)
        self.assertEqual(from_roman('CM'), 900)
    
    def test_complex_numbers(self):
        """Test complex Roman numeral parsing."""
        self.assertEqual(from_roman('XLIX'), 49)
        self.assertEqual(from_roman('XCIX'), 99)
        self.assertEqual(from_roman('CDXLIX'), 449)
        self.assertEqual(from_roman('CMXCIX'), 999)
        self.assertEqual(from_roman('MCMXCIV'), 1994)
        self.assertEqual(from_roman('MMXXIV'), 2024)
        self.assertEqual(from_roman('MMMCMXCIX'), 3999)
    
    def test_case_insensitive(self):
        """Test case insensitive conversion."""
        self.assertEqual(from_roman('i'), 1)
        self.assertEqual(from_roman('iv'), 4)
        self.assertEqual(from_roman('mcmxciv'), 1994)
        self.assertEqual(from_roman('McmXcIv'), 1994)
    
    def test_whitespace_handling(self):
        """Test whitespace is trimmed."""
        self.assertEqual(from_roman('  X  '), 10)
        self.assertEqual(from_roman('\tV\t'), 5)
    
    def test_invalid_roman(self):
        """Test invalid Roman numerals raise ValueError."""
        with self.assertRaises(ValueError):
            from_roman('IIII')
        with self.assertRaises(ValueError):
            from_roman('VV')
        with self.assertRaises(ValueError):
            from_roman('XXXX')
        with self.assertRaises(ValueError):
            from_roman('ABC')
        with self.assertRaises(ValueError):
            from_roman('')
    
    def test_non_string_input(self):
        """Test non-string input raises TypeError."""
        with self.assertRaises(TypeError):
            from_roman(10)
        with self.assertRaises(TypeError):
            from_roman(None)


class TestIsValidRoman(unittest.TestCase):
    """Test is_valid_roman function."""
    
    def test_valid_numerals(self):
        """Test valid Roman numerals."""
        self.assertTrue(is_valid_roman('I'))
        self.assertTrue(is_valid_roman('IV'))
        self.assertTrue(is_valid_roman('IX'))
        self.assertTrue(is_valid_roman('MCMXCIV'))
        self.assertTrue(is_valid_roman('MMMCMXCIX'))
    
    def test_invalid_numerals(self):
        """Test invalid Roman numerals."""
        self.assertFalse(is_valid_roman('IIII'))
        self.assertFalse(is_valid_roman('VV'))
        self.assertFalse(is_valid_roman('XXXX'))
        self.assertFalse(is_valid_roman('LL'))
        self.assertFalse(is_valid_roman('DD'))
        self.assertFalse(is_valid_roman('ABC'))
        self.assertFalse(is_valid_roman(''))
        self.assertFalse(is_valid_roman('MMMM'))
    
    def test_case_insensitive(self):
        """Test case insensitive validation."""
        self.assertTrue(is_valid_roman('iv'))
        self.assertTrue(is_valid_roman('MCMXcIv'))
    
    def test_non_string_input(self):
        """Test non-string input returns False."""
        self.assertFalse(is_valid_roman(10))
        self.assertFalse(is_valid_roman(None))
        self.assertFalse(is_valid_roman(['I', 'V']))


class TestRoundTrip(unittest.TestCase):
    """Test round-trip conversions."""
    
    def test_all_values(self):
        """Test all values 1-3999 for round-trip consistency."""
        for i in range(1, 4000):
            roman = to_roman(i)
            back = from_roman(roman)
            self.assertEqual(i, back, f"Round trip failed for {i}: {roman}")
    
    def test_specific_values(self):
        """Test specific known values."""
        test_cases = [1, 4, 9, 49, 99, 499, 999, 1492, 1776, 1994, 2024, 3999]
        for num in test_cases:
            roman = to_roman(num)
            back = from_roman(roman)
            self.assertEqual(num, back)


class TestParseRomanInText(unittest.TestCase):
    """Test parse_roman_in_text function."""
    
    def test_simple_parsing(self):
        """Test simple text parsing."""
        text = "Chapter IV"
        result = parse_roman_in_text(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ('IV', 4, 8, 10))
    
    def test_multiple_numerals(self):
        """Test parsing multiple numerals."""
        text = "King Henry VIII had VI wives"
        result = parse_roman_in_text(text)
        self.assertEqual(len(result), 2)
        values = [r[1] for r in result]
        self.assertIn(8, values)
        self.assertIn(6, values)
    
    def test_no_numerals(self):
        """Test text with no Roman numerals."""
        text = "This has no Roman numerals"
        result = parse_roman_in_text(text)
        self.assertEqual(len(result), 0)
    
    def test_ignores_invalid(self):
        """Test that invalid sequences are ignored."""
        text = "IIII is invalid but IV is valid"
        result = parse_roman_in_text(text)
        values = [r[1] for r in result]
        self.assertIn(4, values)
        # IIII should not be included as it's invalid
    
    def test_positions(self):
        """Test position reporting."""
        text = "Start IV end"
        result = parse_roman_in_text(text)
        self.assertEqual(result[0][2], 6)  # start position
        self.assertEqual(result[0][3], 8)  # end position


class TestRomanRange(unittest.TestCase):
    """Test roman_range function."""
    
    def test_basic_range(self):
        """Test basic range generation."""
        result = list(roman_range(1, 6))
        self.assertEqual(result, ['I', 'II', 'III', 'IV', 'V'])
    
    def test_with_step(self):
        """Test range with step."""
        result = list(roman_range(1, 11, 2))
        self.assertEqual(result, ['I', 'III', 'V', 'VII', 'IX'])
    
    def test_empty_range(self):
        """Test empty range."""
        result = list(roman_range(5, 5))
        self.assertEqual(result, [])


class TestArithmetic(unittest.TestCase):
    """Test Roman numeral arithmetic."""
    
    def test_addition(self):
        """Test Roman numeral addition."""
        self.assertEqual(add_roman('I', 'I'), 'II')
        self.assertEqual(add_roman('X', 'V'), 'XV')
        self.assertEqual(add_roman('IV', 'I'), 'V')
        self.assertEqual(add_roman('XC', 'X'), 'C')
    
    def test_subtraction(self):
        """Test Roman numeral subtraction."""
        self.assertEqual(subtract_roman('II', 'I'), 'I')
        self.assertEqual(subtract_roman('X', 'V'), 'V')
        self.assertEqual(subtract_roman('V', 'I'), 'IV')
    
    def test_subtraction_out_of_range(self):
        """Test subtraction resulting in invalid range."""
        with self.assertRaises(ValueError):
            subtract_roman('I', 'I')
        with self.assertRaises(ValueError):
            subtract_roman('V', 'X')
    
    def test_compare(self):
        """Test Roman numeral comparison."""
        self.assertEqual(compare_roman('I', 'V'), -1)
        self.assertEqual(compare_roman('V', 'V'), 0)
        self.assertEqual(compare_roman('X', 'V'), 1)


class TestGetRomanInfo(unittest.TestCase):
    """Test get_roman_info function."""
    
    def test_basic_info(self):
        """Test basic info extraction."""
        info = get_roman_info('IV')
        self.assertTrue(info['valid'])
        self.assertEqual(info['value'], 4)
        self.assertEqual(info['length'], 2)
        self.assertEqual(info['characters'], ['I', 'V'])
    
    def test_invalid_info(self):
        """Test info for invalid numeral."""
        info = get_roman_info('IIII')
        self.assertFalse(info['valid'])
        self.assertIsNone(info['value'])
    
    def test_breakdown(self):
        """Test breakdown of numeral."""
        info = get_roman_info('MCMXCIV')
        self.assertTrue(info['valid'])
        self.assertEqual(info['value'], 1994)
        self.assertIsInstance(info['breakdown'], list)
    
    def test_case_insensitive(self):
        """Test case insensitive info."""
        info_lower = get_roman_info('iv')
        info_upper = get_roman_info('IV')
        self.assertEqual(info_lower['value'], info_upper['value'])


class TestFormatWithOrdinal(unittest.TestCase):
    """Test format_with_ordinal function."""
    
    def test_roman_format(self):
        """Test Roman numeral formatting."""
        self.assertEqual(format_with_ordinal(1), 'I')
        self.assertEqual(format_with_ordinal(5), 'V')
        self.assertEqual(format_with_ordinal(10), 'X')
    
    def test_ordinal_format(self):
        """Test ordinal suffix formatting."""
        self.assertEqual(format_with_ordinal(1, use_roman=False), '1st')
        self.assertEqual(format_with_ordinal(2, use_roman=False), '2nd')
        self.assertEqual(format_with_ordinal(3, use_roman=False), '3rd')
        self.assertEqual(format_with_ordinal(4, use_roman=False), '4th')
        self.assertEqual(format_with_ordinal(11, use_roman=False), '11th')
        self.assertEqual(format_with_ordinal(21, use_roman=False), '21st')
        self.assertEqual(format_with_ordinal(22, use_roman=False), '22nd')
        self.assertEqual(format_with_ordinal(23, use_roman=False), '23rd')


class TestConstants(unittest.TestCase):
    """Test module constants."""
    
    def test_ones(self):
        """Test ROMAN_ONES constant."""
        self.assertEqual(len(ROMAN_ONES), 10)
        for i, roman in enumerate(ROMAN_ONES, 1):
            self.assertEqual(from_roman(roman), i)
    
    def test_tens(self):
        """Test ROMAN_TENS constant."""
        self.assertEqual(len(ROMAN_TENS), 10)
        for i, roman in enumerate(ROMAN_TENS, 1):
            self.assertEqual(from_roman(roman), i * 10)
    
    def test_hundreds(self):
        """Test ROMAN_HUNDREDS constant."""
        self.assertEqual(len(ROMAN_HUNDREDS), 10)
        for i, roman in enumerate(ROMAN_HUNDREDS, 1):
            self.assertEqual(from_roman(roman), i * 100)


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)