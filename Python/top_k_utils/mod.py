"""
Top-K 工具集 (Top-K Utilities)
==============================

提供全面的 Top-K 问题解决方案，包括：
- 堆排序法 Top-K（O(n log k)）
- QuickSelect 算法（O(n) 平均）
- 流式 Top-K（在线算法）
- 频繁元素 Top-K（Heavy Hitters）
- 分布式 Top-K 合并

零外部依赖，纯 Python 实现。

作者: AllToolkit
日期: 2026-04-30
版本: 1.0.0
"""

from typing import List, Optional, TypeVar, Generic, Callable, Any, Tuple, Dict, Iterator
from collections import defaultdict
import random

T = TypeVar('T')


# ==================== 基础 Top-K 算法 ====================

def top_k_heap(data: List[T], k: int, 
               key: Optional[Callable[[T], float]] = None,
               largest: bool = True) -> List[T]:
    """
    使用堆方法找出 Top-K 元素
    
    时间复杂度: O(n log k)
    空间复杂度: O(k)
    
    适用于 k << n 的场景，性能优异。
    
    Args:
        data: 数据列表
        k: 要找的元素个数
        key: 比较键函数
        largest: True 找最大的 k 个，False 找最小的 k 个
        
    Returns:
        Top-K 元素列表（已排序）
        
    示例:
        >>> top_k_heap([3, 1, 4, 1, 5, 9, 2, 6], 3)
        [9, 6, 5]
        >>> top_k_heap([3, 1, 4, 1, 5, 9, 2, 6], 3, largest=False)
        [1, 1, 2]
    """
    if k <= 0:
        return []
    if k >= len(data):
        return sorted(data, key=key, reverse=largest)[:k]
    
    def get_key(item):
        if key is not None:
            return key(item)
        return item
    
    # 使用 Python 内置堆（最小堆）
    import heapq
    
    if largest:
        # 找最大的 k 个：维护一个最小堆，堆顶是当前 k 个中最小的
        heap = []
        for item in data:
            key_val = get_key(item)
            if len(heap) < k:
                heapq.heappush(heap, (key_val, item))
            elif key_val > heap[0][0]:
                heapq.heapreplace(heap, (key_val, item))
        # 按从大到小排序
        result = [heapq.heappop(heap)[1] for _ in range(len(heap))]
        result.reverse()
        return result
    else:
        # 找最小的 k 个：维护一个最大堆（取负）
        heap = []
        for item in data:
            key_val = get_key(item)
            if len(heap) < k:
                heapq.heappush(heap, (-key_val, item))
            elif key_val < -heap[0][0]:
                heapq.heapreplace(heap, (-key_val, item))
        # 按从小到大排序（弹出的是从大到小，需要反转）
        result = []
        while heap:
            result.append(heapq.heappop(heap)[1])
        result.reverse()  # 反转后变成从小到大
        return result


def top_k_quickselect(data: List[T], k: int,
                      key: Optional[Callable[[T], float]] = None,
                      largest: bool = True) -> List[T]:
    """
    使用 QuickSelect 算法找出 Top-K 元素
    
    平均时间复杂度: O(n)
    最坏时间复杂度: O(n²)
    空间复杂度: O(n)（原地修改）
    
    适用于 k 较大的场景，平均性能优于堆方法。
    
    Args:
        data: 数据列表（会被修改）
        k: 要找的元素个数
        key: 比较键函数
        largest: True 找最大的 k 个，False 找最小的 k 个
        
    Returns:
        Top-K 元素列表（未保证排序）
        
    示例:
        >>> top_k_quickselect([3, 1, 4, 1, 5, 9, 2, 6], 3)
        [9, 6, 5]  # 或其他顺序，包含最大的3个
    """
    if k <= 0:
        return []
    if k >= len(data):
        return list(data)
    
    arr = list(data)  # 复制避免修改原数组
    
    def get_key(item):
        if key is not None:
            return key(item)
        return item
    
    def partition(left: int, right: int, pivot_idx: int) -> int:
        """分区函数，返回枢轴最终位置"""
        pivot_val = get_key(arr[pivot_idx])
        # 将枢轴移到末尾
        arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
        store_idx = left
        
        for i in range(left, right):
            if largest:
                # 找最大的 k 个，大的放左边
                if get_key(arr[i]) > pivot_val:
                    arr[store_idx], arr[i] = arr[i], arr[store_idx]
                    store_idx += 1
            else:
                # 找最小的 k 个，小的放左边
                if get_key(arr[i]) < pivot_val:
                    arr[store_idx], arr[i] = arr[i], arr[store_idx]
                    store_idx += 1
        
        arr[store_idx], arr[right] = arr[right], arr[store_idx]
        return store_idx
    
    def select(left: int, right: int, k_val: int):
        """选择第 k 大/小的元素"""
        if left == right:
            return
        
        # 随机选择枢轴
        pivot_idx = random.randint(left, right)
        pivot_idx = partition(left, right, pivot_idx)
        
        if k_val == pivot_idx:
            return
        elif k_val < pivot_idx:
            select(left, pivot_idx - 1, k_val)
        else:
            select(pivot_idx + 1, right, k_val)
    
    # 找第 k 大的元素位置（0-indexed，所以是 k-1）
    select(0, len(arr) - 1, k - 1)
    return arr[:k]


