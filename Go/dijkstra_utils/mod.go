// Package dijkstra_utils provides a comprehensive implementation of Dijkstra's
// shortest path algorithm for finding the shortest paths between nodes in a graph.
// Supports weighted graphs with non-negative edges.
//
// Features:
// - Zero external dependencies, pure Go standard library
// - Find shortest path between two nodes
// - Find shortest paths to all nodes from a source
// - K-shortest paths using Yen's algorithm
// - Support for directed and undirected graphs
// - Path reconstruction with total distance
// - Generic node types using comparable constraint
// - Priority queue optimization (heap-based)
// - Early termination when target is found
//
// Time Complexity: O((V + E) log V) with binary heap
// Space Complexity: O(V)
//
// Example:
//
//	graph := dijkstra_utils.NewGraph[string](dijkstra_utils.Directed)
//	graph.AddEdge("A", "B", 4.0)
//	graph.AddEdge("B", "C", 3.0)
//	result := graph.ShortestPath("A", "C")
//	fmt.Println(result.Path)  // [A, B, C]
//	fmt.Println(result.Distance)  // 7.0
package dijkstra_utils

import (
	"container/heap"
	"errors"
	"math"
)

// GraphType defines whether the graph is directed or undirected
type GraphType int

const (
	// Directed graph - edges are one-way
	Directed GraphType = 0
	// Undirected graph - edges are bidirectional
	Undirected GraphType = 1
)

// PathResult represents the result of a shortest path search
type PathResult[T comparable] struct {
	Distance float64
	Path     []T
	Found    bool
}

// AllPathsResult represents the result of finding shortest paths to all reachable nodes
type AllPathsResult[T comparable] struct {
	Source      T
	Distances   map[T]float64
	Predecessor map[T]*T
}

// GetPathTo reconstructs the path to a specific target from AllPathsResult
func (r *AllPathsResult[T]) GetPathTo(target T) PathResult[T] {
	if _, ok := r.Distances[target]; !ok {
		return PathResult[T]{Distance: math.Inf(1), Path: nil, Found: false}
	}

	path := []T{}
	current := target
	for currentPtr := &current; currentPtr != nil; {
		path = append([]T{*currentPtr}, path...)
		if pred, ok := r.Predecessor[*currentPtr]; ok && pred != nil {
			current = *pred
		} else {
			break
		}
	}

	return PathResult[T]{Distance: r.Distances[target], Path: path, Found: true}
}

// GetReachableNodes returns all nodes reachable from the source
func (r *AllPathsResult[T]) GetReachableNodes() []T {
	nodes := make([]T, 0, len(r.Distances))
	for node := range r.Distances {
		nodes = append(nodes, node)
	}
	return nodes
}

// GraphEdge represents a weighted edge in the graph
type GraphEdge[T comparable] struct {
	Target T
	Weight float64
}

// Graph is a graph implementation optimized for Dijkstra's algorithm
type Graph[T comparable] struct {
	adjacency  map[T][]GraphEdge[T]
	directed   bool
	nodeCount  int
	edgeCount  int
}

// NewGraph creates a new graph with the specified type
func NewGraph[T comparable](graphType GraphType) *Graph[T] {
	return &Graph[T]{
		adjacency: make(map[T][]GraphEdge[T]),
		directed:  graphType == Directed,
	}
}

// AddNode adds a node to the graph
func (g *Graph[T]) AddNode(node T) {
	if _, exists := g.adjacency[node]; !exists {
		g.adjacency[node] = []GraphEdge[T]{}
		g.nodeCount++
	}
}

// AddEdge adds a weighted edge to the graph
// Returns error if weight is negative
func (g *Graph[T]) AddEdge(source, target T, weight float64) error {
	if weight < 0 {
		return errors.New("Dijkstra's algorithm does not support negative weights")
	}

	g.AddNode(source)
	g.AddNode(target)

	g.adjacency[source] = append(g.adjacency[source], GraphEdge[T]{Target: target, Weight: weight})
	g.edgeCount++

	if !g.directed {
		g.adjacency[target] = append(g.adjacency[target], GraphEdge[T]{Target: source, Weight: weight})
		g.edgeCount++
	}

	return nil
}

