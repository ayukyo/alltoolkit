"""
Tests for Probability Distribution Utilities

Author: AllToolkit
Date: 2026-04-29
"""

import math
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from probability_distribution_utils import (
    # Distribution classes
    Distribution,
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
    # Convenience functions
    normal_pdf,
    normal_cdf,
    normal_quantile,
    normal_sample,
    confidence_interval,
    z_score,
    p_value_one_tailed,
    p_value_two_tailed,
    # Statistical tests
    z_test,
    t_test,
    # Helper functions
    _factorial,
    _gamma_function,
    _beta_function,
    _erf,
)


def test_factorial():
    """Test factorial function."""
    print("Testing factorial...")
    assert _factorial(0) == 1
    assert _factorial(1) == 1
    assert _factorial(5) == 120
    assert _factorial(10) == 3628800
    print("  factorial: PASS")


def test_gamma_function():
    """Test gamma function."""
    print("Testing gamma function...")
    # Gamma(n) = (n-1)! for positive integers
    assert abs(_gamma_function(1) - 1) < 1e-10
    assert abs(_gamma_function(2) - 1) < 1e-10
    assert abs(_gamma_function(3) - 2) < 1e-10
    assert abs(_gamma_function(4) - 6) < 1e-10
    assert abs(_gamma_function(5) - 24) < 1e-10
    # Gamma(1/2) = sqrt(pi)
    assert abs(_gamma_function(0.5) - math.sqrt(math.pi)) < 1e-10
    print("  gamma_function: PASS")


def test_beta_function():
    """Test beta function."""
    print("Testing beta function...")
    # B(1,1) = 1
    assert abs(_beta_function(1, 1) - 1) < 1e-10
    # B(2,2) = 1/6
    assert abs(_beta_function(2, 2) - 1/6) < 1e-10
    # B(0.5, 0.5) = pi
    assert abs(_beta_function(0.5, 0.5) - math.pi) < 1e-10
    print("  beta_function: PASS")


def test_erf():
    """Test error function."""
    print("Testing error function...")
    assert abs(_erf(0) - 0) < 1e-10
    assert abs(_erf(1) - 0.8427007929) < 1e-6  # Approximation tolerance
    assert abs(_erf(-1) + 0.8427007929) < 1e-6
    assert abs(_erf(2) - 0.995322265) < 1e-6
    print("  erf: PASS")


def test_normal_distribution():
    """Test normal distribution."""
    print("Testing NormalDistribution...")
    normal = NormalDistribution(0, 1)
    
    # Test mean and variance
    assert abs(normal.mean - 0) < 1e-10
    assert abs(normal.variance - 1) < 1e-10
    assert abs(normal.std - 1) < 1e-10
    
    # Test PDF at x=0
    assert abs(normal.pdf(0) - 1/math.sqrt(2*math.pi)) < 1e-10
    
    # Test CDF at x=0 (should be 0.5) - allow small approximation error
    assert abs(normal.cdf(0) - 0.5) < 1e-9
    
    # Test quantile at 0.5 (should be 0)
    assert abs(normal.quantile(0.5) - 0) < 1e-10
    
    # Test quantile at 0.975 (should be approximately 1.96)
    assert abs(normal.quantile(0.975) - 1.96) < 0.01
    
    # Test 95% confidence interval
    ci_low, ci_high = normal.interval(0.95)
    assert abs(ci_low + 1.96) < 0.01
    assert abs(ci_high - 1.96) < 0.01
    
    # Test sampling
    samples = normal.sample(1000)
    assert len(samples) == 1000
    sample_mean = sum(samples) / len(samples)
    assert abs(sample_mean - 0) < 0.1  # Should be close to 0
    
    print("  NormalDistribution: PASS")


def test_normal_distribution_custom():
    """Test normal distribution with custom parameters."""
    print("Testing NormalDistribution (custom)...")
    normal = NormalDistribution(10, 2)
    
    assert abs(normal.mean - 10) < 1e-10
    assert abs(normal.variance - 4) < 1e-10
    
    # Test PDF
    expected = math.exp(-0.5 * ((12 - 10) / 2) ** 2) / (2 * math.sqrt(2 * math.pi))
    assert abs(normal.pdf(12) - expected) < 1e-10
    
    # Test quantile
    assert abs(normal.quantile(0.5) - 10) < 1e-10
    
    print("  NormalDistribution (custom): PASS")


