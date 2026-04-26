"""
cache_utils - 零依赖内存缓存工具
================================

功能完整的内存缓存库，支持TTL、LRU淘汰、自动清理等功能。

功能特性：
- 内存缓存：键值对存储
- TTL过期：支持毫秒级过期时间
- LRU淘汰：可选的最近最少使用淘汰策略
- 自动清理：后台线程定期清理过期条目
- 统计信息：命中率、内存使用等
- 批量操作：get_many、set_many、delete_many
- 装饰器：函数结果缓存
- 线程安全：支持多线程环境

使用示例：
    >>> from cache_utils import MemoryCache
    >>> cache = MemoryCache(max_size=1000, default_ttl=60)
    >>> cache.set("key", "value")
    >>> cache.get("key")
    'value'
"""

import threading
import time
import hashlib
import functools
from typing import Any, Optional, Dict, List, Callable, Tuple, Union
from collections import OrderedDict


class CacheEntry:
    """缓存条目"""
    
    __slots__ = ['value', 'expire_at', 'access_count', 'created_at']
    
    def __init__(self, value: Any, expire_at: Optional[float] = None):
        self.value = value
        self.expire_at = expire_at
        self.access_count = 0
        self.created_at = time.time()
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.expire_at is None:
            return False
        return time.time() > self.expire_at
    
    def touch(self):
        """更新访问计数"""
        self.access_count += 1


