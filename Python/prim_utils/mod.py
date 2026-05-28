"""
Prim's Minimum Spanning Tree Algorithm Utilities

A comprehensive implementation of Prim's algorithm for finding the minimum
spanning tree (MST) of a connected, undirected, weighted graph.

Features:
- Find MST edges and total weight
- Support for adjacency list and edge list representations
- Prim's algorithm with priority queue optimization
- Lazy and eager implementations
- Handle disconnected graphs (find MST for each component)
- Borůvka's algorithm variant for parallel processing
- Kruskal's algorithm comparison
- Graph utility functions

Time Complexity: O(E log V) with binary heap
Space Complexity: O(V)

Author: AllToolkit
License: MIT
"""

import heapq
from typing import Dict, List, Tuple, Optional, Set, Any, Union, Callable
from dataclasses import dataclass, field
from enum import Enum


class MSTAlgorithm(Enum):
    """Available MST algorithms."""
    PRIM = "prim"
    KRUSKAL = "kruskal"
    BORUVKA = "boruvka"


@dataclass
class Edge:
    """Represents a weighted edge in the graph."""
    source: Union[int, str, Tuple]
    target: Union[int, str, Tuple]
    weight: float
    
    def __lt__(self, other: 'Edge') -> bool:
        return self.weight < other.weight
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Edge):
            return False
        return (self.source == other.source and 
                self.target == other.target and 
                self.weight == other.weight)
    
    def __hash__(self) -> int:
        return hash((self.source, self.target, self.weight))
    
    def reverse(self) -> 'Edge':
        """Return a new edge with reversed direction."""
        return Edge(source=self.target, target=self.source, weight=self.weight)


@dataclass
class MSTResult:
    """Result of a minimum spanning tree computation."""
    edges: List[Edge]
    total_weight: float
    connected: bool
    node_count: int
    
    def __repr__(self) -> str:
        status = "connected" if self.connected else "disconnected"
        return f"MSTResult(edges={len(self.edges)}, weight={self.total_weight:.2f}, {status})"
    
    @property
    def edge_count(self) -> int:
        """Number of edges in the MST."""
        return len(self.edges)
    
    def get_edge_list(self) -> List[Tuple]:
        """Get edges as list of (source, target, weight) tuples."""
        return [(e.source, e.target, e.weight) for e in self.edges]
    
    def get_adjacency_list(self) -> Dict[Union[int, str, Tuple], List[Tuple[Union[int, str, Tuple], float]]]:
        """Get MST as adjacency list."""
        adj: Dict[Union[int, str, Tuple], List[Tuple[Union[int, str, Tuple], float]]] = {}
        for edge in self.edges:
            if edge.source not in adj:
                adj[edge.source] = []
            if edge.target not in adj:
                adj[edge.target] = []
            adj[edge.source].append((edge.target, edge.weight))
            adj[edge.target].append((edge.source, edge.weight))
        return adj


@dataclass
class ForestResult:
    """Result of MST computation on potentially disconnected graph."""
    trees: List[MSTResult]
    total_weight: float
    component_count: int
    
    def __repr__(self) -> str:
        return f"ForestResult(components={self.component_count}, total_weight={self.total_weight:.2f})"
    
    @property
    def all_edges(self) -> List[Edge]:
        """Get all edges from all trees."""
        edges = []
        for tree in self.trees:
            edges.extend(tree.edges)
        return edges


