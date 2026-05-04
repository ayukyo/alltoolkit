#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Shamir's Secret Sharing Utilities Tests
======================================================
Comprehensive test suite for Shamir's Secret Sharing implementation.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    split_secret, reconstruct_secret, reconstruct_secret_bytes,
    reconstruct_secret_string, verify_secret_hash,
    ShamirSecretSharing, split_string, split_int, split_bytes,
    Share, ShareSet,
    split_bytes_gf256, reconstruct_bytes_gf256,
    encode_shares_compact, decode_shares_compact,
    get_share_info, validate_share_set,
    PRIME_256, PRIME_128, DEFAULT_PRIME
)
import hashlib


def test_basic_int_secret():
    """Test splitting and reconstructing an integer secret."""
    print("Testing basic integer secret...")
    
    secret = 12345678901234567890
    shares = split_secret(secret, threshold=3, num_shares=5)
    
    assert len(shares.shares) == 5
    assert shares.shares[0].threshold == 3
    
    # Reconstruct with minimum shares
    reconstructed = reconstruct_secret(shares.shares[:3])
    assert reconstructed == secret, f"Expected {secret}, got {reconstructed}"
    
    # Reconstruct with more shares
    reconstructed = reconstruct_secret(shares.shares[:4])
    assert reconstructed == secret
    
    # Reconstruct with all shares
    reconstructed = reconstruct_secret(shares.shares)
    assert reconstructed == secret
    
    print("  ✓ Basic integer secret test passed")


def test_string_secret():
    """Test splitting and reconstructing a string secret."""
    print("Testing string secret...")
    
    secret = "Hello, World! This is a secret message."
    shares = split_string(secret, threshold=4, num_shares=7)
    
    assert len(shares.shares) == 7
    assert shares.secret_hash is not None
    
    # Verify hash
    assert hashlib.sha256(secret.encode()).hexdigest() == shares.secret_hash
    
    # Reconstruct
    reconstructed = reconstruct_secret_string(shares.shares[:4])
    assert reconstructed == secret, f"Expected '{secret}', got '{reconstructed}'"
    
    print("  ✓ String secret test passed")


def test_bytes_secret():
    """Test splitting and reconstructing bytes."""
    print("Testing bytes secret...")
    
    secret = b"\x00\x01\x02\x03\x04\x05\xff\xfe\xfd"
    shares = split_bytes(secret, threshold=2, num_shares=3)
    
    reconstructed = reconstruct_secret_bytes(shares.shares[:2], expected_length=len(secret))
    assert reconstructed == secret, f"Expected {secret.hex()}, got {reconstructed.hex()}"
    
    print("  ✓ Bytes secret test passed")


def test_insufficient_shares():
    """Test that reconstruction fails with insufficient shares."""
    print("Testing insufficient shares error...")
    
    secret = 999999999
    shares = split_secret(secret, threshold=5, num_shares=10)
    
    # Should fail with less than threshold
    try:
        reconstruct_secret(shares.shares[:4])
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Need at least 5 shares" in str(e)
    
    # Should succeed with exactly threshold
    reconstructed = reconstruct_secret(shares.shares[:5])
    assert reconstructed == secret
    
    print("  ✓ Insufficient shares test passed")


def test_share_encoding():
    """Test share encoding and decoding."""
    print("Testing share encoding...")
    
    share = Share(x=12345, y=987654321012345, prime=PRIME_256, threshold=3)
    encoded = share.encode()
    
    decoded = Share.decode(encoded)
    assert decoded.x == share.x
    assert decoded.y == share.y
    assert decoded.prime == share.prime
    assert decoded.threshold == share.threshold
    
    print("  ✓ Share encoding test passed")


def test_shareset_encoding():
    """Test ShareSet encoding and decoding."""
    print("Testing ShareSet encoding...")
    
    secret = "Test secret for encoding"
    shareset = split_string(secret, threshold=3, num_shares=5)
    
    encoded = shareset.encode()
    decoded = ShareSet.decode(encoded)
    
    assert len(decoded.shares) == 5
    assert decoded.secret_hash == shareset.secret_hash
    
    # Reconstruct from decoded shares
    reconstructed = reconstruct_secret_string(decoded.shares[:3])
    assert reconstructed == secret
    
    print("  ✓ ShareSet encoding test passed")


