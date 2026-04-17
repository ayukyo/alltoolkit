"""
decorator_utils - Python Decorator Utilities
============================================

A collection of commonly used decorators for Python development.
Zero external dependencies - uses only Python standard library.

Features:
- @timer - Measure execution time
- @retry - Auto-retry on failure with configurable backoff
- @memoize - Cache function results
- @singleton - Ensure only one instance exists
- @deprecated - Mark functions as deprecated
- @validate_types - Runtime type checking
- @rate_limit - Limit function call frequency
- @log_calls - Log function calls with arguments
- @timeout - Timeout for long-running functions
- @count_calls - Count function invocations

Author: AllToolkit
Date: 2026-04-17
"""

import functools
import time
import threading
import warnings
import inspect
from typing import Any, Callable, TypeVar, Optional, Union, Tuple, Dict
from collections import OrderedDict
from datetime import datetime
from contextlib import contextmanager

F = TypeVar('F', bound=Callable[..., Any])


def timer(func: F) -> F:
    """
    Decorator to measure and print function execution time.
    
    Example:
        @timer
        def slow_function():
            time.sleep(1)
            return "done"
        
        # Output: slow_function took 1.00 seconds
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper  # type: ignore


def timer_verbose(include_args: bool = False) -> Callable[[F], F]:
    """
    Decorator factory for timer with options.
    
    Args:
        include_args: Whether to print function arguments
        
    Example:
        @timer_verbose(include_args=True)
        def process(data, count=10):
            return data * count
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            
            if include_args:
                args_str = f", args={args}, kwargs={kwargs}"
            else:
                args_str = ""
            
            print(f"[TIMER] {func.__name__}{args_str} took {end - start:.4f} seconds")
            return result
        return wrapper  # type: ignore
    return decorator


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[type, ...] = (Exception,),
    on_retry: Optional[Callable[[int, Exception], None]] = None
) -> Callable[[F], F]:
    """
    Decorator to retry a function on failure with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exception types to catch
        on_retry: Optional callback called on each retry (attempt, exception)
        
    Example:
        @retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError,))
        def fetch_data():
            # May raise ConnectionError
            return requests.get("https://api.example.com")
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        if on_retry:
                            on_retry(attempt + 1, e)
                        time.sleep(current_delay)
                        current_delay *= backoff
            
            raise last_exception  # type: ignore
        
        return wrapper  # type: ignore
    return decorator


def memoize(
    maxsize: Optional[int] = 128,
    typed: bool = False,
    ttl: Optional[float] = None
) -> Callable[[F], F]:
    """
    Decorator to cache function results with optional TTL.
    
    Args:
        maxsize: Maximum cache size (None = unlimited)
        typed: Cache different types separately (3 vs 3.0)
        ttl: Time-to-live in seconds (None = no expiration)
        
    Example:
        @memoize(maxsize=100, ttl=60)  # Cache for 60 seconds
        def expensive_computation(n):
            return sum(i ** i for i in range(n))
    """
    def decorator(func: F) -> F:
        cache: OrderedDict = OrderedDict()
        cache_lock = threading.Lock()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = args
            if kwargs:
                key = args + tuple(sorted(kwargs.items()))
            
            if typed and args:
                key = key + tuple(type(arg).__name__ for arg in args)
            
            with cache_lock:
                if key in cache:
                    result, timestamp = cache[key]
                    # Check TTL
                    if ttl is None or (time.time() - timestamp) < ttl:
                        # Move to end (most recently used)
                        cache.move_to_end(key)
                        return result
                    else:
                        # Expired, remove from cache
                        del cache[key]
                
                # Compute result
                result = func(*args, **kwargs)
                cache[key] = (result, time.time())
                
                # Enforce maxsize
                if maxsize is not None and len(cache) > maxsize:
                    cache.popitem(last=False)
                
                return result
        
        # Add cache management methods
        wrapper.cache_clear = lambda: cache.clear()  # type: ignore
        wrapper.cache_info = lambda: {"size": len(cache), "maxsize": maxsize}  # type: ignore
        
        return wrapper  # type: ignore
    return decorator


def singleton(cls: type) -> type:
    """
    Class decorator to ensure only one instance exists.
    Thread-safe implementation.
    
    Example:
        @singleton
        class Database:
            def __init__(self):
                self.connection = connect()
        
        db1 = Database()
        db2 = Database()
        assert db1 is db2  # True
    """
    instances: Dict[type, Any] = {}
    lock = threading.Lock()
    
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    wrapper.__instance__ = None  # type: ignore
    
    return wrapper  # type: ignore


def deprecated(
    reason: str = "",
    version: str = "",
    replacement: str = ""
) -> Callable[[F], F]:
    """
    Decorator to mark a function as deprecated.
    
    Args:
        reason: Explanation of deprecation
        version: Version when deprecated
        replacement: Suggested replacement function
        
    Example:
        @deprecated(reason="Use new_function instead", replacement="new_function")
        def old_function():
            pass
    """
    def decorator(func: F) -> F:
        message = f"{func.__name__} is deprecated"
        if version:
            message += f" since version {version}"
        if reason:
            message += f": {reason}"
        if replacement:
            message += f". Use {replacement} instead."
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        
        wrapper.__deprecated__ = True  # type: ignore
        wrapper.__deprecation_message__ = message  # type: ignore
        
        return wrapper  # type: ignore
    return decorator


def validate_types(**type_hints: type) -> Callable[[F], F]:
    """
    Decorator for runtime type checking of function arguments.
    
    Args:
        **type_hints: Argument name to type mapping
        
    Example:
        @validate_types(name=str, age=int, scores=list)
        def create_student(name, age, scores):
            return {"name": name, "age": age, "scores": scores}
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            
            # Validate types
            for arg_name, expected_type in type_hints.items():
                if arg_name in bound.arguments:
                    value = bound.arguments[arg_name]
                    if not isinstance(value, expected_type):
                        actual_type = type(value).__name__
                        expected_name = expected_type.__name__
                        raise TypeError(
                            f"Argument '{arg_name}' must be {expected_name}, "
                            f"got {actual_type}"
                        )
            
            return func(*args, **kwargs)
        
        return wrapper  # type: ignore
    return decorator


