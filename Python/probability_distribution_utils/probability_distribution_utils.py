"""
Probability Distribution Utilities

A comprehensive library for probability distributions with zero external dependencies.
Supports common distributions: Normal, Exponential, Uniform, Poisson, Binomial,
Geometric, Chi-Square, Student's t, F-distribution, Beta, Gamma, and more.

Author: AllToolkit
Date: 2026-04-29
"""

import math
import random
from typing import List, Tuple, Optional, Union
from functools import lru_cache


# ============================================================================
# Mathematical Helper Functions
# ============================================================================

def _factorial(n: int) -> int:
    """Calculate factorial of n."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def _gamma_function(x: float) -> float:
    """
    Calculate the gamma function using Lanczos approximation.
    Accurate to about 15 decimal places.
    """
    if x < 0.5:
        # Use reflection formula: Gamma(x) * Gamma(1-x) = pi / sin(pi*x)
        return math.pi / (math.sin(math.pi * x) * _gamma_function(1 - x))
    
    # Lanczos coefficients
    g = 7
    coefficients = [
        0.99999999999980993,
        676.5203681218851,
        -1259.1392167224028,
        771.32342877765313,
        -176.61502916214059,
        12.507343278686905,
        -0.13857109526572012,
        9.9843695780195716e-6,
        1.5056327351493116e-7
    ]
    
    x -= 1
    y = coefficients[0]
    for i in range(1, g + 2):
        y += coefficients[i] / (x + i)
    
    t = x + g + 0.5
    return math.sqrt(2 * math.pi) * (t ** (x + 0.5)) * math.exp(-t) * y


def _beta_function(a: float, b: float) -> float:
    """Calculate the beta function B(a, b) = Gamma(a) * Gamma(b) / Gamma(a + b)."""
    # Use log to avoid overflow for large arguments
    log_beta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    return math.exp(log_beta)


def _incomplete_gamma(a: float, x: float, max_iterations: int = 200) -> float:
    """
    Calculate the lower incomplete gamma function using series expansion.
    gamma(a, x) = integral from 0 to x of t^(a-1) * e^(-t) dt
    """
    if x < 0:
        raise ValueError("x must be non-negative")
    if x == 0:
        return 0.0
    
    # Use series expansion for small x
    if x < a + 1:
        ap = a
        sum_val = 1.0 / a
        delta = sum_val
        for _ in range(max_iterations):
            ap += 1
            delta *= x / ap
            sum_val += delta
            if abs(delta) < abs(sum_val) * 1e-15:
                break
        return sum_val * math.exp(-x) * (x ** a)
    
    # Use continued fraction for large x
    else:
        b = x + 1 - a
        c = 1e308  # Large number
        d = 1.0 / b
        h = d
        for i in range(1, max_iterations):
            an = -i * (i - a)
            b += 2
            d = an * d + b
            if abs(d) < 1e-300:
                d = 1e-300
            c = b + an / c
            if abs(c) < 1e-300:
                c = 1e-300
            d = 1.0 / d
            delta = d * c
            h *= delta
            if abs(delta - 1) < 1e-15:
                break
        return _gamma_function(a) - math.exp(-x) * (x ** a) * h


def _regularized_incomplete_gamma(a: float, x: float) -> float:
    """Calculate P(a, x) = gamma(a, x) / Gamma(a)."""
    if x <= 0:
        return 0.0
    return _incomplete_gamma(a, x) / _gamma_function(a)


def _erf(x: float) -> float:
    """
    Calculate the error function erf(x).
    Using Horner's method approximation.
    """
    # Special case: erf(0) = 0
    if x == 0:
        return 0.0
    
    # Save the sign of x
    sign = 1 if x >= 0 else -1
    x = abs(x)
    
    # Constants for approximation
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    
    return sign * y


def _erfc(x: float) -> float:
    """Calculate the complementary error function erfc(x) = 1 - erf(x)."""
    return 1.0 - _erf(x)


def _inverse_normal_cdf(p: float, tolerance: float = 1e-12) -> float:
    """
    Calculate the inverse of the standard normal CDF (quantile function).
    Using Newton-Raphson method with initial approximation.
    """
    if p <= 0:
        return float('-inf')
    if p >= 1:
        return float('inf')
    
    # Special case: p = 0.5 returns 0
    if abs(p - 0.5) < 1e-10:
        return 0.0
    
    # Initial approximation using simple formula
    if p < 0.5:
        sign = -1
        pp = p
    else:
        sign = 1
        pp = 1 - p
    
    # Simple initial approximation
    t = math.sqrt(-2 * math.log(pp))
    x = t - (2.515517 + 0.802853 * t + 0.010328 * t * t) / \
        (1 + 1.432788 * t + 0.189269 * t * t + 0.001308 * t * t * t)
    x = sign * x
    
    # Newton-Raphson refinement
    for _ in range(10):
        cdf_val = 0.5 * (1 + _erf(x / math.sqrt(2)))
        pdf_val = math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
        
        if pdf_val < 1e-300:
            break
        
        delta = (cdf_val - p) / pdf_val
        x = x - delta
        
        if abs(delta) < tolerance:
            break
    
    return x


# ============================================================================
# Base Distribution Class
# ============================================================================

class Distribution:
    """Base class for probability distributions."""
    
    def __init__(self):
        self._mean = None
        self._variance = None
        self._std = None
    
    def pdf(self, x: float) -> float:
        """Probability density function (for continuous) or probability mass function (for discrete)."""
        raise NotImplementedError
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        raise NotImplementedError
    
    def quantile(self, p: float) -> float:
        """Inverse CDF (percent point function)."""
        raise NotImplementedError
    
    def sample(self, n: int = 1) -> List[float]:
        """Generate random samples."""
        raise NotImplementedError
    
    def sample_one(self) -> float:
        """Generate a single random sample."""
        return self.sample(1)[0]
    
    @property
    def mean(self) -> float:
        """Expected value of the distribution."""
        if self._mean is None:
            self._mean = self._calculate_mean()
        return self._mean
    
    @property
    def variance(self) -> float:
        """Variance of the distribution."""
        if self._variance is None:
            self._variance = self._calculate_variance()
        return self._variance
    
    @property
    def std(self) -> float:
        """Standard deviation of the distribution."""
        if self._std is None:
            self._std = math.sqrt(self.variance)
        return self._std
    
    def _calculate_mean(self) -> float:
        raise NotImplementedError
    
    def _calculate_variance(self) -> float:
        raise NotImplementedError
    
    def interval(self, confidence: float = 0.95) -> Tuple[float, float]:
        """Calculate confidence interval."""
        if not 0 < confidence < 1:
            raise ValueError("Confidence must be between 0 and 1")
        alpha = 1 - confidence
        return (self.quantile(alpha / 2), self.quantile(1 - alpha / 2))


# ============================================================================
# Normal (Gaussian) Distribution
# ============================================================================

class NormalDistribution(Distribution):
    """
    Normal (Gaussian) distribution.
    
    Parameters:
        mu: Mean (location parameter)
        sigma: Standard deviation (scale parameter)
    """
    
    def __init__(self, mu: float = 0.0, sigma: float = 1.0):
        if sigma <= 0:
            raise ValueError("Sigma must be positive")
        super().__init__()
        self.mu = mu
        self.sigma = sigma
        self._mean = mu
        self._variance = sigma ** 2
        self._std = sigma
    
    def pdf(self, x: float) -> float:
        """Probability density function."""
        z = (x - self.mu) / self.sigma
        return math.exp(-0.5 * z * z) / (self.sigma * math.sqrt(2 * math.pi))
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        z = (x - self.mu) / self.sigma
        return 0.5 * (1 + _erf(z / math.sqrt(2)))
    
    def quantile(self, p: float) -> float:
        """Inverse CDF (quantile function)."""
        return self.mu + self.sigma * _inverse_normal_cdf(p)
    
    def sample(self, n: int = 1) -> List[float]:
        """Generate random samples using Box-Muller transform."""
        samples = []
        for _ in range(n):
            u1 = random.random()
            u2 = random.random()
            # Avoid log(0)
            while u1 == 0:
                u1 = random.random()
            z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            samples.append(self.mu + self.sigma * z)
        return samples
    
    def _calculate_mean(self) -> float:
        return self.mu
    
    def _calculate_variance(self) -> float:
        return self.sigma ** 2


# ============================================================================
# Uniform Distribution
# ============================================================================

class UniformDistribution(Distribution):
    """
    Continuous uniform distribution.
    
    Parameters:
        a: Lower bound
        b: Upper bound
    """
    
    def __init__(self, a: float = 0.0, b: float = 1.0):
        if b <= a:
            raise ValueError("b must be greater than a")
        super().__init__()
        self.a = a
        self.b = b
        self._mean = (a + b) / 2
        self._variance = ((b - a) ** 2) / 12
    
    def pdf(self, x: float) -> float:
        """Probability density function."""
        if self.a <= x <= self.b:
            return 1.0 / (self.b - self.a)
        return 0.0
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        if x < self.a:
            return 0.0
        elif x > self.b:
            return 1.0
        else:
            return (x - self.a) / (self.b - self.a)
    
    def quantile(self, p: float) -> float:
        """Inverse CDF."""
        if not 0 <= p <= 1:
            raise ValueError("p must be between 0 and 1")
        return self.a + p * (self.b - self.a)
    
    def sample(self, n: int = 1) -> List[float]:
        """Generate random samples."""
        return [random.uniform(self.a, self.b) for _ in range(n)]
    
    def _calculate_mean(self) -> float:
        return (self.a + self.b) / 2
    
    def _calculate_variance(self) -> float:
        return ((self.b - self.a) ** 2) / 12


# ============================================================================
# Exponential Distribution
# ============================================================================

class ExponentialDistribution(Distribution):
    """
    Exponential distribution.
    
    Parameters:
        rate: Rate parameter (lambda), must be positive
    """
    
    def __init__(self, rate: float = 1.0):
        if rate <= 0:
            raise ValueError("Rate must be positive")
        super().__init__()
        self.rate = rate
        self._mean = 1.0 / rate
        self._variance = 1.0 / (rate ** 2)
    
    def pdf(self, x: float) -> float:
        """Probability density function."""
        if x < 0:
            return 0.0
        return self.rate * math.exp(-self.rate * x)
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        if x < 0:
            return 0.0
        return 1 - math.exp(-self.rate * x)
    
    def quantile(self, p: float) -> float:
        """Inverse CDF."""
        if not 0 <= p < 1:
            raise ValueError("p must be between 0 and 1 (exclusive of 1)")
        return -math.log(1 - p) / self.rate
    
    def sample(self, n: int = 1) -> List[float]:
        """Generate random samples using inverse transform."""
        samples = []
        for _ in range(n):
            u = random.random()
            while u == 0:  # Avoid log(0)
                u = random.random()
            samples.append(-math.log(u) / self.rate)
        return samples
    
    def _calculate_mean(self) -> float:
        return 1.0 / self.rate
    
    def _calculate_variance(self) -> float:
        return 1.0 / (self.rate ** 2)


# ============================================================================
# Poisson Distribution
# ============================================================================

class PoissonDistribution(Distribution):
    """
    Poisson distribution (discrete).
    
    Parameters:
        lambda_param: Rate parameter (expected number of events)
    """
    
    def __init__(self, lambda_param: float = 1.0):
        if lambda_param <= 0:
            raise ValueError("Lambda must be positive")
        super().__init__()
        self.lambda_param = lambda_param
        self._mean = lambda_param
        self._variance = lambda_param
    
    def pmf(self, k: int) -> float:
        """Probability mass function."""
        if k < 0:
            return 0.0
        return (self.lambda_param ** k) * math.exp(-self.lambda_param) / _factorial(k)
    
    def pdf(self, x: float) -> float:
        """Alias for pmf."""
        return self.pmf(int(x))
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        k = int(x)
        if k < 0:
            return 0.0
        result = 0.0
        for i in range(k + 1):
            result += self.pmf(i)
        return result
    
    def quantile(self, p: float) -> int:
        """Inverse CDF (returns smallest k such that CDF(k) >= p)."""
        if not 0 <= p <= 1:
            raise ValueError("p must be between 0 and 1")
        cumsum = 0.0
        k = 0
        while cumsum < p:
            cumsum += self.pmf(k)
            k += 1
        return k - 1 if cumsum > p else k
    
    def sample(self, n: int = 1) -> List[int]:
        """Generate random samples using Knuth's algorithm."""
        samples = []
        L = math.exp(-self.lambda_param)
        for _ in range(n):
            k = 0
            p = 1.0
            while p > L:
                k += 1
                p *= random.random()
            samples.append(k - 1)
        return samples
    
    def _calculate_mean(self) -> float:
        return self.lambda_param
    
    def _calculate_variance(self) -> float:
        return self.lambda_param


