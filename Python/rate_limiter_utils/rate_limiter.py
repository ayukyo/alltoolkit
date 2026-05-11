"""
Rate Limiter - 统一速率限制器接口

提供统一的限流器接口，支持多种算法切换。
适用于需要灵活选择限流策略的场景。
"""

import time
import threading
from typing import Optional, Callable, Dict, Any, Tuple
from enum import Enum

from .token_bucket import TokenBucket
from .leaky_bucket import LeakyBucket
from .sliding_window import SlidingWindow, SlidingWindowCounter
from .fixed_window import FixedWindow, FixedWindowKeyed


class Algorithm(Enum):
    """限流算法类型"""
    TOKEN_BUCKET = "token_bucket"
    LEAKY_BUCKET = "leaky_bucket"
    SLIDING_WINDOW = "sliding_window"
    SLIDING_WINDOW_COUNTER = "sliding_window_counter"
    FIXED_WINDOW = "fixed_window"


class RateLimiter:
    """
    统一速率限制器

    提供多种限流算法的统一接口，方便切换和比较。

    示例:
        # 使用令牌桶算法
        limiter = RateLimiter(
            algorithm=Algorithm.TOKEN_BUCKET,
            rate=10,  # 10 requests/second
            capacity=20  # burst capacity
        )

        # 使用滑动窗口算法
        limiter = RateLimiter(
            algorithm=Algorithm.SLIDING_WINDOW,
            limit=100,  # 100 requests
            window_size=60  # per 60 seconds
        )

        if limiter.try_acquire():
            # 处理请求
            pass
    """

    def __init__(
        self,
        algorithm: Algorithm = Algorithm.TOKEN_BUCKET,
        rate: Optional[float] = None,
        capacity: Optional[int] = None,
        limit: Optional[int] = None,
        window_size: Optional[float] = None,
        sub_windows: int = 10,
        time_func: Optional[Callable[[], float]] = None
    ):
        """
        初始化速率限制器

        Args:
            algorithm: 限流算法
            rate: 速率 (requests/second)，用于令牌桶和漏桶
            capacity: 容量，用于令牌桶和漏桶
            limit: 窗口内最大请求数，用于窗口算法
            window_size: 窗口大小（秒），用于窗口算法
            sub_windows: 子窗口数量，用于滑动窗口计数器
            time_func: 时间函数，用于测试注入
        """
        self._algorithm = algorithm
        self._time_func = time_func or time.time

        if algorithm == Algorithm.TOKEN_BUCKET:
            if rate is None:
                rate = 10.0
            if capacity is None:
                capacity = int(rate * 2)
            self._limiter = TokenBucket(
                rate=rate,
                capacity=capacity,
                time_func=time_func
            )

        elif algorithm == Algorithm.LEAKY_BUCKET:
            if rate is None:
                rate = 10.0
            if capacity is None:
                capacity = int(rate * 2)
            self._limiter = LeakyBucket(
                rate=rate,
                capacity=capacity,
                time_func=time_func
            )

        elif algorithm == Algorithm.SLIDING_WINDOW:
            if limit is None:
                limit = 100
            if window_size is None:
                window_size = 60.0
            self._limiter = SlidingWindow(
                limit=limit,
                window_size=window_size,
                time_func=time_func
            )

        elif algorithm == Algorithm.SLIDING_WINDOW_COUNTER:
            if limit is None:
                limit = 100
            if window_size is None:
                window_size = 60.0
            self._limiter = SlidingWindowCounter(
                limit=limit,
                window_size=window_size,
                sub_windows=sub_windows,
                time_func=time_func
            )

        elif algorithm == Algorithm.FIXED_WINDOW:
            if limit is None:
                limit = 100
            if window_size is None:
                window_size = 60.0
            self._limiter = FixedWindow(
                limit=limit,
                window_size=window_size,
                time_func=time_func
            )

        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    @property
    def algorithm(self) -> Algorithm:
        """当前算法"""
        return self._algorithm

    def try_acquire(self, count: int = 1) -> bool:
        """
        尝试获取许可

        Args:
            count: 请求的许可数量

        Returns:
            True 如果成功获取
        """
        if isinstance(self._limiter, TokenBucket):
            return self._limiter.consume(count)
        elif isinstance(self._limiter, LeakyBucket):
            return self._limiter.try_add(count)
        elif isinstance(self._limiter, (SlidingWindow, SlidingWindowCounter, FixedWindow)):
            return self._limiter.try_acquire(count)
        return False

    def acquire_or_wait(self, count: int = 1, max_wait: Optional[float] = None) -> float:
        """
        等待直到可以获取许可

        Args:
            count: 请求的许可数量
            max_wait: 最大等待时间（秒）

        Returns:
            实际等待的时间

        Raises:
            TimeoutError: 如果超时
        """
        if isinstance(self._limiter, TokenBucket):
            return self._limiter.consume_or_wait(count, max_wait)
        elif isinstance(self._limiter, LeakyBucket):
            return self._limiter.add_or_wait(count, max_wait)
        elif isinstance(self._limiter, (SlidingWindow, FixedWindow)):
            return self._limiter.acquire_or_wait(count, max_wait)
        elif isinstance(self._limiter, SlidingWindowCounter):
            # SlidingWindowCounter 没有这个方法，需要自己实现
            start_time = self._time_func()
            while True:
                if self._limiter.try_acquire(count):
                    return self._time_func() - start_time

                if max_wait is not None:
                    elapsed = self._time_func() - start_time
                    if elapsed >= max_wait:
                        raise TimeoutError("rate limit wait timeout")

                time.sleep(0.01)
        return 0.0

    def get_state(self) -> Dict[str, Any]:
        """
        获取当前状态

        Returns:
            包含算法类型和状态的字典
        """
        state = {
            'algorithm': self._algorithm.value
        }

        if isinstance(self._limiter, TokenBucket):
            tb_state = self._limiter.get_state()
            state.update({
                'tokens': tb_state.tokens,
                'capacity': tb_state.capacity,
                'rate': tb_state.rate
            })
        elif isinstance(self._limiter, LeakyBucket):
            lb_state = self._limiter.get_state()
            state.update({
                'level': lb_state.current_level,
                'capacity': lb_state.capacity,
                'rate': lb_state.rate
            })
        elif isinstance(self._limiter, (SlidingWindow, SlidingWindowCounter, FixedWindow)):
            state.update({
                'count': self._limiter.get_count(),
                'limit': self._limiter.limit,
                'window_size': self._limiter.window_size
            })

        return state

    def reset(self) -> None:
        """重置限流器"""
        self._limiter.reset()

    def __repr__(self) -> str:
        return f"RateLimiter(algorithm={self._algorithm.value})"


