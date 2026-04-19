"""
滑动窗口统计工具模块 (Sliding Window Statistics Utils)

提供高效的滑动窗口数据结构和统计计算功能，适用于实时数据流分析、
监控指标计算、性能测量等场景。零外部依赖，纯 Python 标准库实现。

主要功能：
- 滑动窗口最大值/最小值（单调队列实现，O(1) 查询）
- 滑动窗口平均值/总和/计数
- 滑动窗口标准差/方差
- 滑动窗口中位数（双堆实现）
- 滑动窗口百分位数
- 时间窗口统计（基于时间戳的数据）
"""

from collections import deque
from typing import Optional, List, Tuple, Callable, Any, Generic, TypeVar
import math
import heapq
import time

T = TypeVar('T', int, float)


class SlidingWindowMax(Generic[T]):
    """
    滑动窗口最大值计算器
    
    使用单调递减队列实现，支持 O(1) 的最大值查询，
    O(n) 的整体时间复杂度处理 n 个元素。
    
    示例:
        >>> swm = SlidingWindowMax(3)
        >>> for val in [1, 3, 2, 5, 4]:
        ...     swm.push(val)
        ...     print(swm.max())
        1
        3
        3
        5
        5
    """
    
    def __init__(self, window_size: int):
        """
        初始化滑动窗口最大值计算器
        
        Args:
            window_size: 窗口大小，必须为正整数
        """
        if window_size <= 0:
            raise ValueError("窗口大小必须为正整数")
        self.window_size = window_size
        self._deque: deque = deque()  # 存储 (索引, 值) 的单调队列
        self._data: deque = deque()   # 存储所有数据
        self._index = 0
    
    def push(self, value: T) -> Optional[T]:
        """
        添加新值到窗口
        
        Args:
            value: 要添加的数值
            
        Returns:
            被移除的值（如果窗口已满），否则返回 None
        """
        popped = None
        
        # 移除超出窗口的元素
        if len(self._data) >= self.window_size:
            popped = self._data.popleft()
            # 移除队列中过期的元素
            if self._deque and self._deque[0][0] <= self._index - self.window_size:
                self._deque.popleft()
        
        # 维护单调递减队列
        while self._deque and self._deque[-1][1] <= value:
            self._deque.pop()
        
        self._deque.append((self._index, value))
        self._data.append(value)
        self._index += 1
        
        return popped
    
    def max(self) -> Optional[T]:
        """
        获取当前窗口的最大值
        
        Returns:
            窗口内的最大值，如果窗口为空则返回 None
        """
        if not self._deque:
            return None
        return self._deque[0][1]
    
    def __len__(self) -> int:
        return len(self._data)
    
    def is_empty(self) -> bool:
        return len(self._data) == 0
    
    def is_full(self) -> bool:
        return len(self._data) == self.window_size
    
    def clear(self) -> None:
        """清空窗口"""
        self._deque.clear()
        self._data.clear()
        self._index = 0


class SlidingWindowMin(Generic[T]):
    """
    滑动窗口最小值计算器
    
    使用单调递增队列实现，支持 O(1) 的最小值查询。
    
    示例:
        >>> swm = SlidingWindowMin(3)
        >>> for val in [5, 3, 2, 4, 1]:
        ...     swm.push(val)
        ...     print(swm.min())
        5
        3
        2
        2
        1
    """
    
    def __init__(self, window_size: int):
        if window_size <= 0:
            raise ValueError("窗口大小必须为正整数")
        self.window_size = window_size
        self._deque: deque = deque()
        self._data: deque = deque()
        self._index = 0
    
    def push(self, value: T) -> Optional[T]:
        """添加新值到窗口，返回被移除的值（如果有）"""
        popped = None
        
        if len(self._data) >= self.window_size:
            popped = self._data.popleft()
            if self._deque and self._deque[0][0] <= self._index - self.window_size:
                self._deque.popleft()
        
        # 维护单调递增队列
        while self._deque and self._deque[-1][1] >= value:
            self._deque.pop()
        
        self._deque.append((self._index, value))
        self._data.append(value)
        self._index += 1
        
        return popped
    
    def min(self) -> Optional[T]:
        """获取当前窗口的最小值"""
        if not self._deque:
            return None
        return self._deque[0][1]
    
    def __len__(self) -> int:
        return len(self._data)
    
    def is_empty(self) -> bool:
        return len(self._data) == 0
    
    def is_full(self) -> bool:
        return len(self._data) == self.window_size
    
    def clear(self) -> None:
        self._deque.clear()
        self._data.clear()
        self._index = 0