# ============================================================================
# Binomial Distribution
# ============================================================================

class BinomialDistribution(Distribution):
    """
    Binomial distribution (discrete).
    
    Parameters:
        n: Number of trials
        p: Probability of success on each trial
    """
    
    def __init__(self, n: int, p: float):
        if n < 0:
            raise ValueError("n must be non-negative")
        if not 0 <= p <= 1:
            raise ValueError("p must be between 0 and 1")
        super().__init__()
        self.n = n
        self.p = p
        self._mean = n * p
        self._variance = n * p * (1 - p)
    
    def _binomial_coefficient(self, n: int, k: int) -> int:
        """Calculate binomial coefficient C(n, k)."""
        if k < 0 or k > n:
            return 0
        if k == 0 or k == n:
            return 1
        k = min(k, n - k)
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        return result
    
    def pmf(self, k: int) -> float:
        """Probability mass function."""
        if k < 0 or k > self.n:
            return 0.0
        coeff = self._binomial_coefficient(self.n, k)
        return coeff * (self.p ** k) * ((1 - self.p) ** (self.n - k))
    
    def pdf(self, x: float) -> float:
        """Alias for pmf."""
        return self.pmf(int(x))
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        k = int(x)
        if k < 0:
            return 0.0
        k = min(k, self.n)
        result = 0.0
        for i in range(k + 1):
            result += self.pmf(i)
        return result
    
    def quantile(self, p: float) -> int:
        """Inverse CDF."""
        if not 0 <= p <= 1:
            raise ValueError("p must be between 0 and 1")
        cumsum = 0.0
        k = 0
        while cumsum < p and k <= self.n:
            cumsum += self.pmf(k)
            k += 1
        return max(0, k - 1)
    
    def sample(self, n: int = 1) -> List[int]:
        """Generate random samples."""
        samples = []
        for _ in range(n):
            successes = 0
            for _ in range(self.n):
                if random.random() < self.p:
                    successes += 1
            samples.append(successes)
        return samples
    
    def _calculate_mean(self) -> float:
        return self.n * self.p
    
    def _calculate_variance(self) -> float:
        return self.n * self.p * (1 - self.p)


