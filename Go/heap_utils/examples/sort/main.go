// Example: Heap Sort implementation
package main

import (
	"fmt"
	heap_utils "github.com/ayukyo/alltoolkit/Go/heap_utils"
)

func main() {
	fmt.Println("=== Heap Sort: Ascending Order ===")
	
	data := []int{64, 34, 25, 12, 22, 11, 90}
	fmt.Printf("Original: %v\n", data)
	
	sorted := heap_utils.HeapSort(data)
	fmt.Printf("Sorted (ascending): %v\n", sorted)
	
	fmt.Println("\n=== Heap Sort: Descending Order ===")
	
	descending := heap_utils.HeapSortDesc(data)
	fmt.Printf("Sorted (descending): %v\n", descending)
	
	fmt.Println("\n=== Original Unmodified ===")
	fmt.Printf("Original array still: %v\n", data)
	
	fmt.Println("\n=== String Sorting ===")
	
	fruits := []string{"banana", "apple", "cherry", "date", "elderberry"}
	fmt.Printf("Original: %v\n", fruits)
	
	sortedFruits := heap_utils.HeapSort(fruits)
	fmt.Printf("Sorted: %v\n", sortedFruits)
	
	fmt.Println("\n=== Time Complexity ===")
	fmt.Println("Heap Sort: O(n log n) worst, average, and best case")
	fmt.Println("Space: O(n) for this implementation (creates new array)")
}