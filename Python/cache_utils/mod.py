"""
AllToolkit - Python Cache Utilities

A zero-dependency, production-ready in-memory cache utility module.
Supports TTL expiration, LRU eviction, size limits, and thread-safe operations.

Author: AllToolkit
License: MIT
"""

import time
import threading
from typing import Optional, Any, Dict, List, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from collections import OrderedDict
from functools import wraps


T = TypeVar('T')


@dataclass
class CacheEntry(Generic[T]):
    """Represents a cached item with metadata."""
    value: T
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    
    def is_expired(self) -> bool:
        """Check if this entry has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def touch(self) -> None:
        """Update last accessed time and increment access count."""
        self.last_accessed = time.time()
        self.access_count += 1


class CacheStats:
    """Statistics for cache operations."""
    
    def __init__(self):
        self.hits: int = 0
        self.misses: int = 0
        self.evictions: int = 0
        self.expirations: int = 0
        self.sets: int = 0
        self.deletes: int = 0
        self._lock = threading.Lock()
    
    def record_hit(self) -> None:
        with self._lock:
            self.hits += 1
    
    def record_miss(self) -> None:
        with self._lock:
            self.misses += 1
    
    def record_eviction(self) -> None:
        with self._lock:
            self.evictions += 1
    
    def record_expiration(self) -> None:
        with self._lock:
            self.expirations += 1
    
    def record_set(self) -> None:
        with self._lock:
            self.sets += 1
    
    def record_delete(self) -> None:
        with self._lock:
            self.deletes += 1
    
    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary."""
        return {
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'expirations': self.expirations,
            'sets': self.sets,
            'deletes': self.deletes,
            'hit_rate': self.hit_rate,
            'total_requests': self.hits + self.misses,
        }
    
    def reset(self) -> None:
        """Reset all statistics."""
        with self._lock:
            self.hits = 0
            self.misses = 0
            self.evictions = 0
            self.expirations = 0
            self.sets = 0
            self.deletes = 0
    
    def __str__(self) -> str:
        return (
            f"CacheStats(hits={self.hits}, misses={self.misses}, "
            f"hit_rate={self.hit_rate:.2%}, evictions={self.evictions}, "
            f"expirations={self.expirations})"
        )


