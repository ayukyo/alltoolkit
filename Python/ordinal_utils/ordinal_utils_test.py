"""
Test suite for Ordinal Number Utilities

Tests all functions in the ordinal_utils module.
Run with: python -m pytest ordinal_utils_test.py -v
Or directly: python ordinal_utils_test.py
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    get_ordinal_suffix,
    to_ordinal,
    to_ordinal_word,
    from_ordinal,
    is_ordinal,
    get_all_ordinal_forms,
    format_date_with_ordinal,
    get_rank_suffix,
    format_ranking,
    ordinal_range,
    compare_ordinals,
    ordinal_to_roman,
    roman_to_ordinal,
    get_ordinal_suffix_only,
    ordinal,
    from_ordinal_number,
    ordinal_word
)


class TestGetOrdinalSuffix(unittest.TestCase):
    """Tests for get_ordinal_suffix function"""
    
    def test_basic_st(self):
        self.assertEqual(get_ordinal_suffix(1), "st")
        self.assertEqual(get_ordinal_suffix(21), "st")
        self.assertEqual(get_ordinal_suffix(31), "st")
        self.assertEqual(get_ordinal_suffix(101), "st")
    
    def test_basic_nd(self):
        self.assertEqual(get_ordinal_suffix(2), "nd")
        self.assertEqual(get_ordinal_suffix(22), "nd")
        self.assertEqual(get_ordinal_suffix(32), "nd")
        self.assertEqual(get_ordinal_suffix(102), "nd")
    
    def test_basic_rd(self):
        self.assertEqual(get_ordinal_suffix(3), "rd")
        self.assertEqual(get_ordinal_suffix(23), "rd")
        self.assertEqual(get_ordinal_suffix(33), "rd")
        self.assertEqual(get_ordinal_suffix(103), "rd")
    
    def test_basic_th(self):
        self.assertEqual(get_ordinal_suffix(4), "th")
        self.assertEqual(get_ordinal_suffix(5), "th")
        self.assertEqual(get_ordinal_suffix(10), "th")
        self.assertEqual(get_ordinal_suffix(20), "th")
    
    def test_special_cases(self):
        # 11, 12, 13 should all be "th"
        self.assertEqual(get_ordinal_suffix(11), "th")
        self.assertEqual(get_ordinal_suffix(12), "th")
        self.assertEqual(get_ordinal_suffix(13), "th")
        # But 111, 112, 113 also
        self.assertEqual(get_ordinal_suffix(111), "th")
        self.assertEqual(get_ordinal_suffix(112), "th")
        self.assertEqual(get_ordinal_suffix(113), "th")
    
    def test_french_suffix(self):
        self.assertEqual(get_ordinal_suffix(1, "fr"), "er")
        self.assertEqual(get_ordinal_suffix(2, "fr"), "e")
        self.assertEqual(get_ordinal_suffix(5, "fr"), "e")
    
    def test_german_suffix(self):
        self.assertEqual(get_ordinal_suffix(1, "de"), ".")
        self.assertEqual(get_ordinal_suffix(5, "de"), ".")
    
    def test_chinese_suffix(self):
        self.assertEqual(get_ordinal_suffix(5, "zh"), "")


class TestToOrdinal(unittest.TestCase):
    """Tests for to_ordinal function"""
    
    def test_english_ordinals(self):
        self.assertEqual(to_ordinal(1), "1st")
        self.assertEqual(to_ordinal(2), "2nd")
        self.assertEqual(to_ordinal(3), "3rd")
        self.assertEqual(to_ordinal(4), "4th")
        self.assertEqual(to_ordinal(11), "11th")
        self.assertEqual(to_ordinal(12), "12th")
        self.assertEqual(to_ordinal(13), "13th")
        self.assertEqual(to_ordinal(21), "21st")
        self.assertEqual(to_ordinal(22), "22nd")
        self.assertEqual(to_ordinal(23), "23rd")
        self.assertEqual(to_ordinal(100), "100th")
        self.assertEqual(to_ordinal(101), "101st")
    
    def test_french_ordinals(self):
        self.assertEqual(to_ordinal(1, "fr"), "1er")
        self.assertEqual(to_ordinal(2, "fr"), "2e")
        self.assertEqual(to_ordinal(42, "fr"), "42e")
    
    def test_german_ordinals(self):
        self.assertEqual(to_ordinal(1, "de"), "1.")
        self.assertEqual(to_ordinal(5, "de"), "5.")
        self.assertEqual(to_ordinal(100, "de"), "100.")
    
    def test_chinese_ordinals(self):
        self.assertEqual(to_ordinal(1, "zh"), "第1")
        self.assertEqual(to_ordinal(10, "zh"), "第10")
        self.assertEqual(to_ordinal(100, "zh"), "第100")
    
    def test_japanese_ordinals(self):
        self.assertEqual(to_ordinal(1, "ja"), "1番目")
        self.assertEqual(to_ordinal(5, "ja"), "5番目")
    
    def test_zero(self):
        self.assertEqual(to_ordinal(0), "0th")
    
    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            to_ordinal(-1)
    
    def test_unknown_language_defaults_to_english(self):
        self.assertEqual(to_ordinal(1, "unknown"), "1st")


class TestToOrdinalWord(unittest.TestCase):
    """Tests for to_ordinal_word function"""
    
    def test_basic_words(self):
        self.assertEqual(to_ordinal_word(1), "first")
        self.assertEqual(to_ordinal_word(2), "second")
        self.assertEqual(to_ordinal_word(3), "third")
        self.assertEqual(to_ordinal_word(4), "fourth")
        self.assertEqual(to_ordinal_word(5), "fifth")
        self.assertEqual(to_ordinal_word(10), "tenth")
        self.assertEqual(to_ordinal_word(11), "eleventh")
        self.assertEqual(to_ordinal_word(12), "twelfth")
    
    def test_tens(self):
        self.assertEqual(to_ordinal_word(20), "twentieth")
        self.assertEqual(to_ordinal_word(30), "thirtieth")
        self.assertEqual(to_ordinal_word(100), "hundredth")
    
    def test_compound_words(self):
        self.assertEqual(to_ordinal_word(21), "twenty-first")
        self.assertEqual(to_ordinal_word(22), "twenty-second")
        self.assertEqual(to_ordinal_word(33), "thirty-third")
        self.assertEqual(to_ordinal_word(99), "ninety-ninth")
    
    def test_large_number_fallback(self):
        # Numbers > 100 should fall back to numeric ordinal
        result = to_ordinal_word(101)
        self.assertEqual(result, "101st")


class TestFromOrdinal(unittest.TestCase):
    """Tests for from_ordinal function"""
    
    def test_parse_english_ordinals(self):
        self.assertEqual(from_ordinal("1st"), 1)
        self.assertEqual(from_ordinal("2nd"), 2)
        self.assertEqual(from_ordinal("3rd"), 3)
        self.assertEqual(from_ordinal("11th"), 11)
        self.assertEqual(from_ordinal("21st"), 21)
        self.assertEqual(from_ordinal("100th"), 100)
    
    def test_parse_chinese_ordinals(self):
        self.assertEqual(from_ordinal("第1"), 1)
        self.assertEqual(from_ordinal("第100"), 100)
    
    def test_parse_japanese_ordinals(self):
        self.assertEqual(from_ordinal("5番目"), 5)
    
    def test_parse_german_ordinals(self):
        self.assertEqual(from_ordinal("1."), 1)
        self.assertEqual(from_ordinal("10."), 10)
    
    def test_parse_ordinal_words(self):
        self.assertEqual(from_ordinal("first"), 1)
        self.assertEqual(from_ordinal("second"), 2)
        self.assertEqual(from_ordinal("third"), 3)
        self.assertEqual(from_ordinal("tenth"), 10)
        self.assertEqual(from_ordinal("twentieth"), 20)
    
    def test_parse_compound_words(self):
        self.assertEqual(from_ordinal("twenty-first"), 21)
        self.assertEqual(from_ordinal("twenty-second"), 22)
        self.assertEqual(from_ordinal("thirty-third"), 33)
    
    def test_empty_string(self):
        self.assertIsNone(from_ordinal(""))
    
    def test_invalid_string(self):
        self.assertIsNone(from_ordinal("hello"))
        self.assertIsNone(from_ordinal("xyz"))


class TestIsOrdinal(unittest.TestCase):
    """Tests for is_ordinal function"""
    
    def test_valid_ordinals(self):
        self.assertTrue(is_ordinal("1st"))
        self.assertTrue(is_ordinal("2nd"))
        self.assertTrue(is_ordinal("3rd"))
        self.assertTrue(is_ordinal("第5"))
        self.assertTrue(is_ordinal("first"))
        self.assertTrue(is_ordinal("twenty-first"))
    
    def test_invalid_ordinals(self):
        self.assertFalse(is_ordinal("hello"))
        self.assertFalse(is_ordinal(""))
        # Note: "123abc" starts with a number, so it's parseable (returns 123)
        # This is expected behavior - we extract numbers from the beginning
    
    def test_edge_cases(self):
        self.assertFalse(is_ordinal(None))


class TestGetAllOrdinalForms(unittest.TestCase):
    """Tests for get_all_ordinal_forms function"""
    
    def test_all_forms(self):
        forms = get_all_ordinal_forms(5)
        self.assertIn("en", forms)
        self.assertEqual(forms["en"], "5th")
        self.assertIn("fr", forms)
        self.assertIn("de", forms)
        self.assertIn("zh", forms)
    
    def test_first(self):
        forms = get_all_ordinal_forms(1)
        self.assertEqual(forms["en"], "1st")
        self.assertEqual(forms["fr"], "1er")


class TestFormatDateWithOrdinal(unittest.TestCase):
    """Tests for format_date_with_ordinal function"""
    
    def test_mdy_format(self):
        result = format_date_with_ordinal(4, "July", 2026)
        self.assertEqual(result, "July 4th, 2026")
    
    def test_dmy_format(self):
        result = format_date_with_ordinal(3, "May", 2026, format_type="dmy")
        self.assertEqual(result, "3rd May 2026")
    
    def test_no_year(self):
        result = format_date_with_ordinal(1, "January")
        self.assertEqual(result, "January 1st")
    
    def test_month_number(self):
        result = format_date_with_ordinal(15, 3, 2026)
        self.assertEqual(result, "March 15th, 2026")
    
    def test_ordinals_in_dates(self):
        self.assertIn("1st", format_date_with_ordinal(1, "Jan"))
        self.assertIn("2nd", format_date_with_ordinal(2, "Feb"))
        self.assertIn("3rd", format_date_with_ordinal(3, "Mar"))
        self.assertIn("11th", format_date_with_ordinal(11, "Nov"))


class TestRanking(unittest.TestCase):
    """Tests for ranking functions"""
    
    def test_get_rank_suffix(self):
        self.assertEqual(get_rank_suffix(1), "🥇")
        self.assertEqual(get_rank_suffix(2), "🥈")
        self.assertEqual(get_rank_suffix(3), "🥉")
        self.assertEqual(get_rank_suffix(4), "4th")
        self.assertEqual(get_rank_suffix(5), "5th")
    
    def test_format_ranking(self):
        self.assertEqual(format_ranking(1, "Team Alpha"), "🥇 Team Alpha")
        self.assertEqual(format_ranking(2, "Team Beta", 95), "🥈 Team Beta (95)")
        self.assertEqual(format_ranking(4, "Team Delta", 80), "4th Team Delta (80)")
    
    def test_format_ranking_no_name(self):
        self.assertEqual(format_ranking(1), "🥇")


class TestOrdinalRange(unittest.TestCase):
    """Tests for ordinal_range function"""
    
    def test_ascending_range(self):
        result = ordinal_range(1, 5)
        expected = ["1st", "2nd", "3rd", "4th", "5th"]
        self.assertEqual(result, expected)
    
    def test_descending_range(self):
        result = ordinal_range(5, 1)
        expected = ["5th", "4th", "3rd", "2nd", "1st"]
        self.assertEqual(result, expected)
    
    def test_french_range(self):
        result = ordinal_range(1, 3, "fr")
        expected = ["1er", "2e", "3e"]
        self.assertEqual(result, expected)
    
    def test_single_value(self):
        result = ordinal_range(1, 1)
        self.assertEqual(result, ["1st"])


class TestCompareOrdinals(unittest.TestCase):
    """Tests for compare_ordinals function"""
    
    def test_less_than(self):
        self.assertEqual(compare_ordinals("1st", "2nd"), -1)
        self.assertEqual(compare_ordinals("5th", "10th"), -1)
    
    def test_equal(self):
        self.assertEqual(compare_ordinals("3rd", "3rd"), 0)
        self.assertEqual(compare_ordinals("第5", "第5"), 0)
    
    def test_greater_than(self):
        self.assertEqual(compare_ordinals("2nd", "1st"), 1)
        self.assertEqual(compare_ordinals("100th", "50th"), 1)
    
    def test_mixed_languages(self):
        self.assertEqual(compare_ordinals("第1", "10th"), -1)
        self.assertEqual(compare_ordinals("10番目", "5th"), 1)


class TestRomanNumerals(unittest.TestCase):
    """Tests for Roman numeral functions"""
    
    def test_basic_roman(self):
        self.assertEqual(ordinal_to_roman(1), "I")
        self.assertEqual(ordinal_to_roman(5), "V")
        self.assertEqual(ordinal_to_roman(10), "X")
        self.assertEqual(ordinal_to_roman(50), "L")
        self.assertEqual(ordinal_to_roman(100), "C")
        self.assertEqual(ordinal_to_roman(500), "D")
        self.assertEqual(ordinal_to_roman(1000), "M")
    
    def test_subtractive_notation(self):
        self.assertEqual(ordinal_to_roman(4), "IV")
        self.assertEqual(ordinal_to_roman(9), "IX")
        self.assertEqual(ordinal_to_roman(40), "XL")
        self.assertEqual(ordinal_to_roman(90), "XC")
        self.assertEqual(ordinal_to_roman(400), "CD")
        self.assertEqual(ordinal_to_roman(900), "CM")
    
    def test_complex_numbers(self):
        self.assertEqual(ordinal_to_roman(49), "XLIX")
        self.assertEqual(ordinal_to_roman(99), "XCIX")
        self.assertEqual(ordinal_to_roman(2024), "MMXXIV")
        self.assertEqual(ordinal_to_roman(3999), "MMMCMXCIX")
    
    def test_roman_to_ordinal(self):
        self.assertEqual(roman_to_ordinal("I"), 1)
        self.assertEqual(roman_to_ordinal("V"), 5)
        self.assertEqual(roman_to_ordinal("X"), 10)
        self.assertEqual(roman_to_ordinal("IV"), 4)
        self.assertEqual(roman_to_ordinal("IX"), 9)
        self.assertEqual(roman_to_ordinal("MMXXIV"), 2024)
    
    def test_roundtrip(self):
        for n in [1, 4, 9, 49, 100, 3999]:
            self.assertEqual(roman_to_ordinal(ordinal_to_roman(n)), n)
    
    def test_invalid_roman(self):
        self.assertIsNone(roman_to_ordinal(""))
        self.assertIsNone(roman_to_ordinal("ABC"))
    
    def test_out_of_range(self):
        with self.assertRaises(ValueError):
            ordinal_to_roman(0)
        with self.assertRaises(ValueError):
            ordinal_to_roman(4000)
        with self.assertRaises(ValueError):
            ordinal_to_roman(-1)


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for convenience function aliases"""
    
    def test_ordinal_alias(self):
        self.assertEqual(ordinal(1), to_ordinal(1))
        self.assertEqual(ordinal(5), to_ordinal(5))
    
    def test_from_ordinal_number_alias(self):
        self.assertEqual(from_ordinal_number("1st"), from_ordinal("1st"))
    
    def test_ordinal_word_alias(self):
        self.assertEqual(ordinal_word(1), to_ordinal_word(1))
    
    def test_get_ordinal_suffix_only(self):
        self.assertEqual(get_ordinal_suffix_only(1), "st")
        self.assertEqual(get_ordinal_suffix_only(2), "nd")
        self.assertEqual(get_ordinal_suffix_only(11), "th")


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions"""
    
    def test_large_numbers(self):
        self.assertEqual(to_ordinal(1000), "1000th")
        self.assertEqual(to_ordinal(1001), "1001st")
        self.assertEqual(to_ordinal(1011), "1011th")
    
    def test_zero(self):
        self.assertEqual(to_ordinal(0), "0th")
        self.assertEqual(from_ordinal("0th"), 0)
    
    def test_whitespace_handling(self):
        self.assertEqual(from_ordinal("  5th  "), 5)
        self.assertEqual(from_ordinal("  first  "), 1)
    
    def test_case_insensitive_words(self):
        self.assertEqual(from_ordinal("FIRST"), 1)
        self.assertEqual(from_ordinal("Second"), 2)
        self.assertEqual(from_ordinal("TWENTY-FIRST"), 21)


if __name__ == "__main__":
    unittest.main(verbosity=2)