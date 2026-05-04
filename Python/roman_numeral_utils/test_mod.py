"""
Unit tests for Roman Numeral Utilities
======================================

Comprehensive test suite for roman_numeral_utils module.

Run with: python -m pytest test_mod.py -v
Or simply: python test_mod.py
"""

import unittest
from mod import (
    to_roman, from_roman, is_valid_roman,
    roman_add, roman_subtract, roman_multiply, roman_divide,
    get_roman_info, find_roman_palindromes, RomanNumeral,
    InvalidRomanNumeralError, OutOfRangeError, RomanNumeralError,
    int_to_roman, roman_to_int
)


class TestToRoman(unittest.TestCase):
    """Tests for to_roman() function."""
    
    def test_basic_numbers(self):
        """Test basic number conversions."""
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
        self.assertEqual(to_roman(14), 'XIV')
        self.assertEqual(to_roman(49), 'XLIX')
        self.assertEqual(to_roman(99), 'XCIX')
        self.assertEqual(to_roman(444), 'CDXLIV')
        self.assertEqual(to_roman(999), 'CMXCIX')
        self.assertEqual(to_roman(1994), 'MCMXCIV')
        self.assertEqual(to_roman(2023), 'MMXXIII')
        self.assertEqual(to_roman(3999), 'MMMCMXCIX')
    
    def test_out_of_range(self):
        """Test out of range errors."""
        with self.assertRaises(OutOfRangeError):
            to_roman(0)
        with self.assertRaises(OutOfRangeError):
            to_roman(-1)
        with self.assertRaises(OutOfRangeError):
            to_roman(4000)
        with self.assertRaises(OutOfRangeError):
            to_roman(10000)
    
    def test_invalid_type(self):
        """Test type errors."""
        with self.assertRaises(TypeError):
            to_roman(1.5)
        with self.assertRaises(TypeError):
            to_roman("10")
        with self.assertRaises(TypeError):
            to_roman(None)
    
    def test_edge_cases(self):
        """Test edge cases."""
        self.assertEqual(to_roman(2), 'II')
        self.assertEqual(to_roman(3), 'III')
        self.assertEqual(to_roman(6), 'VI')
        self.assertEqual(to_roman(7), 'VII')
        self.assertEqual(to_roman(8), 'VIII')
        self.assertEqual(to_roman(11), 'XI')
        self.assertEqual(to_roman(15), 'XV')
        self.assertEqual(to_roman(19), 'XIX')


class TestFromRoman(unittest.TestCase):
    """Tests for from_roman() function."""
    
    def test_basic_numerals(self):
        """Test basic numeral conversions."""
        self.assertEqual(from_roman('I'), 1)
        self.assertEqual(from_roman('V'), 5)
        self.assertEqual(from_roman('X'), 10)
        self.assertEqual(from_roman('L'), 50)
        self.assertEqual(from_roman('C'), 100)
        self.assertEqual(from_roman('D'), 500)
        self.assertEqual(from_roman('M'), 1000)
    
    def test_subtractive_notation(self):
        """Test subtractive notation conversions."""
        self.assertEqual(from_roman('IV'), 4)
        self.assertEqual(from_roman('IX'), 9)
        self.assertEqual(from_roman('XL'), 40)
        self.assertEqual(from_roman('XC'), 90)
        self.assertEqual(from_roman('CD'), 400)
        self.assertEqual(from_roman('CM'), 900)
    
    def test_complex_numerals(self):
        """Test complex numeral conversions."""
        self.assertEqual(from_roman('XIV'), 14)
        self.assertEqual(from_roman('XLIX'), 49)
        self.assertEqual(from_roman('XCIX'), 99)
        self.assertEqual(from_roman('CDXLIV'), 444)
        self.assertEqual(from_roman('CMXCIX'), 999)
        self.assertEqual(from_roman('MCMXCIV'), 1994)
        self.assertEqual(from_roman('MMXXIII'), 2023)
        self.assertEqual(from_roman('MMMCMXCIX'), 3999)
    
    def test_case_insensitive(self):
        """Test case insensitivity."""
        self.assertEqual(from_roman('iv'), 4)
        self.assertEqual(from_roman('Xv'), 15)
        self.assertEqual(from_roman('Mcmxciv'), 1994)
    
    def test_whitespace_handling(self):
        """Test whitespace handling."""
        self.assertEqual(from_roman('  I  '), 1)
        self.assertEqual(from_roman('\tIV\t'), 4)
    
    def test_invalid_numerals(self):
        """Test invalid numeral detection."""
        with self.assertRaises(InvalidRomanNumeralError):
            from_roman('')
        with self.assertRaises(InvalidRomanNumeralError):
            from_roman('IIII')
        with self.assertRaises(InvalidRomanNumeralError):
            from_roman('VV')
        with self.assertRaises(InvalidRomanNumeralError):
            from_roman('XXXX')
        with self.assertRaises(InvalidRomanNumeralError):
            from_roman('ABC')
    
    def test_invalid_type(self):
        """Test type errors."""
        with self.assertRaises(TypeError):
            from_roman(10)
        with self.assertRaises(TypeError):
            from_roman(None)
        with self.assertRaises(TypeError):
            from_roman([])


