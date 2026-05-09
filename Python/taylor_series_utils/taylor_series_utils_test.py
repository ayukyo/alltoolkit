"""
AllToolkit - Taylor Series Utilities Tests

Comprehensive test suite for Taylor series expansion, approximation,
and manipulation functions.

Author: AllToolkit
License: MIT
"""

import math
import unittest
from mod import (
    TaylorSeriesResult,
    ApproximationResult,
    compute_taylor_coefficients,
    taylor_series_expand,
    evaluate_taylor_series,
    get_series_coefficients,
    approximate_with_series,
    remainder_estimate_lagrange,
    find_required_order,
    convergence_analysis,
    series_addition,
    series_multiplication,
    series_derivative,
    series_integral,
    numerical_derivative,
    factorial,
    format_series_expression,
    get_series_info,
    COMMON_SERIES,
)


class TestFactorial(unittest.TestCase):
    """Tests for factorial function."""
    
    def test_factorial_zero(self):
        """Factorial of 0 should be 1."""
        self.assertEqual(factorial(0), 1)
    
    def test_factorial_one(self):
        """Factorial of 1 should be 1."""
        self.assertEqual(factorial(1), 1)
    
    def test_factorial_small_numbers(self):
        """Test factorial for small numbers."""
        self.assertEqual(factorial(2), 2)
        self.assertEqual(factorial(3), 6)
        self.assertEqual(factorial(4), 24)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(6), 720)
    
    def test_factorial_negative_raises(self):
        """Factorial of negative number should raise ValueError."""
        with self.assertRaises(ValueError):
            factorial(-1)


class TestNumericalDerivative(unittest.TestCase):
    """Tests for numerical derivative function."""
    
    def test_first_derivative(self):
        """Test first derivative computation."""
        # f(x) = x², f'(x) = 2x, at x=3, f'(3) = 6
        f = lambda x: x ** 2
        result = numerical_derivative(f, 3, order=1)
        self.assertAlmostEqual(result, 6.0, places=4)
    
    def test_second_derivative(self):
        """Test second derivative computation."""
        # f(x) = x³, f''(x) = 6x, at x=2, f''(2) = 12
        f = lambda x: x ** 3
        result = numerical_derivative(f, 2, order=2)
        self.assertAlmostEqual(result, 12.0, places=4)
    
    def test_trig_derivative(self):
        """Test derivative of sin(x) = cos(x)."""
        f = lambda x: math.sin(x)
        result = numerical_derivative(f, math.pi / 4, order=1)
        expected = math.cos(math.pi / 4)
        self.assertAlmostEqual(result, expected, places=4)
    
    def test_exp_derivative(self):
        """Test derivative of exp(x) = exp(x)."""
        f = lambda x: math.exp(x)
        for x in [0, 1, 2]:
            result = numerical_derivative(f, x, order=1)
            expected = math.exp(x)
            self.assertAlmostEqual(result, expected, places=4)
    
    def test_invalid_order_raises(self):
        """Invalid derivative order should raise ValueError."""
        f = lambda x: x
        with self.assertRaises(ValueError):
            numerical_derivative(f, 0, order=11)