// AddEdges adds multiple edges at once
func (g *Graph[T]) AddEdges(edges []struct{ Source, Target T; Weight float64 }) error {
	for _, e := range edges {
		if err := g.AddEdge(e.Source, e.Target, e.Weight); err != nil {
			return err
		}
	}
	return nil
}

// RemoveNode removes a node and all its edges from the graph
func (g *Graph[T]) RemoveNode(node T) {
	if _, exists := g.adjacency[node]; !exists {
		return
	}

	// Count edges being removed
	g.edgeCount -= len(g.adjacency[node])
	delete(g.adjacency, node)
	g.nodeCount--

	// Remove edges pointing to this node
	for n := range g.adjacency {
		newEdges := []GraphEdge[T]{}
		for _, e := range g.adjacency[n] {
			if e.Target != node {
				newEdges = append(newEdges, e)
			}
		}
		removed := len(g.adjacency[n]) - len(newEdges)
		g.edgeCount -= removed
		g.adjacency[n] = newEdges
	}
}

// RemoveEdge removes an edge from the graph
func (g *Graph[T]) RemoveEdge(source, target T) {
	// Remove edge from source to target
	if _, exists := g.adjacency[source]; exists {
		newEdges := []GraphEdge[T]{}
		for _, e := range g.adjacency[source] {
			if e.Target != target {
				newEdges = append(newEdges, e)
			}
		}
		g.edgeCount -= len(g.adjacency[source]) - len(newEdges)
		g.adjacency[source] = newEdges
	}

	// For undirected graphs, also remove the reverse edge
	if !g.directed {
		if _, exists := g.adjacency[target]; exists {
			newEdges := []GraphEdge[T]{}
			for _, e := range g.adjacency[target] {
				if e.Target != source {
					newEdges = append(newEdges, e)
			}
			}
			g.edgeCount -= len(g.adjacency[target]) - len(newEdges)
			g.adjacency[target] = newEdges
		}
	}
}

// GetNeighbors returns all neighbors of a node
func (g *Graph[T]) GetNeighbors(node T) []GraphEdge[T] {
	if edges, exists := g.adjacency[node]; exists {
		return edges
	}
	return nil
}

// HasNode checks if a node exists in the graph
func (g *Graph[T]) HasNode(node T) bool {
	_, exists := g.adjacency[node]
	return exists
}

// HasEdge checks if an edge exists between two nodes
func (g *Graph[T]) HasEdge(source, target T) bool {
	if _, exists := g.adjacency[source]; !exists {
		return false
	}
	for _, e := range g.adjacency[source] {
		if e.Target == target {
			return true
		}
	}
	return false
}

// GetEdgeWeight returns the weight of an edge, or -1 if it doesn't exist
func (g *Graph[T]) GetEdgeWeight(source, target T) float64 {
	if _, exists := g.adjacency[source]; !exists {
		return -1
	}
	for _, e := range g.adjacency[source] {
		if e.Target == target {
			return e.Weight
		}
	}
	return -1
}

// Nodes returns all nodes in the graph
func (g *Graph[T]) Nodes() []T {
	nodes := make([]T, 0, len(g.adjacency))
	for node := range g.adjacency {
		nodes = append(nodes, node)
	}
	return nodes
}

// NodeCount returns the number of nodes
func (g *Graph[T]) NodeCount() int {
	return g.nodeCount
}

// EdgeCount returns the number of edges
func (g *Graph[T]) EdgeCount() int {
	return g.edgeCount
}

// IsDirected returns whether the graph is directed
func (g *Graph[T]) IsDirected() bool {
	return g.directed
}

