// Package statistics_utils provides comprehensive statistical analysis functions
// without any external dependencies.
package statistics_utils

import (
	"errors"
	"math"
	"sort"
)

// Statistics holds comprehensive statistical measures for a dataset
type Statistics struct {
	Count         int     `json:"count"`
	Sum           float64 `json:"sum"`
	Mean          float64 `json:"mean"`
	Median        float64 `json:"median"`
	Mode          float64 `json:"mode"`
	Min           float64 `json:"min"`
	Max           float64 `json:"max"`
	Range         float64 `json:"range"`
	Variance      float64 `json:"variance"`
	StdDev        float64 `json:"std_dev"`
	PopVariance   float64 `json:"pop_variance"`
	PopStdDev     float64 `json:"pop_std_dev"`
	Skewness      float64 `json:"skewness"`
	Kurtosis      float64 `json:"kurtosis"`
	GeometricMean  float64 `json:"geometric_mean"`
	HarmonicMean   float64 `json:"harmonic_mean"`
	Quartile1      float64 `json:"quartile1"`
	Quartile3      float64 `json:"quartile3"`
	IQR            float64 `json:"iqr"`
	LowerFence     float64 `json:"lower_fence"`
	UpperFence     float64 `json:"upper_fence"`
	CoeffVar       float64 `json:"coeff_var"`
}

var (
	ErrEmptyDataset = errors.New("dataset cannot be empty")
	ErrNonPositive  = errors.New("all values must be positive for geometric/harmonic mean")
)

// Sum returns the sum of all values in the dataset
func Sum(data []float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	var sum float64
	for _, v := range data {
		sum += v
	}
	return sum, nil
}

// Mean calculates the arithmetic mean of the dataset
func Mean(data []float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	sum, _ := Sum(data)
	return sum / float64(len(data)), nil
}

// Median calculates the median (middle value) of the dataset
func Median(data []float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	
	sorted := make([]float64, len(data))
	copy(sorted, data)
	sort.Float64s(sorted)
	
	n := len(sorted)
	if n%2 == 1 {
		return sorted[n/2], nil
	}
	return (sorted[n/2-1] + sorted[n/2]) / 2, nil
}

// Mode finds the most frequent value in the dataset
// Returns the first mode if multiple values have the same frequency
func Mode(data []float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	
	frequency := make(map[float64]int)
	for _, v := range data {
		frequency[v]++
	}
	
	var mode float64
	maxFreq := 0
	for value, freq := range frequency {
		if freq > maxFreq {
			maxFreq = freq
			mode = value
		}
	}
	return mode, nil
}

// Modes finds all modes (values with maximum frequency)
func Modes(data []float64) ([]float64, error) {
	if len(data) == 0 {
		return nil, ErrEmptyDataset
	}
	
	frequency := make(map[float64]int)
	for _, v := range data {
		frequency[v]++
	}
	
	maxFreq := 0
	for _, freq := range frequency {
		if freq > maxFreq {
			maxFreq = freq
		}
	}
	
	var modes []float64
	for value, freq := range frequency {
		if freq == maxFreq {
			modes = append(modes, value)
		}
	}
	sort.Float64s(modes)
	return modes, nil
}

// Min finds the minimum value in the dataset
func Min(data []float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	
	minVal := data[0]
	for _, v := range data[1:] {
		if v < minVal {
			minVal = v
		}
	}
	return minVal, nil
}

// Max finds the maximum value in the dataset
func Max(data []float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	
	maxVal := data[0]
	for _, v := range data[1:] {
		if v > maxVal {
			maxVal = v
		}
	}
	return maxVal, nil
}

// Range calculates the range (max - min) of the dataset
func Range(data []float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	minVal, _ := Min(data)
	maxVal, _ := Max(data)
	return maxVal - minVal, nil
}

// Variance calculates the sample variance (with Bessel's correction)
func Variance(data []float64) (float64, error) {
	if len(data) < 2 {
		return 0, ErrEmptyDataset
	}
	
	mean, _ := Mean(data)
	var sumSquaredDiff float64
	for _, v := range data {
		diff := v - mean
		sumSquaredDiff += diff * diff
	}
	return sumSquaredDiff / float64(len(data)-1), nil
}

// PopVariance calculates the population variance
func PopVariance(data []float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	
	mean, _ := Mean(data)
	var sumSquaredDiff float64
	for _, v := range data {
		diff := v - mean
		sumSquaredDiff += diff * diff
	}
	return sumSquaredDiff / float64(len(data)), nil
}

