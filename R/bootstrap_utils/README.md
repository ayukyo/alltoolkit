# Bootstrap Utilities for R

Statistical bootstrap methods for resampling and inference - zero external dependencies.

## Features

- **Bootstrap Confidence Intervals**: Percentile, Basic, Normal, BCa methods
- **Bootstrap Hypothesis Testing**: One-sample and two-sample tests
- **Standard Error & Bias Estimation**: Bootstrap SE and bias calculations
- **Stratified Bootstrap**: For stratified sampling
- **Block Bootstrap**: For time series data
- **Parametric Bootstrap**: With custom distribution fitting
- **Jackknife Resampling**: Leave-one-out resampling
- **Bootstrap Regression**: For regression coefficients

## Installation

Copy `bootstrap_utils.R` to your project and source it:

```r
source("bootstrap_utils.R")
```

## Quick Start

```r
# Basic bootstrap confidence interval
set.seed(42)
data <- rnorm(100, mean = 50, sd = 10)

ci <- bootstrap_ci(data, n_samples = 5000, confidence = 0.95)
cat(sprintf("Mean: %.4f, 95%% CI: [%.4f, %.4f]\n", 
            ci$estimate, ci$lower, ci$upper))
```

## Usage Examples

### Bootstrap Confidence Intervals

```r
# Percentile method (default)
ci <- bootstrap_ci(data, n_samples = 2000, method = "percentile")

# Basic (reverse percentile) method
ci <- bootstrap_ci(data, n_samples = 2000, method = "basic")

# Normal approximation
ci <- bootstrap_ci(data, n_samples = 2000, method = "normal")

# BCa (Bias-Corrected and Accelerated) - most accurate
ci <- bootstrap_ci(data, n_samples = 2000, method = "bca")
```

### Custom Statistics

```r
# Bootstrap for median
ci_median <- bootstrap_ci(data, statistic = median, n_samples = 2000)

# Bootstrap for trimmed mean
ci_trimmed <- bootstrap_ci(data, 
                           statistic = function(x) mean(x, trim = 0.1),
                           n_samples = 2000)

# Bootstrap for standard deviation
ci_sd <- bootstrap_ci(data, statistic = sd, n_samples = 2000)
```

### Hypothesis Testing

```r
# Test if mean equals a null value
result <- bootstrap_test(data, null_value = 50, 
                         alternative = "two.sided",
                         n_samples = 5000)

cat(sprintf("P-value: %.4f, Reject H0: %s\n", 
            result$p_value, result$reject_h0))

# One-sided tests
result <- bootstrap_test(data, null_value = 55, 
                         alternative = "less")
```

### Two-Sample Test

```r
group_a <- rnorm(50, mean = 100, sd = 15)
group_b <- rnorm(50, mean = 105, sd = 15)

result <- bootstrap_two_sample(group_a, group_b, n_samples = 5000)

# Custom comparison statistic (e.g., ratio of means)
result <- bootstrap_two_sample(group_a, group_b,
  statistic = function(a, b) mean(a) / mean(b))
```

### Stratified Bootstrap

```r
# Data with strata
strat_data <- data.frame(
  value = c(rnorm(30, mean = 10), rnorm(30, mean = 20)),
  stratum = rep(c("A", "B"), each = 30)
)

boot_stats <- stratified_bootstrap(
  strat_data, "stratum",
  statistic = function(d) mean(d$value),
  n_samples = 2000
)
```

### Block Bootstrap for Time Series

```r
# Time series with autocorrelation
ts_data <- cumsum(rnorm(100))

boot_stats <- block_bootstrap(
  ts_data, 
  block_size = 10,
  statistic = mean,
  n_samples = 2000
)
```

### Parametric Bootstrap

```r
# For exponential data
exp_data <- rexp(100, rate = 0.1)

boot_stats <- parametric_bootstrap(
  exp_data,
  statistic = mean,
  fit_dist = function(d) list(rate = 1/mean(d)),
  sample_dist = function(params, n) rexp(n, rate = params$rate),
  n_samples = 2000
)
```

### Jackknife Resampling

```r
jk <- jackknife(data, statistic = mean)

cat(sprintf("Jackknife estimate: %.4f\n", jk$jackknife_estimate))
cat(sprintf("Jackknife SE: %.4f\n", jk$se))
cat(sprintf("Jackknife bias: %.6f\n", jk$bias))
```

### Bootstrap Regression

```r
reg_data <- data.frame(
  y = rnorm(100),
  x1 = rnorm(100),
  x2 = rnorm(100)
)

result <- bootstrap_regression(y ~ x1 + x2, reg_data, n_samples = 1000)

# View coefficient summary
for (coef_name in names(result$summary)) {
  s <- result$summary[[coef_name]]
  cat(sprintf("%s: %.4f (SE: %.4f)\n", coef_name, s$estimate, s$se))
}
```

## API Reference

### `generate_bootstrap_samples(data, n_samples, seed)`
Generate bootstrap sample matrix.

### `bootstrap_ci(data, statistic, n_samples, confidence, method, seed)`
Compute bootstrap confidence interval.
- `method`: "percentile", "basic", "bca", or "normal"

### `bootstrap_test(data, null_value, statistic, n_samples, alternative, seed)`
Bootstrap hypothesis test.
- `alternative`: "two.sided", "less", or "greater"

### `bootstrap_two_sample(x, y, statistic, n_samples, seed)`
Two-sample bootstrap test.

### `bootstrap_se(data, statistic, n_samples, seed)`
Bootstrap standard error.

### `bootstrap_bias(data, statistic, n_samples, seed)`
Bootstrap bias estimate.

### `stratified_bootstrap(data, strata_col, statistic, n_samples, seed)`
Stratified bootstrap for stratified sampling.

### `block_bootstrap(data, block_size, statistic, n_samples, seed)`
Block bootstrap for time series.

### `bootstrap_summary(boot_stats, confidence)`
Summary statistics for bootstrap distribution.

### `parametric_bootstrap(data, statistic, fit_dist, sample_dist, n_samples, seed)`
Parametric bootstrap with custom distribution.

### `jackknife(data, statistic)`
Jackknife leave-one-out resampling.

### `bootstrap_regression(formula, data, n_samples, seed)`
Bootstrap for regression coefficients.

### `compute_acceleration(data, statistic)`
Compute BCa acceleration factor.

## Testing

Run tests with:

```bash
Rscript test_bootstrap_utils.R
```

## Examples

See `examples.R` for comprehensive usage demonstrations:

```bash
Rscript examples.R
```

## Dependencies

- **R** >= 3.0.0
- **No external packages required** - pure R implementation

## References

- Efron, B., & Tibshirani, R. J. (1993). An Introduction to the Bootstrap
- Davison, A. C., & Hinkley, D. V. (1997). Bootstrap Methods and Their Application