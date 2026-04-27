#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Number Words Utilities Tests
==========================================
Comprehensive test suite for the number-words utilities module.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    number_to_words,
    words_to_number,
    number_to_currency_words,
    is_valid_number_word,
    get_number_words_list,
    to_words,
    from_words,
    Language,
    NumberWordsError,
    UnsupportedLanguageError,
    InvalidNumberError,
    InvalidWordError,
)


class TestNumberToWordsEnglish(unittest.TestCase):
    """Tests for English number to words conversion."""
    
    def test_zero(self):
        self.assertEqual(number_to_words(0), "zero")
    
    def test_ones(self):
        self.assertEqual(number_to_words(1), "one")
        self.assertEqual(number_to_words(5), "five")
        self.assertEqual(number_to_words(9), "nine")
    
    def test_teens(self):
        self.assertEqual(number_to_words(10), "ten")
        self.assertEqual(number_to_words(11), "eleven")
        self.assertEqual(number_to_words(15), "fifteen")
        self.assertEqual(number_to_words(19), "nineteen")
    
    def test_tens(self):
        self.assertEqual(number_to_words(20), "twenty")
        self.assertEqual(number_to_words(30), "thirty")
        self.assertEqual(number_to_words(90), "ninety")
    
    def test_tens_with_ones(self):
        self.assertEqual(number_to_words(21), "twenty-one")
        self.assertEqual(number_to_words(42), "forty-two")
        self.assertEqual(number_to_words(99), "ninety-nine")
    
    def test_hundreds(self):
        self.assertEqual(number_to_words(100), "one hundred")
        self.assertEqual(number_to_words(200), "two hundred")
        self.assertEqual(number_to_words(500), "five hundred")
    
    def test_hundreds_with_remainder(self):
        self.assertEqual(number_to_words(101), "one hundred one")
        self.assertEqual(number_to_words(123), "one hundred twenty-three")
        self.assertEqual(number_to_words(999), "nine hundred ninety-nine")
    
    def test_thousands(self):
        self.assertEqual(number_to_words(1000), "one thousand")
        self.assertEqual(number_to_words(2000), "two thousand")
        self.assertEqual(number_to_words(10000), "ten thousand")
        self.assertEqual(number_to_words(100000), "one hundred thousand")
    
    def test_large_numbers(self):
        self.assertEqual(number_to_words(1000000), "one million")
        self.assertEqual(number_to_words(1000000000), "one billion")
        self.assertEqual(number_to_words(1000000000000), "one trillion")
    
    def test_complex_numbers(self):
        self.assertEqual(
            number_to_words(123456789),
            "one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine"
        )
        self.assertEqual(
            number_to_words(1234567),
            "one million two hundred thirty-four thousand five hundred sixty-seven"
        )
    
    def test_negative_numbers(self):
        self.assertEqual(number_to_words(-1), "minus one")
        self.assertEqual(number_to_words(-42), "minus forty-two")
        self.assertEqual(number_to_words(-100), "minus one hundred")
    
    def test_floats(self):
        self.assertEqual(number_to_words(1.5), "one point five")
        self.assertEqual(number_to_words(123.45), "one hundred twenty-three point four five")
        self.assertEqual(number_to_words(0.5), "zero point five")
    
    def test_ordinal_simple(self):
        self.assertEqual(number_to_words(1, ordinal=True), "first")
        self.assertEqual(number_to_words(2, ordinal=True), "second")
        self.assertEqual(number_to_words(3, ordinal=True), "third")
        self.assertEqual(number_to_words(4, ordinal=True), "fourth")
        self.assertEqual(number_to_words(11, ordinal=True), "eleventh")
        self.assertEqual(number_to_words(12, ordinal=True), "twelfth")
    
    def test_ordinal_tens(self):
        self.assertEqual(number_to_words(20, ordinal=True), "twentieth")
        self.assertEqual(number_to_words(21, ordinal=True), "twenty-first")
        self.assertEqual(number_to_words(22, ordinal=True), "twenty-second")
        self.assertEqual(number_to_words(30, ordinal=True), "thirtieth")


