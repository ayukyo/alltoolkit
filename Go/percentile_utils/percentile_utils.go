// Package percentile_utils provides percentile calculation and statistical utilities.
// Zero external dependencies - pure Go standard library implementation.
//
// Core features:
// - Multiple percentile calculation methods (linear, lower, higher, nearest, midpoint)
// - Quartile calculations (Q1, Q2, Q3, IQR)
// - Percentile rank calculation
// - Boxplot statistics
// - Decile calculations
// - Outlier detection
// - Winsorization
// - Normalization by percentile range
//
// Author: AllToolkit
// Date: 2026-05-18
package percentile_utils

import (
	"errors"
	"math"
	"sort"
)

// InterpolationMethod defines the percentile interpolation method
type InterpolationMethod int

const (
	// Linear interpolation (default, numpy.percentile default)
	Linear InterpolationMethod = iota
	// Lower - take the lower bound value
	Lower
	// Higher - take the upper bound value
	Higher
	// Nearest - take the nearest value
	Nearest
	// Midpoint - take the midpoint between bounds
	Midpoint
	// Exclusive - Excel PERCENTILE.EXC method
	Exclusive
	// Inclusive - Excel PERCENTILE.INC method
	Inclusive
)

// Errors
var (
	ErrEmptyData         = errors.New("data slice cannot be empty")
	ErrInvalidPercentile = errors.New("percentile must be between 0 and 100")
	ErrInvalidValue      = errors.New("invalid value in data (NaN or Inf)")
	ErrInsufficientData  = errors.New("insufficient data points for this method")
)

// QuartileResult holds quartile calculation results
type QuartileResult struct {
	Q1  float64 // First quartile (25th percentile)
	Q2  float64 // Second quartile (median, 50th percentile)
	Q3  float64 // Third quartile (75th percentile)
	IQR float64 // Interquartile range (Q3 - Q1)
}

// BoxplotResult holds boxplot statistical results
type BoxplotResult struct {
	Min          float64   // Minimum value
	Q1           float64   // First quartile
	Median       float64   // Median (Q2)
	Q3           float64   // Third quartile
	Max          float64   // Maximum value
	IQR          float64   // Interquartile range
	LowerWhisker float64   // Lower whisker (non-outlier minimum)
	UpperWhisker float64   // Upper whisker (non-outlier maximum)
	LowerBound   float64   // Lower fence (Q1 - 1.5*IQR)
	UpperBound   float64   // Upper fence (Q3 + 1.5*IQR)
	Outliers     []float64 // Outlier values
}

// SummaryResult holds comprehensive percentile statistics
type SummaryResult struct {
	Count      int                  // Number of data points
	Min        float64              // Minimum value
	Max        float64              // Maximum value
	Sum        float64              // Sum of all values
	Mean       float64              // Arithmetic mean
	Variance   float64              // Population variance
	StdDev     float64              // Standard deviation
	Range      float64              // Range (Max - Min)
	Median     float64              // Median
	Quartiles  QuartileResult       // Quartile statistics
	Percentiles map[float64]float64 // Key percentiles (5, 10, 25, 50, 75, 90, 95)
}

// validateData validates and returns sorted data
func validateData(data []float64, sorted bool) ([]float64, error) {
	if len(data) == 0 {
		return nil, ErrEmptyData
	}

	// Check for invalid values
	for _, v := range data {
		if math.IsNaN(v) || math.IsInf(v, 0) {
			return nil, ErrInvalidValue
		}
	}

	// Sort if not already sorted
	if !sorted {
		sortedData := make([]float64, len(data))
		copy(sortedData, data)
		sort.Float64s(sortedData)
		return sortedData, nil
	}

	return data, nil
}

// validatePercentile validates percentile value
func validatePercentile(p float64) error {
	if p < 0 || p > 100 {
		return ErrInvalidPercentile
	}
	return nil
}

