"""
速率限制器工具库 (Rate Limiter Utils)

提供多种速率限制算法实现，支持 API 调用控制、爬虫限流、流量整形等场景。

包含算法：
- TokenBucket: 令牌桶算法（允许突发流量）
- SlidingWindow: 滑动窗口算法（精确控制）
- FixedWindow: 固定窗口算法（简单高效）
- LeakyBucket: 漏桶算法（平滑流量）
- MultiLimiter: 多维度限制器（支持 IP/用户/API 多重限制）

零外部依赖，仅使用 Python 标准库。
"""

import time
import threading
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from typing import Optional, Callable, Any, Dict, List, Tuple
from functools import wraps
from contextlib import contextmanager


@dataclass
class RateLimitResult:
    """速率限制检查结果"""
    allowed: bool
    remaining: int
    reset_time: float
    retry_after: float = 0.0
    
    def __bool__(self) -> bool:
        return self.allowed


class BaseRateLimiter(ABC):
    """速率限制器基类"""
    
    @abstractmethod
    def acquire(self, tokens: int = 1) -> RateLimitResult:
        """获取许可"""
        pass
    
    @abstractmethod
    def try_acquire(self, tokens: int = 1) -> RateLimitResult:
        """尝试获取许可（非阻塞）"""
        pass
    
    def wait_for_token(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        """
        等待直到获取许可
        
        Args:
            tokens: 需要的令牌数
            timeout: 超时时间（秒），None 表示无限等待
            
        Returns:
            是否成功获取许可
        """
        start_time = time.time()
        while True:
            result = self.acquire(tokens)
            if result.allowed:
                return True
            
            wait_time = result.retry_after
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed + wait_time > timeout:
                    return False
            
            time.sleep(wait_time)
    
    def reset(self) -> None:
        """重置限制器状态"""
        pass


class TokenBucket(BaseRateLimiter):
    """
    令牌桶算法速率限制器
    
    特点：
    - 允许一定程度的突发流量
    - 平滑限流，令牌按固定速率生成
    - 适合需要处理突发流量的场景
    
    Args:
        rate: 令牌生成速率（令牌/秒）
        capacity: 桶容量（最大令牌数）
        initial_tokens: 初始令牌数，默认等于容量
    """
    
    def __init__(
        self,
        rate: float,
        capacity: int,
        initial_tokens: Optional[float] = None
    ):
        if rate <= 0:
            raise ValueError("rate must be positive")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        
        self.rate = rate
        self.capacity = capacity
        self._tokens = float(initial_tokens if initial_tokens is not None else capacity)
        self._last_time = time.time()
        self._lock = threading.Lock()
    
    def _refill(self) -> None:
        """补充令牌"""
        now = time.time()
        elapsed = now - self._last_time
        self._tokens = min(
            self.capacity,
            self._tokens + elapsed * self.rate
        )
        self._last_time = now
    
    def acquire(self, tokens: int = 1) -> RateLimitResult:
        """获取令牌"""
        with self._lock:
            self._refill()
            
            if tokens > self.capacity:
                raise ValueError(f"Requested {tokens} tokens exceeds capacity {self.capacity}")
            
            if self._tokens >= tokens:
                self._tokens -= tokens
                return RateLimitResult(
                    allowed=True,
                    remaining=int(self._tokens),
                    reset_time=self._tokens / self.rate + time.time(),
                    retry_after=0.0
                )
            else:
                needed = tokens - self._tokens
                wait_time = needed / self.rate
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_time=time.time() + wait_time,
                    retry_after=wait_time
                )
    
    def try_acquire(self, tokens: int = 1) -> RateLimitResult:
        """尝试获取令牌（非阻塞）"""
        with self._lock:
            self._refill()
            
            if tokens > self.capacity:
                raise ValueError(f"Requested {tokens} tokens exceeds capacity {self.capacity}")
            
            if self._tokens >= tokens:
                self._tokens -= tokens
                return RateLimitResult(
                    allowed=True,
                    remaining=int(self._tokens),
                    reset_time=self._tokens / self.rate + time.time(),
                    retry_after=0.0
                )
            else:
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_time=time.time() + (self.capacity - self._tokens) / self.rate,
                    retry_after=(tokens - self._tokens) / self.rate
                )
    
    def reset(self) -> None:
        """重置桶状态"""
        with self._lock:
            self._tokens = float(self.capacity)
            self._last_time = time.time()
    
    @property
    def tokens(self) -> float:
        """当前令牌数"""
        with self._lock:
            self._refill()
            return self._tokens


