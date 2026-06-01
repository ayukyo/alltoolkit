#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Fraction Utilities Module
"""

import unittest
import math
from fraction_utils.mod import (
    Fraction, fraction_sum, fraction_product, fraction_stats,
    egyptian_fraction, diophantine_solution, format_fraction,
    fraction_to_latex, fraction_to_unicode, _gcd, _lcm
)


class TestFractionBasic(unittest.TestCase):
    """Test basic Fraction construction and properties."""
    
    def test_create_fraction(self):
        f = Fraction(3, 4)
        self.assertEqual(f.numerator, 3)
        self.assertEqual(f.denominator, 4)
    
    def test_reduce(self):
        f = Fraction(6, 8)
        self.assertEqual(f.numerator, 3)
        self.assertEqual(f.denominator, 4)
    
    def test_negative_denominator(self):
        f = Fraction(3, -4)
        self.assertEqual(f.numerator, -3)
        self.assertEqual(f.denominator, 4)
    
    def test_zero(self):
        f = Fraction(0, 5)
        self.assertEqual(f.numerator, 0)
        self.assertEqual(f.denominator, 1)
    
    def test_integer_fraction(self):
        f = Fraction(7)
        self.assertEqual(f.numerator, 7)
        self.assertEqual(f.denominator, 1)
    
    def test_zero_division_error(self):
        with self.assertRaises(ZeroDivisionError):
            Fraction(1, 0)


class TestFractionArithmetic(unittest.TestCase):
    """Test arithmetic operations."""
    
    def test_addition(self):
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        result = f1 + f2
        self.assertEqual(result, Fraction(5, 6))
    
    def test_addition_with_int(self):
        f = Fraction(1, 2)
        result = f + 1
        self.assertEqual(result, Fraction(3, 2))
    
    def test_subtraction(self):
        f1 = Fraction(3, 4)
        f2 = Fraction(1, 4)
        result = f1 - f2
        self.assertEqual(result, Fraction(1, 2))
    
    def test_multiplication(self):
        f1 = Fraction(2, 3)
        f2 = Fraction(3, 4)
        result = f1 * f2
        self.assertEqual(result, Fraction(1, 2))
    
    def test_division(self):
        f1 = Fraction(1, 2)
        f2 = Fraction(3, 4)
        result = f1 / f2
        self.assertEqual(result, Fraction(2, 3))
    
    def test_division_by_zero(self):
        f = Fraction(1, 2)
        with self.assertRaises(ZeroDivisionError):
            f / Fraction(0)
    
    def test_power(self):
        f = Fraction(2, 3)
        result = f ** 2
        self.assertEqual(result, Fraction(4, 9))
    
    def test_negative_power(self):
        f = Fraction(2, 3)
        result = f ** (-1)
        self.assertEqual(result, Fraction(3, 2))


class TestFractionComparison(unittest.TestCase):
    """Test comparison operations."""
    
    def test_equality(self):
        self.assertEqual(Fraction(1, 2), Fraction(2, 4))
        self.assertEqual(Fraction(3), Fraction(3, 1))
    
    def test_less_than(self):
        self.assertTrue(Fraction(1, 3) < Fraction(1, 2))
        self.assertTrue(Fraction(-1, 2) < Fraction(1, 2))
    
    def test_greater_than(self):
        self.assertTrue(Fraction(3, 4) > Fraction(1, 2))
    
    def test_compare_with_int(self):
        self.assertTrue(Fraction(5) > 4)


class TestFractionProperties(unittest.TestCase):
    """Test Fraction properties."""
    
    def test_is_zero(self):
        self.assertTrue(Fraction(0).is_zero)
        self.assertFalse(Fraction(1, 2).is_zero)
    
    def test_is_integer(self):
        self.assertTrue(Fraction(5).is_integer)
        self.assertFalse(Fraction(3, 2).is_integer)
    
    def test_is_positive(self):
        self.assertTrue(Fraction(1, 2).is_positive)
        self.assertFalse(Fraction(-1, 2).is_positive)
    
    def test_is_proper(self):
        self.assertTrue(Fraction(1, 2).is_proper)
        self.assertFalse(Fraction(3, 2).is_proper)
    
    def test_is_unit(self):
        self.assertTrue(Fraction(1, 3).is_unit)
        self.assertFalse(Fraction(2, 3).is_unit)


class TestMixedNumber(unittest.TestCase):
    """Test mixed number conversion."""
    
    def test_positive_mixed(self):
        f = Fraction(7, 4)
        whole, frac = f.mixed_number
        self.assertEqual(whole, 1)
        self.assertEqual(frac, Fraction(3, 4))
    
    def test_negative_mixed(self):
        f = Fraction(-7, 4)
        whole, frac = f.mixed_number
        self.assertEqual(whole, -1)
        self.assertEqual(frac, Fraction(-3, 4))
    
    def test_integer_mixed(self):
        f = Fraction(5)
        whole, frac = f.mixed_number
        self.assertEqual(whole, 5)
        self.assertTrue(frac.is_zero)


class TestContinuedFraction(unittest.TestCase):
    """Test continued fraction functionality."""
    
    def test_continued_fraction(self):
        f = Fraction(22, 7)
        cf = f.continued_fraction
        self.assertEqual(cf, [3, 7])
    
    def test_from_continued_fraction(self):
        cf = [3, 7]
        f = Fraction.from_continued_fraction(cf)
        self.assertEqual(f, Fraction(22, 7))
    
    def test_roundtrip(self):
        original = Fraction(22, 7)
        cf = original.continued_fraction
        reconstructed = Fraction.from_continued_fraction(cf)
        self.assertEqual(original, reconstructed)


class TestFromFloat(unittest.TestCase):
    """Test float conversion."""
    
    def test_simple_float(self):
        f = Fraction.from_float(0.5)
        self.assertEqual(f, Fraction(1, 2))
    
    def test_repeating_float(self):
        f = Fraction.from_float(0.333, tolerance=1e-3)
        self.assertTrue(abs(float(f) - 0.333) < 1e-3)
    
    def test_pi_approximation(self):
        f = Fraction.from_float(math.pi, tolerance=1e-6)
        self.assertTrue(abs(float(f) - math.pi) < 1e-5)
    
    def test_nan_error(self):
        with self.assertRaises(ValueError):
            Fraction.from_float(float('nan'))
    
    def test_inf_error(self):
        with self.assertRaises(ValueError):
            Fraction.from_float(float('inf'))


class TestFromString(unittest.TestCase):
    """Test string parsing."""
    
    def test_simple_fraction(self):
        f = Fraction.from_string("3/4")
        self.assertEqual(f, Fraction(3, 4))
    
    def test_negative_fraction(self):
        f = Fraction.from_string("-5/6")
        self.assertEqual(f, Fraction(-5, 6))
    
    def test_mixed_number(self):
        f = Fraction.from_string("1 1/2")
        self.assertEqual(f, Fraction(3, 2))
    
    def test_integer_string(self):
        f = Fraction.from_string("42")
        self.assertEqual(f, Fraction(42))
    
    def test_invalid_string(self):
        with self.assertRaises(ValueError):
            Fraction.from_string("invalid")


class TestEgyptianFraction(unittest.TestCase):
    """Test Egyptian fraction decomposition."""
    
    def test_two_thirds(self):
        f = Fraction(2, 3)
        result = egyptian_fraction(f)
        total = fraction_sum(result)
        self.assertEqual(total, f)
        for unit in result:
            self.assertTrue(unit.is_unit)
    
    def test_three_quarters(self):
        f = Fraction(3, 4)
        result = egyptian_fraction(f)
        self.assertEqual(len(result), 2)  # 1/2 + 1/4


class TestDiophantine(unittest.TestCase):
    """Test Diophantine equation solver."""
    
    def test_simple_solution(self):
        result = diophantine_solution(2, 3, 11)
        self.assertIsNotNone(result)
        x, y = result
        self.assertEqual(2 * x + 3 * y, 11)
    
    def test_no_solution(self):
        result = diophantine_solution(2, 4, 7)
        self.assertIsNone(result)


class TestFractionStats(unittest.TestCase):
    """Test fraction statistics."""
    
    def test_stats(self):
        fracs = [Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)]
        stats = fraction_stats(fracs)
        self.assertEqual(stats.count, 3)
        self.assertEqual(stats.min, Fraction(1, 4))
        self.assertEqual(stats.max, Fraction(3, 4))


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_gcd(self):
        self.assertEqual(_gcd(48, 18), 6)
        self.assertEqual(_gcd(7, 13), 1)
    
    def test_lcm(self):
        self.assertEqual(_lcm(4, 6), 12)
    
    def test_format_fraction(self):
        f = Fraction(1, 2)
        self.assertEqual(format_fraction(f, 'normal'), '1/2')
        self.assertEqual(format_fraction(f, 'mixed'), '1/2')
        self.assertEqual(format_fraction(f, 'latex'), r'\frac{1}{2}')
    
    def test_fraction_to_unicode(self):
        self.assertEqual(fraction_to_unicode(Fraction(1, 2)), '½')


class TestFareySequence(unittest.TestCase):
    """Test Farey sequence generation."""
    
    def test_farey_sequence(self):
        seq = Fraction.farey_sequence(4)
        self.assertEqual(seq[0], Fraction(0))
        self.assertEqual(seq[-1], Fraction(1))
        # Check order - consecutive Farey fractions satisfy b*c - a*d = 1
        for i in range(len(seq) - 1):
            a, b = seq[i].numerator, seq[i].denominator
            c, d = seq[i+1].numerator, seq[i+1].denominator
            self.assertTrue(b * c - a * d == 1)


class TestMediant(unittest.TestCase):
    """Test mediant (farey sum)."""
    
    def test_mediant(self):
        f1 = Fraction(1, 3)
        f2 = Fraction(2, 3)
        result = f1.mediant(f2)
        self.assertEqual(result, Fraction(3, 6))
        self.assertEqual(result, Fraction(1, 2))


if __name__ == '__main__':
    unittest.main()