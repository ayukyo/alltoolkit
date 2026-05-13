#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Significant Figures Utilities Examples
===================================================
Basic usage examples for the significant_figures_utils module.

Author: AllToolkit Contributors
License: MIT
"""

import sys
sys.path.insert(0, '..')

from mod import (
    count_significant_figures,
    round_to_sig_figs,
    format_sig_figs,
    to_scientific_notation,
    SigFigNumber,
    add_sig_figs,
    multiply_sig_figs,
    create_measured_value,
    format_with_uncertainty,
    propagate_uncertainty_addition,
    propagate_uncertainty_multiplication,
    calculate_percent_error,
)


def example_counting_sig_figs():
    """Example: Counting significant figures in various numbers."""
    print("\n=== Example: Counting Significant Figures ===")
    
    test_values = [
        ("123", "Integer"),
        ("00123", "With leading zeros"),
        ("12300", "Trailing zeros (no decimal)"),
        ("12300.", "Trailing zeros (with decimal)"),
        ("0.00456", "Small decimal"),
        ("1.2300", "Decimal with trailing zeros"),
        ("1.020", "Zero between digits"),
        ("1.00e3", "Scientific notation"),
    ]
    
    for value, description in test_values:
        sig_figs = count_significant_figures(value)
        print(f"  {value:12} ({description:30}) -> {sig_figs} sf")


def example_rounding():
    """Example: Rounding numbers to specific significant figures."""
    print("\n=== Example: Rounding to Significant Figures ===")
    
    numbers = [123.456, 0.00123456, 999.9, 0.987654]
    sig_figs_list = [1, 2, 3, 4, 5]
    
    for num in numbers:
        print(f"\n  Original: {num}")
        for sf in sig_figs_list:
            rounded = round_to_sig_figs(num, sf)
            formatted = format_sig_figs(num, sf)
            print(f"    {sf} sf: {formatted} (raw: {rounded})")


def example_scientific_notation():
    """Example: Converting to scientific notation."""
    print("\n=== Example: Scientific Notation ===")
    
    numbers = [
        (1234.56, 3),
        (0.00123, 2),
        (1000000, 4),
        (0.000000123, 2),
        (-1234.56, 3),
    ]
    
    for num, sf in numbers:
        sci = to_scientific_notation(num, sf)
        print(f"  {num:15} ({sf} sf) -> {sci}")


def example_arithmetic():
    """Example: Arithmetic operations with significant figures."""
    print("\n=== Example: Arithmetic with Significant Figures ===")
    
    # Addition
    a = SigFigNumber(123.45, 5)
    b = SigFigNumber(67.8, 3)
    print(f"\n  Addition:")
    print(f"    a = {a}")
    print(f"    b = {b}")
    result = add_sig_figs(a, b)
    print(f"    a + b = {result}")
    
    # Multiplication
    c = SigFigNumber(2.34, 3)
    d = SigFigNumber(5.6, 2)
    print(f"\n  Multiplication:")
    print(f"    c = {c}")
    print(f"    d = {d}")
    result = multiply_sig_figs(c, d)
    print(f"    c × d = {result}")
    
    # Operator overload
    e = SigFigNumber(10.0, 3)
    f = SigFigNumber(3.0, 2)
    print(f"\n  Using operators:")
    print(f"    e = {e}")
    print(f"    f = {f}")
    print(f"    e + f = {e + f}")
    print(f"    e × f = {e * f}")
    print(f"    e / f = {e / f}")


def example_measurement_uncertainty():
    """Example: Working with measurement uncertainties."""
    print("\n=== Example: Measurement Uncertainty ===")
    
    # Creating measured values
    print("\n  Creating measured values:")
    g = create_measured_value(9.81, 0.02, "m/s²")
    print(f"    g = {g}")
    print(f"    Relative uncertainty: {g.relative_uncertainty():.2f}%")
    
    # Formatting with uncertainty
    print("\n  Formatting:")
    formatted = format_with_uncertainty(12.34, 0.05, "cm")
    print(f"    {formatted}")
    
    # Propagation
    print("\n  Uncertainty propagation:")
    m1 = create_measured_value(2.50, 0.10, "kg")
    m2 = create_measured_value(1.30, 0.05, "kg")
    m_total = propagate_uncertainty_addition(m1, m2)
    print(f"    m1 = {m1}")
    print(f"    m2 = {m2}")
    print(f"    Total mass = {m_total}")
    
    # Multiplication example (area calculation)
    l = create_measured_value(5.0, 0.1, "m")
    w = create_measured_value(3.0, 0.1, "m")
    area = propagate_uncertainty_multiplication(l, w)
    print(f"\n    length = {l}")
    print(f"    width = {w}")
    print(f"    area = {area}")


def example_physics_lab():
    """Example: Physics lab calculation."""
    print("\n=== Example: Physics Lab Calculation ===")
    
    print("\n  Measuring gravitational acceleration:")
    
    # Measured values
    distance = create_measured_value(1.25, 0.01, "m")
    time = create_measured_value(0.50, 0.02, "s")
    
    print(f"    Distance fallen: {distance}")
    print(f"    Time to fall: {time}")
    
    # Calculate g = 2d / t²
    # Using significant figure arithmetic
    d_sf = SigFigNumber(distance.value, count_significant_figures(distance.value))
    t_sf = SigFigNumber(time.value, count_significant_figures(time.value))
    
    # g = 2 * d / t² (where 2 is exact)
    t_squared = t_sf ** 2
    two_times_d = SigFigNumber(2 * d_sf.value, d_sf.sig_figs)  # 2 is exact
    
    g_calc = two_times_d / t_squared
    
    print(f"\n    Calculated g ≈ {g_calc:.1f} m/s²")
    print(f"    (with proper sig fig handling)")
    
    # Percent error
    measured_g = g_calc.value
    accepted_g = 9.81
    error = calculate_percent_error(measured_g, accepted_g, 2)
    print(f"\n    Percent error: {error}")


def example_chemistry_lab():
    """Example: Chemistry concentration calculation."""
    print("\n=== Example: Chemistry Lab - Concentration ===")
    
    print("\n  Calculating molarity:")
    
    # Measured mass and volume
    mass = SigFigNumber(5.82, 3)  # grams
    volume = SigFigNumber(250.0, 3)  # mL
    
    # Molar mass (exact)
    molar_mass = 58.44  # g/mol (NaCl - exact to many sig figs)
    
    # Moles = mass / molar_mass
    moles = mass / SigFigNumber(molar_mass, 4)
    
    # Convert volume to L (exact conversion)
    volume_L = SigFigNumber(volume.value / 1000, volume.sig_figs)
    
    # Molarity = moles / volume(L)
    molarity = moles / volume_L
    
    print(f"    Mass of NaCl: {mass} g")
    print(f"    Volume: {volume} mL")
    print(f"    Molar mass: {molar_mass} g/mol (exact)")
    print(f"\n    Moles: {moles} mol")
    print(f"    Volume in L: {volume_L} L")
    print(f"    Molarity: {molarity} M")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Significant Figures Utilities - Examples")
    print("=" * 60)
    
    example_counting_sig_figs()
    example_rounding()
    example_scientific_notation()
    example_arithmetic()
    example_measurement_uncertainty()
    example_physics_lab()
    example_chemistry_lab()
    
    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()