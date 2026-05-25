#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frequency Utilities - Basic Usage Examples
===========================================

Basic examples demonstrating frequency conversion and calculations.
"""

import sys
sys.path.insert(0, '..')

from mod import (
    convert_frequency,
    frequency_to_all,
    frequency_to_period,
    period_to_frequency,
    format_frequency,
)


def main():
    print("=" * 60)
    print("Frequency Utilities - Basic Usage Examples")
    print("=" * 60)
    
    # 1. Simple frequency unit conversion
    print("\n--- Simple Unit Conversion ---")
    print(f"1000 Hz = {convert_frequency(1000, 'Hz', 'kHz')} kHz")
    print(f"1 MHz = {convert_frequency(1, 'MHz', 'Hz')} Hz")
    print(f"60 RPM = {convert_frequency(60, 'rpm', 'Hz')} Hz (1 revolution per second)")
    print(f"1 GHz = {convert_frequency(1, 'GHz', 'MHz')} MHz")
    
    # 2. Convert to all units
    print("\n--- Convert to All Units ---")
    result = frequency_to_all(2.4, 'GHz')  # WiFi frequency
    print(f"2.4 GHz WiFi frequency:")
    print(f"  In Hz: {result.hertz:.0f} Hz")
    print(f"  In kHz: {result.kilohertz:.0f} kHz")
    print(f"  In MHz: {result.megahertz} MHz")
    print(f"  Period: {result.period_seconds * 1e12:.4f} ps")
    
    # 3. Frequency to period
    print("\n--- Frequency to Period ---")
    freqs = [50, 440, 1000, 1000000]
    for freq in freqs:
        period = frequency_to_period(freq)
        print(f"{format_frequency(freq)} → Period: {period:.6f} s")
    
    # 4. Period to frequency
    print("\n--- Period to Frequency ---")
    periods = [0.02, 0.001, 1e-6]
    for period in periods:
        freq = period_to_frequency(period)
        print(f"Period {period:.6f} s → {format_frequency(freq)}")
    
    # 5. Format frequency display
    print("\n--- Format Frequency Display ---")
    frequencies = [0.001, 100, 1000, 1000000, 1000000000, 1e12]
    for freq in frequencies:
        print(f"{freq:.0e} Hz → {format_frequency(freq)}")


if __name__ == '__main__':
    main()