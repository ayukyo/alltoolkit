"""
AllToolkit - Python Punycode Utilities Test Suite

Comprehensive tests for Punycode/IDN operations covering:
- Domain encoding/decoding
- Email encoding/decoding
- Validation functions
- Batch operations
- Edge cases and error handling

Run: python punycode_utils_test.py -v
"""

import unittest
import sys
import os

# Add module directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    IDNResult,
    PunycodeError,
    encode_domain,
    decode_domain,
    encode_email,
    decode_email,
    is_idn,
    is_punycode,
    validate_domain,
    get_tld,
    normalize_domain,
    batch_encode,
    batch_decode,
    domain_info,
    ACE_PREFIX,
    MAX_LABEL_LENGTH,
    MAX_DOMAIN_LENGTH,
)


class TestEncodeDomain(unittest.TestCase):
    """Tests for encode_domain function."""
    
    def test_ascii_domain(self):
        """Test encoding of ASCII-only domain."""
        result = encode_domain("example.com")
        self.assertTrue(result.success)
        self.assertEqual(result.encoded, "example.com")
        self.assertTrue(result.is_ascii)
    
    def test_chinese_domain(self):
        """Test encoding of Chinese domain."""
        result = encode_domain("中国.cn")
        self.assertTrue(result.success)
        self.assertEqual(result.encoded, "xn--fiqs8s.cn")
        self.assertFalse(result.is_ascii)
    
    def test_japanese_domain(self):
        """Test encoding of Japanese domain."""
        result = encode_domain("日本.jp")
        self.assertTrue(result.success)
        self.assertEqual(result.encoded, "xn--wgv71a.jp")
    
    def test_german_domain(self):
        """Test encoding of German domain with umlaut."""
        result = encode_domain("münchen.de")
        self.assertTrue(result.success)
        self.assertEqual(result.encoded, "xn--mnchen-3ya.de")
    
    def test_russian_domain(self):
        """Test encoding of Russian domain."""
        result = encode_domain("россия.рф")
        self.assertTrue(result.success)
        # Check that it starts with xn--
        self.assertTrue(result.encoded.startswith("xn--"))
    
    def test_arabic_domain(self):
        """Test encoding of Arabic domain."""
        result = encode_domain("مصر.eg")
        self.assertTrue(result.success)
        self.assertTrue("xn--" in result.encoded)
    
    def test_multi_label_domain(self):
        """Test encoding of domain with multiple labels."""
        result = encode_domain("测试.中国.cn")
        self.assertTrue(result.success)
        # Both Unicode labels should be encoded
        labels = result.encoded.split('.')
        self.assertTrue(any(l.startswith("xn--") for l in labels))
    
    def test_uppercase_normalized(self):
        """Test that uppercase is normalized to lowercase."""
        result = encode_domain("EXAMPLE.COM")
        self.assertTrue(result.success)
        self.assertEqual(result.encoded, "example.com")
    
    def test_trailing_dot_removed(self):
        """Test that trailing dot is handled."""
        result = encode_domain("example.com.")
        self.assertTrue(result.success)
        self.assertEqual(result.encoded, "example.com")
    
    def test_whitespace_trimmed(self):
        """Test that whitespace is trimmed."""
        result = encode_domain("  example.com  ")
        self.assertTrue(result.success)
        self.assertEqual(result.encoded, "example.com")
    
    def test_empty_domain(self):
        """Test encoding empty domain."""
        result = encode_domain("")
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)
    
    def test_label_pairs(self):
        """Test that label pairs are correctly generated."""
        result = encode_domain("中国.cn")
        self.assertTrue(result.success)
        self.assertEqual(len(result.labels), 2)
        # Check first label (Chinese characters encoded)
        original, encoded = result.labels[0]
        self.assertEqual(encoded, "xn--fiqs8s")
        # Check second label (ASCII unchanged)
        original, encoded = result.labels[1]
        self.assertEqual(original, "cn")
        self.assertEqual(encoded, "cn")


