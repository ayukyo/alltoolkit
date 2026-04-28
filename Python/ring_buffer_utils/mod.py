"""
Ring Buffer Utils - 循环缓冲区工具集

提供循环缓冲区（环形缓冲区）的实现，适用于：
- 固定大小队列
- 滚动窗口统计
- 事件缓冲
- 数据流处理

特点：
- 零外部依赖
- 线程安全选项
- 支持迭代和切片
- 支持统计操作
"""

from typing import TypeVar, Generic, Optional, Iterator, List, Any, Callable, Tuple, Sequence
import threading

T = TypeVar('T')


class RingBuffer(Generic[T], Sequence):
    """
    循环缓冲区（环形缓冲区）
    
    当缓冲区满时，新元素会覆盖最旧的元素。
    支持随机访问、迭代和切片操作。
    
    示例:
        >>> rb = RingBuffer[int](5)
        >>> rb.append(1)
        >>> rb.append(2)
        >>> rb.extend([3, 4, 5, 6])  # 会覆盖 1
        >>> list(rb)
        [2, 3, 4, 5, 6]
    """
    
    def __init__(self, capacity: int, thread_safe: bool = False):
        """
        初始化循环缓冲区
        
        Args:
            capacity: 缓冲区容量
            thread_safe: 是否线程安全
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self._capacity = capacity
        self._buffer: List[Optional[T]] = [None] * capacity
        self._head = 0  # 写入位置
        self._count = 0  # 当前元素数量
        self._thread_safe = thread_safe
        self._lock = threading.RLock() if thread_safe else None
    
    def __len__(self) -> int:
        """返回当前元素数量"""
        return self._count
    
    def __bool__(self) -> bool:
        """是否有元素"""
        return self._count > 0
    
    def __getitem__(self, index: int) -> T:
        """获取指定索引的元素（支持负索引）"""
        if self._lock:
            with self._lock:
                return self._get_item(index)
        return self._get_item(index)
    
    def _get_item(self, index: int) -> T:
        """内部获取元素方法"""
        if not -self._count <= index < self._count:
            raise IndexError(f"Index {index} out of range for buffer of size {self._count}")
        
        # 处理负索引
        if index < 0:
            index += self._count
        
        # 计算实际位置
        if self._count < self._capacity:
            # 缓冲区未满，从 0 开始
            actual_index = index
        else:
            # 缓冲区已满，从 _head 开始循环
            actual_index = (self._head + index) % self._capacity
        
        value = self._buffer[actual_index]
        if value is None:
            raise IndexError("Accessing uninitialized element")
        return value
    
    def __iter__(self) -> Iterator[T]:
        """迭代所有元素"""
        if self._lock:
            with self._lock:
                return self._iterate()
        return self._iterate()
    
    def _iterate(self) -> Iterator[T]:
        """内部迭代方法"""
        for i in range(self._count):
            yield self._get_item(i)
    
    def __reversed__(self) -> Iterator[T]:
        """反向迭代"""
        for i in range(self._count - 1, -1, -1):
            yield self[i]
    
    def __contains__(self, item: T) -> bool:
        """检查元素是否存在"""
        return item in list(self)
    
    def __repr__(self) -> str:
        items = list(self)
        return f"RingBuffer({items})"
    
    def __str__(self) -> str:
        return str(list(self))
    
    @property
    def capacity(self) -> int:
        """缓冲区容量"""
        return self._capacity
    
    @property
    def is_full(self) -> bool:
        """缓冲区是否已满"""
        return self._count >= self._capacity
    
    @property
    def is_empty(self) -> bool:
        """缓冲区是否为空"""
        return self._count == 0
    
    def append(self, item: T) -> None:
        """
        添加一个元素
        
        如果缓冲区已满，会覆盖最旧的元素。
        
        Args:
            item: 要添加的元素
        """
        if self._lock:
            with self._lock:
                self._append(item)
        else:
            self._append(item)
    
    def _append(self, item: T) -> None:
        """内部添加方法"""
        self._buffer[self._head] = item
        self._head = (self._head + 1) % self._capacity
        if self._count < self._capacity:
            self._count += 1
    
    def extend(self, items: Sequence[T]) -> None:
        """
        批量添加元素
        
        Args:
            items: 要添加的元素序列
        """
        for item in items:
            self.append(item)
    
    def appendleft(self, item: T) -> None:
        """
        在缓冲区开头添加元素（覆盖最新的元素）
        
        注意：这是一个特殊操作，通常循环缓冲区只支持末尾添加
        
        Args:
            item: 要添加的元素
        """
        if self._lock:
            with self._lock:
                self._appendleft(item)
        else:
            self._appendleft(item)
    
    def _appendleft(self, item: T) -> None:
        """内部左端添加方法"""
        if self._count == 0:
            self._buffer[0] = item
            self._head = 1
            self._count = 1
        else:
            # 计算最旧元素的位置
            if self._count < self._capacity:
                oldest_pos = 0
            else:
                oldest_pos = self._head
            
            self._buffer[oldest_pos] = item
    
    def pop(self) -> T:
        """
        弹出最新添加的元素
        
        Returns:
            最新添加的元素
            
        Raises:
            IndexError: 缓冲区为空
        """
        if self._lock:
            with self._lock:
                return self._pop()
        return self._pop()
    
    def _pop(self) -> T:
        """内部弹出方法"""
        if self._count == 0:
            raise IndexError("Pop from empty buffer")
        
        self._head = (self._head - 1 + self._capacity) % self._capacity
        value = self._buffer[self._head]
        self._buffer[self._head] = None
        self._count -= 1
        
        if value is None:
            raise IndexError("Popped uninitialized element")
        return value
    
    def popleft(self) -> T:
        """
        弹出最旧的元素
        
        Returns:
            最旧的元素
            
        Raises:
            IndexError: 缓冲区为空
        """
        if self._lock:
            with self._lock:
                return self._popleft()
        return self._popleft()
    
    def _popleft(self) -> T:
        """内部左端弹出方法"""
        if self._count == 0:
            raise IndexError("Pop from empty buffer")
        
        # 计算最旧元素的位置
        if self._count < self._capacity:
            # 缓冲区未满，最旧元素从位置 0 开始
            oldest_pos = 0
            # 将后续元素前移
            value = self._buffer[0]
            for i in range(self._count - 1):
                self._buffer[i] = self._buffer[i + 1]
            self._buffer[self._count - 1] = None
        else:
            # 缓冲区已满，最旧元素在 _head 位置
            oldest_pos = self._head
            value = self._buffer[oldest_pos]
            self._buffer[oldest_pos] = None
        
        self._count -= 1
        
        if value is None:
            raise IndexError("Popped uninitialized element")
        return value
    
    def clear(self) -> None:
        """清空缓冲区"""
        if self._lock:
            with self._lock:
                self._clear()
        else:
            self._clear()
    
    def _clear(self) -> None:
        """内部清空方法"""
        self._buffer = [None] * self._capacity
        self._head = 0
        self._count = 0
    
    def peek(self) -> T:
        """
        查看最新元素（不删除）
        
        Returns:
            最新添加的元素
            
        Raises:
            IndexError: 缓冲区为空
        """
        if self._count == 0:
            raise IndexError("Peek from empty buffer")
        return self[-1]
    
    def peekleft(self) -> T:
        """
        查看最旧元素（不删除）
        
        Returns:
            最旧的元素
            
        Raises:
            IndexError: 缓冲区为空
        """
        if self._count == 0:
            raise IndexError("Peek from empty buffer")
        return self[0]
    
    def to_list(self) -> List[T]:
        """
        转换为列表
        
        Returns:
            包含所有元素的列表（按添加顺序）
        """
        return list(self)
    
    def copy(self) -> 'RingBuffer[T]':
        """
        创建副本
        
        Returns:
            新的 RingBuffer 实例
        """
        new_buffer = RingBuffer[T](self._capacity, self._thread_safe)
        new_buffer.extend(self.to_list())
        return new_buffer
    
    def rotate(self, n: int = 1) -> None:
        """
        旋转缓冲区
        
        正数表示向右旋转（最新变为最旧），负数表示向左旋转。
        
        Args:
            n: 旋转步数
        """
        if self._count == 0:
            return
        
        if self._lock:
            with self._lock:
                self._rotate(n)
        else:
            self._rotate(n)
    
    def _rotate(self, n: int) -> None:
        """内部旋转方法"""
        n = n % self._count
        if n == 0:
            return
        
        # 将元素旋转
        items = self.to_list()
        rotated = items[-n:] + items[:-n]
        
        self._clear()
        self.extend(rotated)


class NumericRingBuffer(RingBuffer[float]):
    """
    数值型循环缓冲区
    
    提供额外的统计功能：均值、方差、标准差、最大值、最小值等
    """
    
    def __init__(self, capacity: int, thread_safe: bool = False):
        """初始化数值型循环缓冲区"""
        super().__init__(capacity, thread_safe)
        self._sum = 0.0
        self._sum_sq = 0.0
        self._min: Optional[float] = None
        self._max: Optional[float] = None
    
    def append(self, item: float) -> None:
        """添加元素并更新统计"""
        if self._lock:
            with self._lock:
                self._append_with_stats(item)
        else:
            self._append_with_stats(item)
    
    def _append_with_stats(self, item: float) -> None:
        """带统计更新的添加方法"""
        # 如果缓冲区已满，需要减去被覆盖的值
        old_value = None
        if self._count == self._capacity:
            old_value = self._buffer[self._head]
            if old_value is not None:
                self._sum -= old_value
                self._sum_sq -= old_value * old_value
        
        super()._append(item)
        
        self._sum += item
        self._sum_sq += item * item
        
        # 更新最大最小值
        if self._min is None or item < self._min:
            self._min = item
        if self._max is None or item > self._max:
            self._max = item
        
        # 如果被覆盖的值是当前的 min 或 max，需要重新计算
        if old_value is not None:
            if old_value == self._min or old_value == self._max:
                self._recalculate_min_max()
    
    def _recalculate_min_max(self) -> None:
        """重新计算 min 和 max 值"""
        self._min = None
        self._max = None
        for i in range(self._count):
            val = self._get_item(i)
            if self._min is None or val < self._min:
                self._min = val
            if self._max is None or val > self._max:
                self._max = val
    
    def clear(self) -> None:
        """清空缓冲区并重置统计"""
        super().clear()
        self._sum = 0.0
        self._sum_sq = 0.0
        self._min = None
        self._max = None
    
    @property
    def mean(self) -> float:
        """
        计算均值
        
        Returns:
            所有元素的均值
            
        Raises:
            ValueError: 缓冲区为空
        """
        if self._count == 0:
            raise ValueError("Cannot compute mean of empty buffer")
        return self._sum / self._count
    
    @property
    def variance(self) -> float:
        """
        计算方差
        
        Returns:
            所有元素的样本方差
            
        Raises:
            ValueError: 缓冲区元素少于 2 个
        """
        if self._count < 2:
            raise ValueError("Need at least 2 elements to compute variance")
        
        mean = self.mean
        return (self._sum_sq - self._count * mean * mean) / (self._count - 1)
    
    @property
    def std_dev(self) -> float:
        """
        计算标准差
        
        Returns:
            所有元素的样本标准差
        """
        import math
        return math.sqrt(self.variance)
    
    @property
    def min_value(self) -> float:
        """
        获取最小值
        
        Returns:
            所有元素的最小值
        """
        if self._min is None:
            raise ValueError("Buffer is empty")
        return self._min
    
    @property
    def max_value(self) -> float:
        """
        获取最大值
        
        Returns:
            所有元素的最大值
        """
        if self._max is None:
            raise ValueError("Buffer is empty")
        return self._max
    
    @property
    def range(self) -> float:
        """
        获取范围（最大值 - 最小值）
        
        Returns:
            元素范围
        """
        return self.max_value - self.min_value
    
    @property
    def sum(self) -> float:
        """获取总和"""
        return self._sum
    
    def moving_average(self, window: int) -> List[float]:
        """
        计算移动平均
        
        Args:
            window: 窗口大小
            
        Returns:
            移动平均值列表
        """
        if window > self._count:
            raise ValueError(f"Window size {window} exceeds buffer size {self._count}")
        
        items = self.to_list()
        result = []
        
        for i in range(len(items) - window + 1):
            window_sum = sum(items[i:i + window])
            result.append(window_sum / window)
        
        return result


class EventBuffer(Generic[T]):
    """
    事件缓冲区
    
    带时间戳的事件缓冲，支持时间窗口查询和过期清理。
    适用于事件日志、监控数据等场景。
    """
    
    from time import time
    
    def __init__(self, capacity: int = 1000, ttl_seconds: Optional[float] = None):
        """
        初始化事件缓冲区
        
        Args:
            capacity: 最大容量
            ttl_seconds: 事件存活时间（秒），None 表示不过期
        """
        self._buffer = RingBuffer[Tuple[float, T]](capacity)
        self._ttl = ttl_seconds
    
    def add(self, event: T, timestamp: Optional[float] = None) -> None:
        """
        添加事件
        
        Args:
            event: 事件数据
            timestamp: 时间戳，默认使用当前时间
        """
        from time import time
        if timestamp is None:
            timestamp = time()
        self._buffer.append((timestamp, event))
    
    def get_events(self, since: Optional[float] = None, until: Optional[float] = None) -> List[Tuple[float, T]]:
        """
        获取指定时间范围内的事件
        
        Args:
            since: 起始时间戳（包含）
            until: 结束时间戳（不包含）
            
        Returns:
            (时间戳, 事件) 元组列表
        """
        if since is None and until is None:
            return self._buffer.to_list()
        
        result = []
        for ts, event in self._buffer:
            if since is not None and ts < since:
                continue
            if until is not None and ts >= until:
                continue
            result.append((ts, event))
        
        return result
    
    def get_event_data(self, since: Optional[float] = None, until: Optional[float] = None) -> List[T]:
        """
        获取指定时间范围内的事件数据（不含时间戳）
        
        Args:
            since: 起始时间戳
            until: 结束时间戳
            
        Returns:
            事件数据列表
        """
        return [event for _, event in self.get_events(since, until)]
    
    def cleanup_expired(self) -> int:
        """
        清理过期事件
        
        Returns:
            清理的事件数量
        """
        if self._ttl is None:
            return 0
        
        from time import time
        cutoff = time() - self._ttl
        
        # 获取未过期的事件
        valid_events = [(ts, event) for ts, event in self._buffer if ts >= cutoff]
        expired_count = len(self._buffer) - len(valid_events)
        
        # 重建缓冲区
        self._buffer.clear()
        for event in valid_events:
            self._buffer.append(event)
        
        return expired_count
    
    def count(self, since: Optional[float] = None, until: Optional[float] = None) -> int:
        """
        统计事件数量
        
        Args:
            since: 起始时间戳
            until: 结束时间戳
            
        Returns:
            事件数量
        """
        return len(self.get_events(since, until))
    
    def __len__(self) -> int:
        return len(self._buffer)
    
    def __iter__(self) -> Iterator[Tuple[float, T]]:
        return iter(self._buffer)
    
    def clear(self) -> None:
        """清空缓冲区"""
        self._buffer.clear()


def create_ring_buffer(capacity: int, initial_data: Optional[Sequence[T]] = None,
                       thread_safe: bool = False) -> RingBuffer[T]:
    """
    创建循环缓冲区的便捷函数
    
    Args:
        capacity: 缓冲区容量
        initial_data: 初始数据
        thread_safe: 是否线程安全
        
    Returns:
        RingBuffer 实例
    """
    buffer = RingBuffer[T](capacity, thread_safe)
    if initial_data:
        buffer.extend(initial_data)
    return buffer


def create_numeric_buffer(capacity: int, initial_data: Optional[Sequence[float]] = None,
                          thread_safe: bool = False) -> NumericRingBuffer:
    """
    创建数值型循环缓冲区的便捷函数
    
    Args:
        capacity: 缓冲区容量
        initial_data: 初始数据
        thread_safe: 是否线程安全
        
    Returns:
        NumericRingBuffer 实例
    """
    buffer = NumericRingBuffer(capacity, thread_safe)
    if initial_data:
        buffer.extend(initial_data)
    return buffer


def sliding_window(data: Sequence[T], window_size: int) -> Iterator[List[T]]:
    """
    滑动窗口迭代器
    
    将数据分割为固定大小的滑动窗口。
    
    Args:
        data: 输入数据序列
        window_size: 窗口大小
        
    Yields:
        每个窗口的元素列表
        
    示例:
        >>> list(sliding_window([1, 2, 3, 4, 5], 3))
        [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    """
    if window_size <= 0:
        raise ValueError("Window size must be positive")
    
    data_len = len(data)
    if data_len < window_size:
        return
    
    # 优化：直接使用切片，避免创建 RingBuffer 的开销
    for i in range(data_len - window_size + 1):
        yield list(data[i:i + window_size])


def batch_process(data: Sequence[T], batch_size: int, 
                  processor: Callable[[List[T]], Any]) -> List[Any]:
    """
    批量处理数据
    
    将数据分割为固定大小的批次进行处理。
    
    Args:
        data: 输入数据
        batch_size: 批次大小
        processor: 处理函数
        
    Returns:
        处理结果列表
    """
    if batch_size <= 0:
        raise ValueError("Batch size must be positive")
    
    results = []
    for i in range(0, len(data), batch_size):
        batch = list(data[i:i + batch_size])
        results.append(processor(batch))
    
    return results


# 导出的公共接口
__all__ = [
    'RingBuffer',
    'NumericRingBuffer', 
    'EventBuffer',
    'create_ring_buffer',
    'create_numeric_buffer',
    'sliding_window',
    'batch_process',
]