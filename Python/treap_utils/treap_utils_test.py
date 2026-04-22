"""
Treap 工具模块测试
"""

import unittest
import random
from mod import Treap, ImplicitTreap, create_treap, create_implicit_treap


class TestTreap(unittest.TestCase):
    """Treap 基础测试"""
    
    def test_empty_treap(self):
        """测试空 Treap"""
        treap = Treap()
        self.assertTrue(treap.is_empty())
        self.assertEqual(len(treap), 0)
        self.assertIsNone(treap.get_min())
        self.assertIsNone(treap.get_max())
    
    def test_insert_single(self):
        """测试单个插入"""
        treap = Treap()
        treap.insert(5)
        self.assertEqual(len(treap), 1)
        self.assertEqual(treap.get_min(), 5)
        self.assertEqual(treap.get_max(), 5)
        self.assertTrue(treap.contains(5))
    
    def test_insert_multiple(self):
        """测试多个插入"""
        treap = Treap()
        keys = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        for k in keys:
            treap.insert(k)
        
        self.assertEqual(len(treap), 9)
        self.assertEqual(treap.get_min(), 1)
        self.assertEqual(treap.get_max(), 9)
        self.assertEqual(treap.to_sorted_list(), sorted(keys))
    
    def test_insert_duplicates(self):
        """测试重复元素"""
        treap = Treap()
        keys = [5, 3, 5, 3, 5, 3, 3, 5]
        for k in keys:
            treap.insert(k)
        
        self.assertEqual(len(treap), 8)
        self.assertEqual(treap.search(5), 4)
        self.assertEqual(treap.search(3), 4)
        self.assertEqual(treap.to_sorted_list(), sorted(keys))
    
    def test_delete_single(self):
        """测试单个删除"""
        treap = Treap([5])
        self.assertTrue(treap.delete(5))
        self.assertEqual(len(treap), 0)
        self.assertFalse(treap.contains(5))
    
    def test_delete_not_found(self):
        """测试删除不存在的元素"""
        treap = Treap([1, 2, 3])
        self.assertFalse(treap.delete(999))
        self.assertEqual(len(treap), 3)
    
    def test_delete_multiple(self):
        """测试多个删除"""
        keys = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        treap = Treap(keys)
        
        random.shuffle(keys)
        for k in keys:
            self.assertTrue(treap.delete(k), f"Failed to delete {k}")
        
        self.assertEqual(len(treap), 0)
    
    def test_delete_duplicates(self):
        """测试删除重复元素"""
        treap = Treap([5, 5, 5, 5])
        self.assertEqual(len(treap), 4)
        
        self.assertTrue(treap.delete(5))
        self.assertEqual(len(treap), 3)
        self.assertEqual(treap.search(5), 3)
        
        self.assertTrue(treap.delete(5))
        self.assertTrue(treap.delete(5))
        self.assertTrue(treap.delete(5))
        
        self.assertEqual(len(treap), 0)
        self.assertFalse(treap.contains(5))
    
    def test_search(self):
        """测试查找"""
        treap = Treap([1, 2, 3, 4, 5])
        self.assertEqual(treap.search(3), 1)
        self.assertEqual(treap.search(999), 0)
        self.assertTrue(treap.contains(3))
        self.assertFalse(treap.contains(999))
    
    def test_min_max(self):
        """测试最小最大值"""
        treap = Treap([5, 2, 8, 1, 9, 3, 7])
        self.assertEqual(treap.get_min(), 1)
        self.assertEqual(treap.get_max(), 9)
    
    def test_kth_smallest(self):
        """测试第 k 小元素"""
        treap = Treap([5, 2, 8, 1, 9, 3, 7, 4, 6])
        
        sorted_keys = sorted([5, 2, 8, 1, 9, 3, 7, 4, 6])
        for i, expected in enumerate(sorted_keys, 1):
            self.assertEqual(treap.kth_smallest(i), expected, f"Failed at k={i}")
        
        self.assertIsNone(treap.kth_smallest(0))
        self.assertIsNone(treap.kth_smallest(100))
    
    def test_rank(self):
        """测试排名"""
        treap = Treap([1, 2, 3, 4, 5])
        
        self.assertEqual(treap.rank(1), 1)
        self.assertEqual(treap.rank(3), 3)
        self.assertEqual(treap.rank(5), 5)
        self.assertEqual(treap.rank(0), 1)  # 应该插入的位置
        self.assertEqual(treap.rank(6), 6)
    
    def test_predecessor(self):
        """测试前驱"""
        treap = Treap([1, 3, 5, 7, 9])
        
        self.assertEqual(treap.predecessor(5), 3)
        self.assertEqual(treap.predecessor(3), 1)
        self.assertEqual(treap.predecessor(1), None)
        self.assertEqual(treap.predecessor(4), 3)
        self.assertEqual(treap.predecessor(10), 9)
    
    def test_successor(self):
        """测试后继"""
        treap = Treap([1, 3, 5, 7, 9])
        
        self.assertEqual(treap.successor(5), 7)
        self.assertEqual(treap.successor(7), 9)
        self.assertEqual(treap.successor(9), None)
        self.assertEqual(treap.successor(4), 5)
        self.assertEqual(treap.successor(0), 1)
    
    def test_count_range(self):
        """测试区间计数"""
        treap = Treap([1, 2, 3, 4, 5, 6, 7, 8, 9])
        
        self.assertEqual(treap.count_range(1, 9), 9)
        self.assertEqual(treap.count_range(3, 7), 5)
        self.assertEqual(treap.count_range(10, 20), 0)
        self.assertEqual(treap.count_range(2.5, 5.5), 3)
    
    def test_range_query(self):
        """测试区间查询"""
        treap = Treap([1, 2, 3, 4, 5, 6, 7, 8, 9])
        
        self.assertEqual(treap.range_query(1, 9), [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(treap.range_query(3, 7), [3, 4, 5, 6, 7])
        self.assertEqual(treap.range_query(10, 20), [])
    
    def test_range_query_with_duplicates(self):
        """测试带重复元素的区间查询"""
        treap = Treap([1, 2, 2, 3, 3, 3, 4, 5])
        
        self.assertEqual(treap.range_query(2, 4), [2, 2, 3, 3, 3, 4])
    
    def test_split(self):
        """测试分裂"""
        treap = Treap([1, 2, 3, 4, 5, 6, 7, 8, 9])
        
        left, right = treap.split(5)
        
        self.assertEqual(left.to_sorted_list(), [1, 2, 3, 4])
        self.assertEqual(right.to_sorted_list(), [5, 6, 7, 8, 9])
    
    def test_merge(self):
        """测试合并"""
        treap1 = Treap([1, 2, 3])
        treap2 = Treap([4, 5, 6])
        
        merged = treap1.merge(treap2)
        
        self.assertEqual(merged.to_sorted_list(), [1, 2, 3, 4, 5, 6])
    
    def test_iteration(self):
        """测试迭代"""
        treap = Treap([3, 1, 4, 1, 5, 9, 2, 6])
        result = list(treap)
        self.assertEqual(result, sorted([3, 1, 4, 1, 5, 9, 2, 6]))
    
    def test_clear(self):
        """测试清空"""
        treap = Treap([1, 2, 3, 4, 5])
        treap.clear()
        
        self.assertTrue(treap.is_empty())
        self.assertEqual(len(treap), 0)
    
    def test_height(self):
        """测试高度"""
        treap = Treap()
        self.assertEqual(treap.get_height(), 0)
        
        treap.insert(1)
        self.assertEqual(treap.get_height(), 1)
        
        # 大量插入后高度应该接近 log(n)
        for i in range(2, 1001):
            treap.insert(i)
        
        height = treap.get_height()
        import math
        expected_height = math.log2(1000) * 2  # 期望高度约为 2*log(n)
        self.assertLess(height, expected_height * 2)
    
    def test_custom_key_function(self):
        """测试自定义键函数"""
        # 按字符串长度排序（相同长度按原始字符串排序）
        treap = Treap(key_func=len)
        words = ["apple", "pear", "banana", "kiwi", "orange"]
        for w in words:
            treap.insert(w)
        
        # 长度: apple(5), pear(4), banana(6), kiwi(4), orange(6)
        # 按长度排序，相同长度按原始字符串字典序排序
        result = treap.to_sorted_list()
        self.assertEqual(len(result), 5)
        # kiwi(4) < pear(4) 按长度，apple(5) 单独，banana(6) < orange(6)
        self.assertEqual(result[0], "kiwi")  # 长度 4
        self.assertEqual(result[1], "pear")  # 长度 4
        self.assertEqual(result[2], "apple") # 长度 5
    
    def test_string_keys(self):
        """测试字符串键"""
        treap = Treap(["banana", "apple", "cherry", "date"])
        
        self.assertEqual(treap.get_min(), "apple")
        self.assertEqual(treap.get_max(), "date")
        self.assertTrue(treap.contains("cherry"))
        self.assertFalse(treap.contains("grape"))
    
    def test_large_scale_operations(self):
        """测试大规模操作"""
        treap = Treap()
        n = 1000
        
        # 插入
        keys = list(range(n))
        random.shuffle(keys)
        for k in keys:
            treap.insert(k)
        
        self.assertEqual(len(treap), n)
        
        # 查找
        for k in range(n):
            self.assertTrue(treap.contains(k))
        
        # 排序
        self.assertEqual(treap.to_sorted_list(), list(range(n)))
        
        # 删除一半
        for k in range(0, n, 2):
            self.assertTrue(treap.delete(k))
        
        self.assertEqual(len(treap), n // 2)
        
        # 验证剩余元素
        for k in range(1, n, 2):
            self.assertTrue(treap.contains(k))


class TestImplicitTreap(unittest.TestCase):
    """隐式 Treap 测试"""
    
    def test_empty(self):
        """测试空序列"""
        treap = ImplicitTreap()
        self.assertEqual(len(treap), 0)
    
    def test_init_with_list(self):
        """测试用列表初始化"""
        treap = ImplicitTreap([1, 2, 3, 4, 5])
        self.assertEqual(len(treap), 5)
        self.assertEqual(treap.to_list(), [1, 2, 3, 4, 5])
    
    def test_insert_at(self):
        """测试位置插入"""
        treap = ImplicitTreap()
        
        treap.insert_at(0, 1)  # [1]
        treap.insert_at(1, 3)  # [1, 3]
        treap.insert_at(1, 2)  # [1, 2, 3]
        
        self.assertEqual(treap.to_list(), [1, 2, 3])
    
    def test_delete_at(self):
        """测试位置删除"""
        treap = ImplicitTreap([1, 2, 3, 4, 5])
        
        self.assertEqual(treap.delete_at(0), 1)  # [2, 3, 4, 5]
        self.assertEqual(treap.delete_at(2), 4)  # [2, 3, 5]
        self.assertEqual(treap.to_list(), [2, 3, 5])
    
    def test_get_at(self):
        """测试位置访问"""
        treap = ImplicitTreap([10, 20, 30, 40, 50])
        
        self.assertEqual(treap.get_at(0), 10)
        self.assertEqual(treap.get_at(2), 30)
        self.assertEqual(treap.get_at(4), 50)
    
    def test_set_at(self):
        """测试位置设置"""
        treap = ImplicitTreap([1, 2, 3, 4, 5])
        
        treap.set_at(0, 100)
        treap.set_at(4, 500)
        
        self.assertEqual(treap.to_list(), [100, 2, 3, 4, 500])
    
    def test_indexing(self):
        """测试索引访问"""
        treap = ImplicitTreap([10, 20, 30])
        
        self.assertEqual(treap[0], 10)
        self.assertEqual(treap[1], 20)
        self.assertEqual(treap[2], 30)
        
        treap[1] = 25
        self.assertEqual(treap[1], 25)
    
    def test_index_out_of_range(self):
        """测试索引越界"""
        treap = ImplicitTreap([1, 2, 3])
        
        with self.assertRaises(IndexError):
            treap.get_at(5)
        
        with self.assertRaises(IndexError):
            treap.delete_at(-1)
    
    def test_reverse_range(self):
        """测试区间反转"""
        treap = ImplicitTreap([1, 2, 3, 4, 5])
        
        treap.reverse_range(1, 4)  # 反转 [1, 4) -> [2, 3, 4] -> [4, 3, 2]
        self.assertEqual(treap.to_list(), [1, 4, 3, 2, 5])
    
    def test_reverse_full(self):
        """测试完全反转"""
        treap = ImplicitTreap([1, 2, 3, 4, 5])
        
        treap.reverse_range(0, 5)
        self.assertEqual(treap.to_list(), [5, 4, 3, 2, 1])
    
    def test_to_list(self):
        """测试转换为列表"""
        treap = ImplicitTreap([5, 4, 3, 2, 1])
        self.assertEqual(treap.to_list(), [5, 4, 3, 2, 1])
    
    def test_large_scale(self):
        """测试大规模操作"""
        treap = ImplicitTreap()
        n = 100
        
        # 顺序插入
        for i in range(n):
            treap.insert_at(i, i)
        
        self.assertEqual(len(treap), n)
        
        # 验证顺序
        for i in range(n):
            self.assertEqual(treap.get_at(i), i)


class TestTreapPerformance(unittest.TestCase):
    """Treap 性能测试"""
    
    def test_sequential_insert(self):
        """测试顺序插入"""
        treap = Treap()
        n = 1000
        
        for i in range(n):
            treap.insert(i)
        
        self.assertEqual(len(treap), n)
        self.assertEqual(treap.get_height() < 50, True)
    
    def test_random_insert_delete(self):
        """测试随机插入删除"""
        treap = Treap()
        n = 500
        
        keys = list(range(n))
        random.shuffle(keys)
        
        # 插入
        for k in keys:
            treap.insert(k)
        
        self.assertEqual(len(treap), n)
        
        # 随机删除
        random.shuffle(keys)
        for k in keys[:n//2]:
            treap.delete(k)
        
        self.assertEqual(len(treap), n - n//2)
    
    def test_range_query_performance(self):
        """测试区间查询性能"""
        treap = Treap()
        n = 1000
        
        for i in range(n):
            treap.insert(i)
        
        # 多次区间查询
        for _ in range(100):
            low = random.randint(0, n//2)
            high = low + random.randint(0, n//2)
            count = treap.count_range(low, high)
            self.assertGreaterEqual(count, 0)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_create_treap(self):
        """测试 create_treap 函数"""
        treap = create_treap([3, 1, 4, 1, 5])
        self.assertIsInstance(treap, Treap)
        self.assertEqual(treap.to_sorted_list(), [1, 1, 3, 4, 5])
    
    def test_create_implicit_treap(self):
        """测试 create_implicit_treap 函数"""
        treap = create_implicit_treap([1, 2, 3])
        self.assertIsInstance(treap, ImplicitTreap)
        self.assertEqual(treap.to_list(), [1, 2, 3])


if __name__ == '__main__':
    unittest.main(verbosity=2)