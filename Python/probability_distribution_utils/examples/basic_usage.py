#!/usr/bin/env python3
"""
Probability Distribution Utilities - Examples

This script demonstrates various use cases for the probability distribution library.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from probability_distribution_utils import (
    NormalDistribution,
    UniformDistribution,
    ExponentialDistribution,
    PoissonDistribution,
    BinomialDistribution,
    GeometricDistribution,
    ChiSquareDistribution,
    StudentTDistribution,
    BetaDistribution,
    GammaDistribution,
    FDistribution,
    WeibullDistribution,
    LogNormalDistribution,
    confidence_interval,
    z_test,
    t_test,
)


def example_normal_distribution():
    """Example: Normal distribution for IQ scores."""
    print("\n" + "=" * 60)
    print("Example 1: Normal Distribution (IQ Scores)")
    print("=" * 60)
    
    # IQ scores follow a normal distribution with mean=100, std=15
    iq = NormalDistribution(100, 15)
    
    print(f"\nDistribution properties:")
    print(f"  Mean IQ: {iq.mean}")
    print(f"  Standard deviation: {iq.std}")
    
    print(f"\nProbabilities:")
    print(f"  P(IQ < 85): {iq.cdf(85):.4f} (below average)")
    print(f"  P(IQ > 115): {1 - iq.cdf(115):.4f} (above average)")
    print(f"  P(85 < IQ < 115): {iq.cdf(115) - iq.cdf(85):.4f} (average range)")
    
    print(f"\nPercentiles:")
    print(f"  50th percentile (median): {iq.quantile(0.5):.1f}")
    print(f"  90th percentile: {iq.quantile(0.9):.1f}")
    print(f"  99th percentile: {iq.quantile(0.99):.1f}")
    
    print(f"\n95% confidence interval: {iq.interval(0.95)}")


def example_binomial_distribution():
    """Example: Binomial distribution for quality control."""
    print("\n" + "=" * 60)
    print("Example 2: Binomial Distribution (Quality Control)")
    print("=" * 60)
    
    # A factory produces items with 5% defect rate
    # Sample 20 items per batch
    defect = BinomialDistribution(20, 0.05)
    
    print(f"\nDistribution properties:")
    print(f"  Expected defects per batch: {defect.mean:.2f}")
    print(f"  Standard deviation: {defect.std:.2f}")
    
    print(f"\nProbabilities:")
    print(f"  P(0 defects): {defect.pmf(0):.4f}")
    print(f"  P(1 defect): {defect.pmf(1):.4f}")
    print(f"  P(2 defects): {defect.pmf(2):.4f}")
    print(f"  P(≤2 defects): {defect.cdf(2):.4f}")
    print(f"  P(>3 defects): {1 - defect.cdf(3):.4f}")
    
    print(f"\nSimulating 10 batches:")
    samples = defect.sample(10)
    print(f"  Defects per batch: {samples}")


def example_poisson_distribution():
    """Example: Poisson distribution for call center."""
    print("\n" + "=" * 60)
    print("Example 3: Poisson Distribution (Call Center)")
    print("=" * 60)
    
    # Call center receives average 5 calls per minute
    calls = PoissonDistribution(5.0)
    
    print(f"\nDistribution properties:")
    print(f"  Average calls per minute: {calls.mean}")
    print(f"  Variance: {calls.variance}")
    
    print(f"\nProbabilities:")
    print(f"  P(0 calls in a minute): {calls.pmf(0):.4f}")
    print(f"  P(5 calls in a minute): {calls.pmf(5):.4f}")
    print(f"  P(≤5 calls in a minute): {calls.cdf(5):.4f}")
    print(f"  P(>10 calls in a minute): {1 - calls.cdf(10):.4f}")
    
    print(f"\nSimulating 10 minutes:")
    samples = calls.sample(10)
    print(f"  Calls per minute: {samples}")


def example_exponential_distribution():
    """Example: Exponential distribution for wait times."""
    print("\n" + "=" * 60)
    print("Example 4: Exponential Distribution (Wait Times)")
    print("=" * 60)
    
    # Average wait time of 10 minutes
    wait_time = ExponentialDistribution(1/10)  # rate = 1/mean
    
    print(f"\nDistribution properties:")
    print(f"  Mean wait time: {wait_time.mean:.2f} minutes")
    print(f"  Median wait time: {wait_time.quantile(0.5):.2f} minutes")
    
    print(f"\nProbabilities:")
    print(f"  P(wait < 5 min): {wait_time.cdf(5):.4f}")
    print(f"  P(wait < 10 min): {wait_time.cdf(10):.4f}")
    print(f"  P(wait > 20 min): {1 - wait_time.cdf(20):.4f}")
    
    print(f"\nPercentiles:")
    print(f"  75th percentile: {wait_time.quantile(0.75):.2f} minutes")
    print(f"  90th percentile: {wait_time.quantile(0.90):.2f} minutes")


def example_beta_distribution():
    """Example: Beta distribution for Bayesian inference."""
    print("\n" + "=" * 60)
    print("Example 5: Beta Distribution (A/B Testing)")
    print("=" * 60)
    
    # After observing 150 successes out of 200 trials
    # Prior: Beta(1, 1) = Uniform
    # Posterior: Beta(1+150, 1+50) = Beta(151, 51)
    posterior = BetaDistribution(151, 51)
    
    print(f"\nExperiment results: 150 successes out of 200 trials")
    print(f"Posterior distribution: Beta(151, 51)")
    
    print(f"\nPoint estimates:")
    print(f"  Posterior mean: {posterior.mean:.4f}")
    print(f"  Posterior mode: {(151-1)/(151+51-2):.4f}")
    
    print(f"\nCredible intervals:")
    print(f"  95% CI: ({posterior.quantile(0.025):.4f}, {posterior.quantile(0.975):.4f})")
    print(f"  99% CI: ({posterior.quantile(0.005):.4f}, {posterior.quantile(0.995):.4f})")
    
    print(f"\nProbability conversion rate > 70%:")
    print(f"  P(θ > 0.70): {1 - posterior.cdf(0.70):.4f}")


def example_chi_square_distribution():
    """Example: Chi-square distribution for goodness of fit."""
    print("\n" + "=" * 60)
    print("Example 6: Chi-Square Distribution (Goodness of Fit)")
    print("=" * 60)
    
    # Chi-square test with 5 degrees of freedom
    chi = ChiSquareDistribution(5)
    
    print(f"\nDistribution properties:")
    print(f"  Degrees of freedom: 5")
    print(f"  Mean: {chi.mean}")
    print(f"  Variance: {chi.variance}")
    
    print(f"\nCritical values:")
    print(f"  α=0.05: {chi.quantile(0.95):.4f}")
    print(f"  α=0.01: {chi.quantile(0.99):.4f}")
    
    # Suppose we calculated χ² = 12.0
    observed_chi = 12.0
    p_value = 1 - chi.cdf(observed_chi)
    
    print(f"\nHypothesis test (observed χ² = {observed_chi}):")
    print(f"  P-value: {p_value:.4f}")
    if p_value < 0.05:
        print(f"  Result: Reject null hypothesis at α=0.05")
    else:
        print(f"  Result: Fail to reject null hypothesis at α=0.05")


def example_student_t_distribution():
    """Example: Student's t-distribution for small samples."""
    print("\n" + "=" * 60)
    print("Example 7: Student's t-Distribution (Small Sample)")
    print("=" * 60)
    
    # t-distribution with 10 degrees of freedom
    t_dist = StudentTDistribution(10)
    
    print(f"\nDistribution properties:")
    print(f"  Degrees of freedom: 10")
    print(f"  Mean: {t_dist.mean}")
    print(f"  Variance: {t_dist.variance:.4f}")
    
    print(f"\nCritical values (two-tailed):")
    print(f"  α=0.10: ±{t_dist.quantile(0.95):.4f}")
    print(f"  α=0.05: ±{t_dist.quantile(0.975):.4f}")
    print(f"  α=0.01: ±{t_dist.quantile(0.995):.4f}")
    
    print(f"\nComparison with normal distribution:")
    normal = NormalDistribution(0, 1)
    print(f"  Normal(0,1) 95% critical: ±{normal.quantile(0.975):.4f}")
    print(f"  t(10) 95% critical: ±{t_dist.quantile(0.975):.4f}")
    print(f"  (t-distribution has heavier tails)")


