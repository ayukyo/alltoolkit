#!/usr/bin/env python3
"""
AllToolkit - Retry Utils Basic Usage Examples

Demonstrates fundamental retry patterns and configurations.
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    retry,
    RetryConfig,
    RetryExecutor,
    retry_with_config,
    BackoffStrategies,
    NetworkError,
    ServiceUnavailableError,
    RateLimitError,
)


def example_1_basic_decorator():
    """Example 1: Basic retry decorator."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Retry Decorator")
    print("=" * 60)
    
    call_count = 0
    
    @retry(max_retries=3, base_delay=0.5)
    def unstable_api():
        nonlocal call_count
        call_count += 1
        print(f"  Attempt {call_count}...")
        
        if call_count < 3:
            raise NetworkError("Connection timeout")
        
        return "Success! Data retrieved."
    
    try:
        result = unstable_api()
        print(f"  Result: {result}")
        print(f"  Total attempts: {call_count}")
    except Exception as e:
        print(f"  Failed: {e}")


def example_2_custom_exceptions():
    """Example 2: Retry only specific exceptions."""
    print("\n" + "=" * 60)
    print("Example 2: Custom Exception Filtering")
    print("=" * 60)
    
    call_count = 0
    
    @retry(
        max_retries=3,
        base_delay=0.3,
        retryable_exceptions=(NetworkError, TimeoutError, ConnectionError)
    )
    def fetch_data():
        nonlocal call_count
        call_count += 1
        print(f"  Attempt {call_count}...")
        
        if call_count == 1:
            raise NetworkError("Network error - will retry")
        if call_count == 2:
            raise ValueError("Invalid data - will NOT retry")
        
        return "Data fetched"
    
    try:
        result = fetch_data()
        print(f"  Result: {result}")
    except ValueError as e:
        print(f"  ValueError (not retried): {e}")
    except Exception as e:
        print(f"  Other error: {e}")


def example_3_retry_on_result():
    """Example 3: Retry based on return value."""
    print("\n" + "=" * 60)
    print("Example 3: Retry on Result Value")
    print("=" * 60)
    
    call_count = 0
    
    @retry(
        max_retries=5,
        base_delay=0.2,
        retry_on_result=lambda x: x is None or x == ""
    )
    def get_user_data(user_id):
        nonlocal call_count
        call_count += 1
        print(f"  Attempt {call_count} for user {user_id}...")
        
        # Simulate eventual consistency
        if call_count < 3:
            return None  # Data not ready yet
        
        return {"id": user_id, "name": "Alice"}
    
    result = get_user_data(123)
    print(f"  Result: {result}")
    print(f"  Total attempts: {call_count}")


def example_4_exponential_backoff():
    """Example 4: Exponential backoff with jitter."""
    print("\n" + "=" * 60)
    print("Example 4: Exponential Backoff with Jitter")
    print("=" * 60)
    
    config = BackoffStrategies.exponential(
        base_delay=0.5,
        max_delay=10.0,
        jitter=True,
    )
    
    call_count = 0
    delays = []
    
    def on_retry(attempt, exception, delay):
        delays.append(delay)
        print(f"  Retry {attempt}: waiting {delay:.3f}s (exception: {type(exception).__name__})")
    
    config.on_retry = on_retry
    
    def rate_limited_call():
        nonlocal call_count
        call_count += 1
        print(f"  Attempt {call_count}...")
        
        if call_count < 4:
            raise RateLimitError("Rate limited", retry_after=1.0)
        
        return "Rate limit cleared!"
    
    executor = RetryExecutor(config)
    
    try:
        result = executor.execute(rate_limited_call)
        print(f"  Result: {result}")
        print(f"  Delays used: {[f'{d:.3f}s' for d in delays]}")
    except Exception as e:
        print(f"  Failed: {e}")


def example_5_timeout():
    """Example 5: Timeout enforcement."""
    print("\n" + "=" * 60)
    print("Example 5: Timeout Enforcement")
    print("=" * 60)
    
    config = RetryConfig(
        max_retries=10,
        base_delay=1.0,
        timeout=2.0,  # Overall timeout of 2 seconds
    )
    
    def slow_failing_service():
        print("  Attempt...")
        time.sleep(0.3)  # Simulate slow operation
        raise ConnectionError("Service unavailable")
    
    executor = RetryExecutor(config)
    
    start = time.time()
    try:
        executor.execute(slow_failing_service)
    except Exception as e:
        elapsed = time.time() - start
        print(f"  Failed after {elapsed:.2f}s: {e}")
        print(f"  Timeout worked: {elapsed < 5.0}")