// StdDev calculates the sample standard deviation
func StdDev(data []float64) (float64, error) {
	variance, err := Variance(data)
	if err != nil {
		return 0, err
	}
	return math.Sqrt(variance), nil
}

// PopStdDev calculates the population standard deviation
func PopStdDev(data []float64) (float64, error) {
	variance, err := PopVariance(data)
	if err != nil {
		return 0, err
	}
	return math.Sqrt(variance), nil
}

// Percentile calculates the value at a given percentile (0-100)
// Uses linear interpolation between closest ranks
func Percentile(data []float64, percentile float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	if percentile < 0 || percentile > 100 {
		return 0, errors.New("percentile must be between 0 and 100")
	}
	
	sorted := make([]float64, len(data))
	copy(sorted, data)
	sort.Float64s(sorted)
	
	if percentile == 100 {
		return sorted[len(sorted)-1], nil
	}
	if percentile == 0 {
		return sorted[0], nil
	}
	
	n := len(sorted)
	rank := (percentile / 100) * float64(n-1)
	lowerIndex := int(rank)
	upperIndex := lowerIndex + 1
	
	if upperIndex >= n {
		return sorted[n-1], nil
	}
	
	fraction := rank - float64(lowerIndex)
	return sorted[lowerIndex] + fraction*(sorted[upperIndex]-sorted[lowerIndex]), nil
}

// Quartiles calculates Q1 (25th percentile), Q2 (median), and Q3 (75th percentile)
func Quartiles(data []float64) (q1, q2, q3 float64, err error) {
	if len(data) == 0 {
		return 0, 0, 0, ErrEmptyDataset
	}
	
	q1, err = Percentile(data, 25)
	if err != nil {
		return 0, 0, 0, err
	}
	q2, err = Percentile(data, 50)
	if err != nil {
		return 0, 0, 0, err
	}
	q3, err = Percentile(data, 75)
	if err != nil {
		return 0, 0, 0, err
	}
	return q1, q2, q3, nil
}

// IQR calculates the interquartile range (Q3 - Q1)
func IQR(data []float64) (float64, error) {
	q1, _, q3, err := Quartiles(data)
	if err != nil {
		return 0, err
	}
	return q3 - q1, nil
}

// Outliers returns values that fall outside the fences (1.5 * IQR)
func Outliers(data []float64) ([]float64, []float64, error) {
	if len(data) == 0 {
		return nil, nil, ErrEmptyDataset
	}
	
	q1, _, q3, err := Quartiles(data)
	if err != nil {
		return nil, nil, err
	}
	
	iqr := q3 - q1
	lowerFence := q1 - 1.5*iqr
	upperFence := q3 + 1.5*iqr
	
	var lowerOutliers, upperOutliers []float64
	for _, v := range data {
		if v < lowerFence {
			lowerOutliers = append(lowerOutliers, v)
		} else if v > upperFence {
			upperOutliers = append(upperOutliers, v)
		}
	}
	
	return lowerOutliers, upperOutliers, nil
}

// GeometricMean calculates the geometric mean (nth root of product)
func GeometricMean(data []float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	
	var product float64 = 1
	for _, v := range data {
		if v <= 0 {
			return 0, ErrNonPositive
		}
		product *= v
	}
	return math.Pow(product, 1/float64(len(data))), nil
}

// HarmonicMean calculates the harmonic mean (n / sum of reciprocals)
func HarmonicMean(data []float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	
	var sumReciprocal float64
	for _, v := range data {
		if v <= 0 {
			return 0, ErrNonPositive
		}
		sumReciprocal += 1 / v
	}
	return float64(len(data)) / sumReciprocal, nil
}

// Skewness measures the asymmetry of the distribution
// Negative: left-skewed, Positive: right-skewed, Zero: symmetric
func Skewness(data []float64) (float64, error) {
	if len(data) < 3 {
		return 0, ErrEmptyDataset
	}
	
	n := float64(len(data))
	mean, _ := Mean(data)
	stdDev, err := StdDev(data)
	if err != nil {
		return 0, err
	}
	if stdDev == 0 {
		return 0, nil
	}
	
	var sumCubed float64
	for _, v := range data {
		deviation := (v - mean) / stdDev
		sumCubed += deviation * deviation * deviation
	}
	
	return (sumCubed / n) * (n / (n - 1)) * (n / (n - 2)), nil
}