# ============================================================================
# Geometric Distribution
# ============================================================================

class GeometricDistribution(Distribution):
    """
    Geometric distribution (discrete).
    Models the number of trials needed to get the first success.
    
    Parameters:
        p: Probability of success on each trial
    """
    
    def __init__(self, p: float):
        if not 0 < p <= 1:
            raise ValueError("p must be between 0 (exclusive) and 1")
        super().__init__()
        self.p = p
        self._mean = 1.0 / p
        self._variance = (1 - p) / (p ** 2)
    
    def pmf(self, k: int) -> float:
        """Probability mass function. P(X = k) = (1-p)^(k-1) * p"""
        if k < 1:
            return 0.0
        return ((1 - self.p) ** (k - 1)) * self.p
    
    def pdf(self, x: float) -> float:
        """Alias for pmf."""
        return self.pmf(int(x))
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        k = int(x)
        if k < 1:
            return 0.0
        return 1 - (1 - self.p) ** k
    
    def quantile(self, p: float) -> int:
        """Inverse CDF."""
        if not 0 <= p < 1:
            raise ValueError("p must be between 0 and 1 (exclusive of 1)")
        return int(math.ceil(math.log(1 - p) / math.log(1 - self.p)))
    
    def sample(self, n: int = 1) -> List[int]:
        """Generate random samples."""
        samples = []
        for _ in range(n):
            k = 1
            while random.random() >= self.p:
                k += 1
            samples.append(k)
        return samples
    
    def _calculate_mean(self) -> float:
        return 1.0 / self.p
    
    def _calculate_variance(self) -> float:
        return (1 - self.p) / (self.p ** 2)


