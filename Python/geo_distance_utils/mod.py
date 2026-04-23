#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Geographic Distance Utilities Module
====================================================
A comprehensive geographic distance calculation module for Python with zero external dependencies.

Features:
    - Haversine distance (Earth surface distance between coordinates)
    - Vincenty distance (more accurate ellipsoidal distance)
    - Bearing/azimuth calculation between coordinates
    - Destination point from start point + bearing + distance
    - Coordinate midpoint calculation
    - Point-in-polygon (geographic polygon)
    - Coordinate validation and normalization
    - Distance unit conversions (km, miles, nautical miles, meters)
    - Great circle path interpolation
    - Bounding box calculation for radius search

Author: AllToolkit Contributors
License: MIT
"""

import math
from typing import Any, Dict, List, Optional, Tuple, Union


# ============================================================================
# Type Aliases
# ============================================================================

Coordinate = Tuple[float, float]  # (latitude, longitude)
Coordinate3D = Tuple[float, float, float]  # (latitude, longitude, altitude)


# ============================================================================
# Constants
# ============================================================================

# Earth parameters
EARTH_RADIUS_KM = 6371.0  # Mean Earth radius in kilometers
EARTH_RADIUS_M = 6371000.0  # Mean Earth radius in meters
EARTH_RADIUS_MILES = 3958.8  # Mean Earth radius in miles
EARTH_RADIUS_NAUTICAL = 3440.065  # Mean Earth radius in nautical miles

# WGS-84 Ellipsoid parameters (for Vincenty formula)
WGS84_SEMI_MAJOR = 6378137.0  # Semi-major axis (a) in meters
WGS84_SEMI_MINOR = 6356752.314245  # Semi-minor axis (b) in meters
WGS84_FLATTENING = 1 / 298.257223563  # Flattening (f)

# Conversion factors
KM_TO_MILES = 0.621371
KM_TO_NAUTICAL = 0.539957
MILES_TO_KM = 1.609344
NAUTICAL_TO_KM = 1.852
M_TO_KM = 0.001

# Latitude/longitude bounds
MAX_LATITUDE = 90.0
MIN_LATITUDE = -90.0
MAX_LONGITUDE = 180.0
MIN_LONGITUDE = -180.0

# Degrees to radians conversion
DEG_TO_RAD = math.pi / 180.0
RAD_TO_DEG = 180.0 / math.pi


# ============================================================================
# Utility Functions
# ============================================================================

def _to_float(value: Any) -> float:
    """Convert value to float safely."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _validate_coordinate(lat: float, lng: float) -> Tuple[float, float]:
    """
    Validate and normalize a coordinate.
    
    Args:
        lat: Latitude in degrees
        lng: Longitude in degrees
    
    Returns:
        Tuple (lat, lng) with validated values
    
    Raises:
        ValueError: If coordinates are out of valid range
    """
    lat = _to_float(lat)
    lng = _to_float(lng)
    
    if lat < MIN_LATITUDE or lat > MAX_LATITUDE:
        raise ValueError(f"Latitude must be between {MIN_LATITUDE} and {MAX_LATITUDE}, got {lat}")
    
    # Normalize longitude to [-180, 180]
    while lng < MIN_LONGITUDE:
        lng += 360.0
    while lng > MAX_LONGITUDE:
        lng -= 360.0
    
    return (lat, lng)


def _normalize_longitude(lng: float) -> float:
    """Normalize longitude to [-180, 180] range."""
    lng = _to_float(lng)
    while lng < MIN_LONGITUDE:
        lng += 360.0
    while lng > MAX_LONGITUDE:
        lng -= 360.0
    return lng


def is_valid_coordinate(lat: float, lng: float) -> bool:
    """
    Check if a coordinate is valid.
    
    Args:
        lat: Latitude in degrees
        lng: Longitude in degrees
    
    Returns:
        True if coordinate is valid
    
    Example:
        >>> is_valid_coordinate(39.9, 116.4)
        True
        >>> is_valid_coordinate(91, 0)
        False
    """
    lat = _to_float(lat)
    lng = _to_float(lng)
    return MIN_LATITUDE <= lat <= MAX_LATITUDE and MIN_LONGITUDE <= lng <= MAX_LONGITUDE


def normalize_coordinate(lat: float, lng: float) -> Coordinate:
    """
    Normalize a coordinate (clamp latitude, wrap longitude).
    
    Args:
        lat: Latitude in degrees
        lng: Longitude in degrees
    
    Returns:
        Normalized coordinate (lat, lng)
    
    Example:
        >>> normalize_coordinate(39.9, 200)
        (39.9, -160.0)
        >>> normalize_coordinate(91, 0)  # Latitude clamped
        (90.0, 0.0)
    """
    lat = _to_float(lat)
    lng = _to_float(lng)
    
    # Clamp latitude
    lat = max(MIN_LATITUDE, min(MAX_LATITUDE, lat))
    
    # Wrap longitude
    lng = _normalize_longitude(lng)
    
    return (lat, lng)


# ============================================================================
# Distance Calculations
# ============================================================================

