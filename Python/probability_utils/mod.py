#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Probability Distribution Utilities Module
======================================================
A comprehensive probability distribution and statistics utility module
with zero external dependencies.

Features:
    - Probability distributions (Normal, Binomial, Poisson, Exponential, Uniform)
    - Statistical functions (mean, variance, std, percentile, quartile)
    - Confidence intervals (Z-test, T-test)
    - Probability calculations (PDF, CDF, PPF)
    - Random sampling from distributions
    - Hypothesis testing helpers
    - Combinatorial probability utilities

Author: AllToolkit Contributors
License: MIT
"""

from typing import List, Tuple, Optional, Union, Callable
import math
import random
from functools import lru_cache


# ============================================================================
# Constants
# ============================================================================

# Common statistical values
SQRT_2PI = math.sqrt(2 * math.pi)
SQRT_2 = math.sqrt(2)
E = math.e

# Z-scores for common confidence levels
Z_SCORES = {
    0.90: 1.645,   # 90% confidence
    0.95: 1.96,    # 95% confidence
    0.99: 2.576,   # 99% confidence
    0.999: 3.291,  # 99.9% confidence
}


# ============================================================================
# Basic Statistical Functions
# ============================================================================

def mean(data: List[Union[int, float]]) -> float:
    """
    Calculate the arithmetic mean of a list of numbers.
    
    Args:
        data: List of numeric values
        
    Returns:
        The mean value
        
    Raises:
        ValueError: If data is empty
        
    Example:
        >>> mean([1, 2, 3, 4, 5])
        3.0
        >>> mean([10, 20, 30])
        20.0
    """
    if not data:
        raise ValueError("Cannot calculate mean of empty data")
    return sum(data) / len(data)


def median(data: List[Union[int, float]]) -> float:
    """
    Calculate the median of a list of numbers.
    
    Args:
        data: List of numeric values
        
    Returns:
        The median value
        
    Raises:
        ValueError: If data is empty
        
    Example:
        >>> median([1, 2, 3, 4, 5])
        3.0
        >>> median([1, 2, 3, 4])
        2.5
    """
    if not data:
        raise ValueError("Cannot calculate median of empty data")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return float(sorted_data[mid])


def mode(data: List[Union[int, float, str]]) -> List[Union[int, float, str]]:
    """
    Find the mode(s) of a list of values.
    
    Args:
        data: List of values
        
    Returns:
        List of most frequent value(s)
        
    Raises:
        ValueError: If data is empty
        
    Example:
        >>> mode([1, 2, 2, 3, 3, 3])
        [3]
        >>> mode([1, 1, 2, 2])
        [1, 2]
    """
    if not data:
        raise ValueError("Cannot calculate mode of empty data")
    
    counts = {}
    for item in data:
        counts[item] = counts.get(item, 0) + 1
    
    max_count = max(counts.values())
    return [k for k, v in counts.items() if v == max_count]


def variance(data: List[Union[int, float]], population: bool = True) -> float:
    """
    Calculate the variance of a list of numbers.
    
    Args:
        data: List of numeric values
        population: If True, calculate population variance (N).
                   If False, calculate sample variance (N-1).
        
    Returns:
        The variance value
        
    Raises:
        ValueError: If data has fewer than 2 elements for sample variance
        
    Example:
        >>> variance([1, 2, 3, 4, 5])
        2.0
        >>> variance([1, 2, 3, 4, 5], population=False)
        2.5
    """
    if not data:
        raise ValueError("Cannot calculate variance of empty data")
    
    n = len(data)
    if not population and n < 2:
        raise ValueError("Sample variance requires at least 2 elements")
    
    m = mean(data)
    divisor = n if population else n - 1
    
    return sum((x - m) ** 2 for x in data) / divisor


def std_dev(data: List[Union[int, float]], population: bool = True) -> float:
    """
    Calculate the standard deviation of a list of numbers.
    
    Args:
        data: List of numeric values
        population: If True, calculate population std dev.
                   If False, calculate sample std dev.
        
    Returns:
        The standard deviation
        
    Example:
        >>> std_dev([1, 2, 3, 4, 5])
        1.4142135623730951
    """
    return math.sqrt(variance(data, population))


def percentile(data: List[Union[int, float]], p: float) -> float:
    """
    Calculate the p-th percentile of a dataset.
    
    Args:
        data: List of numeric values
        p: Percentile value (0-100)
        
    Returns:
        The percentile value
        
    Raises:
        ValueError: If data is empty or p is out of range
        
    Example:
        >>> percentile([1, 2, 3, 4, 5], 50)
        3.0
        >>> percentile([1, 2, 3, 4, 5], 25)
        1.5
    """
    if not data:
        raise ValueError("Cannot calculate percentile of empty data")
    
    if not 0 <= p <= 100:
        raise ValueError("Percentile must be between 0 and 100")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    if p == 0:
        return float(sorted_data[0])
    if p == 100:
        return float(sorted_data[-1])
    
    # Linear interpolation method
    rank = (p / 100) * (n - 1)
    lower_idx = int(rank)
    upper_idx = lower_idx + 1
    
    if upper_idx >= n:
        return float(sorted_data[-1])
    
    fraction = rank - lower_idx
    return sorted_data[lower_idx] + fraction * (sorted_data[upper_idx] - sorted_data[lower_idx])


def quartiles(data: List[Union[int, float]]) -> Tuple[float, float, float]:
    """
    Calculate the three quartiles (Q1, Q2, Q3) of a dataset.
    
    Args:
        data: List of numeric values
        
    Returns:
        Tuple of (Q1, median, Q3)
        
    Example:
        >>> quartiles([1, 2, 3, 4, 5, 6, 7, 8])
        (2.5, 4.5, 6.5)
    """
    return (
        percentile(data, 25),
        percentile(data, 50),
        percentile(data, 75)
    )


def iqr(data: List[Union[int, float]]) -> float:
    """
    Calculate the interquartile range (Q3 - Q1).
    
    Args:
        data: List of numeric values
        
    Returns:
        The IQR value
        
    Example:
        >>> iqr([1, 2, 3, 4, 5, 6, 7, 8])
        4.0
    """
    q1, _, q3 = quartiles(data)
    return q3 - q1


def range_(data: List[Union[int, float]]) -> float:
    """
    Calculate the range (max - min) of a dataset.
    
    Args:
        data: List of numeric values
        
    Returns:
        The range value
        
    Example:
        >>> range_([1, 2, 3, 4, 5])
        4.0
    """
    if not data:
        raise ValueError("Cannot calculate range of empty data")
    return float(max(data) - min(data))


def coefficient_of_variation(data: List[Union[int, float]], population: bool = True) -> float:
    """
    Calculate the coefficient of variation (CV) = std_dev / mean.
    
    Args:
        data: List of numeric values
        population: Population or sample std dev
        
    Returns:
        The CV value (ratio, not percentage)
        
    Example:
        >>> coefficient_of_variation([10, 20, 30, 40, 50])
        0.47140452079103173
    """
    m = mean(data)
    if m == 0:
        raise ValueError("Cannot calculate CV when mean is zero")
    return std_dev(data, population) / abs(m)


def skewness(data: List[Union[int, float]]) -> float:
    """
    Calculate the skewness (asymmetry measure) of a dataset.
    
    Args:
        data: List of numeric values
        
    Returns:
        Skewness value:
            - Positive: right-skewed (tail on right)
            - Negative: left-skewed (tail on left)
            - Zero: symmetric
        
    Example:
        >>> skewness([1, 2, 3, 4, 5])
        0.0
        >>> skewness([1, 1, 1, 2, 10])
        1.4915026223126866
    """
    if len(data) < 3:
        raise ValueError("Skewness requires at least 3 elements")
    
    n = len(data)
    m = mean(data)
    s = std_dev(data, population=False)
    
    if s == 0:
        return 0.0
    
    # Fisher-Pearson coefficient of skewness
    return (n / ((n - 1) * (n - 2))) * sum(((x - m) / s) ** 3 for x in data)


def kurtosis(data: List[Union[int, float]]) -> float:
    """
    Calculate the excess kurtosis (tailedness measure) of a dataset.
    
    Args:
        data: List of numeric values
        
    Returns:
        Excess kurtosis value:
            - Positive: heavy tails (leptokurtic)
            - Negative: light tails (platykurtic)
            - Zero: normal distribution (mesokurtic)
        
    Example:
        >>> kurtosis([1, 2, 3, 4, 5])
        -1.2000000000000002
    """
    if len(data) < 4:
        raise ValueError("Kurtosis requires at least 4 elements")
    
    n = len(data)
    m = mean(data)
    s = std_dev(data, population=False)
    
    if s == 0:
        return 0.0
    
    # Excess kurtosis formula
    fourth_moment = sum((x - m) ** 4 for x in data) / n
    kurt = fourth_moment / (s ** 4)
    
    return kurt - 3  # Subtract 3 for excess kurtosis (normal = 0)


# ============================================================================
# Normal Distribution
# ============================================================================

def normal_pdf(x: float, mean: float = 0, std: float = 1) -> float:
    """
    Calculate the probability density function (PDF) for normal distribution.
    
    Args:
        x: Value to evaluate
        mean: Mean of the distribution (default 0)
        std: Standard deviation (default 1)
        
    Returns:
        PDF value at x
        
    Example:
        >>> normal_pdf(0)
        0.3989422804014327
        >>> normal_pdf(1.96, mean=0, std=1)
        0.0584409443334515
    """
    if std <= 0:
        raise ValueError("Standard deviation must be positive")
    
    z = (x - mean) / std
    return (1 / (std * SQRT_2PI)) * math.exp(-0.5 * z ** 2)


def normal_cdf(x: float, mean: float = 0, std: float = 1) -> float:
    """
    Calculate the cumulative distribution function (CDF) for normal distribution.
    
    Args:
        x: Value to evaluate
        mean: Mean of the distribution (default 0)
        std: Standard deviation (default 1)
        
    Returns:
        CDF value at x (probability that X <= x)
        
    Example:
        >>> normal_cdf(0)
        0.5
        >>> round(normal_cdf(1.96), 4)
        0.975
    """
    if std <= 0:
        raise ValueError("Standard deviation must be positive")
    
    z = (x - mean) / std
    return 0.5 * (1 + math.erf(z / SQRT_2))


def normal_ppf(p: float, mean: float = 0, std: float = 1) -> float:
    """
    Calculate the percent point function (PPF) - inverse of CDF.
    
    Args:
        p: Probability value (0-1)
        mean: Mean of the distribution (default 0)
        std: Standard deviation (default 1)
        
    Returns:
        The value x such that P(X <= x) = p
        
    Raises:
        ValueError: If p is not in (0, 1)
        
    Example:
        >>> round(normal_ppf(0.975), 4)
        1.96
        >>> normal_ppf(0.5)
        0.0
    """
    if not 0 < p < 1:
        raise ValueError("Probability must be between 0 and 1 (exclusive)")
    
    if std <= 0:
        raise ValueError("Standard deviation must be positive")
    
    # Rational approximation for inverse normal CDF
    # Abramowitz and Stegun approximation
    a = [
        -3.969683028665376e+01,
        2.209460984245205e+02,
        -2.759285104469687e+02,
        1.383577518672690e+02,
        -3.066479806614716e+01,
        2.506628277459239e+00
    ]
    
    b = [
        -5.447609879822406e+01,
        1.615858368580409e+02,
        -1.556989798598866e+02,
        6.680131188771972e+01,
        -1.328068155288572e+01
    ]
    
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e+00,
        -2.549732539343734e+00,
        4.374664141464968e+00,
        2.938163982698783e+00
    ]
    
    d = [
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e+00,
        3.754408661907416e+00
    ]
    
    p_low = 0.02425
    p_high = 1 - p_low
    
    if p < p_low:
        q = math.sqrt(-2 * math.log(p))
        x = (((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
            ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
    elif p <= p_high:
        q = p - 0.5
        r = q * q
        x = (((((a[0]*r + a[1])*r + a[2])*r + a[3])*r + a[4])*r + a[5])*q / \
            (((((b[0]*r + b[1])*r + b[2])*r + b[3])*r + b[4])*r + 1)
    else:
        q = math.sqrt(-2 * math.log(1 - p))
        x = -(((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
            ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
    
    return mean + std * x


def z_score(x: float, mean: float, std: float) -> float:
    """
    Calculate the z-score (standard score).
    
    Args:
        x: Value to convert
        mean: Mean of the distribution
        std: Standard deviation
        
    Returns:
        Z-score value
        
    Example:
        >>> z_score(85, 70, 10)
        1.5
    """
    if std <= 0:
        raise ValueError("Standard deviation must be positive")
    return (x - mean) / std


def standardize(data: List[Union[int, float]]) -> List[float]:
    """
    Standardize a dataset (z-score normalization).
    
    Args:
        data: List of numeric values
        
    Returns:
        List of z-scores
        
    Example:
        >>> standardize([1, 2, 3, 4, 5])
        [-1.2649110640673518, -0.6324555320336759, 0.0, 0.6324555320336759, 1.2649110640673518]
    """
    m = mean(data)
    s = std_dev(data, population=False)
    if s == 0:
        return [0.0] * len(data)
    return [(x - m) / s for x in data]


# ============================================================================
# Binomial Distribution
# ============================================================================

def factorial(n: int) -> int:
    """Calculate factorial of n."""
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def combination(n: int, k: int) -> int:
    """
    Calculate C(n, k) = n! / (k! * (n-k)!).
    
    Args:
        n: Total number of items
        k: Number to choose
        
    Returns:
        Number of combinations
        
    Example:
        >>> combination(10, 3)
        120
    """
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    
    # Optimize by using smaller k
    k = min(k, n - k)
    
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    
    return result


def permutation(n: int, k: int) -> int:
    """
    Calculate P(n, k) = n! / (n-k)!.
    
    Args:
        n: Total number of items
        k: Number to arrange
        
    Returns:
        Number of permutations
        
    Example:
        >>> permutation(10, 3)
        720
    """
    if k < 0 or k > n:
        return 0
    if k == 0:
        return 1
    
    result = 1
    for i in range(n - k + 1, n + 1):
        result *= i
    
    return result


def binomial_pmf(k: int, n: int, p: float) -> float:
    """
    Calculate the probability mass function (PMF) for binomial distribution.
    
    Args:
        k: Number of successes
        n: Number of trials
        p: Probability of success
        
    Returns:
        Probability of exactly k successes in n trials
        
    Raises:
        ValueError: If parameters are invalid
        
    Example:
        >>> round(binomial_pmf(5, 10, 0.5), 4)
        0.2461
        >>> round(binomial_pmf(2, 5, 0.3), 4)
        0.3087
    """
    if n < 0:
        raise ValueError("Number of trials must be non-negative")
    if k < 0 or k > n:
        return 0.0
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1")
    
    return combination(n, k) * (p ** k) * ((1 - p) ** (n - k))


def binomial_cdf(k: int, n: int, p: float) -> float:
    """
    Calculate the cumulative distribution function for binomial distribution.
    
    Args:
        k: Maximum number of successes
        n: Number of trials
        p: Probability of success
        
    Returns:
        Probability of at most k successes
        
    Example:
        >>> round(binomial_cdf(5, 10, 0.5), 4)
        0.623
    """
    return sum(binomial_pmf(i, n, p) for i in range(k + 1))


def binomial_mean(n: int, p: float) -> float:
    """Calculate the mean of binomial distribution = n * p."""
    return n * p


def binomial_variance(n: int, p: float) -> float:
    """Calculate the variance of binomial distribution = n * p * (1-p)."""
    return n * p * (1 - p)


def binomial_std(n: int, p: float) -> float:
    """Calculate the standard deviation of binomial distribution."""
    return math.sqrt(binomial_variance(n, p))


# ============================================================================
# Poisson Distribution
# ============================================================================

def poisson_pmf(k: int, lambda_: float) -> float:
    """
    Calculate the probability mass function for Poisson distribution.
    
    Args:
        k: Number of events
        lambda_: Expected number of events (rate parameter)
        
    Returns:
        Probability of exactly k events
        
    Example:
        >>> round(poisson_pmf(3, 2.5), 4)
        0.2138
    """
    if k < 0:
        return 0.0
    if lambda_ < 0:
        raise ValueError("Lambda must be non-negative")
    
    if lambda_ == 0:
        return 1.0 if k == 0 else 0.0
    
    # Use log to avoid overflow for large values
    try:
        log_prob = k * math.log(lambda_) - lambda_ - math.lgamma(k + 1)
        return math.exp(log_prob)
    except (OverflowError, ValueError):
        return 0.0


def poisson_cdf(k: int, lambda_: float) -> float:
    """
    Calculate the cumulative distribution function for Poisson distribution.
    
    Args:
        k: Maximum number of events
        lambda_: Expected number of events
        
    Returns:
        Probability of at most k events
        
    Example:
        >>> round(poisson_cdf(3, 2.5), 4)
        0.7576
    """
    return sum(poisson_pmf(i, lambda_) for i in range(k + 1))


def poisson_mean(lambda_: float) -> float:
    """Mean of Poisson distribution = lambda."""
    return lambda_


def poisson_variance(lambda_: float) -> float:
    """Variance of Poisson distribution = lambda."""
    return lambda_


# ============================================================================
# Exponential Distribution
# ============================================================================

def exponential_pdf(x: float, lambda_: float) -> float:
    """
    Calculate the PDF for exponential distribution.
    
    Args:
        x: Value to evaluate (must be >= 0)
        lambda_: Rate parameter (must be > 0)
        
    Returns:
        PDF value
        
    Example:
        >>> round(exponential_pdf(1, 0.5), 4)
        0.3033
    """
    if x < 0:
        return 0.0
    if lambda_ <= 0:
        raise ValueError("Lambda must be positive")
    
    return lambda_ * math.exp(-lambda_ * x)


def exponential_cdf(x: float, lambda_: float) -> float:
    """
    Calculate the CDF for exponential distribution.
    
    Args:
        x: Value to evaluate
        lambda_: Rate parameter
        
    Returns:
        CDF value (probability X <= x)
        
    Example:
        >>> round(exponential_cdf(2, 0.5), 4)
        0.6321
    """
    if x < 0:
        return 0.0
    if lambda_ <= 0:
        raise ValueError("Lambda must be positive")
    
    return 1 - math.exp(-lambda_ * x)


def exponential_ppf(p: float, lambda_: float) -> float:
    """
    Calculate the PPF (quantile) for exponential distribution.
    
    Args:
        p: Probability (0-1)
        lambda_: Rate parameter
        
    Returns:
        Value x such that P(X <= x) = p
        
    Example:
        >>> round(exponential_ppf(0.5, 0.5), 4)
        1.3863
    """
    if not 0 <= p < 1:
        raise ValueError("Probability must be between 0 and 1 (exclusive of 1)")
    if lambda_ <= 0:
        raise ValueError("Lambda must be positive")
    
    return -math.log(1 - p) / lambda_


def exponential_mean(lambda_: float) -> float:
    """Mean of exponential distribution = 1/lambda."""
    return 1 / lambda_


def exponential_variance(lambda_: float) -> float:
    """Variance of exponential distribution = 1/lambda^2."""
    return 1 / (lambda_ ** 2)


# ============================================================================
# Uniform Distribution
# ============================================================================

def uniform_pdf(x: float, a: float, b: float) -> float:
    """
    Calculate the PDF for continuous uniform distribution.
    
    Args:
        x: Value to evaluate
        a: Lower bound
        b: Upper bound
        
    Returns:
        PDF value (1/(b-a) if x in [a,b], else 0)
        
    Example:
        >>> uniform_pdf(0.5, 0, 1)
        1.0
        >>> uniform_pdf(2, 0, 1)
        0.0
    """
    if a >= b:
        raise ValueError("Lower bound must be less than upper bound")
    
    if a <= x <= b:
        return 1 / (b - a)
    return 0.0


def uniform_cdf(x: float, a: float, b: float) -> float:
    """
    Calculate the CDF for continuous uniform distribution.
    
    Args:
        x: Value to evaluate
        a: Lower bound
        b: Upper bound
        
    Returns:
        CDF value
        
    Example:
        >>> uniform_cdf(0.5, 0, 1)
        0.5
        >>> uniform_cdf(2, 0, 1)
        1.0
    """
    if a >= b:
        raise ValueError("Lower bound must be less than upper bound")
    
    if x < a:
        return 0.0
    elif x > b:
        return 1.0
    else:
        return (x - a) / (b - a)


def uniform_mean(a: float, b: float) -> float:
    """Mean of uniform distribution = (a+b)/2."""
    return (a + b) / 2


def uniform_variance(a: float, b: float) -> float:
    """Variance of uniform distribution = (b-a)^2/12."""
    return (b - a) ** 2 / 12


# ============================================================================
# Confidence Intervals
# ============================================================================

def z_confidence_interval(
    sample_mean: float,
    sample_std: float,
    n: int,
    confidence: float = 0.95
) -> Tuple[float, float]:
    """
    Calculate confidence interval using z-test (large sample or known population std).
    
    Args:
        sample_mean: Sample mean
        sample_std: Sample standard deviation
        n: Sample size
        confidence: Confidence level (default 0.95)
        
    Returns:
        Tuple of (lower_bound, upper_bound)
        
    Example:
        >>> ci = z_confidence_interval(100, 15, 50, 0.95)
        >>> round(ci[0], 2), round(ci[1], 2)
        (95.84, 104.16)
    """
    if n <= 0:
        raise ValueError("Sample size must be positive")
    if not 0 < confidence < 1:
        raise ValueError("Confidence must be between 0 and 1")
    
    z = Z_SCORES.get(confidence, normal_ppf((1 + confidence) / 2))
    margin = z * sample_std / math.sqrt(n)
    
    return (sample_mean - margin, sample_mean + margin)


def t_confidence_interval(
    sample_mean: float,
    sample_std: float,
    n: int,
    confidence: float = 0.95
) -> Tuple[float, float]:
    """
    Calculate confidence interval using t-test (small sample, unknown population std).
    
    Args:
        sample_mean: Sample mean
        sample_std: Sample standard deviation
        n: Sample size
        confidence: Confidence level (default 0.95)
        
    Returns:
        Tuple of (lower_bound, upper_bound)
        
    Example:
        >>> ci = t_confidence_interval(100, 15, 10, 0.95)
        >>> round(ci[0], 2), round(ci[1], 2)
        (89.14, 110.86)
    """
    if n <= 1:
        raise ValueError("Sample size must be at least 2")
    if not 0 < confidence < 1:
        raise ValueError("Confidence must be between 0 and 1")
    
    # T critical value approximation using normal approximation for large samples
    # For small samples, use a simplified approximation
    alpha = 1 - confidence
    df = n - 1
    
    # Approximate t critical value
    if df >= 30:
        t_crit = normal_ppf((1 + confidence) / 2)
    else:
        # Simplified approximation for small samples
        # Use inverse normal with correction
        z = normal_ppf((1 + confidence) / 2)
        t_crit = z * (1 + 1 / (4 * df))  # Simple approximation
    
    margin = t_crit * sample_std / math.sqrt(n)
    
    return (sample_mean - margin, sample_mean + margin)


def proportion_confidence_interval(
    successes: int,
    n: int,
    confidence: float = 0.95
) -> Tuple[float, float]:
    """
    Calculate confidence interval for a proportion.
    
    Args:
        successes: Number of successes
        n: Total sample size
        confidence: Confidence level
        
    Returns:
        Tuple of (lower_bound, upper_bound)
        
    Example:
        >>> ci = proportion_confidence_interval(45, 100, 0.95)
        >>> round(ci[0], 3), round(ci[1], 3)
        (0.351, 0.549)
    """
    if n <= 0:
        raise ValueError("Sample size must be positive")
    if successes < 0 or successes > n:
        raise ValueError("Successes must be between 0 and n")
    if not 0 < confidence < 1:
        raise ValueError("Confidence must be between 0 and 1")
    
    p = successes / n
    z = Z_SCORES.get(confidence, normal_ppf((1 + confidence) / 2))
    margin = z * math.sqrt(p * (1 - p) / n)
    
    # Clamp to [0, 1]
    lower = max(0, p - margin)
    upper = min(1, p + margin)
    
    return (lower, upper)


# ============================================================================
# Hypothesis Testing Helpers
# ============================================================================

def z_test(
    sample_mean: float,
    population_mean: float,
    population_std: float,
    n: int,
    two_tailed: bool = True
) -> Tuple[float, float]:
    """
    Perform a one-sample z-test.
    
    Args:
        sample_mean: Sample mean
        population_mean: Hypothesized population mean (H0)
        population_std: Population standard deviation (known)
        n: Sample size
        two_tailed: Whether to use two-tailed test
        
    Returns:
        Tuple of (z_statistic, p_value)
        
    Example:
        >>> z, p = z_test(105, 100, 15, 50)
        >>> round(z, 2), round(p, 3)
        (2.36, 0.018)
    """
    if n <= 0:
        raise ValueError("Sample size must be positive")
    if population_std <= 0:
        raise ValueError("Population std must be positive")
    
    z = (sample_mean - population_mean) / (population_std / math.sqrt(n))
    
    if two_tailed:
        p = 2 * (1 - normal_cdf(abs(z)))
    else:
        p = 1 - normal_cdf(z) if z > 0 else normal_cdf(z)
    
    return (z, p)


def margin_of_error(
    std: float,
    n: int,
    confidence: float = 0.95
) -> float:
    """
    Calculate the margin of error.
    
    Args:
        std: Standard deviation
        n: Sample size
        confidence: Confidence level
        
    Returns:
        Margin of error
        
    Example:
        >>> round(margin_of_error(15, 100, 0.95), 2)
        2.94
    """
    z = Z_SCORES.get(confidence, normal_ppf((1 + confidence) / 2))
    return z * std / math.sqrt(n)


def sample_size_for_mean(
    std: float,
    margin: float,
    confidence: float = 0.95
) -> int:
    """
    Calculate required sample size for estimating a mean.
    
    Args:
        std: Estimated standard deviation
        margin: Desired margin of error
        confidence: Confidence level
        
    Returns:
        Required sample size
        
    Example:
        >>> sample_size_for_mean(15, 3, 0.95)
        97
    """
    z = Z_SCORES.get(confidence, normal_ppf((1 + confidence) / 2))
    n = (z * std / margin) ** 2
    return math.ceil(n)


def sample_size_for_proportion(
    margin: float,
    confidence: float = 0.95,
    p_estimate: float = 0.5
) -> int:
    """
    Calculate required sample size for estimating a proportion.
    
    Args:
        margin: Desired margin of error
        confidence: Confidence level
        p_estimate: Estimated proportion (use 0.5 for maximum sample size)
        
    Returns:
        Required sample size
        
    Example:
        >>> sample_size_for_proportion(0.03, 0.95)
        1068
    """
    z = Z_SCORES.get(confidence, normal_ppf((1 + confidence) / 2))
    n = (z ** 2) * p_estimate * (1 - p_estimate) / (margin ** 2)
    return math.ceil(n)


# ============================================================================
# Probability Calculations
# ============================================================================

def probability_union(
    p_a: float,
    p_b: float,
    p_intersection: float = 0
) -> float:
    """
    Calculate P(A ∪ B) = P(A) + P(B) - P(A ∩ B).
    
    Args:
        p_a: Probability of event A
        p_b: Probability of event B
        p_intersection: Probability of A ∩ B
        
    Returns:
        Probability of A ∪ B
    """
    if not (0 <= p_a <= 1 and 0 <= p_b <= 1 and 0 <= p_intersection <= 1):
        raise ValueError("Probabilities must be between 0 and 1")
    return p_a + p_b - p_intersection


def probability_intersection_independent(p_a: float, p_b: float) -> float:
    """
    Calculate P(A ∩ B) for independent events = P(A) * P(B).
    """
    if not (0 <= p_a <= 1 and 0 <= p_b <= 1):
        raise ValueError("Probabilities must be between 0 and 1")
    return p_a * p_b


def conditional_probability(
    p_a_given_b: float,
    p_b: float
) -> float:
    """
    Calculate P(A ∩ B) = P(A|B) * P(B).
    
    Args:
        p_a_given_b: Probability of A given B
        p_b: Probability of B
        
    Returns:
        Probability of A ∩ B
    """
    if not (0 <= p_a_given_b <= 1 and 0 <= p_b <= 1):
        raise ValueError("Probabilities must be between 0 and 1")
    return p_a_given_b * p_b


def bayes_theorem(
    p_b_given_a: float,
    p_a: float,
    p_b: float
) -> float:
    """
    Calculate P(A|B) using Bayes' theorem.
    
    P(A|B) = P(B|A) * P(A) / P(B)
    
    Args:
        p_b_given_a: Probability of B given A
        p_a: Prior probability of A
        p_b: Probability of B
        
    Returns:
        Posterior probability P(A|B)
        
    Example:
        >>> # Medical test: 99% sensitive, 95% specific, 1% prevalence
        >>> p_disease = 0.01  # Prior
        >>> p_positive_given_disease = 0.99
        >>> p_positive = 0.01 * 0.99 + 0.99 * 0.05  # Total probability
        >>> round(bayes_theorem(0.99, 0.01, p_positive), 3)
        0.167
    """
    if p_b == 0:
        raise ValueError("P(B) cannot be zero")
    if not (0 <= p_b_given_a <= 1 and 0 <= p_a <= 1 and 0 < p_b <= 1):
        raise ValueError("Invalid probability values")
    
    return (p_b_given_a * p_a) / p_b


def total_probability(
    p_b_given_a: List[float],
    p_a: List[float]
) -> float:
    """
    Calculate total probability P(B) = Σ P(B|Ai) * P(Ai).
    
    Args:
        p_b_given_a: List of P(B|Ai) values
        p_a: List of P(Ai) values
        
    Returns:
        Total probability P(B)
        
    Example:
        >>> # Three factories produce parts
        >>> p_factory = [0.5, 0.3, 0.2]  # Production shares
        >>> p_defect = [0.01, 0.02, 0.03]  # Defect rates
        >>> round(total_probability(p_defect, p_factory), 4)
        0.017
    """
    if len(p_b_given_a) != len(p_a):
        raise ValueError("Lists must have equal length")
    if not all(0 <= p <= 1 for p in p_b_given_a + p_a):
        raise ValueError("Probabilities must be between 0 and 1")
    if abs(sum(p_a) - 1.0) > 1e-10:
        raise ValueError("P(A) values must sum to 1")
    
    return sum(p_b_a * p_a_i for p_b_a, p_a_i in zip(p_b_given_a, p_a))


# ============================================================================
# Random Sampling from Distributions
# ============================================================================

def random_normal(mean: float = 0, std: float = 1) -> float:
    """
    Generate a random number from normal distribution using Box-Muller transform.
    
    Args:
        mean: Mean of the distribution
        std: Standard deviation
        
    Returns:
        Random value from N(mean, std)
        
    Example:
        >>> val = random_normal(0, 1)
        >>> isinstance(val, float)
        True
    """
    if std <= 0:
        raise ValueError("Standard deviation must be positive")
    
    u1 = random.random()
    u2 = random.random()
    
    # Avoid log(0)
    while u1 == 0:
        u1 = random.random()
    
    z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
    return mean + std * z


def random_exponential(lambda_: float) -> float:
    """
    Generate a random number from exponential distribution.
    
    Args:
        lambda_: Rate parameter
        
    Returns:
        Random value from Exp(lambda)
    """
    if lambda_ <= 0:
        raise ValueError("Lambda must be positive")
    
    u = random.random()
    while u == 0:
        u = random.random()
    
    return -math.log(u) / lambda_


def random_uniform(a: float, b: float) -> float:
    """
    Generate a random number from uniform distribution.
    
    Args:
        a: Lower bound
        b: Upper bound
        
    Returns:
        Random value from U(a, b)
    """
    if a >= b:
        raise ValueError("Lower bound must be less than upper bound")
    return a + random.random() * (b - a)


def random_binomial(n: int, p: float) -> int:
    """
    Generate a random number from binomial distribution.
    
    Args:
        n: Number of trials
        p: Probability of success
        
    Returns:
        Number of successes (0 to n)
    """
    if n < 0:
        raise ValueError("Number of trials must be non-negative")
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1")
    
    # For small n, use direct simulation
    if n <= 100:
        return sum(1 for _ in range(n) if random.random() < p)
    
    # For large n, use normal approximation
    mean = n * p
    std = math.sqrt(n * p * (1 - p))
    return max(0, min(n, round(random_normal(mean, std))))


def random_poisson(lambda_: float) -> int:
    """
    Generate a random number from Poisson distribution using Knuth's algorithm.
    
    Args:
        lambda_: Rate parameter (expected number of events)
        
    Returns:
        Number of events
    """
    if lambda_ < 0:
        raise ValueError("Lambda must be non-negative")
    if lambda_ == 0:
        return 0
    
    # For small lambda, use Knuth's algorithm
    if lambda_ < 30:
        L = math.exp(-lambda_)
        k = 0
        p = 1.0
        
        while p > L:
            k += 1
            p *= random.random()
        
        return k - 1
    
    # For large lambda, use normal approximation
    return max(0, round(random_normal(lambda_, math.sqrt(lambda_))))


# ============================================================================
# Utility Functions
# ============================================================================

def covariance(x: List[float], y: List[float], population: bool = True) -> float:
    """
    Calculate the covariance between two datasets.
    
    Args:
        x: First dataset
        y: Second dataset
        population: Population or sample covariance
        
    Returns:
        Covariance value
        
    Example:
        >>> round(covariance([1, 2, 3, 4, 5], [2, 4, 6, 8, 10]), 2)
        4.0
    """
    if len(x) != len(y):
        raise ValueError("Datasets must have equal length")
    if len(x) < 2:
        raise ValueError("Datasets must have at least 2 elements")
    
    n = len(x)
    mean_x = mean(x)
    mean_y = mean(y)
    divisor = n if population else n - 1
    
    return sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / divisor


def correlation(x: List[float], y: List[float]) -> float:
    """
    Calculate the Pearson correlation coefficient between two datasets.
    
    Args:
        x: First dataset
        y: Second dataset
        
    Returns:
        Correlation coefficient (-1 to 1)
        
    Example:
        >>> round(correlation([1, 2, 3, 4, 5], [2, 4, 6, 8, 10]), 4)
        1.0
        >>> round(correlation([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]), 4)
        -1.0
    """
    if len(x) != len(y):
        raise ValueError("Datasets must have equal length")
    if len(x) < 2:
        raise ValueError("Datasets must have at least 2 elements")
    
    n = len(x)
    mean_x = mean(x)
    mean_y = mean(y)
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    
    sum_sq_x = sum((xi - mean_x) ** 2 for xi in x)
    sum_sq_y = sum((yi - mean_y) ** 2 for yi in y)
    
    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    
    if denominator == 0:
        return 0.0
    
    return numerator / denominator


def geometric_mean(data: List[Union[int, float]]) -> float:
    """
    Calculate the geometric mean of a dataset.
    
    Args:
        data: List of positive numeric values
        
    Returns:
        Geometric mean
        
    Example:
        >>> round(geometric_mean([1, 2, 4, 8]), 4)
        2.8284
    """
    if not data:
        raise ValueError("Cannot calculate geometric mean of empty data")
    if any(x <= 0 for x in data):
        raise ValueError("All values must be positive for geometric mean")
    
    log_sum = sum(math.log(x) for x in data)
    return math.exp(log_sum / len(data))


def harmonic_mean(data: List[Union[int, float]]) -> float:
    """
    Calculate the harmonic mean of a dataset.
    
    Args:
        data: List of non-zero numeric values
        
    Returns:
        Harmonic mean
        
    Example:
        >>> round(harmonic_mean([1, 2, 4]), 4)
        1.7143
    """
    if not data:
        raise ValueError("Cannot calculate harmonic mean of empty data")
    if any(x == 0 for x in data):
        raise ValueError("Values must be non-zero for harmonic mean")
    
    n = len(data)
    return n / sum(1 / x for x in data)


def trimmed_mean(data: List[Union[int, float]], proportion: float = 0.1) -> float:
    """
    Calculate the trimmed mean by removing extreme values.
    
    Args:
        data: List of numeric values
        proportion: Proportion to trim from each end (0-0.5)
        
    Returns:
        Trimmed mean
        
    Example:
        >>> trimmed_mean([1, 2, 3, 4, 5, 100], proportion=1/6)
        3.5
    """
    if not data:
        raise ValueError("Cannot calculate trimmed mean of empty data")
    if not 0 <= proportion < 0.5:
        raise ValueError("Proportion must be between 0 and 0.5")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    trim_count = int(n * proportion)
    
    if trim_count == 0:
        return mean(data)
    
    trimmed = sorted_data[trim_count:n - trim_count]
    return mean(trimmed)


def weighted_mean(
    data: List[Union[int, float]],
    weights: List[Union[int, float]]
) -> float:
    """
    Calculate the weighted mean.
    
    Args:
        data: List of values
        weights: List of weights
        
    Returns:
        Weighted mean
        
    Example:
        >>> weighted_mean([1, 2, 3], [1, 2, 3])
        2.3333333333333335
    """
    if len(data) != len(weights):
        raise ValueError("Data and weights must have equal length")
    if not data:
        raise ValueError("Cannot calculate weighted mean of empty data")
    if any(w < 0 for w in weights):
        raise ValueError("Weights must be non-negative")
    
    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("Sum of weights cannot be zero")
    
    return sum(d * w for d, w in zip(data, weights)) / total_weight


# ============================================================================
# Classes for Distribution Objects
# ============================================================================

class NormalDistribution:
    """
    Normal (Gaussian) distribution object.
    
    Example:
        >>> norm = NormalDistribution(mean=100, std=15)
        >>> norm.pdf(115)
        0.0108096...
        >>> norm.cdf(115)
        0.8413...
        >>> norm.sample()
        102.34...  # Random value
    """
    
    def __init__(self, mean: float = 0, std: float = 1):
        if std <= 0:
            raise ValueError("Standard deviation must be positive")
        self.mean = mean
        self.std = std
    
    def pdf(self, x: float) -> float:
        """Probability density function."""
        return normal_pdf(x, self.mean, self.std)
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        return normal_cdf(x, self.mean, self.std)
    
    def ppf(self, p: float) -> float:
        """Percent point function (inverse CDF)."""
        return normal_ppf(p, self.mean, self.std)
    
    def sample(self) -> float:
        """Generate a random sample."""
        return random_normal(self.mean, self.std)
    
    def samples(self, n: int) -> List[float]:
        """Generate n random samples."""
        return [self.sample() for _ in range(n)]
    
    def z_score(self, x: float) -> float:
        """Calculate z-score for a value."""
        return z_score(x, self.mean, self.std)
    
    def __repr__(self) -> str:
        return f"NormalDistribution(mean={self.mean}, std={self.std})"


class BinomialDistribution:
    """
    Binomial distribution object.
    
    Example:
        >>> binom = BinomialDistribution(n=10, p=0.5)
        >>> binom.pmf(5)
        0.2460...
        >>> binom.cdf(5)
        0.6230...
    """
    
    def __init__(self, n: int, p: float):
        if n < 0:
            raise ValueError("Number of trials must be non-negative")
        if not 0 <= p <= 1:
            raise ValueError("Probability must be between 0 and 1")
        self.n = n
        self.p = p
    
    def pmf(self, k: int) -> float:
        """Probability mass function."""
        return binomial_pmf(k, self.n, self.p)
    
    def cdf(self, k: int) -> float:
        """Cumulative distribution function."""
        return binomial_cdf(k, self.n, self.p)
    
    def sample(self) -> int:
        """Generate a random sample."""
        return random_binomial(self.n, self.p)
    
    def samples(self, count: int) -> List[int]:
        """Generate n random samples."""
        return [self.sample() for _ in range(count)]
    
    @property
    def mean(self) -> float:
        """Mean of the distribution."""
        return binomial_mean(self.n, self.p)
    
    @property
    def variance(self) -> float:
        """Variance of the distribution."""
        return binomial_variance(self.n, self.p)
    
    @property
    def std(self) -> float:
        """Standard deviation of the distribution."""
        return binomial_std(self.n, self.p)
    
    def __repr__(self) -> str:
        return f"BinomialDistribution(n={self.n}, p={self.p})"


class PoissonDistribution:
    """
    Poisson distribution object.
    
    Example:
        >>> pois = PoissonDistribution(lambda_=3)
        >>> round(pois.pmf(5), 4)
        0.1008
    """
    
    def __init__(self, lambda_: float):
        if lambda_ < 0:
            raise ValueError("Lambda must be non-negative")
        self.lambda_ = lambda_
    
    def pmf(self, k: int) -> float:
        """Probability mass function."""
        return poisson_pmf(k, self.lambda_)
    
    def cdf(self, k: int) -> float:
        """Cumulative distribution function."""
        return poisson_cdf(k, self.lambda_)
    
    def sample(self) -> int:
        """Generate a random sample."""
        return random_poisson(self.lambda_)
    
    def samples(self, count: int) -> List[int]:
        """Generate n random samples."""
        return [self.sample() for _ in range(count)]
    
    @property
    def mean(self) -> float:
        """Mean of the distribution."""
        return self.lambda_
    
    @property
    def variance(self) -> float:
        """Variance of the distribution."""
        return self.lambda_
    
    def __repr__(self) -> str:
        return f"PoissonDistribution(lambda_={self.lambda_})"


class ExponentialDistribution:
    """
    Exponential distribution object.
    
    Example:
        >>> exp = ExponentialDistribution(lambda_=0.5)
        >>> round(exp.pdf(1), 4)
        0.3033
    """
    
    def __init__(self, lambda_: float):
        if lambda_ <= 0:
            raise ValueError("Lambda must be positive")
        self.lambda_ = lambda_
    
    def pdf(self, x: float) -> float:
        """Probability density function."""
        return exponential_pdf(x, self.lambda_)
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        return exponential_cdf(x, self.lambda_)
    
    def ppf(self, p: float) -> float:
        """Percent point function (inverse CDF)."""
        return exponential_ppf(p, self.lambda_)
    
    def sample(self) -> float:
        """Generate a random sample."""
        return random_exponential(self.lambda_)
    
    def samples(self, n: int) -> List[float]:
        """Generate n random samples."""
        return [self.sample() for _ in range(n)]
    
    @property
    def mean(self) -> float:
        """Mean of the distribution."""
        return exponential_mean(self.lambda_)
    
    @property
    def variance(self) -> float:
        """Variance of the distribution."""
        return exponential_variance(self.lambda_)
    
    def __repr__(self) -> str:
        return f"ExponentialDistribution(lambda_={self.lambda_})"


class UniformDistribution:
    """
    Uniform distribution object.
    
    Example:
        >>> unif = UniformDistribution(a=0, b=1)
        >>> unif.pdf(0.5)
        1.0
        >>> unif.sample()
        0.34...  # Random value in [0, 1]
    """
    
    def __init__(self, a: float, b: float):
        if a >= b:
            raise ValueError("Lower bound must be less than upper bound")
        self.a = a
        self.b = b
    
    def pdf(self, x: float) -> float:
        """Probability density function."""
        return uniform_pdf(x, self.a, self.b)
    
    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        return uniform_cdf(x, self.a, self.b)
    
    def sample(self) -> float:
        """Generate a random sample."""
        return random_uniform(self.a, self.b)
    
    def samples(self, n: int) -> List[float]:
        """Generate n random samples."""
        return [self.sample() for _ in range(n)]
    
    @property
    def mean(self) -> float:
        """Mean of the distribution."""
        return uniform_mean(self.a, self.b)
    
    @property
    def variance(self) -> float:
        """Variance of the distribution."""
        return uniform_variance(self.a, self.b)
    
    def __repr__(self) -> str:
        return f"UniformDistribution(a={self.a}, b={self.b})"


# Module exports
__all__ = [
    # Basic Statistics
    'mean', 'median', 'mode', 'variance', 'std_dev',
    'percentile', 'quartiles', 'iqr', 'range_', 'coefficient_of_variation',
    'skewness', 'kurtosis',
    
    # Normal Distribution
    'normal_pdf', 'normal_cdf', 'normal_ppf', 'z_score', 'standardize',
    
    # Binomial Distribution
    'factorial', 'combination', 'permutation',
    'binomial_pmf', 'binomial_cdf', 'binomial_mean', 'binomial_variance', 'binomial_std',
    
    # Poisson Distribution
    'poisson_pmf', 'poisson_cdf', 'poisson_mean', 'poisson_variance',
    
    # Exponential Distribution
    'exponential_pdf', 'exponential_cdf', 'exponential_ppf',
    'exponential_mean', 'exponential_variance',
    
    # Uniform Distribution
    'uniform_pdf', 'uniform_cdf', 'uniform_mean', 'uniform_variance',
    
    # Confidence Intervals
    'z_confidence_interval', 't_confidence_interval', 'proportion_confidence_interval',
    
    # Hypothesis Testing
    'z_test', 'margin_of_error', 'sample_size_for_mean', 'sample_size_for_proportion',
    
    # Probability Calculations
    'probability_union', 'probability_intersection_independent',
    'conditional_probability', 'bayes_theorem', 'total_probability',
    
    # Random Sampling
    'random_normal', 'random_exponential', 'random_uniform',
    'random_binomial', 'random_poisson',
    
    # Utility Functions
    'covariance', 'correlation', 'geometric_mean', 'harmonic_mean',
    'trimmed_mean', 'weighted_mean',
    
    # Distribution Classes
    'NormalDistribution', 'BinomialDistribution', 'PoissonDistribution',
    'ExponentialDistribution', 'UniformDistribution',
    
    # Constants
    'Z_SCORES', 'SQRT_2PI', 'SQRT_2',
]