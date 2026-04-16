"""
LRU (Least Recently Used) memoization implementation.

Provides size-bounded caching with automatic eviction of least recently used items.
"""

import functools
import threading
from collections import OrderedDict
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar

F = TypeVar('F', bound=Callable)


class LRUCache:
    """Thread-safe LRU cache implementation."""
    
    def __init__(self, maxsize: int = 128):
        if maxsize <= 0:
            raise ValueError("maxsize must be positive")
        self.maxsize = maxsize
        self._cache: OrderedDict = OrderedDict()
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0
    
    def get(self, key: Any) -> Tuple[bool, Any]:
        """Get a value from cache. Returns (found, value)."""
        with self._lock:
            if key in self._cache:
                # Move to end (most recently used)
                self._cache.move_to_end(key)
                self._hits += 1
                return True, self._cache[key]
            self._misses += 1
            return False, None
    
    def set(self, key: Any, value: Any):
        """Set a value in cache, evicting LRU item if necessary."""
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                self._cache[key] = value
            else:
                self._cache[key] = value
                if len(self._cache) > self.maxsize:
                    # Remove oldest (first) item
                    self._cache.popitem(last=False)
    
    def clear(self):
        """Clear all cached values."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
    
    def __len__(self) -> int:
        return len(self._cache)
    
    def info(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            return {
                'size': len(self._cache),
                'maxsize': self.maxsize,
                'hits': self._hits,
                'misses': self._misses,
                'hit_rate': self._hits / (self._hits + self._misses) if (self._hits + self._misses) > 0 else 0.0,
            }


# Global registry of LRU caches
_lru_caches: Dict[str, LRUCache] = {}
_lru_lock = threading.Lock()


def lru_memoize(
    maxsize: int = 128,
    name: Optional[str] = None,
) -> Callable:
    """
    LRU memoization decorator with bounded cache size.
    
    Automatically evicts least recently used items when cache is full.
    
    Args:
        maxsize: Maximum number of items to cache (must be > 0).
        name: Optional name for the cache (for management purposes).
    
    Returns:
        Decorated function with LRU caching.
    
    Example:
        @lru_memoize(maxsize=128)
        def get_factorial(n):
            if n <= 1:
                return 1
            return n * get_factorial(n - 1)
        
        # Get cache info
        info = get_factorial.cache_info()
        print(f"Hit rate: {info['hit_rate']:.2%}")
        
        # Clear cache
        get_factorial.cache_clear()
    """
    def decorator(func: F) -> F:
        cache = LRUCache(maxsize=maxsize)
        
        # Register cache
        cache_name = name or f"{func.__module__}.{func.__name__}"
        with _lru_lock:
            _lru_caches[cache_name] = cache
        
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


def lru_memoize_method(maxsize: int = 128) -> Callable:
    """
    LRU memoization decorator for instance methods.
    
    Each instance has its own cache with the specified maxsize.
    
    Args:
        maxsize: Maximum cache size per instance.
    
    Returns:
        Decorated method with per-instance LRU caching.
    
    Example:
        class DataProcessor:
            @lru_memoize_method(maxsize=64)
            def process(self, data_id):
                # Expensive processing
                return self._compute(data_id)
        
        processor = DataProcessor()
        processor.process(123)  # Computed
        processor.process(123)  # Cached
    """
    def decorator(method: F) -> F:
        caches: Dict[int, LRUCache] = {}
        
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            instance_id = id(self)
            
            # Get or create cache for this instance
            if instance_id not in caches:
                caches[instance_id] = LRUCache(maxsize=maxsize)
            
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
            """Clear cache for a specific instance."""
            instance_id = id(self)
            if instance_id in caches:
                caches[instance_id].clear()
        
        def cache_info(self):
            """Get cache info for a specific instance."""
            instance_id = id(self)
            if instance_id in caches:
                return caches[instance_id].info()
            return {'size': 0, 'maxsize': maxsize, 'hits': 0, 'misses': 0, 'hit_rate': 0.0}
        
        wrapper.cache_clear = cache_clear
        wrapper.cache_info = cache_info
        
        return wrapper
    
    return decorator


def clear_lru_caches():
    """Clear all LRU caches registered globally."""
    with _lru_lock:
        for cache in _lru_caches.values():
            cache.clear()


def get_lru_cache_info(name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get information about LRU caches.
    
    Args:
        name: Optional specific cache name. If None, returns all cache info.
    
    Returns:
        Dictionary of cache info.
    """
    with _lru_lock:
        if name:
            if name in _lru_caches:
                return {name: _lru_caches[name].info()}
            return {}
        
        return {
            cache_name: cache.info()
            for cache_name, cache in _lru_caches.items()
        }


class LRUMemoizeContext:
    """
    Context manager for temporary LRU caching.
    
    Useful for caching during a specific operation only.
    
    Example:
        def expensive_operation():
            with LRUMemoizeContext(maxsize=100) as cache:
                # Define and use a cached function
                @cache.decorate
                def compute(x):
                    return x ** 2
                
                result = compute(5)  # Computed
                result = compute(5)  # Cached
            # Cache is cleared when exiting context
    """
    
    def __init__(self, maxsize: int = 128):
        self.maxsize = maxsize
        self.cache = LRUCache(maxsize=maxsize)
    
    def decorate(self, func: F) -> F:
        """Decorate a function to use this cache."""
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