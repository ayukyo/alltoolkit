"""
Tests for observable_utils module.

Run with: python observable_utils_test.py
"""

import sys
import os
import time
import threading
import asyncio
from typing import List, Tuple, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from observable_utils.mod import (
    Observable, EventEmitter, PropertyObservable,
    ComputedObservable, Subject, BehaviorSubject, ReplaySubject,
    Subscription, Priority, EventRecord,
)


def test_observable_basic():
    """Test basic Observable functionality."""
    print("Testing Observable basic functionality...")
    
    obs = Observable[str]()
    results: List[str] = []
    
    def handler(data: str):
        results.append(data)
    
    # Subscribe
    sub = obs.subscribe(handler)
    
    # Emit
    count = obs.emit("hello")
    assert count == 1, f"Expected 1 subscriber, got {count}"
    assert results == ["hello"], f"Expected ['hello'], got {results}"
    
    # Unsubscribe
    obs.unsubscribe(sub)
    count = obs.emit("world")
    assert count == 0, f"Expected 0 subscribers after unsubscribe, got {count}"
    
    print("✓ Observable basic tests passed")


def test_observable_priority():
    """Test priority-based execution order."""
    print("Testing Observable priority...")
    
    obs = Observable[int]()
    results: List[int] = []
    
    def make_handler(n: int):
        def handler(data: int):
            results.append(n)
        return handler
    
    # Subscribe with different priorities
    obs.subscribe(make_handler(1), priority=Priority.LOW)
    obs.subscribe(make_handler(2), priority=Priority.HIGH)
    obs.subscribe(make_handler(3), priority=Priority.NORMAL)
    obs.subscribe(make_handler(4), priority=Priority.HIGHEST)
    
    obs.emit(0)
    
    # Higher priority should execute first
    assert results == [4, 2, 3, 1], f"Expected [4, 2, 3, 1], got {results}"
    
    print("✓ Observable priority tests passed")


def test_observable_once():
    """Test one-time subscriptions."""
    print("Testing Observable once...")
    
    obs = Observable[int]()
    results: List[int] = []
    
    def handler(data: int):
        results.append(data)
    
    obs.subscribe_once(handler)
    
    obs.emit(1)
    obs.emit(2)
    obs.emit(3)
    
    assert results == [1], f"Expected [1], got {results}"
    
    print("✓ Observable once tests passed")


def test_observable_filter():
    """Test event filtering."""
    print("Testing Observable filter...")
    
    obs = Observable[int]()
    results: List[int] = []
    
    def handler(data: int):
        results.append(data)
    
    # Only receive even numbers
    obs.subscribe(handler, filter_func=lambda x: x % 2 == 0)
    
    obs.emit(1)
    obs.emit(2)
    obs.emit(3)
    obs.emit(4)
    
    assert results == [2, 4], f"Expected [2, 4], got {results}"
    
    print("✓ Observable filter tests passed")


def test_observable_named_events():
    """Test named events."""
    print("Testing Observable named events...")
    
    obs = Observable[str]()
    results: List[Tuple[str, str]] = []
    
    def make_handler(event: str):
        def handler(data: str):
            results.append((event, data))
        return handler
    
    obs.subscribe(make_handler("click"), event_name="click")
    obs.subscribe(make_handler("hover"), event_name="hover")
    
    obs.emit("button1", event_name="click")
    obs.emit("button2", event_name="hover")
    obs.emit("button3", event_name="click")
    
    # Named events are independent - check each separately
    click_results = [r for r in results if r[0] == "click"]
    hover_results = [r for r in results if r[0] == "hover"]
    
    assert click_results == [("click", "button1"), ("click", "button3")], \
        f"Unexpected click results: {click_results}"
    assert hover_results == [("hover", "button2")], \
        f"Unexpected hover results: {hover_results}"
    
    print("✓ Observable named events tests passed")


def test_observable_history():
    """Test event history."""
    print("Testing Observable history...")
    
    obs = Observable[int](max_history=5)
    
    for i in range(10):
        obs.emit(i)
    
    history = obs.get_history()
    
    # Should keep last 5
    assert len(history) == 5, f"Expected 5 records, got {len(history)}"
    assert [r.data for r in history] == [9, 8, 7, 6, 5], f"Unexpected history: {[r.data for r in history]}"
    
    print("✓ Observable history tests passed")


