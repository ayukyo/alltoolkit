"""
Throttle Utilities - Function throttling with multiple modes.

Throttling limits the rate of function calls, ensuring a function
is not called more than once in a specified time window.

Modes:
- leading: Call immediately on first invocation, then throttle
- trailing: Wait until the throttle period ends before calling
- both: Call immediately AND at the end of the throttle period

This is different from rate limiting (limits call count per window)
and debouncing (waits for a pause before calling).
"""

import time
from typing import Callable, TypeVar, Generic, Optional, Any, Dict, Tuple, List, Union
from functools import wraps
from threading import Lock
from dataclasses import dataclass, field
from enum import Enum

T = TypeVar('T')


class ThrottleMode(Enum):
    """Throttle behavior modes."""
    LEADING = "leading"      # Call immediately, then throttle
    TRAILING = "trailing"    # Wait until throttle period ends
    BOTH = "both"           # Call immediately AND at end of period


@dataclass
class ThrottleState:
    """Internal state for throttled function."""
    last_call_time: float = 0.0
    last_result: Any = None
    pending_args: Tuple = ()
    pending_kwargs: Dict = field(default_factory=dict)
    has_pending: bool = False
    leading_called: bool = False


class ThrottledFunction(Generic[T]):
    """
    A throttled function wrapper with configurable behavior.
    
    Usage:
        @throttle(0.1, mode='leading')
        def my_func(x):
            return x * 2
    """
    
    def __init__(
        self,
        func: Callable[..., T],
        interval: float,
        mode: Union[ThrottleMode, str] = ThrottleMode.LEADING,
        leading: Optional[bool] = None,
        trailing: Optional[bool] = None,
    ):
        self.func = func
        self.interval = interval
        self._lock = Lock()
        self._state = ThrottleState()
        
        # Handle mode configuration
        if isinstance(mode, str):
            mode = ThrottleMode(mode.lower())
        
        # Override mode with explicit leading/trailing if provided
        if leading is not None or trailing is not None:
            self.leading = leading if leading is not None else False
            self.trailing = trailing if trailing is not None else True
        else:
            if mode == ThrottleMode.LEADING:
                self.leading = True
                self.trailing = False
            elif mode == ThrottleMode.TRAILING:
                self.leading = False
                self.trailing = True
            else:  # BOTH
                self.leading = True
                self.trailing = True
    
    def __call__(self, *args, **kwargs) -> T:
        """Execute the throttled function."""
        with self._lock:
            now = time.time()
            elapsed = now - self._state.last_call_time
            
            # First call ever
            if self._state.last_call_time == 0:
                self._state.last_call_time = now
                if self.leading:
                    self._state.leading_called = True
                    self._state.last_result = self.func(*args, **kwargs)
                    return self._state.last_result
                else:
                    self._state.pending_args = args
                    self._state.pending_kwargs = kwargs
                    self._state.has_pending = True
                    return None
            
            # Within throttle window
            if elapsed < self.interval:
                # Store pending call for trailing
                if self.trailing:
                    self._state.pending_args = args
                    self._state.pending_kwargs = kwargs
                    self._state.has_pending = True
                return self._state.last_result
            
            # Throttle window has passed
            remaining = elapsed - self.interval
            
            # Execute leading call if enabled and not already called
            if self.leading and not self._state.leading_called:
                self._state.leading_called = True
                self._state.last_call_time = now
                self._state.last_result = self.func(*args, **kwargs)
                self._state.has_pending = False
                return self._state.last_result
            
            # Execute trailing call if pending
            if self.trailing and self._state.has_pending:
                self._state.last_call_time = now
                self._state.leading_called = False
                self._state.last_result = self.func(
                    *self._state.pending_args,
                    **self._state.pending_kwargs
                )
                self._state.has_pending = False
                return self._state.last_result
            
            # Fresh call - leading edge
            if self.leading:
                self._state.last_call_time = now
                self._state.leading_called = True
                self._state.last_result = self.func(*args, **kwargs)
                return self._state.last_result
            else:
                # Trailing mode - store and return previous
                self._state.pending_args = args
                self._state.pending_kwargs = kwargs
                self._state.has_pending = True
                self._state.last_call_time = now
                self._state.leading_called = False
                return self._state.last_result
    
    def cancel(self) -> None:
        """Cancel any pending trailing call."""
        with self._lock:
            self._state.has_pending = False
            self._state.pending_args = ()
            self._state.pending_kwargs = {}
    
    def flush(self) -> Optional[T]:
        """
        Immediately execute any pending trailing call.
        Returns the result of the pending call, or None if no pending call.
        """
        with self._lock:
            if self._state.has_pending:
                result = self.func(
                    *self._state.pending_args,
                    **self._state.pending_kwargs
                )
                self._state.last_result = result
                self._state.last_call_time = time.time()
                self._state.has_pending = False
                self._state.leading_called = False
                return result
            return None
    
    def pending(self) -> bool:
        """Check if there's a pending trailing call."""
        with self._lock:
            return self._state.has_pending
    
    def reset(self) -> None:
        """Reset the throttle state completely."""
        with self._lock:
            self._state = ThrottleState()