# ============================================================================
# Chi-Square Distribution
# ============================================================================

class ChiSquareDistribution(Distribution):
    """
    Chi-square distribution.
    
    Parameters:
        df: Degrees of freedom
    """
    
    def __init__(self, df: int):
        if df <= 0:
            raise ValueError("Degrees of freedom must be positive")
        super().__init__()
        self.df = df
        self._mean = df
        self._variance = 2 * df
    
    def pdf(self, x: float) -> float:
        """Probability density function."""
        if x <= 0:
            return 0.0
        k = self.df / 2.0
        return (x ** (k - 1)) * math.exp(-x / 2) / (2 ** k * _gamma_function(k))
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        if x <= 0:
            return 0.0
        return _regularized_incomplete_gamma(self.df / 2.0, x / 2.0)
    
    def quantile(self, p: float) -> float:
        """Inverse CDF using Newton-Raphson method."""
        if not 0 <= p <= 1:
            raise ValueError("p must be between 0 and 1")
        
        # Initial approximation
        x = self.df * (1 - 2 / (9 * self.df) + 
                       math.sqrt(2 / (9 * self.df)) * _inverse_normal_cdf(p)) ** 3
        
        # Newton-Raphson refinement
        for _ in range(50):
            fx = self.cdf(x) - p
            fpx = self.pdf(x)
            if fpx == 0:
                break
            x_new = x - fx / fpx
            if abs(x_new - x) < 1e-10:
                break
            x = max(0.001, x_new)
        
        return x
    
    def sample(self, n: int = 1) -> List[float]:
        """Generate random samples."""
        samples = []
        normal = NormalDistribution(0, 1)
        for _ in range(n):
            chi_sq = sum(normal.sample_one() ** 2 for _ in range(self.df))
            samples.append(chi_sq)
        return samples
    
    def _calculate_mean(self) -> float:
        return self.df
    
    def _calculate_variance(self) -> float:
        return 2 * self.df


# ============================================================================
# Student's t-Distribution
# ============================================================================

class StudentTDistribution(Distribution):
    """
    Student's t-distribution.
    
    Parameters:
        df: Degrees of freedom
    """
    
    def __init__(self, df: float):
        if df <= 0:
            raise ValueError("Degrees of freedom must be positive")
        super().__init__()
        self.df = df
        self._mean = 0 if df > 1 else float('nan')
        self._variance = df / (df - 2) if df > 2 else (float('inf') if df > 1 else float('nan'))
    
    def pdf(self, x: float) -> float:
        """Probability density function."""
        df = self.df
        return (_gamma_function((df + 1) / 2) / 
                (math.sqrt(df * math.pi) * _gamma_function(df / 2)) * 
                (1 + x ** 2 / df) ** (-(df + 1) / 2))
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        df = self.df
        if x == 0:
            return 0.5
        # Use regularized incomplete beta function
        # CDF(t) = 1 - 0.5 * I_{df/(df+t^2)}(df/2, 0.5) for t >= 0
        # CDF(t) = 0.5 * I_{df/(df+t^2)}(df/2, 0.5) for t < 0
        z = df / (df + x ** 2)
        ibeta = self._incomplete_beta(df / 2, 0.5, z)
        if x >= 0:
            return 1 - 0.5 * ibeta
        else:
            return 0.5 * ibeta
    
    def _incomplete_beta(self, a: float, b: float, x: float) -> float:
        """Calculate regularized incomplete beta function."""
        if x < 0 or x > 1:
            raise ValueError("x must be between 0 and 1")
        if x == 0:
            return 0.0
        if x == 1:
            return 1.0
        
        # Use symmetry relation
        if x > (a + 1) / (a + b + 2):
            return 1 - self._incomplete_beta(b, a, 1 - x)
        
        # Continued fraction expansion
        qab = a + b
        qap = a + 1
        qam = a - 1
        c = 1.0
        d = 1.0 - qab * x / qap
        if abs(d) < 1e-300:
            d = 1e-300
        d = 1.0 / d
        h = d
        
        for m in range(1, 200):
            m2 = 2 * m
            aa = m * (b - m) * x / ((qam + m2) * (a + m2))
            d = 1.0 + aa * d
            if abs(d) < 1e-300:
                d = 1e-300
            c = 1.0 + aa / c
            if abs(c) < 1e-300:
                c = 1e-300
            d = 1.0 / d
            h *= d * c
            aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
            d = 1.0 + aa * d
            if abs(d) < 1e-300:
                d = 1e-300
            c = 1.0 + aa / c
            if abs(c) < 1e-300:
                c = 1e-300
            d = 1.0 / d
            delta = d * c
            h *= delta
            if abs(delta - 1) < 1e-10:
                break
        
        # Use log to avoid overflow for large parameters
        log_front = a * math.log(x) + b * math.log(1 - x) - math.lgamma(a) - math.lgamma(b) + math.lgamma(a + b)
        front = math.exp(log_front)
        return front * h / a
    
    def quantile(self, p: float) -> float:
        """Inverse CDF using Newton-Raphson."""
        if not 0 < p < 1:
            raise ValueError("p must be between 0 and 1")
        
        # Start with normal approximation
        x = _inverse_normal_cdf(p)
        
        # Newton-Raphson refinement
        for _ in range(50):
            fx = self.cdf(x) - p
            fpx = self.pdf(x)
            if fpx == 0:
                break
            x_new = x - fx / fpx
            if abs(x_new - x) < 1e-10:
                break
            x = x_new
        
        return x
    
    def sample(self, n: int = 1) -> List[float]:
        """Generate random samples."""
        samples = []
        normal = NormalDistribution(0, 1)
        for _ in range(n):
            z = normal.sample_one()
            chi = ChiSquareDistribution(self.df).sample_one()
            samples.append(z / math.sqrt(chi / self.df))
        return samples
    
    def _calculate_mean(self) -> float:
        return 0 if self.df > 1 else float('nan')
    
    def _calculate_variance(self) -> float:
        if self.df > 2:
            return self.df / (self.df - 2)
        elif self.df > 1:
            return float('inf')
        return float('nan')


