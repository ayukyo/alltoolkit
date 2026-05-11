"""
Rate Limit Decorators - 速率限制装饰器

提供便捷的装饰器方式应用速率限制。
适用于函数级别、类级别的限流。
"""

import time
import threading
import functools
from typing import Optional, Callable, Dict, Any, Union
from dataclasses import dataclass

from .rate_limiter import RateLimiter, MultiRateLimiter, Algorithm


class RateLimitExceeded(Exception):
    """速率限制超出异常"""
    pass


@dataclass
class RateLimitInfo:
    """速率限制信息"""
    limiter_name: str
    algorithm: str
    remaining: int
    limit: int
    wait_time: float


# 全局限流器注册表
_global_limiters: Dict[str, RateLimiter] = {}
_global_limiters_lock = threading.Lock()


def get_or_create_limiter(
    name: str,
    algorithm: Algorithm = Algorithm.TOKEN_BUCKET,
    **kwargs
) -> RateLimiter:
    """
    获取或创建命名的限流器

    Args:
        name: 限流器名称
        algorithm: 算法类型
        **kwargs: 限流器参数

    Returns:
        RateLimiter 实例
    """
    with _global_limiters_lock:
        if name not in _global_limiters:
            _global_limiters[name] = RateLimiter(algorithm=algorithm, **kwargs)
        return _global_limiters[name]


def rate_limit(
    name: Optional[str] = None,
    algorithm: Algorithm = Algorithm.TOKEN_BUCKET,
    rate: Optional[float] = None,
    capacity: Optional[int] = None,
    limit: Optional[int] = None,
    window_size: Optional[float] = None,
    raise_on_limit: bool = True,
    callback: Optional[Callable[[RateLimitInfo], None]] = None
):
    """
    速率限制装饰器

    Args:
        name: 限流器名称（共享相同名称的函数使用同一个限流器）
        algorithm: 限流算法
        rate: 速率 (requests/second)
        capacity: 容量（令牌桶/漏桶）
        limit: 窗口内最大请求数
        window_size: 窗口大小（秒）
        raise_on_limit: 是否在限流时抛出异常
        callback: 限流时的回调函数

    Returns:
        装饰器函数

    示例:
        @rate_limit(rate=10, capacity=20)
        def my_api():
            return "success"

        @rate_limit(name='shared_api', limit=100, window_size=60)
        def another_api():
            return "success"
    """
    def decorator(func: Callable) -> Callable:
        # 生成限流器名称
        limiter_name = name or f"_{func.__module__}_{func.__qualname__}"

        # 创建或获取限流器
        limiter = get_or_create_limiter(
            limiter_name,
            algorithm=algorithm,
            rate=rate,
            capacity=capacity,
            limit=limit,
            window_size=window_size
        )

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 尝试获取许可
            success, wait_time = limiter._limiter.try_acquire_with_wait_time(1) \
                if hasattr(limiter._limiter, 'try_acquire_with_wait_time') \
                else (limiter.try_acquire(1), 0)

            if success:
                return func(*args, **kwargs)

            # 限流
            state = limiter.get_state()
            info = RateLimitInfo(
                limiter_name=limiter_name,
                algorithm=state.get('algorithm', 'unknown'),
                remaining=state.get('limit', 0) - state.get('count', 0),
                limit=state.get('limit', 0),
                wait_time=wait_time
            )

            if callback:
                callback(info)

            if raise_on_limit:
                raise RateLimitExceeded(
                    f"Rate limit exceeded for '{limiter_name}'. "
                    f"Limit: {info.limit}, Wait: {wait_time:.2f}s"
                )

            return None

        # 附加限流器引用以便外部访问
        wrapper._rate_limiter = limiter
        wrapper._rate_limiter_name = limiter_name

        return wrapper

    return decorator