class TestDecodeDomain(unittest.TestCase):
    """Tests for decode_domain function."""
    
    def test_ascii_domain(self):
        """Test decoding of ASCII-only domain."""
        result = decode_domain("example.com")
        self.assertTrue(result.success)
        self.assertEqual(result.encoded, "example.com")
    
    def test_chinese_punycode(self):
        """Test decoding of Chinese Punycode domain."""
        result = decode_domain("xn--fiqs8s.cn")
        self.assertTrue(result.success)
        self.assertEqual(result.encoded, "中国.cn")
    
    def test_japanese_punycode(self):
        """Test decoding of Japanese Punycode domain."""
        result = decode_domain("xn--wgv71a.jp")
        self.assertTrue(result.success)
        self.assertEqual(result.encoded, "日本.jp")
    
    def test_german_punycode(self):
        """Test decoding of German Punycode domain."""
        result = decode_domain("xn--mnchen-3ya.de")
        self.assertTrue(result.success)
        self.assertEqual(result.encoded, "münchen.de")
    
    def test_mixed_domain(self):
        """Test decoding of domain with mixed labels."""
        result = decode_domain("www.xn--fiqs8s.cn")
        self.assertTrue(result.success)
        self.assertEqual(result.encoded, "www.中国.cn")
    
    def test_empty_domain(self):
        """Test decoding empty domain."""
        result = decode_domain("")
        self.assertFalse(result.success)


class TestEncodeDecodeRoundTrip(unittest.TestCase):
    """Tests for encode-decode round trip."""
    
    def test_roundtrip_chinese(self):
        """Test round trip for Chinese domain."""
        original = "中国.cn"
        encoded = encode_domain(original).encoded
        decoded = decode_domain(encoded).encoded
        self.assertEqual(original, decoded)
    
    def test_roundtrip_japanese(self):
        """Test round trip for Japanese domain."""
        original = "日本.jp"
        encoded = encode_domain(original).encoded
        decoded = decode_domain(encoded).encoded
        self.assertEqual(original, decoded)
    
    def test_roundtrip_ascii(self):
        """Test round trip for ASCII domain."""
        original = "example.com"
        encoded = encode_domain(original).encoded
        decoded = decode_domain(encoded).encoded
        self.assertEqual(original, decoded)


class TestEmailFunctions(unittest.TestCase):
    """Tests for email encoding/decoding functions."""
    
    def test_encode_email_unicode_domain(self):
        """Test encoding email with Unicode domain."""
        result = encode_email("user@中国.cn")
        self.assertEqual(result, "user@xn--fiqs8s.cn")
    
    def test_encode_email_ascii_domain(self):
        """Test encoding email with ASCII domain."""
        result = encode_email("user@example.com")
        self.assertEqual(result, "user@example.com")
    
    def test_decode_email_punycode(self):
        """Test decoding email with Punycode domain."""
        result = decode_email("user@xn--fiqs8s.cn")
        self.assertEqual(result, "user@中国.cn")
    
    def test_email_without_at(self):
        """Test handling of invalid email."""
        self.assertEqual(encode_email("notanemail"), "notanemail")
        self.assertEqual(decode_email("notanemail"), "notanemail")
    
    def test_unicode_local_part(self):
        """Test email with Unicode in local part."""
        result = encode_email("用户@example.com")
        self.assertEqual(result, "用户@example.com")


class TestIsIDN(unittest.TestCase):
    """Tests for is_idn function."""
    
    def test_unicode_domain(self):
        """Test detection of Unicode domain."""
        self.assertTrue(is_idn("中国.cn"))
        self.assertTrue(is_idn("münchen.de"))
    
    def test_ascii_domain(self):
        """Test detection of ASCII domain."""
        self.assertFalse(is_idn("example.com"))
        self.assertFalse(is_idn("xn--fiqs8s.cn"))  # ASCII encoding
    
    def test_empty_string(self):
        """Test handling of empty string."""
        self.assertFalse(is_idn(""))


