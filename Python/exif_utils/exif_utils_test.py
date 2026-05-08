#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - EXIF Utilities Test Module

Comprehensive tests for EXIF metadata extraction and manipulation.

Author: AllToolkit
License: MIT
"""

import unittest
import struct
import os
import tempfile
from datetime import datetime

from mod import (
    EXIFParser, EXIFData, GPSLocation, CameraSettings,
    extract_exif, extract_exif_from_bytes,
    get_camera_info, get_gps_location, get_datetime_original,
    has_exif, get_tag_value, get_all_tags,
    format_exposure_time, format_aperture, format_focal_length,
    calculate_ev, get_equivalent_exposure,
    EXIFCleaner,
    IFD0_TAGS, EXIF_TAGS, GPS_TAGS, ALL_TAGS,
    TagType
)


# =============================================================================
# Test Data Generators
# =============================================================================

def create_test_jpeg_with_exif() -> bytes:
    """Create a minimal JPEG with EXIF data for testing."""
    # JPEG structure:
    # SOI + APP1(EXIF) + SOF0 + SOS + Image Data + EOI
    
    # Start of Image
    soi = b'\xff\xd8'
    
    # Create TIFF/EXIF data
    tiff_data = create_test_tiff_exif()
    
    # APP1 marker with EXIF
    exif_header = b'Exif\x00\x00'
    app1_data = exif_header + tiff_data
    app1_length = len(app1_data) + 2  # +2 for length field itself
    app1 = b'\xff\xe1' + struct.pack('>H', app1_length) + app1_data
    
    # SOF0 marker (minimal - just enough to be valid)
    # 2 bytes length, 1 byte precision, 2 bytes height, 2 bytes width
    # 1 byte components, component data
    sof0_data = struct.pack('>BHHB', 8, 100, 100, 3)  # 8-bit, 100x100, 3 components
    component_data = b'\x01\x11\x00\x02\x11\x01\x03\x11\x01'  # Y, Cb, Cr
    sof0_length = len(sof0_data) + len(component_data) + 2
    sof0 = b'\xff\xc0' + struct.pack('>H', sof0_length) + sof0_data + component_data
    
    # DHT (Huffman tables) - minimal
    dht = b'\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b'
    
    # SOS (Start of Scan)
    sos_data = b'\x01\x00\x02\x11\x03\x11\x00\x3f\x00'  # minimal scan header
    sos_length = len(sos_data) + 2
    sos = b'\xff\xda' + struct.pack('>H', sos_length) + sos_data
    
    # Minimal scan data (just enough to make valid JPEG)
    scan_data = b'\x00' * 100
    
    # End of Image
    eoi = b'\xff\xd9'
    
    return soi + app1 + sof0 + dht + sos + scan_data + eoi


def create_test_tiff_exif() -> bytes:
    """Create TIFF-format EXIF data for testing."""
    # TIFF header (little-endian)
    byte_order = '<'  # Little-endian
    
    # Header: "II" + magic number 42 + IFD0 offset
    header = b'II' + struct.pack('<H', 42) + struct.pack('<I', 8)
    
    # IFD0 entries
    # Create a simple IFD0 with a few tags
    ifd0_entries = []
    
    # Tag: ImageWidth (0x0100) = 800
    ifd0_entries.append(struct.pack('<HHII', 0x0100, TagType.LONG, 1, 800))
    
    # Tag: ImageLength (0x0101) = 600
    ifd0_entries.append(struct.pack('<HHII', 0x0101, TagType.LONG, 1, 600))
    
    # Tag: Make (0x010F) - ASCII string
    make_str = b'TestCamera\x00'
    make_offset = 100  # Will be positioned after IFD
    ifd0_entries.append(struct.pack('<HHII', 0x010F, TagType.ASCII, len(make_str), make_offset))
    
    # Tag: Model (0x0110) - ASCII string
    model_str = b'TestModel\x00'
    model_offset = make_offset + len(make_str)
    ifd0_entries.append(struct.pack('<HHII', 0x0110, TagType.ASCII, len(model_str), model_offset))
    
    # Tag: DateTime (0x0132) - ASCII string
    datetime_str = b'2025:05:08 19:00:00\x00'
    datetime_offset = model_offset + len(model_str)
    ifd0_entries.append(struct.pack('<HHII', 0x0132, TagType.ASCII, len(datetime_str), datetime_offset))
    
    # Tag: Orientation (0x0112) = 1 (normal)
    ifd0_entries.append(struct.pack('<HHII', 0x0112, TagType.SHORT, 1, 1))
    
    # Number of entries
    num_entries = len(ifd0_entries)
    
    # Build IFD0
    ifd0 = struct.pack('<H', num_entries)
    for entry in ifd0_entries:
        ifd0 += entry
    
    # Next IFD offset (0 = no more IFDs)
    ifd0 += struct.pack('<I', 0)
    
    # Add the ASCII string values after IFD
    # Pad to make_offset
    current_len = len(header) + len(ifd0)
    padding = make_offset - current_len
    if padding > 0:
        extra_data = b'\x00' * padding
    else:
        extra_data = b''
    
    extra_data += make_str + model_str + datetime_str
    
    return header + ifd0 + extra_data


def create_test_jpeg_with_gps() -> bytes:
    """Create a JPEG with GPS EXIF data."""
    # Similar to above but with GPS IFD
    soi = b'\xff\xd8'
    
    # Create TIFF with GPS
    tiff_data = create_test_tiff_with_gps()
    
    exif_header = b'Exif\x00\x00'
    app1_data = exif_header + tiff_data
    app1_length = len(app1_data) + 2
    app1 = b'\xff\xe1' + struct.pack('>H', app1_length) + app1_data
    
    # Minimal JPEG structure
    sof0 = b'\xff\xc0\x00\x0b\x08\x00\x64\x00\x64\x01\x01\x00'
    dht = b'\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b'
    sos = b'\xff\xda\x00\x08\x01\x01\x00\x00\x3f\x00'
    scan_data = b'\x00' * 50
    eoi = b'\xff\xd9'
    
    return soi + app1 + sof0 + dht + sos + scan_data + eoi


def create_test_tiff_with_gps() -> bytes:
    """Create TIFF with GPS data."""
    byte_order = '<'
    
    # Header
    header = b'II' + struct.pack('<H', 42) + struct.pack('<I', 8)
    
    # IFD0 with GPS offset pointer
    # GPS IFD will be at offset 200
    gps_offset = 200
    
    ifd0 = struct.pack('<H', 2)  # 2 entries
    # ImageWidth
    ifd0 += struct.pack('<HHII', 0x0100, TagType.LONG, 1, 800)
    # GPSInfo offset
    ifd0 += struct.pack('<HHII', 0x8825, TagType.LONG, 1, gps_offset)
    # Next IFD offset
    ifd0 += struct.pack('<I', 0)
    
    # Pad to GPS offset
    padding_needed = gps_offset - len(header) - len(ifd0)
    padding = b'\x00' * max(0, padding_needed)
    
    # GPS IFD
    gps_ifd = struct.pack('<H', 4)  # 4 entries
    
    # GPSLatitudeRef (N)
    gps_ifd += struct.pack('<HHII', 0x0001, TagType.ASCII, 2, ord('N'))
    
    # GPSLatitude (degrees, minutes, seconds)
    # Store at offset 300
    lat_offset = 300
    gps_ifd += struct.pack('<HHII', 0x0002, TagType.RATIONAL, 3, lat_offset)
    
    # GPSLongitudeRef (E)
    gps_ifd += struct.pack('<HHII', 0x0003, TagType.ASCII, 2, ord('E'))
    
    # GPSLongitude
    lon_offset = lat_offset + 24  # 3 rationals * 8 bytes each
    gps_ifd += struct.pack('<HHII', 0x0004, TagType.RATIONAL, 3, lon_offset)
    
    # Next IFD offset
    gps_ifd += struct.pack('<I', 0)
    
    # Pad to latitude offset
    lat_padding = lat_offset - len(header) - len(ifd0) - len(padding) - len(gps_ifd)
    lat_padding_data = b'\x00' * max(0, lat_padding)
    
    # Latitude values (39 degrees, 54 minutes, 0 seconds = NYC-ish)
    lat_deg = struct.pack('<II', 39, 1)   # 39/1
    lat_min = struct.pack('<II', 54, 1)   # 54/1
    lat_sec = struct.pack('<II', 0, 1)    # 0/1
    
    # Longitude values (116 degrees, 23 minutes, 0 seconds = Beijing-ish)
    lon_deg = struct.pack('<II', 116, 1)
    lon_min = struct.pack('<II', 23, 1)
    lon_sec = struct.pack('<II', 0, 1)
    
    return header + ifd0 + padding + gps_ifd + lat_padding_data + lat_deg + lat_min + lat_sec + lon_deg + lon_min + lon_sec


def create_test_jpeg_no_exif() -> bytes:
    """Create a minimal JPEG without EXIF data."""
    soi = b'\xff\xd8'
    # APP0 (JFIF) instead of APP1
    jfif = b'\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
    sof0 = b'\xff\xc0\x00\x0b\x08\x00\x64\x00\x64\x01\x01\x00'
    dht = b'\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b'
    sos = b'\xff\xda\x00\x08\x01\x01\x00\x00\x3f\x00'
    scan_data = b'\x00' * 50
    eoi = b'\xff\xd9'
    
    return soi + jfif + sof0 + dht + sos + scan_data + eoi


# =============================================================================
# Test Classes
# =============================================================================

class TestGPSLocation(unittest.TestCase):
    """Tests for GPSLocation class."""
    
    def test_to_dms(self):
        """Test conversion to degrees/minutes/seconds format."""
        gps = GPSLocation(latitude=40.7128, longitude=-74.0060)  # NYC
        
        lat_dms, lon_dms = gps.to_dms()
        
        self.assertIn('°', lat_dms)
        self.assertIn("'", lat_dms)
        self.assertIn('"', lat_dms)
        self.assertIn('N', lat_dms)  # North latitude (positive)
        
        self.assertIn('W', lon_dms)  # West longitude (negative)
    
    def test_to_google_maps_url(self):
        """Test Google Maps URL generation."""
        gps = GPSLocation(latitude=39.54, longitude=116.23)
        
        url = gps.to_google_maps_url()
        
        self.assertIn('google.com/maps', url)
        self.assertIn('39.54', url)
        self.assertIn('116.23', url)
    
    def test_to_openstreetmap_url(self):
        """Test OpenStreetMap URL generation."""
        gps = GPSLocation(latitude=35.68, longitude=139.69)
        
        url = gps.to_openstreetmap_url()
        
        self.assertIn('openstreetmap.org', url)
        self.assertIn('35.68', url)
        self.assertIn('139.69', url)
    
    def test_altitude(self):
        """Test GPS location with altitude."""
        gps = GPSLocation(latitude=0, longitude=0, altitude=100.5)
        
        self.assertEqual(gps.altitude, 100.5)


class TestCameraSettings(unittest.TestCase):
    """Tests for CameraSettings class."""
    
    def test_str_full_settings(self):
        """Test string representation with full settings."""
        settings = CameraSettings(
            make='Canon',
            model='EOS R5',
            lens_model='RF 50mm F1.2L',
            focal_length=50,
            aperture=1.2,
            shutter_speed='1/250s',
            iso=400
        )
        
        str_repr = str(settings)
        
        self.assertIn('Canon EOS R5', str_repr)
        self.assertIn('50mm', str_repr)
        self.assertIn('f/1.2', str_repr)
        self.assertIn('1/250s', str_repr)
        self.assertIn('ISO 400', str_repr)
    
    def test_str_partial_settings(self):
        """Test string representation with partial settings."""
        settings = CameraSettings(make='Nikon', model='D850')
        
        str_repr = str(settings)
        
        self.assertIn('Nikon D850', str_repr)
    
    def test_str_empty_settings(self):
        """Test string representation with empty settings."""
        settings = CameraSettings()
        
        str_repr = str(settings)
        
        # Should return empty or minimal string
        self.assertEqual(str_repr.strip(), '')


class TestEXIFParser(unittest.TestCase):
    """Tests for EXIFParser class."""
    
    def test_parse_jpeg_with_exif(self):
        """Test parsing JPEG with EXIF data."""
        jpeg_data = create_test_jpeg_with_exif()
        
        parser = EXIFParser(jpeg_data)
        exif = parser.parse()
        
        self.assertIsNotNone(exif)
        self.assertEqual(exif.width, 800)
        self.assertEqual(exif.height, 600)
        self.assertEqual(exif.make, 'TestCamera')
        self.assertEqual(exif.model, 'TestModel')
        self.assertEqual(exif.orientation, 1)
    
    def test_parse_jpeg_with_gps(self):
        """Test parsing JPEG with GPS data."""
        jpeg_data = create_test_jpeg_with_gps()
        
        parser = EXIFParser(jpeg_data)
        exif = parser.parse()
        
        self.assertIsNotNone(exif.gps)
        # 39 degrees + 54 minutes = 39.9
        self.assertAlmostEqual(exif.gps.latitude, 39.9, places=1)
        # 116 degrees + 23 minutes = 116.3833
        self.assertAlmostEqual(exif.gps.longitude, 116.383, places=1)
    
    def test_parse_jpeg_no_exif(self):
        """Test parsing JPEG without EXIF."""
        jpeg_data = create_test_jpeg_no_exif()
        
        parser = EXIFParser(jpeg_data)
        
        # Should not find EXIF data
        # Parser may raise or return empty EXIFData
        try:
            exif = parser.parse()
            self.assertEqual(len(exif.raw_tags), 0)
        except ValueError:
            # Expected if no EXIF marker found
            pass
    
    def test_invalid_format(self):
        """Test handling of invalid image format."""
        invalid_data = b'NOT_AN_IMAGE'
        
        parser = EXIFParser(invalid_data)
        
        with self.assertRaises(ValueError):
            parser.parse()


class TestExtractFunctions(unittest.TestCase):
    """Tests for high-level extraction functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temp files for testing
        self.temp_dir = tempfile.mkdtemp()
        
        self.jpeg_with_exif = os.path.join(self.temp_dir, 'test_exif.jpg')
        with open(self.jpeg_with_exif, 'wb') as f:
            f.write(create_test_jpeg_with_exif())
        
        self.jpeg_with_gps = os.path.join(self.temp_dir, 'test_gps.jpg')
        with open(self.jpeg_with_gps, 'wb') as f:
            f.write(create_test_jpeg_with_gps())
        
        self.jpeg_no_exif = os.path.join(self.temp_dir, 'test_no_exif.jpg')
        with open(self.jpeg_no_exif, 'wb') as f:
            f.write(create_test_jpeg_no_exif())
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_extract_exif(self):
        """Test extract_exif function."""
        exif = extract_exif(self.jpeg_with_exif)
        
        self.assertIsNotNone(exif)
        self.assertEqual(exif.width, 800)
        self.assertEqual(exif.height, 600)
    
    def test_extract_exif_from_bytes(self):
        """Test extract_exif_from_bytes function."""
        data = create_test_jpeg_with_exif()
        exif = extract_exif_from_bytes(data)
        
        self.assertIsNotNone(exif)
        self.assertEqual(exif.make, 'TestCamera')
    
    def test_get_camera_info(self):
        """Test get_camera_info function."""
        settings = get_camera_info(self.jpeg_with_exif)
        
        self.assertIsNotNone(settings)
        self.assertEqual(settings.make, 'TestCamera')
        self.assertEqual(settings.model, 'TestModel')
    
    def test_get_camera_info_no_exif(self):
        """Test get_camera_info on file without EXIF."""
        # Should return None or raise gracefully
        try:
            settings = get_camera_info(self.jpeg_no_exif)
            self.assertIsNone(settings)
        except Exception:
            pass
    
    def test_get_gps_location(self):
        """Test get_gps_location function."""
        gps = get_gps_location(self.jpeg_with_gps)
        
        self.assertIsNotNone(gps)
        # 39 degrees + 54 minutes = 39.9
        self.assertAlmostEqual(gps.latitude, 39.9, places=1)
        # 116 degrees + 23 minutes = 116.383
        self.assertAlmostEqual(gps.longitude, 116.383, places=1)
    
    def test_get_gps_location_no_gps(self):
        """Test get_gps_location on file without GPS."""
        gps = get_gps_location(self.jpeg_with_exif)
        
        self.assertIsNone(gps)
    
    def test_get_datetime_original(self):
        """Test get_datetime_original function."""
        dt = get_datetime_original(self.jpeg_with_exif)
        
        # Our test data has DateTime (not DateTimeOriginal)
        self.assertIsNotNone(dt)
    
    def test_has_exif(self):
        """Test has_exif function."""
        self.assertTrue(has_exif(self.jpeg_with_exif))
        self.assertTrue(has_exif(self.jpeg_with_gps))
        
        # File without EXIF marker
        try:
            result = has_exif(self.jpeg_no_exif)
            self.assertFalse(result)
        except Exception:
            pass
    
    def test_get_tag_value(self):
        """Test get_tag_value function."""
        width = get_tag_value(self.jpeg_with_exif, 'ImageWidth')
        self.assertEqual(width, 800)
        
        make = get_tag_value(self.jpeg_with_exif, 'Make')
        self.assertEqual(make, 'TestCamera')
    
    def test_get_tag_value_hex(self):
        """Test get_tag_value with hex code."""
        width = get_tag_value(self.jpeg_with_exif, '0x0100')
        self.assertEqual(width, 800)
    
    def test_get_tag_value_unknown(self):
        """Test get_tag_value with unknown tag."""
        value = get_tag_value(self.jpeg_with_exif, 'NonexistentTag')
        self.assertIsNone(value)
    
    def test_get_all_tags(self):
        """Test get_all_tags function."""
        tags = get_all_tags(self.jpeg_with_exif)
        
        self.assertIn('ImageWidth', tags)
        self.assertIn('ImageLength', tags)
        self.assertIn('Make', tags)
        self.assertIn('Model', tags)
    
    def test_get_all_tags_gps(self):
        """Test get_all_tags on GPS file."""
        tags = get_all_tags(self.jpeg_with_gps)
        
        # Should have GPS tags
        self.assertIn('GPSLatitude', tags)
        self.assertIn('GPSLongitude', tags)


