package mathutils

import (
	"math"
	"testing"
)

// Helper function to compare floats with tolerance
func approxEqual(a, b, tolerance float64) bool {
	return math.Abs(a-b) < tolerance
}

func TestMean(t *testing.T) {
	tests := []struct {
		name     string
		values   []float64
		expected float64
	}{
		{"empty slice", []float64{}, 0},
		{"single value", []float64{5}, 5},
		{"simple average", []float64{1, 2, 3, 4, 5}, 3},
		{"floating point", []float64{1.5, 2.5, 3.5}, 2.5},
		{"negative values", []float64{-1, 0, 1}, 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Mean(tt.values)
			if !approxEqual(result, tt.expected, 1e-10) {
				t.Errorf("Mean(%v) = %f; want %f", tt.values, result, tt.expected)
			}
		})
	}
}

func TestMedian(t *testing.T) {
	tests := []struct {
		name     string
		values   []float64
		expected float64
	}{
		{"empty slice", []float64{}, 0},
		{"single value", []float64{5}, 5},
		{"odd count", []float64{1, 3, 5}, 3},
		{"even count", []float64{1, 2, 3, 4}, 2.5},
		{"unsorted odd", []float64{5, 1, 3}, 3},
		{"unsorted even", []float64{4, 1, 3, 2}, 2.5},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Median(tt.values)
			if !approxEqual(result, tt.expected, 1e-10) {
				t.Errorf("Median(%v) = %f; want %f", tt.values, result, tt.expected)
			}
		})
	}
}

func TestMode(t *testing.T) {
	tests := []struct {
		name     string
		values   []float64
		expected []float64
	}{
		{"empty slice", []float64{}, []float64{}},
		{"single value", []float64{5}, []float64{5}},
		{"single mode", []float64{1, 2, 2, 3}, []float64{2}},
		{"multiple modes", []float64{1, 1, 2, 2, 3}, []float64{1, 2}},
		{"all same", []float64{3, 3, 3, 3}, []float64{3}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Mode(tt.values)
			if len(result) != len(tt.expected) {
				t.Errorf("Mode(%v) = %v; want %v", tt.values, result, tt.expected)
				return
			}
			for i, v := range result {
				if v != tt.expected[i] {
					t.Errorf("Mode(%v) = %v; want %v", tt.values, result, tt.expected)
					return
				}
			}
		})
	}
}

func TestVariance(t *testing.T) {
	tests := []struct {
		name     string
		values   []float64
		expected float64
	}{
		{"empty slice", []float64{}, 0},
		{"single value", []float64{5}, 0},
		{"simple variance", []float64{2, 4, 4, 4, 5, 5, 7, 9}, 4},
		{"zero variance", []float64{3, 3, 3}, 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Variance(tt.values)
			if !approxEqual(result, tt.expected, 1e-10) {
				t.Errorf("Variance(%v) = %f; want %f", tt.values, result, tt.expected)
			}
		})
	}
}

func TestStdDev(t *testing.T) {
	tests := []struct {
		name     string
		values   []float64
		expected float64
	}{
		{"empty slice", []float64{}, 0},
		{"single value", []float64{5}, 0},
		{"simple stddev", []float64{2, 4, 4, 4, 5, 5, 7, 9}, 2},
		{"zero stddev", []float64{3, 3, 3}, 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := StdDev(tt.values)
			if !approxEqual(result, tt.expected, 1e-10) {
				t.Errorf("StdDev(%v) = %f; want %f", tt.values, result, tt.expected)
			}
		})
	}
}

func TestMin(t *testing.T) {
	tests := []struct {
		name      string
		values    []float64
		expected  float64
		expectOk  bool
	}{
		{"empty slice", []float64{}, 0, false},
		{"single value", []float64{5}, 5, true},
		{"positive values", []float64{3, 1, 4, 1, 5}, 1, true},
		{"negative values", []float64{-3, -1, -4, -1, -5}, -5, true},
		{"mixed values", []float64{-2, 0, 2}, -2, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, ok := Min(tt.values)
			if ok != tt.expectOk {
				t.Errorf("Min(%v) ok = %v; want %v", tt.values, ok, tt.expectOk)
			}
			if ok && !approxEqual(result, tt.expected, 1e-10) {
				t.Errorf("Min(%v) = %f; want %f", tt.values, result, tt.expected)
			}
		})
	}
}

