package main

import (
	"fmt"
	"time"

	lfu "github.com/AllToolkit/Go/lfu_cache_utils"
)

func main() {
	fmt.Println("LFU Cache Utilities - Usage Examples")
	fmt.Println("=====================================")
	fmt.Println()

	// Basic Usage
	fmt.Println("1. Basic Usage")
	fmt.Println("--------------")

	cache := lfu.New(3)

	cache.Set("apple", 1)
	cache.Set("banana", 2)
	cache.Set("cherry", 3)

	v, ok := cache.Get("apple")
	fmt.Printf("Get(apple): %v, ok=%v\n", v, ok)
	fmt.Println()

	// Frequency Tracking
	fmt.Println("2. Frequency Tracking")
	fmt.Println("--------------------")

	cache2 := lfu.New(3)
	cache2.Set("a", 1)
	cache2.Set("b", 2)
	cache2.Set("c", 3)

	cache2.Get("a")
	cache2.Get("a")
	cache2.Get("b")

	freqA, _ := cache2.Frequency("a")
	freqB, _ := cache2.Frequency("b")
	freqC, _ := cache2.Frequency("c")

	fmt.Printf("Frequency(a): %d\n", freqA)
	fmt.Printf("Frequency(b): %d\n", freqB)
	fmt.Printf("Frequency(c): %d\n", freqC)
	fmt.Println()

	// Eviction Demo
	fmt.Println("3. Eviction Demo")
	fmt.Println("---------------")

	cache3 := lfu.New(2)
	cache3.Set("x", 1)
	cache3.Set("y", 2)
	cache3.Get("x") // access x
	cache3.Set("z", 3) // should evict y (least used)

	fmt.Printf("Contains(x): %v\n", cache3.Contains("x"))
	fmt.Printf("Contains(y): %v (evicted)\n", cache3.Contains("y"))
	fmt.Printf("Contains(z): %v\n", cache3.Contains("z"))
	fmt.Println()

	// TTL Support
	fmt.Println("4. TTL Support")
	fmt.Println("--------------")

	cache4 := lfu.NewWithTTL(3, 100*time.Millisecond)
	cache4.Set("expire", 1)

	fmt.Printf("Before TTL: Contains(expire)=%v\n", cache4.Contains("expire"))
	time.Sleep(150 * time.Millisecond)
	fmt.Printf("After TTL:  Contains(expire)=%v\n", cache4.Contains("expire"))
	fmt.Println()

	// Eviction Callback
	fmt.Println("5. Eviction Callback")
	fmt.Println("-------------------")

	evicted := make(map[string]interface{})
	callback := func(key string, value interface{}) {
		evicted[key] = value
		fmt.Printf("  Evicted: key=%s, value=%v\n", key, value)
	}

	cache5 := lfu.NewWithEvict(2, callback)
	cache5.Set("a", 1)
	cache5.Set("b", 2)
	cache5.Set("c", 3) // will evict "a"
	fmt.Println()

	// Stats
	fmt.Println("6. Cache Statistics")
	fmt.Println("-------------------")

	cache6 := lfu.New(3)
	cache6.Set("one", 1)
	cache6.Set("two", 2)
	cache6.Get("one")
	cache6.Get("one")
	cache6.Get("two")

	stats := cache6.Stats()
	fmt.Printf("Capacity: %v\n", stats["capacity"])
	fmt.Printf("Size: %v\n", stats["size"])
	fmt.Printf("Min Freq: %v\n", stats["min_frequency"])
	fmt.Printf("Max Freq: %v\n", stats["max_frequency"])
	fmt.Println()

	// Batch Operations
	fmt.Println("7. Batch Operations")
	fmt.Println("-------------------")

	cache7 := lfu.New(5)
	items := map[string]interface{}{
		"k1": 1,
		"k2": 2,
		"k3": 3,
	}
	cache7.SetMulti(items)

	results := cache7.GetMulti([]string{"k1", "k2", "k3"})
	fmt.Printf("GetMulti: %v\n", results)
	fmt.Println()

	fmt.Println("All examples completed!")
}
