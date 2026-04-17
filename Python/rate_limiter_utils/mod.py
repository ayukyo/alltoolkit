"""
Rate Limiter Utils - 零依赖限流器工具集

提供多种限流算法实现：
- TokenBucket: 令牌桶算法，支持突发流量
- LeakyBucket: 漏桶算法，平滑输出流量
- SlidingWindow: 滑动窗口算法，精确计数
- FixedWindow: 固定窗口算法，简单高效
- RateLimiterRegistry: 多实例限流器管理

适用场景：
- API 请求限流
- 用户操作频率控制
- 资源访问保护
- 流量整形
"""

import time
import threading
from abc import ABC, abstractmethod
from collections import deque
from typing import Optional, Callable, Any, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum


class RateLimitResult:
    """限流检查结果"""
    
    def __init__(
        self,
        allowed: bool,
        remaining: int = 0,
        reset_time: Optional[float] = None,
        retry_after: float = 0.0,
        message: str = ""
    ):
        self.allowed = allowed
        self.remaining = remaining  # 剩余配额
        self.reset_time = reset_time  # 重置时间戳
        self.retry_after = retry_after  # 建议等待秒数
        self.message = message
    
    def __bool__(self) -> bool:
        return self.allowed
    
    def __repr__(self) -> str:
        status = "✓ 允许" if self.allowed else "✗ 拒绝"
        return f"<RateLimitResult {status}, remaining={self.remaining}, retry_after={self.retry_after:.2f}s>"


