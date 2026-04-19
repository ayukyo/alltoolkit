// Package disjoint_set implements a Union-Find (Disjoint Set) data structure.
// It provides efficient operations for managing disjoint sets with path compression
// and union by rank optimizations.
//
// Time Complexity:
//   - Find: O(α(n)) amortized, where α is the inverse Ackermann function
//   - Union: O(α(n)) amortized
//   - Connected: O(α(n)) amortized
//
// Space Complexity: O(n)
package disjoint_set

// DisjointSet represents a Union-Find data structure with path compression
// and union by rank optimizations.
type DisjointSet struct {
	parent []int
	rank   []int
	count   int // number of disjoint sets
}

// New creates a new DisjointSet with n elements (0 to n-1).
// Initially, each element is in its own set.
func New(n int) *DisjointSet {
	parent := make([]int, n)
	rank := make([]int, n)
	for i := 0; i < n; i++ {
		parent[i] = i
		rank[i] = 0
	}
	return &DisjointSet{
		parent: parent,
		rank:   rank,
		count:  n,
	}
}

// Find returns the root (representative) of the set containing element x.
// Uses path compression for efficiency.
func (ds *DisjointSet) Find(x int) int {
	if x < 0 || x >= len(ds.parent) {
		return -1 // invalid element
	}
	if ds.parent[x] != x {
		ds.parent[x] = ds.Find(ds.parent[x]) // path compression
	}
	return ds.parent[x]
}

// Union merges the sets containing elements x and y.
// Uses union by rank to keep trees flat.
// Returns true if the sets were merged, false if they were already in the same set.
func (ds *DisjointSet) Union(x, y int) bool {
	rootX := ds.Find(x)
	rootY := ds.Find(y)

	if rootX == -1 || rootY == -1 {
		return false
	}

	if rootX == rootY {
		return false // already in the same set
	}

	// Union by rank
	if ds.rank[rootX] < ds.rank[rootY] {
		ds.parent[rootX] = rootY
	} else if ds.rank[rootX] > ds.rank[rootY] {
		ds.parent[rootY] = rootX
	} else {
		ds.parent[rootY] = rootX
		ds.rank[rootX]++
	}

	ds.count--
	return true
}

// Connected checks if elements x and y are in the same set.
func (ds *DisjointSet) Connected(x, y int) bool {
	return ds.Find(x) == ds.Find(y) && ds.Find(x) != -1
}

// Count returns the number of disjoint sets.
func (ds *DisjointSet) Count() int {
	return ds.count
}

// Size returns the total number of elements.
func (ds *DisjointSet) Size() int {
	return len(ds.parent)
}

// SetSize returns the size of the set containing element x.
func (ds *DisjointSet) SetSize(x int) int {
	root := ds.Find(x)
	if root == -1 {
		return 0
	}
	size := 0
	for i := 0; i < len(ds.parent); i++ {
		if ds.Find(i) == root {
			size++
		}
	}
	return size
}

// Sets returns all disjoint sets as a map from root to slice of elements.
func (ds *DisjointSet) Sets() map[int][]int {
	sets := make(map[int][]int)
	for i := 0; i < len(ds.parent); i++ {
		root := ds.Find(i)
		sets[root] = append(sets[root], i)
	}
	return sets
}

// Reset resets the disjoint set to its initial state where each element
// is in its own set.
func (ds *DisjointSet) Reset() {
	for i := 0; i < len(ds.parent); i++ {
		ds.parent[i] = i
		ds.rank[i] = 0
	}
	ds.count = len(ds.parent)
}

// Elements returns all elements in the set containing element x.
func (ds *DisjointSet) Elements(x int) []int {
	root := ds.Find(x)
	if root == -1 {
		return nil
	}
	var elements []int
	for i := 0; i < len(ds.parent); i++ {
		if ds.Find(i) == root {
			elements = append(elements, i)
		}
	}
	return elements
}

// WeightedDisjointSet extends DisjointSet with size tracking for each set.
type WeightedDisjointSet struct {
	parent []int
	size   []int
	count   int
}

// NewWeighted creates a new WeightedDisjointSet with n elements.
func NewWeighted(n int) *WeightedDisjointSet {
	parent := make([]int, n)
	size := make([]int, n)
	for i := 0; i < n; i++ {
		parent[i] = i
		size[i] = 1
	}
	return &WeightedDisjointSet{
		parent: parent,
		size:   size,
		count:  n,
	}
}

