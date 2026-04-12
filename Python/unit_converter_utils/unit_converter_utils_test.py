#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Unit Converter Utilities Test Suite
=================================================
Comprehensive test suite for the unit converter module.

Run with: python unit_converter_utils_test.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    convert_length, convert_weight, convert_temperature,
    convert_volume, convert_area, convert_speed,
    convert_time, convert_data, convert_pressure,
    convert_energy, convert_power,
    convert, format_conversion,
    get_available_units, get_unit_info,
    # Length shortcuts
    meters_to_feet, feet_to_meters, kilometers_to_miles,
    miles_to_kilometers, inches_to_centimeters, centimeters_to_inches,
    # Weight shortcuts
    kg_to_pounds, pounds_to_kg, grams_to_ounces, ounces_to_grams,
    # Temperature shortcuts
    celsius_to_fahrenheit, fahrenheit_to_celsius, celsius_to_kelvin,
    kelvin_to_celsius, fahrenheit_to_kelvin, kelvin_to_fahrenheit,
    # Volume shortcuts
    liters_to_gallons, gallons_to_liters,
    # Area shortcuts
    square_meters_to_square_feet, square_feet_to_square_meters,
    acres_to_hectares, hectares_to_acres,
    # Speed shortcuts
    kmh_to_mph, mph_to_kmh, ms_to_kmh, knots_to_kmh,
    # Time shortcuts
    hours_to_minutes, minutes_to_seconds, days_to_hours,
    weeks_to_days, years_to_days,
    # Data shortcuts
    gb_to_mb, gib_to_mib, tb_to_gb, bytes_to_bits, bits_to_bytes,
    # Pressure shortcuts
    atm_to_pascal, psi_to_bar, bar_to_psi,
    # Energy shortcuts
    kwh_to_joules, calories_to_joules, btu_to_kwh,
    # Power shortcuts
    hp_to_kw, kw_to_hp, mw_to_kw,
    # Batch conversions
    batch_convert_length, batch_convert_weight, batch_convert_temperature,
)


# ============================================================================
# Test Framework
# ============================================================================

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, name: str):
        self.passed += 1
        print(f"  ✓ {name}")
    
    def add_fail(self, name: str, expected: any, actual: any):
        self.failed += 1
        self.errors.append((name, expected, actual))
        print(f"  ✗ {name}")
        print(f"    Expected: {expected}")
        print(f"    Actual:   {actual}")
    
    def add_error(self, name: str, error: str):
        self.failed += 1
        self.errors.append((name, "no error", error))
        print(f"  ✗ {name}")
        print(f"    Error: {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Results: {self.passed}/{total} tests passed")
        if self.failed > 0:
            print(f"FAILED: {self.failed} tests")
            return False
        else:
            print("SUCCESS: All tests passed!")
            return True


result = TestResult()


def assert_almost_equal(name: str, actual: float, expected: float, tolerance: float = 1e-6):
    """Assert that two floats are approximately equal."""
    if abs(actual - expected) <= tolerance:
        result.add_pass(name)
    else:
        result.add_fail(name, expected, actual)


def assert_equal(name: str, actual: any, expected: any):
    """Assert that two values are equal."""
    if actual == expected:
        result.add_pass(name)
    else:
        result.add_fail(name, expected, actual)


def assert_error(name: str, func, *args, expected_error: type = ValueError):
    """Assert that a function raises an error."""
    try:
        func(*args)
        result.add_fail(name, f"raises {expected_error.__name__}", "no error")
    except expected_error as e:
        result.add_pass(name)
    except Exception as e:
        result.add_fail(name, f"raises {expected_error.__name__}", f"raises {type(e).__name__}: {e}")


# ============================================================================
# Length Conversion Tests
# ============================================================================

