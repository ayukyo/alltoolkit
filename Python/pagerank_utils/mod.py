"""
PageRank Algorithm Utilities

A pure Python implementation of the PageRank algorithm with zero external dependencies.
Supports classic PageRank, personalized PageRank, and weighted graphs.

Features:
- Classic PageRank with damping factor
- Personalized PageRank with teleportation preferences
- Support for weighted edges
- Multiple input formats (adjacency list, edge list, matrix)
- Convergence threshold and max iteration control
- Graph analysis utilities (out-degree, in-degree)
"""

from typing import Dict, List, Optional, Tuple, Set, Union
from collections import defaultdict
import math


class PageRankError(Exception):
    """Base exception for PageRank utilities."""
    pass


class InvalidGraphError(PageRankError):
    """Raised when the graph structure is invalid."""
    pass


class ConvergenceError(PageRankError):
    """Raised when PageRank fails to converge."""
    pass


def validate_damping_factor(damping: float) -> None:
    """Validate damping factor is in valid range (0, 1)."""
    if not isinstance(damping, (int, float)):
        raise ValueError(f"Damping factor must be a number, got {type(damping).__name__}")
    if damping <= 0 or damping >= 1:
        raise ValueError(f"Damping factor must be in range (0, 1), got {damping}")


def validate_convergence_params(threshold: float, max_iterations: int) -> None:
    """Validate convergence parameters."""
    if threshold <= 0:
        raise ValueError(f"Convergence threshold must be positive, got {threshold}")
    if max_iterations < 1:
        raise ValueError(f"Max iterations must be at least 1, got {max_iterations}")