class SlidingWindow(BaseRateLimiter):
    """
    滑动窗口算法速率限制器
    
    特点：
    - 精确控制，无边界效应
    - 记录每次请求的时间戳
    - 内存使用与请求数成正比
    
    Args:
        max_requests: 窗口内最大请求数
        window_size: 窗口大小（秒）
    """
    
    def __init__(self, max_requests: int, window_size: float):
        if max_requests <= 0:
            raise ValueError("max_requests must be positive")
        if window_size <= 0:
            raise ValueError("window_size must be positive")
        
        self.max_requests = max_requests
        self.window_size = window_size
        self._requests: deque = deque()
        self._lock = threading.Lock()
    
    def _clean_old_requests(self) -> None:
        """清理过期请求"""
        now = time.time()
        cutoff = now - self.window_size
        while self._requests and self._requests[0] < cutoff:
            self._requests.popleft()
    
    def acquire(self, tokens: int = 1) -> RateLimitResult:
        """获取许可"""
        with self._lock:
            self._clean_old_requests()
            current_count = len(self._requests)
            
            if current_count + tokens <= self.max_requests:
                now = time.time()
                for _ in range(tokens):
                    self._requests.append(now)
                
                remaining = self.max_requests - len(self._requests)
                oldest = self._requests[0] if self._requests else now
                reset_time = oldest + self.window_size
                
                return RateLimitResult(
                    allowed=True,
                    remaining=remaining,
                    reset_time=reset_time,
                    retry_after=0.0
                )
            else:
                oldest = self._requests[0] if self._requests else time.time()
                wait_time = oldest + self.window_size - time.time()
                
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_time=oldest + self.window_size,
                    retry_after=max(0, wait_time)
                )
    
    def try_acquire(self, tokens: int = 1) -> RateLimitResult:
        """尝试获取许可（非阻塞）"""
        return self.acquire(tokens)
    
    def reset(self) -> None:
        """重置窗口"""
        with self._lock:
            self._requests.clear()
    
    @property
    def current_count(self) -> int:
        """当前窗口内请求数"""
        with self._lock:
            self._clean_old_requests()
            return len(self._requests)


class FixedWindow(BaseRateLimiter):
    """
    固定窗口算法速率限制器
    
    特点：
    - 简单高效，内存占用低
    - 存在边界效应（窗口边界可能通过 2 倍请求）
    - 适合简单限流场景
    
    Args:
        max_requests: 窗口内最大请求数
        window_size: 窗口大小（秒）
    """
    
    def __init__(self, max_requests: int, window_size: float):
        if max_requests <= 0:
            raise ValueError("max_requests must be positive")
        if window_size <= 0:
            raise ValueError("window_size must be positive")
        
        self.max_requests = max_requests
        self.window_size = window_size
        self._count = 0
        self._window_start = time.time()
        self._lock = threading.Lock()
    
    def _check_window(self) -> None:
        """检查并更新窗口"""
        now = time.time()
        if now - self._window_start >= self.window_size:
            self._count = 0
            self._window_start = now
    
    def acquire(self, tokens: int = 1) -> RateLimitResult:
        """获取许可"""
        with self._lock:
            self._check_window()
            
            if self._count + tokens <= self.max_requests:
                self._count += tokens
                remaining = self.max_requests - self._count
                reset_time = self._window_start + self.window_size
                
                return RateLimitResult(
                    allowed=True,
                    remaining=remaining,
                    reset_time=reset_time,
                    retry_after=0.0
                )
            else:
                reset_time = self._window_start + self.window_size
                wait_time = reset_time - time.time()
                
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_time=reset_time,
                    retry_after=max(0, wait_time)
                )
    
    def try_acquire(self, tokens: int = 1) -> RateLimitResult:
        """尝试获取许可（非阻塞）"""
        return self.acquire(tokens)
    
    def reset(self) -> None:
        """重置窗口"""
        with self._lock:
            self._count = 0
            self._window_start = time.time()
    
    @property
    def current_count(self) -> int:
        """当前窗口内请求数"""
        with self._lock:
            self._check_window()
            return self._count