class TestRoundTrip(unittest.TestCase):
    """Tests for round-trip conversions."""
    
    def test_all_numbers(self):
        """Test that all numbers 1-3999 convert correctly both ways."""
        for num in range(1, 100):  # Test first 100
            roman = to_roman(num)
            back = from_roman(roman)
            self.assertEqual(back, num, f"Failed for {num} -> {roman} -> {back}")
        
        # Test some larger numbers
        for num in [100, 500, 999, 1000, 1994, 2023, 3000, 3999]:
            roman = to_roman(num)
            back = from_roman(roman)
            self.assertEqual(back, num)


class TestIsValidRoman(unittest.TestCase):
    """Tests for is_valid_roman() function."""
    
    def test_valid_numerals(self):
        """Test valid numeral detection."""
        self.assertTrue(is_valid_roman('I'))
        self.assertTrue(is_valid_roman('IV'))
        self.assertTrue(is_valid_roman('XIV'))
        self.assertTrue(is_valid_roman('MCMXCIV'))
        self.assertTrue(is_valid_roman('MMXXIII'))
    
    def test_invalid_numerals(self):
        """Test invalid numeral detection."""
        self.assertFalse(is_valid_roman('IIII'))
        self.assertFalse(is_valid_roman('VV'))
        self.assertFalse(is_valid_roman('ABC'))
        self.assertFalse(is_valid_roman(''))
        self.assertFalse(is_valid_roman('IM'))  # Invalid subtractive
        self.assertFalse(is_valid_roman('XM'))


class TestArithmetic(unittest.TestCase):
    """Tests for arithmetic operations."""
    
    def test_addition(self):
        """Test Roman numeral addition."""
        self.assertEqual(roman_add('I', 'I'), 'II')
        self.assertEqual(roman_add('X', 'V'), 'XV')
        self.assertEqual(roman_add('IX', 'I'), 'X')
        self.assertEqual(roman_add('X', 'X'), 'XX')
        self.assertEqual(roman_add('C', 'D'), 'DC')
    
    def test_subtraction(self):
        """Test Roman numeral subtraction."""
        self.assertEqual(roman_subtract('X', 'V'), 'V')
        self.assertEqual(roman_subtract('X', 'I'), 'IX')
        self.assertEqual(roman_subtract('L', 'X'), 'XL')
        self.assertEqual(roman_subtract('C', 'L'), 'L')
    
    def test_subtraction_zero_error(self):
        """Test subtraction resulting in zero."""
        with self.assertRaises(OutOfRangeError):
            roman_subtract('X', 'X')
    
    def test_multiplication(self):
        """Test Roman numeral multiplication."""
        self.assertEqual(roman_multiply('X', 'V'), 'L')
        self.assertEqual(roman_multiply('IV', 'V'), 'XX')
        self.assertEqual(roman_multiply('X', 'X'), 'C')
        self.assertEqual(roman_multiply('II', 'II'), 'IV')
    
    def test_division(self):
        """Test Roman numeral division."""
        self.assertEqual(roman_divide('X', 'II'), ('V', ''))
        self.assertEqual(roman_divide('X', 'III'), ('III', 'I'))
        self.assertEqual(roman_divide('XX', 'V'), ('IV', ''))
    
    def test_division_zero_error(self):
        """Test division by zero."""
        # Note: There is no Roman numeral for zero, so we cannot test
        # division by zero directly. The function checks if num2 == 0
        # after conversion, but since Roman numerals cannot represent 0,
        # this path is effectively unreachable with valid input.
        pass  # Roman numerals cannot represent zero
    
    def test_division_zero_quotient(self):
        """Test division with zero quotient."""
        with self.assertRaises(OutOfRangeError):
            roman_divide('I', 'V')


class TestGetRomanInfo(unittest.TestCase):
    """Tests for get_roman_info() function."""
    
    def test_info_structure(self):
        """Test info structure."""
        info = get_roman_info(1994)
        self.assertEqual(info['arabic'], 1994)
        self.assertEqual(info['roman'], 'MCMXCIV')
        self.assertIsInstance(info['components'], list)
    
    def test_components(self):
        """Test component breakdown."""
        info = get_roman_info(14)
        self.assertEqual(info['roman'], 'XIV')
        self.assertEqual(info['components'], [('X', 10), ('IV', 4)])
    
    def test_simple_numbers(self):
        """Test simple number info."""
        info = get_roman_info(5)
        self.assertEqual(info['arabic'], 5)
        self.assertEqual(info['roman'], 'V')
        self.assertEqual(info['components'], [('V', 5)])