def top_k_sort(data: List[T], k: int,
               key: Optional[Callable[[T], float]] = None,
               largest: bool = True) -> List[T]:
    """
    使用排序找出 Top-K 元素
    
    时间复杂度: O(n log n)
    空间复杂度: O(n)
    
    最简单直接的方法，适用于小数据集。
    
    Args:
        data: 数据列表
        k: 要找的元素个数
        key: 比较键函数
        largest: True 找最大的 k 个，False 找最小的 k 个
        
    Returns:
        Top-K 元素列表（已排序）
        
    示例:
        >>> top_k_sort([3, 1, 4, 1, 5, 9, 2, 6], 3)
        [9, 6, 5]
    """
    if k <= 0:
        return []
    return sorted(data, key=key, reverse=largest)[:k]


# ==================== 流式 Top-K ====================

class StreamingTopK(Generic[T]):
    """
    流式 Top-K 处理器
    
    支持在线处理数据流，实时维护 Top-K 结果。
    使用最小堆实现，内存占用仅 O(k)。
    
    示例:
        >>> stream = StreamingTopK(3)
        >>> for x in [3, 1, 4, 1, 5, 9, 2, 6]:
        ...     stream.add(x)
        >>> stream.get_top_k()
        [9, 6, 5]
    """
    
    def __init__(self, k: int, key: Optional[Callable[[T], float]] = None,
                 largest: bool = True):
        """
        初始化流式 Top-K 处理器
        
        Args:
            k: 要维护的 Top-K 大小
            key: 比较键函数
            largest: True 维护最大的 k 个，False 维护最小的 k 个
        """
        if k <= 0:
            raise ValueError("k must be positive")
        
        self._k = k
        self._key = key
        self._largest = largest
        self._heap: List[Tuple[float, int, T]] = []
        self._counter = 0
    
    def _get_key(self, item: T) -> float:
        """获取比较键"""
        if self._key is not None:
            return self._key(item)
        if isinstance(item, (int, float)):
            return float(item)
        return hash(item)
    
    def add(self, item: T) -> bool:
        """
        添加元素
        
        Args:
            item: 要添加的元素
            
        Returns:
            是否成功添加到 Top-K 中
        """
        import heapq
        key_val = self._get_key(item)
        
        if self._largest:
            # 维护最大的 k 个：用最小堆
            heap_key = key_val
            if len(self._heap) < self._k:
                heapq.heappush(self._heap, (heap_key, self._counter, item))
                self._counter += 1
                return True
            elif key_val > self._heap[0][0]:
                heapq.heapreplace(self._heap, (heap_key, self._counter, item))
                self._counter += 1
                return True
            return False
        else:
            # 维护最小的 k 个：用最大堆（取负）
            heap_key = -key_val
            if len(self._heap) < self._k:
                heapq.heappush(self._heap, (heap_key, self._counter, item))
                self._counter += 1
                return True
            elif key_val < -self._heap[0][0]:
                heapq.heapreplace(self._heap, (heap_key, self._counter, item))
                self._counter += 1
                return True
            return False
    
    def add_all(self, items: Iterator[T]) -> int:
        """
        批量添加元素
        
        Args:
            items: 元素迭代器
            
        Returns:
            成功添加到 Top-K 的元素数量
        """
        count = 0
        for item in items:
            if self.add(item):
                count += 1
        return count
    
    def get_top_k(self, sorted_: bool = True) -> List[T]:
        """
        获取当前 Top-K 结果
        
        Args:
            sorted_: 是否按从大到小（largest=True）或从小到大（largest=False）排序
            
        Returns:
            Top-K 元素列表
        """
        import heapq
        result = [(k, i, v) for k, i, v in self._heap]
        
        if sorted_:
            if self._largest:
                # 找最大的 k 个，从大到小排序
                result.sort(reverse=True)
            else:
                # 找最小的 k 个，从小到大排序
                # 堆中存储的是 (-key_val, counter, item)
                # 所以需要按 -k（实际 key_val）升序排序
                result.sort(key=lambda x: -x[0])
        
        return [v for k, i, v in result]
    
    def __len__(self) -> int:
        """当前堆中的元素数量"""
        return len(self._heap)
    
    def __repr__(self) -> str:
        direction = "largest" if self._largest else "smallest"
        return f"StreamingTopK(k={self._k}, direction={direction}, items={len(self._heap)})"


