"""
AllToolkit - Python Email Utilities Test Suite

Comprehensive test suite for email validation, parsing, and processing utilities.
Run with: python email_utils_test.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    EmailUtils, EmailAddress,
    validate, parse, normalize, is_disposable, is_free_provider,
    get_domain, get_local, obfuscate, format_with_name,
    extract_from_text, deduplicate, sort_by_domain, group_by_domain
)


# ============================================================================
# Validation Tests
# ============================================================================

def test_validate_valid_emails():
    """Test validation of valid email addresses."""
    valid_emails = [
        "user@example.com",
        "test.email@domain.org",
        "user+tag@gmail.com",
        "user_name@sub.domain.com",
        "a@b.co",
        "user123@test123.com",
        "user-name@example.com",
        "user.name@example.com",
        "user+newsletter@example.com",
        "USER@EXAMPLE.COM",
        "user@EXAMPLE.COM",
        "user@subdomain.example.com",
        "user@very-long-subdomain.example.com",
        "user_name123@test-domain.co.uk",
        "a@b.cd",
    ]
    
    for email in valid_emails:
        result = validate(email)
        assert result is True, f"Expected {email} to be valid, got {result}"
    
    print("✓ test_validate_valid_emails passed")


def test_validate_invalid_emails():
    """Test validation of invalid email addresses."""
    invalid_emails = [
        "",
        "invalid",
        "@example.com",
        "user@",
        "user@.com",
        "user@domain.",
        "user@domain.c",  # TLD too short
        "user@domain.123",  # TLD not alphabetic
        ".user@example.com",  # Leading dot
        "user.@example.com",  # Trailing dot
        "user..name@example.com",  # Consecutive dots
        "user@domain..com",  # Consecutive dots in domain
        "user name@example.com",  # Space in local part
        "user@exam ple.com",  # Space in domain
        "user@-example.com",  # Leading hyphen in domain
        "user@example-.com",  # Trailing hyphen in domain part
        "a" * 65 + "@example.com",  # Local part too long (>64)
        "user@" + "a" * 256 + ".com",  # Domain too long (>255)
        None,
        123,
        "user@example",  # No TLD
    ]
    
    for email in invalid_emails:
        result = validate(email)
        assert result is False, f"Expected {email} to be invalid, got {result}"
    
    print("✓ test_validate_invalid_emails passed")


def test_validate_edge_cases():
    """Test edge cases in validation."""
    # Empty string
    assert validate("") is False
    
    # Whitespace only
    assert validate("   ") is False
    
    # Valid with leading/trailing whitespace (should be stripped)
    assert validate("  user@example.com  ") is True
    
    # Maximum valid lengths
    local_64 = "a" * 64
    assert validate(f"{local_64}@example.com") is True
    
    print("✓ test_validate_edge_cases passed")


# ============================================================================
# Parsing Tests
# ============================================================================

def test_parse_simple_email():
    """Test parsing simple email addresses."""
    result = parse("user@example.com")
    assert result is not None
    assert result.local == "user"
    assert result.domain == "example.com"
    assert result.original == "user@example.com"
    assert result.normalized == "user@example.com"
    assert result.is_valid is True
    assert result.display_name is None
    
    print("✓ test_parse_simple_email passed")


def test_parse_with_display_name():
    """Test parsing emails with display names."""
    # Quoted name
    result = parse('"John Doe" <user@example.com>')
    assert result is not None
    assert result.display_name == "John Doe"
    assert result.local == "user"
    assert result.domain == "example.com"
    
    # Unquoted name
    result2 = parse('Jane Smith <jane@example.com>')
    assert result2 is not None
    assert result2.display_name == "Jane Smith"
    assert result2.local == "jane"
    
    print("✓ test_parse_with_display_name passed")


def test_parse_invalid():
    """Test parsing invalid emails."""
    assert parse("") is None
    assert parse("invalid") is None
    assert parse("@example.com") is None
    assert parse(None) is None
    
    print("✓ test_parse_invalid passed")


def test_parse_normalization():
    """Test that parsing normalizes domain to lowercase."""
    result = parse("User@EXAMPLE.COM")
    assert result is not None
    assert result.local == "User"  # Local part preserved
    assert result.domain == "EXAMPLE.COM"  # Original domain preserved
    assert result.normalized == "User@example.com"  # Normalized has lowercase domain
    
    print("✓ test_parse_normalization passed")


# ============================================================================
# Normalization Tests
# ============================================================================

def test_normalize_lowercase_domain():
    """Test that normalization lowercases both local and domain."""
    assert normalize("User@EXAMPLE.COM") == "user@example.com"
    assert normalize("test@GMAIL.COM") == "test@gmail.com"
    assert normalize("UserName@Example.COM") == "username@example.com"
    
    print("✓ test_normalize_lowercase_domain passed")


def test_normalize_gmail_dots():
    """Test Gmail dot removal."""
    assert normalize("first.last@gmail.com") == "firstlast@gmail.com"
    assert normalize("f.i.r.s.t@gmail.com") == "first@gmail.com"
    assert normalize("first.last@googlemail.com") == "firstlast@googlemail.com"
    
    print("✓ test_normalize_gmail_dots passed")


def test_normalize_gmail_subaddressing():
    """Test Gmail subaddressing (+tag) removal."""
    assert normalize("user+tag@gmail.com") == "user@gmail.com"
    assert normalize("user+newsletter+more@gmail.com") == "user@gmail.com"
    assert normalize("first.last+tag@gmail.com") == "firstlast@gmail.com"
    
    print("✓ test_normalize_gmail_subaddressing passed")


def test_normalize_non_gmail_subaddressing():
    """Test subaddressing removal for non-Gmail providers."""
    assert normalize("user+tag@example.com") == "user@example.com"
    assert normalize("user+newsletter@yahoo.com") == "user@yahoo.com"
    
    # Dots should be preserved for non-Gmail
    assert normalize("first.last@example.com") == "first.last@example.com"
    
    print("✓ test_normalize_non_gmail_subaddressing passed")


def test_normalize_invalid():
    """Test normalization of invalid emails."""
    assert normalize("") is None
    assert normalize("invalid") is None
    
    print("✓ test_normalize_invalid passed")


# ============================================================================
# Disposable Email Tests
# ============================================================================

def test_is_disposable_true():
    """Test detection of disposable email providers."""
    disposable_emails = [
        "user@mailinator.com",
        "test@10minutemail.com",
        "temp@guerrillamail.com",
        "throwaway@yopmail.com",
        "spam@trashmail.com",
    ]
    
    for email in disposable_emails:
        result = is_disposable(email)
        assert result is True, f"Expected {email} to be detected as disposable"
    
    print("✓ test_is_disposable_true passed")


def test_is_disposable_false():
    """Test that regular emails are not flagged as disposable."""
    regular_emails = [
        "user@gmail.com",
        "test@company.com",
        "admin@example.org",
        "contact@university.edu",
    ]
    
    for email in regular_emails:
        result = is_disposable(email)
        assert result is False, f"Expected {email} to NOT be disposable"
    
    print("✓ test_is_disposable_false passed")


def test_is_disposable_case_insensitive():
    """Test case-insensitive disposable detection."""
    assert is_disposable("user@MAILINATOR.COM") is True
    assert is_disposable("test@Yopmail.com") is True
    
    print("✓ test_is_disposable_case_insensitive passed")


# ============================================================================
# Free Provider Tests
# ============================================================================

def test_is_free_provider_true():
    """Test detection of free email providers."""
    free_emails = [
        "user@gmail.com",
        "test@yahoo.com",
        "admin@hotmail.com",
        "contact@outlook.com",
        "me@icloud.com",
        "user@protonmail.com",
        "test@qq.com",
        "admin@163.com",
    ]
    
    for email in free_emails:
        result = is_free_provider(email)
        assert result is True, f"Expected {email} to be detected as free provider"
    
    print("✓ test_is_free_provider_true passed")


def test_is_free_provider_false():
    """Test that disposable/custom domains are not flagged as free providers."""
    custom_emails = [
        "user@company.com",
        "test@university.edu",
        "admin@organization.org",
        "contact@business.co.uk",
    ]
    
    for email in custom_emails:
        result = is_free_provider(email)
        assert result is False, f"Expected {email} to NOT be a free provider"
    
    print("✓ test_is_free_provider_false passed")


# ============================================================================
# Domain/Local Extraction Tests
# ============================================================================

def test_get_domain():
    """Test domain extraction."""
    assert get_domain("user@example.com") == "example.com"
    assert get_domain("test@sub.domain.org") == "sub.domain.org"
    assert get_domain("invalid") is None
    assert get_domain("") is None
    
    print("✓ test_get_domain passed")


def test_get_local():
    """Test local part extraction."""
    assert get_local("user@example.com") == "user"
    assert get_local("test.user+tag@example.com") == "test.user+tag"
    assert get_local("invalid") is None
    assert get_local("") is None
    
    print("✓ test_get_local passed")


# ============================================================================
# Obfuscation Tests
# ============================================================================

def test_obfuscate_default():
    """Test email obfuscation with default settings."""
    result = obfuscate("john.doe@example.com")
    assert result == "jo*******@example.com"
    
    result2 = obfuscate("ab@example.com")
    assert result2 == "ab@example.com"  # Too short to obfuscate
    
    result3 = obfuscate("abc@example.com")
    assert result3 == "ab*******@example.com"  # Shows first 2, then 7 asterisks
    
    print("✓ test_obfuscate_default passed")


def test_obfuscate_custom_chars():
    """Test email obfuscation with custom character count."""
    result = obfuscate("john@example.com", show_chars=3)
    assert result == "joh*******@example.com"  # Shows first 3 chars + 7 asterisks
    
    result2 = obfuscate("john@example.com", show_chars=1)
    assert result2 == "j*******@example.com"  # Shows first 1 char + 7 asterisks
    
    # Short email - no obfuscation
    result3 = obfuscate("ab@example.com", show_chars=3)
    assert result3 == "ab@example.com"
    
    print("✓ test_obfuscate_custom_chars passed")


def test_obfuscate_invalid():
    """Test obfuscation of invalid emails."""
    assert obfuscate("") is None
    assert obfuscate("invalid") is None
    
    print("✓ test_obfuscate_invalid passed")


# ============================================================================
# Format with Name Tests
# ============================================================================

def test_format_with_name_provided():
    """Test formatting with provided name."""
    result = format_with_name("user@example.com", "John Doe")
    assert result == '"John Doe" <user@example.com>'
    
    print("✓ test_format_with_name_provided passed")


def test_format_with_name_from_parsed():
    """Test formatting using parsed display name."""
    result = format_with_name('"Jane Smith" <jane@example.com>')
    assert result == '"Jane Smith" <jane@example.com>'
    
    print("✓ test_format_with_name_from_parsed passed")


def test_format_with_name_no_name():
    """Test formatting without name."""
    result = format_with_name("user@example.com")
    assert result == "user@example.com"
    
    print("✓ test_format_with_name_no_name passed")


def test_format_with_name_special_chars():
    """Test formatting with special characters in name."""
    result = format_with_name("user@example.com", 'John "The Dev" Doe')
    assert '\\"' in result  # Quotes should be escaped
    
    print("✓ test_format_with_name_special_chars passed")


# ============================================================================
# Extract from Text Tests
# ============================================================================

def test_extract_from_text_single():
    """Test extracting single email from text."""
    text = "Contact us at support@example.com for help."
    result = extract_from_text(text)
    assert result == ["support@example.com"]
    
    print("✓ test_extract_from_text_single passed")


def test_extract_from_text_multiple():
    """Test extracting multiple emails from text."""
    text = """
    Contact our team:
    - Sales: sales@company.com
    - Support: support@company.com
    - HR: hr@company.com
    """
    result = extract_from_text(text)
    assert len(result) == 3
    assert "sales@company.com" in result
    assert "support@company.com" in result
    assert "hr@company.com" in result
    
    print("✓ test_extract_from_text_multiple passed")


def test_extract_from_text_none():
    """Test extraction when no emails present."""
    text = "This text contains no email addresses."
    result = extract_from_text(text)
    assert result == []
    
    print("✓ test_extract_from_text_none passed")


def test_extract_from_text_invalid_filtered():
    """Test that invalid emails are filtered out."""
    text = "Valid: user@example.com Invalid: @bad.com also@bad"
    result = extract_from_text(text)
    # "also@bad" is now filtered because domain must have a TLD with dot
    assert result == ["user@example.com"]
    
    print("✓ test_extract_from_text_invalid_filtered passed")


# ============================================================================
# Deduplication Tests
# ============================================================================

def test_deduplicate_exact():
    """Test deduplication of exact duplicates."""
    emails = ["user@example.com", "user@example.com", "user@example.com"]
    result = deduplicate(emails)
    assert result == ["user@example.com"]
    
    print("✓ test_deduplicate_exact passed")


def test_deduplicate_case_insensitive():
    """Test case-insensitive deduplication."""
    emails = ["User@Example.com", "user@example.com", "USER@EXAMPLE.COM"]
    result = deduplicate(emails)
    assert len(result) == 1
    assert result[0] == "User@Example.com"  # First occurrence kept
    
    print("✓ test_deduplicate_case_insensitive passed")


def test_deduplicate_normalized():
    """Test deduplication with Gmail normalization."""
    emails = ["first.last@gmail.com", "firstlast@gmail.com", "first.last+tag@gmail.com"]
    result = deduplicate(emails)
    assert len(result) == 1
    assert result[0] == "first.last@gmail.com"  # First occurrence kept
    
    print("✓ test_deduplicate_normalized passed")


def test_deduplicate_preserves_order():
    """Test that deduplication preserves original order."""
    emails = ["a@example.com", "b@example.com", "a@example.com", "c@example.com"]
    result = deduplicate(emails)
    assert result == ["a@example.com", "b@example.com", "c@example.com"]
    
    print("✓ test_deduplicate_preserves_order passed")


# ============================================================================
# Sorting Tests
# ============================================================================

def test_sort_by_domain():
    """Test sorting emails by domain."""
    emails = ["b@yahoo.com", "a@gmail.com", "c@gmail.com", "d@aol.com"]
    result = sort_by_domain(emails)
    
    # Should be sorted: aol.com, gmail.com, gmail.com, yahoo.com
    assert result[0] == "d@aol.com"
    assert result[1] == "a@gmail.com"
    assert result[2] == "c@gmail.com"
    assert result[3] == "b@yahoo.com"
    
    print("✓ test_sort_by_domain passed")


def test_sort_by_domain_case_insensitive():
    """Test case-insensitive domain sorting."""
    emails = ["user@ZOO.com", "user@apple.com", "user@Banana.com"]
    result = sort_by_domain(emails)
    
    assert result[0] == "user@apple.com"
    assert result[1] == "user@Banana.com"
    assert result[2] == "user@ZOO.com"
    
    print("✓ test_sort_by_domain_case_insensitive passed")


# ============================================================================
# Grouping Tests
# ============================================================================

def test_group_by_domain():
    """Test grouping emails by domain."""
    emails = ["a@gmail.com", "b@yahoo.com", "c@gmail.com", "d@yahoo.com"]
    result = group_by_domain(emails)
    
    assert len(result) == 2
    assert len(result["gmail.com"]) == 2
    assert len(result["yahoo.com"]) == 2
    assert "a@gmail.com" in result["gmail.com"]
    assert "c@gmail.com" in result["gmail.com"]
    
    print("✓ test_group_by_domain passed")


def test_group_by_domain_case_insensitive():
    """Test case-insensitive domain grouping."""
    emails = ["a@Gmail.com", "b@GMAIL.COM", "c@gmail.com"]
    result = group_by_domain(emails)
    
    assert len(result) == 1
    assert "gmail.com" in result
    assert len(result["gmail.com"]) == 3
    
    print("✓ test_group_by_domain_case_insensitive passed")


# ============================================================================
# EmailAddress Dataclass Tests
# ============================================================================

def test_email_address_attributes():
    """Test EmailAddress dataclass attributes."""
    result = parse("test.user+tag@Example.COM")
    assert result is not None
    assert isinstance(result, EmailAddress)
    assert result.local == "test.user+tag"
    assert result.domain == "Example.COM"
    assert result.normalized == "test.user+tag@example.com"
    assert result.is_valid is True
    
    print("✓ test_email_address_attributes passed")


# ============================================================================
# Integration Tests
# ============================================================================

def test_full_workflow():
    """Test a complete email processing workflow."""
    # Input: mixed list with duplicates, various formats
    raw_emails = [
        '"John Doe" <John.Doe+newsletter@Gmail.com>',
        "johndoe@gmail.com",
        "Jane.Smith@Company.com",
        "jane.smith@company.com",  # Duplicate (normalized)
        "spam@mailinator.com",
        "admin@yahoo.com",
        "invalid-email",
        "@bad.com",
    ]
    
    # Extract and validate
    valid_emails = [e for e in raw_emails if validate(e.split('<')[-1].rstrip('>') if '<' in e else e)]
    
    # Normalize and deduplicate
    normalized = [normalize(e) for e in valid_emails if normalize(e)]
    unique = list(set(normalized))
    
    # Group by domain type
    gmail_users = [e for e in unique if 'gmail.com' in e.lower()]
    disposable = [e for e in unique if is_disposable(e)]
    
    assert len(gmail_users) == 1  # John Doe variants should be deduplicated
    assert len(disposable) == 1  # mailinator
    assert "jane.smith@company.com" in unique
    
    print("✓ test_full_workflow passed")


def test_bulk_operations():
    """Test bulk email operations."""
    emails = [
        "user1@gmail.com",
        "user2@yahoo.com",
        "user1@gmail.com",  # Duplicate of user1
        "user4@company.com",
        "user5@hotmail.com",
        "User1@Gmail.com",  # Case-insensitive duplicate
    ]
    
    # Deduplicate
    unique = deduplicate(emails)
    assert len(unique) == 4  # Two duplicates removed (user1 appears 3 times)
    
    # Sort
    sorted_emails = sort_by_domain(unique)
    assert sorted_emails[0].endswith("@company.com")  # company.com comes first alphabetically
    
    # Group
    grouped = group_by_domain(unique)
    assert len(grouped["gmail.com"]) == 1  # Only user1
    
    print("✓ test_bulk_operations passed")


# ============================================================================
# Run All Tests
# ============================================================================

def run_all_tests():
    """Run all test functions."""
    test_functions = [
        test_validate_valid_emails,
        test_validate_invalid_emails,
        test_validate_edge_cases,
        test_parse_simple_email,
        test_parse_with_display_name,
        test_parse_invalid,
        test_parse_normalization,
        test_normalize_lowercase_domain,
        test_normalize_gmail_dots,
        test_normalize_gmail_subaddressing,
        test_normalize_non_gmail_subaddressing,
        test_normalize_invalid,
        test_is_disposable_true,
        test_is_disposable_false,
        test_is_disposable_case_insensitive,
        test_is_free_provider_true,
        test_is_free_provider_false,
        test_get_domain,
        test_get_local,
        test_obfuscate_default,
        test_obfuscate_custom_chars,
        test_obfuscate_invalid,
        test_format_with_name_provided,
        test_format_with_name_from_parsed,
        test_format_with_name_no_name,
        test_format_with_name_special_chars,
        test_extract_from_text_single,
        test_extract_from_text_multiple,
        test_extract_from_text_none,
        test_extract_from_text_invalid_filtered,
        test_deduplicate_exact,
        test_deduplicate_case_insensitive,
        test_deduplicate_normalized,
        test_deduplicate_preserves_order,
        test_sort_by_domain,
        test_sort_by_domain_case_insensitive,
        test_group_by_domain,
        test_group_by_domain_case_insensitive,
        test_email_address_attributes,
        test_full_workflow,
        test_bulk_operations,
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("AllToolkit - Email Utils Test Suite")
    print("=" * 60)
    print()
    
    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_func.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
