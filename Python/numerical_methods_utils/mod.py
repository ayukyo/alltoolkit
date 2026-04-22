"""
AllToolkit - Python Numerical Methods Utilities

A comprehensive numerical methods library providing root finding, 
numerical integration, differentiation, interpolation, and optimization.
Zero external dependencies - pure Python standard library implementation.

Author: AllToolkit
License: MIT
"""

import math
from typing import List, Tuple, Callable, Optional, Union, Any
from dataclasses import dataclass


# =============================================================================
# Type Aliases
# =============================================================================

ScalarFunction = Callable[[float], float]
VectorFunction = Callable[[List[float]], float]
ConvergenceResult = Tuple[bool, float, int, str]


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class RootResult:
    """Result of root finding algorithm."""
    root: float
    iterations: int
    converged: bool
    message: str
    function_value: float


@dataclass
class IntegrationResult:
    """Result of numerical integration."""
    value: float
    error_estimate: float
    intervals: int
    method: str


@dataclass
class InterpolationResult:
    """Result of interpolation."""
    x_values: List[float]
    y_values: List[float]
    coefficients: List[float]
    method: str


# =============================================================================
# Root Finding Algorithms
# =============================================================================

def bisection(
    f: ScalarFunction,
    a: float,
    b: float,
    tol: float = 1e-10,
    max_iter: int = 1000
) -> RootResult:
    """
    Find root of function f in interval [a, b] using bisection method.
    
    The bisection method repeatedly bisects an interval and selects a subinterval
    in which a root must lie. It is guaranteed to converge if f(a) and f(b)
    have opposite signs.
    
    Args:
        f: Function to find root of
        a: Left endpoint of interval
        b: Right endpoint of interval
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        RootResult containing root, iterations, convergence status, and message
    
    Raises:
        ValueError: If f(a) and f(b) have the same sign
    
    Examples:
        >>> # Find sqrt(2) by solving x^2 - 2 = 0
        >>> result = bisection(lambda x: x**2 - 2, 1, 2)
        >>> result.converged
        True
        >>> abs(result.root - math.sqrt(2)) < 1e-9
        True
    """
    fa = f(a)
    fb = f(b)
    
    if fa * fb > 0:
        raise ValueError(
            f"f(a) = {fa} and f(b) = {fb} have the same sign. "
            "Root may not exist in interval, or multiple roots exist."
        )
    
    if abs(fa) < tol:
        return RootResult(a, 0, True, "Root found at left endpoint", fa)
    if abs(fb) < tol:
        return RootResult(b, 0, True, "Root found at right endpoint", fb)
    
    iterations = 0
    c = a
    
    while (b - a) / 2 > tol and iterations < max_iter:
        c = (a + b) / 2
        fc = f(c)
        
        if abs(fc) < tol:
            return RootResult(c, iterations + 1, True, "Converged", fc)
        
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
        
        iterations += 1
    
    converged = (b - a) / 2 <= tol
    message = "Converged" if converged else "Maximum iterations reached"
    
    return RootResult(c, iterations, converged, message, f(c))


def newton_raphson(
    f: ScalarFunction,
    df: ScalarFunction,
    x0: float,
    tol: float = 1e-10,
    max_iter: int = 1000
) -> RootResult:
    """
    Find root of function f using Newton-Raphson method.
    
    Uses the iterative formula: x_{n+1} = x_n - f(x_n) / f'(x_n)
    
    Args:
        f: Function to find root of
        df: Derivative of f
        x0: Initial guess
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        RootResult containing root, iterations, convergence status, and message
    
    Examples:
        >>> # Find sqrt(2) by solving x^2 - 2 = 0
        >>> result = newton_raphson(
        ...     lambda x: x**2 - 2,
        ...     lambda x: 2*x,
        ...     1.5
        ... )
        >>> result.converged
        True
    """
    x = x0
    iterations = 0
    
    for i in range(max_iter):
        fx = f(x)
        
        if abs(fx) < tol:
            return RootResult(x, iterations, True, "Converged", fx)
        
        dfx = df(x)
        
        if abs(dfx) < 1e-15:
            return RootResult(x, iterations, False, "Derivative is zero", fx)
        
        x_new = x - fx / dfx
        
        if abs(x_new - x) < tol:
            return RootResult(x_new, iterations + 1, True, "Converged", f(x_new))
        
        x = x_new
        iterations += 1
    
    return RootResult(x, iterations, False, "Maximum iterations reached", f(x))