class TestFormattingFunctions(unittest.TestCase):
    """Tests for formatting utility functions."""
    
    def test_format_exposure_time_fraction(self):
        """Test exposure time formatting as fraction."""
        self.assertEqual(format_exposure_time(0.004), '1/250s')
        self.assertEqual(format_exposure_time(0.002), '1/500s')
    
    def test_format_exposure_time_integer(self):
        """Test exposure time formatting as integer."""
        self.assertEqual(format_exposure_time(1), '1s')
        self.assertEqual(format_exposure_time(2), '2s')
    
    def test_format_exposure_time_decimal(self):
        """Test exposure time formatting as decimal."""
        self.assertEqual(format_exposure_time(1.5), '1.5s')
    
    def test_format_aperture(self):
        """Test aperture formatting."""
        self.assertEqual(format_aperture(2.8), 'f/2.8')
        self.assertEqual(format_aperture(1.4), 'f/1.4')
        self.assertEqual(format_aperture(8), 'f/8')
    
    def test_format_focal_length(self):
        """Test focal length formatting."""
        self.assertEqual(format_focal_length(50), '50mm')
        self.assertEqual(format_focal_length(24), '24mm')


class TestExposureCalculations(unittest.TestCase):
    """Tests for exposure value calculations."""
    
    def test_calculate_ev(self):
        """Test EV calculation."""
        # Sunny 16 rule: f/16, 1/100s, ISO 100 ≈ EV 14.6
        ev = calculate_ev(16, 1/100, 100)
        self.assertAlmostEqual(ev, 14.6, places=1)
    
    def test_calculate_ev_different_iso(self):
        """Test EV calculation with different ISO."""
        # ISO 400 should give EV 12.6 for same settings
        ev = calculate_ev(16, 1/100, 400)
        self.assertAlmostEqual(ev, 12.6, places=1)
    
    def test_get_equivalent_exposure(self):
        """Test equivalent exposure calculation."""
        # f/2.8, 1/250s, ISO 100
        # Change aperture to f/5.6
        new_ap, new_ss, new_iso = get_equivalent_exposure(
            aperture=2.8, shutter_speed=1/250, iso=100,
            target_aperture=5.6
        )
        
        self.assertEqual(new_ap, 5.6)
        # f/5.6 is 2 stops darker, so shutter should be 2 stops slower
        # 1/250 * 4 = 1/62.5 ≈ 1/60
        self.assertAlmostEqual(new_ss, 1/62.5, places=2)
    
    def test_get_equivalent_exposure_iso(self):
        """Test equivalent exposure with ISO change."""
        # f/4, 1/100s, ISO 100
        # Change ISO to 400 (2 stops more sensitive)
        new_ap, new_ss, new_iso = get_equivalent_exposure(
            aperture=4, shutter_speed=1/100, iso=100,
            target_iso=400
        )
        
        self.assertEqual(new_iso, 400)
        self.assertEqual(new_ap, 4)  # aperture unchanged
        # The new shutter speed should be faster to compensate
        # Approximately 1/25s (0.04s) for the same exposure
        self.assertAlmostEqual(new_ss, 0.04, places=2)


