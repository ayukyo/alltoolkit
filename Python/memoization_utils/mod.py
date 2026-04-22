"""
Memoization Utils - 函数结果缓存工具

提供零依赖的记忆化（缓存）功能，优化函数性能。
支持 TTL、LRU 策略、线程安全和自定义键生成。

Author: AllToolkit
Date: 2026-04-23
"""

import time
import threading
import hashlib
from functools import wraps
from collections import OrderedDict
from typing import Any, Callable, Optional, Dict, Tuple, Union


class CacheEntry:
    """缓存条目"""
    
    __slots__ = ['value', 'expire_at', 'access_count']
    
    def __init__(self, value: Any, expire_at: Optional[float] = None):
        self.value = value
        self.expire_at = expire_at
        self.access_count = 0
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.expire_at is None:
            return False
        return time.time() > self.expire_at
    
    def touch(self):
        """增加访问计数"""
        self.access_count += 1


class MemoCache:
    """
    记忆化缓存
    
    特性：
    - LRU 淘汰策略
    - TTL 过期支持
    - 线程安全
    - 统计信息
    """
    
    def __init__(
        self, 
        max_size: int = 128,
        ttl: Optional[float] = None,
        thread_safe: bool = True
    ):
        """
        初始化缓存
        
        Args:
            max_size: 最大缓存条目数
            ttl: 生存时间（秒），None 表示永不过期
            thread_safe: 是否线程安全
        """
        self.max_size = max_size
        self.ttl = ttl
        self.thread_safe = thread_safe
        self._cache: OrderedDict = OrderedDict()
        self._lock = threading.RLock() if thread_safe else None
        
        # 统计信息
        self.hits = 0
        self.misses = 0
    
    def _get_key_hash(self, args: tuple, kwargs: dict) -> str:
        """生成缓存键哈希"""
        key_str = f"{args}{sorted(kwargs.items())}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _cleanup_expired(self):
        """清理过期条目"""
        if not self._cache:
            return
        
        expired_keys = [
            k for k, v in self._cache.items() 
            if v.is_expired()
        ]
        for k in expired_keys:
            del self._cache[k]
    
    def _evict_lru(self):
        """LRU 淘汰"""
        while len(self._cache) >= self.max_size:
            # 移除最旧的条目
            self._cache.popitem(last=False)
    
    def get(self, args: tuple, kwargs: dict) -> Tuple[bool, Any]:
        """
        获取缓存值
        
        Args:
            args: 位置参数
            kwargs: 关键字参数
        
        Returns:
            (found, value) 元组
        """
        def _get_impl():
            key = self._get_key_hash(args, kwargs)
            
            if key not in self._cache:
                self.misses += 1
                return (False, None)
            
            entry = self._cache[key]
            
            if entry.is_expired():
                del self._cache[key]
                self.misses += 1
                return (False, None)
            
            # 移到最后（最近使用）
            self._cache.move_to_end(key)
            entry.touch()
            self.hits += 1
            return (True, entry.value)
        
        if self.thread_safe and self._lock:
            with self._lock:
                return _get_impl()
        return _get_impl()
    
    def set(self, args: tuple, kwargs: dict, value: Any, ttl: Optional[float] = None):
        """
        设置缓存值
        
        Args:
            args: 位置参数
            kwargs: 关键字参数
            value: 缓存值
            ttl: 生存时间，覆盖默认值
        """
        def _set_impl():
            key = self._get_key_hash(args, kwargs)
            actual_ttl = ttl if ttl is not None else self.ttl
            
            expire_at = None
            if actual_ttl is not None:
                expire_at = time.time() + actual_ttl
            
            # 如果键已存在，先删除
            if key in self._cache:
                del self._cache[key]
            else:
                # 需要淘汰
                self._evict_lru()
            
            self._cache[key] = CacheEntry(value, expire_at)
        
        if self.thread_safe and self._lock:
            with self._lock:
                _set_impl()
        else:
            _set_impl()
    
    def clear(self):
        """清空缓存"""
        if self.thread_safe and self._lock:
            with self._lock:
                self._cache.clear()
                self.hits = 0
                self.misses = 0
        else:
            self._cache.clear()
            self.hits = 0
            self.misses = 0
    
    def cleanup(self):
        """手动清理过期条目"""
        if self.thread_safe and self._lock:
            with self._lock:
                self._cleanup_expired()
        else:
            self._cleanup_expired()
    
    @property
    def size(self) -> int:
        """当前缓存大小"""
        return len(self._cache)
    
    @property
    def hit_rate(self) -> float:
        """命中率"""
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total
    
    def stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'size': self.size,
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{self.hit_rate:.2%}",
            'ttl': self.ttl
        }