class LeakyBucket(BaseRateLimiter):
    """
    漏桶算法速率限制器
    
    特点：
    - 严格限制流出速率
    - 平滑流量，不允许突发
    - 适合需要稳定输出的场景
    
    Args:
        rate: 流出速率（请求/秒）
        capacity: 桶容量（最大排队数）
    """
    
    def __init__(self, rate: float, capacity: int):
        if rate <= 0:
            raise ValueError("rate must be positive")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        
        self.rate = rate
        self.capacity = capacity
        self._water = 0.0
        self._last_time = time.time()
        self._lock = threading.Lock()
    
    def _leak(self) -> None:
        """漏水"""
        now = time.time()
        elapsed = now - self._last_time
        leaked = elapsed * self.rate
        self._water = max(0, self._water - leaked)
        self._last_time = now
    
    def acquire(self, tokens: int = 1) -> RateLimitResult:
        """获取许可"""
        with self._lock:
            self._leak()
            
            if tokens > self.capacity:
                raise ValueError(f"Requested {tokens} tokens exceeds capacity {self.capacity}")
            
            if self._water + tokens <= self.capacity:
                self._water += tokens
                remaining = self.capacity - int(self._water)
                empty_time = self._water / self.rate
                
                return RateLimitResult(
                    allowed=True,
                    remaining=remaining,
                    reset_time=time.time() + empty_time,
                    retry_after=0.0
                )
            else:
                space_needed = self._water + tokens - self.capacity
                wait_time = space_needed / self.rate
                
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_time=time.time() + (self._water / self.rate),
                    retry_after=wait_time
                )
    
    def try_acquire(self, tokens: int = 1) -> RateLimitResult:
        """尝试获取许可（非阻塞）"""
        return self.acquire(tokens)
    
    def reset(self) -> None:
        """重置桶"""
        with self._lock:
            self._water = 0.0
            self._last_time = time.time()
    
    @property
    def water_level(self) -> float:
        """当前水量"""
        with self._lock:
            self._leak()
            return self._water


class MultiLimiter:
    """
    多维度速率限制器
    
    支持对多个维度（如 IP、用户、API）同时进行限制。
    
    Args:
        config: 配置字典，key 为维度名，value 为 (limiter_class, kwargs)
    """
    
    def __init__(
        self,
        config: Dict[str, Tuple[type, Dict[str, Any]]]
    ):
        self._limiters: Dict[str, BaseRateLimiter] = {}
        
        for name, (limiter_class, kwargs) in config.items():
            self._limiters[name] = limiter_class(**kwargs)
    
    def acquire(self, tokens: int = 1, dimensions: Optional[List[str]] = None) -> Dict[str, RateLimitResult]:
        """
        获取许可
        
        Args:
            tokens: 请求数量
            dimensions: 指定维度列表，None 表示所有维度
            
        Returns:
            各维度的检查结果
        """
        results = {}
        dims = dimensions or list(self._limiters.keys())
        
        for dim in dims:
            if dim in self._limiters:
                results[dim] = self._limiters[dim].acquire(tokens)
        
        return results
    
    def try_acquire(self, tokens: int = 1, dimensions: Optional[List[str]] = None) -> Dict[str, RateLimitResult]:
        """尝试获取许可（非阻塞）"""
        results = {}
        dims = dimensions or list(self._limiters.keys())
        
        for dim in dims:
            if dim in self._limiters:
                results[dim] = self._limiters[dim].try_acquire(tokens)
        
        return results
    
    def is_allowed(self, tokens: int = 1, dimensions: Optional[List[str]] = None) -> bool:
        """检查是否所有维度都允许"""
        results = self.try_acquire(tokens, dimensions)
        return all(r.allowed for r in results.values())
    
    def get_retry_after(self, dimensions: Optional[List[str]] = None) -> float:
        """获取最长等待时间"""
        results = self.try_acquire(1, dimensions)
        if not results:
            return 0.0
        return max(r.retry_after for r in results.values() if not r.allowed)
    
    def reset(self, dimension: Optional[str] = None) -> None:
        """重置指定维度或所有维度"""
        if dimension:
            if dimension in self._limiters:
                self._limiters[dimension].reset()
        else:
            for limiter in self._limiters.values():
                limiter.reset()