class BaseRateLimiter(ABC):
    """限流器基类"""
    
    def __init__(self, max_requests: int, window_seconds: float = 1.0):
        """
        Args:
            max_requests: 时间窗口内允许的最大请求数
            window_seconds: 时间窗口大小（秒）
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
    
    @abstractmethod
    def acquire(self, tokens: int = 1) -> RateLimitResult:
        """
        尝试获取访问许可
        
        Args:
            tokens: 请求的令牌数（默认1）
        
        Returns:
            RateLimitResult 检查结果
        """
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """获取限流器状态信息"""
        pass
    
    def reset(self) -> None:
        """重置限流器状态"""
        pass
    
    def __enter__(self) -> 'BaseRateLimiter':
        return self
    
    def __exit__(self, *args) -> None:
        self.reset()


class TokenBucket(BaseRateLimiter):
    """
    令牌桶限流器
    
    特点：
    - 支持突发流量（桶内有令牌时可快速处理）
    - 平滑限流（令牌匀速生成）
    - 适合 API 限流场景
    
    算法说明：
    - 以固定速率向桶中添加令牌
    - 每个请求消耗一个或多个令牌
    - 桶满时令牌溢出
    - 无令牌时请求被拒绝
    """
    
    def __init__(
        self,
        max_requests: int,
        window_seconds: float = 1.0,
        refill_rate: Optional[float] = None
    ):
        """
        Args:
            max_requests: 桶容量（最大令牌数）
            window_seconds: 用于计算填充速率的时间窗口
            refill_rate: 每秒填充的令牌数（默认 = max_requests / window_seconds）
        """
        super().__init__(max_requests, window_seconds)
        self.capacity = max_requests
        self.tokens = float(max_requests)  # 当前令牌数
        self.refill_rate = refill_rate or (max_requests / window_seconds)
        self.last_refill = time.time()
    
    def _refill(self) -> None:
        """补充令牌"""
        now = time.time()
        elapsed = now - self.last_refill
        if elapsed > 0:
            new_tokens = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_refill = now
    
    def acquire(self, tokens: int = 1) -> RateLimitResult:
        with self._lock:
            self._refill()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return RateLimitResult(
                    allowed=True,
                    remaining=int(self.tokens),
                    message=f"请求通过，消耗 {tokens} 令牌"
                )
            else:
                # 计算需要等待的时间
                deficit = tokens - self.tokens
                wait_time = deficit / self.refill_rate
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    retry_after=wait_time,
                    message=f"令牌不足，需等待 {wait_time:.2f}s"
                )
    
    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            self._refill()
            return {
                "type": "TokenBucket",
                "capacity": self.capacity,
                "tokens": self.tokens,
                "refill_rate": self.refill_rate,
                "utilization": (self.capacity - self.tokens) / self.capacity
            }
    
    def reset(self) -> None:
        with self._lock:
            self.tokens = float(self.capacity)
            self.last_refill = time.time()


class LeakyBucket(BaseRateLimiter):
    """
    漏桶限流器
    
    特点：
    - 固定速率输出流量
    - 不支持突发流量
    - 适合流量整形场景
    
    算法说明：
    - 请求进入队列（桶）
    - 以固定速率从队列中取出请求处理
    - 队列满时请求被拒绝
    """
    
    def __init__(
        self,
        max_requests: int,
        window_seconds: float = 1.0,
        leak_rate: Optional[float] = None
    ):
        """
        Args:
            max_requests: 桶容量（队列最大长度）
            window_seconds: 用于计算泄漏速率的时间窗口
            leak_rate: 每秒处理的请求数（默认 = max_requests / window_seconds）
        """
        super().__init__(max_requests, window_seconds)
        self.capacity = max_requests
        self.queue: deque = deque()
        self.leak_rate = leak_rate or (max_requests / window_seconds)
        self.last_leak = time.time()
    
    def _leak(self) -> None:
        """泄漏（处理）请求"""
        now = time.time()
        elapsed = now - self.last_leak
        if elapsed > 0:
            # 计算应该处理的请求数
            process_count = int(elapsed * self.leak_rate)
            for _ in range(min(process_count, len(self.queue))):
                if self.queue:
                    self.queue.popleft()
            self.last_leak = now
    
    def acquire(self, tokens: int = 1) -> RateLimitResult:
        with self._lock:
            self._leak()
            
            if len(self.queue) + tokens <= self.capacity:
                for _ in range(tokens):
                    self.queue.append(time.time())
                return RateLimitResult(
                    allowed=True,
                    remaining=self.capacity - len(self.queue),
                    message=f"请求已入队，队列长度 {len(self.queue)}"
                )
            else:
                # 计算等待时间
                wait_time = len(self.queue) / self.leak_rate
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    retry_after=wait_time,
                    message=f"桶已满，队列长度 {len(self.queue)}"
                )
    
    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            self._leak()
            return {
                "type": "LeakyBucket",
                "capacity": self.capacity,
                "queue_size": len(self.queue),
                "leak_rate": self.leak_rate,
                "utilization": len(self.queue) / self.capacity
            }
    
    def reset(self) -> None:
        with self._lock:
            self.queue.clear()
            self.last_leak = time.time()


class SlidingWindow(BaseRateLimiter):
    """
    滑动窗口限流器
    
    特点：
    - 精确计数
    - 无边界效应
    - 内存占用与请求数成正比
    
    算法说明：
    - 记录每个请求的时间戳
    - 计算窗口内的请求数
    - 超出限制时拒绝请求
    """
    
    def __init__(self, max_requests: int, window_seconds: float = 1.0):
        """
        Args:
            max_requests: 时间窗口内允许的最大请求数
            window_seconds: 时间窗口大小（秒）
        """
        super().__init__(max_requests, window_seconds)
        self.requests: deque = deque()  # 存储请求时间戳
    
    def _clean(self) -> None:
        """清理过期请求"""
        cutoff = time.time() - self.window_seconds
        while self.requests and self.requests[0] < cutoff:
            self.requests.popleft()
    
    def acquire(self, tokens: int = 1) -> RateLimitResult:
        with self._lock:
            self._clean()
            current_count = len(self.requests)
            
            if current_count + tokens <= self.max_requests:
                now = time.time()
                for _ in range(tokens):
                    self.requests.append(now)
                return RateLimitResult(
                    allowed=True,
                    remaining=self.max_requests - len(self.requests),
                    reset_time=now + self.window_seconds,
                    message=f"请求通过，窗口内已有 {len(self.requests)} 次"
                )
            else:
                # 计算最早请求何时过期
                if self.requests:
                    oldest = self.requests[0]
                    retry_after = oldest + self.window_seconds - time.time()
                    reset_time = oldest + self.window_seconds
                else:
                    retry_after = 0
                    reset_time = time.time() + self.window_seconds
                
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_time=reset_time,
                    retry_after=max(0, retry_after),
                    message=f"窗口内已有 {current_count} 次请求，超出限制"
                )
    
    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            self._clean()
            now = time.time()
            window_start = now - self.window_seconds
            return {
                "type": "SlidingWindow",
                "max_requests": self.max_requests,
                "current_count": len(self.requests),
                "window_seconds": self.window_seconds,
                "utilization": len(self.requests) / self.max_requests,
                "window_start": window_start
            }
    
    def reset(self) -> None:
        with self._lock:
            self.requests.clear()


class FixedWindow(BaseRateLimiter):
    """
    固定窗口限流器
    
    特点：
    - 简单高效
    - 内存占用小
    - 存在边界效应（窗口边界可能突发2倍请求）
    
    算法说明：
    - 将时间划分为固定大小的窗口
    - 每个窗口内独立计数
    - 新窗口开始时计数重置
    """
    
    def __init__(
        self,
        max_requests: int,
        window_seconds: float = 1.0,
        window_alignment: str = "natural"
    ):
        """
        Args:
            max_requests: 每个窗口允许的最大请求数
            window_seconds: 窗口大小（秒）
            window_alignment: 窗口对齐方式
                - "natural": 按自然时间对齐（如每分钟、每小时）
                - "from_first": 从第一个请求开始计时
        """
        super().__init__(max_requests, window_seconds)
        self.window_alignment = window_alignment
        self.count = 0
        self.window_start = 0.0
    
    def _get_window_start(self, now: float) -> float:
        """获取当前窗口的开始时间"""
        if self.window_alignment == "natural":
            # 自然对齐：窗口从整点开始
            return now - (now % self.window_seconds)
        else:
            # 从第一个请求开始
            return self.window_start
    
    def _check_window(self) -> None:
        """检查是否需要开启新窗口"""
        now = time.time()
        window_start = self._get_window_start(now)
        
        if self.window_start == 0:
            # 第一个请求
            self.window_start = window_start if self.window_alignment == "natural" else now
            self.count = 0
        elif window_start >= self.window_start + self.window_seconds:
            # 新窗口
            self.window_start = window_start
            self.count = 0
    
    def acquire(self, tokens: int = 1) -> RateLimitResult:
        with self._lock:
            self._check_window()
            
            if self.count + tokens <= self.max_requests:
                self.count += tokens
                now = time.time()
                reset_time = self.window_start + self.window_seconds
                return RateLimitResult(
                    allowed=True,
                    remaining=self.max_requests - self.count,
                    reset_time=reset_time,
                    message=f"请求通过，当前窗口已用 {self.count}/{self.max_requests}"
                )
            else:
                now = time.time()
                reset_time = self.window_start + self.window_seconds
                retry_after = reset_time - now
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_time=reset_time,
                    retry_after=max(0, retry_after),
                    message=f"窗口已达上限 {self.count}/{self.max_requests}"
                )
    
    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            self._check_window()
            now = time.time()
            return {
                "type": "FixedWindow",
                "max_requests": self.max_requests,
                "current_count": self.count,
                "window_seconds": self.window_seconds,
                "window_start": self.window_start,
                "window_end": self.window_start + self.window_seconds,
                "utilization": self.count / self.max_requests
            }
    
    def reset(self) -> None:
        with self._lock:
            self.count = 0
            self.window_start = 0.0


class RateLimiterRegistry:
    """
    限流器注册表
    
    用于管理多个限流器实例，支持按用户、IP、API等维度限流
    """
    
    def __init__(self, limiter_class: type, **limiter_kwargs):
        """
        Args:
            limiter_class: 限流器类（TokenBucket, LeakyBucket等）
            **limiter_kwargs: 限流器初始化参数
        """
        self.limiter_class = limiter_class
        self.limiter_kwargs = limiter_kwargs
        self._limiters: Dict[str, BaseRateLimiter] = {}
        self._lock = threading.Lock()
        self._created_at = time.time()
    
    def get_limiter(self, key: str) -> BaseRateLimiter:
        """获取或创建指定 key 的限流器"""
        with self._lock:
            if key not in self._limiters:
                self._limiters[key] = self.limiter_class(**self.limiter_kwargs)
            return self._limiters[key]
    
    def acquire(self, key: str, tokens: int = 1) -> RateLimitResult:
        """尝试为指定 key 获取访问许可"""
        return self.get_limiter(key).acquire(tokens)
    
    def get_all_status(self) -> Dict[str, Dict[str, Any]]:
        """获取所有限流器状态"""
        with self._lock:
            return {key: limiter.get_status() for key, limiter in self._limiters.items()}
    
    def remove_limiter(self, key: str) -> bool:
        """移除指定的限流器"""
        with self._lock:
            if key in self._limiters:
                del self._limiters[key]
                return True
            return False
    
    def clear_inactive(self, max_age_seconds: float = 3600) -> int:
        """清理长时间未使用的限流器"""
        # 简化实现：清理所有限流器
        with self._lock:
            count = len(self._limiters)
            self._limiters.clear()
            return count
    
    def get_stats(self) -> Dict[str, Any]:
        """获取注册表统计信息"""
        with self._lock:
            return {
                "limiter_count": len(self._limiters),
                "limiter_class": self.limiter_class.__name__,
                "limiter_config": self.limiter_kwargs,
                "uptime_seconds": time.time() - self._created_at
            }


def rate_limit(
    limiter: BaseRateLimiter,
    on_reject: Optional[Callable[[RateLimitResult], Any]] = None
):
    """
    限流装饰器
    
    Args:
        limiter: 限流器实例
        on_reject: 被拒绝时的回调函数
    
    Example:
        >>> limiter = TokenBucket(10, 1.0)
        >>> @rate_limit(limiter, on_reject=lambda r: print(f"被限流: {r.message}"))
        ... def api_call():
        ...     return "success"
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            result = limiter.acquire()
            if result.allowed:
                return func(*args, **kwargs)
            elif on_reject:
                return on_reject(result)
            else:
                raise Exception(f"Rate limit exceeded: {result.message}")
        return wrapper
    return decorator