def example_6_statistics():
    """Example 6: Tracking retry statistics."""
    print("\n" + "=" * 60)
    print("Example 6: Retry Statistics")
    print("=" * 60)
    
    from mod import RetryStats
    
    stats = RetryStats()
    config = RetryConfig(
        max_retries=2,
        base_delay=0.1,
        stats=stats,
    )
    
    def sometimes_fails(fail_probability):
        import random
        if random.random() < fail_probability:
            raise NetworkError("Random failure")
        return "Success"
    
    executor = RetryExecutor(config)
    
    # Simulate multiple calls
    print("  Running 10 simulated API calls...")
    for i in range(10):
        try:
            # 50% failure rate
            executor.execute(sometimes_fails, 0.5)
        except Exception:
            pass
    
    # Print statistics
    print(f"\n  Statistics:")
    print(f"    Total calls: {stats.total_calls}")
    print(f"    Successful: {stats.successful_calls}")
    print(f"    Failed: {stats.failed_calls}")
    print(f"    Total retries: {stats.total_retries}")
    print(f"    Success rate: {stats.success_rate:.1%}")
    print(f"    Avg retries per failure: {stats.avg_retries:.2f}")


def example_7_callback():
    """Example 7: Retry callbacks for logging/monitoring."""
    print("\n" + "=" * 60)
    print("Example 7: Retry Callbacks")
    print("=" * 60)
    
    retry_log = []
    
    def on_retry(attempt, exception, delay):
        retry_log.append({
            'attempt': attempt,
            'exception': str(exception),
            'delay': delay,
            'time': time.time(),
        })
        print(f"  [Callback] Retry {attempt}: {type(exception).__name__} - {exception}")
    
    config = RetryConfig(
        max_retries=3,
        base_delay=0.2,
        on_retry=on_retry,
    )
    
    call_count = 0
    
    def flaky_service():
        nonlocal call_count
        call_count += 1
        
        if call_count < 3:
            raise ServiceUnavailableError(f"Service busy (attempt {call_count})")
        
        return "Service available!"
    
    executor = RetryExecutor(config)
    result = executor.execute(flaky_service)
    
    print(f"\n  Final result: {result}")
    print(f"  Retry log entries: {len(retry_log)}")
    for entry in retry_log:
        print(f"    - Attempt {entry['attempt']}: {entry['exception']}")


def example_8_executor_pattern():
    """Example 8: Executor pattern for reuse."""
    print("\n" + "=" * 60)
    print("Example 8: Executor Pattern")
    print("=" * 60)
    
    # Create a reusable executor with specific config
    api_executor = RetryExecutor(RetryConfig(
        max_retries=3,
        base_delay=0.5,
        max_delay=30.0,
        retryable_exceptions=(NetworkError, ConnectionError, TimeoutError),
    ))
    
    call_counts = {'api1': 0, 'api2': 0}
    
    def api_endpoint_1():
        call_counts['api1'] += 1
        if call_counts['api1'] < 2:
            raise ConnectionError("Connection refused")
        return "API 1 response"
    
    def api_endpoint_2():
        call_counts['api2'] += 1
        return "API 2 response"  # Always succeeds
    
    # Execute multiple functions with same retry policy
    result1 = api_executor.execute(api_endpoint_1)
    result2 = api_executor.execute(api_endpoint_2)
    
    print(f"  API 1 result: {result1} (attempts: {call_counts['api1']})")
    print(f"  API 2 result: {result2} (attempts: {call_counts['api2']})")
    print(f"  Total attempts tracked: {len(api_executor.attempts)}")


def example_9_predefined_configs():
    """Example 9: Using predefined configurations."""
    print("\n" + "=" * 60)
    print("Example 9: Predefined Configurations")
    print("=" * 60)
    
    from mod import RETRY_NETWORK, RETRY_DATABASE, RETRY_API, RETRY_QUICK
    
    configs = [
        ("RETRY_NETWORK", RETRY_NETWORK),
        ("RETRY_DATABASE", RETRY_DATABASE),
        ("RETRY_API", RETRY_API),
        ("RETRY_QUICK", RETRY_QUICK),
    ]
    
    for name, config in configs:
        print(f"\n  {name}:")
        print(f"    Max retries: {config.max_retries}")
        print(f"    Base delay: {config.base_delay}s")
        print(f"    Max delay: {config.max_delay}s")
        print(f"    Jitter: {config.jitter}")
        if config.retryable_exceptions:
            print(f"    Retryable exceptions: {config.retryable_exceptions}")


def example_10_retry_with_config():
    """Example 10: Using retry_with_config function."""
    print("\n" + "=" * 60)
    print("Example 10: retry_with_config Function")
    print("=" * 60)
    
    config = RetryConfig(
        max_retries=2,
        base_delay=0.3,
        jitter=False,
    )
    
    call_count = 0
    
    def my_function():
        nonlocal call_count
        call_count += 1
        print(f"  Attempt {call_count}...")
        
        if call_count < 2:
            raise ValueError("Temporary error")
        
        return "Success!"
    
    # Use retry_with_config for one-off retry
    result = retry_with_config(my_function, config)
    print(f"  Result: {result}")
    print(f"  Total attempts: {call_count}")


def main():
    """Run all examples."""
    print("\n" + "🔄" * 30)
    print("AllToolkit - Python Retry Utils Examples")
    print("🔄" * 30)
    
    example_1_basic_decorator()
    example_2_custom_exceptions()
    example_3_retry_on_result()
    example_4_exponential_backoff()
    example_5_timeout()
    example_6_statistics()
    example_7_callback()
    example_8_executor_pattern()
    example_9_predefined_configs()
    example_10_retry_with_config()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