def memoize(
    max_size: int = 128,
    ttl: Optional[float] = None,
    thread_safe: bool = True,
    key_func: Optional[Callable] = None
):
    """
    记忆化装饰器
    
    缓存函数结果，提高性能。
    
    Args:
        max_size: 最大缓存条目数
        ttl: 生存时间（秒）
        thread_safe: 是否线程安全
        key_func: 自定义键生成函数 (args, kwargs) -> str
    
    Returns:
        装饰器函数
    
    Examples:
        >>> @memoize(max_size=256, ttl=60)
        ... def expensive_calculation(n):
        ...     return sum(range(n))
        
        >>> @memoize(key_func=lambda a, b, **kw: f"{a}-{b}")
        ... def combine(a, b):
        ...     return a + b
    """
    def decorator(func: Callable) -> Callable:
        cache = MemoCache(max_size=max_size, ttl=ttl, thread_safe=thread_safe)
        _key_func = key_func
        
        # 用于防止重复计算的锁
        compute_locks: Dict[str, threading.Lock] = {}
        locks_lock = threading.Lock() if thread_safe else None
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 检查缓存
            found, value = cache.get(args, kwargs)
            if found:
                return value
            
            # 获取或创建计算锁
            key = cache._get_key_hash(args, kwargs)
            if locks_lock:
                with locks_lock:
                    if key not in compute_locks:
                        compute_locks[key] = threading.Lock()
                    compute_lock = compute_locks[key]
            else:
                compute_lock = compute_locks.get(key)
                if compute_lock is None:
                    compute_locks[key] = threading.Lock()
                    compute_lock = compute_locks[key]
            
            # 使用锁防止重复计算
            with compute_lock:
                # 双重检查
                found, value = cache.get(args, kwargs)
                if found:
                    return value
                
                # 计算并缓存
                result = func(*args, **kwargs)
                cache.set(args, kwargs, result)
                return result
        
        # 暴露缓存接口
        wrapper.cache = cache
        wrapper.cache_clear = cache.clear
        wrapper.cache_stats = cache.stats
        
        return wrapper
    
    return decorator


def memoize_method(
    max_size: int = 128,
    ttl: Optional[float] = None,
    thread_safe: bool = True
):
    """
    方法记忆化装饰器
    
    专为类方法设计，正确处理 self/cls 参数。
    
    Args:
        max_size: 最大缓存条目数
        ttl: 生存时间（秒）
        thread_safe: 是否线程安全
    
    Returns:
        装饰器函数
    
    Examples:
        >>> class Calculator:
        ...     @memoize_method(max_size=64)
        ...     def fibonacci(self, n):
        ...         if n <= 1:
        ...             return n
        ...         return self.fibonacci(n-1) + self.fibonacci(n-2)
    """
    def decorator(func: Callable) -> Callable:
        # 每个实例一个缓存
        caches: Dict[int, MemoCache] = {}
        lock = threading.Lock() if thread_safe else None
        
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            instance_id = id(self)
            
            # 获取或创建实例缓存
            if instance_id not in caches:
                cache = MemoCache(max_size=max_size, ttl=ttl, thread_safe=thread_safe)
                if lock:
                    with lock:
                        if instance_id not in caches:
                            caches[instance_id] = cache
                else:
                    caches[instance_id] = cache
            
            cache = caches[instance_id]
            
            # 检查缓存
            found, value = cache.get(args, kwargs)
            if found:
                return value
            
            # 计算并缓存
            result = func(self, *args, **kwargs)
            cache.set(args, kwargs, result)
            return result
        
        return wrapper
    
    return decorator


