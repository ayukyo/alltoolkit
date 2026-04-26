#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - CRC Utilities Test Suite
======================================
Comprehensive tests for CRC computation module.
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crc_utils.mod import (
    CRC,
    crc8,
    crc16,
    crc16_ccitt,
    crc16_modbus,
    crc32,
    crc64,
    file_crc,
    verify_file_crc,
    compute_checksum,
    verify_checksum,
    custom_crc,
    reflect_bits,
    reflect_bits_fast,
    generate_crc_table,
    list_algorithms,
    get_algorithm_info,
    compute_multiple,
    CRC_ALGORITHMS,
)


class TestBitReflection(unittest.TestCase):
    """Test bit reflection utilities."""
    
    def test_reflect_bits_8(self):
        self.assertEqual(reflect_bits(0x00, 8), 0x00)
        self.assertEqual(reflect_bits(0xFF, 8), 0xFF)
        self.assertEqual(reflect_bits(0x31, 8), 0x8C)
        self.assertEqual(reflect_bits(0x55, 8), 0xAA)
        self.assertEqual(reflect_bits(0xAA, 8), 0x55)
    
    def test_reflect_bits_16(self):
        self.assertEqual(reflect_bits(0x0000, 16), 0x0000)
        self.assertEqual(reflect_bits(0xFFFF, 16), 0xFFFF)
        self.assertEqual(reflect_bits(0x1234, 16), 0x2C48)
    
    def test_reflect_bits_32(self):
        self.assertEqual(reflect_bits(0x00000000, 32), 0x00000000)
        self.assertEqual(reflect_bits(0xFFFFFFFF, 32), 0xFFFFFFFF)
    
    def test_reflect_bits_fast(self):
        for width in [8, 16, 32]:
            for value in [0, 1, 0x55, 0xAA, 0x1234, 0x5678]:
                expected = reflect_bits(value, width)
                result = reflect_bits_fast(value, width)
                self.assertEqual(result, expected)
    
    def test_reflect_symmetric(self):
        for value in [0x00, 0x31, 0x55, 0xAA, 0xFF]:
            reflected = reflect_bits(value, 8)
            double_reflected = reflect_bits(reflected, 8)
            self.assertEqual(double_reflected, value)


class TestCRCTable(unittest.TestCase):
    """Test CRC table generation."""
    
    def test_generate_table_crc8(self):
        table = generate_crc_table(0x07, 8)
        self.assertEqual(len(table), 256)
        self.assertEqual(table[0], 0)
    
    def test_generate_table_crc16(self):
        table = generate_crc_table(0x1021, 16)
        self.assertEqual(len(table), 256)
        self.assertEqual(table[0], 0)


class TestCRCClass(unittest.TestCase):
    """Test CRC class functionality."""
    
    def test_init_crc32(self):
        crc = CRC('crc-32')
        self.assertEqual(crc.width, 32)
        self.assertEqual(crc.algorithm, 'crc-32')
    
    def test_init_crc16(self):
        crc = CRC('crc-16-ccitt')
        self.assertEqual(crc.width, 16)
    
    def test_init_crc8(self):
        crc = CRC('crc-8')
        self.assertEqual(crc.width, 8)
    
    def test_init_invalid_algorithm(self):
        with self.assertRaises(ValueError):
            CRC('invalid-algo')
    
    def test_update_bytes(self):
        crc = CRC('crc-32')
        crc.update(b'Hello')
        self.assertIsInstance(crc.value, int)
    
    def test_update_string(self):
        crc = CRC('crc-32')
        crc.update('Hello')
        crc2 = CRC('crc-32')
        crc2.update(b'Hello')
        self.assertEqual(crc.digest, crc2.digest)
    
    def test_reset(self):
        crc = CRC('crc-32')
        crc.update(b'Hello')
        crc.reset()
        self.assertEqual(crc.value, crc._init)


class TestCRC32(unittest.TestCase):
    """Test CRC-32."""
    
    def test_crc32_hello(self):
        result = crc32(b'Hello, World!')
        self.assertEqual(result, 0xEC4AC3D0)
    
    def test_crc32_empty(self):
        result = crc32(b'')
        self.assertEqual(result, 0x00000000)
    
    def test_crc32_check(self):
        result = crc32(b'123456789')
        self.assertEqual(result, 0xCBF43926)
    
    def test_crc32_class(self):
        crc = CRC('crc-32')
        crc.update(b'123456789')
        self.assertEqual(crc.digest, 0xCBF43926)
    
    def test_crc32_static_method(self):
        result = CRC.crc32(b'123456789')
        self.assertEqual(result, 0xCBF43926)


