#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Probability Distribution Utilities Examples
=========================================================
Practical examples demonstrating probability_utils module usage.

Examples include:
    - Basic statistical analysis
    - Normal distribution calculations
    - Binomial and Poisson distributions
    - Confidence intervals
    - Hypothesis testing
    - Bayes' theorem applications
    - Random sampling simulations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from probability_utils.mod import (
    # Basic Statistics
    mean, median, mode, variance, std_dev,
    percentile, quartiles, iqr, skewness, kurtosis,
    
    # Normal Distribution
    normal_pdf, normal_cdf, normal_ppf, z_score, standardize,
    NormalDistribution,
    
    # Binomial Distribution
    binomial_pmf, binomial_cdf, combination,
    BinomialDistribution,
    
    # Poisson Distribution
    poisson_pmf, poisson_cdf, PoissonDistribution,
    
    # Exponential Distribution
    ExponentialDistribution,
    
    # Uniform Distribution
    UniformDistribution,
    
    # Confidence Intervals
    z_confidence_interval, proportion_confidence_interval,
    
    # Hypothesis Testing
    z_test, margin_of_error, sample_size_for_mean,
    
    # Probability Calculations
    bayes_theorem, total_probability,
    
    # Utility Functions
    correlation, covariance, geometric_mean, harmonic_mean,
    
    # Constants
    Z_SCORES,
)

import math


def example_basic_statistics():
    """Example: Basic statistical analysis of a dataset."""
    print("\n" + "="*60)
    print("Example 1: Basic Statistical Analysis")
    print("="*60)
    
    # Sample data: test scores
    scores = [85, 92, 78, 90, 88, 95, 82, 79, 91, 87, 83, 89]
    
    print(f"Data: {scores}")
    print(f"\nDescriptive Statistics:")
    print(f"  Mean: {mean(scores):.2f}")
    print(f"  Median: {median(scores):.2f}")
    print(f"  Mode: {mode(scores)}")
    print(f"  Variance (population): {variance(scores):.2f}")
    print(f"  Variance (sample): {variance(scores, population=False):.2f}")
    print(f"  Standard Deviation: {std_dev(scores):.2f}")
    
    print(f"\nPercentiles:")
    print(f"  25th percentile (Q1): {percentile(scores, 25):.2f}")
    print(f"  50th percentile (median): {percentile(scores, 50):.2f}")
    print(f"  75th percentile (Q3): {percentile(scores, 75):.2f}")
    print(f"  90th percentile: {percentile(scores, 90):.2f}")
    
    q1, q2, q3 = quartiles(scores)
    print(f"\nQuartiles: Q1={q1:.2f}, Q2={q2:.2f}, Q3={q3:.2f}")
    print(f"Interquartile Range (IQR): {iqr(scores):.2f}")
    
    print(f"\nShape Measures:")
    print(f"  Skewness: {skewness(scores):.4f}")
    print(f"  Kurtosis: {kurtosis(scores):.4f}")


def example_normal_distribution():
    """Example: Normal distribution calculations."""
    print("\n" + "="*60)
    print("Example 2: Normal Distribution")
    print("="*60)
    
    # IQ scores follow a normal distribution with mean=100, std=15
    print("IQ Scores Distribution (mean=100, std=15)")
    
    # Calculate probability of IQ between 85 and 115
    prob_85_115 = normal_cdf(115, 100, 15) - normal_cdf(85, 100, 15)
    print(f"\nProbability of IQ between 85-115: {prob_85_115:.2%}")
    
    # Calculate probability of IQ > 130
    prob_above_130 = 1 - normal_cdf(130, 100, 15)
    print(f"Probability of IQ > 130: {prob_above_130:.2%}")
    
    # Find the IQ value at 95th percentile
    iq_95th = normal_ppf(0.95, 100, 15)
    print(f"IQ at 95th percentile: {iq_95th:.1f}")
    
    # Using NormalDistribution class
    print("\nUsing NormalDistribution class:")
    iq_dist = NormalDistribution(mean=100, std=15)
    
    print(f"  PDF at IQ=100: {iq_dist.pdf(100):.4f}")
    print(f"  CDF at IQ=115: {iq_dist.cdf(115):.4f}")
    print(f"  97.5th percentile: {iq_dist.ppf(0.975):.1f}")
    
    # Z-score example
    z = z_score(115, 100, 15)
    print(f"\nZ-score for IQ=115: {z:.2f}")
    print(f"This IQ is {z:.2f} standard deviations above the mean")


