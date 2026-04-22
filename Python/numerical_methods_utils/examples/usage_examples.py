"""
Usage examples for numerical_methods_utils module.

Demonstrates practical applications of root finding, integration,
differentiation, interpolation, and optimization.
"""

import math
from numerical_methods_utils.mod import (
    # Root finding
    bisection, newton_raphson, secant_method, brent_method,
    # Integration
    trapezoidal_rule, simpsons_rule, adaptive_simpson, gaussian_quadrature,
    # Differentiation
    central_difference, second_derivative, richardson_extrapolation,
    # Interpolation
    linear_interpolation, lagrange_interpolation, newton_interpolation,
    cubic_spline_interpolation,
    # Optimization
    golden_section_search, gradient_descent_1d, nelder_mead_1d,
)


def example_root_finding():
    """
    Example: Finding roots of transcendental equations.
    
    Solve the equation: x * cos(x) - 0.5 = 0
    """
    print("=" * 60)
    print("Example: Root Finding")
    print("=" * 60)
    print()
    print("Problem: Find root of f(x) = x·cos(x) - 0.5")
    print()
    
    f = lambda x: x * math.cos(x) - 0.5
    df = lambda x: math.cos(x) - x * math.sin(x)
    
    # Bisection method
    result = bisection(f, 0, 1.5, tol=1e-12)
    print(f"Bisection method:")
    print(f"  Root:        x = {result.root:.12f}")
    print(f"  Iterations:  {result.iterations}")
    print(f"  f(root):     {f(result.root):.12e}")
    print()
    
    # Newton-Raphson method
    result = newton_raphson(f, df, 1.0, tol=1e-12)
    print(f"Newton-Raphson method:")
    print(f"  Root:        x = {result.root:.12f}")
    print(f"  Iterations:  {result.iterations}")
    print(f"  f(root):     {f(result.root):.12e}")
    print()
    
    # Secant method
    result = secant_method(f, 0.5, 1.0, tol=1e-12)
    print(f"Secant method:")
    print(f"  Root:        x = {result.root:.12f}")
    print(f"  Iterations:  {result.iterations}")
    print(f"  f(root):     {f(result.root):.12e}")
    print()
    
    # Brent's method (most robust)
    result = brent_method(f, 0, 1.5, tol=1e-12)
    print(f"Brent's method (recommended):")
    print(f"  Root:        x = {result.root:.12f}")
    print(f"  Iterations:  {result.iterations}")
    print(f"  f(root):     {f(result.root):.12e}")
    print()


def example_integration():
    """
    Example: Calculating the area under a Gaussian curve.
    
    Compute the integral of e^(-x²) from -∞ to ∞ (should be √π ≈ 1.772).
    Approximated from -3 to 3 since the function decays rapidly.
    """
    print("=" * 60)
    print("Example: Gaussian Integration")
    print("=" * 60)
    print()
    print("Problem: Integrate e^(-x²) from -3 to 3 (approximating -∞ to ∞)")
    print(f"Expected value: sqrt(π) = {math.sqrt(math.pi):.10f}")
    print()
    
    f = lambda x: math.exp(-x**2)
    
    # Trapezoidal rule
    result = trapezoidal_rule(f, -3, 3, n=10000)
    print(f"Trapezoidal rule (n=10000):")
    print(f"  Value:  {result.value:.10f}")
    print(f"  Error:  {abs(result.value - math.sqrt(math.pi)):e}")
    print()
    
    # Simpson's rule
    result = simpsons_rule(f, -3, 3, n=1000)
    print(f"Simpson's rule (n=1000):")
    print(f"  Value:  {result.value:.10f}")
    print(f"  Error:  {abs(result.value - math.sqrt(math.pi)):e}")
    print()
    
    # Adaptive Simpson
    result = adaptive_simpson(f, -3, 3, tol=1e-10)
    print(f"Adaptive Simpson:")
    print(f"  Value:  {result.value:.10f}")
    print(f"  Error:  {abs(result.value - math.sqrt(math.pi)):e}")
    print()
    
    # Gaussian quadrature (most accurate for smooth functions)
    result = gaussian_quadrature(f, -3, 3, n=10)
    print(f"Gaussian quadrature (n=10):")
    print(f"  Value:  {result.value:.10f}")
    print(f"  Error:  {abs(result.value - math.sqrt(math.pi)):e}")
    print()


