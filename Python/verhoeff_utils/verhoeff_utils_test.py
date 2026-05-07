#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Verhoeff Utilities Test Suite

Comprehensive tests for the Verhoeff check digit algorithm implementation.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from verhoeff_utils.mod import (
    compute_check_digit,
    compute_check_digit_int,
    validate,
    validate_int,
    append_check_digit,
    append_check_digit_int,
    get_check_digit_position,
    extract_data_digits,
    extract_data_digits_int,
    detect_single_error,
    detect_transposition_error,
    analyze_error,
    compare_with_luhn,
    validate_batch,
    generate_with_check_digits,
    explain_algorithm,
    show_computation_steps,
    D5_MULTIPLICATION,
    PERMUTATION,
    INVERSE,
)


class TestBasicOperations(unittest.TestCase):
    """Test basic Verhoeff operations."""
    
    def test_compute_check_digit_simple(self):
        """Test check digit computation for simple numbers."""
        self.assertEqual(compute_check_digit("12345"), 1)
        self.assertEqual(compute_check_digit("142857"), 0)
        self.assertEqual(compute_check_digit("0"), 4)
        self.assertEqual(compute_check_digit(""), 0)
    
    def test_compute_check_digit_int(self):
        """Test check digit computation for integers."""
        self.assertEqual(compute_check_digit_int(12345), 1)
        self.assertEqual(compute_check_digit_int(0), 4)  # 0 has check digit 4
        self.assertEqual(compute_check_digit_int(999), 8)
    
    def test_compute_check_digit_invalid(self):
        """Test that non-digit inputs raise ValueError."""
        with self.assertRaises(ValueError):
            compute_check_digit("abc")
        with self.assertRaises(ValueError):
            compute_check_digit("123a5")
        with self.assertRaises(ValueError):
            compute_check_digit_int(-1)
    
    def test_validate_correct(self):
        """Test validation of correct numbers."""
        self.assertTrue(validate("123451"))  # 12345 with check digit 1
        self.assertTrue(validate("1428570"))  # 142857 with check digit 0
        self.assertTrue(validate("0"))        # Empty with check digit 0
        self.assertTrue(validate("04"))       # 0 with check digit 4
        self.assertTrue(validate("9998"))     # 999 with check digit 8
    
    def test_validate_incorrect(self):
        """Test validation of incorrect numbers."""
        self.assertFalse(validate("123450"))  # Wrong check digit
        self.assertFalse(validate("123452"))  # Wrong check digit
        self.assertFalse(validate("1428573"))  # Wrong check digit (correct is 0)
        self.assertFalse(validate("1"))        # Invalid (needs check digit)
    
    def test_validate_invalid_input(self):
        """Test validation with invalid inputs."""
        self.assertFalse(validate("abc"))
        self.assertFalse(validate("123a5"))
        self.assertFalse(validate(""))
    
    def test_validate_int(self):
        """Test integer validation."""
        self.assertTrue(validate_int(123451))
        self.assertFalse(validate_int(123450))
        self.assertFalse(validate_int(-1))
    
    def test_append_check_digit(self):
        """Test appending check digit."""
        self.assertEqual(append_check_digit("12345"), "123451")
        self.assertEqual(append_check_digit("142857"), "1428570")
        self.assertEqual(append_check_digit(""), "0")
    
    def test_append_check_digit_int(self):
        """Test appending check digit to integer."""
        self.assertEqual(append_check_digit_int(12345), 123451)
        self.assertEqual(append_check_digit_int(0), 4)  # 0 with check digit 4


class TestExtractOperations(unittest.TestCase):
    """Test extraction operations."""
    
    def test_get_check_digit_position(self):
        """Test check digit position."""
        self.assertEqual(get_check_digit_position("123451"), 5)
        self.assertEqual(get_check_digit_position("0"), 0)
    
    def test_extract_data_digits(self):
        """Test extracting data digits."""
        self.assertEqual(extract_data_digits("123451"), "12345")
        self.assertEqual(extract_data_digits("0"), "")
        self.assertEqual(extract_data_digits(""), "")
    
    def test_extract_data_digits_int(self):
        """Test extracting data digits from integer."""
        self.assertEqual(extract_data_digits_int(123451), 12345)
        self.assertEqual(extract_data_digits_int(0), 0)


