"""
sorting_utils 测试文件
全面测试各种排序算法的功能和边界情况
"""

import sys
import os
import unittest
import random
import time
from typing import List

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    quick_sort,
    merge_sort,
    heap_sort,
    insertion_sort,
    selection_sort,
    bubble_sort,
    shell_sort,
    counting_sort,
    bucket_sort,
    radix_sort,
    tim_sort_like,
    cocktail_sort,
    gnome_sort,
    sort_by_custom,
    is_sorted,
    get_sort_algorithm_complexity,
    recommend_sort_algorithm,
)


class TestQuickSort(unittest.TestCase):
    """快速排序测试"""
    
    def test_basic_sort(self):
        """基础排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = quick_sort(arr)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
        # 原数组不变
        self.assertEqual(arr, [5, 2, 8, 1, 9, 3])
    
    def test_reverse_sort(self):
        """降序排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = quick_sort(arr, reverse=True)
        self.assertEqual(result, [9, 8, 5, 3, 2, 1])
    
    def test_with_key(self):
        """使用 key 函数排序"""
        arr = ['apple', 'banana', 'cherry', 'date']
        result = quick_sort(arr, key=lambda x: len(x))
        self.assertEqual(result, ['date', 'apple', 'banana', 'cherry'])
    
    def test_in_place(self):
        """原地排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = quick_sort(arr, in_place=True)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
        self.assertEqual(arr, [1, 2, 3, 5, 8, 9])  # 原数组已改变
    
    def test_empty_array(self):
        """空数组测试"""
        self.assertEqual(quick_sort([]), [])
    
    def test_single_element(self):
        """单元素测试"""
        self.assertEqual(quick_sort([42]), [42])
    
    def test_already_sorted(self):
        """已排序数组测试"""
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(quick_sort(arr), [1, 2, 3, 4, 5])
    
    def test_all_same(self):
        """全部相同元素测试"""
        arr = [5, 5, 5, 5, 5]
        self.assertEqual(quick_sort(arr), [5, 5, 5, 5, 5])
    
    def test_negative_numbers(self):
        """负数测试"""
        arr = [3, -1, 4, -5, 2]
        self.assertEqual(quick_sort(arr), [-5, -1, 2, 3, 4])
    
    def test_large_array(self):
        """大数组测试"""
        arr = list(range(1000, 0, -1))
        result = quick_sort(arr)
        self.assertEqual(result, list(range(1, 1001)))
    
    def test_duplicates(self):
        """重复元素测试"""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5]
        result = quick_sort(arr)
        self.assertEqual(result, [1, 1, 2, 3, 4, 5, 5, 6, 9])


class TestMergeSort(unittest.TestCase):
    """归并排序测试"""
    
    def test_basic_sort(self):
        """基础排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = merge_sort(arr)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
    
    def test_reverse_sort(self):
        """降序排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = merge_sort(arr, reverse=True)
        self.assertEqual(result, [9, 8, 5, 3, 2, 1])
    
    def test_with_key(self):
        """使用 key 函数排序"""
        arr = [{'name': 'Bob', 'age': 25}, {'name': 'Alice', 'age': 30}]
        result = merge_sort(arr, key=lambda x: x['age'])
        self.assertEqual(result[0]['name'], 'Bob')
        self.assertEqual(result[1]['name'], 'Alice')
    
    def test_stability(self):
        """稳定性测试"""
        arr = [(3, 'a'), (1, 'b'), (3, 'c'), (2, 'd')]
        result = merge_sort(arr, key=lambda x: x[0], stable=True)
        # (3, 'a') 应在 (3, 'c') 前面
        self.assertEqual(result, [(1, 'b'), (2, 'd'), (3, 'a'), (3, 'c')])
    
    def test_empty_array(self):
        """空数组测试"""
        self.assertEqual(merge_sort([]), [])
    
    def test_single_element(self):
        """单元素测试"""
        self.assertEqual(merge_sort([42]), [42])
    
    def test_two_elements(self):
        """两元素测试"""
        self.assertEqual(merge_sort([2, 1]), [1, 2])
        self.assertEqual(merge_sort([1, 2]), [1, 2])


class TestHeapSort(unittest.TestCase):
    """堆排序测试"""
    
    def test_basic_sort(self):
        """基础排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = heap_sort(arr)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
    
    def test_reverse_sort(self):
        """降序排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = heap_sort(arr, reverse=True)
        self.assertEqual(result, [9, 8, 5, 3, 2, 1])
    
    def test_with_key(self):
        """使用 key 函数排序"""
        arr = ['zzz', 'aaa', 'bbb']
        result = heap_sort(arr, key=lambda x: x)
        self.assertEqual(result, ['aaa', 'bbb', 'zzz'])
    
    def test_empty_array(self):
        """空数组测试"""
        self.assertEqual(heap_sort([]), [])
    
    def test_single_element(self):
        """单元素测试"""
        self.assertEqual(heap_sort([42]), [42])
    
    def test_large_array(self):
        """大数组测试"""
        arr = random.sample(range(10000), 1000)
        result = heap_sort(arr)
        self.assertEqual(result, sorted(arr))


class TestInsertionSort(unittest.TestCase):
    """插入排序测试"""
    
    def test_basic_sort(self):
        """基础排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = insertion_sort(arr)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
    
    def test_reverse_sort(self):
        """降序排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = insertion_sort(arr, reverse=True)
        self.assertEqual(result, [9, 8, 5, 3, 2, 1])
    
    def test_in_place(self):
        """原地排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = insertion_sort(arr, in_place=True)
        self.assertEqual(arr, [1, 2, 3, 5, 8, 9])
    
    def test_already_sorted(self):
        """已排序数组测试"""
        arr = [1, 2, 3, 4, 5]
        result = insertion_sort(arr)
        self.assertEqual(result, [1, 2, 3, 4, 5])
    
    def test_empty_array(self):
        """空数组测试"""
        self.assertEqual(insertion_sort([]), [])
    
    def test_single_element(self):
        """单元素测试"""
        self.assertEqual(insertion_sort([42]), [42])
    
    def test_with_key(self):
        """使用 key 函数排序"""
        arr = [{'val': 3}, {'val': 1}, {'val': 2}]
        result = insertion_sort(arr, key=lambda x: x['val'])
        self.assertEqual([x['val'] for x in result], [1, 2, 3])