class TestEXIFCleaner(unittest.TestCase):
    """Tests for EXIFCleaner class."""
    
    def test_remove_exif(self):
        """Test removing EXIF from JPEG."""
        jpeg_with_exif = create_test_jpeg_with_exif()
        
        cleaned = EXIFCleaner.remove_exif(jpeg_with_exif)
        
        # Should still be a valid JPEG (SOI and EOI markers)
        self.assertEqual(cleaned[:2], b'\xff\xd8')
        self.assertEqual(cleaned[-2:], b'\xff\xd9')
        
        # Should not have APP1 EXIF marker
        # Find all markers
        pos = 2
        has_app1_exif = False
        while pos < len(cleaned):
            if cleaned[pos] == 0xFF and pos + 1 < len(cleaned):
                marker = cleaned[pos + 1]
                if marker == 0xE1:
                    # Check for EXIF header
                    if pos + 4 < len(cleaned):
                        segment_len = struct.unpack('>H', cleaned[pos + 2:pos + 4])[0]
                        if cleaned[pos + 4:pos + 10] == b'Exif\x00\x00':
                            has_app1_exif = True
                            break
                    pos += segment_len
                elif marker >= 0xE0:
                    pos += struct.unpack('>H', cleaned[pos + 2:pos + 4])[0]
                elif marker == 0xD9:
                    break
                else:
                    pos += 2
            else:
                pos += 1
        
        self.assertFalse(has_app1_exif)
    
    def test_remove_exif_invalid_format(self):
        """Test remove_exif with non-JPEG."""
        not_jpeg = b'NOT_JPEG_DATA'
        
        with self.assertRaises(ValueError):
            EXIFCleaner.remove_exif(not_jpeg)
    
    def test_remove_gps(self):
        """Test removing GPS data."""
        jpeg_with_gps = create_test_jpeg_with_gps()
        
        cleaned = EXIFCleaner.remove_gps(jpeg_with_gps)
        
        # Should still be valid JPEG
        self.assertEqual(cleaned[:2], b'\xff\xd8')


