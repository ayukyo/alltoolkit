#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Circuit Breaker Usage Examples

Demonstrates various ways to use the Circuit Breaker utilities.

Author: AllToolkit
License: MIT
"""

import time
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from circuit_breaker_utils.mod import (
    CircuitBreaker, CircuitState, CircuitEvent,
    CircuitOpenError, CircuitBreakerRegistry,
    AsyncCircuitBreaker, create_circuit_breaker, get_registry
)


def example_basic_usage():
    """Example 1: Basic circuit breaker usage."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Circuit Breaker Usage")
    print("=" * 60)
    
    # Create a circuit breaker
    breaker = CircuitBreaker(
        name="api_service",
        failure_threshold=3,    # Open after 3 failures
        timeout=10.0,           # Wait 10s before retry
        success_threshold=2     # Close after 2 successes
    )
    
    print(f"\nInitial state: {breaker.state.name}")
    
    # Simulate successful calls
    print("\nMaking successful calls...")
    for i in range(3):
        result = breaker.call(lambda: f"API response {i}")
        print(f"  Call {i}: {result} - State: {breaker.state.name}")
    
    print(f"\nStats: {breaker.stats.successful_calls} successes")
    
    # Simulate failures
    print("\nSimulating failures...")
    def failing_api_call():
        raise ConnectionError("API unavailable")
    
    for i in range(5):
        try:
            breaker.call(failing_api_call)
        except ConnectionError:
            print(f"  Call {i}: ConnectionError - State: {breaker.state.name}")
        except CircuitOpenError as e:
            print(f"  Call {i}: CircuitOpenError - {e}")
    
    print(f"\nStats: {breaker.stats.failed_calls} failures, "
          f"{breaker.stats.rejected_calls} rejected")
    print(f"Final state: {breaker.state.name}")


def example_decorator():
    """Example 2: Using decorator for protection."""
    print("\n" + "=" * 60)
    print("Example 2: Decorator Pattern")
    print("=" * 60)
    
    breaker = CircuitBreaker(
        name="database",
        failure_threshold=5,
        timeout=30.0
    )
    
    # Protect a function with decorator
    @breaker.protect
    def get_user(user_id):
        """Simulated database query."""
        if user_id == "fail":
            raise Exception("Database connection lost")
        return {"id": user_id, "name": f"User {user_id}"}
    
    # Successful call
    print("\nSuccessful query:")
    user = get_user("123")
    print(f"  Result: {user}")
    print(f"  State: {breaker.state.name}")
    
    # Failed calls
    print("\nFailed queries:")
    for i in range(6):
        try:
            get_user("fail")
        except Exception as e:
            print(f"  Attempt {i}: {type(e).__name__} - State: {breaker.state.name}")
    
    # Circuit is open - subsequent calls are rejected
    print("\nAfter circuit opens:")
    try:
        get_user("123")
    except CircuitOpenError as e:
        print(f"  Rejected: {e}")
        print(f"  Retry in: {e.time_until_retry:.1f}s")


def example_context_manager():
    """Example 3: Using context manager."""
    print("\n" + "=" * 60)
    print("Example 3: Context Manager Pattern")
    print("=" * 60)
    
    breaker = CircuitBreaker(name="cache", failure_threshold=3)
    
    print("\nSuccessful operation:")
    with breaker:
        print("  Cache operation completed")
    print(f"  State: {breaker.state.name}")
    
    print("\nFailed operation:")
    try:
        with breaker:
            raise Exception("Cache timeout")
    except Exception as e:
        print(f"  Error: {e}")
    print(f"  State: {breaker.state.name}")
    
    # Trigger open state
    for i in range(2):
        try:
            with breaker:
                raise Exception("Cache error")
        except Exception:
            pass
    
    print("\nBlocked by open circuit:")
    try:
        with breaker:
            print("  This won't execute")
    except CircuitOpenError as e:
        print(f"  Blocked: Circuit is open")


def example_event_handling():
    """Example 4: Monitoring with event handlers."""
    print("\n" + "=" * 60)
    print("Example 4: Event Handling and Monitoring")
    print("=" * 60)
    
    breaker = CircuitBreaker(
        name="monitored_service",
        failure_threshold=2,
        timeout=5.0
    )
    
    # Set up event handlers
    events_log = []
    
    def log_event(event, state, details):
        timestamp = time.strftime("%H:%M:%S")
        events_log.append(f"[{timestamp}] {event.name}: {details}")
    
    breaker.on(CircuitEvent.STATE_CHANGE, log_event)
    breaker.on(CircuitEvent.FAILURE, log_event)
    breaker.on(CircuitEvent.SUCCESS, log_event)
    breaker.on(CircuitEvent.REJECTION, log_event)
    
    # Trigger some events
    print("\nTriggering events...")
    
    # Success
    breaker.call(lambda: "success")
    
    # Failures to open circuit
    for i in range(3):
        try:
            breaker.call(lambda: raise_exception())
        except Exception:
            pass
    
    # Rejection
    try:
        breaker.call(lambda: "blocked")
    except CircuitOpenError:
        pass
    
    # Print event log
    print("\nEvent log:")
    for log in events_log:
        print(f"  {log}")
    
    # Get detailed history
    print("\nDetailed event history:")
    for record in breaker.get_event_history(5):
        print(f"  {record.event_type.name}: {record.state_before.name} -> {record.state_after.name}")


