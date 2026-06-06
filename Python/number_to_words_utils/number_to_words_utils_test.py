"""
Tests for number_to_words_utils

Comprehensive test suite covering all supported languages and edge cases.
"""

import unittest
from decimal import Decimal
from number_to_words_utils.converter import (
    number_to_words,
    number_to_currency_words,
    number_to_ordinal_words,
    get_supported_languages,
)


class TestSupportedLanguages(unittest.TestCase):
    """Test language support."""
    
    def test_get_supported_languages(self):
        """Test that supported languages are returned."""
        languages = get_supported_languages()
        self.assertIsInstance(languages, list)
        self.assertIn("en", languages)
        self.assertIn("zh", languages)
        self.assertIn("ja", languages)
        self.assertIn("ko", languages)
        self.assertIn("es", languages)
        self.assertIn("fr", languages)
        self.assertIn("de", languages)
    
    def test_invalid_language(self):
        """Test that invalid language raises error."""
        with self.assertRaises(ValueError):
            number_to_words(42, lang="invalid")


class TestEnglish(unittest.TestCase):
    """Test English number conversion."""
    
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
        self.assertEqual(number_to_words(42), "forty-two")
        self.assertEqual(number_to_words(99), "ninety-nine")
    
    def test_hundreds(self):
        self.assertEqual(number_to_words(100), "one hundred")
        self.assertEqual(number_to_words(101), "one hundred and one")
        self.assertEqual(number_to_words(500), "five hundred")
        self.assertEqual(number_to_words(999), "nine hundred and ninety-nine")
    
    def test_thousands(self):
        self.assertEqual(number_to_words(1000), "one thousand")
        self.assertEqual(number_to_words(1234), "one thousand two hundred and thirty-four")
        self.assertEqual(number_to_words(10000), "ten thousand")
        self.assertEqual(number_to_words(100000), "one hundred thousand")
        self.assertEqual(number_to_words(1000000), "one million")
    
    def test_large_numbers(self):
        self.assertEqual(number_to_words(1000000000), "one billion")
        self.assertEqual(number_to_words(1000000000000), "one trillion")
    
    def test_negative(self):
        self.assertEqual(number_to_words(-1), "negative one")
        self.assertEqual(number_to_words(-42), "negative forty-two")
    
    def test_decimals(self):
        self.assertEqual(number_to_words(1.5), "one point five")
        self.assertEqual(number_to_words(3.14159), "three point one four one five nine")
    
    def test_string_input(self):
        self.assertEqual(number_to_words("42"), "forty-two")
        self.assertEqual(number_to_words("-10"), "negative ten")
    
    def test_decimal_input(self):
        self.assertEqual(number_to_words(Decimal("42.5")), "forty-two point five")


class TestEnglishOrdinal(unittest.TestCase):
    """Test English ordinal conversion."""
    
    def test_basic_ordinals(self):
        self.assertEqual(number_to_ordinal_words(1), "first")
        self.assertEqual(number_to_ordinal_words(2), "second")
        self.assertEqual(number_to_ordinal_words(3), "third")
        self.assertEqual(number_to_ordinal_words(4), "fourth")
        self.assertEqual(number_to_ordinal_words(5), "fifth")
        self.assertEqual(number_to_ordinal_words(12), "twelfth")
    
    def test_tens_ordinals(self):
        self.assertEqual(number_to_ordinal_words(20), "twentieth")
        self.assertEqual(number_to_ordinal_words(21), "twenty-first")
        self.assertEqual(number_to_ordinal_words(22), "twenty-second")
        self.assertEqual(number_to_ordinal_words(33), "thirty-third")
    
    def test_hundreds_ordinals(self):
        self.assertEqual(number_to_ordinal_words(100), "one hundredth")
        self.assertEqual(number_to_ordinal_words(101), "one hundred first")
    
    def test_negative_ordinal(self):
        self.assertEqual(number_to_ordinal_words(-1), "negative first")


class TestEnglishCurrency(unittest.TestCase):
    """Test English currency conversion."""
    
    def test_simple_currency(self):
        result = number_to_currency_words(1)
        self.assertIn("dollar", result)
    
    def test_plural_currency(self):
        result = number_to_currency_words(5)
        self.assertIn("dollars", result)
    
    def test_cents(self):
        result = number_to_currency_words(0.50)
        self.assertIn("fifty", result.lower())
        self.assertIn("cent", result.lower())
    
    def test_mixed(self):
        result = number_to_currency_words(42.50)
        self.assertIn("forty-two", result)
        self.assertIn("fifty", result.lower())


