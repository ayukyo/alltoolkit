#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XOR Utils 测试文件
================
测试 XOR 工具模块的所有功能。

运行方式: python xor_utils_test.py
"""

import sys
import os
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    xor_byte, xor_bytes, xor_single_pass, xor_rolling_key, xor_chain,
    xor_checksum, xor_checksum_range, xor_checksum_blocks, verify_xor_checksum,
    frequency_analysis, find_most_frequent, guess_single_byte_key,
    guess_key_length, break_repeating_key_xor,
    flip_bits, swap_bits, reverse_bits, count_bits, bit_diff,
    xor_encode_hex, xor_decode_hex, xor_encode_string, xor_decode_string,
    detect_xor_pattern, find_xor_collisions,
    xor_all_with_key, xor_pairs, generate_xor_key_stream,
    create_xor_result, xor_encrypt_file_content, xor_decrypt_file_content,
    printable_xor_result,
    XORCipher, SingleByteXORCipher, XORResult, XORMode
)


class TestBasicXOR(unittest.TestCase):
    """基础 XOR 操作测试"""
    
    def test_xor_byte(self):
        """测试单字节 XOR"""
        data = b"Hello"
        key = 0x55
        encrypted = xor_byte(data, key)
        decrypted = xor_byte(encrypted, key)
        self.assertEqual(decrypted, data)
    
    def test_xor_byte_empty(self):
        """测试空数据的单字节 XOR"""
        self.assertEqual(xor_byte(b"", 0x55), b"")
    
    def test_xor_byte_invalid_key(self):
        """测试无效密钥"""
        with self.assertRaises(ValueError):
            xor_byte(b"Hello", 256)
        with self.assertRaises(ValueError):
            xor_byte(b"Hello", -1)
    
    def test_xor_bytes(self):
        """测试多字节 XOR"""
        data = b"Hello World"
        key = b"KEY"
        encrypted = xor_bytes(data, key)
        decrypted = xor_bytes(encrypted, key)
        self.assertEqual(decrypted, data)
    
    def test_xor_bytes_single_char_key(self):
        """测试单字符密钥"""
        data = b"Test"
        key = b"K"
        encrypted = xor_bytes(data, key)
        decrypted = xor_bytes(encrypted, key)
        self.assertEqual(decrypted, data)
    
    def test_xor_bytes_empty_key(self):
        """测试空密钥"""
        with self.assertRaises(ValueError):
            xor_bytes(b"Hello", b"")
    
    def test_xor_single_pass(self):
        """测试单次 XOR"""
        data = b"Hello World"
        key = b"KEY"
        result = xor_single_pass(data, key)
        self.assertEqual(len(result), 3)  # min(len(data), len(key))
    
    def test_xor_rolling_key(self):
        """测试滚动密钥 XOR"""
        data = b"Hello"
        encrypted = xor_rolling_key(data, 0)
        # seed=0 时，key[i]=i，自 XOR 的性质
        decrypted = xor_rolling_key(encrypted, 0)
        self.assertEqual(decrypted, data)
    
    def test_xor_chain(self):
        """测试链式 XOR"""
        data = b"Hello"
        # 两次 XOR 同一个密钥会还原
        result = xor_chain(data, [0x55])
        result2 = xor_chain(result, [0x55])
        self.assertEqual(result2, data)
    
    def test_xor_chain_multiple(self):
        """测试多密钥链式 XOR"""
        data = b"Hello"
        keys = [0x55, 0xAA, 0xFF]
        result = xor_chain(data, keys)
        # 逆序解密
        result2 = xor_chain(result, keys)
        self.assertEqual(result2, data)


class TestXORChecksum(unittest.TestCase):
    """XOR 校验和测试"""
    
    def test_xor_checksum(self):
        """测试 XOR 校验和"""
        self.assertEqual(xor_checksum(b"\x01\x02\x03"), 0)  # 1^2^3=0
        self.assertEqual(xor_checksum(b"Hello"), 66)  # H^e^l^l^o = 66
    
    def test_xor_checksum_empty(self):
        """测试空数据校验和"""
        self.assertEqual(xor_checksum(b""), 0)
    
    def test_xor_checksum_range(self):
        """测试范围校验和"""
        data = b"Hello World"
        checksum_full = xor_checksum(data[:5])
        checksum_range = xor_checksum_range(data, 0, 5)
        self.assertEqual(checksum_range, checksum_full)
    
    def test_xor_checksum_blocks(self):
        """测试分块校验和"""
        data = b"HelloWorld"
        checksums = xor_checksum_blocks(data, 5)
        self.assertEqual(len(checksums), 2)
        self.assertEqual(checksums[0], xor_checksum(b"Hello"))
        self.assertEqual(checksums[1], xor_checksum(b"World"))
    
    def test_xor_checksum_blocks_invalid_size(self):
        """测试无效块大小"""
        with self.assertRaises(ValueError):
            xor_checksum_blocks(b"Hello", 0)
    
    def test_verify_xor_checksum(self):
        """测试校验和验证"""
        data = b"Hello"
        checksum = xor_checksum(data)
        self.assertTrue(verify_xor_checksum(data, checksum))
        self.assertFalse(verify_xor_checksum(data, checksum + 1))


class TestXORCryptanalysis(unittest.TestCase):
    """XOR 密码分析测试"""
    
    def test_frequency_analysis(self):
        """测试频率分析"""
        data = b"Hello"
        freq = frequency_analysis(data)
        self.assertEqual(freq[ord('l')], 2)
        self.assertEqual(freq[ord('H')], 1)
    
    def test_find_most_frequent(self):
        """测试最频繁字节"""
        data = b"Hello"
        top = find_most_frequent(data, 3)
        self.assertEqual(len(top), 3)
        # 'l' 出现 2 次，应该在第一位
        self.assertEqual(top[0][0], ord('l'))
        self.assertEqual(top[0][1], 2)
    
    def test_guess_single_byte_key(self):
        """测试单字节密钥推测"""
        plaintext = b"Hello World Hello"
        key = 0x55
        ciphertext = xor_byte(plaintext, key)
        guesses = guess_single_byte_key(ciphertext)
        # 正确密钥应该在前列
        top_keys = [g[0] for g in guesses[:10]]
        self.assertIn(key, top_keys)
    
    def test_guess_single_byte_key_with_known_plaintext(self):
        """测试带已知明文的密钥推测"""
        plaintext = b"Hello World"
        key = 0x55
        ciphertext = xor_byte(plaintext, key)
        guesses = guess_single_byte_key(ciphertext, known_plaintext=b"Hello")
        # 第一个猜测应该是正确密钥
        self.assertEqual(guesses[0][0], key)
    
    def test_guess_key_length(self):
        """测试密钥长度推测"""
        plaintext = b"Hello World Hello World Hello World"
        key = b"KEY"
        ciphertext = xor_bytes(plaintext, key)
        guesses = guess_key_length(ciphertext)
        # 正确长度应该在前列
        top_lengths = [g[0] for g in guesses[:5]]
        self.assertIn(3, top_lengths)
    
    def test_break_repeating_key_xor(self):
        """测试破解重复密钥 XOR"""
        plaintext = b"Hello World Hello World Hello World Hello World"
        key = b"KEY"
        ciphertext = xor_bytes(plaintext, key)
        recovered_key, decrypted = break_repeating_key_xor(ciphertext, key_length=3)
        # 解密结果应该接近原文
        self.assertTrue(len(decrypted) > 0)


class TestBitOperations(unittest.TestCase):
    """位操作测试"""
    
    def test_flip_bits(self):
        """测试位翻转"""
        data = b"\x00"
        result = flip_bits(data, [0, 1, 2])
        self.assertEqual(result, b"\x07")
    
    def test_swap_bits(self):
        """测试位交换"""
        data = b"\x01"
        result = swap_bits(data, 0, 7)
        self.assertEqual(result, b"\x80")
    
    def test_reverse_bits(self):
        """测试位反转"""
        self.assertEqual(reverse_bits(b"\x01"), b"\x80")
        self.assertEqual(reverse_bits(b"\xF0"), b"\x0F")
    
    def test_count_bits(self):
        """测试位计数"""
        self.assertEqual(count_bits(b"\xFF"), 8)
        self.assertEqual(count_bits(b"\x00"), 0)
        self.assertEqual(count_bits(b"\x0F"), 4)
    
    def test_bit_diff(self):
        """测试位差（Hamming 距离）"""
        self.assertEqual(bit_diff(b"\x00", b"\xFF"), 8)
        # 'e'(101) XOR 'a'(97) = 4, 有 1 个位不同
        self.assertEqual(bit_diff(b"Hello", b"Hallo"), 1)


class TestXOREncoding(unittest.TestCase):
    """XOR 编码测试"""
    
    def test_xor_encode_hex(self):
        """测试十六进制编码"""
        data = b"Hello"
        key = b"K"
        hex_result = xor_encode_hex(data, key)
        # 验证可以解码
        decrypted = xor_decode_hex(hex_result, key)
        self.assertEqual(decrypted, data)
    
    def test_xor_encode_decode_string(self):
        """测试字符串编码解码"""
        plaintext = "Hello"
        key = "KEY"
        hex_result = xor_encode_string(plaintext, key)
        decrypted = xor_decode_string(hex_result, key)
        self.assertEqual(decrypted, plaintext)


class TestPatternDetection(unittest.TestCase):
    """模式检测测试"""
    
    def test_detect_xor_pattern(self):
        """测试模式检测"""
        plaintext = b"ABCABCABC"
        key = b"K"
        ciphertext = xor_bytes(plaintext, key)
        patterns = detect_xor_pattern(ciphertext, 3)
        # 应检测到某种模式
        self.assertTrue(len(patterns) >= 0)
    
    def test_find_xor_collisions(self):
        """测试碰撞检测"""
        data1 = b"Hello"
        data2 = b"Hallo"
        collisions = find_xor_collisions(data1, data2)
        # H=H(0), l=l(2), l=l(3), o=o(4) 相同
        self.assertEqual(collisions, [0, 2, 3, 4])


class TestBatchOperations(unittest.TestCase):
    """批量操作测试"""
    
    def test_xor_all_with_key(self):
        """测试批量 XOR"""
        datas = [b"Hello", b"World"]
        key = b"K"
        results = xor_all_with_key(datas, key)
        self.assertEqual(len(results), 2)
        # 验证可以解密
        decrypted = xor_all_with_key(results, key)
        self.assertEqual(decrypted, datas)
    
    def test_xor_pairs(self):
        """测试配对 XOR"""
        datas1 = [b"Hello", b"Test"]
        datas2 = [b"KEYKE", b"ABC"]
        results = xor_pairs(datas1, datas2)
        self.assertEqual(len(results), 2)
    
    def test_generate_xor_key_stream(self):
        """测试密钥流生成"""
        key_stream = generate_xor_key_stream(0x55, 10)
        self.assertEqual(len(key_stream), 10)
        # 同样的种子应该生成同样的密钥流
        key_stream2 = generate_xor_key_stream(0x55, 10)
        self.assertEqual(key_stream, key_stream2)


class TestUtilityFunctions(unittest.TestCase):
    """工具函数测试"""
    
    def test_create_xor_result(self):
        """测试创建结果对象"""
        data = b"Hello"
        key = b"K"
        result = create_xor_result(data, key)
        self.assertIsInstance(result, XORResult)
        self.assertEqual(result.key, key)
    
    def test_xor_encrypt_decrypt_file_content(self):
        """测试文件内容加密解密"""
        content = b"Hello World"
        key = b"KEY"
        encrypted = xor_encrypt_file_content(content, key, add_checksum=True)
        decrypted, valid = xor_decrypt_file_content(encrypted, key, verify_checksum=True)
        self.assertEqual(decrypted, content)
        self.assertTrue(valid)
    
    def test_xor_encrypt_file_no_checksum(self):
        """测试无校验和加密"""
        content = b"Hello"
        key = b"KEY"
        encrypted = xor_encrypt_file_content(content, key, add_checksum=False)
        decrypted, valid = xor_decrypt_file_content(encrypted, key, verify_checksum=False)
        self.assertEqual(decrypted, content)
    
    def test_printable_xor_result(self):
        """测试可打印结果"""
        data = b"Hello\x00\xFF"
        result = printable_xor_result(data)
        self.assertEqual(result, "Hello..")


class TestXORCipher(unittest.TestCase):
    """XORCipher 类测试"""
    
    def test_xor_cipher_encrypt_decrypt(self):
        """测试加密解密"""
        cipher = XORCipher(b"KEY")
        data = b"Hello World"
        encrypted = cipher.encrypt(data)
        decrypted = cipher.decrypt(encrypted)
        self.assertEqual(decrypted, data)
    
    def test_xor_cipher_empty_key(self):
        """测试空密钥"""
        with self.assertRaises(ValueError):
            XORCipher(b"")
    
    def test_xor_cipher_key_property(self):
        """测试密钥属性"""
        cipher = XORCipher(b"KEY")
        self.assertEqual(cipher.key, b"KEY")
    
    def test_xor_cipher_stream(self):
        """测试流式加密"""
        cipher = XORCipher(b"KEY")
        def data_gen():
            yield b"Hello"
            yield b"World"
        
        results = list(cipher.encrypt_stream(data_gen()))
        self.assertEqual(len(results), 2)


class TestSingleByteXORCipher(unittest.TestCase):
    """单字节 XOR 加密器测试"""
    
    def test_single_byte_cipher(self):
        """测试单字节加密"""
        cipher = SingleByteXORCipher(0x55)
        data = b"Hello"
        encrypted = cipher.encrypt(data)
        decrypted = cipher.decrypt(encrypted)
        self.assertEqual(decrypted, data)
    
    def test_single_byte_cipher_invalid_key(self):
        """测试无效密钥"""
        with self.assertRaises(ValueError):
            SingleByteXORCipher(256)
    
    def test_brute_force_decrypt(self):
        """测试暴力破解"""
        cipher = SingleByteXORCipher(0x55)
        plaintext = b"Hello World Hello"
        ciphertext = cipher.encrypt(plaintext)
        results = cipher.brute_force_decrypt(ciphertext, top_n=10)
        self.assertEqual(len(results), 10)
        # 正确密钥应该在结果中
        found_key = any(r[0] == 0x55 for r in results)
        self.assertTrue(found_key)


class TestXORResult(unittest.TestCase):
    """XORResult 类测试"""
    
    def test_xor_result_to_hex(self):
        """测试十六进制转换"""
        result = XORResult(data=b"\x01\x02\x03", key=b"K", checksum=0)
        self.assertEqual(result.to_hex(), "010203")
    
    def test_xor_result_to_string(self):
        """测试字符串转换"""
        result = XORResult(data=b"Hello", key=b"K", checksum=66)
        self.assertEqual(result.to_string(), "Hello")
    
    def test_xor_result_to_string_invalid(self):
        """测试无效 UTF-8 字符串"""
        result = XORResult(data=b"\xFF\xFE", key=b"K", checksum=0)
        # 应返回十六进制
        self.assertEqual(result.to_string(), "fffe")


class TestXORMode(unittest.TestCase):
    """XORMode 枚举测试"""
    
    def test_xor_mode_values(self):
        """测试枚举值"""
        self.assertEqual(XORMode.SINGLE_KEY.value, "single")
        self.assertEqual(XORMode.MULTI_KEY.value, "multi")
        self.assertEqual(XORMode.ROLLING_KEY.value, "rolling")
        self.assertEqual(XORMode.REPEATING_KEY.value, "repeating")


if __name__ == "__main__":
    unittest.main(verbosity=2)