class Graph:
    """
    A directed graph representation for PageRank computation.
    
    Supports:
    - Adding nodes and edges
    - Weighted edges
    - Adjacency list export
    - Graph statistics
    """
    
    def __init__(self):
        """Initialize an empty directed graph."""
        self._nodes: Set[str] = set()
        self._edges: Dict[str, Dict[str, float]] = defaultdict(dict)
        self._in_edges: Dict[str, Set[str]] = defaultdict(set)
        self._out_degree: Dict[str, int] = defaultdict(int)
    
    def add_node(self, node: str) -> 'Graph':
        """
        Add a node to the graph.
        
        Args:
            node: Node identifier (string)
            
        Returns:
            Self for chaining
        """
        if not isinstance(node, str):
            raise ValueError(f"Node must be a string, got {type(node).__name__}")
        self._nodes.add(node)
        return self
    
    def add_edge(self, source: str, target: str, weight: float = 1.0) -> 'Graph':
        """
        Add a directed edge to the graph.
        
        Args:
            source: Source node
            target: Target node
            weight: Edge weight (default 1.0)
            
        Returns:
            Self for chaining
        """
        if not isinstance(source, str) or not isinstance(target, str):
            raise ValueError("Source and target must be strings")
        if weight <= 0:
            raise ValueError(f"Weight must be positive, got {weight}")
        
        self._nodes.add(source)
        self._nodes.add(target)
        
        # If edge already exists, sum weights
        if target in self._edges[source]:
            self._edges[source][target] += weight
        else:
            self._edges[source][target] = weight
            self._out_degree[source] += 1
        
        self._in_edges[target].add(source)
        return self
    
    def add_edges_from(self, edges: List[Tuple[str, str, float]]) -> 'Graph':
        """
        Add multiple edges from a list.
        
        Args:
            edges: List of (source, target, weight) tuples
                   or (source, target) tuples (weight defaults to 1.0)
            
        Returns:
            Self for chaining
        """
        for edge in edges:
            if len(edge) == 2:
                self.add_edge(edge[0], edge[1])
            elif len(edge) == 3:
                self.add_edge(edge[0], edge[1], edge[2])
            else:
                raise ValueError(f"Edge tuple must have 2 or 3 elements, got {len(edge)}")
        return self
    
    @property
    def nodes(self) -> Set[str]:
        """Get all nodes in the graph."""
        return self._nodes.copy()
    
    @property
    def edge_count(self) -> int:
        """Get total number of edges."""
        return sum(len(targets) for targets in self._edges.values())
    
    @property
    def node_count(self) -> int:
        """Get total number of nodes."""
        return len(self._nodes)
    
    def get_out_degree(self, node: str) -> int:
        """Get out-degree of a node."""
        return self._out_degree.get(node, 0)
    
    def get_in_degree(self, node: str) -> int:
        """Get in-degree of a node."""
        return len(self._in_edges.get(node, set()))
    
    def get_successors(self, node: str) -> Dict[str, float]:
        """Get successors (outgoing edges) of a node with weights."""
        return self._edges.get(node, {}).copy()
    
    def get_predecessors(self, node: str) -> Set[str]:
        """Get predecessors (incoming edges) of a node."""
        return self._in_edges.get(node, set()).copy()
    
    def get_adjacency_list(self) -> Dict[str, Dict[str, float]]:
        """Get the full adjacency list representation."""
        return {node: dict(self._edges[node]) for node in self._nodes}
    
    def get_dangling_nodes(self) -> Set[str]:
        """Get nodes with no outgoing edges (dangling nodes)."""
        return {node for node in self._nodes if self._out_degree.get(node, 0) == 0}
    
    def get_statistics(self) -> Dict:
        """Get graph statistics."""
        if not self._nodes:
            return {
                'node_count': 0,
                'edge_count': 0,
                'avg_out_degree': 0,
                'avg_in_degree': 0,
                'max_out_degree': 0,
                'max_in_degree': 0,
                'dangling_node_count': 0,
                'density': 0
            }
        
        out_degrees = [self._out_degree.get(n, 0) for n in self._nodes]
        in_degrees = [len(self._in_edges.get(n, set())) for n in self._nodes]
        
        n = len(self._nodes)
        max_possible_edges = n * (n - 1)  # No self-loops
        density = self.edge_count / max_possible_edges if max_possible_edges > 0 else 0
        
        return {
            'node_count': n,
            'edge_count': self.edge_count,
            'avg_out_degree': sum(out_degrees) / n,
            'avg_in_degree': sum(in_degrees) / n,
            'max_out_degree': max(out_degrees) if out_degrees else 0,
            'max_in_degree': max(in_degrees) if in_degrees else 0,
            'dangling_node_count': len(self.get_dangling_nodes()),
            'density': density
        }
    
    def to_edge_list(self) -> List[Tuple[str, str, float]]:
        """Export graph as edge list."""
        edges = []
        for source, targets in self._edges.items():
            for target, weight in targets.items():
                edges.append((source, target, weight))
        return edges
    
    def is_empty(self) -> bool:
        """Check if graph is empty."""
        return len(self._nodes) == 0
    
    def has_node(self, node: str) -> bool:
        """Check if node exists in graph."""
        return node in self._nodes
    
    def has_edge(self, source: str, target: str) -> bool:
        """Check if edge exists in graph."""
        return target in self._edges.get(source, {})


def build_graph_from_edge_list(
    edges: List[Tuple[str, str, float]],
    add_missing_nodes: bool = True
) -> Graph:
    """
    Build a Graph from an edge list.
    
    Args:
        edges: List of (source, target, weight) tuples
        add_missing_nodes: Whether to add nodes not explicitly added
        
    Returns:
        Graph object
    """
    graph = Graph()
    if add_missing_nodes:
        graph.add_edges_from(edges)
    else:
        for edge in edges:
            if len(edge) == 3:
                graph.add_edge(edge[0], edge[1], edge[2])
            else:
                graph.add_edge(edge[0], edge[1])
    return graph


def build_graph_from_adjacency_list(
    adj_list: Dict[str, Union[Dict[str, float], List[str], Set[str]]]
) -> Graph:
    """
    Build a Graph from an adjacency list.
    
    Args:
        adj_list: Dictionary mapping nodes to their successors.
                  Values can be:
                  - Dict[str, float]: node -> weight
                  - List[str]: list of successor nodes (weight = 1.0)
                  - Set[str]: set of successor nodes (weight = 1.0)
    
    Returns:
        Graph object
    """
    graph = Graph()
    
    for source, targets in adj_list.items():
        if isinstance(targets, dict):
            for target, weight in targets.items():
                graph.add_edge(source, target, weight)
        elif isinstance(targets, (list, set)):
            for target in targets:
                graph.add_edge(source, target)
        else:
            raise ValueError(f"Unsupported adjacency list value type: {type(targets).__name__}")
    
    return graph