def test_length_conversions():
    print("\n[Length Conversions]")
    
    # Basic conversions
    assert_almost_equal("1 km to m", convert_length(1, 'km', 'm'), 1000.0)
    assert_almost_equal("1 m to cm", convert_length(1, 'm', 'cm'), 100.0)
    assert_almost_equal("1 cm to mm", convert_length(1, 'cm', 'mm'), 10.0)
    
    # Imperial conversions
    assert_almost_equal("1 ft to in", convert_length(1, 'ft', 'in'), 12.0)
    assert_almost_equal("1 yd to ft", convert_length(1, 'yd', 'ft'), 3.0)
    assert_almost_equal("1 mi to ft", convert_length(1, 'mi', 'ft'), 5280.0)
    
    # Cross-system conversions
    assert_almost_equal("1 in to cm", convert_length(1, 'in', 'cm'), 2.54)
    assert_almost_equal("1 ft to m", convert_length(1, 'ft', 'm'), 0.3048)
    assert_almost_equal("1 mi to km", convert_length(1, 'mi', 'km'), 1.609344)
    
    # Nautical
    assert_almost_equal("1 nmi to m", convert_length(1, 'nmi', 'm'), 1852.0)
    
    # Small units
    assert_almost_equal("1 m to mm", convert_length(1, 'm', 'mm'), 1000.0)
    assert_almost_equal("1 m to μm", convert_length(1, 'm', 'μm'), 1e6)
    assert_almost_equal("1 m to nm", convert_length(1, 'm', 'nm'), 1e9)
    
    # Round-trip conversions
    assert_almost_equal("1 km -> mi -> km", 
                        convert_length(convert_length(1, 'km', 'mi'), 'mi', 'km'), 
                        1.0, tolerance=1e-10)


def test_length_shortcuts():
    print("\n[Length Shortcuts]")
    
    assert_almost_equal("meters_to_feet(1)", meters_to_feet(1), 3.280839895013123)
    assert_almost_equal("feet_to_meters(1)", feet_to_meters(1), 0.3048)
    assert_almost_equal("kilometers_to_miles(1)", kilometers_to_miles(1), 0.6213711922373339)
    assert_almost_equal("miles_to_kilometers(1)", miles_to_kilometers(1), 1.609344)
    assert_almost_equal("inches_to_centimeters(1)", inches_to_centimeters(1), 2.54)
    assert_almost_equal("centimeters_to_inches(1)", centimeters_to_inches(1), 0.3937007874015748)


def test_length_edge_cases():
    print("\n[Length Edge Cases]")
    
    # Zero
    assert_almost_equal("0 m to km", convert_length(0, 'm', 'km'), 0.0)
    
    # Large values
    assert_almost_equal("1000 km to m", convert_length(1000, 'km', 'm'), 1e6)
    
    # Small values
    assert_almost_equal("0.001 m to mm", convert_length(0.001, 'm', 'mm'), 1.0)
    
    # Invalid unit
    assert_error("invalid length unit", convert_length, 1, 'invalid', 'm')


# ============================================================================
# Weight Conversion Tests
# ============================================================================

def test_weight_conversions():
    print("\n[Weight Conversions]")
    
    # Metric
    assert_almost_equal("1 kg to g", convert_weight(1, 'kg', 'g'), 1000.0)
    assert_almost_equal("1 g to mg", convert_weight(1, 'g', 'mg'), 1000.0)
    assert_almost_equal("1 kg to mg", convert_weight(1, 'kg', 'mg'), 1e6)
    
    # Imperial
    assert_almost_equal("1 lb to oz", convert_weight(1, 'lb', 'oz'), 16.0)
    
    # Cross-system
    assert_almost_equal("1 kg to lb", convert_weight(1, 'kg', 'lb'), 2.2046226218487757)
    assert_almost_equal("1 lb to kg", convert_weight(1, 'lb', 'kg'), 0.45359237)
    
    # Tons
    assert_almost_equal("1 metric ton to kg", convert_weight(1, 't', 'kg'), 1000.0)
    assert_almost_equal("1 US ton to kg", convert_weight(1, 'ton', 'kg'), 907.18474)
    
    # Stone
    assert_almost_equal("1 stone to kg", convert_weight(1, 'st', 'kg'), 6.35029318)
    
    # Round-trip
    assert_almost_equal("1 kg -> lb -> kg", 
                        convert_weight(convert_weight(1, 'kg', 'lb'), 'lb', 'kg'), 
                        1.0, tolerance=1e-10)


def test_weight_shortcuts():
    print("\n[Weight Shortcuts]")
    
    assert_almost_equal("kg_to_pounds(1)", kg_to_pounds(1), 2.2046226218487757)
    assert_almost_equal("pounds_to_kg(1)", pounds_to_kg(1), 0.45359237)
    assert_almost_equal("grams_to_ounces(1)", grams_to_ounces(1), 0.03527396194958041)
    assert_almost_equal("ounces_to_grams(1)", ounces_to_grams(1), 28.349523125)


