"""
AllToolkit - Python Observable Utilities

A zero-dependency, production-ready observer pattern / event emitter module.
Supports synchronous and async observers, event filtering, one-time subscriptions,
event history, and thread-safe operations.

Author: AllToolkit
License: MIT
"""

import threading
import weakref
import time
from typing import (
    Callable, Generic, TypeVar, Optional, List, Dict, Any, 
    Set, Tuple, Union, Awaitable, Coroutine
)
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from collections import deque
import asyncio
from concurrent.futures import ThreadPoolExecutor
import inspect


T = TypeVar('T')
EventData = TypeVar('EventData')


class Priority(Enum):
    """Observer priority levels."""
    LOWEST = 0
    LOW = 25
    NORMAL = 50
    HIGH = 75
    HIGHEST = 100
    MONITOR = 150  # Always runs last, for monitoring/logging


@dataclass
class Subscription(Generic[T]):
    """
    Represents a subscription to an event.
    
    Attributes:
        id: Unique subscription identifier
        event_name: Name of the subscribed event
        callback: The callback function
        priority: Priority level (higher = earlier execution)
        once: Whether this is a one-time subscription
        active: Whether the subscription is active
        filter_func: Optional filter function
        metadata: Additional metadata
    """
    id: str
    event_name: str
    callback: Callable[[T], Any]
    priority: int = 50
    once: bool = False
    active: bool = True
    filter_func: Optional[Callable[[T], bool]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    _call_count: int = field(default=0, repr=False)
    _created_at: float = field(default_factory=time.time, repr=False)
    
    def matches(self, data: T) -> bool:
        """Check if this subscription matches the given data."""
        if not self.active:
            return False
        if self.filter_func is not None:
            return self.filter_func(data)
        return True
    
    @property
    def call_count(self) -> int:
        """Number of times this subscription has been called."""
        return self._call_count


@dataclass
class EventRecord(Generic[T]):
    """
    Record of a past event emission.
    
    Attributes:
        event_name: Name of the event
        data: The event data
        timestamp: When the event was emitted
        subscriber_count: Number of subscribers that received it
    """
    event_name: str
    data: T
    timestamp: float
    subscriber_count: int


class Observable(Generic[EventData]):
    """
    A thread-safe observable that manages event subscriptions and emissions.
    
    Features:
    - Subscribe to events with callbacks
    - Priority-based execution order
    - One-time subscriptions
    - Event filtering
    - Event history
    - Weak references to prevent memory leaks
    - Async support
    
    Example:
        observable = Observable[str]()
        
        # Subscribe to events
        def on_message(msg: str):
            print(f"Received: {msg}")
        
        sub = observable.subscribe(on_message)
        
        # Emit events
        observable.emit("Hello, World!")
        
        # Unsubscribe
        sub.unsubscribe()
    """
    
    def __init__(
        self,
        name: str = "Observable",
        max_history: int = 0,
        async_executor: Optional[ThreadPoolExecutor] = None,
    ):
        """
        Initialize the observable.
        
        Args:
            name: Name for debugging/logging
            max_history: Maximum number of events to keep in history (0 = no history)
            async_executor: Optional executor for async callbacks
        """
        self._name = name
        self._max_history = max_history
        self._subscriptions: Dict[str, List[Subscription[EventData]]] = {}
        self._history: deque = deque(maxlen=max_history) if max_history > 0 else None
        self._lock = threading.RLock()
        self._subscription_counter = 0
        self._async_executor = async_executor
        self._weak_refs: Set[weakref.ref] = set()
    
    @property
    def name(self) -> str:
        """Get the observable name."""
        return self._name
    
    @property
    def subscription_count(self) -> int:
        """Get total number of active subscriptions."""
        with self._lock:
            return sum(
                1 for subs in self._subscriptions.values()
                for sub in subs if sub.active
            )
    
    def _generate_id(self) -> str:
        """Generate a unique subscription ID."""
        with self._lock:
            self._subscription_counter += 1
            return f"sub_{self._subscription_counter}_{int(time.time() * 1000)}"
    
    def subscribe(
        self,
        callback: Callable[[EventData], Any],
        event_name: str = "default",
        priority: Union[int, Priority] = Priority.NORMAL,
        once: bool = False,
        filter_func: Optional[Callable[[EventData], bool]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Subscription[EventData]:
        """
        Subscribe to events.
        
        Args:
            callback: Function to call when event is emitted
            event_name: Name of the event to subscribe to
            priority: Execution priority (higher = earlier)
            once: If True, unsubscribe after first emission
            filter_func: Optional filter function to conditionally receive events
            metadata: Additional metadata for the subscription
            
        Returns:
            Subscription object for managing the subscription
            
        Example:
            def handler(data):
                print(f"Got: {data}")
            
            sub = observable.subscribe(handler, event_name="message", priority=Priority.HIGH)
        """
        if isinstance(priority, Priority):
            priority = priority.value
        
        subscription = Subscription(
            id=self._generate_id(),
            event_name=event_name,
            callback=callback,
            priority=priority,
            once=once,
            filter_func=filter_func,
            metadata=metadata or {},
        )
        
        with self._lock:
            if event_name not in self._subscriptions:
                self._subscriptions[event_name] = []
            self._subscriptions[event_name].append(subscription)
            # Sort by priority (higher first)
            self._subscriptions[event_name].sort(key=lambda s: s.priority, reverse=True)
        
        return subscription
    
    def subscribe_once(
        self,
        callback: Callable[[EventData], Any],
        event_name: str = "default",
        priority: Union[int, Priority] = Priority.NORMAL,
        filter_func: Optional[Callable[[EventData], bool]] = None,
    ) -> Subscription[EventData]:
        """
        Subscribe to a single event emission.
        
        Args:
            callback: Function to call when event is emitted
            event_name: Name of the event to subscribe to
            priority: Execution priority
            filter_func: Optional filter function
            
        Returns:
            Subscription object
        """
        return self.subscribe(
            callback=callback,
            event_name=event_name,
            priority=priority,
            once=True,
            filter_func=filter_func,
        )
    
    def unsubscribe(self, subscription: Subscription[EventData]) -> bool:
        """
        Unsubscribe a subscription.
        
        Args:
            subscription: The subscription to remove
            
        Returns:
            True if the subscription was found and removed
        """
        with self._lock:
            event_name = subscription.event_name
            if event_name not in self._subscriptions:
                return False
            
            subs = self._subscriptions[event_name]
            for i, sub in enumerate(subs):
                if sub.id == subscription.id:
                    subs.pop(i)
                    return True
            return False
    
    def unsubscribe_all(self, event_name: Optional[str] = None) -> int:
        """
        Unsubscribe all subscriptions, optionally for a specific event.
        
        Args:
            event_name: If specified, only unsubscribe from this event
            
        Returns:
            Number of subscriptions removed
        """
        with self._lock:
            if event_name is not None:
                count = len(self._subscriptions.get(event_name, []))
                self._subscriptions[event_name] = []
                return count
            
            count = self.subscription_count
            self._subscriptions.clear()
            return count
    
    def emit(
        self,
        data: EventData,
        event_name: str = "default",
        include_history: bool = True,
    ) -> int:
        """
        Emit an event to all subscribers.
        
        Args:
            data: The event data to emit
            event_name: Name of the event to emit
            include_history: Whether to record in history
            
        Returns:
            Number of subscribers that received the event
            
        Example:
            observable.emit({"action": "save", "data": content}, event_name="file")
        """
        callbacks_to_run: List[Tuple[Subscription, Any]] = []
        
        with self._lock:
            subs = self._subscriptions.get(event_name, []).copy()
            
            # Find matching subscriptions
            to_remove = []
            for sub in subs:
                if not sub.active:
                    continue
                if sub.matches(data):
                    callbacks_to_run.append((sub, data))
                    sub._call_count += 1
                    if sub.once:
                        to_remove.append(sub)
            
            # Remove one-time subscriptions
            for sub in to_remove:
                self._unsubscribe_internal(sub)
            
            # Record history
            if include_history and self._history is not None:
                self._history.append(EventRecord(
                    event_name=event_name,
                    data=data,
                    timestamp=time.time(),
                    subscriber_count=len(callbacks_to_run),
                ))
        
        # Execute callbacks outside of lock
        for sub, event_data in callbacks_to_run:
            try:
                # Check if callback is async
                if asyncio.iscoroutinefunction(sub.callback):
                    self._run_async_callback(sub.callback, event_data)
                else:
                    sub.callback(event_data)
            except Exception:
                # Don't let one callback break others
                pass
        
        return len(callbacks_to_run)
    
    def _run_async_callback(self, callback: Callable, data: Any) -> None:
        """Run an async callback in a background thread or event loop."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(callback(data))
            else:
                loop.run_until_complete(callback(data))
        except RuntimeError:
            # No event loop, run in new loop
            asyncio.run(callback(data))
    
    def _unsubscribe_internal(self, subscription: Subscription[EventData]) -> bool:
        """Internal unsubscribe without lock (caller must hold lock)."""
        event_name = subscription.event_name
        if event_name not in self._subscriptions:
            return False
        
        subs = self._subscriptions[event_name]
        for i, sub in enumerate(subs):
            if sub.id == subscription.id:
                subs.pop(i)
                return True
        return False
    
    async def emit_async(
        self,
        data: EventData,
        event_name: str = "default",
        include_history: bool = True,
    ) -> int:
        """
        Emit an event asynchronously, awaiting all async callbacks.
        
        Args:
            data: The event data to emit
            event_name: Name of the event to emit
            include_history: Whether to record in history
            
        Returns:
            Number of subscribers that received the event
        """
        callbacks_to_run: List[Tuple[Subscription, Any]] = []
        
        with self._lock:
            subs = self._subscriptions.get(event_name, []).copy()
            
            to_remove = []
            for sub in subs:
                if not sub.active:
                    continue
                if sub.matches(data):
                    callbacks_to_run.append((sub, data))
                    sub._call_count += 1
                    if sub.once:
                        to_remove.append(sub)
            
            for sub in to_remove:
                self._unsubscribe_internal(sub)
            
            if include_history and self._history is not None:
                self._history.append(EventRecord(
                    event_name=event_name,
                    data=data,
                    timestamp=time.time(),
                    subscriber_count=len(callbacks_to_run),
                ))
        
        # Execute callbacks
        for sub, event_data in callbacks_to_run:
            try:
                if asyncio.iscoroutinefunction(sub.callback):
                    await sub.callback(event_data)
                else:
                    sub.callback(event_data)
            except Exception:
                pass
        
        return len(callbacks_to_run)
    
    def get_history(
        self,
        event_name: Optional[str] = None,
        limit: int = 100,
    ) -> List[EventRecord[EventData]]:
        """
        Get event history.
        
        Args:
            event_name: Filter by event name (None = all events)
            limit: Maximum number of records to return
            
        Returns:
            List of event records, newest first
        """
        with self._lock:
            if self._history is None:
                return []
            
            records = list(self._history)
            if event_name is not None:
                records = [r for r in records if r.event_name == event_name]
            
            return records[-limit:][::-1]  # Newest first
    
    def get_subscriptions(
        self,
        event_name: Optional[str] = None,
    ) -> List[Subscription[EventData]]:
        """
        Get all subscriptions, optionally filtered by event name.
        
        Args:
            event_name: Filter by event name (None = all events)
            
        Returns:
            List of subscriptions
        """
        with self._lock:
            if event_name is not None:
                return self._subscriptions.get(event_name, []).copy()
            
            result = []
            for subs in self._subscriptions.values():
                result.extend(subs)
            return result
    
    def has_subscribers(self, event_name: str = "default") -> bool:
        """Check if there are any active subscribers for an event."""
        with self._lock:
            subs = self._subscriptions.get(event_name, [])
            return any(sub.active for sub in subs)
    
    def pause(self, subscription: Subscription[EventData]) -> None:
        """Temporarily pause a subscription."""
        subscription.active = False
    
    def resume(self, subscription: Subscription[EventData]) -> None:
        """Resume a paused subscription."""
        subscription.active = True


class EventEmitter(Generic[EventData]):
    """
    A multi-event observable that supports named events.
    
    This is a convenience wrapper around Observable that makes it easier
    to work with multiple named events.
    
    Example:
        emitter = EventEmitter[dict]()
        
        @emitter.on("user_created")
        def on_user_created(user):
            print(f"New user: {user['name']}")
        
        emitter.emit("user_created", {"name": "Alice", "id": 1})
    """
    
    def __init__(
        self,
        max_history: int = 0,
        async_executor: Optional[ThreadPoolExecutor] = None,
    ):
        """
        Initialize the event emitter.
        
        Args:
            max_history: Maximum events to keep in history per event type
            async_executor: Optional executor for async callbacks
        """
        self._observable = Observable[EventData](
            name="EventEmitter",
            max_history=max_history,
            async_executor=async_executor,
        )
    
    def on(
        self,
        event_name: str,
        priority: Union[int, Priority] = Priority.NORMAL,
        filter_func: Optional[Callable[[EventData], bool]] = None,
    ) -> Callable[[Callable[[EventData], Any]], Callable[[EventData], Any]]:
        """
        Decorator to subscribe to an event.
        
        Args:
            event_name: Name of the event to subscribe to
            priority: Execution priority
            filter_func: Optional filter function
            
        Returns:
            Decorator function
            
        Example:
            @emitter.on("save")
            def on_save(data):
                print(f"Saving: {data}")
        """
        def decorator(func: Callable[[EventData], Any]) -> Callable[[EventData], Any]:
            self._observable.subscribe(
                callback=func,
                event_name=event_name,
                priority=priority,
                filter_func=filter_func,
            )
            return func
        return decorator
    
    def once(
        self,
        event_name: str,
        priority: Union[int, Priority] = Priority.NORMAL,
        filter_func: Optional[Callable[[EventData], bool]] = None,
    ) -> Callable[[Callable[[EventData], Any]], Callable[[EventData], Any]]:
        """
        Decorator to subscribe to a single event emission.
        
        Args:
            event_name: Name of the event to subscribe to
            priority: Execution priority
            filter_func: Optional filter function
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable[[EventData], Any]) -> Callable[[EventData], Any]:
            self._observable.subscribe_once(
                callback=func,
                event_name=event_name,
                priority=priority,
                filter_func=filter_func,
            )
            return func
        return decorator
    
    def subscribe(
        self,
        event_name: str,
        callback: Callable[[EventData], Any],
        priority: Union[int, Priority] = Priority.NORMAL,
        once: bool = False,
        filter_func: Optional[Callable[[EventData], bool]] = None,
    ) -> Subscription[EventData]:
        """
        Subscribe to an event.
        
        Args:
            event_name: Name of the event
            callback: Function to call
            priority: Execution priority
            once: One-time subscription
            filter_func: Optional filter function
            
        Returns:
            Subscription object
        """
        return self._observable.subscribe(
            callback=callback,
            event_name=event_name,
            priority=priority,
            once=once,
            filter_func=filter_func,
        )
    
    def emit(self, event_name: str, data: EventData) -> int:
        """
        Emit an event.
        
        Args:
            event_name: Name of the event
            data: Event data
            
        Returns:
            Number of subscribers that received the event
        """
        return self._observable.emit(data=data, event_name=event_name)
    
    async def emit_async(self, event_name: str, data: EventData) -> int:
        """
        Emit an event asynchronously.
        
        Args:
            event_name: Name of the event
            data: Event data
            
        Returns:
            Number of subscribers that received the event
        """
        return await self._observable.emit_async(data=data, event_name=event_name)
    
    def unsubscribe(self, subscription: Subscription[EventData]) -> bool:
        """Unsubscribe a subscription."""
        return self._observable.unsubscribe(subscription)
    
    def unsubscribe_all(self, event_name: Optional[str] = None) -> int:
        """Unsubscribe all subscriptions."""
        return self._observable.unsubscribe_all(event_name)
    
    def get_history(self, event_name: Optional[str] = None) -> List[EventRecord[EventData]]:
        """Get event history."""
        return self._observable.get_history(event_name)
    
    def has_subscribers(self, event_name: str) -> bool:
        """Check if there are subscribers for an event."""
        return self._observable.has_subscribers(event_name)


class PropertyObservable(Generic[T]):
    """
    An observable property that notifies subscribers when its value changes.
    
    Example:
        name = PropertyObservable[str]("Alice")
        
        @name.on_change
        def on_name_change(old, new):
            print(f"Name changed from {old} to {new}")
        
        name.value = "Bob"  # Triggers: "Name changed from Alice to Bob"
    """
    
    def __init__(self, initial_value: Optional[T] = None):
        """
        Initialize with an optional initial value.
        
        Args:
            initial_value: Initial value of the property
        """
        self._value = initial_value
        self._observable = Observable[Tuple[Optional[T], T]](name="PropertyObservable")
    
    @property
    def value(self) -> Optional[T]:
        """Get the current value."""
        return self._value
    
    @value.setter
    def value(self, new_value: T) -> None:
        """Set the value and notify subscribers."""
        old_value = self._value
        if old_value != new_value:
            self._value = new_value
            self._observable.emit(data=(old_value, new_value), event_name="change")
    
    def on_change(
        self,
        callback: Callable[[Optional[T], T], Any],
        priority: Union[int, Priority] = Priority.NORMAL,
    ) -> Subscription[Tuple[Optional[T], T]]:
        """
        Subscribe to value changes.
        
        Args:
            callback: Function called with (old_value, new_value)
            priority: Execution priority
            
        Returns:
            Subscription object
            
        Example:
            def handler(old, new):
                print(f"Changed: {old} -> {new}")
            
            sub = prop.on_change(handler)
        """
        def wrapper(data: Tuple[Optional[T], T]) -> Any:
            old_value, new_value = data
            return callback(old_value, new_value)
        
        return self._observable.subscribe(
            callback=wrapper,
            event_name="change",
            priority=priority,
        )
    
    def set_silent(self, value: T) -> None:
        """Set value without triggering notifications."""
        self._value = value


class ComputedObservable(Generic[T]):
    """
    An observable that computes its value from other observables.
    
    Example:
        first_name = PropertyObservable("John")
        last_name = PropertyObservable("Doe")
        
        full_name = ComputedObservable(
            [first_name, last_name],
            lambda fn, ln: f"{fn} {ln}"
        )
        
        @full_name.on_change
        def on_name_change(old, new):
            print(f"Full name: {new}")
    """
    
    def __init__(
        self,
        sources: List[PropertyObservable],
        compute_func: Callable[..., T],
    ):
        """
        Initialize a computed observable.
        
        Args:
            sources: List of source PropertyObservables
            compute_func: Function to compute value from source values
        """
        self._sources = sources
        self._compute_func = compute_func
        self._observable = Observable[Tuple[Optional[T], T]](name="ComputedObservable")
        self._value: Optional[T] = None
        
        # Subscribe to all sources
        for source in sources:
            source.on_change(self._on_source_change)
        
        # Compute initial value
        self._recompute()
    
    def _recompute(self) -> None:
        """Recompute the value from sources."""
        values = [s.value for s in self._sources]
        new_value = self._compute_func(*values)
        old_value = self._value
        
        if old_value != new_value:
            self._value = new_value
            self._observable.emit(data=(old_value, new_value), event_name="change")
    
    def _on_source_change(self, old: Any, new: Any) -> None:
        """Handle source value change."""
        self._recompute()
    
    @property
    def value(self) -> Optional[T]:
        """Get the current computed value."""
        return self._value
    
    def on_change(
        self,
        callback: Callable[[Optional[T], T], Any],
        priority: Union[int, Priority] = Priority.NORMAL,
    ) -> Subscription[Tuple[Optional[T], T]]:
        """Subscribe to value changes."""
        def wrapper(data: Tuple[Optional[T], T]) -> Any:
            old_value, new_value = data
            return callback(old_value, new_value)
        
        return self._observable.subscribe(
            callback=wrapper,
            event_name="change",
            priority=priority,
        )


class Subject(Generic[T]):
    """
    A simple observable value that can be set and observed.
    
    Similar to RxJS Subject, combines Observable and Observer.
    
    Example:
        counter = Subject[int](0)
        
        counter.subscribe(lambda n: print(f"Count: {n}"))
        
        counter.next(1)   # "Count: 1"
        counter.next(2)   # "Count: 2"
    """
    
    def __init__(self, initial_value: Optional[T] = None):
        """
        Initialize with an optional initial value.
        
        Args:
            initial_value: Initial value
        """
        self._value = initial_value
        self._observable = Observable[T](name="Subject")
    
    @property
    def value(self) -> Optional[T]:
        """Get the current value."""
        return self._value
    
    def next(self, value: T) -> int:
        """
        Set a new value and notify subscribers.
        
        Args:
            value: New value
            
        Returns:
            Number of subscribers notified
        """
        self._value = value
        return self._observable.emit(data=value, event_name="default")
    
    def subscribe(
        self,
        callback: Callable[[T], Any],
        priority: Union[int, Priority] = Priority.NORMAL,
    ) -> Subscription[T]:
        """
        Subscribe to value changes.
        
        Args:
            callback: Function to call on value change
            priority: Execution priority
            
        Returns:
            Subscription object
        """
        return self._observable.subscribe(
            callback=callback,
            event_name="default",
            priority=priority,
        )
    
    def unsubscribe_all(self) -> int:
        """Unsubscribe all subscribers."""
        return self._observable.unsubscribe_all()


class BehaviorSubject(Generic[T]):
    """
    A Subject that remembers the current value and emits it to new subscribers.
    
    Example:
        name = BehaviorSubject[str]("initial")
        
        # New subscribers immediately receive current value
        name.subscribe(lambda n: print(f"Name: {n}"))  # "Name: initial"
        
        name.next("updated")  # "Name: updated"
    """
    
    def __init__(self, initial_value: T):
        """
        Initialize with a required initial value.
        
        Args:
            initial_value: Initial value (required)
        """
        self._value = initial_value
        self._observable = Observable[T](name="BehaviorSubject")
    
    @property
    def value(self) -> T:
        """Get the current value."""
        return self._value
    
    def next(self, value: T) -> int:
        """
        Set a new value and notify subscribers.
        
        Args:
            value: New value
            
        Returns:
            Number of subscribers notified
        """
        self._value = value
        return self._observable.emit(data=value, event_name="default")
    
    def subscribe(
        self,
        callback: Callable[[T], Any],
        priority: Union[int, Priority] = Priority.NORMAL,
        emit_current: bool = True,
    ) -> Subscription[T]:
        """
        Subscribe to value changes.
        
        Args:
            callback: Function to call on value change
            priority: Execution priority
            emit_current: If True, immediately call callback with current value
            
        Returns:
            Subscription object
        """
        sub = self._observable.subscribe(
            callback=callback,
            event_name="default",
            priority=priority,
        )
        
        if emit_current:
            try:
                callback(self._value)
            except Exception:
                pass
        
        return sub
    
    def unsubscribe_all(self) -> int:
        """Unsubscribe all subscribers."""
        return self._observable.unsubscribe_all()


class ReplaySubject(Generic[T]):
    """
    A Subject that replays a specified number of previous values to new subscribers.
    
    Example:
        events = ReplaySubject[int](buffer_size=3)
        
        events.next(1)
        events.next(2)
        events.next(3)
        
        # New subscriber receives last 3 values
        events.subscribe(lambda n: print(f"Event: {n}"))
        # Output: "Event: 1", "Event: 2", "Event: 3"
    """
    
    def __init__(self, buffer_size: int = 1):
        """
        Initialize with a buffer size.
        
        Args:
            buffer_size: Number of previous values to replay
        """
        self._buffer: deque = deque(maxlen=buffer_size)
        self._observable = Observable[T](name="ReplaySubject")
    
    def next(self, value: T) -> int:
        """
        Emit a new value.
        
        Args:
            value: Value to emit
            
        Returns:
            Number of subscribers notified
        """
        self._buffer.append(value)
        return self._observable.emit(data=value, event_name="default")
    
    def subscribe(
        self,
        callback: Callable[[T], Any],
        priority: Union[int, Priority] = Priority.NORMAL,
    ) -> Subscription[T]:
        """
        Subscribe to values.
        
        Args:
            callback: Function to call on value
            priority: Execution priority
            
        Returns:
            Subscription object
        """
        sub = self._observable.subscribe(
            callback=callback,
            event_name="default",
            priority=priority,
        )
        
        # Replay buffered values
        for value in self._buffer:
            try:
                callback(value)
            except Exception:
                pass
        
        return sub
    
    def unsubscribe_all(self) -> int:
        """Unsubscribe all subscribers."""
        return self._observable.unsubscribe_all()
    
    @property
    def buffer(self) -> List[T]:
        """Get current buffer."""
        return list(self._buffer)


def observable(
    event_name: str = "default",
    priority: Union[int, Priority] = Priority.NORMAL,
) -> Callable[[Callable[[EventData], Any]], Callable[[EventData], Any]]:
    """
    Decorator to create a simple observable function.
    
    When the decorated function is called, it emits to subscribers.
    
    Example:
        @observable("save")
        def save_file(filename):
            # Actual save logic here
            return True
        
        # Subscribe
        save_file.subscribe(lambda f: print(f"Saving: {f}"))
        
        # Call (triggers notification)
        save_file("data.txt")
    """
    obs = Observable[EventData]()
    
    def decorator(func: Callable[[EventData], Any]) -> Callable[[EventData], Any]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            obs.emit(data=result, event_name=event_name)
            return result
        
        wrapper.subscribe = obs.subscribe  # type: ignore
        wrapper.emit = obs.emit  # type: ignore
        
        return wrapper
    
    return decorator