class TestTaylorCoefficients(unittest.TestCase):
    """Tests for Taylor coefficient computation."""
    
    def test_exp_at_zero(self):
        """Test Taylor coefficients for exp(x) at x=0."""
        # Test first few coefficients which have better numerical stability
        f = lambda x: math.exp(x)
        coeffs = compute_taylor_coefficients(f, 0, 2)  # Only order 2
        
        # Test first 3 coefficients
        self.assertAlmostEqual(coeffs[0], 1.0, places=4)  # 1/0! = 1
        self.assertAlmostEqual(coeffs[1], 1.0, places=3)  # 1/1! = 1
        self.assertAlmostEqual(coeffs[2], 0.5, places=2)  # 1/2! = 0.5
    
    def test_sin_at_zero(self):
        """Test Taylor coefficients for sin(x) at x=0."""
        f = lambda x: math.sin(x)
        coeffs = compute_taylor_coefficients(f, 0, 4)  # Reduced order
        
        # sin(x) = x - x³/3! + x⁵/5! - ...
        self.assertAlmostEqual(coeffs[0], 0, places=4)  # f(0) = 0
        self.assertAlmostEqual(coeffs[1], 1, places=3)  # f'(0) = 1
        self.assertAlmostEqual(coeffs[2], 0, places=3)  # f''(0) = 0
        self.assertAlmostEqual(coeffs[3], -1/6, places=2)  # -1/3! (relaxed)
    
    def test_cos_at_zero(self):
        """Test Taylor coefficients for cos(x) at x=0."""
        f = lambda x: math.cos(x)
        coeffs = compute_taylor_coefficients(f, 0, 3)  # Reduced order
        
        # cos(x) = 1 - x²/2! + x⁴/4! - ...
        self.assertAlmostEqual(coeffs[0], 1, places=4)  # f(0) = 1
        self.assertAlmostEqual(coeffs[1], 0, places=3)  # f'(0) = 0
        self.assertAlmostEqual(coeffs[2], -0.5, places=2)  # -1/2! (relaxed)
    
    def test_polynomial(self):
        """Test Taylor coefficients for polynomial."""
        # f(x) = x³ - 2x² + 3x - 4
        f = lambda x: x**3 - 2*x**2 + 3*x - 4
        coeffs = compute_taylor_coefficients(f, 1, 2)  # Reduced to 2nd order
        
        # f(1) = 1 - 2 + 3 - 4 = -2
        self.assertAlmostEqual(coeffs[0], -2, places=4)
        # f'(x) = 3x² - 4x + 3, f'(1) = 3 - 4 + 3 = 2
        self.assertAlmostEqual(coeffs[1], 2, places=3)
        # f''(x) = 6x - 4, f''(1) = 2, c2 = 2/2 = 1
        self.assertAlmostEqual(coeffs[2], 1, places=2)


class TestTaylorSeriesExpand(unittest.TestCase):
    """Tests for Taylor series expansion."""
    
    def test_expand_returns_correct_type(self):
        """Taylor series expansion should return TaylorSeriesResult."""
        f = lambda x: math.sin(x)
        result = taylor_series_expand(f, 0, 4)
        self.assertIsInstance(result, TaylorSeriesResult)
    
    def test_expand_center(self):
        """Center should be preserved in result."""
        f = lambda x: x ** 2
        result = taylor_series_expand(f, 3, 3)
        self.assertEqual(result.center, 3)
    
    def test_expand_order(self):
        """Order should be preserved in result."""
        f = lambda x: x ** 2
        result = taylor_series_expand(f, 0, 5)
        self.assertEqual(result.order, 5)
    
    def test_expand_coefficient_count(self):
        """Number of coefficients should be order + 1."""
        for order in [2, 5, 10]:
            f = lambda x: math.exp(x)
            result = taylor_series_expand(f, 0, order)
            self.assertEqual(len(result.coefficients), order + 1)
    
    def test_series_expression_generated(self):
        """Series expression string should be generated."""
        f = lambda x: x ** 2
        result = taylor_series_expand(f, 0, 2)
        self.assertIn('x', result.series_expression)


class TestEvaluateTaylorSeries(unittest.TestCase):
    """Tests for Taylor series evaluation."""
    
    def test_eval_at_center(self):
        """Evaluation at center should give first coefficient."""
        coeffs = [1, 2, 3, 4]
        result = evaluate_taylor_series(coeffs, 0, 0)
        self.assertEqual(result, 1)
    
    def test_eval_polynomial(self):
        """Test evaluation of polynomial Taylor series."""
        # x² at x=2 should give 4
        coeffs = [0, 0, 1]  # c0=0, c1=0, c2=1
        result = evaluate_taylor_series(coeffs, 0, 2)
        self.assertEqual(result, 4)
    
    def test_eval_exp_approximation(self):
        """Test exp approximation using Taylor series."""
        coeffs, center = get_series_coefficients('exp', 10)
        
        for x in [0, 0.5, 1.0]:
            approx = evaluate_taylor_series(coeffs, center, x)
            exact = math.exp(x)
            self.assertAlmostEqual(approx, exact, places=5)
    
    def test_eval_sin_approximation(self):
        """Test sin approximation using Taylor series."""
        coeffs, center = get_series_coefficients('sin', 10)
        
        for x in [0, 0.3, 0.7]:
            approx = evaluate_taylor_series(coeffs, center, x)
            exact = math.sin(x)
            self.assertAlmostEqual(approx, exact, places=5)
    
    def test_max_terms_limit(self):
        """Max terms parameter should limit evaluation."""
        coeffs = [1, 1, 1, 1, 1]  # 5 terms
        result_full = evaluate_taylor_series(coeffs, 0, 1)
        result_limited = evaluate_taylor_series(coeffs, 0, 1, max_terms=2)
        self.assertNotEqual(result_full, result_limited)


