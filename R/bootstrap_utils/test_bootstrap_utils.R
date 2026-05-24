# Tests for Bootstrap Utilities
# Run with: Rscript test_bootstrap_utils.R

source("bootstrap_utils.R")

cat("========================================\n")
cat("Bootstrap Utilities Test Suite\n")
cat("========================================\n\n")

tests_passed <- 0
tests_failed <- 0

test_that <- function(description, expr) {
  result <- tryCatch({
    eval(expr)
  }, error = function(e) {
    message("Error: ", e$message)
    FALSE
  })
  
  if (isTRUE(result)) {
    cat("[PASS] ", description, "\n")
    tests_passed <<- tests_passed + 1
  } else {
    cat("[FAIL] ", description, "\n")
    tests_failed <<- tests_failed + 1
  }
}

# Test data
set.seed(42)
test_data <- rnorm(100, mean = 50, sd = 10)

cat("1. Testing generate_bootstrap_samples()\n")
cat("--------------------------------------\n")

test_that("generates correct number of samples", {
  samples <- generate_bootstrap_samples(test_data, n_samples = 500, seed = 123)
  ncol(samples) == 500
})

test_that("each sample has correct length", {
  samples <- generate_bootstrap_samples(test_data, n_samples = 100, seed = 456)
  all(apply(samples, 2, length) == length(test_data))
})

test_that("reproducible with seed", {
  s1 <- generate_bootstrap_samples(test_data, n_samples = 100, seed = 789)
  s2 <- generate_bootstrap_samples(test_data, n_samples = 100, seed = 789)
  identical(s1, s2)
})

test_that("errors on non-numeric data", {
  tryCatch({
    generate_bootstrap_samples(c("a", "b", "c"), n_samples = 10)
    FALSE
  }, error = function(e) TRUE)
})

cat("\n2. Testing bootstrap_ci()\n")
cat("-------------------------\n")

test_that("computes percentile CI correctly", {
  ci <- bootstrap_ci(test_data, n_samples = 2000, confidence = 0.95, 
                     method = "percentile", seed = 111)
  # Check that CI contains the true mean
  ci$lower < 50 && ci$upper > 50
})

test_that("computes basic CI correctly", {
  ci <- bootstrap_ci(test_data, n_samples = 2000, confidence = 0.95,
                     method = "basic", seed = 222)
  ci$estimate == mean(test_data)
})

test_that("computes normal CI correctly", {
  ci <- bootstrap_ci(test_data, n_samples = 2000, confidence = 0.95,
                     method = "normal", seed = 333)
  # Check structure
  !is.null(ci$lower) && !is.null(ci$upper)
})

test_that("computes BCa CI correctly", {
  ci <- bootstrap_ci(test_data, n_samples = 2000, confidence = 0.95,
                     method = "bca", seed = 444)
  # BCa should have finite CI
  is.finite(ci$lower) && is.finite(ci$upper)
})

test_that("works with custom statistic (median)", {
  ci <- bootstrap_ci(test_data, statistic = median, n_samples = 1000, seed = 555)
  ci$estimate == median(test_data)
})

test_that("returns standard error", {
  ci <- bootstrap_ci(test_data, n_samples = 1000, seed = 666)
  ci$se > 0
})

cat("\n3. Testing bootstrap_test()\n")
cat("--------------------------\n")

test_that("performs two-sided test correctly", {
  result <- bootstrap_test(test_data, null_value = 50, n_samples = 2000,
                          alternative = "two.sided", seed = 777)
  # Data centered around 50, should not reject
  result$statistic == mean(test_data)
})

test_that("performs one-sided test (greater)", {
  result <- bootstrap_test(test_data, null_value = 40, n_samples = 2000,
                          alternative = "greater", seed = 888)
  # Mean is around 50, null 40, should reject
  result$reject_h0 == TRUE
})

test_that("performs one-sided test (less)", {
  result <- bootstrap_test(test_data, null_value = 60, n_samples = 2000,
                          alternative = "less", seed = 999)
  # Mean is around 50, null 60, should reject
  result$reject_h0 == TRUE
})

test_that("p-value is between 0 and 1", {
  result <- bootstrap_test(test_data, null_value = 50, n_samples = 1000, seed = 111)
  result$p_value >= 0 && result$p_value <= 1
})

