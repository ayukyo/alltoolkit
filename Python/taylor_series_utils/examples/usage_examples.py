"""
AllToolkit - Taylor Series Utilities Usage Examples

Practical examples demonstrating Taylor series expansion,
approximation, and error analysis for real-world applications.

Author: AllToolkit
License: MIT
"""

import math
import sys
sys.path.insert(0, '..')

from mod import (
    taylor_series_expand,
    evaluate_taylor_series,
    get_series_coefficients,
    approximate_with_series,
    find_required_order,
    convergence_analysis,
    remainder_estimate_lagrange,
    series_addition,
    series_multiplication,
    series_derivative,
    series_integral,
    format_series_expression,
    get_series_info,
    compute_taylor_coefficients,
)


def example_1_basic_approximation():
    """
    Example 1: Basic Taylor Series Approximation
    
    Approximate sin(0.5) using Taylor series and compare with exact value.
    """
    print("=" * 60)
    print("Example 1: Basic Taylor Series Approximation")
    print("=" * 60)
    
    # Get Taylor series for sin(x) centered at 0
    coeffs, center = get_series_coefficients('sin', order=6)
    
    print(f"\nTaylor series for sin(x) at x=0:")
    print(f"  Center: {center}")
    print(f"  Coefficients: {coeffs}")
    print(f"  Expression: {format_series_expression(coeffs, center)}")
    
    # Evaluate at different points
    x_values = [0.1, 0.3, 0.5, 1.0]
    
    print("\nApproximations:")
    for x in x_values:
        approx = evaluate_taylor_series(coeffs, center, x)
        exact = math.sin(x)
        error = abs(approx - exact)
        print(f"  sin({x}) ≈ {approx:.8f}, exact = {exact:.8f}, error = {error:.2e}")
    
    # Show convergence
    print("\nConvergence analysis for sin(0.5):")
    convergence = convergence_analysis('sin', 0.5, max_order=8)
    for order, error, rel_error in convergence:
        print(f"  Order {order}: error = {error:.10f}")


def example_2_custom_function_expansion():
    """
    Example 2: Taylor Expansion for Custom Function
    
    Compute Taylor series for a custom function: f(x) = x² + sin(x)
    """
    print("\n" + "=" * 60)
    print("Example 2: Custom Function Taylor Expansion")
    print("=" * 60)
    
    # Define custom function: f(x) = x² + sin(x)
    custom_func = lambda x: x**2 + math.sin(x)
    
    # Compute Taylor series at center x=0
    result = taylor_series_expand(custom_func, center=0, order=5)
    
    print(f"\nTaylor series for f(x) = x² + sin(x) at x=0:")
    print(f"  Expression: {result.series_expression}")
    print(f"  Coefficients: {result.coefficients}")
    print(f"  Remainder estimate: {result.remainder_estimate:.6f}")
    
    # Evaluate at x=0.5
    x = 0.5
    approx = evaluate_taylor_series(result.coefficients, 0, x)
    exact = custom_func(x)
    
    print(f"\nAt x={x}:")
    print(f"  Approximate: {approx:.8f}")
    print(f"  Exact: {exact:.8f}")
    print(f"  Error: {abs(approx - exact):.2e}")
    
    # Try different center
    print("\n--- Expansion at different center ---")
    result2 = taylor_series_expand(custom_func, center=1, order=4)
    print(f"Taylor series at x=1:")
    print(f"  Expression: {result2.series_expression}")
    
    # Compare accuracy for x near 1
    approx2 = evaluate_taylor_series(result2.coefficients, 1, 1.2)
    exact2 = custom_func(1.2)
    print(f"  At x=1.2: approx = {approx2:.6f}, exact = {exact2:.6f}")


def example_3_accuracy_analysis():
    """
    Example 3: Finding Required Accuracy
    
    Determine minimum order needed for desired precision.
    """
    print("\n" + "=" * 60)
    print("Example 3: Accuracy Analysis - Finding Required Order")
    print("=" * 60)
    
    # Different functions and tolerances
    functions = ['sin', 'cos', 'exp']
    tolerances = [1e-4, 1e-6, 1e-8, 1e-10]
    x = 0.5
    
    print(f"\nFinding minimum order to achieve tolerance for x={x}:")
    print()
    
    for func in functions:
        print(f"{func}(x):")
        for tol in tolerances:
            order, result = find_required_order(func, x, tolerance=tol)
            print(f"  Tolerance {tol:.0e}: order {order}, "
                  f"actual error = {result.error:.2e}")


