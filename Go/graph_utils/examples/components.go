// Example: Connected Components and Bipartite Check
package main

import (
	"fmt"
	"graph_utils"
)

func main() {
	fmt.Println("=== Connected Components & Bipartite ===")

	// Connected Components
	fmt.Println("\n--- Connected Components ---")

	g := graph_utils.NewGraph(9, graph_utils.Undirected)
	// Component 1: 0-1-2-3
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(2, 3, 1.0)
	// Component 2: 4-5-6
	g.AddEdge(4, 5, 1.0)
	g.AddEdge(5, 6, 1.0)
	// Component 3: 7-8
	g.AddEdge(7, 8, 1.0)

	fmt.Println("Graph with 3 separate components:")
	components := g.ConnectedComponents()
	fmt.Printf("Found %d connected components:\n", len(components))
	for i, comp := range components {
		fmt.Printf("  Component %d: %v\n", i+1, comp)
	}

	fmt.Printf("\nIs connected: %v\n", g.IsConnected())

	// Bipartite Check
	fmt.Println("\n--- Bipartite Check ---")

	// Even cycle (bipartite)
	g1 := graph_utils.NewGraph(4, graph_utils.Undirected)
	g1.AddEdge(0, 1, 1.0)
	g1.AddEdge(1, 2, 1.0)
	g1.AddEdge(2, 3, 1.0)
	g1.AddEdge(3, 0, 1.0)

	isBipartite, colors := g1.Bipartite()
	fmt.Println("Square (even cycle):")
	fmt.Printf("  Is bipartite: %v\n", isBipartite)
	if isBipartite {
		fmt.Printf("  Coloring: %v (0 and 1 represent two partitions)\n", colors)
	}

	// Odd cycle (not bipartite)
	g2 := graph_utils.NewGraph(3, graph_utils.Undirected)
	g2.AddEdge(0, 1, 1.0)
	g2.AddEdge(1, 2, 1.0)
	g2.AddEdge(2, 0, 1.0)

	isBipartite, _ = g2.Bipartite()
	fmt.Println("\nTriangle (odd cycle):")
	fmt.Printf("  Is bipartite: %v\n", isBipartite)

	// Large bipartite graph
	fmt.Println("\n--- Bipartite Graph Application ---")
	fmt.Println("Job assignment problem (bipartite matching):")
	fmt.Println("  Workers: 0, 1, 2")
	fmt.Println("  Jobs: 3, 4, 5")

	g3 := graph_utils.NewGraph(6, graph_utils.Undirected)
	g3.AddEdge(0, 3, 1.0) // Worker 0 can do Job 3
	g3.AddEdge(0, 4, 1.0) // Worker 0 can do Job 4
	g3.AddEdge(1, 4, 1.0) // Worker 1 can do Job 4
	g3.AddEdge(1, 5, 1.0) // Worker 1 can do Job 5
	g3.AddEdge(2, 3, 1.0) // Worker 2 can do Job 3
	g3.AddEdge(2, 5, 1.0) // Worker 2 can do Job 5

	isBipartite, colors = g3.Bipartite()
	fmt.Printf("  Is bipartite: %v\n", isBipartite)
	if isBipartite {
		workers := []int{}
		jobs := []int{}
		for v, c := range colors {
			if c == 0 {
				workers = append(workers, v)
			} else {
				jobs = append(jobs, v)
			}
		}
		fmt.Printf("  Partition A (workers): %v\n", workers)
		fmt.Printf("  Partition B (jobs): %v\n", jobs)
	}
}