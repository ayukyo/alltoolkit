#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Nautical Utilities Test
====================================
Comprehensive tests for nautical_utils module.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Constants
    KNOTS_TO_MPH, KNOTS_TO_KPH, KNOTS_TO_MS,
    NAUTICAL_MILE_TO_MILES, NAUTICAL_MILE_TO_KM,
    FATHOM_TO_FEET, FATHOM_TO_METERS,
    EARTH_RADIUS_NM, EARTH_RADIUS_KM,
    
    # Enums
    BeaufortScale,
    
    # Speed conversions
    knots_to_mph,
    knots_to_kph,
    knots_to_ms,
    mph_to_knots,
    kph_to_knots,
    ms_to_knots,
    convert_speed,
    
    # Distance conversions
    nautical_miles_to_miles,
    nautical_miles_to_km,
    miles_to_nautical_miles,
    km_to_nautical_miles,
    convert_distance,
    
    # Depth conversions
    fathoms_to_feet,
    fathoms_to_meters,
    feet_to_fathoms,
    meters_to_fathoms,
    
    # Beaufort scale
    get_beaufort_scale,
    get_beaufort_range,
    describe_wind,
    
    # Compass directions
    degrees_to_cardinal,
    degrees_to_full_name,
    cardinal_to_degrees,
    normalize_heading,
    heading_difference,
    
    # Latitude/Longitude
    Coordinate,
    parse_coordinate,
    format_latitude,
    format_longitude,
    
    # Maritime flags
    get_maritime_flag_meaning,
    encode_maritime_message,
    get_distress_signals,
    
    # Navigation utilities
    calculate_distance_nm,
    calculate_bearing,
    time_to_destination,
    fuel_consumption,
    
    # Summary
    get_nautical_summary,
)


class TestSpeedConversions(unittest.TestCase):
    """Test speed conversion functions."""
    
    def test_knots_to_mph(self):
        """Test knots to mph conversion."""
        self.assertAlmostEqual(knots_to_mph(10), 11.5078, places=4)
        self.assertEqual(knots_to_mph(0), 0)
    
    def test_knots_to_kph(self):
        """Test knots to kph conversion."""
        self.assertEqual(knots_to_kph(10), 18.52)
    
    def test_knots_to_ms(self):
        """Test knots to m/s conversion."""
        self.assertAlmostEqual(knots_to_ms(10), 5.14444, places=4)
    
    def test_mph_to_knots(self):
        """Test mph to knots conversion."""
        self.assertAlmostEqual(mph_to_knots(11.5078), 10, places=4)
    
    def test_kph_to_knots(self):
        """Test kph to knots conversion."""
        self.assertAlmostEqual(kph_to_knots(18.52), 10, places=2)
    
    def test_ms_to_knots(self):
        """Test m/s to knots conversion."""
        self.assertAlmostEqual(ms_to_knots(5.14444), 10, places=2)
    
    def test_convert_speed(self):
        """Test general speed conversion."""
        self.assertAlmostEqual(convert_speed(10, 'knots', 'mph'), 11.5078, places=4)
        self.assertAlmostEqual(convert_speed(10, 'mph', 'knots'), 8.68976, places=4)
        
        # Test with different unit formats
        self.assertAlmostEqual(convert_speed(10, 'm/s', 'knots'), 19.44, places=2)
    
    def test_convert_speed_invalid_unit(self):
        """Test speed conversion with invalid unit."""
        with self.assertRaises(ValueError):
            convert_speed(10, 'invalid', 'knots')
        
        with self.assertRaises(ValueError):
            convert_speed(10, 'knots', 'invalid')


