# Probability Distribution Utilities

A comprehensive Python library for probability distributions with **zero external dependencies**. Supports common distributions, statistical functions, and hypothesis testing.

## Features

### Supported Distributions

| Distribution | Continuous/Discrete | Parameters |
|--------------|---------------------|------------|
| Normal (Gaussian) | Continuous | μ (mean), σ (std) |
| Uniform | Continuous | a (lower), b (upper) |
| Exponential | Continuous | λ (rate) |
| Poisson | Discrete | λ (rate) |
| Binomial | Discrete | n (trials), p (probability) |
| Geometric | Discrete | p (probability) |
| Chi-Square | Continuous | df (degrees of freedom) |
| Student's t | Continuous | df (degrees of freedom) |
| Beta | Continuous | α, β (shape parameters) |
| Gamma | Continuous | k (shape), θ (scale) |
| F | Continuous | df1, df2 (degrees of freedom) |
| Weibull | Continuous | k (shape), λ (scale) |
| Log-Normal | Continuous | μ, σ (log parameters) |

### Common Methods

All distributions support:
- `pdf(x)` / `pmf(k)` - Probability density/mass function
- `cdf(x)` - Cumulative distribution function
- `quantile(p)` - Inverse CDF (percent point function)
- `sample(n)` - Generate n random samples
- `sample_one()` - Generate a single random sample
- `mean` - Expected value
- `variance` - Variance
- `std` - Standard deviation
- `interval(confidence)` - Confidence interval

### Statistical Functions

- `z_score(x, mu, sigma)` - Calculate z-score
- `p_value_one_tailed(z)` - One-tailed p-value
- `p_value_two_tailed(z)` - Two-tailed p-value
- `confidence_interval(mean, std, n, confidence)` - Sample confidence interval

### Hypothesis Tests

- `z_test()` - One-sample z-test
- `t_test()` - One-sample t-test

## Installation

No installation required! Just copy the file to your project:

```python
from probability_distribution_utils import NormalDistribution, BinomialDistribution
```

## Quick Start

### Normal Distribution

```python
from probability_distribution_utils import NormalDistribution

# Create a normal distribution with mean=100, std=15
normal = NormalDistribution(100, 15)

# Basic properties
print(f"Mean: {normal.mean}")          # 100
print(f"Variance: {normal.variance}")  # 225

# PDF and CDF
print(f"PDF at 100: {normal.pdf(100):.6f}")    # Peak value
print(f"CDF at 100: {normal.cdf(100):.6f}")    # 0.5

# Quantile (inverse CDF)
print(f"95th percentile: {normal.quantile(0.95):.2f}")  # ~124.67

# 95% confidence interval
ci_low, ci_high = normal.interval(0.95)
print(f"95% CI: ({ci_low:.2f}, {ci_high:.2f})")

# Generate random samples
samples = normal.sample(1000)
print(f"Sample mean: {sum(samples)/len(samples):.2f}")
```

### Binomial Distribution

```python
from probability_distribution_utils import BinomialDistribution

# 10 coin flips, p=0.5
binom = BinomialDistribution(10, 0.5)

# Probability mass function
print(f"P(X=5): {binom.pmf(5):.6f}")  # ~0.246

# Cumulative distribution
print(f"P(X≤5): {binom.cdf(5):.6f}")   # ~0.623

# Generate samples (simulate 10 experiments)
samples = binom.sample(10)
print(f"Samples: {samples}")
```

### Poisson Distribution

```python
from probability_distribution_utils import PoissonDistribution

# Average 3 events per interval
poisson = PoissonDistribution(3.0)

# Probability of exactly 5 events
print(f"P(X=5): {poisson.pmf(5):.6f}")

# Generate samples
samples = poisson.sample(100)
print(f"Average events: {sum(samples)/len(samples):.2f}")
```

### Hypothesis Testing

```python
from probability_distribution_utils import t_test, z_test

# One-sample t-test
result = t_test(
    sample_mean=105,
    sample_std=15,
    population_mean=100,
    n=25
)
print(f"t-statistic: {result['t_statistic']:.4f}")
print(f"p-value (two-tailed): {result['p_value_two_tailed']:.4f}")

# One-sample z-test (when population std is known)
result = z_test(
    sample_mean=105,
    population_mean=100,
    population_std=15,
    n=25
)
print(f"z-score: {result['z_score']:.4f}")
print(f"p-value (two-tailed): {result['p_value_two_tailed']:.4f}")
```

