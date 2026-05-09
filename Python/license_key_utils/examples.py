"""
License Key Utilities - Examples
=================================

This file demonstrates how to use the license key utilities library.

Features:
- Generate different license types
- Validate license keys
- Manage licenses
- Export/import licenses
- Hardware binding

Author: AllToolkit
"""

from datetime import datetime
from license_key_utils import (
    LicenseKeyGenerator,
    LicenseManager,
    LicenseType,
    LicenseStatus,
    generate_trial_license,
    quick_validate
)


def example_basic_usage():
    """Basic license generation and validation."""
    print("\n" + "="*60)
    print("Example 1: Basic License Generation")
    print("="*60)
    
    # Create a license generator
    generator = LicenseKeyGenerator()
    
    # Generate a standard license
    key, info = generator.generate_license(
        license_type=LicenseType.STANDARD,
        product_name="MyAwesomeApp",
        customer_name="John Doe",
        customer_email="john@example.com"
    )
    
    print(f"\nGenerated License Key: {key}")
    print(f"License ID: {info.license_id}")
    print(f"Type: {info.license_type.value}")
    print(f"Product: {info.product_name}")
    print(f"Customer: {info.customer_name} ({info.customer_email})")
    print(f"Perpetual: {info.expires_at is None}")
    
    # Validate the key
    status = generator.validate_key(key)
    print(f"\nValidation Status: {status.value}")
    
    return key


def example_trial_license():
    """Trial license with expiration."""
    print("\n" + "="*60)
    print("Example 2: Trial License with Expiration")
    print("="*60)
    
    generator = LicenseKeyGenerator()
    
    # Generate a 14-day trial license
    key, info = generator.generate_license(
        license_type=LicenseType.TRIAL,
        product_name="MyAwesomeApp",
        customer_name="Trial User",
        customer_email="trial@example.com",
        validity_days=14
    )
    
    print(f"\nTrial License Key: {key}")
    print(f"Days Remaining: {info.days_remaining()}")
    print(f"Expires At: {info.expires_at}")
    print(f"Is Expired: {info.is_expired()}")
    
    return key


def example_enterprise_license():
    """Enterprise license with features and hardware binding."""
    print("\n" + "="*60)
    print("Example 3: Enterprise License with Features")
    print("="*60)
    
    generator = LicenseKeyGenerator()
    
    # Generate hardware ID
    hwid = LicenseKeyGenerator.generate_hardware_id()
    print(f"\nHardware ID: {hwid}")
    
    # Define licensed features
    features = {
        "reporting",
        "api_access",
        "sso",
        "audit_log",
        "custom_integrations",
        "priority_support"
    }
    
    # Generate enterprise license
    key, info = generator.generate_license(
        license_type=LicenseType.ENTERPRISE,
        product_name="EnterpriseSuite",
        customer_name="Big Corporation Inc.",
        customer_email="license@bigcorp.com",
        validity_days=365,
        features=features,
        hardware_id=hwid,
        max_users=500
    )
    
    print(f"\nEnterprise License Key: {key}")
    print(f"Max Users: {info.max_users}")
    print(f"Licensed Features: {len(features)}")
    
    # Check specific features
    print("\nFeature Checks:")
    for feature in ["reporting", "sso", "advanced_analytics"]:
        has_feature = info.has_feature(feature)
        status = "✓" if has_feature else "✗"
        print(f"  {status} {feature}: {'Available' if has_feature else 'Not Licensed'}")
    
    return key


def example_license_manager():
    """Using the license manager for complete license lifecycle."""
    print("\n" + "="*60)
    print("Example 4: License Manager")
    print("="*60)
    
    manager = LicenseManager()
    
    # Create multiple licenses
    print("\nCreating licenses...")
    
    # Trial license
    trial_key, trial_info = manager.create_license(
        license_type=LicenseType.TRIAL,
        product_name="MyApp",
        customer_name="Trial User",
        customer_email="trial@example.com",
        validity_days=14,
        features={"basic"}
    )
    print(f"  Trial: {trial_key}")
    
    # Professional license
    pro_key, pro_info = manager.create_license(
        license_type=LicenseType.PROFESSIONAL,
        product_name="MyApp",
        customer_name="Pro User",
        customer_email="pro@example.com",
        validity_days=365,
        features={"basic", "advanced", "api_access"}
    )
    print(f"  Professional: {pro_key}")
    
    # Enterprise license
    ent_key, ent_info = manager.create_license(
        license_type=LicenseType.ENTERPRISE,
        product_name="MyApp",
        customer_name="Enterprise Corp",
        customer_email="ent@corp.com",
        validity_days=365,
        features={"basic", "advanced", "api_access", "sso", "audit"},
        max_users=100
    )
    print(f"  Enterprise: {ent_key}")
    
    # List all licenses
    print("\nAll Licenses:")
    all_licenses = manager.list_licenses()
    for lic in all_licenses:
        exp = lic.days_remaining()
        exp_str = f"{exp} days" if exp else "perpetual"
        print(f"  - {lic.license_id}: {lic.license_type.value} ({exp_str})")
    
    # Validate a license
    print(f"\nValidating Professional License...")
    status, validated = manager.validate_license(
        pro_key,
        required_features={"basic", "advanced"}
    )
    print(f"  Status: {status.value}")
    print(f"  Features match: {validated.features >= {'basic', 'advanced'}}")
    
    return manager