class TestNumberToWordsChinese(unittest.TestCase):
    """Tests for Chinese number to words conversion."""
    
    def test_zero(self):
        self.assertEqual(number_to_words(0, Language.CHINESE), "零")
    
    def test_ones(self):
        self.assertEqual(number_to_words(1, Language.CHINESE), "一")
        self.assertEqual(number_to_words(5, Language.CHINESE), "五")
        self.assertEqual(number_to_words(9, Language.CHINESE), "九")
    
    def test_teens_and_tens(self):
        self.assertEqual(number_to_words(10, Language.CHINESE), "十")
        self.assertEqual(number_to_words(11, Language.CHINESE), "十一")
        self.assertEqual(number_to_words(20, Language.CHINESE), "二十")
        self.assertEqual(number_to_words(21, Language.CHINESE), "二十一")
    
    def test_hundreds(self):
        self.assertEqual(number_to_words(100, Language.CHINESE), "一百")
        self.assertEqual(number_to_words(101, Language.CHINESE), "一百零一")
        self.assertEqual(number_to_words(123, Language.CHINESE), "一百二十三")
    
    def test_thousands(self):
        self.assertEqual(number_to_words(1000, Language.CHINESE), "一千")
        self.assertEqual(number_to_words(1234, Language.CHINESE), "一千二百三十四")
    
    def test_ten_thousands(self):
        self.assertEqual(number_to_words(10000, Language.CHINESE), "一万")
        self.assertEqual(number_to_words(12345, Language.CHINESE), "一万二千三百四十五")
        self.assertEqual(number_to_words(100000, Language.CHINESE), "十万")
        self.assertEqual(number_to_words(1000000, Language.CHINESE), "一百万")
    
    def test_hundred_millions(self):
        self.assertEqual(number_to_words(100000000, Language.CHINESE), "一亿")
        self.assertEqual(number_to_words(123456789, Language.CHINESE), "一亿二千三百四十五万六千七百八十九")
    
    def test_negative(self):
        self.assertEqual(number_to_words(-1, Language.CHINESE), "负一")
        self.assertEqual(number_to_words(-100, Language.CHINESE), "负一百")
    
    def test_floats(self):
        self.assertEqual(number_to_words(1.5, Language.CHINESE), "一点五")
        self.assertEqual(number_to_words(123.45, Language.CHINESE), "一百二十三点四五")
    
    def test_ordinal(self):
        self.assertEqual(number_to_words(1, Language.CHINESE, ordinal=True), "第一")
        self.assertEqual(number_to_words(123, Language.CHINESE, ordinal=True), "第一百二十三")


class TestWordsToNumberEnglish(unittest.TestCase):
    """Tests for English words to number conversion."""
    
    def test_zero(self):
        self.assertEqual(words_to_number("zero"), 0)
    
    def test_ones(self):
        self.assertEqual(words_to_number("one"), 1)
        self.assertEqual(words_to_number("five"), 5)
        self.assertEqual(words_to_number("nine"), 9)
    
    def test_teens(self):
        self.assertEqual(words_to_number("ten"), 10)
        self.assertEqual(words_to_number("eleven"), 11)
        self.assertEqual(words_to_number("nineteen"), 19)
    
    def test_tens(self):
        self.assertEqual(words_to_number("twenty"), 20)
        self.assertEqual(words_to_number("thirty"), 30)
        self.assertEqual(words_to_number("ninety"), 90)
    
    def test_tens_with_ones(self):
        self.assertEqual(words_to_number("twenty-one"), 21)
        self.assertEqual(words_to_number("forty-two"), 42)
        self.assertEqual(words_to_number("ninety-nine"), 99)
        # Also test with space
        self.assertEqual(words_to_number("twenty one"), 21)
    
    def test_hundreds(self):
        self.assertEqual(words_to_number("one hundred"), 100)
        self.assertEqual(words_to_number("two hundred"), 200)
        self.assertEqual(words_to_number("one hundred twenty-three"), 123)
    
    def test_thousands(self):
        self.assertEqual(words_to_number("one thousand"), 1000)
        self.assertEqual(words_to_number("two thousand"), 2000)
        self.assertEqual(words_to_number("one thousand two hundred thirty-four"), 1234)
    
    def test_millions(self):
        self.assertEqual(words_to_number("one million"), 1000000)
        self.assertEqual(words_to_number("two million three hundred thousand"), 2300000)
    
    def test_complex(self):
        self.assertEqual(
            words_to_number("one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine"),
            123456789
        )
    
    def test_negative(self):
        self.assertEqual(words_to_number("minus one"), -1)
        self.assertEqual(words_to_number("negative ten"), -10)
    
    def test_decimals(self):
        self.assertEqual(words_to_number("one point five"), 1.5)
        self.assertEqual(words_to_number("one hundred twenty-three point four five"), 123.45)
    
    def test_ordinals(self):
        self.assertEqual(words_to_number("first"), 1)
        self.assertEqual(words_to_number("second"), 2)
        self.assertEqual(words_to_number("third"), 3)
        self.assertEqual(words_to_number("tenth"), 10)
    
    def test_with_and(self):
        self.assertEqual(words_to_number("one hundred and twenty-three"), 123)
        self.assertEqual(words_to_number("one thousand and one"), 1001)