def haversine_distance(coord1: Coordinate, coord2: Coordinate, unit: str = 'km') -> float:
    """
    Calculate the great-circle distance between two coordinates using Haversine formula.
    
    Args:
        coord1: First coordinate (latitude, longitude) in degrees
        coord2: Second coordinate (latitude, longitude) in degrees
        unit: Distance unit ('km', 'm', 'miles', 'nautical')
    
    Returns:
        Distance in specified unit
    
    Example:
        >>> haversine_distance((39.9042, 116.4074), (31.2304, 121.4737))
        1068.3...
        >>> haversine_distance((0, 0), (0, 1))
        111.19...
    
    Note:
        Haversine formula assumes a spherical Earth with radius 6371 km.
        For more accurate results on ellipsoidal Earth, use vincenty_distance.
    """
    lat1, lng1 = _to_float(coord1[0]), _to_float(coord1[1])
    lat2, lng2 = _to_float(coord2[0]), _to_float(coord2[1])
    
    # Convert to radians
    lat1_rad = lat1 * DEG_TO_RAD
    lat2_rad = lat2 * DEG_TO_RAD
    lng1_rad = lng1 * DEG_TO_RAD
    lng2_rad = lng2 * DEG_TO_RAD
    
    # Differences
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in kilometers
    distance_km = EARTH_RADIUS_KM * c
    
    # Convert to requested unit
    unit = unit.lower()
    if unit == 'km':
        return distance_km
    elif unit == 'm':
        return distance_km * 1000
    elif unit == 'miles':
        return distance_km * KM_TO_MILES
    elif unit == 'nautical':
        return distance_km * KM_TO_NAUTICAL
    else:
        raise ValueError(f"Unknown unit: {unit}. Use 'km', 'm', 'miles', or 'nautical'")


def vincenty_distance(coord1: Coordinate, coord2: Coordinate, unit: str = 'km', max_iterations: int = 200) -> float:
    """
    Calculate distance between two coordinates using Vincenty's formulae.
    
    More accurate than Haversine for ellipsoidal Earth (WGS-84).
    
    Args:
        coord1: First coordinate (latitude, longitude) in degrees
        coord2: Second coordinate (latitude, longitude) in degrees
        unit: Distance unit ('km', 'm', 'miles', 'nautical')
        max_iterations: Maximum iterations for convergence
    
    Returns:
        Distance in specified unit, or 0 if fails to converge
    
    Example:
        >>> vincenty_distance((39.9042, 116.4074), (31.2304, 121.4737))
        1067.3...
        >>> vincenty_distance((0, 0), (0, 1))
        111.3...
    
    Note:
        Vincenty formula is more accurate but slower than Haversine.
        Returns 0 if the algorithm fails to converge (rare, occurs for
        nearly antipodal points).
    """
    lat1, lng1 = _to_float(coord1[0]), _to_float(coord1[1])
    lat2, lng2 = _to_float(coord2[0]), _to_float(coord2[1])
    
    # Convert to radians
    lat1_rad = lat1 * DEG_TO_RAD
    lat2_rad = lat2 * DEG_TO_RAD
    lng1_rad = lng1 * DEG_TO_RAD
    lng2_rad = lng2 * DEG_TO_RAD
    
    # WGS-84 parameters
    a = WGS84_SEMI_MAJOR
    b = WGS84_SEMI_MINOR
    f = WGS84_FLATTENING
    
    # Reduced latitudes
    U1 = math.atan((1 - f) * math.tan(lat1_rad))
    U2 = math.atan((1 - f) * math.tan(lat2_rad))
    
    L = lng2_rad - lng1_rad
    lambda_val = L
    
    sin_U1 = math.sin(U1)
    cos_U1 = math.cos(U1)
    sin_U2 = math.sin(U2)
    cos_U2 = math.cos(U2)
    
    # Iterative calculation
    for _ in range(max_iterations):
        sin_lambda = math.sin(lambda_val)
        cos_lambda = math.cos(lambda_val)
        
        sin_sigma = math.sqrt(
            (cos_U2 * sin_lambda) ** 2 +
            (cos_U1 * sin_U2 - sin_U1 * cos_U2 * cos_lambda) ** 2
        )
        
        if sin_sigma == 0:
            return 0.0  # Coincident points
        
        cos_sigma = sin_U1 * sin_U2 + cos_U1 * cos_U2 * cos_lambda
        sigma = math.atan2(sin_sigma, cos_sigma)
        
        sin_alpha = cos_U1 * cos_U2 * sin_lambda / sin_sigma
        cos_sq_alpha = 1 - sin_alpha ** 2
        
        if cos_sq_alpha == 0:
            cos_2sigma_m = 0
        else:
            cos_2sigma_m = cos_sigma - 2 * sin_U1 * sin_U2 / cos_sq_alpha
        
        C = f / 16 * cos_sq_alpha * (4 + f * (4 - 3 * cos_sq_alpha))
        
        lambda_prev = lambda_val
        lambda_val = L + (1 - C) * f * sin_alpha * (
            sigma + C * sin_sigma * (
                cos_2sigma_m + C * cos_sigma * (-1 + 2 * cos_2sigma_m ** 2)
            )
        )
        
        # Check convergence
        if abs(lambda_val - lambda_prev) < 1e-12:
            break
    
    # If not converged, return 0
    if abs(lambda_val - lambda_prev) >= 1e-12:
        return 0.0
    
    # Calculate distance
    u_sq = cos_sq_alpha * (a ** 2 - b ** 2) / (b ** 2)
    A = 1 + u_sq / 16384 * (4096 + u_sq * (-768 + u_sq * (320 - 175 * u_sq)))
    B = u_sq / 1024 * (256 + u_sq * (-128 + u_sq * (74 - 47 * u_sq)))
    
    delta_sigma = B * sin_sigma * (
        cos_2sigma_m + B / 4 * (
            cos_sigma * (-1 + 2 * cos_2sigma_m ** 2) -
            B / 6 * cos_2sigma_m * (-3 + 4 * sin_sigma ** 2) * (-3 + 4 * cos_2sigma_m ** 2)
        )
    )
    
    distance_m = b * A * (sigma - delta_sigma)
    
    # Convert to requested unit
    unit = unit.lower()
    if unit == 'km':
        return distance_m * M_TO_KM
    elif unit == 'm':
        return distance_m
    elif unit == 'miles':
        return distance_m * M_TO_KM * KM_TO_MILES
    elif unit == 'nautical':
        return distance_m * M_TO_KM * KM_TO_NAUTICAL
    else:
        raise ValueError(f"Unknown unit: {unit}")


