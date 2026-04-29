# pagerank_utils

PageRank algorithm utilities for computing importance scores in directed graphs.

## Features

- **Classic PageRank**: Standard PageRank algorithm with configurable damping factor
- **Weighted PageRank**: Consider edge weights when distributing rank
- **Personalized PageRank**: Bias scores toward specific source nodes
- **Graph Utilities**: Build, manipulate, and analyze directed graphs
- **Zero Dependencies**: Pure Python implementation using only standard library

## Installation

No external dependencies required. Simply import the module:

```python
from pagerank_utils.mod import Graph, pagerank
```

## Quick Start

### Basic PageRank

```python
from pagerank_utils.mod import Graph, pagerank

# Create a graph
graph = Graph()
graph.add_edge('A', 'B')
graph.add_edge('B', 'C')
graph.add_edge('C', 'A')

# Compute PageRank
scores = pagerank(graph)

print(scores)  # {'A': 0.333..., 'B': 0.333..., 'C': 0.333...}
```

### Weighted PageRank

```python
graph = Graph()
graph.add_edge('A', 'B', weight=1.0)
graph.add_edge('A', 'C', weight=3.0)  # C receives more rank from A
graph.add_edge('B', 'A')
graph.add_edge('C', 'A')

scores = pagerank_weighted(graph)
# C will have higher score due to higher incoming weight
```

### Personalized PageRank

```python
graph = Graph()
graph.add_edge('A', 'B')
graph.add_edge('B', 'C')
graph.add_edge('C', 'D')

# Only teleport to node 'A'
scores = personalized_pagerank(graph, 'A')
# Scores biased toward nodes reachable from A
```

## API Reference

### Graph Class

```python
class Graph:
    def add_node(node: str) -> Graph
    def add_edge(source: str, target: str, weight: float = 1.0) -> Graph
    def add_edges_from(edges: List[Tuple]) -> Graph
    
    @property nodes -> Set[str]
    @property node_count -> int
    @property edge_count -> int
    
    def get_out_degree(node: str) -> int
    def get_in_degree(node: str) -> int
    def get_successors(node: str) -> Dict[str, float]
    def get_predecessors(node: str) -> Set[str]
    def get_dangling_nodes() -> Set[str]
    def get_statistics() -> Dict
```

### Main Functions

```python
pagerank(
    graph: Graph,
    damping: float = 0.85,          # Probability of following a link
    threshold: float = 1e-8,        # Convergence threshold
    max_iterations: int = 100,      # Maximum iterations
    personalization: Dict[str, float] = None  # Teleportation preferences
) -> Dict[str, float]

pagerank_weighted(
    graph: Graph,
    damping: float = 0.85,
    threshold: float = 1e-8,
    max_iterations: int = 100,
    personalization: Dict[str, float] = None
) -> Dict[str, float]

personalized_pagerank(
    graph: Graph,
    source_nodes: Union[str, List[str]],
    damping: float = 0.85,
    threshold: float = 1e-8,
    max_iterations: int = 100,
    weights: Dict[str, float] = None
) -> Dict[str, float]
```

### Utility Functions

```python
get_top_k(scores: Dict[str, float], k: int = 10) -> List[Tuple[str, float]]
get_rankings(scores: Dict[str, float]) -> Dict[str, int]
normalize_scores(scores: Dict[str, float]) -> Dict[str, float]
compare_scores(scores1, scores2) -> Dict[str, float]
l1_distance(scores1, scores2) -> float
l2_distance(scores1, scores2) -> float
compute_centrality(scores) -> Dict
detect_communities_by_scores(scores, num_tiers=3) -> Dict[str, int]
```

### Graph Builders

```python
build_graph_from_edge_list(edges: List[Tuple[str, str, float]]) -> Graph
build_graph_from_adjacency_list(adj_list: Dict) -> Graph
build_graph_from_matrix(matrix: List[List[float]], labels: List[str] = None) -> Graph
```

## Algorithm Details

### Classic PageRank

PageRank simulates a random surfer who:
1. Starts at a random page
2. Follows links with probability `d` (damping factor)
3. Teleports to a random page with probability `1-d`

Formula:
```
PR(A) = (1-d)/N + d * Σ(PR(Ti)/C(Ti)) for all Ti linking to A
```

Where:
- `d` = damping factor (default 0.85)
- `N` = total number of pages
- `C(Ti)` = number of outgoing links from Ti

### Weighted PageRank

Edge weights affect rank distribution. The contribution from a predecessor
is proportional to the edge weight relative to total outgoing weight:

```
PR(A) = (1-d)/N + d * Σ(PR(Ti) * W(Ti→A) / W(Ti)) for all Ti linking to A
```

### Personalized PageRank

Teleportation is limited to a subset of "source" nodes instead of random pages.
Useful for finding nodes relevant to specific interests.

## Examples

### Analyzing a Website Structure

```python
# Build graph from page links
graph = Graph()
graph.add_edge('home', 'products')
graph.add_edge('home', 'about')
graph.add_edge('products', 'home')
graph.add_edge('products', 'product1')
graph.add_edge('products', 'product2')
graph.add_edge('about', 'home')

scores = pagerank(graph)
top_pages = get_top_k(scores, 3)

print("Most important pages:", top_pages)
```

### Social Network Analysis

```python
# Who follows whom
graph = Graph()
graph.add_edge('alice', 'bob')
graph.add_edge('alice', 'charlie')
graph.add_edge('bob', 'alice')
graph.add_edge('charlie', 'alice')
graph.add_edge('charlie', 'david')

scores = pagerank(graph)
# alice has highest score (many incoming links)
```

### Recommendation System

```python
# Find items related to user's interests
graph = Graph()
# User's liked items -> other items
graph.add_edge('liked_item1', 'related_item1')
graph.add_edge('liked_item1', 'related_item2')
graph.add_edge('related_item1', 'related_item3')

# Personalized PageRank from liked items
scores = personalized_pagerank(graph, ['liked_item1'])
recommendations = get_top_k(scores, 5)
```

## Performance

- Time complexity: O(k * (V + E)) where k is iterations
- Space complexity: O(V + E)
- Typically converges in 10-50 iterations for most graphs

## License

MIT License - Part of AllToolkit project