// Package dijkstra_utils_test provides tests for Dijkstra's algorithm implementation.
package dijkstra_utils

import (
	"math"
	"testing"
)

func TestNewGraph(t *testing.T) {
	graph := NewGraph[string](Directed)
	if graph == nil {
		t.Fatal("NewGraph returned nil")
	}
	if graph.nodeCount != 0 {
		t.Errorf("Expected nodeCount 0, got %d", graph.nodeCount)
	}
	if graph.edgeCount != 0 {
		t.Errorf("Expected edgeCount 0, got %d", graph.edgeCount)
	}
	if !graph.directed {
		t.Error("Expected directed graph")
	}
}

func TestNewGraphUndirected(t *testing.T) {
	graph := NewGraph[string](Undirected)
	if graph == nil {
		t.Fatal("NewGraph returned nil")
	}
	if graph.directed {
		t.Error("Expected undirected graph")
	}
}

func TestAddNode(t *testing.T) {
	graph := NewGraph[int](Directed)
	graph.AddNode(1)
	graph.AddNode(2)
	graph.AddNode(1) // Duplicate

	if graph.nodeCount != 2 {
		t.Errorf("Expected 2 nodes, got %d", graph.nodeCount)
	}
	if !graph.HasNode(1) || !graph.HasNode(2) {
		t.Error("Expected nodes 1 and 2 to exist")
	}
}

func TestAddEdge(t *testing.T) {
	graph := NewGraph[int](Directed)
	err := graph.AddEdge(1, 2, 4.0)
	if err != nil {
		t.Fatalf("AddEdge failed: %v", err)
	}

	if graph.nodeCount != 2 {
		t.Errorf("Expected 2 nodes, got %d", graph.nodeCount)
	}
	if graph.edgeCount != 1 {
		t.Errorf("Expected 1 edge, got %d", graph.edgeCount)
	}
	if !graph.HasEdge(1, 2) {
		t.Error("Expected edge (1, 2) to exist")
	}
	if graph.HasEdge(2, 1) {
		t.Error("Expected edge (2, 1) to not exist in directed graph")
	}
}

func TestAddEdgeUndirected(t *testing.T) {
	graph := NewGraph[int](Undirected)
	err := graph.AddEdge(1, 2, 4.0)
	if err != nil {
		t.Fatalf("AddEdge failed: %v", err)
	}

	if graph.nodeCount != 2 {
		t.Errorf("Expected 2 nodes, got %d", graph.nodeCount)
	}
	if graph.edgeCount != 2 {
		t.Errorf("Expected 2 edges in undirected graph, got %d", graph.edgeCount)
	}
	if !graph.HasEdge(1, 2) || !graph.HasEdge(2, 1) {
		t.Error("Expected bidirectional edges in undirected graph")
	}
}

func TestAddEdgeNegativeWeight(t *testing.T) {
	graph := NewGraph[int](Directed)
	err := graph.AddEdge(1, 2, -1.0)
	if err == nil {
		t.Error("Expected error for negative weight")
	}
}

func TestGetEdgeWeight(t *testing.T) {
	graph := NewGraph[int](Directed)
	graph.AddEdge(1, 2, 4.0)

	weight := graph.GetEdgeWeight(1, 2)
	if weight != 4.0 {
		t.Errorf("Expected weight 4.0, got %f", weight)
	}

	weight = graph.GetEdgeWeight(2, 1)
	if weight != -1 {
		t.Errorf("Expected weight -1 for non-existent edge, got %f", weight)
	}
}

func TestRemoveNode(t *testing.T) {
	graph := NewGraph[int](Directed)
	graph.AddEdge(1, 2, 4.0)
	graph.AddEdge(2, 3, 5.0)
	graph.AddEdge(3, 1, 2.0)

	graph.RemoveNode(2)

	if graph.HasNode(2) {
		t.Error("Expected node 2 to be removed")
	}
	if graph.HasEdge(1, 2) || graph.HasEdge(2, 3) {
		t.Error("Expected edges involving node 2 to be removed")
	}
}

func TestRemoveEdge(t *testing.T) {
	graph := NewGraph[int](Directed)
	graph.AddEdge(1, 2, 4.0)
	graph.AddEdge(1, 3, 5.0)

	graph.RemoveEdge(1, 2)

	if graph.HasEdge(1, 2) {
		t.Error("Expected edge (1, 2) to be removed")
	}
	if !graph.HasEdge(1, 3) {
		t.Error("Expected edge (1, 3) to still exist")
	}
}

func TestGetNeighbors(t *testing.T) {
	graph := NewGraph[int](Directed)
	graph.AddEdge(1, 2, 4.0)
	graph.AddEdge(1, 3, 5.0)

	neighbors := graph.GetNeighbors(1)
	if len(neighbors) != 2 {
		t.Errorf("Expected 2 neighbors, got %d", len(neighbors))
	}
}

