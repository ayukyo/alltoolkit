package sliding_window_average_test

import (
	"fmt"
	"time"

	"github.com/ayukyo/alltoolkit/sliding_window_average"
)

// Example_basic demonstrates basic usage of SlidingWindowAverage
func Example_basic() {
	// Create a sliding window of size 5
	swa, _ := sliding_window_average.New(5)

	// Add some values
	swa.Add(10)
	swa.Add(20)
	swa.Add(30)
	swa.Add(40)
	swa.Add(50)

	fmt.Printf("Count: %d\n", swa.Count())
	fmt.Printf("Sum: %.1f\n", swa.Sum())
	fmt.Printf("Average: %.1f\n", swa.Average())
	fmt.Printf("Min: %.1f\n", swa.Min())
	fmt.Printf("Max: %.1f\n", swa.Max())
	fmt.Printf("IsFull: %v\n", swa.IsFull())

	// Output:
	// Count: 5
	// Sum: 150.0
	// Average: 30.0
	// Min: 10.0
	// Max: 50.0
	// IsFull: true
}

// Example_slidingWindow demonstrates the sliding behavior
func Example_slidingWindow() {
	swa, _ := sliding_window_average.New(3)

	// Add 3 values
	swa.Add(10)
	swa.Add(20)
	swa.Add(30)
	fmt.Printf("Average: %.1f\n", swa.Average())

	// Add one more - oldest (10) is removed
	swa.Add(40)
	fmt.Printf("Average after adding 40: %.1f\n", swa.Average())
	fmt.Printf("Values: %v\n", swa.Values())

	// Output:
	// Average: 20.0
	// Average after adding 40: 30.0
	// Values: [20 30 40]
}

// Example_statistics demonstrates statistical functions
func Example_statistics() {
	swa, _ := sliding_window_average.New(10)

	// Add values 1-10
	for i := 1; i <= 10; i++ {
		swa.Add(float64(i))
	}

	fmt.Printf("Average: %.1f\n", swa.Average())
	fmt.Printf("Variance: %.2f\n", swa.Variance())
	fmt.Printf("StdDev: %.2f\n", swa.StdDev())
	fmt.Printf("Median: %.1f\n", swa.Median())
	fmt.Printf("P95: %.1f\n", swa.Percentile(95))

	// Output:
	// Average: 5.5
	// Variance: 8.25
	// StdDev: 2.87
	// Median: 5.5
	// P95: 9.5
}

// Example_getStats demonstrates getting all statistics at once
func Example_getStats() {
	swa, _ := sliding_window_average.New(5)

	for i := 1; i <= 5; i++ {
		swa.Add(float64(i))
	}

	stats := swa.GetStats()
	fmt.Printf("Count: %d\n", stats.Count)
	fmt.Printf("Average: %.1f\n", stats.Average)
	fmt.Printf("Min: %.1f\n", stats.Min)
	fmt.Printf("Max: %.1f\n", stats.Max)
	fmt.Printf("StdDev: %.2f\n", stats.StdDev)

	// Output:
	// Count: 5
	// Average: 3.0
	// Min: 1.0
	// Max: 5.0
	// StdDev: 1.41
}

// Example_rateTracking demonstrates rate calculation with timestamps
func Example_rateTracking() {
	// Create with timestamp tracking
	swa, _ := sliding_window_average.NewWithTimestamps(10)

	// Simulate receiving values over time
	values := []float64{10, 15, 20, 25, 30}
	now := time.Now()

	for i, v := range values {
		// Add with simulated timestamp
		swa.AddWithTimestamp(v, now.Add(time.Duration(i)*time.Second))
	}

	// Rate is sum / duration
	fmt.Printf("Total sum: %.1f\n", swa.Sum())
	fmt.Printf("Duration: 4 seconds\n")
	fmt.Printf("Rate: %.2f values/second\n", swa.Rate())

	// Output:
	// Total sum: 100.0
	// Duration: 4 seconds
	// Rate: 25.00 values/second
}

// Example_concurrent demonstrates thread-safe usage
func Example_concurrent() {
	swa, _ := sliding_window_average.New(100)

	// Simulate concurrent writes and reads
	done := make(chan bool)

	// Writer goroutine
	go func() {
		for i := 0; i < 1000; i++ {
			swa.Add(float64(i % 100))
		}
		done <- true
	}()

	// Reader goroutine
	go func() {
		for i := 0; i < 100; i++ {
			_ = swa.Average()
			time.Sleep(time.Millisecond)
		}
		done <- true
	}()

	// Wait for completion
	<-done
	<-done

	fmt.Printf("Final count: %d\n", swa.Count())

	// Output:
	// Final count: 100
}

// Example_clear demonstrates clearing the window
func Example_clear() {
	swa, _ := sliding_window_average.New(5)

	for i := 1; i <= 5; i++ {
		swa.Add(float64(i))
	}

	fmt.Printf("Before clear: Count=%d, Average=%.1f\n", swa.Count(), swa.Average())

	swa.Clear()

	fmt.Printf("After clear: Count=%d, IsFull=%v\n", swa.Count(), swa.IsFull())

	// Output:
	// Before clear: Count=5, Average=3.0
	// After clear: Count=0, IsFull=false
}

// Example_percentiles demonstrates various percentile calculations
func Example_percentiles() {
	swa, _ := sliding_window_average.New(100)

	// Add values 1-100
	for i := 1; i <= 100; i++ {
		swa.Add(float64(i))
	}

	fmt.Printf("P50 (Median): %.1f\n", swa.Percentile(50))
	fmt.Printf("P95: %.1f\n", swa.Percentile(95))
	fmt.Printf("P99: %.1f\n", swa.Percentile(99))

	// Output:
	// P50 (Median): 50.5
	// P95: 95.0
	// P99: 99.0
}