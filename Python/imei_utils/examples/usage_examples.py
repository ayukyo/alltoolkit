"""
IMEI Utilities - Usage Examples

This file demonstrates the key features of the IMEI utilities module.

Run with: python usage_examples.py
"""

import sys
sys.path.insert(0, '..')
from mod import (
    validate, parse, format_imei, generate_random, generate_batch,
    calculate_check_digit, get_tac_info, compare_imei, extract_digits,
    IMEIValidator
)


def print_section(title):
    """Print a section header."""
    print(f"\n{'=' * 50}")
    print(f" {title}")
    print('=' * 50)


def example_validation():
    """Demonstrate IMEI validation."""
    print_section("IMEI Validation")
    
    # Valid IMEI (verified correct)
    imei = "490154203237518"
    print(f"Validating '{imei}':")
    print(f"  Result: {validate(imei)}")
    print()
    
    # IMEI with separators
    imei_formatted = "49-015420-323751-8"
    print(f"Validating '{imei_formatted}' (with separators):")
    print(f"  Result: {validate(imei_formatted)}")
    print()
    
    # Invalid IMEI (wrong check digit)
    imei_invalid = "490154203237519"
    print(f"Validating '{imei_invalid}' (wrong check digit):")
    print(f"  Result: {validate(imei_invalid)}")


def example_parsing():
    """Demonstrate IMEI parsing."""
    print_section("IMEI Parsing")
    
    imei = "490154203237518"
    result = parse(imei)
    
    print(f"Parsing '{imei}':")
    print(f"  TAC (Type Allocation Code): {result['tac']}")
    print(f"  SNR (Serial Number): {result['snr']}")
    print(f"  Check Digit: {result['cd']}")
    print(f"  Valid: {result['valid']}")


def example_formatting():
    """Demonstrate IMEI formatting."""
    print_section("IMEI Formatting")
    
    imei = "490154203237518"
    
    print(f"Original: {imei}")
    print(f"Standard: {format_imei(imei, 'standard')}")
    print(f"Dashed:   {format_imei(imei, 'dashed')}")
    print(f"Compact:  {format_imei(imei, 'compact')}")
    print(f"Spaced:   {format_imei(imei, 'spaced')}")


def example_generation():
    """Demonstrate IMEI generation."""
    print_section("IMEI Generation")
    
    # Random IMEI
    print("Generating random IMEI:")
    imei = generate_random()
    print(f"  Generated: {imei}")
    print(f"  Valid: {validate(imei)}")
    print()
    
    # With specific TAC
    print("Generating IMEI with specific TAC (35209900):")
    imei = generate_random("35209900")
    print(f"  Generated: {imei}")
    print(f"  Starts with TAC: {imei.startswith('35209900')}")
    print()
    
    # Batch generation
    print("Generating batch of 5 IMEIs:")
    imeis = generate_batch(5)
    for i, imei in enumerate(imeis, 1):
        print(f"  {i}. {imei}")


def example_check_digit():
    """Demonstrate check digit calculation."""
    print_section("Check Digit Calculation")
    
    imei14 = "49015420323751"
    cd = calculate_check_digit(imei14)
    
    print(f"IMEI body (14 digits): {imei14}")
    print(f"Calculated check digit: {cd}")
    print(f"Complete IMEI: {imei14}{cd}")


def example_tac_info():
    """Demonstrate TAC information lookup."""
    print_section("TAC Information")
    
    tac = "49015420"
    info = get_tac_info(tac)
    
    print(f"TAC: {tac}")
    print(f"  Reporting Body Identifier: {info['reporting_body_identifier']}")
    print(f"  Type: {info['type']}")


