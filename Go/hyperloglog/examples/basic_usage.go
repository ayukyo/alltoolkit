// Example usage of the hyperloglog package
package main

import (
	"fmt"
	"time"

	hll "github.com/ayukyo/alltoolkit/Go/hyperloglog"
)

func main() {
	fmt.Println("=== HyperLogLog Cardinality Estimation Demo ===")
	fmt.Println()

	// Example 1: Basic usage
	basicExample()

	// Example 2: Accuracy comparison
	accuracyExample()

	// Example 3: Memory efficiency
	memoryExample()

	// Example 4: Merging multiple HyperLogLogs
	mergeExample()

	// Example 5: Serialization for storage
	serializationExample()

	// Example 6: Real-world use case - UV counting
	uvCountingExample()
}

func basicExample() {
	fmt.Println("--- Example 1: Basic Usage ---")

	// Create a new HyperLogLog with default precision (14)
	// This uses 16KB of memory
	hyperLogLog := hll.New()

	fmt.Printf("Precision: %d bits\n", hyperLogLog.Precision())
	fmt.Printf("Memory usage: %d bytes\n", hyperLogLog.MemoryUsage())
	fmt.Printf("Theoretical error rate: %.2f%%\n", hyperLogLog.ErrorRate()*100)

	// Add some elements
	elements := []string{"apple", "banana", "cherry", "apple", "banana", "date"}
	for _, elem := range elements {
		hyperLogLog.AddString(elem)
	}

	// Estimate unique count
	fmt.Printf("Added %d elements (with duplicates)\n", len(elements))
	fmt.Printf("Estimated unique count: %d\n", hyperLogLog.Estimate())
	fmt.Printf("Actual unique count: 4\n")
	fmt.Println()
}

func accuracyExample() {
	fmt.Println("--- Example 2: Accuracy Comparison ---")

	cardinalities := []int{100, 1000, 10000, 100000}

	for _, cardinality := range cardinalities {
		hyperLogLog := hll.New()

		for i := 0; i < cardinality; i++ {
			hyperLogLog.AddInt(int64(i))
		}

		estimate := hyperLogLog.Estimate()
		errorPercent := float64(int64(estimate)-int64(cardinality)) / float64(cardinality) * 100
		if errorPercent < 0 {
			errorPercent = -errorPercent
		}

		fmt.Printf("Actual: %7d | Estimated: %7d | Error: %.2f%%\n",
			cardinality, estimate, errorPercent)
	}
	fmt.Println()
}

func memoryExample() {
	fmt.Println("--- Example 3: Memory Efficiency ---")

	precisions := []uint8{4, 8, 12, 14, 16}

	fmt.Println("Precision | Memory (bytes) | Error Rate")
	fmt.Println("----------|----------------|-----------")

	for _, p := range precisions {
		hyperLogLog := hll.NewWithPrecision(p)
		memory := hyperLogLog.MemoryUsage()
		errorRate := hyperLogLog.ErrorRate() * 100

		fmt.Printf("    %2d    |     %6d     |   %.2f%%\n", p, memory, errorRate)
	}
	fmt.Println()
}

func mergeExample() {
	fmt.Println("--- Example 4: Merging HyperLogLogs ---")

	// Create three HyperLogLogs for different data sources
	hll1 := hll.New() // Users from website
	hll2 := hll.New() // Users from mobile app
	hll3 := hll.New() // Users from API

	// Add users to each source
	for i := 0; i < 1000; i++ {
		hll1.AddString(fmt.Sprintf("user_%d", i))
	}
	for i := 500; i < 1500; i++ {
		hll2.AddString(fmt.Sprintf("user_%d", i))
	}
	for i := 1000; i < 2000; i++ {
		hll3.AddString(fmt.Sprintf("user_%d", i))
	}

	fmt.Printf("Website users: ~%d\n", hll1.Estimate())
	fmt.Printf("Mobile app users: ~%d\n", hll2.Estimate())
	fmt.Printf("API users: ~%d\n", hll3.Estimate())

	// Merge all into one
	hll1.Merge(hll2)
	hll1.Merge(hll3)

	fmt.Printf("Total unique users: ~%d (actual: 2000)\n", hll1.Estimate())
	fmt.Println()
}

func serializationExample() {
	fmt.Println("--- Example 5: Serialization ---")

	// Create and populate a HyperLogLog
	hyperLogLog := hll.New()
	for i := 0; i < 10000; i++ {
		hyperLogLog.AddInt(int64(i))
	}

	// Serialize to bytes
	data := hyperLogLog.ToBytes()
	fmt.Printf("Serialized size: %d bytes\n", len(data))

	// Deserialize
	restored, ok := hll.FromBytes(data)
	if !ok {
		fmt.Println("Failed to deserialize")
		return
	}

	fmt.Printf("Original estimate: %d\n", hyperLogLog.Estimate())
	fmt.Printf("Restored estimate: %d\n", restored.Estimate())
	fmt.Println()
}

func uvCountingExample() {
	fmt.Println("--- Example 6: Real-World UV Counting ---")

	// Simulate a day of website traffic
	// Track unique visitors per hour and for the whole day

	hourlyHLLs := make([]*hll.HyperLogLog, 24)
	dailyHLL := hll.New()

	// Simulate hourly traffic
	randSeed := time.Now().UnixNano()

	for hour := 0; hour < 24; hour++ {
		hourlyHLLs[hour] = hll.New()

		// Simulate varying traffic throughout the day
		visitorsPerHour := 500 + (hour*100)%1000
		if hour >= 9 && hour <= 18 {
			visitorsPerHour *= 2 // More traffic during business hours
		}

		for i := 0; i < visitorsPerHour; i++ {
			// Simulate user ID (some users visit multiple times)
			userID := (randSeed + int64(i*hour)) % 10000
			hourlyHLLs[hour].AddInt(userID)
			dailyHLL.AddInt(userID)
		}
	}

	// Print hourly stats
	fmt.Println("Hourly UV stats:")
	for hour := 0; hour < 24; hour++ {
		if hour%6 == 0 {
			fmt.Printf("  %02d:00 - ~%d UVs\n", hour, hourlyHLLs[hour].Estimate())
		}
	}

	fmt.Printf("\nDaily total UV: ~%d\n", dailyHLL.Estimate())
	fmt.Printf("Memory used: %d bytes (vs millions for exact counting)\n", dailyHLL.MemoryUsage())
	fmt.Println()
}