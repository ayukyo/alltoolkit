"""
AllToolkit - Python Async Utilities

零依赖异步编程工具模块。提供重试、超时、限流、并发控制等生产就绪工具。
完全使用 Python 标准库 asyncio 实现，无需任何外部依赖。

Author: AllToolkit
License: MIT
"""

import asyncio
import time
import random
import sys
from typing import Optional, Any, Dict, List, Callable, TypeVar, Awaitable, Coroutine
from functools import wraps
from dataclasses import dataclass, field
from collections import deque
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


# =============================================================================
# 异常类
# =============================================================================

class AsyncUtilsError(Exception):
    """异步工具基础异常"""
    pass


class RetryExhaustedError(AsyncUtilsError):
    """重试次数耗尽异常"""
    
    def __init__(self, message: str, last_exception: Optional[Exception] = None, attempts: int = 0):
        super().__init__(message)
        self.last_exception = last_exception
        self.attempts = attempts


class TimeoutError(AsyncUtilsError):
    """超时异常"""
    pass


class SemaphoreAcquireError(AsyncUtilsError):
    """信号量获取失败异常"""
    pass


# =============================================================================
# 重试工具
# =============================================================================

@dataclass
class RetryConfig:
    """重试配置"""
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True
    jitter_factor: float = 0.1
    retryable_exceptions: tuple = (Exception,)
    
    def get_delay(self, attempt: int) -> float:
        """计算第 N 次重试的延迟时间"""
        delay = min(
            self.initial_delay * (self.exponential_base ** (attempt - 1)),
            self.max_delay
        )
        if self.jitter:
            jitter_range = delay * self.jitter_factor
            delay += random.uniform(-jitter_range, jitter_range)
        return max(0, delay)


