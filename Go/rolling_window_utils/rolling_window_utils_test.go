package rolling_window_utils

import (
	"math"
	"testing"
)

func TestNewRollingWindow(t *testing.T) {
	rw := NewRollingWindow(5)
	if rw.Size() != 5 {
		t.Errorf("Expected size 5, got %d", rw.Size())
	}
	if rw.Count() != 0 {
		t.Errorf("Expected count 0, got %d", rw.Count())
	}
	if rw.IsFull() {
		t.Error("Expected window not to be full")
	}
}

func TestNewRollingWindowWithZeroSize(t *testing.T) {
	rw := NewRollingWindow(0)
	if rw.Size() != 1 {
		t.Errorf("Expected size 1 for zero input, got %d", rw.Size())
	}
}

func TestAddAndValues(t *testing.T) {
	rw := NewRollingWindow(3)
	rw.Add(1)
	rw.Add(2)
	rw.Add(3)

	values := rw.Values()
	if len(values) != 3 {
		t.Fatalf("Expected 3 values, got %d", len(values))
	}
	expected := []float64{1, 2, 3}
	for i, v := range values {
		if v != expected[i] {
			t.Errorf("Index %d: expected %f, got %f", i, expected[i], v)
		}
	}
}

func TestRollingBehavior(t *testing.T) {
	rw := NewRollingWindow(3)
	rw.Add(1)
	rw.Add(2)
	rw.Add(3)
	rw.Add(4) // Should push out 1
	rw.Add(5) // Should push out 2

	values := rw.Values()
	expected := []float64{3, 4, 5}
	for i, v := range values {
		if v != expected[i] {
			t.Errorf("Index %d: expected %f, got %f", i, expected[i], v)
		}
	}
}

func TestSum(t *testing.T) {
	rw := NewRollingWindow(5)
	rw.Add(1)
	rw.Add(2)
	rw.Add(3)
	if rw.Sum() != 6 {
		t.Errorf("Expected sum 6, got %f", rw.Sum())
	}
}

func TestAverage(t *testing.T) {
	rw := NewRollingWindow(5)
	if rw.Average() != 0 {
		t.Error("Empty window should return 0 average")
	}
	rw.Add(2)
	rw.Add(4)
	rw.Add(6)
	if rw.Average() != 4 {
		t.Errorf("Expected average 4, got %f", rw.Average())
	}
}

func TestMin(t *testing.T) {
	rw := NewRollingWindow(5)
	if _, ok := rw.Min(); ok {
		t.Error("Empty window should not return min")
	}
	rw.Add(5)
	rw.Add(2)
	rw.Add(8)
	rw.Add(1)
	rw.Add(9)
	min, ok := rw.Min()
	if !ok {
		t.Error("Expected ok to be true")
	}
	if min != 1 {
		t.Errorf("Expected min 1, got %f", min)
	}
}

func TestMax(t *testing.T) {
	rw := NewRollingWindow(5)
	if _, ok := rw.Max(); ok {
		t.Error("Empty window should not return max")
	}
	rw.Add(5)
	rw.Add(2)
	rw.Add(8)
	rw.Add(1)
	rw.Add(9)
	max, ok := rw.Max()
	if !ok {
		t.Error("Expected ok to be true")
	}
	if max != 9 {
		t.Errorf("Expected max 9, got %f", max)
	}
}

func TestRange(t *testing.T) {
	rw := NewRollingWindow(5)
	rw.Add(5)
	rw.Add(2)
	rw.Add(8)
	rw.Add(1)
	rw.Add(9)
	rng, ok := rw.Range()
	if !ok {
		t.Error("Expected ok to be true")
	}
	if rng != 8 {
		t.Errorf("Expected range 8, got %f", rng)
	}
}

func TestVariance(t *testing.T) {
	rw := NewRollingWindow(5)
	if _, ok := rw.Variance(); ok {
		t.Error("Empty window should not return variance")
	}
	rw.Add(2)
	rw.Add(4)
	rw.Add(4)
	rw.Add(4)
	rw.Add(5)
	rw.Add(5)
	rw.Add(7)
	rw.Add(9) // values: 2,4,4,4,5,5,7,9 but window size 5, so 4,4,5,5,7,9
	// After rolling: window contains 4,5,5,7,9
	// mean = 6, variance = ((4-6)^2 + (5-6)^2 + (5-6)^2 + (7-6)^2 + (9-6)^2) / 5
	// = (4 + 1 + 1 + 1 + 9) / 5 = 16/5 = 3.2
	variance, ok := rw.Variance()
	if !ok {
		t.Fatal("Expected ok to be true")
	}
	expected := 3.2
	if math.Abs(variance-expected) > 0.0001 {
		t.Errorf("Expected variance ~%f, got %f", expected, variance)
	}
}

