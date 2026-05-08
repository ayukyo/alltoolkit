#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Resistor Color Code Utilities Usage Examples
==========================================================
Practical examples demonstrating resistor color code calculations.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resistor_color_code_utils.mod import (
    decode_3band, decode_4band, decode_5band, decode_6band, decode_resistor,
    encode_4band, encode_5band, encode_6band,
    decode_smd, encode_smd,
    get_e_series, find_nearest_standard, is_standard_value,
    parallel_resistance, series_resistance, voltage_divider, led_resistor,
    is_valid_color, get_color_info,
    _format_resistance,
)


def example_decode_color_bands():
    """Example: Decode resistor color bands."""
    print("=" * 60)
    print("Example 1: Decode Color Bands")
    print("=" * 60)
    
    # 4-band resistor (most common)
    colors = ['brown', 'black', 'red', 'gold']
    result = decode_4band(colors)
    print(f"\n4-band: {' - '.join(colors)}")
    print(f"  Resistance: {result['resistance_str']}")
    print(f"  Tolerance: ±{result['tolerance']}%")
    print(f"  Actual value range: {result['resistance'] * (1 - result['tolerance']/100):.1f}Ω to {result['resistance'] * (1 + result['tolerance']/100):.1f}Ω")
    
    # 5-band resistor (higher precision)
    colors = ['yellow', 'violet', 'black', 'brown', 'brown']
    result = decode_5band(colors)
    print(f"\n5-band: {' - '.join(colors)}")
    print(f"  Resistance: {result['resistance_str']}")
    print(f"  Tolerance: ±{result['tolerance']}%")
    
    # 6-band resistor (precision + temperature coefficient)
    colors = ['red', 'red', 'black', 'orange', 'brown', 'red']
    result = decode_6band(colors)
    print(f"\n6-band: {' - '.join(colors)}")
    print(f"  Resistance: {result['resistance_str']}")
    print(f"  Tolerance: ±{result['tolerance']}%")
    print(f"  Temp coefficient: {result['tempco_str']}")


def example_encode_color_bands():
    """Example: Encode resistance values to color bands."""
    print("\n" + "=" * 60)
    print("Example 2: Encode Resistance to Color Bands")
    print("=" * 60)
    
    # Common values
    values = [100, 220, 470, 1000, 4700, 10000, 47000, 100000]
    
    print("\nCommon resistor values (±5% tolerance):")
    for val in values:
        result = encode_4band(val, 5)
        colors_str = ' - '.join(c.upper() for c in result['colors'])
        print(f"  {result['resistance_str']:12} → {colors_str}")
    
    # High precision resistor
    result = encode_5band(4700, 1)
    print(f"\nPrecision resistor (4.7kΩ ±1%):")
    colors_str = ' - '.join(c.upper() for c in result['colors'])
    print(f"  Colors: {colors_str}")


def example_smd_codes():
    """Example: SMD resistor codes."""
    print("\n" + "=" * 60)
    print("Example 3: SMD Resistor Codes")
    print("=" * 60)
    
    # Decode various SMD codes
    smd_codes = ['103', '473', '1002', '4701', '4R7', 'R47', '01C']
    
    print("\nDecoding SMD codes:")
    for code in smd_codes:
        try:
            result = decode_smd(code)
            print(f"  {code:6} → {result['resistance_str']:12} ({result['type']})")
        except ValueError as e:
            print(f"  {code:6} → Error: {e}")
    
    # Encode resistance to SMD codes
    print("\nEncoding to SMD codes:")
    resistances = [100, 1000, 4700, 10000, 0.47, 4.7]
    for r in resistances:
        result = encode_smd(r)
        print(f"  {_format_resistance(r):12} → {result['code']:6} ({result['type']})")


def example_e_series():
    """Example: Standard E-series values."""
    print("\n" + "=" * 60)
    print("Example 4: E-Series Standard Values")
    print("=" * 60)
    
    # Show E-series values
    print("\nE6 series (20% tolerance):")
    print(f"  {get_e_series('E6')}")
    
    print("\nE12 series (10% tolerance):")
    print(f"  {get_e_series('E12')}")
    
    print("\nE24 series (5% tolerance):")
    print(f"  {get_e_series('E24')}")
    
    # Find nearest standard value
    print("\nFinding nearest standard values:")
    values = [4500, 5000, 5500, 3300, 7500]
    for val in values:
        result = find_nearest_standard(val, 'E12')
        print(f"  {val}Ω → nearest E12: {result['nearest_str']} (error: {result['error_percent']}%)")


