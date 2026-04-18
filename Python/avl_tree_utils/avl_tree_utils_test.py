"""
AllToolkit - Python AVL Tree Utilities Test Suite

全面测试 AVL 树工具模块的所有功能
包括：插入、删除、查找、遍历、范围查询、顺序统计、平衡验证、边界值测试

@author AllToolkit
@version 1.0.0
"""

import unittest
import random
import math
import sys
import os

# 导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    AVLTree, AVLNode, create_avl_tree, from_sorted_list,
    merge_avl_trees, split_avl_tree, avl_tree_to_dict, dict_to_avl_tree,
    find_common_elements, find_difference, validate_avl_tree, get_tree_statistics
)


class TestAVLNode(unittest.TestCase):
    """测试 AVLNode 类"""
    
    def test_node_creation(self):
        """测试节点创建"""
        node = AVLNode(10)
        self.assertEqual(node.key, 10)
        self.assertIsNone(node.value)
        self.assertEqual(node.height, 1)
        self.assertEqual(node.size, 1)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)
    
    def test_node_with_value(self):
        """测试带值的节点"""
        node = AVLNode("key", "value")
        self.assertEqual(node.key, "key")
        self.assertEqual(node.value, "value")
    
    def test_balance_factor(self):
        """测试平衡因子计算"""
        node = AVLNode(10)
        node.left = AVLNode(5)
        node.left.height = 1
        node.right = AVLNode(15)
        node.right.height = 2
        node.height = 3
        
        self.assertEqual(node.balance_factor(), -1)  # 1 - 2 = -1
    
    def test_is_balanced(self):
        """测试平衡检查"""
        node = AVLNode(10)
        self.assertTrue(node.is_balanced())
        
        # 创建平衡节点（左右高度相等）
        node.left = AVLNode(5)
        node.left.height = 1
        node.right = AVLNode(15)
        node.right.height = 1
        node.height = 2
        self.assertTrue(node.is_balanced())
        
        # 创建略有不平衡但仍平衡的节点（左高1右高0，差值为1）
        node.right = None
        node.height = 2
        self.assertTrue(node.is_balanced())
        
        # 进一步不平衡（左子树高度差超过1）
        node.left.left = AVLNode(3)
        node.left.left.height = 1
        node.left.height = 2
        node.height = 3
        # balance_factor = 2 - 0 = 2，不平衡
        self.assertFalse(node.is_balanced())
    
    def test_update_height(self):
        """测试高度更新"""
        node = AVLNode(10)
        node.left = AVLNode(5)
        node.right = AVLNode(15)
        node.right.right = AVLNode(20)
        
        node.right.update_height()
        node.update_height()
        
        self.assertEqual(node.height, 3)
    
    def test_update_size(self):
        """测试大小更新"""
        node = AVLNode(10)
        node.left = AVLNode(5)
        node.left.left = AVLNode(3)
        node.left.right = AVLNode(7)
        
        node.left.update_size()
        node.update_size()
        
        self.assertEqual(node.left.size, 3)
        self.assertEqual(node.size, 4)


