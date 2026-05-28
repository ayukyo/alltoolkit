"""
Test suite for GPS Utilities.

Run with: python gps_utils_test.py
Or with pytest: pytest gps_utils_test.py -v
"""

import unittest
import math
from gps_utils import (
    # 数据类
    Coordinate, BoundingBox, UTMCoordinate, CoordinateFormat,
    # 转换器
    GPSConverter,
    # 计算器
    GPSCalculator,
    # 解析器
    GPSParser,
    # 验证器
    GPSValidator,
    # 格式化器
    GPSFormatter,
    # 便捷函数
    parse_gps, distance_between, bearing_to, midpoint_of,
    destination_from, create_bbox, dd_to_dms, dms_to_dd,
    format_gps, validate_gps, is_in_region, get_region,
    create_coordinate, total_track_distance, maps_url,
)


class TestCoordinate(unittest.TestCase):
    """Tests for Coordinate class."""
    
    def test_create_coordinate(self):
        """Test creating a coordinate."""
        coord = Coordinate(39.9042, 116.4074)
        
        self.assertEqual(coord.latitude, 39.9042)
        self.assertEqual(coord.longitude, 116.4074)
        self.assertIsNone(coord.altitude)
    
    def test_create_coordinate_with_altitude(self):
        """Test creating a coordinate with altitude."""
        coord = Coordinate(39.9042, 116.4074, 50.0)
        
        self.assertEqual(coord.altitude, 50.0)
    
    def test_coordinate_validation_lat_range(self):
        """Test latitude range validation."""
        # Valid
        coord = Coordinate(90, 0)
        self.assertEqual(coord.latitude, 90)
        
        coord = Coordinate(-90, 0)
        self.assertEqual(coord.latitude, -90)
        
        # Invalid
        with self.assertRaises(ValueError):
            Coordinate(91, 0)
        
        with self.assertRaises(ValueError):
            Coordinate(-91, 0)
    
    def test_coordinate_validation_lon_range(self):
        """Test longitude range validation."""
        # Valid
        coord = Coordinate(0, 180)
        self.assertEqual(coord.longitude, 180)
        
        coord = Coordinate(0, -180)
        self.assertEqual(coord.longitude, -180)
        
        # Invalid
        with self.assertRaises(ValueError):
            Coordinate(0, 181)
        
        with self.assertRaises(ValueError):
            Coordinate(0, -181)
    
    def test_coordinate_to_dict(self):
        """Test coordinate to dict conversion."""
        coord = Coordinate(39.9042, 116.4074, 50.0)
        result = coord.to_dict()
        
        self.assertEqual(result['latitude'], 39.9042)
        self.assertEqual(result['longitude'], 116.4074)
        self.assertEqual(result['altitude'], 50.0)
    
    def test_coordinate_properties(self):
        """Test coordinate properties."""
        coord_north_east = Coordinate(45, 90)
        self.assertTrue(coord_north_east.is_north)
        self.assertTrue(coord_north_east.is_east)
        self.assertEqual(coord_north_east.hemisphere, {'lat': 'N', 'lon': 'E'})
        
        coord_south_west = Coordinate(-45, -90)
        self.assertFalse(coord_south_west.is_north)
        self.assertFalse(coord_south_west.is_east)
        self.assertEqual(coord_south_west.hemisphere, {'lat': 'S', 'lon': 'W'})


