#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Plus Code Utilities Examples

Demonstrates practical usage of Plus Code (Open Location Code) utilities.
Plus Codes provide a universal addressing solution for any location on Earth.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from plus_code_utils.mod import (
    encode, decode, shorten, recover_nearest,
    is_valid_code, clean_code, get_code_length,
    get_precision_description, encode_with_shortening,
    get_neighbors, calculate_distance_km, format_for_display,
    is_short_code, is_full_code, get_area_size_meters
)


def example_basic_encoding():
    """Example: Basic Plus Code encoding."""
    print("=" * 60)
    print("Example 1: Basic Plus Code Encoding")
    print("=" * 60)
    
    locations = [
        ("Google Zurich", 47.365590, 8.524030),
        ("Times Square, NYC", 40.7580, -73.9855),
        ("Big Ben, London", 51.5007, -0.1246),
        ("Tokyo Tower", 35.6586, 139.7454),
        ("Sydney Opera House", -33.8568, 151.2153),
        ("Mount Everest", 27.9881, 86.9250),
    ]
    
    for name, lat, lon in locations:
        result = encode(lat, lon, 10)
        print(f"\n{name}:")
        print(f"  Coordinates: ({lat}, {lon})")
        print(f"  Plus Code:   {result.full_code}")
        print(f"  Precision:   {get_precision_description(10)}")


def example_precision_levels():
    """Example: Different precision levels."""
    print("\n" + "=" * 60)
    print("Example 2: Precision Levels")
    print("=" * 60)
    
    lat, lon = 47.365590, 8.524030
    
    for code_length in [4, 6, 8, 10, 11]:
        result = encode(lat, lon, code_length)
        print(f"\nLength {code_length}:")
        print(f"  Code:      {result.full_code}")
        print(f"  Precision: {get_precision_description(code_length)}")
        
        lat_size, lon_size = get_area_size_meters(result.full_code)
        print(f"  Area size: {lat_size:.0f}m × {lon_size:.0f}m")


def example_decoding():
    """Example: Decoding Plus Codes."""
    print("\n" + "=" * 60)
    print("Example 3: Decoding Plus Codes")
    print("=" * 60)
    
    codes = [
        "8FVC2222+",     # Standard 10-digit
        "8FVC2222+22",   # Higher precision
        "8FVC+G2",       # Lower precision
    ]
    
    for code in codes:
        if not is_valid_code(code):
            print(f"\n{code}: Invalid code")
            continue
        
        area = decode(code)
        print(f"\n{code}:")
        print(f"  Center:     ({area.latitude_center:.6f}, {area.longitude_center:.6f})")
        print(f"  Bounds:     [{area.latitude_lo:.6f}, {area.longitude_lo:.6f}]")
        print(f"              to [{area.latitude_hi:.6f}, {area.longitude_hi:.6f}]")
        
        lat_size = area.latitude_hi - area.latitude_lo
        lon_size = area.longitude_hi - area.longitude_lo
        print(f"  Size (deg): {lat_size:.6f}° × {lon_size:.6f}°")


def example_shortening():
    """Example: Shortening Plus Codes."""
    print("\n" + "=" * 60)
    print("Example 4: Shortening Plus Codes")
    print("=" * 60)
    
    # Zurich office
    zurich_code = encode(47.365590, 8.524030, 12).full_code
    print(f"\nOriginal code: {zurich_code}")
    
    # Shorten with local reference (Zurich city center)
    local_ref = shorten(zurich_code, 47.37, 8.52)
    print(f"Shortened (local ref): {local_ref}")
    
    # Shorten with distant reference
    distant_ref = shorten(zurich_code, 40.7, -74.0)  # NYC
    print(f"Shortened (distant ref): {distant_ref}")
    
    print("\nUsage tip: Short codes are useful for local communication!")
    print("Example: Tell someone 'the cafe is at 2222+22' in Zurich city")


def example_recovery():
    """Example: Recovering full codes from short codes."""
    print("\n" + "=" * 60)
    print("Example 5: Recovering Full Codes")
    print("=" * 60)
    
    short_codes = [
        ("2222+22", 47.37, 8.52, "Zurich"),
        ("C2G2+", 40.75, -73.98, "NYC"),
        ("6G2G+", 35.66, 139.75, "Tokyo"),
    ]
    
    for short_code, ref_lat, ref_lon, city in short_codes:
        full_code = recover_nearest(short_code, ref_lat, ref_lon)
        area = decode(full_code)
        
        print(f"\nShort: {short_code} (reference: {city})")
        print(f"Full:  {full_code}")
        print(f"Location: ({area.latitude_center:.4f}, {area.longitude_center:.4f})")