def secant_method(
    f: ScalarFunction,
    x0: float,
    x1: float,
    tol: float = 1e-10,
    max_iter: int = 1000
) -> RootResult:
    """
    Find root of function f using the secant method.
    
    A derivative-free method that approximates the derivative using
    finite differences.
    
    Args:
        f: Function to find root of
        x0: First initial guess
        x1: Second initial guess
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        RootResult containing root, iterations, convergence status, and message
    
    Examples:
        >>> result = secant_method(lambda x: x**2 - 2, 1, 2)
        >>> result.converged
        True
    """
    f0 = f(x0)
    f1 = f(x1)
    
    for i in range(max_iter):
        if abs(f1 - f0) < 1e-15:
            return RootResult(x1, i, False, "Function values are too close", f1)
        
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        
        if abs(x2 - x1) < tol:
            return RootResult(x2, i + 1, True, "Converged", f(x2))
        
        x0, x1 = x1, x2
        f0, f1 = f1, f(x2)
    
    return RootResult(x1, max_iter, False, "Maximum iterations reached", f1)


def brent_method(
    f: ScalarFunction,
    a: float,
    b: float,
    tol: float = 1e-10,
    max_iter: int = 1000
) -> RootResult:
    """
    Find root using Brent's method (combines bisection, secant, and inverse quadratic).
    
    Brent's method is a robust root-finding algorithm that combines the 
    reliability of bisection with the speed of secant and inverse quadratic interpolation.
    
    Args:
        f: Function to find root of
        a: Left endpoint of interval
        b: Right endpoint of interval
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        RootResult containing root, iterations, convergence status, and message
    
    Raises:
        ValueError: If f(a) and f(b) have the same sign
    
    Examples:
        >>> result = brent_method(lambda x: x**2 - 2, 1, 2)
        >>> result.converged
        True
    """
    fa = f(a)
    fb = f(b)
    
    if fa * fb > 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    
    if abs(fa) < abs(fb):
        a, b = b, a
        fa, fb = fb, fa
    
    c = a
    fc = fa
    mflag = True
    d = 0.0
    
    for i in range(max_iter):
        if abs(fb) < tol:
            return RootResult(b, i, True, "Converged", fb)
        
        if abs(b - a) < tol:
            return RootResult(b, i, True, "Converged", fb)
        
        # Try inverse quadratic interpolation
        if fa != fc and fb != fc:
            s = (a * fb * fc / ((fa - fb) * (fa - fc)) +
                 b * fa * fc / ((fb - fa) * (fb - fc)) +
                 c * fa * fb / ((fc - fa) * (fc - fb)))
        else:
            # Secant method
            s = b - fb * (b - a) / (fb - fa)
        
        # Conditions for accepting s
        cond1 = not ((3 * a + b) / 4 < s < b or b < s < (3 * a + b) / 4)
        cond2 = mflag and abs(s - b) >= abs(b - c) / 2
        cond3 = not mflag and abs(s - b) >= abs(c - d) / 2
        cond4 = mflag and abs(b - c) < tol
        cond5 = not mflag and abs(c - d) < tol
        
        if cond1 or cond2 or cond3 or cond4 or cond5:
            # Bisection
            s = (a + b) / 2
            mflag = True
        else:
            mflag = False
        
        fs = f(s)
        d = c
        c = b
        fc = fb
        
        if fa * fs < 0:
            b = s
            fb = fs
        else:
            a = s
            fa = fs
        
        if abs(fa) < abs(fb):
            a, b = b, a
            fa, fb = fb, fa
    
    return RootResult(b, max_iter, False, "Maximum iterations reached", fb)


# =============================================================================
# Numerical Integration
# =============================================================================

def trapezoidal_rule(
    f: ScalarFunction,
    a: float,
    b: float,
    n: int = 100
) -> IntegrationResult:
    """
    Numerical integration using the trapezoidal rule.
    
    Approximates the integral of f from a to b using n trapezoids.
    
    Args:
        f: Function to integrate
        a: Lower bound of integration
        b: Upper bound of integration
        n: Number of subintervals
    
    Returns:
        IntegrationResult with approximate value and error estimate
    
    Examples:
        >>> result = trapezoidal_rule(lambda x: x**2, 0, 1)
        >>> abs(result.value - 1/3) < 0.01
        True
    """
    if n < 1:
        raise ValueError("Number of intervals must be at least 1")
    
    h = (b - a) / n
    x = [a + i * h for i in range(n + 1)]
    
    # Trapezoidal formula: h/2 * (f(x0) + 2*f(x1) + ... + 2*f(xn-1) + f(xn))
    result = f(x[0]) + f(x[-1])
    result += 2 * sum(f(x[i]) for i in range(1, n))
    result *= h / 2
    
    # Error estimate using Richardson extrapolation
    result_n2 = trapezoidal_rule_simple(f, a, b, n * 2)
    error_estimate = abs(result - result_n2) / 3
    
    return IntegrationResult(result, error_estimate, n, "trapezoidal")


def trapezoidal_rule_simple(f: ScalarFunction, a: float, b: float, n: int) -> float:
    """Simple trapezoidal rule without error estimate."""
    h = (b - a) / n
    result = (f(a) + f(b)) / 2
    for i in range(1, n):
        result += f(a + i * h)
    return result * h


