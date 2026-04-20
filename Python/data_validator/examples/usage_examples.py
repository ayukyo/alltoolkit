"""
Data Validator - Usage Examples

This file demonstrates how to use the Data Validator module
for various validation scenarios.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Field, Schema, Validators, validate,
    is_valid_email, is_valid_url, is_valid_ipv4
)


def example_basic_usage():
    """Basic field and schema validation."""
    print("\n" + "="*60)
    print("Example 1: Basic Usage")
    print("="*60)
    
    # Define a simple schema
    user_schema = Schema({
        "username": Field(
            field_type=str,
            required=True,
            min_length=3,
            max_length=20
        ),
        "email": Field(
            field_type=str,
            required=True,
            custom_validator=Validators.email
        ),
        "age": Field(
            field_type=int,
            required=False,
            min_value=0,
            max_value=150
        )
    })
    
    # Valid data
    valid_user = {
        "username": "johndoe",
        "email": "john@example.com",
        "age": 25
    }
    result = user_schema.validate(valid_user)
    print(f"Valid user: {result.is_valid}")
    print(f"Data: {result.data}")
    
    # Invalid data
    invalid_user = {
        "username": "jo",  # Too short
        "email": "not-an-email",
        "age": -5  # Negative
    }
    result = user_schema.validate(invalid_user)
    print(f"\nInvalid user: {result.is_valid}")
    print("Errors:")
    for error in result.errors:
        print(f"  - {error}")


def example_nested_objects():
    """Validation with nested object schemas."""
    print("\n" + "="*60)
    print("Example 2: Nested Object Validation")
    print("="*60)
    
    # Define nested schema for address
    address_schema = Schema({
        "street": Field(field_type=str, required=True),
        "city": Field(field_type=str, required=True),
        "zipCode": Field(
            field_type=str,
            required=True,
            pattern=r'^\d{5}(-\d{4})?$'
        ),
        "country": Field(field_type=str, required=False, default="USA")
    })
    
    # Define main schema with nested address
    person_schema = Schema({
        "name": Field(field_type=str, required=True, min_length=1),
        "address": Field(
            field_type=dict,
            required=True,
            nested_schema=address_schema
        )
    })
    
    # Valid nested data
    valid_person = {
        "name": "John Doe",
        "address": {
            "street": "123 Main St",
            "city": "Springfield",
            "zipCode": "12345"
        }
    }
    result = person_schema.validate(valid_person)
    print(f"Valid person: {result.is_valid}")
    print(f"Country (default): {result.data['address']['country']}")
    
    # Invalid nested data
    invalid_person = {
        "name": "John Doe",
        "address": {
            "street": "123 Main St",
            "city": "Springfield",
            "zipCode": "invalid"  # Doesn't match pattern
        }
    }
    result = person_schema.validate(invalid_person)
    print(f"\nInvalid person: {result.is_valid}")
    print("Errors:")
    for error in result.errors:
        print(f"  - {error}")


def example_choices_and_patterns():
    """Using choices and regex patterns."""
    print("\n" + "="*60)
    print("Example 3: Choices and Patterns")
    print("="*60)
    
    product_schema = Schema({
        "sku": Field(
            field_type=str,
            required=True,
            pattern=r'^[A-Z]{3}-\d{6}$'  # e.g., "ABC-123456"
        ),
        "category": Field(
            field_type=str,
            required=True,
            choices=["electronics", "clothing", "food", "books"]
        ),
        "status": Field(
            field_type=str,
            required=False,
            choices=["draft", "published", "archived"],
            default="draft"
        )
    })
    
    # Valid product
    result = product_schema.validate({
        "sku": "ELC-123456",
        "category": "electronics"
    })
    print(f"Valid product: {result.is_valid}")
    print(f"Status (default): {result.data['status']}")
    
    # Invalid product
    result = product_schema.validate({
        "sku": "invalid-sku",
        "category": "furniture"  # Not in choices
    })
    print(f"\nInvalid product: {result.is_valid}")
    print("Errors:")
    for error in result.errors:
        print(f"  - {error}")


def example_list_validation():
    """Validating lists with item type checking."""
    print("\n" + "="*60)
    print("Example 4: List Validation")
    print("="*60)
    
    # Schema with list field
    team_schema = Schema({
        "name": Field(field_type=str, required=True),
        "members": Field(
            field_type=list,
            required=True,
            min_length=1,
            item_type=str
        ),
        "scores": Field(
            field_type=list,
            required=False,
            item_type=int
        )
    })
    
    # Valid team
    result = team_schema.validate({
        "name": "Alpha Team",
        "members": ["Alice", "Bob", "Charlie"],
        "scores": [95, 87, 92]
    })
    print(f"Valid team: {result.is_valid}")
    print(f"Members: {result.data['members']}")
    
    # Invalid team - wrong item types
    result = team_schema.validate({
        "name": "Beta Team",
        "members": ["Alice", 123, "Charlie"],  # 123 is not a string
        "scores": [95, "87", 92]  # "87" is not an int
    })
    print(f"\nInvalid team: {result.is_valid}")
    print("Errors:")
    for error in result.errors:
        print(f"  - {error}")


def example_custom_validators():
    """Creating and using custom validators."""
    print("\n" + "="*60)
    print("Example 5: Custom Validators")
    print("="*60)
    
    # Custom validator: must be a positive even number
    def positive_even(value):
        if value <= 0:
            return False, "Value must be positive"
        if value % 2 != 0:
            return False, "Value must be even"
        return True, ""
    
    # Custom validator: username must be alphanumeric and not taken
    taken_usernames = {"admin", "root", "system"}
    
    def available_username(value):
        if value.lower() in taken_usernames:
            return False, f"Username '{value}' is already taken"
        return True, ""
    
    # Custom validator: password confirmation
    def matches_password(get_password_func):
        def validator(value):
            if value != get_password_func():
                return False, "Passwords do not match"
            return True, ""
        return validator
    
    schema = Schema({
        "username": Field(
            field_type=str,
            required=True,
            custom_validator=available_username
        ),
        "lucky_number": Field(
            field_type=int,
            required=True,
            custom_validator=positive_even
        )
    })
    
    # Valid data
    result = schema.validate({
        "username": "newuser",
        "lucky_number": 42
    })
    print(f"Valid data: {result.is_valid}")
    
    # Invalid - taken username
    result = schema.validate({
        "username": "admin",
        "lucky_number": 42
    })
    print(f"\nInvalid (taken username): {result.is_valid}")
    print(f"Error: {result.errors[0]}")
    
    # Invalid - odd number
    result = schema.validate({
        "username": "newuser",
        "lucky_number": 7
    })
    print(f"\nInvalid (odd number): {result.is_valid}")
    print(f"Error: {result.errors[0]}")


def example_partial_validation():
    """Partial validation for updates/patches."""
    print("\n" + "="*60)
    print("Example 6: Partial Validation (for PATCH operations)")
    print("="*60)
    
    # Full user schema with many fields
    user_schema = Schema({
        "username": Field(field_type=str, required=True, min_length=3),
        "email": Field(field_type=str, required=True, custom_validator=Validators.email),
        "bio": Field(field_type=str, required=False, max_length=500),
        "website": Field(field_type=str, required=False, custom_validator=Validators.url),
        "age": Field(field_type=int, required=False, min_value=0)
    })
    
    # Full validation - all required fields needed
    print("Full validation (all required fields):")
    result = user_schema.validate({"email": "john@example.com"})
    print(f"  Valid: {result.is_valid}")
    print(f"  Errors: {result.error_messages()}")
    
    # Partial validation - only validate provided fields
    print("\nPartial validation (only provided fields):")
    result = user_schema.validate_partial({"email": "new@example.com"})
    print(f"  Valid: {result.is_valid}")
    print(f"  Data: {result.data}")
    
    # Partial validation with invalid data
    result = user_schema.validate_partial({"age": -5, "website": "not-a-url"})
    print(f"\nPartial with errors:")
    print(f"  Valid: {result.is_valid}")
    print(f"  Errors: {result.error_messages()}")


def example_quick_helpers():
    """Using quick validation helper functions."""
    print("\n" + "="*60)
    print("Example 7: Quick Validation Helpers")
    print("="*60)
    
    # Email validation
    emails = ["user@example.com", "invalid-email", "test@domain.co.uk"]
    print("Email validation:")
    for email in emails:
        print(f"  {email}: {is_valid_email(email)}")
    
    # URL validation
    urls = ["https://example.com", "not-a-url", "http://test.org/path"]
    print("\nURL validation:")
    for url in urls:
        print(f"  {url}: {is_valid_url(url)}")
    
    # IP validation
    ips = ["192.168.1.1", "256.1.1.1", "10.0.0.1"]
    print("\nIPv4 validation:")
    for ip in ips:
        print(f"  {ip}: {is_valid_ipv4(ip)}")


def example_complex_schema():
    """Complex real-world schema example."""
    print("\n" + "="*60)
    print("Example 8: Complex Schema (API Request Validation)")
    print("="*60)
    
    # Nested schema for address
    address_schema = Schema({
        "line1": Field(field_type=str, required=True, min_length=1),
        "line2": Field(field_type=str, required=False),
        "city": Field(field_type=str, required=True),
        "state": Field(field_type=str, required=True, min_length=2, max_length=2),
        "zip": Field(field_type=str, required=True, pattern=r'^\d{5}$'),
        "country": Field(field_type=str, required=False, default="US")
    })
    
    # Nested schema for items
    item_schema = Schema({
        "productId": Field(field_type=str, required=True),
        "name": Field(field_type=str, required=True),
        "quantity": Field(field_type=int, required=True, min_value=1),
        "price": Field(field_type=float, required=True, min_value=0)
    })
    
    # Main order schema
    order_schema = Schema({
        "orderId": Field(
            field_type=str,
            required=True,
            custom_validator=Validators.uuid
        ),
        "customer": Schema({
            "email": Field(field_type=str, required=True, custom_validator=Validators.email),
            "phone": Field(field_type=str, required=False, custom_validator=Validators.phone),
            "name": Field(field_type=str, required=True, min_length=1)
        }),
        "shippingAddress": Field(
            field_type=dict,
            required=True,
            nested_schema=address_schema
        ),
        "items": Field(
            field_type=list,
            required=True,
            min_length=1
        ),
        "total": Field(field_type=float, required=True, min_value=0),
        "status": Field(
            field_type=str,
            required=False,
            choices=["pending", "processing", "shipped", "delivered", "cancelled"],
            default="pending"
        )
    })
    
    # Valid order
    valid_order = {
        "orderId": "123e4567-e89b-12d3-a456-426614174000",
        "customer": {
            "email": "customer@example.com",
            "name": "Jane Doe"
        },
        "shippingAddress": {
            "line1": "123 Main St",
            "city": "Springfield",
            "state": "IL",
            "zip": "62701"
        },
        "items": [
            {"productId": "p1", "name": "Widget", "quantity": 2, "price": 9.99}
        ],
        "total": 19.98
    }
    
    result = order_schema.validate(valid_order)
    print(f"Valid order: {result.is_valid}")
    print(f"Status (default): {result.data.get('status')}")


def example_validation_result():
    """Working with ValidationResult objects."""
    print("\n" + "="*60)
    print("Example 9: Working with ValidationResult")
    print("="*60)
    
    schema = Schema({
        "name": Field(field_type=str, required=True, min_length=2),
        "email": Field(field_type=str, required=True, custom_validator=Validators.email),
        "age": Field(field_type=int, required=True, min_value=0, max_value=120)
    })
    
    result = schema.validate({
        "name": "J",  # Too short
        "email": "invalid",
        "age": 150  # Too old
    })
    
    print(f"Is valid: {result.is_valid}")
    print(f"\nError count: {len(result.errors)}")
    print("\nErrors as strings:")
    for msg in result.error_messages():
        print(f"  - {msg}")
    
    print("\nErrors as dict:")
    for error in result.errors:
        print(f"  {error.to_dict()}")
    
    print(f"\nFull result as dict:")
    import json
    print(json.dumps(result.to_dict(), indent=2))


def main():
    """Run all examples."""
    print("\n" + "#"*60)
    print("# Data Validator - Usage Examples")
    print("#"*60)
    
    example_basic_usage()
    example_nested_objects()
    example_choices_and_patterns()
    example_list_validation()
    example_custom_validators()
    example_partial_validation()
    example_quick_helpers()
    example_complex_schema()
    example_validation_result()
    
    print("\n" + "#"*60)
    print("# All examples completed!")
    print("#"*60 + "\n")


if __name__ == "__main__":
    main()