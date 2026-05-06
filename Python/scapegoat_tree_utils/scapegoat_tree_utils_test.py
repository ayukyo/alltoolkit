"""
替罪羊树测试模块
"""

import unittest
import random
from typing import List
from mod import ScapegoatTree, ScapegoatTreeSet, ScapegoatTreeMultiSet


class TestScapegoatTree(unittest.TestCase):
    """替罪羊树基本功能测试"""
    
    def test_insert_and_contains(self):
        """测试插入和查找"""
        tree = ScapegoatTree[int]()
        
        # 插入元素
        self.assertTrue(tree.insert(5))
        self.assertTrue(tree.insert(3))
        self.assertTrue(tree.insert(7))
        
        # 重复插入
        self.assertFalse(tree.insert(5))
        
        # 查找元素
        self.assertTrue(tree.contains(5))
        self.assertTrue(tree.contains(3))
        self.assertTrue(tree.contains(7))
        self.assertFalse(tree.contains(1))
        self.assertFalse(tree.contains(9))
    
    def test_delete(self):
        """测试删除"""
        tree = ScapegoatTree[int]()
        
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        
        # 删除叶子节点
        self.assertTrue(tree.delete(3))
        self.assertFalse(tree.contains(3))
        self.assertEqual(tree.size, 2)
        
        # 删除不存在的元素
        self.assertFalse(tree.delete(10))
        self.assertEqual(tree.size, 2)
        
        # 删除根节点
        self.assertTrue(tree.delete(5))
        self.assertFalse(tree.contains(5))
        self.assertEqual(tree.size, 1)
    
    def test_delete_with_two_children(self):
        """测试删除有两个子节点的节点"""
        tree = ScapegoatTree[int]()
        
        # 构建树
        #       5
        #      / \
        #     3   7
        #    / \   \
        #   1   4   8
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        tree.insert(1)
        tree.insert(4)
        tree.insert(8)
        
        # 删除有两个子节点的节点
        self.assertTrue(tree.delete(3))
        self.assertFalse(tree.contains(3))
        self.assertEqual(tree.size, 5)
        
        # 检查中序遍历仍然有序
        result = list(tree.inorder())
        self.assertEqual(result, sorted(result))
    
    def test_min_max(self):
        """测试最小最大值"""
        tree = ScapegoatTree[int]()
        
        self.assertIsNone(tree.min())
        self.assertIsNone(tree.max())
        
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        tree.insert(1)
        tree.insert(9)
        
        self.assertEqual(tree.min(), 1)
        self.assertEqual(tree.max(), 9)
    
    def test_predecessor_successor(self):
        """测试前驱和后继"""
        tree = ScapegoatTree[int]()
        
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        tree.insert(1)
        tree.insert(9)
        
        self.assertEqual(tree.predecessor(5), 3)
        self.assertEqual(tree.successor(5), 7)
        self.assertEqual(tree.predecessor(1), None)
        self.assertEqual(tree.successor(9), None)
    
    def test_range_query(self):
        """测试范围查询"""
        tree = ScapegoatTree[int]()
        
        for i in range(1, 11):
            tree.insert(i)
        
        result = tree.range_query(3, 7)
        self.assertEqual(sorted(result), [3, 4, 5, 6, 7])
        
        result = tree.range_query(1, 10)
        self.assertEqual(sorted(result), list(range(1, 11)))
        
        result = tree.range_query(0, 100)
        self.assertEqual(sorted(result), list(range(1, 11)))
    
    def test_kth_smallest_largest(self):
        """测试第 k 小/大元素"""
        tree = ScapegoatTree[int]()
        
        for i in [5, 3, 7, 1, 9, 2, 8, 4, 6]:
            tree.insert(i)
        
        for k in range(1, 10):
            self.assertEqual(tree.kth_smallest(k), k)
            self.assertEqual(tree.kth_largest(k), 10 - k)
        
        self.assertIsNone(tree.kth_smallest(0))
        self.assertIsNone(tree.kth_smallest(10))
        self.assertIsNone(tree.kth_largest(0))
        self.assertIsNone(tree.kth_largest(10))
    
    def test_rank(self):
        """测试排名"""
        tree = ScapegoatTree[int]()
        
        for i in [5, 3, 7, 1, 9]:
            tree.insert(i)
        
        self.assertEqual(tree.rank(1), 1)
        self.assertEqual(tree.rank(3), 2)
        self.assertEqual(tree.rank(5), 3)
        self.assertEqual(tree.rank(7), 4)
        self.assertEqual(tree.rank(9), 5)
        self.assertEqual(tree.rank(10), 0)  # 不存在
    
    def test_count_less_greater_than(self):
        """测试小于/大于指定值的元素计数"""
        tree = ScapegoatTree[int]()
        
        for i in range(1, 11):
            tree.insert(i)
        
        self.assertEqual(tree.count_less_than(5), 4)
        self.assertEqual(tree.count_less_than(1), 0)
        self.assertEqual(tree.count_less_than(10), 9)
        
        self.assertEqual(tree.count_greater_than(5), 5)
        self.assertEqual(tree.count_greater_than(9), 1)
        self.assertEqual(tree.count_greater_than(10), 0)
    
    def test_traversals(self):
        """测试遍历"""
        tree = ScapegoatTree[int]()
        
        # 构建简单的 BST
        tree.insert(4)
        tree.insert(2)
        tree.insert(6)
        tree.insert(1)
        tree.insert(3)
        tree.insert(5)
        tree.insert(7)
        
        # 中序遍历应该是有序的
        inorder = list(tree.inorder())
        self.assertEqual(inorder, [1, 2, 3, 4, 5, 6, 7])
        
        # 前序遍历
        preorder = list(tree.preorder())
        self.assertIn(preorder[0], [4, 5, 6])  # 根节点可能变化
        
        # 后序遍历
        postorder = list(tree.postorder())
        self.assertEqual(len(postorder), 7)
    
    def test_custom_comparator(self):
        """测试自定义比较器"""
        # 使用自定义比较器创建降序树
        tree = ScapegoatTree[int](comparator=lambda a, b: b - a)
        
        tree.insert(1)
        tree.insert(2)
        tree.insert(3)
        
        # 在降序树中，min 返回最大值
        result = list(tree.inorder())
        self.assertEqual(result, [3, 2, 1])
    
    def test_string_elements(self):
        """测试字符串元素"""
        tree = ScapegoatTree[str]()
        
        tree.insert("banana")
        tree.insert("apple")
        tree.insert("cherry")
        
        self.assertEqual(tree.min(), "apple")
        self.assertEqual(tree.max(), "cherry")
        self.assertEqual(list(tree.inorder()), ["apple", "banana", "cherry"])
    
    def test_large_scale(self):
        """测试大规模数据"""
        tree = ScapegoatTree[int]()
        n = 1000
        
        # 插入随机数据
        data = list(range(n))
        random.shuffle(data)
        
        for x in data:
            tree.insert(x)
        
        self.assertEqual(tree.size, n)
        self.assertTrue(tree.is_balanced())
        
        # 中序遍历应该有序
        inorder = list(tree.inorder())
        self.assertEqual(inorder, list(range(n)))
        
        # 删除一半
        for x in range(n // 2):
            tree.delete(x)
        
        self.assertEqual(tree.size, n // 2)
        self.assertTrue(tree.is_balanced())
    
    def test_alpha_validation(self):
        """测试 alpha 参数验证"""
        with self.assertRaises(ValueError):
            ScapegoatTree[int](alpha=0.5)
        
        with self.assertRaises(ValueError):
            ScapegoatTree[int](alpha=1.0)
        
        with self.assertRaises(ValueError):
            ScapegoatTree[int](alpha=0.3)
        
        # 有效值
        tree = ScapegoatTree[int](alpha=0.6)
        self.assertEqual(tree.alpha, 0.6)
    
    def test_clear(self):
        """测试清空"""
        tree = ScapegoatTree[int]()
        
        for i in range(10):
            tree.insert(i)
        
        self.assertEqual(tree.size, 10)
        
        tree.clear()
        
        self.assertEqual(tree.size, 0)
        self.assertTrue(tree.is_empty)
        self.assertIsNone(tree.min())
        self.assertIsNone(tree.max())
    
    def test_to_list(self):
        """测试转换为列表"""
        tree = ScapegoatTree[int]()
        
        for i in [5, 3, 7, 1, 9]:
            tree.insert(i)
        
        self.assertEqual(tree.to_list(), [1, 3, 5, 7, 9])
    
    def test_magic_methods(self):
        """测试魔术方法"""
        tree = ScapegoatTree[int]()
        
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        
        self.assertEqual(len(tree), 3)
        self.assertIn(5, tree)
        self.assertNotIn(10, tree)
        
        # 迭代
        items = list(tree)
        self.assertEqual(sorted(items), [3, 5, 7])


class TestScapegoatTreeSet(unittest.TestCase):
    """替罪羊树集合测试"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        s = ScapegoatTreeSet[int]()
        
        self.assertTrue(s.add(1))
        self.assertTrue(s.add(2))
        self.assertTrue(s.add(3))
        self.assertFalse(s.add(1))  # 重复
        
        self.assertEqual(len(s), 3)
        self.assertIn(1, s)
        self.assertIn(2, s)
        self.assertIn(3, s)
        self.assertNotIn(4, s)
    
    def test_remove(self):
        """测试删除"""
        s = ScapegoatTreeSet[int]()
        
        s.add(1)
        s.add(2)
        s.add(3)
        
        self.assertTrue(s.remove(2))
        self.assertFalse(s.contains(2))
        self.assertEqual(len(s), 2)
        
        self.assertFalse(s.remove(10))
        self.assertEqual(len(s), 2)
    
    def test_discard(self):
        """测试丢弃"""
        s = ScapegoatTreeSet[int]()
        
        s.add(1)
        s.add(2)
        
        self.assertTrue(s.discard(1))
        self.assertFalse(s.contains(1))
        
        self.assertFalse(s.discard(10))  # 不存在，但不报错
    
    def test_order_operations(self):
        """测试顺序相关操作"""
        s = ScapegoatTreeSet[int]()
        
        for i in [5, 3, 7, 1, 9]:
            s.add(i)
        
        self.assertEqual(s.min(), 1)
        self.assertEqual(s.max(), 9)
        self.assertEqual(s.predecessor(5), 3)
        self.assertEqual(s.successor(5), 7)
        self.assertEqual(s.kth_smallest(3), 5)
        self.assertEqual(s.kth_largest(1), 9)
        self.assertEqual(s.rank(5), 3)
    
    def test_range_query(self):
        """测试范围查询"""
        s = ScapegoatTreeSet[int]()
        
        for i in range(1, 11):
            s.add(i)
        
        result = s.range_query(3, 7)
        self.assertEqual(sorted(result), [3, 4, 5, 6, 7])
    
    def test_iteration(self):
        """测试迭代"""
        s = ScapegoatTreeSet[int]()
        
        for i in [3, 1, 2]:
            s.add(i)
        
        self.assertEqual(list(s), [1, 2, 3])
    
    def test_clear(self):
        """测试清空"""
        s = ScapegoatTreeSet[int]()
        
        for i in range(5):
            s.add(i)
        
        s.clear()
        
        self.assertEqual(len(s), 0)
        self.assertTrue(s.is_empty)
    
    def test_string_representation(self):
        """测试字符串表示"""
        s = ScapegoatTreeSet[int]()
        
        for i in [1, 2, 3]:
            s.add(i)
        
        self.assertIn("ScapegoatTreeSet", repr(s))
        self.assertIn("1", str(s))


class TestScapegoatTreeMultiSet(unittest.TestCase):
    """替罪羊树多重集测试"""
    
    def test_add_and_count(self):
        """测试添加和计数"""
        ms = ScapegoatTreeMultiSet[str]()
        
        ms.add("apple")
        ms.add("apple")
        ms.add("banana")
        
        self.assertEqual(ms.count("apple"), 2)
        self.assertEqual(ms.count("banana"), 1)
        self.assertEqual(ms.count("cherry"), 0)
    
    def test_add_with_count(self):
        """测试批量添加"""
        ms = ScapegoatTreeMultiSet[int]()
        
        ms.add(1, 5)
        ms.add(2, 3)
        
        self.assertEqual(ms.count(1), 5)
        self.assertEqual(ms.count(2), 3)
    
    def test_remove(self):
        """测试删除"""
        ms = ScapegoatTreeMultiSet[int]()
        
        ms.add(1, 5)
        
        self.assertEqual(ms.remove(1, 2), 2)
        self.assertEqual(ms.count(1), 3)
        
        self.assertEqual(ms.remove(1, 10), 3)  # 只剩3个
        self.assertEqual(ms.count(1), 0)
        
        self.assertEqual(ms.remove(1), 0)  # 不存在
    
    def test_size(self):
        """测试大小"""
        ms = ScapegoatTreeMultiSet[int]()
        
        self.assertEqual(len(ms), 0)
        
        ms.add(1, 5)
        ms.add(2, 3)
        
        self.assertEqual(len(ms), 8)
        self.assertEqual(ms.size, 8)
        self.assertEqual(ms.unique_size, 2)
    
    def test_contains(self):
        """测试包含"""
        ms = ScapegoatTreeMultiSet[str]()
        
        self.assertNotIn("apple", ms)
        
        ms.add("apple")
        self.assertIn("apple", ms)
    
    def test_min_max(self):
        """测试最小最大值"""
        ms = ScapegoatTreeMultiSet[int]()
        
        self.assertIsNone(ms.min())
        self.assertIsNone(ms.max())
        
        ms.add(5, 2)
        ms.add(3, 1)
        ms.add(7, 3)
        
        self.assertEqual(ms.min(), 3)
        self.assertEqual(ms.max(), 7)
    
    def test_unique_elements(self):
        """测试不重复元素"""
        ms = ScapegoatTreeMultiSet[int]()
        
        ms.add(1, 5)
        ms.add(2, 3)
        ms.add(3, 1)
        
        unique = ms.unique_elements()
        self.assertEqual(sorted(unique), [1, 2, 3])
    
    def test_to_list(self):
        """测试转换为列表"""
        ms = ScapegoatTreeMultiSet[int]()
        
        ms.add(1, 2)
        ms.add(2, 3)
        
        result = ms.to_list()
        self.assertEqual(sorted(result), [1, 1, 2, 2, 2])
    
    def test_clear(self):
        """测试清空"""
        ms = ScapegoatTreeMultiSet[int]()
        
        ms.add(1, 5)
        ms.add(2, 3)
        
        ms.clear()
        
        self.assertEqual(len(ms), 0)
        self.assertTrue(ms.is_empty)
    
    def test_string_elements(self):
        """测试字符串元素"""
        ms = ScapegoatTreeMultiSet[str]()
        
        ms.add("apple")
        ms.add("banana")
        ms.add("apple")
        
        self.assertEqual(ms.count("apple"), 2)
        self.assertEqual(ms.count("banana"), 1)


class TestScapegoatTreeBalance(unittest.TestCase):
    """替罪羊树平衡性测试"""
    
    def test_sequential_insert(self):
        """测试顺序插入后的平衡"""
        tree = ScapegoatTree[int]()
        
        # 顺序插入是最坏情况
        for i in range(100):
            tree.insert(i)
        
        self.assertEqual(tree.size, 100)
        self.assertTrue(tree.is_balanced())
        
        # 高度应该是对数级别的
        # 对于替罪羊树，高度应 <= log_{1/alpha}(n)
        import math
        max_height = math.log(tree.size, 1 / tree.alpha)
        self.assertLessEqual(tree.height, max_height + 1)
    
    def test_reverse_insert(self):
        """测试逆序插入后的平衡"""
        tree = ScapegoatTree[int]()
        
        for i in range(99, -1, -1):
            tree.insert(i)
        
        self.assertEqual(tree.size, 100)
        self.assertTrue(tree.is_balanced())
    
    def test_repeated_insert_delete(self):
        """测试反复插入删除后的平衡"""
        tree = ScapegoatTree[int]()
        
        # 插入
        for i in range(100):
            tree.insert(i)
        
        # 删除一半
        for i in range(0, 100, 2):
            tree.delete(i)
        
        self.assertTrue(tree.is_balanced())
        
        # 再插入一些
        for i in range(200, 250):
            tree.insert(i)
        
        self.assertTrue(tree.is_balanced())
    
    def test_different_alpha_values(self):
        """测试不同 alpha 值"""
        for alpha in [0.55, 0.6, 0.7, 0.8, 0.9]:
            tree = ScapegoatTree[int](alpha=alpha)
            
            for i in range(100):
                tree.insert(i)
            
            self.assertTrue(tree.is_balanced(), f"Failed for alpha={alpha}")
    
    def test_tree_structure_after_operations(self):
        """测试操作后树结构的正确性"""
        tree = ScapegoatTree[int]()
        
        # 随机插入
        data = list(range(100))
        random.shuffle(data)
        
        for x in data:
            tree.insert(x)
        
        # 验证中序遍历有序
        inorder = list(tree.inorder())
        self.assertEqual(inorder, list(range(100)))
        
        # 随机删除
        random.shuffle(data)
        for x in data[:50]:
            tree.delete(x)
        
        # 验证剩余元素仍然有序
        inorder = list(tree.inorder())
        self.assertEqual(inorder, sorted(inorder))


class TestScapegoatTreeEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_empty_tree(self):
        """测试空树"""
        tree = ScapegoatTree[int]()
        
        self.assertEqual(tree.size, 0)
        self.assertTrue(tree.is_empty)
        self.assertEqual(tree.height, 0)
        self.assertIsNone(tree.min())
        self.assertIsNone(tree.max())
        self.assertEqual(list(tree.inorder()), [])
        self.assertFalse(tree.contains(1))
        self.assertFalse(tree.delete(1))
    
    def test_single_element(self):
        """测试单个元素"""
        tree = ScapegoatTree[int]()
        
        tree.insert(42)
        
        self.assertEqual(tree.size, 1)
        self.assertEqual(tree.height, 1)
        self.assertEqual(tree.min(), 42)
        self.assertEqual(tree.max(), 42)
        self.assertTrue(tree.contains(42))
        self.assertEqual(tree.predecessor(42), None)
        self.assertEqual(tree.successor(42), None)
    
    def test_duplicate_operations(self):
        """测试重复操作"""
        tree = ScapegoatTree[int]()
        
        # 重复插入
        self.assertTrue(tree.insert(1))
        self.assertFalse(tree.insert(1))
        self.assertFalse(tree.insert(1))
        
        self.assertEqual(tree.size, 1)
        
        # 删除后重新插入
        self.assertTrue(tree.delete(1))
        self.assertEqual(tree.size, 0)
        self.assertTrue(tree.insert(1))
        self.assertEqual(tree.size, 1)
    
    def test_negative_numbers(self):
        """测试负数"""
        tree = ScapegoatTree[int]()
        
        for i in [-5, -3, 0, 3, 5]:
            tree.insert(i)
        
        self.assertEqual(tree.min(), -5)
        self.assertEqual(tree.max(), 5)
        self.assertEqual(list(tree.inorder()), [-5, -3, 0, 3, 5])
    
    def test_float_numbers(self):
        """测试浮点数"""
        tree = ScapegoatTree[float]()
        
        for i in [1.5, 2.7, 0.3, 3.14]:
            tree.insert(i)
        
        self.assertEqual(tree.min(), 0.3)
        self.assertEqual(tree.max(), 3.14)
    
    def test_tuple_keys(self):
        """测试元组键"""
        tree = ScapegoatTree[tuple]()
        
        tree.insert((1, 2))
        tree.insert((1, 3))
        tree.insert((2, 1))
        
        self.assertEqual(tree.min(), (1, 2))
        self.assertEqual(tree.max(), (2, 1))
        self.assertTrue(tree.contains((1, 3)))
    
    def test_large_range_query(self):
        """测试大范围查询"""
        tree = ScapegoatTree[int]()
        
        for i in range(1000):
            tree.insert(i)
        
        result = tree.range_query(100, 899)
        self.assertEqual(len(result), 800)
        self.assertEqual(min(result), 100)
        self.assertEqual(max(result), 899)


if __name__ == '__main__':
    unittest.main()