def example_registry():
    """Example 5: Managing multiple circuit breakers."""
    print("\n" + "=" * 60)
    print("Example 5: Circuit Breaker Registry")
    print("=" * 60)
    
    registry = get_registry()
    
    # Create circuit breakers for different services
    api_breaker = registry.get_or_create(
        'api_gateway',
        failure_threshold=10,
        timeout=60.0
    )
    
    db_breaker = registry.get_or_create(
        'database',
        failure_threshold=5,
        timeout=30.0
    )
    
    cache_breaker = registry.get_or_create(
        'redis_cache',
        failure_threshold=3,
        timeout=10.0
    )
    
    print("\nRegistered circuit breakers:")
    for name, breaker in registry.all():
        print(f"  {name}: {breaker.state.name} (threshold: {breaker.config.failure_threshold})")
    
    # Simulate some activity
    print("\nSimulating service calls...")
    
    # API calls
    for i in range(5):
        api_breaker.call(lambda: f"API response {i}")
    print(f"  API: 5 successful calls")
    
    # Database failures
    for i in range(3):
        try:
            db_breaker.call(lambda: raise_exception())
        except Exception:
            pass
    print(f"  Database: 3 failures, state={db_breaker.state.name}")
    
    # Get health status
    print("\nHealth status:")
    health = registry.get_health()
    for name, status in health.items():
        stats = status['stats']
        print(f"  {name}:")
        print(f"    State: {status['state']}")
        print(f"    Calls: {stats['total_calls']} "
              f"(success: {stats['successful_calls']}, fail: {stats['failed_calls']})")
        print(f"    Failure rate: {stats['failure_rate']:.2%}")


def example_excluded_exceptions():
    """Example 6: Excluding specific exceptions."""
    print("\n" + "=" * 60)
    print("Example 6: Excluded Exceptions")
    print("=" * 60)
    
    breaker = CircuitBreaker(
        name="http_client",
        failure_threshold=5,
        excluded_exceptions=(ValueError, KeyError)  # These don't count
    )
    
    print("\nMaking calls with excluded exceptions:")
    
    # ValueError - doesn't count as failure
    for i in range(10):
        try:
            breaker.call(lambda: raise_value_error())
        except ValueError:
            print(f"  Call {i}: ValueError (excluded) - State: {breaker.state.name}")
    
    print(f"\nStats: {breaker.stats.failed_calls} failures (ValueErrors excluded)")
    
    # ConnectionError - counts as failure
    print("\nMaking calls with counted exceptions:")
    for i in range(6):
        try:
            breaker.call(lambda: raise_connection_error())
        except ConnectionError:
            print(f"  Call {i}: ConnectionError - State: {breaker.state.name}")
        except CircuitOpenError:
            print(f"  Call {i}: CircuitOpenError")
    
    print(f"\nStats: {breaker.stats.failed_calls} failures (ConnectionErrors counted)")


def example_failure_rate_threshold():
    """Example 7: Using failure rate threshold."""
    print("\n" + "=" * 60)
    print("Example 7: Failure Rate Threshold")
    print("=" * 60)
    
    breaker = CircuitBreaker(
        name="rate_based",
        failure_threshold=100,  # High threshold (not used)
        failure_rate_threshold=0.5,  # 50% failure rate
        minimum_calls_for_rate=10,  # Need at least 10 calls
        timeout=30.0
    )
    
    print("\nMaking mixed success/failure calls:")
    
    # 6 successes, 4 failures = 40% rate (below threshold)
    for i in range(6):
        breaker.call(lambda: "success")
    for i in range(4):
        try:
            breaker.call(lambda: raise_exception())
        except Exception:
            pass
    
    print(f"  6 successes + 4 failures = {breaker.stats.failure_rate:.0%} rate")
    print(f"  State: {breaker.state.name} (below 50% threshold)")
    
    # Add 2 more failures = 6 failures / 12 total = 50% (at threshold)
    for i in range(2):
        try:
            breaker.call(lambda: raise_exception())
        except Exception:
            pass
    
    print(f"\n  6 successes + 6 failures = {breaker.stats.failure_rate:.0%} rate")
    print(f"  State: {breaker.state.name} (at 50% threshold)")
    
    # One more failure to exceed
    try:
        breaker.call(lambda: raise_exception())
    except Exception:
        pass
    
    print(f"\n  6 successes + 7 failures = {breaker.stats.failure_rate:.0%} rate")
    print(f"  State: {breaker.state.name} (exceeds threshold)")


