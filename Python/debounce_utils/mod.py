"""
AllToolkit - Python Debounce Utilities

A zero-dependency, production-ready debounce and throttle utility module.
Supports leading/trailing edge execution, cancellation, flushing, and thread-safe operations.

Author: AllToolkit
License: MIT
"""

import time
import threading
from typing import Optional, Any, Callable, TypeVar, Generic, Dict, List, Tuple
from dataclasses import dataclass, field
from functools import wraps
from collections import deque
import hashlib


T = TypeVar('T')
R = TypeVar('R')


@dataclass
class DebounceStats:
    """Statistics for debounce operations."""
    total_calls: int = 0
    executed_calls: int = 0
    cancelled_calls: int = 0
    flushed_calls: int = 0
    pending_calls: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    
    def record_call(self) -> None:
        """Record an incoming call."""
        with self._lock:
            self.total_calls += 1
    
    def record_execution(self) -> None:
        """Record an executed call."""
        with self._lock:
            self.executed_calls += 1
    
    def record_cancellation(self) -> None:
        """Record a cancelled call."""
        with self._lock:
            self.cancelled_calls += 1
    
    def record_flush(self) -> None:
        """Record a flushed call."""
        with self._lock:
            self.flushed_calls += 1
    
    def set_pending(self, count: int) -> None:
        """Set pending call count."""
        with self._lock:
            self.pending_calls = count
    
    @property
    def suppression_rate(self) -> float:
        """Calculate how many calls were suppressed."""
        if self.total_calls == 0:
            return 0.0
        return (self.total_calls - self.executed_calls) / self.total_calls
    
    def to_dict(self) -> dict:
        """Convert stats to dictionary."""
        return {
            'total_calls': self.total_calls,
            'executed_calls': self.executed_calls,
            'cancelled_calls': self.cancelled_calls,
            'flushed_calls': self.flushed_calls,
            'pending_calls': self.pending_calls,
            'suppression_rate': f"{self.suppression_rate:.1%}",
        }
    
    def reset(self) -> None:
        """Reset all statistics."""
        with self._lock:
            self.total_calls = 0
            self.executed_calls = 0
            self.cancelled_calls = 0
            self.flushed_calls = 0
            self.pending_calls = 0


