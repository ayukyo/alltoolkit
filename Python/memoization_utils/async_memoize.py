"""
Async memoization implementation.

Provides caching for async/await functions.
"""

import asyncio
import functools
import hashlib
import threading
import time
from collections import OrderedDict
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar

F = TypeVar('F')


class AsyncLRUCache:
    """Thread-safe LRU cache for async functions."""
    
    def __init__(self, maxsize: int = 128):
        if maxsize <= 0:
            raise ValueError("maxsize must be positive")
        self.maxsize = maxsize
        self._cache: OrderedDict = OrderedDict()
        self._lock = asyncio.Lock()
        self._hits = 0
        self._misses = 0
    
    async def get(self, key: Any) -> Tuple[bool, Any]:
        """Get a value from cache. Returns (found, value)."""
        async with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                self._hits += 1
                return True, self._cache[key]
            self._misses += 1
            return False, None
    
    async def set(self, key: Any, value: Any):
        """Set a value in cache."""
        async with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                self._cache[key] = value
            else:
                self._cache[key] = value
                if len(self._cache) > self.maxsize:
                    self._cache.popitem(last=False)
    
    async def clear(self):
        """Clear all cached values."""
        async with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
    
    def __len__(self) -> int:
        return len(self._cache)
    
    def info(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            'size': len(self._cache),
            'maxsize': self.maxsize,
            'hits': self._hits,
            'misses': self._misses,
            'hit_rate': self._hits / (self._hits + self._misses) if (self._hits + self._misses) > 0 else 0.0,
        }


class AsyncTTLCache:
    """TTL cache for async functions."""
    
    def __init__(self, ttl: float = 300.0, maxsize: Optional[int] = None):
        self.ttl = ttl
        self.maxsize = maxsize
        self._cache: Dict[Any, Tuple[Any, float]] = {}  # key -> (value, expires_at)
        self._lock = asyncio.Lock()
        self._hits = 0
        self._misses = 0
        self._expirations = 0
    
    async def get(self, key: Any) -> Tuple[bool, Any]:
        """Get a value from cache. Returns (found, value)."""
        async with self._lock:
            current_time = time.time()
            
            if key in self._cache:
                value, expires_at = self._cache[key]
                if current_time < expires_at:
                    self._hits += 1
                    return True, value
                else:
                    # Expired
                    del self._cache[key]
                    self._expirations += 1
            
            self._misses += 1
            return False, None
    
    async def set(self, key: Any, value: Any, ttl: Optional[float] = None):
        """Set a value in cache."""
        async with self._lock:
            current_time = time.time()
            actual_ttl = ttl if ttl is not None else self.ttl
            expires_at = current_time + actual_ttl
            
            self._cache[key] = (value, expires_at)
            
            # Enforce maxsize
            if self.maxsize is not None and len(self._cache) > self.maxsize:
                # Remove expired entries first
                expired_keys = [
                    k for k, (_, exp) in self._cache.items()
                    if current_time >= exp
                ]
                for k in expired_keys:
                    del self._cache[k]
                    self._expirations += 1
                
                # If still over limit, remove oldest
                if len(self._cache) > self.maxsize:
                    oldest_key = next(iter(self._cache))
                    del self._cache[oldest_key]
    
    async def clear(self):
        """Clear all cached values."""
        async with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
            self._expirations = 0
    
    def info(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            'size': len(self._cache),
            'maxsize': self.maxsize,
            'ttl': self.ttl,
            'hits': self._hits,
            'misses': self._misses,
            'expirations': self._expirations,
            'hit_rate': self._hits / (self._hits + self._misses) if (self._hits + self._misses) > 0 else 0.0,
        }


# Global registries
_async_lru_caches: Dict[str, AsyncLRUCache] = {}
_async_ttl_caches: Dict[str, AsyncTTLCache] = {}
_async_lock = threading.Lock()


def async_memoize(
    maxsize: int = 128,
    name: Optional[str] = None,
) -> Callable:
    """
    Memoization decorator for async functions.
    
    Args:
        maxsize: Maximum number of items to cache.
        name: Optional name for cache management.
    
    Returns:
        Decorated async function with caching.
    
    Example:
        @async_memoize(maxsize=100)
        async def fetch_user(user_id):
            # Async API call
            async with aiohttp.ClientSession() as session:
                async with session.get(f'/users/{user_id}') as resp:
                    return await resp.json()
        
        # First call: fetches from API
        user = await fetch_user(123)
        
        # Second call: returns cached result
        user = await fetch_user(123)
    """
    def decorator(func: F) -> F:
        cache = AsyncLRUCache(maxsize=maxsize)
        
        # Register cache
        cache_name = name or f"{func.__module__}.{func.__name__}"
        with _async_lock:
            _async_lru_caches[cache_name] = cache
        
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key
            key = (args, frozenset(sorted(kwargs.items()))) if kwargs else args
            
            # Check cache
            found, value = await cache.get(key)
            if found:
                return value
            
            # Compute and cache
            result = await func(*args, **kwargs)
            await cache.set(key, result)
            
            return result
        
        wrapper.cache_clear = cache.clear
        wrapper.cache_info = cache.info
        wrapper._cache = cache
        
        return wrapper
    
    return decorator


