"""
Tests for IBAN Utilities
========================

Comprehensive tests for IBAN validation, parsing, and formatting.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    validate,
    validate_check_digits,
    strip_formatting,
    calculate_check_digits,
    parse,
    format_iban,
    get_country_info,
    get_supported_countries,
    generate_test_iban,
    generate_batch_test_ibans,
    extract_bank_info,
    IBANValidator,
    TEST_IBANS,
    IBAN_STRUCTURES,
)


def test_strip_formatting():
    """Test IBAN formatting removal."""
    assert strip_formatting("GB82 WEST 1234 5698 7654 32") == "GB82WEST12345698765432"
    assert strip_formatting("DE89-3704-0044-0532-0130-00") == "DE89370400440532013000"
    assert strip_formatting("  FR14 2004 1010 0505 0001 3M02 606  ") == "FR1420041010050500013M02606"
    assert strip_formatting("gb82west12345698765432") == "GB82WEST12345698765432"
    print("✓ test_strip_formatting passed")


def test_validate_check_digits():
    """Test MOD-97 check digit validation."""
    # Valid IBANs
    assert validate_check_digits("GB82WEST12345698765432") == True
    assert validate_check_digits("DE89370400440532013000") == True
    assert validate_check_digits("FR1420041010050500013M02606") == True
    
    # Invalid check digits
    assert validate_check_digits("GB82WEST12345698765433") == False
    assert validate_check_digits("DE89370400440532013001") == False
    
    print("✓ test_validate_check_digits passed")


def test_validate():
    """Test complete IBAN validation."""
    # Test all valid IBANs from TEST_IBANS
    for country, iban in TEST_IBANS.items():
        assert validate(iban) == True, f"Failed for {country}: {iban}"
    
    # Invalid IBANs
    assert validate("GB82WEST12345698765433") == False  # Wrong check digit
    assert validate("XX12345678") == False  # Invalid country
    assert validate("") == False  # Empty
    assert validate("GB82") == False  # Too short
    assert validate("GB8212345678") == False  # Wrong length for GB
    
    print("✓ test_validate passed")


def test_calculate_check_digits():
    """Test check digit calculation."""
    # GB IBAN
    check = calculate_check_digits("GB", "WEST12345698765432")
    assert check == "82", f"Expected '82', got '{check}'"
    
    # DE IBAN
    check = calculate_check_digits("DE", "370400440532013000")
    assert check == "89", f"Expected '89', got '{check}'"
    
    # FR IBAN
    check = calculate_check_digits("FR", "20041010050500013M02606")
    assert check == "14", f"Expected '14', got '{check}'"
    
    print("✓ test_calculate_check_digits passed")


def test_parse():
    """Test IBAN parsing."""
    # German IBAN
    parsed = parse("DE89370400440532013000")
    assert parsed['country_code'] == "DE"
    assert parsed['check_digits'] == "89"
    assert parsed['bban'] == "370400440532013000"
    assert parsed['country_name'] == "Germany"
    assert parsed['is_valid'] == True
    
    # UK IBAN
    parsed = parse("GB82WEST12345698765432")
    assert parsed['country_code'] == "GB"
    assert parsed['check_digits'] == "82"
    assert parsed['bban'] == "WEST12345698765432"
    assert parsed['country_name'] == "United Kingdom"
    assert parsed['is_valid'] == True
    
    # Invalid IBAN
    parsed = parse("XX123")
    assert parsed['country_code'] == ""
    assert parsed['is_valid'] == False
    
    print("✓ test_parse passed")


def test_format_iban():
    """Test IBAN formatting."""
    assert format_iban("GB82WEST12345698765432") == "GB82 WEST 1234 5698 7654 32"
    assert format_iban("DE89370400440532013000", separator="-") == "DE89-3704-0044-0532-0130-00"
    assert format_iban("FR1420041010050500013M02606", group_size=4) == "FR14 2004 1010 0505 0001 3M02 606"
    assert format_iban("") == ""
    
    print("✓ test_format_iban passed")


def test_get_country_info():
    """Test country IBAN info retrieval."""
    # Germany
    info = get_country_info("DE")
    assert info['country_code'] == "DE"
    assert info['country_name'] == "Germany"
    assert info['iban_length'] == 22
    
    # Unknown country
    info = get_country_info("XX")
    assert info['country_code'] == "XX"
    assert info['country_name'] == "Unknown"
    assert info['iban_length'] == 0
    
    print("✓ test_get_country_info passed")


def test_get_supported_countries():
    """Test supported countries list."""
    countries = get_supported_countries()
    assert len(countries) > 50, f"Expected >50 countries, got {len(countries)}"
    assert "GB" in countries
    assert "DE" in countries
    assert "FR" in countries
    assert "US" not in countries  # US doesn't use IBAN
    
    # Check list is sorted
    assert countries == sorted(countries)
    
    print("✓ test_get_supported_countries passed")


def test_generate_test_iban():
    """Test IBAN generation."""
    # Generate IBANs for various countries
    for country in ["DE", "GB", "FR", "IT", "ES", "NL", "BE"]:
        iban = generate_test_iban(country)
        assert validate(iban) == True, f"Generated invalid IBAN for {country}: {iban}"
        assert iban.startswith(country), f"IBAN doesn't start with {country}: {iban}"
        
        # Check length
        expected_len = IBAN_STRUCTURES[country][0]
        assert len(iban) == expected_len, f"Wrong length for {country}: {len(iban)} vs {expected_len}"
    
    # Invalid country should raise
    try:
        generate_test_iban("XX")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("✓ test_generate_test_iban passed")


def test_generate_batch_test_ibans():
    """Test batch IBAN generation."""
    ibans = generate_batch_test_ibans("DE", 10)
    assert len(ibans) == 10
    assert all(validate(iban) for iban in ibans)
    assert all(iban.startswith("DE") for iban in ibans)
    
    print("✓ test_generate_batch_test_ibans passed")


def test_extract_bank_info():
    """Test bank information extraction."""
    # German IBAN
    info = extract_bank_info("DE89370400440532013000")
    assert info['country_code'] == "DE"
    assert info['bank_code'] == "37040044"
    assert info['account_number'] == "0532013000"
    
    # UK IBAN
    info = extract_bank_info("GB82WEST12345698765432")
    assert info['country_code'] == "GB"
    assert info['bank_code'] == "WEST"
    assert info['branch_code'] == "1234"
    
    # French IBAN
    info = extract_bank_info("FR1420041010050500013M02606")
    assert info['country_code'] == "FR"
    assert info['bank_code'] == "20041"
    
    print("✓ test_extract_bank_info passed")


def test_iban_validator_class():
    """Test IBANValidator class."""
    validator = IBANValidator()
    
    # Validate
    assert validator.validate("DE89370400440532013000") == True
    assert validator.validate("GB82WEST12345698765433") == False
    
    # Parse
    parsed = validator.parse("DE89370400440532013000")
    assert parsed['country_name'] == "Germany"
    
    # Format
    formatted = validator.format("DE89370400440532013000")
    assert formatted == "DE89 3704 0044 0532 0130 00"
    
    # Strip
    stripped = validator.strip("GB82 WEST 1234 5698 7654 32")
    assert stripped == "GB82WEST12345698765432"
    
    # Get country
    country = validator.get_country("DE89370400440532013000")
    assert country == "Germany"
    
    # Generate test
    test_iban = validator.generate_test("FR")
    assert validator.validate(test_iban) == True
    
    # Bank info
    info = validator.get_bank_info("DE89370400440532013000")
    assert info['country_code'] == "DE"
    
    # Custom separator
    validator2 = IBANValidator(separator="-")
    formatted = validator2.format("DE89370400440532013000")
    assert formatted == "DE89-3704-0044-0532-0130-00"
    
    print("✓ test_iban_validator_class passed")


def test_all_test_ibans():
    """Test all predefined test IBANs."""
    failed = []
    for country, iban in TEST_IBANS.items():
        if not validate(iban):
            failed.append((country, iban))
    
    assert len(failed) == 0, f"Invalid test IBANs: {failed}"
    print(f"✓ test_all_test_ibans passed ({len(TEST_IBANS)} IBANs)")


def test_country_ibans_match_structure():
    """Test that IBAN_STRUCTURES entries have correct information."""
    for country, (length, structure) in IBAN_STRUCTURES.items():
        # Check country code
        assert len(country) == 2, f"Invalid country code: {country}"
        assert country.isupper(), f"Country code not uppercase: {country}"
        
        # Check length
        assert 15 <= length <= 34, f"Unusual IBAN length for {country}: {length}"
        
        # Check structure format
        assert structure, f"Empty structure for {country}"
    
    print(f"✓ test_country_ibans_match_structure passed ({len(IBAN_STRUCTURES)} countries)")


def test_roundtrip_format_strip():
    """Test that format and strip are reversible."""
    test_ibans = [
        "GB82WEST12345698765432",
        "DE89370400440532013000",
        "FR1420041010050500013M02606",
    ]
    
    for iban in test_ibans:
        formatted = format_iban(iban)
        stripped = strip_formatting(formatted)
        assert stripped == iban, f"Roundtrip failed: {iban} -> {formatted} -> {stripped}"
    
    print("✓ test_roundtrip_format_strip passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Running IBAN Utils Tests")
    print("=" * 60 + "\n")
    
    test_strip_formatting()
    test_validate_check_digits()
    test_validate()
    test_calculate_check_digits()
    test_parse()
    test_format_iban()
    test_get_country_info()
    test_get_supported_countries()
    test_generate_test_iban()
    test_generate_batch_test_ibans()
    test_extract_bank_info()
    test_iban_validator_class()
    test_all_test_ibans()
    test_country_ibans_match_structure()
    test_roundtrip_format_strip()
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()