def example_4_error_estimation():
    """
    Example 4: Lagrange Remainder Estimation
    
    Estimate error using Lagrange form of remainder.
    """
    print("\n" + "=" * 60)
    print("Example 4: Lagrange Remainder Estimation")
    print("=" * 60)
    
    # Estimate error for exp(x) approximation
    f = lambda x: math.exp(x)
    
    print("\nLagrange remainder estimate for exp(x):")
    
    orders = [2, 3, 4, 5]
    x = 0.5
    
    for order in orders:
        # Get actual error
        coeffs, center = get_series_coefficients('exp', order)
        approx = evaluate_taylor_series(coeffs, center, x)
        exact = math.exp(x)
        actual_error = abs(approx - exact)
        
        # Get Lagrange estimate
        lagrange_estimate = remainder_estimate_lagrange(f, center, x, order)
        
        print(f"\n  Order {order}:")
        print(f"    Actual error: {actual_error:.10f}")
        print(f"    Lagrange estimate: {lagrange_estimate:.10f}")
        print(f"    Ratio (estimate/actual): {lagrange_estimate/actual_error:.2f}")


def example_5_series_operations():
    """
    Example 5: Series Arithmetic Operations
    
    Add, multiply, differentiate, and integrate Taylor series.
    """
    print("\n" + "=" * 60)
    print("Example 5: Series Arithmetic Operations")
    print("=" * 60)
    
    # Get series for sin and cos
    sin_coeffs, _ = get_series_coefficients('sin', 4)
    cos_coeffs, _ = get_series_coefficients('cos', 4)
    
    print("\n--- Addition ---")
    print(f"sin(x) coeffs: {sin_coeffs[:5]}")
    print(f"cos(x) coeffs: {cos_coeffs[:5]}")
    
    # sin(x) + cos(x)
    sum_coeffs = series_addition(sin_coeffs, cos_coeffs)
    print(f"sin + cos coeffs: {sum_coeffs}")
    print(f"  Expression: {format_series_expression(sum_coeffs, 0)}")
    
    # Verify: at x=0.3
    x = 0.3
    sum_approx = evaluate_taylor_series(sum_coeffs, 0, x)
    sum_exact = math.sin(x) + math.cos(x)
    print(f"  At x={x}: approx = {sum_approx:.6f}, exact = {sum_exact:.6f}")
    
    print("\n--- Multiplication ---")
    # sin(x) * cos(x) = sin(2x)/2
    product_coeffs = series_multiplication(sin_coeffs, cos_coeffs)
    print(f"sin * cos coeffs: {product_coeffs}")
    print(f"  Expression: {format_series_expression(product_coeffs[:6], 0)}")
    
    # Verify
    product_approx = evaluate_taylor_series(product_coeffs, 0, x)
    product_exact = math.sin(x) * math.cos(x)
    print(f"  At x={x}: approx = {product_approx:.6f}, exact = {product_exact:.6f}")
    
    print("\n--- Derivative ---")
    # Derivative of sin is cos
    sin_deriv = series_derivative(sin_coeffs)
    print(f"sin'(x) coeffs: {sin_deriv}")
    print(f"cos(x) coeffs: {cos_coeffs[:len(sin_deriv)]}")
    print("  Note: sin'(x) = cos(x) matches!")
    
    print("\n--- Integral ---")
    # Integral of cos is sin
    cos_integral = series_integral(cos_coeffs, constant=0)
    print(f"∫cos(x) dx coeffs: {cos_integral}")
    print(f"sin(x) coeffs: {sin_coeffs}")
    print("  Note: ∫cos(x) dx = sin(x) matches!")


