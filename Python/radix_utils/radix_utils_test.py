"""
AllToolkit - Python Radix Conversion Utilities Test Suite

Comprehensive test suite for radix conversion utilities.
Run with: python -m pytest radix_utils_test.py -v
Or run directly: python radix_utils_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    RadixUtils,
    to_decimal, from_decimal, convert,
    to_binary, from_binary,
    to_octal, from_octal,
    to_hex, from_hex,
    to_base36, from_base36,
    convert_all_bases, is_valid, detect_base
)


def test_to_decimal_binary():
    """Test converting binary to decimal."""
    assert RadixUtils.to_decimal("0", 2) == 0
    assert RadixUtils.to_decimal("1", 2) == 1
    assert RadixUtils.to_decimal("10", 2) == 2
    assert RadixUtils.to_decimal("1010", 2) == 10
    assert RadixUtils.to_decimal("11111111", 2) == 255
    assert RadixUtils.to_decimal("100000000", 2) == 256
    print("✓ test_to_decimal_binary passed")


def test_to_decimal_octal():
    """Test converting octal to decimal."""
    assert RadixUtils.to_decimal("0", 8) == 0
    assert RadixUtils.to_decimal("7", 8) == 7
    assert RadixUtils.to_decimal("10", 8) == 8
    assert RadixUtils.to_decimal("77", 8) == 63
    assert RadixUtils.to_decimal("377", 8) == 255
    assert RadixUtils.to_decimal("1000", 8) == 512
    print("✓ test_to_decimal_octal passed")


def test_to_decimal_hex():
    """Test converting hexadecimal to decimal."""
    assert RadixUtils.to_decimal("0", 16) == 0
    assert RadixUtils.to_decimal("a", 16) == 10
    assert RadixUtils.to_decimal("f", 16) == 15
    assert RadixUtils.to_decimal("10", 16) == 16
    assert RadixUtils.to_decimal("ff", 16) == 255
    assert RadixUtils.to_decimal("FF", 16) == 255  # Uppercase
    assert RadixUtils.to_decimal("100", 16) == 256
    print("✓ test_to_decimal_hex passed")


def test_to_decimal_base36():
    """Test converting base 36 to decimal."""
    assert RadixUtils.to_decimal("0", 36) == 0
    assert RadixUtils.to_decimal("a", 36) == 10
    assert RadixUtils.to_decimal("z", 36) == 35
    assert RadixUtils.to_decimal("10", 36) == 36
    assert RadixUtils.to_decimal("zz", 36) == 1295
    assert RadixUtils.to_decimal("1000", 36) == 46656
    print("✓ test_to_decimal_base36 passed")


def test_to_decimal_negative():
    """Test converting negative numbers to decimal."""
    assert RadixUtils.to_decimal("-1010", 2) == -10
    assert RadixUtils.to_decimal("-ff", 16) == -255
    assert RadixUtils.to_decimal("-377", 8) == -255
    print("✓ test_to_decimal_negative passed")


def test_to_decimal_fractional():
    """Test converting fractional numbers to decimal."""
    assert RadixUtils.to_decimal("1.1", 2) == 1.5
    assert RadixUtils.to_decimal("0.1", 2) == 0.5
    assert RadixUtils.to_decimal("1.5", 8) == 1.625
    assert RadixUtils.to_decimal("0.a", 16) == 0.625
    print("✓ test_to_decimal_fractional passed")


def test_from_decimal():
    """Test converting decimal to other bases."""
    assert RadixUtils.from_decimal(0, 2) == "0"
    assert RadixUtils.from_decimal(10, 2) == "1010"
    assert RadixUtils.from_decimal(255, 16) == "ff"
    assert RadixUtils.from_decimal(255, 8) == "377"
    assert RadixUtils.from_decimal(35, 36) == "z"
    assert RadixUtils.from_decimal(36, 36) == "10"
    print("✓ test_from_decimal passed")


def test_from_decimal_negative():
    """Test converting negative decimal to other bases."""
    assert RadixUtils.from_decimal(-10, 2) == "-1010"
    assert RadixUtils.from_decimal(-255, 16) == "-ff"
    assert RadixUtils.from_decimal(-1, 2) == "-1"
    print("✓ test_from_decimal_negative passed")


def test_from_decimal_fractional():
    """Test converting decimal fractions to other bases."""
    assert RadixUtils.from_decimal(0.5, 2) == "0.1"
    assert RadixUtils.from_decimal(1.5, 2) == "1.1"
    assert RadixUtils.from_decimal(0.625, 16) == "0.a"
    print("✓ test_from_decimal_fractional passed")


def test_convert():
    """Test converting between bases."""
    # Binary to hex
    assert RadixUtils.convert("11111111", 2, 16) == "ff"
    assert RadixUtils.convert("1010", 2, 10) == "10"
    
    # Hex to binary
    assert RadixUtils.convert("ff", 16, 2) == "11111111"
    assert RadixUtils.convert("a", 16, 2) == "1010"
    
    # Octal to hex
    assert RadixUtils.convert("377", 8, 16) == "ff"
    
    # Decimal to base 36
    assert RadixUtils.convert("12345", 10, 36) == "9ix"
    
    print("✓ test_convert passed")


def test_to_binary():
    """Test converting to binary."""
    assert RadixUtils.to_binary("255") == "11111111"
    assert RadixUtils.to_binary("10") == "1010"
    assert RadixUtils.to_binary("ff", 16) == "11111111"
    assert RadixUtils.to_binary("377", 8) == "11111111"
    print("✓ test_to_binary passed")


def test_from_binary():
    """Test converting from binary."""
    assert RadixUtils.from_binary("11111111") == "255"
    assert RadixUtils.from_binary("1010") == "10"
    assert RadixUtils.from_binary("11111111", 16) == "ff"
    print("✓ test_from_binary passed")


def test_to_octal():
    """Test converting to octal."""
    assert RadixUtils.to_octal("255") == "377"
    assert RadixUtils.to_octal("8") == "10"
    assert RadixUtils.to_octal("ff", 16) == "377"
    assert RadixUtils.to_octal("11111111", 2) == "377"
    print("✓ test_to_octal passed")


def test_from_octal():
    """Test converting from octal."""
    assert RadixUtils.from_octal("377") == "255"
    assert RadixUtils.from_octal("10") == "8"
    assert RadixUtils.from_octal("377", 16) == "ff"
    print("✓ test_from_octal passed")


def test_to_hex():
    """Test converting to hexadecimal."""
    assert RadixUtils.to_hex("255") == "ff"
    assert RadixUtils.to_hex("255", uppercase=True) == "FF"
    assert RadixUtils.to_hex("11111111", 2) == "ff"
    assert RadixUtils.to_hex("377", 8) == "ff"
    print("✓ test_to_hex passed")


def test_from_hex():
    """Test converting from hexadecimal."""
    assert RadixUtils.from_hex("ff") == "255"
    assert RadixUtils.from_hex("FF") == "255"  # Uppercase input
    assert RadixUtils.from_hex("ff", 2) == "11111111"
    assert RadixUtils.from_hex("ff", 8) == "377"
    print("✓ test_from_hex passed")


def test_base36():
    """Test base 36 conversions."""
    assert RadixUtils.to_base36("12345") == "9ix"
    assert RadixUtils.from_base36("9ix") == "12345"
    assert RadixUtils.to_base36("35") == "z"
    assert RadixUtils.from_base36("z") == "35"
    print("✓ test_base36 passed")


def test_convert_all_bases():
    """Test converting to all bases at once."""
    result = RadixUtils.convert_all_bases("255", 10)
    assert result['binary'] == "11111111"
    assert result['octal'] == "377"
    assert result['decimal'] == "255"
    assert result['hexadecimal'] == "ff"
    assert result['base36'] == "73"
    print("✓ test_convert_all_bases passed")


def test_count_bits():
    """Test counting bits."""
    assert RadixUtils.count_bits("255") == 8
    assert RadixUtils.count_bits("256") == 9
    assert RadixUtils.count_bits("1") == 1
    assert RadixUtils.count_bits("0") == 1
    assert RadixUtils.count_bits("ff", 16) == 8
    print("✓ test_count_bits passed")


def test_get_bit():
    """Test getting a specific bit."""
    assert RadixUtils.get_bit("10", 10, 0) == 0
    assert RadixUtils.get_bit("10", 10, 1) == 1
    assert RadixUtils.get_bit("10", 10, 2) == 0
    assert RadixUtils.get_bit("255", 10, 0) == 1
    assert RadixUtils.get_bit("255", 10, 7) == 1
    print("✓ test_get_bit passed")


def test_set_bit():
    """Test setting a specific bit."""
    assert RadixUtils.set_bit("10", 10, 0) == "11"
    assert RadixUtils.set_bit("0", 10, 0) == "1"
    assert RadixUtils.set_bit("0", 10, 3) == "8"
    print("✓ test_set_bit passed")


def test_clear_bit():
    """Test clearing a specific bit."""
    assert RadixUtils.clear_bit("11", 10, 0) == "10"
    assert RadixUtils.clear_bit("255", 10, 0) == "254"
    assert RadixUtils.clear_bit("8", 10, 3) == "0"
    print("✓ test_clear_bit passed")


def test_is_valid():
    """Test validating numbers for a base."""
    assert RadixUtils.is_valid("1010", 2) == True
    assert RadixUtils.is_valid("1020", 2) == False
    assert RadixUtils.is_valid("1234567", 8) == True
    assert RadixUtils.is_valid("12345678", 8) == False
    assert RadixUtils.is_valid("abcdef", 16) == True
    assert RadixUtils.is_valid("ghij", 16) == False
    assert RadixUtils.is_valid("xyz", 36) == True
    print("✓ test_is_valid passed")


def test_detect_base():
    """Test detecting base from prefix."""
    assert RadixUtils.detect_base("0b1010") == 2
    assert RadixUtils.detect_base("0o755") == 8
    assert RadixUtils.detect_base("0xff") == 16
    assert RadixUtils.detect_base("0xFF") == 16
    # Numbers without prefix: algorithm tries to infer
    # "255" has only digits 0-7, so might be interpreted as octal
    # "abc" contains letters, so base is inferred from max letter
    assert RadixUtils.detect_base("abc") == 13  # 'c' -> base 13
    print("✓ test_detect_base passed")


def test_strip_prefix():
    """Test stripping base prefixes."""
    assert RadixUtils.strip_prefix("0xff") == ("ff", 16)
    assert RadixUtils.strip_prefix("0b1010") == ("1010", 2)
    assert RadixUtils.strip_prefix("0o755") == ("755", 8)
    assert RadixUtils.strip_prefix("255") == ("255", None)
    assert RadixUtils.strip_prefix("-0xff") == ("-ff", 16)
    print("✓ test_strip_prefix passed")


def test_edge_cases():
    """Test edge cases."""
    # Zero
    assert RadixUtils.to_decimal("0", 2) == 0
    assert RadixUtils.from_decimal(0, 16) == "0"
    
    # Single digit
    assert RadixUtils.to_decimal("f", 16) == 15
    assert RadixUtils.from_decimal(15, 16) == "f"
    
    # Large numbers
    large = RadixUtils.to_decimal("zzzz", 36)
    assert RadixUtils.from_decimal(large, 36) == "zzzz"
    
    print("✓ test_edge_cases passed")


def test_error_handling():
    """Test error handling for invalid input."""
    # Invalid base
    try:
        RadixUtils.to_decimal("10", 1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        RadixUtils.to_decimal("10", 37)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # Invalid digit for base
    try:
        RadixUtils.to_decimal("2", 2)  # '2' is not valid in binary
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        RadixUtils.to_decimal("g", 16)  # 'g' is not valid in hex
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # Non-string input
    try:
        RadixUtils.to_decimal(10, 10)
        assert False, "Should have raised TypeError"
    except TypeError:
        pass
    
    # Empty string
    try:
        RadixUtils.to_decimal("", 10)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("✓ test_error_handling passed")


def test_roundtrip():
    """Test roundtrip conversions."""
    for decimal in [0, 1, 10, 100, 255, 256, 1000, 12345, 65535]:
        # Decimal -> Base -> Decimal
        for base in [2, 8, 10, 16, 36]:
            converted = RadixUtils.from_decimal(decimal, base)
            back = RadixUtils.to_decimal(converted, base)
            assert back == decimal, f"Failed for {decimal} in base {base}: got {back}"
    
    print("✓ test_roundtrip passed")


def test_roundtrip_negative():
    """Test roundtrip conversions for negative numbers."""
    for decimal in [-1, -10, -100, -255, -1000]:
        for base in [2, 8, 10, 16, 36]:
            converted = RadixUtils.from_decimal(decimal, base)
            back = RadixUtils.to_decimal(converted, base)
            assert back == decimal, f"Failed for {decimal} in base {base}"
    
    print("✓ test_roundtrip_negative passed")


def test_convenience_functions():
    """Test convenience module-level functions."""
    assert to_decimal("ff", 16) == 255
    assert from_decimal(255, 16) == "ff"
    assert convert("11111111", 2, 16) == "ff"
    assert to_binary("255") == "11111111"
    assert from_binary("11111111") == "255"
    assert to_octal("255") == "377"
    assert from_octal("377") == "255"
    assert to_hex("255") == "ff"
    assert from_hex("ff") == "255"
    assert to_base36("12345") == "9ix"
    assert from_base36("9ix") == "12345"
    assert is_valid("1010", 2) == True
    assert detect_base("0xff") == 16
    print("✓ test_convenience_functions passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("AllToolkit - Python Radix Conversion Utilities Test Suite")
    print("=" * 60)
    
    tests = [
        test_to_decimal_binary,
        test_to_decimal_octal,
        test_to_decimal_hex,
        test_to_decimal_base36,
        test_to_decimal_negative,
        test_to_decimal_fractional,
        test_from_decimal,
        test_from_decimal_negative,
        test_from_decimal_fractional,
        test_convert,
        test_to_binary,
        test_from_binary,
        test_to_octal,
        test_from_octal,
        test_to_hex,
        test_from_hex,
        test_base36,
        test_convert_all_bases,
        test_count_bits,
        test_get_bit,
        test_set_bit,
        test_clear_bit,
        test_is_valid,
        test_detect_base,
        test_strip_prefix,
        test_edge_cases,
        test_error_handling,
        test_roundtrip,
        test_roundtrip_negative,
        test_convenience_functions,
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