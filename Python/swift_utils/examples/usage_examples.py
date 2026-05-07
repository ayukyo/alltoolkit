#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - SWIFT/BIC Utilities Usage Examples

Practical examples demonstrating SWIFT/BIC code validation and usage.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    is_valid_swift,
    validate_swift,
    parse_swift,
    get_bank_code,
    get_country_code,
    get_country_name,
    get_location_code,
    get_branch_code,
    normalize_swift,
    format_swift,
    is_primary_office,
    is_test_code,
    is_passive_participant,
    is_swift_connected,
    is_sepa_country,
    swift_info,
    compare_swift,
    generate_test_swift,
    get_all_countries,
    get_sepa_countries,
    country_code_to_name,
)


def example_basic_validation():
    """Basic SWIFT code validation."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Validation")
    print("=" * 60)
    
    codes = [
        'DEUTDEFF',      # Deutsche Bank Frankfurt
        'CHASUS33',      # JP Morgan Chase US
        'BARCGB22',      # Barclays UK
        'INVALID',       # Invalid code
    ]
    
    for code in codes:
        valid = is_valid_swift(code)
        print(f"  {code}: {'✓ Valid' if valid else '✗ Invalid'}")


def example_detailed_validation():
    """Detailed validation with error messages."""
    print("\n" + "=" * 60)
    print("Example 2: Detailed Validation")
    print("=" * 60)
    
    codes = ['DEUTDEFF', 'DEUTDEFFXXX', 'DEUTXXFF', '1234DEFF']
    
    for code in codes:
        result = validate_swift(code)
        print(f"\n  Code: {code}")
        print(f"  Valid: {result.is_valid}")
        if result.is_valid:
            print(f"  Normalized: {result.normalized}")
        else:
            print(f"  Error: {result.error}")


def example_parse_components():
    """Parse and display SWIFT code components."""
    print("\n" + "=" * 60)
    print("Example 3: Parse Components")
    print("=" * 60)
    
    code = 'DEUTDEFFXXX'
    comp = parse_swift(code)
    
    print(f"\n  Code: {code}")
    print(f"  Bank Code: {comp.bank_code}")
    print(f"  Country Code: {comp.country_code}")
    print(f"  Country Name: {comp.country_name}")
    print(f"  Location Code: {comp.location_code}")
    print(f"  Branch Code: {comp.branch_code}")
    print(f"  Primary Office: {comp.is_primary_office}")
    print(f"  Test Code: {comp.is_test_code}")
    print(f"  Passive: {comp.is_passive}")
    print(f"  SWIFT Connected: {comp.is_connected}")
    print(f"  SEPA Country: {comp.is_sepa_country}")


def example_quick_accessors():
    """Quick accessor functions for specific components."""
    print("\n" + "=" * 60)
    print("Example 4: Quick Accessors")
    print("=" * 60)
    
    code = 'CHASUS33'
    
    print(f"\n  Code: {code}")
    print(f"  Bank: {get_bank_code(code)}")
    print(f"  Country: {get_country_code(code)} ({get_country_name(code)})")
    print(f"  Location: {get_location_code(code)}")
    print(f"  Branch: {get_branch_code(code) or 'N/A'}")


def example_normalization():
    """Normalize and format SWIFT codes."""
    print("\n" + "=" * 60)
    print("Example 5: Normalization & Formatting")
    print("=" * 60)
    
    raw_codes = [
        'deutdeff',       # lowercase
        'DEUT DE FF',     # with spaces
        '  DEUTDEFF  ',   # with whitespace
        'DEUTDEFFXXX',    # 11 character
    ]
    
    print("\n  Normalization:")
    for code in raw_codes:
        normalized = normalize_swift(code)
        print(f"    '{code}' -> '{normalized}'")
    
    print("\n  Formatting:")
    for code in ['DEUTDEFF', 'DEUTDEFFXXX', 'CHASUS33']:
        formatted = format_swift(code)
        dashed = format_swift(code, '-')
        print(f"    {code} -> '{formatted}' or '{dashed}'")


def example_status_checks():
    """Check various status flags."""
    print("\n" + "=" * 60)
    print("Example 6: Status Checks")
    print("=" * 60)
    
    codes = [
        ('DEUTDEFF', 'Normal active code'),
        ('DEUTDEFFXXX', 'Primary office'),
        ('TESTDE00', 'Test code'),
        ('TESTFR11', 'Passive participant'),
    ]
    
    print("\n  Status Analysis:")
    for code, description in codes:
        print(f"\n    {code} ({description}):")
        print(f"      Primary Office: {is_primary_office(code)}")
        print(f"      Test Code: {is_test_code(code)}")
        print(f"      Passive: {is_passive_participant(code)}")
        print(f"      Connected: {is_swift_connected(code)}")


def example_sepa_check():
    """Check SEPA eligibility."""
    print("\n" + "=" * 60)
    print("Example 7: SEPA Country Check")
    print("=" * 60)
    
    codes = [
        ('DEUTDEFF', 'Germany'),
        ('BARCGB22', 'UK'),
        ('CHASUS33', 'US'),
        ('SBININBB', 'India'),
        ('HSBCHKHH', 'Hong Kong'),
    ]
    
    print("\n  SEPA Membership:")
    for code, country in codes:
        sepa = is_sepa_country(code)
        status = '✓ Yes' if sepa else '✗ No'
        print(f"    {code} ({country}): {status}")
    
    print("\n  All SEPA Countries:")
    sepa_countries = get_sepa_countries()
    print(f"    Count: {len(sepa_countries)}")
    print(f"    Countries: {', '.join(sorted(sepa_countries)[:10])}...")


def example_comprehensive_info():
    """Get comprehensive SWIFT code information."""
    print("\n" + "=" * 60)
    print("Example 8: Comprehensive Info")
    print("=" * 60)
    
    code = 'UBSWCHZH80A'
    info = swift_info(code)
    
    print(f"\n  Full Info for {code}:")
    for key, value in info.items():
        print(f"    {key}: {value}")


def example_comparison():
    """Compare two SWIFT codes."""
    print("\n" + "=" * 60)
    print("Example 9: Code Comparison")
    print("=" * 60)
    
    comparisons = [
        ('DEUTDEFF', 'DEUTDEFFXXX'),
        ('DEUTDEFF', 'DEUTDEMM'),
        ('DEUTDEFF', 'CHASUS33'),
    ]
    
    for code1, code2 in comparisons:
        result = compare_swift(code1, code2)
        print(f"\n  Comparing {code1} vs {code2}:")
        print(f"    Same Bank: {result['same_bank']}")
        print(f"    Same Country: {result['same_country']}")
        print(f"    Same Location: {result['same_location']}")
        print(f"    Same Branch: {result['same_branch']}")
        print(f"    Same Institution: {result['same_institution']}")


def example_test_generation():
    """Generate test SWIFT codes."""
    print("\n" + "=" * 60)
    print("Example 10: Test Code Generation")
    print("=" * 60)
    
    print("\n  Generating test codes:")
    for country in ['DE', 'US', 'GB', 'FR', 'JP']:
        test_code = generate_test_swift(country)
        print(f"    {country}: {test_code} (is_test={is_test_code(test_code)})")
    
    print("\n  Custom bank code:")
    test_code = generate_test_swift('DE', 'MYBK')
    print(f"    MYBK + DE: {test_code}")


def example_country_utilities():
    """Country code utilities."""
    print("\n" + "=" * 60)
    print("Example 11: Country Utilities")
    print("=" * 60)
    
    print("\n  Country Code to Name:")
    codes = ['US', 'DE', 'GB', 'FR', 'JP', 'CN', 'AU', 'BR']
    for code in codes:
        name = country_code_to_name(code)
        print(f"    {code}: {name}")
    
    print("\n  Total countries supported: {len(get_all_countries())}")


def example_practical_use():
    """Practical use case: Bank transfer validation."""
    print("\n" + "=" * 60)
    print("Example 12: Practical Use - Bank Transfer")
    print("=" * 60)
    
    def validate_bank_transfer(sender_swift, receiver_swift):
        """Validate SWIFT codes for a bank transfer."""
        print(f"\n  Sender: {sender_swift}")
        sender_result = validate_swift(sender_swift)
        if not sender_result.is_valid:
            print(f"    ✗ Invalid: {sender_result.error}")
            return False
        print(f"    ✓ Valid - {sender_result.components.country_name}")
        
        print(f"\n  Receiver: {receiver_swift}")
        receiver_result = validate_swift(receiver_swift)
        if not receiver_result.is_valid:
            print(f"    ✗ Invalid: {receiver_result.error}")
            return False
        print(f"    ✓ Valid - {receiver_result.components.country_name}")
        
        # Check SEPA eligibility
        sender_sepa = is_sepa_country(sender_swift)
        receiver_sepa = is_sepa_country(receiver_swift)
        
        print(f"\n  SEPA Check:")
        print(f"    Sender SEPA: {'✓' if sender_sepa else '✗'}")
        print(f"    Receiver SEPA: {'✓' if receiver_sepa else '✗'}")
        
        if sender_sepa and receiver_sepa:
            print(f"    ✓ Both banks are in SEPA - Can use SEPA transfer")
        else:
            print(f"    ✗ International transfer required")
        
        # Compare institutions
        comp = compare_swift(sender_swift, receiver_swift)
        if comp['same_institution']:
            print(f"    Note: Same institution - Internal transfer possible")
        
        return True
    
    # Example transfers
    validate_bank_transfer('DEUTDEFF', 'BARCGB22')
    print("\n" + "-" * 40)
    validate_bank_transfer('CHASUS33', 'SBININBB')


def run_all_examples():
    """Run all example functions."""
    print("\n" + "=" * 60)
    print("SWIFT/BIC Utilities - Usage Examples")
    print("=" * 60)
    
    example_basic_validation()
    example_detailed_validation()
    example_parse_components()
    example_quick_accessors()
    example_normalization()
    example_status_checks()
    example_sepa_check()
    example_comprehensive_info()
    example_comparison()
    example_test_generation()
    example_country_utilities()
    example_practical_use()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()