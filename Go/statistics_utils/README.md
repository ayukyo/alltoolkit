# Statistics Utils (Go)

A comprehensive, zero-dependency Go library for statistical analysis. Provides essential statistical functions for data analysis, scientific computing, and machine learning applications.

## Features

### Basic Statistics
- **Sum** - Calculate sum of dataset
- **Mean** - Arithmetic mean (average)
- **Median** - Middle value of sorted dataset
- **Mode** - Most frequent value(s)
- **Min/Max/Range** - Basic descriptive statistics

### Measures of Spread
- **Variance** - Sample variance (with Bessel's correction)
- **PopVariance** - Population variance
- **StdDev** - Sample standard deviation
- **PopStdDev** - Population standard deviation
- **CoeffVar** - Coefficient of variation (%)
- **IQR** - Interquartile range
- **MedianAbsoluteDeviation** - Robust variability measure

### Different Types of Means
- **GeometricMean** - Nth root of product (for growth rates)
- **HarmonicMean** - Reciprocal mean (for rates/averages)
- **WeightedMean** - Mean with weights

### Distribution Shape
- **Skewness** - Measure of asymmetry
- **Kurtosis** - Measure of tailedness (excess kurtosis)

### Percentiles & Quartiles
- **Percentile** - Value at any percentile (0-100)
- **Quartiles** - Q1, Q2 (median), Q3
- **IQR** - Interquartile range

### Outlier Detection
- **Outliers** - Find values outside 1.5×IQR fences

### Normalization
- **ZScores** - Standard score normalization
- **Normalize** - Min-max normalization to [0, 1]
- **Standardize** - Same as ZScores

### Time Series Analysis
- **MovingAverage** - Simple moving average (SMA)
- **ExponentialMovingAverage** - EMA with smoothing factor

### Robust Statistics
- **TrimmedMean** - Mean excluding extreme values
- **MedianAbsoluteDeviation** - MAD (robust alternative to std dev)

### Correlation Analysis
- **Covariance** - Covariance between two datasets
- **Correlation** - Pearson correlation coefficient

### Comprehensive Analysis
- **Describe** - Full statistical summary in one call

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/statistics_utils
```

## Quick Start

```go
package main

import (
    "fmt"
    "statistics_utils"
)

func main() {
    data := []float64{23, 45, 67, 89, 12, 34, 56, 78, 90, 11}
    
    // Basic statistics
    mean, _ := statistics_utils.Mean(data)
    median, _ := statistics_utils.Median(data)
    stdDev, _ := statistics_utils.StdDev(data)
    
    fmt.Printf("Mean: %.2f\n", mean)
    fmt.Printf("Median: %.2f\n", median)
    fmt.Printf("Std Dev: %.2f\n", stdDev)
    
    // Get comprehensive statistics
    stats, _ := statistics_utils.Describe(data)
    fmt.Printf("Count: %d\n", stats.Count)
    fmt.Printf("Min: %.2f, Max: %.2f\n", stats.Min, stats.Max)
    fmt.Printf("Skewness: %.4f, Kurtosis: %.4f\n", stats.Skewness, stats.Kurtosis)
}
```

## API Reference

### Basic Functions

```go
// Sum of all values
sum, err := statistics_utils.Sum(data)

// Arithmetic mean
mean, err := statistics_utils.Mean(data)

// Median (middle value)
median, err := statistics_utils.Median(data)

// Mode (most frequent value)
mode, err := statistics_utils.Mode(data)

// All modes if multiple
modes, err := statistics_utils.Modes(data)

// Min, Max, Range
minVal, err := statistics_utils.Min(data)
maxVal, err := statistics_utils.Max(data)
rangeVal, err := statistics_utils.Range(data)
```

### Variance & Standard Deviation

```go
// Sample variance (n-1 denominator)
variance, err := statistics_utils.Variance(data)

// Population variance (n denominator)
popVar, err := statistics_utils.PopVariance(data)

// Sample standard deviation
stdDev, err := statistics_utils.StdDev(data)

// Population standard deviation
popStdDev, err := statistics_utils.PopStdDev(data)
```

### Percentiles

```go
// Any percentile (0-100)
p25, err := statistics_utils.Percentile(data, 25)
p50, err := statistics_utils.Percentile(data, 50)  // Median
p75, err := statistics_utils.Percentile(data, 75)
p95, err := statistics_utils.Percentile(data, 95)

// Quartiles
q1, q2, q3, err := statistics_utils.Quartiles(data)

// Interquartile range
iqr, err := statistics_utils.IQR(data)
```

### Different Means

```go
// Geometric mean (all values must be positive)
geoMean, err := statistics_utils.GeometricMean(positiveData)

// Harmonic mean (all values must be positive)
harmMean, err := statistics_utils.HarmonicMean(positiveData)

// Weighted mean
weights := []float64{1, 2, 3, 4, 5}
weightedMean, err := statistics_utils.WeightedMean(data, weights)
```

### Distribution Shape

```go
// Skewness: negative = left-skewed, positive = right-skewed
skewness, err := statistics_utils.Skewness(data)

// Kurtosis: excess kurtosis (normal = 0)
kurtosis, err := statistics_utils.Kurtosis(data)
```

### Outlier Detection

```go
// Returns lower and upper outliers (outside 1.5×IQR)
lowerOutliers, upperOutliers, err := statistics_utils.Outliers(data)
```

### Normalization

```go
// Z-score normalization (mean=0, std=1)
zScores, err := statistics_utils.ZScores(data)

// Min-max normalization (range [0, 1])
normalized, err := statistics_utils.Normalize(data)

// Single value z-score
zScore := statistics_utils.ZScore(value, mean, stdDev)
```

### Time Series

```go
// Simple moving average (window = 3)
sma, err := statistics_utils.MovingAverage(data, 3)

// Exponential moving average (alpha = 0.3)
ema, err := statistics_utils.ExponentialMovingAverage(data, 0.3)
```

### Correlation

```go
// Covariance between two datasets
cov, err := statistics_utils.Covariance(x, y)

// Pearson correlation (-1 to 1)
corr, err := statistics_utils.Correlation(x, y)
```

### Robust Statistics

```go
// Trimmed mean (exclude 10% from each end)
trimmedMean, err := statistics_utils.TrimmedMean(data, 10)

// Median absolute deviation
mad, err := statistics_utils.MedianAbsoluteDeviation(data)
```

### Comprehensive Statistics

```go
stats, err := statistics_utils.Describe(data)
// Returns Statistics struct with all metrics
```

## Statistics Struct

```go
type Statistics struct {
    Count         int     // Number of values
    Sum           float64 // Sum of all values
    Mean          float64 // Arithmetic mean
    Median        float64 // Median (Q2)
    Mode          float64 // Most frequent value
    Min           float64 // Minimum value
    Max           float64 // Maximum value
    Range         float64 // Max - Min
    Variance      float64 // Sample variance
    StdDev        float64 // Sample standard deviation
    PopVariance   float64 // Population variance
    PopStdDev     float64 // Population standard deviation
    Skewness      float64 // Distribution asymmetry
    Kurtosis      float64 // Excess kurtosis
    GeometricMean  float64 // Geometric mean (if all positive)
    HarmonicMean   float64 // Harmonic mean (if all positive)
    Quartile1      float64 // First quartile (25th percentile)
    Quartile3      float64 // Third quartile (75th percentile)
    IQR            float64 // Interquartile range
    LowerFence     float64 // Q1 - 1.5×IQR
    UpperFence     float64 // Q3 + 1.5×IQR
    CoeffVar       float64 // Coefficient of variation (%)
}
```

## Use Cases

### Data Analysis
```go
stats, _ := statistics_utils.Describe(dataset)
fmt.Printf("Data spread: %.2f%% (CV)\n", stats.CoeffVar)
if stats.Skewness > 0.5 {
    fmt.Println("Right-skewed distribution detected")
}
```

### Financial Analysis
```go
// Calculate average return with geometric mean (CAGR)
returns := []float64{1.1, 1.15, 1.08, 1.12, 1.05}
cagr, _ := statistics_utils.GeometricMean(returns)
```

### Quality Control
```go
// Use IQR method for outlier detection
lowerOutliers, upperOutliers, _ := statistics_utils.Outliers(measurements)
if len(lowerOutliers) > 0 || len(upperOutliers) > 0 {
    fmt.Println("Anomalies detected!")
}
```

### Moving Averages for Trends
```go
// Smooth time series data
prices := []float64{100, 102, 101, 104, 107, 105, 108, 110, 112, 115}
sma, _ := statistics_utils.MovingAverage(prices, 5) // 5-day moving average
ema, _ := statistics_utils.ExponentialMovingAverage(prices, 0.2) // More weight on recent
```

### Correlation Analysis
```go
// Check relationship between two variables
hoursStudied := []float64{1, 2, 3, 4, 5}
testScores := []float64{60, 70, 75, 85, 95}
corr, _ := statistics_utils.Correlation(hoursStudied, testScores)
fmt.Printf("Correlation: %.2f\n", corr) // Strong positive correlation
```

## Error Handling

All functions return errors for edge cases:

```go
mean, err := statistics_utils.Mean(data)
if err != nil {
    switch err {
    case statistics_utils.ErrEmptyDataset:
        fmt.Println("Dataset is empty")
    case statistics_utils.ErrNonPositive:
        fmt.Println("Values must be positive for this operation")
    default:
        fmt.Printf("Error: %v\n", err)
    }
}
```

## Testing

Run the test suite:

```bash
cd Go/statistics_utils
go test -v
```

## Performance

All functions are optimized for performance:
- Single-pass algorithms where possible
- No external dependencies
- Memory-efficient implementations

## License

MIT License - See LICENSE file for details.