class TestGPSConverter(unittest.TestCase):
    """Tests for GPSConverter class."""
    
    def test_dd_to_dms(self):
        """Test decimal degrees to DMS conversion."""
        # Beijing latitude
        lat = 39.9042
        dms = GPSConverter.dd_to_dms(lat, is_latitude=True)
        
        self.assertEqual(dms[0], 39)  # degrees
        self.assertEqual(dms[1], 54)  # minutes
        self.assertAlmostEqual(dms[2], 15.12, places=1)  # seconds
    
    def test_dms_to_dd(self):
        """Test DMS to decimal degrees conversion."""
        dd = GPSConverter.dms_to_dd(39, 54, 15.12, 'N')
        
        self.assertAlmostEqual(dd, 39.9042, places=4)
        
        # South direction
        dd_south = GPSConverter.dms_to_dd(39, 54, 15.12, 'S')
        self.assertAlmostEqual(dd_south, -39.9042, places=4)
    
    def test_dd_to_ddm(self):
        """Test decimal degrees to DDM conversion."""
        lat = 39.9042
        ddm = GPSConverter.dd_to_ddm(lat, is_latitude=True)
        
        self.assertEqual(ddm[0], 39)  # degrees
        self.assertAlmostEqual(ddm[1], 54.252, places=2)  # minutes
    
    def test_ddm_to_dd(self):
        """Test DDM to decimal degrees conversion."""
        dd = GPSConverter.ddm_to_dd(39, 54.252, 'N')
        
        self.assertAlmostEqual(dd, 39.9042, places=4)
    
    def test_dd_dms_roundtrip(self):
        """Test roundtrip conversion DD -> DMS -> DD."""
        original = 45.5
        
        dms = GPSConverter.dd_to_dms(original)
        restored = GPSConverter.dms_to_dd(dms[0], dms[1], dms[2], 'N')
        
        self.assertAlmostEqual(original, restored, places=3)
    
    def test_dd_to_utm(self):
        """Test decimal degrees to UTM conversion."""
        # Beijing
        utm = GPSConverter.dd_to_utm(39.9042, 116.4074)
        
        self.assertEqual(utm.zone, 50)
        self.assertEqual(utm.hemisphere, 'N')
        # Easting should be around 400-500km range for zone 50
        self.assertGreater(utm.easting, 400000)
        self.assertLess(utm.easting, 600000)
    
    def test_negative_longitude_utm(self):
        """Test UTM conversion for negative longitude."""
        utm = GPSConverter.dd_to_utm(40.7128, -74.0060)  # New York
        
        self.assertEqual(utm.hemisphere, 'N')
        self.assertGreater(utm.zone, 18)
        self.assertLess(utm.zone, 20)


class TestGPSCalculator(unittest.TestCase):
    """Tests for GPSCalculator class."""
    
    def test_haversine_distance_same_point(self):
        """Test distance between same point."""
        dist = GPSCalculator.haversine_distance(39.9, 116.4, 39.9, 116.4)
        
        self.assertEqual(dist, 0)
    
    def test_haversine_distance_beijing_shanghai(self):
        """Test distance between Beijing and Shanghai."""
        beijing = (39.9042, 116.4074)
        shanghai = (31.2304, 121.4737)
        
        dist = GPSCalculator.haversine_distance(
            beijing[0], beijing[1], shanghai[0], shanghai[1]
        )
        
        # Expected around 1068 km
        self.assertGreater(dist, 1000)
        self.assertLess(dist, 1100)
    
    def test_haversine_distance_units(self):
        """Test distance in different units."""
        dist_km = GPSCalculator.haversine_distance(0, 0, 0, 1, unit='km')
        dist_m = GPSCalculator.haversine_distance(0, 0, 0, 1, unit='m')
        dist_mi = GPSCalculator.haversine_distance(0, 0, 0, 1, unit='mi')
        dist_nm = GPSCalculator.haversine_distance(0, 0, 0, 1, unit='nm')
        
        # Meter should be km * 1000
        self.assertAlmostEqual(dist_m / 1000, dist_km, places=4)
        
        # Mile should be roughly 0.6214 * km
        self.assertAlmostEqual(dist_km / dist_mi, 1.609, places=1)
    
    def test_bearing(self):
        """Test bearing calculation."""
        # North direction
        bearing = GPSCalculator.bearing(0, 0, 10, 0)
        self.assertAlmostEqual(bearing, 0, places=1)
        
        # East direction
        bearing = GPSCalculator.bearing(0, 0, 0, 10)
        self.assertAlmostEqual(bearing, 90, places=1)
        
        # South direction
        bearing = GPSCalculator.bearing(10, 0, 0, 0)
        self.assertAlmostEqual(bearing, 180, places=1)
    
    def test_midpoint(self):
        """Test midpoint calculation."""
        mid = GPSCalculator.midpoint(0, 0, 10, 0)
        
        self.assertAlmostEqual(mid[0], 5, places=1)
    
    def test_destination_point(self):
        """Test destination point calculation."""
        # Move north 100 km
        dest = GPSCalculator.destination_point(0, 0, 0, 100, 'km')
        
        # Should be approximately 0.9 degrees north
        self.assertGreater(dest[0], 0.8)
        self.assertLess(dest[0], 1.0)
        self.assertAlmostEqual(dest[1], 0, places=4)
    
    def test_bounding_box(self):
        """Test bounding box creation."""
        bbox = GPSCalculator.bounding_box(39.9042, 116.4074, 10, 'km')
        
        self.assertIsInstance(bbox, BoundingBox)
        self.assertGreater(bbox.max_lat, bbox.min_lat)
        self.assertGreater(bbox.max_lon, bbox.min_lon)
    
    def test_total_distance_empty(self):
        """Test total distance with empty list."""
        dist = GPSCalculator.total_distance([])
        
        self.assertEqual(dist, 0)
    
    def test_total_distance_single_point(self):
        """Test total distance with single point."""
        dist = GPSCalculator.total_distance([(39.9, 116.4)])
        
        self.assertEqual(dist, 0)
    
    def test_total_distance_multiple_points(self):
        """Test total distance with multiple points."""
        coords = [(39.9042, 116.4074), (35.0, 117.0), (31.2304, 121.4737)]
        
        dist = GPSCalculator.total_distance(coords)
        
        # Should be Beijing -> Jinan area -> Shanghai
        # Total should be more than direct Beijing-Shanghai distance
        self.assertGreater(dist, 1000)
    
    def test_average_speed_invalid(self):
        """Test average speed with invalid inputs."""
        # Empty
        speed = GPSCalculator.average_speed([], [])
        self.assertEqual(speed, 0)
        
        # None
        speed = GPSCalculator.average_speed(None, None)
        self.assertEqual(speed, 0)


