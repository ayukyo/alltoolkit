package disjoint_set

import (
	"testing"
)

func TestNew(t *testing.T) {
	ds := New(5)
	if ds.Size() != 5 {
		t.Errorf("Expected size 5, got %d", ds.Size())
	}
	if ds.Count() != 5 {
		t.Errorf("Expected 5 disjoint sets, got %d", ds.Count())
	}
}

func TestFind(t *testing.T) {
	ds := New(5)
	for i := 0; i < 5; i++ {
		if ds.Find(i) != i {
			t.Errorf("Expected Find(%d) = %d, got %d", i, i, ds.Find(i))
		}
	}
	// Test invalid element
	if ds.Find(-1) != -1 {
		t.Errorf("Expected Find(-1) = -1, got %d", ds.Find(-1))
	}
	if ds.Find(100) != -1 {
		t.Errorf("Expected Find(100) = -1, got %d", ds.Find(100))
	}
}

func TestUnion(t *testing.T) {
	ds := New(5)
	
	// Union 0 and 1
	if !ds.Union(0, 1) {
		t.Error("Union(0, 1) should return true")
	}
	if ds.Count() != 4 {
		t.Errorf("Expected 4 disjoint sets, got %d", ds.Count())
	}
	if !ds.Connected(0, 1) {
		t.Error("0 and 1 should be connected")
	}
	
	// Union same elements again
	if ds.Union(0, 1) {
		t.Error("Union(0, 1) again should return false")
	}
	
	// Union 1 and 2 (transitive)
	if !ds.Union(1, 2) {
		t.Error("Union(1, 2) should return true")
	}
	if !ds.Connected(0, 2) {
		t.Error("0 and 2 should be connected (transitive)")
	}
}

func TestConnected(t *testing.T) {
	ds := New(5)
	
	if ds.Connected(0, 1) {
		t.Error("0 and 1 should not be connected initially")
	}
	
	ds.Union(0, 1)
	if !ds.Connected(0, 1) {
		t.Error("0 and 1 should be connected after union")
	}
	
	// Test invalid elements
	if ds.Connected(-1, 0) {
		t.Error("-1 and 0 should not be connected (invalid element)")
	}
}

func TestSetSize(t *testing.T) {
	ds := New(5)
	
	if ds.SetSize(0) != 1 {
		t.Errorf("Expected SetSize(0) = 1, got %d", ds.SetSize(0))
	}
	
	ds.Union(0, 1)
	ds.Union(0, 2)
	
	if ds.SetSize(0) != 3 {
		t.Errorf("Expected SetSize(0) = 3, got %d", ds.SetSize(0))
	}
	if ds.SetSize(3) != 1 {
		t.Errorf("Expected SetSize(3) = 1, got %d", ds.SetSize(3))
	}
}

func TestSets(t *testing.T) {
	ds := New(5)
	ds.Union(0, 1)
	ds.Union(2, 3)
	
	sets := ds.Sets()
	if len(sets) != 3 {
		t.Errorf("Expected 3 sets, got %d", len(sets))
	}
}

func TestElements(t *testing.T) {
	ds := New(5)
	ds.Union(0, 1)
	ds.Union(0, 2)
	
	elements := ds.Elements(0)
	if len(elements) != 3 {
		t.Errorf("Expected 3 elements, got %d", len(elements))
	}
	
	// Check if all expected elements are present
	elementMap := make(map[int]bool)
	for _, e := range elements {
		elementMap[e] = true
	}
	for _, expected := range []int{0, 1, 2} {
		if !elementMap[expected] {
			t.Errorf("Expected element %d in set", expected)
		}
	}
}

func TestReset(t *testing.T) {
	ds := New(5)
	ds.Union(0, 1)
	ds.Union(2, 3)
	
	ds.Reset()
	
	if ds.Count() != 5 {
		t.Errorf("Expected 5 disjoint sets after reset, got %d", ds.Count())
	}
	if ds.Connected(0, 1) {
		t.Error("0 and 1 should not be connected after reset")
	}
}

