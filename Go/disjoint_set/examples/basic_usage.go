package main

import (
	"fmt"
	"strings"

	"alltoolkit/Go/disjoint_set"
)

func main() {
	fmt.Println("=== Disjoint Set (Union-Find) Examples ===\n")

	// Example 1: Basic Union-Find Operations
	fmt.Println("1. Basic Union-Find Operations")
	fmt.Println(strings.Repeat("-", 40))

	ds := disjoint_set.New(10)
	fmt.Printf("Created disjoint set with 10 elements\n")
	fmt.Printf("Initial count: %d disjoint sets\n", ds.Count())

	ds.Union(0, 1)
	ds.Union(2, 3)
	ds.Union(0, 2)
	fmt.Printf("After unions (0,1), (2,3), (0,2): %d disjoint sets\n", ds.Count())
	fmt.Printf("Are 0 and 3 connected? %v\n", ds.Connected(0, 3))
	fmt.Printf("Are 0 and 5 connected? %v\n", ds.Connected(0, 5))
	fmt.Printf("Set size containing 0: %d\n", ds.SetSize(0))

	// Show all sets
	fmt.Println("\nAll disjoint sets:")
	for root, elements := range ds.Sets() {
		fmt.Printf("  Set rooted at %d: %v\n", root, elements)
	}
	fmt.Println()

	// Example 2: Finding Connected Components
	fmt.Println("2. Counting Connected Components in a Graph")
	fmt.Println(strings.Repeat("-", 40))

	// Graph:
	//   0 --- 1 --- 2
	//   |
	//   3     4 --- 5
	edges := [][2]int{
		{0, 1}, {1, 2}, {0, 3}, {4, 5},
	}
	components := disjoint_set.CountComponents(6, edges)
	fmt.Printf("Graph with edges: %v\n", edges)
	fmt.Printf("Number of connected components: %d\n\n", components)

	// Example 3: Detecting Cycles / Finding Redundant Edge
	fmt.Println("3. Finding Redundant Connection (Cycle Detection)")
	fmt.Println(strings.Repeat("-", 40))

	// Tree with extra edge creating a cycle
	redundantEdges := [][2]int{
		{1, 2}, {1, 3}, {2, 3}, // Edge 2-3 creates cycle with 1-2-3
	}
	from, to := disjoint_set.FindRedundantConnection(3, redundantEdges)
	fmt.Printf("Edges: %v\n", redundantEdges)
	fmt.Printf("Redundant edge: (%d, %d)\n\n", from, to)

	// Example 4: Bipartite Graph Check
	fmt.Println("4. Checking if Graph is Bipartite")
	fmt.Println(strings.Repeat("-", 40))

	// Bipartite graph (square)
	bipartiteGraph := [][]int{
		{1, 3}, // 0 connects to 1, 3
		{0, 2}, // 1 connects to 0, 2
		{1, 3}, // 2 connects to 1, 3
		{0, 2}, // 3 connects to 0, 2
	}
	fmt.Printf("Square graph is bipartite: %v\n", disjoint_set.IsBipartite(bipartiteGraph))

	// Triangle (not bipartite)
	triangleGraph := [][]int{
		{1, 2},
		{0, 2},
		{0, 1},
	}
	fmt.Printf("Triangle graph is bipartite: %v\n\n", disjoint_set.IsBipartite(triangleGraph))

	// Example 5: Minimum Spanning Tree (Kruskal's Algorithm)
	fmt.Println("5. Minimum Spanning Tree (Kruskal's Algorithm)")
	fmt.Println(strings.Repeat("-", 40))

	// Weighted graph: MST weight = 1+1+2 = 4
	mstEdges := []disjoint_set.Edge{
		{0, 1, 4},
		{0, 2, 1},
		{1, 3, 2},
		{2, 3, 1},
	}

	totalWeight, mst := disjoint_set.MSTKruskal(4, mstEdges)
	fmt.Printf("Graph edges: %v\n", mstEdges)
	fmt.Printf("MST total weight: %d\n", totalWeight)
	fmt.Printf("MST edges: %v\n\n", mst)

	// Example 6: Weighted Disjoint Set
	fmt.Println("6. Weighted Disjoint Set (Union by Size)")
	fmt.Println(strings.Repeat("-", 40))

	wds := disjoint_set.NewWeighted(8)
	wds.Union(0, 1)
	wds.Union(2, 3)
	wds.Union(0, 2)
	wds.Union(4, 5)
	wds.Union(6, 7)
	wds.Union(4, 6)

	fmt.Printf("After unions, disjoint sets count: %d\n", wds.Count())
	fmt.Printf("Size of set containing 0: %d\n", wds.SetSize(0))
	fmt.Printf("Size of set containing 4: %d\n", wds.SetSize(4))
	fmt.Printf("Are 1 and 3 in same set? %v\n", wds.Connected(1, 3))
	fmt.Printf("Are 0 and 4 in same set? %v\n\n", wds.Connected(0, 4))

	// Example 7: Reset and Reuse
	fmt.Println("7. Reset and Reuse")
	fmt.Println(strings.Repeat("-", 40))

	ds2 := disjoint_set.New(5)
	ds2.Union(0, 1)
	ds2.Union(2, 3)
	fmt.Printf("Before reset: %d sets\n", ds2.Count())

	ds2.Reset()
	fmt.Printf("After reset: %d sets\n", ds2.Count())
	fmt.Printf("Are 0 and 1 connected after reset? %v\n", ds2.Connected(0, 1))

	fmt.Println("\n=== All Examples Complete ===")
}