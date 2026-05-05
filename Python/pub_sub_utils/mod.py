"""
AllToolkit - Python Publish/Subscribe Utilities

A zero-dependency, production-ready pub/sub (publish-subscribe) pattern implementation.
Supports topic-based messaging, wildcard subscriptions, message filtering, async handlers,
and comprehensive statistics tracking.

Author: AllToolkit
License: MIT
"""

import time
import threading
import re
import uuid
from typing import (
    Any, Callable, Dict, List, Optional, Set, Tuple, Union,
    TypeVar, Generic, Pattern
)
from dataclasses import dataclass, field
from functools import wraps
from enum import Enum
from collections import defaultdict
import queue
import weakref


T = TypeVar('T')
Handler = Callable[[Any], None]
AsyncHandler = Callable[[Any], Any]


class DeliveryMode(Enum):
    """Message delivery modes."""
    SYNC = "sync"          # Synchronous - block until all handlers complete
    ASYNC = "async"        # Asynchronous - handlers run in background threads
    FIRE_FORGET = "fire_forget"  # Fire and forget - no delivery guarantee


class MatchMode(Enum):
    """Topic matching modes."""
    EXACT = "exact"        # Exact match only
    PREFIX = "prefix"      # Prefix match (topic starts with pattern)
    WILDCARD = "wildcard"  # Wildcard match (* and > patterns)
    REGEX = "regex"        # Regular expression match


@dataclass
class Message:
    """Represents a published message."""
    topic: str
    payload: Any
    timestamp: float = field(default_factory=time.time)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    headers: Dict[str, Any] = field(default_factory=dict)
    publisher: Optional[str] = None
    priority: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            'topic': self.topic,
            'payload': self.payload,
            'timestamp': self.timestamp,
            'message_id': self.message_id,
            'headers': self.headers,
            'publisher': self.publisher,
            'priority': self.priority,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create message from dictionary."""
        return cls(
            topic=data['topic'],
            payload=data['payload'],
            timestamp=data.get('timestamp', time.time()),
            message_id=data.get('message_id', str(uuid.uuid4())),
            headers=data.get('headers', {}),
            publisher=data.get('publisher'),
            priority=data.get('priority', 0),
        )


@dataclass
class Subscription:
    """Represents a topic subscription."""
    subscriber_id: str
    topic_pattern: str
    handler: Handler
    match_mode: MatchMode = MatchMode.EXACT
    filter_func: Optional[Callable[[Message], bool]] = None
    priority: int = 0
    active: bool = True
    created_at: float = field(default_factory=time.time)
    _regex_pattern: Optional[Pattern] = field(default=None, repr=False)
    call_count: int = 0
    last_called: Optional[float] = None
    
    def __post_init__(self):
        """Compile regex pattern if needed."""
        if self.match_mode == MatchMode.REGEX:
            try:
                self._regex_pattern = re.compile(self.topic_pattern)
            except re.error:
                self._regex_pattern = None
    
    def matches(self, topic: str) -> bool:
        """Check if a topic matches this subscription's pattern."""
        if self.match_mode == MatchMode.EXACT:
            return topic == self.topic_pattern
        elif self.match_mode == MatchMode.PREFIX:
            return topic.startswith(self.topic_pattern)
        elif self.match_mode == MatchMode.WILDCARD:
            return self._wildcard_match(topic)
        elif self.match_mode == MatchMode.REGEX:
            if self._regex_pattern:
                return bool(self._regex_pattern.match(topic))
            return False
        return False
    
    def _wildcard_match(self, topic: str) -> bool:
        """
        Match topic against wildcard pattern.
        * matches a single level (e.g., 'user.*.created')
        > matches multiple levels (e.g., 'user.>')
        """
        pattern_parts = self.topic_pattern.split('.')
        topic_parts = topic.split('.')
        
        for i, p in enumerate(pattern_parts):
            if p == '>':
                # > matches all remaining levels
                return True
            if i >= len(topic_parts):
                return False
            if p != '*' and p != topic_parts[i]:
                return False
        
        return len(pattern_parts) == len(topic_parts)
    
    def should_handle(self, message: Message) -> bool:
        """Check if this subscription should handle a message."""
        if not self.active:
            return False
        if not self.matches(message.topic):
            return False
        if self.filter_func and not self.filter_func(message):
            return False
        return True