def rate_limit(
    calls: int = 10,
    period: float = 1.0,
    raise_on_limit: bool = False
) -> Callable[[F], F]:
    """
    Decorator to limit function call frequency.
    
    Args:
        calls: Maximum number of calls allowed in period
        period: Time period in seconds
        raise_on_limit: If True, raise exception; if False, wait
        
    Example:
        @rate_limit(calls=5, period=1.0)
        def api_call():
            return "response"
    """
    def decorator(func: F) -> F:
        call_times: list = []
        lock = threading.Lock()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                now = time.time()
                
                # Remove old timestamps
                call_times[:] = [t for t in call_times if t > now - period]
                
                # Check rate limit
                if len(call_times) >= calls:
                    if raise_on_limit:
                        raise RuntimeError(
                            f"Rate limit exceeded: {calls} calls per {period} seconds"
                        )
                    else:
                        # Wait until oldest call expires
                        wait_time = call_times[0] + period - now
                        if wait_time > 0:
                            time.sleep(wait_time)
                        call_times[:] = [t for t in call_times if t > time.time() - period]
                
                call_times.append(time.time())
            
            return func(*args, **kwargs)
        
        return wrapper  # type: ignore
    return decorator


def log_calls(
    logger: Optional[Callable[[str], None]] = None,
    include_result: bool = False,
    include_time: bool = True
) -> Callable[[F], F]:
    """
    Decorator to log function calls with arguments.
    
    Args:
        logger: Custom logger function (default: print)
        include_result: Whether to log the return value
        include_time: Whether to include timestamp
        
    Example:
        @log_calls(include_result=True)
        def process(data):
            return data.upper()
        
        # Output: [2026-04-17 09:00:00] CALL process(data='hello')
        #         [2026-04-17 09:00:00] RETURN process -> 'HELLO'
    """
    log_func = logger or print
    
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            time_str = f"{timestamp} " if include_time else ""
            
            # Format arguments
            args_str = ", ".join(repr(a) for a in args)
            kwargs_str = ", ".join(f"{k}={repr(v)}" for k, v in kwargs.items())
            all_args = ", ".join(filter(None, [args_str, kwargs_str]))
            
            log_func(f"{time_str}CALL {func.__name__}({all_args})")
            
            try:
                result = func(*args, **kwargs)
                if include_result:
                    log_func(f"{time_str}RETURN {func.__name__} -> {repr(result)}")
                return result
            except Exception as e:
                log_func(f"{time_str}ERROR {func.__name__} raised {type(e).__name__}: {e}")
                raise
        
        return wrapper  # type: ignore
    return decorator


def timeout(seconds: float) -> Callable[[F], F]:
    """
    Decorator to limit function execution time.
    Note: Only works on Unix-like systems with SIGALRM.
    
    Args:
        seconds: Maximum execution time in seconds
        
    Example:
        @timeout(5.0)
        def slow_operation():
            time.sleep(10)  # Will raise TimeoutError
    """
    import signal
    
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def timeout_handler(signum, frame):
                raise TimeoutError(
                    f"Function {func.__name__} exceeded {seconds} seconds timeout"
                )
            
            # Set signal handler
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.setitimer(signal.ITIMER_REAL, seconds)
            
            try:
                result = func(*args, **kwargs)
            finally:
                # Restore original handler
                signal.setitimer(signal.ITIMER_REAL, 0)
                signal.signal(signal.SIGALRM, old_handler)
            
            return result
        
        return wrapper  # type: ignore
    return decorator


