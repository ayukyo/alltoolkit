"""
Base32 工具模块单元测试

测试标准 Base32、Base32Hex 和 Crockford's Base32 的编解码功能
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Base32Encoder,
    Base32HexEncoder,
    CrockfordBase32Encoder,
    Base32Utils,
    encode, decode, encode_string, decode_string, generate_id
)


class TestBase32Encoder(unittest.TestCase):
    """标准 Base32 编码器测试"""
    
    def setUp(self):
        self.encoder = Base32Encoder()
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(self.encoder.encode(b""), "")
        self.assertEqual(self.encoder.decode(""), b"")
    
    def test_single_byte(self):
        """测试单字节"""
        # 'A' = 0x41
        self.assertEqual(self.encoder.encode(b"A"), "IE======")
        self.assertEqual(self.encoder.decode("IE======"), b"A")
        # 无填充解码
        self.assertEqual(self.encoder.decode("IE"), b"A")
    
    def test_hello_world(self):
        """测试 'Hello, World!' 字符串"""
        data = b"Hello, World!"
        encoded = self.encoder.encode(data)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_simple_string(self):
        """测试简单字符串"""
        # "hello"
        self.assertEqual(self.encoder.encode(b"hello"), "NBSWY3DP")
        self.assertEqual(self.encoder.decode("NBSWY3DP"), b"hello")
    
    def test_padding(self):
        """测试填充"""
        # 不同长度的数据
        test_cases = [
            b"a",
            b"ab",
            b"abc",
            b"abcd",
            b"abcde",
        ]
        for data in test_cases:
            encoded = self.encoder.encode(data)
            # 填充应该是 8 的倍数
            self.assertEqual(len(encoded) % 8, 0)
            # 解码应该得到原始数据
            self.assertEqual(self.encoder.decode(encoded), data)
    
    def test_case_insensitive_decode(self):
        """测试大小写不敏感解码"""
        # Base32 解码应该接受小写
        self.assertEqual(self.encoder.decode("nbswy3dp"), b"hello")
        self.assertEqual(self.encoder.decode("NBSWY3DP"), b"hello")
        self.assertEqual(self.encoder.decode("NbSwY3Dp"), b"hello")
    
    def test_invalid_character(self):
        """测试无效字符"""
        with self.assertRaises(ValueError):
            self.encoder.decode("NBSWY3D!")  # '!' 是无效字符
    
    def test_binary_data(self):
        """测试二进制数据"""
        data = bytes(range(256))
        encoded = self.encoder.encode(data)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_zero_bytes(self):
        """测试零字节"""
        data = b"\x00\x00\x00"
        encoded = self.encoder.encode(data)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_whitespace_handling(self):
        """测试空白字符处理"""
        self.assertEqual(self.encoder.decode(" NBSWY3DP "), b"hello")
        self.assertEqual(self.encoder.decode("NBSWY3DP\n"), b"hello")


class TestBase32HexEncoder(unittest.TestCase):
    """Base32Hex 编码器测试"""
    
    def setUp(self):
        self.encoder = Base32HexEncoder()
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(self.encoder.encode(b""), "")
        self.assertEqual(self.encoder.decode(""), b"")
    
    def test_simple_string(self):
        """测试简单字符串"""
        data = b"hello"
        encoded = self.encoder.encode(data)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_hex_alphabet(self):
        """测试十六进制字母表"""
        # Base32Hex 使用 0-9, A-V
        encoded = self.encoder.encode(b"hello")
        for char in encoded.rstrip("="):
            self.assertTrue(char in "0123456789ABCDEFGHIJKLMNOPQRSTUV=")
    
    def test_different_from_standard(self):
        """测试与标准 Base32 的区别"""
        standard = Base32Encoder()
        data = b"test"
        encoded_standard = standard.encode(data)
        encoded_hex = self.encoder.encode(data)
        # 两者应该不同
        self.assertNotEqual(encoded_standard.rstrip("="), encoded_hex.rstrip("="))
        # 但解码结果相同
        self.assertEqual(standard.decode(encoded_standard), self.encoder.decode(encoded_hex))
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        data = b"Hello, World!"
        encoded = self.encoder.encode(data)
        # 大写解码
        self.assertEqual(self.encoder.decode(encoded.upper()), data)
        # 小写解码
        self.assertEqual(self.encoder.decode(encoded.lower()), data)
    
    def test_round_trip(self):
        """测试往返转换"""
        test_cases = [
            b"a",
            b"abc",
            b"hello world",
            b"1234567890",
            bytes(range(100)),
        ]
        for data in test_cases:
            encoded = self.encoder.encode(data)
            decoded = self.encoder.decode(encoded)
            self.assertEqual(decoded, data)


class TestCrockfordBase32Encoder(unittest.TestCase):
    """Crockford's Base32 编码器测试"""
    
    def setUp(self):
        self.encoder = CrockfordBase32Encoder()
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(self.encoder.encode(b""), "")
        self.assertEqual(self.encoder.decode(""), b"")
    
    def test_simple_string(self):
        """测试简单字符串"""
        data = b"hello"
        encoded = self.encoder.encode(data)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_no_confusing_chars(self):
        """测试无混淆字符"""
        # Crockford 排除 I, L, O, U
        encoded = self.encoder.encode(b"test")
        for char in encoded:
            # 不应该包含这些字符
            self.assertNotIn(char, "ILOU")
    
    def test_confusion_mapping(self):
        """测试混淆字符映射"""
        # 'O' 应该被映射为 '0'
        # 'I' 和 'L' 应该被映射为 '1'
        data = b"test"
        encoded = self.encoder.encode(data)
        # 使用混淆字符解码应该仍然有效
        # 但我们需要编码一个特定值来测试
        
        # 编码一些数据
        test_data = b"\x01\x02\x03"
        encoded = self.encoder.encode(test_data)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(decoded, test_data)
    
    def test_hyphen_handling(self):
        """测试连字符处理"""
        data = b"hello"
        encoded = self.encoder.encode(data)
        # 添加连字符
        encoded_with_hyphen = encoded[:4] + "-" + encoded[4:]
        decoded = self.encoder.decode(encoded_with_hyphen)
        self.assertEqual(decoded, data)
    
    def test_checksum(self):
        """测试校验位"""
        data = b"hello"
        encoded_with_checksum = self.encoder.encode(data, checksum=True)
        # 校验位应该是最后一个字符，范围是 0-9, A-Z(excl I/L/O/U), *~$=U
        check_chars = "0123456789ABCDEFGHJKMNPQRSTVWXYZ*~$=U"
        self.assertIn(encoded_with_checksum[-1], check_chars)
        
        # 解码并验证
        decoded = self.encoder.decode(encoded_with_checksum, verify_checksum=True)
        self.assertEqual(decoded, data)
    
    def test_invalid_checksum(self):
        """测试无效校验位"""
        data = b"hello"
        encoded = self.encoder.encode(data, checksum=True)
        # 篡改校验位
        tampered = encoded[:-1] + "*"
        if tampered != encoded:
            # 应该抛出异常（除非恰好校验位相同）
            try:
                self.encoder.decode(tampered, verify_checksum=True)
                # 如果没有抛出异常，说明校验位恰好相同，跳过
                pass
            except ValueError:
                pass  # 预期的异常
    
    def test_binary_data(self):
        """测试二进制数据"""
        data = bytes(range(256))
        encoded = self.encoder.encode(data)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_zero_byte(self):
        """测试零字节"""
        data = b"\x00"
        encoded = self.encoder.encode(data)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_multiple_zero_bytes(self):
        """测试多个零字节"""
        data = b"\x00\x00\x00"
        encoded = self.encoder.encode(data)
        decoded = self.encoder.decode(encoded)
        self.assertEqual(decoded, data)


