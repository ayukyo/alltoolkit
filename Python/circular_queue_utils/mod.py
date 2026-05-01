"""
Circular Queue Utils - 循环队列工具模块

提供高性能的循环队列（环形缓冲区）实现，支持固定容量、自动覆盖、阻塞操作等特性。
零外部依赖，纯 Python 标准库实现。

主要特性：
- 固定容量队列，内存预分配
- 支持自动覆盖旧元素（可选）
- 线程安全的阻塞操作
- 支持迭代器和切片访问
- 统计信息和方法链式调用

Author: AllToolkit
Date: 2026-05-01
"""

from typing import TypeVar, Generic, Optional, Iterator, List, Any, Callable, Iterable
import threading
from contextlib import contextmanager

T = TypeVar('T')


class CircularQueue(Generic[T]):
    """
    循环队列（环形缓冲区）实现
    
    特性：
    - 固定容量，内存高效
    - O(1) 入队和出队操作
    - 支持自动覆盖模式
    - 线程安全选项
    - 支持迭代、切片和统计
    
    Example:
        >>> queue = CircularQueue[int](capacity=5)
        >>> queue.enqueue(1, 2, 3)
        >>> queue.dequeue()
        1
        >>> len(queue)
        2
    """
    
    def __init__(
        self, 
        capacity: int, 
        *,
        overwrite: bool = False,
        thread_safe: bool = False
    ):
        """
        初始化循环队列
        
        Args:
            capacity: 队列容量（必须 > 0）
            overwrite: 当队列满时是否自动覆盖最旧元素（默认 False）
            thread_safe: 是否启用线程安全（默认 False）
        
        Raises:
            ValueError: 容量小于等于 0
        """
        if capacity <= 0:
            raise ValueError(f"容量必须大于 0，收到: {capacity}")
        
        self._capacity = capacity
        self._overwrite = overwrite
        self._thread_safe = thread_safe
        self._buffer: List[Optional[T]] = [None] * capacity
        self._head = 0  # 队首索引（出队位置）
        self._tail = 0  # 队尾索引（下一个入队位置）
        self._size = 0  # 当前元素数量
        self._total_enqueued = 0  # 累计入队数量
        self._total_dequeued = 0  # 累计出队数量
        self._total_overwritten = 0  # 累计覆盖数量
        
        if thread_safe:
            self._lock = threading.RLock()
            self._not_empty = threading.Condition(self._lock)
            self._not_full = threading.Condition(self._lock)
        else:
            self._lock = None
            self._not_empty = None
            self._not_full = None
    
    @property
    def capacity(self) -> int:
        """队列容量"""
        return self._capacity
    
    @property
    def overwrite(self) -> bool:
        """是否启用自动覆盖模式"""
        return self._overwrite
    
    @property
    def thread_safe(self) -> bool:
        """是否启用线程安全"""
        return self._thread_safe
    
    @property
    def is_empty(self) -> bool:
        """队列是否为空"""
        return self._size == 0
    
    @property
    def is_full(self) -> bool:
        """队列是否已满"""
        return self._size == self._capacity
    
    @property
    def size(self) -> int:
        """当前元素数量"""
        return self._size
    
    def __len__(self) -> int:
        """返回队列当前元素数量"""
        return self._size
    
    def __bool__(self) -> bool:
        """队列非空时返回 True"""
        return self._size > 0
    
    def _get_index(self, offset: int) -> int:
        """计算环形索引"""
        return (self._head + offset) % self._capacity
    
    @contextmanager
    def _sync(self):
        """线程同步上下文管理器"""
        if self._lock:
            with self._lock:
                yield
        else:
            yield
    
    def enqueue(self, *items: T) -> 'CircularQueue[T]':
        """
        入队一个或多个元素
        
        Args:
            *items: 要入队的元素
        
        Returns:
            self（支持链式调用）
        
        Raises:
            OverflowError: 队列已满且未启用覆盖模式
        """
        with self._sync():
            for item in items:
                if self.is_full:
                    if self._overwrite:
                        # 覆盖最旧的元素
                        self._head = (self._head + 1) % self._capacity
                        self._total_overwritten += 1
                    else:
                        raise OverflowError(
                            f"队列已满（容量: {self._capacity}），无法入队。"
                            f"提示: 初始化时设置 overwrite=True 启用自动覆盖"
                        )
                
                self._buffer[self._tail] = item
                self._tail = (self._tail + 1) % self._capacity
                
                if not self.is_full or self._overwrite:
                    if self._size < self._capacity:
                        self._size += 1
                
                self._total_enqueued += 1
            
            # 通知等待的消费者
            if self._not_empty:
                self._not_empty.notify_all()
        
        return self
    
    def dequeue(self) -> T:
        """
        出队一个元素
        
        Returns:
            队首元素
        
        Raises:
            IndexError: 队列为空
        """
        with self._sync():
            if self.is_empty:
                raise IndexError("队列为空，无法出队")
            
            item = self._buffer[self._head]
            self._buffer[self._head] = None  # 帮助垃圾回收
            self._head = (self._head + 1) % self._capacity
            self._size -= 1
            self._total_dequeued += 1
            
            # 通知等待的生产者
            if self._not_full:
                self._not_full.notify_all()
            
            return item
    
    def peek(self, offset: int = 0) -> T:
        """
        查看队首元素（不移除）
        
        Args:
            offset: 偏移量（0 = 队首，1 = 第二个元素，以此类推）
        
        Returns:
            指定位置的元素
        
        Raises:
            IndexError: 队列为空或偏移量越界
        """
        with self._sync():
            if self.is_empty:
                raise IndexError("队列为空")
            if offset < 0 or offset >= self._size:
                raise IndexError(f"偏移量 {offset} 越界（队列大小: {self._size}）")
            
            return self._buffer[self._get_index(offset)]
    
    def peek_last(self) -> T:
        """
        查看队尾元素（不移除）
        
        Returns:
            队尾元素
        
        Raises:
            IndexError: 队列为空
        """
        with self._sync():
            if self.is_empty:
                raise IndexError("队列为空")
            
            last_index = (self._tail - 1 + self._capacity) % self._capacity
            return self._buffer[last_index]
    
    def clear(self) -> 'CircularQueue[T]':
        """
        清空队列
        
        Returns:
            self（支持链式调用）
        """
        with self._sync():
            self._buffer = [None] * self._capacity
            self._head = 0
            self._tail = 0
            self._size = 0
        
        return self
    
    def to_list(self) -> List[T]:
        """
        转换为列表（从队首到队尾顺序）
        
        Returns:
            包含所有元素的列表
        """
        with self._sync():
            if self.is_empty:
                return []
            
            result = []
            for i in range(self._size):
                result.append(self._buffer[self._get_index(i)])
            return result
    
    def copy(self) -> 'CircularQueue[T]':
        """
        创建队列的浅拷贝
        
        Returns:
            新的 CircularQueue 实例
        """
        with self._sync():
            new_queue = CircularQueue[T](
                capacity=self._capacity,
                overwrite=self._overwrite,
                thread_safe=self._thread_safe
            )
            new_queue._buffer = self.to_list() + [None] * (self._capacity - self._size)
            new_queue._head = 0
            new_queue._tail = self._size
            new_queue._size = self._size
            return new_queue
    
    def extend(self, iterable: Iterable[T]) -> 'CircularQueue[T]':
        """
        批量入队
        
        Args:
            iterable: 可迭代对象
        
        Returns:
            self（支持链式调用）
        """
        return self.enqueue(*iterable)
    
    def __iter__(self) -> Iterator[T]:
        """迭代器，从队首到队尾"""
        with self._sync():
            for i in range(self._size):
                yield self._buffer[self._get_index(i)]
    
    def __reversed__(self) -> Iterator[T]:
        """反向迭代器，从队尾到队首"""
        with self._sync():
            for i in range(self._size - 1, -1, -1):
                yield self._buffer[self._get_index(i)]
    
    def __getitem__(self, key) -> T:
        """
        索引访问或切片
        
        Args:
            key: 整数索引或切片对象
        
        Returns:
            元素或元素列表
        
        Raises:
            IndexError: 索引越界
            TypeError: 键类型不支持
        """
        with self._sync():
            if isinstance(key, int):
                if key < 0:
                    key = self._size + key
                if key < 0 or key >= self._size:
                    raise IndexError(f"索引 {key} 越界（队列大小: {self._size}）")
                return self._buffer[self._get_index(key)]
            
            elif isinstance(key, slice):
                indices = range(*key.indices(self._size))
                return [self._buffer[self._get_index(i)] for i in indices]
            
            else:
                raise TypeError(f"不支持的键类型: {type(key)}")
    
    def __contains__(self, item: T) -> bool:
        """检查元素是否在队列中"""
        with self._sync():
            for i in range(self._size):
                if self._buffer[self._get_index(i)] == item:
                    return True
            return False
    
    def count(self, item: T) -> int:
        """
        统计元素出现次数
        
        Args:
            item: 要统计的元素
        
        Returns:
            出现次数
        """
        with self._sync():
            result = 0
            for i in range(self._size):
                if self._buffer[self._get_index(i)] == item:
                    result += 1
            return result
    
    def index(self, item: T, start: int = 0, stop: Optional[int] = None) -> int:
        """
        查找元素首次出现的位置
        
        Args:
            item: 要查找的元素
            start: 起始位置
            stop: 结束位置
        
        Returns:
            元素位置
        
        Raises:
            ValueError: 元素不存在
        """
        with self._sync():
            if stop is None:
                stop = self._size
            
            for i in range(max(0, start), min(stop, self._size)):
                if self._buffer[self._get_index(i)] == item:
                    return i
            
            raise ValueError(f"元素 {item} 不在队列中")
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
        查找第一个满足条件的元素
        
        Args:
            predicate: 条件函数
        
        Returns:
            找到的元素，未找到返回 None
        """
        with self._sync():
            for i in range(self._size):
                item = self._buffer[self._get_index(i)]
                if predicate(item):
                    return item
            return None
    
    def find_all(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        查找所有满足条件的元素
        
        Args:
            predicate: 条件函数
        
        Returns:
            满足条件的元素列表
        """
        with self._sync():
            result = []
            for i in range(self._size):
                item = self._buffer[self._get_index(i)]
                if predicate(item):
                    result.append(item)
            return result
    
    def map(self, func: Callable[[T], Any]) -> List[Any]:
        """
        对队列中每个元素应用函数
        
        Args:
            func: 转换函数
        
        Returns:
            转换后的列表
        """
        with self._sync():
            return [func(self._buffer[self._get_index(i)]) for i in range(self._size)]
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        过滤队列中的元素
        
        Args:
            predicate: 过滤条件
        
        Returns:
            过滤后的列表
        """
        return self.find_all(predicate)
    
    def reduce(self, func: Callable[[Any, T], Any], initial: Any = None) -> Any:
        """
        归约操作
        
        Args:
            func: 归约函数 (accumulator, item) -> new_accumulator
            initial: 初始值
        
        Returns:
            归约结果
        """
        with self._sync():
            if self.is_empty:
                return initial
            
            iterator = iter(self)
            
            if initial is None:
                result = next(iterator)
            else:
                result = initial
            
            for item in iterator:
                result = func(result, item)
            
            return result
    
    # ==================== 统计信息 ====================
    
    @property
    def stats(self) -> dict:
        """
        获取队列统计信息
        
        Returns:
            包含统计信息的字典
        """
        with self._sync():
            return {
                'capacity': self._capacity,
                'size': self._size,
                'free_slots': self._capacity - self._size,
                'is_empty': self.is_empty,
                'is_full': self.is_full,
                'overwrite_enabled': self._overwrite,
                'thread_safe': self._thread_safe,
                'total_enqueued': self._total_enqueued,
                'total_dequeued': self._total_dequeued,
                'total_overwritten': self._total_overwritten,
                'utilization': self._size / self._capacity if self._capacity > 0 else 0
            }
    
    # ==================== 线程安全的阻塞操作 ====================
    
    def blocking_enqueue(self, item: T, timeout: Optional[float] = None) -> bool:
        """
        阻塞入队（仅在启用线程安全时可用）
        
        如果队列已满，等待直到有空间或超时。
        
        Args:
            item: 要入队的元素
            timeout: 超时时间（秒），None 表示无限等待
        
        Returns:
            是否成功入队
        
        Raises:
            RuntimeError: 未启用线程安全模式
        """
        if not self._thread_safe:
            raise RuntimeError("阻塞操作需要启用线程安全模式（thread_safe=True）")
        
        with self._not_full:
            if not self._not_full.wait_for(
                lambda: not self.is_full or self._overwrite,
                timeout=timeout
            ):
                return False
            
            self.enqueue(item)
            return True
    
    def blocking_dequeue(self, timeout: Optional[float] = None) -> Optional[T]:
        """
        阻塞出队（仅在启用线程安全时可用）
        
        如果队列为空，等待直到有元素或超时。
        
        Args:
            timeout: 超时时间（秒），None 表示无限等待
        
        Returns:
            出队的元素，超时返回 None
        
        Raises:
            RuntimeError: 未启用线程安全模式
        """
        if not self._thread_safe:
            raise RuntimeError("阻塞操作需要启用线程安全模式（thread_safe=True）")
        
        with self._not_empty:
            if not self._not_empty.wait_for(lambda: not self.is_empty, timeout=timeout):
                return None
            
            return self.dequeue()
    
    # ==================== 特殊方法 ====================
    
    def __repr__(self) -> str:
        """字符串表示"""
        return (
            f"CircularQueue(capacity={self._capacity}, "
            f"size={self._size}, "
            f"overwrite={self._overwrite}, "
            f"thread_safe={self._thread_safe})"
        )
    
    def __str__(self) -> str:
        """可读字符串表示"""
        items = self.to_list()
        preview = ', '.join(repr(item) for item in items[:5])
        if len(items) > 5:
            preview += ', ...'
        return f"[{preview}]"
    
    def __len__(self) -> int:
        """队列当前元素数量"""
        return self._size
    
    def __bool__(self) -> bool:
        """队列非空时返回 True"""
        return self._size > 0


# ==================== 便捷函数 ====================

def create_queue(
    capacity: int, 
    items: Optional[Iterable] = None,
    overwrite: bool = False,
    thread_safe: bool = False
) -> CircularQueue:
    """
    创建循环队列的便捷函数
    
    Args:
        capacity: 队列容量
        items: 初始元素
        overwrite: 是否启用自动覆盖
        thread_safe: 是否启用线程安全
    
    Returns:
        初始化后的 CircularQueue 实例
    
    Example:
        >>> queue = create_queue(5, [1, 2, 3])
        >>> len(queue)
        3
    """
    queue = CircularQueue(capacity, overwrite=overwrite, thread_safe=thread_safe)
    if items:
        queue.extend(items)
    return queue


def sliding_window(
    iterable: Iterable, 
    window_size: int
) -> Iterator[List]:
    """
    滑动窗口迭代器
    
    使用循环队列高效实现滑动窗口。
    
    Args:
        iterable: 输入可迭代对象
        window_size: 窗口大小
    
    Yields:
        每个窗口的元素列表
    
    Example:
        >>> list(sliding_window([1, 2, 3, 4, 5], 3))
        [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    """
    if window_size <= 0:
        raise ValueError(f"窗口大小必须大于 0，收到: {window_size}")
    
    queue = CircularQueue(window_size, overwrite=True)
    iterator = iter(iterable)
    
    # 填充第一个窗口
    for _ in range(window_size):
        try:
            queue.enqueue(next(iterator))
        except StopIteration:
            return
    
    yield queue.to_list()
    
    # 滑动窗口
    for item in iterator:
        queue.enqueue(item)
        yield queue.to_list()


def recent_buffer(
    capacity: int
) -> CircularQueue:
    """
    创建用于保存最近元素的缓冲区
    
    这是创建 overwrite=True 的循环队列的便捷方法。
    
    Args:
        capacity: 缓冲区容量
    
    Returns:
        配置为自动覆盖的 CircularQueue 实例
    
    Example:
        >>> buffer = recent_buffer(100)  # 保存最近 100 个元素
    """
    return CircularQueue(capacity, overwrite=True)


if __name__ == "__main__":
    # 简单演示
    print("=== Circular Queue 演示 ===\n")
    
    # 基本操作
    queue = CircularQueue[int](capacity=5)
    queue.enqueue(1, 2, 3)
    print(f"入队 1, 2, 3: {queue}")
    print(f"出队: {queue.dequeue()}")
    print(f"队首: {queue.peek()}")
    print(f"队尾: {queue.peek_last()}")
    
    # 自动覆盖模式
    print("\n=== 自动覆盖模式 ===")
    buffer = CircularQueue[str](capacity=3, overwrite=True)
    buffer.enqueue("a", "b", "c")
    print(f"初始: {buffer.to_list()}")
    buffer.enqueue("d", "e")
    print(f"添加 d, e 后: {buffer.to_list()}")
    print(f"统计: {buffer.stats}")
    
    # 滑动窗口
    print("\n=== 滑动窗口 ===")
    data = [1, 2, 3, 4, 5]
    windows = list(sliding_window(data, 3))
    print(f"数据: {data}")
    print(f"窗口大小 3: {windows}")