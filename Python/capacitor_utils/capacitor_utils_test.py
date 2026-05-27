#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Capacitor Utilities Test Module
=============================================
Comprehensive tests for capacitor calculations and code decoding.
"""

import unittest
import math
import sys
import os

# Ensure the module directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    convert_capacitance, format_capacitance, parse_capacitance_string,
    decode_capacitor_code, encode_capacitor_code,
    decode_capacitor_colors,
    capacitor_energy, capacitor_charge,
    rc_time_constant, capacitor_reactance, capacitive_impedance,
    parallel_capacitance, series_capacitance, capacitor_divider_voltage,
    capacitor_charge_voltage, capacitor_discharge_voltage, time_to_charge,
    get_capacitor_series, find_nearest_standard,
    supercap_backup_time, supercap_energy_density,
    ripple_current_rating, capacitor_power_loss,
    capacitor_lifetime,
    is_valid_capacitor_code, get_capacitor_info,
    E_SERIES, CAPACITANCE_UNITS,
)


class TestUnitConversion(unittest.TestCase):
    """Tests for capacitance unit conversion functions."""
    
    def test_convert_capacitance(self):
        """Test capacitance unit conversion."""
        # uF to nF
        result = convert_capacitance(1, "uF", "nF")
        self.assertAlmostEqual(result, 1000.0)
        
        # pF to nF
        result = convert_capacitance(1000, "pF", "nF")
        self.assertAlmostEqual(result, 1.0)
        
        # nF to uF
        result = convert_capacitance(100, "nF", "uF")
        self.assertAlmostEqual(result, 0.1)
        
        # F to uF
        result = convert_capacitance(1, "F", "uF")
        self.assertAlmostEqual(result, 1e6)
    
    def test_convert_with_unicode(self):
        """Test conversion with unicode symbols."""
        result = convert_capacitance(1, "µF", "uF")
        self.assertEqual(result, 1.0)
        
        result = convert_capacitance(1, "uF", "µF")
        self.assertEqual(result, 1.0)
    
    def test_format_capacitance(self):
        """Test capacitance formatting."""
        self.assertEqual(format_capacitance(1e-12), "1 pF")
        self.assertEqual(format_capacitance(1e-9), "1 nF")
        self.assertEqual(format_capacitance(1e-6), "1 uF")
        self.assertEqual(format_capacitance(1e-3), "1 mF")
        self.assertEqual(format_capacitance(1.0), "1 F")
        
        # Test with different values
        self.assertIn("pF", format_capacitance(47e-12))
        self.assertIn("nF", format_capacitance(100e-9))
        self.assertIn("uF", format_capacitance(4.7e-6))
    
    def test_parse_capacitance_string(self):
        """Test parsing capacitance strings."""
        self.assertAlmostEqual(parse_capacitance_string("100nF"), 100e-9)
        self.assertAlmostEqual(parse_capacitance_string("10uF"), 10e-6)
        self.assertAlmostEqual(parse_capacitance_string("1pF"), 1e-12)
        self.assertAlmostEqual(parse_capacitance_string("1F"), 1.0)
        
        # Test with unicode
        self.assertAlmostEqual(parse_capacitance_string("10µF"), 10e-6)


class TestCapacitorCodeDecoding(unittest.TestCase):
    """Tests for capacitor code decoding functions."""
    
    def test_decode_3digit_codes(self):
        """Test 3-digit capacitor code decoding."""
        # 104 = 10 * 10^4 pF = 100nF = 0.1uF
        result = decode_capacitor_code("104")
        self.assertEqual(result["code_type"], "3-digit")
        self.assertAlmostEqual(result["capacitance_farads"], 1e-7)
        self.assertIn("nF", result["capacitance_str"])
        
        # 103 = 10 * 10^3 pF = 10nF
        result = decode_capacitor_code("103")
        self.assertAlmostEqual(result["capacitance_farads"], 1e-8)
        
        # 475 = 47 * 10^5 pF = 4.7uF
        result = decode_capacitor_code("475")
        self.assertAlmostEqual(result["capacitance_farads"], 4.7e-6)
        
        # 106 = 10 * 10^6 pF = 10uF
        result = decode_capacitor_code("106")
        self.assertAlmostEqual(result["capacitance_farads"], 1e-5)
    
    def test_decode_4digit_codes(self):
        """Test 4-digit capacitor code decoding."""
        # 1000 = 100 * 10^0 pF = 100pF
        result = decode_capacitor_code("1000")
        self.assertEqual(result["code_type"], "4-digit")
        self.assertAlmostEqual(result["capacitance_farads"], 100e-12)
        
        # 4753 = 475 * 10^3 pF = 475nF
        result = decode_capacitor_code("4753")
        self.assertAlmostEqual(result["capacitance_farads"], 475e-9)
    
    def test_decode_r_notation(self):
        """Test R-notation capacitor code decoding."""
        # 4R7 = 4.7pF
        result = decode_capacitor_code("4R7")
        self.assertEqual(result["code_type"], "R-notation")
        self.assertAlmostEqual(result["capacitance_farads"], 4.7e-12)
        
        # R47 = 0.47pF
        result = decode_capacitor_code("R47")
        self.assertAlmostEqual(result["capacitance_farads"], 0.47e-12)
        
        # 2R2 = 2.2pF
        result = decode_capacitor_code("2R2")
        self.assertAlmostEqual(result["capacitance_farads"], 2.2e-12)
    
    def test_decode_unit_notation(self):
        """Test unit notation decoding."""
        result = decode_capacitor_code("100n")
        self.assertEqual(result["code_type"], "unit_notation")
        self.assertAlmostEqual(result["capacitance_farads"], 100e-9)
        
        result = decode_capacitor_code("10u")
        self.assertAlmostEqual(result["capacitance_farads"], 10e-6)
    
    def test_encode_capacitor_code(self):
        """Test capacitor code encoding."""
        # 100nF = 104
        code = encode_capacitor_code(1e-7)
        self.assertEqual(code, "104")
        
        # 10nF = 103
        code = encode_capacitor_code(1e-8)
        self.assertEqual(code, "103")
        
        # 1nF = 102
        code = encode_capacitor_code(1e-9)
        self.assertEqual(code, "102")
        
        # 4.7pF with R notation
        code = encode_capacitor_code(4.7e-12, "R-notation")
        self.assertEqual(code, "4R7")
    
    def test_encode_decode_symmetry(self):
        """Test encode/decode symmetry."""
        test_values = [1e-7, 1e-8, 4.7e-6, 1e-5, 2.2e-9]
        for value in test_values:
            code = encode_capacitor_code(value)
            decoded = decode_capacitor_code(code)
            # Allow some tolerance due to encoding
            self.assertAlmostEqual(decoded["capacitance_farads"], value, places=-1)


class TestCapacitorColorCodes(unittest.TestCase):
    """Tests for capacitor color code decoding."""
    
    def test_decode_3band_colors(self):
        """Test 3-band color decoding."""
        # Brown-Black-Orange = 10 * 1000 pF = 10nF
        result = decode_capacitor_colors(["brown", "black", "orange"])
        self.assertAlmostEqual(result["capacitance_farads"], 1e-8)
        self.assertIsNone(result["tolerance_percent"])
    
    def test_decode_4band_colors(self):
        """Test 4-band color decoding."""
        # Brown-Black-Red-White = 10 * 100 pF = 1nF, 10% tolerance
        result = decode_capacitor_colors(["brown", "black", "red", "white"])
        self.assertAlmostEqual(result["capacitance_farads"], 1e-9)
        self.assertEqual(result["tolerance_percent"], 10.0)
    
    def test_decode_5band_colors(self):
        """Test 5-band color decoding."""
        # Brown-Black-Yellow-Green-Green = 10 * 10000 pF = 100nF, 0.5%, 500V
        result = decode_capacitor_colors(["brown", "black", "yellow", "green", "green"])
        self.assertAlmostEqual(result["capacitance_farads"], 1e-7)
        self.assertEqual(result["tolerance_percent"], 0.5)
        self.assertEqual(result["voltage_rating"], 500)


class TestElectricalCalculations(unittest.TestCase):
    """Tests for electrical calculation functions."""
    
    def test_capacitor_energy(self):
        """Test energy calculation."""
        # 1uF at 10V: E = 0.5 * 1e-6 * 100 = 50uJ
        result = capacitor_energy(1e-6, 10)
        self.assertAlmostEqual(result["energy_joules"], 5e-5)
        
        # 1000uF at 5V: E = 0.5 * 0.001 * 25 = 12.5mJ
        result = capacitor_energy(1e-3, 5)
        self.assertAlmostEqual(result["energy_joules"], 0.0125)
    
    def test_capacitor_charge(self):
        """Test charge calculation."""
        # Q = C * V
        result = capacitor_charge(1e-6, 5)
        self.assertAlmostEqual(result, 5e-6)
        
        result = capacitor_charge(100e-6, 10)
        self.assertAlmostEqual(result, 1e-3)
    
    def test_rc_time_constant(self):
        """Test RC time constant calculation."""
        # 1kΩ, 1uF: tau = 1ms
        result = rc_time_constant(1000, 1e-6)
        self.assertAlmostEqual(result["tau_seconds"], 0.001)
        self.assertAlmostEqual(result["tau_ms"], 1.0)
        self.assertAlmostEqual(result["five_tau_seconds"], 0.005)
        
        # 10kΩ, 10uF: tau = 100ms
        result = rc_time_constant(10000, 1e-5)
        self.assertAlmostEqual(result["tau_ms"], 100.0)
    
    def test_capacitor_reactance(self):
        """Test capacitive reactance calculation."""
        # 1uF at 1kHz: Xc = 1/(2*pi*1000*1e-6) ≈ 159.15Ω
        result = capacitor_reactance(1e-6, 1000)
        self.assertAlmostEqual(result["reactance_ohms"], 159.1549, places=1)
        
        # 100uF at 50Hz: Xc ≈ 31.83Ω
        result = capacitor_reactance(1e-4, 50)
        self.assertAlmostEqual(result["reactance_ohms"], 31.831, places=1)
        
        # At DC (0Hz): infinite reactance
        result = capacitor_reactance(1e-6, 0)
        self.assertEqual(result["reactance_ohms"], float("inf"))
    
    def test_capacitive_impedance(self):
        """Test complex impedance calculation."""
        z = capacitive_impedance(1e-6, 1000)
        self.assertEqual(z.real, 0)
        self.assertAlmostEqual(abs(z), 159.1549, places=1)


class TestSeriesParallel(unittest.TestCase):
    """Tests for series and parallel capacitor calculations."""
    
    def test_parallel_capacitance(self):
        """Test parallel capacitance calculation."""
        # C_total = C1 + C2 + C3
        result = parallel_capacitance([1e-6, 1e-6, 1e-6])
        self.assertEqual(result, 3e-6)
        
        result = parallel_capacitance([1e-6, 2e-6, 3e-6])
        self.assertEqual(result, 6e-6)
    
    def test_series_capacitance(self):
        """Test series capacitance calculation."""
        # 1/C_total = 1/C1 + 1/C2
        result = series_capacitance([1e-6, 1e-6])
        self.assertEqual(result, 5e-7)  # 0.5uF
        
        # Two equal caps in series = half
        result = series_capacitance([2e-6, 2e-6])
        self.assertEqual(result, 1e-6)
    
    def test_capacitor_divider(self):
        """Test capacitive voltage divider."""
        # Equal capacitors: Vout = Vin/2
        result = capacitor_divider_voltage(1e-6, 1e-6, 10)
        self.assertEqual(result["vout"], 5.0)
        
        # C1=2uF, C2=1uF: Vout = Vin * C1/(C1+C2) = 10 * 2/3 ≈ 6.67
        result = capacitor_divider_voltage(2e-6, 1e-6, 10)
        self.assertAlmostEqual(result["vout"], 6.667, places=2)


class TestChargeDischarge(unittest.TestCase):
    """Tests for capacitor charge/discharge calculations."""
    
    def test_capacitor_charge_voltage(self):
        """Test charging voltage calculation."""
        # After 1 tau, voltage should be ~63.2% of target
        v = capacitor_charge_voltage(1e-6, 1000, 0, 5, 0.001)
        self.assertAlmostEqual(v, 3.16, places=2)  # 5 * 0.632
        
        # After 5 tau, voltage should be ~99.3% of target
        v = capacitor_charge_voltage(1e-6, 1000, 0, 5, 0.005)
        self.assertAlmostEqual(v, 4.97, places=2)
    
    def test_capacitor_discharge_voltage(self):
        """Test discharge voltage calculation."""
        # After 1 tau, voltage should be ~36.8% of initial
        v = capacitor_discharge_voltage(1e-6, 1000, 5, 0.001)
        self.assertAlmostEqual(v, 1.84, places=2)  # 5 * 0.368
        
        # After 5 tau, voltage should be ~0.7% of initial
        v = capacitor_discharge_voltage(1e-6, 1000, 5, 0.005)
        self.assertAlmostEqual(v, 0.034, places=2)
    
    def test_time_to_charge(self):
        """Test time to charge calculation."""
        # Time to 63.2% (1 tau) for 1kΩ, 1uF
        t = time_to_charge(1e-6, 1000, 63.2)
        self.assertAlmostEqual(t, 0.001, places=4)
        
        # Time to 99.3% (5 tau)
        t = time_to_charge(1e-6, 1000, 99.3)
        self.assertAlmostEqual(t, 0.005, places=4)


class TestESeries(unittest.TestCase):
    """Tests for E-series standard values."""
    
    def test_get_capacitor_series(self):
        """Test E-series retrieval."""
        e6 = get_capacitor_series("E6")
        self.assertEqual(len(e6), 6)
        self.assertIn(10, e6)
        self.assertIn(47, e6)
        
        e12 = get_capacitor_series("E12")
        self.assertEqual(len(e12), 12)
        
        e24 = get_capacitor_series("E24")
        self.assertEqual(len(e24), 24)
    
    def test_find_nearest_standard(self):
        """Test finding nearest standard value."""
        # 8.5uF should map to 8.2uF in E12
        result = find_nearest_standard(8.5e-6, "E12")
        self.assertIn("8.2", result["nearest_str"])
        
        # 10uF is a standard value
        result = find_nearest_standard(1e-5, "E12")
        self.assertIn("10", result["nearest_str"])
    
    def test_invalid_series(self):
        """Test invalid E-series."""
        with self.assertRaises(ValueError):
            get_capacitor_series("E99")


class TestSupercapacitor(unittest.TestCase):
    """Tests for supercapacitor calculations."""
    
    def test_supercap_backup_time(self):
        """Test backup time calculation."""
        # 1F, 5V to 3V at 1mA: t = 1 * (5-3) / 0.001 = 2000s
        result = supercap_backup_time(1.0, 5.0, 3.0, 0.001)
        self.assertEqual(result["time_seconds"], 2000.0)
        self.assertAlmostEqual(result["time_minutes"], 33.33, places=2)
    
    def test_supercap_energy_density(self):
        """Test energy density calculation."""
        # 100F, 2.7V, 50g
        result = supercap_energy_density(100, 2.7, weight_kg=0.05)
        # E = 0.5 * 100 * 2.7^2 = 364.5J = 0.10125Wh
        # Specific energy = 0.10125 / 0.05 = 2.025 Wh/kg
        self.assertAlmostEqual(result["specific_energy_wh_kg"], 2.025, places=2)


class TestRippleCurrent(unittest.TestCase):
    """Tests for ripple current calculations."""
    
    def test_ripple_current_rating(self):
        """Test ripple current rating calculation."""
        result = ripple_current_rating(100e-6, 100000, 0.1)
        # Max power = 10/20 = 0.5W
        # Max ripple = sqrt(0.5/0.1) = sqrt(5) ≈ 2.24A
        self.assertAlmostEqual(result["max_ripple_current_arms"], 2.236, places=2)
    
    def test_capacitor_power_loss(self):
        """Test power loss calculation."""
        result = capacitor_power_loss(100e-6, 0.5, 100000, 0.1)
        # Should return positive power loss
        self.assertGreater(result["power_loss_w"], 0)


class TestCapacitorLifetime(unittest.TestCase):
    """Tests for lifetime estimation."""
    
    def test_capacitor_lifetime(self):
        """Test lifetime calculation."""
        # 2000h @ 105°C, operating at 65°C
        # Expected: much longer lifetime
        result = capacitor_lifetime(2000, 105, 65)
        self.assertGreater(result["estimated_hours"], 2000)
        
        # Higher temp should reduce lifetime
        result_hot = capacitor_lifetime(2000, 105, 85)
        result_cool = capacitor_lifetime(2000, 105, 65)
        self.assertGreater(result_cool["estimated_hours"], result_hot["estimated_hours"])
    
    def test_lifetime_voltage_factor(self):
        """Test voltage effect on lifetime."""
        # Lower voltage should extend lifetime
        result_80 = capacitor_lifetime(2000, 105, 85, 0.8)
        result_100 = capacitor_lifetime(2000, 105, 85, 1.0)
        self.assertGreater(result_80["estimated_hours"], result_100["estimated_hours"])


class TestUtilityFunctions(unittest.TestCase):
    """Tests for utility functions."""
    
    def test_is_valid_capacitor_code(self):
        """Test code validation."""
        self.assertTrue(is_valid_capacitor_code("104"))
        self.assertTrue(is_valid_capacitor_code("4R7"))
        self.assertTrue(is_valid_capacitor_code("100n"))
        self.assertFalse(is_valid_capacitor_code("invalid"))
    
    def test_get_capacitor_info(self):
        """Test capacitance info."""
        info = get_capacitor_info(1e-6)
        self.assertEqual(info["farads"], 1e-6)
        self.assertAlmostEqual(info["picofarads"], 1e6)
        self.assertAlmostEqual(info["nanofarads"], 1000)
        self.assertAlmostEqual(info["microfarads"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)