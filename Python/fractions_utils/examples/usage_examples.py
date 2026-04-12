#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Fractions Utilities Usage Examples
================================================
Practical examples demonstrating various use cases for the fractions_utils module.
"""

import sys
import os
from fractions import Fraction

# Add parent directory to path to import mod
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import *


def example_basic_operations():
    """Example 1: Basic arithmetic operations with fractions."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Arithmetic Operations")
    print("=" * 60)
    
    # Create fractions in various ways
    f1 = parse_fraction("3/4")
    f2 = parse_fraction(0.5)
    f3 = create_fraction(2, 3)
    
    print(f"f1 = 3/4 = {f1}")
    print(f"f2 = 0.5 = {f2}")
    print(f"f3 = 2/3 = {f3}")
    
    # Arithmetic operations
    print(f"\nf1 + f2 = {add(f1, f2)} ({to_decimal(add(f1, f2))})")
    print(f"f1 - f2 = {subtract(f1, f2)} ({to_decimal(subtract(f1, f2))})")
    print(f"f1 * f3 = {multiply(f1, f3)} ({to_decimal(multiply(f1, f3))})")
    print(f"f1 / f2 = {divide(f1, f2)} ({to_decimal(divide(f1, f2))})")
    
    # Power and reciprocal
    print(f"\nf1^2 = {power(f1, 2)}")
    print(f"reciprocal(f3) = {reciprocal(f3)}")
    print(f"negate(f1) = {negate(f1)}")
    print(f"abs(negate(f1)) = {abs_fraction(negate(f1))}")


def example_comparison():
    """Example 2: Comparing fractions."""
    print("\n" + "=" * 60)
    print("Example 2: Comparing Fractions")
    print("=" * 60)
    
    fractions = ["3/4", "5/6", "7/8", "2/3", "11/12"]
    
    print("Original fractions:", fractions)
    
    # Sort fractions
    sorted_fracs = sorted(fractions, key=lambda x: parse_fraction(x))
    print("Sorted (ascending):", [to_string(f) for f in sorted_fracs])
    
    # Find min and max
    print(f"\nMinimum: {min_fraction(*fractions)}")
    print(f"Maximum: {max_fraction(*fractions)}")
    
    # Pairwise comparisons
    print("\nPairwise comparisons:")
    for i in range(len(fractions) - 1):
        a, b = fractions[i], fractions[i + 1]
        cmp_result = compare(a, b)
        relation = " < " if cmp_result < 0 else " = " if cmp_result == 0 else " > "
        print(f"  {a}{relation}{b}")


def example_common_denominator():
    """Example 3: Finding common denominators."""
    print("\n" + "=" * 60)
    print("Example 3: Common Denominators")
    print("=" * 60)
    
    fractions = ["1/4", "1/6", "1/8"]
    
    print(f"Fractions: {fractions}")
    print(f"Least common denominator: {common_denominator(*fractions)}")
    
    # Convert to common denominator
    common = with_common_denominator(*fractions)
    print("\nWith common denominator:")
    for orig, converted in zip(fractions, common):
        print(f"  {orig} = {converted}")
    
    # Add them up
    total = sum_fractions(fractions)
    print(f"\nSum: {to_string(total, 'mixed')} ({to_decimal(total)})")


def example_conversions():
    """Example 4: Converting between formats."""
    print("\n" + "=" * 60)
    print("Example 4: Format Conversions")
    print("=" * 60)
    
    test_values = ["3/4", "7/4", "1/3", "5/2", "22/7"]
    
    print(f"{'Fraction':<10} {'Decimal':<12} {'Percentage':<12} {'Mixed':<10}")
    print("-" * 50)
    
    for val in test_values:
        f = parse_fraction(val)
        dec = to_decimal(f)
        pct = to_percentage(f)
        mixed = to_string(f, 'mixed')
        print(f"{val:<10} {dec:<12.4f} {pct:<12.2f}% {mixed:<10}")


