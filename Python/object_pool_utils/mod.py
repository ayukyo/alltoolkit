"""
AllToolkit - Python Object Pool Utilities

A zero-dependency, production-ready object pool implementation for efficient
resource management. Provides thread-safe object pooling with automatic cleanup,
validation, and statistics tracking.

Features:
- Generic object pooling pattern
- Thread-safe operations with configurable timeout
- Object validation and recycling
- Automatic idle object eviction
- Pool statistics and monitoring
- Context manager support
- Connection pool base class

Author: AllToolkit
License: MIT
"""

import threading
import time
import queue
from typing import (
    TypeVar, Generic, Callable, Optional, List, Dict, Any,
    ContextManager, Type, Union
)
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from contextlib import contextmanager
from datetime import datetime


T = TypeVar('T')


@dataclass
class PoolStats:
    """Pool statistics container."""
    total_created: int = 0
    total_destroyed: int = 0
    total_borrowed: int = 0
    total_returned: int = 0
    total_validation_failures: int = 0
    current_idle: int = 0
    current_active: int = 0
    max_borrowed_at_once: int = 0
    total_wait_time_ms: float = 0.0
    total_borrow_count: int = 0
    
    @property
    def avg_wait_time_ms(self) -> float:
        """Average wait time for borrowing objects."""
        if self.total_borrow_count == 0:
            return 0.0
        return self.total_wait_time_ms / self.total_borrow_count
    
    @property
    def utilization_rate(self) -> float:
        """Current pool utilization rate (0.0 - 1.0)."""
        total = self.current_idle + self.current_active
        if total == 0:
            return 0.0
        return self.current_active / total
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'total_created': self.total_created,
            'total_destroyed': self.total_destroyed,
            'total_borrowed': self.total_borrowed,
            'total_returned': self.total_returned,
            'total_validation_failures': self.total_validation_failures,
            'current_idle': self.current_idle,
            'current_active': self.current_active,
            'max_borrowed_at_once': self.max_borrowed_at_once,
            'avg_wait_time_ms': self.avg_wait_time_ms,
            'utilization_rate': self.utilization_rate,
        }


@dataclass
class PooledObject(Generic[T]):
    """Wrapper for pooled objects with metadata."""
    obj: T
    created_at: float = field(default_factory=time.time)
    last_used_at: float = field(default_factory=time.time)
    borrow_count: int = 0
    is_valid: bool = True