class MemoryCache:
    """
    内存缓存类，支持TTL和LRU淘汰。
    
    Args:
        max_size: 最大条目数，0表示无限制
        default_ttl: 默认过期时间（秒），None表示永不过期
        cleanup_interval: 自动清理间隔（秒），0表示禁用自动清理
        thread_safe: 是否线程安全
        
    Examples:
        >>> cache = MemoryCache(max_size=100, default_ttl=60)
        >>> cache.set("name", "Alice")
        >>> cache.get("name")
        'Alice'
    """
    
    def __init__(
        self,
        max_size: int = 0,
        default_ttl: Optional[float] = None,
        cleanup_interval: float = 0,
        thread_safe: bool = True
    ):
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._cleanup_interval = cleanup_interval
        self._thread_safe = thread_safe
        
        # 使用OrderedDict实现LRU
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        
        # 线程锁
        self._lock = threading.RLock() if thread_safe else None
        
        # 统计信息
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._expirations = 0
        
        # 自动清理线程
        self._cleanup_thread: Optional[threading.Thread] = None
        self._running = False
        
        if cleanup_interval > 0:
            self._start_cleanup_thread()
    
    def _start_cleanup_thread(self):
        """启动自动清理线程"""
        self._running = True
        self._cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()
    
    def _cleanup_loop(self):
        """清理循环"""
        while self._running:
            time.sleep(self._cleanup_interval)
            self.cleanup_expired()
    
    def _get_lock(self):
        """获取锁上下文"""
        if self._lock:
            return self._lock
        from contextlib import nullcontext
        return nullcontext()
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[float] = None
    ) -> None:
        """
        设置缓存值。
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒），None使用默认值，负数表示永不过期
            
        Examples:
            >>> cache.set("key", "value")
            >>> cache.set("temp", "data", ttl=10)  # 10秒后过期
        """
        # 计算过期时间
        if ttl is None:
            ttl = self._default_ttl
        elif ttl < 0:
            ttl = None
        
        expire_at = None
        if ttl is not None:
            expire_at = time.time() + ttl
        
        entry = CacheEntry(value, expire_at)
        
        with self._get_lock():
            # 如果键已存在，先删除（重新排序）
            if key in self._cache:
                del self._cache[key]
            
            # 检查是否需要淘汰
            if self._max_size > 0 and len(self._cache) >= self._max_size:
                self._evict_lru()
            
            self._cache[key] = entry
    
    def get(
        self,
        key: str,
        default: Any = None
    ) -> Any:
        """
        获取缓存值。
        
        Args:
            key: 缓存键
            default: 默认值
            
        Returns:
            缓存值，如果不存在或过期则返回默认值
            
        Examples:
            >>> cache.set("name", "Alice")
            >>> cache.get("name")
            'Alice'
            >>> cache.get("missing", "default")
            'default'
        """
        with self._get_lock():
            if key not in self._cache:
                self._misses += 1
                return default
            
            entry = self._cache[key]
            
            # 检查是否过期
            if entry.is_expired():
                del self._cache[key]
                self._misses += 1
                self._expirations += 1
                return default
            
            # LRU: 移到最后表示最近使用
            self._cache.move_to_end(key)
            entry.touch()
            self._hits += 1
            
            return entry.value
    
    def has(self, key: str) -> bool:
        """
        检查键是否存在且未过期。
        
        Args:
            key: 缓存键
            
        Returns:
            是否存在
            
        Examples:
            >>> cache.set("key", "value")
            >>> cache.has("key")
            True
        """
        with self._get_lock():
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            if entry.is_expired():
                del self._cache[key]
                self._expirations += 1
                return False
            
            return True
    
    def delete(self, key: str) -> bool:
        """
        删除缓存条目。
        
        Args:
            key: 缓存键
            
        Returns:
            是否成功删除
            
        Examples:
            >>> cache.set("key", "value")
            >>> cache.delete("key")
            True
            >>> cache.delete("missing")
            False
        """
        with self._get_lock():
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def get_or_set(
        self,
        key: str,
        factory: Callable[[], Any],
        ttl: Optional[float] = None
    ) -> Any:
        """
        获取缓存值，如果不存在则通过factory创建。
        
        Args:
            key: 缓存键
            factory: 创建值的函数
            ttl: 过期时间
            
        Returns:
            缓存值或新创建的值
            
        Examples:
            >>> cache.get_or_set("computed", lambda: expensive_computation())
        """
        with self._get_lock():
            if key in self._cache:
                entry = self._cache[key]
                if not entry.is_expired():
                    self._cache.move_to_end(key)
                    entry.touch()
                    self._hits += 1
                    return entry.value
            
            self._misses += 1
            value = factory()
            self.set(key, value, ttl)
            return value
    
    def get_many(self, keys: List[str]) -> Dict[str, Any]:
        """
        批量获取缓存值。
        
        Args:
            keys: 缓存键列表
            
        Returns:
            键值对字典（只包含存在且未过期的）
            
        Examples:
            >>> cache.set("a", 1)
            >>> cache.set("b", 2)
            >>> cache.get_many(["a", "b", "c"])
            {'a': 1, 'b': 2}
        """
        result = {}
        with self._get_lock():
            for key in keys:
                if key in self._cache:
                    entry = self._cache[key]
                    if not entry.is_expired():
                        self._cache.move_to_end(key)
                        entry.touch()
                        self._hits += 1
                        result[key] = entry.value
                    else:
                        del self._cache[key]
                        self._misses += 1
                        self._expirations += 1
                else:
                    self._misses += 1
        return result
    
    def set_many(
        self,
        items: Dict[str, Any],
        ttl: Optional[float] = None
    ) -> None:
        """
        批量设置缓存值。
        
        Args:
            items: 键值对字典
            ttl: 过期时间
            
        Examples:
            >>> cache.set_many({"a": 1, "b": 2, "c": 3})
        """
        for key, value in items.items():
            self.set(key, value, ttl)
    
    def delete_many(self, keys: List[str]) -> int:
        """
        批量删除缓存条目。
        
        Args:
            keys: 缓存键列表
            
        Returns:
            删除的数量
            
        Examples:
            >>> cache.set_many({"a": 1, "b": 2})
            >>> cache.delete_many(["a", "b", "c"])
            2
        """
        count = 0
        with self._get_lock():
            for key in keys:
                if key in self._cache:
                    del self._cache[key]
                    count += 1
        return count
    
    def clear(self) -> None:
        """
        清空所有缓存。
        
        Examples:
            >>> cache.clear()
        """
        with self._get_lock():
            self._cache.clear()
    
    def cleanup_expired(self) -> int:
        """
        清理所有过期条目。
        
        Returns:
            清理的数量
            
        Examples:
            >>> cache.cleanup_expired()
        """
        count = 0
        current_time = time.time()
        
        with self._get_lock():
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry.expire_at is not None and entry.expire_at < current_time
            ]
            
            for key in expired_keys:
                del self._cache[key]
                count += 1
                self._expirations += 1
        
        return count
    
    def _evict_lru(self) -> None:
        """淘汰最近最少使用的条目"""
        if self._cache:
            # OrderedDict第一个元素是最早插入/最少使用的
            self._cache.popitem(last=False)
            self._evictions += 1
    
    def keys(self) -> List[str]:
        """
        获取所有未过期的键。
        
        Returns:
            键列表
            
        Examples:
            >>> cache.keys()
            ['key1', 'key2']
        """
        with self._get_lock():
            self.cleanup_expired()
            return list(self._cache.keys())
    
    def values(self) -> List[Any]:
        """
        获取所有未过期的值。
        
        Returns:
            值列表
        """
        with self._get_lock():
            self.cleanup_expired()
            return [entry.value for entry in self._cache.values()]
    
    def items(self) -> List[Tuple[str, Any]]:
        """
        获取所有未过期的键值对。
        
        Returns:
            键值对列表
        """
        with self._get_lock():
            self.cleanup_expired()
            return [(key, entry.value) for key, entry in self._cache.items()]
    
    def size(self) -> int:
        """
        获取缓存条目数量（包括过期的）。
        
        Returns:
            条目数量
        """
        return len(self._cache)
    
    def ttl(self, key: str) -> Optional[float]:
        """
        获取键的剩余过期时间。
        
        Args:
            key: 缓存键
            
        Returns:
            剩余秒数，None表示永不过期，-1表示不存在
            
        Examples:
            >>> cache.set("key", "value", ttl=60)
            >>> cache.ttl("key")  # 约60秒
            >>> cache.ttl("missing")
            -1
        """
        with self._get_lock():
            if key not in self._cache:
                return -1
            
            entry = self._cache[key]
            if entry.expire_at is None:
                return None
            
            remaining = entry.expire_at - time.time()
            return max(0, remaining)
    
    def extend_ttl(self, key: str, ttl: float) -> bool:
        """
        延长键的过期时间。
        
        Args:
            key: 缓存键
            ttl: 延长的秒数
            
        Returns:
            是否成功
            
        Examples:
            >>> cache.set("key", "value", ttl=10)
            >>> cache.extend_ttl("key", 30)  # 延长30秒
        """
        with self._get_lock():
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            if entry.is_expired():
                return False
            
            if entry.expire_at is None:
                entry.expire_at = time.time() + ttl
            else:
                entry.expire_at += ttl
            
            return True
    
    def touch(self, key: str, new_ttl: Optional[float] = None) -> bool:
        """
        更新键的访问时间，可选更新过期时间。
        
        Args:
            key: 缓存键
            new_ttl: 新的过期时间（秒），None保持不变
            
        Returns:
            是否成功
        """
        with self._get_lock():
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            if entry.is_expired():
                del self._cache[key]
                return False
            
            # LRU: 移到最后
            self._cache.move_to_end(key)
            entry.touch()
            
            if new_ttl is not None:
                if new_ttl < 0:
                    entry.expire_at = None
                else:
                    entry.expire_at = time.time() + new_ttl
            
            return True
    
    def incr(self, key: str, delta: int = 1) -> int:
        """
        增加数值。
        
        Args:
            key: 缓存键
            delta: 增量
            
        Returns:
            增加后的值
            
        Raises:
            ValueError: 值不是整数
            KeyError: 键不存在
            
        Examples:
            >>> cache.set("counter", 0)
            >>> cache.incr("counter")
            1
            >>> cache.incr("counter", 10)
            11
        """
        with self._get_lock():
            if key not in self._cache:
                raise KeyError(key)
            
            entry = self._cache[key]
            if entry.is_expired():
                del self._cache[key]
                raise KeyError(key)
            
            if not isinstance(entry.value, (int, float)):
                raise ValueError(f"Value is not a number: {type(entry.value)}")
            
            entry.value += delta
            self._cache.move_to_end(key)
            entry.touch()
            
            return int(entry.value)
    
    def decr(self, key: str, delta: int = 1) -> int:
        """减少数值"""
        return self.incr(key, -delta)
    
    def stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息。
        
        Returns:
            统计信息字典，包含：
            - size: 当前条目数
            - max_size: 最大条目数
            - hits: 命中次数
            - misses: 未命中次数
            - hit_rate: 命中率
            - evictions: 淘汰次数
            - expirations: 过期次数
            
        Examples:
            >>> cache.stats()
            {'size': 100, 'hits': 500, 'misses': 50, 'hit_rate': 0.909, ...}
        """
        with self._get_lock():
            total = self._hits + self._misses
            hit_rate = self._hits / total if total > 0 else 0.0
            
            return {
                'size': len(self._cache),
                'max_size': self._max_size,
                'hits': self._hits,
                'misses': self._misses,
                'hit_rate': round(hit_rate, 4),
                'evictions': self._evictions,
                'expirations': self._expirations,
            }
    
    def reset_stats(self) -> None:
        """重置统计信息"""
        with self._get_lock():
            self._hits = 0
            self._misses = 0
            self._evictions = 0
            self._expirations = 0
    
    def __len__(self) -> int:
        return self.size()
    
    def __contains__(self, key: str) -> bool:
        return self.has(key)
    
    def __getitem__(self, key: str) -> Any:
        result = self.get(key)
        if result is None and key not in self._cache:
            raise KeyError(key)
        return result
    
    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)
    
    def __delitem__(self, key: str) -> None:
        if not self.delete(key):
            raise KeyError(key)
    
    def close(self) -> None:
        """关闭缓存，停止后台线程"""
        self._running = False
        self.clear()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


def cached(
    cache: Optional[MemoryCache] = None,
    key_prefix: str = '',
    ttl: Optional[float] = None,
    max_args_length: int = 256,
    skip_args: Optional[List[int]] = None
):
    """
    函数结果缓存装饰器。
    
    Args:
        cache: MemoryCache实例，None则创建新实例
        key_prefix: 缓存键前缀
        ttl: 过期时间
        max_args_length: 参数字符串最大长度
        skip_args: 跳过的参数索引列表
        
    Returns:
        装饰器函数
        
    Examples:
        >>> cache = MemoryCache(default_ttl=60)
        >>> @cached(cache=cache, ttl=30)
        ... def expensive_computation(n):
        ...     return n * n
        >>> expensive_computation(5)  # 第一次计算
        25
        >>> expensive_computation(5)  # 从缓存读取
        25
    """
    _cache = cache or MemoryCache(default_ttl=ttl)
    _skip_args = skip_args or []
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            args_str = str([
                arg for i, arg in enumerate(args) if i not in _skip_args
            ])
            if len(args_str) > max_args_length:
                # 参数太长时使用hash
                args_str = hashlib.md5(args_str.encode()).hexdigest()
            
            kwargs_str = ''
            if kwargs:
                kwargs_str = str(sorted(kwargs.items()))
                if len(kwargs_str) > max_args_length:
                    kwargs_str = hashlib.md5(kwargs_str.encode()).hexdigest()
            
            cache_key = f"{key_prefix}{func.__name__}:{args_str}:{kwargs_str}"
            
            # 尝试从缓存获取
            result = _cache.get(cache_key)
            if result is not None:
                return result
            
            # 计算结果
            result = func(*args, **kwargs)
            _cache.set(cache_key, result, ttl)
            
            return result
        
        # 添加缓存操作方法
        wrapper.cache = _cache
        wrapper.cache_clear = lambda: _cache.clear()
        wrapper.cache_stats = lambda: _cache.stats()
        
        return wrapper
    
    return decorator


def memoize(
    ttl: Optional[float] = None,
    max_size: int = 128
):
    """
    简化的函数记忆装饰器。
    
    Args:
        ttl: 过期时间
        max_size: 最大缓存数
        
    Returns:
        装饰器函数
        
    Examples:
        >>> @memoize(ttl=60)
        ... def fibonacci(n):
        ...     if n < 2:
        ...         return n
        ...     return fibonacci(n-1) + fibonacci(n-2)
        >>> fibonacci(40)  # 会很快，因为结果被缓存
    """
    cache = MemoryCache(max_size=max_size, default_ttl=ttl)
    return cached(cache=cache)


class TimedCache:
    """
    基于时间的缓存，适合存储带时间戳的数据。
    
    每个条目根据访问时间自动更新过期时间。
    
    Examples:
        >>> cache = TimedCache(window=3600)  # 1小时窗口
        >>> cache.set("user:1", {"name": "Alice"})
        >>> cache.get("user:1")
        {'name': 'Alice'}
    """
    
    def __init__(self, window: float, max_size: int = 0):
        """
        Args:
            window: 时间窗口（秒）
            max_size: 最大条目数
        """
        self._cache = MemoryCache(
            max_size=max_size,
            default_ttl=window,
            thread_safe=True
        )
        self._window = window
    
    def get(self, key: str, default: Any = None, refresh: bool = True) -> Any:
        """
        获取值，可选刷新过期时间。
        
        Args:
            key: 缓存键
            default: 默认值
            refresh: 是否刷新过期时间
        """
        if refresh:
            self._cache.touch(key, new_ttl=self._window)
        return self._cache.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """设置值"""
        self._cache.set(key, value, ttl=self._window)
    
    def has(self, key: str) -> bool:
        return self._cache.has(key)
    
    def delete(self, key: str) -> bool:
        return self._cache.delete(key)
    
    def clear(self) -> None:
        self._cache.clear()
    
    def stats(self) -> Dict[str, Any]:
        return self._cache.stats()


class RateLimiter:
    """
    基于缓存的速率限制器。
    
    Examples:
        >>> limiter = RateLimiter(max_requests=100, window=60)  # 60秒100次
        >>> if limiter.allow("user:123"):
        ...     print("Request allowed")
        ... else:
        ...     print("Rate limit exceeded")
    """
    
    def __init__(
        self,
        max_requests: int,
        window: float,
        cleanup_interval: float = 60
    ):
        """
        Args:
            max_requests: 时间窗口内最大请求数
            window: 时间窗口（秒）
            cleanup_interval: 清理间隔
        """
        self._max_requests = max_requests
        self._window = window
        self._cache = MemoryCache(
            default_ttl=window,
            cleanup_interval=cleanup_interval
        )
    
    def allow(self, key: str) -> bool:
        """
        检查是否允许请求。
        
        Args:
            key: 标识符（如用户ID、IP地址）
            
        Returns:
            是否允许
        """
        count_key = f"count:{key}"
        
        try:
            count = self._cache.incr(count_key)
        except KeyError:
            count = 1
            self._cache.set(count_key, 1, ttl=self._window)
        
        return count <= self._max_requests
    
    def remaining(self, key: str) -> int:
        """
        获取剩余请求次数。
        
        Args:
            key: 标识符
            
        Returns:
            剩余次数
        """
        count_key = f"count:{key}"
        count = self._cache.get(count_key, 0)
        return max(0, self._max_requests - count)
    
    def reset(self, key: str) -> None:
        """
        重置计数。
        
        Args:
            key: 标识符
        """
        count_key = f"count:{key}"
        self._cache.delete(count_key)
    
    def stats(self) -> Dict[str, Any]:
        return self._cache.stats()


# 版本信息
__version__ = '1.0.0'
__author__ = 'AllToolkit'
__all__ = [
    'MemoryCache',
    'CacheEntry',
    'cached',
    'memoize',
    'TimedCache',
    'RateLimiter',
]