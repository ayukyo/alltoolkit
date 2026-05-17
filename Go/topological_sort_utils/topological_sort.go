// Package topological_sort_utils provides topological sorting algorithms for directed graphs.
// Useful for dependency resolution, task scheduling, build systems, and more.
package topological_sort_utils

import (
	"errors"
)

// Common errors
var (
	ErrCycleDetected = errors.New("cycle detected in graph")
	ErrNodeNotFound  = errors.New("node not found in graph")
)

// Graph represents a directed graph using adjacency list
type Graph[T comparable] struct {
	nodes    map[T]bool
	edges    map[T][]T
	inDegree map[T]int
}

// NewGraph creates a new directed graph
func NewGraph[T comparable]() *Graph[T] {
	return &Graph[T]{
		nodes:    make(map[T]bool),
		edges:    make(map[T][]T),
		inDegree: make(map[T]int),
	}
}

// AddNode adds a node to the graph
func (g *Graph[T]) AddNode(node T) {
	if !g.nodes[node] {
		g.nodes[node] = true
		g.inDegree[node] = 0
	}
}

// AddEdge adds a directed edge from 'from' to 'to'
// Returns error if either node doesn't exist
func (g *Graph[T]) AddEdge(from, to T) error {
	if !g.nodes[from] {
		return ErrNodeNotFound
	}
	if !g.nodes[to] {
		return ErrNodeNotFound
	}
	g.edges[from] = append(g.edges[from], to)
	g.inDegree[to]++
	return nil
}

// AddNodes adds multiple nodes to the graph
func (g *Graph[T]) AddNodes(nodes ...T) {
	for _, node := range nodes {
		g.AddNode(node)
	}
}

// HasNode checks if a node exists in the graph
func (g *Graph[T]) HasNode(node T) bool {
	return g.nodes[node]
}

// GetNodes returns all nodes in the graph
func (g *Graph[T]) GetNodes() []T {
	nodes := make([]T, 0, len(g.nodes))
	for node := range g.nodes {
		nodes = append(nodes, node)
	}
	return nodes
}

// GetEdges returns all outgoing edges from a node
func (g *Graph[T]) GetEdges(node T) []T {
	return g.edges[node]
}

// Sort returns nodes in topological order using Kahn's algorithm
// Returns error if graph contains a cycle
func (g *Graph[T]) Sort() ([]T, error) {
	// Copy in-degree map
	inDegree := make(map[T]int)
	for node, deg := range g.inDegree {
		inDegree[node] = deg
	}

	// Find all nodes with no incoming edges
	queue := make([]T, 0)
	for node, deg := range inDegree {
		if deg == 0 {
			queue = append(queue, node)
		}
	}

	result := make([]T, 0, len(g.nodes))

	for len(queue) > 0 {
		// Dequeue
		node := queue[0]
		queue = queue[1:]
		result = append(result, node)

		// Process neighbors
		for _, neighbor := range g.edges[node] {
			inDegree[neighbor]--
			if inDegree[neighbor] == 0 {
				queue = append(queue, neighbor)
			}
		}
	}

	// Check for cycle
	if len(result) != len(g.nodes) {
		return nil, ErrCycleDetected
	}

	return result, nil
}

// SortDFS returns nodes in topological order using DFS
// Returns error if graph contains a cycle
func (g *Graph[T]) SortDFS() ([]T, error) {
	visited := make(map[T]int) // 0: unvisited, 1: visiting, 2: visited
	result := make([]T, 0, len(g.nodes))
	var cycle bool

	var dfs func(node T) bool
	dfs = func(node T) bool {
		if visited[node] == 1 {
			// Cycle detected
			return true
		}
		if visited[node] == 2 {
			return false
		}

		visited[node] = 1
		for _, neighbor := range g.edges[node] {
			if dfs(neighbor) {
				return true
			}
		}
		visited[node] = 2
		result = append([]T{node}, result...) // Prepend to reverse order
		return false
	}

	for node := range g.nodes {
		if visited[node] == 0 {
			if dfs(node) {
				cycle = true
				break
			}
		}
	}

	if cycle {
		return nil, ErrCycleDetected
	}

	return result, nil
}

// DetectCycle returns true if the graph contains a cycle
func (g *Graph[T]) DetectCycle() bool {
	_, err := g.Sort()
	return errors.Is(err, ErrCycleDetected)
}

// FindCycle returns one cycle in the graph if exists
// Returns nil if no cycle
func (g *Graph[T]) FindCycle() []T {
	visited := make(map[T]int) // 0: unvisited, 1: visiting, 2: visited
	parent := make(map[T]T)
	var cycleStart T
	var cycleEnd T

	var dfs func(node T) bool
	dfs = func(node T) bool {
		visited[node] = 1
		for _, neighbor := range g.edges[node] {
			if visited[neighbor] == 1 {
				// Found cycle
				cycleStart = neighbor
				cycleEnd = node
				return true
			}
			if visited[neighbor] == 0 {
				parent[neighbor] = node
				if dfs(neighbor) {
					return true
				}
			}
		}
		visited[node] = 2
		return false
	}

	for node := range g.nodes {
		if visited[node] == 0 {
			if dfs(node) {
				// Reconstruct cycle
				cycle := []T{cycleStart}
				current := cycleEnd
				for current != cycleStart {
					cycle = append([]T{current}, cycle...)
					current = parent[current]
				}
				cycle = append([]T{cycleStart}, cycle...)
				return cycle
			}
		}
	}

	return nil
}