class PrimGraph:
    """
    A graph implementation optimized for Prim's algorithm.
    
    Supports:
    - Adding nodes and weighted edges
    - Both directed and undirected graphs (MST requires undirected)
    - Multiple edge representations
    - Custom node types (int, str, tuple)
    
    Example:
        graph = PrimGraph()
        graph.add_edge('A', 'B', 4)
        graph.add_edge('B', 'C', 3)
        mst = graph.minimum_spanning_tree()
        print(f"Total weight: {mst.total_weight}")
        for edge in mst.edges:
            print(f"  {edge.source} -- {edge.target} (weight: {edge.weight})")
    """
    
    def __init__(self, directed: bool = False):
        """
        Initialize the graph.
        
        Args:
            directed: If True, edges are one-way. MST requires undirected graphs.
        """
        self._adjacency: Dict[Union[int, str, Tuple], List[Edge]] = {}
        self._directed = directed
        self._node_count = 0
        self._edge_count = 0
    
    def add_node(self, node: Union[int, str, Tuple]) -> 'PrimGraph':
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
                 weight: float = 1.0) -> 'PrimGraph':
        """
        Add a weighted edge to the graph.
        
        Args:
            source: Source node
            target: Target node
            weight: Edge weight
            
        Returns:
            Self for method chaining
        """
        self.add_node(source)
        self.add_node(target)
        
        edge = Edge(source=source, target=target, weight=weight)
        self._adjacency[source].append(edge)
        self._edge_count += 1
        
        # Add reverse edge for undirected graph
        if not self._directed:
            reverse_edge = Edge(source=target, target=source, weight=weight)
            self._adjacency[target].append(reverse_edge)
        
        return self
    
    def add_edges(self, edges: List[Tuple]) -> 'PrimGraph':
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
    
    def remove_node(self, node: Union[int, str, Tuple]) -> 'PrimGraph':
        """Remove a node and all its edges from the graph."""
        if node in self._adjacency:
            # For directed graphs: subtract edges from this node
            # For undirected graphs: this counts all edges (each edge appears once in logical count)
            edges_from_node = len(self._adjacency[node])
            
            del self._adjacency[node]
            self._node_count -= 1
            
            # Remove edges pointing to this node from other nodes' adjacency lists
            for n in self._adjacency:
                before = len(self._adjacency[n])
                self._adjacency[n] = [e for e in self._adjacency[n] if e.target != node]
                # For undirected graphs, we already counted these edges above
                # For directed graphs, we need to count edges pointing to the removed node
                if self._directed:
                    self._edge_count -= (before - len(self._adjacency[n]))
            
            # Update edge count based on edges from the removed node
            self._edge_count -= edges_from_node
        
        return self
    
    def remove_edge(self, source: Union[int, str, Tuple], 
                    target: Union[int, str, Tuple]) -> 'PrimGraph':
        """Remove an edge from the graph."""
        removed = 0
        
        # Remove edge from source to target
        if source in self._adjacency:
            before = len(self._adjacency[source])
            self._adjacency[source] = [e for e in self._adjacency[source] 
                                       if e.target != target]
            removed = before - len(self._adjacency[source])
        
        # For undirected graphs, also remove the reverse edge from adjacency
        # but don't decrement edge_count again (it's already counted as one logical edge)
        if not self._directed and target in self._adjacency:
            self._adjacency[target] = [e for e in self._adjacency[target]
                                       if e.target != source]
        
        # Decrement edge_count
        self._edge_count -= removed
        
        return self
    
    def get_neighbors(self, node: Union[int, str, Tuple]) -> List[Edge]:
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
    
    def minimum_spanning_tree(self, 
                               start: Optional[Union[int, str, Tuple]] = None,
                               algorithm: MSTAlgorithm = MSTAlgorithm.PRIM) -> MSTResult:
        """
        Find the minimum spanning tree using Prim's algorithm.
        
        Args:
            start: Optional starting node (defaults to first node in graph)
            algorithm: MST algorithm to use
            
        Returns:
            MSTResult containing edges and total weight
            
        Raises:
            ValueError: If graph is empty or directed
        """
        if self._directed:
            raise ValueError("MST requires an undirected graph. Create graph with directed=False.")
        
        if not self._adjacency:
            return MSTResult(edges=[], total_weight=0, connected=False, node_count=0)
        
        if algorithm == MSTAlgorithm.PRIM:
            return self._prim_mst(start)
        elif algorithm == MSTAlgorithm.KRUSKAL:
            return self._kruskal_mst()
        else:
            return self._boruvka_mst()
    
    def _prim_mst(self, start: Optional[Union[int, str, Tuple]] = None) -> MSTResult:
        """
        Prim's algorithm implementation using a priority queue.
        
        Time Complexity: O(E log V)
        Space Complexity: O(V)
        """
        nodes = list(self._adjacency.keys())
        
        if start is None:
            start = nodes[0]
        elif start not in self._adjacency:
            return MSTResult(edges=[], total_weight=0, connected=False, node_count=0)
        
        # Track visited nodes
        visited: Set[Union[int, str, Tuple]] = set()
        
        # MST edges
        mst_edges: List[Edge] = []
        total_weight = 0.0
        
        # Priority queue: (weight, counter, source, target)
        counter = 0
        pq: List[Tuple[float, int, Union[int, str, Tuple], Union[int, str, Tuple]]] = []
        
        # Start from the initial node
        visited.add(start)
        for edge in self._adjacency[start]:
            heapq.heappush(pq, (edge.weight, counter, edge.source, edge.target))
            counter += 1
        
        while pq and len(visited) < self._node_count:
            weight, _, source, target = heapq.heappop(pq)
            
            if target in visited:
                continue
            
            # Add edge to MST
            visited.add(target)
            mst_edges.append(Edge(source=source, target=target, weight=weight))
            total_weight += weight
            
            # Add edges from the new node
            for edge in self._adjacency[target]:
                if edge.target not in visited:
                    heapq.heappush(pq, (edge.weight, counter, edge.source, edge.target))
                    counter += 1
        
        connected = len(visited) == self._node_count
        return MSTResult(edges=mst_edges, total_weight=total_weight, 
                        connected=connected, node_count=len(visited))
    
    def _kruskal_mst(self) -> MSTResult:
        """
        Kruskal's algorithm implementation using Union-Find.
        
        Time Complexity: O(E log E)
        Space Complexity: O(V)
        """
        # Collect all unique edges
        edges_seen: Set[Tuple] = set()
        all_edges: List[Edge] = []
        
        for source, edges in self._adjacency.items():
            for edge in edges:
                # Normalize edge to avoid duplicates
                edge_key = (min(edge.source, edge.target), 
                           max(edge.source, edge.target), edge.weight)
                if edge_key not in edges_seen:
                    edges_seen.add(edge_key)
                    all_edges.append(edge)
        
        # Sort edges by weight
        all_edges.sort(key=lambda e: e.weight)
        
        # Union-Find
        parent: Dict[Union[int, str, Tuple], Union[int, str, Tuple]] = {}
        rank: Dict[Union[int, str, Tuple], int] = {}
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return False
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True
        
        # Initialize
        for node in self._adjacency:
            parent[node] = node
            rank[node] = 0
        
        # Build MST
        mst_edges: List[Edge] = []
        total_weight = 0.0
        
        for edge in all_edges:
            if union(edge.source, edge.target):
                mst_edges.append(edge)
                total_weight += edge.weight
                if len(mst_edges) == self._node_count - 1:
                    break
        
        connected = len(mst_edges) == self._node_count - 1
        return MSTResult(edges=mst_edges, total_weight=total_weight,
                        connected=connected, node_count=self._node_count)
    
    def _boruvka_mst(self) -> MSTResult:
        """
        Borůvka's algorithm implementation.
        
        Time Complexity: O(E log V)
        Good for parallel processing.
        """
        if not self._adjacency:
            return MSTResult(edges=[], total_weight=0, connected=False, node_count=0)
        
        # Union-Find
        parent: Dict[Union[int, str, Tuple], Union[int, str, Tuple]] = {}
        rank: Dict[Union[int, str, Tuple], int] = {}
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return False
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1
            return True
        
        # Initialize
        for node in self._adjacency:
            parent[node] = node
            rank[node] = 0
        
        mst_edges: List[Edge] = []
        total_weight = 0.0
        
        # Borůvka's iterations
        while len(mst_edges) < self._node_count - 1:
            # Find cheapest edge for each component
            cheapest: Dict[Union[int, str, Tuple], Optional[Edge]] = {
                node: None for node in self._adjacency
            }
            
            for node, edges in self._adjacency.items():
                component = find(node)
                for edge in edges:
                    target_component = find(edge.target)
                    if component != target_component:
                        if (cheapest[component] is None or 
                            edge.weight < cheapest[component].weight):
                            cheapest[component] = edge
            
            # Add cheapest edges
            added = False
            for node, edge in cheapest.items():
                if edge is not None:
                    if union(edge.source, edge.target):
                        mst_edges.append(edge)
                        total_weight += edge.weight
                        added = True
            
            if not added:
                break
        
        connected = len(mst_edges) == self._node_count - 1
        return MSTResult(edges=mst_edges, total_weight=total_weight,
                        connected=connected, node_count=self._node_count)
    
    def minimum_spanning_forest(self) -> ForestResult:
        """
        Find minimum spanning trees for all connected components.
        
        Returns:
            ForestResult containing MST for each component
        """
        if not self._adjacency:
            return ForestResult(trees=[], total_weight=0, component_count=0)
        
        # Find connected components
        visited: Set[Union[int, str, Tuple]] = set()
        components: List[Set[Union[int, str, Tuple]]] = []
        
        for node in self._adjacency:
            if node not in visited:
                # BFS to find component
                component: Set[Union[int, str, Tuple]] = set()
                queue = [node]
                while queue:
                    current = queue.pop(0)
                    if current in visited:
                        continue
                    visited.add(current)
                    component.add(current)
                    for edge in self._adjacency[current]:
                        if edge.target not in visited:
                            queue.append(edge.target)
                components.append(component)
        
        # Build MST for each component
        trees: List[MSTResult] = []
        total_weight = 0.0
        
        for component in components:
            if len(component) == 1:
                # Single node, no edges
                node = next(iter(component))
                trees.append(MSTResult(edges=[], total_weight=0, 
                                       connected=True, node_count=1))
            else:
                # Find MST starting from any node in the component
                start = next(iter(component))
                mst = self._prim_mst_for_component(start, component)
                trees.append(mst)
                total_weight += mst.total_weight
        
        return ForestResult(trees=trees, total_weight=total_weight,
                           component_count=len(components))
    
    def _prim_mst_for_component(self, 
                                start: Union[int, str, Tuple],
                                component: Set[Union[int, str, Tuple]]) -> MSTResult:
        """Prim's algorithm for a specific component."""
        visited: Set[Union[int, str, Tuple]] = set()
        mst_edges: List[Edge] = []
        total_weight = 0.0
        
        counter = 0
        pq: List[Tuple[float, int, Union[int, str, Tuple], Union[int, str, Tuple]]] = []
        
        visited.add(start)
        for edge in self._adjacency[start]:
            if edge.target in component:
                heapq.heappush(pq, (edge.weight, counter, edge.source, edge.target))
                counter += 1
        
        while pq and len(visited) < len(component):
            weight, _, source, target = heapq.heappop(pq)
            
            if target in visited:
                continue
            
            visited.add(target)
            mst_edges.append(Edge(source=source, target=target, weight=weight))
            total_weight += weight
            
            for edge in self._adjacency[target]:
                if edge.target not in visited and edge.target in component:
                    heapq.heappush(pq, (edge.weight, counter, edge.source, edge.target))
                    counter += 1
        
        return MSTResult(edges=mst_edges, total_weight=total_weight,
                        connected=True, node_count=len(visited))
    
    def is_connected(self) -> bool:
        """Check if the graph is connected."""
        if not self._adjacency:
            return True
        
        # BFS from any node
        start = next(iter(self._adjacency))
        visited: Set[Union[int, str, Tuple]] = {start}
        queue = [start]
        
        while queue:
            current = queue.pop(0)
            for edge in self._adjacency[current]:
                if edge.target not in visited:
                    visited.add(edge.target)
                    queue.append(edge.target)
        
        return len(visited) == self._node_count
    
    def get_connected_components(self) -> List[Set[Union[int, str, Tuple]]]:
        """Get all connected components of the graph."""
        visited: Set[Union[int, str, Tuple]] = set()
        components: List[Set[Union[int, str, Tuple]]] = []
        
        for node in self._adjacency:
            if node not in visited:
                component: Set[Union[int, str, Tuple]] = set()
                queue = [node]
                while queue:
                    current = queue.pop(0)
                    if current in visited:
                        continue
                    visited.add(current)
                    component.add(current)
                    for edge in self._adjacency[current]:
                        if edge.target not in visited:
                            queue.append(edge.target)
                components.append(component)
        
        return components
    
    def clear(self) -> None:
        """Remove all nodes and edges from the graph."""
        self._adjacency.clear()
        self._node_count = 0
        self._edge_count = 0
    
    def copy(self) -> 'PrimGraph':
        """Create a deep copy of the graph."""
        new_graph = PrimGraph(directed=self._directed)
        for node, edges in self._adjacency.items():
            new_graph._adjacency[node] = [Edge(source=e.source, target=e.target, weight=e.weight)
                                          for e in edges]
        new_graph._node_count = self._node_count
        new_graph._edge_count = self._edge_count
        return new_graph
    
    @classmethod
    def from_adjacency_list(cls,
                          adj_list: Dict[Union[int, str, Tuple], 
                                         List[Tuple[Union[int, str, Tuple], float]]],
                          directed: bool = False) -> 'PrimGraph':
        """
        Create a graph from an adjacency list.
        
        Args:
            adj_list: Dictionary mapping nodes to list of (neighbor, weight) tuples
            directed: Whether the graph is directed
            
        Returns:
            New PrimGraph instance
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
                      directed: bool = False) -> 'PrimGraph':
        """
        Create a graph from a list of edges.
        
        Args:
            edges: List of (source, target, weight) or (source, target) tuples
            directed: Whether the graph is directed
            
        Returns:
            New PrimGraph instance
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
                             directed: bool = False) -> 'PrimGraph':
        """
        Create a graph from an adjacency matrix.
        
        Args:
            matrix: 2D list where matrix[i][j] = weight (or inf/None for no edge)
            nodes: Optional list of node labels (defaults to indices 0, 1, 2, ...)
            directed: Whether the graph is directed
            
        Returns:
            New PrimGraph instance
        """
        n = len(matrix)
        if nodes is None:
            nodes = list(range(n))
        
        graph = cls(directed=directed)
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    weight = matrix[i][j]
                    if weight is not None and weight != float('inf'):
                        graph.add_edge(nodes[i], nodes[j], weight)
        
        return graph


