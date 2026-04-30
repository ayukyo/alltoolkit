"""
Top-K 工具集测试

测试所有 Top-K 功能：
- 堆方法 Top-K
- QuickSelect Top-K
- 流式 Top-K
- 频繁元素 Top-K
- 分布式合并
"""

import unittest
import random
from typing import List

from mod import (
    top_k_heap,
    top_k_quickselect,
    top_k_sort,
    StreamingTopK,
    FrequentItems,
    TopKFrequent,
    merge_top_k,
    merge_top_k_weighted,
    top_k_unique,
    top_k_with_threshold,
    top_k_percentile,
    nth_element,
    median,
)


class TestTopKHeap(unittest.TestCase):
    """测试堆方法 Top-K"""
    
    def test_basic_top_k(self):
        """基本 Top-K 测试"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = top_k_heap(data, 3)
        self.assertEqual(result, [9, 6, 5])
    
    def test_smallest_k(self):
        """测试最小 K 个"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = top_k_heap(data, 3, largest=False)
        self.assertEqual(result, [1, 1, 2])
    
    def test_with_key_function(self):
        """测试带键函数"""
        data = [{'val': 3}, {'val': 1}, {'val': 4}, {'val': 5}]
        result = top_k_heap(data, 2, key=lambda x: x['val'])
        self.assertEqual(result, [{'val': 5}, {'val': 4}])
    
    def test_k_greater_than_n(self):
        """测试 k > n 的情况"""
        data = [1, 2, 3]
        result = top_k_heap(data, 10)
        self.assertEqual(len(result), 3)
        self.assertEqual(result, [3, 2, 1])
    
    def test_k_zero(self):
        """测试 k=0 的情况"""
        data = [1, 2, 3]
        result = top_k_heap(data, 0)
        self.assertEqual(result, [])
    
    def test_empty_data(self):
        """测试空数据"""
        result = top_k_heap([], 5)
        self.assertEqual(result, [])
    
    def test_single_element(self):
        """测试单个元素"""
        result = top_k_heap([42], 1)
        self.assertEqual(result, [42])
    
    def test_duplicates(self):
        """测试重复元素"""
        data = [5, 5, 5, 5, 5]
        result = top_k_heap(data, 3)
        self.assertEqual(result, [5, 5, 5])
    
    def test_negative_numbers(self):
        """测试负数"""
        data = [-3, -1, -4, -1, -5, -9, -2, -6]
        result = top_k_heap(data, 3)
        self.assertEqual(result, [-1, -1, -2])


class TestTopKQuickSelect(unittest.TestCase):
    """测试 QuickSelect Top-K"""
    
    def test_basic_quickselect(self):
        """基本 QuickSelect 测试"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = top_k_quickselect(data, 3)
        # 结果包含最大的3个元素，顺序可能不同
        self.assertEqual(set(result), {9, 6, 5})
    
    def test_smallest_k(self):
        """测试最小 K 个"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = top_k_quickselect(data, 3, largest=False)
        self.assertEqual(set(result), {1, 1, 2})
    
    def test_preserves_original(self):
        """测试不修改原数组"""
        data = [3, 1, 4, 1, 5]
        original = list(data)
        top_k_quickselect(data, 2)
        self.assertEqual(data, original)
    
    def test_with_key_function(self):
        """测试带键函数"""
        data = [{'val': 3}, {'val': 1}, {'val': 4}]
        result = top_k_quickselect(data, 2, key=lambda x: x['val'])
        keys = {x['val'] for x in result}
        self.assertEqual(keys, {4, 3})


class TestTopKSort(unittest.TestCase):
    """测试排序方法 Top-K"""
    
    def test_basic_sort_method(self):
        """基本排序方法测试"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = top_k_sort(data, 3)
        self.assertEqual(result, [9, 6, 5])
    
    def test_smallest_k(self):
        """测试最小 K 个"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = top_k_sort(data, 3, largest=False)
        self.assertEqual(result, [1, 1, 2])


