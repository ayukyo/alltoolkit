#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Event Emitter Utilities Test Suite
================================================
Comprehensive test suite for the event emitter module.
"""

import sys
import os
import time
import threading
import asyncio

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    EventEmitter, EventBus, Listener, EventRecord,
    create_emitter, create_channel,
    emits_event, on_event
)


class TestRunner:
    """Simple test runner with reporting."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, name: str, condition: bool, error_msg: str = ""):
        """Run a single test."""
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            self.errors.append((name, error_msg))
            print(f"  ✗ {name}")
            if error_msg:
                print(f"    Error: {error_msg}")
    
    def report(self) -> bool:
        """Print test report and return success status."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}")
        
        if self.errors:
            print(f"\nFailed tests:")
            for name, msg in self.errors:
                print(f"  - {name}: {msg}")
        
        if self.failed == 0:
            print("✓ All tests passed!")
        else:
            print(f"✗ {self.failed} test(s) failed.")
        print('='*60)
        return self.failed == 0


def run_basic_tests(runner: TestRunner):
    """Test basic event emission and listening."""
    print("\nBasic Event Tests")
    print("-" * 60)
    
    emitter = EventEmitter()
    received_data = []
    
    def handler(data):
        received_data.append(data)
    
    # Test listener registration
    listener = emitter.on("test.event", handler)
    runner.test("on() returns Listener object", isinstance(listener, Listener))
    runner.test("Listener has correct callback", listener.callback == handler)
    
    # Test event emission
    emitter.emit("test.event", {"key": "value"})
    runner.test("Event triggers listener", len(received_data) == 1)
    runner.test("Listener receives correct data", received_data[0] == {"key": "value"})
    
    # Test multiple emissions
    emitter.emit("test.event", "second")
    emitter.emit("test.event", "third")
    runner.test("Multiple emissions work", len(received_data) == 3)
    
    # Test listener count
    runner.test("has_listener returns True", emitter.has_listener("test.event"))
    runner.test("has_listener returns False for unknown", not emitter.has_listener("unknown"))


def run_once_tests(runner: TestRunner):
    """Test once-only listeners."""
    print("\nOnce-Only Listener Tests")
    print("-" * 60)
    
    emitter = EventEmitter()
    call_count = [0]
    
    def once_handler(data):
        call_count[0] += 1
    
    emitter.once("once.event", once_handler)
    
    emitter.emit("once.event", "first")
    emitter.emit("once.event", "second")
    emitter.emit("once.event", "third")
    
    runner.test("Once listener called once", call_count[0] == 1)
    runner.test("Listener removed after call", emitter.get_listener_count("once.event") == 0)


def run_wildcard_tests(runner: TestRunner):
    """Test wildcard pattern matching."""
    print("\nWildcard Pattern Tests")
    print("-" * 60)
    
    emitter = EventEmitter()
    events = []
    
    def single_wildcard(event, data):
        events.append(("single", event, data))
    
    def double_wildcard(event, data):
        events.append(("double", event, data))
    
    emitter.on("user.*", single_wildcard)
    emitter.on("data.**", double_wildcard)
    
    # Single wildcard - matches one level
    emitter.emit("user.created", {"id": 1})
    emitter.emit("user.deleted", {"id": 2})
    emitter.emit("user.profile.updated", {"id": 3})  # Should NOT match single *
    
    runner.test("Single * matches one level", len([e for e in events if e[0] == "single"]) == 2)
    
    # Double wildcard - matches all levels
    emitter.emit("data.users.sync", {"count": 100})
    emitter.emit("data.config.changed", {"key": "value"})
    
    double_events = [e for e in events if e[0] == "double"]
    runner.test("Double ** matches all levels", len(double_events) == 2)
    
    # Test exact match priority
    exact_called = [False]
    emitter.on("exact.event", lambda d: exact_called.__setitem__(0, True))
    emitter.emit("exact.event")
    runner.test("Exact match works", exact_called[0])


def run_priority_tests(runner: TestRunner):
    """Test listener priority ordering."""
    print("\nPriority Ordering Tests")
    print("-" * 60)
    
    emitter = EventEmitter()
    order = []
    
    emitter.on("priority.test", lambda d: order.append(3), priority=0)
    emitter.on("priority.test", lambda d: order.append(1), priority=10)
    emitter.on("priority.test", lambda d: order.append(2), priority=5)
    
    emitter.emit("priority.test")
    
    runner.test("High priority called first", order == [1, 2, 3])


def run_removal_tests(runner: TestRunner):
    """Test listener removal."""
    print("\nListener Removal Tests")
    print("-" * 60)
    
    emitter = EventEmitter()
    calls = {"a": 0, "b": 0}
    
    def handler_a(data):
        calls["a"] += 1
    
    def handler_b(data):
        calls["b"] += 1
    
    emitter.on("remove.test", handler_a)
    emitter.on("remove.test", handler_b)
    
    emitter.emit("remove.test")
    runner.test("Both handlers called initially", calls["a"] == 1 and calls["b"] == 1)
    
    # Remove specific handler
    emitter.off("remove.test", handler_a)
    calls["a"] = 0
    calls["b"] = 0
    emitter.emit("remove.test")
    runner.test("Specific handler removed", calls["a"] == 0 and calls["b"] == 1)
    
    # Remove all handlers
    emitter.off("remove.test")
    runner.test("All handlers removed", emitter.get_listener_count("remove.test") == 0)
    
    # Remove all events
    emitter.on("event1", lambda: None)
    emitter.on("event2", lambda: None)
    emitter.off("*")
    runner.test("Wildcard off removes all", emitter.listener_count == 0)


def run_history_tests(runner: TestRunner):
    """Test event history and replay."""
    print("\nEvent History Tests")
    print("-" * 60)
    
    emitter = EventEmitter(max_history=5)
    
    for i in range(10):
        emitter.emit("log.event", f"message_{i}")
    
    history = emitter.get_history("log.event", limit=10)
    runner.test("History limited to max_history", len(history) == 5)
    runner.test("History contains latest events", history[0].data == "message_5")
    
    # Test replay
    replayed = []
    emitter.replay("log.event", lambda d: replayed.append(d))
    runner.test("Replay replays all history", len(replayed) == 5)
    
    # Test clear history
    emitter.clear_history("log.event")
    runner.test("Clear history works", len(emitter.get_history("log.event")) == 0)


def run_pause_resume_tests(runner: TestRunner):
    """Test event pause/resume functionality."""
    print("\nPause/Resume Tests")
    print("-" * 60)
    
    emitter = EventEmitter()
    called = [False]
    
    emitter.on("paused.event", lambda d: called.__setitem__(0, True))
    
    emitter.pause("paused.event")
    runner.test("Event is paused", emitter.is_paused("paused.event"))
    
    emitter.emit("paused.event")
    runner.test("Paused event not triggered", not called[0])
    
    emitter.resume("paused.event")
    runner.test("Event is resumed", not emitter.is_paused("paused.event"))
    
    emitter.emit("paused.event")
    runner.test("Resumed event triggered", called[0])


def run_introspection_tests(runner: TestRunner):
    """Test emitter introspection."""
    print("\nIntrospection Tests")
    print("-" * 60)
    
    emitter = EventEmitter()
    
    emitter.on("event1", lambda: None, priority=5)
    emitter.on("event1", lambda: None, priority=10)
    emitter.on("event2", lambda: None)
    
    runner.test("get_events returns all events", len(emitter.get_events()) == 2)
    runner.test("get_listener_count correct", emitter.get_listener_count("event1") == 2)
    runner.test("listener_count property correct", emitter.listener_count == 3)
    runner.test("event_count property correct", emitter.event_count == 2)
    
    stats = emitter.get_stats()
    runner.test("Stats has required fields", 
                all(k in stats for k in ["id", "event_count", "total_listeners"]))


def run_channel_tests(runner: TestRunner):
    """Test channel creation."""
    print("\nChannel Tests")
    print("-" * 60)
    
    channel = create_channel("user")
    called = [False]
    
    # Channel should prefix events
    channel.on("created", lambda d: called.__setitem__(0, True))
    channel.emit("created", {"id": 1})
    
    runner.test("Channel prefixes events", called[0])


def run_global_bus_tests(runner: TestRunner):
    """Test global event bus singleton."""
    print("\nGlobal Event Bus Tests")
    print("-" * 60)
    
    # Reset singleton for clean test
    EventBus.reset()
    
    bus1 = EventBus.get_instance()
    bus2 = EventBus.get_instance()
    
    runner.test("Bus is singleton", bus1 is bus2)
    
    called = [False]
    bus1.on("singleton.test", lambda d: called.__setitem__(0, True))
    bus2.emit("singleton.test")
    
    runner.test("Singleton shares state", called[0])
    
    # Cleanup
    EventBus.reset()


def run_decorator_tests(runner: TestRunner):
    """Test decorator utilities."""
    print("\nDecorator Tests")
    print("-" * 60)
    
    emitter = EventEmitter()
    called = [False]
    
    @on_event(emitter, "decorated.event")
    def decorated_handler(data):
        called[0] = True
    
    emitter.emit("decorated.event")
    runner.test("on_event decorator registers listener", called[0])


def run_thread_safety_tests(runner: TestRunner):
    """Test thread safety."""
    print("\nThread Safety Tests")
    print("-" * 60)
    
    emitter = EventEmitter()
    counter = [0]
    lock = threading.Lock()
    
    def thread_handler(data):
        with lock:
            counter[0] += 1
    
    # Register listener
    emitter.on("thread.test", thread_handler)
    
    # Create multiple threads
    threads = []
    for _ in range(10):
        t = threading.Thread(target=lambda: emitter.emit("thread.test"))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    runner.test("Thread-safe emission", counter[0] == 10)


def run_async_tests(runner: TestRunner):
    """Test async listener support."""
    print("\nAsync Listener Tests")
    print("-" * 60)
    
    # Skip if asyncio.run not available (Python < 3.7)
    if not hasattr(asyncio, 'run'):
        runner.test("Async support (skipped - Python < 3.7)", True)
        return
    
    emitter = EventEmitter()
    called = [False]
    
    async def async_handler(data):
        called[0] = True
    
    emitter.on("async.test", async_handler)
    
    # Run async event loop
    async def run_test():
        emitter.emit_async("async.test")
        await asyncio.sleep(0.1)  # Give time for async handler
    
    asyncio.run(run_test())
    
    runner.test("Async listener called", called[0])


def run_edge_cases(runner: TestRunner):
    """Test edge cases."""
    print("\nEdge Case Tests")
    print("-" * 60)
    
    emitter = EventEmitter()
    
    # Empty emitter
    runner.test("Empty emitter has 0 listeners", emitter.listener_count == 0)
    runner.test("Empty emitter has 0 events", emitter.event_count == 0)
    
    # Emit with no listeners (should not crash)
    try:
        emitter.emit("no.listeners")
        runner.test("Emit with no listeners doesn't crash", True)
    except Exception as e:
        runner.test("Emit with no listeners doesn't crash", False, str(e))
    
    # None data
    received = []
    emitter.on("none.data", lambda d: received.append(d))
    emitter.emit("none.data", None)
    runner.test("None data handled", received == [None])
    
    # Clear all
    emitter.on("clear1", lambda: None)
    emitter.on("clear2", lambda: None)
    emitter.clear()
    runner.test("Clear removes all", emitter.listener_count == 0)


def run_tests():
    """Run all tests."""
    runner = TestRunner()
    
    run_basic_tests(runner)
    run_once_tests(runner)
    run_wildcard_tests(runner)
    run_priority_tests(runner)
    run_removal_tests(runner)
    run_history_tests(runner)
    run_pause_resume_tests(runner)
    run_introspection_tests(runner)
    run_channel_tests(runner)
    run_global_bus_tests(runner)
    run_decorator_tests(runner)
    run_thread_safety_tests(runner)
    run_async_tests(runner)
    run_edge_cases(runner)
    
    return runner.report()


if __name__ == "__main__":
    print("=" * 60)
    print("Event Emitter Utilities - Test Suite")
    print("=" * 60)
    
    success = run_tests()
    sys.exit(0 if success else 1)
