"""
Sliding Window Algorithm - 滑动窗口算法

滑动窗口算法精确计算时间窗口内的请求数量，避免了固定窗口的边界问题。
适用于需要精确限流的场景。

工作原理：
1. 记录每个请求的时间戳
2. 计算窗口内请求数时，只统计窗口内的请求
3. 窗口随时间滑动，丢弃过期请求

与固定窗口的区别：
- 固定窗口：可能有边界突发（窗口边界前后都接近限制）
- 滑动窗口：精确控制，无边界问题
"""

import time
import threading
from dataclasses import dataclass, field
from typing import Optional, Callable, List, Tuple
from collections import deque


@dataclass
class SlidingWindowState:
    """滑动窗口状态快照"""
    request_count: int  # 当前窗口内请求数
    limit: int  # 窗口内最大请求数
    window_size: float  # 窗口大小（秒）
    oldest_request: Optional[float]  # 最旧请求时间戳


class SlidingWindow:
    """
    滑动窗口速率限制器

    特点：
    - 精确限流
    - 无边界突发问题
    - 线程安全
    - 自动清理过期记录

    示例:
        # 每秒最多10个请求
        window = SlidingWindow(limit=10, window_size=1.0)

        if window.try_acquire():
            # 处理请求
            pass
        else:
            # 拒绝请求
            pass
    """

    def __init__(
        self,
        limit: int,
        window_size: float,
        time_func: Optional[Callable[[], float]] = None
    ):
        """
        初始化滑动窗口

        Args:
            limit: 窗口内允许的最大请求数
            window_size: 窗口大小（秒）
            time_func: 时间函数，用于测试注入
        """
        if limit <= 0:
            raise ValueError("limit must be positive")
        if window_size <= 0:
            raise ValueError("window_size must be positive")

        self._limit = limit
        self._window_size = window_size
        self._requests = deque()
        self._time_func = time_func or time.time
        self._lock = threading.Lock()

    def _cleanup(self) -> None:
        """清理过期的请求记录"""
        now = self._time_func()
        cutoff = now - self._window_size

        while self._requests and self._requests[0] <= cutoff:
            self._requests.popleft()

    def try_acquire(self, count: int = 1) -> bool:
        """
        尝试获取许可

        Args:
            count: 请求的许可数量

        Returns:
            True 如果成功获取，False 如果超过限制
        """
        with self._lock:
            self._cleanup()

            if len(self._requests) + count <= self._limit:
                now = self._time_func()
                for _ in range(count):
                    self._requests.append(now)
                return True
            return False

    def acquire_or_wait(self, count: int = 1, max_wait: Optional[float] = None) -> float:
        """
        等待直到可以获取许可

        Args:
            count: 请求的许可数量
            max_wait: 最大等待时间（秒），None 表示无限等待

        Returns:
            实际等待的时间（秒）

        Raises:
            TimeoutError: 如果超过最大等待时间
        """
        start_time = self._time_func()

        while True:
            with self._lock:
                self._cleanup()

                if len(self._requests) + count <= self._limit:
                    now = self._time_func()
                    for _ in range(count):
                        self._requests.append(now)
                    return self._time_func() - start_time

            if max_wait is not None:
                elapsed = self._time_func() - start_time
                if elapsed >= max_wait:
                    raise TimeoutError("rate limit wait timeout")

            # 计算需要等待的时间
            with self._lock:
                self._cleanup()
                if self._requests:
                    oldest = self._requests[0]
                    wait_time = (oldest + self._window_size) - self._time_func()
                    wait_time = max(0.01, min(wait_time, 0.1))
                else:
                    wait_time = 0.01

            time.sleep(wait_time)

    def try_acquire_with_wait_time(self, count: int = 1) -> Tuple[bool, float]:
        """
        尝试获取许可，返回等待时间建议

        Args:
            count: 请求的许可数量

        Returns:
            (是否成功, 如果失败需要等待的时间)
        """
        with self._lock:
            self._cleanup()

            if len(self._requests) + count <= self._limit:
                now = self._time_func()
                for _ in range(count):
                    self._requests.append(now)
                return True, 0.0
            else:
                if self._requests:
                    oldest = self._requests[0]
                    wait_time = (oldest + self._window_size) - self._time_func()
                    return False, max(0, wait_time)
                return False, 0.0

    def get_count(self) -> int:
        """获取当前窗口内的请求数"""
        with self._lock:
            self._cleanup()
            return len(self._requests)

    def get_remaining(self) -> int:
        """获取剩余配额"""
        with self._lock:
            self._cleanup()
            return self._limit - len(self._requests)

    def get_wait_time(self, count: int = 1) -> float:
        """
        获取等待指定数量许可所需的时间

        Args:
            count: 需要的许可数量

        Returns:
            等待时间（秒）
        """
        with self._lock:
            self._cleanup()

            if len(self._requests) + count <= self._limit:
                return 0.0

            if not self._requests:
                return 0.0

            # 计算需要等待多少请求过期
            excess = len(self._requests) + count - self._limit
            if excess <= 0:
                return 0.0

            # 返回第 excess 个请求的剩余时间
            if excess <= len(self._requests):
                target_request = self._requests[excess - 1]
                wait_time = (target_request + self._window_size) - self._time_func()
                return max(0, wait_time)

            return self._window_size  # 需要等待整个窗口

    def get_state(self) -> SlidingWindowState:
        """获取当前状态快照"""
        with self._lock:
            self._cleanup()
            return SlidingWindowState(
                request_count=len(self._requests),
                limit=self._limit,
                window_size=self._window_size,
                oldest_request=self._requests[0] if self._requests else None
            )

    def get_timestamps(self) -> List[float]:
        """获取当前窗口内所有请求时间戳（用于调试）"""
        with self._lock:
            self._cleanup()
            return list(self._requests)

    @property
    def limit(self) -> int:
        """窗口内最大请求数"""
        return self._limit

    @property
    def window_size(self) -> float:
        """窗口大小"""
        return self._window_size

    def reset(self) -> None:
        """重置窗口"""
        with self._lock:
            self._requests.clear()

    def __repr__(self) -> str:
        return f"SlidingWindow(limit={self._limit}, window={self._window_size}s, count={self.get_count()})"