// Clear removes all nodes and edges from the graph
func (g *Graph[T]) Clear() {
	g.adjacency = make(map[T][]GraphEdge[T])
	g.nodeCount = 0
	g.edgeCount = 0
}

// Priority queue item for Dijkstra's algorithm
type pqItem[T comparable] struct {
	node     T
	distance float64
	index    int
}

// Priority queue implementation
type priorityQueue[T comparable] []*pqItem[T]

func (pq priorityQueue[T]) Len() int { return len(pq) }

func (pq priorityQueue[T]) Less(i, j int) bool {
	return pq[i].distance < pq[j].distance
}

func (pq priorityQueue[T]) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *priorityQueue[T]) Push(x interface{}) {
	n := len(*pq)
	item := x.(*pqItem[T])
	item.index = n
	*pq = append(*pq, item)
}

func (pq *priorityQueue[T]) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil
	item.index = -1
	*pq = old[0 : n-1]
	return item
}

// ShortestPath finds the shortest path between two nodes using Dijkstra's algorithm
func (g *Graph[T]) ShortestPath(source, target T) PathResult[T] {
	if !g.HasNode(source) {
		return PathResult[T]{Distance: math.Inf(1), Path: nil, Found: false}
	}

	if !g.HasNode(target) {
		return PathResult[T]{Distance: math.Inf(1), Path: nil, Found: false}
	}

	if source == target {
		return PathResult[T]{Distance: 0, Path: []T{source}, Found: true}
	}

	// Initialize distances
	distances := make(map[T]float64)
	for node := range g.adjacency {
		distances[node] = math.Inf(1)
	}
	distances[source] = 0

	// Predecessor tracking
	predecessor := make(map[T]*T)

	// Priority queue
	pq := make(priorityQueue[T], 0)
	heap.Init(&pq)
	heap.Push(&pq, &pqItem[T]{node: source, distance: 0})

	// Visited set
	visited := make(map[T]bool)

	for pq.Len() > 0 {
		item := heap.Pop(&pq).(*pqItem[T])
		current := item.node
		currentDist := item.distance

		if visited[current] {
			continue
		}

		visited[current] = true

		// Early termination
		if current == target {
			break
		}

		// Explore neighbors
		for _, edge := range g.adjacency[current] {
			if visited[edge.Target] {
				continue
			}

			newDist := currentDist + edge.Weight
			if newDist < distances[edge.Target] {
				distances[edge.Target] = newDist
				predecessor[edge.Target] = &current
				heap.Push(&pq, &pqItem[T]{node: edge.Target, distance: newDist})
			}
		}
	}

	// Check if target is reachable
	if distances[target] == math.Inf(1) {
		return PathResult[T]{Distance: math.Inf(1), Path: nil, Found: false}
	}

	// Reconstruct path
	path := []T{}
	current := target
	for {
		path = append([]T{current}, path...)
		if pred, ok := predecessor[current]; ok && pred != nil {
			current = *pred
		} else {
			break
		}
	}

	return PathResult[T]{Distance: distances[target], Path: path, Found: true}
}

// ShortestPathsFrom finds shortest paths from source to all reachable nodes
func (g *Graph[T]) ShortestPathsFrom(source T) AllPathsResult[T] {
	if !g.HasNode(source) {
		return AllPathsResult[T]{
			Source:      source,
			Distances:   make(map[T]float64),
			Predecessor: make(map[T]*T),
		}
	}

	// Initialize distances
	distances := make(map[T]float64)
	for node := range g.adjacency {
		distances[node] = math.Inf(1)
	}
	distances[source] = 0

	predecessor := make(map[T]*T)

	// Priority queue
	pq := make(priorityQueue[T], 0)
	heap.Init(&pq)
	heap.Push(&pq, &pqItem[T]{node: source, distance: 0})

	visited := make(map[T]bool)

	for pq.Len() > 0 {
		item := heap.Pop(&pq).(*pqItem[T])
		current := item.node
		currentDist := item.distance

		if visited[current] {
			continue
		}

		visited[current] = true

		for _, edge := range g.adjacency[current] {
			if visited[edge.Target] {
				continue
			}

			newDist := currentDist + edge.Weight
			if newDist < distances[edge.Target] {
				distances[edge.Target] = newDist
				predecessor[edge.Target] = &current
				heap.Push(&pq, &pqItem[T]{node: edge.Target, distance: newDist})
			}
		}
	}

	// Remove unreachable nodes
	for node, dist := range distances {
		if dist == math.Inf(1) {
			delete(distances, node)
		}
	}

	return AllPathsResult[T]{
		Source:      source,
		Distances:   distances,
		Predecessor: predecessor,
	}
}

