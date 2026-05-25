"""
优先队列工具模块 (Priority Queue Utils)

提供高性能优先队列实现，支持自定义比较器、优先级更新、线程安全等特性。
零外部依赖，纯 Python 标准库实现。

功能特性：
- 基于 heapq 的高效优先队列
- 支持最小堆和最大堆模式
- 支持自定义优先级比较器
- 支持动态优先级更新
- 支持批量插入和批量删除
- 线程安全版本
- 优先队列合并
- 延迟删除标记
"""

import heapq
from typing import (
    TypeVar, Generic, Callable, Optional, List, Tuple, 
    Any, Dict, Set, Iterator, Iterable, Union
)
from dataclasses import dataclass, field
from functools import total_ordering
import threading
from enum import Enum


T = TypeVar('T')
P = TypeVar('P')


class QueueMode(Enum):
    """队列模式"""
    MIN_HEAP = "min"   # 最小堆：最小值在队首
    MAX_HEAP = "max"   # 最大堆：最大值在队首


@total_ordering
@dataclass
class PriorityQueueItem(Generic[T, P]):
    """
    优先队列元素包装器
    
    Attributes:
        value: 实际存储的值
        priority: 优先级（数值越小优先级越高，除非使用最大堆模式）
        sequence: 插入序列号（保证 FIFO 稳定性）
        valid: 是否有效（用于延迟删除）
    """
    value: T
    priority: P
    sequence: int = 0
    valid: bool = True
    
    def __lt__(self, other: 'PriorityQueueItem') -> bool:
        if not isinstance(other, PriorityQueueItem):
            return NotImplemented
        # 先比较优先级，再比较序列号（保证稳定性）
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.sequence < other.sequence
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PriorityQueueItem):
            return NotImplemented
        return (self.priority, self.sequence) == (other.priority, other.sequence)
    
    def __hash__(self) -> int:
        return hash((self.priority, self.sequence))