class TestAVLTreeBasic(unittest.TestCase):
    """测试 AVL 树基本操作"""
    
    def test_empty_tree(self):
        """测试空树"""
        tree = AVLTree()
        self.assertIsNone(tree.root)
        self.assertEqual(tree.size, 0)
        self.assertEqual(tree.height, 0)
        self.assertTrue(tree.is_empty)
        self.assertFalse(tree.allow_duplicates)
    
    def test_single_insert(self):
        """测试单节点插入"""
        tree = AVLTree()
        self.assertTrue(tree.insert(10))
        
        self.assertEqual(tree.size, 1)
        self.assertEqual(tree.height, 1)
        self.assertFalse(tree.is_empty)
        self.assertIsNotNone(tree.root)
        self.assertEqual(tree.root.key, 10)
    
    def test_multiple_inserts(self):
        """测试多节点插入"""
        tree = AVLTree()
        keys = [10, 20, 5, 15, 25, 3, 8]
        
        for key in keys:
            self.assertTrue(tree.insert(key))
        
        self.assertEqual(tree.size, len(keys))
        self.assertTrue(tree.is_valid_avl())
    
    def test_insert_with_value(self):
        """测试带值插入"""
        tree = AVLTree()
        tree.insert(10, "ten")
        tree.insert(5, "five")
        
        self.assertEqual(tree.get_value(10), "ten")
        self.assertEqual(tree.get_value(5), "five")
        self.assertIsNone(tree.get_value(20))
    
    def test_duplicate_insert_no_allow(self):
        """测试不允许重复时的插入"""
        tree = AVLTree(allow_duplicates=False)
        
        self.assertTrue(tree.insert(10))
        self.assertFalse(tree.insert(10))  # 重复插入失败
        self.assertEqual(tree.size, 1)
    
    def test_duplicate_insert_allow(self):
        """测试允许重复时的插入"""
        tree = AVLTree(allow_duplicates=True)
        
        self.assertTrue(tree.insert(10))
        self.assertTrue(tree.insert(10))  # 重复插入成功
        self.assertEqual(tree.size, 2)
    
    def test_update_value(self):
        """测试更新值"""
        tree = AVLTree()
        tree.insert(10, "old")
        
        self.assertFalse(tree.insert(10, "new"))  # 不插入新节点
        self.assertEqual(tree.get_value(10), "new")  # 但值被更新


class TestAVLTreeSearch(unittest.TestCase):
    """测试 AVL 树查找操作"""
    
    def setUp(self):
        """初始化测试树"""
        self.tree = AVLTree()
        keys = [10, 20, 5, 15, 25, 3, 8, 12, 18, 30]
        for key in keys:
            self.tree.insert(key, f"value_{key}")
    
    def test_search_existing(self):
        """测试查找存在的键"""
        for key in [10, 20, 5, 15, 25, 3, 8, 12, 18, 30]:
            node = self.tree.search(key)
            self.assertIsNotNone(node)
            self.assertEqual(node.key, key)
            self.assertEqual(node.value, f"value_{key}")
    
    def test_search_non_existing(self):
        """测试查找不存在的键"""
        for key in [1, 100, 7, 17, 22]:
            node = self.tree.search(key)
            self.assertIsNone(node)
    
    def test_contains(self):
        """测试 contains 方法"""
        self.assertTrue(self.tree.contains(10))
        self.assertTrue(self.tree.contains(5))
        self.assertFalse(self.tree.contains(1))
        self.assertFalse(self.tree.contains(100))
    
    def test_find_min(self):
        """测试查找最小值"""
        min_node = self.tree.find_min()
        self.assertIsNotNone(min_node)
        self.assertEqual(min_node.key, 3)
    
    def test_find_max(self):
        """测试查找最大值"""
        max_node = self.tree.find_max()
        self.assertIsNotNone(max_node)
        self.assertEqual(max_node.key, 30)
    
    def test_find_floor(self):
        """测试查找 floor"""
        self.assertEqual(self.tree.find_floor(15).key, 15)
        self.assertEqual(self.tree.find_floor(14).key, 12)
        self.assertEqual(self.tree.find_floor(4).key, 3)
        self.assertIsNone(self.tree.find_floor(2))
    
    def test_find_ceiling(self):
        """测试查找 ceiling"""
        self.assertEqual(self.tree.find_ceiling(15).key, 15)
        self.assertEqual(self.tree.find_ceiling(16).key, 18)
        self.assertEqual(self.tree.find_ceiling(26).key, 30)
        self.assertIsNone(self.tree.find_ceiling(31))
    
    def test_find_kth(self):
        """测试查找第 k 小"""
        keys = sorted([10, 20, 5, 15, 25, 3, 8, 12, 18, 30])
        
        for k in range(1, len(keys) + 1):
            node = self.tree.find_kth(k)
            self.assertIsNotNone(node)
            self.assertEqual(node.key, keys[k - 1])
        
        self.assertIsNone(self.tree.find_kth(0))
        self.assertIsNone(self.tree.find_kth(len(keys) + 1))
    
    def test_rank(self):
        """测试排名"""
        keys = sorted([10, 20, 5, 15, 25, 3, 8, 12, 18, 30])
        
        for key in keys:
            rank = self.tree.rank(key)
            self.assertEqual(rank, keys.index(key) + 1)
        
        self.assertEqual(self.tree.rank(1), 0)  # 不存在的键
    
    def test_count_range(self):
        """测试范围计数"""
        # keys: [10, 20, 5, 15, 25, 3, 8, 12, 18, 30]
        # range 10-20: 10, 12, 15, 18, 20 = 5 elements
        self.assertEqual(self.tree.count_range(10, 20), 5)
        self.assertEqual(self.tree.count_range(1, 100), 10)
        self.assertEqual(self.tree.count_range(5, 8), 2)  # 5, 8
        self.assertEqual(self.tree.count_range(100, 200), 0)


