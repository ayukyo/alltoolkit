"""
Thread-Safe Token Bucket Implementation

Provides a thread-safe version of the token bucket using threading.Lock.
Suitable for multi-threaded applications where multiple threads need to
consume tokens from the same bucket.

Time complexity:
- All operations: O(1) + lock overhead

Space complexity: O(1)
"""

import time
import threading
from typing import Optional, Callable
from contextlib import contextmanager


class ThreadSafeTokenBucket:
    """
    A thread-safe token bucket rate limiter.
    
    Uses a threading.Lock to ensure atomic operations. Supports:
    - Context manager for automatic token release
    - Callbacks on rate limit events
    - Non-blocking and blocking consume operations
    
    Example:
        >>> bucket = ThreadSafeTokenBucket(capacity=10, refill_rate=2)
        >>> with bucket.consume_or_wait(5):
        ...     # Do rate-limited work
        ...     pass
    """
    
    def __init__(
        self, 
        capacity: int, 
        refill_rate: float,
        on_limited: Optional[Callable[[int, float], None]] = None
    ):
        """
        Initialize the thread-safe token bucket.
        
        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second to add
            on_limited: Optional callback(tokens_needed, wait_time)
                       called when rate limited
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.time()
        self._lock = threading.Lock()
        self._on_limited = on_limited
    
    def _refill_unlocked(self) -> None:
        """Add tokens based on elapsed time (must hold lock)."""
        now = time.time()
        elapsed = now - self._last_refill
        
        if elapsed > 0:
            new_tokens = elapsed * self.refill_rate
            self._tokens = min(self.capacity, self._tokens + new_tokens)
            self._last_refill = now
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens atomically.
        
        Args:
            tokens: Number of tokens to consume
        
        Returns:
            True if consumed, False if insufficient tokens
        """
        if tokens <= 0:
            raise ValueError("Token count must be positive")
        
        with self._lock:
            self._refill_unlocked()
            
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False
    
    def consume_blocking(self, tokens: int = 1, timeout: Optional[float] = None) -> bool:
        """
        Consume tokens, blocking until available or timeout.
        
        Args:
            tokens: Number of tokens to consume
            timeout: Maximum seconds to wait (None = forever)
        
        Returns:
            True if consumed, False if timeout
        
        Example:
            >>> bucket = ThreadSafeTokenBucket(5, 1)
            >>> bucket.consume_blocking(10, timeout=5)  # Wait up to 5s
            True
        """
        if tokens <= 0:
            raise ValueError("Token count must be positive")
        
        start_time = time.time()
        
        while True:
            with self._lock:
                self._refill_unlocked()
                
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return True
                
                # Calculate wait time
                needed = tokens - self._tokens
                wait_time = needed / self.refill_rate
            
            # Check timeout
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return False
                wait_time = min(wait_time, timeout - elapsed)
            
            # Wait before retrying
            if self._on_limited:
                self._on_limited(tokens, wait_time)
            
            time.sleep(min(wait_time, 0.1))  # Poll frequently for responsiveness
    
    @contextmanager
    def consume_or_wait(self, tokens: int = 1, timeout: Optional[float] = None):
        """
        Context manager that waits for tokens and releases on exit.
        
        Note: Tokens are not automatically returned; this is for
        timing/scoping purposes.
        
        Args:
            tokens: Number of tokens to consume
            timeout: Maximum seconds to wait
        
        Yields:
            True if tokens were consumed
        
        Example:
            >>> bucket = ThreadSafeTokenBucket(10, 1)
            >>> with bucket.consume_or_wait(5) as acquired:
            ...     if acquired:
            ...         # Do work
            ...         pass
        """
        acquired = self.consume_blocking(tokens, timeout)
        try:
            yield acquired
        finally:
            pass  # Tokens are consumed, not returned
    
    def available(self) -> float:
        """Get current available tokens (thread-safe)."""
        with self._lock:
            self._refill_unlocked()
            return self._tokens
    
    def wait_time(self, tokens: int = 1) -> float:
        """Calculate time to wait for tokens (thread-safe)."""
        with self._lock:
            self._refill_unlocked()
            if self._tokens >= tokens:
                return 0.0
            needed = tokens - self._tokens
            return needed / self.refill_rate
    
    def reset(self) -> None:
        """Reset bucket to full capacity."""
        with self._lock:
            self._tokens = float(self.capacity)
            self._last_refill = time.time()
    
    def __repr__(self) -> str:
        return (
            f"ThreadSafeTokenBucket(capacity={self.capacity}, "
            f"refill_rate={self.refill_rate})"
        )