def example_exponential_backoff():
    """Example 8: Exponential backoff for recovery."""
    print("\n" + "=" * 60)
    print("Example 8: Exponential Backoff")
    print("=" * 60)
    
    breaker = CircuitBreaker(
        name="backoff_service",
        failure_threshold=2,
        timeout=2.0,
        exponential_backoff=True,
        backoff_multiplier=2.0,
        max_timeout=60.0
    )
    
    print("\nOpening circuit multiple times to demonstrate backoff:")
    
    cycle = 0
    timeouts = []
    
    while cycle < 4:
        # Open the circuit
        while breaker.state != CircuitState.OPEN:
            try:
                breaker.call(lambda: raise_exception())
            except Exception:
                pass
        
        current_timeout = breaker.time_until_retry + 1
        timeouts.append(current_timeout)
        print(f"  Cycle {cycle + 1}: Timeout ≈ {current_timeout:.1f}s")
        
        # Wait and fail again
        time.sleep(current_timeout + 0.5)
        try:
            breaker.call(lambda: raise_exception())
        except Exception:
            pass
        
        cycle += 1
    
    print(f"\nTimeout progression: {[f'{t:.1f}s' for t in timeouts]}")
    print("(Each timeout doubles, up to max_timeout)")


def example_manual_control():
    """Example 9: Manual circuit control."""
    print("\n" + "=" * 60)
    print("Example 9: Manual Control")
    print("=" * 60)
    
    breaker = CircuitBreaker(name="manual_control", failure_threshold=5)
    
    print("\nInitial state:", breaker.state.name)
    
    # Manual open
    print("\nManually opening circuit...")
    breaker.force_open("maintenance_mode")
    print(f"  State: {breaker.state.name}")
    
    try:
        breaker.call(lambda: "blocked")
    except CircuitOpenError as e:
        print(f"  Call rejected: {e}")
    
    # Manual close
    print("\nManually closing circuit...")
    breaker.force_close()
    print(f"  State: {breaker.state.name}")
    
    result = breaker.call(lambda: "success after manual close")
    print(f"  Call succeeded: {result}")
    
    # Full reset
    print("\nFull reset (clears stats too)...")
    breaker.reset()
    print(f"  State: {breaker.state.name}")
    print(f"  Stats cleared: total_calls = {breaker.stats.total_calls}")


def example_production_pattern():
    """Example 10: Production pattern with retries and fallback."""
    print("\n" + "=" * 60)
    print("Example 10: Production Pattern (Retry + Fallback)")
    print("=" * 60)
    
    breaker = CircuitBreaker(
        name="production_api",
        failure_threshold=3,
        timeout=30.0,
        half_open_max_calls=1
    )
    
    # Fallback function
    def fallback_handler():
        return {"data": "cached_value", "source": "fallback"}
    
    # Simulated API call
    call_count = 0
    
    def api_call_with_retry(max_retries=2):
        """Pattern: Circuit breaker + retries + fallback."""
        global call_count
        
        # Check circuit first
        if not breaker.allow_request():
            print("  Using fallback (circuit open)")
            return fallback_handler()
        
        for attempt in range(max_retries + 1):
            try:
                call_count += 1
                # Simulate intermittent failures
                if call_count % 3 == 0:
                    raise ConnectionError("API error")
                
                result = breaker.call(lambda: {"data": f"fresh_{call_count}", "source": "api"})
                return result
                
            except ConnectionError as e:
                print(f"  Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries:
                    time.sleep(0.1)  # Brief retry delay
                continue
        
        # All retries failed, return fallback
        print("  All retries failed, using fallback")
        return fallback_handler()
    
    print("\nMaking calls with production pattern:")
    
    for i in range(8):
        result = api_call_with_retry()
        print(f"  Call {i + 1}: {result['source']} - Circuit: {breaker.state.name}")


def raise_exception():
    """Helper to raise a generic exception."""
    raise Exception("Simulated failure")


def raise_value_error():
    """Helper to raise ValueError."""
    raise ValueError("Invalid value")


def raise_connection_error():
    """Helper to raise ConnectionError."""
    raise ConnectionError("Connection failed")


def main():
    """Run all examples."""
    print("\n" + "#" * 60)
    print("# Circuit Breaker Utilities - Usage Examples")
    print("#" * 60)
    
    example_basic_usage()
    example_decorator()
    example_context_manager()
    example_event_handling()
    example_registry()
    example_excluded_exceptions()
    example_failure_rate_threshold()
    example_exponential_backoff()
    example_manual_control()
    example_production_pattern()
    
    print("\n" + "#" * 60)
    print("# All examples completed!")
    print("#" * 60)


if __name__ == "__main__":
    main()