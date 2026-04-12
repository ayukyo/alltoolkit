"""
AllToolkit - Encryption Utils Test Suite

Comprehensive tests for encryption_utils module.
Covers hashing, HMAC, encryption, token generation, and more.
"""

import unittest
import sys
import os
import time
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Exceptions
    EncryptionError, DecryptionError,
    
    # Hashing
    hash_data, hash_file, verify_hash, hash_password, verify_password,
    HashAlgorithm, HashResult,
    
    # HMAC
    compute_hmac, verify_hmac,
    
    # XOR Encryption
    xor_encrypt, xor_decrypt,
    
    # Substitution Cipher
    SubstitutionCipher,
    
    # Base64
    base64_encode, base64_decode, url_safe_encode, url_safe_decode,
    
    # Token Generation
    generate_token, generate_api_key, generate_session_id,
    
    # Checksum
    compute_checksum, verify_checksum,
    
    # OTP
    generate_otp, otp_encrypt, otp_decrypt,
    
    # Secure Comparison
    secure_compare,
    
    # Key Derivation
    derive_key,
    
    # Utility Classes
    SecureString, HashChain,
    
    # Convenience
    quick_hash, quick_encrypt, quick_decrypt,
)


class TestHashing(unittest.TestCase):
    """Test hashing functions."""
    
    def test_hash_data_sha256(self):
        """Test SHA256 hashing."""
        result = hash_data("hello world")
        self.assertEqual(result.algorithm, HashAlgorithm.SHA256)
        self.assertEqual(len(result.hex_digest), 64)  # SHA256 = 256 bits = 64 hex chars
        self.assertIsInstance(result.bytes_digest, bytes)
        self.assertEqual(len(result.bytes_digest), 32)
    
    def test_hash_data_different_algorithms(self):
        """Test different hash algorithms."""
        data = "test data"
        
        algorithms = [
            HashAlgorithm.SHA256,
            HashAlgorithm.SHA512,
            HashAlgorithm.MD5,
            HashAlgorithm.SHA1,
        ]
        
        for algo in algorithms:
            with self.subTest(algorithm=algo):
                result = hash_data(data, algorithm=algo)
                self.assertEqual(result.algorithm, algo)
                self.assertTrue(len(result.hex_digest) > 0)
    
    def test_hash_data_with_salt(self):
        """Test hashing with salt."""
        data = "password"
        salt = "random_salt"
        
        result1 = hash_data(data, salt=salt)
        result2 = hash_data(data, salt=salt)
        result3 = hash_data(data, salt="different_salt")
        
        self.assertEqual(result1.hex_digest, result2.hex_digest)
        self.assertNotEqual(result1.hex_digest, result3.hex_digest)
    
    def test_hash_data_consistency(self):
        """Test hash consistency."""
        data = "consistent test"
        result1 = hash_data(data)
        result2 = hash_data(data)
        self.assertEqual(result1.hex_digest, result2.hex_digest)
    
    def test_hash_file(self):
        """Test file hashing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test file content")
            filepath = f.name
        
        try:
            result = hash_file(filepath)
            self.assertEqual(result.algorithm, HashAlgorithm.SHA256)
            self.assertTrue(len(result.hex_digest) > 0)
        finally:
            os.unlink(filepath)
    
    def test_verify_hash(self):
        """Test hash verification."""
        data = "verify this"
        result = hash_data(data)
        
        self.assertTrue(verify_hash(data, result.hex_digest))
        self.assertFalse(verify_hash("wrong data", result.hex_digest))
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "my_secure_password"
        hashed = hash_password(password)
        
        self.assertEqual(hashed['algorithm'], 'pbkdf2_sha256')
        self.assertIn('salt', hashed)
        self.assertIn('hash', hashed)
        self.assertIn('iterations', hashed)
    
    def test_verify_password(self):
        """Test password verification."""
        password = "test_password_123"
        hashed = hash_password(password)
        
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("wrong_password", hashed))
    
    def test_hash_result_verify(self):
        """Test HashResult.verify method."""
        result = hash_data("test data")
        self.assertTrue(result.verify("test data"))
        self.assertFalse(result.verify("different data"))
    
    def test_hash_result_to_dict(self):
        """Test HashResult.to_dict method."""
        result = hash_data("test")
        d = result.to_dict()
        
        self.assertIn('algorithm', d)
        self.assertIn('hex', d)
        self.assertIn('input_length', d)
        self.assertIn('timestamp', d)


class TestHMAC(unittest.TestCase):
    """Test HMAC functions."""
    
    def test_compute_hmac(self):
        """Test HMAC computation."""
        data = "message to sign"
        key = "secret_key"
        
        signature = compute_hmac(data, key)
        self.assertEqual(len(signature), 64)  # SHA256 HMAC
    
    def test_compute_hmac_different_algorithms(self):
        """Test HMAC with different algorithms."""
        data = "test"
        key = "key"
        
        for algo in ['sha256', 'sha512', 'sha1']:
            with self.subTest(algorithm=algo):
                sig = compute_hmac(data, key, algorithm=algo)
                self.assertTrue(len(sig) > 0)
    
    def test_verify_hmac_valid(self):
        """Test HMAC verification with valid signature."""
        data = "message"
        key = "secret"
        signature = compute_hmac(data, key)
        
        self.assertTrue(verify_hmac(data, signature, key))
    
    def test_verify_hmac_invalid(self):
        """Test HMAC verification with invalid signature."""
        data = "message"
        key = "secret"
        signature = compute_hmac(data, key)
        
        self.assertFalse(verify_hmac("tampered", signature, key))
        self.assertFalse(verify_hmac(data, signature, "wrong_key"))
    
    def test_hmac_timing_safe(self):
        """Test that HMAC verification is timing-safe."""
        data = "test"
        key = "key"
        signature = compute_hmac(data, key)
        
        # Should not raise, should return False for invalid
        result = verify_hmac(data, "invalid_signature", key)
        self.assertFalse(result)


class TestXOREncryption(unittest.TestCase):
    """Test XOR encryption."""
    
    def test_xor_encrypt_decrypt(self):
        """Test XOR encrypt/decrypt roundtrip."""
        data = "secret message"
        key = "mykey"
        
        encrypted = xor_encrypt(data, key)
        decrypted = xor_decrypt(encrypted, key)
        
        self.assertEqual(decrypted.decode('utf-8'), data)
    
    def test_xor_bytes(self):
        """Test XOR with bytes."""
        data = b"\x00\x01\x02\x03"
        key = b"\xff\xff\xff\xff"
        
        encrypted = xor_encrypt(data, key)
        decrypted = xor_decrypt(encrypted, key)
        
        self.assertEqual(decrypted, data)
    
    def test_xor_different_keys(self):
        """Test that different keys produce different output."""
        data = "test"
        
        enc1 = xor_encrypt(data, "key1")
        enc2 = xor_encrypt(data, "key2")
        
        self.assertNotEqual(enc1, enc2)


class TestSubstitutionCipher(unittest.TestCase):
    """Test substitution cipher."""
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test encrypt/decrypt roundtrip."""
        cipher = SubstitutionCipher(key="test_key")
        plaintext = "hello world"
        
        ciphertext = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(ciphertext)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_deterministic_with_key(self):
        """Test that same key produces same cipher."""
        cipher1 = SubstitutionCipher(key="same_key")
        cipher2 = SubstitutionCipher(key="same_key")
        
        text = "test message"
        self.assertEqual(cipher1.encrypt(text), cipher2.encrypt(text))
    
    def test_preserves_non_alpha(self):
        """Test that non-alphabetic chars are preserved."""
        cipher = SubstitutionCipher()
        text = "hello, world! 123"
        
        encrypted = cipher.encrypt(text)
        decrypted = cipher.decrypt(encrypted)
        
        self.assertEqual(decrypted, text)