def test_weight_edge_cases():
    print("\n[Weight Edge Cases]")
    
    # Zero
    assert_almost_equal("0 kg to g", convert_weight(0, 'kg', 'g'), 0.0)
    
    # Negative should fail
    assert_error("negative weight", convert_weight, -1, 'kg', 'g')
    
    # Invalid unit
    assert_error("invalid weight unit", convert_weight, 1, 'invalid', 'kg')


# ============================================================================
# Temperature Conversion Tests
# ============================================================================

def test_temperature_conversions():
    print("\n[Temperature Conversions]")
    
    # Celsius to Fahrenheit
    assert_almost_equal("0°C to °F", convert_temperature(0, 'C', 'F'), 32.0)
    assert_almost_equal("100°C to °F", convert_temperature(100, 'C', 'F'), 212.0)
    assert_almost_equal("-40°C to °F", convert_temperature(-40, 'C', 'F'), -40.0)
    
    # Fahrenheit to Celsius
    assert_almost_equal("32°F to °C", convert_temperature(32, 'F', 'C'), 0.0)
    assert_almost_equal("212°F to °C", convert_temperature(212, 'F', 'C'), 100.0)
    assert_almost_equal("-40°F to °C", convert_temperature(-40, 'F', 'C'), -40.0)
    
    # Celsius to Kelvin
    assert_almost_equal("0°C to K", convert_temperature(0, 'C', 'K'), 273.15)
    assert_almost_equal("100°C to K", convert_temperature(100, 'C', 'K'), 373.15)
    assert_almost_equal("-273.15°C to K", convert_temperature(-273.15, 'C', 'K'), 0.0)
    
    # Kelvin to Celsius
    assert_almost_equal("273.15 K to °C", convert_temperature(273.15, 'K', 'C'), 0.0)
    assert_almost_equal("0 K to °C", convert_temperature(0, 'K', 'C'), -273.15)
    
    # Fahrenheit to Kelvin
    assert_almost_equal("32°F to K", convert_temperature(32, 'F', 'K'), 273.15)
    
    # Kelvin to Fahrenheit
    assert_almost_equal("273.15 K to °F", convert_temperature(273.15, 'K', 'F'), 32.0)
    
    # Round-trip
    assert_almost_equal("100°C -> °F -> °C", 
                        convert_temperature(convert_temperature(100, 'C', 'F'), 'F', 'C'), 
                        100.0, tolerance=1e-10)


def test_temperature_shortcuts():
    print("\n[Temperature Shortcuts]")
    
    assert_almost_equal("celsius_to_fahrenheit(0)", celsius_to_fahrenheit(0), 32.0)
    assert_almost_equal("celsius_to_fahrenheit(100)", celsius_to_fahrenheit(100), 212.0)
    assert_almost_equal("fahrenheit_to_celsius(32)", fahrenheit_to_celsius(32), 0.0)
    assert_almost_equal("celsius_to_kelvin(0)", celsius_to_kelvin(0), 273.15)
    assert_almost_equal("kelvin_to_celsius(273.15)", kelvin_to_celsius(273.15), 0.0)
    assert_almost_equal("fahrenheit_to_kelvin(32)", fahrenheit_to_kelvin(32), 273.15)
    assert_almost_equal("kelvin_to_fahrenheit(273.15)", kelvin_to_fahrenheit(273.15), 32.0)


def test_temperature_edge_cases():
    print("\n[Temperature Edge Cases]")
    
    # Absolute zero checks
    assert_error("below absolute zero C", convert_temperature, -300, 'C', 'F')
    assert_error("below absolute zero F", convert_temperature, -500, 'F', 'C')
    assert_error("below absolute zero K", convert_temperature, -1, 'K', 'C')
    
    # Invalid unit
    assert_error("invalid temperature unit", convert_temperature, 0, 'X', 'C')
    
    # Unit variations (with/without degree symbol)
    assert_almost_equal("0 C to F (no symbol)", convert_temperature(0, 'C', 'F'), 32.0)
    assert_almost_equal("0 °C to °F (with symbol)", convert_temperature(0, '°C', '°F'), 32.0)


# ============================================================================
# Volume Conversion Tests
# ============================================================================

