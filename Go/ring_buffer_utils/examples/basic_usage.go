// Example usage of ring_buffer_utils package.
// Run with: go run examples/basic_usage.go
package main

import (
	"fmt"
	"time"

	rb "github.com/ayukyo/alltoolkit/Go/ring_buffer_utils"
)

func main() {
	fmt.Println("=== Ring Buffer Utils Examples ===")
	fmt.Println()

	// 1. Basic Ring Buffer
	basicExample()
	
	// 2. Overwrite Behavior
	overwriteExample()
	
	// 3. Queue Operations
	queueExample()
	
	// 4. Numeric Ring Buffer Statistics
	numericStatsExample()
	
	// 5. Moving Average
	movingAverageExample()
	
	// 6. Thread-Safe Operations
	threadSafeExample()
	
	// 7. Sliding Window
	slidingWindowExample()
	
	// 8. Batch Processing
	batchProcessingExample()
	
	// 9. Event Log Buffer
	eventLogExample()
	
	// 10. Time Series Data
	timeSeriesExample()
}

func basicExample() {
	fmt.Println("--- Basic Ring Buffer ---")
	
	// Create a buffer with capacity 5
	buffer := rb.NewRingBuffer[int](5)
	
	// Add elements
	buffer.Push(1)
	buffer.Push(2)
	buffer.Push(3)
	buffer.Push(4)
	buffer.Push(5)
	
	fmt.Printf("Buffer capacity: %d\n", buffer.Cap())
	fmt.Printf("Buffer length: %d\n", buffer.Len())
	fmt.Printf("Is full: %v\n", buffer.IsFull())
	fmt.Printf("Contents: %v\n", buffer.ToSlice())
	fmt.Println()
}

func overwriteExample() {
	fmt.Println("--- Overwrite Behavior ---")
	
	buffer := rb.NewRingBuffer[int](3)
	
	// Fill the buffer
	buffer.Extend([]int{10, 20, 30})
	fmt.Printf("Initial: %v\n", buffer.ToSlice())
	
	// Push more elements - oldest ones get overwritten
	overwritten, wasOverwritten := buffer.Push(40)
	fmt.Printf("Overwritten: %d (occurred: %v)\n", overwritten, wasOverwritten)
	fmt.Printf("After push 40: %v\n", buffer.ToSlice())
	
	buffer.Push(50)
	fmt.Printf("After push 50: %v\n", buffer.ToSlice())
	
	buffer.Push(60)
	fmt.Printf("After push 60: %v\n", buffer.ToSlice())
	fmt.Println()
}

func queueExample() {
	fmt.Println("--- Queue Operations ---")
	
	buffer := rb.NewRingBuffer[string](4)
	
	// Add elements (enqueue)
	buffer.Extend([]string{"first", "second", "third"})
	fmt.Printf("Queue: %v\n", buffer.ToSlice())
	
	// Peek at newest and oldest
	newest, _ := buffer.Peek()
	oldest, _ := buffer.PeekLeft()
	fmt.Printf("Peek newest: %s\n", newest)
	fmt.Printf("Peek oldest: %s\n", oldest)
	
	// Remove from front (dequeue)
	front, _ := buffer.PopLeft()
	fmt.Printf("Dequeued: %s\n", front)
	fmt.Printf("Remaining: %v\n", buffer.ToSlice())
	
	// Remove from back
	back, _ := buffer.Pop()
	fmt.Printf("Popped from back: %s\n", back)
	fmt.Printf("Remaining: %v\n", buffer.ToSlice())
	fmt.Println()
}

func numericStatsExample() {
	fmt.Println("--- Numeric Ring Buffer Statistics ---")
	
	// Create numeric buffer for sensor readings
	sensorBuffer := rb.NewNumericRingBuffer(10)
	
	// Add sensor data
	readings := []float64{23.5, 24.1, 23.8, 24.5, 25.0, 24.7, 23.9, 24.2, 24.8, 25.1}
	for _, r := range readings {
		sensorBuffer.Push(r)
	}
	
	fmt.Printf("Readings: %v\n", sensorBuffer.ToSlice())
	
	// Calculate statistics
	mean, _ := sensorBuffer.Mean()
	fmt.Printf("Mean temperature: %.2f°C\n", mean)
	
	stdDev, _ := sensorBuffer.StdDev()
	fmt.Printf("Standard deviation: %.3f°C\n", stdDev)
	
	min, _ := sensorBuffer.Min()
	max, _ := sensorBuffer.Max()
	fmt.Printf("Range: %.1f°C - %.1f°C (span: %.1f°C)\n", min, max, max-min)
	
	median, _ := sensorBuffer.Median()
	fmt.Printf("Median: %.2f°C\n", median)
	
	p75, _ := sensorBuffer.Percentile(75)
	fmt.Printf("75th percentile: %.2f°C\n", p75)
	fmt.Println()
}

