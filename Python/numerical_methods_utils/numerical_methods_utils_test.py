"""
Test suite for numerical_methods_utils module.

Tests root finding, integration, differentiation, interpolation,
and optimization functions.
"""

import math
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Root finding
    bisection, newton_raphson, secant_method, brent_method,
    # Integration
    trapezoidal_rule, simpsons_rule, adaptive_simpson, gaussian_quadrature,
    # Differentiation
    forward_difference, backward_difference, central_difference,
    second_derivative, richardson_extrapolation,
    # Interpolation
    linear_interpolation, lagrange_interpolation,
    newton_divided_difference, newton_interpolation,
    cubic_spline_coefficients, cubic_spline_interpolation,
    # Optimization
    golden_section_search, gradient_descent_1d, nelder_mead_1d,
    approximate_derivative,
    # Data classes
    RootResult, IntegrationResult,
)


def test_bisection():
    """Test bisection method for root finding."""
    print("Testing bisection method...")
    
    # Test sqrt(2)
    f = lambda x: x**2 - 2
    result = bisection(f, 1, 2)
    assert result.converged, "Should converge"
    assert abs(result.root - math.sqrt(2)) < 1e-9, f"Root should be sqrt(2), got {result.root}"
    
    # Test x^3 - x - 2 (known root ~1.521)
    f = lambda x: x**3 - x - 2
    result = bisection(f, 1, 2)
    assert result.converged, "Should converge"
    assert abs(f(result.root)) < 1e-10, f"f(root) should be ~0, got {f(result.root)}"
    
    # Test error case: same signs
    try:
        bisection(lambda x: x**2 + 1, -1, 1)  # No real root
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    # Test root at endpoint
    result = bisection(lambda x: x, 0, 1)
    assert abs(result.root) < 1e-10, f"Root should be 0, got {result.root}"
    
    print("  ✓ All bisection tests passed")


def test_newton_raphson():
    """Test Newton-Raphson method."""
    print("Testing Newton-Raphson method...")
    
    # Test sqrt(2)
    f = lambda x: x**2 - 2
    df = lambda x: 2*x
    result = newton_raphson(f, df, 1.5)
    assert result.converged, "Should converge"
    assert abs(result.root - math.sqrt(2)) < 1e-9, f"Root should be sqrt(2), got {result.root}"
    
    # Test finding root of sin(x) near π
    result = newton_raphson(math.sin, math.cos, 3.0)
    assert result.converged, "Should converge"
    assert abs(result.root - math.pi) < 1e-9, f"Root should be π, got {result.root}"
    
    # Test derivative zero case
    result = newton_raphson(lambda x: x**2, lambda x: 2*x, 0.0)
    # At x=0, derivative is 0, but we're already at the root
    assert abs(result.root) < 1e-10 or not result.converged
    
    print("  ✓ All Newton-Raphson tests passed")


def test_secant_method():
    """Test secant method."""
    print("Testing secant method...")
    
    # Test sqrt(2)
    f = lambda x: x**2 - 2
    result = secant_method(f, 1, 2)
    assert result.converged, "Should converge"
    assert abs(result.root - math.sqrt(2)) < 1e-9, f"Root should be sqrt(2), got {result.root}"
    
    # Test exp(x) - 1 = 0 (root at x=0)
    result = secant_method(lambda x: math.exp(x) - 1, -0.5, 0.5)
    assert result.converged, "Should converge"
    assert abs(result.root) < 1e-9, f"Root should be 0, got {result.root}"
    
    print("  ✓ All secant method tests passed")


def test_brent_method():
    """Test Brent's method."""
    print("Testing Brent's method...")
    
    # Test sqrt(2)
    f = lambda x: x**2 - 2
    result = brent_method(f, 1, 2)
    assert result.converged, "Should converge"
    assert abs(result.root - math.sqrt(2)) < 1e-9, f"Root should be sqrt(2), got {result.root}"
    
    # Test cos(x) = 0 (root at π/2)
    result = brent_method(math.cos, 0, 2)
    assert result.converged, "Should converge"
    assert abs(result.root - math.pi/2) < 1e-9, f"Root should be π/2, got {result.root}"
    
    print("  ✓ All Brent's method tests passed")