// Kurtosis measures the "tailedness" of the distribution
// Normal distribution has kurtosis of 3 (excess kurtosis of 0)
func Kurtosis(data []float64) (float64, error) {
	if len(data) < 4 {
		return 0, ErrEmptyDataset
	}
	
	n := float64(len(data))
	mean, _ := Mean(data)
	stdDev, err := StdDev(data)
	if err != nil {
		return 0, err
	}
	if stdDev == 0 {
		return 0, nil
	}
	
	var sumFourth float64
	for _, v := range data {
		deviation := (v - mean) / stdDev
		sumFourth += deviation * deviation * deviation * deviation
	}
	
	kurtosis := (sumFourth / n) * (n + 1) / (n - 1) / (n - 2) / (n - 3)
	excessKurtosis := kurtosis - 3*(n-1)*(n-1)/(n-2)/(n-3)
	
	return excessKurtosis, nil
}

// CoeffVar calculates the coefficient of variation (stdDev / mean * 100)
func CoeffVar(data []float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	
	mean, _ := Mean(data)
	if mean == 0 {
		return 0, nil
	}
	
	stdDev, err := StdDev(data)
	if err != nil {
		return 0, err
	}
	
	return (stdDev / mean) * 100, nil
}

// Covariance calculates the covariance between two datasets
func Covariance(x, y []float64) (float64, error) {
	if len(x) != len(y) {
		return 0, errors.New("datasets must have equal length")
	}
	if len(x) < 2 {
		return 0, ErrEmptyDataset
	}
	
	n := float64(len(x))
	meanX, _ := Mean(x)
	meanY, _ := Mean(y)
	
	var sumProduct float64
	for i := range x {
		sumProduct += (x[i] - meanX) * (y[i] - meanY)
	}
	
	return sumProduct / (n - 1), nil
}

// Correlation calculates the Pearson correlation coefficient (-1 to 1)
func Correlation(x, y []float64) (float64, error) {
	if len(x) != len(y) {
		return 0, errors.New("datasets must have equal length")
	}
	if len(x) < 2 {
		return 0, ErrEmptyDataset
	}
	
	cov, err := Covariance(x, y)
	if err != nil {
		return 0, err
	}
	
	stdDevX, err := StdDev(x)
	if err != nil {
		return 0, err
	}
	stdDevY, err := StdDev(y)
	if err != nil {
		return 0, err
	}
	
	if stdDevX == 0 || stdDevY == 0 {
		return 0, nil
	}
	
	return cov / (stdDevX * stdDevY), nil
}

// ZScore normalizes a value to z-score (number of standard deviations from mean)
func ZScore(value, mean, stdDev float64) float64 {
	if stdDev == 0 {
		return 0
	}
	return (value - mean) / stdDev
}

// ZScores returns z-scores for all values in the dataset
func ZScores(data []float64) ([]float64, error) {
	if len(data) < 2 {
		return nil, ErrEmptyDataset
	}
	
	mean, _ := Mean(data)
	stdDev, err := StdDev(data)
	if err != nil {
		return nil, err
	}
	
	zScores := make([]float64, len(data))
	for i, v := range data {
		zScores[i] = ZScore(v, mean, stdDev)
	}
	return zScores, nil
}

// Normalize normalizes the dataset to range [0, 1]
func Normalize(data []float64) ([]float64, error) {
	if len(data) == 0 {
		return nil, ErrEmptyDataset
	}
	
	minVal, _ := Min(data)
	maxVal, _ := Max(data)
	rangeVal := maxVal - minVal
	
	if rangeVal == 0 {
		// All values are the same
		normalized := make([]float64, len(data))
		return normalized, nil
	}
	
	normalized := make([]float64, len(data))
	for i, v := range data {
		normalized[i] = (v - minVal) / rangeVal
	}
	return normalized, nil
}

// Standardize standardizes the dataset (z-score normalization)
func Standardize(data []float64) ([]float64, error) {
	return ZScores(data)
}