def throttle(
    interval: float,
    mode: Union[ThrottleMode, str] = ThrottleMode.LEADING,
    leading: Optional[bool] = None,
    trailing: Optional[bool] = None,
) -> Callable[[Callable[..., T]], ThrottledFunction[T]]:
    """
    Decorator to throttle function calls.
    
    Args:
        interval: Minimum time between calls in seconds
        mode: ThrottleMode.LEADING, TRAILING, or BOTH
        leading: Override - call immediately on first invocation
        trailing: Override - call at end of throttle period
    
    Returns:
        Decorated function with throttling behavior
    
    Examples:
        @throttle(0.1)  # Leading mode by default
        def handle_scroll(y):
            print(f"Scrolling: {y}")
        
        @throttle(0.1, mode='trailing')
        def handle_resize(width, height):
            print(f"Resized to {width}x{height}")
        
        @throttle(0.1, leading=True, trailing=True)
        def handle_input(value):
            print(f"Input: {value}")
    """
    def decorator(func: Callable[..., T]) -> ThrottledFunction[T]:
        return ThrottledFunction(
            func, interval, mode, leading=leading, trailing=trailing
        )
    return decorator


class AsyncThrottledFunction(Generic[T]):
    """
    Async version of ThrottledFunction.
    
    Usage:
        @athrottle(0.1)
        async def my_async_func(x):
            return x * 2
    """
    
    def __init__(
        self,
        func: Callable[..., T],
        interval: float,
        mode: Union[ThrottleMode, str] = ThrottleMode.LEADING,
        leading: Optional[bool] = None,
        trailing: Optional[bool] = None,
    ):
        self.func = func
        self.interval = interval
        self._lock = Lock()
        self._state = ThrottleState()
        
        if isinstance(mode, str):
            mode = ThrottleMode(mode.lower())
        
        if leading is not None or trailing is not None:
            self.leading = leading if leading is not None else False
            self.trailing = trailing if trailing is not None else True
        else:
            if mode == ThrottleMode.LEADING:
                self.leading = True
                self.trailing = False
            elif mode == ThrottleMode.TRAILING:
                self.leading = False
                self.trailing = True
            else:
                self.leading = True
                self.trailing = True
    
    async def __call__(self, *args, **kwargs) -> T:
        """Execute the throttled async function."""
        import asyncio
        
        with self._lock:
            now = time.time()
            elapsed = now - self._state.last_call_time
            
            if self._state.last_call_time == 0:
                self._state.last_call_time = now
                if self.leading:
                    self._state.leading_called = True
                    self._state.last_result = await self.func(*args, **kwargs)
                    return self._state.last_result
                else:
                    self._state.pending_args = args
                    self._state.pending_kwargs = kwargs
                    self._state.has_pending = True
                    return None
            
            if elapsed < self.interval:
                if self.trailing:
                    self._state.pending_args = args
                    self._state.pending_kwargs = kwargs
                    self._state.has_pending = True
                return self._state.last_result
            
            if self.leading and not self._state.leading_called:
                self._state.leading_called = True
                self._state.last_call_time = now
                self._state.last_result = await self.func(*args, **kwargs)
                self._state.has_pending = False
                return self._state.last_result
            
            if self.trailing and self._state.has_pending:
                self._state.last_call_time = now
                self._state.leading_called = False
                self._state.last_result = await self.func(
                    *self._state.pending_args,
                    **self._state.pending_kwargs
                )
                self._state.has_pending = False
                return self._state.last_result
            
            if self.leading:
                self._state.last_call_time = now
                self._state.leading_called = True
                self._state.last_result = await self.func(*args, **kwargs)
                return self._state.last_result
            else:
                self._state.pending_args = args
                self._state.pending_kwargs = kwargs
                self._state.has_pending = True
                self._state.last_call_time = now
                self._state.leading_called = False
                return self._state.last_result
    
    def cancel(self) -> None:
        """Cancel any pending trailing call."""
        with self._lock:
            self._state.has_pending = False
            self._state.pending_args = ()
            self._state.pending_kwargs = {}
    
    async def flush(self) -> Optional[T]:
        """Immediately execute any pending trailing call."""
        with self._lock:
            if self._state.has_pending:
                result = await self.func(
                    *self._state.pending_args,
                    **self._state.pending_kwargs
                )
                self._state.last_result = result
                self._state.last_call_time = time.time()
                self._state.has_pending = False
                self._state.leading_called = False
                return result
            return None
    
    def pending(self) -> bool:
        """Check if there's a pending trailing call."""
        with self._lock:
            return self._state.has_pending
    
    def reset(self) -> None:
        """Reset the throttle state completely."""
        with self._lock:
            self._state = ThrottleState()


