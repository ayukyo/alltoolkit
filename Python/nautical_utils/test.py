"""
Tests for nautical_utils module.
"""

import math
from mod import (
    # Speed conversions
    knots_to_mph, knots_to_kph, knots_to_ms,
    mph_to_knots, kph_to_knots, ms_to_knots, convert_speed,
    
    # Distance conversions
    nautical_miles_to_miles, nautical_miles_to_km,
    miles_to_nautical_miles, km_to_nautical_miles, convert_distance,
    
    # Depth conversions
    fathoms_to_feet, fathoms_to_meters, feet_to_fathoms, meters_to_fathoms,
    
    # Beaufort scale
    get_beaufort_scale, get_beaufort_range, describe_wind,
    
    # Compass
    degrees_to_cardinal, degrees_to_full_name, cardinal_to_degrees,
    normalize_heading, heading_difference,
    
    # Coordinates
    Coordinate, parse_coordinate, format_latitude, format_longitude,
    
    # Maritime flags
    get_maritime_flag_meaning, encode_maritime_message, get_distress_signals,
    
    # Navigation
    calculate_distance_nm, calculate_bearing, time_to_destination, fuel_consumption,
    
    # Summary
    get_nautical_summary,
    
    # Constants
    KNOTS_TO_MPH, KNOTS_TO_KPH, KNOTS_TO_MS,
    NAUTICAL_MILE_TO_MILES, NAUTICAL_MILE_TO_KM,
    FATHOM_TO_FEET, FATHOM_TO_METERS
)


def test_speed_conversions():
    """Test speed conversion functions."""
    print("Testing speed conversions...")
    
    # Basic conversions
    assert abs(knots_to_mph(10) - 11.5078) < 0.001
    assert abs(knots_to_kph(10) - 18.52) < 0.001
    assert abs(knots_to_ms(10) - 5.14444) < 0.001
    
    # Reverse conversions
    assert abs(mph_to_knots(11.5078) - 10) < 0.001
    assert abs(kph_to_knots(18.52) - 10) < 0.001
    assert abs(ms_to_knots(5.14444) - 10) < 0.001
    
    # Zero
    assert knots_to_mph(0) == 0
    assert knots_to_kph(0) == 0
    assert knots_to_ms(0) == 0
    
    # Negative speeds
    assert abs(knots_to_mph(-10) - (-11.5078)) < 0.001
    
    # convert_speed function
    assert abs(convert_speed(10, 'knots', 'mph') - 11.5078) < 0.001
    assert abs(convert_speed(10, 'knots', 'kph') - 18.52) < 0.001
    assert abs(convert_speed(10, 'mph', 'knots') - 8.68976) < 0.001
    
    # Test with different unit formats
    assert abs(convert_speed(10, 'knots', 'm/s') - 5.14444) < 0.001
    assert abs(convert_speed(10, 'ms', 'knots') - 19.44) < 0.1
    
    print("  ✓ Speed conversions passed")


def test_distance_conversions():
    """Test distance conversion functions."""
    print("Testing distance conversions...")
    
    # Basic conversions
    assert abs(nautical_miles_to_miles(100) - 115.078) < 0.001
    assert abs(nautical_miles_to_km(100) - 185.2) < 0.001
    
    # Reverse conversions
    assert abs(miles_to_nautical_miles(115.078) - 100) < 0.001
    assert abs(km_to_nautical_miles(185.2) - 100) < 0.001
    
    # convert_distance function
    assert abs(convert_distance(100, 'nm', 'miles') - 115.078) < 0.001
    assert abs(convert_distance(100, 'nm', 'km') - 185.2) < 0.001
    assert abs(convert_distance(100, 'nm', 'nm') - 100) < 0.001
    
    # Test with different unit names
    assert abs(convert_distance(100, 'nautical_miles', 'kilometers') - 185.2) < 0.001
    
    print("  ✓ Distance conversions passed")


def test_depth_conversions():
    """Test depth conversion functions."""
    print("Testing depth conversions...")
    
    # Basic conversions
    assert fathoms_to_feet(10) == 60
    assert abs(fathoms_to_meters(10) - 18.288) < 0.001
    
    # Reverse conversions
    assert feet_to_fathoms(60) == 10
    assert abs(meters_to_fathoms(18.288) - 10) < 0.001
    
    # Zero
    assert fathoms_to_feet(0) == 0
    
    print("  ✓ Depth conversions passed")


