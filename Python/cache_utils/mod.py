"""
cache_utils - 轻量级内存缓存工具模块

提供零外部依赖的内存缓存实现，支持：
- TTL (Time To Live) 过期
- LRU (Least Recently Used) 淘汰策略
- 最大容量限制
- 缓存统计（命中/未命中/淘汰）
- 线程安全操作
- 装饰器模式缓存函数结果

作者: AllToolkit 自动化开发
日期: 2026-04-17
"""

import time
import threading
from collections import OrderedDict
from typing import Any, Callable, Optional, Dict, List, Tuple, TypeVar, Generic
from functools import wraps
from hashlib import sha256
import pickle

K = TypeVar('K')
V = TypeVar('V')


class CacheStats:
    """缓存统计信息"""
    
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expirations = 0
        self._lock = threading.Lock()
    
    def record_hit(self):
        with self._lock:
            self.hits += 1
    
    def record_miss(self):
        with self._lock:
            self.misses += 1
    
    def record_eviction(self):
        with self._lock:
            self.evictions += 1
    
    def record_expiration(self):
        with self._lock:
            self.expirations += 1
    
    @property
    def total_requests(self) -> int:
        return self.hits + self.misses
    
    @property
    def hit_rate(self) -> float:
        total = self.total_requests
        return self.hits / total if total > 0 else 0.0
    
    def reset(self):
        with self._lock:
            self.hits = 0
            self.misses = 0
            self.evictions = 0
            self.expirations = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'expirations': self.expirations,
            'total_requests': self.total_requests,
            'hit_rate': round(self.hit_rate, 4)
        }
    
    def __repr__(self) -> str:
        return (f"CacheStats(hits={self.hits}, misses={self.misses}, "
                f"hit_rate={self.hit_rate:.2%}, evictions={self.evictions}, "
                f"expirations={self.expirations})")


class CacheEntry(Generic[V]):
    """缓存条目"""
    
    __slots__ = ['value', 'created_at', 'expires_at', 'access_count', 'last_access']
    
    def __init__(self, value: V, ttl: Optional[float] = None):
        self.value = value
        self.created_at = time.time()
        self.expires_at = self.created_at + ttl if ttl else None
        self.access_count = 0
        self.last_access = self.created_at
    
    def touch(self):
        """更新访问时间和计数"""
        self.last_access = time.time()
        self.access_count += 1
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def remaining_ttl(self) -> Optional[float]:
        """返回剩余 TTL 秒数"""
        if self.expires_at is None:
            return None
        remaining = self.expires_at - time.time()
        return max(0, remaining)
    
    def __repr__(self) -> str:
        return f"CacheEntry(value={self.value!r}, ttl={self.remaining_ttl()})"


