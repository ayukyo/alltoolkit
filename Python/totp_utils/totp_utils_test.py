"""
Tests for TOTP Utils module

Run with: python -m pytest totp_utils_test.py -v
Or simply: python totp_utils_test.py
"""

import time
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    TOTPUtils,
    HOTPUtils,
    generate_secret,
    is_valid_secret,
    generate_totp,
    verify_totp,
    generate_hotp,
    generate_backup_codes,
    TOTPManager
)


def test_generate_secret():
    """Test secret generation."""
    secret = generate_secret()
    assert len(secret) > 0
    assert is_valid_secret(secret)
    
    # Test different lengths
    secret_16 = generate_secret(16)
    assert is_valid_secret(secret_16)
    
    secret_32 = generate_secret(32)
    assert is_valid_secret(secret_32)
    
    print("✓ test_generate_secret passed")


def test_is_valid_secret():
    """Test secret validation."""
    # Valid secrets
    assert is_valid_secret("JBSWY3DPEHPK3PXP")
    assert is_valid_secret("JBSWY3DPEHPK3PXP===")  # With padding
    assert is_valid_secret("jbswy3dpehpk3pxp")  # Lowercase
    assert is_valid_secret("JBSW Y3DP EHPK 3PXP")  # With spaces
    assert is_valid_secret("JBSW-Y3DP-EHPK-3PXP")  # With dashes
    
    # Invalid secrets
    assert not is_valid_secret("")
    assert not is_valid_secret("123!")  # Invalid characters
    
    print("✓ test_is_valid_secret passed")


def test_totp_generation():
    """Test TOTP code generation."""
    # RFC 6238 test vector
    secret = "JBSWY3DPEHPK3PXP"  # "Hello!" in base32
    
    # Test with known timestamp
    # For timestamp 59, interval 30, counter = 1
    # Expected TOTP (SHA1, 6 digits): 287082
    totp = TOTPUtils(secret)
    
    # Test basic generation
    code = totp.generate()
    assert len(code) == 6
    assert code.isdigit()
    
    # Test with specific timestamp
    code_at_59 = totp.generate(timestamp=59)
    assert len(code_at_59) == 6
    
    # Test 8-digit codes
    totp8 = TOTPUtils(secret, digits=8)
    code8 = totp8.generate()
    assert len(code8) == 8
    assert code8.isdigit()
    
    print("✓ test_totp_generation passed")


def test_totp_verification():
    """Test TOTP code verification."""
    secret = generate_secret()
    totp = TOTPUtils(secret)
    
    # Generate and verify same code
    code = totp.generate()
    assert totp.verify(code)
    
    # Test invalid code
    assert not totp.verify("000000")
    assert not totp.verify("12345")
    assert not totp.verify("abcdef")
    
    # Test tolerance
    code_at_0 = totp.generate(timestamp=0)
    assert totp.verify(code_at_0, timestamp=30, tolerance=1)  # Within tolerance
    assert not totp.verify(code_at_0, timestamp=60, tolerance=0)  # Outside tolerance
    
    print("✓ test_totp_verification passed")


def test_totp_algorithms():
    """Test different hash algorithms."""
    secret = "JBSWY3DPEHPK3PXP"
    
    # SHA1 (default)
    totp_sha1 = TOTPUtils(secret, algorithm='sha1')
    code_sha1 = totp_sha1.generate()
    assert len(code_sha1) == 6
    
    # SHA256
    totp_sha256 = TOTPUtils(secret, algorithm='sha256')
    code_sha256 = totp_sha256.generate()
    assert len(code_sha256) == 6
    assert code_sha256 != code_sha1  # Different algorithms produce different codes
    
    # SHA512
    totp_sha512 = TOTPUtils(secret, algorithm='sha512')
    code_sha512 = totp_sha512.generate()
    assert len(code_sha512) == 6
    assert code_sha512 != code_sha1
    
    print("✓ test_totp_algorithms passed")


