package topological_sort_utils

import (
	"testing"
)

func TestNewGraph(t *testing.T) {
	g := NewGraph[int]()
	if g == nil {
		t.Fatal("NewGraph returned nil")
	}
	if g.Count() != 0 {
		t.Errorf("Expected empty graph, got %d nodes", g.Count())
	}
}

func TestAddNode(t *testing.T) {
	g := NewGraph[string]()
	g.AddNode("A")
	g.AddNode("B")
	g.AddNode("A") // duplicate

	if g.Count() != 2 {
		t.Errorf("Expected 2 nodes, got %d", g.Count())
	}
	if !g.HasNode("A") || !g.HasNode("B") {
		t.Error("Missing expected nodes")
	}
	if g.HasNode("C") {
		t.Error("Unexpected node C found")
	}
}

func TestAddEdge(t *testing.T) {
	g := NewGraph[int]()
	g.AddNodes(1, 2, 3)

	err := g.AddEdge(1, 2)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}

	err = g.AddEdge(2, 3)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}

	edges := g.GetEdges(1)
	if len(edges) != 1 || edges[0] != 2 {
		t.Errorf("Expected edge 1->2, got %v", edges)
	}

	// Test edge from non-existent node
	err = g.AddEdge(4, 1)
	if err != ErrNodeNotFound {
		t.Errorf("Expected ErrNodeNotFound, got %v", err)
	}
}

func TestSort(t *testing.T) {
	g := NewGraph[string]()
	g.AddNodes("A", "B", "C", "D")
	g.AddEdge("A", "B")
	g.AddEdge("B", "C")
	g.AddEdge("C", "D")

	result, err := g.Sort()
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	// Verify order: A should come before B, B before C, C before D
	positions := make(map[string]int)
	for i, node := range result {
		positions[node] = i
	}

	if positions["A"] >= positions["B"] {
		t.Error("A should come before B")
	}
	if positions["B"] >= positions["C"] {
		t.Error("B should come before C")
	}
	if positions["C"] >= positions["D"] {
		t.Error("C should come before D")
	}
}

func TestSortWithCycle(t *testing.T) {
	g := NewGraph[int]()
	g.AddNodes(1, 2, 3)
	g.AddEdge(1, 2)
	g.AddEdge(2, 3)
	g.AddEdge(3, 1) // Creates cycle

	_, err := g.Sort()
	if err != ErrCycleDetected {
		t.Errorf("Expected ErrCycleDetected, got %v", err)
	}
}

func TestSortDFS(t *testing.T) {
	g := NewGraph[int]()
	g.AddNodes(1, 2, 3, 4)
	g.AddEdge(1, 2)
	g.AddEdge(2, 3)
	g.AddEdge(1, 4)

	result, err := g.SortDFS()
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	positions := make(map[int]int)
	for i, node := range result {
		positions[node] = i
	}

	// 1 must come before 2 and 4
	// 2 must come before 3
	if positions[1] >= positions[2] {
		t.Error("1 should come before 2")
	}
	if positions[2] >= positions[3] {
		t.Error("2 should come before 3")
	}
	if positions[1] >= positions[4] {
		t.Error("1 should come before 4")
	}
}

func TestSortDFSWithCycle(t *testing.T) {
	g := NewGraph[string]()
	g.AddNodes("X", "Y", "Z")
	g.AddEdge("X", "Y")
	g.AddEdge("Y", "Z")
	g.AddEdge("Z", "X") // Cycle

	_, err := g.SortDFS()
	if err != ErrCycleDetected {
		t.Errorf("Expected ErrCycleDetected, got %v", err)
	}
}

func TestDetectCycle(t *testing.T) {
	// Graph with cycle
	g1 := NewGraph[int]()
	g1.AddNodes(1, 2, 3)
	g1.AddEdge(1, 2)
	g1.AddEdge(2, 3)
	g1.AddEdge(3, 1)

	if !g1.DetectCycle() {
		t.Error("Expected cycle detection")
	}

	// Graph without cycle
	g2 := NewGraph[int]()
	g2.AddNodes(1, 2, 3)
	g2.AddEdge(1, 2)
	g2.AddEdge(2, 3)

	if g2.DetectCycle() {
		t.Error("Unexpected cycle detected")
	}
}

func TestFindCycle(t *testing.T) {
	g := NewGraph[int]()
	g.AddNodes(1, 2, 3, 4)
	g.AddEdge(1, 2)
	g.AddEdge(2, 3)
	g.AddEdge(3, 1) // Cycle: 1->2->3->1
	g.AddEdge(3, 4)

	cycle := g.FindCycle()
	if cycle == nil {
		t.Fatal("Expected cycle, got nil")
	}

	// Verify it's a valid cycle
	if len(cycle) < 2 {
		t.Error("Cycle too short")
	}

	// First and last should be same
	if cycle[0] != cycle[len(cycle)-1] {
		t.Errorf("Cycle should start and end with same node: %v", cycle)
	}
}