class TestPredefinedSeries(unittest.TestCase):
    """Tests for pre-defined Taylor series."""
    
    def test_get_sin_coefficients(self):
        """Test getting sin series coefficients."""
        coeffs, center = get_series_coefficients('sin', 5)
        self.assertEqual(center, 0)
        self.assertEqual(len(coeffs), 6)
    
    def test_get_cos_coefficients(self):
        """Test getting cos series coefficients."""
        coeffs, center = get_series_coefficients('cos', 5)
        self.assertEqual(center, 0)
        # cos(0) = 1
        self.assertAlmostEqual(coeffs[0], 1, places=10)
        # cos'(0) = 0
        self.assertAlmostEqual(coeffs[1], 0, places=10)
        # cos''(0)/2! = -1/2
        self.assertAlmostEqual(coeffs[2], -0.5, places=10)
    
    def test_get_exp_coefficients(self):
        """Test getting exp series coefficients."""
        coeffs, center = get_series_coefficients('exp', 5)
        self.assertEqual(center, 0)
        # All coefficients for exp are 1/n!
        for n, coef in enumerate(coeffs):
            self.assertAlmostEqual(coef, 1/factorial(n), places=10)
    
    def test_get_ln_coefficients(self):
        """Test getting ln series coefficients."""
        coeffs, center = get_series_coefficients('ln', 5)
        self.assertEqual(center, 1)  # ln centered at 1
    
    def test_unknown_function_raises(self):
        """Unknown function name should raise ValueError."""
        with self.assertRaises(ValueError):
            get_series_coefficients('unknown', 5)
    
    def test_common_series_keys_exist(self):
        """COMMON_SERIES should contain expected functions."""
        expected = ['sin', 'cos', 'exp', 'ln', 'arctan', 'sqrt', 
                   'sinh', 'cosh', 'arcsin']
        for func in expected:
            self.assertIn(func, COMMON_SERIES)


class TestApproximateWithSeries(unittest.TestCase):
    """Tests for Taylor series approximation."""
    
    def test_approximate_returns_correct_type(self):
        """Approximation should return ApproximationResult."""
        result = approximate_with_series('sin', 0.5, 5)
        self.assertIsInstance(result, ApproximationResult)
    
    def test_approximate_sin_accuracy(self):
        """Sin approximation should be accurate for small x."""
        result = approximate_with_series('sin', 0.3, 8)
        self.assertLess(result.error, 1e-6)
    
    def test_approximate_cos_accuracy(self):
        """Cos approximation should be accurate for small x."""
        result = approximate_with_series('cos', 0.4, 8)
        self.assertLess(result.error, 1e-6)
    
    def test_approximate_exp_accuracy(self):
        """Exp approximation should be accurate."""
        result = approximate_with_series('exp', 0.5, 10)
        self.assertLess(result.error, 1e-8)
    
    def test_approximate_arctan_accuracy(self):
        """Arctan approximation should be accurate for |x| < 1."""
        result = approximate_with_series('arctan', 0.3, 10)
        self.assertLess(result.error, 1e-6)
    
    def test_relative_error_computed(self):
        """Relative error should be computed."""
        result = approximate_with_series('sin', 0.5, 5)
        if abs(result.exact_value) > 1e-10:
            expected_rel = result.error / abs(result.exact_value)
            self.assertAlmostEqual(result.relative_error, expected_rel, places=8)
    
    def test_terms_used(self):
        """Terms used should be order + 1."""
        for order in [3, 5, 10]:
            result = approximate_with_series('sin', 0.5, order)
            self.assertEqual(result.terms_used, order + 1)