class TestSelectionSort(unittest.TestCase):
    """选择排序测试"""
    
    def test_basic_sort(self):
        """基础排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = selection_sort(arr)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
    
    def test_reverse_sort(self):
        """降序排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = selection_sort(arr, reverse=True)
        self.assertEqual(result, [9, 8, 5, 3, 2, 1])
    
    def test_empty_array(self):
        """空数组测试"""
        self.assertEqual(selection_sort([]), [])
    
    def test_single_element(self):
        """单元素测试"""
        self.assertEqual(selection_sort([42]), [42])
    
    def test_all_same(self):
        """全部相同元素测试"""
        arr = [5, 5, 5, 5]
        self.assertEqual(selection_sort(arr), [5, 5, 5, 5])


class TestBubbleSort(unittest.TestCase):
    """冒泡排序测试"""
    
    def test_basic_sort(self):
        """基础排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = bubble_sort(arr)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
    
    def test_reverse_sort(self):
        """降序排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = bubble_sort(arr, reverse=True)
        self.assertEqual(result, [9, 8, 5, 3, 2, 1])
    
    def test_optimized_version(self):
        """优化版本测试"""
        arr = [1, 2, 3, 4, 5]  # 已排序
        result = bubble_sort(arr, optimized=True)
        self.assertEqual(result, [1, 2, 3, 4, 5])
    
    def test_non_optimized_version(self):
        """非优化版本测试"""
        arr = [1, 2, 3, 4, 5]
        result = bubble_sort(arr, optimized=False)
        self.assertEqual(result, [1, 2, 3, 4, 5])
    
    def test_empty_array(self):
        """空数组测试"""
        self.assertEqual(bubble_sort([]), [])
    
    def test_single_element(self):
        """单元素测试"""
        self.assertEqual(bubble_sort([42]), [42])


