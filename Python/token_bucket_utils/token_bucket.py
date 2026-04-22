"""
Basic Token Bucket Implementation

The token bucket algorithm:
1. Tokens are added to the bucket at a fixed rate (refill_rate)
2. The bucket has a maximum capacity (burst_capacity)
3. Each request consumes tokens
4. If insufficient tokens, the request is denied

Time complexity:
- consume: O(1)
- refill: O(1)

Space complexity: O(1)
"""

import time
from typing import Optional


class TokenBucket:
    """
    A simple token bucket rate limiter.
    
    Attributes:
        capacity: Maximum number of tokens the bucket can hold
        refill_rate: Number of tokens added per second
        tokens: Current number of tokens in the bucket
        last_refill: Timestamp of last token refill
    
    Example:
        >>> bucket = TokenBucket(capacity=10, refill_rate=2)
        >>> bucket.consume(5)  # Burst of 5 allowed
        True
        >>> bucket.consume(6)  # Only 5 tokens left, 6 denied
        False
        >>> time.sleep(2.5)    # Refills 5 tokens
        >>> bucket.consume(5)  # Now allowed
        True
    """
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize the token bucket.
        
        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second to add
        
        Raises:
            ValueError: If capacity <= 0 or refill_rate <= 0
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.time()
    
    @property
    def tokens(self) -> float:
        """Get current token count (triggers refill)."""
        self._refill()
        return self._tokens
    
    def _refill(self) -> None:
        """Add tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self._last_refill
        
        if elapsed > 0:
            new_tokens = elapsed * self.refill_rate
            self._tokens = min(self.capacity, self._tokens + new_tokens)
            self._last_refill = now
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens from the bucket.
        
        Args:
            tokens: Number of tokens to consume (default: 1)
        
        Returns:
            True if tokens were consumed, False if insufficient tokens
        
        Example:
            >>> bucket = TokenBucket(10, 1)
            >>> bucket.consume(5)
            True
            >>> bucket.available()
            5.0
        """
        if tokens <= 0:
            raise ValueError("Token count must be positive")
        
        self._refill()
        
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False
    
    def available(self) -> float:
        """
        Get number of available tokens without consuming.
        
        Returns:
            Current token count
        
        Example:
            >>> bucket = TokenBucket(10, 1)
            >>> bucket.available()
            10.0
        """
        self._refill()
        return self._tokens
    
    def wait_time(self, tokens: int = 1) -> float:
        """
        Calculate time to wait for enough tokens.
        
        Args:
            tokens: Number of tokens needed
        
        Returns:
            Seconds to wait (0 if already available)
        
        Example:
            >>> bucket = TokenBucket(10, 10)  # 10 tokens/sec
            >>> bucket.consume(8)
            True
            >>> bucket.wait_time(5)  # Need 3 more, 0.3 sec
            0.3
        """
        if tokens <= 0:
            return 0.0
        
        self._refill()
        
        if self._tokens >= tokens:
            return 0.0
        
        needed = tokens - self._tokens
        return needed / self.refill_rate
    
    def peek(self) -> float:
        """
        Get token count without triggering refill.
        
        Returns:
            Last known token count (may be stale)
        """
        return self._tokens
    
    def reset(self) -> None:
        """Reset bucket to full capacity."""
        self._tokens = float(self.capacity)
        self._last_refill = time.time()
    
    def __repr__(self) -> str:
        return (
            f"TokenBucket(capacity={self.capacity}, "
            f"refill_rate={self.refill_rate}, tokens={self._tokens:.2f})"
        )