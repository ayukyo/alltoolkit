#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Validation Utilities Usage Examples
=================================================
Practical examples demonstrating how to use the validation_utils module
in real-world scenarios.

Run: python examples/usage_examples.py
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # Basic validators
    is_not_none, is_not_empty, is_type, is_in,
    
    # String validators
    is_email, is_url, is_phone, is_chinese_id, is_credit_card,
    
    # IP validators
    is_ipv4, is_ipv6, is_ip,
    
    # Date/Time validators
    is_date, is_time, is_datetime,
    
    # Number validators
    is_number, is_integer, in_range, is_positive, is_non_negative,
    
    # String length validators
    has_length, matches_pattern,
    
    # Composite validators
    all_of, any_of, optional,
    
    # Batch validation
    Validator, ValidationError,
    
    # Convenience functions
    validate_email, validate_url, validate_phone, validate_credit_card,
    validate_chinese_id, validate_ipv4, validate_ipv6, validate_date,
    validate_range,
)


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_example(description: str, code: str, result):
    """Print an example with description, code, and result."""
    print(f"\n{description}")
    print(f"  Code: {code}")
    print(f"  Result: {result}")


# ============================================================================
# Example 1: Basic Validation
# ============================================================================
def example_basic_validation():
    print_section("Example 1: Basic Validation")
    
    # Check if value is not None
    print_example(
        "Check if value is not None",
        'is_not_none("hello")',
        is_not_none("hello")
    )
    
    # Check if value is not empty
    print_example(
        "Check if string is not empty",
        'is_not_empty("hello")',
        is_not_empty("hello")
    )
    
    # Check type
    print_example(
        "Check if value is an integer",
        'is_type(42, int)',
        is_type(42, int)
    )
    
    # Check if value is in choices
    print_example(
        "Check if value is in allowed choices",
        'is_in("admin", ["admin", "user", "guest"])',
        is_in("admin", ["admin", "user", "guest"])
    )


# ============================================================================
# Example 2: Email and URL Validation
# ============================================================================
def example_email_url():
    print_section("Example 2: Email and URL Validation")
    
    # Valid emails
    emails = [
        "user@example.com",
        "user.name+tag@domain.co.uk",
        "admin@test-domain.org",
    ]
    
    print("\nValidating email addresses:")
    for email in emails:
        result = is_email(email)
        status = "✓" if result.is_valid else "✗"
        print(f"  {status} {email}")
    
    # Invalid emails
    invalid_emails = ["invalid", "@example.com", "user@", "user name@example.com"]
    
    print("\nInvalid email addresses:")
    for email in invalid_emails:
        result = is_email(email)
        status = "✓" if not result.is_valid else "✗"
        print(f"  {status} {email} - Correctly rejected")
    
    # URL validation
    print("\nValidating URLs:")
    urls = [
        ("https://example.com", True),
        ("http://localhost:8080/api", True),
        ("ftp://example.com", False),  # Only http/https allowed
        ("example.com", False),  # Missing scheme
    ]
    
    for url, should_be_valid in urls:
        result = is_url(url)
        status = "✓" if result.is_valid == should_be_valid else "✗"
        expected = "valid" if should_be_valid else "invalid"
        print(f"  {status} {url} (expected: {expected})")


# ============================================================================
# Example 3: Phone Number Validation
# ============================================================================
def example_phone_validation():
    print_section("Example 3: Phone Number Validation")
    
    # Chinese phone numbers
    print("\nChinese phone numbers:")
    cn_phones = ["13812345678", "19912345678", "13 8123 4567 8", "138-1234-5678"]
    
    for phone in cn_phones:
        result = is_phone(phone, country='CN')
        status = "✓" if result.is_valid else "✗"
        print(f"  {status} {phone} -> {result.value if result.is_valid else result.error}")
    
    # US phone numbers
    print("\nUS phone numbers:")
    us_phones = ["2125551234", "12125551234", "(212) 555-1234"]
    
    for phone in us_phones:
        result = is_phone(phone, country='US')
        status = "✓" if result.is_valid else "✗"
        print(f"  {status} {phone} -> {result.value if result.is_valid else result.error}")