def athrottle(
    interval: float,
    mode: Union[ThrottleMode, str] = ThrottleMode.LEADING,
    leading: Optional[bool] = None,
    trailing: Optional[bool] = None,
) -> Callable[[Callable[..., T]], AsyncThrottledFunction[T]]:
    """
    Decorator to throttle async function calls.
    
    Args:
        interval: Minimum time between calls in seconds
        mode: ThrottleMode.LEADING, TRAILING, or BOTH
        leading: Override - call immediately on first invocation
        trailing: Override - call at end of throttle period
    
    Examples:
        @athrottle(0.1)
        async def handle_scroll(y):
            print(f"Scrolling: {y}")
    """
    def decorator(func: Callable[..., T]) -> AsyncThrottledFunction[T]:
        return AsyncThrottledFunction(
            func, interval, mode, leading=leading, trailing=trailing
        )
    return decorator


class ThrottleQueue:
    """
    A queue that throttles the rate at which items are processed.
    
    Useful for rate-limiting API calls, database writes, etc.
    
    Example:
        queue = ThrottleQueue(process_item, interval=0.1)
        queue.enqueue(item1)
        queue.enqueue(item2)  # Will wait for interval
    """
    
    def __init__(
        self,
        processor: Callable[[Any], T],
        interval: float,
        max_queue_size: int = 1000,
    ):
        self.processor = processor
        self.interval = interval
        self.max_queue_size = max_queue_size
        self._queue: List[Tuple[Tuple, Dict]] = []
        self._last_process_time = 0.0
        self._lock = Lock()
    
    def enqueue(self, *args, **kwargs) -> bool:
        """
        Add an item to the queue.
        
        Returns True if added, False if queue is full.
        """
        with self._lock:
            if len(self._queue) >= self.max_queue_size:
                return False
            self._queue.append((args, kwargs))
            return True
    
    def process_next(self) -> Optional[T]:
        """
        Process the next item if enough time has passed.
        
        Returns the result, or None if no items or throttled.
        """
        with self._lock:
            if not self._queue:
                return None
            
            now = time.time()
            elapsed = now - self._last_process_time
            
            if elapsed < self.interval:
                return None
            
            args, kwargs = self._queue.pop(0)
            self._last_process_time = now
            return self.processor(*args, **kwargs)
    
    def process_all_available(self) -> List[T]:
        """
        Process all items that can be processed immediately.
        
        Returns list of results.
        """
        results = []
        while True:
            result = self.process_next()
            if result is None:
                break
            results.append(result)
        return results
    
    def clear(self) -> None:
        """Clear all pending items."""
        with self._lock:
            self._queue.clear()
    
    def size(self) -> int:
        """Get current queue size."""
        with self._lock:
            return len(self._queue)
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        with self._lock:
            return len(self._queue) == 0


class SlidingThrottle:
    """
    Sliding window throttle - ensures minimum time between each call.
    
    More precise than fixed interval throttling.
    """
    
    def __init__(self, interval: float):
        self.interval = interval
        self._last_call_time = 0.0
        self._lock = Lock()
    
    def acquire(self) -> float:
        """
        Acquire permission to proceed.
        
        Returns the time to wait before proceeding (0 if can proceed immediately).
        """
        with self._lock:
            now = time.time()
            elapsed = now - self._last_call_time
            
            if elapsed >= self.interval:
                self._last_call_time = now
                return 0.0
            
            wait_time = self.interval - elapsed
            return wait_time
    
    def wait_and_acquire(self) -> None:
        """Wait if necessary, then acquire."""
        wait_time = self.acquire()
        if wait_time > 0:
            time.sleep(wait_time)
            with self._lock:
                self._last_call_time = time.time()
    
    def try_acquire(self) -> bool:
        """Try to acquire immediately. Returns True if successful."""
        with self._lock:
            now = time.time()
            elapsed = now - self._last_call_time
            
            if elapsed >= self.interval:
                self._last_call_time = now
                return True
            return False
    
    def reset(self) -> None:
        """Reset the throttle."""
        with self._lock:
            self._last_call_time = 0.0


