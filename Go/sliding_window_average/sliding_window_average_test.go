package sliding_window_average

import (
	"testing"
	"time"
)

func TestNew(t *testing.T) {
	// Valid size
	swa, err := New(10)
	if err != nil {
		t.Fatalf("New(10) returned error: %v", err)
	}
	if swa == nil {
		t.Fatal("New(10) returned nil")
	}

	// Invalid size
	_, err = New(0)
	if err == nil {
		t.Error("New(0) should return error")
	}

	_, err = New(-5)
	if err == nil {
		t.Error("New(-5) should return error")
	}
}

func TestNewWithTimestamps(t *testing.T) {
	swa, err := NewWithTimestamps(5)
	if err != nil {
		t.Fatalf("NewWithTimestamps(5) returned error: %v", err)
	}
	if !swa.withTime {
		t.Error("withTime should be true")
	}
}

func TestAdd(t *testing.T) {
	swa, _ := New(3)

	swa.Add(10)
	if swa.Count() != 1 {
		t.Errorf("Count should be 1, got %d", swa.Count())
	}
	if swa.Sum() != 10 {
		t.Errorf("Sum should be 10, got %f", swa.Sum())
	}

	swa.Add(20)
	swa.Add(30)
	if swa.Count() != 3 {
		t.Errorf("Count should be 3, got %d", swa.Count())
	}
	if swa.IsFull() != true {
		t.Error("IsFull should be true")
	}

	// Add beyond capacity - should remove oldest
	swa.Add(40)
	if swa.Count() != 3 {
		t.Errorf("Count should still be 3, got %d", swa.Count())
	}
	// Sum should now be 20+30+40=90 (10 removed)
	if swa.Sum() != 90 {
		t.Errorf("Sum should be 90, got %f", swa.Sum())
	}
}

func TestAverage(t *testing.T) {
	swa, _ := New(5)

	// Empty window
	if swa.Average() != 0 {
		t.Error("Empty window average should be 0")
	}

	swa.Add(10)
	swa.Add(20)
	swa.Add(30)

	expected := 20.0
	if swa.Average() != expected {
		t.Errorf("Average should be %f, got %f", expected, swa.Average())
	}
}

func TestMinMax(t *testing.T) {
	swa, _ := New(5)

	swa.Add(5)
	swa.Add(10)
	swa.Add(3)
	swa.Add(8)

	if swa.Min() != 3 {
		t.Errorf("Min should be 3, got %f", swa.Min())
	}
	if swa.Max() != 10 {
		t.Errorf("Max should be 10, got %f", swa.Max())
	}
}

func TestVariance(t *testing.T) {
	swa, _ := New(10)

	// Use simple dataset: [1, 2, 3, 4, 5]
	// Mean = 3, Variance = ((1-3)² + (2-3)² + (3-3)² + (4-3)² + (5-3)²) / 5 = (4+1+0+1+4)/5 = 2
	swa.Add(1)
	swa.Add(2)
	swa.Add(3)
	swa.Add(4)
	swa.Add(5)

	variance := swa.Variance()
	if variance < 1.9 || variance > 2.1 {
		t.Errorf("Variance should be around 2, got %f", variance)
	}
}

func TestStdDev(t *testing.T) {
	swa, _ := New(10)

	// Use simple dataset: [1, 2, 3, 4, 5]
	// Mean = 3, Variance = 2, StdDev = sqrt(2) ≈ 1.414
	swa.Add(1)
	swa.Add(2)
	swa.Add(3)
	swa.Add(4)
	swa.Add(5)

	stdDev := swa.StdDev()
	if stdDev < 1.3 || stdDev > 1.5 {
		t.Errorf("StdDev should be around 1.414, got %f", stdDev)
	}
}

func TestMedian(t *testing.T) {
	swa, _ := New(10)

	// Odd count
	swa.Add(1)
	swa.Add(3)
	swa.Add(2)
	if swa.Median() != 2 {
		t.Errorf("Median should be 2, got %f", swa.Median())
	}

	// Even count
	swa.Add(4)
	if swa.Median() != 2.5 {
		t.Errorf("Median should be 2.5, got %f", swa.Median())
	}
}

func TestPercentile(t *testing.T) {
	swa, _ := New(10)

	// Add values 1-10
	for i := 1; i <= 10; i++ {
		swa.Add(float64(i))
	}

	p25 := swa.Percentile(25)
	if p25 < 2.5 || p25 > 3.5 {
		t.Errorf("P25 should be around 3, got %f", p25)
	}

	p50 := swa.Percentile(50)
	if p50 < 4.5 || p50 > 5.5 {
		t.Errorf("P50 should be around 5.5, got %f", p50)
	}

	p95 := swa.Percentile(95)
	if p95 < 9.4 || p95 > 9.6 {
		t.Errorf("P95 should be around 9.45, got %f", p95)
	}
}

func TestValues(t *testing.T) {
	swa, _ := New(5)

	swa.Add(1)
	swa.Add(2)
	swa.Add(3)

	values := swa.Values()
	if len(values) != 3 {
		t.Fatalf("Expected 3 values, got %d", len(values))
	}

	expected := []float64{1, 2, 3}
	for i, v := range values {
		if v != expected[i] {
			t.Errorf("Values[%d] should be %f, got %f", i, expected[i], v)
		}
	}
}

func TestValuesOrder(t *testing.T) {
	swa, _ := New(3)

	swa.Add(1)
	swa.Add(2)
	swa.Add(3)
	swa.Add(4) // Removes 1

	values := swa.Values()
	if len(values) != 3 {
		t.Fatalf("Expected 3 values, got %d", len(values))
	}

	expected := []float64{2, 3, 4}
	for i, v := range values {
		if v != expected[i] {
			t.Errorf("Values[%d] should be %f, got %f", i, expected[i], v)
		}
	}
}

