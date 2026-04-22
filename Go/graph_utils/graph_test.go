package graph_utils

import (
	"math"
	"testing"
)

// TestNewGraph tests graph creation
func TestNewGraph(t *testing.T) {
	g := NewGraph(5, Undirected)
	if g.Vertices() != 5 {
		t.Errorf("Expected 5 vertices, got %d", g.Vertices())
	}
	if g.Edges() != 0 {
		t.Errorf("Expected 0 edges, got %d", g.Edges())
	}
	if g.IsDirected() {
		t.Error("Undirected graph should not be directed")
	}

	dg := NewGraph(3, Directed)
	if !dg.IsDirected() {
		t.Error("Directed graph should be directed")
	}
}

// TestAddEdge tests adding edges
func TestAddEdge(t *testing.T) {
	g := NewGraph(3, Undirected)

	err := g.AddEdge(0, 1, 1.0)
	if err != nil {
		t.Errorf("AddEdge failed: %v", err)
	}
	if g.Edges() != 2 { // Undirected: 2 directed edges
		t.Errorf("Expected 2 edges, got %d", g.Edges())
	}
	if !g.HasEdge(0, 1) || !g.HasEdge(1, 0) {
		t.Error("Edge should exist in both directions")
	}

	// Test invalid vertex
	err = g.AddEdge(0, 10, 1.0)
	if err == nil {
		t.Error("Should fail for invalid vertex")
	}
}

// TestAddEdges tests adding multiple edges
func TestAddEdges(t *testing.T) {
	g := NewGraph(4, Undirected)
	edges := []Edge{
		{From: 0, To: 1, Weight: 1.0},
		{From: 1, To: 2, Weight: 2.0},
		{From: 2, To: 3, Weight: 3.0},
	}

	err := g.AddEdges(edges)
	if err != nil {
		t.Errorf("AddEdges failed: %v", err)
	}
	if g.Edges() != 6 {
		t.Errorf("Expected 6 edges, got %d", g.Edges())
	}
}

// TestRemoveEdge tests removing edges
func TestRemoveEdge(t *testing.T) {
	g := NewGraph(3, Undirected)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 2.0)

	removed := g.RemoveEdge(0, 1)
	if !removed {
		t.Error("Edge should be removed")
	}
	if g.HasEdge(0, 1) || g.HasEdge(1, 0) {
		t.Error("Edge should not exist after removal")
	}
	if g.Edges() != 2 { // Only edge 1-2 remains
		t.Errorf("Expected 2 edges, got %d", g.Edges())
	}

	removed = g.RemoveEdge(0, 2)
	if removed {
		t.Error("Non-existent edge should not be removed")
	}
}

// TestBFS tests breadth-first search
func TestBFS(t *testing.T) {
	g := NewGraph(6, Undirected)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(0, 2, 1.0)
	g.AddEdge(1, 3, 1.0)
	g.AddEdge(2, 4, 1.0)
	g.AddEdge(3, 5, 1.0)

	result, err := g.BFS(0)
	if err != nil {
		t.Errorf("BFS failed: %v", err)
	}

	if len(result) != 6 {
		t.Errorf("Expected 6 vertices in BFS result, got %d", len(result))
	}

	// First vertex should be 0
	if result[0] != 0 {
		t.Errorf("BFS should start with vertex 0, got %d", result[0])
	}

	// BFS order: 0 should be before its neighbors
	pos0 := indexOf(result, 0)
	pos1 := indexOf(result, 1)
	pos2 := indexOf(result, 2)
	if pos0 > pos1 || pos0 > pos2 {
		t.Error("BFS order incorrect: 0 should come before its neighbors")
	}
}

// TestDFS tests depth-first search
func TestDFS(t *testing.T) {
	g := NewGraph(5, Undirected)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(0, 2, 1.0)
	g.AddEdge(1, 3, 1.0)
	g.AddEdge(1, 4, 1.0)

	result, err := g.DFS(0)
	if err != nil {
		t.Errorf("DFS failed: %v", err)
	}

	if len(result) != 5 {
		t.Errorf("Expected 5 vertices, got %d", len(result))
	}

	// First vertex should be 0
	if result[0] != 0 {
		t.Errorf("DFS should start with vertex 0, got %d", result[0])
	}
}