class SlidingWindowStats:
    """
    滑动窗口统计计算器
    
    提供滑动窗口内的平均值、总和、标准差、方差等统计量计算。
    
    示例:
        >>> stats = SlidingWindowStats(3)
        >>> for val in [1, 2, 3, 4, 5]:
        ...     stats.push(val)
        ...     print(f"avg={stats.mean():.2f}, sum={stats.sum()}")
        avg=1.00, sum=1
        avg=1.50, sum=3
        avg=2.00, sum=6
        avg=3.00, sum=9
        avg=4.00, sum=12
    """
    
    def __init__(self, window_size: int):
        """
        初始化滑动窗口统计计算器
        
        Args:
            window_size: 窗口大小
        """
        if window_size <= 0:
            raise ValueError("窗口大小必须为正整数")
        self.window_size = window_size
        self._data: deque = deque()
        self._sum: float = 0.0
        self._sum_sq: float = 0.0  # 用于计算方差
    
    def push(self, value: float) -> Optional[float]:
        """
        添加新值到窗口
        
        Args:
            value: 要添加的数值
            
        Returns:
            被移除的值（如果窗口已满）
        """
        popped = None
        
        if len(self._data) >= self.window_size:
            popped = self._data.popleft()
            self._sum -= popped
            self._sum_sq -= popped * popped
        
        self._data.append(value)
        self._sum += value
        self._sum_sq += value * value
        
        return popped
    
    def sum(self) -> float:
        """获取窗口内数据的总和"""
        return self._sum
    
    def mean(self) -> Optional[float]:
        """获取窗口内数据的平均值"""
        if not self._data:
            return None
        return self._sum / len(self._data)
    
    def variance(self, population: bool = True) -> Optional[float]:
        """
        计算方差
        
        Args:
            population: True 为总体方差，False 为样本方差
            
        Returns:
            方差值，窗口为空返回 None
        """
        if not self._data:
            return None
        
        n = len(self._data)
        mean = self._sum / n
        
        if population:
            return (self._sum_sq / n) - (mean * mean)
        else:
            if n < 2:
                return None
            return ((self._sum_sq / n) - (mean * mean)) * n / (n - 1)
    
    def std_dev(self, population: bool = True) -> Optional[float]:
        """
        计算标准差
        
        Args:
            population: True 为总体标准差，False 为样本标准差
            
        Returns:
            标准差值，窗口为空返回 None
        """
        var = self.variance(population)
        if var is None:
            return None
        return math.sqrt(var)
    
    def count(self) -> int:
        """获取窗口内数据的数量"""
        return len(self._data)
    
    def min(self) -> Optional[float]:
        """获取窗口内最小值"""
        if not self._data:
            return None
        return min(self._data)
    
    def max(self) -> Optional[float]:
        """获取窗口内最大值"""
        if not self._data:
            return None
        return max(self._data)
    
    def range(self) -> Optional[float]:
        """获取窗口内数据的极差（最大值 - 最小值）"""
        if not self._data:
            return None
        return max(self._data) - min(self._data)
    
    def __len__(self) -> int:
        return len(self._data)
    
    def is_empty(self) -> bool:
        return len(self._data) == 0
    
    def is_full(self) -> bool:
        return len(self._data) == self.window_size
    
    def clear(self) -> None:
        """清空窗口"""
        self._data.clear()
        self._sum = 0.0
        self._sum_sq = 0.0