class Debouncer(Generic[T]):
    """
    Thread-safe debouncer that delays function execution until after
    a specified wait time has elapsed since the last call.
    
    Features:
    - Leading edge execution (execute immediately on first call)
    - Trailing edge execution (execute after wait time)
    - Cancellation support
    - Flush support (execute immediately)
    - Statistics tracking
    
    Example:
        debouncer = Debouncer(wait_seconds=0.5)
        
        def save_data(data):
            print(f"Saving: {data}")
        
        # Rapid calls - only the last one executes
        debouncer.call(save_data, "data1")  # Cancelled
        debouncer.call(save_data, "data2")  # Cancelled
        debouncer.call(save_data, "data3")  # Executes after 0.5s
    """
    
    def __init__(
        self,
        wait_seconds: float = 0.3,
        leading: bool = False,
        trailing: bool = True,
        max_wait: Optional[float] = None,
    ):
        """
        Initialize debouncer.
        
        Args:
            wait_seconds: Time to wait before executing (default: 0.3)
            leading: Execute on leading edge (first call immediately)
            trailing: Execute on trailing edge (after wait time)
            max_wait: Maximum time to wait before forcing execution
        """
        if wait_seconds <= 0:
            raise ValueError("wait_seconds must be positive")
        if max_wait is not None and max_wait <= 0:
            raise ValueError("max_wait must be positive if specified")
        
        self._wait_seconds = wait_seconds
        self._leading = leading
        self._trailing = trailing
        self._max_wait = max_wait
        
        self._timer: Optional[threading.Timer] = None
        self._max_timer: Optional[threading.Timer] = None
        self._pending_func: Optional[Callable[..., T]] = None
        self._pending_args: tuple = ()
        self._pending_kwargs: dict = {}
        self._leading_executed = False
        self._first_call_time: Optional[float] = None
        
        self._lock = threading.Lock()
        self._stats = DebounceStats()
    
    @property
    def wait_seconds(self) -> float:
        """Get wait time in seconds."""
        return self._wait_seconds
    
    @property
    def is_pending(self) -> bool:
        """Check if there's a pending execution."""
        with self._lock:
            return self._timer is not None or self._pending_func is not None
    
    @property
    def stats(self) -> DebounceStats:
        """Get statistics."""
        return self._stats
    
    def call(self, func: Callable[..., T], *args, **kwargs) -> Optional[T]:
        """
        Call the debounced function.
        
        Args:
            func: Function to debounce
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result if executed immediately (leading edge), else None
        """
        with self._lock:
            self._stats.record_call()
            
            # Store pending call
            self._pending_func = func
            self._pending_args = args
            self._pending_kwargs = kwargs
            
            # Track first call time for max_wait
            if self._first_call_time is None:
                self._first_call_time = time.time()
            
            result = None
            
            # Leading edge execution
            if self._leading and not self._leading_executed:
                result = func(*args, **kwargs)
                self._leading_executed = True
                self._stats.record_execution()
            
            # Cancel existing timer
            if self._timer is not None:
                self._timer.cancel()
            
            # Set up max_wait timer if needed
            if self._max_wait is not None and self._max_timer is None:
                self._max_timer = threading.Timer(
                    self._max_wait,
                    self._execute_max_wait
                )
                self._max_timer.daemon = True
                self._max_timer.start()
            
            # Set up trailing edge timer
            if self._trailing:
                self._timer = threading.Timer(
                    self._wait_seconds,
                    self._execute_trailing
                )
                self._timer.daemon = True
                self._timer.start()
                self._stats.set_pending(1)
            
            return result
    
    def _execute_trailing(self) -> None:
        """Execute on trailing edge."""
        with self._lock:
            if self._pending_func is None:
                return
            
            func = self._pending_func
            args = self._pending_args
            kwargs = self._pending_kwargs
            
            # Clear pending
            self._clear_pending()
            
            # Execute
            try:
                func(*args, **kwargs)
                self._stats.record_execution()
            except Exception:
                raise
            finally:
                self._stats.set_pending(0)
    
    def _execute_max_wait(self) -> None:
        """Execute when max_wait is reached."""
        with self._lock:
            if self._pending_func is None:
                return
            
            func = self._pending_func
            args = self._pending_args
            kwargs = self._pending_kwargs
            
            # Clear pending and timers
            self._clear_pending()
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
            
            # Execute
            try:
                func(*args, **kwargs)
                self._stats.record_execution()
            except Exception:
                raise
            finally:
                self._max_timer = None
                self._stats.set_pending(0)
    
    def _clear_pending(self) -> None:
        """Clear pending state."""
        self._pending_func = None
        self._pending_args = ()
        self._pending_kwargs = {}
        self._leading_executed = False
        self._first_call_time = None
        self._timer = None
    
    def cancel(self) -> bool:
        """
        Cancel pending execution.
        
        Returns:
            True if there was a pending execution to cancel
        """
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
            
            if self._max_timer is not None:
                self._max_timer.cancel()
                self._max_timer = None
            
            was_pending = self._pending_func is not None
            self._clear_pending()
            
            if was_pending:
                self._stats.record_cancellation()
                self._stats.set_pending(0)
            
            return was_pending
    
    def flush(self) -> Optional[T]:
        """
        Immediately execute pending call if any.
        
        Returns:
            Result of the pending function, or None if no pending call
        """
        with self._lock:
            if self._pending_func is None:
                return None
            
            # Cancel timers
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
            
            if self._max_timer is not None:
                self._max_timer.cancel()
                self._max_timer = None
            
            # Get pending call
            func = self._pending_func
            args = self._pending_args
            kwargs = self._pending_kwargs
            
            # Clear pending
            self._clear_pending()
            self._stats.record_flush()
            self._stats.set_pending(0)
            
            # Execute
            result = func(*args, **kwargs)
            self._stats.record_execution()
            
            return result
    
    def pending_args(self) -> Optional[Tuple[tuple, dict]]:
        """
        Get pending call arguments without executing.
        
        Returns:
            Tuple of (args, kwargs) or None if no pending call
        """
        with self._lock:
            if self._pending_func is None:
                return None
            return (self._pending_args, self._pending_kwargs)
    
    def reset(self) -> None:
        """Reset debouncer state."""
        with self._lock:
            self.cancel()
            self._leading_executed = False
            self._first_call_time = None


