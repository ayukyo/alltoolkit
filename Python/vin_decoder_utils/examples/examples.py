#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - VIN Decoder Utilities Examples
===========================================
Example usage of VIN decoder utilities.

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os

# Add module path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vin_decoder_utils.mod import (
    decode_vin,
    validate_vin,
    validate_vin_format,
    validate_check_digit,
    calculate_check_digit,
    get_region,
    get_country,
    get_manufacturer,
    get_model_year,
    get_possible_years,
    decode_wmi,
    generate_vin,
    format_vin,
    extract_vin_from_text,
    compare_vins,
    get_year_code,
)


def example_validation():
    """Example: VIN validation."""
    print("=" * 60)
    print("VIN Validation Examples")
    print("=" * 60)
    
    test_vins = [
        "1HGBH41JXMN109186",  # Valid format, may have check digit issue
        "1HG123",             # Too short
        "1HGI41JXMN109186",   # Contains invalid 'I'
        generate_vin("1HG"),  # Generated valid VIN
    ]
    
    for vin in test_vins:
        print(f"\nVIN: {vin}")
        
        # Format validation
        result = validate_vin_format(vin)
        print(f"  Format valid: {result.valid}")
        if result.errors:
            print(f"  Errors: {result.errors}")
        
        # Check digit validation
        if result.valid:
            check_valid = validate_check_digit(vin)
            print(f"  Check digit valid: {check_valid}")
            
            calculated = calculate_check_digit(vin)
            actual = vin[8]
            print(f"  Expected check digit: {calculated}")
            print(f"  Actual check digit: {actual}")


def example_decoding():
    """Example: VIN decoding."""
    print("\n" + "=" * 60)
    print("VIN Decoding Examples")
    print("=" * 60)
    
    manufacturers = [
        ("1HG", "Honda US"),
        ("JHM", "Honda Japan"),
        ("WB", "BMW Germany"),
        ("WA", "Audi Germany"),
        ("JT", "Toyota Japan"),
        ("KN", "Kia Korea"),
        ("YV", "Volvo Sweden"),
        ("ZF", "Ferrari Italy"),
    ]
    
    for wmi, description in manufacturers:
        vin = generate_vin(wmi, model_year=2020)
        info = decode_vin(vin)
        
        print(f"\n{description}:")
        print(f"  VIN: {vin}")
        print(f"  Manufacturer: {info.manufacturer}")
        print(f"  Country: {info.country}")
        print(f"  Region: {info.region}")
        print(f"  Model Year: {info.model_year}")
        print(f"  WMI: {info.wmi}")
        print(f"  Valid: {info.valid}")


def example_year_codes():
    """Example: Year code handling."""
    print("\n" + "=" * 60)
    print("Year Code Examples")
    print("=" * 60)
    
    years = [1980, 1990, 2000, 2010, 2020, 2023]
    
    print("\nYear code mapping:")
    for year in years:
        code = get_year_code(year)
        print(f"  {year} → '{code}'")
    
    print("\n30-year cycle handling:")
    vin = generate_vin("1HG", model_year=2020)  # Uses 'L' code
    possible_years = get_possible_years(vin)
    print(f"  VIN: {vin}")
    print(f"  Year code: {vin[9]}")
    print(f"  Possible years: {possible_years}")
    
    print("\nSame code, different years:")
    print(f"  1990 and 2020 both use '{get_year_code(1990)}'")
    print(f"  1980 and 2010 both use '{get_year_code(1980)}'")


def example_region_identification():
    """Example: Region and country identification."""
    print("\n" + "=" * 60)
    print("Region Identification Examples")
    print("=" * 60)
    
    vin_samples = [
        (generate_vin("1HG"), "North America (US)"),
        (generate_vin("2HG"), "North America (Canada)"),
        (generate_vin("3H"), "North America (Mexico)"),
        (generate_vin("JHM"), "Asia (Japan)"),
        (generate_vin("KM"), "Asia (Korea)"),
        (generate_vin("MA"), "Asia (India)"),
        (generate_vin("LS"), "Asia (China)"),
        (generate_vin("WA"), "Europe (Germany)"),
        (generate_vin("YV"), "Europe (Sweden)"),
        (generate_vin("ZA"), "Europe (Italy)"),
        (generate_vin("6H"), "Oceania (Australia)"),
        (generate_vin("9H"), "South America (Brazil)"),
    ]
    
    print("\nRegion by first character:")
    for vin, expected_region in vin_samples:
        region = get_region(vin)
        country = get_country(vin)
        manufacturer = get_manufacturer(vin)
        print(f"  {vin[:3]}... → {region} ({country or 'Unknown'}) - {manufacturer or 'Unknown'}")
        print(f"    Expected: {expected_region}")


def example_manufacturers():
    """Example: Manufacturer lookup."""
    print("\n" + "=" * 60)
    print("Manufacturer Lookup Examples")
    print("=" * 60)
    
    manufacturers = [
        ("1HG", "Honda"),
        ("1F", "Ford"),
        ("1G", "General Motors"),
        ("1C", "Chrysler"),
        ("JH", "Honda Japan"),
        ("JT", "Toyota Japan"),
        ("JN", "Nissan Japan"),
        ("JM", "Mazda Japan"),
        ("WB", "BMW Germany"),
        ("WA", "Audi Germany"),
        ("WV", "Volkswagen Germany"),
        ("KN", "Kia Korea"),
        ("KM", "Hyundai Korea"),
        ("YV", "Volvo Sweden"),
        ("ZF", "Ferrari Italy"),
        ("SG", "Rolls-Royce UK"),
        ("SB", "Bentley UK"),
    ]
    
    print("\nWMI → Manufacturer:")
    for wmi, expected in manufacturers:
        manufacturer, country = decode_wmi(wmi)
        print(f"  {wmi} → {manufacturer or 'Unknown'} ({country or 'Unknown'})")
        print(f"    Expected: {expected}")