class TestBoundingBox(unittest.TestCase):
    """Tests for BoundingBox class."""
    
    def test_bbox_creation(self):
        """Test bounding box creation."""
        bbox = BoundingBox(30, 40, 100, 120)
        
        self.assertEqual(bbox.min_lat, 30)
        self.assertEqual(bbox.max_lat, 40)
        self.assertEqual(bbox.min_lon, 100)
        self.assertEqual(bbox.max_lon, 120)
    
    def test_bbox_contains(self):
        """Test bounding box contains check."""
        bbox = BoundingBox(30, 40, 100, 120)
        
        inside = Coordinate(35, 110)
        outside = Coordinate(45, 110)
        
        self.assertTrue(bbox.contains(inside))
        self.assertFalse(bbox.contains(outside))
    
    def test_bbox_center(self):
        """Test bounding box center."""
        bbox = BoundingBox(30, 40, 100, 120)
        center = bbox.center()
        
        self.assertEqual(center.latitude, 35)
        self.assertEqual(center.longitude, 110)
    
    def test_bbox_dimensions(self):
        """Test bounding box dimensions."""
        bbox = BoundingBox(39, 40, 116, 117)
        
        width = bbox.width_km()
        height = bbox.height_km()
        
        # Roughly 1 degree at this latitude
        self.assertGreater(width, 80)
        self.assertLess(width, 120)
        self.assertGreater(height, 100)
        self.assertLess(height, 120)
    
    def test_bbox_validation(self):
        """Test bounding box validation."""
        # Invalid: min > max
        with self.assertRaises(ValueError):
            BoundingBox(40, 30, 100, 120)


class TestGPSParser(unittest.TestCase):
    """Tests for GPSParser class."""
    
    def test_parse_dms_format(self):
        """Test parsing DMS format."""
        value, dir_ = GPSParser.parse("39°54'15\"N")
        
        self.assertAlmostEqual(value, 39.904, places=2)
        self.assertEqual(dir_, 'N')
    
    def test_parse_ddm_format(self):
        """Test parsing DDM format."""
        value, dir_ = GPSParser.parse("39°54.25'N")
        
        self.assertAlmostEqual(value, 39.9042, places=3)
    
    def test_parse_dd_format(self):
        """Test parsing decimal degrees format."""
        value, dir_ = GPSParser.parse("39.9042°N")
        
        self.assertAlmostEqual(value, 39.9042, places=4)
    
    def test_parse_nMEA_format(self):
        """Test parsing NMEA format."""
        value, dir_ = GPSParser.parse("3954.2500,N")
        
        self.assertAlmostEqual(value, 39.9042, places=3)
    
    def test_parse_pure_number(self):
        """Test parsing pure number."""
        value, dir_ = GPSParser.parse("45.5")
        
        self.assertAlmostEqual(value, 45.5, places=4)
        self.assertIsNone(dir_)
    
    def test_parse_coordinate_pair_comma(self):
        """Test parsing coordinate pair with comma."""
        coord = GPSParser.parse_coordinate_pair("39.9042, 116.4074")
        
        self.assertEqual(coord.latitude, 39.9042)
        self.assertEqual(coord.longitude, 116.4074)
    
    def test_parse_coordinate_pair_space(self):
        """Test parsing coordinate pair with space."""
        coord = GPSParser.parse_coordinate_pair("39.9042 116.4074")
        
        self.assertEqual(coord.latitude, 39.9042)
        self.assertEqual(coord.longitude, 116.4074)
    
    def test_parse_geojson_point(self):
        """Test parsing GeoJSON Point."""
        geojson = {
            'type': 'Point',
            'coordinates': [116.4074, 39.9042]
        }
        
        coords = GPSParser.parse_geojson(geojson)
        
        self.assertEqual(len(coords), 1)
        self.assertEqual(coords[0].latitude, 39.9042)
        self.assertEqual(coords[0].longitude, 116.4074)
    
    def test_parse_geojson_linestring(self):
        """Test parsing GeoJSON LineString."""
        geojson = {
            'type': 'LineString',
            'coordinates': [[116, 39], [117, 40], [118, 41]]
        }
        
        coords = GPSParser.parse_geojson(geojson)
        
        self.assertEqual(len(coords), 3)
    
    def test_parse_invalid(self):
        """Test parsing invalid format."""
        with self.assertRaises(ValueError):
            GPSParser.parse("not a coordinate")


