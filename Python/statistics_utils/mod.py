"""
AllToolkit - Python Statistics Utilities

A zero-dependency, production-ready statistical utility module.
Provides descriptive statistics, distribution functions, correlation,
regression, hypothesis testing, normalization, and outlier detection.
Built entirely with Python standard library.

Author: AllToolkit
License: MIT
"""

import math
from typing import List, Tuple, Optional, Dict, Any, Union, Callable
from collections import Counter


class StatisticsError(Exception):
    """Base exception for statistics operations."""
    pass


class EmptyDataError(StatisticsError):
    """Raised when data is empty."""
    pass


class InvalidDataError(StatisticsError):
    """Raised when data contains invalid values."""
    pass


# ============================================================================
# Descriptive Statistics
# ============================================================================

def mean(data: List[float]) -> float:
    """
    Calculate the arithmetic mean.
    
    Args:
        data: List of numeric values
        
    Returns:
        Arithmetic mean of the data
        
    Raises:
        EmptyDataError: If data is empty
    """
    if not data:
        raise EmptyDataError("Cannot calculate mean of empty data")
    return sum(data) / len(data)


def geometric_mean(data: List[float]) -> float:
    """
    Calculate the geometric mean.
    
    Args:
        data: List of positive numeric values
        
    Returns:
        Geometric mean of the data
        
    Raises:
        EmptyDataError: If data is empty
        InvalidDataError: If data contains non-positive values
    """
    if not data:
        raise EmptyDataError("Cannot calculate geometric mean of empty data")
    if any(x <= 0 for x in data):
        raise InvalidDataError("Geometric mean requires all positive values")
    
    log_sum = sum(math.log(x) for x in data)
    return math.exp(log_sum / len(data))


def harmonic_mean(data: List[float]) -> float:
    """
    Calculate the harmonic mean.
    
    Args:
        data: List of positive numeric values
        
    Returns:
        Harmonic mean of the data
        
    Raises:
        EmptyDataError: If data is empty
        InvalidDataError: If data contains non-positive values
    """
    if not data:
        raise EmptyDataError("Cannot calculate harmonic mean of empty data")
    if any(x <= 0 for x in data):
        raise InvalidDataError("Harmonic mean requires all positive values")
    
    return len(data) / sum(1/x for x in data)


def median(data: List[float]) -> float:
    """
    Calculate the median (middle value).
    
    Args:
        data: List of numeric values
        
    Returns:
        Median of the data
    """
    if not data:
        raise EmptyDataError("Cannot calculate median of empty data")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    else:
        return sorted_data[mid]


def mode(data: List[float]) -> List[float]:
    """
    Find the mode(s) - most frequently occurring value(s).
    
    Args:
        data: List of numeric values
        
    Returns:
        List of mode values (can be multiple if tied)
    """
    if not data:
        raise EmptyDataError("Cannot calculate mode of empty data")
    
    counter = Counter(data)
    max_count = max(counter.values())
    return [x for x, count in counter.items() if count == max_count]


def variance(data: List[float], population: bool = False) -> float:
    """
    Calculate the variance.
    
    Args:
        data: List of numeric values
        population: If True, calculate population variance (divide by N)
                   If False, calculate sample variance (divide by N-1)
                   
    Returns:
        Variance of the data
        
    Raises:
        EmptyDataError: If data is empty
        ValueError: If sample variance with only one data point
    """
    if not data:
        raise EmptyDataError("Cannot calculate variance of empty data")
    
    n = len(data)
    if not population and n < 2:
        raise ValueError("Sample variance requires at least 2 data points")
    
    m = mean(data)
    squared_diff_sum = sum((x - m) ** 2 for x in data)
    
    if population:
        return squared_diff_sum / n
    else:
        return squared_diff_sum / (n - 1)


def std_dev(data: List[float], population: bool = False) -> float:
    """
    Calculate the standard deviation.
    
    Args:
        data: List of numeric values
        population: If True, calculate population std dev
        
    Returns:
        Standard deviation of the data
    """
    return math.sqrt(variance(data, population))


