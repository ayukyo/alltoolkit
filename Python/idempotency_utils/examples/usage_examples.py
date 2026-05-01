"""
AllToolkit - Idempotency Utilities Usage Examples

Practical examples demonstrating how to use idempotency utilities
for preventing duplicate operations in distributed systems.

Author: AllToolkit
License: MIT
"""

import time
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from idempotency_utils.mod import (
    IdempotencyStore,
    IdempotencyKeyGenerator,
    IdempotencyManager,
    RequestDeduplicator,
    idempotent,
    DuplicateOperationError,
    OperationInProgressError,
)


def example_basic_store():
    """
    Example: Basic idempotency store usage.
    
    Use IdempotencyStore to cache operation results and prevent
    duplicate executions.
    """
    print("\n" + "="*60)
    print("Example 1: Basic Store Usage")
    print("="*60)
    
    store = IdempotencyStore(default_ttl=3600)  # 1 hour TTL
    
    # Operation 1: First execution
    print("\n[First execution]")
    key = "payment:user:123:amount:100"
    store.set_pending(key)
    
    # Simulate processing
    result = {"transaction_id": "tx-001", "status": "success"}
    store.set_completed(key, result)
    print(f"  Key: {key}")
    print(f"  Result: {result}")
    
    # Operation 2: Duplicate request
    print("\n[Duplicate request - same key]")
    cached = store.get_result(key)
    if cached:
        print(f"  ✓ Cached result returned: {cached}")
        print("  No duplicate execution!")
    
    # Different request
    print("\n[Different request - different key]")
    key2 = "payment:user:456:amount:50"
    cached2 = store.get_result(key2)
    if not cached2:
        print("  No cached result, would execute operation")
        store.set_pending(key2)
        store.set_completed(key2, {"transaction_id": "tx-002", "status": "success"})
        print(f"  ✓ New result stored")


def example_key_generation():
    """
    Example: Different ways to generate idempotency keys.
    
    Shows various methods for creating unique keys for operations.
    """
    print("\n" + "="*60)
    print("Example 2: Key Generation Methods")
    print("="*60)
    
    gen = IdempotencyKeyGenerator
    
    # Random key
    print("\n[Random key (UUID format)]")
    key1 = gen.random()
    print(f"  {key1}")
    print(f"  Length: {len(key1)} chars")
    
    # Key from hash
    print("\n[Key from function arguments]")
    key2 = gen.from_hash("process_order", order_id=123, user_id="user:456")
    print(f"  From args: process_order(order_id=123, user_id='user:456')")
    print(f"  Key: {key2}")
    
    # Same args = same key
    key3 = gen.from_hash("process_order", order_id=123, user_id="user:456")
    print(f"  Same args again: {key3}")
    print(f"  Keys match: {key2 == key3}")
    
    # Different args = different key
    key4 = gen.from_hash("process_order", order_id=456, user_id="user:456")
    print(f"  Different args: {key4}")
    print(f"  Keys match: {key2 == key4}")
    
    # Key from HTTP request
    print("\n[Key from HTTP request]")
    key5 = gen.from_request(
        method="POST",
        url="/api/payments",
        body={"amount": 100, "currency": "USD"},
    )
    print(f"  Request: POST /api/payments")
    print(f"  Body: {{'amount': 100, 'currency': 'USD'}}")
    print(f"  Key: {key5}")
    
    # Prefixed key
    print("\n[Prefixed keys]")
    base_key = "123"
    prefixed = gen.prefix("payment", base_key)
    print(f"  Base: {base_key}")
    print(f"  Prefixed: {prefixed}")
    
    # Key with timestamp
    print("\n[Key with timestamp]")
    ts_key = gen.with_timestamp("operation-123")
    print(f"  With timestamp: {ts_key}")


def example_decorator():
    """
    Example: Using the @idempotent decorator.
    
    Decorate functions to automatically prevent duplicate calls.
    """
    print("\n" + "="*60)
    print("Example 3: @idempotent Decorator")
    print("="*60)
    
    class Counter:
        count = 0
    
    @idempotent()
    def process_payment(amount: float, user_id: str):
        """Process a payment (idempotent)."""
        Counter.count += 1
        print(f"  [Actually processing payment #{Counter.count}]")
        time.sleep(0.1)  # Simulate work
        return {
            "transaction_id": f"tx-{Counter.count}",
            "amount": amount,
            "user_id": user_id,
            "status": "success",
        }
    
    # First call
    print("\n[First call]")
    result1 = process_payment(100.0, "user:123")
    print(f"  Result: {result1}")
    print(f"  Call count: {Counter.count}")
    
    # Duplicate call (same args) - cached
    print("\n[Duplicate call - same arguments]")
    result2 = process_payment(100.0, "user:123")
    print(f"  Result: {result2}")
    print(f"  Call count: {Counter.count} (unchanged!)")
    print("  ✓ Function was NOT called again")
    
    # Different args - executes
    print("\n[Different arguments]")
    result3 = process_payment(200.0, "user:456")
    print(f"  Result: {result3}")
    print(f"  Call count: {Counter.count}")


