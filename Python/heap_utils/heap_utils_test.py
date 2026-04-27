"""
堆工具集测试 (Heap Utilities Tests)
=====================================

全面测试 MinHeap、MaxHeap、MinMaxHeap、PriorityQueue 和工具函数。

运行方式：
    python -m pytest heap_utils_test.py -v
    python heap_utils_test.py

作者: AllToolkit
日期: 2026-04-17
"""

import sys
import os
import unittest
import random
from typing import List

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    HeapItem, MinHeap, MaxHeap, MinMaxHeap, PriorityQueue,
    heap_sort, nth_smallest, nth_largest, k_smallest, k_largest,
    merge_sorted_lists, is_valid_heap, heapify, median_of_data
)


class TestHeapItem(unittest.TestCase):
    """测试 HeapItem 类"""
    
    def test_basic_comparison(self):
        """测试基本比较"""
        item1 = HeapItem(1, "low")
        item2 = HeapItem(2, "high")
        
        self.assertTrue(item1 < item2)
        self.assertTrue(item2 > item1)
        self.assertTrue(item1 == HeapItem(1, "other"))
        self.assertTrue(item1 <= item2)
    
    def test_equal_priority(self):
        """测试相同优先级"""
        item1 = HeapItem(1, "first")
        item2 = HeapItem(1, "second")
        
        self.assertEqual(item1, item2)
    
    def test_repr(self):
        """测试字符串表示"""
        item = HeapItem(3.14, "pi")
        self.assertIn("3.14", repr(item))
        self.assertIn("pi", repr(item))


class TestMinHeap(unittest.TestCase):
    """测试最小堆"""
    
    def test_push_pop(self):
        """测试基本入队出队"""
        heap = MinHeap[int]()
        heap.push(3)
        heap.push(1)
        heap.push(4)
        heap.push(1)
        heap.push(5)
        
        self.assertEqual(heap.pop(), 1)
        self.assertEqual(heap.pop(), 1)
        self.assertEqual(heap.pop(), 3)
        self.assertEqual(heap.pop(), 4)
        self.assertEqual(heap.pop(), 5)
    
    def test_init_with_list(self):
        """测试使用列表初始化"""
        heap = MinHeap([5, 3, 1, 4, 2])
        
        result = list(heap)
        self.assertEqual(result, [1, 2, 3, 4, 5])
    
    def test_peek(self):
        """测试查看堆顶"""
        heap = MinHeap([3, 1, 2])
        
        self.assertEqual(heap.peek(), 1)
        self.assertEqual(len(heap), 3)  # peek 不移除元素
    
    def test_empty_operations(self):
        """测试空堆操作"""
        heap = MinHeap()
        
        self.assertEqual(len(heap), 0)
        self.assertFalse(heap)
        
        with self.assertRaises(IndexError):
            heap.pop()
        
        with self.assertRaises(IndexError):
            heap.peek()
    
    def test_replace(self):
        """测试替换堆顶"""
        heap = MinHeap([3, 1, 2])
        
        result = heap.replace(0)
        self.assertEqual(result, 1)
        self.assertEqual(heap.peek(), 0)
    
    def test_pushpop(self):
        """测试先入后出"""
        heap = MinHeap([3, 1, 2])
        
        result = heap.pushpop(0)
        self.assertEqual(result, 0)
        self.assertEqual(heap.peek(), 1)
    
    def test_key_function(self):
        """测试自定义比较键"""
        data = [{'name': 'a', 'score': 90}, 
                {'name': 'b', 'score': 70},
                {'name': 'c', 'score': 85}]
        heap = MinHeap(data, key=lambda x: x['score'])
        
        first = heap.pop()
        self.assertEqual(first['name'], 'b')
        self.assertEqual(first['score'], 70)
    
    def test_with_heap_items(self):
        """测试使用 HeapItem"""
        heap = MinHeap[HeapItem[str]]()
        heap.push(HeapItem(3, "low"))
        heap.push(HeapItem(1, "high"))
        heap.push(HeapItem(2, "medium"))
        
        result = heap.pop()
        self.assertEqual(result.value, "high")
        self.assertEqual(result.priority, 1)
    
    def test_update(self):
        """测试更新元素"""
        heap = MinHeap([5, 3, 1, 4, 2])
        heap.update(2, 0)  # 将索引2的元素（值为1）更新为0
        
        # 验证堆性质
        self.assertEqual(heap.peek(), 0)
    
    def test_to_list_sorted(self):
        """测试转换为排序列表"""
        heap = MinHeap([3, 1, 4, 1, 5])
        sorted_list = heap.to_list(sorted_=True)
        
        self.assertEqual(sorted_list, [1, 1, 3, 4, 5])
    
    def test_clear(self):
        """测试清空"""
        heap = MinHeap([1, 2, 3])
        heap.clear()
        
        self.assertEqual(len(heap), 0)
        self.assertFalse(heap)


