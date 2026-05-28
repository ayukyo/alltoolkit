#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Geohash Utilities Module
=====================================
A comprehensive geohash encoding/decoding utility module for Python with zero external dependencies.

Features:
    - Geohash encoding (lat/lng to geohash string)
    - Geohash decoding (geohash string to lat/lng bounds)
    - Neighbor geohash calculation (all 8 directions)
    - Geohash prefix/prefix search
    - Distance calculation between geohashes
    - Bounding box to geohash coverage
    - Geohash validation and properties
    - Precision-based area estimation

Geohash is a geocoding system invented by Gustavo Niemeyer that encodes
geographic coordinates into a short string of letters and digits.

Author: AllToolkit Contributors
License: MIT
"""

from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
import math


# ============================================================================
# Constants
# ============================================================================

# Base32 character set used in geohashing
BASE32_CHARS = '0123456789bcdefghjkmnpqrstuvwxyz'

# Reverse lookup: character to index
BASE32_DECODE = {char: idx for idx, char in enumerate(BASE32_CHARS)}

# Neighbor directions: (lat_offset, lng_offset) in terms of geohash grid
# Directions: n, ne, e, se, s, sw, w, nw
DIRECTIONS = {
    'n': (1, 0),
    'ne': (1, 1),
    'e': (0, 1),
    'se': (-1, 1),
    's': (-1, 0),
    'sw': (-1, -1),
    'w': (0, -1),
    'nw': (1, -1),
}

# Bounding box for valid coordinates
LAT_RANGE = (-90.0, 90.0)
LNG_RANGE = (-180.0, 180.0)

# Approximate cell dimensions at each precision level
# Format: (width_km, height_km) at equator
PRECISION_DIMS = {
    1: (5000.0, 5000.0),
    2: (1250.0, 625.0),
    3: (156.0, 156.0),
    4: (39.1, 19.5),
    5: (4.9, 4.9),
    6: (1.2, 0.61),
    7: (0.152, 0.152),
    8: (0.038, 0.019),
    9: (0.0048, 0.0048),
    10: (0.0012, 0.0006),
    11: (0.000149, 0.000149),
    12: (0.000037, 0.000019),
}


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class GeoPoint:
    """A geographic point with latitude and longitude."""
    lat: float
    lng: float
    
    def __post_init__(self):
        """Validate coordinates."""
        if not (LAT_RANGE[0] <= self.lat <= LAT_RANGE[1]):
            raise ValueError(f"Latitude must be between {LAT_RANGE[0]} and {LAT_RANGE[1]}, got {self.lat}")
        if not (LNG_RANGE[0] <= self.lng <= LNG_RANGE[1]):
            raise ValueError(f"Longitude must be between {LNG_RANGE[0]} and {LNG_RANGE[1]}, got {self.lng}")
    
    def distance_to(self, other: 'GeoPoint') -> float:
        """Calculate distance to another point in kilometers using Haversine formula."""
        return haversine_distance(self.lat, self.lng, other.lat, other.lng)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {'lat': self.lat, 'lng': self.lng}
    
    def __repr__(self) -> str:
        return f"GeoPoint(lat={self.lat:.6f}, lng={self.lng:.6f})"


@dataclass
class GeoBounds:
    """Geographic bounding box."""
    min_lat: float
    max_lat: float
    min_lng: float
    max_lng: float
    
    @property
    def center(self) -> Tuple[float, float]:
        """Get center point of bounds."""
        return ((self.min_lat + self.max_lat) / 2, 
                (self.min_lng + self.max_lng) / 2)
    
    @property
    def width(self) -> float:
        """Get width in degrees."""
        return self.max_lng - self.min_lng
    
    @property
    def height(self) -> float:
        """Get height in degrees."""
        return self.max_lat - self.min_lat
    
    def contains(self, lat: float, lng: float) -> bool:
        """Check if a point is within bounds."""
        return (self.min_lat <= lat <= self.max_lat and 
                self.min_lng <= lng <= self.max_lng)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'min_lat': self.min_lat,
            'max_lat': self.max_lat,
            'min_lng': self.min_lng,
            'max_lng': self.max_lng,
        }
    
    def __repr__(self) -> str:
        return f"GeoBounds(lat=[{self.min_lat:.6f}, {self.max_lat:.6f}], lng=[{self.min_lng:.6f}, {self.max_lng:.6f}])"


@dataclass
class GeoCell:
    """A geohash cell with its properties."""
    geohash: str
    bounds: GeoBounds
    center: Tuple[float, float]
    precision: int
    width_km: float
    height_km: float
    
    def contains(self, lat: float, lng: float) -> bool:
        """Check if a point is within this cell."""
        return self.bounds.contains(lat, lng)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'geohash': self.geohash,
            'bounds': self.bounds.to_dict(),
            'center': self.center,
            'precision': self.precision,
            'width_km': self.width_km,
            'height_km': self.height_km,
        }


# ============================================================================
# Encoding Functions
# ============================================================================

def encode(lat: float, lng: float, precision: int = 12) -> str:
    """
    Encode latitude and longitude into a geohash string.
    
    Args:
        lat: Latitude (-90 to 90)
        lng: Longitude (-180 to 180)
        precision: Number of characters in output (1-12, default 12)
    
    Returns:
        Geohash string of specified precision
    
    Raises:
        ValueError: If coordinates are out of range or precision is invalid
    
    Example:
        >>> encode(57.64911, 10.40744, 6)
        'u4pruy'
        >>> encode(40.7128, -74.0060, 10)
        'dr5ru7j0qc'
    """
    if not (1 <= precision <= 12):
        raise ValueError(f"Precision must be between 1 and 12, got {precision}")
    
    if not (LAT_RANGE[0] <= lat <= LAT_RANGE[1]):
        raise ValueError(f"Latitude must be between {LAT_RANGE[0]} and {LAT_RANGE[1]}, got {lat}")
    
    if not (LNG_RANGE[0] <= lng <= LNG_RANGE[1]):
        raise ValueError(f"Longitude must be between {LNG_RANGE[0]} and {LNG_RANGE[1]}, got {lng}")
    
    # Initialize bit collection
    bits = 0
    bit_length = precision * 5  # 5 bits per character
    
    # Binary search ranges
    lat_range = list(LAT_RANGE)
    lng_range = list(LNG_RANGE)
    
    # Alternate between longitude and latitude bits
    for i in range(bit_length):
        if i % 2 == 0:
            # Longitude bit (even positions)
            mid = (lng_range[0] + lng_range[1]) / 2
            if lng >= mid:
                bits = (bits << 1) | 1
                lng_range[0] = mid
            else:
                bits = bits << 1
                lng_range[1] = mid
        else:
            # Latitude bit (odd positions)
            mid = (lat_range[0] + lat_range[1]) / 2
            if lat >= mid:
                bits = (bits << 1) | 1
                lat_range[0] = mid
            else:
                bits = bits << 1
                lat_range[1] = mid
    
    # Convert bits to base32 string
    chars = []
    for i in range(precision):
        # Extract 5 bits from the right
        idx = (bits >> (5 * (precision - i - 1))) & 0x1F
        chars.append(BASE32_CHARS[idx])
    
    return ''.join(chars)


def decode(geohash: str, round_result: bool = True) -> Tuple[float, float]:
    """
    Decode a geohash string to latitude and longitude.
    
    Args:
        geohash: Geohash string to decode
        round_result: If True, round result to precision-appropriate decimal places
    
    Returns:
        Tuple of (latitude, longitude) - the center point of the geohash cell
    
    Raises:
        ValueError: If geohash contains invalid characters
    
    Example:
        >>> lat, lng = decode('u4pruy')
        >>> print(f"{lat:.5f}, {lng:.5f}")
        57.64911, 10.40744
    """
    geohash = geohash.lower().strip()
    
    if not geohash:
        raise ValueError("Geohash cannot be empty")
    
    # Validate characters
    for char in geohash:
        if char not in BASE32_DECODE:
            raise ValueError(f"Invalid geohash character: '{char}'")
    
    # Initialize ranges
    lat_range = list(LAT_RANGE)
    lng_range = list(LNG_RANGE)
    
    # Process each character
    for i, char in enumerate(geohash):
        bits = BASE32_DECODE[char]
        
        # Process 5 bits per character
        for j in range(4, -1, -1):
            bit = (bits >> j) & 1
            
            # Even positions (0, 2, 4, ...) are longitude
            # Odd positions (1, 3, 5, ...) are latitude
            # Position within the overall bit stream
            pos = i * 5 + (4 - j)
            
            if pos % 2 == 0:
                # Longitude bit
                mid = (lng_range[0] + lng_range[1]) / 2
                if bit:
                    lng_range[0] = mid
                else:
                    lng_range[1] = mid
            else:
                # Latitude bit
                mid = (lat_range[0] + lat_range[1]) / 2
                if bit:
                    lat_range[0] = mid
                else:
                    lat_range[1] = mid
    
    # Calculate center point
    lat = (lat_range[0] + lat_range[1]) / 2
    lng = (lng_range[0] + lng_range[1]) / 2
    
    if round_result:
        # Round to appropriate precision
        # More characters = more decimal places
        decimals = min(12, len(geohash) * 2 + 1)
        lat = round(lat, decimals)
        lng = round(lng, decimals)
    
    return (lat, lng)


def decode_bounds(geohash: str) -> GeoBounds:
    """
    Decode a geohash to its bounding box.
    
    Args:
        geohash: Geohash string to decode
    
    Returns:
        GeoBounds with the bounding box coordinates
    
    Example:
        >>> bounds = decode_bounds('u4pruy')
        >>> print(bounds)
        GeoBounds(lat=[57.64909, 57.64914], lng=[10.40741, 10.40747])
    """
    geohash = geohash.lower().strip()
    
    if not geohash:
        raise ValueError("Geohash cannot be empty")
    
    for char in geohash:
        if char not in BASE32_DECODE:
            raise ValueError(f"Invalid geohash character: '{char}'")
    
    # Initialize ranges
    lat_range = list(LAT_RANGE)
    lng_range = list(LNG_RANGE)
    
    # Process each character
    for i, char in enumerate(geohash):
        bits = BASE32_DECODE[char]
        
        for j in range(4, -1, -1):
            bit = (bits >> j) & 1
            pos = i * 5 + (4 - j)
            
            if pos % 2 == 0:
                mid = (lng_range[0] + lng_range[1]) / 2
                if bit:
                    lng_range[0] = mid
                else:
                    lng_range[1] = mid
            else:
                mid = (lat_range[0] + lat_range[1]) / 2
                if bit:
                    lat_range[0] = mid
                else:
                    lat_range[1] = mid
    
    return GeoBounds(
        min_lat=lat_range[0],
        max_lat=lat_range[1],
        min_lng=lng_range[0],
        max_lng=lng_range[1],
    )


# ============================================================================
# Neighbor Functions
# ============================================================================

def neighbors(geohash: str) -> Dict[str, str]:
    """
    Get all 8 neighboring geohashes.
    
    Args:
        geohash: The geohash to find neighbors for
    
    Returns:
        Dictionary mapping direction to neighbor geohash
        Keys: 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'
    
    Example:
        >>> n = neighbors('u4pruy')
        >>> n['n']
        'u4pruz'
    """
    result = {}
    for direction in DIRECTIONS:
        result[direction] = neighbor(geohash, direction)
    return result


def neighbor(geohash: str, direction: str) -> str:
    """
    Get the neighbor geohash in a specific direction.
    
    Args:
        geohash: The geohash
        direction: Direction ('n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw')
    
    Returns:
        The neighboring geohash
    
    Raises:
        ValueError: If direction is invalid
    
    Example:
        >>> neighbor('u4pruy', 'n')
        'u4pruz'
    """
    direction = direction.lower()
    
    if direction not in DIRECTIONS:
        raise ValueError(f"Invalid direction: '{direction}'. Must be one of: {list(DIRECTIONS.keys())}")
    
    geohash = geohash.lower().strip()
    
    # Get bounds for the geohash
    bounds = decode_bounds(geohash)
    
    # Get center and calculate offset
    center_lat, center_lng = bounds.center
    
    # Calculate cell dimensions
    lat_height = bounds.height
    lng_width = bounds.width
    
    # Get direction offset
    lat_offset, lng_offset = DIRECTIONS[direction]
    
    # Calculate neighbor center
    new_lat = center_lat + (lat_offset * lat_height)
    new_lng = center_lng + (lng_offset * lng_width)
    
    # Handle wrapping around the world for longitude
    if new_lng > 180:
        new_lng -= 360
    elif new_lng < -180:
        new_lng += 360
    
    # Handle poles for latitude
    if new_lat > 90:
        # Wrap to other pole (this is edge case behavior)
        new_lat = 180 - new_lat
        new_lng = new_lng + 180 if new_lng < 0 else new_lng - 180
    elif new_lat < -90:
        new_lat = -180 - new_lat
        new_lng = new_lng + 180 if new_lng < 0 else new_lng - 180
    
    # Re-encode with same precision
    return encode(new_lat, new_lng, len(geohash))


def expand(geohash: str, radius_km: float) -> List[str]:
    """
    Expand a geohash to include all geohashes within a given radius.
    
    Args:
        geohash: The center geohash
        radius_km: Radius in kilometers
    
    Returns:
        List of geohashes that could be within the radius (including center)
    
    Example:
        >>> expand('u4pruy', 1.0)  # Get geohashes within 1km
        ['u4pruy', 'u4pruz', 'u4prux', ...]
    """
    # Get approximate cell size
    precision = len(geohash)
    dims = get_cell_dimensions(precision)
    cell_km = max(dims[0], dims[1])
    
    # Calculate how many cells we need to expand
    # Be conservative and expand enough cells to cover the radius
    num_cells = max(1, int(math.ceil(radius_km / cell_km)))
    
    result = set([geohash])
    
    # Iteratively expand
    for _ in range(num_cells):
        new_cells = set()
        for gh in result:
            for n in neighbors(gh).values():
                new_cells.add(n)
        result.update(new_cells)
    
    return sorted(result)


# ============================================================================
# Distance Functions
# ============================================================================

def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate the great-circle distance between two points using Haversine formula.
    
    Args:
        lat1, lng1: First point coordinates
        lat2, lng2: Second point coordinates
    
    Returns:
        Distance in kilometers
    
    Example:
        >>> haversine_distance(40.7128, -74.0060, 34.0522, -118.2437)  # NYC to LA
        3935.746...
    """
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lng1_rad = math.radians(lng1)
    lng2_rad = math.radians(lng2)
    
    # Differences
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def distance(geohash1: str, geohash2: str) -> float:
    """
    Calculate distance between two geohashes in kilometers.
    
    Args:
        geohash1: First geohash
        geohash2: Second geohash
    
    Returns:
        Distance in kilometers
    
    Example:
        >>> distance('dr5ru7', '9q8yhu')
        3935.746...
    """
    lat1, lng1 = decode(geohash1)
    lat2, lng2 = decode(geohash2)
    return haversine_distance(lat1, lng1, lat2, lng2)


