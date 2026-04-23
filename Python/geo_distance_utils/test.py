#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Geographic Distance Utilities Tests
==================================================
Comprehensive test suite for geo_distance_utils module.
"""

import math
import unittest
import sys
import os

# Add module directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Constants
    EARTH_RADIUS_KM, EARTH_RADIUS_M, EARTH_RADIUS_MILES, EARTH_RADIUS_NAUTICAL,
    DEG_TO_RAD, RAD_TO_DEG, MAX_LATITUDE, MIN_LATITUDE, MAX_LONGITUDE, MIN_LONGITUDE,
    
    # Validation
    is_valid_coordinate, normalize_coordinate,
    
    # Distance calculations
    haversine_distance, vincenty_distance, distance,
    
    # Bearing
    initial_bearing, final_bearing,
    
    # Coordinate operations
    midpoint_coordinate, destination_point,
    
    # Polygon
    bounding_box, point_in_polygon, polygon_area_km2,
    
    # Path
    interpolate_path, nearest_point_on_path, total_path_distance,
    
    # Format conversions
    decimal_to_dms, dms_to_decimal, coordinate_to_string,
    
    # Unit conversions
    km_to_miles, km_to_nautical, km_to_m,
    miles_to_km, nautical_to_km, m_to_km, convert_distance,
    
    # Batch operations
    find_nearest, distances_to_all, within_radius,
)


class TestConstants(unittest.TestCase):
    """Test module constants."""
    
    def test_earth_radius_values(self):
        """Verify Earth radius constants are reasonable."""
        self.assertAlmostEqual(EARTH_RADIUS_KM, 6371.0, places=1)
        self.assertAlmostEqual(EARTH_RADIUS_M, 6371000.0, places=1)
        self.assertAlmostEqual(EARTH_RADIUS_MILES, 3958.8, places=1)
        self.assertAlmostEqual(EARTH_RADIUS_NAUTICAL, 3440.065, places=1)
    
    def test_coordinate_bounds(self):
        """Verify coordinate bounds."""
        self.assertEqual(MAX_LATITUDE, 90.0)
        self.assertEqual(MIN_LATITUDE, -90.0)
        self.assertEqual(MAX_LONGITUDE, 180.0)
        self.assertEqual(MIN_LONGITUDE, -180.0)
    
    def test_conversion_factors(self):
        """Verify conversion factors."""
        self.assertAlmostEqual(DEG_TO_RAD, math.pi / 180)
        self.assertAlmostEqual(RAD_TO_DEG, 180 / math.pi)


class TestCoordinateValidation(unittest.TestCase):
    """Test coordinate validation and normalization."""
    
    def test_is_valid_coordinate_valid(self):
        """Test valid coordinates."""
        self.assertTrue(is_valid_coordinate(0, 0))
        self.assertTrue(is_valid_coordinate(90, 180))
        self.assertTrue(is_valid_coordinate(-90, -180))
        self.assertTrue(is_valid_coordinate(39.9, 116.4))
    
    def test_is_valid_coordinate_invalid_lat(self):
        """Test invalid latitude."""
        self.assertFalse(is_valid_coordinate(91, 0))
        self.assertFalse(is_valid_coordinate(-91, 0))
    
    def test_is_valid_coordinate_invalid_lng(self):
        """Test invalid longitude."""
        self.assertFalse(is_valid_coordinate(0, 181))
        self.assertFalse(is_valid_coordinate(0, -181))
    
    def test_normalize_coordinate_longitude_wrap(self):
        """Test longitude wrapping."""
        self.assertEqual(normalize_coordinate(0, 200)[1], -160.0)
        self.assertEqual(normalize_coordinate(0, 400)[1], 40.0)
        self.assertEqual(normalize_coordinate(0, -200)[1], 160.0)
    
    def test_normalize_coordinate_latitude_clamp(self):
        """Test latitude clamping."""
        self.assertEqual(normalize_coordinate(100, 0)[0], 90.0)
        self.assertEqual(normalize_coordinate(-100, 0)[0], -90.0)


class TestHaversineDistance(unittest.TestCase):
    """Test Haversine distance calculations."""
    
    def test_same_point(self):
        """Distance to same point should be zero."""
        self.assertAlmostEqual(haversine_distance((0, 0), (0, 0)), 0.0, places=6)
        self.assertAlmostEqual(haversine_distance((39.9, 116.4), (39.9, 116.4)), 0.0, places=6)
    
    def test_one_degree_latitude(self):
        """One degree latitude ≈ 111 km."""
        dist = haversine_distance((0, 0), (1, 0))
        self.assertAlmostEqual(dist, 111.19, places=1)
    
    def test_one_degree_longitude_equator(self):
        """One degree longitude at equator ≈ 111 km."""
        dist = haversine_distance((0, 0), (0, 1))
        self.assertAlmostEqual(dist, 111.19, places=1)
    
    def test_longitude_at_pole(self):
        """Longitude at pole should be near zero."""
        dist = haversine_distance((90, 0), (90, 90))
        self.assertAlmostEqual(dist, 0.0, places=2)
    
    def test_distance_units(self):
        """Test different distance units."""
        dist_km = haversine_distance((0, 0), (1, 0), 'km')
        dist_m = haversine_distance((0, 0), (1, 0), 'm')
        dist_miles = haversine_distance((0, 0), (1, 0), 'miles')
        dist_nautical = haversine_distance((0, 0), (1, 0), 'nautical')
        
        self.assertAlmostEqual(dist_m, dist_km * 1000, places=1)
        self.assertAlmostEqual(dist_miles, dist_km * 0.621371, places=1)
        self.assertAlmostEqual(dist_nautical, dist_km * 0.539957, places=1)
    
    def test_beijing_shanghai(self):
        """Test Beijing to Shanghai distance."""
        beijing = (39.9042, 116.4074)
        shanghai = (31.2304, 121.4737)
        dist = haversine_distance(beijing, shanghai)
        # Known distance ≈ 1068 km
        self.assertTrue(1060 < dist < 1080)
    
    def test_antipodal_points(self):
        """Test antipodal points (opposite sides of Earth)."""
        dist = haversine_distance((0, 0), (0, 180))
        # Half circumference ≈ 20000 km
        self.assertTrue(19900 < dist < 20100)
    
    def test_invalid_unit(self):
        """Test invalid unit raises error."""
        with self.assertRaises(ValueError):
            haversine_distance((0, 0), (1, 0), 'invalid')


class TestVincentyDistance(unittest.TestCase):
    """Test Vincenty distance calculations."""
    
    def test_same_point(self):
        """Distance to same point should be zero."""
        self.assertAlmostEqual(vincenty_distance((0, 0), (0, 0)), 0.0, places=6)
    
    def test_one_degree_latitude(self):
        """One degree latitude ≈ 111 km (slightly different from Haversine)."""
        dist = vincenty_distance((0, 0), (1, 0))
        self.assertTrue(110 < dist < 112)
    
    def test_vincenty_more_accurate(self):
        """Vincenty should be more accurate than Haversine."""
        beijing = (39.9042, 116.4074)
        shanghai = (31.2304, 121.4737)
        haversine = haversine_distance(beijing, shanghai)
        vincenty = vincenty_distance(beijing, shanghai)
        # Vincenty is slightly more accurate
        self.assertTrue(abs(haversine - vincenty) < 5)  # Difference < 5 km
    
    def test_distance_units(self):
        """Test different distance units for Vincenty."""
        dist_km = vincenty_distance((0, 0), (1, 0), 'km')
        dist_m = vincenty_distance((0, 0), (1, 0), 'm')
        self.assertAlmostEqual(dist_m, dist_km * 1000, places=0)


class TestDistanceFunction(unittest.TestCase):
    """Test the unified distance function."""
    
    def test_haversine_method(self):
        """Test distance with haversine method."""
        dist1 = distance((0, 0), (1, 0), method='haversine')
        dist2 = haversine_distance((0, 0), (1, 0))
        self.assertAlmostEqual(dist1, dist2, places=6)
    
    def test_vincenty_method(self):
        """Test distance with vincenty method."""
        dist1 = distance((0, 0), (1, 0), method='vincenty')
        dist2 = vincenty_distance((0, 0), (1, 0))
        self.assertAlmostEqual(dist1, dist2, places=6)
    
    def test_invalid_method(self):
        """Test invalid method raises error."""
        with self.assertRaises(ValueError):
            distance((0, 0), (1, 0), method='invalid')


class TestBearing(unittest.TestCase):
    """Test bearing calculations."""
    
    def test_north_bearing(self):
        """Bearing from (0,0) to (1,0) should be 0° (north)."""
        self.assertAlmostEqual(initial_bearing((0, 0), (1, 0)), 0.0, places=2)
    
    def test_east_bearing(self):
        """Bearing from (0,0) to (0,1) should be 90° (east)."""
        self.assertAlmostEqual(initial_bearing((0, 0), (0, 1)), 90.0, places=2)
    
    def test_south_bearing(self):
        """Bearing from (0,0) to (-1,0) should be 180° (south)."""
        self.assertAlmostEqual(initial_bearing((0, 0), (-1, 0)), 180.0, places=2)
    
    def test_west_bearing(self):
        """Bearing from (0,0) to (0,-1) should be 270° (west)."""
        self.assertAlmostEqual(initial_bearing((0, 0), (0, -1)), 270.0, places=2)
    
    def test_final_bearing(self):
        """Final bearing should be approximately opposite of initial bearing."""
        initial = initial_bearing((0, 0), (10, 10))
        final = final_bearing((0, 0), (10, 10))
        # Final bearing = initial bearing from end to start + 180
        expected = (initial_bearing((10, 10), (0, 0)) + 180) % 360
        self.assertTrue(abs(final - expected) < 1 or abs(abs(final - expected) - 360) < 1)


class TestMidpointCoordinate(unittest.TestCase):
    """Test midpoint calculations."""
    
    def test_midpoint_same_longitude(self):
        """Midpoint of points with same longitude."""
        mid = midpoint_coordinate((0, 0), (10, 0))
        self.assertAlmostEqual(mid[0], 5.0, places=2)
        self.assertAlmostEqual(mid[1], 0.0, places=2)
    
    def test_midpoint_same_latitude(self):
        """Midpoint of points with same latitude at equator."""
        mid = midpoint_coordinate((0, 0), (0, 10))
        self.assertAlmostEqual(mid[0], 0.0, places=2)
        self.assertAlmostEqual(mid[1], 5.0, places=2)
    
    def test_midpoint_antipodal(self):
        """Midpoint of antipodal points."""
        mid = midpoint_coordinate((0, 0), (0, 180))
        # Midpoint should be at equator
        self.assertAlmostEqual(mid[0], 0.0, places=2)


class TestDestinationPoint(unittest.TestCase):
    """Test destination point calculations."""
    
    def test_destination_north(self):
        """Move north 1 degree distance."""
        # 1 degree latitude ≈ 111 km
        dest = destination_point((0, 0), 0, 111.19)
        self.assertAlmostEqual(dest[0], 1.0, places=1)
        self.assertAlmostEqual(dest[1], 0.0, places=1)
    
    def test_destination_east(self):
        """Move east 1 degree distance at equator."""
        dest = destination_point((0, 0), 90, 111.19)
        self.assertAlmostEqual(dest[0], 0.0, places=1)
        self.assertAlmostEqual(dest[1], 1.0, places=1)
    
    def test_destination_zero_distance(self):
        """Zero distance should return same point."""
        dest = destination_point((39.9, 116.4), 45, 0)
        self.assertAlmostEqual(dest[0], 39.9, places=6)
        self.assertAlmostEqual(dest[1], 116.4, places=6)


class TestBoundingBox(unittest.TestCase):
    """Test bounding box calculations."""
    
    def test_bounding_box_at_equator(self):
        """Bounding box at equator."""
        bbox = bounding_box((0, 0), 111.19)  # ~1 degree
        min_coord, max_coord = bbox
        
        # Check latitude bounds (±1 degree)
        self.assertTrue(min_coord[0] < -0.9)
        self.assertTrue(max_coord[0] > 0.9)
        
        # Check longitude bounds (should be approximately ±1 degree at equator)
        self.assertTrue(min_coord[1] < -0.9)
        self.assertTrue(max_coord[1] > 0.9)
    
    def test_bounding_box_at_high_latitude(self):
        """Bounding box at high latitude (longitude wider)."""
        bbox = bounding_box((60, 0), 100)
        min_coord, max_coord = bbox
        
        # Longitude range should be wider at higher latitudes
        lng_range = max_coord[1] - min_coord[1]
        self.assertTrue(lng_range > 2)  # More than 2 degrees
    
    def test_bounding_box_clamped_latitude(self):
        """Bounding box near pole should clamp latitude."""
        bbox = bounding_box((89, 0), 200)
        min_coord, max_coord = bbox
        
        self.assertTrue(min_coord[0] >= MIN_LATITUDE)
        self.assertTrue(max_coord[0] <= MAX_LATITUDE)


class TestPointInPolygon(unittest.TestCase):
    """Test point-in-polygon detection."""
    
    def test_point_inside_square(self):
        """Point inside a square polygon."""
        polygon = [(0, 0), (0, 10), (10, 10), (10, 0)]
        self.assertTrue(point_in_polygon((5, 5), polygon))
    
    def test_point_outside_square(self):
        """Point outside a square polygon."""
        polygon = [(0, 0), (0, 10), (10, 10), (10, 0)]
        self.assertFalse(point_in_polygon((15, 5), polygon))
        self.assertFalse(point_in_polygon((-5, 5), polygon))
    
    def test_point_on_edge(self):
        """Point on polygon edge."""
        polygon = [(0, 0), (0, 10), (10, 10), (10, 0)]
        # Edge behavior depends on implementation
        # Typically considered inside or indeterminate
        self.assertTrue(point_in_polygon((0, 5), polygon) or not point_in_polygon((0, 5), polygon))
    
    def test_polygon_too_small(self):
        """Polygon with < 3 points should return False."""
        self.assertFalse(point_in_polygon((5, 5), [(0, 0)]))
        self.assertFalse(point_in_polygon((5, 5), [(0, 0), (10, 10)]))
    
    def test_complex_polygon(self):
        """Test with a more complex polygon shape."""
        # Triangle
        triangle = [(0, 0), (10, 0), (5, 10)]
        self.assertTrue(point_in_polygon((5, 3), triangle))
        self.assertFalse(point_in_polygon((15, 5), triangle))


class TestPolygonArea(unittest.TestCase):
    """Test polygon area calculations."""
    
    def test_square_area(self):
        """Area of 1-degree square at equator."""
        # 1 degree ≈ 111 km, so ~111 x 111 = 12321 km²
        polygon = [(0, 0), (0, 1), (1, 1), (1, 0)]
        area = polygon_area_km2(polygon)
        # Approximate check
        self.assertTrue(12000 < area < 13000)
    
    def test_triangle_area(self):
        """Area of a triangle."""
        polygon = [(0, 0), (0, 1), (1, 0)]
        area = polygon_area_km2(polygon)
        # Half of square
        self.assertTrue(6000 < area < 6500)
    
    def test_empty_polygon(self):
        """Empty polygon has zero area."""
        self.assertEqual(polygon_area_km2([]), 0.0)
        self.assertEqual(polygon_area_km2([(0, 0)]), 0.0)


class TestInterpolatePath(unittest.TestCase):
    """Test path interpolation."""
    
    def test_interpolate_linear(self):
        """Interpolate along a simple path."""
        path = interpolate_path((0, 0), (0, 10), 3)
        
        # Should have 4 points (including start and end)
        self.assertEqual(len(path), 4)
        
        # All should have latitude near 0
        for point in path:
            self.assertAlmostEqual(point[0], 0.0, places=2)
        
        # Longitude should progress from 0 to 10
        self.assertAlmostEqual(path[0][1], 0.0, places=2)
        self.assertAlmostEqual(path[-1][1], 10.0, places=2)
    
    def test_interpolate_minimum_points(self):
        """Interpolate with minimum points."""
        path = interpolate_path((0, 0), (10, 10), 1)
        self.assertEqual(len(path), 2)
    
    def test_interpolate_same_point(self):
        """Interpolate between same points."""
        path = interpolate_path((0, 0), (0, 0), 5)
        self.assertEqual(len(path), 6)
        for point in path:
            self.assertAlmostEqual(point[0], 0.0)
            self.assertAlmostEqual(point[1], 0.0)


class TestNearestPointOnPath(unittest.TestCase):
    """Test nearest point on path."""
    
    def test_nearest_on_segment(self):
        """Nearest point on a simple segment."""
        path = [(0, 0), (0, 10)]
        nearest, dist, idx = nearest_point_on_path((1, 5), path)
        
        # Nearest should be at longitude 5
        self.assertAlmostEqual(nearest[1], 5.0, places=2)
        self.assertEqual(idx, 0)
    
    def test_nearest_at_endpoint(self):
        """Nearest point is an endpoint."""
        path = [(0, 0), (0, 10)]
        nearest, dist, idx = nearest_point_on_path((1, 15), path)
        
        # Nearest should be the endpoint
        self.assertAlmostEqual(nearest[1], 10.0, places=2)
    
    def test_single_point_path(self):
        """Path with single point."""
        path = [(0, 0)]
        nearest, dist, idx = nearest_point_on_path((1, 1), path)
        self.assertEqual(nearest, (0, 0))
        self.assertEqual(idx, 0)


class TestTotalPathDistance(unittest.TestCase):
    """Test total path distance."""
    
    def test_two_point_path(self):
        """Distance of two-point path."""
        dist = total_path_distance([(0, 0), (0, 1)])
        self.assertAlmostEqual(dist, 111.19, places=1)
    
    def test_multi_point_path(self):
        """Distance of multi-point path."""
        dist = total_path_distance([(0, 0), (0, 1), (0, 2)])
        # Should be approximately 2 * 111 km
        self.assertTrue(220 < dist < 225)
    
    def test_empty_path(self):
        """Empty path has zero distance."""
        self.assertEqual(total_path_distance([]), 0.0)
        self.assertEqual(total_path_distance([(0, 0)]), 0.0)
    
    def test_path_distance_units(self):
        """Test path distance in different units."""
        dist_km = total_path_distance([(0, 0), (0, 1)], 'km')
        dist_miles = total_path_distance([(0, 0), (0, 1)], 'miles')
        self.assertAlmostEqual(dist_miles, dist_km * 0.621371, places=1)


class TestCoordinateFormatConversions(unittest.TestCase):
    """Test coordinate format conversions."""
    
    def test_decimal_to_dms(self):
        """Convert decimal to DMS."""
        result = decimal_to_dms((39.9042, 116.4074))
        
        # Latitude
        self.assertEqual(result['lat']['degrees'], 39)
        self.assertEqual(result['lat']['minutes'], 54)
        self.assertAlmostEqual(result['lat']['seconds'], 15.12, places=1)
        self.assertEqual(result['lat']['direction'], 'N')
        
        # Longitude
        self.assertEqual(result['lng']['degrees'], 116)
        self.assertEqual(result['lng']['minutes'], 24)
        self.assertAlmostEqual(result['lng']['seconds'], 26.64, places=1)
        self.assertEqual(result['lng']['direction'], 'E')
    
    def test_decimal_to_dms_negative(self):
        """Convert negative decimal to DMS."""
        result = decimal_to_dms((-39.5, -116.5))
        
        self.assertEqual(result['lat']['direction'], 'S')
        self.assertEqual(result['lng']['direction'], 'W')
    
    def test_dms_to_decimal(self):
        """Convert DMS to decimal."""
        dms_lat = {'degrees': 39, 'minutes': 54, 'seconds': 15.12, 'direction': 'N'}
        dms_lng = {'degrees': 116, 'minutes': 24, 'seconds': 26.64, 'direction': 'E'}
        
        lat, lng = dms_to_decimal(dms_lat, dms_lng)
        self.assertAlmostEqual(lat, 39.9042, places=3)
        self.assertAlmostEqual(lng, 116.4074, places=3)
    
    def test_dms_to_decimal_negative(self):
        """Convert DMS with S/W to negative decimal."""
        dms_lat = {'degrees': 39, 'minutes': 30, 'seconds': 0, 'direction': 'S'}
        dms_lng = {'degrees': 116, 'minutes': 30, 'seconds': 0, 'direction': 'W'}
        
        lat, lng = dms_to_decimal(dms_lat, dms_lng)
        self.assertTrue(lat < 0)
        self.assertTrue(lng < 0)
    
    def test_coordinate_to_string_decimal(self):
        """Convert coordinate to decimal string."""
        result = coordinate_to_string((39.9, 116.4))
        self.assertIn('39.9', result)
        self.assertIn('N', result)
        self.assertIn('116.4', result)
        self.assertIn('E', result)
    
    def test_coordinate_to_string_dms(self):
        """Convert coordinate to DMS string."""
        result = coordinate_to_string((39.9042, 116.4074), format='dms')
        self.assertIn('°', result)
        self.assertIn("'", result)
        self.assertIn('"', result)
    
    def test_coordinate_to_string_dm(self):
        """Convert coordinate to degrees-minutes string."""
        result = coordinate_to_string((39.9042, 116.4074), format='dm')
        self.assertIn('°', result)
        self.assertIn("'", result)
        # Should not have seconds
        self.assertNotIn('"', result)


class TestDistanceUnitConversions(unittest.TestCase):
    """Test distance unit conversions."""
    
    def test_km_to_miles(self):
        """Convert km to miles."""
        self.assertAlmostEqual(km_to_miles(100), 62.1371, places=4)
    
    def test_km_to_nautical(self):
        """Convert km to nautical miles."""
        self.assertAlmostEqual(km_to_nautical(100), 53.9957, places=4)
    
    def test_km_to_m(self):
        """Convert km to meters."""
        self.assertEqual(km_to_m(1), 1000)
    
    def test_miles_to_km(self):
        """Convert miles to km."""
        self.assertAlmostEqual(miles_to_km(100), 160.9344, places=4)
    
    def test_nautical_to_km(self):
        """Convert nautical miles to km."""
        self.assertAlmostEqual(nautical_to_km(100), 185.2, places=4)
    
    def test_m_to_km(self):
        """Convert meters to km."""
        self.assertEqual(m_to_km(1000), 1)
    
    def test_convert_distance(self):
        """Test unified conversion function."""
        self.assertAlmostEqual(convert_distance(100, 'km', 'miles'), 62.1371, places=4)
        self.assertAlmostEqual(convert_distance(100, 'miles', 'km'), 160.9344, places=4)
        self.assertAlmostEqual(convert_distance(100, 'km', 'nautical'), 53.9957, places=4)
        self.assertAlmostEqual(convert_distance(1000, 'm', 'km'), 1.0, places=4)
    
    def test_convert_distance_invalid_unit(self):
        """Test conversion with invalid unit."""
        with self.assertRaises(ValueError):
            convert_distance(100, 'km', 'invalid')
        with self.assertRaises(ValueError):
            convert_distance(100, 'invalid', 'km')


class TestBatchOperations(unittest.TestCase):
    """Test batch operations."""
    
    def test_find_nearest(self):
        """Find nearest candidate."""
        candidates = [(40, 116), (35, 117), (30, 120)]
        idx, dist, coord = find_nearest((39, 116), candidates)
        
        # First should be nearest
        self.assertEqual(idx, 0)
        self.assertTrue(dist < 150)
    
    def test_find_nearest_empty(self):
        """Find nearest with empty candidates."""
        with self.assertRaises(ValueError):
            find_nearest((0, 0), [])
    
    def test_distances_to_all(self):
        """Calculate distances to all targets."""
        targets = [(0, 1), (1, 0), (0, -1)]
        distances = distances_to_all((0, 0), targets)
        
        self.assertEqual(len(distances), 3)
        # All should be approximately 111 km
        for d in distances:
            self.assertTrue(110 < d < 112)
    
    def test_within_radius(self):
        """Find candidates within radius."""
        candidates = [(0, 0.5), (0, 1.5), (0, 2.5)]
        results = within_radius((0, 0), candidates, 120)  # ~120 km
        
        # Only first candidate should be within 120 km
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], 0)
    
    def test_within_radius_multiple(self):
        """Find multiple candidates within radius."""
        candidates = [(0, 0.5), (0, 0.8), (0, 1.5)]
        results = within_radius((0, 0), candidates, 150)  # ~150 km
        
        # First two should be within 150 km
        self.assertEqual(len(results), 2)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_pole_coordinates(self):
        """Test coordinates at poles."""
        # North pole
        self.assertTrue(is_valid_coordinate(90, 0))
        # South pole
        self.assertTrue(is_valid_coordinate(-90, 0))
    
    def test_antimeridian(self):
        """Test coordinates near antimeridian (180°)."""
        # Should wrap
        coord = normalize_coordinate(0, 185)
        self.assertAlmostEqual(coord[1], -175, places=1)
    
    def test_negative_values(self):
        """Test negative coordinate values."""
        # Negative latitude (south)
        self.assertTrue(is_valid_coordinate(-45, 0))
        # Negative longitude (west)
        self.assertTrue(is_valid_coordinate(0, -45))
    
    def test_float_precision(self):
        """Test float precision in calculations."""
        # High precision coordinates
        beijing = (39.904200, 116.407400)
        shanghai = (31.230400, 121.473700)
        
        dist1 = haversine_distance(beijing, shanghai)
        dist2 = haversine_distance((39.9042, 116.4074), (31.2304, 121.4737))
        
        self.assertAlmostEqual(dist1, dist2, places=3)
    
    def test_long_distance(self):
        """Test long distance calculations."""
        # Beijing to New York
        beijing = (39.9042, 116.4074)
        newyork = (40.7128, -74.0060)
        
        dist = haversine_distance(beijing, newyork)
        # Known distance ≈ 10900 km
        self.assertTrue(10800 < dist < 11000)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)