def test_trapezoidal_rule():
    """Test trapezoidal rule integration."""
    print("Testing trapezoidal rule...")
    
    # Test x^2 from 0 to 1 (exact: 1/3)
    result = trapezoidal_rule(lambda x: x**2, 0, 1, 1000)
    assert abs(result.value - 1/3) < 1e-4, f"Integral should be ~0.333, got {result.value}"
    
    # Test sin(x) from 0 to π (exact: 2)
    result = trapezoidal_rule(math.sin, 0, math.pi, 1000)
    assert abs(result.value - 2) < 1e-3, f"Integral should be ~2, got {result.value}"
    
    # Test constant function
    result = trapezoidal_rule(lambda x: 5, 0, 2, 10)
    assert abs(result.value - 10) < 1e-10, f"Integral should be 10, got {result.value}"
    
    print("  ✓ All trapezoidal rule tests passed")


def test_simpsons_rule():
    """Test Simpson's rule integration."""
    print("Testing Simpson's rule...")
    
    # Test x^2 from 0 to 1 (exact: 1/3)
    result = simpsons_rule(lambda x: x**2, 0, 1, 10)
    # Simpson's rule is exact for polynomials up to degree 3
    assert abs(result.value - 1/3) < 1e-10, f"Integral should be 1/3, got {result.value}"
    
    # Test sin(x) from 0 to π (exact: 2)
    result = simpsons_rule(math.sin, 0, math.pi, 100)
    assert abs(result.value - 2) < 1e-6, f"Integral should be ~2, got {result.value}"
    
    # Test x^3 from 0 to 1 (exact: 1/4)
    result = simpsons_rule(lambda x: x**3, 0, 1, 10)
    assert abs(result.value - 0.25) < 1e-10, f"Integral should be 0.25, got {result.value}"
    
    # Test n must be even
    try:
        simpsons_rule(lambda x: x, 0, 1, 5)
        assert False, "Should raise ValueError for odd n"
    except ValueError:
        pass
    
    print("  ✓ All Simpson's rule tests passed")


def test_adaptive_simpson():
    """Test adaptive Simpson's integration."""
    print("Testing adaptive Simpson's rule...")
    
    # Test sin(x) from 0 to π
    result = adaptive_simpson(math.sin, 0, math.pi)
    assert abs(result.value - 2) < 1e-9, f"Integral should be ~2, got {result.value}"
    
    # Test exp(x) from 0 to 1 (exact: e - 1)
    result = adaptive_simpson(math.exp, 0, 1)
    assert abs(result.value - (math.e - 1)) < 1e-9, f"Integral should be e-1, got {result.value}"
    
    print("  ✓ All adaptive Simpson's tests passed")


def test_gaussian_quadrature():
    """Test Gaussian quadrature integration."""
    print("Testing Gaussian quadrature...")
    
    # Test sin(x) from 0 to π
    result = gaussian_quadrature(math.sin, 0, math.pi, 5)
    assert abs(result.value - 2) < 1e-6, f"Integral should be ~2, got {result.value}"
    
    # Test exp(x) from 0 to 1
    result = gaussian_quadrature(math.exp, 0, 1, 5)
    assert abs(result.value - (math.e - 1)) < 1e-9, f"Integral should be e-1, got {result.value}"
    
    # Test error case: invalid n
    try:
        gaussian_quadrature(lambda x: x, 0, 1, 0)
        assert False, "Should raise ValueError for n < 1"
    except ValueError:
        pass
    
    print("  ✓ All Gaussian quadrature tests passed")


def test_forward_difference():
    """Test forward difference differentiation."""
    print("Testing forward difference...")
    
    # Test x^2 at x=3 (derivative = 6)
    result = forward_difference(lambda x: x**2, 3)
    assert abs(result - 6) < 1e-4, f"Derivative should be ~6, got {result}"
    
    # Test sin(x) at x=0 (derivative = 1)
    result = forward_difference(math.sin, 0)
    assert abs(result - 1) < 1e-4, f"Derivative should be ~1, got {result}"
    
    print("  ✓ All forward difference tests passed")


def test_backward_difference():
    """Test backward difference differentiation."""
    print("Testing backward difference...")
    
    # Test x^2 at x=3 (derivative = 6)
    result = backward_difference(lambda x: x**2, 3)
    assert abs(result - 6) < 1e-4, f"Derivative should be ~6, got {result}"
    
    print("  ✓ All backward difference tests passed")


def test_central_difference():
    """Test central difference differentiation."""
    print("Testing central difference...")
    
    # Test x^2 at x=3 (derivative = 6)
    result = central_difference(lambda x: x**2, 3)
    assert abs(result - 6) < 1e-6, f"Derivative should be ~6, got {result}"
    
    # Test x^3 at x=2 (derivative = 12)
    result = central_difference(lambda x: x**3, 2)
    assert abs(result - 12) < 1e-7, f"Derivative should be ~12, got {result}"
    
    # Test sin(x) at x=π/4 (derivative = cos(π/4) = sqrt(2)/2)
    result = central_difference(math.sin, math.pi/4)
    assert abs(result - math.sqrt(2)/2) < 1e-6, f"Derivative should be sqrt(2)/2, got {result}"
    
    print("  ✓ All central difference tests passed")


