# Dijkstra's Shortest Path Algorithm Utils

A comprehensive implementation of Dijkstra's shortest path algorithm for Go, with zero external dependencies.

## Features

- **Shortest Path Finding**: Find the shortest path between any two nodes
- **Multi-path Support**: K-shortest paths using Yen's algorithm
- **All Paths from Source**: Find shortest paths to all reachable nodes
- **Generic Types**: Support for any comparable node types (int, string, etc.)
- **Directed/Undirected**: Support for both graph types
- **Graph Analytics**: Calculate diameter and center of graph
- **O((V + E) log V) Complexity**: Using priority queue optimization

## Installation

```go
import dijkstra_utils "github.com/ayukyo/alltoolkit/Go/dijkstra_utils"
```

## Quick Start

```go
// Create a directed graph
graph := dijkstra_utils.NewGraph[string](dijkstra_utils.Directed)

// Add edges
graph.AddEdge("A", "B", 4.0)
graph.AddEdge("B", "C", 3.0)
graph.AddEdge("A", "C", 10.0) // Direct but longer

// Find shortest path
result := graph.ShortestPath("A", "C")
fmt.Println(result.Path)     // [A, B, C]
fmt.Println(result.Distance) // 7.0
```

## API Reference

### Graph Creation

```go
// Directed graph
graph := dijkstra_utils.NewGraph[string](dijkstra_utils.Directed)

// Undirected graph
graph := dijkstra_utils.NewGraph[int](dijkstra_utils.Undirected)
```

### Adding Nodes and Edges

```go
// Add a single node
graph.AddNode("A")

// Add an edge (automatically creates nodes)
graph.AddEdge("A", "B", 4.0) // source, target, weight

// Add multiple edges
graph.AddEdges([]struct{Source, Target string; Weight float64}{
    {Source: "A", Target: "B", Weight: 4.0},
    {Source: "B", Target: "C", Weight: 3.0},
})
```

### Path Finding

```go
// Shortest path between two nodes
result := graph.ShortestPath("A", "Z")
if result.Found {
    fmt.Println(result.Path)     // Path nodes
    fmt.Println(result.Distance) // Total distance
}

// Shortest paths from source to all reachable nodes
allPaths := graph.ShortestPathsFrom("A")
pathToB := allPaths.GetPathTo("B")

// K-shortest paths (Yen's algorithm)
kPaths := graph.KShortestPaths("A", "Z", 3) // Find top 3 paths
```

### Graph Properties

```go
// Basic properties
graph.NodeCount()
graph.EdgeCount()
graph.IsDirected()
graph.Nodes()         // All nodes
graph.HasNode("A")    // Check node exists
graph.HasEdge("A", "B") // Check edge exists
graph.GetEdgeWeight("A", "B") // Get edge weight

// Connectivity
graph.IsConnected("A", "B")
graph.GetReachableNodes("A")

// Analytics
diameter, ep1, ep2 := graph.GraphDiameter()
center := graph.CenterOfGraph()
```

### Modifying Graph

```go
graph.RemoveNode("A")
graph.RemoveEdge("A", "B")
graph.Clear() // Remove all nodes and edges
```

### Factory Functions

```go
// From adjacency list
adjList := map[string][]struct{Node string; Weight float64}{
    "A": {{Node: "B", Weight: 4.0}},
    "B": {{Node: "C", Weight: 3.0}},
}
graph := dijkstra_utils.FromAdjacencyList(adjList, true) // true = directed

// From edge list
edges := []struct{Source, Target string; Weight float64}{
    {Source: "A", Target: "B", Weight: 4.0},
    {Source: "B", Target: "C", Weight: 3.0},
}
graph := dijkstra_utils.FromEdgeList(edges, false) // false = undirected
```

## Example

```go
package main

import (
    "fmt"
    dijkstra_utils "github.com/ayukyo/alltoolkit/Go/dijkstra_utils"
)

func main() {
    // Create a complex undirected graph
    graph := dijkstra_utils.NewGraph[string](dijkstra_utils.Undirected)
    graph.AddEdge("A", "B", 4.0)
    graph.AddEdge("A", "C", 2.0)
    graph.AddEdge("B", "C", 1.0)
    graph.AddEdge("B", "D", 5.0)
    graph.AddEdge("C", "D", 8.0)
    graph.AddEdge("D", "E", 2.0)
    graph.AddEdge("E", "Z", 3.0)

    // Find shortest path
    result := graph.ShortestPath("A", "Z")
    fmt.Printf("Path: %v\n", result.Path)
    fmt.Printf("Distance: %.1f\n", result.Distance)

    // Find all paths from A
    allPaths := graph.ShortestPathsFrom("A")
    for _, node := range graph.Nodes() {
        pathResult := allPaths.GetPathTo(node)
        if pathResult.Found {
            fmt.Printf("To %s: %.1f via %v\n", 
                node, pathResult.Distance, pathResult.Path)
        }
    }
}
```

## Time Complexity

| Operation | Complexity |
|-----------|------------|
| AddEdge | O(1) |
| RemoveNode | O(V + E) |
| ShortestPath | O((V + E) log V) |
| ShortestPathsFrom | O((V + E) log V) |
| KShortestPaths | O(k * (V + E) log V) |

## License

MIT License - Part of AllToolkit