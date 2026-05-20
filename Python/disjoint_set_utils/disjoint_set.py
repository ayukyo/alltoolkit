"""
Disjoint Set Union Implementation

Core implementation of Union-Find data structure with optimizations.
"""

from typing import Dict, List, Optional, Tuple, Generic, TypeVar, Set, Any
from abc import ABC, abstractmethod

T = TypeVar('T')


class DisjointSet(Generic[T]):
    """
    A Disjoint Set Union (Union-Find) data structure with path compression
    and union by rank optimizations.
    
    Time Complexity:
    - Find: O(α(n)) amortized, where α is the inverse Ackermann function
    - Union: O(α(n)) amortized
    - Space: O(n)
    
    Example:
        >>> ds = DisjointSet[int]()
        >>> ds.make_set(1)
        >>> ds.make_set(2)
        >>> ds.union(1, 2)
        >>> ds.connected(1, 2)
        True
        >>> ds.find(1) == ds.find(2)
        True
    """
    
    def __init__(self) -> None:
        """Initialize an empty disjoint set."""
        self._parent: Dict[T, T] = {}
        self._rank: Dict[T, int] = {}
        self._size: Dict[T, int] = {}  # Size of each component
        self._count: int = 0  # Number of disjoint sets
    
    def make_set(self, x: T) -> None:
        """
        Create a new set containing only element x.
        
        Args:
            x: The element to create a set for
            
        Raises:
            ValueError: If element already exists
        """
        if x in self._parent:
            raise ValueError(f"Element {x} already exists in the set")
        
        self._parent[x] = x
        self._rank[x] = 0
        self._size[x] = 1
        self._count += 1
    
    def make_sets(self, elements: List[T]) -> None:
        """
        Create multiple singleton sets.
        
        Args:
            elements: List of elements to create sets for
        """
        for x in elements:
            if x not in self._parent:
                self.make_set(x)
    
    def find(self, x: T) -> T:
        """
        Find the representative (root) of the set containing x.
        Uses path compression for optimization.
        
        Args:
            x: The element to find
            
        Returns:
            The representative element of the set containing x
            
        Raises:
            KeyError: If element x is not in any set
        """
        if x not in self._parent:
            raise KeyError(f"Element {x} not found in any set")
        
        # Path compression: make every node point directly to root
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        
        return self._parent[x]
    
    def find_iterative(self, x: T) -> T:
        """
        Iterative version of find with two-pass path compression.
        
        Args:
            x: The element to find
            
        Returns:
            The representative element of the set containing x
        """
        if x not in self._parent:
            raise KeyError(f"Element {x} not found in any set")
        
        # Find root
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        
        # Path compression: point all nodes to root
        current = x
        while self._parent[current] != root:
            next_node = self._parent[current]
            self._parent[current] = root
            current = next_node
        
        return root
    
    def union(self, x: T, y: T) -> bool:
        """
        Unite the sets containing elements x and y.
        Uses union by rank for optimization.
        
        Args:
            x: First element
            y: Second element
            
        Returns:
            True if sets were united (were different), False if already in same set
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in the same set
        
        # Union by rank: attach smaller tree under root of larger tree
        if self._rank[root_x] < self._rank[root_y]:
            root_x, root_y = root_y, root_x
        
        self._parent[root_y] = root_x
        self._size[root_x] += self._size[root_y]
        
        # Increment rank if trees were same height
        if self._rank[root_x] == self._rank[root_y]:
            self._rank[root_x] += 1
        
        self._count -= 1
        return True
    
    def union_by_size(self, x: T, y: T) -> bool:
        """
        Unite sets using union by size strategy.
        
        Args:
            x: First element
            y: Second element
            
        Returns:
            True if sets were united, False if already in same set
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        # Attach smaller tree under larger tree
        if self._size[root_x] < self._size[root_y]:
            root_x, root_y = root_y, root_x
        
        self._parent[root_y] = root_x
        self._size[root_x] += self._size[root_y]
        self._count -= 1
        
        return True
    
    def connected(self, x: T, y: T) -> bool:
        """
        Check if elements x and y are in the same set.
        
        Args:
            x: First element
            y: Second element
            
        Returns:
            True if in the same set, False otherwise
        """
        return self.find(x) == self.find(y)
    
    def get_size(self, x: T) -> int:
        """
        Get the size of the set containing element x.
        
        Args:
            x: The element
            
        Returns:
            Size of the component containing x
        """
        root = self.find(x)
        return self._size[root]
    
    def count_sets(self) -> int:
        """
        Get the number of disjoint sets.
        
        Returns:
            Number of disjoint sets
        """
        return self._count
    
    def get_sets(self) -> Dict[T, Set[T]]:
        """
        Get all disjoint sets as a dictionary mapping roots to their members.
        
        Returns:
            Dictionary mapping root elements to sets of members
        """
        sets: Dict[T, Set[T]] = {}
        for x in self._parent:
            root = self.find(x)
            if root not in sets:
                sets[root] = set()
            sets[root].add(x)
        return sets
    
    def get_members(self, x: T) -> Set[T]:
        """
        Get all members of the set containing element x.
        
        Args:
            x: The element
            
        Returns:
            Set of all elements in the same component as x
        """
        root = self.find(x)
        return {y for y in self._parent if self.find(y) == root}
    
    def __len__(self) -> int:
        """Return total number of elements in all sets."""
        return len(self._parent)
    
    def __contains__(self, x: T) -> bool:
        """Check if element x is in any set."""
        return x in self._parent
    
    def __repr__(self) -> str:
        return f"DisjointSet(sets={self._count}, elements={len(self._parent)})"


