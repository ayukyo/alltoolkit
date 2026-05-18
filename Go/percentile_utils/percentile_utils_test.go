package percentile_utils

import (
	"math"
	"testing"
)

// Test data
var testData = []float64{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
var testDataWithOutlier = []float64{1, 2, 3, 4, 5, 6, 7, 8, 9, 100}

func TestPercentile(t *testing.T) {
	tests := []struct {
		name     string
		data     []float64
		p        float64
		method   InterpolationMethod
		expected float64
	}{
		{"P50_Linear", testData, 50, Linear, 5.5},
		{"P25_Linear", testData, 25, Linear, 3.25},
		{"P75_Linear", testData, 75, Linear, 7.75},
		{"P0", testData, 0, Linear, 1},
		{"P100", testData, 100, Linear, 10},
		{"P50_Nearest", testData, 50, Nearest, 6},
		{"P50_Lower", testData, 50, Lower, 5},
		{"P50_Higher", testData, 50, Higher, 6},
		{"SingleElement", []float64{42}, 50, Linear, 42},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Percentile(tt.data, tt.p, tt.method, false)
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if math.Abs(result-tt.expected) > 0.01 {
				t.Errorf("expected %.2f, got %.2f", tt.expected, result)
			}
		})
	}
}

func TestPercentileErrors(t *testing.T) {
	_, err := Percentile(nil, 50, Linear, false)
	if err != ErrEmptyData {
		t.Errorf("expected ErrEmptyData, got %v", err)
	}

	_, err = Percentile(testData, 150, Linear, false)
	if err != ErrInvalidPercentile {
		t.Errorf("expected ErrInvalidPercentile, got %v", err)
	}

	_, err = Percentile(testData, -10, Linear, false)
	if err != ErrInvalidPercentile {
		t.Errorf("expected ErrInvalidPercentile, got %v", err)
	}

	_, err = Percentile([]float64{1, math.NaN()}, 50, Linear, false)
	if err != ErrInvalidValue {
		t.Errorf("expected ErrInvalidValue, got %v", err)
	}
}

func TestQuartiles(t *testing.T) {
	qs, err := CalculateQuartiles(testData, Linear, false)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if math.Abs(qs.Q1-3.25) > 0.01 {
		t.Errorf("Q1 expected 3.25, got %.2f", qs.Q1)
	}
	if math.Abs(qs.Q2-5.5) > 0.01 {
		t.Errorf("Q2 expected 5.5, got %.2f", qs.Q2)
	}
	if math.Abs(qs.Q3-7.75) > 0.01 {
		t.Errorf("Q3 expected 7.75, got %.2f", qs.Q3)
	}
	if math.Abs(qs.IQR-4.5) > 0.01 {
		t.Errorf("IQR expected 4.5, got %.2f", qs.IQR)
	}
}

func TestPercentileRank(t *testing.T) {
	tests := []struct {
		name     string
		data     []float64
		value    float64
		expected float64
	}{
		{"ExactValue", testData, 5, 45},
		{"Interpolated", testData, 5.5, 55},
		{"BelowMin", testData, 0, 0},
		{"AboveMax", testData, 100, 100},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := PercentileRank(tt.data, tt.value, false)
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if math.Abs(result-tt.expected) > 1 {
				t.Errorf("expected %.1f, got %.2f", tt.expected, result)
			}
		})
	}
}

func TestBoxplotStats(t *testing.T) {
	stats, err := CalculateBoxplotStats(testDataWithOutlier, Linear, false, 1.5)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if math.Abs(stats.Min-1) > 0.01 {
		t.Errorf("Min expected 1, got %.2f", stats.Min)
	}
	if math.Abs(stats.Max-100) > 0.01 {
		t.Errorf("Max expected 100, got %.2f", stats.Max)
	}
	if len(stats.Outliers) != 1 {
		t.Errorf("expected 1 outlier, got %d", len(stats.Outliers))
	}
	if len(stats.Outliers) > 0 && math.Abs(stats.Outliers[0]-100) > 0.01 {
		t.Errorf("outlier expected 100, got %.2f", stats.Outliers[0])
	}
}

