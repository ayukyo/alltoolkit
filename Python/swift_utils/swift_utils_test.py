#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - SWIFT/BIC Utilities Test Suite

Comprehensive tests for SWIFT/BIC code validation, parsing, and utilities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swift_utils.mod import (
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
    get_country_info,
    swift_info,
    compare_swift,
    generate_test_swift,
    get_all_countries,
    get_sepa_countries,
    country_code_to_name,
    ISO_COUNTRIES,
    SEPA_COUNTRIES,
)


def test_is_valid_swift():
    """Test basic validation."""
    # Valid 8-character codes
    assert is_valid_swift('DEUTDEFF') == True
    assert is_valid_swift('CHASUS33') == True
    assert is_valid_swift('BARCGB22') == True
    
    # Valid 11-character codes
    assert is_valid_swift('DEUTDEFFXXX') == True
    assert is_valid_swift('CHASUS33XXX') == True
    
    # Case insensitive
    assert is_valid_swift('deutdeff') == True
    assert is_valid_swift('DeUtDeFf') == True
    
    # Invalid codes
    assert is_valid_swift('INVALID') == False  # Wrong length
    assert is_valid_swift('DEUT') == False     # Too short
    assert is_valid_swift('DEUTDEFF12345') == False  # Too long
    assert is_valid_swift('1234DEFF') == False  # Numbers in bank code
    assert is_valid_swift('DEUT12FF') == False  # Numbers in country code
    assert is_valid_swift('DEUTXXFF') == False  # Invalid country code
    assert is_valid_swift('') == False         # Empty
    assert is_valid_swift(None) == False        # None
    
    print("✓ test_is_valid_swift passed")


def test_validate_swift():
    """Test detailed validation."""
    # Valid code
    result = validate_swift('DEUTDEFFXXX')
    assert result.is_valid == True
    assert result.normalized == 'DEUTDEFFXXX'
    assert result.error is None
    assert result.components is not None
    assert result.components.bank_code == 'DEUT'
    assert result.components.country_code == 'DE'
    assert result.components.country_name == 'Germany'
    
    # Invalid code
    result = validate_swift('INVALID')
    assert result.is_valid == False
    assert result.error is not None
    
    # Invalid country
    result = validate_swift('DEUTXXFF')
    assert result.is_valid == False
    assert 'country' in result.error.lower()
    
    print("✓ test_validate_swift passed")


def test_parse_swift():
    """Test parsing components."""
    comp = parse_swift('DEUTDEFF')
    assert comp is not None
    assert comp.bank_code == 'DEUT'
    assert comp.country_code == 'DE'
    assert comp.country_name == 'Germany'
    assert comp.location_code == 'FF'
    assert comp.branch_code is None
    
    # 11-character code
    comp = parse_swift('CHASUS33XXX')
    assert comp is not None
    assert comp.bank_code == 'CHAS'
    assert comp.country_code == 'US'
    assert comp.country_name == 'United States'
    assert comp.location_code == '33'
    assert comp.branch_code == 'XXX'
    
    # Invalid code
    assert parse_swift('INVALID') is None
    
    print("✓ test_parse_swift passed")


def test_getters():
    """Test individual getter functions."""
    assert get_bank_code('DEUTDEFF') == 'DEUT'
    assert get_country_code('DEUTDEFF') == 'DE'
    assert get_country_name('DEUTDEFF') == 'Germany'
    assert get_location_code('DEUTDEFF') == 'FF'
    assert get_branch_code('DEUTDEFF') is None
    assert get_branch_code('DEUTDEFFXXX') == 'XXX'
    
    # Invalid code returns None
    assert get_bank_code('INVALID') is None
    assert get_country_name('INVALID') is None
    
    print("✓ test_getters passed")


def test_normalize_swift():
    """Test normalization."""
    assert normalize_swift('deutdeff') == 'DEUTDEFF'
    assert normalize_swift('DEUT DE FF') == 'DEUTDEFF'
    assert normalize_swift('  DEUTDEFF  ') == 'DEUTDEFF'
    assert normalize_swift('DeUtDeFf') == 'DEUTDEFF'
    assert normalize_swift('INVALID') is None
    assert normalize_swift('') is None
    
    print("✓ test_normalize_swift passed")