def distance_point_to_geohash(lat: float, lng: float, geohash: str) -> float:
    """
    Calculate distance from a point to the center of a geohash.
    
    Args:
        lat, lng: Point coordinates
        geohash: Geohash
    
    Returns:
        Distance in kilometers
    """
    gh_lat, gh_lng = decode(geohash)
    return haversine_distance(lat, lng, gh_lat, gh_lng)


# ============================================================================
# Validation Functions
# ============================================================================

def is_valid(geohash: str) -> bool:
    """
    Check if a geohash string is valid.
    
    Args:
        geohash: Geohash string to validate
    
    Returns:
        True if valid, False otherwise
    
    Example:
        >>> is_valid('u4pruy')
        True
        >>> is_valid('u4prui')  # 'i' is not valid
        False
    """
    if not geohash:
        return False
    
    geohash = geohash.lower().strip()
    
    for char in geohash:
        if char not in BASE32_DECODE:
            return False
    
    return True


def validate(geohash: str) -> str:
    """
    Validate and normalize a geohash string.
    
    Args:
        geohash: Geohash string to validate
    
    Returns:
        Normalized (lowercase) geohash
    
    Raises:
        ValueError: If geohash is invalid
    
    Example:
        >>> validate('U4PRUY')
        'u4pruy'
    """
    geohash = geohash.lower().strip()
    
    if not geohash:
        raise ValueError("Geohash cannot be empty")
    
    for char in geohash:
        if char not in BASE32_DECODE:
            raise ValueError(f"Invalid geohash character: '{char}'")
    
    return geohash