func TestBoxplotStatsNoOutliers(t *testing.T) {
	stats, err := CalculateBoxplotStats(testData, Linear, false, 1.5)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(stats.Outliers) != 0 {
		t.Errorf("expected 0 outliers, got %d", len(stats.Outliers))
	}
}

func TestDeciles(t *testing.T) {
	deciles, err := CalculateDeciles(testData, Linear, false)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(deciles) != 10 {
		t.Errorf("expected 10 deciles, got %d", len(deciles))
	}

	// Check D0 and D9 (D9 is P90, not P100)
	if math.Abs(deciles[0]-1) > 0.01 {
		t.Errorf("D0 expected 1, got %.2f", deciles[0])
	}
	// D9 = P90 = 9.1 for data [1-10]
	if math.Abs(deciles[9]-9.1) > 0.1 {
		t.Errorf("D9 expected 9.1, got %.2f", deciles[9])
	}
}

func TestPercentiles(t *testing.T) {
	pList := []float64{10, 25, 50, 75, 90}
	ps, err := CalculatePercentiles(testData, pList, Linear, false)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(ps) != len(pList) {
		t.Errorf("expected %d percentiles, got %d", len(pList), len(ps))
	}

	// Check P50
	if math.Abs(ps[50]-5.5) > 0.01 {
		t.Errorf("P50 expected 5.5, got %.2f", ps[50])
	}
}

func TestIsOutlier(t *testing.T) {
	isOutlier, err := IsOutlier(100, testData, Linear, 1.5)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if !isOutlier {
		t.Error("100 should be an outlier in testData")
	}

	isOutlier, err = IsOutlier(5, testData, Linear, 1.5)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if isOutlier {
		t.Error("5 should not be an outlier in testData")
	}
}

func TestWinsorize(t *testing.T) {
	result, err := Winsorize(testDataWithOutlier, 10, 90, Linear)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(result) != len(testDataWithOutlier) {
		t.Errorf("expected %d values, got %d", len(testDataWithOutlier), len(result))
	}
}

func TestNormalizeByPercentile(t *testing.T) {
	result, err := NormalizeByPercentile(testData, 25, 75, Linear)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(result) != len(testData) {
		t.Errorf("expected %d values, got %d", len(testData), len(result))
	}

	// Check normalization bounds
	for _, v := range result {
		if math.IsNaN(v) || math.IsInf(v, 0) {
			t.Errorf("normalized value is invalid: %.2f", v)
		}
	}
}

func TestMean(t *testing.T) {
	mean := Mean(testData)
	expected := 5.5

	if math.Abs(mean-expected) > 0.01 {
		t.Errorf("expected %.2f, got %.2f", expected, mean)
	}
}

func TestVariance(t *testing.T) {
	variance := Variance(testData)
	expected := 8.25

	if math.Abs(variance-expected) > 0.01 {
		t.Errorf("expected %.2f, got %.2f", expected, variance)
	}
}

func TestStdDev(t *testing.T) {
	stdDev := StdDev(testData)
	expected := math.Sqrt(8.25)

	if math.Abs(stdDev-expected) > 0.01 {
		t.Errorf("expected %.2f, got %.2f", expected, stdDev)
	}
}

func TestMedian(t *testing.T) {
	median, err := Median(testData, Linear)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if math.Abs(median-5.5) > 0.01 {
		t.Errorf("expected 5.5, got %.2f", median)
	}
}

func TestSummary(t *testing.T) {
	summary, err := CalculateSummary(testData, Linear)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if summary.Count != 10 {
		t.Errorf("Count expected 10, got %d", summary.Count)
	}
	if math.Abs(summary.Min-1) > 0.01 {
		t.Errorf("Min expected 1, got %.2f", summary.Min)
	}
	if math.Abs(summary.Max-10) > 0.01 {
		t.Errorf("Max expected 10, got %.2f", summary.Max)
	}
	if math.Abs(summary.Sum-55) > 0.01 {
		t.Errorf("Sum expected 55, got %.2f", summary.Sum)
	}
	if math.Abs(summary.Mean-5.5) > 0.01 {
		t.Errorf("Mean expected 5.5, got %.2f", summary.Mean)
	}
	if len(summary.Percentiles) != 7 {
		t.Errorf("Percentiles expected 7 keys, got %d", len(summary.Percentiles))
	}
}