def example_differentiation():
    """
    Example: Computing derivatives for a physics problem.
    
    For position function s(t) = t³ - 6t² + 9t + 1:
    - Compute velocity v(t) = ds/dt
    - Compute acceleration a(t) = dv/dt = d²s/dt²
    """
    print("=" * 60)
    print("Example: Physics - Motion Analysis")
    print("=" * 60)
    print()
    print("Position function: s(t) = t³ - 6t² + 9t + 1")
    print("Velocity: v(t) = 3t² - 12t + 9")
    print("Acceleration: a(t) = 6t - 12")
    print()
    
    s = lambda t: t**3 - 6*t**2 + 9*t + 1
    
    # Compute velocity at t = 2
    v_exact = 3*2**2 - 12*2 + 9
    v_numerical = central_difference(s, 2)
    
    print(f"Velocity at t = 2:")
    print(f"  Exact:      v = {v_exact}")
    print(f"  Numerical:  v = {v_numerical:.6f}")
    print(f"  Error:      {abs(v_numerical - v_exact):.2e}")
    print()
    
    # Compute acceleration at t = 2
    a_exact = 6*2 - 12
    a_numerical = second_derivative(s, 2)
    
    print(f"Acceleration at t = 2:")
    print(f"  Exact:      a = {a_exact}")
    print(f"  Numerical:  a = {a_numerical:.6f}")
    print(f"  Error:      {abs(a_numerical - a_exact):.2e}")
    print()
    
    # Richardson extrapolation (high accuracy)
    v_richardson = richardson_extrapolation(s, 2)
    
    print(f"Richardson extrapolation for velocity:")
    print(f"  Numerical:  v = {v_richardson:.10f}")
    print(f"  Error:      {abs(v_richardson - v_exact):.2e}")
    print()


def example_interpolation():
    """
    Example: Interpolating temperature data.
    
    Given temperature measurements at specific times,
    estimate the temperature at other times.
    """
    print("=" * 60)
    print("Example: Temperature Interpolation")
    print("=" * 60)
    print()
    print("Given hourly temperature measurements:")
    
    # Temperature data (time in hours, temp in °C)
    times = [0, 1, 2, 3, 4, 5, 6]
    temps = [15.0, 14.5, 14.2, 14.8, 16.5, 18.0, 19.5]
    
    print()
    for t, temp in zip(times, temps):
        print(f"  {t:02d}:00 → {temp:.1f}°C")
    print()
    
    # Estimate temperature at 2:30
    target_time = 2.5
    
    print(f"Estimating temperature at {target_time:.1f} hours (2:30):")
    
    # Linear interpolation
    temp_linear = linear_interpolation(times, temps, target_time)
    print(f"  Linear:        {temp_linear:.2f}°C")
    
    # Lagrange interpolation
    temp_lagrange = lagrange_interpolation(times, temps, target_time)
    print(f"  Lagrange:      {temp_lagrange:.2f}°C")
    
    # Newton interpolation
    temp_newton = newton_interpolation(times, temps, target_time)
    print(f"  Newton:        {temp_newton:.2f}°C")
    
    # Cubic spline (smoothest)
    temp_spline = cubic_spline_interpolation(times, temps, target_time)
    print(f"  Cubic spline:  {temp_spline:.2f}°C")
    
    print()


def example_optimization():
    """
    Example: Finding the optimal launch angle.
    
    For projectile motion, find the angle that maximizes range
    on flat ground (should be 45°).
    """
    print("=" * 60)
    print("Example: Projectile Motion Optimization")
    print("=" * 60)
    print()
    print("Finding the angle that maximizes projectile range")
    print("Range R = v₀² · sin(2θ) / g")
    print("Expected maximum at θ = 45°")
    print()
    
    # Range function (normalized, assuming v0²/g = 1)
    # θ is in radians
    def range_function(theta):
        return math.sin(2 * theta)
    
    # Negative of range (we want to minimize to find maximum)
    def neg_range(theta):
        return -range_function(theta)
    
    # Golden section search (0 to π/2)
    result_min = golden_section_search(neg_range, 0, math.pi/2)
    optimal_angle = result_min.root
    
    print(f"Golden section search:")
    print(f"  Optimal angle:  {optimal_angle:.6f} rad = {optimal_angle * 180/math.pi:.2f}°")
    print(f"  Max range:      {range_function(optimal_angle):.6f}")
    print()
    
    # Alternative: directly find maximum
    result_max = golden_section_search(range_function, 0, math.pi/2, find_min=False)
    
    print(f"Finding maximum directly:")
    print(f"  Optimal angle:  {result_max.root:.6f} rad = {result_max.root * 180/math.pi:.2f}°")
    print()