class Cache(Generic[T]):
    """
    Thread-safe in-memory cache with TTL and LRU support.
    
    Features:
    - TTL (Time To Live) expiration
    - LRU (Least Recently Used) eviction
    - Maximum size limit
    - Thread-safe operations
    - Statistics tracking
    - Cache warming
    - Bulk operations
    """
    
    def __init__(
        self,
        max_size: int = 1000,
        default_ttl: Optional[float] = None,
        enable_stats: bool = True,
    ):
        """
        Initialize cache.
        
        Args:
            max_size: Maximum number of items (default: 1000)
            default_ttl: Default TTL in seconds (None = no expiration)
            enable_stats: Enable statistics tracking (default: True)
        """
        self._cache: OrderedDict[str, CacheEntry[T]] = OrderedDict()
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._stats = CacheStats() if enable_stats else None
        self._lock = threading.RLock()
    
    def get(self, key: str, default: Optional[T] = None) -> Optional[T]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            default: Default value if key not found or expired
            
        Returns:
            Cached value or default
        """
        with self._lock:
            if key not in self._cache:
                if self._stats:
                    self._stats.record_miss()
                return default
            
            entry = self._cache[key]
            
            # Check expiration
            if entry.is_expired():
                self._delete_internal(key)
                if self._stats:
                    self._stats.record_expiration()
                return default
            
            # Update access info (for LRU)
            entry.touch()
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            
            if self._stats:
                self._stats.record_hit()
            
            return entry.value
    
    def set(
        self,
        key: str,
        value: T,
        ttl: Optional[float] = None,
    ) -> None:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (uses default_ttl if None)
        """
        with self._lock:
            # Calculate expiration time
            expires_at = None
            ttl_to_use = ttl if ttl is not None else self._default_ttl
            if ttl_to_use is not None:
                expires_at = time.time() + ttl_to_use
            
            # If key exists, update and move to end
            if key in self._cache:
                self._cache[key] = CacheEntry(
                    value=value,
                    created_at=self._cache[key].created_at,
                    expires_at=expires_at,
                    access_count=self._cache[key].access_count,
                    last_accessed=time.time(),
                )
                self._cache.move_to_end(key)
            else:
                # Evict if at capacity
                while len(self._cache) >= self._max_size:
                    self._evict_lru()
                
                self._cache[key] = CacheEntry(
                    value=value,
                    expires_at=expires_at,
                )
            
            if self._stats:
                self._stats.record_set()
    
    def delete(self, key: str) -> bool:
        """
        Delete key from cache.
        
        Args:
            key: Cache key to delete
            
        Returns:
            True if key was deleted, False if not found
        """
        with self._lock:
            if key in self._cache:
                self._delete_internal(key)
                if self._stats:
                    self._stats.record_delete()
                return True
            return False
    
    def _delete_internal(self, key: str) -> None:
        """Internal delete without lock (caller must hold lock)."""
        del self._cache[key]
    
    def _evict_lru(self) -> None:
        """Evict least recently used item (caller must hold lock)."""
        if self._cache:
            # First item in OrderedDict is least recently used
            oldest_key = next(iter(self._cache))
            self._delete_internal(oldest_key)
            if self._stats:
                self._stats.record_eviction()
    
    def clear(self) -> None:
        """Clear all items from cache."""
        with self._lock:
            self._cache.clear()
            if self._stats:
                self._stats.record_delete()
    
    def contains(self, key: str) -> bool:
        """
        Check if key exists in cache (without updating access time).
        
        Args:
            key: Cache key
            
        Returns:
            True if key exists and is not expired
        """
        with self._lock:
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            if entry.is_expired():
                self._delete_internal(key)
                if self._stats:
                    self._stats.record_expiration()
                return False
            
            return True
    
    def __contains__(self, key: str) -> bool:
        return self.contains(key)
    
    def __len__(self) -> int:
        with self._lock:
            return len(self._cache)
    
    def __getitem__(self, key: str) -> T:
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value
    
    def __setitem__(self, key: str, value: T) -> None:
        self.set(key, value)
    
    def __delitem__(self, key: str) -> None:
        if not self.delete(key):
            raise KeyError(key)
    
    @property
    def size(self) -> int:
        """Current number of items in cache."""
        return len(self)
    
    @property
    def max_size(self) -> int:
        """Maximum cache size."""
        return self._max_size
    
    @property
    def stats(self) -> Optional[CacheStats]:
        """Get cache statistics."""
        return self._stats
    
    def keys(self) -> List[str]:
        """Get all non-expired keys."""
        with self._lock:
            current_time = time.time()
            return [
                key for key, entry in self._cache.items()
                if entry.expires_at is None or current_time <= entry.expires_at
            ]
    
    def values(self) -> List[T]:
        """Get all non-expired values."""
        with self._lock:
            current_time = time.time()
            return [
                entry.value for key, entry in self._cache.items()
                if entry.expires_at is None or current_time <= entry.expires_at
            ]
    
    def items(self) -> List[Tuple[str, T]]:
        """Get all non-expired key-value pairs."""
        with self._lock:
            current_time = time.time()
            return [
                (key, entry.value) for key, entry in self._cache.items()
                if entry.expires_at is None or current_time <= entry.expires_at
            ]
    
    def get_many(self, keys: List[str]) -> Dict[str, T]:
        """
        Get multiple values from cache.
        
        Args:
            keys: List of cache keys
            
        Returns:
            Dictionary of found key-value pairs
        """
        with self._lock:
            result = {}
            for key in keys:
                if key in self._cache:
                    entry = self._cache[key]
                    if not entry.is_expired():
                        entry.touch()
                        self._cache.move_to_end(key)
                        result[key] = entry.value
                        if self._stats:
                            self._stats.record_hit()
                    else:
                        self._delete_internal(key)
                        if self._stats:
                            self._stats.record_expiration()
                        if self._stats:
                            self._stats.record_miss()
                else:
                    if self._stats:
                        self._stats.record_miss()
            return result
    
    def set_many(self, items: Dict[str, T], ttl: Optional[float] = None) -> None:
        """
        Set multiple values in cache.
        
        Args:
            items: Dictionary of key-value pairs
            ttl: Time to live in seconds
        """
        with self._lock:
            for key, value in items.items():
                self.set(key, value, ttl)
    
    def delete_many(self, keys: List[str]) -> int:
        """
        Delete multiple keys from cache.
        
        Args:
            keys: List of cache keys
            
        Returns:
            Number of keys deleted
        """
        with self._lock:
            count = 0
            for key in keys:
                if self.delete(key):
                    count += 1
            return count
    
    def expire(self) -> int:
        """
        Remove all expired entries.
        
        Optimized to use list comprehension and avoid multiple iterations.
        Returns:
            Number of entries removed
        """
        with self._lock:
            current_time = time.time()
            # 使用列表推导一次性收集所有过期键
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry.expires_at is not None and current_time > entry.expires_at
            ]
            
            # 批量删除
            for key in expired_keys:
                self._delete_internal(key)
                if self._stats:
                    self._stats.record_expiration()
            
            return len(expired_keys)
    
    def ttl(self, key: str) -> Optional[float]:
        """
        Get remaining TTL for a key.
        
        Args:
            key: Cache key
            
        Returns:
            Remaining TTL in seconds, None if no TTL or key not found
        """
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            if entry.expires_at is None:
                return None
            
            remaining = entry.expires_at - time.time()
            if remaining <= 0:
                return 0.0
            
            return remaining
    
    def touch(self, key: str, ttl: Optional[float] = None) -> bool:
        """
        Reset TTL for a key without changing value.
        
        Args:
            key: Cache key
            ttl: New TTL (uses default if None)
            
        Returns:
            True if key was touched, False if not found
        """
        with self._lock:
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            if entry.is_expired():
                self._delete_internal(key)
                return False
            
            ttl_to_use = ttl if ttl is not None else self._default_ttl
            if ttl_to_use is not None:
                entry.expires_at = time.time() + ttl_to_use
            
            entry.touch()
            self._cache.move_to_end(key)
            return True
    
    def increment(self, key: str, amount: int = 1, default: int = 0) -> int:
        """
        Atomically increment a numeric value.
        
        Args:
            key: Cache key
            amount: Amount to increment by
            default: Default value if key doesn't exist
            
        Returns:
            New value after increment
        """
        with self._lock:
            current = self.get(key, default)
            if not isinstance(current, (int, float)):
                current = default
            new_value = current + amount
            self.set(key, new_value)  # Preserve existing TTL
            return new_value
    
    def decrement(self, key: str, amount: int = 1, default: int = 0) -> int:
        """
        Atomically decrement a numeric value.
        
        Args:
            key: Cache key
            amount: Amount to decrement by
            default: Default value if key doesn't exist
            
        Returns:
            New value after decrement
        """
        return self.increment(key, -amount, default)
    
    def get_or_set(
        self,
        key: str,
        factory: Callable[[], T],
        ttl: Optional[float] = None,
    ) -> T:
        """
        Get value from cache or compute and cache it.
        
        Args:
            key: Cache key
            factory: Function to compute value if not cached
            ttl: Time to live in seconds
            
        Returns:
            Cached or computed value
        """
        with self._lock:
            # Try to get existing value
            if key in self._cache:
                entry = self._cache[key]
                if not entry.is_expired():
                    entry.touch()
                    self._cache.move_to_end(key)
                    if self._stats:
                        self._stats.record_hit()
                    return entry.value
                else:
                    self._delete_internal(key)
                    if self._stats:
                        self._stats.record_expiration()
            
            if self._stats:
                self._stats.record_miss()
            
            # Compute and cache new value
            value = factory()
            self.set(key, value, ttl)
            return value
    
    def warm(self, items: Dict[str, T], ttl: Optional[float] = None) -> int:
        """
        Warm cache with initial values (only sets missing keys).
        
        Args:
            items: Dictionary of key-value pairs to warm
            ttl: Time to live in seconds
            
        Returns:
            Number of items actually added
        """
        with self._lock:
            count = 0
            for key, value in items.items():
                if key not in self._cache:
                    self.set(key, value, ttl)
                    count += 1
            return count
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Export cache contents as dictionary.
        
        Returns:
            Dictionary with cache data and metadata
        """
        with self._lock:
            items = {}
            for key, entry in self._cache.items():
                if not entry.is_expired():
                    items[key] = {
                        'value': entry.value,
                        'created_at': entry.created_at,
                        'expires_at': entry.expires_at,
                        'access_count': entry.access_count,
                        'last_accessed': entry.last_accessed,
                        'ttl_remaining': self.ttl(key),
                    }
            
            return {
                'items': items,
                'size': len(items),
                'max_size': self._max_size,
                'default_ttl': self._default_ttl,
                'stats': self._stats.to_dict() if self._stats else None,
            }


# Convenience decorator for memoization

def cached(
    cache: Optional[Cache] = None,
    ttl: Optional[float] = None,
    key_prefix: str = "",
):
    """
    Decorator to cache function results.
    
    Args:
        cache: Cache instance (creates new one if None)
        ttl: Time to live in seconds
        key_prefix: Prefix for cache keys
        
    Returns:
        Decorated function with caching
    """
    _cache = cache if cache is not None else Cache()
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key_parts = [key_prefix, func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)
            
            return _cache.get_or_set(
                cache_key,
                lambda: func(*args, **kwargs),
                ttl=ttl,
            )
        
        wrapper.cache = _cache  # type: ignore
        return wrapper
    
    return decorator


# Module-level convenience functions

_default_cache: Optional[Cache] = None


def get_default_cache() -> Cache:
    """Get or create default cache instance."""
    global _default_cache
    if _default_cache is None:
        _default_cache = Cache()
    return _default_cache


def cache_get(key: str, default: Any = None) -> Any:
    """Get value from default cache."""
    return get_default_cache().get(key, default)


def cache_set(key: str, value: Any, ttl: Optional[float] = None) -> None:
    """Set value in default cache."""
    get_default_cache().set(key, value, ttl)


def cache_delete(key: str) -> bool:
    """Delete key from default cache."""
    return get_default_cache().delete(key)


def cache_clear() -> None:
    """Clear default cache."""
    get_default_cache().clear()
