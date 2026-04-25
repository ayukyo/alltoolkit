# Statistics Utilities (Fortran)

Complete statistics module for Fortran with zero external dependencies.

## Features

### Basic Statistics
- **mean** - Arithmetic mean
- **geometric_mean** - Geometric mean (for positive values)
- **harmonic_mean** - Harmonic mean (for positive values)
- **median** - Median value
- **mode** - Most frequent value
- **variance** - Sample variance
- **variance_pop** - Population variance
- **std_dev** - Sample standard deviation
- **std_dev_pop** - Population standard deviation
- **range_val** - Range (max - min)
- **coefficient_of_variation** - CV as percentage

### Percentiles
- **percentile** - Any percentile (0-100)
- **quartiles** - Q1, Q2, Q3
- **iqr** - Interquartile range

### Shape Measures
- **skewness** - Fisher's skewness coefficient
- **kurtosis** - Excess kurtosis

### Correlation
- **covariance** - Sample covariance
- **pearson_correlation** - Pearson r coefficient
- **spearman_correlation** - Spearman rank correlation

### Linear Regression
- **linear_regression** - Simple linear regression with R²

### Moving Statistics
- **moving_mean** - Moving/rolling average
- **moving_std** - Moving/rolling standard deviation

### Histogram
- **histogram** - Generate histogram counts and bin edges

### Normalization
- **z_score** - Z-score standardization
- **normalize** - Normalize to [0, 1] range
- **standard_error** - Standard error of the mean
- **confidence_interval** - Confidence interval for the mean

### Probability Distributions
- **normal_pdf** - Normal probability density function
- **normal_cdf** - Normal cumulative distribution function

## Usage

```fortran
use statistics_utils

! Basic statistics
real(8) :: data(10)
data = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0, 6.0d0, 7.0d0, 8.0d0, 9.0d0, 10.0d0/)

print *, "Mean: ", mean(data)
print *, "Median: ", median(data)
print *, "Std Dev: ", std_dev(data)

! Percentiles
print *, "25th percentile: ", percentile(data, 25.0d0)

! Correlation
real(8) :: x(5), y(5)
x = (/1.0d0, 2.0d0, 3.0d0, 4.0d0, 5.0d0/)
y = (/2.0d0, 4.0d0, 6.0d0, 8.0d0, 10.0d0/)
print *, "Pearson r: ", pearson_correlation(x, y)

! Linear regression
real(8) :: slope, intercept, r_sq
call linear_regression(x, y, slope, intercept, r_sq)

! Histogram
integer, allocatable :: counts(:)
real(8), allocatable :: edges(:)
call histogram(data, 5, counts, edges)
```

## Compilation

```bash
# Compile module
gfortran -c statistics_utils.f90

# Compile and run tests
gfortran statistics_utils.f90 statistics_utils_test.f90 -o test
./test

# Compile and run examples
gfortran statistics_utils.f90 statistics_utils_examples.f90 -o examples
./examples
```

## Requirements

- Fortran 90/95 compiler (gfortran, ifort, etc.)
- No external dependencies

## Test Coverage

- 50+ test cases covering all functions
- Tests for edge cases (empty data, constant data)
- Validation against known values

## Version

1.0.0 - 2026-04-25