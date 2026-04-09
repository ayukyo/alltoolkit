#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Validation Utilities Test Suite
=============================================
Comprehensive test suite for the validation_utils module.
Covers normal cases, edge cases, and error conditions.

Run: python validation_utils_test.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Result types
    ValidationResult,
    ValidationError,
    
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
    Validator,
    
    # Convenience functions
    validate_email, validate_url, validate_phone, validate_credit_card,
    validate_chinese_id, validate_ipv4, validate_ipv6, validate_date,
    validate_range,
)


class TestRunner:
    """Simple test runner for validation tests."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self._current_section = ""
    
    def section(self, name: str):
        """Start a new test section."""
        self._current_section = name
        print(f"\n{name}")
        print("=" * 60)
    
    def test(self, name: str, condition: bool, details: str = ""):
        """Run a single test."""
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            msg = f"  ✗ {name}"
            if details:
                msg += f" - {details}"
            print(msg)
    
    def report(self) -> bool:
        """Print test report and return success status."""
        total = self.passed + self.failed
        print(f"\n{'=' * 60}")
        print(f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}")
        if self.failed == 0:
            print("🎉 All tests passed!")
        else:
            print(f"⚠️  {self.failed} test(s) failed.")
        print('=' * 60)
        return self.failed == 0


def run_tests():
    """Run all validation tests."""
    runner = TestRunner()
    
    # =========================================================================
    # ValidationResult Tests
    # =========================================================================
    runner.section("ValidationResult Tests")
    
    result = ValidationResult(True, "test_value")
    runner.test("Valid result is truthy", bool(result))
    runner.test("Valid result has correct value", result.value == "test_value")
    runner.test("Valid result error is None", result.error is None)
    
    result = ValidationResult(False, "bad_value", error="Invalid!")
    runner.test("Invalid result is falsy", not bool(result))
    runner.test("Invalid result has error message", result.error == "Invalid!")
    runner.test("Invalid result to_dict works", result.to_dict()['valid'] == False)
    
    # =========================================================================
    # Basic Validators Tests
    # =========================================================================
    runner.section("Basic Validators Tests")
    
    # is_not_none
    runner.test("is_not_none accepts value", is_not_none(42).is_valid)
    runner.test("is_not_none rejects None", not is_not_none(None).is_valid)
    runner.test("is_not_none accepts empty string", is_not_none("").is_valid)
    
    # is_not_empty
    runner.test("is_not_empty accepts non-empty", is_not_empty("hello").is_valid)
    runner.test("is_not_empty rejects empty string", not is_not_empty("").is_valid)
    runner.test("is_not_empty rejects empty list", not is_not_empty([]).is_valid)
    runner.test("is_not_empty rejects None", not is_not_empty(None).is_valid)
    runner.test("is_not_empty accepts zero", is_not_empty(0).is_valid)
    
    # is_type
    runner.test("is_type accepts correct type", is_type(42, int).is_valid)
    runner.test("is_type rejects wrong type", not is_type("42", int).is_valid)
    runner.test("is_type accepts float", is_type(3.14, float).is_valid)
    runner.test("is_type accepts list", is_type([1, 2], list).is_valid)
    
    # is_in
    runner.test("is_in accepts valid choice", is_in("a", ["a", "b", "c"]).is_valid)
    runner.test("is_in rejects invalid choice", not is_in("d", ["a", "b", "c"]).is_valid)
    runner.test("is_in accepts number in range", is_in(2, [1, 2, 3]).is_valid)
    
    # =========================================================================
    # Email Validation Tests
    # =========================================================================
    runner.section("Email Validation Tests")
    
    valid_emails = [
        "test@example.com",
        "user.name@domain.co.uk",
        "user+tag@example.org",
        "user123@test-domain.com",
        "a@b.co",
    ]
    for email in valid_emails:
        runner.test(f"is_email accepts {email}", is_email(email).is_valid)
    
    invalid_emails = [
        "invalid",
        "@example.com",
        "user@",
        "user@domain",
        "user name@example.com",
        "",
        None,
        123,
    ]
    for email in invalid_emails:
        runner.test(f"is_email rejects {email!r}", not is_email(email).is_valid)
    
    # Convenience function
    runner.test("validate_email works", validate_email("test@example.com") == True)
    
    # =========================================================================
    # URL Validation Tests
    # =========================================================================
    runner.section("URL Validation Tests")
    
    valid_urls = [
        "https://example.com",
        "http://localhost",
        "https://sub.domain.com/path",
        "http://192.168.1.1:8080/api",
        "https://example.com/path?query=value&other=123",
    ]
    for url in valid_urls:
        runner.test(f"is_url accepts {url}", is_url(url).is_valid)
    
    invalid_urls = [
        "not-a-url",
        "ftp://example.com",  # Only http/https
        "example.com",  # Missing scheme
        "",
        None,
    ]
    for url in invalid_urls:
        runner.test(f"is_url rejects {url!r}", not is_url(url).is_valid)
    
    # Allowed schemes
    result = is_url("https://example.com", allowed_schemes=["https"])
    runner.test("is_url with https-only accepts https", result.is_valid)
    result = is_url("http://example.com", allowed_schemes=["https"])
    runner.test("is_url with https-only rejects http", not result.is_valid)
    
    runner.test("validate_url works", validate_url("https://example.com") == True)
    
    # =========================================================================
    # Phone Validation Tests
    # =========================================================================
    runner.section("Phone Validation Tests")
    
    # Chinese phones
    valid_cn = ["13812345678", "19912345678", "13 8123 4567 8", "138-1234-5678"]
    for phone in valid_cn:
        runner.test(f"is_phone CN accepts {phone}", is_phone(phone, 'CN').is_valid)
    
    invalid_cn = ["12345678901", "0812345678", "23812345678", ""]
    for phone in invalid_cn:
        runner.test(f"is_phone CN rejects {phone!r}", not is_phone(phone, 'CN').is_valid)
    
    # US phones
    valid_us = ["2125551234", "12125551234", "(212) 555-1234", "212-555-1234"]
    for phone in valid_us:
        runner.test(f"is_phone US accepts {phone}", is_phone(phone, 'US').is_valid)
    
    runner.test("validate_phone works", validate_phone("13812345678") == True)
    
    # =========================================================================
    # Chinese ID Validation Tests
    # =========================================================================
    runner.section("Chinese ID Validation Tests")
    
    # Valid ID (with correct check digit)
    valid_id = "11010519491231002X"
    runner.test("is_chinese_id accepts valid ID", is_chinese_id(valid_id).is_valid)
    
    # Test with different area code - use computed valid IDs
    runner.test("is_chinese_id accepts different area code", 
                is_chinese_id("310104198001010017").is_valid)
    
    invalid_ids = [
        "123456789012345678",  # Wrong format
        "11010519491231002A",  # Wrong check digit
        "01010519491231002X",  # Area code starts with 0
        "",
        None,
    ]
    for id_num in invalid_ids:
        runner.test(f"is_chinese_id rejects {id_num!r}", not is_chinese_id(id_num).is_valid)
    
    runner.test("validate_chinese_id works", validate_chinese_id(valid_id) == True)
    
    # =========================================================================
    # Credit Card Validation Tests
    # =========================================================================
    runner.section("Credit Card Validation Tests")
    
    # Valid cards (test numbers that pass Luhn)
    valid_visa = "4532015112830366"
    valid_mc = "5425233430109903"
    valid_amex = "374245455400126"
    
    runner.test("is_credit_card accepts Visa", is_credit_card(valid_visa, 'visa').is_valid)
    runner.test("is_credit_card accepts Mastercard", is_credit_card(valid_mc, 'mastercard').is_valid)
    runner.test("is_credit_card accepts Amex", is_credit_card(valid_amex, 'amex').is_valid)
    
    # Without type specification
    runner.test("is_credit_card without type", is_credit_card(valid_visa).is_valid)
    
    # Invalid cards
    runner.test("is_credit_card rejects wrong type", 
                not is_credit_card(valid_visa, 'amex').is_valid)
    runner.test("is_credit_card rejects bad number", 
                not is_credit_card("1234567890123456").is_valid)
    runner.test("is_credit_card rejects non-digits", 
                not is_credit_card("abcd1234567890ab").is_valid)
    
    runner.test("validate_credit_card works", validate_credit_card(valid_visa) == True)
    
    # =========================================================================
    # IP Address Validation Tests
    # =========================================================================
    runner.section("IP Address Validation Tests")
    
    # IPv4
    valid_ipv4 = ["192.168.1.1", "10.0.0.1", "255.255.255.255", "0.0.0.0"]
    for ip in valid_ipv4:
        runner.test(f"is_ipv4 accepts {ip}", is_ipv4(ip).is_valid)
    
    invalid_ipv4 = ["256.1.1.1", "192.168.1", "192.168.1.1.1", "abc.def.ghi.jkl"]
    for ip in invalid_ipv4:
        runner.test(f"is_ipv4 rejects {ip}", not is_ipv4(ip).is_valid)
    
    # IPv6
    valid_ipv6 = [
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "fe80:0000:0000:0000:0000:0000:0000:0001",
        "::1",
        "::",
    ]
    for ip in valid_ipv6:
        runner.test(f"is_ipv6 accepts {ip}", is_ipv6(ip).is_valid)
    
    invalid_ipv6 = ["2001:db8:::1", "gggg::1", ""]
    for ip in invalid_ipv6:
        runner.test(f"is_ipv6 rejects {ip}", not is_ipv6(ip).is_valid)
    
    # Generic is_ip
    runner.test("is_ip accepts IPv4", is_ip("192.168.1.1").is_valid)
    runner.test("is_ip accepts IPv6", is_ip("::1").is_valid)
    runner.test("is_ip version=4 accepts IPv4", is_ip("192.168.1.1", version=4).is_valid)
    runner.test("is_ip version=4 rejects IPv6", not is_ip("::1", version=4).is_valid)
    runner.test("is_ip version=6 accepts IPv6", is_ip("::1", version=6).is_valid)
    
    runner.test("validate_ipv4 works", validate_ipv4("192.168.1.1") == True)
    runner.test("validate_ipv6 works", validate_ipv6("::1") == True)
    
    # =========================================================================
    # Date/Time Validation Tests
    # =========================================================================
    runner.section("Date/Time Validation Tests")
    
    # Date
    valid_dates = ["2024-01-15", "2024-12-31", "2000-02-29"]  # 2000 is leap year
    for date_str in valid_dates:
        runner.test(f"is_date accepts {date_str}", is_date(date_str).is_valid)
    
    invalid_dates = [
        "2024-13-01",  # Invalid month
        "2024-02-30",  # Invalid day
        "2023-02-29",  # Not a leap year
        "24-01-15",    # Wrong format
        "",
    ]
    for date_str in invalid_dates:
        runner.test(f"is_date rejects {date_str}", not is_date(date_str).is_valid)
    
    # Different formats
    runner.test("is_date YYYY/MM/DD", is_date("2024/01/15", 'YYYY/MM/DD').is_valid)
    runner.test("is_date DD-MM-YYYY", is_date("15-01-2024", 'DD-MM-YYYY').is_valid)
    runner.test("is_date MM/DD/YYYY", is_date("01/15/2024", 'MM/DD/YYYY').is_valid)
    
    # Time
    valid_times = ["09:30", "23:59", "00:00", "12:30:45", "23:59:59.999"]
    runner.test("is_time HH:MM", is_time("09:30", 'HH:MM').is_valid)
    runner.test("is_time HH:MM:SS", is_time("12:30:45", 'HH:MM:SS').is_valid)
    runner.test("is_time HH:MM:SS.fff", is_time("12:30:45.123", 'HH:MM:SS.fff').is_valid)
    
    invalid_times = ["25:00", "12:60", "12:30:60", "9:30"]
    for time_str in invalid_times:
        runner.test(f"is_time rejects {time_str}", not is_time(time_str, 'HH:MM:SS').is_valid)
    
    # Datetime
    runner.test("is_datetime accepts valid", 
                is_datetime("2024-01-15 09:30:00").is_valid)
    runner.test("is_datetime rejects invalid", 
                not is_datetime("2024-13-45 25:61:61").is_valid)
    
    runner.test("validate_date works", validate_date("2024-01-15") == True)
    
    # =========================================================================
    # Number Validation Tests
    # =========================================================================
    runner.section("Number Validation Tests")
    
    # is_number
    runner.test("is_number accepts int", is_number(42).is_valid)
    runner.test("is_number accepts float", is_number(3.14).is_valid)
    runner.test("is_number rejects bool", not is_number(True).is_valid)
    runner.test("is_number rejects string", not is_number("42").is_valid)
    
    # is_integer
    runner.test("is_integer accepts int", is_integer(42).is_valid)
    runner.test("is_integer rejects float", not is_integer(3.14).is_valid)
    runner.test("is_integer rejects bool", not is_integer(True).is_valid)
    
    # in_range
    runner.test("in_range accepts within", in_range(5, 0, 10).is_valid)
    runner.test("in_range accepts boundary min", in_range(0, 0, 10).is_valid)
    runner.test("in_range accepts boundary max", in_range(10, 0, 10).is_valid)
    runner.test("in_range rejects below", not in_range(-1, 0, 10).is_valid)
    runner.test("in_range rejects above", not in_range(11, 0, 10).is_valid)
    runner.test("in_range no min", in_range(-100, max_val=10).is_valid)
    runner.test("in_range no max", in_range(100, min_val=0).is_valid)
    
    # is_positive
    runner.test("is_positive accepts positive", is_positive(1).is_valid)
    runner.test("is_positive rejects zero", not is_positive(0).is_valid)
    runner.test("is_positive rejects negative", not is_positive(-1).is_valid)
    
    # is_non_negative
    runner.test("is_non_negative accepts zero", is_non_negative(0).is_valid)
    runner.test("is_non_negative accepts positive", is_non_negative(1).is_valid)
    runner.test("is_non_negative rejects negative", not is_non_negative(-1).is_valid)
    
    runner.test("validate_range works", validate_range(5, 0, 10) == True)
    
    # =========================================================================
    # String Length Validation Tests
    # =========================================================================
    runner.section("String Length Validation Tests")
    
    # has_length
    runner.test("has_length accepts within", has_length("hello", 3, 10).is_valid)
    runner.test("has_length accepts min boundary", has_length("abc", 3, 10).is_valid)
    runner.test("has_length accepts max boundary", has_length("abcdefghij", 3, 10).is_valid)
    runner.test("has_length rejects too short", not has_length("ab", 3, 10).is_valid)
    runner.test("has_length rejects too long", not has_length("abcdefghijk", 3, 10).is_valid)
    runner.test("has_length no min", has_length("a", max_len=10).is_valid)
    runner.test("has_length no max", has_length("very long string", min_len=5).is_valid)
    
    # matches_pattern
    runner.test("matches_pattern accepts match", 
                matches_pattern("abc123", r'^[a-z]+\d+$').is_valid)
    runner.test("matches_pattern rejects non-match", 
                not matches_pattern("123abc", r'^[a-z]+\d+$').is_valid)
    runner.test("matches_pattern with compiled pattern", 
                matches_pattern("test", __import__('re').compile(r'^test$')).is_valid)
    
    # =========================================================================
    # Composite Validators Tests
    # =========================================================================
    runner.section("Composite Validators Tests")
    
    # all_of
    combined = all_of([
        lambda v, f: is_type(v, str, f),
        lambda v, f: has_length(v, 3, 10, f),
    ])
    runner.test("all_of accepts all pass", combined("hello").is_valid)
    runner.test("all_of rejects one fails", not combined("hi").is_valid)
    runner.test("all_of rejects type wrong", not combined(123).is_valid)
    
    # any_of
    either = any_of([
        lambda v, f: is_email(v, f),
        lambda v, f: is_phone(v, 'CN', f),
    ])
    runner.test("any_of accepts first", either("test@example.com").is_valid)
    runner.test("any_of accepts second", either("13812345678").is_valid)
    runner.test("any_of rejects neither", not either("invalid").is_valid)
    
    # optional
    opt_email = optional(is_email)
    runner.test("optional accepts None", opt_email(None).is_valid)
    runner.test("optional accepts valid", opt_email("test@example.com").is_valid)
    runner.test("optional rejects invalid", not opt_email("invalid").is_valid)
    
    # =========================================================================
    # Validator Class Tests
    # =========================================================================
    runner.section("Validator Class Tests")
    
    validator = Validator()
    validator.rule('email', is_email)
    validator.rule('age', lambda v, f: in_range(v, 0, 150, f))
    validator.rule('name', lambda v, f: has_length(v, 1, 50, f) if v else ValidationResult(False, v, error="Name required"))
    
    # Valid data
    valid_data = {'email': 'test@example.com', 'age': 25, 'name': 'John'}
    result = validator.validate(valid_data)
    runner.test("Validator accepts valid data", result.is_valid)
    runner.test("Validator valid data has no errors", len(validator.get_errors()) == 0)
    
    # Invalid data
    invalid_data = {'email': 'invalid', 'age': 200, 'name': ''}
    result = validator.validate(invalid_data)
    runner.test("Validator rejects invalid data", not result.is_valid)
    runner.test("Validator invalid data has errors", len(validator.get_errors()) > 0)
    runner.test("Validator catches email error", 'email' in validator.get_errors())
    runner.test("Validator catches age error", 'age' in validator.get_errors())
    
    # Strict mode
    extra_data = {'email': 'test@example.com', 'age': 25, 'name': 'John', 'unknown': 'field'}
    result = validator.validate(extra_data, strict=True)
    runner.test("Validator strict mode catches unknown", not result.is_valid)
    
    # Method chaining
    chained = Validator().rule('a', is_integer).rule('b', is_email)
    result = chained.validate({'a': 1, 'b': 'test@example.com'})
    runner.test("Validator method chaining works", result.is_valid)
    
    # raise_if_invalid
    try:
        validator.raise_if_invalid(invalid_data)
        runner.test("raise_if_invalid raises exception", False)
    except ValidationError as e:
        runner.test("raise_if_invalid raises exception", True)
        runner.test("ValidationError has value", e.value == invalid_data)
    
    # =========================================================================
    # Edge Cases and Error Handling
    # =========================================================================
    runner.section("Edge Cases and Error Handling Tests")
    
    # None handling
    runner.test("is_email handles None", not is_email(None).is_valid)
    runner.test("is_url handles None", not is_url(None).is_valid)
    runner.test("is_phone handles None", not is_phone(None).is_valid)
    runner.test("is_date handles None", not is_date(None).is_valid)
    runner.test("is_ipv4 handles None", not is_ipv4(None).is_valid)
    
    # Empty string handling
    runner.test("is_email handles empty", not is_email("").is_valid)
    runner.test("is_url handles empty", not is_url("").is_valid)
    
    # Type errors
    runner.test("is_email handles int", not is_email(123).is_valid)
    runner.test("is_url handles int", not is_url(123).is_valid)
    runner.test("is_phone handles int", not is_phone(123).is_valid)
    
    # Field name in errors
    result = is_email("invalid", field="user_email")
    runner.test("Error includes field name", "user_email" in result.error)
    
    # =========================================================================
    # Convenience Functions Tests
    # =========================================================================
    runner.section("Convenience Functions Tests")
    
    runner.test("validate_email True", validate_email("test@example.com") == True)
    runner.test("validate_email False", validate_email("invalid") == False)
    runner.test("validate_url True", validate_url("https://example.com") == True)
    runner.test("validate_url False", validate_url("not-url") == False)
    runner.test("validate_phone True", validate_phone("13812345678") == True)
    runner.test("validate_phone False", validate_phone("12345") == False)
    runner.test("validate_ipv4 True", validate_ipv4("192.168.1.1") == True)
    runner.test("validate_ipv4 False", validate_ipv4("256.1.1.1") == False)
    runner.test("validate_ipv6 True", validate_ipv6("::1") == True)
    runner.test("validate_ipv6 False", validate_ipv6("gggg::1") == False)
    runner.test("validate_date True", validate_date("2024-01-15") == True)
    runner.test("validate_date False", validate_date("2024-13-45") == False)
    runner.test("validate_range True", validate_range(5, 0, 10) == True)
    runner.test("validate_range False", validate_range(15, 0, 10) == False)
    
    # =========================================================================
    # Report
    # =========================================================================
    return runner.report()


if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Validation Utilities Test Suite")
    print("=" * 60)
    
    success = run_tests()
    sys.exit(0 if success else 1)
