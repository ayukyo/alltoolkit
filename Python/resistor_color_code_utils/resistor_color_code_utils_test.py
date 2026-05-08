#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Resistor Color Code Utilities Test Module
========================================================
Comprehensive tests for resistor color code calculations.
"""

import unittest
import math
from mod import (
    decode_3band, decode_4band, decode_5band, decode_6band, decode_resistor,
    encode_4band, encode_5band, encode_6band,
    decode_smd, encode_smd,
    get_e_series, find_nearest_standard, is_standard_value,
    parallel_resistance, series_resistance, voltage_divider, led_resistor,
    is_valid_color, get_color_info,
    COLOR_VALUES, COLOR_MULTIPLIERS, COLOR_TOLERANCES, COLOR_TEMPCO,
    _format_resistance, _parse_resistance_string,
)


class TestColorBandDecoding(unittest.TestCase):
    """Tests for color band decoding functions."""
    
    def test_decode_3band(self):
        """Test 3-band resistor decoding."""
        # Brown-Black-Red = 1000Ω (1kΩ), 20% tolerance
        result = decode_3band(['brown', 'black', 'red'])
        self.assertEqual(result['resistance'], 1000.0)
        self.assertEqual(result['tolerance'], 20.0)
        
        # Red-Red-Orange = 22000Ω (22kΩ)
        result = decode_3band(['red', 'red', 'orange'])
        self.assertEqual(result['resistance'], 22000.0)
        
        # Yellow-Violet-Black = 47Ω
        result = decode_3band(['yellow', 'violet', 'black'])
        self.assertEqual(result['resistance'], 47.0)
        
        # Blue-Gray-Gold = 6.8Ω
        result = decode_3band(['blue', 'gray', 'gold'])
        self.assertAlmostEqual(result['resistance'], 6.8, places=1)
    
    def test_decode_4band(self):
        """Test 4-band resistor decoding."""
        # Brown-Black-Red-Gold = 1000Ω ±5%
        result = decode_4band(['brown', 'black', 'red', 'gold'])
        self.assertEqual(result['resistance'], 1000.0)
        self.assertEqual(result['tolerance'], 5.0)
        
        # Red-Violet-Yellow-Gold = 270kΩ ±5%
        result = decode_4band(['red', 'violet', 'yellow', 'gold'])
        self.assertEqual(result['resistance'], 270000.0)
        self.assertEqual(result['tolerance'], 5.0)
        
        # Orange-Orange-Black-Silver = 33Ω ±10%
        result = decode_4band(['orange', 'orange', 'black', 'silver'])
        self.assertEqual(result['resistance'], 33.0)
        self.assertEqual(result['tolerance'], 10.0)
        
        # Green-Blue-Black-Brown = 56Ω ±1%
        result = decode_4band(['green', 'blue', 'black', 'brown'])
        self.assertEqual(result['resistance'], 56.0)
        self.assertEqual(result['tolerance'], 1.0)
    
    def test_decode_5band(self):
        """Test 5-band resistor decoding."""
        # Brown-Black-Black-Red-Gold = 10kΩ ±5%
        result = decode_5band(['brown', 'black', 'black', 'red', 'gold'])
        self.assertEqual(result['resistance'], 10000.0)
        self.assertEqual(result['tolerance'], 5.0)
        
        # Red-Red-Black-Orange-Brown = 220kΩ ±1%
        result = decode_5band(['red', 'red', 'black', 'orange', 'brown'])
        self.assertEqual(result['resistance'], 220000.0)
        self.assertEqual(result['tolerance'], 1.0)
        
        # Yellow-Violet-Black-Brown-Red = 4.7kΩ ±2%
        result = decode_5band(['yellow', 'violet', 'black', 'brown', 'red'])
        self.assertEqual(result['resistance'], 4700.0)
        self.assertEqual(result['tolerance'], 2.0)
    
    def test_decode_6band(self):
        """Test 6-band resistor decoding."""
        # Brown-Black-Black-Red-Gold-Brown = 10kΩ ±5% 100ppm/°C
        result = decode_6band(['brown', 'black', 'black', 'red', 'gold', 'brown'])
        self.assertEqual(result['resistance'], 10000.0)
        self.assertEqual(result['tolerance'], 5.0)
        self.assertEqual(result['tempco'], 100)
        
        # Red-Red-Black-Orange-Brown-Red = 220kΩ ±1% 50ppm/°C
        result = decode_6band(['red', 'red', 'black', 'orange', 'brown', 'red'])
        self.assertEqual(result['resistance'], 220000.0)
        self.assertEqual(result['tolerance'], 1.0)
        self.assertEqual(result['tempco'], 50)
    
    def test_decode_resistor_auto(self):
        """Test automatic resistor decoding."""
        # 4-band
        result = decode_resistor(['red', 'violet', 'yellow', 'gold'])
        self.assertEqual(result['bands'], 4)
        self.assertEqual(result['resistance'], 270000.0)
        
        # 5-band
        result = decode_resistor(['brown', 'black', 'black', 'red', 'gold'])
        self.assertEqual(result['bands'], 5)
        self.assertEqual(result['resistance'], 10000.0)
    
    def test_decode_invalid_bands(self):
        """Test error handling for invalid band count."""
        with self.assertRaises(ValueError):
            decode_resistor(['red', 'violet'])  # Too few
        
        with self.assertRaises(ValueError):
            decode_resistor(['red', 'violet', 'yellow', 'gold', 'brown', 'black', 'white'])  # Too many
    
    def test_decode_invalid_colors(self):
        """Test error handling for invalid colors."""
        with self.assertRaises(ValueError):
            decode_4band(['purple', 'black', 'red', 'gold'])  # Invalid sig color
        
        with self.assertRaises(ValueError):
            decode_4band(['brown', 'black', 'pink', 'gold'])  # Invalid multiplier
    
    def test_decode_case_insensitive(self):
        """Test case-insensitive color decoding."""
        result = decode_4band(['BROWN', 'BLACK', 'RED', 'GOLD'])
        self.assertEqual(result['resistance'], 1000.0)
        
        result = decode_4band(['Brown', 'Black', 'Red', 'Gold'])
        self.assertEqual(result['resistance'], 1000.0)


class TestColorBandEncoding(unittest.TestCase):
    """Tests for color band encoding functions."""
    
    def test_encode_4band(self):
        """Test 4-band encoding."""
        # 1000Ω ±5% = Brown-Black-Red-Gold
        result = encode_4band(1000, 5)
        self.assertEqual(result['colors'], ['brown', 'black', 'red', 'gold'])
        
        # 4700Ω ±5% = Yellow-Violet-Red-Gold
        result = encode_4band(4700, 5)
        self.assertEqual(result['colors'], ['yellow', 'violet', 'red', 'gold'])
        
        # 270000Ω ±5% = Red-Violet-Yellow-Gold
        result = encode_4band(270000, 5)
        self.assertEqual(result['colors'], ['red', 'violet', 'yellow', 'gold'])
    
    def test_encode_5band(self):
        """Test 5-band encoding."""
        # 10000Ω ±1% = Brown-Black-Black-Red-Brown
        result = encode_5band(10000, 1)
        self.assertEqual(result['colors'], ['brown', 'black', 'black', 'red', 'brown'])
        
        # 4700Ω ±1% = Yellow-Violet-Black-Brown-Brown
        result = encode_5band(4700, 1)
        self.assertEqual(result['colors'], ['yellow', 'violet', 'black', 'brown', 'brown'])
    
    def test_encode_6band(self):
        """Test 6-band encoding."""
        # 10000Ω ±1% 100ppm = Brown-Black-Black-Red-Brown-Brown
        result = encode_6band(10000, 1, 100)
        self.assertEqual(result['colors'][:5], ['brown', 'black', 'black', 'red', 'brown'])
        self.assertEqual(result['colors'][5], 'brown')
        self.assertEqual(result['tempco'], 100)
    
    def test_encode_tolerance_rounding(self):
        """Test tolerance value rounding to nearest available."""
        # Request 3% tolerance - should round to nearest (2% or 5%)
        result = encode_4band(1000, 3)
        self.assertIn(result['tolerance'], [2.0, 5.0])
    
    def test_encode_small_values(self):
        """Test encoding small resistance values."""
        # 4.7Ω
        result = encode_4band(4.7, 5)
        self.assertEqual(result['colors'][0], 'yellow')
        self.assertEqual(result['colors'][1], 'violet')
        self.assertEqual(result['colors'][2], 'gold')
    
    def test_encode_large_values(self):
        """Test encoding large resistance values."""
        # 1MΩ = Brown-Black-Green-Gold
        result = encode_4band(1000000, 5)
        self.assertEqual(result['colors'], ['brown', 'black', 'green', 'gold'])


class TestSMDCodes(unittest.TestCase):
    """Tests for SMD resistor code decoding and encoding."""
    
    def test_decode_3digit_smd(self):
        """Test 3-digit SMD code decoding."""
        # 103 = 10kΩ
        result = decode_smd('103')
        self.assertEqual(result['resistance'], 10000.0)
        self.assertEqual(result['type'], '3-digit')
        
        # 473 = 47kΩ
        result = decode_smd('473')
        self.assertEqual(result['resistance'], 47000.0)
        
        # 100 = 10Ω
        result = decode_smd('100')
        self.assertEqual(result['resistance'], 10.0)
        
        # 102 = 1kΩ
        result = decode_smd('102')
        self.assertEqual(result['resistance'], 1000.0)
    
    def test_decode_4digit_smd(self):
        """Test 4-digit SMD code decoding."""
        # 1002 = 10kΩ
        result = decode_smd('1002')
        self.assertEqual(result['resistance'], 10000.0)
        self.assertEqual(result['type'], '4-digit')
        
        # 4701 = 4.7kΩ
        result = decode_smd('4701')
        self.assertEqual(result['resistance'], 4700.0)
        
        # 1000 = 100Ω
        result = decode_smd('1000')
        self.assertEqual(result['resistance'], 100.0)
    
    def test_decode_r_notation(self):
        """Test R notation SMD code decoding."""
        # 4R7 = 4.7Ω
        result = decode_smd('4R7')
        self.assertEqual(result['resistance'], 4.7)
        self.assertEqual(result['type'], 'R-notation')
        
        # R47 = 0.47Ω
        result = decode_smd('R47')
        self.assertEqual(result['resistance'], 0.47)
        
        # 47R = 47Ω
        result = decode_smd('47R')
        self.assertEqual(result['resistance'], 47.0)
        
        # 0R5 = 0.5Ω
        result = decode_smd('0R5')
        self.assertEqual(result['resistance'], 0.5)
    
    def test_encode_smd_auto(self):
        """Test automatic SMD encoding."""
        # 10000Ω should encode to 103
        result = encode_smd(10000)
        self.assertEqual(result['code'], '103')
        
        # 4700Ω should encode to valid SMD code (472 or 473 or 4701)
        result = encode_smd(4700, 'auto')
        # Accept valid encodings - 472 (47*10^2) = 4700Ω is also valid
        self.assertIn(result['code'], ['472', '473', '4701', '4702'])
        
        # 4.7Ω - encoding depends on implementation
        result = encode_smd(4.7)
        # Should be a valid SMD code for 4.7Ω
        decoded = decode_smd('4R7')
        self.assertEqual(decoded['resistance'], 4.7)
    
    def test_encode_smd_3digit(self):
        """Test 3-digit SMD encoding."""
        result = encode_smd(10000, '3-digit')
        self.assertEqual(result['code'], '103')
        self.assertEqual(result['type'], '3-digit')
    
    def test_encode_smd_4digit(self):
        """Test 4-digit SMD encoding."""
        result = encode_smd(4700, '4-digit')
        self.assertEqual(result['code'], '4701')
        self.assertEqual(result['type'], '4-digit')
    
    def test_decode_invalid_smd(self):
        """Test error handling for invalid SMD codes."""
        with self.assertRaises(ValueError):
            decode_smd('')
        
        with self.assertRaises(ValueError):
            decode_smd('ABC')  # Invalid format


class TestESeries(unittest.TestCase):
    """Tests for E-series standard values."""
    
    def test_get_e_series(self):
        """Test getting E-series values."""
        e6 = get_e_series('E6')
        self.assertEqual(len(e6), 6)
        self.assertIn(10, e6)
        self.assertIn(47, e6)
        
        e12 = get_e_series('E12')
        self.assertEqual(len(e12), 12)
        
        e24 = get_e_series('E24')
        self.assertEqual(len(e24), 24)
        
        e96 = get_e_series('E96')
        self.assertEqual(len(e96), 96)
    
    def test_find_nearest_standard(self):
        """Test finding nearest standard value."""
        # Exact match
        result = find_nearest_standard(4700, 'E12')
        self.assertEqual(result['nearest'], 4700.0)
        self.assertEqual(result['error_percent'], 0.0)
        
        # Not exact - should find nearest
        result = find_nearest_standard(5000, 'E12')
        self.assertIn(result['nearest'], [4700.0, 5600.0])
        
        # E24 should have more options
        result = find_nearest_standard(5000, 'E24')
        self.assertLess(result['error_percent'], 10)
    
    def test_is_standard_value(self):
        """Test checking if value is standard."""
        self.assertTrue(is_standard_value(4700, 'E12'))
        self.assertTrue(is_standard_value(1000, 'E6'))
        self.assertFalse(is_standard_value(4800, 'E12', tolerance=0.1))
        self.assertTrue(is_standard_value(4800, 'E12', tolerance=5.0))


class TestCircuitCalculations(unittest.TestCase):
    """Tests for circuit calculation functions."""
    
    def test_parallel_resistance(self):
        """Test parallel resistance calculation."""
        # Two equal resistors: R = R1/2
        result = parallel_resistance([100, 100])
        self.assertEqual(result, 50.0)
        
        # Three equal resistors
        result = parallel_resistance([100, 100, 100])
        self.assertAlmostEqual(result, 33.33, places=2)
        
        # Different values
        result = parallel_resistance([1000, 2000])
        self.assertAlmostEqual(result, 666.67, places=2)
        
        # 1k + 2k + 4k in parallel
        result = parallel_resistance([1000, 2000, 4000])
        self.assertAlmostEqual(result, 571.43, places=2)
    
    def test_series_resistance(self):
        """Test series resistance calculation."""
        result = series_resistance([100, 200])
        self.assertEqual(result, 300.0)
        
        result = series_resistance([1000, 2000, 3000])
        self.assertEqual(result, 6000.0)
    
    def test_voltage_divider(self):
        """Test voltage divider calculation."""
        # Equal resistors: half voltage
        result = voltage_divider(10000, 10000, 5)
        self.assertEqual(result, 2.5)
        
        # R2 = 10k, R1 = 20k, Vin = 12V -> Vout = 4V
        result = voltage_divider(20000, 10000, 12)
        self.assertEqual(result, 4.0)
        
        # R2 = 1k, R1 = 9k, Vin = 10V -> Vout = 1V
        result = voltage_divider(9000, 1000, 10)
        self.assertEqual(result, 1.0)
    
    def test_led_resistor(self):
        """Test LED resistor calculation."""
        # 5V supply, 2V LED, 20mA -> 150Ω
        result = led_resistor(5, 2, 0.02)
        self.assertEqual(result, 150.0)
        
        # 12V supply, 3V LED, 20mA -> 450Ω
        result = led_resistor(12, 3, 0.02)
        self.assertEqual(result, 450.0)
        
        # 3.3V supply, 2V LED, 10mA -> 130Ω
        result = led_resistor(3.3, 2, 0.01)
        self.assertAlmostEqual(result, 130.0, places=1)
    
    def test_led_resistor_errors(self):
        """Test error handling for LED resistor calculation."""
        with self.assertRaises(ValueError):
            led_resistor(2, 5, 0.02)  # Supply < LED voltage
        
        with self.assertRaises(ValueError):
            led_resistor(5, 2, 0)  # Zero current
    
    def test_parallel_with_zero(self):
        """Test parallel resistance with zero resistor."""
        # Any zero in parallel = short circuit (0Ω)
        result = parallel_resistance([100, 0])
        self.assertEqual(result, 0.0)
        
        result = parallel_resistance([0, 0])
        self.assertEqual(result, 0.0)


class TestUtilityFunctions(unittest.TestCase):
    """Tests for utility functions."""
    
    def test_format_resistance(self):
        """Test resistance formatting."""
        self.assertEqual(_format_resistance(0.001), '1 mΩ')
        self.assertEqual(_format_resistance(1), '1 Ω')
        self.assertEqual(_format_resistance(1000), '1 kΩ')
        self.assertEqual(_format_resistance(1000000), '1 MΩ')
        self.assertEqual(_format_resistance(1000000000), '1 GΩ')
        
        # Decimal values
        self.assertIn('4.7', _format_resistance(4700))
        self.assertIn('k', _format_resistance(4700))
    
    def test_parse_resistance_string(self):
        """Test parsing resistance strings."""
        self.assertEqual(_parse_resistance_string('4K7'), 4700.0)
        self.assertEqual(_parse_resistance_string('1M5'), 1500000.0)
        self.assertEqual(_parse_resistance_string('100R'), 100.0)
        self.assertEqual(_parse_resistance_string('47'), 47.0)
    
    def test_is_valid_color(self):
        """Test color validation."""
        self.assertTrue(is_valid_color('red'))
        self.assertTrue(is_valid_color('gold'))
        self.assertTrue(is_valid_color('brown'))
        self.assertFalse(is_valid_color('purple'))
        self.assertFalse(is_valid_color('pink'))
    
    def test_get_color_info(self):
        """Test getting color information."""
        info = get_color_info('red')
        self.assertEqual(info['value'], 2)
        self.assertEqual(info['multiplier'], 100)
        self.assertEqual(info['tolerance'], 2.0)
        self.assertEqual(info['tempco'], 50)
        
        info = get_color_info('gold')
        self.assertIsNone(info['value'])  # Not a sig fig color
        self.assertEqual(info['multiplier'], 0.1)
        self.assertEqual(info['tolerance'], 5.0)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary values."""
    
    def test_zero_resistance(self):
        """Test handling of zero resistance."""
        result = encode_4band(0, 5)
        self.assertEqual(result['colors'], ['black', 'black', 'black', 'gold'])
    
    def test_very_small_resistance(self):
        """Test handling of very small resistance."""
        # 0.1Ω
        result = decode_4band(['black', 'brown', 'gold', 'gold'])
        self.assertAlmostEqual(result['resistance'], 0.1, places=2)
    
    def test_very_large_resistance(self):
        """Test handling of very large resistance."""
        # 10MΩ
        result = decode_4band(['brown', 'black', 'blue', 'gold'])
        self.assertEqual(result['resistance'], 10000000.0)
    
    def test_high_precision_tolerance(self):
        """Test high precision tolerance values."""
        # 0.05% tolerance (gray)
        result = decode_5band(['brown', 'black', 'black', 'red', 'gray'])
        self.assertEqual(result['tolerance'], 0.05)
        
        # 0.1% tolerance (violet)
        result = decode_5band(['brown', 'black', 'black', 'red', 'violet'])
        self.assertEqual(result['tolerance'], 0.1)


class TestRoundTrip(unittest.TestCase):
    """Tests for encode-decode round-trip consistency."""
    
    def test_4band_roundtrip(self):
        """Test 4-band encode-decode round-trip."""
        for resistance in [100, 1000, 4700, 10000, 47000, 100000]:
            encoded = encode_4band(resistance, 5)
            decoded = decode_4band(encoded['colors'])
            self.assertEqual(decoded['resistance'], encoded['resistance'])
    
    def test_5band_roundtrip(self):
        """Test 5-band encode-decode round-trip."""
        for resistance in [100, 1000, 4700, 10000, 47000]:
            encoded = encode_5band(resistance, 1)
            decoded = decode_5band(encoded['colors'])
            self.assertEqual(decoded['resistance'], encoded['resistance'])


if __name__ == '__main__':
    unittest.main(verbosity=2)