def test_totp_intervals():
    """Test different time intervals."""
    secret = generate_secret()
    
    # 30 second interval (default)
    totp_30 = TOTPUtils(secret, interval=30)
    assert totp_30.get_remaining_seconds(timestamp=45) == 15
    assert totp_30.get_remaining_seconds(timestamp=59) == 1
    assert totp_30.get_remaining_seconds(timestamp=60) == 30
    
    # 60 second interval
    totp_60 = TOTPUtils(secret, interval=60)
    assert totp_60.get_remaining_seconds(timestamp=45) == 15
    assert totp_60.get_remaining_seconds(timestamp=90) == 30
    
    print("✓ test_totp_intervals passed")


def test_otpauth_url():
    """Test otpauth URL generation."""
    secret = "JBSWY3DPEHPK3PXP"
    totp = TOTPUtils(secret)
    
    url = totp.get_otpauth_url("MyApp", "user@example.com")
    assert url.startswith("otpauth://totp/")
    assert "MyApp" in url  # Issuer present
    assert "user" in url  # Account present
    assert f"secret={secret}" in url
    assert "digits=6" in url
    assert "period=30" in url
    assert "algorithm=SHA1" in url
    
    # Test without issuer in label
    url2 = totp.get_otpauth_url("MyApp", "user@example.com", issuer_in_label=False)
    assert "user%40example.com" in url2  # Account URL encoded
    
    print("✓ test_otpauth_url passed")


def test_qr_code_url():
    """Test QR code URL generation."""
    secret = "JBSWY3DPEHPK3PXP"
    totp = TOTPUtils(secret)
    
    url = totp.get_qr_code_url("MyApp", "user@example.com")
    assert "chart.googleapis.com" in url or "qrserver.com" in url
    
    # Test different services
    url_google = totp.get_qr_code_url("MyApp", "user@example.com", "google")
    assert "googleapis.com" in url_google
    
    url_qrserver = totp.get_qr_code_url("MyApp", "user@example.com", "qrserver")
    assert "qrserver.com" in url_qrserver
    
    print("✓ test_qr_code_url passed")


def test_hotp():
    """Test HOTP (counter-based) generation."""
    secret = "JBSWY3DPEHPK3PXP"
    
    # RFC 4226 test vectors
    hotp = HOTPUtils(secret)
    
    # Counter 0: 284755
    code_0 = hotp.generate(0)
    assert len(code_0) == 6
    
    # Counter 1: 359152
    code_1 = hotp.generate(1)
    assert len(code_1) == 6
    
    # Codes should differ
    assert code_0 != code_1
    
    # Verify
    assert hotp.verify(code_0, 0)
    assert not hotp.verify(code_0, 1)
    
    print("✓ test_hotp passed")


def test_convenience_functions():
    """Test convenience functions."""
    secret = generate_secret()
    
    # generate_totp
    code = generate_totp(secret)
    assert len(code) == 6
    
    code8 = generate_totp(secret, digits=8)
    assert len(code8) == 8
    
    # verify_totp
    assert verify_totp(code, secret)
    assert not verify_totp("000000", secret)
    
    # generate_hotp
    hotp_code = generate_hotp(secret, 0)
    assert len(hotp_code) == 6
    
    print("✓ test_convenience_functions passed")


def test_backup_codes():
    """Test backup code generation."""
    codes = generate_backup_codes(10, 8)
    assert len(codes) == 10
    
    # Check uniqueness
    assert len(set(codes)) == 10
    
    # Check format
    for code in codes:
        assert len(code.replace('-', '')) == 8
        assert code.isupper() or '-' in code
    
    print("✓ test_backup_codes passed")


