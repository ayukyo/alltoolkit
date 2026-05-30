# Dial Code Utils Test

import sys
import os
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dial_code_utils.mod import (
    get_country_by_dial_code,
    get_dial_code_by_country,
    get_all_countries,
    get_countries_by_continent,
    format_phone_number,
    validate_phone_number,
    extract_dial_code,
    get_country_name,
    is_valid_dial_code,
    search_countries,
    compare_dial_codes,
    DialCodeUtils,
)


class TestDialCodeLookup(unittest.TestCase):
    """Test dial code lookup functions."""

    def test_get_country_by_dial_code(self):
        """Test getting country by dial code."""
        result = get_country_by_dial_code("86")
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], '中国')
        self.assertEqual(result['code'], 'CN')
    
    def test_get_country_by_dial_code_with_plus(self):
        """Test getting country with + prefix."""
        result = get_country_by_dial_code("+86")
        self.assertIsNotNone(result)
    
    def test_get_country_by_dial_code_us(self):
        """Test US/Canada dial code."""
        result = get_country_by_dial_code("1")
        self.assertIsNotNone(result)
        self.assertIn('美国', result['name'])
    
    def test_get_country_not_found(self):
        """Test dial code not found."""
        result = get_country_by_dial_code("999")
        self.assertIsNone(result)


class TestCountryLookup(unittest.TestCase):
    """Test country lookup functions."""

    def test_get_dial_code_by_country_zh(self):
        """Test getting dial code by Chinese name."""
        self.assertEqual(get_dial_code_by_country("中国"), "86")
        self.assertEqual(get_dial_code_by_country("日本"), "81")
    
    def test_get_dial_code_by_country_code(self):
        """Test getting dial code by ISO code."""
        self.assertEqual(get_dial_code_by_country("CN"), "86")
        self.assertEqual(get_dial_code_by_country("JP"), "81")
        self.assertEqual(get_dial_code_by_country("US"), "1")
    
    def test_get_dial_code_by_country_alpha3(self):
        """Test getting dial code by alpha-3 code."""
        self.assertEqual(get_dial_code_by_country("CHN"), "86")
        self.assertEqual(get_dial_code_by_country("JPN"), "81")
    
    def test_get_dial_code_not_found(self):
        """Test country not found."""
        self.assertIsNone(get_dial_code_by_country(""))


class TestGetAllCountries(unittest.TestCase):
    """Test getting all countries."""

    def test_get_all_countries(self):
        """Test getting all countries list."""
        countries = get_all_countries()
        self.assertIsInstance(countries, list)
        self.assertGreater(len(countries), 200)
    
    def test_get_countries_by_continent(self):
        """Test getting countries by continent."""
        asia = get_countries_by_continent("亚洲")
        self.assertIsInstance(asia, list)
        self.assertTrue(any(c['name'] == '中国' for c in asia))


class TestPhoneFormatting(unittest.TestCase):
    """Test phone number formatting."""

    def test_format_international(self):
        """Test international format."""
        result = format_phone_number("13800138000", "86", "international")
        self.assertIn("+86", result)
        self.assertIn("138", result)
    
    def test_format_e164(self):
        """Test E.164 format."""
        result = format_phone_number("13800138000", "86", "e164")
        self.assertEqual(result, "+8613800138000")
    
    def test_format_local(self):
        """Test local format."""
        result = format_phone_number("13800138000", "86", "local")
        self.assertIn("138", result)
        self.assertIn("-", result)
    
    def test_format_auto_detect(self):
        """Test auto-detecting dial code."""
        result = format_phone_number("+8613800138000", format_type="e164")
        self.assertEqual(result, "+8613800138000")


class TestPhoneValidation(unittest.TestCase):
    """Test phone number validation."""

    def test_validate_valid_china(self):
        """Test validating valid China phone."""
        valid, formatted = validate_phone_number("13800138000", "86")
        self.assertTrue(valid)
        self.assertIn("+86", formatted)
    
    def test_validate_invalid_length(self):
        """Test invalid phone length."""
        valid, msg = validate_phone_number("123", "86")
        self.assertFalse(valid)
    
    def test_validate_empty(self):
        """Test empty phone."""
        valid, msg = validate_phone_number("", "86")
        self.assertFalse(valid)


class TestExtractDialCode(unittest.TestCase):
    """Test extracting dial code from phone."""

    def test_extract_with_plus(self):
        """Test extracting from + prefix."""
        code, local = extract_dial_code("+8613800138000")
        self.assertEqual(code, "86")
        self.assertEqual(local, "13800138000")
    
    def test_extract_with_00(self):
        """Test extracting from 00 prefix."""
        code, local = extract_dial_code("008613800138000")
        self.assertEqual(code, "86")
    
    def test_extract_us(self):
        """Test extracting US dial code."""
        code, local = extract_dial_code("+12125551234")
        self.assertEqual(code, "1")
        self.assertEqual(len(local), 10)


class TestCountryName(unittest.TestCase):
    """Test getting country name."""

    def test_get_country_name_zh(self):
        """Test getting Chinese name."""
        name = get_country_name("86")
        self.assertEqual(name, "中国")
    
    def test_get_country_name_en(self):
        """Test getting English name."""
        name = get_country_name("86", lang="en")
        self.assertIsNotNone(name)


class TestValidation(unittest.TestCase):
    """Test dial code validation."""

    def test_is_valid_dial_code(self):
        """Test validating dial code."""
        self.assertTrue(is_valid_dial_code("86"))
        self.assertTrue(is_valid_dial_code("+86"))
        self.assertFalse(is_valid_dial_code("999"))


class TestSearch(unittest.TestCase):
    """Test country search."""

    def test_search_by_name(self):
        """Test searching by country name."""
        results = search_countries("中国")
        self.assertTrue(len(results) >= 1)
        self.assertEqual(results[0]['name'], '中国')
    
    def test_search_by_dial_code(self):
        """Test searching by dial code."""
        results = search_countries("86")
        self.assertTrue(len(results) >= 1)
    
    def test_search_empty(self):
        """Test empty search query."""
        results = search_countries("")
        self.assertIsInstance(results, list)


class TestCompare(unittest.TestCase):
    """Test comparing dial codes."""

    def test_compare_dial_codes(self):
        """Test comparing two dial codes."""
        result = compare_dial_codes("86", "1")
        self.assertTrue(result['valid'])
        self.assertFalse(result['same_continent'])


class TestDialCodeUtils(unittest.TestCase):
    """Test DialCodeUtils class."""

    def test_get_country(self):
        """Test DialCodeUtils.get_country()."""
        result = DialCodeUtils.get_country("86")
        self.assertIsNotNone(result)
    
    def test_get_dial_code(self):
        """Test DialCodeUtils.get_dial_code()."""
        self.assertEqual(DialCodeUtils.get_dial_code("中国"), "86")
    
    def test_format_phone(self):
        """Test DialCodeUtils.format_phone()."""
        result = DialCodeUtils.format_phone("13800138000", "86")
        self.assertIn("+86", result)


if __name__ == '__main__':
    unittest.main()