# ============================================================================
# Beta Distribution
# ============================================================================

class BetaDistribution(Distribution):
    """
    Beta distribution.
    
    Parameters:
        alpha: Shape parameter 1
        beta: Shape parameter 2
    """
    
    def __init__(self, alpha: float, beta: float):
        if alpha <= 0 or beta <= 0:
            raise ValueError("Alpha and beta must be positive")
        super().__init__()
        self.alpha = alpha
        self.beta = beta
        self._mean = alpha / (alpha + beta)
        self._variance = (alpha * beta) / ((alpha + beta) ** 2 * (alpha + beta + 1))
    
    def pdf(self, x: float) -> float:
        """Probability density function."""
        if x < 0 or x > 1:
            return 0.0
        if x == 0 and self.alpha < 1:
            return float('inf')
        if x == 1 and self.beta < 1:
            return float('inf')
        if x == 0 or x == 1:
            return 0.0 if self.alpha > 1 and self.beta > 1 else float('inf')
        
        return ((x ** (self.alpha - 1)) * ((1 - x) ** (self.beta - 1)) / 
                _beta_function(self.alpha, self.beta))
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function using regularized incomplete beta."""
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        return self._incomplete_beta(self.alpha, self.beta, x)
    
    def _incomplete_beta(self, a: float, b: float, x: float) -> float:
        """Calculate regularized incomplete beta function."""
        if x < 0 or x > 1:
            raise ValueError("x must be between 0 and 1")
        if x == 0:
            return 0.0
        if x == 1:
            return 1.0
        
        # Use symmetry relation
        if x > (a + 1) / (a + b + 2):
            return 1 - self._incomplete_beta(b, a, 1 - x)
        
        # Continued fraction expansion
        qab = a + b
        qap = a + 1
        qam = a - 1
        c = 1.0
        d = 1.0 - qab * x / qap
        if abs(d) < 1e-300:
            d = 1e-300
        d = 1.0 / d
        h = d
        
        for m in range(1, 200):
            m2 = 2 * m
            aa = m * (b - m) * x / ((qam + m2) * (a + m2))
            d = 1.0 + aa * d
            if abs(d) < 1e-300:
                d = 1e-300
            c = 1.0 + aa / c
            if abs(c) < 1e-300:
                c = 1e-300
            d = 1.0 / d
            h *= d * c
            aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
            d = 1.0 + aa * d
            if abs(d) < 1e-300:
                d = 1e-300
            c = 1.0 + aa / c
            if abs(c) < 1e-300:
                c = 1e-300
            d = 1.0 / d
            delta = d * c
            h *= delta
            if abs(delta - 1) < 1e-10:
                break
        
        # Use log to avoid overflow for large parameters
        log_front = a * math.log(x) + b * math.log(1 - x) - math.lgamma(a) - math.lgamma(b) + math.lgamma(a + b)
        front = math.exp(log_front)
        return front * h / a
    
    def quantile(self, p: float) -> float:
        """Inverse CDF using Newton-Raphson."""
        if not 0 <= p <= 1:
            raise ValueError("p must be between 0 and 1")
        
        # Initial approximation
        x = self._mean
        
        # Newton-Raphson refinement
        for _ in range(50):
            fx = self.cdf(x) - p
            fpx = self.pdf(x)
            if fpx == 0 or not math.isfinite(fpx):
                break
            x_new = x - fx / fpx
            if x_new <= 0:
                x_new = 0.001
            elif x_new >= 1:
                x_new = 0.999
            if abs(x_new - x) < 1e-10:
                break
            x = x_new
        
        return x
    
    def sample(self, n: int = 1) -> List[float]:
        """Generate random samples using transformation method."""
        samples = []
        for _ in range(n):
            # Use gamma distribution transformation
            x = _gamma_sample(self.alpha, 1)
            y = _gamma_sample(self.beta, 1)
            samples.append(x / (x + y))
        return samples
    
    def _calculate_mean(self) -> float:
        return self.alpha / (self.alpha + self.beta)
    
    def _calculate_variance(self) -> float:
        return (self.alpha * self.beta) / ((self.alpha + self.beta) ** 2 * (self.alpha + self.beta + 1))


def _gamma_sample(shape: float, scale: float = 1.0) -> float:
    """Generate a random sample from gamma distribution using Marsaglia and Tsang's method."""
    if shape < 1:
        # For shape < 1, use transformation
        return _gamma_sample(shape + 1, scale) * (random.random() ** (1 / shape))
    
    d = shape - 1 / 3
    c = 1 / math.sqrt(9 * d)
    
    while True:
        while True:
            x = NormalDistribution(0, 1).sample_one()
            v = 1 + c * x
            if v > 0:
                break
        v = v ** 3
        u = random.random()
        
        if u < 1 - 0.0331 * (x ** 2) ** 2:
            return d * v * scale
        if math.log(u) < 0.5 * x ** 2 + d * (1 - v + math.log(v)):
            return d * v * scale


