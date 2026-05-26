package skiplist_utils

import (
	"fmt"
)

// Example_basicUsage demonstrates basic skip list operations
func Example_basicUsage() {
	// Create a skip list for integer keys
	sl := NewInt[string]()

	// Insert elements
	sl.Insert(3, "three")
	sl.Insert(1, "one")
	sl.Insert(4, "four")
	sl.Insert(1, "ONE") // Update existing key

	fmt.Println("Length:", sl.Length())

	// Search
	val, found := sl.Search(1)
	fmt.Printf("Search 1: found=%v, value=%s\n", found, val)

	// Min and Max
	minKey, minVal, _ := sl.Min()
	maxKey, maxVal, _ := sl.Max()
	fmt.Printf("Min: (%d, %s)\n", minKey, minVal)
	fmt.Printf("Max: (%d, %s)\n", maxKey, maxVal)

	// Output:
	// Length: 3
	// Search 1: found=true, value=ONE
	// Min: (1, ONE)
	// Max: (4, four)
}

// Example_rangeQuery demonstrates range queries
func Example_rangeQuery() {
	sl := NewInt[string]()

	// Insert elements
	for i := 0; i < 20; i++ {
		sl.Insert(i, string(rune('a'+i)))
	}

	// Get range [5, 10]
	results := sl.Range(5, 10)
	fmt.Println("Range [5, 10]:")
	for _, r := range results {
		fmt.Printf("  %d -> %s\n", r.Key, r.Value)
	}

	// Output:
	// Range [5, 10]:
	//   5 -> f
	//   6 -> g
	//   7 -> h
	//   8 -> i
	//   9 -> j
	//   10 -> k
}

// Example_sortedIteration demonstrates sorted iteration
func Example_sortedIteration() {
	sl := NewInt[string]()

	// Insert in random order
	sl.Insert(5, "five")
	sl.Insert(2, "two")
	sl.Insert(8, "eight")
	sl.Insert(1, "one")
	sl.Insert(9, "nine")

	// Iterate in sorted order
	fmt.Println("Sorted iteration:")
	sl.ForEach(func(key int, value string) bool {
		fmt.Printf("  %d: %s\n", key, value)
		return true
	})

	// Output:
	// Sorted iteration:
	//   1: one
	//   2: two
	//   5: five
	//   8: eight
	//   9: nine
}

// Example_delete demonstrates deletion
func Example_delete() {
	sl := NewInt[string]()

	sl.Insert(1, "one")
	sl.Insert(2, "two")
	sl.Insert(3, "three")

	fmt.Println("Before delete:", sl.Length())

	deleted := sl.Delete(2)
	fmt.Println("Deleted 2:", deleted)

	_, found := sl.Search(2)
	fmt.Println("2 found:", found)

	fmt.Println("After delete:", sl.Length())

	// Output:
	// Before delete: 3
	// Deleted 2: true
	// 2 found: false
	// After delete: 2
}

// Example_customComparator demonstrates custom comparison
func Example_customComparator() {
	// Skip list for descending order
	sl := New[int, string](func(a, b int) int {
		if a > b {
			return -1
		} else if a < b {
			return 1
		}
		return 0
	})

	sl.Insert(1, "one")
	sl.Insert(5, "five")
	sl.Insert(3, "three")

	// Elements will be in descending order
	slice := sl.ToSlice()
	fmt.Println("Descending order:")
	for _, r := range slice {
		fmt.Printf("  %d: %s\n", r.Key, r.Value)
	}

	// Output:
	// Descending order:
	//   5: five
	//   3: three
	//   1: one
}

// Example_bounds demonstrates lower and upper bound operations
func Example_bounds() {
	sl := NewInt[string]()

	sl.Insert(10, "ten")
	sl.Insert(20, "twenty")
	sl.Insert(30, "thirty")
	sl.Insert(40, "forty")

	// Lower bound: first element >= key
	key, val, _ := sl.LowerBound(25)
	fmt.Printf("LowerBound(25): %d -> %s\n", key, val)

	// Upper bound: first element > key
	key, val, _ = sl.UpperBound(20)
	fmt.Printf("UpperBound(20): %d -> %s\n", key, val)

	// Output:
	// LowerBound(25): 30 -> thirty
	// UpperBound(20): 30 -> thirty
}

// Example_ranking demonstrates ranking operations
func Example_ranking() {
	sl := NewInt[string]()

	sl.Insert(100, "hundred")
	sl.Insert(200, "two-hundred")
	sl.Insert(300, "three-hundred")
	sl.Insert(400, "four-hundred")

	// Get rank of a key (0-based position in sorted order)
	rank, _ := sl.Rank(200)
	fmt.Printf("Rank of 200: %d\n", rank)

	// Get element by rank
	key, val, _ := sl.GetByRank(2)
	fmt.Printf("Element at rank 2: %d -> %s\n", key, val)

	// Output:
	// Rank of 200: 1
	// Element at rank 2: 300 -> three-hundred
}

// Example_stringKeys demonstrates string keys
func Example_stringKeys() {
	sl := NewString[int]()

	sl.Insert("banana", 1)
	sl.Insert("apple", 2)
	sl.Insert("cherry", 3)
	sl.Insert("date", 4)

	// Elements are in lexicographic order
	fmt.Println("String keys (sorted):")
	sl.ForEach(func(key string, value int) bool {
		fmt.Printf("  %s: %d\n", key, value)
		return true
	})

	// Output:
	// String keys (sorted):
	//   apple: 2
	//   banana: 1
	//   cherry: 3
	//   date: 4
}

// Example_getOrInsert demonstrates GetOrInsert
func Example_getOrInsert() {
	sl := NewInt[string]()

	// Insert new
	val := sl.GetOrInsert(1, "one")
	fmt.Printf("GetOrInsert(1, 'one'): %s\n", val)

	// Get existing (doesn't update)
	val = sl.GetOrInsert(1, "ONE")
	fmt.Printf("GetOrInsert(1, 'ONE'): %s\n", val)

	fmt.Println("Length:", sl.Length())

	// Output:
	// GetOrInsert(1, 'one'): one
	// GetOrInsert(1, 'ONE'): one
	// Length: 1
}

// Example_filtering demonstrates filtering and counting
func Example_filtering() {
	sl := NewInt[int]()

	for i := 0; i <= 20; i++ {
		sl.Insert(i, i)
	}

	// Count even numbers
	evenCount := sl.Count(func(key int, value int) bool {
		return key%2 == 0
	})
	fmt.Printf("Even numbers: %d\n", evenCount)

	// Find first number > 10
	key, _, _ := sl.FindFirst(func(k int, v int) bool {
		return k > 10
	})
	fmt.Printf("First > 10: %d\n", key)

	// Output:
	// Even numbers: 11
	// First > 10: 11
}