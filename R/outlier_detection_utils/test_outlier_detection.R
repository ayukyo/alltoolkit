# Tests for Outlier Detection Utils
# Run with: Rscript test_outlier_detection.R

source("outlier_detection.R")

# Test counter
tests_passed <- 0
tests_failed <- 0

test_that <- function(description, expr) {
  cat("Testing:", description, "... ")
  result <- tryCatch({
    if (eval(expr)) {
      cat("PASSED\n")
      tests_passed <<- tests_passed + 1
      TRUE
    } else {
      cat("FAILED\n")
      tests_failed <<- tests_failed + 1
      FALSE
    }
  }, error = function(e) {
    cat("ERROR:", e$message, "\n")
    tests_failed <<- tests_failed + 1
    FALSE
  })
  invisible(result)
}

cat("========================================\n")
cat("Outlier Detection Utils Test Suite\n")
cat("========================================\n\n")

# ============================================================================
# IQR Method Tests
# ============================================================================

cat("--- IQR Method Tests ---\n")

test_that("IQR detects simple outliers", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result <- detect_outliers_iqr(data)
  length(result$outliers) == 1 && result$outliers[1] == 100
})

test_that("IQR returns correct bounds", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
  result <- detect_outliers_iqr(data)
  result$lower_bound < 1 && result$upper_bound > 10
})

test_that("IQR handles no outliers case", {
  data <- 1:10
  result <- detect_outliers_iqr(data)
  length(result$outliers) == 0
})

test_that("IQR works with custom multiplier", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 50)
  result_normal <- detect_outliers_iqr(data, 1.5)
  result_extreme <- detect_outliers_iqr(data, 3)
  result_normal$total_detected >= result_extreme$total_detected
})

# ============================================================================
# Z-Score Method Tests
# ============================================================================

cat("\n--- Z-Score Method Tests ---\n")

test_that("Z-Score detects outliers", {
  data <- c(rnorm(20, mean = 0, sd = 1), 10)  # Add extreme value
  result <- detect_outliers_zscore(data, threshold = 3)
  any(result$indices == 21)
})

test_that("Z-Score calculates correct z-scores", {
  data <- c(0, 1, 2, 3, 4)
  result <- detect_outliers_zscore(data, threshold = 10)
  mean(result$z_scores) < 0.001  # Z-scores should have mean ~0
})

test_that("Z-Score handles zero SD", {
  data <- c(5, 5, 5, 5, 5)
  result <- detect_outliers_zscore(data)
  length(result$outliers) == 0
})

test_that("Z-Score threshold affects detection", {
  data <- c(1, 2, 3, 4, 5, 100)
  result_loose <- detect_outliers_zscore(data, threshold = 2)
  result_strict <- detect_outliers_zscore(data, threshold = 5)
  result_loose$total_detected >= result_strict$total_detected
})

# ============================================================================
# Modified Z-Score (MAD) Tests
# ============================================================================

cat("\n--- Modified Z-Score (MAD) Tests ---\n")

test_that("MAD detects outliers", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result <- detect_outliers_mad(data, threshold = 3.5)
  length(result$outliers) > 0
})

test_that("MAD is robust to extreme values", {
  data_with_outlier <- c(1, 2, 3, 4, 5, 100)
  data_clean <- c(1, 2, 3, 4, 5)
  
  result_with <- detect_outliers_mad(data_with_outlier)
  result_clean <- detect_outliers_mad(data_clean)
  
  # MAD should be less affected by the outlier than SD
  abs(result_with$median - result_clean$median) < 2
})

test_that("MAD handles identical values", {
  data <- c(1, 1, 1, 1, 1)
  result <- detect_outliers_mad(data)
  length(result$outliers) == 0
})

# ============================================================================
# Percentile Method Tests
# ============================================================================

cat("\n--- Percentile Method Tests ---\n")

test_that("Percentile method detects outliers", {
  data <- c(1:100, 200)
  result <- detect_outliers_percentile(data, 1, 99)
  length(result$outliers) > 0
})

test_that("Percentile bounds are correct", {
  data <- 1:100
  result <- detect_outliers_percentile(data, 5, 95)
  result$lower_bound == 5 && result$upper_bound == 95
})

test_that("Percentile with wide range has no outliers", {
  data <- 1:100
  result <- detect_outliers_percentile(data, 0, 100)
  length(result$outliers) == 0
})

# ============================================================================
# Tukey's Fences Tests
# ============================================================================

cat("\n--- Tukey's Fences Tests ---\n")

test_that("Tukey inner fences use 1.5 IQR", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result_inner <- detect_outliers_tukey(data, "inner")
  result_outer <- detect_outliers_tukey(data, "outer")
  result_inner$total_detected >= result_outer$total_detected
})

test_that("Tukey outer fences use 3 IQR", {
  data <- c(1:10, 50, 100)
  result <- detect_outliers_tukey(data, "outer")
  result$fences_type == "outer"
})

# ============================================================================
# Grubbs' Test Tests
# ============================================================================