class MemoizedFunction:
    """
    可记忆化的函数类
    
    提供更细粒度的控制。
    
    Examples:
        >>> @MemoizedFunction(ttl=30)
        ... def fetch_data(url):
        ...     return requests.get(url).text
        ...
        >>> result = fetch_data("https://example.com")
        >>> fetch_data.cache_stats()
    """
    
    def __init__(
        self,
        func: Optional[Callable] = None,
        *,
        max_size: int = 128,
        ttl: Optional[float] = None,
        thread_safe: bool = True
    ):
        """
        初始化
        
        Args:
            func: 要包装的函数
            max_size: 最大缓存条目数
            ttl: 生存时间
            thread_safe: 是否线程安全
        """
        self.max_size = max_size
        self.ttl = ttl
        self.thread_safe = thread_safe
        self.cache = MemoCache(max_size, ttl, thread_safe)
        self._func = func
    
    def __call__(self, *args, **kwargs):
        """调用函数或作为装饰器"""
        # 如果没有函数且只传入一个可调用参数，作为装饰器使用
        if self._func is None and len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            self._func = args[0]
            return self
        
        if self._func is None:
            raise RuntimeError("No function to call")
        
        found, value = self.cache.get(args, kwargs)
        if found:
            return value
        
        result = self._func(*args, **kwargs)
        self.cache.set(args, kwargs, result)
        return result
    
    def __get__(self, obj, objtype=None):
        """支持作为方法使用"""
        if obj is None:
            return self
        return lambda *args, **kwargs: self(obj, *args, **kwargs)
    
    def wrap(self, func: Callable) -> 'MemoizedFunction':
        """包装函数"""
        self._func = func
        return self


def lru_cache(max_size: int = 128):
    """
    简化的 LRU 缓存装饰器
    
    Args:
        max_size: 最大缓存条目数
    
    Examples:
        >>> @lru_cache(100)
        ... def factorial(n):
        ...     return 1 if n <= 1 else n * factorial(n-1)
    """
    return memoize(max_size=max_size, ttl=None)


def ttl_cache(ttl: float, max_size: int = 128):
    """
    TTL 缓存装饰器
    
    Args:
        ttl: 生存时间（秒）
        max_size: 最大缓存条目数
    
    Examples:
        >>> @ttl_cache(ttl=60)
        ... def get_current_time():
        ...     return time.time()
    """
    return memoize(max_size=max_size, ttl=ttl, thread_safe=True)


def cached_property(func: Callable) -> property:
    """
    缓存属性装饰器
    
    缓存计算结果，类似于 functools.cached_property。
    
    Examples:
        >>> class DataProcessor:
        ...     @cached_property
        ...     def expensive_data(self):
        ...         return [i**2 for i in range(1000)]
    """
    attr_name = f"_cached_{func.__name__}"
    
    @property
    @wraps(func)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    
    return wrapper


def expire_after(seconds: float):
    """
    定时过期装饰器
    
    在指定时间后自动清理缓存。
    
    Args:
        seconds: 过期时间
    
    Examples:
        >>> @expire_after(300)  # 5分钟后过期
        ... def load_config():
        ...     return {"key": "value"}
    """
    return memoize(ttl=seconds, max_size=1)


# 导出
__all__ = [
    'MemoCache',
    'memoize',
    'memoize_method',
    'MemoizedFunction',
    'lru_cache',
    'ttl_cache',
    'cached_property',
    'expire_after',
]