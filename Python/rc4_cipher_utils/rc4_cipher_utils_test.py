#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - RC4 Cipher Utils Test
RC4 流加密工具测试模块

测试覆盖:
- 基本加密/解密
- 密钥调度算法 (KSA)
- 伪随机生成算法 (PRGA)
- RC4-drop 变体
- 十六进制/Base64 输出
- 边界条件和错误处理
- 已知向量测试
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    RC4Cipher,
    RC4Drop,
    RC4Drop256,
    RC4Drop768,
    RC4Drop3072,
    RC4Error,
    rc4_encrypt,
    rc4_decrypt,
    rc4_encrypt_hex,
    rc4_decrypt_hex,
    rc4_encrypt_b64,
    rc4_decrypt_b64,
)


class TestRC4Basic(unittest.TestCase):
    """基本加密解密测试"""
    
    def test_encrypt_decrypt_bytes(self):
        """测试字节加密解密"""
        key = b'test_key'
        plaintext = b'Hello, World!'
        
        cipher = RC4Cipher(key)
        encrypted = cipher.encrypt(plaintext)
        
        cipher2 = RC4Cipher(key)
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_encrypt_decrypt_string(self):
        """测试字符串加密解密"""
        key = 'password123'
        plaintext = 'Hello, RC4!'
        
        encrypted = RC4Cipher.encrypt_string(plaintext, key)
        decrypted = RC4Cipher.decrypt_string(encrypted, key)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_empty_data(self):
        """测试空数据"""
        key = b'key'
        
        cipher = RC4Cipher(key)
        encrypted = cipher.encrypt(b'')
        self.assertEqual(encrypted, b'')
        
        cipher2 = RC4Cipher(key)
        decrypted = cipher2.decrypt(b'')
        self.assertEqual(decrypted, b'')
    
    def test_single_byte(self):
        """测试单字节数据"""
        key = b'key'
        plaintext = b'A'
        
        cipher = RC4Cipher(key)
        encrypted = cipher.encrypt(plaintext)
        
        cipher2 = RC4Cipher(key)
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_large_data(self):
        """测试大数据"""
        key = b'key'
        plaintext = b'X' * 10000
        
        cipher = RC4Cipher(key)
        encrypted = cipher.encrypt(plaintext)
        
        cipher2 = RC4Cipher(key)
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_unicode_string(self):
        """测试 Unicode 字符串"""
        key = '密钥'
        plaintext = '你好世界！Hello World! 🎉'
        
        encrypted = RC4Cipher.encrypt_string(plaintext, key)
        decrypted = RC4Cipher.decrypt_string(encrypted, key)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_different_keys_different_output(self):
        """测试不同密钥产生不同输出"""
        plaintext = b'Same plaintext'
        
        cipher1 = RC4Cipher(b'key1')
        encrypted1 = cipher1.encrypt(plaintext)
        
        cipher2 = RC4Cipher(b'key2')
        encrypted2 = cipher2.encrypt(plaintext)
        
        self.assertNotEqual(encrypted1, encrypted2)
    
    def test_same_key_same_output(self):
        """测试相同密钥产生相同输出（确定性）"""
        key = b'same_key'
        plaintext = b'Same plaintext'
        
        cipher1 = RC4Cipher(key)
        encrypted1 = cipher1.encrypt(plaintext)
        
        cipher2 = RC4Cipher(key)
        encrypted2 = cipher2.encrypt(plaintext)
        
        self.assertEqual(encrypted1, encrypted2)


class TestRC4KeyHandling(unittest.TestCase):
    """密钥处理测试"""
    
    def test_string_key_auto_conversion(self):
        """测试字符串密钥自动转换"""
        key = 'string_key'
        plaintext = b'test'
        
        cipher = RC4Cipher(key)
        encrypted = cipher.encrypt(plaintext)
        
        cipher2 = RC4Cipher(key)
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_long_key_truncation(self):
        """测试长密钥截断（256字节）"""
        # RC4 密钥最长 256 字节
        key = b'x' * 300  # 300 字节，应该被截断到 256
        plaintext = b'test'
        
        # 不应该抛出异常
        cipher = RC4Cipher(key)
        encrypted = cipher.encrypt(plaintext)
        
        # 使用相同的截断后密钥应该能解密
        cipher2 = RC4Cipher(key[:256])
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_empty_key_error(self):
        """测试空密钥抛出错误"""
        with self.assertRaises(RC4Error):
            RC4Cipher(b'')
        
        with self.assertRaises(RC4Error):
            RC4Cipher('')
    
    def test_single_byte_key(self):
        """测试单字节密钥"""
        key = b'K'
        plaintext = b'test data'
        
        cipher = RC4Cipher(key)
        encrypted = cipher.encrypt(plaintext)
        
        cipher2 = RC4Cipher(key)
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)