class WeightedDisjointSet(Generic[T]):
    """
    A Disjoint Set with support for weighted edges.
    Useful for problems involving relationships between elements.
    
    Example:
        >>> wds = WeightedDisjointSet[str]()
        >>> wds.make_set("a")
        >>> wds.make_set("b")
        >>> wds.union_weighted("a", "b", 5)
        >>> wds.same_component("a", "b")
        True
    """
    
    def __init__(self) -> None:
        """Initialize an empty weighted disjoint set."""
        self._parent: Dict[T, T] = {}
        self._weight: Dict[T, Dict[T, float]] = {}  # Edge weights
        self._rank: Dict[T, int] = {}
        self._component_weight: Dict[T, float] = {}  # Total weight per component
        self._count: int = 0
    
    def make_set(self, x: T) -> None:
        """Create a new singleton set."""
        if x in self._parent:
            raise ValueError(f"Element {x} already exists")
        
        self._parent[x] = x
        self._weight[x] = {}
        self._rank[x] = 0
        self._component_weight[x] = 0.0
        self._count += 1
    
    def make_sets(self, elements: List[T]) -> None:
        """
        Create multiple singleton sets.
        
        Args:
            elements: List of elements to create sets for
        """
        for x in elements:
            if x not in self._parent:
                self.make_set(x)
    
    def find(self, x: T) -> T:
        """Find the root of x with path compression."""
        if x not in self._parent:
            raise KeyError(f"Element {x} not found")
        
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        
        return self._parent[x]
    
    def union_weighted(self, x: T, y: T, weight: float = 1.0) -> bool:
        """
        Unite sets with an associated weight.
        
        Args:
            x: First element
            y: Second element
            weight: Weight of the connection
            
        Returns:
            True if united, False if already connected
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        if self._rank[root_x] < self._rank[root_y]:
            root_x, root_y = root_y, root_x
        
        self._parent[root_y] = root_x
        self._component_weight[root_x] += self._component_weight[root_y] + weight
        
        if self._rank[root_x] == self._rank[root_y]:
            self._rank[root_x] += 1
        
        self._count -= 1
        return True
    
    def get_component_weight(self, x: T) -> float:
        """Get total weight of the component containing x."""
        root = self.find(x)
        return self._component_weight[root]
    
    def same_component(self, x: T, y: T) -> bool:
        """Check if x and y are in the same component."""
        return self.find(x) == self.find(y)
    
    def count_sets(self) -> int:
        """Get the number of disjoint sets."""
        return self._count


class DisjointSetWithUndo(Generic[T]):
    """
    A Disjoint Set that supports undo operations.
    Uses persistent data structure techniques.
    
    Useful for backtracking algorithms and offline dynamic connectivity.
    """
    
    def __init__(self) -> None:
        """Initialize an empty undoable disjoint set."""
        self._parent: Dict[T, T] = {}
        self._rank: Dict[T, int] = {}
        self._size: Dict[T, int] = {}
        self._count: int = 0
        self._history: List[Tuple[str, T, T, int, int, int]] = []  # (op, a, b, rank_a, size_a, count)
    
    def make_set(self, x: T) -> None:
        """Create a new singleton set."""
        if x in self._parent:
            raise ValueError(f"Element {x} already exists")
        
        self._parent[x] = x
        self._rank[x] = 0
        self._size[x] = 1
        self._count += 1
        self._history.append(('make', x, x, 0, 1, self._count))
    
    def make_sets(self, elements: List[T]) -> None:
        """
        Create multiple singleton sets.
        
        Args:
            elements: List of elements to create sets for
        """
        for x in elements:
            if x not in self._parent:
                self.make_set(x)
    
    def find(self, x: T) -> T:
        """Find root without path compression (to support undo)."""
        if x not in self._parent:
            raise KeyError(f"Element {x} not found")
        
        while self._parent[x] != x:
            x = self._parent[x]
        
        return x
    
    def union(self, x: T, y: T) -> bool:
        """
        Unite sets containing x and y.
        Records operation for potential undo.
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            self._history.append(('union_skip', x, y, 0, 0, self._count))
            return False
        
        # Record state before change
        old_rank_x = self._rank[root_x]
        old_size_x = self._size[root_x]
        old_count = self._count
        
        if self._rank[root_x] < self._rank[root_y]:
            root_x, root_y = root_y, root_x
        
        self._parent[root_y] = root_x
        self._size[root_x] += self._size[root_y]
        
        if self._rank[root_x] == self._rank[root_y]:
            self._rank[root_x] += 1
        
        self._count -= 1
        
        self._history.append(('union', root_y, root_x, old_rank_x, old_size_x, old_count))
        return True
    
    def undo(self) -> bool:
        """
        Undo the last operation.
        
        Returns:
            True if an operation was undone, False if no history
        """
        if not self._history:
            return False
        
        op, a, b, rank_a, size_a, count = self._history.pop()
        
        if op == 'make':
            del self._parent[a]
            del self._rank[a]
            del self._size[a]
            self._count = count
        elif op == 'union':
            # Restore parent, rank, and size
            self._parent[a] = a  # a was root_y, restore it as its own parent
            self._rank[b] = rank_a  # b was root_x
            self._size[b] = size_a
            self._count = count
        
        return True
    
    def connected(self, x: T, y: T) -> bool:
        """Check if x and y are in the same set."""
        return self.find(x) == self.find(y)
    
    def count_sets(self) -> int:
        """Get the number of disjoint sets."""
        return self._count
    
    def history_size(self) -> int:
        """Get the number of operations in history."""
        return len(self._history)


