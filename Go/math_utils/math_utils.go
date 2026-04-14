// Package mathutils provides mathematical and statistical utility functions.
// All functions are safe for concurrent use and handle edge cases gracefully.
package mathutils

import (
	"math"
	"sort"
)

// Mean calculates the arithmetic mean (average) of a slice of float64 values.
// Returns 0 if the slice is empty.
//
// Parameters:
//   - values: A slice of float64 values to calculate the mean of.
//
// Returns:
//   - The arithmetic mean of the values.
//   - 0 if the slice is empty.
//
// Example:
//
//     Mean([]float64{1, 2, 3, 4, 5})  // Returns 3.0
//     Mean([]float64{})                // Returns 0.0
func Mean(values []float64) float64 {
	if len(values) == 0 {
		return 0
	}
	sum := 0.0
	for _, v := range values {
		sum += v
	}
	return sum / float64(len(values))
}

// Median calculates the median (middle value) of a slice of float64 values.
// For even-length slices, returns the average of the two middle values.
// Returns 0 if the slice is empty.
//
// Parameters:
//   - values: A slice of float64 values to calculate the median of.
//
// Returns:
//   - The median value of the slice.
//   - 0 if the slice is empty.
//
// Example:
//
//     Median([]float64{1, 3, 5})      // Returns 3.0
//     Median([]float64{1, 2, 3, 4})   // Returns 2.5
func Median(values []float64) float64 {
	if len(values) == 0 {
		return 0
	}

	// Create a copy to avoid modifying the original
	sorted := make([]float64, len(values))
	copy(sorted, values)
	sort.Float64s(sorted)

	n := len(sorted)
	if n%2 == 1 {
		return sorted[n/2]
	}
	return (sorted[n/2-1] + sorted[n/2]) / 2
}

// Mode calculates the mode (most frequent value) of a slice of float64 values.
// Returns all modes if there are multiple values with the same highest frequency.
// Returns an empty slice if the input is empty.
//
// Parameters:
//   - values: A slice of float64 values to calculate the mode of.
//
// Returns:
//   - A slice containing all mode values.
//   - Empty slice if input is empty.
//
// Example:
//
//     Mode([]float64{1, 2, 2, 3, 3, 3})    // Returns [3]
//     Mode([]float64{1, 1, 2, 2})          // Returns [1, 2]
func Mode(values []float64) []float64 {
	if len(values) == 0 {
		return []float64{}
	}

	frequency := make(map[float64]int)
	for _, v := range values {
		frequency[v]++
	}

	maxFreq := 0
	for _, count := range frequency {
		if count > maxFreq {
			maxFreq = count
		}
	}

	var modes []float64
	for v, count := range frequency {
		if count == maxFreq {
			modes = append(modes, v)
		}
	}

	sort.Float64s(modes)
	return modes
}

// Variance calculates the population variance of a slice of float64 values.
// Returns 0 if the slice has fewer than 2 elements.
//
// Parameters:
//   - values: A slice of float64 values to calculate the variance of.
//
// Returns:
//   - The population variance of the values.
//   - 0 if the slice has fewer than 2 elements.
//
// Example:
//
//     Variance([]float64{2, 4, 4, 4, 5, 5, 7, 9})  // Returns 4.0
func Variance(values []float64) float64 {
	if len(values) < 2 {
		return 0
	}

	mean := Mean(values)
	sumSquaredDiff := 0.0
	for _, v := range values {
		diff := v - mean
		sumSquaredDiff += diff * diff
	}

	return sumSquaredDiff / float64(len(values))
}

// SampleVariance calculates the sample variance (with Bessel's correction) of a slice of float64 values.
// Returns 0 if the slice has fewer than 2 elements.
//
// Parameters:
//   - values: A slice of float64 values to calculate the sample variance of.
//
// Returns:
//   - The sample variance of the values.
//   - 0 if the slice has fewer than 2 elements.
//
// Example:
//
//     SampleVariance([]float64{2, 4, 4, 4, 5, 5, 7, 9})  // Returns ~4.57
func SampleVariance(values []float64) float64 {
	if len(values) < 2 {
		return 0
	}

	mean := Mean(values)
	sumSquaredDiff := 0.0
	for _, v := range values {
		diff := v - mean
		sumSquaredDiff += diff * diff
	}

	return sumSquaredDiff / float64(len(values)-1)
}

// StdDev calculates the population standard deviation of a slice of float64 values.
// Returns 0 if the slice has fewer than 2 elements.
//
// Parameters:
//   - values: A slice of float64 values to calculate the standard deviation of.
//
// Returns:
//   - The population standard deviation of the values.
//   - 0 if the slice has fewer than 2 elements.
//
// Example:
//
//     StdDev([]float64{2, 4, 4, 4, 5, 5, 7, 9})  // Returns 2.0
func StdDev(values []float64) float64 {
	return math.Sqrt(Variance(values))
}