func TestFindCycleNoCycle(t *testing.T) {
	g := NewGraph[string]()
	g.AddNodes("A", "B", "C")
	g.AddEdge("A", "B")
	g.AddEdge("B", "C")

	cycle := g.FindCycle()
	if cycle != nil {
		t.Errorf("Expected no cycle, got %v", cycle)
	}
}

func TestLevels(t *testing.T) {
	// Example:
	// Level 0: A
	// Level 1: B, C
	// Level 2: D
	g := NewGraph[string]()
	g.AddNodes("A", "B", "C", "D")
	g.AddEdge("A", "B")
	g.AddEdge("A", "C")
	g.AddEdge("B", "D")
	g.AddEdge("C", "D")

	levels, err := g.Levels()
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if len(levels) != 3 {
		t.Errorf("Expected 3 levels, got %d", len(levels))
	}

	// Level 0 should contain A
	if !containsAll(levels[0], "A") {
		t.Errorf("Level 0 should contain A, got %v", levels[0])
	}

	// Level 1 should contain B and C
	if !containsAll(levels[1], "B", "C") {
		t.Errorf("Level 1 should contain B,C, got %v", levels[1])
	}

	// Level 2 should contain D
	if !containsAll(levels[2], "D") {
		t.Errorf("Level 2 should contain D, got %v", levels[2])
	}
}

func TestLevelsWithCycle(t *testing.T) {
	g := NewGraph[int]()
	g.AddNodes(1, 2, 3)
	g.AddEdge(1, 2)
	g.AddEdge(2, 3)
	g.AddEdge(3, 1) // Cycle

	_, err := g.Levels()
	if err != ErrCycleDetected {
		t.Errorf("Expected ErrCycleDetected, got %v", err)
	}
}

func TestLongestPath(t *testing.T) {
	g := NewGraph[string]()
	g.AddNodes("A", "B", "C", "D")
	g.AddEdge("A", "B")
	g.AddEdge("B", "C")
	g.AddEdge("A", "D")

	path, err := g.LongestPath("A")
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	// Longest path should be A->B->C (length 3)
	if len(path) != 3 {
		t.Errorf("Expected path length 3, got %d: %v", len(path), path)
	}

	// Path should start with A
	if path[0] != "A" {
		t.Errorf("Path should start with A, got %v", path)
	}
}

func TestLongestPathWithCycle(t *testing.T) {
	g := NewGraph[int]()
	g.AddNodes(1, 2, 3)
	g.AddEdge(1, 2)
	g.AddEdge(2, 3)
	g.AddEdge(3, 1) // Cycle

	_, err := g.LongestPath(1)
	if err != ErrCycleDetected {
		t.Errorf("Expected ErrCycleDetected, got %v", err)
	}
}

func TestCountAndEdgeCount(t *testing.T) {
	g := NewGraph[int]()
	g.AddNodes(1, 2, 3, 4)
	g.AddEdge(1, 2)
	g.AddEdge(2, 3)
	g.AddEdge(3, 4)

	if g.Count() != 4 {
		t.Errorf("Expected 4 nodes, got %d", g.Count())
	}

	if g.EdgeCount() != 3 {
		t.Errorf("Expected 3 edges, got %d", g.EdgeCount())
	}
}

func TestClear(t *testing.T) {
	g := NewGraph[int]()
	g.AddNodes(1, 2, 3)
	g.AddEdge(1, 2)

	g.Clear()

	if g.Count() != 0 {
		t.Errorf("Expected 0 nodes after clear, got %d", g.Count())
	}
	if g.EdgeCount() != 0 {
		t.Errorf("Expected 0 edges after clear, got %d", g.EdgeCount())
	}
}

func TestReverse(t *testing.T) {
	g := NewGraph[int]()
	g.AddNodes(1, 2, 3)
	g.AddEdge(1, 2)
	g.AddEdge(2, 3)

	rev := g.Reverse()

	// Original: 1->2, 2->3
	// Reversed: 2->1, 3->2
	edges1 := rev.GetEdges(2)
	if len(edges1) != 1 || edges1[0] != 1 {
		t.Errorf("Expected reversed edge 2->1, got %v", edges1)
	}

	edges2 := rev.GetEdges(3)
	if len(edges2) != 1 || edges2[0] != 2 {
		t.Errorf("Expected reversed edge 3->2, got %v", edges2)
	}
}

func TestAllPaths(t *testing.T) {
	g := NewGraph[string]()
	g.AddNodes("A", "B", "C", "D")
	g.AddEdge("A", "B")
	g.AddEdge("A", "C")
	g.AddEdge("B", "D")
	g.AddEdge("C", "D")

	paths := g.AllPaths("A", "D")
	if len(paths) != 2 {
		t.Errorf("Expected 2 paths, got %d", len(paths))
	}

	// Both paths should end with D
	for _, path := range paths {
		if path[len(path)-1] != "D" {
			t.Errorf("Path should end with D: %v", path)
		}
		if path[0] != "A" {
			t.Errorf("Path should start with A: %v", path)
		}
	}
}