class TestAVLTreeDelete(unittest.TestCase):
    """测试 AVL 树删除操作"""
    
    def test_delete_leaf(self):
        """测试删除叶子节点"""
        tree = AVLTree()
        keys = [10, 5, 15, 3, 8, 12, 20]
        for key in keys:
            tree.insert(key)
        
        self.assertTrue(tree.delete(3))
        self.assertEqual(tree.size, 6)
        self.assertFalse(tree.contains(3))
        self.assertTrue(tree.is_valid_avl())
    
    def test_delete_single_child(self):
        """测试删除只有一个子节点的节点"""
        tree = AVLTree()
        keys = [10, 5, 15, 3, 20]
        for key in keys:
            tree.insert(key)
        
        self.assertTrue(tree.delete(15))
        self.assertEqual(tree.size, 4)
        self.assertFalse(tree.contains(15))
        self.assertTrue(tree.contains(20))
        self.assertTrue(tree.is_valid_avl())
    
    def test_delete_two_children(self):
        """测试删除有两个子节点的节点"""
        tree = AVLTree()
        keys = [10, 5, 15, 3, 8, 12, 20]
        for key in keys:
            tree.insert(key)
        
        self.assertTrue(tree.delete(10))
        self.assertEqual(tree.size, 6)
        self.assertFalse(tree.contains(10))
        self.assertTrue(tree.is_valid_avl())
    
    def test_delete_root(self):
        """测试删除根节点"""
        tree = AVLTree()
        keys = [10, 5, 15]
        for key in keys:
            tree.insert(key)
        
        self.assertTrue(tree.delete(10))
        self.assertEqual(tree.size, 2)
        self.assertTrue(tree.is_valid_avl())
    
    def test_delete_non_existing(self):
        """测试删除不存在的键"""
        tree = AVLTree()
        keys = [10, 5, 15]
        for key in keys:
            tree.insert(key)
        
        self.assertFalse(tree.delete(100))
        self.assertEqual(tree.size, 3)
    
    def test_delete_min(self):
        """测试删除最小值"""
        tree = AVLTree()
        keys = [10, 5, 15, 3, 8]
        for key in keys:
            tree.insert(key)
        
        min_key = tree.delete_min()
        self.assertEqual(min_key, 3)
        self.assertEqual(tree.size, 4)
        self.assertFalse(tree.contains(3))
        self.assertEqual(tree.find_min().key, 5)
    
    def test_delete_max(self):
        """测试删除最大值"""
        tree = AVLTree()
        keys = [10, 5, 15, 12, 20]
        for key in keys:
            tree.insert(key)
        
        max_key = tree.delete_max()
        self.assertEqual(max_key, 20)
        self.assertEqual(tree.size, 4)
        self.assertFalse(tree.contains(20))
        self.assertEqual(tree.find_max().key, 15)
    
    def test_delete_all(self):
        """测试删除所有节点"""
        tree = AVLTree()
        keys = [10, 5, 15, 3, 8, 12, 20]
        for key in keys:
            tree.insert(key)
        
        for key in keys:
            self.assertTrue(tree.delete(key))
        
        self.assertTrue(tree.is_empty)
        self.assertEqual(tree.size, 0)
    
    def test_delete_causes_rebalance(self):
        """测试删除导致重平衡"""
        tree = AVLTree()
        # 创建一个可能不平衡的序列
        keys = [10, 5, 15, 3, 7, 12, 20, 1, 4, 6, 8]
        for key in keys:
            tree.insert(key)
        
        # 删除一些节点触发重平衡
        for key in [20, 15, 12]:
            self.assertTrue(tree.delete(key))
        
        self.assertTrue(tree.is_valid_avl())