def test_format_swift():
    """Test formatting."""
    assert format_swift('DEUTDEFF') == 'DEUT DE FF'
    assert format_swift('DEUTDEFFXXX') == 'DEUT DE FF XXX'
    assert format_swift('DEUTDEFF', '-') == 'DEUT-DE-FF'
    assert format_swift('deutdeff') == 'DEUT DE FF'
    assert format_swift('INVALID') is None
    
    print("✓ test_format_swift passed")


def test_status_flags():
    """Test status flag functions."""
    # Primary office (XXX or omitted)
    assert is_primary_office('DEUTDEFF') == True
    assert is_primary_office('DEUTDEFFXXX') == True
    assert is_primary_office('DEUTDEFF123') == False
    
    # Test code (location code ends with 0)
    assert is_test_code('TESTDE00') == True
    assert is_test_code('TESTDE01') == False
    assert is_test_code('DEUTDEFF') == False
    
    # Passive participant (location code ends with 1)
    assert is_passive_participant('TESTDE11') == True
    assert is_passive_participant('DEUTDEFF') == False
    
    # SWIFT connected
    assert is_swift_connected('DEUTDEFF') == True
    assert is_swift_connected('TESTDE00') == False  # Test code
    
    # Invalid codes return False
    assert is_primary_office('INVALID') == False
    assert is_test_code('INVALID') == False
    
    print("✓ test_status_flags passed")


def test_sepa():
    """Test SEPA country detection."""
    # SEPA countries
    assert is_sepa_country('DEUTDEFF') == True   # Germany
    assert is_sepa_country('BARCGB22') == True    # UK
    assert is_sepa_country('CHASUS33') == False   # US
    
    # Invalid returns False
    assert is_sepa_country('INVALID') == False
    
    print("✓ test_sepa passed")


def test_get_country_info():
    """Test country info retrieval."""
    info = get_country_info('DEUTDEFF')
    assert info is not None
    assert info['code'] == 'DE'
    assert info['name'] == 'Germany'
    assert info['is_sepa'] == True
    
    # US is not in SEPA
    info = get_country_info('CHASUS33')
    assert info['is_sepa'] == False
    
    # Invalid code
    assert get_country_info('INVALID') is None
    
    print("✓ test_get_country_info passed")


def test_swift_info():
    """Test comprehensive info function."""
    info = swift_info('DEUTDEFFXXX')
    assert info['valid'] == True
    assert info['normalized'] == 'DEUTDEFFXXX'
    assert info['formatted'] == 'DEUT DE FF XXX'
    assert info['bank_code'] == 'DEUT'
    assert info['country_code'] == 'DE'
    assert info['country_name'] == 'Germany'
    assert info['location_code'] == 'FF'
    assert info['branch_code'] == 'XXX'
    assert info['is_primary_office'] == True
    assert info['is_sepa_country'] == True
    assert info['length'] == 11
    
    # Invalid code
    info = swift_info('INVALID')
    assert info['valid'] == False
    assert info['error'] is not None
    
    print("✓ test_swift_info passed")


def test_compare_swift():
    """Test comparison function."""
    # Same bank, different branch code format
    result = compare_swift('DEUTDEFF', 'DEUTDEFFXXX')
    assert result['same_bank'] == True
    assert result['same_country'] == True
    assert result['same_location'] == True
    assert result['same_branch'] == False  # None vs 'XXX' are different
    assert result['same_institution'] == True
    
    # Different banks
    result = compare_swift('DEUTDEFF', 'CHASUS33')
    assert result['same_bank'] == False
    assert result['same_country'] == False
    assert result['same_institution'] == False
    
    # Same bank, different location
    result = compare_swift('DEUTDEFF', 'DEUTDEMM')
    assert result['same_bank'] == True
    assert result['same_country'] == True
    assert result['same_location'] == False
    
    # Invalid codes
    result = compare_swift('DEUTDEFF', 'INVALID')
    assert 'error' in result
    assert result['code1_valid'] == True
    assert result['code2_valid'] == False
    
    print("✓ test_compare_swift passed")