class TestShellSort(unittest.TestCase):
    """希尔排序测试"""
    
    def test_basic_sort(self):
        """基础排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = shell_sort(arr)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
    
    def test_reverse_sort(self):
        """降序排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = shell_sort(arr, reverse=True)
        self.assertEqual(result, [9, 8, 5, 3, 2, 1])
    
    def test_custom_gaps(self):
        """自定义间隔序列测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = shell_sort(arr, gaps=[4, 2, 1])
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
    
    def test_empty_array(self):
        """空数组测试"""
        self.assertEqual(shell_sort([]), [])
    
    def test_single_element(self):
        """单元素测试"""
        self.assertEqual(shell_sort([42]), [42])
    
    def test_large_array(self):
        """大数组测试"""
        arr = list(range(1000, 0, -1))
        result = shell_sort(arr)
        self.assertEqual(result, list(range(1, 1001)))


class TestCountingSort(unittest.TestCase):
    """计数排序测试"""
    
    def test_basic_sort(self):
        """基础排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = counting_sort(arr)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
    
    def test_reverse_sort(self):
        """降序排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = counting_sort(arr, reverse=True)
        self.assertEqual(result, [9, 8, 5, 3, 2, 1])
    
    def test_with_range(self):
        """指定范围测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = counting_sort(arr, min_val=0, max_val=10)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
    
    def test_empty_array(self):
        """空数组测试"""
        self.assertEqual(counting_sort([]), [])
    
    def test_single_element(self):
        """单元素测试"""
        self.assertEqual(counting_sort([42]), [42])
    
    def test_duplicates(self):
        """重复元素测试"""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5]
        result = counting_sort(arr)
        self.assertEqual(result, [1, 1, 2, 3, 4, 5, 5, 6, 9])
    
    def test_negative_numbers(self):
        """负数测试"""
        arr = [3, -1, 4, -5, 2]
        result = counting_sort(arr)
        self.assertEqual(result, [-5, -1, 2, 3, 4])
    
    def test_non_integer_raises(self):
        """非整数抛出异常测试"""
        with self.assertRaises(TypeError):
            counting_sort([1.5, 2.5, 3.5])
    
    def test_large_values(self):
        """大值测试"""
        arr = [1000000, 500000, 750000]
        result = counting_sort(arr)
        self.assertEqual(result, [500000, 750000, 1000000])


class TestBucketSort(unittest.TestCase):
    """桶排序测试"""
    
    def test_basic_sort(self):
        """基础排序测试"""
        arr = [0.5, 0.2, 0.8, 0.1, 0.9, 0.3]
        result = bucket_sort(arr)
        self.assertEqual(result, [0.1, 0.2, 0.3, 0.5, 0.8, 0.9])
    
    def test_reverse_sort(self):
        """降序排序测试"""
        arr = [0.5, 0.2, 0.8, 0.1, 0.9, 0.3]
        result = bucket_sort(arr, reverse=True)
        self.assertEqual(result, [0.9, 0.8, 0.5, 0.3, 0.2, 0.1])
    
    def test_custom_buckets(self):
        """自定义桶数量测试"""
        arr = [0.5, 0.2, 0.8, 0.1, 0.9, 0.3]
        result = bucket_sort(arr, num_buckets=5)
        self.assertEqual(result, [0.1, 0.2, 0.3, 0.5, 0.8, 0.9])
    
    def test_empty_array(self):
        """空数组测试"""
        self.assertEqual(bucket_sort([]), [])
    
    def test_single_element(self):
        """单元素测试"""
        self.assertEqual(bucket_sort([0.5]), [0.5])
    
    def test_with_range(self):
        """指定范围测试"""
        arr = [0.5, 0.2, 0.8]
        result = bucket_sort(arr, min_val=0.0, max_val=1.0)
        self.assertEqual(result, [0.2, 0.5, 0.8])
    
    def test_all_same(self):
        """全部相同元素测试"""
        arr = [0.5, 0.5, 0.5]
        result = bucket_sort(arr)
        self.assertEqual(result, [0.5, 0.5, 0.5])


