#!/usr/bin/env Rscript
# correlation_utils_example.R - Example Usage for Correlation Utilities
#
# Demonstrates various functions in the correlation_utils module
#
# Author: AllToolkit
# Version: 1.0.0

# Source the module
source("../correlation_utils/mod.R")

cat("\n========================================\n")
cat("correlation_utils - Usage Examples\n")
cat("========================================\n\n")

# ============================================================================
# Example 1: Basic Correlation Coefficients
# ============================================================================

cat("=== Example 1: Basic Correlation Coefficients ===\n\n")

# Height and weight data (fictional)
height <- c(150, 160, 170, 180, 190)
weight <- c(50, 60, 70, 80, 90)

cat("Height:", height, "\n")
cat("Weight:", weight, "\n\n")

# Pearson correlation (measures linear relationship)
pearson_r <- pearson_cor(height, weight)
cat("Pearson correlation:", round(pearson_r, 4), "\n")
cat("Interpretation:", interpret_cor(pearson_r), "\n\n")

# Spearman correlation (monotonic relationship, less sensitive to outliers)
spearman_r <- spearman_cor(height, weight)
cat("Spearman correlation:", round(spearman_r, 4), "\n\n")

# Kendall's tau (robust non-parametric correlation)
kendall_r <- kendall_tau(height, weight)
cat("Kendall's tau:", round(kendall_r, 4), "\n\n")

# ============================================================================
# Example 2: Correlation with NA Values
# ============================================================================

cat("=== Example 2: Handling NA Values ===\n\n")

# Data with missing values
x_missing <- c(1, 2, NA, 4, 5, 6, NA, 8)
y_missing <- c(2, 4, 6, NA, 10, 12, 14, 16)

cat("X (with NA):", x_missing, "\n")
cat("Y (with NA):", y_missing, "\n\n")

r_with_na <- pearson_cor(x_missing, y_missing, na.rm = TRUE)
cat("Pearson correlation (na.rm=TRUE):", round(r_with_na, 4), "\n\n")

# ============================================================================
# Example 3: Correlation Matrix
# ============================================================================

cat("=== Example 3: Correlation Matrix ===\n\n")

# Multiple variables for correlation analysis
data_frame <- data.frame(
  math_score = c(85, 90, 78, 92, 88, 75, 95, 82),
  science_score = c(88, 92, 80, 90, 85, 72, 94, 80),
  reading_score = c(70, 75, 65, 80, 72, 60, 85, 68),
  study_hours = c(20, 25, 15, 28, 22, 10, 30, 18)
)

cat("Data frame:\n")
print(data_frame)

# Compute correlation matrix
cat("\nPearson Correlation Matrix:\n")
cor_mat <- cor_matrix(data_frame, method = "pearson")
print(round(cor_mat, 3))

# Format with significance stars
cat("\nFormatted with significance stars (* p<0.05, ** p<0.01, *** p<0.001):\n")
formatted <- format_cor_matrix(cor_mat, nrow(data_frame))
print(formatted)

# ============================================================================
# Example 4: Significance Testing
# ============================================================================

cat("\n=== Example 4: Significance Testing ===\n\n")

# Perform correlation test
test_result <- cor_test(
  data_frame$math_score,
  data_frame$science_score,
  method = "pearson",
  alpha = 0.05
)

cat("Correlation test (Math vs Science):\n")
cat("  Correlation:", round(test_result$correlation, 4), "\n")
cat("  P-value:", round(test_result$p_value, 6), "\n")
cat("  Significant at α=0.05?", test_result$significant, "\n")

# Confidence interval
ci_result <- cor_ci(test_result$correlation, test_result$n, conf_level = 0.95)
cat("\n95% Confidence Interval:\n")
cat("  Lower bound:", round(ci_result$lower, 4), "\n")
cat("  Upper bound:", round(ci_result$upper, 4), "\n")

# ============================================================================
# Example 5: Partial Correlation
# ============================================================================

cat("\n=== Example 5: Partial Correlation ===\n\n")

