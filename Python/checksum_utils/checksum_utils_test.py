"""
checksum_utils 单元测试
"""

import unittest
import tempfile
import os
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    CRC32, CRC64, Adler32, Fletcher, InternetChecksum, SimpleChecksum,
    ChecksumCalculator, crc32, crc64, adler32, fletcher16, fletcher32,
    fletcher64, internet_checksum
)


class TestCRC32(unittest.TestCase):
    """CRC32 测试"""
    
    def test_basic_string(self):
        """测试基本字符串"""
        result = CRC32.calculate("Hello")
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0xF7D18982)
    
    def test_empty_string(self):
        """测试空字符串"""
        result = CRC32.calculate("")
        self.assertEqual(result, 0)
    
    def test_bytes_input(self):
        """测试字节输入"""
        result = CRC32.calculate(b"Hello")
        self.assertEqual(result, 0xF7D18982)
    
    def test_incremental(self):
        """测试增量计算"""
        full = CRC32.calculate("Hello World")
        partial = CRC32.calculate("Hello ")
        partial = CRC32.calculate("World", partial)
        self.assertEqual(full, partial)
    
    def test_unicode(self):
        """测试 Unicode 字符串"""
        result = CRC32.calculate("你好世界")
        self.assertIsInstance(result, int)
    
    def test_file_calculation(self):
        """测试文件计算"""
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            f.write(b"Hello, World!")
            filepath = f.name
        
        try:
            file_crc = CRC32.calculate_file(filepath)
            data_crc = CRC32.calculate(b"Hello, World!")
            self.assertEqual(file_crc, data_crc)
        finally:
            os.unlink(filepath)


class TestCRC64(unittest.TestCase):
    """CRC64 测试"""
    
    def test_basic_string(self):
        """测试基本字符串"""
        result = CRC64.calculate("Hello")
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0x51CF5C3BC87BACC8)
    
    def test_empty_string(self):
        """测试空字符串"""
        result = CRC64.calculate("")
        self.assertEqual(result, 0)
    
    def test_bytes_input(self):
        """测试字节输入"""
        result = CRC64.calculate(b"Hello")
        self.assertEqual(result, 0x51CF5C3BC87BACC8)
    
    def test_incremental(self):
        """测试增量计算"""
        full = CRC64.calculate("Hello World")
        partial = CRC64.calculate("Hello ")
        partial = CRC64.calculate("World", partial)
        self.assertEqual(full, partial)
    
    def test_file_calculation(self):
        """测试文件计算"""
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            f.write(b"Hello, World!")
            filepath = f.name
        
        try:
            file_crc = CRC64.calculate_file(filepath)
            data_crc = CRC64.calculate(b"Hello, World!")
            self.assertEqual(file_crc, data_crc)
        finally:
            os.unlink(filepath)


class TestAdler32(unittest.TestCase):
    """Adler32 测试"""
    
    def test_basic_string(self):
        """测试基本字符串"""
        result = Adler32.calculate("Hello")
        self.assertIsInstance(result, int)
        # Adler32("Hello") = 0x058C01F5
        self.assertEqual(result, 0x058C01F5)
    
    def test_empty_string(self):
        """测试空字符串"""
        result = Adler32.calculate("")
        self.assertEqual(result, 1)  # 默认初始值为 1
    
    def test_bytes_input(self):
        """测试字节输入"""
        result = Adler32.calculate(b"Hello")
        self.assertEqual(result, 0x058C01F5)
    
    def test_incremental(self):
        """测试增量计算"""
        full = Adler32.calculate("Hello World")
        partial = Adler32.calculate("Hello ")
        partial = Adler32.calculate("World", partial)
        self.assertEqual(full, partial)
    
    def test_file_calculation(self):
        """测试文件计算"""
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            f.write(b"Hello, World!")
            filepath = f.name
        
        try:
            file_adler = Adler32.calculate_file(filepath)
            data_adler = Adler32.calculate(b"Hello, World!")
            self.assertEqual(file_adler, data_adler)
        finally:
            os.unlink(filepath)