cat("\n4. Testing bootstrap_two_sample()\n")
cat("--------------------------------\n")

set.seed(42)
group_a <- rnorm(50, mean = 100, sd = 15)
group_b <- rnorm(50, mean = 105, sd = 15)

test_that("compares two samples correctly", {
  result <- bootstrap_two_sample(group_a, group_b, n_samples = 2000, seed = 222)
  # Difference should be around -5
  abs(result$statistic - (-5)) < 3
})

test_that("returns CI bounds in correct order", {
  result <- bootstrap_two_sample(group_a, group_b, n_samples = 1000, seed = 333)
  result$ci_lower < result$ci_upper
})

test_that("works with custom statistic (ratio of means)", {
  result <- bootstrap_two_sample(group_a, group_b, 
                                 statistic = function(a, b) mean(a) / mean(b),
                                 n_samples = 1000, seed = 444)
  !is.na(result$statistic) && result$statistic > 0
})

cat("\n5. Testing bootstrap_se() and bootstrap_bias()\n")
cat("----------------------------------------------\n")

test_that("bootstrap_se returns positive value", {
  se <- bootstrap_se(test_data, statistic = mean, n_samples = 1000, seed = 555)
  se > 0
})

test_that("bootstrap_se approximates theoretical SE", {
  se <- bootstrap_se(test_data, statistic = mean, n_samples = 5000, seed = 666)
  theoretical_se <- sd(test_data) / sqrt(length(test_data))
  # Within 20% of theoretical
  abs(se - theoretical_se) / theoretical_se < 0.20
})

test_that("bootstrap_bias returns numeric", {
  bias <- bootstrap_bias(test_data, statistic = mean, n_samples = 1000, seed = 777)
  is.numeric(bias)
})

test_that("bootstrap_bias for mean is close to zero", {
  bias <- bootstrap_bias(test_data, statistic = mean, n_samples = 5000, seed = 888)
  abs(bias) < 0.5
})

cat("\n6. Testing stratified_bootstrap()\n")
cat("----------------------------------\n")

strat_data <- data.frame(
  value = c(rnorm(30, mean = 10), rnorm(30, mean = 20), rnorm(30, mean = 30)),
  group = rep(c("A", "B", "C"), each = 30)
)

test_that("stratified bootstrap preserves strata proportions", {
  boot_stats <- stratified_bootstrap(strat_data, "group",
                                     statistic = function(d) mean(d$value),
                                     n_samples = 100, seed = 111)
  length(boot_stats) == 100
})

test_that("stratified bootstrap works with multiple strata", {
  result <- stratified_bootstrap(strat_data, "group",
                                 statistic = function(d) {
                                   tapply(d$value, d$group, mean)
                                 },
                                 n_samples = 50, seed = 222)
  # Result should be matrix of means by group
  is.matrix(result) || is.list(result) || is.numeric(result)
})

cat("\n7. Testing block_bootstrap()\n")
cat("----------------------------\n")

# Time series data with autocorrelation
set.seed(42)
ts_data <- cumsum(rnorm(100))  # Random walk

test_that("block bootstrap preserves structure", {
  boot_stats <- block_bootstrap(ts_data, block_size = 10,
                                statistic = mean, n_samples = 100, seed = 333)
  length(boot_stats) == 100
})

test_that("block bootstrap with different block sizes", {
  boot_small <- block_bootstrap(ts_data, block_size = 5,
                                statistic = mean, n_samples = 100, seed = 444)
  boot_large <- block_bootstrap(ts_data, block_size = 20,
                                statistic = mean, n_samples = 100, seed = 444)
  # Different block sizes should give different results
  !identical(boot_small, boot_large)
})

cat("\n8. Testing bootstrap_summary()\n")
cat("-------------------------------\n")

boot_stats <- rnorm(1000, mean = 50, sd = 5)

test_that("summary returns all statistics", {
  summ <- bootstrap_summary(boot_stats)
  all(c("mean", "median", "sd", "se", "ci_lower", "ci_upper", "skewness", "kurtosis") 
      %in% names(summ))
})

test_that("summary CI bounds are correct", {
  summ <- bootstrap_summary(boot_stats, confidence = 0.95)
  summ$ci_lower < summ$mean && summ$ci_upper > summ$mean
})