class TestRadixSort(unittest.TestCase):
    """基数排序测试"""
    
    def test_basic_sort(self):
        """基础排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = radix_sort(arr)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
    
    def test_reverse_sort(self):
        """降序排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = radix_sort(arr, reverse=True)
        self.assertEqual(result, [9, 8, 5, 3, 2, 1])
    
    def test_different_base(self):
        """不同进制测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = radix_sort(arr, base=16)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
    
    def test_empty_array(self):
        """空数组测试"""
        self.assertEqual(radix_sort([]), [])
    
    def test_single_element(self):
        """单元素测试"""
        self.assertEqual(radix_sort([42]), [42])
    
    def test_negative_numbers(self):
        """负数测试"""
        arr = [3, -1, 4, -5, 2]
        result = radix_sort(arr)
        self.assertEqual(result, [-5, -1, 2, 3, 4])
    
    def test_large_numbers(self):
        """大数测试"""
        arr = [123456789, 987654321, 111111111]
        result = radix_sort(arr)
        self.assertEqual(result, [111111111, 123456789, 987654321])
    
    def test_non_integer_raises(self):
        """非整数抛出异常测试"""
        with self.assertRaises(TypeError):
            radix_sort([1.5, 2.5])


class TestTimSortLike(unittest.TestCase):
    """类 TimSort 测试"""
    
    def test_basic_sort(self):
        """基础排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = tim_sort_like(arr)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
    
    def test_small_array(self):
        """小数组测试（应使用插入排序）"""
        arr = [5, 2, 8, 1, 9]
        result = tim_sort_like(arr)
        self.assertEqual(result, [1, 2, 5, 8, 9])
    
    def test_large_array(self):
        """大数组测试（应使用归并排序）"""
        arr = list(range(100, 0, -1))
        result = tim_sort_like(arr)
        self.assertEqual(result, list(range(1, 101)))
    
    def test_empty_array(self):
        """空数组测试"""
        self.assertEqual(tim_sort_like([]), [])
    
    def test_single_element(self):
        """单元素测试"""
        self.assertEqual(tim_sort_like([42]), [42])


class TestCocktailSort(unittest.TestCase):
    """鸡尾酒排序测试"""
    
    def test_basic_sort(self):
        """基础排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = cocktail_sort(arr)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
    
    def test_reverse_sort(self):
        """降序排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = cocktail_sort(arr, reverse=True)
        self.assertEqual(result, [9, 8, 5, 3, 2, 1])
    
    def test_empty_array(self):
        """空数组测试"""
        self.assertEqual(cocktail_sort([]), [])
    
    def test_single_element(self):
        """单元素测试"""
        self.assertEqual(cocktail_sort([42]), [42])
    
    def test_already_sorted(self):
        """已排序数组测试"""
        arr = [1, 2, 3, 4, 5]
        result = cocktail_sort(arr)
        self.assertEqual(result, [1, 2, 3, 4, 5])