// KShortestPaths finds the k shortest paths between two nodes using Yen's algorithm
func (g *Graph[T]) KShortestPaths(source, target T, k int) []PathResult[T] {
	if !g.HasNode(source) || !g.HasNode(target) {
		return nil
	}

	if source == target {
		return []PathResult[T]{{Distance: 0, Path: []T{source}, Found: true}}
	}

	// Find the shortest path first
	shortest := g.ShortestPath(source, target)
	if !shortest.Found {
		return nil
	}

	paths := []PathResult[T]{shortest}

	if k == 1 {
		return paths
	}

	// Candidates for next shortest paths
	type candidate struct {
		distance float64
		path     []T
	}
	candidates := []candidate{}

	for i := 1; i < k && len(paths) > 0; i++ {
		prevPath := paths[len(paths)-1].Path

		// Generate deviations from previous paths
		for j := 0; j < len(prevPath)-1; j++ {
			spurNode := prevPath[j]
			rootPath := prevPath[:j+1]

			// Create a modified graph
			tempGraph := NewGraph[T](Directed)
			for node := range g.adjacency {
				tempGraph.AddNode(node)
			}
			for node, edges := range g.adjacency {
				for _, edge := range edges {
					tempGraph.adjacency[node] = append(tempGraph.adjacency[node], edge)
				}
			}

			// Remove edges that would recreate previously found paths
			for _, pathResult := range paths {
				path := pathResult.Path
				if len(path) > j && equalPaths(path[:j+1], rootPath) {
					if len(path) > j+1 {
						// Remove the edge
						newEdges := []GraphEdge[T]{}
						for _, e := range tempGraph.adjacency[spurNode] {
							if e.Target != path[j+1] {
								newEdges = append(newEdges, e)
							}
						}
						tempGraph.adjacency[spurNode] = newEdges
					}
				}
			}

			// Remove root path nodes (except spur) from graph
			for idx := 0; idx < len(rootPath)-1; idx++ {
				delete(tempGraph.adjacency, rootPath[idx])
			}

			// Find spur path
			spurResult := tempGraph.ShortestPath(spurNode, target)

			if spurResult.Found {
				totalPath := append(rootPath[:j], spurResult.Path...)

				// Calculate distance
				distance := 0.0
				for idx := 0; idx < len(totalPath)-1; idx++ {
					w := g.GetEdgeWeight(totalPath[idx], totalPath[idx+1])
					if w >= 0 {
						distance += w
					}
				}

				// Check if this path is unique
				isDuplicate := false
				for _, p := range paths {
					if equalPaths(p.Path, totalPath) {
						isDuplicate = true
						break
					}
				}
				for _, c := range candidates {
					if equalPaths(c.path, totalPath) {
						isDuplicate = true
						break
					}
				}

				if !isDuplicate {
					candidates = append(candidates, candidate{distance: distance, path: totalPath})
				}
			}
		}

		if len(candidates) == 0 {
			break
		}

		// Get the best candidate
		bestIdx := 0
		for idx, c := range candidates {
			if c.distance < candidates[bestIdx].distance {
				bestIdx = idx
			}
		}
		best := candidates[bestIdx]
		candidates = append(candidates[:bestIdx], candidates[bestIdx+1:]...)
		paths = append(paths, PathResult[T]{Distance: best.distance, Path: best.path, Found: true})
	}

	return paths
}