def distance(coord1: Coordinate, coord2: Coordinate, unit: str = 'km', method: str = 'haversine') -> float:
    """
    Calculate distance between two coordinates.
    
    Args:
        coord1: First coordinate (latitude, longitude) in degrees
        coord2: Second coordinate (latitude, longitude) in degrees
        unit: Distance unit ('km', 'm', 'miles', 'nautical')
        method: Calculation method ('haversine' or 'vincenty')
    
    Returns:
        Distance in specified unit
    
    Example:
        >>> distance((39.9, 116.4), (31.2, 121.5))
        1068.3...
        >>> distance((39.9, 116.4), (31.2, 121.5), method='vincenty')
        1067.3...
    """
    method = method.lower()
    if method == 'haversine':
        return haversine_distance(coord1, coord2, unit)
    elif method == 'vincenty':
        return vincenty_distance(coord1, coord2, unit)
    else:
        raise ValueError(f"Unknown method: {method}. Use 'haversine' or 'vincenty'")


# ============================================================================
# Bearing Calculations
# ============================================================================

def initial_bearing(coord1: Coordinate, coord2: Coordinate) -> float:
    """
    Calculate the initial bearing (azimuth) from coord1 to coord2.
    
    Args:
        coord1: Start coordinate (latitude, longitude) in degrees
        coord2: End coordinate (latitude, longitude) in degrees
    
    Returns:
        Initial bearing in degrees [0, 360)
    
    Example:
        >>> initial_bearing((0, 0), (0, 1))
        90.0
        >>> initial_bearing((0, 0), (1, 0))
        0.0
    """
    lat1, lng1 = _to_float(coord1[0]), _to_float(coord1[1])
    lat2, lng2 = _to_float(coord2[0]), _to_float(coord2[1])
    
    lat1_rad = lat1 * DEG_TO_RAD
    lat2_rad = lat2 * DEG_TO_RAD
    dlng_rad = (lng2 - lng1) * DEG_TO_RAD
    
    y = math.sin(dlng_rad) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlng_rad)
    
    bearing = math.atan2(y, x) * RAD_TO_DEG
    
    # Normalize to [0, 360)
    return (bearing + 360) % 360


def final_bearing(coord1: Coordinate, coord2: Coordinate) -> float:
    """
    Calculate the final bearing from coord1 to coord2.
    
    The final bearing is the bearing at the destination point,
    which differs from the initial bearing due to the curvature
    of the great circle path.
    
    Args:
        coord1: Start coordinate (latitude, longitude) in degrees
        coord2: End coordinate (latitude, longitude) in degrees
    
    Returns:
        Final bearing in degrees [0, 360)
    
    Example:
        >>> final_bearing((0, 0), (0, 1))
        90.0
    """
    # Final bearing is initial bearing from end to start, reversed
    bearing = initial_bearing(coord2, coord1)
    return (bearing + 180) % 360


