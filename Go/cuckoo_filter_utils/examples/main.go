// Example usage of cuckoo_filter_utils
package main

import (
	"fmt"
	"math/rand"
	"time"

	cuckoo "github.com/ayukyo/alltoolkit/Go/cuckoo_filter_utils"
)

func main() {
	fmt.Println("=== Cuckoo Filter Examples ===")
	fmt.Println()

	// Example 1: Basic usage
	exampleBasic()

	// Example 2: Custom configuration
	exampleCustomConfig()

	// Example 3: Statistics
	exampleStats()

	// Example 4: Clone and merge
	exampleCloneMerge()

	// Example 5: False positive rate measurement
	exampleFalsePositiveRate()

	// Example 6: Large scale test
	exampleLargeScale()

	// Example 7: URL deduplication simulation
	exampleURLDeduplication()

	// Example 8: Cache simulation
	exampleCacheSimulation()

	// Example 9: Fingerprint operations
	exampleFingerprintOps()

	// Example 10: Stress test
	exampleStressTest()
}

func exampleBasic() {
	fmt.Println("--- Example 1: Basic Usage ---")

	cf, err := cuckoo.New(cuckoo.DefaultOptions(100))
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Add items
	items := []string{"apple", "banana", "cherry", "date", "elderberry"}
	for _, item := range items {
		cf.Add([]byte(item))
		fmt.Printf("Added: %s\n", item)
	}

	// Check membership
	fmt.Println("\nMembership checks:")
	for _, item := range items {
		fmt.Printf("  Contains '%s': %v\n", item, cf.Contains([]byte(item)))
	}

	// Check non-existent items
	fmt.Println("\nNon-existent items:")
	fmt.Printf("  Contains 'grape': %v\n", cf.Contains([]byte("grape")))
	fmt.Printf("  Contains 'fig': %v\n", cf.Contains([]byte("fig")))

	// Remove an item
	cf.Remove([]byte("banana"))
	fmt.Printf("\nAfter removing 'banana': Contains 'banana': %v\n", cf.Contains([]byte("banana")))

	fmt.Println()
}

func exampleCustomConfig() {
	fmt.Println("--- Example 2: Custom Configuration ---")

	opts := cuckoo.Options{
		Capacity:          1000,
		FalsePositiveRate: 0.001, // Very low FP rate
		BucketSize:        4,
		MaxKicks:          500,
	}

	cf, err := cuckoo.New(opts)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	fmt.Printf("Configuration:\n")
	fmt.Printf("  Capacity: %d\n", opts.Capacity)
	fmt.Printf("  False Positive Rate: %.4f\n", opts.FalsePositiveRate)
	fmt.Printf("  Bucket Size: %d\n", opts.BucketSize)
	fmt.Printf("  Max Kicks: %d\n", opts.MaxKicks)

	fmt.Printf("\nFilter details:\n")
	fmt.Printf("  Fingerprint bits: %d\n", cf.fpBits)
	fmt.Printf("  Number of buckets: %d\n", cf.numBuckets)
	fmt.Printf("  Memory size: %d bytes\n", cf.Size())

	// Add some items
	for i := 0; i < 500; i++ {
		cf.Add([]byte(fmt.Sprintf("item_%d", i)))
	}

	fmt.Printf("  Items added: %d\n", cf.Count())
	fmt.Printf("  Load factor: %.2f\n", cf.LoadFactor())
	fmt.Println()
}

func exampleStats() {
	fmt.Println("--- Example 3: Statistics ---")

	cf, _ := cuckoo.New(cuckoo.DefaultOptions(10000))

	// Add items
	for i := 0; i < 5000; i++ {
		cf.Add([]byte(fmt.Sprintf("data_%d", i)))
	}

	stats := cf.GetStats()
	fmt.Printf("Filter Statistics:\n")
	fmt.Printf("  Count: %d items\n", stats.Count)
	fmt.Printf("  Capacity: %d slots\n", stats.Capacity)
	fmt.Printf("  Load Factor: %.2f%%\n", stats.LoadFactor*100)
	fmt.Printf("  Expected FP Rate: %.4f (%.2f%%)\n", stats.FalsePositiveRate, stats.FalsePositiveRate*100)
	fmt.Printf("  Fingerprint Bits: %d\n", stats.FingerprintBits)
	fmt.Printf("  Bucket Size: %d\n", stats.BucketSize)
	fmt.Printf("  Number of Buckets: %d\n", stats.NumBuckets)
	fmt.Printf("  Memory Usage: %d bytes\n", stats.MemoryBytes)
	fmt.Println()
}