func TestMax(t *testing.T) {
	tests := []struct {
		name      string
		values    []float64
		expected  float64
		expectOk  bool
	}{
		{"empty slice", []float64{}, 0, false},
		{"single value", []float64{5}, 5, true},
		{"positive values", []float64{3, 1, 4, 1, 5}, 5, true},
		{"negative values", []float64{-3, -1, -4, -1, -5}, -1, true},
		{"mixed values", []float64{-2, 0, 2}, 2, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, ok := Max(tt.values)
			if ok != tt.expectOk {
				t.Errorf("Max(%v) ok = %v; want %v", tt.values, ok, tt.expectOk)
			}
			if ok && !approxEqual(result, tt.expected, 1e-10) {
				t.Errorf("Max(%v) = %f; want %f", tt.values, result, tt.expected)
			}
		})
	}
}

func TestSum(t *testing.T) {
	tests := []struct {
		name     string
		values   []float64
		expected float64
	}{
		{"empty slice", []float64{}, 0},
		{"single value", []float64{5}, 5},
		{"positive values", []float64{1, 2, 3, 4, 5}, 15},
		{"negative values", []float64{-1, -2, -3}, -6},
		{"mixed values", []float64{-1, 0, 1}, 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Sum(tt.values)
			if !approxEqual(result, tt.expected, 1e-10) {
				t.Errorf("Sum(%v) = %f; want %f", tt.values, result, tt.expected)
			}
		})
	}
}

func TestRange(t *testing.T) {
	tests := []struct {
		name     string
		values   []float64
		expected float64
	}{
		{"empty slice", []float64{}, 0},
		{"single value", []float64{5}, 0},
		{"positive values", []float64{1, 5, 3, 9, 2}, 8},
		{"negative values", []float64{-5, -1, -3}, 4},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Range(tt.values)
			if !approxEqual(result, tt.expected, 1e-10) {
				t.Errorf("Range(%v) = %f; want %f", tt.values, result, tt.expected)
			}
		})
	}
}

func TestPercentile(t *testing.T) {
	tests := []struct {
		name       string
		values     []float64
		percentile float64
		expected   float64
	}{
		{"empty slice", []float64{}, 50, 0},
		{"p0", []float64{1, 2, 3, 4, 5}, 0, 1},
		{"p25", []float64{1, 2, 3, 4, 5}, 25, 2},
		{"p50 (median)", []float64{1, 2, 3, 4, 5}, 50, 3},
		{"p75", []float64{1, 2, 3, 4, 5}, 75, 4},
		{"p100", []float64{1, 2, 3, 4, 5}, 100, 5},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Percentile(tt.values, tt.percentile)
			if !approxEqual(result, tt.expected, 0.1) {
				t.Errorf("Percentile(%v, %f) = %f; want %f", tt.values, tt.percentile, result, tt.expected)
			}
		})
	}
}

func TestPercentilePanic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Percentile with invalid percentile should panic")
		}
	}()
	Percentile([]float64{1, 2, 3}, 150)
}

func TestQuartiles(t *testing.T) {
	tests := []struct {
		name    string
		values  []float64
		q1      float64
		q2      float64
		q3      float64
	}{
		{"empty slice", []float64{}, 0, 0, 0},
		{"simple set", []float64{1, 2, 3, 4, 5, 6, 7, 8}, 2.75, 4.5, 6.25},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			q1, q2, q3 := Quartiles(tt.values)
			if len(tt.values) > 0 {
				if !approxEqual(q1, tt.q1, 0.1) {
					t.Errorf("Q1 = %f; want %f", q1, tt.q1)
				}
				if !approxEqual(q2, tt.q2, 0.1) {
					t.Errorf("Q2 = %f; want %f", q2, tt.q2)
				}
				if !approxEqual(q3, tt.q3, 0.1) {
					t.Errorf("Q3 = %f; want %f", q3, tt.q3)
				}
			}
		})
	}
}

func TestIQR(t *testing.T) {
	tests := []struct {
		name     string
		values   []float64
		expected float64
	}{
		{"empty slice", []float64{}, 0},
		{"simple set", []float64{1, 2, 3, 4, 5, 6, 7, 8}, 3.5},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := IQR(tt.values)
			if !approxEqual(result, tt.expected, 0.1) {
				t.Errorf("IQR(%v) = %f; want %f", tt.values, result, tt.expected)
			}
		})
	}
}

func TestGeometricMean(t *testing.T) {
	tests := []struct {
		name     string
		values   []float64
		expected float64
	}{
		{"empty slice", []float64{}, 0},
		{"single value", []float64{4}, 4},
		{"simple", []float64{2, 8}, 4},
		{"three values", []float64{1, 2, 4}, 2},
		{"non-positive", []float64{1, -2, 3}, 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := GeometricMean(tt.values)
			if !approxEqual(result, tt.expected, 1e-10) {
				t.Errorf("GeometricMean(%v) = %f; want %f", tt.values, result, tt.expected)
			}
		})
	}
}

