"""
Leaky Bucket Algorithm - 漏桶算法

漏桶算法以恒定速率处理请求，平滑突发流量。
适用于需要恒定输出速率的场景，如网络流量整形。

工作原理：
1. 请求作为水滴进入桶中
2. 桶以恒定速率漏水（处理请求）
3. 如果桶满了，新请求被拒绝
4. 请求按先进先出顺序处理

与令牌桶的区别：
- 令牌桶：允许突发流量（令牌可以累积）
- 漏桶：恒定输出速率，不允许突发
"""

import time
import threading
from dataclasses import dataclass, field
from typing import Optional, Callable, Tuple
from collections import deque


@dataclass
class LeakyBucketState:
    """漏桶状态快照"""
    current_level: int  # 当前水量（请求数）
    capacity: int  # 桶容量
    rate: float  # 漏水速率 (requests/second)
    last_leak: float  # 上次漏水时间戳


class LeakyBucket:
    """
    漏桶速率限制器

    特点：
    - 恒定处理速率
    - 平滑突发流量
    - 线程安全
    - 请求排队等待

    示例:
        # 每秒处理5个请求，桶容量10
        bucket = LeakyBucket(rate=5, capacity=10)

        if bucket.try_add():
            # 请求进入队列等待处理
            pass
        else:
            # 拒绝请求
            pass
    """

    def __init__(
        self,
        rate: float,
        capacity: int,
        time_func: Optional[Callable[[], float]] = None
    ):
        """
        初始化漏桶

        Args:
            rate: 漏水速率 (requests/second)
            capacity: 桶的最大容量
            time_func: 时间函数，用于测试注入
        """
        if rate <= 0:
            raise ValueError("rate must be positive")
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self._rate = rate
        self._capacity = capacity
        self._current_level = 0
        self._last_leak = time_func() if time_func else time.time()
        self._time_func = time_func or time.time
        self._lock = threading.Lock()

    def _leak(self) -> None:
        """根据时间流逝漏水"""
        now = self._time_func()
        elapsed = now - self._last_leak

        if elapsed > 0:
            # 计算应该漏掉的数量
            leaked = int(elapsed * self._rate)
            if leaked > 0:
                self._current_level = max(0, self._current_level - leaked)
                self._last_leak = now

    def try_add(self, count: int = 1) -> bool:
        """
        尝试向桶中添加请求

        Args:
            count: 要添加的请求数

        Returns:
            True 如果成功添加，False 如果桶已满
        """
        with self._lock:
            self._leak()

            if self._current_level + count <= self._capacity:
                self._current_level += count
                return True
            return False

    def add_or_wait(self, count: int = 1, max_wait: Optional[float] = None) -> float:
        """
        等待直到可以添加请求，或超时

        Args:
            count: 要添加的请求数
            max_wait: 最大等待时间（秒），None 表示无限等待

        Returns:
            实际等待的时间（秒）

        Raises:
            TimeoutError: 如果超过最大等待时间
        """
        start_time = self._time_func()

        while True:
            with self._lock:
                self._leak()

                if self._current_level + count <= self._capacity:
                    self._current_level += count
                    return self._time_func() - start_time

            if max_wait is not None:
                elapsed = self._time_func() - start_time
                if elapsed >= max_wait:
                    raise TimeoutError("rate limit wait timeout")

            # 计算需要等待的时间
            with self._lock:
                overflow = (self._current_level + count) - self._capacity
                if overflow > 0:
                    wait_time = overflow / self._rate
                else:
                    wait_time = 0.1

            time.sleep(min(wait_time, 0.1))

    def try_add_with_wait_time(self, count: int = 1) -> Tuple[bool, float]:
        """
        尝试添加请求，返回等待时间建议

        Args:
            count: 要添加的请求数

        Returns:
            (是否成功, 如果失败需要等待的时间)
        """
        with self._lock:
            self._leak()

            if self._current_level + count <= self._capacity:
                self._current_level += count
                return True, 0.0
            else:
                overflow = (self._current_level + count) - self._capacity
                wait_time = overflow / self._rate if self._rate > 0 else float('inf')
                return False, wait_time

    def get_level(self) -> int:
        """获取当前水量（排队请求数）"""
        with self._lock:
            self._leak()
            return self._current_level

    def get_available_capacity(self) -> int:
        """获取剩余容量"""
        with self._lock:
            self._leak()
            return self._capacity - self._current_level

    def get_wait_time(self, count: int = 1) -> float:
        """
        获取添加指定数量请求所需的等待时间

        Args:
            count: 要添加的请求数

        Returns:
            等待时间（秒）
        """
        with self._lock:
            self._leak()
            if self._current_level + count <= self._capacity:
                return 0.0
            overflow = (self._current_level + count) - self._capacity
            return overflow / self._rate if self._rate > 0 else float('inf')

    def get_state(self) -> LeakyBucketState:
        """获取当前状态快照"""
        with self._lock:
            self._leak()
            return LeakyBucketState(
                current_level=self._current_level,
                capacity=self._capacity,
                rate=self._rate,
                last_leak=self._last_leak
            )

    @property
    def rate(self) -> float:
        """漏水速率"""
        return self._rate

    @property
    def capacity(self) -> int:
        """桶容量"""
        return self._capacity

    def reset(self) -> None:
        """重置漏桶"""
        with self._lock:
            self._current_level = 0
            self._last_leak = self._time_func()

    def __repr__(self) -> str:
        return f"LeakyBucket(rate={self._rate}, capacity={self._capacity}, level={self.get_level()})"