class TestAVLTreeTraversal(unittest.TestCase):
    """测试 AVL 树遍历操作"""
    
    def setUp(self):
        """初始化测试树"""
        self.tree = AVLTree()
        self.keys = [10, 5, 15, 3, 8, 12, 20]
        for key in self.keys:
            self.tree.insert(key)
    
    def test_inorder(self):
        """测试中序遍历"""
        result = list(self.tree.inorder())
        self.assertEqual(result, sorted(self.keys))
    
    def test_preorder(self):
        """测试前序遍历"""
        result = list(self.tree.preorder())
        self.assertEqual(len(result), len(self.keys))
        self.assertEqual(result[0], self.tree.root.key)
    
    def test_postorder(self):
        """测试后序遍历"""
        result = list(self.tree.postorder())
        self.assertEqual(len(result), len(self.keys))
        # 后序遍历最后访问根
        self.assertEqual(result[-1], self.tree.root.key)
    
    def test_level_order(self):
        """测试层序遍历"""
        result = list(self.tree.level_order())
        self.assertEqual(len(result), len(self.keys))
        self.assertEqual(result[0], self.tree.root.key)
    
    def test_inorder_nodes(self):
        """测试中序遍历节点"""
        nodes = list(self.tree.inorder_nodes())
        keys = [node.key for node in nodes]
        self.assertEqual(keys, sorted(self.keys))
    
    def test_empty_tree_traversal(self):
        """测试空树遍历"""
        tree = AVLTree()
        
        self.assertEqual(list(tree.inorder()), [])
        self.assertEqual(list(tree.preorder()), [])
        self.assertEqual(list(tree.postorder()), [])
        self.assertEqual(list(tree.level_order()), [])
    
    def test_iteration(self):
        """测试迭代器"""
        result = list(self.tree)
        self.assertEqual(result, sorted(self.keys))


class TestAVLTreeRangeQuery(unittest.TestCase):
    """测试 AVL 树范围查询"""
    
    def setUp(self):
        """初始化测试树"""
        self.tree = AVLTree()
        self.keys = [10, 5, 15, 3, 8, 12, 20, 1, 7, 14, 18, 25]
        for key in self.keys:
            self.tree.insert(key)
    
    def test_range_query(self):
        """测试范围查询"""
        result = self.tree.range_query(8, 15)
        expected = sorted([k for k in self.keys if 8 <= k <= 15])
        self.assertEqual(result, expected)
    
    def test_range_query_full(self):
        """测试全范围查询"""
        result = self.tree.range_query(0, 100)
        self.assertEqual(result, sorted(self.keys))
    
    def test_range_query_empty(self):
        """测试空范围查询"""
        result = self.tree.range_query(100, 200)
        self.assertEqual(result, [])
    
    def test_range_query_single(self):
        """测试单元素范围"""
        result = self.tree.range_query(10, 10)
        self.assertEqual(result, [10])
    
    def test_range_query_nodes(self):
        """测试范围查询节点"""
        nodes = self.tree.range_query_nodes(5, 15)
        keys = [node.key for node in nodes]
        expected = sorted([k for k in self.keys if 5 <= k <= 15])
        self.assertEqual(keys, expected)