def example_vin_generation():
    """Example: VIN generation."""
    print("\n" + "=" * 60)
    print("VIN Generation Examples")
    print("=" * 60)
    
    # Generate VINs for different manufacturers
    print("\nGenerating VINs for different manufacturers:")
    
    configs = [
        ("JHM", 2020, "Honda Japan"),
        ("WB", 2018, "BMW Germany"),
        ("JT", 2023, "Toyota Japan"),
        ("YV", 2015, "Volvo Sweden"),
        ("KN", 2021, "Kia Korea"),
    ]
    
    for wmi, year, description in configs:
        vin = generate_vin(wmi, model_year=year)
        info = decode_vin(vin)
        print(f"\n  {description}:")
        print(f"    VIN: {vin}")
        print(f"    Valid: {info.check_digit_valid}")
        print(f"    Year: {info.model_year}")
    
    # Generate multiple unique VINs
    print("\nGenerating 5 unique VINs for same manufacturer:")
    vins = [generate_vin("1HG", model_year=2020) for _ in range(5)]
    for i, vin in enumerate(vins):
        print(f"  {i+1}. {vin}")
    print(f"  All unique: {len(set(vins)) == 5}")


def example_vin_extraction():
    """Example: VIN extraction from text."""
    print("\n" + "=" * 60)
    print("VIN Extraction from Text Examples")
    print("=" * 60)
    
    texts = [
        "My car's VIN is 1HGBH41JXMN109186 and my friend's is JHMFA16586S012345",
        "Vehicle registration: VIN WAUZZZ4G0FN012345, registered in 2020",
        "Invalid VIN ABC123DEF456GHI789 should not be extracted",
        "Found potential VINs: 1234567890ABCDEFF, 1HGBH41JXMN109186",
    ]
    
    for text in texts:
        # Replace placeholder VINs with generated valid ones for demo
        text_demo = text.replace("1HGBH41JXMN109186", generate_vin("1HG"))
        text_demo = text_demo.replace("JHMFA16586S012345", generate_vin("JH"))
        text_demo = text_demo.replace("WAUZZZ4G0FN012345", generate_vin("WA"))
        
        vins = extract_vin_from_text(text_demo)
        print(f"\n  Text: {text[:50]}...")
        print(f"  Extracted VINs: {vins}")


def example_vin_comparison():
    """Example: VIN comparison."""
    print("\n" + "=" * 60)
    print("VIN Comparison Examples")
    print("=" * 60)
    
    # Generate VINs for comparison
    honda1 = generate_vin("1HG", model_year=2020)
    honda2 = generate_vin("1HG", model_year=2021)
    bmw = generate_vin("WB", model_year=2020)
    
    print("\nComparing VINs:")
    print(f"  Honda 1: {honda1}")
    print(f"  Honda 2: {honda2}")
    print(f"  BMW: {bmw}")
    
    # Compare Honda VINs
    comparison = compare_vins(honda1, honda2)
    print(f"\n  Honda vs Honda (same manufacturer, different year):")
    for key, value in comparison.items():
        print(f"    {key}: {value}")
    
    # Compare Honda vs BMW
    comparison = compare_vins(honda1, bmw)
    print(f"\n  Honda vs BMW:")
    for key, value in comparison.items():
        print(f"    {key}: {value}")


def example_formatting():
    """Example: VIN formatting."""
    print("\n" + "=" * 60)
    print("VIN Formatting Examples")
    print("=" * 60)
    
    vin = generate_vin("1HG", model_year=2020)
    
    separators = [' ', '-', ':', '/', '']
    
    print(f"\nVIN: {vin}")
    for sep in separators:
        formatted = format_vin(vin, sep)
        print(f"  Separator '{sep}': {formatted}")


def example_full_decode():
    """Example: Full VIN decoding."""
    print("\n" + "=" * 60)
    print("Full VIN Decoding Example")
    print("=" * 60)
    
    vin = generate_vin("JHM", model_year=2020)  # Honda Japan
    info = decode_vin(vin)
    
    print(f"\nVIN: {vin}")
    print(f"\nDecoded Information:")
    print(f"  WMI (World Manufacturer Identifier): {info.wmi}")
    print(f"  VDS (Vehicle Descriptor Section): {info.vds}")
    print(f"  VIS (Vehicle Identifier Section): {info.vis}")
    print(f"  Manufacturer: {info.manufacturer}")
    print(f"  Country: {info.country}")
    print(f"  Region: {info.region}")
    print(f"  Model Year: {info.model_year}")
    print(f"  Possible Years: {info.model_years}")
    print(f"  Check Digit: {info.check_digit} (valid: {info.check_digit_valid})")
    print(f"  Plant Code: {info.plant_code}")
    print(f"  Sequential Number: {info.sequential_number}")
    print(f"  Overall Valid: {info.valid}")
    
    print(f"\nFormatted: {format_vin(vin, ' ')}")


def main():
    """Run all examples."""
    print("\n")
    print("*" * 60)
    print("VIN Decoder Utilities - Examples")
    print("*" * 60)
    
    example_validation()
    example_decoding()
    example_year_codes()
    example_region_identification()
    example_manufacturers()
    example_vin_generation()
    example_vin_extraction()
    example_vin_comparison()
    example_formatting()
    example_full_decode()
    
    print("\n" + "*" * 60)
    print("Examples Complete")
    print("*" * 60 + "\n")


if __name__ == "__main__":
    main()