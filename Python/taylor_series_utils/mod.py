"""
AllToolkit - Taylor Series Utilities

A comprehensive Taylor series expansion library for function approximation,
series generation, and error analysis. Zero external dependencies - pure 
Python standard library implementation.

Taylor series: f(x) = Σ f^(n)(a) / n! * (x - a)^n

Author: AllToolkit
License: MIT
"""

import math
from typing import List, Tuple, Callable, Optional, Dict, Any
from dataclasses import dataclass


# =============================================================================
# Type Aliases
# =============================================================================

ScalarFunction = Callable[[float], float]
SeriesCoefficients = List[float]


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class TaylorSeriesResult:
    """Result of Taylor series expansion."""
    center: float
    coefficients: List[float]
    order: int
    series_expression: str
    remainder_estimate: float


@dataclass
class ApproximationResult:
    """Result of Taylor series approximation."""
    exact_value: float
    approximate_value: float
    error: float
    relative_error: float
    terms_used: int


# =============================================================================
# Derivative Utilities
# =============================================================================

def numerical_derivative(
    f: ScalarFunction,
    x: float,
    order: int = 1,
    h: float = 1e-5
) -> float:
    """
    Compute numerical derivative of any order using central differences.
    
    Supports orders 1-10 using finite difference formulas.
    
    Args:
        f: Function to differentiate
        x: Point at which to compute derivative
        order: Order of derivative (1-10)
        h: Step size for finite difference
    
    Returns:
        Approximate derivative value
    
    Examples:
        >>> numerical_derivative(lambda x: x**3, 2, order=1)
        12.0
        >>> numerical_derivative(lambda x: x**3, 2, order=2)
        12.0
    """
    # Central difference coefficients for various orders
    # These are derived from Taylor series expansions
    if order == 1:
        return (f(x + h) - f(x - h)) / (2 * h)
    elif order == 2:
        return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)
    elif order == 3:
        return (f(x + 2*h) - 2*f(x + h) + 2*f(x - h) - f(x - 2*h)) / (2 * h ** 3)
    elif order == 4:
        return (f(x + 2*h) - 4*f(x + h) + 6*f(x) - 4*f(x - h) + f(x - 2*h)) / (h ** 4)
    elif order == 5:
        return (f(x + 3*h) - 4*f(x + 2*h) + 5*f(x + h) - 5*f(x - h) + 4*f(x - 2*h) - f(x - 3*h)) / (2 * h ** 5)
    elif order == 6:
        return (f(x + 3*h) - 6*f(x + 2*h) + 15*f(x + h) - 20*f(x) + 15*f(x - h) - 6*f(x - 2*h) + f(x - 3*h)) / (h ** 6)
    elif order == 7:
        return (f(x + 4*h) - 8*f(x + 3*h) + 13*f(x + 2*h) - 4*f(x + h) + 4*f(x - h) - 13*f(x - 2*h) + 8*f(x - 3*h) - f(x - 4*h)) / (2 * h ** 7)
    elif order == 8:
        return (f(x + 4*h) - 8*f(x + 3*h) + 28*f(x + 2*h) - 56*f(x + h) + 70*f(x) - 56*f(x - h) + 28*f(x - 2*h) - 8*f(x - 3*h) + f(x - 4*h)) / (h ** 8)
    elif order == 9:
        return (f(x + 5*h) - 12*f(x + 4*h) + 22*f(x + 3*h) - 8*f(x + 2*h) + 6*f(x + h) - 6*f(x - h) + 8*f(x - 2*h) - 22*f(x - 3*h) + 12*f(x - 4*h) - f(x - 5*h)) / (2 * h ** 9)
    elif order == 10:
        return (f(x + 5*h) - 10*f(x + 4*h) + 45*f(x + 3*h) - 120*f(x + 2*h) + 210*f(x + h) - 252*f(x) + 210*f(x - h) - 120*f(x - 2*h) + 45*f(x - 3*h) - 10*f(x - 4*h) + f(x - 5*h)) / (h ** 10)
    else:
        raise ValueError(f"Derivative order {order} not supported (1-10 only)")


