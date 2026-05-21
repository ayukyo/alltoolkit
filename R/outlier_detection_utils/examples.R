# Outlier Detection Utils - Usage Examples
# Run with: Rscript examples.R

source("outlier_detection.R")

cat("============================================================\n")
cat("         Outlier Detection Utils - Usage Examples          \n")
cat("============================================================\n\n")

# ============================================================================
# Example 1: Basic IQR Detection
# ============================================================================

cat("Example 1: Basic IQR Outlier Detection\n")
cat("--------------------------------------\n")

data1 <- c(12, 15, 14, 10, 13, 17, 16, 14, 11, 13, 100, 150)
cat("Data:", paste(data1, collapse = ", "), "\n\n")

result1 <- detect_outliers_iqr(data1)
cat("Method:", result1$method, "\n")
cat("Q1:", result1$q1, "  Q3:", result1$q3, "  IQR:", result1$iqr, "\n")
cat("Lower Bound:", result1$lower_bound, "\n")
cat("Upper Bound:", result1$upper_bound, "\n")
cat("Outliers detected:", result1$total_detected, "\n")
cat("Outlier values:", paste(result1$outliers, collapse = ", "), "\n")
cat("Outlier indices:", paste(result1$indices, collapse = ", "), "\n\n")

# ============================================================================
# Example 2: Z-Score Method
# ============================================================================

cat("Example 2: Z-Score Outlier Detection\n")
cat("------------------------------------\n")

set.seed(42)
data2 <- c(rnorm(30, mean = 50, sd = 5), 95, 105)  # Normal data + outliers
cat("Generated 30 normal values (mean=50, sd=5) plus 2 outliers: 95, 105\n\n")

result2 <- detect_outliers_zscore(data2, threshold = 2.5)
cat("Method:", result2$method, "\n")
cat("Mean:", round(result2$mean, 2), "  SD:", round(result2$sd, 2), "\n")
cat("Threshold:", result2$threshold, "\n")
cat("Outliers detected:", result2$total_detected, "\n")
cat("Outlier values:", paste(round(result2$outliers, 2), collapse = ", "), "\n\n")

# ============================================================================
# Example 3: Modified Z-Score (MAD) - Robust Method
# ============================================================================

cat("Example 3: Modified Z-Score (MAD) - Robust Detection\n")
cat("----------------------------------------------------\n")

data3 <- c(1.2, 1.5, 1.3, 1.4, 1.6, 1.3, 1.5, 1.4, 50)  # One extreme outlier
cat("Data with extreme outlier:", paste(data3, collapse = ", "), "\n\n")

result_zscore <- detect_outliers_zscore(data3)
result_mad <- detect_outliers_mad(data3)

cat("Standard Z-Score Method:\n")
cat("  Mean:", round(result_zscore$mean, 2), "  SD:", round(result_zscore$sd, 2), "\n")
cat("  Outliers:", result_zscore$total_detected, "\n\n")

cat("Modified Z-Score (MAD) Method:\n")
cat("  Median:", round(result_mad$median, 2), "  MAD:", round(result_mad$mad, 2), "\n")
cat("  Outliers:", result_mad$total_detected, "\n")
cat("  Note: MAD is more robust to extreme outliers!\n\n")

# ============================================================================
# Example 4: Percentile Method
# ============================================================================

cat("Example 4: Percentile-Based Detection\n")
cat("-------------------------------------\n")

data4 <- c(1:50, 95, 99, 101)
cat("Data:", paste(data4[1:10], collapse = ", "), "...", 
    paste(tail(data4, 5), collapse = ", "), "\n\n")

result4 <- detect_outliers_percentile(data4, lower_percentile = 5, upper_percentile = 95)
cat("Method:", result4$method, "\n")
cat("Lower percentile:", result4$lower_percentile, "% -> Bound:", result4$lower_bound, "\n")
cat("Upper percentile:", result4$upper_percentile, "% -> Bound:", result4$upper_bound, "\n")
cat("Outliers detected:", result4$total_detected, "\n")
cat("Outlier values:", paste(result4$outliers, collapse = ", "), "\n\n")

# ============================================================================
# Example 5: Tukey's Fences (Inner and Outer)
# ============================================================================

cat("Example 5: Tukey's Fences\n")
cat("-------------------------\n")

data5 <- c(10, 12, 14, 15, 16, 18, 19, 20, 22, 35, 60)
cat("Data:", paste(data5, collapse = ", "), "\n\n")

