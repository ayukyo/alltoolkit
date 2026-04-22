// Example: Shortest path algorithms (Dijkstra and Bellman-Ford)
package main

import (
	"fmt"
	"graph_utils"
	"math"
)

func main() {
	fmt.Println("=== Shortest Path Algorithms ===")

	// Create a weighted directed graph
	g := graph_utils.NewGraph(5, graph_utils.Directed)
	g.AddEdge(0, 1, 10.0)
	g.AddEdge(0, 2, 3.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(1, 3, 2.0)
	g.AddEdge(2, 1, 4.0)
	g.AddEdge(2, 3, 8.0)
	g.AddEdge(2, 4, 2.0)
	g.AddEdge(3, 4, 7.0)
	g.AddEdge(4, 3, 9.0)

	fmt.Println("\nGraph (directed with weights):")
	fmt.Println("  0 --10--> 1")
	fmt.Println("  0 --3---> 2")
	fmt.Println("  1 --1---> 2")
	fmt.Println("  1 --2---> 3")
	fmt.Println("  2 --4---> 1")
	fmt.Println("  2 --8---> 3")
	fmt.Println("  2 --2---> 4")
	fmt.Println("  3 --7---> 4")
	fmt.Println("  4 --9---> 3")

	// Dijkstra's algorithm
	fmt.Println("\n--- Dijkstra's Algorithm ---")
	result, _ := g.Dijkstra(0)

	fmt.Println("\nShortest distances from vertex 0:")
	for i, d := range result.Distances {
		if d < float64(1<<62) {
			fmt.Printf("  To %d: %.1f", i, d)
			path := result.GetPath(i)
			fmt.Printf(" (path: %v)\n", path)
		} else {
			fmt.Printf("  To %d: unreachable\n", i)
		}
	}

	// Detailed path reconstruction
	fmt.Println("\n--- Path Details ---")
	target := 4
	path := result.GetPath(target)
	fmt.Printf("Path from 0 to %d: %v\n", target, path)
	fmt.Printf("Total distance: %.1f\n", result.Distances[target])

	// Bellman-Ford (handles negative weights)
	fmt.Println("\n--- Bellman-Ford Algorithm ---")

	// Create graph with negative weights
	g2 := graph_utils.NewGraph(4, graph_utils.Directed)
	g2.AddEdge(0, 1, 4.0)
	g2.AddEdge(0, 2, 5.0)
	g2.AddEdge(1, 2, -3.0) // Negative weight!
	g2.AddEdge(2, 3, 2.0)

	bfResult, err := g2.BellmanFord(0)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	} else {
		fmt.Println("\nDistances with negative edge (Bellman-Ford):")
		for i, d := range bfResult.Distances {
			if d < float64(1<<62) {
				fmt.Printf("  To %d: %.1f\n", i, d)
			}
		}
	}

	// Negative cycle detection
	fmt.Println("\n--- Negative Cycle Detection ---")
	g3 := graph_utils.NewGraph(3, graph_utils.Directed)
	g3.AddEdge(0, 1, 1.0)
	g3.AddEdge(1, 2, -2.0)
	g3.AddEdge(2, 0, 1.0) // Creates negative cycle: 0->1->2->0 = 0

	_, err = g3.BellmanFord(0)
	fmt.Printf("Graph with negative cycle: %v\n", err)

	// Utility function
	_ = math.Floor
}