def example_f_distribution():
    """Example: F-distribution for ANOVA."""
    print("\n" + "=" * 60)
    print("Example 8: F-Distribution (ANOVA)")
    print("=" * 60)
    
    # F-distribution for comparing 3 groups (df1=2) with 30 total subjects (df2=27)
    f_dist = FDistribution(2, 27)
    
    print(f"\nANOVA setup:")
    print(f"  Number of groups: 3 (df1 = k-1 = 2)")
    print(f"  Total subjects: 30 (df2 = n-k = 27)")
    
    print(f"\nDistribution properties:")
    print(f"  Mean: {f_dist.mean:.4f}")
    
    print(f"\nCritical values:")
    print(f"  α=0.05: {f_dist.quantile(0.95):.4f}")
    print(f"  α=0.01: {f_dist.quantile(0.99):.4f}")
    
    # Suppose F-statistic = 4.5
    observed_f = 4.5
    p_value = 1 - f_dist.cdf(observed_f)
    
    print(f"\nHypothesis test (observed F = {observed_f}):")
    print(f"  P-value: {p_value:.4f}")


def example_weibull_distribution():
    """Example: Weibull distribution for reliability."""
    print("\n" + "=" * 60)
    print("Example 9: Weibull Distribution (Reliability Analysis)")
    print("=" * 60)
    
    # Component lifetime follows Weibull with shape=2, scale=1000 hours
    weibull = WeibullDistribution(shape=2, scale=1000)
    
    print(f"\nComponent lifetime distribution:")
    print(f"  Shape parameter (k): 2 (increasing failure rate)")
    print(f"  Scale parameter (λ): 1000 hours")
    
    print(f"\nReliability analysis:")
    print(f"  Mean lifetime: {weibull.mean:.2f} hours")
    print(f"  Median lifetime: {weibull.quantile(0.5):.2f} hours")
    
    print(f"\nSurvival probabilities:")
    print(f"  P(survive 500 hours): {1 - weibull.cdf(500):.4f}")
    print(f"  P(survive 1000 hours): {1 - weibull.cdf(1000):.4f}")
    print(f"  P(survive 2000 hours): {1 - weibull.cdf(2000):.4f}")
    
    print(f"\nPercentiles:")
    print(f"  10% fail by: {weibull.quantile(0.1):.2f} hours")
    print(f"  50% fail by: {weibull.quantile(0.5):.2f} hours")
    print(f"  90% fail by: {weibull.quantile(0.9):.2f} hours")