result_inner <- detect_outliers_tukey(data5, "inner")
result_outer <- detect_outliers_tukey(data5, "outer")

cat("Inner Fences (1.5 * IQR):\n")
cat("  Bounds: [", round(result_inner$lower_bound, 2), ",", 
    round(result_inner$upper_bound, 2), "]\n")
cat("  Outliers:", result_inner$total_detected, "\n")
cat("  Values:", paste(result_inner$outliers, collapse = ", "), "\n\n")

cat("Outer Fences (3 * IQR):\n")
cat("  Bounds: [", round(result_outer$lower_bound, 2), ",", 
    round(result_outer$upper_bound, 2), "]\n")
cat("  Outliers:", result_outer$total_detected, "\n")
cat("  Values:", paste(result_outer$outliers, collapse = ", "), "\n\n")

# ============================================================================
# Example 6: Grubbs' Test for Single Outlier
# ============================================================================

cat("Example 6: Grubbs' Test for Single Outlier\n")
cat("------------------------------------------\n")

data6 <- c(98, 99, 100, 101, 102, 103, 104, 105, 106, 150)
cat("Data:", paste(data6, collapse = ", "), "\n\n")

result6 <- detect_outlier_grubbs(data6, alpha = 0.05)
cat("Method:", result6$method, "\n")
cat("G-statistic:", round(result6$g_statistic, 4), "\n")
cat("Critical value (alpha=0.05):", round(result6$critical_value, 4), "\n")
cat("Is outlier:", result6$is_outlier, "\n")
cat("Outlier value:", result6$outlier_value, "\n")
cat("Outlier index:", result6$outlier_index, "\n\n")

# ============================================================================
# Example 7: Dixon's Q Test for Small Samples
# ============================================================================

cat("Example 7: Dixon's Q Test for Small Samples\n")
cat("-------------------------------------------\n")

data7 <- c(1.23, 1.25, 1.24, 1.22, 1.26, 1.24, 1.85)
cat("Data (n=7):", paste(data7, collapse = ", "), "\n\n")

result7 <- detect_outlier_dixon(data7, alpha = 0.05)
cat("Method:", result7$method, "\n")
cat("Q-statistic:", round(result7$q_statistic, 4), "\n")
cat("Critical value (alpha=0.05):", result7$critical_value, "\n")
cat("Is outlier:", result7$is_outlier, "\n")
cat("Outlier value:", result7$outlier_value, "\n")
cat("Outlier position:", result7$outlier_position, "\n\n")

# ============================================================================
# Example 8: Comprehensive Analysis (All Methods)
# ============================================================================

cat("Example 8: Comprehensive Analysis\n")
cat("---------------------------------\n")

set.seed(123)
data8 <- c(rnorm(25, mean = 100, sd = 10), 50, 160)  # 25 normal + 2 outliers
cat("Generated 25 normal values (mean=100, sd=10) plus 2 outliers: 50, 160\n\n")

result8 <- detect_outliers_all(data8)

cat("Summary of all methods:\n")
print(result8$summary)
cat("\n")

cat("Consensus outliers (detected by 3+ methods):\n")
cat("  Indices:", paste(result8$consensus$outlier_indices, collapse = ", "), "\n")
cat("  Values:", paste(round(result8$consensus$outlier_values, 2), collapse = ", "), "\n")
cat("  Detection counts per index:\n")
for (idx in names(result8$consensus$detection_counts)) {
  cat(sprintf("    Index %s: %d methods\n", idx, result8$consensus$detection_counts[idx]))
}
cat("\n")

# ============================================================================
# Example 9: Removing Outliers
# ============================================================================

cat("Example 9: Removing Outliers\n")
cat("----------------------------\n")

data9 <- c(10, 12, 14, 15, 16, 18, 19, 20, 22, 100)
cat("Original data:", paste(data9, collapse = ", "), "\n\n")

removed <- remove_outliers(data9, method = "iqr")
cat("After removing outliers (IQR method):\n")
cat("  Cleaned:", paste(removed$cleaned, collapse = ", "), "\n")
cat("  Removed indices:", paste(removed$removed_indices, collapse = ", "), "\n")
cat("  Removed values:", paste(removed$removed_values, collapse = ", "), "\n\n")

# ============================================================================
# Example 10: Replacing Outliers
# ============================================================================

cat("Example 10: Replacing Outliers\n")
cat("-----------------------------\n")

