// Example demonstrating Dijkstra's shortest path algorithm
package main

import (
	"fmt"

	dijkstra_utils "github.com/ayukyo/alltoolkit/Go/dijkstra_utils"
)

func main() {
	fmt.Println("=== Dijkstra's Algorithm Demo ===\n")

	// Example 1: Simple graph
	fmt.Println("--- Example 1: Simple Graph ---")
	simpleGraph := dijkstra_utils.NewGraph[string](dijkstra_utils.Directed)
	simpleGraph.AddEdge("A", "B", 4.0)
	simpleGraph.AddEdge("B", "C", 3.0)
	simpleGraph.AddEdge("A", "C", 10.0) // Direct but longer

	result := simpleGraph.ShortestPath("A", "C")
	fmt.Printf("Path from A to C: %v\n", result.Path)
	fmt.Printf("Distance: %.1f\n", result.Distance)

	// Example 2: Complex graph
	fmt.Println("\n--- Example 2: Complex Graph ---")
	complexGraph := dijkstra_utils.NewGraph[string](dijkstra_utils.Undirected)
	complexGraph.AddEdge("A", "B", 4.0)
	complexGraph.AddEdge("A", "C", 2.0)
	complexGraph.AddEdge("B", "C", 1.0)
	complexGraph.AddEdge("B", "D", 5.0)
	complexGraph.AddEdge("C", "D", 8.0)
	complexGraph.AddEdge("C", "E", 10.0)
	complexGraph.AddEdge("D", "E", 2.0)
	complexGraph.AddEdge("D", "Z", 6.0)
	complexGraph.AddEdge("E", "Z", 3.0)

	fmt.Println("Graph edges:")
	for _, node := range complexGraph.Nodes() {
		for _, edge := range complexGraph.GetNeighbors(node) {
			fmt.Printf("  %s -> %s (weight: %.1f)\n", node, edge.Target, edge.Weight)
		}
	}

	result2 := complexGraph.ShortestPath("A", "Z")
	fmt.Printf("\nShortest path from A to Z: %v\n", result2.Path)
	fmt.Printf("Distance: %.1f\n", result2.Distance)

	// Example 3: Find all paths from a source
	fmt.Println("\n--- Example 3: All Paths from Source ---")
	allPaths := complexGraph.ShortestPathsFrom("A")
	fmt.Println("Shortest distances from A:")
	for _, node := range complexGraph.Nodes() {
		pathResult := allPaths.GetPathTo(node)
		if pathResult.Found {
			fmt.Printf("  To %s: %.1f via %v\n", node, pathResult.Distance, pathResult.Path)
		}
	}

	// Example 4: K-shortest paths
	fmt.Println("\n--- Example 4: K-Shortest Paths ---")
	kPaths := complexGraph.KShortestPaths("A", "Z", 3)
	fmt.Printf("Top 3 shortest paths from A to Z:\n")
	for i, path := range kPaths {
		fmt.Printf("  Path %d: %v (distance: %.1f)\n", i+1, path.Path, path.Distance)
	}

	// Example 5: Graph statistics
	fmt.Println("\n--- Example 5: Graph Statistics ---")
	fmt.Printf("Nodes: %d\n", complexGraph.NodeCount())
	fmt.Printf("Edges: %d\n", complexGraph.EdgeCount())
	fmt.Printf("Is directed: %v\n", complexGraph.IsDirected())

	diameter, ep1, ep2 := complexGraph.GraphDiameter()
	fmt.Printf("Diameter: %.1f (between %s and %s)\n", diameter, ep1, ep2)

	center := complexGraph.CenterOfGraph()
	fmt.Printf("Center nodes: %v\n", center)

	// Example 6: Integer nodes
	fmt.Println("\n--- Example 6: Integer Node Graph ---")
	intGraph := dijkstra_utils.NewGraph[int](dijkstra_utils.Directed)
	intGraph.AddEdge(1, 2, 1.0)
	intGraph.AddEdge(2, 3, 1.0)
	intGraph.AddEdge(3, 4, 1.0)
	intGraph.AddEdge(1, 4, 5.0) // Direct but longer

	result3 := intGraph.ShortestPath(1, 4)
	fmt.Printf("Path from 1 to 4: %v\n", result3.Path)
	fmt.Printf("Distance: %.1f\n", result3.Distance)

	// Example 7: From adjacency list
	fmt.Println("\n--- Example 7: From Adjacency List ---")
	adjList := map[string][]struct{ Node string; Weight float64 }{
		"A": {{Node: "B", Weight: 4.0}, {Node: "C", Weight: 2.0}},
		"B": {{Node: "C", Weight: 1.0}, {Node: "D", Weight: 5.0}},
		"C": {{Node: "D", Weight: 8.0}},
		"D": {},
	}
	fromAdjGraph := dijkstra_utils.FromAdjacencyList(adjList, true)
	result4 := fromAdjGraph.ShortestPath("A", "D")
	fmt.Printf("Path from A to D: %v\n", result4.Path)
	fmt.Printf("Distance: %.1f\n", result4.Distance)

	// Example 8: Connectivity check
	fmt.Println("\n--- Example 8: Connectivity Check ---")
	fmt.Printf("A and D connected: %v\n", complexGraph.IsConnected("A", "D"))
	fmt.Printf("A and Z connected: %v\n", complexGraph.IsConnected("A", "Z"))

	reachable := complexGraph.GetReachableNodes("A")
	fmt.Printf("Nodes reachable from A: %v\n", reachable)

	fmt.Println("\n=== Demo Complete ===")
}