// Percentile calculates the p-th percentile of the data
func Percentile(data []float64, p float64, method InterpolationMethod, sorted bool) (float64, error) {
	if err := validatePercentile(p); err != nil {
		return 0, err
	}

	sortedData, err := validateData(data, sorted)
	if err != nil {
		return 0, err
	}

	n := len(sortedData)

	// Single element
	if n == 1 {
		return sortedData[0], nil
	}

	// Special cases
	if p == 0 {
		return sortedData[0], nil
	}
	if p == 100 {
		return sortedData[n-1], nil
	}

	switch method {
	case Linear:
		return linearPercentile(sortedData, p), nil
	case Lower:
		return lowerPercentile(sortedData, p), nil
	case Higher:
		return higherPercentile(sortedData, p), nil
	case Nearest:
		return nearestPercentile(sortedData, p), nil
	case Midpoint:
		return midpointPercentile(sortedData, p), nil
	case Exclusive:
		return exclusivePercentile(sortedData, p)
	case Inclusive:
		return inclusivePercentile(sortedData, p), nil
	default:
		return linearPercentile(sortedData, p), nil
	}
}

// linearPercentile uses linear interpolation (numpy default)
func linearPercentile(data []float64, p float64) float64 {
	n := len(data)
	rank := (p / 100) * float64(n-1)
	lowerIdx := int(math.Floor(rank))
	upperIdx := lowerIdx + 1

	if upperIdx >= n {
		return data[n-1]
	}

	fraction := rank - float64(lowerIdx)
	return data[lowerIdx] + fraction*(data[upperIdx]-data[lowerIdx])
}

// lowerPercentile takes the lower bound value
func lowerPercentile(data []float64, p float64) float64 {
	n := len(data)
	idx := int(math.Floor((p / 100) * float64(n-1)))
	return data[idx]
}

// higherPercentile takes the upper bound value
func higherPercentile(data []float64, p float64) float64 {
	n := len(data)
	idx := int(math.Ceil((p / 100) * float64(n-1)))
	if idx >= n {
		return data[n-1]
	}
	return data[idx]
}

// nearestPercentile takes the nearest value
func nearestPercentile(data []float64, p float64) float64 {
	n := len(data)
	idx := int(math.Round((p / 100) * float64(n-1)))
	if idx >= n {
		return data[n-1]
	}
	return data[idx]
}

// midpointPercentile takes the midpoint between bounds
func midpointPercentile(data []float64, p float64) float64 {
	n := len(data)
	rank := (p / 100) * float64(n-1)
	lowerIdx := int(math.Floor(rank))
	upperIdx := lowerIdx + 1
	if upperIdx >= n {
		return data[n-1]
	}
	return (data[lowerIdx] + data[upperIdx]) / 2
}

// exclusivePercentile uses Excel PERCENTILE.EXC method
func exclusivePercentile(data []float64, p float64) (float64, error) {
	n := len(data)
	if n < 4 {
		return 0, ErrInsufficientData
	}

	rank := (p / 100) * float64(n+1)

	// Check bounds for exclusive method
	if rank < 1 || rank > float64(n) {
		minP := 100.0 / float64(n+1)
		maxP := 100.0 * float64(n) / float64(n+1)
		return 0, errors.New("percentile out of bounds for exclusive method (must be between " +
			formatFloat(minP) + " and " + formatFloat(maxP))
	}

	idx := rank - 1
	lowerIdx := int(math.Floor(idx))
	upperIdx := lowerIdx + 1
	fraction := idx - float64(lowerIdx)

	return data[lowerIdx] + fraction*(data[upperIdx]-data[lowerIdx]), nil
}

// formatFloat formats a float for error messages
func formatFloat(v float64) string {
	return string([]byte{ /* placeholder */ })
}

// inclusivePercentile uses Excel PERCENTILE.INC method (same as linear)
func inclusivePercentile(data []float64, p float64) float64 {
	return linearPercentile(data, p)
}

// CalculateQuartiles calculates Q1, Q2 (median), Q3, and IQR
func CalculateQuartiles(data []float64, method InterpolationMethod, sorted bool) (QuartileResult, error) {
	sortedData, err := validateData(data, sorted)
	if err != nil {
		return QuartileResult{}, err
	}

	q1, _ := Percentile(sortedData, 25, method, true)
	q2, _ := Percentile(sortedData, 50, method, true)
	q3, _ := Percentile(sortedData, 75, method, true)

	return QuartileResult{
		Q1:  q1,
		Q2:  q2,
		Q3:  q3,
		IQR: q3 - q1,
	}, nil
}

