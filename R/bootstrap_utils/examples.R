# Bootstrap Utilities Examples
# Demonstrating usage of bootstrap_utils.R

source("bootstrap_utils.R")

cat("========================================\n")
cat("Bootstrap Utilities Examples\n")
cat("========================================\n\n")

# Example 1: Basic Bootstrap Confidence Interval
cat("Example 1: Basic Bootstrap CI for Mean\n")
cat("--------------------------------------\n")
set.seed(42)
data <- rnorm(100, mean = 50, sd = 10)

# Compute 95% CI using percentile method
ci <- bootstrap_ci(data, n_samples = 5000, confidence = 0.95, 
                   method = "percentile", seed = 123)
cat(sprintf("Sample mean: %.4f\n", mean(data)))
cat(sprintf("Bootstrap SE: %.4f\n", ci$se))
cat(sprintf("95%% CI: [%.4f, %.4f]\n\n", ci$lower, ci$upper))

# Example 2: Different CI Methods Comparison
cat("Example 2: Comparing CI Methods\n")
cat("-------------------------------\n")
methods <- c("percentile", "basic", "normal", "bca")
for (method in methods) {
  ci <- bootstrap_ci(data, n_samples = 2000, method = method, seed = 456)
  cat(sprintf("%10s CI: [%.4f, %.4f] (width: %.4f)\n", 
              method, ci$lower, ci$upper, ci$upper - ci$lower))
}
cat("\n")

# Example 3: Bootstrap for Different Statistics
cat("Example 3: Bootstrap for Median and Trimmed Mean\n")
cat("------------------------------------------------\n")
ci_median <- bootstrap_ci(data, statistic = median, n_samples = 2000, seed = 789)
ci_trimmed <- bootstrap_ci(data, statistic = function(x) mean(x, trim = 0.1),
                           n_samples = 2000, seed = 789)

cat(sprintf("Median: %.4f, 95%% CI: [%.4f, %.4f]\n", 
            ci_median$estimate, ci_median$lower, ci_median$upper))
cat(sprintf("10%% Trimmed Mean: %.4f, 95%% CI: [%.4f, %.4f]\n\n",
            ci_trimmed$estimate, ci_trimmed$lower, ci_trimmed$upper))

# Example 4: Bootstrap Hypothesis Test
cat("Example 4: Bootstrap Hypothesis Test\n")
cat("-----------------------------------\n")
# Test if mean equals 50 (true value)
result <- bootstrap_test(data, null_value = 50, n_samples = 5000,
                         alternative = "two.sided", seed = 111)
cat(sprintf("H0: mean = 50\n"))
cat(sprintf("Sample mean: %.4f\n", result$statistic))
cat(sprintf("P-value: %.4f\n", result$p_value))
cat(sprintf("Reject H0: %s\n\n", result$reject_h0))

# Test if mean equals 55 (false)
result2 <- bootstrap_test(data, null_value = 55, n_samples = 5000,
                          alternative = "two.sided", seed = 222)
cat(sprintf("H0: mean = 55\n"))
cat(sprintf("Sample mean: %.4f\n", result2$statistic))
cat(sprintf("P-value: %.4f\n", result2$p_value))
cat(sprintf("Reject H0: %s\n\n", result2$reject_h0))

# Example 5: Two-Sample Bootstrap Test
cat("Example 5: Two-Sample Bootstrap Test\n")
cat("-------------------------------------\n")
set.seed(42)
group_a <- rnorm(50, mean = 100, sd = 15)
group_b <- rnorm(50, mean = 110, sd = 15)

two_sample <- bootstrap_two_sample(group_a, group_b, n_samples = 5000, seed = 333)
cat(sprintf("Group A mean: %.4f\n", mean(group_a)))
cat(sprintf("Group B mean: %.4f\n", mean(group_b)))
cat(sprintf("Difference: %.4f\n", two_sample$statistic))
cat(sprintf("P-value: %.4f\n", two_sample$p_value))
cat(sprintf("95%% CI for difference: [%.4f, %.4f]\n\n", 
            two_sample$ci_lower, two_sample$ci_upper))

# Example 6: Bootstrap Standard Error and Bias
cat("Example 6: Bootstrap SE and Bias Estimation\n")
cat("--------------------------------------------\n")
se <- bootstrap_se(data, statistic = mean, n_samples = 5000, seed = 444)
bias <- bootstrap_bias(data, statistic = mean, n_samples = 5000, seed = 555)
theoretical_se <- sd(data) / sqrt(length(data))

cat(sprintf("Bootstrap SE: %.4f\n", se))
cat(sprintf("Theoretical SE: %.4f\n", theoretical_se))
cat(sprintf("Relative error: %.2f%%\n", abs(se - theoretical_se) / theoretical_se * 100))
cat(sprintf("Bootstrap bias: %.6f\n\n", bias))

