"""
Decorator Utils - Usage Examples
=================================

This file demonstrates practical usage of all decorators in the module.
"""

import time
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from decorator_utils.mod import (
    timer, timer_verbose, retry, memoize, singleton,
    deprecated, validate_types, rate_limit, log_calls,
    timeout, count_calls, once, throttle, wrap_exceptions,
    profile, timed_block, combine
)


def example_timer():
    """Example: Using @timer to measure execution time"""
    print("\n" + "="*60)
    print("Example: @timer decorator")
    print("="*60)
    
    @timer
    def slow_computation(n):
        """Compute sum of squares up to n"""
        return sum(i ** 2 for i in range(n))
    
    result = slow_computation(100000)
    print(f"Result: {result}")


def example_timer_verbose():
    """Example: Using @timer_verbose with detailed output"""
    print("\n" + "="*60)
    print("Example: @timer_verbose decorator")
    print("="*60)
    
    @timer_verbose(include_args=True)
    def process_data(data, multiplier=2):
        time.sleep(0.1)
        return [x * multiplier for x in data]
    
    result = process_data([1, 2, 3, 4, 5], multiplier=3)
    print(f"Result: {result}")


def example_retry():
    """Example: Using @retry for resilient API calls"""
    print("\n" + "="*60)
    print("Example: @retry decorator")
    print("="*60)
    
    attempts = 0
    
    @retry(max_attempts=3, delay=0.1, backoff=2.0, exceptions=(ConnectionError,))
    def fetch_data():
        nonlocal attempts
        attempts += 1
        print(f"  Attempt {attempts}...")
        
        # Simulate intermittent failure
        if attempts < 3:
            raise ConnectionError("Network error")
        
        return {"status": "success", "data": [1, 2, 3]}
    
    try:
        result = fetch_data()
        print(f"  Final result: {result}")
    except ConnectionError as e:
        print(f"  Failed after retries: {e}")


def example_memoize():
    """Example: Using @memoize for caching expensive computations"""
    print("\n" + "="*60)
    print("Example: @memoize decorator")
    print("="*60)
    
    call_count = 0
    
    @memoize(maxsize=100, ttl=60)
    def fibonacci(n):
        nonlocal call_count
        call_count += 1
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    print("  Computing fib(30)...")
    result = fibonacci(30)
    print(f"  Result: {result}")
    print(f"  Function calls: {call_count}")
    
    # Clear cache and recalculate
    fibonacci.cache_clear()
    call_count = 0
    print("\n  After cache clear, computing fib(30) again...")
    result = fibonacci(30)
    print(f"  Result: {result}")
    print(f"  Function calls: {call_count}")


def example_singleton():
    """Example: Using @singleton for single instance classes"""
    print("\n" + "="*60)
    print("Example: @singleton decorator")
    print("="*60)
    
    @singleton
    class DatabaseConnection:
        def __init__(self):
            print("  Initializing database connection...")
            self.host = "localhost"
            self.port = 5432
            self.connected = True
        
        def query(self, sql):
            return f"Result of: {sql}"
    
    # Create multiple "instances"
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"  db1 is db2: {db1 is db2}")
    print(f"  db1.query('SELECT *'): {db1.query('SELECT *')}")


def example_deprecated():
    """Example: Using @deprecated to mark old functions"""
    print("\n" + "="*60)
    print("Example: @deprecated decorator")
    print("="*60)
    
    @deprecated(reason="Use new_api_call instead", replacement="new_api_call", version="2.0.0")
    def old_api_call(endpoint):
        return f"Calling {endpoint}"
    
    import warnings
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        result = old_api_call("/users")
        print(f"  Result: {result}")


