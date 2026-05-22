#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Adler-32 Checksum Utilities Test Module
=====================================================
Unit tests for adler32_utils module.

Tests cover:
    - Basic checksum computation
    - Streaming/incremental computation
    - File operations
    - Verification functions
    - Combined checksums
    - Utility functions
    - Known test values

Run: python -m pytest Python/adler32_utils/test.py -v
Or: python Python/adler32_utils/test.py
"""

import sys
import os
import tempfile
import unittest

# Add module path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adler32_utils.mod import (
    adler32,
    adler32_detailed,
    adler32_hex,
    Adler32Streaming,
    adler32_file,
    adler32_file_hex,
    verify_adler32,
    verify_file_adler32,
    compute_combined_checksum,
    verify_combined_checksum,
    adler32_to_hex,
    hex_to_adler32,
    decompose_adler32,
    compose_adler32,
    compare_adler32,
    adler32_statistics,
    test_adler32,
    Adler32Result,
    ADLER32_MOD,
)


class TestAdler32Basic(unittest.TestCase):
    """Test basic Adler-32 computation."""
    
    def test_empty_string(self):
        """Test empty string returns 1."""
        self.assertEqual(adler32(b''), 1)
        self.assertEqual(adler32_hex(b''), '00000001')
    
    def test_single_byte(self):
        """Test single byte checksum."""
        # 'a' = 97
        # A = 97 + 1 = 98
        # B = 98
        # Adler-32 = (98 << 16) | 98 = 6422626
        self.assertEqual(adler32(b'a'), 6422626)
    
    def test_string_input(self):
        """Test string input (UTF-8 encoding)."""
        self.assertEqual(adler32('Hello'), adler32(b'Hello'))
    
    def test_known_values(self):
        """Test known Adler-32 values (verified against zlib.adler32)."""
        known_values = {
            b'': 1,
            b'a': 6422626,
            b'abc': 38600999,
            b'Hello': 93061621,
            b'Hello World': 403375133,
            b'Wikipedia': 300286872,
        }
        
        for data, expected in known_values.items():
            self.assertEqual(adler32(data), expected,
                           f"Failed for {data!r}")
    
    def test_hex_output(self):
        """Test hexadecimal output."""
        self.assertEqual(adler32_hex(b'Hello'), '058c01f5')
        self.assertEqual(len(adler32_hex(b'')), 8)
    
    def test_detailed_result(self):
        """Test detailed result structure."""
        result = adler32_detailed(b'Hello')
        
        self.assertEqual(result.value, 93061621)
        self.assertEqual(result.hex, '058c01f5')
        self.assertIsInstance(result.a, int)
        self.assertIsInstance(result.b, int)
        
        # Verify decomposition
        self.assertEqual(decompose_adler32(result.value), (result.a, result.b))


class TestAdler32Streaming(unittest.TestCase):
    """Test streaming/incremental Adler-32 computation."""
    
    def test_basic_streaming(self):
        """Test basic streaming computation."""
        stream = Adler32Streaming()
        stream.update(b'Hello')
        stream.update(b' World')
        
        expected = adler32(b'Hello World')
        self.assertEqual(stream.value, expected)
    
    def test_chunked_vs_whole(self):
        """Test chunked computation matches whole data."""
        data = b'The quick brown fox jumps over the lazy dog'
        
        # Whole data
        whole_checksum = adler32(data)
        
        # Chunked data
        stream = Adler32Streaming()
        chunk_size = 10
        for i in range(0, len(data), chunk_size):
            stream.update(data[i:i + chunk_size])
        
        self.assertEqual(stream.value, whole_checksum)
    
    def test_large_chunks(self):
        """Test with large data chunks."""
        # Create large data (> 5552 bytes to test block processing)
        large_data = b'X' * 10000
        
        whole = adler32(large_data)
        
        stream = Adler32Streaming()
        stream.update(large_data)
        
        self.assertEqual(stream.value, whole)
    
    def test_string_input_streaming(self):
        """Test string input in streaming mode."""
        stream = Adler32Streaming()
        stream.update('Hello')
        stream.update(' ')
        stream.update('World')
        
        self.assertEqual(stream.value, adler32(b'Hello World'))
    
    def test_byte_count(self):
        """Test byte counting."""
        stream = Adler32Streaming()
        stream.update(b'Hello')
        self.assertEqual(stream.byte_count, 5)
        stream.update(b' World')
        self.assertEqual(stream.byte_count, 11)
    
    def test_reset(self):
        """Test reset functionality."""
        stream = Adler32Streaming()
        stream.update(b'Hello')
        
        stream.reset()
        self.assertEqual(stream.value, 1)
        self.assertEqual(stream.byte_count, 0)
        
        # After reset, compute different data
        stream.update(b'World')
        self.assertEqual(stream.value, adler32(b'World'))
    
    def test_get_result(self):
        """Test get_result method."""
        stream = Adler32Streaming()
        stream.update(b'Hello')
        
        result = stream.get_result()
        self.assertIsInstance(result, Adler32Result)
        self.assertEqual(result.value, stream.value)


class TestAdler32Verification(unittest.TestCase):
    """Test verification functions."""
    
    def test_verify_with_int(self):
        """Test verification with integer checksum."""
        self.assertTrue(verify_adler32(b'Hello', 93061621))
        self.assertFalse(verify_adler32(b'Hello', 12345))
    
    def test_verify_with_hex(self):
        """Test verification with hex string."""
        self.assertTrue(verify_adler32(b'Hello', '058c01f5'))
        self.assertTrue(verify_adler32(b'Hello', '058C01F5'))  # Case insensitive
        self.assertFalse(verify_adler32(b'Hello', 'invalid'))
        self.assertFalse(verify_adler32(b'Hello', '00000000'))
    
    def test_compare_adler32(self):
        """Test checksum comparison."""
        self.assertTrue(compare_adler32(b'Hello', b'Hello'))
        self.assertFalse(compare_adler32(b'Hello', b'hello'))  # Different case
        self.assertFalse(compare_adler32(b'Hello', b'World'))


class TestAdler32Combined(unittest.TestCase):
    """Test combined Adler-32 + CRC-32 checksums."""
    
    def test_combined_checksum(self):
        """Test combined checksum computation."""
        adler, crc = compute_combined_checksum(b'Hello')
        
        # Adler-32 should match zlib
        self.assertEqual(adler, '058c01f5')
        
        # CRC-32 should be computed
        self.assertEqual(len(crc), 8)
        self.assertIsInstance(int(crc, 16), int)
    
    def test_combined_verification(self):
        """Test combined checksum verification."""
        adler, crc = compute_combined_checksum(b'Hello World')
        
        adler_ok, crc_ok = verify_combined_checksum(b'Hello World', adler, crc)
        
        self.assertTrue(adler_ok)
        self.assertTrue(crc_ok)
        
        # Test with wrong data
        adler_ok2, crc_ok2 = verify_combined_checksum(b'Wrong', adler, crc)
        
        self.assertFalse(adler_ok2)
        self.assertFalse(crc_ok2)
    
    def test_combined_empty(self):
        """Test combined checksum of empty data."""
        adler, crc = compute_combined_checksum(b'')
        
        self.assertEqual(adler, '00000001')  # Adler-32 of empty is 1


class TestAdler32Utilities(unittest.TestCase):
    """Test utility functions."""
    
    def test_to_hex(self):
        """Test integer to hex conversion."""
        self.assertEqual(adler32_to_hex(93061621), '058c01f5')
        self.assertEqual(adler32_to_hex(1), '00000001')
    
    def test_from_hex(self):
        """Test hex to integer conversion."""
        self.assertEqual(hex_to_adler32('058c01f5'), 93061621)
        self.assertEqual(hex_to_adler32('00000001'), 1)
        
        # Invalid hex should raise error
        with self.assertRaises(ValueError):
            hex_to_adler32('invalid')
    
    def test_decompose_compose(self):
        """Test decomposition and composition."""
        original = 93061621
        a, b = decompose_adler32(original)
        
        recomposed = compose_adler32(a, b)
        self.assertEqual(recomposed, original)
    
    def test_statistics(self):
        """Test statistics computation."""
        stats = adler32_statistics(b'Hello')
        
        self.assertEqual(stats['checksum'], 93061621)
        self.assertEqual(stats['checksum_hex'], '058c01f5')
        self.assertEqual(stats['byte_count'], 5)
        self.assertIn('a_value', stats)
        self.assertIn('b_value', stats)
        self.assertIn('byte_sum', stats)
        self.assertIn('byte_average', stats)


class TestAdler32Files(unittest.TestCase):
    """Test file operations."""
    
    def setUp(self):
        """Create temporary test files."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test.txt')
        
        with open(self.test_file, 'wb') as f:
            f.write(b'Hello World')
    
    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.test_file):
            os.unlink(self.test_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_file_checksum(self):
        """Test file checksum computation."""
        result = adler32_file(self.test_file)
        
        self.assertEqual(result.value, adler32(b'Hello World'))
        self.assertIsInstance(result, Adler32Result)
    
    def test_file_checksum_hex(self):
        """Test file checksum hex output."""
        hex_result = adler32_file_hex(self.test_file)
        
        self.assertEqual(hex_result, adler32_hex(b'Hello World'))
    
    def test_file_verification(self):
        """Test file verification."""
        expected = adler32_hex(b'Hello World')
        self.assertTrue(verify_file_adler32(self.test_file, expected))
        
        # Wrong checksum
        self.assertFalse(verify_file_adler32(self.test_file, '00000000'))
    
    def test_file_not_found(self):
        """Test file not found handling."""
        with self.assertRaises(FileNotFoundError):
            adler32_file('/nonexistent/path/file.txt')


class TestAdler32EdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_max_a_value(self):
        """Test behavior near A value overflow."""
        # Create data that would cause A to approach ADLER32_MOD
        # Without triggering overflow before modulo
        large_bytes = bytes([255] * 500)
        
        checksum = adler32(large_bytes)
        self.assertIsInstance(checksum, int)
        
        # A should be < ADLER32_MOD
        a, b = decompose_adler32(checksum)
        self.assertLess(a, ADLER32_MOD)
        self.assertLess(b, ADLER32_MOD)
    
    def test_unicode_string(self):
        """Test Unicode string handling."""
        # UTF-8 encoded string
        unicode_str = '你好世界'  # Chinese "Hello World"
        
        checksum = adler32(unicode_str)
        self.assertIsInstance(checksum, int)
        
        # Should match manually encoded
        self.assertEqual(checksum, adler32(unicode_str.encode('utf-8')))
    
    def test_incremental_with_initial(self):
        """Test incremental computation with non-default initial."""
        # Start with previous checksum
        prev = adler32(b'Hello')
        
        # Continue from that point
        continued = adler32(b' World', initial=prev)
        
        # Should match whole data
        whole = adler32(b'Hello World')
        self.assertEqual(continued, whole)


class TestAdler32SelfTest(unittest.TestCase):
    """Test the built-in self-test function."""
    
    def test_self_test_passes(self):
        """Test that self-test passes."""
        self.assertTrue(test_adler32())


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)