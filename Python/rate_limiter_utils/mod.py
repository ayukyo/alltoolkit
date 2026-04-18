"""
rate_limiter_utils - 速率限制器工具集

提供多种速率限制算法的实现，支持：
- 滑动窗口计数器 (Sliding Window Counter)
- 令牌桶 (Token Bucket)
- 漏桶 (Leaky Bucket)
- 固定窗口计数器 (Fixed Window Counter)

所有实现均为零外部依赖，纯 Python 标准库实现。

作者: AllToolkit
日期: 2026-04-19
"""

import time
import threading
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass
from typing import Optional, Callable, Any
from enum import Enum


class RateLimitResult:
    """速率限制检查结果"""
    
    def __init__(self, allowed: bool, remaining: int, reset_time: float, retry_after: float = 0):
        """
        初始化结果
        
        Args:
            allowed: 是否允许请求
            remaining: 剩余配额
            reset_time: 配额重置时间戳
            retry_after: 需要等待的秒数（仅当不允许时有效）
        """
        self.allowed = allowed
        self.remaining = remaining
        self.reset_time = reset_time
        self.retry_after = retry_after
    
    def __repr__(self):
        return (f"RateLimitResult(allowed={self.allowed}, remaining={self.remaining}, "
                f"reset_time={self.reset_time:.2f}, retry_after={self.retry_after:.2f})")
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'allowed': self.allowed,
            'remaining': self.remaining,
            'reset_time': self.reset_time,
            'retry_after': self.retry_after
        }