class SlidingWindowMedian:
    """
    滑动窗口中位数计算器
    
    使用双堆（大顶堆 + 小顶堆）实现，支持 O(log n) 的中位数查询。
    
    示例:
        >>> swm = SlidingWindowMedian(3)
        >>> for val in [1, 2, 3, 4, 5]:
        ...     swm.push(val)
        ...     print(f"median={swm.median()}")
        median=1
        median=1.5
        median=2
        median=3
        median=4
    """
    
    def __init__(self, window_size: int):
        if window_size <= 0:
            raise ValueError("窗口大小必须为正整数")
        self.window_size = window_size
        self._data: deque = deque()
        # 大顶堆（存储较小的一半，用负数模拟）
        self._max_heap: List[float] = []
        # 小顶堆（存储较大的一半）
        self._min_heap: List[float] = []
        # 延迟删除的元素计数
        self._delayed: dict = {}
        self._max_heap_size = 0
        self._min_heap_size = 0
    
    def push(self, value: float) -> Optional[float]:
        """添加新值到窗口，返回被移除的值"""
        popped = None
        
        if len(self._data) >= self.window_size:
            popped = self._data.popleft()
            self._delayed[popped] = self._delayed.get(popped, 0) + 1
            if popped <= -self._max_heap[0]:
                self._max_heap_size -= 1
            else:
                self._min_heap_size -= 1
        
        self._data.append(value)
        self._add_num(value)
        self._rebalance()
        self._prune()
        
        return popped
    
    def _add_num(self, num: float) -> None:
        """将数字添加到合适的堆"""
        if not self._max_heap or num <= -self._max_heap[0]:
            heapq.heappush(self._max_heap, -num)
            self._max_heap_size += 1
        else:
            heapq.heappush(self._min_heap, num)
            self._min_heap_size += 1
    
    def _rebalance(self) -> None:
        """平衡两个堆的大小"""
        while self._max_heap_size > self._min_heap_size + 1:
            self._prune_max_heap()
            if self._max_heap:
                val = -heapq.heappop(self._max_heap)
                self._max_heap_size -= 1
                heapq.heappush(self._min_heap, val)
                self._min_heap_size += 1
                self._prune_min_heap()
        
        while self._min_heap_size > self._max_heap_size:
            self._prune_min_heap()
            if self._min_heap:
                val = heapq.heappop(self._min_heap)
                self._min_heap_size -= 1
                heapq.heappush(self._max_heap, -val)
                self._max_heap_size += 1
                self._prune_max_heap()
    
    def _prune(self) -> None:
        """清理延迟删除的元素"""
        while self._max_heap and self._delayed.get(-self._max_heap[0], 0) > 0:
            val = -heapq.heappop(self._max_heap)
            self._delayed[val] -= 1
            if self._delayed[val] == 0:
                del self._delayed[val]
        
        while self._min_heap and self._delayed.get(self._min_heap[0], 0) > 0:
            val = heapq.heappop(self._min_heap)
            self._delayed[val] -= 1
            if self._delayed[val] == 0:
                del self._delayed[val]
    
    def _prune_max_heap(self) -> None:
        """清理大顶堆顶部的延迟删除元素"""
        while self._max_heap and self._delayed.get(-self._max_heap[0], 0) > 0:
            val = -heapq.heappop(self._max_heap)
            self._delayed[val] -= 1
            if self._delayed[val] == 0:
                del self._delayed[val]
    
    def _prune_min_heap(self) -> None:
        """清理小顶堆顶部的延迟删除元素"""
        while self._min_heap and self._delayed.get(self._min_heap[0], 0) > 0:
            val = heapq.heappop(self._min_heap)
            self._delayed[val] -= 1
            if self._delayed[val] == 0:
                del self._delayed[val]
    
    def median(self) -> Optional[float]:
        """获取当前窗口的中位数"""
        if not self._data:
            return None
        
        self._prune()
        
        if self._max_heap_size > self._min_heap_size:
            return -self._max_heap[0]
        else:
            return (-self._max_heap[0] + self._min_heap[0]) / 2
    
    def __len__(self) -> int:
        return len(self._data)
    
    def is_empty(self) -> bool:
        return len(self._data) == 0
    
    def is_full(self) -> bool:
        return len(self._data) == self.window_size
    
    def clear(self) -> None:
        """清空窗口"""
        self._data.clear()
        self._max_heap.clear()
        self._min_heap.clear()
        self._delayed.clear()
        self._max_heap_size = 0
        self._min_heap_size = 0


class SlidingWindowPercentile:
    """
    滑动窗口百分位数计算器
    
    支持任意百分位数的计算，使用两个有序列表实现。
    
    示例:
        >>> swp = SlidingWindowPercentile(5, percentile=75)
        >>> for val in [1, 2, 3, 4, 5, 6, 7]:
        ...     swp.push(val)
        ...     print(f"P75={swp.percentile_value()}")
    """
    
    def __init__(self, window_size: int, percentile: float = 50.0):
        """
        初始化百分位数计算器
        
        Args:
            window_size: 窗口大小
            percentile: 百分位数 (0-100)，默认50（中位数）
        """
        if window_size <= 0:
            raise ValueError("窗口大小必须为正整数")
        if not 0 <= percentile <= 100:
            raise ValueError("百分位数必须在 0-100 之间")
        
        self.window_size = window_size
        self.percentile = percentile
        self._data: deque = deque()
    
    def push(self, value: float) -> Optional[float]:
        """添加新值到窗口"""
        popped = None
        if len(self._data) >= self.window_size:
            popped = self._data.popleft()
        self._data.append(value)
        return popped
    
    def percentile_value(self) -> Optional[float]:
        """获取当前窗口的百分位数值"""
        if not self._data:
            return None
        
        sorted_data = sorted(self._data)
        n = len(sorted_data)
        
        # 计算百分位位置
        index = (self.percentile / 100) * (n - 1)
        lower = int(index)
        upper = lower + 1
        
        if upper >= n:
            return sorted_data[lower]
        
        # 线性插值
        weight = index - lower
        return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight
    
    def set_percentile(self, percentile: float) -> None:
        """设置百分位数"""
        if not 0 <= percentile <= 100:
            raise ValueError("百分位数必须在 0-100 之间")
        self.percentile = percentile
    
    def __len__(self) -> int:
        return len(self._data)
    
    def is_empty(self) -> bool:
        return len(self._data) == 0
    
    def is_full(self) -> bool:
        return len(self._data) == self.window_size
    
    def clear(self) -> None:
        """清空窗口"""
        self._data.clear()