class TestDistanceConversions(unittest.TestCase):
    """Test distance conversion functions."""
    
    def test_nautical_miles_to_miles(self):
        """Test nautical miles to miles conversion."""
        self.assertAlmostEqual(nautical_miles_to_miles(100), 115.078, places=3)
    
    def test_nautical_miles_to_km(self):
        """Test nautical miles to km conversion."""
        self.assertAlmostEqual(nautical_miles_to_km(100), 185.2, places=1)
    
    def test_miles_to_nautical_miles(self):
        """Test miles to nautical miles conversion."""
        self.assertAlmostEqual(miles_to_nautical_miles(115.078), 100, places=2)
    
    def test_km_to_nautical_miles(self):
        """Test km to nautical miles conversion."""
        self.assertAlmostEqual(km_to_nautical_miles(185.2), 100, places=1)
    
    def test_convert_distance(self):
        """Test general distance conversion."""
        self.assertAlmostEqual(convert_distance(100, 'nm', 'km'), 185.2, places=1)
        self.assertAlmostEqual(convert_distance(100, 'km', 'nm'), 54.0, places=1)
    
    def test_convert_distance_invalid_unit(self):
        """Test distance conversion with invalid unit."""
        with self.assertRaises(ValueError):
            convert_distance(100, 'invalid', 'nm')


class TestDepthConversions(unittest.TestCase):
    """Test depth conversion functions."""
    
    def test_fathoms_to_feet(self):
        """Test fathoms to feet conversion."""
        self.assertEqual(fathoms_to_feet(10), 60)
        self.assertEqual(fathoms_to_feet(1), 6)
    
    def test_fathoms_to_meters(self):
        """Test fathoms to meters conversion."""
        self.assertAlmostEqual(fathoms_to_meters(10), 18.288, places=3)
    
    def test_feet_to_fathoms(self):
        """Test feet to fathoms conversion."""
        self.assertEqual(feet_to_fathoms(60), 10)
    
    def test_meters_to_fathoms(self):
        """Test meters to fathoms conversion."""
        self.assertAlmostEqual(meters_to_fathoms(18.288), 10, places=3)


class TestBeaufortScale(unittest.TestCase):
    """Test Beaufort scale functions."""
    
    def test_get_beaufort_scale(self):
        """Test Beaufort scale determination."""
        scale, desc, sea = get_beaufort_scale(0)
        self.assertEqual(scale, 0)
        self.assertEqual(desc, 'Calm')
        
        scale, desc, sea = get_beaufort_scale(25)
        self.assertEqual(scale, 6)
        self.assertEqual(desc, 'Strong Breeze')
        
        scale, desc, sea = get_beaufort_scale(100)
        self.assertEqual(scale, 12)
        self.assertEqual(desc, 'Hurricane')
    
    def test_get_beaufort_range(self):
        """Test Beaufort range retrieval."""
        min_k, max_k = get_beaufort_range(5)
        self.assertEqual(min_k, 17)
        self.assertEqual(max_k, 21)
        
        min_k, max_k = get_beaufort_range(0)
        self.assertEqual(min_k, 0)
        self.assertEqual(max_k, 0)
    
    def test_get_beaufort_range_invalid(self):
        """Test invalid Beaufort scale."""
        with self.assertRaises(ValueError):
            get_beaufort_range(-1)
        
        with self.assertRaises(ValueError):
            get_beaufort_range(13)
    
    def test_describe_wind(self):
        """Test wind description."""
        result = describe_wind(25)
        self.assertEqual(result['knots'], 25)
        self.assertEqual(result['beaufort'], 6)
        self.assertEqual(result['description'], 'Strong Breeze')
        self.assertIn('mph', result)
        self.assertIn('kph', result)