class TestAVLTreeConversion(unittest.TestCase):
    """测试 AVL 树转换操作"""
    
    def setUp(self):
        """初始化测试树"""
        self.tree = AVLTree()
        for i, key in enumerate([10, 5, 15, 3, 8]):
            self.tree.insert(key, f"v{i}")
    
    def test_to_list(self):
        """测试转换为列表"""
        result = self.tree.to_list()
        self.assertEqual(result, [3, 5, 8, 10, 15])
    
    def test_to_sorted_list(self):
        """测试转换为有序列表"""
        result = self.tree.to_sorted_list()
        self.assertEqual(result, sorted([10, 5, 15, 3, 8]))
    
    def test_to_dict(self):
        """测试转换为字典"""
        result = self.tree.to_dict()
        expected_keys = {10, 5, 15, 3, 8}
        self.assertEqual(set(result.keys()), expected_keys)
    
    def test_keys(self):
        """测试获取键"""
        result = self.tree.keys()
        self.assertEqual(result, [3, 5, 8, 10, 15])
    
    def test_values(self):
        """测试获取值"""
        result = self.tree.values()
        self.assertEqual(len(result), 5)
    
    def test_clear(self):
        """测试清空"""
        self.tree.clear()
        self.assertTrue(self.tree.is_empty)
        self.assertEqual(self.tree.size, 0)
    
    def test_bulk_insert(self):
        """测试批量插入"""
        tree = AVLTree()
        items = [(10, "a"), (5, "b"), (15, "c")]
        count = tree.bulk_insert(items)
        self.assertEqual(count, 3)
        self.assertEqual(tree.size, 3)


class TestAVLTreeOtherOperations(unittest.TestCase):
    """测试 AVL 树其他操作"""
    
    def setUp(self):
        """初始化测试树"""
        self.tree = AVLTree()
        self.keys = [10, 5, 15, 3, 8, 12, 20]
        for key in self.keys:
            self.tree.insert(key)
    
    def test_predecessor(self):
        """测试前驱"""
        self.assertEqual(self.tree.predecessor(10), 8)
        self.assertEqual(self.tree.predecessor(5), 3)
        self.assertEqual(self.tree.predecessor(3), None)
    
    def test_successor(self):
        """测试后继"""
        self.assertEqual(self.tree.successor(10), 12)
        self.assertEqual(self.tree.successor(15), 20)
        self.assertEqual(self.tree.successor(20), None)
    
    def test_depth(self):
        """测试深度"""
        root_key = self.tree.root.key
        self.assertEqual(self.tree.depth(root_key), 0)
        
        # 子节点深度应该大于 0
        for key in self.keys:
            depth = self.tree.depth(key)
            self.assertGreaterEqual(depth, 0)
    
    def test_depth_non_existing(self):
        """测试不存在键的深度"""
        self.assertEqual(self.tree.depth(100), -1)
    
    def test_path_to(self):
        """测试路径"""
        for key in self.keys:
            path = self.tree.path_to(key)
            self.assertGreater(len(path), 0)
            self.assertEqual(path[-1], key)
            self.assertEqual(path[0], self.tree.root.key)
    
    def test_path_to_non_existing(self):
        """测试不存在键的路径"""
        path = self.tree.path_to(100)
        self.assertEqual(path, [])
    
    def test_visualize(self):
        """测试可视化"""
        viz = self.tree.visualize()
        self.assertGreater(len(viz), 0)
        self.assertIn(str(self.tree.root.key), viz)
    
    def test_empty_tree_visualize(self):
        """测试空树可视化"""
        tree = AVLTree()
        viz = tree.visualize()
        self.assertEqual(viz, "(empty tree)")
    
    def test_len(self):
        """测试 __len__"""
        self.assertEqual(len(self.tree), len(self.keys))
    
    def test_contains_operator(self):
        """测试 __contains__"""
        for key in self.keys:
            self.assertTrue(key in self.tree)
        self.assertFalse(100 in self.tree)
    
    def test_repr(self):
        """测试 __repr__"""
        repr_str = repr(self.tree)
        self.assertIn("AVLTree", repr_str)
        self.assertIn("size", repr_str)


