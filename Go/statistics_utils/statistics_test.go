package statistics_utils

import (
	"math"
	"testing"
)

const epsilon = 1e-10

func almostEqual(a, b float64) bool {
	return math.Abs(a-b) < epsilon
}

func TestSum(t *testing.T) {
	tests := []struct {
		name     string
		data     []float64
		expected float64
		hasError bool
	}{
		{"simple sum", []float64{1, 2, 3, 4, 5}, 15, false},
		{"negative values", []float64{-1, -2, -3}, -6, false},
		{"mixed values", []float64{-1, 2, -3, 4}, 2, false},
		{"single value", []float64{5}, 5, false},
		{"empty dataset", []float64{}, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Sum(tt.data)
			if tt.hasError {
				if err == nil {
					t.Errorf("expected error but got none")
				}
			} else {
				if err != nil {
					t.Errorf("unexpected error: %v", err)
				}
				if !almostEqual(result, tt.expected) {
					t.Errorf("Sum() = %v, want %v", result, tt.expected)
				}
			}
		})
	}
}

func TestMean(t *testing.T) {
	tests := []struct {
		name     string
		data     []float64
		expected float64
		hasError bool
	}{
		{"simple mean", []float64{1, 2, 3, 4, 5}, 3, false},
		{"uneven mean", []float64{1, 2, 3, 4}, 2.5, false},
		{"single value", []float64{7}, 7, false},
		{"empty dataset", []float64{}, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Mean(tt.data)
			if tt.hasError {
				if err == nil {
					t.Errorf("expected error but got none")
				}
			} else {
				if err != nil {
					t.Errorf("unexpected error: %v", err)
				}
				if !almostEqual(result, tt.expected) {
					t.Errorf("Mean() = %v, want %v", result, tt.expected)
				}
			}
		})
	}
}

func TestMedian(t *testing.T) {
	tests := []struct {
		name     string
		data     []float64
		expected float64
		hasError bool
	}{
		{"odd count", []float64{1, 3, 5}, 3, false},
		{"even count", []float64{1, 2, 3, 4}, 2.5, false},
		{"unsorted odd", []float64{5, 1, 3}, 3, false},
		{"unsorted even", []float64{4, 1, 3, 2}, 2.5, false},
		{"single value", []float64{5}, 5, false},
		{"empty dataset", []float64{}, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Median(tt.data)
			if tt.hasError {
				if err == nil {
					t.Errorf("expected error but got none")
				}
			} else {
				if err != nil {
					t.Errorf("unexpected error: %v", err)
				}
				if !almostEqual(result, tt.expected) {
					t.Errorf("Median() = %v, want %v", result, tt.expected)
				}
			}
		})
	}
}

func TestMode(t *testing.T) {
	tests := []struct {
		name     string
		data     []float64
		expected float64
		hasError bool
	}{
		{"clear mode", []float64{1, 2, 2, 3}, 2, false},
		{"single value", []float64{5}, 5, false},
		{"empty dataset", []float64{}, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Mode(tt.data)
			if tt.hasError {
				if err == nil {
					t.Errorf("expected error but got none")
				}
			} else {
				if err != nil {
					t.Errorf("unexpected error: %v", err)
				}
				if !almostEqual(result, tt.expected) {
					t.Errorf("Mode() = %v, want %v", result, tt.expected)
				}
			}
		})
	}
	
	// Test that Mode returns one of the values with maximum frequency
	t.Run("multiple modes", func(t *testing.T) {
		data := []float64{1, 1, 2, 2, 3} // Both 1 and 2 have frequency 2
		result, err := Mode(data)
		if err != nil {
			t.Errorf("unexpected error: %v", err)
		}
		// Result should be either 1 or 2 (both have max frequency)
		if result != 1 && result != 2 {
			t.Errorf("Mode() = %v, want either 1 or 2", result)
		}
	})
}

func TestModes(t *testing.T) {
	modes, err := Modes([]float64{1, 1, 2, 2, 3})
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if len(modes) != 2 {
		t.Errorf("expected 2 modes, got %d", len(modes))
	}
}