class TestMaxHeap(unittest.TestCase):
    """测试最大堆"""
    
    def test_push_pop(self):
        """测试基本入队出队"""
        heap = MaxHeap[int]()
        heap.push(3)
        heap.push(1)
        heap.push(4)
        heap.push(1)
        heap.push(5)
        
        self.assertEqual(heap.pop(), 5)
        self.assertEqual(heap.pop(), 4)
        self.assertEqual(heap.pop(), 3)
        self.assertEqual(heap.pop(), 1)
        self.assertEqual(heap.pop(), 1)
    
    def test_init_with_list(self):
        """测试使用列表初始化"""
        heap = MaxHeap([1, 5, 2, 4, 3])
        
        result = list(heap)
        self.assertEqual(result, [5, 4, 3, 2, 1])
    
    def test_key_function(self):
        """测试自定义比较键"""
        data = [{'name': 'a', 'score': 90}, 
                {'name': 'b', 'score': 70},
                {'name': 'c', 'score': 85}]
        heap = MaxHeap(data, key=lambda x: x['score'])
        
        first = heap.pop()
        self.assertEqual(first['name'], 'a')
        self.assertEqual(first['score'], 90)


class TestMinMaxHeap(unittest.TestCase):
    """测试双端堆"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        heap = MinMaxHeap[int]()
        heap.push(3)
        heap.push(1)
        heap.push(4)
        heap.push(1)
        heap.push(5)
        
        self.assertEqual(heap.get_min(), 1)
        self.assertEqual(heap.get_max(), 5)
    
    def test_pop_min(self):
        """测试弹出最小元素"""
        heap = MinMaxHeap([3, 1, 4, 1, 5])
        
        self.assertEqual(heap.pop_min(), 1)
        self.assertEqual(heap.pop_min(), 1)
        self.assertEqual(heap.pop_min(), 3)
    
    def test_pop_max(self):
        """测试弹出最大元素"""
        heap = MinMaxHeap([3, 1, 4, 1, 5])
        
        self.assertEqual(heap.pop_max(), 5)
        self.assertEqual(heap.pop_max(), 4)
        self.assertEqual(heap.pop_max(), 3)
    
    def test_empty_operations(self):
        """测试空堆操作"""
        heap = MinMaxHeap()
        
        with self.assertRaises(IndexError):
            heap.get_min()
        
        with self.assertRaises(IndexError):
            heap.get_max()
    
    def test_single_element(self):
        """测试单个元素"""
        heap = MinMaxHeap([42])
        
        self.assertEqual(heap.get_min(), 42)
        self.assertEqual(heap.get_max(), 42)


class TestPriorityQueue(unittest.TestCase):
    """测试优先队列"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        pq = PriorityQueue[str]()
        pq.push("low", priority=3)
        pq.push("high", priority=1)
        pq.push("medium", priority=2)
        
        self.assertEqual(pq.pop(), "high")
        self.assertEqual(pq.pop(), "medium")
        self.assertEqual(pq.pop(), "low")
    
    def test_fifo_for_same_priority(self):
        """测试相同优先级时遵循FIFO"""
        pq = PriorityQueue[str]()
        pq.push("first", priority=1)
        pq.push("second", priority=1)
        pq.push("third", priority=1)
        
        self.assertEqual(pq.pop(), "first")
        self.assertEqual(pq.pop(), "second")
        self.assertEqual(pq.pop(), "third")
    
    def test_max_priority_queue(self):
        """测试最大优先队列"""
        pq = PriorityQueue[str](max_priority=True)
        pq.push("low", priority=1)
        pq.push("high", priority=3)
        pq.push("medium", priority=2)
        
        self.assertEqual(pq.pop(), "high")
        self.assertEqual(pq.pop(), "medium")
        self.assertEqual(pq.pop(), "low")
    
    def test_peek(self):
        """测试查看队首"""
        pq = PriorityQueue[int]()
        pq.push(1, priority=2)
        pq.push(2, priority=1)
        
        self.assertEqual(pq.peek(), 2)
        self.assertEqual(len(pq), 2)
    
    def test_empty_operations(self):
        """测试空队列操作"""
        pq = PriorityQueue()
        
        with self.assertRaises(IndexError):
            pq.pop()
        
        with self.assertRaises(IndexError):
            pq.peek()
    
    def test_clear(self):
        """测试清空"""
        pq = PriorityQueue()
        pq.push(1, priority=1)
        pq.push(2, priority=2)
        pq.clear()
        
        self.assertEqual(len(pq), 0)