class LeakyBucketQueue:
    """
    带队列的漏桶实现

    将请求存入队列，按恒定速率处理。
    支持请求优先级和超时。
    """

    def __init__(
        self,
        rate: float,
        capacity: int,
        time_func: Optional[Callable[[], float]] = None
    ):
        if rate <= 0:
            raise ValueError("rate must be positive")
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self._rate = rate
        self._capacity = capacity
        self._queue = deque()
        self._last_process = time_func() if time_func else time.time()
        self._time_func = time_func or time.time
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)

    def _get_process_time(self) -> float:
        """获取处理一个请求需要的时间"""
        return 1.0 / self._rate if self._rate > 0 else 0

    def try_enqueue(self, item: any, timeout: float = 0) -> bool:
        """
        尝试将请求加入队列

        Args:
            item: 请求内容
            timeout: 等待超时时间（秒），0 表示不等待

        Returns:
            True 如果成功加入队列
        """
        start_time = self._time_func()

        while True:
            with self._condition:
                if len(self._queue) < self._capacity:
                    self._queue.append({
                        'item': item,
                        'enqueue_time': self._time_func()
                    })
                    self._condition.notify()
                    return True

                if timeout == 0:
                    return False

                elapsed = self._time_func() - start_time
                if timeout > 0 and elapsed >= timeout:
                    return False

                wait_time = min(0.1, timeout - elapsed if timeout > 0 else 0.1)
                self._condition.wait(wait_time)

    def dequeue(self, timeout: Optional[float] = None) -> Optional[any]:
        """
        从队列获取下一个请求（阻塞）

        Args:
            timeout: 等待超时时间（秒），None 表示无限等待

        Returns:
            请求内容，如果超时返回 None
        """
        process_interval = self._get_process_time()

        with self._condition:
            while True:
                if self._queue:
                    now = self._time_func()
                    # 确保按速率处理
                    elapsed = now - self._last_process
                    if elapsed < process_interval:
                        wait_needed = process_interval - elapsed
                        if timeout is not None:
                            if wait_needed > timeout:
                                return None
                            timeout -= wait_needed
                        self._condition.wait(wait_needed)

                    entry = self._queue.popleft()
                    self._last_process = self._time_func()
                    return entry['item']

                if timeout == 0:
                    return None

                if timeout is not None:
                    if timeout <= 0:
                        return None
                    self._condition.wait(min(timeout, 0.1))
                    timeout -= 0.1
                else:
                    self._condition.wait(0.1)

    @property
    def queue_size(self) -> int:
        """当前队列大小"""
        with self._lock:
            return len(self._queue)

    @property
    def capacity(self) -> int:
        """队列容量"""
        return self._capacity

    @property
    def rate(self) -> float:
        """处理速率"""
        return self._rate

    def clear(self) -> None:
        """清空队列"""
        with self._condition:
            self._queue.clear()
            self._condition.notify_all()