def example_comparison():
    """Demonstrate IMEI comparison."""
    print_section("IMEI Comparison")
    
    imei1 = "490154203237518"
    imei2 = "490154203237518"
    imei3 = "490154203237519"  # Invalid (wrong check digit)
    
    print(f"Comparing '{imei1}' and '{imei2}':")
    result = compare_imei(imei1, imei2)
    print(f"  Match: {result['match']}")
    print(f"  Same TAC: {result['same_tac']}")
    print(f"  Same SNR: {result['same_snr']}")
    print()
    
    print(f"Comparing '{imei1}' and '{imei3}':")
    result = compare_imei(imei1, imei3)
    print(f"  Match: {result['match']}")
    print(f"  Same TAC: {result['same_tac']}")
    print(f"  Same SNR: {result['same_snr']}")
    print(f"  First valid: {result['valid1']}")
    print(f"  Second valid: {result['valid2']}")


def example_extraction():
    """Demonstrate IMEI extraction from text."""
    print_section("IMEI Extraction")
    
    # Generate valid IMEIs for extraction
    imei1 = "490154203237518"
    imei2 = generate_random("12345678")
    
    text = f"""
    Device Information:
    - Model: Smartphone X
    - IMEI 1: {imei1}
    - IMEI 2: {imei2}
    - Serial: ABC123
    
    Some other number: 123456789012345 (invalid check digit)
    """
    
    print("Extracting IMEIs from text:")
    print(text)
    imeis = extract_digits(text)
    print(f"Found {len(imeis)} valid IMEI(s):")
    for imei in imeis:
        print(f"  - {imei}")


def example_validator_class():
    """Demonstrate the IMEIValidator class."""
    print_section("IMEIValidator Class")
    
    imei = "490154203237518"
    validator = IMEIValidator(imei)
    
    print(f"Creating validator for '{imei}':")
    print(f"  Is valid: {validator.is_valid}")
    print(f"  TAC: {validator.tac}")
    print(f"  SNR: {validator.snr}")
    print(f"  Check digit: {validator.check_digit}")
    print(f"  Formatted (standard): {validator.format('standard')}")
    print(f"  String representation: {str(validator)}")
    print(f"  Repr: {repr(validator)}")
    print()
    
    # Invalid IMEI
    print("Testing invalid IMEI:")
    bad_validator = IMEIValidator("12345")
    print(f"  Is valid: {bad_validator.is_valid}")
    print(f"  TAC: {bad_validator.tac}")


def example_real_world_scenario():
    """Demonstrate a real-world use case."""
    print_section("Real-World Scenario: Device Registration")
    
    print("Scenario: Validating device IMEIs for registration\n")
    
    # Generate a valid IMEI for demonstration
    valid_imei = generate_random("35209900")
    
    # Simulating device registration
    device_data = [
        {"name": "Phone A", "imei": "49-015420-323751-8"},
        {"name": "Phone B", "imei": "490154203237519"},  # Invalid
        {"name": "Phone C", "imei": valid_imei},
    ]
    
    print("Processing devices:")
    for device in device_data:
        validator = IMEIValidator(device['imei'])
        status = "✓ Valid" if validator.is_valid else "✗ Invalid"
        print(f"\n{device['name']}:")
        print(f"  IMEI: {device['imei']}")
        print(f"  Status: {status}")
        
        if validator.is_valid:
            print(f"  TAC: {validator.tac}")
            print(f"  Formatted: {validator.format('standard')}")
        else:
            # Try to fix by recalculating check digit
            clean = str(validator)
            if len(clean) >= 14:
                correct_cd = calculate_check_digit(clean[:14])
                corrected = clean[:14] + str(correct_cd)
                print(f"  Suggested correction: {corrected}")


if __name__ == "__main__":
    print("=" * 60)
    print("        IMEI UTILITIES - USAGE EXAMPLES")
    print("=" * 60)
    
    example_validation()
    example_parsing()
    example_formatting()
    example_generation()
    example_check_digit()
    example_tac_info()
    example_comparison()
    example_extraction()
    example_validator_class()
    example_real_world_scenario()
    
    print("\n" + "=" * 60)
    print("        All examples completed!")
    print("=" * 60)