class TestHeapSort(unittest.TestCase):
    """测试堆排序"""
    
    def test_sort_ascending(self):
        """测试升序排序"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = heap_sort(data)
        
        self.assertEqual(result, [1, 1, 2, 3, 4, 5, 6, 9])
    
    def test_sort_descending(self):
        """测试降序排序"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = heap_sort(data, reverse=True)
        
        self.assertEqual(result, [9, 6, 5, 4, 3, 2, 1, 1])
    
    def test_sort_with_key(self):
        """测试带键函数排序"""
        data = ['apple', 'pie', 'a', 'longword']
        result = heap_sort(data, key=len)
        
        self.assertEqual(result, ['a', 'pie', 'apple', 'longword'])
    
    def test_empty_list(self):
        """测试空列表"""
        self.assertEqual(heap_sort([]), [])
    
    def test_single_element(self):
        """测试单元素"""
        self.assertEqual(heap_sort([42]), [42])


class TestNthSmallest(unittest.TestCase):
    """测试第n小元素"""
    
    def test_basic(self):
        """测试基本功能"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        
        self.assertEqual(nth_smallest(data, 1), 1)
        self.assertEqual(nth_smallest(data, 2), 1)
        self.assertEqual(nth_smallest(data, 3), 2)
        self.assertEqual(nth_smallest(data, 8), 9)
    
    def test_with_key(self):
        """测试带键函数"""
        data = [{'v': 3}, {'v': 1}, {'v': 2}]
        result = nth_smallest(data, 1, key=lambda x: x['v'])
        self.assertEqual(result, {'v': 1})
    
    def test_invalid_n(self):
        """测试无效n值"""
        with self.assertRaises(ValueError):
            nth_smallest([1, 2, 3], 0)
        
        with self.assertRaises(ValueError):
            nth_smallest([1, 2, 3], 4)


class TestNthLargest(unittest.TestCase):
    """测试第n大元素"""
    
    def test_basic(self):
        """测试基本功能"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        
        self.assertEqual(nth_largest(data, 1), 9)
        self.assertEqual(nth_largest(data, 2), 6)
        self.assertEqual(nth_largest(data, 3), 5)


class TestKSmallest(unittest.TestCase):
    """测试最小的k个元素"""
    
    def test_basic(self):
        """测试基本功能"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = k_smallest(data, 3)
        
        self.assertEqual(result, [1, 1, 2])
    
    def test_k_larger_than_size(self):
        """测试k大于列表大小"""
        data = [3, 1, 2]
        result = k_smallest(data, 10)
        
        self.assertEqual(result, [1, 2, 3])
    
    def test_k_zero(self):
        """测试k为0"""
        self.assertEqual(k_smallest([1, 2, 3], 0), [])


class TestKLargest(unittest.TestCase):
    """测试最大的k个元素"""
    
    def test_basic(self):
        """测试基本功能"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = k_largest(data, 3)
        
        self.assertEqual(result, [9, 6, 5])


class TestMergeSortedLists(unittest.TestCase):
    """测试合并有序列表"""
    
    def test_basic(self):
        """测试基本功能"""
        result = merge_sorted_lists([1, 3, 5], [2, 4, 6], [0, 7])
        
        self.assertEqual(result, [0, 1, 2, 3, 4, 5, 6, 7])
    
    def test_empty_lists(self):
        """测试包含空列表"""
        result = merge_sorted_lists([], [1, 2], [])
        
        self.assertEqual(result, [1, 2])
    
    def test_all_empty(self):
        """测试全部空列表"""
        self.assertEqual(merge_sorted_lists(), [])
    
    def test_single_list(self):
        """测试单个列表"""
        self.assertEqual(merge_sorted_lists([1, 2, 3]), [1, 2, 3])