class TestRC4OutputFormats(unittest.TestCase):
    """输出格式测试"""
    
    def test_hex_output(self):
        """测试十六进制输出"""
        key = b'key'
        plaintext = b'Hello'
        
        cipher = RC4Cipher(key)
        hex_encrypted = cipher.encrypt_to_hex(plaintext)
        
        # 十六进制字符串应该是偶数长度
        self.assertEqual(len(hex_encrypted) % 2, 0)
        
        # 可以解密
        cipher2 = RC4Cipher(key)
        decrypted = cipher2.decrypt_from_hex(hex_encrypted)
        self.assertEqual(plaintext, decrypted)
    
    def test_base64_output(self):
        """测试 Base64 输出"""
        key = b'key'
        plaintext = b'Hello'
        
        cipher = RC4Cipher(key)
        b64_encrypted = cipher.encrypt_to_base64(plaintext)
        
        # Base64 字符串应该只包含有效字符
        import base64
        try:
            base64.b64decode(b64_encrypted)
        except Exception:
            self.fail("Invalid base64 output")
        
        # 可以解密
        cipher2 = RC4Cipher(key)
        decrypted = cipher2.decrypt_from_base64(b64_encrypted)
        self.assertEqual(plaintext, decrypted)
    
    def test_convenience_functions(self):
        """测试便捷函数"""
        key = 'test_key'
        plaintext = b'Test data'
        
        # rc4_encrypt/rc4_decrypt
        encrypted = rc4_encrypt(plaintext, key)
        decrypted = rc4_decrypt(encrypted, key)
        self.assertEqual(plaintext, decrypted)
        
        # rc4_encrypt_hex/rc4_decrypt_hex
        hex_enc = rc4_encrypt_hex(plaintext, key)
        hex_dec = rc4_decrypt_hex(hex_enc, key)
        self.assertEqual(plaintext, hex_dec)
        
        # rc4_encrypt_b64/rc4_decrypt_b64
        b64_enc = rc4_encrypt_b64(plaintext, key)
        b64_dec = rc4_decrypt_b64(b64_enc, key)
        self.assertEqual(plaintext, b64_dec)


class TestRC4DropVariants(unittest.TestCase):
    """RC4-drop 变体测试"""
    
    def test_rc4_drop_basic(self):
        """测试基本 RC4-drop"""
        key = b'key'
        plaintext = b'Hello, RC4-drop!'
        
        cipher = RC4Drop(key, drop_bytes=256)
        encrypted = cipher.encrypt(plaintext)
        
        cipher2 = RC4Drop(key, drop_bytes=256)
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_rc4_drop256(self):
        """测试 RC4Drop256"""
        key = b'key'
        plaintext = b'Test data'
        
        cipher = RC4Drop256(key)
        encrypted = cipher.encrypt(plaintext)
        
        cipher2 = RC4Drop256(key)
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_rc4_drop768(self):
        """测试 RC4Drop768"""
        key = b'key'
        plaintext = b'Test data'
        
        cipher = RC4Drop768(key)
        encrypted = cipher.encrypt(plaintext)
        
        cipher2 = RC4Drop768(key)
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_rc4_drop3072(self):
        """测试 RC4Drop3072"""
        key = b'key'
        plaintext = b'Test data'
        
        cipher = RC4Drop3072(key)
        encrypted = cipher.encrypt(plaintext)
        
        cipher2 = RC4Drop3072(key)
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_drop_different_from_standard(self):
        """测试 drop 变体与标准 RC4 产生不同输出"""
        key = b'key'
        plaintext = b'Test data'
        
        standard = RC4Cipher(key)
        enc_standard = standard.encrypt(plaintext)
        
        drop = RC4Drop256(key)
        enc_drop = drop.encrypt(plaintext)
        
        # 两者应该产生不同的输出
        self.assertNotEqual(enc_standard, enc_drop)
    
    def test_different_drop_values(self):
        """测试不同丢弃值产生不同输出"""
        key = b'key'
        plaintext = b'Test data'
        
        drop256 = RC4Drop256(key)
        enc256 = drop256.encrypt(plaintext)
        
        drop768 = RC4Drop768(key)
        enc768 = drop768.encrypt(plaintext)
        
        # 不同丢弃值应该产生不同输出
        self.assertNotEqual(enc256, enc768)


