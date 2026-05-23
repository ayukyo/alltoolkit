#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Orbital Mechanics Utilities Module
================================================
A comprehensive orbital mechanics calculation utility module for Python with zero external dependencies.

Features:
    - Kepler's laws calculations
    - Orbital period calculations
    - Orbital velocity calculations
    - Escape velocity calculations
    - Satellite orbit parameters
    - Apogee/Perigee calculations
    - Orbital energy calculations
    - Semi-major axis and eccentricity
    - Hohmann transfer orbit calculations
    - Launch window calculations
    - Orbital inclination effects
    - Geostationary orbit helpers
    - Two-body problem solutions

Author: AllToolkit Contributors
License: MIT
"""

import math
from typing import Any, Dict, List, Optional, Tuple, Union


# ============================================================================
# Physical Constants
# ============================================================================

# Gravitational constant (m³/(kg·s²))
G = 6.67430e-11

# Standard gravitational parameters (GM) in m³/s²
GM_SUN = 1.32712440018e20      # Sun
GM_EARTH = 3.986004418e14      # Earth
GM_MOON = 4.9048695e12         # Moon
GM_MARS = 4.282837e13          # Mars
GM_JUPITER = 1.26686534e17     # Jupiter
GM_VENUS = 3.24859e14          # Venus
GM_MERCURY = 2.2032e13         # Mercury
GM_SATURN = 3.7931187e16       # Saturn

# Body radii in meters (mean equatorial radius)
R_SUN = 6.96e8                 # Sun
R_EARTH = 6.371e6              # Earth
R_MOON = 1.7374e6              # Moon
R_MARS = 3.3895e6              # Mars
R_JUPITER = 6.9911e7           # Jupiter
R_VENUS = 6.0518e6             # Venus
R_MERCURY = 2.4397e6           # Mercury
R_SATURN = 5.8232e7            # Saturn

# Standard gravity (m/s²) - Earth surface
G0 = 9.80665

# Astronomical Unit (m)
AU = 1.495978707e11

# Speed of light (m/s)
C = 299792458


# ============================================================================
# Utility Functions
# ============================================================================

def _to_float(value: Any) -> float:
    """Convert value to float safely."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _is_positive(value: Any) -> bool:
    """Check if value is a positive number."""
    return isinstance(value, (int, float)) and value > 0


# ============================================================================
# Kepler's Laws
# ============================================================================

def kepler_third_law_period(semi_major_axis: float, gm: float = GM_EARTH) -> float:
    """
    Calculate orbital period using Kepler's third law.
    
    T² = 4π²a³ / GM
    
    Args:
        semi_major_axis: Semi-major axis in meters
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Orbital period in seconds
    
    Example:
        >>> # Period of a satellite at 400 km altitude
        >>> period = kepler_third_law_period(R_EARTH + 400000)
        >>> period / 60  # Convert to minutes
        92.52...
    """
    a = _to_float(semi_major_axis)
    gm_val = _to_float(gm)
    
    if a <= 0 or gm_val <= 0:
        return 0.0
    
    return 2 * math.pi * math.sqrt(a ** 3 / gm_val)


def kepler_third_lax_axis(period: float, gm: float = GM_EARTH) -> float:
    """
    Calculate semi-major axis from orbital period using Kepler's third law.
    
    a³ = GM × T² / 4π²
    
    Args:
        period: Orbital period in seconds
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Semi-major axis in meters
    
    Example:
        >>> # Semi-major axis for a 24-hour orbit (geostationary)
        >>> axis = kepler_third_lax_axis(24 * 3600)
        >>> axis / 1000  # Convert to km
        42164.17...
    """
    t = _to_float(period)
    gm_val = _to_float(gm)
    
    if t <= 0 or gm_val <= 0:
        return 0.0
    
    return (gm_val * t ** 2 / (4 * math.pi ** 2)) ** (1/3)


def kepler_first_law_velocity(distance: float, semi_major_axis: float, gm: float = GM_EARTH) -> float:
    """
    Calculate orbital velocity at a given distance using vis-viva equation (derived from Kepler's laws).
    
    v² = GM(2/r - 1/a)
    
    Args:
        distance: Current distance from center in meters
        semi_major_axis: Semi-major axis in meters
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Orbital velocity in m/s
    
    Example:
        >>> # Velocity at perigee of elliptical orbit
        >>> v = kepler_first_law_velocity(R_EARTH + 200000, R_EARTH + 400000)
    """
    r = _to_float(distance)
    a = _to_float(semi_major_axis)
    gm_val = _to_float(gm)
    
    if r <= 0 or a <= 0 or gm_val <= 0:
        return 0.0
    
    # Vis-viva equation: v² = GM(2/r - 1/a)
    v_squared = gm_val * (2 / r - 1 / a)
    
    if v_squared <= 0:
        return 0.0
    
    return math.sqrt(v_squared)