# ============================================================================
# Example 4: Chinese ID Card Validation
# ============================================================================
def example_chinese_id():
    print_section("Example 4: Chinese ID Card Validation")
    
    # Valid ID cards
    valid_ids = [
        "11010519491231002X",
        "440106199001011234",
    ]
    
    print("\nValid Chinese ID cards:")
    for id_card in valid_ids:
        result = is_chinese_id(id_card)
        status = "✓" if result.is_valid else "✗"
        print(f"  {status} {id_card}")
    
    # Invalid ID cards
    invalid_ids = [
        "123456789012345678",  # Wrong format
        "11010519491231002A",  # Wrong check digit
        "01010519491231002X",  # Area code starts with 0
    ]
    
    print("\nInvalid Chinese ID cards:")
    for id_card in invalid_ids:
        result = is_chinese_id(id_card)
        status = "✓" if not result.is_valid else "✗"
        print(f"  {status} {id_card} - {result.error}")


# ============================================================================
# Example 5: Credit Card Validation
# ============================================================================
def example_credit_card():
    print_section("Example 5: Credit Card Validation")
    
    # Test card numbers (pass Luhn check)
    cards = [
        ("4532015112830366", "visa", True),
        ("5425233430109903", "mastercard", True),
        ("374245455400126", "amex", True),
        ("6011111111111117", "discover", True),
        ("4532015112830366", "amex", False),  # Wrong type
    ]
    
    print("\nCredit card validation:")
    for card_number, card_type, should_be_valid in cards:
        result = is_credit_card(card_number, card_type=card_type)
        status = "✓" if result.is_valid == should_be_valid else "✗"
        print(f"  {status} {card_type.upper()}: {card_number} (expected: {'valid' if should_be_valid else 'invalid'})")


# ============================================================================
# Example 6: IP Address Validation
# ============================================================================
def example_ip_validation():
    print_section("Example 6: IP Address Validation")
    
    # IPv4
    print("\nIPv4 addresses:")
    ipv4_addresses = [
        ("192.168.1.1", True),
        ("10.0.0.1", True),
        ("255.255.255.255", True),
        ("256.1.1.1", False),
        ("192.168.1", False),
    ]
    
    for ip, should_be_valid in ipv4_addresses:
        result = is_ipv4(ip)
        status = "✓" if result.is_valid == should_be_valid else "✗"
        print(f"  {status} {ip}")
    
    # IPv6
    print("\nIPv6 addresses:")
    ipv6_addresses = [
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", True),
        ("::1", True),
        ("::", True),
        ("2001:db8:::1", False),
        ("gggg::1", False),
    ]
    
    for ip, should_be_valid in ipv6_addresses:
        result = is_ipv6(ip)
        status = "✓" if result.is_valid == should_be_valid else "✗"
        print(f"  {status} {ip}")


# ============================================================================
# Example 7: Date and Time Validation
# ============================================================================
def example_datetime_validation():
    print_section("Example 7: Date and Time Validation")
    
    # Dates
    print("\nDate validation (YYYY-MM-DD):")
    dates = [
        ("2024-01-15", True),
        ("2024-12-31", True),
        ("2000-02-29", True),  # Leap year
        ("2023-02-29", False),  # Not a leap year
        ("2024-13-01", False),  # Invalid month
    ]
    
    for date_str, should_be_valid in dates:
        result = is_date(date_str)
        status = "✓" if result.is_valid == should_be_valid else "✗"
        print(f"  {status} {date_str}")
    
    # Times
    print("\nTime validation:")
    times = [
        ("09:30", "HH:MM", True),
        ("23:59:59", "HH:MM:SS", True),
        ("12:30:45.123", "HH:MM:SS.fff", True),
        ("25:00", "HH:MM", False),
        ("12:60", "HH:MM", False),
    ]
    
    for time_str, fmt, should_be_valid in times:
        result = is_time(time_str, format=fmt)
        status = "✓" if result.is_valid == should_be_valid else "✗"
        print(f"  {status} {time_str} ({fmt})")