class AsyncRetry:
    """异步重试工具类"""
    
    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()
        self._stats = {
            'total_attempts': 0,
            'successful': 0,
            'failed': 0,
            'retries': 0,
        }
    
    async def execute(
        self,
        func: Callable[..., Awaitable[T]],
        *args,
        **kwargs
    ) -> T:
        """执行带重试的异步函数"""
        last_exception: Optional[Exception] = None
        
        for attempt in range(1, self.config.max_attempts + 1):
            self._stats['total_attempts'] += 1
            
            try:
                result = await func(*args, **kwargs)
                self._stats['successful'] += 1
                return result
            except self.config.retryable_exceptions as e:
                last_exception = e
                self._stats['failed'] += 1
                
                if attempt < self.config.max_attempts:
                    self._stats['retries'] += 1
                    delay = self.config.get_delay(attempt)
                    logger.info(
                        f"Attempt {attempt} failed: {e}. "
                        f"Retrying in {delay:.2f}s"
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(
                        f"All {self.config.max_attempts} attempts failed. "
                        f"Last error: {e}"
                    )
        
        raise RetryExhaustedError(
            f"Failed after {self.config.max_attempts} attempts",
            last_exception=last_exception,
            attempts=self.config.max_attempts
        )
    
    @property
    def stats(self) -> Dict[str, int]:
        """获取统计信息"""
        return self._stats.copy()
    
    def reset_stats(self) -> None:
        """重置统计"""
        self._stats = {
            'total_attempts': 0,
            'successful': 0,
            'failed': 0,
            'retries': 0,
        }


def retry(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: tuple = (Exception,)
):
    """异步重试装饰器"""
    config = RetryConfig(
        max_attempts=max_attempts,
        initial_delay=initial_delay,
        max_delay=max_delay,
        exponential_base=exponential_base,
        jitter=jitter,
        retryable_exceptions=retryable_exceptions,
    )
    retry_executor = AsyncRetry(config)
    
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            return await retry_executor.execute(func, *args, **kwargs)
        return wrapper
    return decorator


# =============================================================================
# 超时工具
# =============================================================================

async def with_timeout(
    coro: Awaitable[T],
    timeout: float,
    timeout_message: str = "Operation timed out"
) -> T:
    """带超时的异步操作"""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        raise TimeoutError(timeout_message)


def timeout(timeout: float, timeout_message: str = "Operation timed out"):
    """超时装饰器"""
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            return await with_timeout(
                func(*args, **kwargs),
                timeout,
                timeout_message
            )
        return wrapper
    return decorator


# =============================================================================
# 信号量限流
# =============================================================================

class AsyncSemaphore:
    """异步信号量，用于限制并发数"""
    
    def __init__(self, limit: int = 10, timeout: Optional[float] = None):
        if limit < 1:
            raise ValueError("Limit must be at least 1")
        self._limit = limit
        self._timeout = timeout
        self._semaphore = asyncio.Semaphore(limit)
        self._acquired = 0
        self._stats = {
            'total_acquires': 0,
            'total_releases': 0,
            'timeouts': 0,
            'current_held': 0,
        }
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> bool:
        """获取信号量"""
        try:
            if self._timeout:
                acquired = await asyncio.wait_for(
                    self._semaphore.acquire(),
                    timeout=self._timeout
                )
            else:
                acquired = await self._semaphore.acquire()
            
            if acquired:
                async with self._lock:
                    self._acquired += 1
                    self._stats['total_acquires'] += 1
                    self._stats['current_held'] += 1
            return acquired
        except asyncio.TimeoutError:
            self._stats['timeouts'] += 1
            return False
    
    def release(self) -> None:
        """释放信号量"""
        self._semaphore.release()
        self._stats['total_releases'] += 1
        self._stats['current_held'] -= 1
    
    @property
    def limit(self) -> int:
        """获取限制数"""
        return self._limit
    
    @property
    def available(self) -> int:
        """获取可用数量"""
        return self._limit - self._stats['current_held']
    
    @property
    def stats(self) -> Dict[str, int]:
        """获取统计信息"""
        return self._stats.copy()


class SemaphoreContext:
    """信号量上下文管理器（Python 3.6 兼容）"""
    
    def __init__(self, semaphore: AsyncSemaphore):
        self._semaphore = semaphore
        self._acquired = False
    
    async def __aenter__(self):
        acquired = await self._semaphore.acquire()
        if not acquired:
            raise SemaphoreAcquireError(
                f"Failed to acquire semaphore within {self._semaphore._timeout}s"
            )
        self._acquired = True
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._acquired:
            self._semaphore.release()
        return False


class AsyncSemaphoreWithContext(AsyncSemaphore):
    """支持 async with 的信号量"""
    
    def limit_context(self) -> SemaphoreContext:
        """返回上下文管理器"""
        return SemaphoreContext(self)


def rate_limit(limit: int, timeout: Optional[float] = None):
    """速率限制装饰器"""
    semaphore = AsyncSemaphoreWithContext(limit, timeout)
    
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            async with semaphore.limit_context():
                return await func(*args, **kwargs)
        return wrapper
    return decorator


# =============================================================================
# 并发收集工具
# =============================================================================

@dataclass
class GatherResult:
    """并发收集结果"""
    successful: List[Any] = field(default_factory=list)
    failed: List[tuple] = field(default_factory=list)  # (index, exception)
    total: int = 0
    
    @property
    def success_rate(self) -> float:
        """成功率"""
        if self.total == 0:
            return 0.0
        return len(self.successful) / self.total


async def gather_with_results(
    *coros: Awaitable,
    return_exceptions: bool = True
) -> GatherResult:
    """增强的并发收集，返回详细结果"""
    if not coros:
        return GatherResult()
    
    results = await asyncio.gather(*coros, return_exceptions=return_exceptions)
    
    result = GatherResult(total=len(results))
    for i, r in enumerate(results):
        if isinstance(r, Exception):
            result.failed.append((i, r))
        else:
            result.successful.append(r)
    
    return result


async def gather_with_timeout(
    *coros: Awaitable,
    timeout: float,
    return_exceptions: bool = True
) -> GatherResult:
    """带超时的并发收集"""
    try:
        return await asyncio.wait_for(
            gather_with_results(*coros, return_exceptions=return_exceptions),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        result = GatherResult()
        result.failed.append((-1, TimeoutError(f"Gather timed out after {timeout}s")))
        return result


# =============================================================================
# 异步锁工具
# =============================================================================

class AsyncLock:
    """异步锁，带超时和统计"""
    
    def __init__(self, timeout: Optional[float] = None):
        self._lock = asyncio.Lock()
        self._timeout = timeout
        self._stats = {
            'total_acquires': 0,
            'total_releases': 0,
            'timeouts': 0,
            'contentions': 0,
        }
    
    async def acquire(self) -> bool:
        """获取锁"""
        if not self._lock.locked():
            self._stats['contentions'] = self._stats.get('contentions', 0) + 1
        else:
            self._stats['contentions'] = self._stats.get('contentions', 0) + 1
        
        try:
            if self._timeout:
                acquired = await asyncio.wait_for(
                    self._lock.acquire(),
                    timeout=self._timeout
                )
            else:
                acquired = await self._lock.acquire()
            
            if acquired:
                self._stats['total_acquires'] += 1
            return acquired
        except asyncio.TimeoutError:
            self._stats['timeouts'] += 1
            return False
    
    def release(self) -> None:
        """释放锁"""
        self._lock.release()
        self._stats['total_releases'] += 1
    
    @property
    def locked(self) -> bool:
        """检查是否已锁定"""
        return self._lock.locked()
    
    @property
    def stats(self) -> Dict[str, int]:
        """获取统计信息"""
        return self._stats.copy()


class LockContext:
    """锁上下文管理器（Python 3.6 兼容）"""
    
    def __init__(self, lock: AsyncLock):
        self._lock = lock
        self._acquired = False
    
    async def __aenter__(self):
        acquired = await self._lock.acquire()
        if not acquired:
            raise asyncio.TimeoutError(
                f"Failed to acquire lock within {self._lock._timeout}s"
            )
        self._acquired = True
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._acquired:
            self._lock.release()
        return False


class AsyncLockWithContext(AsyncLock):
    """支持 async with 的锁"""
    
    def lock_context(self) -> LockContext:
        """返回上下文管理器"""
        return LockContext(self)


# =============================================================================
# 异步缓存装饰器
# =============================================================================

class AsyncCache:
    """异步函数结果缓存"""
    
    def __init__(self, ttl: float = 300.0, max_size: int = 100):
        self._cache: Dict[str, tuple] = {}  # key -> (value, expires_at)
        self._ttl = ttl
        self._max_size = max_size
        self._lock = asyncio.Lock()
        self._stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'evictions': 0,
            'expirations': 0,
        }
    
    def _make_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """生成缓存键"""
        key_parts = [func_name]
        for arg in args:
            key_parts.append(str(arg))
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}={v}")
        return ":".join(key_parts)
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        async with self._lock:
            if key in self._cache:
                value, expires_at = self._cache[key]
                if expires_at is None or time.time() < expires_at:
                    self._stats['hits'] += 1
                    return value
                else:
                    # 过期，删除
                    del self._cache[key]
                    self._stats['expirations'] += 1
            self._stats['misses'] += 1
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """设置缓存"""
        async with self._lock:
            # 检查是否需要淘汰
            if len(self._cache) >= self._max_size and key not in self._cache:
                # 简单淘汰：删除最旧的
                oldest_key = min(
                    self._cache.keys(),
                    key=lambda k: self._cache[k][1] or float('inf')
                )
                del self._cache[oldest_key]
                self._stats['evictions'] += 1
            
            expires_at = None
            if ttl is not None:
                expires_at = time.time() + ttl
            elif self._ttl > 0:
                expires_at = time.time() + self._ttl
            
            self._cache[key] = (value, expires_at)
            self._stats['sets'] += 1
    
    async def clear(self) -> None:
        """清空缓存"""
        async with self._lock:
            self._cache.clear()
    
    @property
    def size(self) -> int:
        """当前缓存大小"""
        return len(self._cache)
    
    @property
    def stats(self) -> Dict[str, int]:
        """获取统计信息"""
        return self._stats.copy()
    
    @property
    def hit_rate(self) -> float:
        """命中率"""
        total = self._stats['hits'] + self._stats['misses']
        if total == 0:
            return 0.0
        return self._stats['hits'] / total