def kepler_second_law_area_velocity(semi_major_axis: float, gm: float = GM_EARTH) -> float:
    """
    Calculate specific angular momentum (area velocity) using Kepler's second law.
    
    For circular orbit: h = r × v = sqrt(GM × a)
    
    Args:
        semi_major_axis: Semi-major axis in meters
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Specific angular momentum in m²/s
    
    Example:
        >>> h = kepler_second_law_area_velocity(R_EARTH + 400000)
    """
    a = _to_float(semi_major_axis)
    gm_val = _to_float(gm)
    
    if a <= 0 or gm_val <= 0:
        return 0.0
    
    return math.sqrt(gm_val * a)


# ============================================================================
# Basic Orbital Parameters
# ============================================================================

def orbital_velocity_circular(altitude: float, body_radius: float = R_EARTH, gm: float = GM_EARTH) -> float:
    """
    Calculate circular orbital velocity at a given altitude.
    
    v = sqrt(GM / r)
    
    Args:
        altitude: Altitude above surface in meters
        body_radius: Central body radius (default: Earth)
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Orbital velocity in m/s
    
    Example:
        >>> # Velocity at 400 km altitude (ISS orbit)
        >>> v = orbital_velocity_circular(400000)
        >>> v
        7672.0...
    """
    h = _to_float(altitude)
    r_body = _to_float(body_radius)
    gm_val = _to_float(gm)
    
    if h < 0 or r_body <= 0 or gm_val <= 0:
        return 0.0
    
    r = r_body + h  # Total distance from center
    
    return math.sqrt(gm_val / r)


def orbital_period_circular(altitude: float, body_radius: float = R_EARTH, gm: float = GM_EARTH) -> float:
    """
    Calculate circular orbital period at a given altitude.
    
    Args:
        altitude: Altitude above surface in meters
        body_radius: Central body radius (default: Earth)
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Orbital period in seconds
    
    Example:
        >>> # Period at 400 km altitude
        >>> period = orbital_period_circular(400000)
        >>> period / 60  # Minutes
        92.52...
    """
    h = _to_float(altitude)
    r_body = _to_float(body_radius)
    
    if h < 0 or r_body <= 0:
        return 0.0
    
    semi_major_axis = r_body + h
    return kepler_third_law_period(semi_major_axis, gm)


def escape_velocity(altitude: float = 0, body_radius: float = R_EARTH, gm: float = GM_EARTH) -> float:
    """
    Calculate escape velocity at a given altitude.
    
    v_esc = sqrt(2GM / r)
    
    Args:
        altitude: Altitude above surface in meters (default: 0)
        body_radius: Central body radius (default: Earth)
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Escape velocity in m/s
    
    Example:
        >>> # Earth's surface escape velocity
        >>> v_esc = escape_velocity()
        >>> v_esc
        11186.0...
    """
    h = _to_float(altitude)
    r_body = _to_float(body_radius)
    gm_val = _to_float(gm)
    
    if h < 0 or r_body <= 0 or gm_val <= 0:
        return 0.0
    
    r = r_body + h
    
    return math.sqrt(2 * gm_val / r)


def surface_gravity(body_radius: float = R_EARTH, gm: float = GM_EARTH) -> float:
    """
    Calculate surface gravity of a body.
    
    g = GM / r²
    
    Args:
        body_radius: Body radius in meters (default: Earth)
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Surface gravity in m/s²
    
    Example:
        >>> g = surface_gravity()
        >>> g
        9.81...
    """
    r = _to_float(body_radius)
    gm_val = _to_float(gm)
    
    if r <= 0 or gm_val <= 0:
        return 0.0
    
    return gm_val / r ** 2


# ============================================================================
# Elliptical Orbit Parameters
# ============================================================================

def calculate_eccentricity(apogee: float, perigee: float, body_radius: float = R_EARTH) -> float:
    """
    Calculate orbital eccentricity from apogee and perigee.
    
    e = (r_a - r_p) / (r_a + r_p)
    
    Args:
        apogee: Apogee altitude in meters
        perigee: Perigee altitude in meters
        body_radius: Central body radius (default: Earth)
    
    Returns:
        Eccentricity (0 for circular, <1 for elliptical)
    
    Example:
        >>> # GTO orbit (apogee 35786 km, perigee 200 km)
        >>> e = calculate_eccentricity(35786000, 200000)
        >>> e
        0.72...
    """
    r_a = _to_float(body_radius) + _to_float(apogee)
    r_p = _to_float(body_radius) + _to_float(perigee)
    
    if r_a <= 0 or r_p <= 0:
        return 0.0
    
    return (r_a - r_p) / (r_a + r_p)