class TestBase64(unittest.TestCase):
    """Test Base64 encoding."""
    
    def test_base64_encode_decode(self):
        """Test base64 encode/decode roundtrip."""
        data = "Hello, World!"
        encoded = base64_encode(data)
        decoded = base64_decode(encoded)
        
        self.assertEqual(decoded.decode('utf-8'), data)
    
    def test_url_safe_encode_decode(self):
        """Test URL-safe encode/decode roundtrip."""
        data = "test data with special chars: +/="
        encoded = url_safe_encode(data)
        
        # Should not contain + or /
        self.assertNotIn('+', encoded)
        self.assertNotIn('/', encoded)
        
        decoded = url_safe_decode(encoded)
        self.assertEqual(decoded.decode('utf-8'), data)
    
    def test_base64_bytes(self):
        """Test base64 with bytes."""
        data = b"\x00\x01\x02\x03"
        encoded = base64_encode(data)
        decoded = base64_decode(encoded)
        
        self.assertEqual(decoded, data)


class TestTokenGeneration(unittest.TestCase):
    """Test token generation."""
    
    def test_generate_token(self):
        """Test token generation."""
        token1 = generate_token()
        token2 = generate_token()
        
        self.assertEqual(len(token1), 44)  # 32 bytes base64
        self.assertNotEqual(token1, token2)
    
    def test_generate_token_url_safe(self):
        """Test URL-safe token generation."""
        token = generate_token(url_safe=True)
        
        self.assertNotIn('+', token)
        self.assertNotIn('/', token)
    
    def test_generate_token_with_timestamp(self):
        """Test token with timestamp."""
        token1 = generate_token(include_timestamp=True)
        time.sleep(0.01)
        token2 = generate_token(include_timestamp=True)
        
        self.assertNotEqual(token1, token2)
    
    def test_generate_api_key(self):
        """Test API key generation."""
        key1 = generate_api_key()
        key2 = generate_api_key(prefix="sk")
        
        self.assertTrue(key1.startswith("ak_"))
        self.assertTrue(key2.startswith("sk_"))
        self.assertNotEqual(key1, key2)
    
    def test_generate_session_id(self):
        """Test session ID generation."""
        session1 = generate_session_id()
        session2 = generate_session_id()
        
        self.assertEqual(len(session1), 64)  # 32 bytes hex
        self.assertNotEqual(session1, session2)