class TestStreamingTopK(unittest.TestCase):
    """测试流式 Top-K"""
    
    def test_streaming_basic(self):
        """基本流式测试"""
        stream = StreamingTopK(3)
        for x in [3, 1, 4, 1, 5, 9, 2, 6]:
            stream.add(x)
        
        result = stream.get_top_k()
        self.assertEqual(result, [9, 6, 5])
    
    def test_streaming_smallest(self):
        """测试最小 K 个"""
        stream = StreamingTopK(3, largest=False)
        for x in [3, 1, 4, 1, 5, 9, 2, 6]:
            stream.add(x)
        
        result = stream.get_top_k()
        self.assertEqual(result, [1, 1, 2])
    
    def test_streaming_with_key(self):
        """测试带键函数"""
        stream = StreamingTopK(2, key=lambda x: x['val'])
        for x in [{'val': 3}, {'val': 1}, {'val': 4}]:
            stream.add(x)
        
        result = stream.get_top_k()
        self.assertEqual(result, [{'val': 4}, {'val': 3}])
    
    def test_streaming_add_all(self):
        """测试批量添加"""
        stream = StreamingTopK(3)
        count = stream.add_all(iter([3, 1, 4, 1, 5, 9, 2, 6]))
        self.assertGreater(count, 0)
        self.assertEqual(len(stream), 3)
    
    def test_streaming_unsorted_output(self):
        """测试未排序输出"""
        stream = StreamingTopK(3)
        stream.add_all([1, 5, 3, 9, 2])
        result = stream.get_top_k(sorted_=False)
        self.assertEqual(len(result), 3)
        self.assertIn(9, result)
    
    def test_streaming_length(self):
        """测试长度"""
        stream = StreamingTopK(5)
        self.assertEqual(len(stream), 0)
        stream.add(1)
        self.assertEqual(len(stream), 1)
        stream.add_all([2, 3, 4, 5, 6])
        self.assertEqual(len(stream), 5)
    
    def test_streaming_invalid_k(self):
        """测试无效 k"""
        with self.assertRaises(ValueError):
            StreamingTopK(0)
        with self.assertRaises(ValueError):
            StreamingTopK(-1)


class TestFrequentItems(unittest.TestCase):
    """测试频繁元素计数器"""
    
    def test_basic_frequency(self):
        """基本频率测试"""
        freq = FrequentItems(5)  # 使用更大的 k 以跟踪所有元素
        for x in [1, 1, 1, 2, 2, 3, 4, 5]:
            freq.add(x)
        
        result = freq.get_top_k()
        # 元素1出现3次，元素2出现2次
        self.assertEqual(result[0], (1, 3))
        self.assertEqual(result[1], (2, 2))
    
    def test_frequency_count(self):
        """测试计数"""
        freq = FrequentItems(3)
        self.assertEqual(freq.add(1), 1)
        self.assertEqual(freq.add(1), 2)
        self.assertEqual(freq.add(1, 5), 7)  # 增加5
    
    def test_get_frequency(self):
        """测试获取单个元素频率"""
        freq = FrequentItems(5)
        freq.add_all([1, 1, 1, 2, 2, 3])
        self.assertEqual(freq.get_frequency(1), 3)
        self.assertEqual(freq.get_frequency(2), 2)
        self.assertEqual(freq.get_frequency(99), 0)  # 不存在的元素
    
    def test_total_count(self):
        """测试总计数"""
        freq = FrequentItems(5)
        freq.add_all([1, 2, 3, 4, 5])
        self.assertEqual(freq.get_total(), 5)
    
    def test_space_saving(self):
        """测试 Space-Saving 算法特性"""
        freq = FrequentItems(2)
        # 只跟踪2个元素
        freq.add(1)
        freq.add(2)
        self.assertEqual(len(freq), 2)
        
        # 当添加第3个元素时，应该替换计数最小的
        freq.add(3)
        self.assertEqual(len(freq), 2)
    
    def test_unsorted_output(self):
        """测试未排序输出"""
        freq = FrequentItems(3)
        freq.add_all([1, 2, 3, 1, 2])
        result = freq.get_top_k(sorted_=False)
        self.assertEqual(len(result), 3)


class TestTopKFrequent(unittest.TestCase):
    """测试精确频繁元素计数器"""
    
    def test_exact_frequency(self):
        """精确频率测试"""
        freq = TopKFrequent()
        freq.add_all([1, 1, 1, 2, 2, 3, 4, 5])
        
        result = freq.get_top_k(3)
        self.assertEqual(result, [(1, 3), (2, 2), (3, 1)])
    
    def test_unique_count(self):
        """测试唯一元素数量"""
        freq = TopKFrequent()
        freq.add_all([1, 1, 1, 2, 2, 3, 4, 5])
        self.assertEqual(freq.get_unique_count(), 5)
    
    def test_get_all(self):
        """测试获取所有元素"""
        freq = TopKFrequent()
        freq.add_all([1, 2, 2])
        all_items = freq.get_all()
        self.assertEqual(all_items, {1: 1, 2: 2})


class TestMergeTopK(unittest.TestCase):
    """测试分布式 Top-K 合并"""
    
    def test_merge_basic(self):
        """基本合并测试"""
        lists = [[9, 8, 7], [10, 5, 3], [6, 4, 2]]
        result = merge_top_k(lists, 3)
        self.assertEqual(result, [10, 9, 8])
    
    def test_merge_smallest(self):
        """测试合并最小"""
        lists = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
        result = merge_top_k(lists, 3, largest=False)
        self.assertEqual(result, [0, 1, 2])
    
    def test_merge_weighted(self):
        """测试带权重合并"""
        lists = [([9, 8], 1.0), ([5, 4], 2.0)]  # 第二组权重更高
        result = merge_top_k_weighted(lists, 2)
        # 5*2=10 > 9*1=9, 4*2=8 > 8*1=8
        self.assertEqual(result, [5, 9])