def simpsons_rule(
    f: ScalarFunction,
    a: float,
    b: float,
    n: int = 100
) -> IntegrationResult:
    """
    Numerical integration using Simpson's rule.
    
    More accurate than trapezoidal rule for smooth functions.
    Requires n to be even.
    
    Args:
        f: Function to integrate
        a: Lower bound of integration
        b: Upper bound of integration
        n: Number of subintervals (must be even)
    
    Returns:
        IntegrationResult with approximate value and error estimate
    
    Raises:
        ValueError: If n is not even
    
    Examples:
        >>> result = simpsons_rule(lambda x: x**2, 0, 1, 10)
        >>> abs(result.value - 1/3) < 1e-10
        True
    """
    if n % 2 != 0:
        raise ValueError("Number of intervals must be even for Simpson's rule")
    
    h = (b - a) / n
    x = [a + i * h for i in range(n + 1)]
    
    # Simpson's formula: h/3 * (f(x0) + 4*f(x1) + 2*f(x2) + 4*f(x3) + ... + f(xn))
    result = f(x[0]) + f(x[-1])
    result += 4 * sum(f(x[i]) for i in range(1, n, 2))  # Odd indices
    result += 2 * sum(f(x[i]) for i in range(2, n, 2))  # Even indices
    result *= h / 3
    
    # Error estimate using Richardson extrapolation
    result_n2 = simpsons_rule_simple(f, a, b, n * 2)
    error_estimate = abs(result - result_n2) / 15
    
    return IntegrationResult(result, error_estimate, n, "simpsons")


def simpsons_rule_simple(f: ScalarFunction, a: float, b: float, n: int) -> float:
    """Simple Simpson's rule without error estimate."""
    h = (b - a) / n
    result = f(a) + f(b)
    for i in range(1, n):
        coef = 4 if i % 2 == 1 else 2
        result += coef * f(a + i * h)
    return result * h / 3


def adaptive_simpson(
    f: ScalarFunction,
    a: float,
    b: float,
    tol: float = 1e-10,
    max_depth: int = 50
) -> IntegrationResult:
    """
    Adaptive Simpson's rule with automatic interval subdivision.
    
    Recursively subdivides intervals where the error estimate is too large.
    
    Args:
        f: Function to integrate
        a: Lower bound of integration
        b: Upper bound of integration
        tol: Tolerance for stopping criterion
        max_depth: Maximum recursion depth
    
    Returns:
        IntegrationResult with approximate value and total intervals
    
    Examples:
        >>> result = adaptive_simpson(lambda x: math.sin(x), 0, math.pi)
        >>> abs(result.value - 2) < 1e-9
        True
    """
    total_intervals = [0]  # Use list to allow modification in nested function
    
    def adaptive_helper(a: float, b: float, fa: float, fb: float, fm: float, 
                        whole: float, tol: float, depth: int) -> float:
        m = (a + b) / 2
        lm = (a + m) / 2
        rm = (m + b) / 2
        
        flm = f(lm)
        frm = f(rm)
        
        # Simpson's rule: (h/6) * (fa + 4*fm + fb) where h = b - a
        h = b - a
        left = h / 12 * (fa + 4 * flm + fm)
        right = h / 12 * (fm + 4 * frm + fb)
        delta = left + right - whole
        
        if depth >= max_depth or abs(delta) <= 15 * tol:
            total_intervals[0] += 2
            return left + right + delta / 15
        
        return (adaptive_helper(a, m, fa, fm, flm, left, tol / 2, depth + 1) +
                adaptive_helper(m, b, fm, fb, frm, right, tol / 2, depth + 1))
    
    fa = f(a)
    fb = f(b)
    m = (a + b) / 2
    fm = f(m)
    whole = (b - a) / 6 * (fa + 4 * fm + fb)
    
    result = adaptive_helper(a, b, fa, fb, fm, whole, tol, 0)
    
    return IntegrationResult(result, tol, total_intervals[0], "adaptive_simpson")