def count_calls(func: F) -> F:
    """
    Decorator to count how many times a function is called.
    
    Example:
        @count_calls
        def my_function():
            return "result"
        
        my_function()
        my_function()
        print(my_function.call_count)  # 2
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1  # type: ignore
        return func(*args, **kwargs)
    
    wrapper.call_count = 0  # type: ignore
    return wrapper  # type: ignore


def once(func: F) -> F:
    """
    Decorator to ensure a function only executes once.
    Subsequent calls return the cached result.
    
    Example:
        @once
        def initialize():
            print("Initializing...")
            return "initialized"
        
        initialize()  # Prints "Initializing..."
        initialize()  # Returns cached "initialized" without printing
    """
    result: Any = None
    executed = False
    lock = threading.Lock()
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal result, executed
        
        if not executed:
            with lock:
                if not executed:
                    result = func(*args, **kwargs)
                    executed = True
        
        return result
    
    return wrapper  # type: ignore


def throttle(
    interval: float = 1.0,
    leading: bool = True,
    trailing: bool = True
) -> Callable[[F], F]:
    """
    Decorator to throttle function calls.
    
    Args:
        interval: Minimum time between calls in seconds
        leading: Execute on the leading edge
        trailing: Execute on the trailing edge
        
    Example:
        @throttle(interval=0.5)
        def handle_scroll(position):
            print(f"Scrolled to {position}")
    """
    def decorator(func: F) -> F:
        last_call: float = 0
        last_result: Any = None
        pending = False
        lock = threading.Lock()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_call, last_result, pending
            
            with lock:
                now = time.time()
                
                if leading and (now - last_call) >= interval:
                    last_call = now
                    last_result = func(*args, **kwargs)
                    return last_result
                
                if trailing and not pending:
                    pending = True
                    wait_time = interval - (now - last_call)
                    
                    def delayed_call():
                        nonlocal last_call, last_result, pending
                        time.sleep(wait_time)
                        with lock:
                            last_call = time.time()
                            last_result = func(*args, **kwargs)
                            pending = False
                    
                    thread = threading.Thread(target=delayed_call, daemon=True)
                    thread.start()
                
                return last_result
        
        return wrapper  # type: ignore
    return decorator


def wrap_exceptions(
    catch: Tuple[type, ...] = (Exception,),
    raise_as: type = RuntimeError,
    message: str = ""
) -> Callable[[F], F]:
    """
    Decorator to wrap exceptions into a different type.
    
    Args:
        catch: Exception types to catch
        raise_as: Exception type to raise instead
        message: Custom message prefix
        
    Example:
        @wrap_exceptions(catch=(ValueError, KeyError), raise_as=CustomError)
        def parse_config(data):
            return data['required_key']
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except catch as e:
                new_message = f"{message}: {e}" if message else str(e)
                raise raise_as(new_message) from e
        
        return wrapper  # type: ignore
    return decorator


def profile(func: F) -> F:
    """
    Decorator to profile function execution with detailed stats.
    
    Example:
        @profile
        def complex_calculation():
            return [i ** 2 for i in range(10000)]
        
        # Output:
        # complex_calculation:
        #   Execution time: 0.0023 seconds
        #   Memory usage: available if tracemalloc enabled
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Timing
        start_time = time.perf_counter()
        
        # Memory tracking (optional)
        try:
            import tracemalloc
            tracemalloc.start()
            result = func(*args, **kwargs)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
        except ImportError:
            result = func(*args, **kwargs)
            current, peak = 0, 0
        
        end_time = time.perf_counter()
        
        # Print profile
        print(f"\n{'='*50}")
        print(f"PROFILE: {func.__name__}")
        print(f"{'='*50}")
        print(f"  Execution time: {end_time - start_time:.6f} seconds")
        if peak > 0:
            print(f"  Peak memory: {peak / 1024:.2f} KB")
        print(f"{'='*50}\n")
        
        return result
    
    return wrapper  # type: ignore


# Context manager for timing code blocks
@contextmanager
def timed_block(name: str = "block"):
    """
    Context manager to time a block of code.
    
    Example:
        with timed_block("data processing"):
            process_large_dataset()
        
        # Output: data processing took 2.34 seconds
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"{name} took {end - start:.4f} seconds")


# Utility function to combine multiple decorators
def combine(*decorators: Callable[[F], F]) -> Callable[[F], F]:
    """
    Combine multiple decorators into one.
    Decorators are applied in reverse order.
    
    Example:
        @combine(timer, retry(max_attempts=3))
        def fetch_data():
            return requests.get(url)
    """
    def combined_decorator(func: F) -> F:
        for decorator in reversed(decorators):
            func = decorator(func)
        return func
    return combined_decorator


# Export all decorators
__all__ = [
    'timer',
    'timer_verbose',
    'retry',
    'memoize',
    'singleton',
    'deprecated',
    'validate_types',
    'rate_limit',
    'log_calls',
    'timeout',
    'count_calls',
    'once',
    'throttle',
    'wrap_exceptions',
    'profile',
    'timed_block',
    'combine',
]