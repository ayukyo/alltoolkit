# Outlier Detection Utils (R)

A comprehensive R toolkit for detecting outliers in data using multiple statistical methods. Zero external dependencies - uses only base R functions.

## Features

### Detection Methods

| Method | Function | Description | Best For |
|--------|----------|-------------|----------|
| **IQR** | `detect_outliers_iqr()` | Interquartile Range method | General purpose, no distribution assumptions |
| **Z-Score** | `detect_outliers_zscore()` | Standard deviation based | Normally distributed data |
| **Modified Z-Score** | `detect_outliers_mad()` | Median Absolute Deviation | Non-normal distributions, robust |
| **Percentile** | `detect_outliers_percentile()` | Percentile-based bounds | Custom thresholds |
| **Tukey's Fences** | `detect_outliers_tukey()` | Inner (1.5×IQR) or Outer (3×IQR) | Boxplot-style detection |
| **Grubbs' Test** | `detect_outlier_grubbs()` | Statistical test for single outlier | Testing ONE outlier, normal distribution |
| **Dixon's Q** | `detect_outlier_dixon()` | Q-test for small samples | Small samples (n=3-30) |
| **Comprehensive** | `detect_outliers_all()` | All methods + consensus | Complete analysis |

### Utility Functions

- `remove_outliers()` - Remove outliers from data
- `replace_outliers()` - Replace outliers with mean, median, winsorized, or custom values
- `boxplot_outlier_stats()` - Generate box plot statistics

## Quick Start

```r
# Source the module
source("outlier_detection.R")

# Sample data with outliers
data <- c(12, 15, 14, 10, 13, 17, 16, 14, 11, 13, 100, 150)

# Basic IQR detection
result <- detect_outliers_iqr(data)
print(result$outliers)  # [1] 100 150
print(result$indices)   # [1] 11 12

# Z-Score method
result <- detect_outliers_zscore(data, threshold = 3)

# Robust MAD method (better for non-normal distributions)
result <- detect_outliers_mad(data, threshold = 3.5)

# Run all methods and get consensus
result <- detect_outliers_all(data)
print(result$consensus$outlier_values)
```

## Usage Examples

### 1. IQR Method

```r
data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 100)
result <- detect_outliers_iqr(data, multiplier = 1.5)

# Result contains:
# - outliers: detected outlier values
# - indices: positions of outliers
# - lower_bound, upper_bound: IQR bounds
# - q1, q3, iqr: quartile statistics
```

### 2. Z-Score Method

```r
# For normally distributed data
data <- c(rnorm(30, mean = 50, sd = 5), 95, 105)
result <- detect_outliers_zscore(data, threshold = 2.5)

# Lower threshold = more sensitive detection
```

### 3. Modified Z-Score (MAD)

```r
# More robust for non-normal data
data <- c(1.2, 1.5, 1.3, 1.4, 1.6, 1.3, 1.5, 1.4, 50)
result <- detect_outliers_mad(data, threshold = 3.5)
```

### 4. Grubbs' Test for Single Outlier

```r
# Test if there's exactly one outlier
data <- c(98, 99, 100, 101, 102, 103, 104, 105, 106, 150)
result <- detect_outlier_grubbs(data, alpha = 0.05)

if (result$is_outlier) {
  print(paste("Outlier found:", result$outlier_value))
}
```

### 5. Dixon's Q Test for Small Samples

```r
# For small datasets (n=3-30)
data <- c(1.23, 1.25, 1.24, 1.22, 1.26, 1.24, 1.85)
result <- detect_outlier_dixon(data, alpha = 0.05)
```

### 6. Comprehensive Analysis

```r
# Run all methods at once
data <- c(rnorm(25, mean = 100, sd = 10), 50, 160)
result <- detect_outliers_all(data)

# View summary
print(result$summary)

# Get consensus outliers (detected by 3+ methods)
print(result$consensus$outlier_values)
```

### 7. Remove Outliers

```r
data <- c(10, 12, 14, 15, 16, 18, 19, 20, 22, 100)

# Remove outliers (replace with NA)
removed <- remove_outliers(data, method = "iqr")
print(removed$cleaned)  # NA in place of outliers
```

### 8. Replace Outliers

```r
data <- c(10, 12, 14, 15, 16, 18, 19, 20, 22, 100)

# Replace with median
replaced <- replace_outliers(data, method = "iqr", replacement = "median")

# Replace with mean
replaced <- replace_outliers(data, method = "iqr", replacement = "mean")

# Winsorize (trim to bounds)
replaced <- replace_outliers(data, method = "iqr", replacement = "trim")

# Custom value
replaced <- replace_outliers(data, method = "iqr", replacement = -999)
```

## Method Selection Guide

| Scenario | Recommended Method |
|----------|-------------------|
| General purpose | IQR or Tukey's Fences |
| Normal distribution | Z-Score |
| Skewed/non-normal | Modified Z-Score (MAD) |
| Custom percentile thresholds | Percentile |
| Testing single outlier | Grubbs' Test |
| Small samples (n≤30) | Dixon's Q Test |
| Complete analysis | `detect_outliers_all()` |

## Running Tests

```bash
Rscript test_outlier_detection.R
```

## Running Examples

```bash
Rscript examples.R
```

## Return Value Structure

All detection functions return a list with:

```r
list(
  method = "Method Name",
  outliers = c(...),       # Detected outlier values
  indices = c(...),        # Positions in original data
  total_detected = n,      # Count of outliers
  # ... method-specific statistics
)
```

## Dependencies

None! Uses only base R functions:
- `mean()`, `median()`, `sd()`, `quantile()`
- `which()`, `table()`, `sort()`
- `boxplot.stats()`

## License

Part of AllToolkit - MIT License