@dataclass
class PubSubStats:
    """Statistics for pub/sub operations."""
    messages_published: int = 0
    messages_delivered: int = 0
    messages_failed: int = 0
    total_subscriptions: int = 0
    active_subscriptions: int = 0
    total_handlers_called: int = 0
    total_time: float = 0.0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    
    def record_publish(self, deliveries: int, failures: int, time_taken: float) -> None:
        """Record a publish operation."""
        with self._lock:
            self.messages_published += 1
            self.messages_delivered += deliveries
            self.messages_failed += failures
            self.total_time += time_taken
    
    def record_handler_call(self) -> None:
        """Record a handler call."""
        with self._lock:
            self.total_handlers_called += 1
    
    def update_subscriptions(self, total: int, active: int) -> None:
        """Update subscription counts."""
        with self._lock:
            self.total_subscriptions = total
            self.active_subscriptions = active
    
    @property
    def avg_delivery_time(self) -> float:
        """Average time per publish."""
        if self.messages_published == 0:
            return 0.0
        return self.total_time / self.messages_published
    
    @property
    def delivery_rate(self) -> float:
        """Delivery success rate."""
        total = self.messages_delivered + self.messages_failed
        if total == 0:
            return 1.0
        return self.messages_delivered / total
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary."""
        return {
            'messages_published': self.messages_published,
            'messages_delivered': self.messages_delivered,
            'messages_failed': self.messages_failed,
            'total_subscriptions': self.total_subscriptions,
            'active_subscriptions': self.active_subscriptions,
            'total_handlers_called': self.total_handlers_called,
            'total_time': self.total_time,
            'avg_delivery_time': self.avg_delivery_time,
            'delivery_rate': self.delivery_rate,
        }
    
    def reset(self) -> None:
        """Reset all statistics."""
        with self._lock:
            self.messages_published = 0
            self.messages_delivered = 0
            self.messages_failed = 0
            self.total_subscriptions = 0
            self.active_subscriptions = 0
            self.total_handlers_called = 0
            self.total_time = 0.0


class PubSub:
    """
    A publish-subscribe message broker.
    
    Features:
    - Multiple subscription modes (exact, prefix, wildcard, regex)
    - Message filtering
    - Priority-based delivery
    - Synchronous and asynchronous delivery
    - Handler error handling
    - Statistics tracking
    - Thread-safe operations
    
    Example:
        >>> broker = PubSub()
        >>> 
        >>> # Subscribe to exact topic
        >>> broker.subscribe('user.created', lambda msg: print(f"User created: {msg.payload}"))
        >>> 
        >>> # Subscribe with wildcard
        >>> broker.subscribe('user.*', handler, match_mode=MatchMode.WILDCARD)
        >>> 
        >>> # Publish message
        >>> broker.publish('user.created', {'id': 1, 'name': 'Alice'})
    """
    
    def __init__(
        self,
        delivery_mode: DeliveryMode = DeliveryMode.SYNC,
        max_workers: int = 10,
        error_handler: Optional[Callable[[Exception, Message, Handler], None]] = None,
        stats: Optional[PubSubStats] = None,
    ):
        """
        Initialize the pub/sub broker.
        
        Args:
            delivery_mode: Default delivery mode for publications
            max_workers: Maximum worker threads for async delivery
            error_handler: Handler called when a subscriber throws an exception
            stats: Shared stats object for tracking
        """
        self._subscriptions: Dict[str, Subscription] = {}
        self._topic_index: Dict[str, Set[str]] = defaultdict(set)
        self._lock = threading.RLock()
        self._worker_queue: Optional[queue.Queue] = None
        self._workers: List[threading.Thread] = []
        self.delivery_mode = delivery_mode
        self.max_workers = max_workers
        self.error_handler = error_handler
        self.stats = stats or PubSubStats()
        
        if delivery_mode in (DeliveryMode.ASYNC, DeliveryMode.FIRE_FORGET):
            self._start_workers()
    
    def _start_workers(self) -> None:
        """Start worker threads for async delivery."""
        self._worker_queue = queue.Queue()
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self._workers.append(worker)
    
    def _worker_loop(self) -> None:
        """Worker thread loop for async delivery."""
        while True:
            try:
                task = self._worker_queue.get()
                if task is None:  # Shutdown signal
                    break
                handler, message = task
                try:
                    handler(message.payload)
                except Exception as e:
                    if self.error_handler:
                        self.error_handler(e, message, handler)
                self.stats.record_handler_call()
                self._worker_queue.task_done()
            except Exception:
                pass
    
    def subscribe(
        self,
        topic_pattern: str,
        handler: Handler,
        match_mode: MatchMode = MatchMode.EXACT,
        filter_func: Optional[Callable[[Message], bool]] = None,
        priority: int = 0,
        subscriber_id: Optional[str] = None,
    ) -> str:
        """
        Subscribe to a topic pattern.
        
        Args:
            topic_pattern: Topic pattern to subscribe to
            handler: Function to call when message is received
            match_mode: How to match topics (exact, prefix, wildcard, regex)
            filter_func: Optional filter function to further filter messages
            priority: Higher priority handlers are called first
            subscriber_id: Optional custom subscriber ID
        
        Returns:
            Subscriber ID (can be used to unsubscribe)
        
        Example:
            >>> def handle_user(msg):
            ...     print(f"User event: {msg.topic}")
            >>> 
            >>> # Exact match
            >>> broker.subscribe('user.created', handle_user)
            >>> 
            >>> # Prefix match
            >>> broker.subscribe('user.', handle_user, match_mode=MatchMode.PREFIX)
            >>> 
            >>> # Wildcard match
            >>> broker.subscribe('user.*.created', handle_user, match_mode=MatchMode.WILDCARD)
            >>> broker.subscribe('user.>', handle_user, match_mode=MatchMode.WILDCARD)
            >>> 
            >>> # Regex match
            >>> broker.subscribe(r'user\.\d+\.created', handle_user, match_mode=MatchMode.REGEX)
            >>> 
            >>> # With filter
            >>> broker.subscribe('order.*', handle_order, 
            ...                  filter_func=lambda msg: msg.payload.get('amount', 0) > 100)
        """
        subscriber_id = subscriber_id or str(uuid.uuid4())
        
        subscription = Subscription(
            subscriber_id=subscriber_id,
            topic_pattern=topic_pattern,
            handler=handler,
            match_mode=match_mode,
            filter_func=filter_func,
            priority=priority,
        )
        
        with self._lock:
            self._subscriptions[subscriber_id] = subscription
            # Index by exact topic for quick lookup
            if match_mode == MatchMode.EXACT:
                self._topic_index[topic_pattern].add(subscriber_id)
            else:
                # Non-exact patterns need to be checked against all topics
                self._topic_index['__pattern__'].add(subscriber_id)
            
            self._update_stats()
        
        return subscriber_id
    
    def unsubscribe(self, subscriber_id: str) -> bool:
        """
        Unsubscribe from a topic.
        
        Args:
            subscriber_id: Subscriber ID returned from subscribe()
        
        Returns:
            True if subscription was found and removed, False otherwise
        """
        with self._lock:
            if subscriber_id not in self._subscriptions:
                return False
            
            subscription = self._subscriptions[subscriber_id]
            
            # Remove from index
            if subscription.match_mode == MatchMode.EXACT:
                self._topic_index[subscription.topic_pattern].discard(subscriber_id)
            else:
                self._topic_index['__pattern__'].discard(subscriber_id)
            
            del self._subscriptions[subscriber_id]
            self._update_stats()
        
        return True
    
    def publish(
        self,
        topic: str,
        payload: Any,
        headers: Optional[Dict[str, Any]] = None,
        publisher: Optional[str] = None,
        priority: int = 0,
        delivery_mode: Optional[DeliveryMode] = None,
    ) -> Tuple[int, int]:
        """
        Publish a message to a topic.
        
        Args:
            topic: Topic to publish to
            payload: Message payload
            headers: Optional message headers
            publisher: Optional publisher identifier
            priority: Message priority
            delivery_mode: Override default delivery mode
        
        Returns:
            Tuple of (successful deliveries, failed deliveries)
        
        Example:
            >>> broker.publish('user.created', {'id': 1, 'name': 'Alice'})
            >>> broker.publish('user.updated', {'id': 1, 'name': 'Bob'}, 
            ...                headers={'source': 'admin'})
        """
        delivery_mode = delivery_mode or self.delivery_mode
        
        message = Message(
            topic=topic,
            payload=payload,
            headers=headers or {},
            publisher=publisher,
            priority=priority,
        )
        
        start_time = time.time()
        deliveries = 0
        failures = 0
        
        # Find matching subscriptions
        matching = self._find_matching_subscriptions(message)
        
        # Sort by priority (higher first)
        matching.sort(key=lambda s: s.priority, reverse=True)
        
        for subscription in matching:
            try:
                if delivery_mode == DeliveryMode.SYNC:
                    subscription.handler(message.payload)
                    self.stats.record_handler_call()
                    deliveries += 1
                elif delivery_mode in (DeliveryMode.ASYNC, DeliveryMode.FIRE_FORGET):
                    if self._worker_queue:
                        self._worker_queue.put((subscription.handler, message))
                    deliveries += 1
                
                # Update subscription stats
                subscription.call_count += 1
                subscription.last_called = time.time()
                
            except Exception as e:
                failures += 1
                if self.error_handler and delivery_mode == DeliveryMode.SYNC:
                    self.error_handler(e, message, subscription.handler)
        
        # Record stats
        time_taken = time.time() - start_time
        self.stats.record_publish(deliveries, failures, time_taken)
        
        return deliveries, failures
    
    def _find_matching_subscriptions(self, message: Message) -> List[Subscription]:
        """Find all subscriptions that match a message."""
        with self._lock:
            matching = []
            
            # Check exact matches first
            exact_ids = self._topic_index.get(message.topic, set())
            for sid in exact_ids:
                sub = self._subscriptions.get(sid)
                if sub and sub.should_handle(message):
                    matching.append(sub)
            
            # Check pattern matches
            pattern_ids = self._topic_index.get('__pattern__', set())
            for sid in pattern_ids:
                sub = self._subscriptions.get(sid)
                if sub and sub.should_handle(message):
                    matching.append(sub)
            
            return matching
    
    def _update_stats(self) -> None:
        """Update subscription statistics."""
        total = len(self._subscriptions)
        active = sum(1 for s in self._subscriptions.values() if s.active)
        self.stats.update_subscriptions(total, active)
    
    def get_subscription(self, subscriber_id: str) -> Optional[Subscription]:
        """Get a subscription by ID."""
        return self._subscriptions.get(subscriber_id)
    
    def get_subscriptions_for_topic(self, topic: str) -> List[Subscription]:
        """Get all subscriptions that would match a topic."""
        message = Message(topic=topic, payload=None)
        return self._find_matching_subscriptions(message)
    
    def pause_subscription(self, subscriber_id: str) -> bool:
        """Pause a subscription (temporarily stop receiving messages)."""
        with self._lock:
            if subscriber_id not in self._subscriptions:
                return False
            self._subscriptions[subscriber_id].active = False
            self._update_stats()
        return True
    
    def resume_subscription(self, subscriber_id: str) -> bool:
        """Resume a paused subscription."""
        with self._lock:
            if subscriber_id not in self._subscriptions:
                return False
            self._subscriptions[subscriber_id].active = True
            self._update_stats()
        return True
    
    def clear_topic(self, topic_pattern: str) -> int:
        """Remove all subscriptions for a topic pattern. Returns count removed."""
        with self._lock:
            to_remove = [
                sid for sid, sub in self._subscriptions.items()
                if sub.topic_pattern == topic_pattern
            ]
            for sid in to_remove:
                self.unsubscribe(sid)
            return len(to_remove)
    
    def clear_all(self) -> int:
        """Remove all subscriptions. Returns count removed."""
        with self._lock:
            count = len(self._subscriptions)
            self._subscriptions.clear()
            self._topic_index.clear()
            self._update_stats()
        return count
    
    def get_topics(self) -> Set[str]:
        """Get all unique topic patterns currently subscribed."""
        with self._lock:
            return {sub.topic_pattern for sub in self._subscriptions.values()}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        return self.stats.to_dict()
    
    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats.reset()
    
    def shutdown(self, wait: bool = True, timeout: Optional[float] = None) -> None:
        """
        Shutdown the broker, stopping worker threads.
        
        Args:
            wait: Wait for workers to finish
            timeout: Maximum time to wait
        """
        if self._worker_queue:
            # Send shutdown signals
            for _ in self._workers:
                self._worker_queue.put(None)
            
            if wait:
                for worker in self._workers:
                    worker.join(timeout)


def subscribe(
    topic_pattern: str,
    match_mode: MatchMode = MatchMode.EXACT,
    filter_func: Optional[Callable[[Message], bool]] = None,
    priority: int = 0,
    broker: Optional[PubSub] = None,
) -> Callable[[Handler], Handler]:
    """
    Decorator to subscribe a function to a topic.
    
    Args:
        topic_pattern: Topic pattern to subscribe to
        match_mode: How to match topics
        filter_func: Optional filter function
        priority: Handler priority
        broker: Broker instance (uses global if None)
    
    Returns:
        Decorated function
    
    Example:
        >>> @subscribe('user.created')
        ... def handle_user_created(payload):
        ...     print(f"User created: {payload}")
        >>> 
        >>> @subscribe('user.*', match_mode=MatchMode.WILDCARD)
        ... def handle_all_user_events(payload):
        ...     print(f"User event: {payload}")
    """
    def decorator(func: Handler) -> Handler:
        _broker = broker or _global_broker
        _broker.subscribe(
            topic_pattern=topic_pattern,
            handler=func,
            match_mode=match_mode,
            filter_func=filter_func,
            priority=priority,
        )
        return func
    return decorator


# Global broker instance
_global_broker = PubSub()
_global_stats = PubSubStats()


def get_global_broker() -> PubSub:
    """Get the global pub/sub broker instance."""
    return _global_broker


def publish(
    topic: str,
    payload: Any,
    headers: Optional[Dict[str, Any]] = None,
    publisher: Optional[str] = None,
    priority: int = 0,
) -> Tuple[int, int]:
    """Publish to the global broker."""
    return _global_broker.publish(topic, payload, headers, publisher, priority)


def get_global_stats() -> PubSubStats:
    """Get global pub/sub statistics."""
    return _global_stats


def reset_global_stats() -> None:
    """Reset global statistics."""
    _global_stats.reset()


class Topic:
    """
    A typed topic wrapper for convenient publishing.
    
    Example:
        >>> user_topic = Topic('user')
        >>> user_topic.publish('created', {'id': 1})
        >>> # publishes to 'user.created'
        >>> 
        >>> order_topic = Topic('order', broker=my_broker)
        >>> order_topic.publish('updated', {'id': 123})
    """
    
    def __init__(
        self,
        prefix: str,
        broker: Optional[PubSub] = None,
        separator: str = '.',
    ):
        """
        Initialize a topic wrapper.
        
        Args:
            prefix: Topic prefix (e.g., 'user')
            broker: Broker instance (uses global if None)
            separator: Topic separator (default: '.')
        """
        self.prefix = prefix
        self._broker = broker or _global_broker
        self.separator = separator
    
    def publish(
        self,
        subtopic: str,
        payload: Any,
        headers: Optional[Dict[str, Any]] = None,
        publisher: Optional[str] = None,
        priority: int = 0,
    ) -> Tuple[int, int]:
        """Publish to a subtopic under this topic."""
        full_topic = f"{self.prefix}{self.separator}{subtopic}"
        return self._broker.publish(full_topic, payload, headers, publisher, priority)
    
    def subscribe(
        self,
        subtopic: str,
        handler: Handler,
        match_mode: MatchMode = MatchMode.EXACT,
        filter_func: Optional[Callable[[Message], bool]] = None,
        priority: int = 0,
    ) -> str:
        """Subscribe to a subtopic under this topic."""
        full_topic = f"{self.prefix}{self.separator}{subtopic}"
        return self._broker.subscribe(
            topic_pattern=full_topic,
            handler=handler,
            match_mode=match_mode,
            filter_func=filter_func,
            priority=priority,
        )
    
    def child(self, subtopic: str) -> 'Topic':
        """Create a child topic with extended prefix."""
        return Topic(
            prefix=f"{self.prefix}{self.separator}{subtopic}",
            broker=self._broker,
            separator=self.separator,
        )


class EventEmitter:
    """
    A simpler event emitter pattern implementation.
    
    Example:
        >>> emitter = EventEmitter()
        >>> 
        >>> @emitter.on('data')
        ... def handle_data(data):
        ...     print(f"Received: {data}")
        >>> 
        >>> emitter.emit('data', {'value': 42})
        >>> emitter.emit('data', value=42)  # also works with kwargs
        >>> 
        >>> # One-time listener
        >>> emitter.once('init', lambda: print("Initialized!"))
        >>> 
        >>> # Remove listener
        >>> handler_id = emitter.on('event', my_handler)
        >>> emitter.off(handler_id)
    """
    
    def __init__(self):
        """Initialize the event emitter."""
        self._listeners: Dict[str, Dict[str, Tuple[Callable, bool]]] = defaultdict(dict)
        self._lock = threading.RLock()
    
    def on(
        self,
        event: str,
        handler: Optional[Callable] = None,
    ) -> Union[str, Callable]:
        """
        Register an event listener.
        
        Args:
            event: Event name
            handler: Handler function (if None, acts as decorator)
        
        Returns:
            Handler ID (or decorator if no handler provided)
        
        Example:
            >>> @emitter.on('event')
            ... def handler(data):
            ...     pass
            >>> 
            >>> # Or directly:
            >>> handler_id = emitter.on('event', my_handler)
        """
        def register(h: Callable) -> str:
            handler_id = str(uuid.uuid4())
            with self._lock:
                self._listeners[event][handler_id] = (h, False)
            return handler_id
        
        if handler is not None:
            return register(handler)
        return register
    
    def once(self, event: str, handler: Callable) -> str:
        """Register a one-time event listener."""
        handler_id = str(uuid.uuid4())
        with self._lock:
            self._listeners[event][handler_id] = (handler, True)
        return handler_id
    
    def off(self, handler_id: str, event: Optional[str] = None) -> bool:
        """Remove an event listener."""
        with self._lock:
            if event:
                if event in self._listeners and handler_id in self._listeners[event]:
                    del self._listeners[event][handler_id]
                    return True
            else:
                for event_listeners in self._listeners.values():
                    if handler_id in event_listeners:
                        del event_listeners[handler_id]
                        return True
        return False
    
    def emit(self, event: str, *args, **kwargs) -> int:
        """
        Emit an event.
        
        Args:
            event: Event name
            *args: Positional arguments to pass to handlers
            **kwargs: Keyword arguments to pass to handlers
        
        Returns:
            Number of handlers called
        """
        called = 0
        to_remove = []
        
        with self._lock:
            if event not in self._listeners:
                return 0
            
            for handler_id, (handler, once) in list(self._listeners[event].items()):
                try:
                    handler(*args, **kwargs)
                    called += 1
                except Exception:
                    pass  # Ignore handler errors
                
                if once:
                    to_remove.append(handler_id)
            
            for handler_id in to_remove:
                del self._listeners[event][handler_id]
        
        return called
    
    def listeners(self, event: str) -> List[Callable]:
        """Get all listeners for an event."""
        with self._lock:
            return [h for h, _ in self._listeners.get(event, {}).values()]
    
    def event_names(self) -> Set[str]:
        """Get all event names with listeners."""
        with self._lock:
            return set(self._listeners.keys())
    
    def remove_all_listeners(self, event: Optional[str] = None) -> int:
        """Remove all listeners for an event (or all events)."""
        with self._lock:
            if event:
                count = len(self._listeners.get(event, {}))
                if event in self._listeners:
                    del self._listeners[event]
                return count
            else:
                count = sum(len(l) for l in self._listeners.values())
                self._listeners.clear()
                return count


# Convenience exports
__all__ = [
    'PubSub',
    'Message',
    'Subscription',
    'PubSubStats',
    'DeliveryMode',
    'MatchMode',
    'Topic',
    'EventEmitter',
    'subscribe',
    'publish',
    'get_global_broker',
    'get_global_stats',
    'reset_global_stats',
]