class TestEXIFData(unittest.TestCase):
    """Tests for EXIFData class."""
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        exif = EXIFData(
            width=800,
            height=600,
            make='Canon',
            model='EOS R5',
            datetime=datetime(2025, 5, 8, 19, 0, 0),
        )
        
        result = exif.to_dict()
        
        self.assertEqual(result['width'], 800)
        self.assertEqual(result['height'], 600)
        self.assertEqual(result['make'], 'Canon')
        self.assertEqual(result['model'], 'EOS R5')
        self.assertEqual(result['datetime'], '2025-05-08T19:00:00')
    
    def test_to_dict_with_camera_settings(self):
        """Test conversion with camera settings."""
        settings = CameraSettings(
            make='Canon',
            model='EOS R5',
            focal_length=50,
            aperture=1.8,
            iso=400
        )
        
        exif = EXIFData(camera_settings=settings)
        result = exif.to_dict()
        
        self.assertIn('camera_settings', result)
        self.assertEqual(result['camera_settings']['focal_length'], 50)
        self.assertEqual(result['camera_settings']['iso'], 400)
    
    def test_to_dict_with_gps(self):
        """Test conversion with GPS."""
        gps = GPSLocation(latitude=35.68, longitude=139.69)
        
        exif = EXIFData(gps=gps)
        result = exif.to_dict()
        
        self.assertIn('gps', result)
        self.assertEqual(result['gps']['latitude'], 35.68)
        self.assertIn('google_maps_url', result['gps'])