class PriorityQueue(Generic[T, P]):
    """
    优先队列实现
    
    支持最小堆（默认）和最大堆模式，支持动态优先级更新。
    
    Example:
        >>> pq = PriorityQueue[str, int]()
        >>> pq.push("task1", 3)
        >>> pq.push("task2", 1)
        >>> pq.push("task3", 2)
        >>> pq.pop()
        ('task2', 1)
    """
    
    def __init__(
        self, 
        mode: QueueMode = QueueMode.MIN_HEAP,
        comparator: Optional[Callable[[P, P], bool]] = None
    ):
        """
        初始化优先队列
        
        Args:
            mode: 队列模式（MIN_HEAP 或 MAX_HEAP）
            comparator: 自定义比较器函数，返回 True 表示第一个参数优先级更高
        """
        self._heap: List[PriorityQueueItem[T, P]] = []
        self._sequence = 0
        self._mode = mode
        self._comparator = comparator
        self._entry_map: Dict[int, PriorityQueueItem[T, P]] = {}  # sequence -> item
        self._value_sequences: Dict[T, Set[int]] = {}  # value -> set of sequences
        self._invalid_count = 0  # 无效元素计数
    
    def push(self, value: T, priority: P) -> int:
        """
        入队
        
        Args:
            value: 存储的值
            priority: 优先级
            
        Returns:
            元素的序列号（可用于后续更新或删除）
        """
        # 如果是最大堆，取负数实现
        actual_priority = priority
        if self._mode == QueueMode.MAX_HEAP and self._comparator is None:
            # 对数值类型取负
            try:
                actual_priority = -priority  # type: ignore
            except TypeError:
                # 非数值类型，需要自定义比较器
                pass
        
        self._sequence += 1
        item = PriorityQueueItem(
            value=value,
            priority=actual_priority,
            sequence=self._sequence,
            valid=True
        )
        
        heapq.heappush(self._heap, item)
        self._entry_map[self._sequence] = item
        
        # 维护值到序列号的映射
        if value not in self._value_sequences:
            self._value_sequences[value] = set()
        self._value_sequences[value].add(self._sequence)
        
        return self._sequence
    
    def pop(self) -> Optional[Tuple[T, P]]:
        """
        出队（返回优先级最高的元素）
        
        Returns:
            (value, priority) 元组，如果队列为空则返回 None
        """
        self._cleanup_invalid()
        
        if not self._heap:
            return None
        
        item = heapq.heappop(self._heap)
        del self._entry_map[item.sequence]
        
        # 清理值映射
        if item.value in self._value_sequences:
            self._value_sequences[item.value].discard(item.sequence)
            if not self._value_sequences[item.value]:
                del self._value_sequences[item.value]
        
        # 恢复原始优先级
        original_priority = item.priority
        if self._mode == QueueMode.MAX_HEAP and self._comparator is None:
            try:
                original_priority = -item.priority  # type: ignore
            except TypeError:
                pass
        
        return (item.value, original_priority)
    
    def peek(self) -> Optional[Tuple[T, P]]:
        """
        查看队首元素（不出队）
        
        Returns:
            (value, priority) 元组，如果队列为空则返回 None
        """
        self._cleanup_invalid()
        
        if not self._heap:
            return None
        
        item = self._heap[0]
        original_priority = item.priority
        if self._mode == QueueMode.MAX_HEAP and self._comparator is None:
            try:
                original_priority = -item.priority  # type: ignore
            except TypeError:
                pass
        
        return (item.value, original_priority)
    
    def update_priority(self, sequence: int, new_priority: P) -> bool:
        """
        更新指定元素的优先级
        
        Args:
            sequence: 元素序列号（push 时返回）
            new_priority: 新的优先级
            
        Returns:
            是否更新成功
        """
        if sequence not in self._entry_map:
            return False
        
        item = self._entry_map[sequence]
        if not item.valid:
            return False
        
        # 标记旧元素无效
        item.valid = False
        self._invalid_count += 1
        
        # 插入新元素
        return self.push(item.value, new_priority) > 0
    
    def update_priority_by_value(self, value: T, new_priority: P) -> int:
        """
        更新所有指定值的元素优先级
        
        Args:
            value: 要更新的值
            new_priority: 新的优先级
            
        Returns:
            更新的元素数量
        """
        if value not in self._value_sequences:
            return 0
        
        sequences = list(self._value_sequences[value])
        count = 0
        
        for seq in sequences:
            if self.update_priority(seq, new_priority):
                count += 1
        
        return count
    
    def remove(self, sequence: int) -> bool:
        """
        删除指定元素（延迟删除）
        
        Args:
            sequence: 元素序列号
            
        Returns:
            是否删除成功
        """
        if sequence not in self._entry_map:
            return False
        
        item = self._entry_map[sequence]
        if not item.valid:
            return False
        
        item.valid = False
        self._invalid_count += 1
        return True
    
    def remove_by_value(self, value: T) -> int:
        """
        删除所有指定值的元素
        
        Args:
            value: 要删除的值
            
        Returns:
            删除的元素数量
        """
        if value not in self._value_sequences:
            return 0
        
        sequences = list(self._value_sequences[value])
        count = 0
        
        for seq in sequences:
            if self.remove(seq):
                count += 1
        
        return count
    
    def contains(self, value: T) -> bool:
        """
        检查队列是否包含指定值
        
        Args:
            value: 要检查的值
            
        Returns:
            是否包含
        """
        if value not in self._value_sequences:
            return False
        
        # 检查是否有有效的序列号
        for seq in self._value_sequences[value]:
            if seq in self._entry_map and self._entry_map[seq].valid:
                return True
        
        return False
    
    def get_priority(self, value: T) -> Optional[List[P]]:
        """
        获取指定值的所有优先级
        
        Args:
            value: 要查询的值
            
        Returns:
            优先级列表，如果不存在则返回 None
        """
        if value not in self._value_sequences:
            return None
        
        priorities = []
        for seq in self._value_sequences[value]:
            if seq in self._entry_map and self._entry_map[seq].valid:
                priority = self._entry_map[seq].priority
                if self._mode == QueueMode.MAX_HEAP and self._comparator is None:
                    try:
                        priority = -priority  # type: ignore
                    except TypeError:
                        pass
                priorities.append(priority)
        
        return priorities if priorities else None
    
    def extend(self, items: Iterable[Tuple[T, P]]) -> List[int]:
        """
        批量入队
        
        Args:
            items: (value, priority) 可迭代对象
            
        Returns:
            所有元素的序列号列表
        """
        return [self.push(value, priority) for value, priority in items]
    
    def drain(self, n: Optional[int] = None) -> List[Tuple[T, P]]:
        """
        批量出队
        
        Args:
            n: 出队数量，None 表示全部出队
            
        Returns:
            (value, priority) 列表
        """
        result = []
        count = 0
        
        while (n is None or count < n):
            item = self.pop()
            if item is None:
                break
            result.append(item)
            count += 1
        
        return result
    
    def merge(self, other: 'PriorityQueue[T, P]') -> int:
        """
        合并另一个优先队列
        
        Args:
            other: 要合并的优先队列
            
        Returns:
            合并的元素数量
        """
        if other._mode != self._mode:
            raise ValueError("Cannot merge queues with different modes")
        
        count = 0
        while True:
            item = other.pop()
            if item is None:
                break
            self.push(item[0], item[1])
            count += 1
        
        return count
    
    def _cleanup_invalid(self) -> None:
        """清理无效元素"""
        while self._heap and not self._heap[0].valid:
            item = heapq.heappop(self._heap)
            del self._entry_map[item.sequence]
            self._invalid_count -= 1
    
    def __len__(self) -> int:
        """返回有效元素数量"""
        return len(self._entry_map) - self._invalid_count
    
    def __bool__(self) -> bool:
        """返回队列是否非空"""
        return len(self) > 0
    
    def __contains__(self, value: T) -> bool:
        """支持 `value in queue` 语法"""
        return self.contains(value)
    
    def __iter__(self) -> Iterator[Tuple[T, P]]:
        """迭代队列（按优先级顺序）"""
        # 创建副本进行迭代
        temp_queue = PriorityQueue(mode=self._mode)
        temp_queue._heap = self._heap.copy()
        temp_queue._entry_map = self._entry_map.copy()
        temp_queue._sequence = self._sequence
        temp_queue._invalid_count = self._invalid_count
        temp_queue._value_sequences = {k: v.copy() for k, v in self._value_sequences.items()}
        
        while True:
            item = temp_queue.pop()
            if item is None:
                break
            yield item
    
    def clear(self) -> None:
        """清空队列"""
        self._heap.clear()
        self._entry_map.clear()
        self._value_sequences.clear()
        self._invalid_count = 0
        self._sequence = 0
    
    def to_list(self) -> List[Tuple[T, P]]:
        """
        转换为列表（按优先级顺序）
        
        Returns:
            (value, priority) 列表
        """
        return list(self)
    
    def copy(self) -> 'PriorityQueue[T, P]':
        """
        创建队列副本
        
        Returns:
            新的优先队列实例
        """
        new_queue = PriorityQueue(mode=self._mode)
        new_queue._heap = [PriorityQueueItem(
            value=item.value,
            priority=item.priority,
            sequence=item.sequence,
            valid=item.valid
        ) for item in self._heap]
        new_queue._sequence = self._sequence
        new_queue._entry_map = dict(self._entry_map)
        new_queue._value_sequences = {k: v.copy() for k, v in self._value_sequences.items()}
        new_queue._invalid_count = self._invalid_count
        return new_queue
    
    @property
    def mode(self) -> QueueMode:
        """获取队列模式"""
        return self._mode


