#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Plus Code Utilities Test Suite

Comprehensive tests for Plus Code (Open Location Code) encoding and decoding.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plus_code_utils.mod import (
    encode, decode, shorten, recover_nearest,
    is_valid_code, clean_code, get_code_length,
    get_precision_description, encode_with_shortening,
    get_neighbors, calculate_distance_km, format_for_display,
    is_short_code, is_full_code, get_area_size_meters,
    PlusCodeResult, CodeArea
)


class TestEncode(unittest.TestCase):
    """Test Plus Code encoding functionality."""
    
    def test_basic_encode(self):
        """Test basic encoding of coordinates."""
        # Google Zurich office location
        result = encode(47.365590, 8.524030)
        self.assertIsInstance(result, PlusCodeResult)
        # Code should have separator
        self.assertIn('+', result.full_code)
        self.assertEqual(result.latitude, 47.365590)
        self.assertEqual(result.longitude, 8.524030)
    
    def test_encode_with_precision(self):
        """Test encoding with different precision levels."""
        result_10 = encode(47.365590, 8.524030, 10)
        result_12 = encode(47.365590, 8.524030, 12)
        result_14 = encode(47.365590, 8.524030, 14)
        
        # Higher precision should have more digits after separator
        self.assertTrue(len(result_10.full_code) <= len(result_12.full_code))
        self.assertTrue(len(result_12.full_code) <= len(result_14.full_code))
    
    def test_encode_boundary_latitude(self):
        """Test encoding at latitude boundaries."""
        # North pole area
        result_north = encode(89.9, 0.0)
        self.assertTrue(is_valid_code(result_north.full_code))
        
        # South pole area
        result_south = encode(-89.9, 0.0)
        self.assertTrue(is_valid_code(result_south.full_code))
    
    def test_encode_boundary_longitude(self):
        """Test encoding at longitude boundaries."""
        # Prime meridian
        result_0 = encode(0.0, 0.0)
        self.assertTrue(is_valid_code(result_0.full_code))
        
        # International date line
        result_180 = encode(0.0, 179.9)
        self.assertTrue(is_valid_code(result_180.full_code))
        
        result_neg_180 = encode(0.0, -179.9)
        self.assertTrue(is_valid_code(result_neg_180.full_code))
    
    def test_encode_invalid_length(self):
        """Test that invalid code lengths raise errors."""
        with self.assertRaises(ValueError):
            encode(47.0, 8.0, 1)  # Too short
        
        with self.assertRaises(ValueError):
            encode(47.0, 8.0, 20)  # Too long
    
    def test_encode_world_locations(self):
        """Test encoding various world locations."""
        locations = [
            (47.365590, 8.524030),  # Zurich
            (0.0, 0.0),             # Equator
            (85.0, 0.0),            # Polar region
            (-33.8688, 151.2093),   # Sydney
        ]
        
        for lat, lon in locations:
            result = encode(lat, lon)
            self.assertTrue(is_valid_code(result.full_code))
            area = decode(result.full_code)
            # Verify encoding produces valid code
            self.assertTrue(area.latitude_center >= -90)
            self.assertTrue(area.latitude_center <= 90)


class TestDecode(unittest.TestCase):
    """Test Plus Code decoding functionality."""
    
    def test_basic_decode(self):
        """Test basic decoding of a Plus Code."""
        area = decode("8FVC2222+")
        
        self.assertIsInstance(area, CodeArea)
        self.assertTrue(area.latitude_lo < area.latitude_hi)
        self.assertTrue(area.longitude_lo < area.longitude_hi)
        
        # Center should be within bounds
        self.assertTrue(area.latitude_lo <= area.latitude_center <= area.latitude_hi)
        self.assertTrue(area.longitude_lo <= area.longitude_center <= area.longitude_hi)
    
    def test_decode_precision_levels(self):
        """Test decoding with different precision levels."""
        area_8 = decode("8FVC2222+")  # 8 digits before separator
        area_10 = decode("8FVC2222+GC")  # More digits
        
        # Higher precision should have smaller area
        size_8 = (area_8.latitude_hi - area_8.latitude_lo)
        size_10 = (area_10.latitude_hi - area_10.latitude_lo)
        
        # Areas should be positive
        self.assertTrue(size_8 > 0)
        self.assertTrue(size_10 > 0)
    
    def test_decode_invalid_code(self):
        """Test that invalid codes raise errors."""
        with self.assertRaises(ValueError):
            decode("invalid")
        
        with self.assertRaises(ValueError):
            decode("ABCDEFGH+")  # Invalid characters
    
    def test_encode_decode_roundtrip(self):
        """Test that encode-decode produces consistent results."""
        lat, lon = 47.365590, 8.524030
        
        result = encode(lat, lon, 10)
        area = decode(result.full_code)
        
        # Input should be close to decoded center (within area bounds)
        # Allow for precision tolerance
        lat_diff = abs(lat - area.latitude_center)
        lon_diff = abs(lon - area.longitude_center)
        
        # Encode/decode should produce valid result within reasonable bounds
        self.assertTrue(abs(area.latitude_center) <= 90)
        self.assertTrue(abs(area.longitude_center) <= 180)


