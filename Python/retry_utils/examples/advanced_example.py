#!/usr/bin/env python3
"""
AllToolkit - Retry Utils Advanced Examples

Demonstrates advanced patterns like circuit breakers, cascading retries,
and integration with external services.
"""

import sys
import os
import time
import random
from typing import Optional, Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    retry,
    RetryConfig,
    RetryExecutor,
    RetryStats,
    RetryError,
    BackoffStrategies,
    NetworkError,
    ServiceUnavailableError,
    RateLimitError,
)


class CircuitBreaker:
    """
    Simple circuit breaker implementation using retry_utils.
    
    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Circuit is open, requests fail immediately
    - HALF_OPEN: Testing if service recovered
    """
    
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        half_open_max_calls: int = 3,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        
        self.state = self.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.half_open_calls = 0
        self._lock = None  # Would use threading.Lock in production
    
    def call(self, func, *args, **kwargs):
        """Execute function through circuit breaker."""
        if self.state == self.OPEN:
            if self._should_attempt_reset():
                self.state = self.HALF_OPEN
                self.half_open_calls = 0
                print(f"  [Circuit] State: OPEN -> HALF_OPEN")
            else:
                raise ServiceUnavailableError(
                    f"Circuit is OPEN. Retry after {self.recovery_timeout}s"
                )
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True
        return (time.time() - self.last_failure_time) >= self.recovery_timeout
    
    def _on_success(self):
        """Handle successful call."""
        if self.state == self.HALF_OPEN:
            self.half_open_calls += 1
            if self.half_open_calls >= self.half_open_max_calls:
                self.state = self.CLOSED
                self.failure_count = 0
                print(f"  [Circuit] State: HALF_OPEN -> CLOSED (recovered)")
        else:
            self.failure_count = 0
    
    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == self.HALF_OPEN:
            self.state = self.OPEN
            print(f"  [Circuit] State: HALF_OPEN -> OPEN (recovery failed)")
        elif self.failure_count >= self.failure_threshold:
            self.state = self.OPEN
            print(f"  [Circuit] State: CLOSED -> OPEN (threshold reached)")


def example_circuit_breaker():
    """Example: Circuit breaker with retry."""
    print("\n" + "=" * 60)
    print("Advanced Example 1: Circuit Breaker Pattern")
    print("=" * 60)
    
    circuit = CircuitBreaker(failure_threshold=3, recovery_timeout=5.0)
    
    call_count = 0
    
    @retry(max_retries=2, base_delay=0.1)
    def unstable_service():
        nonlocal call_count
        call_count += 1
        print(f"  Service call {call_count}...")
        
        # Simulate service that fails initially then recovers
        if call_count <= 5:
            raise NetworkError("Service unavailable")
        
        return "Service response"
    
    # Simulate multiple calls over time
    for i in range(8):
        print(f"\n[Iteration {i + 1}]")
        try:
            result = circuit.call(unstable_service)
            print(f"  Success: {result}")
        except Exception as e:
            print(f"  Failed: {e}")
        
        time.sleep(0.5)  # Wait between calls
    
    print(f"\n  Final circuit state: {circuit.state}")
    print(f"  Total service calls: {call_count}")


def example_cascading_fallback():
    """Example: Cascading fallback with multiple services."""
    print("\n" + "=" * 60)
    print("Advanced Example 2: Cascading Fallback")
    print("=" * 60)
    
    # Primary service config (aggressive retry)
    primary_config = RetryConfig(
        max_retries=2,
        base_delay=0.2,
        retryable_exceptions=(NetworkError, ConnectionError),
    )
    
    # Secondary service config (quick retry)
    secondary_config = RetryConfig(
        max_retries=1,
        base_delay=0.1,
        retryable_exceptions=(NetworkError,),
    )
    
    primary_calls = 0
    secondary_calls = 0
    cache_hits = 0
    
    cache: Dict[str, Any] = {}
    
    def call_primary_service(key: str):
        nonlocal primary_calls
        primary_calls += 1
        print(f"  Primary service call for '{key}' (attempt #{primary_calls})...")
        
        # Simulate primary being down
        raise NetworkError("Primary service unavailable")
    
    def call_secondary_service(key: str):
        nonlocal secondary_calls
        secondary_calls += 1
        print(f"  Secondary service call for '{key}'...")
        
        # Simulate secondary working
        return f"Data from secondary: {key}"
    
    def get_from_cache(key: str) -> Optional[Any]:
        nonlocal cache_hits
        if key in cache:
            cache_hits += 1
            print(f"  Cache hit for '{key}'!")
            return cache[key]
        return None
    
    def get_data_with_fallback(key: str):
        """Try primary, then secondary, then cache."""
        # Try primary
        try:
            executor = RetryExecutor(primary_config)
            result = executor.execute(call_primary_service, key)
            cache[key] = result
            return result
        except RetryError as e:
            print(f"  Primary failed after {e.attempts} attempts")
        
        # Try secondary
        try:
            executor = RetryExecutor(secondary_config)
            result = executor.execute(call_secondary_service, key)
            cache[key] = result
            return result
        except RetryError:
            print(f"  Secondary also failed")
        
        # Try cache
        cached = get_from_cache(key)
        if cached is not None:
            return cached
        
        raise ServiceUnavailableError("All data sources unavailable")
    
    # Test the cascading fallback
    print("\n  Request 1:")
    result = get_data_with_fallback("user:123")
    print(f"  Result: {result}")
    
    print("\n  Request 2 (should use cache):")
    result = get_data_with_fallback("user:123")
    print(f"  Result: {result}")
    
    print(f"\n  Statistics:")
    print(f"    Primary calls: {primary_calls}")
    print(f"    Secondary calls: {secondary_calls}")
    print(f"    Cache hits: {cache_hits}")