def build_graph_from_matrix(
    matrix: List[List[float]],
    node_labels: Optional[List[str]] = None
) -> Graph:
    """
    Build a Graph from an adjacency matrix.
    
    Args:
        matrix: Square adjacency matrix where matrix[i][j] is the weight
                of edge from node i to node j
        node_labels: Optional labels for nodes (default: "0", "1", "2", ...)
        
    Returns:
        Graph object
    """
    n = len(matrix)
    if n == 0:
        return Graph()
    
    # Validate square matrix
    for i, row in enumerate(matrix):
        if len(row) != n:
            raise ValueError(f"Row {i} has {len(row)} elements, expected {n}")
    
    # Create node labels
    if node_labels is None:
        node_labels = [str(i) for i in range(n)]
    elif len(node_labels) != n:
        raise ValueError(f"Expected {n} node labels, got {len(node_labels)}")
    
    graph = Graph()
    for i, label_i in enumerate(node_labels):
        for j, label_j in enumerate(node_labels):
            weight = matrix[i][j]
            if weight > 0:
                graph.add_edge(label_i, label_j, weight)
    
    return graph


def pagerank(
    graph: Graph,
    damping: float = 0.85,
    threshold: float = 1e-8,
    max_iterations: int = 100,
    personalization: Optional[Dict[str, float]] = None
) -> Dict[str, float]:
    """
    Compute PageRank scores for all nodes in the graph.
    
    The PageRank algorithm computes a probability distribution over nodes
    representing the likelihood that a random surfer ends up at each node.
    
    Formula:
        PR(A) = (1-d)/N + d * sum(PR(Ti)/C(Ti) for Ti linking to A)
    
    Where:
        - d is the damping factor
        - N is the total number of nodes
        - C(Ti) is the out-degree of Ti
    
    Args:
        graph: Graph object
        damping: Damping factor (probability of following a link).
                 Default 0.85. Must be in range (0, 1).
        threshold: Convergence threshold. Algorithm stops when the maximum
                   change in any node's PageRank is less than this value.
                   Default 1e-8.
        max_iterations: Maximum number of iterations. Default 100.
        personalization: Optional dictionary mapping nodes to personalization
                         weights. Nodes not in the dict get weight 0.
                         If None, uniform personalization is used.
    
    Returns:
        Dictionary mapping node names to PageRank scores.
        Scores sum to 1.0.
    
    Raises:
        InvalidGraphError: If graph is empty
        ValueError: If parameters are invalid
        ConvergenceError: If algorithm doesn't converge within max_iterations
    
    Example:
        >>> graph = Graph()
        >>> graph.add_edge('A', 'B').add_edge('B', 'A').add_edge('A', 'C')
        >>> scores = pagerank(graph)
        >>> print(scores)
        {'A': 0.387..., 'B': 0.387..., 'C': 0.225...}
    """
    validate_damping_factor(damping)
    validate_convergence_params(threshold, max_iterations)
    
    if graph.is_empty():
        raise InvalidGraphError("Cannot compute PageRank on empty graph")
    
    nodes = list(graph.nodes)
    n = len(nodes)
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    
    # Initialize PageRank scores uniformly
    scores = {node: 1.0 / n for node in nodes}
    
    # Get dangling nodes (nodes with no outgoing edges)
    dangling_nodes = graph.get_dangling_nodes()
    dangling_idx = [node_to_idx[node] for node in dangling_nodes]
    
    # Precompute out-degrees and successors for efficiency
    out_degrees = {}
    successors = {}
    for node in nodes:
        out_degrees[node] = graph.get_out_degree(node)
        successors[node] = graph.get_successors(node)
    
    # Setup personalization vector
    if personalization is not None:
        # Validate personalization
        missing_nodes = set(personalization.keys()) - set(nodes)
        if missing_nodes:
            raise ValueError(f"Personalization contains unknown nodes: {missing_nodes}")
        
        # Normalize personalization
        total = sum(personalization.values())
        if total <= 0:
            raise ValueError("Personalization weights must sum to a positive value")
        
        p_vector = {node: personalization.get(node, 0.0) / total for node in nodes}
    else:
        p_vector = {node: 1.0 / n for node in nodes}
    
    # PageRank iteration
    for iteration in range(max_iterations):
        prev_scores = scores.copy()
        
        # Compute dangling node contribution
        dangling_sum = sum(prev_scores[node] for node in dangling_nodes)
        
        # Compute new scores
        new_scores = {}
        
        for node in nodes:
            # Start with teleportation probability
            rank = (1 - damping) * p_vector[node]
            
            # Add contribution from dangling nodes
            rank += damping * dangling_sum / n
            
            # Add contribution from incoming links
            for predecessor in graph.get_predecessors(node):
                pred_out_degree = out_degrees[predecessor]
                if pred_out_degree > 0:
                    rank += damping * prev_scores[predecessor] / pred_out_degree
            
            new_scores[node] = rank
        
        scores = new_scores
        
        # Check convergence
        max_change = max(abs(scores[node] - prev_scores[node]) for node in nodes)
        if max_change < threshold:
            break
    else:
        # Didn't converge
        raise ConvergenceError(
            f"PageRank did not converge after {max_iterations} iterations. "
            f"Last max change: {max_change:.2e}"
        )
    
    # Normalize to ensure scores sum to 1.0
    total = sum(scores.values())
    if total > 0:
        scores = {node: score / total for node, score in scores.items()}
    
    return scores


