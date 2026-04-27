#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Secrets Utilities Test Suite
==========================================
Comprehensive test suite for the secrets_utils module.

Coverage:
    - Password generation with various configurations
    - Passphrase generation
    - API key and token generation
    - Password strength evaluation
    - Secret hashing and verification
    - TOTP generation and verification
    - Secure random utilities
    - Edge cases and error handling

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os
import time
import unittest
from typing import List, Tuple

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Password generation
    generate_password,
    generate_passphrase,
    LOWERCASE,
    UPPERCASE,
    DIGITS,
    SPECIAL,
    
    # API key generation
    generate_api_key,
    generate_bearer_token,
    generate_session_id,
    
    # Password strength
    evaluate_password_strength,
    is_password_strong,
    
    # Hashing
    hash_secret,
    verify_secret,
    
    # TOTP
    generate_totp,
    verify_totp,
    generate_totp_secret,
    
    # Secure random
    secure_random_int,
    secure_random_bytes,
    secure_random_hex,
    secure_shuffle,
    secure_choice,
    
    # Utilities
    is_secure_string,
    compare_secrets,
    mask_secret,
)


# ============================================================================
# Password Generation Tests
# ============================================================================

class TestPasswordGeneration(unittest.TestCase):
    
    def test_generate_password_default(self):
        """测试默认密码生成"""
        password = generate_password()
        self.assertEqual(len(password), 16)
        self.assertIsInstance(password, str)
    
    def test_generate_password_custom_length(self):
        """测试自定义长度密码生成"""
        for length in [8, 12, 20, 32, 64]:
            password = generate_password(length=length)
            self.assertEqual(len(password), length)
    
    def test_generate_password_minimum_length(self):
        """测试最小长度限制"""
        password = generate_password(length=4)
        self.assertEqual(len(password), 4)
    
    def test_generate_password_too_short(self):
        """测试长度过短抛出异常"""
        with self.assertRaises(ValueError):
            generate_password(length=3)
    
    def test_generate_password_no_lowercase(self):
        """测试不包含小写字母"""
        password = generate_password(length=20, use_lowercase=False)
        self.assertTrue(all(c not in LOWERCASE for c in password))
    
    def test_generate_password_no_uppercase(self):
        """测试不包含大写字母"""
        password = generate_password(length=20, use_uppercase=False)
        self.assertTrue(all(c not in UPPERCASE for c in password))
    
    def test_generate_password_no_digits(self):
        """测试不包含数字"""
        password = generate_password(length=20, use_digits=False)
        self.assertTrue(all(c not in DIGITS for c in password))
    
    def test_generate_password_no_special(self):
        """测试不包含特殊字符"""
        password = generate_password(length=20, use_special=False)
        self.assertTrue(all(c not in SPECIAL for c in password))
    
    def test_generate_password_with_all_types(self):
        """测试包含所有字符类型"""
        password = generate_password(length=20, use_lowercase=True, use_uppercase=True, 
                                      use_digits=True, use_special=True)
        has_lower = any(c in LOWERCASE for c in password)
        has_upper = any(c in UPPERCASE for c in password)
        has_digit = any(c in DIGITS for c in password)
        has_special = any(c in SPECIAL for c in password)
        
        self.assertTrue(has_lower)
        self.assertTrue(has_upper)
        self.assertTrue(has_digit)
        self.assertTrue(has_special)
    
    def test_generate_password_exclude_ambiguous(self):
        """测试排除易混淆字符"""
        password = generate_password(length=20, exclude_ambiguous=True)
        ambiguous_chars = 'l1IO0|;'
        self.assertTrue(all(c not in ambiguous_chars for c in password))
    
    def test_generate_password_no_char_sets(self):
        """测试未选择任何字符集抛出异常"""
        with self.assertRaises(ValueError):
            generate_password(use_lowercase=False, use_uppercase=False, 
                            use_digits=False, use_special=False)
    
    def test_generate_password_uniqueness(self):
        """测试密码唯一性"""
        passwords = [generate_password() for _ in range(100)]
        unique_passwords = set(passwords)
        self.assertEqual(len(unique_passwords), 100)