def calculate_semi_major_axis(apogee: float, perigee: float, body_radius: float = R_EARTH) -> float:
    """
    Calculate semi-major axis from apogee and perigee.
    
    a = (r_a + r_p) / 2
    
    Args:
        apogee: Apogee altitude in meters
        perigee: Perigee altitude in meters
        body_radius: Central body radius (default: Earth)
    
    Returns:
        Semi-major axis in meters
    
    Example:
        >>> a = calculate_semi_major_axis(35786000, 200000)
    """
    r_a = _to_float(body_radius) + _to_float(apogee)
    r_p = _to_float(body_radius) + _to_float(perigee)
    
    if r_a <= 0 or r_p <= 0:
        return 0.0
    
    return (r_a + r_p) / 2


def calculate_semi_minor_axis(semi_major_axis: float, eccentricity: float) -> float:
    """
    Calculate semi-minor axis from semi-major axis and eccentricity.
    
    b = a × sqrt(1 - e²)
    
    Args:
        semi_major_axis: Semi-major axis in meters
        eccentricity: Orbital eccentricity
    
    Returns:
        Semi-minor axis in meters
    
    Example:
        >>> b = calculate_semi_minor_axis(42164000, 0.72)
    """
    a = _to_float(semi_major_axis)
    e = _to_float(eccentricity)
    
    if a <= 0 or e < 0 or e >= 1:
        return 0.0
    
    return a * math.sqrt(1 - e ** 2)


def velocity_at_apogee(apogee: float, perigee: float, body_radius: float = R_EARTH, gm: float = GM_EARTH) -> float:
    """
    Calculate orbital velocity at apogee.
    
    Args:
        apogee: Apogee altitude in meters
        perigee: Perigee altitude in meters
        body_radius: Central body radius (default: Earth)
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Velocity at apogee in m/s
    
    Example:
        >>> # Velocity at GTO apogee
        >>> v = velocity_at_apogee(35786000, 200000)
    """
    r_a = _to_float(body_radius) + _to_float(apogee)
    a = calculate_semi_major_axis(apogee, perigee, body_radius)
    return kepler_first_law_velocity(r_a, a, gm)


def velocity_at_perigee(apogee: float, perigee: float, body_radius: float = R_EARTH, gm: float = GM_EARTH) -> float:
    """
    Calculate orbital velocity at perigee.
    
    Args:
        apogee: Apogee altitude in meters
        perigee: Perigee altitude in meters
        body_radius: Central body radius (default: Earth)
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Velocity at perigee in m/s
    
    Example:
        >>> # Velocity at GTO perigee
        >>> v = velocity_at_perigee(35786000, 200000)
    """
    r_p = _to_float(body_radius) + _to_float(perigee)
    a = calculate_semi_major_axis(apogee, perigee, body_radius)
    return kepler_first_law_velocity(r_p, a, gm)


def orbital_period_elliptical(apogee: float, perigee: float, body_radius: float = R_EARTH, gm: float = GM_EARTH) -> float:
    """
    Calculate orbital period for an elliptical orbit.
    
    Args:
        apogee: Apogee altitude in meters
        perigee: Perigee altitude in meters
        body_radius: Central body radius (default: Earth)
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Orbital period in seconds
    
    Example:
        >>> # Period of GTO orbit
        >>> period = orbital_period_elliptical(35786000, 200000)
        >>> period / 3600  # Hours
        10.5...
    """
    a = calculate_semi_major_axis(apogee, perigee, body_radius)
    return kepler_third_law_period(a, gm)


# ============================================================================
# Orbital Energy
# ============================================================================

def specific_orbital_energy(semi_major_axis: float, gm: float = GM_EARTH) -> float:
    """
    Calculate specific orbital energy (energy per unit mass).
    
    ε = -GM / 2a
    
    Args:
        semi_major_axis: Semi-major axis in meters
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Specific orbital energy in J/kg (negative for bound orbits)
    
    Example:
        >>> energy = specific_orbital_energy(R_EARTH + 400000)
    """
    a = _to_float(semi_major_axis)
    gm_val = _to_float(gm)
    
    if a <= 0 or gm_val <= 0:
        return 0.0
    
    return -gm_val / (2 * a)


def specific_kinetic_energy(velocity: float) -> float:
    """
    Calculate specific kinetic energy (kinetic energy per unit mass).
    
    KE = v² / 2
    
    Args:
        velocity: Velocity in m/s
    
    Returns:
        Specific kinetic energy in J/kg
    
    Example:
        >>> ke = specific_kinetic_energy(7672)
    """
    v = _to_float(velocity)
    return v ** 2 / 2