// PercentileRank calculates the percentile rank of a value in the data
func PercentileRank(data []float64, value float64, sorted bool) (float64, error) {
	sortedData, err := validateData(data, sorted)
	if err != nil {
		return 0, err
	}

	n := len(sortedData)
	countBelow := 0
	countEqual := 0

	for _, v := range sortedData {
		if v < value {
			countBelow++
		} else if v == value {
			countEqual++
		}
	}

	if countEqual == 0 {
		// Value not in data, use linear interpolation
		for i := 0; i < n-1; i++ {
			if sortedData[i] < value && value < sortedData[i+1] {
				fraction := (value - sortedData[i]) / (sortedData[i+1] - sortedData[i])
				rank := (float64(countBelow) + fraction) / float64(n) * 100
				return math.Round(rank*100) / 100, nil
			}
		}
		// Out of range
		if value < sortedData[0] {
			return 0, nil
		}
		return 100, nil
	}

	// Use formula: (below + 0.5*equal) / total * 100
	rank := (float64(countBelow) + 0.5*float64(countEqual)) / float64(n) * 100
	return math.Round(rank*100) / 100, nil
}

// CalculateBoxplotStats calculates complete boxplot statistics
func CalculateBoxplotStats(data []float64, method InterpolationMethod, sorted bool, whiskerMultiplier float64) (BoxplotResult, error) {
	sortedData, err := validateData(data, sorted)
	if err != nil {
		return BoxplotResult{}, err
	}

	qs, _ := CalculateQuartiles(sortedData, method, true)

	// Calculate whisker bounds
	lowerBound := qs.Q1 - whiskerMultiplier*qs.IQR
	upperBound := qs.Q3 + whiskerMultiplier*qs.IQR

	// Find actual whisker endpoints
	lowerWhisker := sortedData[0]
	upperWhisker := sortedData[len(sortedData)-1]
	outliers := []float64{}

	for _, v := range sortedData {
		if v >= lowerBound && v <= upperBound {
			if v < lowerWhisker {
				lowerWhisker = v
			}
			if v > upperWhisker {
				upperWhisker = v
			}
		} else {
			outliers = append(outliers, v)
		}
	}

	return BoxplotResult{
		Min:          sortedData[0],
		Q1:           qs.Q1,
		Median:       qs.Q2,
		Q3:           qs.Q3,
		Max:          sortedData[len(sortedData)-1],
		IQR:          qs.IQR,
		LowerWhisker: lowerWhisker,
		UpperWhisker: upperWhisker,
		LowerBound:   lowerBound,
		UpperBound:   upperBound,
		Outliers:     outliers,
	}, nil
}

// CalculateDeciles calculates all deciles (D0 to D9)
func CalculateDeciles(data []float64, method InterpolationMethod, sorted bool) ([]float64, error) {
	sortedData, err := validateData(data, sorted)
	if err != nil {
		return nil, err
	}

	deciles := make([]float64, 10)
	for i := 0; i < 10; i++ {
		p, _ := Percentile(sortedData, float64(i*10), method, true)
		deciles[i] = p
	}
	return deciles, nil
}

// CalculatePercentiles calculates multiple percentiles at once
func CalculatePercentiles(data []float64, pList []float64, method InterpolationMethod, sorted bool) (map[float64]float64, error) {
	sortedData, err := validateData(data, sorted)
	if err != nil {
		return nil, err
	}

	for _, p := range pList {
		if err := validatePercentile(p); err != nil {
			return nil, err
		}
	}

	result := make(map[float64]float64)
	for _, p := range pList {
		val, _ := Percentile(sortedData, p, method, true)
		result[p] = val
	}
	return result, nil
}

// IsOutlier checks if a value is an outlier based on IQR method
func IsOutlier(value float64, data []float64, method InterpolationMethod, whiskerMultiplier float64) (bool, error) {
	stats, err := CalculateBoxplotStats(data, method, false, whiskerMultiplier)
	if err != nil {
		return false, err
	}
	return value < stats.LowerBound || value > stats.UpperBound, nil
}

// Winsorize replaces extreme values with percentile bounds
func Winsorize(data []float64, lowerPercentile, upperPercentile float64, method InterpolationMethod) ([]float64, error) {
	validatedData, err := validateData(data, false)
	if err != nil {
		return nil, err
	}

	lowerVal, _ := Percentile(validatedData, lowerPercentile, method, true)
	upperVal, _ := Percentile(validatedData, upperPercentile, method, true)

	result := make([]float64, len(validatedData))
	for i, v := range validatedData {
		if v < lowerVal {
			result[i] = lowerVal
		} else if v > upperVal {
			result[i] = upperVal
		} else {
			result[i] = v
		}
	}
	return result, nil
}