class Throttler(Generic[T]):
    """
    Thread-safe throttler that limits function execution to once
    per specified time interval.
    
    Features:
    - Leading edge execution (execute immediately on first call)
    - Trailing edge execution (execute after interval if calls occurred)
    - Statistics tracking
    
    Example:
        throttler = Throttler(interval_seconds=1.0)
        
        def log_action(action):
            print(f"Action: {action}")
        
        # Rapid calls - only one per second executes
        throttler.call(log_action, "a")  # Executes immediately
        throttler.call(log_action, "b")  # Dropped (within interval)
        throttler.call(log_action, "c")  # Dropped (within interval)
        # After 1 second, next call executes
    """
    
    def __init__(
        self,
        interval_seconds: float = 1.0,
        leading: bool = True,
        trailing: bool = False,
    ):
        """
        Initialize throttler.
        
        Args:
            interval_seconds: Minimum time between executions
            leading: Execute on leading edge (immediately on first call)
            trailing: Execute on trailing edge (after interval)
        """
        if interval_seconds <= 0:
            raise ValueError("interval_seconds must be positive")
        
        self._interval_seconds = interval_seconds
        self._leading = leading
        self._trailing = trailing
        
        self._last_execution_time: Optional[float] = None
        self._pending_func: Optional[Callable[..., T]] = None
        self._pending_args: tuple = ()
        self._pending_kwargs: dict = {}
        self._has_pending = False
        
        self._timer: Optional[threading.Timer] = None
        self._lock = threading.Lock()
        self._stats = DebounceStats()
    
    @property
    def interval_seconds(self) -> float:
        """Get interval in seconds."""
        return self._interval_seconds
    
    @property
    def is_throttled(self) -> bool:
        """Check if currently throttled (within interval)."""
        with self._lock:
            if self._last_execution_time is None:
                return False
            return (time.time() - self._last_execution_time) < self._interval_seconds
    
    @property
    def time_until_next(self) -> float:
        """Get time until next execution is allowed."""
        with self._lock:
            if self._last_execution_time is None:
                return 0.0
            elapsed = time.time() - self._last_execution_time
            return max(0.0, self._interval_seconds - elapsed)
    
    @property
    def stats(self) -> DebounceStats:
        """Get statistics."""
        return self._stats
    
    def call(self, func: Callable[..., T], *args, **kwargs) -> Optional[T]:
        """
        Call the throttled function.
        
        Args:
            func: Function to throttle
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result if executed, else None
        """
        with self._lock:
            self._stats.record_call()
            now = time.time()
            
            # Check if we can execute immediately
            can_execute = (
                self._last_execution_time is None or
                (now - self._last_execution_time) >= self._interval_seconds
            )
            
            if can_execute and self._leading:
                # Execute immediately
                self._last_execution_time = now
                self._stats.record_execution()
                return func(*args, **kwargs)
            
            # Store as pending for trailing execution
            if self._trailing:
                self._pending_func = func
                self._pending_args = args
                self._pending_kwargs = kwargs
                self._has_pending = True
                
                # Set timer if not already set
                if self._timer is None:
                    time_until = self._interval_seconds
                    if self._last_execution_time is not None:
                        time_until = max(0.0, self._interval_seconds - (now - self._last_execution_time))
                    
                    self._timer = threading.Timer(time_until, self._execute_trailing)
                    self._timer.daemon = True
                    self._timer.start()
                    self._stats.set_pending(1)
            
            return None
    
    def _execute_trailing(self) -> None:
        """Execute pending trailing call."""
        with self._lock:
            if not self._has_pending or self._pending_func is None:
                self._timer = None
                return
            
            func = self._pending_func
            args = self._pending_args
            kwargs = self._pending_kwargs
            
            self._pending_func = None
            self._pending_args = ()
            self._pending_kwargs = {}
            self._has_pending = False
            self._timer = None
            self._stats.set_pending(0)
            
            self._last_execution_time = time.time()
            self._stats.record_execution()
            func(*args, **kwargs)
    
    def cancel(self) -> bool:
        """
        Cancel pending trailing execution.
        
        Returns:
            True if there was a pending execution to cancel
        """
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
            
            was_pending = self._has_pending
            self._pending_func = None
            self._pending_args = ()
            self._pending_kwargs = {}
            self._has_pending = False
            
            if was_pending:
                self._stats.record_cancellation()
                self._stats.set_pending(0)
            
            return was_pending
    
    def flush(self) -> Optional[T]:
        """
        Immediately execute pending call if any.
        
        Returns:
            Result of the pending function, or None if no pending call
        """
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
            
            if not self._has_pending or self._pending_func is None:
                return None
            
            func = self._pending_func
            args = self._pending_args
            kwargs = self._pending_kwargs
            
            self._pending_func = None
            self._pending_args = ()
            self._pending_kwargs = {}
            self._has_pending = False
            self._stats.set_pending(0)
            self._stats.record_flush()
            
            self._last_execution_time = time.time()
            self._stats.record_execution()
            return func(*args, **kwargs)
    
    def reset(self) -> None:
        """Reset throttler state."""
        with self._lock:
            self.cancel()
            self._last_execution_time = None