# ============================================================================
# Example 8: Number Validation
# ============================================================================
def example_number_validation():
    print_section("Example 8: Number Validation")
    
    # Type checking
    print("\nNumber type checking:")
    print_example("is_number(42)", 'is_number(42)', is_number(42))
    print_example("is_number(3.14)", 'is_number(3.14)', is_number(3.14))
    print_example("is_number(True)", 'is_number(True)', is_number(True))  # bool excluded
    print_example("is_number('42')", "is_number('42')", is_number('42'))
    
    # Range checking
    print("\nRange checking:")
    ranges = [
        (5, 0, 10, True),
        (0, 0, 10, True),   # Boundary
        (10, 0, 10, True),  # Boundary
        (-1, 0, 10, False),
        (11, 0, 10, False),
    ]
    
    for value, min_val, max_val, should_be_valid in ranges:
        result = in_range(value, min_val, max_val)
        status = "✓" if result.is_valid == should_be_valid else "✗"
        print(f"  {status} in_range({value}, {min_val}, {max_val})")
    
    # Positive / Non-negative
    print("\nPositive / Non-negative:")
    print_example("is_positive(1)", 'is_positive(1)', is_positive(1))
    print_example("is_positive(0)", 'is_positive(0)', is_positive(0))
    print_example("is_non_negative(0)", 'is_non_negative(0)', is_non_negative(0))
    print_example("is_non_negative(-1)", 'is_non_negative(-1)', is_non_negative(-1))


# ============================================================================
# Example 9: String Length and Pattern Validation
# ============================================================================
def example_string_validation():
    print_section("Example 9: String Length and Pattern Validation")
    
    # Length checking
    print("\nString length checking:")
    strings = [
        ("hello", 3, 10, True),
        ("ab", 3, 10, False),
        ("abcdefghijk", 3, 10, False),
        ("a", None, 10, True),  # No minimum
        ("very long string", 5, None, True),  # No maximum
    ]
    
    for s, min_len, max_len, should_be_valid in strings:
        result = has_length(s, min_len, max_len)
        status = "✓" if result.is_valid == should_be_valid else "✗"
        print(f"  {status} has_length('{s}', min={min_len}, max={max_len})")
    
    # Pattern matching
    print("\nPattern matching:")
    patterns = [
        ("abc123", r'^[a-z]+\d+$', True),
        ("123abc", r'^[a-z]+\d+$', False),
        ("username_123", r'^[a-zA-Z][a-zA-Z0-9_]*$', True),
        ("123invalid", r'^[a-zA-Z][a-zA-Z0-9_]*$', False),
    ]
    
    for s, pattern, should_be_valid in patterns:
        result = matches_pattern(s, pattern)
        status = "✓" if result.is_valid == should_be_valid else "✗"
        print(f"  {status} matches_pattern('{s}', '{pattern}')")


# ============================================================================
# Example 10: Composite Validators
# ============================================================================
def example_composite_validators():
    print_section("Example 10: Composite Validators")
    
    # all_of - all validators must pass
    print("\nall_of (all must pass):")
    string_validator = all_of([
        lambda v, f: is_type(v, str, f),
        lambda v, f: has_length(v, 3, 10, f),
    ])
    
    test_values = ["hello", "hi", 123, "abcdefghijk"]
    for value in test_values:
        result = string_validator(value)
        status = "✓" if result.is_valid else "✗"
        print(f"  {status} {value!r} -> {result.error if not result.is_valid else 'valid'}")
    
    # any_of - at least one must pass
    print("\nany_of (at least one must pass):")
    contact_validator = any_of([
        lambda v, f: is_email(v, f),
        lambda v, f: is_phone(v, 'CN', f),
    ])
    
    test_values = ["test@example.com", "13812345678", "invalid"]
    for value in test_values:
        result = contact_validator(value)
        status = "✓" if result.is_valid else "✗"
        print(f"  {status} {value!r} -> {'valid' if result.is_valid else 'rejected'}")
    
    # optional - allows None
    print("\noptional (allows None):")
    opt_email = optional(is_email)
    
    test_values = [None, "test@example.com", "invalid"]
    for value in test_values:
        result = opt_email(value)
        status = "✓" if result.is_valid else "✗"
        print(f"  {status} {value!r} -> {'valid' if result.is_valid else result.error}")


