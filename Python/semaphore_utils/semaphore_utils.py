"""
Semaphore utilities for Python.

A semaphore is a synchronization primitive that limits the number of concurrent
operations. This module provides enhanced semaphore implementations with:

- Standard counting semaphores with timeout support
- Weighted semaphores for variable resource allocation
- Semaphore pools for managing multiple resources
- Async/await support
- Context manager protocol
- Zero external dependencies (uses only Python standard library)

Example usage:

    # Basic semaphore
    sem = Semaphore(10)
    
    with sem:
        # Do work with permit held
        process_data()
    
    # Weighted semaphore
    weighted = WeightedSemaphore(100)
    with weighted.acquire(20):
        # Use 20 units of resource
        process_large_data()

Author: AllToolkit
Date: 2026-04-29
Version: 1.0.0
License: MIT
"""

import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, TypeVar
from enum import Enum
import asyncio
from functools import wraps

__all__ = [
    'Semaphore',
    'WeightedSemaphore',
    'SemaphorePool',
    'AsyncSemaphore',
    'AsyncWeightedSemaphore',
    'BoundedSemaphore',
    'PrioritySemaphore',
    'RateLimiter',
    'ConcurrencyLimit',
    'SemaphoreError',
    'TimeoutError',
    'acquire_all',
    'run_with_semaphore',
]

T = TypeVar('T')


class SemaphoreError(Exception):
    """Base exception for semaphore errors."""
    pass


class TimeoutError(SemaphoreError):
    """Raised when an acquire operation times out."""
    pass


class CancelledError(SemaphoreError):
    """Raised when an acquire operation is cancelled."""
    pass