// Helper function to compare paths
func equalPaths[T comparable](a, b []T) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

// IsConnected checks if two nodes are connected
func (g *Graph[T]) IsConnected(node1, node2 T) bool {
	result := g.ShortestPath(node1, node2)
	return result.Found
}

// GetReachableNodes returns all nodes reachable from a source node
func (g *Graph[T]) GetReachableNodes(source T) []T {
	result := g.ShortestPathsFrom(source)
	return result.GetReachableNodes()
}

// GraphDiameter calculates the diameter of the graph (longest shortest path)
func (g *Graph[T]) GraphDiameter() (float64, T, T) {
	maxDist := 0.0
	var endpoint1, endpoint2 T

	nodes := g.Nodes()
	for _, source := range nodes {
		result := g.ShortestPathsFrom(source)
		for target, dist := range result.Distances {
			if dist > maxDist {
				maxDist = dist
				endpoint1 = source
				endpoint2 = target
			}
		}
	}

	return maxDist, endpoint1, endpoint2
}

// CenterOfGraph finds the center of the graph (nodes with minimum eccentricity)
func (g *Graph[T]) CenterOfGraph() []T {
	nodes := g.Nodes()
	if len(nodes) == 0 {
		return nil
	}

	eccentricities := make(map[T]float64)

	for _, node := range nodes {
		result := g.ShortestPathsFrom(node)
		if len(result.Distances) > 0 {
			maxDist := 0.0
			for _, dist := range result.Distances {
				if dist > maxDist {
					maxDist = dist
				}
			}
			eccentricities[node] = maxDist
		} else {
			eccentricities[node] = math.Inf(1)
		}
	}

	// Find minimum eccentricity
	minEcc := math.Inf(1)
	for _, ecc := range eccentricities {
		if ecc < minEcc {
			minEcc = ecc
		}
	}

	// Find all nodes with minimum eccentricity
	center := []T{}
	for node, ecc := range eccentricities {
		if ecc == minEcc {
			center = append(center, node)
		}
	}

	return center
}

// Convenience functions

// Dijkstra runs Dijkstra's algorithm on a graph
func Dijkstra[T comparable](graph *Graph[T], source T, target *T) interface{} {
	if target != nil {
		return graph.ShortestPath(source, *target)
	}
	return graph.ShortestPathsFrom(source)
}

// ShortestPath is a convenience function to find the shortest path between two nodes
func ShortestPath[T comparable](graph *Graph[T], source, target T) PathResult[T] {
	return graph.ShortestPath(source, target)
}

// AllShortestPaths is a convenience function to find shortest paths to all reachable nodes
func AllShortestPaths[T comparable](graph *Graph[T], source T) AllPathsResult[T] {
	return graph.ShortestPathsFrom(source)
}

// FromAdjacencyList creates a graph from an adjacency list
func FromAdjacencyList[T comparable](adjList map[T][]struct{ Node T; Weight float64 }, directed bool) *Graph[T] {
	graphType := Directed
	if !directed {
		graphType = Undirected
	}

	graph := NewGraph[T](graphType)
	for node, neighbors := range adjList {
		graph.AddNode(node)
		for _, n := range neighbors {
			graph.AddEdge(node, n.Node, n.Weight)
		}
	}
	return graph
}

// FromEdgeList creates a graph from a list of edges
func FromEdgeList[T comparable](edges []struct{ Source, Target T; Weight float64 }, directed bool) *Graph[T] {
	graphType := Directed
	if !directed {
		graphType = Undirected
	}

	graph := NewGraph[T](graphType)
	for _, e := range edges {
		graph.AddEdge(e.Source, e.Target, e.Weight)
	}
	return graph
}