class TimeWindowStats:
    """
    时间窗口统计计算器
    
    基于时间戳的滑动窗口，自动清理过期数据。
    
    示例:
        >>> import time
        >>> tws = TimeWindowStats(window_seconds=10)
        >>> tws.push(time.time(), 100)
        >>> tws.push(time.time(), 200)
        >>> print(f"avg={tws.mean()}")
    """
    
    def __init__(self, window_seconds: float):
        """
        初始化时间窗口统计计算器
        
        Args:
            window_seconds: 窗口时长（秒）
        """
        if window_seconds <= 0:
            raise ValueError("窗口时长必须为正数")
        self.window_seconds = window_seconds
        self._data: deque = deque()  # 存储 (timestamp, value) 元组
    
    def push(self, timestamp: float, value: float, current_time: Optional[float] = None) -> int:
        """
        添加带时间戳的数据点
        
        Args:
            timestamp: 数据的时间戳（秒）
            value: 数值
            current_time: 当前时间戳（秒），用于判断过期。如果不提供，使用系统当前时间
            
        Returns:
            清理的过期数据点数量
        """
        ref_time = current_time if current_time is not None else time.time()
        self._data.append((timestamp, value))
        return self._cleanup(ref_time)
    
    def _cleanup(self, current_time: float) -> int:
        """清理过期数据"""
        cutoff = current_time - self.window_seconds
        removed = 0
        while self._data and self._data[0][0] < cutoff:
            self._data.popleft()
            removed += 1
        return removed
    
    def refresh(self, current_time: float) -> int:
        """刷新窗口，清理过期数据"""
        return self._cleanup(current_time)
    
    def sum(self) -> float:
        """获取窗口内数据总和"""
        return sum(v for _, v in self._data)
    
    def mean(self) -> Optional[float]:
        """获取窗口内数据平均值"""
        if not self._data:
            return None
        return self.sum() / len(self._data)
    
    def min(self) -> Optional[float]:
        """获取窗口内最小值"""
        if not self._data:
            return None
        return min(v for _, v in self._data)
    
    def max(self) -> Optional[float]:
        """获取窗口内最大值"""
        if not self._data:
            return None
        return max(v for _, v in self._data)
    
    def count(self) -> int:
        """获取窗口内数据点数量"""
        return len(self._data)
    
    def rate(self, current_time: Optional[float] = None) -> Optional[float]:
        """
        计算数据点的到达速率（每秒多少个）
        
        Args:
            current_time: 当前时间戳，如果提供会先清理过期数据
            
        Returns:
            速率，如果没有数据返回 None
        """
        if current_time is not None:
            self._cleanup(current_time)
        
        if len(self._data) < 2:
            return None
        
        time_span = self._data[-1][0] - self._data[0][0]
        if time_span <= 0:
            return None
        
        return (len(self._data) - 1) / time_span
    
    def time_span(self) -> Optional[float]:
        """获取窗口内数据的时间跨度（秒）"""
        if len(self._data) < 2:
            return None
        return self._data[-1][0] - self._data[0][0]
    
    def __len__(self) -> int:
        return len(self._data)
    
    def is_empty(self) -> bool:
        return len(self._data) == 0
    
    def clear(self) -> None:
        """清空窗口"""
        self._data.clear()


