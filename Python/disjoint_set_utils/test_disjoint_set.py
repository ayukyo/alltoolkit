"""
Tests for Disjoint Set Union Implementation

Comprehensive test suite for Union-Find data structure.
"""

import unittest
from disjoint_set_utils import (
    DisjointSet,
    WeightedDisjointSet,
    DisjointSetWithUndo,
    count_connected_components,
    detect_cycle_undirected,
    kruskal_mst,
    find_redundant_connection
)


class TestDisjointSet(unittest.TestCase):
    """Test cases for basic DisjointSet."""
    
    def test_make_set(self):
        """Test creating singleton sets."""
        ds = DisjointSet[int]()
        ds.make_set(1)
        
        self.assertIn(1, ds)
        self.assertEqual(ds.find(1), 1)
        self.assertEqual(ds.count_sets(), 1)
    
    def test_make_sets(self):
        """Test creating multiple sets at once."""
        ds = DisjointSet[int]()
        ds.make_sets([1, 2, 3, 4, 5])
        
        self.assertEqual(len(ds), 5)
        self.assertEqual(ds.count_sets(), 5)
        
        # Each element should be its own parent
        for i in range(1, 6):
            self.assertEqual(ds.find(i), i)
    
    def test_duplicate_make_set(self):
        """Test that duplicate make_set raises error."""
        ds = DisjointSet[int]()
        ds.make_set(1)
        
        with self.assertRaises(ValueError):
            ds.make_set(1)
    
    def test_find_nonexistent(self):
        """Test finding non-existent element."""
        ds = DisjointSet[int]()
        
        with self.assertRaises(KeyError):
            ds.find(1)
    
    def test_union(self):
        """Test uniting two sets."""
        ds = DisjointSet[int]()
        ds.make_sets([1, 2])
        
        # Initially separate
        self.assertFalse(ds.connected(1, 2))
        self.assertEqual(ds.count_sets(), 2)
        
        # Union
        result = ds.union(1, 2)
        self.assertTrue(result)  # Union performed
        
        # Now connected
        self.assertTrue(ds.connected(1, 2))
        self.assertEqual(ds.count_sets(), 1)
        
        # Same root
        self.assertEqual(ds.find(1), ds.find(2))
    
    def test_union_same_set(self):
        """Test union of already connected elements."""
        ds = DisjointSet[int]()
        ds.make_sets([1, 2])
        
        ds.union(1, 2)
        result = ds.union(1, 2)  # Already connected
        
        self.assertFalse(result)
    
    def test_path_compression(self):
        """Test that path compression works."""
        ds = DisjointSet[int]()
        ds.make_sets([1, 2, 3, 4, 5])
        
        # Create a chain: 1 <- 2 <- 3 <- 4 <- 5
        ds.union(1, 2)
        ds.union(2, 3)
        ds.union(3, 4)
        ds.union(4, 5)
        
        # All should have same root
        root = ds.find(5)
        self.assertEqual(ds.find(1), root)
        self.assertEqual(ds.find(2), root)
        self.assertEqual(ds.find(3), root)
        self.assertEqual(ds.find(4), root)
        self.assertEqual(ds.find(5), root)
    
    def test_union_by_rank(self):
        """Test union by rank optimization."""
        ds = DisjointSet[int]()
        ds.make_sets(list(range(10)))
        
        # Union 0-4, 5-9 separately
        for i in range(1, 5):
            ds.union(0, i)
        for i in range(6, 10):
            ds.union(5, i)
        
        # Now union the two groups
        ds.union(0, 5)
        
        # All should be connected
        for i in range(10):
            self.assertTrue(ds.connected(0, i))
    
    def test_get_size(self):
        """Test getting component size."""
        ds = DisjointSet[int]()
        ds.make_sets([1, 2, 3, 4, 5])
        
        ds.union(1, 2)
        ds.union(1, 3)
        
        self.assertEqual(ds.get_size(1), 3)
        self.assertEqual(ds.get_size(2), 3)
        self.assertEqual(ds.get_size(4), 1)
    
    def test_get_sets(self):
        """Test getting all disjoint sets."""
        ds = DisjointSet[int]()
        ds.make_sets([1, 2, 3, 4, 5])
        
        ds.union(1, 2)
        ds.union(4, 5)
        
        sets = ds.get_sets()
        self.assertEqual(len(sets), 3)  # 3 disjoint sets
        
        # Check that 1,2 are together and 4,5 are together
        for root, members in sets.items():
            if 1 in members:
                self.assertIn(2, members)
                self.assertEqual(len(members), 2)
            elif 4 in members:
                self.assertIn(5, members)
                self.assertEqual(len(members), 2)
            elif 3 in members:
                self.assertEqual(len(members), 1)
    
    def test_get_members(self):
        """Test getting members of a component."""
        ds = DisjointSet[int]()
        ds.make_sets([1, 2, 3, 4])
        
        ds.union(1, 2)
        ds.union(2, 3)
        
        members = ds.get_members(1)
        self.assertEqual(members, {1, 2, 3})
    
    def test_string_elements(self):
        """Test with string elements."""
        ds = DisjointSet[str]()
        ds.make_sets(['a', 'b', 'c', 'd'])
        
        ds.union('a', 'b')
        ds.union('c', 'd')
        
        self.assertTrue(ds.connected('a', 'b'))
        self.assertTrue(ds.connected('c', 'd'))
        self.assertFalse(ds.connected('a', 'c'))
        self.assertEqual(ds.count_sets(), 2)
    
    def test_tuple_elements(self):
        """Test with tuple elements."""
        ds = DisjointSet[tuple]()
        ds.make_sets([(0, 0), (0, 1), (1, 0), (1, 1)])
        
        ds.union((0, 0), (0, 1))
        ds.union((1, 0), (1, 1))
        ds.union((0, 0), (1, 0))
        
        self.assertTrue(ds.connected((0, 1), (1, 1)))
        self.assertEqual(ds.count_sets(), 1)
    
    def test_large_scale(self):
        """Test with many elements."""
        n = 10000
        ds = DisjointSet[int]()
        ds.make_sets(list(range(n)))
        
        # Union pairs: 0-1, 2-3, 4-5, ...
        for i in range(0, n, 2):
            if i + 1 < n:
                ds.union(i, i + 1)
        
        self.assertEqual(ds.count_sets(), n // 2)


class TestWeightedDisjointSet(unittest.TestCase):
    """Test cases for WeightedDisjointSet."""
    
    def test_basic_operations(self):
        """Test basic weighted union operations."""
        wds = WeightedDisjointSet[str]()
        wds.make_set('a')
        wds.make_set('b')
        wds.make_set('c')
        
        wds.union_weighted('a', 'b', 5.0)
        self.assertTrue(wds.same_component('a', 'b'))
        self.assertEqual(wds.get_component_weight('a'), 5.0)
        
        wds.union_weighted('b', 'c', 3.0)
        self.assertTrue(wds.same_component('a', 'c'))
        self.assertEqual(wds.get_component_weight('a'), 8.0)
    
    def test_cumulative_weights(self):
        """Test that weights accumulate correctly."""
        wds = WeightedDisjointSet[int]()
        for i in range(5):
            wds.make_set(i)
        
        wds.union_weighted(0, 1, 2.0)
        wds.union_weighted(1, 2, 3.0)
        wds.union_weighted(2, 3, 4.0)
        wds.union_weighted(3, 4, 5.0)
        
        self.assertEqual(wds.get_component_weight(0), 14.0)
    
    def test_count_sets(self):
        """Test counting sets in weighted DSU."""
        wds = WeightedDisjointSet[int]()
        wds.make_sets([1, 2, 3, 4, 5])
        
        self.assertEqual(wds.count_sets(), 5)
        
        wds.union_weighted(1, 2)
        wds.union_weighted(3, 4)
        
        self.assertEqual(wds.count_sets(), 3)


class TestDisjointSetWithUndo(unittest.TestCase):
    """Test cases for DisjointSetWithUndo."""
    
    def test_make_and_undo(self):
        """Test making and undoing make_set."""
        ds = DisjointSetWithUndo[int]()
        
        ds.make_set(1)
        self.assertIn(1, ds._parent)
        
        ds.undo()
        self.assertNotIn(1, ds._parent)
    
    def test_union_and_undo(self):
        """Test union and undo."""
        ds = DisjointSetWithUndo[int]()
        ds.make_sets([1, 2, 3])
        
        ds.union(1, 2)
        self.assertTrue(ds.connected(1, 2))
        
        ds.undo()
        self.assertFalse(ds.connected(1, 2))
    
    def test_multiple_undos(self):
        """Test multiple undo operations."""
        ds = DisjointSetWithUndo[int]()
        ds.make_sets([1, 2, 3, 4])
        
        ds.union(1, 2)
        ds.union(3, 4)
        ds.union(1, 3)
        
        self.assertEqual(ds.count_sets(), 1)
        
        # Undo union(1, 3)
        ds.undo()
        self.assertEqual(ds.count_sets(), 2)
        
        # Undo union(3, 4)
        ds.undo()
        self.assertEqual(ds.count_sets(), 3)
        
        # Undo union(1, 2)
        ds.undo()
        self.assertEqual(ds.count_sets(), 4)
    
    def test_history_size(self):
        """Test tracking history size."""
        ds = DisjointSetWithUndo[int]()
        ds.make_sets([1, 2])
        
        self.assertEqual(ds.history_size(), 2)
        
        ds.union(1, 2)
        self.assertEqual(ds.history_size(), 3)
        
        ds.undo()
        self.assertEqual(ds.history_size(), 2)


class TestAlgorithmHelpers(unittest.TestCase):
    """Test cases for algorithm helper functions."""
    
    def test_count_connected_components(self):
        """Test counting connected components."""
        # Single component
        n = 5
        edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
        self.assertEqual(count_connected_components(n, edges), 1)
        
        # Multiple components
        n = 6
        edges = [(0, 1), (2, 3), (4, 5)]
        self.assertEqual(count_connected_components(n, edges), 3)
        
        # No edges
        n = 5
        edges = []
        self.assertEqual(count_connected_components(n, edges), 5)
    
    def test_detect_cycle_undirected(self):
        """Test cycle detection in undirected graphs."""
        # Has cycle: 0-1-2-0
        self.assertTrue(detect_cycle_undirected(3, [(0, 1), (1, 2), (2, 0)]))
        
        # No cycle
        self.assertFalse(detect_cycle_undirected(3, [(0, 1), (1, 2)]))
        
        # Complex graph with cycle
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 1)]  # Cycle: 1-2-3-4-1
        self.assertTrue(detect_cycle_undirected(5, edges))
    
    def test_kruskal_mst(self):
        """Test Kruskal's MST algorithm."""
        n = 4
        edges = [
            (0, 1, 1.0),
            (1, 2, 2.0),
            (2, 3, 3.0),
            (0, 3, 4.0),  # This edge won't be in MST
            (1, 3, 5.0)   # This edge won't be in MST
        ]
        
        mst, total_weight = kruskal_mst(n, edges)
        
        self.assertEqual(len(mst), 3)  # MST has n-1 edges
        self.assertEqual(total_weight, 6.0)  # 1 + 2 + 3
        
        # Check that all vertices are connected
        ds = DisjointSet[int]()
        ds.make_sets(list(range(n)))
        for u, v, w in mst:
            ds.union(u, v)
        
        self.assertEqual(ds.count_sets(), 1)
    
    def test_kruskal_mst_disconnected(self):
        """Test MST on disconnected graph."""
        n = 4
        edges = [(0, 1, 1.0), (2, 3, 1.0)]  # Two separate components
        
        mst, total_weight = kruskal_mst(n, edges)
        
        self.assertEqual(len(mst), 2)
        self.assertEqual(total_weight, 2.0)
    
    def test_find_redundant_connection(self):
        """Test finding redundant connection."""
        # Graph with redundancy
        n = 3
        edges = [(1, 2), (1, 3), (2, 3)]
        result = find_redundant_connection(n, edges)
        self.assertEqual(result, (2, 3))
        
        # No redundancy
        n = 3
        edges = [(1, 2), (2, 3)]
        result = find_redundant_connection(n, edges)
        self.assertIsNone(result)
    
    def test_find_redundant_connection_multiple(self):
        """Test finding last redundant connection."""
        n = 5
        edges = [(1, 2), (2, 3), (3, 4), (1, 4), (1, 5)]
        # (1, 4) creates cycle: 1-2-3-4-1
        result = find_redundant_connection(n, edges)
        self.assertEqual(result, (1, 4))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_single_element(self):
        """Test with single element."""
        ds = DisjointSet[int]()
        ds.make_set(1)
        
        self.assertEqual(ds.find(1), 1)
        self.assertEqual(ds.count_sets(), 1)
        self.assertEqual(ds.get_size(1), 1)
        self.assertEqual(ds.get_members(1), {1})
    
    def test_empty_disjoint_set(self):
        """Test operations on empty set."""
        ds = DisjointSet[int]()
        
        self.assertEqual(len(ds), 0)
        self.assertEqual(ds.count_sets(), 0)
        self.assertEqual(ds.get_sets(), {})
    
    def test_large_numbers(self):
        """Test with large element values."""
        ds = DisjointSet[int]()
        elements = [10**15, 10**15 + 1, 10**15 + 2]
        
        ds.make_sets(elements)
        ds.union(elements[0], elements[1])
        
        self.assertTrue(ds.connected(elements[0], elements[1]))
        self.assertFalse(ds.connected(elements[0], elements[2]))
    
    def test_negative_elements(self):
        """Test with negative element values."""
        ds = DisjointSet[int]()
        ds.make_sets([-1, -2, -3])
        
        ds.union(-1, -2)
        self.assertTrue(ds.connected(-1, -2))
        self.assertFalse(ds.connected(-1, -3))
    
    def test_union_by_size_vs_rank(self):
        """Compare union by size vs union by rank."""
        # Both should produce same connectivity
        ds1 = DisjointSet[int]()
        ds2 = DisjointSet[int]()
        
        elements = list(range(100))
        ds1.make_sets(elements)
        ds2.make_sets(elements)
        
        import random
        random.seed(42)
        pairs = [(random.randint(0, 99), random.randint(0, 99)) for _ in range(50)]
        
        for a, b in pairs:
            ds1.union(a, b)
            ds2.union_by_size(a, b)
        
        # Both should have same connectivity
        for i in range(100):
            for j in range(100):
                self.assertEqual(ds1.connected(i, j), ds2.connected(i, j))


class TestIterativeFind(unittest.TestCase):
    """Test iterative find with path compression."""
    
    def test_iterative_vs_recursive(self):
        """Test that iterative find produces same results."""
        ds = DisjointSet[int]()
        ds.make_sets(list(range(100)))
        
        # Create some unions
        for i in range(0, 99, 2):
            ds.union(i, i + 1)
        
        # Compare recursive and iterative finds
        for i in range(100):
            self.assertEqual(ds.find(i), ds.find_iterative(i))


if __name__ == '__main__':
    unittest.main(verbosity=2)