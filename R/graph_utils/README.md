# Graph Utilities for R

A zero-dependency R library providing graph data structures and common graph algorithms.

## Features

- **Graph Operations**: Create graphs, add vertices and edges
- **Traversals**: BFS (Breadth-First Search), DFS (Depth-First Search)
- **Shortest Path**: Dijkstra's algorithm with path reconstruction
- **Connected Components**: Find isolated groups in undirected graphs
- **Cycle Detection**: Detect cycles in both directed and undirected graphs
- **Topological Sort**: Order vertices in a DAG
- **Minimum Spanning Tree**: Prim's algorithm for MST
- **Degree Calculation**: Vertex degree statistics
- **Import/Export**: Edge list conversion for interoperability

## Installation

No installation required! Simply source the file:

```r
source("graph_utils.R")
```

## Quick Start

```r
source("graph_utils.R")

# Create an undirected graph
g <- graph_create(directed = FALSE)

# Add edges (vertices are auto-created)
g <- graph_add_edge(g, "A", "B", 5)  # weight = 5
g <- graph_add_edge(g, "B", "C", 3)
g <- graph_add_edge(g, "A", "C", 10)

# Find shortest path
path <- graph_shortest_path(g, "A", "C")
print(path)  # "A" "B" "C"

# BFS and DFS traversals
graph_bfs(g, "A")
graph_dfs(g, "A")
```

## API Reference

### Graph Creation

```r
g <- graph_create(directed = FALSE)  # Create undirected graph
g <- graph_create(directed = TRUE)   # Create directed graph
```

### Vertex Operations

```r
g <- graph_add_vertex(g, "NodeName")  # Add a vertex
```

### Edge Operations

```r
g <- graph_add_edge(g, "from", "to")           # Unweighted edge
g <- graph_add_edge(g, "from", "to", weight=5) # Weighted edge
neighbors <- graph_neighbors(g, "NodeName")    # Get neighbors
```

### Traversals

```r
graph_bfs(g, "start")  # Breadth-First Search
graph_dfs(g, "start")  # Depth-First Search
```

### Shortest Path

```r
# Get distances from start to all vertices
result <- graph_dijkstra(g, "start")
print(result$distances)   # Named vector of distances
print(result$previous)    # For path reconstruction

# Get specific path
path <- graph_shortest_path(g, "from", "to")
```

### Connected Components

```r
components <- graph_connected_components(g)
# Returns list of character vectors
```

### Cycle Detection

```r
has_cycle <- graph_has_cycle(g)  # TRUE if cycle exists
```

### Topological Sort

```r
order <- graph_topological_sort(g)  # Only for DAGs
```

### Minimum Spanning Tree

```r
mst <- graph_minimum_spanning_tree(g)  # Returns edge data frame
total_weight <- sum(mst$weight)
```

### Degree

```r
degrees <- graph_degree(g)      # All degrees
deg_A <- graph_degree(g, "A")    # Single vertex degree
```

### Import/Export

```r
edgelist <- graph_to_edgelist(g)           # Export
g <- graph_from_edgelist(edgelist, directed=FALSE)  # Import
```

## Running Tests

```bash
Rscript graph_utils_test.R
```

## Running Examples

```bash
Rscript examples.R
```

## Use Cases

1. **Social Network Analysis**: Find communities, popularity (degree), connections
2. **Route Planning**: Shortest path for navigation
3. **Task Scheduling**: Topological sort for dependencies
4. **Network Design**: Minimum spanning tree for cable/pipe layout
5. **Web Crawling**: BFS/DFS for systematic page discovery
6. **Dependency Analysis**: Detect circular dependencies

## Complexity

| Algorithm | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| BFS | O(V + E) | O(V) |
| DFS | O(V + E) | O(V) |
| Dijkstra | O(V²) | O(V) |
| Topological Sort | O(V + E) | O(V) |
| MST (Prim's) | O(V²) | O(V) |
| Cycle Detection | O(V + E) | O(V) |

## License

MIT License