def test_uniform_distribution():
    """Test uniform distribution."""
    print("Testing UniformDistribution...")
    uniform = UniformDistribution(0, 1)
    
    # Test mean and variance
    assert abs(uniform.mean - 0.5) < 1e-10
    assert abs(uniform.variance - 1/12) < 1e-10
    
    # Test PDF
    assert abs(uniform.pdf(0.5) - 1) < 1e-10
    assert abs(uniform.pdf(-0.5) - 0) < 1e-10
    assert abs(uniform.pdf(1.5) - 0) < 1e-10
    
    # Test CDF
    assert abs(uniform.cdf(0) - 0) < 1e-10
    assert abs(uniform.cdf(0.5) - 0.5) < 1e-10
    assert abs(uniform.cdf(1) - 1) < 1e-10
    
    # Test quantile
    assert abs(uniform.quantile(0) - 0) < 1e-10
    assert abs(uniform.quantile(0.5) - 0.5) < 1e-10
    assert abs(uniform.quantile(1) - 1) < 1e-10
    
    # Test sampling
    samples = uniform.sample(1000)
    assert len(samples) == 1000
    assert all(0 <= s <= 1 for s in samples)
    
    print("  UniformDistribution: PASS")


def test_exponential_distribution():
    """Test exponential distribution."""
    print("Testing ExponentialDistribution...")
    exp = ExponentialDistribution(1.0)
    
    # Test mean and variance
    assert abs(exp.mean - 1) < 1e-10
    assert abs(exp.variance - 1) < 1e-10
    
    # Test PDF
    assert abs(exp.pdf(0) - 1) < 1e-10
    assert abs(exp.pdf(-1) - 0) < 1e-10
    
    # Test CDF
    assert abs(exp.cdf(0) - 0) < 1e-10
    assert abs(exp.cdf(1) - (1 - 1/math.e)) < 1e-10
    
    # Test quantile
    assert abs(exp.quantile(0.5) - math.log(2)) < 1e-10
    
    # Test sampling
    samples = exp.sample(1000)
    assert len(samples) == 1000
    assert all(s >= 0 for s in samples)
    
    print("  ExponentialDistribution: PASS")


def test_poisson_distribution():
    """Test Poisson distribution."""
    print("Testing PoissonDistribution...")
    poisson = PoissonDistribution(3.0)
    
    # Test mean and variance
    assert abs(poisson.mean - 3) < 1e-10
    assert abs(poisson.variance - 3) < 1e-10
    
    # Test PMF
    assert abs(poisson.pmf(0) - math.exp(-3)) < 1e-10
    
    # Test CDF
    cdf_0 = poisson.pmf(0)
    assert abs(poisson.cdf(0) - cdf_0) < 1e-10
    
    # Test sampling
    samples = poisson.sample(1000)
    assert len(samples) == 1000
    assert all(isinstance(s, int) for s in samples)
    sample_mean = sum(samples) / len(samples)
    assert abs(sample_mean - 3) < 0.5  # Should be close to lambda
    
    print("  PoissonDistribution: PASS")


def test_binomial_distribution():
    """Test binomial distribution."""
    print("Testing BinomialDistribution...")
    binom = BinomialDistribution(10, 0.5)
    
    # Test mean and variance
    assert abs(binom.mean - 5) < 1e-10
    assert abs(binom.variance - 2.5) < 1e-10
    
    # Test PMF
    # P(X=5) for n=10, p=0.5 = C(10,5) * 0.5^10 = 252/1024
    expected_pmf_5 = 252 / 1024
    assert abs(binom.pmf(5) - expected_pmf_5) < 1e-10
    
    # Test CDF
    assert abs(binom.cdf(10) - 1) < 1e-10
    
    # Test sampling
    samples = binom.sample(1000)
    assert len(samples) == 1000
    assert all(0 <= s <= 10 for s in samples)
    
    print("  BinomialDistribution: PASS")


def test_geometric_distribution():
    """Test geometric distribution."""
    print("Testing GeometricDistribution...")
    geom = GeometricDistribution(0.3)
    
    # Test mean and variance
    expected_mean = 1 / 0.3
    expected_var = (1 - 0.3) / (0.3 ** 2)
    assert abs(geom.mean - expected_mean) < 1e-10
    assert abs(geom.variance - expected_var) < 1e-10
    
    # Test PMF
    # P(X=1) = p = 0.3
    assert abs(geom.pmf(1) - 0.3) < 1e-10
    
    # Test CDF
    # P(X<=1) = p = 0.3
    assert abs(geom.cdf(1) - 0.3) < 1e-10
    
    # Test sampling
    samples = geom.sample(1000)
    assert len(samples) == 1000
    assert all(s >= 1 for s in samples)
    
    print("  GeometricDistribution: PASS")


