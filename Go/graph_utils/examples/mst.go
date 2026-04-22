// Example: Minimum Spanning Tree (Kruskal and Prim)
package main

import (
	"fmt"
	"graph_utils"
)

func main() {
	fmt.Println("=== Minimum Spanning Tree Example ===")

	// Create a weighted undirected graph
	fmt.Println("\nNetwork Cable Layout:")
	fmt.Println("  Vertices: A, B, C, D")
	fmt.Println("  Edges with costs:")
	fmt.Println("    A-B: $10")
	fmt.Println("    A-C: $6")
	fmt.Println("    A-D: $5")
	fmt.Println("    B-D: $15")
	fmt.Println("    C-D: $4")

	g := graph_utils.NewGraph(4, graph_utils.Undirected)
	// Map: 0=A, 1=B, 2=C, 3=D
	g.AddEdge(0, 1, 10.0) // A-B
	g.AddEdge(0, 2, 6.0)  // A-C
	g.AddEdge(0, 3, 5.0)  // A-D
	g.AddEdge(1, 3, 15.0) // B-D
	g.AddEdge(2, 3, 4.0)  // C-D

	// Kruskal's algorithm
	fmt.Println("\n--- Kruskal's Algorithm ---")
	mst, err := g.Kruskal()
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	vertexNames := []string{"A", "B", "C", "D"}
	fmt.Println("MST Edges (sorted by weight, greedy selection):")
	for _, e := range mst.Edges {
		fmt.Printf("  %s -- %s (cost: $%.0f)\n",
			vertexNames[e.From], vertexNames[e.To], e.Weight)
	}
	fmt.Printf("Total MST cost: $%.0f\n", mst.Weight)

	// Prim's algorithm
	fmt.Println("\n--- Prim's Algorithm ---")
	mst2, err := g.Prim(0)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	fmt.Println("MST Edges (grown from vertex A):")
	for _, e := range mst2.Edges {
		fmt.Printf("  %s -- %s (cost: $%.0f)\n",
			vertexNames[e.From], vertexNames[e.To], e.Weight)
	}
	fmt.Printf("Total MST cost: $%.0f\n", mst2.Weight)

	// Verify both algorithms produce same total weight
	fmt.Println("\n--- Verification ---")
	if mst.Weight == mst2.Weight {
		fmt.Printf("✓ Both algorithms found optimal MST with total cost: $%.0f\n", mst.Weight)
	}

	// Disconnected graph test
	fmt.Println("\n--- Disconnected Graph Test ---")
	g2 := graph_utils.NewGraph(4, graph_utils.Undirected)
	g2.AddEdge(0, 1, 1.0)
	g2.AddEdge(2, 3, 1.0)
	// Components: {0,1} and {2,3}

	_, err = g2.Kruskal()
	fmt.Printf("MST on disconnected graph: %v\n", err)
}