// TestDFSIterative tests iterative DFS
func TestDFSIterative(t *testing.T) {
	g := NewGraph(5, Undirected)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(0, 2, 1.0)
	g.AddEdge(1, 3, 1.0)
	g.AddEdge(2, 4, 1.0)

	result, err := g.DFSIterative(0)
	if err != nil {
		t.Errorf("DFSIterative failed: %v", err)
	}

	if len(result) != 5 {
		t.Errorf("Expected 5 vertices, got %d", len(result))
	}
}

// TestDijkstra tests Dijkstra's algorithm
func TestDijkstra(t *testing.T) {
	g := NewGraph(5, Directed)
	g.AddEdge(0, 1, 10.0)
	g.AddEdge(0, 2, 3.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(1, 3, 2.0)
	g.AddEdge(2, 1, 4.0)
	g.AddEdge(2, 3, 8.0)
	g.AddEdge(2, 4, 2.0)
	g.AddEdge(3, 4, 7.0)
	g.AddEdge(4, 3, 9.0)

	result, err := g.Dijkstra(0)
	if err != nil {
		t.Errorf("Dijkstra failed: %v", err)
	}

	// Expected distances from 0:
	// 0->0: 0
	// 0->1: 7 (0->2->1)
	// 0->2: 3
	// 0->3: 9 (0->2->1->3)
	// 0->4: 5 (0->2->4)

	expectedDist := []float64{0, 7, 3, 9, 5}
	for i, d := range expectedDist {
		if math.Abs(result.Distances[i]-d) > 1e-9 {
			t.Errorf("Distance to %d: expected %.1f, got %.1f", i, d, result.Distances[i])
		}
	}

	// Test path reconstruction
	path := result.GetPath(4)
	if len(path) == 0 || path[0] != 0 || path[len(path)-1] != 4 {
		t.Errorf("Path to 4 incorrect: %v", path)
	}
}

// TestDijkstraUnreachable tests Dijkstra with unreachable vertices
func TestDijkstraUnreachable(t *testing.T) {
	g := NewGraph(4, Directed)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 1.0)
	// Vertex 3 is unreachable

	result, err := g.Dijkstra(0)
	if err != nil {
		t.Errorf("Dijkstra failed: %v", err)
	}

	if result.HasPath[3] {
		t.Error("Vertex 3 should not be reachable")
	}
	path := result.GetPath(3)
	if path != nil {
		t.Errorf("Path to unreachable vertex should be nil, got %v", path)
	}
}

// TestBellmanFord tests Bellman-Ford algorithm
func TestBellmanFord(t *testing.T) {
	g := NewGraph(4, Directed)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 2.0)
	g.AddEdge(2, 3, 3.0)
	g.AddEdge(0, 3, 10.0)

	result, err := g.BellmanFord(0)
	if err != nil {
		t.Errorf("BellmanFord failed: %v", err)
	}

	// Shortest path to 3 should be 0->1->2->3 = 6
	if math.Abs(result.Distances[3]-6.0) > 1e-9 {
		t.Errorf("Expected distance 6 to vertex 3, got %.1f", result.Distances[3])
	}
}

// TestBellmanFordNegativeCycle tests Bellman-Ford with negative cycle
func TestBellmanFordNegativeCycle(t *testing.T) {
	g := NewGraph(3, Directed)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, -2.0)
	g.AddEdge(2, 0, 1.0) // Creates negative cycle: 0->1->2->0 = 0

	_, err := g.BellmanFord(0)
	if err == nil {
		t.Error("Should detect negative cycle")
	}
}

// TestTopologicalSort tests topological sorting
func TestTopologicalSort(t *testing.T) {
	g := NewGraph(6, Directed)
	g.AddEdge(5, 2, 1.0)
	g.AddEdge(5, 0, 1.0)
	g.AddEdge(4, 0, 1.0)
	g.AddEdge(4, 1, 1.0)
	g.AddEdge(2, 3, 1.0)
	g.AddEdge(3, 1, 1.0)

	result, err := g.TopologicalSort()
	if err != nil {
		t.Errorf("TopologicalSort failed: %v", err)
	}

	// Verify topological order: all dependencies come before
	edges := g.GetAllEdges()
	for _, e := range edges {
		fromIdx := indexOf(result, e.From)
		toIdx := indexOf(result, e.To)
		if fromIdx > toIdx {
			t.Errorf("Invalid topological order: %d should come before %d", e.From, e.To)
		}
	}
}