func TestMustFunctions(t *testing.T) {
	// Test MustPercentile
	result := MustPercentile(testData, 50, Linear)
	if math.Abs(result-5.5) > 0.01 {
		t.Errorf("MustPercentile expected 5.5, got %.2f", result)
	}

	// Test MustQuartiles
	qs := MustQuartiles(testData, Linear)
	if math.Abs(qs.Q2-5.5) > 0.01 {
		t.Errorf("MustQuartiles Q2 expected 5.5, got %.2f", qs.Q2)
	}

	// Test MustMedian
	median := MustMedian(testData)
	if math.Abs(median-5.5) > 0.01 {
		t.Errorf("MustMedian expected 5.5, got %.2f", median)
	}

	// Test MustSummary
	summary := MustSummary(testData)
	if summary.Count != 10 {
		t.Errorf("MustSummary Count expected 10, got %d", summary.Count)
	}
}

func TestMustFunctionsPanic(t *testing.T) {
	// Test that MustPercentile panics on empty data
	defer func() {
		if r := recover(); r == nil {
			t.Error("MustPercentile should panic on empty data")
		}
	}()
	MustPercentile(nil, 50, Linear)
}

func TestInterpolationMethods(t *testing.T) {
	data := []float64{1, 2, 3, 4, 5}

	// For 5-element data [1,2,3,4,5], P30:
	// rank = 0.30 * (5-1) = 1.2
	tests := []struct {
		method   InterpolationMethod
		p        float64
		expected float64
	}{
		{Linear, 30, 2.2},    // rank=1.2, idx 1->2, fraction=0.2 => 2+0.2*(3-2)=2.2
		{Lower, 30, 2},       // floor(1.2)=1 -> data[1]=2
		{Higher, 30, 3},      // ceil(1.2)=2 -> data[2]=3
		{Nearest, 30, 2},     // round(1.2)=1 -> data[1]=2
		{Midpoint, 30, 2.5},  // (data[1]+data[2])/2 = (2+3)/2 = 2.5
		{Inclusive, 30, 2.2}, // same as linear
	}

	for _, tt := range tests {
		t.Run(tt.method.String()+"_P30", func(t *testing.T) {
			result, err := Percentile(data, tt.p, tt.method, false)
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if math.Abs(result-tt.expected) > 0.01 {
				t.Errorf("expected %.2f, got %.2f", tt.expected, result)
			}
		})
	}
}

func TestExclusiveMethod(t *testing.T) {
	// Exclusive method requires at least 4 data points
	_, err := Percentile([]float64{1, 2, 3}, 50, Exclusive, false)
	if err != ErrInsufficientData {
		t.Errorf("expected ErrInsufficientData, got %v", err)
	}

	// Test with sufficient data
	data := []float64{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	result, err := Percentile(data, 50, Exclusive, false)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	// Should work for valid percentile range
	if result < 1 || result > 10 {
		t.Errorf("result should be within data range, got %.2f", result)
	}
}

func TestSortedDataFlag(t *testing.T) {
	unsorted := []float64{5, 1, 3, 2, 4}
	sorted := []float64{1, 2, 3, 4, 5}

	// Results should be the same regardless of sorted flag
	p1, err1 := Percentile(unsorted, 50, Linear, false)
	p2, err2 := Percentile(sorted, 50, Linear, true)

	if err1 != nil || err2 != nil {
		t.Fatalf("unexpected errors: %v, %v", err1, err2)
	}

	if math.Abs(p1-p2) > 0.01 {
		t.Errorf("sorted flag should not affect result: %.2f vs %.2f", p1, p2)
	}
}

func TestInterpolationMethodString(t *testing.T) {
	tests := []struct {
		method   InterpolationMethod
		expected string
	}{
		{Linear, "Linear"},
		{Lower, "Lower"},
		{Higher, "Higher"},
		{Nearest, "Nearest"},
		{Midpoint, "Midpoint"},
		{Exclusive, "Exclusive"},
		{Inclusive, "Inclusive"},
	}

	for _, tt := range tests {
		if tt.method.String() != tt.expected {
			t.Errorf("expected %s, got %s", tt.expected, tt.method.String())
		}
	}
}