class TestGnomeSort(unittest.TestCase):
    """侏儒排序测试"""
    
    def test_basic_sort(self):
        """基础排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = gnome_sort(arr)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
    
    def test_reverse_sort(self):
        """降序排序测试"""
        arr = [5, 2, 8, 1, 9, 3]
        result = gnome_sort(arr, reverse=True)
        self.assertEqual(result, [9, 8, 5, 3, 2, 1])
    
    def test_empty_array(self):
        """空数组测试"""
        self.assertEqual(gnome_sort([]), [])
    
    def test_single_element(self):
        """单元素测试"""
        self.assertEqual(gnome_sort([42]), [42])
    
    def test_already_sorted(self):
        """已排序数组测试"""
        arr = [1, 2, 3, 4, 5]
        result = gnome_sort(arr)
        self.assertEqual(result, [1, 2, 3, 4, 5])


class TestSortByCustom(unittest.TestCase):
    """自定义比较函数排序测试"""
    
    def test_custom_comparator(self):
        """自定义比较函数测试"""
        arr = [5, 2, 8, 1, 9, 3]
        # 自定义：奇数在前，偶数在后，各自排序
        def comparator(a, b):
            if a % 2 != b % 2:
                return -1 if a % 2 == 1 else 1
            return a - b
        
        result = sort_by_custom(arr, comparator)
        self.assertEqual(result, [1, 3, 5, 9, 2, 8])
    
    def test_reverse_comparator(self):
        """反向比较函数测试"""
        arr = [5, 2, 8, 1]
        result = sort_by_custom(arr, lambda a, b: b - a)
        self.assertEqual(result, [8, 5, 2, 1])


class TestIsSorted(unittest.TestCase):
    """检查是否排序测试"""
    
    def test_sorted_array(self):
        """已排序数组"""
        self.assertTrue(is_sorted([1, 2, 3, 4, 5]))
    
    def test_unsorted_array(self):
        """未排序数组"""
        self.assertFalse(is_sorted([5, 2, 8, 1]))
    
    def test_reverse_sorted(self):
        """反向排序检查"""
        self.assertTrue(is_sorted([5, 4, 3, 2, 1], reverse=True))
    
    def test_with_key(self):
        """使用 key 函数检查"""
        arr = [{'val': 1}, {'val': 2}, {'val': 3}]
        self.assertTrue(is_sorted(arr, key=lambda x: x['val']))
    
    def test_empty_array(self):
        """空数组"""
        self.assertTrue(is_sorted([]))
    
    def test_single_element(self):
        """单元素"""
        self.assertTrue(is_sorted([42]))
    
    def test_all_same(self):
        """全部相同"""
        self.assertTrue(is_sorted([5, 5, 5, 5]))


class TestComplexityInfo(unittest.TestCase):
    """复杂度信息测试"""
    
    def test_get_complexity(self):
        """获取复杂度信息"""
        info = get_sort_algorithm_complexity()
        self.assertIn('quick_sort', info)
        self.assertIn('merge_sort', info)
        self.assertEqual(info['merge_sort']['stable'], True)
        self.assertEqual(info['quick_sort']['stable'], False)


class TestAlgorithmRecommendation(unittest.TestCase):
    """算法推荐测试"""
    
    def test_small_dataset(self):
        """小数据集推荐"""
        self.assertEqual(recommend_sort_algorithm(10), 'insertion_sort')
    
    def test_large_dataset_unstable(self):
        """大数据集非稳定推荐"""
        self.assertEqual(recommend_sort_algorithm(1000), 'quick_sort')
    
    def test_large_dataset_stable(self):
        """大数据集稳定推荐"""
        self.assertEqual(recommend_sort_algorithm(1000, require_stable=True), 'merge_sort')
    
    def test_integer_small_range(self):
        """整数小值域推荐"""
        result = recommend_sort_algorithm(100, is_integers=True, value_range=50)
        self.assertEqual(result, 'counting_sort')
    
    def test_integer_medium_range(self):
        """整数中等值域推荐"""
        result = recommend_sort_algorithm(100, is_integers=True, value_range=500)
        self.assertEqual(result, 'radix_sort')


class TestCrossAlgorithmConsistency(unittest.TestCase):
    """跨算法一致性测试"""
    
    def test_all_algorithms_same_result(self):
        """所有算法结果一致"""
        arr = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        expected = sorted(arr)
        
        algorithms = [
            quick_sort,
            merge_sort,
            heap_sort,
            insertion_sort,
            selection_sort,
            bubble_sort,
            shell_sort,
            counting_sort,
            radix_sort,
            tim_sort_like,
            cocktail_sort,
            gnome_sort,
        ]
        
        for algo in algorithms:
            result = algo(arr)
            self.assertEqual(result, expected, f"{algo.__name__} failed")
    
    def test_all_algorithms_reverse_consistent(self):
        """所有算法降序结果一致"""
        arr = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        expected = sorted(arr, reverse=True)
        
        algorithms = [
            quick_sort,
            merge_sort,
            heap_sort,
            insertion_sort,
            selection_sort,
            bubble_sort,
            shell_sort,
            counting_sort,
            radix_sort,
            cocktail_sort,
            gnome_sort,
        ]
        
        for algo in algorithms:
            result = algo(arr, reverse=True)
            self.assertEqual(result, expected, f"{algo.__name__} reverse failed")


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_very_large_numbers(self):
        """超大数测试"""
        arr = [10**18, 10**12, 10**15]
        result = quick_sort(arr)
        self.assertEqual(result, [10**12, 10**15, 10**18])
    
    def test_mixed_positive_negative(self):
        """正负混合测试"""
        arr = [-100, 100, -50, 50, 0]
        expected = sorted(arr)
        for algo in [quick_sort, merge_sort, heap_sort, counting_sort, radix_sort]:
            result = algo(arr)
            self.assertEqual(result, expected)
    
    def test_floating_point_precision(self):
        """浮点数精度测试"""
        arr = [0.1, 0.2, 0.3]
        result = bucket_sort(arr)
        self.assertAlmostEqual(result[0], 0.1)
        self.assertAlmostEqual(result[1], 0.2)
        self.assertAlmostEqual(result[2], 0.3)
    
    def test_string_sorting(self):
        """字符串排序测试"""
        arr = ['zzz', 'aaa', 'bbb', 'ccc']
        expected = sorted(arr)
        result = quick_sort(arr)
        self.assertEqual(result, expected)
    
    def test_tuple_sorting(self):
        """元组排序测试"""
        arr = [(3, 'c'), (1, 'a'), (2, 'b')]
        result = quick_sort(arr)
        self.assertEqual(result, [(1, 'a'), (2, 'b'), (3, 'c')])


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_sorting_1000_elements(self):
        """1000 元素排序性能"""
        arr = random.sample(range(10000), 1000)
        
        algorithms = {
            'quick_sort': quick_sort,
            'merge_sort': merge_sort,
            'heap_sort': heap_sort,
            'radix_sort': radix_sort,
        }
        
        for name, algo in algorithms.items():
            start = time.time()
            result = algo(arr)
            elapsed = time.time() - start
            
            # 验证结果正确
            self.assertEqual(result, sorted(arr))
            # 性能应在合理范围内（<1秒）
            self.assertLess(elapsed, 1.0, f"{name} too slow: {elapsed}s")


class TestStability(unittest.TestCase):
    """稳定性测试"""
    
    def test_merge_sort_stability(self):
        """归并排序稳定性验证"""
        arr = [(1, 'a'), (2, 'x'), (1, 'b'), (2, 'y'), (1, 'c')]
        result = merge_sort(arr, key=lambda x: x[0])
        
        # (1, 'a') 应在 (1, 'b') 前面，(1, 'b') 应在 (1, 'c') 前面
        ones = [x for x in result if x[0] == 1]
        self.assertEqual(ones, [(1, 'a'), (1, 'b'), (1, 'c')])
    
    def test_insertion_sort_stability(self):
        """插入排序稳定性验证"""
        arr = [(1, 'a'), (2, 'x'), (1, 'b'), (2, 'y'), (1, 'c')]
        result = insertion_sort(arr, key=lambda x: x[0])
        
        ones = [x for x in result if x[0] == 1]
        self.assertEqual(ones, [(1, 'a'), (1, 'b'), (1, 'c')])
    
    def test_bubble_sort_stability(self):
        """冒泡排序稳定性验证"""
        arr = [(1, 'a'), (2, 'x'), (1, 'b'), (2, 'y'), (1, 'c')]
        result = bubble_sort(arr, key=lambda x: x[0])
        
        ones = [x for x in result if x[0] == 1]
        self.assertEqual(ones, [(1, 'a'), (1, 'b'), (1, 'c')])


if __name__ == '__main__':
    unittest.main(verbosity=2)