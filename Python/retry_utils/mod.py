"""
AllToolkit - Python Retry Utilities

A zero-dependency, production-ready retry mechanism utility module.
Supports exponential backoff, custom retry conditions, jitter, and comprehensive statistics.

Author: AllToolkit
License: MIT
"""

import time
import random
import threading
from typing import Optional, Any, Callable, TypeVar, Tuple, List, Union, Type
from dataclasses import dataclass, field
from functools import wraps
import sys


T = TypeVar('T')
R = TypeVar('R')


class RetryError(Exception):
    """Exception raised when all retry attempts are exhausted."""
    
    def __init__(self, message: str, last_exception: Optional[Exception] = None, 
                 attempts: int = 0, total_time: float = 0.0):
        super().__init__(message)
        self.last_exception = last_exception
        self.attempts = attempts
        self.total_time = total_time
    
    def __str__(self) -> str:
        base = f"{super().__str__()} (attempts: {self.attempts}, time: {self.total_time:.2f}s)"
        if self.last_exception:
            base += f" - Last error: {type(self.last_exception).__name__}: {self.last_exception}"
        return base


@dataclass
class RetryStats:
    """Statistics for retry operations."""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    total_retries: int = 0
    total_time: float = 0.0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    
    def record_success(self, time_taken: float) -> None:
        """Record a successful call."""
        with self._lock:
            self.total_calls += 1
            self.successful_calls += 1
            self.total_time += time_taken
    
    def record_failure(self, retries: int, time_taken: float) -> None:
        """Record a failed call after all retries."""
        with self._lock:
            self.total_calls += 1
            self.failed_calls += 1
            self.total_retries += retries
            self.total_time += time_taken
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_calls == 0:
            return 0.0
        return self.successful_calls / self.total_calls
    
    @property
    def avg_retries(self) -> float:
        """Calculate average retries per failed call."""
        if self.failed_calls == 0:
            return 0.0
        return self.total_retries / self.failed_calls
    
    @property
    def avg_time(self) -> float:
        """Calculate average time per call."""
        if self.total_calls == 0:
            return 0.0
        return self.total_time / self.total_calls
    
    def to_dict(self) -> dict:
        """Convert stats to dictionary."""
        return {
            'total_calls': self.total_calls,
            'successful_calls': self.successful_calls,
            'failed_calls': self.failed_calls,
            'total_retries': self.total_retries,
            'total_time': self.total_time,
            'success_rate': self.success_rate,
            'avg_retries': self.avg_retries,
            'avg_time': self.avg_time,
        }
    
    def reset(self) -> None:
        """Reset all statistics."""
        with self._lock:
            self.total_calls = 0
            self.successful_calls = 0
            self.failed_calls = 0
            self.total_retries = 0
            self.total_time = 0.0


@dataclass
class RetryAttempt:
    """Information about a single retry attempt."""
    attempt_number: int
    exception: Optional[Exception]
    delay_before: float
    delay_after: float
    timestamp: float = field(default_factory=time.time)


class RetryConfig:
    """Configuration for retry behavior."""
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        jitter_factor: float = 0.1,
        retryable_exceptions: Optional[Union[Type[Exception], Tuple[Type[Exception], ...]]] = None,
        retry_on_result: Optional[Callable[[Any], bool]] = None,
        timeout: Optional[float] = None,
        on_retry: Optional[Callable[[int, Exception, float], None]] = None,
        stats: Optional[RetryStats] = None,
    ):
        """
        Initialize retry configuration.
        
        Args:
            max_retries: Maximum number of retry attempts (default: 3)
            base_delay: Base delay between retries in seconds (default: 1.0)
            max_delay: Maximum delay between retries in seconds (default: 60.0)
            exponential_base: Base for exponential backoff (default: 2.0)
            jitter: Add random jitter to delays (default: True)
            jitter_factor: Jitter factor (0.0-1.0) as fraction of delay (default: 0.1)
            retryable_exceptions: Exception types that trigger retry (default: Exception)
            retry_on_result: Callable that returns True if result should trigger retry
            timeout: Overall timeout in seconds (default: None = no timeout)
            on_retry: Callback called before each retry (attempt, exception, delay)
            stats: Shared stats object for tracking
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.jitter_factor = jitter_factor
        self.retryable_exceptions = retryable_exceptions or Exception
        self.retry_on_result = retry_on_result
        self.timeout = timeout
        self.on_retry = on_retry
        self.stats = stats or RetryStats()
    
    def calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay for given attempt number using exponential backoff.
        
        Args:
            attempt: Attempt number (0-indexed)
        
        Returns:
            Delay in seconds
        """
        # Exponential backoff
        delay = self.base_delay * (self.exponential_base ** attempt)
        
        # Cap at max_delay
        delay = min(delay, self.max_delay)
        
        # Add jitter
        if self.jitter:
            jitter_range = delay * self.jitter_factor
            delay += random.uniform(-jitter_range, jitter_range)
            delay = max(0.0, delay)  # Ensure non-negative
        
        return delay
    
    def is_retryable_exception(self, exception: Exception) -> bool:
        """Check if exception should trigger a retry."""
        return isinstance(exception, self.retryable_exceptions)
    
    def should_retry_result(self, result: Any) -> bool:
        """Check if result should trigger a retry."""
        if self.retry_on_result is None:
            return False
        return self.retry_on_result(result)