class TestChecksum(unittest.TestCase):
    """Test checksum functions."""
    
    def test_crc32_checksum(self):
        """Test CRC32 checksum."""
        data = "test data"
        checksum = compute_checksum(data, "crc32")
        
        self.assertIsInstance(checksum, int)
        self.assertTrue(verify_checksum(data, checksum, "crc32"))
        self.assertFalse(verify_checksum("different", checksum, "crc32"))
    
    def test_adler32_checksum(self):
        """Test Adler32 checksum."""
        data = "test data"
        checksum = compute_checksum(data, "adler32")
        
        self.assertIsInstance(checksum, int)
        self.assertTrue(verify_checksum(data, checksum, "adler32"))
    
    def test_checksum_consistency(self):
        """Test checksum consistency."""
        data = "consistent"
        cs1 = compute_checksum(data)
        cs2 = compute_checksum(data)
        
        self.assertEqual(cs1, cs2)


class TestOTP(unittest.TestCase):
    """Test One-Time Pad encryption."""
    
    def test_otp_encrypt_decrypt(self):
        """Test OTP encrypt/decrypt roundtrip."""
        data = "secret message"
        otp = generate_otp(len(data))
        
        encrypted = otp_encrypt(data, otp)
        decrypted = otp_decrypt(encrypted, otp)
        
        self.assertEqual(decrypted.decode('utf-8'), data)
    
    def test_otp_insufficient_length(self):
        """Test OTP with insufficient length raises error."""
        data = "long message"
        otp = generate_otp(5)  # Too short
        
        with self.assertRaises(EncryptionError):
            otp_encrypt(data, otp)
    
    def test_otp_different_pads(self):
        """Test that different OTPs produce different output."""
        data = "test"
        otp1 = generate_otp(4)
        otp2 = generate_otp(4)
        
        enc1 = otp_encrypt(data, otp1)
        enc2 = otp_encrypt(data, otp2)
        
        self.assertNotEqual(enc1, enc2)