func TestMinMax(t *testing.T) {
	data := []float64{3, 1, 4, 1, 5, 9, 2, 6}
	
	minVal, err := Min(data)
	if err != nil || !almostEqual(minVal, 1) {
		t.Errorf("Min() = %v, want 1, err: %v", minVal, err)
	}
	
	maxVal, err := Max(data)
	if err != nil || !almostEqual(maxVal, 9) {
		t.Errorf("Max() = %v, want 9, err: %v", maxVal, err)
	}
	
	rangeVal, err := Range(data)
	if err != nil || !almostEqual(rangeVal, 8) {
		t.Errorf("Range() = %v, want 8, err: %v", rangeVal, err)
	}
	
	_, err = Min([]float64{})
	if err == nil {
		t.Error("expected error for empty dataset")
	}
}

func TestVarianceAndStdDev(t *testing.T) {
	// Test data: {2, 4, 4, 4, 5, 5, 7, 9}
	// Known: sample variance = 4.5714..., population variance = 4
	data := []float64{2, 4, 4, 4, 5, 5, 7, 9}
	
	popVar, err := PopVariance(data)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if !almostEqual(popVar, 4) {
		t.Errorf("PopVariance() = %v, want 4", popVar)
	}
	
	popStdDev, err := PopStdDev(data)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if !almostEqual(popStdDev, 2) {
		t.Errorf("PopStdDev() = %v, want 2", popStdDev)
	}
	
	// Sample variance should be slightly larger (Bessel's correction)
	sampleVar, err := Variance(data)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	expectedSampleVar := 4.0 * 8.0 / 7.0
	if !almostEqual(sampleVar, expectedSampleVar) {
		t.Errorf("Variance() = %v, want %v", sampleVar, expectedSampleVar)
	}
	
	_, err = Variance([]float64{1})
	if err == nil {
		t.Error("expected error for single value in Variance")
	}
}

func TestPercentile(t *testing.T) {
	data := []float64{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	
	tests := []struct {
		percentile float64
		expected   float64
	}{
		{0, 1},
		{25, 3.25},
		{50, 5.5},
		{75, 7.75},
		{100, 10},
	}

	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			result, err := Percentile(data, tt.percentile)
			if err != nil {
				t.Errorf("unexpected error: %v", err)
			}
			if !almostEqual(result, tt.expected) {
				t.Errorf("Percentile(%v) = %v, want %v", tt.percentile, result, tt.expected)
			}
		})
	}
	
	_, err := Percentile(data, -1)
	if err == nil {
		t.Error("expected error for negative percentile")
	}
	
	_, err = Percentile(data, 101)
	if err == nil {
		t.Error("expected error for percentile > 100")
	}
}

