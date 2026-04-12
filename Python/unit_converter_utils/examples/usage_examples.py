#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Unit Converter Utils Usage Examples
==================================================
Practical examples demonstrating common unit conversion scenarios.

Run with: python usage_examples.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    convert_length, convert_weight, convert_temperature,
    convert_volume, convert_area, convert_speed,
    convert_time, convert_data, convert_pressure,
    convert_energy, convert_power,
    convert, format_conversion,
    batch_convert_length, batch_convert_temperature,
    get_available_units, get_unit_info,
    # Shortcuts
    celsius_to_fahrenheit, kg_to_pounds, kilometers_to_miles,
    liters_to_gallons, gallons_to_liters, square_meters_to_square_feet,
    gb_to_mb, hp_to_kw,
)


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


# ============================================================================
# Daily Life Conversions
# ============================================================================

def daily_life_examples():
    """Common conversions for everyday use."""
    print_section("🏠 Daily Life Conversions")
    
    # Weather / Temperature
    print("\n🌡️  Weather & Temperature:")
    print(f"   Room temperature: 20°C = {celsius_to_fahrenheit(20):.1f}°F")
    print(f"   Body temperature: 37°C = {celsius_to_fahrenheit(37):.1f}°F")
    print(f"   Freezing point: 0°C = {celsius_to_fahrenheit(0):.1f}°F")
    print(f"   Hot day: 100°F = {convert_temperature(100, 'F', 'C'):.1f}°C")
    
    # Cooking / Volume
    print("\n🍳 Cooking & Volume:")
    print(f"   1 cup = {convert_volume(1, 'cup', 'mL'):.0f} mL")
    print(f"   1 tbsp = {convert_volume(1, 'tbsp', 'tsp'):.0f} tsp")
    print(f"   1 gallon = {gallons_to_liters(1):.2f} L")
    print(f"   500 mL = {convert_volume(500, 'mL', 'cup'):.2f} cups")
    
    # Weight / Shopping
    print("\n⚖️  Weight & Shopping:")
    print(f"   1 kg = {kg_to_pounds(1):.2f} lb")
    print(f"   5 lb = {convert_weight(5, 'lb', 'kg'):.2f} kg")
    print(f"   1 oz = {convert_weight(1, 'oz', 'g'):.2f} g")
    
    # Distance / Travel
    print("\n🚗 Distance & Travel:")
    print(f"   1 km = {kilometers_to_miles(1):.3f} mi")
    print(f"   5 mi = {convert_length(5, 'mi', 'km'):.3f} km")
    print(f"   Marathon: 42.195 km = {convert_length(42.195, 'km', 'mi'):.3f} mi")
    print(f"   100 m = {convert_length(100, 'm', 'ft'):.1f} ft")


# ============================================================================
# Scientific & Engineering
# ============================================================================

def scientific_examples():
    """Conversions for scientific and engineering work."""
    print_section("🔬 Scientific & Engineering")
    
    # Physics / Energy
    print("\n⚡ Energy & Power:")
    print(f"   1 kWh = {convert_energy(1, 'kWh', 'J'):,.0f} J")
    print(f"   1000 cal = {convert_energy(1000, 'cal', 'kJ'):.2f} kJ")
    print(f"   1 hp = {hp_to_kw(1):.3f} kW")
    print(f"   1 BTU = {convert_energy(1, 'BTU', 'Wh'):.3f} Wh")
    
    # Pressure
    print("\n🔽 Pressure:")
    print(f"   1 atm = {convert_pressure(1, 'atm', 'kPa'):.2f} kPa")
    print(f"   1 bar = {convert_pressure(1, 'bar', 'psi'):.2f} psi")
    print(f"   Standard tire pressure: 32 psi = {convert_pressure(32, 'psi', 'bar'):.2f} bar")
    print(f"   Blood pressure: 120 mmHg = {convert_pressure(120, 'mmHg', 'kPa'):.2f} kPa")
    
    # Speed
    print("\n🚀 Speed & Velocity:")
    print(f"   Speed of sound: 343 m/s = {convert_speed(343, 'm/s', 'km/h'):.0f} km/h")
    print(f"   Highway speed: 120 km/h = {convert_speed(120, 'km/h', 'mph'):.1f} mph")
    print(f"   1 knot = {convert_speed(1, 'kn', 'km/h'):.3f} km/h")
    
    # Small scales
    print("\n🔬 Micro & Nano:")
    print(f"   1 μm = {convert_length(1, 'μm', 'nm')} nm")
    print(f"   1 nm = {convert_length(1, 'nm', 'm')} m")
    print(f"   Human hair: ~80 μm = {convert_length(80, 'μm', 'mm'):.2f} mm")