class TestSecureCompare(unittest.TestCase):
    """Test secure comparison."""
    
    def test_secure_compare_equal(self):
        """Test secure compare with equal values."""
        self.assertTrue(secure_compare("test", "test"))
        self.assertTrue(secure_compare(b"bytes", b"bytes"))
    
    def test_secure_compare_not_equal(self):
        """Test secure compare with different values."""
        self.assertFalse(secure_compare("test", "different"))
        self.assertFalse(secure_compare("abc", "abd"))
    
    def test_secure_compare_different_length(self):
        """Test secure compare with different lengths."""
        self.assertFalse(secure_compare("short", "much longer string"))


class TestKeyDerivation(unittest.TestCase):
    """Test key derivation."""
    
    def test_derive_key_pbkdf2(self):
        """Test PBKDF2 key derivation."""
        password = "my_password"
        key, salt = derive_key(password)
        
        self.assertEqual(len(key), 32)
        self.assertEqual(len(salt), 32)
    
    def test_derive_key_custom_length(self):
        """Test key derivation with custom length."""
        password = "password"
        key, salt = derive_key(password, length=64)
        
        self.assertEqual(len(key), 64)
    
    def test_derive_key_deterministic(self):
        """Test that same password+salt produces same key."""
        password = "test"
        salt = b"fixed_salt_12345678901234567890"
        
        key1, _ = derive_key(password, salt=salt)
        key2, _ = derive_key(password, salt=salt)
        
        self.assertEqual(key1, key2)


class TestSecureString(unittest.TestCase):
    """Test SecureString class."""
    
    def test_secure_string_get(self):
        """Test SecureString get."""
        ss = SecureString("secret")
        self.assertEqual(ss.get(), "secret")
    
    def test_secure_string_consume(self):
        """Test SecureString consume."""
        ss = SecureString("secret")
        value = ss.consume()
        
        self.assertEqual(value, "secret")
        with self.assertRaises(EncryptionError):
            ss.get()
    
    def test_secure_string_clear(self):
        """Test SecureString clear."""
        ss = SecureString("secret")
        ss.clear()
        
        self.assertTrue(ss._consumed)
        self.assertIsNone(ss._value)
    
    def test_secure_string_context_manager(self):
        """Test SecureString as context manager."""
        with SecureString("secret") as ss:
            self.assertEqual(ss.get(), "secret")
        
        self.assertTrue(ss._consumed)
    
    def test_secure_string_repr(self):
        """Test SecureString repr."""
        ss = SecureString("test")
        repr_str = repr(ss)
        
        self.assertIn("SecureString", repr_str)
        self.assertIn("consumed", repr_str)


class TestHashChain(unittest.TestCase):
    """Test HashChain class."""
    
    def test_hash_chain_single(self):
        """Test hash chain with single entry."""
        chain = HashChain()
        chain.add("first")
        
        self.assertEqual(len(chain._chain), 1)
        self.assertTrue(len(chain.get_chain_hash()) > 0)
    
    def test_hash_chain_multiple(self):
        """Test hash chain with multiple entries."""
        chain = HashChain()
        chain.add("first").add("second").add("third")
        
        self.assertEqual(len(chain._chain), 3)
    
    def test_hash_chain_verify(self):
        """Test hash chain verification."""
        chain = HashChain()
        chain.add("a").add("b").add("c")
        expected = chain.get_chain_hash()
        
        self.assertTrue(chain.verify(["a", "b", "c"], expected))
        self.assertFalse(chain.verify(["a", "x", "c"], expected))
    
    def test_hash_chain_to_dict(self):
        """Test hash chain to_dict."""
        chain = HashChain()
        chain.add("test")
        
        d = chain.to_dict()
        
        self.assertIn('algorithm', d)
        self.assertIn('length', d)
        self.assertIn('chain_hash', d)
        self.assertIn('entries', d)
        self.assertEqual(d['length'], 1)