func TestQuartiles(t *testing.T) {
	data := []float64{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	
	q1, q2, q3, err := Quartiles(data)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	
	if !almostEqual(q2, 5.5) {
		t.Errorf("Q2 (median) = %v, want 5.5", q2)
	}
	
	iqr, err := IQR(data)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	
	expectedIQR := q3 - q1
	if !almostEqual(iqr, expectedIQR) {
		t.Errorf("IQR = %v, want %v", iqr, expectedIQR)
	}
}

func TestGeometricMean(t *testing.T) {
	// Geometric mean of {2, 8} = sqrt(16) = 4
	data := []float64{2, 8}
	result, err := GeometricMean(data)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if !almostEqual(result, 4) {
		t.Errorf("GeometricMean() = %v, want 4", result)
	}
	
	// Test with non-positive values
	_, err = GeometricMean([]float64{-1, 2, 3})
	if err == nil {
		t.Error("expected error for negative values")
	}
	
	_, err = GeometricMean([]float64{0, 1, 2})
	if err == nil {
		t.Error("expected error for zero values")
	}
}

func TestHarmonicMean(t *testing.T) {
	// Harmonic mean of {1, 4} = 2 / (1 + 0.25) = 1.6
	data := []float64{1, 4}
	result, err := HarmonicMean(data)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if !almostEqual(result, 1.6) {
		t.Errorf("HarmonicMean() = %v, want 1.6", result)
	}
	
	// Test with non-positive values
	_, err = HarmonicMean([]float64{-1, 2, 3})
	if err == nil {
		t.Error("expected error for negative values")
	}
}

func TestSkewness(t *testing.T) {
	// Symmetric distribution should have skewness near 0
	data := []float64{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	result, err := Skewness(data)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if math.Abs(result) > 0.1 {
		t.Errorf("Skewness for symmetric data should be near 0, got %v", result)
	}
	
	_, err = Skewness([]float64{1})
	if err == nil {
		t.Error("expected error for insufficient data")
	}
}

func TestCorrelation(t *testing.T) {
	// Perfect positive correlation
	x := []float64{1, 2, 3, 4, 5}
	y := []float64{2, 4, 6, 8, 10}
	
	corr, err := Correlation(x, y)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if !almostEqual(corr, 1) {
		t.Errorf("Correlation() = %v, want 1", corr)
	}
	
	// Perfect negative correlation
	y2 := []float64{10, 8, 6, 4, 2}
	corr, err = Correlation(x, y2)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if !almostEqual(corr, -1) {
		t.Errorf("Correlation() = %v, want -1", corr)
	}
	
	// Mismatched lengths
	_, err = Correlation(x, []float64{1, 2})
	if err == nil {
		t.Error("expected error for mismatched lengths")
	}
}

func TestZScore(t *testing.T) {
	// Z-score of 80 in distribution with mean 70, std dev 10 = 1
	result := ZScore(80, 70, 10)
	if !almostEqual(result, 1) {
		t.Errorf("ZScore() = %v, want 1", result)
	}
	
	// Zero std dev should return 0
	result = ZScore(80, 70, 0)
	if !almostEqual(result, 0) {
		t.Errorf("ZScore() with zero std dev = %v, want 0", result)
	}
}

func TestZScores(t *testing.T) {
	data := []float64{1, 2, 3, 4, 5}
	zScores, err := ZScores(data)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	
	// Mean of z-scores should be 0
	var sum float64
	for _, z := range zScores {
		sum += z
	}
	mean := sum / float64(len(zScores))
	if math.Abs(mean) > epsilon {
		t.Errorf("Mean of z-scores = %v, want 0", mean)
	}
}

func TestNormalize(t *testing.T) {
	data := []float64{0, 5, 10}
	normalized, err := Normalize(data)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	
	expected := []float64{0, 0.5, 1}
	for i, v := range normalized {
		if !almostEqual(v, expected[i]) {
			t.Errorf("Normalize()[%d] = %v, want %v", i, v, expected[i])
		}
	}
}

func TestDescribe(t *testing.T) {
	data := []float64{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	stats, err := Describe(data)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	
	if stats.Count != 10 {
		t.Errorf("Count = %d, want 10", stats.Count)
	}
	if !almostEqual(stats.Sum, 55) {
		t.Errorf("Sum = %v, want 55", stats.Sum)
	}
	if !almostEqual(stats.Mean, 5.5) {
		t.Errorf("Mean = %v, want 5.5", stats.Mean)
	}
	if !almostEqual(stats.Median, 5.5) {
		t.Errorf("Median = %v, want 5.5", stats.Median)
	}
	if !almostEqual(stats.Min, 1) {
		t.Errorf("Min = %v, want 1", stats.Min)
	}
	if !almostEqual(stats.Max, 10) {
		t.Errorf("Max = %v, want 10", stats.Max)
	}
	if !almostEqual(stats.Range, 9) {
		t.Errorf("Range = %v, want 9", stats.Range)
	}
	
	_, err = Describe([]float64{})
	if err == nil {
		t.Error("expected error for empty dataset")
	}
}

func TestMovingAverage(t *testing.T) {
	data := []float64{1, 2, 3, 4, 5}
	
	ma, err := MovingAverage(data, 3)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	
	expected := []float64{2, 3, 4} // (1+2+3)/3, (2+3+4)/3, (3+4+5)/3
	for i, v := range ma {
		if !almostEqual(v, expected[i]) {
			t.Errorf("MovingAverage()[%d] = %v, want %v", i, v, expected[i])
		}
	}
	
	_, err = MovingAverage(data, 0)
	if err == nil {
		t.Error("expected error for window size 0")
	}
	
	_, err = MovingAverage(data, 10)
	if err == nil {
		t.Error("expected error for window size > data length")
	}
}

func TestExponentialMovingAverage(t *testing.T) {
	data := []float64{1, 2, 3, 4, 5}
	
	ema, err := ExponentialMovingAverage(data, 0.5)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	
	if len(ema) != len(data) {
		t.Errorf("EMA length = %d, want %d", len(ema), len(data))
	}
	
	// EMA[0] should equal data[0]
	if !almostEqual(ema[0], data[0]) {
		t.Errorf("EMA[0] = %v, want %v", ema[0], data[0])
	}
	
	_, err = ExponentialMovingAverage(data, -0.1)
	if err == nil {
		t.Error("expected error for alpha < 0")
	}
	
	_, err = ExponentialMovingAverage(data, 1.1)
	if err == nil {
		t.Error("expected error for alpha > 1")
	}
}

func TestWeightedMean(t *testing.T) {
	data := []float64{1, 2, 3, 4, 5}
	weights := []float64{1, 1, 1, 1, 1}
	
	result, err := WeightedMean(data, weights)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if !almostEqual(result, 3) {
		t.Errorf("WeightedMean with equal weights = %v, want 3", result)
	}
	
	// Higher weight on higher values
	weights2 := []float64{1, 1, 1, 5, 5}
	result, err = WeightedMean(data, weights2)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if result <= 3 {
		t.Errorf("WeightedMean should be > 3 with higher weights on larger values, got %v", result)
	}
	
	_, err = WeightedMean(data, []float64{1, 2})
	if err == nil {
		t.Error("expected error for mismatched lengths")
	}
	
	_, err = WeightedMean(data, []float64{-1, 1, 1, 1, 1})
	if err == nil {
		t.Error("expected error for negative weights")
	}
}

func TestMedianAbsoluteDeviation(t *testing.T) {
	// MAD of {1, 2, 3, 4, 5} = median(|x - 3|) = median({2, 1, 0, 1, 2}) = 1
	data := []float64{1, 2, 3, 4, 5}
	result, err := MedianAbsoluteDeviation(data)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if !almostEqual(result, 1) {
		t.Errorf("MAD() = %v, want 1", result)
	}
}

func TestTrimmedMean(t *testing.T) {
	// Trim 20% from each end of {1, 2, 3, 4, 5} -> {2, 3, 4} -> mean = 3
	data := []float64{1, 2, 3, 4, 5}
	result, err := TrimmedMean(data, 20)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	// Note: 20% of 5 = 1, so trim 1 from each end
	if !almostEqual(result, 3) {
		t.Errorf("TrimmedMean() = %v, want 3", result)
	}
	
	_, err = TrimmedMean(data, -1)
	if err == nil {
		t.Error("expected error for negative trim percentage")
	}
	
	_, err = TrimmedMean(data, 50)
	if err == nil {
		t.Error("expected error for trim percentage >= 50")
	}
}

func TestOutliers(t *testing.T) {
	// Data with clear outliers: {1, 100, 100, 100, 100, 100, 100}
	data := []float64{1, 100, 100, 100, 100, 100, 100}
	lower, upper, err := Outliers(data)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	
	if len(lower) != 1 || !almostEqual(lower[0], 1) {
		t.Errorf("Expected 1 lower outlier (1), got %v", lower)
	}
	
	if len(upper) != 0 {
		t.Errorf("Expected 0 upper outliers, got %v", upper)
	}
}

func TestCovariance(t *testing.T) {
	x := []float64{1, 2, 3, 4, 5}
	y := []float64{2, 4, 6, 8, 10} // Perfect positive correlation
	
	cov, err := Covariance(x, y)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if cov <= 0 {
		t.Errorf("Covariance should be positive for positively correlated data, got %v", cov)
	}
	
	_, err = Covariance(x, []float64{1, 2})
	if err == nil {
		t.Error("expected error for mismatched lengths")
	}
}

func TestCoeffVar(t *testing.T) {
	// CV = (stdDev / mean) * 100
	// For {1, 2, 3, 4, 5}: mean = 3, stdDev = sqrt(2.5)
	data := []float64{1, 2, 3, 4, 5}
	cv, err := CoeffVar(data)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	
	// stdDev = sqrt(10/4) = sqrt(2.5) ≈ 1.5811
	// CV = 1.5811 / 3 * 100 ≈ 52.7
	if cv <= 0 {
		t.Errorf("Coefficient of variation should be positive, got %v", cv)
	}
}