func TestNodes(t *testing.T) {
	graph := NewGraph[int](Directed)
	graph.AddEdge(1, 2, 4.0)
	graph.AddEdge(3, 4, 5.0)

	nodes := graph.Nodes()
	if len(nodes) != 4 {
		t.Errorf("Expected 4 nodes, got %d", len(nodes))
	}
}

func TestShortestPathSimple(t *testing.T) {
	graph := NewGraph[int](Directed)
	graph.AddEdge(1, 2, 4.0)
	graph.AddEdge(2, 3, 3.0)

	result := graph.ShortestPath(1, 3)
	if !result.Found {
		t.Fatal("Expected path to be found")
	}
	if result.Distance != 7.0 {
		t.Errorf("Expected distance 7.0, got %f", result.Distance)
	}
	expectedPath := []int{1, 2, 3}
	if len(result.Path) != len(expectedPath) {
		t.Errorf("Expected path length %d, got %d", len(expectedPath), len(result.Path))
	}
	for i, node := range expectedPath {
		if result.Path[i] != node {
			t.Errorf("Expected path node %d at index %d, got %d", node, i, result.Path[i])
		}
	}
}

func TestShortestPathComplex(t *testing.T) {
	// Create a more complex graph
	// A --4-- B --5-- D
	// |       |       |
	// 2       1       6
	// |       |       |
	// C --8-- D --2-- E --3-- Z
	//   \____10____/
	graph := NewGraph[string](Undirected)
	graph.AddEdge("A", "B", 4.0)
	graph.AddEdge("A", "C", 2.0)
	graph.AddEdge("B", "C", 1.0)
	graph.AddEdge("B", "D", 5.0)
	graph.AddEdge("C", "D", 8.0)
	graph.AddEdge("C", "E", 10.0)
	graph.AddEdge("D", "E", 2.0)
	graph.AddEdge("D", "Z", 6.0)
	graph.AddEdge("E", "Z", 3.0)

	result := graph.ShortestPath("A", "Z")
	if !result.Found {
		t.Fatal("Expected path to be found")
	}
	// Shortest path: A -> C -> B -> D -> E -> Z = 2+1+5+2+3 = 13
	if result.Distance != 13.0 {
		t.Errorf("Expected distance 13.0, got %f", result.Distance)
	}
}

func TestShortestPathNotFound(t *testing.T) {
	graph := NewGraph[int](Directed)
	graph.AddEdge(1, 2, 4.0)

	result := graph.ShortestPath(1, 3) // Node 3 doesn't exist
	if result.Found {
		t.Error("Expected path to not be found")
	}
}

func TestShortestPathDisconnected(t *testing.T) {
	graph := NewGraph[int](Directed)
	graph.AddEdge(1, 2, 4.0)
	graph.AddEdge(3, 4, 5.0) // Disconnected component

	result := graph.ShortestPath(1, 4)
	if result.Found {
		t.Error("Expected path to not be found for disconnected nodes")
	}
}

func TestShortestPathSameNode(t *testing.T) {
	graph := NewGraph[int](Directed)
	graph.AddEdge(1, 2, 4.0)

	result := graph.ShortestPath(1, 1)
	if !result.Found {
		t.Fatal("Expected path to be found for same node")
	}
	if result.Distance != 0 {
		t.Errorf("Expected distance 0, got %f", result.Distance)
	}
	if len(result.Path) != 1 || result.Path[0] != 1 {
		t.Errorf("Expected path [1], got %v", result.Path)
	}
}

func TestShortestPathsFrom(t *testing.T) {
	graph := NewGraph[string](Directed)
	graph.AddEdge("A", "B", 4.0)
	graph.AddEdge("A", "C", 2.0)
	graph.AddEdge("B", "D", 5.0)
	graph.AddEdge("C", "D", 8.0)

	result := graph.ShortestPathsFrom("A")

	if _, ok := result.Distances["B"]; !ok {
		t.Error("Expected distance to B")
	}
	if result.Distances["B"] != 4.0 {
		t.Errorf("Expected distance to B = 4.0, got %f", result.Distances["B"])
	}
	// A -> B -> D = 4+5 = 9
	if result.Distances["D"] != 9.0 {
		t.Errorf("Expected distance to D = 9.0, got %f", result.Distances["D"])
	}
}

func TestGetPathTo(t *testing.T) {
	graph := NewGraph[string](Directed)
	graph.AddEdge("A", "B", 4.0)
	graph.AddEdge("B", "C", 3.0)

	allPaths := graph.ShortestPathsFrom("A")
	pathResult := allPaths.GetPathTo("C")

	if !pathResult.Found {
		t.Fatal("Expected path to be found")
	}
	if pathResult.Distance != 7.0 {
		t.Errorf("Expected distance 7.0, got %f", pathResult.Distance)
	}
}