class ThreadSafePriorityQueue(Generic[T, P]):
    """
    线程安全的优先队列
    
    所有操作都通过锁保护，适合多线程环境使用。
    
    Example:
        >>> pq = ThreadSafePriorityQueue[str, int]()
        >>> pq.push("task1", 3)
        >>> with pq:
        ...     pq.push("task2", 1)
        ...     print(pq.peek())
    """
    
    def __init__(self, mode: QueueMode = QueueMode.MIN_HEAP):
        """初始化线程安全优先队列"""
        self._queue = PriorityQueue[T, P](mode=mode)
        self._lock = threading.RLock()
    
    def push(self, value: T, priority: P) -> int:
        """入队（线程安全）"""
        with self._lock:
            return self._queue.push(value, priority)
    
    def pop(self) -> Optional[Tuple[T, P]]:
        """出队（线程安全）"""
        with self._lock:
            return self._queue.pop()
    
    def peek(self) -> Optional[Tuple[T, P]]:
        """查看队首（线程安全）"""
        with self._lock:
            return self._queue.peek()
    
    def update_priority(self, sequence: int, new_priority: P) -> bool:
        """更新优先级（线程安全）"""
        with self._lock:
            return self._queue.update_priority(sequence, new_priority)
    
    def update_priority_by_value(self, value: T, new_priority: P) -> int:
        """按值更新优先级（线程安全）"""
        with self._lock:
            return self._queue.update_priority_by_value(value, new_priority)
    
    def remove(self, sequence: int) -> bool:
        """删除元素（线程安全）"""
        with self._lock:
            return self._queue.remove(sequence)
    
    def remove_by_value(self, value: T) -> int:
        """按值删除（线程安全）"""
        with self._lock:
            return self._queue.remove_by_value(value)
    
    def contains(self, value: T) -> bool:
        """检查是否包含（线程安全）"""
        with self._lock:
            return self._queue.contains(value)
    
    def extend(self, items: Iterable[Tuple[T, P]]) -> List[int]:
        """批量入队（线程安全）"""
        with self._lock:
            return self._queue.extend(items)
    
    def drain(self, n: Optional[int] = None) -> List[Tuple[T, P]]:
        """批量出队（线程安全）"""
        with self._lock:
            return self._queue.drain(n)
    
    def merge(self, other: PriorityQueue[T, P]) -> int:
        """合并队列（线程安全）"""
        with self._lock:
            return self._queue.merge(other)
    
    def __len__(self) -> int:
        with self._lock:
            return len(self._queue)
    
    def __bool__(self) -> bool:
        with self._lock:
            return bool(self._queue)
    
    def __contains__(self, value: T) -> bool:
        with self._lock:
            return value in self._queue
    
    def clear(self) -> None:
        """清空队列（线程安全）"""
        with self._lock:
            self._queue.clear()
    
    def to_list(self) -> List[Tuple[T, P]]:
        """转换为列表（线程安全）"""
        with self._lock:
            return self._queue.to_list()
    
    def __enter__(self) -> 'ThreadSafePriorityQueue[T, P]':
        """支持上下文管理器"""
        self._lock.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._lock.release()
    
    @property
    def mode(self) -> QueueMode:
        """获取队列模式"""
        return self._queue.mode