class RateLimiterRegistry:
    """
    速率限制器注册表
    
    用于管理多个命名的限制器实例。
    """
    
    _instance: Optional['RateLimiterRegistry'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'RateLimiterRegistry':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._limiters: Dict[str, BaseRateLimiter] = {}
        return cls._instance
    
    def register(self, name: str, limiter: BaseRateLimiter) -> None:
        """注册限制器"""
        self._limiters[name] = limiter
    
    def get(self, name: str) -> Optional[BaseRateLimiter]:
        """获取限制器"""
        return self._limiters.get(name)
    
    def unregister(self, name: str) -> bool:
        """注销限制器"""
        if name in self._limiters:
            del self._limiters[name]
            return True
        return False
    
    def clear(self) -> None:
        """清空所有限制器"""
        self._limiters.clear()
    
    def names(self) -> List[str]:
        """获取所有限制器名称"""
        return list(self._limiters.keys())


def rate_limit(
    limiter: BaseRateLimiter,
    tokens: int = 1,
    on_reject: Optional[Callable[[RateLimitResult], Any]] = None
):
    """
    速率限制装饰器
    
    Args:
        limiter: 速率限制器实例
        tokens: 消耗的令牌数
        on_reject: 被拒绝时的回调函数
        
    Example:
        >>> limiter = TokenBucket(rate=10, capacity=100)
        >>> @rate_limit(limiter, tokens=1)
        ... def api_call():
        ...     return "success"
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = limiter.try_acquire(tokens)
            if result.allowed:
                return func(*args, **kwargs)
            elif on_reject:
                return on_reject(result)
            else:
                raise RateLimitExceeded(
                    f"Rate limit exceeded. Retry after {result.retry_after:.2f}s",
                    result
                )
        return wrapper
    return decorator


def async_rate_limit(
    limiter: BaseRateLimiter,
    tokens: int = 1,
    on_reject: Optional[Callable[[RateLimitResult], Any]] = None
):
    """
    异步速率限制装饰器
    
    Args:
        limiter: 速率限制器实例
        tokens: 消耗的令牌数
        on_reject: 被拒绝时的回调函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = limiter.try_acquire(tokens)
            if result.allowed:
                return await func(*args, **kwargs)
            elif on_reject:
                return on_reject(result)
            else:
                raise RateLimitExceeded(
                    f"Rate limit exceeded. Retry after {result.retry_after:.2f}s",
                    result
                )
        return wrapper
    return decorator


class RateLimitExceeded(Exception):
    """速率限制超出异常"""
    
    def __init__(self, message: str, result: RateLimitResult):
        super().__init__(message)
        self.result = result


@contextmanager
def rate_limit_context(limiter: BaseRateLimiter, tokens: int = 1):
    """
    速率限制上下文管理器
    
    Example:
        >>> limiter = TokenBucket(rate=10, capacity=100)
        >>> with rate_limit_context(limiter):
        ...     # 执行受限操作
        ...     pass
    """
    result = limiter.acquire(tokens)
    if not result.allowed:
        raise RateLimitExceeded(
            f"Rate limit exceeded. Retry after {result.retry_after:.2f}s",
            result
        )
    try:
        yield result
    finally:
        pass


# 便捷函数
def create_token_bucket(rate: float, capacity: int) -> TokenBucket:
    """创建令牌桶限制器"""
    return TokenBucket(rate=rate, capacity=capacity)


def create_sliding_window(max_requests: int, window_size: float) -> SlidingWindow:
    """创建滑动窗口限制器"""
    return SlidingWindow(max_requests=max_requests, window_size=window_size)


def create_fixed_window(max_requests: int, window_size: float) -> FixedWindow:
    """创建固定窗口限制器"""
    return FixedWindow(max_requests=max_requests, window_size=window_size)


def create_leaky_bucket(rate: float, capacity: int) -> LeakyBucket:
    """创建漏桶限制器"""
    return LeakyBucket(rate=rate, capacity=capacity)