// Package graph_utils provides comprehensive graph data structures and algorithms.
// Zero external dependencies, pure Go standard library implementation.
package graph_utils

import (
	"container/heap"
	"container/list"
	"errors"
	"fmt"
	"sort"
)

// Graph types
type GraphType int

const (
	Undirected GraphType = iota
	Directed
)

// Edge represents an edge in the graph
type Edge struct {
	From   int
	To     int
	Weight float64
}

// Graph is the main graph structure using adjacency list
type Graph struct {
	vertices  int
	adjList   [][]Edge
	directed  bool
	edgeCount int
}

// NewGraph creates a new graph with given number of vertices
func NewGraph(vertices int, graphType GraphType) *Graph {
	return &Graph{
		vertices: vertices,
		adjList:  make([][]Edge, vertices),
		directed: graphType == Directed,
	}
}

// AddEdge adds an edge to the graph
func (g *Graph) AddEdge(from, to int, weight float64) error {
	if from < 0 || from >= g.vertices || to < 0 || to >= g.vertices {
		return errors.New("vertex index out of bounds")
	}

	g.adjList[from] = append(g.adjList[from], Edge{From: from, To: to, Weight: weight})
	g.edgeCount++

	if !g.directed {
		g.adjList[to] = append(g.adjList[to], Edge{From: to, To: from, Weight: weight})
		g.edgeCount++
	}

	return nil
}

// AddEdges adds multiple edges
func (g *Graph) AddEdges(edges []Edge) error {
	for _, e := range edges {
		if err := g.AddEdge(e.From, e.To, e.Weight); err != nil {
			return err
		}
	}
	return nil
}

// Vertices returns the number of vertices
func (g *Graph) Vertices() int {
	return g.vertices
}

// Edges returns the number of edges
func (g *Graph) Edges() int {
	return g.edgeCount
}

// IsDirected returns whether the graph is directed
func (g *Graph) IsDirected() bool {
	return g.directed
}

// GetNeighbors returns neighbors of a vertex
func (g *Graph) GetNeighbors(v int) ([]Edge, error) {
	if v < 0 || v >= g.vertices {
		return nil, errors.New("vertex index out of bounds")
	}
	return g.adjList[v], nil
}

// GetAllEdges returns all edges in the graph
func (g *Graph) GetAllEdges() []Edge {
	edges := make([]Edge, 0)
	seen := make(map[[2]int]bool)

	for from, neighbors := range g.adjList {
		for _, e := range neighbors {
			key := [2]int{min(from, e.To), max(from, e.To)}
			if g.directed || !seen[key] {
				edges = append(edges, e)
				if !g.directed {
					seen[key] = true
				}
			}
		}
	}
	return edges
}

// HasEdge checks if an edge exists
func (g *Graph) HasEdge(from, to int) bool {
	if from < 0 || from >= g.vertices || to < 0 || to >= g.vertices {
		return false
	}
	for _, e := range g.adjList[from] {
		if e.To == to {
			return true
		}
	}
	return false
}

// RemoveEdge removes an edge from the graph
func (g *Graph) RemoveEdge(from, to int) bool {
	if from < 0 || from >= g.vertices || to < 0 || to >= g.vertices {
		return false
	}

	removed := false
	newList := make([]Edge, 0)
	for _, e := range g.adjList[from] {
		if e.To != to {
			newList = append(newList, e)
		} else {
			removed = true
		}
	}
	g.adjList[from] = newList

	if !g.directed && removed {
		newList = make([]Edge, 0)
		for _, e := range g.adjList[to] {
			if e.To != from {
				newList = append(newList, e)
			}
		}
		g.adjList[to] = newList
	}

	if removed {
		g.edgeCount--
		if !g.directed {
			g.edgeCount--
		}
	}
	return removed
}

