"""
Graph Metrics Utilities - Centrality, connectivity, and graph analysis metrics.
Zero external dependencies.
"""

from collections import deque
from typing import Optional, Dict, List


def degree_centrality(graph, node):
    """
    Compute degree centrality for a node.
    Degree centrality = degree(node) / (n - 1)

    Args:
        graph: Adjacency list representation {node: [neighbors]}
        node: Target node

    Returns:
        Degree centrality score (0.0 to 1.0)
    """
    n = len(graph)
    if n <= 1:
        return 0.0
    degree = len(graph.get(node, []))
    return degree / (n - 1)


def betweenness_centrality(graph, node, normalized=True):
    """
    Approximate betweenness centrality using sampling.
    Measures how often a node lies on shortest paths between other nodes.

    Args:
        graph: Adjacency list
        node: Target node
        normalized: Whether to normalize by (n-1)(n-2)/2

    Returns:
        Betweenness centrality score
    """
    nodes = list(graph.keys())
    n = len(nodes)
    if n <= 2:
        return 0.0

    score = 0.0
    for source in nodes:
        if source == node:
            continue
        for target in nodes:
            if target == node or target == source:
                continue
            if _is_on_shortest_path(graph, source, target, node):
                score += 1

    if normalized:
        denominator = (n - 1) * (n - 2)
        if denominator > 0:
            score /= denominator

    return score


def _is_on_shortest_path(graph, source, target, intermediate):
    """Check if intermediate node is on any shortest path from source to target."""
    dist_s, _ = _bfs(graph, source)
    dist_t, _ = _bfs(graph, target)

    if dist_s.get(target, float('inf')) == float('inf'):
        return False

    shortest_dist = dist_s[target]
    if dist_s.get(intermediate, float('inf')) + dist_t.get(intermediate, float('inf')) == shortest_dist:
        return True
    return False


def _bfs(graph, start):
    """Breadth-first search returning distances and predecessors."""
    distances = {start: 0}
    predecessors = {start: None}
    queue = deque([start])

    while queue:
        current = queue.popleft()
        for neighbor in graph.get(current, []):
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                predecessors[neighbor] = current
                queue.append(neighbor)

    return distances, predecessors


def closeness_centrality(graph, node, normalized=True):
    """
    Compute closeness centrality.
    Closeness = 1 / average_shortest_path_length

    Args:
        graph: Adjacency list
        node: Target node
        normalized: Use n-1 as denominator instead of sum of distances

    Returns:
        Closeness centrality score
    """
    distances, _ = _bfs(graph, node)
    reachable = [d for d in distances.values() if d > 0]

    if not reachable:
        return 0.0

    if normalized:
        n = len(graph)
        return len(reachable) / sum(reachable) if sum(reachable) > 0 else 0.0
    else:
        return len(reachable) / sum(reachable) if sum(reachable) > 0 else 0.0


def page_rank(graph, damping=0.85, iterations=100, tolerance=1e-6):
    """
    Compute PageRank scores for all nodes.

    Args:
        graph: Adjacency list
        damping: Damping factor (0.85 typical)
        iterations: Maximum iterations
        tolerance: Convergence threshold

    Returns:
        Dict mapping node -> PageRank score
    """
    nodes = list(graph.keys())
    n = len(nodes)
    if n == 0:
        return {}

    ranks = {node: 1.0 / n for node in nodes}

    for _ in range(iterations):
        new_ranks = {}
        dangling_sum = 0.0

        for node in nodes:
            if not graph.get(node):
                dangling_sum += ranks[node]

        for node in nodes:
            rank_sum = 0.0
            for other in nodes:
                if node in graph.get(other, []):
                    out_degree = len(graph[other])
                    if out_degree > 0:
                        rank_sum += ranks[other] / out_degree

            new_ranks[node] = (1 - damping) / n + damping * (rank_sum + dangling_sum / n)

        diff = sum(abs(new_ranks[node] - ranks[node]) for node in nodes)
        ranks = new_ranks
        if diff < tolerance:
            break

    return ranks