# ============================================================================
# Utility Functions
# ============================================================================

def get_precision(geohash: str) -> int:
    """
    Get the precision (length) of a geohash.
    
    Args:
        geohash: Geohash string
    
    Returns:
        Precision (length) of the geohash
    """
    return len(validate(geohash))


def get_cell_dimensions(precision: int) -> Tuple[float, float]:
    """
    Get approximate cell dimensions at a given precision.
    
    Args:
        precision: Geohash precision (1-12)
    
    Returns:
        Tuple of (width_km, height_km) at equator
    
    Example:
        >>> get_cell_dimensions(6)
        (1.2, 0.61)
    """
    if precision not in PRECISION_DIMS:
        precision = max(1, min(12, precision))
    return PRECISION_DIMS.get(precision, (0.001, 0.001))


def get_cell_area(precision: int) -> float:
    """
    Get approximate cell area at a given precision in square kilometers.
    
    Args:
        precision: Geohash precision (1-12)
    
    Returns:
        Approximate area in square kilometers
    """
    width, height = get_cell_dimensions(precision)
    return width * height


def common_prefix(geohashes: List[str]) -> str:
    """
    Find the common prefix of a list of geohashes.
    
    Args:
        geohashes: List of geohash strings
    
    Returns:
        Common prefix string
    
    Example:
        >>> common_prefix(['u4pruy', 'u4pruz', 'u4prux'])
        'u4pru'
    """
    if not geohashes:
        return ''
    
    geohashes = [validate(gh) for gh in geohashes]
    
    prefix = geohashes[0]
    for gh in geohashes[1:]:
        while not gh.startswith(prefix) and prefix:
            prefix = prefix[:-1]
    
    return prefix


