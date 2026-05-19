// Example applications demonstrating fenwick_tree_utils usage
package main

import (
	"fmt"

	fenwick "github.com/ayukyo/alltoolkit/Go/fenwick_tree_utils"
)

func main() {
	fmt.Println("=== Fenwick Tree Utils Examples ===")

	// 1. Basic Prefix Sum
	basicPrefixSumExample()

	// 2. Range Sum Queries
	rangeSumExample()

	// 3. Inverse Operations (Find)
	findExample()

	// 4. 2D Fenwick Tree
	twoDExample()

	// 5. Range Update / Point Query
	diffExample()

	// 6. Frequency Counting
	frequencyCountExample()

	// 7. Weighted Median
	weightedMedianExample()

	// 8. GCD Queries
	gcdExample()

	// 9. Min/Max Queries
	minMaxExample()
}

// 1. Basic Prefix Sum Example
func basicPrefixSumExample() {
	fmt.Println("--- Basic Prefix Sum ---")

	// Create from array
	arr := []int64{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	tree := fenwick.NewFromArray(arr)

	// Prefix sum queries
	fmt.Printf("Array: %v\n", arr)
	fmt.Printf("Prefix sum [1..5]: %d\n", getPrefixSum(tree, 5))
	fmt.Printf("Prefix sum [1..10]: %d\n", getPrefixSum(tree, 10))
	fmt.Printf("Total sum: %d\n\n", tree.Total())
}

func getPrefixSum(tree *fenwick.FenwickTree, idx int) int64 {
	sum, _ := tree.PrefixSum(idx)
	return sum
}

// 2. Range Sum Queries Example
func rangeSumExample() {
	fmt.Println("--- Range Sum Queries ---")

	tree := fenwick.New(100)

	// Populate with some values
	for i := 1; i <= 100; i++ {
		tree.Update(i, int64(i))
	}

	// Query specific ranges
	fmt.Printf("Sum of first 10 numbers: %d\n", getRangeSum(tree, 1, 10))
	fmt.Printf("Sum of numbers 50-60: %d\n", getRangeSum(tree, 50, 60))
	fmt.Printf("Sum of last 10 numbers: %d\n", getRangeSum(tree, 91, 100))
	fmt.Printf("Total sum (1-100): %d\n\n", tree.Total())
}

func getRangeSum(tree *fenwick.FenwickTree, l, r int) int64 {
	sum, _ := tree.RangeSum(l, r)
	return sum
}

// 3. Find (Inverse Operation) Example
func findExample() {
	fmt.Println("--- Find (Inverse Operation) ---")

	// Frequency array (counts of each value)
	frequencies := []int64{10, 20, 30, 20, 10} // 5 bins
	tree := fenwick.NewFromArray(frequencies)

	fmt.Printf("Frequency array: %v\n", frequencies)

	// Find index where cumulative count >= target
	targets := []int64{15, 50, 80}
	for _, target := range targets {
		idx, _ := tree.Find(target)
		fmt.Printf("Find cumulative >= %d: index %d\n", target, idx)
	}
	fmt.Println()
}

// 4. 2D Fenwick Tree Example
func twoDExample() {
	fmt.Println("--- 2D Fenwick Tree ---")

	// Create a 4x4 matrix
	matrix := [][]int64{
		{1, 2, 3, 4},
		{5, 6, 7, 8},
		{9, 10, 11, 12},
		{13, 14, 15, 16},
	}

	tree := fenwick.New2DFromArray(matrix)

	fmt.Printf("Matrix:\n")
	for _, row := range matrix {
		fmt.Printf("  %v\n", row)
	}

	// Query submatrix sums
	sum1, _ := tree.RangeSum2D(1, 1, 2, 2)
	sum2, _ := tree.RangeSum2D(2, 2, 3, 3)
	sum3, _ := tree.RangeSum2D(1, 1, 4, 4)

	fmt.Printf("Sum of top-left 2x2: %d (1+2+5+6)\n", sum1)
	fmt.Printf("Sum of center 2x2: %d (6+7+10+11)\n", sum2)
	fmt.Printf("Sum of entire matrix: %d\n\n", sum3)
}

// 5. Range Update / Point Query Example
func diffExample() {
	fmt.Println("--- Range Update / Point Query ---")

	// Difference array technique
	tree := fenwick.NewDiff(10)

	// Initialize with zeros, then apply range updates
	fmt.Println("Initial array: all zeros")

	// Add 5 to range [3, 7]
	tree.RangeUpdate(3, 7, 5)
	fmt.Println("After adding 5 to range [3, 7]:")

	for i := 1; i <= 10; i++ {
		val, _ := tree.PointQuery(i)
		fmt.Printf("  Index %d: %d\n", i, val)
	}

	// Add 10 to range [5, 8]
	tree.RangeUpdate(5, 8, 10)
	fmt.Println("After adding 10 to range [5, 8]:")

	for i := 1; i <= 10; i++ {
		val, _ := tree.PointQuery(i)
		fmt.Printf("  Index %d: %d\n", i, val)
	}
	fmt.Println()
}

// 6. Frequency Counting Example
func frequencyCountExample() {
	fmt.Println("--- Frequency Counting ---")

	// Count occurrences using compressed coordinates
	values := []int64{100, 200, 150, 100, 200, 300, 100, 200, 150}

	tree, mapping := fenwick.NewCompressed(values)

	fmt.Printf("Original values: %v\n", values)
	fmt.Printf("Compressed mapping: %v\n", mapping)

	// Count frequencies
	for _, v := range values {
		tree.Update(mapping[v], 1)
	}

	// Query cumulative frequencies
	for v := range mapping {
		idx := mapping[v]
		prefix, _ := tree.PrefixSum(idx)
		fmt.Printf("Value %d appears %d times, cumulative up to %d: %d\n",
			v, getVal(tree, idx), v, prefix)
	}
	fmt.Println()
}

func getVal(tree *fenwick.FenwickTree, idx int) int64 {
	val, _ := tree.Value(idx)
	return val
}

// 7. Weighted Median Example
func weightedMedianExample() {
	fmt.Println("--- Weighted Median ---")

	// Weighted values (index = value weight, tree value = frequency)
	weights := []int64{5, 10, 15, 10, 5} // Frequency distribution
	tree := fenwick.NewFromArray(weights)

	fmt.Printf("Weight distribution: %v\n", weights)

	total := tree.Total()
	fmt.Printf("Total weight: %d\n", total)

	// Find median position
	medianIdx, _ := fenwick.Median(tree)
	fmt.Printf("Median position: %d\n", medianIdx)

	// Find 25th and 75th percentile
	p25, _ := fenwick.Percentile(tree, 25)
	p75, _ := fenwick.Percentile(tree, 75)
	fmt.Printf("25th percentile: index %d\n", p25)
	fmt.Printf("75th percentile: index %d\n\n", p75)
}

// 8. GCD Queries Example
func gcdExample() {
	fmt.Println("--- GCD Queries ---")

	tree := fenwick.NewGcd(5)

	// Set values
	values := []int64{12, 18, 24, 30, 36}
	for i, v := range values {
		tree.UpdateGcd(i+1, v)
	}

	fmt.Printf("Values: %v\n", values)

	// Query GCD ranges
	gcd1, _ := tree.RangeGcd(1, 3)
	gcd2, _ := tree.RangeGcd(2, 5)
	gcd3, _ := tree.RangeGcd(3, 4)

	fmt.Printf("GCD of [1,3]: %d (gcd(12,18,24))\n", gcd1)
	fmt.Printf("GCD of [2,5]: %d (gcd(18,24,30,36))\n", gcd2)
	fmt.Printf("GCD of [3,4]: %d (gcd(24,30))\n\n", gcd3)
}

// 9. Min/Max Queries Example
func minMaxExample() {
	fmt.Println("--- Min/Max Queries ---")

	values := []int64{10, 5, 20, 3, 15}

	// Min tree
	minTree := fenwick.NewMinFromArray(values)
	min1, _ := minTree.RangeMin(1, 5)
	min2, _ := minTree.RangeMin(2, 4)

	fmt.Printf("Values: %v\n", values)
	fmt.Printf("Min in [1,5]: %d\n", min1)
	fmt.Printf("Min in [2,4]: %d\n", min2)

	// Max tree
	maxTree := fenwick.NewMax(5, -999999)
	for i, v := range values {
		maxTree.UpdateMax(i+1, v)
	}
	max1, _ := maxTree.RangeMax(1, 5)
	max2, _ := maxTree.RangeMax(3, 5)

	fmt.Printf("Max in [1,5]: %d\n", max1)
	fmt.Printf("Max in [3,5]: %d\n\n", max2)
}