def rate_limit_per_argument(
    key_func: Callable[..., str],
    algorithm: Algorithm = Algorithm.SLIDING_WINDOW,
    rate: Optional[float] = None,
    capacity: Optional[int] = None,
    limit: Optional[int] = None,
    window_size: Optional[float] = None,
    raise_on_limit: bool = True
):
    """
    基于参数的速率限制装饰器

    为不同的参数值创建独立的限流器。

    Args:
        key_func: 从函数参数提取键的函数
        algorithm: 限流算法
        rate: 速率
        capacity: 容量
        limit: 窗口内最大请求数
        window_size: 窗口大小
        raise_on_limit: 是否抛出异常

    Returns:
        装饰器函数

    示例:
        @rate_limit_per_argument(
            key_func=lambda user_id: f"user_{user_id}",
            limit=10,
            window_size=60
        )
        def user_api(user_id):
            return f"Hello, {user_id}"
    """
    def decorator(func: Callable) -> Callable:
        limiters: Dict[str, RateLimiter] = {}
        limiters_lock = threading.Lock()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 提取键
            key = key_func(*args, **kwargs)

            # 获取或创建限流器
            with limiters_lock:
                if key not in limiters:
                    limiters[key] = RateLimiter(
                        algorithm=algorithm,
                        rate=rate,
                        capacity=capacity,
                        limit=limit,
                        window_size=window_size
                    )
                limiter = limiters[key]

            # 尝试获取许可
            if not limiter.try_acquire(1):
                state = limiter.get_state()
                if raise_on_limit:
                    raise RateLimitExceeded(
                        f"Rate limit exceeded for key '{key}'. "
                        f"Limit: {state.get('limit', 'N/A')}"
                    )
                return None

            return func(*args, **kwargs)

        wrapper._per_argument_limiters = limiters

        return wrapper

    return decorator


class RateLimiterContext:
    """
    上下文管理器形式的速率限制器

    示例:
        limiter = RateLimiterContext(
            algorithm=Algorithm.TOKEN_BUCKET,
            rate=10,
            capacity=20
        )

        with limiter:
            # 受限流保护的代码
            pass

        # 或者
        with limiter.acquire_or_raise():
            pass

        # 或者等待
        with limiter.acquire_or_wait(timeout=5):
            pass
    """

    def __init__(
        self,
        algorithm: Algorithm = Algorithm.TOKEN_BUCKET,
        **kwargs
    ):
        self._limiter = RateLimiter(algorithm=algorithm, **kwargs)
        self._acquired = False
        self._timeout: Optional[float] = None

    def __enter__(self):
        """默认行为：尝试获取，失败返回 None"""
        self._acquired = self._limiter.try_acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._acquired = False
        return False

    def acquire_or_raise(self) -> 'RateLimiterContext':
        """
        获取许可或抛出异常

        Returns:
            self 用于链式调用
        """
        if not self._limiter.try_acquire():
            raise RateLimitExceeded("Rate limit exceeded")
        self._acquired = True
        return self

    def acquire_or_wait(self, timeout: Optional[float] = None) -> 'RateLimiterContext':
        """
        等待获取许可

        Args:
            timeout: 超时时间（秒）

        Returns:
            self 用于链式调用
        """
        self._timeout = timeout
        self._limiter.acquire_or_wait(max_wait=timeout)
        self._acquired = True
        return self

    @property
    def acquired(self) -> bool:
        """是否已获取许可"""
        return self._acquired

    @property
    def limiter(self) -> RateLimiter:
        """底层限流器"""
        return self._limiter


def async_rate_limit(
    name: Optional[str] = None,
    algorithm: Algorithm = Algorithm.TOKEN_BUCKET,
    rate: Optional[float] = None,
    capacity: Optional[int] = None,
    limit: Optional[int] = None,
    window_size: Optional[float] = None
):
    """
    异步函数速率限制装饰器

    示例:
        @async_rate_limit(rate=10, capacity=20)
        async def my_async_api():
            return "success"
    """
    def decorator(func: Callable) -> Callable:
        import asyncio

        limiter_name = name or f"_{func.__module__}_{func.__qualname__}"
        limiter = get_or_create_limiter(
            limiter_name,
            algorithm=algorithm,
            rate=rate,
            capacity=capacity,
            limit=limit,
            window_size=window_size
        )
        lock = asyncio.Lock()

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with lock:
                # 使用循环等待
                while not limiter.try_acquire(1):
                    await asyncio.sleep(0.01)

            return await func(*args, **kwargs)

        wrapper._rate_limiter = limiter
        wrapper._rate_limiter_name = limiter_name

        return wrapper

    return decorator


def clear_limiters() -> None:
    """清除所有全局限流器"""
    with _global_limiters_lock:
        _global_limiters.clear()


def list_limiters() -> Dict[str, Dict[str, Any]]:
    """列出所有全局限流器及其状态"""
    with _global_limiters_lock:
        return {name: limiter.get_state() for name, limiter in _global_limiters.items()}