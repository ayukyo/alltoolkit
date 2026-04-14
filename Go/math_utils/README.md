# math_utils - Mathematical and Statistical Utilities

A comprehensive Go package providing mathematical and statistical utility functions. All functions are safe for concurrent use and handle edge cases gracefully.

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/math_utils
```

## Features

- **Basic Statistics**: Mean, Median, Mode, Sum, Range
- **Dispersion Measures**: Variance, Standard Deviation, IQR, Coefficient of Variation
- **Position Measures**: Percentile, Quartiles, Z-Score
- **Advanced Means**: Geometric Mean, Harmonic Mean
- **Summary Statistics**: `Describe()` function for comprehensive analysis
- **Zero external dependencies**
- **Thread-safe** - All functions use local variables only

## Quick Start

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/math_utils"
)

func main() {
    data := []float64{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    
    // Basic statistics
    fmt.Printf("Mean: %.2f\n", mathutils.Mean(data))
    fmt.Printf("Median: %.2f\n", mathutils.Median(data))
    fmt.Printf("StdDev: %.2f\n", mathutils.StdDev(data))
    
    // Comprehensive summary
    stats := mathutils.Describe(data)
    fmt.Printf("Count: %d\n", stats.Count)
    fmt.Printf("Min: %.2f, Max: %.2f\n", stats.Min, stats.Max)
    fmt.Printf("Q1: %.2f, Q2: %.2f, Q3: %.2f\n", stats.Q1, stats.Q2, stats.Q3)
}
```

## API Reference

### Basic Statistics

#### Mean(values []float64) float64
Calculates the arithmetic mean (average) of a slice.

```go
Mean([]float64{1, 2, 3, 4, 5})  // Returns 3.0
```

#### Median(values []float64) float64
Calculates the median (middle value). For even-length slices, returns the average of two middle values.

```go
Median([]float64{1, 3, 5})      // Returns 3.0
Median([]float64{1, 2, 3, 4})   // Returns 2.5
```

#### Mode(values []float64) []float64
Returns the mode(s) - most frequent value(s). Returns multiple values if there's a tie.

```go
Mode([]float64{1, 2, 2, 3, 3, 3})  // Returns [3]
Mode([]float64{1, 1, 2, 2})        // Returns [1, 2]
```

#### Sum(values []float64) float64
Returns the sum of all values.

```go
Sum([]float64{1, 2, 3, 4, 5})  // Returns 15.0
```

#### Range(values []float64) float64
Returns the range (max - min).

```go
Range([]float64{1, 5, 3, 9, 2})  // Returns 8.0
```

### Min/Max

#### Min(values []float64) (float64, bool)
Returns the minimum value. Returns false if slice is empty.

```go
min, ok := Min([]float64{3, 1, 4, 1, 5})
// min = 1.0, ok = true
```

#### Max(values []float64) (float64, bool)
Returns the maximum value. Returns false if slice is empty.

```go
max, ok := Max([]float64{3, 1, 4, 1, 5})
// max = 5.0, ok = true
```

### Dispersion Measures

#### Variance(values []float64) float64
Calculates population variance.

```go
Variance([]float64{2, 4, 4, 4, 5, 5, 7, 9})  // Returns 4.0
```

#### SampleVariance(values []float64) float64
Calculates sample variance (with Bessel's correction).

```go
SampleVariance([]float64{2, 4, 4, 4, 5, 5, 7, 9})  // Returns ~4.57
```

#### StdDev(values []float64) float64
Calculates population standard deviation.

```go
StdDev([]float64{2, 4, 4, 4, 5, 5, 7, 9})  // Returns 2.0
```

#### SampleStdDev(values []float64) float64
Calculates sample standard deviation.

```go
SampleStdDev([]float64{2, 4, 4, 4, 5, 5, 7, 9})  // Returns ~2.14
```

#### IQR(values []float64) float64
Calculates the interquartile range (Q3 - Q1).

```go
IQR([]float64{1, 2, 3, 4, 5, 6, 7, 8})  // Returns 3.5
```

#### CoefficientOfVariation(values []float64) float64
Calculates CV as a percentage: (StdDev / Mean) * 100

```go
CoefficientOfVariation([]float64{10, 12, 14, 16, 18})  // Returns ~22.36
```

### Position Measures

#### Percentile(values []float64, p float64) float64
Calculates value at given percentile (0-100). Uses linear interpolation.

```go
Percentile([]float64{1, 2, 3, 4, 5}, 50)   // Returns 3.0 (median)
Percentile([]float64{1, 2, 3, 4, 5}, 25)   // Returns 2.0
Percentile([]float64{1, 2, 3, 4, 5}, 75)   // Returns 4.0
```

#### Quartiles(values []float64) (q1, q2, q3 float64)
Calculates the three quartiles.

```go
q1, q2, q3 := Quartiles([]float64{1, 2, 3, 4, 5, 6, 7, 8})
// q1 = 2.75, q2 = 4.5, q3 = 6.25
```

#### ZScore(values []float64, x float64) float64
Calculates the z-score (standard score) for a value.

```go
ZScore([]float64{1, 2, 3, 4, 5}, 3)  // Returns 0.0 (at mean)
ZScore([]float64{1, 2, 3, 4, 5}, 1)  // Returns -1.414...
```

### Advanced Means

#### GeometricMean(values []float64) float64
Calculates geometric mean. Returns 0 for empty or non-positive values.

```go
GeometricMean([]float64{2, 8})     // Returns 4.0
GeometricMean([]float64{1, 2, 4})  // Returns 2.0
```

#### HarmonicMean(values []float64) float64
Calculates harmonic mean. Returns 0 for empty or non-positive values.

```go
HarmonicMean([]float64{1, 4})      // Returns 1.6
HarmonicMean([]float64{1, 2, 4})   // Returns ~1.714
```

### Summary Statistics

#### Describe(values []float64) Stats
Returns comprehensive summary statistics in a struct.

```go
stats := Describe([]float64{1, 2, 3, 4, 5})
// Stats{
//   Count: 5, Sum: 15, Mean: 3, Median: 3,
//   Min: 1, Max: 5, Range: 4,
//   Variance: 2, StdDev: 1.414...,
//   Q1: 1.75, Q2: 3, Q3: 4.25, IQR: 2.5
// }
```

## Edge Cases

All functions handle edge cases gracefully:

| Function | Empty Slice | Single Value | Non-positive Values |
|----------|-------------|--------------|---------------------|
| Mean | 0 | value | ✓ |
| Median | 0 | value | ✓ |
| Mode | [] | [value] | ✓ |
| Variance | 0 | 0 | ✓ |
| StdDev | 0 | 0 | ✓ |
| Min | 0, false | value, true | ✓ |
| Max | 0, false | value, true | ✓ |
| Sum | 0 | value | ✓ |
| Range | 0 | 0 | ✓ |
| GeometricMean | 0 | value | Returns 0 |
| HarmonicMean | 0 | value | Returns 0 |
| Percentile | 0 | value | ✓ |

## Performance

Benchmarks on a standard dataset (1000 elements):

- Mean: ~1μs
- Median: ~50μs (due to sorting)
- StdDev: ~2μs
- Describe: ~150μs (comprehensive analysis)

## License

MIT License