def example_6_exp_and_ln():
    """
    Example 6: Exponential and Logarithm Series
    
    Taylor series for exp and ln with practical applications.
    """
    print("\n" + "=" * 60)
    print("Example 6: Exponential and Logarithm Series")
    print("=" * 60)
    
    # Exp series
    print("\n--- Exponential Series ---")
    exp_coeffs, exp_center = get_series_coefficients('exp', 10)
    exp_info = get_series_info('exp')
    
    print(f"exp(x) Taylor series:")
    print(f"  Center: {exp_center}")
    print(f"  Pattern: {exp_info['pattern']}")
    print(f"  Convergence radius: {exp_info['convergence_radius']}")
    
    # Approximate e (exp(1))
    approx_e = evaluate_taylor_series(exp_coeffs, 0, 1)
    print(f"\nApproximating e = exp(1):")
    print(f"  Taylor approximation: {approx_e:.10f}")
    print(f"  Actual e: {math.e:.10f}")
    print(f"  Error: {abs(approx_e - math.e):.2e}")
    
    # Ln series (centered at 1)
    print("\n--- Natural Logarithm Series ---")
    ln_coeffs, ln_center = get_series_coefficients('ln', 10)
    ln_info = get_series_info('ln')
    
    print(f"ln(x) Taylor series:")
    print(f"  Center: {ln_center}")
    print(f"  Pattern: {ln_info['pattern']}")
    
    # ln(1 + x) series converges for |x| < 1
    print("\nApproximating ln values:")
    for x in [1.1, 1.2, 1.5]:
        # For ln(1 + dx), we use ln centered at 1
        dx = x - 1
        approx = evaluate_taylor_series(ln_coeffs, 1, x)
        exact = math.log(x)
        print(f"  ln({x}) ≈ {approx:.6f}, exact = {exact:.6f}, "
              f"error = {abs(approx - exact):.2e}")


def example_7_hyperbolic_functions():
    """
    Example 7: Hyperbolic Functions Series
    
    Taylor series for sinh and cosh.
    """
    print("\n" + "=" * 60)
    print("Example 7: Hyperbolic Functions")
    print("=" * 60)
    
    # sinh series
    sinh_coeffs, sinh_center = get_series_coefficients('sinh', 8)
    sinh_info = get_series_info('sinh')
    
    print(f"\nsinh(x) Taylor series:")
    print(f"  Center: {sinh_center}")
    print(f"  Pattern: {sinh_info['pattern']}")
    print(f"  Expression: {format_series_expression(sinh_coeffs, 0)}")
    
    # cosh series
    cosh_coeffs, cosh_center = get_series_coefficients('cosh', 8)
    cosh_info = get_series_info('cosh')
    
    print(f"\ncosh(x) Taylor series:")
    print(f"  Center: {cosh_center}")
    print(f"  Pattern: {cosh_info['pattern']}")
    print(f"  Expression: {format_series_expression(cosh_coeffs, 0)}")
    
    # Verify identity: cosh² - sinh² = 1
    print("\nVerifying identity: cosh²(x) - sinh²(x) = 1")
    x = 0.5
    cosh_approx = evaluate_taylor_series(cosh_coeffs, 0, x)
    sinh_approx = evaluate_taylor_series(sinh_coeffs, 0, x)
    identity_result = cosh_approx**2 - sinh_approx**2
    print(f"  cosh({x}) ≈ {cosh_approx:.6f}")
    print(f"  sinh({x}) ≈ {sinh_approx:.6f}")
    print(f"  cosh² - sinh² = {identity_result:.6f} (should be 1)")


def example_8_arctan_series():
    """
    Example 8: Arctangent Series
    
    Taylor series for arctan - used in π calculations.
    """
    print("\n" + "=" * 60)
    print("Example 8: Arctangent Series (π Calculation)")
    print("=" * 60)
    
    arctan_coeffs, center = get_series_coefficients('arctan', 20)
    arctan_info = get_series_info('arctan')
    
    print(f"\narctan(x) Taylor series:")
    print(f"  Center: {center}")
    print(f"  Pattern: {arctan_info['pattern']}")
    
    # Historical π calculation: π = 4*arctan(1)
    # arctan(1) = π/4, but convergence is slow
    print("\nHistorical π calculation:")
    print("  π = 4 * arctan(1)")
    print("  Using Taylor series (slow convergence at x=1):")
    
    for order in [10, 50, 100, 200]:
        coeffs, _ = get_series_coefficients('arctan', order)
        arctan1 = evaluate_taylor_series(coeffs, 0, 1)
        pi_approx = 4 * arctan1
        print(f"    Order {order}: π ≈ {pi_approx:.10f}, error = {abs(pi_approx - math.pi):.2e}")
    
    # Better approach: π = 4*arctan(1/2) + 4*arctan(1/3)
    print("\nMore efficient π calculation:")
    print("  π = 4*arctan(1/2) + 4*arctan(1/3)")
    
    coeffs, _ = get_series_coefficients('arctan', 15)
    arctan_half = evaluate_taylor_series(coeffs, 0, 0.5)
    arctan_third = evaluate_taylor_series(coeffs, 0, 1/3)
    pi_approx = 4 * (arctan_half + arctan_third)
    print(f"    Order 15: π ≈ {pi_approx:.10f}, error = {abs(pi_approx - math.pi):.2e}")


