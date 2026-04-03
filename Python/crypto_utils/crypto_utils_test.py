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
