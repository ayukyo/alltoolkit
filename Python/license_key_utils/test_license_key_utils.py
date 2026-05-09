"""
Tests for License Key Utilities
================================

Run with: python test_license_key_utils.py
"""

import sys
from datetime import datetime, timedelta

sys.path.insert(0, '.')

from license_key_utils import (
    LicenseKeyGenerator,
    LicenseManager,
    LicenseType,
    LicenseStatus,
    LicenseInfo,
    generate_trial_license,
    quick_validate
)


def test_license_generation():
    """Test license key generation."""
    print("\nTest: License Generation")
    print("-" * 40)
    
    generator = LicenseKeyGenerator()
    
    # Test standard license
    key, info = generator.generate_license(
        license_type=LicenseType.STANDARD,
        product_name="TestApp",
        customer_name="John Doe",
        customer_email="john@example.com"
    )
    
    assert key is not None
    assert len(key) == 21  # TYPE-XXXX-XXXX-XXXX-XXXX (1+1+4+1+4+1+4+1+4 = 21)
    assert key.count('-') == 4
    assert info.license_type == LicenseType.STANDARD
    print(f"✓ Standard license: {key}")
    
    # Test trial license with expiration
    key2, info2 = generator.generate_license(
        license_type=LicenseType.TRIAL,
        product_name="TestApp",
        customer_name="Trial",
        customer_email="trial@example.com",
        validity_days=14
    )
    
    assert info2.expires_at is not None
    assert info2.days_remaining() <= 14
    print(f"✓ Trial license: {key2}")
    
    # Test enterprise license with features
    features = {"reporting", "api_access", "sso"}
    key3, info3 = generator.generate_license(
        license_type=LicenseType.ENTERPRISE,
        product_name="EnterpriseApp",
        customer_name="Big Corp",
        customer_email="corp@big.com",
        validity_days=365,
        features=features,
        max_users=100
    )
    
    assert info3.license_type == LicenseType.ENTERPRISE
    assert info3.features == features
    assert info3.max_users == 100
    assert info3.has_feature("reporting")
    assert not info3.has_feature("nonexistent")
    print(f"✓ Enterprise license: {key3}")
    
    return True


def test_key_format():
    """Test key format."""
    print("\nTest: Key Format")
    print("-" * 40)
    
    generator = LicenseKeyGenerator()
    
    # All license types should produce valid format
    for ltype in [LicenseType.TRIAL, LicenseType.STANDARD, LicenseType.PROFESSIONAL, LicenseType.ENTERPRISE]:
        key, _ = generator.generate_license(
            license_type=ltype,
            product_name="Test",
            customer_name="Test",
            customer_email="test@example.com"
        )
        
        # Check format
        assert generator.KEY_PATTERN.match(key)
        assert key[0] == generator.TYPE_PREFIXES[ltype]
        print(f"✓ {ltype.value} key: {key}")
    
    return True


def test_key_validation():
    """Test key validation."""
    print("\nTest: Key Validation")
    print("-" * 40)
    
    generator = LicenseKeyGenerator()
    
    # Valid keys
    for ltype in LicenseType:
        key, _ = generator.generate_license(
            license_type=ltype,
            product_name="Test",
            customer_name="Test",
            customer_email="test@example.com"
        )
        status = generator.validate_key(key)
        assert status == LicenseStatus.VALID
        print(f"✓ {ltype.value} key is valid")
    
    # Invalid keys (wrong format, not content)
    invalid_keys = ["INVALID", "X-1234-5678-90AB-CDEF", "T-123-4567-890A-BCDE", "TYPE-XXXX-XXXX-XXXX-XXXX"]
    for k in invalid_keys:
        status = generator.validate_key(k)
        assert status == LicenseStatus.INVALID_FORMAT
    print("✓ Invalid format detection works")
    
    return True


def test_key_uniqueness():
    """Test that generated keys are unique."""
    print("\nTest: Key Uniqueness")
    print("-" * 40)
    
    generator = LicenseKeyGenerator()
    keys = set()
    
    for _ in range(100):
        key, _ = generator.generate_license(
            license_type=LicenseType.STANDARD,
            product_name="Test",
            customer_name="Test",
            customer_email="test@example.com"
        )
        assert key not in keys
        keys.add(key)
    
    print(f"✓ Generated 100 unique keys")
    return True


def test_hardware_id():
    """Test hardware ID generation."""
    print("\nTest: Hardware ID")
    print("-" * 40)
    
    hwid = LicenseKeyGenerator.generate_hardware_id()
    assert hwid.startswith("HWID-")
    assert len(hwid) == 21  # HWID-XXXXXXXXXXXXXXXX
    print(f"✓ Hardware ID: {hwid}")
    
    # Generate license with hardware binding
    generator = LicenseKeyGenerator()
    key, info = generator.generate_license(
        license_type=LicenseType.PROFESSIONAL,
        product_name="HWApp",
        customer_name="HW User",
        customer_email="hw@example.com",
        hardware_id=hwid
    )
    
    assert info.hardware_id == hwid
    print(f"✓ Hardware-bound license: {key}")
    return True