class TestAVLTreeBalancing(unittest.TestCase):
    """测试 AVL 树平衡机制"""
    
    def test_insert_maintains_balance(self):
        """测试插入后保持平衡"""
        tree = AVLTree()
        
        # 顺序插入可能导致不平衡的序列
        keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for key in keys:
            tree.insert(key)
            self.assertTrue(tree.is_valid_avl())
    
    def test_delete_maintains_balance(self):
        """测试删除后保持平衡"""
        tree = AVLTree()
        keys = list(range(1, 21))
        for key in keys:
            tree.insert(key)
        
        # 随机删除
        random.shuffle(keys)
        for key in keys[:10]:
            tree.delete(key)
            self.assertTrue(tree.is_valid_avl())
    
    def test_ll_rotation(self):
        """测试 LL 旋转"""
        tree = AVLTree()
        tree.insert(30)
        tree.insert(20)
        tree.insert(10)  # 触发 LL
        
        self.assertTrue(tree.is_valid_avl())
        self.assertEqual(tree.root.key, 20)
    
    def test_rr_rotation(self):
        """测试 RR 旋转"""
        tree = AVLTree()
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)  # 触发 RR
        
        self.assertTrue(tree.is_valid_avl())
        self.assertEqual(tree.root.key, 20)
    
    def test_lr_rotation(self):
        """测试 LR 旋转"""
        tree = AVLTree()
        tree.insert(30)
        tree.insert(10)
        tree.insert(20)  # 触发 LR
        
        self.assertTrue(tree.is_valid_avl())
        self.assertEqual(tree.root.key, 20)
    
    def test_rl_rotation(self):
        """测试 RL 旋转"""
        tree = AVLTree()
        tree.insert(10)
        tree.insert(30)
        tree.insert(20)  # 触发 RL
        
        self.assertTrue(tree.is_valid_avl())
        self.assertEqual(tree.root.key, 20)
    
    def test_height_bound(self):
        """测试高度界限"""
        tree = AVLTree()
        n = 100
        
        for i in range(n):
            tree.insert(i)
        
        # AVL 树高度不超过 1.44 * log2(n + 2)
        max_height = int(1.44 * math.log2(n + 2))
        self.assertLessEqual(tree.height, max_height + 1)


class TestAVLTreeUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_create_avl_tree(self):
        """测试创建 AVL 树"""
        tree = create_avl_tree([(10, "a"), (5, "b"), (15, "c")])
        
        self.assertEqual(tree.size, 3)
        self.assertEqual(tree.get_value(10), "a")
        self.assertTrue(tree.is_valid_avl())
    
    def test_from_sorted_list(self):
        """测试从有序列表构建"""
        keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        values = [str(k) for k in keys]
        
        tree = from_sorted_list(keys, values)
        
        self.assertEqual(tree.size, len(keys))
        self.assertEqual(tree.height, math.ceil(math.log2(len(keys) + 1)))
        self.assertTrue(tree.is_valid_avl())
    
    def test_merge_avl_trees(self):
        """测试合并 AVL 树"""
        tree1 = create_avl_tree([(1, "a"), (5, "b"), (10, "c")])
        tree2 = create_avl_tree([(2, "d"), (7, "e"), (15, "f")])
        
        merged = merge_avl_trees(tree1, tree2)
        
        self.assertEqual(merged.size, 6)
        self.assertTrue(merged.is_valid_avl())
        self.assertEqual(merged.to_list(), [1, 2, 5, 7, 10, 15])
    
    def test_split_avl_tree(self):
        """测试分割 AVL 树"""
        tree = create_avl_tree([(1, "a"), (5, "b"), (10, "c"), (15, "d"), (20, "e")])
        
        left, right = split_avl_tree(tree, 10)
        
        self.assertEqual(left.to_list(), [1, 5])
        self.assertEqual(right.to_list(), [10, 15, 20])
    
    def test_avl_tree_to_dict(self):
        """测试 AVL 树转字典"""
        tree = create_avl_tree([(10, "a"), (5, "b")])
        d = avl_tree_to_dict(tree)
        
        self.assertEqual(d, {10: "a", 5: "b"})
    
    def test_dict_to_avl_tree(self):
        """测试字典转 AVL 树"""
        d = {10: "a", 5: "b", 15: "c"}
        tree = dict_to_avl_tree(d)
        
        self.assertEqual(tree.size, 3)
        self.assertEqual(tree.get_value(10), "a")
    
    def test_find_common_elements(self):
        """测试找公共元素"""
        tree1 = create_avl_tree([(1, None), (5, None), (10, None)])
        tree2 = create_avl_tree([(5, None), (10, None), (15, None)])
        
        common = find_common_elements(tree1, tree2)
        self.assertEqual(common, [5, 10])
    
    def test_find_difference(self):
        """测试找差集"""
        tree1 = create_avl_tree([(1, None), (5, None), (10, None)])
        tree2 = create_avl_tree([(5, None), (10, None), (15, None)])
        
        diff1, diff2 = find_difference(tree1, tree2)
        self.assertEqual(diff1, [1])
        self.assertEqual(diff2, [15])
    
    def test_validate_avl_tree(self):
        """测试验证 AVL 树"""
        tree = create_avl_tree([(10, None), (5, None), (15, None)])
        
        valid, msg = validate_avl_tree(tree)
        self.assertTrue(valid)
        self.assertIn("valid", msg)
    
    def test_get_tree_statistics(self):
        """测试获取统计信息"""
        tree = create_avl_tree([(i, None) for i in range(1, 11)])
        
        stats = get_tree_statistics(tree)
        
        self.assertEqual(stats["size"], 10)
        self.assertGreater(stats["height"], 0)
        self.assertTrue(stats["is_balanced"])
        self.assertEqual(stats["min_key"], 1)
        self.assertEqual(stats["max_key"], 10)