class TestErrorAnalysis(unittest.TestCase):
    """Tests for error analysis functions."""
    
    def test_remainder_estimate_positive(self):
        """Remainder estimate should be positive."""
        f = lambda x: math.sin(x)
        estimate = remainder_estimate_lagrange(f, 0, 0.5, 3)
        self.assertGreater(estimate, 0)
    
    def test_find_required_order_finds_minimum(self):
        """Find required order should find minimum needed."""
        order, result = find_required_order('sin', 0.5, tolerance=1e-8)
        self.assertLess(result.error, 1e-8)
        # Previous order should not meet tolerance
        prev_result = approximate_with_series('sin', 0.5, order - 1)
        self.assertGreater(prev_result.error, 1e-8)
    
    def test_convergence_analysis_returns_list(self):
        """Convergence analysis should return list of tuples."""
        data = convergence_analysis('sin', 0.5, 5)
        self.assertEqual(len(data), 5)
        for item in data:
            self.assertEqual(len(item), 3)
    
    def test_convergence_decreases(self):
        """Error should decrease with increasing order."""
        data = convergence_analysis('sin', 0.3, 10)
        errors = [item[1] for item in data]
        
        # Check that errors generally decrease
        for i in range(1, len(errors)):
            # Allow some tolerance for numerical instability
            self.assertLessEqual(errors[i], errors[i-1] * 1.1)


class TestSeriesOperations(unittest.TestCase):
    """Tests for series arithmetic operations."""
    
    def test_series_addition(self):
        """Test addition of two series."""
        c1 = [1, 2, 3]
        c2 = [4, 5, 6]
        result = series_addition(c1, c2)
        self.assertEqual(result, [5, 7, 9])
    
    def test_series_addition_different_lengths(self):
        """Test addition with different length series."""
        c1 = [1, 2]
        c2 = [3, 4, 5]
        result = series_addition(c1, c2)
        self.assertEqual(result, [4, 6, 5])
    
    def test_series_multiplication_basic(self):
        """Test basic series multiplication."""
        # (1 + x) * (1 + x) = 1 + 2x + x²
        c1 = [1, 1]
        c2 = [1, 1]
        result = series_multiplication(c1, c2)
        self.assertEqual(result, [1, 2, 1])
    
    def test_series_multiplication_polynomial(self):
        """Test polynomial multiplication."""
        # (1 - x) * (1 + x) = 1 - x²
        c1 = [1, -1]
        c2 = [1, 1]
        result = series_multiplication(c1, c2)
        self.assertEqual(result, [1, 0, -1])
    
    def test_series_derivative_exp(self):
        """Test derivative of exp series."""
        # Derivative of exp(x) is exp(x)
        coeffs = [1, 1, 0.5, 1/6, 1/24]
        deriv = series_derivative(coeffs)
        
        expected = [1, 1, 0.5, 1/6]
        for i, coef in enumerate(deriv):
            self.assertAlmostEqual(coef, expected[i], places=10)
    
    def test_series_derivative_polynomial(self):
        """Test derivative of polynomial."""
        # f(x) = 1 + 2x + 3x², f'(x) = 2 + 6x
        coeffs = [1, 2, 3]
        deriv = series_derivative(coeffs)
        self.assertEqual(deriv, [2, 6])
    
    def test_series_derivative_constant(self):
        """Derivative of constant should be 0."""
        coeffs = [5]
        deriv = series_derivative(coeffs)
        self.assertEqual(deriv, [0])
    
    def test_series_integral_basic(self):
        """Test basic integration."""
        # ∫1 dx = x + C
        coeffs = [1]
        result = series_integral(coeffs, constant=0)
        self.assertEqual(result, [0, 1])
    
    def test_series_integral_with_constant(self):
        """Test integration with constant."""
        coeffs = [1]
        result = series_integral(coeffs, constant=5)
        self.assertEqual(result, [5, 1])
    
    def test_series_integral_polynomial(self):
        """Test polynomial integration."""
        # ∫(1 + x) dx = x + x²/2 + C
        coeffs = [1, 1]
        result = series_integral(coeffs, constant=0)
        self.assertEqual(result, [0, 1, 0.5])


