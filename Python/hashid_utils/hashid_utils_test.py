#!/usr/bin/env python3
"""
Comprehensive tests for hashid_utils module.

Tests cover:
- Basic encode/decode operations
- Multiple numbers encoding/decoding
- Custom salt and alphabet
- Minimum length padding
- Edge cases (zero, large numbers)
- Error handling
- Convenience functions
- Pre-configured classes
"""

import sys
import os
import time
from typing import List

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hashid_utils.mod import (
    HashID,
    encode_id,
    decode_id,
    encode_ids,
    decode_ids,
    is_valid_hashid,
    estimate_length,
    YouTubeHashID,
    ShortHashID,
)


class OutcomeCollector:
    """Test result collector."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors: List[str] = []
    
    def test(self, name: str, condition: bool, message: str = ""):
        """Run a single test."""
        if condition:
            self.passed += 1
            print(f"  ✅ {name}")
        else:
            self.failed += 1
            error_msg = f"  ❌ {name}"
            if message:
                error_msg += f" - {message}"
            print(error_msg)
            self.errors.append(f"{name}: {message}")
    
    def summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}")
        if self.errors:
            print("\nFailed tests:")
            for error in self.errors:
                print(f"  - {error}")
        print('='*60)
        return self.failed == 0


def test_basic_encode_decode(result: OutcomeCollector):
    """Test basic encode and decode operations."""
    print("\n[test_basic_encode_decode]")
    
    h = HashID()
    
    # Basic encoding/decoding
    for num in [0, 1, 10, 100, 1000, 10000, 100000, 1000000]:
        encoded = h.encode(num)
        decoded = h.decode(encoded)
        result.test(
            f"encode/decode {num}",
            decoded == [num],
            f"got {decoded}"
        )
    
    # Verify encoded strings are non-empty
    encoded = h.encode(123)
    result.test("encoded string is non-empty", len(encoded) > 0)
    
    # Verify encoded strings contain only alphanumeric chars
    encoded = h.encode(456)
    is_alnum = all(c.isalnum() for c in encoded)
    result.test("encoded string is alphanumeric", is_alnum, f"got: {encoded}")


def test_multiple_numbers(result: OutcomeCollector):
    """Test encoding/decoding multiple numbers."""
    print("\n[test_multiple_numbers]")
    
    h = HashID(salt="test salt")
    
    # Two numbers
    encoded = h.encode(1, 2)
    decoded = h.decode(encoded)
    result.test("encode/decode two numbers", decoded == [1, 2], f"got {decoded}")
    
    # Three numbers
    encoded = h.encode(100, 200, 300)
    decoded = h.decode(encoded)
    result.test("encode/decode three numbers", decoded == [100, 200, 300], f"got {decoded}")
    
    # Many numbers
    numbers = list(range(10))
    encoded = h.encode(*numbers)
    decoded = h.decode(encoded)
    result.test("encode/decode 10 numbers", decoded == numbers, f"got {decoded}")
    
    # Mixed size numbers
    encoded = h.encode(1, 999999, 5, 12345)
    decoded = h.decode(encoded)
    result.test("encode/decode mixed sizes", decoded == [1, 999999, 5, 12345], f"got {decoded}")


def test_custom_salt(result: OutcomeCollector):
    """Test encoding with custom salt."""
    print("\n[test_custom_salt]")
    
    h1 = HashID(salt="app secret 1")
    h2 = HashID(salt="app secret 2")
    
    # Same number with different salts produces different hashes
    encoded1 = h1.encode(12345)
    encoded2 = h2.encode(12345)
    
    result.test("different salts produce different hashes", encoded1 != encoded2, 
                f"{encoded1} == {encoded2}")
    
    # Verify each can decode its own hash
    decoded1 = h1.decode(encoded1)
    decoded2 = h2.decode(encoded2)
    
    result.test("decode with correct salt 1", decoded1 == [12345])
    result.test("decode with correct salt 2", decoded2 == [12345])
    
    # Verify wrong salt produces different numbers
    wrong_decode = h2.decode(encoded1)
    result.test("decode with wrong salt produces different result", 
                wrong_decode != [12345])


def test_min_length(result: OutcomeCollector):
    """Test minimum length padding."""
    print("\n[test_min_length]")
    
    # Without min_length
    h1 = HashID()
    encoded1 = h1.encode(1)
    
    # With min_length
    h2 = HashID(min_length=10)
    encoded2 = h2.encode(1)
    
    result.test("min_length increases encoded length", len(encoded2) >= 10,
                f"length: {len(encoded2)}")
    
    result.test("encoded with min_length is longer", len(encoded2) > len(encoded1),
                f"{len(encoded2)} vs {len(encoded1)}")
    
    # Verify decoding works with padded hash
    decoded = h2.decode(encoded2)
    result.test("decode padded hash", decoded == [1], f"got {decoded}")
    
    # Test various min_lengths
    for min_len in [5, 8, 12, 20]:
        h = HashID(min_length=min_len)
        encoded = h.encode(42)
        result.test(f"min_length {min_len}", len(encoded) >= min_len,
                    f"got length {len(encoded)}")


def test_custom_alphabet(result: OutcomeCollector):
    """Test encoding with custom alphabet."""
    print("\n[test_custom_alphabet]")
    
    # Hex alphabet
    h_hex = HashID(alphabet="0123456789abcdef")
    encoded = h_hex.encode(255)
    decoded = h_hex.decode(encoded)
    result.test("hex alphabet encode/decode", decoded == [255], f"got {decoded}")
    result.test("hex alphabet only hex chars", all(c in "0123456789abcdef" for c in encoded),
                f"got: {encoded}")
    
    # Lowercase only alphabet
    h_lower = HashID(alphabet="abcdefghijklmnopqrstuvwxyz")
    encoded = h_lower.encode(1000)
    decoded = h_lower.decode(encoded)
    result.test("lowercase alphabet encode/decode", decoded == [1000], f"got {decoded}")
    result.test("lowercase alphabet only lowercase", encoded.islower() and encoded.isalpha(),
                f"got: {encoded}")
    
    # Numbers only alphabet - needs at least 16 chars, so use hex
    h_nums = HashID(alphabet="0123456789ABCDEF")  # Hex-style with uppercase
    encoded = h_nums.encode(12345)
    decoded = h_nums.decode(encoded)
    result.test("numbers+letters alphabet encode/decode", decoded == [12345], f"got {decoded}")
    result.test("numbers+letters only hex chars", all(c in "0123456789ABCDEF" for c in encoded), f"got: {encoded}")


def test_encode_single_decode_single(result: OutcomeCollector):
    """Test single number encode/decode methods."""
    print("\n[test_encode_single_decode_single]")
    
    h = HashID(salt="test")
    
    # Basic usage
    encoded = h.encode_single(12345)
    decoded = h.decode_single(encoded)
    result.test("encode_single/decode_single", decoded == 12345, f"got {decoded}")
    
    # Verify it's the same as encode(number)
    encoded_multi = h.encode(12345)
    decoded_multi = h.decode(encoded_multi)
    result.test("single methods match multi methods", 
                decoded == decoded_multi[0] and encoded == encoded_multi)


def test_convenience_functions(result: OutcomeCollector):
    """Test module-level convenience functions."""
    print("\n[test_convenience_functions]")
    
    # encode_id / decode_id
    encoded = encode_id(999, salt="my app")
    decoded = decode_id(encoded, salt="my app")
    result.test("encode_id/decode_id", decoded == 999, f"got {decoded}")
    
    # encode_ids / decode_ids
    encoded = encode_ids(1, 2, 3, salt="my app")
    decoded = decode_ids(encoded, salt="my app")
    result.test("encode_ids/decode_ids", decoded == [1, 2, 3], f"got {decoded}")
    
    # Verify salt matters
    encoded1 = encode_id(123, salt="salt1")
    encoded2 = encode_id(123, salt="salt2")
    result.test("convenience functions respect salt", encoded1 != encoded2)
    
    # Verify min_length works
    encoded = encode_id(1, min_length=8)
    result.test("convenience functions respect min_length", len(encoded) >= 8,
                f"length: {len(encoded)}")


def test_preconfigured_classes(result: OutcomeCollector):
    """Test pre-configured HashID classes."""
    print("\n[test_preconfigured_classes]")
    
    # YouTubeHashID
    yt = YouTubeHashID(salt="youtube clone")
    encoded = yt.encode(123456789)
    decoded = yt.decode(encoded)
    result.test("YouTubeHashID encode/decode", decoded == [123456789], f"got {decoded}")
    result.test("YouTubeHashID min length", len(encoded) >= 11, f"length: {len(encoded)}")
    
    # ShortHashID
    short = ShortHashID(salt="short app")
    encoded = short.encode(12345)
    decoded = short.decode(encoded)
    result.test("ShortHashID encode/decode", decoded == [12345], f"got {decoded}")
    result.test("ShortHashID min length", len(encoded) >= 4, f"length: {len(encoded)}")


def test_is_valid_hashid(result: OutcomeCollector):
    """Test hashid validation function."""
    print("\n[test_is_valid_hashid]")
    
    # Valid hashids
    result.test("valid alphanumeric", is_valid_hashid("abc123"))
    result.test("valid mixed case", is_valid_hashid("AbCdEfG"))
    result.test("valid numbers", is_valid_hashid("123456789"))
    
    # Invalid hashids
    result.test("empty string invalid", not is_valid_hashid(""))
    result.test("spaces invalid", not is_valid_hashid("abc 123"))
    result.test("special chars invalid", not is_valid_hashid("abc@123"))
    result.test("unicode invalid", not is_valid_hashid("abc中文"))
    
    # Generated hashids are valid
    h = HashID()
    encoded = h.encode(12345)
    result.test("generated hashid is valid", is_valid_hashid(encoded))


def test_estimate_length(result: OutcomeCollector):
    """Test length estimation function."""
    print("\n[test_estimate_length]")
    
    # Basic estimations
    result.test("estimate 0", estimate_length(0) == 1)
    result.test("estimate 1", estimate_length(1) == 1)
    result.test("estimate 10", estimate_length(10) == 1)
    result.test("estimate 100", estimate_length(100) == 2)
    result.test("estimate 1000", estimate_length(1000) == 2)
    result.test("estimate 10000", estimate_length(10000) == 3)
    
    # Larger numbers
    result.test("estimate million", estimate_length(1000000) == 4)
    result.test("estimate billion", estimate_length(1000000000) == 6)
    
    # Custom alphabet length
    result.test("estimate with hex alphabet", estimate_length(1000000, 16) == 5)
    result.test("estimate with large alphabet", estimate_length(1000000, 128) == 3,
                f"got {estimate_length(1000000, 128)}")
    
    # Verify estimation is reasonable
    h = HashID()
    for num in [1, 100, 10000, 1000000]:
        encoded = h.encode(num)
        estimated = estimate_length(num)
        result.test(f"estimate for {num} is reasonable", 
                    len(encoded) <= estimated + 2,  # Allow some margin
                    f"actual: {len(encoded)}, estimated: {estimated}")


def test_edge_cases(result: OutcomeCollector):
    """Test edge cases and boundary conditions."""
    print("\n[test_edge_cases]")
    
    h = HashID()
    
    # Zero
    encoded = h.encode(0)
    decoded = h.decode(encoded)
    result.test("encode/decode zero", decoded == [0], f"got {decoded}")
    
    # Very large number
    large_num = 10**18
    encoded = h.encode(large_num)
    decoded = h.decode(encoded)
    result.test("encode/decode very large number", decoded == [large_num], f"got {decoded}")
    
    # Multiple zeros
    encoded = h.encode(0, 0, 0)
    decoded = h.decode(encoded)
    result.test("encode/decode multiple zeros", decoded == [0, 0, 0], f"got {decoded}")
    
    # Sequential numbers should produce different hashes
    hash1 = h.encode(1)
    hash2 = h.encode(2)
    hash3 = h.encode(3)
    result.test("sequential numbers produce different hashes", 
                hash1 != hash2 and hash2 != hash3 and hash1 != hash3)
    
    # Empty decode
    decoded = h.decode("")
    result.test("decode empty string returns empty list", decoded == [])


def test_error_handling(result: OutcomeCollector):
    """Test error handling and invalid inputs."""
    print("\n[test_error_handling]")
    
    h = HashID()
    
    # Negative numbers
    try:
        h.encode(-1)
        result.test("negative number raises error", False, "no error raised")
    except ValueError as e:
        result.test("negative number raises ValueError", True)
    
    # Invalid alphabet (too short)
    try:
        HashID(alphabet="abc")
        result.test("short alphabet raises error", False, "no error raised")
    except ValueError as e:
        result.test("short alphabet raises ValueError", True)
    
    # Decode single on multi-number hash
    encoded = h.encode(1, 2, 3)
    try:
        h.decode_single(encoded)
        result.test("decode_single on multi-number raises error", False, "no error raised")
    except ValueError as e:
        result.test("decode_single on multi-number raises ValueError", True)
    
    # Duplicate chars in alphabet are removed (use valid alphabet)
    h2 = HashID(alphabet="aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz")
    encoded = h2.encode(100)
    decoded = h2.decode(encoded)
    result.test("duplicate chars in alphabet are handled", decoded == [100], f"got {decoded}")


def test_deterministic(result: OutcomeCollector):
    """Test that encoding is deterministic."""
    print("\n[test_deterministic]")
    
    h = HashID(salt="deterministic test")
    
    # Same input should always produce same output
    encoded1 = h.encode(12345)
    encoded2 = h.encode(12345)
    encoded3 = h.encode(12345)
    
    result.test("encoding is deterministic", 
                encoded1 == encoded2 == encoded3)
    
    # Multiple numbers
    encoded1 = h.encode(1, 2, 3, 4, 5)
    encoded2 = h.encode(1, 2, 3, 4, 5)
    
    result.test("multi-number encoding is deterministic", encoded1 == encoded2)


def test_url_safety(result: OutcomeCollector):
    """Test that encoded strings are URL-safe."""
    print("\n[test_url_safety]")
    
    h = HashID()
    
    # Test various numbers
    for num in [0, 1, 10, 100, 1000, 10000, 100000, 1000000]:
        encoded = h.encode(num)
        
        # Check for URL-safe characters
        is_url_safe = all(c.isalnum() or c in "-_" for c in encoded)
        result.test(f"URL-safe encoding for {num}", is_url_safe, f"got: {encoded}")
        
        # Check no special URL-breaking chars
        has_bad_chars = any(c in " /?#[]@!$&'()*+,;=" for c in encoded)
        result.test(f"No URL-breaking chars for {num}", not has_bad_chars)


def test_collisions(result: OutcomeCollector):
    """Test that there are no collisions in a large set."""
    print("\n[test_collisions]")
    
    h = HashID(salt="collision test")
    
    # Test 10000 sequential numbers
    seen = set()
    collisions = []
    
    for num in range(10000):
        encoded = h.encode(num)
        if encoded in seen:
            collisions.append((num, encoded))
        seen.add(encoded)
    
    result.test("no collisions in 10000 sequential numbers", len(collisions) == 0,
                f"collisions: {collisions[:5]}")
    
    # Test 10000 random-ish numbers
    seen = set()
    collisions = []
    
    for num in range(0, 1000000, 100):
        encoded = h.encode(num)
        if encoded in seen:
            collisions.append((num, encoded))
        seen.add(encoded)
    
    result.test("no collisions in sparse numbers", len(collisions) == 0,
                f"collisions: {collisions[:5]}")


def test_performance(result: OutcomeCollector):
    """Test encoding/decoding performance."""
    print("\n[test_performance]")
    
    h = HashID(salt="performance test")
    
    # Encode 10000 numbers
    start = time.time()
    for i in range(10000):
        h.encode(i)
    encode_time = time.time() - start
    
    result.test("encode 10000 numbers < 1 second", encode_time < 1.0,
                f"time: {encode_time:.3f}s")
    
    # Decode 10000 hashes
    hashes = [h.encode(i) for i in range(10000)]
    start = time.time()
    for hash_str in hashes:
        h.decode(hash_str)
    decode_time = time.time() - start
    
    result.test("decode 10000 hashes < 1 second", decode_time < 1.0,
                f"time: {decode_time:.3f}s")


def test_reversible(result: OutcomeCollector):
    """Test that all encodings are reversible."""
    print("\n[test_reversible]")
    
    h = HashID(salt="reversible test", min_length=8)
    
    # Test various numbers
    test_numbers = [
        0, 1, 2, 10, 100, 1000, 10000, 100000, 1000000,
        2**10, 2**20, 2**30, 2**40,
        1234567890, 9876543210,
    ]
    
    for num in test_numbers:
        encoded = h.encode(num)
        decoded = h.decode(encoded)
        result.test(f"reversible for {num}", decoded == [num],
                    f"encoded: {encoded}, decoded: {decoded}")
    
    # Test multi-number reversibility
    test_lists = [
        [1, 2],
        [1, 2, 3],
        [0, 100, 10000],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    ]
    
    for nums in test_lists:
        encoded = h.encode(*nums)
        decoded = h.decode(encoded)
        result.test(f"reversible for list {nums}", decoded == nums,
                    f"encoded: {encoded}, decoded: {decoded}")


def run_all_tests():
    """Run all test suites."""
    print("="*60)
    print("HashID Utils - Comprehensive Test Suite")
    print("="*60)
    
    result = OutcomeCollector()
    
    test_basic_encode_decode(result)
    test_multiple_numbers(result)
    test_custom_salt(result)
    test_min_length(result)
    test_custom_alphabet(result)
    test_encode_single_decode_single(result)
    test_convenience_functions(result)
    test_preconfigured_classes(result)
    test_is_valid_hashid(result)
    test_estimate_length(result)
    test_edge_cases(result)
    test_error_handling(result)
    test_deterministic(result)
    test_url_safety(result)
    test_collisions(result)
    test_performance(result)
    test_reversible(result)
    
    success = result.summary()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())