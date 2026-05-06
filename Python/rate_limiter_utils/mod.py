"""
Rate Limiter Utils - 速率限制器工具集

提供多种速率限制算法的实现，用于控制请求频率、防止系统过载。

支持算法：
- TokenBucket: 令牌桶算法，允许突发流量
- LeakyBucket: 漏桶算法，平滑输出流量
- SlidingWindow: 滑动窗口算法，精确控制
- FixedWindow: 固定窗口算法，简单高效

零外部依赖，仅使用Python标准库。
"""

import time
import threading
from collections import deque
from typing import Optional, Callable, Any
from abc import ABC, abstractmethod
from functools import wraps


class RateLimiterBase(ABC):
    """速率限制器基类"""
    
    @abstractmethod
    def acquire(self, tokens: int = 1) -> bool:
        """
        尝试获取许可
        
        Args:
            tokens: 需要的令牌数量
            
        Returns:
            是否成功获取
        """
        pass
    
    @abstractmethod
    def wait_for(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        """
        等待直到获取许可
        
        Args:
            tokens: 需要的令牌数量
            timeout: 超时时间（秒），None表示无限等待
            
        Returns:
            是否成功获取
        """
        pass
    
    @property
    @abstractmethod
    def available(self) -> float:
        """当前可用许可数量"""
        pass


class TokenBucket(RateLimiterBase):
    """
    令牌桶算法
    
    以固定速率向桶中添加令牌，请求消耗令牌。
    允许一定程度的突发流量（桶满时）。
    
    特点：
    - 平滑限流
    - 允许突发流量
    - 内存效率高
    """
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        初始化令牌桶
        
        Args:
            capacity: 桶容量（最大令牌数）
            refill_rate: 令牌填充速率（令牌/秒）
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
            
        self._capacity = capacity
        self._refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.time()
        self._lock = threading.Lock()
    
    def _refill(self) -> None:
        """重新填充令牌"""
        now = time.time()
        elapsed = now - self._last_refill
        tokens_to_add = elapsed * self._refill_rate
        self._tokens = min(self._capacity, self._tokens + tokens_to_add)
        self._last_refill = now
    
    def acquire(self, tokens: int = 1) -> bool:
        if tokens <= 0:
            raise ValueError("Tokens must be positive")
            
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False
    
    def wait_for(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        if tokens > self._capacity:
            return False
            
        start_time = time.time()
        while True:
            if self.acquire(tokens):
                return True
                
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return False
                    
            # 计算需要等待的时间
            with self._lock:
                self._refill()
                needed = tokens - self._tokens
                if needed <= 0:
                    continue
                wait_time = needed / self._refill_rate
                
            if timeout is not None:
                elapsed = time.time() - start_time
                remaining = timeout - elapsed
                if remaining <= 0:
                    return False
                wait_time = min(wait_time, remaining)
                
            time.sleep(min(wait_time, 0.01))
    
    @property
    def available(self) -> float:
        with self._lock:
            self._refill()
            return self._tokens
    
    @property
    def capacity(self) -> int:
        return self._capacity
    
    @property
    def refill_rate(self) -> float:
        return self._refill_rate


class LeakyBucket(RateLimiterBase):
    """
    漏桶算法
    
    请求以任意速率进入桶中，以固定速率流出。
    强制平滑输出流量，不允许突发。
    
    特点：
    - 严格限流
    - 平滑输出
    - 防止突发流量
    """
    
    def __init__(self, capacity: int, leak_rate: float):
        """
        初始化漏桶
        
        Args:
            capacity: 桶容量
            leak_rate: 漏出速率（请求/秒）
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if leak_rate <= 0:
            raise ValueError("Leak rate must be positive")
            
        self._capacity = capacity
        self._leak_rate = leak_rate
        self._water = 0.0
        self._last_leak = time.time()
        self._lock = threading.Lock()
    
    def _leak(self) -> None:
        """漏水"""
        now = time.time()
        elapsed = now - self._last_leak
        leaked = elapsed * self._leak_rate
        self._water = max(0, self._water - leaked)
        self._last_leak = now
    
    def acquire(self, tokens: int = 1) -> bool:
        if tokens <= 0:
            raise ValueError("Tokens must be positive")
            
        with self._lock:
            self._leak()
            if self._water + tokens <= self._capacity:
                self._water += tokens
                return True
            return False
    
    def wait_for(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        if tokens > self._capacity:
            return False
            
        start_time = time.time()
        while True:
            if self.acquire(tokens):
                return True
                
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return False
                    
            # 计算需要等待的时间
            with self._lock:
                self._leak()
                wait_time = (self._water + tokens - self._capacity) / self._leak_rate
                wait_time = max(0, wait_time)
                
            if timeout is not None:
                elapsed = time.time() - start_time
                remaining = timeout - elapsed
                if remaining <= 0:
                    return False
                wait_time = min(wait_time, remaining)
                
            time.sleep(min(wait_time, 0.01))
    
    @property
    def available(self) -> float:
        with self._lock:
            self._leak()
            return self._capacity - self._water
    
    @property
    def capacity(self) -> int:
        return self._capacity
    
    @property
    def leak_rate(self) -> float:
        return self._leak_rate


class SlidingWindow(RateLimiterBase):
    """
    滑动窗口算法
    
    在滑动时间窗口内统计请求数量，精确控制速率。
    使用时间戳队列实现。
    
    特点：
    - 精确限流
    - 无突发流量
    - 内存使用与窗口大小成正比
    """
    
    def __init__(self, max_requests: int, window_seconds: float):
        """
        初始化滑动窗口
        
        Args:
            max_requests: 窗口内最大请求数
            window_seconds: 窗口大小（秒）
        """
        if max_requests <= 0:
            raise ValueError("Max requests must be positive")
        if window_seconds <= 0:
            raise ValueError("Window seconds must be positive")
            
        self._max_requests = max_requests
        self._window = window_seconds
        self._timestamps: deque = deque()
        self._lock = threading.Lock()
    
    def _cleanup(self) -> None:
        """清理过期时间戳"""
        cutoff = time.time() - self._window
        while self._timestamps and self._timestamps[0] <= cutoff:
            self._timestamps.popleft()
    
    def acquire(self, tokens: int = 1) -> bool:
        if tokens <= 0:
            raise ValueError("Tokens must be positive")
            
        with self._lock:
            self._cleanup()
            if len(self._timestamps) + tokens <= self._max_requests:
                now = time.time()
                for _ in range(tokens):
                    self._timestamps.append(now)
                return True
            return False
    
    def wait_for(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        if tokens > self._max_requests:
            return False
            
        start_time = time.time()
        while True:
            if self.acquire(tokens):
                return True
                
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return False
            
            # 计算需要等待的时间
            with self._lock:
                self._cleanup()
                if len(self._timestamps) + tokens <= self._max_requests:
                    continue
                # 等待最旧的请求过期
                oldest = self._timestamps[0] if self._timestamps else time.time()
                wait_time = oldest + self._window - time.time() + 0.001
                
            if timeout is not None:
                elapsed = time.time() - start_time
                remaining = timeout - elapsed
                if remaining <= 0:
                    return False
                wait_time = min(wait_time, remaining)
                
            time.sleep(max(0, min(wait_time, 0.01)))
    
    @property
    def available(self) -> float:
        with self._lock:
            self._cleanup()
            return self._max_requests - len(self._timestamps)
    
    @property
    def max_requests(self) -> int:
        return self._max_requests
    
    @property
    def window_seconds(self) -> float:
        return self._window
    
    @property
    def current_count(self) -> int:
        """当前窗口内的请求数"""
        with self._lock:
            self._cleanup()
            return len(self._timestamps)


class FixedWindow(RateLimiterBase):
    """
    固定窗口算法
    
    在固定时间窗口内限制请求数量。
    实现简单，但在窗口边界可能有问题（突发）。
    
    特点：
    - 实现简单
    - 内存效率高
    - 边界突发问题
    """
    
    def __init__(self, max_requests: int, window_seconds: float):
        """
        初始化固定窗口
        
        Args:
            max_requests: 窗口内最大请求数
            window_seconds: 窗口大小（秒）
        """
        if max_requests <= 0:
            raise ValueError("Max requests must be positive")
        if window_seconds <= 0:
            raise ValueError("Window seconds must be positive")
            
        self._max_requests = max_requests
        self._window = window_seconds
        self._count = 0
        self._window_start = time.time()
        self._lock = threading.Lock()
    
    def _check_window(self) -> None:
        """检查是否需要重置窗口"""
        now = time.time()
        if now - self._window_start >= self._window:
            self._count = 0
            self._window_start = now
    
    def acquire(self, tokens: int = 1) -> bool:
        if tokens <= 0:
            raise ValueError("Tokens must be positive")
            
        with self._lock:
            self._check_window()
            if self._count + tokens <= self._max_requests:
                self._count += tokens
                return True
            return False
    
    def wait_for(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        if tokens > self._max_requests:
            return False
            
        start_time = time.time()
        while True:
            if self.acquire(tokens):
                return True
                
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return False
            
            # 计算需要等待的时间
            with self._lock:
                self._check_window()
                if self._count + tokens <= self._max_requests:
                    continue
                elapsed_in_window = time.time() - self._window_start
                wait_time = self._window - elapsed_in_window + 0.001
                
            if timeout is not None:
                elapsed = time.time() - start_time
                remaining = timeout - elapsed
                if remaining <= 0:
                    return False
                wait_time = min(wait_time, remaining)
                
            time.sleep(max(0, min(wait_time, 0.01)))
    
    @property
    def available(self) -> float:
        with self._lock:
            self._check_window()
            return self._max_requests - self._count
    
    @property
    def max_requests(self) -> int:
        return self._max_requests
    
    @property
    def window_seconds(self) -> float:
        return self._window
    
    @property
    def current_count(self) -> int:
        """当前窗口内的请求数"""
        with self._lock:
            self._check_window()
            return self._count
    
    @property
    def time_until_reset(self) -> float:
        """距离窗口重置的时间"""
        with self._lock:
            self._check_window()
            elapsed = time.time() - self._window_start
            return max(0, self._window - elapsed)


class RateLimiter:
    """
    综合速率限制器
    
    提供便捷的接口和装饰器支持。
    """
    
    ALGORITHM_TOKEN_BUCKET = 'token_bucket'
    ALGORITHM_LEAKY_BUCKET = 'leaky_bucket'
    ALGORITHM_SLIDING_WINDOW = 'sliding_window'
    ALGORITHM_FIXED_WINDOW = 'fixed_window'
    
    def __init__(
        self,
        max_requests: int,
        window_seconds: float = 1.0,
        algorithm: str = ALGORITHM_TOKEN_BUCKET
    ):
        """
        创建速率限制器
        
        Args:
            max_requests: 最大请求数
            window_seconds: 时间窗口（秒）
            algorithm: 算法类型
            
        Algorithms:
            - token_bucket: 令牌桶，允许突发
            - leaky_bucket: 漏桶，平滑输出
            - sliding_window: 滑动窗口，精确控制
            - fixed_window: 固定窗口，简单高效
        """
        self._algorithm = algorithm
        
        if algorithm == self.ALGORITHM_TOKEN_BUCKET:
            self._limiter = TokenBucket(max_requests, max_requests / window_seconds)
        elif algorithm == self.ALGORITHM_LEAKY_BUCKET:
            self._limiter = LeakyBucket(max_requests, max_requests / window_seconds)
        elif algorithm == self.ALGORITHM_SLIDING_WINDOW:
            self._limiter = SlidingWindow(max_requests, window_seconds)
        elif algorithm == self.ALGORITHM_FIXED_WINDOW:
            self._limiter = FixedWindow(max_requests, window_seconds)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    
    @property
    def algorithm(self) -> str:
        return self._algorithm
    
    def acquire(self, tokens: int = 1) -> bool:
        return self._limiter.acquire(tokens)
    
    def wait_for(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        return self._limiter.wait_for(tokens, timeout)
    
    @property
    def available(self) -> float:
        return self._limiter.available
    
    def limit(
        self,
        tokens: int = 1,
        timeout: Optional[float] = None,
        on_limit: Optional[Callable[[], Any]] = None
    ) -> Callable:
        """
        装饰器：限制函数调用速率
        
        Args:
            tokens: 每次调用消耗的令牌数
            timeout: 等待超时
            on_limit: 被限制时的回调，返回值将作为函数返回值
            
        Returns:
            装饰后的函数
            
        Example:
            >>> limiter = RateLimiter(10, 1.0)
            >>> @limiter.limit(on_limit=lambda: None)
            ... def api_call():
            ...     return "result"
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 当没有超时但有回调时，使用即时检查
                # 当有超时或没有回调时，使用等待模式
                if timeout is None and on_limit is not None:
                    # 即时检查，不等待
                    if not self.acquire(tokens):
                        return on_limit()
                else:
                    # 等待模式（可超时）
                    if not self.wait_for(tokens, timeout):
                        if on_limit is not None:
                            return on_limit()
                        raise RuntimeError("Rate limit exceeded")
                return func(*args, **kwargs)
            return wrapper
        return decorator


class MultiRateLimiter:
    """
    多键速率限制器
    
    为不同的键维护独立的速率限制器。
    适用于多用户、多接口场景。
    """
    
    def __init__(
        self,
        max_requests: int,
        window_seconds: float = 1.0,
        algorithm: str = RateLimiter.ALGORITHM_TOKEN_BUCKET,
        max_keys: int = 10000
    ):
        """
        Args:
            max_requests: 每个键的最大请求数
            window_seconds: 时间窗口
            algorithm: 算法类型
            max_keys: 最大键数量（防止内存泄漏）
        """
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._algorithm = algorithm
        self._max_keys = max_keys
        self._limiters: dict[str, RateLimiterBase] = {}
        self._lock = threading.Lock()
    
    def _get_limiter(self, key: str) -> RateLimiterBase:
        """获取或创建指定键的限制器"""
        with self._lock:
            if key not in self._limiters:
                if len(self._limiters) >= self._max_keys:
                    # 清理旧的限制器
                    self._limiters.clear()
                
                if self._algorithm == RateLimiter.ALGORITHM_TOKEN_BUCKET:
                    rate = self._max_requests / self._window_seconds
                    self._limiters[key] = TokenBucket(self._max_requests, rate)
                elif self._algorithm == RateLimiter.ALGORITHM_LEAKY_BUCKET:
                    rate = self._max_requests / self._window_seconds
                    self._limiters[key] = LeakyBucket(self._max_requests, rate)
                elif self._algorithm == RateLimiter.ALGORITHM_SLIDING_WINDOW:
                    self._limiters[key] = SlidingWindow(self._max_requests, self._window_seconds)
                else:
                    self._limiters[key] = FixedWindow(self._max_requests, self._window_seconds)
                    
            return self._limiters[key]
    
    def acquire(self, key: str, tokens: int = 1) -> bool:
        return self._get_limiter(key).acquire(tokens)
    
    def wait_for(self, key: str, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        return self._get_limiter(key).wait_for(tokens, timeout)
    
    def available(self, key: str) -> float:
        return self._get_limiter(key).available
    
    def reset(self, key: str) -> None:
        """重置指定键的限制器"""
        with self._lock:
            if key in self._limiters:
                del self._limiters[key]
    
    def reset_all(self) -> None:
        """重置所有限制器"""
        with self._lock:
            self._limiters.clear()
    
    @property
    def key_count(self) -> int:
        """当前键数量"""
        with self._lock:
            return len(self._limiters)


# 便捷函数
def create_token_bucket(capacity: int, refill_rate: float) -> TokenBucket:
    """创建令牌桶限制器"""
    return TokenBucket(capacity, refill_rate)


def create_leaky_bucket(capacity: int, leak_rate: float) -> LeakyBucket:
    """创建漏桶限制器"""
    return LeakyBucket(capacity, leak_rate)


def create_sliding_window(max_requests: int, window_seconds: float) -> SlidingWindow:
    """创建滑动窗口限制器"""
    return SlidingWindow(max_requests, window_seconds)


def create_fixed_window(max_requests: int, window_seconds: float) -> FixedWindow:
    """创建固定窗口限制器"""
    return FixedWindow(max_requests, window_seconds)


__all__ = [
    'RateLimiterBase',
    'TokenBucket',
    'LeakyBucket',
    'SlidingWindow',
    'FixedWindow',
    'RateLimiter',
    'MultiRateLimiter',
    'create_token_bucket',
    'create_leaky_bucket',
    'create_sliding_window',
    'create_fixed_window',
]