#!/usr/bin/env Rscript
# stats_utils_test.R - Unit Tests for Stats Utils Module
#
# Run with: Rscript stats_utils_test.R

source("mod.R")

total_tests <- 0
passed_tests <- 0
failed_tests <- 0

test <- function(name, condition) {
  total_tests <<- total_tests + 1
  if (condition) {
    passed_tests <<- passed_tests + 1
    cat("[PASS] ", name, "\n", sep = "")
  } else {
    failed_tests <<- failed_tests + 1
    cat("[FAIL] ", name, "\n", sep = "")
  }
}

test_equal <- function(name, actual, expected, tolerance = 1e-6) {
  test(name, abs(actual - expected) < tolerance)
}

cat("Running Stats Utils Tests...\n")
cat("==============================\n\n")

# Descriptive Statistics
cat("--- Descriptive Statistics ---\n")
test_equal("mean_value basic", mean_value(c(1, 2, 3, 4, 5)), 3)
test_equal("mean_value with NA", mean_value(c(1, 2, NA, 4, 5)), 3)
test("mean_value empty returns NA", is.na(mean_value(numeric(0))))

test_equal("median_value odd", median_value(c(1, 2, 3, 4, 5)), 3)
test_equal("median_value even", median_value(c(1, 2, 3, 4)), 2.5)

test("mode_value basic", all(mode_value(c(1, 2, 2, 3, 3, 3)) == 3))
test("mode_value multiple", length(mode_value(c(1, 1, 2, 2))) == 2)

test_equal("variance sample", variance(c(1, 2, 3, 4, 5)), 2.5)
test_equal("variance population", variance(c(1, 2, 3, 4, 5), sample = FALSE), 2)
test("variance single NA", is.na(variance(1)))

test_equal("std_dev basic", std_dev(c(1, 2, 3, 4, 5)), sqrt(2.5))
test_equal("range_value basic", range_value(c(1, 2, 3, 4, 5)), 4)
test_equal("iqr basic", iqr(c(1:10)), 5)
test_equal("quantile_value median", quantile_value(c(1, 2, 3, 4, 5), 0.5), 3)

test("summary_stats list", is.list(summary_stats(c(1, 2, 3, 4, 5))))

# Distribution Functions
cat("\n--- Distribution Functions ---\n")
test_equal("z_score basic", z_score(75, 70, 10), 0.5)
test("z_score Inf", all(is.infinite(z_score(c(1, 1, 1)))))
test_equal("dnorm_approx mean", dnorm_approx(0), 1/sqrt(2*pi))
test_equal("pnorm_approx mean", pnorm_approx(0), 0.5)
test("random_normal len", length(random_normal(100)) == 100)
test("random_uniform len", length(random_uniform(50)) == 50)
test("random_exp len", length(random_exponential(50, 1)) == 50)

# Correlation & Regression
cat("\n--- Correlation and Regression ---\n")
test_equal("correlation perfect", correlation(1:5, c(2, 4, 6, 8, 10)), 1)
test_equal("correlation negative", correlation(1:5, c(10, 8, 6, 4, 2)), -1)
test("correlation NA", is.na(correlation(c(1, 1, 1), 1:3)))

lm_r <- linear_regression(1:5, c(2, 4, 6, 8, 10))
test_equal("lm slope", lm_r$slope, 2)
test_equal("lm intercept", lm_r$intercept, 0)
test_equal("lm r2", lm_r$r_squared, 1)
test_equal("lm predict", lm_r$predict(6), 12)

# Outlier Detection
cat("\n--- Outlier Detection ---\n")
data <- c(1:9, 100)
test("detect_iqr outlier", detect_outliers_iqr(data)[10])
test("detect_iqr clean", !any(detect_outliers_iqr(1:10)))
test("detect_zscore outlier", detect_outliers_zscore(data, 2)[10])
test("remove_outliers", length(remove_outliers(data, "iqr")) == 9)

# Data Transformation
cat("\n--- Data Transformation ---\n")
test_equal("min_max_scale", min_max_scale(c(0, 5, 10))[2], 0.5)
test_equal("standardize mean", mean_value(standardize(1:5)), 0)
test_equal("log_transform", log_transform(c(1, exp(1))), c(0, 1))
test("log_transform err", tryCatch(log_transform(-1), error = function(e) TRUE))

# Utility Functions
cat("\n--- Utility Functions ---\n")
test("percentile_rank", percentile_rank(1:100, 50) == 50)
test("cv basic", coefficient_of_variation(c(1, 2, 3, 4, 5)) > 0)
test("skewness basic", !is.na(skewness(c(1, 2, 3, 4, 5))))
test("kurtosis basic", !is.na(kurtosis(c(1, 2, 3, 4, 5))))
test("moving_average", length(moving_average(1:10, 3)) == 10)
test("ci basic", is.list(confidence_interval(1:10)))
test("qq_normal", is.list(qq_normal(1:10)))

# Statistical Tests
cat("\n--- Statistical Tests ---\n")
t_test <- t_test_one_sample(c(1, 2, 3, 4, 5), 3)
test("t_test list", is.list(t_test))
test("t_test stat", !is.na(t_test$statistic))

chi_test <- chi_square_test(c(10, 20, 30))
test("chi_test list", is.list(chi_test))

# Summary
cat("\n==============================\n")
cat("Total:  ", total_tests, "\n")
cat("Passed: ", passed_tests, "\n")
cat("Failed: ", failed_tests, "\n")

if (failed_tests == 0) {
  cat("\nAll tests passed!\n")
  quit(status = 0)
} else {
  cat("\nSome tests failed!\n")
  quit(status = 1)
}