func movingAverageExample() {
	fmt.Println("--- Moving Average ---")
	
	// Stock price monitoring
	priceBuffer := rb.NewNumericRingBuffer(20)
	
	// Simulate stock prices
	prices := []float64{100, 102, 101, 103, 105, 104, 106, 108, 107, 109,
		110, 112, 111, 113, 115, 114, 116, 118, 117, 119}
	priceBuffer.Extend(prices)
	
	fmt.Printf("Last 20 prices: %v\n", priceBuffer.ToSlice())
	
	// 5-day moving average
	ma5, _ := priceBuffer.MovingAverage(5)
	fmt.Printf("5-day MA: %.2f (latest)\n", ma5[len(ma5)-1])
	
	// 10-day moving average
	ma10, _ := priceBuffer.MovingAverage(10)
	fmt.Printf("10-day MA: %.2f (latest)\n", ma10[len(ma10)-1])
	fmt.Println()
}

func threadSafeExample() {
	fmt.Println("--- Thread-Safe Buffer ---")
	
	// Thread-safe buffer for concurrent access
	buffer := rb.NewThreadSafeRingBuffer[int](100)
	
	// Simulate concurrent writes (in production, this would be goroutines)
	for i := 0; i < 50; i++ {
		buffer.Push(i)
	}
	
	fmt.Printf("Thread-safe buffer length: %d\n", buffer.Len())
	fmt.Printf("First 10 elements: %v\n", buffer.ToSlice()[:10])
	fmt.Println()
}

func slidingWindowExample() {
	fmt.Println("--- Sliding Window ---")
	
	// Time series data
	data := []float64{1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0}
	
	// Create sliding windows of size 4
	windows := rb.SlidingWindow(data, 4)
	
	fmt.Printf("Original data: %v\n", data)
	fmt.Println("Sliding windows (size 4):")
	for i, win := range windows {
		sum := 0.0
		for _, v := range win {
			sum += v
		}
		avg := sum / float64(len(win))
		fmt.Printf("  Window %d: %v (avg: %.2f)\n", i+1, win, avg)
	}
	fmt.Println()
}

func batchProcessingExample() {
	fmt.Println("--- Batch Processing ---")
	
	// Process large dataset in batches
	dataset := make([]int, 100)
	for i := 0; i < 100; i++ {
		dataset[i] = i + 1
	}
	
	// Process in batches of 10
	batchSums := rb.Batch(dataset, 10, func(batch []int) int {
		sum := 0
		for _, v := range batch {
			sum += v
		}
		return sum
	})
	
	fmt.Printf("Dataset: 1 to 100\n")
	fmt.Printf("Batch sums (size 10): %v\n", batchSums)
	fmt.Printf("Total sum: %d\n", func() int {
		total := 0
		for _, s := range batchSums {
			total += s
		}
		return total
	}())
	fmt.Println()
}

func eventLogExample() {
	fmt.Println("--- Event Log Buffer ---")
	
	// Buffer for recent log entries (strings)
	logBuffer := rb.NewRingBuffer[string](100)
	
	// Simulate log entries
	for i := 1; i <= 5; i++ {
		logBuffer.Push(fmt.Sprintf("Event %d: User logged in", i))
	}
	
	fmt.Printf("Recent %d log entries:\n", logBuffer.Len())
	logBuffer.ForEach(func(entry string) bool {
		fmt.Printf("  %s\n", entry)
		return true
	})
	
	// Get specific entries
	for i := 0; i < 3; i++ {
		entry, _ := logBuffer.Get(i)
		fmt.Printf("  Entry[%d]: %s\n", i, entry)
	}
	fmt.Println()
}

func timeSeriesExample() {
	fmt.Println("--- Time Series Data ---")
	
	// Monitoring system metrics
	metricsBuffer := rb.NewNumericRingBuffer(60) // 60 seconds of data
	
	// Simulate 1 minute of CPU usage data
	for i := 0; i < 60; i++ {
		// Simulate varying CPU usage
		usage := 30.0 + float64(i%10)*2.0 + float64(i/20)*5.0
		metricsBuffer.Push(usage)
	}
	
	fmt.Printf("CPU usage samples (last 60s): %v\n", func() []float64 {
		// Show last 10 samples
		slice := metricsBuffer.ToSlice()
		return slice[len(slice)-10:]
	}())
	
	// Real-time statistics
	mean, _ := metricsBuffer.Mean()
	fmt.Printf("Average CPU: %.1f%%\n", mean)
	
	max, _ := metricsBuffer.Max()
	fmt.Printf("Peak CPU: %.1f%%\n", max)
	
	// Rolling statistics
	ma5, _ := metricsBuffer.MovingAverage(5)
	fmt.Printf("Last 5-second average: %.1f%%\n", ma5[len(ma5)-1])
	
	// Percentiles
	p90, _ := metricsBuffer.Percentile(90)
	fmt.Printf("90th percentile: %.1f%%\n", p90)
	
	fmt.Println()
	
	// Demonstrate timestamp-based tracking
	fmt.Println("Timestamp tracking:")
	start := time.Now()
	
	tsBuffer := rb.NewRingBuffer[time.Time](10)
	for i := 0; i < 10; i++ {
		tsBuffer.Push(start.Add(time.Duration(i) * time.Second))
	}
	
	firstTs, _ := tsBuffer.PeekLeft()
	lastTs, _ := tsBuffer.Peek()
	fmt.Printf("Time range: %v to %v (%v duration)\n", 
		firstTs.Format("15:04:05"),
		lastTs.Format("15:04:05"),
		lastTs.Sub(firstTs))
	fmt.Println()
}