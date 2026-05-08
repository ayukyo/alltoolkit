#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Steganography Utilities Test Suite
================================================
Comprehensive test suite for steganography utility module.

Tests cover:
- Zero-width character steganography
- Whitespace steganography
- Case-based steganography
- Variation selector steganography
- Detection and analysis
- Edge cases and error handling
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from steganography_utils.mod import (
    # Core functions
    text_to_binary,
    binary_to_text,
    
    # Zero-width steganography
    encode_zw_steganography,
    decode_zw_steganography,
    detect_zw_steganography,
    remove_zw_steganography,
    
    # Whitespace steganography
    encode_whitespace_steganography,
    decode_whitespace_steganography,
    detect_whitespace_steganography,
    remove_whitespace_steganography,
    
    # Case-based steganography
    encode_case_steganography,
    decode_case_steganography,
    auto_decode_case_steganography,
    
    # Variation selector steganography
    encode_variation_selector_steganography,
    decode_variation_selector_steganography,
    
    # Analysis
    analyze_steganography,
    clean_all_steganography,
    
    # Capacity
    calculate_zw_capacity,
    calculate_whitespace_capacity,
    calculate_case_capacity,
    
    # Constants
    ZERO_WIDTH_SPACE,
    ZERO_WIDTH_NON_JOINER,
    ZERO_WIDTH_JOINER,
)


class TestBinaryConversion(unittest.TestCase):
    """Test text to binary and binary to text conversion."""
    
    def test_text_to_binary_basic(self):
        """Test basic text to binary conversion."""
        self.assertEqual(text_to_binary('A'), '01000001')
        self.assertEqual(text_to_binary('AB'), '0100000101000010')
        self.assertEqual(text_to_binary(''), '')
    
    def test_binary_to_text_basic(self):
        """Test basic binary to text conversion."""
        self.assertEqual(binary_to_text('01000001'), 'A')
        self.assertEqual(binary_to_text('0100000101000010'), 'AB')
    
    def test_roundtrip(self):
        """Test conversion roundtrip."""
        texts = ['Hello', 'World!', '123', '中文', '']
        for text in texts:
            binary = text_to_binary(text)
            decoded = binary_to_text(binary)
            self.assertEqual(decoded, text)
    
    def test_binary_to_text_invalid(self):
        """Test invalid binary input."""
        with self.assertRaises(ValueError):
            binary_to_text('010')  # Not multiple of 8
        
        with self.assertRaises(ValueError):
            binary_to_text('not_binary')
    
    def test_unicode_support(self):
        """Test Unicode character support."""
        # Chinese characters
        chinese = '你好'
        binary = text_to_binary(chinese)
        decoded = binary_to_text(binary)
        self.assertEqual(decoded, chinese)
        
        # Emoji
        emoji = '😀'
        binary = text_to_binary(emoji)
        decoded = binary_to_text(binary)
        self.assertEqual(decoded, emoji)


class TestZeroWidthSteganography(unittest.TestCase):
    """Test zero-width character steganography."""
    
    def test_encode_decode_basic(self):
        """Test basic encode and decode."""
        cover = "Hello World"
        secret = "Hi"
        
        stego = encode_zw_steganography(cover, secret)
        decoded = decode_zw_steganography(stego)
        
        self.assertEqual(decoded, secret)
        self.assertTrue(stego.startswith(cover))
        self.assertTrue(len(stego) > len(cover))
    
    def test_encode_preserves_cover(self):
        """Test that cover text is preserved."""
        cover = "Hello World"
        secret = "Secret123"
        
        stego = encode_zw_steganography(cover, secret)
        
        # Cover should be at the start
        self.assertEqual(stego[:len(cover)], cover)
    
    def test_decode_empty_secret(self):
        """Test decoding with no hidden message."""
        plain_text = "Just plain text"
        decoded = decode_zw_steganography(plain_text)
        self.assertEqual(decoded, '')
    
    def test_encode_empty_message(self):
        """Test encoding empty secret."""
        cover = "Hello"
        stego = encode_zw_steganography(cover, '')
        decoded = decode_zw_steganography(stego)
        self.assertEqual(decoded, '')
    
    def test_detect_steganography(self):
        """Test detection of zero-width steganography."""
        cover = "Hello"
        secret = "Secret"
        
        stego = encode_zw_steganography(cover, secret)
        detected, count, msg = detect_zw_steganography(stego)
        
        self.assertTrue(detected)
        self.assertTrue(count > 0)
        self.assertEqual(msg, secret)
    
    def test_detect_clean_text(self):
        """Test detection on clean text."""
        plain = "Just regular text"
        detected, count, msg = detect_zw_steganography(plain)
        
        self.assertFalse(detected)
        self.assertEqual(count, 0)
        self.assertIsNone(msg)
    
    def test_remove_steganography(self):
        """Test removing steganography."""
        cover = "Hello"
        secret = "Secret"
        
        stego = encode_zw_steganography(cover, secret)
        cleaned = remove_zw_steganography(stego)
        
        self.assertEqual(cleaned, cover)
    
    def test_unicode_secret(self):
        """Test with Unicode secret message."""
        cover = "Hello World"
        secret = "秘密"
        
        stego = encode_zw_steganography(cover, secret)
        decoded = decode_zw_steganography(stego)
        
        self.assertEqual(decoded, secret)
    
    def test_long_secret(self):
        """Test with longer secret message."""
        cover = "Cover text"
        secret = "This is a much longer secret message"
        
        stego = encode_zw_steganography(cover, secret)
        decoded = decode_zw_steganography(stego)
        
        self.assertEqual(decoded, secret)


