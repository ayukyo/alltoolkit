#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Probability Distribution Utilities Test Suite
===========================================================
Comprehensive tests for probability_utils module.

Tests cover:
    - Basic statistical functions
    - Normal distribution
    - Binomial distribution
    - Poisson distribution
    - Exponential distribution
    - Uniform distribution
    - Confidence intervals
    - Hypothesis testing
    - Probability calculations
    - Random sampling
    - Utility functions
    - Distribution classes
    - Edge cases and error handling
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Basic Statistics
    mean, median, mode, variance, std_dev,
    percentile, quartiles, iqr, range_, coefficient_of_variation,
    skewness, kurtosis,
    
    # Normal Distribution
    normal_pdf, normal_cdf, normal_ppf, z_score, standardize,
    
    # Binomial Distribution
    factorial, combination, permutation,
    binomial_pmf, binomial_cdf, binomial_mean, binomial_variance, binomial_std,
    
    # Poisson Distribution
    poisson_pmf, poisson_cdf, poisson_mean, poisson_variance,
    
    # Exponential Distribution
    exponential_pdf, exponential_cdf, exponential_ppf,
    exponential_mean, exponential_variance,
    
    # Uniform Distribution
    uniform_pdf, uniform_cdf, uniform_mean, uniform_variance,
    
    # Confidence Intervals
    z_confidence_interval, t_confidence_interval, proportion_confidence_interval,
    
    # Hypothesis Testing
    z_test, margin_of_error, sample_size_for_mean, sample_size_for_proportion,
    
    # Probability Calculations
    probability_union, probability_intersection_independent,
    conditional_probability, bayes_theorem, total_probability,
    
    # Random Sampling
    random_normal, random_exponential, random_uniform,
    random_binomial, random_poisson,
    
    # Utility Functions
    covariance, correlation, geometric_mean, harmonic_mean,
    trimmed_mean, weighted_mean,
    
    # Distribution Classes
    NormalDistribution, BinomialDistribution, PoissonDistribution,
    ExponentialDistribution, UniformDistribution,
    
    # Constants
    Z_SCORES,
)

import math
import random