class MemoryCache(Generic[K, V]):
    """
    内存缓存实现
    
    特性：
    - 支持 TTL 过期
    - 支持 LRU 淘汰策略
    - 支持最大容量限制
    - 线程安全
    - 提供统计信息
    
    示例:
        cache = MemoryCache(max_size=1000, default_ttl=300)
        cache.set('key', 'value')
        value = cache.get('key')
    """
    
    def __init__(
        self,
        max_size: int = 1000,
        default_ttl: Optional[float] = None,
        thread_safe: bool = True
    ):
        """
        初始化缓存
        
        Args:
            max_size: 最大缓存条目数
            default_ttl: 默认 TTL（秒），None 表示永不过期
            thread_safe: 是否启用线程安全
        """
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._thread_safe = thread_safe
        self._cache: OrderedDict[K, CacheEntry[V]] = OrderedDict()
        self._stats = CacheStats()
        self._lock = threading.RLock() if thread_safe else None
    
    def _get_lock(self):
        """获取锁上下文"""
        if self._lock:
            return self._lock
        return _DummyLock()
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """
        获取缓存值
        
        Args:
            key: 缓存键
            default: 未找到时的默认值
        
        Returns:
            缓存值或默认值
        """
        with self._get_lock():
            entry = self._cache.get(key)
            
            if entry is None:
                self._stats.record_miss()
                return default
            
            if entry.is_expired():
                del self._cache[key]
                self._stats.record_expiration()
                self._stats.record_miss()
                return default
            
            # LRU: 移到末尾（最近使用）
            self._cache.move_to_end(key)
            entry.touch()
            self._stats.record_hit()
            return entry.value
    
    def set(
        self,
        key: K,
        value: V,
        ttl: Optional[float] = None
    ) -> None:
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒），None 使用默认 TTL
        """
        with self._get_lock():
            # 如果键已存在，先删除
            if key in self._cache:
                del self._cache[key]
            
            # 检查容量，执行 LRU 淘汰
            while len(self._cache) >= self._max_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
                self._stats.record_eviction()
            
            # 添加新条目
            effective_ttl = ttl if ttl is not None else self._default_ttl
            self._cache[key] = CacheEntry(value, effective_ttl)
    
    def delete(self, key: K) -> bool:
        """
        删除缓存条目
        
        Args:
            key: 缓存键
        
        Returns:
            是否成功删除
        """
        with self._get_lock():
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def exists(self, key: K) -> bool:
        """检查键是否存在且未过期"""
        with self._get_lock():
            entry = self._cache.get(key)
            if entry is None:
                return False
            if entry.is_expired():
                del self._cache[key]
                self._stats.record_expiration()
                return False
            return True
    
    def clear(self) -> None:
        """清空缓存"""
        with self._get_lock():
            self._cache.clear()
    
    def size(self) -> int:
        """返回当前缓存大小"""
        with self._get_lock():
            return len(self._cache)
    
    def cleanup_expired(self) -> int:
        """
        清理所有过期条目
        
        Returns:
            清理的条目数
        """
        with self._get_lock():
            # 优化：使用 dict comprehension 重建非过期条目，避免逐个删除开销
            # 对于大量过期条目场景，重建字典比逐个删除更高效
            current_time = time.time()
            valid_keys = set()
            
            for key, entry in self._cache.items():
                if entry.expires_at is None or current_time <= entry.expires_at:
                    valid_keys.add(key)
            
            expired_count = len(self._cache) - len(valid_keys)
            
            if expired_count > 0:
                # 只有有过期条目时才重建
                self._cache = OrderedDict(
                    (k, self._cache[k]) for k in valid_keys
                )
                # 更新统计
                for _ in range(expired_count):
                    self._stats.record_expiration()
            
            return expired_count
    
    def get_or_set(
        self,
        key: K,
        factory: Callable[[], V],
        ttl: Optional[float] = None
    ) -> V:
        """
        获取缓存值，如果不存在则使用工厂函数创建并缓存
        
        Args:
            key: 缓存键
            factory: 值工厂函数
            ttl: 过期时间
        
        Returns:
            缓存值或新创建的值
        """
        with self._get_lock():
            value = self.get(key)
            if value is not None:
                return value
            
            new_value = factory()
            self.set(key, new_value, ttl)
            return new_value
    
    def get_stats(self) -> CacheStats:
        """获取统计信息"""
        return self._stats
    
    def get_all_keys(self) -> List[K]:
        """获取所有键（不包括过期的）"""
        with self._get_lock():
            self.cleanup_expired()
            return list(self._cache.keys())
    
    def get_entries_info(self) -> List[Dict[str, Any]]:
        """获取所有条目的详细信息"""
        with self._get_lock():
            self.cleanup_expired()
            result = []
            for key, entry in self._cache.items():
                result.append({
                    'key': str(key),
                    'created_at': entry.created_at,
                    'last_access': entry.last_access,
                    'access_count': entry.access_count,
                    'remaining_ttl': entry.remaining_ttl()
                })
            return result
    
    def __len__(self) -> int:
        return self.size()
    
    def __contains__(self, key: K) -> bool:
        return self.exists(key)
    
    def __getitem__(self, key: K) -> V:
        result = self.get(key)
        if result is None:
            raise KeyError(key)
        return result
    
    def __setitem__(self, key: K, value: V):
        self.set(key, value)
    
    def __delitem__(self, key: K):
        if not self.delete(key):
            raise KeyError(key)
    
    def __repr__(self) -> str:
        return f"MemoryCache(size={self.size()}, max_size={self._max_size})"


class _DummyLock:
    """空锁，用于非线程安全模式"""
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass


def cached(
    ttl: Optional[float] = None,
    max_size: int = 1000,
    key_prefix: str = '',
    key_builder: Optional[Callable[..., str]] = None
):
    """
    函数结果缓存装饰器
    
    Args:
        ttl: 缓存时间（秒）
        max_size: 最大缓存条目数
        key_prefix: 缓存键前缀
        key_builder: 自定义键构建函数
    
    示例:
        @cached(ttl=60)
        def expensive_function(n):
            return n * n
    """
    cache = MemoryCache(max_size=max_size, default_ttl=ttl)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 构建缓存键
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                # 默认键构建：基于参数哈希
                key_data = pickle.dumps((args, sorted(kwargs.items())))
                cache_key = key_prefix + sha256(key_data).hexdigest()[:16]
            
            return cache.get_or_set(cache_key, lambda: func(*args, **kwargs))
        
        # 暴露缓存供外部访问
        wrapper.cache = cache
        wrapper.cache_clear = cache.clear
        wrapper.cache_stats = cache.get_stats
        
        return wrapper
    
    return decorator


class TimedCache:
    """
    基于时间窗口的缓存
    
    在指定时间窗口内缓存结果，窗口结束后自动刷新。
    适用于定时数据同步场景。
    """
    
    def __init__(self, window_seconds: float = 60.0):
        """
        Args:
            window_seconds: 时间窗口（秒）
        """
        self._window = window_seconds
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._lock = threading.Lock()
    
    def get_or_refresh(
        self,
        key: str,
        refresh_func: Callable[[], Any]
    ) -> Any:
        """
        获取值，如果过期则刷新
        
        Args:
            key: 缓存键
            refresh_func: 刷新函数
        
        Returns:
            缓存值或刷新后的值
        """
        with self._lock:
            now = time.time()
            cached = self._cache.get(key)
            
            if cached is None or (now - cached[1]) > self._window:
                value = refresh_func()
                self._cache[key] = (value, now)
                return value
            
            return cached[0]
    
    def invalidate(self, key: str) -> bool:
        """使指定键失效"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self):
        """清空所有缓存"""
        with self._lock:
            self._cache.clear()