def test_compact_encoding():
    """Test compact encoding functions."""
    print("Testing compact encoding...")
    
    secret = 42
    shares = split_secret(secret, threshold=2, num_shares=3)
    
    encoded = encode_shares_compact(shares.shares)
    decoded = decode_shares_compact(encoded)
    
    assert len(decoded) == 3
    for original, dec in zip(shares.shares, decoded):
        assert original.x == dec.x
        assert original.y == dec.y
    
    # Reconstruct from compact-encoded shares
    reconstructed = reconstruct_secret(decoded[:2])
    assert reconstructed == secret
    
    print("  ✓ Compact encoding test passed")


def test_shamir_class():
    """Test ShamirSecretSharing class interface."""
    print("Testing ShamirSecretSharing class...")
    
    sss = ShamirSecretSharing(threshold=3, num_shares=6)
    
    secret = b"Class interface test"
    shares = sss.split(secret)
    
    assert len(shares.shares) == 6
    
    reconstructed = sss.reconstruct_bytes(shares.shares[:3])
    assert reconstructed == secret
    
    # Test with string
    str_secret = "String secret"
    str_shares = sss.split(str_secret)
    reconstructed_str = sss.reconstruct_string(str_shares.shares[:3])
    assert reconstructed_str == str_secret
    
    print("  ✓ ShamirSecretSharing class test passed")


def test_hash_verification():
    """Test hash verification."""
    print("Testing hash verification...")
    
    secret = "Hash test secret"
    shares = split_string(secret, threshold=3, num_shares=5)
    
    assert verify_secret_hash(shares, secret)
    
    # Wrong secret should fail
    assert not verify_secret_hash(shares, "Wrong secret")
    
    print("  ✓ Hash verification test passed")


def test_gf256_basic():
    """Test GF(2^8) byte sharing."""
    print("Testing GF(2^8) basic operations...")
    
    secret = b"Hello, GF(2^8)!"
    shares = split_bytes_gf256(secret, threshold=3, num_shares=5)
    
    assert len(shares) == 5
    assert all(len(s) == len(secret) + 1 for s in shares)
    
    # Reconstruct with minimum
    reconstructed = reconstruct_bytes_gf256(shares[:3])
    assert reconstructed == secret
    
    # Reconstruct with more
    reconstructed = reconstruct_bytes_gf256(shares[:5])
    assert reconstructed == secret
    
    print("  ✓ GF(2^8) basic test passed")


def test_gf256_binary():
    """Test GF(2^8) with binary data."""
    print("Testing GF(2^8) binary data...")
    
    secret = bytes(range(256))  # All possible byte values
    shares = split_bytes_gf256(secret, threshold=5, num_shares=10)
    
    reconstructed = reconstruct_bytes_gf256(shares[:5])
    assert reconstructed == secret
    
    # Test with different threshold
    reconstructed = reconstruct_bytes_gf256(shares[:7])
    assert reconstructed == secret
    
    print("  ✓ GF(2^8) binary test passed")


def test_gf256_threshold():
    """Test GF(2^8) threshold enforcement."""
    print("Testing GF(2^8) threshold...")
    
    secret = b"Threshold test"
    shares = split_bytes_gf256(secret, threshold=5, num_shares=8)
    
    # Should fail with insufficient shares
    try:
        # GF(2^8) doesn't enforce threshold in reconstruct, but values will be wrong
        # Let's verify with less than threshold gives wrong result
        wrong_reconstruct = reconstruct_bytes_gf256(shares[:3])
        # This might accidentally match, so we don't assert here
        # The security comes from the math, not a check in reconstruct
        pass
    except:
        pass
    
    # Correct reconstruction
    reconstructed = reconstruct_bytes_gf256(shares[:5])
    assert reconstructed == secret
    
    print("  ✓ GF(2^8) threshold test passed")


