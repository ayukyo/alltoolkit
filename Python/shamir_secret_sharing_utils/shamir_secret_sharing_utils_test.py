#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shamir Secret Sharing Utils Test Suite
Tests for Shamir's Secret Sharing implementation
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shamir_secret_sharing_utils.mod import (
    Share, ShareSet,
    split_secret, reconstruct_secret, reconstruct_secret_bytes, reconstruct_secret_string,
    verify_secret_hash, ShamirSecretSharing,
    split_string, split_int, split_bytes,
    split_bytes_gf256, reconstruct_bytes_gf256,
    encode_shares_compact, decode_shares_compact,
    get_share_info, validate_share_set,
    PRIME_128, PRIME_256, PRIME_512, DEFAULT_PRIME
)


class TestResultCollector:
    """Collects test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_result(self, name, passed, message=""):
        self.tests.append((name, passed, message))
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Shamir Secret Sharing Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}")
        if self.failed > 0:
            print("Failed tests:")
            for name, passed, msg in self.tests:
                if not passed:
                    print(f"  - {name}: {msg}")
        return self.failed == 0


results = TestResultCollector()


def test_share_dataclass():
    """Test Share dataclass"""
    try:
        share = Share(x=1, y=12345, prime=PRIME_128, threshold=3)
        assert share.x == 1
        assert share.y == 12345
        assert share.threshold == 3
        
        # Encode/decode
        encoded = share.encode()
        decoded = Share.decode(encoded)
        assert decoded.x == share.x
        assert decoded.y == share.y
        
        results.add_result("share_dataclass", True)
    except Exception as e:
        results.add_result("share_dataclass", False, str(e))


def test_share_set():
    """Test ShareSet dataclass"""
    try:
        shares = [
            Share(x=1, y=100, prime=PRIME_128, threshold=3),
            Share(x=2, y=200, prime=PRIME_128, threshold=3),
            Share(x=3, y=300, prime=PRIME_128, threshold=3),
        ]
        set = ShareSet(shares=shares, secret_hash="abc123")
        
        assert len(set.shares) == 3
        assert set.secret_hash == "abc123"
        
        # Encode/decode
        encoded = set.encode()
        decoded = ShareSet.decode(encoded)
        assert len(decoded.shares) == 3
        
        results.add_result("share_set", True)
    except Exception as e:
        results.add_result("share_set", False, str(e))


def test_split_reconstruct_int():
    """Test splitting and reconstructing an integer"""
    try:
        secret = 12345
        
        # Split
        shares = split_secret(secret, threshold=3, num_shares=5)
        assert len(shares.shares) == 5
        assert shares.shares[0].threshold == 3
        
        # Reconstruct with minimum shares
        reconstructed = reconstruct_secret(shares.shares[:3])
        assert reconstructed == secret
        
        # Reconstruct with more shares
        reconstructed = reconstruct_secret(shares.shares[:5])
        assert reconstructed == secret
        
        results.add_result("split_reconstruct_int", True)
    except Exception as e:
        results.add_result("split_reconstruct_int", False, str(e))


def test_split_reconstruct_bytes():
    """Test splitting and reconstructing bytes"""
    try:
        secret = b"Hello, World!"
        
        # Split
        shares = split_bytes(secret, threshold=3, num_shares=5)
        assert len(shares.shares) == 5
        
        # Reconstruct
        reconstructed = reconstruct_secret_bytes(shares.shares[:3], expected_length=len(secret))
        assert reconstructed == secret
        
        results.add_result("split_reconstruct_bytes", True)
    except Exception as e:
        results.add_result("split_reconstruct_bytes", False, str(e))


def test_split_reconstruct_string():
    """Test splitting and reconstructing a string"""
    try:
        secret = "My secret password!"
        
        # Split
        shares = split_string(secret, threshold=3, num_shares=5)
        assert len(shares.shares) == 5
        
        # Reconstruct
        reconstructed = reconstruct_secret_string(shares.shares[:3])
        assert reconstructed == secret
        
        results.add_result("split_reconstruct_string", True)
    except Exception as e:
        results.add_result("split_reconstruct_string", False, str(e))


def test_threshold_validation():
    """Test threshold validation"""
    try:
        # Threshold < 2 should raise
        try:
            split_secret(123, threshold=1, num_shares=3)
            results.add_result("threshold_validation", False, "Should raise for threshold < 2")
        except ValueError:
            pass
        
        # Shares < threshold should raise
        try:
            split_secret(123, threshold=5, num_shares=3)
            results.add_result("threshold_validation", False, "Should raise for shares < threshold")
        except ValueError:
            pass
        
        results.add_result("threshold_validation", True)
    except Exception as e:
        results.add_result("threshold_validation", False, str(e))


def test_insufficient_shares():
    """Test reconstruction with insufficient shares"""
    try:
        shares = split_secret(12345, threshold=3, num_shares=5)
        
        # Try to reconstruct with fewer than threshold
        try:
            reconstruct_secret(shares.shares[:2])
            results.add_result("insufficient_shares", False, "Should raise for insufficient shares")
        except ValueError:
            pass
        
        results.add_result("insufficient_shares", True)
    except Exception as e:
        results.add_result("insufficient_shares", False, str(e))


def test_hash_verification():
    """Test hash verification"""
    try:
        secret = b"test secret"
        
        # Split with hash
        shares = split_secret(secret, threshold=3, num_shares=5, include_hash=True)
        assert shares.secret_hash is not None
        
        # Reconstruct and verify
        reconstructed = reconstruct_secret_bytes(shares.shares[:3])
        assert verify_secret_hash(shares, reconstructed) == True
        
        # Wrong secret
        assert verify_secret_hash(shares, b"wrong") == False
        
        results.add_result("hash_verification", True)
    except Exception as e:
        results.add_result("hash_verification", False, str(e))


def test_shamir_secret_sharing_class():
    """Test ShamirSecretSharing class"""
    try:
        sss = ShamirSecretSharing(threshold=3, num_shares=5)
        
        assert sss.threshold == 3
        assert sss.num_shares == 5
        
        # Split
        shares = sss.split(b"test")
        assert len(shares.shares) == 5
        
        # Reconstruct
        reconstructed = sss.reconstruct_bytes(shares.shares[:3])
        assert reconstructed == b"test"
        
        # Reconstruct string
        shares_str = sss.split("hello")
        reconstructed_str = sss.reconstruct_string(shares_str.shares[:3])
        assert reconstructed_str == "hello"
        
        results.add_result("shamir_secret_sharing_class", True)
    except Exception as e:
        results.add_result("shamir_secret_sharing_class", False, str(e))


def test_gf256_bytes():
    """Test GF(2^8) byte-level sharing"""
    try:
        secret = b"\x01\x02\x03\x04\x05"
        
        # Split
        shares = split_bytes_gf256(secret, threshold=3, num_shares=5)
        assert len(shares) == 5
        assert len(shares[0]) == len(secret) + 1  # x-coordinate + data
        
        # Reconstruct
        reconstructed = reconstruct_bytes_gf256(shares[:3])
        assert reconstructed == secret
        
        # Reconstruct with more shares
        reconstructed = reconstruct_bytes_gf256(shares[:5])
        assert reconstructed == secret
        
        results.add_result("gf256_bytes", True)
    except Exception as e:
        results.add_result("gf256_bytes", False, str(e))


def test_gf256_threshold_validation():
    """Test GF(2^8) threshold validation"""
    try:
        # Threshold < 2 should raise
        try:
            split_bytes_gf256(b"test", threshold=1, num_shares=3)
            results.add_result("gf256_threshold_validation", False, "Should raise for threshold < 2")
        except ValueError:
            pass
        
        # Shares > 255 should raise
        try:
            split_bytes_gf256(b"test", threshold=3, num_shares=256)
            results.add_result("gf256_threshold_validation", False, "Should raise for shares > 255")
        except ValueError:
            pass
        
        results.add_result("gf256_threshold_validation", True)
    except Exception as e:
        results.add_result("gf256_threshold_validation", False, str(e))


def test_encode_decode_compact():
    """Test compact share encoding"""
    try:
        shares = split_secret(12345, threshold=3, num_shares=5)
        
        # Encode compact
        encoded = encode_shares_compact(shares.shares)
        assert len(encoded) > 0
        
        # Decode
        decoded = decode_shares_compact(encoded)
        assert len(decoded) == 5
        
        # Verify reconstruction works
        reconstructed = reconstruct_secret(decoded[:3])
        assert reconstructed == 12345
        
        results.add_result("encode_decode_compact", True)
    except Exception as e:
        results.add_result("encode_decode_compact", False, str(e))


def test_get_share_info():
    """Test share info function"""
    try:
        shares = split_secret(12345, threshold=3, num_shares=5)
        
        info = get_share_info(shares.shares[0])
        assert info["threshold"] == 3
        assert info["x_coordinate"] > 0
        assert info["is_valid"] == True
        
        results.add_result("get_share_info", True)
    except Exception as e:
        results.add_result("get_share_info", False, str(e))


def test_validate_share_set():
    """Test share set validation"""
    try:
        shares = split_secret(12345, threshold=3, num_shares=5)
        
        valid, error = validate_share_set(shares.shares)
        assert valid == True
        assert error is None
        
        # Insufficient shares
        valid, error = validate_share_set(shares.shares[:2])
        assert valid == False
        assert "Insufficient" in error
        
        # Empty set
        valid, error = validate_share_set([])
        assert valid == False
        
        results.add_result("validate_share_set", True)
    except Exception as e:
        results.add_result("validate_share_set", False, str(e))


def test_primes():
    """Test prime constants"""
    try:
        assert PRIME_128 > 0
        assert PRIME_256 > PRIME_128
        assert PRIME_512 > PRIME_256
        assert DEFAULT_PRIME == PRIME_512
        
        results.add_result("primes", True)
    except Exception as e:
        results.add_result("primes", False, str(e))


def test_different_thresholds():
    """Test different threshold values"""
    try:
        for threshold in [2, 3, 4, 5]:
            for num_shares in [threshold, threshold + 1, threshold + 2]:
                shares = split_secret(12345, threshold=threshold, num_shares=num_shares)
                assert len(shares.shares) == num_shares
                
                reconstructed = reconstruct_secret(shares.shares[:threshold])
                assert reconstructed == 12345
        
        results.add_result("different_thresholds", True)
    except Exception as e:
        results.add_result("different_thresholds", False, str(e))


def test_large_secret():
    """Test large secret"""
    try:
        # Large bytes (50 bytes - within PRIME_512 bounds)
        secret = b"A" * 50
        shares = split_bytes(secret, threshold=3, num_shares=5)
        reconstructed = reconstruct_secret_bytes(shares.shares[:3])
        assert reconstructed == secret
        
        # Large integer (within PRIME_512 bounds)
        secret_int = 10**20  # 20-digit number
        shares = split_int(secret_int, threshold=3, num_shares=5)
        reconstructed = reconstruct_secret(shares.shares[:3])
        assert reconstructed == secret_int
        
        results.add_result("large_secret", True)
    except Exception as e:
        results.add_result("large_secret", False, str(e))


def test_convenience_functions():
    """Test convenience functions"""
    try:
        # split_int
        shares = split_int(999, threshold=2, num_shares=3)
        assert reconstruct_secret(shares.shares[:2]) == 999
        
        # split_bytes
        shares = split_bytes(b"test", threshold=2, num_shares=3)
        assert reconstruct_secret_bytes(shares.shares[:2]) == b"test"
        
        # split_string
        shares = split_string("hello", threshold=2, num_shares=3)
        assert reconstruct_secret_string(shares.shares[:2]) == "hello"
        
        results.add_result("convenience_functions", True)
    except Exception as e:
        results.add_result("convenience_functions", False, str(e))


def test_secret_security():
    """Test that less than threshold shares reveals nothing"""
    try:
        secret = 12345
        shares = split_secret(secret, threshold=5, num_shares=10)
        
        # 4 shares (less than threshold) should not reveal secret
        # We can't prove they reveal nothing, but we verify they don't equal secret
        partial_shares = shares.shares[:4]
        
        # Try to reconstruct should fail
        try:
            reconstruct_secret(partial_shares)
            results.add_result("secret_security", False, "Should raise for insufficient shares")
        except ValueError:
            pass
        
        results.add_result("secret_security", True)
    except Exception as e:
        results.add_result("secret_security", False, str(e))


def test_empty_share_set():
    """Test empty share set handling"""
    try:
        # Empty list reconstruction
        try:
            reconstruct_secret([])
            results.add_result("empty_share_set", False, "Should raise for empty shares")
        except ValueError:
            pass
        
        # Empty GF256 reconstruction
        try:
            reconstruct_bytes_gf256([])
            results.add_result("empty_share_set", False, "Should raise for empty shares")
        except ValueError:
            pass
        
        # Empty compact decode
        decoded = decode_shares_compact("")
        assert decoded == []
        
        results.add_result("empty_share_set", True)
    except Exception as e:
        results.add_result("empty_share_set", False, str(e))


def test_share_set_reconstruction():
    """Test reconstruction from ShareSet"""
    try:
        secret = 12345
        shares = split_secret(secret, threshold=3, num_shares=5)
        
        # Reconstruct from ShareSet directly
        reconstructed = reconstruct_secret(shares)
        assert reconstructed == secret
        
        reconstructed_bytes = reconstruct_secret_bytes(shares)
        expected_bytes = secret.to_bytes(2, 'big')
        assert reconstructed_bytes == expected_bytes
        
        results.add_result("share_set_reconstruction", True)
    except Exception as e:
        results.add_result("share_set_reconstruction", False, str(e))


def test_unicode_secret():
    """Test Unicode string secrets"""
    try:
        secret = "你好世界 🌍"
        shares = split_string(secret, threshold=3, num_shares=5)
        
        reconstructed = reconstruct_secret_string(shares.shares[:3])
        assert reconstructed == secret
        
        results.add_result("unicode_secret", True)
    except Exception as e:
        results.add_result("unicode_secret", False, str(e))


def test_edge_cases():
    """Test edge cases"""
    try:
        # Zero secret
        shares = split_int(0, threshold=2, num_shares=3)
        reconstructed = reconstruct_secret(shares.shares[:2])
        assert reconstructed == 0
        
        # Single byte - use GF256 for reliability
        shares = split_bytes_gf256(b"\x00", threshold=2, num_shares=3)
        reconstructed = reconstruct_bytes_gf256(shares[:2])
        assert reconstructed == b"\x00"
        
        # Empty bytes - use GF256
        shares = split_bytes_gf256(b"", threshold=2, num_shares=3)
        reconstructed = reconstruct_bytes_gf256(shares[:2])
        assert reconstructed == b""
        
        results.add_result("edge_cases", True)
    except Exception as e:
        results.add_result("edge_cases", False, str(e))


# Run all tests
def run_tests():
    """Run all test functions"""
    test_share_dataclass()
    test_share_set()
    test_split_reconstruct_int()
    test_split_reconstruct_bytes()
    test_split_reconstruct_string()
    test_threshold_validation()
    test_insufficient_shares()
    test_hash_verification()
    test_shamir_secret_sharing_class()
    test_gf256_bytes()
    test_gf256_threshold_validation()
    test_encode_decode_compact()
    test_get_share_info()
    test_validate_share_set()
    test_primes()
    test_different_thresholds()
    test_large_secret()
    test_convenience_functions()
    test_secret_security()
    test_empty_share_set()
    test_share_set_reconstruction()
    test_unicode_secret()
    test_edge_cases()
    
    return results.summary()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)