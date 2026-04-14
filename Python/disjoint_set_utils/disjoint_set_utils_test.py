#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Disjoint Set Utilities Test Suite
===============================================
Comprehensive tests for the DisjointSet module.

Run with: python -m pytest disjoint_set_utils_test.py -v
Or: python disjoint_set_utils_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from disjoint_set_utils.mod import (
    DisjointSet,
    count_connected_components,
    find_connected_groups,
    is_connected_graph,
    detect_cycle_undirected,
    kruskal_mst,
    find_friend_circles,
    get_circle_sizes,
    find_connected_pixels
)


class TestDisjointSetBasic:
    """Test basic DisjointSet operations."""
    
    def test_init(self):
        """Test initialization."""
        ds = DisjointSet[int]()
        assert len(ds) == 0
        assert ds.component_count() == 0
    
    def test_make_set(self):
        """Test make_set operation."""
        ds = DisjointSet[int]()
        assert ds.make_set(1) == True
        assert ds.make_set(1) == False  # Duplicate
        assert len(ds) == 1
        assert 1 in ds
    
    def test_make_sets(self):
        """Test batch make_set operation."""
        ds = DisjointSet[int]()
        count = ds.make_sets(1, 2, 3, 4)
        assert count == 4
        assert len(ds) == 4
        assert all(i in ds for i in [1, 2, 3, 4])
    
    def test_find(self):
        """Test find operation."""
        ds = DisjointSet[str]()
        ds.make_set("A")
        assert ds.find("A") == "A"
        assert ds.find("B") is None  # Non-existent
    
    def test_union(self):
        """Test union operation."""
        ds = DisjointSet[int]()
        ds.make_sets(1, 2)
        assert ds.union(1, 2) == True
        assert ds.find(1) == ds.find(2)
        assert ds.union(1, 2) == False  # Already connected
        assert ds.component_count() == 1
    
    def test_union_all(self):
        """Test union_all operation."""
        ds = DisjointSet[int]()
        ds.make_sets(1, 2, 3, 4)
        unions = ds.union_all(1, 2, 3, 4)
        assert unions == 3
        assert ds.component_count() == 1
        assert all(ds.connected(1, i) for i in [2, 3, 4])
    
    def test_connected(self):
        """Test connected operation."""
        ds = DisjointSet[int]()
        ds.make_sets(1, 2, 3)
        assert ds.connected(1, 2) == False
        ds.union(1, 2)
        assert ds.connected(1, 2) == True
        assert ds.connected(1, 3) == False


class TestDisjointSetQuery:
    """Test query operations."""
    
    def test_component_count(self):
        """Test component counting."""
        ds = DisjointSet[int]()
        ds.make_sets(1, 2, 3, 4, 5)
        assert ds.component_count() == 5
        ds.union(1, 2)
        assert ds.component_count() == 4
        ds.union(2, 3)
        assert ds.component_count() == 3
        ds.union(4, 5)
        assert ds.component_count() == 2
        ds.union(1, 4)
        assert ds.component_count() == 1
    
    def test_component_size(self):
        """Test component size."""
        ds = DisjointSet[int]()
        ds.make_sets(1, 2, 3, 4)
        ds.union(1, 2)
        ds.union(2, 3)
        assert ds.component_size(1) == 3
        assert ds.component_size(4) == 1
    
    def test_get_component(self):
        """Test getting all elements in a component."""
        ds = DisjointSet[int]()
        ds.make_sets(1, 2, 3, 4, 5)
        ds.union(1, 2)
        ds.union(2, 3)
        assert ds.get_component(1) == {1, 2, 3}
        assert ds.get_component(4) == {4}
        assert ds.get_component(6) == set()  # Non-existent
    
    def test_get_components(self):
        """Test getting all components."""
        ds = DisjointSet[int]()
        ds.make_sets(1, 2, 3, 4, 5)
        ds.union(1, 2)
        ds.union(4, 5)
        components = ds.get_components()
        assert len(components) == 3
        assert {1, 2} in components
        assert {3} in components
        assert {4, 5} in components
    
    def test_get_representatives(self):
        """Test getting all representatives."""
        ds = DisjointSet[int]()
        ds.make_sets(1, 2, 3)
        ds.union(1, 2)
        reps = ds.get_representatives()
        assert len(reps) == 2  # Two components: {1,2} and {3}