// Find returns the root of the set containing element x.
func (wds *WeightedDisjointSet) Find(x int) int {
	if x < 0 || x >= len(wds.parent) {
		return -1
	}
	if wds.parent[x] != x {
		wds.parent[x] = wds.Find(wds.parent[x])
	}
	return wds.parent[x]
}

// Union merges the sets containing elements x and y using union by size.
func (wds *WeightedDisjointSet) Union(x, y int) bool {
	rootX := wds.Find(x)
	rootY := wds.Find(y)

	if rootX == -1 || rootY == -1 {
		return false
	}

	if rootX == rootY {
		return false
	}

	// Union by size - attach smaller tree under larger tree
	if wds.size[rootX] < wds.size[rootY] {
		wds.parent[rootX] = rootY
		wds.size[rootY] += wds.size[rootX]
	} else {
		wds.parent[rootY] = rootX
		wds.size[rootX] += wds.size[rootY]
	}

	wds.count--
	return true
}

// Connected checks if elements x and y are in the same set.
func (wds *WeightedDisjointSet) Connected(x, y int) bool {
	return wds.Find(x) == wds.Find(y) && wds.Find(x) != -1
}

// SetSize returns the size of the set containing element x.
func (wds *WeightedDisjointSet) SetSize(x int) int {
	root := wds.Find(x)
	if root == -1 {
		return 0
	}
	return wds.size[root]
}

// Count returns the number of disjoint sets.
func (wds *WeightedDisjointSet) Count() int {
	return wds.count
}

// CountComponents counts the number of connected components in a graph
// given the number of nodes and a list of edges.
func CountComponents(n int, edges [][2]int) int {
	ds := New(n)
	for _, edge := range edges {
		ds.Union(edge[0], edge[1])
	}
	return ds.Count()
}

// FindRedundantConnection finds a redundant edge in an undirected graph
// that, if removed, would make the graph a tree.
// Returns the edge that can be removed, or -1, -1 if no redundant edge exists.
func FindRedundantConnection(n int, edges [][2]int) (int, int) {
	ds := New(n + 1) // 1-indexed
	for _, edge := range edges {
		if ds.Connected(edge[0], edge[1]) {
			return edge[0], edge[1]
		}
		ds.Union(edge[0], edge[1])
	}
	return -1, -1
}

// IsBipartite checks if a graph is bipartite using disjoint set.
// graph[i] contains the neighbors of node i.
func IsBipartite(graph [][]int) bool {
	n := len(graph)
	ds := New(2 * n) // Each node has two "sides"

	for i := 0; i < n; i++ {
		for _, neighbor := range graph[i] {
			// If i and neighbor are in the same set, not bipartite
			if ds.Connected(i, neighbor) {
				return false
			}
			// Put i and neighbor in opposite groups
			ds.Union(i, neighbor+n)
			ds.Union(i+n, neighbor)
		}
	}
	return true
}

// MSTKruskal computes the minimum spanning tree using Kruskal's algorithm.
// Returns the total weight and the edges in the MST.
func MSTKruskal(n int, edges []Edge) (int64, []Edge) {
	// Sort edges by weight (simple bubble sort for zero dependencies)
	sortedEdges := make([]Edge, len(edges))
	copy(sortedEdges, edges)
	for i := 0; i < len(sortedEdges)-1; i++ {
		for j := 0; j < len(sortedEdges)-i-1; j++ {
			if sortedEdges[j].Weight > sortedEdges[j+1].Weight {
				sortedEdges[j], sortedEdges[j+1] = sortedEdges[j+1], sortedEdges[j]
			}
		}
	}

	ds := New(n)
	var totalWeight int64 = 0
	var mstEdges []Edge

	for _, edge := range sortedEdges {
		if ds.Union(edge.From, edge.To) {
			totalWeight += edge.Weight
			mstEdges = append(mstEdges, edge)
			if len(mstEdges) == n-1 {
				break
			}
		}
	}

	return totalWeight, mstEdges
}

// Edge represents a weighted edge in a graph.
type Edge struct {
	From   int
	To     int
	Weight int64
}