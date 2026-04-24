package hyperloglog

import (
	"math/rand"
	"testing"
)

func TestNew(t *testing.T) {
	hll := New()
	if hll == nil {
		t.Fatal("New() returned nil")
	}
	if hll.precision != DefaultPrecision {
		t.Errorf("Expected precision %d, got %d", DefaultPrecision, hll.precision)
	}
}

func TestNewWithPrecision(t *testing.T) {
	tests := []struct {
		input    uint8
		expected uint8
	}{
		{4, 4},   // Minimum
		{14, 14}, // Default
		{16, 16}, // Maximum
		{0, 4},   // Below minimum, should clamp
		{20, 16}, // Above maximum, should clamp
	}

	for _, tt := range tests {
		hll := NewWithPrecision(tt.input)
		if hll.precision != tt.expected {
			t.Errorf("NewWithPrecision(%d) = precision %d, want %d", tt.input, hll.precision, tt.expected)
		}
	}
}

func TestEmpty(t *testing.T) {
	hll := New()
	if !hll.Empty() {
		t.Error("New HyperLogLog should be empty")
	}

	hll.AddString("test")
	if hll.Empty() {
		t.Error("HyperLogLog with one element should not be empty")
	}
}

func TestAddString(t *testing.T) {
	hll := New()

	// Add same string multiple times
	for i := 0; i < 100; i++ {
		hll.AddString("hello")
	}

	estimate := hll.Estimate()
	if estimate != 1 {
		t.Errorf("Expected estimate 1 for single unique element, got %d", estimate)
	}
}

func TestAddInt(t *testing.T) {
	hll := New()

	// Add same int multiple times
	for i := 0; i < 100; i++ {
		hll.AddInt(42)
	}

	estimate := hll.Estimate()
	if estimate != 1 {
		t.Errorf("Expected estimate 1 for single unique element, got %d", estimate)
	}
}

func TestMultipleUniqueElements(t *testing.T) {
	hll := New()

	// Add 1000 unique strings
	for i := 0; i < 1000; i++ {
		hll.AddString(randomString(10))
	}

	estimate := hll.Estimate()
	errorRate := float64(estimate-1000) / 1000.0
	if errorRate < 0 {
		errorRate = -errorRate
	}

	// HyperLogLog with precision 14 should have < 2% error
	if errorRate > 0.05 { // Use 5% threshold for test reliability
		t.Errorf("Error rate too high: %.2f%% (estimate: %d, actual: 1000)", errorRate*100, estimate)
	}
}

func TestEstimateAccuracy(t *testing.T) {
	hll := NewWithPrecision(14)

	cardinalities := []int{100, 1000, 10000}

	for _, cardinality := range cardinalities {
		hll.Reset()
		for i := 0; i < cardinality; i++ {
			hll.AddInt(int64(i))
		}

		estimate := hll.Estimate()
		errorRate := float64(estimate-int64(cardinality)) / float64(cardinality)
		if errorRate < 0 {
			errorRate = -errorRate
		}

		t.Logf("Cardinality %d: estimate=%d, error=%.2f%%", cardinality, estimate, errorRate*100)

		// Should be within 5% error
		if errorRate > 0.05 {
			t.Errorf("Error rate too high for cardinality %d: %.2f%% (estimate: %d)", cardinality, errorRate*100, estimate)
		}
	}
}

func TestMerge(t *testing.T) {
	hll1 := New()
	hll2 := New()

	// Add different elements to each
	for i := 0; i < 500; i++ {
		hll1.AddInt(int64(i))
	}
	for i := 500; i < 1000; i++ {
		hll2.AddInt(int64(i))
	}

	// Merge
	if !hll1.Merge(hll2) {
		t.Fatal("Merge failed")
	}

	estimate := hll1.Estimate()
	errorRate := float64(estimate-1000) / 1000.0
	if errorRate < 0 {
		errorRate = -errorRate
	}

	if errorRate > 0.05 {
		t.Errorf("Merge error rate too high: %.2f%% (estimate: %d, actual: 1000)", errorRate*100, estimate)
	}
}

func TestMergeDifferentPrecision(t *testing.T) {
	hll1 := NewWithPrecision(10)
	hll2 := NewWithPrecision(14)

	if hll1.Merge(hll2) {
		t.Error("Merge with different precision should return false")
	}
}

func TestReset(t *testing.T) {
	hll := New()

	for i := 0; i < 100; i++ {
		hll.AddInt(int64(i))
	}

	if hll.Empty() {
		t.Error("HyperLogLog should not be empty after adding elements")
	}

	hll.Reset()

	if !hll.Empty() {
		t.Error("HyperLogLog should be empty after reset")
	}
}