class TestConvenience(unittest.TestCase):
    """Test convenience functions."""
    
    def test_quick_hash(self):
        """Test quick_hash."""
        result = quick_hash("test")
        self.assertEqual(len(result), 64)
    
    def test_quick_encrypt_decrypt(self):
        """Test quick_encrypt/quick_decrypt."""
        data = "secret"
        key = "mykey"
        
        encrypted = quick_encrypt(data, key)
        decrypted = quick_decrypt(encrypted, key)
        
        self.assertEqual(decrypted.decode('utf-8'), data)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_data_hash(self):
        """Test hashing empty data."""
        result = hash_data("")
        self.assertTrue(len(result.hex_digest) > 0)
    
    def test_empty_data_checksum(self):
        """Test checksum of empty data."""
        cs = compute_checksum("")
        self.assertIsInstance(cs, int)
    
    def test_unicode_data(self):
        """Test with unicode data."""
        data = "你好世界 🌍"
        result = hash_data(data)
        self.assertTrue(len(result.hex_digest) > 0)
    
    def test_large_data(self):
        """Test with large data."""
        data = "x" * 1000000  # 1MB
        result = hash_data(data)
        self.assertTrue(len(result.hex_digest) > 0)
    
    def test_unsupported_checksum_algorithm(self):
        """Test unsupported checksum algorithm."""
        with self.assertRaises(EncryptionError):
            compute_checksum("test", "unsupported")
    
    def test_unsupported_kdf(self):
        """Test unsupported KDF."""
        with self.assertRaises(EncryptionError):
            derive_key("password", algorithm="unsupported")


class TestIntegration(unittest.TestCase):
    """Integration tests."""
    
    def test_password_workflow(self):
        """Test complete password workflow."""
        password = "MyS3cur3P@ssw0rd!"
        
        # Hash password
        hashed = hash_password(password)
        
        # Verify correct password
        self.assertTrue(verify_password(password, hashed))
        
        # Verify incorrect password
        self.assertFalse(verify_password("wrong", hashed))
    
    def test_hmac_message_authentication(self):
        """Test HMAC for message authentication."""
        message = "Important message"
        key = "secret_key"
        
        # Sign
        signature = compute_hmac(message, key)
        
        # Verify authentic
        self.assertTrue(verify_hmac(message, signature, key))
        
        # Verify tampered
        self.assertFalse(verify_hmac("Tampered message", signature, key))
    
    def test_token_session_workflow(self):
        """Test token-based session workflow."""
        # Generate session
        session_id = generate_session_id()
        self.assertEqual(len(session_id), 64)
        
        # Generate API key
        api_key = generate_api_key(prefix="test")
        self.assertTrue(api_key.startswith("test_"))
        
        # Generate token
        token = generate_token(url_safe=True)
        self.assertNotIn('+', token)
        self.assertNotIn('/', token)
    
    def test_hash_chain_integrity(self):
        """Test hash chain for data integrity."""
        documents = ["doc1", "doc2", "doc3", "doc4"]
        
        # Create chain
        chain = HashChain()
        for doc in documents:
            chain.add(doc)
        
        final_hash = chain.get_chain_hash()
        
        # Verify intact chain
        self.assertTrue(chain.verify(documents, final_hash))
        
        # Verify tampered chain fails
        tampered = ["doc1", "TAMPERED", "doc3", "doc4"]
        self.assertFalse(chain.verify(tampered, final_hash))


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestHashing,
        TestHMAC,
        TestXOREncryption,
        TestSubstitutionCipher,
        TestBase64,
        TestTokenGeneration,
        TestChecksum,
        TestOTP,
        TestSecureCompare,
        TestKeyDerivation,
        TestSecureString,
        TestHashChain,
        TestConvenience,
        TestEdgeCases,
        TestIntegration,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
