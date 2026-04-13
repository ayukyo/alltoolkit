#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Circuit Breaker Utilities Module

Implementation of the Circuit Breaker pattern for fault tolerance in distributed systems.
Provides automatic failure detection, recovery, and service protection.

Features:
- Three states: CLOSED, OPEN, HALF_OPEN
- Configurable failure thresholds and recovery timeouts
- Exponential backoff support
- Event hooks for monitoring
- Decorator and context manager interfaces
- Zero external dependencies

Author: AllToolkit
License: MIT
"""

import time
import threading
import functools
import random
from typing import (
    Callable, Optional, Any, Dict, List, Union,
    TypeVar, Generic
)
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque


# =============================================================================
# Type Aliases and Generics
# =============================================================================

T = TypeVar('T')


# =============================================================================
# Enums and Constants
# =============================================================================

class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = auto()      # Normal operation, requests flow through
    OPEN = auto()       # Circuit is open, requests are blocked
    HALF_OPEN = auto()  # Testing if service has recovered


class CircuitEvent(Enum):
    """Circuit breaker events."""
    STATE_CHANGE = "state_change"
    SUCCESS = "success"
    FAILURE = "failure"
    REJECTION = "rejection"
    TIMEOUT = "timeout"
    HALF_OPEN_SUCCESS = "half_open_success"
    HALF_OPEN_FAILURE = "half_open_failure"


# =============================================================================
# Exceptions
# =============================================================================

class CircuitBreakerError(Exception):
    """Base exception for circuit breaker errors."""
    pass


class CircuitOpenError(CircuitBreakerError):
    """Raised when circuit is open and requests are rejected."""
    
    def __init__(self, message: str, time_until_retry: float = 0):
        super().__init__(message)
        self.time_until_retry = time_until_retry


class CircuitTimeoutError(CircuitBreakerError):
    """Raised when operation times out."""
    
    def __init__(self, timeout: float, operation: str = "operation"):
        super().__init__(f"Operation '{operation}' timed out after {timeout}s")
        self.timeout = timeout


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class CircuitStats:
    """Statistics for circuit breaker."""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    rejected_calls: int = 0
    timeout_calls: int = 0
    last_failure_time: Optional[float] = None
    last_success_time: Optional[float] = None
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    state_changes: int = 0
    
    def reset(self) -> None:
        """Reset all statistics."""
        self.total_calls = 0
        self.successful_calls = 0
        self.failed_calls = 0
        self.rejected_calls = 0
        self.timeout_calls = 0
        self.last_failure_time = None
        self.last_success_time = None
        self.consecutive_failures = 0
        self.consecutive_successes = 0
        self.state_changes = 0
    
    @property
    def failure_rate(self) -> float:
        """Calculate failure rate."""
        if self.total_calls == 0:
            return 0.0
        return self.failed_calls / self.total_calls
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_calls == 0:
            return 0.0
        return self.successful_calls / self.total_calls


@dataclass
class CircuitConfig:
    """Configuration for circuit breaker."""
    failure_threshold: int = 5
    success_threshold: int = 3  # Successes needed to close from half-open
    timeout: float = 60.0  # Seconds before attempting to close
    reset_timeout: float = 60.0  # Alias for timeout
    half_open_max_calls: int = 3  # Max calls allowed in half-open state
    failure_rate_threshold: Optional[float] = None  # e.g., 0.5 for 50%
    minimum_calls_for_rate: int = 10  # Min calls before rate threshold applies
    excluded_exceptions: tuple = ()  # Exceptions that don't count as failures
    include_exceptions: tuple = ()  # Only these exceptions count (if specified)
    
    # Exponential backoff settings
    exponential_backoff: bool = False
    backoff_multiplier: float = 2.0
    max_timeout: float = 300.0  # Max timeout with backoff
    
    def __post_init__(self):
        # If reset_timeout was explicitly set different from timeout, use it
        # This handles cases where user wants to set reset_timeout explicitly
        pass  # No automatic override


@dataclass
class EventRecord:
    """Record of a circuit event."""
    event_type: CircuitEvent
    timestamp: float
    state_before: CircuitState
    state_after: CircuitState
    details: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# Event Handlers
# =============================================================================

EventHandler = Callable[[CircuitEvent, CircuitState, Dict[str, Any]], None]


class EventEmitter:
    """Simple event emitter for circuit breaker events."""
    
    def __init__(self):
        self._handlers: Dict[CircuitEvent, List[EventHandler]] = {
            event: [] for event in CircuitEvent
        }
        self._global_handlers: List[EventHandler] = []
        self._event_history: deque = deque(maxlen=100)
    
    def on(self, event: CircuitEvent, handler: EventHandler) -> None:
        """Register an event handler."""
        self._handlers[event].append(handler)
    
    def on_any(self, handler: EventHandler) -> None:
        """Register a handler for all events."""
        self._global_handlers.append(handler)
    
    def off(self, event: CircuitEvent, handler: EventHandler) -> None:
        """Unregister an event handler."""
        if handler in self._handlers[event]:
            self._handlers[event].remove(handler)
    
    def emit(self, event: CircuitEvent, state: CircuitState, 
             details: Optional[Dict[str, Any]] = None) -> None:
        """Emit an event to all registered handlers."""
        details = details or {}
        
        # Record event
        record = EventRecord(
            event_type=event,
            timestamp=time.time(),
            state_before=details.get('state_before', state),
            state_after=details.get('state_after', state),
            details=details
        )
        self._event_history.append(record)
        
        # Call specific handlers
        for handler in self._handlers[event]:
            try:
                handler(event, state, details)
            except Exception:
                pass  # Don't let handler errors propagate
        
        # Call global handlers
        for handler in self._global_handlers:
            try:
                handler(event, state, details)
            except Exception:
                pass
    
    def get_history(self, limit: int = 10) -> List[EventRecord]:
        """Get recent event history."""
        return list(self._event_history)[-limit:]


# =============================================================================
# Main Circuit Breaker Class
# =============================================================================

class CircuitBreaker:
    """
    Circuit Breaker implementation for fault tolerance.
    
    The circuit breaker has three states:
    - CLOSED: Normal operation, all requests go through
    - OPEN: Circuit is open, requests are rejected immediately
    - HALF_OPEN: Testing if service has recovered, limited requests allowed
    
    Example:
        >>> breaker = CircuitBreaker(failure_threshold=3, timeout=30)
        >>> 
        >>> @breaker.protect
        ... def unreliable_service():
        ...     # May fail
        ...     pass
        >>> 
        >>> try:
        ...     result = unreliable_service()
        ... except CircuitOpenError:
        ...     print("Service is unavailable")
    """
    
    def __init__(
        self,
        name: str = "default",
        failure_threshold: int = 5,
        success_threshold: int = 3,
        timeout: float = 60.0,
        failure_rate_threshold: Optional[float] = None,
        minimum_calls_for_rate: int = 10,
        excluded_exceptions: tuple = (),
        include_exceptions: tuple = (),
        half_open_max_calls: int = 3,
        exponential_backoff: bool = False,
        backoff_multiplier: float = 2.0,
        max_timeout: float = 300.0,
    ):
        """
        Initialize circuit breaker.
        
        Args:
            name: Name for this circuit breaker
            failure_threshold: Number of failures before opening
            success_threshold: Successes needed to close from half-open
            timeout: Seconds to wait before attempting recovery
            failure_rate_threshold: Failure rate (0-1) to trigger open
            minimum_calls_for_rate: Min calls before rate threshold applies
            excluded_exceptions: Exceptions that don't count as failures
            include_exceptions: Only these exceptions count (if specified)
            half_open_max_calls: Max calls allowed in half-open state
            exponential_backoff: Enable exponential backoff for timeouts
            backoff_multiplier: Multiplier for backoff
            max_timeout: Maximum timeout with backoff
        """
        self.name = name
        self._config = CircuitConfig(
            failure_threshold=failure_threshold,
            success_threshold=success_threshold,
            timeout=timeout,
            failure_rate_threshold=failure_rate_threshold,
            minimum_calls_for_rate=minimum_calls_for_rate,
            excluded_exceptions=excluded_exceptions,
            include_exceptions=include_exceptions,
            half_open_max_calls=half_open_max_calls,
            exponential_backoff=exponential_backoff,
            backoff_multiplier=backoff_multiplier,
            max_timeout=max_timeout,
        )
        
        self._state = CircuitState.CLOSED
        self._stats = CircuitStats()
        self._events = EventEmitter()
        self._lock = threading.RLock()
        self._opened_at: Optional[float] = None
        self._half_open_calls = 0
        self._current_timeout = timeout
        self._failure_history: deque = deque(maxlen=100)
    
    @property
    def state(self) -> CircuitState:
        """Get current state."""
        with self._lock:
            self._check_state_transition()
            return self._state
    
    @property
    def stats(self) -> CircuitStats:
        """Get statistics."""
        with self._lock:
            return self._stats
    
    @property
    def config(self) -> CircuitConfig:
        """Get configuration."""
        return self._config
    
    @property
    def is_closed(self) -> bool:
        """Check if circuit is closed."""
        return self.state == CircuitState.CLOSED
    
    @property
    def is_open(self) -> bool:
        """Check if circuit is open."""
        return self.state == CircuitState.OPEN
    
    @property
    def is_half_open(self) -> bool:
        """Check if circuit is half-open."""
        return self.state == CircuitState.HALF_OPEN
    
    @property
    def time_until_retry(self) -> float:
        """Get seconds until retry is possible."""
        with self._lock:
            if self._state != CircuitState.OPEN or self._opened_at is None:
                return 0.0
            
            elapsed = time.time() - self._opened_at
            remaining = self._current_timeout - elapsed
            return max(0.0, remaining)
    
    # =========================================================================
    # Event Handling
    # =========================================================================
    
    def on(self, event: CircuitEvent, handler: EventHandler) -> 'CircuitBreaker':
        """Register an event handler. Returns self for chaining."""
        self._events.on(event, handler)
        return self
    
    def on_any(self, handler: EventHandler) -> 'CircuitBreaker':
        """Register a handler for all events. Returns self for chaining."""
        self._events.on_any(handler)
        return self
    
    def get_event_history(self, limit: int = 10) -> List[EventRecord]:
        """Get recent event history."""
        return self._events.get_history(limit)
    
    # =========================================================================
    # State Transitions
    # =========================================================================
    
    def _check_state_transition(self) -> None:
        """Check if state should transition (called with lock held)."""
        if self._state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._transition_to_half_open()
    
    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset from open state."""
        if self._opened_at is None:
            return True
        
        elapsed = time.time() - self._opened_at
        return elapsed >= self._current_timeout
    
    def _transition_to_open(self, reason: str = "") -> None:
        """Transition to open state (called with lock held)."""
        old_state = self._state
        self._state = CircuitState.OPEN
        self._opened_at = time.time()
        self._half_open_calls = 0
        
        # Apply exponential backoff if enabled and transitioning from half-open
        # (only apply backoff on subsequent failures, not initial failure)
        if self._config.exponential_backoff and old_state == CircuitState.HALF_OPEN:
            self._current_timeout = min(
                self._current_timeout * self._config.backoff_multiplier,
                self._config.max_timeout
            )
        
        self._stats.state_changes += 1
        
        self._events.emit(
            CircuitEvent.STATE_CHANGE,
            self._state,
            {
                'state_before': old_state,
                'state_after': CircuitState.OPEN,
                'reason': reason
            }
        )
    
    def _transition_to_half_open(self) -> None:
        """Transition to half-open state (called with lock held)."""
        old_state = self._state
        self._state = CircuitState.HALF_OPEN
        self._half_open_calls = 0
        
        self._stats.state_changes += 1
        
        self._events.emit(
            CircuitEvent.STATE_CHANGE,
            self._state,
            {
                'state_before': old_state,
                'state_after': CircuitState.HALF_OPEN
            }
        )
    
    def _transition_to_closed(self) -> None:
        """Transition to closed state (called with lock held)."""
        old_state = self._state
        self._state = CircuitState.CLOSED
        self._opened_at = None
        self._half_open_calls = 0
        self._stats.consecutive_failures = 0
        self._current_timeout = self._config.timeout  # Reset timeout
        
        self._stats.state_changes += 1
        
        self._events.emit(
            CircuitEvent.STATE_CHANGE,
            self._state,
            {
                'state_before': old_state,
                'state_after': CircuitState.CLOSED
            }
        )
    
    # =========================================================================
    # Core Methods
    # =========================================================================
    
    def _should_count_as_failure(self, exception: Exception) -> bool:
        """Check if an exception should count as a failure."""
        # If include_exceptions is specified, only those count
        if self._config.include_exceptions:
            return isinstance(exception, self._config.include_exceptions)
        
        # Otherwise, exclude specified exceptions
        return not isinstance(exception, self._config.excluded_exceptions)
    
    def _record_success(self) -> None:
        """Record a successful call (called with lock held)."""
        self._stats.total_calls += 1
        self._stats.successful_calls += 1
        self._stats.last_success_time = time.time()
        self._stats.consecutive_successes += 1
        self._stats.consecutive_failures = 0
        
        self._events.emit(CircuitEvent.SUCCESS, self._state, {})
        
        if self._state == CircuitState.HALF_OPEN:
            self._half_open_calls += 1
            self._events.emit(CircuitEvent.HALF_OPEN_SUCCESS, self._state, {})
            
            if self._stats.consecutive_successes >= self._config.success_threshold:
                self._transition_to_closed()
    
    def _record_failure(self, exception: Exception) -> None:
        """Record a failed call (called with lock held)."""
        self._stats.total_calls += 1
        self._stats.failed_calls += 1
        self._stats.last_failure_time = time.time()
        self._stats.consecutive_failures += 1
        self._stats.consecutive_successes = 0
        
        self._failure_history.append({
            'time': time.time(),
            'exception': type(exception).__name__,
            'message': str(exception)
        })
        
        self._events.emit(
            CircuitEvent.FAILURE,
            self._state,
            {
                'exception': exception,
                'consecutive_failures': self._stats.consecutive_failures
            }
        )
        
        if self._state == CircuitState.HALF_OPEN:
            self._events.emit(CircuitEvent.HALF_OPEN_FAILURE, self._state, {})
            self._transition_to_open("Failure in half-open state")
        elif self._state == CircuitState.CLOSED:
            self._check_failure_threshold()
    
    def _record_timeout(self) -> None:
        """Record a timeout (called with lock held)."""
        self._stats.total_calls += 1
        self._stats.timeout_calls += 1
        self._events.emit(CircuitEvent.TIMEOUT, self._state, {})
    
    def _record_rejection(self) -> None:
        """Record a rejected call (called with lock held)."""
        self._stats.rejected_calls += 1
        self._events.emit(CircuitEvent.REJECTION, self._state, {})
    
    def _check_failure_threshold(self) -> None:
        """Check if failure threshold is exceeded (called with lock held)."""
        # Check consecutive failure threshold
        if self._stats.consecutive_failures >= self._config.failure_threshold:
            self._transition_to_open(
                f"Consecutive failures ({self._stats.consecutive_failures}) "
                f"exceeded threshold ({self._config.failure_threshold})"
            )
            return
        
        # Check failure rate threshold if configured
        if (self._config.failure_rate_threshold is not None and
            self._stats.total_calls >= self._config.minimum_calls_for_rate):
            if self._stats.failure_rate >= self._config.failure_rate_threshold:
                self._transition_to_open(
                    f"Failure rate ({self._stats.failure_rate:.2%}) "
                    f"exceeded threshold ({self._config.failure_rate_threshold:.2%})"
                )
    
    def _can_execute(self) -> bool:
        """Check if execution is allowed (called with lock held)."""
        self._check_state_transition()
        
        if self._state == CircuitState.CLOSED:
            return True
        
        if self._state == CircuitState.OPEN:
            return False
        
        if self._state == CircuitState.HALF_OPEN:
            return self._half_open_calls < self._config.half_open_max_calls
        
        return False
    
    def allow_request(self) -> bool:
        """
        Check if a request is allowed.
        
        Returns:
            True if request can proceed, False otherwise
        """
        with self._lock:
            return self._can_execute()
    
    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        Execute a function with circuit breaker protection.
        
        Args:
            func: Function to execute
            *args: Arguments for function
            **kwargs: Keyword arguments for function
            
        Returns:
            Function result
            
        Raises:
            CircuitOpenError: If circuit is open
            Exception: Any exception from the function
        """
        with self._lock:
            if not self._can_execute():
                self._record_rejection()
                raise CircuitOpenError(
                    f"Circuit '{self.name}' is open",
                    time_until_retry=self.time_until_retry
                )
        
        try:
            result = func(*args, **kwargs)
            with self._lock:
                self._record_success()
            return result
            
        except Exception as e:
            with self._lock:
                if self._should_count_as_failure(e):
                    self._record_failure(e)
            raise
    
    def protect(self, func: Callable[..., T]) -> Callable[..., T]:
        """
        Decorator to protect a function with circuit breaker.
        
        Example:
            >>> breaker = CircuitBreaker(failure_threshold=3)
            >>> 
            >>> @breaker.protect
            ... def my_function():
            ...     return "success"
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return self.call(func, *args, **kwargs)
        return wrapper
    
    def __enter__(self) -> 'CircuitBreaker':
        """Enter context manager."""
        with self._lock:
            if not self._can_execute():
                self._record_rejection()
                raise CircuitOpenError(
                    f"Circuit '{self.name}' is open",
                    time_until_retry=self.time_until_retry
                )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Exit context manager."""
        with self._lock:
            if exc_type is None:
                self._record_success()
            elif self._should_count_as_failure(exc_val):
                self._record_failure(exc_val)
        return False  # Don't suppress exceptions
    
    def reset(self) -> None:
        """
        Manually reset the circuit breaker.
        
        Resets to closed state and clears all statistics.
        """
        with self._lock:
            old_state = self._state
            self._state = CircuitState.CLOSED
            self._opened_at = None
            self._half_open_calls = 0
            self._current_timeout = self._config.timeout
            self._stats.reset()
            self._failure_history.clear()
            
            if old_state != CircuitState.CLOSED:
                self._events.emit(
                    CircuitEvent.STATE_CHANGE,
                    self._state,
                    {
                        'state_before': old_state,
                        'state_after': CircuitState.CLOSED,
                        'reason': 'manual_reset'
                    }
                )
    
    def force_open(self, reason: str = "forced") -> None:
        """Manually open the circuit breaker."""
        with self._lock:
            self._transition_to_open(reason)
    
    def force_close(self) -> None:
        """Manually close the circuit breaker."""
        with self._lock:
            self._transition_to_closed()
    
    def get_failure_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent failure history."""
        with self._lock:
            return list(self._failure_history)[-limit:]
    
    def __repr__(self) -> str:
        return (
            f"CircuitBreaker(name={self.name!r}, state={self._state.name}, "
            f"failures={self._stats.consecutive_failures})"
        )