def test_volume_conversions():
    print("\n[Volume Conversions]")
    
    # Metric
    assert_almost_equal("1 L to mL", convert_volume(1, 'L', 'mL'), 1000.0)
    assert_almost_equal("1 m³ to L", convert_volume(1, 'm³', 'L'), 1000.0)
    
    # US Customary
    assert_almost_equal("1 gal to qt", convert_volume(1, 'gal', 'qt'), 4.0)
    assert_almost_equal("1 qt to pt", convert_volume(1, 'qt', 'pt'), 2.0)
    assert_almost_equal("1 pt to cup", convert_volume(1, 'pt', 'cup'), 2.0)
    assert_almost_equal("1 cup to fl oz", convert_volume(1, 'cup', 'fl oz'), 8.0)
    
    # Cross-system
    assert_almost_equal("1 gal to L", convert_volume(1, 'gal', 'L'), 3.785411784)
    assert_almost_equal("1 L to gal", convert_volume(1, 'L', 'gal'), 0.2641720523581484)
    
    # Cooking measures
    assert_almost_equal("1 tbsp to tsp", convert_volume(1, 'tbsp', 'tsp'), 3.0)
    
    # Round-trip
    assert_almost_equal("1 L -> gal -> L", 
                        convert_volume(convert_volume(1, 'L', 'gal'), 'gal', 'L'), 
                        1.0, tolerance=1e-10)


def test_volume_shortcuts():
    print("\n[Volume Shortcuts]")
    
    assert_almost_equal("liters_to_gallons(1)", liters_to_gallons(1), 0.2641720523581484)
    assert_almost_equal("gallons_to_liters(1)", gallons_to_liters(1), 3.785411784)


def test_volume_edge_cases():
    print("\n[Volume Edge Cases]")
    
    # Zero
    assert_almost_equal("0 L to mL", convert_volume(0, 'L', 'mL'), 0.0)
    
    # Negative should fail
    assert_error("negative volume", convert_volume, -1, 'L', 'mL')
    
    # Invalid unit
    assert_error("invalid volume unit", convert_volume, 1, 'invalid', 'L')


# ============================================================================
# Area Conversion Tests
# ============================================================================

def test_area_conversions():
    print("\n[Area Conversions]")
    
    # Metric
    assert_almost_equal("1 km² to m²", convert_area(1, 'km²', 'm²'), 1e6)
    assert_almost_equal("1 m² to cm²", convert_area(1, 'm²', 'cm²'), 10000.0)
    assert_almost_equal("1 ha to m²", convert_area(1, 'ha', 'm²'), 10000.0)
    
    # Imperial
    assert_almost_equal("1 ft² to in²", convert_area(1, 'ft²', 'in²'), 144.0)
    assert_almost_equal("1 yd² to ft²", convert_area(1, 'yd²', 'ft²'), 9.0)
    
    # Land measures
    assert_almost_equal("1 acre to ft²", convert_area(1, 'acre', 'ft²'), 43560.0)
    assert_almost_equal("1 acre to m²", convert_area(1, 'acre', 'm²'), 4046.8564224)
    
    # Cross-system
    assert_almost_equal("1 m² to ft²", convert_area(1, 'm²', 'ft²'), 10.763910416709722)
    
    # Round-trip
    assert_almost_equal("1 ha -> acre -> ha", 
                        convert_area(convert_area(1, 'ha', 'acre'), 'acre', 'ha'), 
                        1.0, tolerance=1e-10)


def test_area_shortcuts():
    print("\n[Area Shortcuts]")
    
    assert_almost_equal("square_meters_to_square_feet(1)", square_meters_to_square_feet(1), 10.763910416709722)
    assert_almost_equal("square_feet_to_square_meters(100)", square_feet_to_square_meters(100), 9.290304)
    assert_almost_equal("acres_to_hectares(1)", acres_to_hectares(1), 0.40468564224)
    assert_almost_equal("hectares_to_acres(1)", hectares_to_acres(1), 2.471053814671653)


def test_area_edge_cases():
    print("\n[Area Edge Cases]")
    
    # Zero
    assert_almost_equal("0 m² to ft²", convert_area(0, 'm²', 'ft²'), 0.0)
    
    # Negative should fail
    assert_error("negative area", convert_area, -1, 'm²', 'ft²')


# ============================================================================
# Speed Conversion Tests
# ============================================================================