def specific_potential_energy(distance: float, gm: float = GM_EARTH) -> float:
    """
    Calculate specific potential energy (potential energy per unit mass).
    
    PE = -GM / r
    
    Args:
        distance: Distance from center in meters
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Specific potential energy in J/kg (negative)
    
    Example:
        >>> pe = specific_potential_energy(R_EARTH + 400000)
    """
    r = _to_float(distance)
    gm_val = _to_float(gm)
    
    if r <= 0 or gm_val <= 0:
        return 0.0
    
    return -gm_val / r


def total_specific_energy(distance: float, velocity: float, gm: float = GM_EARTH) -> float:
    """
    Calculate total specific mechanical energy.
    
    ε = v²/2 - GM/r
    
    Args:
        distance: Distance from center in meters
        velocity: Velocity in m/s
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Total specific energy in J/kg
    
    Example:
        >>> # Energy at circular orbit velocity
        >>> r = R_EARTH + 400000
        >>> v = orbital_velocity_circular(400000)
        >>> energy = total_specific_energy(r, v)
    """
    return specific_kinetic_energy(velocity) + specific_potential_energy(distance, gm)


# ============================================================================
# Hohmann Transfer Orbit
# ============================================================================

def hohmann_transfer_time(r1: float, r2: float, gm: float = GM_EARTH) -> float:
    """
    Calculate time for Hohmann transfer between two circular orbits.
    
    T_transfer = π × sqrt((r1 + r2)³ / 8GM)
    
    Args:
        r1: Initial orbit radius in meters
        r2: Final orbit radius in meters
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Transfer time in seconds (half period of transfer orbit)
    
    Example:
        >>> # Transfer time from LEO to GEO
        >>> t = hohmann_transfer_time(R_EARTH + 400000, R_EARTH + 35786000)
        >>> t / 3600  # Hours
        5.25...
    """
    r1_val = _to_float(r1)
    r2_val = _to_float(r2)
    gm_val = _to_float(gm)
    
    if r1_val <= 0 or r2_val <= 0 or gm_val <= 0:
        return 0.0
    
    # Semi-major axis of transfer ellipse
    a_transfer = (r1_val + r2_val) / 2
    
    # Half the orbital period of the transfer ellipse
    return math.pi * math.sqrt(a_transfer ** 3 / gm_val)


def hohmann_transfer_velocity(r1: float, r2: float, gm: float = GM_EARTH) -> Tuple[float, float, float]:
    """
    Calculate velocities for Hohmann transfer.
    
    Returns the three key velocities:
    - v1: Initial circular orbit velocity
    - v_transfer1: Transfer orbit velocity at departure
    - v_transfer2: Transfer orbit velocity at arrival
    
    Args:
        r1: Initial orbit radius in meters
        r2: Final orbit radius in meters
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Tuple of (v1, v_transfer1, v_transfer2) in m/s
    
    Example:
        >>> v1, vt1, vt2 = hohmann_transfer_velocity(R_EARTH + 400000, R_EARTH + 35786000)
    """
    r1_val = _to_float(r1)
    r2_val = _to_float(r2)
    gm_val = _to_float(gm)
    
    if r1_val <= 0 or r2_val <= 0 or gm_val <= 0:
        return (0.0, 0.0, 0.0)
    
    a_transfer = (r1_val + r2_val) / 2
    
    # Initial circular orbit velocity
    v1 = math.sqrt(gm_val / r1_val)
    
    # Transfer orbit velocity at perigee (r1)
    v_transfer1 = math.sqrt(gm_val * (2 / r1_val - 1 / a_transfer))
    
    # Transfer orbit velocity at apogee (r2)
    v_transfer2 = math.sqrt(gm_val * (2 / r2_val - 1 / a_transfer))
    
    return (v1, v_transfer1, v_transfer2)


def hohmann_delta_v(r1: float, r2: float, gm: float = GM_EARTH) -> Tuple[float, float, float]:
    """
    Calculate delta-V requirements for Hohmann transfer.
    
    Args:
        r1: Initial orbit radius in meters
        r2: Final orbit radius in meters
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Tuple of (delta_v1, delta_v2, total_delta_v) in m/s
        - delta_v1: First burn (departure)
        - delta_v2: Second burn (arrival)
        - total_delta_v: Total delta-V
    
    Example:
        >>> # Delta-V from LEO to GEO
        >>> dv1, dv2, total = hohmann_delta_v(R_EARTH + 400000, R_EARTH + 35786000)
        >>> total
        3893.0...
    """
    v1, v_transfer1, v_transfer2 = hohmann_transfer_velocity(r1, r2, gm)
    
    # Final circular orbit velocity
    v2 = math.sqrt(gm / r2)
    
    # Delta-V for first burn (acceleration to transfer orbit)
    delta_v1 = v_transfer1 - v1
    
    # Delta-V for second burn (acceleration to final orbit)
    delta_v2 = v2 - v_transfer2
    
    total_delta_v = abs(delta_v1) + abs(delta_v2)
    
    return (delta_v1, delta_v2, total_delta_v)


