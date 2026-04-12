#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Fractions Utilities Module
========================================
A comprehensive fraction math utility module for Python with zero external dependencies.

Features:
    - Fraction creation and parsing
    - Arithmetic operations (add, subtract, multiply, divide)
    - Comparison operations
    - Simplification and normalization
    - Conversion to/from decimal, percentage, mixed numbers
    - GCD/LCM utilities
    - Batch operations
    - Fraction sequences and series

Author: AllToolkit Contributors
License: MIT
"""

from fractions import Fraction
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
from functools import reduce
import math
import re


# ============================================================================
# Type Aliases
# ============================================================================

FractionLike = Union[int, float, str, Fraction, Tuple[int, int]]


# ============================================================================
# Fraction Creation and Parsing
# ============================================================================

def create_fraction(numerator: int, denominator: int) -> Fraction:
    """
    Create a Fraction from numerator and denominator.
    
    Args:
        numerator: The numerator
        denominator: The denominator (must not be zero)
    
    Returns:
        A Fraction object
    
    Raises:
        ZeroDivisionError: If denominator is zero
    
    Example:
        >>> create_fraction(3, 4)
        Fraction(3, 4)
        >>> create_fraction(6, 8)
        Fraction(3, 4)
    """
    if denominator == 0:
        raise ZeroDivisionError("Denominator cannot be zero")
    return Fraction(numerator, denominator)


def parse_fraction(value: FractionLike) -> Fraction:
    """
    Parse various input types into a Fraction.
    
    Args:
        value: Can be int, float, str, Fraction, or tuple (numerator, denominator)
    
    Returns:
        A Fraction object
    
    Raises:
        ValueError: If the input cannot be parsed
        ZeroDivisionError: If denominator is zero
    
    Example:
        >>> parse_fraction("3/4")
        Fraction(3, 4)
        >>> parse_fraction(0.75)
        Fraction(3, 4)
        >>> parse_fraction((3, 4))
        Fraction(3, 4)
        >>> parse_fraction(2)
        Fraction(2, 1)
    """
    if isinstance(value, Fraction):
        return value
    
    if isinstance(value, int):
        return Fraction(value)
    
    if isinstance(value, float):
        return Fraction(value).limit_denominator(10**12)
    
    if isinstance(value, tuple):
        if len(value) != 2:
            raise ValueError(f"Tuple must have exactly 2 elements, got {len(value)}")
        return create_fraction(value[0], value[1])
    
    if isinstance(value, str):
        value = value.strip()
        
        # Handle mixed numbers like "1 1/2" or "1+1/2"
        mixed_match = re.match(r'^(-?\d+)\s*[+\s]\s*(\d+)/(\d+)$', value)
        if mixed_match:
            whole = int(mixed_match.group(1))
            num = int(mixed_match.group(2))
            denom = int(mixed_match.group(3))
            if denom == 0:
                raise ZeroDivisionError("Denominator cannot be zero")
            sign = -1 if whole < 0 else 1
            return Fraction(whole * denom + sign * num, denom)
        
        # Handle simple fractions like "3/4"
        if '/' in value:
            parts = value.split('/')
            if len(parts) != 2:
                raise ValueError(f"Invalid fraction format: {value}")
            return create_fraction(int(parts[0]), int(parts[1]))
        
        # Handle decimal strings like "0.75"
        try:
            return Fraction(value).limit_denominator(10**12)
        except (ValueError, ZeroDivisionError):
            raise ValueError(f"Cannot parse '{value}' as a fraction")
    
    raise ValueError(f"Cannot parse type {type(value)} as a fraction")


def from_decimal(value: float, max_denominator: int = 10**12) -> Fraction:
    """
    Convert a decimal to a Fraction with limited denominator.
    
    Args:
        value: The decimal value
        max_denominator: Maximum allowed denominator (default: 10^12)
    
    Returns:
        A Fraction approximation
    
    Example:
        >>> from_decimal(0.333333)
        Fraction(1, 3)
        >>> from_decimal(3.14159, max_denominator=100)
        Fraction(311, 99)
    """
    return Fraction(value).limit_denominator(max_denominator)


def from_percentage(percentage: Union[int, float, str]) -> Fraction:
    """
    Convert a percentage to a Fraction.
    
    Args:
        percentage: The percentage value (e.g., 25 for 25%)
    
    Returns:
        A Fraction representing the percentage
    
    Example:
        >>> from_percentage(25)
        Fraction(1, 4)
        >>> from_percentage("150%")
        Fraction(3, 2)
        >>> from_percentage(0.5)
        Fraction(1, 200)
    """
    if isinstance(percentage, str):
        percentage = percentage.replace('%', '')
        # Check if it's a decimal string like "0.5%" or integer like "50%"
        if '.' in percentage:
            percentage = float(percentage)
        else:
            percentage = int(percentage)
    
    if isinstance(percentage, float):
        return Fraction(percentage).limit_denominator(10**12) / 100
    return Fraction(percentage, 100)


# ============================================================================
# Arithmetic Operations
# ============================================================================

def add(*fractions: FractionLike) -> Fraction:
    """
    Add multiple fractions together.
    
    Args:
        *fractions: One or more fraction-like values
    
    Returns:
        The sum as a Fraction
    
    Example:
        >>> add("1/2", "1/3")
        Fraction(5, 6)
        >>> add(1, "1/2", "1/4")
        Fraction(7, 4)
    """
    if not fractions:
        return Fraction(0)
    parsed = [parse_fraction(f) for f in fractions]
    return sum(parsed)


def subtract(minuend: FractionLike, *subtrahends: FractionLike) -> Fraction:
    """
    Subtract one or more fractions from a minuend.
    
    Args:
        minuend: The value to subtract from
        *subtrahends: Values to subtract
    
    Returns:
        The difference as a Fraction
    
    Example:
        >>> subtract("3/4", "1/2")
        Fraction(1, 4)
        >>> subtract(1, "1/2", "1/4")
        Fraction(1, 4)
    """
    result = parse_fraction(minuend)
    for sub in subtrahends:
        result -= parse_fraction(sub)
    return result


def multiply(*fractions: FractionLike) -> Fraction:
    """
    Multiply multiple fractions together.
    
    Args:
        *fractions: One or more fraction-like values
    
    Returns:
        The product as a Fraction
    
    Example:
        >>> multiply("1/2", "2/3", "3/4")
        Fraction(1, 4)
    """
    if not fractions:
        return Fraction(1)
    parsed = [parse_fraction(f) for f in fractions]
    return reduce(lambda x, y: x * y, parsed)


def divide(dividend: FractionLike, *divisors: FractionLike) -> Fraction:
    """
    Divide a dividend by one or more divisors.
    
    Args:
        dividend: The value to be divided
        *divisors: Values to divide by
    
    Returns:
        The quotient as a Fraction
    
    Raises:
        ZeroDivisionError: If any divisor is zero
    
    Example:
        >>> divide("3/4", "1/2")
        Fraction(3, 2)
        >>> divide(1, "1/2", "1/4")
        Fraction(8, 1)
    """
    result = parse_fraction(dividend)
    for div in divisors:
        divisor = parse_fraction(div)
        if divisor == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result /= divisor
    return result


def power(base: FractionLike, exponent: Union[int, float]) -> Fraction:
    """
    Raise a fraction to a power.
    
    Args:
        base: The base fraction
        exponent: The exponent (should be integer for exact results)
    
    Returns:
        The result as a Fraction
    
    Example:
        >>> power("1/2", 3)
        Fraction(1, 8)
        >>> power("2/3", 2)
        Fraction(4, 9)
    """
    base_frac = parse_fraction(base)
    if isinstance(exponent, float) and not exponent.is_integer():
        # For non-integer exponents, convert to float operation
        return Fraction(float(base_frac) ** exponent).limit_denominator(10**12)
    return base_frac ** int(exponent)


def reciprocal(fraction: FractionLike) -> Fraction:
    """
    Get the reciprocal (multiplicative inverse) of a fraction.
    
    Args:
        fraction: The input fraction
    
    Returns:
        The reciprocal as a Fraction
    
    Raises:
        ZeroDivisionError: If the fraction is zero
    
    Example:
        >>> reciprocal("3/4")
        Fraction(4, 3)
        >>> reciprocal(5)
        Fraction(1, 5)
    """
    frac = parse_fraction(fraction)
    if frac == 0:
        raise ZeroDivisionError("Cannot get reciprocal of zero")
    return Fraction(frac.denominator, frac.numerator)


def negate(fraction: FractionLike) -> Fraction:
    """
    Negate a fraction (multiply by -1).
    
    Args:
        fraction: The input fraction
    
    Returns:
        The negated fraction
    
    Example:
        >>> negate("3/4")
        Fraction(-3, 4)
        >>> negate(-5)
        Fraction(5, 1)
    """
    return -parse_fraction(fraction)


def abs_fraction(fraction: FractionLike) -> Fraction:
    """
    Get the absolute value of a fraction.
    
    Args:
        fraction: The input fraction
    
    Returns:
        The absolute value as a Fraction
    
    Example:
        >>> abs_fraction("-3/4")
        Fraction(3, 4)
    """
    return abs(parse_fraction(fraction))


# ============================================================================
# Comparison Operations
# ============================================================================

def compare(a: FractionLike, b: FractionLike) -> int:
    """
    Compare two fractions.
    
    Args:
        a: First fraction
        b: Second fraction
    
    Returns:
        -1 if a < b, 0 if a == b, 1 if a > b
    
    Example:
        >>> compare("1/2", "2/3")
        -1
        >>> compare("2/4", "1/2")
        0
        >>> compare("3/4", "1/2")
        1
    """
    a_frac = parse_fraction(a)
    b_frac = parse_fraction(b)
    if a_frac < b_frac:
        return -1
    elif a_frac > b_frac:
        return 1
    return 0


def equals(a: FractionLike, b: FractionLike) -> bool:
    """Check if two fractions are equal."""
    return parse_fraction(a) == parse_fraction(b)


def less_than(a: FractionLike, b: FractionLike) -> bool:
    """Check if a is less than b."""
    return parse_fraction(a) < parse_fraction(b)


def greater_than(a: FractionLike, b: FractionLike) -> bool:
    """Check if a is greater than b."""
    return parse_fraction(a) > parse_fraction(b)


def less_than_or_equal(a: FractionLike, b: FractionLike) -> bool:
    """Check if a is less than or equal to b."""
    return parse_fraction(a) <= parse_fraction(b)


def greater_than_or_equal(a: FractionLike, b: FractionLike) -> bool:
    """Check if a is greater than or equal to b."""
    return parse_fraction(a) >= parse_fraction(b)


def min_fraction(*fractions: FractionLike) -> Fraction:
    """
    Find the minimum of multiple fractions.
    
    Args:
        *fractions: One or more fraction-like values
    
    Returns:
        The smallest fraction
    
    Example:
        >>> min_fraction("1/2", "1/3", "1/4")
        Fraction(1, 4)
    """
    if not fractions:
        raise ValueError("At least one fraction required")
    parsed = [parse_fraction(f) for f in fractions]
    return min(parsed)


def max_fraction(*fractions: FractionLike) -> Fraction:
    """
    Find the maximum of multiple fractions.
    
    Args:
        *fractions: One or more fraction-like values
    
    Returns:
        The largest fraction
    
    Example:
        >>> max_fraction("1/2", "2/3", "3/4")
        Fraction(3, 4)
    """
    if not fractions:
        raise ValueError("At least one fraction required")
    parsed = [parse_fraction(f) for f in fractions]
    return max(parsed)


# ============================================================================
# Simplification and Normalization
# ============================================================================

def simplify(fraction: FractionLike) -> Fraction:
    """
    Simplify a fraction to lowest terms.
    
    Args:
        fraction: The input fraction
    
    Returns:
        The simplified fraction
    
    Example:
        >>> simplify("6/8")
        Fraction(3, 4)
        >>> simplify("100/150")
        Fraction(2, 3)
    """
    return parse_fraction(fraction)  # Fraction automatically simplifies


def normalize(fraction: FractionLike) -> Fraction:
    """
    Normalize a fraction (ensure positive denominator).
    
    Args:
        fraction: The input fraction
    
    Returns:
        The normalized fraction
    
    Example:
        >>> normalize("3/-4")
        Fraction(-3, 4)
    """
    frac = parse_fraction(fraction)
    return Fraction(frac.numerator, frac.denominator)


def to_mixed_number(fraction: FractionLike) -> Tuple[int, Fraction]:
    """
    Convert an improper fraction to a mixed number.
    
    Args:
        fraction: The input fraction
    
    Returns:
        A tuple of (whole_number, fractional_part)
    
    Example:
        >>> to_mixed_number("7/4")
        (1, Fraction(3, 4))
        >>> to_mixed_number("5/2")
        (2, Fraction(1, 2))
    """
    frac = parse_fraction(fraction)
    whole = frac.numerator // frac.denominator
    remainder = abs(frac.numerator % frac.denominator)
    return (whole, Fraction(remainder, frac.denominator))


def to_improper_fraction(whole: int, numerator: int, denominator: int) -> Fraction:
    """
    Convert a mixed number to an improper fraction.
    
    Args:
        whole: The whole number part
        numerator: The numerator of the fractional part
        denominator: The denominator of the fractional part
    
    Returns:
        The improper fraction
    
    Example:
        >>> to_improper_fraction(1, 3, 4)
        Fraction(7, 4)
    """
    if denominator == 0:
        raise ZeroDivisionError("Denominator cannot be zero")
    sign = -1 if whole < 0 else 1
    return Fraction(whole * denominator + sign * numerator, denominator)


# ============================================================================
# Conversion Functions
# ============================================================================

def to_decimal(fraction: FractionLike, precision: int = 10) -> float:
    """
    Convert a fraction to a decimal.
    
    Args:
        fraction: The input fraction
        precision: Number of decimal places (default: 10)
    
    Returns:
        The decimal representation
    
    Example:
        >>> to_decimal("1/3")
        0.3333333333
        >>> to_decimal("1/4")
        0.25
    """
    return round(float(parse_fraction(fraction)), precision)


def to_percentage(fraction: FractionLike, precision: int = 2) -> float:
    """
    Convert a fraction to a percentage.
    
    Args:
        fraction: The input fraction
        precision: Number of decimal places (default: 2)
    
    Returns:
        The percentage value
    
    Example:
        >>> to_percentage("1/4")
        25.0
        >>> to_percentage("1/3")
        33.33
    """
    return round(float(parse_fraction(fraction)) * 100, precision)


def to_string(fraction: FractionLike, format_type: str = 'fraction') -> str:
    """
    Convert a fraction to a string representation.
    
    Args:
        fraction: The input fraction
        format_type: One of 'fraction', 'decimal', 'percentage', 'mixed'
    
    Returns:
        String representation
    
    Example:
        >>> to_string("3/4", 'fraction')
        '3/4'
        >>> to_string("3/4", 'decimal')
        '0.75'
        >>> to_string("3/4", 'percentage')
        '75.0%'
        >>> to_string("7/4", 'mixed')
        '1 3/4'
    """
    frac = parse_fraction(fraction)
    
    if format_type == 'fraction':
        if frac.denominator == 1:
            return str(frac.numerator)
        return f"{frac.numerator}/{frac.denominator}"
    
    elif format_type == 'decimal':
        return str(float(frac))
    
    elif format_type == 'percentage':
        return f"{float(frac) * 100}%"
    
    elif format_type == 'mixed':
        whole, remainder = to_mixed_number(frac)
        if remainder == 0:
            return str(whole)
        if whole == 0:
            return f"{remainder.numerator}/{remainder.denominator}"
        return f"{whole} {remainder.numerator}/{remainder.denominator}"
    
    else:
        raise ValueError(f"Unknown format type: {format_type}")


# ============================================================================
# GCD/LCM Utilities
# ============================================================================

def gcd(*numbers: int) -> int:
    """
    Calculate the Greatest Common Divisor of multiple integers.
    
    Args:
        *numbers: One or more integers
    
    Returns:
        The GCD
    
    Example:
        >>> gcd(12, 18)
        6
        >>> gcd(12, 18, 24)
        6
    """
    if not numbers:
        return 0
    return reduce(math.gcd, numbers)


def lcm(*numbers: int) -> int:
    """
    Calculate the Least Common Multiple of multiple integers.
    
    Args:
        *numbers: One or more integers
    
    Returns:
        The LCM
    
    Example:
        >>> lcm(4, 6)
        12
        >>> lcm(4, 6, 8)
        24
    """
    if not numbers:
        return 1
    
    def lcm_two(a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // math.gcd(a, b)
    
    return reduce(lcm_two, numbers)


def common_denominator(*fractions: FractionLike) -> int:
    """
    Find a common denominator for multiple fractions.
    
    Args:
        *fractions: One or more fraction-like values
    
    Returns:
        The least common denominator
    
    Example:
        >>> common_denominator("1/4", "1/6", "1/8")
        24
    """
    if not fractions:
        return 1
    parsed = [parse_fraction(f) for f in fractions]
    denominators = [f.denominator for f in parsed]
    return lcm(*denominators)


def with_common_denominator(*fractions: FractionLike) -> List[Fraction]:
    """
    Convert multiple fractions to have a common denominator.
    
    Args:
        *fractions: One or more fraction-like values
    
    Returns:
        List of fractions with the same denominator
    
    Example:
        >>> with_common_denominator("1/4", "1/6")
        [Fraction(3, 12), Fraction(2, 12)]
    """
    if not fractions:
        return []
    
    parsed = [parse_fraction(f) for f in fractions]
    common_denom = common_denominator(*fractions)
    
    result = []
    for frac in parsed:
        multiplier = common_denom // frac.denominator
        result.append(Fraction(frac.numerator * multiplier, common_denom))
    
    return result


# ============================================================================
# Batch Operations
# ============================================================================

def sum_fractions(fractions: List[FractionLike]) -> Fraction:
    """
    Sum a list of fractions.
    
    Args:
        fractions: List of fraction-like values
    
    Returns:
        The sum as a Fraction
    
    Example:
        >>> sum_fractions(["1/2", "1/3", "1/6"])
        Fraction(1, 1)
    """
    return add(*fractions)


def product_fractions(fractions: List[FractionLike]) -> Fraction:
    """
    Calculate the product of a list of fractions.
    
    Args:
        fractions: List of fraction-like values
    
    Returns:
        The product as a Fraction
    
    Example:
        >>> product_fractions(["1/2", "2/3", "3/4"])
        Fraction(1, 4)
    """
    return multiply(*fractions)


def average_fractions(fractions: List[FractionLike]) -> Fraction:
    """
    Calculate the average of a list of fractions.
    
    Args:
        fractions: List of fraction-like values
    
    Returns:
        The average as a Fraction
    
    Example:
        >>> average_fractions(["1/2", "1/4", "3/4"])
        Fraction(1, 2)
    """
    if not fractions:
        return Fraction(0)
    total = sum_fractions(fractions)
    return total / len(fractions)


def map_fractions(fractions: List[FractionLike], func: Callable[[Fraction], Fraction]) -> List[Fraction]:
    """
    Apply a function to each fraction in a list.
    
    Args:
        fractions: List of fraction-like values
        func: Function to apply to each fraction
    
    Returns:
        List of transformed fractions
    
    Example:
        >>> map_fractions(["1/2", "1/3", "1/4"], reciprocal)
        [Fraction(2, 1), Fraction(3, 1), Fraction(4, 1)]
    """
    return [func(parse_fraction(f)) for f in fractions]


def filter_fractions(fractions: List[FractionLike], 
                     predicate: Callable[[Fraction], bool]) -> List[Fraction]:
    """
    Filter fractions based on a predicate.
    
    Args:
        fractions: List of fraction-like values
        predicate: Function that returns True for fractions to keep
    
    Returns:
        List of fractions that satisfy the predicate
    
    Example:
        >>> filter_fractions(["1/2", "3/4", "5/4", "1/4"], lambda x: x > Fraction(1, 2))
        [Fraction(3, 4), Fraction(5, 4)]
    """
    return [parse_fraction(f) for f in fractions if predicate(parse_fraction(f))]


# ============================================================================
# Sequences and Series
# ============================================================================

def arithmetic_sequence(first: FractionLike, diff: FractionLike, n: int) -> List[Fraction]:
    """
    Generate an arithmetic sequence of fractions.
    
    Args:
        first: The first term
        diff: The common difference
        n: Number of terms to generate
    
    Returns:
        List of fractions in the sequence
    
    Example:
        >>> arithmetic_sequence("1/2", "1/4", 4)
        [Fraction(1, 2), Fraction(3, 4), Fraction(1, 1), Fraction(5, 4)]
    """
    first_frac = parse_fraction(first)
    diff_frac = parse_fraction(diff)
    return [first_frac + i * diff_frac for i in range(n)]


def geometric_sequence(first: FractionLike, ratio: FractionLike, n: int) -> List[Fraction]:
    """
    Generate a geometric sequence of fractions.
    
    Args:
        first: The first term
        ratio: The common ratio
        n: Number of terms to generate
    
    Returns:
        List of fractions in the sequence
    
    Example:
        >>> geometric_sequence("1/2", "1/2", 4)
        [Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)]
    """
    first_frac = parse_fraction(first)
    ratio_frac = parse_fraction(ratio)
    return [first_frac * (ratio_frac ** i) for i in range(n)]


def arithmetic_series_sum(first: FractionLike, diff: FractionLike, n: int) -> Fraction:
    """
    Calculate the sum of an arithmetic series.
    
    Args:
        first: The first term
        diff: The common difference
        n: Number of terms
    
    Returns:
        The sum of the series
    
    Example:
        >>> arithmetic_series_sum(1, 1, 5)  # 1+2+3+4+5
        Fraction(15, 1)
    """
    first_frac = parse_fraction(first)
    diff_frac = parse_fraction(diff)
    # Sum = n/2 * (2*first + (n-1)*diff)
    return Fraction(n, 2) * (2 * first_frac + (n - 1) * diff_frac)


def geometric_series_sum(first: FractionLike, ratio: FractionLike, n: int) -> Fraction:
    """
    Calculate the sum of a finite geometric series.
    
    Args:
        first: The first term
        ratio: The common ratio
        n: Number of terms
    
    Returns:
        The sum of the series
    
    Raises:
        ValueError: If ratio equals 1
    
    Example:
        >>> geometric_series_sum("1/2", "1/2", 4)
        Fraction(15, 16)
    """
    first_frac = parse_fraction(first)
    ratio_frac = parse_fraction(ratio)
    
    if ratio_frac == 1:
        return first_frac * n
    
    # Sum = first * (1 - ratio^n) / (1 - ratio)
    return first_frac * (1 - ratio_frac ** n) / (1 - ratio_frac)


def infinite_geometric_series_sum(first: FractionLike, ratio: FractionLike) -> Optional[Fraction]:
    """
    Calculate the sum of an infinite geometric series.
    
    Args:
        first: The first term
        ratio: The common ratio (must have absolute value < 1)
    
    Returns:
        The sum of the series, or None if it doesn't converge
    
    Example:
        >>> infinite_geometric_series_sum("1/2", "1/2")
        Fraction(1, 1)
    """
    first_frac = parse_fraction(first)
    ratio_frac = parse_fraction(ratio)
    
    if abs(ratio_frac) >= 1:
        return None  # Series doesn't converge
    
    # Sum = first / (1 - ratio)
    return first_frac / (1 - ratio_frac)


# ============================================================================
# Utility Functions
# ============================================================================

def is_proper_fraction(fraction: FractionLike) -> bool:
    """
    Check if a fraction is a proper fraction (|numerator| < denominator).
    
    Args:
        fraction: The input fraction
    
    Returns:
        True if it's a proper fraction
    
    Example:
        >>> is_proper_fraction("3/4")
        True
        >>> is_proper_fraction("5/4")
        False
    """
    frac = parse_fraction(fraction)
    return abs(frac.numerator) < frac.denominator


def is_unit_fraction(fraction: FractionLike) -> bool:
    """
    Check if a fraction is a unit fraction (numerator = 1).
    
    Args:
        fraction: The input fraction
    
    Returns:
        True if it's a unit fraction
    
    Example:
        >>> is_unit_fraction("1/4")
        True
        >>> is_unit_fraction("3/4")
        False
    """
    frac = parse_fraction(fraction)
    return frac.numerator == 1


def is_integer(fraction: FractionLike) -> bool:
    """
    Check if a fraction represents an integer.
    
    Args:
        fraction: The input fraction
    
    Returns:
        True if it's an integer
    
    Example:
        >>> is_integer("4/1")
        True
        >>> is_integer("4/2")
        True
        >>> is_integer("3/4")
        False
    """
    frac = parse_fraction(fraction)
    return frac.denominator == 1


def denominator_count(fraction: FractionLike) -> int:
    """
    Count the number of digits in the denominator.
    
    Args:
        fraction: The input fraction
    
    Returns:
        Number of digits in the denominator
    
    Example:
        >>> denominator_count("1/100")
        3
    """
    frac = parse_fraction(fraction)
    return len(str(frac.denominator))


def approximate(target: FractionLike, max_denominator: int = 100) -> Fraction:
    """
    Find the best rational approximation with limited denominator.
    
    Args:
        target: The target value to approximate
        max_denominator: Maximum allowed denominator
    
    Returns:
        The best approximation as a Fraction
    
    Example:
        >>> approximate(3.14159, max_denominator=100)
        Fraction(311, 99)
        >>> approximate("22/7", max_denominator=10)
        Fraction(22, 7)
    """
    return parse_fraction(target).limit_denominator(max_denominator)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Creation and Parsing
    'create_fraction', 'parse_fraction', 'from_decimal', 'from_percentage',
    
    # Arithmetic Operations
    'add', 'subtract', 'multiply', 'divide', 'power', 'reciprocal', 'negate', 'abs_fraction',
    
    # Comparison Operations
    'compare', 'equals', 'less_than', 'greater_than', 'less_than_or_equal', 
    'greater_than_or_equal', 'min_fraction', 'max_fraction',
    
    # Simplification and Normalization
    'simplify', 'normalize', 'to_mixed_number', 'to_improper_fraction',
    
    # Conversion Functions
    'to_decimal', 'to_percentage', 'to_string',
    
    # GCD/LCM Utilities
    'gcd', 'lcm', 'common_denominator', 'with_common_denominator',
    
    # Batch Operations
    'sum_fractions', 'product_fractions', 'average_fractions', 
    'map_fractions', 'filter_fractions',
    
    # Sequences and Series
    'arithmetic_sequence', 'geometric_sequence', 
    'arithmetic_series_sum', 'geometric_series_sum', 'infinite_geometric_series_sum',
    
    # Utility Functions
    'is_proper_fraction', 'is_unit_fraction', 'is_integer', 
    'denominator_count', 'approximate',
    
    # Type Aliases
    'FractionLike',
]


if __name__ == '__main__':
    # Quick demo
    print("AllToolkit - Fractions Utilities Demo")
    print("=" * 50)
    
    # Parse and display
    f1 = parse_fraction("3/4")
    f2 = parse_fraction("1/2")
    print(f"f1 = {f1}, f2 = {f2}")
    
    # Arithmetic
    print(f"f1 + f2 = {add(f1, f2)}")
    print(f"f1 - f2 = {subtract(f1, f2)}")
    print(f"f1 * f2 = {multiply(f1, f2)}")
    print(f"f1 / f2 = {divide(f1, f2)}")
    
    # Conversion
    print(f"to_decimal(f1) = {to_decimal(f1)}")
    print(f"to_percentage(f1) = {to_percentage(f1)}%")
    print(f"to_string(7/4, 'mixed') = {to_string('7/4', 'mixed')}")
    
    # GCD/LCM
    print(f"gcd(12, 18, 24) = {gcd(12, 18, 24)}")
    print(f"lcm(4, 6, 8) = {lcm(4, 6, 8)}")
    
    # Sequences
    print(f"arithmetic_sequence(1, 1, 5) = {arithmetic_sequence(1, 1, 5)}")
    print(f"geometric_sequence(1, '1/2', 5) = {geometric_sequence(1, '1/2', 5)}")
    
    print("\nRun fractions_utils_test.py for full test suite.")