def covers_area(sw_lat: float, sw_lng: float, ne_lat: float, ne_lng: float, 
                precision: int = 6) -> List[str]:
    """
    Get all geohashes that cover a rectangular area.
    
    Args:
        sw_lat: Southwest latitude
        sw_lng: Southwest longitude
        ne_lat: Northeast latitude
        ne_lng: Northeast longitude
        precision: Geohash precision (default 6)
    
    Returns:
        List of geohashes covering the area
    
    Example:
        >>> covers_area(40.7, -74.1, 40.8, -73.9, 6)
        ['dr5ru7', 'dr5ru7', ...]
    """
    # Calculate grid dimensions
    dims = get_cell_dimensions(precision)
    cell_width = dims[0] / 111.0  # Convert km to degrees (approximate)
    cell_height = dims[1] / 111.0
    
    # Generate grid of points
    geohashes = set()
    
    lat = sw_lat
    while lat <= ne_lat:
        lng = sw_lng
        while lng <= ne_lng:
            gh = encode(lat, lng, precision)
            geohashes.add(gh)
            lng += cell_width
        lat += cell_height
    
    # Also check corners and edges for coverage
    corners = [
        (sw_lat, sw_lng),
        (sw_lat, ne_lng),
        (ne_lat, sw_lng),
        (ne_lat, ne_lng),
    ]
    
    for lat, lng in corners:
        geohashes.add(encode(lat, lng, precision))
    
    return sorted(geohashes)


