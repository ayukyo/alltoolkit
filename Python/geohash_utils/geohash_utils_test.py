#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Geohash Utilities Test Suite
==========================================
Comprehensive tests for geohash_utils module.

Run with: python -m pytest geohash_utils_test.py -v
Or directly: python geohash_utils_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Data classes
    GeoPoint, GeoBounds, GeoCell,
    
    # Encoding/decoding
    encode, decode, decode_bounds,
    
    # Neighbor functions
    neighbors, neighbor, expand,
    
    # Distance functions
    haversine_distance, distance, distance_point_to_geohash,
    
    # Validation
    is_valid, validate,
    
    # Utilities
    get_precision, get_cell_dimensions, get_cell_area,
    common_prefix, covers_area,
    
    # Cell functions
    get_cell, children, parent,
    
    # Constants
    BASE32_CHARS, BASE32_DECODE, DIRECTIONS,
)

import unittest
import math


class TestGeoPoint(unittest.TestCase):
    """Test GeoPoint dataclass."""
    
    def test_valid_point(self):
        """Test creating valid geographic point."""
        point = GeoPoint(40.7128, -74.0060)
        self.assertEqual(point.lat, 40.7128)
        self.assertEqual(point.lng, -74.0060)
    
    def test_invalid_latitude(self):
        """Test invalid latitude raises error."""
        with self.assertRaises(ValueError):
            GeoPoint(91.0, 0.0)
        with self.assertRaises(ValueError):
            GeoPoint(-91.0, 0.0)
    
    def test_invalid_longitude(self):
        """Test invalid longitude raises error."""
        with self.assertRaises(ValueError):
            GeoPoint(0.0, 181.0)
        with self.assertRaises(ValueError):
            GeoPoint(0.0, -181.0)
    
    def test_distance_to(self):
        """Test distance calculation between points."""
        nyc = GeoPoint(40.7128, -74.0060)
        la = GeoPoint(34.0522, -118.2437)
        dist = nyc.distance_to(la)
        # NYC to LA is approximately 3936 km
        self.assertAlmostEqual(dist, 3936, delta=10)
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        point = GeoPoint(40.7128, -74.0060)
        d = point.to_dict()
        self.assertEqual(d['lat'], 40.7128)
        self.assertEqual(d['lng'], -74.0060)


class TestGeoBounds(unittest.TestCase):
    """Test GeoBounds dataclass."""
    
    def test_center(self):
        """Test center calculation."""
        bounds = GeoBounds(0, 10, 0, 10)
        self.assertEqual(bounds.center, (5, 5))
    
    def test_dimensions(self):
        """Test width and height."""
        bounds = GeoBounds(0, 10, -10, 10)
        self.assertEqual(bounds.height, 10)
        self.assertEqual(bounds.width, 20)
    
    def test_contains(self):
        """Test point containment."""
        bounds = GeoBounds(0, 10, 0, 10)
        self.assertTrue(bounds.contains(5, 5))
        self.assertTrue(bounds.contains(0, 0))
        self.assertTrue(bounds.contains(10, 10))
        self.assertFalse(bounds.contains(-1, 5))
        self.assertFalse(bounds.contains(5, 11))


class TestEncoding(unittest.TestCase):
    """Test geohash encoding."""
    
    def test_encode_basic(self):
        """Test basic encoding."""
        # Known test cases - verify that encoding produces valid geohashes
        gh = encode(57.64911, 10.40744, 6)
        self.assertEqual(gh, 'u4pruy')
        
        gh = encode(40.7128, -74.0060, 6)
        # Verify it's valid and decodes close to original
        self.assertEqual(len(gh), 6)
        self.assertTrue(is_valid(gh))
        lat, lng = decode(gh)
        self.assertAlmostEqual(lat, 40.7128, delta=0.02)
        self.assertAlmostEqual(lng, -74.0060, delta=0.02)
    
    def test_encode_precision(self):
        """Test different precision levels."""
        lat, lng = 40.7128, -74.0060
        
        for precision in range(1, 13):
            gh = encode(lat, lng, precision)
            self.assertEqual(len(gh), precision)
    
    def test_encode_world_locations(self):
        """Test encoding various world locations."""
        locations = [
            (35.6762, 139.6503, 'xn76ur'),    # Tokyo
            (-33.8688, 151.2093, 'r3gx2f'),   # Sydney
            (51.5074, -0.1278, 'gcpvj0'),     # London
            (48.8566, 2.3522, 'u09tvr'),     # Paris
            (0, 0, 's00000'),                 # Null Island
        ]
        
        for lat, lng, expected_prefix in locations:
            gh = encode(lat, lng, 6)
            with self.subTest(lat=lat, lng=lng):
                self.assertTrue(gh.startswith(expected_prefix[:2]))
    
    def test_encode_invalid_latitude(self):
        """Test encoding with invalid latitude."""
        with self.assertRaises(ValueError):
            encode(91, 0, 6)
        with self.assertRaises(ValueError):
            encode(-91, 0, 6)
    
    def test_encode_invalid_longitude(self):
        """Test encoding with invalid longitude."""
        with self.assertRaises(ValueError):
            encode(0, 181, 6)
        with self.assertRaises(ValueError):
            encode(0, -181, 6)
    
    def test_encode_invalid_precision(self):
        """Test encoding with invalid precision."""
        with self.assertRaises(ValueError):
            encode(0, 0, 0)
        with self.assertRaises(ValueError):
            encode(0, 0, 13)


