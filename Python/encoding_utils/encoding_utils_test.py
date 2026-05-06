"""
Encoding Utilities 测试套件

测试各种编码格式的转换、检测和处理功能。
"""

import unittest
from mod import (
    # Base64
    base64_encode, base64_decode, base64_encode_json, base64_decode_json,
    
    # Base32
    base32_encode, base32_decode,
    
    # Base58
    base58_encode, base58_decode,
    
    # URL
    url_encode, url_decode, url_encode_query, url_decode_query, url_encode_all,
    
    # Hex
    hex_encode, hex_decode, hex_encode_with_prefix, hex_decode_with_prefix,
    
    # Quoted-printable
    quoted_printable_encode, quoted_printable_decode,
    
    # Unicode
    unicode_normalize_nfc, unicode_normalize_nfd, unicode_normalize_nfkc,
    unicode_normalize_nfkd, unicode_remove_accents,
    
    # 检测
    detect_base64, detect_hex, detect_url_encoded, detect_encoding, auto_decode,
    
    # 信息
    count_bytes, get_unicode_name, get_unicode_category,
    
    # 批量操作
    batch_encode, batch_decode,
    
    # 转换
    convert_encoding,
)


class TestBase64(unittest.TestCase):
    """测试 Base64 编码"""
    
    def test_base64_encode_basic(self):
        """测试基础 Base64 编码"""
        self.assertEqual(base64_encode("Hello"), "SGVsbG8")
        self.assertEqual(base64_encode("World"), "V29ybGQ")
    
    def test_base64_encode_bytes(self):
        """测试字节 Base64 编码"""
        self.assertEqual(base64_encode(b"Hello"), "SGVsbG8")
    
    def test_base64_encode_url_safe(self):
        """测试 URL-safe Base64 编码"""
        encoded = base64_encode(bytes(range(256)), url_safe=True)
        self.assertNotIn('+', encoded)
        self.assertNotIn('/', encoded)
    
    def test_base64_decode_basic(self):
        """测试基础 Base64 解码"""
        self.assertEqual(base64_decode("SGVsbG8=").decode(), "Hello")
        self.assertEqual(base64_decode("SGVsbG8").decode(), "Hello")  # 无 padding
    
    def test_base64_decode_url_safe(self):
        """测试 URL-safe Base64 解码"""
        original = "Test Data"
        encoded = base64_encode(original, url_safe=True)
        decoded = base64_decode(encoded, url_safe=True).decode()
        self.assertEqual(decoded, original)
    
    def test_base64_encode_json(self):
        """测试 JSON Base64 编码"""
        obj = {"name": "test", "value": 123}
        encoded = base64_encode_json(obj)
        decoded = base64_decode_json(encoded)
        self.assertEqual(decoded, obj)
    
    def test_base64_roundtrip(self):
        """测试 Base64 往返"""
        original = "Hello 你好"
        encoded = base64_encode(original)
        decoded = base64_decode(encoded).decode()
        self.assertEqual(decoded, original)


class TestBase32(unittest.TestCase):
    """测试 Base32 编码"""
    
    def test_base32_encode_basic(self):
        """测试基础 Base32 编码"""
        encoded = base32_encode("Hello")
        self.assertTrue(len(encoded) > 0)
    
    def test_base32_encode_bytes(self):
        """测试字节 Base32 编码"""
        encoded = base32_encode(b"Hello")
        self.assertTrue(len(encoded) > 0)
    
    def test_base32_decode_basic(self):
        """测试基础 Base32 解码"""
        original = "Hello"
        encoded = base32_encode(original)
        decoded = base32_decode(encoded).decode()
        self.assertEqual(decoded, original)
    
    def test_base32_roundtrip(self):
        """测试 Base32 往返"""
        original = "Hello World 你好"
        encoded = base32_encode(original)
        decoded = base32_decode(encoded).decode()
        self.assertEqual(decoded, original)