class Semaphore:
    """
    A counting semaphore with enhanced features.
    
    Limits the number of concurrent operations to a fixed capacity.
    Supports timeouts, non-blocking acquire, and context manager protocol.
    
    Attributes:
        capacity: Maximum number of permits.
    
    Example:
        >>> sem = Semaphore(3)
        >>> sem.try_acquire()
        True
        >>> sem.available()
        2
        >>> sem.release()
        >>> sem.available()
        3
    """
    
    def __init__(self, capacity: int):
        """
        Initialize a semaphore.
        
        Args:
            capacity: Maximum number of permits (must be > 0).
        
        Raises:
            ValueError: If capacity is not positive.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._current = 0
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._waiters = 0
    
    @property
    def capacity(self) -> int:
        """Return the total capacity."""
        return self._capacity
    
    def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Acquire a permit, blocking until available or timeout.
        
        Args:
            timeout: Maximum seconds to wait. None means wait forever.
        
        Returns:
            True if permit was acquired.
        
        Raises:
            TimeoutError: If timeout expires before permit is acquired.
        
        Example:
            >>> sem = Semaphore(1)
            >>> sem.acquire(timeout=1.0)  # Returns True
            True
        """
        start_time = time.monotonic()
        
        with self._condition:
            # Fast path: permit available
            if self._current < self._capacity:
                self._current += 1
                return True
            
            # Slow path: wait for permit
            self._waiters += 1
            try:
                while self._current >= self._capacity:
                    remaining = None
                    if timeout is not None:
                        elapsed = time.monotonic() - start_time
                        remaining = timeout - elapsed
                        if remaining <= 0:
                            raise TimeoutError("Semaphore acquire timeout")
                    
                    if not self._condition.wait(remaining):
                        if timeout is not None:
                            elapsed = time.monotonic() - start_time
                            if elapsed >= timeout:
                                raise TimeoutError("Semaphore acquire timeout")
                
                self._current += 1
                return True
            finally:
                self._waiters -= 1
    
    def try_acquire(self) -> bool:
        """
        Try to acquire a permit without blocking.
        
        Returns:
            True if permit was acquired, False if semaphore is full.
        
        Example:
            >>> sem = Semaphore(1)
            >>> sem.try_acquire()
            True
            >>> sem.try_acquire()  # Already at capacity
            False
        """
        with self._lock:
            if self._current < self._capacity:
                self._current += 1
                return True
            return False
    
    def release(self) -> None:
        """
        Release a permit back to the semaphore.
        
        Example:
            >>> sem = Semaphore(1)
            >>> sem.acquire()
            >>> sem.release()
        """
        with self._condition:
            if self._current > 0:
                self._current -= 1
            self._condition.notify()
    
    def available(self) -> int:
        """
        Return the number of available permits.
        
        Returns:
            Number of permits currently available.
        """
        with self._lock:
            return self._capacity - self._current
    
    def in_use(self) -> int:
        """
        Return the number of permits currently in use.
        
        Returns:
            Number of acquired permits.
        """
        with self._lock:
            return self._current
    
    def waiters(self) -> int:
        """
        Return the number of threads waiting for a permit.
        
        Returns:
            Number of waiting threads.
        """
        with self._lock:
            return self._waiters
    
    def __enter__(self) -> 'Semaphore':
        """Context manager entry - acquires a permit."""
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - releases the permit."""
        self.release()
    
    def __repr__(self) -> str:
        return f"Semaphore(capacity={self._capacity}, in_use={self.in_use()})"


class WeightedSemaphore:
    """
    A weighted semaphore for variable resource allocation.
    
    Allows acquiring multiple units at once, useful when operations
    require different amounts of resources.
    
    Attributes:
        capacity: Total weight capacity.
    
    Example:
        >>> sem = WeightedSemaphore(100)
        >>> sem.acquire(30)  # Acquire 30 units
        True
        >>> sem.available()
        70
        >>> sem.release(30)
        >>> sem.available()
        100
    """
    
    def __init__(self, capacity: int):
        """
        Initialize a weighted semaphore.
        
        Args:
            capacity: Total weight capacity (must be > 0).
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._current = 0
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._waiters: List[tuple] = []  # List of (weight, event)
    
    @property
    def capacity(self) -> int:
        """Return the total capacity."""
        return self._capacity
    
    def acquire(self, weight: int = 1, timeout: Optional[float] = None) -> bool:
        """
        Acquire weight units from the semaphore.
        
        Args:
            weight: Number of units to acquire (must be > 0 and <= capacity).
            timeout: Maximum seconds to wait. None means wait forever.
        
        Returns:
            True if units were acquired.
        
        Raises:
            ValueError: If weight is invalid.
            TimeoutError: If timeout expires.
        """
        if weight <= 0:
            raise ValueError("Weight must be positive")
        if weight > self._capacity:
            raise ValueError("Weight exceeds capacity")
        
        start_time = time.monotonic()
        
        with self._condition:
            # Fast path: enough capacity
            if self._current + weight <= self._capacity:
                self._current += weight
                return True
            
            # Slow path: wait for capacity
            event = threading.Event()
            waiter = (weight, event)
            self._waiters.append(waiter)
            
            try:
                while self._current + weight > self._capacity:
                    remaining = None
                    if timeout is not None:
                        elapsed = time.monotonic() - start_time
                        remaining = timeout - elapsed
                        if remaining <= 0:
                            raise TimeoutError("Semaphore acquire timeout")
                    
                    self._condition.release()
                    try:
                        if not event.wait(remaining):
                            if timeout is not None:
                                elapsed = time.monotonic() - start_time
                                if elapsed >= timeout:
                                    raise TimeoutError("Semaphore acquire timeout")
                    finally:
                        self._condition.acquire()
                
                self._current += weight
                return True
            finally:
                # Remove from waiters
                if waiter in self._waiters:
                    self._waiters.remove(waiter)
    
    def try_acquire(self, weight: int = 1) -> bool:
        """
        Try to acquire weight units without blocking.
        
        Args:
            weight: Number of units to acquire.
        
        Returns:
            True if acquired, False if not enough capacity.
        """
        if weight <= 0 or weight > self._capacity:
            return False
        
        with self._lock:
            if self._current + weight <= self._capacity:
                self._current += weight
                return True
            return False
    
    def release(self, weight: int = 1) -> None:
        """
        Release weight units back to the semaphore.
        
        Args:
            weight: Number of units to release.
        """
        if weight <= 0:
            return
        
        with self._condition:
            self._current = max(0, self._current - weight)
            
            # Notify eligible waiters
            self._notify_waiters()
    
    def _notify_waiters(self) -> None:
        """Notify waiting threads that might now be able to acquire."""
        for weight, event in self._waiters[:]:
            if self._current + weight <= self._capacity:
                event.set()
    
    def available(self) -> int:
        """Return the available capacity."""
        with self._lock:
            return self._capacity - self._current
    
    def in_use(self) -> int:
        """Return the units currently in use."""
        with self._lock:
            return self._current
    
    @contextmanager
    def acquire_context(self, weight: int = 1, timeout: Optional[float] = None):
        """
        Context manager for acquiring weight units.
        
        Args:
            weight: Number of units to acquire.
            timeout: Maximum seconds to wait.
        
        Yields:
            self
        """
        self.acquire(weight, timeout)
        try:
            yield self
        finally:
            self.release(weight)
    
    def __repr__(self) -> str:
        return f"WeightedSemaphore(capacity={self._capacity}, in_use={self.in_use()})"


