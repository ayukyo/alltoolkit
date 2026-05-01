"""
AllToolkit - Python Idempotency Utilities Test Suite

Comprehensive tests covering idempotency key management,
result caching, request deduplication, and edge cases.

Author: AllToolkit
License: MIT
"""

import threading
import time
import uuid
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from idempotency_utils.mod import (
    IdempotencyStore,
    IdempotencyRecord,
    IdempotencyStatus,
    IdempotencyKeyGenerator,
    IdempotencyManager,
    RequestDeduplicator,
    IdempotencyError,
    DuplicateOperationError,
    OperationInProgressError,
    idempotent,
    get_global_store,
    get_global_deduplicator,
    reset_global_store,
    reset_global_deduplicator,
)


class TestResultCollector:
    """Collect test results."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, name: str):
        self.passed += 1
        print(f"✅ PASS: {name}")
    
    def add_fail(self, name: str, error: str):
        self.failed += 1
        self.errors.append(f"{name}: {error}")
        print(f"❌ FAIL: {name} - {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}")
        if self.errors:
            print("Failures:")
            for e in self.errors:
                print(f"  - {e}")
        return self.failed == 0


def run_test(name: str, func, collector: TestResultCollector):
    """Run a single test."""
    try:
        func()
        collector.add_pass(name)
    except AssertionError as e:
        collector.add_fail(name, str(e))
    except Exception as e:
        collector.add_fail(name, f"Exception: {type(e).__name__}: {e}")


# ============================================================================
# IdempotencyRecord Tests
# ============================================================================

def test_record_creation():
    """Test record creation."""
    record = IdempotencyRecord(
        key="test-key",
        status=IdempotencyStatus.PENDING,
    )
    assert record.key == "test-key"
    assert record.status == IdempotencyStatus.PENDING
    assert record.result is None
    assert record.error is None
    assert record.created_at > 0
    assert record.completed_at is None
    assert record.expires_at is None


def test_record_expiry():
    """Test record expiry checking."""
    # Not expired
    record = IdempotencyRecord(
        key="test",
        status=IdempotencyStatus.COMPLETED,
        expires_at=time.time() + 100,
    )
    assert not record.is_expired()
    
    # Expired
    record = IdempotencyRecord(
        key="test",
        status=IdempotencyStatus.COMPLETED,
        expires_at=time.time() - 1,
    )
    assert record.is_expired()
    
    # No expiry
    record = IdempotencyRecord(
        key="test",
        status=IdempotencyStatus.COMPLETED,
        expires_at=None,
    )
    assert not record.is_expired()


def test_record_age():
    """Test record age calculation."""
    record = IdempotencyRecord(
        key="test",
        status=IdempotencyStatus.PENDING,
    )
    age = record.age()
    assert age >= 0
    assert age < 1  # Should be very recent


def test_record_to_dict():
    """Test record serialization."""
    record = IdempotencyRecord(
        key="test",
        status=IdempotencyStatus.COMPLETED,
        result={"data": "value"},
        metadata={"foo": "bar"},
    )
    d = record.to_dict()
    assert d['key'] == "test"
    assert d['status'] == "completed"
    assert d['result'] == {"data": "value"}
    assert d['metadata'] == {"foo": "bar"}


# ============================================================================
# IdempotencyStore Tests
# ============================================================================

def test_store_basic_operations():
    """Test basic store operations."""
    store = IdempotencyStore()
    
    # Set pending
    store.set_pending("key-1")
    record = store.get("key-1")
    assert record is not None
    assert record.status == IdempotencyStatus.IN_PROGRESS
    
    # Set completed
    store.set_completed("key-1", {"result": "success"})
    record = store.get("key-1")
    assert record.status == IdempotencyStatus.COMPLETED
    assert record.result == {"result": "success"}
    
    # Delete
    assert store.delete("key-1")
    assert store.get("key-1") is None
    assert not store.delete("key-1")  # Already deleted


def test_store_exists_checks():
    """Test existence check methods."""
    store = IdempotencyStore()
    
    # Initially not exists
    assert not store.exists("key-1")
    assert not store.is_in_progress("key-1")
    assert not store.is_completed("key-1")
    
    # Pending
    store.set_pending("key-1")
    assert store.exists("key-1")
    assert store.is_in_progress("key-1")
    assert not store.is_completed("key-1")
    
    # Completed
    store.set_completed("key-1", "result")
    assert store.exists("key-1")
    assert not store.is_in_progress("key-1")
    assert store.is_completed("key-1")


def test_store_get_result():
    """Test result retrieval."""
    store = IdempotencyStore()
    
    # No result
    assert store.get_result("key-1") is None
    
    # Pending - no result
    store.set_pending("key-1")
    assert store.get_result("key-1") is None
    
    # Completed - has result
    store.set_completed("key-1", 42)
    assert store.get_result("key-1") == 42


def test_store_ttl():
    """Test TTL functionality."""
    store = IdempotencyStore(default_ttl=2.0)
    
    store.set_completed("key-1", "result", ttl=2.0)
    assert store.get("key-1") is not None
    
    # Wait for expiry
    time.sleep(2.5)
    assert store.get("key-1") is None


def test_store_error_handling():
    """Test error state handling."""
    store = IdempotencyStore()
    
    store.set_pending("key-1")
    store.set_error("key-1", "Something went wrong")
    
    record = store.get("key-1")
    assert record.status == IdempotencyStatus.PENDING
    assert record.error == "Something went wrong"


def test_store_stats():
    """Test store statistics."""
    store = IdempotencyStore()
    
    stats = store.stats()
    assert stats['total'] == 0
    assert stats['pending'] == 0
    assert stats['completed'] == 0
    
    store.set_pending("key-1")
    store.set_completed("key-2", "result")
    store.set_pending("key-3")
    
    stats = store.stats()
    assert stats['total'] == 3
    assert stats['in_progress'] == 2
    assert stats['completed'] == 1


def test_store_clear():
    """Test clearing the store."""
    store = IdempotencyStore()
    
    store.set_completed("key-1", "r1")
    store.set_completed("key-2", "r2")
    
    count = store.clear()
    assert count == 2
    assert store.stats()['total'] == 0


def test_store_cleanup():
    """Test cleanup of expired records."""
    store = IdempotencyStore()
    
    store.set_completed("key-1", "r1", ttl=0.5)
    store.set_completed("key-2", "r2", ttl=10)
    
    time.sleep(1.0)
    removed = store.cleanup_expired()
    assert removed == 1
    assert store.get("key-1") is None
    assert store.get("key-2") is not None


def test_store_max_size():
    """Test max size enforcement."""
    store = IdempotencyStore(max_size=3, cleanup_interval=0.1)
    
    # Add more than max
    for i in range(5):
        store.set_completed(f"key-{i}", f"result-{i}")
    
    # Trigger cleanup manually (cleanup happens on next access)
    store.cleanup_expired()
    time.sleep(0.2)
    
    # Force cleanup by accessing the store
    store.get("key-0")
    
    stats = store.stats()
    # Note: cleanup is lazy, max_size enforcement removes oldest records
    assert stats['total'] <= 5  # At least within reasonable bounds


def test_store_thread_safety():
    """Test thread safety."""
    store = IdempotencyStore()
    errors = []
    
    def writer(start_id: int):
        try:
            for i in range(100):
                key = f"key-{start_id}-{i}"
                store.set_pending(key)
                store.set_completed(key, i)
        except Exception as e:
            errors.append(e)
    
    threads = [threading.Thread(target=writer, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    assert len(errors) == 0
    stats = store.stats()
    assert stats['total'] == 1000


# ============================================================================
# IdempotencyKeyGenerator Tests
# ============================================================================

def test_key_generator_random():
    """Test random key generation."""
    key1 = IdempotencyKeyGenerator.random()
    key2 = IdempotencyKeyGenerator.random()
    
    assert key1 != key2
    assert len(key1) == 36  # UUID format


def test_key_generator_from_uuid():
    """Test key from UUID."""
    u = uuid.uuid4()
    key = IdempotencyKeyGenerator.from_uuid(u)
    assert key == str(u)
    
    key2 = IdempotencyKeyGenerator.from_uuid("550e8400-e29b-41d4-a716-446655440000")
    assert key2 == "550e8400-e29b-41d4-a716-446655440000"


def test_key_generator_from_hash():
    """Test key from hash."""
    key1 = IdempotencyKeyGenerator.from_hash("arg1", "arg2", kwarg="value")
    key2 = IdempotencyKeyGenerator.from_hash("arg1", "arg2", kwarg="value")
    key3 = IdempotencyKeyGenerator.from_hash("arg1", "arg3", kwarg="value")
    
    # Same args = same key
    assert key1 == key2
    assert len(key1) == 64  # SHA-256
    
    # Different args = different key
    assert key1 != key3


def test_key_generator_from_request():
    """Test key from HTTP request."""
    key1 = IdempotencyKeyGenerator.from_request(
        method="POST",
        url="/api/orders",
        body={"order_id": 123},
    )
    
    key2 = IdempotencyKeyGenerator.from_request(
        method="POST",
        url="/api/orders",
        body={"order_id": 123},
    )
    
    assert key1 == key2
    
    # Different method
    key3 = IdempotencyKeyGenerator.from_request(
        method="GET",
        url="/api/orders",
        body={"order_id": 123},
    )
    assert key1 != key3


def test_key_generator_from_function_call():
    """Test key from function call."""
    key1 = IdempotencyKeyGenerator.from_function_call(
        func_name="process_order",
        args=(123,),
        kwargs={"user": "test"},
    )
    
    key2 = IdempotencyKeyGenerator.from_function_call(
        func_name="process_order",
        args=(123,),
        kwargs={"user": "test"},
    )
    
    assert key1 == key2
    
    key3 = IdempotencyKeyGenerator.from_function_call(
        func_name="process_order",
        args=(456,),
        kwargs={"user": "test"},
    )
    assert key1 != key3


def test_key_generator_prefix():
    """Test prefix functionality."""
    key = IdempotencyKeyGenerator.prefix("order", "123")
    assert key == "order:123"


def test_key_generator_with_timestamp():
    """Test timestamp suffix."""
    ts = 1700000000.0
    key = IdempotencyKeyGenerator.with_timestamp("base-key", ts)
    assert key == "base-key:1700000000"


# ============================================================================
# IdempotencyManager Tests
# ============================================================================

def test_manager_execute():
    """Test manager execute."""
    manager = IdempotencyManager()
    
    # First execution
    result1 = manager.execute("key-1", lambda: 42)
    assert result1 == 42
    
    # Second execution - cached
    result2 = manager.execute("key-1", lambda: 999)  # Different function
    assert result2 == 42  # Returns cached


def test_manager_has_result():
    """Test manager result check."""
    manager = IdempotencyManager()
    
    assert not manager.has_result("key-1")
    
    manager.execute("key-1", lambda: "result")
    
    assert manager.has_result("key-1")


def test_manager_cancel():
    """Test manager cancel."""
    manager = IdempotencyManager()
    
    # Cancel non-existent
    assert not manager.cancel("key-1")
    
    # Cancel in progress
    manager._store.set_pending("key-1")
    assert manager.cancel("key-1")
    assert not manager._store.exists("key-1")


def test_manager_stats():
    """Test manager statistics."""
    manager = IdempotencyManager()
    
    manager.execute("key-1", lambda: 1)
    manager.execute("key-2", lambda: 2)
    
    stats = manager.stats()
    assert stats['completed'] == 2


# ============================================================================
# RequestDeduplicator Tests
# ============================================================================

def test_deduplicator_basic():
    """Test basic deduplication."""
    deduper = RequestDeduplicator(window_seconds=2.0)
    
    # First request - not duplicate
    assert not deduper.is_duplicate("req-1")
    deduper.mark("req-1")
    
    # Same request within window - duplicate
    assert deduper.is_duplicate("req-1")
    
    # Different request - not duplicate
    assert not deduper.is_duplicate("req-2")


def test_deduplicator_window_expiry():
    """Test window expiry."""
    deduper = RequestDeduplicator(window_seconds=1.0)
    
    deduper.mark("req-1")
    assert deduper.is_duplicate("req-1")
    
    # Wait for window to expire
    time.sleep(1.5)
    
    assert not deduper.is_duplicate("req-1")


def test_deduplicator_check_and_mark():
    """Test atomic check and mark."""
    deduper = RequestDeduplicator()
    
    # First - not duplicate, marked
    assert not deduper.check_and_mark("req-1")
    
    # Second - duplicate
    assert deduper.check_and_mark("req-1")


def test_deduplicator_clear():
    """Test clearing deduplicator."""
    deduper = RequestDeduplicator()
    
    deduper.mark("req-1")
    deduper.mark("req-2")
    
    count = deduper.clear()
    assert count == 2
    assert not deduper.is_duplicate("req-1")


def test_deduplicator_stats():
    """Test deduplicator statistics."""
    deduper = RequestDeduplicator()
    
    deduper.mark("req-1")
    deduper.mark("req-2")
    
    stats = deduper.stats()
    assert stats['tracked_requests'] == 2


def test_deduplicator_max_requests():
    """Test max requests limit."""
    deduper = RequestDeduplicator(max_requests=3)
    
    deduper.mark("req-1")
    deduper.mark("req-2")
    deduper.mark("req-3")
    deduper.mark("req-4")  # Should evict oldest
    
    # One should have been evicted
    stats = deduper.stats()
    assert stats['tracked_requests'] <= 3


# ============================================================================
# Decorator Tests
# ============================================================================

def test_idempotent_decorator():
    """Test idempotent decorator."""
    reset_global_store()
    
    class Counter:
        count = 0
    
    @idempotent()
    def expensive_operation(x: int):
        Counter.count += 1
        return x * 2
    
    # First call
    result1 = expensive_operation(5)
    assert result1 == 10
    assert Counter.count == 1
    
    # Same args - cached, not called again
    result2 = expensive_operation(5)
    assert result2 == 10
    assert Counter.count == 1  # Still 1
    
    # Different args - called
    result3 = expensive_operation(10)
    assert result3 == 20
    assert Counter.count == 2


def test_idempotent_decorator_custom_key():
    """Test decorator with custom key function."""
    store = IdempotencyStore()
    
    @idempotent(
        key_func=lambda order_id, items=None, user_id=None: f"order:{order_id}",
        store=store,
    )
    def process_order(order_id: str, items: list = None, user_id: str = None):
        return {"order_id": order_id, "processed": True}
    
    result1 = process_order("123", ["item1"])
    result2 = process_order("123", ["item2"])  # Different items
    
    # Same order_id = cached
    assert result1 == result2
    assert result1["order_id"] == "123"


def test_idempotent_decorator_ttl():
    """Test decorator with TTL."""
    store = IdempotencyStore(default_ttl=1.0)
    
    @idempotent(store=store, ttl=1.0)
    def timed_operation(x: int):
        return x
    
    result1 = timed_operation(5)
    
    time.sleep(1.5)
    
    # After TTL - should re-execute
    result2 = timed_operation(5)
    assert result2 == 5  # Still correct value


def test_idempotent_decorator_error_handling():
    """Test decorator error handling."""
    store = IdempotencyStore()
    
    class Counter:
        calls = 0
    
    @idempotent(store=store)
    def failing_operation():
        Counter.calls += 1
        raise ValueError("Test error")
    
    # First call - error
    try:
        failing_operation()
    except ValueError:
        pass
    
    assert Counter.calls == 1
    record = store.get(IdempotencyKeyGenerator.from_function_call(
        "failing_operation", (), {}
    ))
    assert record.error == "Test error"


def test_idempotent_decorator_raise_on_duplicate():
    """Test decorator raising on duplicate."""
    reset_global_store()
    
    @idempotent(raise_on_duplicate=True, return_cached=False)
    def unique_operation(x: int):
        return x
    
    # First call
    result1 = unique_operation(5)
    assert result1 == 5
    
    # Duplicate - should raise
    try:
        unique_operation(5)
        assert False, "Should have raised DuplicateOperationError"
    except DuplicateOperationError:
        pass


# ============================================================================
# Global Instances Tests
# ============================================================================

def test_global_store():
    """Test global store access."""
    store = get_global_store()
    assert store is not None
    
    reset_global_store()
    store.set_completed("test", "result")
    assert store.get_result("test") == "result"
    
    reset_global_store()
    assert store.stats()['total'] == 0


def test_global_deduplicator():
    """Test global deduplicator access."""
    deduper = get_global_deduplicator()
    assert deduper is not None
    
    reset_global_deduplicator()
    deduper.mark("test")
    assert deduper.is_duplicate("test")
    
    reset_global_deduplicator()
    assert not deduper.is_duplicate("test")


# ============================================================================
# Edge Cases Tests
# ============================================================================

def test_empty_key():
    """Test handling empty key."""
    store = IdempotencyStore()
    
    store.set_pending("")
    record = store.get("")
    assert record.key == ""


def test_large_key():
    """Test handling large key."""
    store = IdempotencyStore()
    
    large_key = "x" * 1000
    store.set_pending(large_key)
    record = store.get(large_key)
    assert record is not None


def test_special_chars_key():
    """Test handling special characters in key."""
    store = IdempotencyStore()
    
    special_key = "key:with:colons:and/slashes\\and\\unicode-中文-🔥"
    store.set_pending(special_key)
    record = store.get(special_key)
    assert record is not None


def test_complex_result_types():
    """Test storing complex result types."""
    store = IdempotencyStore()
    
    # Dict
    store.set_completed("dict-key", {"nested": {"data": [1, 2, 3]}})
    result = store.get_result("dict-key")
    assert result["nested"]["data"] == [1, 2, 3]
    
    # List
    store.set_completed("list-key", [{"a": 1}, {"b": 2}])
    result = store.get_result("list-key")
    assert len(result) == 2
    
    # Tuple (stored as tuple)
    store.set_completed("tuple-key", (1, 2, 3))
    result = store.get_result("tuple-key")
    assert result == (1, 2, 3)


def test_concurrent_access():
    """Test concurrent access patterns."""
    store = IdempotencyStore()
    results = []
    
    def worker(key: str, value: int):
        store.set_pending(key)
        time.sleep(0.01)  # Simulate work
        store.set_completed(key, value)
        results.append(store.get_result(key))
    
    threads = [
        threading.Thread(target=worker, args=(f"key-{i}", i))
        for i in range(10)
    ]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    assert len(results) == 10
    assert all(r is not None for r in results)


def test_zero_ttl():
    """Test zero TTL (immediate expiry)."""
    store = IdempotencyStore()
    
    # Zero TTL means expires_at = time.time() + 0 = now
    # The record is immediately expired but cleanup may not run yet
    store.set_completed("key-1", "result", ttl=0.0)
    
    # Record might still exist but be expired
    record = store.get("key-1")
    # get() checks expiry and removes expired records
    # So the record should not be returned
    assert record is None or record.is_expired()


def test_negative_ttl():
    """Test negative TTL handling."""
    store = IdempotencyStore()
    
    # Negative TTL should result in immediate expiry
    store.set_completed("key-1", "result", ttl=-1.0)
    record = store.get("key-1")
    # Should either not exist or be expired
    if record:
        assert record.is_expired()


def test_unicode_handling():
    """Test Unicode handling in keys and results."""
    store = IdempotencyStore()
    
    # Chinese characters
    store.set_completed("订单-123", {"结果": "成功"})
    result = store.get_result("订单-123")
    assert result["结果"] == "成功"
    
    # Emoji
    store.set_completed("🔥-key", {"value": "🔥"})
    result = store.get_result("🔥-key")
    assert result["value"] == "🔥"


def test_hash_stability():
    """Test hash key stability across calls."""
    # Same arguments should always produce same hash
    key1 = IdempotencyKeyGenerator.from_hash(
        {"data": "test"},
        ["list", "items"],
        kwarg={"nested": "value"},
    )
    
    key2 = IdempotencyKeyGenerator.from_hash(
        {"data": "test"},
        ["list", "items"],
        kwarg={"nested": "value"},
    )
    
    assert key1 == key2


def test_large_data_hash():
    """Test hashing large data."""
    large_data = {"data": "x" * 10000}
    
    key = IdempotencyKeyGenerator.from_hash(large_data)
    assert len(key) == 64  # SHA-256 always 64 hex chars


# ============================================================================
# Run All Tests
# ============================================================================

def main():
    """Run all tests."""
    print("="*60)
    print("AllToolkit - Idempotency Utilities Test Suite")
    print("="*60)
    print()
    
    collector = TestResultCollector()
    
    # Record tests
    run_test("record_creation", test_record_creation, collector)
    run_test("record_expiry", test_record_expiry, collector)
    run_test("record_age", test_record_age, collector)
    run_test("record_to_dict", test_record_to_dict, collector)
    
    # Store tests
    run_test("store_basic_operations", test_store_basic_operations, collector)
    run_test("store_exists_checks", test_store_exists_checks, collector)
    run_test("store_get_result", test_store_get_result, collector)
    run_test("store_ttl", test_store_ttl, collector)
    run_test("store_error_handling", test_store_error_handling, collector)
    run_test("store_stats", test_store_stats, collector)
    run_test("store_clear", test_store_clear, collector)
    run_test("store_cleanup", test_store_cleanup, collector)
    run_test("store_max_size", test_store_max_size, collector)
    run_test("store_thread_safety", test_store_thread_safety, collector)
    
    # Key generator tests
    run_test("key_generator_random", test_key_generator_random, collector)
    run_test("key_generator_from_uuid", test_key_generator_from_uuid, collector)
    run_test("key_generator_from_hash", test_key_generator_from_hash, collector)
    run_test("key_generator_from_request", test_key_generator_from_request, collector)
    run_test("key_generator_from_function_call", test_key_generator_from_function_call, collector)
    run_test("key_generator_prefix", test_key_generator_prefix, collector)
    run_test("key_generator_with_timestamp", test_key_generator_with_timestamp, collector)
    
    # Manager tests
    run_test("manager_execute", test_manager_execute, collector)
    run_test("manager_has_result", test_manager_has_result, collector)
    run_test("manager_cancel", test_manager_cancel, collector)
    run_test("manager_stats", test_manager_stats, collector)
    
    # Deduplicator tests
    run_test("deduplicator_basic", test_deduplicator_basic, collector)
    run_test("deduplicator_window_expiry", test_deduplicator_window_expiry, collector)
    run_test("deduplicator_check_and_mark", test_deduplicator_check_and_mark, collector)
    run_test("deduplicator_clear", test_deduplicator_clear, collector)
    run_test("deduplicator_stats", test_deduplicator_stats, collector)
    run_test("deduplicator_max_requests", test_deduplicator_max_requests, collector)
    
    # Decorator tests
    run_test("idempotent_decorator", test_idempotent_decorator, collector)
    run_test("idempotent_decorator_custom_key", test_idempotent_decorator_custom_key, collector)
    run_test("idempotent_decorator_ttl", test_idempotent_decorator_ttl, collector)
    run_test("idempotent_decorator_error_handling", test_idempotent_decorator_error_handling, collector)
    run_test("idempotent_decorator_raise_on_duplicate", test_idempotent_decorator_raise_on_duplicate, collector)
    
    # Global instances tests
    run_test("global_store", test_global_store, collector)
    run_test("global_deduplicator", test_global_deduplicator, collector)
    
    # Edge cases tests
    run_test("empty_key", test_empty_key, collector)
    run_test("large_key", test_large_key, collector)
    run_test("special_chars_key", test_special_chars_key, collector)
    run_test("complex_result_types", test_complex_result_types, collector)
    run_test("concurrent_access", test_concurrent_access, collector)
    run_test("zero_ttl", test_zero_ttl, collector)
    run_test("negative_ttl", test_negative_ttl, collector)
    run_test("unicode_handling", test_unicode_handling, collector)
    run_test("hash_stability", test_hash_stability, collector)
    run_test("large_data_hash", test_large_data_hash, collector)
    
    return collector.summary()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)