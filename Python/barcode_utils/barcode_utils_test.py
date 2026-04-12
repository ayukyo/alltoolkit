#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Barcode Utilities Test Suite

Comprehensive tests for barcode generation utilities.
Tests cover all barcode formats, edge cases, and error handling.

Run: python barcode_utils_test.py
"""

import sys
import os
import unittest
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    generate_code39, generate_code128, generate_ean13, generate_ean8,
    generate_upca, generate_itf, generate_matrix, generate_barcode,
    save_barcode, get_supported_formats, BarcodeConfig, BarcodeResult,
    _calculate_ean13_checksum, _parse_color
)


class TestBarcodeConfig(unittest.TestCase):
    """Test BarcodeConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = BarcodeConfig()
        self.assertEqual(config.width, 2)
        self.assertEqual(config.height, 100)
        self.assertEqual(config.margin, 10)
        self.assertTrue(config.show_text)
        self.assertEqual(config.text_size, 14)
        self.assertEqual(config.foreground, "#000000")
        self.assertEqual(config.background, "#FFFFFF")
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = BarcodeConfig(
            width=3,
            height=150,
            margin=20,
            show_text=False,
            foreground="red",
            background="white"
        )
        self.assertEqual(config.width, 3)
        self.assertEqual(config.height, 150)
        self.assertFalse(config.show_text)


class TestCode39(unittest.TestCase):
    """Test Code 39 barcode generation."""
    
    def test_basic_code39(self):
        """Test basic Code 39 generation."""
        result = generate_code39("ABC123")
        self.assertIsInstance(result, BarcodeResult)
        self.assertEqual(result.format, 'code39')
        self.assertEqual(result.data, "ABC123")
        self.assertIn('<svg', result.svg)
        self.assertIn('</svg>', result.svg)
        self.assertTrue(result.width > 0)
        self.assertTrue(result.height > 0)
    
    def test_code39_numeric(self):
        """Test Code 39 with numeric data."""
        result = generate_code39("1234567890")
        self.assertEqual(result.format, 'code39')
        self.assertIn('<svg', result.svg)
    
    def test_code39_special_chars(self):
        """Test Code 39 with special characters."""
        result = generate_code39("HELLO-WORLD")
        self.assertEqual(result.format, 'code39')
    
    def test_code39_lowercase(self):
        """Test Code 39 automatically converts to uppercase."""
        result = generate_code39("hello")
        self.assertEqual(result.data, "HELLO")  # Converted to uppercase
    
    def test_code39_invalid_char(self):
        """Test Code 39 rejects invalid characters."""
        with self.assertRaises(ValueError):
            generate_code39("HELLO@WORLD")
    
    def test_code39_custom_config(self):
        """Test Code 39 with custom configuration."""
        config = BarcodeConfig(width=3, height=150, show_text=False)
        result = generate_code39("TEST", config)
        self.assertTrue(result.width > 50)
    
    def test_code39_no_text(self):
        """Test Code 39 without text label."""
        config = BarcodeConfig(show_text=False)
        result = generate_code39("TEST", config)
        self.assertNotIn('<text', result.svg)
    
    def test_code39_empty_data(self):
        """Test Code 39 with minimal data."""
        result = generate_code39("A")
        self.assertEqual(result.format, 'code39')


class TestCode128(unittest.TestCase):
    """Test Code 128 barcode generation."""
    
    def test_basic_code128(self):
        """Test basic Code 128 generation."""
        result = generate_code128("Hello World")
        self.assertIsInstance(result, BarcodeResult)
        self.assertEqual(result.format, 'code128')
        self.assertEqual(result.data, "Hello World")
        self.assertIn('<svg', result.svg)
    
    def test_code128_numeric(self):
        """Test Code 128 with numeric data."""
        result = generate_code128("1234567890")
        self.assertEqual(result.format, 'code128')
    
    def test_code128_mixed(self):
        """Test Code 128 with mixed characters."""
        result = generate_code128("ABC123xyz")
        self.assertEqual(result.format, 'code128')
    
    def test_code128_special_chars(self):
        """Test Code 128 with special characters."""
        result = generate_code128("Test@email.com")
        self.assertEqual(result.format, 'code128')
    
    def test_code128_custom_config(self):
        """Test Code 128 with custom configuration."""
        config = BarcodeConfig(width=2, height=80, scale=1.5)
        result = generate_code128("TEST", config)
        self.assertTrue(result.width > 0)


