// Package topological_sort_utils_test demonstrates topological sorting for various use cases
package topological_sort_utils_test

import (
	"fmt"
	"strings"

	"github.com/ayukyo/alltoolkit/Go/topological_sort_utils"
)

// RunExamples demonstrates all use cases for topological sorting
func RunExamples() {
	fmt.Println("=== Topological Sort Utils Examples ===")
	fmt.Println()

	// Example 1: Course Prerequisites
	fmt.Println("1. Course Prerequisites:")
	g := topological_sort_utils.NewGraph[string]()
	g.AddNodes("Math101", "Math201", "Math301", "Physics201", "Physics301", "CS101", "CS201", "CS301")
	g.AddEdge("Math101", "Math201")
	g.AddEdge("Math201", "Math301")
	g.AddEdge("Math101", "Physics201")
	g.AddEdge("Math201", "Physics301")
	g.AddEdge("Physics201", "Physics301")
	g.AddEdge("CS101", "CS201")
	g.AddEdge("CS201", "CS301")
	order, _ := g.Sort()
	fmt.Printf("   Course order: %v\n\n", order)

	// Example 2: Build System Dependencies
	fmt.Println("2. Build System Dependencies:")
	deps := map[string][]string{
		"core":     {},
		"utils":    {"core"},
		"database": {"core", "utils"},
		"api":      {"core", "database"},
		"web":      {"api", "utils"},
	}
	buildOrder, _ := topological_sort_utils.TopologicalSort(deps)
	fmt.Printf("   Build order: %v\n\n", buildOrder)

	// Example 3: Task Scheduling with Levels
	fmt.Println("3. Task Scheduling (Parallel Levels):")
	g2 := topological_sort_utils.NewGraph[string]()
	g2.AddNodes("design_db", "design_api", "implement_db", "implement_api", "testing", "deployment")
	g2.AddEdge("design_db", "implement_db")
	g2.AddEdge("design_api", "implement_api")
	g2.AddEdge("implement_db", "testing")
	g2.AddEdge("implement_api", "testing")
	g2.AddEdge("testing", "deployment")
	levels, _ := g2.Levels()
	for i, level := range levels {
		fmt.Printf("   Level %d: %v\n", i, level)
	}
	fmt.Println()

	// Example 4: Detect Circular Dependencies
	fmt.Println("4. Circular Dependency Detection:")
	g3 := topological_sort_utils.NewGraph[string]()
	g3.AddNodes("A", "B", "C", "D")
	g3.AddEdge("A", "B")
	g3.AddEdge("B", "C")
	g3.AddEdge("C", "D")
	g3.AddEdge("D", "B") // Creates cycle
	cycle := g3.FindCycle()
	if cycle != nil {
		fmt.Printf("   Cycle found: %s\n\n", strings.Join(cycle, " -> "))
	}

	// Example 5: Dependency Resolver
	fmt.Println("5. Dependency Resolver:")
	resolver := topological_sort_utils.NewDependencyResolver[string]()
	resolver.AddItem("app", "database", "config")
	resolver.AddItem("config", "env")
	resolver.AddItem("database", "env")
	resolver.AddItem("env")
	resolveOrder, _ := resolver.Resolve()
	fmt.Printf("   Install order: %v\n\n", resolveOrder)

	// Example 6: Longest Path (Critical Path)
	fmt.Println("6. Longest Path (Critical Path):")
	g4 := topological_sort_utils.NewGraph[string]()
	g4.AddNodes("start", "A", "B", "end")
	g4.AddEdge("start", "A")
	g4.AddEdge("start", "B")
	g4.AddEdge("A", "end")
	g4.AddEdge("B", "end")
	path, _ := g4.LongestPath("start")
	fmt.Printf("   Longest path: %v\n\n", path)
}