# Convenience functions

def prim_mst(graph: Union[PrimGraph, Dict, List[Tuple]],
             start: Optional[Union[int, str, Tuple]] = None) -> MSTResult:
    """
    Convenience function to find MST using Prim's algorithm.
    
    Args:
        graph: PrimGraph instance, adjacency list, or edge list
        start: Optional starting node
        
    Returns:
        MSTResult with edges and total weight
    """
    if isinstance(graph, PrimGraph):
        return graph.minimum_spanning_tree(start, MSTAlgorithm.PRIM)
    elif isinstance(graph, dict):
        g = PrimGraph.from_adjacency_list(graph)
    else:
        g = PrimGraph.from_edge_list(graph)
    return g.minimum_spanning_tree(start, MSTAlgorithm.PRIM)


def kruskal_mst(graph: Union[PrimGraph, Dict, List[Tuple]]) -> MSTResult:
    """
    Convenience function to find MST using Kruskal's algorithm.
    
    Args:
        graph: PrimGraph instance, adjacency list, or edge list
        
    Returns:
        MSTResult with edges and total weight
    """
    if isinstance(graph, PrimGraph):
        return graph.minimum_spanning_tree(algorithm=MSTAlgorithm.KRUSKAL)
    elif isinstance(graph, dict):
        g = PrimGraph.from_adjacency_list(graph)
    else:
        g = PrimGraph.from_edge_list(graph)
    return g.minimum_spanning_tree(algorithm=MSTAlgorithm.KRUSKAL)