class TestRoundTrip(unittest.TestCase):
    """Test round-trip operations (append then validate)."""
    
    def test_round_trip_various_numbers(self):
        """Test that append + validate always works."""
        test_numbers = [
            "", "0", "1", "9", "10", "11", "99", "100",
            "12345", "99999", "123456789", "987654321",
            "111111111", "222222222", "12345678901234567890"
        ]
        
        for num in test_numbers:
            with self.subTest(num=num):
                full = append_check_digit(num)
                self.assertTrue(validate(full), 
                    f"Round trip failed for {num}: got {full}")


class TestErrorDetection(unittest.TestCase):
    """Test error detection capabilities."""
    
    def test_detect_single_error(self):
        """Test single digit error detection."""
        # Single substitution
        result = detect_single_error("123451", "123351")
        self.assertEqual(result, (3, 4, 3))
        
        # No error
        result = detect_single_error("123451", "123451")
        self.assertIsNone(result)
        
        # Multiple errors
        result = detect_single_error("123451", "123352")
        self.assertIsNone(result)
        
        # Length change
        result = detect_single_error("123451", "12345")
        self.assertIsNone(result)
    
    def test_detect_transposition_error(self):
        """Test transposition error detection."""
        # Adjacent transposition
        result = detect_transposition_error("123451", "124351")
        self.assertEqual(result, (2, 3))
        
        # Another transposition
        result = detect_transposition_error("123451", "213451")
        self.assertEqual(result, (0, 1))
        
        # No error
        result = detect_transposition_error("123451", "123451")
        self.assertIsNone(result)
        
        # Non-adjacent swap (not a transposition)
        result = detect_transposition_error("123451", "321451")
        self.assertIsNone(result)
        
        # Not a swap
        result = detect_transposition_error("123451", "124551")
        self.assertIsNone(result)
    
    def test_analyze_error_single(self):
        """Test error analysis for single substitution."""
        result = analyze_error("123451", "123351")
        self.assertEqual(result['error_type'], 'single_substitution')
        self.assertEqual(result['position'], 3)
        self.assertFalse(result['valid'])
    
    def test_analyze_error_transposition(self):
        """Test error analysis for transposition."""
        result = analyze_error("123451", "124351")
        self.assertEqual(result['error_type'], 'transposition')
        self.assertEqual(result['position'], (2, 3))
        self.assertFalse(result['valid'])
    
    def test_analyze_error_no_error(self):
        """Test error analysis when no error."""
        result = analyze_error("123451", "123451")
        self.assertIsNone(result['error_type'])
        self.assertTrue(result['valid'])
    
    def test_analyze_error_multiple(self):
        """Test error analysis for multiple errors."""
        result = analyze_error("123451", "123352")
        # Two errors at positions 3 and 5 is a non_adjacent_swap
        self.assertEqual(result['error_type'], 'non_adjacent_swap')


class TestErrorDetectionCapability(unittest.TestCase):
    """Test that Verhoeff catches all single and transposition errors."""
    
    def test_catches_all_single_digit_errors(self):
        """Verhoeff should catch ALL single digit substitution errors."""
        base = "12345"
        full = append_check_digit(base)
        
        for pos in range(len(full)):
            for wrong_digit in range(10):
                if int(full[pos]) != wrong_digit:
                    modified = full[:pos] + str(wrong_digit) + full[pos+1:]
                    self.assertFalse(validate(modified),
                        f"Failed to catch error: {full} -> {modified} (pos {pos}, digit {wrong_digit})")
    
    def test_catches_all_adjacent_transpositions(self):
        """Verhoeff should catch ALL adjacent transposition errors."""
        base = "123456789"
        full = append_check_digit(base)
        
        for pos in range(len(full) - 1):
            if full[pos] != full[pos + 1]:  # Skip identical adjacent digits
                # Transpose adjacent digits
                modified = (full[:pos] + full[pos + 1] + full[pos] + 
                           full[pos + 2:])
                self.assertFalse(validate(modified),
                    f"Failed to catch transposition: {full} -> {modified} (pos {pos})")


class TestComparisonWithLuhn(unittest.TestCase):
    """Test comparison with Luhn algorithm."""
    
    def test_compare_basic(self):
        """Test basic comparison."""
        result = compare_with_luhn("12345")
        self.assertEqual(result['number'], "12345")
        self.assertEqual(result['verhoeff_check'], 1)
        self.assertEqual(result['luhn_check'], 5)
        self.assertEqual(result['verhoeff_full'], "123451")
        self.assertEqual(result['luhn_full'], "123455")
    
    def test_both_produce_valid_numbers(self):
        """Test that both algorithms produce valid numbers."""
        for num in ["12345", "98765", "11111", "99999", "123456789"]:
            result = compare_with_luhn(num)
            self.assertTrue(validate(result['verhoeff_full']))


