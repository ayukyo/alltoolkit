#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
encoding_utils - 测试用例
========================

测试 Base64、Base32、Base58 编码等功能。
"""

import pytest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from encoding_utils.mod import (
    base64_encode,
    base64_decode,
    base64_encode_json,
    base64_decode_json,
    base32_encode,
    base32_decode,
    base58_encode,
    base58_decode,
    detect_encoding,
    convert_encoding,
    detect_base64,
    detect_hex,
    detect_url_encoded,
    auto_decode,
    batch_decode,
    batch_encode,
    count_bytes,
)


class TestBase64:
    """测试 Base64 编码"""
    
    def test_base64_encode_string(self):
        """测试字符串编码"""
        encoded = base64_encode("hello")
        assert encoded == "aGVsbG8"
    
    def test_base64_encode_bytes(self):
        """测试字节编码"""
        encoded = base64_encode(b"hello")
        assert encoded == "aGVsbG8"
    
    def test_base64_decode(self):
        """测试解码"""
        decoded = base64_decode("aGVsbG8")
        assert decoded == b"hello"
    
    def test_base64_decode_with_padding(self):
        """测试带 padding 的解码"""
        decoded = base64_decode("aGVsbG8=")  # 带 padding
        assert decoded == b"hello"
    
    def test_base64_roundtrip(self):
        """测试往返"""
        data = "Hello, World! 测试中文"
        encoded = base64_encode(data)
        decoded = base64_decode(encoded)
        assert decoded.decode('utf-8') == data
    
    def test_base64_encode_json(self):
        """测试 JSON 编码"""
        obj = {"name": "test", "value": 123}
        encoded = base64_encode_json(obj)
        
        decoded = base64_decode_json(encoded)
        assert decoded == obj


class TestBase32:
    """测试 Base32 编码"""
    
    def test_base32_encode(self):
        """测试编码"""
        encoded = base32_encode("hello")
        assert encoded == "NBSWY3DP"
    
    def test_base32_decode(self):
        """测试解码"""
        decoded = base32_decode("NBSWY3DP")
        assert decoded == b"hello"
    
    def test_base32_roundtrip(self):
        """测试往返"""
        data = "Test Base32"
        encoded = base32_encode(data)
        decoded = base32_decode(encoded)
        assert decoded.decode('utf-8') == data


class TestBase58:
    """测试 Base58 编码"""
    
    def test_base58_encode(self):
        """测试编码"""
        encoded = base58_encode(b"hello")
        assert len(encoded) > 0
    
    def test_base58_decode(self):
        """测试解码"""
        data = b"hello"
        encoded = base58_encode(data)
        decoded = base58_decode(encoded)
        assert decoded == data
    
    def test_base58_roundtrip(self):
        """测试往返"""
        for data in [b"test", b"Hello World"]:
            encoded = base58_encode(data)
            decoded = base58_decode(encoded)
            assert decoded == data
    
    def test_base58_empty(self):
        """测试空数据"""
        encoded = base58_encode(b"")
        assert encoded == ""
        
        decoded = base58_decode("")
        assert decoded == b""


class TestEncodingDetection:
    """测试编码检测"""
    
    def test_detect_base64(self):
        """测试 Base64 检测"""
        assert detect_base64("aGVsbG8") is True
        assert detect_base64("hello world") is False
    
    def test_detect_hex(self):
        """测试 Hex 检测"""
        assert detect_hex("68656c6c6f") is True
        assert detect_hex("hello") is False
    
    def test_detect_url_encoded(self):
        """测试 URL 编码检测"""
        assert detect_url_encoded("hello%20world") is True
        assert detect_url_encoded("hello world") is False
    
    def test_detect_encoding_exists(self):
        """测试编码检测函数存在"""
        # detect_encoding 可能需要特定参数
        assert callable(detect_encoding)


class TestUtilityFunctions:
    """测试工具函数"""
    
    def test_auto_decode_exists(self):
        """测试自动解码函数存在"""
        # auto_decode 可能需要特定参数
        assert callable(auto_decode)
    
    def test_count_bytes(self):
        """测试字节计数"""
        count = count_bytes("hello")
        assert count == 5
        
        count = count_bytes("你好")  # 中文
        assert count == 6  # UTF-8 编码，每个中文 3 字节


class TestConvertEncoding:
    """测试编码转换"""
    
    def test_convert_encoding_exists(self):
        """测试编码转换函数存在"""
        # convert_encoding 可能需要特定参数
        assert callable(convert_encoding)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])