#!/usr/bin/env Rscript
# correlation_utils/correlation_utils_test.R - Test Suite for Correlation Utilities
#
# Tests all functions in the correlation_utils module
#
# Author: AllToolkit
# Version: 1.0.0

# Source the module
source("mod.R")

# Test counter
tests_passed <- 0
tests_failed <- 0

# Helper function for testing
test_that <- function(description, expr) {
  result <- tryCatch({
    eval(expr)
  }, error = function(e) {
    FALSE
  })
  
  if (isTRUE(result)) {
    cat("✓ PASS:", description, "\n")
    tests_passed <<- tests_passed + 1
  } else {
    cat("✗ FAIL:", description, "\n")
    tests_failed <<- tests_failed + 1
  }
}

# Tolerance for floating point comparisons
approx_equal <- function(a, b, tol = 1e-6) {
  abs(a - b) < tol
}

cat("\n========================================\n")
cat("Testing correlation_utils Module\n")
cat("========================================\n\n")

# ============================================================================
# Test Data
# ============================================================================

# Perfect positive correlation
x1 <- c(1, 2, 3, 4, 5)
y1 <- c(2, 4, 6, 8, 10)

# Perfect negative correlation
x2 <- c(1, 2, 3, 4, 5)
y2 <- c(10, 8, 6, 4, 2)

# No correlation (random-ish)
x3 <- c(1, 2, 3, 4, 5)
y3 <- c(2, 5, 1, 4, 3)

# Data with NA values
x_na <- c(1, 2, NA, 4, 5)
y_na <- c(2, NA, 6, 8, 10)

# Data for partial correlation
x_partial <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
y_partial <- c(2, 4, 5, 4, 5, 8, 9, 10, 12, 11)
z_partial <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

# ============================================================================
# Test Pearson Correlation
# ============================================================================

cat("--- Pearson Correlation Tests ---\n")

test_that("Pearson correlation for perfect positive correlation equals 1", {
  r <- pearson_cor(x1, y1)
  approx_equal(r, 1)
})

test_that("Pearson correlation for perfect negative correlation equals -1", {
  r <- pearson_cor(x2, y2)
  approx_equal(r, -1)
})

test_that("Pearson correlation handles NA values correctly", {
  r <- pearson_cor(x_na, y_na, na.rm = TRUE)
  approx_equal(r, 1, tol = 0.01)
})

test_that("Pearson correlation returns NA for insufficient data", {
  r <- pearson_cor(c(1), c(1))
  is.na(r)
})

test_that("Pearson correlation handles zero variance", {
  r <- pearson_cor(c(1, 1, 1, 1), c(1, 2, 3, 4))
  is.na(r)
})

# ============================================================================
# Test Spearman Correlation
# ============================================================================

cat("\n--- Spearman Correlation Tests ---\n")

test_that("Spearman correlation for monotonic data equals 1", {
  r <- spearman_cor(x1, y1)
  approx_equal(r, 1)
})

test_that("Spearman correlation handles ties correctly", {
  x_ties <- c(1, 2, 2, 4, 5)
  y_ties <- c(2, 4, 4, 8, 10)
  r <- spearman_cor(x_ties, y_ties)
  !is.na(r) && r > 0.9
})

# ============================================================================
# Test Kendall's Tau
# ============================================================================

cat("\n--- Kendall's Tau Tests ---\n")

test_that("Kendall tau for perfect positive correlation equals 1", {
  r <- kendall_tau(x1, y1)
  approx_equal(r, 1)
})

test_that("Kendall tau for perfect negative correlation equals -1", {
  r <- kendall_tau(x2, y2)
  approx_equal(r, -1)
})

test_that("Kendall tau-b handles ties correctly", {
  x_ties <- c(1, 2, 2, 3, 4)
  y_ties <- c(1, 2, 2, 3, 4)
  r <- kendall_tau_b(x_ties, y_ties)
  !is.na(r) && r > 0.9
})

# ============================================================================
# Test Correlation Matrix
# ============================================================================

cat("\n--- Correlation Matrix Tests ---\n")

test_data <- data.frame(
  a = c(1, 2, 3, 4, 5),
  b = c(2, 4, 6, 8, 10),
  c = c(5, 4, 3, 2, 1)
)

test_that("Correlation matrix has correct dimensions", {
  mat <- cor_matrix(test_data)
  nrow(mat) == 3 && ncol(mat) == 3
})

test_that("Correlation matrix diagonal is all 1s", {
  mat <- cor_matrix(test_data)
  all(diag(mat) == 1)
})

test_that("Correlation matrix is symmetric", {
  mat <- cor_matrix(test_data)
  all(mat == t(mat), na.rm = TRUE)
})

test_that("Correlation matrix detects perfect correlation", {
  mat <- cor_matrix(test_data)
  approx_equal(mat[1, 2], 1) && approx_equal(mat[1, 3], -1)
})

# ============================================================================
# Test Covariance
# ============================================================================

cat("\n--- Covariance Tests ---\n")

test_that("Covariance calculation is correct", {
  x <- c(1, 2, 3, 4, 5)
  y <- c(2, 4, 6, 8, 10)
  cov_val <- covariance(x, y)
  cov_val > 0
})

test_that("Covariance matrix has correct dimensions", {
  mat <- cov_matrix(test_data)
  nrow(mat) == 3 && ncol(mat) == 3
})

# ============================================================================
# Test Significance Testing
# ============================================================================