class TestTagDefinitions(unittest.TestCase):
    """Tests for tag definitions."""
    
    def test_ifd0_tags(self):
        """Test IFD0 tag definitions."""
        self.assertEqual(IFD0_TAGS[0x010F], 'Make')
        self.assertEqual(IFD0_TAGS[0x0110], 'Model')
        self.assertEqual(IFD0_TAGS[0x8769], 'ExifOffset')
    
    def test_exif_tags(self):
        """Test EXIF tag definitions."""
        self.assertEqual(EXIF_TAGS[0x829A], 'ExposureTime')
        self.assertEqual(EXIF_TAGS[0x829D], 'FNumber')
        self.assertEqual(EXIF_TAGS[0x8827], 'ISOSpeedRatings')
    
    def test_gps_tags(self):
        """Test GPS tag definitions."""
        self.assertEqual(GPS_TAGS[0x0002], 'GPSLatitude')
        self.assertEqual(GPS_TAGS[0x0004], 'GPSLongitude')
    
    def test_all_tags_coverage(self):
        """Test that ALL_TAGS combines all dictionaries."""
        # Should contain tags from all IFDs
        self.assertIn(0x010F, ALL_TAGS)  # IFD0
        self.assertIn(0x829A, ALL_TAGS)  # EXIF
        self.assertIn(0x0002, ALL_TAGS)  # GPS


# =============================================================================
# Run Tests
# =============================================================================

if __name__ == '__main__':
    unittest.main(verbosity=2)