def async_cached(ttl: float = 300.0, max_size: int = 100):
    """异步函数缓存装饰器"""
    cache = AsyncCache(ttl, max_size)
    
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            key = cache._make_key(func.__name__, args, kwargs)
            
            # 尝试从缓存获取
            cached_value = await cache.get(key)
            if cached_value is not None:
                return cached_value
            
            # 执行函数并缓存结果
            result = await func(*args, **kwargs)
            await cache.set(key, result)
            return result
        return wrapper
    return decorator


# =============================================================================
# 批量处理工具
# =============================================================================

async def batch_process(
    items: List[Any],
    processor: Callable[[Any], Awaitable[T]],
    batch_size: int = 10,
    concurrency: int = 5,
) -> List[T]:
    """批量处理项目，控制并发"""
    results = []
    semaphore = AsyncSemaphoreWithContext(concurrency)
    
    async def process_with_semaphore(item: Any) -> T:
        async with semaphore.limit_context():
            return await processor(item)
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_results = await asyncio.gather(*[
            process_with_semaphore(item) for item in batch
        ])
        results.extend(batch_results)
    
    return results


async def chunked_gather(
    coros: List[Awaitable[T]],
    chunk_size: int = 10,
    delay_between_chunks: float = 0.0,
) -> List[T]:
    """分块并发执行，避免同时发起过多请求"""
    results = []
    
    for i in range(0, len(coros), chunk_size):
        chunk = coros[i:i + chunk_size]
        chunk_results = await asyncio.gather(*chunk)
        results.extend(chunk_results)
        
        if delay_between_chunks > 0 and i + chunk_size < len(coros):
            await asyncio.sleep(delay_between_chunks)
    
    return results