def gaussian_quadrature(
    f: ScalarFunction,
    a: float,
    b: float,
    n: int = 5
) -> IntegrationResult:
    """
    Numerical integration using Gaussian quadrature.
    
    Uses Gauss-Legendre quadrature with n points. Very accurate for
    smooth functions.
    
    Args:
        f: Function to integrate
        a: Lower bound of integration
        b: Upper bound of integration
        n: Number of quadrature points (1-10 supported)
    
    Returns:
        IntegrationResult with approximate value
    
    Raises:
        ValueError: If n is not in valid range
    
    Examples:
        >>> result = gaussian_quadrature(lambda x: math.sin(x), 0, math.pi)
        >>> abs(result.value - 2) < 1e-10
        True
    """
    # Gauss-Legendre nodes and weights for standard interval [-1, 1]
    nodes_weights = {
        1: ([0.0], [2.0]),
        2: ([-0.5773502691896257, 0.5773502691896257], [1.0, 1.0]),
        3: ([-0.7745966692414834, 0.0, 0.7745966692414834],
            [0.5555555555555556, 0.8888888888888888, 0.5555555555555556]),
        4: ([-0.8611363115940526, -0.3399810435848563, 
             0.3399810435848563, 0.8611363115940526],
            [0.3478548451374538, 0.6521451548625461, 
             0.6521451548625461, 0.3478548451374538]),
        5: ([-0.9061798459386640, -0.5384693101056831, 0.0,
             0.5384693101056831, 0.9061798459386640],
            [0.2369268850561891, 0.4786286704993665, 0.5688888888888889,
             0.4786286704993665, 0.2369268850561891]),
        6: ([-0.9324695142031521, -0.6612093864662645, -0.2386191860831969,
             0.2386191860831969, 0.6612093864662645, 0.9324695142031521],
            [0.1713244923791704, 0.3607615730481386, 0.4679139345726910,
             0.4679139345726910, 0.3607615730481386, 0.1713244923791704]),
        7: ([-0.9491079123427585, -0.7415311855993945, -0.4058451513773972,
             0.0, 0.4058451513773972, 0.7415311855993945, 0.9491079123427585],
            [0.1294849661688697, 0.2797053914892766, 0.3818300505051189,
             0.4179591836734694, 0.3818300505051189, 0.2797053914892766,
             0.1294849661688697]),
        8: ([-0.9602898564975363, -0.7966664774136267, -0.5255324099163290,
             -0.1834346424956498, 0.1834346424956498, 0.5255324099163290,
             0.7966664774136267, 0.9602898564975363],
            [0.1012285362903763, 0.2223810344533745, 0.3137066458778873,
             0.3626837833783620, 0.3626837833783620, 0.3137066458778873,
             0.2223810344533745, 0.1012285362903763]),
        9: ([-0.9681602395076261, -0.8360311073266358, -0.6133714327005904,
             -0.3242534234038089, 0.0, 0.3242534234038089, 0.6133714327005904,
             0.8360311073266358, 0.9681602395076261],
            [0.0812743883615744, 0.1806481606948574, 0.2606106964029354,
             0.3123470770400029, 0.3302393550012598, 0.3123470770400029,
             0.2606106964029354, 0.1806481606948574, 0.0812743883615744]),
        10: ([-0.9739065285171717, -0.8650633666889845, -0.6794095682990244,
              -0.4333953941292472, -0.1488743389816312, 0.1488743389816312,
              0.4333953941292472, 0.6794095682990244, 0.8650633666889845,
              0.9739065285171717],
             [0.0666713443086881, 0.1494513491505806, 0.2190863625159821,
              0.2692667193099963, 0.2955242247147529, 0.2955242247147529,
              0.2692667193099963, 0.2190863625159821, 0.1494513491505806,
              0.0666713443086881])
    }
    
    if n not in nodes_weights:
        raise ValueError(f"n must be between 1 and 10, got {n}")
    
    nodes, weights = nodes_weights[n]
    
    # Transform from [-1, 1] to [a, b]
    mid = (b + a) / 2
    half = (b - a) / 2
    
    result = 0.0
    for node, weight in zip(nodes, weights):
        x = mid + half * node
        result += weight * f(x)
    
    result *= half
    
    return IntegrationResult(result, float('nan'), n, "gaussian_quadrature")


# =============================================================================
# Numerical Differentiation
# =============================================================================

def forward_difference(
    f: ScalarFunction,
    x: float,
    h: float = 1e-6
) -> float:
    """
    First derivative using forward difference approximation.
    
    f'(x) ≈ (f(x + h) - f(x)) / h
    
    Args:
        f: Function to differentiate
        x: Point at which to compute derivative
        h: Step size
    
    Returns:
        Approximate derivative
    
    Examples:
        >>> result = forward_difference(lambda x: x**2, 3)
        >>> abs(result - 6) < 1e-4
        True
    """
    return (f(x + h) - f(x)) / h


def backward_difference(
    f: ScalarFunction,
    x: float,
    h: float = 1e-6
) -> float:
    """
    First derivative using backward difference approximation.
    
    f'(x) ≈ (f(x) - f(x - h)) / h
    
    Args:
        f: Function to differentiate
        x: Point at which to compute derivative
        h: Step size
    
    Returns:
        Approximate derivative
    """
    return (f(x) - f(x - h)) / h


def central_difference(
    f: ScalarFunction,
    x: float,
    h: float = 1e-6
) -> float:
    """
    First derivative using central difference approximation.
    
    f'(x) ≈ (f(x + h) - f(x - h)) / (2h)
    
    More accurate than forward or backward difference.
    
    Args:
        f: Function to differentiate
        x: Point at which to compute derivative
        h: Step size
    
    Returns:
        Approximate derivative
    
    Examples:
        >>> result = central_difference(lambda x: x**3, 2)
        >>> abs(result - 12) < 1e-8
        True
    """
    return (f(x + h) - f(x - h)) / (2 * h)


