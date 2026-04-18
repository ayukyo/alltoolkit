// Package main demonstrates usage of the red_black_tree package
package main

import (
	"fmt"
	"github.com/ayukyo/alltoolkit/go/red_black_tree"
)

func main() {
	fmt.Println("=== Red-Black Tree Usage Examples ===\n")

	// Example 1: Basic Integer Tree
	basicExample()

	// Example 2: String Tree
	stringExample()

	// Example 3: Range Queries
	rangeQueryExample()

	// Example 4: Custom Comparator
	customComparatorExample()

	// Example 5: Traversal Methods
	traversalExample()

	// Example 6: LowerBound and UpperBound
	boundsExample()

	// Example 7: Large Dataset Performance
	performanceExample()
}

func basicExample() {
	fmt.Println("--- Example 1: Basic Integer Tree ---")

	// Create a new Red-Black Tree for integers
	tree := red_black_tree.NewInt()

	// Insert elements
	fmt.Println("Inserting: 7, 3, 9, 1, 5, 8, 10")
	tree.Insert(7)
	tree.Insert(3)
	tree.Insert(9)
	tree.Insert(1)
	tree.Insert(5)
	tree.Insert(8)
	tree.Insert(10)

	fmt.Printf("Tree size: %d\n", tree.Size())
	fmt.Printf("In-order traversal: %v\n", tree.InOrder())

	// Search
	fmt.Printf("Contains 5: %v\n", tree.Contains(5))
	fmt.Printf("Contains 100: %v\n", tree.Contains(100))

	// Min and Max
	min, _ := tree.Min()
	max, _ := tree.Max()
	fmt.Printf("Min: %d, Max: %d\n", min, max)

	// Delete
	fmt.Println("\nDeleting 5...")
	tree.Delete(5)
	fmt.Printf("In-order after deletion: %v\n", tree.InOrder())

	// Validate
	if err := tree.Validate(); err != nil {
		fmt.Printf("Validation error: %v\n", err)
	} else {
		fmt.Println("Tree is valid ✓")
	}

	fmt.Println()
}

func stringExample() {
	fmt.Println("--- Example 2: String Tree ---")

	// Create a new Red-Black Tree for strings
	tree := red_black_tree.NewString()

	// Insert strings
	words := []string{"banana", "apple", "cherry", "date", "elderberry"}
	fmt.Printf("Inserting: %v\n", words)
	for _, word := range words {
		tree.Insert(word)
	}

	fmt.Printf("Sorted order: %v\n", tree.InOrder())

	// Search
	fmt.Printf("Contains 'cherry': %v\n", tree.Contains("cherry"))
	fmt.Printf("Contains 'grape': %v\n", tree.Contains("grape"))

	// Min and Max
	min, _ := tree.Min()
	max, _ := tree.Max()
	fmt.Printf("Alphabetically first: %s, last: %s\n", min, max)

	fmt.Println()
}

func rangeQueryExample() {
	fmt.Println("--- Example 3: Range Queries ---")

	tree := red_black_tree.NewInt()

	// Insert numbers 1-20
	for i := 1; i <= 20; i++ {
		tree.Insert(i)
	}

	fmt.Printf("Tree contains: %v\n", tree.ToSlice())

	// Range query
	fmt.Printf("Range [5, 10]: %v\n", tree.Range(5, 10))
	fmt.Printf("Range [15, 20]: %v\n", tree.Range(15, 20))
	fmt.Printf("Count in range [5, 15]: %d\n", tree.Count(5, 15))

	fmt.Println()
}

func customComparatorExample() {
	fmt.Println("--- Example 4: Custom Comparator ---")

	// Create a tree with descending order
	tree := red_black_tree.New(func(a, b int) int {
		if a > b {
			return -1 // a comes before b
		} else if a < b {
			return 1 // a comes after b
		}
		return 0
	})

	numbers := []int{1, 5, 3, 9, 2, 8}
	fmt.Printf("Inserting (with descending order): %v\n", numbers)
	for _, n := range numbers {
		tree.Insert(n)
	}

	fmt.Printf("Sorted (descending): %v\n", tree.InOrder())

	// Min and Max are reversed in this case
	min, _ := tree.Min()
	max, _ := tree.Max()
	fmt.Printf("First (largest): %d, Last (smallest): %d\n", min, max)

	fmt.Println()
}

func traversalExample() {
	fmt.Println("--- Example 5: Traversal Methods ---")

	tree := red_black_tree.NewInt()
	tree.FromSlice([]int{5, 3, 7, 1, 9, 2, 8})

	fmt.Printf("Inserted: [5, 3, 7, 1, 9, 2, 8]\n")
	fmt.Printf("In-order (sorted): %v\n", tree.InOrder())
	fmt.Printf("Pre-order (root first): %v\n", tree.PreOrder())
	fmt.Printf("Post-order (root last): %v\n", tree.PostOrder())

	// ForEach iteration
	fmt.Print("ForEach iteration: ")
	tree.ForEach(func(key int) bool {
		fmt.Printf("%d ", key)
		return true
	})
	fmt.Println()

	// Early termination with ForEach
	fmt.Print("ForEach (stop at 5): ")
	tree.ForEach(func(key int) bool {
		fmt.Printf("%d ", key)
		return key < 5
	})
	fmt.Println()

	fmt.Println()
}

func boundsExample() {
	fmt.Println("--- Example 6: LowerBound and UpperBound ---")

	tree := red_black_tree.NewInt()
	tree.FromSlice([]int{1, 3, 5, 7, 9})

	fmt.Printf("Tree: %v\n", tree.InOrder())

	// LowerBound: first element >= target
	fmt.Println("\nLowerBound examples:")
	for _, target := range []int{0, 1, 4, 5, 9, 10} {
		if result, found := tree.LowerBound(target); found {
			fmt.Printf("  LowerBound(%d) = %d\n", target, result)
		} else {
			fmt.Printf("  LowerBound(%d) = not found\n", target)
		}
	}

	// UpperBound: first element > target
	fmt.Println("\nUpperBound examples:")
	for _, target := range []int{0, 1, 4, 5, 9, 10} {
		if result, found := tree.UpperBound(target); found {
			fmt.Printf("  UpperBound(%d) = %d\n", target, result)
		} else {
			fmt.Printf("  UpperBound(%d) = not found\n", target)
		}
	}

	fmt.Println()
}

func performanceExample() {
	fmt.Println("--- Example 7: Large Dataset Performance ---")

	tree := red_black_tree.NewInt()
	n := 10000

	fmt.Printf("Inserting %d elements...\n", n)
	for i := 0; i < n; i++ {
		tree.Insert(i)
	}

	fmt.Printf("Size: %d\n", tree.Size())
	fmt.Printf("Height: %d (optimal for %d elements: ~%d)\n", 
		tree.Height(), n, log2(n))

	// Validate the tree
	if err := tree.Validate(); err != nil {
		fmt.Printf("Validation error: %v\n", err)
	} else {
		fmt.Println("Tree validation: ✓")
	}

	// Delete half
	fmt.Printf("\nDeleting %d elements...\n", n/2)
	for i := 0; i < n/2; i++ {
		tree.Delete(i)
	}

	fmt.Printf("Size after deletions: %d\n", tree.Size())
	fmt.Printf("Height after deletions: %d\n", tree.Height())

	// Validate again
	if err := tree.Validate(); err != nil {
		fmt.Printf("Validation error: %v\n", err)
	} else {
		fmt.Println("Tree validation after deletions: ✓")
	}

	fmt.Println()
}

func log2(n int) int {
	result := 0
	for n > 1 {
		n /= 2
		result++
	}
	return result
}