class TestDecoding(unittest.TestCase):
    """Test geohash decoding."""
    
    def test_decode_basic(self):
        """Test basic decoding."""
        lat, lng = decode('u4pruy')
        # Should be close to original (within cell dimensions for 6-char precision)
        self.assertAlmostEqual(lat, 57.649, delta=0.01)
        self.assertAlmostEqual(lng, 10.407, delta=0.01)
    
    def test_decode_precision(self):
        """Test decoding at different precisions."""
        # Higher precision = smaller error
        lat_low, lng_low = decode('u4')
        lat_high, lng_high = decode('u4pruy')
        
        # Higher precision should be closer to true value
        true_lat, true_lng = 57.64911, 10.40744
        
        error_low = abs(lat_low - true_lat) + abs(lng_low - true_lng)
        error_high = abs(lat_high - true_lat) + abs(lng_high - true_lng)
        
        self.assertLess(error_high, error_low)
    
    def test_decode_bounds(self):
        """Test bounds decoding."""
        bounds = decode_bounds('u4pruy')
        
        # Check that the center is near expected (with appropriate tolerance for 6-char precision)
        # 6-char geohash cells are ~1.2km x 0.6km
        center_lat, center_lng = bounds.center
        self.assertAlmostEqual(center_lat, 57.649, delta=0.01)
        self.assertAlmostEqual(center_lng, 10.407, delta=0.01)
    
    def test_decode_invalid_character(self):
        """Test decoding with invalid character."""
        with self.assertRaises(ValueError):
            decode('u4prui')  # 'i' is not valid base32
    
    def test_decode_empty(self):
        """Test decoding empty string."""
        with self.assertRaises(ValueError):
            decode('')
    
    def test_case_insensitive(self):
        """Test that decoding is case-insensitive."""
        lat1, lng1 = decode('U4PRUY')
        lat2, lng2 = decode('u4pruy')
        self.assertEqual((lat1, lng1), (lat2, lng2))


class TestEncodeDecodeRoundTrip(unittest.TestCase):
    """Test that encode/decode are consistent."""
    
    def test_round_trip_various_locations(self):
        """Test round trip for various locations."""
        locations = [
            (40.7128, -74.0060),
            (35.6762, 139.6503),
            (-33.8688, 151.2093),
            (51.5074, -0.1278),
            (0, 0),
            (-45, -90),
            (45, 90),
        ]
        
        for lat, lng in locations:
            for precision in [4, 6, 8, 10]:
                with self.subTest(lat=lat, lng=lng, precision=precision):
                    gh = encode(lat, lng, precision)
                    decoded_lat, decoded_lng = decode(gh)
                    
                    # Error should decrease with higher precision
                    lat_error = abs(decoded_lat - lat)
                    lng_error = abs(decoded_lng - lng)
                    
                    # Allow error based on precision (cell dimensions)
                    # Higher precision means smaller max_error
                    dims = get_cell_dimensions(precision)
                    # Convert km to degrees (approximate)
                    max_lat_error = dims[1] / 111.0  # km to lat degrees
                    max_lng_error = dims[0] / 111.0  # km to lng degrees
                    
                    self.assertLess(lat_error, max_lat_error * 2)
                    self.assertLess(lng_error, max_lng_error * 2)


class TestNeighbors(unittest.TestCase):
    """Test neighbor calculations."""
    
    def test_neighbor_directions(self):
        """Test all 8 neighbor directions."""
        gh = 'u4pruy'
        n = neighbors(gh)
        
        expected_directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        for direction in expected_directions:
            with self.subTest(direction=direction):
                self.assertIn(direction, n)
                self.assertEqual(len(n[direction]), len(gh))
                self.assertTrue(is_valid(n[direction]))
    
    def test_neighbor_single_direction(self):
        """Test single direction neighbor."""
        n = neighbor('u4pruy', 'n')
        self.assertEqual(len(n), 6)
        self.assertTrue(is_valid(n))
    
    def test_neighbor_invalid_direction(self):
        """Test invalid direction raises error."""
        with self.assertRaises(ValueError):
            neighbor('u4pruy', 'x')
    
    def test_neighbors_are_adjacent(self):
        """Test that neighbors are actually adjacent."""
        gh = 'u4pruy'
        center_bounds = decode_bounds(gh)
        center_lat, center_lng = center_bounds.center
        
        for direction, neighbor_gh in neighbors(gh).items():
            neighbor_bounds = decode_bounds(neighbor_gh)
            neighbor_lat, neighbor_lng = neighbor_bounds.center
            
            # Distance should be approximately one cell size
            dist = haversine_distance(center_lat, center_lng, neighbor_lat, neighbor_lng)
            # Should be close (within a few hundred meters for precision 6)
            self.assertLess(dist, 1.0, f"Neighbor {direction} too far: {dist} km")