class RateLimiterBase(ABC):
    """速率限制器基类"""
    
    def __init__(self, max_requests: int, window_seconds: float):
        """
        初始化速率限制器
        
        Args:
            max_requests: 时间窗口内允许的最大请求数
            window_seconds: 时间窗口大小（秒）
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
    
    @abstractmethod
    def try_acquire(self, tokens: int = 1) -> RateLimitResult:
        """
        尝试获取许可
        
        Args:
            tokens: 请求的令牌数（默认为1）
            
        Returns:
            RateLimitResult: 检查结果
        """
        pass
    
    @abstractmethod
    def get_state(self) -> dict:
        """获取当前状态（用于监控/调试）"""
        pass
    
    def reset(self):
        """重置限制器状态"""
        pass


class FixedWindowRateLimiter(RateLimiterBase):
    """
    固定窗口计数器算法
    
    特点：
    - 实现简单，内存占用小
    - 存在边界突发问题（两个窗口交界处可能突破限制）
    - 适合对精度要求不高的场景
    """
    
    def __init__(self, max_requests: int, window_seconds: float):
        super().__init__(max_requests, window_seconds)
        self._count = 0
        self._window_start = time.time()
    
    def _get_current_window_start(self) -> float:
        """获取当前窗口的起始时间"""
        now = time.time()
        window_start = self._window_start
        elapsed = now - window_start
        
        if elapsed >= self.window_seconds:
            # 进入新窗口
            windows_passed = int(elapsed // self.window_seconds)
            self._window_start = window_start + windows_passed * self.window_seconds
            self._count = 0
        
        return self._window_start
    
    def try_acquire(self, tokens: int = 1) -> RateLimitResult:
        with self._lock:
            self._get_current_window_start()
            
            remaining = max(0, self.max_requests - self._count)
            reset_time = self._window_start + self.window_seconds
            
            if self._count + tokens <= self.max_requests:
                self._count += tokens
                remaining = self.max_requests - self._count
                return RateLimitResult(True, remaining, reset_time)
            else:
                retry_after = reset_time - time.time()
                return RateLimitResult(False, 0, reset_time, retry_after)
    
    def get_state(self) -> dict:
        with self._lock:
            self._get_current_window_start()
            return {
                'type': 'fixed_window',
                'count': self._count,
                'max_requests': self.max_requests,
                'window_seconds': self.window_seconds,
                'window_start': self._window_start,
                'window_end': self._window_start + self.window_seconds
            }
    
    def reset(self):
        with self._lock:
            self._count = 0
            self._window_start = time.time()


class SlidingWindowRateLimiter(RateLimiterBase):
    """
    滑动窗口计数器算法
    
    特点：
    - 精确控制速率，无边界突发问题
    - 使用时间戳队列记录请求
    - 适合需要精确控制的场景
    """
    
    def __init__(self, max_requests: int, window_seconds: float):
        super().__init__(max_requests, window_seconds)
        self._timestamps: deque = deque()
    
    def _cleanup(self):
        """清理过期的请求记录"""
        now = time.time()
        cutoff = now - self.window_seconds
        while self._timestamps and self._timestamps[0] < cutoff:
            self._timestamps.popleft()
    
    def try_acquire(self, tokens: int = 1) -> RateLimitResult:
        with self._lock:
            self._cleanup()
            
            current_count = len(self._timestamps)
            remaining = max(0, self.max_requests - current_count)
            
            # 计算最老请求过期的时间作为重置时间
            if self._timestamps:
                oldest = self._timestamps[0]
                reset_time = oldest + self.window_seconds
            else:
                reset_time = time.time() + self.window_seconds
            
            if current_count + tokens <= self.max_requests:
                now = time.time()
                for _ in range(tokens):
                    self._timestamps.append(now)
                remaining = self.max_requests - len(self._timestamps)
                return RateLimitResult(True, remaining, reset_time)
            else:
                retry_after = reset_time - time.time()
                return RateLimitResult(False, 0, reset_time, retry_after)
    
    def get_state(self) -> dict:
        with self._lock:
            self._cleanup()
            timestamps = list(self._timestamps)
            return {
                'type': 'sliding_window',
                'count': len(timestamps),
                'max_requests': self.max_requests,
                'window_seconds': self.window_seconds,
                'oldest_request': timestamps[0] if timestamps else None,
                'newest_request': timestamps[-1] if timestamps else None
            }
    
    def reset(self):
        with self._lock:
            self._timestamps.clear()


class TokenBucketRateLimiter(RateLimiterBase):
    """
    令牌桶算法
    
    特点：
    - 支持突发流量（令牌可累积）
    - 平滑限流
    - 适合需要处理突发流量的场景
    
    参数：
        max_requests: 桶的最大容量
        window_seconds: 填满桶所需的时间
    """
    
    def __init__(self, max_requests: int, window_seconds: float, initial_tokens: Optional[float] = None):
        super().__init__(max_requests, window_seconds)
        # 每秒添加的令牌数
        self._rate = max_requests / window_seconds
        # 当前令牌数
        self._tokens = initial_tokens if initial_tokens is not None else float(max_requests)
        # 上次更新时间
        self._last_update = time.time()
    
    def _refill(self):
        """补充令牌"""
        now = time.time()
        elapsed = now - self._last_update
        new_tokens = elapsed * self._rate
        self._tokens = min(self.max_requests, self._tokens + new_tokens)
        self._last_update = now
    
    def try_acquire(self, tokens: int = 1) -> RateLimitResult:
        with self._lock:
            self._refill()
            
            remaining = int(self._tokens)
            
            if self._tokens >= tokens:
                self._tokens -= tokens
                remaining = int(self._tokens)
                # 下一个令牌可用时间
                if self._tokens < 1:
                    reset_time = self._last_update + (1 - self._tokens) / self._rate
                else:
                    reset_time = self._last_update
                return RateLimitResult(True, remaining, reset_time)
            else:
                # 计算需要等待的时间
                needed = tokens - self._tokens
                retry_after = needed / self._rate
                reset_time = time.time() + retry_after
                return RateLimitResult(False, 0, reset_time, retry_after)
    
    def get_state(self) -> dict:
        with self._lock:
            self._refill()
            return {
                'type': 'token_bucket',
                'tokens': self._tokens,
                'max_requests': self.max_requests,
                'window_seconds': self.window_seconds,
                'rate_per_second': self._rate,
                'last_update': self._last_update
            }
    
    def reset(self):
        with self._lock:
            self._tokens = float(self.max_requests)
            self._last_update = time.time()


class LeakyBucketRateLimiter(RateLimiterBase):
    """
    漏桶算法
    
    特点：
    - 以恒定速率处理请求
    - 无突发流量，严格限流
    - 适合需要严格控制流出速率的场景
    """
    
    def __init__(self, capacity: int, leak_rate: float):
        """
        初始化漏桶
        
        Args:
            capacity: 桶的容量（最大排队请求数）
            leak_rate: 漏出速率（请求/秒）
        """
        super().__init__(capacity, 1.0)  # window_seconds 不适用于漏桶
        self._leak_rate = leak_rate  # 每秒处理的请求数
        self._water = 0.0  # 当前水量
        self._last_leak = time.time()
    
    def _leak(self):
        """漏水"""
        now = time.time()
        elapsed = now - self._last_leak
        leaked = elapsed * self._leak_rate
        self._water = max(0, self._water - leaked)
        self._last_leak = now
    
    def try_acquire(self, tokens: int = 1) -> RateLimitResult:
        with self._lock:
            self._leak()
            
            remaining = int(self.max_requests - self._water)
            
            if self._water + tokens <= self.max_requests:
                self._water += tokens
                remaining = int(self.max_requests - self._water)
                # 桶完全漏空的时间
                reset_time = self._last_leak + self._water / self._leak_rate
                return RateLimitResult(True, remaining, reset_time)
            else:
                # 计算需要等待的时间
                overflow = self._water + tokens - self.max_requests
                retry_after = overflow / self._leak_rate
                reset_time = time.time() + retry_after
                return RateLimitResult(False, 0, reset_time, retry_after)
    
    def get_state(self) -> dict:
        with self._lock:
            self._leak()
            return {
                'type': 'leaky_bucket',
                'water': self._water,
                'capacity': self.max_requests,
                'leak_rate': self._leak_rate,
                'last_leak': self._last_leak
            }
    
    def reset(self):
        with self._lock:
            self._water = 0.0
            self._last_leak = time.time()


class RateLimiterRegistry:
    """
    速率限制器注册表
    
    管理多个命名限制器，支持按 key（如用户ID、IP等）进行限制
    """
    
    def __init__(self, limiter_class: type, max_requests: int, window_seconds: float, **limiter_kwargs):
        """
        初始化注册表
        
        Args:
            limiter_class: 限制器类
            max_requests: 最大请求数
            window_seconds: 时间窗口
            **limiter_kwargs: 传递给限制器的其他参数
        """
        self._limiter_class = limiter_class
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._limiter_kwargs = limiter_kwargs
        self._limiters: dict[str, RateLimiterBase] = {}
        self._lock = threading.Lock()
    
    def _get_limiter(self, key: str) -> RateLimiterBase:
        """获取或创建限制器"""
        with self._lock:
            if key not in self._limiters:
                self._limiters[key] = self._limiter_class(
                    self._max_requests, 
                    self._window_seconds,
                    **self._limiter_kwargs
                )
            return self._limiters[key]
    
    def try_acquire(self, key: str, tokens: int = 1) -> RateLimitResult:
        """
        尝试为指定 key 获取许可
        
        Args:
            key: 标识符（如用户ID、IP等）
            tokens: 请求的令牌数
            
        Returns:
            RateLimitResult: 检查结果
        """
        limiter = self._get_limiter(key)
        return limiter.try_acquire(tokens)
    
    def get_state(self, key: str) -> dict:
        """获取指定 key 的限制器状态"""
        return self._get_limiter(key).get_state()
    
    def reset(self, key: str):
        """重置指定 key 的限制器"""
        with self._lock:
            if key in self._limiters:
                self._limiters[key].reset()
    
    def reset_all(self):
        """重置所有限制器"""
        with self._lock:
            for limiter in self._limiters.values():
                limiter.reset()
    
    def cleanup(self, max_age_seconds: float = 3600):
        """
        清理长时间未使用的限制器
        
        Args:
            max_age_seconds: 最大闲置时间（秒）
        """
        # 注意：此方法需要限制器支持获取最后访问时间
        # 简化实现：清理状态中长时间未更新的限制器
        pass


def rate_limit(
    limiter: RateLimiterBase,
    on_reject: Optional[Callable[[RateLimitResult], Any]] = None
):
    """
    装饰器：为函数添加速率限制
    
    Args:
        limiter: 速率限制器实例
        on_reject: 被拒绝时的回调函数
        
    Returns:
        装饰器函数
        
    Example:
        >>> limiter = TokenBucketRateLimiter(10, 1.0)
        >>> @rate_limit(limiter)
        ... def my_api():
        ...     return "success"
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = limiter.try_acquire()
            if result.allowed:
                return func(*args, **kwargs)
            elif on_reject:
                return on_reject(result)
            else:
                raise RateLimitExceeded(
                    f"Rate limit exceeded. Retry after {result.retry_after:.2f} seconds",
                    result
                )
        return wrapper
    return decorator