class TestGPSValidator(unittest.TestCase):
    """Tests for GPSValidator class."""
    
    def test_is_valid_latitude(self):
        """Test latitude validation."""
        self.assertTrue(GPSValidator.is_valid_latitude(45))
        self.assertTrue(GPSValidator.is_valid_latitude(-45))
        self.assertTrue(GPSValidator.is_valid_latitude(90))
        self.assertTrue(GPSValidator.is_valid_latitude(-90))
        self.assertFalse(GPSValidator.is_valid_latitude(91))
        self.assertFalse(GPSValidator.is_valid_latitude(-91))
    
    def test_is_valid_longitude(self):
        """Test longitude validation."""
        self.assertTrue(GPSValidator.is_valid_longitude(90))
        self.assertTrue(GPSValidator.is_valid_longitude(-90))
        self.assertTrue(GPSValidator.is_valid_longitude(180))
        self.assertTrue(GPSValidator.is_valid_longitude(-180))
        self.assertFalse(GPSValidator.is_valid_longitude(181))
        self.assertFalse(GPSValidator.is_valid_longitude(-181))
    
    def test_validate_coordinate(self):
        """Test coordinate validation."""
        valid, msg = GPSValidator.validate_coordinate(39.9042, 116.4074)
        self.assertTrue(valid)
        self.assertEqual(msg, "")
        
        valid, msg = GPSValidator.validate_coordinate(100, 116.4074)
        self.assertFalse(valid)
        self.assertIn("纬度", msg)
    
    def test_is_near_pole(self):
        """Test pole proximity check."""
        self.assertTrue(GPSValidator.is_near_pole(85))
        self.assertTrue(GPSValidator.is_near_pole(-85))
        self.assertFalse(GPSValidator.is_near_pole(50))
    
    def test_is_near_dateline(self):
        """Test dateline proximity check."""
        self.assertTrue(GPSValidator.is_near_dateline(170))
        self.assertTrue(GPSValidator.is_near_dateline(-170))
        self.assertFalse(GPSValidator.is_near_dateline(50))
    
    def test_get_region(self):
        """Test region detection."""
        # Beijing should be in China/Asia
        region = GPSValidator.get_region(39.9042, 116.4074)
        self.assertIn(region, ['china', 'asia'])
        
        # New York should be in USA
        region = GPSValidator.get_region(40.7128, -74.0060)
        self.assertEqual(region, 'usa')
    
    def test_is_in_region(self):
        """Test region check."""
        self.assertTrue(GPSValidator.is_in_region(39.9042, 116.4074, 'china'))
        self.assertTrue(GPSValidator.is_in_region(39.9042, 116.4074, 'asia'))
        self.assertFalse(GPSValidator.is_in_region(39.9042, 116.4074, 'usa'))
    
    def test_invalid_region(self):
        """Test invalid region name."""
        self.assertFalse(GPSValidator.is_in_region(39.9, 116.4, 'invalid_region'))