class TestWordsToNumberChinese(unittest.TestCase):
    """Tests for Chinese words to number conversion."""
    
    def test_zero(self):
        self.assertEqual(words_to_number("零", Language.CHINESE), 0)
    
    def test_ones(self):
        self.assertEqual(words_to_number("一", Language.CHINESE), 1)
        self.assertEqual(words_to_number("五", Language.CHINESE), 5)
        self.assertEqual(words_to_number("九", Language.CHINESE), 9)
    
    def test_teens_and_tens(self):
        self.assertEqual(words_to_number("十", Language.CHINESE), 10)
        self.assertEqual(words_to_number("十一", Language.CHINESE), 11)
        self.assertEqual(words_to_number("二十", Language.CHINESE), 20)
        self.assertEqual(words_to_number("二十一", Language.CHINESE), 21)
    
    def test_hundreds(self):
        self.assertEqual(words_to_number("一百", Language.CHINESE), 100)
        self.assertEqual(words_to_number("一百二十三", Language.CHINESE), 123)
    
    def test_thousands(self):
        self.assertEqual(words_to_number("一千", Language.CHINESE), 1000)
        self.assertEqual(words_to_number("一千二百三十四", Language.CHINESE), 1234)
    
    def test_ten_thousands(self):
        self.assertEqual(words_to_number("一万", Language.CHINESE), 10000)
        self.assertEqual(words_to_number("一万二千三百四十五", Language.CHINESE), 12345)
    
    def test_hundred_millions(self):
        self.assertEqual(words_to_number("一亿", Language.CHINESE), 100000000)
    
    def test_negative(self):
        self.assertEqual(words_to_number("负一", Language.CHINESE), -1)
        self.assertEqual(words_to_number("负一百", Language.CHINESE), -100)
    
    def test_decimals(self):
        self.assertEqual(words_to_number("一点五", Language.CHINESE), 1.5)
    
    def test_ordinal(self):
        self.assertEqual(words_to_number("第一", Language.CHINESE), 1)
        self.assertEqual(words_to_number("第一百二十三", Language.CHINESE), 123)
    
    def test_alternative_two(self):
        self.assertEqual(words_to_number("两", Language.CHINESE), 2)


class TestCurrencyWords(unittest.TestCase):
    """Tests for currency to words conversion."""
    
    def test_usd_integer(self):
        result = number_to_currency_words(100, "USD")
        self.assertIn("one hundred", result)
        self.assertIn("dollars", result)
    
    def test_usd_decimal(self):
        result = number_to_currency_words(123.45, "USD")
        self.assertIn("one hundred twenty-three dollars", result)
        self.assertIn("forty-five cents", result)
    
    def test_usd_singular(self):
        result = number_to_currency_words(1, "USD")
        self.assertIn("one dollar", result)
        self.assertNotIn("dollars", result)
    
    def test_eur(self):
        result = number_to_currency_words(100, "EUR")
        self.assertIn("one hundred", result)
        self.assertIn("euros", result)
    
    def test_gbp(self):
        result = number_to_currency_words(100, "GBP")
        self.assertIn("one hundred", result)
        self.assertIn("pounds", result)
    
    def test_cny(self):
        result = number_to_currency_words(100, "CNY")
        self.assertIn("one hundred", result)
        self.assertIn("yuan", result)
    
    def test_jpy(self):
        result = number_to_currency_words(100, "JPY")
        self.assertIn("one hundred", result)
        self.assertIn("yen", result)
    
    def test_chinese_currency(self):
        result = number_to_currency_words(123.45, "CNY", Language.CHINESE)
        self.assertIn("一百二十三", result)
        self.assertIn("元", result)