// BFS performs breadth-first search starting from vertex v
func (g *Graph) BFS(start int) ([]int, error) {
	if start < 0 || start >= g.vertices {
		return nil, errors.New("start vertex out of bounds")
	}

	result := make([]int, 0)
	visited := make([]bool, g.vertices)
	queue := list.New()

	queue.PushBack(start)
	visited[start] = true

	for queue.Len() > 0 {
		v := queue.Remove(queue.Front()).(int)
		result = append(result, v)

		for _, e := range g.adjList[v] {
			if !visited[e.To] {
				visited[e.To] = true
				queue.PushBack(e.To)
			}
		}
	}

	return result, nil
}

// DFS performs depth-first search starting from vertex v
func (g *Graph) DFS(start int) ([]int, error) {
	if start < 0 || start >= g.vertices {
		return nil, errors.New("start vertex out of bounds")
	}

	result := make([]int, 0)
	visited := make([]bool, g.vertices)
	g.dfsHelper(start, visited, &result)
	return result, nil
}

func (g *Graph) dfsHelper(v int, visited []bool, result *[]int) {
	visited[v] = true
	*result = append(*result, v)

	for _, e := range g.adjList[v] {
		if !visited[e.To] {
			g.dfsHelper(e.To, visited, result)
		}
	}
}

// DFSIterative performs iterative depth-first search
func (g *Graph) DFSIterative(start int) ([]int, error) {
	if start < 0 || start >= g.vertices {
		return nil, errors.New("start vertex out of bounds")
	}

	result := make([]int, 0)
	visited := make([]bool, g.vertices)
	stack := []int{start}

	for len(stack) > 0 {
		v := stack[len(stack)-1]
		stack = stack[:len(stack)-1]

		if visited[v] {
			continue
		}

		visited[v] = true
		result = append(result, v)

		// Add neighbors in reverse order for correct DFS order
		for i := len(g.adjList[v]) - 1; i >= 0; i-- {
			if !visited[g.adjList[v][i].To] {
				stack = append(stack, g.adjList[v][i].To)
			}
		}
	}

	return result, nil
}

// ShortestPathResult contains shortest path information
type ShortestPathResult struct {
	Distances []float64
	Previous  []int
	HasPath   []bool
}

// Dijkstra finds shortest paths from source using Dijkstra's algorithm
func (g *Graph) Dijkstra(source int) (*ShortestPathResult, error) {
	if source < 0 || source >= g.vertices {
		return nil, errors.New("source vertex out of bounds")
	}

	dist := make([]float64, g.vertices)
	prev := make([]int, g.vertices)
	hasPath := make([]bool, g.vertices)

	for i := range dist {
		dist[i] = float64(1<<63 - 1) // Infinity
		prev[i] = -1
	}
	dist[source] = 0
	hasPath[source] = true

	pq := &priorityQueue{}
	heap.Init(pq)
	heap.Push(pq, &item{vertex: source, priority: 0})

	for pq.Len() > 0 {
		u := heap.Pop(pq).(*item).vertex

		for _, e := range g.adjList[u] {
			alt := dist[u] + e.Weight
			if alt < dist[e.To] {
				dist[e.To] = alt
				prev[e.To] = u
				hasPath[e.To] = true
				heap.Push(pq, &item{vertex: e.To, priority: alt})
			}
		}
	}

	return &ShortestPathResult{
		Distances: dist,
		Previous:  prev,
		HasPath:   hasPath,
	}, nil
}

// GetPath reconstructs the path from source to target
func (r *ShortestPathResult) GetPath(target int) []int {
	if !r.HasPath[target] {
		return nil
	}

	path := []int{}
	for v := target; v != -1; v = r.Previous[v] {
		path = append([]int{v}, path...)
	}
	return path
}

