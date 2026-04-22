// Example: Social Network Analysis
package main

import (
	"fmt"
	"graph_utils"
)

func main() {
	fmt.Println("=== Social Network Analysis ===")

	// Create a social network graph
	fmt.Println("\n--- Social Network Structure ---")
	fmt.Println("Users: Alice, Bob, Carol, Dave, Eve, Frank")

	g := graph_utils.NewGraph(6, graph_utils.Undirected)
	names := []string{"Alice", "Bob", "Carol", "Dave", "Eve", "Frank"}

	// Friend connections (weight = closeness score)
	g.AddEdge(0, 1, 5.0) // Alice-Bob
	g.AddEdge(0, 2, 3.0) // Alice-Carol
	g.AddEdge(0, 3, 2.0) // Alice-Dave
	g.AddEdge(1, 2, 4.0)  // Bob-Carol
	g.AddEdge(1, 4, 1.0)  // Bob-Eve
	g.AddEdge(2, 3, 6.0)  // Carol-Dave
	g.AddEdge(2, 5, 2.0)  // Carol-Frank
	g.AddEdge(3, 5, 3.0)  // Dave-Frank
	g.AddEdge(4, 5, 4.0)  // Eve-Frank

	fmt.Printf("Network: %d users, %d connections\n", g.Vertices(), g.Edges()/2)

	// Analyze connectivity
	fmt.Println("\n--- Connectivity Analysis ---")
	fmt.Printf("Network is connected: %v\n", g.IsConnected())
	components := g.ConnectedComponents()
	fmt.Printf("Number of components: %d\n", len(components))

	// User degrees (number of friends)
	fmt.Println("\n--- User Connections (Degree) ---")
	for i, name := range names {
		deg, _ := g.Degree(i)
		fmt.Printf("  %s has %d connections\n", name, deg)
	}

	// Find influential users (highest degree)
	maxDeg := 0
	influential := ""
	for i, name := range names {
		deg, _ := g.Degree(i)
		if deg > maxDeg {
			maxDeg = deg
			influential = name
		}
	}
	fmt.Printf("\nMost connected user: %s (%d connections)\n", influential, maxDeg)

	// Shortest paths (social distance)
	fmt.Println("\n--- Social Distance (Shortest Paths) ---")
	alice := 0
	result, _ := g.Dijkstra(alice)

	fmt.Printf("Distances from %s:\n", names[alice])
	for i, d := range result.Distances {
		path := result.GetPath(i)
		pathNames := make([]string, len(path))
		for j, v := range path {
			pathNames[j] = names[v]
		}
		fmt.Printf("  to %s: %.0f hops (path: %v)\n", names[i], d, pathNames)
	}

	// Find mutual friends
	fmt.Println("\n--- Network Analysis ---")

	// Check if Alice (0) and Frank (5) are connected
	fmt.Printf("Are Alice and Frank connected? %v\n", g.HasEdge(0, 5))

	// MST (minimum connections for everyone to be connected)
	mst, _ := g.Kruskal()
	fmt.Printf("\nMinimum connections to connect everyone: %d\n", len(mst.Edges))
	fmt.Println("Essential connections:")
	for _, e := range mst.Edges {
		fmt.Printf("  %s -- %s\n", names[e.From], names[e.To])
	}

	// Bipartite check (can we split into two groups with no internal connections?)
	isBipartite, colors := g.Bipartite()
	fmt.Printf("\nCan split into two exclusive groups? %v\n", isBipartite)
	if isBipartite {
		groupA := []string{}
		groupB := []string{}
		for i, c := range colors {
			if c == 0 {
				groupA = append(groupA, names[i])
			} else {
				groupB = append(groupB, names[i])
			}
		}
		fmt.Printf("  Group A: %v\n", groupA)
		fmt.Printf("  Group B: %v\n", groupB)
	}
}