def example_9_convergence_radius():
    """
    Example 9: Convergence Radius Analysis
    
    Demonstrate importance of convergence radius.
    """
    print("\n" + "=" * 60)
    print("Example 9: Convergence Radius Analysis")
    print("=" * 60)
    
    print("\nTaylor series only converge within their radius of convergence:")
    
    # ln series converges for |x-1| < 1
    print("\n--- ln(x) series (centered at 1) ---")
    print("  Convergence radius: 1 (valid for x in (0, 2))")
    
    ln_coeffs, ln_center = get_series_coefficients('ln', 20)
    
    test_x = [0.5, 1.5, 0.1, 1.9, 2.5]
    
    print("\n  Testing different x values:")
    for x in test_x:
        if x > 0:  # ln defined for positive x
            approx = evaluate_taylor_series(ln_coeffs, 1, x)
            exact = math.log(x)
            error = abs(approx - exact)
            within_radius = abs(x - 1) < 1
            status = "✓ converges" if within_radius else "✗ outside radius"
            print(f"    ln({x}) = {approx:.4f} vs {exact:.4f}, "
                  f"error = {error:.2e} [{status}]")
    
    # sin series converges everywhere
    print("\n--- sin(x) series (centered at 0) ---")
    print("  Convergence radius: ∞ (converges everywhere)")
    
    sin_coeffs, _ = get_series_coefficients('sin', 10)
    
    test_x = [0.5, 2, 5, 10]
    print("\n  Testing different x values:")
    for x in test_x:
        approx = evaluate_taylor_series(sin_coeffs, 0, x)
        exact = math.sin(x)
        error = abs(approx - exact)
        print(f"    sin({x}) = {approx:.4f} vs {exact:.4f}, error = {error:.2e}")


def example_10_practical_calculator():
    """
    Example 10: Practical Calculator Application
    
    Use Taylor series to compute trigonometric values without math library.
    """
    print("\n" + "=" * 60)
    print("Example 10: Practical Taylor Series Calculator")
    print("=" * 60)
    
    def taylor_sin(x, order=10):
        """Compute sin using Taylor series."""
        coeffs, center = get_series_coefficients('sin', order)
        return evaluate_taylor_series(coeffs, center, x)
    
    def taylor_cos(x, order=10):
        """Compute cos using Taylor series."""
        coeffs, center = get_series_coefficients('cos', order)
        return evaluate_taylor_series(coeffs, center, x)
    
    def taylor_exp(x, order=15):
        """Compute exp using Taylor series."""
        coeffs, center = get_series_coefficients('exp', order)
        return evaluate_taylor_series(coeffs, center, x)
    
    print("\nTaylor series calculator:")
    print("  (Computing values without using math.sin/cos/exp)")
    
    # Angles in radians
    angles = [0, math.pi/6, math.pi/4, math.pi/3, math.pi/2]
    
    print("\n  Trigonometric values:")
    print(f"    {'Angle':^10} {'sin':^12} {'Taylor sin':^12} {'cos':^12} {'Taylor cos':^12}")
    
    for angle in angles:
        sin_exact = math.sin(angle)
        sin_taylor = taylor_sin(angle)
        cos_exact = math.cos(angle)
        cos_taylor = taylor_cos(angle)
        
        angle_str = f"{angle:.4f}"
        print(f"    {angle_str:^10} {sin_exact:^12.6f} {sin_taylor:^12.6f} "
              f"{cos_exact:^12.6f} {cos_taylor:^12.6f}")
    
    # Exponential values
    print("\n  Exponential values:")
    print(f"    {'x':^10} {'exp(x)':^12} {'Taylor exp':^12} {'Error':^12}")
    
    for x in [0, 0.5, 1, 2]:
        exp_exact = math.exp(x)
        exp_taylor = taylor_exp(x)
        error = abs(exp_exact - exp_taylor)
        
        print(f"    {x:^10} {exp_exact:^12.6f} {exp_taylor:^12.6f} {error:^12.2e}")
    
    # Compute e using Taylor series
    print("\n  Computing fundamental constants:")
    e_approx = taylor_exp(1, order=20)
    print(f"    e ≈ {e_approx:.10f} (using Taylor, order 20)")
    print(f"    Actual e = {math.e:.10f}")


def main():
    """Run all examples."""
    example_1_basic_approximation()
    example_2_custom_function_expansion()
    example_3_accuracy_analysis()
    example_4_error_estimation()
    example_5_series_operations()
    example_6_exp_and_ln()
    example_7_hyperbolic_functions()
    example_8_arctan_series()
    example_9_convergence_radius()
    example_10_practical_calculator()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()