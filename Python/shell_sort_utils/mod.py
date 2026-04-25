#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shell Sort Utils - 希尔排序工具库

希尔排序（Shell Sort）是插入排序的优化版本，通过使用递减的间隔序列，
使元素能够大跨度移动，从而提高排序效率。

时间复杂度:
    - 最好: O(n log n)
    - 平均: O(n^1.3) 到 O(n log²n)（取决于间隔序列）
    - 最坏: O(n²)（某些间隔序列）

空间复杂度: O(1)

特点:
    - 原地排序，空间效率高
    - 对中等规模数据效率较高
    - 不稳定排序
    - 对部分有序数据效率更高

零外部依赖，纯 Python 标准库实现。
"""

from typing import List, TypeVar, Callable, Optional, Tuple, Generator, Any
from dataclasses import dataclass
from enum import Enum

T = TypeVar('T')
U = TypeVar('U')


class GapSequence(Enum):
    """间隔序列类型"""
    SHELL = "shell"           # 原始 Shell 序列: n//2, n//4, ...
    KNUTH = "knuth"           # Knuth 序列: 1, 4, 13, 40, 121, ...
    HIBBARD = "hibbard"       # Hibbard 序列: 1, 3, 7, 15, 31, ...
    SEDGEWICK = "sedgewick"   # Sedgewick 序列: 1, 5, 19, 41, 109, ...
    CIURA = "ciura"           # Ciura 序列: 1, 4, 10, 23, 57, 132, 301, 701, ...
    TOKUDA = "tokuda"         # Tokuda 序列: 1, 4, 9, 20, 45, 101, ...
    PRATT = "pratt"           # Pratt 序列 (3-smooth): 1, 2, 3, 4, 6, 8, 9, ...


@dataclass
class SortResult:
    """排序结果"""
    data: List[T]              # 排序后的数据
    comparisons: int           # 比较次数
    swaps: int                 # 交换次数
    gap_sequence: List[int]    # 使用的间隔序列
    passes: int                # 扫描轮数


def generate_shell_gaps(n: int) -> List[int]:
    """
    生成原始 Shell 间隔序列
    
    序列: n//2, n//4, n//8, ..., 1
    
    时间复杂度: O(n²) 最坏情况
    
    Args:
        n: 数据长度
    
    Returns:
        间隔序列（从大到小）
    """
    gaps = []
    gap = n // 2
    while gap > 0:
        gaps.append(gap)
        gap //= 2
    return gaps


def generate_knuth_gaps(n: int) -> List[int]:
    """
    生成 Knuth 间隔序列
    
    序列: ..., 121, 40, 13, 4, 1
    公式: h = 3h + 1, 从 h=1 开始
    
    时间复杂度: O(n^(3/2))
    
    Args:
        n: 数据长度
    
    Returns:
        间隔序列（从大到小）
    """
    gaps = []
    h = 1
    while h < n:
        gaps.append(h)
        h = 3 * h + 1
    return gaps[::-1]  # 反转为从大到小


def generate_hibbard_gaps(n: int) -> List[int]:
    """
    生成 Hibbard 间隔序列
    
    序列: ..., 31, 15, 7, 3, 1
    公式: 2^k - 1
    
    时间复杂度: O(n^(3/2))
    
    Args:
        n: 数据长度
    
    Returns:
        间隔序列（从大到小）
    """
    gaps = []
    k = 1
    while (2**k - 1) < n:
        gaps.append(2**k - 1)
        k += 1
    return gaps[::-1]


def generate_sedgewick_gaps(n: int) -> List[int]:
    """
    生成 Sedgewick 间隔序列
    
    结合两种公式生成更优的序列
    
    时间复杂度: O(n^(4/3))
    
    Args:
        n: 数据长度
    
    Returns:
        间隔序列（从大到小）
    """
    gaps = []
    k = 0
    
    while True:
        # 两种公式交替使用
        if k % 2 == 0:
            gap = 9 * (2**k - 2**(k//2)) + 1
        else:
            gap = 8 * (2**k - 2**((k+1)//2)) + 1
        
        if gap >= n:
            break
        gaps.append(gap)
        k += 1
    
    return gaps[::-1]


def generate_ciura_gaps(n: int) -> List[int]:
    """
    生成 Ciura 间隔序列
    
    已知的最优经验序列，通过实验得出
    
    时间复杂度: 约 O(n log n)
    
    Args:
        n: 数据长度
    
    Returns:
        间隔序列（从大到小）
    """
    # Ciura 的经验最优序列
    ciura_sequence = [701, 301, 132, 57, 23, 10, 4, 1]
    
    gaps = []
    ratio = 2.25  # 经验比例
    
    # 从 701 开始扩展（如果需要更大的间隔）
    gap = 701
    while gap < n:
        gaps.append(int(gap))
        gap = int(gap * ratio)
    
    # 合并并返回
    gaps = gaps[::-1] + ciura_sequence
    
    # 过滤掉超过 n 的间隔
    return [g for g in gaps if g < n or g == 1]


def generate_tokuda_gaps(n: int) -> List[int]:
    """
    生成 Tokuda 间隔序列
    
    公式: h_k = ceil((9 * (9/4)^(k-1) - 4) / 5)
    
    时间复杂度: 约 O(n log n)
    
    Args:
        n: 数据长度
    
    Returns:
        间隔序列（从大到小）
    """
    import math
    
    gaps = []
    k = 1
    while True:
        gap = math.ceil((9 * (9/4)**(k-1) - 4) / 5)
        if gap > n:
            break
        gaps.append(gap)
        k += 1
    
    return gaps[::-1]


def generate_pratt_gaps(n: int) -> List[int]:
    """
    生成 Pratt 间隔序列（3-smooth 数）
    
    只包含 2^a * 3^b 形式的数
    
    时间复杂度: O(n log²n)
    
    Args:
        n: 数据长度
    
    Returns:
        间隔序列（从大到小）
    """
    gaps = set()
    
    # 生成所有 2^a * 3^b < n 的数
    a = 0
    while 2**a < n:
        b = 0
        while 2**a * 3**b < n:
            gaps.add(2**a * 3**b)
            b += 1
        a += 1
    
    return sorted(gaps, reverse=True)


def get_gap_sequence(n: int, sequence: GapSequence = GapSequence.CIURA) -> List[int]:
    """
    获取指定类型的间隔序列
    
    Args:
        n: 数据长度
        sequence: 间隔序列类型
    
    Returns:
        间隔序列（从大到小）
    """
    generators = {
        GapSequence.SHELL: generate_shell_gaps,
        GapSequence.KNUTH: generate_knuth_gaps,
        GapSequence.HIBBARD: generate_hibbard_gaps,
        GapSequence.SEDGEWICK: generate_sedgewick_gaps,
        GapSequence.CIURA: generate_ciura_gaps,
        GapSequence.TOKUDA: generate_tokuda_gaps,
        GapSequence.PRATT: generate_pratt_gaps,
    }
    
    return generators[sequence](n)


def shell_sort(
    data: List[T],
    gap_sequence: GapSequence = GapSequence.CIURA,
    reverse: bool = False,
    key: Optional[Callable[[T], any]] = None,
    inplace: bool = False
) -> SortResult:
    """
    希尔排序
    
    使用指定间隔序列对数据进行排序。
    
    Args:
        data: 待排序数据
        gap_sequence: 间隔序列类型
        reverse: 是否降序排序
        key: 排序键函数
        inplace: 是否原地排序
    
    Returns:
        SortResult 对象，包含排序结果和统计信息
    
    Example:
        >>> result = shell_sort([64, 34, 25, 12, 22, 11, 90])
        >>> result.data
        [11, 12, 22, 25, 34, 64, 90]
        >>> result.comparisons
        15
    """
    if not inplace:
        data = data.copy()
    
    n = len(data)
    if n <= 1:
        return SortResult(
            data=data,
            comparisons=0,
            swaps=0,
            gap_sequence=[],
            passes=0
        )
    
    # 生成间隔序列
    gaps = get_gap_sequence(n, gap_sequence)
    
    comparisons = 0
    swaps = 0
    passes = 0
    
    # 提取键值
    def get_key(x):
        return key(x) if key else x
    
    # 比较函数
    def compare(a, b):
        nonlocal comparisons
        comparisons += 1
        ka, kb = get_key(a), get_key(b)
        if reverse:
            return ka > kb
        return ka < kb
    
    # 对每个间隔进行插入排序
    for gap in gaps:
        passes += 1
        for i in range(gap, n):
            temp = data[i]
            j = i
            
            # 插入排序
            while j >= gap and compare(temp, data[j - gap]):
                data[j] = data[j - gap]
                swaps += 1
                j -= gap
            
            if j != i:
                data[j] = temp
                swaps += 1
    
    return SortResult(
        data=data,
        comparisons=comparisons,
        swaps=swaps,
        gap_sequence=gaps,
        passes=passes
    )


def shell_sort_with_trace(
    data: List[T],
    gap_sequence: GapSequence = GapSequence.CIURA,
    reverse: bool = False,
    key: Optional[Callable[[T], any]] = None
) -> Generator[Tuple[List[T], int, int], None, None]:
    """
    带跟踪的希尔排序
    
    生成每一步的状态，用于可视化和教学。
    
    Args:
        data: 待排序数据
        gap_sequence: 间隔序列类型
        reverse: 是否降序排序
        key: 排序键函数
    
    Yields:
        (当前状态, 当前间隔, 当前索引)
    
    Example:
        >>> for state, gap, idx in shell_sort_with_trace([5, 3, 1, 4, 2]):
        ...     print(f"gap={gap}, i={idx}: {state}")
    """
    data = data.copy()
    n = len(data)
    
    if n <= 1:
        yield (data, 0, 0)
        return
    
    gaps = get_gap_sequence(n, gap_sequence)
    
    def get_key(x):
        return key(x) if key else x
    
    def compare(a, b):
        ka, kb = get_key(a), get_key(b)
        if reverse:
            return ka > kb
        return ka < kb
    
    for gap in gaps:
        for i in range(gap, n):
            temp = data[i]
            j = i
            
            while j >= gap and compare(temp, data[j - gap]):
                data[j] = data[j - gap]
                j -= gap
                yield (data.copy(), gap, j)
            
            data[j] = temp
            yield (data.copy(), gap, i)


def shell_sort_optimized(
    data: List[T],
    reverse: bool = False,
    key: Optional[Callable[[T], any]] = None,
    inplace: bool = False
) -> SortResult:
    """
    优化的希尔排序
    
    根据数据特征自动选择最优间隔序列和优化策略：
    - 小数据量 (< 50): 使用 Knuth 序列
    - 中等数据量 (< 1000): 使用 Ciura 序列
    - 大数据量: 使用 Sedgewick 序列
    - 已部分有序: 检测并优化
    
    Args:
        data: 待排序数据
        reverse: 是否降序排序
        key: 排序键函数
        inplace: 是否原地排序
    
    Returns:
        SortResult 对象
    """
    if not inplace:
        data = data.copy()
    
    n = len(data)
    if n <= 1:
        return SortResult(data=data, comparisons=0, swaps=0, gap_sequence=[], passes=0)
    
    # 检测是否已部分有序
    def count_inversions(arr):
        """
        计算逆序对数量（优化版本）
        
        使用归并排序方法计算，时间复杂度 O(n log n)，
        远优于暴力 O(n²) 方法。
        
        Args:
            arr: 数组
        
        Returns:
            逆序对数量
        
        Note:
            优化版本：使用归并排序的 O(n log n) 算法，
            边界处理：空数组、单元素数组返回 0。
        """
        # 边界处理：空或单元素数组
        n = len(arr)
        if n <= 1:
            return 0
        
        # 对于小数组使用简单方法（避免递归开销）
        if n <= 100:
            inv = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if arr[i] > arr[j]:
                        inv += 1
            return inv
        
        # 使用归并排序方法计算逆序对（O(n log n)）
        def _merge_count(left, right):
            """合并两个有序数组并计算跨数组逆序对"""
            merged = []
            i, j = 0, 0
            inversions = 0
            
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    # left[i] > right[j]，形成逆序对
                    # 左数组剩余元素都与 right[j] 构成逆序对
                    merged.append(right[j])
                    inversions += len(left) - i
                    j += 1
            
            merged.extend(left[i:])
            merged.extend(right[j:])
            return merged, inversions
        
        def _sort_count(arr):
            """递归排序并计算逆序对"""
            if len(arr) <= 1:
                return arr, 0
            
            mid = len(arr) // 2
            left, left_inv = _sort_count(arr[:mid])
            right, right_inv = _sort_count(arr[mid:])
            merged, cross_inv = _merge_count(left, right)
            
            return merged, left_inv + right_inv + cross_inv
        
        _, total_inv = _sort_count(list(arr))  # 复制以避免修改原数组
        return total_inv
    
    # 根据数据特征选择间隔序列
    if n < 50:
        gap_seq = GapSequence.KNUTH
    elif n < 1000:
        gap_seq = GapSequence.CIURA
    else:
        # 检测有序程度
        sample_arr = [key(x) if key else x for x in data[:min(100, n)]]
        inv_count = count_inversions(sample_arr)
        max_inv = len(sample_arr) * (len(sample_arr) - 1) // 2
        order_ratio = 1 - (inv_count / max_inv if max_inv > 0 else 0)
        
        if order_ratio > 0.8:
            # 高度有序，使用简单序列
            gap_seq = GapSequence.SHELL
        else:
            gap_seq = GapSequence.SEDGEWICK
    
    return shell_sort(data, gap_seq, reverse, key, inplace=True)


def is_sorted(data: List[T], reverse: bool = False, key: Optional[Callable[[T], any]] = None) -> bool:
    """
    检查数据是否已排序
    
    Args:
        data: 待检查数据
        reverse: 是否检查降序
        key: 比较键函数
    
    Returns:
        是否已排序
    """
    if len(data) <= 1:
        return True
    
    def get_key(x):
        return key(x) if key else x
    
    for i in range(len(data) - 1):
        k1, k2 = get_key(data[i]), get_key(data[i + 1])
        if reverse:
            if k1 < k2:
                return False
        else:
            if k1 > k2:
                return False
    return True


def shell_sort_pair(data1: List[T], data2: List[U], 
                    gap_sequence: GapSequence = GapSequence.CIURA,
                    reverse: bool = False,
                    key: Optional[Callable[[T], any]] = None) -> Tuple[List[T], List[U]]:
    """
    联合排序两个列表
    
    根据第一个列表排序，同时调整第二个列表的顺序。
    
    Args:
        data1: 主排序列表
        data2: 联动排序列表
        gap_sequence: 间隔序列类型
        reverse: 是否降序排序
        key: 排序键函数
    
    Returns:
        排序后的两个列表
    
    Example:
        >>> names = ['Alice', 'Bob', 'Charlie']
        >>> scores = [85, 92, 78]
        >>> sorted_names, sorted_scores = shell_sort_pair(scores, names)
        >>> sorted_names, sorted_scores
        ([78, 85, 92], ['Charlie', 'Alice', 'Bob'])
    """
    if len(data1) != len(data2):
        raise ValueError("两个列表长度必须相同")
    
    # 创建索引列表
    indices = list(range(len(data1)))
    
    # 排序索引
    def get_key(idx):
        return key(data1[idx]) if key else data1[idx]
    
    # 使用自定义比较的 shell sort
    n = len(indices)
    gaps = get_gap_sequence(n, gap_sequence)
    
    def compare(idx1, idx2):
        k1, k2 = get_key(idx1), get_key(idx2)
        if reverse:
            return k1 > k2
        return k1 < k2
    
    for gap in gaps:
        for i in range(gap, n):
            temp_idx = indices[i]
            j = i
            
            while j >= gap and compare(temp_idx, indices[j - gap]):
                indices[j] = indices[j - gap]
                j -= gap
            
            indices[j] = temp_idx
    
    # 根据排序后的索引重排两个列表
    return (
        [data1[i] for i in indices],
        [data2[i] for i in indices]
    )


def benchmark_gaps(data: List[T], key: Optional[Callable[[T], any]] = None) -> dict:
    """
    比较不同间隔序列的性能
    
    Args:
        data: 测试数据
        key: 排序键函数
    
    Returns:
        各间隔序列的性能统计
    """
    results = {}
    
    for seq in GapSequence:
        result = shell_sort(data, seq, key=key)
        results[seq.value] = {
            'comparisons': result.comparisons,
            'swaps': result.swaps,
            'passes': result.passes,
            'gaps': result.gap_sequence
        }
    
    return results


# 便捷函数别名
def shellsort(data: List[T], **kwargs) -> List[T]:
    """shell_sort 的别名，只返回排序后的数据"""
    return shell_sort(data, **kwargs).data


def sort(data: List[T], **kwargs) -> List[T]:
    """shell_sort 的简写，只返回排序后的数据"""
    return shell_sort(data, **kwargs).data


__all__ = [
    # 枚举
    'GapSequence',
    # 数据类
    'SortResult',
    # 间隔序列生成器
    'generate_shell_gaps',
    'generate_knuth_gaps',
    'generate_hibbard_gaps',
    'generate_sedgewick_gaps',
    'generate_ciura_gaps',
    'generate_tokuda_gaps',
    'generate_pratt_gaps',
    'get_gap_sequence',
    # 排序函数
    'shell_sort',
    'shell_sort_with_trace',
    'shell_sort_optimized',
    'shell_sort_pair',
    'shellsort',
    'sort',
    # 工具函数
    'is_sorted',
    'benchmark_gaps',
]