def second_derivative(
    f: ScalarFunction,
    x: float,
    h: float = 1e-5
) -> float:
    """
    Second derivative using central difference.
    
    f''(x) ≈ (f(x + h) - 2*f(x) + f(x - h)) / h²
    
    Args:
        f: Function to differentiate
        x: Point at which to compute second derivative
        h: Step size
    
    Returns:
        Approximate second derivative
    
    Examples:
        >>> result = second_derivative(lambda x: x**3, 2)
        >>> abs(result - 12) < 1e-6
        True
    """
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)


def richardson_extrapolation(
    f: ScalarFunction,
    x: float,
    h: float = 1e-3,
    n: int = 4
) -> float:
    """
    First derivative using Richardson extrapolation.
    
    Combines multiple finite difference approximations to achieve
    higher accuracy.
    
    Args:
        f: Function to differentiate
        x: Point at which to compute derivative
        h: Initial step size
        n: Number of extrapolation levels
    
    Returns:
        Highly accurate approximate derivative
    """
    D = [[0.0] * n for _ in range(n)]
    
    # First column: central differences with decreasing h
    for i in range(n):
        D[i][0] = central_difference(f, x, h / (2 ** i))
    
    # Richardson extrapolation
    for j in range(1, n):
        for i in range(j, n):
            D[i][j] = D[i][j-1] + (D[i][j-1] - D[i-1][j-1]) / (4 ** j - 1)
    
    return D[n-1][n-1]


# =============================================================================
# Interpolation
# =============================================================================

def linear_interpolation(
    x_data: List[float],
    y_data: List[float],
    x: float
) -> float:
    """
    Linear interpolation at point x.
    
    Args:
        x_data: x coordinates of data points (must be sorted)
        y_data: y coordinates of data points
        x: Point at which to interpolate
    
    Returns:
        Interpolated value
    
    Raises:
        ValueError: If x is outside the data range or lists have different lengths
    
    Examples:
        >>> linear_interpolation([0, 1, 2], [0, 2, 4], 1.5)
        3.0
    """
    if len(x_data) != len(y_data):
        raise ValueError("x_data and y_data must have the same length")
    
    if len(x_data) < 2:
        raise ValueError("Need at least 2 data points for interpolation")
    
    if x < x_data[0] or x > x_data[-1]:
        raise ValueError(f"x = {x} is outside the data range [{x_data[0]}, {x_data[-1]}]")
    
    # Find the interval
    for i in range(len(x_data) - 1):
        if x_data[i] <= x <= x_data[i + 1]:
            t = (x - x_data[i]) / (x_data[i + 1] - x_data[i])
            return y_data[i] + t * (y_data[i + 1] - y_data[i])
    
    # Should not reach here
    return y_data[-1]


def lagrange_interpolation(
    x_data: List[float],
    y_data: List[float],
    x: float
) -> float:
    """
    Lagrange interpolation at point x.
    
    Constructs the Lagrange polynomial that passes through all data points.
    Warning: May suffer from Runge's phenomenon for many points.
    
    Args:
        x_data: x coordinates of data points
        y_data: y coordinates of data points
        x: Point at which to interpolate
    
    Returns:
        Interpolated value
    
    Examples:
        >>> lagrange_interpolation([0, 1, 2], [1, 3, 9], 1.5)
        5.75
    """
    n = len(x_data)
    result = 0.0
    
    for i in range(n):
        term = y_data[i]
        for j in range(n):
            if i != j:
                term *= (x - x_data[j]) / (x_data[i] - x_data[j])
        result += term
    
    return result


def newton_divided_difference(
    x_data: List[float],
    y_data: List[float]
) -> List[float]:
    """
    Compute Newton's divided difference coefficients.
    
    Args:
        x_data: x coordinates of data points
        y_data: y coordinates of data points
    
    Returns:
        List of divided difference coefficients
    
    Examples:
        >>> newton_divided_difference([0, 1, 2], [1, 3, 9])
        [1, 2.0, 2.0]
    """
    n = len(x_data)
    # Create a copy of y_data to work with
    dd = y_data.copy()
    coefficients = [dd[0]]
    
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            dd[i] = (dd[i] - dd[i - 1]) / (x_data[i] - x_data[i - j])
        coefficients.append(dd[j])
    
    return coefficients