def test_speed_conversions():
    print("\n[Speed Conversions]")
    
    # Basic
    assert_almost_equal("1 m/s to km/h", convert_speed(1, 'm/s', 'km/h'), 3.6)
    assert_almost_equal("3.6 km/h to m/s", convert_speed(3.6, 'km/h', 'm/s'), 1.0)
    
    # mph
    assert_almost_equal("1 mph to km/h", convert_speed(1, 'mph', 'km/h'), 1.609344)
    assert_almost_equal("100 km/h to mph", convert_speed(100, 'km/h', 'mph'), 62.137119223733395)
    
    # Knots
    assert_almost_equal("1 kn to km/h", convert_speed(1, 'kn', 'km/h'), 1.852)
    assert_almost_equal("1 kn to m/s", convert_speed(1, 'kn', 'm/s'), 0.5144444444444444)
    
    # ft/s
    assert_almost_equal("1 ft/s to m/s", convert_speed(1, 'ft/s', 'm/s'), 0.3048)
    
    # Round-trip
    assert_almost_equal("100 km/h -> mph -> km/h", 
                        convert_speed(convert_speed(100, 'km/h', 'mph'), 'mph', 'km/h'), 
                        100.0, tolerance=1e-10)


def test_speed_shortcuts():
    print("\n[Speed Shortcuts]")
    
    assert_almost_equal("kmh_to_mph(100)", kmh_to_mph(100), 62.137119223733395)
    assert_almost_equal("mph_to_kmh(60)", mph_to_kmh(60), 96.56064)
    assert_almost_equal("ms_to_kmh(1)", ms_to_kmh(1), 3.6)
    assert_almost_equal("knots_to_kmh(1)", knots_to_kmh(1), 1.852)


def test_speed_edge_cases():
    print("\n[Speed Edge Cases]")
    
    # Zero
    assert_almost_equal("0 km/h to mph", convert_speed(0, 'km/h', 'mph'), 0.0)
    
    # Negative should fail
    assert_error("negative speed", convert_speed, -1, 'km/h', 'mph')


# ============================================================================
# Time Conversion Tests
# ============================================================================

def test_time_conversions():
    print("\n[Time Conversions]")
    
    # Basic
    assert_almost_equal("1 h to min", convert_time(1, 'h', 'min'), 60.0)
    assert_almost_equal("1 min to s", convert_time(1, 'min', 's'), 60.0)
    assert_almost_equal("1 h to s", convert_time(1, 'h', 's'), 3600.0)
    
    # Days/weeks
    assert_almost_equal("1 day to h", convert_time(1, 'day', 'h'), 24.0)
    assert_almost_equal("1 week to day", convert_time(1, 'week', 'day'), 7.0)
    
    # Small units
    assert_almost_equal("1 s to ms", convert_time(1, 's', 'ms'), 1000.0)
    assert_almost_equal("1 ms to μs", convert_time(1, 'ms', 'μs'), 1000.0)
    
    # Large units
    assert_almost_equal("1 year to day", convert_time(1, 'year', 'day'), 365.2425)
    
    # Round-trip
    assert_almost_equal("24 h -> day -> h", 
                        convert_time(convert_time(24, 'h', 'day'), 'day', 'h'), 
                        24.0, tolerance=1e-10)


def test_time_shortcuts():
    print("\n[Time Shortcuts]")
    
    assert_almost_equal("hours_to_minutes(1)", hours_to_minutes(1), 60.0)
    assert_almost_equal("minutes_to_seconds(1)", minutes_to_seconds(1), 60.0)
    assert_almost_equal("days_to_hours(1)", days_to_hours(1), 24.0)
    assert_almost_equal("weeks_to_days(1)", weeks_to_days(1), 7.0)
    assert_almost_equal("years_to_days(1)", years_to_days(1), 365.2425)


def test_time_edge_cases():
    print("\n[Time Edge Cases]")
    
    # Zero
    assert_almost_equal("0 h to min", convert_time(0, 'h', 'min'), 0.0)
    
    # Negative should fail
    assert_error("negative time", convert_time, -1, 'h', 'min')


# ============================================================================
# Data Storage Conversion Tests
# ============================================================================