class TestIsValidHeap(unittest.TestCase):
    """测试堆有效性检查"""
    
    def test_valid_min_heap(self):
        """测试有效的最小堆"""
        self.assertTrue(is_valid_heap([1, 2, 3, 4, 5]))
        self.assertTrue(is_valid_heap([1, 1, 1, 1]))
    
    def test_invalid_min_heap(self):
        """测试无效的最小堆"""
        self.assertFalse(is_valid_heap([5, 4, 3, 2, 1]))
    
    def test_valid_max_heap(self):
        """测试有效的最大堆"""
        self.assertTrue(is_valid_heap([5, 4, 3, 2, 1], min_heap=False))
    
    def test_invalid_max_heap(self):
        """测试无效的最大堆"""
        self.assertFalse(is_valid_heap([1, 2, 3, 4, 5], min_heap=False))
    
    def test_empty_heap(self):
        """测试空堆"""
        self.assertTrue(is_valid_heap([]))
    
    def test_single_element(self):
        """测试单元素堆"""
        self.assertTrue(is_valid_heap([42]))


class TestHeapify(unittest.TestCase):
    """测试原地堆化"""
    
    def test_heapify_min(self):
        """测试最小堆化"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = heapify(data.copy())
        
        self.assertTrue(is_valid_heap(result))
    
    def test_heapify_max(self):
        """测试最大堆化"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = heapify(data.copy(), min_heap=False)
        
        self.assertTrue(is_valid_heap(result, min_heap=False))
    
    def test_in_place_modification(self):
        """测试原地修改"""
        data = [3, 1, 4, 1, 5]
        original_id = id(data)
        result = heapify(data)
        
        self.assertEqual(id(result), original_id)


class TestMedianOfData(unittest.TestCase):
    """测试中位数计算"""
    
    def test_odd_count(self):
        """测试奇数个元素"""
        data = [1, 2, 3, 4, 5]
        self.assertEqual(median_of_data(data), 3.0)
    
    def test_even_count(self):
        """测试偶数个元素"""
        data = [1, 2, 3, 4]
        self.assertEqual(median_of_data(data), 2.5)
    
    def test_unsorted_data(self):
        """测试未排序数据"""
        data = [5, 1, 3, 2, 4]
        self.assertEqual(median_of_data(data), 3.0)
    
    def test_empty_data(self):
        """测试空数据"""
        with self.assertRaises(ValueError):
            median_of_data([])
    
    def test_single_element(self):
        """测试单元素"""
        self.assertEqual(median_of_data([42]), 42.0)


class TestLargeData(unittest.TestCase):
    """测试大数据量"""
    
    def test_large_heap_sort(self):
        """测试大数据量堆排序"""
        random.seed(42)
        data = [random.randint(0, 10000) for _ in range(1000)]
        result = heap_sort(data)
        
        self.assertEqual(result, sorted(data))
    
    def test_large_k_smallest(self):
        """测试大数据量k小元素"""
        random.seed(42)
        data = [random.randint(0, 10000) for _ in range(1000)]
        result = k_smallest(data, 100)
        
        self.assertEqual(len(result), 100)
        self.assertEqual(result, sorted(data)[:100])


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_duplicate_elements(self):
        """测试重复元素"""
        heap = MinHeap([5, 5, 5, 5, 5])
        
        for _ in range(5):
            self.assertEqual(heap.pop(), 5)
    
    def test_negative_numbers(self):
        """测试负数"""
        heap = MinHeap([-3, -1, -4, -1, -5, -9, -2, -6])
        
        self.assertEqual(heap.pop(), -9)
        self.assertEqual(heap.pop(), -6)
        self.assertEqual(heap.pop(), -5)
    
    def test_float_numbers(self):
        """测试浮点数"""
        heap = MinHeap([3.14, 2.71, 1.41, 1.73])
        
        result = list(heap)
        self.assertEqual(result, [1.41, 1.73, 2.71, 3.14])
    
    def test_string_elements(self):
        """测试字符串元素"""
        heap = MinHeap(["cherry", "apple", "banana"])
        
        result = list(heap)
        self.assertEqual(result, ["apple", "banana", "cherry"])


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)