def test_second_derivative():
    """Test second derivative calculation."""
    print("Testing second derivative...")
    
    # Test x^3 at x=2 (second derivative = 12)
    result = second_derivative(lambda x: x**3, 2)
    assert abs(result - 12) < 1e-5, f"Second derivative should be 12, got {result}"
    
    # Test sin(x) at x=0 (second derivative = -sin(0) = 0)
    result = second_derivative(math.sin, 0)
    assert abs(result) < 1e-4, f"Second derivative should be 0, got {result}"
    
    # Test x^2 at x=5 (second derivative = 2)
    result = second_derivative(lambda x: x**2, 5)
    assert abs(result - 2) < 1e-3, f"Second derivative should be ~2, got {result}"
    
    print("  ✓ All second derivative tests passed")


def test_richardson_extrapolation():
    """Test Richardson extrapolation for derivative."""
    print("Testing Richardson extrapolation...")
    
    # Test x^3 at x=2 (derivative = 12)
    result = richardson_extrapolation(lambda x: x**3, 2)
    assert abs(result - 12) < 1e-9, f"Derivative should be 12, got {result}"
    
    # Test exp(x) at x=1 (derivative = e)
    result = richardson_extrapolation(math.exp, 1)
    assert abs(result - math.e) < 1e-8, f"Derivative should be e, got {result}"
    
    print("  ✓ All Richardson extrapolation tests passed")


def test_linear_interpolation():
    """Test linear interpolation."""
    print("Testing linear interpolation...")
    
    x_data = [0, 1, 2]
    y_data = [0, 2, 4]
    
    # Test at 1.5 (should be 3)
    result = linear_interpolation(x_data, y_data, 1.5)
    assert abs(result - 3) < 1e-10, f"Interpolation should be 3, got {result}"
    
    # Test at 0.5 (should be 1)
    result = linear_interpolation(x_data, y_data, 0.5)
    assert abs(result - 1) < 1e-10, f"Interpolation should be 1, got {result}"
    
    # Test error: different lengths
    try:
        linear_interpolation([0, 1], [0, 1, 2], 0.5)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    # Test error: out of range
    try:
        linear_interpolation(x_data, y_data, 3)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("  ✓ All linear interpolation tests passed")


def test_lagrange_interpolation():
    """Test Lagrange interpolation."""
    print("Testing Lagrange interpolation...")
    
    # Test quadratic function: y = x^2
    x_data = [0, 1, 2]
    y_data = [0, 1, 4]  # y = x^2
    
    # Test at 1.5 (should be 2.25)
    result = lagrange_interpolation(x_data, y_data, 1.5)
    assert abs(result - 2.25) < 1e-10, f"Interpolation should be 2.25, got {result}"
    
    # Test at known point (should return exact value)
    result = lagrange_interpolation(x_data, y_data, 1)
    assert abs(result - 1) < 1e-10, f"Interpolation should be 1, got {result}"
    
    print("  ✓ All Lagrange interpolation tests passed")


def test_newton_interpolation():
    """Test Newton interpolation."""
    print("Testing Newton interpolation...")
    
    x_data = [0, 1, 2, 3]
    y_data = [0, 1, 4, 9]  # y = x^2
    
    # Test at 2.5 (should be 6.25)
    result = newton_interpolation(x_data, y_data, 2.5)
    assert abs(result - 6.25) < 1e-10, f"Interpolation should be 6.25, got {result}"
    
    # Test divided difference coefficients
    coeffs = newton_divided_difference(x_data, y_data)
    # For y = x^2, coefficients are [0, 1, 1]
    assert abs(coeffs[0]) < 1e-10, f"First coefficient should be 0, got {coeffs[0]}"
    assert abs(coeffs[1] - 1) < 1e-10, f"Second coefficient should be 1, got {coeffs[1]}"
    assert abs(coeffs[2] - 1) < 1e-10, f"Third coefficient should be 1, got {coeffs[2]}"
    
    print("  ✓ All Newton interpolation tests passed")


def test_cubic_spline_interpolation():
    """Test cubic spline interpolation."""
    print("Testing cubic spline interpolation...")
    
    x_data = [0, 1, 2, 3]
    y_data = [0, 1, 8, 27]  # y = x^3
    
    # Test at 1.5 - cubic spline on x^3 will have some error
    result = cubic_spline_interpolation(x_data, y_data, 1.5)
    # Should be reasonably close to 3.375
    assert abs(result - 3.375) < 0.3, f"Interpolation should be ~3.375, got {result}"
    
    # Test at endpoint
    result = cubic_spline_interpolation(x_data, y_data, 0)
    assert abs(result - 0) < 1e-10, f"Interpolation should be 0, got {result}"
    
    # Test error: out of range
    try:
        cubic_spline_interpolation(x_data, y_data, 4)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("  ✓ All cubic spline tests passed")