class TestCompassDirections(unittest.TestCase):
    """Test compass direction functions."""
    
    def test_degrees_to_cardinal(self):
        """Test degrees to cardinal conversion."""
        self.assertEqual(degrees_to_cardinal(0), 'N')
        self.assertEqual(degrees_to_cardinal(45), 'NE')
        self.assertEqual(degrees_to_cardinal(90), 'E')
        self.assertEqual(degrees_to_cardinal(180), 'S')
        self.assertEqual(degrees_to_cardinal(270), 'W')
        self.assertEqual(degrees_to_cardinal(360), 'N')
        
        # Edge cases - N covers 348.75-11.25
        self.assertEqual(degrees_to_cardinal(350), 'N')
        self.assertEqual(degrees_to_cardinal(10), 'N')
    
    def test_degrees_to_full_name(self):
        """Test degrees to full name conversion."""
        self.assertEqual(degrees_to_full_name(45), 'Northeast')
        self.assertEqual(degrees_to_full_name(90), 'East')
        self.assertEqual(degrees_to_full_name(225), 'Southwest')
    
    def test_cardinal_to_degrees(self):
        """Test cardinal to degrees conversion."""
        self.assertEqual(cardinal_to_degrees('N'), 0.0)
        self.assertEqual(cardinal_to_degrees('NE'), 45.0)
        self.assertEqual(cardinal_to_degrees('S'), 180.0)
        self.assertEqual(cardinal_to_degrees('W'), 270.0)
    
    def test_cardinal_to_degrees_invalid(self):
        """Test invalid cardinal direction."""
        with self.assertRaises(ValueError):
            cardinal_to_degrees('INVALID')
    
    def test_normalize_heading(self):
        """Test heading normalization."""
        self.assertEqual(normalize_heading(450), 90.0)
        self.assertEqual(normalize_heading(-90), 270.0)
        self.assertEqual(normalize_heading(0), 0.0)
        self.assertEqual(normalize_heading(180), 180.0)
    
    def test_heading_difference(self):
        """Test heading difference calculation."""
        self.assertEqual(heading_difference(10, 350), 20.0)
        self.assertEqual(heading_difference(90, 180), 90.0)
        self.assertEqual(heading_difference(0, 180), 180.0)


class TestCoordinate(unittest.TestCase):
    """Test Coordinate class and functions."""
    
    def test_coordinate_to_decimal(self):
        """Test coordinate to decimal conversion."""
        coord = Coordinate(degrees=45, minutes=30, seconds=0, direction='N')
        self.assertEqual(coord.to_decimal(), 45.5)
        
        coord = Coordinate(degrees=45, minutes=30, seconds=0, direction='S')
        self.assertEqual(coord.to_decimal(), -45.5)
    
    def test_coordinate_from_decimal(self):
        """Test coordinate from decimal conversion."""
        coord = Coordinate.from_decimal(45.5, is_latitude=True)
        self.assertEqual(coord.degrees, 45)
        self.assertEqual(coord.direction, 'N')
        
        coord = Coordinate.from_decimal(-45.5, is_latitude=True)
        self.assertEqual(coord.degrees, 45)
        self.assertEqual(coord.direction, 'S')
    
    def test_coordinate_to_dms_string(self):
        """Test DMS string formatting."""
        coord = Coordinate(degrees=45, minutes=30, seconds=30, direction='N')
        result = coord.to_dms_string()
        self.assertIn('45', result)
        self.assertIn('30', result)
        self.assertIn('N', result)
    
    def test_parse_coordinate_decimal(self):
        """Test parsing decimal coordinate."""
        decimal, direction = parse_coordinate("45.5")
        self.assertEqual(decimal, 45.5)
        self.assertIsNone(direction)
    
    def test_parse_coordinate_dms(self):
        """Test parsing DMS coordinate."""
        decimal, direction = parse_coordinate("45°30'N")
        self.assertEqual(decimal, 45.5)
        self.assertEqual(direction, 'N')
    
    def test_parse_coordinate_with_space(self):
        """Test parsing coordinate with spaces."""
        decimal, direction = parse_coordinate("45 30 N")
        self.assertEqual(decimal, 45.5)
        self.assertEqual(direction, 'N')
    
    def test_format_latitude(self):
        """Test latitude formatting."""
        result = format_latitude(45.5, 'dms')
        self.assertIn('45', result)
        self.assertIn('N', result)
    
    def test_format_longitude(self):
        """Test longitude formatting."""
        result = format_longitude(-122.3, 'dms')
        self.assertIn('122', result)
        self.assertIn('W', result)


