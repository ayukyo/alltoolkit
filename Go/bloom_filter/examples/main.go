// Example usage of the bloom_filter package
package main

import (
	"fmt"
	"math/rand"
	"time"

	bloom "github.com/ayukyo/alltoolkit/Go/bloom_filter"
)

func main() {
	fmt.Println("=== Bloom Filter Examples ===\n")

	// Example 1: Basic usage
	basicExample()

	// Example 2: Auto-optimized configuration
	configExample()

	// Example 3: Serialization
	serializationExample()

	// Example 4: Set operations
	setOperationsExample()

	// Example 5: Performance demonstration
	performanceExample()
}

func basicExample() {
	fmt.Println("--- Example 1: Basic Usage ---")

	// Create a bloom filter with size 10000 and 7 hash functions
	bf := bloom.New(10000, 7)

	// Add some items
	bf.AddString("apple")
	bf.AddString("banana")
	bf.AddString("cherry")

	// Check if items exist
	fmt.Printf("'apple' exists: %v\n", bf.ContainsString("apple"))
	fmt.Printf("'banana' exists: %v\n", bf.ContainsString("banana"))
	fmt.Printf("'grape' exists: %v\n", bf.ContainsString("grape"))

	// Get stats
	fmt.Printf("\nStats: %s\n\n", bf.String())
}

func configExample() {
	fmt.Println("--- Example 2: Auto-Optimized Configuration ---")

	// Create a bloom filter optimized for 1 million items with 0.1% false positive rate
	bf := bloom.NewWithConfig(bloom.Config{
		ExpectedItems:     1000000,
		FalsePositiveRate: 0.001,
	})

	fmt.Printf("Size: %d bits (~%.2f MB)\n", bf.Size(), float64(bf.Size())/(8*1024*1024))
	fmt.Printf("Hash functions: %d\n", bf.HashCount())

	// Add some items
	for i := 0; i < 10000; i++ {
		bf.AddString(fmt.Sprintf("user-%d", i))
	}

	stats := bf.Stats()
	fmt.Printf("Items added: %d\n", stats.ItemCount)
	fmt.Printf("Fill ratio: %.4f%%\n", stats.FillRatio*100)
	fmt.Printf("Expected FP rate: %.6f%%\n\n", stats.ExpectedFP*100)
}

func serializationExample() {
	fmt.Println("--- Example 3: Serialization ---")

	// Create and populate a filter
	original := bloom.NewWithConfig(bloom.Config{
		ExpectedItems:     1000,
		FalsePositiveRate: 0.01,
	})

	// Add some data
	items := []string{"item1", "item2", "item3", "item4", "item5"}
	for _, item := range items {
		original.AddString(item)
	}

	// Export to JSON
	jsonStr, err := original.ToJSON()
	if err != nil {
		fmt.Printf("Error exporting: %v\n", err)
		return
	}
	fmt.Printf("Exported JSON length: %d bytes\n", len(jsonStr))

	// Import from JSON
	imported, err := bloom.FromJSON(jsonStr)
	if err != nil {
		fmt.Printf("Error importing: %v\n", err)
		return
	}

	// Verify items still exist
	fmt.Println("Verifying imported filter:")
	for _, item := range items {
		if imported.ContainsString(item) {
			fmt.Printf("  ✓ '%s' found\n", item)
		} else {
			fmt.Printf("  ✗ '%s' NOT found (error!)\n", item)
		}
	}
	fmt.Println()
}

func setOperationsExample() {
	fmt.Println("--- Example 4: Set Operations ---")

	bf1 := bloom.New(5000, 5)
	bf2 := bloom.New(5000, 5)

	// Populate filters
	bf1.AddString("apple")
	bf1.AddString("banana")
	bf1.AddString("cherry")

	bf2.AddString("banana")
	bf2.AddString("cherry")
	bf2.AddString("date")
	bf2.AddString("elderberry")

	// Union
	union, _ := bf1.Union(bf2)
	fmt.Println("Union contains:")
	for _, fruit := range []string{"apple", "banana", "cherry", "date", "elderberry"} {
		if union.ContainsString(fruit) {
			fmt.Printf("  ✓ %s\n", fruit)
		}
	}

	// Intersection
	intersect, _ := bf1.Intersect(bf2)
	fmt.Println("\nIntersection contains:")
	for _, fruit := range []string{"apple", "banana", "cherry", "date", "elderberry"} {
		if intersect.ContainsString(fruit) {
			fmt.Printf("  ✓ %s\n", fruit)
		}
	}
	fmt.Println()
}

func performanceExample() {
	fmt.Println("--- Example 5: Performance Demonstration ---")

	// Create a large filter
	bf := bloom.NewWithConfig(bloom.Config{
		ExpectedItems:     1000000,
		FalsePositiveRate: 0.01,
	})

	// Measure add time
	start := time.Now()
	for i := 0; i < 100000; i++ {
		bf.AddString(fmt.Sprintf("item-%d", i))
	}
	addDuration := time.Since(start)

	fmt.Printf("Added 100,000 items in %v (%.2f μs/item)\n", addDuration, float64(addDuration.Microseconds())/100000)

	// Measure contains time
	start = time.Now()
	for i := 0; i < 100000; i++ {
		bf.ContainsString(fmt.Sprintf("item-%d", i))
	}
	containsDuration := time.Since(start)

	fmt.Printf("Checked 100,000 items in %v (%.2f μs/item)\n", containsDuration, float64(containsDuration.Microseconds())/100000)

	// Measure false positive rate
	rand.Seed(time.Now().UnixNano())
	fpCount := 0
	testCount := 100000
	for i := 0; i < testCount; i++ {
		// Test with items that were NOT added
		if bf.ContainsString(fmt.Sprintf("not-added-%d", rand.Int())) {
			fpCount++
		}
	}

	fmt.Printf("False positive rate: %.4f%% (expected: ~1%%)\n", float64(fpCount)/float64(testCount)*100)
	fmt.Printf("Memory used: ~%.2f MB\n", float64(bf.Size())/(8*1024*1024))
}