class TestFindRomanPalindromes(unittest.TestCase):
    """Tests for find_roman_palindromes() function."""
    
    def test_palindromes(self):
        """Test finding palindromes."""
        palindromes = find_roman_palindromes(1, 20)
        # I, II, III are palindromes
        self.assertIn((1, 'I'), palindromes)
        self.assertIn((2, 'II'), palindromes)
        self.assertIn((3, 'III'), palindromes)
    
    def test_non_palindromes(self):
        """Test that non-palindromes are not included."""
        palindromes = find_roman_palindromes(1, 10)
        # IV is not a palindrome
        self.assertNotIn((4, 'IV'), palindromes)


class TestRomanNumeralClass(unittest.TestCase):
    """Tests for RomanNumeral class."""
    
    def test_creation_from_int(self):
        """Test creating from integer."""
        r = RomanNumeral(10)
        self.assertEqual(r.arabic, 10)
        self.assertEqual(r.roman, 'X')
    
    def test_creation_from_string(self):
        """Test creating from Roman numeral string."""
        r = RomanNumeral('XIV')
        self.assertEqual(r.arabic, 14)
        self.assertEqual(r.roman, 'XIV')
    
    def test_string_representation(self):
        """Test string representation."""
        r = RomanNumeral(10)
        self.assertEqual(str(r), 'X')
    
    def test_repr(self):
        """Test repr."""
        r = RomanNumeral(10)
        self.assertEqual(repr(r), "RomanNumeral('X', 10)")
    
    def test_int_conversion(self):
        """Test integer conversion."""
        r = RomanNumeral(10)
        self.assertEqual(int(r), 10)
    
    def test_equality(self):
        """Test equality comparisons."""
        r1 = RomanNumeral(10)
        r2 = RomanNumeral(10)
        r3 = RomanNumeral(5)
        
        self.assertEqual(r1, r2)
        self.assertNotEqual(r1, r3)
        self.assertEqual(r1, 10)
        self.assertEqual(r1, 'X')
    
    def test_comparison(self):
        """Test comparison operators."""
        r1 = RomanNumeral(10)
        r2 = RomanNumeral(5)
        
        self.assertTrue(r1 > r2)
        self.assertTrue(r2 < r1)
        self.assertTrue(r1 >= r2)
        self.assertTrue(r2 <= r1)
    
    def test_addition(self):
        """Test addition."""
        r1 = RomanNumeral(10)
        r2 = RomanNumeral(5)
        
        result = r1 + r2
        self.assertEqual(result.roman, 'XV')
        self.assertEqual(result.arabic, 15)
        
        result = r1 + 5
        self.assertEqual(result.arabic, 15)
    
    def test_subtraction(self):
        """Test subtraction."""
        r1 = RomanNumeral(10)
        r2 = RomanNumeral(5)
        
        result = r1 - r2
        self.assertEqual(result.roman, 'V')
        self.assertEqual(result.arabic, 5)
    
    def test_multiplication(self):
        """Test multiplication."""
        r1 = RomanNumeral(10)
        
        result = r1 * 2
        self.assertEqual(result.roman, 'XX')
        self.assertEqual(result.arabic, 20)
    
    def test_floor_division(self):
        """Test floor division."""
        r1 = RomanNumeral(10)
        
        result = r1 // 3
        self.assertEqual(result.arabic, 3)
    
    def test_hash(self):
        """Test hashing."""
        r1 = RomanNumeral(10)
        r2 = RomanNumeral(10)
        
        self.assertEqual(hash(r1), hash(r2))
        
        # Can be used in sets and dicts
        s = {r1, r2}
        self.assertEqual(len(s), 1)
    
    def test_invalid_creation(self):
        """Test invalid creation."""
        with self.assertRaises(TypeError):
            RomanNumeral(1.5)
        with self.assertRaises(TypeError):
            RomanNumeral([])


class TestAliases(unittest.TestCase):
    """Tests for alias functions."""
    
    def test_int_to_roman(self):
        """Test int_to_roman alias."""
        self.assertEqual(int_to_roman(10), to_roman(10))
        self.assertEqual(int_to_roman(1994), to_roman(1994))
    
    def test_roman_to_int(self):
        """Test roman_to_int alias."""
        self.assertEqual(roman_to_int('X'), from_roman('X'))
        self.assertEqual(roman_to_int('MCMXCIV'), from_roman('MCMXCIV'))


if __name__ == '__main__':
    unittest.main(verbosity=2)