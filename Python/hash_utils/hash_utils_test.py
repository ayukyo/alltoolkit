#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Hash Utilities Test Suite

Comprehensive tests for hash_utils module.
Run with: python hash_utils_test.py
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    md5, sha1, sha256, sha512, hash, hash_algorithms,
    hmac_hash, hmac_verify,
    hash_file, hash_directory, verify_file_hash,
    compare_hashes, hash_diff,
    hex_to_base64, base64_to_hex, bytes_to_hex, hex_to_bytes,
    IncrementalHasher,
    hash_key, consistent_hash,
    simple_hash_password, verify_password,
    crc32, crc32_hex,
    SUPPORTED_ALGORITHMS
)


class TestRunner:
    """Simple test runner with pass/fail tracking."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, name: str, condition: bool, error_msg: str = ""):
        """Run a single test."""
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            msg = f"  ✗ {name}"
            if error_msg:
                msg += f" - {error_msg}"
            print(msg)
            self.errors.append(name)
    
    def report(self) -> bool:
        """Print test report and return True if all tests passed."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}")
        
        if self.failed == 0:
            print("✓ All tests passed!")
        else:
            print(f"✗ {self.failed} test(s) failed:")
            for error in self.errors:
                print(f"    - {error}")
        
        print('='*60)
        return self.failed == 0