# ============================================================================
# Geostationary Orbit
# ============================================================================

def geostationary_altitude(body_radius: float = R_EARTH, gm: float = GM_EARTH, rotation_period: float = 86164.1) -> float:
    """
    Calculate geostationary orbit altitude for a body.
    
    Args:
        body_radius: Body radius in meters (default: Earth)
        gm: Standard gravitational parameter (default: Earth)
        rotation_period: Sidereal rotation period in seconds (default: Earth ~23h56m)
    
    Returns:
        Altitude above surface in meters
    
    Example:
        >>> alt = geostationary_altitude()
        >>> alt / 1000  # km
        35786.0...
    """
    r_body = _to_float(body_radius)
    gm_val = _to_float(gm)
    period = _to_float(rotation_period)
    
    if r_body <= 0 or gm_val <= 0 or period <= 0:
        return 0.0
    
    # Radius where orbital period equals rotation period
    orbital_radius = kepler_third_lax_axis(period, gm_val)
    
    return orbital_radius - r_body


def geostationary_velocity(body_radius: float = R_EARTH, gm: float = GM_EARTH) -> float:
    """
    Calculate orbital velocity in geostationary orbit.
    
    Args:
        body_radius: Body radius in meters (default: Earth)
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Orbital velocity in m/s
    
    Example:
        >>> v = geostationary_velocity()
        >>> v
        3074.7...
    """
    alt = geostationary_altitude(body_radius, gm)
    return orbital_velocity_circular(alt, body_radius, gm)


# ============================================================================
# Launch Calculations
# ============================================================================

def launch_velocity_to_orbit(altitude: float, body_radius: float = R_EARTH, gm: float = GM_EARTH) -> float:
    """
    Calculate minimum launch velocity to reach a given orbit altitude (ignoring atmosphere).
    
    This is the velocity needed if launching directly to orbit altitude.
    
    Args:
        altitude: Target altitude in meters
        body_radius: Body radius (default: Earth)
        gm: Standard gravitational parameter (default: Earth)
    
    Returns:
        Required launch velocity in m/s
    
    Example:
        >>> v = launch_velocity_to_orbit(400000)
    """
    h = _to_float(altitude)
    r_body = _to_float(body_radius)
    gm_val = _to_float(gm)
    
    if h < 0 or r_body <= 0 or gm_val <= 0:
        return 0.0
    
    r_target = r_body + h
    
    # Need enough energy to reach orbit and circularize
    # Minimum: sqrt(GM × (2/r_body - 1/r_target))
    v_launch = math.sqrt(gm_val * (2 / r_body - 1 / r_target))
    
    return v_launch


def gravity_loss_estimate(velocity: float, flight_time: float, g: float = G0) -> float:
    """
    Estimate gravity loss during vertical ascent.
    
    Gravity loss = g × t (for vertical ascent)
    
    Args:
        velocity: Burnout velocity in m/s
        flight_time: Time of powered flight in seconds
        g: Surface gravity (default: Earth)
    
    Returns:
        Estimated gravity loss in m/s
    
    Example:
        >>> loss = gravity_loss_estimate(9000, 180)
    """
    t = _to_float(flight_time)
    g_val = _to_float(g)
    
    return g_val * t


def launch_window_azimuth(inclination: float, latitude: float) -> float:
    """
    Calculate required launch azimuth for a given orbital inclination from a launch site.
    
    sin(azimuth) = sin(inclination) / cos(latitude)
    
    Args:
        inclination: Target orbit inclination in degrees
        latitude: Launch site latitude in degrees
    
    Returns:
        Launch azimuth in degrees (0° = North, 90° = East)
    
    Example:
        >>> # Launch azimuth for ISS orbit (51.6°) from Kennedy (28.5°N)
        >>> azimuth = launch_window_azimuth(51.6, 28.5)
    """
    inc = math.radians(_to_float(inclination))
    lat = math.radians(_to_float(latitude))
    
    if abs(math.cos(lat)) < 1e-10:
        return 0.0  # Can't launch from poles
    
    sin_azimuth = math.sin(inc) / math.cos(lat)
    
    # Clamp to valid range
    sin_azimuth = max(-1, min(1, sin_azimuth))
    
    azimuth = math.degrees(math.asin(sin_azimuth))
    
    return azimuth


def minimum_inclination_from_latitude(latitude: float) -> float:
    """
    Calculate minimum achievable inclination from a launch site.
    
    Minimum inclination = latitude (launching due east)
    
    Args:
        latitude: Launch site latitude in degrees
    
    Returns:
        Minimum achievable inclination in degrees
    
    Example:
        >>> min_inc = minimum_inclination_from_latitude(28.5)  # Kennedy
    """
    return abs(_to_float(latitude))


