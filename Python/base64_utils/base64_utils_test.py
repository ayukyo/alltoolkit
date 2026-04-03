"""
AllToolkit - Python Base64 Utilities Test Suite

Comprehensive test suite for Base64 encoding/decoding utilities.
Run with: python -m pytest base64_utils_test.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import Base64Utils, encode, decode, encode_urlsafe, decode_urlsafe, is_valid


def test_encode_string():
    """Test encoding strings to Base64."""
    assert Base64Utils.encode("Hello, World!") == "SGVsbG8sIFdvcmxkIQ=="
    assert Base64Utils.encode("") == ""
    assert Base64Utils.encode("a") == "YQ=="
    assert Base64Utils.encode("ab") == "YWI="
    assert Base64Utils.encode("abc") == "YWJj"
    print("✓ test_encode_string passed")


def test_encode_bytes():
    """Test encoding bytes to Base64."""
    assert Base64Utils.encode(b"Hello, World!") == "SGVsbG8sIFdvcmxkIQ=="
    assert Base64Utils.encode(b"\x00\x01\x02\xff") == "AAEC/w=="
    print("✓ test_encode_bytes passed")


def test_decode_string():
    """Test decoding Base64 to strings."""
    assert Base64Utils.decode("SGVsbG8sIFdvcmxkIQ==") == "Hello, World!"
    assert Base64Utils.decode("") == ""
    assert Base64Utils.decode("YQ==") == "a"
    assert Base64Utils.decode("YWI=") == "ab"
    assert Base64Utils.decode("YWJj") == "abc"
    print("✓ test_decode_string passed")


def test_decode_to_bytes():
    """Test decoding Base64 to bytes."""
    assert Base64Utils.decode_to_bytes("AAEC/w==") == b"\x00\x01\x02\xff"
    assert Base64Utils.decode_to_bytes("SGVsbG8=") == b"Hello"
    print("✓ test_decode_to_bytes passed")


def test_encode_urlsafe():
    """Test URL-safe Base64 encoding."""
    # String with characters that differ between standard and URL-safe
    result = Base64Utils.encode_urlsafe("hello+world/test")
    assert "+" not in result
    assert "/" not in result
    assert "-" in result or "_" in result or result == "aGVsbG8rd29ybGQvdGVzdA=="
    print("✓ test_encode_urlsafe passed")


def test_encode_urlsafe_no_padding():
    """Test URL-safe Base64 encoding without padding."""
    result = Base64Utils.encode_urlsafe("hello", padding=False)
    assert "=" not in result
    assert result == "aGVsbG8"
    print("✓ test_encode_urlsafe_no_padding passed")


def test_decode_urlsafe():
    """Test URL-safe Base64 decoding."""
    # aGVsbG8- decodes to bytes: hello + 0xfb
    result1 = Base64Utils.decode_urlsafe("aGVsbG8-")
    assert result1.startswith("hello")
    result2 = Base64Utils.decode_urlsafe("aGVsbG8_")
    assert result2.startswith("hello")
    print("✓ test_decode_urlsafe passed")


def test_decode_urlsafe_no_padding():
    """Test decoding URL-safe Base64 without padding."""
    # "hello" encoded without padding
    assert Base64Utils.decode_urlsafe("aGVsbG8") == "hello"
    print("✓ test_decode_urlsafe_no_padding passed")


def test_to_urlsafe():
    """Test converting standard Base64 to URL-safe."""
    standard = "aGVsbG8+/test="
    urlsafe = Base64Utils.to_urlsafe(standard)
    assert "+" not in urlsafe
    assert "/" not in urlsafe
    assert "-" in urlsafe
    assert "_" in urlsafe
    print("✓ test_to_urlsafe passed")


def test_to_urlsafe_no_padding():
    """Test converting to URL-safe without padding."""
    standard = "aGVsbG8+/test="
    urlsafe = Base64Utils.to_urlsafe(standard, padding=False)
    assert "=" not in urlsafe
    print("✓ test_to_urlsafe_no_padding passed")


def test_from_urlsafe():
    """Test converting URL-safe Base64 to standard."""
    urlsafe = "aGVsbG8-_test"
    standard = Base64Utils.from_urlsafe(urlsafe)
    assert "-" not in standard
    assert "_" not in standard
    assert "+" in standard
    assert "/" in standard
    print("✓ test_from_urlsafe passed")


def test_is_valid_standard():
    """Test validating standard Base64."""
    assert Base64Utils.is_valid("SGVsbG8=") == True
    assert Base64Utils.is_valid("YWJj") == True
    assert Base64Utils.is_valid("") == True
    assert Base64Utils.is_valid("Invalid!") == False
    assert Base64Utils.is_valid("aGVsbG8-") == False  # URL-safe in standard mode
    print("✓ test_is_valid_standard passed")


def test_is_valid_urlsafe():
    """Test validating URL-safe Base64."""
    assert Base64Utils.is_valid("aGVsbG8-", urlsafe=True) == True
    assert Base64Utils.is_valid("aGVsbG8_", urlsafe=True) == True
    assert Base64Utils.is_valid("SGVsbG8=", urlsafe=True) == True  # Standard is also valid URL-safe
    assert Base64Utils.is_valid("Invalid!", urlsafe=True) == False
    print("✓ test_is_valid_urlsafe passed")


def test_is_valid_non_string():
    """Test validation with non-string input."""
    assert Base64Utils.is_valid(123) == False
    assert Base64Utils.is_valid(None) == False
    print("✓ test_is_valid_non_string passed")


def test_encoded_length():
    """Test calculating encoded length."""
    assert Base64Utils.encoded_length(0) == 0
    assert Base64Utils.encoded_length(1) == 4  # 1 byte -> 2 chars + 2 padding
    assert Base64Utils.encoded_length(2) == 4  # 2 bytes -> 3 chars + 1 padding
    assert Base64Utils.encoded_length(3) == 4  # 3 bytes -> 4 chars
    assert Base64Utils.encoded_length(100) == 136
    print("✓ test_encoded_length passed")


def test_encoded_length_no_padding():
    """Test calculating encoded length without padding."""
    assert Base64Utils.encoded_length(1, padding=False) == 2
    assert Base64Utils.encoded_length(2, padding=False) == 3
    assert Base64Utils.encoded_length(3, padding=False) == 4
    print("✓ test_encoded_length_no_padding passed")


def test_decoded_max_length():
    """Test calculating max decoded length."""
    assert Base64Utils.decoded_max_length(0) == 0
    assert Base64Utils.decoded_max_length(4) == 3
    assert Base64Utils.decoded_max_length(8) == 6
    assert Base64Utils.decoded_max_length(136) == 102
    print("✓ test_decoded_max_length passed")


def test_roundtrip():
    """Test encode/decode roundtrip."""
    test_cases = [
        "Hello, World!",
        "The quick brown fox jumps over the lazy dog",
        "1234567890",
        "!@#$%^&*()",
        "Unicode: 你好世界 🌍",
        "",
        "a",
        "ab",
        "abc",
    ]
    
    for original in test_cases:
        encoded = Base64Utils.encode(original)
        decoded = Base64Utils.decode(encoded)
        assert decoded == original, f"Failed for: {original}"
    
    print("✓ test_roundtrip passed")


def test_roundtrip_urlsafe():
    """Test URL-safe encode/decode roundtrip."""
    test_cases = [
        "hello+world/test",
        "user+name@example.com",
        "path/to/file",
        "a+b/c=d",
    ]
    
    for original in test_cases:
        encoded = Base64Utils.encode_urlsafe(original)
        decoded = Base64Utils.decode_urlsafe(encoded)
        assert decoded == original, f"Failed for: {original}"
    
    print("✓ test_roundtrip_urlsafe passed")


def test_roundtrip_bytes():
    """Test bytes encode/decode roundtrip."""
    test_cases = [
        b"\x00\x01\x02\x03",
        b"\xff\xfe\xfd\xfc",
        b"\x00\x00\x00\x00",
        b"\xff\xff\xff\xff",
        bytes(range(256)),
    ]
    
    for original in test_cases:
        encoded = Base64Utils.encode(original)
        decoded = Base64Utils.decode_to_bytes(encoded)
        assert decoded == original, f"Failed for: {original}"
    
    print("✓ test_roundtrip_bytes passed")


def test_convenience_functions():
    """Test convenience module-level functions."""
    assert encode("test") == Base64Utils.encode("test")
    assert decode("dGVzdA==") == Base64Utils.decode("dGVzdA==")
    assert encode_urlsafe("test") == Base64Utils.encode_urlsafe("test")
    assert decode_urlsafe("dGVzdA==") == Base64Utils.decode_urlsafe("dGVzdA==")
    assert is_valid("dGVzdA==") == Base64Utils.is_valid("dGVzdA==")
    print("✓ test_convenience_functions passed")


def test_error_handling():
    """Test error handling for invalid input."""
    try:
        Base64Utils.encode(123)
        assert False, "Should have raised TypeError"
    except TypeError:
        pass
    
    try:
        Base64Utils.decode("Invalid!!!")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("✓ test_error_handling passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("AllToolkit - Python Base64 Utilities Test Suite")
    print("=" * 60)
    
    tests = [
        test_encode_string,
        test_encode_bytes,
        test_decode_string,
        test_decode_to_bytes,
        test_encode_urlsafe,
        test_encode_urlsafe_no_padding,
        test_decode_urlsafe,
        test_decode_urlsafe_no_padding,
        test_to_urlsafe,
        test_to_urlsafe_no_padding,
        test_from_urlsafe,
        test_is_valid_standard,
        test_is_valid_urlsafe,
        test_is_valid_non_string,
        test_encoded_length,
        test_encoded_length_no_padding,
        test_decoded_max_length,
        test_roundtrip,
        test_roundtrip_urlsafe,
        test_roundtrip_bytes,
        test_convenience_functions,
        test_error_handling,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)