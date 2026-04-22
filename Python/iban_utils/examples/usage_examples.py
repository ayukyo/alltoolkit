"""
IBAN Utilities - Usage Examples
================================

Practical examples demonstrating IBAN validation, parsing, and generation.

Usage:
    python usage_examples.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    validate,
    parse,
    format_iban,
    strip_formatting,
    calculate_check_digits,
    get_country_info,
    get_supported_countries,
    generate_test_iban,
    generate_batch_test_ibans,
    extract_bank_info,
    IBANValidator,
    TEST_IBANS,
)


def example_basic_validation():
    """Basic IBAN validation."""
    print("\n" + "=" * 60)
    print("Example 1: Basic IBAN Validation")
    print("=" * 60)
    
    ibans = [
        "GB82WEST12345698765432",       # Valid UK IBAN
        "DE89370400440532013000",        # Valid German IBAN
        "FR1420041010050500013M02606",   # Valid French IBAN
        "GB82WEST12345698765433",        # Invalid (wrong check digit)
        "XX12345678",                     # Invalid (unknown country)
        "DE8937040044053201300",          # Invalid (wrong length)
    ]
    
    print("\nValidating IBANs:")
    for iban in ibans:
        result = validate(iban)
        status = "✓ Valid" if result else "✗ Invalid"
        print(f"  {format_iban(iban):40} {status}")


def example_formatting():
    """IBAN formatting examples."""
    print("\n" + "=" * 60)
    print("Example 2: IBAN Formatting")
    print("=" * 60)
    
    iban = "GB82WEST12345698765432"
    
    print(f"\nRaw IBAN: {iban}")
    print(f"Default format: {format_iban(iban)}")
    print(f"With hyphens: {format_iban(iban, separator='-')}")
    print(f"Groups of 6: {format_iban(iban, group_size=6, separator=' ')}")
    
    # Stripping formatting
    formatted = "GB82 WEST 1234 5698 7654 32"
    stripped = strip_formatting(formatted)
    print(f"\nStripping: '{formatted}' -> '{stripped}'")


def example_parsing():
    """Parse IBAN into components."""
    print("\n" + "=" * 60)
    print("Example 3: Parsing IBAN Components")
    print("=" * 60)
    
    test_ibans = [
        "DE89370400440532013000",
        "GB82WEST12345698765432",
        "FR1420041010050500013M02606",
        "IT60X0542811101000000123456",
    ]
    
    for iban in test_ibans:
        parsed = parse(iban)
        print(f"\n  {format_iban(iban)}")
        print(f"    Country:      {parsed['country_name']} ({parsed['country_code']})")
        print(f"    Check digits: {parsed['check_digits']}")
        print(f"    BBAN:         {parsed['bban']}")
        print(f"    Total length: {parsed['total_length']}")
        print(f"    Valid:        {'Yes' if parsed['is_valid'] else 'No'}")


def example_bank_info():
    """Extract bank information from IBAN."""
    print("\n" + "=" * 60)
    print("Example 4: Extracting Bank Information")
    print("=" * 60)
    
    examples = [
        ("Germany", "DE89370400440532013000"),
        ("United Kingdom", "GB82WEST12345698765432"),
        ("France", "FR1420041010050500013M02606"),
        ("Netherlands", "NL91ABNA0417164300"),
    ]
    
    for country_name, iban in examples:
        info = extract_bank_info(iban)
        print(f"\n  {country_name}: {format_iban(iban)}")
        print(f"    Bank code:   {info.get('bank_code', 'N/A')}")
        if info.get('branch_code'):
            print(f"    Branch code: {info['branch_code']}")
        print(f"    Account:     {info.get('account_number', 'N/A')}")


def example_check_digit_calculation():
    """Calculate check digits."""
    print("\n" + "=" * 60)
    print("Example 5: Calculating Check Digits")
    print("=" * 60)
    
    print("\nCalculating check digits for given BBANs:")
    
    examples = [
        ("GB", "WEST12345698765432"),
        ("DE", "370400440532013000"),
        ("FR", "20041010050500013M02606"),
        ("IT", "X0542811101000000123456"),
    ]
    
    for country, bban in examples:
        check = calculate_check_digits(country, bban)
        full_iban = country + check + bban
        is_valid = validate(full_iban)
        print(f"  {country} + {bban[:15]}... -> Check: {check}")
        print(f"    Full IBAN: {format_iban(full_iban)} (Valid: {is_valid})")


def example_country_info():
    """Get IBAN structure for countries."""
    print("\n" + "=" * 60)
    print("Example 6: Country IBAN Information")
    print("=" * 60)
    
    countries = ["DE", "GB", "FR", "IT", "NL", "CH", "AT", "BE"]
    
    print("\nIBAN structures by country:")
    for code in countries:
        info = get_country_info(code)
        print(f"  {code}: {info['country_name']:20} Length: {info['iban_length']:2}  Structure: {info['bban_structure']}")
    
    # Total supported countries
    all_countries = get_supported_countries()
    print(f"\n  Total supported countries: {len(all_countries)}")


def example_generate_test_ibans():
    """Generate test IBANs."""
    print("\n" + "=" * 60)
    print("Example 7: Generating Test IBANs")
    print("=" * 60)
    
    print("\nGenerating random valid IBANs for testing:")
    
    countries = ["DE", "GB", "FR", "IT", "ES", "NL"]
    
    for country in countries:
        test_iban = generate_test_iban(country)
        is_valid = validate(test_iban)
        print(f"  {country}: {format_iban(test_iban)} (Valid: {is_valid})")
    
    print("\nGenerating batch of test IBANs:")
    batch = generate_batch_test_ibans("DE", 5)
    for iban in batch:
        print(f"  {format_iban(iban)}")


def example_validator_class():
    """Using the IBANValidator class."""
    print("\n" + "=" * 60)
    print("Example 8: Using IBANValidator Class")
    print("=" * 60)
    
    # Create validator with custom formatting
    validator = IBANValidator(group_size=4, separator="-")
    
    iban = "DE89370400440532013000"
    
    print(f"\nValidating: {iban}")
    print(f"  Is valid: {validator.validate(iban)}")
    print(f"  Formatted: {validator.format(iban)}")
    
    parsed = validator.parse(iban)
    print(f"  Country: {parsed['country_name']}")
    
    info = validator.get_bank_info(iban)
    print(f"  Bank code: {info['bank_code']}")
    print(f"  Account: {info['account_number']}")
    
    # Generate test IBAN
    test = validator.generate_test("GB")
    print(f"\nGenerated test IBAN: {validator.format(test)}")


def example_all_test_ibans():
    """Show all predefined test IBANs."""
    print("\n" + "=" * 60)
    print("Example 9: All Predefined Test IBANs")
    print("=" * 60)
    
    print("\nValid test IBANs for major countries:")
    for country in sorted(TEST_IBANS.keys())[:15]:
        iban = TEST_IBANS[country]
        info = get_country_info(country)
        print(f"  {country}: {format_iban(iban):32} ({info['iban_length']} chars)")


def example_payment_integration():
    """Example: IBAN validation in a payment system."""
    print("\n" + "=" * 60)
    print("Example 10: Payment Integration Example")
    print("=" * 60)
    
    def validate_payment_iban(iban: str) -> dict:
        """
        Validate IBAN for a payment system.
        
        Returns:
            Dictionary with validation result and extracted info.
        """
        # Clean the IBAN
        clean_iban = strip_formatting(iban)
        
        # Validate
        is_valid = validate(clean_iban)
        
        if not is_valid:
            return {
                "valid": False,
                "error": "Invalid IBAN format or check digits",
                "iban": clean_iban
            }
        
        # Parse and extract info
        parsed = parse(clean_iban)
        bank_info = extract_bank_info(clean_iban)
        
        return {
            "valid": True,
            "iban": clean_iban,
            "formatted": format_iban(clean_iban),
            "country": parsed['country_name'],
            "country_code": parsed['country_code'],
            "bank_code": bank_info.get('bank_code', ''),
            "account_number": bank_info.get('account_number', ''),
        }
    
    # Test with various IBANs
    test_inputs = [
        "GB82 WEST 1234 5698 7654 32",  # Valid, with spaces
        "de89370400440532013000",        # Valid, lowercase
        "FR1420041010050500013M02606",  # Valid
        "GB82WEST12345698765433",        # Invalid check digit
        "XX123456789",                   # Invalid country
    ]
    
    print("\nPayment IBAN Validation:")
    for iban_input in test_inputs:
        result = validate_payment_iban(iban_input)
        print(f"\n  Input: {iban_input}")
        if result['valid']:
            print(f"    Status: ✓ Valid")
            print(f"    IBAN: {result['formatted']}")
            print(f"    Country: {result['country']}")
            print(f"    Bank Code: {result['bank_code']}")
        else:
            print(f"    Status: ✗ {result['error']}")


def example_sepa_validation():
    """Example: SEPA IBAN validation."""
    print("\n" + "=" * 60)
    print("Example 11: SEPA Zone Validation")
    print("=" * 60)
    
    # SEPA countries (subset)
    SEPA_COUNTRIES = {
        "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR",
        "DE", "GR", "HU", "IS", "IE", "IT", "LV", "LI", "LT", "LU",
        "MT", "NL", "NO", "PL", "PT", "RO", "SK", "SI", "ES", "SE",
        "CH", "GB",
    }
    
    def is_sepa_iban(iban: str) -> bool:
        """Check if IBAN is from a SEPA country."""
        clean_iban = strip_formatting(iban)
        if len(clean_iban) < 2:
            return False
        country = clean_iban[:2].upper()
        return country in SEPA_COUNTRIES
    
    test_ibans = [
        "DE89370400440532013000",  # Germany (SEPA)
        "GB82WEST12345698765432",  # UK (SEPA)
        "CH9300762011623852957",   # Switzerland (SEPA)
        "US12345678901234567890",  # US (not SEPA)
        "BR1800360305000010009795493C1",  # Brazil (not SEPA)
    ]
    
    print("\nSEPA Zone Check:")
    for iban in test_ibans:
        clean = strip_formatting(iban)
        is_valid = validate(clean)
        is_sepa = is_sepa_iban(clean)
        
        status = "✓ SEPA" if is_sepa else "✗ Non-SEPA"
        valid = "Valid" if is_valid else "Invalid"
        
        print(f"  {format_iban(iban)[:30]:30} {status} ({valid})")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("IBAN Utilities - Usage Examples")
    print("=" * 60)
    
    example_basic_validation()
    example_formatting()
    example_parsing()
    example_bank_info()
    example_check_digit_calculation()
    example_country_info()
    example_generate_test_ibans()
    example_validator_class()
    example_all_test_ibans()
    example_payment_integration()
    example_sepa_validation()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()