def example_rate_limit_handling():
    """Example: Smart rate limit handling."""
    print("\n" + "=" * 60)
    print("Advanced Example 3: Rate Limit Handling")
    print("=" * 60)
    
    # Track rate limit state
    rate_limit_reset_time: Optional[float] = None
    request_count = 0
    
    def on_retry_with_rate_limit(attempt: int, exception: Exception, delay: float):
        """Custom retry handler that respects rate limit headers."""
        nonlocal rate_limit_reset_time
        
        if isinstance(exception, RateLimitError) and exception.retry_after:
            rate_limit_reset_time = time.time() + exception.retry_after
            print(f"  Rate limited! Waiting {exception.retry_after}s as instructed...")
        else:
            print(f"  Retry {attempt}: {type(exception).__name__}")
    
    config = RetryConfig(
        max_retries=5,
        base_delay=1.0,
        max_delay=60.0,
        on_retry=on_retry_with_rate_limit,
    )
    
    def make_api_request():
        nonlocal request_count
        request_count += 1
        
        print(f"  API request #{request_count}...")
        
        # Simulate rate limiting
        if request_count <= 2:
            raise RateLimitError("Rate limit exceeded", retry_after=2.0)
        
        if request_count == 3:
            raise NetworkError("Connection error")
        
        return {"status": "success", "data": "API response"}
    
    executor = RetryExecutor(config)
    
    start = time.time()
    result = executor.execute(make_api_request)
    elapsed = time.time() - start
    
    print(f"\n  Result: {result}")
    print(f"  Total time: {elapsed:.2f}s")
    print(f"  Total requests: {request_count}")


def example_batch_operations():
    """Example: Batch operations with retry."""
    print("\n" + "=" * 60)
    print("Advanced Example 4: Batch Operations")
    print("=" * 60)
    
    config = RetryConfig(
        max_retries=2,
        base_delay=0.1,
        stats=RetryStats(),
    )
    
    # Simulate batch processing
    items = [f"item_{i}" for i in range(10)]
    results = []
    failures = []
    
    def process_item(item: str):
        """Process a single item with retry."""
        call_count = 0
        
        def do_process():
            nonlocal call_count
            call_count += 1
            
            # Simulate random failures (30% chance)
            if random.random() < 0.3:
                raise NetworkError(f"Transient failure processing {item}")
            
            return f"Processed: {item}"
        
        executor = RetryExecutor(config)
        return executor.execute(do_process)
    
    print("  Processing batch of 10 items...")
    
    for item in items:
        try:
            result = process_item(item)
            results.append(result)
            print(f"  ✓ {result}")
        except RetryError as e:
            failures.append((item, e))
            print(f"  ✗ {item}: Failed after {e.attempts} attempts")
    
    print(f"\n  Batch Summary:")
    print(f"    Successful: {len(results)}")
    print(f"    Failed: {len(failures)}")
    print(f"    Success rate: {len(results) / len(items):.1%}")
    print(f"    Stats: {config.stats.to_dict()}")


def example_priority_queue():
    """Example: Priority-based retry with different configs."""
    print("\n" + "=" * 60)
    print("Advanced Example 5: Priority-Based Retry")
    print("=" * 60)
    
    # Different configs for different priorities
    high_priority = RetryConfig(
        max_retries=5,
        base_delay=0.1,
        max_delay=5.0,
        jitter=False,
    )
    
    normal_priority = RetryConfig(
        max_retries=3,
        base_delay=0.5,
        max_delay=30.0,
    )
    
    low_priority = RetryConfig(
        max_retries=1,
        base_delay=1.0,
        max_delay=60.0,
    )
    
    def get_config_for_priority(priority: str) -> RetryConfig:
        """Get retry config based on priority."""
        configs = {
            'high': high_priority,
            'normal': normal_priority,
            'low': low_priority,
        }
        return configs.get(priority, normal_priority)
    
    def process_with_priority(task_name: str, priority: str):
        """Process task with priority-appropriate retry."""
        config = get_config_for_priority(priority)
        
        call_count = 0
        
        def do_task():
            nonlocal call_count
            call_count += 1
            print(f"  [{priority.upper()}] {task_name} - attempt {call_count}")
            
            # Simulate task
            if random.random() < 0.4:
                raise NetworkError("Task failed")
            
            return f"Task {task_name} completed"
        
        executor = RetryExecutor(config)
        return executor.execute(do_task)
    
    # Process tasks with different priorities
    tasks = [
        ("Critical payment", "high"),
        ("Email notification", "normal"),
        ("Analytics update", "low"),
        ("User login", "high"),
        ("Log aggregation", "low"),
    ]
    
    for task_name, priority in tasks:
        print(f"\n  Processing: {task_name} ({priority} priority)")
        try:
            result = process_with_priority(task_name, priority)
            print(f"  Result: {result}")
        except RetryError as e:
            print(f"  Failed: {e}")