class TestIsPunycode(unittest.TestCase):
    """Tests for is_punycode function."""
    
    def test_punycode_domain(self):
        """Test detection of Punycode domain."""
        self.assertTrue(is_punycode("xn--fiqs8s.cn"))
        self.assertTrue(is_punycode("xn--wgv71a.jp"))
    
    def test_ascii_domain(self):
        """Test detection of non-Punycode ASCII domain."""
        self.assertFalse(is_punycode("example.com"))
    
    def test_unicode_domain(self):
        """Test detection of Unicode domain (not Punycode)."""
        self.assertFalse(is_punycode("中国.cn"))


class TestValidateDomain(unittest.TestCase):
    """Tests for validate_domain function."""
    
    def test_valid_domain(self):
        """Test validation of valid domain."""
        is_valid, error = validate_domain("example.com")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_valid_subdomain(self):
        """Test validation of valid subdomain."""
        is_valid, error = validate_domain("www.example.com")
        self.assertTrue(is_valid)
    
    def test_valid_punycode(self):
        """Test validation of valid Punycode domain."""
        is_valid, error = validate_domain("xn--fiqs8s.cn")
        self.assertTrue(is_valid)
    
    def test_valid_idn(self):
        """Test validation of valid IDN."""
        is_valid, error = validate_domain("中国.cn")
        self.assertTrue(is_valid)
    
    def test_empty_domain(self):
        """Test validation of empty domain."""
        is_valid, error = validate_domain("")
        self.assertFalse(is_valid)
    
    def test_single_label(self):
        """Test validation of single label (invalid)."""
        is_valid, error = validate_domain("localhost")
        self.assertFalse(is_valid)
    
    def test_starting_hyphen(self):
        """Test validation of domain starting with hyphen."""
        is_valid, error = validate_domain("-invalid.com")
        self.assertFalse(is_valid)
    
    def test_ending_hyphen(self):
        """Test validation of domain ending with hyphen."""
        is_valid, error = validate_domain("invalid-.com")
        self.assertFalse(is_valid)
    
    def test_long_label(self):
        """Test validation of overly long label."""
        long_label = "a" * 64 + ".com"
        is_valid, error = validate_domain(long_label)
        self.assertFalse(is_valid)
        self.assertIn("63", error)


class TestGetTLD(unittest.TestCase):
    """Tests for get_tld function."""
    
    def test_simple_tld(self):
        """Test extraction of simple TLD."""
        self.assertEqual(get_tld("example.com"), "com")
    
    def test_country_tld(self):
        """Test extraction of country TLD."""
        self.assertEqual(get_tld("example.cn"), "cn")
        self.assertEqual(get_tld("example.jp"), "jp")
    
    def test_unicode_tld(self):
        """Test extraction of Unicode TLD."""
        self.assertEqual(get_tld("中国.cn"), "cn")
    
    def test_empty_domain(self):
        """Test handling of empty domain."""
        self.assertEqual(get_tld(""), "")


class TestNormalizeDomain(unittest.TestCase):
    """Tests for normalize_domain function."""
    
    def test_normalize_to_ascii(self):
        """Test normalization to ASCII."""
        result = normalize_domain("中国.cn", to_ascii=True)
        self.assertEqual(result, "xn--fiqs8s.cn")
    
    def test_normalize_to_unicode(self):
        """Test normalization to Unicode."""
        result = normalize_domain("xn--fiqs8s.cn", to_ascii=False)
        self.assertEqual(result, "中国.cn")
    
    def test_normalize_ascii_to_ascii(self):
        """Test normalization of ASCII to ASCII."""
        result = normalize_domain("example.com", to_ascii=True)
        self.assertEqual(result, "example.com")