def async_ttl_memoize(
    ttl: float = 300.0,
    maxsize: Optional[int] = None,
    name: Optional[str] = None,
) -> Callable:
    """
    TTL memoization decorator for async functions.
    
    Args:
        ttl: Time-to-live in seconds.
        maxsize: Maximum cache size. None for unlimited.
        name: Optional name for cache management.
    
    Returns:
        Decorated async function with TTL caching.
    
    Example:
        @async_ttl_memoize(ttl=60.0)
        async def fetch_stock_price(symbol):
            # Fetch stock price (cached for 60 seconds)
            async with aiohttp.ClientSession() as session:
                async with session.get(f'/stocks/{symbol}') as resp:
                    return await resp.json()
    """
    def decorator(func: F) -> F:
        cache = AsyncTTLCache(ttl=ttl, maxsize=maxsize)
        
        # Register cache
        cache_name = name or f"{func.__module__}.{func.__name__}"
        with _async_lock:
            _async_ttl_caches[cache_name] = cache
        
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key
            key = (args, frozenset(sorted(kwargs.items()))) if kwargs else args
            
            # Check cache
            found, value = await cache.get(key)
            if found:
                return value
            
            # Compute and cache
            result = await func(*args, **kwargs)
            await cache.set(key, result)
            
            return result
        
        wrapper.cache_clear = cache.clear
        wrapper.cache_info = cache.info
        wrapper._cache = cache
        
        return wrapper
    
    return decorator


def async_lru_memoize(
    maxsize: int = 128,
    name: Optional[str] = None,
) -> Callable:
    """
    LRU memoization for async functions (alias for async_memoize).
    
    Args:
        maxsize: Maximum number of items to cache.
        name: Optional name for cache management.
    
    Returns:
        Decorated async function with LRU caching.
    """
    return async_memoize(maxsize=maxsize, name=name)


async def clear_async_caches():
    """Clear all async caches."""
    async def clear_lru():
        for cache in _async_lru_caches.values():
            await cache.clear()
    
    async def clear_ttl():
        for cache in _async_ttl_caches.values():
            await cache.clear()
    
    await asyncio.gather(clear_lru(), clear_ttl())


def get_async_cache_info(name: Optional[str] = None) -> Dict[str, Any]:
    """Get information about async caches."""
    result = {}
    
    if name:
        if name in _async_lru_caches:
            result[f"{name}_lru"] = _async_lru_caches[name].info()
        if name in _async_ttl_caches:
            result[f"{name}_ttl"] = _async_ttl_caches[name].info()
    else:
        for cache_name, cache in _async_lru_caches.items():
            result[f"{cache_name}_lru"] = cache.info()
        for cache_name, cache in _async_ttl_caches.items():
            result[f"{cache_name}_ttl"] = cache.info()
    
    return result


class AsyncMemoizeContext:
    """
    Async context manager for temporary caching.
    
    Example:
        async with AsyncMemoizeContext(maxsize=100) as cache:
            @cache.decorate
            async def fetch_data(url):
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        return await resp.json()
            
            data = await fetch_data('/api/data')  # Cached within context
    """
    
    def __init__(self, maxsize: int = 128):
        self.maxsize = maxsize
        self.cache = AsyncLRUCache(maxsize=maxsize)
    
    def decorate(self, func: F) -> F:
        """Decorate an async function to use this cache."""
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = (args, frozenset(sorted(kwargs.items()))) if kwargs else args
            found, value = await self.cache.get(key)
            if found:
                return value
            result = await func(*args, **kwargs)
            await self.cache.set(key, result)
            return result
        
        return wrapper
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.cache.clear()
    
    def info(self):
        return self.cache.info()


class AsyncTTLMemoizeContext:
    """
    Async context manager for temporary TTL caching.
    
    Example:
        async with AsyncTTLMemoizeContext(ttl=60.0) as cache:
            @cache.decorate
            async def fetch_data(url):
                # Cached for 60 seconds
                ...
    """
    
    def __init__(self, ttl: float = 300.0, maxsize: Optional[int] = None):
        self.ttl = ttl
        self.maxsize = maxsize
        self.cache = AsyncTTLCache(ttl=ttl, maxsize=maxsize)
    
    def decorate(self, func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = (args, frozenset(sorted(kwargs.items()))) if kwargs else args
            found, value = await self.cache.get(key)
            if found:
                return value
            result = await func(*args, **kwargs)
            await self.cache.set(key, result)
            return result
        
        return wrapper
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.cache.clear()
    
    def info(self):
        return self.cache.info()