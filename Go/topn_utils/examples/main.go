// Example usage of topn_utils package
package main

import (
	"fmt"
	"math/rand"
	"time"

	topn_utils "github.com/ayukyo/alltoolkit/Go/topn_utils"
)

func main() {
	fmt.Println("=== Top N Utils Examples ===")
	fmt.Println()

	// Example 1: Find top N largest integers
	fmt.Println("1. Top N Largest Integers")
	data := []int{45, 23, 67, 12, 89, 34, 78, 56, 90, 11, 33, 44}
	finder := topn_utils.NewTopNFinder(5)
	largest := finder.Largest(data)
	fmt.Printf("   Data: %v\n", data)
	fmt.Printf("   Top 5 Largest: %v\n", largest)
	fmt.Println()

	// Example 2: Find top N smallest integers
	fmt.Println("2. Top N Smallest Integers")
	smallest := finder.Smallest(data)
	fmt.Printf("   Data: %v\n", data)
	fmt.Printf("   Top 5 Smallest: %v\n", smallest)
	fmt.Println()

	// Example 3: Float64 operations
	fmt.Println("3. Top N Float64 Values")
	floatData := []float64{3.14, 2.71, 1.41, 9.81, 6.67, 0.58, 4.44}
	topFloats := topn_utils.NewTopNFinder(3).LargestFloats(floatData)
	bottomFloats := topn_utils.NewTopNFinder(3).SmallestFloats(floatData)
	fmt.Printf("   Data: %v\n", floatData)
	fmt.Printf("   Top 3 Largest: %v\n", topFloats)
	fmt.Printf("   Top 3 Smallest: %v\n", bottomFloats)
	fmt.Println()

	// Example 4: String operations (lexicographic)
	fmt.Println("4. Top N Strings (Lexicographic)")
	words := []string{"zebra", "apple", "mango", "banana", "cherry", "orange"}
	topWords := topn_utils.NewTopNFinder(3).LargestStrings(words)
	bottomWords := topn_utils.NewTopNFinder(3).SmallestStrings(words)
	fmt.Printf("   Data: %v\n", words)
	fmt.Printf("   Top 3 (Z-A): %v\n", topWords)
	fmt.Printf("   Top 3 (A-Z): %v\n", bottomWords)
	fmt.Println()

	// Example 5: Custom items with scores
	fmt.Println("5. Custom Items with Scores (e.g., Product Ratings)")
	products := []topn_utils.Item{
		{Value: "Laptop", Score: 4.8},
		{Value: "Phone", Score: 4.5},
		{Value: "Tablet", Score: 4.2},
		{Value: "Monitor", Score: 4.7},
		{Value: "Keyboard", Score: 4.1},
		{Value: "Mouse", Score: 4.9},
		{Value: "Headphones", Score: 4.6},
	}
	topProducts := topn_utils.NewTopNFinder(3).LargestItems(products)
	fmt.Println("   Top 3 Highest Rated Products:")
	for i, item := range topProducts {
		fmt.Printf("   %d. %s (Score: %.1f)\n", i+1, item.Value, item.Score)
	}
	fmt.Println()

	// Example 6: Quick Select - find k-th element
	fmt.Println("6. Quick Select (K-th Element)")
	testData := []int{7, 2, 5, 3, 9, 1, 6, 4, 8}
	kthSmallest := topn_utils.KthSmallest(testData, 3)
	kthLargest := topn_utils.KthLargest(testData, 2)
	fmt.Printf("   Data: %v\n", testData)
	fmt.Printf("   3rd Smallest: %d\n", kthSmallest)
	fmt.Printf("   2nd Largest: %d\n", kthLargest)
	fmt.Println()

	// Example 7: Median and Percentile
	fmt.Println("7. Statistical Functions")
	scores := []int{85, 92, 78, 95, 88, 72, 90, 82, 79, 91}
	median := topn_utils.Median(scores)
	p25 := topn_utils.Percentile(scores, 25)
	p75 := topn_utils.Percentile(scores, 75)
	fmt.Printf("   Scores: %v\n", scores)
	fmt.Printf("   Median: %.1f\n", median)
	fmt.Printf("   25th Percentile: %d\n", p25)
	fmt.Printf("   75th Percentile: %d\n", p75)
	fmt.Println()

	// Example 8: Large dataset performance demo
	fmt.Println("8. Large Dataset Performance")
	rand.Seed(time.Now().UnixNano())
	largeData := make([]int, 1000000)
	for i := range largeData {
		largeData[i] = rand.Intn(10000000)
	}

	start := time.Now()
	top100 := topn_utils.NewTopNFinder(100).Largest(largeData)
	elapsed := time.Since(start)
	fmt.Printf("   Found top 100 from 1,000,000 elements in %v\n", elapsed)
	fmt.Printf("   Result (first 5): %v...\n", top100[:5])
	fmt.Println()

	// Example 9: Convenience functions
	fmt.Println("9. Convenience Functions (Quick API)")
	quickData := []int{15, 3, 9, 8, 2, 6, 12, 1, 7}
	top3 := topn_utils.TopNLargest(quickData, 3)
	bottom3 := topn_utils.TopNSmallest(quickData, 3)
	fmt.Printf("   Data: %v\n", quickData)
	fmt.Printf("   Top 3 Largest: %v\n", top3)
	fmt.Printf("   Top 3 Smallest: %v\n", bottom3)
	fmt.Println()

	// Example 10: Real-world use case - Log analysis
	fmt.Println("10. Real-World Use Case: Finding Slowest Requests")
	responseTimes := []topn_utils.Item{
		{Value: "/api/users", Score: 45},
		{Value: "/api/products", Score: 120},
		{Value: "/api/orders", Score: 89},
		{Value: "/api/search", Score: 230},
		{Value: "/api/auth", Score: 35},
		{Value: "/api/reports", Score: 450},
		{Value: "/api/export", Score: 380},
		{Value: "/api/import", Score: 520},
	}
	slowest := topn_utils.NewTopNFinder(3).LargestItems(responseTimes)
	fmt.Println("   Top 3 Slowest API Endpoints:")
	for i, item := range slowest {
		fmt.Printf("   %d. %s (%.0fms)\n", i+1, item.Value, item.Score)
	}
}