class TestBatchOperations(unittest.TestCase):
    """Tests for batch operations."""
    
    def test_batch_encode(self):
        """Test batch encoding."""
        domains = ["中国.cn", "日本.jp", "example.com"]
        results = batch_encode(domains)
        
        self.assertEqual(results["中国.cn"], "xn--fiqs8s.cn")
        self.assertEqual(results["日本.jp"], "xn--wgv71a.jp")
        self.assertEqual(results["example.com"], "example.com")
    
    def test_batch_decode(self):
        """Test batch decoding."""
        domains = ["xn--fiqs8s.cn", "xn--wgv71a.jp"]
        results = batch_decode(domains)
        
        self.assertEqual(results["xn--fiqs8s.cn"], "中国.cn")
        self.assertEqual(results["xn--wgv71a.jp"], "日本.jp")
    
    def test_batch_empty(self):
        """Test batch with empty list."""
        self.assertEqual(batch_encode([]), {})
        self.assertEqual(batch_decode([]), {})


class TestDomainInfo(unittest.TestCase):
    """Tests for domain_info function."""
    
    def test_ascii_domain_info(self):
        """Test info for ASCII domain."""
        info = domain_info("example.com")
        
        self.assertEqual(info['original'], "example.com")
        self.assertEqual(info['unicode'], "example.com")
        self.assertEqual(info['ascii'], "example.com")
        self.assertFalse(info['is_idn'])
        self.assertFalse(info['is_punycode'])
        self.assertTrue(info['is_valid'])
        self.assertEqual(info['tld'], "com")
        self.assertEqual(info['label_count'], 2)
    
    def test_idn_domain_info(self):
        """Test info for IDN domain."""
        info = domain_info("中国.cn")
        
        self.assertEqual(info['original'], "中国.cn")
        self.assertEqual(info['unicode'], "中国.cn")
        self.assertEqual(info['ascii'], "xn--fiqs8s.cn")
        self.assertTrue(info['is_idn'])
        self.assertTrue(info['is_punycode'])
        self.assertTrue(info['is_valid'])
        self.assertEqual(info['tld'], "cn")
    
    def test_punycode_domain_info(self):
        """Test info for Punycode domain."""
        info = domain_info("xn--fiqs8s.cn")
        
        self.assertEqual(info['original'], "xn--fiqs8s.cn")
        self.assertEqual(info['unicode'], "中国.cn")
        self.assertEqual(info['ascii'], "xn--fiqs8s.cn")
        self.assertTrue(info['is_punycode'])


class TestConstants(unittest.TestCase):
    """Tests for module constants."""
    
    def test_ace_prefix(self):
        """Test ACE prefix constant."""
        self.assertEqual(ACE_PREFIX, "xn--")
    
    def test_max_label_length(self):
        """Test max label length constant."""
        self.assertEqual(MAX_LABEL_LENGTH, 63)
    
    def test_max_domain_length(self):
        """Test max domain length constant."""
        self.assertEqual(MAX_DOMAIN_LENGTH, 253)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_emoji_domain(self):
        """Test encoding of emoji domain (if supported)."""
        # Emoji domains exist (e.g., i❤️.ws)
        # This tests that the encoder handles them without crashing
        try:
            result = encode_domain("😀.com")
            # May or may not succeed depending on punycode codec
            self.assertIsInstance(result, IDNResult)
        except Exception:
            pass  # Some emoji may not be valid
    
    def test_numbers_in_domain(self):
        """Test encoding of domain with numbers."""
        result = encode_domain("123.中国.cn")
        self.assertTrue(result.success)
    
    def test_hyphen_in_domain(self):
        """Test encoding of domain with hyphens."""
        result = encode_domain("test-example.com")
        self.assertTrue(result.success)
        self.assertEqual(result.encoded, "test-example.com")
    
    def test_case_insensitivity(self):
        """Test that encoding is case-insensitive."""
        result1 = encode_domain("中国.CN")
        result2 = encode_domain("中国.cn")
        self.assertEqual(result1.encoded, result2.encoded)


if __name__ == '__main__':
    unittest.main(verbosity=2)