# ============================================================================
# Gamma Distribution
# ============================================================================

class GammaDistribution(Distribution):
    """
    Gamma distribution.
    
    Parameters:
        shape: Shape parameter (k or alpha)
        scale: Scale parameter (theta)
    """
    
    def __init__(self, shape: float, scale: float = 1.0):
        if shape <= 0 or scale <= 0:
            raise ValueError("Shape and scale must be positive")
        super().__init__()
        self.shape = shape
        self.scale = scale
        self._mean = shape * scale
        self._variance = shape * (scale ** 2)
    
    def pdf(self, x: float) -> float:
        """Probability density function."""
        if x < 0:
            return 0.0
        return ((x ** (self.shape - 1)) * math.exp(-x / self.scale) / 
                (_gamma_function(self.shape) * (self.scale ** self.shape)))
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        if x <= 0:
            return 0.0
        return _regularized_incomplete_gamma(self.shape, x / self.scale)
    
    def quantile(self, p: float) -> float:
        """Inverse CDF using Newton-Raphson."""
        if not 0 <= p <= 1:
            raise ValueError("p must be between 0 and 1")
        
        # Initial approximation
        x = self._mean
        
        # Newton-Raphson refinement
        for _ in range(50):
            fx = self.cdf(x) - p
            fpx = self.pdf(x)
            if fpx == 0:
                break
            x_new = x - fx / fpx
            if x_new <= 0:
                x_new = 0.001
            if abs(x_new - x) < 1e-10:
                break
            x = x_new
        
        return x
    
    def sample(self, n: int = 1) -> List[float]:
        """Generate random samples."""
        return [_gamma_sample(self.shape, self.scale) for _ in range(n)]
    
    def _calculate_mean(self) -> float:
        return self.shape * self.scale
    
    def _calculate_variance(self) -> float:
        return self.shape * (self.scale ** 2)


# ============================================================================
# F-Distribution
# ============================================================================

class FDistribution(Distribution):
    """
    F-distribution.
    
    Parameters:
        df1: Degrees of freedom for numerator
        df2: Degrees of freedom for denominator
    """
    
    def __init__(self, df1: int, df2: int):
        if df1 <= 0 or df2 <= 0:
            raise ValueError("Degrees of freedom must be positive")
        super().__init__()
        self.df1 = df1
        self.df2 = df2
        if df2 > 2:
            self._mean = df2 / (df2 - 2)
        else:
            self._mean = float('nan')
        if df2 > 4:
            self._variance = (2 * df2 ** 2 * (df1 + df2 - 2)) / (df1 * (df2 - 2) ** 2 * (df2 - 4))
        else:
            self._variance = float('nan')
    
    def pdf(self, x: float) -> float:
        """Probability density function."""
        if x <= 0:
            return 0.0
        d1, d2 = self.df1, self.df2
        return ((d1 / d2) ** (d1 / 2) * 
                (x ** ((d1 / 2) - 1)) * 
                ((1 + (d1 / d2) * x) ** (-(d1 + d2) / 2)) / 
                _beta_function(d1 / 2, d2 / 2))
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        if x <= 0:
            return 0.0
        # F CDF can be expressed using regularized incomplete beta
        d1, d2 = self.df1, self.df2
        t = (d1 * x) / (d1 * x + d2)
        return BetaDistribution(d1 / 2, d2 / 2).cdf(t)
    
    def quantile(self, p: float) -> float:
        """Inverse CDF."""
        if not 0 <= p <= 1:
            raise ValueError("p must be between 0 and 1")
        
        # Use beta distribution quantile
        beta_q = BetaDistribution(self.df1 / 2, self.df2 / 2).quantile(p)
        return (beta_q * self.df2) / ((1 - beta_q) * self.df1)
    
    def sample(self, n: int = 1) -> List[float]:
        """Generate random samples."""
        samples = []
        chi1 = ChiSquareDistribution(self.df1)
        chi2 = ChiSquareDistribution(self.df2)
        for _ in range(n):
            x1 = chi1.sample_one()
            x2 = chi2.sample_one()
            samples.append((x1 / self.df1) / (x2 / self.df2))
        return samples
    
    def _calculate_mean(self) -> float:
        if self.df2 > 2:
            return self.df2 / (self.df2 - 2)
        return float('nan')
    
    def _calculate_variance(self) -> float:
        if self.df2 > 4:
            return (2 * self.df2 ** 2 * (self.df1 + self.df2 - 2)) / \
                   (self.df1 * (self.df2 - 2) ** 2 * (self.df2 - 4))
        return float('nan')


