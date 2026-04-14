#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Disjoint Set (Union-Find) Utilities Module
========================================================
A comprehensive disjoint set / union-find data structure module for Python 
with zero external dependencies.

Features:
    - DisjointSet class with path compression and union by rank
    - Efficient find, union, and connected operations
    - Support for any hashable element type
    - Component counting and size tracking
    - Batch operations for performance
    - Kruskal's MST algorithm helper
    - Network connectivity analysis utilities

Time Complexity (amortized):
    - Find: O(α(n)) ≈ O(1), where α is inverse Ackermann function
    - Union: O(α(n)) ≈ O(1)
    - Connected: O(α(n)) ≈ O(1)

Author: AllToolkit Contributors
License: MIT
"""

from typing import Dict, Generic, Hashable, Iterator, List, Optional, Set, Tuple, TypeVar

T = TypeVar('T', bound=Hashable)


class DisjointSet(Generic[T]):
    """
    A disjoint-set (union-find) data structure with path compression 
    and union by rank optimization.
    
    This data structure keeps track of elements partitioned into disjoint 
    (non-overlapping) subsets. It provides near-constant-time operations 
    for adding new sets, merging sets, and finding set representatives.
    
    Examples:
        >>> ds = DisjointSet[str]()
        >>> ds.make_set("A")
        >>> ds.make_set("B")
        >>> ds.union("A", "B")
        True
        >>> ds.connected("A", "B")
        True
        >>> ds.find("A")
        'A' or 'B' (representative)
    """
    
    def __init__(self) -> None:
        """Initialize an empty disjoint set."""
        self._parent: Dict[T, T] = {}
        self._rank: Dict[T, int] = {}
        self._size: Dict[T, int] = {}
        self._count: int = 0
    
    def __len__(self) -> int:
        """Return the number of elements in the disjoint set."""
        return len(self._parent)
    
    def __contains__(self, element: T) -> bool:
        """Check if an element exists in the disjoint set."""
        return element in self._parent
    
    def __iter__(self) -> Iterator[T]:
        """Iterate over all elements in the disjoint set."""
        return iter(self._parent.keys())
    
    def __repr__(self) -> str:
        """Return string representation of the disjoint set."""
        components = self.get_components()
        return f"DisjointSet({components})"
    
    def __str__(self) -> str:
        """Return human-readable string representation."""
        components = self.get_components()
        parts = [f"{{{', '.join(map(str, sorted(c))) if all(isinstance(x, (str, int)) for x in c) else ', '.join(map(str, c))}}}" 
                 for c in components]
        return f"DisjointSet({', '.join(parts)})"
    
    # ========================================================================
    # Core Operations
    # ========================================================================
    
    def make_set(self, element: T) -> bool:
        """
        Create a new set containing only the given element.
        
        Args:
            element: The element to add as a new singleton set.
            
        Returns:
            True if element was added, False if it already existed.
            
        Examples:
            >>> ds = DisjointSet[int]()
            >>> ds.make_set(1)
            True
            >>> ds.make_set(1)  # Already exists
            False
        """
        if element in self._parent:
            return False
        
        self._parent[element] = element
        self._rank[element] = 0
        self._size[element] = 1
        self._count += 1
        return True
    
    def make_sets(self, *elements: T) -> int:
        """
        Create multiple singleton sets from the given elements.
        
        Args:
            *elements: Elements to add as new singleton sets.
            
        Returns:
            Number of elements actually added.
            
        Examples:
            >>> ds = DisjointSet[int]()
            >>> ds.make_sets(1, 2, 3, 4)
            4
        """
        added = 0
        for element in elements:
            if self.make_set(element):
                added += 1
        return added
    
    def find(self, element: T) -> Optional[T]:
        """
        Find the representative (root) of the set containing the element.
        
        Uses path compression to flatten the tree structure, making future
        queries faster.
        
        Args:
            element: The element to find the representative for.
            
        Returns:
            The representative element, or None if element doesn't exist.
            
        Examples:
            >>> ds = DisjointSet[int]()
            >>> ds.make_sets(1, 2)
            >>> ds.union(1, 2)
            True
            >>> ds.find(1) == ds.find(2)
            True
        """
        if element not in self._parent:
            return None
        
        # Path compression: make every node point directly to root
        if self._parent[element] != element:
            self._parent[element] = self.find(self._parent[element])
        return self._parent[element]
    
    def find_path(self, element: T) -> Optional[List[T]]:
        """
        Find the path from element to its representative.
        
        Useful for debugging or visualization.
        
        Args:
            element: The element to find the path for.
            
        Returns:
            List of elements from given element to root, or None if not found.
        """
        if element not in self._parent:
            return None
        
        path = [element]
        current = element
        while self._parent[current] != current:
            current = self._parent[current]
            path.append(current)
        return path
    
    def union(self, element1: T, element2: T) -> bool:
        """
        Merge the sets containing element1 and element2.
        
        Uses union by rank to keep trees shallow.
        
        Args:
            element1: First element.
            element2: Second element.
            
        Returns:
            True if sets were merged, False if already in same set or 
            one/both elements don't exist.
            
        Examples:
            >>> ds = DisjointSet[int]()
            >>> ds.make_sets(1, 2, 3)
            3
            >>> ds.union(1, 2)
            True
            >>> ds.union(1, 2)  # Already connected
            False
        """
        root1 = self.find(element1)
        root2 = self.find(element2)
        
        if root1 is None or root2 is None:
            return False
        
        if root1 == root2:
            return False  # Already in same set
        
        # Union by rank: attach smaller tree under larger tree
        if self._rank[root1] < self._rank[root2]:
            root1, root2 = root2, root1
        
        self._parent[root2] = root1
        self._size[root1] += self._size[root2]
        
        if self._rank[root1] == self._rank[root2]:
            self._rank[root1] += 1
        
        self._count -= 1
        return True
    
    def union_all(self, *elements: T) -> int:
        """
        Union all given elements into a single set.
        
        Args:
            *elements: Elements to union together.
            
        Returns:
            Number of successful unions performed.
            
        Examples:
            >>> ds = DisjointSet[int]()
            >>> ds.make_sets(1, 2, 3, 4)
            4
            >>> ds.union_all(1, 2, 3, 4)
            3
        """
        if len(elements) < 2:
            return 0
        
        unions = 0
        first = elements[0]
        for element in elements[1:]:
            if self.union(first, element):
                unions += 1
        return unions
    
    def connected(self, element1: T, element2: T) -> bool:
        """
        Check if two elements are in the same set.
        
        Args:
            element1: First element.
            element2: Second element.
            
        Returns:
            True if both elements exist and are in the same set.
            
        Examples:
            >>> ds = DisjointSet[int]()
            >>> ds.make_sets(1, 2)
            2
            >>> ds.connected(1, 2)
            False
            >>> ds.union(1, 2)
            True
            >>> ds.connected(1, 2)
            True
        """
        root1 = self.find(element1)
        root2 = self.find(element2)
        return root1 is not None and root1 == root2
    
    # ========================================================================
    # Query Operations
    # ========================================================================
    
    def component_count(self) -> int:
        """
        Get the number of disjoint sets (components).
        
        Returns:
            Number of disjoint sets.
        """
        return self._count
    
    def component_size(self, element: T) -> int:
        """
        Get the size of the component containing the element.
        
        Args:
            element: The element to check.
            
        Returns:
            Size of the component, or 0 if element doesn't exist.
        """
        root = self.find(element)
        if root is None:
            return 0
        return self._size[root]
    
    def get_component(self, element: T) -> Set[T]:
        """
        Get all elements in the same component as the given element.
        
        Args:
            element: The element to get the component for.
            
        Returns:
            Set of all elements in the component, or empty set if not found.
        """
        if element not in self._parent:
            return set()
        
        root = self.find(element)
        return {e for e in self._parent if self.find(e) == root}
    
    def get_components(self) -> List[Set[T]]:
        """
        Get all disjoint sets (components).
        
        Returns:
            List of sets, each containing elements of one component.
        """
        components: Dict[T, Set[T]] = {}
        for element in self._parent:
            root = self.find(element)
            if root not in components:
                components[root] = set()
            components[root].add(element)
        return list(components.values())
    
    def get_representatives(self) -> Set[T]:
        """
        Get all representative elements (roots of each component).
        
        Returns:
            Set of representative elements.
        """
        return {self.find(e) for e in self._parent if self.find(e) is not None}
    
    def get_rank(self, element: T) -> int:
        """
        Get the rank of an element.
        
        Args:
            element: The element to check.
            
        Returns:
            Rank of the element, or -1 if not found.
        """
        root = self.find(element)
        if root is None:
            return -1
        return self._rank[root]
    
    # ========================================================================
    # Bulk Operations
    # ========================================================================
    
    def add_connections(self, connections: List[Tuple[T, T]]) -> int:
        """
        Add multiple connections (unions) at once.
        
        Elements are automatically created if they don't exist.
        
        Args:
            connections: List of (element1, element2) tuples to union.
            
        Returns:
            Number of successful unions.
            
        Examples:
            >>> ds = DisjointSet[int]()
            >>> ds.add_connections([(1, 2), (2, 3), (4, 5)])
            3
        """
        # First, add all elements
        elements = set()
        for e1, e2 in connections:
            elements.add(e1)
            elements.add(e2)
        for e in elements:
            self.make_set(e)
        
        # Then perform unions
        unions = 0
        for e1, e2 in connections:
            if self.union(e1, e2):
                unions += 1
        return unions
    
    def from_edges(self, edges: List[Tuple[T, T]]) -> 'DisjointSet[T]':
        """
        Create a disjoint set from a list of edges.
        
        Args:
            edges: List of (node1, node2) tuples representing connections.
            
        Returns:
            Self for method chaining.
            
        Examples:
            >>> ds = DisjointSet[int]().from_edges([(1, 2), (2, 3), (4, 5)])
            >>> ds.component_count()
            2
        """
        for e1, e2 in edges:
            self.make_set(e1)
            self.make_set(e2)
            self.union(e1, e2)
        return self
    
    def reset(self) -> None:
        """Reset the disjoint set to empty state."""
        self._parent.clear()
        self._rank.clear()
        self._size.clear()
        self._count = 0
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    def copy(self) -> 'DisjointSet[T]':
        """
        Create a shallow copy of this disjoint set.
        
        Returns:
            A new DisjointSet with the same structure.
        """
        new_ds = DisjointSet[T]()
        new_ds._parent = self._parent.copy()
        new_ds._rank = self._rank.copy()
        new_ds._size = self._size.copy()
        new_ds._count = self._count
        return new_ds
    
    def to_dict(self) -> Dict[str, any]:
        """
        Export the disjoint set state as a dictionary.
        
        Useful for serialization or debugging.
        
        Returns:
            Dictionary with parent, rank, size, and count info.
        """
        return {
            'parent': dict(self._parent),
            'rank': dict(self._rank),
            'size': dict(self._size),
            'count': self._count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'DisjointSet':
        """
        Create a disjoint set from a dictionary (inverse of to_dict).
        
        Args:
            data: Dictionary with parent, rank, size, and count.
            
        Returns:
            A new DisjointSet instance.
        """
        ds = cls()
        ds._parent = data['parent'].copy()
        ds._rank = data['rank'].copy()
        ds._size = data['size'].copy()
        ds._count = data['count']
        return ds


# ============================================================================
# Graph/Network Utilities using DisjointSet
# ============================================================================

def count_connected_components(nodes: List[T], edges: List[Tuple[T, T]]) -> int:
    """
    Count the number of connected components in an undirected graph.
    
    Args:
        nodes: List of node identifiers.
        edges: List of (node1, node2) tuples representing edges.
        
    Returns:
        Number of connected components.
        
    Examples:
        >>> nodes = [1, 2, 3, 4, 5]
        >>> edges = [(1, 2), (2, 3), (4, 5)]
        >>> count_connected_components(nodes, edges)
        2
    """
    ds = DisjointSet[T]()
    for node in nodes:
        ds.make_set(node)
    for n1, n2 in edges:
        ds.union(n1, n2)
    return ds.component_count()


def find_connected_groups(elements: List[T], 
                          connections: List[Tuple[T, T]]) -> List[Set[T]]:
    """
    Find all connected groups given a list of connections.
    
    Args:
        elements: List of element identifiers.
        connections: List of (elem1, elem2) tuples representing connections.
        
    Returns:
        List of sets, each containing a connected group.
        
    Examples:
        >>> elements = ['A', 'B', 'C', 'D', 'E']
        >>> connections = [('A', 'B'), ('B', 'C'), ('D', 'E')]
        >>> find_connected_groups(elements, connections)
        [{'A', 'B', 'C'}, {'D', 'E'}]
    """
    ds = DisjointSet[T]()
    for elem in elements:
        ds.make_set(elem)
    for e1, e2 in connections:
        ds.union(e1, e2)
    return ds.get_components()


def is_connected_graph(nodes: List[T], edges: List[Tuple[T, T]]) -> bool:
    """
    Check if an undirected graph is connected (single component).
    
    Args:
        nodes: List of node identifiers.
        edges: List of (node1, node2) tuples.
        
    Returns:
        True if the graph has exactly one connected component.
        
    Examples:
        >>> is_connected_graph([1, 2, 3], [(1, 2), (2, 3)])
        True
        >>> is_connected_graph([1, 2, 3, 4], [(1, 2), (3, 4)])
        False
    """
    if not nodes:
        return True
    return count_connected_components(nodes, edges) == 1


def detect_cycle_undirected(nodes: List[T], edges: List[Tuple[T, T]]) -> bool:
    """
    Detect if an undirected graph has a cycle using union-find.
    
    For each edge, if the two endpoints are already in the same set,
    adding this edge would create a cycle.
    
    Args:
        nodes: List of node identifiers.
        edges: List of (node1, node2) tuples.
        
    Returns:
        True if a cycle exists.
        
    Examples:
        >>> detect_cycle_undirected([1, 2, 3], [(1, 2), (2, 3), (3, 1)])
        True
        >>> detect_cycle_undirected([1, 2, 3], [(1, 2), (2, 3)])
        False
    """
    ds = DisjointSet[T]()
    for node in nodes:
        ds.make_set(node)
    
    for n1, n2 in edges:
        if ds.connected(n1, n2):
            return True  # Adding this edge creates a cycle
        ds.union(n1, n2)
    
    return False


# ============================================================================
# Kruskal's MST Helper
# ============================================================================

Edge = Tuple[T, T, float]  # (node1, node2, weight)


def kruskal_mst(nodes: List[T], edges: List[Edge]) -> Tuple[List[Edge], float]:
    """
    Find the Minimum Spanning Tree using Kruskal's algorithm.
    
    Args:
        nodes: List of node identifiers.
        edges: List of (node1, node2, weight) tuples.
        
    Returns:
        Tuple of (mst_edges, total_weight).
        Returns ([], 0.0) if graph is disconnected.
        
    Examples:
        >>> nodes = ['A', 'B', 'C', 'D']
        >>> edges = [('A', 'B', 1), ('B', 'C', 2), ('C', 'D', 3), ('A', 'D', 4)]
        >>> mst, weight = kruskal_mst(nodes, edges)
        >>> len(mst)
        3
        >>> weight
        6.0
    """
    ds = DisjointSet[T]()
    for node in nodes:
        ds.make_set(node)
    
    # Sort edges by weight
    sorted_edges = sorted(edges, key=lambda e: e[2])
    
    mst_edges: List[Edge] = []
    total_weight = 0.0
    
    for n1, n2, weight in sorted_edges:
        if not ds.connected(n1, n2):
            ds.union(n1, n2)
            mst_edges.append((n1, n2, weight))
            total_weight += weight
            
            if len(mst_edges) == len(nodes) - 1:
                break
    
    # Check if we have a valid MST (all nodes connected)
    if len(mst_edges) != len(nodes) - 1:
        return ([], 0.0)
    
    return (mst_edges, total_weight)


# ============================================================================
# Social Network Analysis Utilities
# ============================================================================

def find_friend_circles(users: List[T], 
                        friendships: List[Tuple[T, T]]) -> Dict[T, int]:
    """
    Find friend circles (connected components) in a social network.
    
    Returns a mapping from each user to their circle ID (representative).
    
    Args:
        users: List of user identifiers.
        friendships: List of (user1, user2) tuples.
        
    Returns:
        Dictionary mapping each user to their circle representative.
        
    Examples:
        >>> users = ['Alice', 'Bob', 'Carol', 'Dave']
        >>> friendships = [('Alice', 'Bob'), ('Bob', 'Carol')]
        >>> circles = find_friend_circles(users, friendships)
        >>> circles['Alice'] == circles['Bob'] == circles['Carol']
        True
        >>> circles['Dave'] != circles['Alice']
        True
    """
    ds = DisjointSet[T]()
    for user in users:
        ds.make_set(user)
    for u1, u2 in friendships:
        ds.union(u1, u2)
    
    return {user: ds.find(user) for user in users if ds.find(user) is not None}


def get_circle_sizes(users: List[T], 
                    friendships: List[Tuple[T, T]]) -> Dict[T, int]:
    """
    Get the size of each user's friend circle.
    
    Args:
        users: List of user identifiers.
        friendships: List of (user1, user2) tuples.
        
    Returns:
        Dictionary mapping each user to their circle size.
        
    Examples:
        >>> users = ['A', 'B', 'C', 'D']
        >>> friendships = [('A', 'B'), ('B', 'C')]
        >>> get_circle_sizes(users, friendships)
        {'A': 3, 'B': 3, 'C': 3, 'D': 1}
    """
    ds = DisjointSet[T]()
    for user in users:
        ds.make_set(user)
    for u1, u2 in friendships:
        ds.union(u1, u2)
    
    return {user: ds.component_size(user) for user in users}


# ============================================================================
# Image Processing Utilities (Connected Components)
# ============================================================================

def find_connected_pixels(grid: List[List[int]], 
                          connectivity: int = 4) -> List[List[int]]:
    """
    Label connected components in a binary image (grid of 0s and 1s).
    
    Uses union-find for efficient connected component labeling.
    
    Args:
        grid: 2D list where 1 = foreground, 0 = background.
        connectivity: 4 for 4-connected, 8 for 8-connected (including diagonals).
        
    Returns:
        2D list with each connected component labeled with a unique integer.
        
    Examples:
        >>> grid = [[1, 1, 0], [1, 0, 0], [0, 0, 1]]
        >>> result = find_connected_pixels(grid)
        >>> # First component labeled 1, second labeled 2
    """
    if not grid or not grid[0]:
        return []
    
    rows, cols = len(grid), len(grid[0])
    ds = DisjointSet[int]()
    
    # First pass: assign provisional labels and record equivalences
    labels = [[0] * cols for _ in range(rows)]
    current_label = 0
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                continue
            
            neighbors = []
            if r > 0 and labels[r-1][c] > 0:
                neighbors.append(labels[r-1][c])
            if c > 0 and labels[r][c-1] > 0:
                neighbors.append(labels[r][c-1])
            if connectivity == 8:
                if r > 0 and c > 0 and labels[r-1][c-1] > 0:
                    neighbors.append(labels[r-1][c-1])
                if r > 0 and c < cols-1 and labels[r-1][c+1] > 0:
                    neighbors.append(labels[r-1][c+1])
            
            if not neighbors:
                current_label += 1
                labels[r][c] = current_label
                ds.make_set(current_label)
            else:
                min_label = min(neighbors)
                labels[r][c] = min_label
                for lbl in neighbors:
                    ds.union(min_label, lbl)
    
    # Second pass: assign final labels
    label_map = {}
    final_label = 0
    for r in range(rows):
        for c in range(cols):
            if labels[r][c] > 0:
                root = ds.find(labels[r][c])
                if root not in label_map:
                    final_label += 1
                    label_map[root] = final_label
                labels[r][c] = label_map[root]
    
    return labels


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    # Basic usage demonstration
    print("=== DisjointSet Demo ===\n")
    
    # Create and populate
    ds = DisjointSet[int]()
    ds.make_sets(1, 2, 3, 4, 5, 6, 7, 8)
    print(f"Initial state: {ds}")
    print(f"Component count: {ds.component_count()}")
    
    # Union operations
    ds.union(1, 2)
    ds.union(2, 3)
    ds.union(4, 5)
    ds.union_all(6, 7, 8)
    print(f"\nAfter unions: {ds}")
    print(f"Component count: {ds.component_count()}")
    
    # Query operations
    print(f"\n1 and 3 connected: {ds.connected(1, 3)}")
    print(f"1 and 4 connected: {ds.connected(1, 4)}")
    print(f"Component containing 1: {ds.get_component(1)}")
    print(f"Size of component with 1: {ds.component_size(1)}")
    
    # MST example
    print("\n=== Kruskal MST ===")
    nodes = ['A', 'B', 'C', 'D']
    edges = [('A', 'B', 1), ('B', 'C', 2), ('C', 'D', 3), ('A', 'D', 4), ('B', 'D', 5)]
    mst, weight = kruskal_mst(nodes, edges)
    print(f"MST edges: {mst}")
    print(f"Total weight: {weight}")
    
    # Cycle detection
    print("\n=== Cycle Detection ===")
    print(f"Has cycle (triangle): {detect_cycle_undirected([1,2,3], [(1,2), (2,3), (3,1)])}")
    print(f"Has cycle (line): {detect_cycle_undirected([1,2,3], [(1,2), (2,3)])}")
    
    # Connected components in image
    print("\n=== Image Connected Components ===")
    grid = [
        [1, 1, 0, 0, 1],
        [1, 0, 0, 1, 1],
        [0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0]
    ]
    labeled = find_connected_pixels(grid)
    for row in labeled:
        print(row)