# Exam scores influenced by study hours
exam_score <- c(70, 75, 80, 85, 90, 95, 100, 78)
iq_score <- c(100, 105, 110, 115, 120, 125, 130, 112)
study_hours <- c(5, 10, 15, 20, 25, 30, 35, 12)

cat("Exam scores:", exam_score, "\n")
cat("IQ scores:", iq_score, "\n")
cat("Study hours:", study_hours, "\n\n")

# Simple correlation (may be confounded by study hours)
simple_r <- pearson_cor(exam_score, iq_score)
cat("Simple correlation (Exam vs IQ):", round(simple_r, 4), "\n")

# Partial correlation controlling for study hours
partial_r <- partial_cor(exam_score, iq_score, study_hours)
cat("Partial correlation (controlling for study hours):", round(partial_r, 4), "\n")
cat("Interpretation:", interpret_cor(partial_r), "\n\n")

# ============================================================================
# Example 6: Distance Correlation (Detecting Non-linear Relationships)
# ============================================================================

cat("=== Example 6: Distance Correlation ===\n\n")

# Linear relationship
linear_x <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
linear_y <- c(2, 4, 6, 8, 10, 12, 14, 16, 18, 20)

# Non-linear relationship (parabolic)
parabolic_x <- c(-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5)
parabolic_y <- parabolic_x^2

cat("Linear relationship - Pearson:", round(pearson_cor(linear_x, linear_y), 4), "\n")
cat("Linear relationship - Distance:", round(distance_cor(linear_x, linear_y), 4), "\n\n")

cat("Parabolic relationship - Pearson:", round(pearson_cor(parabolic_x, parabolic_y), 4), "\n")
cat("Parabolic relationship - Distance:", round(distance_cor(parabolic_x, parabolic_y), 4), "\n")
cat("(Distance correlation can detect non-linear relationships!)\n\n")

# ============================================================================
# Example 7: Effect Sizes
# ============================================================================

cat("=== Example 7: Effect Sizes ===\n\n")

# R-squared (variance explained)
r2 <- r_squared(height, weight)
cat("R-squared (variance explained):", round(r2, 4), "\n")
cat("Interpretation:", round(r2 * 100, 2), "% of weight variance is explained by height\n\n")

# Cohen's d (group difference effect size)
group_a_scores <- c(75, 78, 82, 85, 88, 90, 92)
group_b_scores <- c(60, 65, 70, 72, 75, 78, 80)

d <- cohens_d(group_a_scores, group_b_scores)
cat("Cohen's d (Group A vs Group B):", round(d, 4), "\n")
cat("Interpretation: ", if(abs(d) < 0.2) "small" else if(abs(d) < 0.8) "medium" else "large", " effect\n\n")

# ============================================================================
# Example 8: Finding Significant Correlations
# ============================================================================

cat("=== Example 8: Finding Significant Correlations ===\n\n")

# Generate correlation matrix
cor_mat <- cor_matrix(data_frame)

# Find all significant correlations
sig_cors <- significant_cors(cor_mat, nrow(data_frame), alpha = 0.05)

if (nrow(sig_cors) > 0) {
  cat("Significant correlations found:\n")
  for (i in 1:nrow(sig_cors)) {
    cat(sprintf("  %s vs %s: r=%.3f, p=%.4f\n",
                sig_cors$var1[i],
                sig_cors$var2[i],
                sig_cors$r[i],
                sig_cors$p_value[i]))
  }
} else {
  cat("No significant correlations found at α=0.05\n")
}

# ============================================================================
# Example 9: Covariance Matrix
# ============================================================================

cat("\n=== Example 9: Covariance Matrix ===\n\n")

cov_mat <- cov_matrix(data_frame)
cat("Covariance Matrix:\n")
print(round(cov_mat, 2))

# ============================================================================
# Summary
# ============================================================================

cat("\n========================================\n")
cat("Module Info\n")
cat("========================================\n\n")

correlation_info()

cat("\n--- Examples completed! ---\n")