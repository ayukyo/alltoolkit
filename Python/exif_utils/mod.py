#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - EXIF Metadata Utilities Module

Comprehensive EXIF (Exchangeable Image File Format) metadata extraction and
manipulation utilities with zero external dependencies.

Supports:
- JPEG, TIFF, and PNG EXIF data extraction
- GPS coordinate extraction and conversion
- Camera settings and metadata parsing
- DateTime parsing and conversion
- Thumbnail extraction
- EXIF tag validation and cleaning

Author: AllToolkit
License: MIT
"""

import struct
import math
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union, BinaryIO
from dataclasses import dataclass, field
from enum import IntEnum


# =============================================================================
# Type Aliases
# =============================================================================

Number = Union[int, float]
Rational = Tuple[int, int]  # numerator, denominator


# =============================================================================
# EXIF Tag Definitions
# =============================================================================

class TagType(IntEnum):
    """EXIF tag data types."""
    BYTE = 1
    ASCII = 2
    SHORT = 3
    LONG = 4
    RATIONAL = 5
    SBYTE = 6
    UNDEFINED = 7
    SSHORT = 8
    SLONG = 9
    SRATIONAL = 10
    FLOAT = 11
    DOUBLE = 12


# IFD0 (Main Image Tags)
IFD0_TAGS = {
    0x0100: 'ImageWidth',
    0x0101: 'ImageLength',
    0x0102: 'BitsPerSample',
    0x0103: 'Compression',
    0x0106: 'PhotometricInterpretation',
    0x010E: 'ImageDescription',
    0x010F: 'Make',
    0x0110: 'Model',
    0x0111: 'StripOffsets',
    0x0112: 'Orientation',
    0x0115: 'SamplesPerPixel',
    0x0116: 'RowsPerStrip',
    0x0117: 'StripByteCounts',
    0x011A: 'XResolution',
    0x011B: 'YResolution',
    0x011C: 'PlanarConfiguration',
    0x0128: 'ResolutionUnit',
    0x012D: 'TransferFunction',
    0x0131: 'Software',
    0x0132: 'DateTime',
    0x013B: 'Artist',
    0x013E: 'WhitePoint',
    0x013F: 'PrimaryChromaticities',
    0x0201: 'JPEGInterchangeFormat',
    0x0202: 'JPEGInterchangeFormatLength',
    0x0211: 'YCbCrCoefficients',
    0x0212: 'YCbCrSubSampling',
    0x0213: 'YCbCrPositioning',
    0x0214: 'ReferenceBlackWhite',
    0x8298: 'Copyright',
    0x8769: 'ExifOffset',
    0x8825: 'GPSInfo',
}

# EXIF IFD Tags
EXIF_TAGS = {
    0x829A: 'ExposureTime',
    0x829D: 'FNumber',
    0x8822: 'ExposureProgram',
    0x8824: 'SpectralSensitivity',
    0x8827: 'ISOSpeedRatings',
    0x8828: 'OECF',
    0x8830: 'SensitivityType',
    0x8831: 'StandardOutputSensitivity',
    0x8832: 'RecommendedExposureIndex',
    0x8833: 'ISOSpeed',
    0x8834: 'ISOSpeedLatitudeyyy',
    0x8835: 'ISOSpeedLatitudezzz',
    0x9000: 'ExifVersion',
    0x9003: 'DateTimeOriginal',
    0x9004: 'DateTimeDigitized',
    0x9101: 'ComponentsConfiguration',
    0x9102: 'CompressedBitsPerPixel',
    0x9201: 'ShutterSpeedValue',
    0x9202: 'ApertureValue',
    0x9203: 'BrightnessValue',
    0x9204: 'ExposureBiasValue',
    0x9205: 'MaxApertureValue',
    0x9206: 'SubjectDistance',
    0x9207: 'MeteringMode',
    0x9208: 'LightSource',
    0x9209: 'Flash',
    0x920A: 'FocalLength',
    0x9214: 'SubjectArea',
    0x927C: 'MakerNote',
    0x9286: 'UserComment',
    0x9290: 'SubSecTime',
    0x9291: 'SubSecTimeOriginal',
    0x9292: 'SubSecTimeDigitized',
    0xA000: 'FlashpixVersion',
    0xA001: 'ColorSpace',
    0xA002: 'PixelXDimension',
    0xA003: 'PixelYDimension',
    0xA004: 'RelatedSoundFile',
    0xA005: 'InteroperabilityOffset',
    0xA20B: 'FlashEnergy',
    0xA20C: 'SpatialFrequencyResponse',
    0xA20E: 'FocalPlaneXResolution',
    0xA20F: 'FocalPlaneYResolution',
    0xA210: 'FocalPlaneResolutionUnit',
    0xA214: 'SubjectLocation',
    0xA215: 'ExposureIndex',
    0xA217: 'SensingMethod',
    0xA300: 'FileSource',
    0xA301: 'SceneType',
    0xA302: 'CFAPattern',
    0xA303: 'CustomRendered',
    0xA304: 'ExposureMode',
    0xA305: 'WhiteBalance',
    0xA306: 'DigitalZoomRatio',
    0xA307: 'FocalLengthIn35mmFilm',
    0xA308: 'SceneCaptureType',
    0xA309: 'GainControl',
    0xA30A: 'Contrast',
    0xA30B: 'Saturation',
    0xA30C: 'Sharpness',
    0xA30D: 'DeviceSettingDescription',
    0xA30E: 'SubjectDistanceRange',
    0xA401: 'ImageUniqueID',
    0xA402: 'CameraOwnerName',
    0xA403: 'BodySerialNumber',
    0xA404: 'LensSpecification',
    0xA405: 'LensMake',
    0xA406: 'LensModel',
    0xA407: 'LensSerialNumber',
    0xA420: 'ImageUniqueID',
    0xA430: 'CameraOwnerName',
    0xA431: 'BodySerialNumber',
    0xA432: 'LensSpecification',
    0xA433: 'LensMake',
    0xA434: 'LensModel',
    0xA435: 'LensSerialNumber',
}

# GPS IFD Tags
GPS_TAGS = {
    0x0000: 'GPSVersionID',
    0x0001: 'GPSLatitudeRef',
    0x0002: 'GPSLatitude',
    0x0003: 'GPSLongitudeRef',
    0x0004: 'GPSLongitude',
    0x0005: 'GPSAltitudeRef',
    0x0006: 'GPSAltitude',
    0x0007: 'GPSTimeStamp',
    0x0008: 'GPSSatellites',
    0x0009: 'GPSStatus',
    0x000A: 'GPSMeasureMode',
    0x000B: 'GPSDOP',
    0x000C: 'GPSSpeedRef',
    0x000D: 'GPSSpeed',
    0x000E: 'GPSTrackRef',
    0x000F: 'GPSTrack',
    0x0010: 'GPSImgDirectionRef',
    0x0011: 'GPSImgDirection',
    0x0012: 'GPSMapDatum',
    0x0013: 'GPSDestLatitudeRef',
    0x0014: 'GPSDestLatitude',
    0x0015: 'GPSDestLongitudeRef',
    0x0016: 'GPSDestLongitude',
    0x0017: 'GPSDestBearingRef',
    0x0018: 'GPSDestBearing',
    0x0019: 'GPSDestDistanceRef',
    0x001A: 'GPSDestDistance',
    0x001B: 'GPSProcessingMethod',
    0x001C: 'GPSAreaInformation',
    0x001D: 'GPSDateStamp',
    0x001E: 'GPSDifferential',
    0x001F: 'GPSHPositioningError',
}

# Combined tag dictionary for reverse lookup
ALL_TAGS = {**IFD0_TAGS, **EXIF_TAGS, **GPS_TAGS}
TAG_CODES = {v: k for k, v in ALL_TAGS.items()}


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class GPSLocation:
    """GPS location data with conversion utilities."""
    latitude: float
    longitude: float
    altitude: Optional[float] = None
    
    def to_dms(self) -> Tuple[str, str]:
        """Convert coordinates to degrees/minutes/seconds format."""
        def decimal_to_dms(decimal: float, is_latitude: bool) -> str:
            decimal = abs(decimal)
            
            degrees = int(decimal)
            minutes_decimal = (decimal - degrees) * 60
            minutes = int(minutes_decimal)
            seconds = (minutes_decimal - minutes) * 60
            
            # Determine direction based on original sign
            if is_latitude:
                direction = 'N' if self.latitude >= 0 else 'S'
            else:
                direction = 'E' if self.longitude >= 0 else 'W'
            
            return f"{degrees}°{minutes}'{seconds:.2f}\"{direction}"
        
        lat_str = decimal_to_dms(self.latitude, True)
        lon_str = decimal_to_dms(self.longitude, False)
        return lat_str, lon_str
    
    def to_google_maps_url(self) -> str:
        """Generate Google Maps URL for this location."""
        return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
    
    def to_openstreetmap_url(self) -> str:
        """Generate OpenStreetMap URL for this location."""
        return f"https://www.openstreetmap.org/?mlat={self.latitude}&mlon={self.longitude}#map=15/{self.latitude}/{self.longitude}"


@dataclass
class CameraSettings:
    """Camera settings extracted from EXIF data."""
    make: Optional[str] = None
    model: Optional[str] = None
    lens_model: Optional[str] = None
    focal_length: Optional[float] = None
    focal_length_35mm: Optional[float] = None
    aperture: Optional[float] = None
    shutter_speed: Optional[str] = None
    iso: Optional[int] = None
    exposure_program: Optional[str] = None
    metering_mode: Optional[str] = None
    flash: Optional[str] = None
    white_balance: Optional[str] = None
    
    def __str__(self) -> str:
        parts = []
        if self.make and self.model:
            parts.append(f"{self.make} {self.model}")
        if self.lens_model:
            parts.append(f"Lens: {self.lens_model}")
        if self.focal_length:
            parts.append(f"{self.focal_length}mm")
        if self.aperture:
            parts.append(f"f/{self.aperture}")
        if self.shutter_speed:
            parts.append(self.shutter_speed)
        if self.iso:
            parts.append(f"ISO {self.iso}")
        return " | ".join(parts)


@dataclass
class EXIFData:
    """Complete EXIF data container."""
    # Basic image info
    width: Optional[int] = None
    height: Optional[int] = None
    orientation: Optional[int] = None
    
    # Camera info
    make: Optional[str] = None
    model: Optional[str] = None
    software: Optional[str] = None
    artist: Optional[str] = None
    copyright: Optional[str] = None
    
    # DateTime info
    datetime: Optional[datetime] = None
    datetime_original: Optional[datetime] = None
    datetime_digitized: Optional[datetime] = None
    
    # Camera settings
    camera_settings: Optional[CameraSettings] = None
    
    # GPS info
    gps: Optional[GPSLocation] = None
    
    # Raw tags
    raw_tags: Dict[int, Any] = field(default_factory=dict)
    
    # Thumbnail
    thumbnail: Optional[bytes] = None
    thumbnail_offset: Optional[int] = None
    thumbnail_length: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            'width': self.width,
            'height': self.height,
            'orientation': self.orientation,
            'make': self.make,
            'model': self.model,
            'software': self.software,
            'artist': self.artist,
            'copyright': self.copyright,
            'datetime': self.datetime.isoformat() if self.datetime else None,
            'datetime_original': self.datetime_original.isoformat() if self.datetime_original else None,
            'datetime_digitized': self.datetime_digitized.isoformat() if self.datetime_digitized else None,
            'camera_settings': None,
            'gps': None,
            'has_thumbnail': self.thumbnail is not None,
        }
        
        if self.camera_settings:
            result['camera_settings'] = {
                'make': self.camera_settings.make,
                'model': self.camera_settings.model,
                'lens_model': self.camera_settings.lens_model,
                'focal_length': self.camera_settings.focal_length,
                'focal_length_35mm': self.camera_settings.focal_length_35mm,
                'aperture': self.camera_settings.aperture,
                'shutter_speed': self.camera_settings.shutter_speed,
                'iso': self.camera_settings.iso,
                'exposure_program': self.camera_settings.exposure_program,
                'metering_mode': self.camera_settings.metering_mode,
                'flash': self.camera_settings.flash,
                'white_balance': self.camera_settings.white_balance,
            }
        
        if self.gps:
            result['gps'] = {
                'latitude': self.gps.latitude,
                'longitude': self.gps.longitude,
                'altitude': self.gps.altitude,
                'google_maps_url': self.gps.to_google_maps_url(),
            }
        
        return result


# =============================================================================
# EXIF Parser
# =============================================================================

class EXIFParser:
    """
    EXIF metadata parser with zero external dependencies.
    
    Parses EXIF data from JPEG, TIFF, and other image formats.
    """
    
    def __init__(self, data: bytes):
        """
        Initialize parser with image data.
        
        Args:
            data: Raw image bytes
        """
        self.data = data
        self.byte_order = '<'  # Little-endian by default
        self.exif_data = EXIFData()
    
    def parse(self) -> EXIFData:
        """
        Parse EXIF data from the image.
        
        Returns:
            EXIFData object containing extracted metadata
        """
        # Check for JPEG format
        if self.data[:2] == b'\xff\xd8':
            self._parse_jpeg()
        # Check for TIFF format
        elif self.data[:2] in (b'II', b'MM'):
            self._parse_tiff()
        else:
            raise ValueError("Unsupported image format. Only JPEG and TIFF are supported.")
        
        return self.exif_data
    
    def _parse_jpeg(self) -> None:
        """Parse EXIF data from JPEG file."""
        pos = 2  # Skip SOI marker
        
        while pos < len(self.data):
            # Check for marker
            if self.data[pos] != 0xFF:
                break
            
            marker = self.data[pos + 1]
            pos += 2
            
            # APP1 marker (EXIF)
            if marker == 0xE1:
                segment_length = struct.unpack('>H', self.data[pos:pos + 2])[0]
                segment_data = self.data[pos + 2:pos + segment_length]
                
                # Check for EXIF header
                if segment_data[:6] == b'Exif\x00\x00':
                    tiff_data = segment_data[6:]
                    self._parse_tiff_data(tiff_data)
                    return
                
                pos += segment_length
            
            # Skip other markers
            elif marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                           0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
                           0xC4, 0xCC, 0xDA, 0xDB, 0xDD, 0xDE):
                segment_length = struct.unpack('>H', self.data[pos:pos + 2])[0]
                pos += segment_length
            
            # Handle standalone markers
            elif marker in (0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9):
                pass
            
            # EOI marker
            elif marker == 0xD9:
                break
            
            else:
                # Skip unknown markers with length
                if marker >= 0xE0:
                    segment_length = struct.unpack('>H', self.data[pos:pos + 2])[0]
                    pos += segment_length
    
    def _parse_tiff(self) -> None:
        """Parse TIFF image directly."""
        self._parse_tiff_data(self.data)
    
    def _parse_tiff_data(self, data: bytes) -> None:
        """Parse TIFF-format EXIF data."""
        # Determine byte order
        if data[:2] == b'II':
            self.byte_order = '<'  # Little-endian
        elif data[:2] == b'MM':
            self.byte_order = '>'  # Big-endian
        else:
            raise ValueError("Invalid TIFF header")
        
        # Verify magic number
        magic = struct.unpack(f'{self.byte_order}H', data[2:4])[0]
        if magic != 42:
            raise ValueError(f"Invalid TIFF magic number: {magic}")
        
        # Get IFD0 offset
        ifd0_offset = struct.unpack(f'{self.byte_order}I', data[4:8])[0]
        
        # Parse IFD0
        exif_offset = None
        gps_offset = None
        
        self._parse_ifd(data, ifd0_offset, self.exif_data, 'IFD0')
        exif_offset = self.exif_data.raw_tags.get(0x8769)
        gps_offset = self.exif_data.raw_tags.get(0x8825)
        
        # Parse EXIF IFD
        if exif_offset:
            self._parse_ifd(data, exif_offset, self.exif_data, 'EXIF')
        
        # Parse GPS IFD
        if gps_offset:
            self._parse_ifd(data, gps_offset, self.exif_data, 'GPS')
        
        # Build camera settings
        self._build_camera_settings()
    
    def _parse_ifd(self, data: bytes, offset: int, exif_data: EXIFData, ifd_type: str) -> None:
        """Parse an Image File Directory (IFD)."""
        num_entries = struct.unpack(f'{self.byte_order}H', data[offset:offset + 2])[0]
        offset += 2
        
        for _ in range(num_entries):
            tag_code = struct.unpack(f'{self.byte_order}H', data[offset:offset + 2])[0]
            tag_type = struct.unpack(f'{self.byte_order}H', data[offset + 2:offset + 4])[0]
            count = struct.unpack(f'{self.byte_order}I', data[offset + 4:offset + 8])[0]
            
            value_offset = offset + 8
            
            # Calculate value size
            type_size = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 6: 1, 7: 1, 8: 2, 9: 4, 10: 8, 11: 4, 12: 8}
            value_size = type_size.get(tag_type, 1) * count
            
            # Get value data
            if value_size <= 4:
                value_data = data[offset + 8:offset + 12]
            else:
                actual_offset = struct.unpack(f'{self.byte_order}I', data[offset + 8:offset + 12])[0]
                value_data = data[actual_offset:actual_offset + value_size]
            
            # Parse value
            value = self._parse_tag_value(data=value_data, tag_type=tag_type, count=count)
            
            # Store in raw tags
            exif_data.raw_tags[tag_code] = value
            
            # Store in structured fields
            self._store_tag_value(tag_code, value, exif_data, ifd_type)
            
            offset += 12
    
    def _parse_tag_value(self, data: bytes, tag_type: int, count: int) -> Any:
        """Parse a tag value based on its type."""
        if tag_type == TagType.BYTE:
            return list(data[:count])
        
        elif tag_type == TagType.ASCII:
            # Null-terminated string
            return data[:count].rstrip(b'\x00').decode('ascii', errors='replace')
        
        elif tag_type == TagType.SHORT:
            fmt = f'{self.byte_order}{count}H'
            values = struct.unpack(fmt, data[:count * 2])
            return values[0] if count == 1 else list(values)
        
        elif tag_type == TagType.LONG:
            fmt = f'{self.byte_order}{count}I'
            values = struct.unpack(fmt, data[:count * 4])
            return values[0] if count == 1 else list(values)
        
        elif tag_type == TagType.RATIONAL:
            values = []
            for i in range(count):
                num = struct.unpack(f'{self.byte_order}I', data[i * 8:i * 8 + 4])[0]
                den = struct.unpack(f'{self.byte_order}I', data[i * 8 + 4:i * 8 + 8])[0]
                values.append((num, den))
            return values[0] if count == 1 else values
        
        elif tag_type == TagType.SBYTE:
            return list(struct.unpack(f'{count}b', data[:count]))
        
        elif tag_type == TagType.UNDEFINED:
            return data[:count]
        
        elif tag_type == TagType.SSHORT:
            fmt = f'{self.byte_order}{count}h'
            values = struct.unpack(fmt, data[:count * 2])
            return values[0] if count == 1 else list(values)
        
        elif tag_type == TagType.SLONG:
            fmt = f'{self.byte_order}{count}i'
            values = struct.unpack(fmt, data[:count * 4])
            return values[0] if count == 1 else list(values)
        
        elif tag_type == TagType.SRATIONAL:
            values = []
            for i in range(count):
                num = struct.unpack(f'{self.byte_order}i', data[i * 8:i * 8 + 4])[0]
                den = struct.unpack(f'{self.byte_order}i', data[i * 8 + 4:i * 8 + 8])[0]
                values.append((num, den))
            return values[0] if count == 1 else values
        
        elif tag_type == TagType.FLOAT:
            fmt = f'{count}f'
            values = struct.unpack(fmt, data[:count * 4])
            return values[0] if count == 1 else list(values)
        
        elif tag_type == TagType.DOUBLE:
            fmt = f'{count}d'
            values = struct.unpack(fmt, data[:count * 8])
            return values[0] if count == 1 else list(values)
        
        return data[:count]
    
    def _store_tag_value(self, tag_code: int, value: Any, exif_data: EXIFData, ifd_type: str) -> None:
        """Store parsed tag value in appropriate EXIFData field."""
        # IFD0 tags
        if tag_code == 0x0100:  # ImageWidth
            exif_data.width = int(value) if isinstance(value, (int, float)) else value
        elif tag_code == 0x0101:  # ImageLength
            exif_data.height = int(value) if isinstance(value, (int, float)) else value
        elif tag_code == 0x0112:  # Orientation
            exif_data.orientation = int(value) if isinstance(value, (int, float)) else value
        elif tag_code == 0x010F:  # Make
            exif_data.make = str(value).strip()
        elif tag_code == 0x0110:  # Model
            exif_data.model = str(value).strip()
        elif tag_code == 0x0131:  # Software
            exif_data.software = str(value).strip()
        elif tag_code == 0x013B:  # Artist
            exif_data.artist = str(value).strip()
        elif tag_code == 0x8298:  # Copyright
            exif_data.copyright = str(value).strip()
        elif tag_code == 0x0132:  # DateTime
            exif_data.datetime = self._parse_datetime(value)
        
        # EXIF tags
        elif ifd_type == 'EXIF':
            if tag_code == 0x9003:  # DateTimeOriginal
                exif_data.datetime_original = self._parse_datetime(value)
            elif tag_code == 0x9004:  # DateTimeDigitized
                exif_data.datetime_digitized = self._parse_datetime(value)
        
        # GPS tags
        elif ifd_type == 'GPS':
            self._parse_gps_tag(tag_code, value, exif_data)
    
    def _parse_datetime(self, value: Any) -> Optional[datetime]:
        """Parse EXIF datetime string to datetime object."""
        if not isinstance(value, str):
            return None
        
        try:
            # Standard EXIF datetime format: "YYYY:MM:DD HH:MM:SS"
            return datetime.strptime(value.strip(), '%Y:%m:%d %H:%M:%S')
        except (ValueError, AttributeError):
            return None
    
    def _parse_gps_tag(self, tag_code: int, value: Any, exif_data: EXIFData) -> None:
        """Parse GPS-specific tags."""
        if tag_code == 0x0002:  # GPSLatitude
            lat = self._parse_gps_coordinate(value)
            if lat is not None and exif_data.gps is None:
                exif_data.gps = GPSLocation(latitude=lat, longitude=0)
            elif lat is not None and exif_data.gps:
                exif_data.gps.latitude = lat
            else:
                exif_data.gps = GPSLocation(latitude=lat or 0, longitude=0)
        
        elif tag_code == 0x0001:  # GPSLatitudeRef
            if isinstance(value, str) and value.upper() == 'S' and exif_data.gps:
                exif_data.gps.latitude = -abs(exif_data.gps.latitude)
        
        elif tag_code == 0x0004:  # GPSLongitude
            lon = self._parse_gps_coordinate(value)
            if lon is not None:
                if exif_data.gps is None:
                    exif_data.gps = GPSLocation(latitude=0, longitude=lon)
                else:
                    exif_data.gps.longitude = lon
        
        elif tag_code == 0x0003:  # GPSLongitudeRef
            if isinstance(value, str) and value.upper() == 'W' and exif_data.gps:
                exif_data.gps.longitude = -abs(exif_data.gps.longitude)
        
        elif tag_code == 0x0006:  # GPSAltitude
            if isinstance(value, tuple) and len(value) == 2:
                alt = value[0] / value[1] if value[1] != 0 else 0
                if exif_data.gps:
                    exif_data.gps.altitude = alt
        
        elif tag_code == 0x0005:  # GPSAltitudeRef
            if value == 1 and exif_data.gps and exif_data.gps.altitude:
                exif_data.gps.altitude = -abs(exif_data.gps.altitude)
    
    def _parse_gps_coordinate(self, value: Any) -> Optional[float]:
        """Parse GPS coordinate from degrees/minutes/seconds format."""
        if not isinstance(value, list) or len(value) < 3:
            return None
        
        try:
            degrees = value[0][0] / value[0][1] if isinstance(value[0], tuple) else float(value[0])
            minutes = value[1][0] / value[1][1] if isinstance(value[1], tuple) else float(value[1])
            seconds = value[2][0] / value[2][1] if isinstance(value[2], tuple) else float(value[2])
            
            return degrees + minutes / 60 + seconds / 3600
        except (IndexError, TypeError, ZeroDivisionError):
            return None
    
    def _build_camera_settings(self) -> None:
        """Build CameraSettings object from raw tags."""
        tags = self.exif_data.raw_tags
        
        settings = CameraSettings()
        
        # Make and Model
        settings.make = self.exif_data.make
        settings.model = self.exif_data.model
        
        # Lens
        if 0xA434 in tags:  # LensModel
            settings.lens_model = str(tags[0xA434]).strip()
        
        # Focal length
        if 0x920A in tags:  # FocalLength
            value = tags[0x920A]
            if isinstance(value, tuple):
                settings.focal_length = value[0] / value[1] if value[1] != 0 else 0
            else:
                settings.focal_length = float(value)
        
        # Focal length in 35mm
        if 0xA307 in tags:  # FocalLengthIn35mmFilm
            settings.focal_length_35mm = int(tags[0xA307])
        
        # Aperture
        if 0x829D in tags:  # FNumber
            value = tags[0x829D]
            if isinstance(value, tuple):
                settings.aperture = round(value[0] / value[1], 1) if value[1] != 0 else 0
            else:
                settings.aperture = float(value)
        
        # Shutter speed
        if 0x829A in tags:  # ExposureTime
            value = tags[0x829A]
            if isinstance(value, tuple):
                exposure_time = value[0] / value[1] if value[1] != 0 else 0
            else:
                exposure_time = float(value)
            settings.shutter_speed = self._format_shutter_speed(exposure_time)
        
        # ISO
        if 0x8827 in tags:  # ISOSpeedRatings
            settings.iso = int(tags[0x8827])
        
        # Exposure program
        if 0x8822 in tags:  # ExposureProgram
            settings.exposure_program = self._get_exposure_program_name(tags[0x8822])
        
        # Metering mode
        if 0x9207 in tags:  # MeteringMode
            settings.metering_mode = self._get_metering_mode_name(tags[0x9207])
        
        # Flash
        if 0x9209 in tags:  # Flash
            settings.flash = self._get_flash_status(tags[0x9209])
        
        # White balance
        if 0xA403 in tags:  # WhiteBalance
            settings.white_balance = 'Auto' if tags[0xA403] == 0 else 'Manual'
        
        self.exif_data.camera_settings = settings
    
    def _format_shutter_speed(self, exposure_time: float) -> str:
        """Format exposure time as shutter speed string."""
        if exposure_time >= 1:
            return f"{int(exposure_time)}s"
        else:
            # Find a nice fraction representation
            denominator = round(1 / exposure_time)
            return f"1/{denominator}s"
    
    def _get_exposure_program_name(self, code: int) -> str:
        """Get exposure program name from code."""
        programs = {
            0: 'Not defined',
            1: 'Manual',
            2: 'Normal program',
            3: 'Aperture priority',
            4: 'Shutter priority',
            5: 'Creative program',
            6: 'Action program',
            7: 'Portrait mode',
            8: 'Landscape mode',
        }
        return programs.get(code, f'Unknown ({code})')
    
    def _get_metering_mode_name(self, code: int) -> str:
        """Get metering mode name from code."""
        modes = {
            0: 'Unknown',
            1: 'Average',
            2: 'CenterWeightedAverage',
            3: 'Spot',
            4: 'MultiSpot',
            5: 'Pattern',
            6: 'Partial',
            255: 'Other',
        }
        return modes.get(code, f'Unknown ({code})')
    
    def _get_flash_status(self, code: int) -> str:
        """Get flash status from code."""
        if code == 0:
            return 'No flash'
        elif code & 1:
            return 'Flash fired'
        else:
            return f'Flash code: {code}'


# =============================================================================
# High-Level Functions
# =============================================================================

def extract_exif(file_path: str) -> EXIFData:
    """
    Extract EXIF data from an image file.
    
    Args:
        file_path: Path to the image file
    
    Returns:
        EXIFData object containing extracted metadata
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format is not supported
    """
    with open(file_path, 'rb') as f:
        data = f.read()
    
    parser = EXIFParser(data)
    return parser.parse()


def extract_exif_from_bytes(data: bytes) -> EXIFData:
    """
    Extract EXIF data from image bytes.
    
    Args:
        data: Raw image bytes
    
    Returns:
        EXIFData object containing extracted metadata
    """
    parser = EXIFParser(data)
    return parser.parse()


def get_camera_info(file_path: str) -> Optional[CameraSettings]:
    """
    Get camera settings from an image file.
    
    Args:
        file_path: Path to the image file
    
    Returns:
        CameraSettings object or None if no EXIF data found
    """
    try:
        exif = extract_exif(file_path)
        return exif.camera_settings
    except Exception:
        return None


def get_gps_location(file_path: str) -> Optional[GPSLocation]:
    """
    Get GPS location from an image file.
    
    Args:
        file_path: Path to the image file
    
    Returns:
        GPSLocation object or None if no GPS data found
    """
    try:
        exif = extract_exif(file_path)
        return exif.gps
    except Exception:
        return None


def get_datetime_original(file_path: str) -> Optional[datetime]:
    """
    Get the original capture datetime from an image file.
    
    Args:
        file_path: Path to the image file
    
    Returns:
        datetime object or None if not found
    """
    try:
        exif = extract_exif(file_path)
        return exif.datetime_original or exif.datetime
    except Exception:
        return None


def has_exif(file_path: str) -> bool:
    """
    Check if an image file contains EXIF data.
    
    Args:
        file_path: Path to the image file
    
    Returns:
        True if EXIF data is present
    """
    try:
        exif = extract_exif(file_path)
        return len(exif.raw_tags) > 0
    except Exception:
        return False


def get_tag_value(file_path: str, tag_name: str) -> Any:
    """
    Get a specific EXIF tag value by name.
    
    Args:
        file_path: Path to the image file
        tag_name: Name of the EXIF tag (e.g., 'Make', 'Model', 'ISOSpeedRatings')
    
    Returns:
        Tag value or None if not found
    """
    try:
        exif = extract_exif(file_path)
        
        # Look up tag code by name
        tag_code = TAG_CODES.get(tag_name)
        if tag_code is None:
            # Try direct lookup with hex string
            try:
                tag_code = int(tag_name, 16)
            except ValueError:
                return None
        
        return exif.raw_tags.get(tag_code)
    except Exception:
        return None


def get_all_tags(file_path: str) -> Dict[str, Any]:
    """
    Get all EXIF tags as a named dictionary.
    
    Args:
        file_path: Path to the image file
    
    Returns:
        Dictionary of tag names to values
    """
    try:
        exif = extract_exif(file_path)
        result = {}
        
        for code, value in exif.raw_tags.items():
            name = ALL_TAGS.get(code, f'Unknown_0x{code:04X}')
            result[name] = value
        
        return result
    except Exception:
        return {}


def format_exposure_time(seconds: float) -> str:
    """
    Format exposure time as a human-readable string.
    
    Args:
        seconds: Exposure time in seconds
    
    Returns:
        Formatted string (e.g., '1/250s' or '2s')
    """
    if seconds >= 1:
        if seconds == int(seconds):
            return f"{int(seconds)}s"
        return f"{seconds:.1f}s"
    else:
        denominator = round(1 / seconds)
        return f"1/{denominator}s"


def format_aperture(f_number: float) -> str:
    """
    Format aperture as a human-readable string.
    
    Args:
        f_number: F-number value
    
    Returns:
        Formatted string (e.g., 'f/2.8')
    """
    return f"f/{f_number:.1f}".replace('.0', '')


def format_focal_length(mm: float) -> str:
    """
    Format focal length as a human-readable string.
    
    Args:
        mm: Focal length in millimeters
    
    Returns:
        Formatted string (e.g., '50mm' or '50mm (35mm eq: 75mm)')
    """
    return f"{mm:.0f}mm"


def calculate_ev(aperture: float, shutter_speed: float, iso: int) -> float:
    """
    Calculate exposure value (EV) from camera settings.
    
    Args:
        aperture: F-number
        shutter_speed: Exposure time in seconds
        iso: ISO sensitivity
    
    Returns:
        EV value (EV at ISO 100)
    """
    # EV = log2(N^2 / t) - log2(ISO/100)
    # where N = f-number, t = exposure time
    ev_100 = math.log2((aperture ** 2) / shutter_speed)
    ev_correction = math.log2(iso / 100)
    return ev_100 - ev_correction


def get_equivalent_exposure(
    aperture: float,
    shutter_speed: float,
    iso: int,
    target_aperture: Optional[float] = None,
    target_iso: Optional[int] = None
) -> Tuple[float, float, int]:
    """
    Calculate equivalent exposure with different settings.
    
    Args:
        aperture: Current aperture (f-number)
        shutter_speed: Current shutter speed (seconds)
        iso: Current ISO
        target_aperture: Desired aperture (optional)
        target_iso: Desired ISO (optional)
    
    Returns:
        Tuple of (new_aperture, new_shutter_speed, new_iso)
    """
    # Calculate current EV
    ev = math.log2((aperture ** 2) / shutter_speed) + math.log2(iso / 100)
    
    # Determine new settings
    new_aperture = target_aperture if target_aperture else aperture
    new_iso = target_iso if target_iso else iso
    
    # Calculate new shutter speed
    # EV = log2(A^2 / T) + log2(ISO/100)
    # T = A^2 / 2^(EV - log2(ISO/100))
    new_shutter = (new_aperture ** 2) / (2 ** (ev - math.log2(new_iso / 100)))
    
    return new_aperture, new_shutter, new_iso


# =============================================================================
# Utility Classes
# =============================================================================

class EXIFCleaner:
    """Remove or modify EXIF data from images."""
    
    @staticmethod
    def remove_exif(data: bytes) -> bytes:
        """
        Remove all EXIF data from JPEG image bytes.
        
        Args:
            data: Raw JPEG image bytes
        
        Returns:
            JPEG bytes without EXIF data
        """
        if data[:2] != b'\xff\xd8':
            raise ValueError("Not a JPEG file")
        
        output = bytearray(data[:2])  # SOI marker
        pos = 2
        
        while pos < len(data):
            if data[pos] != 0xFF:
                # Not a marker - might be image data, copy until next marker
                # Find next 0xFF
                next_marker = data.find(b'\xff', pos)
                if next_marker == -1:
                    # Copy remaining data and break
                    output.extend(data[pos:])
                    break
                output.extend(data[pos:next_marker])
                pos = next_marker
                continue
            
            marker = data[pos + 1]
            marker_pos = pos
            pos += 2
            
            # Skip APP1 (EXIF) marker
            if marker == 0xE1:
                if pos + 2 <= len(data):
                    segment_length = struct.unpack('>H', data[pos:pos + 2])[0]
                    pos += segment_length
                continue
            
            # EOI marker - stop
            if marker == 0xD9:
                output.extend(b'\xff\xd9')
                break
            
            # RST markers (D0-D7) - standalone, no length
            if marker in (0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7):
                output.extend(b'\xff' + bytes([marker]))
                continue
            
            # SOF and other markers with length
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                        0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
                        0xC4, 0xCC, 0xDA, 0xDB, 0xDD, 0xDE,
                        0xE0, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7,
                        0xE8, 0xE9, 0xEA, 0xEB, 0xEC, 0xED, 0xEE, 0xEF):
                if pos + 2 <= len(data):
                    segment_length = struct.unpack('>H', data[pos:pos + 2])[0]
                    output.extend(data[marker_pos:pos + segment_length])
                    pos += segment_length
                continue
            
            # Unknown marker - try to handle with length if it's APP marker
            if marker >= 0xE0 and marker <= 0xEF:
                if pos + 2 <= len(data):
                    segment_length = struct.unpack('>H', data[pos:pos + 2])[0]
                    output.extend(data[marker_pos:pos + segment_length])
                    pos += segment_length
                continue
            
            # Other standalone markers
            output.extend(b'\xff' + bytes([marker]))
        
        return bytes(output)
    
    @staticmethod
    def remove_gps(data: bytes) -> bytes:
        """
        Remove GPS data from JPEG EXIF while keeping other metadata.
        
        Note: This is a simplified implementation that removes all EXIF.
        A full implementation would require rewriting the EXIF segment.
        
        Args:
            data: Raw JPEG image bytes
        
        Returns:
            JPEG bytes without GPS data
        """
        # Simplified: remove all EXIF
        # A full implementation would parse and rebuild EXIF without GPS
        return EXIFCleaner.remove_exif(data)


class EXIFWriter:
    """Write/modify EXIF data in images."""
    
    @staticmethod
    def set_orientation(data: bytes, orientation: int) -> bytes:
        """
        Set the orientation tag in JPEG EXIF data.
        
        Note: This is a simplified implementation.
        A full implementation would require proper EXIF rewriting.
        
        Args:
            data: Raw JPEG image bytes
            orientation: Orientation value (1-8)
        
        Returns:
            JPEG bytes with modified orientation
        """
        # This is a placeholder - full implementation would require
        # parsing and rebuilding the EXIF segment
        raise NotImplementedError(
            "EXIF modification requires proper EXIF segment parsing and rebuilding. "
            "Consider using Pillow or piexif libraries for EXIF modification."
        )


# =============================================================================
# Convenience Functions
# =============================================================================

def summarize(file_path: str) -> Dict[str, Any]:
    """
    Get a summary of EXIF data from an image file.
    
    Args:
        file_path: Path to the image file
    
    Returns:
        Dictionary with summary information
    """
    try:
        exif = extract_exif(file_path)
        
        summary = {
            'file': file_path,
            'has_exif': len(exif.raw_tags) > 0,
            'dimensions': f"{exif.width}x{exif.height}" if exif.width and exif.height else None,
            'orientation': exif.orientation,
            'camera': None,
            'settings': None,
            'taken_at': None,
            'gps': None,
        }
        
        if exif.camera_settings:
            settings = exif.camera_settings
            summary['camera'] = f"{settings.make or ''} {settings.model or ''}".strip()
            summary['settings'] = str(settings) if str(settings) else None
        
        if exif.datetime_original:
            summary['taken_at'] = exif.datetime_original.isoformat()
        elif exif.datetime:
            summary['taken_at'] = exif.datetime.isoformat()
        
        if exif.gps:
            summary['gps'] = {
                'coordinates': (exif.gps.latitude, exif.gps.longitude),
                'google_maps': exif.gps.to_google_maps_url(),
            }
        
        return summary
    
    except Exception as e:
        return {'file': file_path, 'error': str(e)}


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python mod.py <image_file>")
        print("       python mod.py --summary <image_file>")
        print("       python mod.py --gps <image_file>")
        print("       python mod.py --camera <image_file>")
        sys.exit(1)
    
    file_path = sys.argv[-1]
    mode = sys.argv[1] if len(sys.argv) > 2 else '--all'
    
    try:
        exif = extract_exif(file_path)
        
        if mode == '--summary':
            print("=== EXIF Summary ===")
            print(f"File: {file_path}")
            print(f"Dimensions: {exif.width}x{exif.height}")
            print(f"Orientation: {exif.orientation}")
            
            if exif.camera_settings:
                print(f"Camera: {exif.camera_settings}")
            
            if exif.datetime_original:
                print(f"Taken: {exif.datetime_original}")
            
            if exif.gps:
                print(f"Location: {exif.gps.latitude:.6f}, {exif.gps.longitude:.6f}")
                print(f"Map: {exif.gps.to_google_maps_url()}")
        
        elif mode == '--gps':
            if exif.gps:
                lat, lon = exif.gps.latitude, exif.gps.longitude
                lat_dms, lon_dms = exif.gps.to_dms()
                print(f"Latitude: {exif.gps.latitude:.6f} ({lat_dms})")
                print(f"Longitude: {exif.gps.longitude:.6f} ({lon_dms})")
                if exif.gps.altitude:
                    print(f"Altitude: {exif.gps.altitude:.2f}m")
                print(f"\nGoogle Maps: {exif.gps.to_google_maps_url()}")
                print(f"OpenStreetMap: {exif.gps.to_openstreetmap_url()}")
            else:
                print("No GPS data found in this image.")
        
        elif mode == '--camera':
            if exif.camera_settings:
                settings = exif.camera_settings
                print("=== Camera Settings ===")
                print(f"Camera: {settings.make or 'Unknown'} {settings.model or 'Unknown'}")
                if settings.lens_model:
                    print(f"Lens: {settings.lens_model}")
                if settings.focal_length:
                    fl = f"{settings.focal_length:.0f}mm"
                    if settings.focal_length_35mm:
                        fl += f" (35mm eq: {settings.focal_length_35mm}mm)"
                    print(f"Focal Length: {fl}")
                if settings.aperture:
                    print(f"Aperture: f/{settings.aperture}")
                if settings.shutter_speed:
                    print(f"Shutter Speed: {settings.shutter_speed}")
                if settings.iso:
                    print(f"ISO: {settings.iso}")
                if settings.exposure_program:
                    print(f"Exposure Program: {settings.exposure_program}")
                if settings.metering_mode:
                    print(f"Metering Mode: {settings.metering_mode}")
                if settings.flash:
                    print(f"Flash: {settings.flash}")
                if settings.white_balance:
                    print(f"White Balance: {settings.white_balance}")
            else:
                print("No camera settings found in this image.")
        
        else:  # --all
            print("=== All EXIF Tags ===")
            for code, value in sorted(exif.raw_tags.items()):
                name = ALL_TAGS.get(code, f'Unknown_0x{code:04X}')
                if isinstance(value, bytes):
                    value = f"<{len(value)} bytes>"
                print(f"0x{code:04X} {name}: {value}")
    
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)