class TestPassphraseGeneration(unittest.TestCase):
    
    def test_generate_passphrase_default(self):
        """测试默认短语生成"""
        passphrase = generate_passphrase()
        words = passphrase.split('-')
        self.assertEqual(len(words), 4)
    
    def test_generate_passphrase_custom_words(self):
        """测试自定义单词数量"""
        for count in [1, 3, 5, 8]:
            passphrase = generate_passphrase(word_count=count)
            words = passphrase.split('-')
            self.assertEqual(len(words), count)
    
    def test_generate_passphrase_custom_separator(self):
        """测试自定义分隔符"""
        passphrase = generate_passphrase(separator='_')
        self.assertIn('_', passphrase)
        self.assertNotIn('-', passphrase)
    
    def test_generate_passphrase_custom_word_list(self):
        """测试自定义单词列表"""
        custom_words = ['apple', 'banana', 'cherry', 'date', 'elderberry']
        passphrase = generate_passphrase(word_count=3, word_list=custom_words)
        words = passphrase.split('-')
        for word in words:
            self.assertIn(word, custom_words)
    
    def test_generate_passphrase_zero_words(self):
        """测试零个单词抛出异常"""
        with self.assertRaises(ValueError):
            generate_passphrase(word_count=0)
    
    def test_generate_passphrase_uniqueness(self):
        """测试短语唯一性"""
        passphrases = [generate_passphrase() for _ in range(50)]
        unique_passphrases = set(passphrases)
        self.assertEqual(len(unique_passphrases), 50)


# ============================================================================
# API Key Generation Tests
# ============================================================================

class TestApiKeyGeneration(unittest.TestCase):
    
    def test_generate_api_key_default(self):
        """测试默认 API 密钥生成"""
        api_key = generate_api_key()
        self.assertTrue(api_key.startswith('ak_'))
        self.assertGreater(len(api_key), 10)
    
    def test_generate_api_key_custom_prefix(self):
        """测试自定义前缀"""
        api_key = generate_api_key(prefix='sk')
        self.assertTrue(api_key.startswith('sk_'))
    
    def test_generate_api_key_empty_prefix(self):
        """测试空前缀"""
        api_key = generate_api_key(prefix='')
        self.assertTrue(api_key.startswith('_'))
    
    def test_generate_bearer_token(self):
        """测试 bearer token 生成"""
        token = generate_bearer_token()
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 50)
    
    def test_generate_session_id(self):
        """测试 session ID 生成"""
        session_id = generate_session_id()
        self.assertTrue(session_id.startswith('sess_'))
        self.assertIn('_', session_id[5:])  # Should have timestamp separator
    
    def test_generate_session_id_custom_prefix(self):
        """测试自定义 session 前缀"""
        session_id = generate_session_id(prefix='user')
        self.assertTrue(session_id.startswith('user_'))


# ============================================================================
# Password Strength Tests
# ============================================================================

class TestPasswordStrength(unittest.TestCase):
    
    def test_evaluate_very_weak(self):
        """测试非常弱密码评估"""
        score, strength, suggestions = evaluate_password_strength("abc")
        self.assertLess(score, 25)
        self.assertEqual(strength, "Very Weak")
        self.assertGreater(len(suggestions), 0)
    
    def test_evaluate_weak(self):
        """测试弱密码评估"""
        score, strength, suggestions = evaluate_password_strength("abcdef")
        self.assertLess(score, 50)
    
    def test_evaluate_moderate(self):
        """测试中等强度密码评估"""
        # Need stronger password for moderate rating
        score, strength, suggestions = evaluate_password_strength("Abcdef12!@")
        self.assertGreaterEqual(score, 50)
        self.assertLess(score, 70)
    
    def test_evaluate_strong(self):
        """测试强密码评估"""
        score, strength, suggestions = evaluate_password_strength("MyStr0ng!Pass")
        self.assertGreaterEqual(score, 70)
        self.assertLess(score, 85)
    
    def test_evaluate_very_strong(self):
        """测试非常强密码评估"""
        score, strength, suggestions = evaluate_password_strength("Str0ng!Pass#2024@Secure")
        self.assertGreaterEqual(score, 85)
        self.assertEqual(strength, "Very Strong")
    
    def test_evaluate_common_pattern(self):
        """测试常见模式检测"""
        score, strength, suggestions = evaluate_password_strength("password123")
        self.assertLess(score, 50)
        self.assertTrue(any("common" in s.lower() or "pattern" in s.lower() for s in suggestions))
    
    def test_evaluate_repeated_chars(self):
        """测试重复字符检测"""
        score, strength, suggestions = evaluate_password_strength("aaaBBB111!!!")
        self.assertTrue(any("repeated" in s.lower() for s in suggestions))
    
    def test_is_password_strong(self):
        """测试密码强度判断"""
        self.assertTrue(is_password_strong("MyStr0ng!Pass#2024"))
        self.assertFalse(is_password_strong("weak"))
        self.assertFalse(is_password_strong("12345678"))
    
    def test_is_password_strong_custom_threshold(self):
        """测试自定义强度阈值"""
        self.assertFalse(is_password_strong("Abcdef12", min_score=90))
        self.assertTrue(is_password_strong("Abcdef12", min_score=30))