class BoundedPriorityQueue(Generic[T, P]):
    """
    有界优先队列
    
    当队列达到最大容量时，自动弹出优先级最低的元素。
    
    Example:
        >>> pq = BoundedPriorityQueue[str, int](max_size=3)
        >>> pq.push("a", 1)
        >>> pq.push("b", 2)
        >>> pq.push("c", 3)
        >>> pq.push("d", 0)  # "a" 会被弹出
        >>> pq.to_list()
        [('b', 2), ('c', 3), ('d', 0)]
    """
    
    def __init__(self, max_size: int, mode: QueueMode = QueueMode.MIN_HEAP):
        """
        初始化有界优先队列
        
        Args:
            max_size: 最大容量
            mode: 队列模式
        """
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        
        self._max_size = max_size
        self._queue = PriorityQueue[T, P](mode=mode)
        self._evicted: List[Tuple[T, P]] = []  # 被弹出的元素
    
    def push(self, value: T, priority: P) -> Tuple[bool, Optional[Tuple[T, P]]]:
        """
        入队
        
        Args:
            value: 存储的值
            priority: 优先级
            
        Returns:
            (是否成功入队, 被弹出的元素或 None)
        """
        evicted = None
        
        if len(self._queue) >= self._max_size:
            # 弹出优先级最低的元素
            evicted = self._queue.pop()
            self._evicted.append(evicted)
        
        self._queue.push(value, priority)
        return (True, evicted)
    
    def pop(self) -> Optional[Tuple[T, P]]:
        """出队"""
        return self._queue.pop()
    
    def peek(self) -> Optional[Tuple[T, P]]:
        """查看队首"""
        return self._queue.peek()
    
    def get_evicted(self) -> List[Tuple[T, P]]:
        """获取所有被弹出的元素"""
        return self._evicted.copy()
    
    def clear_evicted(self) -> None:
        """清空被弹出元素列表"""
        self._evicted.clear()
    
    def __len__(self) -> int:
        return len(self._queue)
    
    def __bool__(self) -> bool:
        return bool(self._queue)
    
    def to_list(self) -> List[Tuple[T, P]]:
        """转换为列表（按优先级顺序）"""
        return self._queue.to_list()
    
    def __iter__(self) -> Iterator[Tuple[T, P]]:
        """迭代队列"""
        return iter(self._queue)
    
    @property
    def max_size(self) -> int:
        return self._max_size
    
    @property
    def is_full(self) -> bool:
        return len(self._queue) >= self._max_size