class TokenBucketThrottle:
    """
    Token bucket throttle for rate limiting.
    
    Allows bursts up to bucket capacity, then throttles to refill rate.
    
    Example:
        bucket = TokenBucketThrottle(
            capacity=10,  # Max 10 tokens
            refill_rate=2  # 2 tokens per second
        )
        if bucket.try_consume(1):
            # Make API call
            pass
    """
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket.
        
        Args:
            capacity: Maximum number of tokens
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.time()
        self._lock = Lock()
    
    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self._last_refill
        tokens_to_add = elapsed * self.refill_rate
        self._tokens = min(float(self.capacity), self._tokens + tokens_to_add)
        self._last_refill = now
    
    def try_consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens.
        
        Returns True if successful, False if not enough tokens.
        """
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False
    
    def consume(self, tokens: int = 1) -> float:
        """
        Consume tokens, waiting if necessary.
        
        Returns time waited in seconds.
        """
        with self._lock:
            self._refill()
            
            if self._tokens >= tokens:
                self._tokens -= tokens
                return 0.0
            
            tokens_needed = tokens - self._tokens
            wait_time = tokens_needed / self.refill_rate
            self._tokens = 0.0
            return wait_time
    
    def available(self) -> float:
        """Get current available tokens."""
        with self._lock:
            self._refill()
            return self._tokens
    
    def reset(self) -> None:
        """Reset to full capacity."""
        with self._lock:
            self._tokens = float(self.capacity)
            self._last_refill = time.time()


class AdaptiveThrottle:
    """
    Adaptive throttle that adjusts interval based on success/failure.
    
    Useful for handling backpressure from APIs or services.
    
    Example:
        throttle = AdaptiveThrottle(
            initial_interval=0.1,
            min_interval=0.01,
            max_interval=1.0,
            backoff_factor=2.0
        )
        
        # On success:
        throttle.success()
        
        # On failure (like 429 Too Many Requests):
        throttle.failure()
    """
    
    def __init__(
        self,
        initial_interval: float = 0.1,
        min_interval: float = 0.01,
        max_interval: float = 1.0,
        backoff_factor: float = 2.0,
        recovery_factor: float = 0.9,
    ):
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.backoff_factor = backoff_factor
        self.recovery_factor = recovery_factor
        self._interval = initial_interval
        self._last_call_time = 0.0
        self._lock = Lock()
    
    @property
    def interval(self) -> float:
        """Current throttle interval."""
        return self._interval
    
    def acquire(self) -> float:
        """Acquire permission. Returns wait time (0 if immediate)."""
        with self._lock:
            now = time.time()
            elapsed = now - self._last_call_time
            
            if elapsed >= self._interval:
                self._last_call_time = now
                return 0.0
            
            return self._interval - elapsed
    
    def success(self) -> None:
        """Called on successful operation - gradually reduce interval."""
        with self._lock:
            self._interval = max(
                self.min_interval,
                self._interval * self.recovery_factor
            )
    
    def failure(self) -> None:
        """Called on failure - increase interval (backoff)."""
        with self._lock:
            self._interval = min(
                self.max_interval,
                self._interval * self.backoff_factor
            )
    
    def reset(self) -> None:
        """Reset to initial state."""
        with self._lock:
            self._interval = self.min_interval
            self._last_call_time = 0.0


# Convenience function for creating throttles
def create_throttle(
    interval: float,
    mode: str = "leading",
    **kwargs
) -> Callable[[Callable], ThrottledFunction]:
    """
    Convenience function to create a throttle decorator.
    
    Args:
        interval: Minimum time between calls
        mode: 'leading', 'trailing', or 'both'
        **kwargs: Additional options for ThrottledFunction
    
    Returns:
        Decorator function
    """
    return throttle(interval, mode=mode, **kwargs)


__all__ = [
    'ThrottleMode',
    'ThrottledFunction',
    'AsyncThrottledFunction',
    'throttle',
    'athrottle',
    'ThrottleQueue',
    'SlidingThrottle',
    'TokenBucketThrottle',
    'AdaptiveThrottle',
    'create_throttle',
]