# ============================================================================
# Orbital Mechanics Utilities
# ============================================================================

def orbital_altitude_range(semi_major_axis: float, eccentricity: float, body_radius: float = R_EARTH) -> Tuple[float, float]:
    """
    Calculate apogee and perigee altitudes from semi-major axis and eccentricity.
    
    Args:
        semi_major_axis: Semi-major axis in meters
        eccentricity: Orbital eccentricity
        body_radius: Central body radius (default: Earth)
    
    Returns:
        Tuple of (perigee_altitude, apogee_altitude) in meters
    
    Example:
        >>> perigee, apogee = orbital_altitude_range(42164000, 0.72)
    """
    a = _to_float(semi_major_axis)
    e = _to_float(eccentricity)
    r_body = _to_float(body_radius)
    
    if a <= 0 or e < 0 or e >= 1 or r_body <= 0:
        return (0.0, 0.0)
    
    r_perigee = a * (1 - e)
    r_apogee = a * (1 + e)
    
    return (r_perigee - r_body, r_apogee - r_body)


def orbital_radius_at_angle(semi_major_axis: float, eccentricity: float, true_anomaly: float) -> float:
    """
    Calculate orbital radius at a given true anomaly.
    
    r = a(1 - e²) / (1 + e×cos(θ))
    
    Args:
        semi_major_axis: Semi-major axis in meters
        eccentricity: Orbital eccentricity
        true_anomaly: True anomaly in radians
    
    Returns:
        Orbital radius in meters
    
    Example:
        >>> # Radius at 90° from perigee
        >>> r = orbital_radius_at_angle(42164000, 0.72, math.pi/2)
    """
    a = _to_float(semi_major_axis)
    e = _to_float(eccentricity)
    theta = _to_float(true_anomaly)
    
    if a <= 0 or e < 0 or e >= 1:
        return 0.0
    
    return a * (1 - e ** 2) / (1 + e * math.cos(theta))


def true_anomaly_from_radius(semi_major_axis: float, eccentricity: float, radius: float) -> float:
    """
    Calculate true anomaly from orbital radius.
    
    cos(θ) = (a(1 - e²) / r - 1) / e
    
    Args:
        semi_major_axis: Semi-major axis in meters
        eccentricity: Orbital eccentricity
        radius: Orbital radius in meters
    
    Returns:
        True anomaly in radians (0 to π for valid orbits)
    
    Example:
        >>> theta = true_anomaly_from_radius(42164000, 0.72, R_EARTH + 200000)
    """
    a = _to_float(semi_major_axis)
    e = _to_float(eccentricity)
    r = _to_float(radius)
    
    if a <= 0 or e <= 0 or r <= 0:
        return 0.0
    
    # Solve for cos(theta)
    cos_theta = (a * (1 - e ** 2) / r - 1) / e
    
    # Clamp to valid range
    cos_theta = max(-1, min(1, cos_theta))
    
    return math.acos(cos_theta)


def orbital_distance_traveled(semi_major_axis: float, eccentricity: float, angle1: float, angle2: float) -> float:
    """
    Approximate distance traveled along an orbit between two true anomalies.
    
    Uses small angle approximation for short distances.
    
    Args:
        semi_major_axis: Semi-major axis in meters
        eccentricity: Orbital eccentricity
        angle1: Starting true anomaly in radians
        angle2: Ending true anomaly in radians
    
    Returns:
        Approximate distance in meters
    
    Example:
        >>> # Distance traveled in first quarter orbit
        >>> dist = orbital_distance_traveled(42164000, 0.72, 0, math.pi/2)
    """
    a = _to_float(semi_major_axis)
    e = _to_float(eccentricity)
    
    if a <= 0 or e < 0 or e >= 1:
        return 0.0
    
    # Use average of radii at both angles
    r1 = orbital_radius_at_angle(a, e, angle1)
    r2 = orbital_radius_at_angle(a, e, angle2)
    
    # Approximate distance using average radius
    avg_r = (r1 + r2) / 2
    angle_diff = abs(_to_float(angle2) - _to_float(angle1))
    
    return avg_r * angle_diff


# ============================================================================
# Multi-Body Calculations
# ============================================================================

def sphere_of_influence_radius(primary_radius: float, primary_gm: float, secondary_gm: float) -> float:
    """
    Calculate sphere of influence radius for a body orbiting a larger primary.
    
    r_SOI = a × (m_secondary / m_primary)^(2/5)
    ≈ a × (GM_secondary / GM_primary)^(2/5)
    
    Args:
        primary_radius: Semi-major axis of secondary's orbit around primary (in meters)
        primary_gm: Primary body's GM
        secondary_gm: Secondary body's GM
    
    Returns:
        Sphere of influence radius in meters
    
    Example:
        >>> # Earth's sphere of influence around Sun
        >>> soi = sphere_of_influence_radius(AU, GM_SUN, GM_EARTH)
    """
    a = _to_float(primary_radius)
    gm_p = _to_float(primary_gm)
    gm_s = _to_float(secondary_gm)
    
    if a <= 0 or gm_p <= 0 or gm_s <= 0:
        return 0.0
    
    return a * (gm_s / gm_p) ** (2/5)