class TestWhitespaceSteganography(unittest.TestCase):
    """Test whitespace steganography."""
    
    def test_encode_decode_basic(self):
        """Test basic encode and decode."""
        cover = "Hello World"
        secret = "Hi"
        
        stego = encode_whitespace_steganography(cover, secret)
        decoded = decode_whitespace_steganography(stego)
        
        self.assertEqual(decoded, secret)
    
    def test_encode_adds_whitespace(self):
        """Test that encoding adds whitespace."""
        cover = "Hello"
        secret = "Secret"
        
        stego = encode_whitespace_steganography(cover, secret)
        
        # Should end with newline marker
        self.assertTrue(stego.endswith('\n\n'))
        self.assertTrue(stego.startswith(cover))
    
    def test_decode_plain_text(self):
        """Test decoding plain text."""
        plain = "Just plain text\n"
        decoded = decode_whitespace_steganography(plain)
        self.assertEqual(decoded, '')
    
    def test_detect_steganography(self):
        """Test detection of whitespace steganography."""
        cover = "Hello"
        secret = "Secret"
        
        stego = encode_whitespace_steganography(cover, secret)
        detected, count, msg = detect_whitespace_steganography(stego)
        
        self.assertTrue(detected)
        self.assertTrue(count > 0)
        self.assertEqual(msg, secret)
    
    def test_detect_clean_text(self):
        """Test detection on clean text."""
        plain = "Just regular text\nNo hidden content"
        detected, count, msg = detect_whitespace_steganography(plain)
        
        self.assertFalse(detected)
        self.assertEqual(count, 0)
    
    def test_remove_steganography(self):
        """Test removing whitespace steganography."""
        cover = "Hello"
        secret = "Secret"
        
        stego = encode_whitespace_steganography(cover, secret)
        cleaned = remove_whitespace_steganography(stego)
        
        # Should not contain the hidden whitespace
        self.assertEqual(cleaned, cover)
    
    def test_empty_secret(self):
        """Test with empty secret."""
        cover = "Hello"
        stego = encode_whitespace_steganography(cover, '')
        decoded = decode_whitespace_steganography(stego)
        self.assertEqual(decoded, '')


class TestCaseSteganography(unittest.TestCase):
    """Test case-based steganography."""
    
    def test_encode_basic(self):
        """Test basic case encoding."""
        cover = "abcdefghij"
        secret = "A"
        
        stego = encode_case_steganography(cover, secret)
        
        # Should have same length
        self.assertEqual(len(stego), len(cover))
        
        # Decode should work
        decoded = decode_case_steganography(stego, len(secret))
        self.assertEqual(decoded, secret)
    
    def test_encode_insufficient_chars(self):
        """Test encoding with insufficient cover characters."""
        cover = "abc"
        secret = "Hello"  # Needs 40 bits
        
        with self.assertRaises(ValueError):
            encode_case_steganography(cover, secret)
    
    def test_decode_roundtrip(self):
        """Test encode-decode roundtrip."""
        cover = "abcdefghijklmnopqrstuvwxyz"
        secret = "Hi"
        
        stego = encode_case_steganography(cover, secret)
        decoded = decode_case_steganography(stego, len(secret))
        
        self.assertEqual(decoded, secret)
    
    def test_auto_decode(self):
        """Test automatic decoding."""
        cover = "abcdefghij" * 2
        secret = "X"
        
        stego = encode_case_steganography(cover, secret)
        decoded = auto_decode_case_steganography(stego)
        
        self.assertEqual(decoded, secret)
    
    def test_case_preserves_non_alpha(self):
        """Test that non-alphabetic characters are preserved."""
        cover = "a1b2c3d4e5f6g7h"
        secret = "A"
        
        stego = encode_case_steganography(cover, secret)
        
        # Numbers should be unchanged
        self.assertIn('1', stego)
        self.assertIn('2', stego)


class TestVariationSelectorSteganography(unittest.TestCase):
    """Test variation selector steganography."""
    
    def test_encode_decode_basic(self):
        """Test basic encode and decode."""
        cover = "Hello"
        secret = "Hi"
        
        stego = encode_variation_selector_steganography(cover, secret)
        decoded = decode_variation_selector_steganography(stego)
        
        self.assertEqual(decoded, secret)
    
    def test_encode_adds_selectors(self):
        """Test that encoding adds variation selectors."""
        cover = "Hello"
        secret = "Test"
        
        stego = encode_variation_selector_steganography(cover, secret)
        
        # Should be longer due to variation selectors
        self.assertTrue(len(stego) > len(cover))
    
    def test_decode_plain_text(self):
        """Test decoding plain text."""
        plain = "Just plain text"
        decoded = decode_variation_selector_steganography(plain)
        self.assertEqual(decoded, '')
    
    def test_unicode_secret(self):
        """Test with Unicode secret."""
        cover = "Hello"
        secret = "秘密"
        
        stego = encode_variation_selector_steganography(cover, secret)
        decoded = decode_variation_selector_steganography(stego)
        
        self.assertEqual(decoded, secret)