class TestGPSFormatter(unittest.TestCase):
    """Tests for GPSFormatter class."""
    
    def test_format_dd(self):
        """Test decimal degrees formatting."""
        result = GPSFormatter.format_dd(39.9042, 116.4074, precision=4)
        
        self.assertIn("39.9042", result)
        self.assertIn("116.4074", result)
    
    def test_format_dms(self):
        """Test DMS formatting."""
        result = GPSFormatter.format_dms(39.9042, 116.4074)
        
        self.assertIn("39°", result)
        self.assertIn("N", result)
        self.assertIn("E", result)
    
    def test_format_ddm(self):
        """Test DDM formatting."""
        result = GPSFormatter.format_ddm(39.9042, 116.4074)
        
        self.assertIn("39°", result)
        self.assertIn("'", result)
    
    def test_format_nMEA(self):
        """Test NMEA formatting."""
        result = GPSFormatter.format_nMEA(39.9042, 116.4074)
        
        self.assertIn(",", result)
        self.assertIn("N", result)
        self.assertIn("E", result)
    
    def test_format_distance_km(self):
        """Test distance formatting (km)."""
        result = GPSFormatter.format_distance(1.5, 'km')
        self.assertEqual(result, "1.5 km")
        
        result = GPSFormatter.format_distance(0.5, 'km')
        self.assertEqual(result, "500 m")
    
    def test_format_distance_m(self):
        """Test distance formatting (m)."""
        result = GPSFormatter.format_distance(1500, 'm')
        self.assertEqual(result, "1.5 km")
        
        result = GPSFormatter.format_distance(500, 'm')
        self.assertEqual(result, "500 m")
    
    def test_format_bearing(self):
        """Test bearing formatting."""
        result = GPSFormatter.format_bearing(45)
        
        self.assertIn("45", result)
        self.assertIn("NE", result)
    
    def test_format_geojson_point(self):
        """Test GeoJSON Point formatting."""
        result = GPSFormatter.format_geojson_point(39.9042, 116.4074)
        
        self.assertEqual(result['type'], 'Point')
        self.assertEqual(result['coordinates'], [116.4074, 39.9042])
    
    def test_format_geojson_line(self):
        """Test GeoJSON LineString formatting."""
        coords = [(39.9, 116.4), (40.0, 117.0)]
        result = GPSFormatter.format_geojson_line(coords)
        
        self.assertEqual(result['type'], 'LineString')
        self.assertEqual(len(result['coordinates']), 2)
    
    def test_format_google_maps_url(self):
        """Test Google Maps URL formatting."""
        result = GPSFormatter.format_google_maps_url(39.9042, 116.4074)
        
        self.assertIn("google.com", result)
        self.assertIn("39.9042", result)
        self.assertIn("116.4074", result)
    
    def test_format_openstreetmap_url(self):
        """Test OpenStreetMap URL formatting."""
        result = GPSFormatter.format_openstreetmap_url(39.9042, 116.4074)
        
        self.assertIn("openstreetmap.org", result)
        self.assertIn("39.9042", result)
        self.assertIn("116.4074", result)


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for convenience functions."""
    
    def test_distance_between(self):
        """Test distance_between function."""
        dist = distance_between(0, 0, 0, 1)
        
        self.assertGreater(dist, 100)  # At least 100 km for 1 degree longitude at equator
        self.assertLess(dist, 120)
    
    def test_bearing_to(self):
        """Test bearing_to function."""
        bearing = bearing_to(0, 0, 0, 10)
        
        self.assertAlmostEqual(bearing, 90, places=1)
    
    def test_midpoint_of(self):
        """Test midpoint_of function."""
        mid = midpoint_of(0, 0, 10, 0)
        
        self.assertAlmostEqual(mid[0], 5, places=1)
    
    def test_destination_from(self):
        """Test destination_from function."""
        dest = destination_from(0, 0, 0, 100)
        
        self.assertGreater(dest[0], 0.8)
        self.assertLess(dest[0], 1.0)
    
    def test_create_bbox(self):
        """Test create_bbox function."""
        bbox = create_bbox(39.9, 116.4, 10)
        
        self.assertIsInstance(bbox, BoundingBox)
    
    def test_dd_to_dms(self):
        """Test dd_to_dms convenience function."""
        dms = dd_to_dms(39.9042)
        
        self.assertEqual(dms[0], 39)
    
    def test_dms_to_dd(self):
        """Test dms_to_dd convenience function."""
        dd = dms_to_dd(39, 54, 15, 'N')
        
        self.assertAlmostEqual(dd, 39.904, places=2)
    
    def test_format_gps(self):
        """Test format_gps convenience function."""
        result = format_gps(39.9042, 116.4074, 'dms')
        
        self.assertIn("°", result)
    
    def test_validate_gps(self):
        """Test validate_gps convenience function."""
        valid, msg = validate_gps(39.9, 116.4)
        self.assertTrue(valid)
    
    def test_create_coordinate(self):
        """Test create_coordinate convenience function."""
        coord = create_coordinate(39.9, 116.4)
        
        self.assertIsInstance(coord, Coordinate)
        self.assertEqual(coord.latitude, 39.9)
    
    def test_total_track_distance(self):
        """Test total_track_distance convenience function."""
        dist = total_track_distance([(0, 0), (0, 1)])
        
        self.assertGreater(dist, 100)
    
    def test_maps_url(self):
        """Test maps_url convenience function."""
        url = maps_url(39.9, 116.4, 'google')
        
        self.assertIn("google.com", url)
        
        url = maps_url(39.9, 116.4, 'osm')
        
        self.assertIn("openstreetmap.org", url)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_polar_coordinates(self):
        """Test coordinates near poles."""
        coord = Coordinate(89.9999, 0)
        
        self.assertTrue(GPSValidator.is_near_pole(coord.latitude))
    
    def test_dateline_coordinates(self):
        """Test coordinates near dateline."""
        coord = Coordinate(0, 179.9999)
        
        self.assertTrue(GPSValidator.is_near_dateline(coord.longitude))
    
    def test_negative_coordinates(self):
        """Test negative coordinates."""
        coord = Coordinate(-45.5, -120.25)
        
        self.assertFalse(coord.is_north)
        self.assertFalse(coord.is_east)
    
    def test_zero_coordinates(self):
        """Test zero coordinates."""
        coord = Coordinate(0, 0)
        
        self.assertTrue(coord.is_north)
        self.assertTrue(coord.is_east)
    
    def test_boundary_coordinates(self):
        """Test boundary coordinates."""
        # Extreme values
        coord_n = Coordinate(90, 0)
        coord_s = Coordinate(-90, 0)
        coord_e = Coordinate(0, 180)
        coord_w = Coordinate(0, -180)
        
        self.assertEqual(coord_n.latitude, 90)
        self.assertEqual(coord_s.latitude, -90)
        self.assertEqual(coord_e.longitude, 180)
        self.assertEqual(coord_w.longitude, -180)
    
    def test_high_precision_coordinates(self):
        """Test high precision coordinates."""
        coord = Coordinate(39.123456789, 116.123456789)
        
        self.assertAlmostEqual(coord.latitude, 39.123456789, places=9)
    
    def test_distance_at_equator(self):
        """Test distance calculation at equator."""
        # 1 degree longitude at equator ≈ 111.32 km
        dist = GPSCalculator.haversine_distance(0, 0, 0, 1)
        
        self.assertGreater(dist, 110)
        self.assertLess(dist, 112)
    
    def test_distance_at_high_latitude(self):
        """Test distance calculation at high latitude."""
        # 1 degree longitude at 60° latitude ≈ 55.8 km
        dist = GPSCalculator.haversine_distance(60, 0, 60, 1)
        
        self.assertGreater(dist, 55)
        self.assertLess(dist, 56)


class TestPerformance(unittest.TestCase):
    """Tests for performance optimizations."""
    
    def test_same_point_distance_zero(self):
        """Test that same point returns zero immediately."""
        dist = GPSCalculator.haversine_distance(39.9, 116.4, 39.9, 116.4)
        
        # Should be exactly 0 (optimization)
        self.assertEqual(dist, 0.0)
    
    def test_empty_track_distance_zero(self):
        """Test that empty track returns zero immediately."""
        dist = GPSCalculator.total_distance([])
        self.assertEqual(dist, 0.0)
        
        dist = GPSCalculator.total_distance(None)
        self.assertEqual(dist, 0.0)
    
    def test_single_point_distance_zero(self):
        """Test that single point returns zero immediately."""
        dist = GPSCalculator.total_distance([(39.9, 116.4)])
        self.assertEqual(dist, 0.0)
    
    def test_invalid_speed_inputs(self):
        """Test that invalid speed inputs return zero."""
        speed = GPSCalculator.average_speed(None, None)
        self.assertEqual(speed, 0.0)
        
        speed = GPSCalculator.average_speed([], [])
        self.assertEqual(speed, 0.0)
        
        # Mismatched lengths
        speed = GPSCalculator.average_speed([(0, 0), (1, 1)], [0])
        self.assertEqual(speed, 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)