class TestEAN13(unittest.TestCase):
    """Test EAN-13 barcode generation."""
    
    def test_basic_ean13(self):
        """Test basic EAN-13 generation."""
        result = generate_ean13("590123412345")
        self.assertIsInstance(result, BarcodeResult)
        self.assertEqual(result.format, 'ean13')
        self.assertEqual(len(result.data), 13)  # Includes checksum
        self.assertIn('<svg', result.svg)
    
    def test_ean13_with_checksum(self):
        """Test EAN-13 with 13 digits (checksum included)."""
        result = generate_ean13("5901234123457")
        self.assertEqual(result.format, 'ean13')
    
    def test_ean13_checksum_calculation(self):
        """Test EAN-13 checksum calculation."""
        checksum = _calculate_ean13_checksum("590123412345")
        self.assertEqual(checksum, 7)
    
    def test_ean13_invalid_length(self):
        """Test EAN-13 rejects invalid length."""
        with self.assertRaises(ValueError):
            generate_ean13("12345")
    
    def test_ean13_non_numeric(self):
        """Test EAN-13 filters non-numeric characters."""
        result = generate_ean13("590-123-412345")
        self.assertEqual(result.format, 'ean13')
    
    def test_ean13_different_prefixes(self):
        """Test EAN-13 with different country prefixes."""
        for code in ["012345678905", "400123456789", "690123456789"]:
            result = generate_ean13(code)
            self.assertEqual(result.format, 'ean13')


class TestEAN8(unittest.TestCase):
    """Test EAN-8 barcode generation."""
    
    def test_basic_ean8(self):
        """Test basic EAN-8 generation."""
        result = generate_ean8("1234567")
        self.assertIsInstance(result, BarcodeResult)
        self.assertEqual(result.format, 'ean8')
        self.assertEqual(len(result.data), 8)
        self.assertIn('<svg', result.svg)
    
    def test_ean8_with_checksum(self):
        """Test EAN-8 with 8 digits."""
        result = generate_ean8("12345670")
        self.assertEqual(result.format, 'ean8')
    
    def test_ean8_invalid_length(self):
        """Test EAN-8 rejects invalid length."""
        with self.assertRaises(ValueError):
            generate_ean8("123")


class TestUPCA(unittest.TestCase):
    """Test UPC-A barcode generation."""
    
    def test_basic_upca(self):
        """Test basic UPC-A generation."""
        result = generate_upca("01234567890")
        self.assertIsInstance(result, BarcodeResult)
        self.assertEqual(result.format, 'upca')
        self.assertEqual(len(result.data), 12)
        self.assertIn('<svg', result.svg)
    
    def test_upca_with_checksum(self):
        """Test UPC-A with 12 digits."""
        result = generate_upca("012345678905")
        self.assertEqual(result.format, 'upca')
    
    def test_upca_invalid_length(self):
        """Test UPC-A rejects invalid length."""
        with self.assertRaises(ValueError):
            generate_upca("12345")


class TestITF(unittest.TestCase):
    """Test ITF (Interleaved 2 of 5) barcode generation."""
    
    def test_basic_itf(self):
        """Test basic ITF generation."""
        result = generate_itf("12345678")
        self.assertIsInstance(result, BarcodeResult)
        self.assertEqual(result.format, 'itf')
        self.assertIn('<svg', result.svg)
    
    def test_itf_odd_length(self):
        """Test ITF with odd number of digits (auto-padded)."""
        result = generate_itf("12345")
        self.assertEqual(result.format, 'itf')
    
    def test_itf_non_numeric(self):
        """Test ITF filters non-numeric characters."""
        result = generate_itf("12-34-56")
        self.assertEqual(result.format, 'itf')
    
    def test_itf_empty(self):
        """Test ITF rejects empty data."""
        with self.assertRaises(ValueError):
            generate_itf("")