# ==================== 频繁元素 Top-K（Heavy Hitters）====================

class FrequentItems(Generic[T]):
    """
    频繁元素计数器（Heavy Hitters）
    
    使用 Space-Saving 算法高效找出频繁出现的元素。
    内存占用 O(k)，支持流式数据。
    
    示例:
        >>> freq = FrequentItems(3)
        >>> for x in [1, 1, 1, 2, 2, 3, 4, 5]:
        ...     freq.add(x)
        >>> freq.get_top_k()
        [(1, 3), (2, 2), (3, 1)]
    """
    
    def __init__(self, k: int):
        """
        初始化频繁元素计数器
        
        Args:
            k: 要跟踪的元素数量
        """
        if k <= 0:
            raise ValueError("k must be positive")
        
        self._k = k
        self._counters: Dict[T, int] = {}
        self._total = 0
    
    def add(self, item: T, count: int = 1) -> int:
        """
        添加元素
        
        Args:
            item: 要添加的元素
            count: 计数增量（默认为1）
            
        Returns:
            该元素的当前估计频率
        """
        self._total += count
        
        if item in self._counters:
            self._counters[item] += count
        elif len(self._counters) < self._k:
            self._counters[item] = count
        else:
            # 找到最小计数的元素并替换
            min_item = min(self._counters, key=self._counters.get)
            min_count = self._counters[min_item]
            del self._counters[min_item]
            self._counters[item] = min_count + count
        
        return self._counters.get(item, 0)
    
    def add_all(self, items: Iterator[T]) -> None:
        """
        批量添加元素
        
        Args:
            items: 元素迭代器
        """
        for item in items:
            self.add(item)
    
    def get_top_k(self, sorted_: bool = True) -> List[Tuple[T, int]]:
        """
        获取 Top-K 频繁元素
        
        Args:
            sorted_: 是否按频率排序
            
        Returns:
            (元素, 估计频率) 元组列表
        """
        items = list(self._counters.items())
        if sorted_:
            items.sort(key=lambda x: -x[1])
        return items[:self._k]
    
    def get_frequency(self, item: T) -> int:
        """
        获取某元素的估计频率
        
        Args:
            item: 要查询的元素
            
        Returns:
            估计频率（如果不在跟踪列表中则返回0）
        """
        return self._counters.get(item, 0)
    
    def get_total(self) -> int:
        """获取总计数"""
        return self._total
    
    def __len__(self) -> int:
        """当前跟踪的元素数量"""
        return len(self._counters)
    
    def __repr__(self) -> str:
        return f"FrequentItems(k={self._k}, tracked={len(self._counters)}, total={self._total})"