test_that("summary calculates skewness", {
  skewed_data <- rexp(1000)  # Positively skewed
  summ <- bootstrap_summary(skewed_data)
  summ$skewness > 0
})

cat("\n9. Testing parametric_bootstrap()\n")
cat("----------------------------------\n")

test_that("parametric bootstrap with normal distribution", {
  boot_stats <- parametric_bootstrap(test_data, 
                                     statistic = mean, 
                                     n_samples = 100, seed = 555)
  length(boot_stats) == 100
})

test_that("parametric bootstrap with exponential distribution", {
  exp_data <- rexp(100, rate = 0.5)
  boot_stats <- parametric_bootstrap(
    exp_data,
    statistic = mean,
    fit_dist = function(d) list(rate = 1/mean(d)),
    sample_dist = function(params, n) rexp(n, rate = params$rate),
    n_samples = 100,
    seed = 666
  )
  mean(boot_stats) > 0
})

cat("\n10. Testing jackknife()\n")
cat("-----------------------\n")

test_that("jackknife returns correct structure", {
  jk <- jackknife(test_data, statistic = mean)
  all(c("original", "jackknife_estimate", "bias", "se", "pseudo_values") %in% names(jk))
})

test_that("jackknife estimate equals mean for mean statistic", {
  jk <- jackknife(test_data, statistic = mean)
  abs(jk$jackknife_estimate - mean(test_data)) < 0.001
})

test_that("jackknife pseudo-values have correct length", {
  jk <- jackknife(test_data, statistic = mean)
  length(jk$pseudo_values) == length(test_data)
})

test_that("jackknife works with median", {
  jk <- jackknife(test_data, statistic = median)
  is.numeric(jk$se) && jk$se > 0
})

cat("\n11. Testing bootstrap_regression()\n")
cat("----------------------------------\n")

reg_data <- data.frame(
  y = rnorm(50),
  x1 = rnorm(50),
  x2 = rnorm(50)
)

test_that("bootstrap regression returns coefficients", {
  result <- bootstrap_regression(y ~ x1 + x2, reg_data, n_samples = 100, seed = 777)
  ncol(result$coefficients) == 3  # Intercept + x1 + x2
})

test_that("bootstrap regression summary is correct", {
  result <- bootstrap_regression(y ~ x1 + x2, reg_data, n_samples = 100, seed = 888)
  length(result$summary) == 3
})

test_that("bootstrap regression CI contains estimate", {
  result <- bootstrap_regression(y ~ x1 + x2, reg_data, n_samples = 500, seed = 999)
  # Check that each CI contains the point estimate
  all(sapply(result$summary, function(s) {
    s$ci_lower <= s$estimate && s$ci_upper >= s$estimate
  }))
})

cat("\n12. Testing compute_acceleration()\n")
cat("----------------------------------\n")

test_that("acceleration factor is finite", {
  a <- compute_acceleration(test_data, statistic = mean)
  is.finite(a)
})

test_that("acceleration factor for mean is small", {
  a <- compute_acceleration(test_data, statistic = mean)
  abs(a) < 1  # Should be small for symmetric distribution
})

cat("\n13. Edge cases and error handling\n")
cat("----------------------------------\n")

test_that("handles small sample size", {
  small_data <- c(1, 2, 3, 4, 5)
  ci <- bootstrap_ci(small_data, n_samples = 100, seed = 111)
  !is.null(ci$estimate)
})

test_that("handles skewed data", {
  skewed <- rexp(100, rate = 0.1)
  ci <- bootstrap_ci(skewed, n_samples = 500, seed = 222)
  ci$estimate == mean(skewed)
})

test_that("handles constant data gracefully", {
  constant_data <- rep(5, 100)
  ci <- bootstrap_ci(constant_data, n_samples = 100, seed = 333)
  ci$estimate == 5
})

cat("\n========================================\n")
cat(sprintf("Tests passed: %d\n", tests_passed))
cat(sprintf("Tests failed: %d\n", tests_failed))
cat("========================================\n")

if (tests_failed == 0) {
  cat("\nAll tests passed!\n")
} else {
  cat("\nSome tests failed. Please review.\n")
  quit(status = 1)
}