def debounce(
    wait_seconds: float = 0.3,
    leading: bool = False,
    trailing: bool = True,
    max_wait: Optional[float] = None,
) -> Callable[[Callable[..., T]], Callable[..., Optional[T]]]:
    """
    Decorator to debounce function calls.
    
    Args:
        wait_seconds: Time to wait before executing
        leading: Execute on leading edge (first call)
        trailing: Execute on trailing edge (after wait time)
        max_wait: Maximum time to wait before forcing execution
    
    Returns:
        Decorated function with debouncing
    
    Example:
        @debounce(wait_seconds=0.5)
        def search(query):
            print(f"Searching for: {query}")
        
        # Rapid calls - only last executes
        search("h")
        search("he")
        search("hello")  # Executes after 0.5s
    """
    debouncer = Debouncer(
        wait_seconds=wait_seconds,
        leading=leading,
        trailing=trailing,
        max_wait=max_wait,
    )
    
    def decorator(func: Callable[..., T]) -> Callable[..., Optional[T]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Optional[T]:
            return debouncer.call(func, *args, **kwargs)
        
        wrapper.debouncer = debouncer  # type: ignore
        wrapper.cancel = debouncer.cancel  # type: ignore
        wrapper.flush = debouncer.flush  # type: ignore
        
        return wrapper
    
    return decorator


def throttle(
    interval_seconds: float = 1.0,
    leading: bool = True,
    trailing: bool = False,
) -> Callable[[Callable[..., T]], Callable[..., Optional[T]]]:
    """
    Decorator to throttle function calls.
    
    Args:
        interval_seconds: Minimum time between executions
        leading: Execute on leading edge (immediately on first call)
        trailing: Execute on trailing edge (after interval)
    
    Returns:
        Decorated function with throttling
    
    Example:
        @throttle(interval_seconds=1.0)
        def handle_scroll(position):
            print(f"Scroll position: {position}")
        
        # Rapid calls - only one per second executes
        handle_scroll(100)  # Executes immediately
        handle_scroll(200)  # Dropped
        handle_scroll(300)  # Dropped
    """
    throttler = Throttler(
        interval_seconds=interval_seconds,
        leading=leading,
        trailing=trailing,
    )
    
    def decorator(func: Callable[..., T]) -> Callable[..., Optional[T]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Optional[T]:
            return throttler.call(func, *args, **kwargs)
        
        wrapper.throttler = throttler  # type: ignore
        wrapper.cancel = throttler.cancel  # type: ignore
        wrapper.flush = throttler.flush  # type: ignore
        
        return wrapper
    
    return decorator


class MultiKeyDebouncer:
    """
    Multi-key debouncer supporting independent debouncing per key.
    
    Example:
        debouncer = MultiKeyDebouncer(wait_seconds=0.5)
        
        # Each key has independent debouncing
        debouncer.call("user_1", save_user, user1_data)
        debouncer.call("user_2", save_user, user2_data)
    """
    
    def __init__(
        self,
        wait_seconds: float = 0.3,
        leading: bool = False,
        trailing: bool = True,
        max_wait: Optional[float] = None,
        cleanup_interval: float = 300.0,
    ):
        """
        Initialize multi-key debouncer.
        
        Args:
            wait_seconds: Time to wait before executing
            leading: Execute on leading edge
            trailing: Execute on trailing edge
            max_wait: Maximum time to wait
            cleanup_interval: Seconds between cleanup of stale keys
        """
        self._wait_seconds = wait_seconds
        self._leading = leading
        self._trailing = trailing
        self._max_wait = max_wait
        self._cleanup_interval = cleanup_interval
        
        self._debouncers: Dict[str, Debouncer] = {}
        self._key_times: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._last_cleanup = time.time()
    
    def _cleanup_stale(self) -> None:
        """Remove stale debouncers."""
        now = time.time()
        if now - self._last_cleanup < self._cleanup_interval:
            return
        
        with self._lock:
            stale_cutoff = now - self._cleanup_interval * 2
            stale_keys = [
                key for key, last_used in self._key_times.items()
                if last_used < stale_cutoff
            ]
            for key in stale_keys:
                if key in self._debouncers:
                    self._debouncers[key].cancel()
                del self._debouncers[key]
                del self._key_times[key]
            self._last_cleanup = now
    
    def _get_debouncer(self, key: str) -> Debouncer:
        """Get or create debouncer for key."""
        with self._lock:
            if key not in self._debouncers:
                self._debouncers[key] = Debouncer(
                    wait_seconds=self._wait_seconds,
                    leading=self._leading,
                    trailing=self._trailing,
                    max_wait=self._max_wait,
                )
            self._key_times[key] = time.time()
            return self._debouncers[key]
    
    def call(self, key: str, func: Callable[..., T], *args, **kwargs) -> Optional[T]:
        """
        Call debounced function for a specific key.
        
        Args:
            key: Unique key for this debouncer
            func: Function to debounce
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result if executed immediately, else None
        """
        self._cleanup_stale()
        debouncer = self._get_debouncer(key)
        return debouncer.call(func, *args, **kwargs)
    
    def cancel(self, key: str) -> bool:
        """
        Cancel pending execution for a key.
        
        Args:
            key: Debouncer key
            
        Returns:
            True if there was a pending execution to cancel
        """
        with self._lock:
            if key in self._debouncers:
                return self._debouncers[key].cancel()
            return False
    
    def cancel_all(self) -> int:
        """
        Cancel all pending executions.
        
        Returns:
            Number of cancelled executions
        """
        with self._lock:
            count = 0
            for debouncer in self._debouncers.values():
                if debouncer.cancel():
                    count += 1
            return count
    
    def flush(self, key: str) -> Optional[T]:
        """
        Immediately execute pending call for a key.
        
        Args:
            key: Debouncer key
            
        Returns:
            Result of pending function, or None
        """
        with self._lock:
            if key in self._debouncers:
                return self._debouncers[key].flush()
            return None
    
    def flush_all(self) -> List[T]:
        """
        Flush all pending executions.
        
        Returns:
            List of results from flushed executions
        """
        results = []
        with self._lock:
            for debouncer in self._debouncers.values():
                result = debouncer.flush()
                if result is not None:
                    results.append(result)
        return results
    
    def is_pending(self, key: str) -> bool:
        """Check if there's a pending execution for a key."""
        with self._lock:
            if key in self._debouncers:
                return self._debouncers[key].is_pending
            return False
    
    def pending_keys(self) -> List[str]:
        """Get list of keys with pending executions."""
        with self._lock:
            return [key for key, deb in self._debouncers.items() if deb.is_pending]


class MultiKeyThrottler:
    """
    Multi-key throttler supporting independent throttling per key.
    
    Example:
        throttler = MultiKeyThrottler(interval_seconds=1.0)
        
        # Each key has independent throttling
        throttler.call("api_1", call_api, "endpoint1")
        throttler.call("api_2", call_api, "endpoint2")
    """
    
    def __init__(
        self,
        interval_seconds: float = 1.0,
        leading: bool = True,
        trailing: bool = False,
        cleanup_interval: float = 300.0,
    ):
        """
        Initialize multi-key throttler.
        
        Args:
            interval_seconds: Minimum time between executions
            leading: Execute on leading edge
            trailing: Execute on trailing edge
            cleanup_interval: Seconds between cleanup of stale keys
        """
        self._interval_seconds = interval_seconds
        self._leading = leading
        self._trailing = trailing
        self._cleanup_interval = cleanup_interval
        
        self._throttlers: Dict[str, Throttler] = {}
        self._key_times: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._last_cleanup = time.time()
    
    def _cleanup_stale(self) -> None:
        """Remove stale throttlers."""
        now = time.time()
        if now - self._last_cleanup < self._cleanup_interval:
            return
        
        with self._lock:
            stale_cutoff = now - self._cleanup_interval * 2
            stale_keys = [
                key for key, last_used in self._key_times.items()
                if last_used < stale_cutoff
            ]
            for key in stale_keys:
                if key in self._throttlers:
                    self._throttlers[key].cancel()
                del self._throttlers[key]
                del self._key_times[key]
            self._last_cleanup = now
    
    def _get_throttler(self, key: str) -> Throttler:
        """Get or create throttler for key."""
        with self._lock:
            if key not in self._throttlers:
                self._throttlers[key] = Throttler(
                    interval_seconds=self._interval_seconds,
                    leading=self._leading,
                    trailing=self._trailing,
                )
            self._key_times[key] = time.time()
            return self._throttlers[key]
    
    def call(self, key: str, func: Callable[..., T], *args, **kwargs) -> Optional[T]:
        """
        Call throttled function for a specific key.
        
        Args:
            key: Unique key for this throttler
            func: Function to throttle
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result if executed, else None
        """
        self._cleanup_stale()
        throttler = self._get_throttler(key)
        return throttler.call(func, *args, **kwargs)
    
    def cancel(self, key: str) -> bool:
        """Cancel pending execution for a key."""
        with self._lock:
            if key in self._throttlers:
                return self._throttlers[key].cancel()
            return False
    
    def cancel_all(self) -> int:
        """Cancel all pending executions."""
        with self._lock:
            count = 0
            for throttler in self._throttlers.values():
                if throttler.cancel():
                    count += 1
            return count
    
    def is_throttled(self, key: str) -> bool:
        """Check if a key is currently throttled."""
        with self._lock:
            if key in self._throttlers:
                return self._throttlers[key].is_throttled
            return False
    
    def time_until_next(self, key: str) -> float:
        """Get time until next execution is allowed for a key."""
        with self._lock:
            if key in self._throttlers:
                return self._throttlers[key].time_until_next
            return 0.0


def generate_debounce_key(*args: Any, **kwargs: Any) -> str:
    """
    Generate a debounce key from function arguments.
    
    Creates a hash-based key from all arguments.
    
    Args:
        *args: Positional arguments
        **kwargs: Keyword arguments
    
    Returns:
        SHA256 hash of arguments as hex string
    """
    key_data = {
        'args': args,
        'kwargs': kwargs,
    }
    key_str = str(key_data)
    return hashlib.sha256(key_str.encode()).hexdigest()[:16]


class DebouncedFunction:
    """
    Wrapper for creating debounced versions of functions.
    Useful when you need multiple debounced versions of the same function.
    
    Example:
        def save(data):
            print(f"Saving: {data}")
        
        # Create debounced version
        debounced_save = DebouncedFunction(save, wait_seconds=0.5)
        
        # Or use as context manager
        with DebouncedFunction(save, wait_seconds=0.3) as debounced:
            debounced("data1")
            debounced("data2")  # Only this one executes
    """
    
    def __init__(
        self,
        func: Callable[..., T],
        wait_seconds: float = 0.3,
        leading: bool = False,
        trailing: bool = True,
        max_wait: Optional[float] = None,
    ):
        """
        Initialize debounced function wrapper.
        
        Args:
            func: Function to debounce
            wait_seconds: Time to wait before executing
            leading: Execute on leading edge
            trailing: Execute on trailing edge
            max_wait: Maximum time to wait
        """
        self._func = func
        self._debouncer = Debouncer(
            wait_seconds=wait_seconds,
            leading=leading,
            trailing=trailing,
            max_wait=max_wait,
        )
    
    def __call__(self, *args, **kwargs) -> Optional[T]:
        """Call the debounced function."""
        return self._debouncer.call(self._func, *args, **kwargs)
    
    def cancel(self) -> bool:
        """Cancel pending execution."""
        return self._debouncer.cancel()
    
    def flush(self) -> Optional[T]:
        """Immediately execute pending call."""
        return self._debouncer.flush()
    
    @property
    def is_pending(self) -> bool:
        """Check if there's a pending execution."""
        return self._debouncer.is_pending
    
    def __enter__(self) -> 'DebouncedFunction':
        """Enter context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager, flush pending execution."""
        self.flush()


class ThrottledFunction:
    """
    Wrapper for creating throttled versions of functions.
    
    Example:
        def send_event(data):
            print(f"Event: {data}")
        
        # Create throttled version
        throttled_send = ThrottledFunction(send_event, interval_seconds=1.0)
        
        # Or use as context manager
        with ThrottledFunction(send_event, interval_seconds=0.5) as throttled:
            throttled("e1")  # Executes
            throttled("e2")  # Dropped
    """
    
    def __init__(
        self,
        func: Callable[..., T],
        interval_seconds: float = 1.0,
        leading: bool = True,
        trailing: bool = False,
    ):
        """
        Initialize throttled function wrapper.
        
        Args:
            func: Function to throttle
            interval_seconds: Minimum time between executions
            leading: Execute on leading edge
            trailing: Execute on trailing edge
        """
        self._func = func
        self._throttler = Throttler(
            interval_seconds=interval_seconds,
            leading=leading,
            trailing=trailing,
        )
    
    def __call__(self, *args, **kwargs) -> Optional[T]:
        """Call the throttled function."""
        return self._throttler.call(self._func, *args, **kwargs)
    
    def cancel(self) -> bool:
        """Cancel pending execution."""
        return self._throttler.cancel()
    
    def flush(self) -> Optional[T]:
        """Immediately execute pending call."""
        return self._throttler.flush()
    
    @property
    def is_throttled(self) -> bool:
        """Check if currently throttled."""
        return self._throttler.is_throttled
    
    @property
    def time_until_next(self) -> float:
        """Get time until next execution is allowed."""
        return self._throttler.time_until_next
    
    def __enter__(self) -> 'ThrottledFunction':
        """Enter context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager, flush pending execution."""
        self.flush()