# ============================================================================
# Hashing Tests
# ============================================================================

class TestHashing(unittest.TestCase):
    
    def test_hash_secret_default(self):
        """测试默认哈希"""
        hashed = hash_secret("my_password")
        self.assertTrue(hashed.startswith('sha256:'))
        self.assertIn(':', hashed)
    
    def test_hash_secret_sha512(self):
        """测试 SHA512 哈希"""
        hashed = hash_secret("my_password", algorithm='sha512')
        self.assertTrue(hashed.startswith('sha512:'))
    
    def test_hash_secret_custom_iterations(self):
        """测试自定义迭代次数"""
        hashed = hash_secret("my_password", iterations=50000)
        self.assertIn('50000', hashed)
    
    def test_hash_secret_custom_salt(self):
        """测试自定义盐值"""
        hashed = hash_secret("my_password", salt='custom_salt')
        self.assertIn('custom_salt', hashed)
    
    def test_verify_secret_correct(self):
        """测试正确密码验证"""
        password = "my_secure_password_123!"
        hashed = hash_secret(password)
        self.assertTrue(verify_secret(password, hashed))
    
    def test_verify_secret_incorrect(self):
        """测试错误密码验证"""
        password = "my_secure_password_123!"
        hashed = hash_secret(password)
        self.assertFalse(verify_secret("wrong_password", hashed))
    
    def test_verify_secret_invalid_hash(self):
        """测试无效哈希格式"""
        self.assertFalse(verify_secret("password", "invalid_hash_format"))
        self.assertFalse(verify_secret("password", ""))
        self.assertFalse(verify_secret("password", "sha256:only:two:parts"))
    
    def test_hash_deterministic(self):
        """测试相同密码相同盐值产生相同哈希"""
        password = "test_password"
        salt = "fixed_salt"
        hashed1 = hash_secret(password, salt=salt)
        hashed2 = hash_secret(password, salt=salt)
        self.assertEqual(hashed1, hashed2)
    
    def test_hash_different_salt(self):
        """测试相同密码不同盐值产生不同哈希"""
        password = "test_password"
        hashed1 = hash_secret(password)
        hashed2 = hash_secret(password)
        self.assertNotEqual(hashed1, hashed2)


# ============================================================================
# TOTP Tests
# ============================================================================

class TestTOTP(unittest.TestCase):
    
    def test_generate_totp_format(self):
        """测试 TOTP 格式"""
        secret = 'JBSWY3DPEHPK3PXP'
        code = generate_totp(secret)
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())
    
    def test_generate_totp_custom_digits(self):
        """测试自定义位数 TOTP"""
        secret = 'JBSWY3DPEHPK3PXP'
        code = generate_totp(secret, digits=8)
        self.assertEqual(len(code), 8)
        self.assertTrue(code.isdigit())
    
    def test_generate_totp_deterministic(self):
        """测试相同时间相同输出"""
        secret = 'JBSWY3DPEHPK3PXP'
        timestamp = 1234567890.0
        code1 = generate_totp(secret, timestamp=timestamp)
        code2 = generate_totp(secret, timestamp=timestamp)
        self.assertEqual(code1, code2)
    
    def test_generate_totp_time_based(self):
        """测试 TOTP 基于时间变化"""
        secret = 'JBSWY3DPEHPK3PXP'
        code1 = generate_totp(secret, timestamp=1000000.0)
        code2 = generate_totp(secret, timestamp=1000030.0)  # 30 seconds later
        self.assertNotEqual(code1, code2)
    
    def test_verify_totp_correct(self):
        """测试正确 TOTP 验证"""
        secret = generate_totp_secret()
        code = generate_totp(secret)
        self.assertTrue(verify_totp(secret, code))
    
    def test_verify_totp_window(self):
        """测试 TOTP 时间窗口验证"""
        secret = 'JBSWY3DPEHPK3PXP'
        current_time = time.time()
        # Generate code for 30 seconds ago
        old_code = generate_totp(secret, timestamp=current_time - 30)
        # Should still be valid with window=1
        self.assertTrue(verify_totp(secret, old_code, window=1))
    
    def test_verify_totp_invalid(self):
        """测试无效 TOTP 验证"""
        secret = 'JBSWY3DPEHPK3PXP'
        self.assertFalse(verify_totp(secret, "000000"))
        self.assertFalse(verify_totp(secret, "invalid"))
    
    def test_generate_totp_secret_format(self):
        """测试 TOTP 密钥格式"""
        secret = generate_totp_secret()
        self.assertIsInstance(secret, str)
        self.assertGreater(len(secret), 20)
        # Should be valid base32
        valid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567=')
        self.assertTrue(all(c in valid_chars for c in secret.upper()))
    
    def test_generate_totp_secret_uniqueness(self):
        """测试 TOTP 密钥唯一性"""
        secrets = [generate_totp_secret() for _ in range(50)]
        unique_secrets = set(secrets)
        self.assertEqual(len(unique_secrets), 50)