cat("\n--- Significance Testing Tests ---\n")

test_that("P-value for perfect correlation is very small", {
  p <- cor_p_value(1, 10)
  p < 0.001
})

test_that("P-value for zero correlation is large", {
  p <- cor_p_value(0, 10)
  p > 0.05
})

test_that("cor_test returns correct structure", {
  result <- cor_test(x1, y1)
  all(c("correlation", "p_value", "n", "method", "significant") %in% names(result))
})

test_that("cor_test detects significance correctly", {
  result <- cor_test(x1, y1)
  result$significant == TRUE
})

# ============================================================================
# Test Partial Correlation
# ============================================================================

cat("\n--- Partial Correlation Tests ---\n")

test_that("Partial correlation returns numeric value", {
  r <- partial_cor(x_partial, y_partial, z_partial)
  is.numeric(r) && !is.na(r)
})

test_that("Partial correlation with single control variable works", {
  r <- partial_cor(c(1, 2, 3, 4, 5), c(2, 3, 4, 5, 6), c(0.5, 1, 1.5, 2, 2.5))
  is.numeric(r)
})

test_that("Semi-partial correlation returns numeric value", {
  r <- semi_partial_cor(c(1, 2, 3, 4, 5), c(2, 3, 4, 5, 6), c(1, 2, 3, 4, 5))
  is.numeric(r) && !is.na(r)
})

# ============================================================================
# Test Distance Correlation
# ============================================================================

cat("\n--- Distance Correlation Tests ---\n")

test_that("Distance correlation for linear relationship is high", {
  r <- distance_cor(x1, y1)
  r > 0.9
})

test_that("Distance correlation handles NA values", {
  r <- distance_cor(x_na, y_na, na.rm = TRUE)
  is.numeric(r) && !is.na(r)
})

test_that("Correlation distance is non-negative", {
  d <- cor_distance(x1, y1)
  d >= 0
})

# ============================================================================
# Test Effect Sizes
# ============================================================================

cat("\n--- Effect Size Tests ---\n")

test_that("R-squared for perfect correlation equals 1", {
  r2 <- r_squared(x1, y1)
  approx_equal(r2, 1)
})

test_that("Adjusted R-squared is calculated correctly", {
  r2 <- 0.5
  adj_r2 <- adjusted_r_squared(r2, 100, 2)
  is.numeric(adj_r2) && adj_r2 < r2
})

test_that("Cohen's d for equal groups equals 0", {
  x <- c(1, 2, 3, 4, 5)
  y <- c(1, 2, 3, 4, 5)
  d <- cohens_d(x, y)
  approx_equal(d, 0)
})

test_that("Cohen's d for different groups is non-zero", {
  x <- c(1, 2, 3, 4, 5)
  y <- c(10, 11, 12, 13, 14)
  d <- cohens_d(x, y)
  d != 0
})

# ============================================================================
# Test Confidence Intervals
# ============================================================================

cat("\n--- Confidence Interval Tests ---\n")

test_that("Confidence interval contains the true correlation", {
  ci <- cor_ci(0.5, 100)
  ci$lower < 0.5 && ci$upper > 0.5
})

test_that("Confidence interval width is reasonable", {
  ci <- cor_ci(0.5, 100)
  ci$upper - ci$lower > 0 && ci$upper - ci$lower < 0.5
})

test_that("Confidence interval handles edge cases", {
  ci <- cor_ci(0.99, 10)
  ci$lower > 0 && ci$upper <= 1
})

# ============================================================================
# Test Utility Functions
# ============================================================================

cat("\n--- Utility Function Tests ---\n")

test_that("interpret_cor returns meaningful descriptions", {
  desc <- interpret_cor(0.8)
  grepl("strong", desc, ignore.case = TRUE) || grepl("very strong", desc, ignore.case = TRUE)
})

test_that("interpret_cor handles negative correlations", {
  desc <- interpret_cor(-0.6)
  grepl("negative", desc, ignore.case = TRUE)
})

test_that("is_significant detects significance correctly", {
  is_sig <- is_significant(0.9, 10)
  is_sig == TRUE
})

test_that("format_cor_matrix produces formatted output", {
  mat <- cor_matrix(test_data)
  formatted <- format_cor_matrix(mat, 5)
  is.matrix(formatted) && is.character(formatted[1, 1])
})

# ============================================================================
# Test Error Handling
# ============================================================================

cat("\n--- Error Handling Tests ---\n")

test_that("pearson_cor errors on non-numeric input", {
  tryCatch({
    pearson_cor(c("a", "b"), c(1, 2))
    FALSE
  }, error = function(e) TRUE)
})

test_that("pearson_cor errors on unequal length vectors", {
  tryCatch({
    pearson_cor(c(1, 2, 3), c(1, 2))
    FALSE
  }, error = function(e) TRUE)
})

test_that("cor_matrix errors on single column", {
  tryCatch({
    cor_matrix(data.frame(a = c(1, 2, 3)))
    FALSE
  }, error = function(e) TRUE)
})

# ============================================================================
# Test Summary
# ============================================================================

cat("\n========================================\n")
cat("Test Summary\n")
cat("========================================\n")
cat("Passed:", tests_passed, "\n")
cat("Failed:", tests_failed, "\n")

if (tests_failed == 0) {
  cat("\n✓ All tests passed!\n")
  quit(status = 0)
} else {
  cat("\n✗ Some tests failed.\n")
  quit(status = 1)
}