class TestDisjointSetBulk:
    """Test bulk operations."""
    
    def test_add_connections(self):
        """Test adding multiple connections."""
        ds = DisjointSet[str]()
        connections = [("A", "B"), ("B", "C"), ("D", "E")]
        unions = ds.add_connections(connections)
        assert unions == 3
        assert ds.component_count() == 2
        assert ds.connected("A", "C")
        assert ds.connected("D", "E")
        assert not ds.connected("A", "D")
    
    def test_from_edges(self):
        """Test creating from edges."""
        ds = DisjointSet[int]().from_edges([(1, 2), (2, 3), (4, 5)])
        assert ds.component_count() == 2
        assert ds.connected(1, 3)
        assert not ds.connected(3, 4)
    
    def test_reset(self):
        """Test reset operation."""
        ds = DisjointSet[int]()
        ds.make_sets(1, 2, 3)
        ds.union(1, 2)
        ds.reset()
        assert len(ds) == 0
        assert ds.component_count() == 0
    
    def test_copy(self):
        """Test copy operation."""
        ds1 = DisjointSet[int]()
        ds1.make_sets(1, 2, 3)
        ds1.union(1, 2)
        ds2 = ds1.copy()
        assert len(ds2) == 3
        assert ds2.connected(1, 2)
        # Modify copy shouldn't affect original
        ds2.union(2, 3)
        assert ds2.connected(1, 3)
        assert not ds1.connected(1, 3)


class TestDisjointSetSerialization:
    """Test serialization operations."""
    
    def test_to_dict_and_from_dict(self):
        """Test dictionary serialization."""
        ds1 = DisjointSet[str]()
        ds1.make_sets("A", "B", "C")
        ds1.union("A", "B")
        
        data = ds1.to_dict()
        ds2 = DisjointSet.from_dict(data)
        
        assert len(ds2) == 3
        assert ds2.connected("A", "B")
        assert not ds2.connected("A", "C")


class TestDisjointSetTypes:
    """Test with different types."""
    
    def test_string_elements(self):
        """Test with string elements."""
        ds = DisjointSet[str]()
        ds.make_sets("apple", "banana", "cherry")
        ds.union("apple", "banana")
        assert ds.connected("apple", "banana")
    
    def test_tuple_elements(self):
        """Test with tuple elements."""
        ds = DisjointSet[tuple]()
        ds.make_sets((0, 0), (0, 1), (1, 0))
        ds.union((0, 0), (0, 1))
        assert ds.connected((0, 0), (0, 1))


class TestGraphUtilities:
    """Test graph utility functions."""
    
    def test_count_connected_components(self):
        """Test counting connected components."""
        nodes = [1, 2, 3, 4, 5]
        edges = [(1, 2), (2, 3), (4, 5)]
        assert count_connected_components(nodes, edges) == 2
        
        # Single component
        edges2 = [(1, 2), (2, 3), (3, 4), (4, 5)]
        assert count_connected_components(nodes, edges2) == 1
        
        # No edges
        assert count_connected_components(nodes, []) == 5
    
    def test_find_connected_groups(self):
        """Test finding connected groups."""
        elements = ['A', 'B', 'C', 'D', 'E']
        connections = [('A', 'B'), ('B', 'C'), ('D', 'E')]
        groups = find_connected_groups(elements, connections)
        assert len(groups) == 2
        assert {'A', 'B', 'C'} in groups
        assert {'D', 'E'} in groups
    
    def test_is_connected_graph(self):
        """Test graph connectivity check."""
        # Connected graph
        assert is_connected_graph([1, 2, 3], [(1, 2), (2, 3)]) == True
        # Disconnected graph
        assert is_connected_graph([1, 2, 3, 4], [(1, 2), (3, 4)]) == False
        # Empty graph
        assert is_connected_graph([], []) == True
    
    def test_detect_cycle_undirected(self):
        """Test cycle detection."""
        # Triangle - has cycle
        assert detect_cycle_undirected([1, 2, 3], [(1, 2), (2, 3), (3, 1)]) == True
        # Line - no cycle
        assert detect_cycle_undirected([1, 2, 3], [(1, 2), (2, 3)]) == False
        # Square - has cycle
        assert detect_cycle_undirected([1, 2, 3, 4], 
                                        [(1, 2), (2, 3), (3, 4), (4, 1)]) == True


