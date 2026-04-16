"""
Disk-based memoization implementation.

Provides persistent caching to disk with optional TTL.
"""

import functools
import hashlib
import json
import os
import pickle
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union

F = TypeVar('F', bound=Callable)


@dataclass
class DiskCacheEntry:
    """Metadata for a disk cache entry."""
    key_hash: str
    created_at: float
    expires_at: Optional[float]
    file_extension: str


class DiskMemoizeStats:
    """Statistics for disk memoized functions."""
    
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.disk_reads = 0
        self.disk_writes = 0
        self.errors = 0
    
    @property
    def total_calls(self) -> int:
        return self.hits + self.misses
    
    @property
    def hit_rate(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return self.hits / self.total_calls
    
    def __repr__(self) -> str:
        return (
            f"DiskMemoizeStats(hits={self.hits}, misses={self.misses}, "
            f"reads={self.disk_reads}, writes={self.disk_writes}, "
            f"hit_rate={self.hit_rate:.2%})"
        )


class DiskCache:
    """Thread-safe disk-based cache with optional TTL."""
    
    def __init__(
        self,
        cache_dir: str = ".cache",
        default_ttl: Optional[float] = None,
        max_size_mb: Optional[float] = None,
        serializer: str = "pickle",  # "pickle" or "json"
    ):
        """
        Initialize disk cache.
        
        Args:
            cache_dir: Directory to store cache files.
            default_ttl: Default time-to-live in seconds. None for no expiration.
            max_size_mb: Maximum total cache size in MB. None for unlimited.
            serializer: Serialization method ("pickle" or "json").
        """
        self.cache_dir = Path(cache_dir)
        self.default_ttl = default_ttl
        self.max_size_mb = max_size_mb
        self.serializer = serializer
        self._lock = threading.RLock()
        self._stats = DiskMemoizeStats()
        
        # Create cache directory
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or create metadata
        self._metadata_file = self.cache_dir / ".metadata.json"
        self._metadata: Dict[str, Dict] = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Dict]:
        """Load cache metadata from disk."""
        if self._metadata_file.exists():
            try:
                with open(self._metadata_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_metadata(self):
        """Save cache metadata to disk."""
        try:
            with open(self._metadata_file, 'w') as f:
                json.dump(self._metadata, f, indent=2)
        except IOError:
            pass
    
    def _hash_key(self, key: Any) -> str:
        """Create a hash string from a cache key."""
        try:
            if isinstance(key, (str, int, float, bool)):
                key_str = str(key)
            else:
                key_str = str(key)
            
            return hashlib.md5(key_str.encode()).hexdigest()
        except Exception:
            # Fallback
            return hashlib.md5(str(key).encode()).hexdigest()
    
    def _get_cache_path(self, key_hash: str) -> Path:
        """Get the file path for a cache entry."""
        ext = ".json" if self.serializer == "json" else ".pkl"
        return self.cache_dir / f"{key_hash}{ext}"
    
    def _serialize(self, value: Any) -> bytes:
        """Serialize a value."""
        if self.serializer == "json":
            return json.dumps(value, default=str).encode('utf-8')
        else:
            return pickle.dumps(value)
    
    def _deserialize(self, data: bytes) -> Any:
        """Deserialize a value."""
        if self.serializer == "json":
            return json.loads(data.decode('utf-8'))
        else:
            return pickle.loads(data)
    
    def _is_expired(self, key_hash: str) -> bool:
        """Check if a cache entry is expired."""
        if key_hash not in self._metadata:
            return True
        
        metadata = self._metadata[key_hash]
        if metadata.get("expires_at") is None:
            return False
        
        return time.time() > metadata["expires_at"]
    
    def _cleanup_expired(self):
        """Remove expired entries."""
        current_time = time.time()
        expired_keys = [
            key_hash for key_hash, meta in self._metadata.items()
            if meta.get("expires_at") is not None and current_time > meta["expires_at"]
        ]
        
        for key_hash in expired_keys:
            self._delete_entry(key_hash)
    
    def _delete_entry(self, key_hash: str):
        """Delete a cache entry."""
        cache_path = self._get_cache_path(key_hash)
        try:
            if cache_path.exists():
                cache_path.unlink()
        except IOError:
            pass
        
        if key_hash in self._metadata:
            del self._metadata[key_hash]
    
    def _check_size_limit(self):
        """Check and enforce size limit by removing old entries."""
        if self.max_size_mb is None:
            return
        
        max_bytes = self.max_size_mb * 1024 * 1024
        total_size = sum(
            self._get_cache_path(k).stat().st_size
            for k in self._metadata
            if self._get_cache_path(k).exists()
        )
        
        if total_size <= max_bytes:
            return
        
        # Sort by creation time and remove oldest
        sorted_keys = sorted(
            self._metadata.keys(),
            key=lambda k: self._metadata[k].get("created_at", 0)
        )
        
        for key_hash in sorted_keys:
            if total_size <= max_bytes:
                break
            
            cache_path = self._get_cache_path(key_hash)
            if cache_path.exists():
                total_size -= cache_path.stat().st_size
                self._delete_entry(key_hash)
        
        self._save_metadata()
    
    def get(self, key: Any) -> Tuple[bool, Any]:
        """Get a value from cache. Returns (found, value)."""
        with self._lock:
            key_hash = self._hash_key(key)
            
            # Check if entry exists and is not expired
            if key_hash not in self._metadata or self._is_expired(key_hash):
                self._stats.misses += 1
                return False, None
            
            # Read from disk
            cache_path = self._get_cache_path(key_hash)
            if not cache_path.exists():
                self._stats.misses += 1
                return False, None
            
            try:
                with open(cache_path, 'rb') as f:
                    data = f.read()
                value = self._deserialize(data)
                self._stats.hits += 1
                self._stats.disk_reads += 1
                return True, value
            except Exception as e:
                self._stats.misses += 1
                self._stats.errors += 1
                return False, None
    
    def set(self, key: Any, value: Any, ttl: Optional[float] = None):
        """Set a value in cache."""
        with self._lock:
            key_hash = self._hash_key(key)
            ttl = ttl if ttl is not None else self.default_ttl
            current_time = time.time()
            
            # Write to disk
            cache_path = self._get_cache_path(key_hash)
            try:
                data = self._serialize(value)
                with open(cache_path, 'wb') as f:
                    f.write(data)
                
                self._stats.disk_writes += 1
                
                # Update metadata
                self._metadata[key_hash] = {
                    "created_at": current_time,
                    "expires_at": current_time + ttl if ttl is not None else None,
                }
                
                self._save_metadata()
                self._check_size_limit()
                
            except Exception as e:
                self._stats.errors += 1
    
    def delete(self, key: Any) -> bool:
        """Delete a key from cache."""
        with self._lock:
            key_hash = self._hash_key(key)
            if key_hash in self._metadata:
                self._delete_entry(key_hash)
                self._save_metadata()
                return True
            return False
    
    def clear(self):
        """Clear all cached values."""
        with self._lock:
            for key_hash in list(self._metadata.keys()):
                self._delete_entry(key_hash)
            self._save_metadata()
    
    def __len__(self) -> int:
        return len(self._metadata)
    
    def info(self) -> Dict[str, Any]:
        """Get cache statistics and info."""
        with self._lock:
            self._cleanup_expired()
            total_size = sum(
                self._get_cache_path(k).stat().st_size
                for k in self._metadata
                if self._get_cache_path(k).exists()
            )
            
            return {
                'size': len(self._metadata),
                'cache_dir': str(self.cache_dir),
                'total_size_bytes': total_size,
                'total_size_mb': total_size / (1024 * 1024),
                'max_size_mb': self.max_size_mb,
                'default_ttl': self.default_ttl,
                'serializer': self.serializer,
                'stats': self._stats,
            }


# Global registry of disk caches
_disk_caches: Dict[str, DiskCache] = {}
_disk_lock = threading.Lock()


def disk_memoize(
    cache_dir: str = ".cache",
    ttl: Optional[float] = None,
    max_size_mb: Optional[float] = None,
    serializer: str = "pickle",
    name: Optional[str] = None,
) -> Callable:
    """
    Disk-based memoization decorator with persistence.
    
    Cached values persist across process restarts.
    
    Args:
        cache_dir: Directory to store cache files.
        ttl: Time-to-live in seconds. None for no expiration.
        max_size_mb: Maximum total cache size in MB.
        serializer: Serialization method ("pickle" or "json").
        name: Optional name for cache management.
    
    Returns:
        Decorated function with disk-based caching.
    
    Example:
        @disk_memoize(cache_dir=".my_cache", ttl=3600)
        def fetch_large_dataset(url):
            # Expensive operation that fetches large data
            return requests.get(url).json()
        
        # First call: computes and caches to disk
        data = fetch_large_dataset("https://api.example.com/data")
        
        # Subsequent calls: reads from disk
        data = fetch_large_dataset("https://api.example.com/data")
        
        # Even after process restart, cache persists!
    """
    def decorator(func: F) -> F:
        cache = DiskCache(
            cache_dir=cache_dir,
            default_ttl=ttl,
            max_size_mb=max_size_mb,
            serializer=serializer,
        )
        
        # Register cache
        cache_name = name or f"{func.__module__}.{func.__name__}"
        with _disk_lock:
            _disk_caches[cache_name] = cache
        
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


def disk_memoize_method(
    cache_dir: str = ".cache",
    ttl: Optional[float] = None,
    max_size_mb: Optional[float] = None,
    serializer: str = "pickle",
) -> Callable:
    """
    Disk-based memoization for instance methods.
    
    Each instance has its own cache subdirectory.
    """
    def decorator(method: F) -> F:
        caches: Dict[int, DiskCache] = {}
        
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            instance_id = id(self)
            
            # Get or create cache for this instance
            if instance_id not in caches:
                instance_cache_dir = f"{cache_dir}/{type(self).__name__}_{instance_id}"
                caches[instance_id] = DiskCache(
                    cache_dir=instance_cache_dir,
                    default_ttl=ttl,
                    max_size_mb=max_size_mb,
                    serializer=serializer,
                )
            
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
            return None
        
        wrapper.cache_clear = cache_clear
        wrapper.cache_info = cache_info
        
        return wrapper
    
    return decorator


def clear_disk_cache(name: Optional[str] = None):
    """Clear disk cache(s)."""
    with _disk_lock:
        if name:
            if name in _disk_caches:
                _disk_caches[name].clear()
        else:
            for cache in _disk_caches.values():
                cache.clear()


def get_disk_cache_stats(name: Optional[str] = None) -> Dict[str, Any]:
    """Get disk cache statistics."""
    with _disk_lock:
        if name:
            if name in _disk_caches:
                return {name: _disk_caches[name].info()}
            return {}
        
        return {
            cache_name: cache.info()
            for cache_name, cache in _disk_caches.items()
        }