// NormalizeByPercentile normalizes data using percentile range
func NormalizeByPercentile(data []float64, lowerPercentile, upperPercentile float64, method InterpolationMethod) ([]float64, error) {
	validatedData, err := validateData(data, false)
	if err != nil {
		return nil, err
	}

	lowerVal, _ := Percentile(validatedData, lowerPercentile, method, true)
	upperVal, _ := Percentile(validatedData, upperPercentile, method, true)

	iqr := upperVal - lowerVal
	if iqr == 0 {
		// If IQR is 0, return zero-mean data
		mean := Mean(validatedData)
		result := make([]float64, len(validatedData))
		for i, v := range validatedData {
			result[i] = v - mean
		}
		return result, nil
	}

	result := make([]float64, len(validatedData))
	for i, v := range validatedData {
		result[i] = (v - lowerVal) / iqr
	}
	return result, nil
}

// Mean calculates arithmetic mean
func Mean(data []float64) float64 {
	if len(data) == 0 {
		return 0
	}
	sum := 0.0
	for _, v := range data {
		sum += v
	}
	return sum / float64(len(data))
}

// Variance calculates population variance
func Variance(data []float64) float64 {
	if len(data) == 0 {
		return 0
	}
	mean := Mean(data)
	sum := 0.0
	for _, v := range data {
		diff := v - mean
		sum += diff * diff
	}
	return sum / float64(len(data))
}

// StdDev calculates standard deviation
func StdDev(data []float64) float64 {
	return math.Sqrt(Variance(data))
}

// CalculateSummary generates comprehensive percentile statistics
func CalculateSummary(data []float64, method InterpolationMethod) (SummaryResult, error) {
	sortedData, err := validateData(data, false)
	if err != nil {
		return SummaryResult{}, err
	}

	n := len(sortedData)
	sum := 0.0
	for _, v := range sortedData {
		sum += v
	}
	mean := sum / float64(n)
	variance := Variance(sortedData)
	stdDev := StdDev(sortedData)

	qs, _ := CalculateQuartiles(sortedData, method, true)
	pList := []float64{5, 10, 25, 50, 75, 90, 95}
	ps, _ := CalculatePercentiles(sortedData, pList, method, true)

	return SummaryResult{
		Count:      n,
		Min:        sortedData[0],
		Max:        sortedData[n-1],
		Sum:        sum,
		Mean:       mean,
		Variance:   variance,
		StdDev:     stdDev,
		Range:      sortedData[n-1] - sortedData[0],
		Median:     ps[50],
		Quartiles:  qs,
		Percentiles: ps,
	}, nil
}

// Median calculates the median (50th percentile)
func Median(data []float64, method InterpolationMethod) (float64, error) {
	return Percentile(data, 50, method, false)
}

// MustPercentile calculates percentile, panics on error
func MustPercentile(data []float64, p float64, method InterpolationMethod) float64 {
	result, err := Percentile(data, p, method, false)
	if err != nil {
		panic(err)
	}
	return result
}

// MustQuartiles calculates quartiles, panics on error
func MustQuartiles(data []float64, method InterpolationMethod) QuartileResult {
	result, err := CalculateQuartiles(data, method, false)
	if err != nil {
		panic(err)
	}
	return result
}

// MustMedian calculates median, panics on error
func MustMedian(data []float64) float64 {
	result, err := Median(data, Linear)
	if err != nil {
		panic(err)
	}
	return result
}

// MustSummary generates summary, panics on error
func MustSummary(data []float64) SummaryResult {
	result, err := CalculateSummary(data, Linear)
	if err != nil {
		panic(err)
	}
	return result
}

// String returns the name of the interpolation method
func (m InterpolationMethod) String() string {
	switch m {
	case Linear:
		return "Linear"
	case Lower:
		return "Lower"
	case Higher:
		return "Higher"
	case Nearest:
		return "Nearest"
	case Midpoint:
		return "Midpoint"
	case Exclusive:
		return "Exclusive"
	case Inclusive:
		return "Inclusive"
	default:
		return "Unknown"
	}
}