# ============================================================================
# Weibull Distribution
# ============================================================================

class WeibullDistribution(Distribution):
    """
    Weibull distribution.
    
    Parameters:
        shape: Shape parameter (k)
        scale: Scale parameter (lambda)
    """
    
    def __init__(self, shape: float, scale: float = 1.0):
        if shape <= 0 or scale <= 0:
            raise ValueError("Shape and scale must be positive")
        super().__init__()
        self.shape = shape
        self.scale = scale
        self._mean = scale * _gamma_function(1 + 1 / shape)
        self._variance = (scale ** 2) * (_gamma_function(1 + 2 / shape) - _gamma_function(1 + 1 / shape) ** 2)
    
    def pdf(self, x: float) -> float:
        """Probability density function."""
        if x < 0:
            return 0.0
        if x == 0:
            return 0.0 if self.shape > 1 else float('inf')
        return (self.shape / self.scale) * ((x / self.scale) ** (self.shape - 1)) * math.exp(-(x / self.scale) ** self.shape)
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        if x < 0:
            return 0.0
        return 1 - math.exp(-(x / self.scale) ** self.shape)
    
    def quantile(self, p: float) -> float:
        """Inverse CDF."""
        if not 0 <= p < 1:
            raise ValueError("p must be between 0 and 1 (exclusive of 1)")
        return self.scale * ((-math.log(1 - p)) ** (1 / self.shape))
    
    def sample(self, n: int = 1) -> List[float]:
        """Generate random samples using inverse transform."""
        samples = []
        for _ in range(n):
            u = random.random()
            while u == 0 or u == 1:
                u = random.random()
            samples.append(self.scale * ((-math.log(1 - u)) ** (1 / self.shape)))
        return samples
    
    def _calculate_mean(self) -> float:
        return self.scale * _gamma_function(1 + 1 / self.shape)
    
    def _calculate_variance(self) -> float:
        return (self.scale ** 2) * (_gamma_function(1 + 2 / self.shape) - _gamma_function(1 + 1 / self.shape) ** 2)


# ============================================================================
# Log-Normal Distribution
# ============================================================================

class LogNormalDistribution(Distribution):
    """
    Log-normal distribution.
    If X ~ LogNormal(mu, sigma), then log(X) ~ Normal(mu, sigma).
    
    Parameters:
        mu: Mean of the logarithm
        sigma: Standard deviation of the logarithm
    """
    
    def __init__(self, mu: float = 0.0, sigma: float = 1.0):
        if sigma <= 0:
            raise ValueError("Sigma must be positive")
        super().__init__()
        self.mu = mu
        self.sigma = sigma
        self._mean = math.exp(mu + sigma ** 2 / 2)
        self._variance = (math.exp(sigma ** 2) - 1) * math.exp(2 * mu + sigma ** 2)
    
    def pdf(self, x: float) -> float:
        """Probability density function."""
        if x <= 0:
            return 0.0
        return (1 / (x * self.sigma * math.sqrt(2 * math.pi))) * \
               math.exp(-((math.log(x) - self.mu) ** 2) / (2 * self.sigma ** 2))
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        if x <= 0:
            return 0.0
        return 0.5 * (1 + _erf((math.log(x) - self.mu) / (self.sigma * math.sqrt(2))))
    
    def quantile(self, p: float) -> float:
        """Inverse CDF."""
        if not 0 <= p <= 1:
            raise ValueError("p must be between 0 and 1")
        return math.exp(self.mu + self.sigma * _inverse_normal_cdf(p))
    
    def sample(self, n: int = 1) -> List[float]:
        """Generate random samples."""
        normal = NormalDistribution(self.mu, self.sigma)
        return [math.exp(normal.sample_one()) for _ in range(n)]
    
    def _calculate_mean(self) -> float:
        return math.exp(self.mu + self.sigma ** 2 / 2)
    
    def _calculate_variance(self) -> float:
        return (math.exp(self.sigma ** 2) - 1) * math.exp(2 * self.mu + self.sigma ** 2)


# ============================================================================
# Convenience Functions
# ============================================================================

def normal_pdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """Calculate normal distribution PDF."""
    return NormalDistribution(mu, sigma).pdf(x)


def normal_cdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """Calculate normal distribution CDF."""
    return NormalDistribution(mu, sigma).cdf(x)