### Convenience Functions

```python
from probability_distribution_utils import (
    normal_pdf, normal_cdf, normal_quantile,
    normal_sample, z_score, p_value_two_tailed
)

# Quick normal distribution functions
print(f"PDF at 0: {normal_pdf(0):.6f}")          # Standard normal
print(f"CDF at 0: {normal_cdf(0):.6f}")          # 0.5
print(f"Quantile(0.975): {normal_quantile(0.975):.4f}")  # ~1.96

# Z-score calculation
z = z_score(130, 100, 15)  # (130-100)/15 = 2
print(f"Z-score: {z:.2f}")

# P-value for hypothesis testing
p = p_value_two_tailed(1.96)  # ~0.05
print(f"P-value: {p:.4f}")
```

## Advanced Usage

### Beta Distribution (Bayesian Inference)

```python
from probability_distribution_utils import BetaDistribution

# Prior: Beta(2, 2) - weak prior belief
prior = BetaDistribution(2, 2)

# After observing 10 successes and 5 failures
# Posterior: Beta(2+10, 2+5) = Beta(12, 7)
posterior = BetaDistribution(12, 7)

print(f"Posterior mean: {posterior.mean:.4f}")  # 12/19 ≈ 0.63
print(f"95% CI: {posterior.interval(0.95)}")
```

### Weibull Distribution (Reliability Analysis)

```python
from probability_distribution_utils import WeibullDistribution

# Weibull with shape=2, scale=100 (Rayleigh-like)
weibull = WeibullDistribution(shape=2, scale=100)

# Reliability at time t=100
reliability = 1 - weibull.cdf(100)
print(f"Reliability at t=100: {reliability:.4f}")

# 95th percentile (time by which 95% fail)
p95 = weibull.quantile(0.95)
print(f"95th percentile: {p95:.2f}")
```

### F-Distribution (ANOVA)

```python
from probability_distribution_utils import FDistribution

# F-distribution with df1=3, df2=20
f_dist = FDistribution(3, 20)

# Critical value for alpha=0.05
critical = f_dist.quantile(0.95)
print(f"Critical F(3,20) at α=0.05: {critical:.4f}")

# P-value for observed F=5.0
p_value = 1 - f_dist.cdf(5.0)
print(f"P-value for F=5.0: {p_value:.4f}")
```

## Mathematical Functions

The library includes several mathematical utility functions:

```python
from probability_distribution_utils import (
    _factorial,      # Factorial
    _gamma_function, # Gamma function
    _beta_function,  # Beta function
    _erf,            # Error function
)

# Factorial
print(_factorial(5))  # 120

# Gamma function (Γ(n) = (n-1)! for integers)
print(_gamma_function(6))  # 120

# Beta function
print(_beta_function(2, 3))  # 1/12

# Error function
print(_erf(1))  # ~0.8427
```

## Algorithm Details

### Random Number Generation

- **Normal**: Box-Muller transform
- **Exponential**: Inverse transform
- **Poisson**: Knuth's algorithm
- **Binomial**: Direct simulation
- **Geometric**: Direct simulation
- **Chi-Square**: Sum of squared normal variates
- **Student's t**: Normal / sqrt(Chi-Square / df)
- **Beta**: Gamma ratio transformation
- **Gamma**: Marsaglia and Tsang's method
- **F**: Chi-Square ratio
- **Weibull**: Inverse transform
- **Log-Normal**: Exponential of normal

### Numerical Methods

- **Gamma function**: Lanczos approximation
- **Beta function**: Via gamma function relation
- **Error function**: Horner's method approximation
- **Normal quantile**: Rational approximation (Abramowitz & Stegun)
- **Incomplete gamma**: Series expansion and continued fraction
- **Incomplete beta**: Continued fraction expansion

## Testing

Run the test suite:

```bash
python probability_distribution_utils_test.py
```

## Zero Dependencies

This library uses only Python's standard library:
- `math` - Mathematical functions
- `random` - Random number generation
- `typing` - Type hints

No numpy, scipy, or other external packages required!

## License

MIT License - Free for personal and commercial use.

## Author

AllToolkit - 2026-04-29