def quartiles(data: List[float]) -> Tuple[float, float, float]:
    """
    Calculate Q1, Q2 (median), and Q3 quartiles.
    
    Args:
        data: List of numeric values
        
    Returns:
        Tuple of (Q1, Q2, Q3)
    """
    if not data:
        raise EmptyDataError("Cannot calculate quartiles of empty data")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    q2 = median(sorted_data)
    
    # Q1: median of lower half
    lower_half = sorted_data[:n // 2]
    q1 = median(lower_half) if lower_half else sorted_data[0]
    
    # Q3: median of upper half
    if n % 2 == 0:
        upper_half = sorted_data[n // 2:]
    else:
        upper_half = sorted_data[n // 2 + 1:]
    q3 = median(upper_half) if upper_half else sorted_data[-1]
    
    return (q1, q2, q3)


def iqr(data: List[float]) -> float:
    """
    Calculate the interquartile range (IQR = Q3 - Q1).
    
    Args:
        data: List of numeric values
        
    Returns:
        Interquartile range
    """
    q1, _, q3 = quartiles(data)
    return q3 - q1


def percentile(data: List[float], p: float) -> float:
    """
    Calculate the p-th percentile.
    
    Args:
        data: List of numeric values
        p: Percentile value (0-100)
        
    Returns:
        The p-th percentile value
    """
    if not data:
        raise EmptyDataError("Cannot calculate percentile of empty data")
    if not 0 <= p <= 100:
        raise ValueError("Percentile must be between 0 and 100")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    # Use linear interpolation
    k = (n - 1) * p / 100
    f = math.floor(k)
    c = math.ceil(k)
    
    if f == c:
        return sorted_data[int(k)]
    
    return sorted_data[int(f)] * (c - k) + sorted_data[int(c)] * (k - f)


def range_value(data: List[float]) -> float:
    """
    Calculate the range (max - min).
    
    Args:
        data: List of numeric values
        
    Returns:
        Range of the data
    """
    if not data:
        raise EmptyDataError("Cannot calculate range of empty data")
    return max(data) - min(data)


def coefficient_of_variation(data: List[float]) -> float:
    """
    Calculate the coefficient of variation (CV = std_dev / mean).
    
    Args:
        data: List of numeric values
        
    Returns:
        Coefficient of variation
    """
    m = mean(data)
    if m == 0:
        raise InvalidDataError("Cannot calculate CV when mean is zero")
    return std_dev(data) / abs(m)


def skewness(data: List[float]) -> float:
    """
    Calculate the skewness (measure of asymmetry).
    
    Args:
        data: List of numeric values
        
    Returns:
        Skewness value (positive = right skewed, negative = left skewed)
    """
    if len(data) < 3:
        raise ValueError("Skewness requires at least 3 data points")
    
    n = len(data)
    m = mean(data)
    s = std_dev(data)
    
    if s == 0:
        return 0.0
    
    skew = sum((x - m) ** 3 for x in data) / n
    return skew / (s ** 3)


def kurtosis(data: List[float]) -> float:
    """
    Calculate the excess kurtosis (measure of tail heaviness).
    
    Args:
        data: List of numeric values
        
    Returns:
        Excess kurtosis (positive = heavy tails, negative = light tails)
    """
    if len(data) < 4:
        raise ValueError("Kurtosis requires at least 4 data points")
    
    n = len(data)
    m = mean(data)
    s = std_dev(data)
    
    if s == 0:
        return 0.0
    
    kurt = sum((x - m) ** 4 for x in data) / n
    excess_kurt = (kurt / (s ** 4)) - 3
    return excess_kurt


# ============================================================================
# Correlation and Regression
# ============================================================================

def covariance(x: List[float], y: List[float]) -> float:
    """
    Calculate the covariance between two variables.
    
    Args:
        x: First variable data
        y: Second variable data
        
    Returns:
        Covariance between x and y
    """
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    if len(x) < 2:
        raise ValueError("Covariance requires at least 2 data points")
    
    mx = mean(x)
    my = mean(y)
    
    return sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / (len(x) - 1)


def correlation(x: List[float], y: List[float]) -> float:
    """
    Calculate Pearson correlation coefficient.
    
    Args:
        x: First variable data
        y: Second variable data
        
    Returns:
        Correlation coefficient (-1 to 1)
    """
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    if len(x) < 2:
        raise ValueError("Correlation requires at least 2 data points")
    
    sx = std_dev(x)
    sy = std_dev(y)
    
    if sx == 0 or sy == 0:
        return 0.0
    
    return covariance(x, y) / (sx * sy)


def spearman_correlation(x: List[float], y: List[float]) -> float:
    """
    Calculate Spearman rank correlation coefficient.
    
    Args:
        x: First variable data
        y: Second variable data
        
    Returns:
        Spearman correlation coefficient (-1 to 1)
    """
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    if len(x) < 2:
        raise ValueError("Correlation requires at least 2 data points")
    
    def rank(data: List[float]) -> List[float]:
        sorted_indices = sorted(range(len(data)), key=lambda i: data[i])
        ranks = [0.0] * len(data)
        for rank_val, idx in enumerate(sorted_indices, 1):
            ranks[idx] = rank_val
        return ranks
    
    rank_x = rank(x)
    rank_y = rank(y)
    
    return correlation(rank_x, rank_y)


def linear_regression(x: List[float], y: List[float]) -> Dict[str, float]:
    """
    Perform simple linear regression (y = slope * x + intercept).
    
    Args:
        x: Independent variable data
        y: Dependent variable data
        
    Returns:
        Dictionary with slope, intercept, r_squared, and std_error
    """
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    if len(x) < 2:
        raise ValueError("Regression requires at least 2 data points")
    
    n = len(x)
    mx = mean(x)
    my = mean(y)
    
    # Calculate slope
    numerator = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    denominator = sum((xi - mx) ** 2 for xi in x)
    
    if denominator == 0:
        raise InvalidDataError("Cannot perform regression: x values are constant")
    
    slope = numerator / denominator
    intercept = my - slope * mx
    
    # Calculate R-squared
    y_pred = [slope * xi + intercept for xi in x]
    ss_res = sum((yi - ypi) ** 2 for yi, ypi in zip(y, y_pred))
    ss_tot = sum((yi - my) ** 2 for yi in y)
    
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0
    
    # Calculate standard error of estimate
    std_error = math.sqrt(ss_res / (n - 2)) if n > 2 else 0.0
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'std_error': std_error
    }


def predict(regression: Dict[str, float], x: float) -> float:
    """
    Predict y value using linear regression results.
    
    Args:
        regression: Result from linear_regression()
        x: X value to predict
        
    Returns:
        Predicted y value
    """
    return regression['slope'] * x + regression['intercept']


# ============================================================================
# Normalization and Scaling
# ============================================================================

def normalize_minmax(data: List[float], new_min: float = 0.0, new_max: float = 1.0) -> List[float]:
    """
    Normalize data to a new range using min-max scaling.
    
    Args:
        data: List of numeric values
        new_min: New minimum value (default 0.0)
        new_max: New maximum value (default 1.0)
        
    Returns:
        Normalized data
    """
    if not data:
        raise EmptyDataError("Cannot normalize empty data")
    
    old_min = min(data)
    old_max = max(data)
    old_range = old_max - old_min
    
    if old_range == 0:
        return [(new_min + new_max) / 2] * len(data)
    
    new_range = new_max - new_min
    return [((x - old_min) / old_range) * new_range + new_min for x in data]


def standardize(data: List[float]) -> List[float]:
    """
    Standardize data to z-scores (mean=0, std_dev=1).
    
    Args:
        data: List of numeric values
        
    Returns:
        Standardized data (z-scores)
    """
    if not data:
        raise EmptyDataError("Cannot standardize empty data")
    
    m = mean(data)
    s = std_dev(data)
    
    if s == 0:
        return [0.0] * len(data)
    
    return [(x - m) / s for x in data]


def robust_scale(data: List[float]) -> List[float]:
    """
    Scale data using median and IQR (robust to outliers).
    
    Args:
        data: List of numeric values
        
    Returns:
        Robustly scaled data
    """
    if not data:
        raise EmptyDataError("Cannot scale empty data")
    
    med = median(data)
    iqr_val = iqr(data)
    
    if iqr_val == 0:
        return [0.0] * len(data)
    
    return [(x - med) / iqr_val for x in data]


# ============================================================================
# Outlier Detection
# ============================================================================

def detect_outliers_iqr(data: List[float], multiplier: float = 1.5) -> List[Tuple[int, float]]:
    """
    Detect outliers using the IQR method.
    
    Args:
        data: List of numeric values
        multiplier: IQR multiplier for bounds (default 1.5)
        
    Returns:
        List of (index, value) tuples for outliers
    """
    if not data:
        raise EmptyDataError("Cannot detect outliers in empty data")
    
    q1, _, q3 = quartiles(data)
    iqr_val = q3 - q1
    
    lower_bound = q1 - multiplier * iqr_val
    upper_bound = q3 + multiplier * iqr_val
    
    return [(i, x) for i, x in enumerate(data) if x < lower_bound or x > upper_bound]


def detect_outliers_zscore(data: List[float], threshold: float = 3.0) -> List[Tuple[int, float]]:
    """
    Detect outliers using z-score method.
    
    Args:
        data: List of numeric values
        threshold: Z-score threshold (default 3.0)
        
    Returns:
        List of (index, value) tuples for outliers
    """
    if not data:
        raise EmptyDataError("Cannot detect outliers in empty data")
    
    m = mean(data)
    s = std_dev(data)
    
    if s == 0:
        return []
    
    return [(i, x) for i, x in enumerate(data) if abs((x - m) / s) > threshold]


def remove_outliers(data: List[float], method: str = 'iqr', **kwargs) -> List[float]:
    """
    Remove outliers from data.
    
    Args:
        data: List of numeric values
        method: 'iqr' or 'zscore'
        **kwargs: Additional arguments for outlier detection
        
    Returns:
        Data with outliers removed
    """
    if method == 'iqr':
        outliers = detect_outliers_iqr(data, **kwargs)
    elif method == 'zscore':
        outliers = detect_outliers_zscore(data, **kwargs)
    else:
        raise ValueError("Method must be 'iqr' or 'zscore'")
    
    outlier_indices = {i for i, _ in outliers}
    return [x for i, x in enumerate(data) if i not in outlier_indices]


# ============================================================================
# Distribution Functions
# ============================================================================

def normal_pdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """
    Calculate normal distribution probability density function.
    
    Args:
        x: Value to evaluate
        mu: Mean (default 0.0)
        sigma: Standard deviation (default 1.0)
        
    Returns:
        PDF value at x
    """
    if sigma <= 0:
        raise ValueError("Sigma must be positive")
    
    coeff = 1.0 / (sigma * math.sqrt(2 * math.pi))
    exponent = -((x - mu) ** 2) / (2 * sigma ** 2)
    return coeff * math.exp(exponent)


def normal_cdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """
    Calculate normal distribution cumulative distribution function.
    Uses error function approximation.
    
    Args:
        x: Value to evaluate
        mu: Mean (default 0.0)
        sigma: Standard deviation (default 1.0)
        
    Returns:
        CDF value at x (0 to 1)
    """
    if sigma <= 0:
        raise ValueError("Sigma must be positive")
    
    z = (x - mu) / (sigma * math.sqrt(2))
    return 0.5 * (1 + math.erf(z))


def z_score(x: float, mu: float, sigma: float) -> float:
    """
    Calculate z-score for a value.
    
    Args:
        x: Value
        mu: Mean
        sigma: Standard deviation
        
    Returns:
        Z-score
    """
    if sigma <= 0:
        raise ValueError("Sigma must be positive")
    return (x - mu) / sigma


def chi_square_statistic(observed: List[float], expected: List[float]) -> float:
    """
    Calculate chi-square statistic for goodness of fit.
    
    Args:
        observed: Observed frequencies
        expected: Expected frequencies
        
    Returns:
        Chi-square statistic
    """
    if len(observed) != len(expected):
        raise ValueError("Observed and expected must have same length")
    if any(e <= 0 for e in expected):
        raise InvalidDataError("Expected frequencies must be positive")
    
    return sum((o - e) ** 2 / e for o, e in zip(observed, expected))


# ============================================================================
# Frequency Analysis
# ============================================================================

def frequency_table(data: List[Any]) -> Dict[Any, int]:
    """
    Create a frequency table.
    
    Args:
        data: List of values
        
    Returns:
        Dictionary mapping values to their counts
    """
    return dict(Counter(data))


def relative_frequency(data: List[Any]) -> Dict[Any, float]:
    """
    Calculate relative frequencies.
    
    Args:
        data: List of values
        
    Returns:
        Dictionary mapping values to their relative frequencies (0-1)
    """
    if not data:
        raise EmptyDataError("Cannot calculate relative frequency of empty data")
    
    freq = frequency_table(data)
    n = len(data)
    return {k: v / n for k, v in freq.items()}


def cumulative_frequency(data: List[float], bins: Optional[int] = None) -> List[Tuple[float, int]]:
    """
    Calculate cumulative frequency distribution.
    
    Args:
        data: List of numeric values
        bins: Number of bins (default: auto using Sturges' formula)
        
    Returns:
        List of (bin_upper_bound, cumulative_count) tuples
    """
    if not data:
        raise EmptyDataError("Cannot calculate cumulative frequency of empty data")
    
    if bins is None:
        bins = int(1 + 3.322 * math.log10(len(data)))  # Sturges' formula
        bins = max(1, min(bins, 20))
    
    min_val = min(data)
    max_val = max(data)
    bin_width = (max_val - min_val) / bins if max_val != min_val else 1
    
    # Count frequencies
    bin_counts = [0] * bins
    for x in data:
        bin_idx = min(int((x - min_val) / bin_width), bins - 1)
        bin_counts[bin_idx] += 1
    
    # Calculate cumulative
    cumulative = []
    cum_count = 0
    for i, count in enumerate(bin_counts):
        cum_count += count
        bin_upper = min_val + (i + 1) * bin_width
        cumulative.append((bin_upper, cum_count))
    
    return cumulative


# ============================================================================
# Convenience Functions (Module-level API)
# ============================================================================

def describe(data: List[float]) -> Dict[str, float]:
    """
    Generate comprehensive descriptive statistics.
    
    Args:
        data: List of numeric values
        
    Returns:
        Dictionary with all descriptive statistics
    """
    return {
        'count': len(data),
        'mean': mean(data),
        'std_dev': std_dev(data),
        'variance': variance(data),
        'min': min(data),
        'q1': quartiles(data)[0],
        'median': median(data),
        'q3': quartiles(data)[2],
        'max': max(data),
        'range': range_value(data),
        'iqr': iqr(data),
        'skewness': skewness(data),
        'kurtosis': kurtosis(data),
        'cv': coefficient_of_variation(data),
    }


def summary(data: List[float], percentiles: List[float] = None) -> str:
    """
    Generate a human-readable summary string.
    
    Args:
        data: List of numeric values
        percentiles: Additional percentiles to include (default: [25, 50, 75])
        
    Returns:
        Formatted summary string
    """
    if percentiles is None:
        percentiles = [25, 50, 75]
    
    stats = describe(data)
    lines = [
        f"Count:  {stats['count']}",
        f"Mean:   {stats['mean']:.4f}",
        f"Std Dev: {stats['std_dev']:.4f}",
        f"Min:    {stats['min']:.4f}",
    ]
    
    for p in percentiles:
        lines.append(f"P{int(p):02d}:    {percentile(data, p):.4f}")
    
    lines.extend([
        f"Max:    {stats['max']:.4f}",
        f"Range:  {stats['range']:.4f}",
    ])
    
    return '\n'.join(lines)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Exceptions
    'StatisticsError', 'EmptyDataError', 'InvalidDataError',
    
    # Descriptive Statistics
    'mean', 'geometric_mean', 'harmonic_mean', 'median', 'mode',
    'variance', 'std_dev', 'quartiles', 'iqr', 'percentile',
    'range_value', 'coefficient_of_variation', 'skewness', 'kurtosis',
    
    # Correlation and Regression
    'covariance', 'correlation', 'spearman_correlation',
    'linear_regression', 'predict',
    
    # Normalization
    'normalize_minmax', 'standardize', 'robust_scale',
    
    # Outlier Detection
    'detect_outliers_iqr', 'detect_outliers_zscore', 'remove_outliers',
    
    # Distribution Functions
    'normal_pdf', 'normal_cdf', 'z_score', 'chi_square_statistic',
    
    # Frequency Analysis
    'frequency_table', 'relative_frequency', 'cumulative_frequency',
    
    # Convenience
    'describe', 'summary',
]
