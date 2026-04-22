// Example: Topological Sort for DAG
package main

import (
	"fmt"
	"graph_utils"
)

func main() {
	fmt.Println("=== Topological Sort Example ===")

	// Create a DAG for course prerequisites
	fmt.Println("\nCourse Prerequisites Example:")
	fmt.Println("  CS101 -> CS201, CS202")
	fmt.Println("  CS201 -> CS301")
	fmt.Println("  CS202 -> CS302")
	fmt.Println("  CS301 -> CS401")
	fmt.Println("  CS302 -> CS401")

	g := graph_utils.NewGraph(6, graph_utils.Directed)

	// Map: 0=CS101, 1=CS201, 2=CS202, 3=CS301, 4=CS302, 5=CS401
	courses := []string{"CS101", "CS201", "CS202", "CS301", "CS302", "CS401"}

	g.AddEdge(0, 1, 1.0) // CS101 -> CS201
	g.AddEdge(0, 2, 1.0) // CS101 -> CS202
	g.AddEdge(1, 3, 1.0) // CS201 -> CS301
	g.AddEdge(2, 4, 1.0) // CS202 -> CS302
	g.AddEdge(3, 5, 1.0) // CS301 -> CS401
	g.AddEdge(4, 5, 1.0) // CS302 -> CS401

	// Topological sort
	order, err := g.TopologicalSort()
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	fmt.Println("\nTopological order (valid course sequence):")
	for i, v := range order {
		fmt.Printf("  %d. %s\n", i+1, courses[v])
	}

	// Cycle detection
	fmt.Println("\n--- Cycle Detection ---")

	// Graph with cycle
	g2 := graph_utils.NewGraph(3, graph_utils.Directed)
	g2.AddEdge(0, 1, 1.0)
	g2.AddEdge(1, 2, 1.0)
	g2.AddEdge(2, 0, 1.0) // Cycle!

	fmt.Printf("Graph with cycle hasCycle: %v\n", g2.HasCycle())
	_, err = g2.TopologicalSort()
	fmt.Printf("Topological sort on cyclic graph: %v\n", err)

	// Graph without cycle
	fmt.Printf("\nCourse graph hasCycle: %v\n", g.HasCycle())
}