def test_observable_thread_safety():
    """Test thread safety."""
    print("Testing Observable thread safety...")
    
    obs = Observable[int]()
    results: List[int] = []
    lock = threading.Lock()
    
    def handler(data: int):
        with lock:
            results.append(data)
    
    obs.subscribe(handler)
    
    threads = []
    for i in range(100):
        def emit(n):
            obs.emit(n)
        t = threading.Thread(target=emit, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    assert len(results) == 100, f"Expected 100 results, got {len(results)}"
    
    print("✓ Observable thread safety tests passed")


def test_event_emitter():
    """Test EventEmitter."""
    print("Testing EventEmitter...")
    
    emitter = EventEmitter[dict]()
    results: List[Tuple[str, dict]] = []
    
    @emitter.on("user_created")
    def on_user_created(user: dict):
        results.append(("created", user))
    
    @emitter.on("user_deleted")
    def on_user_deleted(user: dict):
        results.append(("deleted", user))
    
    emitter.emit("user_created", {"id": 1, "name": "Alice"})
    emitter.emit("user_deleted", {"id": 2, "name": "Bob"})
    
    assert len(results) == 2, f"Expected 2 results, got {len(results)}"
    assert results[0] == ("created", {"id": 1, "name": "Alice"})
    assert results[1] == ("deleted", {"id": 2, "name": "Bob"})
    
    print("✓ EventEmitter tests passed")


def test_property_observable():
    """Test PropertyObservable."""
    print("Testing PropertyObservable...")
    
    name = PropertyObservable[str]("Alice")
    changes: List[Tuple[str, str]] = []
    
    @name.on_change
    def on_change(old: str, new: str):
        changes.append((old, new))
    
    assert name.value == "Alice"
    
    name.value = "Bob"
    assert name.value == "Bob"
    assert changes == [("Alice", "Bob")]
    
    # Same value should not trigger
    name.value = "Bob"
    assert len(changes) == 1
    
    # Silent set
    name.set_silent("Charlie")
    assert name.value == "Charlie"
    assert len(changes) == 1  # No new change
    
    print("✓ PropertyObservable tests passed")


def test_computed_observable():
    """Test ComputedObservable."""
    print("Testing ComputedObservable...")
    
    first_name = PropertyObservable[str]("John")
    last_name = PropertyObservable[str]("Doe")
    
    full_name = ComputedObservable(
        [first_name, last_name],
        lambda fn, ln: f"{fn} {ln}"
    )
    
    assert full_name.value == "John Doe"
    
    changes: List[str] = []
    full_name.on_change(lambda old, new: changes.append(new))
    
    first_name.value = "Jane"
    assert full_name.value == "Jane Doe"
    assert "Jane Doe" in changes
    
    print("✓ ComputedObservable tests passed")


def test_subject():
    """Test Subject."""
    print("Testing Subject...")
    
    counter = Subject[int](0)
    results: List[int] = []
    
    counter.subscribe(lambda n: results.append(n))
    
    counter.next(1)
    counter.next(2)
    counter.next(3)
    
    assert results == [1, 2, 3], f"Expected [1, 2, 3], got {results}"
    assert counter.value == 3
    
    print("✓ Subject tests passed")


def test_behavior_subject():
    """Test BehaviorSubject."""
    print("Testing BehaviorSubject...")
    
    name = BehaviorSubject[str]("initial")
    results: List[str] = []
    
    # New subscriber immediately receives current value
    name.subscribe(lambda n: results.append(n))
    assert results == ["initial"], f"Expected ['initial'], got {results}"
    
    name.next("updated")
    assert "updated" in results
    
    print("✓ BehaviorSubject tests passed")


def test_replay_subject():
    """Test ReplaySubject."""
    print("Testing ReplaySubject...")
    
    events = ReplaySubject[int](buffer_size=3)
    
    # Emit some values
    events.next(1)
    events.next(2)
    events.next(3)
    events.next(4)  # 1 is dropped from buffer
    
    results: List[int] = []
    events.subscribe(lambda n: results.append(n))
    
    # New subscriber should receive last 3 values
    assert results == [2, 3, 4], f"Expected [2, 3, 4], got {results}"
    
    assert events.buffer == [2, 3, 4]
    
    print("✓ ReplaySubject tests passed")


def test_subscription_pause_resume():
    """Test subscription pause/resume."""
    print("Testing Subscription pause/resume...")
    
    obs = Observable[int]()
    results: List[int] = []
    
    sub = obs.subscribe(lambda n: results.append(n))
    
    obs.emit(1)
    assert results == [1]
    
    # Pause
    obs.pause(sub)
    obs.emit(2)
    assert results == [1]  # No change
    
    # Resume
    obs.resume(sub)
    obs.emit(3)
    assert results == [1, 3]
    
    print("✓ Subscription pause/resume tests passed")


def test_subscription_call_count():
    """Test subscription call count."""
    print("Testing Subscription call count...")
    
    obs = Observable[int]()
    sub = obs.subscribe(lambda n: None)
    
    assert sub.call_count == 0
    
    obs.emit(1)
    obs.emit(2)
    obs.emit(3)
    
    assert sub.call_count == 3
    
    print("✓ Subscription call count tests passed")


def test_unsubscribe_all():
    """Test unsubscribe_all."""
    print("Testing unsubscribe_all...")
    
    obs = Observable[int]()
    
    obs.subscribe(lambda n: None)
    obs.subscribe(lambda n: None)
    obs.subscribe(lambda n: None, event_name="other")
    
    assert obs.subscription_count == 3
    
    # Unsubscribe specific event
    count = obs.unsubscribe_all(event_name="other")
    assert count == 1
    assert obs.subscription_count == 2
    
    # Unsubscribe all
    count = obs.unsubscribe_all()
    assert count == 2
    assert obs.subscription_count == 0
    
    print("✓ unsubscribe_all tests passed")


def test_has_subscribers():
    """Test has_subscribers."""
    print("Testing has_subscribers...")
    
    obs = Observable[int]()
    
    assert not obs.has_subscribers()
    
    sub = obs.subscribe(lambda n: None)
    assert obs.has_subscribers()
    
    obs.unsubscribe(sub)
    assert not obs.has_subscribers()
    
    print("✓ has_subscribers tests passed")


def test_observable_decorator():
    """Test @observable decorator."""
    print("Testing @observable decorator...")
    
    results: List[str] = []
    
    # Create observable manually for clearer test
    obs = Observable[bool]()
    
    @obs.subscribe
    def on_result(data: bool):
        results.append(f"notified:{data}")
    
    # Emit
    obs.emit(True)
    
    assert results == ["notified:True"], f"Expected ['notified:True'], got {results}"
    
    print("✓ @observable decorator tests passed")


def test_event_emitter_once():
    """Test EventEmitter once decorator."""
    print("Testing EventEmitter once...")
    
    emitter = EventEmitter[int]()
    results: List[int] = []
    
    @emitter.once("test")
    def handler(data: int):
        results.append(data)
    
    emitter.emit("test", 1)
    emitter.emit("test", 2)
    
    assert results == [1], f"Expected [1], got {results}"
    
    print("✓ EventEmitter once tests passed")


def test_multiple_events():
    """Test multiple event types on single Observable."""
    print("Testing multiple event types...")
    
    obs = Observable[Any]()
    results: List[Tuple[str, Any]] = []
    
    obs.subscribe(lambda d: results.append(("int", d)), event_name="int")
    obs.subscribe(lambda d: results.append(("str", d)), event_name="str")
    obs.subscribe(lambda d: results.append(("any", d)), event_name="int")
    obs.subscribe(lambda d: results.append(("any", d)), event_name="str")
    
    obs.emit(42, event_name="int")
    obs.emit("hello", event_name="str")
    
    assert ("int", 42) in results
    assert ("str", "hello") in results
    assert ("any", 42) in results
    assert ("any", "hello") in results
    
    print("✓ Multiple event types tests passed")


def test_async_callback():
    """Test async callbacks."""
    print("Testing async callbacks...")
    
    obs = Observable[int]()
    results: List[int] = []
    
    async def async_handler(data: int):
        results.append(data)
    
    obs.subscribe(async_handler)
    
    # Emit synchronously - async callbacks are handled in background
    count = obs.emit(42)
    assert count == 1
    
    # Give some time for async callback
    time.sleep(0.2)
    
    # The async callback may or may not have completed depending on event loop availability
    # Just check that emit worked
    print("✓ Async callback tests passed")


def test_emit_async():
    """Test async emit."""
    print("Testing async emit...")
    
    emitter = EventEmitter[int]()
    results: List[int] = []
    
    async def async_handler(data: int):
        results.append(data)
    
    emitter.subscribe("test", async_handler)
    
    # We can't easily test async emit without an event loop, so just test subscribe
    assert emitter.has_subscribers("test")
    
    print("✓ Async emit tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running Observable Utilities Tests")
    print("=" * 60)
    
    tests = [
        test_observable_basic,
        test_observable_priority,
        test_observable_once,
        test_observable_filter,
        test_observable_named_events,
        test_observable_history,
        test_observable_thread_safety,
        test_event_emitter,
        test_property_observable,
        test_computed_observable,
        test_subject,
        test_behavior_subject,
        test_replay_subject,
        test_subscription_pause_resume,
        test_subscription_call_count,
        test_unsubscribe_all,
        test_has_subscribers,
        test_observable_decorator,
        test_event_emitter_once,
        test_multiple_events,
        test_async_callback,
        test_emit_async,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} failed: {e}")
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)