class TestChinese(unittest.TestCase):
    """Test Chinese number conversion."""
    
    def test_zero(self):
        self.assertEqual(number_to_words(0, lang="zh"), "零")
    
    def test_ones(self):
        self.assertEqual(number_to_words(1, lang="zh"), "一")
        self.assertEqual(number_to_words(5, lang="zh"), "五")
        self.assertEqual(number_to_words(9, lang="zh"), "九")
    
    def test_teens(self):
        self.assertEqual(number_to_words(10, lang="zh"), "十")
        self.assertEqual(number_to_words(11, lang="zh"), "十一")
        self.assertEqual(number_to_words(15, lang="zh"), "十五")
        self.assertEqual(number_to_words(19, lang="zh"), "十九")
    
    def test_tens(self):
        self.assertEqual(number_to_words(20, lang="zh"), "二十")
        self.assertEqual(number_to_words(42, lang="zh"), "四十二")
        self.assertEqual(number_to_words(99, lang="zh"), "九十九")
    
    def test_hundreds(self):
        self.assertEqual(number_to_words(100, lang="zh"), "一百")
        self.assertEqual(number_to_words(101, lang="zh"), "一百零一")
        self.assertEqual(number_to_words(500, lang="zh"), "五百")
        self.assertEqual(number_to_words(999, lang="zh"), "九百九十九")
    
    def test_thousands(self):
        self.assertEqual(number_to_words(1000, lang="zh"), "一千")
        self.assertEqual(number_to_words(10000, lang="zh"), "一万")
        self.assertEqual(number_to_words(100000, lang="zh"), "十万")
        self.assertEqual(number_to_words(1000000, lang="zh"), "一百万")
    
    def test_scales(self):
        self.assertEqual(number_to_words(100000000, lang="zh"), "一亿")
    
    def test_negative(self):
        self.assertEqual(number_to_words(-1, lang="zh"), "负一")
    
    def test_decimals(self):
        self.assertEqual(number_to_words(1.5, lang="zh"), "一点五")
    
    def test_ordinal(self):
        self.assertEqual(number_to_ordinal_words(1, lang="zh"), "第一")
        self.assertEqual(number_to_ordinal_words(10, lang="zh"), "第十")


class TestChineseCurrency(unittest.TestCase):
    """Test Chinese currency (人民币大写) conversion."""
    
    def test_simple_currency(self):
        result = number_to_currency_words(1, lang="zh")
        self.assertIn("壹", result)
        self.assertIn("元", result)
    
    def test_larger_amount(self):
        result = number_to_currency_words(100, lang="zh")
        self.assertIn("壹佰", result)
    
    def test_with_jiao(self):
        result = number_to_currency_words(1.5, lang="zh")
        self.assertIn("伍角", result)


class TestJapanese(unittest.TestCase):
    """Test Japanese number conversion."""
    
    def test_zero(self):
        self.assertEqual(number_to_words(0, lang="ja"), "零")
    
    def test_ones(self):
        self.assertEqual(number_to_words(1, lang="ja"), "一")
        self.assertEqual(number_to_words(5, lang="ja"), "五")
    
    def test_tens(self):
        self.assertEqual(number_to_words(10, lang="ja"), "十")
        self.assertEqual(number_to_words(20, lang="ja"), "二十")
        self.assertEqual(number_to_words(42, lang="ja"), "四十二")
    
    def test_hundreds_thousands(self):
        self.assertEqual(number_to_words(100, lang="ja"), "百")
        self.assertEqual(number_to_words(1000, lang="ja"), "千")
        self.assertEqual(number_to_words(10000, lang="ja"), "一万")


class TestKorean(unittest.TestCase):
    """Test Korean number conversion."""
    
    def test_zero(self):
        self.assertEqual(number_to_words(0, lang="ko"), "영")
    
    def test_small_numbers(self):
        self.assertEqual(number_to_words(1, lang="ko"), "일")
        self.assertEqual(number_to_words(5, lang="ko"), "오")
    
    def test_tens(self):
        self.assertEqual(number_to_words(10, lang="ko"), "십")
        self.assertEqual(number_to_words(42, lang="ko"), "사십이")
    
    def test_large_numbers(self):
        self.assertEqual(number_to_words(100, lang="ko"), "백")
        self.assertEqual(number_to_words(1000, lang="ko"), "천")
        self.assertEqual(number_to_words(10000, lang="ko"), "일만")


class TestSpanish(unittest.TestCase):
    """Test Spanish number conversion."""
    
    def test_zero(self):
        self.assertEqual(number_to_words(0, lang="es"), "cero")
    
    def test_ones(self):
        self.assertEqual(number_to_words(1, lang="es"), "uno")
        self.assertEqual(number_to_words(5, lang="es"), "cinco")
    
    def test_teens(self):
        self.assertEqual(number_to_words(10, lang="es"), "diez")
        self.assertEqual(number_to_words(15, lang="es"), "quince")
        self.assertEqual(number_to_words(19, lang="es"), "diecinueve")
    
    def test_twenties(self):
        self.assertEqual(number_to_words(20, lang="es"), "veinte")
        self.assertEqual(number_to_words(21, lang="es"), "veintiuno")
        self.assertEqual(number_to_words(25, lang="es"), "veinticinco")
    
    def test_tens(self):
        self.assertEqual(number_to_words(30, lang="es"), "treinta")
        self.assertEqual(number_to_words(42, lang="es"), "cuarenta y dos")
    
    def test_hundreds(self):
        self.assertEqual(number_to_words(100, lang="es"), "cien")
        self.assertEqual(number_to_words(101, lang="es"), "ciento uno")
        self.assertEqual(number_to_words(500, lang="es"), "quinientos")