data10 <- c(10, 12, 14, 15, 16, 18, 19, 20, 22, 100)
cat("Original data:", paste(data10, collapse = ", "), "\n\n")

# Replace with median
replaced_median <- replace_outliers(data10, method = "iqr", replacement = "median")
cat("Replace with median:\n")
cat("  Result:", paste(replaced_median$replaced, collapse = ", "), "\n")
cat("  Replacement value:", replaced_median$replacement_value, "\n\n")

# Replace with mean
replaced_mean <- replace_outliers(data10, method = "iqr", replacement = "mean")
cat("Replace with mean:\n")
cat("  Result:", paste(round(replaced_mean$replaced, 2), collapse = ", "), "\n")
cat("  Replacement value:", round(replaced_mean$replacement_value, 2), "\n\n")

# Winsorize (trim to bounds)
replaced_trim <- replace_outliers(data10, method = "iqr", replacement = "trim")
cat("Winsorize (trim to bounds):\n")
cat("  Result:", paste(round(replaced_trim$replaced, 2), collapse = ", "), "\n\n")

# Custom value
replaced_custom <- replace_outliers(data10, method = "iqr", replacement = -1)
cat("Replace with custom value (-1):\n")
cat("  Result:", paste(replaced_custom$replaced, collapse = ", "), "\n\n")

# ============================================================================
# Example 11: Box Plot Statistics
# ============================================================================

cat("Example 11: Box Plot Statistics\n")
cat("-------------------------------\n")

data11 <- c(5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 45)
cat("Data:", paste(data11, collapse = ", "), "\n\n")

bp_stats <- boxplot_outlier_stats(data11)
cat("Box Plot Statistics:\n")
cat("  Lower whisker:", bp_stats$lower_whisker, "\n")
cat("  Q1:", bp_stats$q1, "\n")
cat("  Median:", bp_stats$median, "\n")
cat("  Q3:", bp_stats$q3, "\n")
cat("  Upper whisker:", bp_stats$upper_whisker, "\n")
cat("  Outliers:", paste(bp_stats$outliers, collapse = ", "), "\n\n")

# ============================================================================
# Example 12: Real-World Scenario - Temperature Anomalies
# ============================================================================

cat("Example 12: Real-World Scenario - Temperature Anomalies\n")
cat("-------------------------------------------------------\n")

# Simulated daily temperatures for a month
set.seed(456)
normal_temps <- rnorm(28, mean = 22, sd = 3)
# Add some anomalies (sensor errors)
temp_data <- c(normal_temps, 55, -15)  # Impossible temperatures
cat("Daily temperatures (30 days) with sensor errors:\n")
cat("Normal range: 15-30°C\n")
cat("Anomalies: 55°C and -15°C\n\n")

result_temp <- detect_outliers_all(temp_data)
cat("Detection Summary:\n")
print(result_temp$summary)
cat("\n")

cat("Recommended action: Remove or flag", result_temp$consensus$total_detected, 
    "anomalous readings\n\n")

# ============================================================================
# Example 13: Choosing the Right Method
# ============================================================================

cat("Example 13: Choosing the Right Method\n")
cat("-------------------------------------\n")

cat("Method Selection Guide:\n")
cat("  - IQR/Tukey: General purpose, no distribution assumptions\n")
cat("  - Z-Score: Normally distributed data, sensitive to extreme values\n")
cat("  - MAD: Non-normal distributions, more robust than Z-score\n")
cat("  - Percentile: Custom thresholds, non-parametric\n")
cat("  - Grubbs: Testing for ONE outlier, assumes normality\n")
cat("  - Dixon: Small samples (n=3-30), single outlier\n\n")

cat("For this example, comparing methods on skewed data:\n")
skewed_data <- c(rexp(50, rate = 0.1), 100)  # Exponential + outlier
cat("Data: Exponential distribution + outlier at 100\n\n")

iqr_result <- detect_outliers_iqr(skewed_data)
zscore_result <- detect_outliers_zscore(skewed_data, threshold = 3)
mad_result <- detect_outliers_mad(skewed_data)

cat(sprintf("IQR method:      %2d outliers\n", iqr_result$total_detected))
cat(sprintf("Z-Score method:  %2d outliers\n", zscore_result$total_detected))
cat(sprintf("MAD method:      %2d outliers (recommended for skewed data)\n", 
            mad_result$total_detected))
cat("\n")

cat("============================================================\n")
cat("              Examples Complete!                           \n")
cat("============================================================\n")