def example_custom_key_decorator():
    """
    Example: Decorator with custom key function.
    
    Use a custom key function for more flexible idempotency.
    """
    print("\n" + "="*60)
    print("Example 4: Custom Key Function")
    print("="*60)
    
    store = IdempotencyStore()
    
    @idempotent(
        key_func=lambda order_id, items=None, user_id=None: f"order:{order_id}",
        store=store,
    )
    def create_order(order_id: str, items: list = None, user_id: str = None):
        """Create an order - idempotent by order_id."""
        return {
            "order_id": order_id,
            "items": items,
            "user_id": user_id,
            "status": "created",
        }
    
    # First order
    print("\n[Create order 123]")
    result1 = create_order("123", ["item1", "item2"], "user:A")
    print(f"  Result: {result1}")
    
    # Duplicate with same order_id but different items
    print("\n[Duplicate request - same order_id]")
    result2 = create_order("123", ["different-items"], "user:B")
    print(f"  Result: {result2}")
    print("  ✓ Returned cached result (same order_id)")
    
    # Different order_id
    print("\n[New order 456]")
    result3 = create_order("456", ["item3"], "user:C")
    print(f"  Result: {result3}")


def example_manager():
    """
    Example: Using IdempotencyManager.
    
    High-level manager for idempotent operations.
    """
    print("\n" + "="*60)
    print("Example 5: IdempotencyManager")
    print("="*60)
    
    manager = IdempotencyManager(default_ttl=3600)
    
    # Define operation
    def send_email(to: str, subject: str):
        print(f"  [Sending email to {to}]")
        time.sleep(0.1)
        return {"sent": True, "to": to}
    
    # Execute with idempotency
    print("\n[First email send]")
    email_key = IdempotencyKeyGenerator.from_hash("send_email", to="user@example.com", subject="Hello")
    result1 = manager.execute(email_key, lambda: send_email("user@example.com", "Hello"))
    print(f"  Result: {result1}")
    
    # Check for result
    print("\n[Check if result exists]")
    has_result = manager.has_result(email_key)
    print(f"  Has result: {has_result}")
    
    # Get cached result
    print("\n[Get cached result]")
    cached = manager.get_result(email_key)
    print(f"  Cached: {cached}")
    
    # Duplicate send
    print("\n[Duplicate email - same key]")
    result2 = manager.execute(email_key, lambda: send_email("user@example.com", "Hello"))
    print(f"  Result: {result2}")
    print("  ✓ Used cached result")
    
    # Stats
    print("\n[Manager stats]")
    stats = manager.stats()
    print(f"  Total: {stats['total']}")
    print(f"  Completed: {stats['completed']}")


def example_request_deduplicator():
    """
    Example: Request deduplication for APIs.
    
    Prevent duplicate requests within a time window.
    """
    print("\n" + "="*60)
    print("Example 6: Request Deduplicator")
    print("="*60)
    
    deduper = RequestDeduplicator(window_seconds=5.0)
    
    # Simulate API request handling
    request_id = "req-abc123"
    
    print("\n[First request]")
    if not deduper.is_duplicate(request_id):
        print("  ✓ Processing request")
        deduper.mark(request_id)
        # Process the request
        print("  Request processed successfully")
    else:
        print("  ✗ Duplicate detected, rejected")
    
    print("\n[Duplicate request (within window)]")
    if not deduper.is_duplicate(request_id):
        print("  Processing request")
        deduper.mark(request_id)
    else:
        print("  ✓ Duplicate detected, rejected!")
    
    # Atomic check-and-mark
    print("\n[Atomic check and mark]")
    request_id2 = "req-def456"
    is_dup = deduper.check_and_mark(request_id2)
    print(f"  First check: {is_dup} (is duplicate: No)")
    
    is_dup2 = deduper.check_and_mark(request_id2)
    print(f"  Second check: {is_dup2} (is duplicate: Yes)")
    
    # Stats
    print("\n[Deduplicator stats]")
    stats = deduper.stats()
    print(f"  Tracked requests: {stats['tracked_requests']}")
    print(f"  Window: {stats['window_seconds']}s")


