"""
TTL (Time-To-Live) memoization implementation.

Provides caching with automatic expiration of cached values.
"""

import functools
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar, Union

F = TypeVar('F', bound=Callable)


@dataclass
class CacheEntry:
    """A cache entry with expiration time."""
    value: Any
    expires_at: float
    created_at: float


class TTLMemoizeStats:
    """Statistics for TTL memoized functions."""
    
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.expirations = 0
        self.total_time_saved = 0.0
    
    @property
    def total_calls(self) -> int:
        return self.hits + self.misses
    
    @property
    def hit_rate(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return self.hits / self.total_calls
    
    def record_hit(self, time_saved: float = 0.0):
        self.hits += 1
        self.total_time_saved += time_saved
    
    def record_miss(self):
        self.misses += 1
    
    def record_expiration(self):
        self.expirations += 1
    
    def __repr__(self) -> str:
        return (
            f"TTLMemoizeStats(hits={self.hits}, misses={self.misses}, "
            f"expirations={self.expirations}, hit_rate={self.hit_rate:.2%})"
        )


class TTLCache:
    """Thread-safe cache with time-to-live expiration."""
    
    def __init__(self, default_ttl: float = 300.0, maxsize: Optional[int] = None):
        """
        Initialize TTL cache.
        
        Args:
            default_ttl: Default time-to-live in seconds.
            maxsize: Maximum cache size. None for unlimited.
        """
        self.default_ttl = default_ttl
        self.maxsize = maxsize
        self._cache: Dict[Any, CacheEntry] = {}
        self._lock = threading.RLock()
        self._stats = TTLMemoizeStats()
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if an entry has expired."""
        return time.time() > entry.expires_at
    
    def _cleanup_expired(self):
        """Remove expired entries."""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items()
            if current_time > entry.expires_at
        ]
        for key in expired_keys:
            del self._cache[key]
            self._stats.record_expiration()
    
    def get(self, key: Any) -> Tuple[bool, Any]:
        """Get a value from cache. Returns (found, value)."""
        with self._lock:
            # Cleanup expired entries occasionally
            self._cleanup_expired()
            
            if key in self._cache:
                entry = self._cache[key]
                if not self._is_expired(entry):
                    self._stats.record_hit()
                    return True, entry.value
                else:
                    # Remove expired entry
                    del self._cache[key]
                    self._stats.record_expiration()
            
            self._stats.record_miss()
            return False, None
    
    def set(self, key: Any, value: Any, ttl: Optional[float] = None):
        """Set a value in cache with optional custom TTL."""
        with self._lock:
            current_time = time.time()
            ttl = ttl if ttl is not None else self.default_ttl
            
            entry = CacheEntry(
                value=value,
                expires_at=current_time + ttl,
                created_at=current_time
            )
            
            self._cache[key] = entry
            
            # Check maxsize
            if self.maxsize is not None and len(self._cache) > self.maxsize:
                # Remove oldest entries
                self._cleanup_expired()
                if len(self._cache) > self.maxsize:
                    # Remove oldest (by creation time)
                    oldest_key = min(self._cache.keys(), 
                                    key=lambda k: self._cache[k].created_at)
                    del self._cache[oldest_key]
    
    def delete(self, key: Any) -> bool:
        """Delete a key from cache. Returns True if key existed."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self):
        """Clear all cached values."""
        with self._lock:
            self._cache.clear()
    
    def __len__(self) -> int:
        with self._lock:
            self._cleanup_expired()
            return len(self._cache)
    
    def info(self) -> Dict[str, Any]:
        """Get cache statistics and info."""
        with self._lock:
            self._cleanup_expired()
            return {
                'size': len(self._cache),
                'maxsize': self.maxsize,
                'default_ttl': self.default_ttl,
                'stats': self._stats,
            }


# Global registry of TTL caches
_ttl_caches: Dict[str, TTLCache] = {}
_ttl_lock = threading.Lock()


def ttl_memoize(
    ttl: float = 300.0,
    maxsize: Optional[int] = None,
    name: Optional[str] = None,
) -> Callable:
    """
    TTL memoization decorator with automatic expiration.
    
    Cached values expire after the specified time-to-live.
    
    Args:
        ttl: Time-to-live in seconds (default: 300 = 5 minutes).
        maxsize: Maximum cache size. None for unlimited.
        name: Optional name for cache management.
    
    Returns:
        Decorated function with TTL caching.
    
    Example:
        @ttl_memoize(ttl=60.0)  # Cache for 60 seconds
        def fetch_api_data(endpoint):
            # Expensive API call
            return requests.get(endpoint).json()
        
        data1 = fetch_api_data('/users')  # Fetched from API
        data2 = fetch_api_data('/users')  # Cached
        time.sleep(61)
        data3 = fetch_api_data('/users')  # Fetched again (expired)
    """
    def decorator(func: F) -> F:
        cache = TTLCache(default_ttl=ttl, maxsize=maxsize)
        
        # Register cache
        cache_name = name or f"{func.__module__}.{func.__name__}"
        with _ttl_lock:
            _ttl_caches[cache_name] = cache
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = (args, frozenset(sorted(kwargs.items()))) if kwargs else args
            
            # Check cache
            found, value = cache.get(key)
            if found:
                return value
            
            # Compute and cache
            result = func(*args, **kwargs)
            cache.set(key, result)
            
            return result
        
        wrapper.cache_clear = cache.clear
        wrapper.cache_info = cache.info
        wrapper._cache = cache
        
        return wrapper
    
    return decorator


def ttl_memoize_method(
    ttl: float = 300.0,
    maxsize: Optional[int] = None,
) -> Callable:
    """
    TTL memoization decorator for instance methods.
    
    Each instance has its own cache with TTL expiration.
    
    Args:
        ttl: Time-to-live in seconds.
        maxsize: Maximum cache size per instance.
    
    Returns:
        Decorated method with per-instance TTL caching.
    
    Example:
        class APIClient:
            @ttl_memoize_method(ttl=30.0)
            def get_user(self, user_id):
                return self._fetch_user(user_id)
    """
    def decorator(method: F) -> F:
        caches: Dict[int, TTLCache] = {}
        
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            instance_id = id(self)
            
            # Get or create cache for this instance
            if instance_id not in caches:
                caches[instance_id] = TTLCache(default_ttl=ttl, maxsize=maxsize)
            
            cache = caches[instance_id]
            
            # Create cache key (excluding self)
            key = (args, frozenset(sorted(kwargs.items()))) if kwargs else args
            
            # Check cache
            found, value = cache.get(key)
            if found:
                return value
            
            # Compute and cache
            result = method(self, *args, **kwargs)
            cache.set(key, result)
            
            return result
        
        def cache_clear(self):
            instance_id = id(self)
            if instance_id in caches:
                caches[instance_id].clear()
        
        def cache_info(self):
            instance_id = id(self)
            if instance_id in caches:
                return caches[instance_id].info()
            return {'size': 0, 'maxsize': maxsize, 'default_ttl': ttl, 'stats': None}
        
        wrapper.cache_clear = cache_clear
        wrapper.cache_info = cache_info
        
        return wrapper
    
    return decorator


def clear_ttl_caches():
    """Clear all TTL caches registered globally."""
    with _ttl_lock:
        for cache in _ttl_caches.values():
            cache.clear()


def get_ttl_cache_info(name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get information about TTL caches.
    
    Args:
        name: Optional specific cache name.
    
    Returns:
        Dictionary of cache info.
    """
    with _ttl_lock:
        if name:
            if name in _ttl_caches:
                return {name: _ttl_caches[name].info()}
            return {}
        
        return {
            cache_name: cache.info()
            for cache_name, cache in _ttl_caches.items()
        }


class TTLMemoizeContext:
    """
    Context manager for temporary TTL caching.
    
    Example:
        with TTLMemoizeContext(ttl=60.0) as cache:
            @cache.decorate
            def fetch_data(url):
                return requests.get(url).json()
            
            data = fetch_data('/api/data')  # Cached for 60 seconds
    """
    
    def __init__(self, ttl: float = 300.0, maxsize: Optional[int] = None):
        self.ttl = ttl
        self.maxsize = maxsize
        self.cache = TTLCache(default_ttl=ttl, maxsize=maxsize)
    
    def decorate(self, func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(sorted(kwargs.items()))) if kwargs else args
            found, value = self.cache.get(key)
            if found:
                return value
            result = func(*args, **kwargs)
            self.cache.set(key, result)
            return result
        
        return wrapper
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.cache.clear()
    
    def info(self):
        return self.cache.info()