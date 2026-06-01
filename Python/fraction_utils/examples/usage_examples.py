#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fraction Utilities - Usage Examples
"""

from fraction_utils.mod import (
    Fraction, fraction_sum, fraction_product, fraction_stats,
    egyptian_fraction, diophantine_solution, format_fraction,
    fraction_to_latex, fraction_to_unicode, FractionStats
)


def basic_examples():
    """Basic fraction operations."""
    print("=== Basic Fraction Examples ===")
    
    # Create fractions
    f1 = Fraction(3, 4)
    f2 = Fraction(1, 6)
    print(f"f1 = {f1}")
    print(f"f2 = {f2}")
    
    # Arithmetic
    print(f"f1 + f2 = {f1 + f2}")
    print(f"f1 - f2 = {f1 - f2}")
    print(f"f1 * f2 = {f1 * f2}")
    print(f"f1 / f2 = {f1 / f2}")
    
    # Comparison
    print(f"f1 > f2: {f1 > f2}")
    print(f"f1 == Fraction(6, 8): {f1 == Fraction(6, 8)}")
    
    # Power
    print(f"f1 ** 2 = {f1 ** 2}")
    print(f"f1 ** -1 = {f1 ** -1} (reciprocal)")
    print()


def properties_examples():
    """Fraction properties."""
    print("=== Fraction Properties ===")
    
    f = Fraction(7, 4)
    print(f"Fraction: {f}")
    print(f"  Is zero: {f.is_zero}")
    print(f"  Is integer: {f.is_integer}")
    print(f"  Is positive: {f.is_positive}")
    print(f"  Is proper: {f.is_proper}")
    print(f"  Is unit: {f.is_unit}")
    
    whole, frac = f.mixed_number
    print(f"  Mixed number: {whole} + {frac}")
    
    # Reciprocal
    print(f"  Reciprocal: {f.reciprocal()}")
    print()


def float_conversion_examples():
    """Converting floats to fractions."""
    print("=== Float to Fraction Conversion ===")
    
    test_floats = [0.5, 0.75, 0.333, 0.142857, 3.14159265]
    for val in test_floats:
        f = Fraction.from_float(val)
        print(f"{val} -> {f} (float: {float(f):.6f})")
    print()


def string_parsing_examples():
    """Parsing fractions from strings."""
    print("=== String Parsing ===")
    
    strings = ["3/4", "1 1/2", "-5/6", "42", "7/14"]
    for s in strings:
        f = Fraction.from_string(s)
        print(f"'{s}' -> {f}")
    print()


def continued_fraction_examples():
    """Continued fraction operations."""
    print("=== Continued Fractions ===")
    
    # Pi approximation
    pi_frac = Fraction.from_float(3.14159265358979, tolerance=1e-10)
    print(f"Pi approximation: {pi_frac}")
    print(f"  Continued fraction: {pi_frac.continued_fraction}")
    
    # Golden ratio (should give Fibonacci terms)
    phi = (1 + 5**0.5) / 2
    phi_frac = Fraction.from_float(phi)
    print(f"Golden ratio: {phi_frac}")
    print(f"  Continued fraction: {phi_frac.continued_fraction}")
    
    # Roundtrip
    original = Fraction(22, 7)
    cf = original.continued_fraction
    reconstructed = Fraction.from_continued_fraction(cf)
    print(f"{original} via CF -> {reconstructed}")
    print()


def egyptian_fraction_examples():
    """Egyptian fraction decomposition."""
    print("=== Egyptian Fractions ===")
    
    fractions = [Fraction(2, 3), Fraction(3, 4), Fraction(4, 5)]
    for f in fractions:
        result = egyptian_fraction(f)
        total = fraction_sum(result)
        terms = " + ".join(str(x) for x in result)
        print(f"{f} = {terms}")
        print(f"  Verification: {total}")
    print()


def diophantine_examples():
    """Solving Diophantine equations."""
    print("=== Diophantine Equations ===")
    
    equations = [
        (2, 3, 11),
        (5, 7, 23),
        (12, 8, 32),
    ]
    for a, b, c in equations:
        result = diophantine_solution(a, b, c)
        if result:
            x, y = result
            print(f"{a}x + {b}y = {c}")
            print(f"  Solution: x={x}, y={y}")
            print(f"  Verification: {a*x + b*y}")
        else:
            print(f"{a}x + {b}y = {c} has no integer solution")
    print()


def statistics_examples():
    """Statistics on fractions."""
    print("=== Fraction Statistics ===")
    
    fractions = [
        Fraction(1, 4),
        Fraction(1, 2),
        Fraction(3, 4),
        Fraction(1, 3),
        Fraction(2, 3),
    ]
    
    stats = fraction_stats(fractions)
    print(f"Count: {stats.count}")
    print(f"Sum: {stats.sum}")
    print(f"Mean: {stats.mean}")
    print(f"Min: {stats.min}")
    print(f"Max: {stats.max}")
    print(f"Median: {stats.median}")
    print()


def farey_sequence_examples():
    """Farey sequence generation."""
    print("=== Farey Sequences ===")
    
    for n in [3, 4, 5]:
        seq = Fraction.farey_sequence(n)
        print(f"Order {n}:")
        print("  " + ", ".join(str(f) for f in seq))
    print()


def formatting_examples():
    """Various formatting options."""
    print("=== Formatting ===")
    
    f = Fraction(5, 2)
    print(f"Normal: {format_fraction(f)}")
    print(f"Mixed: {format_fraction(f, 'mixed')}")
    print(f"LaTeX: {format_fraction(f, 'latex')}")
    
    # Unicode fractions
    for denom in [2, 3, 4, 5, 6, 7, 8]:
        u = format_fraction(Fraction(1, denom), 'unicode')
        print(f"  1/{denom} = {u}")
    print()


def mediant_examples():
    """Mediant (farey sum) examples."""
    print("=== Mediant Examples ===")
    
    pairs = [
        (Fraction(1, 2), Fraction(1, 3)),
        (Fraction(2, 3), Fraction(3, 4)),
        (Fraction(1, 4), Fraction(3, 4)),
    ]
    
    for f1, f2 in pairs:
        m = Fraction.mediant(f1, f2)
        print(f"mediant({f1}, {f2}) = {m}")
    print()


def utility_examples():
    """Utility function examples."""
    print("=== Utility Functions ===")
    
    from fraction_utils.mod import _gcd, _lcm
    
    pairs = [(12, 18), (7, 13), (24, 36)]
    for a, b in pairs:
        print(f"GCD({a}, {b}) = {_gcd(a, b)}")
        print(f"LCM({a}, {b}) = {_lcm(a, b)}")
    print()


if __name__ == "__main__":
    basic_examples()
    properties_examples()
    float_conversion_examples()
    string_parsing_examples()
    continued_fraction_examples()
    egyptian_fraction_examples()
    diophantine_examples()
    statistics_examples()
    farey_sequence_examples()
    formatting_examples()
    mediant_examples()
    utility_examples()