def boruvka_mst(graph: Union[PrimGraph, Dict, List[Tuple]]) -> MSTResult:
    """
    Convenience function to find MST using Borůvka's algorithm.
    
    Args:
        graph: PrimGraph instance, adjacency list, or edge list
        
    Returns:
        MSTResult with edges and total weight
    """
    if isinstance(graph, PrimGraph):
        return graph.minimum_spanning_tree(algorithm=MSTAlgorithm.BORUVKA)
    elif isinstance(graph, dict):
        g = PrimGraph.from_adjacency_list(graph)
    else:
        g = PrimGraph.from_edge_list(graph)
    return g.minimum_spanning_tree(algorithm=MSTAlgorithm.BORUVKA)


def minimum_spanning_tree(graph: Union[PrimGraph, Dict, List[Tuple]],
                         algorithm: MSTAlgorithm = MSTAlgorithm.PRIM) -> MSTResult:
    """
    Convenience function to find MST.
    
    Args:
        graph: PrimGraph instance, adjacency list, or edge list
        algorithm: Algorithm to use (default: Prim)
        
    Returns:
        MSTResult with edges and total weight
    """
    if isinstance(graph, PrimGraph):
        return graph.minimum_spanning_tree(algorithm=algorithm)
    elif isinstance(graph, dict):
        g = PrimGraph.from_adjacency_list(graph)
    else:
        g = PrimGraph.from_edge_list(graph)
    return g.minimum_spanning_tree(algorithm=algorithm)


