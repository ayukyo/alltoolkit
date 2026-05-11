"""
Dijkstra's Shortest Path Algorithm Utilities

A comprehensive implementation of Dijkstra's algorithm for finding the shortest
paths between nodes in a graph. Supports weighted graphs with non-negative edges.

Features:
- Find shortest path between two nodes
- Find shortest paths to all nodes from a source
- Support for adjacency list and edge list representations
- Path reconstruction with total distance
- Support for custom graph structures
- Priority queue optimization (heap-based)
- Early termination when target is found

Time Complexity: O((V + E) log V) with binary heap
Space Complexity: O(V)

Author: AllToolkit
License: MIT
"""

import heapq
from typing import Dict, List, Tuple, Optional, Set, Any, Union
from dataclasses import dataclass
from enum import Enum


class NodeType(Enum):
    """Node representation types."""
    INTEGER = "integer"
    STRING = "string"
    TUPLE = "tuple"


@dataclass
class GraphEdge:
    """Represents a weighted edge in the graph."""
    target: Union[int, str, Tuple]
    weight: float
    
    def __post_init__(self):
        if self.weight < 0:
            raise ValueError("Dijkstra's algorithm does not support negative weights")


@dataclass
class PathResult:
    """Result of a shortest path search."""
    distance: float
    path: List[Union[int, str, Tuple]]
    found: bool
    
    def __repr__(self) -> str:
        if not self.found:
            return f"PathResult(not found)"
        return f"PathResult(distance={self.distance}, path={self.path})"


@dataclass
class AllPathsResult:
    """Result of finding shortest paths to all reachable nodes."""
    source: Union[int, str, Tuple]
    distances: Dict[Union[int, str, Tuple], float]
    predecessors: Dict[Union[int, str, Tuple], Optional[Union[int, str, Tuple]]]
    
    def get_path_to(self, target: Union[int, str, Tuple]) -> PathResult:
        """Reconstruct path to a specific target."""
        if target not in self.distances:
            return PathResult(distance=float('inf'), path=[], found=False)
        
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = self.predecessors.get(current)
        path.reverse()
        
        return PathResult(distance=self.distances[target], path=path, found=True)
    
    def get_reachable_nodes(self) -> Set[Union[int, str, Tuple]]:
        """Get all nodes reachable from source."""
        return set(self.distances.keys())


