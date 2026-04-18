// Package examples demonstrates usage of slice_utils package.
package main

import (
	"fmt"
	"log"
	"math/rand"
	"time"

	"github.com/ayukyo/alltoolkit/Go/slice_utils"
)

func main() {
	rand.Seed(time.Now().UnixNano())

	fmt.Println("=== slice_utils Usage Examples ===")
	fmt.Println()

	// =============================================================================
	// Basic Operations
	// =============================================================================
	fmt.Println("--- Basic Operations ---")

	numbers := []int{1, 2, 3, 4, 5}

	fmt.Printf("Contains([1,2,3,4,5], 3): %v\n", slice_utils.Contains(numbers, 3))
	fmt.Printf("Contains([1,2,3,4,5], 6): %v\n", slice_utils.Contains(numbers, 6))
	fmt.Printf("IndexOf([1,2,3,4,5], 3): %d\n", slice_utils.IndexOf(numbers, 3))
	fmt.Printf("Count([1,2,2,2,3], 2): %d\n", slice_utils.Count([]int{1, 2, 2, 2, 3}, 2))

	// =============================================================================
	// Transformation Operations
	// =============================================================================
	fmt.Println("\n--- Transformation Operations ---")

	// Map: transform elements
 doubled := slice_utils.Map(numbers, func(n int) int { return n * 2 })
	fmt.Printf("Map([1,2,3,4,5], double): %v\n", doubled)

	// Filter: select elements
	evens := slice_utils.Filter(numbers, func(n int) bool { return n%2 == 0 })
	fmt.Printf("Filter([1,2,3,4,5], even): %v\n", evens)

	// Reduce: accumulate elements
	sum := slice_utils.Reduce(numbers, 0, func(acc, n int) int { return acc + n })
	fmt.Printf("Reduce([1,2,3,4,5], sum): %d\n", sum)

	// FlatMap: map and flatten
	flatMapped := slice_utils.FlatMap(numbers, func(n int) []int { return []int{n, n * 10} })
	fmt.Printf("FlatMap([1,2,3], n->[n,n*10]): %v\n", flatMapped)

	// =============================================================================
	// Slice Manipulation
	// =============================================================================
	fmt.Println("\n--- Slice Manipulation ---")

	// Chunk: split into parts
	chunks, err := slice_utils.Chunk(numbers, 2)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Chunk([1,2,3,4,5], size=2): %v\n", chunks)

	// Reverse: reverse in place
	reversed := slice_utils.Reversed(numbers)
	fmt.Printf("Reversed([1,2,3,4,5]): %v\n", reversed)

	// Take/Drop
	fmt.Printf("Take([1,2,3,4,5], 3): %v\n", slice_utils.Take(numbers, 3))
	fmt.Printf("Drop([1,2,3,4,5], 2): %v\n", slice_utils.Drop(numbers, 2))
	fmt.Printf("TakeLast([1,2,3,4,5], 2): %v\n", slice_utils.TakeLast(numbers, 2))

	// =============================================================================
	// Set Operations
	// =============================================================================
	fmt.Println("\n--- Set Operations ---")

	a := []int{1, 2, 3}
	b := []int{3, 4, 5}

	fmt.Printf("Union([1,2,3], [3,4,5]): %v\n", slice_utils.Union(a, b))
	fmt.Printf("Intersection([1,2,3], [3,4,5]): %v\n", slice_utils.Intersection(a, b))
	fmt.Printf("Difference([1,2,3], [3,4,5]): %v\n", slice_utils.Difference(a, b))

	duplicates := []int{1, 2, 2, 3, 3, 3, 4}
	fmt.Printf("Unique([1,2,2,3,3,3,4]): %v\n", slice_utils.Unique(duplicates))

	// =============================================================================
	// Sorting and Min/Max
	// =============================================================================
	fmt.Println("\n--- Sorting and Min/Max ---")

	unsorted := []int{5, 2, 8, 1, 9}
	sorted := slice_utils.SortedBy(unsorted, func(n int) int { return n })
	fmt.Printf("SortedBy([5,2,8,1,9]): %v\n", sorted)

	min, _ := slice_utils.Min(numbers)
	max, _ := slice_utils.Max(numbers)
	fmt.Printf("Min([1,2,3,4,5]): %d\n", min)
	fmt.Printf("Max([1,2,3,4,5]): %d\n", max)

	// Sort custom type
	people := []Person{
		{"Alice", 30},
		{"Bob", 25},
		{"Charlie", 35},
	}
	slice_utils.SortBy(people, func(p Person) int { return p.Age })
	fmt.Printf("SortBy(people, age): %v\n", people)

	// =============================================================================
	// Search Operations
	// =============================================================================
	fmt.Println("\n--- Search Operations ---")

	// Find
	found, ok := slice_utils.Find(numbers, func(n int) bool { return n > 3 })
	if ok {
		fmt.Printf("Find(>3): %d\n", found)
	}

	// FindIndex
	idx := slice_utils.FindIndex(numbers, func(n int) bool { return n > 3 })
	fmt.Printf("FindIndex(>3): %d\n", idx)

	// Every/Some
	fmt.Printf("Every([2,4,6], even): %v\n", slice_utils.Every([]int{2, 4, 6}, func(n int) bool { return n%2 == 0 }))
	fmt.Printf("Some([1,3,5,6], even): %v\n", slice_utils.Some([]int{1, 3, 5, 6}, func(n int) bool { return n%2 == 0 }))

	// =============================================================================
	// Partition and Grouping
	// =============================================================================
	fmt.Println("\n--- Partition and Grouping ---")

	// Partition
	even, odd := slice_utils.Partition(numbers, func(n int) bool { return n%2 == 0 })
	fmt.Printf("Partition([1,2,3,4,5]): even=%v, odd=%v\n", even, odd)

	// GroupBy
	groups := slice_utils.GroupBy(numbers, func(n int) int { return n % 2 })
	fmt.Printf("GroupBy([1,2,3,4,5], n%%2): 0=%v, 1=%v\n", groups[0], groups[1])

	// =============================================================================
	// Insert, Remove, Replace
	// =============================================================================
	fmt.Println("\n--- Insert, Remove, Replace ---")

	// Insert
	inserted, _ := slice_utils.Insert(numbers, 2, 10)
	fmt.Printf("Insert([1,2,3,4,5], index=2, 10): %v\n", inserted)

	// Remove
	removed, _ := slice_utils.Remove(numbers, 2)
	fmt.Printf("Remove([1,2,3,4,5], index=2): %v\n", removed)

	// RemoveFirst
	fmt.Printf("RemoveFirst([1,2,2,3], 2): %v\n", slice_utils.RemoveFirst([]int{1, 2, 2, 3}, 2))

	// Replace
	replaced, _ := slice_utils.Replace(numbers, 1, 100)
	fmt.Printf("Replace([1,2,3,4,5], index=1, 100): %v\n", replaced)

	// =============================================================================
	// Shuffling and Sampling
	// =============================================================================
	fmt.Println("\n--- Shuffling and Sampling ---")

	// Shuffled
	shuffled := slice_utils.Shuffled(numbers)
	fmt.Printf("Shuffled([1,2,3,4,5]): %v\n", shuffled)

	// Sample
	sample, _ := slice_utils.Sample(numbers, 3)
	fmt.Printf("Sample([1,2,3,4,5], 3): %v\n", sample)

	// RandomElement
	random, _ := slice_utils.RandomElement(numbers)
	fmt.Printf("RandomElement([1,2,3,4,5]): %d\n", random)

	// =============================================================================
	// Utility Functions
	// =============================================================================
	fmt.Println("\n--- Utility Functions ---")

	// Clone
	cloned := slice_utils.Clone(numbers)
	fmt.Printf("Clone([1,2,3,4,5]): %v\n", cloned)

	// Concat
	concatenated := slice_utils.Concat([]int{1, 2}, []int{3, 4}, []int{5})
	fmt.Printf("Concat([1,2], [3,4], [5]): %v\n", concatenated)

	// Repeat
	repeated, _ := slice_utils.Repeat(7, 3)
	fmt.Printf("Repeat(7, 3): %v\n", repeated)

	// Range
	fmt.Printf("Range(1, 6): %v\n", slice_utils.Range(1, 6))
	rangeWithStep, _ := slice_utils.RangeWithStep(0, 10, 2)
	fmt.Printf("RangeWithStep(0, 10, 2): %v\n", rangeWithStep)

	// First/Last
	first, _ := slice_utils.First(numbers)
	last, _ := slice_utils.Last(numbers)
	fmt.Printf("First([1,2,3,4,5]): %d\n", first)
	fmt.Printf("Last([1,2,3,4,5]): %d\n", last)

	// Nth (supports negative index)
	nth, _ := slice_utils.Nth(numbers, -1)
	fmt.Printf("Nth([1,2,3,4,5], -1): %d\n", nth)

	// =============================================================================
	// Statistics
	// =============================================================================
	fmt.Println("\n--- Statistics ---")

	data := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	fmt.Printf("Sum([1..10]): %d\n", slice_utils.Sum(data))
	fmt.Printf("Product([1,2,3,4]): %d\n", slice_utils.Product([]int{1, 2, 3, 4}))
	avg, _ := slice_utils.Average(data)
	fmt.Printf("Average([1..10]): %.2f\n", avg)
	median, _ := slice_utils.Median(data)
	fmt.Printf("Median([1..10]): %d\n", median)
	mode, _ := slice_utils.Mode([]int{1, 2, 2, 3, 3, 3, 4})
	fmt.Printf("Mode([1,2,2,3,3,3,4]): %d\n", mode)

	// =============================================================================
	// Zip and Unzip
	// =============================================================================
	fmt.Println("\n--- Zip and Unzip ---")

	keys := []int{1, 2, 3}
	values := []string{"one", "two", "three"}

	pairs, _ := slice_utils.Zip(keys, values)
	fmt.Printf("Zip([1,2,3], [one,two,three]): %v\n", pairs)

	// Unzip
	k, v := slice_utils.Unzip(pairs)
	fmt.Printf("Unzip: keys=%v, values=%v\n", k, v)

	// ZipWith: add two slices
	slice1 := []int{1, 2, 3}
	slice2 := []int{10, 20, 30}
	added, _ := slice_utils.ZipWith(slice1, slice2, func(a, b int) int { return a + b })
	fmt.Printf("ZipWith([1,2,3], [10,20,30], add): %v\n", added)

	// =============================================================================
	// Practical Examples
	// =============================================================================
	fmt.Println("\n--- Practical Examples ---")

	// Example 1: Processing a list of users
	users := []User{
		{ID: 1, Name: "Alice", Active: true},
		{ID: 2, Name: "Bob", Active: false},
		{ID: 3, Name: "Charlie", Active: true},
		{ID: 4, Name: "Diana", Active: true},
	}

	// Get active user names
	activeNames := slice_utils.Map(
		slice_utils.Filter(users, func(u User) bool { return u.Active }),
		func(u User) string { return u.Name },
	)
	fmt.Printf("Active user names: %v\n", activeNames)

	// Find user by ID
	user, found := slice_utils.Find(users, func(u User) bool { return u.ID == 3 })
	if found {
		fmt.Printf("Found user with ID 3: %s\n", user.Name)
	}

	// Group users by active status
	groupedByActive := slice_utils.GroupBy(users, func(u User) bool { return u.Active })
	fmt.Printf("Active users count: %d, Inactive users count: %d\n",
		len(groupedByActive[true]), len(groupedByActive[false]))

	// Example 2: Working with paginated data
	allItems := slice_utils.Range(1, 101) // 1 to 100
	pageSize := 20
	page1, _ := slice_utils.Chunk(allItems, pageSize)
	fmt.Printf("Page 1 of items (first 20): %v\n", page1[0][:5])

	// Example 3: Deduplication with custom key
	items := []Item{
		{Name: "apple", Category: "fruit"},
		{Name: "banana", Category: "fruit"},
		{Name: "carrot", Category: "vegetable"},
		{Name: "apple", Category: "fruit"}, // duplicate
	}
	uniqueItems := slice_utils.UniqueBy(items, func(i Item) string { return i.Name })
	fmt.Printf("Unique items by name: %d items\n", len(uniqueItems))

	// Example 4: Batch processing
	batchSize := 25
	batches, _ := slice_utils.Chunk(allItems, batchSize)
	fmt.Printf("Total batches: %d\n", len(batches))

	fmt.Println("\n=== Examples Complete ===")
}

// Custom types for examples
type Person struct {
	Name string
	Age  int
}

type User struct {
	ID     int
	Name   string
	Active bool
}

type Item struct {
	Name     string
	Category string
}