def test_beaufort_scale():
    """Test Beaufort scale functions."""
    print("Testing Beaufort scale...")
    
    # Test get_beaufort_scale
    scale, desc, sea = get_beaufort_scale(0)
    assert scale == 0
    assert desc == "Calm"
    
    scale, desc, sea = get_beaufort_scale(3)  # Should be scale 1 (1-3 knots)
    assert scale == 1
    assert desc == "Light Air"
    
    scale, desc, sea = get_beaufort_scale(5)  # Should be scale 2 (4-6 knots)
    assert scale == 2
    assert desc == "Light Breeze"
    
    scale, desc, sea = get_beaufort_scale(25)
    assert scale == 6
    assert desc == "Strong Breeze"
    
    scale, desc, sea = get_beaufort_scale(100)
    assert scale == 12
    assert desc == "Hurricane"
    
    # Test get_beaufort_range (returns inclusive range)
    min_k, max_k = get_beaufort_range(5)
    assert min_k == 17
    assert max_k == 21  # inclusive max
    
    min_k, max_k = get_beaufort_range(11)
    assert min_k == 56
    assert max_k == 63  # inclusive max
    
    # Test describe_wind
    wind = describe_wind(25)
    assert wind['knots'] == 25
    assert wind['beaufort'] == 6
    assert 'mph' in wind
    assert 'kph' in wind
    assert wind['description'] == 'Strong Breeze'
    
    # Test edge cases
    assert get_beaufort_scale(0)[0] == 0
    assert get_beaufort_scale(1)[0] == 1
    assert get_beaufort_scale(63)[0] == 11  # 63 knots is scale 11
    assert get_beaufort_scale(64)[0] == 12   # 64+ knots is scale 12
    
    print("  ✓ Beaufort scale passed")


def test_compass_directions():
    """Test compass direction functions."""
    print("Testing compass directions...")
    
    # Test degrees_to_cardinal
    assert degrees_to_cardinal(0) == 'N'
    assert degrees_to_cardinal(360) == 'N'
    assert degrees_to_cardinal(45) == 'NE'
    assert degrees_to_cardinal(90) == 'E'
    assert degrees_to_cardinal(135) == 'SE'
    assert degrees_to_cardinal(180) == 'S'
    assert degrees_to_cardinal(225) == 'SW'
    assert degrees_to_cardinal(270) == 'W'
    assert degrees_to_cardinal(315) == 'NW'
    
    # Test intercardinal directions
    assert degrees_to_cardinal(22.5) == 'NNE'
    assert degrees_to_cardinal(67.5) == 'ENE'
    assert degrees_to_cardinal(112.5) == 'ESE'
    
    # Test degrees_to_full_name
    assert degrees_to_full_name(0) == 'North'
    assert degrees_to_full_name(45) == 'Northeast'
    assert degrees_to_full_name(90) == 'East'
    assert degrees_to_full_name(180) == 'South'
    assert degrees_to_full_name(270) == 'West'
    
    # Test cardinal_to_degrees
    assert cardinal_to_degrees('N') == 0.0
    assert cardinal_to_degrees('NE') == 45.0
    assert cardinal_to_degrees('E') == 90.0
    assert cardinal_to_degrees('S') == 180.0
    assert cardinal_to_degrees('W') == 270.0
    
    # Test normalize_heading
    assert normalize_heading(450) == 90.0
    assert normalize_heading(-90) == 270.0
    assert normalize_heading(360) == 0.0
    assert normalize_heading(0) == 0.0
    
    # Test heading_difference
    assert abs(heading_difference(10, 20) - 10) < 0.001
    assert abs(heading_difference(10, 350) - 20) < 0.001
    assert abs(heading_difference(0, 180) - 180) < 0.001
    assert abs(heading_difference(90, 270) - 180) < 0.001
    
    print("  ✓ Compass directions passed")


def test_coordinates():
    """Test coordinate functions."""
    print("Testing coordinates...")
    
    # Test Coordinate class
    coord = Coordinate(degrees=45, minutes=30, seconds=0, direction='N')
    assert abs(coord.to_decimal() - 45.5) < 0.001
    
    coord2 = Coordinate.from_decimal(45.5, is_latitude=True)
    assert coord2.degrees == 45
    assert coord2.direction == 'N'
    
    # Test negative coordinates
    coord3 = Coordinate.from_decimal(-122.5, is_latitude=False)
    assert coord3.degrees == 122
    assert coord3.direction == 'W'
    
    # Test string formats
    coord4 = Coordinate(degrees=37, minutes=46, seconds=29.2, direction='N')
    dms = coord4.to_dms_string()
    assert '37' in dms
    assert 'N' in dms
    
    dm = coord4.to_dm_string()
    assert '37' in dm
    assert 'N' in dm
    
    # Test parse_coordinate
    decimal, direction = parse_coordinate("45°30'N")
    assert abs(decimal - 45.5) < 0.001
    assert direction == 'N'
    
    decimal, direction = parse_coordinate("122 30.5 W")
    assert abs(decimal - (-122.508333)) < 0.01
    assert direction == 'W'
    
    decimal, direction = parse_coordinate("-122.5")
    assert abs(decimal - (-122.5)) < 0.001
    
    # Test format_latitude and format_longitude
    lat_str = format_latitude(45.5084, format='dms')
    assert 'N' in lat_str
    assert '45' in lat_str
    
    lon_str = format_longitude(-122.3, format='dm')
    assert 'W' in lon_str
    assert '122' in lon_str
    
    print("  ✓ Coordinates passed")