def test_golden_section_search():
    """Test golden section search optimization."""
    print("Testing golden section search...")
    
    # Test (x-2)^2 (minimum at x=2)
    result = golden_section_search(lambda x: (x-2)**2, 0, 4)
    assert result.converged, "Should converge"
    assert abs(result.root - 2) < 1e-9, f"Minimum should be at x=2, got {result.root}"
    
    # Test sin(x) from 0 to π (maximum at π/2)
    result = golden_section_search(math.sin, 0, math.pi, find_min=False)
    assert result.converged, "Should converge"
    assert abs(result.root - math.pi/2) < 1e-7, f"Maximum should be ~π/2, got {result.root}"
    
    print("  ✓ All golden section search tests passed")


def test_gradient_descent_1d():
    """Test 1D gradient descent."""
    print("Testing gradient descent 1D...")
    
    # Test (x-3)^2 (minimum at x=3)
    df = lambda x: 2*(x-3)
    result = gradient_descent_1d(df, 0.0, lr=0.1)
    assert result.converged, "Should converge"
    assert abs(result.root - 3) < 1e-8, f"Minimum should be at x=3, got {result.root}"
    
    # Test with momentum
    result = gradient_descent_1d(df, 10.0, lr=0.05, momentum=0.5)
    assert abs(result.root - 3) < 1e-6, f"Minimum should be at x=3, got {result.root}"
    
    print("  ✓ All gradient descent tests passed")


def test_nelder_mead_1d():
    """Test 1D Nelder-Mead pattern search."""
    print("Testing Nelder-Mead 1D...")
    
    # Test (x-5)^2 + 2 (minimum at x=5)
    f = lambda x: (x-5)**2 + 2
    result = nelder_mead_1d(f, 0.0)
    assert result.converged or abs(result.root - 5) < 0.1, "Should find minimum near x=5"
    
    print("  ✓ All Nelder-Mead tests passed")


def test_approximate_derivative():
    """Test approximate derivative function."""
    print("Testing approximate_derivative...")
    
    f = lambda x: x**4
    
    # First derivative at x=1 (should be 4)
    result = approximate_derivative(f, 1, order=1, method='central')
    assert abs(result - 4) < 1e-5, f"Derivative should be 4, got {result}"
    
    # Second derivative at x=1 (should be 12)
    result = approximate_derivative(f, 1, order=2, method='central')
    assert abs(result - 12) < 1e-3, f"Second derivative should be ~12, got {result}"
    
    # Third derivative at x=1 (should be 24) - use larger h for stability
    result = approximate_derivative(f, 1, order=3, method='central', h=0.01)
    assert abs(result - 24) < 1e-3, f"Third derivative should be ~24, got {result}"
    
    # Fourth derivative at x=1 (should be 24) - use larger h for stability
    result = approximate_derivative(f, 1, order=4, method='central', h=0.01)
    assert abs(result - 24) < 1e-2, f"Fourth derivative should be ~24, got {result}"
    
    # Test forward method
    result = approximate_derivative(f, 1, order=1, method='forward')
    assert abs(result - 4) < 1e-3, f"Forward derivative should be ~4, got {result}"
    
    # Test error cases
    try:
        approximate_derivative(f, 1, order=5)
        assert False, "Should raise ValueError for invalid order"
    except ValueError:
        pass
    
    print("  ✓ All approximate_derivative tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Numerical Methods Utils Test Suite")
    print("=" * 60)
    print()
    
    # Root finding tests
    test_bisection()
    test_newton_raphson()
    test_secant_method()
    test_brent_method()
    
    # Integration tests
    test_trapezoidal_rule()
    test_simpsons_rule()
    test_adaptive_simpson()
    test_gaussian_quadrature()
    
    # Differentiation tests
    test_forward_difference()
    test_backward_difference()
    test_central_difference()
    test_second_derivative()
    test_richardson_extrapolation()
    
    # Interpolation tests
    test_linear_interpolation()
    test_lagrange_interpolation()
    test_newton_interpolation()
    test_cubic_spline_interpolation()
    
    # Optimization tests
    test_golden_section_search()
    test_gradient_descent_1d()
    test_nelder_mead_1d()
    
    # Utility tests
    test_approximate_derivative()
    
    print()
    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()