// BellmanFord finds shortest paths using Bellman-Ford algorithm (handles negative weights)
func (g *Graph) BellmanFord(source int) (*ShortestPathResult, error) {
	if source < 0 || source >= g.vertices {
		return nil, errors.New("source vertex out of bounds")
	}

	dist := make([]float64, g.vertices)
	prev := make([]int, g.vertices)
	hasPath := make([]bool, g.vertices)

	for i := range dist {
		dist[i] = float64(1<<63 - 1)
		prev[i] = -1
	}
	dist[source] = 0
	hasPath[source] = true

	edges := g.GetAllEdges()

	// Relax edges V-1 times
	for i := 0; i < g.vertices-1; i++ {
		for _, e := range edges {
			if dist[e.From] != float64(1<<63-1) && dist[e.From]+e.Weight < dist[e.To] {
				dist[e.To] = dist[e.From] + e.Weight
				prev[e.To] = e.From
				hasPath[e.To] = true
			}
		}
	}

	// Check for negative cycles
	for _, e := range edges {
		if dist[e.From] != float64(1<<63-1) && dist[e.From]+e.Weight < dist[e.To] {
			return nil, errors.New("graph contains negative weight cycle")
		}
	}

	return &ShortestPathResult{
		Distances: dist,
		Previous:  prev,
		HasPath:   hasPath,
	}, nil
}

// TopologicalSort performs topological sorting (for DAGs)
func (g *Graph) TopologicalSort() ([]int, error) {
	if !g.directed {
		return nil, errors.New("topological sort only works on directed graphs")
	}

	inDegree := make([]int, g.vertices)
	for _, neighbors := range g.adjList {
		for _, e := range neighbors {
			inDegree[e.To]++
		}
	}

	queue := list.New()
	for i, d := range inDegree {
		if d == 0 {
			queue.PushBack(i)
		}
	}

	result := make([]int, 0)

	for queue.Len() > 0 {
		v := queue.Remove(queue.Front()).(int)
		result = append(result, v)

		for _, e := range g.adjList[v] {
			inDegree[e.To]--
			if inDegree[e.To] == 0 {
				queue.PushBack(e.To)
			}
		}
	}

	if len(result) != g.vertices {
		return nil, errors.New("graph contains a cycle")
	}

	return result, nil
}

// HasCycle checks if the graph has a cycle
func (g *Graph) HasCycle() bool {
	if g.directed {
		return g.hasCycleDirected()
	}
	return g.hasCycleUndirected()
}

func (g *Graph) hasCycleDirected() bool {
	visited := make([]int, g.vertices) // 0: unvisited, 1: in current path, 2: done

	var dfs func(v int) bool
	dfs = func(v int) bool {
		visited[v] = 1

		for _, e := range g.adjList[v] {
			if visited[e.To] == 1 {
				return true
			}
			if visited[e.To] == 0 && dfs(e.To) {
				return true
			}
		}

		visited[v] = 2
		return false
	}

	for i := 0; i < g.vertices; i++ {
		if visited[i] == 0 {
			if dfs(i) {
				return true
			}
		}
	}

	return false
}

func (g *Graph) hasCycleUndirected() bool {
	visited := make([]bool, g.vertices)

	var dfs func(v, parent int) bool
	dfs = func(v, parent int) bool {
		visited[v] = true

		for _, e := range g.adjList[v] {
			if !visited[e.To] {
				if dfs(e.To, v) {
					return true
				}
			} else if e.To != parent {
				return true
			}
		}

		return false
	}

	for i := 0; i < g.vertices; i++ {
		if !visited[i] {
			if dfs(i, -1) {
				return true
			}
		}
	}

	return false
}

// ConnectedComponents finds all connected components
func (g *Graph) ConnectedComponents() [][]int {
	if g.directed {
		// For directed graphs, use weakly connected components
		return g.weaklyConnectedComponents()
	}

	visited := make([]bool, g.vertices)
	components := make([][]int, 0)

	for i := 0; i < g.vertices; i++ {
		if !visited[i] {
			component := make([]int, 0)
			g.dfsHelper(i, visited, &component)
			components = append(components, component)
		}
	}

	return components
}