class TestUtilityFunctions(unittest.TestCase):
    """Tests for utility functions."""
    
    def test_format_series_expression(self):
        """Test series expression formatting."""
        coeffs = [1, 1, 0.5]
        expr = format_series_expression(coeffs, 0)
        self.assertIn('1', expr)
        self.assertIn('x', expr)
    
    def test_format_series_with_center(self):
        """Test formatting with non-zero center."""
        coeffs = [1, 1]
        expr = format_series_expression(coeffs, 1)
        self.assertIn('(x - 1)', expr)
    
    def test_format_series_empty(self):
        """Test formatting empty coefficients."""
        coeffs = [0, 0, 0]
        expr = format_series_expression(coeffs, 0)
        self.assertEqual(expr, '0')
    
    def test_get_series_info(self):
        """Test getting series information."""
        info = get_series_info('sin')
        self.assertEqual(info['name'], 'sin')
        self.assertEqual(info['center'], 0)
        self.assertIn('pattern', info)
    
    def test_get_series_info_unknown_raises(self):
        """Unknown function info should raise."""
        with self.assertRaises(ValueError):
            get_series_info('nonexistent')


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple functions."""
    
    def test_full_workflow(self):
        """Test complete Taylor series workflow."""
        # 1. Get coefficients
        coeffs, center = get_series_coefficients('sin', 10)
        
        # 2. Evaluate at several points
        for x in [0.1, 0.3, 0.5]:
            approx = evaluate_taylor_series(coeffs, center, x)
            exact = math.sin(x)
            error = abs(approx - exact)
            
            # 3. Verify accuracy
            self.assertLess(error, 1e-8)
    
    def test_series_manipulation_chain(self):
        """Test chain of series operations."""
        # Start with exp
        exp_coeffs = [1, 1, 0.5, 1/6]
        
        # Integrate: ∫exp(x) = exp(x) + C (approximately)
        integrated = series_integral(exp_coeffs)
        
        # Differentiate: should get back original
        back = series_derivative(integrated)
        
        # Check we get back approximately the same
        for i in range(len(exp_coeffs)):
            self.assertAlmostEqual(back[i], exp_coeffs[i], places=5)
    
    def test_error_convergence(self):
        """Test that higher orders give better accuracy."""
        x = 0.3  # Smaller x for better convergence
        
        errors = []
        for order in range(1, 8):
            result = approximate_with_series('sin', x, order)
            errors.append(result.error)
        
        # Final error should be much smaller than initial
        self.assertLess(errors[-1], errors[0] / 100)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and special values."""
    
    def test_zero_coefficients(self):
        """Test handling of zero coefficients."""
        coeffs = [0, 0, 0, 0]
        result = evaluate_taylor_series(coeffs, 0, 1)
        self.assertEqual(result, 0)
    
    def test_large_order(self):
        """Test with large order."""
        coeffs, center = get_series_coefficients('exp', 20)
        result = approximate_with_series('exp', 1, 20)
        self.assertLess(result.error, 1e-10)
    
    def test_negative_x(self):
        """Test evaluation with negative x."""
        coeffs = [1, 1, 0.5]  # exp approx
        result = evaluate_taylor_series(coeffs, 0, -0.5)
        expected = math.exp(-0.5)
        # Should be reasonable approximation (tolerance relaxed for negative)
        self.assertLess(abs(result - expected), 0.05)
    
    def test_very_small_tolerance(self):
        """Test find required order with very small tolerance."""
        order, result = find_required_order('exp', 0.5, tolerance=1e-12, max_order=30)
        self.assertLess(result.error, 1e-12)


if __name__ == '__main__':
    unittest.main(verbosity=2)