class DijkstraGraph:
    """
    A graph implementation optimized for Dijkstra's algorithm.
    
    Supports:
    - Adding nodes and weighted edges
    - Both directed and undirected graphs
    - Multiple edge representations
    - Custom node types (int, str, tuple)
    
    Example:
        graph = DijkstraGraph()
        graph.add_edge('A', 'B', 4)
        graph.add_edge('B', 'C', 3)
        result = graph.shortest_path('A', 'C')
        print(result.path)  # ['A', 'B', 'C']
        print(result.distance)  # 7.0
    """
    
    def __init__(self, directed: bool = True):
        """
        Initialize the graph.
        
        Args:
            directed: If True, edges are one-way. If False, edges are bidirectional.
        """
        self._adjacency: Dict[Union[int, str, Tuple], List[GraphEdge]] = {}
        self._directed = directed
        self._node_count = 0
        self._edge_count = 0
    
    def add_node(self, node: Union[int, str, Tuple]) -> 'DijkstraGraph':
        """
        Add a node to the graph.
        
        Args:
            node: The node to add (int, str, or tuple)
            
        Returns:
            Self for method chaining
        """
        if node not in self._adjacency:
            self._adjacency[node] = []
            self._node_count += 1
        return self
    
    def add_edge(self, source: Union[int, str, Tuple], 
                 target: Union[int, str, Tuple], 
                 weight: float = 1.0) -> 'DijkstraGraph':
        """
        Add a weighted edge to the graph.
        
        Args:
            source: Source node
            target: Target node
            weight: Edge weight (must be non-negative)
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If weight is negative
        """
        if weight < 0:
            raise ValueError("Dijkstra's algorithm does not support negative weights")
        
        # Ensure nodes exist
        self.add_node(source)
        self.add_node(target)
        
        # Add edge
        self._adjacency[source].append(GraphEdge(target=target, weight=weight))
        self._edge_count += 1
        
        # Add reverse edge for undirected graph
        if not self._directed:
            self._adjacency[target].append(GraphEdge(target=source, weight=weight))
            self._edge_count += 1
        
        return self
    
    def add_edges(self, edges: List[Tuple]) -> 'DijkstraGraph':
        """
        Add multiple edges at once.
        
        Args:
            edges: List of (source, target, weight) tuples or (source, target) pairs
            
        Returns:
            Self for method chaining
        """
        for edge in edges:
            if len(edge) == 2:
                self.add_edge(edge[0], edge[1])
            elif len(edge) == 3:
                self.add_edge(edge[0], edge[1], edge[2])
        return self
    
    def remove_node(self, node: Union[int, str, Tuple]) -> 'DijkstraGraph':
        """
        Remove a node and all its edges from the graph.
        
        Args:
            node: The node to remove
            
        Returns:
            Self for method chaining
        """
        if node in self._adjacency:
            # Count edges being removed
            self._edge_count -= len(self._adjacency[node])
            del self._adjacency[node]
            self._node_count -= 1
            
            # Remove edges pointing to this node
            for n in self._adjacency:
                before = len(self._adjacency[n])
                self._adjacency[n] = [e for e in self._adjacency[n] if e.target != node]
                self._edge_count -= (before - len(self._adjacency[n]))
        
        return self
    
    def remove_edge(self, source: Union[int, str, Tuple], 
                    target: Union[int, str, Tuple]) -> 'DijkstraGraph':
        """
        Remove an edge from the graph.
        
        Args:
            source: Source node
            target: Target node
            
        Returns:
            Self for method chaining
        """
        # Remove edge from source to target
        if source in self._adjacency:
            before = len(self._adjacency[source])
            self._adjacency[source] = [e for e in self._adjacency[source] 
                                       if e.target != target]
            self._edge_count -= (before - len(self._adjacency[source]))
        
        # For undirected graphs, also remove the reverse edge
        if not self._directed and target in self._adjacency:
            before = len(self._adjacency[target])
            self._adjacency[target] = [e for e in self._adjacency[target]
                                       if e.target != source]
            self._edge_count -= (before - len(self._adjacency[target]))
        
        return self
    
    def get_neighbors(self, node: Union[int, str, Tuple]) -> List[GraphEdge]:
        """Get all neighbors of a node."""
        return self._adjacency.get(node, [])
    
    def has_node(self, node: Union[int, str, Tuple]) -> bool:
        """Check if a node exists in the graph."""
        return node in self._adjacency
    
    def has_edge(self, source: Union[int, str, Tuple], 
                 target: Union[int, str, Tuple]) -> bool:
        """Check if an edge exists between two nodes."""
        if source not in self._adjacency:
            return False
        return any(e.target == target for e in self._adjacency[source])
    
    def get_edge_weight(self, source: Union[int, str, Tuple], 
                        target: Union[int, str, Tuple]) -> Optional[float]:
        """Get the weight of an edge, or None if it doesn't exist."""
        if source not in self._adjacency:
            return None
        for edge in self._adjacency[source]:
            if edge.target == target:
                return edge.weight
        return None
    
    @property
    def nodes(self) -> Set[Union[int, str, Tuple]]:
        """Get all nodes in the graph."""
        return set(self._adjacency.keys())
    
    @property
    def node_count(self) -> int:
        """Get the number of nodes."""
        return self._node_count
    
    @property
    def edge_count(self) -> int:
        """Get the number of edges."""
        return self._edge_count
    
    @property
    def is_directed(self) -> bool:
        """Check if the graph is directed."""
        return self._directed
    
    def shortest_path(self, source: Union[int, str, Tuple], 
                      target: Union[int, str, Tuple]) -> PathResult:
        """
        Find the shortest path between two nodes using Dijkstra's algorithm.
        
        Args:
            source: Starting node
            target: Destination node
            
        Returns:
            PathResult containing distance and path, or found=False if no path exists
        """
        if source not in self._adjacency:
            return PathResult(distance=float('inf'), path=[], found=False)
        
        if target not in self._adjacency:
            return PathResult(distance=float('inf'), path=[], found=False)
        
        if source == target:
            return PathResult(distance=0, path=[source], found=True)
        
        # Initialize distances
        distances: Dict[Union[int, str, Tuple], float] = {node: float('inf') 
                                                          for node in self._adjacency}
        distances[source] = 0
        
        # Predecessor tracking for path reconstruction
        predecessors: Dict[Union[int, str, Tuple], Optional[Union[int, str, Tuple]]] = {}
        
        # Priority queue: (distance, node)
        # Using counter to break ties (Python's heapq doesn't handle node comparison well)
        counter = 0
        pq: List[Tuple[float, int, Union[int, str, Tuple]]] = [(0, counter, source)]
        
        # Track visited nodes
        visited: Set[Union[int, str, Tuple]] = set()
        
        while pq:
            current_dist, _, current = heapq.heappop(pq)
            
            # Skip if already visited
            if current in visited:
                continue
            
            visited.add(current)
            
            # Early termination if we reached the target
            if current == target:
                break
            
            # Explore neighbors
            for edge in self._adjacency.get(current, []):
                if edge.target in visited:
                    continue
                
                # Skip if target node was removed (for k_shortest_paths)
                if edge.target not in distances:
                    continue
                
                new_dist = current_dist + edge.weight
                
                if new_dist < distances[edge.target]:
                    distances[edge.target] = new_dist
                    predecessors[edge.target] = current
                    counter += 1
                    heapq.heappush(pq, (new_dist, counter, edge.target))
        
        # Check if target is reachable
        if distances[target] == float('inf'):
            return PathResult(distance=float('inf'), path=[], found=False)
        
        # Reconstruct path
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = predecessors.get(current)
        path.reverse()
        
        return PathResult(distance=distances[target], path=path, found=True)
    
    def shortest_paths_from(self, source: Union[int, str, Tuple]) -> AllPathsResult:
        """
        Find shortest paths from source to all reachable nodes.
        
        Args:
            source: Starting node
            
        Returns:
            AllPathsResult containing distances and path reconstruction data
        """
        if source not in self._adjacency:
            return AllPathsResult(
                source=source,
                distances={},
                predecessors={}
            )
        
        # Initialize
        distances: Dict[Union[int, str, Tuple], float] = {node: float('inf') 
                                                          for node in self._adjacency}
        distances[source] = 0
        
        predecessors: Dict[Union[int, str, Tuple], Optional[Union[int, str, Tuple]]] = {}
        
        counter = 0
        pq: List[Tuple[float, int, Union[int, str, Tuple]]] = [(0, counter, source)]
        visited: Set[Union[int, str, Tuple]] = set()
        
        while pq:
            current_dist, _, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            for edge in self._adjacency.get(current, []):
                if edge.target in visited:
                    continue
                
                # Skip if target node was removed
                if edge.target not in distances:
                    continue
                
                new_dist = current_dist + edge.weight
                
                if new_dist < distances[edge.target]:
                    distances[edge.target] = new_dist
                    predecessors[edge.target] = current
                    counter += 1
                    heapq.heappush(pq, (new_dist, counter, edge.target))
        
        # Remove unreachable nodes from distances
        distances = {k: v for k, v in distances.items() if v < float('inf')}
        
        return AllPathsResult(source=source, distances=distances, predecessors=predecessors)
    
    def k_shortest_paths(self, source: Union[int, str, Tuple], 
                         target: Union[int, str, Tuple], 
                         k: int = 3) -> List[PathResult]:
        """
        Find the k shortest paths between two nodes using Yen's algorithm.
        
        Args:
            source: Starting node
            target: Destination node
            k: Number of paths to find
            
        Returns:
            List of PathResult objects, sorted by distance
        """
        if source not in self._adjacency or target not in self._adjacency:
            return []
        
        if source == target:
            return [PathResult(distance=0, path=[source], found=True)]
        
        # Find the shortest path first
        shortest = self.shortest_path(source, target)
        if not shortest.found:
            return []
        
        paths = [shortest]
        
        if k == 1:
            return paths
        
        # Candidates for next shortest paths
        candidates: List[Tuple[float, int, List[Union[int, str, Tuple]]]] = []
        candidate_counter = 0
        
        for i in range(1, k):
            if not paths:
                break
            
            prev_path = paths[-1].path
            
            # Generate deviations from previous paths
            for j in range(len(prev_path) - 1):
                # Spur node
                spur_node = prev_path[j]
                
                # Root path
                root_path = prev_path[:j + 1]
                
                # Create a modified graph
                temp_graph = DijkstraGraph(directed=self._directed)
                for node in self._adjacency:
                    temp_graph.add_node(node)
                
                for node, edges in self._adjacency.items():
                    for edge in edges:
                        temp_graph._adjacency[node].append(edge)
                
                # Remove edges that would recreate previously found paths
                for path_result in paths:
                    path = path_result.path
                    if len(path) > j and path[:j + 1] == root_path:
                        if len(path) > j + 1:
                            # Remove the edge
                            temp_graph._adjacency[spur_node] = [
                                e for e in temp_graph._adjacency[spur_node]
                                if e.target != path[j + 1]
                            ]
                
                # Remove root path nodes (except spur) from graph
                for node in root_path[:-1]:
                    if node in temp_graph._adjacency:
                        del temp_graph._adjacency[node]
                
                # Find spur path
                spur_result = temp_graph.shortest_path(spur_node, target)
                
                if spur_result.found:
                    total_path = root_path[:-1] + spur_result.path
                    
                    # Calculate distance
                    distance = 0
                    for idx in range(len(total_path) - 1):
                        d = self.get_edge_weight(total_path[idx], total_path[idx + 1])
                        if d is not None:
                            distance += d
                    
                    # Check if this path is unique
                    path_tuple = tuple(total_path)
                    is_duplicate = any(
                        tuple(p.path) == path_tuple for p in paths
                    ) or any(
                        tuple(p[2]) == path_tuple for p in candidates
                    )
                    
                    if not is_duplicate:
                        candidates.append((distance, candidate_counter, total_path))
                        candidate_counter += 1
            
            if not candidates:
                break
            
            # Get the best candidate
            candidates.sort()
            best_dist, _, best_path = candidates.pop(0)
            paths.append(PathResult(distance=best_dist, path=best_path, found=True))
        
        return paths[:k]
    
    def clear(self) -> None:
        """Remove all nodes and edges from the graph."""
        self._adjacency.clear()
        self._node_count = 0
        self._edge_count = 0
    
    def copy(self) -> 'DijkstraGraph':
        """Create a deep copy of the graph."""
        new_graph = DijkstraGraph(directed=self._directed)
        for node, edges in self._adjacency.items():
            new_graph._adjacency[node] = [GraphEdge(target=e.target, weight=e.weight) 
                                           for e in edges]
        new_graph._node_count = self._node_count
        new_graph._edge_count = self._edge_count
        return new_graph
    
    def to_adjacency_matrix(self) -> Tuple[List[Union[int, str, Tuple]], List[List[float]]]:
        """
        Convert graph to adjacency matrix representation.
        
        Returns:
            Tuple of (node_list, adjacency_matrix)
            where matrix[i][j] = weight of edge from node_list[i] to node_list[j]
            (float('inf') if no edge exists)
        """
        nodes = sorted(self._adjacency.keys(), key=lambda x: str(x))
        n = len(nodes)
        node_to_idx = {node: i for i, node in enumerate(nodes)}
        
        matrix = [[float('inf')] * n for _ in range(n)]
        
        # Diagonal is 0
        for i in range(n):
            matrix[i][i] = 0
        
        # Fill edges
        for node, edges in self._adjacency.items():
            i = node_to_idx[node]
            for edge in edges:
                j = node_to_idx[edge.target]
                matrix[i][j] = edge.weight
        
        return nodes, matrix
    
    @classmethod
    def from_adjacency_list(cls, 
                           adj_list: Dict[Union[int, str, Tuple], 
                                         List[Tuple[Union[int, str, Tuple], float]]],
                           directed: bool = True) -> 'DijkstraGraph':
        """
        Create a graph from an adjacency list.
        
        Args:
            adj_list: Dictionary mapping nodes to list of (neighbor, weight) tuples
            directed: Whether the graph is directed
            
        Returns:
            New DijkstraGraph instance
        """
        graph = cls(directed=directed)
        for node, neighbors in adj_list.items():
            graph.add_node(node)
            for neighbor, weight in neighbors:
                graph.add_edge(node, neighbor, weight)
        return graph
    
    @classmethod
    def from_edge_list(cls, 
                      edges: List[Tuple],
                      directed: bool = True) -> 'DijkstraGraph':
        """
        Create a graph from a list of edges.
        
        Args:
            edges: List of (source, target, weight) or (source, target) tuples
            directed: Whether the graph is directed
            
        Returns:
            New DijkstraGraph instance
        """
        graph = cls(directed=directed)
        for edge in edges:
            if len(edge) == 2:
                graph.add_edge(edge[0], edge[1])
            elif len(edge) == 3:
                graph.add_edge(edge[0], edge[1], edge[2])
        return graph
    
    @classmethod
    def from_adjacency_matrix(cls,
                             matrix: List[List[float]],
                             nodes: Optional[List[Union[int, str, Tuple]]] = None,
                             directed: bool = True) -> 'DijkstraGraph':
        """
        Create a graph from an adjacency matrix.
        
        Args:
            matrix: 2D list where matrix[i][j] = weight (or inf/None for no edge)
            nodes: Optional list of node labels (defaults to indices 0, 1, 2, ...)
            directed: Whether the graph is directed
            
        Returns:
            New DijkstraGraph instance
        """
        n = len(matrix)
        if nodes is None:
            nodes = list(range(n))
        
        graph = cls(directed=directed)
        
        for i in range(n):
            for j in range(n):
                if i != j:  # Skip diagonal
                    weight = matrix[i][j]
                    if weight is not None and weight != float('inf'):
                        graph.add_edge(nodes[i], nodes[j], weight)
        
        return graph


def dijkstra(graph: Union[DijkstraGraph, Dict],
             source: Union[int, str, Tuple],
             target: Optional[Union[int, str, Tuple]] = None) -> Union[PathResult, AllPathsResult]:
    """
    Convenience function to run Dijkstra's algorithm.
    
    Args:
        graph: DijkstraGraph instance or adjacency list dictionary
        source: Starting node
        target: Optional target node (if None, finds paths to all nodes)
        
    Returns:
        PathResult if target is specified, AllPathsResult otherwise
    """
    if isinstance(graph, dict):
        g = DijkstraGraph.from_adjacency_list(graph)
    else:
        g = graph
    
    if target is not None:
        return g.shortest_path(source, target)
    return g.shortest_paths_from(source)


def shortest_path(graph: Union[DijkstraGraph, Dict],
                  source: Union[int, str, Tuple],
                  target: Union[int, str, Tuple]) -> PathResult:
    """
    Convenience function to find the shortest path between two nodes.
    
    Args:
        graph: DijkstraGraph instance or adjacency list dictionary
        source: Starting node
        target: Destination node
        
    Returns:
        PathResult with distance and path
    """
    if isinstance(graph, dict):
        g = DijkstraGraph.from_adjacency_list(graph)
    else:
        g = graph
    
    return g.shortest_path(source, target)