func (g *Graph) weaklyConnectedComponents() [][]int {
	// Build undirected adjacency list
	undirectedAdj := make([][]int, g.vertices)
	for from, neighbors := range g.adjList {
		for _, e := range neighbors {
			undirectedAdj[from] = append(undirectedAdj[from], e.To)
			undirectedAdj[e.To] = append(undirectedAdj[e.To], from)
		}
	}

	visited := make([]bool, g.vertices)
	components := make([][]int, 0)

	var dfs func(v int, component *[]int)
	dfs = func(v int, component *[]int) {
		visited[v] = true
		*component = append(*component, v)
		for _, neighbor := range undirectedAdj[v] {
			if !visited[neighbor] {
				dfs(neighbor, component)
			}
		}
	}

	for i := 0; i < g.vertices; i++ {
		if !visited[i] {
			component := make([]int, 0)
			dfs(i, &component)
			components = append(components, component)
		}
	}

	return components
}

// MSTResult contains minimum spanning tree information
type MSTResult struct {
	Edges    []Edge
	Weight   float64
	Vertices int
}

// Kruskal finds minimum spanning tree using Kruskal's algorithm
func (g *Graph) Kruskal() (*MSTResult, error) {
	if g.directed {
		return nil, errors.New("MST only works on undirected graphs")
	}

	edges := g.GetAllEdges()
	sort.Slice(edges, func(i, j int) bool {
		return edges[i].Weight < edges[j].Weight
	})

	uf := newUnionFind(g.vertices)
	mstEdges := make([]Edge, 0)
	totalWeight := 0.0

	for _, e := range edges {
		if uf.find(e.From) != uf.find(e.To) {
			uf.union(e.From, e.To)
			mstEdges = append(mstEdges, e)
			totalWeight += e.Weight
		}
	}

	if len(mstEdges) != g.vertices-1 && g.vertices > 0 {
		return nil, errors.New("graph is not connected")
	}

	return &MSTResult{
		Edges:    mstEdges,
		Weight:   totalWeight,
		Vertices: g.vertices,
	}, nil
}

// Prim finds minimum spanning tree using Prim's algorithm
func (g *Graph) Prim(start int) (*MSTResult, error) {
	if g.directed {
		return nil, errors.New("MST only works on undirected graphs")
	}
	if start < 0 || start >= g.vertices {
		return nil, errors.New("start vertex out of bounds")
	}

	mstEdges := make([]Edge, 0)
	totalWeight := 0.0
	inMST := make([]bool, g.vertices)

	pq := &priorityQueue{}
	heap.Init(pq)
	heap.Push(pq, &item{vertex: start, priority: 0, parent: -1})

	for pq.Len() > 0 {
		curr := heap.Pop(pq).(*item)

		if inMST[curr.vertex] {
			continue
		}

		inMST[curr.vertex] = true

		if curr.parent != -1 {
			mstEdges = append(mstEdges, Edge{
				From:   curr.parent,
				To:     curr.vertex,
				Weight: curr.priority,
			})
			totalWeight += curr.priority
		}

		for _, e := range g.adjList[curr.vertex] {
			if !inMST[e.To] {
				heap.Push(pq, &item{vertex: e.To, priority: e.Weight, parent: curr.vertex})
			}
		}
	}

	return &MSTResult{
		Edges:    mstEdges,
		Weight:   totalWeight,
		Vertices: g.vertices,
	}, nil
}

// Union-Find for Kruskal's algorithm
type unionFind struct {
	parent []int
	rank   []int
}

func newUnionFind(n int) *unionFind {
	parent := make([]int, n)
	rank := make([]int, n)
	for i := range parent {
		parent[i] = i
	}
	return &unionFind{parent: parent, rank: rank}
}

func (uf *unionFind) find(x int) int {
	if uf.parent[x] != x {
		uf.parent[x] = uf.find(uf.parent[x])
	}
	return uf.parent[x]
}

