"""
AllToolkit - Benchmark Utils 对比示例

演示如何对比多个实现的性能。
"""

import sys
import os

# Add parent directory (benchmark_utils) to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from mod import (
    BenchmarkRunner,
    compare_implementations,
    BenchmarkComparison,
)


def example_sorting_algorithms():
    """示例 1: 排序算法对比"""
    print("=" * 60)
    print("示例 1: 排序算法性能对比")
    print("=" * 60)
    
    import random
    
    # 生成测试数据
    test_data = [random.randint(1, 10000) for _ in range(1000)]
    
    def bubble_sort(arr):
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    def selection_sort(arr):
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr
    
    def quick_sort(arr):
        arr = arr.copy()
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)
    
    def built_in_sort(arr):
        arr = arr.copy()
        arr.sort()
        return arr
    
    # 运行对比
    runner = BenchmarkRunner(warmup_iterations=2, verbose=True)
    
    comparison = runner.run_comparison({
        'bubble_sort': lambda: bubble_sort(test_data),
        'selection_sort': lambda: selection_sort(test_data),
        'quick_sort': lambda: quick_sort(test_data),
        'built_in_sort': lambda: built_in_sort(test_data),
    }, iterations=100)
    
    # 设置基线（使用内置排序作为参考）
    comparison.set_baseline('built_in_sort')
    
    # 显示相对性能
    print("\n相对性能（相对于内置 sort）:")
    relative = comparison.get_relative_performance()
    for name, ratio in sorted(relative.items(), key=lambda x: x[1], reverse=True):
        speed = "更快" if ratio > 1 else "更慢"
        print(f"  {name}: {ratio:.2f}x {speed}")
    
    print()


def example_string_concatenation():
    """示例 2: 字符串拼接方法对比"""
    print("=" * 60)
    print("示例 2: 字符串拼接方法对比")
    print("=" * 60)
    
    def method_join():
        return ''.join([str(i) for i in range(1000)])
    
    def method_plus():
        result = ''
        for i in range(1000):
            result += str(i)
        return result
    
    def method_list_append():
        result = []
        for i in range(1000):
            result.append(str(i))
        return ''.join(result)
    
    def method_generator():
        return ''.join(str(i) for i in range(1000))
    
    comparison = compare_implementations(
        {
            'join_list': method_join,
            'plus_operator': method_plus,
            'list_append': method_list_append,
            'generator': method_generator,
        },
        iterations=500,
    )
    
    comparison.set_baseline('join_list')
    
    print("\n相对性能（相对于 join）:")
    relative = comparison.get_relative_performance()
    for name, ratio in sorted(relative.items(), key=lambda x: x[1], reverse=True):
        print(f"  {name}: {ratio:.2f}x")
    
    print()


def example_search_algorithms():
    """示例 3: 搜索算法对比"""
    print("=" * 60)
    print("示例 3: 搜索算法性能对比")
    print("=" * 60)
    
    # 准备有序数据
    sorted_data = list(range(10000))
    target = 5000
    
    def linear_search():
        for i, val in enumerate(sorted_data):
            if val == target:
                return i
        return -1
    
    def binary_search():
        left, right = 0, len(sorted_data) - 1
        while left <= right:
            mid = (left + right) // 2
            if sorted_data[mid] == target:
                return mid
            elif sorted_data[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    
    def built_in_index():
        try:
            return sorted_data.index(target)
        except ValueError:
            return -1
    
    runner = BenchmarkRunner(warmup_iterations=3, verbose=True)
    
    comparison = runner.run_comparison({
        'linear_search': linear_search,
        'binary_search': binary_search,
        'built_in_index': built_in_index,
    }, iterations=1000)
    
    comparison.set_baseline('binary_search')
    
    print("\n相对性能（相对于二分查找）:")
    relative = comparison.get_relative_performance()
    for name, ratio in sorted(relative.items(), key=lambda x: x[1], reverse=True):
        print(f"  {name}: {ratio:.2f}x")
    
    print()


def example_data_structures():
    """示例 4: 数据结构操作对比"""
    print("=" * 60)
    print("示例 4: 数据结构操作对比")
    print("=" * 60)
    
    def list_lookup():
        data = list(range(10000))
        return 5000 in data
    
    def set_lookup():
        data = set(range(10000))
        return 5000 in data
    
    def dict_lookup():
        data = {i: i for i in range(10000)}
        return 5000 in data
    
    def list_append_1000():
        data = []
        for i in range(1000):
            data.append(i)
        return len(data)
    
    def list_extend_1000():
        data = []
        data.extend(range(1000))
        return len(data)
    
    def list_comprehension_1000():
        data = [i for i in range(1000)]
        return len(data)
    
    runner = BenchmarkRunner(warmup_iterations=2, verbose=True)
    
    # 查找操作对比
    print("\n查找操作对比:")
    lookup_comparison = runner.run_comparison({
        'list_lookup': list_lookup,
        'set_lookup': set_lookup,
        'dict_lookup': dict_lookup,
    }, iterations=10000)
    
    # 添加操作对比
    print("\n添加操作对比:")
    append_comparison = runner.run_comparison({
        'append_loop': list_append_1000,
        'extend': list_extend_1000,
        'comprehension': list_comprehension_1000,
    }, iterations=1000)
    
    print()


def example_export_results():
    """示例 5: 导出对比结果"""
    print("=" * 60)
    print("示例 5: 导出对比结果")
    print("=" * 60)
    
    runner = BenchmarkRunner(warmup_iterations=2, verbose=False)
    
    # 运行一些基准测试
    runner.run("test_1", lambda: sum(range(1000)), iterations=5000)
    runner.run("test_2", lambda: [i for i in range(1000)], iterations=5000)
    runner.run("test_3", lambda: list(range(1000)), iterations=5000)
    
    # 导出 JSON
    json_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'benchmark_results.json'
    )
    runner.export_json(json_path)
    print(f"✓ JSON 报告已导出：{json_path}")
    
    # 导出 Markdown
    md_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'benchmark_report.md'
    )
    runner.export_markdown(md_path)
    print(f"✓ Markdown 报告已导出：{md_path}")
    
    print()


def main():
    """运行所有对比示例"""
    print("\n🔧 AllToolkit Benchmark Utils 对比示例\n")
    
    example_sorting_algorithms()
    example_string_concatenation()
    example_search_algorithms()
    example_data_structures()
    example_export_results()
    
    print("=" * 60)
    print("所有对比示例完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
