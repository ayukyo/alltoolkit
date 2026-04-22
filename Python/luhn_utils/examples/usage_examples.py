"""
Luhn Algorithm Utilities - Usage Examples
========================================

This file demonstrates various use cases for the luhn_utils module.

Run from the Python directory:
    cd Python && python luhn_utils/examples/usage_examples.py
"""

import sys
import os

# Ensure we can import from the Python directory
_parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# Now import from the correct path
try:
    from luhn_utils.mod import (
        validate,
        calculate_check_digit,
        add_check_digit,
        strip_formatting,
        format_number,
        generate_valid_number,
        generate_test_credit_cards,
        find_check_digit_errors,
        calculate_luhn_sum,
        LuhnValidator,
        identify_card_type,
    )
except ImportError:
    # Fallback for direct execution
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from mod import (
        validate,
        calculate_check_digit,
        add_check_digit,
        strip_formatting,
        format_number,
        generate_valid_number,
        generate_test_credit_cards,
        find_check_digit_errors,
        calculate_luhn_sum,
        LuhnValidator,
        identify_card_type,
    )


def example_1_basic_validation():
    """Example 1: Basic credit card validation."""
    print("=" * 60)
    print("Example 1: Basic Credit Card Validation")
    print("=" * 60)
    
    test_cards = [
        ("Visa", "4532015112830366"),
        ("MasterCard", "5500000000000004"),
        ("Amex", "378282246310005"),
        ("Discover", "6011111111111117"),
        ("Invalid Card", "4532015112830367"),
        ("With Formatting", "4532-0151-1283-0366"),
    ]
    
    for name, number in test_cards:
        is_valid = validate(number)
        status = "✓ Valid" if is_valid else "✗ Invalid"
        print(f"  {name}: {number} -> {status}")
    print()


def example_2_check_digit_calculation():
    """Example 2: Calculate and add check digits."""
    print("=" * 60)
    print("Example 2: Check Digit Calculation")
    print("=" * 60)
    
    partial_numbers = [
        "453201511283036",  # Visa prefix
        "550000000000000",  # MasterCard prefix
        "37828224631000",   # Amex prefix
    ]
    
    for partial in partial_numbers:
        check_digit = calculate_check_digit(partial)
        full_number = add_check_digit(partial)
        is_valid = validate(full_number)
        
        print(f"  Partial: {partial}")
        print(f"  Check Digit: {check_digit}")
        print(f"  Full Number: {full_number}")
        print(f"  Valid: {is_valid}")
        print()


def example_3_formatting():
    """Example 3: Format and parse card numbers."""
    print("=" * 60)
    print("Example 3: Number Formatting")
    print("=" * 60)
    
    number = "4532015112830366"
    
    print(f"  Original: {number}")
    print(f"  Default formatting: {format_number(number)}")
    print(f"  With dashes: {format_number(number, separator='-')}")
    print(f"  With dots: {format_number(number, separator='.')}")
    print(f"  Groups of 2: {format_number(number, group_size=2)}")
    print()
    
    # Strip formatting
    formatted = "4532-0151-1283-0366"
    stripped = strip_formatting(formatted)
    print(f"  Stripped '{formatted}' -> '{stripped}'")
    print()


def example_4_generate_test_cards():
    """Example 4: Generate test credit card numbers."""
    print("=" * 60)
    print("Example 4: Generate Test Credit Card Numbers")
    print("=" * 60)
    
    # Generate single numbers
    print("  Single Numbers:")
    visa = generate_valid_number("4", 16)
    mc = generate_valid_number("55", 16)
    amex = generate_valid_number("34", 15)
    
    print(f"    Visa: {visa} (valid: {validate(visa)})")
    print(f"    MasterCard: {mc} (valid: {validate(mc)})")
    print(f"    Amex: {amex} (valid: {validate(amex)})")
    print()
    
    # Generate multiple cards
    print("  Batch Generation (10 Visa numbers):")
    visa_numbers = [generate_valid_number("4", 16) for _ in range(10)]
    for i, num in enumerate(visa_numbers, 1):
        print(f"    {i}. {num}")
    print()


def example_5_card_type_detection():
    """Example 5: Identify card types."""
    print("=" * 60)
    print("Example 5: Card Type Identification")
    print("=" * 60)
    
    test_numbers = [
        ("4111111111111111", "Known Visa"),
        ("5500000000000004", "Known MasterCard"),
        ("378282246310005", "Known Amex"),
        ("6011111111111117", "Known Discover"),
        ("3530111333300000", "Known JCB"),
        ("30569309025904", "Known Diners"),
        ("6225881234567890", "Known UnionPay"),
    ]
    
    for number, description in test_numbers:
        card_type = identify_card_type(number)
        print(f"  {description}: {number} -> {card_type}")
    print()


