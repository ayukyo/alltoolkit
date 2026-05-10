"""
Rate Limiter Utils - 多种速率限制算法实现

提供多种限流算法：
- TokenBucket: 令牌桶算法，支持突发流量
- LeakyBucket: 漏桶算法，平滑流量输出
- SlidingWindow: 滑动窗口，精确计数
- FixedWindow: 固定窗口，简单高效
- RateLimiter: 统一接口的通用限流器

零外部依赖，线程安全。
"""

import time
import threading
from abc import ABC, abstractmethod
from collections import deque
from typing import Optional, Callable, Any


class RateLimitExceeded(Exception):
    """速率限制超出异常"""
    pass


class BaseRateLimiter(ABC):
    """速率限制器基类"""
    
    @abstractmethod
    def acquire(self, tokens: int = 1) -> bool:
        """
        尝试获取许可
        
        Args:
            tokens: 需要的令牌数量
            
        Returns:
            是否获取成功
        """
        pass
    
    @abstractmethod
    def wait_for_acquire(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        """
        等待直到获取许可或超时
        
        Args:
            tokens: 需要的令牌数量
            timeout: 超时时间（秒），None 表示无限等待
            
        Returns:
            是否获取成功
        """
        pass
    
    @property
    @abstractmethod
    def available(self) -> float:
        """当前可用许可数量"""
        pass


class TokenBucket(BaseRateLimiter):
    """
    令牌桶算法
    
    以固定速率向桶中添加令牌，请求消耗令牌。
    支持突发流量（桶满时），适合需要灵活限流的场景。
    
    特点：
    - 允许突发流量
    - 平滑限流
    - 高效实现
    """
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        初始化令牌桶
        
        Args:
            capacity: 桶容量（最大令牌数）
            refill_rate: 令牌填充速率（令牌数/秒）
        """
        if capacity <= 0:
            raise ValueError("容量必须为正数")
        if refill_rate <= 0:
            raise ValueError("填充速率必须为正数")
            
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.time()
        self._lock = threading.Lock()
    
    def _refill(self):
        """重新填充令牌"""
        now = time.time()
        elapsed = now - self._last_refill
        new_tokens = elapsed * self.refill_rate
        self._tokens = min(self.capacity, self._tokens + new_tokens)
        self._last_refill = now
    
    def acquire(self, tokens: int = 1) -> bool:
        """尝试获取令牌"""
        if tokens <= 0:
            raise ValueError("令牌数必须为正数")
        if tokens > self.capacity:
            raise ValueError(f"请求令牌数 {tokens} 超过容量 {self.capacity}")
            
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False
    
    def wait_for_acquire(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        """等待获取令牌"""
        if tokens <= 0:
            raise ValueError("令牌数必须为正数")
        if tokens > self.capacity:
            raise ValueError(f"请求令牌数 {tokens} 超过容量 {self.capacity}")
            
        start_time = time.time()
        
        while True:
            if self.acquire(tokens):
                return True
                
            # 计算需要等待的时间
            with self._lock:
                self._refill()
                needed_tokens = tokens - self._tokens
                wait_time = needed_tokens / self.refill_rate
                
            # 检查是否超时
            elapsed = time.time() - start_time
            if timeout is not None and elapsed >= timeout:
                return False
                
            # 等待一小段时间再尝试
            # 如果等待时间很短，直接等待；否则分批等待
            sleep_time = min(wait_time, 0.1)
            if timeout is not None:
                remaining_timeout = timeout - elapsed
                sleep_time = min(sleep_time, remaining_timeout / 2)
            
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    @property
    def available(self) -> float:
        """当前可用令牌数"""
        with self._lock:
            self._refill()
            return self._tokens


class LeakyBucket(BaseRateLimiter):
    """
    漏桶算法
    
    以固定速率从桶中漏水，请求加入水滴。
    强制固定输出速率，适合需要严格限流的场景。
    
    特点：
    - 固定输出速率
    - 不允许突发流量
    - 队列化请求
    """
    
    def __init__(self, capacity: int, leak_rate: float):
        """
        初始化漏桶
        
        Args:
            capacity: 桶容量（最大请求数）
            leak_rate: 漏水速率（请求数/秒）
        """
        if capacity <= 0:
            raise ValueError("容量必须为正数")
        if leak_rate <= 0:
            raise ValueError("漏水速率必须为正数")
            
        self.capacity = capacity
        self.leak_rate = leak_rate
        self._queue: deque = deque()
        self._last_leak = time.time()
        self._lock = threading.Lock()
    
    def _leak(self):
        """漏水处理"""
        now = time.time()
        elapsed = now - self._last_leak
        leak_count = int(elapsed * self.leak_rate)
        
        for _ in range(leak_count):
            if self._queue:
                self._queue.popleft()
            else:
                break
                
        self._last_leak = now
    
    def acquire(self, tokens: int = 1) -> bool:
        """尝试加入请求"""
        if tokens <= 0:
            raise ValueError("令牌数必须为正数")
            
        with self._lock:
            self._leak()
            if len(self._queue) + tokens <= self.capacity:
                for _ in range(tokens):
                    self._queue.append(time.time())
                return True
            return False
    
    def wait_for_acquire(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        """等待加入请求"""
        if tokens <= 0:
            raise ValueError("令牌数必须为正数")
        if tokens > self.capacity:
            raise ValueError(f"请求令牌数 {tokens} 超过容量 {self.capacity}")
            
        start_time = time.time()
        
        while True:
            if self.acquire(tokens):
                return True
                
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return False
                    
            time.sleep(1.0 / self.leak_rate / 2)
    
    @property
    def available(self) -> float:
        """当前可用空间"""
        with self._lock:
            self._leak()
            return float(self.capacity - len(self._queue))


class SlidingWindow(BaseRateLimiter):
    """
    滑动窗口算法
    
    精确记录时间窗口内的请求数，滑动窗口边界。
    提供精确的限流控制。
    
    特点：
    - 精确计数
    - 无边界突发问题
    - 内存消耗较高
    """
    
    def __init__(self, max_requests: int, window_seconds: float):
        """
        初始化滑动窗口
        
        Args:
            max_requests: 窗口内最大请求数
            window_seconds: 窗口时间（秒）
        """
        if max_requests <= 0:
            raise ValueError("最大请求数必须为正数")
        if window_seconds <= 0:
            raise ValueError("窗口时间必须为正数")
            
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._timestamps: deque = deque()
        self._lock = threading.Lock()
    
    def _cleanup(self):
        """清理过期时间戳"""
        now = time.time()
        cutoff = now - self.window_seconds
        
        while self._timestamps and self._timestamps[0] < cutoff:
            self._timestamps.popleft()
    
    def acquire(self, tokens: int = 1) -> bool:
        """尝试获取许可"""
        if tokens <= 0:
            raise ValueError("令牌数必须为正数")
        if tokens > self.max_requests:
            raise ValueError(f"请求令牌数 {tokens} 超过最大请求数 {self.max_requests}")
            
        with self._lock:
            self._cleanup()
            if len(self._timestamps) + tokens <= self.max_requests:
                now = time.time()
                for _ in range(tokens):
                    self._timestamps.append(now)
                return True
            return False
    
    def wait_for_acquire(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        """等待获取许可"""
        if tokens <= 0:
            raise ValueError("令牌数必须为正数")
        if tokens > self.max_requests:
            raise ValueError(f"请求令牌数 {tokens} 超过最大请求数 {self.max_requests}")
            
        start_time = time.time()
        
        while True:
            if self.acquire(tokens):
                return True
                
            with self._lock:
                self._cleanup()
                if self._timestamps:
                    oldest = self._timestamps[0]
                    wait_time = oldest + self.window_seconds - time.time() + 0.001
                else:
                    wait_time = 0.1
                    
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return False
                    
            time.sleep(max(0.001, min(wait_time, 0.1)))
    
    @property
    def available(self) -> float:
        """当前可用请求数"""
        with self._lock:
            self._cleanup()
            return float(self.max_requests - len(self._timestamps))


class FixedWindow(BaseRateLimiter):
    """
    固定窗口算法
    
    按固定时间窗口计数，简单高效。
    存在边界突发问题（窗口边界可能 2 倍请求）。
    
    特点：
    - 实现简单
    - 内存消耗低
    - 存在边界突发问题
    """
    
    def __init__(self, max_requests: int, window_seconds: float):
        """
        初始化固定窗口
        
        Args:
            max_requests: 窗口内最大请求数
            window_seconds: 窗口时间（秒）
        """
        if max_requests <= 0:
            raise ValueError("最大请求数必须为正数")
        if window_seconds <= 0:
            raise ValueError("窗口时间必须为正数")
            
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._count = 0
        self._window_start = time.time()
        self._lock = threading.Lock()
    
    def _check_window(self):
        """检查是否需要新窗口"""
        now = time.time()
        if now - self._window_start >= self.window_seconds:
            self._count = 0
            self._window_start = now
    
    def acquire(self, tokens: int = 1) -> bool:
        """尝试获取许可"""
        if tokens <= 0:
            raise ValueError("令牌数必须为正数")
        if tokens > self.max_requests:
            raise ValueError(f"请求令牌数 {tokens} 超过最大请求数 {self.max_requests}")
            
        with self._lock:
            self._check_window()
            if self._count + tokens <= self.max_requests:
                self._count += tokens
                return True
            return False
    
    def wait_for_acquire(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        """等待获取许可"""
        if tokens <= 0:
            raise ValueError("令牌数必须为正数")
        if tokens > self.max_requests:
            raise ValueError(f"请求令牌数 {tokens} 超过最大请求数 {self.max_requests}")
            
        start_time = time.time()
        
        while True:
            if self.acquire(tokens):
                return True
                
            with self._lock:
                self._check_window()
                elapsed = time.time() - self._window_start
                wait_time = self.window_seconds - elapsed + 0.001
                
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return False
                    
            time.sleep(max(0.001, min(wait_time, 0.1)))
    
    @property
    def available(self) -> float:
        """当前可用请求数"""
        with self._lock:
            self._check_window()
            return float(self.max_requests - self._count)


class RateLimiter:
    """
    通用速率限制器
    
    提供统一的限流接口，支持多种算法切换。
    支持装饰器模式和上下文管理器模式。
    """
    
    ALGORITHMS = {
        'token_bucket': TokenBucket,
        'leaky_bucket': LeakyBucket,
        'sliding_window': SlidingWindow,
        'fixed_window': FixedWindow,
    }
    
    def __init__(
        self,
        max_requests: int,
        window_seconds: float = 1.0,
        algorithm: str = 'token_bucket',
        capacity: Optional[int] = None
    ):
        """
        初始化通用速率限制器
        
        Args:
            max_requests: 窗口内最大请求数
            window_seconds: 窗口时间（秒）
            algorithm: 算法类型 ('token_bucket', 'leaky_bucket', 'sliding_window', 'fixed_window')
            capacity: 桶容量（仅 token_bucket 和 leaky_bucket 使用）
        """
        if algorithm not in self.ALGORITHMS:
            raise ValueError(f"未知算法: {algorithm}，可用: {list(self.ALGORITHMS.keys())}")
            
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.algorithm = algorithm
        
        rate = max_requests / window_seconds
        cap = capacity if capacity is not None else max_requests
        
        if algorithm == 'token_bucket':
            self._limiter = TokenBucket(cap, rate)
        elif algorithm == 'leaky_bucket':
            self._limiter = LeakyBucket(cap, rate)
        elif algorithm == 'sliding_window':
            self._limiter = SlidingWindow(max_requests, window_seconds)
        else:  # fixed_window
            self._limiter = FixedWindow(max_requests, window_seconds)
    
    def acquire(self, tokens: int = 1) -> bool:
        """尝试获取许可"""
        return self._limiter.acquire(tokens)
    
    def wait_for_acquire(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        """等待获取许可"""
        return self._limiter.wait_for_acquire(tokens, timeout)
    
    @property
    def available(self) -> float:
        """当前可用许可"""
        return self._limiter.available
    
    def __enter__(self):
        """上下文管理器入口"""
        if not self.wait_for_acquire(timeout=60):
            raise RateLimitExceeded("等待获取许可超时")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        return False
    
    def __call__(self, func: Callable) -> Callable:
        """
        装饰器模式
        
        用法:
            @limiter
            def my_function():
                pass
        """
        def wrapper(*args, **kwargs) -> Any:
            if not self.wait_for_acquire(timeout=60):
                raise RateLimitExceeded("等待获取许可超时")
            return func(*args, **kwargs)
        return wrapper
    
    def decorate(self, tokens: int = 1) -> Callable:
        """
        带参数的装饰器
        
        用法:
            @limiter.decorate(tokens=2)
            def my_function():
                pass
        """
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs) -> Any:
                if not self.wait_for_acquire(tokens, timeout=60):
                    raise RateLimitExceeded("等待获取许可超时")
                return func(*args, **kwargs)
            return wrapper
        return decorator


class AsyncRateLimiter:
    """
    异步速率限制器
    
    提供异步版本的限流控制。
    """
    
    def __init__(
        self,
        max_requests: int,
        window_seconds: float = 1.0,
        algorithm: str = 'token_bucket'
    ):
        """
        初始化异步速率限制器
        
        Args:
            max_requests: 窗口内最大请求数
            window_seconds: 窗口时间（秒）
            algorithm: 算法类型
        """
        self._sync_limiter = RateLimiter(max_requests, window_seconds, algorithm)
        self._lock = threading.Lock()
    
    async def acquire(self, tokens: int = 1) -> bool:
        """异步尝试获取许可"""
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_limiter.acquire, tokens)
    
    async def wait_for_acquire(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        """异步等待获取许可"""
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, 
            lambda: self._sync_limiter.wait_for_acquire(tokens, timeout)
        )
    
    @property
    def available(self) -> float:
        """当前可用许可"""
        return self._sync_limiter.available


class MultiRateLimiter:
    """
    多键速率限制器
    
    为不同的键提供独立的限流控制。
    适合多租户、多用户场景。
    """
    
    def __init__(
        self,
        max_requests: int,
        window_seconds: float = 1.0,
        algorithm: str = 'sliding_window'
    ):
        """
        初始化多键速率限制器
        
        Args:
            max_requests: 窗口内最大请求数
            window_seconds: 窗口时间（秒）
            algorithm: 算法类型
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.algorithm = algorithm
        self._limiters: dict = {}
        self._lock = threading.Lock()
    
    def _get_limiter(self, key: str) -> RateLimiter:
        """获取或创建指定键的限流器"""
        with self._lock:
            if key not in self._limiters:
                self._limiters[key] = RateLimiter(
                    self.max_requests,
                    self.window_seconds,
                    self.algorithm
                )
            return self._limiters[key]
    
    def acquire(self, key: str, tokens: int = 1) -> bool:
        """尝试为指定键获取许可"""
        return self._get_limiter(key).acquire(tokens)
    
    def wait_for_acquire(self, key: str, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        """等待为指定键获取许可"""
        return self._get_limiter(key).wait_for_acquire(tokens, timeout)
    
    def available(self, key: str) -> float:
        """获取指定键的可用许可"""
        return self._get_limiter(key).available
    
    def keys(self) -> list:
        """获取所有键"""
        with self._lock:
            return list(self._limiters.keys())
    
    def clear(self, key: Optional[str] = None):
        """清除指定键或所有键的限流器"""
        with self._lock:
            if key is None:
                self._limiters.clear()
            elif key in self._limiters:
                del self._limiters[key]


# 便捷函数
def create_rate_limiter(
    max_requests: int,
    window_seconds: float = 1.0,
    algorithm: str = 'token_bucket'
) -> RateLimiter:
    """
    创建速率限制器的便捷函数
    
    Args:
        max_requests: 窗口内最大请求数
        window_seconds: 窗口时间（秒）
        algorithm: 算法类型
        
    Returns:
        RateLimiter 实例
    """
    return RateLimiter(max_requests, window_seconds, algorithm)


def rate_limit(
    max_requests: int,
    window_seconds: float = 1.0,
    algorithm: str = 'token_bucket'
) -> Callable:
    """
    速率限制装饰器
    
    用法:
        @rate_limit(10, 1.0)
        def my_api_call():
            pass
    """
    limiter = RateLimiter(max_requests, window_seconds, algorithm)
    return limiter


if __name__ == '__main__':
    # 简单演示
    print("=== Token Bucket 演示 ===")
    tb = TokenBucket(5, 2)  # 容量5，每秒补充2个
    for i in range(10):
        if tb.acquire():
            print(f"请求 {i+1}: 成功 (剩余: {tb.available:.2f})")
        else:
            print(f"请求 {i+1}: 被限流")
        time.sleep(0.3)
    
    print("\n=== Sliding Window 演示 ===")
    sw = SlidingWindow(5, 1.0)  # 1秒内最多5个请求
    for i in range(8):
        if sw.acquire():
            print(f"请求 {i+1}: 成功 (剩余: {sw.available:.0f})")
        else:
            print(f"请求 {i+1}: 被限流")
    
    time.sleep(1.0)
    print("1秒后...")
    if sw.acquire():
        print("新请求: 成功")