def example_mixed_numbers():
    """Example 5: Working with mixed numbers."""
    print("\n" + "=" * 60)
    print("Example 5: Mixed Numbers")
    print("=" * 60)
    
    # Convert improper to mixed
    improper = ["5/2", "7/3", "17/4", "100/7"]
    
    print("Improper → Mixed:")
    for imp in improper:
        whole, frac = to_mixed_number(imp)
        if frac == 0:
            print(f"  {imp} = {whole}")
        else:
            print(f"  {imp} = {whole} {frac.numerator}/{frac.denominator}")
    
    # Convert mixed to improper
    print("\nMixed → Improper:")
    mixed_cases = [(2, 1, 3), (5, 3, 4), (10, 1, 2)]
    for whole, num, denom in mixed_cases:
        improper = to_improper_fraction(whole, num, denom)
        print(f"  {whole} {num}/{denom} = {improper}")


def example_gcd_lcm():
    """Example 6: GCD and LCM calculations."""
    print("\n" + "=" * 60)
    print("Example 6: GCD and LCM")
    print("=" * 60)
    
    # GCD examples
    print("GCD calculations:")
    print(f"  gcd(12, 18) = {gcd(12, 18)}")
    print(f"  gcd(12, 18, 24) = {gcd(12, 18, 24)}")
    print(f"  gcd(17, 19) = {gcd(17, 19)} (coprime)")
    print(f"  gcd(100, 50, 25) = {gcd(100, 50, 25)}")
    
    # LCM examples
    print("\nLCM calculations:")
    print(f"  lcm(4, 6) = {lcm(4, 6)}")
    print(f"  lcm(4, 6, 8) = {lcm(4, 6, 8)}")
    print(f"  lcm(3, 5, 7) = {lcm(3, 5, 7)} (coprime)")
    print(f"  lcm(12, 18) = {lcm(12, 18)}")


def example_sequences():
    """Example 7: Arithmetic and geometric sequences."""
    print("\n" + "=" * 60)
    print("Example 7: Sequences and Series")
    print("=" * 60)
    
    # Arithmetic sequence
    print("Arithmetic sequence (first=1, diff=2, n=10):")
    arith_seq = arithmetic_sequence(1, 2, 10)
    print(f"  {[str(f) for f in arith_seq]}")
    print(f"  Sum: {arithmetic_series_sum(1, 2, 10)}")
    
    # Geometric sequence
    print("\nGeometric sequence (first=1, ratio=1/2, n=10):")
    geom_seq = geometric_sequence(1, "1/2", 10)
    print(f"  {[to_string(f) for f in geom_seq]}")
    print(f"  Sum (first 10 terms): {geometric_series_sum(1, '1/2', 10)}")
    
    # Infinite geometric series
    print("\nInfinite geometric series:")
    print(f"  1/2 + 1/4 + 1/8 + ... = {infinite_geometric_series_sum('1/2', '1/2')}")
    print(f"  1/3 + 1/9 + 1/27 + ... = {infinite_geometric_series_sum('1/3', '1/3')}")
    print(f"  1 + 1/2 + 1/4 + ... = {infinite_geometric_series_sum(1, '1/2')}")


def example_batch_operations():
    """Example 8: Batch operations on lists of fractions."""
    print("\n" + "=" * 60)
    print("Example 8: Batch Operations")
    print("=" * 60)
    
    fractions = ["1/2", "1/3", "1/4", "1/5", "1/6"]
    
    print(f"Fractions: {fractions}")
    print(f"Sum: {sum_fractions(fractions)} ({to_decimal(sum_fractions(fractions)):.4f})")
    print(f"Product: {product_fractions(fractions)}")
    print(f"Average: {average_fractions(fractions)} ({to_decimal(average_fractions(fractions)):.4f})")
    
    # Map: get reciprocals
    reciprocals = map_fractions(fractions, reciprocal)
    print(f"\nReciprocals: {[str(f) for f in reciprocals]}")
    
    # Filter: keep fractions > 1/4
    filtered = filter_fractions(fractions, lambda x: x > Fraction(1, 4))
    print(f"Fractions > 1/4: {[str(f) for f in filtered]}")


def example_special_fractions():
    """Example 9: Special fraction types."""
    print("\n" + "=" * 60)
    print("Example 9: Special Fraction Types")
    print("=" * 60)
    
    test_values = ["3/4", "5/4", "1/7", "4/2", "7/1", "0/5"]
    
    print(f"{'Fraction':<10} {'Proper?':<8} {'Unit?':<8} {'Integer?':<10} {'Denom Digits':<12}")
    print("-" * 55)
    
    for val in test_values:
        f = parse_fraction(val)
        proper = is_proper_fraction(f)
        unit = is_unit_fraction(f)
        integer = is_integer(f)
        denom_digits = denominator_count(f)
        print(f"{val:<10} {str(proper):<8} {str(unit):<8} {str(integer):<10} {denom_digits:<12}")


