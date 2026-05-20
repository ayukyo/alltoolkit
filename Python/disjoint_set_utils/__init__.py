"""
Disjoint Set Union (Union-Find) Utils

A comprehensive implementation of the Disjoint Set Union (DSU) data structure,
also known as Union-Find. This data structure efficiently manages a partition
of a set into disjoint subsets and supports two primary operations:
- Find: Determine which subset a particular element is in
- Union: Join two subsets into a single subset

Features:
- Path compression for O(α(n)) amortized find operations
- Union by rank for balanced tree structure
- Support for both integer and generic element types
- Connected components detection
- Cycle detection in graphs
- Kruskal's MST algorithm support

Author: AllToolkit
Date: 2026-05-20
"""

from .disjoint_set import DisjointSet, WeightedDisjointSet, DisjointSetWithUndo
from .disjoint_set import (
    count_connected_components,
    detect_cycle_undirected,
    kruskal_mst,
    find_redundant_connection
)

__all__ = [
    'DisjointSet',
    'WeightedDisjointSet', 
    'DisjointSetWithUndo',
    'count_connected_components',
    'detect_cycle_undirected',
    'kruskal_mst',
    'find_redundant_connection'
]

__version__ = '1.0.0'