# ============================================================================
# Secure Random Tests
# ============================================================================

class TestSecureRandom(unittest.TestCase):
    
    def test_secure_random_int_range(self):
        """测试随机整数范围"""
        for _ in range(100):
            value = secure_random_int(1, 100)
            self.assertGreaterEqual(value, 1)
            self.assertLessEqual(value, 100)
    
    def test_secure_random_int_single_value(self):
        """测试单值范围"""
        value = secure_random_int(42, 42)
        self.assertEqual(value, 42)
    
    def test_secure_random_int_invalid_range(self):
        """测试无效范围抛出异常"""
        with self.assertRaises(ValueError):
            secure_random_int(100, 1)
    
    def test_secure_random_bytes_length(self):
        """测试随机字节长度"""
        for length in [1, 16, 32, 64, 128]:
            data = secure_random_bytes(length)
            self.assertEqual(len(data), length)
            self.assertIsInstance(data, bytes)
    
    def test_secure_random_hex_length(self):
        """测试随机十六进制长度"""
        for length in [16, 32, 64]:
            hex_str = secure_random_hex(length)
            self.assertEqual(len(hex_str), length)
            self.assertTrue(all(c in '0123456789abcdef' for c in hex_str))
    
    def test_secure_shuffle_length(self):
        """测试随机打乱长度"""
        original = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        shuffled = secure_shuffle(original)
        self.assertEqual(len(shuffled), len(original))
        self.assertEqual(set(shuffled), set(original))
    
    def test_secure_shuffle_original_unchanged(self):
        """测试原始列表不变"""
        original = [1, 2, 3, 4, 5]
        original_copy = original.copy()
        secure_shuffle(original)
        self.assertEqual(original, original_copy)
    
    def test_secure_choice_valid(self):
        """测试有效选择"""
        items = ['a', 'b', 'c', 'd', 'e']
        for _ in range(50):
            choice = secure_choice(items)
            self.assertIn(choice, items)
    
    def test_secure_choice_empty(self):
        """测试空列表抛出异常"""
        with self.assertRaises(ValueError):
            secure_choice([])
    
    def test_secure_random_uniqueness(self):
        """测试随机值唯一性"""
        values = [secure_random_hex(32) for _ in range(100)]
        unique_values = set(values)
        self.assertEqual(len(unique_values), 100)


# ============================================================================
# Utility Function Tests
# ============================================================================

