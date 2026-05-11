"""
Token Bucket Algorithm - 令牌桶算法

令牌桶算法允许一定程度的突发流量，同时限制平均速率。
适用于需要处理突发流量的场景，如 API 限流、网络流量控制。

工作原理：
1. 以固定速率向桶中添加令牌
2. 每个请求消耗一个令牌
3. 如果桶中没有令牌，请求被拒绝
4. 桶有最大容量，令牌数量不会超过容量
"""

import time
import threading
from dataclasses import dataclass
from typing import Optional, Callable, Tuple


@dataclass
class TokenBucketState:
    """令牌桶状态快照"""
    tokens: float  # 当前令牌数
    capacity: float  # 桶容量
    rate: float  # 令牌产生速率 (tokens/second)
    last_update: float  # 上次更新时间戳


class TokenBucket:
    """
    令牌桶速率限制器

    特点：
    - 允许突发流量（最多桶容量）
    - 平滑限流
    - 线程安全

    示例:
        # 每秒10个请求，桶容量20
        bucket = TokenBucket(rate=10, capacity=20)

        if bucket.consume():
            # 处理请求
            pass
        else:
            # 拒绝请求
            pass
    """

    def __init__(
        self,
        rate: float,
        capacity: float,
        initial_tokens: Optional[float] = None,
        time_func: Optional[Callable[[], float]] = None
    ):
        """
        初始化令牌桶

        Args:
            rate: 令牌产生速率 (tokens/second)
            capacity: 桶的最大容量
            initial_tokens: 初始令牌数，默认为满桶
            time_func: 时间函数，用于测试注入
        """
        if rate <= 0:
            raise ValueError("rate must be positive")
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self._rate = rate
        self._capacity = capacity
        self._tokens = initial_tokens if initial_tokens is not None else capacity
        self._last_update = time_func() if time_func else time.time()
        self._time_func = time_func or time.time
        self._lock = threading.Lock()

    def _refill(self) -> None:
        """根据时间流逝补充令牌"""
        now = self._time_func()
        elapsed = now - self._last_update

        if elapsed > 0:
            new_tokens = elapsed * self._rate
            self._tokens = min(self._capacity, self._tokens + new_tokens)
            self._last_update = now

    def consume(self, tokens: float = 1.0) -> bool:
        """
        尝试消耗令牌

        Args:
            tokens: 要消耗的令牌数

        Returns:
            True 如果成功消耗，False 如果令牌不足
        """
        with self._lock:
            self._refill()

            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    def consume_or_wait(self, tokens: float = 1.0, max_wait: Optional[float] = None) -> float:
        """
        等待直到可以消耗令牌，或超时

        Args:
            tokens: 要消耗的令牌数
            max_wait: 最大等待时间（秒），None 表示无限等待

        Returns:
            实际等待的时间（秒）

        Raises:
            TimeoutError: 如果超过最大等待时间
        """
        start_time = self._time_func()

        while True:
            with self._lock:
                self._refill()

                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return self._time_func() - start_time

            if max_wait is not None:
                elapsed = self._time_func() - start_time
                if elapsed >= max_wait:
                    raise TimeoutError("rate limit wait timeout")

            # 计算需要等待的时间
            with self._lock:
                deficit = tokens - self._tokens
                wait_time = deficit / self._rate if self._rate > 0 else 1.0

            time.sleep(min(wait_time, 0.1))  # 分段等待，避免长时间阻塞

    def try_consume(self, tokens: float = 1.0) -> Tuple[bool, float]:
        """
        尝试消耗令牌，返回等待时间建议

        Args:
            tokens: 要消耗的令牌数

        Returns:
            (是否成功, 如果失败需要等待的时间)
        """
        with self._lock:
            self._refill()

            if self._tokens >= tokens:
                self._tokens -= tokens
                return True, 0.0
            else:
                deficit = tokens - self._tokens
                wait_time = deficit / self._rate if self._rate > 0 else float('inf')
                return False, wait_time

    def get_tokens(self) -> float:
        """获取当前可用令牌数"""
        with self._lock:
            self._refill()
            return self._tokens

    def get_wait_time(self, tokens: float = 1.0) -> float:
        """
        获取等待指定令牌数所需的时间

        Args:
            tokens: 需要的令牌数

        Returns:
            等待时间（秒）
        """
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                return 0.0
            deficit = tokens - self._tokens
            return deficit / self._rate if self._rate > 0 else float('inf')

    def get_state(self) -> TokenBucketState:
        """获取当前状态快照"""
        with self._lock:
            self._refill()
            return TokenBucketState(
                tokens=self._tokens,
                capacity=self._capacity,
                rate=self._rate,
                last_update=self._last_update
            )

    @property
    def rate(self) -> float:
        """令牌产生速率"""
        return self._rate

    @property
    def capacity(self) -> float:
        """桶容量"""
        return self._capacity

    def reset(self, tokens: Optional[float] = None) -> None:
        """
        重置令牌桶

        Args:
            tokens: 重置后的令牌数，默认为满桶
        """
        with self._lock:
            self._tokens = tokens if tokens is not None else self._capacity
            self._last_update = self._time_func()

    def __repr__(self) -> str:
        return f"TokenBucket(rate={self._rate}, capacity={self._capacity}, tokens={self.get_tokens():.2f})"


class AsyncTokenBucket:
    """
    异步令牌桶速率限制器

    适用于异步代码环境
    """

    def __init__(
        self,
        rate: float,
        capacity: float,
        initial_tokens: Optional[float] = None
    ):
        if rate <= 0:
            raise ValueError("rate must be positive")
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self._rate = rate
        self._capacity = capacity
        self._tokens = initial_tokens if initial_tokens is not None else capacity
        self._last_update = time.time()
        import asyncio
        self._lock = asyncio.Lock()

    async def _refill(self) -> None:
        """补充令牌"""
        now = time.time()
        elapsed = now - self._last_update

        if elapsed > 0:
            new_tokens = elapsed * self._rate
            self._tokens = min(self._capacity, self._tokens + new_tokens)
            self._last_update = now

    async def consume(self, tokens: float = 1.0) -> bool:
        """尝试消耗令牌"""
        async with self._lock:
            await self._refill()

            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    async def consume_or_wait(self, tokens: float = 1.0, max_wait: Optional[float] = None) -> float:
        """等待直到可以消耗令牌"""
        import asyncio
        start_time = time.time()

        while True:
            async with self._lock:
                await self._refill()

                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return time.time() - start_time

            if max_wait is not None:
                elapsed = time.time() - start_time
                if elapsed >= max_wait:
                    raise TimeoutError("rate limit wait timeout")

            await asyncio.sleep(0.01)