class SlidingWindowCounter:
    """
    滑动窗口计数器
    
    统计滑动窗口内的事件数量，支持任意类型的键。
    
    示例:
        >>> counter = SlidingWindowCounter(window_size=5)
        >>> for event in ['a', 'b', 'a', 'c', 'a', 'b']:
        ...     counter.push(event)
        ...     print(f"a: {counter.count('a')}, total: {counter.total()}")
    """
    
    def __init__(self, window_size: int):
        if window_size <= 0:
            raise ValueError("窗口大小必须为正整数")
        self.window_size = window_size
        self._data: deque = deque()
        self._counts: dict = {}
    
    def push(self, key: Any) -> Optional[Any]:
        """
        添加一个事件
        
        Args:
            key: 事件键
            
        Returns:
            被移除的事件键（如果窗口已满）
        """
        popped = None
        
        if len(self._data) >= self.window_size:
            popped = self._data.popleft()
            self._counts[popped] -= 1
            if self._counts[popped] == 0:
                del self._counts[popped]
        
        self._data.append(key)
        self._counts[key] = self._counts.get(key, 0) + 1
        
        return popped
    
    def count(self, key: Any) -> int:
        """获取指定键在窗口内的出现次数"""
        return self._counts.get(key, 0)
    
    def total(self) -> int:
        """获取窗口内事件总数"""
        return len(self._data)
    
    def unique_count(self) -> int:
        """获取窗口内唯一键的数量"""
        return len(self._counts)
    
    def most_common(self, n: int = 1) -> List[Tuple[Any, int]]:
        """
        获取出现次数最多的 n 个键
        
        Args:
            n: 返回数量
            
        Returns:
            (key, count) 元组列表，按计数降序排列
        """
        sorted_items = sorted(self._counts.items(), key=lambda x: (-x[1], x[0]))
        return sorted_items[:n]
    
    def all_counts(self) -> dict:
        """获取所有键的计数（副本）"""
        return self._counts.copy()
    
    def __len__(self) -> int:
        return len(self._data)
    
    def is_empty(self) -> bool:
        return len(self._data) == 0
    
    def is_full(self) -> bool:
        return len(self._data) == self.window_size
    
    def clear(self) -> None:
        """清空窗口"""
        self._data.clear()
        self._counts.clear()


# 便捷函数

def sliding_max(data: List[T], window_size: int) -> List[Optional[T]]:
    """
    计算滑动窗口最大值
    
    Args:
        data: 输入数据列表
        window_size: 窗口大小
        
    Returns:
        每个位置的最大值列表
    """
    swm = SlidingWindowMax(window_size)
    result = []
    for val in data:
        swm.push(val)
        result.append(swm.max())
    return result


def sliding_min(data: List[T], window_size: int) -> List[Optional[T]]:
    """
    计算滑动窗口最小值
    
    Args:
        data: 输入数据列表
        window_size: 窗口大小
        
    Returns:
        每个位置的最小值列表
    """
    swm = SlidingWindowMin(window_size)
    result = []
    for val in data:
        swm.push(val)
        result.append(swm.min())
    return result


def sliding_mean(data: List[float], window_size: int) -> List[Optional[float]]:
    """
    计算滑动窗口平均值
    
    Args:
        data: 输入数据列表
        window_size: 窗口大小
        
    Returns:
        每个位置的平均值列表
    """
    stats = SlidingWindowStats(window_size)
    result = []
    for val in data:
        stats.push(val)
        result.append(stats.mean())
    return result


def sliding_sum(data: List[float], window_size: int) -> List[float]:
    """
    计算滑动窗口总和
    
    Args:
        data: 输入数据列表
        window_size: 窗口大小
        
    Returns:
        每个位置的总和列表
    """
    stats = SlidingWindowStats(window_size)
    result = []
    for val in data:
        stats.push(val)
        result.append(stats.sum())
    return result


def sliding_median(data: List[float], window_size: int) -> List[Optional[float]]:
    """
    计算滑动窗口中位数
    
    Args:
        data: 输入数据列表
        window_size: 窗口大小
        
    Returns:
        每个位置的中位数列表
    """
    swm = SlidingWindowMedian(window_size)
    result = []
    for val in data:
        swm.push(val)
        result.append(swm.median())
    return result


if __name__ == "__main__":
    # 简单演示
    print("=== 滑动窗口最大值 ===")
    data = [1, 3, 2, 5, 4, 6, 3, 2]
    print(f"数据: {data}")
    print(f"窗口大小: 3")
    print(f"最大值: {sliding_max(data, 3)}")
    
    print("\n=== 滑动窗口统计 ===")
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"数据: {data}")
    print(f"窗口大小: 4")
    print(f"平均值: {sliding_mean(data, 4)}")
    print(f"总和: {sliding_sum(data, 4)}")
    
    stats = SlidingWindowStats(4)
    for val in data:
        stats.push(val)
        if stats.is_full():
            print(f"窗口: {stats._sum/std_dev:.2f}")  # 演示用