def example_validate_types():
    """Example: Using @validate_types for runtime type checking"""
    print("\n" + "="*60)
    print("Example: @validate_types decorator")
    print("="*60)
    
    @validate_types(name=str, age=int, scores=list)
    def create_student(name, age, scores):
        return {
            "name": name,
            "age": age,
            "scores": scores,
            "average": sum(scores) / len(scores) if scores else 0
        }
    
    # Valid call
    student = create_student("Alice", 20, [85, 90, 92])
    print(f"  Valid call: {student}")
    
    # Invalid call
    try:
        create_student("Bob", "twenty", [80, 85])
    except TypeError as e:
        print(f"  Type error caught: {e}")


def example_rate_limit():
    """Example: Using @rate_limit for API throttling"""
    print("\n" + "="*60)
    print("Example: @rate_limit decorator")
    print("="*60)
    
    @rate_limit(calls=3, period=1.0, raise_on_limit=True)
    def api_request(endpoint):
        return f"Response from {endpoint}"
    
    print("  Making 5 requests with rate limit of 3/second:")
    for i in range(5):
        try:
            result = api_request(f"/api/data/{i}")
            print(f"  Request {i+1}: {result}")
        except RuntimeError as e:
            print(f"  Request {i+1}: Rate limited - {e}")


def example_log_calls():
    """Example: Using @log_calls for debugging"""
    print("\n" + "="*60)
    print("Example: @log_calls decorator")
    print("="*60)
    
    logs = []
    
    def custom_logger(msg):
        logs.append(msg)
        print(f"  [LOG] {msg}")
    
    @log_calls(logger=custom_logger, include_result=True, include_time=False)
    def process_order(order_id, items, priority="normal"):
        total = sum(item["price"] * item["qty"] for item in items)
        return {"order_id": order_id, "total": total}
    
    result = process_order(
        "ORD-123",
        [{"name": "Widget", "price": 10, "qty": 2}, {"name": "Gadget", "price": 25, "qty": 1}],
        priority="high"
    )
    print(f"  Result: {result}")


def example_timeout():
    """Example: Using @timeout for long-running operations"""
    print("\n" + "="*60)
    print("Example: @timeout decorator")
    print("="*60)
    
    @timeout(0.5)
    def quick_operation():
        time.sleep(0.1)
        return "Done quickly"
    
    @timeout(0.2)
    def slow_operation():
        time.sleep(1.0)
        return "Done slowly"
    
    print("  Running quick_operation (timeout: 0.5s, actual: 0.1s):")
    result = quick_operation()
    print(f"  Result: {result}")
    
    print("\n  Running slow_operation (timeout: 0.2s, actual: 1.0s):")
    try:
        result = slow_operation()
    except TimeoutError as e:
        print(f"  Timeout caught: {e}")


def example_count_calls():
    """Example: Using @count_calls for metrics"""
    print("\n" + "="*60)
    print("Example: @count_calls decorator")
    print("="*60)
    
    @count_calls
    def handle_request(user_id):
        return f"Handling request for user {user_id}"
    
    # Simulate multiple calls
    for i in range(5):
        handle_request(i)
    
    print(f"  Total calls: {handle_request.call_count}")


def example_once():
    """Example: Using @once for initialization"""
    print("\n" + "="*60)
    print("Example: @once decorator")
    print("="*60)
    
    @once
    def load_config():
        print("  Loading configuration...")
        return {
            "api_key": "secret-key",
            "timeout": 30,
            "retries": 3
        }
    
    config1 = load_config()
    config2 = load_config()
    config3 = load_config()
    
    print(f"  Config loaded once: {config1 is config2 and config2 is config3}")


def example_throttle():
    """Example: Using @throttle for UI events"""
    print("\n" + "="*60)
    print("Example: @throttle decorator")
    print("="*60)
    
    events = []
    
    @throttle(interval=0.3)
    def handle_scroll(position):
        events.append(position)
        return position
    
    print("  Simulating rapid scroll events:")
    for i in range(10):
        result = handle_scroll(i * 100)
        time.sleep(0.05)
    
    print(f"  Events processed: {len(events)}")
    print(f"  Positions: {events}")