def example_6_class_based_validator():
    """Example 6: Using the LuhnValidator class."""
    print("=" * 60)
    print("Example 6: LuhnValidator Class")
    print("=" * 60)
    
    # Create validator with default settings
    validator = LuhnValidator()
    
    # Validate
    number = "4532015112830366"
    print(f"  Validate '{number}': {validator.validate(number)}")
    
    # Generate
    generated = validator.generate("4", 16)
    print(f"  Generated Visa: {generated}")
    
    # Format
    formatted = validator.format(generated)
    print(f"  Formatted: {formatted}")
    
    # Strip
    stripped = validator.strip(formatted)
    print(f"  Stripped back: {stripped}")
    
    # Batch generation
    print("\n  Batch Generation (5 cards):")
    batch = validator.generate_batch("4", 5, 16)
    for i, num in enumerate(batch, 1):
        print(f"    {i}. {num}")
    print()


def example_7_error_detection():
    """Example 7: Find potential digit errors."""
    print("=" * 60)
    print("Example 7: Error Detection")
    print("=" * 60)
    
    # Valid number
    valid = "4532015112830366"
    errors = find_check_digit_errors(valid)
    print(f"  Valid number '{valid}':")
    print(f"    Error positions: {errors if errors else 'None (valid)'}")
    print()
    
    # Invalid number (typo in last digit)
    invalid = "4532015112830367"
    errors = find_check_digit_errors(invalid)
    print(f"  Invalid number '{invalid}':")
    print(f"    Potential error positions: {errors}")
    
    # Show what the digit at error position is
    if errors:
        pos = errors[0]
        print(f"    Digit at position {pos}: {invalid[pos]}")
    print()


def example_8_luhn_sum_debug():
    """Example 8: Debug Luhn calculation."""
    print("=" * 60)
    print("Example 8: Luhn Sum Debugging")
    print("=" * 60)
    
    numbers = [
        "4532015112830366",  # Valid Visa
        "4532015112830367",  # Invalid
        "0000000000000000",  # All zeros
    ]
    
    for number in numbers:
        total, is_valid = calculate_luhn_sum(number)
        status = "Valid" if is_valid else "Invalid"
        print(f"  {number}")
        print(f"    Sum: {total}")
        print(f"    Sum % 10: {total % 10}")
        print(f"    Status: {status}")
        print()


def example_9_test_card_generation():
    """Example 9: Generate test cards for various types."""
    print("=" * 60)
    print("Example 9: Test Card Generation by Type")
    print("=" * 60)
    
    cards = generate_test_credit_cards(count=2)
    
    # Group by card type
    by_type = {}
    for card_type, number in cards:
        if card_type not in by_type:
            by_type[card_type] = []
        by_type[card_type].append(number)
    
    for card_type, numbers in sorted(by_type.items()):
        print(f"  {card_type}:")
        for num in numbers:
            formatted = format_number(num)
            is_valid = validate(num)
            print(f"    {formatted} {'✓' if is_valid else '✗'}")
    print()


def example_10_imei_validation():
    """Example 10: IMEI number validation."""
    print("=" * 60)
    print("Example 10: IMEI Number Validation")
    print("=" * 60)
    
    # IMEI numbers also use Luhn algorithm
    # IMEI is 15 digits, IMEISV is 16 digits
    
    # Generate a test IMEI number
    # Standard IMEI reporting body identifier starts
    imei_prefixes = ["35", "01", "44"]  # Common TAC prefixes
    
    print("  Generating test IMEI numbers:")
    for prefix in imei_prefixes:
        imei = generate_valid_number(prefix, 15)
        print(f"    Prefix {prefix}: {imei} (valid: {validate(imei)})")
    
    # Known valid IMEI for testing (from GSMA)
    # These are example/test IMEI numbers
    print("\n  Note: IMEI numbers use the same Luhn algorithm")
    print("  Real IMEI validation should also check TAC in GSMA database")
    print()


def main():
    """Run all examples."""
    print()
    print("=" * 60)
    print("LUHN ALGORITHM UTILITIES - USAGE EXAMPLES")
    print("=" * 60)
    print()
    
    example_1_basic_validation()
    example_2_check_digit_calculation()
    example_3_formatting()
    example_4_generate_test_cards()
    example_5_card_type_detection()
    example_6_class_based_validator()
    example_7_error_detection()
    example_8_luhn_sum_debug()
    example_9_test_card_generation()
    example_10_imei_validation()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()