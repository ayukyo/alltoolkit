#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Fractions Utilities Test Suite
============================================
Comprehensive test suite for the fractions_utils module.
Covers normal cases, edge cases, and error conditions.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    create_fraction, parse_fraction, from_decimal, from_percentage,
    add, subtract, multiply, divide, power, reciprocal, negate, abs_fraction,
    compare, equals, less_than, greater_than, less_than_or_equal, greater_than_or_equal,
    min_fraction, max_fraction,
    simplify, normalize, to_mixed_number, to_improper_fraction,
    to_decimal, to_percentage, to_string,
    gcd, lcm, common_denominator, with_common_denominator,
    sum_fractions, product_fractions, average_fractions, map_fractions, filter_fractions,
    arithmetic_sequence, geometric_sequence,
    arithmetic_series_sum, geometric_series_sum, infinite_geometric_series_sum,
    is_proper_fraction, is_unit_fraction, is_integer, denominator_count, approximate,
    Fraction
)


class TestRunner:
    """Simple test runner with pass/fail tracking."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, name: str, condition: bool, error_msg: str = ""):
        """Run a single test."""
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            msg = f"  ✗ {name}"
            if error_msg:
                msg += f" - {error_msg}"
            print(msg)
            self.errors.append(name)
    
    def test_exception(self, name: str, func, exception_type, *args, **kwargs):
        """Test that a function raises a specific exception."""
        try:
            func(*args, **kwargs)
            self.failed += 1
            print(f"  ✗ {name} - Expected {exception_type.__name__} but no exception raised")
            self.errors.append(name)
        except exception_type:
            self.passed += 1
            print(f"  ✓ {name}")
        except Exception as e:
            self.failed += 1
            print(f"  ✗ {name} - Expected {exception_type.__name__} but got {type(e).__name__}: {e}")
            self.errors.append(name)
    
    def report(self) -> bool:
        """Print test report and return True if all tests passed."""
        total = self.passed + self.failed
        print(f"\n{'=' * 60}")
        print(f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}")
        if self.failed == 0:
            print("🎉 All tests passed!")
        else:
            print(f"❌ {self.failed} test(s) failed.")
            if self.errors:
                print("\nFailed tests:")
                for err in self.errors:
                    print(f"  - {err}")
        print('=' * 60)
        return self.failed == 0


def run_tests() -> bool:
    """Run all tests."""
    runner = TestRunner()
    
    # ========================================================================
    # Fraction Creation and Parsing Tests
    # ========================================================================
    print("\n📋 Fraction Creation and Parsing Tests")
    print("=" * 60)
    
    # create_fraction
    runner.test("create_fraction(3, 4) creates Fraction(3, 4)", 
                create_fraction(3, 4) == Fraction(3, 4))
    runner.test("create_fraction(6, 8) simplifies to Fraction(3, 4)", 
                create_fraction(6, 8) == Fraction(3, 4))
    runner.test("create_fraction(-3, 4) creates negative fraction", 
                create_fraction(-3, 4) == Fraction(-3, 4))
    runner.test("create_fraction(3, -4) creates negative fraction", 
                create_fraction(3, -4) == Fraction(-3, 4))
    runner.test_exception("create_fraction raises ZeroDivisionError for zero denominator",
                         create_fraction, ZeroDivisionError, 3, 0)
    
    # parse_fraction
    runner.test("parse_fraction('3/4') parses string fraction", 
                parse_fraction("3/4") == Fraction(3, 4))
    runner.test("parse_fraction(3) parses integer", 
                parse_fraction(3) == Fraction(3, 1))
    runner.test("parse_fraction(0.75) parses float", 
                parse_fraction(0.75) == Fraction(3, 4))
    runner.test("parse_fraction((3, 4)) parses tuple", 
                parse_fraction((3, 4)) == Fraction(3, 4))
    runner.test("parse_fraction(Fraction(3, 4)) returns same Fraction", 
                parse_fraction(Fraction(3, 4)) == Fraction(3, 4))
    runner.test("parse_fraction('1 1/2') parses mixed number", 
                parse_fraction("1 1/2") == Fraction(3, 2))
    runner.test("parse_fraction('-1 1/2') parses negative mixed number", 
                parse_fraction("-1 1/2") == Fraction(-3, 2))
    runner.test("parse_fraction('0.25') parses decimal string", 
                parse_fraction("0.25") == Fraction(1, 4))
    runner.test_exception("parse_fraction raises ValueError for invalid string",
                         parse_fraction, ValueError, "invalid")
    runner.test_exception("parse_fraction raises ValueError for wrong tuple size",
                         parse_fraction, ValueError, (1, 2, 3))
    
    # from_decimal
    runner.test("from_decimal(0.5) converts to Fraction(1, 2)", 
                from_decimal(0.5) == Fraction(1, 2))
    runner.test("from_decimal(0.333333) approximates close to Fraction(1, 3)", 
                abs(float(from_decimal(0.333333)) - 1/3) < 0.0001)
    runner.test("from_decimal with max_denominator limits denominator", 
                from_decimal(3.14159, max_denominator=100).denominator <= 100)
    
    # from_percentage
    runner.test("from_percentage(25) converts to Fraction(1, 4)", 
                from_percentage(25) == Fraction(1, 4))
    runner.test("from_percentage(100) converts to Fraction(1, 1)", 
                from_percentage(100) == Fraction(1, 1))
    runner.test("from_percentage('50%') converts string percentage", 
                from_percentage("50%") == Fraction(1, 2))
    runner.test("from_percentage(150) converts to Fraction(3, 2)", 
                from_percentage(150) == Fraction(3, 2))
    
    # ========================================================================
    # Arithmetic Operations Tests
    # ========================================================================
    print("\n📋 Arithmetic Operations Tests")
    print("=" * 60)
    
    # add
    runner.test("add('1/2', '1/3') = 5/6", 
                add("1/2", "1/3") == Fraction(5, 6))
    runner.test("add(1, '1/2', '1/4') = 7/4", 
                add(1, "1/2", "1/4") == Fraction(7, 4))
    runner.test("add() with no args returns 0", 
                add() == Fraction(0))
    runner.test("add('1/4', '1/4', '1/4', '1/4') = 1", 
                add("1/4", "1/4", "1/4", "1/4") == Fraction(1, 1))
    
    # subtract
    runner.test("subtract('3/4', '1/2') = 1/4", 
                subtract("3/4", "1/2") == Fraction(1, 4))
    runner.test("subtract(1, '1/2', '1/4') = 1/4", 
                subtract(1, "1/2", "1/4") == Fraction(1, 4))
    runner.test("subtract('1/2', '3/4') = -1/4", 
                subtract("1/2", "3/4") == Fraction(-1, 4))
    
    # multiply
    runner.test("multiply('1/2', '2/3') = 1/3", 
                multiply("1/2", "2/3") == Fraction(1, 3))
    runner.test("multiply('1/2', '2/3', '3/4') = 1/4", 
                multiply("1/2", "2/3", "3/4") == Fraction(1, 4))
    runner.test("multiply() with no args returns 1", 
                multiply() == Fraction(1))
    runner.test("multiply('1/2', 0) = 0", 
                multiply("1/2", 0) == Fraction(0))
    
    # divide
    runner.test("divide('3/4', '1/2') = 3/2", 
                divide("3/4", "1/2") == Fraction(3, 2))
    runner.test("divide(1, '1/2', '1/4') = 8", 
                divide(1, "1/2", "1/4") == Fraction(8, 1))
    runner.test_exception("divide raises ZeroDivisionError for zero divisor",
                         divide, ZeroDivisionError, "1/2", 0)
    
    # power
    runner.test("power('1/2', 3) = 1/8", 
                power("1/2", 3) == Fraction(1, 8))
    runner.test("power('2/3', 2) = 4/9", 
                power("2/3", 2) == Fraction(4, 9))
    runner.test("power('1/2', 0) = 1", 
                power("1/2", 0) == Fraction(1, 1))
    runner.test("power(2, -3) = 1/8", 
                power(2, -3) == Fraction(1, 8))
    
    # reciprocal
    runner.test("reciprocal('3/4') = 4/3", 
                reciprocal("3/4") == Fraction(4, 3))
    runner.test("reciprocal(5) = 1/5", 
                reciprocal(5) == Fraction(1, 5))
    runner.test("reciprocal('1/2') = 2", 
                reciprocal("1/2") == Fraction(2, 1))
    runner.test_exception("reciprocal raises ZeroDivisionError for zero",
                         reciprocal, ZeroDivisionError, 0)
    
    # negate
    runner.test("negate('3/4') = -3/4", 
                negate("3/4") == Fraction(-3, 4))
    runner.test("negate(-5) = 5", 
                negate(-5) == Fraction(5, 1))
    runner.test("negate(0) = 0", 
                negate(0) == Fraction(0))
    
    # abs_fraction
    runner.test("abs_fraction('-3/4') = 3/4", 
                abs_fraction("-3/4") == Fraction(3, 4))
    runner.test("abs_fraction('3/4') = 3/4", 
                abs_fraction("3/4") == Fraction(3, 4))
    runner.test("abs_fraction(-5) = 5", 
                abs_fraction(-5) == Fraction(5, 1))
    
    # ========================================================================
    # Comparison Operations Tests
    # ========================================================================
    print("\n📋 Comparison Operations Tests")
    print("=" * 60)
    
    # compare
    runner.test("compare('1/2', '2/3') = -1 (less than)", 
                compare("1/2", "2/3") == -1)
    runner.test("compare('2/4', '1/2') = 0 (equal)", 
                compare("2/4", "1/2") == 0)
    runner.test("compare('3/4', '1/2') = 1 (greater than)", 
                compare("3/4", "1/2") == 1)
    
    # equals
    runner.test("equals('1/2', '2/4') = True", 
                equals("1/2", "2/4") == True)
    runner.test("equals('1/2', '1/3') = False", 
                equals("1/2", "1/3") == False)
    
    # less_than
    runner.test("less_than('1/3', '1/2') = True", 
                less_than("1/3", "1/2") == True)
    runner.test("less_than('1/2', '1/3') = False", 
                less_than("1/2", "1/3") == False)
    
    # greater_than
    runner.test("greater_than('3/4', '1/2') = True", 
                greater_than("3/4", "1/2") == True)
    runner.test("greater_than('1/4', '1/2') = False", 
                greater_than("1/4", "1/2") == False)
    
    # less_than_or_equal
    runner.test("less_than_or_equal('1/2', '1/2') = True", 
                less_than_or_equal("1/2", "1/2") == True)
    runner.test("less_than_or_equal('1/3', '1/2') = True", 
                less_than_or_equal("1/3", "1/2") == True)
    
    # greater_than_or_equal
    runner.test("greater_than_or_equal('1/2', '1/2') = True", 
                greater_than_or_equal("1/2", "1/2") == True)
    runner.test("greater_than_or_equal('3/4', '1/2') = True", 
                greater_than_or_equal("3/4", "1/2") == True)
    
    # min_fraction
    runner.test("min_fraction('1/2', '1/3', '1/4') = 1/4", 
                min_fraction("1/2", "1/3", "1/4") == Fraction(1, 4))
    runner.test_exception("min_fraction raises ValueError for empty args",
                         min_fraction, ValueError)
    
    # max_fraction
    runner.test("max_fraction('1/2', '2/3', '3/4') = 3/4", 
                max_fraction("1/2", "2/3", "3/4") == Fraction(3, 4))
    runner.test_exception("max_fraction raises ValueError for empty args",
                         max_fraction, ValueError)
    
    # ========================================================================
    # Simplification and Normalization Tests
    # ========================================================================
    print("\n📋 Simplification and Normalization Tests")
    print("=" * 60)
    
    # simplify
    runner.test("simplify('6/8') = 3/4", 
                simplify("6/8") == Fraction(3, 4))
    runner.test("simplify('100/150') = 2/3", 
                simplify("100/150") == Fraction(2, 3))
    runner.test("simplify('4/2') = 2", 
                simplify("4/2") == Fraction(2, 1))
    
    # normalize
    runner.test("normalize('3/-4') = -3/4", 
                normalize("3/-4") == Fraction(-3, 4))
    runner.test("normalize('-3/4') = -3/4", 
                normalize("-3/4") == Fraction(-3, 4))
    
    # to_mixed_number
    runner.test("to_mixed_number('7/4') = (1, 3/4)", 
                to_mixed_number("7/4") == (1, Fraction(3, 4)))
    runner.test("to_mixed_number('5/2') = (2, 1/2)", 
                to_mixed_number("5/2") == (2, Fraction(1, 2)))
    runner.test("to_mixed_number('3/4') = (0, 3/4)", 
                to_mixed_number("3/4") == (0, Fraction(3, 4)))
    runner.test("to_mixed_number('8/4') = (2, 0)", 
                to_mixed_number("8/4") == (2, Fraction(0, 1)))
    
    # to_improper_fraction
    runner.test("to_improper_fraction(1, 3, 4) = 7/4", 
                to_improper_fraction(1, 3, 4) == Fraction(7, 4))
    runner.test("to_improper_fraction(2, 1, 2) = 5/2", 
                to_improper_fraction(2, 1, 2) == Fraction(5, 2))
    runner.test_exception("to_improper_fraction raises ZeroDivisionError for zero denominator",
                         to_improper_fraction, ZeroDivisionError, 1, 1, 0)
    
    # ========================================================================
    # Conversion Functions Tests
    # ========================================================================
    print("\n📋 Conversion Functions Tests")
    print("=" * 60)
    
    # to_decimal
    runner.test("to_decimal('1/4') = 0.25", 
                to_decimal("1/4") == 0.25)
    runner.test("to_decimal('1/3') approximates 0.333...", 
                abs(to_decimal("1/3") - 0.3333333333) < 0.0001)
    
    # to_percentage
    runner.test("to_percentage('1/4') = 25.0", 
                to_percentage("1/4") == 25.0)
    runner.test("to_percentage('1/2') = 50.0", 
                to_percentage("1/2") == 50.0)
    runner.test("to_percentage('1/3') approximates 33.33", 
                abs(to_percentage("1/3") - 33.33) < 0.01)
    
    # to_string
    runner.test("to_string('3/4', 'fraction') = '3/4'", 
                to_string("3/4", 'fraction') == "3/4")
    runner.test("to_string('4/1', 'fraction') = '4'", 
                to_string("4/1", 'fraction') == "4")
    runner.test("to_string('3/4', 'decimal') = '0.75'", 
                to_string("3/4", 'decimal') == "0.75")
    runner.test("to_string('3/4', 'percentage') = '75.0%'", 
                to_string("3/4", 'percentage') == "75.0%")
    runner.test("to_string('7/4', 'mixed') = '1 3/4'", 
                to_string("7/4", 'mixed') == "1 3/4")
    runner.test_exception("to_string raises ValueError for unknown format",
                         to_string, ValueError, "3/4", "unknown")
    
    # ========================================================================
    # GCD/LCM Utilities Tests
    # ========================================================================
    print("\n📋 GCD/LCM Utilities Tests")
    print("=" * 60)
    
    # gcd
    runner.test("gcd(12, 18) = 6", 
                gcd(12, 18) == 6)
    runner.test("gcd(12, 18, 24) = 6", 
                gcd(12, 18, 24) == 6)
    runner.test("gcd(7, 13) = 1 (coprime)", 
                gcd(7, 13) == 1)
    runner.test("gcd(100, 50) = 50", 
                gcd(100, 50) == 50)
    runner.test("gcd() with no args returns 0", 
                gcd() == 0)
    
    # lcm
    runner.test("lcm(4, 6) = 12", 
                lcm(4, 6) == 12)
    runner.test("lcm(4, 6, 8) = 24", 
                lcm(4, 6, 8) == 24)
    runner.test("lcm(3, 5) = 15 (coprime)", 
                lcm(3, 5) == 15)
    runner.test("lcm() with no args returns 1", 
                lcm() == 1)
    
    # common_denominator
    runner.test("common_denominator('1/4', '1/6', '1/8') = 24", 
                common_denominator("1/4", "1/6", "1/8") == 24)
    runner.test("common_denominator('1/3', '1/5') = 15", 
                common_denominator("1/3", "1/5") == 15)
    
    # with_common_denominator
    result = with_common_denominator("1/4", "1/6")
    # Fraction auto-simplifies, but we verify the values are equivalent
    runner.test("with_common_denominator('1/4', '1/6') values are correct", 
                result[0] == Fraction(3, 12) and result[1] == Fraction(2, 12))
    
    # ========================================================================
    # Batch Operations Tests
    # ========================================================================
    print("\n📋 Batch Operations Tests")
    print("=" * 60)
    
    # sum_fractions
    runner.test("sum_fractions(['1/2', '1/3', '1/6']) = 1", 
                sum_fractions(["1/2", "1/3", "1/6"]) == Fraction(1, 1))
    runner.test("sum_fractions([]) = 0", 
                sum_fractions([]) == Fraction(0))
    
    # product_fractions
    runner.test("product_fractions(['1/2', '2/3', '3/4']) = 1/4", 
                product_fractions(["1/2", "2/3", "3/4"]) == Fraction(1, 4))
    runner.test("product_fractions([]) = 1", 
                product_fractions([]) == Fraction(1))
    
    # average_fractions
    runner.test("average_fractions(['1/2', '1/4', '3/4']) = 1/2", 
                average_fractions(["1/2", "1/4", "3/4"]) == Fraction(1, 2))
    runner.test("average_fractions([]) = 0", 
                average_fractions([]) == Fraction(0))
    
    # map_fractions
    result = map_fractions(["1/2", "1/3", "1/4"], reciprocal)
    runner.test("map_fractions with reciprocal", 
                result == [Fraction(2, 1), Fraction(3, 1), Fraction(4, 1)])
    
    # filter_fractions
    result = filter_fractions(["1/2", "3/4", "5/4", "1/4"], lambda x: x > Fraction(1, 2))
    runner.test("filter_fractions with predicate", 
                result == [Fraction(3, 4), Fraction(5, 4)])
    
    # ========================================================================
    # Sequences and Series Tests
    # ========================================================================
    print("\n📋 Sequences and Series Tests")
    print("=" * 60)
    
    # arithmetic_sequence
    result = arithmetic_sequence("1/2", "1/4", 4)
    runner.test("arithmetic_sequence('1/2', '1/4', 4) correct length", 
                len(result) == 4)
    runner.test("arithmetic_sequence('1/2', '1/4', 4) first term", 
                result[0] == Fraction(1, 2))
    runner.test("arithmetic_sequence('1/2', '1/4', 4) second term", 
                result[1] == Fraction(3, 4))
    
    # geometric_sequence
    result = geometric_sequence("1/2", "1/2", 4)
    runner.test("geometric_sequence('1/2', '1/2', 4) correct length", 
                len(result) == 4)
    runner.test("geometric_sequence('1/2', '1/2', 4) first term", 
                result[0] == Fraction(1, 2))
    runner.test("geometric_sequence('1/2', '1/2', 4) second term", 
                result[1] == Fraction(1, 4))
    
    # arithmetic_series_sum
    runner.test("arithmetic_series_sum(1, 1, 5) = 15 (1+2+3+4+5)", 
                arithmetic_series_sum(1, 1, 5) == Fraction(15, 1))
    runner.test("arithmetic_series_sum(0, 2, 5) = 20 (0+2+4+6+8)", 
                arithmetic_series_sum(0, 2, 5) == Fraction(20, 1))
    
    # geometric_series_sum
    runner.test("geometric_series_sum('1/2', '1/2', 4) = 15/16", 
                geometric_series_sum("1/2", "1/2", 4) == Fraction(15, 16))
    runner.test("geometric_series_sum(1, 2, 4) = 15 (1+2+4+8)", 
                geometric_series_sum(1, 2, 4) == Fraction(15, 1))
    
    # infinite_geometric_series_sum
    runner.test("infinite_geometric_series_sum('1/2', '1/2') = 1", 
                infinite_geometric_series_sum("1/2", "1/2") == Fraction(1, 1))
    runner.test("infinite_geometric_series_sum('1/4', '1/4') = 1/3", 
                infinite_geometric_series_sum("1/4", "1/4") == Fraction(1, 3))
    runner.test("infinite_geometric_series_sum(1, 2) = None (diverges)", 
                infinite_geometric_series_sum(1, 2) is None)
    runner.test("infinite_geometric_series_sum(1, 1) = None (diverges)", 
                infinite_geometric_series_sum(1, 1) is None)
    
    # ========================================================================
    # Utility Functions Tests
    # ========================================================================
    print("\n📋 Utility Functions Tests")
    print("=" * 60)
    
    # is_proper_fraction
    runner.test("is_proper_fraction('3/4') = True", 
                is_proper_fraction("3/4") == True)
    runner.test("is_proper_fraction('5/4') = False", 
                is_proper_fraction("5/4") == False)
    runner.test("is_proper_fraction('1/1') = False", 
                is_proper_fraction("1/1") == False)
    
    # is_unit_fraction
    runner.test("is_unit_fraction('1/4') = True", 
                is_unit_fraction("1/4") == True)
    runner.test("is_unit_fraction('3/4') = False", 
                is_unit_fraction("3/4") == False)
    runner.test("is_unit_fraction('1/1') = True", 
                is_unit_fraction("1/1") == True)
    
    # is_integer
    runner.test("is_integer('4/1') = True", 
                is_integer("4/1") == True)
    runner.test("is_integer('4/2') = True", 
                is_integer("4/2") == True)
    runner.test("is_integer('3/4') = False", 
                is_integer("3/4") == False)
    
    # denominator_count
    runner.test("denominator_count('1/100') = 3", 
                denominator_count("1/100") == 3)
    runner.test("denominator_count('1/2') = 1", 
                denominator_count("1/2") == 1)
    runner.test("denominator_count('1/10000') = 5", 
                denominator_count("1/10000") == 5)
    
    # approximate
    runner.test("approximate(3.14159, 100) has denominator <= 100", 
                approximate(3.14159, 100).denominator <= 100)
    runner.test("approximate('22/7', 10) = 22/7", 
                approximate("22/7", 10) == Fraction(22, 7))
    
    # ========================================================================
    # Edge Cases and Error Handling
    # ========================================================================
    print("\n📋 Edge Cases and Error Handling Tests")
    print("=" * 60)
    
    # Negative fractions
    runner.test("add('-1/2', '-1/2') = -1", 
                add("-1/2", "-1/2") == Fraction(-1, 1))
    runner.test("multiply('-1/2', '-1/2') = 1/4", 
                multiply("-1/2", "-1/2") == Fraction(1, 4))
    
    # Zero handling
    runner.test("add(0, 0) = 0", 
                add(0, 0) == Fraction(0))
    runner.test("multiply(0, '1/2') = 0", 
                multiply(0, "1/2") == Fraction(0))
    
    # Large numbers
    runner.test("create_fraction(10**10, 10**10 + 1) works", 
                create_fraction(10**10, 10**10 + 1).denominator == 10**10 + 1)
    
    # ========================================================================
    # Print Report
    # ========================================================================
    return runner.report()


if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Fractions Utilities Test Suite")
    print("=" * 60)
    
    success = run_tests()
    sys.exit(0 if success else 1)