def hill_sphere_radius(semi_major_axis: float, primary_gm: float, secondary_gm: float) -> float:
    """
    Calculate Hill sphere radius (approximation of stable orbit region).
    
    r_H = a × (m_secondary / (3 × m_primary))^(1/3)
    ≈ a × (GM_secondary / (3 × GM_primary))^(1/3)
    
    Args:
        semi_major_axis: Semi-major axis of secondary's orbit
        primary_gm: Primary body's GM
        secondary_gm: Secondary body's GM
    
    Returns:
        Hill sphere radius in meters
    
    Example:
        >>> # Earth's Hill sphere around Sun
        >>> r_hill = hill_sphere_radius(AU, GM_SUN, GM_EARTH)
    """
    a = _to_float(semi_major_axis)
    gm_p = _to_float(primary_gm)
    gm_s = _to_float(secondary_gm)
    
    if a <= 0 or gm_p <= 0 or gm_s <= 0:
        return 0.0
    
    return a * (gm_s / (3 * gm_p)) ** (1/3)


def synodic_period(period1: float, period2: float) -> float:
    """
    Calculate synodic period (time between conjunctions) of two bodies.
    
    1/T_syn = |1/T1 - 1/T2|
    
    Args:
        period1: Orbital period of first body in seconds
        period2: Orbital period of second body in seconds
    
    Returns:
        Synodic period in seconds
    
    Example:
        >>> # Synodic period of Moon relative to Sun (lunar month)
        >>> lunar_period = kepler_third_law_period(AU, GM_SUN)  # ~27.3 days sidereal
        >>> solar_period = 365.25 * 24 * 3600  # Earth's orbit
        >>> synodic = synodic_period(lunar_period, solar_period)
        >>> synodic / 3600 / 24  # Days
        29.5...
    """
    t1 = _to_float(period1)
    t2 = _to_float(period2)
    
    if t1 <= 0 or t2 <= 0:
        return 0.0
    
    return abs(1 / (1/t1 - 1/t2))


def orbital_phase_angle(period: float, elapsed_time: float) -> float:
    """
    Calculate orbital phase angle after elapsed time.
    
    θ = 2π × t / T
    
    Args:
        period: Orbital period in seconds
        elapsed_time: Time elapsed in seconds
    
    Returns:
        Phase angle in radians (normalized to [0, 2π])
    
    Example:
        >>> # Phase after 1 hour in LEO orbit
        >>> period = orbital_period_circular(400000)
        >>> phase = orbital_phase_angle(period, 3600)
    """
    t = _to_float(period)
    elapsed = _to_float(elapsed_time)
    
    if t <= 0:
        return 0.0
    
    phase = 2 * math.pi * elapsed / t
    return phase % (2 * math.pi)


# ============================================================================
# Body-Specific Presets
# ============================================================================

def earth_orbit_info(altitude_km: float) -> Dict[str, float]:
    """
    Get comprehensive orbital information for an Earth orbit.
    
    Args:
        altitude_km: Altitude in kilometers
    
    Returns:
        Dictionary with orbital parameters
    
    Example:
        >>> info = earth_orbit_info(400)  # ISS orbit
        >>> info['velocity_mps']
        7672.0...
    """
    altitude = altitude_km * 1000
    
    v = orbital_velocity_circular(altitude)
    period = orbital_period_circular(altitude)
    energy = specific_orbital_energy(R_EARTH + altitude)
    
    return {
        'altitude_km': altitude_km,
        'velocity_mps': v,
        'velocity_kmps': v / 1000,
        'period_seconds': period,
        'period_minutes': period / 60,
        'period_hours': period / 3600,
        'energy_jkg': energy,
        'radius_m': R_EARTH + altitude,
        'radius_km': (R_EARTH + altitude) / 1000,
    }


def moon_orbit_info(altitude_km: float) -> Dict[str, float]:
    """
    Get comprehensive orbital information for a Moon orbit.
    
    Args:
        altitude_km: Altitude in kilometers
    
    Returns:
        Dictionary with orbital parameters
    
    Example:
        >>> info = moon_orbit_info(100)
    """
    altitude = altitude_km * 1000
    
    v = orbital_velocity_circular(altitude, R_MOON, GM_MOON)
    period = orbital_period_circular(altitude, R_MOON, GM_MOON)
    energy = specific_orbital_energy(R_MOON + altitude, GM_MOON)
    
    return {
        'altitude_km': altitude_km,
        'velocity_mps': v,
        'velocity_kmps': v / 1000,
        'period_seconds': period,
        'period_minutes': period / 60,
        'period_hours': period / 3600,
        'energy_jkg': energy,
        'radius_m': R_MOON + altitude,
        'radius_km': (R_MOON + altitude) / 1000,
    }