# ============================================================================
# Computing & Data
# ============================================================================

def computing_examples():
    """Data storage and computing conversions."""
    print_section("💻 Computing & Data Storage")
    
    # Storage
    print("\n💾 Storage Capacity:")
    print(f"   1 TB = {convert_data(1, 'TB', 'GB'):.0f} GB")
    print(f"   500 GB = {convert_data(500, 'GB', 'MB'):.0f} MB")
    print(f"   1 GiB = {convert_data(1, 'GiB', 'MB'):.2f} MB (binary)")
    print(f"   1 GB = {convert_data(1, 'GB', 'GiB'):.4f} GiB")
    
    # Network
    print("\n🌐 Network Speed:")
    print(f"   100 Mbps = {convert_data(100, 'Mibit', 'MB'):.2f} MB/s")
    print(f"   1 Gbps = {convert_data(1, 'Gibit', 'MB'):.2f} MB/s theoretical")
    
    # File sizes
    print("\n📁 File Sizes:")
    print(f"   1.5 GB video = {convert_data(1.5, 'GB', 'MB'):.0f} MB")
    print(f"   256 GB SSD = {convert_data(256, 'GB', 'GiB'):.2f} GiB actual")


# ============================================================================
# Real Estate & Construction
# ============================================================================

def real_estate_examples():
    """Area and construction related conversions."""
    print_section("🏗️ Real Estate & Construction")
    
    # Area
    print("\n📐 Area Measurements:")
    print(f"   100 m² = {square_meters_to_square_feet(100):.1f} ft²")
    print(f"   1000 ft² = {convert_area(1000, 'ft²', 'm²'):.1f} m²")
    print(f"   1 acre = {convert_area(1, 'acre', 'm²'):,.0f} m²")
    print(f"   1 hectare = {convert_area(1, 'ha', 'acre'):.2f} acres")
    
    # Room dimensions
    print("\n🏠 Room Sizes:")
    print(f"   10 ft × 12 ft = {convert_length(10, 'ft', 'm'):.2f} m × {convert_length(12, 'ft', 'm'):.2f} m")
    print(f"   Standard ceiling: 8 ft = {convert_length(8, 'ft', 'm'):.2f} m")
    
    # Land
    print("\n🌍 Land:")
    print(f"   Football field: ~1 acre = {convert_area(1, 'acre', 'm²'):,.0f} m²")
    print(f"   1 square km = {convert_area(1, 'km²', 'ha'):.0f} hectares")


# ============================================================================
# Time & Scheduling
# ============================================================================

def time_examples():
    """Time related conversions."""
    print_section("⏰ Time & Scheduling")
    
    # Basic
    print("\n📅 Basic Time:")
    print(f"   1.5 hours = {convert_time(1.5, 'h', 'min'):.0f} minutes")
    print(f"   90 minutes = {convert_time(90, 'min', 'h'):.1f} hours")
    print(f"   2 weeks = {convert_time(2, 'week', 'day'):.0f} days")
    
    # Project planning
    print("\n📋 Project Planning:")
    print(f"   1 quarter = {convert_time(0.25, 'year', 'day'):.0f} days")
    print(f"   30 days = {convert_time(30, 'day', 'week'):.1f} weeks")
    
    # Precise timing
    print("\n⏱️  Precise Timing:")
    print(f"   1 ms = {convert_time(1, 'ms', 'μs'):.0f} μs")
    print(f"   1 μs = {convert_time(1, 'μs', 'ns'):.0f} ns")
    print(f"   CPU cycle (1 ns) = {convert_time(1, 'ns', 's')} s")