class MultiLevelCache:
    """
    多级缓存
    
    实现本地缓存 + 可选远程缓存的分层架构。
    支持 L1（本地）和 L2（远程，需自定义）两级缓存。
    """
    
    def __init__(
        self,
        l1_size: int = 1000,
        l1_ttl: Optional[float] = 300
    ):
        """
        Args:
            l1_size: L1 缓存大小
            l1_ttl: L1 缓存 TTL
        """
        self._l1 = MemoryCache(max_size=l1_size, default_ttl=l1_ttl)
        self._l2_get: Optional[Callable[[str], Any]] = None
        self._l2_set: Optional[Callable[[str, Any, Optional[float]], None]] = None
        self._l2_delete: Optional[Callable[[str], bool]] = None
    
    def set_l2_handlers(
        self,
        get_handler: Callable[[str], Any],
        set_handler: Callable[[str, Any, Optional[float]], None],
        delete_handler: Optional[Callable[[str], bool]] = None
    ):
        """设置 L2 缓存处理器"""
        self._l2_get = get_handler
        self._l2_set = set_handler
        self._l2_delete = delete_handler
    
    def get(self, key: str, default: Any = None) -> Any:
        """从缓存获取值"""
        # 先查 L1
        value = self._l1.get(key)
        if value is not None:
            return value
        
        # 再查 L2
        if self._l2_get:
            value = self._l2_get(key)
            if value is not None:
                # 回填 L1
                self._l1.set(key, value)
                return value
        
        return default
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None):
        """设置缓存"""
        self._l1.set(key, value, ttl)
        if self._l2_set:
            self._l2_set(key, value, ttl)
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        l1_deleted = self._l1.delete(key)
        l2_deleted = False
        if self._l2_delete:
            l2_deleted = self._l2_delete(key)
        return l1_deleted or l2_deleted
    
    def get_l1_stats(self) -> CacheStats:
        """获取 L1 缓存统计"""
        return self._l1.get_stats()


class CacheManager:
    """
    缓存管理器
    
    管理多个命名缓存实例。
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._caches: Dict[str, MemoryCache] = {}
                    cls._instance._cache_lock = threading.Lock()
        return cls._instance
    
    def get_cache(
        self,
        name: str,
        max_size: int = 1000,
        default_ttl: Optional[float] = None
    ) -> MemoryCache:
        """
        获取或创建命名缓存
        
        Args:
            name: 缓存名称
            max_size: 最大大小
            default_ttl: 默认 TTL
        
        Returns:
            缓存实例
        """
        with self._cache_lock:
            if name not in self._caches:
                self._caches[name] = MemoryCache(
                    max_size=max_size,
                    default_ttl=default_ttl
                )
            return self._caches[name]
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """获取所有缓存的统计信息"""
        with self._cache_lock:
            return {
                name: cache.get_stats().to_dict()
                for name, cache in self._caches.items()
            }
    
    def clear_all(self):
        """清空所有缓存"""
        with self._cache_lock:
            for cache in self._caches.values():
                cache.clear()
    
    def remove_cache(self, name: str) -> bool:
        """删除命名缓存"""
        with self._cache_lock:
            if name in self._caches:
                del self._caches[name]
                return True
            return False


# 便捷函数
def create_cache(max_size: int = 1000, ttl: Optional[float] = None) -> MemoryCache:
    """创建缓存的便捷函数"""
    return MemoryCache(max_size=max_size, default_ttl=ttl)


if __name__ == '__main__':
    # 简单测试
    print("=== Cache Utils 测试 ===\n")
    
    # 基本用法
    cache = MemoryCache(max_size=3)
    cache.set('a', 1)
    cache.set('b', 2)
    cache.set('c', 3)
    print(f"缓存内容: {cache.get_all_keys()}")
    
    # LRU 淘汰测试
    cache.set('d', 4)  # 应该淘汰 'a'
    print(f"添加 'd' 后: {cache.get_all_keys()}")
    
    # TTL 测试
    ttl_cache = MemoryCache(default_ttl=1)
    ttl_cache.set('temp', 'will expire')
    print(f"临时值: {ttl_cache.get('temp')}")
    time.sleep(1.1)
    print(f"1秒后: {ttl_cache.get('temp')}")
    
    # 统计信息
    stats = cache.get_stats()
    print(f"\n统计: {stats}")
    
    # 装饰器测试
    @cached(ttl=10)
    def compute(n):
        print(f"  计算 {n}^2...")
        return n * n
    
    print(f"\n第一次调用: {compute(5)}")
    print(f"第二次调用 (缓存): {compute(5)}")
    
    print("\n=== 测试完成 ===")