class SemaphorePool:
    """
    A pool of semaphores identified by keys.
    
    Useful for managing different resources with separate limits.
    
    Example:
        >>> pool = SemaphorePool(default_capacity=5)
        >>> sem = pool.get('database')
        >>> with sem:
        ...     query_database()
        >>> pool.keys()
        ['database']
    """
    
    def __init__(self, default_capacity: int):
        """
        Initialize a semaphore pool.
        
        Args:
            default_capacity: Default capacity for each new semaphore.
        """
        self._semaphores: Dict[str, Semaphore] = {}
        self._default_capacity = default_capacity
        self._lock = threading.Lock()
    
    def get(self, key: str, capacity: Optional[int] = None) -> Semaphore:
        """
        Get or create a semaphore for the given key.
        
        Args:
            key: Identifier for the semaphore.
            capacity: Optional capacity override.
        
        Returns:
            Semaphore for the given key.
        """
        with self._lock:
            if key not in self._semaphores:
                cap = capacity if capacity is not None else self._default_capacity
                self._semaphores[key] = Semaphore(cap)
            return self._semaphores[key]
    
    def remove(self, key: str) -> None:
        """Remove a semaphore from the pool."""
        with self._lock:
            self._semaphores.pop(key, None)
    
    def keys(self) -> List[str]:
        """Return all semaphore keys."""
        with self._lock:
            return list(self._semaphores.keys())
    
    def size(self) -> int:
        """Return the number of semaphores in the pool."""
        with self._lock:
            return len(self._semaphores)
    
    def stats(self) -> Dict[str, Dict[str, int]]:
        """Return statistics for all semaphores."""
        result = {}
        with self._lock:
            for key, sem in self._semaphores.items():
                result[key] = {
                    'capacity': sem.capacity,
                    'in_use': sem.in_use(),
                    'available': sem.available(),
                    'waiters': sem.waiters()
                }
        return result
    
    def __repr__(self) -> str:
        return f"SemaphorePool(size={self.size()})"