def example_standardization():
    """Example: Standardizing a dataset."""
    print("\n" + "="*60)
    print("Example 3: Standardization (Z-score normalization)")
    print("="*60)
    
    # Original test scores
    test1 = [60, 70, 80, 90, 100]
    test2 = [5.5, 6.0, 6.5, 7.0, 7.5]
    
    print(f"Test 1 scores: {test1}")
    print(f"Test 2 scores: {test2}")
    
    # Standardize both
    std_test1 = standardize(test1)
    std_test2 = standardize(test2)
    
    print(f"\nStandardized Test 1: {[round(x, 2) for x in std_test1]}")
    print(f"Standardized Test 2: {[round(x, 2) for x in std_test2]}")
    
    print("\nAfter standardization:")
    print(f"  Both have mean ≈ 0")
    print(f"  Both have std ≈ 1")
    print("  Can now compare scores across different scales!")


def example_binomial_distribution():
    """Example: Binomial distribution calculations."""
    print("\n" + "="*60)
    print("Example 4: Binomial Distribution")
    print("="*60)
    
    # Quality control: 20% defect rate, inspect 10 items
    n = 10
    p = 0.2
    
    print(f"Quality Control Scenario:")
    print(f"  Sample size: {n} items")
    print(f"  Defect rate: {p:.0%}")
    
    # Probability of exactly 2 defects
    prob_2 = binomial_pmf(2, n, p)
    print(f"\nProbability of exactly 2 defects: {prob_2:.4f} ({prob_2:.2%})")
    
    # Probability of at most 2 defects
    prob_at_most_2 = binomial_cdf(2, n, p)
    print(f"Probability of at most 2 defects: {prob_at_most_2:.4f} ({prob_at_most_2:.2%})")
    
    # Probability of more than 5 defects
    prob_more_than_5 = 1 - binomial_cdf(5, n, p)
    print(f"Probability of more than 5 defects: {prob_more_than_5:.4f}")
    
    # Expected values
    print(f"\nExpected Statistics:")
    print(f"  Mean defects: {binomial_mean(n, p):.2f}")
    print(f"  Variance: {binomial_variance(n, p):.2f}")
    print(f"  Standard deviation: {binomial_std(n, p):.2f}")
    
    # Coin flip example
    print("\nCoin Flip Scenario (n=10, p=0.5):")
    print(f"  Probability of exactly 5 heads: {binomial_pmf(5, 10, 0.5):.4f}")
    print(f"  Probability of at least 8 heads: {1 - binomial_cdf(7, 10, 0.5):.4f}")


def example_poisson_distribution():
    """Example: Poisson distribution calculations."""
    print("\n" + "="*60)
    print("Example 5: Poisson Distribution")
    print("="*60)
    
    # Customer arrivals at a store
    lambda_rate = 5  # 5 customers per hour on average
    
    print(f"Customer Arrival Scenario:")
    print(f"  Average arrivals per hour: {lambda_rate}")
    
    # Probability of exactly 3 arrivals
    prob_3 = poisson_pmf(3, lambda_rate)
    print(f"\nProbability of exactly 3 arrivals: {prob_3:.4f} ({prob_3:.2%})")
    
    # Probability of at most 3 arrivals
    prob_at_most_3 = poisson_cdf(3, lambda_rate)
    print(f"Probability of at most 3 arrivals: {prob_at_most_3:.4f}")
    
    # Probability of more than 10 arrivals
    prob_more_than_10 = 1 - poisson_cdf(10, lambda_rate)
    print(f"Probability of more than 10 arrivals: {prob_more_than_10:.4f}")
    
    print(f"\nExpected Statistics:")
    print(f"  Mean: {poisson_mean(lambda_rate)}")
    print(f"  Variance: {poisson_variance(lambda_rate)}")
    
    # Using PoissonDistribution class
    pois = PoissonDistribution(lambda_=5)
    print("\nProbability distribution table:")
    for k in range(11):
        print(f"  P(X={k}): {pois.pmf(k):.4f}")