def pagerank_weighted(
    graph: Graph,
    damping: float = 0.85,
    threshold: float = 1e-8,
    max_iterations: int = 100,
    personalization: Optional[Dict[str, float]] = None
) -> Dict[str, float]:
    """
    Compute weighted PageRank scores.
    
    Unlike regular PageRank, weighted PageRank considers edge weights
    when distributing rank scores. The contribution from a predecessor
    is proportional to the weight of the edge.
    
    Formula:
        PR(A) = (1-d)/N + d * sum(PR(Ti) * W(Ti->A) / W(Ti) for Ti linking to A)
    
    Where:
        - W(Ti->A) is the weight of edge from Ti to A
        - W(Ti) is the sum of all outgoing edge weights from Ti
    
    Args:
        graph: Graph object with weighted edges
        damping: Damping factor (default 0.85)
        threshold: Convergence threshold (default 1e-8)
        max_iterations: Maximum iterations (default 100)
        personalization: Optional personalization weights
    
    Returns:
        Dictionary mapping node names to weighted PageRank scores
    """
    validate_damping_factor(damping)
    validate_convergence_params(threshold, max_iterations)
    
    if graph.is_empty():
        raise InvalidGraphError("Cannot compute PageRank on empty graph")
    
    nodes = list(graph.nodes)
    n = len(nodes)
    
    # Initialize scores
    scores = {node: 1.0 / n for node in nodes}
    
    # Precompute total outgoing weight for each node
    total_out_weights = {}
    predecessors_map = {}
    for node in nodes:
        successors = graph.get_successors(node)
        total_out_weights[node] = sum(successors.values())
        predecessors_map[node] = graph.get_predecessors(node)
    
    # Get dangling nodes (nodes with zero outgoing weight)
    dangling_nodes = {node for node in nodes if total_out_weights[node] == 0}
    
    # Setup personalization
    if personalization is not None:
        missing_nodes = set(personalization.keys()) - set(nodes)
        if missing_nodes:
            raise ValueError(f"Personalization contains unknown nodes: {missing_nodes}")
        total = sum(personalization.values())
        if total <= 0:
            raise ValueError("Personalization weights must sum to a positive value")
        p_vector = {node: personalization.get(node, 0.0) / total for node in nodes}
    else:
        p_vector = {node: 1.0 / n for node in nodes}
    
    # Iteration
    for iteration in range(max_iterations):
        prev_scores = scores.copy()
        
        # Dangling contribution
        dangling_sum = sum(prev_scores[node] for node in dangling_nodes)
        
        new_scores = {}
        for node in nodes:
            rank = (1 - damping) * p_vector[node]
            rank += damping * dangling_sum / n
            
            for pred in predecessors_map[node]:
                pred_successors = graph.get_successors(pred)
                pred_total_weight = total_out_weights[pred]
                if pred_total_weight > 0:
                    edge_weight = pred_successors.get(node, 0)
                    rank += damping * prev_scores[pred] * (edge_weight / pred_total_weight)
            
            new_scores[node] = rank
        
        scores = new_scores
        
        max_change = max(abs(scores[node] - prev_scores[node]) for node in nodes)
        if max_change < threshold:
            break
    else:
        raise ConvergenceError(
            f"Weighted PageRank did not converge after {max_iterations} iterations"
        )
    
    # Normalize
    total = sum(scores.values())
    if total > 0:
        scores = {node: score / total for node, score in scores.items()}
    
    return scores