def example_ttl_expiry():
    """
    Example: TTL (Time-to-Live) expiry.
    
    Show how results expire after TTL.
    """
    print("\n" + "="*60)
    print("Example 7: TTL Expiry")
    print("="*60)
    
    store = IdempotencyStore(default_ttl=2.0)  # 2 second TTL
    
    # Store result with TTL
    print("\n[Store result with 2s TTL]")
    key = "temp-operation"
    store.set_completed(key, {"data": "value"}, ttl=2.0)
    print(f"  Key: {key}")
    print(f"  TTL: 2.0 seconds")
    
    # Check immediately
    print("\n[Check immediately]")
    result = store.get_result(key)
    print(f"  Result exists: {result is not None}")
    
    # Wait for expiry
    print("\n[Wait 2.5 seconds...]")
    time.sleep(2.5)
    
    # Check after expiry
    print("[Check after expiry]")
    result = store.get_result(key)
    print(f"  Result exists: {result is not None}")
    print("  ✓ Result expired and was cleaned up")


def example_api_handler():
    """
    Example: API request handler pattern.
    
    Typical pattern for handling idempotent API requests.
    """
    print("\n" + "="*60)
    print("Example 8: API Request Handler Pattern")
    print("="*60)
    
    manager = IdempotencyManager(default_ttl=86400)  # 24 hours
    deduper = RequestDeduplicator(window_seconds=10.0)
    
    def handle_api_request(request_id: str, operation_type: str, data: dict):
        """Handle an idempotent API request."""
        
        # Step 1: Check for duplicate within short window
        if deduper.check_and_mark(request_id):
            return {"error": "duplicate_request", "message": "Request already processing"}
        
        # Step 2: Generate idempotency key
        key = IdempotencyKeyGenerator.prefix(
            operation_type,
            IdempotencyKeyGenerator.from_hash(data),
        )
        
        # Step 3: Check for cached result
        if manager.has_result(key):
            cached = manager.get_result(key)
            return {
                "status": "cached",
                "result": cached,
                "message": "Returning cached result",
            }
        
        # Step 4: Execute operation
        try:
            result = manager.execute(key, lambda: {
                "processed": True,
                "operation": operation_type,
                "data": data,
            })
            return {
                "status": "success",
                "result": result,
            }
        except OperationInProgressError:
            return {
                "status": "in_progress",
                "message": "Operation already in progress",
            }
    
    # First request
    print("\n[First API request]")
    response1 = handle_api_request(
        "req-001",
        "create_order",
        {"order_id": 123, "items": ["apple", "banana"]},
    )
    print(f"  Response: {response1}")
    
    # Duplicate request (same request_id)
    print("\n[Duplicate request_id]")
    response2 = handle_api_request(
        "req-001",  # Same request ID
        "create_order",
        {"order_id": 123, "items": ["apple", "banana"]},
    )
    print(f"  Response: {response2}")
    
    # Same operation, different request_id
    print("\n[Same operation, different request_id]")
    response3 = handle_api_request(
        "req-002",  # Different request ID
        "create_order",
        {"order_id": 123, "items": ["apple", "banana"]},
    )
    print(f"  Response: {response3}")
    print("  ✓ Cached result returned")


def example_error_handling():
    """
    Example: Error handling with idempotency.
    
    Show how errors are tracked and operations can be retried.
    """
    print("\n" + "="*60)
    print("Example 9: Error Handling")
    print("="*60)
    
    store = IdempotencyStore()
    
    key = "risky-operation"
    
    # Attempt 1: Error
    print("\n[First attempt - fails]")
    store.set_pending(key)
    try:
        # Simulate error
        raise ValueError("Database connection failed")
    except ValueError as e:
        store.set_error(key, str(e))
        print(f"  Error recorded: {e}")
    
    # Check status
    record = store.get(key)
    print(f"  Status: {record.status.value}")
    print(f"  Error: {record.error}")
    
    # Retry (error state allows retry)
    print("\n[Retry - succeeds]")
    store.set_pending(key)  # Reset to pending
    result = {"data": "success"}
    store.set_completed(key, result)
    print(f"  Result: {result}")
    
    # Final check
    final = store.get_result(key)
    print(f"  Cached result: {final}")


def main():
    """Run all examples."""
    print("="*60)
    print("AllToolkit - Idempotency Utilities Examples")
    print("="*60)
    
    example_basic_store()
    example_key_generation()
    example_decorator()
    example_custom_key_decorator()
    example_manager()
    example_request_deduplicator()
    example_ttl_expiry()
    example_api_handler()
    example_error_handling()
    
    print("\n" + "="*60)
    print("All examples completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()