# =============================================================================
# Circuit Breaker Registry
# =============================================================================

class CircuitBreakerRegistry:
    """
    Registry for managing multiple circuit breakers.
    
    Example:
        >>> registry = CircuitBreakerRegistry()
        >>> 
        >>> # Get or create a circuit breaker
        >>> db_breaker = registry.get_or_create('database', failure_threshold=5)
        >>> 
        >>> # List all circuit breakers
        >>> for name, breaker in registry.all():
        ...     print(f"{name}: {breaker.state.name}")
    """
    
    _instance: Optional['CircuitBreakerRegistry'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'CircuitBreakerRegistry':
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._breakers: Dict[str, CircuitBreaker] = {}
                cls._instance._breaker_lock = threading.RLock()
            return cls._instance
    
    @classmethod
    def get_instance(cls) -> 'CircuitBreakerRegistry':
        """Get the singleton instance."""
        return cls()
    
    def get_or_create(
        self,
        name: str,
        **kwargs
    ) -> CircuitBreaker:
        """Get an existing circuit breaker or create a new one."""
        with self._breaker_lock:
            if name not in self._breakers:
                self._breakers[name] = CircuitBreaker(name=name, **kwargs)
            return self._breakers[name]
    
    def get(self, name: str) -> Optional[CircuitBreaker]:
        """Get a circuit breaker by name."""
        with self._breaker_lock:
            return self._breakers.get(name)
    
    def remove(self, name: str) -> Optional[CircuitBreaker]:
        """Remove a circuit breaker by name."""
        with self._breaker_lock:
            return self._breakers.pop(name, None)
    
    def all(self) -> List[tuple]:
        """Get all circuit breakers as (name, breaker) tuples."""
        with self._breaker_lock:
            return list(self._breakers.items())
    
    def reset_all(self) -> None:
        """Reset all circuit breakers."""
        with self._breaker_lock:
            for breaker in self._breakers.values():
                breaker.reset()
    
    def get_health(self) -> Dict[str, Dict[str, Any]]:
        """Get health status of all circuit breakers."""
        with self._breaker_lock:
            return {
                name: {
                    'state': breaker.state.name,
                    'stats': {
                        'total_calls': breaker.stats.total_calls,
                        'successful_calls': breaker.stats.successful_calls,
                        'failed_calls': breaker.stats.failed_calls,
                        'rejected_calls': breaker.stats.rejected_calls,
                        'failure_rate': breaker.stats.failure_rate,
                    }
                }
                for name, breaker in self._breakers.items()
            }


# =============================================================================
# Async Support (for Python 3.7+)
# =============================================================================

class AsyncCircuitBreaker:
    """
    Async version of CircuitBreaker.
    
    Example:
        >>> breaker = AsyncCircuitBreaker(failure_threshold=3)
        >>> 
        >>> @breaker.protect
        ... async def my_async_function():
        ...     return "success"
    """
    
    def __init__(self, **kwargs):
        """Initialize async circuit breaker with same options as CircuitBreaker."""
        self._sync_breaker = CircuitBreaker(**kwargs)
    
    @property
    def state(self) -> CircuitState:
        """Get current state."""
        return self._sync_breaker.state
    
    @property
    def stats(self) -> CircuitStats:
        """Get statistics."""
        return self._sync_breaker.stats
    
    @property
    def is_closed(self) -> bool:
        """Check if circuit is closed."""
        return self._sync_breaker.is_closed
    
    @property
    def is_open(self) -> bool:
        """Check if circuit is open."""
        return self._sync_breaker.is_open
    
    @property
    def is_half_open(self) -> bool:
        """Check if circuit is half-open."""
        return self._sync_breaker.is_half_open
    
    async def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute an async function with circuit breaker protection."""
        import asyncio
        import inspect
        
        if not self._sync_breaker.allow_request():
            with self._sync_breaker._lock:
                self._sync_breaker._record_rejection()
            raise CircuitOpenError(
                f"Circuit '{self._sync_breaker.name}' is open",
                time_until_retry=self._sync_breaker.time_until_retry
            )
        
        try:
            if inspect.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            with self._sync_breaker._lock:
                self._sync_breaker._record_success()
            return result
            
        except Exception as e:
            with self._sync_breaker._lock:
                if self._sync_breaker._should_count_as_failure(e):
                    self._sync_breaker._record_failure(e)
            raise
    
    def protect(self, func: Callable[..., T]) -> Callable[..., T]:
        """Decorator to protect an async function."""
        import asyncio
        import functools
        import inspect
        
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await self.call(func, *args, **kwargs)
            return async_wrapper
        else:
            return self._sync_breaker.protect(func)
    
    def reset(self) -> None:
        """Reset the circuit breaker."""
        self._sync_breaker.reset()
    
    def on(self, event: CircuitEvent, handler: EventHandler) -> 'AsyncCircuitBreaker':
        """Register an event handler."""
        self._sync_breaker.on(event, handler)
        return self


# =============================================================================
# Utility Functions
# =============================================================================

def create_circuit_breaker(name: str = "default", **kwargs) -> CircuitBreaker:
    """
    Create a new circuit breaker.
    
    Args:
        name: Name for the circuit breaker
        **kwargs: Configuration options
        
    Returns:
        New CircuitBreaker instance
    """
    return CircuitBreaker(name=name, **kwargs)


def get_registry() -> CircuitBreakerRegistry:
    """Get the global circuit breaker registry."""
    return CircuitBreakerRegistry.get_instance()


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    # Demo usage
    print("Circuit Breaker Utilities Demo")
    print("=" * 50)
    
    # Create a circuit breaker
    breaker = CircuitBreaker(
        name="demo",
        failure_threshold=3,
        timeout=5,
        success_threshold=2
    )
    
    # Add event handlers
    def on_state_change(event, state, details):
        print(f"[EVENT] State changed: {details.get('state_before')} -> {details.get('state_after')}")
    
    def on_failure(event, state, details):
        print(f"[EVENT] Failure recorded: {details.get('consecutive_failures')} consecutive")
    
    breaker.on(CircuitEvent.STATE_CHANGE, on_state_change)
    breaker.on(CircuitEvent.FAILURE, on_failure)
    
    print("\n1. Testing with successful calls:")
    for i in range(5):
        try:
            result = breaker.call(lambda: f"Success {i}")
            print(f"   Call {i}: {result} - State: {breaker.state.name}")
        except CircuitOpenError as e:
            print(f"   Call {i}: REJECTED - {e}")
    
    print(f"\n   Stats: {breaker.stats.successful_calls} successes, {breaker.stats.failed_calls} failures")
    
    print("\n2. Testing with failures (will trigger open):")
    for i in range(5):
        try:
            breaker.call(lambda: 1/0)  # Intentional error
        except ZeroDivisionError:
            print(f"   Call {i}: Failed (ZeroDivisionError) - State: {breaker.state.name}")
        except CircuitOpenError as e:
            print(f"   Call {i}: REJECTED - Circuit is open")
    
    print(f"\n   Stats: {breaker.stats.successful_calls} successes, {breaker.stats.failed_calls} failures")
    print(f"   Current state: {breaker.state.name}")
    
    print("\n3. Testing rejection when open:")
    try:
        breaker.call(lambda: "This won't execute")
    except CircuitOpenError as e:
        print(f"   Rejected as expected. Time until retry: {e.time_until_retry:.1f}s")
    
    print("\n4. Simulating timeout and recovery:")
    import time
    print(f"   Waiting for timeout ({breaker.config.timeout}s)...")
    time.sleep(breaker.config.timeout + 0.5)
    
    print(f"   State after timeout: {breaker.state.name}")
    
    print("\n5. Testing recovery in half-open state:")
    for i in range(3):
        try:
            result = breaker.call(lambda: f"Recovery {i}")
            print(f"   Call {i}: {result} - State: {breaker.state.name}")
        except CircuitOpenError:
            print(f"   Call {i}: REJECTED")
    
    print(f"\n   Final state: {breaker.state.name}")
    print(f"   Final stats: {breaker.stats.successful_calls} successes, {breaker.stats.failed_calls} failures")
    
    print("\n6. Testing with decorator:")
    @breaker.protect
    def protected_function(value):
        return f"Protected: {value}"
    
    try:
        result = protected_function("test")
        print(f"   Decorator result: {result}")
    except CircuitOpenError as e:
        print(f"   Decorator rejected: {e}")
    
    print("\n7. Testing with context manager:")
    try:
        with breaker:
            print("   Inside context manager - executing safely")
    except CircuitOpenError:
        print("   Context manager blocked - circuit is open")
    
    print("\n8. Registry demo:")
    registry = get_registry()
    
    # Create breakers via registry
    api_breaker = registry.get_or_create('api', failure_threshold=10)
    db_breaker = registry.get_or_create('database', failure_threshold=5)
    
    print(f"   Registered breakers: {[name for name, _ in registry.all()]}")
    
    # Reset and show health
    breaker.reset()
    health = registry.get_health()
    print(f"   Health status:")
    for name, status in health.items():
        print(f"     {name}: {status['state']}")
    
    print("\n" + "=" * 50)
    print("Demo complete!")