def example_approximation():
    """Example 10: Fraction approximation."""
    print("\n" + "=" * 60)
    print("Example 10: Fraction Approximation")
    print("=" * 60)
    
    # Approximate famous constants
    constants = [
        ("π (pi)", 3.14159265359),
        ("e (Euler)", 2.71828182845),
        ("√2 (sqrt 2)", 1.41421356237),
        ("φ (golden ratio)", 1.61803398874),
    ]
    
    print(f"{'Constant':<20} {'Value':<12} {'Approximation':<12} {'Error':<15}")
    print("-" * 65)
    
    for name, value in constants:
        approx = approximate(value, max_denominator=1000)
        error = abs(float(approx) - value)
        print(f"{name:<20} {value:<12.6f} {str(approx):<12} {error:<15.10f}")
    
    # Approximate with different max denominators
    print("\nApproximating π with different max denominators:")
    for max_denom in [10, 100, 1000, 10000]:
        approx = approximate(3.14159265359, max_denominator=max_denom)
        print(f"  max_denom={max_denom:<5} → {str(approx):<10} (error: {abs(float(approx) - 3.14159265359):.10f})")


def example_real_world():
    """Example 11: Real-world application - Recipe scaling."""
    print("\n" + "=" * 60)
    print("Example 11: Real-World Application - Recipe Scaling")
    print("=" * 60)
    
    # Original recipe (makes 12 cookies)
    recipe = {
        'flour': parse_fraction("2 1/4"),      # 2.25 cups
        'sugar': parse_fraction("3/4"),         # 0.75 cups
        'butter': parse_fraction("1/2"),        # 0.5 cups
        'eggs': parse_fraction("2"),            # 2 eggs
        'vanilla': parse_fraction("1 1/2"),     # 1.5 tsp
        'salt': parse_fraction("1/4"),          # 0.25 tsp
    }
    
    print("Original recipe (12 cookies):")
    for ingredient, amount in recipe.items():
        print(f"  {ingredient}: {to_string(amount, 'mixed')}")
    
    # Scale to different quantities
    for target_cookies in [6, 24, 36]:
        scale = Fraction(target_cookies, 12)
        print(f"\nScaled recipe ({target_cookies} cookies, scale factor {scale}):")
        for ingredient, amount in recipe.items():
            scaled = multiply(amount, scale)
            print(f"  {ingredient}: {to_string(scaled, 'mixed')}")


def example_percentage_calculations():
    """Example 12: Percentage calculations."""
    print("\n" + "=" * 60)
    print("Example 12: Percentage Calculations")
    print("=" * 60)
    
    # Common percentages
    percentages = [1, 5, 10, 20, 25, 33, 50, 66, 75, 100, 150, 200]
    
    print(f"{'Percentage':<12} {'Fraction':<12} {'Decimal':<10}")
    print("-" * 40)
    
    for pct in percentages:
        frac = from_percentage(pct)
        dec = to_decimal(frac)
        print(f"{pct}%{'':<8} {str(frac):<12} {dec:<10.4f}")
    
    # Calculate discounts
    print("\nDiscount calculations (original price: $100):")
    original_price = Fraction(100, 1)
    for discount in [10, 20, 25, 50]:
        discount_frac = from_percentage(discount)
        savings = multiply(original_price, discount_frac)
        final_price = subtract(original_price, savings)
        print(f"  {discount}% off: save ${to_decimal(savings)}, pay ${to_decimal(final_price)}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("  AllToolkit - Fractions Utilities Examples")
    print("=" * 60)
    
    example_basic_operations()
    example_comparison()
    example_common_denominator()
    example_conversions()
    example_mixed_numbers()
    example_gcd_lcm()
    example_sequences()
    example_batch_operations()
    example_special_fractions()
    example_approximation()
    example_real_world()
    example_percentage_calculations()
    
    print("\n" + "=" * 60)
    print("  All examples completed!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