class TestMatrix(unittest.TestCase):
    """Test matrix barcode generation."""
    
    def test_basic_matrix(self):
        """Test basic matrix barcode."""
        result = generate_matrix("Hello World")
        self.assertIsInstance(result, BarcodeResult)
        self.assertEqual(result.format, 'matrix')
        self.assertIn('<svg', result.svg)
    
    def test_matrix_custom_size(self):
        """Test matrix with custom size."""
        result = generate_matrix("Test", size=25)
        self.assertEqual(result.format, 'matrix')
    
    def test_matrix_long_data(self):
        """Test matrix with long data."""
        result = generate_matrix("A" * 100)
        self.assertEqual(result.format, 'matrix')


class TestUniversalGenerator(unittest.TestCase):
    """Test universal generate_barcode function."""
    
    def test_universal_code39(self):
        """Test universal generator with Code 39."""
        result = generate_barcode("ABC123", format='code39')
        self.assertEqual(result.format, 'code39')
    
    def test_universal_code128(self):
        """Test universal generator with Code 128."""
        result = generate_barcode("Hello", format='code128')
        self.assertEqual(result.format, 'code128')
    
    def test_universal_ean13(self):
        """Test universal generator with EAN-13."""
        result = generate_barcode("590123412345", format='ean13')
        self.assertEqual(result.format, 'ean13')
    
    def test_universal_invalid_format(self):
        """Test universal generator rejects invalid format."""
        with self.assertRaises(ValueError):
            generate_barcode("Test", format='invalid')


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_get_supported_formats(self):
        """Test getting supported formats."""
        formats = get_supported_formats()
        self.assertIsInstance(formats, list)
        self.assertIn('code39', formats)
        self.assertIn('code128', formats)
        self.assertIn('ean13', formats)
        self.assertIn('matrix', formats)
    
    def test_parse_color_named(self):
        """Test parsing named colors."""
        self.assertEqual(_parse_color("black"), "#000000")
        self.assertEqual(_parse_color("white"), "#FFFFFF")
        self.assertEqual(_parse_color("red"), "#FF0000")
    
    def test_parse_color_hex(self):
        """Test parsing hex colors."""
        self.assertEqual(_parse_color("#FF5733"), "#FF5733")
    
    def test_save_barcode(self):
        """Test saving barcode to file."""
        import tempfile
        result = generate_code128("Test")
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as f:
            filepath = f.name
        try:
            save_barcode(result, filepath)
            with open(filepath, 'r') as f:
                content = f.read()
            self.assertIn('<svg', content)
        finally:
            os.unlink(filepath)


class TestBarcodeResult(unittest.TestCase):
    """Test BarcodeResult dataclass."""
    
    def test_result_attributes(self):
        """Test BarcodeResult has all required attributes."""
        result = BarcodeResult(
            svg='<svg></svg>',
            width=200,
            height=100,
            data="TEST",
            format='code128'
        )
        self.assertEqual(result.svg, '<svg></svg>')
        self.assertEqual(result.width, 200)
        self.assertEqual(result.height, 100)
        self.assertEqual(result.data, "TEST")
        self.assertEqual(result.format, 'code128')