def example_circuit_calculations():
    """Example: Circuit calculations."""
    print("\n" + "=" * 60)
    print("Example 5: Circuit Calculations")
    print("=" * 60)
    
    # Parallel resistance
    print("\nParallel resistors:")
    resistors = [
        [100, 100],
        [1000, 2000],
        [100, 200, 300],
        [4700, 4700],
    ]
    for r_list in resistors:
        result = parallel_resistance(r_list)
        r_str = ', '.join(_format_resistance(r) for r in r_list)
        print(f"  {r_str} → {_format_resistance(result)}")
    
    # Series resistance
    print("\nSeries resistors:")
    resistors = [
        [100, 200],
        [1000, 2000, 3000],
        [4700, 10000],
    ]
    for r_list in resistors:
        result = series_resistance(r_list)
        r_str = ', '.join(_format_resistance(r) for r in r_list)
        print(f"  {r_str} → {_format_resistance(result)}")
    
    # Voltage divider
    print("\nVoltage dividers:")
    dividers = [
        (10000, 10000, 5),  # Equal resistors, half voltage
        (20000, 10000, 12), # R1=20k, R2=10k, Vin=12V
        (9000, 1000, 10),   # R1=9k, R2=1k, Vin=10V
    ]
    for r1, r2, vin in dividers:
        vout = voltage_divider(r1, r2, vin)
        print(f"  R1={_format_resistance(r1)}, R2={_format_resistance(r2)}, Vin={vin}V → Vout={vout:.2f}V")


def example_led_resistor():
    """Example: LED resistor calculations."""
    print("\n" + "=" * 60)
    print("Example 6: LED Resistor Calculator")
    print("=" * 60)
    
    # Common LED configurations
    leds = [
        (5, 2, 0.02),     # Red LED on 5V
        (5, 3, 0.02),     # Blue/White LED on 5V
        (12, 2, 0.02),    # Red LED on 12V
        (3.3, 2, 0.01),   # LED on 3.3V (Arduino)
        (9, 2.5, 0.015),  # Green LED on 9V battery
    ]
    
    print("\nLED resistor calculations:")
    for supply_v, led_v, current in leds:
        resistor = led_resistor(supply_v, led_v, current)
        current_ma = current * 1000
        print(f"  Supply={supply_v}V, LED={led_v}V, Current={current_ma}mA → {_format_resistance(resistor)}")
    
    # Find nearest standard resistor
    print("\nNearest standard resistor values:")
    for supply_v, led_v, current in leds[:3]:
        resistor = led_resistor(supply_v, led_v, current)
        nearest = find_nearest_standard(resistor, 'E12')
        print(f"  Calculated: {_format_resistance(resistor)} → Standard: {nearest['nearest_str']}")


def example_color_info():
    """Example: Color band information."""
    print("\n" + "=" * 60)
    print("Example 7: Color Band Information")
    print("=" * 60)
    
    colors = ['black', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'violet', 'gray', 'white', 'gold', 'silver']
    
    print("\nColor band values and meanings:")
    print(f"{'Color':10} {'Value':>8} {'Multiplier':>12} {'Tolerance':>10} {'TempCo':>10}")
    print("-" * 52)
    for color in colors:
        info = get_color_info(color)
        val_str = str(info['value']) if info['value'] is not None else '-'
        mult_str = str(info['multiplier']) if info['multiplier'] is not None else '-'
        tol_str = str(info['tolerance']) + '%' if info['tolerance'] is not None else '-'
        tempco_str = str(info['tempco']) + ' ppm' if info['tempco'] is not None else '-'
        print(f"{color:10} {val_str:>8} {mult_str:>12} {tol_str:>10} {tempco_str:>10}")


def example_practical_scenarios():
    """Example: Practical electronics scenarios."""
    print("\n" + "=" * 60)
    print("Example 8: Practical Electronics Scenarios")
    print("=" * 60)
    
    # Scenario 1: Design a voltage divider for Arduino ADC
    print("\nScenario: Measure 12V with Arduino (5V ADC)")
    print("  Need Vout ≤ 5V when Vin = 12V")
    r1 = 7000  # 7kΩ upper resistor
    r2 = 5000  # 5kΩ lower resistor
    vout = voltage_divider(r1, r2, 12)
    print(f"  R1=7kΩ, R2=5kΩ → Vout = {vout:.2f}V (safe for Arduino)")
    
    # Find nearest standard values
    nearest_r1 = find_nearest_standard(r1, 'E12')
    nearest_r2 = find_nearest_standard(r2, 'E12')
    print(f"  Standard values: R1={nearest_r1['nearest_str']}, R2={nearest_r2['nearest_str']}")
    
    # Scenario 2: Calculate equivalent resistance
    print("\nScenario: Three 10kΩ resistors available")
    r = 10000
    parallel_3 = parallel_resistance([r, r, r])
    series_3 = series_resistance([r, r, r])
    print(f"  In parallel: {_format_resistance(parallel_3)}")
    print(f"  In series: {_format_resistance(series_3)}")
    
    # Scenario 3: LED indicator circuit
    print("\nScenario: 5V indicator LED circuit")
    resistor = led_resistor(5, 2.1, 0.02)  # Red LED, 20mA
    nearest = find_nearest_standard(resistor, 'E24')
    print(f"  Required resistor: {_format_resistance(resistor)}")
    print(f"  Nearest E24: {nearest['nearest_str']}")
    
    # Calculate actual current with nearest resistor
    actual_current = (5 - 2.1) / nearest['nearest']
    print(f"  Actual current: {actual_current * 1000:.1f}mA")


def main():
    """Run all examples."""
    example_decode_color_bands()
    example_encode_color_bands()
    example_smd_codes()
    example_e_series()
    example_circuit_calculations()
    example_led_resistor()
    example_color_info()
    example_practical_scenarios()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()