def example_numerical_integration_comparison():
    """
    Example: Comparing integration methods for difficult integrals.
    
    Integrate sqrt(x) from 0 to 1 (exact: 2/3).
    This is challenging because the derivative is unbounded at x=0.
    """
    print("=" * 60)
    print("Example: Comparing Integration Methods")
    print("=" * 60)
    print()
    print("Integral: ∫₀¹ √x dx")
    print("Exact value: 2/3 = 0.666666...")
    print()
    
    f = lambda x: math.sqrt(x)
    exact = 2/3
    
    # Test with different methods and interval counts
    print("Method comparison:")
    print()
    
    # Trapezoidal
    for n in [10, 100, 1000, 10000]:
        result = trapezoidal_rule(f, 0, 1, n=n)
        error = abs(result.value - exact)
        print(f"  Trapezoidal n={n:5d}: value = {result.value:.8f}, error = {error:.2e}")
    
    print()
    
    # Simpson's
    for n in [10, 100, 1000]:
        result = simpsons_rule(f, 0, 1, n=n)
        error = abs(result.value - exact)
        print(f"  Simpson's n={n:5d}: value = {result.value:.8f}, error = {error:.2e}")
    
    print()
    
    # Gaussian quadrature
    for n in [3, 5, 7, 10]:
        result = gaussian_quadrature(f, 0, 1, n=n)
        error = abs(result.value - exact)
        print(f"  Gaussian n={n:2d}: value = {result.value:.8f}, error = {error:.2e}")
    
    print()
    
    # Adaptive Simpson
    for tol in [1e-4, 1e-8, 1e-12]:
        result = adaptive_simpson(f, 0, 1, tol=tol)
        error = abs(result.value - exact)
        print(f"  Adaptive tol={tol:.0e}: value = {result.value:.8f}, error = {error:.2e}")
    
    print()


def example_curve_fitting():
    """
    Example: Using interpolation for curve fitting.
    
    Fit a smooth curve through data points and evaluate at many points.
    """
    print("=" * 60)
    print("Example: Curve Fitting with Cubic Splines")
    print("=" * 60)
    print()
    print("Data points (x, y):")
    
    # Sample data points
    x_data = [0, 1, 2, 3, 4, 5]
    y_data = [0, 0.5, 1.5, 2.5, 4, 6.5]
    
    print()
    for x, y in zip(x_data, y_data):
        print(f"  ({x}, {y})")
    print()
    
    # Generate smooth curve
    print("Smooth curve values (every 0.5 units):")
    print()
    
    print("  x    Linear    Lagrange    Newton    Spline")
    print("  " + "-" * 45)
    
    for x in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]:
        y_linear = linear_interpolation(x_data, y_data, x)
        y_lagrange = lagrange_interpolation(x_data, y_data, x)
        y_newton = newton_interpolation(x_data, y_data, x)
        y_spline = cubic_spline_interpolation(x_data, y_data, x)
        
        print(f"  {x:.1f}  {y_linear:.3f}    {y_lagrange:.3f}     {y_newton:.3f}    {y_spline:.3f}")
    
    print()


def example_minimize_cost():
    """
    Example: Minimizing a cost function.
    
    Find the minimum of a production cost function.
    """
    print("=" * 60)
    print("Example: Cost Function Minimization")
    print("=" * 60)
    print()
    print("Cost function: C(x) = 100/x + 10x + 50")
    print("Find the quantity x that minimizes cost.")
    print()
    
    cost = lambda x: 100/x + 10*x + 50
    d_cost = lambda x: -100/(x**2) + 10
    
    # The analytical solution: derivative = 0 → x = sqrt(10) ≈ 3.16
    analytical_min = math.sqrt(10)
    
    print(f"Analytical minimum: x = sqrt(10) = {analytical_min:.6f}")
    print(f"Minimum cost: C({analytical_min:.2f}) = {cost(analytical_min):.2f}")
    print()
    
    # Golden section search
    result = golden_section_search(cost, 1, 10)
    print(f"Golden section search:")
    print(f"  Optimal x:  {result.root:.6f}")
    print(f"  Cost:       {cost(result.root):.2f}")
    print()
    
    # Gradient descent
    result = gradient_descent_1d(d_cost, 5.0, lr=0.1)
    print(f"Gradient descent:")
    print(f"  Optimal x:  {result.root:.6f}")
    print(f"  Cost:       {cost(result.root):.2f}")
    print()
    
    # Nelder-Mead
    result = nelder_mead_1d(cost, 5.0)
    print(f"Nelder-Mead:")
    print(f"  Optimal x:  {result.root:.6f}")
    print(f"  Cost:       {cost(result.root):.2f}")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Numerical Methods Utils - Usage Examples")
    print("=" * 60 + "\n")
    
    example_root_finding()
    example_integration()
    example_differentiation()
    example_interpolation()
    example_optimization()
    example_numerical_integration_comparison()
    example_curve_fitting()
    example_minimize_cost()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()