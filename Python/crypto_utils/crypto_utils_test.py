#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Python Crypto Utils Test Suite
加密工具模块单元测试

运行测试:
    cd Python/crypto_utils
    python crypto_utils_test.py
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import CryptoUtils


class TestCryptoUtils:
    """CryptoUtils 测试类"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def assert_equal(self, actual, expected, test_name):
        """断言相等"""
        if actual == expected:
            print(f"  ✓ {test_name}")
            self.passed += 1
            return True
        else:
            print(f"  ✗ {test_name}")
            print(f"    Expected: {expected}")
            print(f"    Actual: {actual}")
            self.failed += 1
            return False
    
    def assert_true(self, condition, test_name):
        """断言为真"""
        if condition:
            print(f"  ✓ {test_name}")
            self.passed += 1
            return True
        else:
            print(f"  ✗ {test_name}")
            self.failed += 1
            return False
    
    def assert_false(self, condition, test_name):
        """断言为假"""
        return self.assert_true(not condition, test_name)
    
    def assert_length(self, data, length, test_name):
        """断言长度"""
        return self.assert_equal(len(data), length, test_name)
    
    def assert_raises(self, exception_class, func, test_name):
        """断言抛出异常"""
        try:
            func()
            print(f"  ✗ {test_name}")
            print(f"    Expected: {exception_class.__name__}")
            print(f"    Actual: No exception raised")
            self.failed += 1
            return False
        except exception_class:
            print(f"  ✓ {test_name}")
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ✗ {test_name}")
            print(f"    Expected: {exception_class.__name__}")
            print(f"    Actual: {type(e).__name__}")
            self.failed += 1
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("AllToolkit Python Crypto Utils Test Suite")
        print("=" * 60)
        
        self.test_md5_hash()
        self.test_sha1_hash()
        self.test_sha256_hash()
        self.test_sha512_hash()
        self.test_sha3_hash()
        self.test_blake2b_hash()
        self.test_hmac()
        self.test_base64()
        self.test_base64_url()
        self.test_base32()
        self.test_base16()
        self.test_xor_encryption()
        self.test_random_string()
        self.test_random_password()
        self.test_random_bytes()
        self.test_uuid()
        self.test_validation()
        
        # 边界值测试（新增）- 2026-04-17
        self.test_edge_cases()
        
        # 打印测试结果
        print("\n" + "=" * 60)
        print(f"Tests: {self.passed + self.failed}, Passed: {self.passed}, Failed: {self.failed}")
        print("=" * 60)
        
        return self.failed == 0
    
    def test_md5_hash(self):
        """测试 MD5 哈希"""
        print("\n[MD5 Hash Tests]")
        
        # 已知 MD5 值测试
        self.assert_equal(
            CryptoUtils.md5_hash("hello"),
            "5d41402abc4b2a76b9719d911017c592",
            "MD5 hash of 'hello'"
        )
        
        self.assert_equal(
            CryptoUtils.md5_hash(""),
            "d41d8cd98f00b204e9800998ecf8427e",
            "MD5 hash of empty string"
        )
        
        # 字节输入测试
        self.assert_equal(
            CryptoUtils.md5_hash(b"hello"),
            "5d41402abc4b2a76b9719d911017c592",
            "MD5 hash of bytes"
        )
        
        # 中文测试
        self.assert_true(
            len(CryptoUtils.md5_hash("你好世界")) == 32,
            "MD5 hash of Chinese characters"
        )
    
    def test_sha1_hash(self):
        """测试 SHA1 哈希"""
        print("\n[SHA1 Hash Tests]")
        
        self.assert_equal(
            CryptoUtils.sha1_hash("hello"),
            "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",
            "SHA1 hash of 'hello'"
        )
        
        self.assert_length(
            CryptoUtils.sha1_hash("test"),
            40,
            "SHA1 hash length is 40"
        )
    
    def test_sha256_hash(self):
        """测试 SHA256 哈希"""
        print("\n[SHA256 Hash Tests]")
        
        self.assert_equal(
            CryptoUtils.sha256_hash("hello"),
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
            "SHA256 hash of 'hello'"
        )
        
        self.assert_length(
            CryptoUtils.sha256_hash("test"),
            64,
            "SHA256 hash length is 64"
        )
    
    def test_sha512_hash(self):
        """测试 SHA512 哈希"""
        print("\n[SHA512 Hash Tests]")
        
        self.assert_length(
            CryptoUtils.sha512_hash("hello"),
            128,
            "SHA512 hash length is 128"
        )
        
        self.assert_true(
            CryptoUtils.sha512_hash("hello") != CryptoUtils.sha512_hash("Hello"),
            "SHA512 is case-sensitive"
        )
    
    def test_sha3_hash(self):
        """测试 SHA3 哈希"""
        print("\n[SHA3 Hash Tests]")
        
        self.assert_length(
            CryptoUtils.sha3_256_hash("hello"),
            64,
            "SHA3-256 hash length is 64"
        )
        
        self.assert_length(
            CryptoUtils.sha3_512_hash("hello"),
            128,
            "SHA3-512 hash length is 128"
        )
    
    def test_blake2b_hash(self):
        """测试 BLAKE2b 哈希"""
        print("\n[BLAKE2b Hash Tests]")
        
        # 默认 32 字节（64 位十六进制）
        self.assert_length(
            CryptoUtils.blake2b_hash("hello"),
            64,
            "BLAKE2b default hash length is 64"
        )
        
        # 自定义长度
        self.assert_length(
            CryptoUtils.blake2b_hash("hello", digest_size=16),
            32,
            "BLAKE2b with 16 bytes digest"
        )
    
    def test_hmac(self):
        """测试 HMAC"""
        print("\n[HMAC Tests]")
        
        # HMAC-SHA256 测试
        hmac_result = CryptoUtils.hmac_sha256("key", "message")
        self.assert_length(hmac_result, 64, "HMAC-SHA256 length is 64")
        
        # 相同输入产生相同输出
        self.assert_equal(
            CryptoUtils.hmac_sha256("key", "message"),
            CryptoUtils.hmac_sha256("key", "message"),
            "HMAC-SHA256 is deterministic"
        )
        
        # 不同密钥产生不同输出
        self.assert_true(
            CryptoUtils.hmac_sha256("key1", "message") != CryptoUtils.hmac_sha256("key2", "message"),
            "Different keys produce different HMAC"
        )
        
        # HMAC-SHA512 测试
        self.assert_length(
            CryptoUtils.hmac_sha512("key", "message"),
            128,
            "HMAC-SHA512 length is 128"
        )
    
    def test_base64(self):
        """测试 Base64 编码"""
        print("\n[Base64 Tests]")
        
        # 编码测试
        self.assert_equal(
            CryptoUtils.base64_encode("hello"),
            "aGVsbG8=",
            "Base64 encode 'hello'"
        )
        
        self.assert_equal(
            CryptoUtils.base64_encode("hello world"),
            "aGVsbG8gd29ybGQ=",
            "Base64 encode 'hello world'"
        )
        
        # 解码测试
        self.assert_equal(
            CryptoUtils.base64_decode_string("aGVsbG8="),
            "hello",
            "Base64 decode 'aGVsbG8='"
        )
        
        # 编解码一致性
        original = "Hello, 世界! 🌍"
        encoded = CryptoUtils.base64_encode(original)
        decoded = CryptoUtils.base64_decode_string(encoded)
        self.assert_equal(decoded, original, "Base64 round-trip with Unicode")
    
    def test_base64_url(self):
        """测试 URL 安全的 Base64"""
        print("\n[Base64 URL Tests]")
        
        # URL 安全编码不应包含 +/
        encoded = CryptoUtils.base64_url_encode("hello world+/")
        self.assert_false('+' in encoded or '/' in encoded, "Base64URL has no + or /")
        self.assert_false('=' in encoded, "Base64URL has no padding")
        
        # 编解码一致性
        original = "test data+/"
        encoded = CryptoUtils.base64_url_encode(original)
        decoded = CryptoUtils.base64_url_decode(encoded)
        self.assert_equal(decoded.decode('utf-8'), original, "Base64URL round-trip")
    
    def test_base32(self):
        """测试 Base32 编码"""
        print("\n[Base32 Tests]")
        
        # 编码测试（注意：某些实现不添加填充）
        encoded = CryptoUtils.base32_encode("hello")
        # Base32 编码 "hello" 应该以 NBSWY3DP 开头
        self.assert_true(encoded.startswith("NBSWY3DP"), "Base32 encode 'hello' starts correctly")
        
        # 编解码一致性
        original = "test data"
        encoded = CryptoUtils.base32_encode(original)
        decoded = CryptoUtils.base32_decode(encoded)
        self.assert_equal(decoded.decode('utf-8'), original, "Base32 round-trip")
    
    def test_base16(self):
        """测试 Base16 (Hex) 编码"""
        print("\n[Base16 Tests]")
        
        # 编码测试
        self.assert_equal(
            CryptoUtils.base16_encode("hello"),
            "68656C6C6F",
            "Base16 encode 'hello'"
        )
        
        # 编解码一致性
        original = "test"
        encoded = CryptoUtils.base16_encode(original)
        decoded = CryptoUtils.base16_decode(encoded)
        self.assert_equal(decoded.decode('utf-8'), original, "Base16 round-trip")
    
    def test_xor_encryption(self):
        """测试 XOR 加密"""
        print("\n[XOR Encryption Tests]")
        
        # 加密解密一致性
        original = "Hello, World!"
        key = "secret_key"
        encrypted = CryptoUtils.xor_encrypt(original, key)
        decrypted = CryptoUtils.xor_decrypt(encrypted, key)
        self.assert_equal(decrypted, original, "XOR encrypt/decrypt round-trip")
        
        # 不同密钥产生不同结果
        encrypted1 = CryptoUtils.xor_encrypt("test", "key1")
        encrypted2 = CryptoUtils.xor_encrypt("test", "key2")
        self.assert_true(encrypted1 != encrypted2, "Different keys produce different encrypted data")
        
        # 中文加密
        original_chinese = "你好世界"
        encrypted = CryptoUtils.xor_encrypt(original_chinese, "key")
        decrypted = CryptoUtils.xor_decrypt(encrypted, "key")
        self.assert_equal(decrypted, original_chinese, "XOR encrypt/decrypt Chinese")
    
    def test_random_string(self):
        """测试随机字符串生成"""
        print("\n[Random String Tests]")
        
        # 长度测试
        for length in [8, 16, 32, 64]:
            result = CryptoUtils.random_string(length)
            self.assert_length(result, length, f"Random string length {length}")
        
        # 不同调用产生不同结果
        str1 = CryptoUtils.random_string(16)
        str2 = CryptoUtils.random_string(16)
        self.assert_true(str1 != str2, "Random strings are unique")
        
        # 字符集测试
        result = CryptoUtils.random_string(10, chars="abc")
        self.assert_true(all(c in "abc" for c in result), "Random string with custom chars")
    
    def test_random_password(self):
        """测试随机密码生成"""
        print("\n[Random Password Tests]")
        
        # 长度测试
        password = CryptoUtils.random_password(16)
        self.assert_length(password, 16, "Password length 16")
        
        # 默认密码包含各类字符
        password = CryptoUtils.random_password(20)
        self.assert_true(any(c.isupper() for c in password), "Password contains uppercase")
        self.assert_true(any(c.islower() for c in password), "Password contains lowercase")
        self.assert_true(any(c.isdigit() for c in password), "Password contains digits")
        
        # 不同调用产生不同密码
        pwd1 = CryptoUtils.random_password(16)
        pwd2 = CryptoUtils.random_password(16)
        self.assert_true(pwd1 != pwd2, "Random passwords are unique")
    
    def test_random_bytes(self):
        """测试随机字节生成"""
        print("\n[Random Bytes Tests]")
        
        # 长度测试
        for length in [8, 16, 32]:
            result = CryptoUtils.random_bytes(length)
            self.assert_length(result, length, f"Random bytes length {length}")
        
        # 不同调用产生不同结果
        bytes1 = CryptoUtils.random_bytes(16)
        bytes2 = CryptoUtils.random_bytes(16)
        self.assert_true(bytes1 != bytes2, "Random bytes are unique")
    
    def test_uuid(self):
        """测试 UUID 生成"""
        print("\n[UUID Tests]")
        
        # UUID4 格式测试
        uuid4 = CryptoUtils.uuid_v4()
        self.assert_length(uuid4, 36, "UUID4 length is 36")
        self.assert_true(uuid4.count('-') == 4, "UUID4 has 4 hyphens")
        
        # UUID4 唯一性
        uuid1 = CryptoUtils.uuid_v4()
        uuid2 = CryptoUtils.uuid_v4()
        self.assert_true(uuid1 != uuid2, "UUID4s are unique")
        
        # UUID 紧凑格式
        uuid_compact = CryptoUtils.uuid_v4_compact()
        self.assert_length(uuid_compact, 32, "UUID compact length is 32")
        self.assert_true('-' not in uuid_compact, "UUID compact has no hyphens")
    
    def test_validation(self):
        """测试验证函数"""
        print("\n[Validation Tests]")
        
        # MD5 格式验证
        self.assert_true(CryptoUtils.is_valid_md5("5d41402abc4b2a76b9719d911017c592"), 
                        "Valid MD5 format")
        self.assert_false(CryptoUtils.is_valid_md5("invalid"), "Invalid MD5 format")
        self.assert_false(CryptoUtils.is_valid_md5(""), "Empty MD5 format")
        
        # SHA256 格式验证
        self.assert_true(CryptoUtils.is_valid_sha256("2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"),
                        "Valid SHA256 format")
        self.assert_false(CryptoUtils.is_valid_sha256("invalid"), "Invalid SHA256 format")
        
        # Base64 验证
        self.assert_true(CryptoUtils.is_valid_base64("aGVsbG8="), "Valid Base64")
        self.assert_false(CryptoUtils.is_valid_base64("invalid!!!"), "Invalid Base64")
    
    def test_edge_cases(self):
        """边界值测试（新增）- 2026-04-17"""
        print("\n[Edge Case Tests - Added 2026-04-17]")
        
        # 空字符串哈希
        self.assert_true(CryptoUtils.md5_hash("") != "", "MD5 of empty string is non-empty")
        self.assert_true(CryptoUtils.sha256_hash("") != "", "SHA256 of empty string is non-empty")
        
        # 单字符哈希
        self.assert_length(CryptoUtils.md5_hash("a"), 32, "MD5 of single character")
        self.assert_length(CryptoUtils.sha256_hash("a"), 64, "SHA256 of single character")
        
        # 极长数据哈希
        long_data = "A" * 10000
        self.assert_length(CryptoUtils.sha256_hash(long_data), 64, "SHA256 of long data")
        
        # Base64 边界值
        self.assert_equal(CryptoUtils.base64_encode(""), "", "Base64 of empty string")
        
        # Base64 URL 边界值 - 空字符串
        self.assert_equal(CryptoUtils.base64_url_encode(""), "", "Base64URL of empty string")
        
        # XOR 空数据
        encrypted = CryptoUtils.xor_encrypt("", "key")
        decrypted = CryptoUtils.xor_decrypt(encrypted, "key")
        self.assert_equal(decrypted, "", "XOR encrypt/decrypt empty string")
        
        # 随机密码最小长度（注意：需要至少4个字符以包含各类型字符）
        password = CryptoUtils.random_password(4)
        self.assert_length(password, 4, "Password with minimum length 4")
        
        # 随机字符串最小长度
        result = CryptoUtils.random_string(1)
        self.assert_length(result, 1, "Random string with minimum length 1")
        
        # 随机字节最小长度
        result = CryptoUtils.random_bytes(1)
        self.assert_length(result, 1, "Random bytes with minimum length 1")
        
        # BLAKE2b 边界值
        self.assert_length(CryptoUtils.blake2b_hash(""), 64, "BLAKE2b of empty string")
        
        # HMAC 空密钥
        hmac_result = CryptoUtils.hmac_sha256("", "message")
        self.assert_length(hmac_result, 64, "HMAC with empty key")
        
        # HMAC 空消息
        hmac_result = CryptoUtils.hmac_sha256("key", "")
        self.assert_length(hmac_result, 64, "HMAC with empty message")
        
        # Base32 空数据
        self.assert_equal(CryptoUtils.base32_encode(""), "", "Base32 of empty string")
        
        # Base16 空数据
        self.assert_equal(CryptoUtils.base16_encode(""), "", "Base16 of empty string")


def run_tests():
    """运行测试套件"""
    test = TestCryptoUtils()
    success = test.run_all_tests()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(run_tests())