def newton_interpolation(
    x_data: List[float],
    y_data: List[float],
    x: float
) -> float:
    """
    Newton interpolation at point x.
    
    Uses Newton's form of the interpolating polynomial with divided differences.
    More numerically stable and allows easy addition of new points.
    
    Args:
        x_data: x coordinates of data points
        y_data: y coordinates of data points
        x: Point at which to interpolate
    
    Returns:
        Interpolated value
    """
    coefficients = newton_divided_difference(x_data, y_data)
    n = len(x_data)
    
    result = coefficients[0]
    product = 1.0
    
    for i in range(1, n):
        product *= (x - x_data[i - 1])
        result += coefficients[i] * product
    
    return result


def cubic_spline_coefficients(
    x_data: List[float],
    y_data: List[float],
    natural: bool = True
) -> Tuple[List[float], List[float], List[float], List[float]]:
    """
    Compute cubic spline coefficients for natural or clamped spline.
    
    Args:
        x_data: x coordinates of data points (must be sorted)
        y_data: y coordinates of data points
        natural: If True, use natural boundary conditions (zero second derivative)
    
    Returns:
        Tuple of (a, b, c, d) coefficients for each interval
        S(x) = a_i + b_i*(x - x_i) + c_i*(x - x_i)^2 + d_i*(x - x_i)^3
    """
    n = len(x_data) - 1
    
    # Step sizes
    h = [x_data[i + 1] - x_data[i] for i in range(n)]
    
    # Set up tridiagonal system
    alpha = [0.0] * (n + 1)
    
    for i in range(1, n):
        alpha[i] = (3 / h[i] * (y_data[i + 1] - y_data[i]) -
                   3 / h[i - 1] * (y_data[i] - y_data[i - 1]))
    
    # Solve tridiagonal system
    l = [1.0] + [0.0] * n
    mu = [0.0] * (n + 1)
    z = [0.0] * (n + 1)
    
    for i in range(1, n):
        l[i] = 2 * (x_data[i + 1] - x_data[i - 1]) - h[i - 1] * mu[i - 1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i]
    
    l[n] = 1.0
    
    # Back substitution
    c = [0.0] * (n + 1)
    b = [0.0] * n
    d = [0.0] * n
    
    for j in range(n - 1, -1, -1):
        c[j] = z[j] - mu[j] * c[j + 1]
        b[j] = (y_data[j + 1] - y_data[j]) / h[j] - h[j] * (c[j + 1] + 2 * c[j]) / 3
        d[j] = (c[j + 1] - c[j]) / (3 * h[j])
    
    a = y_data[:-1]
    
    return a, b, c[:-1], d


def cubic_spline_interpolation(
    x_data: List[float],
    y_data: List[float],
    x: float,
    natural: bool = True
) -> float:
    """
    Cubic spline interpolation at point x.
    
    Uses natural cubic spline (zero second derivatives at boundaries).
    
    Args:
        x_data: x coordinates of data points (must be sorted)
        y_data: y coordinates of data points
        x: Point at which to interpolate
        natural: Use natural boundary conditions
    
    Returns:
        Interpolated value
    
    Raises:
        ValueError: If x is outside the data range
    """
    if x < x_data[0] or x > x_data[-1]:
        raise ValueError(f"x = {x} is outside the data range")
    
    n = len(x_data) - 1
    a, b, c, d = cubic_spline_coefficients(x_data, y_data, natural)
    
    # Find the interval
    for i in range(n):
        if x_data[i] <= x <= x_data[i + 1]:
            dx = x - x_data[i]
            return a[i] + b[i] * dx + c[i] * dx ** 2 + d[i] * dx ** 3
    
    # Should not reach here
    return y_data[-1]


# =============================================================================
# Optimization
# =============================================================================

def golden_section_search(
    f: ScalarFunction,
    a: float,
    b: float,
    tol: float = 1e-10,
    max_iter: int = 1000,
    find_min: bool = True
) -> RootResult:
    """
    Find minimum or maximum of unimodal function using golden section search.
    
    A derivative-free optimization method that uses the golden ratio
    to efficiently bracket the extremum.
    
    Args:
        f: Function to optimize
        a: Left endpoint of interval
        b: Right endpoint of interval
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
        find_min: If True, find minimum; otherwise find maximum
    
    Returns:
        RootResult with the extremum location
    
    Examples:
        >>> result = golden_section_search(lambda x: x**2, -1, 1)
        >>> abs(result.root) < 1e-9
        True
    """
    golden_ratio = (math.sqrt(5) - 1) / 2
    
    # Comparison function based on whether we're finding min or max
    def compare(fa, fb):
        return fa < fb if find_min else fa > fb
    
    c = b - golden_ratio * (b - a)
    d = a + golden_ratio * (b - a)
    
    fc = f(c)
    fd = f(d)
    
    for i in range(max_iter):
        if b - a < tol:
            extremum = (a + b) / 2
            return RootResult(extremum, i, True, "Converged", f(extremum))
        
        if compare(fc, fd):
            b = d
            d = c
            fd = fc
            c = b - golden_ratio * (b - a)
            fc = f(c)
        else:
            a = c
            c = d
            fc = fd
            d = a + golden_ratio * (b - a)
            fd = f(d)
    
    extremum = (a + b) / 2
    return RootResult(extremum, max_iter, False, "Maximum iterations reached", f(extremum))