func TestStdDev(t *testing.T) {
	rw := NewRollingWindow(5)
	rw.Add(2)
	rw.Add(4)
	rw.Add(4)
	rw.Add(4)
	rw.Add(5)
	rw.Add(5)
	rw.Add(7)
	rw.Add(9)
	stdDev, ok := rw.StdDev()
	if !ok {
		t.Fatal("Expected ok to be true")
	}
	expected := math.Sqrt(3.2)
	if math.Abs(stdDev-expected) > 0.0001 {
		t.Errorf("Expected stdDev ~%f, got %f", expected, stdDev)
	}
}

func TestMedian(t *testing.T) {
	tests := []struct {
		values   []float64
		window   int
		expected float64
	}{
		{[]float64{1, 2, 3, 4, 5}, 5, 3},
		{[]float64{1, 2, 3, 4}, 4, 2.5},
		{[]float64{5, 1, 3, 2, 4}, 5, 3}, // unsorted input
	}

	for _, tt := range tests {
		rw := NewRollingWindow(tt.window)
		for _, v := range tt.values {
			rw.Add(v)
		}
		median, ok := rw.Median()
		if !ok {
			t.Error("Expected ok to be true")
		}
		if median != tt.expected {
			t.Errorf("Values %v: expected median %f, got %f", tt.values, tt.expected, median)
		}
	}
}

func TestPercentile(t *testing.T) {
	rw := NewRollingWindow(100)
	for i := 1; i <= 100; i++ {
		rw.Add(float64(i))
	}

	tests := []struct {
		p        float64
		expected float64
	}{
		{0, 1},
		{50, 50.5},
		{100, 100},
		{25, 25.75},
		{75, 75.25},
	}

	for _, tt := range tests {
		p, ok := rw.Percentile(tt.p)
		if !ok {
			t.Errorf("Percentile %f: expected ok to be true", tt.p)
		}
		if math.Abs(p-tt.expected) > 0.1 {
			t.Errorf("Percentile %f: expected ~%f, got %f", tt.p, tt.expected, p)
		}
	}
}

func TestFirstAndLast(t *testing.T) {
	rw := NewRollingWindow(5)
	rw.Add(1)
	rw.Add(2)
	rw.Add(3)

	first, ok := rw.First()
	if !ok || first != 1 {
		t.Errorf("Expected first 1, got %f, ok=%v", first, ok)
	}

	last, ok := rw.Last()
	if !ok || last != 3 {
		t.Errorf("Expected last 3, got %f, ok=%v", last, ok)
	}
}

func TestClear(t *testing.T) {
	rw := NewRollingWindow(5)
	rw.Add(1)
	rw.Add(2)
	rw.Add(3)
	rw.Clear()

	if rw.Count() != 0 {
		t.Errorf("Expected count 0 after clear, got %d", rw.Count())
	}
	if rw.Sum() != 0 {
		t.Errorf("Expected sum 0 after clear, got %f", rw.Sum())
	}
}

func TestStats(t *testing.T) {
	rw := NewRollingWindow(5)
	for i := 1; i <= 5; i++ {
		rw.Add(float64(i))
	}

	stats, ok := rw.Stats()
	if !ok {
		t.Fatal("Expected ok to be true")
	}

	if stats.Count != 5 {
		t.Errorf("Expected count 5, got %d", stats.Count)
	}
	if stats.Sum != 15 {
		t.Errorf("Expected sum 15, got %f", stats.Sum)
	}
	if stats.Average != 3 {
		t.Errorf("Expected average 3, got %f", stats.Average)
	}
	if stats.Min != 1 {
		t.Errorf("Expected min 1, got %f", stats.Min)
	}
	if stats.Max != 5 {
		t.Errorf("Expected max 5, got %f", stats.Max)
	}
	if !stats.IsFull {
		t.Error("Expected window to be full")
	}
}

func TestRollingInt(t *testing.T) {
	ri := NewRollingInt(3)
	ri.Add(1)
	ri.Add(2)
	ri.Add(3)
	ri.Add(4)

	values := ri.Values()
	expected := []int{2, 3, 4}
	for i, v := range values {
		if v != expected[i] {
			t.Errorf("Index %d: expected %d, got %d", i, expected[i], v)
		}
	}

	if ri.Sum() != 9 {
		t.Errorf("Expected sum 9, got %d", ri.Sum())
	}

	min, ok := ri.Min()
	if !ok || min != 2 {
		t.Errorf("Expected min 2, got %d, ok=%v", min, ok)
	}

	max, ok := ri.Max()
	if !ok || max != 4 {
		t.Errorf("Expected max 4, got %d, ok=%v", max, ok)
	}
}

func TestEMA(t *testing.T) {
	ema := NewEMA(0.5)

	ema.Add(10)
	if ema.Value() != 10 {
		t.Errorf("First value should be 10, got %f", ema.Value())
	}

	ema.Add(20)
	// EMA = 0.5 * 20 + 0.5 * 10 = 15
	if ema.Value() != 15 {
		t.Errorf("Expected EMA 15, got %f", ema.Value())
	}

	ema.Add(30)
	// EMA = 0.5 * 30 + 0.5 * 15 = 22.5
	if ema.Value() != 22.5 {
		t.Errorf("Expected EMA 22.5, got %f", ema.Value())
	}
}