class TestBatchOperations(unittest.TestCase):
    """Test batch operations."""
    
    def test_validate_batch(self):
        """Test batch validation."""
        numbers = ["123451", "123450", "1428570", "invalid", ""]
        results = validate_batch(numbers)
        
        self.assertEqual(results[0], ("123451", True))
        self.assertEqual(results[1], ("123450", False))
        self.assertEqual(results[2], ("1428570", True))
        self.assertEqual(results[3], ("invalid", False))
        self.assertEqual(results[4], ("", False))
    
    def test_generate_with_check_digits(self):
        """Test batch generation."""
        numbers = ["12345", "142857", "999"]
        results = generate_with_check_digits(numbers)
        
        self.assertEqual(results, ["123451", "1428570", "9998"])
        
        # All should be valid
        for r in results:
            self.assertTrue(validate(r))


class TestEducationalFunctions(unittest.TestCase):
    """Test educational functions."""
    
    def test_explain_algorithm(self):
        """Test that explain_algorithm returns a string."""
        explanation = explain_algorithm()
        self.assertIsInstance(explanation, str)
        self.assertIn("Verhoeff", explanation)
        self.assertIn("D5", explanation)
    
    def test_show_computation_steps(self):
        """Test computation step display."""
        steps = show_computation_steps("12345")
        self.assertIsInstance(steps, str)
        self.assertIn("12345", steps)
        self.assertIn("Check digit:", steps)
    
    def test_show_computation_steps_invalid(self):
        """Test computation steps with invalid input."""
        steps = show_computation_steps("abc")
        self.assertIn("Error", steps)


class TestTables(unittest.TestCase):
    """Test that the algorithm tables are properly defined."""
    
    def test_d5_multiplication_table(self):
        """Test D5 multiplication table dimensions."""
        self.assertEqual(len(D5_MULTIPLICATION), 10)
        for row in D5_MULTIPLICATION:
            self.assertEqual(len(row), 10)
    
    def test_permutation_table(self):
        """Test permutation table dimensions."""
        self.assertEqual(len(PERMUTATION), 8)
        for row in PERMUTATION:
            self.assertEqual(len(row), 10)
    
    def test_inverse_table(self):
        """Test inverse table."""
        self.assertEqual(len(INVERSE), 10)
        # Verify inverses
        for j in range(10):
            self.assertEqual(D5_MULTIPLICATION[INVERSE[j]][j], 0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_single_digit(self):
        """Test single digit numbers."""
        for d in range(10):
            full = append_check_digit(str(d))
            self.assertTrue(validate(full))
    
    def test_very_long_number(self):
        """Test with very long numbers."""
        long_num = "1" * 100
        full = append_check_digit(long_num)
        self.assertTrue(validate(full))
    
    def test_all_zeros(self):
        """Test with all zeros."""
        full = append_check_digit("00000")
        self.assertTrue(validate(full))
    
    def test_all_nines(self):
        """Test with all nines."""
        full = append_check_digit("99999")
        self.assertTrue(validate(full))
    
    def test_sequential_digits(self):
        """Test with sequential digits."""
        for start in range(10):
            seq = "".join(str((start + i) % 10) for i in range(10))
            full = append_check_digit(seq)
            self.assertTrue(validate(full))


class TestKnownValues(unittest.TestCase):
    """Test against known Verhoeff check digit values."""
    
    def test_known_values(self):
        """Test against known check digit values."""
        # Test values computed by the implemented algorithm
        known_cases = [
            ("", 0),
            ("1", 5),
            ("12", 1),
            ("123", 3),
            ("1234", 0),
            ("12345", 1),
            ("123456", 8),
            ("1234567", 9),
            ("12345678", 4),
            ("123456789", 0),
            ("1234567890", 2),
            ("0", 4),
            ("10", 9),
            ("100", 3),
            ("142857", 0),
            ("999", 8),
        ]
        
        for number, expected_check in known_cases:
            with self.subTest(number=number):
                computed = compute_check_digit(number)
                self.assertEqual(computed, expected_check,
                    f"Mismatch for '{number}': got {computed}, expected {expected_check}")


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)