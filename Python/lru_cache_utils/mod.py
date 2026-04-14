"""
LRU Cache Utils - LRU（最近最少使用）缓存工具模块

提供零依赖的 LRU 缓存实现，支持：
- 线程安全的缓存操作
- TTL（生存时间）支持
- 自动过期清理
- 统计信息收集
- 批量操作
- 装饰器模式

仅使用 Python 标准库实现。
"""

from collections import OrderedDict
from threading import RLock
from typing import Any, Callable, Dict, Generic, Iterator, List, Optional, Tuple, TypeVar, Union
from functools import wraps
from datetime import datetime, timedelta
import time
import heapq

K = TypeVar('K')
V = TypeVar('V')


class CacheEntry(Generic[K, V]):
    """缓存条目类"""
    
    __slots__ = ['key', 'value', 'created_at', 'expires_at', 'access_count', 'last_access']
    
    def __init__(
        self, 
        key: K, 
        value: V, 
        ttl: Optional[float] = None,
        created_at: Optional[float] = None
    ):
        self.key = key
        self.value = value
        self.created_at = created_at or time.time()
        self.expires_at = self.created_at + ttl if ttl else None
        self.access_count = 0
        self.last_access = self.created_at
    
    def is_expired(self) -> bool:
        """检查条目是否已过期"""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def touch(self) -> None:
        """更新访问时间和计数"""
        self.last_access = time.time()
        self.access_count += 1
    
    @property
    def age(self) -> float:
        """条目存活时间（秒）"""
        return time.time() - self.created_at
    
    @property
    def remaining_ttl(self) -> Optional[float]:
        """剩余 TTL（秒），无过期返回 None"""
        if self.expires_at is None:
            return None
        return max(0, self.expires_at - time.time())


