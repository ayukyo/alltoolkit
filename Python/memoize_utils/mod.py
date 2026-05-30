# Package memoize_utils provides function memoization utilities with TTL, LRU eviction,
# and thread-safe caching capabilities.
#
# Features:
#   - Generic memoization for any function signature
#   - TTL (Time-To-Live) support for cache expiration
#   - LRU (Least Recently Used) eviction policy
#   - Thread-safe operations (using threading.Lock)
#   - Memory statistics and cache management
#   - Zero external dependencies
#
# Example usage:
#
#     from memoize_utils import LRUCache, memoize
#
#     # Create a cache with max size of 1000
#     cache = LRUCache(max_size=1000)
#
#     # Set a value
#     cache.set("key", "value")
#
#     # Get a value
#     if cache.has("key"):
#         print(cache.get("key"))
#
#     # Memoize a function
#     @memoize(max_size=100, ttl=3600)
#     def expensive_function(n):
#         return n * 2
#
#     result = expensive_function(10)  # Computed
#     result = expensive_function(10)  # Cached

import time
import threading
from collections import OrderedDict
from typing import Generic, TypeVar, Callable, Optional, Any, Dict, List, Tuple, Union

K = TypeVar('K')
V = TypeVar('V')
K1 = TypeVar('K1')
K2 = TypeVar('K2')


class Entry(Generic[V]):
    """Represents a cached value with metadata."""

    def __init__(self, value: V, ttl: Optional[float] = None):
        self.value: V = value
        self.created_at: float = time.time()
        self.expires_at: Optional[float] = time.time() + ttl if ttl and ttl > 0 else None
        self.access_at: float = self.created_at
        self.access_count: int = 0

    def is_expired(self) -> bool:
        """Check if the entry has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at

    def age(self) -> float:
        """Return the age of the entry in seconds."""
        return time.time() - self.created_at

    def ttl(self) -> float:
        """Return the remaining time to live in seconds. Returns -1 if no expiration."""
        if self.expires_at is None:
            return -1.0
        remaining = self.expires_at - time.time()
        return max(0.0, remaining)


class CacheStats:
    """Holds cache statistics."""

    def __init__(self):
        self.hits: int = 0
        self.misses: int = 0
        self.size: int = 0
        self.max_size: int = 0
        self.hit_rate: float = 0.0

    def __repr__(self) -> str:
        return f"CacheStats(hits={self.hits}, misses={self.misses}, size={self.size}, max_size={self.max_size}, hit_rate={self.hit_rate:.2f}%)"


class LRUCache(Generic[K, V]):
    """Thread-safe LRU cache with TTL support."""

    def __init__(self, max_size: int = 1000, ttl: Optional[float] = None,
                 on_evict: Optional[Callable[[str, Any], None]] = None,
                 stats_enabled: bool = False):
        """
        Create a new LRU cache.

        Args:
            max_size: Maximum number of entries (0 = unlimited)
            ttl: Default TTL in seconds for cache entries (None = no expiration)
            on_evict: Callback function called when entries are evicted
            stats_enabled: Enable statistics tracking
        """
        self._max_size: int = max_size if max_size > 0 else 1000
        self._ttl: Optional[float] = ttl
        self._on_evict: Optional[Callable[[str, Any], None]] = on_evict
        self._cache: OrderedDict[K, Entry[V]] = OrderedDict()
        self._lock: threading.RLock = threading.RLock()
        self._stats: Optional[CacheStats] = CacheStats() if stats_enabled else None
        if self._stats:
            self._stats.max_size = self._max_size

    def set(self, key: K, value: V, ttl: Optional[float] = None) -> None:
        """Add a value to the cache."""
        self._set_with_ttl(key, value, ttl)

    def _set_with_ttl(self, key: K, value: V, ttl: Optional[float] = None) -> None:
        """Add a value to the cache with optional custom TTL."""
        with self._lock:
            # Check if key exists
            if key in self._cache:
                # Move to front (most recently used)
                self._cache.move_to_end(key)
                entry = self._cache[key]
                entry.value = value
                entry.created_at = time.time()
                entry.access_at = time.time()
                entry.access_count += 1
                if ttl is not None and ttl > 0:
                    entry.expires_at = time.time() + ttl
                elif self._ttl is not None and self._ttl > 0:
                    entry.expires_at = time.time() + self._ttl
                else:
                    entry.expires_at = None
                return

            # Create new entry
            effective_ttl = ttl if ttl is not None else self._ttl
            entry = Entry(value, effective_ttl)

            # Add to cache
            self._cache[key] = entry

            # Evict if necessary
            if self._max_size > 0 and len(self._cache) > self._max_size:
                self._evict()

    def get(self, key: K) -> Tuple[V, bool]:
        """
        Retrieve a value from the cache.

        Returns:
            Tuple of (value, found). If not found, value will be None.
        """
        with self._lock:
            if key not in self._cache:
                if self._stats:
                    self._stats.misses += 1
                return None, False

            entry = self._cache[key]

            # Check expiration
            if entry.is_expired():
                del self._cache[key]
                if self._stats:
                    self._stats.misses += 1
                return None, False

            # Update access info
            self._cache.move_to_end(key)
            entry.access_at = time.time()
            entry.access_count += 1

            if self._stats:
                self._stats.hits += 1

            return entry.value, True

    def get_or_compute(self, key: K, compute: Callable[[], V]) -> V:
        """
        Retrieve a value from the cache, or compute it if not found.

        Args:
            key: The cache key
            compute: Function to compute the value if not cached

        Returns:
            The cached or computed value
        """
        value, found = self.get(key)
        if found:
            return value

        value = compute()
        self.set(key, value)
        return value

    def get_or_compute_with_error(self, key: K,
                                   compute: Callable[[], Tuple[V, Optional[Exception]]]) -> Tuple[V, Optional[Exception]]:
        """
        Retrieve a value from the cache, or compute it if not found.
        Allows compute function to return an error.

        Returns:
            Tuple of (value, error). If error is not None, the operation failed.
        """
        value, found = self.get(key)
        if found:
            return value, None

        value, err = compute()
        if err is not None:
            return None, err

        self.set(key, value)
        return value, None

    def delete(self, key: K) -> bool:
        """Remove a key from the cache. Returns True if key was found."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> None:
        """Clear all entries from the cache."""
        with self._lock:
            if self._on_evict:
                for key, entry in self._cache.items():
                    self._on_evict(str(key), entry.value)
            self._cache.clear()

    def has(self, key: K) -> bool:
        """Check if a key exists and is not expired."""
        with self._lock:
            if key not in self._cache:
                return False
            entry = self._cache[key]
            return not entry.is_expired()

    def size(self) -> int:
        """Return the number of entries in the cache."""
        with self._lock:
            return len(self._cache)

    def keys(self) -> List[K]:
        """Return all keys in the cache."""
        with self._lock:
            return list(self._cache.keys())

    def purge_expired(self) -> int:
        """Remove all expired entries. Returns count of removed entries."""
        with self._lock:
            count = 0
            expired_keys = [k for k, e in self._cache.items() if e.is_expired()]
            for key in expired_keys:
                if self._on_evict:
                    self._on_evict(str(key), self._cache[key].value)
                del self._cache[key]
                count += 1
            return count

    def get_stats(self) -> CacheStats:
        """Return cache statistics."""
        if self._stats is None:
            return CacheStats()
        with self._lock:
            stats = CacheStats()
            stats.hits = self._stats.hits
            stats.misses = self._stats.misses
            stats.size = len(self._cache)
            stats.max_size = self._max_size
            total = stats.hits + stats.misses
            if total > 0:
                stats.hit_rate = (stats.hits / total) * 100
            return stats

    def _evict(self) -> None:
        """Evict the oldest entry."""
        if not self._cache:
            return
        key, entry = self._cache.popitem(last=False)
        if self._on_evict:
            self._on_evict(str(key), entry.value)