def gradient_descent_1d(
    df: ScalarFunction,
    x0: float,
    lr: float = 0.1,
    tol: float = 1e-10,
    max_iter: int = 1000,
    momentum: float = 0.0
) -> RootResult:
    """
    1D gradient descent optimization.
    
    Args:
        df: Derivative of the function to minimize
        x0: Initial guess
        lr: Learning rate
        tol: Tolerance for stopping (based on gradient magnitude)
        max_iter: Maximum number of iterations
        momentum: Momentum coefficient (0 = no momentum)
    
    Returns:
        RootResult with the minimum location
    
    Examples:
        >>> result = gradient_descent_1d(lambda x: 2*x, 5.0, lr=0.1)
        >>> abs(result.root) < 1e-8
        True
    """
    x = x0
    velocity = 0.0
    
    for i in range(max_iter):
        grad = df(x)
        
        if abs(grad) < tol:
            return RootResult(x, i, True, "Converged", grad)
        
        # Momentum update
        velocity = momentum * velocity - lr * grad
        x = x + velocity
    
    return RootResult(x, max_iter, False, "Maximum iterations reached", df(x))


def nelder_mead_1d(
    f: ScalarFunction,
    x0: float,
    delta: float = 1.0,
    tol: float = 1e-10,
    max_iter: int = 1000
) -> RootResult:
    """
    1D Nelder-Mead simplex method (pattern search).
    
    A derivative-free optimization method that uses a simple pattern
    to find the minimum.
    
    Args:
        f: Function to minimize
        x0: Initial guess
        delta: Initial step size
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
    
    Returns:
        RootResult with the minimum location
    """
    # Simple pattern search for 1D
    x = x0
    step = delta
    fx = f(x)
    
    for i in range(max_iter):
        if step < tol:
            return RootResult(x, i, True, "Converged", fx)
        
        # Try positive step
        x_plus = x + step
        f_plus = f(x_plus)
        
        # Try negative step
        x_minus = x - step
        f_minus = f(x_minus)
        
        # Find best direction
        if f_plus < fx and f_plus <= f_minus:
            x = x_plus
            fx = f_plus
            step *= 2  # Expand
        elif f_minus < fx:
            x = x_minus
            fx = f_minus
            step *= 2  # Expand
        else:
            step /= 2  # Contract
    
    return RootResult(x, max_iter, False, "Maximum iterations reached", fx)


# =============================================================================
# Utility Functions
# =============================================================================

def approximate_derivative(
    f: ScalarFunction,
    x: float,
    order: int = 1,
    h: float = 1e-6,
    method: str = 'central'
) -> float:
    """
    Approximate derivative of any order using finite differences.
    
    Args:
        f: Function to differentiate
        x: Point at which to compute derivative
        order: Order of derivative (1, 2, 3, or 4)
        h: Step size
        method: 'forward', 'backward', or 'central'
    
    Returns:
        Approximate derivative
    
    Raises:
        ValueError: If order is not 1-4 or method is invalid
    """
    if method == 'forward':
        if order == 1:
            return (f(x + h) - f(x)) / h
        elif order == 2:
            return (f(x + 2*h) - 2*f(x + h) + f(x)) / (h**2)
        elif order == 3:
            return (f(x + 3*h) - 3*f(x + 2*h) + 3*f(x + h) - f(x)) / (h**3)
        elif order == 4:
            return (f(x + 4*h) - 4*f(x + 3*h) + 6*f(x + 2*h) - 4*f(x + h) + f(x)) / (h**4)
    
    elif method == 'backward':
        if order == 1:
            return (f(x) - f(x - h)) / h
        elif order == 2:
            return (f(x) - 2*f(x - h) + f(x - 2*h)) / (h**2)
        elif order == 3:
            return (f(x) - 3*f(x - h) + 3*f(x - 2*h) - f(x - 3*h)) / (h**3)
        elif order == 4:
            return (f(x) - 4*f(x - h) + 6*f(x - 2*h) - 4*f(x - 3*h) + f(x - 4*h)) / (h**4)
    
    elif method == 'central':
        if order == 1:
            return (f(x + h) - f(x - h)) / (2 * h)
        elif order == 2:
            return (f(x + h) - 2*f(x) + f(x - h)) / (h**2)
        elif order == 3:
            return (f(x + 2*h) - 2*f(x + h) + 2*f(x - h) - f(x - 2*h)) / (2 * h**3)
        elif order == 4:
            return (f(x + 2*h) - 4*f(x + h) + 6*f(x) - 4*f(x - h) + f(x - 2*h)) / (h**4)
    
    raise ValueError(f"Invalid order ({order}) or method ({method})")


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Data classes
    'RootResult',
    'IntegrationResult',
    'InterpolationResult',
    
    # Root finding
    'bisection',
    'newton_raphson',
    'secant_method',
    'brent_method',
    
    # Integration
    'trapezoidal_rule',
    'simpsons_rule',
    'adaptive_simpson',
    'gaussian_quadrature',
    
    # Differentiation
    'forward_difference',
    'backward_difference',
    'central_difference',
    'second_derivative',
    'richardson_extrapolation',
    
    # Interpolation
    'linear_interpolation',
    'lagrange_interpolation',
    'newton_divided_difference',
    'newton_interpolation',
    'cubic_spline_coefficients',
    'cubic_spline_interpolation',
    
    # Optimization
    'golden_section_search',
    'gradient_descent_1d',
    'nelder_mead_1d',
    
    # Utilities
    'approximate_derivative',
]


