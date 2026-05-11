"""
Fixed Window Algorithm - 固定窗口算法

固定窗口算法是最简单的限流算法，按固定时间窗口计数。
实现简单，内存使用少，但存在边界突发问题。

工作原理：
1. 将时间划分为固定大小的窗口
2. 每个窗口独立计数
3. 窗口内请求数超过限制则拒绝
4. 新窗口重置计数

边界突发问题：
- 窗口边界前一刻和后一刻都可能接近限制
- 实际可能达到 2 倍限制
"""

import time
import threading
from dataclasses import dataclass
from typing import Optional, Callable, Tuple
from enum import Enum


class WindowUnit(Enum):
    """窗口时间单位"""
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400


@dataclass
class FixedWindowState:
    """固定窗口状态快照"""
    request_count: int  # 当前窗口内请求数
    limit: int  # 窗口内最大请求数
    window_size: float  # 窗口大小（秒）
    window_start: float  # 当前窗口开始时间
    window_end: float  # 当前窗口结束时间


class FixedWindow:
    """
    固定窗口速率限制器

    特点：
    - 实现简单
    - 内存占用小
    - 存在边界突发问题
    - 线程安全

    示例:
        # 每分钟最多60个请求
        window = FixedWindow(limit=60, window_size=60)

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
        unit: Optional[WindowUnit] = None,
        time_func: Optional[Callable[[], float]] = None
    ):
        """
        初始化固定窗口

        Args:
            limit: 窗口内允许的最大请求数
            window_size: 窗口大小（秒），如果指定 unit 则忽略此参数
            unit: 窗口时间单位（可选）
            time_func: 时间函数，用于测试注入
        """
        if limit <= 0:
            raise ValueError("limit must be positive")

        if unit is not None:
            self._window_size = unit.value
        else:
            if window_size <= 0:
                raise ValueError("window_size must be positive")
            self._window_size = window_size

        self._limit = limit
        self._count = 0
        self._window_start = 0.0
        self._time_func = time_func or time.time
        self._lock = threading.Lock()

    def _get_window_start(self, timestamp: float) -> float:
        """获取时间戳所在窗口的开始时间"""
        return int(timestamp / self._window_size) * self._window_size

    def _check_and_reset(self) -> None:
        """检查是否需要重置窗口"""
        now = self._time_func()
        current_window_start = self._get_window_start(now)

        if current_window_start != self._window_start:
            self._window_start = current_window_start
            self._count = 0

    def try_acquire(self, count: int = 1) -> bool:
        """
        尝试获取许可

        Args:
            count: 请求的许可数量

        Returns:
            True 如果成功获取，False 如果超过限制
        """
        with self._lock:
            self._check_and_reset()

            if self._count + count <= self._limit:
                self._count += count
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
                self._check_and_reset()

                if self._count + count <= self._limit:
                    self._count += count
                    return self._time_func() - start_time

            if max_wait is not None:
                elapsed = self._time_func() - start_time
                if elapsed >= max_wait:
                    raise TimeoutError("rate limit wait timeout")

            # 计算到下一个窗口的时间
            with self._lock:
                now = self._time_func()
                next_window = self._window_start + self._window_size
                wait_time = max(0.01, min(next_window - now, 0.1))

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
            self._check_and_reset()

            if self._count + count <= self._limit:
                self._count += count
                return True, 0.0
            else:
                now = self._time_func()
                next_window = self._window_start + self._window_size
                wait_time = next_window - now
                return False, max(0, wait_time)

    def get_count(self) -> int:
        """获取当前窗口内的请求数"""
        with self._lock:
            self._check_and_reset()
            return self._count

    def get_remaining(self) -> int:
        """获取剩余配额"""
        with self._lock:
            self._check_and_reset()
            return self._limit - self._count

    def get_wait_time(self) -> float:
        """获取到下一个窗口的等待时间"""
        with self._lock:
            self._check_and_reset()
            now = self._time_func()
            next_window = self._window_start + self._window_size
            return max(0, next_window - now)

    def get_state(self) -> FixedWindowState:
        """获取当前状态快照"""
        with self._lock:
            self._check_and_reset()
            now = self._time_func()
            return FixedWindowState(
                request_count=self._count,
                limit=self._limit,
                window_size=self._window_size,
                window_start=self._window_start,
                window_end=self._window_start + self._window_size
            )

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
            self._count = 0
            self._window_start = 0.0

    def __repr__(self) -> str:
        state = self.get_state()
        return f"FixedWindow(limit={self._limit}, window={self._window_size}s, count={state.request_count})"


class FixedWindowKeyed:
    """
    多键固定窗口速率限制器

    支持对不同的键进行独立的限流。
    适用于多用户、多IP等场景。

    示例:
        # 每个IP每分钟最多100个请求
        limiter = FixedWindowKeyed(limit=100, window_size=60)

        if limiter.try_acquire('192.168.1.1'):
            # 处理请求
            pass
    """

    def __init__(
        self,
        limit: int,
        window_size: float,
        max_keys: int = 10000,
        time_func: Optional[Callable[[], float]] = None
    ):
        """
        初始化多键固定窗口

        Args:
            limit: 每个键窗口内允许的最大请求数
            window_size: 窗口大小（秒）
            max_keys: 最大键数量，超过后清理最旧的键
            time_func: 时间函数，用于测试注入
        """
        if limit <= 0:
            raise ValueError("limit must be positive")
        if window_size <= 0:
            raise ValueError("window_size must be positive")

        self._limit = limit
        self._window_size = window_size
        self._max_keys = max_keys
        self._windows = {}  # key -> (count, window_start)
        self._time_func = time_func or time.time
        self._lock = threading.Lock()

    def _get_window_start(self, timestamp: float) -> float:
        """获取时间戳所在窗口的开始时间"""
        return int(timestamp / self._window_size) * self._window_size

    def _cleanup(self) -> None:
        """清理过期的键"""
        if len(self._windows) <= self._max_keys:
            return

        now = self._time_func()
        cutoff = now - self._window_size * 2

        keys_to_remove = [
            k for k, (_, start) in self._windows.items()
            if start < cutoff
        ]

        for key in keys_to_remove:
            del self._windows[key]

    def try_acquire(self, key: str, count: int = 1) -> bool:
        """
        尝试获取指定键的许可

        Args:
            key: 键名
            count: 请求的许可数量

        Returns:
            True 如果成功获取，False 如果超过限制
        """
        with self._lock:
            now = self._time_func()
            current_window_start = self._get_window_start(now)

            if key not in self._windows:
                self._windows[key] = (count, current_window_start)
                self._cleanup()
                return True

            count_key, window_start = self._windows[key]

            if window_start != current_window_start:
                # 新窗口
                self._windows[key] = (count, current_window_start)
                self._cleanup()
                return True

            if count_key + count <= self._limit:
                self._windows[key] = (count_key + count, window_start)
                return True

            return False

    def get_count(self, key: str) -> int:
        """获取指定键当前窗口内的请求数"""
        with self._lock:
            now = self._time_func()
            current_window_start = self._get_window_start(now)

            if key not in self._windows:
                return 0

            count, window_start = self._windows[key]
            if window_start != current_window_start:
                return 0

            return count

    def get_remaining(self, key: str) -> int:
        """获取指定键的剩余配额"""
        return self._limit - self.get_count(key)

    def reset(self, key: Optional[str] = None) -> None:
        """
        重置计数器

        Args:
            key: 要重置的键，None 表示重置所有
        """
        with self._lock:
            if key is None:
                self._windows.clear()
            elif key in self._windows:
                del self._windows[key]

    def keys(self) -> list:
        """获取所有活跃键"""
        with self._lock:
            now = self._time_func()
            current_window_start = self._get_window_start(now)

            return [
                k for k, (_, start) in self._windows.items()
                if start == current_window_start
            ]

    @property
    def limit(self) -> int:
        """窗口内最大请求数"""
        return self._limit

    @property
    def window_size(self) -> float:
        """窗口大小"""
        return self._window_size

    def __repr__(self) -> str:
        return f"FixedWindowKeyed(limit={self._limit}, window={self._window_size}s, keys={len(self.keys())})"