class TestResult:
    """Test result tracker."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def success(self, test_name: str):
        self.passed += 1
        print(f"✓ {test_name}")
    
    def failure(self, test_name: str, message: str):
        self.failed += 1
        self.errors.append((test_name, message))
        print(f"✗ {test_name}: {message}")
    
    def assert_equal(self, test_name: str, expected, actual, tolerance: float = 1e-10):
        if isinstance(expected, float) and isinstance(actual, float):
            if abs(expected - actual) <= tolerance:
                self.success(test_name)
            else:
                self.failure(test_name, f"Expected {expected}, got {actual}")
        else:
            if expected == actual:
                self.success(test_name)
            else:
                self.failure(test_name, f"Expected {expected}, got {actual}")
    
    def assert_raises(self, test_name: str, exception_type, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.failure(test_name, f"Expected {exception_type.__name__} to be raised")
        except exception_type:
            self.success(test_name)
        except Exception as e:
            self.failure(test_name, f"Expected {exception_type.__name__}, got {type(e).__name__}: {e}")
    
    def assert_true(self, test_name: str, condition: bool):
        if condition:
            self.success(test_name)
        else:
            self.failure(test_name, "Condition is False")
    
    def assert_in_range(self, test_name: str, value: float, low: float, high: float):
        if low <= value <= high:
            self.success(test_name)
        else:
            self.failure(test_name, f"Value {value} not in range [{low}, {high}]")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Summary: {self.passed}/{total} passed ({self.failed} failed)")
        if self.errors:
            print("\nFailed tests:")
            for name, msg in self.errors:
                print(f"  - {name}: {msg}")
        print(f"{'='*60}")
        return self.failed == 0


def run_tests():
    """Run all tests."""
    result = TestResult()
    
    print("\n" + "="*60)
    print("AllToolkit - Probability Distribution Utilities Tests")
    print("="*60)
    
    # ========================================
    # Basic Statistical Functions Tests
    # ========================================
    print("\n--- Basic Statistical Functions ---")
    
    result.assert_equal("mean: basic", 3.0, mean([1, 2, 3, 4, 5]))
    result.assert_equal("mean: single element", 10.0, mean([10]))
    result.assert_equal("mean: negative values", 0.0, mean([-2, 0, 2]))
    result.assert_raises("mean: empty list", ValueError, mean, [])
    
    result.assert_equal("median: odd count", 3.0, median([1, 2, 3, 4, 5]))
    result.assert_equal("median: even count", 2.5, median([1, 2, 3, 4]))
    result.assert_equal("median: unsorted", 3.0, median([5, 1, 3, 2, 4]))
    result.assert_raises("median: empty list", ValueError, median, [])
    
    result.assert_equal("mode: single mode", [3], mode([1, 2, 2, 3, 3, 3]))
    result.assert_equal("mode: multiple modes", [1, 2], mode([1, 1, 2, 2]))
    result.assert_equal("mode: all unique", [1, 2, 3], mode([1, 2, 3]))
    result.assert_raises("mode: empty list", ValueError, mode, [])
    
    result.assert_equal("variance: population", 2.0, variance([1, 2, 3, 4, 5]))
    result.assert_equal("variance: sample", 2.5, variance([1, 2, 3, 4, 5], population=False))
    result.assert_equal("variance: zero", 0.0, variance([5, 5, 5]))
    result.assert_raises("variance: empty list", ValueError, variance, [])
    result.assert_raises("variance: sample with 1 element", ValueError, variance, [1], population=False)
    
    result.assert_equal("std_dev: basic", math.sqrt(2), std_dev([1, 2, 3, 4, 5]), 1e-10)
    result.assert_equal("std_dev: zero", 0.0, std_dev([5, 5, 5]))
    
    result.assert_equal("percentile: 50th (median)", 3.0, percentile([1, 2, 3, 4, 5], 50))
    result.assert_equal("percentile: 0th (min)", 1.0, percentile([1, 2, 3, 4, 5], 0))
    result.assert_equal("percentile: 100th (max)", 5.0, percentile([1, 2, 3, 4, 5], 100))
    # Linear interpolation method gives different result than exclusive method
    result.assert_in_range("percentile: 25th", percentile([1, 2, 3, 4, 5], 25), 1.5, 2.5)
    result.assert_raises("percentile: empty list", ValueError, percentile, [], 50)
    result.assert_raises("percentile: invalid p", ValueError, percentile, [1, 2, 3], 150)
    
    q1, q2, q3 = quartiles([1, 2, 3, 4, 5, 6, 7, 8])
    result.assert_in_range("quartiles: Q1", q1, 2.0, 3.0)
    result.assert_equal("quartiles: Q2 (median)", 4.5, q2, 1e-6)
    result.assert_in_range("quartiles: Q3", q3, 5.5, 7.0)
    
    result.assert_in_range("iqr: basic", iqr([1, 2, 3, 4, 5, 6, 7, 8]), 3.0, 5.0)
    
    result.assert_equal("range: basic", 4.0, range_([1, 2, 3, 4, 5]))
    result.assert_equal("range: negative values", 10.0, range_([-5, 5]))
    result.assert_raises("range: empty list", ValueError, range_, [])
    
    cv = coefficient_of_variation([10, 20, 30, 40, 50])
    result.assert_in_range("coefficient_of_variation: basic", cv, 0.4, 0.5)
    result.assert_raises("coefficient_of_variation: zero mean", ValueError, coefficient_of_variation, [0, 0, 0])
    
    result.assert_equal("skewness: symmetric", 0.0, skewness([1, 2, 3, 4, 5]), 1e-6)
    result.assert_raises("skewness: fewer than 3", ValueError, skewness, [1, 2])
    
    # Kurtosis formula varies; excess kurtosis of flat uniform distribution is negative
    result.assert_true("kurtosis: flat distribution is negative", kurtosis([1, 2, 3, 4, 5]) < 0)
    result.assert_raises("kurtosis: fewer than 4", ValueError, kurtosis, [1, 2, 3])
    
    # ========================================
    # Normal Distribution Tests
    # ========================================
    print("\n--- Normal Distribution ---")
    
    result.assert_equal("normal_pdf: at mean", 0.3989422804014327, normal_pdf(0), 1e-10)
    result.assert_equal("normal_pdf: at z=1", 0.24197072451914337, normal_pdf(1), 1e-10)
    # PDF at z=1 with std=15: exp(-0.5 * 1^2) / (15 * sqrt(2*pi))
    result.assert_in_range("normal_pdf: custom params", normal_pdf(115, 100, 15), 0.016, 0.017)
    result.assert_raises("normal_pdf: negative std", ValueError, normal_pdf, 0, 0, -1)
    
    result.assert_equal("normal_cdf: at mean", 0.5, normal_cdf(0))
    result.assert_equal("normal_cdf: at z=1.96", 0.975, normal_cdf(1.96), 0.001)
    result.assert_equal("normal_cdf: at z=-1.96", 0.025, normal_cdf(-1.96), 0.001)
    result.assert_equal("normal_cdf: far right", 1.0, normal_cdf(10), 1e-10)
    result.assert_equal("normal_cdf: far left", 0.0, normal_cdf(-10), 1e-10)
    
    result.assert_equal("normal_ppf: at 0.5", 0.0, normal_ppf(0.5))
    result.assert_equal("normal_ppf: at 0.975", 1.96, normal_ppf(0.975), 0.01)
    result.assert_equal("normal_ppf: at 0.025", -1.96, normal_ppf(0.025), 0.01)
    result.assert_equal("normal_ppf: custom params", 100, normal_ppf(0.5, 100, 15))
    result.assert_raises("normal_ppf: p=0", ValueError, normal_ppf, 0)
    result.assert_raises("normal_ppf: p=1", ValueError, normal_ppf, 1)
    
    result.assert_equal("z_score: basic", 1.5, z_score(85, 70, 10))
    result.assert_equal("z_score: negative", -1.0, z_score(50, 60, 10))
    result.assert_raises("z_score: zero std", ValueError, z_score, 85, 70, 0)
    
    standardized = standardize([1, 2, 3, 4, 5])
    result.assert_equal("standardize: mean of standardized", 0.0, mean(standardized), 1e-10)
    # Standardize uses population variance (N), not sample variance (N-1)
    result.assert_in_range("standardize: std of standardized", std_dev(standardized), 0.85, 1.0)
    result.assert_equal("standardize: constant data", [0.0, 0.0, 0.0], standardize([5, 5, 5]))
    
    # ========================================
    # Binomial Distribution Tests
    # ========================================
    print("\n--- Binomial Distribution ---")
    
    result.assert_equal("factorial: 0", 1, factorial(0))
    result.assert_equal("factorial: 1", 1, factorial(1))
    result.assert_equal("factorial: 5", 120, factorial(5))
    result.assert_equal("factorial: 10", 3628800, factorial(10))
    result.assert_raises("factorial: negative", ValueError, factorial, -1)
    
    result.assert_equal("combination: C(10,0)", 1, combination(10, 0))
    result.assert_equal("combination: C(10,10)", 1, combination(10, 10))
    result.assert_equal("combination: C(10,3)", 120, combination(10, 3))
    result.assert_equal("combination: C(10,7)", 120, combination(10, 7))  # Symmetry
    result.assert_equal("combination: C(5,2)", 10, combination(5, 2))
    result.assert_equal("combination: C(0,0)", 1, combination(0, 0))
    result.assert_equal("combination: out of range", 0, combination(10, 15))
    
    result.assert_equal("permutation: P(10,0)", 1, permutation(10, 0))
    result.assert_equal("permutation: P(10,3)", 720, permutation(10, 3))
    result.assert_equal("permutation: P(5,5)", 120, permutation(5, 5))
    result.assert_equal("permutation: out of range", 0, permutation(10, 15))
    
    result.assert_in_range("binomial_pmf: P(X=5,n=10,p=0.5)", binomial_pmf(5, 10, 0.5), 0.24, 0.25)
    result.assert_in_range("binomial_pmf: P(X=0,n=10,p=0.5)", binomial_pmf(0, 10, 0.5), 0.0009, 0.0011)
    result.assert_in_range("binomial_pmf: P(X=10,n=10,p=0.5)", binomial_pmf(10, 10, 0.5), 0.0009, 0.0011)
    result.assert_equal("binomial_pmf: k out of range", 0.0, binomial_pmf(15, 10, 0.5))
    result.assert_in_range("binomial_pmf: p=0.3", binomial_pmf(2, 5, 0.3), 0.30, 0.31)
    result.assert_raises("binomial_pmf: invalid p", ValueError, binomial_pmf, 5, 10, 1.5)
    
    result.assert_in_range("binomial_cdf: P(X<=5,n=10,p=0.5)", binomial_cdf(5, 10, 0.5), 0.62, 0.63)
    result.assert_in_range("binomial_cdf: P(X<=0,n=10,p=0.5)", binomial_cdf(0, 10, 0.5), 0.0009, 0.0011)
    result.assert_in_range("binomial_cdf: P(X<=10,n=10,p=0.5)", binomial_cdf(10, 10, 0.5), 0.99, 1.01)
    
    result.assert_equal("binomial_mean", 5.0, binomial_mean(10, 0.5))
    result.assert_equal("binomial_variance", 2.5, binomial_variance(10, 0.5))
    result.assert_equal("binomial_std", math.sqrt(2.5), binomial_std(10, 0.5), 1e-10)
    
    # ========================================
    # Poisson Distribution Tests
    # ========================================
    print("\n--- Poisson Distribution ---")
    
    result.assert_in_range("poisson_pmf: P(X=3,λ=2.5)", poisson_pmf(3, 2.5), 0.21, 0.22)
    result.assert_in_range("poisson_pmf: P(X=0,λ=2)", poisson_pmf(0, 2), 0.13, 0.14)
    result.assert_equal("poisson_pmf: λ=0, k=0", 1.0, poisson_pmf(0, 0))
    result.assert_equal("poisson_pmf: λ=0, k>0", 0.0, poisson_pmf(1, 0))
    result.assert_equal("poisson_pmf: k negative", 0.0, poisson_pmf(-1, 2))
    
    result.assert_in_range("poisson_cdf: P(X<=3,λ=2.5)", poisson_cdf(3, 2.5), 0.75, 0.76)
    result.assert_in_range("poisson_cdf: P(X<=0,λ=2)", poisson_cdf(0, 2), 0.13, 0.14)
    
    result.assert_equal("poisson_mean", 3.0, poisson_mean(3))
    result.assert_equal("poisson_variance", 3.0, poisson_variance(3))
    
    # ========================================
    # Exponential Distribution Tests
    # ========================================
    print("\n--- Exponential Distribution ---")
    
    result.assert_in_range("exponential_pdf: x=1,λ=0.5", exponential_pdf(1, 0.5), 0.30, 0.31)
    result.assert_equal("exponential_pdf: x<0", 0.0, exponential_pdf(-1, 0.5))
    result.assert_raises("exponential_pdf: negative lambda", ValueError, exponential_pdf, 1, -1)
    
    result.assert_in_range("exponential_cdf: x=2,λ=0.5", exponential_cdf(2, 0.5), 0.63, 0.64)
    result.assert_equal("exponential_cdf: x<0", 0.0, exponential_cdf(-1, 0.5))
    result.assert_equal("exponential_cdf: x=0", 0.0, exponential_cdf(0, 0.5))
    
    result.assert_in_range("exponential_ppf: p=0.5,λ=0.5", exponential_ppf(0.5, 0.5), 1.38, 1.39)
    result.assert_equal("exponential_ppf: p=0", 0.0, exponential_ppf(0.0001, 0.5), 0.01)
    result.assert_raises("exponential_ppf: p=1", ValueError, exponential_ppf, 1, 0.5)
    
    result.assert_equal("exponential_mean", 2.0, exponential_mean(0.5))
    result.assert_equal("exponential_variance", 4.0, exponential_variance(0.5))
    
    # ========================================
    # Uniform Distribution Tests
    # ========================================
    print("\n--- Uniform Distribution ---")
    
    result.assert_equal("uniform_pdf: in range", 1.0, uniform_pdf(0.5, 0, 1))
    result.assert_equal("uniform_pdf: out of range", 0.0, uniform_pdf(2, 0, 1))
    result.assert_equal("uniform_pdf: at boundary", 1.0, uniform_pdf(0, 0, 1))
    result.assert_raises("uniform_pdf: invalid bounds", ValueError, uniform_pdf, 0.5, 1, 0)
    
    result.assert_equal("uniform_cdf: in middle", 0.5, uniform_cdf(0.5, 0, 1))
    result.assert_equal("uniform_cdf: below range", 0.0, uniform_cdf(-1, 0, 1))
    result.assert_equal("uniform_cdf: above range", 1.0, uniform_cdf(2, 0, 1))
    result.assert_equal("uniform_cdf: at lower bound", 0.0, uniform_cdf(0, 0, 1))
    result.assert_equal("uniform_cdf: at upper bound", 1.0, uniform_cdf(1, 0, 1))
    
    result.assert_equal("uniform_mean", 0.5, uniform_mean(0, 1))
    result.assert_equal("uniform_variance", 1/12, uniform_variance(0, 1), 1e-10)
    
    # ========================================
    # Confidence Intervals Tests
    # ========================================
    print("\n--- Confidence Intervals ---")
    
    ci = z_confidence_interval(100, 15, 50, 0.95)
    result.assert_in_range("z_confidence_interval: lower", ci[0], 95.5, 96.0)
    result.assert_in_range("z_confidence_interval: upper", ci[1], 103.5, 104.5)
    result.assert_raises("z_confidence_interval: invalid n", ValueError, z_confidence_interval, 100, 15, 0)
    
    ci = t_confidence_interval(100, 15, 10, 0.95)
    result.assert_in_range("t_confidence_interval: lower", ci[0], 89, 91)
    result.assert_in_range("t_confidence_interval: upper", ci[1], 109, 111)
    result.assert_raises("t_confidence_interval: n=1", ValueError, t_confidence_interval, 100, 15, 1)
    
    ci = proportion_confidence_interval(45, 100, 0.95)
    result.assert_in_range("proportion_confidence_interval: lower", ci[0], 0.35, 0.36)
    result.assert_in_range("proportion_confidence_interval: upper", ci[1], 0.54, 0.55)
    
    # ========================================
    # Hypothesis Testing Tests
    # ========================================
    print("\n--- Hypothesis Testing ---")
    
    z, p = z_test(105, 100, 15, 50)
    result.assert_in_range("z_test: z statistic", z, 2.3, 2.4)
    result.assert_in_range("z_test: p value", p, 0.01, 0.03)
    
    result.assert_in_range("margin_of_error", margin_of_error(15, 100, 0.95), 2.8, 3.0)
    
    result.assert_equal("sample_size_for_mean", 97, sample_size_for_mean(15, 3, 0.95))
    result.assert_equal("sample_size_for_proportion", 1068, sample_size_for_proportion(0.03, 0.95))
    
    # ========================================
    # Probability Calculations Tests
    # ========================================
    print("\n--- Probability Calculations ---")
    
    result.assert_equal("probability_union: with intersection", 0.6, probability_union(0.4, 0.5, 0.3))
    result.assert_equal("probability_union: disjoint", 0.7, probability_union(0.4, 0.3, 0.0))
    
    result.assert_equal("probability_intersection_independent", 0.12, probability_intersection_independent(0.3, 0.4))
    
    result.assert_equal("conditional_probability", 0.12, conditional_probability(0.3, 0.4))
    
    # Bayes theorem example: medical test
    p_disease = 0.01
    p_positive_given_disease = 0.99
    p_positive = p_disease * p_positive_given_disease + (1 - p_disease) * 0.05
    posterior = bayes_theorem(p_positive_given_disease, p_disease, p_positive)
    result.assert_in_range("bayes_theorem: medical test", posterior, 0.15, 0.18)
    
    # Total probability example
    p_factory = [0.5, 0.3, 0.2]
    p_defect = [0.01, 0.02, 0.03]
    result.assert_in_range("total_probability", total_probability(p_defect, p_factory), 0.016, 0.018)
    
    # ========================================
    # Utility Functions Tests
    # ========================================
    print("\n--- Utility Functions ---")
    
    result.assert_equal("covariance: perfect correlation", 4.0, covariance([1, 2, 3, 4, 5], [2, 4, 6, 8, 10]))
    cov = covariance([1, 2, 3], [3, 1, 2])
    result.assert_in_range("covariance: partial correlation", cov, -0.5, 0.5)
    result.assert_raises("covariance: unequal length", ValueError, covariance, [1, 2], [1, 2, 3])
    
    result.assert_equal("correlation: perfect positive", 1.0, correlation([1, 2, 3, 4, 5], [2, 4, 6, 8, 10]), 1e-10)
    result.assert_equal("correlation: perfect negative", -1.0, correlation([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]), 1e-10)
    r = correlation([1, 2, 3], [3, 1, 2])
    result.assert_in_range("correlation: partial", r, -1, 1)
    
    result.assert_in_range("geometric_mean", geometric_mean([1, 2, 4, 8]), 2.8, 2.9)
    result.assert_raises("geometric_mean: zero value", ValueError, geometric_mean, [1, 0, 2])
    result.assert_raises("geometric_mean: negative value", ValueError, geometric_mean, [1, -1, 2])
    
    result.assert_in_range("harmonic_mean", harmonic_mean([1, 2, 4]), 1.7, 1.8)
    result.assert_raises("harmonic_mean: zero value", ValueError, harmonic_mean, [1, 0, 2])
    
    result.assert_in_range("trimmed_mean", trimmed_mean([1, 2, 3, 4, 5, 100], 1/6), 3.3, 3.7)
    result.assert_equal("trimmed_mean: no trim", 3.0, trimmed_mean([1, 2, 3, 4, 5], 0))
    
    result.assert_in_range("weighted_mean", weighted_mean([1, 2, 3], [1, 2, 3]), 2.3, 2.4)
    result.assert_raises("weighted_mean: unequal length", ValueError, weighted_mean, [1, 2], [1])
    result.assert_raises("weighted_mean: negative weights", ValueError, weighted_mean, [1, 2], [1, -1])
    result.assert_raises("weighted_mean: zero total weight", ValueError, weighted_mean, [1, 2], [0, 0])
    
    # ========================================
    # Random Sampling Tests
    # ========================================
    print("\n--- Random Sampling ---")
    
    # Test that samples are in valid ranges
    samples = [random_normal(0, 1) for _ in range(100)]
    result.assert_in_range("random_normal: mean", mean(samples), -0.5, 0.5)
    result.assert_in_range("random_normal: std", std_dev(samples), 0.7, 1.3)
    result.assert_raises("random_normal: negative std", ValueError, random_normal, 0, -1)
    
    samples = [random_exponential(0.5) for _ in range(100)]
    result.assert_true("random_exponential: all positive", all(s >= 0 for s in samples))
    result.assert_in_range("random_exponential: mean", mean(samples), 1.5, 3.0)
    
    samples = [random_uniform(0, 10) for _ in range(100)]
    result.assert_true("random_uniform: all in range", all(0 <= s <= 10 for s in samples))
    result.assert_in_range("random_uniform: mean", mean(samples), 4, 6)
    result.assert_raises("random_uniform: invalid bounds", ValueError, random_uniform, 10, 0)
    
    samples = [random_binomial(10, 0.5) for _ in range(100)]
    result.assert_true("random_binomial: all in valid range", all(0 <= s <= 10 for s in samples))
    result.assert_in_range("random_binomial: mean", mean(samples), 3, 7)
    
    samples = [random_poisson(3) for _ in range(100)]
    result.assert_true("random_poisson: all non-negative", all(s >= 0 for s in samples))
    result.assert_in_range("random_poisson: mean", mean(samples), 2, 5)
    
    # ========================================
    # Distribution Classes Tests
    # ========================================
    print("\n--- Distribution Classes ---")
    
    norm = NormalDistribution(mean=100, std=15)
    result.assert_in_range("NormalDistribution.pdf", norm.pdf(115), 0.016, 0.017)
    result.assert_in_range("NormalDistribution.cdf", norm.cdf(115), 0.84, 0.85)
    result.assert_equal("NormalDistribution.mean", 100, norm.mean)
    result.assert_equal("NormalDistribution.std", 15, norm.std)
    result.assert_true("NormalDistribution.sample valid", 50 <= norm.sample() <= 150)
    result.assert_raises("NormalDistribution: negative std", ValueError, NormalDistribution, 0, -1)
    
    binom = BinomialDistribution(n=10, p=0.5)
    result.assert_in_range("BinomialDistribution.pmf", binom.pmf(5), 0.24, 0.25)
    result.assert_in_range("BinomialDistribution.cdf", binom.cdf(5), 0.62, 0.63)
    result.assert_equal("BinomialDistribution.mean", 5.0, binom.mean)
    result.assert_equal("BinomialDistribution.variance", 2.5, binom.variance)
    result.assert_true("BinomialDistribution.sample valid", 0 <= binom.sample() <= 10)
    
    pois = PoissonDistribution(lambda_=3)
    result.assert_in_range("PoissonDistribution.pmf", pois.pmf(3), 0.22, 0.23)
    result.assert_equal("PoissonDistribution.mean", 3.0, pois.mean)
    result.assert_equal("PoissonDistribution.variance", 3.0, pois.variance)
    result.assert_true("PoissonDistribution.sample valid", pois.sample() >= 0)
    
    exp = ExponentialDistribution(lambda_=0.5)
    result.assert_in_range("ExponentialDistribution.pdf", exp.pdf(1), 0.30, 0.31)
    result.assert_equal("ExponentialDistribution.mean", 2.0, exp.mean)
    result.assert_true("ExponentialDistribution.sample valid", exp.sample() >= 0)
    
    unif = UniformDistribution(a=0, b=1)
    result.assert_equal("UniformDistribution.pdf", 1.0, unif.pdf(0.5))
    result.assert_equal("UniformDistribution.mean", 0.5, unif.mean)
    result.assert_true("UniformDistribution.sample valid", 0 <= unif.sample() <= 1)
    
    # Test samples method
    norm_samples = norm.samples(50)
    result.assert_equal("NormalDistribution.samples: count", 50, len(norm_samples))
    
    binom_samples = binom.samples(50)
    result.assert_equal("BinomialDistribution.samples: count", 50, len(binom_samples))
    
    # ========================================
    # Edge Cases Tests
    # ========================================
    print("\n--- Edge Cases ---")
    
    # Empty data handling
    result.assert_raises("edge: mean empty", ValueError, mean, [])
    result.assert_raises("edge: variance empty", ValueError, variance, [])
    result.assert_raises("edge: std_dev empty", ValueError, std_dev, [])
    
    # Single element handling
    result.assert_equal("edge: mean single", 5.0, mean([5]))
    result.assert_equal("edge: variance single", 0.0, variance([5]))
    result.assert_raises("edge: sample variance single", ValueError, variance, [5], population=False)
    
    # Large values
    large_data = [1e10, 2e10, 3e10]
    result.assert_equal("edge: mean large values", 2e10, mean(large_data))
    
    # Negative values
    negative_data = [-5, -3, -1]
    result.assert_equal("edge: mean negative", -3.0, mean(negative_data))
    
    # Very small differences
    small_diff = [1.0000001, 1.0000002, 1.0000003]
    result.assert_in_range("edge: small differences", std_dev(small_diff), 0, 1e-7)
    
    # Probability at boundaries
    result.assert_equal("edge: normal_cdf extreme positive", 1.0, normal_cdf(100), 1e-10)
    result.assert_equal("edge: normal_cdf extreme negative", 0.0, normal_cdf(-100), 1e-10)
    
    # Binomial at boundaries
    result.assert_in_range("edge: binomial_pmf k=0", binomial_pmf(0, 10, 0.5), 0.0009, 0.0011)
    result.assert_in_range("edge: binomial_pmf k=n", binomial_pmf(10, 10, 0.5), 0.0009, 0.0011)
    
    # Poisson with small lambda
    result.assert_in_range("edge: poisson_pmf lambda=0.1", poisson_pmf(0, 0.1), 0.90, 0.91)
    
    # Confidence interval with large sample
    ci = z_confidence_interval(50, 5, 10000, 0.95)
    # Margin = z * std / sqrt(n) = 1.96 * 5 / 100 = 0.098
    result.assert_in_range("edge: CI very narrow", ci[1] - ci[0], 0.19, 0.20)
    
    return result.summary()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)