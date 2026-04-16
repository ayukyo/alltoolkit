"""
Memoization Utils - A comprehensive function memoization/caching toolkit.

This module provides various memoization decorators and utilities for
caching function results to improve performance.
"""

from .memoize import (
    memoize,
    memoize_method,
    MemoizeStats,
)

from .lru_memoize import (
    lru_memoize,
    lru_memoize_method,
    clear_lru_caches,
    get_lru_cache_info,
)

from .ttl_memoize import (
    ttl_memoize,
    ttl_memoize_method,
    clear_ttl_caches,
    TTLMemoizeStats,
)

from .disk_memoize import (
    disk_memoize,
    disk_memoize_method,
    clear_disk_cache,
    get_disk_cache_stats,
    DiskMemoizeStats,
)

from .async_memoize import (
    async_memoize,
    async_ttl_memoize,
    async_lru_memoize,
    clear_async_caches,
)

__version__ = '1.0.0'
__all__ = [
    # Basic memoize
    'memoize',
    'memoize_method',
    'MemoizeStats',
    
    # LRU memoize
    'lru_memoize',
    'lru_memoize_method',
    'clear_lru_caches',
    'get_lru_cache_info',
    
    # TTL memoize
    'ttl_memoize',
    'ttl_memoize_method',
    'clear_ttl_caches',
    'TTLMemoizeStats',
    
    # Disk memoize
    'disk_memoize',
    'disk_memoize_method',
    'clear_disk_cache',
    'get_disk_cache_stats',
    'DiskMemoizeStats',
    
    # Async memoize
    'async_memoize',
    'async_ttl_memoize',
    'async_lru_memoize',
    'clear_async_caches',
]