def example_confidence_intervals():
    """Example: Confidence intervals calculations."""
    print("\n" + "="*60)
    print("Example 6: Confidence Intervals")
    print("="*60)
    
    # Survey results: sample of 100, mean=52, std=8
    sample_mean = 52
    sample_std = 8
    n = 100
    
    print(f"Survey Data:")
    print(f"  Sample size: {n}")
    print(f"  Sample mean: {sample_mean}")
    print(f"  Sample std: {sample_std}")
    
    # 95% confidence interval
    ci_95 = z_confidence_interval(sample_mean, sample_std, n, 0.95)
    print(f"\n95% Confidence Interval: [{ci_95[0]:.2f}, {ci_95[1]:.2f}]")
    
    # 99% confidence interval
    ci_99 = z_confidence_interval(sample_mean, sample_std, n, 0.99)
    print(f"99% Confidence Interval: [{ci_99[0]:.2f}, {ci_99[1]:.2f}]")
    
    # Margin of error
    moe = margin_of_error(sample_std, n, 0.95)
    print(f"\nMargin of Error (95%): ±{moe:.2f}")
    
    # Proportion confidence interval
    print("\nProportion Example:")
    successes = 65
    n_prop = 100
    ci_prop = proportion_confidence_interval(successes, n_prop, 0.95)
    print(f"  Survey: {successes}/{n_prop} responded 'Yes'")
    print(f"  95% CI for proportion: [{ci_prop[0]:.3f}, {ci_prop[1]:.3f}]")
    print(f"  Point estimate: {successes/n_prop:.1%}")
    
    # Sample size calculation
    print("\nSample Size Calculation:")
    required_n = sample_size_for_mean(std=15, margin=2, confidence=0.95)
    print(f"  To estimate mean with ±2 margin (σ=15, 95% confidence)")
    print(f"  Required sample size: {required_n}")


def example_hypothesis_testing():
    """Example: Hypothesis testing."""
    print("\n" + "="*60)
    print("Example 7: Hypothesis Testing")
    print("="*60)
    
    # Testing if a new teaching method improves test scores
    # H0: μ = 70 (population mean)
    # Sample: mean = 75, n = 30, population std = 10
    
    sample_mean = 75
    population_mean = 70
    population_std = 10
    n = 30
    
    print(f"Hypothesis Test:")
    print(f"  H0: Population mean = {population_mean}")
    print(f"  H1: Population mean > {population_mean} (one-tailed)")
    print(f"  Sample mean: {sample_mean}")
    print(f"  Sample size: {n}")
    print(f"  Population std: {population_std}")
    
    z, p = z_test(sample_mean, population_mean, population_std, n, two_tailed=False)
    
    print(f"\nResults:")
    print(f"  Z-statistic: {z:.3f}")
    print(f"  P-value (one-tailed): {p:.4f}")
    
    alpha = 0.05
    if p < alpha:
        print(f"  Conclusion: Reject H0 (p < {alpha})")
        print("  The new method appears effective!")
    else:
        print(f"  Conclusion: Cannot reject H0 (p >= {alpha})")


def example_bayes_theorem():
    """Example: Bayes' theorem application."""
    print("\n" + "="*60)
    print("Example 8: Bayes' Theorem")
    print("="*60)
    
    # Medical test example
    # Disease prevalence: 1%
    # Test sensitivity (true positive rate): 99%
    # Test specificity (true negative rate): 95%
    
    prevalence = 0.01
    sensitivity = 0.99
    specificity = 0.95
    
    print("Medical Test Scenario:")
    print(f"  Disease prevalence: {prevalence:.1%}")
    print(f"  Test sensitivity (P(+|disease)): {sensitivity:.1%}")
    print(f"  Test specificity (P(-|no disease)): {specificity:.1%}")
    
    # P(test positive) = P(+|disease)*P(disease) + P(+|no disease)*P(no disease)
    false_positive_rate = 1 - specificity
    p_positive = sensitivity * prevalence + false_positive_rate * (1 - prevalence)
    
    # Apply Bayes' theorem
    p_disease_given_positive = bayes_theorem(sensitivity, prevalence, p_positive)
    
    print(f"\nProbability of testing positive: {p_positive:.3f}")
    print(f"Probability of having disease given positive test: {p_disease_given_positive:.2%}")
    
    print("\nInterpretation:")
    print("  Even with a positive test, only ~17% actually have the disease!")
    print("  This is due to low disease prevalence causing many false positives.")
    
    # Alternative calculation using total probability
    print("\nUsing total probability for factory quality:")
    p_factory = [0.5, 0.3, 0.2]  # Production shares
    p_defect = [0.01, 0.02, 0.03]  # Defect rates per factory
    
    total_defect = total_probability(p_defect, p_factory)
    print(f"  Factory shares: {p_factory}")
    print(f"  Defect rates: {p_defect}")
    print(f"  Overall defect rate: {total_defect:.3f} ({total_defect:.1%})")


