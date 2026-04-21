package main

import (
	"fmt"
	"avl_tree_utils"
)

func main() {
	fmt.Println("=== AVL Tree Examples ===")
	fmt.Println()

	// Example 1: Basic operations with integers
	fmt.Println("--- Example 1: Basic Integer Operations ---")
	tree := avl_tree_utils.NewInt()
	
	// Insert elements
	values := []int{50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45}
	for _, v := range values {
		tree.Insert(v)
		fmt.Printf("Inserted: %d, Height: %d\n", v, tree.Height())
	}

	fmt.Printf("\nTree size: %d\n", tree.Size())
	fmt.Printf("Tree height: %d (balanced)\n", tree.Height())
	fmt.Printf("In-order: %v\n", tree.InOrder())
	fmt.Printf("Pre-order: %v\n", tree.PreOrder())
	fmt.Printf("Level-order: %v\n", tree.LevelOrder())

	// Min and Max
	min, _ := tree.Min()
	max, _ := tree.Max()
	fmt.Printf("Min: %d, Max: %d\n", min, max)

	fmt.Println()

	// Example 2: Search and Contains
	fmt.Println("--- Example 2: Search Operations ---")
	fmt.Printf("Contains 40: %v\n", tree.Contains(40))
	fmt.Printf("Contains 100: %v\n", tree.Contains(100))
	
	if node := tree.Search(40); node != nil {
		fmt.Printf("Found node with key 40, height: %d\n", tree.GetHeight(40))
	}

	fmt.Println()

	// Example 3: Range queries
	fmt.Println("--- Example 3: Range Queries ---")
	fmt.Printf("Keys in range [25, 60]: %v\n", tree.Range(25, 60))
	fmt.Printf("Count in range [25, 60]: %d\n", tree.Count(25, 60))

	fmt.Println()

	// Example 4: Lower and Upper bounds
	fmt.Println("--- Example 4: Lower and Upper Bounds ---")
	lb, ok := tree.LowerBound(35)
	fmt.Printf("Lower bound of 35: %d (found: %v)\n", lb, ok)
	
	ub, ok := tree.UpperBound(35)
	fmt.Printf("Upper bound of 35: %d (found: %v)\n", ub, ok)

	fmt.Println()

	// Example 5: Predecessor and Successor
	fmt.Println("--- Example 5: Predecessor and Successor ---")
	pred, _ := tree.Predecessor(40)
	fmt.Printf("Predecessor of 40: %d\n", pred)
	
	succ, _ := tree.Successor(40)
	fmt.Printf("Successor of 40: %d\n", succ)

	fmt.Println()

	// Example 6: K-th element operations
	fmt.Println("--- Example 6: K-th Element Operations ---")
	for k := 1; k <= 5; k++ {
		kth, _ := tree.KthSmallest(k)
		fmt.Printf("%d-th smallest: %d\n", k, kth)
	}
	
	fmt.Println()
	for k := 1; k <= 3; k++ {
		kth, _ := tree.KthLargest(k)
		fmt.Printf("%d-th largest: %d\n", k, kth)
	}

	fmt.Println()

	// Example 7: Rank
	fmt.Println("--- Example 7: Rank ---")
	fmt.Printf("Rank of 40: %d (position in sorted order)\n", tree.Rank(40))
	fmt.Printf("Rank of 20: %d\n", tree.Rank(20))

	fmt.Println()

	// Example 8: Deletion
	fmt.Println("--- Example 8: Deletion ---")
	fmt.Printf("Before deletion: %v\n", tree.InOrder())
	fmt.Printf("Delete 40: %v\n", tree.Delete(40))
	fmt.Printf("After deletion: %v\n", tree.InOrder())
	fmt.Printf("Tree still balanced: %v\n", tree.IsBalanced())

	fmt.Println()

	// Example 9: String keys
	fmt.Println("--- Example 9: String Keys ---")
	strTree := avl_tree_utils.NewString()
	words := []string{"delta", "alpha", "charlie", "bravo", "echo"}
	
	for _, w := range words {
		strTree.Insert(w)
	}
	
	fmt.Printf("Words in order: %v\n", strTree.InOrder())
	fmt.Printf("Find 'charlie': %v\n", strTree.Contains("charlie"))

	fmt.Println()

	// Example 10: Using ForEach
	fmt.Println("--- Example 10: ForEach Iteration ---")
	fmt.Print("Iterating: ")
	tree.ForEach(func(key int) bool {
		fmt.Printf("%d ", key)
		return true
	})
	fmt.Println()

	fmt.Println()

	// Example 11: FromSlice and ToSlice
	fmt.Println("--- Example 11: FromSlice and ToSlice ---")
	newTree := avl_tree_utils.NewInt()
	count := newTree.FromSlice([]int{5, 3, 7, 1, 9})
	fmt.Printf("Inserted %d elements from slice\n", count)
	fmt.Printf("To slice: %v\n", newTree.ToSlice())

	fmt.Println()

	// Example 12: Validation
	fmt.Println("--- Example 12: Tree Validation ---")
	if err := tree.Validate(); err != nil {
		fmt.Printf("Tree invalid: %v\n", err)
	} else {
		fmt.Println("Tree is valid (satisfies all AVL properties)")
	}
}