def test_generate_test_swift():
    """Test test code generation."""
    code = generate_test_swift('DE')
    assert code == 'TESTDE00'
    assert is_valid_swift(code) == True
    assert is_test_code(code) == True
    
    # Custom bank code
    code = generate_test_swift('US', 'JPMO')
    assert code == 'JPMOUS00'
    
    # Invalid country
    assert generate_test_swift('XX') is None
    
    # Bank code padding
    code = generate_test_swift('DE', 'AB')
    assert code == 'ABXXDE00'
    
    print("✓ test_generate_test_swift passed")


def test_country_utilities():
    """Test country code utilities."""
    # Get all countries
    countries = get_all_countries()
    assert isinstance(countries, dict)
    assert len(countries) > 200
    assert countries['US'] == 'United States'
    assert countries['DE'] == 'Germany'
    assert countries['GB'] == 'United Kingdom'
    
    # Get SEPA countries
    sepa = get_sepa_countries()
    assert isinstance(sepa, set)
    assert 'DE' in sepa
    assert 'FR' in sepa
    assert 'US' not in sepa
    
    # Country code to name
    assert country_code_to_name('US') == 'United States'
    assert country_code_to_name('DE') == 'Germany'
    assert country_code_to_name('XX') is None
    
    print("✓ test_country_utilities passed")


def test_real_world_codes():
    """Test with real-world SWIFT codes."""
    real_codes = [
        ('DEUTDEFF', 'DE', 'Germany', 'DEUT', True),       # Deutsche Bank
        ('CHASUS33', 'US', 'United States', 'CHAS', False), # JP Morgan Chase
        ('BARCGB22', 'GB', 'United Kingdom', 'BARC', True), # Barclays
        ('HSBCHKHH', 'HK', 'Hong Kong', 'HSBC', False),     # HSBC Hong Kong
        ('SBININBB', 'IN', 'India', 'SBIN', False),         # State Bank of India (NOT SEPA)
        ('BOFAUS3N', 'US', 'United States', 'BOFA', False), # Bank of America
        ('CITIUS33', 'US', 'United States', 'CITI', False), # Citibank
        ('UBSWCHZH80A', 'CH', 'Switzerland', 'UBSW', True), # UBS Switzerland (SEPA)
    ]
    
    for code, country, country_name, bank, is_sepa in real_codes:
        comp = parse_swift(code)
        assert comp is not None, f"Failed to parse {code}"
        assert comp.country_code == country, f"Country code mismatch for {code}"
        assert comp.country_name == country_name, f"Country name mismatch for {code}"
        assert comp.bank_code == bank, f"Bank code mismatch for {code}"
        assert comp.is_sepa_country == is_sepa, f"SEPA mismatch for {code}"
    
    print("✓ test_real_world_codes passed")


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    # Whitespace handling
    assert is_valid_swift('  DEUTDEFF  ') == True
    assert normalize_swift('DEUT DE FF') == 'DEUTDEFF'
    
    # Mixed case
    assert normalize_swift('DeUtDeFf') == 'DEUTDEFF'
    
    # Numbers in location and branch codes (valid)
    assert is_valid_swift('CHASUS33') == True
    assert is_valid_swift('CHASUS33123') == True
    
    # All numeric branch code
    assert is_valid_swift('CHASUS33001') == True
    
    # Test code generation
    test_code = generate_test_swift('FR')
    assert test_code == 'TESTFR00'
    assert is_test_code(test_code) == True
    
    # Passive participant
    passive_code = 'TESTFR11'
    assert is_passive_participant(passive_code) == True
    
    print("✓ test_edge_cases passed")


def run_all_tests():
    """Run all test functions."""
    print("=" * 60)
    print("SWIFT/BIC Utilities Test Suite")
    print("=" * 60)
    print()
    
    test_is_valid_swift()
    test_validate_swift()
    test_parse_swift()
    test_getters()
    test_normalize_swift()
    test_format_swift()
    test_status_flags()
    test_sepa()
    test_get_country_info()
    test_swift_info()
    test_compare_swift()
    test_generate_test_swift()
    test_country_utilities()
    test_real_world_codes()
    test_edge_cases()
    
    print()
    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()