class TTLCache(Generic[K, V]):
    """Simple TTL cache without LRU eviction."""

    def __init__(self, ttl: float, max_size: int = 0,
                 on_evict: Optional[Callable[[str, Any], None]] = None,
                 stats_enabled: bool = False):
        """
        Create a new TTL cache.

        Args:
            ttl: TTL in seconds for all cache entries
            max_size: Maximum number of entries (0 = unlimited)
            on_evict: Callback function called when entries are evicted
            stats_enabled: Enable statistics tracking
        """
        self._ttl: float = ttl
        self._max_size: int = max_size
        self._on_evict: Optional[Callable[[str, Any], None]] = on_evict
        self._cache: Dict[K, Entry[V]] = {}
        self._lock: threading.RLock = threading.RLock()
        self._stats: Optional[CacheStats] = CacheStats() if stats_enabled else None

    def set(self, key: K, value: V, ttl: Optional[float] = None) -> None:
        """Add a value to the cache."""
        with self._lock:
            effective_ttl = ttl if ttl is not None else self._ttl
            entry = Entry(value, effective_ttl)
            self._cache[key] = entry

            # Evict oldest if at capacity
            if self._max_size > 0 and len(self._cache) > self._max_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]

    def get(self, key: K) -> Tuple[V, bool]:
        """Retrieve a value from the cache."""
        with self._lock:
            if key not in self._cache:
                if self._stats:
                    self._stats.misses += 1
                return None, False

            entry = self._cache[key]

            if entry.is_expired():
                del self._cache[key]
                if self._stats:
                    self._stats.misses += 1
                return None, False

            entry.access_at = time.time()
            entry.access_count += 1
            if self._stats:
                self._stats.hits += 1

            return entry.value, True

    def delete(self, key: K) -> bool:
        """Remove a key from the cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> None:
        """Clear all entries."""
        with self._lock:
            self._cache.clear()

    def has(self, key: K) -> bool:
        """Check if a key exists and is not expired."""
        with self._lock:
            if key not in self._cache:
                return False
            entry = self._cache[key]
            return not entry.is_expired()

    def size(self) -> int:
        """Return the number of entries."""
        with self._lock:
            return len(self._cache)

    def purge_expired(self) -> int:
        """Remove all expired entries."""
        with self._lock:
            count = 0
            expired_keys = [k for k, e in self._cache.items() if e.is_expired()]
            for key in expired_keys:
                if self._on_evict:
                    self._on_evict(str(key), self._cache[key].value)
                del self._cache[key]
                count += 1
            return count

    def get_stats(self) -> CacheStats:
        """Return cache statistics."""
        if self._stats is None:
            return CacheStats()
        with self._lock:
            stats = CacheStats()
            stats.hits = self._stats.hits
            stats.misses = self._stats.misses
            stats.size = len(self._cache)
            total = stats.hits + stats.misses
            if total > 0:
                stats.hit_rate = (stats.hits / total) * 100
            return stats


def memoize(fn: Callable[[K], V] = None, *, max_size: int = 1000,
            ttl: Optional[float] = None) -> Callable[[K], V]:
    """
    Decorator to memoize a single-argument function.

    Args:
        fn: The function to memoize
        max_size: Maximum cache size
        ttl: TTL in seconds

    Example:
        @memoize(max_size=100, ttl=3600)
        def expensive_function(n):
            return n * 2
    """
    def decorator(func: Callable[[K], V]) -> Callable[[K], V]:
        cache = LRUCache(max_size=max_size, ttl=ttl)

        def wrapper(key: K) -> V:
            value, found = cache.get(key)
            if found:
                return value
            value = func(key)
            cache.set(key, value)
            return value
        return wrapper

    if fn is not None:
        return decorator(fn)
    return decorator


def memoize_err(fn: Callable[[K], Tuple[V, Optional[Exception]]] = None, *,
                max_size: int = 1000,
                ttl: Optional[float] = None) -> Callable[[K], Tuple[V, Optional[Exception]]]:
    """
    Decorator to memoize a single-argument function that returns (value, error).

    Args:
        fn: The function to memoize
        max_size: Maximum cache size
        ttl: TTL in seconds
    """
    def decorator(func: Callable[[K], Tuple[V, Optional[Exception]]]) -> Callable[[K], Tuple[V, Optional[Exception]]]:
        cache = LRUCache(max_size=max_size, ttl=ttl)

        def wrapper(key: K) -> Tuple[V, Optional[Exception]]:
            value, found = cache.get(key)
            if found:
                return value, None
            value, err = func(key)
            if err is not None:
                return None, err
            cache.set(key, value)
            return value, None
        return wrapper

    if fn is not None:
        return decorator(fn)
    return decorator


def memoize2(fn: Callable[[K1, K2], V] = None, *,
             max_size: int = 1000,
             ttl: Optional[float] = None) -> Callable[[K1, K2], V]:
    """
    Decorator to memoize a two-argument function.

    Args:
        fn: The function to memoize
        max_size: Maximum cache size
        ttl: TTL in seconds
    """
    def decorator(func: Callable[[K1, K2], V]) -> Callable[[K1, K2], V]:
        cache = LRUCache(max_size=max_size, ttl=ttl)

        def wrapper(k1: K1, k2: K2) -> V:
            key = (k1, k2)
            value, found = cache.get(key)
            if found:
                return value
            value = func(k1, k2)
            cache.set(key, value)
            return value
        return wrapper

    if fn is not None:
        return decorator(fn)
    return decorator


def memoize2_err(fn: Callable[[K1, K2], Tuple[V, Optional[Exception]]] = None, *,
                 max_size: int = 1000,
                 ttl: Optional[float] = None) -> Callable[[K1, K2], Tuple[V, Optional[Exception]]]:
    """
    Decorator to memoize a two-argument function that returns (value, error).
    """
    def decorator(func: Callable[[K1, K2], Tuple[V, Optional[Exception]]]) -> Callable[[K1, K2], Tuple[V, Optional[Exception]]]:
        cache = LRUCache(max_size=max_size, ttl=ttl)

        def wrapper(k1: K1, k2: K2) -> Tuple[V, Optional[Exception]]:
            key = (k1, k2)
            value, found = cache.get(key)
            if found:
                return value, None
            value, err = func(k1, k2)
            if err is not None:
                return None, err
            cache.set(key, value)
            return value, None
        return wrapper

    if fn is not None:
        return decorator(fn)
    return decorator


# ============================================================================
# Utility Functions
# ============================================================================

def expired_entries(m: Dict[K, Entry[V]]) -> int:
    """Count expired entries in a dictionary."""
    return sum(1 for e in m.values() if e.is_expired())


def purge_map(m: Dict[K, Entry[V]]) -> int:
    """Remove expired entries from a dictionary. Returns count removed."""
    count = 0
    expired_keys = [k for k, e in m.items() if e.is_expired()]
    for key in expired_keys:
        del m[key]
        count += 1
    return count