def all_shortest_paths(graph: Union[DijkstraGraph, Dict],
                       source: Union[int, str, Tuple]) -> AllPathsResult:
    """
    Convenience function to find shortest paths to all reachable nodes.
    
    Args:
        graph: DijkstraGraph instance or adjacency list dictionary
        source: Starting node
        
    Returns:
        AllPathsResult with distances and path data
    """
    if isinstance(graph, dict):
        g = DijkstraGraph.from_adjacency_list(graph)
    else:
        g = graph
    
    return g.shortest_paths_from(source)


def is_connected(graph: DijkstraGraph, 
                 node1: Union[int, str, Tuple], 
                 node2: Union[int, str, Tuple]) -> bool:
    """
    Check if two nodes are connected.
    
    Args:
        graph: DijkstraGraph instance
        node1: First node
        node2: Second node
        
    Returns:
        True if there is a path between the nodes
    """
    result = graph.shortest_path(node1, node2)
    return result.found


def get_reachable_nodes(graph: DijkstraGraph, 
                        source: Union[int, str, Tuple]) -> Set[Union[int, str, Tuple]]:
    """
    Get all nodes reachable from a source node.
    
    Args:
        graph: DijkstraGraph instance
        source: Starting node
        
    Returns:
        Set of reachable nodes
    """
    result = graph.shortest_paths_from(source)
    return result.get_reachable_nodes()


