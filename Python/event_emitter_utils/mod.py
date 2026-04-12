#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Event Emitter Utilities Module
============================================
A comprehensive event emitter/pub-sub implementation for Python with zero external dependencies.

Features:
    - Event registration and emission
    - Wildcard event patterns (*, **)
    - Once-only listeners
    - Event namespacing (e.g., "user.created", "user.deleted")
    - Async listener support
    - Listener priority ordering
    - Event data transformation
    - Thread-safe operations
    - Event history/replay
    - Listener introspection and debugging

Author: AllToolkit Contributors
License: MIT
"""

import threading
import fnmatch
import time
import inspect
import asyncio
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, Set
from collections import defaultdict
from dataclasses import dataclass, field
from functools import wraps
import weakref
import re


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Listener:
    """Represents an event listener with metadata."""
    callback: Callable
    once: bool = False
    priority: int = 0
    namespace: str = "*"
    created_at: float = field(default_factory=time.time)
    call_count: int = 0
    
    def __hash__(self):
        return hash(id(self.callback))
    
    def __eq__(self, other):
        if isinstance(other, Listener):
            return self.callback == other.callback
        return False


@dataclass
class EventRecord:
    """Records an emitted event for history/replay."""
    name: str
    data: Any
    timestamp: float = field(default_factory=time.time)
    emitter_id: str = ""


# ============================================================================
# Decorator Utilities
# ============================================================================

def emits_event(event_name: str):
    """
    Decorator to mark a function as emitting an event.
    Wraps the function to automatically emit an event after execution.
    
    Args:
        event_name: The name of the event to emit
        
    Example:
        >>> @emits_event("user.created")
        ... def create_user(name):
        ...     return {"name": name}
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Get the emitter from context or use global
            emitter = kwargs.pop('_emitter', None)
            if emitter:
                emitter.emit(event_name, result)
            return result
        return wrapper
    return decorator


def on_event(emitter: 'EventEmitter', event_name: str, priority: int = 0):
    """
    Decorator to register a function as an event listener.
    
    Args:
        emitter: The EventEmitter instance
        event_name: The event name to listen for
        priority: Listener priority (higher = called first)
        
    Example:
        >>> emitter = EventEmitter()
        >>> @on_event(emitter, "user.created")
        ... def handle_user_created(data):
        ...     print(f"User created: {data}")
    """
    def decorator(func: Callable) -> Callable:
        emitter.on(event_name, func, priority=priority)
        return func
    return decorator


# ============================================================================
# Main Event Emitter Class
# ============================================================================

class EventEmitter:
    """
    A thread-safe event emitter with advanced features.
    
    Features:
        - Wildcard event patterns (* matches one level, ** matches all)
        - Once-only listeners
        - Priority-based listener ordering
        - Async listener support
        - Event namespacing
        - Event history and replay
        - Thread-safe operations
        - Listener introspection
    
    Example:
        >>> emitter = EventEmitter()
        >>> emitter.on("user.created", lambda data: print(f"New user: {data}"))
        >>> emitter.emit("user.created", {"id": 1, "name": "Alice"})
    """
    
    def __init__(self, max_history: int = 100, enable_history: bool = True):
        """
        Initialize the event emitter.
        
        Args:
            max_history: Maximum number of events to keep in history (default: 100)
            enable_history: Whether to record event history (default: True)
        """
        self._listeners: Dict[str, List[Listener]] = defaultdict(list)
        self._lock = threading.RLock()
        self._max_history = max_history
        self._enable_history = enable_history
        self._history: List[EventRecord] = []
        self._id = f"emitter_{id(self)}"
        self._wildcard_cache: Dict[str, List[Listener]] = {}
        self._paused_events: Set[str] = set()
        self._async_handlers: bool = False
    
    @property
    def id(self) -> str:
        """Get the unique emitter ID."""
        return self._id
    
    @property
    def event_count(self) -> int:
        """Get the number of unique events with listeners."""
        with self._lock:
            return len(self._listeners)
    
    @property
    def listener_count(self) -> int:
        """Get the total number of listeners."""
        with self._lock:
            return sum(len(listeners) for listeners in self._listeners.values())
    
    # =========================================================================
    # Listener Registration
    # =========================================================================
    
    def on(self, event_name: str, callback: Callable, 
           priority: int = 0, once: bool = False) -> Listener:
        """
        Register a listener for an event.
        
        Args:
            event_name: The event name (supports * and ** wildcards)
            callback: The callback function to invoke
            priority: Listener priority (higher = called first, default: 0)
            once: If True, listener is removed after first invocation (default: False)
        
        Returns:
            The Listener object (can be used to remove later)
        
        Example:
            >>> emitter.on("user.*", handle_user_events)
            >>> emitter.on("data.**", handle_all_data, priority=10)
        """
        listener = Listener(
            callback=callback,
            once=once,
            priority=priority,
            namespace=event_name
        )
        
        with self._lock:
            self._listeners[event_name].append(listener)
            # Sort by priority (descending) then by registration time
            self._listeners[event_name].sort(
                key=lambda l: (-l.priority, l.created_at)
            )
            self._wildcard_cache.clear()
        
        return listener
    
    def once(self, event_name: str, callback: Callable, 
             priority: int = 0) -> Listener:
        """
        Register a one-time listener.
        
        Args:
            event_name: The event name
            callback: The callback function
            priority: Listener priority (default: 0)
        
        Returns:
            The Listener object
        
        Example:
            >>> emitter.once("app.startup", handle_startup)
        """
        return self.on(event_name, callback, priority=priority, once=True)
    
    def off(self, event_name: str, callback: Optional[Callable] = None) -> int:
        """
        Remove listener(s).
        
        Args:
            event_name: The event name (or "*" for all events)
            callback: Specific callback to remove (None removes all for event)
        
        Returns:
            Number of listeners removed
        
        Example:
            >>> emitter.off("user.created")  # Remove all listeners
            >>> emitter.off("user.created", specific_handler)  # Remove specific
        """
        removed = 0
        
        with self._lock:
            if event_name == "*":
                # Remove all listeners
                removed = self.listener_count
                self._listeners.clear()
            elif event_name in self._listeners:
                if callback is None:
                    # Remove all listeners for this event
                    removed = len(self._listeners[event_name])
                    del self._listeners[event_name]
                else:
                    # Remove specific listener
                    original_len = len(self._listeners[event_name])
                    self._listeners[event_name] = [
                        l for l in self._listeners[event_name]
                        if l.callback != callback
                    ]
                    removed = original_len - len(self._listeners[event_name])
            
            self._wildcard_cache.clear()
        
        return removed
    
    def remove_listener(self, listener: Listener) -> bool:
        """
        Remove a specific listener object.
        
        Args:
            listener: The Listener object to remove
        
        Returns:
            True if removed, False if not found
        """
        with self._lock:
            for event_name, listeners in self._listeners.items():
                if listener in listeners:
                    listeners.remove(listener)
                    self._wildcard_cache.clear()
                    return True
        return False
    
    # =========================================================================
    # Event Emission
    # =========================================================================
    
    def emit(self, event_name: str, data: Any = None, 
             async_mode: bool = False) -> int:
        """
        Emit an event to all matching listeners.
        
        Args:
            event_name: The event name to emit
            data: Data to pass to listeners (default: None)
            async_mode: If True, run async listeners (default: False)
        
        Returns:
            Number of listeners invoked
        
        Example:
            >>> emitter.emit("user.created", {"id": 1, "name": "Alice"})
        """
        # Check if event is paused
        if event_name in self._paused_events:
            return 0
        
        # Record history
        if self._enable_history:
            self._record_event(event_name, data)
        
        # Get matching listeners
        listeners = self._get_matching_listeners(event_name)
        
        invoked = 0
        once_listeners = []
        
        for listener in listeners:
            try:
                # Check if listener is async
                is_async = asyncio.iscoroutinefunction(listener.callback)
                
                if is_async and async_mode:
                    # Queue for async execution
                    asyncio.create_task(self._invoke_async(listener, event_name, data))
                    invoked += 1
                elif not is_async:
                    # Synchronous invocation
                    self._invoke_listener(listener, event_name, data)
                    invoked += 1
                    
                    # Track once-only listeners for removal
                    if listener.once:
                        once_listeners.append(listener)
                        
            except Exception as e:
                # Don't let one listener break others
                print(f"Event listener error for '{event_name}': {e}")
        
        # Remove once-only listeners
        if once_listeners:
            with self._lock:
                for listener in once_listeners:
                    for event_name_key, listeners in self._listeners.items():
                        if listener in listeners:
                            listeners.remove(listener)
                self._wildcard_cache.clear()
        
        return invoked
    
    def _invoke_listener(self, listener: Listener, event_name: str, data: Any):
        """Invoke a synchronous listener."""
        listener.call_count += 1
        
        # Check if callback accepts event_name parameter
        sig = inspect.signature(listener.callback)
        params = list(sig.parameters.keys())
        
        if len(params) >= 2:
            listener.callback(event_name, data)
        elif len(params) >= 1:
            listener.callback(data)
        else:
            listener.callback()
    
    async def _invoke_async(self, listener: Listener, event_name: str, data: Any):
        """Invoke an async listener."""
        listener.call_count += 1
        sig = inspect.signature(listener.callback)
        params = list(sig.parameters.keys())
        
        if len(params) >= 2:
            await listener.callback(event_name, data)
        elif len(params) >= 1:
            await listener.callback(data)
        else:
            await listener.callback()
    
    def emit_async(self, event_name: str, data: Any = None) -> int:
        """
        Emit an event with async support.
        
        Args:
            event_name: The event name
            data: Data to pass to listeners
        
        Returns:
            Number of listeners invoked
        """
        return self.emit(event_name, data, async_mode=True)
    
    # =========================================================================
    # Wildcard Matching
    # =========================================================================
    
    def _get_matching_listeners(self, event_name: str) -> List[Listener]:
        """Get all listeners matching an event name (including wildcards)."""
        with self._lock:
            if event_name in self._wildcard_cache:
                return self._wildcard_cache[event_name]
            
            matching = []
            seen_callbacks: Set[int] = set()
            
            for pattern, listeners in self._listeners.items():
                if self._matches_pattern(event_name, pattern):
                    for listener in listeners:
                        # Avoid duplicate callbacks
                        cb_id = id(listener.callback)
                        if cb_id not in seen_callbacks:
                            matching.append(listener)
                            seen_callbacks.add(cb_id)
            
            # Sort by priority
            matching.sort(key=lambda l: (-l.priority, l.created_at))
            self._wildcard_cache[event_name] = matching
            return matching
    
    def _matches_pattern(self, event_name: str, pattern: str) -> bool:
        """Check if an event name matches a pattern."""
        if pattern == event_name:
            return True
        
        # Handle ** (matches everything after a prefix)
        if pattern.endswith(".**"):
            prefix = pattern[:-3]  # Remove .**
            return event_name.startswith(prefix + ".") or event_name == prefix
        
        if pattern == "**":
            return True
        
        # Handle * (matches one level)
        if "*" in pattern:
            # Convert pattern to regex
            regex_pattern = pattern.replace(".", r"\.")
            regex_pattern = regex_pattern.replace("**", ".*")
            regex_pattern = regex_pattern.replace("*", r"[^.]*")
            regex_pattern = f"^{regex_pattern}$"
            
            if re.match(regex_pattern, event_name):
                return True
        
        return False
    
    # =========================================================================
    # Event History
    # =========================================================================
    
    def _record_event(self, event_name: str, data: Any):
        """Record an event in history."""
        record = EventRecord(
            name=event_name,
            data=data,
            emitter_id=self._id
        )
        
        with self._lock:
            self._history.append(record)
            # Trim history if needed
            if len(self._history) > self._max_history:
                self._history = self._history[-self._max_history:]
    
    def get_history(self, event_name: Optional[str] = None, 
                    limit: int = 10) -> List[EventRecord]:
        """
        Get event history.
        
        Args:
            event_name: Filter by event name (None for all)
            limit: Maximum records to return (default: 10)
        
        Returns:
            List of EventRecord objects
        """
        with self._lock:
            if event_name is None:
                return self._history[-limit:]
            
            filtered = [r for r in self._history if r.name == event_name]
            return filtered[-limit:]
    
    def replay(self, event_name: str, callback: Callable, 
               from_index: int = 0) -> int:
        """
        Replay historical events to a callback.
        
        Args:
            event_name: The event name to replay
            callback: Function to call for each historical event
            from_index: Start index in history (default: 0)
        
        Returns:
            Number of events replayed
        """
        with self._lock:
            history = [r for r in self._history if r.name == event_name]
        
        count = 0
        for record in history[from_index:]:
            callback(record.data)
            count += 1
        
        return count
    
    def clear_history(self, event_name: Optional[str] = None):
        """
        Clear event history.
        
        Args:
            event_name: Clear only this event (None for all)
        """
        with self._lock:
            if event_name is None:
                self._history.clear()
            else:
                self._history = [
                    r for r in self._history if r.name != event_name
                ]
    
    # =========================================================================
    # Event Control
    # =========================================================================
    
    def pause(self, event_name: str):
        """Pause emission of an event."""
        self._paused_events.add(event_name)
    
    def resume(self, event_name: str):
        """Resume emission of an event."""
        self._paused_events.discard(event_name)
    
    def is_paused(self, event_name: str) -> bool:
        """Check if an event is paused."""
        return event_name in self._paused_events
    
    # =========================================================================
    # Introspection
    # =========================================================================
    
    def has_listener(self, event_name: str) -> bool:
        """Check if an event has any listeners."""
        with self._lock:
            return bool(self._get_matching_listeners(event_name))
    
    def get_listeners(self, event_name: str) -> List[Callable]:
        """
        Get all listeners for an event.
        
        Args:
            event_name: The event name
        
        Returns:
            List of callback functions
        """
        with self._lock:
            listeners = self._get_matching_listeners(event_name)
            return [l.callback for l in listeners]
    
    def get_listener_count(self, event_name: str) -> int:
        """Get the number of listeners for an event."""
        with self._lock:
            return len(self._get_matching_listeners(event_name))
    
    def get_events(self) -> List[str]:
        """Get all registered event names."""
        with self._lock:
            return list(self._listeners.keys())
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get emitter statistics.
        
        Returns:
            Dict with emitter stats
        """
        with self._lock:
            listener_stats = {}
            for event_name, listeners in self._listeners.items():
                listener_stats[event_name] = {
                    "count": len(listeners),
                    "once_count": sum(1 for l in listeners if l.once),
                    "total_calls": sum(l.call_count for l in listeners)
                }
            
            return {
                "id": self._id,
                "event_count": len(self._listeners),
                "total_listeners": self.listener_count,
                "history_size": len(self._history),
                "paused_events": list(self._paused_events),
                "listeners": listener_stats
            }
    
    def clear(self):
        """Remove all listeners and clear history."""
        with self._lock:
            self._listeners.clear()
            self._history.clear()
            self._wildcard_cache.clear()
            self._paused_events.clear()


# ============================================================================
# Global Event Bus
# ============================================================================

class EventBus:
    """
    A global event bus for application-wide events.
    Singleton pattern for shared event handling.
    
    Example:
        >>> bus = EventBus.get_instance()
        >>> bus.on("app.error", handle_error)
        >>> bus.emit("app.error", {"message": "Something went wrong"})
    """
    
    _instance: Optional['EventBus'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'EventBus':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._emitter = EventEmitter()
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> 'EventBus':
        """Get the singleton instance."""
        return cls()
    
    @classmethod
    def reset(cls):
        """Reset the singleton (useful for testing)."""
        with cls._lock:
            cls._instance = None
    
    # Delegate all methods to the internal emitter
    def on(self, *args, **kwargs):
        return self._emitter.on(*args, **kwargs)
    
    def once(self, *args, **kwargs):
        return self._emitter.once(*args, **kwargs)
    
    def off(self, *args, **kwargs):
        return self._emitter.off(*args, **kwargs)
    
    def emit(self, *args, **kwargs):
        return self._emitter.emit(*args, **kwargs)
    
    def emit_async(self, *args, **kwargs):
        return self._emitter.emit_async(*args, **kwargs)
    
    def get_history(self, *args, **kwargs):
        return self._emitter.get_history(*args, **kwargs)
    
    def replay(self, *args, **kwargs):
        return self._emitter.replay(*args, **kwargs)
    
    def has_listener(self, *args, **kwargs):
        return self._emitter.has_listener(*args, **kwargs)
    
    def get_listeners(self, *args, **kwargs):
        return self._emitter.get_listeners(*args, **kwargs)
    
    def get_events(self) -> List[str]:
        return self._emitter.get_events()
    
    def get_stats(self) -> Dict[str, Any]:
        return self._emitter.get_stats()
    
    def clear(self):
        return self._emitter.clear()


# ============================================================================
# Convenience Functions
# ============================================================================

def create_emitter(max_history: int = 100) -> EventEmitter:
    """Create a new EventEmitter instance."""
    return EventEmitter(max_history=max_history)


def create_channel(name: str) -> EventEmitter:
    """
    Create a named event channel (useful for organizing events).
    
    Args:
        name: Channel name (used as event prefix)
    
    Returns:
        EventEmitter configured for this channel
    
    Example:
        >>> user_channel = create_channel("user")
        >>> user_channel.on("created", handler)  # Listens to "user.created"
        >>> user_channel.emit("created", data)   # Emits "user.created"
    """
    emitter = EventEmitter()
    
    # Wrap emit to auto-prefix
    original_emit = emitter.emit
    def prefixed_emit(event_name: str, data: Any = None, **kwargs):
        full_name = f"{name}.{event_name}"
        return original_emit(full_name, data, **kwargs)
    
    # Wrap on to auto-prefix
    original_on = emitter.on
    def prefixed_on(event_name: str, callback: Callable, 
                    priority: int = 0, once: bool = False) -> Listener:
        full_name = f"{name}.{event_name}"
        return original_on(full_name, callback, priority=priority, once=once)
    
    emitter.emit = prefixed_emit  # type: ignore
    emitter.on = prefixed_on  # type: ignore
    emitter.once = lambda ev, cb, pr=0: prefixed_on(ev, cb, priority=pr, once=True)  # type: ignore
    
    return emitter


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Event Emitter Utilities - Demo")
    print("=" * 60)
    
    # Basic usage
    emitter = EventEmitter()
    
    def on_user_created(data):
        print(f"  [Handler] User created: {data}")
    
    def on_any_user_event(event_name, data):
        print(f"  [Wildcard] {event_name}: {data}")
    
    # Register listeners
    emitter.on("user.created", on_user_created)
    emitter.on("user.*", on_any_user_event, priority=10)
    
    # Emit events
    print("\n1. Basic Event Emission:")
    emitter.emit("user.created", {"id": 1, "name": "Alice"})
    
    # Once-only listener
    print("\n2. Once-Only Listener:")
    emitter.once("app.startup", lambda d: print(f"  Startup: {d}"))
    emitter.emit("app.startup", "v1.0.0")
    emitter.emit("app.startup", "v1.0.1")  # Won't trigger
    
    # Wildcard patterns
    print("\n3. Wildcard Patterns:")
    emitter.on("data.**", lambda d: print(f"  [**] Data event: {d}"))
    emitter.emit("data.users.sync", {"count": 100})
    
    # Priority ordering
    print("\n4. Priority Ordering:")
    emitter.on("test.event", lambda d: print("  First (priority 10)"), priority=10)
    emitter.on("test.event", lambda d: print("  Second (priority 5)"), priority=5)
    emitter.on("test.event", lambda d: print("  Third (priority 0)"), priority=0)
    emitter.emit("test.event")
    
    # Event history
    print("\n5. Event History:")
    emitter.emit("log.info", "Message 1")
    emitter.emit("log.info", "Message 2")
    emitter.emit("log.info", "Message 3")
    history = emitter.get_history("log.info", limit=5)
    print(f"  History contains {len(history)} events")
    
    # Statistics
    print("\n6. Statistics:")
    stats = emitter.get_stats()
    print(f"  Total events: {stats['event_count']}")
    print(f"  Total listeners: {stats['total_listeners']}")
    
    # Global event bus
    print("\n7. Global Event Bus:")
    bus = EventBus.get_instance()
    bus.on("global.event", lambda d: print(f"  Global: {d}"))
    bus.emit("global.event", "Hello from bus!")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)
