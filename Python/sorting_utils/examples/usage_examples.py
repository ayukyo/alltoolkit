"""
sorting_utils 使用示例
展示各种排序算法的实际应用场景
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


def example_basic_sorting():
    """基础排序示例"""
    print("=== 基础排序示例 ===")
    
    # 整数排序
    numbers = [64, 34, 25, 12, 22, 11, 90]
    print(f"原始数组: {numbers}")
    
    # 快速排序
    sorted_numbers = quick_sort(numbers)
    print(f"快速排序结果: {sorted_numbers}")
    
    # 降序
    descending = quick_sort(numbers, reverse=True)
    print(f"降序排列: {descending}")


def example_with_key_function():
    """使用 key 函数排序示例"""
    print("\n=== Key 函数示例 ===")
    
    # 按字符串长度排序
    words = ['elephant', 'cat', 'dog', 'butterfly', 'ant']
    by_length = quick_sort(words, key=lambda x: len(x))
    print(f"按长度排序: {by_length}")
    
    # 按对象的属性排序
    students = [
        {'name': 'Alice', 'score': 85},
        {'name': 'Bob', 'score': 92},
        {'name': 'Charlie', 'score': 78},
    ]
    by_score = merge_sort(students, key=lambda x: x['score'], reverse=True)
    print(f"按分数降序: {[s['name'] for s in by_score]}")


def example_integer_specific_algorithms():
    """整数专用算法示例"""
    print("\n=== 整数专用算法 ===")
    
    # 计数排序 - 值域有限
    small_range = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    counted = counting_sort(small_range)
    print(f"计数排序: {counted}")
    
    # 基数排序 - 大整数
    large_numbers = [12345678, 98765, 1111111, 500, 999999]
    radix_sorted = radix_sort(large_numbers)
    print(f"基数排序: {radix_sorted}")
    
    # 带负数
    with_negative = [100, -50, 75, -25, 0, 50]
    negative_sorted = radix_sort(with_negative)
    print(f"负数排序: {negative_sorted}")


def example_float_specific_algorithm():
    """浮点数专用算法示例"""
    print("\n=== 浮点数专用算法 ===")
    
    # 桶排序
    floats = [0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]
    bucket_sorted = bucket_sort(floats)
    print(f"桶排序: {[f'{x:.2f}' for x in bucket_sorted]}")


def example_in_place_sorting():
    """原地排序示例"""
    print("\n=== 原地排序示例 ===")
    
    arr = [64, 34, 25, 12, 22]
    print(f"原始数组: {arr}")
    
    # 原地快速排序
    quick_sort(arr, in_place=True)
    print(f"原地排序后: {arr}")
    
    # 原地插入排序
    arr2 = [5, 2, 4, 6, 1, 3]
    print(f"原始数组2: {arr2}")
    insertion_sort(arr2, in_place=True)
    print(f"原地插入排序: {arr2}")


def example_custom_comparator():
    """自定义比较函数示例"""
    print("\n=== 自定义比较函数 ===")
    
    # 偶数在前，奇数在后，各自升序
    def even_first(a, b):
        if a % 2 == 0 and b % 2 != 0:
            return -1
        if a % 2 != 0 and b % 2 == 0:
            return 1
        return a - b
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    custom_sorted = sort_by_custom(numbers, even_first)
    print(f"偶数在前: {custom_sorted}")


def example_check_sorted():
    """检查是否已排序示例"""
    print("\n=== 检查排序状态 ===")
    
    sorted_arr = [1, 2, 3, 4, 5]
    unsorted_arr = [5, 3, 1, 4, 2]
    descending_arr = [5, 4, 3, 2, 1]
    
    print(f"{sorted_arr} 已排序? {is_sorted(sorted_arr)}")
    print(f"{unsorted_arr} 已排序? {is_sorted(unsorted_arr)}")
    print(f"{descending_arr} 降序? {is_sorted(descending_arr, reverse=True)}")


def example_stability():
    """稳定性示例"""
    print("\n=== 排序稳定性演示 ===")
    
    # 带标签的相同值
    data = [(1, 'a'), (2, 'x'), (1, 'b'), (2, 'y'), (1, 'c')]
    print(f"原始数据: {data}")
    
    # 稳定排序（归并）
    stable_result = merge_sort(data, key=lambda x: x[0])
    print(f"稳定排序: {stable_result}")
    # 1 的顺序保持: a, b, c
    
    # 非稳定排序（快速）可能改变顺序
    quick_result = quick_sort(data, key=lambda x: x[0])
    print(f"快速排序: {quick_result}")


def example_algorithm_recommendation():
    """算法推荐示例"""
    print("\n=== 算法推荐系统 ===")
    
    # 小数据集
    small_algo = recommend_sort_algorithm(n=20)
    print(f"20 个元素推荐: {small_algo}")
    
    # 大数据集
    large_algo = recommend_sort_algorithm(n=10000)
    print(f"10000 个元素推荐: {large_algo}")
    
    # 需要稳定排序
    stable_algo = recommend_sort_algorithm(n=10000, require_stable=True)
    print(f"需要稳定排序: {stable_algo}")
    
    # 整数，小值域
    int_small_range = recommend_sort_algorithm(
        n=1000, is_integers=True, value_range=100
    )
    print(f"整数小值域推荐: {int_small_range}")
    
    # 整数，大值域
    int_large_range = recommend_sort_algorithm(
        n=1000, is_integers=True, value_range=100000
    )
    print(f"整数大值域推荐: {int_large_range}")


def example_complexity_info():
    """复杂度信息示例"""
    print("\n=== 算法复杂度信息 ===")
    
    info = get_sort_algorithm_complexity()
    
    print("各算法复杂度:")
    print("-" * 60)
    for algo, details in info.items():
        print(f"{algo}:")
        print(f"  最佳: {details['best']}, 平均: {details['average']}")
        print(f"  最坏: {details['worst']}, 稳定: {details['stable']}")
    print("-" * 60)


def example_special_algorithms():
    """特殊算法示例"""
    print("\n=== 特殊算法演示 ===")
    
    # 鸡尾酒排序
    arr = [5, 1, 4, 2, 8, 0, 2]
    cocktail_result = cocktail_sort(arr)
    print(f"鸡尾酒排序: {cocktail_result}")
    
    # 侏儒排序
    gnome_result = gnome_sort(arr)
    print(f"侏儒排序: {gnome_result}")
    
    # 类 TimSort
    tim_result = tim_sort_like(arr)
    print(f"类 TimSort: {tim_result}")
    
    # 希尔排序
    shell_result = shell_sort(arr)
    print(f"希尔排序: {shell_result}")


def example_cross_comparison():
    """跨算法对比示例"""
    print("\n=== 跨算法对比 ===")
    
    test_arr = [64, 34, 25, 12, 22, 11, 90]
    expected = sorted(test_arr)
    
    algorithms = [
        ('快速排序', quick_sort),
        ('归并排序', merge_sort),
        ('堆排序', heap_sort),
        ('插入排序', insertion_sort),
        ('选择排序', selection_sort),
        ('冒泡排序', bubble_sort),
        ('计数排序', counting_sort),
        ('基数排序', radix_sort),
    ]
    
    print(f"原始数组: {test_arr}")
    print(f"期望结果: {expected}")
    print()
    
    for name, algo in algorithms:
        result = algo(test_arr)
        match = result == expected
        print(f"{name}: {result} {'✅' if match else '❌'}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("sorting_utils 使用示例")
    print("=" * 60)
    
    example_basic_sorting()
    example_with_key_function()
    example_integer_specific_algorithms()
    example_float_specific_algorithm()
    example_in_place_sorting()
    example_custom_comparator()
    example_check_sorted()
    example_stability()
    example_algorithm_recommendation()
    example_complexity_info()
    example_special_algorithms()
    example_cross_comparison()
    
    print("\n" + "=" * 60)
    print("示例运行完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()