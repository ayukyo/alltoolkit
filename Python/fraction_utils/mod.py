#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Fraction Utilities Module
=======================================
A comprehensive fraction and rational number utility module with zero external dependencies.

Features:
    - Fraction arithmetic (add, subtract, multiply, divide)
    - Fraction comparison and ordering
    - Fraction simplification/reduction
    - Mixed number conversion
    - Decimal conversion
    - Continued fraction support
    - Fraction approximation from floats
    - Fraction formatting and display

Author: AllToolkit Contributors
License: MIT
"""

from typing import Union, Optional, Tuple, List
import math
import re


# =============================================================================
# Helper Functions
# =============================================================================

def _gcd(a: int, b: int) -> int:
    """Compute the greatest common divisor using Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return abs(a)


def _lcm(a: int, b: int) -> int:
    """Compute the least common multiple."""
    return abs(a * b) // _gcd(a, b)


def _continued_fraction(value: float, tolerance: float) -> List[int]:
    """Compute the continued fraction representation of a float."""
    result = []
    int_part = int(value)
    frac_part = value - int_part
    result.append(int_part)
    
    a, b = 1, 0
    current = frac_part
    
    while b <= 1e15:
        if current < tolerance:
            break
        reciprocal = 1.0 / current
        a, b = b, a
        digit = int(reciprocal)
        a = a * digit + b
        current = reciprocal - digit
        
        if digit > 1e15:
            break
        result.append(digit)
    
    return result


# =============================================================================
# Fraction Class
# =============================================================================

