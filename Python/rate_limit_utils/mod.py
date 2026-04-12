"""
AllToolkit - Python Rate Limit Utilities

A zero-dependency, production-ready rate limiting utility module.
Supports token bucket, sliding window, and fixed window rate limiters.
Thread-safe with optional async support.

Author: AllToolkit
License: MIT
"""

import time
import threading
from typing import Optional, Dict, List, Callable, Any, TypeVar, Generic
from dataclasses import dataclass, field
from collections import deque
from functools import wraps
from contextlib import contextmanager
import hashlib


T = TypeVar('T')


@dataclass
class RateLimitResult:
    """Result of a rate limit check."""
    allowed: bool
    remaining: int
    reset_at: float
    retry_after: Optional[float] = None
    limit: int = 0
    window_seconds: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'allowed': self.allowed,
            'remaining': self.remaining,
            'reset_at': self.reset_at,
            'retry_after': self.retry_after,
            'limit': self.limit,
            'window_seconds': self.window_seconds,
        }
    
    def __bool__(self) -> bool:
        return self.allowed


class TokenBucket:
    """
    Token bucket rate limiter.
    
    Tokens are added at a constant rate up to a maximum capacity.
    Each request consumes one token. If no tokens are available,
    the request is rate limited.
    
    Example:
        bucket = TokenBucket(capacity=10, refill_rate=2.0)  # 10 tokens, 2 per second
        if bucket.consume():
            # Request allowed
        else:
            # Rate limited
    """
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket.
        
        Args:
            capacity: Maximum number of tokens in the bucket
            refill_rate: Tokens added per second
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        
        self._capacity = capacity
        self._refill_rate = refill_rate
        self._tokens = float(capacity)
        self._last_refill = time.time()
        self._lock = threading.Lock()
    
    @property
    def capacity(self) -> int:
        """Get bucket capacity."""
        return self._capacity
    
    @property
    def refill_rate(self) -> float:
        """Get refill rate (tokens per second)."""
        return self._refill_rate
    
    @property
    def tokens(self) -> float:
        """Get current token count (after refill)."""
        with self._lock:
            self._refill()
            return self._tokens
    
    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self._last_refill
        tokens_to_add = elapsed * self._refill_rate
        self._tokens = min(self._capacity, self._tokens + tokens_to_add)
        self._last_refill = now
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens.
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            True if tokens were consumed, False if rate limited
        """
        if tokens <= 0:
            raise ValueError("Tokens to consume must be positive")
        
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False
    
    def wait_time(self, tokens: int = 1) -> float:
        """
        Calculate wait time until tokens are available.
        
        Args:
            tokens: Number of tokens needed
            
        Returns:
            Seconds to wait (0 if tokens available now)
        """
        if tokens <= 0:
            raise ValueError("Tokens must be positive")
        
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                return 0.0
            tokens_needed = tokens - self._tokens
            return tokens_needed / self._refill_rate
    
    def reset(self) -> None:
        """Reset bucket to full capacity."""
        with self._lock:
            self._tokens = float(self._capacity)
            self._last_refill = time.time()
    
    def check(self, tokens: int = 1) -> RateLimitResult:
        """
        Check rate limit status without consuming tokens.
        
        Args:
            tokens: Number of tokens to check
            
        Returns:
            RateLimitResult with status information
        """
        with self._lock:
            self._refill()
            allowed = self._tokens >= tokens
            remaining = max(0, int(self._tokens))
            retry_after = self.wait_time(tokens) if not allowed else 0.0
            
            # Calculate reset time (when bucket will be full)
            tokens_to_full = self._capacity - self._tokens
            reset_at = time.time() + (tokens_to_full / self._refill_rate) if tokens_to_full > 0 else time.time()
            
            return RateLimitResult(
                allowed=allowed,
                remaining=remaining,
                reset_at=reset_at,
                retry_after=retry_after if not allowed else None,
                limit=self._capacity,
                window_seconds=self._capacity / self._refill_rate,
            )


class SlidingWindowCounter:
    """
    Sliding window rate limiter using counter approximation.
    
    Combines benefits of fixed window (low memory) and sliding window
    (smooth rate limiting). Uses two overlapping windows for accuracy.
    
    Example:
        limiter = SlidingWindowCounter(max_requests=100, window_seconds=60)
        if limiter.allow():
            # Request allowed
        else:
            # Rate limited
    """
    
    def __init__(self, max_requests: int, window_seconds: float):
        """
        Initialize sliding window counter.
        
        Args:
            max_requests: Maximum requests allowed per window
            window_seconds: Window duration in seconds
        """
        if max_requests <= 0:
            raise ValueError("Max requests must be positive")
        if window_seconds <= 0:
            raise ValueError("Window seconds must be positive")
        
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._prev_count = 0
        self._curr_count = 0
        self._prev_window_start = time.time()
        self._lock = threading.Lock()
    
    @property
    def max_requests(self) -> int:
        """Get maximum requests per window."""
        return self._max_requests
    
    @property
    def window_seconds(self) -> float:
        """Get window duration in seconds."""
        return self._window_seconds
    
    def _update_windows(self) -> None:
        """Update window counters based on current time."""
        now = time.time()
        window_start = now - (now % self._window_seconds)
        
        if window_start > self._prev_window_start:
            windows_passed = int((window_start - self._prev_window_start) / self._window_seconds)
            
            if windows_passed == 1:
                self._prev_count = self._curr_count
                self._curr_count = 0
            elif windows_passed > 1:
                self._prev_count = 0
                self._curr_count = 0
            
            self._prev_window_start = window_start
    
    def _get_count(self) -> float:
        """Get weighted count using sliding window approximation."""
        now = time.time()
        window_start = now - (now % self._window_seconds)
        window_position = (now - window_start) / self._window_seconds
        
        prev_weight = 1.0 - window_position
        return (self._prev_count * prev_weight) + self._curr_count
    
    def allow(self) -> bool:
        """
        Check if request is allowed and record it if so.
        
        Returns:
            True if allowed, False if rate limited
        """
        with self._lock:
            self._update_windows()
            
            if self._get_count() >= self._max_requests:
                return False
            
            self._curr_count += 1
            return True
    
    def check(self) -> RateLimitResult:
        """
        Check rate limit status without recording a request.
        
        Returns:
            RateLimitResult with status information
        """
        with self._lock:
            self._update_windows()
            
            current_count = self._get_count()
            remaining = max(0, int(self._max_requests - current_count))
            allowed = remaining > 0
            
            # Calculate reset time (end of current window)
            now = time.time()
            window_end = (now // self._window_seconds + 1) * self._window_seconds
            
            retry_after = None
            if not allowed:
                retry_after = self._window_seconds * (1.0 - (now % self._window_seconds) / self._window_seconds)
            
            return RateLimitResult(
                allowed=allowed,
                remaining=remaining,
                reset_at=window_end,
                retry_after=retry_after,
                limit=self._max_requests,
                window_seconds=self._window_seconds,
            )
    
    def reset(self) -> None:
        """Reset all counters."""
        with self._lock:
            self._prev_count = 0
            self._curr_count = 0
            self._prev_window_start = time.time()


class SlidingWindowLog:
    """
    Precise sliding window rate limiter using timestamp log.
    
    Maintains a log of request timestamps for accurate rate limiting.
    More memory-intensive but provides exact rate limiting.
    
    Example:
        limiter = SlidingWindowLog(max_requests=100, window_seconds=60)
        if limiter.allow():
            # Request allowed
    """
    
    def __init__(self, max_requests: int, window_seconds: float):
        """
        Initialize sliding window log.
        
        Args:
            max_requests: Maximum requests allowed per window
            window_seconds: Window duration in seconds
        """
        if max_requests <= 0:
            raise ValueError("Max requests must be positive")
        if window_seconds <= 0:
            raise ValueError("Window seconds must be positive")
        
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._timestamps: deque = deque()
        self._lock = threading.Lock()
    
    @property
    def max_requests(self) -> int:
        """Get maximum requests per window."""
        return self._max_requests
    
    @property
    def window_seconds(self) -> float:
        """Get window duration in seconds."""
        return self._window_seconds
    
    def _cleanup(self) -> None:
        """Remove expired timestamps."""
        now = time.time()
        cutoff = now - self._window_seconds
        
        while self._timestamps and self._timestamps[0] < cutoff:
            self._timestamps.popleft()
    
    def allow(self) -> bool:
        """
        Check if request is allowed and record it if so.
        
        Returns:
            True if allowed, False if rate limited
        """
        with self._lock:
            self._cleanup()
            
            if len(self._timestamps) >= self._max_requests:
                return False
            
            self._timestamps.append(time.time())
            return True
    
    def check(self) -> RateLimitResult:
        """
        Check rate limit status without recording a request.
        
        Returns:
            RateLimitResult with status information
        """
        with self._lock:
            self._cleanup()
            
            remaining = max(0, self._max_requests - len(self._timestamps))
            allowed = remaining > 0
            
            now = time.time()
            retry_after = None
            reset_at = now + self._window_seconds
            
            if not allowed and self._timestamps:
                oldest = self._timestamps[0]
                retry_after = (oldest + self._window_seconds) - now
                reset_at = oldest + self._window_seconds
            
            return RateLimitResult(
                allowed=allowed,
                remaining=remaining,
                reset_at=reset_at,
                retry_after=retry_after,
                limit=self._max_requests,
                window_seconds=self._window_seconds,
            )
    
    def reset(self) -> None:
        """Clear all timestamps."""
        with self._lock:
            self._timestamps.clear()
    
    @property
    def count(self) -> int:
        """Get current request count in window."""
        with self._lock:
            self._cleanup()
            return len(self._timestamps)


class FixedWindowCounter:
    """
    Simple fixed window rate limiter.
    
    Counts requests within fixed time windows. Simple but can allow
    bursts at window boundaries.
    
    Example:
        limiter = FixedWindowCounter(max_requests=100, window_seconds=60)
        if limiter.allow():
            # Request allowed
    """
    
    def __init__(self, max_requests: int, window_seconds: float):
        """
        Initialize fixed window counter.
        
        Args:
            max_requests: Maximum requests allowed per window
            window_seconds: Window duration in seconds
        """
        if max_requests <= 0:
            raise ValueError("Max requests must be positive")
        if window_seconds <= 0:
            raise ValueError("Window seconds must be positive")
        
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._count = 0
        self._window_start = time.time()
        self._lock = threading.Lock()
    
    @property
    def max_requests(self) -> int:
        """Get maximum requests per window."""
        return self._max_requests
    
    @property
    def window_seconds(self) -> float:
        """Get window duration in seconds."""
        return self._window_seconds
    
    def _check_window(self) -> None:
        """Reset counter if window has expired."""
        now = time.time()
        if now - self._window_start >= self._window_seconds:
            self._count = 0
            self._window_start = now
    
    def allow(self) -> bool:
        """
        Check if request is allowed and record it if so.
        
        Returns:
            True if allowed, False if rate limited
        """
        with self._lock:
            self._check_window()
            
            if self._count >= self._max_requests:
                return False
            
            self._count += 1
            return True
    
    def check(self) -> RateLimitResult:
        """
        Check rate limit status without recording a request.
        
        Returns:
            RateLimitResult with status information
        """
        with self._lock:
            self._check_window()
            
            remaining = max(0, self._max_requests - self._count)
            allowed = remaining > 0
            
            reset_at = self._window_start + self._window_seconds
            retry_after = None
            if not allowed:
                retry_after = reset_at - time.time()
            
            return RateLimitResult(
                allowed=allowed,
                remaining=remaining,
                reset_at=reset_at,
                retry_after=retry_after,
                limit=self._max_requests,
                window_seconds=self._window_seconds,
            )
    
    def reset(self) -> None:
        """Reset counter and window."""
        with self._lock:
            self._count = 0
            self._window_start = time.time()


class RateLimiter:
    """
    Multi-key rate limiter supporting multiple rate limit strategies.
    
    Allows rate limiting by different keys (e.g., user ID, IP address, API key).
    Each key gets its own independent rate limit.
    
    Example:
        limiter = RateLimiter(strategy='token_bucket', capacity=10, refill_rate=1.0)
        if limiter.allow('user_123'):
            # Request for user_123 allowed
    """
    
    def __init__(
        self,
        strategy: str = 'token_bucket',
        max_requests: int = 100,
        window_seconds: float = 60.0,
        capacity: int = 10,
        refill_rate: float = 1.0,
        cleanup_interval: float = 300.0,
    ):
        """
        Initialize multi-key rate limiter.
        
        Args:
            strategy: Rate limiting strategy ('token_bucket', 'sliding_window', 
                     'sliding_window_log', 'fixed_window')
            max_requests: Max requests per window (for window-based strategies)
            window_seconds: Window duration in seconds
            capacity: Bucket capacity (for token bucket)
            refill_rate: Token refill rate per second (for token bucket). 
                        Use a small positive value like 0.001 for near-zero refill.
            cleanup_interval: Seconds between cleanup of stale keys
        """
        """
        Initialize multi-key rate limiter.
        
        Args:
            strategy: Rate limiting strategy ('token_bucket', 'sliding_window', 
                     'sliding_window_log', 'fixed_window')
            max_requests: Max requests per window (for window-based strategies)
            window_seconds: Window duration in seconds
            capacity: Bucket capacity (for token bucket)
            refill_rate: Token refill rate per second (for token bucket)
            cleanup_interval: Seconds between cleanup of stale keys
        """
        self._strategy = strategy
        self._limiters: Dict[str, Any] = {}
        self._params = {
            'max_requests': max_requests,
            'window_seconds': window_seconds,
            'capacity': capacity,
            'refill_rate': refill_rate,
        }
        self._lock = threading.Lock()
        self._last_cleanup = time.time()
        self._cleanup_interval = cleanup_interval
        self._key_times: Dict[str, float] = {}
    
    def _create_limiter(self) -> Any:
        """Create a new rate limiter instance based on strategy."""
        if self._strategy == 'token_bucket':
            # Ensure refill_rate is positive (use small value for near-zero)
            refill_rate = max(0.001, self._params['refill_rate'])
            return TokenBucket(
                capacity=self._params['capacity'],
                refill_rate=refill_rate,
            )
        elif self._strategy == 'sliding_window':
            return SlidingWindowCounter(
                max_requests=self._params['max_requests'],
                window_seconds=self._params['window_seconds'],
            )
        elif self._strategy == 'sliding_window_log':
            return SlidingWindowLog(
                max_requests=self._params['max_requests'],
                window_seconds=self._params['window_seconds'],
            )
        elif self._strategy == 'fixed_window':
            return FixedWindowCounter(
                max_requests=self._params['max_requests'],
                window_seconds=self._params['window_seconds'],
            )
        else:
            raise ValueError(f"Unknown strategy: {self._strategy}")
    
    def _maybe_cleanup(self) -> None:
        """Cleanup stale keys if enough time has passed."""
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
                del self._limiters[key]
                del self._key_times[key]
            self._last_cleanup = now
    
    def allow(self, key: str) -> bool:
        """
        Check if request is allowed for the given key.
        
        Args:
            key: Unique identifier (e.g., user ID, IP address)
            
        Returns:
            True if allowed, False if rate limited
        """
        self._maybe_cleanup()
        
        with self._lock:
            if key not in self._limiters:
                self._limiters[key] = self._create_limiter()
            
            self._key_times[key] = time.time()
            limiter = self._limiters[key]
        
        # TokenBucket uses consume(), others use allow()
        if self._strategy == 'token_bucket':
            return limiter.consume()
        return limiter.allow()
    
    def check(self, key: str) -> RateLimitResult:
        """
        Check rate limit status for a key without consuming.
        
        Args:
            key: Unique identifier
            
        Returns:
            RateLimitResult with status information
        """
        self._maybe_cleanup()
        
        with self._lock:
            if key not in self._limiters:
                self._limiters[key] = self._create_limiter()
            
            self._key_times[key] = time.time()
            limiter = self._limiters[key]
        
        return limiter.check()
    
    def reset(self, key: str) -> None:
        """
        Reset rate limit for a specific key.
        
        Args:
            key: Unique identifier
        """
        with self._lock:
            if key in self._limiters:
                self._limiters[key].reset()
    
    def reset_all(self) -> None:
        """Reset all rate limits."""
        with self._lock:
            self._limiters.clear()
            self._key_times.clear()


def rate_limit(
    max_requests: int = 100,
    window_seconds: float = 60.0,
    key_func: Optional[Callable[..., str]] = None,
    strategy: str = 'sliding_window',
    on_limit: Optional[Callable[..., Any]] = None,
):
    """
    Decorator for rate limiting functions.
    
    Args:
        max_requests: Maximum requests allowed per window
        window_seconds: Window duration in seconds
        key_func: Function to extract rate limit key from arguments.
                  Default uses function name.
        strategy: Rate limiting strategy
        on_limit: Callback function when rate limited (receives same args)
    
    Example:
        @rate_limit(max_requests=10, window_seconds=60)
        def api_call(user_id: str):
            # This function is rate limited to 10 calls per minute
            pass
        
        @rate_limit(
            max_requests=100,
            window_seconds=60,
            key_func=lambda *args, **kwargs: kwargs.get('user_id', 'default')
        )
        def user_action(user_id: str, action: str):
            # Rate limited per user
            pass
    """
    limiter = RateLimiter(
        strategy=strategy,
        max_requests=max_requests,
        window_seconds=window_seconds,
    )
    
    def decorator(func: Callable[..., T]) -> Callable[..., Optional[T]]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Optional[T]:
            if key_func is not None:
                key = key_func(*args, **kwargs)
            else:
                key = func.__name__
            
            if not limiter.allow(key):
                if on_limit is not None:
                    return on_limit(*args, **kwargs)
                return None
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


@contextmanager
def rate_limit_context(
    limiter: Any,
    key: str,
    on_limit: Optional[Callable[[], Any]] = None,
):
    """
    Context manager for rate limiting code blocks.
    
    Args:
        limiter: Rate limiter instance
        key: Rate limit key
        on_limit: Callback when rate limited
    
    Example:
        limiter = RateLimiter()
        with rate_limit_context(limiter, 'user_123'):
            # Rate limited code
            pass
    """
    if limiter.allow(key):
        yield
    else:
        if on_limit is not None:
            on_limit()


def generate_rate_limit_key(*args: Any, **kwargs: Any) -> str:
    """
    Generate a rate limit key from arguments.
    
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