class TestDistance(unittest.TestCase):
    """Test distance calculations."""
    
    def test_haversine_same_point(self):
        """Test distance to same point is zero."""
        dist = haversine_distance(40.7128, -74.0060, 40.7128, -74.0060)
        self.assertAlmostEqual(dist, 0, places=5)
    
    def test_haversine_nyc_to_la(self):
        """Test NYC to LA distance."""
        dist = haversine_distance(40.7128, -74.0060, 34.0522, -118.2437)
        # Approximately 3936 km
        self.assertAlmostEqual(dist, 3936, delta=10)
    
    def test_haversine_antipodal(self):
        """Test antipodal points."""
        dist = haversine_distance(0, 0, 0, 180)
        # Half the circumference
        self.assertAlmostEqual(dist, 20015, delta=100)
    
    def test_geohash_distance(self):
        """Test distance between geohashes."""
        dist = distance('u4pruy', 'u4pruz')
        # Adjacent geohashes should be close
        self.assertLess(dist, 1.0)
    
    def test_distance_point_to_geohash(self):
        """Test distance from point to geohash center."""
        lat, lng = 57.64911, 10.40744
        gh = encode(lat, lng, 6)
        
        # Distance to own geohash center should be within cell dimensions
        # 6-char cells are ~1.2km x 0.6km, so max distance to center is ~0.6km
        dist = distance_point_to_geohash(lat, lng, gh)
        self.assertLess(dist, 0.5)  # Less than 500 meters (half cell width)


class TestValidation(unittest.TestCase):
    """Test geohash validation."""
    
    def test_is_valid_true(self):
        """Test valid geohashes."""
        self.assertTrue(is_valid('u4pruy'))
        self.assertTrue(is_valid('U4PRUY'))  # Uppercase
        self.assertTrue(is_valid('000000'))
        self.assertTrue(is_valid('zzzzzz'))
        self.assertTrue(is_valid('bcdefghjkmnpqrstuvwxyz'))  # All valid chars
    
    def test_is_valid_false(self):
        """Test invalid geohashes."""
        self.assertFalse(is_valid(''))
        self.assertFalse(is_valid(None))
        self.assertFalse(is_valid('u4prui'))  # 'i' is invalid
        self.assertFalse(is_valid('u4prua'))  # 'a' is invalid
        self.assertFalse(is_valid('u4prul'))  # 'l' is invalid
        self.assertFalse(is_valid('u4pruo'))  # 'o' is invalid
    
    def test_validate(self):
        """Test validate function."""
        self.assertEqual(validate('U4PRUY'), 'u4pruy')
        self.assertEqual(validate('  u4pruy  '), 'u4pruy')
    
    def test_validate_invalid(self):
        """Test validate with invalid input."""
        with self.assertRaises(ValueError):
            validate('')
        with self.assertRaises(ValueError):
            validate('u4prui')


class TestUtilities(unittest.TestCase):
    """Test utility functions."""
    
    def test_get_precision(self):
        """Test precision getter."""
        self.assertEqual(get_precision('u4pruy'), 6)
        self.assertEqual(get_precision('u4'), 2)
    
    def test_get_cell_dimensions(self):
        """Test cell dimensions."""
        # Precision 1 should be largest
        dims_1 = get_cell_dimensions(1)
        dims_6 = get_cell_dimensions(6)
        
        self.assertGreater(dims_1[0], dims_6[0])
        self.assertGreater(dims_1[1], dims_6[1])
    
    def test_get_cell_area(self):
        """Test cell area."""
        area_1 = get_cell_area(1)
        area_6 = get_cell_area(6)
        
        # Higher precision = smaller area
        self.assertGreater(area_1, area_6)
    
    def test_common_prefix(self):
        """Test common prefix finding."""
        self.assertEqual(common_prefix(['u4pruy', 'u4pruz', 'u4prux']), 'u4pru')
        self.assertEqual(common_prefix(['u4pruy', 'dr5ru7']), '')
        self.assertEqual(common_prefix([]), '')
    
    def test_covers_area(self):
        """Test area coverage."""
        # Small area in NYC
        geohashes = covers_area(40.71, -74.02, 40.72, -74.00, 5)
        
        # Should return multiple geohashes
        self.assertGreater(len(geohashes), 0)
        
        # All should be valid
        for gh in geohashes:
            self.assertTrue(is_valid(gh))