func TestHarmonicMean(t *testing.T) {
	tests := []struct {
		name     string
		values   []float64
		expected float64
	}{
		{"empty slice", []float64{}, 0},
		{"single value", []float64{4}, 4},
		{"simple", []float64{1, 4}, 1.6},
		{"three values", []float64{1, 2, 4}, 1.714285714},
		{"non-positive", []float64{1, -2, 3}, 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := HarmonicMean(tt.values)
			if !approxEqual(result, tt.expected, 1e-6) {
				t.Errorf("HarmonicMean(%v) = %f; want %f", tt.values, result, tt.expected)
			}
		})
	}
}

func TestDescribe(t *testing.T) {
	values := []float64{1, 2, 3, 4, 5}
	stats := Describe(values)

	if stats.Count != 5 {
		t.Errorf("Count = %d; want 5", stats.Count)
	}
	if !approxEqual(stats.Sum, 15, 1e-10) {
		t.Errorf("Sum = %f; want 15", stats.Sum)
	}
	if !approxEqual(stats.Mean, 3, 1e-10) {
		t.Errorf("Mean = %f; want 3", stats.Mean)
	}
	if !approxEqual(stats.Median, 3, 1e-10) {
		t.Errorf("Median = %f; want 3", stats.Median)
	}
	if !approxEqual(stats.Min, 1, 1e-10) {
		t.Errorf("Min = %f; want 1", stats.Min)
	}
	if !approxEqual(stats.Max, 5, 1e-10) {
		t.Errorf("Max = %f; want 5", stats.Max)
	}
	if !approxEqual(stats.Range, 4, 1e-10) {
		t.Errorf("Range = %f; want 4", stats.Range)
	}
}

func TestDescribeEmpty(t *testing.T) {
	stats := Describe([]float64{})
	if stats.Count != 0 {
		t.Errorf("Count = %d; want 0", stats.Count)
	}
}

func TestCoefficientOfVariation(t *testing.T) {
	tests := []struct {
		name     string
		values   []float64
		expected float64
	}{
		{"empty slice", []float64{}, 0},
		{"single value", []float64{5}, 0},
		{"simple", []float64{10, 12, 14, 16, 18}, 22.360679775},
		{"zero mean", []float64{-1, 0, 1}, 0}, // zero mean edge case
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CoefficientOfVariation(tt.values)
			if tt.expected == 0 {
				if result != 0 {
					t.Errorf("CoefficientOfVariation(%v) = %f; want 0", tt.values, result)
				}
			} else {
				if !approxEqual(result, tt.expected, 0.01) {
					t.Errorf("CoefficientOfVariation(%v) = %f; want %f", tt.values, result, tt.expected)
				}
			}
		})
	}
}

func TestZScore(t *testing.T) {
	tests := []struct {
		name     string
		values   []float64
		x        float64
		expected float64
	}{
		{"empty slice", []float64{}, 3, 0},
		{"single value", []float64{5}, 5, 0},
		{"mean value", []float64{1, 2, 3, 4, 5}, 3, 0},
		{"below mean", []float64{1, 2, 3, 4, 5}, 1, -1.414213562},
		{"above mean", []float64{1, 2, 3, 4, 5}, 5, 1.414213562},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := ZScore(tt.values, tt.x)
			if !approxEqual(result, tt.expected, 1e-6) {
				t.Errorf("ZScore(%v, %f) = %f; want %f", tt.values, tt.x, result, tt.expected)
			}
		})
	}
}

func TestSampleVariance(t *testing.T) {
	values := []float64{2, 4, 4, 4, 5, 5, 7, 9}
	result := SampleVariance(values)
	expected := 32.0 / 7.0 // Bessel's correction
	if !approxEqual(result, expected, 1e-10) {
		t.Errorf("SampleVariance(%v) = %f; want %f", values, result, expected)
	}
}

func TestSampleStdDev(t *testing.T) {
	values := []float64{2, 4, 4, 4, 5, 5, 7, 9}
	result := SampleStdDev(values)
	expected := math.Sqrt(32.0 / 7.0)
	if !approxEqual(result, expected, 1e-10) {
		t.Errorf("SampleStdDev(%v) = %f; want %f", values, result, expected)
	}
}

// Benchmark tests
func BenchmarkMean(b *testing.B) {
	values := make([]float64, 1000)
	for i := range values {
		values[i] = float64(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Mean(values)
	}
}

func BenchmarkMedian(b *testing.B) {
	values := make([]float64, 1000)
	for i := range values {
		values[i] = float64(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Median(values)
	}
}

func BenchmarkStdDev(b *testing.B) {
	values := make([]float64, 1000)
	for i := range values {
		values[i] = float64(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		StdDev(values)
	}
}

func BenchmarkDescribe(b *testing.B) {
	values := make([]float64, 1000)
	for i := range values {
		values[i] = float64(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Describe(values)
	}
}