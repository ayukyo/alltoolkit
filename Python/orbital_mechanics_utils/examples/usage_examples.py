#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Orbital Mechanics Utilities Examples
==================================================
Demonstration of orbital mechanics calculations for various scenarios.
"""

import math
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # Constants
    GM_EARTH, GM_MOON, GM_SUN, GM_MARS, GM_JUPITER, GM_VENUS,
    R_EARTH, R_MOON, R_MARS, R_JUPITER, R_VENUS, AU,
    
    # Kepler's Laws
    kepler_third_law_period, kepler_third_lax_axis,
    kepler_first_law_velocity,
    
    # Basic Orbital Parameters
    orbital_velocity_circular, orbital_period_circular,
    escape_velocity, surface_gravity,
    
    # Elliptical Orbit Parameters
    calculate_eccentricity, calculate_semi_major_axis,
    velocity_at_perigee, velocity_at_apogee,
    orbital_period_elliptical,
    
    # Orbital Energy
    specific_orbital_energy, specific_kinetic_energy,
    specific_potential_energy,
    
    # Hohmann Transfer
    hohmann_transfer_time, hohmann_delta_v,
    
    # Geostationary Orbit
    geostationary_altitude, geostationary_velocity,
    
    # Launch Calculations
    launch_window_azimuth, minimum_inclination_from_latitude,
    
    # Multi-Body Calculations
    sphere_of_influence_radius, hill_sphere_radius,
    synodic_period,
    
    # Body-Specific Presets
    earth_orbit_info, moon_orbit_info, mars_orbit_info,
)


def example_1_iss_orbit():
    """
    Example 1: ISS (International Space Station) Orbit Analysis
    
    The ISS orbits at approximately 400 km altitude.
    """
    print("=" * 60)
    print("Example 1: ISS Orbit Analysis (400 km altitude)")
    print("=" * 60)
    
    altitude_km = 400
    info = earth_orbit_info(altitude_km)
    
    print(f"\nOrbital Parameters:")
    print(f"  Altitude: {info['altitude_km']} km")
    print(f"  Orbital Radius: {info['radius_km']:.2f} km")
    print(f"  Velocity: {info['velocity_kmps']:.2f} km/s ({info['velocity_mps']:.1f} m/s)")
    print(f"  Period: {info['period_minutes']:.2f} minutes ({info['period_hours']:.2f} hours)")
    print(f"  Specific Energy: {info['energy_jkg']:.2e} J/kg")
    
    # Additional calculations
    print(f"\nAdditional Info:")
    orbits_per_day = 24 * 60 / info['period_minutes']
    print(f"  Orbits per day: {orbits_per_day:.2f}")
    
    # Velocity relative to Earth's rotation
    earth_surface_velocity = 2 * math.pi * R_EARTH / (24 * 3600)  # ~465 m/s at equator
    relative_velocity = info['velocity_mps'] - earth_surface_velocity
    print(f"  Relative velocity (vs Earth surface): {relative_velocity:.1f} m/s")


def example_2_geostationary_orbit():
    """
    Example 2: Geostationary Orbit Analysis
    
    Geostationary satellites orbit at ~35,786 km altitude.
    """
    print("\n" + "=" * 60)
    print("Example 2: Geostationary Orbit Analysis")
    print("=" * 60)
    
    geo_alt = geostationary_altitude()
    geo_v = geostationary_velocity()
    geo_period = orbital_period_circular(geo_alt)
    
    print(f"\nGeostationary Parameters:")
    print(f"  Altitude: {geo_alt/1000:.2f} km")
    print(f"  Orbital Radius: {(R_EARTH + geo_alt)/1000:.2f} km")
    print(f"  Velocity: {geo_v:.2f} m/s ({geo_v/1000:.3f} km/s)")
    print(f"  Period: {geo_period/3600:.2f} hours")
    
    print(f"\nComparison with LEO (400 km):")
    leo_info = earth_orbit_info(400)
    print(f"  GEO altitude: {geo_alt/1000:.1f} km vs LEO: 400 km")
    print(f"  GEO velocity: {geo_v/1000:.3f} km/s vs LEO: {leo_info['velocity_kmps']:.2f} km/s")
    print(f"  GEO period: {geo_period/3600:.2f} hrs vs LEO: {leo_info['period_hours']:.2f} hrs")


def example_3_gto_transfer():
    """
    Example 3: Geostationary Transfer Orbit (GTO)
    
    Typical GTO: perigee 200 km, apogee 35,786 km
    """
    print("\n" + "=" * 60)
    print("Example 3: Geostationary Transfer Orbit (GTO)")
    print("=" * 60)
    
    apogee_km = 35786
    perigee_km = 200
    
    print(f"\nGTO Parameters:")
    print(f"  Perigee: {perigee_km} km")
    print(f"  Apogee: {apogee_km} km")
    
    # Orbital characteristics
    e = calculate_eccentricity(apogee_km * 1000, perigee_km * 1000)
    a = calculate_semi_major_axis(apogee_km * 1000, perigee_km * 1000)
    
    print(f"  Eccentricity: {e:.4f}")
    print(f"  Semi-major axis: {a/1000:.2f} km")
    
    # Velocities at key points
    v_perigee = velocity_at_perigee(apogee_km * 1000, perigee_km * 1000)
    v_apogee = velocity_at_apogee(apogee_km * 1000, perigee_km * 1000)
    
    print(f"\nVelocities:")
    print(f"  At perigee: {v_perigee:.2f} m/s ({v_perigee/1000:.3f} km/s)")
    print(f"  At apogee: {v_apogee:.2f} m/s ({v_apogee/1000:.3f} km/s)")
    print(f"  Ratio (perigee/apogee): {v_perigee/v_apogee:.2f}")
    
    # Orbital period
    period = orbital_period_elliptical(apogee_km * 1000, perigee_km * 1000)
    print(f"\nOrbital Period: {period/3600:.2f} hours")


def example_4_hohmann_transfer():
    """
    Example 4: Hohmann Transfer - LEO to GEO
    
    Calculate the delta-V requirements for transferring from LEO to GEO.
    """
    print("\n" + "=" * 60)
    print("Example 4: Hohmann Transfer (LEO → GEO)")
    print("=" * 60)
    
    r_leo = R_EARTH + 400000  # 400 km LEO
    r_geo = R_EARTH + 35786000  # GEO
    
    print(f"\nTransfer Parameters:")
    print(f"  Initial orbit: 400 km LEO")
    print(f"  Final orbit: GEO ({35786} km)")
    
    # Transfer time
    transfer_time = hohmann_transfer_time(r_leo, r_geo)
    print(f"\nTransfer Time: {transfer_time/3600:.2f} hours")
    
    # Delta-V requirements
    dv1, dv2, total = hohmann_delta_v(r_leo, r_geo)
    
    print(f"\nDelta-V Requirements:")
    print(f"  First burn (departure): {dv1:.2f} m/s")
    print(f"  Second burn (arrival): {dv2:.2f} m/s")
    print(f"  Total delta-V: {total:.2f} m/s ({total/1000:.3f} km/s)")
    
    # Compare with direct launch
    print(f"\nComparison:")
    print(f"  Direct launch to GEO from surface: ~{escape_velocity(35786000)/1000:.2f} km/s (escape)")
    print(f"  Two-burn transfer: {total/1000:.3f} km/s (much less fuel)")


def example_5_escape_velocity():
    """
    Example 5: Escape Velocity Calculations
    
    Escape velocity from various bodies at different altitudes.
    """
    print("\n" + "=" * 60)
    print("Example 5: Escape Velocity Analysis")
    print("=" * 60)
    
    print("\nEscape Velocity from Earth:")
    altitudes = [0, 400, 35786]  # km
    for alt_km in altitudes:
        v_esc = escape_velocity(alt_km * 1000)
        print(f"  At {alt_km} km: {v_esc:.2f} m/s ({v_esc/1000:.3f} km/s)")
    
    print("\nSurface Escape Velocity of Various Bodies:")
    
    # Moon
    v_esc_moon = escape_velocity(0, R_MOON, GM_MOON)
    print(f"  Moon: {v_esc_moon:.2f} m/s ({v_esc_moon/1000:.3f} km/s)")
    
    # Mars
    v_esc_mars = escape_velocity(0, R_MARS, GM_MARS)
    print(f"  Mars: {v_esc_mars:.2f} m/s ({v_esc_mars/1000:.3f} km/s)")
    
    # Earth (already calculated)
    v_esc_earth = escape_velocity()
    print(f"  Earth: {v_esc_earth:.2f} m/s ({v_esc_earth/1000:.3f} km/s)")
    
    print(f"\nComparison:")
    print(f"  Moon escape velocity is {v_esc_earth/v_esc_moon:.1f}× lower than Earth")
    print(f"  Mars escape velocity is {v_esc_earth/v_esc_mars:.2f}× lower than Earth")


def example_6_launch_window():
    """
    Example 6: Launch Window Calculations
    
    Calculate launch azimuth for various orbital inclinations.
    """
    print("\n" + "=" * 60)
    print("Example 6: Launch Window Calculations")
    print("=" * 60)
    
    launch_sites = {
        'Kennedy Space Center (28.5°N)': 28.5,
        'Vandenberg (34.7°N)': 34.7,
        'Baikonur (45.6°N)': 45.6,
        'Kourou (5.2°N)': 5.2,
    }
    
    target_inclinations = [28.5, 51.6, 90]  # Degrees
    
    print("\nLaunch Azimuths for Different Inclinations:")
    print(f"(Azimuth: 0°=North, 90°=East, 180°=South)")
    
    for site, lat in launch_sites.items():
        print(f"\n{site}:")
        min_inc = minimum_inclination_from_latitude(lat)
        print(f"  Minimum achievable inclination: {min_inc:.1f}°")
        
        for inc in target_inclinations:
            if inc >= min_inc:
                azimuth = launch_window_azimuth(inc, lat)
                print(f"  For {inc}° inclination: azimuth = {azimuth:.1f}°")
            else:
                print(f"  Cannot reach {inc}° inclination from this latitude")


def example_7_sphere_of_influence():
    """
    Example 7: Sphere of Influence and Hill Sphere
    
    Calculate regions where a body's gravity dominates.
    """
    print("\n" + "=" * 60)
    print("Example 7: Sphere of Influence Analysis")
    print("=" * 60)
    
    print("\nEarth's Sphere of Influence around Sun:")
    soi_earth = sphere_of_influence_radius(AU, GM_SUN, GM_EARTH)
    print(f"  SOI radius: {soi_earth/1e6:.2f} million km")
    print(f"  Ratio to AU: {soi_earth/AU:.4f}")
    
    print("\nEarth's Hill Sphere around Sun:")
    hill_earth = hill_sphere_radius(AU, GM_SUN, GM_EARTH)
    print(f"  Hill radius: {hill_earth/1e6:.2f} million km")
    print(f"  Stable orbit region (1/3 Hill radius): {hill_earth/3/1e6:.2f} million km")
    
    print("\nMoon's Sphere of Influence around Earth:")
    moon_distance = 384400000  # Average distance to Moon
    soi_moon = sphere_of_influence_radius(moon_distance, GM_EARTH, GM_MOON)
    print(f"  SOI radius: {soi_moon/1000:.1f} km")
    print(f"  Ratio to Moon's radius: {soi_moon/R_MOON:.1f}×")


def example_8_moon_and_mars_orbits():
    """
    Example 8: Lunar and Martian Orbit Analysis
    """
    print("\n" + "=" * 60)
    print("Example 8: Moon and Mars Orbit Analysis")
    print("=" * 60)
    
    # Lunar orbit
    print("\nLow Lunar Orbit (100 km):")
    moon_info = moon_orbit_info(100)
    print(f"  Velocity: {moon_info['velocity_mps']:.2f} m/s")
    print(f"  Period: {moon_info['period_minutes']:.2f} minutes")
    print(f"  (Note: Apollo missions orbited at ~100 km)")
    
    # Mars orbit
    print("\nLow Mars Orbit (300 km):")
    mars_info = mars_orbit_info(300)
    print(f"  Velocity: {mars_info['velocity_mps']:.2f} m/s")
    print(f"  Period: {mars_info['period_minutes']:.2f} minutes")
    
    # Comparison
    print("\nComparison with Earth LEO (400 km):")
    earth_info = earth_orbit_info(400)
    print(f"  Earth: {earth_info['velocity_mps']:.2f} m/s, {earth_info['period_minutes']:.2f} min")
    print(f"  Moon: {moon_info['velocity_mps']:.2f} m/s, {moon_info['period_minutes']:.2f} min")
    print(f"  Mars: {mars_info['velocity_mps']:.2f} m/s, {mars_info['period_minutes']:.2f} min")


def example_9_orbital_energy():
    """
    Example 9: Orbital Energy Analysis
    
    Compare energy requirements for different orbits.
    """
    print("\n" + "=" * 60)
    print("Example 9: Orbital Energy Analysis")
    print("=" * 60)
    
    orbits = [
        ('LEO (200 km)', 200),
        ('LEO (400 km)', 400),
        ('LEO (800 km)', 800),
        ('MEO (2000 km)', 2000),
        ('GEO', 35786),
    ]
    
    print("\nSpecific Orbital Energy (J/kg) for Different Orbits:")
    print("(Negative = bound orbit, more negative = more energy to escape)")
    
    for name, alt_km in orbits:
        r = R_EARTH + alt_km * 1000
        energy = specific_orbital_energy(r)
        print(f"  {name}: {energy:.2e} J/kg")
    
    print("\nEnergy to Escape from Different Orbits:")
    for name, alt_km in orbits:
        r = R_EARTH + alt_km * 1000
        orbital_energy = specific_orbital_energy(r)
        # Need to add |orbital_energy| to escape
        escape_energy = abs(orbital_energy)
        print(f"  {name}: {escape_energy:.2e} J/kg")


def example_10_satellite_design():
    """
    Example 10: Satellite Design Calculations
    
    Practical calculations for satellite mission planning.
    """
    print("\n" + "=" * 60)
    print("Example 10: Satellite Mission Planning")
    print("=" * 60)
    
    # Scenario: Communications satellite
    print("\nMission: Communications Satellite in GEO")
    
    geo_alt = geostationary_altitude()
    geo_info = earth_orbit_info(geo_alt / 1000)
    
    print(f"\nOrbital Parameters:")
    print(f"  Altitude: {geo_alt/1000:.0f} km")
    print(f"  Velocity: {geo_info['velocity_mps']:.1f} m/s")
    print(f"  Orbital circumference: {2*math.pi*geo_info['radius_m']/1000:.0f} km")
    
    # Launch requirements
    r_leo = R_EARTH + 200000  # 200 km parking orbit
    dv1, dv2, total = hohmann_delta_v(r_leo, R_EARTH + geo_alt)
    
    print(f"\nLaunch Requirements:")
    print(f"  Parking orbit altitude: 200 km")
    print(f"  Transfer delta-V: {total:.0f} m/s")
    print(f"  Transfer time: {hohmann_transfer_time(r_leo, R_EARTH + geo_alt)/3600:.1f} hours")
    
    # Coverage
    print(f"\nCoverage Analysis:")
    # GEO can see about 1/3 of Earth's surface
    coverage_angle = math.asin(R_EARTH / geo_info['radius_m'])
    coverage_degrees = math.degrees(coverage_angle)
    print(f"  Coverage angle from satellite: {coverage_degrees:.1f}°")
    print(f"  Visible Earth surface: ~{1 - math.cos(coverage_angle):.1%}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("AllToolkit Orbital Mechanics Examples")
    print("=" * 60)
    
    example_1_iss_orbit()
    example_2_geostationary_orbit()
    example_3_gto_transfer()
    example_4_hohmann_transfer()
    example_5_escape_velocity()
    example_6_launch_window()
    example_7_sphere_of_influence()
    example_8_moon_and_mars_orbits()
    example_9_orbital_energy()
    example_10_satellite_design()
    
    print("\n" + "=" * 60)
    print("Examples Complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()