def personalized_pagerank(
    graph: Graph,
    source_nodes: Union[str, List[str]],
    damping: float = 0.85,
    threshold: float = 1e-8,
    max_iterations: int = 100,
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, float]:
    """
    Compute Personalized PageRank from specific source nodes.
    
    The random surfer always teleports back to one of the source nodes
    instead of any random node.
    
    Args:
        graph: Graph object
        source_nodes: Single source node or list of source nodes.
                      The teleportation is limited to these nodes.
        damping: Damping factor (default 0.85)
        threshold: Convergence threshold (default 1e-8)
        max_iterations: Maximum iterations (default 100)
        weights: Optional weights for source nodes.
                 If None, uniform weights are used.
    
    Returns:
        Dictionary mapping node names to personalized PageRank scores
    
    Example:
        >>> graph = Graph()
        >>> graph.add_edge('A', 'B').add_edge('B', 'C').add_edge('C', 'A')
        >>> scores = personalized_pagerank(graph, 'A')
        # Scores are biased towards nodes reachable from 'A'
    """
    if isinstance(source_nodes, str):
        source_nodes = [source_nodes]
    
    # Validate source nodes exist
    missing = set(source_nodes) - graph.nodes
    if missing:
        raise ValueError(f"Source nodes not in graph: {missing}")
    
    # Setup personalization
    if weights is None:
        personalization = {node: 1.0 for node in source_nodes}
    else:
        # Validate weight keys
        missing_weights = set(weights.keys()) - set(source_nodes)
        if missing_weights:
            raise ValueError(f"Weights contain nodes not in source_nodes: {missing_weights}")
        personalization = weights.copy()
        # Add missing weights as 0
        for node in source_nodes:
            if node not in personalization:
                personalization[node] = 0.0
    
    return pagerank(graph, damping, threshold, max_iterations, personalization)


def get_top_k(
    scores: Dict[str, float],
    k: int = 10
) -> List[Tuple[str, float]]:
    """
    Get the top k nodes by PageRank score.
    
    Args:
        scores: PageRank scores dictionary
        k: Number of top nodes to return (default 10)
        
    Returns:
        List of (node, score) tuples sorted by score descending
    """
    if k <= 0:
        raise ValueError(f"k must be positive, got {k}")
    
    sorted_nodes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_nodes[:k]


def get_rankings(
    scores: Dict[str, float]
) -> Dict[str, int]:
    """
    Convert PageRank scores to rankings.
    
    Rank 1 is the highest score, rank N is the lowest.
    Ties are broken by alphabetical order of node names.
    
    Args:
        scores: PageRank scores dictionary
        
    Returns:
        Dictionary mapping node names to their rank (1-indexed)
    """
    # Sort by score descending, then by name ascending for ties
    sorted_nodes = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    
    rankings = {}
    for rank, (node, _) in enumerate(sorted_nodes, start=1):
        rankings[node] = rank
    
    return rankings