# ==================== Algorithm Helpers ====================

def count_connected_components(n: int, edges: List[Tuple[int, int]]) -> int:
    """
    Count the number of connected components in an undirected graph.
    
    Args:
        n: Number of vertices (0 to n-1)
        edges: List of edges as (u, v) tuples
        
    Returns:
        Number of connected components
        
    Example:
        >>> count_connected_components(5, [(0, 1), (1, 2), (3, 4)])
        2
    """
    ds = DisjointSet[int]()
    ds.make_sets(list(range(n)))
    
    for u, v in edges:
        ds.union(u, v)
    
    return ds.count_sets()


def detect_cycle_undirected(n: int, edges: List[Tuple[int, int]]) -> bool:
    """
    Detect if an undirected graph has a cycle.
    
    Args:
        n: Number of vertices (0 to n-1)
        edges: List of edges as (u, v) tuples
        
    Returns:
        True if cycle exists, False otherwise
        
    Example:
        >>> detect_cycle_undirected(3, [(0, 1), (1, 2), (2, 0)])
        True
        >>> detect_cycle_undirected(3, [(0, 1), (1, 2)])
        False
    """
    ds = DisjointSet[int]()
    ds.make_sets(list(range(n)))
    
    for u, v in edges:
        if ds.connected(u, v):
            return True  # Edge connects already connected vertices = cycle
        ds.union(u, v)
    
    return False


def kruskal_mst(n: int, edges: List[Tuple[int, int, float]]) -> Tuple[List[Tuple[int, int, float]], float]:
    """
    Find Minimum Spanning Tree using Kruskal's algorithm.
    
    Args:
        n: Number of vertices (0 to n-1)
        edges: List of edges as (u, v, weight) tuples
        
    Returns:
        Tuple of (MST edges, total weight)
        
    Example:
        >>> mst, weight = kruskal_mst(4, [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)])
        >>> weight
        6
    """
    # Sort edges by weight
    sorted_edges = sorted(edges, key=lambda e: e[2])
    
    ds = DisjointSet[int]()
    ds.make_sets(list(range(n)))
    
    mst_edges: List[Tuple[int, int, float]] = []
    total_weight = 0.0
    
    for u, v, w in sorted_edges:
        if ds.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            
            if len(mst_edges) == n - 1:
                break  # MST complete
    
    return mst_edges, total_weight


def find_redundant_connection(n: int, edges: List[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    """
    Find a redundant connection in a graph that would create a cycle.
    Returns the last edge that creates a cycle when added.
    
    Args:
        n: Number of vertices (1 to n)
        edges: List of edges as (u, v) tuples
        
    Returns:
        The redundant edge, or None if no redundancy
        
    Example:
        >>> find_redundant_connection(3, [(1, 2), (1, 3), (2, 3)])
        (2, 3)
    """
    ds = DisjointSet[int]()
    ds.make_sets(list(range(1, n + 1)))
    
    for u, v in edges:
        if ds.connected(u, v):
            return (u, v)
        ds.union(u, v)
    
    return None