def test_data_conversions():
    print("\n[Data Storage Conversions]")
    
    # Decimal (SI)
    assert_almost_equal("1 KB to B", convert_data(1, 'KB', 'B'), 1000.0)
    assert_almost_equal("1 MB to KB", convert_data(1, 'MB', 'KB'), 1000.0)
    assert_almost_equal("1 GB to MB", convert_data(1, 'GB', 'MB'), 1000.0)
    assert_almost_equal("1 TB to GB", convert_data(1, 'TB', 'GB'), 1000.0)
    
    # Binary (IEC)
    assert_almost_equal("1 KiB to B", convert_data(1, 'KiB', 'B'), 1024.0)
    assert_almost_equal("1 MiB to KiB", convert_data(1, 'MiB', 'KiB'), 1024.0)
    assert_almost_equal("1 GiB to MiB", convert_data(1, 'GiB', 'MiB'), 1024.0)
    
    # Bits
    assert_almost_equal("1 B to bit", convert_data(1, 'B', 'bit'), 8.0)
    assert_almost_equal("8 bit to B", convert_data(8, 'bit', 'B'), 1.0)
    
    # Cross-system
    assert_almost_equal("1 GB vs GiB", convert_data(1, 'GB', 'GiB'), 0.9313225746154785)
    
    # Round-trip
    assert_almost_equal("1 GB -> MB -> GB", 
                        convert_data(convert_data(1, 'GB', 'MB'), 'MB', 'GB'), 
                        1.0, tolerance=1e-10)


def test_data_shortcuts():
    print("\n[Data Shortcuts]")
    
    assert_almost_equal("gb_to_mb(1)", gb_to_mb(1), 1000.0)
    assert_almost_equal("gib_to_mib(1)", gib_to_mib(1), 1024.0)
    assert_almost_equal("tb_to_gb(1)", tb_to_gb(1), 1000.0)
    assert_almost_equal("bytes_to_bits(1)", bytes_to_bits(1), 8.0)
    assert_almost_equal("bits_to_bytes(8)", bits_to_bytes(8), 1.0)


def test_data_edge_cases():
    print("\n[Data Edge Cases]")
    
    # Zero
    assert_almost_equal("0 GB to MB", convert_data(0, 'GB', 'MB'), 0.0)
    
    # Negative should fail
    assert_error("negative data", convert_data, -1, 'GB', 'MB')


# ============================================================================
# Pressure Conversion Tests
# ============================================================================

def test_pressure_conversions():
    print("\n[Pressure Conversions]")
    
    # Standard atmosphere
    assert_almost_equal("1 atm to Pa", convert_pressure(1, 'atm', 'Pa'), 101325.0)
    
    # Bar
    assert_almost_equal("1 bar to Pa", convert_pressure(1, 'bar', 'Pa'), 100000.0)
    assert_almost_equal("1 bar to atm", convert_pressure(1, 'bar', 'atm'), 0.9869232667160128)
    
    # PSI
    assert_almost_equal("1 psi to Pa", convert_pressure(1, 'psi', 'Pa'), 6894.757293168)
    assert_almost_equal("1 bar to psi", convert_pressure(1, 'bar', 'psi'), 14.50377377304066)
    
    # mmHg / Torr
    assert_almost_equal("760 mmHg to atm", convert_pressure(760, 'mmHg', 'atm'), 0.9999998462107669)
    assert_almost_equal("1 Torr to Pa", convert_pressure(1, 'Torr', 'Pa'), 133.322368421)
    
    # kPa
    assert_almost_equal("1 kPa to Pa", convert_pressure(1, 'kPa', 'Pa'), 1000.0)
    
    # Round-trip
    assert_almost_equal("1 atm -> bar -> atm", 
                        convert_pressure(convert_pressure(1, 'atm', 'bar'), 'bar', 'atm'), 
                        1.0, tolerance=1e-10)


def test_pressure_shortcuts():
    print("\n[Pressure Shortcuts]")
    
    assert_almost_equal("atm_to_pascal(1)", atm_to_pascal(1), 101325.0)
    assert_almost_equal("psi_to_bar(14.50377377304066)", psi_to_bar(14.50377377304066), 1.0, tolerance=1e-6)
    assert_almost_equal("bar_to_psi(1)", bar_to_psi(1), 14.50377377304066)


def test_pressure_edge_cases():
    print("\n[Pressure Edge Cases]")
    
    # Zero
    assert_almost_equal("0 Pa to bar", convert_pressure(0, 'Pa', 'bar'), 0.0)
    
    # Negative should fail
    assert_error("negative pressure", convert_pressure, -1, 'Pa', 'bar')