class AsyncSemaphore:
    """
    An async semaphore with enhanced features.
    
    Async version of Semaphore for use with asyncio.
    
    Example:
        >>> sem = AsyncSemaphore(10)
        >>> async with sem:
        ...     await process_data()
    """
    
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._current = 0
        self._lock = asyncio.Lock()
        self._condition = asyncio.Condition(self._lock)
    
    @property
    def capacity(self) -> int:
        return self._capacity
    
    async def acquire(self) -> bool:
        """Acquire a permit asynchronously."""
        async with self._condition:
            while self._current >= self._capacity:
                await self._condition.wait()
            self._current += 1
            return True
    
    def try_acquire(self) -> bool:
        """Try to acquire without blocking."""
        if self._current < self._capacity:
            self._current += 1
            return True
        return False
    
    async def release(self) -> None:
        """Release a permit asynchronously."""
        async with self._condition:
            if self._current > 0:
                self._current -= 1
            self._condition.notify()
    
    def available(self) -> int:
        """Return available permits."""
        return self._capacity - self._current
    
    def in_use(self) -> int:
        """Return permits in use."""
        return self._current
    
    async def __aenter__(self) -> 'AsyncSemaphore':
        await self.acquire()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.release()
    
    def __repr__(self) -> str:
        return f"AsyncSemaphore(capacity={self._capacity}, in_use={self.in_use()})"


class AsyncWeightedSemaphore:
    """
    An async weighted semaphore.
    
    Async version of WeightedSemaphore for use with asyncio.
    """
    
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._current = 0
        self._lock = asyncio.Lock()
        self._condition = asyncio.Condition(self._lock)
    
    @property
    def capacity(self) -> int:
        return self._capacity
    
    async def acquire(self, weight: int = 1) -> bool:
        """Acquire weight units asynchronously."""
        if weight <= 0 or weight > self._capacity:
            raise ValueError("Invalid weight")
        
        async with self._condition:
            while self._current + weight > self._capacity:
                await self._condition.wait()
            self._current += weight
            return True
    
    def try_acquire(self, weight: int = 1) -> bool:
        """Try to acquire without blocking."""
        if weight <= 0 or weight > self._capacity:
            return False
        if self._current + weight <= self._capacity:
            self._current += weight
            return True
        return False
    
    async def release(self, weight: int = 1) -> None:
        """Release weight units asynchronously."""
        async with self._condition:
            self._current = max(0, self._current - weight)
            self._condition.notify_all()
    
    def available(self) -> int:
        return self._capacity - self._current
    
    def in_use(self) -> int:
        return self._current
    
    async def __aenter__(self) -> 'AsyncWeightedSemaphore':
        await self.acquire()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.release()
    
    def __repr__(self) -> str:
        return f"AsyncWeightedSemaphore(capacity={self._capacity}, in_use={self.in_use()})"


class BoundedSemaphore(Semaphore):
    """
    A bounded semaphore that raises an error if release() is called too many times.
    
    Unlike a regular semaphore, this prevents accidental over-release.
    
    Example:
        >>> sem = BoundedSemaphore(2)
        >>> sem.acquire()
        >>> sem.acquire()
        >>> sem.release()
        >>> sem.release()
        >>> sem.release()  # Raises ValueError
    """
    
    def __init__(self, capacity: int):
        super().__init__(capacity)
        self._initial = capacity
    
    def release(self) -> None:
        """Release a permit, raising ValueError if over-released."""
        with self._condition:
            if self._current <= 0:
                raise ValueError("Semaphore released too many times")
            self._current -= 1
            self._condition.notify()