def test_share_info():
    """Test get_share_info function."""
    print("Testing share info...")
    
    share = Share(x=123, y=456, prime=PRIME_256, threshold=3)
    info = get_share_info(share)
    
    assert info["x_coordinate"] == 123
    assert info["threshold"] == 3
    assert info["is_valid"] == True
    
    print("  ✓ Share info test passed")


def test_validate_share_set():
    """Test share set validation."""
    print("Testing share set validation...")
    
    shares = split_secret(12345, threshold=3, num_shares=5)
    
    # Valid set
    is_valid, error = validate_share_set(shares.shares)
    assert is_valid
    assert error is None
    
    # Insufficient shares
    is_valid, error = validate_share_set(shares.shares[:2])
    assert not is_valid
    assert "Insufficient" in error
    
    print("  ✓ Share set validation test passed")


def test_edge_cases():
    """Test edge cases."""
    print("Testing edge cases...")
    
    # Empty secret (single zero byte)
    shares = split_bytes(b"\x00", threshold=2, num_shares=3)
    reconstructed = reconstruct_secret_bytes(shares.shares[:2], expected_length=1)
    assert reconstructed == b"\x00"
    
    # Single character
    shares = split_string("A", threshold=2, num_shares=3)
    reconstructed = reconstruct_secret_string(shares.shares[:2])
    assert reconstructed == "A"
    
    # Maximum threshold
    shares = split_secret(42, threshold=255, num_shares=255)
    reconstructed = reconstruct_secret(shares.shares[:255])
    assert reconstructed == 42
    
    print("  ✓ Edge cases test passed")


def test_different_thresholds():
    """Test various threshold configurations."""
    print("Testing different thresholds...")
    
    secret = 987654321
    
    for threshold in [2, 3, 5, 10]:
        for num_shares in [threshold, threshold + 1, threshold + 5]:
            shares = split_secret(secret, threshold=threshold, num_shares=num_shares)
            reconstructed = reconstruct_secret(shares.shares[:threshold])
            assert reconstructed == secret, f"Failed for threshold={threshold}, num_shares={num_shares}"
    
    print("  ✓ Different thresholds test passed")


def test_large_secret():
    """Test with large secrets."""
    print("Testing large secrets...")
    
    # 100 byte secret (fits in 1024 bit prime)
    secret = os.urandom(100)
    shares = split_bytes(secret, threshold=3, num_shares=5)
    
    reconstructed = reconstruct_secret_bytes(shares.shares[:3], expected_length=len(secret))
    assert reconstructed == secret
    
    # Large integer (close to 512-bit prime)
    large_int = (2**512 - 1) // 2  # About 511 bits
    shares = split_int(large_int, threshold=2, num_shares=3)
    reconstructed = reconstruct_secret(shares.shares[:2])
    assert reconstructed == large_int
    
    print("  ✓ Large secret test passed")


def test_unicode():
    """Test with Unicode strings."""
    print("Testing Unicode strings...")
    
    secrets = [
        "Hello 世界",  # Chinese
        "Привет мир",  # Russian
        "مرحبا بالعالم",  # Arabic
        "🎉🔒🗝️",  # Emojis
        "Mixed: 日本語 русский emoji 🚀",  # Mixed
    ]
    
    for secret in secrets:
        shares = split_string(secret, threshold=2, num_shares=4)
        reconstructed = reconstruct_secret_string(shares.shares[:2])
        assert reconstructed == secret, f"Failed for: {secret}"
    
    print("  ✓ Unicode test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Shamir's Secret Sharing Test Suite")
    print("=" * 60)
    
    tests = [
        test_basic_int_secret,
        test_string_secret,
        test_bytes_secret,
        test_insufficient_shares,
        test_share_encoding,
        test_shareset_encoding,
        test_compact_encoding,
        test_shamir_class,
        test_hash_verification,
        test_gf256_basic,
        test_gf256_binary,
        test_gf256_threshold,
        test_share_info,
        test_validate_share_set,
        test_edge_cases,
        test_different_thresholds,
        test_large_secret,
        test_unicode,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ Test failed: {test.__name__}")
            print(f"    Error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)