class RateLimitExceeded(Exception):
    """速率限制异常"""
    
    def __init__(self, message: str, result: RateLimitResult):
        super().__init__(message)
        self.result = result


# 便捷函数
def create_limiter(
    algorithm: str,
    max_requests: int,
    window_seconds: float,
    **kwargs
) -> RateLimiterBase:
    """
    创建速率限制器的便捷函数
    
    Args:
        algorithm: 算法类型 ('fixed_window', 'sliding_window', 'token_bucket', 'leaky_bucket')
        max_requests: 最大请求数
        window_seconds: 时间窗口（秒）
        **kwargs: 其他参数
        
    Returns:
        RateLimiterBase: 限制器实例
        
    Example:
        >>> limiter = create_limiter('token_bucket', 100, 60)
    """
    algorithms = {
        'fixed_window': FixedWindowRateLimiter,
        'sliding_window': SlidingWindowRateLimiter,
        'token_bucket': TokenBucketRateLimiter,
        'leaky_bucket': LeakyBucketRateLimiter,
    }
    
    if algorithm not in algorithms:
        raise ValueError(f"Unknown algorithm: {algorithm}. "
                        f"Available: {list(algorithms.keys())}")
    
    # 漏桶算法使用不同的参数名
    if algorithm == 'leaky_bucket':
        return LeakyBucketRateLimiter(
            capacity=max_requests,
            leak_rate=kwargs.get('leak_rate', max_requests / window_seconds)
        )
    
    return algorithms[algorithm](max_requests, window_seconds, **kwargs)


if __name__ == "__main__":
    # 简单演示
    print("=== 固定窗口算法 ===")
    fw = FixedWindowRateLimiter(5, 10)
    for i in range(7):
        result = fw.try_acquire()
        print(f"请求 {i+1}: {result}")
    
    print("\n=== 令牌桶算法 ===")
    tb = TokenBucketRateLimiter(5, 10)
    for i in range(7):
        result = tb.try_acquire()
        print(f"请求 {i+1}: {result}")
    
    print("\n=== 多用户限流 ===")
    registry = RateLimiterRegistry(SlidingWindowRateLimiter, 3, 60)
    for user in ['user1', 'user2']:
        print(f"\n{user}:")
        for i in range(5):
            result = registry.try_acquire(user)
            print(f"  请求 {i+1}: {result}")