def graph_diameter(graph: DijkstraGraph) -> Tuple[float, 
                                                   Tuple[Union[int, str, Tuple], 
                                                         Union[int, str, Tuple]]]:
    """
    Calculate the diameter of a graph (longest shortest path).
    
    For disconnected graphs, returns the diameter of the largest component.
    
    Args:
        graph: DijkstraGraph instance
        
    Returns:
        Tuple of (diameter, (node1, node2)) where diameter is the longest
        shortest path and (node1, node2) are the endpoints
    """
    max_dist = 0
    endpoints = (None, None)
    
    nodes = list(graph.nodes)
    for i, source in enumerate(nodes):
        result = graph.shortest_paths_from(source)
        for target, dist in result.distances.items():
            if dist > max_dist:
                max_dist = dist
                endpoints = (source, target)
    
    return max_dist, endpoints


def center_of_graph(graph: DijkstraGraph) -> List[Union[int, str, Tuple]]:
    """
    Find the center of the graph (nodes with minimum eccentricity).
    
    Eccentricity of a node is the maximum distance to any other node.
    The center consists of nodes with minimum eccentricity.
    
    Args:
        graph: DijkstraGraph instance
        
    Returns:
        List of center nodes
    """
    nodes = list(graph.nodes)
    if not nodes:
        return []
    
    eccentricities = {}
    
    for node in nodes:
        result = graph.shortest_paths_from(node)
        if result.distances:
            eccentricities[node] = max(result.distances.values())
        else:
            eccentricities[node] = float('inf')
    
    min_eccentricity = min(eccentricities.values())
    return [node for node, ecc in eccentricities.items() if ecc == min_eccentricity]


