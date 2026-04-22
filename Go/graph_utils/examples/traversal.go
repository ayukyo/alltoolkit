// Example: Graph traversal (BFS and DFS)
package main

import (
	"fmt"
	"graph_utils"
)

func main() {
	fmt.Println("=== Graph Traversal Example ===")

	// Create a graph
	g := graph_utils.NewGraph(7, graph_utils.Undirected)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(0, 2, 1.0)
	g.AddEdge(1, 3, 1.0)
	g.AddEdge(1, 4, 1.0)
	g.AddEdge(2, 5, 1.0)
	g.AddEdge(2, 6, 1.0)

	fmt.Println("\nGraph structure:")
	fmt.Println("        0")
	fmt.Println("       / \\")
	fmt.Println("      1   2")
	fmt.Println("     /\\  /\\")
	fmt.Println("    3 4 5 6")

	// BFS
	fmt.Println("\n--- Breadth-First Search (BFS) ---")
	bfs, _ := g.BFS(0)
	fmt.Printf("BFS order: %v\n", bfs)

	// DFS (recursive)
	fmt.Println("\n--- Depth-First Search (DFS) ---")
	dfs, _ := g.DFS(0)
	fmt.Printf("DFS (recursive) order: %v\n", dfs)

	// DFS (iterative)
	dfsIter, _ := g.DFSIterative(0)
	fmt.Printf("DFS (iterative) order: %v\n", dfsIter)

	// Explain the difference
	fmt.Println("\n--- Analysis ---")
	fmt.Println("BFS explores level by level (breadth-first)")
	fmt.Println("DFS explores depth-first before backtracking")
	fmt.Println("The order difference shows different exploration strategies")
}