class SlidingWindowCounter:
    """
    滑动窗口计数器（优化内存版本）

    使用多个固定窗口近似滑动窗口，减少内存使用。
    适用于高并发场景。

    精度与内存权衡：
    - 子窗口越多，越精确，内存使用越大
    - 通常 10 个子窗口就足够精确
    """

    def __init__(
        self,
        limit: int,
        window_size: float,
        sub_windows: int = 10,
        time_func: Optional[Callable[[], float]] = None
    ):
        """
        初始化滑动窗口计数器

        Args:
            limit: 窗口内允许的最大请求数
            window_size: 窗口大小（秒）
            sub_windows: 子窗口数量
            time_func: 时间函数，用于测试注入
        """
        if limit <= 0:
            raise ValueError("limit must be positive")
        if window_size <= 0:
            raise ValueError("window_size must be positive")
        if sub_windows <= 0:
            raise ValueError("sub_windows must be positive")

        self._limit = limit
        self._window_size = window_size
        self._sub_window_size = window_size / sub_windows
        self._sub_windows = sub_windows
        self._counters = [0] * sub_windows
        self._timestamps = [0.0] * sub_windows
        self._time_func = time_func or time.time
        self._lock = threading.Lock()

    def _get_current_window(self) -> int:
        """获取当前子窗口索引"""
        now = self._time_func()
        return int(now / self._sub_window_size) % self._sub_windows

    def _cleanup(self) -> None:
        """清理过期的计数器"""
        now = self._time_func()
        current_window = self._get_current_window()

        for i in range(self._sub_windows):
            window_start = self._timestamps[i]
            if window_start > 0 and (now - window_start) > self._window_size:
                self._counters[i] = 0
                self._timestamps[i] = 0.0

    def _get_total_count(self) -> int:
        """获取当前窗口内的总请求数"""
        now = self._time_func()
        cutoff = now - self._window_size

        total = 0
        for i in range(self._sub_windows):
            if self._timestamps[i] > cutoff:
                total += self._counters[i]
        return total

    def try_acquire(self, count: int = 1) -> bool:
        """
        尝试获取许可

        Args:
            count: 请求的许可数量

        Returns:
            True 如果成功获取，False 如果超过限制
        """
        with self._lock:
            self._cleanup()
            total = self._get_total_count()

            if total + count <= self._limit:
                current_window = self._get_current_window()
                now = self._time_func()

                # 如果是新的子窗口，重置计数器
                if self._timestamps[current_window] == 0 or \
                   (now - self._timestamps[current_window]) >= self._sub_window_size:
                    self._counters[current_window] = 0
                    self._timestamps[current_window] = now

                self._counters[current_window] += count
                return True
            return False

    def get_count(self) -> int:
        """获取当前窗口内的请求数"""
        with self._lock:
            self._cleanup()
            return self._get_total_count()

    def get_remaining(self) -> int:
        """获取剩余配额"""
        with self._lock:
            self._cleanup()
            return max(0, self._limit - self._get_total_count())

    @property
    def limit(self) -> int:
        """窗口内最大请求数"""
        return self._limit

    @property
    def window_size(self) -> float:
        """窗口大小"""
        return self._window_size

    def reset(self) -> None:
        """重置计数器"""
        with self._lock:
            self._counters = [0] * self._sub_windows
            self._timestamps = [0.0] * self._sub_windows

    def __repr__(self) -> str:
        return f"SlidingWindowCounter(limit={self._limit}, window={self._window_size}s, count={self.get_count()})"