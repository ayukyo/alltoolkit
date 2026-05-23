// Example demonstrating LFU Cache usage
package main

import (
	"fmt"
	"time"

	"github.com/ayukyo/alltoolkit/Go/lfu_cache_utils"
)

func main() {
	fmt.Println("=== LFU Cache Examples ===\n")

	// Example 1: Basic Usage
	basicExample()

	// Example 2: Eviction Policy
	evictionExample()

	// Example 3: TTL (Time-to-Live)
	ttlExample()

	// Example 4: Statistics
	statsExample()

	// Example 5: GetOrSet and GetOrCompute
	computeExample()

	// Example 6: Custom Types
	customTypesExample()
}

func basicExample() {
	fmt.Println("--- Basic Usage ---")

	// Create a cache with capacity 3
	cache := lfu_cache_utils.New[string, int](3)

	// Add items
	cache.Put("apple", 1)
	cache.Put("banana", 2)
	cache.Put("cherry", 3)

	// Get items
	if v, ok := cache.Get("apple"); ok {
		fmt.Printf("Got 'apple': %d\n", v)
	}

	// Update existing item
	cache.Put("apple", 10)
	if v, ok := cache.Get("apple"); ok {
		fmt.Printf("Updated 'apple': %d\n", v)
	}

	// Check existence
	fmt.Printf("Contains 'banana': %v\n", cache.Contains("banana"))
	fmt.Printf("Contains 'grape': %v\n", cache.Contains("grape"))

	// Delete item
	cache.Delete("banana")
	fmt.Printf("After delete, contains 'banana': %v\n", cache.Contains("banana"))

	fmt.Println()
}

func evictionExample() {
	fmt.Println("--- Eviction Policy ---")

	cache := lfu_cache_utils.New[string, string](3)

	// Add 3 items
	cache.Put("A", "first")
	cache.Put("B", "second")
	cache.Put("C", "third")

	fmt.Println("Added: A, B, C")

	// Access items to increase their frequency
	cache.Get("A")
	cache.Get("A")
	cache.Get("B")

	fmt.Println("Accessed: A twice, B once, C zero times")

	// Add new item - should evict C (lowest frequency)
	cache.Put("D", "fourth")

	fmt.Println("Added D (triggers eviction)")
	fmt.Printf("Contains 'A': %v (freq: highest)\n", cache.Contains("A"))
	fmt.Printf("Contains 'B': %v (freq: medium)\n", cache.Contains("B"))
	fmt.Printf("Contains 'C': %v (evicted - lowest freq)\n", cache.Contains("C"))
	fmt.Printf("Contains 'D': %v (new item)\n", cache.Contains("D"))

	fmt.Println()
}

func ttlExample() {
	fmt.Println("--- TTL (Time-to-Live) ---")

	// Create cache with TTL
	cache := lfu_cache_utils.NewWithConfig[string, string](lfu_cache_utils.Config{
		Capacity: 10,
		TTL:      2 * time.Second,
	})

	cache.Put("temp", "I'll expire soon")
	fmt.Println("Added 'temp' with 2s TTL")

	// Check immediately
	if _, ok := cache.Get("temp"); ok {
		fmt.Println("'temp' is present (immediately)")
	}

	// Wait for expiration
	time.Sleep(2100 * time.Millisecond)

	if _, ok := cache.Get("temp"); ok {
		fmt.Println("'temp' is still present")
	} else {
		fmt.Println("'temp' has expired")
	}

	// Per-item TTL
	cache.PutWithTTL("custom", "Custom TTL", 5*time.Second)
	fmt.Println("Added 'custom' with 5s TTL")

	fmt.Println()
}

func statsExample() {
	fmt.Println("--- Statistics ---")

	cache := lfu_cache_utils.New[string, int](100)

	// Add items
	for i := 0; i < 50; i++ {
		key := fmt.Sprintf("key-%d", i)
		cache.Put(key, i)
	}

	// Generate some hits and misses
	for i := 0; i < 40; i++ {
		cache.Get(fmt.Sprintf("key-%d", i)) // hits
	}
	for i := 50; i < 60; i++ {
		cache.Get(fmt.Sprintf("key-%d", i)) // misses
	}

	stats := cache.Stats()
	fmt.Printf("Capacity: %d\n", stats.Capacity)
	fmt.Printf("Size: %d\n", stats.Size)
	fmt.Printf("Hits: %d\n", stats.Hits)
	fmt.Printf("Misses: %d\n", stats.Misses)
	fmt.Printf("Hit Rate: %.2f%%\n", stats.HitRate*100)
	fmt.Printf("Evictions: %d\n", stats.Evictions)
	fmt.Printf("Cache: %s\n", cache.String())

	fmt.Println()
}

func computeExample() {
	fmt.Println("--- GetOrSet and GetOrCompute ---")

	cache := lfu_cache_utils.New[string, int](10)

	// GetOrSet: Get existing or set new value
	v1, found1 := cache.GetOrSet("key1", 42)
	fmt.Printf("GetOrSet (new): value=%d, found=%v\n", v1, found1)

	v2, found2 := cache.GetOrSet("key1", 100)
	fmt.Printf("GetOrSet (existing): value=%d, found=%v\n", v2, found2)

	// GetOrCompute: Get existing or compute new value
	computeCount := 0
	v3, found3 := cache.GetOrCompute("key2", func() int {
		computeCount++
		return 999
	})
	fmt.Printf("GetOrCompute (new): value=%d, found=%v, computed=%d time(s)\n", v3, found3, computeCount)

	v4, found4 := cache.GetOrCompute("key2", func() int {
		computeCount++
		return 1111
	})
	fmt.Printf("GetOrCompute (existing): value=%d, found=%v, computed=%d time(s)\n", v4, found4, computeCount)

	fmt.Println()
}

func customTypesExample() {
	fmt.Println("--- Custom Types ---")

	type User struct {
		ID   int
		Name string
	}

	cache := lfu_cache_utils.New[int, User](10)

	// Store custom struct
	cache.Put(1, User{ID: 1, Name: "Alice"})
	cache.Put(2, User{ID: 2, Name: "Bob"})

	// Retrieve custom struct
	if user, ok := cache.Get(1); ok {
		fmt.Printf("User: ID=%d, Name=%s\n", user.ID, user.Name)
	}

	// Iterate over all users
	fmt.Println("All users:")
	cache.ForEach(func(id int, user User) bool {
		fmt.Printf("  %d: %s\n", id, user.Name)
		return true
	})

	// Export to JSON
	json, err := cache.ToJSON()
	if err != nil {
		fmt.Printf("Error exporting: %v\n", err)
	} else {
		fmt.Printf("JSON export: %s\n", json)
	}

	fmt.Println()
}