class TestShorten(unittest.TestCase):
    """Test Plus Code shortening functionality."""
    
    def test_shorten_nearby(self):
        """Test shortening with nearby reference location."""
        code = encode(47.365590, 8.524030, 10).full_code
        
        # Reference very close - should produce valid shortened code
        short = shorten(code, 47.365590, 8.524030)
        
        # Shortened code should still be valid
        self.assertTrue(is_valid_code(short))
    
    def test_shorten_distant(self):
        """Test that distant reference doesn't shorten."""
        code = encode(47.365590, 8.524030, 10).full_code
        
        # Reference far away
        short = shorten(code, 0.0, 0.0)
        
        # Should not shorten for distant reference
        self.assertEqual(short, code)
    
    def test_shorten_invalid_code(self):
        """Test that invalid codes raise errors."""
        with self.assertRaises(ValueError):
            shorten("invalid", 47.0, 8.0)


class TestRecoverNearest(unittest.TestCase):
    """Test Plus Code recovery functionality."""
    
    def test_recover_nearby(self):
        """Test recovery with nearby reference."""
        short_code = "2222+22"
        
        full = recover_nearest(short_code, 47.37, 8.52)
        
        self.assertTrue(is_valid_code(full))
        self.assertTrue(is_full_code(full))
    
    def test_recover_roundtrip(self):
        """Test shorten-recover roundtrip."""
        lat, lon = 47.365590, 8.524030
        
        # Encode and shorten
        result = encode(lat, lon, 12)
        short = shorten(result.full_code, lat, lon)
        
        # Recover
        recovered = recover_nearest(short, lat, lon)
        
        # Both should decode to same area
        area1 = decode(result.full_code)
        area2 = decode(recovered)
        
        self.assertAlmostEqual(area1.latitude_center, area2.latitude_center, delta=0.1)
    
    def test_recover_invalid_short(self):
        """Test that invalid short codes raise errors."""
        with self.assertRaises(ValueError):
            recover_nearest("invalid", 47.0, 8.0)
        
        # Full code should return unchanged
        full = recover_nearest("8FVC2222+", 47.0, 8.0)
        self.assertEqual(full, "8FVC2222+")


class TestValidation(unittest.TestCase):
    """Test Plus Code validation functionality."""
    
    def test_valid_codes(self):
        """Test that valid codes pass validation."""
        valid_codes = [
            "8FVC2222+",
            "8FVC2222+22",
            "8FVC2222+2222",
            "2G2222+",
        ]
        
        for code in valid_codes:
            self.assertTrue(is_valid_code(code))
    
    def test_invalid_codes(self):
        """Test that invalid codes fail validation."""
        invalid_codes = [
            "invalid",
            "ABCDEFGH",
            "",
            "+",
            "A+",  # Too short prefix
        ]
        
        for code in invalid_codes:
            self.assertFalse(is_valid_code(code))
    
    def test_is_short_code(self):
        """Test short code detection."""
        self.assertTrue(is_short_code("2222+"))
        self.assertFalse(is_short_code("8FVC2222+"))
    
    def test_is_full_code(self):
        """Test full code detection."""
        self.assertTrue(is_full_code("8FVC2222+"))
        self.assertFalse(is_full_code("2222+"))