def test_chi_square_distribution():
    """Test chi-square distribution."""
    print("Testing ChiSquareDistribution...")
    chi = ChiSquareDistribution(5)
    
    # Test mean and variance
    assert abs(chi.mean - 5) < 1e-10
    assert abs(chi.variance - 10) < 1e-10
    
    # Test PDF
    assert chi.pdf(-1) == 0
    assert chi.pdf(0) == 0
    
    # Test CDF
    assert chi.cdf(0) == 0
    assert chi.cdf(100) > 0.999
    
    # Test sampling
    samples = chi.sample(1000)
    assert len(samples) == 1000
    assert all(s >= 0 for s in samples)
    
    print("  ChiSquareDistribution: PASS")


def test_student_t_distribution():
    """Test Student's t-distribution."""
    print("Testing StudentTDistribution...")
    t = StudentTDistribution(10)
    
    # Test mean (undefined for df<=1, 0 for df>1)
    assert abs(t.mean - 0) < 1e-10
    
    # Test PDF
    assert t.pdf(0) > 0
    
    # Test CDF
    assert abs(t.cdf(0) - 0.5) < 1e-10
    
    # Test sampling
    samples = t.sample(1000)
    assert len(samples) == 1000
    
    print("  StudentTDistribution: PASS")


def test_beta_distribution():
    """Test beta distribution."""
    print("Testing BetaDistribution...")
    beta = BetaDistribution(2, 5)
    
    # Test mean
    expected_mean = 2 / (2 + 5)
    assert abs(beta.mean - expected_mean) < 1e-10
    
    # Test PDF at boundaries
    assert beta.pdf(0) == 0
    assert beta.pdf(1) == 0
    
    # Test CDF
    assert beta.cdf(0) == 0
    assert abs(beta.cdf(1) - 1) < 1e-10
    
    # Test sampling
    samples = beta.sample(1000)
    assert len(samples) == 1000
    assert all(0 <= s <= 1 for s in samples)
    
    print("  BetaDistribution: PASS")


def test_gamma_distribution():
    """Test gamma distribution."""
    print("Testing GammaDistribution...")
    gamma = GammaDistribution(2, 2)
    
    # Test mean and variance
    assert abs(gamma.mean - 4) < 1e-10
    assert abs(gamma.variance - 8) < 1e-10
    
    # Test PDF
    assert gamma.pdf(-1) == 0
    assert gamma.pdf(0) == 0  # For shape > 1
    
    # Test CDF
    assert gamma.cdf(0) == 0
    assert gamma.cdf(100) > 0.999
    
    # Test sampling
    samples = gamma.sample(1000)
    assert len(samples) == 1000
    assert all(s >= 0 for s in samples)
    
    print("  GammaDistribution: PASS")


def test_f_distribution():
    """Test F-distribution."""
    print("Testing FDistribution...")
    f = FDistribution(5, 10)
    
    # Test mean (df2 > 2)
    expected_mean = 10 / 8
    assert abs(f.mean - expected_mean) < 1e-10
    
    # Test PDF
    assert f.pdf(0) == 0
    assert f.pdf(-1) == 0
    
    # Test CDF
    assert f.cdf(0) == 0
    assert f.cdf(100) > 0.999
    
    # Test sampling
    samples = f.sample(1000)
    assert len(samples) == 1000
    assert all(s >= 0 for s in samples)
    
    print("  FDistribution: PASS")


def test_weibull_distribution():
    """Test Weibull distribution."""
    print("Testing WeibullDistribution...")
    weib = WeibullDistribution(2, 1)  # Rayleigh distribution
    
    # Test PDF
    assert weib.pdf(-1) == 0
    
    # Test CDF
    assert weib.cdf(0) == 0
    assert abs(weib.cdf(100) - 1) < 1e-10
    
    # Test sampling
    samples = weib.sample(1000)
    assert len(samples) == 1000
    assert all(s >= 0 for s in samples)
    
    print("  WeibullDistribution: PASS")


def test_log_normal_distribution():
    """Test log-normal distribution."""
    print("Testing LogNormalDistribution...")
    lognorm = LogNormalDistribution(0, 1)
    
    # Test mean
    expected_mean = math.exp(0.5)
    assert abs(lognorm.mean - expected_mean) < 1e-10
    
    # Test PDF
    assert lognorm.pdf(0) == 0
    assert lognorm.pdf(-1) == 0
    
    # Test CDF
    assert lognorm.cdf(0) == 0
    assert abs(lognorm.cdf(math.e) - (0.5 + 0.5 * _erf(1/math.sqrt(2)))) < 1e-7
    
    # Test sampling
    samples = lognorm.sample(1000)
    assert len(samples) == 1000
    assert all(s > 0 for s in samples)
    
    print("  LogNormalDistribution: PASS")