func (uf *unionFind) union(x, y int) {
	px, py := uf.find(x), uf.find(y)
	if px == py {
		return
	}
	if uf.rank[px] < uf.rank[py] {
		uf.parent[px] = py
	} else if uf.rank[px] > uf.rank[py] {
		uf.parent[py] = px
	} else {
		uf.parent[py] = px
		uf.rank[px]++
	}
}

// Priority queue for Dijkstra and Prim
type item struct {
	vertex   int
	priority float64
	parent   int
	index    int
}

type priorityQueue []*item

func (pq priorityQueue) Len() int           { return len(pq) }
func (pq priorityQueue) Less(i, j int) bool { return pq[i].priority < pq[j].priority }
func (pq priorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *priorityQueue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*item)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *priorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil
	item.index = -1
	*pq = old[0 : n-1]
	return item
}

// Bipartite checks if the graph is bipartite
func (g *Graph) Bipartite() (bool, []int) {
	color := make([]int, g.vertices)
	for i := range color {
		color[i] = -1
	}

	for start := 0; start < g.vertices; start++ {
		if color[start] == -1 {
			queue := list.New()
			queue.PushBack(start)
			color[start] = 0

			for queue.Len() > 0 {
				v := queue.Remove(queue.Front()).(int)

				for _, e := range g.adjList[v] {
					if color[e.To] == -1 {
						color[e.To] = 1 - color[v]
						queue.PushBack(e.To)
					} else if color[e.To] == color[v] {
						return false, nil
					}
				}
			}
		}
	}

	return true, color
}

// Degree returns the degree of a vertex
func (g *Graph) Degree(v int) (int, error) {
	if v < 0 || v >= g.vertices {
		return 0, errors.New("vertex index out of bounds")
	}
	return len(g.adjList[v]), nil
}

// InDegree returns the in-degree of a vertex (for directed graphs)
func (g *Graph) InDegree(v int) (int, error) {
	if v < 0 || v >= g.vertices {
		return 0, errors.New("vertex index out of bounds")
	}

	if !g.directed {
		return g.Degree(v)
	}

	inDegree := 0
	for _, neighbors := range g.adjList {
		for _, e := range neighbors {
			if e.To == v {
				inDegree++
			}
		}
	}
	return inDegree, nil
}

// IsConnected checks if the graph is connected
func (g *Graph) IsConnected() bool {
	components := g.ConnectedComponents()
	return len(components) == 1
}

// Clone creates a deep copy of the graph
func (g *Graph) Clone() *Graph {
	newGraph := NewGraph(g.vertices, Directed)
	if !g.directed {
		newGraph.directed = false
	}

	for from, neighbors := range g.adjList {
		newGraph.adjList[from] = make([]Edge, len(neighbors))
		copy(newGraph.adjList[from], neighbors)
	}
	newGraph.edgeCount = g.edgeCount

	return newGraph
}

// Transpose returns the transpose of a directed graph
func (g *Graph) Transpose() (*Graph, error) {
	if !g.directed {
		return nil, errors.New("transpose only works on directed graphs")
	}

	t := NewGraph(g.vertices, Directed)
	for from, neighbors := range g.adjList {
		for _, e := range neighbors {
			t.adjList[e.To] = append(t.adjList[e.To], Edge{From: e.To, To: from, Weight: e.Weight})
		}
	}
	t.edgeCount = g.edgeCount

	return t, nil
}

// String returns a string representation of the graph
func (g *Graph) String() string {
	result := fmt.Sprintf("Graph(vertices=%d, edges=%d, directed=%v)\n", g.vertices, g.edgeCount, g.directed)
	for from, neighbors := range g.adjList {
		if len(neighbors) > 0 {
			result += fmt.Sprintf("  %d -> ", from)
			for i, e := range neighbors {
				if i > 0 {
					result += ", "
				}
				result += fmt.Sprintf("%d(%.1f)", e.To, e.Weight)
			}
			result += "\n"
		}
	}
	return result
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}