class TestCellFunctions(unittest.TestCase):
    """Test cell info functions."""
    
    def test_get_cell(self):
        """Test getting cell info."""
        cell = get_cell('u4pruy')
        
        self.assertEqual(cell.geohash, 'u4pruy')
        self.assertEqual(cell.precision, 6)
        self.assertIsInstance(cell.bounds, GeoBounds)
        self.assertIsInstance(cell.center, tuple)
        self.assertGreater(cell.width_km, 0)
        self.assertGreater(cell.height_km, 0)
    
    def test_children(self):
        """Test getting child geohashes."""
        children_gh = children('u4')
        
        # Should return 32 children
        self.assertEqual(len(children_gh), 32)
        
        # All should be valid and have parent prefix
        for child in children_gh:
            self.assertTrue(is_valid(child))
            self.assertTrue(child.startswith('u4'))
            self.assertEqual(len(child), 3)
    
    def test_parent(self):
        """Test getting parent geohash."""
        self.assertEqual(parent('u4pruy'), 'u4pru')
        self.assertEqual(parent('u4'), 'u')
        self.assertIsNone(parent('u'))
    
    def test_children_parent_roundtrip(self):
        """Test that children and parent are consistent."""
        parent_gh = 'u4pru'
        children_gh = children(parent_gh)
        
        for child in children_gh:
            self.assertEqual(parent(child), parent_gh)


class TestExpand(unittest.TestCase):
    """Test geohash expansion."""
    
    def test_expand_basic(self):
        """Test basic expansion."""
        expanded = expand('u4pruy', 0.5)  # 500m radius
        
        # Should include the original
        self.assertIn('u4pruy', expanded)
        
        # Should include neighbors
        self.assertGreater(len(expanded), 1)
    
    def test_expand_larger_radius(self):
        """Test expansion with larger radius."""
        small = expand('u4pruy', 0.5)
        large = expand('u4pruy', 2.0)
        
        # Larger radius should have more geohashes
        self.assertGreater(len(large), len(small))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_poles(self):
        """Test encoding near poles."""
        # Near North Pole
        gh = encode(89.9, 0, 6)
        lat, lng = decode(gh)
        self.assertGreater(lat, 89)
        
        # Near South Pole
        gh = encode(-89.9, 0, 6)
        lat, lng = decode(gh)
        self.assertLess(lat, -89)
    
    def test_dateline(self):
        """Test encoding near dateline."""
        # Just west of dateline
        gh1 = encode(0, 179.9, 6)
        # Just east of dateline
        gh2 = encode(0, -179.9, 6)
        
        # Should be different geohashes
        self.assertNotEqual(gh1, gh2)
    
    def test_prime_meridian(self):
        """Test encoding near prime meridian."""
        gh1 = encode(0, 0.001, 6)
        gh2 = encode(0, -0.001, 6)
        
        # Should be different geohashes
        self.assertNotEqual(gh1, gh2)
    
    def test_null_island(self):
        """Test encoding at null island (0, 0)."""
        gh = encode(0, 0, 6)
        lat, lng = decode(gh)
        
        # Should be close to (0, 0)
        self.assertAlmostEqual(lat, 0, delta=0.01)
        self.assertAlmostEqual(lng, 0, delta=0.01)
    
    def test_maximum_precision(self):
        """Test maximum precision (12)."""
        gh = encode(40.7128, -74.0060, 12)
        self.assertEqual(len(gh), 12)
        self.assertTrue(is_valid(gh))
    
    def test_minimum_precision(self):
        """Test minimum precision (1)."""
        gh = encode(40.7128, -74.0060, 1)
        self.assertEqual(len(gh), 1)
        self.assertTrue(is_valid(gh))


class TestBase32(unittest.TestCase):
    """Test base32 encoding specifics."""
    
    def test_all_valid_chars(self):
        """Test that all characters in BASE32_CHARS are valid."""
        for char in BASE32_CHARS:
            self.assertIn(char, BASE32_DECODE)
    
    def test_excluded_chars(self):
        """Test that excluded characters are not valid."""
        # Geohash excludes: a, i, l, o
        excluded = ['a', 'i', 'l', 'o']
        for char in excluded:
            self.assertNotIn(char, BASE32_DECODE)
    
    def test_char_count(self):
        """Test that we have exactly 32 characters."""
        self.assertEqual(len(BASE32_CHARS), 32)
        self.assertEqual(len(BASE32_DECODE), 32)


if __name__ == '__main__':
    unittest.main(verbosity=2)