# Example 7: Jackknife Resampling
cat("Example 7: Jackknife Estimation\n")
cat("------------------------------\n")
jk <- jackknife(data, statistic = mean)
cat(sprintf("Original estimate: %.4f\n", jk$original))
cat(sprintf("Jackknife estimate: %.4f\n", jk$jackknife_estimate))
cat(sprintf("Jackknife SE: %.4f\n", jk$se))
cat(sprintf("Jackknife bias: %.6f\n\n", jk$bias))

# Example 8: Stratified Bootstrap
cat("Example 8: Stratified Bootstrap\n")
cat("-------------------------------\n")
set.seed(42)
strat_data <- data.frame(
  value = c(rnorm(30, mean = 10, sd = 2),
            rnorm(30, mean = 20, sd = 2),
            rnorm(30, mean = 30, sd = 2)),
  stratum = rep(c("Low", "Medium", "High"), each = 30)
)

boot_stats <- stratified_bootstrap(
  strat_data, "stratum",
  statistic = function(d) mean(d$value),
  n_samples = 2000, seed = 666
)
summ <- bootstrap_summary(boot_stats)
cat(sprintf("Overall mean from stratified bootstrap: %.4f\n", summ$mean))
cat(sprintf("Stratified bootstrap SE: %.4f\n", summ$sd))
cat(sprintf("95%% CI: [%.4f, %.4f]\n\n", summ$ci_lower, summ$ci_upper))

# Example 9: Block Bootstrap for Time Series
cat("Example 9: Block Bootstrap for Time Series\n")
cat("-------------------------------------------\n")
set.seed(42)
# Generate AR(1) time series
n_ts <- 200
ts_data <- numeric(n_ts)
ts_data[1] <- rnorm(1)
for (i in 2:n_ts) {
  ts_data[i] <- 0.7 * ts_data[i-1] + rnorm(1)
}

block_stats <- block_bootstrap(ts_data, block_size = 20,
                               statistic = mean, n_samples = 1000, seed = 777)
ts_summ <- bootstrap_summary(block_stats)
cat(sprintf("Time series mean: %.4f\n", mean(ts_data)))
cat(sprintf("Block bootstrap mean: %.4f\n", ts_summ$mean))
cat(sprintf("Block bootstrap SE: %.4f\n", ts_summ$sd))
cat(sprintf("95%% CI: [%.4f, %.4f]\n\n", ts_summ$ci_lower, ts_summ$ci_upper))

# Example 10: Parametric Bootstrap
cat("Example 10: Parametric Bootstrap\n")
cat("--------------------------------\n")
set.seed(42)
exp_data <- rexp(100, rate = 0.1)  # Mean = 10

# Fit exponential distribution and bootstrap
para_stats <- parametric_bootstrap(
  exp_data,
  statistic = mean,
  fit_dist = function(d) list(rate = 1/mean(d)),
  sample_dist = function(params, n) rexp(n, rate = params$rate),
  n_samples = 2000,
  seed = 888
)
para_summ <- bootstrap_summary(para_stats)
cat(sprintf("Sample mean: %.4f\n", mean(exp_data)))
cat(sprintf("Parametric bootstrap mean: %.4f\n", para_summ$mean))
cat(sprintf("Parametric bootstrap SE: %.4f\n", para_summ$sd))
cat(sprintf("95%% CI: [%.4f, %.4f]\n\n", para_summ$ci_lower, para_summ$ci_upper))

# Example 11: Bootstrap Regression
cat("Example 11: Bootstrap Regression Coefficients\n")
cat("----------------------------------------------\n")
set.seed(42)
reg_data <- data.frame(
  y = rnorm(100),
  x1 = rnorm(100),
  x2 = rnorm(100)
)
reg_data$y <- 2 + 1.5 * reg_data$x1 - 0.8 * reg_data$x2 + rnorm(100, sd = 0.5)

reg_result <- bootstrap_regression(y ~ x1 + x2, reg_data, n_samples = 1000, seed = 999)

cat("Bootstrap regression results:\n")
for (coef_name in names(reg_result$summary)) {
  s <- reg_result$summary[[coef_name]]
  cat(sprintf("  %s: %.4f (SE: %.4f, 95%% CI: [%.4f, %.4f])\n",
              coef_name, s$estimate, s$se, s$ci_lower, s$ci_upper))
}
cat("\n")

# Example 12: Acceleration Factor for BCa
cat("Example 12: Computing BCa Acceleration Factor\n")
cat("---------------------------------------------\n")
a <- compute_acceleration(data, statistic = mean)
cat(sprintf("Acceleration factor: %.6f\n", a))
cat("(Close to 0 suggests symmetric distribution)\n\n")

cat("========================================\n")
cat("All examples completed successfully!\n")
cat("========================================\n")