"""
Unit tests for BST Utilities
=============================
Comprehensive tests for Binary Search Tree operations.
"""

import sys
import os
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    BST, BSTNode, create_bst, create_balanced_bst, 
    merge_bsts, are_identical, lowest_common_ancestor
)


class TestBSTNode(unittest.TestCase):
    """Tests for BSTNode class."""
    
    def test_node_creation(self):
        """Test node creation with value."""
        node = BSTNode(5)
        self.assertEqual(node.value, 5)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)
        self.assertIsNone(node.parent)
    
    def test_node_with_parent(self):
        """Test node creation with parent."""
        parent = BSTNode(10)
        child = BSTNode(5, parent=parent)
        parent.left = child
        
        self.assertEqual(child.parent, parent)
        self.assertEqual(parent.left, child)
    
    def test_is_leaf(self):
        """Test leaf node detection."""
        node = BSTNode(5)
        self.assertTrue(node.is_leaf())
        
        node.left = BSTNode(3)
        self.assertFalse(node.is_leaf())
    
    def test_has_one_child(self):
        """Test single child detection."""
        node = BSTNode(5)
        self.assertFalse(node.has_one_child())
        
        node.left = BSTNode(3)
        self.assertTrue(node.has_one_child())
        
        node.right = BSTNode(7)
        self.assertFalse(node.has_one_child())
    
    def test_has_two_children(self):
        """Test two children detection."""
        node = BSTNode(5)
        self.assertFalse(node.has_two_children())
        
        node.left = BSTNode(3)
        node.right = BSTNode(7)
        self.assertTrue(node.has_two_children())