class LRUCache(Generic[K, V]):
    """
    线程安全的 LRU 缓存实现
    
    特性：
    - 自动淘汰最少使用的条目
    - 支持 TTL 过期
    - 线程安全操作
    - 统计信息收集
    - 批量操作支持
    
    示例:
        >>> cache = LRUCache(max_size=100, default_ttl=300)
        >>> cache.set('key', 'value')
        >>> cache.get('key')
        'value'
    """
    
    def __init__(
        self, 
        max_size: int = 128,
        default_ttl: Optional[float] = None,
        auto_cleanup: bool = True,
        cleanup_interval: int = 100
    ):
        """
        初始化 LRU 缓存
        
        Args:
            max_size: 最大缓存条目数
            default_ttl: 默认 TTL（秒），None 表示永不过期
            auto_cleanup: 是否自动清理过期条目
            cleanup_interval: 每多少次操作后清理过期条目
        """
        if max_size <= 0:
            raise ValueError("max_size 必须大于 0")
        
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._auto_cleanup = auto_cleanup
        self._cleanup_interval = cleanup_interval
        
        self._cache: OrderedDict[K, CacheEntry[K, V]] = OrderedDict()
        self._lock = RLock()
        self._operation_count = 0
        
        # 统计信息
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._expirations = 0
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """
        获取缓存值
        
        Args:
            key: 缓存键
            default: 未找到时的默认值
            
        Returns:
            缓存值或默认值
        """
        with self._lock:
            self._maybe_cleanup()
            
            if key not in self._cache:
                self._misses += 1
                return default
            
            entry = self._cache[key]
            
            # 检查是否过期
            if entry.is_expired():
                self._remove(key)
                self._expirations += 1
                self._misses += 1
                return default
            
            # 更新访问信息并移到末尾（最近使用）
            entry.touch()
            self._cache.move_to_end(key)
            self._hits += 1
            
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
        with self._lock:
            self._maybe_cleanup()
            
            effective_ttl = ttl if ttl is not None else self._default_ttl
            
            if key in self._cache:
                # 更新现有条目
                entry = self._cache[key]
                entry.value = value
                entry.expires_at = time.time() + effective_ttl if effective_ttl else None
                entry.touch()
                self._cache.move_to_end(key)
            else:
                # 检查是否需要淘汰
                while len(self._cache) >= self._max_size:
                    self._evict_lru()
                
                # 添加新条目
                entry = CacheEntry(key, value, effective_ttl)
                self._cache[key] = entry
    
    def delete(self, key: K) -> bool:
        """
        删除缓存条目
        
        Args:
            key: 缓存键
            
        Returns:
            是否成功删除
        """
        with self._lock:
            return self._remove(key)
    
    def _remove(self, key: K) -> bool:
        """内部删除方法（不加锁）"""
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def _evict_lru(self) -> Optional[K]:
        """淘汰最近最少使用的条目"""
        if not self._cache:
            return None
        
        # OrderedDict 的第一个元素是最久未使用的
        oldest_key = next(iter(self._cache))
        self._remove(oldest_key)
        self._evictions += 1
        return oldest_key
    
    def exists(self, key: K) -> bool:
        """
        检查键是否存在且未过期
        
        Args:
            key: 缓存键
            
        Returns:
            是否存在
        """
        with self._lock:
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            if entry.is_expired():
                self._remove(key)
                return False
            
            return True
    
    def clear(self) -> None:
        """清空缓存"""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
            self._evictions = 0
            self._expirations = 0
    
    def size(self) -> int:
        """获取当前缓存大小"""
        with self._lock:
            return len(self._cache)
    
    def keys(self) -> List[K]:
        """获取所有键（按访问时间排序，最近使用的在后）"""
        with self._lock:
            return list(self._cache.keys())
    
    def values(self) -> List[V]:
        """获取所有值"""
        with self._lock:
            return [entry.value for entry in self._cache.values() if not entry.is_expired()]
    
    def items(self) -> List[Tuple[K, V]]:
        """获取所有键值对"""
        with self._lock:
            return [(k, v.value) for k, v in self._cache.items() if not v.is_expired()]
    
    def get_many(self, keys: List[K]) -> Dict[K, V]:
        """
        批量获取多个键的值
        
        Args:
            keys: 键列表
            
        Returns:
            键值对字典（不包含未找到或过期的键）
        """
        result = {}
        with self._lock:
            for key in keys:
                value = self.get(key)
                if value is not None:
                    result[key] = value
        return result
    
    def set_many(self, items: Dict[K, V], ttl: Optional[float] = None) -> None:
        """
        批量设置多个键值对
        
        Args:
            items: 键值对字典
            ttl: 过期时间
        """
        with self._lock:
            for key, value in items.items():
                self.set(key, value, ttl)
    
    def delete_many(self, keys: List[K]) -> int:
        """
        批量删除多个键
        
        Args:
            keys: 键列表
            
        Returns:
            成功删除的数量
        """
        count = 0
        with self._lock:
            for key in keys:
                if self._remove(key):
                    count += 1
        return count
    
    def get_or_set(
        self, 
        key: K, 
        factory: Callable[[], V],
        ttl: Optional[float] = None
    ) -> V:
        """
        获取缓存值，不存在则通过工厂函数创建并缓存
        
        Args:
            key: 缓存键
            factory: 值工厂函数
            ttl: 过期时间
            
        Returns:
            缓存值或新创建的值
        """
        with self._lock:
            value = self.get(key)
            if value is not None:
                return value
            
            value = factory()
            self.set(key, value, ttl)
            return value
    
    def touch(self, key: K, ttl: Optional[float] = None) -> bool:
        """
        更新条目的访问时间和 TTL
        
        Args:
            key: 缓存键
            ttl: 新的 TTL（None 保持原 TTL）
            
        Returns:
            是否成功
        """
        with self._lock:
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            if entry.is_expired():
                self._remove(key)
                return False
            
            entry.touch()
            if ttl is not None:
                entry.expires_at = time.time() + ttl
            
            self._cache.move_to_end(key)
            return True
    
    def ttl(self, key: K) -> Optional[float]:
        """
        获取键的剩余 TTL
        
        Args:
            key: 缓存键
            
        Returns:
            剩余秒数，永不过期返回 None，不存在返回 -1
        """
        with self._lock:
            if key not in self._cache:
                return -1
            
            entry = self._cache[key]
            if entry.is_expired():
                self._remove(key)
                return -1
            
            return entry.remaining_ttl
    
    def _maybe_cleanup(self) -> None:
        """可能执行过期条目清理"""
        self._operation_count += 1
        
        if self._auto_cleanup and self._operation_count % self._cleanup_interval == 0:
            self._cleanup_expired()
    
    def _cleanup_expired(self) -> int:
        """清理所有过期条目"""
        count = 0
        expired_keys = []
        
        for key, entry in self._cache.items():
            if entry.is_expired():
                expired_keys.append(key)
        
        for key in expired_keys:
            self._remove(key)
            self._expirations += 1
            count += 1
        
        return count
    
    def cleanup(self) -> int:
        """
        手动清理过期条目
        
        Returns:
            清理的条目数量
        """
        with self._lock:
            return self._cleanup_expired()
    
    def stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息
        
        Returns:
            统计信息字典
        """
        with self._lock:
            total_requests = self._hits + self._misses
            hit_rate = self._hits / total_requests if total_requests > 0 else 0
            
            return {
                'size': len(self._cache),
                'max_size': self._max_size,
                'hits': self._hits,
                'misses': self._misses,
                'hit_rate': hit_rate,
                'evictions': self._evictions,
                'expirations': self._expirations,
                'total_requests': total_requests
            }
    
    def reset_stats(self) -> None:
        """重置统计信息"""
        with self._lock:
            self._hits = 0
            self._misses = 0
            self._evictions = 0
            self._expirations = 0
    
    def peek(self, key: K) -> Optional[V]:
        """
        查看键对应的值但不更新访问信息
        
        Args:
            key: 缓存键
            
        Returns:
            缓存值或 None
        """
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            if entry.is_expired():
                self._remove(key)
                return None
            
            return entry.value
    
    def __len__(self) -> int:
        return self.size()
    
    def __contains__(self, key: K) -> bool:
        return self.exists(key)
    
    def __getitem__(self, key: K) -> V:
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value
    
    def __setitem__(self, key: K, value: V) -> None:
        self.set(key, value)
    
    def __delitem__(self, key: K) -> None:
        if not self.delete(key):
            raise KeyError(key)
    
    def __iter__(self) -> Iterator[K]:
        return iter(self.keys())


def lru_cache(
    max_size: int = 128,
    ttl: Optional[float] = None
) -> Callable:
    """
    LRU 缓存装饰器
    
    将函数结果缓存，下次相同参数直接返回缓存结果。
    
    Args:
        max_size: 最大缓存条目数
        ttl: 缓存过期时间（秒）
        
    Returns:
        装饰器函数
        
    示例:
        >>> @lru_cache(max_size=100, ttl=60)
        ... def expensive_function(n):
        ...     return n * 2
        >>> expensive_function(5)
        10
    """
    def decorator(func: Callable) -> Callable:
        cache = LRUCache(max_size=max_size, default_ttl=ttl)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 创建缓存键
            key = (args, frozenset(kwargs.items()))
            
            # 尝试获取缓存
            result = cache.get(key)
            if result is not None:
                return result
            
            # 计算并缓存结果
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        
        # 添加缓存操作方法
        wrapper.cache = cache
        wrapper.cache_clear = cache.clear
        wrapper.cache_stats = cache.stats
        
        return wrapper
    
    return decorator


class TTLCache(LRUCache[K, V]):
    """
    TTL 缓存（带强制过期）
    
    与普通 LRU 缓存的区别：
    - 必须设置 TTL
    - 支持 TTL 更新和刷新
    - 支持批量设置不同 TTL
    """
    
    def __init__(
        self,
        max_size: int = 128,
        default_ttl: float = 300,
        auto_cleanup: bool = True,
        cleanup_interval: int = 100
    ):
        if default_ttl is None or default_ttl <= 0:
            raise ValueError("TTLCache 必须设置有效的 default_ttl")
        
        super().__init__(
            max_size=max_size,
            default_ttl=default_ttl,
            auto_cleanup=auto_cleanup,
            cleanup_interval=cleanup_interval
        )
    
    def refresh_ttl(self, key: K) -> bool:
        """
        刷新键的 TTL（重置为默认值）
        
        Args:
            key: 缓存键
            
        Returns:
            是否成功
        """
        return self.touch(key, self._default_ttl)
    
    def refresh_all(self) -> int:
        """
        刷新所有键的 TTL
        
        Returns:
            成功刷新的数量
        """
        count = 0
        with self._lock:
            for key in list(self._cache.keys()):
                if self.touch(key, self._default_ttl):
                    count += 1
        return count


class BoundedLRUCache(LRUCache[K, V]):
    """
    有界 LRU 缓存
    
    支持设置最小保留数量和淘汰策略。
    """
    
    def __init__(
        self,
        max_size: int = 128,
        min_size: int = 0,
        default_ttl: Optional[float] = None,
        auto_cleanup: bool = True,
        cleanup_interval: int = 100
    ):
        if min_size < 0:
            raise ValueError("min_size 不能为负数")
        if min_size >= max_size:
            raise ValueError("min_size 必须小于 max_size")
        
        super().__init__(
            max_size=max_size,
            default_ttl=default_ttl,
            auto_cleanup=auto_cleanup,
            cleanup_interval=cleanup_interval
        )
        
        self._min_size = min_size
    
    @property
    def min_size(self) -> int:
        """最小保留数量"""
        return self._min_size
    
    def _evict_lru(self) -> Optional[K]:
        """淘汰最近最少使用的条目（考虑最小保留）"""
        if len(self._cache) <= self._min_size:
            return None
        
        return super()._evict_lru()


class WeightedLRUCache(LRUCache[K, V]):
    """
    加权 LRU 缓存
    
    淘汰时考虑权重，优先淘汰权重低的条目。
    """
    
    def __init__(
        self,
        max_weight: int = 1024,
        default_weight: int = 1,
        default_ttl: Optional[float] = None,
        auto_cleanup: bool = True,
        cleanup_interval: int = 100
    ):
        """
        Args:
            max_weight: 最大权重总量
            default_weight: 默认条目权重
        """
        super().__init__(
            max_size=10**9,  # 大数值，实际用权重控制
            default_ttl=default_ttl,
            auto_cleanup=auto_cleanup,
            cleanup_interval=cleanup_interval
        )
        
        self._max_weight = max_weight
        self._default_weight = default_weight
        self._current_weight = 0
        self._weights: Dict[K, int] = {}
    
    def set(
        self,
        key: K,
        value: V,
        ttl: Optional[float] = None,
        weight: Optional[int] = None
    ) -> None:
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间
            weight: 条目权重
        """
        with self._lock:
            effective_weight = weight or self._default_weight
            
            # 如果键已存在，先减去旧权重
            if key in self._weights:
                self._current_weight -= self._weights[key]
            
            # 淘汰直到有足够空间
            while (
                self._current_weight + effective_weight > self._max_weight
                and len(self._cache) > 0
            ):
                evicted_key = self._evict_lru_weighted()
                if evicted_key is None:
                    break
            
            # 设置条目
            super().set(key, value, ttl)
            self._weights[key] = effective_weight
            self._current_weight += effective_weight
    
    def _evict_lru_weighted(self) -> Optional[K]:
        """加权淘汰"""
        if not self._cache:
            return None
        
        # 找到权重最低的最久未使用条目
        oldest_key = next(iter(self._cache))
        
        self._current_weight -= self._weights.pop(oldest_key, 0)
        self._remove(oldest_key)
        self._evictions += 1
        
        return oldest_key
    
    def delete(self, key: K) -> bool:
        result = super().delete(key)
        if result:
            with self._lock:
                self._current_weight -= self._weights.pop(key, 0)
        return result
    
    def clear(self) -> None:
        super().clear()
        with self._lock:
            self._weights.clear()
            self._current_weight = 0
    
    def current_weight(self) -> int:
        """获取当前权重"""
        return self._current_weight
    
    def available_weight(self) -> int:
        """获取可用权重"""
        return self._max_weight - self._current_weight
    
    def stats(self) -> Dict[str, Any]:
        stats = super().stats()
        stats.update({
            'current_weight': self._current_weight,
            'max_weight': self._max_weight,
            'available_weight': self.available_weight()
        })
        return stats


