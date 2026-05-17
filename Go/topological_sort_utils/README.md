# Topological Sort Utils

A comprehensive Go package for topological sorting and dependency resolution. Provides multiple algorithms for DAG (Directed Acyclic Graph) operations with zero external dependencies.

## Features

- **Two Topological Sort Algorithms**: Kahn's algorithm and DFS-based
- **Cycle Detection**: Find and report circular dependencies
- **Level-based Sorting**: Group nodes by dependency levels for parallel processing
- **Path Analysis**: Longest path and all paths between nodes
- **Graph Utilities**: Reverse graph, node/edge management
- **Dependency Resolver**: High-level API for dependency resolution
- **Generic Support**: Works with any comparable type
- **Zero Dependencies**: Pure Go standard library

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/topological_sort_utils
```

## Quick Start

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/topological_sort_utils"
)

func main() {
    // Create a graph
    g := topological_sort_utils.NewGraph[string]()
    
    // Add nodes
    g.AddNodes("A", "B", "C", "D")
    
    // Add edges (A -> B means A must come before B)
    g.AddEdge("A", "B")
    g.AddEdge("B", "C")
    g.AddEdge("C", "D")
    
    // Get topological order
    order, err := g.Sort()
    if err != nil {
        fmt.Println("Cycle detected!")
        return
    }
    
    fmt.Println(order) // [A B C D]
}
```

## API Reference

### Graph[T comparable]

#### Creation

```go
g := topological_sort_utils.NewGraph[int]() // or string, or any comparable type
```

#### Node Operations

```go
g.AddNode("A")           // Add single node
g.AddNodes("A", "B", "C") // Add multiple nodes
g.HasNode("A")            // Check if node exists
g.GetNodes()              // Get all nodes
g.Count()                 // Number of nodes
```

#### Edge Operations

```go
g.AddEdge("A", "B")  // Add directed edge A -> B
g.GetEdges("A")      // Get all outgoing edges from A
g.EdgeCount()        // Total number of edges
```

#### Sorting Algorithms

```go
// Kahn's algorithm (BFS-based)
order, err := g.Sort()

// DFS-based algorithm
order, err := g.SortDFS()

// Get nodes grouped by levels (for parallel processing)
levels, err := g.Levels()
```

#### Cycle Detection

```go
hasCycle := g.DetectCycle()      // Boolean check
cycle := g.FindCycle()           // Returns cycle path if exists
```

#### Path Analysis

```go
// Longest path from a node (critical path)
path, err := g.LongestPath("A")

// All paths between two nodes
paths := g.AllPaths("A", "D")
```

#### Graph Operations

```go
reversed := g.Reverse()  // Create reversed graph
g.Clear()                // Remove all nodes and edges
```

### DependencyResolver[T comparable]

Higher-level API for dependency management:

```go
resolver := topological_sort_utils.NewDependencyResolver[string]()

// Add item with its dependencies
resolver.AddItem("app", "database", "config")
resolver.AddItem("config", "env")
resolver.AddItem("database", "env")
resolver.AddItem("env")

// Get full dependency order
order, err := resolver.Resolve()

// Get dependencies for a specific item
deps, err := resolver.ResolveItem("app")
```

### Convenience Function

```go
// Simple topological sort with dependencies map
deps := map[string][]string{
    "main":   {"utils", "config"},
    "utils":  {"types"},
    "config": {"types"},
    "types":  {},
}

order, err := topological_sort_utils.TopologicalSort(deps)
```

## Use Cases

### 1. Course Prerequisites

```go
g := topological_sort_utils.NewGraph[string]()
g.AddNodes("Math101", "Math201", "Math301")
g.AddEdge("Math101", "Math201") // Math101 is prerequisite for Math201
g.AddEdge("Math201", "Math301") // Math201 is prerequisite for Math301

order, _ := g.Sort()
// ["Math101", "Math201", "Math301"]
```

### 2. Build System

```go
deps := map[string][]string{
    "core":     {},
    "utils":    {"core"},
    "database": {"core", "utils"},
    "api":      {"core", "database"},
    "web":      {"api"},
}

order, _ := topological_sort_utils.TopologicalSort(deps)
// Build in this order
```

### 3. Task Scheduling

```go
g := topological_sort_utils.NewGraph[string]()
// ... add tasks and dependencies

// Get tasks by level for parallel execution
levels, _ := g.Levels()
for i, level := range levels {
    fmt.Printf("Run in parallel: %v\n", level)
}
```

### 4. Circular Dependency Detection

```go
g := topological_sort_utils.NewGraph[string]()
g.AddEdge("A", "B")
g.AddEdge("B", "C")
g.AddEdge("C", "A") // Cycle!

if g.DetectCycle() {
    cycle := g.FindCycle()
    fmt.Printf("Circular dependency: %v\n", cycle)
}
```

### 5. Package Manager Dependencies

```go
resolver := topological_sort_utils.NewDependencyResolver[string]()
resolver.AddItem("express", "body-parser", "cookie-parser")
resolver.AddItem("body-parser", "bytes", "iconv-lite")
// ... add all packages

order, _ := resolver.Resolve()
// Install packages in this order
```

## Performance

- **Time Complexity**:
  - Sort/Kahn's: O(V + E)
  - SortDFS: O(V + E)
  - DetectCycle: O(V + E)
  - FindCycle: O(V + E)
  - Levels: O(V + E)
  - LongestPath: O(V + E)

- **Space Complexity**: O(V + E)

## Testing

Run tests:

```bash
go test -v
```

Run benchmarks:

```bash
go test -bench=.
```

## License

MIT License