class TestBase58(unittest.TestCase):
    """测试 Base58 编码"""
    
    def test_base58_encode_basic(self):
        """测试基础 Base58 编码"""
        encoded = base58_encode("Hello")
        self.assertTrue(len(encoded) > 0)
    
    def test_base58_encode_bytes(self):
        """测试字节 Base58 编码"""
        encoded = base58_encode(b"Hello")
        self.assertTrue(len(encoded) > 0)
    
    def test_base58_encode_leading_zeros(self):
        """测试前导零字节编码"""
        # 前导零字节映射为 '1'
        encoded = base58_encode(b"\x00\x00Hello")
        self.assertTrue(encoded.startswith('11'))
    
    def test_base58_decode_basic(self):
        """测试基础 Base58 解码"""
        original = "Hello"
        encoded = base58_encode(original)
        decoded = base58_decode(encoded).decode()
        self.assertEqual(decoded, original)
    
    def test_base58_decode_leading_zeros(self):
        """测试前导零字节解码"""
        original = b"\x00\x00Hello"
        encoded = base58_encode(original)
        decoded = base58_decode(encoded)
        self.assertEqual(decoded, original)
    
    def test_base58_roundtrip(self):
        """测试 Base58 往返"""
        original = "Test Data 123"
        encoded = base58_encode(original)
        decoded = base58_decode(encoded).decode()
        self.assertEqual(decoded, original)
    
    def test_base58_invalid_char(self):
        """测试无效 Base58 字符"""
        with self.assertRaises(ValueError):
            base58_decode("Invalid0")  # 0 不是有效 Base58 字符


class TestURL(unittest.TestCase):
    """测试 URL 编码"""
    
    def test_url_encode_basic(self):
        """测试基础 URL 编码"""
        self.assertEqual(url_encode("Hello World"), "Hello%20World")
    
    def test_url_encode_safe(self):
        """测试 URL 编码安全字符"""
        self.assertEqual(url_encode("Hello World", safe=" "), "Hello World")
    
    def test_url_encode_special(self):
        """测试特殊字符 URL 编码"""
        self.assertEqual(url_encode("a=b&c=d"), "a%3Db%26c%3Dd")
    
    def test_url_decode_basic(self):
        """测试基础 URL 解码"""
        self.assertEqual(url_decode("Hello%20World"), "Hello World")
    
    def test_url_decode_special(self):
        """测试特殊字符 URL 解码"""
        self.assertEqual(url_decode("a%3Db%26c%3Dd"), "a=b&c=d")
    
    def test_url_encode_query(self):
        """测试 URL 查询参数编码"""
        params = {"name": "test", "value": 123}
        encoded = url_encode_query(params)
        self.assertIn("name=test", encoded)
        self.assertIn("value=123", encoded)
    
    def test_url_decode_query(self):
        """测试 URL 查询参数解码"""
        decoded = url_decode_query("name=test&value=123")
        self.assertEqual(decoded, {"name": "test", "value": "123"})
    
    def test_url_encode_all(self):
        """测试全字符 URL 编码"""
        encoded = url_encode_all("Hello")
        self.assertEqual(encoded, "%48%65%6c%6c%6f")
    
    def test_url_roundtrip(self):
        """测试 URL 编码往返"""
        original = "测试 Test!@#$%^&*()"
        encoded = url_encode(original)
        decoded = url_decode(encoded)
        self.assertEqual(decoded, original)


class TestHex(unittest.TestCase):
    """测试 Hex 编码"""
    
    def test_hex_encode_basic(self):
        """测试基础 Hex 编码"""
        self.assertEqual(hex_encode("Hello"), "48656c6c6f")
    
    def test_hex_encode_bytes(self):
        """测试字节 Hex 编码"""
        self.assertEqual(hex_encode(b"Hello"), "48656c6c6f")
    
    def test_hex_decode_basic(self):
        """测试基础 Hex 解码"""
        self.assertEqual(hex_decode("48656c6c6f").decode(), "Hello")
    
    def test_hex_decode_uppercase(self):
        """测试大写 Hex 解码"""
        self.assertEqual(hex_decode("48656C6C6F").decode(), "Hello")
    
    def test_hex_encode_with_prefix(self):
        """测试带前缀 Hex 编码"""
        self.assertEqual(hex_encode_with_prefix("Hello"), "0x48656c6c6f")
    
    def test_hex_decode_with_prefix(self):
        """测试带前缀 Hex 解码"""
        self.assertEqual(hex_decode_with_prefix("0x48656c6c6f").decode(), "Hello")
        self.assertEqual(hex_decode_with_prefix("0X48656c6c6f").decode(), "Hello")
    
    def test_hex_roundtrip(self):
        """测试 Hex 往返"""
        original = "Test 数据"
        encoded = hex_encode(original)
        decoded = hex_decode(encoded).decode()
        self.assertEqual(decoded, original)


