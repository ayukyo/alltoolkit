"""Tests for binary_tree_utils."""

import unittest
from mod import (
    TreeNode, from_list, from_nested_tuple, to_list, to_nested_tuple,
    preorder, inorder, postorder, level_order, zigzag_level_order, morris_inorder,
    find, find_path, lowest_common_ancestor, lowest_common_ancestor_nodes,
    height, count, leaf_count, is_balanced, is_symmetric, is_same_tree, is_subtree,
    mirror, invert, clone, map_values, filter_nodes,
    insert_level_order, delete_node,
    diameter, all_paths, path_sum, max_path_sum,
    serialize, deserialize, pretty_print
)


class TestConstruction(unittest.TestCase):
    def test_from_list_complete(self):
        root = from_list([1, 2, 3])
        self.assertEqual(root.val, 1)
        self.assertEqual(root.left.val, 2)
        self.assertEqual(root.right.val, 3)
    
    def test_from_list_with_none(self):
        root = from_list([1, 2, None, 3, 4])
        self.assertEqual(root.val, 1)
        self.assertEqual(root.left.val, 2)
        self.assertEqual(root.right, None)
    
    def test_from_list_empty(self):
        self.assertIsNone(from_list([]))
    
    def test_from_nested_tuple(self):
        root = from_nested_tuple(((None, 2, None), 1, (None, 3, None)))
        self.assertEqual(root.val, 1)
        self.assertEqual(root.left.val, 2)
        self.assertEqual(root.right.val, 3)
    
    def test_to_list(self):
        root = from_list([1, 2, 3, None, 4])
        lst = to_list(root)
        self.assertEqual(lst, [1, 2, 3, None, 4])
    
    def test_to_nested_tuple(self):
        root = from_list([1, 2, 3])
        tpl = to_nested_tuple(root)
        self.assertEqual(tpl, ((None, 2, None), 1, (None, 3, None)))


class TestTraversal(unittest.TestCase):
    def setUp(self):
        self.root = from_list([1, 2, 3, 4, 5])
    
    def test_preorder(self):
        self.assertEqual(preorder(self.root), [1, 2, 4, 5, 3])
    
    def test_inorder(self):
        self.assertEqual(inorder(self.root), [4, 2, 5, 1, 3])
    
    def test_postorder(self):
        self.assertEqual(postorder(self.root), [4, 5, 2, 3, 1])
    
    def test_level_order(self):
        self.assertEqual(level_order(self.root), [[1], [2, 3], [4, 5]])
    
    def test_zigzag_level_order(self):
        self.assertEqual(zigzag_level_order(self.root), [[1], [3, 2], [4, 5]])
    
    def test_morris_inorder(self):
        self.assertEqual(morris_inorder(self.root), [4, 2, 5, 1, 3])


class TestQuery(unittest.TestCase):
    def setUp(self):
        self.root = from_list([1, 2, 3, 4, 5])
    
    def test_find_existing(self):
        node = find(self.root, 4)
        self.assertIsNotNone(node)
        self.assertEqual(node.val, 4)
    
    def test_find_non_existing(self):
        self.assertIsNone(find(self.root, 10))
    
    def test_find_path(self):
        path = find_path(self.root, 5)
        self.assertEqual([n.val for n in path], [1, 3, 5])
    
    def test_lowest_common_ancestor(self):
        lca = lowest_common_ancestor(self.root, 4, 5)
        self.assertEqual(lca.val, 2)
    
    def test_lca_root(self):
        lca = lowest_common_ancestor(self.root, 1, 5)
        self.assertEqual(lca.val, 1)