class RetryExecutor:
    """Execute functions with retry logic."""
    
    def __init__(self, config: Optional[RetryConfig] = None):
        """
        Initialize retry executor.
        
        Args:
            config: Retry configuration (default: create new config)
        """
        self.config = config or RetryConfig()
        self._attempts: List[RetryAttempt] = []
    
    @property
    def attempts(self) -> List[RetryAttempt]:
        """Get list of retry attempts from last execution."""
        return self._attempts
    
    def execute(
        self,
        func: Callable[..., T],
        *args,
        **kwargs
    ) -> T:
        """
        Execute function with retry logic.
        
        Args:
            func: Function to execute
            *args: Positional arguments for function
            **kwargs: Keyword arguments for function
        
        Returns:
            Function result
        
        Raises:
            RetryError: When all retry attempts are exhausted
        """
        self._attempts = []
        start_time = time.time()
        last_exception: Optional[Exception] = None
        attempt = 0
        
        while True:
            try:
                result = func(*args, **kwargs)
                
                # Check if result should trigger retry
                if self.config.should_retry_result(result):
                    if attempt >= self.config.max_retries:
                        elapsed = time.time() - start_time
                        self.config.stats.record_failure(attempt, elapsed)
                        raise RetryError(
                            "Function returned retryable result",
                            last_exception=last_exception,
                            attempts=attempt + 1,
                            total_time=elapsed
                        )
                    
                    delay = self.config.calculate_delay(attempt)
                    self._record_attempt(attempt, None, delay)
                    
                    if self.config.on_retry:
                        self.config.on_retry(attempt + 1, None, delay)
                    
                    self._sleep(delay, start_time)
                    attempt += 1
                    continue
                
                # Success
                elapsed = time.time() - start_time
                self.config.stats.record_success(elapsed)
                return result
                
            except Exception as e:
                last_exception = e
                
                # Check if exception is retryable
                if not self.config.is_retryable_exception(e):
                    elapsed = time.time() - start_time
                    self.config.stats.record_failure(attempt, elapsed)
                    raise
                
                # Check if we've exhausted retries
                if attempt >= self.config.max_retries:
                    elapsed = time.time() - start_time
                    self.config.stats.record_failure(attempt, elapsed)
                    raise RetryError(
                        f"All {self.config.max_retries + 1} attempts failed",
                        last_exception=e,
                        attempts=attempt + 1,
                        total_time=elapsed
                    )
                
                # Check timeout
                elapsed = time.time() - start_time
                if self.config.timeout and elapsed + self.config.calculate_delay(attempt) > self.config.timeout:
                    self.config.stats.record_failure(attempt, elapsed)
                    raise RetryError(
                        f"Timeout exceeded ({self.config.timeout}s)",
                        last_exception=e,
                        attempts=attempt + 1,
                        total_time=elapsed
                    )
                
                # Calculate delay and retry
                delay = self.config.calculate_delay(attempt)
                self._record_attempt(attempt, e, delay)
                
                if self.config.on_retry:
                    self.config.on_retry(attempt + 1, e, delay)
                
                self._sleep(delay, start_time)
                attempt += 1
    
    def _record_attempt(self, attempt: int, exception: Optional[Exception], delay: float) -> None:
        """Record a retry attempt."""
        self._attempts.append(RetryAttempt(
            attempt_number=attempt + 1,
            exception=exception,
            delay_before=delay,
            delay_after=0.0,
        ))
    
    def _sleep(self, delay: float, start_time: float) -> None:
        """Sleep with timeout check."""
        if delay <= 0:
            return
        
        elapsed = time.time() - start_time
        if self.config.timeout and elapsed + delay > self.config.timeout:
            delay = max(0, self.config.timeout - elapsed)
        
        if delay > 0:
            time.sleep(delay)


def retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    jitter_factor: float = 0.1,
    retryable_exceptions: Optional[Union[Type[Exception], Tuple[Type[Exception], ...]]] = None,
    retry_on_result: Optional[Callable[[Any], bool]] = None,
    timeout: Optional[float] = None,
    on_retry: Optional[Callable[[int, Exception, float], None]] = None,
    stats: Optional[RetryStats] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for adding retry logic to functions.
    
    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        base_delay: Base delay between retries in seconds (default: 1.0)
        max_delay: Maximum delay between retries in seconds (default: 60.0)
        exponential_base: Base for exponential backoff (default: 2.0)
        jitter: Add random jitter to delays (default: True)
        jitter_factor: Jitter factor (0.0-1.0) as fraction of delay (default: 0.1)
        retryable_exceptions: Exception types that trigger retry (default: Exception)
        retry_on_result: Callable that returns True if result should trigger retry
        timeout: Overall timeout in seconds (default: None = no timeout)
        on_retry: Callback called before each retry (attempt, exception, delay)
        stats: Shared stats object for tracking
    
    Returns:
        Decorated function with retry logic
    
    Example:
        @retry(max_retries=3, base_delay=1.0, retryable_exceptions=(ConnectionError, TimeoutError))
        def fetch_data(url):
            response = requests.get(url)
            return response.json()
    """
    config = RetryConfig(
        max_retries=max_retries,
        base_delay=base_delay,
        max_delay=max_delay,
        exponential_base=exponential_base,
        jitter=jitter,
        jitter_factor=jitter_factor,
        retryable_exceptions=retryable_exceptions,
        retry_on_result=retry_on_result,
        timeout=timeout,
        on_retry=on_retry,
        stats=stats,
    )
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            executor = RetryExecutor(config)
            return executor.execute(func, *args, **kwargs)
        return wrapper
    
    return decorator


def retry_with_config(
    func: Callable[..., T],
    config: RetryConfig,
    *args,
    **kwargs
) -> T:
    """
    Execute function with given retry configuration.
    
    Args:
        func: Function to execute
        config: Retry configuration
        *args: Positional arguments for function
        **kwargs: Keyword arguments for function
    
    Returns:
        Function result
    
    Example:
        config = RetryConfig(max_retries=5, base_delay=0.5)
        result = retry_with_config(my_function, config, arg1, arg2)
    """
    executor = RetryExecutor(config)
    return executor.execute(func, *args, **kwargs)


class BackoffStrategies:
    """Predefined backoff strategies."""
    
    @staticmethod
    def constant(delay: float = 1.0) -> RetryConfig:
        """Constant delay between retries."""
        return RetryConfig(
            base_delay=delay,
            exponential_base=1.0,
            jitter=False,
        )
    
    @staticmethod
    def linear(base_delay: float = 1.0, max_delay: float = 60.0) -> RetryConfig:
        """Linear increase in delay."""
        return RetryConfig(
            base_delay=base_delay,
            max_delay=max_delay,
            exponential_base=1.0,
            jitter=False,
        )
    
    @staticmethod
    def exponential(
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
    ) -> RetryConfig:
        """Exponential backoff with optional jitter."""
        return RetryConfig(
            base_delay=base_delay,
            max_delay=max_delay,
            exponential_base=exponential_base,
            jitter=jitter,
        )
    
    @staticmethod
    def fibonacci(max_delay: float = 60.0) -> RetryConfig:
        """Fibonacci sequence backoff."""
        # Approximate fibonacci with exponential
        return RetryConfig(
            base_delay=1.0,
            max_delay=max_delay,
            exponential_base=1.618,  # Golden ratio
            jitter=False,
        )


# Shared stats instance for module-level tracking
_global_stats = RetryStats()


def get_global_stats() -> RetryStats:
    """Get the global retry statistics instance."""
    return _global_stats


def reset_global_stats() -> None:
    """Reset global retry statistics."""
    _global_stats.reset()


# Convenience exceptions for common retry scenarios
class TransientError(Exception):
    """Represents a transient error that should be retried."""
    pass


class NetworkError(TransientError):
    """Represents a network-related transient error."""
    pass


class ServiceUnavailableError(TransientError):
    """Represents a service unavailable error that should be retried."""
    pass


class RateLimitError(TransientError):
    """Represents a rate limit error. Retry after the specified delay."""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: Optional[float] = None):
        super().__init__(message)
        self.retry_after = retry_after


# Convenience retry configurations
RETRY_NETWORK = RetryConfig(
    max_retries=3,
    base_delay=1.0,
    max_delay=30.0,
    retryable_exceptions=(NetworkError, ConnectionError, TimeoutError, OSError),
)

RETRY_DATABASE = RetryConfig(
    max_retries=5,
    base_delay=0.5,
    max_delay=10.0,
    retryable_exceptions=(ConnectionError, TimeoutError),
)

RETRY_API = RetryConfig(
    max_retries=3,
    base_delay=2.0,
    max_delay=60.0,
    retryable_exceptions=(NetworkError, ServiceUnavailableError, RateLimitError),
)

RETRY_QUICK = RetryConfig(
    max_retries=2,
    base_delay=0.1,
    max_delay=1.0,
    jitter=False,
)