class TestRC4KnownVectors(unittest.TestCase):
    """已知测试向量验证"""
    
    def test_rc4_deterministic(self):
        """
        测试 RC4 加密确定性
        
        RC4 是确定性流加密：相同密钥和明文总是产生相同密文。
        这是 RC4 的基本特性。
        """
        key = bytes([0x01, 0x02, 0x03, 0x04, 0x05])
        plaintext = bytes(8)  # 8 个零字节
        
        # 多次加密应该产生相同结果
        cipher1 = RC4Cipher(key)
        encrypted1 = cipher1.encrypt(plaintext)
        
        cipher2 = RC4Cipher(key)
        encrypted2 = cipher2.encrypt(plaintext)
        
        self.assertEqual(encrypted1, encrypted2)
        
        # 解密应该恢复原文
        cipher3 = RC4Cipher(key)
        decrypted = cipher3.decrypt(encrypted1)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_wikipedia_vector(self):
        """
        测试 Wikipedia 提供的测试向量
        
        Key: "Key"
        Plaintext: "Plaintext"
        Expected ciphertext: BBF316E8D940AF0AD3
        """
        key = b'Key'
        plaintext = b'Plaintext'
        
        cipher = RC4Cipher(key)
        encrypted = cipher.encrypt(plaintext)
        
        # 预期密文（十六进制）
        expected_hex = 'bbf316e8d940af0ad3'
        
        self.assertEqual(encrypted.hex(), expected_hex)
    
    def test_another_known_vector(self):
        """
        测试另一个已知向量
        
        Key: "password"
        Plaintext: "hello"
        """
        key = b'password'
        plaintext = b'hello'
        
        cipher = RC4Cipher(key)
        encrypted = cipher.encrypt(plaintext)
        
        # 验证加密再解密能恢复原文
        cipher2 = RC4Cipher(key)
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)
        
        # 验证确定性：相同密钥和明文总是产生相同密文
        cipher3 = RC4Cipher(key)
        encrypted2 = cipher3.encrypt(plaintext)
        self.assertEqual(encrypted, encrypted2)


class TestRC4ErrorHandling(unittest.TestCase):
    """错误处理测试"""
    
    def test_none_plaintext_error(self):
        """测试 None 明文抛出错误"""
        cipher = RC4Cipher(b'key')
        
        with self.assertRaises(RC4Error):
            cipher.encrypt(None)
    
    def test_none_ciphertext_error(self):
        """测试 None 密文抛出错误"""
        cipher = RC4Cipher(b'key')
        
        with self.assertRaises(RC4Error):
            cipher.decrypt(None)
    
    def test_invalid_hex_error(self):
        """测试无效十六进制字符串抛出错误"""
        cipher = RC4Cipher(b'key')
        
        with self.assertRaises(RC4Error):
            cipher.decrypt_from_hex('not_valid_hex!')
    
    def test_invalid_base64_error(self):
        """测试无效 Base64 字符串抛出错误"""
        cipher = RC4Cipher(b'key')
        
        with self.assertRaises(RC4Error):
            cipher.decrypt_from_base64('not valid base64!!!')


class TestRC4Reusability(unittest.TestCase):
    """加密器重用测试"""
    
    def test_multiple_encryptions_fresh_state(self):
        """测试多次加密使用新实例"""
        key = b'key'
        plaintext = b'test'
        
        # 每次加密都应该使用新的状态
        cipher1 = RC4Cipher(key)
        enc1 = cipher1.encrypt(plaintext)
        
        cipher2 = RC4Cipher(key)
        enc2 = cipher2.encrypt(plaintext)
        
        # 相同密钥和明文应该产生相同密文
        self.assertEqual(enc1, enc2)
    
    def test_state_not_persistent(self):
        """测试状态不持久"""
        key = b'key'
        
        # 第一个实例
        cipher = RC4Cipher(key)
        enc1 = cipher.encrypt(b'data1')
        
        # 重置后加密不同数据
        cipher2 = RC4Cipher(key)
        enc2 = cipher2.encrypt(b'data2')
        
        # 不应该抛出异常
        self.assertIsInstance(enc1, bytes)
        self.assertIsInstance(enc2, bytes)


class TestRC4EdgeCases(unittest.TestCase):
    """边界条件测试"""
    
    def test_all_byte_values(self):
        """测试所有字节值"""
        key = b'key'
        plaintext = bytes(range(256))
        
        cipher = RC4Cipher(key)
        encrypted = cipher.encrypt(plaintext)
        
        cipher2 = RC4Cipher(key)
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_long_key(self):
        """测试长密钥（接近 256 字节）"""
        key = b'x' * 255
        plaintext = b'test'
        
        cipher = RC4Cipher(key)
        encrypted = cipher.encrypt(plaintext)
        
        cipher2 = RC4Cipher(key)
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_binary_data(self):
        """测试二进制数据"""
        key = b'binary_key'
        plaintext = bytes([0, 128, 255, 1, 127, 64])
        
        cipher = RC4Cipher(key)
        encrypted = cipher.encrypt(plaintext)
        
        cipher2 = RC4Cipher(key)
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_repeated_encryption_decryption(self):
        """测试重复加密解密"""
        key = b'key'
        data = b'original'
        
        for _ in range(10):
            cipher = RC4Cipher(key)
            encrypted = cipher.encrypt(data)
            
            cipher2 = RC4Cipher(key)
            decrypted = cipher2.decrypt(encrypted)
            
            self.assertEqual(data, decrypted)
            data = encrypted  # 下一轮使用加密后的数据


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)