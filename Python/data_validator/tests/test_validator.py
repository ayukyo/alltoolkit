"""
Tests for Data Validator module.
Run with: python -m pytest tests/test_validator.py -v
Or with: python tests/test_validator.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Field, Schema, ValidationResult, ValidationError,
    Validators, validate, validate_field,
    is_valid_email, is_valid_url, is_valid_phone, is_valid_uuid, is_valid_ipv4
)


def test_required_field():
    """Test required field validation."""
    field = Field(field_type=str, required=True)
    
    # Missing required field should fail
    result = field.validate(None, "name")
    assert not result.is_valid
    assert len(result.errors) == 1
    assert "required" in result.errors[0].message.lower()
    
    # Provided field should pass
    result = field.validate("John", "name")
    assert result.is_valid


def test_optional_field():
    """Test optional field validation."""
    field = Field(field_type=str, required=False)
    
    result = field.validate(None, "nickname")
    assert result.is_valid


def test_type_validation():
    """Test type checking."""
    field = Field(field_type=int)
    
    assert field.validate(42, "age").is_valid
    assert field.validate(-10, "age").is_valid
    
    result = field.validate("42", "age")
    assert not result.is_valid
    assert "type" in result.errors[0].rule


def test_int_as_float():
    """Test that int is accepted when float is expected."""
    field = Field(field_type=float)
    
    assert field.validate(3.14, "price").is_valid
    assert field.validate(42, "price").is_valid  # int accepted for float


def test_min_max_values():
    """Test min/max value constraints."""
    field = Field(field_type=int, min_value=0, max_value=100)
    
    assert field.validate(50, "score").is_valid
    assert field.validate(0, "score").is_valid
    assert field.validate(100, "score").is_valid
    
    assert not field.validate(-1, "score").is_valid
    assert not field.validate(101, "score").is_valid


def test_string_length():
    """Test string length constraints."""
    field = Field(field_type=str, min_length=3, max_length=10)
    
    assert field.validate("hello", "name").is_valid
    assert field.validate("abc", "name").is_valid
    
    assert not field.validate("ab", "name").is_valid
    assert not field.validate("abcdefghijk", "name").is_valid


def test_list_length():
    """Test list length constraints."""
    field = Field(field_type=list, min_length=1, max_length=3)
    
    assert field.validate([1], "items").is_valid
    assert field.validate([1, 2, 3], "items").is_valid
    
    assert not field.validate([], "items").is_valid
    assert not field.validate([1, 2, 3, 4], "items").is_valid


def test_regex_pattern():
    """Test regex pattern matching."""
    field = Field(field_type=str, pattern=r'^[A-Z]{2}\d{4}$')
    
    assert field.validate("AB1234", "code").is_valid
    assert field.validate("XY9999", "code").is_valid
    
    assert not field.validate("ab1234", "code").is_valid  # lowercase
    assert not field.validate("ABC123", "code").is_valid  # wrong format


def test_choices():
    """Test choices validation."""
    field = Field(field_type=str, choices=["red", "green", "blue"])
    
    assert field.validate("red", "color").is_valid
    assert field.validate("green", "color").is_valid
    
    assert not field.validate("yellow", "color").is_valid


def test_custom_validator():
    """Test custom validator function."""
    def is_even(value):
        return value % 2 == 0, "Value must be even"
    
    field = Field(field_type=int, custom_validator=is_even)
    
    assert field.validate(2, "number").is_valid
    assert field.validate(100, "number").is_valid
    
    result = field.validate(3, "number")
    assert not result.is_valid
    assert "even" in result.errors[0].message.lower()


def test_list_item_type():
    """Test validation of list item types."""
    field = Field(field_type=list, item_type=int)
    
    assert field.validate([1, 2, 3], "numbers").is_valid
    assert field.validate([], "numbers").is_valid
    
    result = field.validate([1, "two", 3], "numbers")
    assert not result.is_valid
    assert "[1]" in result.errors[0].field


def test_nested_schema():
    """Test nested object validation."""
    address_schema = Schema({
        "street": Field(field_type=str, required=True),
        "city": Field(field_type=str, required=True),
        "zip": Field(field_type=str, pattern=r'^\d{5}$')
    })
    
    user_schema = Schema({
        "name": Field(field_type=str, required=True),
        "address": Field(field_type=dict, nested_schema=address_schema)
    })
    
    valid_data = {
        "name": "John",
        "address": {
            "street": "123 Main St",
            "city": "Springfield",
            "zip": "12345"
        }
    }
    result = user_schema.validate(valid_data)
    assert result.is_valid
    
    invalid_data = {
        "name": "John",
        "address": {
            "street": "123 Main St",
            "city": "Springfield",
            "zip": "abcde"  # Invalid zip
        }
    }
    result = user_schema.validate(invalid_data)
    assert not result.is_valid
    assert "address" in result.errors[0].field


def test_schema_validation():
    """Test complete schema validation."""
    schema = Schema({
        "username": Field(field_type=str, required=True, min_length=3, max_length=20),
        "email": Field(field_type=str, required=True, custom_validator=Validators.email),
        "age": Field(field_type=int, required=False, min_value=0, max_value=150),
        "role": Field(field_type=str, choices=["admin", "user", "guest"], required=False, default="user")
    })
    
    valid_data = {
        "username": "johndoe",
        "email": "john@example.com",
        "age": 25
    }
    result = schema.validate(valid_data)
    assert result.is_valid
    assert result.data["role"] == "user"  # Default applied
    
    invalid_data = {
        "username": "jo",  # Too short
        "email": "invalid-email",
        "age": -5  # Negative
    }
    result = schema.validate(invalid_data)
    assert not result.is_valid
    assert len(result.errors) >= 3


def test_partial_validation():
    """Test partial validation (only validate provided fields)."""
    schema = Schema({
        "name": Field(field_type=str, required=True),
        "email": Field(field_type=str, required=True),
        "age": Field(field_type=int)
    })
    
    # Partial update - only email provided
    result = schema.validate_partial({"email": "new@example.com"})
    assert result.is_valid
    assert "email" in result.data
    assert "name" not in result.data


def test_validators_email():
    """Test email validator."""
    assert Validators.email("test@example.com")[0]
    assert Validators.email("user.name+tag@domain.co.uk")[0]
    assert not Validators.email("invalid")[0]
    assert not Validators.email("@domain.com")[0]
    assert not Validators.email("user@")[0]


def test_validators_url():
    """Test URL validator."""
    assert Validators.url("https://example.com")[0]
    assert Validators.url("http://test.org/path?query=1")[0]
    assert not Validators.url("not-a-url")[0]
    assert not Validators.url("ftp://invalid")[0]


def test_validators_phone():
    """Test phone validator."""
    assert Validators.phone("1234567890")[0]
    assert Validators.phone("+1-234-567-8900")[0]
    assert Validators.phone("(123) 456-7890")[0]
    assert not Validators.phone("123")[0]  # Too short
    assert not Validators.phone("abcdefghij")[0]  # Non-digits


def test_validators_uuid():
    """Test UUID validator."""
    assert Validators.uuid("123e4567-e89b-12d3-a456-426614174000")[0]
    assert Validators.uuid("123E4567-E89B-12D3-A456-426614174000")[0]  # Uppercase
    assert not Validators.uuid("not-a-uuid")[0]
    assert not Validators.uuid("123e4567-e89b-12d3-a456")[0]  # Too short


def test_validators_ipv4():
    """Test IPv4 validator."""
    assert Validators.ipv4("192.168.1.1")[0]
    assert Validators.ipv4("0.0.0.0")[0]
    assert Validators.ipv4("255.255.255.255")[0]
    assert not Validators.ipv4("256.1.1.1")[0]  # Invalid octet
    assert not Validators.ipv4("1.2.3")[0]  # Missing octet
    assert not Validators.ipv4("1.2.3.4.5")[0]  # Too many


def test_validators_date():
    """Test date validators."""
    assert Validators.date_iso("2024-01-15")[0]
    assert not Validators.date_iso("2024-13-01")[0]  # Invalid month
    assert not Validators.date_iso("2024-01-32")[0]  # Invalid day
    assert not Validators.date_iso("01-15-2024")[0]  # Wrong format


def test_validators_datetime():
    """Test datetime validator."""
    assert Validators.datetime_iso("2024-01-15T10:30:00")[0]
    assert Validators.datetime_iso("2024-01-15T10:30:00Z")[0]
    assert Validators.datetime_iso("2024-01-15 10:30:00")[0]
    assert not Validators.datetime_iso("invalid")[0]


def test_validators_hex_color():
    """Test hex color validator."""
    assert Validators.hex_color("#fff")[0]
    assert Validators.hex_color("#ffffff")[0]
    assert Validators.hex_color("#ABC123")[0]
    assert not Validators.hex_color("ffffff")[0]  # Missing #
    assert not Validators.hex_color("#ffff")[0]  # Wrong length


def test_validators_port():
    """Test port validator."""
    assert Validators.port(80)[0]
    assert Validators.port(443)[0]
    assert Validators.port(8080)[0]
    assert Validators.port(0)[0]
    assert Validators.port(65535)[0]
    assert not Validators.port(-1)[0]
    assert not Validators.port(65536)[0]


def test_password_strength_validator():
    """Test password strength validator."""
    # Only length requirement (uppercase/lower/digit are True by default, so need to include them)
    validator = Validators.password_strength(min_length=8, require_upper=False, require_digit=False)
    
    assert validator("password")[0]  # lowercase only, 8 chars
    assert not validator("short")[0]  # too short
    
    # Test with default requirements (upper, lower, digit)
    default_validator = Validators.password_strength(min_length=8)
    assert default_validator("Password123")[0]
    assert not default_validator("password")[0]  # no uppercase
    
    strict_validator = Validators.password_strength(
        min_length=12, require_upper=True, require_lower=True,
        require_digit=True, require_special=True
    )
    
    assert strict_validator("MyP@ssw0rd!X")[0]
    assert not strict_validator("no_uppercase!")[0]
    assert not strict_validator("NO_LOWERCASE1!")[0]
    assert not strict_validator("NoDigits!")[0]
    assert not strict_validator("NoSpecial123")[0]


def test_range_validator():
    """Test range validator factory."""
    validator = Validators.in_range(0, 100)
    
    assert validator(50)[0]
    assert validator(0)[0]
    assert validator(100)[0]
    assert not validator(-1)[0]
    assert not validator(101)[0]


def test_length_validator():
    """Test length validator factory."""
    validator = Validators.length(min_len=3, max_len=10)
    
    assert validator("hello")[0]
    assert validator("abc")[0]
    assert not validator("ab")[0]
    assert not validator("abcdefghijk")[0]


def test_default_values():
    """Test default value assignment."""
    schema = Schema({
        "name": Field(field_type=str, required=True),
        "role": Field(field_type=str, required=False, default="guest"),
        "active": Field(field_type=bool, required=False, default=True)
    })
    
    result = schema.validate({"name": "John"})
    assert result.is_valid
    assert result.data["role"] == "guest"
    assert result.data["active"] == True


def test_quick_helpers():
    """Test quick validation helper functions."""
    assert is_valid_email("test@example.com")
    assert is_valid_url("https://example.com")
    assert is_valid_phone("1234567890")
    assert is_valid_uuid("123e4567-e89b-12d3-a456-426614174000")
    assert is_valid_ipv4("192.168.1.1")


def test_validation_result_to_dict():
    """Test ValidationResult serialization."""
    result = ValidationResult(is_valid=False)
    result.add_error("field1", "Error 1", "value1", "rule1")
    
    d = result.to_dict()
    assert d["is_valid"] == False
    assert len(d["errors"]) == 1
    assert d["errors"][0]["field"] == "field1"
    assert d["errors"][0]["message"] == "Error 1"


def test_validation_error_str():
    """Test ValidationError string representation."""
    error = ValidationError("email", "Invalid format", "bad-email", "email")
    assert str(error) == "[email] Invalid format"


def test_schema_add_field():
    """Test adding fields to schema."""
    schema = Schema()
    schema.add_field("name", Field(field_type=str, required=True))
    schema.add_field("age", Field(field_type=int, min_value=0))
    
    result = schema.validate({"name": "John", "age": 25})
    assert result.is_valid


def run_all_tests():
    """Run all tests and print results."""
    tests = [
        test_required_field,
        test_optional_field,
        test_type_validation,
        test_int_as_float,
        test_min_max_values,
        test_string_length,
        test_list_length,
        test_regex_pattern,
        test_choices,
        test_custom_validator,
        test_list_item_type,
        test_nested_schema,
        test_schema_validation,
        test_partial_validation,
        test_validators_email,
        test_validators_url,
        test_validators_phone,
        test_validators_uuid,
        test_validators_ipv4,
        test_validators_date,
        test_validators_datetime,
        test_validators_hex_color,
        test_validators_port,
        test_password_strength_validator,
        test_range_validator,
        test_length_validator,
        test_default_values,
        test_quick_helpers,
        test_validation_result_to_dict,
        test_validation_error_str,
        test_schema_add_field,
    ]
    
    passed = 0
    failed = 0
    
    print(f"\n{'='*60}")
    print(f"Running {len(tests)} tests...")
    print(f"{'='*60}\n")
    
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"💥 {test.__name__}: {type(e).__name__}: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print(f"{'='*60}\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)