// Levels returns nodes grouped by their level in the topological order
// All nodes at the same level have no dependencies between them
func (g *Graph[T]) Levels() ([][]T, error) {
	// Copy in-degree map
	inDegree := make(map[T]int)
	for node, deg := range g.inDegree {
		inDegree[node] = deg
	}

	levels := make([][]T, 0)

	for {
		// Find all nodes with no incoming edges
		level := make([]T, 0)
		for node, deg := range inDegree {
			if deg == 0 {
				level = append(level, node)
			}
		}

		if len(level) == 0 {
			break
		}

		levels = append(levels, level)

		// Remove edges from these nodes
		for _, node := range level {
			delete(inDegree, node)
			for _, neighbor := range g.edges[node] {
				inDegree[neighbor]--
			}
		}
	}

	// Check for remaining nodes (cycle)
	if len(inDegree) > 0 {
		return nil, ErrCycleDetected
	}

	return levels, nil
}

// LongestPath returns the longest path from start to any reachable node
// Useful for finding critical path in task scheduling
func (g *Graph[T]) LongestPath(start T) ([]T, error) {
	if !g.nodes[start] {
		return nil, ErrNodeNotFound
	}

	// Check for cycle
	if g.DetectCycle() {
		return nil, ErrCycleDetected
	}

	visited := make(map[T]bool)
	var longestPath []T

	var dfs func(node T, path []T)
	dfs = func(node T, path []T) {
		if visited[node] {
			return
		}

		path = append(path, node)
		visited[node] = true

		if len(path) > len(longestPath) {
			longestPath = make([]T, len(path))
			copy(longestPath, path)
		}

		for _, neighbor := range g.edges[node] {
			dfs(neighbor, path)
		}

		visited[node] = false
	}

	dfs(start, []T{})
	return longestPath, nil
}

// Count returns the number of nodes in the graph
func (g *Graph[T]) Count() int {
	return len(g.nodes)
}

// EdgeCount returns the number of edges in the graph
func (g *Graph[T]) EdgeCount() int {
	count := 0
	for _, edges := range g.edges {
		count += len(edges)
	}
	return count
}

// Clear removes all nodes and edges from the graph
func (g *Graph[T]) Clear() {
	g.nodes = make(map[T]bool)
	g.edges = make(map[T][]T)
	g.inDegree = make(map[T]int)
}

// Reverse returns a new graph with all edges reversed
func (g *Graph[T]) Reverse() *Graph[T] {
	reversed := NewGraph[T]()
	for node := range g.nodes {
		reversed.AddNode(node)
	}
	for from, edges := range g.edges {
		for _, to := range edges {
			reversed.AddEdge(to, from)
		}
	}
	return reversed
}

// AllPaths returns all paths from start to end
func (g *Graph[T]) AllPaths(start, end T) [][]T {
	if !g.nodes[start] || !g.nodes[end] {
		return nil
	}

	visited := make(map[T]bool)
	var allPaths [][]T

	var dfs func(node T, path []T)
	dfs = func(node T, path []T) {
		if visited[node] {
			return
		}

		path = append(path, node)

		if node == end {
			pathCopy := make([]T, len(path))
			copy(pathCopy, path)
			allPaths = append(allPaths, pathCopy)
			return
		}

		visited[node] = true
		for _, neighbor := range g.edges[node] {
			dfs(neighbor, path)
		}
		visited[node] = false
	}

	dfs(start, []T{})
	return allPaths
}

// TopologicalSort is a convenience function for sorting dependencies
// dependencies[node] = list of nodes that 'node' depends on
func TopologicalSort[T comparable](dependencies map[T][]T) ([]T, error) {
	graph := NewGraph[T]()

	// Add all nodes
	for node := range dependencies {
		graph.AddNode(node)
	}
	for _, deps := range dependencies {
		for _, dep := range deps {
			graph.AddNode(dep)
		}
	}

	// Add edges (dep -> node means node depends on dep, so dep must come before node)
	for node, deps := range dependencies {
		for _, dep := range deps {
			if err := graph.AddEdge(dep, node); err != nil {
				return nil, err
			}
		}
	}

	return graph.Sort()
}

// DependencyResolver helps resolve dependencies for items
type DependencyResolver[T comparable] struct {
	graph *Graph[T]
	items map[T]bool
}

// NewDependencyResolver creates a new dependency resolver
func NewDependencyResolver[T comparable]() *DependencyResolver[T] {
	return &DependencyResolver[T]{
		graph: NewGraph[T](),
		items: make(map[T]bool),
	}
}

// AddItem adds an item with its dependencies
func (r *DependencyResolver[T]) AddItem(item T, dependencies ...T) {
	r.graph.AddNode(item)
	r.items[item] = true

	for _, dep := range dependencies {
		r.graph.AddNode(dep)
		r.graph.AddEdge(dep, item)
	}
}

// Resolve returns all items in dependency order
func (r *DependencyResolver[T]) Resolve() ([]T, error) {
	return r.graph.Sort()
}

// ResolveItem returns the dependency order for a specific item
func (r *DependencyResolver[T]) ResolveItem(item T) ([]T, error) {
	if !r.items[item] {
		return nil, ErrNodeNotFound
	}

	// BFS to find all dependencies
	visited := make(map[T]bool)
	queue := []T{item}
	result := []T{}

	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]

		if visited[current] {
			continue
		}
		visited[current] = true

		// Get dependencies (incoming edges)
		for node := range r.graph.nodes {
			for _, edge := range r.graph.edges[node] {
				if edge == current && !visited[node] {
					queue = append(queue, node)
				}
			}
		}

		result = append(result, current)
	}

	// Reverse to get dependency order
	for i, j := 0, len(result)-1; i < j; i, j = i+1, j-1 {
		result[i], result[j] = result[j], result[i]
	}

	return result, nil
}