def is_connected_graph(graph: PrimGraph) -> bool:
    """Check if the graph is connected."""
    return graph.is_connected()


def get_connected_components(graph: PrimGraph) -> List[Set[Union[int, str, Tuple]]]:
    """Get all connected components of the graph."""
    return graph.get_connected_components()


def compare_algorithms(graph: PrimGraph) -> Dict[str, MSTResult]:
    """
    Compare all MST algorithms on the same graph.
    
    Args:
        graph: PrimGraph instance
        
    Returns:
        Dictionary mapping algorithm names to their results
    """
    return {
        'prim': graph.minimum_spanning_tree(algorithm=MSTAlgorithm.PRIM),
        'kruskal': graph.minimum_spanning_tree(algorithm=MSTAlgorithm.KRUSKAL),
        'boruvka': graph.minimum_spanning_tree(algorithm=MSTAlgorithm.BORUVKA)
    }


if __name__ == "__main__":
    # Quick demo
    print("=== Prim's Algorithm Demo ===\n")
    
    # Create a graph
    g = PrimGraph()
    g.add_edges([
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 5),
        ('C', 'D', 8),
        ('C', 'E', 10),
        ('D', 'E', 2),
        ('D', 'F', 6),
        ('E', 'F', 3),
    ])
    
    print("Graph edges:")
    for node in sorted(g.nodes):
        for edge in g.get_neighbors(node):
            if edge.source < edge.target:  # Avoid printing twice
                print(f"  {edge.source} -- {edge.target} (weight: {edge.weight})")
    
    print(f"\nNodes: {g.node_count}, Edges: {g.edge_count}")
    print(f"Is connected: {g.is_connected()}")
    
    print("\n--- Prim's Algorithm ---")
    mst_prim = g.minimum_spanning_tree(algorithm=MSTAlgorithm.PRIM)
    print(f"Total weight: {mst_prim.total_weight}")
    print(f"Edges: {len(mst_prim.edges)}")
    for edge in mst_prim.edges:
        print(f"  {edge.source} -- {edge.target} (weight: {edge.weight})")
    
    print("\n--- Kruskal's Algorithm ---")
    mst_kruskal = g.minimum_spanning_tree(algorithm=MSTAlgorithm.KRUSKAL)
    print(f"Total weight: {mst_kruskal.total_weight}")
    for edge in mst_kruskal.edges:
        print(f"  {edge.source} -- {edge.target} (weight: {edge.weight})")
    
    print("\n--- Borůvka's Algorithm ---")
    mst_boruvka = g.minimum_spanning_tree(algorithm=MSTAlgorithm.BORUVKA)
    print(f"Total weight: {mst_boruvka.total_weight}")
    for edge in mst_boruvka.edges:
        print(f"  {edge.source} -- {edge.target} (weight: {edge.weight})")
    
    # Test disconnected graph
    print("\n\n=== Disconnected Graph Test ===")
    g2 = PrimGraph()
    g2.add_edges([('A', 'B', 1), ('B', 'C', 2)])  # Component 1
    g2.add_edges([('D', 'E', 3), ('E', 'F', 4)])  # Component 2
    g2.add_node('G')  # Isolated node
    
    print(f"Is connected: {g2.is_connected()}")
    print(f"Components: {len(g2.get_connected_components())}")
    
    forest = g2.minimum_spanning_forest()
    print(f"\nMinimum Spanning Forest:")
    print(f"Total components: {forest.component_count}")
    print(f"Total weight: {forest.total_weight}")
    for i, tree in enumerate(forest.trees, 1):
        print(f"  Tree {i}: {tree.node_count} nodes, weight {tree.total_weight}")
        for edge in tree.edges:
            print(f"    {edge.source} -- {edge.target}")