// SampleStdDev calculates the sample standard deviation of a slice of float64 values.
// Returns 0 if the slice has fewer than 2 elements.
//
// Parameters:
//   - values: A slice of float64 values to calculate the sample standard deviation of.
//
// Returns:
//   - The sample standard deviation of the values.
//   - 0 if the slice has fewer than 2 elements.
func SampleStdDev(values []float64) float64 {
	return math.Sqrt(SampleVariance(values))
}

// Min returns the minimum value from a slice of float64 values.
// Returns 0 and false if the slice is empty.
//
// Parameters:
//   - values: A slice of float64 values to find the minimum of.
//
// Returns:
//   - The minimum value.
//   - true if found, false if slice is empty.
//
// Example:
//
//     Min([]float64{3, 1, 4, 1, 5})  // Returns 1.0, true
//     Min([]float64{})                 // Returns 0.0, false
func Min(values []float64) (float64, bool) {
	if len(values) == 0 {
		return 0, false
	}

	minVal := values[0]
	for _, v := range values[1:] {
		if v < minVal {
			minVal = v
		}
	}
	return minVal, true
}

// Max returns the maximum value from a slice of float64 values.
// Returns 0 and false if the slice is empty.
//
// Parameters:
//   - values: A slice of float64 values to find the maximum of.
//
// Returns:
//   - The maximum value.
//   - true if found, false if slice is empty.
//
// Example:
//
//     Max([]float64{3, 1, 4, 1, 5})  // Returns 5.0, true
//     Max([]float64{})                 // Returns 0.0, false
func Max(values []float64) (float64, bool) {
	if len(values) == 0 {
		return 0, false
	}

	maxVal := values[0]
	for _, v := range values[1:] {
		if v > maxVal {
			maxVal = v
		}
	}
	return maxVal, true
}

// Sum returns the sum of all values in a slice of float64 values.
// Returns 0 if the slice is empty.
//
// Parameters:
//   - values: A slice of float64 values to sum.
//
// Returns:
//   - The sum of all values.
//   - 0 if the slice is empty.
//
// Example:
//
//     Sum([]float64{1, 2, 3, 4, 5})  // Returns 15.0
func Sum(values []float64) float64 {
	sum := 0.0
	for _, v := range values {
		sum += v
	}
	return sum
}

// Range calculates the range (max - min) of a slice of float64 values.
// Returns 0 if the slice is empty.
//
// Parameters:
//   - values: A slice of float64 values to calculate the range of.
//
// Returns:
//   - The range (max - min) of the values.
//   - 0 if the slice is empty.
//
// Example:
//
//     Range([]float64{1, 5, 3, 9, 2})  // Returns 8.0
func Range(values []float64) float64 {
	if len(values) == 0 {
		return 0
	}

	minVal, _ := Min(values)
	maxVal, _ := Max(values)
	return maxVal - minVal
}

// Percentile calculates the value at a given percentile (0-100) of a slice of float64 values.
// Uses linear interpolation for non-integer positions.
// Returns 0 if the slice is empty.
//
// Parameters:
//   - values: A slice of float64 values to calculate the percentile of.
//   - p: The percentile to calculate (0-100).
//
// Returns:
//   - The value at the given percentile.
//   - 0 if the slice is empty.
//   - Panics if p is not between 0 and 100.
//
// Example:
//
//     Percentile([]float64{1, 2, 3, 4, 5}, 50)   // Returns 3.0 (median)
//     Percentile([]float64{1, 2, 3, 4, 5}, 25)   // Returns 2.0
func Percentile(values []float64, p float64) float64 {
	if len(values) == 0 {
		return 0
	}
	if p < 0 || p > 100 {
		panic("percentile must be between 0 and 100")
	}

	// Create a sorted copy
	sorted := make([]float64, len(values))
	copy(sorted, values)
	sort.Float64s(sorted)

	if p == 100 {
		return sorted[len(sorted)-1]
	}
	if p == 0 {
		return sorted[0]
	}

	// Calculate position using linear interpolation
	n := len(sorted)
	rank := p / 100 * float64(n-1)
	lowerIdx := int(rank)
	upperIdx := lowerIdx + 1

	if upperIdx >= n {
		return sorted[n-1]
	}

	fraction := rank - float64(lowerIdx)
	return sorted[lowerIdx] + fraction*(sorted[upperIdx]-sorted[lowerIdx])
}

// Quartiles calculates the three quartiles (Q1, Q2, Q3) of a slice of float64 values.
// Q1 = 25th percentile, Q2 = 50th percentile (median), Q3 = 75th percentile.
// Returns all zeros if the slice is empty.
//
// Parameters:
//   - values: A slice of float64 values to calculate the quartiles of.
//
// Returns:
//   - q1: The first quartile (25th percentile).
//   - q2: The second quartile (median).
//   - q3: The third quartile (75th percentile).
//
// Example:
//
//     q1, q2, q3 := Quartiles([]float64{1, 2, 3, 4, 5, 6, 7, 8})
//     // q1 = 2.75, q2 = 4.5, q3 = 6.25
func Quartiles(values []float64) (q1, q2, q3 float64) {
	if len(values) == 0 {
		return 0, 0, 0
	}

	q1 = Percentile(values, 25)
	q2 = Percentile(values, 50)
	q3 = Percentile(values, 75)
	return q1, q2, q3
}