class PrioritySemaphore:
    """
    A semaphore that serves waiters by priority.
    
    Higher priority requests are served first when permits become available.
    
    Example:
        >>> sem = PrioritySemaphore(5)
        >>> sem.acquire(priority=1)  # Higher priority (lower number)
        >>> sem.acquire(priority=10)  # Lower priority
    """
    
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._current = 0
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._waiters: List[tuple] = []  # List of (priority, event)
    
    @property
    def capacity(self) -> int:
        return self._capacity
    
    def acquire(self, priority: int = 0, timeout: Optional[float] = None) -> bool:
        """
        Acquire a permit with priority.
        
        Lower priority values are served first.
        
        Args:
            priority: Priority level (lower = higher priority).
            timeout: Maximum seconds to wait.
        
        Returns:
            True if acquired.
        """
        start_time = time.monotonic()
        
        with self._condition:
            # Fast path: permit available and no waiters
            if self._current < self._capacity and not self._waiters:
                self._current += 1
                return True
            
            # Slow path: wait for permit
            event = threading.Event()
            waiter = (priority, event)
            self._waiters.append(waiter)
            self._waiters.sort(key=lambda x: x[0])  # Sort by priority
            
            try:
                while True:
                    # Check if we're next
                    if self._current < self._capacity:
                        # Find highest priority waiter (us or someone else)
                        for i, (p, e) in enumerate(self._waiters):
                            if e is event:
                                self._current += 1
                                self._waiters.pop(i)
                                return True
                            elif not e.is_set():
                                break
                    
                    remaining = None
                    if timeout is not None:
                        elapsed = time.monotonic() - start_time
                        remaining = timeout - elapsed
                        if remaining <= 0:
                            # Remove ourselves from waiters
                            for i, (p, e) in enumerate(self._waiters):
                                if e is event:
                                    self._waiters.pop(i)
                                    break
                            raise TimeoutError("Semaphore acquire timeout")
                    
                    self._condition.wait(remaining)
            finally:
                pass
    
    def release(self) -> None:
        """Release a permit."""
        with self._condition:
            if self._current > 0:
                self._current -= 1
            self._condition.notify_all()
    
    def available(self) -> int:
        return self._capacity - self._current
    
    def in_use(self) -> int:
        return self._current
    
    def __enter__(self) -> 'PrioritySemaphore':
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()
    
    def __repr__(self) -> str:
        return f"PrioritySemaphore(capacity={self._capacity}, in_use={self.in_use()})"


@dataclass
class RateLimitConfig:
    """Configuration for rate limiter."""
    permits: int
    period: float  # seconds
    burst: int = 1  # initial burst capacity