class TopKFrequent(Generic[T]):
    """
    Top-K 频繁元素追踪器（精确版本）
    
    使用完整计数器精确统计所有元素频率。
    内存占用 O(n)，适用于元素种类不多的场景。
    
    示例:
        >>> freq = TopKFrequent()
        >>> freq.add_all([1, 1, 1, 2, 2, 3, 4, 5])
        >>> freq.get_top_k(3)
        [(1, 3), (2, 2), (3, 1)]
    """
    
    def __init__(self):
        """初始化精确频繁元素计数器"""
        self._counters: Dict[T, int] = defaultdict(int)
        self._total = 0
    
    def add(self, item: T, count: int = 1) -> int:
        """
        添加元素
        
        Args:
            item: 要添加的元素
            count: 计数增量
            
        Returns:
            该元素的当前频率
        """
        self._counters[item] += count
        self._total += count
        return self._counters[item]
    
    def add_all(self, items: Iterator[T]) -> None:
        """批量添加元素"""
        for item in items:
            self.add(item)
    
    def get_top_k(self, k: int, sorted_: bool = True) -> List[Tuple[T, int]]:
        """
        获取 Top-K 频繁元素
        
        Args:
            k: 要获取的元素数量
            sorted_: 是否按频率排序
            
        Returns:
            (元素, 频率) 元组列表
        """
        items = list(self._counters.items())
        if sorted_:
            items.sort(key=lambda x: -x[1])
        return items[:k]
    
    def get_frequency(self, item: T) -> int:
        """获取某元素的频率"""
        return self._counters.get(item, 0)
    
    def get_all(self) -> Dict[T, int]:
        """获取所有元素及其频率"""
        return dict(self._counters)
    
    def get_total(self) -> int:
        """获取总计数"""
        return self._total
    
    def get_unique_count(self) -> int:
        """获取唯一元素数量"""
        return len(self._counters)
    
    def __len__(self) -> int:
        """唯一元素数量"""
        return len(self._counters)
    
    def __repr__(self) -> str:
        return f"TopKFrequent(unique={len(self._counters)}, total={self._total})"


# ==================== 分布式 Top-K 合并 ====================

def merge_top_k(top_k_lists: List[List[T]], k: int,
                key: Optional[Callable[[T], float]] = None,
                largest: bool = True) -> List[T]:
    """
    合并多个 Top-K 列表
    
    适用于分布式场景，将多个分片的 Top-K 结果合并为全局 Top-K。
    
    Args:
        top_k_lists: 多个 Top-K 列表
        k: 最终要保留的元素数量
        key: 比较键函数
        largest: True 找最大的，False 找最小的
        
    Returns:
        合并后的 Top-K 列表
        
    示例:
        >>> lists = [[9, 8, 7], [10, 5, 3], [6, 4, 2]]
        >>> merge_top_k(lists, 3)
        [10, 9, 8]
    """
    all_items = []
    for lst in top_k_lists:
        all_items.extend(lst)
    
    return top_k_heap(all_items, k, key=key, largest=largest)


def merge_top_k_weighted(top_k_lists: List[Tuple[List[T], float]], k: int,
                         key: Optional[Callable[[T], float]] = None,
                         largest: bool = True) -> List[T]:
    """
    合并多个带权重的 Top-K 列表
    
    Args:
        top_k_lists: 多个 (Top-K 列表, 权重) 元组
        k: 最终要保留的元素数量
        key: 比较键函数
        largest: True 找最大的，False 找最小的
        
    Returns:
        合并后的 Top-K 列表
    """
    weighted_items = []
    for lst, weight in top_k_lists:
        for item in lst:
            item_key = key(item) if key else item
            weighted_key = item_key * weight
            weighted_items.append((weighted_key, item))
    
    result = sorted(weighted_items, key=lambda x: x[0], reverse=largest)[:k]
    return [item for _, item in result]


# ==================== 特殊用途 Top-K ====================

def top_k_unique(data: List[T], k: int,
                 key: Optional[Callable[[T], float]] = None,
                 largest: bool = True) -> List[T]:
    """
    找出 Top-K 唯一元素
    
    忽略重复元素，返回值唯一的前 k 个元素。
    
    Args:
        data: 数据列表
        k: 要找的元素个数
        key: 比较键函数
        largest: True 找最大的，False 找最小的
        
    Returns:
        Top-K 唯一元素列表
        
    示例:
        >>> top_k_unique([3, 1, 4, 1, 5, 9, 2, 6, 5], 3)
        [9, 6, 5]
    """
    seen = set()
    unique_data = []
    for item in data:
        key_val = key(item) if key else item
        if key_val not in seen:
            seen.add(key_val)
            unique_data.append(item)
    
    return top_k_heap(unique_data, k, key=key, largest=largest)


def top_k_with_threshold(data: List[T], threshold: float,
                        key: Optional[Callable[[T], float]] = None,
                        largest: bool = True) -> List[T]:
    """
    找出超过阈值的所有元素
    
    Args:
        data: 数据列表
        threshold: 阈值
        key: 比较键函数
        largest: True 找大于阈值的，False 找小于阈值的
        
    Returns:
        符合条件的元素列表（已排序）
        
    示例:
        >>> top_k_with_threshold([3, 1, 4, 1, 5, 9, 2, 6], 4)
        [9, 6, 5]
    """
    filtered = []
    for item in data:
        key_val = key(item) if key else item
        if largest:
            if key_val > threshold:
                filtered.append(item)
        else:
            if key_val < threshold:
                filtered.append(item)
    
    return sorted(filtered, key=key, reverse=largest)