// IQR calculates the interquartile range (Q3 - Q1) of a slice of float64 values.
// Returns 0 if the slice is empty.
//
// Parameters:
//   - values: A slice of float64 values to calculate the IQR of.
//
// Returns:
//   - The interquartile range (Q3 - Q1).
//
// Example:
//
//     IQR([]float64{1, 2, 3, 4, 5, 6, 7, 8})  // Returns 3.5
func IQR(values []float64) float64 {
	q1, _, q3 := Quartiles(values)
	return q3 - q1
}

// GeometricMean calculates the geometric mean of a slice of positive float64 values.
// Returns 0 if the slice is empty or contains non-positive values.
//
// Parameters:
//   - values: A slice of positive float64 values.
//
// Returns:
//   - The geometric mean of the values.
//   - 0 if the slice is empty or contains non-positive values.
//
// Example:
//
//     GeometricMean([]float64{2, 8})  // Returns 4.0
func GeometricMean(values []float64) float64 {
	if len(values) == 0 {
		return 0
	}

	sum := 0.0
	for _, v := range values {
		if v <= 0 {
			return 0
		}
		sum += math.Log(v)
	}

	return math.Exp(sum / float64(len(values)))
}

// HarmonicMean calculates the harmonic mean of a slice of positive float64 values.
// Returns 0 if the slice is empty or contains non-positive values.
//
// Parameters:
//   - values: A slice of positive float64 values.
//
// Returns:
//   - The harmonic mean of the values.
//   - 0 if the slice is empty or contains non-positive values.
//
// Example:
//
//     HarmonicMean([]float64{1, 4})  // Returns 1.6
func HarmonicMean(values []float64) float64 {
	if len(values) == 0 {
		return 0
	}

	sumReciprocal := 0.0
	for _, v := range values {
		if v <= 0 {
			return 0
		}
		sumReciprocal += 1.0 / v
	}

	return float64(len(values)) / sumReciprocal
}

// Stats contains summary statistics for a dataset.
type Stats struct {
	Count   int
	Sum     float64
	Mean    float64
	Median  float64
	Mode    []float64
	Min     float64
	Max     float64
	Range   float64
	Variance float64
	StdDev  float64
	Q1      float64
	Q2      float64
	Q3      float64
	IQR     float64
}

// Describe calculates comprehensive summary statistics for a slice of float64 values.
// Returns a Stats struct with all fields set to zero values if the slice is empty.
//
// Parameters:
//   - values: A slice of float64 values to analyze.
//
// Returns:
//   - A Stats struct containing all summary statistics.
//
// Example:
//
//     stats := Describe([]float64{1, 2, 3, 4, 5})
//     // stats.Mean = 3.0, stats.StdDev = 1.414..., etc.
func Describe(values []float64) Stats {
	if len(values) == 0 {
		return Stats{}
	}

	minVal, _ := Min(values)
	maxVal, _ := Max(values)
	q1, q2, q3 := Quartiles(values)

	return Stats{
		Count:    len(values),
		Sum:      Sum(values),
		Mean:     Mean(values),
		Median:   Median(values),
		Mode:     Mode(values),
		Min:      minVal,
		Max:      maxVal,
		Range:    maxVal - minVal,
		Variance: Variance(values),
		StdDev:   StdDev(values),
		Q1:       q1,
		Q2:       q2,
		Q3:       q3,
		IQR:      q3 - q1,
	}
}

// CoefficientOfVariation calculates the coefficient of variation (CV) as a percentage.
// CV = (StdDev / Mean) * 100
// Returns 0 if the slice has fewer than 2 elements or if mean is 0.
//
// Parameters:
//   - values: A slice of float64 values to calculate the CV of.
//
// Returns:
//   - The coefficient of variation as a percentage.
//
// Example:
//
//     CoefficientOfVariation([]float64{10, 12, 14, 16, 18})  // Returns ~22.36
func CoefficientOfVariation(values []float64) float64 {
	if len(values) < 2 {
		return 0
	}

	mean := Mean(values)
	if mean == 0 {
		return 0
	}

	return (StdDev(values) / mean) * 100
}

// ZScore calculates the z-score (standard score) for a given value.
// Z = (x - mean) / stddev
// Returns 0 if the slice has fewer than 2 elements or stddev is 0.
//
// Parameters:
//   - values: The dataset to use for calculating mean and stddev.
//   - x: The value to calculate the z-score for.
//
// Returns:
//   - The z-score of the value x.
//
// Example:
//
//     ZScore([]float64{1, 2, 3, 4, 5}, 3)  // Returns 0.0
//     ZScore([]float64{1, 2, 3, 4, 5}, 1)  // Returns -1.414...
func ZScore(values []float64, x float64) float64 {
	if len(values) < 2 {
		return 0
	}

	stddev := StdDev(values)
	if stddev == 0 {
		return 0
	}

	return (x - Mean(values)) / stddev
}