class ObjectPool(Generic[T]):
    """
    Thread-safe generic object pool.
    
    Manages a pool of reusable objects to avoid expensive creation/destruction
    overhead. Objects are created on-demand up to a maximum size, and idle
    objects can be evicted after a configurable timeout.
    
    Features:
    - Thread-safe borrow/return operations
    - Object validation before reuse
    - Automatic idle object eviction
    - Pool statistics tracking
    - Context manager support for borrowed objects
    
    Example:
        >>> def create_connection():
        ...     return {'id': id(object()), 'connected': True}
        ...
        >>> pool = ObjectPool(
        ...     factory=create_connection,
        ...     max_size=10,
        ...     validate=lambda obj: obj.get('connected', False)
        ... )
        >>> with pool.borrow() as conn:
        ...     print(conn['id'])
    """
    
    def __init__(
        self,
        factory: Callable[[], T],
        destructor: Optional[Callable[[T], None]] = None,
        validator: Optional[Callable[[T], bool]] = None,
        reset: Optional[Callable[[T], None]] = None,
        max_size: int = 10,
        min_idle: int = 0,
        max_idle_time: float = 300.0,
        borrow_timeout: float = 30.0,
        validation_on_borrow: bool = True,
        validation_on_return: bool = False,
        reset_on_return: bool = True,
    ):
        """
        Initialize the object pool.
        
        Args:
            factory: Function to create new objects
            destructor: Function to destroy objects (optional)
            validator: Function to validate objects (optional)
            reset: Function to reset object state (optional)
            max_size: Maximum number of objects in pool
            min_idle: Minimum number of idle objects to maintain
            max_idle_time: Max seconds an idle object can exist (0 = no limit)
            borrow_timeout: Max seconds to wait for available object
            validation_on_borrow: Validate objects before borrowing
            validation_on_return: Validate objects when returning
            reset_on_return: Reset objects when returning
        """
        if max_size < 1:
            raise ValueError("max_size must be at least 1")
        if min_idle > max_size:
            raise ValueError("min_idle cannot exceed max_size")
        if borrow_timeout < 0:
            raise ValueError("borrow_timeout cannot be negative")
        
        self._factory = factory
        self._destructor = destructor
        self._validator = validator or (lambda x: True)
        self._reset = reset
        self._max_size = max_size
        self._min_idle = min_idle
        self._max_idle_time = max_idle_time
        self._borrow_timeout = borrow_timeout
        self._validation_on_borrow = validation_on_borrow
        self._validation_on_return = validation_on_return
        self._reset_on_return = reset_on_return
        
        self._idle: queue.Queue[PooledObject[T]] = queue.Queue()
        self._active: Dict[int, PooledObject[T]] = {}
        self._lock = threading.RLock()
        self._stats = PoolStats()
        self._closed = False
        self._eviction_thread: Optional[threading.Thread] = None
        self._eviction_stop = threading.Event()
        
        # Pre-populate min_idle objects
        self._initialize_min_idle()
        
        # Start eviction thread if max_idle_time > 0
        if self._max_idle_time > 0:
            self._start_eviction_thread()
    
    def _initialize_min_idle(self) -> None:
        """Pre-populate minimum idle objects."""
        for _ in range(self._min_idle):
            try:
                obj = self._create_object()
                self._idle.put(obj)
                self._stats.current_idle += 1
            except Exception:
                break
    
    def _create_object(self) -> PooledObject[T]:
        """Create a new pooled object."""
        obj = self._factory()
        pooled = PooledObject(obj=obj)
        self._stats.total_created += 1
        return pooled
    
    def _destroy_object(self, pooled: PooledObject[T]) -> None:
        """Destroy a pooled object."""
        if self._destructor:
            try:
                self._destructor(pooled.obj)
            except Exception:
                pass
        self._stats.total_destroyed += 1
    
    def _validate_object(self, pooled: PooledObject[T]) -> bool:
        """Validate a pooled object."""
        try:
            is_valid = self._validator(pooled.obj)
            pooled.is_valid = is_valid
            if not is_valid:
                self._stats.total_validation_failures += 1
            return is_valid
        except Exception:
            pooled.is_valid = False
            self._stats.total_validation_failures += 1
            return False
    
    def _reset_object(self, pooled: PooledObject[T]) -> None:
        """Reset a pooled object's state."""
        if self._reset:
            try:
                self._reset(pooled.obj)
            except Exception:
                pass
    
    def _start_eviction_thread(self) -> None:
        """Start the background eviction thread."""
        def evict_idle():
            while not self._eviction_stop.is_set():
                try:
                    self.evict_idle_objects()
                except Exception:
                    pass
                # Check every 10% of max_idle_time or at least every second
                sleep_time = max(1.0, self._max_idle_time / 10)
                self._eviction_stop.wait(timeout=sleep_time)
        
        self._eviction_thread = threading.Thread(
            target=evict_idle,
            daemon=True,
            name=f"ObjectPool-Eviction-{id(self)}"
        )
        self._eviction_thread.start()
    
    def _stop_eviction_thread(self) -> None:
        """Stop the background eviction thread."""
        if self._eviction_thread:
            self._eviction_stop.set()
            self._eviction_thread.join(timeout=5.0)
            self._eviction_thread = None
    
    def borrow(self, timeout: Optional[float] = None) -> T:
        """
        Borrow an object from the pool.
        
        Args:
            timeout: Max seconds to wait (uses pool default if None)
            
        Returns:
            A pooled object
            
        Raises:
            RuntimeError: If pool is closed
            TimeoutError: If no object available within timeout
        """
        if self._closed:
            raise RuntimeError("Pool is closed")
        
        timeout = timeout if timeout is not None else self._borrow_timeout
        start_time = time.time()
        
        with self._lock:
            total_count = self._stats.current_idle + self._stats.current_active
            can_create = total_count < self._max_size
        
        # Try to get from idle queue
        pooled = None
        while True:
            try:
                pooled = self._idle.get_nowait()
                with self._lock:
                    self._stats.current_idle -= 1
            except queue.Empty:
                break
            
            # Validate if needed
            if self._validation_on_borrow and not self._validate_object(pooled):
                self._destroy_object(pooled)
                pooled = None
                continue
            
            break
        
        # Create new if possible
        if pooled is None:
            with self._lock:
                total_count = self._stats.current_idle + self._stats.current_active
                if total_count < self._max_size:
                    pooled = self._create_object()
                    pooled.borrow_count = 1
                else:
                    # Wait for an object to be returned
                    wait_remaining = timeout - (time.time() - start_time)
                    if wait_remaining <= 0:
                        raise TimeoutError("No object available within timeout")
                    
                    # Release lock and wait
                    try:
                        pooled = self._idle.get(timeout=wait_remaining)
                        with self._lock:
                            self._stats.current_idle -= 1
                        
                        if self._validation_on_borrow and not self._validate_object(pooled):
                            self._destroy_object(pooled)
                            pooled = None
                            # Recursively try again
                            return self.borrow(timeout - (time.time() - start_time))
                    except queue.Empty:
                        raise TimeoutError("No object available within timeout")
        
        # Register as active
        with self._lock:
            obj_id = id(pooled.obj)
            self._active[obj_id] = pooled
            self._stats.current_active += 1
            self._stats.total_borrowed += 1
            self._stats.total_borrow_count += 1
            self._stats.max_borrowed_at_once = max(
                self._stats.max_borrowed_at_once,
                self._stats.current_active
            )
        
        pooled.last_used_at = time.time()
        pooled.borrow_count += 1
        
        wait_time = time.time() - start_time
        self._stats.total_wait_time_ms += wait_time * 1000
        
        return pooled.obj
    
    def return_object(self, obj: T) -> None:
        """
        Return an object to the pool.
        
        Args:
            obj: The object to return
            
        Note:
            Silently ignores objects not tracked by this pool.
        """
        if self._closed:
            # Destroy object if pool is closed
            if self._destructor:
                try:
                    self._destructor(obj)
                except Exception:
                    pass
            return
        
        obj_id = id(obj)
        
        with self._lock:
            pooled = self._active.pop(obj_id, None)
            if pooled is None:
                # Not from this pool, ignore
                return
            
            self._stats.current_active -= 1
            self._stats.total_returned += 1
        
        # Validate on return if configured
        if self._validation_on_return and not self._validate_object(pooled):
            self._destroy_object(pooled)
            return
        
        # Reset object state if configured
        if self._reset_on_return:
            self._reset_object(pooled)
        
        # Return to idle pool
        pooled.last_used_at = time.time()
        
        with self._lock:
            total_count = self._stats.current_idle + self._stats.current_active
            # Don't exceed max_size
            if total_count >= self._max_size:
                self._destroy_object(pooled)
                return
            
            self._idle.put(pooled)
            self._stats.current_idle += 1
    
    @contextmanager
    def use(self, timeout: Optional[float] = None):
        """
        Context manager for borrowing and returning objects.
        
        Args:
            timeout: Max seconds to wait for an object
            
        Yields:
            A pooled object
            
        Example:
            >>> with pool.use() as conn:
            ...     conn.execute("SELECT 1")
        """
        obj = self.borrow(timeout=timeout)
        try:
            yield obj
        finally:
            self.return_object(obj)
    
    def evict_idle_objects(self) -> int:
        """
        Evict idle objects that have exceeded max_idle_time.
        
        Returns:
            Number of objects evicted
        """
        if self._max_idle_time <= 0:
            return 0
        
        evicted = 0
        now = time.time()
        temp_list = []
        
        # Drain the idle queue
        while True:
            try:
                pooled = self._idle.get_nowait()
                temp_list.append(pooled)
            except queue.Empty:
                break
        
        # Check each object
        for pooled in temp_list:
            idle_time = now - pooled.last_used_at
            should_evict = idle_time > self._max_idle_time
            
            # Don't evict below min_idle
            with self._lock:
                if should_evict and self._stats.current_idle <= self._min_idle:
                    should_evict = False
            
            if should_evict:
                self._destroy_object(pooled)
                evicted += 1
                with self._lock:
                    self._stats.current_idle -= 1
            else:
                self._idle.put(pooled)
        
        return evicted
    
    def clear(self) -> None:
        """Clear all idle objects from the pool."""
        while True:
            try:
                pooled = self._idle.get_nowait()
                self._destroy_object(pooled)
                with self._lock:
                    self._stats.current_idle -= 1
            except queue.Empty:
                break
    
    def close(self) -> None:
        """
        Close the pool and destroy all objects.
        
        After closing, the pool cannot be used.
        """
        if self._closed:
            return
        
        self._closed = True
        self._stop_eviction_thread()
        
        # Destroy all idle objects
        self.clear()
        
        # Destroy all active objects
        with self._lock:
            for pooled in self._active.values():
                self._destroy_object(pooled)
            self._active.clear()
            self._stats.current_active = 0
    
    def get_stats(self) -> PoolStats:
        """Get pool statistics."""
        return self._stats
    
    @property
    def is_closed(self) -> bool:
        """Check if pool is closed."""
        return self._closed
    
    @property
    def size(self) -> int:
        """Total number of objects (idle + active)."""
        with self._lock:
            return self._stats.current_idle + self._stats.current_active
    
    @property
    def idle_count(self) -> int:
        """Number of idle objects."""
        return self._stats.current_idle
    
    @property
    def active_count(self) -> int:
        """Number of active (borrowed) objects."""
        return self._stats.current_active
    
    def __enter__(self) -> 'ObjectPool[T]':
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
    
    def __repr__(self) -> str:
        return (
            f"ObjectPool(size={self.size}, idle={self.idle_count}, "
            f"active={self.active_count}, max_size={self._max_size})"
        )