func TestKShortestPaths(t *testing.T) {
	// Create a graph with multiple paths between nodes
	graph := NewGraph[string](Undirected)
	graph.AddEdge("A", "B", 1.0)
	graph.AddEdge("B", "C", 1.0)
	graph.AddEdge("A", "C", 3.0) // Direct path (longer)
	graph.AddEdge("A", "D", 1.0)
	graph.AddEdge("D", "C", 1.0) // Another path via D

	paths := graph.KShortestPaths("A", "C", 3)

	if len(paths) < 1 {
		t.Fatalf("Expected at least 1 path, got %d", len(paths))
	}

	// First path should be shortest (A -> B -> C or A -> D -> C, both have distance 2)
	if paths[0].Distance != 2.0 {
		t.Errorf("Expected shortest path distance 2.0, got %f", paths[0].Distance)
	}

	// Paths should be sorted by distance
	for i := 1; i < len(paths); i++ {
		if paths[i-1].Distance > paths[i].Distance {
			t.Errorf("Expected paths to be sorted by distance")
		}
	}
}

func TestKShortestPathsSinglePath(t *testing.T) {
	graph := NewGraph[string](Directed)
	graph.AddEdge("A", "B", 4.0)

	paths := graph.KShortestPaths("A", "B", 3)

	if len(paths) != 1 {
		t.Errorf("Expected 1 path, got %d", len(paths))
	}
}

func TestIsConnected(t *testing.T) {
	graph := NewGraph[int](Directed)
	graph.AddEdge(1, 2, 4.0)
	graph.AddEdge(2, 3, 5.0)

	if !graph.IsConnected(1, 3) {
		t.Error("Expected nodes 1 and 3 to be connected")
	}
	if graph.IsConnected(1, 4) {
		t.Error("Expected nodes 1 and 4 to not be connected")
	}
}

func TestGetReachableNodes(t *testing.T) {
	graph := NewGraph[int](Directed)
	graph.AddEdge(1, 2, 4.0)
	graph.AddEdge(2, 3, 5.0)
	graph.AddEdge(4, 5, 1.0) // Disconnected component

	reachable := graph.GetReachableNodes(1)

	if len(reachable) != 3 {
		t.Errorf("Expected 3 reachable nodes, got %d", len(reachable))
	}
}

func TestGraphDiameter(t *testing.T) {
	// Linear graph: 1 -- 2 -- 3 -- 4
	// Diameter should be distance from 1 to 4 = 3
	graph := NewGraph[int](Undirected)
	graph.AddEdge(1, 2, 1.0)
	graph.AddEdge(2, 3, 1.0)
	graph.AddEdge(3, 4, 1.0)

	diameter, _, _ := graph.GraphDiameter()
	if diameter != 3.0 {
		t.Errorf("Expected diameter 3.0, got %f", diameter)
	}
}

func TestCenterOfGraph(t *testing.T) {
	// Linear graph: 1 -- 2 -- 3 -- 4 -- 5
	// Center should be node 3 (min eccentricity = 2)
	graph := NewGraph[int](Undirected)
	graph.AddEdge(1, 2, 1.0)
	graph.AddEdge(2, 3, 1.0)
	graph.AddEdge(3, 4, 1.0)
	graph.AddEdge(4, 5, 1.0)

	center := graph.CenterOfGraph()
	if len(center) != 1 || center[0] != 3 {
		t.Errorf("Expected center [3], got %v", center)
	}
}

func TestClear(t *testing.T) {
	graph := NewGraph[int](Directed)
	graph.AddEdge(1, 2, 4.0)
	graph.AddEdge(2, 3, 5.0)

	graph.Clear()

	if graph.nodeCount != 0 {
		t.Errorf("Expected 0 nodes after clear, got %d", graph.nodeCount)
	}
	if graph.edgeCount != 0 {
		t.Errorf("Expected 0 edges after clear, got %d", graph.edgeCount)
	}
}

func TestFromAdjacencyList(t *testing.T) {
	adjList := map[string][]struct{ Node string; Weight float64 }{
		"A": {{Node: "B", Weight: 4.0}, {Node: "C", Weight: 2.0}},
		"B": {{Node: "C", Weight: 1.0}},
		"C": {{Node: "D", Weight: 5.0}},
	}

	graph := FromAdjacencyList(adjList, true)

	if graph.nodeCount != 4 {
		t.Errorf("Expected 4 nodes, got %d", graph.nodeCount)
	}
	if !graph.HasEdge("A", "B") {
		t.Error("Expected edge A -> B")
	}

	result := graph.ShortestPath("A", "D")
	if !result.Found {
		t.Fatal("Expected path to be found")
	}
}