# ============================================================================
# Cell Info Functions
# ============================================================================

def get_cell(geohash: str) -> GeoCell:
    """
    Get detailed information about a geohash cell.
    
    Args:
        geohash: Geohash string
    
    Returns:
        GeoCell with bounds, center, dimensions, etc.
    
    Example:
        >>> cell = get_cell('u4pruy')
        >>> cell.center
        (57.64911, 10.40744)
    """
    geohash = validate(geohash)
    bounds = decode_bounds(geohash)
    center = bounds.center
    precision = len(geohash)
    dims = get_cell_dimensions(precision)
    
    return GeoCell(
        geohash=geohash,
        bounds=bounds,
        center=center,
        precision=precision,
        width_km=dims[0],
        height_km=dims[1],
    )


def children(geohash: str) -> List[str]:
    """
    Get the 32 child geohashes (one precision level deeper).
    
    Args:
        geohash: Parent geohash
    
    Returns:
        List of 32 child geohashes
    
    Example:
        >>> children('u4')
        ['u40', 'u41', 'u42', ...]
    """
    geohash = validate(geohash)
    return [geohash + char for char in BASE32_CHARS]


def parent(geohash: str) -> Optional[str]:
    """
    Get the parent geohash (one precision level up).
    
    Args:
        geohash: Child geohash
    
    Returns:
        Parent geohash or None if already at precision 1
    
    Example:
        >>> parent('u4pruy')
        'u4pru'
    """
    geohash = validate(geohash)
    if len(geohash) <= 1:
        return None
    return geohash[:-1]


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    # Demo
    print("Geohash Utilities Demo")
    print("=" * 60)
    
    # Encoding examples
    print("\nEncoding:")
    locations = [
        (57.64911, 10.40744, "Aalborg, Denmark"),
        (40.7128, -74.0060, "New York City"),
        (35.6762, 139.6503, "Tokyo"),
        (-33.8688, 151.2093, "Sydney"),
        (51.5074, -0.1278, "London"),
    ]
    
    for lat, lng, name in locations:
        for precision in [6, 8, 10]:
            gh = encode(lat, lng, precision)
            print(f"  {name} ({precision}): {gh}")
    
    # Decoding examples
    print("\nDecoding:")
    geohashes = ['u4pruy', 'dr5ru7j0', 'xn76urwe']
    for gh in geohashes:
        lat, lng = decode(gh)
        bounds = decode_bounds(gh)
        print(f"  {gh}: ({lat:.5f}, {lng:.5f})")
        print(f"    Bounds: {bounds}")
    
    # Neighbor examples
    print("\nNeighbors:")
    gh = 'u4pruy'
    n = neighbors(gh)
    print(f"  Center: {gh}")
    for direction, neighbor_gh in n.items():
        print(f"    {direction}: {neighbor_gh}")
    
    # Distance examples
    print("\nDistance:")
    gh1, gh2 = 'dr5ru7', '9q8yhu'
    dist = distance(gh1, gh2)
    print(f"  {gh1} to {gh2}: {dist:.2f} km")
    
    # Cell info
    print("\nCell Info:")
    cell = get_cell('u4pruy')
    print(f"  Geohash: {cell.geohash}")
    print(f"  Center: {cell.center}")
    print(f"  Bounds: {cell.bounds}")
    print(f"  Precision: {cell.precision}")
    print(f"  Dimensions: {cell.width_km:.4f} km x {cell.height_km:.4f} km")