class TestKruskalMST:
    """Test Kruskal's MST algorithm."""
    
    def test_simple_mst(self):
        """Test simple MST."""
        nodes = ['A', 'B', 'C']
        edges = [('A', 'B', 1), ('B', 'C', 2), ('A', 'C', 3)]
        mst, weight = kruskal_mst(nodes, edges)
        assert len(mst) == 2
        assert weight == 3.0  # 1 + 2
    
    def test_disconnected_graph(self):
        """Test MST on disconnected graph returns empty."""
        nodes = ['A', 'B', 'C', 'D']
        edges = [('A', 'B', 1), ('C', 'D', 2)]
        mst, weight = kruskal_mst(nodes, edges)
        assert mst == []
        assert weight == 0.0
    
    def test_single_node(self):
        """Test MST on single node."""
        mst, weight = kruskal_mst(['A'], [])
        assert mst == []
        assert weight == 0.0


class TestSocialNetwork:
    """Test social network utilities."""
    
    def test_find_friend_circles(self):
        """Test friend circle detection."""
        users = ['Alice', 'Bob', 'Carol', 'Dave', 'Eve']
        friendships = [('Alice', 'Bob'), ('Bob', 'Carol'), ('Dave', 'Eve')]
        circles = find_friend_circles(users, friendships)
        
        # Alice, Bob, Carol should share same circle
        assert circles['Alice'] == circles['Bob'] == circles['Carol']
        # Dave and Eve should share another circle
        assert circles['Dave'] == circles['Eve']
        # The two circles should be different
        assert circles['Alice'] != circles['Dave']
    
    def test_get_circle_sizes(self):
        """Test circle size calculation."""
        users = ['A', 'B', 'C', 'D']
        friendships = [('A', 'B'), ('B', 'C')]
        sizes = get_circle_sizes(users, friendships)
        assert sizes['A'] == 3
        assert sizes['B'] == 3
        assert sizes['C'] == 3
        assert sizes['D'] == 1


class TestImageProcessing:
    """Test image processing utilities."""
    
    def test_connected_pixels_simple(self):
        """Test simple connected component labeling."""
        grid = [
            [1, 1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ]
        labeled = find_connected_pixels(grid)
        
        # First two 1s should have same label
        assert labeled[0][0] == labeled[0][1] == labeled[1][0]
        # Last 1 should have different label
        assert labeled[2][2] != labeled[0][0]
    
    def test_connected_pixels_empty(self):
        """Test empty grid."""
        assert find_connected_pixels([]) == []
        assert find_connected_pixels([[]]) == []
    
    def test_connected_pixels_all_zeros(self):
        """Test grid of all zeros."""
        grid = [[0, 0], [0, 0]]
        labeled = find_connected_pixels(grid)
        assert all(all(cell == 0 for cell in row) for row in labeled)
    
    def test_connected_pixels_8_connectivity(self):
        """Test 8-connectivity."""
        grid = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1]
        ]
        # With 4-connectivity, these are 5 separate components
        labeled_4 = find_connected_pixels(grid, connectivity=4)
        # With 8-connectivity, they're all connected through diagonals
        labeled_8 = find_connected_pixels(grid, connectivity=8)
        
        # Count unique non-zero labels
        labels_4 = set(x for row in labeled_4 for x in row if x > 0)
        labels_8 = set(x for row in labeled_8 for x in row if x > 0)
        
        assert len(labels_4) > len(labels_8)