// TestTopologicalSortUndirected tests topological sort on undirected graph
func TestTopologicalSortUndirected(t *testing.T) {
	g := NewGraph(3, Undirected)
	_, err := g.TopologicalSort()
	if err == nil {
		t.Error("Topological sort should fail on undirected graph")
	}
}

// TestHasCycleUndirected tests cycle detection in undirected graph
func TestHasCycleUndirected(t *testing.T) {
	// Graph with cycle
	g1 := NewGraph(3, Undirected)
	g1.AddEdge(0, 1, 1.0)
	g1.AddEdge(1, 2, 1.0)
	g1.AddEdge(2, 0, 1.0)
	if !g1.HasCycle() {
		t.Error("Graph 1 should have a cycle")
	}

	// Graph without cycle
	g2 := NewGraph(3, Undirected)
	g2.AddEdge(0, 1, 1.0)
	g2.AddEdge(1, 2, 1.0)
	if g2.HasCycle() {
		t.Error("Graph 2 should not have a cycle")
	}
}

// TestHasCycleDirected tests cycle detection in directed graph
func TestHasCycleDirected(t *testing.T) {
	// Graph with cycle
	g1 := NewGraph(3, Directed)
	g1.AddEdge(0, 1, 1.0)
	g1.AddEdge(1, 2, 1.0)
	g1.AddEdge(2, 0, 1.0)
	if !g1.HasCycle() {
		t.Error("Graph 1 should have a cycle")
	}

	// Graph without cycle (DAG)
	g2 := NewGraph(3, Directed)
	g2.AddEdge(0, 1, 1.0)
	g2.AddEdge(1, 2, 1.0)
	if g2.HasCycle() {
		t.Error("Graph 2 should not have a cycle")
	}
}

// TestConnectedComponents tests connected components
func TestConnectedComponents(t *testing.T) {
	// Graph with 2 connected components
	g := NewGraph(6, Undirected)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 1.0)
	g.AddEdge(3, 4, 1.0)
	g.AddEdge(4, 5, 1.0)

	components := g.ConnectedComponents()
	if len(components) != 2 {
		t.Errorf("Expected 2 components, got %d", len(components))
	}
}

// TestIsConnected tests connectivity check
func TestIsConnected(t *testing.T) {
	// Connected graph
	g1 := NewGraph(3, Undirected)
	g1.AddEdge(0, 1, 1.0)
	g1.AddEdge(1, 2, 1.0)
	if !g1.IsConnected() {
		t.Error("Graph 1 should be connected")
	}

	// Disconnected graph
	g2 := NewGraph(4, Undirected)
	g2.AddEdge(0, 1, 1.0)
	g2.AddEdge(2, 3, 1.0)
	if g2.IsConnected() {
		t.Error("Graph 2 should not be connected")
	}
}

// TestKruskal tests Kruskal's MST algorithm
func TestKruskal(t *testing.T) {
	g := NewGraph(4, Undirected)
	g.AddEdge(0, 1, 10.0)
	g.AddEdge(0, 2, 6.0)
	g.AddEdge(0, 3, 5.0)
	g.AddEdge(1, 3, 15.0)
	g.AddEdge(2, 3, 4.0)

	result, err := g.Kruskal()
	if err != nil {
		t.Errorf("Kruskal failed: %v", err)
	}

	// MST should have n-1 edges and total weight = 4+5+6 = 15
	if len(result.Edges) != 3 {
		t.Errorf("Expected 3 MST edges, got %d", len(result.Edges))
	}

	expectedWeight := 19.0 // 4 + 5 + 10 = 19 (corrected)
	if math.Abs(result.Weight-expectedWeight) > 1e-9 {
		t.Errorf("Expected MST weight %.1f, got %.1f", expectedWeight, result.Weight)
	}
}