def example_hypothesis_testing():
    """Example: Hypothesis testing."""
    print("\n" + "=" * 60)
    print("Example 10: Hypothesis Testing")
    print("=" * 60)
    
    # Scenario: Testing if a new teaching method improves test scores
    # Population mean = 75, Sample mean = 78, Sample std = 12, n = 25
    
    print(f"\nScenario: Testing new teaching method")
    print(f"  Population mean (μ₀): 75")
    print(f"  Sample mean (x̄): 78")
    print(f"  Sample std (s): 12")
    print(f"  Sample size (n): 25")
    
    # t-test (when population std is unknown)
    t_result = t_test(
        sample_mean=78,
        sample_std=12,
        population_mean=75,
        n=25
    )
    
    print(f"\nOne-sample t-test:")
    print(f"  t-statistic: {t_result['t_statistic']:.4f}")
    print(f"  p-value (one-tailed): {t_result['p_value_one_tailed']:.4f}")
    print(f"  p-value (two-tailed): {t_result['p_value_two_tailed']:.4f}")
    
    if t_result['p_value_two_tailed'] < 0.05:
        print(f"  Conclusion: Reject H₀ at α=0.05 (significant difference)")
    else:
        print(f"  Conclusion: Fail to reject H₀ at α=0.05")
    
    # Confidence interval
    ci = confidence_interval(mean=78, std=12, n=25, confidence=0.95)
    print(f"\n95% Confidence interval for population mean:")
    print(f"  ({ci[0]:.2f}, {ci[1]:.2f})")


def example_geometric_distribution():
    """Example: Geometric distribution for success counting."""
    print("\n" + "=" * 60)
    print("Example 11: Geometric Distribution (Sales Calls)")
    print("=" * 60)
    
    # Salesperson has 20% success rate on cold calls
    geom = GeometricDistribution(0.20)
    
    print(f"\nSales call scenario:")
    print(f"  Success rate per call: 20%")
    
    print(f"\nExpected number of calls:")
    print(f"  Mean calls until first sale: {geom.mean:.2f}")
    print(f"  Standard deviation: {geom.std:.2f}")
    
    print(f"\nProbabilities:")
    print(f"  P(sale on 1st call): {geom.pmf(1):.4f}")
    print(f"  P(sale on 2nd call): {geom.pmf(2):.4f}")
    print(f"  P(sale on 3rd call): {geom.pmf(3):.4f}")
    
    print(f"\nCumulative probabilities:")
    print(f"  P(sale within 3 calls): {geom.cdf(3):.4f}")
    print(f"  P(sale within 5 calls): {geom.cdf(5):.4f}")
    print(f"  P(sale within 10 calls): {geom.cdf(10):.4f}")


def example_lognormal_distribution():
    """Example: Log-normal distribution for income."""
    print("\n" + "=" * 60)
    print("Example 12: Log-Normal Distribution (Income)")
    print("=" * 60)
    
    # Annual income follows log-normal with mu=10.5, sigma=0.5
    income = LogNormalDistribution(10.5, 0.5)
    
    print(f"\nIncome distribution:")
    print(f"  Parameters: μ=10.5, σ=0.5 (log scale)")
    
    print(f"\nProperties:")
    print(f"  Mean income: ${income.mean:,.2f}")
    print(f"  Median income: ${income.quantile(0.5):,.2f}")
    
    print(f"\nPercentiles:")
    print(f"  10th percentile: ${income.quantile(0.10):,.2f}")
    print(f"  25th percentile: ${income.quantile(0.25):,.2f}")
    print(f"  50th percentile (median): ${income.quantile(0.50):,.2f}")
    print(f"  75th percentile: ${income.quantile(0.75):,.2f}")
    print(f"  90th percentile: ${income.quantile(0.90):,.2f}")
    
    print(f"\nProbability of income > $100,000:")
    print(f"  P(X > 100000): {1 - income.cdf(100000):.4f}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("PROBABILITY DISTRIBUTION UTILITIES - EXAMPLES")
    print("=" * 60)
    
    example_normal_distribution()
    example_binomial_distribution()
    example_poisson_distribution()
    example_exponential_distribution()
    example_beta_distribution()
    example_chi_square_distribution()
    example_student_t_distribution()
    example_f_distribution()
    example_weibull_distribution()
    example_hypothesis_testing()
    example_geometric_distribution()
    example_lognormal_distribution()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()