if __name__ == "__main__":
    # Quick demo
    print("=== Dijkstra's Algorithm Demo ===\n")
    
    # Create a simple graph
    g = DijkstraGraph(directed=False)
    g.add_edge('A', 'B', 4)
    g.add_edge('A', 'C', 2)
    g.add_edge('B', 'C', 1)
    g.add_edge('B', 'D', 5)
    g.add_edge('C', 'D', 8)
    g.add_edge('C', 'E', 10)
    g.add_edge('D', 'E', 2)
    g.add_edge('D', 'Z', 6)
    g.add_edge('E', 'Z', 3)
    
    print("Graph edges:")
    for node in sorted(g.nodes):
        for edge in g.get_neighbors(node):
            print(f"  {node} -> {edge.target} (weight: {edge.weight})")
    
    print("\n--- Shortest Path: A to Z ---")
    result = g.shortest_path('A', 'Z')
    print(f"Path: {' -> '.join(map(str, result.path))}")
    print(f"Distance: {result.distance}")
    
    print("\n--- All Paths from A ---")
    all_paths = g.shortest_paths_from('A')
    for node in sorted(g.nodes):
        path_result = all_paths.get_path_to(node)
        if path_result.found:
            print(f"  To {node}: {path_result.distance} via {' -> '.join(map(str, path_result.path))}")
    
    print("\n--- K-Shortest Paths (A to Z, k=3) ---")
    k_paths = g.k_shortest_paths('A', 'Z', k=3)
    for i, path_result in enumerate(k_paths, 1):
        print(f"  Path {i}: {' -> '.join(map(str, path_result.path))} (distance: {path_result.distance})")
    
    print("\n--- Graph Statistics ---")
    print(f"Nodes: {g.node_count}")
    print(f"Edges: {g.edge_count}")
    print(f"Is directed: {g.is_directed}")
    
    diameter, endpoints = graph_diameter(g)
    print(f"Diameter: {diameter} (between {endpoints[0]} and {endpoints[1]})")
    
    center = center_of_graph(g)
    print(f"Center nodes: {center}")