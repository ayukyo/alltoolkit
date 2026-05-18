"""
LRU Cache Utils - Versatile Least Recently Used Cache Implementations

Provides comprehensive LRU cache utilities with advanced features:
- Thread-safe operations
- TTL (Time-To-Live) support
- Size-based and weight-based eviction
- Statistics and monitoring
- Decorator interface
- Zero external dependencies

Author: AllToolkit
Date: 2026-05-18
"""

import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Hashable,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)
from functools import wraps

K = TypeVar('K', bound=Hashable)
V = TypeVar('V')


@dataclass
class CacheStats:
    """Cache statistics."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expired: int = 0
    inserts: int = 0
    updates: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    @property
    def total_requests(self) -> int:
        """Total cache requests."""
        return self.hits + self.misses
    
    def reset(self) -> None:
        """Reset all statistics."""
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expired = 0
        self.inserts = 0
        self.updates = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'expired': self.expired,
            'inserts': self.inserts,
            'updates': self.updates,
            'hit_rate': self.hit_rate,
            'total_requests': self.total_requests,
        }


@dataclass
class CacheEntry(Generic[V]):
    """A cache entry with metadata."""
    value: V
    created_at: float
    last_accessed: float
    access_count: int = 1
    ttl: Optional[float] = None
    weight: int = 1
    
    @property
    def is_expired(self) -> bool:
        """Check if entry has expired."""
        if self.ttl is None:
            return False
        return time.time() - self.created_at > self.ttl
    
    @property
    def age(self) -> float:
        """Age of entry in seconds."""
        return time.time() - self.created_at
    
    @property
    def idle_time(self) -> float:
        """Time since last access."""
        return time.time() - self.last_accessed


class LRUCache(Generic[K, V]):
    """
    Thread-safe LRU Cache with TTL and weight support.
    
    Examples:
        >>> cache = LRUCache(max_size=100, ttl=300)  # 5-minute TTL
        >>> cache.set('key1', 'value1')
        >>> cache.get('key1')
        'value1'
        >>> cache.delete('key1')
        True
    """
    
    def __init__(
        self,
        max_size: int = 1000,
        ttl: Optional[float] = None,
        max_weight: Optional[int] = None,
        on_evict: Optional[Callable[[K, V], None]] = None,
    ):
        """
        Initialize LRU cache.
        
        Args:
            max_size: Maximum number of entries
            ttl: Default time-to-live in seconds (None = no expiration)
            max_weight: Maximum total weight (None = no weight limit)
            on_evict: Callback when entry is evicted
        """
        self.max_size = max_size
        self.ttl = ttl
        self.max_weight = max_weight
        self.on_evict = on_evict
        
        self._cache: OrderedDict[K, CacheEntry[V]] = OrderedDict()
        self._lock = threading.RLock()
        self._stats = CacheStats()
        self._current_weight = 0
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            default: Default value if not found
        
        Returns:
            Cached value or default
        """
        with self._lock:
            if key not in self._cache:
                self._stats.misses += 1
                return default
            
            entry = self._cache[key]
            
            # Check expiration
            if entry.is_expired:
                self._remove_entry(key)
                self._stats.expired += 1
                self._stats.misses += 1
                return default
            
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            entry.last_accessed = time.time()
            entry.access_count += 1
            self._stats.hits += 1
            
            return entry.value
    
    def set(
        self,
        key: K,
        value: V,
        ttl: Optional[float] = None,
        weight: int = 1,
    ) -> None:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if None)
            weight: Entry weight for weight-based eviction
        """
        with self._lock:
            now = time.time()
            entry_ttl = ttl if ttl is not None else self.ttl
            
            # Update existing entry
            if key in self._cache:
                old_entry = self._cache[key]
                self._current_weight -= old_entry.weight
                self._stats.updates += 1
            
            # Create new entry
            entry = CacheEntry(
                value=value,
                created_at=now,
                last_accessed=now,
                ttl=entry_ttl,
                weight=weight,
            )
            
            self._cache[key] = entry
            self._cache.move_to_end(key)
            self._current_weight += weight
            self._stats.inserts += 1
            
            # Evict if necessary
            self._evict_if_needed()
    
    def delete(self, key: K) -> bool:
        """
        Delete entry from cache.
        
        Returns:
            True if entry was deleted
        """
        with self._lock:
            if key in self._cache:
                self._remove_entry(key)
                return True
            return False
    
    def contains(self, key: K) -> bool:
        """Check if key exists and is not expired."""
        with self._lock:
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            if entry.is_expired:
                self._remove_entry(key)
                self._stats.expired += 1
                return False
            
            return True
    
    def clear(self) -> None:
        """Clear all entries."""
        with self._lock:
            if self.on_evict:
                for key, entry in self._cache.items():
                    self.on_evict(key, entry.value)
            self._cache.clear()
            self._current_weight = 0
    
    def size(self) -> int:
        """Get current number of entries."""
        return len(self._cache)
    
    def weight(self) -> int:
        """Get current total weight."""
        return self._current_weight
    
    def get_stats(self) -> CacheStats:
        """Get cache statistics."""
        return self._stats
    
    def reset_stats(self) -> None:
        """Reset statistics."""
        self._stats.reset()
    
    def keys(self) -> List[K]:
        """Get all keys (most recently used last)."""
        with self._lock:
            return list(self._cache.keys())
    
    def values(self) -> List[V]:
        """Get all values (most recently used last)."""
        with self._lock:
            return [entry.value for entry in self._cache.values()]
    
    def items(self) -> Iterator[Tuple[K, V]]:
        """Iterate over (key, value) pairs."""
        with self._lock:
            for key, entry in self._cache.items():
                yield key, entry.value
    
    def get_entry(self, key: K) -> Optional[CacheEntry[V]]:
        """Get full cache entry (including metadata)."""
        with self._lock:
            if key in self._cache:
                return self._cache[key]
            return None
    
    def touch(self, key: K) -> bool:
        """
        Touch entry to mark as recently used.
        
        Returns:
            True if entry exists
        """
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                self._cache[key].last_accessed = time.time()
                return True
            return False
    
    def prune_expired(self) -> int:
        """
        Remove all expired entries.
        
        Returns:
            Number of entries removed
        """
        with self._lock:
            expired_keys = [
                k for k, entry in self._cache.items()
                if entry.is_expired
            ]
            for key in expired_keys:
                self._remove_entry(key)
                self._stats.expired += 1
            return len(expired_keys)
    
    def get_or_set(
        self,
        key: K,
        factory: Callable[[], V],
        ttl: Optional[float] = None,
        weight: int = 1,
    ) -> V:
        """
        Get value or compute and set if not present.
        
        Args:
            key: Cache key
            factory: Function to create value if not cached
            ttl: Time-to-live in seconds
            weight: Entry weight
        
        Returns:
            Cached or computed value
        """
        with self._lock:
            value = self.get(key)
            if value is not None:
                return value
            
            # Compute value (outside lock to avoid deadlock)
            # Release lock temporarily
            pass
        
        # Compute without lock
        value = factory()
        
        with self._lock:
            # Double-check (another thread might have set it)
            existing = self.get(key)
            if existing is not None:
                return existing
            
            self.set(key, value, ttl=ttl, weight=weight)
            return value
    
    def _remove_entry(self, key: K) -> None:
        """Remove entry and update weight."""
        entry = self._cache.pop(key, None)
        if entry:
            self._current_weight -= entry.weight
            if self.on_evict:
                self.on_evict(key, entry.value)
    
    def _evict_if_needed(self) -> None:
        """Evict entries if size or weight limits exceeded."""
        # Evict by size
        while len(self._cache) > self.max_size:
            oldest_key = next(iter(self._cache))
            self._remove_entry(oldest_key)
            self._stats.evictions += 1
        
        # Evict by weight
        if self.max_weight is not None:
            while self._current_weight > self.max_weight and self._cache:
                oldest_key = next(iter(self._cache))
                self._remove_entry(oldest_key)
                self._stats.evictions += 1
    
    def __len__(self) -> int:
        return self.size()
    
    def __contains__(self, key: K) -> bool:
        return self.contains(key)
    
    def __getitem__(self, key: K) -> V:
        result = self.get(key)
        if result is None:
            raise KeyError(key)
        return result
    
    def __setitem__(self, key: K, value: V) -> None:
        self.set(key, value)
    
    def __delitem__(self, key: K) -> None:
        if not self.delete(key):
            raise KeyError(key)


class TTLCache(Generic[K, V]):
    """
    Time-To-Live focused cache with automatic cleanup.
    
    Optimized for TTL-based expiration scenarios.
    
    Examples:
        >>> cache = TTLCache(default_ttl=60)  # 1 minute
        >>> cache.set('key', 'value')
        >>> cache.get('key')
        'value'
    """
    
    def __init__(
        self,
        default_ttl: float = 300,
        max_size: int = 10000,
        cleanup_interval: float = 60,
    ):
        """
        Initialize TTL cache.
        
        Args:
            default_ttl: Default TTL in seconds
            max_size: Maximum entries
            cleanup_interval: Interval for automatic cleanup
        """
        self.default_ttl = default_ttl
        self.max_size = max_size
        self.cleanup_interval = cleanup_interval
        
        self._cache: Dict[K, Tuple[V, float, float]] = {}  # key -> (value, expires_at, created_at)
        self._lock = threading.RLock()
        self._last_cleanup = time.time()
        self._stats = CacheStats()
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Get value if not expired."""
        with self._lock:
            self._maybe_cleanup()
            
            if key not in self._cache:
                self._stats.misses += 1
                return default
            
            value, expires_at, _ = self._cache[key]
            
            if time.time() > expires_at:
                del self._cache[key]
                self._stats.expired += 1
                self._stats.misses += 1
                return default
            
            self._stats.hits += 1
            return value
    
    def set(self, key: K, value: V, ttl: Optional[float] = None) -> None:
        """Set value with TTL."""
        with self._lock:
            now = time.time()
            actual_ttl = ttl if ttl is not None else self.default_ttl
            expires_at = now + actual_ttl
            
            self._cache[key] = (value, expires_at, now)
            self._stats.inserts += 1
            
            # Evict if over size
            self._maybe_cleanup()
            while len(self._cache) > self.max_size:
                # Remove oldest expired entries first
                expired = [k for k, (_, exp, _) in self._cache.items() if exp < now]
                if expired:
                    for k in expired:
                        del self._cache[k]
                        self._stats.evictions += 1
                else:
                    # Remove entry with earliest expiration
                    oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
                    del self._cache[oldest_key]
                    self._stats.evictions += 1
    
    def delete(self, key: K) -> bool:
        """Delete entry."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def get_ttl(self, key: K) -> Optional[float]:
        """Get remaining TTL for a key."""
        with self._lock:
            if key not in self._cache:
                return None
            
            _, expires_at, _ = self._cache[key]
            remaining = expires_at - time.time()
            return remaining if remaining > 0 else None
    
    def extend_ttl(self, key: K, additional_seconds: float) -> bool:
        """Extend TTL for a key."""
        with self._lock:
            if key not in self._cache:
                return False
            
            value, expires_at, created_at = self._cache[key]
            if time.time() > expires_at:
                del self._cache[key]
                return False
            
            self._cache[key] = (value, expires_at + additional_seconds, created_at)
            return True
    
    def cleanup(self) -> int:
        """Remove all expired entries."""
        with self._lock:
            now = time.time()
            expired = [
                k for k, (_, exp, _) in self._cache.items()
                if exp < now
            ]
            for k in expired:
                del self._cache[k]
                self._stats.expired += 1
            
            self._last_cleanup = now
            return len(expired)
    
    def _maybe_cleanup(self) -> None:
        """Cleanup if interval passed."""
        now = time.time()
        if now - self._last_cleanup > self.cleanup_interval:
            self.cleanup()
    
    def clear(self) -> None:
        """Clear all entries."""
        with self._lock:
            self._cache.clear()
    
    def size(self) -> int:
        """Get current size."""
        return len(self._cache)
    
    def get_stats(self) -> CacheStats:
        """Get statistics."""
        return self._stats
    
    def __len__(self) -> int:
        return self.size()
    
    def __contains__(self, key: K) -> bool:
        return self.get(key) is not None


def lru_cache(
    maxsize: int = 128,
    ttl: Optional[float] = None,
    typed: bool = False,
) -> Callable:
    """
    Decorator for LRU caching function results.
    
    Args:
        maxsize: Maximum cache size
        ttl: Time-to-live in seconds
        typed: Cache different types separately
    
    Returns:
        Decorated function
    
    Examples:
        >>> @lru_cache(maxsize=100, ttl=60)
        ... def expensive_function(n):
        ...     return n * n
        >>> expensive_function(5)
        25
    """
    def decorator(func: Callable) -> Callable:
        cache: LRUCache[tuple, Any] = LRUCache(max_size=maxsize, ttl=ttl)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            if typed:
                key = (args, tuple(sorted(kwargs.items())), 
                       tuple(type(a).__name__ for a in args))
            else:
                key = (args, tuple(sorted(kwargs.items())))
            
            result = cache.get(key)
            if result is not None:
                return result
            
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        
        # Add cache methods
        wrapper.cache = cache
        wrapper.cache_clear = cache.clear
        wrapper.cache_info = lambda: cache.get_stats()
        
        return wrapper
    
    return decorator


class MultiLevelCache(Generic[K, V]):
    """
    Multi-level cache with L1 (fast) and L2 (slow) tiers.
    
    Examples:
        >>> l1 = LRUCache(max_size=100)
        >>> l2 = LRUCache(max_size=10000)
        >>> cache = MultiLevelCache([l1, l2])
        >>> cache.set('key', 'value')
        >>> cache.get('key')
        'value'
    """
    
    def __init__(self, levels: List[LRUCache[K, V]]):
        """
        Initialize multi-level cache.
        
        Args:
            levels: List of caches from fastest (L1) to slowest
        """
        self.levels = levels
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Get value, promoting from slower levels if found."""
        for i, cache in enumerate(self.levels):
            value = cache.get(key)
            if value is not None:
                # Promote to faster levels
                for j in range(i):
                    self.levels[j].set(key, value)
                return value
        
        return default
    
    def set(self, key: K, value: V, **kwargs) -> None:
        """Set value in all levels."""
        for cache in self.levels:
            cache.set(key, value, **kwargs)
    
    def delete(self, key: K) -> bool:
        """Delete from all levels."""
        deleted = False
        for cache in self.levels:
            if cache.delete(key):
                deleted = True
        return deleted
    
    def clear(self) -> None:
        """Clear all levels."""
        for cache in self.levels:
            cache.clear()