class TestUtilityFunctions(unittest.TestCase):
    """Tests for utility functions."""
    
    def test_is_valid_number_word_english(self):
        self.assertTrue(is_valid_number_word("one"))
        self.assertTrue(is_valid_number_word("hundred"))
        self.assertTrue(is_valid_number_word("million"))
        self.assertTrue(is_valid_number_word("first"))
        self.assertTrue(is_valid_number_word("and"))
        self.assertTrue(is_valid_number_word("point"))
        self.assertFalse(is_valid_number_word("hello"))
        self.assertFalse(is_valid_number_word("world"))
    
    def test_is_valid_number_word_chinese(self):
        self.assertTrue(is_valid_number_word("一", Language.CHINESE))
        self.assertTrue(is_valid_number_word("百", Language.CHINESE))
        self.assertTrue(is_valid_number_word("万", Language.CHINESE))
        self.assertFalse(is_valid_number_word("你好", Language.CHINESE))
    
    def test_get_number_words_list_english(self):
        words = get_number_words_list(Language.ENGLISH)
        self.assertIn("one", words)
        self.assertIn("hundred", words)
        self.assertIn("million", words)
        self.assertIn("zero", words)
    
    def test_get_number_words_list_chinese(self):
        words = get_number_words_list(Language.CHINESE)
        self.assertIn("一", words)
        self.assertIn("百", words)
        self.assertIn("万", words)
    
    def test_convenience_aliases(self):
        self.assertEqual(to_words(123), "one hundred twenty-three")
        self.assertEqual(to_words(123, "zh"), "一百二十三")
        self.assertEqual(from_words("one hundred twenty-three"), 123)
        self.assertEqual(from_words("一百二十三", "zh"), 123)


class TestRoundTrip(unittest.TestCase):
    """Tests for round-trip conversion (number → words → number)."""
    
    def test_round_trip_english(self):
        test_numbers = [0, 1, 10, 42, 100, 123, 1000, 1234, 10000, 12345, 100000, 1000000]
        for num in test_numbers:
            words = number_to_words(num)
            result = words_to_number(words)
            self.assertEqual(result, num, f"Round trip failed for {num}: got {words} → {result}")
    
    def test_round_trip_chinese(self):
        test_numbers = [0, 1, 10, 42, 100, 123, 1000, 1234, 10000, 12345]
        for num in test_numbers:
            words = number_to_words(num, Language.CHINESE)
            result = words_to_number(words, Language.CHINESE)
            self.assertEqual(result, num, f"Round trip failed for {num}: got {words} → {result}")


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""
    
    def test_large_number(self):
        words = number_to_words(10**15)  # Quadrillion
        self.assertIn("quadrillion", words)
    
    def test_quintillion(self):
        words = number_to_words(10**18)  # Quintillion
        self.assertIn("quintillion", words)
    
    def test_float_precision(self):
        words = number_to_words(3.14159)
        self.assertIn("three", words)
        self.assertIn("point", words)
    
    def test_zero_with_ordinal(self):
        self.assertEqual(number_to_words(0, ordinal=True), "zeroth")
    
    def test_negative_with_ordinal(self):
        result = number_to_words(-1, ordinal=True)
        self.assertIn("minus", result)
    
    def test_invalid_language(self):
        with self.assertRaises((UnsupportedLanguageError, ValueError)):
            number_to_words(123, Language("invalid"))


if __name__ == "__main__":
    unittest.main(verbosity=2)