class ConnectionPool(ObjectPool[T], Generic[T]):
    """
    Specialized object pool for connection-like resources.
    
    Extends ObjectPool with connection-specific features like
    health checks, connection recycling, and automatic reconnection.
    
    Example:
        >>> import socket
        ...
        >>> def create_socket():
        ...     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ...     s.connect(('example.com', 80))
        ...     return s
        ...
        >>> def close_socket(s):
        ...     s.close()
        ...
        >>> def is_socket_alive(s):
        ...     # Simple check - might fail if socket was closed
        ...     try:
        ...         s.getpeername()
        ...         return True
        ...     except:
        ...         return False
        ...
        >>> pool = ConnectionPool(
        ...     factory=create_socket,
        ...     destructor=close_socket,
        ...     validator=is_socket_alive,
        ...     max_size=5
        ... )
    """
    
    def __init__(
        self,
        factory: Callable[[], T],
        destructor: Optional[Callable[[T], None]] = None,
        validator: Optional[Callable[[T], bool]] = None,
        max_size: int = 10,
        min_idle: int = 1,
        max_idle_time: float = 300.0,
        borrow_timeout: float = 30.0,
        max_lifetime: float = 3600.0,
        max_usage_count: int = 0,
    ):
        """
        Initialize connection pool.
        
        Args:
            factory: Function to create new connections
            destructor: Function to close connections
            validator: Function to check connection health
            max_size: Maximum connections in pool
            min_idle: Minimum idle connections to maintain
            max_idle_time: Max seconds before idle connection is closed
            borrow_timeout: Max seconds to wait for available connection
            max_lifetime: Max seconds a connection can exist (0 = no limit)
            max_usage_count: Max times a connection can be reused (0 = no limit)
        """
        super().__init__(
            factory=factory,
            destructor=destructor,
            validator=validator,
            max_size=max_size,
            min_idle=min_idle,
            max_idle_time=max_idle_time,
            borrow_timeout=borrow_timeout,
            validation_on_borrow=True,
            validation_on_return=False,
            reset_on_return=False,
        )
        self._max_lifetime = max_lifetime
        self._max_usage_count = max_usage_count
    
    def borrow(self, timeout: Optional[float] = None) -> T:
        """Borrow a connection from the pool."""
        obj = super().borrow(timeout=timeout)
        
        # Check if connection should be recycled
        obj_id = id(obj)
        with self._lock:
            pooled = self._active.get(obj_id)
            if pooled:
                now = time.time()
                age = now - pooled.created_at
                
                # Check lifetime
                if self._max_lifetime > 0 and age > self._max_lifetime:
                    # Connection too old, destroy and get new one
                    self._destroy_object(pooled)
                    self._active.pop(obj_id, None)
                    self._stats.current_active -= 1
                    return self.borrow(timeout=timeout)
                
                # Check usage count
                if self._max_usage_count > 0 and pooled.borrow_count > self._max_usage_count:
                    # Connection overused, destroy and get new one
                    self._destroy_object(pooled)
                    self._active.pop(obj_id, None)
                    self._stats.current_active -= 1
                    return self.borrow(timeout=timeout)
        
        return obj
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on all connections.
        
        Returns:
            Health check results
        """
        results = {
            'healthy': 0,
            'unhealthy': 0,
            'destroyed': 0,
            'errors': [],
        }
        
        # Check idle connections
        temp_list = []
        while True:
            try:
                pooled = self._idle.get_nowait()
                temp_list.append(pooled)
            except queue.Empty:
                break
        
        for pooled in temp_list:
            if self._validate_object(pooled):
                results['healthy'] += 1
                self._idle.put(pooled)
            else:
                results['unhealthy'] += 1
                self._destroy_object(pooled)
                with self._lock:
                    self._stats.current_idle -= 1
                results['destroyed'] += 1
        
        return results


class PoolManager:
    """
    Manager for multiple named object pools.
    
    Useful for managing multiple pools of different types or
    configurations in a centralized way.
    
    Example:
        >>> manager = PoolManager()
        >>> manager.create_pool(
        ...     'connections',
        ...     factory=lambda: {'id': id(object())},
        ...     max_size=5
        ... )
        >>> with manager.borrow('connections') as conn:
        ...     print(conn['id'])
    """
    
    def __init__(self):
        """Initialize the pool manager."""
        self._pools: Dict[str, ObjectPool] = {}
        self._lock = threading.RLock()
    
    def create_pool(
        self,
        name: str,
        factory: Callable[[], T],
        **kwargs
    ) -> ObjectPool[T]:
        """
        Create and register a new pool.
        
        Args:
            name: Pool name
            factory: Object factory function
            **kwargs: Additional pool configuration
            
        Returns:
            The created pool
        """
        with self._lock:
            if name in self._pools:
                raise ValueError(f"Pool '{name}' already exists")
            
            pool = ObjectPool(factory=factory, **kwargs)
            self._pools[name] = pool
            return pool
    
    def get_pool(self, name: str) -> Optional[ObjectPool]:
        """Get a pool by name."""
        return self._pools.get(name)
    
    def borrow(self, name: str, timeout: Optional[float] = None) -> Any:
        """Borrow an object from a named pool."""
        pool = self._pools.get(name)
        if pool is None:
            raise KeyError(f"Pool '{name}' not found")
        return pool.borrow(timeout=timeout)
    
    def return_object(self, name: str, obj: Any) -> None:
        """Return an object to a named pool."""
        pool = self._pools.get(name)
        if pool:
            pool.return_object(obj)
    
    @contextmanager
    def use(self, name: str, timeout: Optional[float] = None):
        """Context manager for borrowing from a named pool."""
        obj = self.borrow(name, timeout=timeout)
        try:
            yield obj
        finally:
            self.return_object(name, obj)
    
    def get_all_stats(self) -> Dict[str, PoolStats]:
        """Get statistics for all pools."""
        return {name: pool.get_stats() for name, pool in self._pools.items()}
    
    def close_all(self) -> None:
        """Close all pools."""
        with self._lock:
            for pool in self._pools.values():
                pool.close()
            self._pools.clear()
    
    def close_pool(self, name: str) -> bool:
        """Close and remove a specific pool."""
        with self._lock:
            pool = self._pools.pop(name, None)
            if pool:
                pool.close()
                return True
            return False
    
    def __enter__(self) -> 'PoolManager':
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close_all()


# Convenience functions

def create_pool(
    factory: Callable[[], T],
    max_size: int = 10,
    **kwargs
) -> ObjectPool[T]:
    """
    Create an object pool with default settings.
    
    Args:
        factory: Function to create objects
        max_size: Maximum pool size
        **kwargs: Additional pool configuration
        
    Returns:
        Configured ObjectPool instance
    """
    return ObjectPool(factory=factory, max_size=max_size, **kwargs)


def create_connection_pool(
    factory: Callable[[], T],
    destructor: Optional[Callable[[T], None]] = None,
    validator: Optional[Callable[[T], bool]] = None,
    max_size: int = 10,
    **kwargs
) -> ConnectionPool[T]:
    """
    Create a connection pool with default settings.
    
    Args:
        factory: Function to create connections
        destructor: Function to destroy connections
        validator: Function to validate connections
        max_size: Maximum pool size
        **kwargs: Additional pool configuration
        
    Returns:
        Configured ConnectionPool instance
    """
    return ConnectionPool(
        factory=factory,
        destructor=destructor,
        validator=validator,
        max_size=max_size,
        **kwargs
    )


# Example pooled resource classes

class PooledStringBuilder:
    """Example of a pooled resource for efficient string building."""
    
    def __init__(self, initial_size: int = 1024):
        self._buffer = []
        self._initial_size = initial_size
    
    def append(self, s: str) -> 'PooledStringBuilder':
        self._buffer.append(s)
        return self
    
    def build(self) -> str:
        return ''.join(self._buffer)
    
    def clear(self) -> None:
        self._buffer.clear()
    
    def __str__(self) -> str:
        return self.build()


class PooledList(list):
    """Example of a pooled list that can be reset."""
    
    def reset(self) -> None:
        self.clear()


class PooledDict(dict):
    """Example of a pooled dict that can be reset."""
    
    def reset(self) -> None:
        self.clear()


if __name__ == '__main__':
    # Basic demo
    print("Object Pool Demo")
    print("=" * 60)
    
    # Create a simple pool
    def create_resource():
        return {'id': id(object()), 'data': []}
    
    with ObjectPool(
        factory=create_resource,
        max_size=3,
        min_idle=1
    ) as pool:
        print(f"Pool created: {pool}")
        
        # Borrow and use
        with pool.use() as obj:
            obj['data'].append('test')
            print(f"Borrowed object: {obj['id']}")
        
        print(f"After use: {pool}")
        print(f"Stats: {pool.get_stats().to_dict()}")
    
    print("\nDemo complete!")