class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded."""
    
    def __init__(self, result: RateLimitResult, message: str = "Rate limit exceeded"):
        super().__init__(message)
        self.result = result
        self.retry_after = result.retry_after
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception info to dictionary."""
        return {
            'message': str(self),
            'retry_after': self.retry_after,
            'limit_info': self.result.to_dict(),
        }


def rate_limit_strict(
    max_requests: int = 100,
    window_seconds: float = 60.0,
    key_func: Optional[Callable[..., str]] = None,
    strategy: str = 'sliding_window',
):
    """
    Strict rate limit decorator that raises exception when limited.
    
    Args:
        max_requests: Maximum requests allowed per window
        window_seconds: Window duration in seconds
        key_func: Function to extract rate limit key from arguments
        strategy: Rate limiting strategy
    
    Example:
        @rate_limit_strict(max_requests=10, window_seconds=60)
        def api_call(user_id: str):
            # Raises RateLimitExceeded when limited
            pass
    """
    limiter = RateLimiter(
        strategy=strategy,
        max_requests=max_requests,
        window_seconds=window_seconds,
    )
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            if key_func is not None:
                key = key_func(*args, **kwargs)
            else:
                key = func.__name__
            
            result = limiter.check(key)
            if not result.allowed:
                raise RateLimitExceeded(result)
            
            limiter.allow(key)
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator
