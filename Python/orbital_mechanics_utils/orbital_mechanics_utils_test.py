#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Orbital Mechanics Utilities Test Suite
====================================================
Comprehensive tests for orbital mechanics calculations.
"""

import math
import unittest
from mod import (
    # Constants
    G, GM_EARTH, GM_MOON, GM_SUN, R_EARTH, R_MOON, AU, G0,
    
    # Kepler's Laws
    kepler_third_law_period, kepler_third_lax_axis,
    kepler_first_law_velocity, kepler_second_law_area_velocity,
    
    # Basic Orbital Parameters
    orbital_velocity_circular, orbital_period_circular,
    escape_velocity, surface_gravity,
    
    # Elliptical Orbit Parameters
    calculate_eccentricity, calculate_semi_major_axis,
    calculate_semi_minor_axis,
    velocity_at_apogee, velocity_at_perigee,
    orbital_period_elliptical,
    
    # Orbital Energy
    specific_orbital_energy, specific_kinetic_energy,
    specific_potential_energy, total_specific_energy,
    
    # Hohmann Transfer
    hohmann_transfer_time, hohmann_transfer_velocity,
    hohmann_delta_v,
    
    # Geostationary Orbit
    geostationary_altitude, geostationary_velocity,
    
    # Launch Calculations
    launch_velocity_to_orbit, gravity_loss_estimate,
    launch_window_azimuth, minimum_inclination_from_latitude,
    
    # Orbital Mechanics Utilities
    orbital_altitude_range, orbital_radius_at_angle,
    true_anomaly_from_radius,
    
    # Multi-Body Calculations
    sphere_of_influence_radius, hill_sphere_radius,
    synodic_period, orbital_phase_angle,
    
    # Body-Specific Presets
    earth_orbit_info, moon_orbit_info, mars_orbit_info,
)


class TestConstants(unittest.TestCase):
    """Test physical constants."""
    
    def test_gravitational_constant(self):
        """Test G value is correct."""
        self.assertAlmostEqual(G, 6.67430e-11, places=5)
    
    def test_earth_gm(self):
        """Test Earth's GM."""
        self.assertAlmostEqual(GM_EARTH, 3.986004418e14, places=5)
    
    def test_earth_radius(self):
        """Test Earth radius."""
        self.assertAlmostEqual(R_EARTH, 6.371e6, places=3)
    
    def test_au_value(self):
        """Test Astronomical Unit."""
        self.assertAlmostEqual(AU, 1.495978707e11, places=3)


class TestKeplersLaws(unittest.TestCase):
    """Test Kepler's laws calculations."""
    
    def test_kepler_third_law_period_leo(self):
        """Test orbital period for LEO orbit."""
        # ISS orbit ~400 km, period ~92.5 minutes
        altitude = 400000  # meters
        r = R_EARTH + altitude
        period = kepler_third_law_period(r)
        period_minutes = period / 60
        self.assertAlmostEqual(period_minutes, 92.5, delta=0.5)
    
    def test_kepler_third_law_period_geo(self):
        """Test orbital period for GEO orbit."""
        # GEO period should be ~24 hours sidereal
        altitude = 35786000  # meters
        r = R_EARTH + altitude
        period = kepler_third_law_period(r)
        period_hours = period / 3600
        self.assertAlmostEqual(period_hours, 24, delta=0.1)
    
    def test_kepler_third_lax_axis(self):
        """Test semi-major axis calculation from period."""
        # For 24-hour orbit, should give GEO radius
        period = 24 * 3600  # sidereal day
        axis = kepler_third_lax_axis(period)
        expected_alt = R_EARTH + 35786000
        self.assertAlmostEqual(axis, expected_alt, delta=100000)  # 100 km tolerance
    
    def test_kepler_first_law_velocity_circular(self):
        """Test vis-viva equation for circular orbit."""
        altitude = 400000
        r = R_EARTH + altitude
        v = kepler_first_law_velocity(r, r)  # circular orbit: a = r
        v_circular = orbital_velocity_circular(altitude)
        self.assertAlmostEqual(v, v_circular, places=1)
    
    def test_kepler_second_law_area_velocity(self):
        """Test specific angular momentum."""
        altitude = 400000
        r = R_EARTH + altitude
        h = kepler_second_law_area_velocity(r)
        # h = r × v for circular orbit
        v = orbital_velocity_circular(altitude)
        expected_h = r * v
        self.assertAlmostEqual(h, expected_h, places=0)


class TestBasicOrbitalParameters(unittest.TestCase):
    """Test basic orbital parameter calculations."""
    
    def test_orbital_velocity_circular(self):
        """Test circular orbital velocity."""
        # ISS velocity ~7.67 km/s at 400 km
        v = orbital_velocity_circular(400000)
        self.assertAlmostEqual(v / 1000, 7.67, delta=0.05)
    
    def test_orbital_period_circular(self):
        """Test circular orbital period."""
        # LEO period ~92.5 minutes
        period = orbital_period_circular(400000)
        self.assertAlmostEqual(period / 60, 92.5, delta=0.5)
    
    def test_escape_velocity_surface(self):
        """Test escape velocity from Earth surface."""
        # Earth escape velocity ~11.2 km/s
        v_esc = escape_velocity()
        self.assertAlmostEqual(v_esc / 1000, 11.2, delta=0.1)
    
    def test_escape_velocity_altitude(self):
        """Test escape velocity at altitude."""
        v_esc_surface = escape_velocity(0)
        v_esc_400km = escape_velocity(400000)
        # Should decrease with altitude
        self.assertLess(v_esc_400km, v_esc_surface)
    
    def test_surface_gravity(self):
        """Test surface gravity calculation."""
        g = surface_gravity()
        self.assertAlmostEqual(g, G0, delta=0.1)
    
    def test_orbital_velocity_zero_altitude(self):
        """Test velocity at zero altitude (surface)."""
        v = orbital_velocity_circular(0)
        # Should be ~7.9 km/s (surface circular orbit theoretical)
        self.assertAlmostEqual(v / 1000, 7.9, delta=0.1)


class TestEllipticalOrbit(unittest.TestCase):
    """Test elliptical orbit calculations."""
    
    def test_calculate_eccentricity_gto(self):
        """Test eccentricity calculation for GTO."""
        # GTO: perigee 200 km, apogee 35786 km
        e = calculate_eccentricity(35786000, 200000)
        # Should be ~0.73
        self.assertAlmostEqual(e, 0.73, delta=0.01)
    
    def test_calculate_eccentricity_circular(self):
        """Test eccentricity for circular orbit."""
        e = calculate_eccentricity(400000, 400000)
        self.assertAlmostEqual(e, 0.0, places=5)
    
    def test_calculate_semi_major_axis(self):
        """Test semi-major axis calculation."""
        a = calculate_semi_major_axis(35786000, 200000)
        r_p = R_EARTH + 200000
        r_a = R_EARTH + 35786000
        expected = (r_p + r_a) / 2
        self.assertAlmostEqual(a, expected, places=0)
    
    def test_calculate_semi_minor_axis(self):
        """Test semi-minor axis calculation."""
        a = 42164000
        e = 0.72
        b = calculate_semi_minor_axis(a, e)
        expected = a * math.sqrt(1 - e**2)
        self.assertAlmostEqual(b, expected, places=0)
    
    def test_velocity_at_perigee_vs_apogee(self):
        """Test velocity relationship at perigee vs apogee."""
        v_perigee = velocity_at_perigee(35786000, 200000)
        v_apogee = velocity_at_apogee(35786000, 200000)
        # Perigee velocity should be higher than apogee
        self.assertGreater(v_perigee, v_apogee)
    
    def test_orbital_period_elliptical(self):
        """Test elliptical orbit period."""
        # GTO period ~10.5 hours
        period = orbital_period_elliptical(35786000, 200000)
        self.assertAlmostEqual(period / 3600, 10.5, delta=0.2)


class TestOrbitalEnergy(unittest.TestCase):
    """Test orbital energy calculations."""
    
    def test_specific_orbital_energy_negative(self):
        """Test that bound orbit energy is negative."""
        energy = specific_orbital_energy(R_EARTH + 400000)
        self.assertLess(energy, 0)
    
    def test_specific_kinetic_energy(self):
        """Test kinetic energy calculation."""
        v = 7672  # m/s
        ke = specific_kinetic_energy(v)
        expected = v**2 / 2
        self.assertAlmostEqual(ke, expected, places=1)
    
    def test_specific_potential_energy(self):
        """Test potential energy calculation."""
        r = R_EARTH + 400000
        pe = specific_potential_energy(r)
        expected = -GM_EARTH / r
        self.assertAlmostEqual(pe, expected, places=1)
    
    def test_total_specific_energy(self):
        """Test total energy equals orbital energy."""
        r = R_EARTH + 400000
        v = orbital_velocity_circular(400000)
        total = total_specific_energy(r, v)
        orbital = specific_orbital_energy(r)
        # For circular orbit, they should match
        self.assertAlmostEqual(total, orbital, places=0)


class TestHohmannTransfer(unittest.TestCase):
    """Test Hohmann transfer calculations."""
    
    def test_hohmann_transfer_time(self):
        """Test Hohmann transfer time."""
        # LEO to GEO transfer ~5.25 hours
        r1 = R_EARTH + 400000
        r2 = R_EARTH + 35786000
        t = hohmann_transfer_time(r1, r2)
        self.assertAlmostEqual(t / 3600, 5.25, delta=0.1)
    
    def test_hohmann_transfer_velocity(self):
        """Test Hohmann transfer velocities."""
        r1 = R_EARTH + 400000
        r2 = R_EARTH + 35786000
        v1, vt1, vt2 = hohmann_transfer_velocity(r1, r2)
        
        # Initial circular velocity
        v_circular = orbital_velocity_circular(400000)
        self.assertAlmostEqual(v1, v_circular, places=0)
        
        # Transfer velocities should be between circular velocities
        v2 = orbital_velocity_circular(35786000)
        self.assertGreater(vt1, v1)  # Acceleration at perigee
        self.assertLess(vt2, v2)     # Need to accelerate at apogee
    
    def test_hohmann_delta_v(self):
        """Test Hohmann delta-V calculation."""
        # LEO to GEO total delta-V ~3.9 km/s
        r1 = R_EARTH + 400000
        r2 = R_EARTH + 35786000
        dv1, dv2, total = hohmann_delta_v(r1, r2)
        self.assertAlmostEqual(total / 1000, 3.9, delta=0.2)
    
    def test_hohmann_transfer_same_orbit(self):
        """Test Hohmann transfer to same orbit."""
        r = R_EARTH + 400000
        t = hohmann_transfer_time(r, r)
        # Should be half period of circular orbit
        half_period = orbital_period_circular(400000) / 2
        self.assertAlmostEqual(t, half_period, places=0)


class TestGeostationaryOrbit(unittest.TestCase):
    """Test geostationary orbit calculations."""
    
    def test_geostationary_altitude(self):
        """Test geostationary altitude calculation."""
        alt = geostationary_altitude()
        # Should be ~35786 km
        self.assertAlmostEqual(alt / 1000, 35786, delta=100)
    
    def test_geostationary_velocity(self):
        """Test geostationary velocity."""
        v = geostationary_velocity()
        # Should be ~3.07 km/s
        self.assertAlmostEqual(v / 1000, 3.07, delta=0.05)
    
    def test_geostationary_period(self):
        """Test geostationary orbit period."""
        alt = geostationary_altitude()
        period = orbital_period_circular(alt)
        # Should be ~24 hours sidereal
        self.assertAlmostEqual(period / 3600, 24, delta=0.1)


class TestLaunchCalculations(unittest.TestCase):
    """Test launch calculations."""
    
    def test_launch_velocity_to_orbit(self):
        """Test launch velocity calculation."""
        v = launch_velocity_to_orbit(400000)
        # Should be less than escape velocity
        self.assertLess(v, escape_velocity())
        # Should be greater than circular orbit velocity
        self.assertGreater(v, orbital_velocity_circular(400000))
    
    def test_gravity_loss_estimate(self):
        """Test gravity loss estimate."""
        loss = gravity_loss_estimate(9000, 180)  # 3 min ascent
        expected = G0 * 180
        self.assertAlmostEqual(loss, expected, places=0)
    
    def test_launch_window_azimuth(self):
        """Test launch azimuth calculation."""
        # ISS orbit 51.6° from Kennedy (28.5°N)
        azimuth = launch_window_azimuth(51.6, 28.5)
        # Should be approximately 63° (NE)
        self.assertGreater(azimuth, 60)
        self.assertLess(azimuth, 65)
    
    def test_minimum_inclination_from_latitude(self):
        """Test minimum inclination."""
        min_inc = minimum_inclination_from_latitude(28.5)
        self.assertEqual(min_inc, 28.5)


class TestOrbitalUtilities(unittest.TestCase):
    """Test orbital mechanics utilities."""
    
    def test_orbital_altitude_range(self):
        """Test altitude range calculation."""
        # Use actual GTO parameters: a = 42,164,000 m, e ≈ 0.73
        a = calculate_semi_major_axis(35786000, 200000)
        e = calculate_eccentricity(35786000, 200000)
        perigee, apogee = orbital_altitude_range(a, e)
        
        # Should match input values
        self.assertAlmostEqual(perigee / 1000, 200, delta=20)  # ~200 km
        self.assertAlmostEqual(apogee / 1000, 35786, delta=500)  # ~35786 km
    
    def test_orbital_radius_at_angle(self):
        """Test radius at true anomaly."""
        a = 42164000
        e = 0.72
        
        # At perigee (θ = 0)
        r_perigee = orbital_radius_at_angle(a, e, 0)
        expected_r_p = a * (1 - e)
        self.assertAlmostEqual(r_perigee, expected_r_p, places=0)
        
        # At apogee (θ = π)
        r_apogee = orbital_radius_at_angle(a, e, math.pi)
        expected_r_a = a * (1 + e)
        self.assertAlmostEqual(r_apogee, expected_r_a, places=0)
    
    def test_orbital_radius_at_90_degrees(self):
        """Test radius at 90°."""
        a = 42164000
        e = 0.72
        r_90 = orbital_radius_at_angle(a, e, math.pi / 2)
        # At 90°, r = a(1-e²)
        expected = a * (1 - e**2)
        self.assertAlmostEqual(r_90, expected, places=0)


class TestMultiBodyCalculations(unittest.TestCase):
    """Test multi-body orbital calculations."""
    
    def test_sphere_of_influence_earth(self):
        """Test Earth's sphere of influence around Sun."""
        soi = sphere_of_influence_radius(AU, GM_SUN, GM_EARTH)
        # Should be ~925000 km (~0.925 million km)
        self.assertAlmostEqual(soi / 1e9, 0.925, delta=0.05)  # Convert to million km
    
    def test_hill_sphere_earth(self):
        """Test Earth's Hill sphere."""
        r_hill = hill_sphere_radius(AU, GM_SUN, GM_EARTH)
        # Should be ~1.5 million km
        self.assertAlmostEqual(r_hill / 1e9, 1.5, delta=0.1)  # Convert to million km
    
    def test_synodic_period(self):
        """Test synodic period calculation."""
        # Earth-Moon synodic period ~29.5 days
        sidereal_month = 27.3 * 24 * 3600
        sidereal_year = 365.25 * 24 * 3600
        synodic = synodic_period(sidereal_month, sidereal_year)
        self.assertAlmostEqual(synodic / 3600 / 24, 29.5, delta=0.5)
    
    def test_orbital_phase_angle(self):
        """Test orbital phase angle."""
        period = 92.5 * 60  # LEO period in seconds
        phase = orbital_phase_angle(period, period)  # After one full orbit
        self.assertAlmostEqual(phase, 0, places=5)  # Should be normalized to 0
        
        phase_half = orbital_phase_angle(period, period / 2)
        self.assertAlmostEqual(phase_half, math.pi, places=5)