// TestPrim tests Prim's MST algorithm
func TestPrim(t *testing.T) {
	g := NewGraph(4, Undirected)
	g.AddEdge(0, 1, 10.0)
	g.AddEdge(0, 2, 6.0)
	g.AddEdge(0, 3, 5.0)
	g.AddEdge(1, 3, 15.0)
	g.AddEdge(2, 3, 4.0)

	result, err := g.Prim(0)
	if err != nil {
		t.Errorf("Prim failed: %v", err)
	}

	// MST should have n-1 edges
	if len(result.Edges) != 3 {
		t.Errorf("Expected 3 MST edges, got %d", len(result.Edges))
	}

	// Total weight should match Kruskal
	kruskalResult, _ := g.Kruskal()
	if math.Abs(result.Weight-kruskalResult.Weight) > 1e-9 {
		t.Errorf("Prim and Kruskal MST weights should match")
	}
}

// TestMSTDirectedGraph tests MST on directed graph
func TestMSTDirectedGraph(t *testing.T) {
	g := NewGraph(3, Directed)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 1.0)

	_, err := g.Kruskal()
	if err == nil {
		t.Error("Kruskal should fail on directed graph")
	}

	_, err = g.Prim(0)
	if err == nil {
		t.Error("Prim should fail on directed graph")
	}
}

// TestBipartite tests bipartite check
func TestBipartite(t *testing.T) {
	// Bipartite graph
	g1 := NewGraph(4, Undirected)
	g1.AddEdge(0, 1, 1.0)
	g1.AddEdge(1, 2, 1.0)
	g1.AddEdge(2, 3, 1.0)
	g1.AddEdge(3, 0, 1.0)

	isBipartite, colors := g1.Bipartite()
	if !isBipartite {
		t.Error("Graph 1 should be bipartite")
	}
	if colors == nil {
		t.Error("Colors should be returned for bipartite graph")
	}

	// Non-bipartite graph (odd cycle)
	g2 := NewGraph(3, Undirected)
	g2.AddEdge(0, 1, 1.0)
	g2.AddEdge(1, 2, 1.0)
	g2.AddEdge(2, 0, 1.0)

	isBipartite, _ = g2.Bipartite()
	if isBipartite {
		t.Error("Graph 2 should not be bipartite")
	}
}

// TestDegree tests degree operations
func TestDegree(t *testing.T) {
	// Undirected graph
	g := NewGraph(4, Undirected)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(0, 2, 1.0)
	g.AddEdge(0, 3, 1.0)

	deg, err := g.Degree(0)
	if err != nil {
		t.Errorf("Degree failed: %v", err)
	}
	if deg != 3 {
		t.Errorf("Expected degree 3, got %d", deg)
	}

	// Directed graph
	dg := NewGraph(3, Directed)
	dg.AddEdge(0, 1, 1.0)
	dg.AddEdge(2, 0, 1.0)

	outDeg, _ := dg.Degree(0)
	inDeg, _ := dg.InDegree(0)

	if outDeg != 1 {
		t.Errorf("Expected out-degree 1, got %d", outDeg)
	}
	if inDeg != 1 {
		t.Errorf("Expected in-degree 1, got %d", inDeg)
	}
}

// TestClone tests graph cloning
func TestClone(t *testing.T) {
	g := NewGraph(3, Undirected)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 2.0)

	clone := g.Clone()
	if clone.Vertices() != g.Vertices() {
		t.Error("Clone should have same number of vertices")
	}
	if clone.Edges() != g.Edges() {
		t.Error("Clone should have same number of edges")
	}

	// Modify original
	g.RemoveEdge(0, 1)
	if g.HasEdge(0, 1) {
		t.Error("Original should be modified")
	}
	if !clone.HasEdge(0, 1) {
		t.Error("Clone should not be affected by original modification")
	}
}