cat("\n--- Grubbs' Test Tests ---\n")

test_that("Grubbs detects single outlier", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result <- detect_outlier_grubbs(data)
  result$is_outlier
})

test_that("Grubbs identifies correct outlier", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result <- detect_outlier_grubbs(data)
  result$outlier_value == 100
})

test_that("Grubbs handles no outlier case", {
  set.seed(42)
  data <- rnorm(30, mean = 10, sd = 1)
  result <- detect_outlier_grubbs(data, alpha = 0.01)
  !result$is_outlier
})

# ============================================================================
# Dixon's Q Test Tests
# ============================================================================

cat("\n--- Dixon's Q Test Tests ---\n")

test_that("Dixon Q detects outlier in small sample", {
  data <- c(1.2, 1.3, 1.4, 1.3, 1.2, 1.3, 5.0)
  result <- detect_outlier_dixon(data)
  result$is_outlier
})

test_that("Dixon Q handles no outlier case", {
  data <- c(10.1, 10.2, 10.0, 10.3, 10.1, 9.9, 10.2)
  result <- detect_outlier_dixon(data)
  !result$is_outlier
})

test_that("Dixon Q requires sample size 3-30", {
  data <- 1:31
  tryCatch({
    detect_outlier_dixon(data)
    FALSE  # Should have thrown error
  }, error = function(e) {
    TRUE  # Expected error
  })
})

# ============================================================================
# Comprehensive Detection Tests
# ============================================================================

cat("\n--- Comprehensive Detection Tests ---\n")

test_that("detect_outliers_all returns all methods", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result <- detect_outliers_all(data)
  !is.null(result$iqr) && !is.null(result$zscore) && !is.null(result$mad)
})

test_that("detect_outliers_all provides consensus", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result <- detect_outliers_all(data)
  !is.null(result$consensus)
})

test_that("detect_outliers_all includes summary", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result <- detect_outliers_all(data)
  nrow(result$summary) == 7  # 7 methods in summary
})

# ============================================================================
# Remove/Replace Outliers Tests
# ============================================================================

cat("\n--- Remove/Replace Outliers Tests ---\n")

test_that("remove_outliers removes IQR outliers", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result <- remove_outliers(data, "iqr")
  sum(is.na(result$cleaned)) == 1
})

test_that("remove_outliers preserves non-outliers", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result <- remove_outliers(data, "iqr")
  length(result$cleaned) == length(data)
})

test_that("replace_outliers with median works", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result <- replace_outliers(data, "iqr", "median")
  all(!is.na(result$replaced))
})

test_that("replace_outliers with trim (winsorize) works", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result <- replace_outliers(data, "percentile", "trim", lower_percentile = 5, upper_percentile = 95)
  max(result$replaced) < 100
})

test_that("replace_outliers with custom value works", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result <- replace_outliers(data, "iqr", -999)
  any(result$replaced == -999)
})

# ============================================================================
# Box Plot Stats Tests
# ============================================================================

cat("\n--- Box Plot Stats Tests ---\n")

test_that("boxplot_outlier_stats returns correct structure", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result <- boxplot_outlier_stats(data)
  !is.null(result$q1) && !is.null(result$median) && !is.null(result$q3)
})

test_that("boxplot_outlier_stats identifies outliers", {
  data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
  result <- boxplot_outlier_stats(data)
  100 %in% result$outliers
})

# ============================================================================
# Edge Cases Tests
# ============================================================================

cat("\n--- Edge Cases Tests ---\n")

test_that("Handles NA values", {
  data <- c(1, 2, NA, 4, 5, NA, 7, 8, 9, 100)
  result <- detect_outliers_iqr(data)
  length(result$outliers) == 1 && result$outliers[1] == 100
})

test_that("Handles single value", {
  data <- 5
  result <- detect_outliers_iqr(data)
  length(result$outliers) == 0
})

test_that("Handles two values", {
  data <- c(1, 100)
  result <- detect_outliers_iqr(data)
  length(result$outliers) == 0
})

test_that("Handles negative values", {
  data <- c(-100, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5)
  result <- detect_outliers_iqr(data)
  -100 %in% result$outliers
})

test_that("Handles very large numbers", {
  data <- c(1e6, 1e6 + 1, 1e6 + 2, 1e6 + 3, 1e6 + 4, 1e12)
  result <- detect_outliers_iqr(data)
  1e12 %in% result$outliers
})

# ============================================================================
# Print Results
# ============================================================================

cat("\n========================================\n")
cat("Test Results Summary\n")
cat("========================================\n")
cat(sprintf("Tests Passed: %d\n", tests_passed))
cat(sprintf("Tests Failed: %d\n", tests_failed))
cat(sprintf("Total Tests:  %d\n", tests_passed + tests_failed))
cat(sprintf("Pass Rate:    %.1f%%\n", 
            100 * tests_passed / (tests_passed + tests_failed)))
cat("========================================\n")

if (tests_failed > 0) {
  quit(status = 1)
}