class TestQuotedPrintable(unittest.TestCase):
    """测试 Quoted-printable 编码"""
    
    def test_qp_encode_ascii(self):
        """测试 ASCII Quoted-printable 编码"""
        encoded = quoted_printable_encode("Hello World")
        # ASCII 字符大多不需要编码
        self.assertIn("Hello", encoded)
    
    def test_qp_encode_unicode(self):
        """测试 Unicode Quoted-printable 编码"""
        encoded = quoted_printable_encode("你好")
        self.assertIn("=", encoded)  # Unicode 字符编码为 =XX
    
    def test_qp_decode_ascii(self):
        """测试 ASCII Quoted-printable 解码"""
        decoded = quoted_printable_decode("Hello World")
        self.assertEqual(decoded.decode(), "Hello World")
    
    def test_qp_decode_unicode(self):
        """测试 Unicode Quoted-printable 解码"""
        original = "你好"
        encoded = quoted_printable_encode(original)
        decoded = quoted_printable_decode(encoded).decode()
        self.assertEqual(decoded, original)
    
    def test_qp_roundtrip(self):
        """测试 Quoted-printable 往返"""
        original = "Hello 你好 World 世界"
        encoded = quoted_printable_encode(original)
        decoded = quoted_printable_decode(encoded).decode()
        self.assertEqual(decoded, original)


class TestUnicode(unittest.TestCase):
    """测试 Unicode 规范化"""
    
    def test_nfc_normalize(self):
        """测试 NFC 规范化"""
        text = "café"
        normalized = unicode_normalize_nfc(text)
        self.assertEqual(len(normalized), 4)
    
    def test_nfd_normalize(self):
        """测试 NFD 规范化"""
        text = "café"
        normalized = unicode_normalize_nfd(text)
        # NFD 分解后长度可能增加
        self.assertTrue(len(normalized) >= 4)
    
    def test_nfkc_normalize(self):
        """测试 NFKC 规范化"""
        # 全角转半角
        self.assertEqual(unicode_normalize_nfkc("Ａ"), "A")
        self.assertEqual(unicode_normalize_nfkc("１"), "1")
    
    def test_nfkd_normalize(self):
        """测试 NFKD 规范化"""
        text = "①"  # 带圈数字
        normalized = unicode_normalize_nfkd(text)
        self.assertEqual(normalized, "1")
    
    def test_remove_accents(self):
        """测试移除重音"""
        self.assertEqual(unicode_remove_accents("café"), "cafe")
        self.assertEqual(unicode_remove_accents("über"), "uber")
        self.assertEqual(unicode_remove_accents("naïve"), "naive")


class TestDetection(unittest.TestCase):
    """测试编码检测"""
    
    def test_detect_base64(self):
        """测试 Base64 检测"""
        self.assertTrue(detect_base64("SGVsbG8="))
        self.assertTrue(detect_base64("SGVsbG8"))
        self.assertFalse(detect_base64("Hello World"))
    
    def test_detect_hex(self):
        """测试 Hex 检测"""
        self.assertTrue(detect_hex("48656c6c6f"))
        self.assertTrue(detect_hex("0x48656c6c6f"))
        self.assertFalse(detect_hex("Hello"))
        self.assertFalse(detect_hex("486"))  # 长度不是偶数
        self.assertFalse(detect_hex("48"))  # 长度小于 4
    
    def test_detect_url_encoded(self):
        """测试 URL 编码检测"""
        self.assertTrue(detect_url_encoded("Hello%20World"))
        self.assertFalse(detect_url_encoded("Hello World"))
    
    def test_detect_encoding(self):
        """测试编码类型检测"""
        self.assertEqual(detect_encoding("SGVsbG8gV29ybGQ="), "base64")
        # 短 hex 可能被检测为 base64，长 hex 被检测为 hex
        self.assertEqual(detect_encoding("48656c6c6f20776f726c64"), "hex")
        self.assertEqual(detect_encoding("Hello%20World"), "url")
    
    def test_auto_decode(self):
        """测试自动解码"""
        decoded, encoding = auto_decode("SGVsbG8=")
        self.assertEqual(decoded, "Hello")
        self.assertEqual(encoding, "base64")
        
        decoded, encoding = auto_decode("Hello%20World")
        self.assertEqual(decoded, "Hello World")
        self.assertEqual(encoding, "url")