def test_convenience_functions():
    """Test convenience functions."""
    print("Testing convenience functions...")
    
    # Test normal_pdf
    expected = 1 / math.sqrt(2 * math.pi)
    assert abs(normal_pdf(0) - expected) < 1e-10
    
    # Test normal_cdf - allow small approximation error
    assert abs(normal_cdf(0) - 0.5) < 1e-9
    
    # Test normal_quantile
    assert abs(normal_quantile(0.5) - 0) < 1e-10
    
    # Test normal_sample
    samples = normal_sample(0, 1, 100)
    assert len(samples) == 100
    
    # Test z_score
    assert abs(z_score(100, 80, 10) - 2) < 1e-10
    
    # Test p_value_one_tailed
    p = p_value_one_tailed(1.96)
    assert 0.02 < p < 0.03
    
    # Test p_value_two_tailed
    p = p_value_two_tailed(1.96)
    assert 0.04 < p < 0.06
    
    print("  Convenience functions: PASS")


def test_confidence_interval():
    """Test confidence interval function."""
    print("Testing confidence_interval...")
    
    # Test with known values
    ci = confidence_interval(100, 15, 25, 0.95)
    # For n=25, std=15, 95% CI uses t-distribution (n-1=24 df)
    # The interval should contain the mean
    assert ci[0] < 100 < ci[1]
    # Margin should be approximately t * std / sqrt(n) where t ~ 2.064 for df=24
    margin = (ci[1] - ci[0]) / 2
    expected_margin = 15 / math.sqrt(25)  # std / sqrt(n) = 3
    # margin = t * expected_margin, where t ~ 2.064
    assert margin > expected_margin  # t > 1.96 for small samples
    
    # Test with large n (uses normal approximation)
    ci_large = confidence_interval(100, 15, 100, 0.95)
    assert ci_large[0] < 100 < ci_large[1]
    # For n=100, margin ≈ 1.96 * 15/10 = 2.94
    assert abs((ci_large[1] - ci_large[0]) / 2 - 1.96 * 1.5) < 0.5
    
    print("  confidence_interval: PASS")


def test_z_test():
    """Test z-test function."""
    print("Testing z_test...")
    
    result = z_test(sample_mean=105, population_mean=100, population_std=15, n=25)
    
    # z = (105 - 100) / (15 / sqrt(25)) = 5 / 3 ≈ 1.67
    assert abs(result['z_score'] - 5/3) < 1e-10
    
    # p-value should be positive and less than 0.5
    assert 0 < result['p_value_two_tailed'] < 0.5
    
    print("  z_test: PASS")


def test_t_test():
    """Test t-test function."""
    print("Testing t_test...")
    
    result = t_test(sample_mean=105, sample_std=15, population_mean=100, n=25)
    
    # t = (105 - 100) / (15 / sqrt(25)) = 5 / 3 ≈ 1.67
    assert abs(result['t_statistic'] - 5/3) < 1e-10
    
    # p-value should be positive
    assert 0 < result['p_value_two_tailed'] < 0.5
    
    print("  t_test: PASS")


def test_edge_cases():
    """Test edge cases and error handling."""
    print("Testing edge cases...")
    
    # Test invalid parameters
    try:
        NormalDistribution(0, -1)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    try:
        BinomialDistribution(-1, 0.5)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    try:
        PoissonDistribution(-1)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    # Test boundary conditions
    normal = NormalDistribution(0, 1)
    assert normal.quantile(0) < -10
    assert normal.quantile(1) > 10
    
    print("  Edge cases: PASS")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Running Probability Distribution Utilities Tests")
    print("=" * 60 + "\n")
    
    tests = [
        test_factorial,
        test_gamma_function,
        test_beta_function,
        test_erf,
        test_normal_distribution,
        test_normal_distribution_custom,
        test_uniform_distribution,
        test_exponential_distribution,
        test_poisson_distribution,
        test_binomial_distribution,
        test_geometric_distribution,
        test_chi_square_distribution,
        test_student_t_distribution,
        test_beta_distribution,
        test_gamma_distribution,
        test_f_distribution,
        test_weibull_distribution,
        test_log_normal_distribution,
        test_convenience_functions,
        test_confidence_interval,
        test_z_test,
        test_t_test,
        test_edge_cases,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  FAILED: {test.__name__}")
            print(f"    Error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)