class TestBSTBasicOperations(unittest.TestCase):
    """Tests for basic BST operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.bst = BST[int]()
    
    def test_empty_tree(self):
        """Test empty tree properties."""
        self.assertTrue(self.bst.is_empty)
        self.assertEqual(self.bst.size, 0)
        self.assertIsNone(self.bst.root)
        self.assertEqual(self.bst.height(), -1)
    
    def test_insert_single(self):
        """Test inserting a single value."""
        self.assertTrue(self.bst.insert(5))
        self.assertFalse(self.bst.is_empty)
        self.assertEqual(self.bst.size, 1)
        self.assertEqual(self.bst.root.value, 5)
    
    def test_insert_duplicate(self):
        """Test inserting duplicate value."""
        self.assertTrue(self.bst.insert(5))
        self.assertFalse(self.bst.insert(5))
        self.assertEqual(self.bst.size, 1)
    
    def test_insert_many(self):
        """Test inserting multiple values."""
        count = self.bst.insert_many([5, 3, 7, 1, 9, 4, 6])
        self.assertEqual(count, 7)
        self.assertEqual(self.bst.size, 7)
    
    def test_search_found(self):
        """Test searching for existing value."""
        self.bst.insert_many([5, 3, 7, 1, 9])
        node = self.bst.search(7)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 7)
    
    def test_search_not_found(self):
        """Test searching for non-existing value."""
        self.bst.insert_many([5, 3, 7, 1, 9])
        self.assertIsNone(self.bst.search(10))
    
    def test_contains(self):
        """Test contains method."""
        self.bst.insert_many([5, 3, 7])
        self.assertTrue(self.bst.contains(5))
        self.assertTrue(self.bst.contains(3))
        self.assertFalse(self.bst.contains(10))
    
    def test_delete_leaf(self):
        """Test deleting a leaf node."""
        self.bst.insert_many([5, 3, 7])
        self.assertTrue(self.bst.delete(3))
        self.assertEqual(self.bst.size, 2)
        self.assertIsNone(self.bst.root.left)
    
    def test_delete_node_with_one_child(self):
        """Test deleting node with one child."""
        self.bst.insert_many([5, 3, 2])
        self.assertTrue(self.bst.delete(3))
        self.assertEqual(self.bst.size, 2)
        self.assertEqual(self.bst.root.left.value, 2)
    
    def test_delete_node_with_two_children(self):
        """Test deleting node with two children."""
        self.bst.insert_many([5, 3, 7, 2, 4, 6, 8])
        self.assertTrue(self.bst.delete(3))
        self.assertEqual(self.bst.size, 6)
        self.assertTrue(self.bst.contains(2))
        self.assertTrue(self.bst.contains(4))
    
    def test_delete_root(self):
        """Test deleting root node."""
        self.bst.insert_many([5, 3, 7])
        self.assertTrue(self.bst.delete(5))
        self.assertEqual(self.bst.size, 2)
        self.assertIsNotNone(self.bst.root)
    
    def test_delete_nonexistent(self):
        """Test deleting non-existent value."""
        self.bst.insert_many([5, 3, 7])
        self.assertFalse(self.bst.delete(10))
        self.assertEqual(self.bst.size, 3)
    
    def test_clear(self):
        """Test clearing the tree."""
        self.bst.insert_many([5, 3, 7, 1, 9])
        self.bst.clear()
        self.assertTrue(self.bst.is_empty)
        self.assertEqual(self.bst.size, 0)
        self.assertIsNone(self.bst.root)


class TestBSTMinMax(unittest.TestCase):
    """Tests for min/max operations."""
    
    def setUp(self):
        self.bst = BST[int]()
    
    def test_find_min_empty(self):
        """Test finding min in empty tree."""
        self.assertIsNone(self.bst.find_min())
    
    def test_find_max_empty(self):
        """Test finding max in empty tree."""
        self.assertIsNone(self.bst.find_max())
    
    def test_find_min_single(self):
        """Test finding min with single node."""
        self.bst.insert(5)
        self.assertEqual(self.bst.find_min(), 5)
    
    def test_find_max_single(self):
        """Test finding max with single node."""
        self.bst.insert(5)
        self.assertEqual(self.bst.find_max(), 5)
    
    def test_find_min_multiple(self):
        """Test finding min with multiple nodes."""
        self.bst.insert_many([5, 3, 7, 1, 9, 2, 8])
        self.assertEqual(self.bst.find_min(), 1)
    
    def test_find_max_multiple(self):
        """Test finding max with multiple nodes."""
        self.bst.insert_many([5, 3, 7, 1, 9, 2, 8])
        self.assertEqual(self.bst.find_max(), 9)


class TestBSTSuccessorPredecessor(unittest.TestCase):
    """Tests for successor/predecessor operations."""
    
    def setUp(self):
        self.bst = BST[int]()
    
    def test_successor_empty(self):
        """Test successor in empty tree."""
        self.assertIsNone(self.bst.find_successor(5))
    
    def test_successor_not_found(self):
        """Test successor of non-existent value."""
        self.bst.insert_many([5, 3, 7])
        self.assertIsNone(self.bst.find_successor(10))
    
    def test_successor_right_subtree(self):
        """Test successor when right subtree exists."""
        self.bst.insert_many([5, 3, 7, 6, 8])
        self.assertEqual(self.bst.find_successor(5), 6)
        self.assertEqual(self.bst.find_successor(7), 8)
    
    def test_successor_no_right_subtree(self):
        """Test successor when no right subtree."""
        self.bst.insert_many([5, 3, 7, 6])
        self.assertEqual(self.bst.find_successor(6), 7)
    
    def test_successor_max(self):
        """Test successor of maximum value."""
        self.bst.insert_many([5, 3, 7])
        self.assertIsNone(self.bst.find_successor(7))
    
    def test_predecessor_empty(self):
        """Test predecessor in empty tree."""
        self.assertIsNone(self.bst.find_predecessor(5))
    
    def test_predecessor_not_found(self):
        """Test predecessor of non-existent value."""
        self.bst.insert_many([5, 3, 7])
        self.assertIsNone(self.bst.find_predecessor(10))
    
    def test_predecessor_left_subtree(self):
        """Test predecessor when left subtree exists."""
        self.bst.insert_many([5, 3, 7, 2, 4])
        self.assertEqual(self.bst.find_predecessor(5), 4)
        self.assertEqual(self.bst.find_predecessor(3), 2)
    
    def test_predecessor_no_left_subtree(self):
        """Test predecessor when no left subtree."""
        self.bst.insert_many([5, 3, 7, 4])
        self.assertEqual(self.bst.find_predecessor(4), 3)
    
    def test_predecessor_min(self):
        """Test predecessor of minimum value."""
        self.bst.insert_many([5, 3, 7])
        self.assertIsNone(self.bst.find_predecessor(3))


class TestBSTTraversals(unittest.TestCase):
    """Tests for traversal methods."""
    
    def setUp(self):
        """
        Build tree:
              5
            /   \
           3     7
          / \   / \
         1   4 6   9
        """
        self.bst = BST[int]()
        self.bst.insert_many([5, 3, 7, 1, 4, 6, 9])
    
    def test_inorder(self):
        """Test in-order traversal (sorted order)."""
        result = list(self.bst.inorder())
        self.assertEqual(result, [1, 3, 4, 5, 6, 7, 9])
    
    def test_preorder(self):
        """Test pre-order traversal."""
        result = list(self.bst.preorder())
        self.assertEqual(result, [5, 3, 1, 4, 7, 6, 9])
    
    def test_postorder(self):
        """Test post-order traversal."""
        result = list(self.bst.postorder())
        self.assertEqual(result, [1, 4, 3, 6, 9, 7, 5])
    
    def test_levelorder(self):
        """Test level-order traversal."""
        result = list(self.bst.levelorder())
        self.assertEqual(result, [5, 3, 7, 1, 4, 6, 9])
    
    def test_reverse_inorder(self):
        """Test reverse in-order traversal (descending)."""
        result = list(self.bst.reverse_inorder())
        self.assertEqual(result, [9, 7, 6, 5, 4, 3, 1])
    
    def test_iterator(self):
        """Test iteration over BST."""
        result = list(self.bst)
        self.assertEqual(result, [1, 3, 4, 5, 6, 7, 9])


class TestBSTProperties(unittest.TestCase):
    """Tests for tree property methods."""
    
    def test_height_empty(self):
        """Test height of empty tree."""
        bst = BST[int]()
        self.assertEqual(bst.height(), -1)
    
    def test_height_single_node(self):
        """Test height of single node."""
        bst = BST[int]()
        bst.insert(5)
        self.assertEqual(bst.height(), 0)
    
    def test_height_balanced(self):
        """Test height of balanced tree."""
        bst = BST[int]()
        bst.insert_many([5, 3, 7])
        self.assertEqual(bst.height(), 1)
    
    def test_height_unbalanced(self):
        """Test height of unbalanced tree."""
        bst = BST[int]()
        bst.insert_many([1, 2, 3, 4, 5])
        self.assertEqual(bst.height(), 4)
    
    def test_depth(self):
        """Test depth calculation."""
        bst = BST[int]()
        bst.insert_many([5, 3, 7, 1, 9])
        
        self.assertEqual(bst.depth(5), 0)  # root
        self.assertEqual(bst.depth(3), 1)
        self.assertEqual(bst.depth(7), 1)
        self.assertEqual(bst.depth(1), 2)
        self.assertEqual(bst.depth(9), 2)
    
    def test_depth_not_found(self):
        """Test depth of non-existent value."""
        bst = BST[int]()
        bst.insert_many([5, 3, 7])
        self.assertEqual(bst.depth(10), -1)
    
    def test_is_balanced_true(self):
        """Test balanced tree detection."""
        bst = BST[int]()
        bst.insert_many([5, 3, 7, 1, 4, 6, 9])
        self.assertTrue(bst.is_balanced())
    
    def test_is_balanced_false(self):
        """Test unbalanced tree detection."""
        bst = BST[int]()
        bst.insert_many([1, 2, 3, 4, 5])
        self.assertFalse(bst.is_balanced())
    
    def test_is_valid_bst_true(self):
        """Test valid BST detection."""
        bst = BST[int]()
        bst.insert_many([5, 3, 7, 1, 9])
        self.assertTrue(bst.is_valid_bst())
    
    def test_len(self):
        """Test len() function."""
        bst = BST[int]()
        self.assertEqual(len(bst), 0)
        bst.insert_many([5, 3, 7])
        self.assertEqual(len(bst), 3)


class TestBSTRangeQuery(unittest.TestCase):
    """Tests for range query operations."""
    
    def setUp(self):
        self.bst = BST[int]()
        self.bst.insert_many([5, 3, 7, 1, 4, 6, 9, 2, 8])
    
    def test_range_query_full(self):
        """Test range query covering all values."""
        result = self.bst.range_query(1, 9)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    
    def test_range_query_partial(self):
        """Test partial range query."""
        result = self.bst.range_query(3, 7)
        self.assertEqual(result, [3, 4, 5, 6, 7])
    
    def test_range_query_single(self):
        """Test range query for single value."""
        result = self.bst.range_query(5, 5)
        self.assertEqual(result, [5])
    
    def test_range_query_empty(self):
        """Test range query with no results."""
        result = self.bst.range_query(10, 20)
        self.assertEqual(result, [])
    
    def test_count_range(self):
        """Test counting values in range."""
        self.assertEqual(self.bst.count_range(3, 7), 5)
        self.assertEqual(self.bst.count_range(1, 9), 9)


class TestBSTKthElement(unittest.TestCase):
    """Tests for k-th element operations."""
    
    def setUp(self):
        self.bst = BST[int]()
        self.bst.insert_many([5, 3, 7, 1, 9, 4, 6])
    
    def test_kth_smallest(self):
        """Test finding k-th smallest."""
        self.assertEqual(self.bst.kth_smallest(1), 1)
        self.assertEqual(self.bst.kth_smallest(2), 3)
        self.assertEqual(self.bst.kth_smallest(3), 4)
        self.assertEqual(self.bst.kth_smallest(7), 9)
    
    def test_kth_smallest_invalid(self):
        """Test k-th smallest with invalid k."""
        self.assertIsNone(self.bst.kth_smallest(0))
        self.assertIsNone(self.bst.kth_smallest(8))
        self.assertIsNone(self.bst.kth_smallest(-1))
    
    def test_kth_largest(self):
        """Test finding k-th largest."""
        self.assertEqual(self.bst.kth_largest(1), 9)
        self.assertEqual(self.bst.kth_largest(2), 7)
        self.assertEqual(self.bst.kth_largest(3), 6)
        self.assertEqual(self.bst.kth_largest(7), 1)
    
    def test_kth_largest_invalid(self):
        """Test k-th largest with invalid k."""
        self.assertIsNone(self.bst.kth_largest(0))
        self.assertIsNone(self.bst.kth_largest(8))


class TestBSTSerialization(unittest.TestCase):
    """Tests for serialization/deserialization."""
    
    def test_to_list_empty(self):
        """Test serializing empty tree."""
        bst = BST[int]()
        self.assertEqual(bst.to_list(), [])
    
    def test_to_list_single(self):
        """Test serializing single node."""
        bst = BST[int]()
        bst.insert(5)
        self.assertEqual(bst.to_list(), [5])
    
    def test_to_list_full_tree(self):
        """Test serializing full tree."""
        bst = BST[int]()
        bst.insert_many([5, 3, 7])
        result = bst.to_list()
        self.assertEqual(result[0], 5)  # root
        # Level order: [5, 3, 7]
    
    def test_from_list_empty(self):
        """Test deserializing empty list."""
        bst = BST.from_list([])
        self.assertTrue(bst.is_empty)
    
    def test_from_list_single(self):
        """Test deserializing single element."""
        bst = BST.from_list([5])
        self.assertEqual(bst.size, 1)
        self.assertEqual(bst.root.value, 5)
    
    def test_from_list_full(self):
        """Test deserializing full tree."""
        bst = BST[int]()
        bst.insert_many([5, 3, 7, 1, 9])
        serialized = bst.to_list()
        
        bst2 = BST.from_list(serialized)
        self.assertEqual(bst.size, bst2.size)
        self.assertEqual(list(bst.inorder()), list(bst2.inorder()))
    
    def test_to_sorted_list(self):
        """Test getting sorted list."""
        bst = BST[int]()
        bst.insert_many([5, 3, 7, 1, 9, 4, 6])
        self.assertEqual(bst.to_sorted_list(), [1, 3, 4, 5, 6, 7, 9])
    
    def test_round_trip(self):
        """Test serialize/deserialize round trip."""
        bst1 = BST[int]()
        bst1.insert_many([5, 3, 7, 1, 9, 4, 6, 2, 8])
        
        serialized = bst1.to_list()
        bst2 = BST.from_list(serialized)
        
        self.assertEqual(list(bst1.inorder()), list(bst2.inorder()))


class TestBSTBalancing(unittest.TestCase):
    """Tests for balancing operations."""
    
    def test_from_sorted_list(self):
        """Test creating BST from sorted list."""
        values = [1, 2, 3, 4, 5, 6, 7]
        bst = BST.from_sorted_list(values)
        
        self.assertEqual(bst.size, 7)
        self.assertEqual(bst.root.value, 4)  # Middle element
        self.assertTrue(bst.is_balanced())
    
    def test_balance_unbalanced(self):
        """Test balancing an unbalanced tree."""
        bst = BST[int]()
        bst.insert_many([1, 2, 3, 4, 5, 6, 7])
        
        self.assertEqual(bst.height(), 6)
        self.assertFalse(bst.is_balanced())
        
        bst.balance()
        
        self.assertEqual(bst.size, 7)
        self.assertTrue(bst.is_balanced())
        self.assertLess(bst.height(), 3)


class TestUtilityFunctions(unittest.TestCase):
    """Tests for utility functions."""
    
    def test_create_bst(self):
        """Test create_bst function."""
        bst = create_bst([5, 3, 7, 1, 9])
        self.assertEqual(bst.size, 5)
        self.assertEqual(list(bst.inorder()), [1, 3, 5, 7, 9])
    
    def test_create_balanced_bst(self):
        """Test create_balanced_bst function."""
        bst = create_balanced_bst([1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(bst.size, 7)
        self.assertTrue(bst.is_balanced())
    
    def test_merge_bsts(self):
        """Test merging two BSTs."""
        bst1 = create_bst([1, 3, 5])
        bst2 = create_bst([2, 4, 6])
        
        merged = merge_bsts(bst1, bst2)
        
        self.assertEqual(merged.size, 6)
        self.assertEqual(list(merged.inorder()), [1, 2, 3, 4, 5, 6])
        self.assertTrue(merged.is_balanced())
    
    def test_merge_bsts_with_overlap(self):
        """Test merging BSTs with overlapping values."""
        bst1 = create_bst([1, 2, 3])
        bst2 = create_bst([2, 3, 4])
        
        merged = merge_bsts(bst1, bst2)
        
        self.assertEqual(merged.size, 4)  # Duplicates removed
        self.assertEqual(list(merged.inorder()), [1, 2, 3, 4])
    
    def test_are_identical_true(self):
        """Test identical trees detection."""
        bst1 = create_bst([5, 3, 7, 1, 9])
        bst2 = create_bst([5, 3, 7, 1, 9])
        
        self.assertTrue(are_identical(bst1, bst2))
    
    def test_are_identical_false_structure(self):
        """Test different structure detection."""
        bst1 = create_bst([5, 3, 7])
        bst2 = create_bst([5, 3, 9])
        
        self.assertFalse(are_identical(bst1, bst2))
    
    def test_are_identical_false_values(self):
        """Test different values detection."""
        bst1 = create_bst([5, 3, 7])
        bst2 = create_bst([5, 3, 8])
        
        self.assertFalse(are_identical(bst1, bst2))
    
    def test_lowest_common_ancestor(self):
        """Test LCA finding."""
        bst = create_bst([5, 3, 7, 1, 4, 6, 9])
        
        self.assertEqual(lowest_common_ancestor(bst, 1, 4), 3)
        self.assertEqual(lowest_common_ancestor(bst, 3, 7), 5)
        self.assertEqual(lowest_common_ancestor(bst, 6, 9), 7)
        self.assertEqual(lowest_common_ancestor(bst, 1, 9), 5)
    
    def test_lca_not_found(self):
        """Test LCA with non-existent values."""
        bst = create_bst([5, 3, 7])
        
        self.assertIsNone(lowest_common_ancestor(bst, 1, 3))
        self.assertIsNone(lowest_common_ancestor(bst, 5, 10))


class TestBSTStringTypes(unittest.TestCase):
    """Tests with string values."""
    
    def test_string_insert_search(self):
        """Test BST with string values."""
        bst = BST[str]()
        bst.insert_many(["banana", "apple", "cherry", "date"])
        
        self.assertEqual(bst.size, 4)
        self.assertEqual(list(bst.inorder()), ["apple", "banana", "cherry", "date"])
        self.assertTrue(bst.contains("apple"))
        self.assertFalse(bst.contains("grape"))
    
    def test_string_min_max(self):
        """Test min/max with strings."""
        bst = BST[str]()
        bst.insert_many(["banana", "apple", "cherry"])
        
        self.assertEqual(bst.find_min(), "apple")
        self.assertEqual(bst.find_max(), "cherry")


class TestBSTEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_large_tree(self):
        """Test with larger tree."""
        bst = BST[int]()
        values = list(range(1000, 0, -1))  # Descending order
        bst.insert_many(values)
        
        self.assertEqual(bst.size, 1000)
        self.assertEqual(bst.find_min(), 1)
        self.assertEqual(bst.find_max(), 1000)
        self.assertEqual(bst.kth_smallest(500), 500)
    
    def test_negative_values(self):
        """Test with negative values."""
        bst = BST[int]()
        bst.insert_many([-5, -10, 0, 5, 10])
        
        self.assertEqual(bst.find_min(), -10)
        self.assertEqual(bst.find_max(), 10)
        self.assertEqual(list(bst.inorder()), [-10, -5, 0, 5, 10])
    
    def test_float_values(self):
        """Test with float values."""
        bst = BST[float]()
        bst.insert_many([3.14, 2.71, 1.41, 1.73])
        
        self.assertEqual(bst.find_min(), 1.41)
        self.assertEqual(bst.find_max(), 3.14)
    
    def test_contains_operator(self):
        """Test 'in' operator."""
        bst = create_bst([1, 2, 3, 4, 5])
        
        self.assertIn(3, bst)
        self.assertNotIn(6, bst)
    
    def test_str_representation(self):
        """Test string representation."""
        bst = BST[int]()
        bst.insert_many([5, 3, 7])
        
        s = str(bst)
        self.assertIn("BST:", s)
        self.assertIn("5", s)


if __name__ == "__main__":
    unittest.main(verbosity=2)