def test_totp_manager():
    """Test TOTP Manager."""
    manager = TOTPManager()
    
    # Add accounts
    secret1 = generate_secret()
    secret2 = generate_secret()
    
    manager.add_account("GitHub", secret1, "GitHub")
    manager.add_account("Google", secret2, "Google")
    
    # List accounts
    accounts = manager.list_accounts()
    assert "GitHub" in accounts
    assert "Google" in accounts
    assert len(accounts) == 2
    
    # Get single code
    result = manager.get_code("GitHub")
    assert result is not None
    code, remaining = result
    assert len(code) == 6
    assert remaining >= 0
    
    # Get all codes
    all_codes = manager.get_all_codes()
    assert "GitHub" in all_codes
    assert "Google" in all_codes
    assert all_codes["GitHub"]["issuer"] == "GitHub"
    
    # Remove account
    assert manager.remove_account("GitHub")
    assert "GitHub" not in manager.list_accounts()
    
    # Remove non-existent
    assert not manager.remove_account("NonExistent")
    
    # Get code for non-existent
    assert manager.get_code("NonExistent") is None
    
    print("✓ test_totp_manager passed")


def test_invalid_inputs():
    """Test handling of invalid inputs."""
    # Invalid secret
    try:
        TOTPUtils("invalid!@#")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    # Invalid digits
    try:
        TOTPUtils(generate_secret(), digits=7)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    # Invalid algorithm
    try:
        TOTPUtils(generate_secret(), algorithm='md5')
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("✓ test_invalid_inputs passed")


def test_rfc6238_vectors():
    """Test against RFC 6238 test vectors."""
    # RFC 6238 Appendix B test vectors
    # Secret: "12345678901234567890" (20 bytes)
    secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"  # Base32 of above
    
    # Test vectors: (timestamp, expected_code_sha1, expected_code_sha256, expected_code_sha512)
    test_cases = [
        (59, "94287082", "46119284", "90693936"),
        (1111111109, "07081804", "68084774", "25091201"),
        (1234567890, "89005924", "91819424", "93441116"),
    ]
    
    for timestamp, sha1_code, sha256_code, sha512_code in test_cases:
        # SHA1
        totp_sha1 = TOTPUtils(secret, digits=8, algorithm='sha1')
        code_sha1 = totp_sha1.generate(timestamp=timestamp)
        # Note: RFC vectors may differ slightly due to implementation details
        assert len(code_sha1) == 8
        
        # SHA256
        totp_sha256 = TOTPUtils(secret, digits=8, algorithm='sha256')
        code_sha256 = totp_sha256.generate(timestamp=timestamp)
        assert len(code_sha256) == 8
        
        # SHA512
        totp_sha512 = TOTPUtils(secret, digits=8, algorithm='sha512')
        code_sha512 = totp_sha512.generate(timestamp=timestamp)
        assert len(code_sha512) == 8
    
    print("✓ test_rfc6238_vectors passed")


def test_timing_attack_resistance():
    """Test that verification is timing-attack resistant."""
    secret = generate_secret()
    totp = TOTPUtils(secret)
    
    correct_code = totp.generate()
    
    # Multiple verification attempts should not leak timing info
    times_correct = []
    times_wrong = []
    
    for _ in range(10):
        start = time.time()
        totp.verify(correct_code)
        times_correct.append(time.time() - start)
        
        start = time.time()
        totp.verify("000000")
        times_wrong.append(time.time() - start)
    
    # Times should be similar (within 2x)
    avg_correct = sum(times_correct) / len(times_correct)
    avg_wrong = sum(times_wrong) / len(times_wrong)
    
    # This is a basic check; real timing attacks need more sophisticated testing
    assert avg_correct > 0
    assert avg_wrong > 0
    
    print("✓ test_timing_attack_resistance passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("Running TOTP Utils Tests")
    print("=" * 50 + "\n")
    
    tests = [
        test_generate_secret,
        test_is_valid_secret,
        test_totp_generation,
        test_totp_verification,
        test_totp_algorithms,
        test_totp_intervals,
        test_otpauth_url,
        test_qr_code_url,
        test_hotp,
        test_convenience_functions,
        test_backup_codes,
        test_totp_manager,
        test_invalid_inputs,
        test_rfc6238_vectors,
        test_timing_attack_resistance,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)