func TestTopologicalSort(t *testing.T) {
	// Example: Build dependencies
	deps := map[string][]string{
		"app":    {"database", "config"},
		"config": {"env"},
		"database": {"env"},
		"env":     {},
	}

	result, err := TopologicalSort(deps)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	positions := make(map[string]int)
	for i, node := range result {
		positions[node] = i
	}

	// env must come before config and database
	// config and database must come before app
	if positions["env"] >= positions["config"] {
		t.Error("env should come before config")
	}
	if positions["env"] >= positions["database"] {
		t.Error("env should come before database")
	}
	if positions["config"] >= positions["app"] {
		t.Error("config should come before app")
	}
	if positions["database"] >= positions["app"] {
		t.Error("database should come before app")
	}
}

func TestDependencyResolver(t *testing.T) {
	r := NewDependencyResolver[string]()
	r.AddItem("app", "database", "config")
	r.AddItem("config", "env")
	r.AddItem("database", "env")
	r.AddItem("env")

	result, err := r.Resolve()
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	positions := make(map[string]int)
	for i, node := range result {
		positions[node] = i
	}

	// Verify order
	if positions["env"] >= positions["config"] {
		t.Error("env should come before config")
	}
	if positions["env"] >= positions["database"] {
		t.Error("env should come before database")
	}
	if positions["config"] >= positions["app"] {
		t.Error("config should come before app")
	}
	if positions["database"] >= positions["app"] {
		t.Error("database should come before app")
	}
}

func TestResolveItem(t *testing.T) {
	r := NewDependencyResolver[string]()
	r.AddItem("app", "database", "config")
	r.AddItem("config", "env")
	r.AddItem("database", "env")
	r.AddItem("env")

	result, err := r.ResolveItem("app")
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	// Should include all dependencies of app
	if !containsAll(result, "app", "database", "config", "env") {
		t.Errorf("Missing dependencies in result: %v", result)
	}
}

func TestResolveItemNotFound(t *testing.T) {
	r := NewDependencyResolver[int]()
	r.AddItem(1, 2)

	_, err := r.ResolveItem(99)
	if err != ErrNodeNotFound {
		t.Errorf("Expected ErrNodeNotFound, got %v", err)
	}
}

func TestEmptyGraph(t *testing.T) {
	g := NewGraph[int]()

	result, err := g.Sort()
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if len(result) != 0 {
		t.Errorf("Expected empty result, got %v", result)
	}

	levels, err := g.Levels()
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if len(levels) != 0 {
		t.Errorf("Expected empty levels, got %v", levels)
	}
}

func TestSingleGraph(t *testing.T) {
	g := NewGraph[string]()
	g.AddNode("A")

	result, err := g.Sort()
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if len(result) != 1 || result[0] != "A" {
		t.Errorf("Expected [A], got %v", result)
	}
}

func TestDisconnectedComponents(t *testing.T) {
	g := NewGraph[int]()
	// Two disconnected components: 1->2 and 3->4
	g.AddNodes(1, 2, 3, 4)
	g.AddEdge(1, 2)
	g.AddEdge(3, 4)

	result, err := g.Sort()
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	positions := make(map[int]int)
	for i, node := range result {
		positions[node] = i
	}

	// 1 before 2, 3 before 4
	if positions[1] >= positions[2] {
		t.Error("1 should come before 2")
	}
	if positions[3] >= positions[4] {
		t.Error("3 should come before 4")
	}
}

// Helper function
func containsAll[T comparable](slice []T, items ...T) bool {
	for _, item := range items {
		found := false
		for _, s := range slice {
			if s == item {
				found = true
				break
			}
		}
		if !found {
			return false
		}
	}
	return true
}

// Benchmark tests
func BenchmarkSort(b *testing.B) {
	g := NewGraph[int]()
	for i := 0; i < 1000; i++ {
		g.AddNode(i)
	}
	for i := 0; i < 999; i++ {
		g.AddEdge(i, i+1)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		g.Sort()
	}
}

func BenchmarkSortDFS(b *testing.B) {
	g := NewGraph[int]()
	for i := 0; i < 1000; i++ {
		g.AddNode(i)
	}
	for i := 0; i < 999; i++ {
		g.AddEdge(i, i+1)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		g.SortDFS()
	}
}

func BenchmarkDetectCycle(b *testing.B) {
	g := NewGraph[int]()
	for i := 0; i < 1000; i++ {
		g.AddNode(i)
	}
	for i := 0; i < 999; i++ {
		g.AddEdge(i, i+1)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		g.DetectCycle()
	}
}

func BenchmarkLevels(b *testing.B) {
	g := NewGraph[int]()
	for i := 0; i < 1000; i++ {
		g.AddNode(i)
	}
	for i := 0; i < 999; i++ {
		g.AddEdge(i, i+1)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		g.Levels()
	}
}