def example_correlation_analysis():
    """Example: Correlation and covariance analysis."""
    print("\n" + "="*60)
    print("Example 9: Correlation Analysis")
    print("="*60)
    
    # Study time vs test scores
    study_hours = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    test_scores = [65, 70, 75, 78, 82, 85, 88, 92, 95]
    
    print(f"Study Hours: {study_hours}")
    print(f"Test Scores: {test_scores}")
    
    # Calculate correlation
    r = correlation(study_hours, test_scores)
    print(f"\nCorrelation coefficient (r): {r:.4f}")
    print(f"Strong positive correlation!")
    
    # Covariance
    cov = covariance(study_hours, test_scores)
    print(f"Covariance: {cov:.2f}")
    
    # Geometric and harmonic means
    print(f"\nAlternative Mean Measures:")
    print(f"  Geometric mean of study hours: {geometric_mean(study_hours):.2f}")
    print(f"  Harmonic mean of study hours: {harmonic_mean(study_hours):.2f}")
    print(f"  Arithmetic mean: {mean(study_hours):.2f}")


def example_random_sampling():
    """Example: Random sampling from distributions."""
    print("\n" + "="*60)
    print("Example 10: Random Sampling Simulation")
    print("="*60)
    
    # Using distribution classes to generate samples
    print("Generating random samples from different distributions:")
    
    # Normal distribution samples
    norm = NormalDistribution(mean=50, std=10)
    norm_samples = norm.samples(5)
    print(f"\nNormal(μ=50, σ=10) samples: {[round(x, 1) for x in norm_samples]}")
    
    # Binomial distribution samples
    binom = BinomialDistribution(n=10, p=0.3)
    binom_samples = binom.samples(5)
    print(f"Binomial(n=10, p=0.3) samples: {binom_samples}")
    
    # Poisson distribution samples
    pois = PoissonDistribution(lambda_=4)
    pois_samples = pois.samples(5)
    print(f"Poisson(λ=4) samples: {pois_samples}")
    
    # Exponential distribution samples
    exp = ExponentialDistribution(lambda_=0.5)
    exp_samples = exp.samples(5)
    print(f"Exponential(λ=0.5) samples: {[round(x, 2) for x in exp_samples]}")
    
    # Uniform distribution samples
    unif = UniformDistribution(a=0, b=100)
    unif_samples = unif.samples(5)
    print(f"Uniform(a=0, b=100) samples: {[round(x, 1) for x in unif_samples]}")


def example_combinatorics():
    """Example: Combinatorial calculations."""
    print("\n" + "="*60)
    print("Example 11: Combinatorial Calculations")
    print("="*60)
    
    # Lottery example
    print("Lottery Scenario:")
    total_numbers = 49
    pick_numbers = 6
    
    total_combinations = combination(total_numbers, pick_numbers)
    print(f"  Total numbers: {total_numbers}")
    print(f"  Pick: {pick_numbers}")
    print(f"  Total possible combinations: {total_combinations}")
    print(f"  Probability of winning: 1/{total_combinations}")
    
    # Committee selection
    print("\nCommittee Selection:")
    n_people = 12
    committee_size = 5
    
    ways = combination(n_people, committee_size)
    print(f"  {n_people} people, select committee of {committee_size}")
    print(f"  Number of ways: {ways}")
    
    # Arrangements (permutations)
    print("\nPermutations:")
    n = 8
    k = 3
    print(f"  Number of ways to arrange {k} items from {n}: {permutation(n, k)}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("AllToolkit - Probability Distribution Utilities Examples")
    print("="*60)
    
    example_basic_statistics()
    example_normal_distribution()
    example_standardization()
    example_binomial_distribution()
    example_poisson_distribution()
    example_confidence_intervals()
    example_hypothesis_testing()
    example_bayes_theorem()
    example_correlation_analysis()
    example_random_sampling()
    example_combinatorics()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()