func TestClear(t *testing.T) {
	swa, _ := New(5)

	swa.Add(1)
	swa.Add(2)
	swa.Add(3)

	swa.Clear()

	if swa.Count() != 0 {
		t.Errorf("Count after clear should be 0, got %d", swa.Count())
	}
	if swa.Sum() != 0 {
		t.Errorf("Sum after clear should be 0, got %f", swa.Sum())
	}
	if swa.IsFull() {
		t.Error("Window should not be full after clear")
	}
}

func TestRate(t *testing.T) {
	swa, _ := NewWithTimestamps(5)

	// Add first value
	swa.AddWithTimestamp(10, time.Now())
	
	// Add second value 2 seconds later
	swa.AddWithTimestamp(30, time.Now().Add(2*time.Second))

	// Sum = 40, duration = 2 seconds, rate = 20 per second
	rate := swa.Rate()
	if rate < 19 || rate > 21 {
		t.Errorf("Rate should be around 20, got %f", rate)
	}
}

func TestGetStats(t *testing.T) {
	swa, _ := New(10)

	for i := 1; i <= 10; i++ {
		swa.Add(float64(i))
	}

	stats := swa.GetStats()

	if stats.Count != 10 {
		t.Errorf("Count should be 10, got %d", stats.Count)
	}
	if stats.Sum != 55 {
		t.Errorf("Sum should be 55, got %f", stats.Sum)
	}
	if stats.Average != 5.5 {
		t.Errorf("Average should be 5.5, got %f", stats.Average)
	}
	if stats.Min != 1 {
		t.Errorf("Min should be 1, got %f", stats.Min)
	}
	if stats.Max != 10 {
		t.Errorf("Max should be 10, got %f", stats.Max)
	}
}

func TestConcurrentAccess(t *testing.T) {
	swa, _ := New(100)
	done := make(chan bool)

	// Writer goroutine
	go func() {
		for i := 0; i < 1000; i++ {
			swa.Add(float64(i))
		}
		done <- true
	}()

	// Reader goroutines
	go func() {
		for i := 0; i < 1000; i++ {
			_ = swa.Average()
			_ = swa.Count()
			_ = swa.Values()
		}
		done <- true
	}()

	go func() {
		for i := 0; i < 1000; i++ {
			_ = swa.Min()
			_ = swa.Max()
			_ = swa.StdDev()
		}
		done <- true
	}()

	// Wait for all goroutines
	<-done
	<-done
	<-done

	// Just verify no panic occurred
	if swa.Count() != 100 {
		t.Errorf("Final count should be 100, got %d", swa.Count())
	}
}

func TestSqrt(t *testing.T) {
	tests := []struct {
		input    float64
		expected float64
	}{
		{0, 0},
		{1, 1},
		{4, 2},
		{9, 3},
		{16, 4},
		{2, 1.414}, // approximately
	}

	for _, tt := range tests {
		result := sqrt(tt.input)
		if tt.input == 0 || tt.input == 1 {
			if result != tt.expected {
				t.Errorf("sqrt(%f) = %f, expected %f", tt.input, result, tt.expected)
			}
		} else {
			// Allow small margin for approximation
			diff := result - tt.expected
			if diff < 0 {
				diff = -diff
			}
			if diff > 0.1 {
				t.Errorf("sqrt(%f) = %f, expected approximately %f", tt.input, result, tt.expected)
			}
		}
	}
}

func TestEdgeCases(t *testing.T) {
	t.Run("SingleValue", func(t *testing.T) {
		swa, _ := New(5)
		swa.Add(42)

		if swa.Average() != 42 {
			t.Errorf("Single value average should be 42, got %f", swa.Average())
		}
		if swa.Variance() != 0 {
			t.Errorf("Single value variance should be 0, got %f", swa.Variance())
		}
	})

	t.Run("NegativeValues", func(t *testing.T) {
		swa, _ := New(5)
		swa.Add(-5)
		swa.Add(-10)
		swa.Add(-15)

		if swa.Average() != -10 {
			t.Errorf("Average of negatives should be -10, got %f", swa.Average())
		}
		if swa.Min() != -15 {
			t.Errorf("Min should be -15, got %f", swa.Min())
		}
	})

	t.Run("MixedValues", func(t *testing.T) {
		swa, _ := New(5)
		swa.Add(-5)
		swa.Add(0)
		swa.Add(5)

		if swa.Average() != 0 {
			t.Errorf("Average should be 0, got %f", swa.Average())
		}
	})

	t.Run("FloatingPointPrecision", func(t *testing.T) {
		swa, _ := New(3)
		swa.Add(0.1)
		swa.Add(0.2)
		swa.Add(0.3)

		// Just verify it doesn't crash and produces reasonable results
		avg := swa.Average()
		if avg < 0.19 || avg > 0.21 {
			t.Errorf("Average should be around 0.2, got %f", avg)
		}
	})
}

func BenchmarkAdd(b *testing.B) {
	swa, _ := New(100)
	for i := 0; i < b.N; i++ {
		swa.Add(float64(i))
	}
}

func BenchmarkAverage(b *testing.B) {
	swa, _ := New(100)
	for i := 0; i < 100; i++ {
		swa.Add(float64(i))
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = swa.Average()
	}
}

func BenchmarkMedian(b *testing.B) {
	swa, _ := New(100)
	for i := 0; i < 100; i++ {
		swa.Add(float64(i))
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = swa.Median()
	}
}

func BenchmarkConcurrent(b *testing.B) {
	swa, _ := New(100)
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			swa.Add(float64(1))
			_ = swa.Average()
		}
	})
}