# =============================================================================
# 工具函数
# =============================================================================

async def async_map(
    func: Callable[[Any], Awaitable[T]],
    items: List[Any],
    concurrency: int = 10,
) -> List[T]:
    """异步 map，带并发控制"""
    semaphore = AsyncSemaphoreWithContext(concurrency)
    
    async def wrapped(item: Any) -> T:
        async with semaphore.limit_context():
            return await func(item)
    
    return await asyncio.gather(*[wrapped(item) for item in items])


async def async_filter(
    predicate: Callable[[Any], Awaitable[bool]],
    items: List[Any],
    concurrency: int = 10,
) -> List[Any]:
    """异步 filter，带并发控制"""
    results = await async_map(predicate, items, concurrency)
    return [item for item, keep in zip(items, results) if keep]


async def run_concurrently(
    *coros: Awaitable[T],
    limit: int = 10,
) -> List[T]:
    """限制并发数执行多个协程"""
    semaphore = asyncio.Semaphore(limit)
    
    async def wrapped(coro: Awaitable[T]) -> T:
        async with semaphore:
            return await coro
    
    return await asyncio.gather(*[wrapped(coro) for coro in coros])


# =============================================================================
# 导出
# =============================================================================

__all__ = [
    # 异常
    'AsyncUtilsError',
    'RetryExhaustedError',
    'TimeoutError',
    'SemaphoreAcquireError',
    
    # 重试
    'RetryConfig',
    'AsyncRetry',
    'retry',
    
    # 超时
    'with_timeout',
    'timeout',
    
    # 限流
    'AsyncSemaphore',
    'AsyncSemaphoreWithContext',
    'SemaphoreContext',
    'rate_limit',
    
    # 并发
    'GatherResult',
    'gather_with_results',
    'gather_with_timeout',
    
    # 锁
    'AsyncLock',
    'AsyncLockWithContext',
    'LockContext',
    
    # 缓存
    'AsyncCache',
    'async_cached',
    
    # 批量处理
    'batch_process',
    'chunked_gather',
    
    # 工具函数
    'async_map',
    'async_filter',
    'run_concurrently',
]