class TestProperties(unittest.TestCase):
    def test_height(self):
        root = from_list([1, 2, 3, 4, 5])
        self.assertEqual(height(root), 3)
    
    def test_height_empty(self):
        self.assertEqual(height(None), 0)
    
    def test_count(self):
        root = from_list([1, 2, 3, 4, 5])
        self.assertEqual(count(root), 5)
    
    def test_leaf_count(self):
        root = from_list([1, 2, 3, 4, 5])
        self.assertEqual(leaf_count(root), 2)
    
    def test_is_balanced_true(self):
        root = from_list([1, 2, 3])
        self.assertTrue(is_balanced(root))
    
    def test_is_balanced_false(self):
        root = from_list([1, None, 2, None, 3])
        self.assertFalse(is_balanced(root))
    
    def test_is_symmetric(self):
        root = from_nested_tuple(((None, 2, None), 1, (None, 2, None)))
        self.assertTrue(is_symmetric(root))
    
    def test_is_symmetric_false(self):
        root = from_list([1, 2, 3])
        self.assertFalse(is_symmetric(root))
    
    def test_is_same_tree_identical(self):
        t1 = from_list([1, 2, 3])
        t2 = from_list([1, 2, 3])
        self.assertTrue(is_same_tree(t1, t2))
    
    def test_is_same_tree_different(self):
        t1 = from_list([1, 2, 3])
        t2 = from_list([1, 2, 4])
        self.assertFalse(is_same_tree(t1, t2))
    
    def test_is_subtree(self):
        s = from_list([1, 2, 3, 4, 5])
        t = from_list([2, 4, 5])
        self.assertTrue(is_subtree(s, t))
    
    def test_is_not_subtree(self):
        s = from_list([1, 2, 3])
        t = from_list([2, 3, 4])
        self.assertFalse(is_subtree(s, t))


class TestModification(unittest.TestCase):
    def test_mirror(self):
        root = from_list([1, 2, 3, None, 4])
        mirrored = mirror(root)
        self.assertEqual(level_order(mirrored), [[1], [3, 2], [4]])
    
    def test_invert_alias(self):
        root = from_list([1, 2, 3])
        self.assertEqual(invert(root).right.val, 2)
    
    def test_clone(self):
        original = from_list([1, 2, 3])
        copy = clone(original)
        self.assertTrue(is_same_tree(original, copy))
        self.assertIsNot(original, copy)
    
    def test_map_values(self):
        root = from_list([1, 2, 3])
        doubled = map_values(root, lambda x: x * 2)
        self.assertEqual(level_order(doubled), [[2], [4, 6]])
    
    def test_filter_nodes(self):
        root = from_list([1, 2, 3, 4, 5, 6])
        filtered = filter_nodes(root, lambda x: x % 2 == 0)
        self.assertIsNotNone(find(filtered, 2))
        self.assertIsNone(find(filtered, 1))
    
    def test_insert_level_order(self):
        root = from_list([1, 2])
        inserted = insert_level_order(root, 3)
        self.assertEqual(level_order(inserted), [[1], [2, 3]])
    
    def test_delete_node(self):
        root = from_list([1, 2, 3, 4, 5])
        deleted = delete_node(root, 2)
        self.assertIsNone(find(deleted, 2))


class TestPathOperations(unittest.TestCase):
    def test_diameter(self):
        root = from_list([1, 2, 3, 4, 5])
        self.assertEqual(diameter(root), 3)
    
    def test_all_paths(self):
        root = from_list([1, 2, 3])
        paths = all_paths(root)
        self.assertEqual(len(paths), 2)
    
    def test_path_sum_true(self):
        root = from_list([1, 2, 3])
        self.assertTrue(path_sum(root, 6))
    
    def test_path_sum_false(self):
        root = from_list([1, 2, 3])
        self.assertFalse(path_sum(root, 10))
    
    def test_max_path_sum(self):
        root = from_list([1, 2, 3])
        self.assertEqual(max_path_sum(root), 6)


class TestSerialization(unittest.TestCase):
    def test_serialize_deserialize(self):
        original = from_list([1, 2, 3, None, 4])
        serialized = serialize(original)
        restored = deserialize(serialized)
        self.assertTrue(is_same_tree(original, restored))
    
    def test_serialize_empty(self):
        self.assertEqual(serialize(None), "#")


class TestPrettyPrint(unittest.TestCase):
    def test_pretty_print(self):
        root = from_list([1, 2, 3])
        output = pretty_print(root)
        self.assertIn("1", output)


if __name__ == '__main__':
    unittest.main()