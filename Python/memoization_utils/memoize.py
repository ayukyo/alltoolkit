"""
Basic memoization implementation with no external dependencies.

Provides simple yet powerful function result caching.
"""

import functools
import hashlib
import pickle
import threading
import time
from collections import OrderedDict
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar, Union

T = TypeVar('T')
F = TypeVar('F', bound=Callable)


class MemoizeStats:
    """Statistics for memoized functions."""
    
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.total_time_saved = 0.0  # seconds
    
    @property
    def total_calls(self) -> int:
        return self.hits + self.misses
    
    @property
    def hit_rate(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return self.hits / self.total_calls
    
    @property
    def miss_rate(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return self.misses / self.total_calls
    
    def record_hit(self, time_saved: float = 0.0):
        self.hits += 1
        self.total_time_saved += time_saved
    
    def record_miss(self):
        self.misses += 1
    
    def __repr__(self) -> str:
        return (
            f"MemoizeStats(hits={self.hits}, misses={self.misses}, "
            f"hit_rate={self.hit_rate:.2%}, time_saved={self.total_time_saved:.3f}s)"
        )


class MemoizeStore:
    """Thread-safe store for memoized values."""
    
    def __init__(self, maxsize: Optional[int] = None):
        self.maxsize = maxsize
        self._cache: OrderedDict = OrderedDict()
        self._lock = threading.RLock()
    
    def get(self, key: Any) -> Tuple[bool, Any]:
        """Get a value from cache. Returns (found, value)."""
        with self._lock:
            if key in self._cache:
                # Move to end (most recently used)
                self._cache.move_to_end(key)
                return True, self._cache[key]
            return False, None
    
    def set(self, key: Any, value: Any):
        """Set a value in cache."""
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                self._cache[key] = value
            else:
                self._cache[key] = value
                if self.maxsize is not None and len(self._cache) > self.maxsize:
                    # Remove oldest (first) item
                    self._cache.popitem(last=False)
    
    def clear(self):
        """Clear all cached values."""
        with self._lock:
            self._cache.clear()
    
    def __len__(self) -> int:
        return len(self._cache)
    
    def __contains__(self, key: Any) -> bool:
        return key in self._cache


def _make_key(args: tuple, kwargs: dict, kwargs_key: Callable = None) -> Any:
    """Create a cache key from function arguments."""
    if kwargs_key:
        # Use custom key function
        return kwargs_key(*args, **kwargs)
    
    # Default key creation
    if kwargs:
        return (args, frozenset(sorted(kwargs.items())))
    return args


def _hash_key(key: Any) -> str:
    """Create a hash string from a key for complex objects."""
    try:
        serialized = pickle.dumps(key)
        return hashlib.md5(serialized).hexdigest()
    except (TypeError, pickle.PicklingError):
        # Fallback to string representation
        return hashlib.md5(str(key).encode()).hexdigest()


def memoize(
    maxsize: Optional[int] = None,
    key_func: Optional[Callable] = None,
    use_hash: bool = False,
    stats: Optional[MemoizeStats] = None,
) -> Callable:
    """
    Memoization decorator that caches function results.
    
    Args:
        maxsize: Maximum cache size. None for unlimited.
        key_func: Custom function to generate cache keys from args.
        use_hash: Use hashed keys for complex arguments (slower but more flexible).
        stats: MemoizeStats instance to track cache performance.
    
    Returns:
        Decorated function with caching.
    
    Example:
        @memoize()
        def fibonacci(n):
            if n < 2:
                return n
            return fibonacci(n-1) + fibonacci(n-2)
        
        @memoize(maxsize=128)
        def expensive_computation(x, y):
            return x ** y
    """
    def decorator(func: F) -> F:
        store = MemoizeStore(maxsize=maxsize)
        _stats = stats or MemoizeStats()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = _make_key(args, kwargs, key_func)
            if use_hash:
                key = _hash_key(key)
            
            # Check cache
            found, value = store.get(key)
            if found:
                _stats.record_hit()
                return value
            
            # Compute and cache
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            
            store.set(key, result)
            _stats.record_miss()
            # Time saved would be calculated on future hits
            
            return result
        
        # Add cache management methods
        wrapper.cache_clear = store.clear
        wrapper.cache_info = lambda: {'size': len(store), 'stats': _stats}
        wrapper.cache_store = store
        
        return wrapper
    
    return decorator


def memoize_method(
    maxsize: Optional[int] = None,
    key_func: Optional[Callable] = None,
    use_hash: bool = False,
) -> Callable:
    """
    Memoization decorator for instance methods.
    
    Handles 'self' argument properly and stores cache per-instance.
    
    Args:
        maxsize: Maximum cache size per instance.
        key_func: Custom function to generate cache keys from args (excluding self).
        use_hash: Use hashed keys for complex arguments.
    
    Returns:
        Decorated method with per-instance caching.
    
    Example:
        class Calculator:
            @memoize_method(maxsize=100)
            def compute(self, x, y):
                # Expensive computation
                return x ** y
        
        calc1 = Calculator()
        calc2 = Calculator()
        # Each instance has its own cache
        calc1.compute(5, 3)  # Computed
        calc1.compute(5, 3)  # Cached
        calc2.compute(5, 3)  # Computed (different instance)
    """
    def decorator(method: F) -> F:
        # Use a weak reference dictionary to track instances
        caches: Dict[int, MemoizeStore] = {}
        stats: Dict[int, MemoizeStats] = {}
        
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            # Get instance ID
            instance_id = id(self)
            
            # Get or create cache for this instance
            if instance_id not in caches:
                caches[instance_id] = MemoizeStore(maxsize=maxsize)
                stats[instance_id] = MemoizeStats()
            
            store = caches[instance_id]
            _stats = stats[instance_id]
            
            # Create cache key (excluding self)
            key = _make_key(args, kwargs, key_func)
            if use_hash:
                key = _hash_key(key)
            
            # Check cache
            found, value = store.get(key)
            if found:
                _stats.record_hit()
                return value
            
            # Compute and cache
            result = method(self, *args, **kwargs)
            store.set(key, result)
            _stats.record_miss()
            
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
                return {'size': len(caches[instance_id]), 'stats': stats[instance_id]}
            return {'size': 0, 'stats': None}
        
        wrapper.cache_clear = cache_clear
        wrapper.cache_info = cache_info
        
        return wrapper
    
    return decorator


class MemoizedClass:
    """
    A class wrapper that memoizes method calls across all instances.
    
    Example:
        @MemoizedClass
        class API:
            def fetch_data(self, url):
                # This will be cached across all instances
                return requests.get(url).json()
    """
    
    def __init__(self, cls):
        self._cls = cls
        self._cache = MemoizeStore()
        self._stats = MemoizeStats()
    
    def __call__(self, *args, **kwargs):
        return self._cls(*args, **kwargs)
    
    def cache_clear(self):
        self._cache.clear()
    
    def cache_info(self):
        return {'size': len(self._cache), 'stats': self._stats}


# Decorator alias for class-level memoization
def memoize_class(cls):
    """Decorator to memoize all method calls across instances of a class."""
    return MemoizedClass(cls)