func exampleCloneMerge() {
	fmt.Println("--- Example 4: Clone and Merge ---")

	// Create first filter
	cf1, _ := cuckoo.New(cuckoo.DefaultOptions(100))
	cf1.Add([]byte("shared"))
	cf1.Add([]byte("cf1_unique"))

	// Clone it
	clone := cf1.Clone()
	clone.Add([]byte("clone_unique"))

	fmt.Println("Clone test:")
	fmt.Printf("  Original contains 'clone_unique': %v\n", cf1.Contains([]byte("clone_unique")))
	fmt.Printf("  Clone contains 'clone_unique': %v\n", clone.Contains([]byte("clone_unique")))

	// Create second filter for merge
	cf2, _ := cuckoo.New(cuckoo.DefaultOptions(100))
	cf2.Add([]byte("shared"))
	cf2.Add([]byte("cf2_unique"))

	// Merge
	merged, err := cf1.Merge(cf2)
	if err != nil {
		fmt.Printf("Merge error: %v\n", err)
	} else {
		fmt.Println("\nMerge test:")
		fmt.Printf("  Merged contains 'shared': %v\n", merged.Contains([]byte("shared")))
		fmt.Printf("  Merged contains 'cf1_unique': %v\n", merged.Contains([]byte("cf1_unique")))
		fmt.Printf("  Merged contains 'cf2_unique': %v\n", merged.Contains([]byte("cf2_unique")))
		fmt.Printf("  Merged count: %d\n", merged.Count())
	}
	fmt.Println()
}

func exampleFalsePositiveRate() {
	fmt.Println("--- Example 5: False Positive Rate Measurement ---")

	opts := cuckoo.Options{
		Capacity:          10000,
		FalsePositiveRate: 0.01,
		BucketSize:        4,
	}

	cf, _ := cuckoo.New(opts)

	// Add items
	addedCount := 5000
	for i := 0; i < addedCount; i++ {
		cf.Add([]byte(fmt.Sprintf("added_%d", i)))
	}

	// Test false positives with items that weren't added
	testCount := 10000
	falsePositives := 0
	for i := 0; i < testCount; i++ {
		if cf.Contains([]byte(fmt.Sprintf("test_%d", i))) {
			falsePositives++
		}
	}

	actualRate := float64(falsePositives) / float64(testCount)
	fmt.Printf("False Positive Measurement:\n")
	fmt.Printf("  Added items: %d\n", addedCount)
	fmt.Printf("  Test queries: %d\n", testCount)
	fmt.Printf("  False positives: %d\n", falsePositives)
	fmt.Printf("  Actual FP rate: %.4f (%.2f%%)\n", actualRate, actualRate*100)
	fmt.Printf("  Expected FP rate: %.4f (%.2f%%)\n", opts.FalsePositiveRate, opts.FalsePositiveRate*100)
	fmt.Println()
}

func exampleLargeScale() {
	fmt.Println("--- Example 6: Large Scale Test ---")

	cf, _ := cuckoo.New(cuckoo.DefaultOptions(100000))

	// Add many items
	itemsAdded := 0
	for i := 0; i < 50000; i++ {
		if err := cf.Add([]byte(fmt.Sprintf("large_%d", i))); err == nil {
			itemsAdded++
		}
	}

	fmt.Printf("Large Scale Results:\n")
	fmt.Printf("  Attempted to add: 50000\n")
	fmt.Printf("  Successfully added: %d\n", itemsAdded)
	fmt.Printf("  Filter count: %d\n", cf.Count())
	fmt.Printf("  Capacity: %d\n", cf.Capacity())
	fmt.Printf("  Load factor: %.2f\n", cf.LoadFactor())

	// Verify no false negatives
	falseNegatives := 0
	for i := 0; i < itemsAdded; i++ {
		if !cf.Contains([]byte(fmt.Sprintf("large_%d", i))) {
			falseNegatives++
		}
	}
	fmt.Printf("  False negatives: %d (should be 0)\n", falseNegatives)
	fmt.Println()
}

func exampleURLDeduplication() {
	fmt.Println("--- Example 7: URL Deduplication Simulation ---")

	// Simulate a crawler checking if URLs were already visited
	cf, _ := cuckoo.New(cuckoo.DefaultOptions(1000))

	urls := []string{
		"https://example.com/page1",
		"https://example.com/page2",
		"https://example.com/page3",
		"https://test.com/article",
		"https://blog.com/post",
	}

	visitedCount := 0
	for _, url := range urls {
		if !cf.Contains([]byte(url)) {
			cf.Add([]byte(url))
			fmt.Printf("Visited: %s\n", url)
			visitedCount++
		} else {
			fmt.Printf("Already visited (skip): %s\n", url)
		}
	}

	// Try to visit same URLs again
	fmt.Println("\nSecond pass:")
	skippedCount := 0
	for _, url := range urls {
		if cf.Contains([]byte(url)) {
			fmt.Printf("Skip (already visited): %s\n", url)
			skippedCount++
		}
	}

	fmt.Printf("\nSummary: Visited %d, Skipped %d\n", visitedCount, skippedCount)
	fmt.Println()
}