// TestTranspose tests graph transpose
func TestTranspose(t *testing.T) {
	g := NewGraph(3, Directed)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 2.0)

	tg, err := g.Transpose()
	if err != nil {
		t.Errorf("Transpose failed: %v", err)
	}

	if !tg.HasEdge(1, 0) {
		t.Error("Transpose should have reversed edge 1->0")
	}
	if !tg.HasEdge(2, 1) {
		t.Error("Transpose should have reversed edge 2->1")
	}
	if tg.HasEdge(0, 1) {
		t.Error("Transpose should not have original edge 0->1")
	}
}

// TestTransposeUndirected tests transpose on undirected graph
func TestTransposeUndirected(t *testing.T) {
	g := NewGraph(3, Undirected)
	g.AddEdge(0, 1, 1.0)

	_, err := g.Transpose()
	if err == nil {
		t.Error("Transpose should fail on undirected graph")
	}
}

// TestGetAllEdges tests getting all edges
func TestGetAllEdges(t *testing.T) {
	g := NewGraph(3, Undirected)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(1, 2, 2.0)

	edges := g.GetAllEdges()
	if len(edges) != 2 {
		t.Errorf("Expected 2 unique edges, got %d", len(edges))
	}
}

// TestGetNeighbors tests getting neighbors
func TestGetNeighbors(t *testing.T) {
	g := NewGraph(3, Undirected)
	g.AddEdge(0, 1, 1.0)
	g.AddEdge(0, 2, 2.0)

	neighbors, err := g.GetNeighbors(0)
	if err != nil {
		t.Errorf("GetNeighbors failed: %v", err)
	}
	if len(neighbors) != 2 {
		t.Errorf("Expected 2 neighbors, got %d", len(neighbors))
	}

	// Test invalid vertex
	_, err = g.GetNeighbors(10)
	if err == nil {
		t.Error("Should fail for invalid vertex")
	}
}

// TestString tests string representation
func TestString(t *testing.T) {
	g := NewGraph(3, Undirected)
	g.AddEdge(0, 1, 1.0)

	s := g.String()
	if s == "" {
		t.Error("String representation should not be empty")
	}
}

// TestEmptyGraph tests operations on empty graph
func TestEmptyGraph(t *testing.T) {
	g := NewGraph(0, Undirected)

	if g.Vertices() != 0 {
		t.Error("Empty graph should have 0 vertices")
	}
	if g.Edges() != 0 {
		t.Error("Empty graph should have 0 edges")
	}

	components := g.ConnectedComponents()
	if len(components) != 0 {
		t.Error("Empty graph should have 0 components")
	}
}

// TestSingleVertex tests operations on single vertex graph
func TestSingleVertex(t *testing.T) {
	g := NewGraph(1, Undirected)

	bfs, err := g.BFS(0)
	if err != nil || len(bfs) != 1 {
		t.Error("BFS on single vertex should work")
	}

	dfs, err := g.DFS(0)
	if err != nil || len(dfs) != 1 {
		t.Error("DFS on single vertex should work")
	}

	// MST on single vertex
	_, err = g.Kruskal()
	if err != nil {
		t.Error("Kruskal on single vertex should work")
	}
}

// TestLargeGraph tests performance on larger graph
func TestLargeGraph(t *testing.T) {
	n := 100
	g := NewGraph(n, Undirected)

	// Create a connected graph
	for i := 0; i < n-1; i++ {
		g.AddEdge(i, i+1, float64(i+1))
	}

	// BFS should visit all vertices
	bfs, _ := g.BFS(0)
	if len(bfs) != n {
		t.Errorf("BFS should visit all %d vertices, got %d", n, len(bfs))
	}

	// DFS should visit all vertices
	dfs, _ := g.DFS(0)
	if len(dfs) != n {
		t.Errorf("DFS should visit all %d vertices, got %d", n, len(dfs))
	}

	// Should be connected
	if !g.IsConnected() {
		t.Error("Graph should be connected")
	}

	// Dijkstra
	result, err := g.Dijkstra(0)
	if err != nil {
		t.Errorf("Dijkstra failed: %v", err)
	}
	if !result.HasPath[n-1] {
		t.Error("Path to last vertex should exist")
	}
}

// Helper function
func indexOf(slice []int, val int) int {
	for i, v := range slice {
		if v == val {
			return i
		}
	}
	return -1
}