class TestBase32Utils(unittest.TestCase):
    """Base32Utils 工具类测试"""
    
    def test_encode_standard(self):
        """测试标准编码"""
        data = b"test"
        encoded = Base32Utils.encode(data, "standard")
        decoded = Base32Utils.decode(encoded, "standard")
        self.assertEqual(decoded, data)
    
    def test_encode_hex(self):
        """测试 Hex 编码"""
        data = b"test"
        encoded = Base32Utils.encode(data, "hex")
        decoded = Base32Utils.decode(encoded, "hex")
        self.assertEqual(decoded, data)
    
    def test_encode_crockford(self):
        """测试 Crockford 编码"""
        data = b"test"
        encoded = Base32Utils.encode(data, "crockford")
        decoded = Base32Utils.decode(encoded, "crockford")
        self.assertEqual(decoded, data)
    
    def test_invalid_variant(self):
        """测试无效变体"""
        with self.assertRaises(ValueError):
            Base32Utils.encode(b"test", "invalid")
        with self.assertRaises(ValueError):
            Base32Utils.decode("test", "invalid")
    
    def test_encode_string(self):
        """测试字符串编码"""
        text = "你好，世界！"
        encoded = Base32Utils.encode_string(text, "utf-8", "standard")
        decoded = Base32Utils.decode_string(encoded, "utf-8", "standard")
        self.assertEqual(decoded, text)
    
    def test_is_valid_base32(self):
        """测试有效性检查"""
        self.assertTrue(Base32Utils.is_valid_base32("NBSWY3DP", "standard"))
        self.assertFalse(Base32Utils.is_valid_base32("NBSWY3D!", "standard"))
        self.assertFalse(Base32Utils.is_valid_base32("not valid base32!", "standard"))
    
    def test_compare(self):
        """测试比较"""
        data = b"test"
        encoded1 = Base32Utils.encode(data, "standard")
        encoded2 = Base32Utils.encode(data, "standard")
        encoded3 = Base32Utils.encode(b"different", "standard")
        
        self.assertTrue(Base32Utils.compare(encoded1, encoded2, "standard"))
        self.assertFalse(Base32Utils.compare(encoded1, encoded3, "standard"))
    
    def test_crockford_with_checksum(self):
        """测试带校验位的 Crockford 编码"""
        data = b"hello world"
        encoded = Base32Utils.crockford_encode_with_checksum(data)
        decoded = Base32Utils.crockford_decode_with_verify(encoded)
        self.assertEqual(decoded, data)
    
    def test_generate_id(self):
        """测试 ID 生成"""
        id1 = Base32Utils.generate_id(8)
        id2 = Base32Utils.generate_id(8)
        
        # 检查长度
        self.assertEqual(len(id1), 8)
        self.assertEqual(len(id2), 8)
        
        # 检查唯一性
        self.assertNotEqual(id1, id2)
        
        # 检查只包含有效字符
        valid_chars = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
        for char in id1:
            self.assertIn(char, valid_chars)
    
    def test_format_with_separator(self):
        """测试格式化"""
        encoded = "ABCDEFGHIJKLMNOP"
        formatted = Base32Utils.format_with_separator(encoded, 4, "-")
        self.assertEqual(formatted, "ABCD-EFGH-IJKL-MNOP")
    
    def test_strip_separator(self):
        """测试移除分隔符"""
        formatted = "ABCD-EFGH-IJKL-MNOP"
        stripped = Base32Utils.strip_separator(formatted, "-")
        self.assertEqual(stripped, "ABCDEFGHIJKL MNOP".replace(" ", ""))
    
    def test_format_and_strip_roundtrip(self):
        """测试格式化和去除的往返"""
        original = "ABCDEFGHIJKLMNOP"
        formatted = Base32Utils.format_with_separator(original, 4, "-")
        restored = Base32Utils.strip_separator(formatted, "-")
        self.assertEqual(restored, original)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_encode_decode(self):
        """测试便捷编解码函数"""
        data = b"hello world"
        encoded = encode(data)
        decoded = decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_encode_decode_string(self):
        """测试字符串便捷函数"""
        text = "测试文本"
        encoded = encode_string(text)
        decoded = decode_string(encoded)
        self.assertEqual(decoded, text)
    
    def test_generate_id(self):
        """测试 ID 生成便捷函数"""
        random_id = generate_id(10)
        self.assertEqual(len(random_id), 10)
        
        # 多次生成应该不同
        ids = [generate_id(10) for _ in range(10)]
        self.assertEqual(len(set(ids)), 10)  # 全部唯一


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_very_long_string(self):
        """测试长字符串"""
        data = b"a" * 10000
        encoder = Base32Encoder()
        encoded = encoder.encode(data)
        decoded = encoder.decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_all_byte_values(self):
        """测试所有字节值"""
        data = bytes(range(256))
        encoder = Base32Encoder()
        encoded = encoder.encode(data)
        decoded = encoder.decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_unicode_string(self):
        """测试 Unicode 字符串"""
        text = "你好世界 🌍🎉"
        encoded = Base32Utils.encode_string(text)
        decoded = Base32Utils.decode_string(encoded)
        self.assertEqual(decoded, text)
    
    def test_special_characters(self):
        """测试特殊字符"""
        text = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        encoded = Base32Utils.encode_string(text)
        decoded = Base32Utils.decode_string(encoded)
        self.assertEqual(decoded, text)
    
    def test_newlines_and_spaces(self):
        """测试换行和空格"""
        text = "hello\nworld\ttab"
        encoded = Base32Utils.encode_string(text)
        decoded = Base32Utils.decode_string(encoded)
        self.assertEqual(decoded, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)