func TestWeightedDisjointSet(t *testing.T) {
	wds := NewWeighted(5)
	
	if wds.SetSize(0) != 1 {
		t.Errorf("Expected SetSize(0) = 1, got %d", wds.SetSize(0))
	}
	
	wds.Union(0, 1)
	wds.Union(0, 2)
	
	if wds.SetSize(0) != 3 {
		t.Errorf("Expected SetSize(0) = 3, got %d", wds.SetSize(0))
	}
	if wds.Count() != 3 {
		t.Errorf("Expected 3 disjoint sets, got %d", wds.Count())
	}
}

func TestCountComponents(t *testing.T) {
	// Graph: 0-1-2, 3-4
	edges := [][2]int{{0, 1}, {1, 2}, {3, 4}}
	count := CountComponents(5, edges)
	
	if count != 2 {
		t.Errorf("Expected 2 components, got %d", count)
	}
	
	// Graph: all connected
	edges = [][2]int{{0, 1}, {1, 2}, {2, 3}, {3, 4}}
	count = CountComponents(5, edges)
	
	if count != 1 {
		t.Errorf("Expected 1 component, got %d", count)
	}
}

func TestFindRedundantConnection(t *testing.T) {
	// Graph with cycle: edges 0-1, 1-2, 2-0 (redundant)
	edges := [][2]int{
		{1, 2},
		{1, 3},
		{2, 3}, // This creates a cycle
	}
	
	from, to := FindRedundantConnection(3, edges)
	if from != 2 || to != 3 {
		t.Errorf("Expected redundant edge (2, 3), got (%d, %d)", from, to)
	}
}

func TestIsBipartite(t *testing.T) {
	// Bipartite graph
	graph := [][]int{
		{1, 3},    // 0 connects to 1, 3
		{0, 2},    // 1 connects to 0, 2
		{1, 3},    // 2 connects to 1, 3
		{0, 2},    // 3 connects to 0, 2
	}
	
	if !IsBipartite(graph) {
		t.Error("Expected graph to be bipartite")
	}
	
	// Non-bipartite graph (triangle)
	graph = [][]int{
		{1, 2},
		{0, 2},
		{0, 1},
	}
	
	if IsBipartite(graph) {
		t.Error("Expected graph to NOT be bipartite")
	}
}

func TestMSTKruskal(t *testing.T) {
	// Graph with 4 nodes: MST weight = 1+1+2 = 4
	edges := []Edge{
		{0, 1, 4},
		{0, 2, 1},
		{1, 3, 2},
		{2, 3, 1},
	}
	
	totalWeight, mstEdges := MSTKruskal(4, edges)
	
	if totalWeight != 4 {
		t.Errorf("Expected total weight 4, got %d", totalWeight)
	}
	if len(mstEdges) != 3 {
		t.Errorf("Expected 3 MST edges, got %d", len(mstEdges))
	}
}

func TestPathCompression(t *testing.T) {
	ds := New(10)
	
	// Create a long chain
	for i := 0; i < 9; i++ {
		ds.Union(i, i+1)
	}
	
	// After path compression, all should have the same root
	root := ds.Find(0)
	for i := 1; i < 10; i++ {
		if ds.Find(i) != root {
			t.Errorf("Path compression failed for element %d", i)
		}
	}
}

func TestUnionByRank(t *testing.T) {
	ds := New(100)
	
	// Union elements in a way that tests rank
	for i := 0; i < 99; i++ {
		ds.Union(i, i+1)
	}
	
	if ds.Count() != 1 {
		t.Errorf("Expected 1 set after all unions, got %d", ds.Count())
	}
}

func BenchmarkUnionFind(b *testing.B) {
	ds := New(b.N)
	for i := 0; i < b.N; i++ {
		ds.Find(i % 1000)
	}
	for i := 0; i < b.N-1; i++ {
		ds.Union(i, i+1)
	}
}

func BenchmarkUnionFindWorstCase(b *testing.B) {
	ds := New(b.N)
	for i := 0; i < b.N-1; i++ {
		ds.Union(i, i+1)
	}
	for i := 0; i < b.N; i++ {
		ds.Find(0)
	}
}