class TestUtilities(unittest.TestCase):
    
    def test_is_secure_string_valid(self):
        """测试有效安全字符串"""
        self.assertTrue(is_secure_string("Abc123Def"))
        self.assertTrue(is_secure_string("Str0ng!Pass"))
    
    def test_is_secure_string_too_short(self):
        """测试过短字符串"""
        self.assertFalse(is_secure_string("Ab1"))
    
    def test_is_secure_string_no_uppercase(self):
        """测试无大写"""
        self.assertFalse(is_secure_string("abc123def"))
    
    def test_is_secure_string_no_lowercase(self):
        """测试无小写"""
        self.assertFalse(is_secure_string("ABC123DEF"))
    
    def test_is_secure_string_no_digit(self):
        """测试无数字"""
        self.assertFalse(is_secure_string("AbcdefGhi"))
    
    def test_is_secure_string_custom_length(self):
        """测试自定义长度"""
        self.assertTrue(is_secure_string("Ab1", min_length=3))
        self.assertFalse(is_secure_string("Ab1", min_length=4))
    
    def test_compare_secrets_equal(self):
        """测试相同密钥比较"""
        self.assertTrue(compare_secrets("secret1", "secret1"))
        self.assertTrue(compare_secrets("", ""))
    
    def test_compare_secrets_unequal(self):
        """测试不同密钥比较"""
        self.assertFalse(compare_secrets("secret1", "secret2"))
        self.assertFalse(compare_secrets("secret", "secret1"))
    
    def test_mask_secret_long(self):
        """测试长密钥掩码"""
        secret = "sk-1234567890abcdef"
        masked = mask_secret(secret)
        # 19 chars total, 4 visible each side = 11 asterisks
        self.assertEqual(masked, "sk-1***********cdef")
        self.assertNotIn("1234567890ab", masked)
    
    def test_mask_secret_short(self):
        """测试短密钥掩码"""
        secret = "short"
        masked = mask_secret(secret, visible_chars=2)
        # 5 chars total, 2 visible each side = 1 asterisk
        self.assertEqual(masked, "sh*rt")
        self.assertNotIn("hor", masked)
    
    def test_mask_secret_very_short(self):
        """测试非常短密钥掩码"""
        secret = "ab"
        masked = mask_secret(secret, visible_chars=4)
        self.assertEqual(masked, "**")
    
    def test_mask_secret_custom_visible(self):
        """测试自定义可见字符数"""
        secret = "abcdefghij"
        masked = mask_secret(secret, visible_chars=2)
        # 10 chars, 2 visible each side = 6 asterisks
        self.assertEqual(masked, "ab******ij")
        
        masked = mask_secret(secret, visible_chars=3)
        # 10 chars, 3 visible each side = 4 asterisks
        self.assertEqual(masked, "abc****hij")


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration(unittest.TestCase):
    
    def test_password_workflow(self):
        """测试完整密码工作流程"""
        # Generate password
        password = generate_password(length=16)
        
        # Evaluate strength
        score, strength, suggestions = evaluate_password_strength(password)
        
        # Should be strong
        self.assertGreaterEqual(score, 70)
        self.assertTrue(is_password_strong(password))
        
        # Hash it
        hashed = hash_secret(password)
        
        # Verify
        self.assertTrue(verify_secret(password, hashed))
        self.assertFalse(verify_secret("wrong", hashed))
    
    def test_totp_workflow(self):
        """测试完整 TOTP 工作流程"""
        # Generate secret
        secret = generate_totp_secret()
        
        # Generate code
        code = generate_totp(secret)
        
        # Verify code
        self.assertTrue(verify_totp(secret, code))
        
        # Verify old code within window
        old_code = generate_totp(secret, timestamp=time.time() - 25)
        self.assertTrue(verify_totp(secret, old_code, window=1))
    
    def test_api_key_workflow(self):
        """测试完整 API 密钥工作流程"""
        # Generate API key
        api_key = generate_api_key(prefix='test')
        
        # Store in environment
        from mod import store_secret_env, get_secret_env
        store_secret_env('TEST_API_KEY', api_key)
        
        # Retrieve from environment
        retrieved = get_secret_env('TEST_API_KEY')
        self.assertEqual(api_key, retrieved)
        
        # Mask for display - first 4 chars should be visible
        masked = mask_secret(api_key)
        self.assertTrue(api_key.startswith(masked[:4]))
        self.assertIn('***', masked)


# ============================================================================
# Run Tests
# ============================================================================

def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestPasswordGeneration,
        TestPassphraseGeneration,
        TestApiKeyGeneration,
        TestPasswordStrength,
        TestHashing,
        TestTOTP,
        TestSecureRandom,
        TestUtilities,
        TestIntegration,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    print("=" * 70)
    print("AllToolkit - Secrets Utilities Test Suite")
    print("=" * 70)
    print()
    
    result = run_tests()
    
    print()
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    print("=" * 70)
    
    sys.exit(0 if result.wasSuccessful() else 1)