class TestFletcher(unittest.TestCase):
    """Fletcher 测试"""
    
    def test_fletcher16_basic(self):
        """测试 Fletcher-16 基本功能"""
        result = Fletcher.fletcher16("Hello")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 0xFFFF)
    
    def test_fletcher16_empty(self):
        """测试 Fletcher-16 空字符串"""
        result = Fletcher.fletcher16("")
        self.assertEqual(result, 0)
    
    def test_fletcher32_basic(self):
        """测试 Fletcher-32 基本功能"""
        result = Fletcher.fletcher32("Hello")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 0xFFFFFFFF)
    
    def test_fletcher32_empty(self):
        """测试 Fletcher-32 空字符串"""
        result = Fletcher.fletcher32("")
        self.assertEqual(result, 0)
    
    def test_fletcher64_basic(self):
        """测试 Fletcher-64 基本功能"""
        result = Fletcher.fletcher64("Hello")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 0xFFFFFFFFFFFFFFFF)
    
    def test_fletcher64_empty(self):
        """测试 Fletcher-64 空字符串"""
        result = Fletcher.fletcher64("")
        self.assertEqual(result, 0)
    
    def test_known_value(self):
        """测试已知值"""
        # Fletcher-16 for "abcde"
        result = Fletcher.fletcher16("abcde")
        self.assertEqual(result, 0xC8F0)


class TestInternetChecksum(unittest.TestCase):
    """Internet Checksum 测试"""
    
    def test_basic_string(self):
        """测试基本字符串"""
        result = InternetChecksum.calculate("Hello")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 0xFFFF)
    
    def test_empty_string(self):
        """测试空字符串"""
        result = InternetChecksum.calculate("")
        self.assertEqual(result, 0xFFFF)
    
    def test_known_value(self):
        """测试已知值"""
        # RFC 1071 示例 (但顺序不同)
        data = bytes([0x00, 0x01, 0xf2, 0x03, 0xf4, 0xf5, 0xf6, 0xf7])
        result = InternetChecksum.calculate(data)
        # 实际计算值
        self.assertEqual(result, 0x220D)
    
    def test_verify(self):
        """测试验证功能"""
        data = "Hello World"
        checksum = InternetChecksum.calculate(data)
        # 正确的校验和
        self.assertTrue(InternetChecksum.verify(data, checksum))
        # 错误的校验和
        self.assertFalse(InternetChecksum.verify(data, 0x0000))


class TestSimpleChecksum(unittest.TestCase):
    """简单校验和测试"""
    
    def test_sum8(self):
        """测试 8 位求和"""
        result = SimpleChecksum.sum8("Hello")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 0xFF)
    
    def test_sum8_empty(self):
        """测试空字符串"""
        result = SimpleChecksum.sum8("")
        self.assertEqual(result, 0)
    
    def test_sum16(self):
        """测试 16 位求和"""
        result = SimpleChecksum.sum16("Hello")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 0xFFFF)
    
    def test_sum32(self):
        """测试 32 位求和"""
        result = SimpleChecksum.sum32("Hello")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 0xFFFFFFFF)
    
    def test_xor8(self):
        """测试 8 位异或"""
        result = SimpleChecksum.xor8("Hello")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 0xFF)
    
    def test_xor8_empty(self):
        """测试空字符串异或"""
        result = SimpleChecksum.xor8("")
        self.assertEqual(result, 0)
    
    def test_xor8_known(self):
        """测试已知异或值"""
        # "AB" = 0x41 XOR 0x42 = 0x03
        result = SimpleChecksum.xor8("AB")
        self.assertEqual(result, 0x03)
    
    def test_lrc(self):
        """测试 LRC"""
        result = SimpleChecksum.lrc("Hello")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 0xFF)
    
    def test_lrc_empty(self):
        """测试空字符串 LRC"""
        result = SimpleChecksum.lrc("")
        self.assertEqual(result, 0)