class TestEncodingInfo(unittest.TestCase):
    """测试编码信息"""
    
    def test_count_bytes(self):
        """测试字节计数"""
        # ASCII
        self.assertEqual(count_bytes("Hello"), 5)
        # UTF-8 中文每个字符 3 字节
        self.assertEqual(count_bytes("你好"), 6)
    
    def test_get_unicode_name(self):
        """测试获取 Unicode 名称"""
        self.assertEqual(get_unicode_name('A'), 'LATIN CAPITAL LETTER A')
        self.assertIsNotNone(get_unicode_name('中'))
    
    def test_get_unicode_category(self):
        """测试获取 Unicode 分类"""
        self.assertEqual(get_unicode_category('A'), 'Lu')  # Letter uppercase
        self.assertEqual(get_unicode_category('a'), 'Ll')  # Letter lowercase
        self.assertEqual(get_unicode_category('1'), 'Nd')  # Number digit
        self.assertEqual(get_unicode_category(' '), 'Zs')  # Separator space


class TestBatchOperations(unittest.TestCase):
    """测试批量操作"""
    
    def test_batch_encode(self):
        """测试批量编码"""
        items = ["Hello", "World", "Test"]
        encoded = batch_encode(items, 'base64')
        self.assertEqual(len(encoded), 3)
        self.assertEqual(encoded[0], "SGVsbG8")
    
    def test_batch_decode(self):
        """测试批量解码"""
        items = ["SGVsbG8", "V29ybGQ", "VGVzdA"]
        decoded = batch_decode(items, 'base64')
        self.assertEqual(decoded, ["Hello", "World", "Test"])
    
    def test_batch_hex(self):
        """测试批量 Hex 编码"""
        items = ["Hello", "World"]
        encoded = batch_encode(items, 'hex')
        self.assertEqual(encoded, ["48656c6c6f", "576f726c64"])
    
    def test_batch_url(self):
        """测试批量 URL 编码"""
        items = ["Hello World", "Test Data"]
        encoded = batch_encode(items, 'url')
        self.assertEqual(encoded, ["Hello%20World", "Test%20Data"])


class TestEncodingConversion(unittest.TestCase):
    """测试编码转换"""
    
    def test_convert_base64_to_hex(self):
        """测试 Base64 转 Hex"""
        converted = convert_encoding("SGVsbG8=", 'base64', 'hex')
        self.assertEqual(converted, "48656c6c6f")
    
    def test_convert_hex_to_base64(self):
        """测试 Hex 转 Base64"""
        converted = convert_encoding("48656c6c6f", 'hex', 'base64')
        self.assertEqual(converted, "SGVsbG8")
    
    def test_convert_invalid_encoding(self):
        """测试无效编码类型"""
        with self.assertRaises(ValueError):
            convert_encoding("test", 'invalid', 'base64')
        
        with self.assertRaises(ValueError):
            convert_encoding("test", 'base64', 'invalid')


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(base64_encode(""), "")
        self.assertEqual(hex_encode(""), "")
        self.assertEqual(url_encode(""), "")
    
    def test_unicode_characters(self):
        """测试 Unicode 字符"""
        text = "中文测试"
        # Base64
        encoded = base64_encode(text)
        decoded = base64_decode(encoded).decode()
        self.assertEqual(decoded, text)
        
        # Hex
        encoded = hex_encode(text)
        decoded = hex_decode(encoded).decode()
        self.assertEqual(decoded, text)
    
    def test_large_data(self):
        """测试大数据"""
        data = "A" * 10000
        encoded = base64_encode(data)
        decoded = base64_decode(encoded).decode()
        self.assertEqual(decoded, data)


if __name__ == "__main__":
    unittest.main(verbosity=2)