class TestAVLTreeEdgeCases(unittest.TestCase):
    """测试边界值和特殊情况"""
    
    def test_empty_tree_operations(self):
        """测试空树操作"""
        tree = AVLTree()
        
        self.assertIsNone(tree.search(10))
        self.assertFalse(tree.contains(10))
        self.assertIsNone(tree.find_min())
        self.assertIsNone(tree.find_max())
        self.assertIsNone(tree.find_floor(10))
        self.assertIsNone(tree.find_ceiling(10))
        self.assertIsNone(tree.find_kth(1))
        self.assertEqual(tree.rank(10), 0)
        self.assertEqual(tree.delete_min(), None)
        self.assertEqual(tree.delete_max(), None)
    
    def test_single_node_tree(self):
        """测试单节点树"""
        tree = AVLTree()
        tree.insert(10)
        
        self.assertEqual(tree.size, 1)
        self.assertEqual(tree.height, 1)
        self.assertEqual(tree.find_min().key, 10)
        self.assertEqual(tree.find_max().key, 10)
        self.assertEqual(tree.find_kth(1).key, 10)
        self.assertEqual(tree.rank(10), 1)
    
    def test_large_tree(self):
        """测试大树"""
        tree = AVLTree()
        n = 1000
        
        for i in range(n):
            tree.insert(i)
        
        self.assertEqual(tree.size, n)
        self.assertTrue(tree.is_valid_avl())
        
        # 测试查找效率
        for i in [0, n // 2, n - 1]:
            self.assertTrue(tree.contains(i))
    
    def test_negative_keys(self):
        """测试负数键"""
        tree = AVLTree()
        keys = [-10, -5, 0, 5, 10]
        
        for key in keys:
            tree.insert(key)
        
        self.assertEqual(tree.to_list(), sorted(keys))
        self.assertEqual(tree.find_min().key, -10)
        self.assertEqual(tree.find_max().key, 10)
    
    def test_float_keys(self):
        """测试浮点数键"""
        tree = AVLTree()
        keys = [1.5, 2.3, 0.7, 3.1]
        
        for key in keys:
            tree.insert(key)
        
        self.assertEqual(tree.to_list(), sorted(keys))
    
    def test_string_keys(self):
        """测试字符串键"""
        tree = AVLTree()
        keys = ["apple", "banana", "cherry", "date"]
        
        for key in keys:
            tree.insert(key)
        
        self.assertEqual(tree.to_list(), sorted(keys))
    
    def test_mixed_types_separate_trees(self):
        """测试不同类型的键（分开的树）"""
        int_tree = AVLTree()
        str_tree = AVLTree()
        
        int_tree.insert(10)
        str_tree.insert("10")
        
        self.assertEqual(int_tree.size, 1)
        self.assertEqual(str_tree.size, 1)
    
    def test_random_insert_delete(self):
        """测试随机插入删除"""
        tree = AVLTree()
        keys = list(range(100))
        
        # 随机插入
        random.shuffle(keys)
        for key in keys:
            tree.insert(key)
            self.assertTrue(tree.is_valid_avl())
        
        # 随机删除
        random.shuffle(keys)
        for key in keys[:50]:
            tree.delete(key)
            self.assertTrue(tree.is_valid_avl())
        
        self.assertEqual(tree.size, 50)
    
    def test_duplicate_keys_operations(self):
        """测试重复键的操作"""
        tree = AVLTree(allow_duplicates=True)
        
        tree.insert(10)
        tree.insert(10)
        tree.insert(10)
        
        self.assertEqual(tree.size, 3)
        
        # 删除一个
        tree.delete(10)
        self.assertEqual(tree.size, 2)
    
    def test_extreme_values(self):
        """测试极值"""
        tree = AVLTree()
        
        # 大数值
        tree.insert(10**10)
        tree.insert(10**10 - 1)
        tree.insert(10**10 + 1)
        
        self.assertEqual(tree.size, 3)
        self.assertEqual(tree.find_min().key, 10**10 - 1)
        self.assertEqual(tree.find_max().key, 10**10 + 1)
    
    def test_sequential_insertions(self):
        """测试顺序插入"""
        tree = AVLTree()
        n = 100
        
        # 递增插入（最可能导致不平衡）
        for i in range(n):
            tree.insert(i)
            self.assertTrue(tree.is_valid_avl())
        
        # 递减插入
        tree.clear()
        for i in range(n - 1, -1, -1):
            tree.insert(i)
            self.assertTrue(tree.is_valid_avl())
    
    def test_range_query_edge_cases(self):
        """测试范围查询边界"""
        tree = AVLTree()
        keys = [1, 2, 3, 4, 5]
        for key in keys:
            tree.insert(key)
        
        # 超出范围
        self.assertEqual(tree.range_query(10, 20), [])
        self.assertEqual(tree.range_query(0, 0), [])
        
        # 部分超出
        self.assertEqual(tree.range_query(3, 10), [3, 4, 5])
        self.assertEqual(tree.range_query(0, 3), [1, 2, 3])
    
    def test_kth_element_edge_cases(self):
        """测试第 k 小边界"""
        tree = AVLTree()
        keys = [1, 2, 3]
        for key in keys:
            tree.insert(key)
        
        self.assertIsNone(tree.find_kth(0))
        self.assertIsNone(tree.find_kth(4))
        self.assertEqual(tree.find_kth(1).key, 1)
        self.assertEqual(tree.find_kth(3).key, 3)


class TestAVLTreePerformance(unittest.TestCase):
    """测试性能相关"""
    
    def test_large_scale_operations(self):
        """测试大规模操作"""
        tree = AVLTree()
        n = 500
        
        # 插入
        for i in range(n):
            tree.insert(i)
        
        self.assertEqual(tree.size, n)
        
        # 查找
        for i in range(n):
            self.assertTrue(tree.contains(i))
        
        # 删除一半
        for i in range(n // 2):
            tree.delete(i)
        
        self.assertEqual(tree.size, n // 2)
        self.assertTrue(tree.is_valid_avl())
    
    def test_bulk_operations(self):
        """测试批量操作"""
        tree = AVLTree()
        items = [(i, f"v{i}") for i in range(100)]
        
        count = tree.bulk_insert(items)
        self.assertEqual(count, 100)
        self.assertEqual(tree.size, 100)
    
    def test_from_sorted_list_efficiency(self):
        """测试有序构建效率"""
        keys = list(range(100))
        tree = from_sorted_list(keys)
        
        # 有序构建应该更平衡
        self.assertTrue(tree.is_valid_avl())
        self.assertLessEqual(tree.height, math.ceil(math.log2(len(keys) + 1)) + 1)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestAVLNode,
        TestAVLTreeBasic,
        TestAVLTreeSearch,
        TestAVLTreeDelete,
        TestAVLTreeTraversal,
        TestAVLTreeRangeQuery,
        TestAVLTreeConversion,
        TestAVLTreeOtherOperations,
        TestAVLTreeBalancing,
        TestAVLTreeUtilityFunctions,
        TestAVLTreeEdgeCases,
        TestAVLTreePerformance,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.2f}%")
    
    if result.failures:
        print("\nFailures:")
        for test, trace in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\nErrors:")
        for test, trace in result.errors:
            print(f"  - {test}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)