class CachedFunction(Generic[K, V]):
    """
    Cached function wrapper with background refresh support.
    
    Examples:
        >>> def fetch_data(key):
        ...     return f"data_{key}"
        >>> cached = CachedFunction(fetch_data, ttl=60)
        >>> cached("key1")
        'data_key1'
    """
    
    def __init__(
        self,
        func: Callable[[K], V],
        ttl: float = 300,
        max_size: int = 1000,
        refresh_before_expiry: float = 0.8,
        background_refresh: bool = False,
    ):
        """
        Initialize cached function.
        
        Args:
            func: Function to cache
            ttl: Cache TTL in seconds
            max_size: Maximum cache size
            refresh_before_expiry: Fraction of TTL after which refresh is triggered
            background_refresh: Whether to refresh in background
        """
        self.func = func
        self.ttl = ttl
        self.refresh_threshold = refresh_before_expiry * ttl
        self.background_refresh = background_refresh
        
        self._cache = TTLCache(default_ttl=ttl, max_size=max_size)
        self._lock = threading.RLock()
        self._refreshing: set = set()
    
    def __call__(self, key: K) -> V:
        """Get cached or compute value."""
        value = self._cache.get(key)
        
        if value is not None:
            # Check if refresh needed
            remaining = self._cache.get_ttl(key)
            if remaining is not None and remaining < self.refresh_threshold:
                self._maybe_refresh(key)
            
            return value
        
        # Compute and cache
        value = self.func(key)
        self._cache.set(key, value)
        return value
    
    def _maybe_refresh(self, key: K) -> None:
        """Refresh value if not already refreshing."""
        if not self.background_refresh:
            return
        
        with self._lock:
            if key in self._refreshing:
                return
            self._refreshing.add(key)
        
        def refresh():
            try:
                value = self.func(key)
                self._cache.set(key, value)
            finally:
                with self._lock:
                    self._refreshing.discard(key)
        
        thread = threading.Thread(target=refresh, daemon=True)
        thread.start()
    
    def invalidate(self, key: K) -> bool:
        """Invalidate cached value."""
        return self._cache.delete(key)
    
    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
    
    def get_stats(self) -> CacheStats:
        """Get cache statistics."""
        return self._cache.get_stats()