def mars_orbit_info(altitude_km: float) -> Dict[str, float]:
    """
    Get comprehensive orbital information for a Mars orbit.
    
    Args:
        altitude_km: Altitude in kilometers
    
    Returns:
        Dictionary with orbital parameters
    
    Example:
        >>> info = mars_orbit_info(300)
    """
    altitude = altitude_km * 1000
    
    v = orbital_velocity_circular(altitude, R_MARS, GM_MARS)
    period = orbital_period_circular(altitude, R_MARS, GM_MARS)
    energy = specific_orbital_energy(R_MARS + altitude, GM_MARS)
    
    return {
        'altitude_km': altitude_km,
        'velocity_mps': v,
        'velocity_kmps': v / 1000,
        'period_seconds': period,
        'period_minutes': period / 60,
        'period_hours': period / 3600,
        'energy_jkg': energy,
        'radius_m': R_MARS + altitude,
        'radius_km': (R_MARS + altitude) / 1000,
    }


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Constants
    'G', 'GM_SUN', 'GM_EARTH', 'GM_MOON', 'GM_MARS', 'GM_JUPITER',
    'GM_VENUS', 'GM_MERCURY', 'GM_SATURN',
    'R_SUN', 'R_EARTH', 'R_MOON', 'R_MARS', 'R_JUPITER',
    'R_VENUS', 'R_MERCURY', 'R_SATURN',
    'G0', 'AU', 'C',
    
    # Kepler's Laws
    'kepler_third_law_period', 'kepler_third_lax_axis',
    'kepler_first_law_velocity', 'kepler_second_law_area_velocity',
    
    # Basic Orbital Parameters
    'orbital_velocity_circular', 'orbital_period_circular',
    'escape_velocity', 'surface_gravity',
    
    # Elliptical Orbit Parameters
    'calculate_eccentricity', 'calculate_semi_major_axis',
    'calculate_semi_minor_axis',
    'velocity_at_apogee', 'velocity_at_perigee',
    'orbital_period_elliptical',
    
    # Orbital Energy
    'specific_orbital_energy', 'specific_kinetic_energy',
    'specific_potential_energy', 'total_specific_energy',
    
    # Hohmann Transfer
    'hohmann_transfer_time', 'hohmann_transfer_velocity',
    'hohmann_delta_v',
    
    # Geostationary Orbit
    'geostationary_altitude', 'geostationary_velocity',
    
    # Launch Calculations
    'launch_velocity_to_orbit', 'gravity_loss_estimate',
    'launch_window_azimuth', 'minimum_inclination_from_latitude',
    
    # Orbital Mechanics Utilities
    'orbital_altitude_range', 'orbital_radius_at_angle',
    'true_anomaly_from_radius', 'orbital_distance_traveled',
    
    # Multi-Body Calculations
    'sphere_of_influence_radius', 'hill_sphere_radius',
    'synodic_period', 'orbital_phase_angle',
    
    # Body-Specific Presets
    'earth_orbit_info', 'moon_orbit_info', 'mars_orbit_info',
]


if __name__ == '__main__':
    # Quick demo
    print("AllToolkit Orbital Mechanics Utils Demo")
    print("=" * 50)
    
    # ISS orbit (400 km)
    print("\nISS Orbit (400 km altitude):")
    info = earth_orbit_info(400)
    print(f"  Velocity: {info['velocity_kmps']:.2f} km/s")
    print(f"  Period: {info['period_minutes']:.2f} minutes")
    
    # Geostationary orbit
    print("\nGeostationary Orbit:")
    geo_alt = geostationary_altitude() / 1000
    print(f"  Altitude: {geo_alt:.2f} km")
    print(f"  Velocity: {geostationary_velocity():.2f} m/s")
    
    # GTO transfer
    print("\nGTO (200 km → 35786 km):")
    dv1, dv2, total = hohmann_delta_v(R_EARTH + 200000, R_EARTH + 35786000)
    print(f"  Delta-V: {total:.2f} m/s")
    print(f"  Transfer time: {hohmann_transfer_time(R_EARTH + 200000, R_EARTH + 35786000)/3600:.2f} hours")
    
    # Escape velocity
    print("\nEarth Escape Velocity:")
    print(f"  Surface: {escape_velocity():.2f} m/s")
    print(f"  From 400 km: {escape_velocity(400000):.2f} m/s")
    
    print("\nFor full documentation, see README.md")