def midpoint_coordinate(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    """
    Calculate the geographic midpoint between two coordinates.
    
    Args:
        coord1: First coordinate (latitude, longitude) in degrees
        coord2: Second coordinate (latitude, longitude) in degrees
    
    Returns:
        Midpoint coordinate (latitude, longitude)
    
    Example:
        >>> midpoint_coordinate((0, 0), (0, 10))
        (0.0, 5.0)
        >>> midpoint_coordinate((40, -74), (34, -118))
        (37.1..., -96.0...)
    """
    lat1, lng1 = _to_float(coord1[0]), _to_float(coord1[1])
    lat2, lng2 = _to_float(coord2[0]), _to_float(coord2[1])
    
    lat1_rad = lat1 * DEG_TO_RAD
    lat2_rad = lat2 * DEG_TO_RAD
    lng1_rad = lng1 * DEG_TO_RAD
    
    dlng_rad = (lng2 - lng1) * DEG_TO_RAD
    
    Bx = math.cos(lat2_rad) * math.cos(dlng_rad)
    By = math.cos(lat2_rad) * math.sin(dlng_rad)
    
    lat_mid_rad = math.atan2(
        math.sin(lat1_rad) + math.sin(lat2_rad),
        math.sqrt((math.cos(lat1_rad) + Bx) ** 2 + By ** 2)
    )
    
    lng_mid_rad = lng1_rad + math.atan2(By, math.cos(lat1_rad) + Bx)
    
    lat_mid = lat_mid_rad * RAD_TO_DEG
    lng_mid = lng_mid_rad * RAD_TO_DEG
    
    return (lat_mid, _normalize_longitude(lng_mid))


def destination_point(coord: Coordinate, bearing: float, distance_km: float) -> Coordinate:
    """
    Calculate destination point from start coordinate, bearing, and distance.
    
    Args:
        coord: Start coordinate (latitude, longitude) in degrees
        bearing: Bearing in degrees [0, 360)
        distance_km: Distance in kilometers
    
    Returns:
        Destination coordinate (latitude, longitude)
    
    Example:
        >>> destination_point((0, 0), 0, 111.19)  # 1 degree north
        (1.0, 0.0)
        >>> destination_point((0, 0), 90, 111.19)  # 1 degree east
        (0.0, 1.0)
    """
    lat1, lng1 = _to_float(coord[0]), _to_float(coord[1])
    bearing = _to_float(bearing)
    distance_km = _to_float(distance_km)
    
    lat1_rad = lat1 * DEG_TO_RAD
    lng1_rad = lng1 * DEG_TO_RAD
    bearing_rad = bearing * DEG_TO_RAD
    
    angular_dist = distance_km / EARTH_RADIUS_KM
    
    lat2_rad = math.asin(
        math.sin(lat1_rad) * math.cos(angular_dist) +
        math.cos(lat1_rad) * math.sin(angular_dist) * math.cos(bearing_rad)
    )
    
    lng2_rad = lng1_rad + math.atan2(
        math.sin(bearing_rad) * math.sin(angular_dist) * math.cos(lat1_rad),
        math.cos(angular_dist) - math.sin(lat1_rad) * math.sin(lat2_rad)
    )
    
    lat2 = lat2_rad * RAD_TO_DEG
    lng2 = lng2_rad * RAD_TO_DEG
    
    return (lat2, _normalize_longitude(lng2))


# ============================================================================
# Bounding Box and Polygon
# ============================================================================

def bounding_box(coord: Coordinate, radius_km: float) -> Tuple[Coordinate, Coordinate]:
    """
    Calculate bounding box (min/max coordinates) for a radius search.
    
    Args:
        coord: Center coordinate (latitude, longitude) in degrees
        radius_km: Search radius in kilometers
    
    Returns:
        Tuple of (min_coord, max_coord) where each is (lat, lng)
    
    Example:
        >>> bounding_box((39.9, 116.4), 10)
        ((39.81..., 116.29...), (39.99..., 116.51...))
    
    Note:
        This is an approximation using angular distance.
        For precise calculations, use destination_point for each corner.
    """
    lat, lng = _to_float(coord[0]), _to_float(coord[1])
    radius_km = _to_float(radius_km)
    
    # Angular distance in radians
    angular_dist = radius_km / EARTH_RADIUS_KM
    
    # Latitude bounds (simple - same angular distance)
    lat_min = lat - angular_dist * RAD_TO_DEG
    lat_max = lat + angular_dist * RAD_TO_DEG
    
    # Longitude bounds (depends on latitude)
    lat_rad = lat * DEG_TO_RAD
    if abs(lat_rad) < math.pi / 2 - 1e-6:  # Not at poles
        lng_offset = angular_dist / math.cos(lat_rad) * RAD_TO_DEG
    else:
        lng_offset = 180  # At poles, whole world
    
    lng_min = lng - lng_offset
    lng_max = lng + lng_offset
    
    # Clamp latitude to valid range
    lat_min = max(MIN_LATITUDE, lat_min)
    lat_max = min(MAX_LATITUDE, lat_max)
    
    # Normalize longitude
    lng_min = _normalize_longitude(lng_min)
    lng_max = _normalize_longitude(lng_max)
    
    return ((lat_min, lng_min), (lat_max, lng_max))


def point_in_polygon(point: Coordinate, polygon: List[Coordinate]) -> bool:
    """
    Check if a point is inside a geographic polygon.
    
    Uses the ray casting algorithm (counts polygon edge crossings).
    
    Args:
        point: Point coordinate (latitude, longitude) in degrees
        polygon: List of polygon vertex coordinates
    
    Returns:
        True if point is inside polygon
    
    Example:
        >>> # Simple square polygon around Beijing
        >>> polygon = [(39, 116), (40, 116), (40, 117), (39, 117)]
        >>> point_in_polygon((39.5, 116.5), polygon)
        True
        >>> point_in_polygon((38, 115), polygon)
        False
    
    Note:
        For polygons that cross the antimeridian (180/-180),
        ensure longitude values are consistently normalized.
    """
    lat, lng = _to_float(point[0]), _to_float(point[1])
    
    if len(polygon) < 3:
        return False
    
    n = len(polygon)
    inside = False
    
    j = n - 1
    for i in range(n):
        lat_i, lng_i = _to_float(polygon[i][0]), _to_float(polygon[i][1])
        lat_j, lng_j = _to_float(polygon[j][0]), _to_float(polygon[j][1])
        
        # Ray casting: count crossings
        if ((lng_i > lng) != (lng_j > lng)) and \
           (lat < (lat_j - lat_i) * (lng - lng_i) / (lng_j - lng_i) + lat_i):
            inside = not inside
        
        j = i
    
    return inside


def polygon_area_km2(polygon: List[Coordinate]) -> float:
    """
    Calculate area of a geographic polygon on Earth's surface.
    
    Args:
        polygon: List of polygon vertex coordinates [(lat, lng), ...]
    
    Returns:
        Area in square kilometers
    
    Example:
        >>> # Square of 1 degree at equator (~111km x 111km)
        >>> polygon = [(0, 0), (0, 1), (1, 1), (1, 0)]
        >>> polygon_area_km2(polygon)
        12364.0...
    
    Note:
        Uses spherical Earth approximation. For precise ellipsoidal
        calculations, consider specialized GIS libraries.
    """
    if len(polygon) < 3:
        return 0.0
    
    n = len(polygon)
    area_rad = 0.0
    
    for i in range(n):
        lat_i, lng_i = _to_float(polygon[i][0]) * DEG_TO_RAD, _to_float(polygon[i][1]) * DEG_TO_RAD
        lat_j, lng_j = _to_float(polygon[(i + 1) % n][0]) * DEG_TO_RAD, _to_float(polygon[(i + 1) % n][1]) * DEG_TO_RAD
        
        area_rad += (lng_j - lng_i) * (2 + math.sin(lat_i) + math.sin(lat_j))
    
    area_rad = abs(area_rad) * EARTH_RADIUS_KM ** 2 / 2
    return area_rad


# ============================================================================
# Interpolation and Path
# ============================================================================

def interpolate_path(coord1: Coordinate, coord2: Coordinate, num_points: int) -> List[Coordinate]:
    """
    Interpolate points along a great circle path between two coordinates.
    
    Args:
        coord1: Start coordinate (latitude, longitude) in degrees
        coord2: End coordinate (latitude, longitude) in degrees
        num_points: Number of intermediate points to generate
    
    Returns:
        List of interpolated coordinates including start and end
    
    Example:
        >>> interpolate_path((0, 0), (0, 10), 3)
        [(0.0, 0.0), (0.0, 5.0), (0.0, 10.0)]
    """
    if num_points < 2:
        return [coord1, coord2]
    
    lat1, lng1 = _to_float(coord1[0]), _to_float(coord1[1])
    lat2, lng2 = _to_float(coord2[0]), _to_float(coord2[1])
    
    lat1_rad = lat1 * DEG_TO_RAD
    lat2_rad = lat2 * DEG_TO_RAD
    lng1_rad = lng1 * DEG_TO_RAD
    lng2_rad = lng2 * DEG_TO_RAD
    
    # Calculate angular distance
    d = math.acos(
        math.sin(lat1_rad) * math.sin(lat2_rad) +
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.cos(lng2_rad - lng1_rad)
    )
    
    if d < 1e-10:
        # Points are essentially coincident
        return [coord1] * (num_points + 1)
    
    points = []
    for i in range(num_points + 1):
        f = i / num_points
        
        # Interpolate along great circle
        A = math.sin((1 - f) * d) / math.sin(d)
        B = math.sin(f * d) / math.sin(d)
        
        x = A * math.cos(lat1_rad) * math.cos(lng1_rad) + B * math.cos(lat2_rad) * math.cos(lng2_rad)
        y = A * math.cos(lat1_rad) * math.sin(lng1_rad) + B * math.cos(lat2_rad) * math.sin(lng2_rad)
        z = A * math.sin(lat1_rad) + B * math.sin(lat2_rad)
        
        lat_rad = math.atan2(z, math.sqrt(x ** 2 + y ** 2))
        lng_rad = math.atan2(y, x)
        
        lat = lat_rad * RAD_TO_DEG
        lng = lng_rad * RAD_TO_DEG
        
        points.append((lat, _normalize_longitude(lng)))
    
    return points


# ============================================================================
# Coordinate Utilities
# ============================================================================

def decimal_to_dms(coord: Coordinate) -> Dict[str, Dict[str, Any]]:
    """
    Convert decimal degrees to degrees-minutes-seconds (DMS) format.
    
    Args:
        coord: Coordinate (latitude, longitude) in decimal degrees
    
    Returns:
        Dictionary with 'lat' and 'lng' keys, each containing:
            - 'degrees': integer degrees
            - 'minutes': integer minutes
            - 'seconds': float seconds
            - 'direction': 'N'/'S' for lat, 'E'/'W' for lng
    
    Example:
        >>> decimal_to_dms((39.9042, -116.4074))
        {'lat': {'degrees': 39, 'minutes': 54, 'seconds': 15.12, 'direction': 'N'},
         'lng': {'degrees': 116, 'minutes': 24, 'seconds': 26.64, 'direction': 'W'}}
    """
    lat, lng = _to_float(coord[0]), _to_float(coord[1])
    
    def convert(value: float, is_lat: bool) -> Dict[str, Any]:
        abs_val = abs(value)
        degrees = int(abs_val)
        minutes_full = (abs_val - degrees) * 60
        minutes = int(minutes_full)
        seconds = (minutes_full - minutes) * 60
        
        if is_lat:
            direction = 'N' if value >= 0 else 'S'
        else:
            direction = 'E' if value >= 0 else 'W'
        
        return {
            'degrees': degrees,
            'minutes': minutes,
            'seconds': seconds,
            'direction': direction
        }
    
    return {
        'lat': convert(lat, True),
        'lng': convert(lng, False)
    }


def dms_to_decimal(dms_lat: Dict[str, Any], dms_lng: Dict[str, Any]) -> Coordinate:
    """
    Convert DMS (degrees-minutes-seconds) to decimal degrees.
    
    Args:
        dms_lat: Latitude DMS dict with 'degrees', 'minutes', 'seconds', 'direction'
        dms_lng: Longitude DMS dict with 'degrees', 'minutes', 'seconds', 'direction'
    
    Returns:
        Coordinate (latitude, longitude) in decimal degrees
    
    Example:
        >>> dms_to_decimal({'degrees': 39, 'minutes': 54, 'seconds': 15.12, 'direction': 'N'},
        ...                {'degrees': 116, 'minutes': 24, 'seconds': 26.64, 'direction': 'W'})
        (39.9042, -116.4074)
    """
    def convert(dms: Dict[str, Any]) -> float:
        degrees = _to_float(dms.get('degrees', 0))
        minutes = _to_float(dms.get('minutes', 0))
        seconds = _to_float(dms.get('seconds', 0))
        direction = dms.get('direction', 'N')
        
        decimal = degrees + minutes / 60 + seconds / 3600
        if direction in ('S', 'W'):
            decimal = -decimal
        
        return decimal
    
    lat = convert(dms_lat)
    lng = convert(dms_lng)
    
    return (lat, lng)


def coordinate_to_string(coord: Coordinate, format: str = 'decimal', precision: int = 4) -> str:
    """
    Convert coordinate to human-readable string.
    
    Args:
        coord: Coordinate (latitude, longitude) in degrees
        format: Output format ('decimal', 'dms', 'dm')
        precision: Decimal precision for decimal format
    
    Returns:
        String representation of coordinate
    
    Example:
        >>> coordinate_to_string((39.9042, 116.4074))
        '39.9042°N, 116.4074°E'
        >>> coordinate_to_string((39.9042, 116.4074), format='dms')
        '39°54\'15"N, 116°24\'26"E'
    """
    lat, lng = _to_float(coord[0]), _to_float(coord[1])
    
    if format == 'decimal':
        lat_dir = 'N' if lat >= 0 else 'S'
        lng_dir = 'E' if lng >= 0 else 'W'
        return f"{abs(lat):.{precision}f}°{lat_dir}, {abs(lng):.{precision}f}°{lng_dir}"
    
    elif format == 'dms':
        dms = decimal_to_dms(coord)
        lat_str = f"{dms['lat']['degrees']}°{dms['lat']['minutes']}'{dms['lat']['seconds']:.1f}\"{dms['lat']['direction']}"
        lng_str = f"{dms['lng']['degrees']}°{dms['lng']['minutes']}'{dms['lng']['seconds']:.1f}\"{dms['lng']['direction']}"
        return f"{lat_str}, {lng_str}"
    
    elif format == 'dm':
        # Degrees and minutes only
        lat_dir = 'N' if lat >= 0 else 'S'
        lng_dir = 'E' if lng >= 0 else 'W'
        
        lat_deg = int(abs(lat))
        lat_min = (abs(lat) - lat_deg) * 60
        lng_deg = int(abs(lng))
        lng_min = (abs(lng) - lng_deg) * 60
        
        return f"{lat_deg}°{lat_min:.2f}'{lat_dir}, {lng_deg}°{lng_min:.2f}'{lng_dir}"
    
    else:
        raise ValueError(f"Unknown format: {format}")


# ============================================================================
# Distance Unit Conversions
# ============================================================================

def km_to_miles(km: float) -> float:
    """Convert kilometers to miles."""
    return _to_float(km) * KM_TO_MILES


def km_to_nautical(km: float) -> float:
    """Convert kilometers to nautical miles."""
    return _to_float(km) * KM_TO_NAUTICAL


def km_to_m(km: float) -> float:
    """Convert kilometers to meters."""
    return _to_float(km) * 1000


def miles_to_km(miles: float) -> float:
    """Convert miles to kilometers."""
    return _to_float(miles) * MILES_TO_KM


def nautical_to_km(nautical: float) -> float:
    """Convert nautical miles to kilometers."""
    return _to_float(nautical) * NAUTICAL_TO_KM


def m_to_km(m: float) -> float:
    """Convert meters to kilometers."""
    return _to_float(m) * M_TO_KM


def convert_distance(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert distance between units.
    
    Args:
        value: Distance value
        from_unit: Source unit ('km', 'm', 'miles', 'nautical')
        to_unit: Target unit ('km', 'm', 'miles', 'nautical')
    
    Returns:
        Converted distance
    
    Example:
        >>> convert_distance(100, 'km', 'miles')
        62.1371
        >>> convert_distance(100, 'miles', 'km')
        160.9344
    """
    value = _to_float(value)
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    units = ['km', 'm', 'miles', 'nautical']
    if from_unit not in units or to_unit not in units:
        raise ValueError(f"Unknown unit. Use: {units}")
    
    # Convert to km first
    if from_unit == 'km':
        km_value = value
    elif from_unit == 'm':
        km_value = value * M_TO_KM
    elif from_unit == 'miles':
        km_value = value * MILES_TO_KM
    elif from_unit == 'nautical':
        km_value = value * NAUTICAL_TO_KM
    
    # Convert from km to target
    if to_unit == 'km':
        return km_value
    elif to_unit == 'm':
        return km_value * 1000
    elif to_unit == 'miles':
        return km_value * KM_TO_MILES
    elif to_unit == 'nautical':
        return km_value * KM_TO_NAUTICAL


# ============================================================================
# Special Calculations
# ============================================================================

def nearest_point_on_path(point: Coordinate, path: List[Coordinate]) -> Tuple[Coordinate, float, int]:
    """
    Find the nearest point on a path to a given point.
    
    Args:
        point: The point to find nearest location from
        path: List of coordinates forming a path
    
    Returns:
        Tuple of (nearest_point, distance_km, segment_index)
    
    Example:
        >>> path = [(0, 0), (0, 10)]
        >>> nearest_point_on_path((1, 5), path)
        ((0.0, 5.0), 111.19..., 0)
    """
    if len(path) < 2:
        if len(path) == 1:
            return (path[0], haversine_distance(point, path[0]), 0)
        raise ValueError("Path must have at least 1 point")
    
    min_distance = float('inf')
    nearest_point = None
    segment_index = 0
    
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        
        # Find nearest point on this segment
        # Project point onto great circle arc
        nearest = _nearest_on_segment(point, start, end)
        dist = haversine_distance(point, nearest)
        
        if dist < min_distance:
            min_distance = dist
            nearest_point = nearest
            segment_index = i
    
    return (nearest_point, min_distance, segment_index)


def _nearest_on_segment(point: Coordinate, start: Coordinate, end: Coordinate) -> Coordinate:
    """Find nearest point on a great circle segment."""
    # Calculate bearing from start to end
    bearing_start_end = initial_bearing(start, end)
    
    # Calculate bearing from start to point
    bearing_start_point = initial_bearing(start, point)
    
    # Calculate cross-track distance
    dist_start_point = haversine_distance(start, point)
    
    # Angular distance
    dxt = math.asin(
        math.sin(dist_start_point / EARTH_RADIUS_KM) *
        math.sin((bearing_start_point - bearing_start_end) * DEG_TO_RAD)
    )
    
    # Along-track distance
    dat = math.acos(
        math.cos(dist_start_point / EARTH_RADIUS_KM) / math.cos(dxt)
    ) * EARTH_RADIUS_KM
    
    # Distance from start along the path
    dist_start_end = haversine_distance(start, end)
    
    # Check if nearest point is within segment
    if dat < 0:
        return start
    elif dat > dist_start_end:
        return end
    else:
        return destination_point(start, bearing_start_end, dat)


def total_path_distance(path: List[Coordinate], unit: str = 'km') -> float:
    """
    Calculate total distance along a path.
    
    Args:
        path: List of coordinates [(lat, lng), ...]
        unit: Distance unit ('km', 'm', 'miles', 'nautical')
    
    Returns:
        Total distance in specified unit
    
    Example:
        >>> total_path_distance([(0, 0), (0, 1), (0, 2)])
        222.38...
    """
    if len(path) < 2:
        return 0.0
    
    total = 0.0
    for i in range(len(path) - 1):
        total += haversine_distance(path[i], path[i + 1], 'km')
    
    return convert_distance(total, 'km', unit)


# ============================================================================
# Batch Operations
# ============================================================================

def find_nearest(point: Coordinate, candidates: List[Coordinate], unit: str = 'km') -> Tuple[int, float, Coordinate]:
    """
    Find the nearest candidate to a point.
    
    Args:
        point: Reference point (lat, lng)
        candidates: List of candidate coordinates
        unit: Distance unit
    
    Returns:
        Tuple of (index, distance, nearest_coordinate)
    
    Example:
        >>> candidates = [(40, 116), (35, 117), (30, 120)]
        >>> find_nearest((39, 116), candidates)
        (0, 111.19..., (40, 116))
    """
    if not candidates:
        raise ValueError("Candidates list is empty")
    
    min_dist = float('inf')
    min_idx = 0
    
    for i, candidate in enumerate(candidates):
        dist = haversine_distance(point, candidate, unit)
        if dist < min_dist:
            min_dist = dist
            min_idx = i
    
    return (min_idx, min_dist, candidates[min_idx])


def distances_to_all(point: Coordinate, targets: List[Coordinate], unit: str = 'km') -> List[float]:
    """
    Calculate distances from a point to all targets.
    
    Args:
        point: Reference point (lat, lng)
        targets: List of target coordinates
        unit: Distance unit
    
    Returns:
        List of distances
    
    Example:
        >>> distances_to_all((0, 0), [(0, 1), (1, 0)])
        [111.19..., 111.19...]
    """
    return [haversine_distance(point, target, unit) for target in targets]


def within_radius(point: Coordinate, candidates: List[Coordinate], radius_km: float, unit: str = 'km') -> List[Tuple[int, float, Coordinate]]:
    """
    Find all candidates within a radius of a point.
    
    Args:
        point: Center point (lat, lng)
        candidates: List of candidate coordinates
        radius_km: Search radius in kilometers
        unit: Distance unit for returned distances
    
    Returns:
        List of tuples (index, distance, coordinate) for points within radius
    
    Example:
        >>> candidates = [(0, 1), (0, 2), (0, 3)]
        >>> within_radius((0, 0), candidates, 200)
        [(0, 111.19..., (0, 1)), (1, 222.38..., (0, 2))]
    """
    results = []
    for i, candidate in enumerate(candidates):
        dist = haversine_distance(point, candidate, unit)
        if dist <= radius_km:
            results.append((i, dist, candidate))
    
    return results


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Constants
    'EARTH_RADIUS_KM', 'EARTH_RADIUS_M', 'EARTH_RADIUS_MILES', 'EARTH_RADIUS_NAUTICAL',
    'WGS84_SEMI_MAJOR', 'WGS84_SEMI_MINOR', 'WGS84_FLATTENING',
    'KM_TO_MILES', 'KM_TO_NAUTICAL', 'MILES_TO_KM', 'NAUTICAL_TO_KM',
    'MAX_LATITUDE', 'MIN_LATITUDE', 'MAX_LONGITUDE', 'MIN_LONGITUDE',
    'DEG_TO_RAD', 'RAD_TO_DEG',
    
    # Type aliases
    'Coordinate', 'Coordinate3D',
    
    # Validation and normalization
    'is_valid_coordinate', 'normalize_coordinate',
    
    # Distance calculations
    'haversine_distance', 'vincenty_distance', 'distance',
    
    # Bearing and direction
    'initial_bearing', 'final_bearing',
    
    # Coordinate operations
    'midpoint_coordinate', 'destination_point',
    
    # Polygon operations
    'bounding_box', 'point_in_polygon', 'polygon_area_km2',
    
    # Path operations
    'interpolate_path', 'nearest_point_on_path', 'total_path_distance',
    
    # Coordinate format conversions
    'decimal_to_dms', 'dms_to_decimal', 'coordinate_to_string',
    
    # Distance unit conversions
    'km_to_miles', 'km_to_nautical', 'km_to_m',
    'miles_to_km', 'nautical_to_km', 'm_to_km', 'convert_distance',
    
    # Batch operations
    'find_nearest', 'distances_to_all', 'within_radius',
]


if __name__ == '__main__':
    # Quick demo
    print("AllToolkit Geographic Distance Utils Demo")
    print("=" * 50)
    
    # Beijing to Shanghai
    beijing = (39.9042, 116.4074)
    shanghai = (31.2304, 121.4737)
    
    print(f"Beijing to Shanghai:")
    print(f"  Haversine: {haversine_distance(beijing, shanghai):.2f} km")
    print(f"  Vincenty:  {vincenty_distance(beijing, shanghai):.2f} km")
    print(f"  Miles:     {convert_distance(haversine_distance(beijing, shanghai), 'km', 'miles'):.2f}")
    
    # Bearing
    print(f"  Initial bearing: {initial_bearing(beijing, shanghai):.2f}°")
    
    # Midpoint
    mid = midpoint_coordinate(beijing, shanghai)
    print(f"  Midpoint: {coordinate_to_string(mid)}")
    
    # Destination
    dest = destination_point(beijing, 90, 100)
    print(f"  100km east from Beijing: {coordinate_to_string(dest)}")
    
    # Bounding box
    bbox = bounding_box(beijing, 50)
    print(f"  50km bounding box: {coordinate_to_string(bbox[0])} to {coordinate_to_string(bbox[1])}")
    
    # DMS format
    print(f"\nBeijing in DMS: {coordinate_to_string(beijing, format='dms')}")
    
    print("\nFor full documentation, see README.md")