def factorial(n: int) -> int:
    """
    Compute factorial of n.
    
    Args:
        n: Non-negative integer
    
    Returns:
        n! = n * (n-1) * ... * 1
    
    Raises:
        ValueError: If n is negative
    
    Examples:
        >>> factorial(5)
        120
        >>> factorial(0)
        1
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# =============================================================================
# Taylor Series Computation
# =============================================================================

def compute_taylor_coefficients(
    f: ScalarFunction,
    center: float,
    order: int,
    h: float = 1e-5
) -> SeriesCoefficients:
    """
    Compute Taylor series coefficients for a function at a given center.
    
    Coefficient formula: c_n = f^(n)(a) / n!
    
    Args:
        f: Function to expand
        center: Center point (a) for the expansion
        order: Maximum order of the series
        h: Step size for numerical differentiation
    
    Returns:
        List of Taylor coefficients [c0, c1, c2, ..., c_order]
    
    Examples:
        >>> coeffs = compute_taylor_coefficients(lambda x: math.exp(x), 0, 3)
        >>> coeffs  # All coefficients for exp(x) at x=0 are 1/n!
        [1.0, 1.0, 0.5, 0.166666...]
    """
    coefficients = []
    for n in range(order + 1):
        if n == 0:
            derivative = f(center)
        else:
            derivative = numerical_derivative(f, center, order=n, h=h)
        coefficient = derivative / factorial(n)
        coefficients.append(coefficient)
    return coefficients


def taylor_series_expand(
    f: ScalarFunction,
    center: float,
    order: int,
    h: float = 1e-5,
    variable: str = 'x'
) -> TaylorSeriesResult:
    """
    Compute complete Taylor series expansion for a function.
    
    Args:
        f: Function to expand
        center: Center point for expansion
        order: Maximum order of the series
        h: Step size for numerical differentiation
        variable: Variable name for expression string
    
    Returns:
        TaylorSeriesResult with coefficients, expression, and error estimate
    
    Examples:
        >>> result = taylor_series_expand(lambda x: math.sin(x), 0, 4)
        >>> result.series_expression
        'f(x) ≈ 1.0 + 1.0*(x - 0)^1 - 0.5*(x - 0)^2 + ...'
    """
    coefficients = compute_taylor_coefficients(f, center, order, h)
    
    # Build series expression string
    terms = []
    for n, coef in enumerate(coefficients):
        if abs(coef) < 1e-10:
            continue
        
        sign = '+' if coef >= 0 else '-'
        abs_coef = abs(coef)
        
        if n == 0:
            terms.append(f"{coef:.6g}")
        elif n == 1:
            if center == 0:
                terms.append(f"{sign} {abs_coef:.6g}*{variable}")
            else:
                terms.append(f"{sign} {abs_coef:.6g}*({variable} - {center:.6g})")
        else:
            if center == 0:
                terms.append(f"{sign} {abs_coef:.6g}*{variable}^{n}")
            else:
                terms.append(f"{sign} {abs_coef:.6g}*({variable} - {center:.6g})^{n}")
    
    series_expression = f"f({variable}) ≈ " + " ".join(terms) if terms else "f(x) ≈ 0"
    
    # Estimate remainder (Lagrange form)
    # R_n(x) ≈ |f^(n+1)(center)| / (n+1)! * |x - center|^(n+1)
    try:
        next_derivative = numerical_derivative(f, center, order=order + 1, h=h)
        remainder_estimate = abs(next_derivative) / factorial(order + 1)
    except ValueError:
        remainder_estimate = 0.0
    
    return TaylorSeriesResult(
        center=center,
        coefficients=coefficients,
        order=order,
        series_expression=series_expression,
        remainder_estimate=remainder_estimate
    )


def evaluate_taylor_series(
    coefficients: SeriesCoefficients,
    center: float,
    x: float,
    max_terms: Optional[int] = None
) -> float:
    """
    Evaluate Taylor series at a given point.
    
    Formula: Σ c_n * (x - center)^n
    
    Args:
        coefficients: Taylor series coefficients
        center: Center point of the series
        x: Point at which to evaluate
        max_terms: Maximum number of terms to use (default: all)
    
    Returns:
        Approximate value of the series at x
    
    Examples:
        >>> coeffs = [1, 1, 0.5, 1/6]  # exp(x) at x=0, order 3
        >>> evaluate_taylor_series(coeffs, 0, 1)  # exp(1) ≈ e
        2.6666...
    """
    if max_terms is None:
        max_terms = len(coefficients)
    else:
        max_terms = min(max_terms, len(coefficients))
    
    result = 0.0
    dx = x - center
    dx_power = 1.0
    
    for n in range(max_terms):
        result += coefficients[n] * dx_power
        dx_power *= dx
    
    return result


# =============================================================================
# Pre-defined Taylor Series for Common Functions
# =============================================================================

# Taylor series coefficients for common functions centered at 0
COMMON_SERIES = {
    'sin': {
        'center': 0,
        'coefficients': lambda n: [
            0 if k % 2 == 0 else (-1)**((k-1)//2) / factorial(k)
            for k in range(n + 1)
        ],
        'pattern': 'Odd powers alternating: x - x³/3! + x⁵/5! - ...',
        'exact': lambda x: math.sin(x)
    },
    'cos': {
        'center': 0,
        'coefficients': lambda n: [
            (-1)**(k//2) / factorial(k) if k % 2 == 0 else 0
            for k in range(n + 1)
        ],
        'pattern': 'Even powers alternating: 1 - x²/2! + x⁴/4! - ...',
        'exact': lambda x: math.cos(x)
    },
    'exp': {
        'center': 0,
        'coefficients': lambda n: [1 / factorial(k) for k in range(n + 1)],
        'pattern': 'All powers: 1 + x + x²/2! + x³/3! + ...',
        'exact': lambda x: math.exp(x)
    },
    'ln': {
        'center': 1,
        'coefficients': lambda n: [
            0 if k == 0 else (-1)**(k-1) / k
            for k in range(n + 1)
        ],
        'pattern': 'ln(1+x) = x - x²/2 + x³/3 - ... (valid for |x| < 1)',
        'exact': lambda x: math.log(x)
    },
    'arctan': {
        'center': 0,
        'coefficients': lambda n: [
            0 if k % 2 == 0 else (-1)**((k-1)//2) / k
            for k in range(n + 1)
        ],
        'pattern': 'Odd powers alternating: x - x³/3 + x⁵/5 - ...',
        'exact': lambda x: math.atan(x)
    },
    'sqrt': {
        'center': 1,
        'coefficients': lambda n: [
            math.factorial(2*k) / (math.factorial(k)**2 * (1 - 2*k) * 4**k)
            if k > 0 else 1
            for k in range(min(n + 1, 20))  # Limit for convergence
        ],
        'pattern': '√(1+x) = 1 + x/2 - x²/8 + ... (valid for |x| < 1)',
        'exact': lambda x: math.sqrt(x)
    },
    'sinh': {
        'center': 0,
        'coefficients': lambda n: [
            0 if k % 2 == 0 else 1 / factorial(k)
            for k in range(n + 1)
        ],
        'pattern': 'Odd powers: x + x³/3! + x⁵/5! + ...',
        'exact': lambda x: math.sinh(x)
    },
    'cosh': {
        'center': 0,
        'coefficients': lambda n: [
            1 / factorial(k) if k % 2 == 0 else 0
            for k in range(n + 1)
        ],
        'pattern': 'Even powers: 1 + x²/2! + x⁴/4! + ...',
        'exact': lambda x: math.cosh(x)
    },
    'arcsin': {
        'center': 0,
        'coefficients': lambda n: [
            0 if k % 2 == 0 else (
                factorial(k) / (factorial((k-1)//2)**2 * k * 2**(k-1))
                if k > 0 else 0
            )
            for k in range(min(n + 1, 15))
        ],
        'pattern': 'arcsin(x) = x + x³/6 + 3x⁵/40 + ... (valid for |x| < 1)',
        'exact': lambda x: math.asin(x) if abs(x) <= 1 else float('nan')
    },
}


def get_series_coefficients(
    function_name: str,
    order: int
) -> Tuple[SeriesCoefficients, float]:
    """
    Get pre-computed Taylor series coefficients for common functions.
    
    Args:
        function_name: Name of the function ('sin', 'cos', 'exp', 'ln', etc.)
        order: Maximum order of the series
    
    Returns:
        Tuple of (coefficients, center point)
    
    Raises:
        ValueError: If function name is not recognized
    
    Examples:
        >>> coeffs, center = get_series_coefficients('sin', 5)
        >>> center
        0
        >>> coeffs[1]  # First non-zero term
        1.0
    """
    if function_name not in COMMON_SERIES:
        raise ValueError(
            f"Unknown function '{function_name}'. "
            f"Available: {list(COMMON_SERIES.keys())}"
        )
    
    series_info = COMMON_SERIES[function_name]
    coefficients = series_info['coefficients'](order)
    center = series_info['center']
    
    return coefficients, center


def approximate_with_series(
    function_name: str,
    x: float,
    order: int
) -> ApproximationResult:
    """
    Approximate a function value using its Taylor series.
    
    Args:
        function_name: Name of the function
        x: Point at which to approximate
        order: Order of the Taylor series
    
    Returns:
        ApproximationResult with exact and approximate values
    
    Examples:
        >>> result = approximate_with_series('sin', 0.5, 5)
        >>> abs(result.error) < 0.001
        True
    """
    coefficients, center = get_series_coefficients(function_name, order)
    exact_func = COMMON_SERIES[function_name]['exact']
    
    exact_value = exact_func(x)
    approximate_value = evaluate_taylor_series(coefficients, center, x)
    
    error = abs(exact_value - approximate_value)
    relative_error = error / abs(exact_value) if abs(exact_value) > 1e-10 else error
    
    return ApproximationResult(
        exact_value=exact_value,
        approximate_value=approximate_value,
        error=error,
        relative_error=relative_error,
        terms_used=order + 1
    )


# =============================================================================
# Error Analysis
# =============================================================================

def remainder_estimate_lagrange(
    f: ScalarFunction,
    center: float,
    x: float,
    order: int,
    h: float = 1e-4
) -> float:
    """
    Estimate remainder using Lagrange form of Taylor remainder.
    
    R_n(x) = f^(n+1)(ξ) / (n+1)! * (x - a)^(n+1)
    
    Upper bound: |R_n(x)| ≤ M / (n+1)! * |x - a|^(n+1)
    where M = max|f^(n+1)(t)| for t in [a, x]
    
    Args:
        f: Original function
        center: Taylor series center
        x: Evaluation point
        order: Order of the series
        h: Step size for numerical differentiation
    
    Returns:
        Estimated remainder bound
    
    Examples:
        >>> estimate = remainder_estimate_lagrange(
        ...     lambda x: math.sin(x), 0, 0.5, 3
        ... )
        >>> estimate > 0
        True
    """
    dx = abs(x - center)
    
    # Estimate maximum derivative in interval
    # Use endpoints and midpoint
    test_points = [center, x, (center + x) / 2]
    
    max_derivative = 0.0
    for t in test_points:
        try:
            derivative = abs(numerical_derivative(f, t, order=order + 1, h=h))
            max_derivative = max(max_derivative, derivative)
        except ValueError:
            max_derivative = max(max_derivative, 1.0)  # Conservative estimate
    
    remainder = max_derivative / factorial(order + 1) * dx ** (order + 1)
    return remainder


def find_required_order(
    function_name: str,
    x: float,
    tolerance: float = 1e-6,
    max_order: int = 50
) -> Tuple[int, ApproximationResult]:
    """
    Find the minimum order needed to achieve desired accuracy.
    
    Args:
        function_name: Name of the function
        x: Point at which to approximate
        tolerance: Desired error tolerance
        max_order: Maximum order to try
    
    Returns:
        Tuple of (required order, approximation result at that order)
    
    Examples:
        >>> order, result = find_required_order('sin', 0.5, tolerance=1e-10)
        >>> result.error < 1e-10
        True
    """
    for order in range(1, max_order + 1):
        result = approximate_with_series(function_name, x, order)
        if result.error < tolerance:
            return order, result
    
    # If max_order doesn't achieve tolerance
    result = approximate_with_series(function_name, x, max_order)
    return max_order, result


def convergence_analysis(
    function_name: str,
    x: float,
    max_order: int = 20
) -> List[Tuple[int, float, float]]:
    """
    Analyze convergence of Taylor series approximation.
    
    Args:
        function_name: Name of the function
        x: Point at which to analyze
        max_order: Maximum order to analyze
    
    Returns:
        List of (order, error, relative_error) tuples
    
    Examples:
        >>> data = convergence_analysis('sin', 0.5, 5)
        >>> len(data)
        5
    """
    results = []
    for order in range(1, max_order + 1):
        result = approximate_with_series(function_name, x, order)
        results.append((order, result.error, result.relative_error))
    return results


# =============================================================================
# Series Manipulation
# =============================================================================

def series_addition(
    coeffs1: SeriesCoefficients,
    coeffs2: SeriesCoefficients
) -> SeriesCoefficients:
    """
    Add two Taylor series (same center).
    
    (f + g)(x) has coefficients c_n = a_n + b_n
    
    Args:
        coeffs1: Coefficients of first series
        coeffs2: Coefficients of second series
    
    Returns:
        Coefficients of the sum
    
    Examples:
        >>> c1 = [1, 1, 0.5]  # exp(x) up to order 2
        >>> c2 = [1, 0, -0.5]  # cos(x) up to order 2
        >>> series_addition(c1, c2)
        [2, 1, 0.0]
    """
    max_len = max(len(coeffs1), len(coeffs2))
    result = []
    for i in range(max_len):
        c1 = coeffs1[i] if i < len(coeffs1) else 0
        c2 = coeffs2[i] if i < len(coeffs2) else 0
        result.append(c1 + c2)
    return result


def series_multiplication(
    coeffs1: SeriesCoefficients,
    coeffs2: SeriesCoefficients
) -> SeriesCoefficients:
    """
    Multiply two Taylor series (same center).
    
    (f * g)(x) has coefficients c_n = Σ a_k * b_(n-k)
    
    Args:
        coeffs1: Coefficients of first series
        coeffs2: Coefficients of second series
    
    Returns:
        Coefficients of the product
    
    Examples:
        >>> c1 = [1, 1]  # 1 + x
        >>> c2 = [1, -1]  # 1 - x
        >>> series_multiplication(c1, c2)  # 1 - x²
        [1, 0, -1]
    """
    result_len = len(coeffs1) + len(coeffs2) - 1
    result = [0.0] * result_len
    
    for i, a in enumerate(coeffs1):
        for j, b in enumerate(coeffs2):
            result[i + j] += a * b
    
    return result


def series_derivative(coeffs: SeriesCoefficients) -> SeriesCoefficients:
    """
    Compute derivative of Taylor series.
    
    d/dx Σ c_n x^n = Σ n * c_n x^(n-1) = Σ c'_n x^n
    where c'_n = (n+1) * c_(n+1)
    
    Args:
        coeffs: Original series coefficients
    
    Returns:
        Coefficients of derivative series
    
    Examples:
        >>> coeffs = [1, 1, 0.5, 1/6]  # exp(x)
        >>> series_derivative(coeffs)  # exp'(x) = exp(x)
        [1, 1, 0.5]
    """
    if len(coeffs) <= 1:
        return [0.0]
    
    result = []
    for n in range(len(coeffs) - 1):
        result.append((n + 1) * coeffs[n + 1])
    return result


def series_integral(
    coeffs: SeriesCoefficients,
    constant: float = 0.0
) -> SeriesCoefficients:
    """
    Compute integral of Taylor series.
    
    ∫ Σ c_n x^n dx = Σ c_n / (n+1) x^(n+1) + C
    
    Args:
        coeffs: Original series coefficients
        constant: Integration constant
    
    Returns:
        Coefficients of integral series
    
    Examples:
        >>> coeffs = [1, 1, 0.5]  # exp(x) up to x²
        >>> series_integral(coeffs, constant=0)  # ∫exp(x) ≈ x + x²/2 + x³/6
        [0, 1, 0.5, 0.1666...]
    """
    result = [constant]
    for n, c in enumerate(coeffs):
        result.append(c / (n + 1))
    return result


# =============================================================================
# Utility Functions
# =============================================================================

def format_series_expression(
    coefficients: SeriesCoefficients,
    center: float,
    variable: str = 'x',
    precision: int = 6
) -> str:
    """
    Format Taylor series as a readable mathematical expression.
    
    Args:
        coefficients: Taylor series coefficients
        center: Center point
        variable: Variable name
        precision: Decimal precision
    
    Returns:
        Formatted string expression
    
    Examples:
        >>> coeffs = [1, 1, 0.5, 1/6]
        >>> format_series_expression(coeffs, 0)
        '1 + x + 0.5x² + 0.166667x³'
    """
    terms = []
    for n, coef in enumerate(coefficients):
        if abs(coef) < 1e-10:
            continue
        
        sign = '+' if coef >= 0 else '-'
        abs_coef = abs(coef)
        coef_str = f"{abs_coef:.{precision}g}"
        
        if n == 0:
            terms.append(f"{coef:.{precision}g}")
        elif n == 1:
            if center == 0:
                if abs_coef == 1:
                    terms.append(f"{sign} {variable}")
                else:
                    terms.append(f"{sign} {coef_str}{variable}")
            else:
                terms.append(f"{sign} {coef_str}({variable} - {center:.{precision}g})")
        else:
            if center == 0:
                if abs_coef == 1:
                    terms.append(f"{sign} {variable}^{n}")
                else:
                    terms.append(f"{sign} {coef_str}{variable}^{n}")
            else:
                terms.append(f"{sign} {coef_str}({variable} - {center:.{precision}g})^{n}")
    
    return " ".join(terms) if terms else "0"


def get_series_info(function_name: str) -> Dict[str, Any]:
    """
    Get information about a pre-defined Taylor series.
    
    Args:
        function_name: Name of the function
    
    Returns:
        Dictionary with series information
    
    Raises:
        ValueError: If function name is not recognized
    
    Examples:
        >>> info = get_series_info('sin')
        >>> info['pattern']
        'Odd powers alternating: x - x³/3! + x⁵/5! - ...'
    """
    if function_name not in COMMON_SERIES:
        raise ValueError(f"Unknown function '{function_name}'")
    
    series_info = COMMON_SERIES[function_name]
    return {
        'name': function_name,
        'center': series_info['center'],
        'pattern': series_info['pattern'],
        'convergence_radius': '∞' if function_name in ['sin', 'cos', 'exp', 'sinh', 'cosh'] else 1
    }


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Data classes
    'TaylorSeriesResult',
    'ApproximationResult',
    
    # Core functions
    'compute_taylor_coefficients',
    'taylor_series_expand',
    'evaluate_taylor_series',
    
    # Pre-defined series
    'get_series_coefficients',
    'approximate_with_series',
    'COMMON_SERIES',
    
    # Error analysis
    'remainder_estimate_lagrange',
    'find_required_order',
    'convergence_analysis',
    
    # Series operations
    'series_addition',
    'series_multiplication',
    'series_derivative',
    'series_integral',
    
    # Utilities
    'numerical_derivative',
    'factorial',
    'format_series_expression',
    'get_series_info',
]


# =============================================================================
# Demo
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Taylor Series Utilities Demo")
    print("=" * 60)
    
    # Taylor series expansion
    print("\n--- Taylor Series Expansion ---")
    
    # Compute Taylor series for sin(x) at x=0
    f = lambda x: math.sin(x)
    result = taylor_series_expand(f, center=0, order=6)
    print(f"\nTaylor series for sin(x) at x=0, order 6:")
    print(f"  Expression: {result.series_expression}")
    print(f"  Coefficients: {result.coefficients}")
    
    # Evaluate at x=0.5
    approx = evaluate_taylor_series(result.coefficients, 0, 0.5)
    exact = math.sin(0.5)
    print(f"\n  At x=0.5: approx = {approx:.10f}, exact = {exact:.10f}")
    print(f"  Error: {abs(approx - exact):.10f}")
    
    # Pre-defined series
    print("\n--- Pre-defined Taylor Series ---")
    
    for func_name in ['sin', 'cos', 'exp', 'arctan']:
        info = get_series_info(func_name)
        print(f"\n{func_name}(x):")
        print(f"  Center: {info['center']}")
        print(f"  Pattern: {info['pattern']}")
        print(f"  Convergence radius: {info['convergence_radius']}")
        
        # Approximation
        x = 0.3
        approx_result = approximate_with_series(func_name, x, order=5)
        print(f"  At x={x}: approx = {approx_result.approximate_value:.8f}, "
              f"exact = {approx_result.exact_value:.8f}, "
              f"error = {approx_result.error:.2e}")
    
    # Convergence analysis
    print("\n--- Convergence Analysis ---")
    print("\nConvergence of sin(0.5) approximation:")
    convergence = convergence_analysis('sin', 0.5, max_order=8)
    for order, error, rel_error in convergence:
        print(f"  Order {order}: error = {error:.2e}, relative = {rel_error:.2%}")
    
    # Find required order
    print("\n--- Finding Required Order ---")
    order, result = find_required_order('sin', 0.5, tolerance=1e-10)
    print(f"To achieve 1e-10 accuracy for sin(0.5):")
    print(f"  Required order: {order}")
    print(f"  Error achieved: {result.error:.2e}")
    
    # Series operations
    print("\n--- Series Operations ---")
    
    # sin + cos
    sin_coeffs, _ = get_series_coefficients('sin', 4)
    cos_coeffs, _ = get_series_coefficients('cos', 4)
    sum_coeffs = series_addition(sin_coeffs, cos_coeffs)
    print(f"\nsin(x) + cos(x) coefficients (order 4): {sum_coeffs}")
    print(f"  Expression: {format_series_expression(sum_coeffs, 0)}")
    
    # Derivative of exp
    exp_coeffs, _ = get_series_coefficients('exp', 4)
    deriv_coeffs = series_derivative(exp_coeffs)
    print(f"\nDerivative of exp(x): {deriv_coeffs}")
    print(f"  (Should equal exp(x): {exp_coeffs[:len(deriv_coeffs)]})")
    
    # Integral of 1 + x (which gives x + x²/2)
    coeffs = [1, 1]
    int_coeffs = series_integral(coeffs, constant=0)
    print(f"\nIntegral of 1 + x: {format_series_expression(int_coeffs, 0)}")
    
    # Multiplication
    print("\n--- Series Multiplication ---")
    c1 = [1, 1]  # 1 + x
    c2 = [1, -1]  # 1 - x
    product = series_multiplication(c1, c2)
    print(f"(1 + x)(1 - x) = {format_series_expression(product, 0)}")
    print(f"  Coefficients: {product}")
    
    # Error estimation
    print("\n--- Error Estimation ---")
    f = lambda x: math.exp(x)
    remainder = remainder_estimate_lagrange(f, center=0, x=0.5, order=3)
    print(f"Lagrange remainder estimate for exp(0.5), order 3:")
    print(f"  Estimate: {remainder:.6f}")
    
    actual_error = abs(math.exp(0.5) - evaluate_taylor_series(
        get_series_coefficients('exp', 3)[0], 0, 0.5
    ))
    print(f"  Actual error: {actual_error:.6f}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")