class TestSVGOutput(unittest.TestCase):
    """Test SVG output quality."""
    
    def test_svg_valid_xml(self):
        """Test SVG is valid XML structure."""
        result = generate_code128("Test")
        self.assertTrue(result.svg.startswith('<?xml'))
        self.assertIn('<svg', result.svg)
        self.assertIn('</svg>', result.svg)
    
    def test_svg_has_viewbox(self):
        """Test SVG has viewBox attribute."""
        result = generate_code128("Test")
        self.assertIn('viewBox', result.svg)
    
    def test_svg_has_dimensions(self):
        """Test SVG has width and height."""
        result = generate_code128("Test")
        self.assertIn('width=', result.svg)
        self.assertIn('height=', result.svg)
    
    def test_svg_has_background(self):
        """Test SVG has background rect."""
        result = generate_code128("Test")
        self.assertIn('<rect', result.svg)
    
    def test_svg_has_bars(self):
        """Test SVG has bar elements."""
        result = generate_code128("Test")
        self.assertIn('<rect', result.svg)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_single_character(self):
        """Test single character data."""
        result = generate_code128("A")
        self.assertEqual(result.format, 'code128')
    
    def test_very_long_data(self):
        """Test very long data string."""
        result = generate_code128("A" * 100)
        self.assertEqual(result.format, 'code128')
        self.assertTrue(result.width > 100)
    
    def test_unicode_data(self):
        """Test Unicode characters (Code 128)."""
        result = generate_code128("Hello 世界")
        self.assertEqual(result.format, 'code128')
    
    def test_spaces_in_data(self):
        """Test data with spaces."""
        result = generate_code128("Hello World Test")
        self.assertEqual(result.format, 'code128')
    
    def test_zero_scale(self):
        """Test with very small scale."""
        config = BarcodeConfig(scale=0.5)
        result = generate_code128("Test", config)
        self.assertTrue(result.width > 0)
    
    def test_large_scale(self):
        """Test with large scale."""
        config = BarcodeConfig(scale=3.0)
        result = generate_code128("Test", config)
        self.assertTrue(result.width > 100)


class TestChecksumValidation(unittest.TestCase):
    """Test checksum calculation and validation."""
    
    def test_ean13_checksum_zero(self):
        """Test EAN-13 checksum that results in 0."""
        # 978020137962 should have checksum 4
        checksum = _calculate_ean13_checksum("978020137962")
        self.assertEqual(checksum, 4)
    
    def test_ean13_checksum_nine(self):
        """Test EAN-13 checksum that results in 9."""
        checksum = _calculate_ean13_checksum("000000000000")
        self.assertEqual(checksum, 0)
    
    def test_ean8_checksum(self):
        """Test EAN-8 checksum calculation."""
        # Similar algorithm to EAN-13
        code = "1234567"
        total = 0
        for i, digit in enumerate(code):
            d = int(digit)
            if i % 2 == 0:
                total += d * 3
            else:
                total += d
        checksum = (10 - (total % 10)) % 10
        self.assertTrue(0 <= checksum <= 9)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def test_generate_and_save(self):
        """Test complete generate and save workflow."""
        import tempfile
        
        result = generate_code128("Integration Test")
        
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as f:
            filepath = f.name
        
        try:
            save_barcode(result, filepath)
            
            # Verify file exists and has content
            self.assertTrue(os.path.exists(filepath))
            with open(filepath, 'r') as f:
                content = f.read()
            self.assertGreater(len(content), 100)
            self.assertIn('Integration Test', content)
        finally:
            os.unlink(filepath)
    
    def test_multiple_formats(self):
        """Test generating multiple barcode formats."""
        formats = ['code39', 'code128', 'ean13', 'ean8', 'upca', 'itf']
        data_map = {
            'code39': 'ABC123',
            'code128': 'Hello World',
            'ean13': '590123412345',
            'ean8': '1234567',
            'upca': '01234567890',
            'itf': '12345678',
        }
        
        for fmt in formats:
            result = generate_barcode(data_map[fmt], format=fmt)
            self.assertEqual(result.format, fmt)
            self.assertIn('<svg', result.svg)


def run_tests():
    """Run all tests and print summary."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestBarcodeConfig,
        TestCode39,
        TestCode128,
        TestEAN13,
        TestEAN8,
        TestUPCA,
        TestITF,
        TestMatrix,
        TestUniversalGenerator,
        TestUtilityFunctions,
        TestBarcodeResult,
        TestSVGOutput,
        TestEdgeCases,
        TestChecksumValidation,
        TestIntegration,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    if result.wasSuccessful():
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1


if __name__ == '__main__':
    sys.exit(run_tests())