def run_basic_hash_tests(runner: TestRunner):
    """Test basic hash functions."""
    print("\nBasic Hash Function Tests")
    print("="*60)
    
    # MD5 tests
    runner.test("MD5: known value", 
                md5("hello") == "5d41402abc4b2a76b9719d911017c592")
    runner.test("MD5: bytes input", 
                md5(b"hello") == "5d41402abc4b2a76b9719d911017c592")
    runner.test("MD5: binary output", 
                len(md5("hello", hex_output=False)) == 16)
    runner.test("MD5: empty string", 
                md5("") == "d41d8cd98f00b204e9800998ecf8427e")
    
    # SHA1 tests
    runner.test("SHA1: known value", 
                sha1("hello") == "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d")
    runner.test("SHA1: binary output", 
                len(sha1("hello", hex_output=False)) == 20)
    
    # SHA256 tests
    runner.test("SHA256: known value", 
                sha256("hello") == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824")
    runner.test("SHA256: binary output", 
                len(sha256("hello", hex_output=False)) == 32)
    runner.test("SHA256: unicode support", 
                sha256("你好") == sha256("你好".encode('utf-8')))
    
    # SHA512 tests
    runner.test("SHA512: binary output", 
                len(sha512("hello", hex_output=False)) == 64)
    runner.test("SHA512: hex output length", 
                len(sha512("hello")) == 128)
    
    # Generic hash function
    runner.test("hash(): md5 algorithm", 
                hash("hello", "md5") == md5("hello"))
    runner.test("hash(): sha256 algorithm", 
                hash("hello", "sha256") == sha256("hello"))
    runner.test("hash(): sha512 algorithm", 
                hash("hello", "sha512") == sha512("hello"))
    
    # Unsupported algorithm
    try:
        hash("hello", "invalid_algo")
        runner.test("hash(): raises on invalid algorithm", False)
    except ValueError:
        runner.test("hash(): raises on invalid algorithm", True)
    
    # Hash algorithms list
    runner.test("hash_algorithms(): returns list", 
                isinstance(hash_algorithms(), list))
    runner.test("hash_algorithms(): contains sha256", 
                "sha256" in hash_algorithms())
    runner.test("hash_algorithms(): contains md5", 
                "md5" in hash_algorithms())


def run_hmac_tests(runner: TestRunner):
    """Test HMAC functions."""
    print("\nHMAC Tests")
    print("="*60)
    
    key = "secret-key"
    data = "test message"
    
    # HMAC generation
    mac = hmac_hash(data, key)
    runner.test("HMAC: generates hex string", 
                len(mac) == 64)  # SHA256 = 64 hex chars
    runner.test("HMAC: consistent output", 
                hmac_hash(data, key) == hmac_hash(data, key))
    runner.test("HMAC: different keys produce different results", 
                hmac_hash(data, key) != hmac_hash(data, "different-key"))
    runner.test("HMAC: different data produces different results", 
                hmac_hash(data, key) != hmac_hash("different", key))
    
    # HMAC verification
    runner.test("HMAC verify: valid signature", 
                hmac_verify(data, key, mac))
    runner.test("HMAC verify: tampered data", 
                not hmac_verify("tampered", key, mac))
    runner.test("HMAC verify: wrong key", 
                not hmac_verify(data, "wrong-key", mac))
    runner.test("HMAC verify: wrong signature", 
                not hmac_verify(data, key, "0" * 64))
    
    # HMAC with different algorithms
    mac_sha1 = hmac_hash(data, key, algorithm="sha1")
    runner.test("HMAC: sha1 algorithm", 
                len(mac_sha1) == 40)  # SHA1 = 40 hex chars
    
    mac_sha512 = hmac_hash(data, key, algorithm="sha512")
    runner.test("HMAC: sha512 algorithm", 
                len(mac_sha512) == 128)  # SHA512 = 128 hex chars


def run_file_hash_tests(runner: TestRunner):
    """Test file hashing functions."""
    print("\nFile Hash Tests")
    print("="*60)
    
    # Create temp directory for tests
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create test file
        test_file = Path(temp_dir) / "test.txt"
        test_file.write_text("hello world")
        
        # Hash file
        file_hash = hash_file(test_file)
        runner.test("hash_file(): generates hash", 
                    len(file_hash) == 64)
        
        # Verify known hash
        expected = sha256("hello world")
        runner.test("hash_file(): matches data hash", 
                    file_hash == expected)
        
        # Verify file hash
        runner.test("verify_file_hash(): valid hash", 
                    verify_file_hash(test_file, file_hash))
        runner.test("verify_file_hash(): invalid hash", 
                    not verify_file_hash(test_file, "wrong_hash"))
        runner.test("verify_file_hash(): missing file", 
                    not verify_file_hash("/nonexistent/file.txt", file_hash))
        
        # Hash non-existent file
        try:
            hash_file("/nonexistent/file.txt")
            runner.test("hash_file(): raises on missing file", False)
        except FileNotFoundError:
            runner.test("hash_file(): raises on missing file", True)
        
        # Test different algorithms
        md5_hash = hash_file(test_file, algorithm="md5")
        runner.test("hash_file(): md5 algorithm", 
                    len(md5_hash) == 32)
        
        # Create directory structure
        subdir = Path(temp_dir) / "subdir"
        subdir.mkdir()
        (subdir / "nested.txt").write_text("nested content")
        
        # Hash directory
        dir_hashes = hash_directory(temp_dir)
        runner.test("hash_directory(): returns dict", 
                    isinstance(dir_hashes, dict))
        runner.test("hash_directory(): contains files", 
                    len(dir_hashes) >= 2)
        runner.test("hash_directory(): relative paths", 
                    any("test.txt" in k for k in dir_hashes.keys()))
        
        # Test with ignore patterns
        (Path(temp_dir) / "ignore.pyc").write_text("should ignore")
        dir_hashes_filtered = hash_directory(temp_dir, ignore_patterns=["*.pyc"])
        runner.test("hash_directory(): ignores patterns", 
                    not any("pyc" in k for k in dir_hashes_filtered.keys()))
        
        # Non-recursive
        dir_hashes_flat = hash_directory(temp_dir, recursive=False)
        runner.test("hash_directory(): non-recursive", 
                    not any("subdir" in k for k in dir_hashes_flat.keys()))
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


def run_comparison_tests(runner: TestRunner):
    """Test hash comparison functions."""
    print("\nHash Comparison Tests")
    print("="*60)
    
    hash1 = "abc123def456"
    hash2 = "ABC123DEF456"
    hash3 = "abc123def789"
    
    runner.test("compare_hashes(): case insensitive match", 
                compare_hashes(hash1, hash2))
    runner.test("compare_hashes(): case sensitive mismatch", 
                not compare_hashes(hash1, hash2, case_sensitive=True))
    runner.test("compare_hashes(): different values", 
                not compare_hashes(hash1, hash3))
    runner.test("compare_hashes(): same values", 
                compare_hashes(hash1, hash1))
    
    # Hash diff
    diff = hash_diff(hash1, hash3)
    runner.test("hash_diff(): detects mismatch", 
                not diff['match'])
    runner.test("hash_diff(): detects length match", 
                diff['length_match'])
    runner.test("hash_diff(): shows differences", 
                len(diff['differ_at']) > 0)
    
    diff_same = hash_diff(hash1, hash2)
    runner.test("hash_diff(): case insensitive match", 
                diff_same['match'])


def run_encoding_tests(runner: TestRunner):
    """Test encoding conversion functions."""
    print("\nEncoding Tests")
    print("="*60)
    
    # Hex to Base64
    runner.test("hex_to_base64(): 'Hello'", 
                hex_to_base64("48656c6c6f") == "SGVsbG8=")
    runner.test("hex_to_base64(): empty", 
                hex_to_base64("") == "")
    
    # Base64 to Hex
    runner.test("base64_to_hex(): 'Hello'", 
                base64_to_hex("SGVsbG8=") == "48656c6c6f")
    runner.test("base64_to_hex(): round trip", 
                base64_to_hex(hex_to_base64("deadbeef")) == "deadbeef")
    
    # Invalid input
    try:
        hex_to_base64("invalid")
        runner.test("hex_to_base64(): raises on invalid", False)
    except ValueError:
        runner.test("hex_to_base64(): raises on invalid", True)
    
    # Bytes conversions
    runner.test("bytes_to_hex(): basic", 
                bytes_to_hex(b"Hi") == "4869")
    runner.test("hex_to_bytes(): basic", 
                hex_to_bytes("4869") == b"Hi")
    runner.test("hex_to_bytes(): round trip", 
                bytes_to_hex(hex_to_bytes("cafebabe")) == "cafebabe")


def run_incremental_hash_tests(runner: TestRunner):
    """Test incremental hashing."""
    print("\nIncremental Hash Tests")
    print("="*60)
    
    # Basic incremental hashing
    hasher = IncrementalHasher('sha256')
    hasher.update("Hello ")
    hasher.update("World")
    
    expected = sha256("Hello World")
    runner.test("IncrementalHasher: matches bulk hash", 
                hasher.hexdigest() == expected)
    
    # Reset
    hasher.reset()
    hasher.update("test")
    runner.test("IncrementalHasher: reset works", 
                hasher.hexdigest() == sha256("test"))
    
    # Copy
    hasher1 = IncrementalHasher('sha256')
    hasher1.update("data")
    hasher2 = hasher1.copy()
    hasher1.update("more")
    runner.test("IncrementalHasher: copy is independent", 
                hasher1.hexdigest() != hasher2.hexdigest())
    runner.test("IncrementalHasher: copy preserves state", 
                hasher2.hexdigest() == sha256("data"))
    
    # Chaining
    result = IncrementalHasher('md5').update("a").update("b").update("c").hexdigest()
    runner.test("IncrementalHasher: method chaining", 
                result == md5("abc"))
    
    # Binary digest
    hasher = IncrementalHasher('sha256')
    hasher.update("test")
    runner.test("IncrementalHasher: binary digest", 
                len(hasher.digest()) == 32)


def run_utility_tests(runner: TestRunner):
    """Test utility functions."""
    print("\nUtility Function Tests")
    print("="*60)
    
    # Consistent hash
    bucket = consistent_hash("user123", 10)
    runner.test("consistent_hash(): returns valid bucket", 
                0 <= bucket < 10)
    runner.test("consistent_hash(): deterministic", 
                consistent_hash("user123", 10) == consistent_hash("user123", 10))
    
    # CRC32
    runner.test("crc32(): returns int", 
                isinstance(crc32("hello"), int))
    runner.test("crc32_hex(): returns 8 char hex", 
                len(crc32_hex("hello")) == 8)
    runner.test("crc32(): deterministic", 
                crc32("test") == crc32("test"))


def run_password_tests(runner: TestRunner):
    """Test password hashing functions."""
    print("\nPassword Hash Tests")
    print("="*60)
    
    password = "my_secure_password"
    
    # Hash password
    result = simple_hash_password(password)
    runner.test("simple_hash_password(): returns dict", 
                isinstance(result, dict))
    runner.test("simple_hash_password(): has hash", 
                'hash' in result)
    runner.test("simple_hash_password(): has salt", 
                'salt' in result)
    runner.test("simple_hash_password(): has algorithm", 
                'algorithm' in result)
    runner.test("simple_hash_password(): salt is random", 
                simple_hash_password(password)['salt'] != simple_hash_password(password)['salt'])
    
    # Verify password
    runner.test("verify_password(): correct password", 
                verify_password(password, result['hash'], result['salt']))
    runner.test("verify_password(): wrong password", 
                not verify_password("wrong_password", result['hash'], result['salt']))
    
    # Custom salt
    custom_salt = "fixed_salt_12345"
    result2 = simple_hash_password(password, custom_salt)
    runner.test("simple_hash_password(): uses custom salt", 
                result2['salt'] == custom_salt)


def run_unicode_tests(runner: TestRunner):
    """Test unicode handling."""
    print("\nUnicode Tests")
    print("="*60)
    
    # Chinese characters
    chinese = "你好世界"
    runner.test("Unicode: SHA256 Chinese", 
                len(sha256(chinese)) == 64)
    
    # Emoji
    emoji = "Hello 🌍!"
    runner.test("Unicode: SHA256 emoji", 
                len(sha256(emoji)) == 64)
    
    # Mixed
    mixed = "Test 测试 тест 🎉"
    hash1 = sha256(mixed)
    hash2 = sha256(mixed)
    runner.test("Unicode: consistent hashing", 
                hash1 == hash2)
    
    # HMAC with unicode
    mac = hmac_hash(chinese, "key")
    runner.test("Unicode: HMAC Chinese", 
                len(mac) == 64)


def run_edge_case_tests(runner: TestRunner):
    """Test edge cases."""
    print("\nEdge Case Tests")
    print("="*60)
    
    # Empty strings
    runner.test("Empty: MD5", 
                md5("") == "d41d8cd98f00b204e9800998ecf8427e")
    runner.test("Empty: SHA256", 
                sha256("") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    
    # Very long string
    long_string = "a" * 1000000
    runner.test("Long string: SHA256", 
                len(sha256(long_string)) == 64)
    
    # Special characters
    special = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    runner.test("Special chars: hashes", 
                len(sha256(special)) == 64)
    
    # Null bytes
    null_data = b"hello\x00world"
    runner.test("Null bytes: hashes", 
                len(sha256(null_data)) == 64)


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Hash Utils Test Suite")
    print("="*60)
    
    runner = TestRunner()
    
    run_basic_hash_tests(runner)
    run_hmac_tests(runner)
    run_file_hash_tests(runner)
    run_comparison_tests(runner)
    run_encoding_tests(runner)
    run_incremental_hash_tests(runner)
    run_utility_tests(runner)
    run_password_tests(runner)
    run_unicode_tests(runner)
    run_edge_case_tests(runner)
    
    success = runner.report()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