class TestBodySpecificPresets(unittest.TestCase):
    """Test body-specific orbital presets."""
    
    def test_earth_orbit_info(self):
        """Test Earth orbit info."""
        info = earth_orbit_info(400)
        
        self.assertAlmostEqual(info['velocity_kmps'], 7.67, delta=0.05)
        self.assertAlmostEqual(info['period_minutes'], 92.5, delta=0.5)
        self.assertLess(info['energy_jkg'], 0)  # Bound orbit
    
    def test_moon_orbit_info(self):
        """Test Moon orbit info."""
        info = moon_orbit_info(100)
        
        # Moon orbital velocity should be lower than Earth
        self.assertLess(info['velocity_mps'], orbital_velocity_circular(100000))
    
    def test_mars_orbit_info(self):
        """Test Mars orbit info."""
        info = mars_orbit_info(300)
        
        # Mars velocity should be lower than Earth at same altitude
        self.assertLess(info['velocity_mps'], orbital_velocity_circular(300000))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_negative_altitude(self):
        """Test negative altitude handling."""
        v = orbital_velocity_circular(-100000)
        self.assertEqual(v, 0.0)
    
    def test_zero_semi_major_axis(self):
        """Test zero semi-major axis."""
        period = kepler_third_law_period(0)
        self.assertEqual(period, 0.0)
    
    def test_eccentricity_bounds(self):
        """Test eccentricity boundary conditions."""
        # e >= 1 should return 0
        b = calculate_semi_minor_axis(42164000, 1.0)
        self.assertEqual(b, 0.0)
        
        # e < 0 should return 0
        b = calculate_semi_minor_axis(42164000, -0.5)
        self.assertEqual(b, 0.0)
    
    def test_circular_orbit_eccentricity(self):
        """Test circular orbit properties."""
        e = calculate_eccentricity(400000, 400000)
        self.assertAlmostEqual(e, 0.0, places=10)
        
        v_p = velocity_at_perigee(400000, 400000)
        v_a = velocity_at_apogee(400000, 400000)
        self.assertAlmostEqual(v_p, v_a, places=1)


class TestPhysicalConsistency(unittest.TestCase):
    """Test physical consistency of calculations."""
    
    def test_energy_conservation(self):
        """Test energy conservation in orbit."""
        r = R_EARTH + 400000
        v = orbital_velocity_circular(400000)
        
        # For circular orbit, kinetic + potential = orbital energy
        ke = specific_kinetic_energy(v)
        pe = specific_potential_energy(r)
        orbital = specific_orbital_energy(r)
        
        self.assertAlmostEqual(ke + pe, orbital, places=0)
    
    def test_velocity_period_consistency(self):
        """Test velocity and period consistency."""
        altitude = 400000
        v = orbital_velocity_circular(altitude)
        period = orbital_period_circular(altitude)
        r = R_EARTH + altitude
        
        # v = 2πr / T
        v_from_period = 2 * math.pi * r / period
        self.assertAlmostEqual(v, v_from_period, places=1)
    
    def test_escape_velocity_ratio(self):
        """Test escape velocity vs circular velocity ratio."""
        # Escape velocity should be sqrt(2) × circular velocity
        v_circular = orbital_velocity_circular(400000)
        v_escape = escape_velocity(400000)
        
        ratio = v_escape / v_circular
        self.assertAlmostEqual(ratio, math.sqrt(2), places=3)


if __name__ == '__main__':
    unittest.main(verbosity=2)