def clustering_coefficient(graph, node):
    """
    Compute local clustering coefficient for a node.
    Fraction of node's neighbors that are also neighbors of each other.

    Args:
        graph: Adjacency list
        node: Target node

    Returns:
        Clustering coefficient (0.0 to 1.0)
    """
    neighbors = graph.get(node, [])
    k = len(neighbors)

    if k < 2:
        return 0.0

    edges_between_neighbors = 0
    for i, n1 in enumerate(neighbors):
        for n2 in neighbors[i + 1:]:
            if n2 in graph.get(n1, []) or n1 in graph.get(n2, []):
                edges_between_neighbors += 1

    return (2.0 * edges_between_neighbors) / (k * (k - 1))


def average_clustering_coefficient(graph):
    """Compute average clustering coefficient over all nodes."""
    nodes = list(graph.keys())
    if not nodes:
        return 0.0
    return sum(clustering_coefficient(graph, n) for n in nodes) / len(nodes)


def is_connected(graph):
    """Check if graph is connected (weakly for directed)."""
    if not graph:
        return True
    nodes = list(graph.keys())
    visited = set()
    queue = deque(nodes)

    queue = deque([nodes[0]])
    visited.add(nodes[0])

    while queue:
        current = queue.popleft()
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return len(visited) == len(nodes)


def count_connected_components(graph):
    """Count number of connected components."""
    if not graph:
        return 0

    nodes = list(graph.keys())
    visited = set()
    components = 0

    for node in nodes:
        if node not in visited:
            components += 1
            queue = deque([node])
            visited.add(node)
            while queue:
                current = queue.popleft()
                for neighbor in graph.get(current, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

    return components


def graph_density(graph):
    """
    Compute graph density.
    Density = actual_edges / possible_edges

    For undirected graphs.
    """
    n = len(graph)
    if n < 2:
        return 0.0

    edges = set()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            edge = tuple(sorted([node, neighbor]))
            edges.add(edge)

    max_edges = n * (n - 1) / 2
    return len(edges) / max_edges if max_edges > 0 else 0.0


def shortest_path_length(graph, source, target):
    """
    Find shortest path length between two nodes using BFS.

    Returns:
        Path length (number of edges) or None if no path exists
    """
    if source == target:
        return 0

    distances, _ = _bfs(graph, source)
    dist = distances.get(target)
    return int(dist) if dist is not None and dist != float('inf') else None


def all_pairs_shortest_paths(graph):
    """
    Compute all-pairs shortest path lengths using Floyd-Warshall.
    Returns dict of (source, target) -> distance
    """
    nodes = list(graph.keys())
    n = len(nodes)
    if n == 0:
        return {}

    dist = {}
    for a in nodes:
        for b in nodes:
            dist[(a, b)] = 0 if a == b else float('inf')

    for node, neighbors in graph.items():
        for neighbor in neighbors:
            dist[(node, neighbor)] = 1

    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[(i, k)] + dist[(k, j)] < dist[(i, j)]:
                    dist[(i, j)] = dist[(i, k)] + dist[(k, j)]

    return {k: int(v) for k, v in dist.items() if v != float('inf')}


def eccentricity(graph, node):
    """
    Eccentricity of a node = maximum distance to all other nodes.
    Returns None if node is isolated.
    """
    distances, _ = _bfs(graph, node)
    non_zero = [d for d in distances.values() if d > 0]
    return int(max(non_zero)) if non_zero else None


def graph_diameter(graph):
    """
    Graph diameter = maximum eccentricity across all nodes.
    Returns None if graph is disconnected.
    """
    nodes = list(graph.keys())
    if not nodes:
        return None

    diameters = [eccentricity(graph, n) for n in nodes]
    valid = [d for d in diameters if d is not None]
    return max(valid) if valid else None


def graph_radius(graph):
    """
    Graph radius = minimum eccentricity across all nodes.
    """
    nodes = list(graph.keys())
    if not nodes:
        return None

    eccens = [eccentricity(graph, n) for n in nodes]
    valid = [e for e in eccens if e is not None]
    return min(valid) if valid else None