# 便捷函数
def create_min_heap() -> PriorityQueue:
    """创建最小堆优先队列"""
    return PriorityQueue(mode=QueueMode.MIN_HEAP)


def create_max_heap() -> PriorityQueue:
    """创建最大堆优先队列"""
    return PriorityQueue(mode=QueueMode.MAX_HEAP)


def merge_queues(*queues: PriorityQueue[T, P]) -> PriorityQueue[T, P]:
    """
    合并多个优先队列
    
    Args:
        *queues: 要合并的优先队列
        
    Returns:
        合并后的新优先队列
    """
    if not queues:
        return PriorityQueue()
    
    result = PriorityQueue(mode=queues[0].mode)
    
    for queue in queues:
        if queue.mode != result.mode:
            raise ValueError("All queues must have the same mode")
        result.merge(queue)
    
    return result


def from_list(
    items: List[Tuple[T, P]], 
    mode: QueueMode = QueueMode.MIN_HEAP
) -> PriorityQueue[T, P]:
    """
    从列表创建优先队列
    
    Args:
        items: (value, priority) 列表
        mode: 队列模式
        
    Returns:
        新的优先队列
    """
    queue = PriorityQueue[T, P](mode=mode)
    queue.extend(items)
    return queue


def top_k(
    items: Iterable[Tuple[T, P]], 
    k: int, 
    largest: bool = False
) -> List[Tuple[T, P]]:
    """
    获取前 K 个元素
    
    Args:
        items: (value, priority) 可迭代对象
        k: 元素数量
        largest: True 返回最大的 K 个，False 返回最小的 K 个
        
    Returns:
        前 K 个元素列表
    """
    # 使用堆辅助实现:
    # - 求最小的 K 个: 用最大堆，堆顶是当前最大的，只有比堆顶小才替换
    # - 求最大的 K 个: 用最小堆，堆顶是当前最小的，只有比堆顶大才替换
    heap: List[Tuple] = []
    
    for value, priority in items:
        if largest:
            # 求最大的 K 个：用最小堆
            if len(heap) < k:
                heapq.heappush(heap, (priority, value))
            elif priority > heap[0][0]:  # 比堆顶大才替换
                heapq.heapreplace(heap, (priority, value))
        else:
            # 求最小的 K 个：用最大堆（存负数）
            if len(heap) < k:
                heapq.heappush(heap, (-priority, value))
            elif priority < -heap[0][0]:  # 比堆顶小才替换
                heapq.heapreplace(heap, (-priority, value))
    
    # 转换结果
    if largest:
        result = [(value, priority) for priority, value in heap]
    else:
        result = [(value, -priority) for priority, value in heap]
    
    return sorted(result, key=lambda x: x[1], reverse=largest)


__all__ = [
    'PriorityQueue',
    'ThreadSafePriorityQueue', 
    'BoundedPriorityQueue',
    'PriorityQueueItem',
    'QueueMode',
    'create_min_heap',
    'create_max_heap',
    'merge_queues',
    'from_list',
    'top_k',
]