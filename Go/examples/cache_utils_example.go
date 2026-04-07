package main

import (
	"fmt"
	"sync"
	"time"

	"github.com/ayukyo/alltoolkit/Go/cache_utils"
)

func main() {
	fmt.Println("=== Go Cache Utilities Example ===\n")

	// Example 1: Basic cache operations
	fmt.Println("1. Basic Cache Operations")
	fmt.Println("-------------------------")
	basicOperations()

	// Example 2: TTL (Time To Live)
	fmt.Println("\n2. TTL (Time To Live)")
	fmt.Println("---------------------")
	ttlExample()

	// Example 3: LRU Eviction
	fmt.Println("\n3. LRU Eviction Policy")
	fmt.Println("----------------------")
	lruEvictionExample()

	// Example 4: GetOrCompute (Lazy Loading)
	fmt.Println("\n4. GetOrCompute (Lazy Loading)")
	fmt.Println("-------------------------------")
	getOrComputeExample()

	// Example 5: Cache Statistics
	fmt.Println("\n5. Cache Statistics")
	fmt.Println("-------------------")
	statisticsExample()

	// Example 6: Eviction Callback
	fmt.Println("\n6. Eviction Callback")
	fmt.Println("--------------------")
	evictionCallbackExample()

	// Example 7: Advanced Operations
	fmt.Println("\n7. Advanced Operations")
	fmt.Println("----------------------")
	advancedOperationsExample()

	// Example 8: Different Types
	fmt.Println("\n8. Generic Type Support")
	fmt.Println("-----------------------")
	genericTypesExample()

	// Example 9: Concurrent Access
	fmt.Println("\n9. Concurrent Access")
	fmt.Println("--------------------")
	concurrentAccessExample()
}

func basicOperations() {
	// Create a cache with capacity of 100 items
	cache := cache_utils.NewCache[string, int](100)

	// Set values
	cache.Set("user:1", 42, 0)
	cache.Set("user:2", 100, 0)

	// Get values
	if val, ok := cache.Get("user:1"); ok {
		fmt.Printf("user:1 = %d\n", val)
	}

	// Check if key exists
	if cache.Has("user:2") {
		fmt.Println("user:2 exists in cache")
	}

	// Delete a key
	cache.Delete("user:1")
	if _, ok := cache.Get("user:1"); !ok {
		fmt.Println("user:1 has been deleted")
	}

	// Get cache size
	fmt.Printf("Cache size: %d\n", cache.Len())
	fmt.Printf("Cache capacity: %d\n", cache.Capacity())
}

func ttlExample() {
	cache := cache_utils.NewCache[string, string](10)

	// Set with 2 second TTL
	cache.Set("session:123", "active", 2*time.Second)

	// Should exist immediately
	if val, ok := cache.Get("session:123"); ok {
		fmt.Printf("Session found: %s\n", val)
	}

	// Wait for expiration
	fmt.Println("Waiting for expiration...")
	time.Sleep(3 * time.Second)

	// Should be expired now
	if _, ok := cache.Get("session:123"); !ok {
		fmt.Println("Session has expired (expected)")
	}

	// Set without TTL (never expires)
	cache.Set("config:api_key", "secret123", 0)
	fmt.Printf("Config (no TTL): %s\n", func() string {
		v, _ := cache.Get("config:api_key")
		return v
	}())
}

func lruEvictionExample() {
	// Create cache with capacity of 3
	cache := cache_utils.NewCache[string, int](3)

	// Add 3 items
	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)
	cache.Set("c", 3, 0)

	fmt.Println("Added items: a, b, c")

	// Access 'a' to make it most recently used
	cache.Get("a")
	fmt.Println("Accessed 'a' (now most recently used)")

	// Add new item, should evict 'b' (least recently used)
	cache.Set("d", 4, 0)
	fmt.Println("Added item 'd'")

	// Check which items exist
	fmt.Printf("'a' exists: %v (expected: true)\n", cache.Has("a"))
	fmt.Printf("'b' exists: %v (expected: false - evicted)\n", cache.Has("b"))
	fmt.Printf("'c' exists: %v (expected: true)\n", cache.Has("c"))
	fmt.Printf("'d' exists: %v (expected: true)\n", cache.Has("d"))
}

func getOrComputeExample() {
	cache := cache_utils.NewCache[string, int](10)

	computeCount := 0

	// Expensive computation function
	expensiveCompute := func() int {
		computeCount++
		fmt.Printf("  (Computing value... call #%d)\n", computeCount)
		time.Sleep(100 * time.Millisecond) // Simulate work
		return 42
	}

	// First call - will compute
	fmt.Println("First GetOrCompute call:")
	val := cache.GetOrCompute("key1", expensiveCompute, 5*time.Second)
	fmt.Printf("Result: %d\n", val)

	// Second call - will use cached value
	fmt.Println("\nSecond GetOrCompute call (should use cache):")
	val = cache.GetOrCompute("key1", expensiveCompute, 5*time.Second)
	fmt.Printf("Result: %d\n", val)

	fmt.Printf("\nTotal computations: %d (expected: 1)\n", computeCount)
}

