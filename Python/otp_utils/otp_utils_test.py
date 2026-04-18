#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - OTP Utilities Tests
================================
Comprehensive test suite for OTP utilities module.
"""

import sys
import time
import os
from urllib.parse import quote

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from otp_utils.mod import (
    # Constants
    DEFAULT_DIGITS, DEFAULT_PERIOD, DEFAULT_WINDOW,
    SUPPORTED_DIGITS, SUPPORTED_ALGORITHMS,
    # Base32 utilities
    encode_base32, decode_base32, generate_secret,
    # HOTP functions
    generate_hotp, validate_hotp,
    # TOTP functions
    generate_totp, validate_totp,
    # URI functions
    build_totp_uri, build_hotp_uri, parse_otp_uri,
    # Recovery codes
    generate_recovery_codes, validate_recovery_code,
    # Time utilities
    get_remaining_seconds, format_code,
    # Classes
    TOTP, HOTP
)


def test_base32():
    """Test Base32 encoding and decoding."""
    print("Testing Base32 utilities...")
    
    # Test encode/decode round trip
    test_cases = [
        b'Hello',
        b'World',
        b'1234567890',
        b'\x00\x01\x02\x03\x04\x05',
        b'A' * 20,  # Secret length
    ]
    
    for data in test_cases:
        encoded = encode_base32(data)
        decoded = decode_base32(encoded)
        assert decoded == data, f"Round trip failed for {data}"
    
    # Test with padding
    assert decode_base32('JBSWY3DP') == b'Hello'
    
    # Test a longer string that needs padding
    test_data = b'Hello World!'
    encoded = encode_base32(test_data)
    assert decode_base32(encoded) == test_data
    
    # Test generate_secret
    secret = generate_secret(20)
    assert len(decode_base32(secret)) == 20
    assert len(secret) > 0
    
    print("  ✓ Base32 utilities passed")


def test_hotp():
    """Test HOTP generation and validation."""
    print("Testing HOTP functions...")
    
    # RFC 4226 test vectors
    secret = 'GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ'  # "12345678901234567890" in Base32
    
    # Expected values from RFC 4226 (using SHA1, 6 digits)
    expected_codes = [
        '755224',  # counter 0
        '287082',  # counter 1
        '359152',  # counter 2
        '969429',  # counter 3
        '338314',  # counter 4
        '254676',  # counter 5
        '287922',  # counter 6
        '162583',  # counter 7
        '399871',  # counter 8
        '520489',  # counter 9
    ]
    
    for counter, expected in enumerate(expected_codes):
        code = generate_hotp(secret, counter)
        assert code == expected, f"HOTP failed at counter {counter}: got {code}, expected {expected}"
        
        # Test validation
        assert validate_hotp(secret, counter, code), "HOTP validation failed"
    
    # Test invalid code
    assert not validate_hotp(secret, 0, '000000')
    
    # Test different digit counts
    code6 = generate_hotp(secret, 0, digits=6)
    code7 = generate_hotp(secret, 0, digits=7)
    code8 = generate_hotp(secret, 0, digits=8)
    
    assert len(code6) == 6
    assert len(code7) == 7
    assert len(code8) == 8
    
    # Test different algorithms
    sha1 = generate_hotp(secret, 0, algorithm='SHA1')
    sha256 = generate_hotp(secret, 0, algorithm='SHA256')
    sha512 = generate_hotp(secret, 0, algorithm='SHA512')
    
    assert len(sha1) == 6
    assert len(sha256) == 6
    assert len(sha512) == 6
    
    print("  ✓ HOTP functions passed")


def test_totp():
    """Test TOTP generation and validation."""
    print("Testing TOTP functions...")
    
    secret = 'JBSWY3DPEHPK3PXP'
    
    # Test with specific timestamp (RFC 6238 test vector)
    # timestamp 1234567890 should give '680647' with SHA1, 8 digits
    # But we're using 6 digits, so let's test basic functionality
    
    # Test generation
    code = generate_totp(secret)
    assert len(code) == 6
    assert code.isdigit()
    
    # Test validation with current time
    assert validate_totp(secret, code)
    
    # Test with specific timestamp
    timestamp = 1234567890
    code = generate_totp(secret, timestamp=timestamp, digits=6, period=30)
    assert len(code) == 6
    
    # Test window validation
    assert validate_totp(secret, code, timestamp=timestamp, window=1)
    
    # Test code at different time periods should be different
    code1 = generate_totp(secret, timestamp=1000, period=30)
    code2 = generate_totp(secret, timestamp=1030, period=30)
    assert code1 != code2
    
    print("  ✓ TOTP functions passed")


def test_uri():
    """Test OTP URI generation and parsing."""
    print("Testing URI functions...")
    
    secret = 'JBSWY3DPEHPK3PXP'
    account = 'user@example.com'
    issuer = 'TestApp'
    
    # Test TOTP URI
    totp_uri = build_totp_uri(secret, account, issuer)
    assert totp_uri.startswith('otpauth://totp/')
    assert 'secret=' in totp_uri
    assert 'issuer=' in totp_uri
    assert quote(account) in totp_uri or account in totp_uri
    
    # Parse TOTP URI
    parsed = parse_otp_uri(totp_uri)
    assert parsed['type'] == 'totp'
    assert parsed['secret'] == secret
    assert parsed['issuer'] == issuer
    assert parsed['digits'] == DEFAULT_DIGITS
    assert parsed['period'] == DEFAULT_PERIOD
    
    # Test HOTP URI
    hotp_uri = build_hotp_uri(secret, account, issuer, counter=0)
    assert hotp_uri.startswith('otpauth://hotp/')
    assert 'counter=0' in hotp_uri
    
    # Parse HOTP URI
    parsed = parse_otp_uri(hotp_uri)
    assert parsed['type'] == 'hotp'
    assert parsed['counter'] == 0
    
    # Test custom parameters
    custom_uri = build_totp_uri(secret, account, issuer, digits=8, period=60,
                                algorithm='SHA256')
    assert 'digits=8' in custom_uri
    assert 'period=60' in custom_uri
    assert 'algorithm=SHA256' in custom_uri
    
    print("  ✓ URI functions passed")


def test_recovery_codes():
    """Test recovery codes generation and validation."""
    print("Testing recovery codes...")
    
    # Generate recovery codes
    codes = generate_recovery_codes(10, 8)
    assert len(codes) == 10
    
    # All codes should be unique
    assert len(codes) == len(set(codes))
    
    # Codes should have dash in middle
    for code in codes:
        assert '-' in code
        parts = code.split('-')
        assert len(parts) == 2
        assert len(parts[0]) == 4
        assert len(parts[1]) == 4
    
    # Test validation
    valid_code = codes[0]
    is_valid, remaining = validate_recovery_code(codes, valid_code)
    assert is_valid
    assert valid_code not in remaining
    assert len(remaining) == 9
    
    # Test with consume=False
    codes = generate_recovery_codes(5)
    is_valid, remaining = validate_recovery_code(codes, codes[0], consume=False)
    assert is_valid
    assert len(remaining) == 5  # Code not consumed
    
    # Test invalid code
    is_valid, remaining = validate_recovery_code(codes, 'ZZZZ-ZZZZ')
    assert not is_valid
    
    # Test code with spaces (should be normalized)
    codes = generate_recovery_codes(1, 8)
    code = codes[0].replace('-', ' ')
    is_valid, _ = validate_recovery_code(codes, code)
    assert is_valid
    
    print("  ✓ Recovery codes passed")


def test_time_utilities():
    """Test time utility functions."""
    print("Testing time utilities...")
    
    # Test remaining seconds
    remaining = get_remaining_seconds()
    assert 0 <= remaining <= DEFAULT_PERIOD
    
    # Test with specific timestamp
    assert get_remaining_seconds(period=30, timestamp=0) == 30
    assert get_remaining_seconds(period=30, timestamp=15) == 15
    assert get_remaining_seconds(period=30, timestamp=30) == 30
    
    # Test format_code
    assert format_code('123456') == '123 456'
    assert format_code('12345678', 4) == '1234 5678'
    assert format_code('12345678', 2) == '12 34 56 78'
    
    print("  ✓ Time utilities passed")


def test_totp_class():
    """Test TOTP class."""
    print("Testing TOTP class...")
    
    secret = generate_secret()
    totp = TOTP(secret)
    
    # Test generation
    code = totp.generate()
    assert len(code) == 6
    assert code.isdigit()
    
    # Test validation
    assert totp.validate(code)
    
    # Test URI generation
    uri = totp.get_uri('user@test.com', 'MyApp')
    assert uri.startswith('otpauth://totp/')
    
    # Test remaining seconds
    remaining = totp.get_remaining_seconds()
    assert 0 <= remaining <= 30
    
    # Test custom parameters
    totp8 = TOTP(secret, digits=8, period=60, algorithm='SHA256')
    code8 = totp8.generate()
    assert len(code8) == 8
    
    print("  ✓ TOTP class passed")


def test_hotp_class():
    """Test HOTP class."""
    print("Testing HOTP class...")
    
    secret = generate_secret()
    hotp = HOTP(secret)
    
    # Test initial counter
    assert hotp.counter == 0
    
    # Test generation with auto-increment
    code0 = hotp.generate()
    assert hotp.counter == 1
    
    code1 = hotp.generate()
    assert hotp.counter == 2
    
    # Codes should be different
    assert code0 != code1
    
    # Test validation
    assert hotp.validate(code0, 0)
    assert hotp.validate(code1, 1)
    
    # Test URI generation
    uri = hotp.get_uri('user@test.com', 'MyApp')
    assert uri.startswith('otpauth://hotp/')
    
    # Test reset counter
    hotp.reset_counter(100)
    assert hotp.counter == 100
    
    # Test custom parameters
    hotp8 = HOTP(secret, digits=8, algorithm='SHA512')
    code8 = hotp8.generate(0)
    assert len(code8) == 8
    
    print("  ✓ HOTP class passed")


def test_error_handling():
    """Test error handling."""
    print("Testing error handling...")
    
    # Invalid digits
    try:
        generate_hotp(generate_secret(), 0, digits=5)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Digits" in str(e)
    
    # Invalid algorithm
    try:
        generate_hotp(generate_secret(), 0, algorithm='MD5')
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Algorithm" in str(e)
    
    # Invalid Base32
    try:
        decode_base32('!@#$%')
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # Invalid OTP URI
    try:
        parse_otp_uri('https://example.com')
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "otpauth" in str(e)
    
    # Validate with invalid secret
    assert not validate_totp('invalid!', '123456')
    assert not validate_hotp('invalid!', 0, '123456')
    
    print("  ✓ Error handling passed")


def run_tests():
    """Run all tests."""
    print("=" * 50)
    print("OTP Utilities Test Suite")
    print("=" * 50)
    
    test_base32()
    test_hotp()
    test_totp()
    test_uri()
    test_recovery_codes()
    test_time_utilities()
    test_totp_class()
    test_hotp_class()
    test_error_handling()
    
    print("=" * 50)
    print("✅ All tests passed!")
    print("=" * 50)


if __name__ == '__main__':
    run_tests()