# ============================================================================
# Energy Conversion Tests
# ============================================================================

def test_energy_conversions():
    print("\n[Energy Conversions]")
    
    # Basic
    assert_almost_equal("1 kJ to J", convert_energy(1, 'kJ', 'J'), 1000.0)
    
    # Calories
    assert_almost_equal("1 cal to J", convert_energy(1, 'cal', 'J'), 4.184)
    assert_almost_equal("1 kcal to J", convert_energy(1, 'kcal', 'J'), 4184.0)
    assert_almost_equal("1 kcal to cal", convert_energy(1, 'kcal', 'cal'), 1000.0)
    
    # Electrical
    assert_almost_equal("1 Wh to J", convert_energy(1, 'Wh', 'J'), 3600.0)
    assert_almost_equal("1 kWh to J", convert_energy(1, 'kWh', 'J'), 3600000.0)
    
    # BTU
    assert_almost_equal("1 BTU to J", convert_energy(1, 'BTU', 'J'), 1055.05585262)
    
    # eV
    assert_almost_equal("1 eV to J", convert_energy(1, 'eV', 'J'), 1.602176634e-19)
    
    # Round-trip
    assert_almost_equal("1 kWh -> J -> kWh", 
                        convert_energy(convert_energy(1, 'kWh', 'J'), 'J', 'kWh'), 
                        1.0, tolerance=1e-10)


def test_energy_shortcuts():
    print("\n[Energy Shortcuts]")
    
    assert_almost_equal("kwh_to_joules(1)", kwh_to_joules(1), 3600000.0)
    assert_almost_equal("calories_to_joules(1)", calories_to_joules(1), 4.184)
    assert_almost_equal("btu_to_kwh(1)", btu_to_kwh(1), 0.0002930710701722222)


def test_energy_edge_cases():
    print("\n[Energy Edge Cases]")
    
    # Zero
    assert_almost_equal("0 J to kJ", convert_energy(0, 'J', 'kJ'), 0.0)
    
    # Negative should fail
    assert_error("negative energy", convert_energy, -1, 'J', 'kJ')


# ============================================================================
# Power Conversion Tests
# ============================================================================

def test_power_conversions():
    print("\n[Power Conversions]")
    
    # Basic
    assert_almost_equal("1 kW to W", convert_power(1, 'kW', 'W'), 1000.0)
    assert_almost_equal("1 MW to kW", convert_power(1, 'MW', 'kW'), 1000.0)
    
    # Horsepower
    assert_almost_equal("1 hp to W", convert_power(1, 'hp', 'W'), 745.6998715822702)
    assert_almost_equal("1 hp to kW", convert_power(1, 'hp', 'kW'), 0.7456998715822702)
    
    # BTU/h
    assert_almost_equal("1 BTU/h to W", convert_power(1, 'BTU/h', 'W'), 0.2930710701722222)
    
    # Round-trip
    assert_almost_equal("1 kW -> W -> kW", 
                        convert_power(convert_power(1, 'kW', 'W'), 'W', 'kW'), 
                        1.0, tolerance=1e-10)


def test_power_shortcuts():
    print("\n[Power Shortcuts]")
    
    assert_almost_equal("hp_to_kw(1)", hp_to_kw(1), 0.7456998715822702)
    assert_almost_equal("kw_to_hp(1)", kw_to_hp(1), 1.341022089595028)
    assert_almost_equal("mw_to_kw(1)", mw_to_kw(1), 1000.0)


def test_power_edge_cases():
    print("\n[Power Edge Cases]")
    
    # Zero
    assert_almost_equal("0 W to kW", convert_power(0, 'W', 'kW'), 0.0)
    
    # Negative should fail
    assert_error("negative power", convert_power, -1, 'W', 'kW')


# ============================================================================
# Universal Convert Function Tests
# ============================================================================

def test_universal_convert():
    print("\n[Universal Convert Function]")
    
    # Auto-detect length
    assert_almost_equal("convert 1 km to mi", convert(1, 'km', 'mi'), 0.6213711922373339)
    
    # Auto-detect temperature
    assert_almost_equal("convert 0 C to F", convert(0, 'C', 'F'), 32.0)
    
    # Auto-detect weight
    assert_almost_equal("convert 1 kg to lb", convert(1, 'kg', 'lb'), 2.2046226218487757)
    
    # Cross-category should fail
    assert_error("convert length to weight", convert, 1, 'm', 'kg')