class TestSpecialPurposeTopK(unittest.TestCase):
    """测试特殊用途 Top-K"""
    
    def test_top_k_unique(self):
        """测试唯一元素 Top-K"""
        data = [3, 1, 4, 1, 5, 9, 2, 6, 5]
        result = top_k_unique(data, 3)
        self.assertEqual(len(set(result)), 3)
        self.assertEqual(result, [9, 6, 5])
    
    def test_top_k_with_threshold(self):
        """测试阈值 Top-K"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = top_k_with_threshold(data, 4)
        self.assertEqual(result, [9, 6, 5])
    
    def test_top_k_with_threshold_below(self):
        """测试小于阈值"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = top_k_with_threshold(data, 3, largest=False)
        self.assertEqual(result, [1, 1, 2])
    
    def test_top_k_percentile(self):
        """测试百分位 Top-K"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = top_k_percentile(data, 80)
        self.assertEqual(result, [9, 10])
    
    def test_top_k_percentile_below(self):
        """测试低于百分位"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = top_k_percentile(data, 30, largest=False)
        self.assertEqual(result, [1, 2, 3])


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_nth_element(self):
        """测试第 n 大元素"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = nth_element(data, 3)  # 第3大
        self.assertIn(result, [5, 6])  # 第3大是5或6（取决于重复处理）
    
    def test_nth_element_smallest(self):
        """测试第 n 小元素"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        result = nth_element(data, 2, largest=False)  # 第2小
        self.assertEqual(result, 1)
    
    def test_nth_element_invalid(self):
        """测试无效 n"""
        with self.assertRaises(ValueError):
            nth_element([1, 2, 3], 0)
        with self.assertRaises(ValueError):
            nth_element([1, 2, 3], 4)
    
    def test_median_odd(self):
        """测试奇数个元素的中位数"""
        result = median([1, 2, 3, 4, 5])
        self.assertEqual(result, 3.0)
    
    def test_median_even(self):
        """测试偶数个元素的中位数"""
        result = median([1, 2, 3, 4])
        self.assertEqual(result, 2.5)
    
    def test_median_with_key(self):
        """测试带键函数的中位数"""
        data = [{'val': 1}, {'val': 2}, {'val': 3}]
        result = median(data, key=lambda x: x['val'])
        self.assertEqual(result, 2.0)
    
    def test_median_empty(self):
        """测试空数据的中位数"""
        with self.assertRaises(ValueError):
            median([])


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_large_dataset_heap(self):
        """大数据集堆方法测试"""
        random.seed(42)
        data = [random.randint(1, 1000000) for _ in range(10000)]
        result = top_k_heap(data, 100)
        self.assertEqual(len(result), 100)
        # 验证结果正确性
        sorted_data = sorted(data, reverse=True)[:100]
        self.assertEqual(result, sorted_data)
    
    def test_large_dataset_quickselect(self):
        """大数据集 QuickSelect 测试"""
        random.seed(42)
        data = [random.randint(1, 1000000) for _ in range(10000)]
        result = top_k_quickselect(data, 100)
        self.assertEqual(len(result), 100)
        # 验证结果包含最大的100个
        sorted_data = sorted(data, reverse=True)[:100]
        self.assertEqual(set(result), set(sorted_data))
    
    def test_streaming_performance(self):
        """流式处理性能测试"""
        stream = StreamingTopK(100)
        random.seed(42)
        for _ in range(10000):
            stream.add(random.randint(1, 1000000))
        
        result = stream.get_top_k()
        self.assertEqual(len(result), 100)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_all_same_values(self):
        """测试所有值相同"""
        data = [5] * 10
        result = top_k_heap(data, 3)
        self.assertEqual(result, [5, 5, 5])
    
    def test_already_sorted(self):
        """测试已排序数据"""
        data = list(range(100))
        result = top_k_heap(data, 10)
        self.assertEqual(result, list(range(99, 89, -1)))
    
    def test_reverse_sorted(self):
        """测试逆序数据"""
        data = list(range(100, 0, -1))
        result = top_k_heap(data, 10)
        self.assertEqual(result, list(range(100, 90, -1)))
    
    def test_k_equals_n(self):
        """测试 k=n 的情况"""
        data = [3, 1, 4, 1, 5]
        result = top_k_heap(data, 5)
        self.assertEqual(result, [5, 4, 3, 1, 1])


if __name__ == '__main__':
    unittest.main(verbosity=2)