# ============================================================================
# Universal Convert Function
# ============================================================================

def universal_convert_examples():
    """Using the universal convert() function."""
    print_section("🔄 Universal Convert Function")
    
    print("\nThe convert() function auto-detects the unit category:")
    print(f"   convert(100, 'C', 'F') = {convert(100, 'C', 'F')} (temperature)")
    print(f"   convert(1, 'km', 'mi') = {convert(1, 'km', 'mi'):.6f} (length)")
    print(f"   convert(1, 'kg', 'lb') = {convert(1, 'kg', 'lb'):.6f} (weight)")
    print(f"   convert(1, 'L', 'gal') = {convert(1, 'L', 'gal'):.6f} (volume)")
    print(f"   convert(1, 'GB', 'MB') = {convert(1, 'GB', 'MB')} (data)")
    
    print("\nFormatted output:")
    print(f"   format_conversion(1, 'mi', 'km', 2) = '{format_conversion(1, 'mi', 'km', 2)}'")
    print(f"   format_conversion(0, 'C', 'F') = '{format_conversion(0, 'C', 'F')}'")
    print(f"   format_conversion(1000, 'm', 'km') = '{format_conversion(1000, 'm', 'km')}'")


# ============================================================================
# Batch Operations
# ============================================================================

def batch_examples():
    """Batch conversion examples."""
    print_section("📊 Batch Conversions")
    
    # Temperature readings
    print("\n🌡️  Temperature Readings (C → F):")
    readings_c = [0, 10, 20, 25, 30, 37, 100]
    readings_f = batch_convert_temperature(readings_c, 'C', 'F')
    for c, f in zip(readings_c, readings_f):
        print(f"   {c:3d}°C = {f:6.1f}°F")
    
    # Race distances
    print("\n🏃 Race Distances (km → mi):")
    races_km = [5, 10, 21.0975, 42.195]  # 5K, 10K, Half, Full marathon
    races_mi = batch_convert_length(races_km, 'km', 'mi')
    names = ['5K', '10K', 'Half Marathon', 'Full Marathon']
    for name, km, mi in zip(names, races_km, races_mi):
        print(f"   {name:15s}: {km:7.3f} km = {mi:7.3f} mi")


# ============================================================================
# Unit Discovery
# ============================================================================

def unit_discovery_examples():
    """Discovering available units."""
    print_section("🔍 Unit Discovery")
    
    print("\nAvailable length units:")
    print(f"   {get_available_units('length')}")
    
    print("\nAvailable weight units:")
    print(f"   {get_available_units('weight')}")
    
    print("\nAvailable temperature units:")
    print(f"   {get_available_units('temperature')}")
    
    print("\nUnit info for 'km':")
    info = get_unit_info('km')
    print(f"   {info}")
    
    print("\nUnit info for 'kg':")
    info = get_unit_info('kg')
    print(f"   {info}")


# ============================================================================
# Error Handling Demo
# ============================================================================

def error_handling_examples():
    """Demonstrating error handling."""
    print_section("⚠️ Error Handling")
    
    print("\nAttempting invalid conversions:")
    
    # Negative weight
    try:
        convert_weight(-1, 'kg', 'g')
    except ValueError as e:
        print(f"   ✓ Caught: {e}")
    
    # Below absolute zero
    try:
        convert_temperature(-300, 'C', 'F')
    except ValueError as e:
        print(f"   ✓ Caught: {e}")
    
    # Invalid unit
    try:
        convert_length(1, 'invalid', 'm')
    except ValueError as e:
        print(f"   ✓ Caught: {e}")
    
    # Cross-category
    try:
        convert(1, 'm', 'kg')
    except ValueError as e:
        print(f"   ✓ Caught: {e}")


# ============================================================================
# Main
# ============================================================================

def main():
    print("=" * 60)
    print("  AllToolkit - Unit Converter Utils Examples")
    print("=" * 60)
    
    daily_life_examples()
    scientific_examples()
    computing_examples()
    real_estate_examples()
    time_examples()
    universal_convert_examples()
    batch_examples()
    unit_discovery_examples()
    error_handling_examples()
    
    print("\n" + "=" * 60)
    print("  Examples Complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
