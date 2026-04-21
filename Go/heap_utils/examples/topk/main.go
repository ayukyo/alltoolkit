// Example: TopK and BottomK for finding extreme values
package main

import (
	"fmt"
	heap_utils "github.com/ayukyo/alltoolkit/Go/heap_utils"
)

func main() {
	fmt.Println("=== TopK: Find K Largest Elements ===")
	
	scores := []int{85, 92, 78, 95, 88, 72, 91, 83, 77, 90, 85}
	
	fmt.Printf("All scores: %v\n", scores)
	
	// Find top 3 scores
	top3 := heap_utils.TopK(scores, 3)
	fmt.Printf("Top 3 scores: %v\n", top3)
	
	// Find top 5 scores
	top5 := heap_utils.TopK(scores, 5)
	fmt.Printf("Top 5 scores: %v\n", top5)
	
	fmt.Println("\n=== BottomK: Find K Smallest Elements ===")
	
	// Find bottom 3 scores
	bottom3 := heap_utils.BottomK(scores, 3)
	fmt.Printf("Bottom 3 scores: %v\n", bottom3)
	
	// Find bottom 5 scores
	bottom5 := heap_utils.BottomK(scores, 5)
	fmt.Printf("Bottom 5 scores: %v\n", bottom5)
	
	fmt.Println("\n=== Nth Element: Find Rank ===")
	
	// Find 3rd smallest (3rd lowest score)
	thirdSmallest, ok := heap_utils.NthSmallest(scores, 3)
	if ok {
		fmt.Printf("3rd lowest score: %d\n", thirdSmallest)
	}
	
	// Find 2nd largest score
	secondLargest, ok := heap_utils.NthLargest(scores, 2)
	if ok {
		fmt.Printf("2nd highest score: %d\n", secondLargest)
	}
	
	// Find median
	median, ok := heap_utils.Median(scores)
	if ok {
		fmt.Printf("Median score: %d\n", median)
	}
	
	fmt.Println("\n=== Performance Note ===")
	fmt.Println("TopK/BottomK use O(n log k) time, O(k) space")
	fmt.Println("Much more efficient than sorting entire array for small k")
}