class Fraction:
    """
    A rational number represented as numerator/denominator.
    
    Attributes:
        numerator: The numerator (top number)
        denominator: The denominator (bottom number, always positive)
    
    The fraction is always kept in reduced form after construction.
    Zero is represented as 0/1.
    """
    
    __slots__ = ('numerator', 'denominator')
    
    def __init__(self, numerator: int = 0, denominator: int = 1):
        """Construct a Fraction from numerator and denominator."""
        if denominator == 0:
            raise ZeroDivisionError("denominator cannot be zero")
        
        # Normalize sign: denominator is always positive
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        
        # Handle zero numerator
        if numerator == 0:
            self.numerator = 0
            self.denominator = 1
            return
        
        # Reduce to lowest terms using GCD
        g = _gcd(abs(numerator), denominator)
        self.numerator = numerator // g
        self.denominator = denominator // g
    
    def __repr__(self) -> str:
        if self.denominator == 1:
            return f"Fraction({self.numerator})"
        return f"Fraction({self.numerator}, {self.denominator})"
    
    def __str__(self) -> str:
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"
    
    def __hash__(self) -> int:
        return hash((self.numerator, self.denominator))
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Fraction):
            return self.numerator == other.numerator and self.denominator == other.denominator
        if isinstance(other, int):
            return self.denominator == 1 and self.numerator == other
        if isinstance(other, float):
            return float(self) == other
        return NotImplemented
    
    def __lt__(self, other) -> bool:
        if isinstance(other, Fraction):
            return self.numerator * other.denominator < other.numerator * self.denominator
        if isinstance(other, int):
            return self.numerator < other * self.denominator
        if isinstance(other, float):
            return float(self) < other
        return NotImplemented
    
    def __le__(self, other) -> bool:
        return self == other or self < other
    
    def __gt__(self, other) -> bool:
        if isinstance(other, Fraction):
            return self.numerator * other.denominator > other.numerator * self.denominator
        if isinstance(other, int):
            return self.numerator > other * self.denominator
        if isinstance(other, float):
            return float(self) > other
        return NotImplemented
    
    def __ge__(self, other) -> bool:
        return self == other or self > other
    
    def __neg__(self) -> 'Fraction':
        return Fraction(-self.numerator, self.denominator)
    
    def __pos__(self) -> 'Fraction':
        return Fraction(self.numerator, self.denominator)
    
    def __abs__(self) -> 'Fraction':
        return Fraction(abs(self.numerator), self.denominator)
    
    def __int__(self) -> int:
        return self.numerator // self.denominator
    
    def __float__(self) -> float:
        return self.numerator / self.denominator
    
    def __round__(self, ndigits: Optional[int] = None) -> Union[int, float]:
        val = self.numerator / self.denominator
        return round(val, ndigits)
    
    def __add__(self, other) -> 'Fraction':
        if isinstance(other, Fraction):
            num = self.numerator * other.denominator + other.numerator * self.denominator
            den = self.denominator * other.denominator
            return Fraction(num, den)
        if isinstance(other, int):
            return Fraction(self.numerator + other * self.denominator, self.denominator)
        if isinstance(other, float):
            return Fraction.from_float(other) + self
        return NotImplemented
    
    def __radd__(self, other) -> 'Fraction':
        return self.__add__(other)
    
    def __sub__(self, other) -> 'Fraction':
        if isinstance(other, Fraction):
            num = self.numerator * other.denominator - other.numerator * self.denominator
            den = self.denominator * other.denominator
            return Fraction(num, den)
        if isinstance(other, int):
            return Fraction(self.numerator - other * self.denominator, self.denominator)
        if isinstance(other, float):
            return self - Fraction.from_float(other)
        return NotImplemented
    
    def __rsub__(self, other) -> 'Fraction':
        if isinstance(other, int):
            return Fraction(other * self.denominator - self.numerator, self.denominator)
        if isinstance(other, float):
            return Fraction.from_float(other) - self
        return NotImplemented
    
    def __mul__(self, other) -> 'Fraction':
        if isinstance(other, Fraction):
            num = self.numerator * other.numerator
            den = self.denominator * other.denominator
            return Fraction(num, den)
        if isinstance(other, int):
            return Fraction(self.numerator * other, self.denominator)
        if isinstance(other, float):
            return self * Fraction.from_float(other)
        return NotImplemented
    
    def __rmul__(self, other) -> 'Fraction':
        return self.__mul__(other)
    
    def __truediv__(self, other) -> 'Fraction':
        if isinstance(other, Fraction):
            if other.numerator == 0:
                raise ZeroDivisionError("division by zero")
            num = self.numerator * other.denominator
            den = self.denominator * other.numerator
            return Fraction(num, den)
        if isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError("division by zero")
            return Fraction(self.numerator, self.denominator * other)
        if isinstance(other, float):
            return self / Fraction.from_float(other)
        return NotImplemented
    
    def __rtruediv__(self, other) -> 'Fraction':
        if isinstance(other, int):
            if self.numerator == 0:
                raise ZeroDivisionError("division by zero")
            return Fraction(other * self.denominator, self.numerator)
        if isinstance(other, float):
            return Fraction.from_float(other) / self
        return NotImplemented
    
    def __pow__(self, other: int) -> 'Fraction':
        if other == 0:
            return Fraction(1)
        if other > 0:
            return Fraction(self.numerator ** other, self.denominator ** other)
        if other < 0:
            if self.numerator == 0:
                raise ZeroDivisionError("zero cannot be raised to negative power")
            return Fraction(self.denominator ** abs(other), self.numerator ** abs(other))
        return NotImplemented
    
    def __floor__(self) -> int:
        return math.floor(self.numerator / self.denominator)
    
    def __ceil__(self) -> int:
        return math.ceil(self.numerator / self.denominator)
    
    @property
    def is_zero(self) -> bool:
        """Check if the fraction equals zero."""
        return self.numerator == 0
    
    @property
    def is_integer(self) -> bool:
        """Check if the fraction equals an integer."""
        return self.denominator == 1
    
    @property
    def is_positive(self) -> bool:
        """Check if the fraction is positive."""
        return self.numerator > 0
    
    @property
    def is_negative(self) -> bool:
        """Check if the fraction is negative."""
        return self.numerator < 0
    
    @property
    def is_proper(self) -> bool:
        """Check if the fraction is proper (|numerator| < denominator)."""
        return abs(self.numerator) < self.denominator
    
    @property
    def is_unit(self) -> bool:
        """Check if the fraction is a unit fraction (numerator = 1)."""
        return self.numerator == 1 and self.denominator > 1
    
    @property
    def mixed_number(self) -> Tuple[int, 'Fraction']:
        """Convert to mixed number as (whole, fraction).
        
        Returns (whole, fraction) such that original = whole + frac.
        For negative fractions, if frac is negative: whole + frac = original.
        E.g., -7/4 -> whole=-1, frac=-3/4, since -1 + (-3/4) = -7/4.
        """
        if self.numerator == 0:
            return (0, Fraction(0))
        
        if self.denominator == 1:
            return (self.numerator, Fraction(0))
        
        # Use floor division which in Python gives the "correct" whole part
        # For negative values: -7 // 4 = -2, -7 % 4 = 1
        # So -7/4 = -2 + 1/4
        whole = self.numerator // self.denominator
        remainder = self.numerator % self.denominator
        
        if remainder == 0:
            return (whole, Fraction(0))
        
        # For negative fractions with non-zero remainder, remainder is positive
        # but we want: original = whole + frac where frac has the same sign as original
        # With floor div: -7/4 = -2 + 1/4, but we want -1 + (-3/4) = -7/4
        # So we adjust: if whole < 0 and remainder > 0, use (whole+1, -1 + remainder/denom)
        if whole < 0 and remainder > 0:
            # remainder/denom gives positive fraction, so negate it
            return (whole + 1, Fraction(remainder - self.denominator, self.denominator))
        
        return (whole, Fraction(remainder, self.denominator))
    
    @property
    def continued_fraction(self) -> List[int]:
        """Return the continued fraction representation."""
        if self.numerator == 0:
            return [0]
        
        result = []
        a, b = abs(self.numerator), self.denominator
        
        while b != 0:
            result.append(a // b)
            a, b = b, a % b
        
        return result
    
    @property
    def simplified(self) -> 'Fraction':
        """Return the fraction in simplest form (already reduced, this is a no-op)."""
        return Fraction(self.numerator, self.denominator)
    
    def reciprocal(self) -> 'Fraction':
        """Return the reciprocal (swap numerator and denominator)."""
        if self.numerator == 0:
            raise ZeroDivisionError("zero has no reciprocal")
        return Fraction(self.denominator, self.numerator)
    
    def abs(self) -> 'Fraction':
        """Return the absolute value of the fraction."""
        return Fraction(abs(self.numerator), self.denominator)
    
    def floor(self) -> int:
        """Return the floor of the fraction as an integer."""
        return self.__floor__()
    
    def ceil(self) -> int:
        """Return the ceiling of the fraction as an integer."""
        return self.__ceil__()
    
    def round(self, ndigits: Optional[int] = None) -> Union[int, float]:
        """Return the fraction rounded to ndigits decimal places."""
        return self.__round__(ndigits)
    
    # =========================================================================
    # Class Methods
    # =========================================================================
    
    @classmethod
    def from_float(cls, value: float, tolerance: float = 1e-12) -> 'Fraction':
        """
        Convert a float to a fraction using continued fraction approximation.
        
        Args:
            value: The float to convert
            tolerance: Maximum allowed error (default 1e-12)
        
        Returns:
            Approximate Fraction representation
        
        Raises:
            ValueError: If value is NaN or infinity
        """
        if math.isnan(value):
            raise ValueError("cannot convert NaN to Fraction")
        if math.isinf(value):
            raise ValueError("cannot convert infinity to Fraction")
        if value == 0:
            return cls(0)
        
        # Handle negative values
        sign = -1 if value < 0 else 1
        value = abs(value)
        
        # Separate integer and fractional parts
        int_part = int(value)
        frac_part = value - int_part
        
        # Use continued fraction to find best approximation of the fractional part
        cf = _continued_fraction(frac_part, tolerance)
        
        # Build fraction from continued fraction of fractional part only
        num, den = 1, 0
        for i in reversed(cf):
            num, den = den + num * i, num
        
        # Total = int_part + num/den = (int_part * den + num) / den
        result = cls(sign * (int_part * den + num), den)
        return result
    
    @classmethod
    def from_string(cls, value: str) -> 'Fraction':
        """
        Parse a fraction from a string.
        
        Accepts formats: "3/4", "1 1/2" (mixed), "-5/6", "7"
        
        Args:
            value: String representation of the fraction
        
        Returns:
            Parsed Fraction
        
        Raises:
            ValueError: If the string cannot be parsed
        """
        value = value.strip()
        
        # Try simple fraction: "3/4"
        simple = re.match(r'^(-?\d+)/(\d+)$', value)
        if simple:
            return cls(int(simple.group(1)), int(simple.group(2)))
        
        # Try mixed number: "1 1/2" or "-1 1/2"
        mixed = re.match(r'^(-?\d+)\s+(\d+)/(\d+)$', value)
        if mixed:
            whole = int(mixed.group(1))
            num = int(mixed.group(2))
            den = int(mixed.group(3))
            total_num = whole * den + num
            if whole < 0:
                total_num = -abs(total_num) if num != 0 else whole * den
            if whole < 0 and num > 0:
                total_num = whole * den - num
            return cls(total_num, den)
        
        # Try integer: "42"
        integer = re.match(r'^-?\d+$', value)
        if integer:
            return cls(int(value))
        
        raise ValueError(f"cannot parse '{value}' as Fraction")
    
    @classmethod
    def from_continued_fraction(cls, cf: List[int]) -> 'Fraction':
        """
        Create a fraction from a continued fraction representation.
        
        Args:
            cf: List of continued fraction terms
        
        Returns:
            The corresponding Fraction
        
        Raises:
            ValueError: If cf is empty
        """
        if not cf:
            raise ValueError("continued fraction cannot be empty")
        
        num, den = 1, 0
        for i in reversed(cf):
            num, den = den + num * i, num
        
        return cls(num, den)
    
    @classmethod
    def from_decimal(cls, decimal_str: str) -> 'Fraction':
        """
        Convert a decimal string to a fraction.
        
        Args:
            decimal_str: String like "0.75", "3.14159"
        
        Returns:
            Reduced Fraction
        """
        decimal_str = decimal_str.strip()
        
        # Handle negative
        sign = -1 if decimal_str.startswith('-') else 1
        if decimal_str.startswith('-'):
            decimal_str = decimal_str[1:]
        
        # Split integer and fractional parts
        if '.' in decimal_str:
            int_part, frac_part = decimal_str.split('.')
            if int_part == '':
                int_part = '0'
        else:
            int_part = decimal_str
            frac_part = ''
        
        # Convert to fraction: int_part + frac_part / (10^len)
        if frac_part:
            denominator = 10 ** len(frac_part)
            numerator = int(int_part) * denominator + int(frac_part)
        else:
            denominator = 1
            numerator = int(int_part)
        
        return cls(sign * numerator, denominator)
    
    def mediant(self, other: 'Fraction') -> 'Fraction':
        """
        Return the mediant (farey sum) of two fractions: (a+c)/(b+d).
        """
        num = self.numerator + other.numerator
        den = self.denominator + other.denominator
        return Fraction(num, den)
    
    @classmethod
    def farey_sequence(cls, n: int) -> List['Fraction']:
        """
        Generate the Farey sequence of order n.
        
        Args:
            n: The maximum denominator
        
        Returns:
            List of Fractions in order from 0 to 1
        """
        if n < 1:
            raise ValueError("n must be at least 1")
        
        if n == 1:
            return [cls(0, 1), cls(1, 1)]
        
        sequence = [cls(0, 1), cls(1, n)]
        a, b = 0, 1
        c, d = 1, n
        
        while c < n:
            k = (n + b) // d
            a, b, c, d = c, d, k * c - a, k * d - b
            if c <= n:
                sequence.append(cls(c, d))
        
        return sequence
    
    @classmethod
    def best_approximation(cls, value: float, max_denominator: int = 1000) -> 'Fraction':
        """
        Find the best rational approximation with bounded denominator.
        
        Args:
            value: The float to approximate
            max_denominator: Maximum denominator allowed
        
        Returns:
            Best Fraction approximation
        """
        if max_denominator < 1:
            raise ValueError("max_denominator must be at least 1")
        
        if math.isnan(value) or math.isinf(value):
            raise ValueError("value must be finite")
        
        sign = -1 if value < 0 else 1
        value = abs(value)
        
        int_part = int(value)
        frac_part = value - int_part
        
        # Use continued fraction with denominator limit
        cf = _continued_fraction(value, 1.0 / (max_denominator * max_denominator))
        
        num, den = 1, 0
        for i in reversed(cf):
            num, den = den + num * i, num
            if den > max_denominator:
                break
        
        # If we overshot, find best approximation with limit
        if den > max_denominator:
            num, den = 1, 0
            for i in reversed(cf):
                num, den = den + num * i, num
                if den > max_denominator:
                    num = num * max_denominator // den
                    den = max_denominator
                    break
        
        return cls(sign * (int_part * den + num), den)


class FractionStats:
    """Statistics for a collection of fractions."""
    
    def __init__(
        self,
        count: int = 0,
        sum: Optional[Fraction] = None,
        mean: Optional[Fraction] = None,
        min: Optional[Fraction] = None,
        max: Optional[Fraction] = None,
        median: Optional[Fraction] = None
    ):
        self.count = count
        self.sum = sum
        self.mean = mean
        self.min = min
        self.max = max
        self.median = median
    
    def to_dict(self) -> dict:
        return {
            'count': self.count,
            'sum': str(self.sum) if self.sum else None,
            'mean': str(self.mean) if self.mean else None,
            'min': str(self.min) if self.min else None,
            'max': str(self.max) if self.max else None,
            'median': str(self.median) if self.median else None,
        }


# =============================================================================
# Utility Functions
# =============================================================================

def fraction_sum(fractions: List[Fraction]) -> Fraction:
    """
    Sum a list of fractions efficiently using pairwise reduction.
    """
    if not fractions:
        return Fraction(0)
    
    result = fractions[0]
    for f in fractions[1:]:
        result = result + f
    return result


def fraction_product(fractions: List[Fraction]) -> Fraction:
    """
    Multiply a list of fractions.
    """
    if not fractions:
        return Fraction(1)
    
    result = fractions[0]
    for f in fractions[1:]:
        result = result * f
    return result


def fraction_stats(fractions: List[Fraction]) -> FractionStats:
    """
    Calculate statistics for a collection of fractions.
    """
    if not fractions:
        return FractionStats()
    
    sorted_fracs = sorted(fractions)
    n = len(sorted_fracs)
    
    total = fraction_sum(fractions)
    mean = total / n
    
    mid = n // 2
    if n % 2 == 0:
        median = (sorted_fracs[mid - 1] + sorted_fracs[mid]) / 2
    else:
        median = sorted_fracs[mid]
    
    return FractionStats(
        count=n,
        sum=total,
        mean=mean,
        min=sorted_fracs[0],
        max=sorted_fracs[-1],
        median=median,
    )


def diophantine_solution(a: int, b: int, c: int) -> Optional[Tuple[int, int]]:
    """
    Solve the Diophantine equation ax + by = c.
    
    Uses the extended Euclidean algorithm.
    """
    g = _gcd(a, b)
    if c % g != 0:
        return None
    
    a //= g
    b //= g
    c //= g
    
    # Extended Euclidean algorithm
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    
    x = c * old_s
    y = c * old_t
    
    return (x, y)


def egyptian_fraction(f: Fraction) -> List[Fraction]:
    """
    Decompose a fraction into an Egyptian fraction (sum of unit fractions).
    
    Uses the greedy algorithm (Fibonacci's algorithm).
    """
    if f.numerator == 0:
        return []
    
    if f.is_integer:
        return [f]
    
    result = []
    remaining = Fraction(f.numerator, f.denominator)
    
    while remaining.numerator > 1:
        unit_denom = (remaining.denominator + remaining.numerator - 1) // remaining.numerator
        unit = Fraction(1, unit_denom)
        result.append(unit)
        remaining = remaining - unit
    
    if remaining.numerator > 0:
        result.append(remaining)
    
    return result


def fraction_to_latex(f: Fraction) -> str:
    """Convert a fraction to LaTeX format."""
    if f.denominator == 1:
        return str(f.numerator)
    return f"\\frac{{{f.numerator}}}{{{f.denominator}}}"


def fraction_to_unicode(f: Fraction) -> str:
    """Convert a fraction to Unicode character if available."""
    unicode_map = {
        (1, 2): '½', (1, 3): '⅓', (2, 3): '⅔',
        (1, 4): '¼', (3, 4): '¾', (1, 5): '⅕',
        (2, 5): '⅖', (3, 5): '⅗', (4, 5): '⅘',
        (1, 6): '⅙', (5, 6): '⅚', (1, 7): '⅐',
        (1, 8): '⅛', (3, 8): '⅜', (5, 8): '⅝', (7, 8): '⅞',
        (1, 9): '⅑', (1, 10): '⅒',
    }
    
    key = (abs(f.numerator), f.denominator)
    if key in unicode_map:
        sign = '-' if f.numerator < 0 else ''
        return sign + unicode_map[key]
    
    return str(f)


def format_fraction(f: Fraction, style: str = 'normal') -> str:
    """
    Format a fraction in various styles.
    
    Args:
        f: The Fraction
        style: One of 'normal', 'mixed', 'latex', 'unicode'
    """
    if style == 'normal':
        return str(f)
    elif style == 'mixed':
        whole, frac = f.mixed_number
        if frac.is_zero:
            return str(whole)
        if whole == 0:
            return str(frac)
        return f"{whole} {frac}"
    elif style == 'latex':
        return fraction_to_latex(f)
    elif style == 'unicode':
        return fraction_to_unicode(f)
    else:
        raise ValueError(f"unknown style '{style}'")