class RateLimiter:
    """
    A rate limiter using the token bucket algorithm.
    
    Limits the rate of operations over time, rather than total concurrency.
    
    Example:
        >>> limiter = RateLimiter(10, 1.0)  # 10 operations per second
        >>> limiter.acquire()  # Returns immediately
        >>> limiter.acquire()  # May wait if rate exceeded
    """
    
    def __init__(self, permits: int, period: float = 1.0, burst: Optional[int] = None):
        """
        Initialize a rate limiter.
        
        Args:
            permits: Maximum permits per period.
            period: Time period in seconds.
            burst: Initial burst capacity (defaults to permits).
        """
        if permits <= 0:
            raise ValueError("Permits must be positive")
        if period <= 0:
            raise ValueError("Period must be positive")
        
        self._permits = permits
        self._period = period
        self._burst = burst if burst is not None else permits
        self._tokens = self._burst
        self._last_update = time.monotonic()
        self._lock = threading.Lock()
    
    @property
    def permits(self) -> int:
        return self._permits
    
    @property
    def period(self) -> float:
        return self._period
    
    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self._last_update
        self._last_update = now
        
        # Calculate tokens to add
        tokens_to_add = (elapsed / self._period) * self._permits
        self._tokens = min(self._burst, self._tokens + tokens_to_add)
    
    def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Acquire a permit, waiting if necessary.
        
        Args:
            timeout: Maximum seconds to wait.
        
        Returns:
            True if permit acquired.
        
        Raises:
            TimeoutError: If timeout expires.
        """
        start_time = time.monotonic()
        
        with self._lock:
            while True:
                self._refill()
                
                if self._tokens >= 1:
                    self._tokens -= 1
                    return True
                
                # Calculate wait time
                tokens_needed = 1 - self._tokens
                wait_time = (tokens_needed / self._permits) * self._period
                
                if timeout is not None:
                    elapsed = time.monotonic() - start_time
                    remaining = timeout - elapsed
                    if remaining <= 0:
                        raise TimeoutError("Rate limiter timeout")
                    wait_time = min(wait_time, remaining)
                
                self._lock.release()
                try:
                    time.sleep(wait_time)
                finally:
                    self._lock.acquire()
    
    def try_acquire(self) -> bool:
        """Try to acquire without waiting."""
        with self._lock:
            self._refill()
            if self._tokens >= 1:
                self._tokens -= 1
                return True
            return False
    
    def available(self) -> float:
        """Return the number of available tokens."""
        with self._lock:
            self._refill()
            return self._tokens
    
    def __repr__(self) -> str:
        return f"RateLimiter(permits={self._permits}/period={self._period}s)"


class ConcurrencyLimit:
    """
    A context manager for limiting concurrency of operations.
    
    Combines semaphore and rate limiting.
    
    Example:
        >>> limit = ConcurrencyLimit(max_concurrent=5, rate=10, period=1.0)
        >>> with limit:
        ...     process_data()
    """
    
    def __init__(
        self,
        max_concurrent: int,
        rate: Optional[int] = None,
        period: float = 1.0
    ):
        """
        Initialize a concurrency limit.
        
        Args:
            max_concurrent: Maximum concurrent operations.
            rate: Maximum rate (operations per period).
            period: Time period for rate limiting.
        """
        self._semaphore = Semaphore(max_concurrent)
        self._rate_limiter = RateLimiter(rate, period) if rate else None
    
    def acquire(self, timeout: Optional[float] = None) -> bool:
        """Acquire both semaphore and rate limit."""
        if self._rate_limiter:
            self._rate_limiter.acquire(timeout)
        return self._semaphore.acquire(timeout)
    
    def release(self) -> None:
        """Release the semaphore."""
        self._semaphore.release()
    
    def __enter__(self) -> 'ConcurrencyLimit':
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()
    
    @property
    def available(self) -> int:
        return self._semaphore.available()


def acquire_all(
    *semaphores: Semaphore,
    timeout: Optional[float] = None
) -> bool:
    """
    Acquire all semaphores atomically (all-or-nothing).
    
    Args:
        *semaphores: Semaphores to acquire.
        timeout: Maximum time to wait.
    
    Returns:
        True if all semaphores were acquired.
    
    Raises:
        TimeoutError: If timeout expires.
    
    Example:
        >>> sem1, sem2 = Semaphore(1), Semaphore(1)
        >>> acquire_all(sem1, sem2)
        True
        >>> sem1.available()
        0
        >>> sem2.available()
        0
    """
    acquired = []
    
    try:
        for sem in semaphores:
            if not sem.try_acquire():
                # Release what we've acquired
                for a in acquired:
                    a.release()
                
                # Wait for this one
                if timeout is not None:
                    sem.acquire(timeout)
                else:
                    sem.acquire()
                
                # Try to reacquire others
                for a in acquired:
                    a.acquire()
                
                acquired.append(sem)
            else:
                acquired.append(sem)
        
        return True
    except Exception:
        for a in acquired:
            a.release()
        raise


def run_with_semaphore(
    sem: Semaphore,
    func: Callable[..., T],
    *args,
    timeout: Optional[float] = None,
    **kwargs
) -> T:
    """
    Run a function with a semaphore permit acquired.
    
    Args:
        sem: Semaphore to use.
        func: Function to run.
        *args: Positional arguments for func.
        timeout: Maximum time to wait for semaphore.
        **kwargs: Keyword arguments for func.
    
    Returns:
        Result of func.
    
    Example:
        >>> sem = Semaphore(1)
        >>> result = run_with_semaphore(sem, expensive_operation, timeout=5.0)
    """
    sem.acquire(timeout)
    try:
        return func(*args, **kwargs)
    finally:
        sem.release()


# Convenience functions

def create_bounded(capacity: int) -> BoundedSemaphore:
    """Create a bounded semaphore."""
    return BoundedSemaphore(capacity)


def create_pool(default_capacity: int) -> SemaphorePool:
    """Create a semaphore pool."""
    return SemaphorePool(default_capacity)


def create_rate_limiter(permits: int, period: float = 1.0) -> RateLimiter:
    """Create a rate limiter."""
    return RateLimiter(permits, period)