def normal_quantile(p: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """Calculate normal distribution quantile (inverse CDF)."""
    return NormalDistribution(mu, sigma).quantile(p)


def normal_sample(mu: float = 0.0, sigma: float = 1.0, n: int = 1) -> List[float]:
    """Generate random samples from normal distribution."""
    return NormalDistribution(mu, sigma).sample(n)


def confidence_interval(mean: float, std: float, n: int, confidence: float = 0.95) -> Tuple[float, float]:
    """
    Calculate confidence interval for a sample mean.
    
    Parameters:
        mean: Sample mean
        std: Sample standard deviation
        n: Sample size
        confidence: Confidence level (default 0.95)
    
    Returns:
        Tuple of (lower, upper) bounds
    """
    if n < 2:
        raise ValueError("Sample size must be at least 2")
    
    alpha = 1 - confidence
    # Use t-distribution for small samples, normal for large
    if n >= 30:
        z = NormalDistribution(0, 1).quantile(1 - alpha / 2)
        margin = z * std / math.sqrt(n)
    else:
        t = StudentTDistribution(n - 1).quantile(1 - alpha / 2)
        margin = t * std / math.sqrt(n)
    
    return (mean - margin, mean + margin)


def z_score(x: float, mu: float, sigma: float) -> float:
    """Calculate z-score."""
    return (x - mu) / sigma


def p_value_one_tailed(z: float) -> float:
    """Calculate one-tailed p-value for z-score."""
    return 1 - NormalDistribution(0, 1).cdf(z)


def p_value_two_tailed(z: float) -> float:
    """Calculate two-tailed p-value for z-score."""
    return 2 * (1 - NormalDistribution(0, 1).cdf(abs(z)))


# ============================================================================
# Statistical Tests
# ============================================================================

def z_test(sample_mean: float, population_mean: float, population_std: float, n: int) -> dict:
    """
    Perform a one-sample z-test.
    
    Parameters:
        sample_mean: Sample mean
        population_mean: Hypothesized population mean
        population_std: Population standard deviation (known)
        n: Sample size
    
    Returns:
        Dictionary with z-score and p-values
    """
    z = (sample_mean - population_mean) / (population_std / math.sqrt(n))
    return {
        'z_score': z,
        'p_value_one_tailed': p_value_one_tailed(z),
        'p_value_two_tailed': p_value_two_tailed(z)
    }


def t_test(sample_mean: float, sample_std: float, population_mean: float, n: int) -> dict:
    """
    Perform a one-sample t-test.
    
    Parameters:
        sample_mean: Sample mean
        sample_std: Sample standard deviation
        population_mean: Hypothesized population mean
        n: Sample size
    
    Returns:
        Dictionary with t-statistic and p-values
    """
    t = (sample_mean - population_mean) / (sample_std / math.sqrt(n))
    t_dist = StudentTDistribution(n - 1)
    return {
        't_statistic': t,
        'p_value_one_tailed': 1 - t_dist.cdf(t),
        'p_value_two_tailed': 2 * (1 - t_dist.cdf(abs(t)))
    }


# ============================================================================
# Export Classes and Functions
# ============================================================================

__all__ = [
    # Distribution classes
    'Distribution',
    'NormalDistribution',
    'UniformDistribution',
    'ExponentialDistribution',
    'PoissonDistribution',
    'BinomialDistribution',
    'GeometricDistribution',
    'ChiSquareDistribution',
    'StudentTDistribution',
    'BetaDistribution',
    'GammaDistribution',
    'FDistribution',
    'WeibullDistribution',
    'LogNormalDistribution',
    # Convenience functions
    'normal_pdf',
    'normal_cdf',
    'normal_quantile',
    'normal_sample',
    'confidence_interval',
    'z_score',
    'p_value_one_tailed',
    'p_value_two_tailed',
    # Statistical tests
    'z_test',
    't_test',
    # Helper functions
    '_factorial',
    '_gamma_function',
    '_beta_function',
    '_erf',
]


if __name__ == '__main__':
    # Quick demo
    print("Probability Distribution Utilities Demo")
    print("=" * 50)
    
    # Normal distribution
    normal = NormalDistribution(0, 1)
    print(f"\nNormal(0, 1):")
    print(f"  Mean: {normal.mean}")
    print(f"  Variance: {normal.variance}")
    print(f"  PDF(0): {normal.pdf(0):.6f}")
    print(f"  CDF(0): {normal.cdf(0):.6f}")
    print(f"  Quantile(0.975): {normal.quantile(0.975):.6f}")
    print(f"  95% CI: {normal.interval(0.95)}")
    
    # Binomial distribution
    binom = BinomialDistribution(10, 0.5)
    print(f"\nBinomial(10, 0.5):")
    print(f"  Mean: {binom.mean}")
    print(f"  Variance: {binom.variance}")
    print(f"  PMF(5): {binom.pmf(5):.6f}")
    print(f"  CDF(5): {binom.cdf(5):.6f}")
    print(f"  Samples: {binom.sample(5)}")
    
    # Exponential distribution
    exp = ExponentialDistribution(0.5)
    print(f"\nExponential(0.5):")
    print(f"  Mean: {exp.mean}")
    print(f"  PDF(2): {exp.pdf(2):.6f}")
    print(f"  CDF(2): {exp.cdf(2):.6f}")
    
    # T-test example
    print(f"\nT-test example:")
    result = t_test(sample_mean=105, sample_std=15, population_mean=100, n=25)
    print(f"  t-statistic: {result['t_statistic']:.4f}")
    print(f"  p-value (two-tailed): {result['p_value_two_tailed']:.4f}")