def top_k_percentile(data: List[T], percentile: float,
                    key: Optional[Callable[[T], float]] = None,
                    largest: bool = True) -> List[T]:
    """
    找出位于指定百分位之上的元素
    
    Args:
        data: 数据列表
        percentile: 百分位 (0-100)
        key: 比较键函数
        largest: True 找高于百分位的，False 找低于百分位的
        
    Returns:
        符合条件的元素列表
        
    示例:
        >>> top_k_percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 80)
        [9, 10]
    """
    if not data:
        return []
    
    sorted_data = sorted(data, key=key)
    n = len(sorted_data)
    idx = int(n * percentile / 100)
    
    if largest:
        return sorted_data[idx:]
    else:
        return sorted_data[:idx]


# ==================== 工具函数 ====================

def nth_element(data: List[T], n: int,
                key: Optional[Callable[[T], float]] = None,
                largest: bool = True) -> T:
    """
    找出第 n 大/小的元素
    
    使用 QuickSelect 算法，平均 O(n) 时间复杂度。
    
    Args:
        data: 数据列表
        n: 第 n 大/小（从1开始）
        key: 比较键函数
        largest: True 找第 n 大，False 找第 n 小
        
    Returns:
        第 n 大/小的元素
        
    Raises:
        ValueError: n 超出范围
        
    示例:
        >>> nth_element([3, 1, 4, 1, 5, 9, 2, 6], 3)
        5  # 第3大
    """
    if not 1 <= n <= len(data):
        raise ValueError(f"n must be between 1 and {len(data)}")
    
    arr = list(data)
    
    def get_key(item):
        return key(item) if key else item
    
    def partition(left: int, right: int, pivot_idx: int) -> int:
        pivot_val = get_key(arr[pivot_idx])
        arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
        store_idx = left
        
        for i in range(left, right):
            if largest:
                if get_key(arr[i]) > pivot_val:
                    arr[store_idx], arr[i] = arr[i], arr[store_idx]
                    store_idx += 1
            else:
                if get_key(arr[i]) < pivot_val:
                    arr[store_idx], arr[i] = arr[i], arr[store_idx]
                    store_idx += 1
        
        arr[store_idx], arr[right] = arr[right], arr[store_idx]
        return store_idx
    
    def select(left: int, right: int, k_val: int):
        if left == right:
            return
        pivot_idx = random.randint(left, right)
        pivot_idx = partition(left, right, pivot_idx)
        
        if k_val == pivot_idx:
            return
        elif k_val < pivot_idx:
            select(left, pivot_idx - 1, k_val)
        else:
            select(pivot_idx + 1, right, k_val)
    
    select(0, len(arr) - 1, n - 1)
    return arr[n - 1]


def median(data: List[T], key: Optional[Callable[[T], float]] = None) -> float:
    """
    计算中位数
    
    Args:
        data: 数据列表
        key: 比较键函数
        
    Returns:
        中位数（偶数个元素时返回中间两个的平均值）
        
    示例:
        >>> median([1, 2, 3, 4, 5])
        3.0
        >>> median([1, 2, 3, 4])
        2.5
    """
    if not data:
        raise ValueError("Cannot find median of empty data")
    
    sorted_data = sorted(data, key=key)
    n = len(sorted_data)
    
    if n % 2 == 1:
        mid = sorted_data[n // 2]
        if key:
            return key(mid)
        return float(mid)
    else:
        mid1, mid2 = sorted_data[n // 2 - 1], sorted_data[n // 2]
        if key:
            return (key(mid1) + key(mid2)) / 2
        return (mid1 + mid2) / 2.0


# ==================== 导出 ====================

__all__ = [
    # 基础算法
    'top_k_heap',
    'top_k_quickselect',
    'top_k_sort',
    
    # 流式处理
    'StreamingTopK',
    
    # 频繁元素
    'FrequentItems',
    'TopKFrequent',
    
    # 分布式合并
    'merge_top_k',
    'merge_top_k_weighted',
    
    # 特殊用途
    'top_k_unique',
    'top_k_with_threshold',
    'top_k_percentile',
    
    # 工具函数
    'nth_element',
    'median',
]