class BoundedLRUCache(Generic[K, V]):
    """
    Memory-bounded LRU cache that estimates object sizes.
    
    Examples:
        >>> cache = BoundedLRUCache(max_memory_mb=10)  # 10 MB limit
        >>> cache.set('key', 'value')
        >>> cache.memory_usage()
        55
    """
    
    def __init__(
        self,
        max_memory_mb: float = 100,
        on_evict: Optional[Callable[[K, V], None]] = None,
    ):
        """
        Initialize memory-bounded cache.
        
        Args:
            max_memory_mb: Maximum memory in megabytes
            on_evict: Callback when entry is evicted
        """
        self.max_memory = int(max_memory_mb * 1024 * 1024)
        self.on_evict = on_evict
        
        self._cache: OrderedDict[K, Tuple[V, int]] = OrderedDict()
        self._current_memory = 0
        self._lock = threading.RLock()
        self._stats = CacheStats()
    
    def _estimate_size(self, obj: Any) -> int:
        """Estimate object size in bytes."""
        if isinstance(obj, (str, bytes)):
            return len(obj)
        elif isinstance(obj, (int, float)):
            return 24  # Approximate
        elif isinstance(obj, (list, tuple)):
            return sum(self._estimate_size(item) for item in obj) + 56
        elif isinstance(obj, dict):
            size = 72
            for k, v in obj.items():
                size += self._estimate_size(k) + self._estimate_size(v)
            return size
        elif hasattr(obj, '__sizeof__'):
            return obj.__sizeof__()
        else:
            return 64  # Default estimate
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Get value from cache."""
        with self._lock:
            if key not in self._cache:
                self._stats.misses += 1
                return default
            
            self._cache.move_to_end(key)
            self._stats.hits += 1
            return self._cache[key][0]
    
    def set(self, key: K, value: V) -> None:
        """Set value in cache."""
        with self._lock:
            size = self._estimate_size(value)
            
            # Remove old if exists
            if key in self._cache:
                _, old_size = self._cache[key]
                self._current_memory -= old_size
            
            # Add new
            self._cache[key] = (value, size)
            self._cache.move_to_end(key)
            self._current_memory += size
            self._stats.inserts += 1
            
            # Evict if over memory
            while self._current_memory > self.max_memory and self._cache:
                oldest_key = next(iter(self._cache))
                _, oldest_size = self._cache[oldest_key]
                del self._cache[oldest_key]
                self._current_memory -= oldest_size
                self._stats.evictions += 1
    
    def delete(self, key: K) -> bool:
        """Delete entry."""
        with self._lock:
            if key in self._cache:
                _, size = self._cache[key]
                del self._cache[key]
                self._current_memory -= size
                return True
            return False
    
    def memory_usage(self) -> int:
        """Get current memory usage in bytes."""
        return self._current_memory
    
    def memory_usage_mb(self) -> float:
        """Get current memory usage in megabytes."""
        return self._current_memory / (1024 * 1024)
    
    def clear(self) -> None:
        """Clear all entries."""
        with self._lock:
            self._cache.clear()
            self._current_memory = 0
    
    def size(self) -> int:
        """Get number of entries."""
        return len(self._cache)
    
    def get_stats(self) -> CacheStats:
        """Get statistics."""
        return self._stats
    
    def __len__(self) -> int:
        return self.size()


# Utility functions

def memoize(
    ttl: Optional[float] = None,
    maxsize: int = 128,
) -> Callable:
    """
    Simple memoization decorator.
    
    Args:
        ttl: Time-to-live in seconds
        maxsize: Maximum cache size
    
    Examples:
        >>> @memoize(ttl=60, maxsize=100)
        ... def fibonacci(n):
        ...     if n < 2:
        ...         return n
        ...     return fibonacci(n-1) + fibonacci(n-2)
    """
    return lru_cache(maxsize=maxsize, ttl=ttl)


if __name__ == "__main__":
    # Demo
    print("=" * 60)
    print("LRU Cache Utils Demo")
    print("=" * 60)
    
    # Basic LRU Cache
    print("\n1. Basic LRU Cache:")
    cache = LRUCache(max_size=3)
    cache.set('a', 1)
    cache.set('b', 2)
    cache.set('c', 3)
    print(f"   Set a=1, b=2, c=3")
    cache.set('d', 4)  # Evicts 'a'
    print(f"   Set d=4 (evicts oldest)")
    print(f"   Get 'a': {cache.get('a')} (should be None)")
    print(f"   Get 'd': {cache.get('d')}")
    print(f"   Stats: {cache.get_stats().to_dict()}")
    
    # TTL Cache
    print("\n2. TTL Cache:")
    ttl_cache = TTLCache(default_ttl=1)  # 1 second
    ttl_cache.set('key', 'value')
    print(f"   Set key='value' with 1s TTL")
    print(f"   Get immediately: {ttl_cache.get('key')}")
    time.sleep(1.5)
    print(f"   Get after 1.5s: {ttl_cache.get('key')} (expired)")
    
    # Decorator
    print("\n3. Decorator Usage:")
    call_count = 0
    
    @lru_cache(maxsize=10)
    def expensive_function(n):
        global call_count
        call_count += 1
        return n * n
    
    print(f"   expensive_function(5) = {expensive_function(5)} (call_count={call_count})")
    print(f"   expensive_function(5) = {expensive_function(5)} (call_count={call_count}, cached)")
    print(f"   Cache info: {expensive_function.cache_info().to_dict()}")
    
    # Memory-bounded cache
    print("\n4. Memory-Bounded Cache:")
    mem_cache = BoundedLRUCache(max_memory_mb=0.001)  # 1KB for demo
    mem_cache.set('small', 'x' * 100)
    print(f"   Memory usage: {mem_cache.memory_usage()} bytes")
    print(f"   Entries: {mem_cache.size()}")
    
    # Cached Function
    print("\n5. Cached Function:")
    fetch_count = 0
    
    def fetch_user(user_id):
        global fetch_count
        fetch_count += 1
        return f"user_{user_id}"
    
    cached_fetch = CachedFunction(fetch_user, ttl=60)
    print(f"   cached_fetch(1) = {cached_fetch(1)} (fetch_count={fetch_count})")
    print(f"   cached_fetch(1) = {cached_fetch(1)} (fetch_count={fetch_count}, cached)")
    
    print("\n" + "=" * 60)