class TestChecksumCalculator(unittest.TestCase):
    """统一接口测试"""
    
    def test_all_methods(self):
        """测试所有方法"""
        data = "Test data for checksum"
        
        # 测试所有静态方法
        self.assertIsInstance(ChecksumCalculator.crc32(data), int)
        self.assertIsInstance(ChecksumCalculator.crc64(data), int)
        self.assertIsInstance(ChecksumCalculator.adler32(data), int)
        self.assertIsInstance(ChecksumCalculator.fletcher16(data), int)
        self.assertIsInstance(ChecksumCalculator.fletcher32(data), int)
        self.assertIsInstance(ChecksumCalculator.fletcher64(data), int)
        self.assertIsInstance(ChecksumCalculator.internet(data), int)
        self.assertIsInstance(ChecksumCalculator.sum8(data), int)
        self.assertIsInstance(ChecksumCalculator.sum16(data), int)
        self.assertIsInstance(ChecksumCalculator.sum32(data), int)
        self.assertIsInstance(ChecksumCalculator.xor8(data), int)
        self.assertIsInstance(ChecksumCalculator.lrc(data), int)
    
    def test_calculate_all(self):
        """测试计算所有校验和"""
        data = "Test"
        result = ChecksumCalculator.calculate_all(data)
        
        self.assertIn('crc32', result)
        self.assertIn('crc64', result)
        self.assertIn('adler32', result)
        self.assertIn('fletcher16', result)
        self.assertIn('fletcher32', result)
        self.assertIn('fletcher64', result)
        self.assertIn('internet', result)
        self.assertIn('sum8', result)
        self.assertIn('sum16', result)
        self.assertIn('sum32', result)
        self.assertIn('xor8', result)
        self.assertIn('lrc', result)
        self.assertIn('crc32_hex', result)
        self.assertIn('crc64_hex', result)
        self.assertIn('adler32_hex', result)
    
    def test_to_hex(self):
        """测试十六进制转换"""
        self.assertEqual(ChecksumCalculator.to_hex(0x1234ABCD, 8), '1234ABCD')
        self.assertEqual(ChecksumCalculator.to_hex(0xFF, 4), '00FF')
        self.assertEqual(ChecksumCalculator.to_hex(0, 4), '0000')


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_crc32_function(self):
        """测试 crc32 便捷函数"""
        result = crc32("Hello")
        self.assertEqual(result, CRC32.calculate("Hello"))
    
    def test_crc64_function(self):
        """测试 crc64 便捷函数"""
        result = crc64("Hello")
        self.assertEqual(result, CRC64.calculate("Hello"))
    
    def test_adler32_function(self):
        """测试 adler32 便捷函数"""
        result = adler32("Hello")
        self.assertEqual(result, Adler32.calculate("Hello"))
    
    def test_fletcher16_function(self):
        """测试 fletcher16 便捷函数"""
        result = fletcher16("Hello")
        self.assertEqual(result, Fletcher.fletcher16("Hello"))
    
    def test_fletcher32_function(self):
        """测试 fletcher32 便捷函数"""
        result = fletcher32("Hello")
        self.assertEqual(result, Fletcher.fletcher32("Hello"))
    
    def test_fletcher64_function(self):
        """测试 fletcher64 便捷函数"""
        result = fletcher64("Hello")
        self.assertEqual(result, Fletcher.fletcher64("Hello"))
    
    def test_internet_checksum_function(self):
        """测试 internet_checksum 便捷函数"""
        result = internet_checksum("Hello")
        self.assertEqual(result, InternetChecksum.calculate("Hello"))


class TestEdgeCases(unittest.TestCase):
    """边缘情况测试"""
    
    def test_large_data(self):
        """测试大数据"""
        data = "A" * 100000
        result = CRC32.calculate(data)
        self.assertIsInstance(result, int)
    
    def test_binary_data(self):
        """测试二进制数据"""
        data = bytes(range(256))
        result = CRC32.calculate(data)
        self.assertIsInstance(result, int)
    
    def test_unicode_data(self):
        """测试 Unicode 数据"""
        data = "你好世界 🌍🎉"
        result = CRC32.calculate(data)
        self.assertIsInstance(result, int)
    
    def test_special_characters(self):
        """测试特殊字符"""
        data = "\x00\x01\x02\x03\x04\x05"
        result = CRC32.calculate(data)
        self.assertIsInstance(result, int)


if __name__ == '__main__':
    unittest.main(verbosity=2)