def example_validation():
    """Example: Validating Plus Codes."""
    print("\n" + "=" * 60)
    print("Example 6: Code Validation")
    print("=" * 60)
    
    test_codes = [
        "8FVC2222+",       # Valid
        "8FVC2222+22",     # Valid
        "8fvc2222+",       # Valid (case insensitive)
        "2222+",           # Valid short code
        "invalid",         # Invalid
        "12345678",        # Invalid (no separator)
        "8FVC-2222+",      # Becomes valid after cleaning
    ]
    
    for code in test_codes:
        is_valid = is_valid_code(code)
        cleaned = clean_code(code)
        is_short = is_short_code(cleaned)
        
        print(f"\nInput: '{code}'")
        print(f"  Valid:    {is_valid}")
        print(f"  Cleaned:  '{cleaned}'")
        print(f"  Is short: {is_short}")


def example_neighbors():
    """Example: Finding neighboring Plus Codes."""
    print("\n" + "=" * 60)
    print("Example 7: Neighboring Codes")
    print("=" * 60)
    
    code = "8FVC2222+"
    print(f"\nCenter code: {code}")
    
    neighbors = get_neighbors(code)
    
    for direction in ['north', 'south', 'east', 'west']:
        neighbor_code = neighbors[direction]
        if neighbor_code:
            area = decode(neighbor_code)
            print(f"  {direction}: {neighbor_code} ({area.latitude_center:.4f}, {area.longitude_center:.4f})")


def example_distance_calculation():
    """Example: Calculating distance between codes."""
    print("\n" + "=" * 60)
    print("Example 8: Distance Calculation")
    print("=" * 60)
    
    pairs = [
        ("8FVC2222+", "8FVC4422+"),      # Nearby
        ("8FVC2222+", "C2G2G2G2+"),      # Different cities
        ("2G2222+", "C2G2G2G2+"),        # Low precision codes
    ]
    
    for code1, code2 in pairs:
        dist = calculate_distance_km(code1, code2)
        area1 = decode(code1)
        area2 = decode(code2)
        
        print(f"\nFrom: {code1} ({area1.latitude_center:.2f}, {area1.longitude_center:.2f})")
        print(f"To:   {code2} ({area2.latitude_center:.2f}, {area2.longitude_center:.2f})")
        print(f"Distance: {dist:.2f} km")


def example_practical_use():
    """Example: Practical use case - delivery address."""
    print("\n" + "=" * 60)
    print("Example 9: Practical Use Case - Delivery Address")
    print("=" * 60)
    
    # Scenario: A delivery service needs an address for a location
    # that doesn't have a traditional street address
    
    print("\nScenario: Remote cabin location")
    cabin_lat = 46.8523
    cabin_lon = 9.5342
    
    print(f"Cabin coordinates: ({cabin_lat}, {cabin_lon})")
    
    # Generate full Plus Code
    result = encode(cabin_lat, cabin_lon, 10)
    print(f"\nFull Plus Code: {result.full_code}")
    
    # For local delivery, shorten using nearby town reference
    nearby_town_lat = 46.85
    nearby_town_lon = 9.53
    
    short = shorten(result.full_code, nearby_town_lat, nearby_town_lon)
    print(f"Local format (for driver): {short}")
    
    # Display formatted for customer
    formatted = format_for_display(result.full_code)
    print(f"Customer display: {formatted}")
    
    # Validate customer input
    customer_input = "2222+"
    cleaned_input = clean_code(customer_input)
    
    print(f"\nCustomer entered: '{customer_input}'")
    print(f"Cleaned: '{cleaned_input}'")
    
    # Recover full code for processing
    recovered = recover_nearest(cleaned_input, nearby_town_lat, nearby_town_lon)
    print(f"Recovered for system: {recovered}")


def example_batch_processing():
    """Example: Batch processing of coordinates."""
    print("\n" + "=" * 60)
    print("Example 10: Batch Processing")
    print("=" * 60)
    
    # Multiple locations to process
    locations = [
        (47.365590, 8.524030),
        (40.7128, -74.0060),
        (51.5074, -0.1278),
        (35.6762, 139.6503),
        (-33.8688, 151.2093),
    ]
    
    print("\nProcessing 5 locations:")
    
    codes = []
    for lat, lon in locations:
        result = encode(lat, lon, 10)
        codes.append(result.full_code)
        print(f"  ({lat}, {lon}) → {result.full_code}")
    
    # Calculate distances between consecutive locations
    print("\nDistances between consecutive locations:")
    for i in range(len(codes) - 1):
        dist = calculate_distance_km(codes[i], codes[i+1])
        print(f"  {i+1} to {i+2}: {dist:.0f} km")


def example_display_formatting():
    """Example: Display formatting for user interfaces."""
    print("\n" + "=" * 60)
    print("Example 11: Display Formatting")
    print("=" * 60)
    
    codes = ["8FVC2222+", "8FVC2222+22", "2G+"]
    
    print("\nStandard display:")
    for code in codes:
        print(f"  {format_for_display(code)}")
    
    print("\nCompact display (no precision):")
    for code in codes:
        print(f"  {format_for_display(code, include_precision=False)}")


def run_all_examples():
    """Run all examples."""
    example_basic_encoding()
    example_precision_levels()
    example_decoding()
    example_shortening()
    example_recovery()
    example_validation()
    example_neighbors()
    example_distance_calculation()
    example_practical_use()
    example_batch_processing()
    example_display_formatting()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()