class TestCRC16(unittest.TestCase):
    """Test CRC-16 variants."""
    
    def test_crc16_ccitt(self):
        result = crc16_ccitt(b'123456789')
        self.assertEqual(result, 0x2189)
    
    def test_crc16_ccitt_false(self):
        crc = CRC('crc-16-ccitt-false')
        crc.update(b'123456789')
        self.assertEqual(crc.digest, 0x29B1)
    
    def test_crc16_modbus(self):
        result = crc16_modbus(b'123456789')
        self.assertEqual(result, 0x4B37)
    
    def test_crc16_xmodem(self):
        crc = CRC('crc-16-xmodem')
        crc.update(b'123456789')
        self.assertEqual(crc.digest, 0x31C3)
    
    def test_crc16_static(self):
        result = crc16(b'123456789')
        self.assertEqual(result, 0x29B1)


class TestCRC8(unittest.TestCase):
    """Test CRC-8."""
    
    def test_crc8_basic(self):
        result = crc8(b'123456789')
        self.assertEqual(result, 0xF4)
    
    def test_crc8_class(self):
        crc = CRC('crc-8')
        crc.update(b'123456789')
        self.assertEqual(crc.digest, 0xF4)


class TestCRC64(unittest.TestCase):
    """Test CRC-64."""
    
    def test_crc64_ecma(self):
        result = crc64(b'123456789')
        self.assertEqual(result, 0x6C40DF5F0B497347)


class TestVerify(unittest.TestCase):
    """Test verification functions."""
    
    def test_verify_int(self):
        crc = CRC('crc-32')
        result = crc.verify(b'Hello, World!', 0xEC4AC3D0)
        self.assertTrue(result)
    
    def test_verify_hex(self):
        crc = CRC('crc-32')
        result = crc.verify(b'Hello, World!', 'EC4AC3D0')
        self.assertTrue(result)
    
    def test_verify_wrong(self):
        crc = CRC('crc-32')
        result = crc.verify(b'Hello, World!', 0x12345678)
        self.assertFalse(result)
    
    def test_verify_checksum(self):
        result = verify_checksum(b'Hello, World!', 'ec4ac3d0')
        self.assertTrue(result)


class TestFileCRC(unittest.TestCase):
    """Test file CRC operations."""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b'Hello, World!')
        self.temp_file.close()
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_file_crc(self):
        crc_value, hex_str = file_crc(self.temp_file.name, 'crc-32')
        self.assertEqual(crc_value, 0xEC4AC3D0)
        self.assertEqual(hex_str, 'ec4ac3d0')
    
    def test_verify_file_crc(self):
        result = verify_file_crc(self.temp_file.name, 'ec4ac3d0')
        self.assertTrue(result)


class TestCustomCRC(unittest.TestCase):
    """Test custom CRC parameters."""
    
    def test_custom_crc_8(self):
        result = custom_crc(b'123456789', 8, 0x07)
        self.assertEqual(result, 0xF4)
    
    def test_custom_crc_basic(self):
        result = custom_crc(b'test', 16, 0x1021, init=0xFFFF)
        self.assertIsInstance(result, int)


class TestUtilities(unittest.TestCase):
    """Test utility functions."""
    
    def test_list_algorithms(self):
        algos = list_algorithms()
        self.assertIn('crc-32', algos)
        self.assertIn('crc-16-ccitt', algos)
    
    def test_get_algorithm_info(self):
        info = get_algorithm_info('crc-32')
        self.assertEqual(info['width'], 32)
    
    def test_compute_checksum(self):
        result = compute_checksum(b'Hello, World!')
        self.assertEqual(result, 'ec4ac3d0')


class TestCRC32Compatibility(unittest.TestCase):
    """Test CRC-32 compatibility with zlib."""
    
    def test_crc32_matches_zlib(self):
        import zlib
        data = b'Hello, World!'
        zlib_crc = zlib.crc32(data) & 0xFFFFFFFF
        our_crc = crc32(data)
        self.assertEqual(our_crc, zlib_crc)
    
    def test_crc32_various_data(self):
        import zlib
        test_data = [
            b'', b'a', b'Hello', b'123456789',
            bytes(range(256)), b'A' * 1000
        ]
        for data in test_data:
            zlib_crc = zlib.crc32(data) & 0xFFFFFFFF
            our_crc = crc32(data)
            self.assertEqual(our_crc, zlib_crc, f"Mismatch for data: {data[:50]}")


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    test_classes = [
        TestBitReflection,
        TestCRCTable,
        TestCRCClass,
        TestCRC32,
        TestCRC16,
        TestCRC8,
        TestCRC64,
        TestVerify,
        TestFileCRC,
        TestCustomCRC,
        TestUtilities,
        TestCRC32Compatibility,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)