if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Numerical Methods Utilities Demo")
    print("=" * 60)
    
    # Root finding demo
    print("\n--- Root Finding ---")
    f = lambda x: x**2 - 2
    df = lambda x: 2*x
    
    print("\nFinding root of x² - 2 = 0 (sqrt(2)):")
    
    result = bisection(f, 1, 2)
    print(f"  Bisection:        root = {result.root:.10f}, iterations = {result.iterations}")
    
    result = newton_raphson(f, df, 1.5)
    print(f"  Newton-Raphson:   root = {result.root:.10f}, iterations = {result.iterations}")
    
    result = secant_method(f, 1, 2)
    print(f"  Secant method:    root = {result.root:.10f}, iterations = {result.iterations}")
    
    result = brent_method(f, 1, 2)
    print(f"  Brent's method:   root = {result.root:.10f}, iterations = {result.iterations}")
    
    print(f"  Actual sqrt(2):   {math.sqrt(2):.10f}")
    
    # Integration demo
    print("\n--- Numerical Integration ---")
    g = lambda x: math.sin(x)
    
    print("\nIntegrating sin(x) from 0 to π:")
    print(f"  Exact value: 2.0")
    
    result = trapezoidal_rule(g, 0, math.pi, 100)
    print(f"  Trapezoidal (n=100):  {result.value:.10f}")
    
    result = simpsons_rule(g, 0, math.pi, 100)
    print(f"  Simpson's (n=100):    {result.value:.10f}")
    
    result = adaptive_simpson(g, 0, math.pi)
    print(f"  Adaptive Simpson:     {result.value:.10f}")
    
    result = gaussian_quadrature(g, 0, math.pi, 5)
    print(f"  Gaussian (n=5):       {result.value:.10f}")
    
    # Differentiation demo
    print("\n--- Numerical Differentiation ---")
    h = lambda x: x**3
    
    print("\nDerivative of x³ at x = 2:")
    print(f"  Exact value: 12.0")
    print(f"  Forward difference:  {forward_difference(h, 2):.10f}")
    print(f"  Backward difference: {backward_difference(h, 2):.10f}")
    print(f"  Central difference:  {central_difference(h, 2):.10f}")
    print(f"  Richardson:          {richardson_extrapolation(h, 2):.10f}")
    
    # For second derivative, use x² to get constant 2
    k = lambda x: x**2
    print("\nSecond derivative of x² at x = 2:")
    print(f"  Exact value: 2.0")
    print(f"  Second derivative:   {second_derivative(k, 2):.10f}")
    
    # Interpolation demo
    print("\n--- Interpolation ---")
    x_data = [0, 1, 2, 3, 4]
    y_data = [0, 1, 4, 9, 16]  # y = x²
    
    print("\nInterpolating y = x² at x = 2.5:")
    print(f"  Exact value: 6.25")
    print(f"  Linear:      {linear_interpolation(x_data, y_data, 2.5):.10f}")
    print(f"  Lagrange:    {lagrange_interpolation(x_data, y_data, 2.5):.10f}")
    print(f"  Newton:      {newton_interpolation(x_data, y_data, 2.5):.10f}")
    print(f"  Cubic spline: {cubic_spline_interpolation(x_data, y_data, 2.5):.10f}")
    
    # Optimization demo
    print("\n--- Optimization ---")
    func = lambda x: (x - 2)**2 + 1
    dfunc = lambda x: 2*(x - 2)
    
    print("\nMinimizing (x - 2)² + 1:")
    print(f"  Exact minimum: x = 2.0")
    
    result = golden_section_search(func, 0, 4)
    print(f"  Golden section:  x = {result.root:.10f}")
    
    result = gradient_descent_1d(dfunc, 0.0, lr=0.1)
    print(f"  Gradient descent: x = {result.root:.10f}")
    
    result = nelder_mead_1d(func, 0.0)
    print(f"  Nelder-Mead:     x = {result.root:.10f}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")