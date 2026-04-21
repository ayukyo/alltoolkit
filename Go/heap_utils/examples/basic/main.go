// Example: Basic heap operations with MinHeap and MaxHeap
package main

import (
	"fmt"
	heap_utils "github.com/ayukyo/alltoolkit/Go/heap_utils"
)

func main() {
	fmt.Println("=== MinHeap Example ===")
	
	// Create a min-heap
	minHeap := heap_utils.NewMinHeap(5, 3, 8, 1, 9, 2)
	
	fmt.Printf("Heap size: %d\n", minHeap.Len())
	
	// Peek at minimum
	if top, ok := minHeap.Peek(); ok {
		fmt.Printf("Minimum element: %d\n", top)
	}
	
	// Pop elements in sorted order
	fmt.Print("Elements in ascending order: ")
	for !minHeap.IsEmpty() {
		fmt.Printf("%d ", minHeap.Pop())
	}
	fmt.Println()
	
	fmt.Println("\n=== MaxHeap Example ===")
	
	// Create a max-heap
	maxHeap := heap_utils.NewMaxHeap(5, 3, 8, 1, 9, 2)
	
	// Peek at maximum
	if top, ok := maxHeap.Peek(); ok {
		fmt.Printf("Maximum element: %d\n", top)
	}
	
	// Pop elements in descending order
	fmt.Print("Elements in descending order: ")
	for !maxHeap.IsEmpty() {
		fmt.Printf("%d ", maxHeap.Pop())
	}
	fmt.Println()
	
	fmt.Println("\n=== String Heap Example ===")
	
	// Min-heap with strings (lexicographic order)
	strHeap := heap_utils.NewMinHeap("cherry", "apple", "banana", "date")
	
	fmt.Print("Strings in alphabetical order: ")
	for !strHeap.IsEmpty() {
		fmt.Printf("%s ", strHeap.Pop())
	}
	fmt.Println()
}