func TestClone(t *testing.T) {
	hll1 := New()

	for i := 0; i < 100; i++ {
		hll1.AddInt(int64(i))
	}

	hll2 := hll1.Clone()

	if hll1.Estimate() != hll2.Estimate() {
		t.Errorf("Clone estimate mismatch: %d vs %d", hll1.Estimate(), hll2.Estimate())
	}

	// Modify original, clone should be unaffected
	hll1.AddInt(int64(999999))

	if hll1.Estimate() == hll2.Estimate() {
		t.Error("Clone should be independent from original")
	}
}

func TestSerializeDeserialize(t *testing.T) {
	hll1 := New()

	for i := 0; i < 1000; i++ {
		hll1.AddInt(int64(i))
	}

	data := hll1.ToBytes()
	hll2, ok := FromBytes(data)

	if !ok {
		t.Fatal("Deserialization failed")
	}

	if hll1.Estimate() != hll2.Estimate() {
		t.Errorf("Estimate mismatch after deserialization: %d vs %d", hll1.Estimate(), hll2.Estimate())
	}

	if hll1.precision != hll2.precision {
		t.Errorf("Precision mismatch: %d vs %d", hll1.precision, hll2.precision)
	}
}

func TestSerializeDeserializeInvalid(t *testing.T) {
	tests := []struct {
		name string
		data []byte
	}{
		{"empty", []byte{}},
		{"too short", []byte{14}},
		{"invalid precision", []byte{3, 0, 0}},           // Below minimum
		{"invalid precision 2", []byte{20, 0, 0}},        // Above maximum
		{"wrong length", append([]byte{14}, make([]byte, 10)...)}, // Wrong number of buckets
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			_, ok := FromBytes(tt.data)
			if ok {
				t.Errorf("FromBytes should fail for invalid data: %v", tt.name)
			}
		})
	}
}

func TestMemoryUsage(t *testing.T) {
	hll := NewWithPrecision(14)
	expected := 1 << 14 // 16384 bytes
	if hll.MemoryUsage() != expected {
		t.Errorf("MemoryUsage() = %d, want %d", hll.MemoryUsage(), expected)
	}
}

func TestErrorRate(t *testing.T) {
	hll := NewWithPrecision(14)
	expectedError := 1.04 / float64(1<<7) // sqrt(16384) = 128
	errorRate := hll.ErrorRate()

	delta := expectedError - errorRate
	if delta < 0 {
		delta = -delta
	}

	if delta > 0.001 {
		t.Errorf("ErrorRate() = %.4f, want approximately %.4f", errorRate, expectedError)
	}
}

func TestCount(t *testing.T) {
	hll := New()

	for i := 0; i < 100; i++ {
		hll.AddInt(int64(i))
	}

	// Count() should return the same as Estimate()
	if hll.Count() != hll.Estimate() {
		t.Errorf("Count() != Estimate(): %d vs %d", hll.Count(), hll.Estimate())
	}
}

// Benchmark tests
func BenchmarkAdd(b *testing.B) {
	hll := New()
	data := []byte("benchmark test string")

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		hll.Add(data)
	}
}

func BenchmarkAddInt(b *testing.B) {
	hll := New()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		hll.AddInt(int64(i))
	}
}

func BenchmarkEstimate(b *testing.B) {
	hll := New()

	for i := 0; i < 100000; i++ {
		hll.AddInt(int64(i))
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		hll.Estimate()
	}
}

func BenchmarkMerge(b *testing.B) {
	hll1 := New()
	hll2 := New()

	for i := 0; i < 10000; i++ {
		hll1.AddInt(int64(i))
		hll2.AddInt(int64(i + 10000))
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		hll1.Clone().Merge(hll2)
	}
}

func BenchmarkSerialize(b *testing.B) {
	hll := New()

	for i := 0; i < 10000; i++ {
		hll.AddInt(int64(i))
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		hll.ToBytes()
	}
}

func BenchmarkDeserialize(b *testing.B) {
	hll := New()

	for i := 0; i < 10000; i++ {
		hll.AddInt(int64(i))
	}

	data := hll.ToBytes()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		FromBytes(data)
	}
}

// Helper function
func randomString(length int) string {
	const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	b := make([]byte, length)
	for i := range b {
		b[i] = charset[rand.Intn(len(charset))]
	}
	return string(b)
}