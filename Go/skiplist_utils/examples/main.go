// Skip List Utilities - Example Main Program
//
// Run this example with: go run main.go
package main

import (
	"fmt"
	"time"

	skiplist "github.com/ayukyo/alltoolkit/Go/skiplist_utils"
)

func main() {
	fmt.Println("=== Skip List Demo ===\n")

	// Basic operations
	fmt.Println("--- Basic Operations ---")
	sl := skiplist.NewInt[string]()

	sl.Insert(5, "five")
	sl.Insert(2, "two")
	sl.Insert(8, "eight")
	sl.Insert(1, "one")
	sl.Insert(9, "nine")

	fmt.Printf("Length: %d\n", sl.Length())
	fmt.Printf("Level: %d\n", sl.Level())

	val, found := sl.Search(5)
	fmt.Printf("Search 5: found=%v, value=%s\n", found, val)

	_, found = sl.Search(99)
	fmt.Printf("Search 99: found=%v\n", found)

	// Min and Max
	minKey, minVal, _ := sl.Min()
	maxKey, maxVal, _ := sl.Max()
	fmt.Printf("Min: (%d, %s)\n", minKey, minVal)
	fmt.Printf("Max: (%d, %s)\n", maxKey, maxVal)

	// Sorted iteration
	fmt.Println("\n--- Sorted Iteration ---")
	sl.ForEach(func(key int, value string) bool {
		fmt.Printf("  %d -> %s\n", key, value)
		return true
	})

	// Range query
	fmt.Println("\n--- Range Query [3, 7] ---")
	sl.Insert(3, "three")
	sl.Insert(7, "seven")
	sl.Insert(6, "six")
	results := sl.Range(3, 7)
	for _, r := range results {
		fmt.Printf("  %d -> %s\n", r.Key, r.Value)
	}

	// Bounds
	fmt.Println("\n--- Lower/Upper Bounds ---")
	key, val, _ := sl.LowerBound(4)
	fmt.Printf("LowerBound(4): %d -> %s\n", key, val)

	key, val, _ = sl.UpperBound(5)
	fmt.Printf("UpperBound(5): %d -> %s\n", key, val)

	// Ranking
	fmt.Println("\n--- Ranking ---")
	rank, _ := sl.Rank(5)
	fmt.Printf("Rank of 5: %d\n", rank)

	key, val, _ = sl.GetByRank(0)
	fmt.Printf("Element at rank 0: %d -> %s\n", key, val)

	// String keys
	fmt.Println("\n--- String Keys ---")
	slStr := skiplist.NewString[int]()
	slStr.Insert("banana", 1)
	slStr.Insert("apple", 2)
	slStr.Insert("cherry", 3)

	slice := slStr.ToSlice()
	for _, r := range slice {
		fmt.Printf("  %s: %d\n", r.Key, r.Value)
	}

	// Performance test
	fmt.Println("\n--- Performance Test ---")
	slPerf := skiplist.NewInt[int]()

	start := time.Now()
	for i := 0; i < 100000; i++ {
		slPerf.Insert(i, i*10)
	}
	insertTime := time.Since(start)

	start = time.Now()
	for i := 0; i < 100000; i++ {
		slPerf.Search(i)
	}
	searchTime := time.Since(start)

	start = time.Now()
	for i := 0; i < 50000; i++ {
		slPerf.Delete(i)
	}
	deleteTime := time.Since(start)

	fmt.Printf("Insert 100,000: %v\n", insertTime)
	fmt.Printf("Search 100,000: %v\n", searchTime)
	fmt.Printf("Delete 50,000: %v\n", deleteTime)
	fmt.Printf("Final length: %d\n", slPerf.Length())

	// GetOrInsert demo
	fmt.Println("\n--- GetOrInsert Demo ---")
	slGet := skiplist.NewInt[string]()
	val = slGet.GetOrInsert(1, "one")
	fmt.Printf("GetOrInsert(1, 'one'): %s\n", val)
	val = slGet.GetOrInsert(1, "ONE")
	fmt.Printf("GetOrInsert(1, 'ONE'): %s (returns existing)\n", val)
	fmt.Printf("Length: %d\n", slGet.Length())

	// Filtering demo
	fmt.Println("\n--- Filtering Demo ---")
	slFilter := skiplist.NewInt[int]()
	for i := 0; i <= 20; i++ {
		slFilter.Insert(i, i)
	}

	evenCount := slFilter.Count(func(key int, value int) bool {
		return key%2 == 0
	})
	fmt.Printf("Even numbers in 0-20: %d\n", evenCount)

	key, val, _ = slFilter.FindFirst(func(k int, v int) bool {
		return k > 15
	})
	fmt.Printf("First key > 15: %d\n", key)
}