class TestMaritimeFlags(unittest.TestCase):
    """Test maritime flag functions."""
    
    def test_get_maritime_flag_meaning(self):
        """Test maritime flag meaning retrieval."""
        result = get_maritime_flag_meaning('A')
        self.assertEqual(result, 'Alpha - Diver below; keep clear')
        
        result = get_maritime_flag_meaning('O')
        self.assertEqual(result, 'Oscar - Man overboard')
    
    def test_get_maritime_flag_meaning_invalid(self):
        """Test invalid flag letter."""
        with self.assertRaises(ValueError):
            get_maritime_flag_meaning('1')
    
    def test_encode_maritime_message(self):
        """Test maritime message encoding."""
        result = encode_maritime_message('SOS')
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['letter'], 'S')
    
    def test_get_distress_signals(self):
        """Test distress signals retrieval."""
        signals = get_distress_signals()
        self.assertIn('MAYDAY', signals)
        self.assertIn('SOS', signals)
        self.assertIn('PAN-PAN', signals)


class TestNavigationUtilities(unittest.TestCase):
    """Test navigation utility functions."""
    
    def test_calculate_distance_nm(self):
        """Test distance calculation."""
        # San Francisco to Los Angeles (approximately 300nm)
        distance = calculate_distance_nm(37.7749, -122.4194, 34.0522, -118.2437)
        self.assertTrue(295 < distance < 310)  # Roughly 300nm
        
        # Same point
        distance = calculate_distance_nm(0, 0, 0, 0)
        self.assertEqual(distance, 0)
    
    def test_calculate_bearing(self):
        """Test bearing calculation."""
        # From SF to LA (roughly southeast)
        bearing = calculate_bearing(37.7749, -122.4194, 34.0522, -118.2437)
        self.assertTrue(100 < bearing < 150)  # Southeast direction
    
    def test_time_to_destination(self):
        """Test time to destination calculation."""
        self.assertEqual(time_to_destination(100, 20), 5.0)
        self.assertEqual(time_to_destination(200, 10), 20.0)
    
    def test_time_to_destination_zero_speed(self):
        """Test time calculation with zero speed."""
        with self.assertRaises(ValueError):
            time_to_destination(100, 0)
    
    def test_fuel_consumption(self):
        """Test fuel consumption calculation."""
        result = fuel_consumption(100, 10, 20)
        self.assertEqual(result, 50.0)


class TestConstants(unittest.TestCase):
    """Test module constants."""
    
    def test_speed_constants(self):
        """Test speed conversion constants."""
        self.assertAlmostEqual(KNOTS_TO_MPH, 1.15078, places=5)
        self.assertEqual(KNOTS_TO_KPH, 1.852)
    
    def test_distance_constants(self):
        """Test distance conversion constants."""
        self.assertEqual(NAUTICAL_MILE_TO_KM, 1.852)
    
    def test_depth_constants(self):
        """Test depth conversion constants."""
        self.assertEqual(FATHOM_TO_FEET, 6)
    
    def test_earth_constants(self):
        """Test Earth radius constants."""
        self.assertEqual(EARTH_RADIUS_NM, 3440.065)
        self.assertEqual(EARTH_RADIUS_KM, 6371.0)


class TestSummary(unittest.TestCase):
    """Test summary function."""
    
    def test_get_nautical_summary(self):
        """Test nautical summary retrieval."""
        summary = get_nautical_summary()
        self.assertEqual(summary['module'], 'nautical_utils')
        self.assertIn('features', summary)
        self.assertIn('constants', summary)


if __name__ == '__main__':
    unittest.main()