func statisticsExample() {
	cache := cache_utils.NewCache[string, int](10)

	// Perform some operations
	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)

	cache.Get("a") // hit
	cache.Get("b") // hit
	cache.Get("c") // miss
	cache.Get("d") // miss

	// Get statistics
	stats := cache.Stats()
	fmt.Printf("Hits: %d\n", stats.Hits)
	fmt.Printf("Misses: %d\n", stats.Misses)
	fmt.Printf("Hit Rate: %.2f%%\n", stats.HitRate()*100)
	fmt.Printf("Size: %d / %d\n", stats.Size, stats.Capacity)

	// Reset statistics
	cache.ResetStats()
	stats = cache.Stats()
	fmt.Printf("\nAfter reset - Hits: %d, Misses: %d\n", stats.Hits, stats.Misses)
}

func evictionCallbackExample() {
	cache := cache_utils.NewCache[string, int](3)

	// Set up eviction callback
	cache.SetEvictionCallback(func(key string, value int) {
		fmt.Printf("  [Callback] Evicted: %s = %d\n", key, value)
	})

	fmt.Println("Adding items to trigger eviction:")
	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)
	cache.Set("c", 3, 0)
	fmt.Println("Added: a, b, c")

	cache.Set("d", 4, 0)
	fmt.Println("Added: d (should evict 'a')")

	cache.Set("e", 5, 0)
	fmt.Println("Added: e (should evict 'b')")
}

func advancedOperationsExample() {
	cache := cache_utils.NewCache[string, int](10)

	// Add some items
	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)
	cache.Set("c", 3, 0)

	// Peek (get without updating LRU)
	val, _ := cache.Peek("a")
	fmt.Printf("Peek 'a': %d\n", val)

	// Update value
	updated := cache.Update("a", 100)
	fmt.Printf("Updated 'a': %v, new value: %d\n", updated, func() int {
		v, _ := cache.Get("a")
		return v
	}())

	// Update TTL
	cache.UpdateTTL("b", 5*time.Minute)
	fmt.Println("Updated TTL for 'b' to 5 minutes")

	// Get all keys
	keys := cache.Keys()
	fmt.Printf("All keys: %v\n", keys)

	// Get all items
	items := cache.Items()
	fmt.Printf("All items: %v\n", items)

	// Filter items
	filtered := cache.Filter(func(key string, value int) bool {
		return value > 1
	})
	fmt.Printf("Filtered (value > 1): %v\n", filtered)

	// Find item
	key, val, found := cache.Find(func(k string, v int) bool {
		return v == 100
	})
	fmt.Printf("Found item with value 100: key=%s, val=%d, found=%v\n", key, val, found)

	// Count matching items
	count := cache.Count(func(k string, v int) bool {
		return v >= 2
	})
	fmt.Printf("Count of items with value >= 2: %d\n", count)

	// ForEach iteration
	fmt.Println("Iterating with ForEach:")
	cache.ForEach(func(key string, value int) bool {
		fmt.Printf("  %s = %d\n", key, value)
		return true // continue iteration
	})
}

func genericTypesExample() {
	// Cache with string keys and struct values
	type User struct {
		ID    int
		Name  string
		Email string
	}

	userCache := cache_utils.NewCache[string, User](10)

	userCache.Set("user:1", User{ID: 1, Name: "Alice", Email: "alice@example.com"}, 0)
	userCache.Set("user:2", User{ID: 2, Name: "Bob", Email: "bob@example.com"}, 0)

	if user, ok := userCache.Get("user:1"); ok {
		fmt.Printf("User: %+v\n", user)
	}

	// Cache with int keys and string values
	stringCache := cache_utils.NewCache[int, string](10)
	stringCache.Set(1, "one", 0)
	stringCache.Set(2, "two", 0)
	stringCache.Set(3, "three", 0)

	if str, ok := stringCache.Get(2); ok {
		fmt.Printf("String value for key 2: %s\n", str)
	}
}

func concurrentAccessExample() {
	cache := cache_utils.NewCache[int, int](100)

	fmt.Println("Performing concurrent operations...")

	// Simulate concurrent writes
	done := make(chan bool, 10)
	for i := 0; i < 10; i++ {
		go func(id int) {
			for j := 0; j < 100; j++ {
				cache.Set(id*100+j, j, 0)
			}
			done <- true
		}(i)
	}

	// Wait for all goroutines
	for i := 0; i < 10; i++ {
		<-done
	}

	fmt.Printf("Cache size after concurrent writes: %d\n", cache.Len())

	// Simulate concurrent reads
	readCount := 0
	var mu sync.Mutex
	for i := 0; i < 10; i++ {
		go func(id int) {
			for j := 0; j < 100; j++ {
				if _, ok := cache.Get(id*100 + j); ok {
					mu.Lock()
					readCount++
					mu.Unlock()
				}
			}
			done <- true
		}(i)
	}

	// Wait for all reads
	for i := 0; i < 10; i++ {
		<-done
	}

	fmt.Printf("Successful reads: %d\n", readCount)
	fmt.Println("Concurrent access completed without race conditions!")
}