def test_format_conversion():
    print("\n[Format Conversion]")
    
    assert_equal("format 1 km to m", format_conversion(1, 'km', 'm'), "1000.0000 m")
    assert_equal("format 1 mi to km (2 decimals)", format_conversion(1, 'mi', 'km', 2), "1.61 km")


# ============================================================================
# Batch Conversion Tests
# ============================================================================

def test_batch_conversions():
    print("\n[Batch Conversions]")
    
    # Batch length
    lengths = batch_convert_length([1, 2, 3], 'km', 'm')
    assert_equal("batch length result count", len(lengths), 3)
    assert_almost_equal("batch length[0]", lengths[0], 1000.0)
    assert_almost_equal("batch length[1]", lengths[1], 2000.0)
    assert_almost_equal("batch length[2]", lengths[2], 3000.0)
    
    # Batch weight
    weights = batch_convert_weight([1, 2, 3], 'kg', 'lb')
    assert_equal("batch weight result count", len(weights), 3)
    assert_almost_equal("batch weight[0]", weights[0], 2.2046226218487757)
    
    # Batch temperature
    temps = batch_convert_temperature([0, 100], 'C', 'F')
    assert_equal("batch temp result count", len(temps), 2)
    assert_almost_equal("batch temp[0]", temps[0], 32.0)
    assert_almost_equal("batch temp[1]", temps[1], 212.0)


# ============================================================================
# Unit Info Tests
# ============================================================================

def test_get_available_units():
    print("\n[Get Available Units]")
    
    length_units = get_available_units('length')
    assert_equal("length units has 'm'", 'm' in length_units, True)
    assert_equal("length units has 'km'", 'km' in length_units, True)
    assert_equal("length units has 'ft'", 'ft' in length_units, True)
    
    weight_units = get_available_units('weight')
    assert_equal("weight units has 'kg'", 'kg' in weight_units, True)
    assert_equal("weight units has 'lb'", 'lb' in weight_units, True)
    
    # Invalid category
    assert_error("invalid category", get_available_units, 'invalid')


def test_get_unit_info():
    print("\n[Get Unit Info]")
    
    info = get_unit_info('km')
    assert_equal("km category", info['category'], 'length')
    assert_equal("km symbol", info['symbol'], 'km')
    assert_equal("km name", info['name'], 'Kilometer')
    
    info = get_unit_info('kg')
    assert_equal("kg category", info['category'], 'weight')
    
    # Unknown unit
    info = get_unit_info('unknown')
    assert_equal("unknown unit returns None", info, None)


# ============================================================================
# Main Test Runner
# ============================================================================

def run_all_tests():
    print("=" * 60)
    print("AllToolkit - Unit Converter Utils Test Suite")
    print("=" * 60)
    
    # Length
    test_length_conversions()
    test_length_shortcuts()
    test_length_edge_cases()
    
    # Weight
    test_weight_conversions()
    test_weight_shortcuts()
    test_weight_edge_cases()
    
    # Temperature
    test_temperature_conversions()
    test_temperature_shortcuts()
    test_temperature_edge_cases()
    
    # Volume
    test_volume_conversions()
    test_volume_shortcuts()
    test_volume_edge_cases()
    
    # Area
    test_area_conversions()
    test_area_shortcuts()
    test_area_edge_cases()
    
    # Speed
    test_speed_conversions()
    test_speed_shortcuts()
    test_speed_edge_cases()
    
    # Time
    test_time_conversions()
    test_time_shortcuts()
    test_time_edge_cases()
    
    # Data
    test_data_conversions()
    test_data_shortcuts()
    test_data_edge_cases()
    
    # Pressure
    test_pressure_conversions()
    test_pressure_shortcuts()
    test_pressure_edge_cases()
    
    # Energy
    test_energy_conversions()
    test_energy_shortcuts()
    test_energy_edge_cases()
    
    # Power
    test_power_conversions()
    test_power_shortcuts()
    test_power_edge_cases()
    
    # Universal
    test_universal_convert()
    test_format_conversion()
    
    # Batch
    test_batch_conversions()
    
    # Info
    test_get_available_units()
    test_get_unit_info()
    
    return result.summary()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
