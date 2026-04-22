"""
Sliding Window Token Bucket Implementation

A hybrid approach combining token bucket with sliding window:
- Maintains the burst handling of token bucket
- Uses sliding window for smoother rate enforcement
- Prevents the "burst at window edge" problem

Useful for API rate limiting where smooth distribution matters.

Time complexity:
- consume: O(1) amortized
- cleanup: O(n) where n is number of recorded requests

Space complexity: O(window_size * request_rate)
"""

import time
from typing import List, Tuple
from collections import deque


class SlidingWindowBucket:
    """
    Sliding window rate limiter with token bucket semantics.
    
    Combines sliding window precision with token bucket burst handling.
    Records individual request timestamps for accurate rate limiting.
    
    Attributes:
        capacity: Maximum burst size
        rate: Maximum requests per second (smoothed over window)
        window_size: Size of sliding window in seconds
    
    Example:
        >>> bucket = SlidingWindowBucket(capacity=10, rate=2, window_size=1.0)
        >>> bucket.consume(5)  # Burst allowed
        True
        >>> bucket.consume(10)  # Exceeds capacity
        False
    """
    
    def __init__(
        self, 
        capacity: int, 
        rate: float, 
        window_size: float = 1.0
    ):
        """
        Initialize sliding window bucket.
        
        Args:
            capacity: Maximum burst capacity
            rate: Maximum requests per second
            window_size: Sliding window size in seconds
        
        Note:
            The effective rate limit is 'rate' requests per 'window_size' seconds.
            For typical API limiting, use window_size=1.0.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if rate <= 0:
            raise ValueError("Rate must be positive")
        if window_size <= 0:
            raise ValueError("Window size must be positive")
        
        self.capacity = capacity
        self.rate = rate
        self.window_size = window_size
        self._requests: deque = deque()  # Timestamps of requests
        self._total_tokens = float(capacity)
        self._last_refill = time.time()
    
    def _cleanup(self) -> None:
        """Remove expired request records."""
        now = time.time()
        cutoff = now - self.window_size
        
        while self._requests and self._requests[0] < cutoff:
            self._requests.popleft()
    
    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self._last_refill
        
        if elapsed > 0:
            new_tokens = elapsed * self.rate
            self._total_tokens = min(self.capacity, self._total_tokens + new_tokens)
            self._last_refill = now
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens using sliding window logic.
        
        Args:
            tokens: Number of tokens to consume
        
        Returns:
            True if request allowed, False if rate limited
        """
        if tokens <= 0:
            raise ValueError("Token count must be positive")
        
        now = time.time()
        self._cleanup()
        self._refill()
        
        # Check sliding window constraint
        window_requests = sum(
            1 for ts in self._requests 
            if ts >= now - self.window_size
        )
        
        max_in_window = int(self.rate * self.window_size)
        
        # Check both burst capacity and window rate
        if self._total_tokens >= tokens and window_requests + tokens <= max_in_window:
            self._total_tokens -= tokens
            self._requests.append(now)
            return True
        
        return False
    
    def available(self) -> float:
        """Get currently available tokens."""
        self._cleanup()
        self._refill()
        return self._total_tokens
    
    def requests_in_window(self) -> int:
        """Get number of requests in current window."""
        self._cleanup()
        return len(self._requests)
    
    def wait_time(self, tokens: int = 1) -> float:
        """
        Calculate time until tokens available.
        
        Returns:
            Estimated seconds to wait
        """
        if tokens <= 0:
            return 0.0
        
        self._cleanup()
        self._refill()
        
        # Token-based wait time
        if self._total_tokens < tokens:
            token_wait = (tokens - self._total_tokens) / self.rate
        else:
            token_wait = 0.0
        
        # Window-based wait time
        if self._requests:
            oldest = self._requests[0]
            window_wait = oldest + self.window_size - time.time()
            window_wait = max(0, window_wait)
        else:
            window_wait = 0.0
        
        return max(token_wait, window_wait)
    
    def reset(self) -> None:
        """Reset bucket to full capacity."""
        self._requests.clear()
        self._total_tokens = float(self.capacity)
        self._last_refill = time.time()
    
    def __repr__(self) -> str:
        return (
            f"SlidingWindowBucket(capacity={self.capacity}, "
            f"rate={self.rate}, window={self.window_size}s)"
        )