// Example: Basic graph operations
package main

import (
	"fmt"
	"graph_utils"
)

func main() {
	fmt.Println("=== Basic Graph Operations ===")

	// Create an undirected graph with 5 vertices
	g := graph_utils.NewGraph(5, graph_utils.Undirected)

	// Add edges
	fmt.Println("\nAdding edges...")
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(0, 2, 1.0)
	g.AddEdge(1, 3, 1.0)
	g.AddEdge(2, 3, 1.0)
	g.AddEdge(3, 4, 1.0)

	fmt.Printf("Graph: %d vertices, %d edges\n", g.Vertices(), g.Edges())
	fmt.Println(g)

	// Check edge existence
	fmt.Println("\nEdge existence:")
	fmt.Printf("  HasEdge(0, 1): %v\n", g.HasEdge(0, 1))
	fmt.Printf("  HasEdge(0, 4): %v\n", g.HasEdge(0, 4))

	// Get neighbors
	fmt.Println("\nNeighbors of vertex 0:")
	neighbors, _ := g.GetNeighbors(0)
	for _, e := range neighbors {
		fmt.Printf("  -> %d (weight: %.1f)\n", e.To, e.Weight)
	}

	// Degree
	deg, _ := g.Degree(0)
	fmt.Printf("\nDegree of vertex 0: %d\n", deg)

	// Remove an edge
	fmt.Println("\nRemoving edge (0, 1)...")
	g.RemoveEdge(0, 1)
	fmt.Printf("HasEdge(0, 1): %v\n", g.HasEdge(0, 1))
	fmt.Printf("Edges after removal: %d\n", g.Edges())
}