class TestAnalysis(unittest.TestCase):
    """Test steganography analysis functions."""
    
    def test_analyze_zw_steganography(self):
        """Test analysis of zero-width steganography."""
        cover = "Hello"
        secret = "Secret"
        
        stego = encode_zw_steganography(cover, secret)
        analysis = analyze_steganography(stego)
        
        self.assertTrue(analysis['zero_width']['detected'])
        self.assertEqual(analysis['zero_width']['message'], secret)
        self.assertTrue(analysis['suspicious'])
    
    def test_analyze_whitespace_steganography(self):
        """Test analysis of whitespace steganography."""
        cover = "Hello"
        secret = "Secret"
        
        stego = encode_whitespace_steganography(cover, secret)
        analysis = analyze_steganography(stego)
        
        self.assertTrue(analysis['whitespace']['detected'])
        self.assertEqual(analysis['whitespace']['message'], secret)
    
    def test_analyze_clean_text(self):
        """Test analysis of clean text."""
        plain = "Just plain text"
        analysis = analyze_steganography(plain)
        
        self.assertFalse(analysis['zero_width']['detected'])
        self.assertFalse(analysis['whitespace']['detected'])
        self.assertFalse(analysis['suspicious'])
    
    def test_clean_all(self):
        """Test cleaning all steganography."""
        cover = "Hello"
        secret = "Secret"
        
        stego = encode_zw_steganography(cover, secret)
        cleaned = clean_all_steganography(stego)
        
        self.assertEqual(cleaned, cover)


class TestCapacity(unittest.TestCase):
    """Test capacity calculation functions."""
    
    def test_zw_capacity(self):
        """Test zero-width capacity calculation."""
        capacity = calculate_zw_capacity(100)
        self.assertEqual(capacity, 12)
        
        capacity = calculate_zw_capacity(0)
        self.assertEqual(capacity, 0)
    
    def test_whitespace_capacity(self):
        """Test whitespace capacity calculation."""
        capacity = calculate_whitespace_capacity(100)
        self.assertEqual(capacity, 12)
    
    def test_case_capacity(self):
        """Test case-based capacity calculation."""
        # All alphabetic
        capacity = calculate_case_capacity("abcdefghij")
        self.assertEqual(capacity, 1)
        
        # Mixed
        capacity = calculate_case_capacity("a1b2c3d4e5f6g7h8")
        self.assertEqual(capacity, 1)
        
        # No alphabetic
        capacity = calculate_case_capacity("12345678")
        self.assertEqual(capacity, 0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_empty_cover(self):
        """Test with empty cover text."""
        cover = ""
        secret = "Secret"
        
        stego = encode_zw_steganography(cover, secret)
        decoded = decode_zw_steganography(stego)
        
        self.assertEqual(decoded, secret)
    
    def test_long_cover(self):
        """Test with long cover text."""
        cover = "A" * 1000
        secret = "Test"
        
        stego = encode_zw_steganography(cover, secret)
        decoded = decode_zw_steganography(stego)
        
        self.assertEqual(decoded, secret)
    
    def test_binary_encoding_edge_cases(self):
        """Test binary encoding edge cases."""
        # Empty string
        self.assertEqual(text_to_binary(''), '')
        
        # Single character
        self.assertEqual(text_to_binary('A'), '01000001')
    
    def test_multiline_text(self):
        """Test with multiline cover text."""
        cover = "Line1\nLine2\nLine3"
        secret = "Secret"
        
        stego = encode_zw_steganography(cover, secret)
        decoded = decode_zw_steganography(stego)
        
        self.assertEqual(decoded, secret)
    
    def test_special_characters(self):
        """Test with special characters in secret."""
        cover = "Hello"
        secret = "!@#$%^&*()"
        
        stego = encode_zw_steganography(cover, secret)
        decoded = decode_zw_steganography(stego)
        
        self.assertEqual(decoded, secret)


class TestConstants(unittest.TestCase):
    """Test that constants are correctly defined."""
    
    def test_zero_width_chars(self):
        """Test zero-width character constants."""
        self.assertEqual(ZERO_WIDTH_SPACE, '\u200B')
        self.assertEqual(ZERO_WIDTH_NON_JOINER, '\u200C')
        self.assertEqual(ZERO_WIDTH_JOINER, '\u200D')


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBinaryConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestZeroWidthSteganography))
    suite.addTests(loader.loadTestsFromTestCase(TestWhitespaceSteganography))
    suite.addTests(loader.loadTestsFromTestCase(TestCaseSteganography))
    suite.addTests(loader.loadTestsFromTestCase(TestVariationSelectorSteganography))
    suite.addTests(loader.loadTestsFromTestCase(TestAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestCapacity))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestConstants))
    
    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)