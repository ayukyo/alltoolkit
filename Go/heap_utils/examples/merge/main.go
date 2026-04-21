// Example: Merge multiple sorted sequences efficiently
package main

import (
	"fmt"
	heap_utils "github.com/ayukyo/alltoolkit/Go/heap_utils"
)

func main() {
	fmt.Println("=== Merge K Sorted Arrays ===")
	
	// Multiple sorted arrays
	sorted1 := []int{1, 4, 7, 10}
	sorted2 := []int{2, 5, 8, 11}
	sorted3 := []int{3, 6, 9, 12}
	
	fmt.Printf("Array 1: %v\n", sorted1)
	fmt.Printf("Array 2: %v\n", sorted2)
	fmt.Printf("Array 3: %v\n", sorted3)
	
	// Merge all arrays
	merged := heap_utils.MergeKSorted(sorted1, sorted2, sorted3)
	fmt.Printf("Merged: %v\n", merged)
	
	fmt.Println("\n=== Merge with Different Sizes ===")
	
	small1 := []int{1, 10, 100}
	small2 := []int{2}
	small3 := []int{3, 4, 5, 6, 7, 8, 9}
	
	result := heap_utils.MergeKSorted(small1, small2, small3)
	fmt.Printf("Merged: %v\n", result)
	
	fmt.Println("\n=== Merge String Arrays ===")
	
	names1 := []string{"Alice", "Charlie", "Eve"}
	names2 := []string{"Bob", "David"}
	names3 := []string{"Frank", "Grace", "Henry", "Ivy"}
	
	mergedNames := heap_utils.MergeKSorted(names1, names2, names3)
	fmt.Printf("Merged names: %v\n", mergedNames)
	
	fmt.Println("\n=== External Merge Sort Scenario ===")
	
	// Simulating external merge sort: 4 sorted runs
	run1 := []int{10, 30, 50, 70}
	run2 := []int{20, 40, 60, 80}
	run3 := []int{15, 35, 55, 75}
	run4 := []int{25, 45, 65, 85}
	
	finalSorted := heap_utils.MergeKSorted(run1, run2, run3, run4)
	fmt.Printf("External merge result: %v\n", finalSorted)
	
	fmt.Println("\n=== Time Complexity ===")
	fmt.Println("MergeKSorted: O(n log k) where n = total elements, k = number of arrays")
	fmt.Println("Much faster than naive O(n*k) merge for large k")
}