def test_maritime_flags():
    """Test maritime flag functions."""
    print("Testing maritime flags...")
    
    # Test get_maritime_flag_meaning
    meaning = get_maritime_flag_meaning('A')
    assert 'Alpha' in meaning
    assert 'diver' in meaning.lower()
    
    meaning = get_maritime_flag_meaning('O')
    assert 'Oscar' in meaning
    assert 'overboard' in meaning.lower()
    
    # Test all letters
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        meaning = get_maritime_flag_meaning(letter)
        assert len(meaning) > 0
    
    # Test encode_maritime_message
    encoded = encode_maritime_message('SOS')
    assert len(encoded) == 3
    assert encoded[0]['letter'] == 'S'
    assert encoded[1]['letter'] == 'O'
    assert encoded[2]['letter'] == 'S'
    
    # Test get_distress_signals
    signals = get_distress_signals()
    assert 'MAYDAY' in signals
    assert 'SOS' in signals
    assert 'PAN-PAN' in signals
    
    print("  ✓ Maritime flags passed")


def test_navigation():
    """Test navigation functions."""
    print("Testing navigation...")
    
    # Test calculate_distance_nm (San Francisco to Los Angeles ~ 298-300 nm)
    distance = calculate_distance_nm(37.7749, -122.4194, 34.0522, -118.2437)
    assert 295 < distance < 305
    
    # Test same point distance
    same_distance = calculate_distance_nm(0, 0, 0, 0)
    assert same_distance == 0
    
    # Test equator distance
    eq_distance = calculate_distance_nm(0, 0, 0, 180)
    assert 10700 < eq_distance < 10900  # ~10800 nm (halfway around earth at equator)
    
    # Test calculate_bearing
    bearing = calculate_bearing(0, 0, 0, 1)  # East
    assert 88 < bearing < 92
    
    bearing = calculate_bearing(0, 0, 1, 0)  # North
    assert 358 < bearing or bearing < 2
    
    bearing = calculate_bearing(0, 0, -1, 0)  # South
    assert 178 < bearing < 182
    
    # Test time_to_destination
    time = time_to_destination(100, 20)
    assert time == 5.0
    
    time = time_to_destination(150, 10)
    assert time == 15.0
    
    # Test fuel_consumption
    fuel = fuel_consumption(100, 10, 20)
    assert fuel == 50.0
    
    fuel = fuel_consumption(200, 5, 10)
    assert fuel == 100.0
    
    print("  ✓ Navigation passed")


def test_constants():
    """Test that constants are correct."""
    print("Testing constants...")
    
    # Speed constants
    assert abs(KNOTS_TO_MPH - 1.15078) < 0.00001
    assert abs(KNOTS_TO_KPH - 1.852) < 0.00001
    assert abs(KNOTS_TO_MS - 0.514444) < 0.00001
    
    # Distance constants
    assert abs(NAUTICAL_MILE_TO_MILES - 1.15078) < 0.00001
    assert abs(NAUTICAL_MILE_TO_KM - 1.852) < 0.00001
    
    # Depth constants
    assert FATHOM_TO_FEET == 6
    assert abs(FATHOM_TO_METERS - 1.8288) < 0.0001
    
    print("  ✓ Constants passed")


def test_get_nautical_summary():
    """Test summary function."""
    print("Testing summary...")
    
    summary = get_nautical_summary()
    assert summary['module'] == 'nautical_utils'
    assert 'features' in summary
    assert len(summary['features']) > 0
    assert 'constants' in summary
    
    print("  ✓ Summary passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Running Nautical Utils Tests")
    print("=" * 50)
    print()
    
    test_speed_conversions()
    test_distance_conversions()
    test_depth_conversions()
    test_beaufort_scale()
    test_compass_directions()
    test_coordinates()
    test_maritime_flags()
    test_navigation()
    test_constants()
    test_get_nautical_summary()
    
    print()
    print("=" * 50)
    print("All tests passed! ✓")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()