def example_wrap_exceptions():
    """Example: Using @wrap_exceptions for error handling"""
    print("\n" + "="*60)
    print("Example: @wrap_exceptions decorator")
    print("="*60)
    
    class ConfigError(Exception):
        pass
    
    @wrap_exceptions(catch=(KeyError, ValueError), raise_as=ConfigError, message="Invalid configuration")
    def load_config_value(config, key):
        return config[key]
    
    config = {"host": "localhost", "port": 8080}
    
    # Valid access
    host = load_config_value(config, "host")
    print(f"  Valid key 'host': {host}")
    
    # Invalid access
    try:
        load_config_value(config, "missing_key")
    except ConfigError as e:
        print(f"  Caught ConfigError: {e}")


def example_profile():
    """Example: Using @profile for performance analysis"""
    print("\n" + "="*60)
    print("Example: @profile decorator")
    print("="*60)
    
    @profile
    def analyze_data(n):
        """Perform some data analysis"""
        data = [i ** 2 for i in range(n)]
        return {
            "count": len(data),
            "sum": sum(data),
            "avg": sum(data) / len(data) if data else 0
        }
    
    result = analyze_data(100000)
    print(f"  Analysis result: sum={result['sum']}")


def example_timed_block():
    """Example: Using timed_block context manager"""
    print("\n" + "="*60)
    print("Example: timed_block context manager")
    print("="*60)
    
    print("  Processing data in timed blocks:")
    
    with timed_block("Data loading"):
        time.sleep(0.1)
        print("  - Loaded 1000 records")
    
    with timed_block("Data processing"):
        time.sleep(0.15)
        print("  - Processed 1000 records")


def example_combine():
    """Example: Combining multiple decorators"""
    print("\n" + "="*60)
    print("Example: @combine decorator")
    print("="*60)
    
    @combine(count_calls, timer, retry(max_attempts=3, delay=0.1, exceptions=(ValueError,)))
    def robust_api_call(endpoint):
        """API call with timing, counting, and retry"""
        if robust_api_call.call_count < 2:
            raise ValueError("Temporary error")
        return {"endpoint": endpoint, "status": "ok"}
    
    result = robust_api_call("/users")
    print(f"  Result: {result}")
    print(f"  Total calls: {robust_api_call.call_count}")


def example_real_world():
    """Example: Real-world combination of decorators"""
    print("\n" + "="*60)
    print("Example: Real-world API client with decorators")
    print("="*60)
    
    import warnings
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    
    # Simulated API client with full decorator stack
    @singleton
    class APIClient:
        @log_calls(include_time=False, include_result=False)
        @rate_limit(calls=5, period=1.0)
        @retry(max_attempts=3, delay=0.1, exceptions=(ConnectionError,))
        def fetch(self, endpoint):
            print(f"  Fetching: {endpoint}")
            time.sleep(0.1)
            return {"data": f"Response from {endpoint}"}
        
        @deprecated(reason="Use fetch instead", version="2.0.0")
        def get(self, endpoint):
            return self.fetch(endpoint)
    
    client1 = APIClient()
    client2 = APIClient()
    
    print(f"  Singleton: client1 is client2 = {client1 is client2}")
    
    # Make some API calls
    result = client1.fetch("/users")
    print(f"  Response: {result}")


def main():
    """Run all examples"""
    print("\n" + "#"*60)
    print("# Decorator Utils - Complete Usage Examples")
    print("#"*60)
    
    examples = [
        example_timer,
        example_timer_verbose,
        example_retry,
        example_memoize,
        example_singleton,
        example_deprecated,
        example_validate_types,
        example_rate_limit,
        example_log_calls,
        example_timeout,
        example_count_calls,
        example_once,
        example_throttle,
        example_wrap_exceptions,
        example_profile,
        example_timed_block,
        example_combine,
        example_real_world,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n  Error in {example.__name__}: {e}")
    
    print("\n" + "#"*60)
    print("# All examples completed!")
    print("#"*60 + "\n")


if __name__ == "__main__":
    main()