class TestFrench(unittest.TestCase):
    """Test French number conversion."""
    
    def test_zero(self):
        self.assertEqual(number_to_words(0, lang="fr"), "zéro")
    
    def test_ones(self):
        self.assertEqual(number_to_words(1, lang="fr"), "un")
        self.assertEqual(number_to_words(5, lang="fr"), "cinq")
    
    def test_teens(self):
        self.assertEqual(number_to_words(10, lang="fr"), "dix")
        self.assertEqual(number_to_words(15, lang="fr"), "quinze")
        self.assertEqual(number_to_words(17, lang="fr"), "dix-sept")
    
    def test_special_tens(self):
        self.assertEqual(number_to_words(70, lang="fr"), "soixante-dix")
        self.assertEqual(number_to_words(71, lang="fr"), "soixante et onze")
        self.assertEqual(number_to_words(80, lang="fr"), "quatre-vingts")
        self.assertEqual(number_to_words(90, lang="fr"), "quatre-vingt-dix")
    
    def test_hundreds_thousands(self):
        self.assertEqual(number_to_words(100, lang="fr"), "cent")
        self.assertEqual(number_to_words(1000, lang="fr"), "mille")


class TestGerman(unittest.TestCase):
    """Test German number conversion."""
    
    def test_zero(self):
        self.assertEqual(number_to_words(0, lang="de"), "null")
    
    def test_ones(self):
        self.assertEqual(number_to_words(1, lang="de"), "eins")
        self.assertEqual(number_to_words(5, lang="de"), "fünf")
    
    def test_teens(self):
        self.assertEqual(number_to_words(10, lang="de"), "zehn")
        self.assertEqual(number_to_words(15, lang="de"), "fünfzehn")
    
    def test_tens(self):
        # German writes ones before tens
        self.assertEqual(number_to_words(20, lang="de"), "zwanzig")
        self.assertEqual(number_to_words(21, lang="de"), "einundzwanzig")
        self.assertEqual(number_to_words(42, lang="de"), "zweiundvierzig")
    
    def test_compound_words(self):
        # German uses compound words
        result = number_to_words(123, lang="de")
        self.assertIn("hundert", result)
        self.assertIn("dreiundzwanzig", result)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_large_number(self):
        """Test that very large numbers raise an error."""
        with self.assertRaises(ValueError):
            number_to_words(10**40)
    
    def test_infinity(self):
        """Test that infinity raises an error."""
        with self.assertRaises(ValueError):
            number_to_words(float("inf"))
    
    def test_nan(self):
        """Test that NaN raises an error."""
        with self.assertRaises(ValueError):
            number_to_words(float("nan"))
    
    def test_invalid_string(self):
        """Test that invalid string raises an error."""
        with self.assertRaises(ValueError):
            number_to_words("not a number")
    
    def test_ordinal_with_decimal(self):
        """Test that ordinal with decimal raises an error."""
        with self.assertRaises(ValueError):
            number_to_ordinal_words(1.5)
    
    def test_positive_string(self):
        """Test string with explicit positive sign."""
        self.assertEqual(number_to_words("+42"), "forty-two")
    
    def test_whitespace_in_string(self):
        """Test string with leading/trailing whitespace."""
        self.assertEqual(number_to_words("  42  "), "forty-two")


class TestMultilingualComparison(unittest.TestCase):
    """Compare the same number across different languages."""
    
    def test_42(self):
        """Test number 42 in all supported languages."""
        self.assertEqual(number_to_words(42, "en"), "forty-two")
        self.assertEqual(number_to_words(42, "zh"), "四十二")
        self.assertEqual(number_to_words(42, "ja"), "四十二")
        self.assertEqual(number_to_words(42, "ko"), "사십이")
        self.assertIn("cuarenta", number_to_words(42, "es"))  # cuarenta y dos
        self.assertIn("quarante", number_to_words(42, "fr"))  # quarante-deux
        self.assertIn("zweiundvierzig", number_to_words(42, "de"))
    
    def test_100(self):
        """Test number 100 in all supported languages."""
        self.assertEqual(number_to_words(100, "en"), "one hundred")
        self.assertEqual(number_to_words(100, "zh"), "一百")
        self.assertEqual(number_to_words(100, "ja"), "百")
        self.assertEqual(number_to_words(100, "ko"), "백")
        self.assertEqual(number_to_words(100, "es"), "cien")
        self.assertEqual(number_to_words(100, "fr"), "cent")
        self.assertIn("hundert", number_to_words(100, "de"))


if __name__ == "__main__":
    unittest.main(verbosity=2)