# 便捷函数
def create_token_bucket(qps: float, burst: int = None) -> TokenBucket:
    """
    创建令牌桶限流器
    
    Args:
        qps: 每秒请求数
        burst: 突发容量（默认等于 qps）
    
    Example:
        >>> limiter = create_token_bucket(qps=100, burst=200)
        >>> result = limiter.acquire()
    """
    burst = burst or int(qps)
    return TokenBucket(max_requests=burst, window_seconds=1.0, refill_rate=qps)


def create_sliding_window(max_requests: int, window_seconds: float) -> SlidingWindow:
    """
    创建滑动窗口限流器
    
    Args:
        max_requests: 窗口内最大请求数
        window_seconds: 窗口大小（秒）
    
    Example:
        >>> limiter = create_sliding_window(100, 60)  # 每分钟100次
        >>> result = limiter.acquire()
    """
    return SlidingWindow(max_requests, window_seconds)


if __name__ == "__main__":
    # 简单演示
    print("=" * 50)
    print("Rate Limiter Utils 演示")
    print("=" * 50)
    
    # 令牌桶演示
    print("\n[TokenBucket] 10 令牌，每秒补充 5 个")
    tb = TokenBucket(10, 1.0, refill_rate=5)
    for i in range(15):
        result = tb.acquire()
        print(f"  请求 {i+1}: {result}")
    time.sleep(1)
    print(f"  等待1秒后: {tb.acquire()}")
    
    # 滑动窗口演示
    print("\n[SlidingWindow] 每秒最多 5 次")
    sw = SlidingWindow(5, 1.0)
    for i in range(7):
        result = sw.acquire()
        print(f"  请求 {i+1}: {result}")
    
    # 固定窗口演示
    print("\n[FixedWindow] 每秒最多 5 次")
    fw = FixedWindow(5, 1.0)
    for i in range(7):
        result = fw.acquire()
        print(f"  请求 {i+1}: {result}")
    
    print("\n" + "=" * 50)
    print("演示完成")