func TestEMAFromPeriod(t *testing.T) {
	ema := NewEMAFromPeriod(10)
	expectedAlpha := 2.0 / 11.0
	if ema.alpha != expectedAlpha {
		t.Errorf("Expected alpha %f, got %f", expectedAlpha, ema.alpha)
	}
}

func TestEMAReset(t *testing.T) {
	ema := NewEMA(0.5)
	ema.Add(10)
	if !ema.IsInitialized() {
		t.Error("Expected EMA to be initialized")
	}

	ema.Reset()
	if ema.IsInitialized() {
		t.Error("Expected EMA to not be initialized after reset")
	}
	if ema.Value() != 0 {
		t.Errorf("Expected value 0 after reset, got %f", ema.Value())
	}
}

func TestCumulativeSum(t *testing.T) {
	cs := NewCumulativeSum()
	cs.Add(10)
	cs.Add(20)
	cs.Add(30)
	if cs.Sum() != 60 {
		t.Errorf("Expected sum 60, got %f", cs.Sum())
	}

	oldSum := cs.Reset()
	if oldSum != 60 {
		t.Errorf("Expected reset to return 60, got %f", oldSum)
	}
	if cs.Sum() != 0 {
		t.Errorf("Expected sum 0 after reset, got %f", cs.Sum())
	}
}

func TestCounter(t *testing.T) {
	c := NewCounter()

	if c.Value() != 0 {
		t.Errorf("Expected initial value 0, got %d", c.Value())
	}

	if c.Increment() != 1 {
		t.Errorf("Expected increment to return 1")
	}

	if c.Increment() != 2 {
		t.Errorf("Expected increment to return 2")
	}

	if c.Decrement() != 1 {
		t.Errorf("Expected decrement to return 1")
	}

	if c.Add(10) != 11 {
		t.Errorf("Expected add to return 11")
	}

	old := c.Reset()
	if old != 11 {
		t.Errorf("Expected reset to return 11, got %d", old)
	}

	if c.Value() != 0 {
		t.Errorf("Expected value 0 after reset, got %d", c.Value())
	}
}

func TestConcurrentAccess(t *testing.T) {
	rw := NewRollingWindow(100)
	done := make(chan bool)

	// Writer goroutine
	go func() {
		for i := 0; i < 1000; i++ {
			rw.Add(float64(i))
		}
		done <- true
	}()

	// Reader goroutines
	for i := 0; i < 5; i++ {
		go func() {
			for j := 0; j < 200; j++ {
				_ = rw.Sum()
				_ = rw.Average()
				_, _ = rw.Min()
				_, _ = rw.Max()
				_ = rw.Values()
			}
			done <- true
		}()
	}

	// Wait for all goroutines
	for i := 0; i < 6; i++ {
		<-done
	}

	// Verify final state
	if rw.Count() != 100 {
		t.Errorf("Expected count 100, got %d", rw.Count())
	}
}

func TestLargeWindow(t *testing.T) {
	size := 10000
	rw := NewRollingWindow(size)

	for i := 0; i < size*2; i++ {
		rw.Add(float64(i))
	}

	// Window should only contain last 10000 values
	values := rw.Values()
	if len(values) != size {
		t.Errorf("Expected %d values, got %d", size, len(values))
	}

	// First value should be 10000 (first 10000 were pushed out)
	if values[0] != float64(size) {
		t.Errorf("Expected first value %d, got %f", size, values[0])
	}

	// Last value should be 19999
	if values[len(values)-1] != float64(size*2-1) {
		t.Errorf("Expected last value %d, got %f", size*2-1, values[len(values)-1])
	}
}

func BenchmarkAdd(b *testing.B) {
	rw := NewRollingWindow(100)
	for i := 0; i < b.N; i++ {
		rw.Add(float64(i))
	}
}

func BenchmarkMin(b *testing.B) {
	rw := NewRollingWindow(100)
	for i := 0; i < 100; i++ {
		rw.Add(float64(i))
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		rw.Min()
	}
}

func BenchmarkMax(b *testing.B) {
	rw := NewRollingWindow(100)
	for i := 0; i < 100; i++ {
		rw.Add(float64(i))
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		rw.Max()
	}
}

func BenchmarkStats(b *testing.B) {
	rw := NewRollingWindow(100)
	for i := 0; i < 100; i++ {
		rw.Add(float64(i))
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		rw.Stats()
	}
}

func BenchmarkConcurrentAdd(b *testing.B) {
	rw := NewRollingWindow(100)
	b.RunParallel(func(pb *testing.PB) {
		i := 0
		for pb.Next() {
			rw.Add(float64(i))
			i++
		}
	})
}