def example_adaptive_retry():
    """Example: Adaptive retry based on error patterns."""
    print("\n" + "=" * 60)
    print("Advanced Example 6: Adaptive Retry")
    print("=" * 60)
    
    error_history = []
    
    def get_adaptive_config() -> RetryConfig:
        """Adjust retry config based on recent error patterns."""
        if len(error_history) < 3:
            return RetryConfig(max_retries=3, base_delay=0.5)
        
        # Analyze recent errors
        recent_errors = error_history[-5:]
        network_errors = sum(1 for e in recent_errors if isinstance(e, NetworkError))
        
        if network_errors >= 3:
            # Network seems unstable - be more aggressive
            print("  [Adaptive] Network unstable - increasing retries")
            return RetryConfig(max_retries=5, base_delay=0.3, max_delay=10.0)
        else:
            # Normal operation
            return RetryConfig(max_retries=3, base_delay=0.5)
    
    def make_request():
        """Make request with adaptive retry."""
        config = get_adaptive_config()
        
        call_count = 0
        
        def do_request():
            nonlocal call_count
            call_count += 1
            
            # Simulate varying error patterns
            if call_count == 1:
                error = NetworkError("Connection timeout")
                error_history.append(error)
                raise error
            
            if call_count == 2:
                error = NetworkError("DNS resolution failed")
                error_history.append(error)
                raise error
            
            return "Request successful"
        
        executor = RetryExecutor(config)
        return executor.execute(do_request)
    
    # Make multiple requests to trigger adaptive behavior
    for i in range(3):
        print(f"\n  Request {i + 1}:")
        try:
            result = make_request()
            print(f"  Result: {result}")
        except RetryError as e:
            print(f"  Failed: {e}")
        
        # Clear history periodically
        if len(error_history) > 10:
            error_history.clear()


def example_distributed_retry():
    """Example: Distributed retry coordination (simulation)."""
    print("\n" + "=" * 60)
    print("Advanced Example 7: Distributed Retry Coordination")
    print("=" * 60)
    
    # Simulate distributed state
    shared_state = {
        'global_retry_count': 0,
        'last_retry_time': 0,
        'circuit_state': 'closed',
    }
    
    def distributed_retry_config() -> RetryConfig:
        """Get config that considers distributed state."""
        # In real implementation, this would check a distributed cache
        
        if shared_state['circuit_state'] == 'open':
            # Global circuit is open
            return RetryConfig(max_retries=0)  # Fail immediately
        
        return RetryConfig(
            max_retries=3,
            base_delay=0.5,
            on_retry=lambda a, e, d: update_distributed_state(a, e),
        )
    
    def update_distributed_state(attempt: int, exception: Exception):
        """Update shared state on retry."""
        shared_state['global_retry_count'] += 1
        shared_state['last_retry_time'] = time.time()
        
        # Open circuit if too many global retries
        if shared_state['global_retry_count'] > 10:
            shared_state['circuit_state'] = 'open'
            print(f"  [Distributed] Global circuit OPENED")
    
    def call_distributed_service():
        call_count = 0
        
        def do_call():
            nonlocal call_count
            call_count += 1
            print(f"  Distributed call {call_count}...")
            
            if call_count <= 2:
                raise NetworkError("Service unavailable")
            
            return "Distributed response"
        
        config = distributed_retry_config()
        executor = RetryExecutor(config)
        return executor.execute(do_call)
    
    # Simulate multiple nodes calling the service
    print("  Simulating 3 distributed nodes...")
    
    for node_id in range(3):
        print(f"\n  Node {node_id}:")
        try:
            result = call_distributed_service()
            print(f"  Result: {result}")
        except RetryError as e:
            print(f"  Failed: {e}")
        
        time.sleep(0.1)
    
    print(f"\n  Final distributed state:")
    print(f"    Global retry count: {shared_state['global_retry_count']}")
    print(f"    Circuit state: {shared_state['circuit_state']}")


def main():
    """Run all advanced examples."""
    print("\n" + "🚀" * 30)
    print("AllToolkit - Python Retry Utils Advanced Examples")
    print("🚀" * 30)
    
    # Set random seed for reproducibility in demos
    random.seed(42)
    
    example_circuit_breaker()
    example_cascading_fallback()
    example_rate_limit_handling()
    example_batch_operations()
    example_priority_queue()
    example_adaptive_retry()
    example_distributed_retry()
    
    print("\n" + "=" * 60)
    print("All advanced examples completed!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
