"""
排序算法工具模块 (sorting_utils)
提供多种经典排序算法的零依赖实现

支持算法：
- 快速排序 (Quick Sort)
- 归并排序 (Merge Sort)
- 堆排序 (Heap Sort)
- 插入排序 (Insertion Sort)
- 选择排序 (Selection Sort)
- 冒泡排序 (Bubble Sort)
- 希尔排序 (Shell Sort)
- 计数排序 (Counting Sort)
- 桶排序 (Bucket Sort)
- 基数排序 (Radix Sort)

特性：
- 支持自定义比较函数
- 支持升序/降序
- 支持稳定排序
- 完全零外部依赖
"""

from typing import List, TypeVar, Callable, Optional, Any, Tuple
from functools import cmp_to_key

T = TypeVar('T')


def quick_sort(
    arr: List[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
    in_place: bool = False
) -> List[T]:
    """
    快速排序 - O(n log n) 平均, O(n²) 最坏
    
    Args:
        arr: 待排序列表
        key: 用于提取比较键的函数
        reverse: 是否降序排列
        in_place: 是否原地排序
    
    Returns:
        排序后的列表
    """
    if not arr:
        return arr if not in_place else arr
    
    if in_place:
        _quick_sort_inplace(arr, 0, len(arr) - 1, key, reverse)
        return arr
    else:
        result = arr.copy()
        _quick_sort_inplace(result, 0, len(result) - 1, key, reverse)
        return result


def _quick_sort_inplace(
    arr: List[T],
    low: int,
    high: int,
    key: Optional[Callable[[T], Any]],
    reverse: bool
) -> None:
    """原地快速排序的递归实现（使用尾递归优化和三数取中法）"""
    # 使用迭代代替递归避免栈溢出
    while low < high:
        # 小数组使用插入排序
        if high - low < 16:
            _insertion_sort_range(arr, low, high, key, reverse)
            return
        
        pi = _partition(arr, low, high, key, reverse)
        
        # 优先处理较小的子数组（尾递归优化）
        if pi - low < high - pi:
            _quick_sort_inplace(arr, low, pi - 1, key, reverse)
            low = pi + 1
        else:
            _quick_sort_inplace(arr, pi + 1, high, key, reverse)
            high = pi - 1


def _insertion_sort_range(
    arr: List[T],
    low: int,
    high: int,
    key: Optional[Callable[[T], Any]],
    reverse: bool
) -> None:
    """对范围内的元素进行插入排序"""
    for i in range(low + 1, high + 1):
        key_item = arr[i]
        key_val = key(key_item) if key else key_item
        j = i - 1
        
        while j >= low:
            current_val = key(arr[j]) if key else arr[j]
            if (current_val > key_val if not reverse else current_val < key_val):
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        
        arr[j + 1] = key_item


def _median_of_three(
    arr: List[T],
    low: int,
    high: int,
    key: Optional[Callable[[T], Any]]
) -> int:
    """三数取中法选择 pivot 索引"""
    mid = (low + high) // 2
    
    low_val = key(arr[low]) if key else arr[low]
    mid_val = key(arr[mid]) if key else arr[mid]
    high_val = key(arr[high]) if key else arr[high]
    
    # 找出中值
    if low_val <= mid_val <= high_val or high_val <= mid_val <= low_val:
        return mid
    elif mid_val <= low_val <= high_val or high_val <= low_val <= mid_val:
        return low
    else:
        return high


def _partition(
    arr: List[T],
    low: int,
    high: int,
    key: Optional[Callable[[T], Any]],
    reverse: bool
) -> int:
    """分区函数（使用三数取中法）"""
    # 选择更好的 pivot
    pivot_idx = _median_of_three(arr, low, high, key)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    
    pivot = arr[high]
    pivot_val = key(pivot) if key else pivot
    
    i = low - 1
    for j in range(low, high):
        current_val = key(arr[j]) if key else arr[j]
        
        should_swap = current_val < pivot_val if not reverse else current_val > pivot_val
        if should_swap:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def merge_sort(
    arr: List[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
    stable: bool = True
) -> List[T]:
    """
    归并排序 - O(n log n) 稳定排序
    
    Args:
        arr: 待排序列表
        key: 用于提取比较键的函数
        reverse: 是否降序排列
        stable: 是否保持稳定性
    
    Returns:
        排序后的列表
    """
    if len(arr) <= 1:
        return arr.copy()
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key, reverse, stable)
    right = merge_sort(arr[mid:], key, reverse, stable)
    
    return _merge(left, right, key, reverse, stable)


def _merge(
    left: List[T],
    right: List[T],
    key: Optional[Callable[[T], Any]],
    reverse: bool,
    stable: bool
) -> List[T]:
    """合并两个有序列表"""
    result = []
    i, j = 0, 0
    
    while i < len(left) and j < len(right):
        left_val = key(left[i]) if key else left[i]
        right_val = key(right[j]) if key else right[j]
        
        # 稳定性：相等时优先取左边的元素
        if stable:
            should_take_left = left_val <= right_val if not reverse else left_val >= right_val
        else:
            should_take_left = left_val < right_val if not reverse else left_val > right_val
        
        if should_take_left:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def heap_sort(
    arr: List[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False
) -> List[T]:
    """
    堆排序 - O(n log n)
    
    Args:
        arr: 待排序列表
        key: 用于提取比较键的函数
        reverse: 是否降序排列
    
    Returns:
        排序后的列表
    """
    if len(arr) <= 1:
        return arr.copy()
    
    result = arr.copy()
    n = len(result)
    
    # 构建堆
    for i in range(n // 2 - 1, -1, -1):
        _heapify(result, n, i, key, reverse)
    
    # 逐个提取元素
    for i in range(n - 1, 0, -1):
        result[0], result[i] = result[i], result[0]
        _heapify(result, i, 0, key, reverse)
    
    return result


def _heapify(
    arr: List[T],
    n: int,
    i: int,
    key: Optional[Callable[[T], Any]],
    reverse: bool
) -> None:
    """堆化函数"""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    # 根据排序方向调整比较逻辑
    if left < n:
        left_val = key(arr[left]) if key else arr[left]
        largest_val = key(arr[largest]) if key else arr[largest]
        if (left_val > largest_val if not reverse else left_val < largest_val):
            largest = left
    
    if right < n:
        right_val = key(arr[right]) if key else arr[right]
        largest_val = key(arr[largest]) if key else arr[largest]
        if (right_val > largest_val if not reverse else right_val < largest_val):
            largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest, key, reverse)


def insertion_sort(
    arr: List[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
    in_place: bool = False
) -> List[T]:
    """
    插入排序 - O(n²) 稳定排序，小数据集高效
    
    Args:
        arr: 待排序列表
        key: 用于提取比较键的函数
        reverse: 是否降序排列
        in_place: 是否原地排序
    
    Returns:
        排序后的列表
    """
    if not arr:
        return arr if not in_place else arr
    
    result = arr if in_place else arr.copy()
    
    for i in range(1, len(result)):
        key_item = result[i]
        key_val = key(key_item) if key else key_item
        j = i - 1
        
        while j >= 0:
            current_val = key(result[j]) if key else result[j]
            if (current_val > key_val if not reverse else current_val < key_val):
                result[j + 1] = result[j]
                j -= 1
            else:
                break
        
        result[j + 1] = key_item
    
    return result


def selection_sort(
    arr: List[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False
) -> List[T]:
    """
    选择排序 - O(n²)
    
    Args:
        arr: 待排序列表
        key: 用于提取比较键的函数
        reverse: 是否降序排列
    
    Returns:
        排序后的列表
    """
    if len(arr) <= 1:
        return arr.copy()
    
    result = arr.copy()
    n = len(result)
    
    for i in range(n):
        # 找到最小/最大元素的索引
        target_idx = i
        target_val = key(result[target_idx]) if key else result[target_idx]
        
        for j in range(i + 1, n):
            current_val = key(result[j]) if key else result[j]
            if (current_val < target_val if not reverse else current_val > target_val):
                target_idx = j
                target_val = current_val
        
        result[i], result[target_idx] = result[target_idx], result[i]
    
    return result


def bubble_sort(
    arr: List[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
    optimized: bool = True
) -> List[T]:
    """
    冒泡排序 - O(n²) 稳定排序
    
    Args:
        arr: 待排序列表
        key: 用于提取比较键的函数
        reverse: 是否降序排列
        optimized: 是否使用优化版本（提前终止）
    
    Returns:
        排序后的列表
    """
    if len(arr) <= 1:
        return arr.copy()
    
    result = arr.copy()
    n = len(result)
    
    for i in range(n):
        swapped = False
        
        for j in range(0, n - i - 1):
            left_val = key(result[j]) if key else result[j]
            right_val = key(result[j + 1]) if key else result[j + 1]
            
            if (left_val > right_val if not reverse else left_val < right_val):
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        
        # 优化：如果没有发生交换，说明已经有序
        if optimized and not swapped:
            break
    
    return result


def shell_sort(
    arr: List[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
    gaps: Optional[List[int]] = None
) -> List[T]:
    """
    希尔排序 - O(n log n) 到 O(n²) 取决于间隔序列
    
    Args:
        arr: 待排序列表
        key: 用于提取比较键的函数
        reverse: 是否降序排列
        gaps: 自定义间隔序列
    
    Returns:
        排序后的列表
    """
    if len(arr) <= 1:
        return arr.copy()
    
    result = arr.copy()
    n = len(result)
    
    # 默认使用 Knuth 间隔序列
    if gaps is None:
        gaps = []
        gap = 1
        while gap < n:
            gaps.append(gap)
            gap = 3 * gap + 1
        gaps = gaps[::-1]
    
    for gap in gaps:
        for i in range(gap, n):
            temp = result[i]
            temp_val = key(temp) if key else temp
            j = i
            
            while j >= gap:
                current_val = key(result[j - gap]) if key else result[j - gap]
                if (current_val > temp_val if not reverse else current_val < temp_val):
                    result[j] = result[j - gap]
                    j -= gap
                else:
                    break
            
            result[j] = temp
    
    return result


def counting_sort(
    arr: List[int],
    reverse: bool = False,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None
) -> List[int]:
    """
    计数排序 - O(n + k) 仅适用于整数，k 为值域范围
    
    Args:
        arr: 待排序整数列表
        reverse: 是否降序排列
        min_val: 最小值（可选，自动检测）
        max_val: 最大值（可选，自动检测）
    
    Returns:
        排序后的列表
    """
    if len(arr) <= 1:
        return arr.copy()
    
    if min_val is None:
        min_val = min(arr)
    if max_val is None:
        max_val = max(arr)
    
    # 检查是否为整数
    for x in arr:
        if not isinstance(x, int):
            raise TypeError("计数排序仅适用于整数列表")
    
    range_size = max_val - min_val + 1
    count = [0] * range_size
    
    # 计数
    for x in arr:
        count[x - min_val] += 1
    
    # 生成排序结果
    result = []
    if reverse:
        for i in range(range_size - 1, -1, -1):
            result.extend([i + min_val] * count[i])
    else:
        for i in range(range_size):
            result.extend([i + min_val] * count[i])
    
    return result


def bucket_sort(
    arr: List[float],
    num_buckets: int = 10,
    reverse: bool = False,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None
) -> List[float]:
    """
    桶排序 - O(n + k) 适用于浮点数
    
    Args:
        arr: 待排序浮点数列表
        num_buckets: 桶的数量
        reverse: 是否降序排列
        min_val: 最小值（可选，自动检测）
        max_val: 最大值（可选，自动检测）
    
    Returns:
        排序后的列表
    """
    if len(arr) <= 1:
        return arr.copy()
    
    if min_val is None:
        min_val = min(arr)
    if max_val is None:
        max_val = max(arr)
    
    # 创建桶
    buckets = [[] for _ in range(num_buckets)]
    
    # 分配元素到桶
    for x in arr:
        if max_val == min_val:
            bucket_idx = 0
        else:
            bucket_idx = int((x - min_val) / (max_val - min_val) * (num_buckets - 1))
        buckets[bucket_idx].append(x)
    
    # 对每个桶进行排序
    result = []
    bucket_range = range(num_buckets) if not reverse else range(num_buckets - 1, -1, -1)
    
    for i in bucket_range:
        # 使用插入排序对小桶排序
        sorted_bucket = insertion_sort(buckets[i], reverse=reverse)
        result.extend(sorted_bucket)
    
    return result


def radix_sort(
    arr: List[int],
    reverse: bool = False,
    base: int = 10
) -> List[int]:
    """
    基数排序 - O(d * n) d 为位数
    
    Args:
        arr: 待排序整数列表
        reverse: 是否降序排列
        base: 进制基数
    
    Returns:
        排序后的列表
    """
    if len(arr) <= 1:
        return arr.copy()
    
    # 检查是否为整数
    for x in arr:
        if not isinstance(x, int):
            raise TypeError("基数排序仅适用于整数列表")
    
    # 处理负数：分离正负
    negatives = [x for x in arr if x < 0]
    positives = [x for x in arr if x >= 0]
    
    # 对负数取绝对值排序后再反转
    if negatives:
        abs_negatives = [-x for x in negatives]
        sorted_abs_negatives = _radix_sort_positive(abs_negatives, base)
        sorted_negatives = [-x for x in reversed(sorted_abs_negatives)]
    else:
        sorted_negatives = []
    
    # 对正数排序
    sorted_positives = _radix_sort_positive(positives, base) if positives else []
    
    # 合并结果
    if reverse:
        return sorted_positives[::-1] + sorted_negatives[::-1]
    else:
        return sorted_negatives + sorted_positives


def _radix_sort_positive(arr: List[int], base: int) -> List[int]:
    """对正整数进行基数排序"""
    if len(arr) <= 1:
        return arr.copy()
    
    max_val = max(arr)
    result = arr.copy()
    
    exp = 1
    while max_val // exp > 0:
        result = _counting_sort_by_digit(result, exp, base)
        exp *= base
    
    return result


def _counting_sort_by_digit(arr: List[int], exp: int, base: int) -> List[int]:
    """按指定位数进行计数排序"""
    n = len(arr)
    output = [0] * n
    count = [0] * base
    
    # 统计每个数字的出现次数
    for x in arr:
        digit = (x // exp) % base
        count[digit] += 1
    
    # 计算累计位置
    for i in range(1, base):
        count[i] += count[i - 1]
    
    # 构建输出数组（从后向前以保证稳定性）
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % base
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    return output


def tim_sort_like(
    arr: List[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False
) -> List[T]:
    """
    类 TimSort 实现 - 结合插入排序和归并排序
    Python 内置 sorted() 使用 TimSort
    
    Args:
        arr: 待排序列表
        key: 用于提取比较键的函数
        reverse: 是否降序排列
    
    Returns:
        排序后的列表
    """
    if len(arr) <= 1:
        return arr.copy()
    
    # 小数组直接用插入排序
    if len(arr) <= 32:
        return insertion_sort(arr, key, reverse)
    
    # 大数组用归并排序
    return merge_sort(arr, key, reverse)


def cocktail_sort(
    arr: List[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False
) -> List[T]:
    """
    鸡尾酒排序（双向冒泡排序） - O(n²)
    
    Args:
        arr: 待排序列表
        key: 用于提取比较键的函数
        reverse: 是否降序排列
    
    Returns:
        排序后的列表
    """
    if len(arr) <= 1:
        return arr.copy()
    
    result = arr.copy()
    n = len(result)
    left = 0
    right = n - 1
    swapped = True
    
    while swapped:
        swapped = False
        
        # 从左向右
        for i in range(left, right):
            left_val = key(result[i]) if key else result[i]
            right_val = key(result[i + 1]) if key else result[i + 1]
            
            if (left_val > right_val if not reverse else left_val < right_val):
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True
        
        if not swapped:
            break
        
        right -= 1
        swapped = False
        
        # 从右向左
        for i in range(right, left, -1):
            left_val = key(result[i - 1]) if key else result[i - 1]
            right_val = key(result[i]) if key else result[i]
            
            if (left_val > right_val if not reverse else left_val < right_val):
                result[i - 1], result[i] = result[i], result[i - 1]
                swapped = True
        
        left += 1
    
    return result


def gnome_sort(
    arr: List[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False
) -> List[T]:
    """
    侏儒排序 - O(n²) 简单但有趣的排序
    
    Args:
        arr: 待排序列表
        key: 用于提取比较键的函数
        reverse: 是否降序排列
    
    Returns:
        排序后的列表
    """
    if len(arr) <= 1:
        return arr.copy()
    
    result = arr.copy()
    i = 0
    
    while i < len(result):
        if i == 0:
            i += 1
        
        prev_val = key(result[i - 1]) if key else result[i - 1]
        curr_val = key(result[i]) if key else result[i]
        
        if (prev_val <= curr_val if not reverse else prev_val >= curr_val):
            i += 1
        else:
            result[i], result[i - 1] = result[i - 1], result[i]
            i -= 1
    
    return result


def sort_by_custom(
    arr: List[T],
    comparator: Callable[[T, T], int]
) -> List[T]:
    """
    使用自定义比较函数排序
    
    Args:
        arr: 待排序列表
        comparator: 比较函数，返回负数/零/正数
    
    Returns:
        排序后的列表
    """
    return sorted(arr.copy(), key=cmp_to_key(comparator))


def is_sorted(
    arr: List[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False
) -> bool:
    """
    检查列表是否已排序
    
    Args:
        arr: 待检查列表
        key: 用于提取比较键的函数
        reverse: 是否检查降序
    
    Returns:
        是否已排序
    """
    if len(arr) <= 1:
        return True
    
    for i in range(len(arr) - 1):
        left_val = key(arr[i]) if key else arr[i]
        right_val = key(arr[i + 1]) if key else arr[i + 1]
        
        if (left_val > right_val if not reverse else left_val < right_val):
            return False
    
    return True


def get_sort_algorithm_complexity() -> dict:
    """
    获取各排序算法的时间复杂度信息
    
    Returns:
        包含各算法复杂度的字典
    """
    return {
        'quick_sort': {'best': 'O(n log n)', 'average': 'O(n log n)', 'worst': 'O(n²)', 'stable': False},
        'merge_sort': {'best': 'O(n log n)', 'average': 'O(n log n)', 'worst': 'O(n log n)', 'stable': True},
        'heap_sort': {'best': 'O(n log n)', 'average': 'O(n log n)', 'worst': 'O(n log n)', 'stable': False},
        'insertion_sort': {'best': 'O(n)', 'average': 'O(n²)', 'worst': 'O(n²)', 'stable': True},
        'selection_sort': {'best': 'O(n²)', 'average': 'O(n²)', 'worst': 'O(n²)', 'stable': False},
        'bubble_sort': {'best': 'O(n)', 'average': 'O(n²)', 'worst': 'O(n²)', 'stable': True},
        'shell_sort': {'best': 'O(n log n)', 'average': 'O(n^1.5)', 'worst': 'O(n²)', 'stable': False},
        'counting_sort': {'best': 'O(n + k)', 'average': 'O(n + k)', 'worst': 'O(n + k)', 'stable': True},
        'bucket_sort': {'best': 'O(n + k)', 'average': 'O(n + k)', 'worst': 'O(n²)', 'stable': True},
        'radix_sort': {'best': 'O(d * n)', 'average': 'O(d * n)', 'worst': 'O(d * n)', 'stable': True},
        'cocktail_sort': {'best': 'O(n)', 'average': 'O(n²)', 'worst': 'O(n²)', 'stable': True},
        'gnome_sort': {'best': 'O(n)', 'average': 'O(n²)', 'worst': 'O(n²)', 'stable': True},
    }


def recommend_sort_algorithm(
    n: int,
    is_integers: bool = False,
    value_range: Optional[int] = None,
    require_stable: bool = False
) -> str:
    """
    根据输入特性推荐最合适的排序算法
    
    Args:
        n: 数据量
        is_integers: 是否为整数
        value_range: 值域范围（仅对整数有意义）
        require_stable: 是否需要稳定排序
    
    Returns:
        推荐的算法名称
    """
    # 小数据集
    if n <= 32:
        if require_stable:
            return 'insertion_sort'
        else:
            return 'insertion_sort'  # 插入排序对小数据集最优
    
    # 整数且值域有限
    if is_integers and value_range is not None:
        if value_range <= n * 2:  # 值域不大，计数排序最优
            return 'counting_sort'
        elif value_range <= 1000:  # 值域适中
            return 'radix_sort'
    
    # 大数据集
    if require_stable:
        return 'merge_sort'
    else:
        return 'quick_sort'  # 快速排序通常最快


# 导出所有公开函数
__all__ = [
    'quick_sort',
    'merge_sort',
    'heap_sort',
    'insertion_sort',
    'selection_sort',
    'bubble_sort',
    'shell_sort',
    'counting_sort',
    'bucket_sort',
    'radix_sort',
    'tim_sort_like',
    'cocktail_sort',
    'gnome_sort',
    'sort_by_custom',
    'is_sorted',
    'get_sort_algorithm_complexity',
    'recommend_sort_algorithm',
]