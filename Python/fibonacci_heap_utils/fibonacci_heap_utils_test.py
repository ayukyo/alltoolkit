#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Fibonacci Heap Utilities Test Suite
斐波那契堆工具模块测试套件

@author: AllToolkit Contributors
@license: MIT
"""

import unittest
import sys
import random
from typing import List
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    FibonacciHeap, MaxFibonacciHeap, FibonacciNode,
    FibonacciHeapUtils,
    create_min_heap, create_max_heap, heap_sort, top_k
)


class TestFibonacciHeapBasic(unittest.TestCase):
    """基本功能测试"""
    
    def test_create_empty_heap(self):
        """测试创建空堆"""
        heap = FibonacciHeap[int]()
        self.assertTrue(heap.is_empty())
        self.assertEqual(heap.size, 0)
        self.assertIsNone(heap.find_min())
        self.assertIsNone(heap.find_min_value())
        self.assertIsNone(heap.peek())
        self.assertIsNone(heap.peek_key())
    
    def test_single_insert(self):
        """测试单个元素插入"""
        heap = FibonacciHeap[int]()
        node = heap.insert(5, "test")
        
        self.assertEqual(heap.size, 1)
        self.assertFalse(heap.is_empty())
        self.assertEqual(heap.find_min(), 5)
        self.assertEqual(heap.find_min_value(), "test")
        self.assertEqual(node.key, 5)
        self.assertEqual(node.value, "test")
    
    def test_multiple_inserts(self):
        """测试多个元素插入"""
        heap = FibonacciHeap[int]()
        
        heap.insert(5, "five")
        self.assertEqual(heap.find_min(), 5)
        
        heap.insert(2, "two")
        self.assertEqual(heap.find_min(), 2)
        
        heap.insert(8, "eight")
        self.assertEqual(heap.find_min(), 2)
        
        heap.insert(1, "one")
        self.assertEqual(heap.find_min(), 1)
        
        self.assertEqual(heap.size, 4)
    
    def test_extract_min_single(self):
        """测试单个元素提取"""
        heap = FibonacciHeap[int]()
        heap.insert(5, "five")
        
        value = heap.extract_min()
        self.assertEqual(value, "five")
        self.assertTrue(heap.is_empty())
        self.assertEqual(heap.size, 0)
    
    def test_extract_min_multiple(self):
        """测试多个元素按序提取"""
        heap = FibonacciHeap[int]()
        
        values = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        for v in values:
            heap.insert(v, str(v))
        
        result = []
        while not heap.is_empty():
            result.append(heap.extract_min())
        
        expected = [str(v) for v in sorted(values)]
        self.assertEqual(result, expected)
    
    def test_extract_min_with_key(self):
        """测试带键值提取"""
        heap = FibonacciHeap[str]()
        
        heap.insert(3, "c")
        heap.insert(1, "a")
        heap.insert(2, "b")
        
        key, value = heap.extract_min_with_key()
        self.assertEqual(key, 1)
        self.assertEqual(value, "a")
        
        key, value = heap.extract_min_with_key()
        self.assertEqual(key, 2)
        self.assertEqual(value, "b")
    
    def test_insert_with_none_value(self):
        """测试插入None值"""
        heap = FibonacciHeap[int]()
        
        heap.insert(5)
        heap.insert(3)
        
        self.assertEqual(heap.find_min(), 3)
        self.assertIsNone(heap.find_min_value())


class TestFibonacciHeapMaxHeap(unittest.TestCase):
    """最大堆测试"""
    
    def test_max_heap_basic(self):
        """测试最大堆基本功能"""
        heap = MaxFibonacciHeap[int]()
        
        heap.insert(5, "five")
        heap.insert(1, "one")
        heap.insert(10, "ten")
        heap.insert(3, "three")
        
        self.assertEqual(heap.find_max(), 10)
        self.assertEqual(heap.find_max_value(), "ten")
        
        result = []
        while not heap.is_empty():
            result.append(heap.extract_max())
        
        self.assertEqual(result, ["ten", "five", "three", "one"])
    
    def test_max_heap_with_duplicate_keys(self):
        """测试最大堆重复键值"""
        heap = MaxFibonacciHeap[int]()
        
        heap.insert(5, "first")
        heap.insert(5, "second")
        heap.insert(5, "third")
        
        # 所有值都应该被提取
        values = [heap.extract_max() for _ in range(3)]
        self.assertEqual(set(values), {"first", "second", "third"})
    
    def test_increase_key(self):
        """测试增大键值"""
        heap = MaxFibonacciHeap[int]()
        
        n1 = heap.insert(5, "task1")
        n2 = heap.insert(3, "task2")
        n3 = heap.insert(7, "task3")
        
        self.assertEqual(heap.find_max_value(), "task3")
        
        heap.increase_key(n1, 10)  # 将task1从5增大到10
        
        self.assertEqual(heap.find_max_value(), "task1")
        self.assertEqual(heap.extract_max(), "task1")


class TestFibonacciHeapDecreaseKey(unittest.TestCase):
    """decrease_key 操作测试"""
    
    def test_decrease_key_basic(self):
        """测试基本的decrease_key"""
        heap = FibonacciHeap[str]()
        
        n1 = heap.insert(10, "task1")
        n2 = heap.insert(5, "task2")
        n3 = heap.insert(8, "task3")
        
        self.assertEqual(heap.find_min_value(), "task2")
        
        heap.decrease_key(n1, 1)  # task1从10降到1
        
        self.assertEqual(heap.find_min_value(), "task1")
        self.assertEqual(heap.find_min(), 1)
    
    def test_decrease_key_with_extract(self):
        """测试decrease_key后提取"""
        heap = FibonacciHeap[str]()
        
        n1 = heap.insert(10, "low")
        n2 = heap.insert(5, "medium")
        n3 = heap.insert(3, "high")
        
        heap.decrease_key(n1, 1)  # low 变成最高优先级
        
        result = []
        while not heap.is_empty():
            result.append(heap.extract_min())
        
        self.assertEqual(result, ["low", "high", "medium"])
    
    def test_decrease_key_invalid(self):
        """测试无效的decrease_key"""
        heap = FibonacciHeap[int]()
        node = heap.insert(5, "test")
        
        # 在最小堆中，新键值不能大于当前键值
        with self.assertRaises(ValueError):
            heap.decrease_key(node, 10)
    
    def test_decrease_key_to_same_value(self):
        """测试decrease_key到相同值"""
        heap = FibonacciHeap[int]()
        node = heap.insert(5, "test")
        
        # 应该不报错
        heap.decrease_key(node, 5)
        self.assertEqual(node.key, 5)


class TestFibonacciHeapDelete(unittest.TestCase):
    """删除操作测试"""
    
    def test_delete_specific_node(self):
        """测试删除特定节点"""
        heap = FibonacciHeap[str]()
        
        n1 = heap.insert(1, "one")
        n2 = heap.insert(2, "two")
        n3 = heap.insert(3, "three")
        
        # 删除中间节点
        deleted = heap.delete(n2)
        self.assertEqual(deleted, "two")
        self.assertEqual(heap.size, 2)
        
        # 验证剩余元素
        result = heap.to_list()
        self.assertEqual(set(result), {"one", "three"})
    
    def test_delete_min_node(self):
        """测试删除最小节点"""
        heap = FibonacciHeap[str]()
        
        n1 = heap.insert(1, "one")
        n2 = heap.insert(2, "two")
        n3 = heap.insert(3, "three")
        
        deleted = heap.delete(n1)
        self.assertEqual(deleted, "one")
        self.assertEqual(heap.find_min_value(), "two")
    
    def test_delete_max_node_in_max_heap(self):
        """测试在最大堆中删除最大节点"""
        heap = MaxFibonacciHeap[int]()
        
        n1 = heap.insert(1, "one")
        n2 = heap.insert(2, "two")
        n3 = heap.insert(3, "three")
        
        deleted = heap.delete(n3)
        self.assertEqual(deleted, "three")
        self.assertEqual(heap.find_max_value(), "two")


class TestFibonacciHeapMerge(unittest.TestCase):
    """合并操作测试"""
    
    def test_merge_two_heaps(self):
        """测试合并两个堆"""
        h1 = FibonacciHeap[int]()
        h1.insert(1, "h1-1")
        h1.insert(3, "h1-3")
        
        h2 = FibonacciHeap[int]()
        h2.insert(2, "h2-2")
        h2.insert(4, "h2-4")
        
        h1.merge(h2)
        
        self.assertEqual(h1.size, 4)
        self.assertEqual(h2.size, 0)
        self.assertTrue(h2.is_empty())
        
        result = h1.to_list()
        self.assertEqual(result, ["h1-1", "h2-2", "h1-3", "h2-4"])
    
    def test_merge_empty_heap(self):
        """测试合并空堆"""
        h1 = FibonacciHeap[int]()
        h1.insert(1, "one")
        
        h2 = FibonacciHeap[int]()
        
        h1.merge(h2)
        self.assertEqual(h1.size, 1)
        
        h2.merge(h1)
        self.assertEqual(h2.size, 1)
    
    def test_merge_max_heaps(self):
        """测试合并最大堆"""
        h1 = MaxFibonacciHeap[int]()
        h1.insert(5, "h1-5")
        h1.insert(1, "h1-1")
        
        h2 = MaxFibonacciHeap[int]()
        h2.insert(3, "h2-3")
        h2.insert(7, "h2-7")
        
        h1.merge(h2)
        
        result = h1.to_list()
        self.assertEqual(result, ["h2-7", "h1-5", "h2-3", "h1-1"])


class TestFibonacciHeapQuery(unittest.TestCase):
    """查询操作测试"""
    
    def test_contains(self):
        """测试包含检查"""
        heap = FibonacciHeap[str]()
        
        heap.insert(1, "one")
        heap.insert(2, "two")
        heap.insert(3, "three")
        
        self.assertTrue(heap.contains("one"))
        self.assertTrue(heap.contains("two"))
        self.assertFalse(heap.contains("four"))
    
    def test_find_node(self):
        """测试查找节点"""
        heap = FibonacciHeap[str]()
        
        heap.insert(1, "one")
        heap.insert(2, "two")
        
        node = heap.find_node("two")
        self.assertIsNotNone(node)
        self.assertEqual(node.key, 2)
        self.assertEqual(node.value, "two")
        
        node = heap.find_node("three")
        self.assertIsNone(node)
    
    def test_get_all_values(self):
        """测试获取所有值"""
        heap = FibonacciHeap[int]()
        
        values = [5, 2, 8, 1]
        for v in values:
            heap.insert(v, v)
        
        all_values = heap.get_all_values()
        self.assertEqual(set(all_values), set(values))
    
    def test_get_all_keys(self):
        """测试获取所有键"""
        heap = FibonacciHeap[int]()
        
        keys = [5, 2, 8, 1]
        for k in keys:
            heap.insert(k, str(k))
        
        all_keys = heap.get_all_keys()
        self.assertEqual(set(all_keys), set(keys))
    
    def test_iteration(self):
        """测试迭代器"""
        heap = FibonacciHeap[str]()
        
        values = ["a", "b", "c", "d"]
        for i, v in enumerate(values):
            heap.insert(i, v)
        
        result = list(heap)
        self.assertEqual(set(result), set(values))
    
    def test_len(self):
        """测试长度"""
        heap = FibonacciHeap[int]()
        
        self.assertEqual(len(heap), 0)
        
        heap.insert(1, "one")
        self.assertEqual(len(heap), 1)
        
        heap.insert(2, "two")
        self.assertEqual(len(heap), 2)
        
        heap.extract_min()
        self.assertEqual(len(heap), 1)


class TestFibonacciHeapSerialization(unittest.TestCase):
    """序列化测试"""
    
    def test_to_dict(self):
        """测试转换为字典"""
        heap = FibonacciHeap[str]()
        heap.insert(1, "one")
        heap.insert(2, "two")
        heap.insert(3, "three")
        
        data = heap.to_dict()
        
        self.assertEqual(data['size'], 3)
        self.assertEqual(data['is_max_heap'], False)
        self.assertEqual(len(data['nodes']), 3)
    
    def test_from_dict(self):
        """测试从字典创建"""
        heap = FibonacciHeap[str]()
        heap.insert(1, "one")
        heap.insert(2, "two")
        
        data = heap.to_dict()
        new_heap = FibonacciHeap.from_dict(data)
        
        self.assertEqual(new_heap.size, 2)
        self.assertEqual(new_heap.to_list(), ["one", "two"])
    
    def test_to_json(self):
        """测试JSON序列化"""
        heap = FibonacciHeap[int]()
        heap.insert(1, 10)
        heap.insert(2, 20)
        
        json_str = heap.to_json()
        self.assertIn('"size": 2', json_str)
        self.assertIn('"is_max_heap": false', json_str)
    
    def test_from_json(self):
        """测试从JSON创建"""
        heap = FibonacciHeap[str]()
        heap.insert(1, "a")
        heap.insert(2, "b")
        
        json_str = heap.to_json()
        new_heap = FibonacciHeap.from_json(json_str)
        
        self.assertEqual(new_heap.to_list(), ["a", "b"])
    
    def test_copy(self):
        """测试复制"""
        heap = FibonacciHeap[str]()
        heap.insert(1, "one")
        heap.insert(2, "two")
        
        copy = heap.copy()
        
        self.assertEqual(copy.size, 2)
        # 不使用 to_list() 因为它会清空堆
        # 验证副本独立存在
        self.assertEqual(copy.peek(), "one")
        self.assertEqual(copy.peek_key(), 1)
        
        # 修改原堆不影响副本
        heap.extract_min()
        self.assertEqual(heap.size, 1)
        self.assertEqual(copy.size, 2)
        self.assertEqual(copy.peek(), "one")


class TestFibonacciHeapClear(unittest.TestCase):
    """清空操作测试"""
    
    def test_clear(self):
        """测试清空堆"""
        heap = FibonacciHeap[int]()
        
        for i in range(10):
            heap.insert(i, str(i))
        
        self.assertEqual(heap.size, 10)
        
        heap.clear()
        
        self.assertTrue(heap.is_empty())
        self.assertEqual(heap.size, 0)
        self.assertIsNone(heap.find_min())


class TestFibonacciHeapEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_large_number_of_elements(self):
        """测试大量元素"""
        heap = FibonacciHeap[int]()
        n = 1000
        
        for i in range(n):
            heap.insert(random.randint(0, n), str(i))
        
        self.assertEqual(heap.size, n)
        
        # 验证提取顺序
        prev_key = float('-inf')
        count = 0
        while not heap.is_empty():
            key, _ = heap.extract_min_with_key()
            self.assertGreaterEqual(key, prev_key)
            prev_key = key
            count += 1
        
        self.assertEqual(count, n)
    
    def test_negative_keys(self):
        """测试负键值"""
        heap = FibonacciHeap[int]()
        
        heap.insert(-5, "neg5")
        heap.insert(0, "zero")
        heap.insert(5, "pos5")
        
        result = heap.to_list()
        self.assertEqual(result, ["neg5", "zero", "pos5"])
    
    def test_float_keys(self):
        """测试浮点键值"""
        heap = FibonacciHeap[str]()
        
        heap.insert(1.5, "a")
        heap.insert(0.5, "b")
        heap.insert(2.0, "c")
        
        result = heap.to_list()
        self.assertEqual(result, ["b", "a", "c"])
    
    def test_duplicate_keys(self):
        """测试重复键值"""
        heap = FibonacciHeap[str]()
        
        heap.insert(5, "first")
        heap.insert(5, "second")
        heap.insert(5, "third")
        heap.insert(1, "one")
        
        # 第一个应该是最小值
        first = heap.extract_min()
        self.assertEqual(first, "one")
        
        # 其余三个顺序可能不确定，但都应该被提取
        remaining = set()
        while not heap.is_empty():
            remaining.add(heap.extract_min())
        
        self.assertEqual(remaining, {"first", "second", "third"})
    
    def test_string_values(self):
        """测试字符串值"""
        heap = FibonacciHeap[str]()
        
        heap.insert(3, "hello")
        heap.insert(1, "world")
        heap.insert(2, "test")
        
        self.assertEqual(heap.to_list(), ["world", "test", "hello"])
    
    def test_none_values(self):
        """测试None值"""
        heap = FibonacciHeap[None]()
        
        heap.insert(3)
        heap.insert(1)
        heap.insert(2)
        
        result = []
        while not heap.is_empty():
            result.append(heap.extract_min())
        
        self.assertEqual(result, [None, None, None])


class TestFibonacciHeapUtils(unittest.TestCase):
    """工具类测试"""
    
    def test_create_min_heap(self):
        """测试创建最小堆"""
        heap = create_min_heap()
        self.assertFalse(heap.is_max_heap)
        self.assertTrue(heap.is_empty())
    
    def test_create_max_heap(self):
        """测试创建最大堆"""
        heap = create_max_heap()
        self.assertTrue(heap.is_max_heap)
        self.assertTrue(heap.is_empty())
    
    def test_heap_sort_ascending(self):
        """测试升序堆排序"""
        items = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        result = heap_sort(items)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    
    def test_heap_sort_descending(self):
        """测试降序堆排序"""
        items = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        result = heap_sort(items, reverse=True)
        self.assertEqual(result, [9, 8, 7, 6, 5, 4, 3, 2, 1])
    
    def test_heap_sort_empty(self):
        """测试空数组排序"""
        result = heap_sort([])
        self.assertEqual(result, [])
    
    def test_top_k_largest(self):
        """测试最大的K个元素"""
        items = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        result = top_k(items, 3, largest=True)
        self.assertEqual(set(result), {9, 8, 7})
    
    def test_top_k_smallest(self):
        """测试最小的K个元素"""
        items = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        result = top_k(items, 3, largest=False)
        self.assertEqual(set(result), {1, 2, 3})
    
    def test_top_k_with_key_func(self):
        """测试带键函数的Top K"""
        items = ["apple", "pie", "banana", "hi", "cherry"]
        result = top_k(items, 2, key_func=len, largest=True)
        # 最长的两个: banana, cherry
        self.assertEqual(set(result), {"banana", "cherry"})
    
    def test_top_k_k_greater_than_n(self):
        """测试K大于N的情况"""
        items = [1, 2, 3]
        result = top_k(items, 10, largest=True)
        self.assertEqual(sorted(result), [1, 2, 3])
    
    def test_merge_heaps(self):
        """测试合并多个堆"""
        h1 = FibonacciHeap[int]()
        h1.insert(1, "h1")
        h1.insert(3, "h1-3")
        
        h2 = FibonacciHeap[int]()
        h2.insert(2, "h2")
        h2.insert(4, "h2-4")
        
        h3 = FibonacciHeap[int]()
        h3.insert(0, "h3")
        
        merged = FibonacciHeapUtils.merge_heaps(h1, h2, h3)
        
        result = merged.to_list()
        self.assertEqual(result, ["h3", "h1", "h2", "h1-3", "h2-4"])
    
    def test_find_median_odd(self):
        """测试找中位数（奇数个元素）"""
        items = [5, 2, 8, 1, 9]
        median = FibonacciHeapUtils.find_median(items)
        self.assertEqual(median, 5)
    
    def test_find_median_even(self):
        """测试找中位数（偶数个元素）"""
        items = [5, 2, 8, 1]
        median = FibonacciHeapUtils.find_median(items)
        self.assertEqual(median, 3.5)  # (2 + 5) / 2
    
    def test_find_median_empty(self):
        """测试空数组找中位数"""
        median = FibonacciHeapUtils.find_median([])
        self.assertIsNone(median)
    
    def test_from_list(self):
        """测试从列表创建"""
        items = [5, 2, 8, 1]
        heap = FibonacciHeap.from_list(items)
        
        result = heap.to_list()
        self.assertEqual(result, [1, 2, 5, 8])
    
    def test_from_list_with_key_func(self):
        """测试从列表创建（带键函数）"""
        items = ["apple", "pie", "banana"]
        heap = FibonacciHeap.from_list(items, key_func=len)
        
        # 按长度排序: pie(3), apple(5), banana(6)
        result = heap.to_list()
        self.assertEqual(result, ["pie", "apple", "banana"])


class TestFibonacciHeapStress(unittest.TestCase):
    """压力测试"""
    
    def test_many_inserts_and_extracts(self):
        """测试大量插入和提取"""
        heap = FibonacciHeap[int]()
        n = 500
        
        # 插入
        for i in range(n):
            heap.insert(random.randint(0, n * 10), i)
        
        self.assertEqual(heap.size, n)
        
        # 提取并验证顺序
        prev_key = float('-inf')
        count = 0
        while not heap.is_empty():
            key, _ = heap.extract_min_with_key()
            self.assertGreaterEqual(key, prev_key)
            prev_key = key
            count += 1
        
        self.assertEqual(count, n)
    
    def test_many_decrease_keys(self):
        """测试大量decrease_key操作"""
        heap = FibonacciHeap[int]()
        nodes = []
        n = 100
        
        # 插入
        for i in range(n):
            node = heap.insert(i * 10, str(i))
            nodes.append(node)
        
        # 随机减小键值
        for _ in range(50):
            idx = random.randint(0, n - 1)
            new_key = random.randint(0, nodes[idx].key)
            heap.decrease_key(nodes[idx], new_key)
        
        # 验证堆性质
        prev_key = float('-inf')
        while not heap.is_empty():
            key, _ = heap.extract_min_with_key()
            self.assertGreaterEqual(key, prev_key)
            prev_key = key
    
    def test_alternating_operations(self):
        """测试交替操作"""
        heap = FibonacciHeap[int]()
        
        # 交替插入和提取
        for i in range(100):
            heap.insert(random.randint(0, 100), i)
            if i % 3 == 0 and heap.size > 0:
                heap.extract_min()
        
        # 验证堆性质
        prev_key = float('-inf')
        while not heap.is_empty():
            key, _ = heap.extract_min_with_key()
            self.assertGreaterEqual(key, prev_key)
            prev_key = key
    
    def test_merge_large_heaps(self):
        """测试合并大堆"""
        h1 = FibonacciHeap[int]()
        h2 = FibonacciHeap[int]()
        
        for i in range(500):
            h1.insert(random.randint(0, 1000), f"h1-{i}")
            h2.insert(random.randint(0, 1000), f"h2-{i}")
        
        h1.merge(h2)
        
        self.assertEqual(h1.size, 1000)
        self.assertEqual(h2.size, 0)
        
        # 验证堆性质
        prev_key = float('-inf')
        count = 0
        while not h1.is_empty():
            key, _ = h1.extract_min_with_key()
            self.assertGreaterEqual(key, prev_key)
            prev_key = key
            count += 1
        
        self.assertEqual(count, 1000)


class TestFibonacciNode(unittest.TestCase):
    """节点测试"""
    
    def test_node_creation(self):
        """测试节点创建"""
        node = FibonacciNode(5, "test")
        
        self.assertEqual(node.key, 5)
        self.assertEqual(node.value, "test")
        self.assertEqual(node.degree, 0)
        self.assertFalse(node.mark)
        self.assertIsNone(node.parent)
        self.assertIsNone(node.child)
        self.assertIs(node.left, node)
        self.assertIs(node.right, node)
    
    def test_node_is_single(self):
        """测试节点单例检查"""
        node = FibonacciNode(1, "test")
        self.assertTrue(node.is_single())
        
        # 添加兄弟
        node2 = FibonacciNode(2, "test2")
        node.right = node2
        node2.left = node
        
        self.assertFalse(node.is_single())
    
    def test_node_comparison(self):
        """测试节点比较"""
        node1 = FibonacciNode(1, "a")
        node2 = FibonacciNode(2, "b")
        node3 = FibonacciNode(1, "c")
        
        self.assertTrue(node1 < node2)
        self.assertTrue(node2 > node1)
        self.assertTrue(node1 == node3)
        self.assertTrue(node1 <= node3)
    
    def test_node_repr(self):
        """测试节点字符串表示"""
        node = FibonacciNode(5, "test")
        repr_str = repr(node)
        
        self.assertIn("key=5", repr_str)
        self.assertIn("value=test", repr_str)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestFibonacciHeapBasic))
    suite.addTests(loader.loadTestsFromTestCase(TestFibonacciHeapMaxHeap))
    suite.addTests(loader.loadTestsFromTestCase(TestFibonacciHeapDecreaseKey))
    suite.addTests(loader.loadTestsFromTestCase(TestFibonacciHeapDelete))
    suite.addTests(loader.loadTestsFromTestCase(TestFibonacciHeapMerge))
    suite.addTests(loader.loadTestsFromTestCase(TestFibonacciHeapQuery))
    suite.addTests(loader.loadTestsFromTestCase(TestFibonacciHeapSerialization))
    suite.addTests(loader.loadTestsFromTestCase(TestFibonacciHeapClear))
    suite.addTests(loader.loadTestsFromTestCase(TestFibonacciHeapEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestFibonacciHeapUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestFibonacciHeapStress))
    suite.addTests(loader.loadTestsFromTestCase(TestFibonacciNode))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)