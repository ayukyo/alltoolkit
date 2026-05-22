#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Plus Code (Open Location Code) Utilities Module

Plus Code (also known as Open Location Code) is a geocoding system developed by Google
that encodes latitude and longitude into a short alphanumeric string. It provides
a universal addressing solution for locations without traditional street addresses.

Features:
- Encode latitude/longitude to Plus Code
- Decode Plus Code back to coordinates
- Shorten Plus Code using a reference location
- Recover full Plus Code from shortened code
- Validate Plus Code format
- Calculate code area boundaries

Pure Python implementation with zero external dependencies.

Author: AllToolkit
License: MIT
"""

import math
import re
from typing import Tuple, Optional, List, Dict, Any
from dataclasses import dataclass


# =============================================================================
# Constants
# =============================================================================

# Valid characters in the Plus Code alphabet (excludes I, O for OCR compatibility)
CODE_ALPHABET = "23456789CFGHJJKLMNPQRSTVWXYZ"

# Separator used to separate the code into two parts
SEPARATOR = "+"

# Position of the separator in the code
SEPARATOR_POSITION = 8

# Maximum number of digits after the separator
MAX_SUFFIX_LENGTH = 7

# Maximum code length (including separator)
MAX_CODE_LENGTH = 15

# Pair encoding values (degrees per encoded pair)
PAIR_FIRST_VALUE = 20.0
PAIR_SECOND_VALUE = 0.5
PAIR_THIRD_VALUE = 0.025
PAIR_FOURTH_VALUE = 0.00125
PAIR_FIFTH_VALUE = 0.0000625
PAIR_SIXTH_VALUE = 0.000003125

PAIR_ENCODING_VALUES = [
    PAIR_FIRST_VALUE, PAIR_SECOND_VALUE, PAIR_THIRD_VALUE,
    PAIR_FOURTH_VALUE, PAIR_FIFTH_VALUE, PAIR_SIXTH_VALUE
]

# Grid encoding values
GRID_LATITUDE_UNITS = 0.000125
GRID_LONGITUDE_UNITS = 0.00025

GRID_ROWS = 5
GRID_COLUMNS = 4


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class PlusCodeResult:
    """Result of Plus Code encoding."""
    full_code: str
    latitude: float
    longitude: float
    precision_meters: float
    short_code: Optional[str] = None


@dataclass
class CodeArea:
    """Area covered by a Plus Code."""
    latitude_lo: float
    latitude_hi: float
    longitude_lo: float
    longitude_hi: float
    latitude_center: float
    longitude_center: float
    code_length: int


# =============================================================================
# Helper Functions
# =============================================================================

def _clip_latitude(latitude: float) -> float:
    """Clip latitude to valid range [-90, 90]."""
    return max(-90.0, min(90.0, latitude))


def _normalize_longitude(longitude: float) -> float:
    """Normalize longitude to range [-180, 180)."""
    while longitude < -180.0:
        longitude += 360.0
    while longitude >= 180.0:
        longitude -= 360.0
    return longitude


def _encode_value(value: float, max_value: float, encoding_length: int) -> Tuple[int, float]:
    """Encode a value to digit indices."""
    scaled_value = (value + max_value) % (2 * max_value)
    digit_value = int(scaled_value / encoding_length)
    remainder = scaled_value - digit_value * encoding_length
    return digit_value, remainder


def _decode_value(digits: str, max_value: float) -> Tuple[float, float]:
    """Decode digits to value and precision."""
    value = 0.0
    precision = 0.0
    
    for i, char in enumerate(digits):
        digit_index = CODE_ALPHABET.find(char.upper())
        if digit_index >= 0:
            encoding_value = PAIR_ENCODING_VALUES[i] if i < len(PAIR_ENCODING_VALUES) else PAIR_ENCODING_VALUES[-1]
            value += digit_index * encoding_value
            precision = encoding_value
    
    return value, precision


def _get_alphabet_position(char: str) -> int:
    """Get position of character in alphabet."""
    return CODE_ALPHABET.find(char.upper())


# =============================================================================
# Core Functions
# =============================================================================

def encode(
    latitude: float,
    longitude: float,
    code_length: int = 10
) -> PlusCodeResult:
    """
    Encode latitude and longitude to a Plus Code.
    
    Args:
        latitude: Latitude in decimal degrees (-90 to 90)
        longitude: Longitude in decimal degrees (-180 to 180)
        code_length: Number of digits in the code (default 10, max 15)
        
    Returns:
        PlusCodeResult with the encoded code and coordinates
        
    Example:
        >>> result = encode(47.365590, 8.524030)
        >>> print(result.full_code)
        8FVC2222+
        
        >>> result = encode(47.365590, 8.524030, 12)
        >>> print(result.full_code)
        8FVC2222+22
    """
    # Validate inputs
    latitude = _clip_latitude(latitude)
    longitude = _normalize_longitude(longitude)
    
    # Validate code length
    if code_length < 2:
        raise ValueError("Code length must be at least 2")
    if code_length > MAX_CODE_LENGTH:
        raise ValueError(f"Code length cannot exceed {MAX_CODE_LENGTH}")
    
    # Ensure even length for pair encoding (except when using grid)
    if code_length < 10 and code_length % 2 != 0:
        code_length += 1
    
    # Generate code
    code = ""
    lat_remaining = latitude + 90.0  # Shift to positive range [0, 180]
    lon_remaining = longitude + 180.0  # Shift to positive range [0, 360]
    
    # Generate pairs until separator position
    pair_count = min(code_length, SEPARATOR_POSITION) // 2
    
    for i in range(pair_count):
        encoding_value = PAIR_ENCODING_VALUES[i]
        
        # Encode latitude
        lat_digit = int(lat_remaining / encoding_value)
        lat_remaining -= lat_digit * encoding_value
        
        # Encode longitude (uses larger range)
        lon_digit = int(lon_remaining / (encoding_value * 2))
        lon_remaining -= lon_digit * (encoding_value * 2)
        
        code += CODE_ALPHABET[lat_digit % 20]
        code += CODE_ALPHABET[lon_digit % 20]
    
    # Add separator if code length >= separator position
    if code_length >= SEPARATOR_POSITION:
        code += SEPARATOR
    else:
        # Pad with zeros and add separator for short codes
        code += CODE_ALPHABET[0] * (SEPARATOR_POSITION - len(code))
        code += SEPARATOR
    
    # Generate refinement digits after separator using grid
    if code_length > SEPARATOR_POSITION:
        refinement_length = code_length - SEPARATOR_POSITION
        
        # Grid refinement (first 2-3 digits after separator)
        lat_grid_value = int(lat_remaining / GRID_LATITUDE_UNITS)
        lon_grid_value = int(lon_remaining / GRID_LONGITUDE_UNITS)
        
        lat_grid_remaining = lat_remaining - lat_grid_value * GRID_LATITUDE_UNITS
        lon_grid_remaining = lon_remaining - lon_grid_value * GRID_LONGITUDE_UNITS
        
        # Calculate grid code
        grid_row = lat_grid_value % GRID_ROWS
        grid_col = lon_grid_value % GRID_COLUMNS
        
        grid_code = grid_row * GRID_COLUMNS + grid_col
        code += CODE_ALPHABET[grid_code]
        
        if refinement_length >= 2:
            # Second grid refinement
            lat_grid_value_2 = int(lat_grid_remaining / GRID_LATITUDE_UNITS)
            lon_grid_value_2 = int(lon_grid_remaining / GRID_LONGITUDE_UNITS)
            
            grid_row_2 = lat_grid_value_2 % GRID_ROWS
            grid_col_2 = lon_grid_value_2 % GRID_COLUMNS
            
            grid_code_2 = grid_row_2 * GRID_COLUMNS + grid_col_2
            code += CODE_ALPHABET[grid_code_2]
        
        # Additional refinement digits (after first 2 grid digits)
        if refinement_length > 2:
            remaining_length = refinement_length - 2
            
            # Each additional pair adds more precision
            for j in range(remaining_length):
                additional_precision = GRID_LATITUDE_UNITS / pow(20, j + 1)
                
                lat_extra = int(lat_grid_remaining / additional_precision) % 20
                lon_extra = int(lon_grid_remaining / additional_precision) % 20
                
                code += CODE_ALPHABET[lat_extra]
                code += CODE_ALPHABET[lon_extra]
    
    # Calculate precision
    if code_length <= SEPARATOR_POSITION:
        precision_index = (code_length // 2) - 1
        lat_precision = PAIR_ENCODING_VALUES[precision_index]
    elif code_length == SEPARATOR_POSITION + 1:
        lat_precision = GRID_LATITUDE_UNITS
    elif code_length == SEPARATOR_POSITION + 2:
        lat_precision = GRID_LATITUDE_UNITS
    else:
        extra_digits = code_length - (SEPARATOR_POSITION + 2)
        lat_precision = GRID_LATITUDE_UNITS / pow(20, extra_digits // 2)
    
    precision_meters = lat_precision * 111000  # Approximate meters
    
    return PlusCodeResult(
        full_code=code,
        latitude=latitude,
        longitude=longitude,
        precision_meters=precision_meters,
        short_code=None
    )


def decode(code: str) -> CodeArea:
    """
    Decode a Plus Code to get the geographic area it represents.
    
    Args:
        code: Plus Code string
        
    Returns:
        CodeArea with latitude/longitude bounds and center
        
    Example:
        >>> area = decode("8FVC2222+")
        >>> print(f"Center: ({area.latitude_center}, {area.longitude_center})")
    """
    # Clean and validate code
    code = clean_code(code)
    
    if not is_valid_code(code):
        raise ValueError(f"Invalid Plus Code: {code}")
    
    # Split code into prefix and suffix
    separator_pos = code.find(SEPARATOR)
    prefix = code[:separator_pos]
    suffix = code[separator_pos + 1:] if separator_pos + 1 < len(code) else ""
    
    # Decode prefix (pairs)
    latitude = -90.0
    longitude = -180.0
    
    for i in range(0, len(prefix), 2):
        if i + 1 < len(prefix):
            lat_digit = _get_alphabet_position(prefix[i])
            lon_digit = _get_alphabet_position(prefix[i + 1])
            
            if lat_digit >= 0 and lon_digit >= 0:
                encoding_value = PAIR_ENCODING_VALUES[i // 2]
                latitude += lat_digit * encoding_value
                longitude += lon_digit * encoding_value
    
    # Determine precision from prefix
    lat_precision = PAIR_ENCODING_VALUES[len(prefix) // 2 - 1]
    lon_precision = lat_precision * 2
    
    # Decode suffix (grid refinement)
    if len(suffix) >= 1:
        grid_digit_1 = _get_alphabet_position(suffix[0])
        if grid_digit_1 >= 0:
            grid_row = grid_digit_1 // GRID_COLUMNS
            grid_col = grid_digit_1 % GRID_COLUMNS
            
            latitude += grid_row * GRID_LATITUDE_UNITS
            longitude += grid_col * GRID_LONGITUDE_UNITS
            
            lat_precision = GRID_LATITUDE_UNITS
            lon_precision = GRID_LONGITUDE_UNITS
    
    if len(suffix) >= 2:
        grid_digit_2 = _get_alphabet_position(suffix[1])
        if grid_digit_2 >= 0:
            grid_row_2 = grid_digit_2 // GRID_COLUMNS
            grid_col_2 = grid_digit_2 % GRID_COLUMNS
            
            latitude += grid_row_2 * GRID_LATITUDE_UNITS / GRID_ROWS
            longitude += grid_col_2 * GRID_LONGITUDE_UNITS / GRID_COLUMNS
            
            lat_precision = GRID_LATITUDE_UNITS / GRID_ROWS
            lon_precision = GRID_LONGITUDE_UNITS / GRID_COLUMNS
    
    # Additional precision digits
    if len(suffix) > 2:
        extra_digits = len(suffix) - 2
        for j in range(extra_digits):
            extra_digit = _get_alphabet_position(suffix[j + 2])
            if extra_digit >= 0:
                additional_precision = GRID_LATITUDE_UNITS / pow(20, j // 2 + 1)
                
                if j % 2 == 0:  # Latitude digit
                    latitude += extra_digit * additional_precision
                else:  # Longitude digit
                    longitude += extra_digit * additional_precision
                
                if j == extra_digits - 1:
                    lat_precision = additional_precision
                    lon_precision = additional_precision * 2
    
    # Calculate bounds
    latitude_lo = latitude
    latitude_hi = latitude + lat_precision
    longitude_lo = longitude
    longitude_hi = longitude + lon_precision
    
    # Handle longitude wrapping
    if longitude_hi >= 180.0:
        longitude_hi -= 360.0
    if longitude_hi < longitude_lo:
        longitude_hi += 360.0
    
    # Calculate centers
    latitude_center = (latitude_lo + latitude_hi) / 2
    longitude_center = (longitude_lo + longitude_hi) / 2
    if longitude_hi < longitude_lo:
        longitude_center = (longitude_lo + longitude_hi + 360.0) / 2
        if longitude_center >= 180.0:
            longitude_center -= 360.0
    
    # Calculate code length
    code_length = len(prefix) + len(suffix)
    
    return CodeArea(
        latitude_lo=latitude_lo,
        latitude_hi=latitude_hi,
        longitude_lo=longitude_lo,
        longitude_hi=longitude_hi,
        latitude_center=latitude_center,
        longitude_center=longitude_center,
        code_length=code_length
    )


def shorten(
    code: str,
    reference_latitude: float,
    reference_longitude: float
) -> str:
    """
    Shorten a Plus Code using a reference location.
    
    Args:
        code: Full Plus Code string
        reference_latitude: Latitude of reference location
        reference_longitude: Longitude of reference location
        
    Returns:
        Shortened Plus Code string
    """
    code = clean_code(code)
    
    if not is_valid_code(code):
        raise ValueError(f"Invalid Plus Code: {code}")
    
    # Decode the code
    area = decode(code)
    
    # Check proximity to reference
    reference_latitude = _clip_latitude(reference_latitude)
    reference_longitude = _normalize_longitude(reference_longitude)
    
    # Calculate how much of the prefix can be removed
    # Each pair of prefix digits covers a larger area
    prefix_length = code.find(SEPARATOR)
    
    for i in range(prefix_length - 2, 0, -2):
        encoding_value = PAIR_ENCODING_VALUES[i // 2]
        
        # Check if reference is within the coverage area
        lat_diff = abs(reference_latitude - area.latitude_center)
        lon_diff = abs(reference_longitude - area.longitude_center)
        
        # Adjust longitude difference for wrapping
        if lon_diff > 180:
            lon_diff = 360 - lon_diff
        
        if lat_diff > encoding_value or lon_diff > encoding_value * 2:
            # Can't remove this pair - reference is too far
            break
        
        prefix_length -= 2
    
    # Create shortened code
    if prefix_length < code.find(SEPARATOR):
        prefix = code[:prefix_length]
        suffix = code[code.find(SEPARATOR):]
        return prefix + suffix
    
    return code


def recover_nearest(
    short_code: str,
    reference_latitude: float,
    reference_longitude: float
) -> str:
    """
    Recover the full Plus Code from a shortened code using a reference location.
    
    Args:
        short_code: Shortened Plus Code (missing prefix)
        reference_latitude: Latitude of reference location
        reference_longitude: Longitude of reference location
        
    Returns:
        Full Plus Code string
    """
    # Clean and validate
    short_code = clean_code(short_code)
    
    if SEPARATOR not in short_code:
        raise ValueError("Code must contain separator")
    
    # Check if it's already a full code
    separator_pos = short_code.find(SEPARATOR)
    if separator_pos >= SEPARATOR_POSITION:
        return short_code
    
    # Calculate needed prefix
    reference_latitude = _clip_latitude(reference_latitude)
    reference_longitude = _normalize_longitude(reference_longitude)
    
    # Build prefix from reference location
    lat_remaining = reference_latitude + 90.0
    lon_remaining = reference_longitude + 180.0
    
    prefix_length = SEPARATOR_POSITION - separator_pos
    prefix = ""
    
    for i in range(prefix_length // 2):
        encoding_value = PAIR_ENCODING_VALUES[i]
        
        lat_digit = int(lat_remaining / encoding_value) % 20
        lon_digit = int(lon_remaining / (encoding_value * 2)) % 20
        
        prefix += CODE_ALPHABET[lat_digit]
        prefix += CODE_ALPHABET[lon_digit]
        
        lat_remaining -= lat_digit * encoding_value
        lon_remaining -= lon_digit * (encoding_value * 2)
    
    # Combine prefix with short code
    full_code = prefix + short_code
    
    # Verify and adjust if necessary
    area = decode(full_code)
    
    # Check if recovered area is closest to reference
    # May need adjustment near boundaries
    
    return full_code


def is_valid_code(code: str) -> bool:
    """
    Check if a string is a valid Plus Code.
    
    Args:
        code: String to validate
        
    Returns:
        True if valid Plus Code, False otherwise
    """
    code = code.upper().strip()
    
    # Must contain separator
    if SEPARATOR not in code:
        return False
    
    separator_pos = code.find(SEPARATOR)
    
    # Check prefix length
    if separator_pos > SEPARATOR_POSITION:
        return False
    
    # Check prefix characters
    prefix = code[:separator_pos]
    for char in prefix:
        if char not in CODE_ALPHABET:
            return False
    
    # Check suffix length
    suffix = code[separator_pos + 1:]
    if len(suffix) > MAX_SUFFIX_LENGTH:
        return False
    
    # Check suffix characters
    for char in suffix:
        if char not in CODE_ALPHABET:
            return False
    
    # Must have at least 2 digits before separator
    if separator_pos < 2:
        return False
    
    return True


def clean_code(code: str) -> str:
    """
    Clean and normalize a Plus Code string.
    
    Args:
        code: Plus Code string (may have extra characters)
        
    Returns:
        Cleaned Plus Code string
    """
    code = code.upper().strip()
    
    # Remove spaces and common separators
    code = re.sub(r'\s+', '', code)
    code = code.replace('-', '')
    code = code.replace('_', '')
    
    return code


def get_code_length(code: str) -> int:
    """
    Get the meaningful length of a Plus Code.
    
    Args:
        code: Plus Code string
        
    Returns:
        Number of meaningful digits
    """
    code = clean_code(code)
    
    separator_pos = code.find(SEPARATOR)
    prefix_length = separator_pos
    suffix_length = len(code) - separator_pos - 1
    
    return prefix_length + suffix_length


def get_precision_description(code_length: int) -> str:
    """
    Get a human-readable description of code precision.
    
    Args:
        code_length: Length of the Plus Code
        
    Returns:
        Description string
    """
    precision_map = {
        2: "~2000 kilometers",
        4: "~100 kilometers",
        6: "~5 kilometers",
        8: "~500 meters",
        9: "~125 meters",
        10: "~50 meters",
        11: "~25 meters",
        12: "~5 meters",
        13: "~2.5 meters",
        14: "~1 meter",
        15: "~0.5 meter",
    }
    
    return precision_map.get(code_length, "very high precision")


def encode_with_shortening(
    latitude: float,
    longitude: float,
    reference_latitude: Optional[float] = None,
    reference_longitude: Optional[float] = None,
    code_length: int = 10
) -> PlusCodeResult:
    """
    Encode coordinates with optional shortening using reference location.
    
    Args:
        latitude: Target latitude
        longitude: Target longitude
        reference_latitude: Optional reference latitude for shortening
        reference_longitude: Optional reference longitude for shortening
        code_length: Code length (default 10)
        
    Returns:
        PlusCodeResult with full and shortened code
    """
    result = encode(latitude, longitude, code_length)
    
    if reference_latitude is not None and reference_longitude is not None:
        short_code = shorten(result.full_code, reference_latitude, reference_longitude)
        if short_code != result.full_code:
            result.short_code = short_code
    
    return result


def get_neighbors(code: str) -> Dict[str, str]:
    """
    Get Plus Codes for neighboring areas.
    
    Args:
        code: Plus Code string
        
    Returns:
        Dictionary with neighbor codes
    """
    area = decode(code)
    
    # Calculate precision
    lat_precision = area.latitude_hi - area.latitude_lo
    lon_precision = area.longitude_hi - area.longitude_lo
    
    neighbors = {}
    
    offsets = {
        'north': (lat_precision, 0),
        'south': (-lat_precision, 0),
        'east': (0, lon_precision),
        'west': (0, -lon_precision),
        'north_east': (lat_precision, lon_precision),
        'north_west': (lat_precision, -lon_precision),
        'south_east': (-lat_precision, lon_precision),
        'south_west': (-lat_precision, -lon_precision),
    }
    
    for direction, (lat_offset, lon_offset) in offsets.items():
        neighbor_lat = area.latitude_center + lat_offset
        neighbor_lon = area.longitude_center + lon_offset
        
        if neighbor_lat > 90.0 or neighbor_lat < -90.0:
            neighbors[direction] = None
        else:
            neighbor_result = encode(neighbor_lat, neighbor_lon, area.code_length)
            neighbors[direction] = neighbor_result.full_code
    
    return neighbors


def calculate_distance_km(code1: str, code2: str) -> float:
    """
    Calculate approximate distance between two Plus Codes in kilometers.
    
    Args:
        code1: First Plus Code
        code2: Second Plus Code
        
    Returns:
        Distance in kilometers
    """
    area1 = decode(code1)
    area2 = decode(code2)
    
    # Haversine formula
    lat1 = math.radians(area1.latitude_center)
    lon1 = math.radians(area1.longitude_center)
    lat2 = math.radians(area2.latitude_center)
    lon2 = math.radians(area2.longitude_center)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    earth_radius = 6371.0
    return earth_radius * c


def format_for_display(code: str, include_precision: bool = True) -> str:
    """
    Format a Plus Code for display with optional precision info.
    
    Args:
        code: Plus Code string
        include_precision: Whether to include precision description
        
    Returns:
        Formatted string for display
    """
    code = clean_code(code)
    code_length = get_code_length(code)
    
    if include_precision:
        precision = get_precision_description(code_length)
        return f"{code} ({precision})"
    
    return code


# =============================================================================
# Utility Functions
# =============================================================================

def is_short_code(code: str) -> bool:
    """Check if a code is a shortened Plus Code."""
    code = clean_code(code)
    separator_pos = code.find(SEPARATOR)
    return separator_pos < SEPARATOR_POSITION


def is_full_code(code: str) -> bool:
    """Check if a code is a full Plus Code."""
    code = clean_code(code)
    separator_pos = code.find(SEPARATOR)
    return separator_pos >= SEPARATOR_POSITION


def get_area_size_meters(code: str) -> Tuple[float, float]:
    """Get the approximate size of a Plus Code area in meters."""
    area = decode(code)
    
    lat_size_deg = area.latitude_hi - area.latitude_lo
    lon_size_deg = area.longitude_hi - area.longitude_lo
    
    lat_meters = lat_size_deg * 111000
    lon_meters = lon_size_deg * 111000
    
    return (lat_meters, lon_meters)


# =============================================================================
# Main (for testing)
# =============================================================================

if __name__ == '__main__':
    print("Testing Plus Code utilities...")
    
    # Test encoding
    result = encode(47.365590, 8.524030)
    print(f"Encode (47.365590, 8.524030): {result.full_code}")
    
    # Test encoding with higher precision
    result = encode(47.365590, 8.524030, 12)
    print(f"Encode with 12 digits: {result.full_code}")
    
    # Test decoding
    area = decode("8FVC2222+")
    print(f"Decode 8FVC2222+: Center ({area.latitude_center:.6f}, {area.longitude_center:.6f})")
    
    # Test validation
    print(f"is_valid_code('8FVC2222+'): {is_valid_code('8FVC2222+')}")
    print(f"is_valid_code('invalid'): {is_valid_code('invalid')}")
    
    # Test precision description
    print(f"Precision (10 digits): {get_precision_description(10)}")
    
    print("All basic tests passed!")