class TestPathCompression:
    """Test path compression optimization."""
    
    def test_path_compression(self):
        """Test that path compression works correctly."""
        ds = DisjointSet[int]()
        # Create a chain: 1 -> 2 -> 3 -> 4 -> 5
        ds.make_sets(1, 2, 3, 4, 5)
        ds.union(1, 2)
        ds.union(2, 3)
        ds.union(3, 4)
        ds.union(4, 5)
        
        # All should be connected
        assert ds.connected(1, 5)
        
        # After find(5), path should be compressed
        root = ds.find(5)
        path = ds.find_path(5)
        assert path is not None
        assert path[-1] == root
        # Path should be short after compression
        assert len(path) <= 3


class TestUnionByRank:
    """Test union by rank optimization."""
    
    def test_union_by_rank(self):
        """Test that smaller tree is attached under larger tree."""
        ds = DisjointSet[int]()
        # Create two trees of different heights
        ds.make_sets(1, 2, 3, 4, 5, 6)
        ds.union(1, 2)  # Tree 1 has rank 1
        ds.union(3, 4)
        ds.union(3, 5)
        ds.union(3, 6)  # Tree 3 has rank 2
        
        # After union, rank should be at most max(rank1, rank2) + 1
        initial_rank = ds.get_rank(1)
        ds.union(1, 3)
        final_rank = ds.get_rank(1)
        assert final_rank >= initial_rank


class TestEdgeCases:
    """Test edge cases."""
    
    def test_empty_operations(self):
        """Test operations on empty set."""
        ds = DisjointSet[int]()
        assert ds.find(1) is None
        assert ds.component_size(1) == 0
        assert ds.get_component(1) == set()
        assert ds.union(1, 2) == False
    
    def test_single_element(self):
        """Test with single element."""
        ds = DisjointSet[int]()
        ds.make_set(1)
        assert ds.find(1) == 1
        assert ds.component_size(1) == 1
        assert ds.component_count() == 1
    
    def test_self_union(self):
        """Test union with self."""
        ds = DisjointSet[int]()
        ds.make_set(1)
        assert ds.union(1, 1) == False  # No change
    
    def test_nonexistent_union(self):
        """Test union with non-existent elements."""
        ds = DisjointSet[int]()
        ds.make_set(1)
        assert ds.union(1, 2) == False  # 2 doesn't exist
        assert ds.union(3, 4) == False  # Both don't exist


def run_tests():
    """Run all tests manually."""
    import traceback
    
    test_classes = [
        TestDisjointSetBasic,
        TestDisjointSetQuery,
        TestDisjointSetBulk,
        TestDisjointSetSerialization,
        TestDisjointSetTypes,
        TestGraphUtilities,
        TestKruskalMST,
        TestSocialNetwork,
        TestImageProcessing,
        TestPathCompression,
        TestUnionByRank,
        TestEdgeCases
    ]
    
    total_tests = 0
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                total_tests += 1
                try:
                    getattr(instance, method_name)()
                    passed += 1
                    print(f"✓ {test_class.__name__}.{method_name}")
                except AssertionError as e:
                    failed += 1
                    print(f"✗ {test_class.__name__}.{method_name}")
                    print(f"  AssertionError: {e}")
                except Exception as e:
                    failed += 1
                    print(f"✗ {test_class.__name__}.{method_name}")
                    traceback.print_exc()
    
    print(f"\n{'='*50}")
    print(f"Total: {total_tests}, Passed: {passed}, Failed: {failed}")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)