// Describe calculates comprehensive statistics for the dataset
func Describe(data []float64) (*Statistics, error) {
	if len(data) == 0 {
		return nil, ErrEmptyDataset
	}
	
	count := len(data)
	sum, _ := Sum(data)
	mean, _ := Mean(data)
	median, _ := Median(data)
	mode, _ := Mode(data)
	minVal, _ := Min(data)
	maxVal, _ := Max(data)
	rangeVal, _ := Range(data)
	
	var variance, stdDev float64
	if count > 1 {
		variance, _ = Variance(data)
		stdDev, _ = StdDev(data)
	}
	
	popVariance, _ := PopVariance(data)
	popStdDev, _ := PopStdDev(data)
	
	q1, _, q3, _ := Quartiles(data)
	iqr, _ := IQR(data)
	lowerFence := q1 - 1.5*iqr
	upperFence := q3 + 1.5*iqr
	
	var skewness, kurtosis float64
	if count > 2 {
		skewness, _ = Skewness(data)
	}
	if count > 3 {
		kurtosis, _ = Kurtosis(data)
	}
	
	var geometricMean, harmonicMean float64
	allPositive := true
	for _, v := range data {
		if v <= 0 {
			allPositive = false
			break
		}
	}
	if allPositive {
		geometricMean, _ = GeometricMean(data)
		harmonicMean, _ = HarmonicMean(data)
	}
	
	coeffVar, _ := CoeffVar(data)
	
	return &Statistics{
		Count:          count,
		Sum:            sum,
		Mean:           mean,
		Median:         median,
		Mode:           mode,
		Min:            minVal,
		Max:            maxVal,
		Range:          rangeVal,
		Variance:       variance,
		StdDev:         stdDev,
		PopVariance:    popVariance,
		PopStdDev:      popStdDev,
		Skewness:       skewness,
		Kurtosis:       kurtosis,
		GeometricMean:  geometricMean,
		HarmonicMean:   harmonicMean,
		Quartile1:      q1,
		Quartile3:      q3,
		IQR:            iqr,
		LowerFence:     lowerFence,
		UpperFence:     upperFence,
		CoeffVar:       coeffVar,
	}, nil
}

// MovingAverage calculates the simple moving average with a given window size
func MovingAverage(data []float64, window int) ([]float64, error) {
	if len(data) == 0 {
		return nil, ErrEmptyDataset
	}
	if window < 1 {
		return nil, errors.New("window size must be at least 1")
	}
	if window > len(data) {
		return nil, errors.New("window size cannot exceed data length")
	}
	
	result := make([]float64, len(data)-window+1)
	for i := 0; i <= len(data)-window; i++ {
		var sum float64
		for j := i; j < i+window; j++ {
			sum += data[j]
		}
		result[i] = sum / float64(window)
	}
	return result, nil
}

// ExponentialMovingAverage calculates the EMA with a given smoothing factor alpha
func ExponentialMovingAverage(data []float64, alpha float64) ([]float64, error) {
	if len(data) == 0 {
		return nil, ErrEmptyDataset
	}
	if alpha < 0 || alpha > 1 {
		return nil, errors.New("alpha must be between 0 and 1")
	}
	
	ema := make([]float64, len(data))
	ema[0] = data[0]
	
	for i := 1; i < len(data); i++ {
		ema[i] = alpha*data[i] + (1-alpha)*ema[i-1]
	}
	return ema, nil
}

// WeightedMean calculates the weighted arithmetic mean
func WeightedMean(data, weights []float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	if len(data) != len(weights) {
		return 0, errors.New("data and weights must have equal length")
	}
	
	var sumWeightedValues, sumWeights float64
	for i := range data {
		if weights[i] < 0 {
			return 0, errors.New("weights cannot be negative")
		}
		sumWeightedValues += data[i] * weights[i]
		sumWeights += weights[i]
	}
	
	if sumWeights == 0 {
		return 0, errors.New("sum of weights cannot be zero")
	}
	
	return sumWeightedValues / sumWeights, nil
}

// MedianAbsoluteDeviation calculates MAD (median of absolute deviations from median)
func MedianAbsoluteDeviation(data []float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	
	median, _ := Median(data)
	deviations := make([]float64, len(data))
	for i, v := range data {
		deviations[i] = math.Abs(v - median)
	}
	
	return Median(deviations)
}

// TrimmedMean calculates the mean after removing a percentage of extreme values
func TrimmedMean(data []float64, trimPercent float64) (float64, error) {
	if len(data) == 0 {
		return 0, ErrEmptyDataset
	}
	if trimPercent < 0 || trimPercent >= 50 {
		return 0, errors.New("trim percentage must be between 0 and 50")
	}
	
	sorted := make([]float64, len(data))
	copy(sorted, data)
	sort.Float64s(sorted)
	
	trimCount := int(float64(len(sorted)) * trimPercent / 100)
	if trimCount == 0 {
		return Mean(sorted)
	}
	
	trimmed := sorted[trimCount : len(sorted)-trimCount]
	return Mean(trimmed)
}