class MultiRateLimiter:
    """
    多层速率限制器

    支持同时应用多个限流规则，例如：
    - 每秒最多10个请求
    - 每分钟最多100个请求
    - 每小时最多1000个请求

    所有规则都必须满足才能通过。

    示例:
        limiter = MultiRateLimiter()
        limiter.add_limit('per_second', Algorithm.SLIDING_WINDOW, limit=10, window_size=1)
        limiter.add_limit('per_minute', Algorithm.SLIDING_WINDOW, limit=100, window_size=60)
        limiter.add_limit('per_hour', Algorithm.SLIDING_WINDOW, limit=1000, window_size=3600)

        if limiter.try_acquire():
            # 所有规则都满足
            pass
    """

    def __init__(self):
        """初始化多层速率限制器"""
        self._limiters: Dict[str, RateLimiter] = {}
        self._lock = threading.Lock()

    def add_limit(
        self,
        name: str,
        algorithm: Algorithm = Algorithm.SLIDING_WINDOW,
        **kwargs
    ) -> None:
        """
        添加限流规则

        Args:
            name: 规则名称
            algorithm: 算法类型
            **kwargs: 传递给 RateLimiter 的参数
        """
        with self._lock:
            self._limiters[name] = RateLimiter(algorithm=algorithm, **kwargs)

    def remove_limit(self, name: str) -> bool:
        """
        移除限流规则

        Args:
            name: 规则名称

        Returns:
            True 如果成功移除
        """
        with self._lock:
            if name in self._limiters:
                del self._limiters[name]
                return True
            return False

    def try_acquire(self, count: int = 1) -> Tuple[bool, Optional[str]]:
        """
        尝试获取许可

        Args:
            count: 请求的许可数量

        Returns:
            (是否成功, 失败的规则名称)
        """
        with self._lock:
            # 先检查所有规则
            for name, limiter in self._limiters.items():
                if not limiter.try_acquire(count):
                    return False, name

            # 所有规则都满足，实际消耗
            return True, None

    def try_acquire_atomic(self, count: int = 1) -> Tuple[bool, Optional[str]]:
        """
        原子性尝试获取许可

        如果任何规则不满足，不会消耗任何配额。

        Args:
            count: 请求的许可数量

        Returns:
            (是否成功, 失败的规则名称)
        """
        with self._lock:
            # 检查所有规则是否有足够配额
            failed_rule = None
            for name, limiter in self._limiters.items():
                state = limiter.get_state()
                # 简单检查：如果当前计数+count > limit，则失败
                if 'count' in state and state['count'] + count > state.get('limit', float('inf')):
                    failed_rule = name
                    break
                elif 'tokens' in state and state['tokens'] < count:
                    failed_rule = name
                    break
                elif 'level' in state and state['level'] + count > state.get('capacity', float('inf')):
                    failed_rule = name
                    break

            if failed_rule:
                return False, failed_rule

            # 所有规则都满足，实际消耗
            for limiter in self._limiters.values():
                limiter.try_acquire(count)

            return True, None

    def get_state(self) -> Dict[str, Dict[str, Any]]:
        """获取所有限流规则的状态"""
        with self._lock:
            return {name: limiter.get_state() for name, limiter in self._limiters.items()}

    def reset(self, name: Optional[str] = None) -> None:
        """
        重置限流器

        Args:
            name: 要重置的规则名称，None 表示重置所有
        """
        with self._lock:
            if name is None:
                for limiter in self._limiters.values():
                    limiter.reset()
            elif name in self._limiters:
                self._limiters[name].reset()

    @property
    def rules(self) -> list:
        """获取所有规则名称"""
        return list(self._limiters.keys())

    def __repr__(self) -> str:
        return f"MultiRateLimiter(rules={self.rules})"