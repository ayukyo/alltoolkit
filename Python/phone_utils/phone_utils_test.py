"""
AllToolkit - Python Phone Utilities Test Suite

Comprehensive test suite for phone number validation, parsing, and processing utilities.
Run with: python phone_utils_test.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    PhoneUtils, PhoneNumber,
    validate, parse, normalize, format_international, format_national,
    get_country_code, get_country, get_country_name, get_number_type,
    is_mobile, is_landline, is_toll_free,
    extract_from_text, deduplicate, sort_by_country, group_by_country, mask
)


# ============================================================================
# Validation Tests
# ============================================================================

def test_validate_valid_phones():
    """Test validation of valid phone numbers."""
    valid_phones = [
        "+12345678900",
        "+8613812345678",
        "+447911123456",
        "+4915123456789",
        "+33612345678",
        "+819012345678",
        "+61412345678",
        "+5511987654321",
        "+919876543210",
        "+1-234-567-8900",
        "+86 138 1234 5678",
        "(234) 567-8900",
        "234-567-8900",
        "13812345678",
    ]
    
    for phone in valid_phones:
        result = validate(phone)
        assert result is True, f"Expected {phone} to be valid, got {result}"
    
    print("✓ test_validate_valid_phones passed")


def test_validate_invalid_phones():
    """Test validation of invalid phone numbers."""
    invalid_phones = [
        "",
        "123",
        "12345",
        "123456",
        None,
        12345,
        "+",
        "+0",
        "+12",
        "abc123",
        "+1-234-567",  # Too short
    ]
    
    for phone in invalid_phones:
        result = validate(phone)
        assert result is False, f"Expected {phone} to be invalid, got {result}"
    
    print("✓ test_validate_invalid_phones passed")


def test_validate_with_country():
    """Test validation with explicit country code."""
    # US number with country specified
    assert validate("2345678900", "US") is True
    assert validate("234567890", "US") is False  # Too short (9 digits)
    
    # China number with country specified
    assert validate("13812345678", "CN") is True
    assert validate("138123456", "CN") is False  # Too short (9 digits, not valid mobile)
    
    # UK number
    assert validate("7911123456", "GB") is True
    
    print("✓ test_validate_with_country passed")


# ============================================================================
# Parsing Tests
# ============================================================================

def test_parse_with_country_code():
    """Test parsing phone numbers with country codes."""
    # US number
    parsed = parse("+12345678900")
    assert parsed is not None
    assert parsed.country_code == "+1"
    assert parsed.national_number == "2345678900"
    assert parsed.country == "US"
    assert parsed.e164 == "+12345678900"
    
    # China number
    parsed = parse("+8613812345678")
    assert parsed is not None
    assert parsed.country_code == "+86"
    assert parsed.national_number == "13812345678"
    assert parsed.country == "CN"
    
    # UK number
    parsed = parse("+447911123456")
    assert parsed is not None
    assert parsed.country_code == "+44"
    assert parsed.country == "GB"
    
    print("✓ test_parse_with_country_code passed")


def test_parse_without_country_code():
    """Test parsing phone numbers without country codes."""
    # US format
    parsed = parse("(234) 567-8900", "US")
    assert parsed is not None
    assert parsed.country == "US"
    
    # Simple number with default country
    parsed = parse("13812345678", "CN")
    assert parsed is not None
    assert parsed.country == "CN"
    
    print("✓ test_parse_without_country_code passed")


def test_parse_invalid():
    """Test parsing invalid phone numbers."""
    assert parse("") is None
    assert parse("123") is None
    assert parse(None) is None
    assert parse("abc") is None
    
    print("✓ test_parse_invalid passed")


# ============================================================================
# Normalization Tests
# ============================================================================

def test_normalize_to_e164():
    """Test normalization to E.164 format."""
    assert normalize("+1-234-567-8900") == "+12345678900"
    assert normalize("+86 138 1234 5678") == "+8613812345678"
    assert normalize("+44 7911 123456") == "+447911123456"
    assert normalize("(234) 567-8900", "US") == "+12345678900"
    
    print("✓ test_normalize_to_e164 passed")


def test_normalize_invalid():
    """Test normalization of invalid numbers."""
    assert normalize("") is None
    assert normalize("123") is None
    assert normalize("abc") is None
    
    print("✓ test_normalize_invalid passed")


# ============================================================================
# Formatting Tests
# ============================================================================

def test_format_international():
    """Test international formatting."""
    result = format_international("+12345678900")
    assert result is not None
    assert result.startswith("+1")
    
    result = format_international("+8613812345678")
    assert result is not None
    assert result.startswith("+86")
    
    print("✓ test_format_international passed")


def test_format_national():
    """Test national formatting."""
    # US format
    result = format_national("+12345678900")
    assert result is not None
    assert "(" in result or " " in result  # US format has parentheses or spaces
    
    # China format
    result = format_national("+8613812345678")
    assert result is not None
    
    print("✓ test_format_national passed")


# ============================================================================
# Country Detection Tests
# ============================================================================

def test_get_country_code():
    """Test country code extraction."""
    assert get_country_code("+12345678900") == "+1"
    assert get_country_code("+8613812345678") == "+86"
    assert get_country_code("+447911123456") == "+44"
    assert get_country_code("+4915123456789") == "+49"
    assert get_country_code("") is None
    
    print("✓ test_get_country_code passed")


def test_get_country():
    """Test country detection."""
    assert get_country("+12345678900") == "US"
    assert get_country("+8613812345678") == "CN"
    assert get_country("+447911123456") == "GB"
    assert get_country("+4915123456789") == "DE"
    assert get_country("+819012345678") == "JP"
    assert get_country("+61412345678") == "AU"
    assert get_country("") is None
    
    print("✓ test_get_country passed")


def test_get_country_name():
    """Test country name lookup."""
    assert get_country_name("US") == "United States"
    assert get_country_name("CN") == "China"
    assert get_country_name("GB") == "United Kingdom"
    assert get_country_name("DE") == "Germany"
    assert get_country_name("XX") is None
    
    print("✓ test_get_country_name passed")


# ============================================================================
# Number Type Detection Tests
# ============================================================================

def test_is_mobile():
    """Test mobile number detection."""
    # China mobile
    assert is_mobile("+8613812345678", "CN") is True
    assert is_mobile("+8615912345678", "CN") is True
    
    # Note: US/Canada NANP numbers cannot be reliably classified as mobile vs landline
    # by prefix alone due to number portability. Skip US mobile test.
    # assert is_mobile("+12345678900", "US") is True
    
    # UK mobile (starts with 7)
    assert is_mobile("+447911123456", "GB") is True
    
    # Germany mobile
    assert is_mobile("+4915123456789", "DE") is True
    
    print("✓ test_is_mobile passed")


def test_is_landline():
    """Test landline detection."""
    # US landline
    assert is_landline("+12125551234", "US") is True
    
    # China landline (not starting with 1)
    # Note: This depends on the prefix detection
    
    print("✓ test_is_landline passed")


def test_is_toll_free():
    """Test toll-free number detection."""
    # US toll-free
    assert is_toll_free("+18001234567", "US") is True
    assert is_toll_free("+18881234567", "US") is True
    
    # China toll-free
    assert is_toll_free("+864001234567", "CN") is True
    
    print("✓ test_is_toll_free passed")


def test_get_number_type():
    """Test number type detection."""
    # Mobile
    assert get_number_type("+8613812345678", "CN") == "mobile"
    
    # Toll-free
    assert get_number_type("+18001234567", "US") == "toll_free"
    
    # Premium (US 900)
    assert get_number_type("+19001234567", "US") == "premium"
    
    print("✓ test_get_number_type passed")


# ============================================================================
# Extraction Tests
# ============================================================================

def test_extract_from_text():
    """Test phone number extraction from text."""
    text = """
    Contact us at:
    - US: +1-234-567-8900
    - China: +86 138 1234 5678
    - UK: +44 7911 123456
    - Office: (234) 567-8900
    - Fax: 234-567-8901
    """
    
    phones = extract_from_text(text)
    assert len(phones) >= 3  # At least 3 valid numbers
    
    print("✓ test_extract_from_text passed")


def test_extract_empty():
    """Test extraction from empty text."""
    assert extract_from_text("") == []
    assert extract_from_text("No numbers here") == []
    
    print("✓ test_extract_empty passed")


# ============================================================================
# Deduplication Tests
# ============================================================================

def test_deduplicate():
    """Test phone number deduplication."""
    phones = [
        "+1-234-567-8900",
        "+12345678900",
        "(234) 567-8900",
        "234-567-8900",
        "+8613812345678",
        "+86 138 1234 5678",
    ]
    
    unique = deduplicate(phones, "US")
    # Should deduplicate US numbers, keep Chinese
    assert len(unique) < len(phones)
    
    print("✓ test_deduplicate passed")


def test_deduplicate_empty():
    """Test deduplication of empty list."""
    assert deduplicate([]) == []
    
    print("✓ test_deduplicate_empty passed")


# ============================================================================
# Sorting and Grouping Tests
# ============================================================================

def test_sort_by_country():
    """Test sorting by country code."""
    phones = [
        "+8613812345678",
        "+12345678900",
        "+447911123456",
        "+4915123456789",
    ]
    
    sorted_phones = sort_by_country(phones)
    assert sorted_phones[0].startswith("+1")  # US first
    assert sorted_phones[-1].startswith("+86")  # CN last
    
    print("✓ test_sort_by_country passed")


def test_group_by_country():
    """Test grouping by country."""
    phones = [
        "+12345678900",
        "+19876543210",
        "+8613812345678",
        "+447911123456",
    ]
    
    grouped = group_by_country(phones)
    assert "US" in grouped
    assert "CN" in grouped
    assert "GB" in grouped
    assert len(grouped["US"]) == 2
    assert len(grouped["CN"]) == 1
    assert len(grouped["GB"]) == 1
    
    print("✓ test_group_by_country passed")


def test_group_empty():
    """Test grouping empty list."""
    assert group_by_country([]) == {}
    
    print("✓ test_group_empty passed")


# ============================================================================
# Masking Tests
# ============================================================================

def test_mask():
    """Test phone number masking."""
    # Default: show last 4
    masked = mask("+12345678900")
    assert masked is not None
    assert "*" in masked
    assert masked.endswith("8900")
    
    # China number
    masked = mask("+8613812345678")
    assert masked is not None
    assert "*" in masked
    assert masked.endswith("5678")
    
    print("✓ test_mask passed")


def test_mask_custom():
    """Test masking with custom show_last."""
    masked = mask("+12345678900", show_last=2)
    assert masked is not None
    assert masked.endswith("00")
    
    masked = mask("+12345678900", show_last=6)
    assert masked is not None
    assert masked.endswith("678900")
    
    print("✓ test_mask_custom passed")


def test_mask_invalid():
    """Test masking invalid numbers."""
    assert mask("") is None
    assert mask("123") is None
    
    print("✓ test_mask_invalid passed")


# ============================================================================
# Edge Cases and Boundary Tests
# ============================================================================

def test_edge_cases():
    """Test edge cases."""
    # Very long number
    assert validate("+1" + "1234567890123456") is False
    
    # Minimum valid length
    assert validate("1234567") is True  # 7 digits minimum
    
    # Special characters
    assert validate("+1 (234) 567-8900") is True
    assert validate("+1.234.567.8900") is True
    
    print("✓ test_edge_cases passed")


def test_country_code_variants():
    """Test various country codes."""
    # Test a variety of country codes
    test_cases = [
        ("+1234567890", "US"),
        ("+71234567890", "RU"),
        ("+33123456789", "FR"),
        ("+491234567890", "DE"),
        ("+811234567890", "JP"),
        ("+911234567890", "IN"),
        ("+5511234567890", "BR"),
        ("+61123456789", "AU"),
    ]
    
    for phone, expected_country in test_cases:
        country = get_country(phone)
        assert country == expected_country, f"Expected {expected_country} for {phone}, got {country}"
    
    print("✓ test_country_code_variants passed")


# ============================================================================
# Integration Tests
# ============================================================================

def test_full_workflow():
    """Test complete workflow."""
    raw_phones = [
        "+1-234-567-8900",
        "+86 138 1234 5678",
        "+44 7911 123456",
        "+1-234-567-8900",  # Duplicate
        "Invalid",
        "+4915123456789",
    ]
    
    # Extract and validate
    valid_phones = [p for p in raw_phones if validate(p)]
    assert len(valid_phones) == 5  # 5 valid (including duplicate)
    
    # Deduplicate
    unique = deduplicate(valid_phones, "US")
    assert len(unique) == 4  # One duplicate removed (5 - 1 = 4)
    
    # Group by country
    grouped = group_by_country(unique)
    assert "US" in grouped
    assert "CN" in grouped
    assert "GB" in grouped or "DE" in grouped
    
    # Parse and format
    for phone in unique:
        parsed = parse(phone)
        assert parsed is not None
        assert parsed.is_valid is True
        assert parsed.e164 is not None
    
    print("✓ test_full_workflow passed")


def test_phone_number_dataclass():
    """Test PhoneNumber dataclass."""
    parsed = parse("+12345678900")
    assert parsed is not None
    
    # Check all fields exist
    assert hasattr(parsed, 'country_code')
    assert hasattr(parsed, 'national_number')
    assert hasattr(parsed, 'original')
    assert hasattr(parsed, 'international')
    assert hasattr(parsed, 'national')
    assert hasattr(parsed, 'e164')
    assert hasattr(parsed, 'country')
    assert hasattr(parsed, 'is_valid')
    assert hasattr(parsed, 'number_type')
    
    # Check values
    assert parsed.country_code == "+1"
    assert parsed.national_number == "2345678900"
    assert parsed.country == "US"
    assert parsed.is_valid is True
    
    print("✓ test_phone_number_dataclass passed")


# ============================================================================
# Test Runner
# ============================================================================

def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("AllToolkit - Phone Utils Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_validate_valid_phones,
        test_validate_invalid_phones,
        test_validate_with_country,
        test_parse_with_country_code,
        test_parse_without_country_code,
        test_parse_invalid,
        test_normalize_to_e164,
        test_normalize_invalid,
        test_format_international,
        test_format_national,
        test_get_country_code,
        test_get_country,
        test_get_country_name,
        test_is_mobile,
        test_is_landline,
        test_is_toll_free,
        test_get_number_type,
        test_extract_from_text,
        test_extract_empty,
        test_deduplicate,
        test_deduplicate_empty,
        test_sort_by_country,
        test_group_by_country,
        test_group_empty,
        test_mask,
        test_mask_custom,
        test_mask_invalid,
        test_edge_cases,
        test_country_code_variants,
        test_full_workflow,
        test_phone_number_dataclass,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