def example_export_import():
    """Export and import licenses."""
    print("\n" + "="*60)
    print("Example 5: Export/Import Licenses")
    print("="*60)
    
    manager = LicenseManager()
    
    # Create a license
    key, info = manager.create_license(
        license_type=LicenseType.PROFESSIONAL,
        product_name="ExportApp",
        customer_name="Export User",
        customer_email="export@example.com",
        validity_days=90,
        features={"feature_a", "feature_b"}
    )
    
    # Export the license
    exported = manager.export_license(info.license_id)
    print(f"\nExported License String:")
    print(f"  {exported[:50]}...")
    print(f"  Length: {len(exported)} chars")
    
    # Import into new manager
    new_manager = LicenseManager()
    imported = new_manager.import_license(exported)
    
    print(f"\nImported License:")
    print(f"  License ID: {imported.license_id}")
    print(f"  Type: {imported.license_type.value}")
    print(f"  Customer: {imported.customer_name}")
    print(f"  Features: {imported.features}")
    
    return exported


def example_validation_scenarios():
    """Various validation scenarios."""
    print("\n" + "="*60)
    print("Example 6: Validation Scenarios")
    print("="*60)
    
    generator = LicenseKeyGenerator()
    
    # Valid key
    print("\nScenario 1: Valid Key")
    key, _ = generator.generate_license(
        license_type=LicenseType.STANDARD,
        product_name="TestApp",
        customer_name="Test",
        customer_email="test@example.com"
    )
    status = quick_validate(key)
    print(f"  Key: {key}")
    print(f"  Status: {status.value}")
    
    # Invalid format
    print("\nScenario 2: Invalid Format")
    invalid_keys = ["INVALID", "XXXX-XXXX", "T-123-4567-890A-BCDE"]
    for k in invalid_keys:
        status = quick_validate(k)
        print(f"  Key: {k}")
        print(f"  Status: {status.value}")
    
    # Feature check
    print("\nScenario 3: Feature Requirement Check")
    manager = LicenseManager()
    key, info = manager.create_license(
        license_type=LicenseType.PROFESSIONAL,
        product_name="FeatureApp",
        customer_name="User",
        customer_email="user@example.com",
        features={"basic", "advanced"}
    )
    
    # Check with allowed feature
    status, _ = manager.validate_license(key, required_features={"basic"})
    print(f"  Required: basic → Status: {status.value}")
    
    # Check with missing feature
    status, _ = manager.validate_license(key, required_features={"premium"})
    print(f"  Required: premium → Status: {status.value}")


def example_convenience_functions():
    """Using convenience functions."""
    print("\n" + "="*60)
    print("Example 7: Convenience Functions")
    print("="*60)
    
    # Quick trial license
    key, info = generate_trial_license(
        product_name="QuickTrial",
        customer_email="quick@example.com",
        validity_days=7,
        features={"basic_trial"}
    )
    
    print(f"\nTrial License (Convenience Function):")
    print(f"  Key: {key}")
    print(f"  Days: {info.days_remaining()}")
    print(f"  Features: {info.features}")
    
    # Quick validation
    status = quick_validate(key)
    print(f"  Quick Validate: {status.value}")


def main():
    """Run all examples."""
    print("\n" + "#"*60)
    print("#  License Key Utilities - Examples")
    print("#"*60)
    
    example_basic_usage()
    example_trial_license()
    example_enterprise_license()
    example_license_manager()
    example_export_import()
    example_validation_scenarios()
    example_convenience_functions()
    
    print("\n" + "#"*60)
    print("#  All examples completed!")
    print("#"*60 + "\n")


if __name__ == "__main__":
    main()