def normalize_scores(scores: Dict[str, float]) -> Dict[str, float]:
    """
    Normalize PageRank scores to sum to 1.0.
    
    Args:
        scores: PageRank scores dictionary
        
    Returns:
        Normalized scores dictionary
    """
    total = sum(scores.values())
    if total == 0:
        return {node: 0.0 for node in scores}
    return {node: score / total for node, score in scores.items()}


def compare_scores(
    scores1: Dict[str, float],
    scores2: Dict[str, float]
) -> Dict[str, float]:
    """
    Compare two PageRank score distributions.
    
    Returns the absolute difference between scores for each node.
    Useful for detecting significant changes in rankings.
    
    Args:
        scores1: First PageRank scores
        scores2: Second PageRank scores
        
    Returns:
        Dictionary mapping node names to absolute score differences
    """
    all_nodes = set(scores1.keys()) | set(scores2.keys())
    
    differences = {}
    for node in all_nodes:
        s1 = scores1.get(node, 0.0)
        s2 = scores2.get(node, 0.0)
        differences[node] = abs(s1 - s2)
    
    return differences


def l1_distance(
    scores1: Dict[str, float],
    scores2: Dict[str, float]
) -> float:
    """
    Compute L1 (Manhattan) distance between two PageRank distributions.
    
    Args:
        scores1: First PageRank scores
        scores2: Second PageRank scores
        
    Returns:
        L1 distance (sum of absolute differences)
    """
    differences = compare_scores(scores1, scores2)
    return sum(differences.values())


def l2_distance(
    scores1: Dict[str, float],
    scores2: Dict[str, float]
) -> float:
    """
    Compute L2 (Euclidean) distance between two PageRank distributions.
    
    Args:
        scores1: First PageRank scores
        scores2: Second PageRank scores
        
    Returns:
        L2 distance
    """
    differences = compare_scores(scores1, scores2)
    return math.sqrt(sum(d ** 2 for d in differences.values()))


def compute_centrality(
    scores: Dict[str, float]
) -> Dict[str, any]:
    """
    Compute centrality statistics from PageRank scores.
    
    Args:
        scores: PageRank scores dictionary
        
    Returns:
        Dictionary with statistics:
        - mean: Average score
        - std: Standard deviation
        - min: Minimum score
        - max: Maximum score
        - median: Median score
        - gini: Gini coefficient (inequality measure, 0=equal, 1=unequal)
    """
    values = list(scores.values())
    n = len(values)
    
    if n == 0:
        return {
            'mean': 0,
            'std': 0,
            'min': 0,
            'max': 0,
            'median': 0,
            'gini': 0
        }
    
    # Basic stats
    mean = sum(values) / n
    variance = sum((v - mean) ** 2 for v in values) / n
    std = math.sqrt(variance)
    
    # Median
    sorted_values = sorted(values)
    if n % 2 == 0:
        median = (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
    else:
        median = sorted_values[n // 2]
    
    # Gini coefficient
    # Formula: G = sum(|xi - xj|) / (2 * n * sum(xi))
    total = sum(values)
    if total == 0:
        gini = 0
    else:
        gini = sum(abs(v1 - v2) for v1 in values for v2 in values) / (2 * n * total)
    
    return {
        'mean': mean,
        'std': std,
        'min': min(values),
        'max': max(values),
        'median': median,
        'gini': gini
    }


def detect_communities_by_scores(
    scores: Dict[str, float],
    num_tiers: int = 3
) -> Dict[str, int]:
    """
    Partition nodes into tiers based on PageRank scores.
    
    Args:
        scores: PageRank scores dictionary
        num_tiers: Number of tiers to create (default 3)
        
    Returns:
        Dictionary mapping node names to tier numbers (1 is highest)
    """
    if num_tiers < 2:
        raise ValueError(f"num_tiers must be at least 2, got {num_tiers}")
    
    sorted_nodes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    n = len(sorted_nodes)
    
    if n == 0:
        return {}
    
    tiers = {}
    tier_size = n / num_tiers
    
    for i, (node, _) in enumerate(sorted_nodes):
        tier = min(int(i / tier_size) + 1, num_tiers)
        tiers[node] = tier
    
    return tiers