def test_license_manager():
    """Test license manager operations."""
    print("\nTest: License Manager")
    print("-" * 40)
    
    manager = LicenseManager()
    
    # Create licenses
    key1, info1 = manager.create_license(
        license_type=LicenseType.TRIAL,
        product_name="App",
        customer_name="User1",
        customer_email="user1@example.com",
        validity_days=14
    )
    print(f"✓ Created trial: {key1}")
    
    key2, info2 = manager.create_license(
        license_type=LicenseType.STANDARD,
        product_name="App",
        customer_name="User2",
        customer_email="user2@example.com"
    )
    print(f"✓ Created standard: {key2}")
    
    # Validate licenses
    status1, validated1 = manager.validate_license(key1)
    assert status1 == LicenseStatus.VALID
    print("✓ Trial license validated")
    
    status2, validated2 = manager.validate_license(key2)
    assert status2 == LicenseStatus.VALID
    print("✓ Standard license validated")
    
    # Get license
    retrieved = manager.get_license(info1.license_id)
    assert retrieved is not None
    assert retrieved.license_id == info1.license_id
    print("✓ Get license by ID works")
    
    # List licenses
    all_licenses = manager.list_licenses()
    assert len(all_licenses) == 2
    print(f"✓ List licenses: {len(all_licenses)} found")
    
    # Revoke license
    assert manager.revoke_license(info1.license_id) is True
    assert manager.get_license(info1.license_id) is None
    print("✓ License revocation works")
    
    return True


def test_export_import():
    """Test license export and import."""
    print("\nTest: Export/Import")
    print("-" * 40)
    
    manager = LicenseManager()
    
    # Create license
    key, info = manager.create_license(
        license_type=LicenseType.PROFESSIONAL,
        product_name="ExportApp",
        customer_name="Export User",
        customer_email="export@example.com",
        validity_days=90,
        features={"export", "import"}
    )
    
    # Export
    exported = manager.export_license(info.license_id)
    assert exported is not None
    print(f"✓ Exported license string length: {len(exported)}")
    
    # Import into new manager
    new_manager = LicenseManager()
    imported = new_manager.import_license(exported)
    
    assert imported is not None
    assert imported.license_id == info.license_id
    assert imported.license_type == LicenseType.PROFESSIONAL
    assert imported.features == {"export", "import"}
    print("✓ Import works correctly")
    
    return True


def test_feature_validation():
    """Test feature-based validation."""
    print("\nTest: Feature Validation")
    print("-" * 40)
    
    manager = LicenseManager()
    
    features = {"basic", "advanced"}
    key, info = manager.create_license(
        license_type=LicenseType.PROFESSIONAL,
        product_name="FeatureApp",
        customer_name="User",
        customer_email="user@example.com",
        features=features
    )
    
    # Validate with allowed feature
    status, _ = manager.validate_license(key, required_features={"basic"})
    assert status == LicenseStatus.VALID
    print("✓ Feature 'basic' is licensed")
    
    # Validate with multiple allowed features
    status, _ = manager.validate_license(key, required_features={"basic", "advanced"})
    assert status == LicenseStatus.VALID
    print("✓ Features 'basic' and 'advanced' are licensed")
    
    # Validate with missing feature
    status, _ = manager.validate_license(key, required_features={"premium"})
    assert status == LicenseStatus.FEATURE_NOT_LICENSED
    print("✓ Feature 'premium' is not licensed")
    
    return True


def test_license_info():
    """Test LicenseInfo dataclass."""
    print("\nTest: License Info")
    print("-" * 40)
    
    # Non-expiring license
    info = LicenseInfo(
        license_id="TEST-001",
        license_type=LicenseType.STANDARD,
        product_name="Test",
        customer_name="Test",
        customer_email="test@example.com",
        issued_at=datetime.now(),
        expires_at=None
    )
    assert not info.is_expired()
    assert info.days_remaining() is None
    print("✓ Perpetual license: never expires")
    
    # Expired license
    expired_info = LicenseInfo(
        license_id="TEST-002",
        license_type=LicenseType.TRIAL,
        product_name="Test",
        customer_name="Test",
        customer_email="test@example.com",
        issued_at=datetime.now() - timedelta(days=30),
        expires_at=datetime.now() - timedelta(days=1)
    )
    assert expired_info.is_expired()
    assert expired_info.days_remaining() == 0
    print("✓ Expired license detected")
    
    # Active license with features
    active_info = LicenseInfo(
        license_id="TEST-003",
        license_type=LicenseType.TRIAL,
        product_name="Test",
        customer_name="Test",
        customer_email="test@example.com",
        issued_at=datetime.now(),
        expires_at=datetime.now() + timedelta(days=7),
        features={"feature_a", "feature_b"}
    )
    assert not active_info.is_expired()
    assert active_info.days_remaining() <= 7
    assert active_info.has_feature("feature_a")
    assert not active_info.has_feature("feature_c")
    print("✓ Active license with features")
    
    return True


def test_convenience_functions():
    """Test convenience functions."""
    print("\nTest: Convenience Functions")
    print("-" * 40)
    
    # generate_trial_license
    key, info = generate_trial_license(
        product_name="TrialApp",
        customer_email="trial@example.com",
        validity_days=14,
        features={"basic"}
    )
    
    assert info.license_type == LicenseType.TRIAL
    assert info.product_name == "TrialApp"
    assert info.customer_email == "trial@example.com"
    assert "basic" in info.features
    print(f"✓ Trial license: {key}")
    
    # quick_validate
    status = quick_validate(key)
    assert status == LicenseStatus.VALID
    print("✓ Quick validate works")
    
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("License Key Utilities Test Suite")
    print("="*60)
    
    tests = [
        test_license_generation,
        test_key_format,
        test_key_validation,
        test_key_uniqueness,
        test_hardware_id,
        test_license_manager,
        test_export_import,
        test_feature_validation,
        test_license_info,
        test_convenience_functions,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ FAILED: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ ERROR: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{len(tests)} tests passed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)