# ============================================================================
# Example 11: Batch Validation with Validator Class
# ============================================================================
def example_batch_validation():
    print_section("Example 11: Batch Validation with Validator Class")
    
    # Create a user registration validator
    user_validator = Validator()
    user_validator.rule('email', is_email)
    user_validator.rule('username', lambda v, f: has_length(v, 3, 20, f) if v else 
                       ValidationResult(False, v, error="Username is required"))
    user_validator.rule('age', lambda v, f: in_range(v, 18, 120, f))
    user_validator.rule('phone', optional(lambda v, f: is_phone(v, 'CN', f)))
    
    # Valid user data
    print("\nValid user data:")
    valid_user = {
        'email': 'user@example.com',
        'username': 'john_doe',
        'age': 25,
        'phone': '13812345678',
    }
    
    result = user_validator.validate(valid_user)
    print(f"  Valid: {result.is_valid}")
    if not result.is_valid:
        print(f"  Errors: {user_validator.get_errors()}")
    
    # Invalid user data
    print("\nInvalid user data:")
    invalid_user = {
        'email': 'invalid-email',
        'username': 'ab',  # Too short
        'age': 150,  # Out of range
        'phone': 'not-a-phone',
    }
    
    result = user_validator.validate(invalid_user)
    print(f"  Valid: {result.is_valid}")
    print(f"  Errors:")
    for field, error in user_validator.get_errors().items():
        print(f"    - {field}: {error}")
    
    # Strict mode (no unknown fields)
    print("\nStrict mode (unknown fields):")
    extra_user = {
        'email': 'user@example.com',
        'username': 'john_doe',
        'age': 25,
        'unknown_field': 'value',
    }
    
    result = user_validator.validate(extra_user, strict=True)
    print(f"  Valid: {result.is_valid}")
    if not result.is_valid:
        print(f"  Errors: {user_validator.get_errors()}")
    
    # Exception handling
    print("\nException handling:")
    try:
        user_validator.raise_if_invalid(invalid_user)
    except ValidationError as e:
        print(f"  Caught ValidationError: {e}")


# ============================================================================
# Example 12: Convenience Functions
# ============================================================================
def example_convenience_functions():
    print_section("Example 12: Convenience Functions")
    
    print("\nQuick boolean checks:")
    
    checks = [
        ("validate_email('test@example.com')", validate_email("test@example.com")),
        ("validate_email('invalid')", validate_email("invalid")),
        ("validate_url('https://example.com')", validate_url("https://example.com")),
        ("validate_phone('13812345678')", validate_phone("13812345678")),
        ("validate_ipv4('192.168.1.1')", validate_ipv4("192.168.1.1")),
        ("validate_ipv6('::1')", validate_ipv6("::1")),
        ("validate_date('2024-01-15')", validate_date("2024-01-15")),
        ("validate_range(5, 0, 10)", validate_range(5, 0, 10)),
        ("validate_range(15, 0, 10)", validate_range(15, 0, 10)),
    ]
    
    for code, result in checks:
        status = "✓" if result else "✗"
        print(f"  {status} {code} = {result}")


# ============================================================================
# Example 13: Real-World Use Case - API Request Validation
# ============================================================================
def example_api_validation():
    print_section("Example 13: Real-World Use Case - API Request Validation")
    
    def validate_api_request(params: dict) -> tuple:
        """Validate API request parameters"""
        validator = Validator()
        validator.rule('page', optional(lambda v, f: in_range(v, 1, 1000, f)))
        validator.rule('per_page', optional(lambda v, f: in_range(v, 1, 100, f)))
        validator.rule('search', optional(lambda v, f: has_length(v, 0, 100, f) if v else ValidationResult(True, v)))
        validator.rule('sort_by', optional(lambda v, f: is_in(v, ['created', 'updated', 'name'], f) if v else ValidationResult(True, v)))
        
        result = validator.validate(params)
        return result.is_valid, validator.get_errors()
    
    # Valid request
    print("\nValid API request:")
    valid_request = {
        'page': 5,
        'per_page': 20,
        'search': 'python',
        'sort_by': 'created',
    }
    
    is_valid, errors = validate_api_request(valid_request)
    print(f"  Valid: {is_valid}")
    if errors:
        print(f"  Errors: {errors}")
    
    # Invalid request
    print("\nInvalid API request:")
    invalid_request = {
        'page': 0,  # Out of range
        'per_page': 200,  # Out of range
        'sort_by': 'invalid_field',
    }
    
    is_valid, errors = validate_api_request(invalid_request)
    print(f"  Valid: {is_valid}")
    print(f"  Errors:")
    for field, error in errors.items():
        print(f"    - {field}: {error}")


# ============================================================================
# Main
# ============================================================================
def main():
    print("=" * 70)
    print("  AllToolkit - Validation Utilities Usage Examples")
    print("=" * 70)
    
    example_basic_validation()
    example_email_url()
    example_phone_validation()
    example_chinese_id()
    example_credit_card()
    example_ip_validation()
    example_datetime_validation()
    example_number_validation()
    example_string_validation()
    example_composite_validators()
    example_batch_validation()
    example_convenience_functions()
    example_api_validation()
    
    print("\n" + "=" * 70)
    print("  All examples completed!")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