func TestFromEdgeList(t *testing.T) {
	edges := []struct{ Source, Target string; Weight float64 }{
		{Source: "A", Target: "B", Weight: 4.0},
		{Source: "B", Target: "C", Weight: 3.0},
	}

	graph := FromEdgeList(edges, true)

	if graph.nodeCount != 3 {
		t.Errorf("Expected 3 nodes, got %d", graph.nodeCount)
	}

	result := graph.ShortestPath("A", "C")
	if !result.Found {
		t.Fatal("Expected path to be found")
	}
	if result.Distance != 7.0 {
		t.Errorf("Expected distance 7.0, got %f", result.Distance)
	}
}

func TestConvenienceFunctions(t *testing.T) {
	graph := NewGraph[int](Directed)
	graph.AddEdge(1, 2, 4.0)
	graph.AddEdge(2, 3, 5.0)

	// Test ShortestPath convenience function
	result := ShortestPath(graph, 1, 3)
	if !result.Found {
		t.Fatal("ShortestPath convenience function failed")
	}

	// Test AllShortestPaths convenience function
	allPaths := AllShortestPaths(graph, 1)
	if _, ok := allPaths.Distances[3]; !ok {
		t.Error("AllShortestPaths convenience function failed")
	}
}

func TestLargeGraph(t *testing.T) {
	// Create a larger graph for performance test
	graph := NewGraph[int](Directed)

	// Create a grid-like graph
	for i := 0; i < 100; i++ {
		// Horizontal edges
		if i % 10 < 9 {
			graph.AddEdge(i, i+1, 1.0)
		}
		// Vertical edges
		if i < 90 {
			graph.AddEdge(i, i+10, 1.0)
		}
	}

	// Find path from top-left to bottom-right
	result := graph.ShortestPath(0, 99)
	if !result.Found {
		t.Fatal("Expected path to be found in large graph")
	}

	// Should go 9 right + 9 down = 18
	expectedDist := 18.0
	if result.Distance != expectedDist {
		t.Errorf("Expected distance %f, got %f", expectedDist, result.Distance)
	}
}

func TestNegativeWeightRejection(t *testing.T) {
	graph := NewGraph[int](Directed)

	// Try to add multiple edges, one with negative weight
	err := graph.AddEdges([]struct{ Source, Target int; Weight float64 }{
		{Source: 1, Target: 2, Weight: 4.0},
		{Source: 2, Target: 3, Weight: -1.0}, // This should fail
	})

	if err == nil {
		t.Error("Expected error for negative weight in AddEdges")
	}

	// First edge should have been added
	if !graph.HasEdge(1, 2) {
		t.Error("Expected edge (1, 2) to exist even after failed AddEdges")
	}
}

func TestPathResultString(t *testing.T) {
	foundResult := PathResult[int]{Distance: 10.0, Path: []int{1, 2, 3}, Found: true}
	if foundResult.Distance != 10.0 {
		t.Errorf("Expected distance 10.0, got %f", foundResult.Distance)
	}

	notFoundResult := PathResult[int]{Distance: math.Inf(1), Path: nil, Found: false}
	if notFoundResult.Found {
		t.Error("Expected not found")
	}
}

func TestGraphNodeTypes(t *testing.T) {
	// Test with different node types

	// Int nodes
	graphInt := NewGraph[int](Directed)
	graphInt.AddEdge(1, 2, 1.0)
	resultInt := graphInt.ShortestPath(1, 2)
	if !resultInt.Found {
		t.Error("Expected path in int graph")
	}

	// String nodes
	graphStr := NewGraph[string](Directed)
	graphStr.AddEdge("A", "B", 1.0)
	resultStr := graphStr.ShortestPath("A", "B")
	if !resultStr.Found {
		t.Error("Expected path in string graph")
	}
}

func BenchmarkShortestPath(b *testing.B) {
	// Create a medium-sized graph
	graph := NewGraph[int](Directed)
	for i := 0; i < 1000; i++ {
		if i < 999 {
			graph.AddEdge(i, i+1, 1.0)
		}
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		graph.ShortestPath(0, 999)
	}
}

func BenchmarkShortestPathsFrom(b *testing.B) {
	// Create a medium-sized graph
	graph := NewGraph[int](Undirected)
	for i := 0; i < 100; i++ {
		if i % 10 < 9 {
			graph.AddEdge(i, i+1, 1.0)
		}
		if i < 90 {
			graph.AddEdge(i, i+10, 1.0)
		}
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		graph.ShortestPathsFrom(0)
	}
}

func BenchmarkKShortestPaths(b *testing.B) {
	// Create a graph with multiple paths
	graph := NewGraph[int](Undirected)
	for i := 0; i < 50; i++ {
		graph.AddEdge(i, i+1, 1.0)
		graph.AddEdge(i, i+50, 2.0)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		graph.KShortestPaths(0, 99, 3)
	}
}