func exampleCacheSimulation() {
	fmt.Println("--- Example 8: Cache Simulation ---")

	cf, _ := cuckoo.New(cuckoo.DefaultOptions(100))

	// Simulate cache entries
	cacheKeys := []string{"user:123", "user:456", "product:789", "session:abc"}

	fmt.Println("Adding cache entries:")
	for _, key := range cacheKeys {
		cf.Add([]byte(key))
		fmt.Printf("  Cached: %s\n", key)
	}

	// Check cache on subsequent requests
	fmt.Println("\nCache lookups:")
	requests := []string{"user:123", "user:999", "product:789", "product:000"}
	for _, key := range requests {
		if cf.Contains([]byte(key)) {
			fmt.Printf("  HIT: %s\n", key)
		} else {
			fmt.Printf("  MISS: %s\n", key)
		}
	}

	// Evict an entry
	fmt.Println("\nEvicting 'user:123':")
	cf.Remove([]byte("user:123"))
	if cf.Contains([]byte("user:123")) {
		fmt.Println("  Still in cache (unexpected)")
	} else {
		fmt.Println("  Removed from cache")
	}
	fmt.Println()
}

func exampleFingerprintOps() {
	fmt.Println("--- Example 9: Fingerprint Operations ---")

	cf, _ := cuckoo.New(cuckoo.DefaultOptions(100))

	// Work with fingerprints directly
	fmt.Println("Direct fingerprint operations:")

	// Add some fingerprints
	fps := []uint8{10, 20, 30, 42, 99}
	for _, fp := range fps {
		cf.AddWithFingerprint(fp)
		fmt.Printf("  Added fingerprint: %d\n", fp)
	}

	// Check fingerprints
	fmt.Println("\nFingerprint checks:")
	for _, fp := range fps {
		fmt.Printf("  Contains fp %d: %v\n", fp, cf.ContainsFingerprint(fp))
	}
	fmt.Printf("  Contains fp 255: %v\n", cf.ContainsFingerprint(255))

	// Remove a fingerprint
	cf.RemoveFingerprint(42)
	fmt.Printf("\nAfter removing fp 42: Contains fp 42: %v\n", cf.ContainsFingerprint(42))

	// Iterate over all fingerprints
	fmt.Println("\nAll fingerprints in filter:")
	cf.ForEach(func(fp uint8) {
		fmt.Printf("  Fingerprint: %d\n", fp)
	})
	fmt.Println()
}

func exampleStressTest() {
	fmt.Println("--- Example 10: Stress Test ---")

	cf, _ := cuckoo.New(cuckoo.Options{
		Capacity:   5000,
		BucketSize: 4,
		MaxKicks:   1000,
	})

	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	operations := 10000

	adds := 0
	removes := 0
	lookups := 0
	fullErrors := 0

	start := time.Now()

	for i := 0; i < operations; i++ {
		item := []byte(fmt.Sprintf("stress_%d", r.Intn(1000)))

		switch i % 4 {
		case 0:
			if err := cf.Add(item); err == nil {
				adds++
			} else if err == cuckoo.ErrFilterFull {
				fullErrors++
			}
		case 1:
			cf.Contains(item)
			lookups++
		case 2:
			if cf.Remove(item) {
				removes++
			}
		case 3:
			cf.Contains(item)
			lookups++
		}
	}

	duration := time.Since(start)

	fmt.Printf("Stress Test Results:\n")
	fmt.Printf("  Total operations: %d\n", operations)
	fmt.Printf("  Adds: %d\n", adds)
	fmt.Printf("  Removes: %d\n", removes)
	fmt.Printf("  Lookups: %d\n", lookups)
	fmt.Printf("  Filter full errors: %d\n", fullErrors)
	fmt.Printf("  Duration: %v\n", duration)
	fmt.Printf("  Ops/sec: %.0f\n", float64(operations)/duration.Seconds())
	fmt.Printf("  Final count: %d\n", cf.Count())
	fmt.Printf("  Final load factor: %.2f\n", cf.LoadFactor())
	fmt.Println()
}