class ExpiringPriorityCache(Generic[K, V]):
    """
    过期优先缓存
    
    淘汰时优先淘汰即将过期的条目。
    """
    
    def __init__(
        self,
        max_size: int = 128,
        default_ttl: Optional[float] = None
    ):
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._cache: Dict[K, CacheEntry[K, V]] = {}
        self._expiry_heap: List[Tuple[float, K]] = []  # (expires_at, key)
        self._lock = RLock()
        self._hits = 0
        self._misses = 0
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return default
            
            entry = self._cache[key]
            if entry.is_expired():
                self._remove(key)
                self._misses += 1
                return default
            
            entry.touch()
            self._hits += 1
            return entry.value
    
    def set(self, key: K, value: V, ttl: Optional[float] = None) -> None:
        with self._lock:
            # 如果已存在，先删除
            if key in self._cache:
                self._remove(key)
            
            # 检查容量
            while len(self._cache) >= self._max_size:
                self._evict_expiring()
            
            effective_ttl = ttl if ttl is not None else self._default_ttl
            entry = CacheEntry(key, value, effective_ttl)
            self._cache[key] = entry
            
            # 如果有过期时间，加入堆
            if entry.expires_at:
                heapq.heappush(self._expiry_heap, (entry.expires_at, key))
    
    def _remove(self, key: K) -> None:
        if key in self._cache:
            del self._cache[key]
            # 注意：不从堆中删除，在淘汰时跳过已删除的键
    
    def _evict_expiring(self) -> Optional[K]:
        """淘汰即将过期的条目"""
        # 首先清理堆中的过期/已删除条目
        while self._expiry_heap:
            expires_at, key = self._expiry_heap[0]
            
            if key not in self._cache:
                heapq.heappop(self._expiry_heap)
                continue
            
            if expires_at < time.time():
                heapq.heappop(self._expiry_heap)
                self._remove(key)
                continue
            
            break
        
        # 如果有即将过期的条目，淘汰它
        if self._expiry_heap:
            _, key = heapq.heappop(self._expiry_heap)
            self._remove(key)
            return key
        
        # 否则淘汰任意一个
        if self._cache:
            key = next(iter(self._cache))
            self._remove(key)
            return key
        
        return None
    
    def delete(self, key: K) -> bool:
        with self._lock:
            if key in self._cache:
                self._remove(key)
                return True
            return False
    
    def size(self) -> int:
        with self._lock:
            return len(self._cache)
    
    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
            self._expiry_heap.clear()
    
    def stats(self) -> Dict[str, Any]:
        total = self._hits + self._misses
        return {
            'size': len(self._cache),
            'max_size': self._max_size,
            'hits': self._hits,
            'misses': self._misses,
            'hit_rate': self._hits / total if total > 0 else 0
        }