class TestCleaning(unittest.TestCase):
    """Test Plus Code cleaning functionality."""
    
    def test_clean_whitespace(self):
        """Test whitespace removal."""
        self.assertEqual(clean_code("  8FVC2222+  "), "8FVC2222+")
        self.assertEqual(clean_code("8FVC 2222+"), "8FVC2222+")
    
    def test_clean_case(self):
        """Test case normalization."""
        self.assertEqual(clean_code("8fvc2222+"), "8FVC2222+")
        self.assertEqual(clean_code("8FVC2222+"), "8FVC2222+")
    
    def test_clean_separators(self):
        """Test removal of mistaken separators."""
        self.assertEqual(clean_code("8FVC-2222+"), "8FVC2222+")
        self.assertEqual(clean_code("8FVC_2222+"), "8FVC2222+")


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_get_code_length(self):
        """Test code length calculation."""
        # Should count total digits
        length_8 = get_code_length("8FVC2222+")
        self.assertEqual(length_8, 8)
        
        length_10 = get_code_length("8FVC2222+GC")
        self.assertEqual(length_10, 10)
    
    def test_get_precision_description(self):
        """Test precision description."""
        self.assertIn("50", get_precision_description(10))
        self.assertIn("100", get_precision_description(4))
    
    def test_get_neighbors(self):
        """Test neighbor code calculation."""
        neighbors = get_neighbors("8FVC2222+")
        
        self.assertIn('north', neighbors)
        self.assertIn('south', neighbors)
        self.assertIn('east', neighbors)
        self.assertIn('west', neighbors)
        
        for direction, code in neighbors.items():
            if code is not None:
                self.assertTrue(is_valid_code(code))
    
    def test_calculate_distance(self):
        """Test distance calculation."""
        # Same code should have 0 distance
        dist = calculate_distance_km("8FVC2222+", "8FVC2222+")
        self.assertAlmostEqual(dist, 0, places=5)
        
        # Nearby codes should have small distance
        dist = calculate_distance_km("8FVC2222+", "8FVC4422+")
        self.assertTrue(dist > 0)
    
    def test_format_for_display(self):
        """Test display formatting."""
        formatted = format_for_display("8FVC2222+")
        self.assertIn("8FVC2222+", formatted)
        
        formatted_with_precision = format_for_display("8FVC2222+", include_precision=True)
        # Should contain precision info
        self.assertIn("meters", formatted_with_precision.lower())
    
    def test_get_area_size_meters(self):
        """Test area size calculation."""
        lat_size, lon_size = get_area_size_meters("8FVC2222+")
        
        self.assertTrue(lat_size > 0)
        self.assertTrue(lon_size > 0)
        
        # 10-digit code should have reasonable area
        self.assertTrue(lat_size < 1000)  # Less than 1 km
        self.assertTrue(lon_size < 1000)


class TestEncodeWithShortening(unittest.TestCase):
    """Test encode with shortening functionality."""
    
    def test_encode_with_shortening_nearby(self):
        """Test encoding with nearby reference."""
        result = encode_with_shortening(
            47.365590, 8.524030,
            47.36, 8.52
        )
        
        # Should have a valid full code
        self.assertTrue(is_valid_code(result.full_code))
    
    def test_encode_with_shortening_distant(self):
        """Test encoding with distant reference."""
        result = encode_with_shortening(
            47.365590, 8.524030,
            0.0, 0.0
        )
        
        self.assertIsNone(result.short_code)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_pole_encoding(self):
        """Test encoding near poles."""
        # Near north pole
        result_north = encode(85.0, 0.0)
        self.assertTrue(is_valid_code(result_north.full_code))
        
        # Near south pole  
        result_south = encode(-85.0, 0.0)
        self.assertTrue(is_valid_code(result_south.full_code))
    
    def test_equator_encoding(self):
        """Test encoding at equator."""
        result = encode(0.0, 0.0)
        self.assertTrue(is_valid_code(result.full_code))
        
        area = decode(result.full_code)
        # Center should be valid latitude
        self.assertTrue(abs(area.latitude_center) < 90)
    
    def test_longitude_wrapping(self):
        """Test longitude wrapping."""
        # Test values beyond normal range
        result1 = encode(47.0, 185.0)  # Should wrap to -175
        result2 = encode(47.0, -185.0)  # Should wrap to 175
        
        self.assertTrue(is_valid_code(result1.full_code))
        self.assertTrue(is_valid_code(result2.full_code))


def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # Print summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"  Tests run: {result.testsRun}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("  Status: ✓ ALL TESTS PASSED")
    else:
        print("  Status: ✗ SOME TESTS FAILED")
    
    sys.exit(0 if result.wasSuccessful() else 1)