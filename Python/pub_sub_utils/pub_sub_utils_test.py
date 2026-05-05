"""
AllToolkit - Python Publish/Subscribe Utilities Tests

Comprehensive test suite covering all pub/sub functionality.

Run with: python pub_sub_utils_test.py
"""

import sys
import os
import time
import threading

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    PubSub, Message, Subscription, PubSubStats,
    DeliveryMode, MatchMode, Topic, EventEmitter,
    subscribe, publish, get_global_broker, get_global_stats, reset_global_stats,
)


class TestResult:
    """Test result collector."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def success(self, name: str):
        self.passed += 1
        print(f"  ✅ {name}")
    
    def fail(self, name: str, error: str):
        self.failed += 1
        self.errors.append((name, error))
        print(f"  ❌ {name}: {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}")
        if self.errors:
            print("\nFailed tests:")
            for name, error in self.errors:
                print(f"  - {name}: {error}")
        print('='*60)
        return self.failed == 0


results = TestResult()


def test(name: str):
    """Test decorator."""
    def decorator(func):
        def wrapper():
            try:
                func()
                results.success(name)
            except AssertionError as e:
                results.fail(name, str(e))
            except Exception as e:
                results.fail(name, f"Unexpected error: {e}")
        wrapper._test_name = name
        return wrapper
    return decorator


# ============== Message Tests ==============

@test("Message: Create message with defaults")
def test_message_create_defaults():
    msg = Message(topic='test', payload={'data': 42})
    assert msg.topic == 'test'
    assert msg.payload == {'data': 42}
    assert isinstance(msg.message_id, str)
    assert isinstance(msg.timestamp, float)
    assert msg.headers == {}
    assert msg.publisher is None
    assert msg.priority == 0


@test("Message: Create message with custom values")
def test_message_create_custom():
    msg = Message(
        topic='custom',
        payload='hello',
        message_id='msg-123',
        timestamp=1000.0,
        headers={'source': 'test'},
        publisher='sender-1',
        priority=10
    )
    assert msg.topic == 'custom'
    assert msg.payload == 'hello'
    assert msg.message_id == 'msg-123'
    assert msg.timestamp == 1000.0
    assert msg.headers == {'source': 'test'}
    assert msg.publisher == 'sender-1'
    assert msg.priority == 10


@test("Message: Convert to/from dictionary")
def test_message_dict_conversion():
    msg = Message(
        topic='test',
        payload={'x': 1},
        message_id='id-1',
        headers={'h': 2}
    )
    d = msg.to_dict()
    assert d['topic'] == 'test'
    assert d['payload'] == {'x': 1}
    
    restored = Message.from_dict(d)
    assert restored.topic == msg.topic
    assert restored.payload == msg.payload
    assert restored.message_id == msg.message_id


# ============== Subscription Tests ==============

@test("Subscription: Exact match")
def test_subscription_exact_match():
    sub = Subscription(
        subscriber_id='sub-1',
        topic_pattern='user.created',
        handler=lambda x: None
    )
    assert sub.match_mode == MatchMode.EXACT
    assert sub.matches('user.created')
    assert not sub.matches('user.updated')
    assert not sub.matches('user')


@test("Subscription: Prefix match")
def test_subscription_prefix_match():
    sub = Subscription(
        subscriber_id='sub-2',
        topic_pattern='user.',
        handler=lambda x: None,
        match_mode=MatchMode.PREFIX
    )
    assert sub.matches('user.created')
    assert sub.matches('user.updated')
    assert sub.matches('user.deleted')
    assert not sub.matches('order.created')
    assert not sub.matches('user')  # No trailing dot


@test("Subscription: Wildcard match - single level")
def test_subscription_wildcard_single():
    sub = Subscription(
        subscriber_id='sub-3',
        topic_pattern='user.*.created',
        handler=lambda x: None,
        match_mode=MatchMode.WILDCARD
    )
    assert sub.matches('user.1.created')
    assert sub.matches('user.admin.created')
    assert not sub.matches('user.1.2.created')
    assert not sub.matches('user.created')


@test("Subscription: Wildcard match - multi level")
def test_subscription_wildcard_multi():
    sub = Subscription(
        subscriber_id='sub-4',
        topic_pattern='user.>',
        handler=lambda x: None,
        match_mode=MatchMode.WILDCARD
    )
    assert sub.matches('user.created')
    assert sub.matches('user.1.created')
    assert sub.matches('user.1.2.3')
    assert not sub.matches('order.created')


@test("Subscription: Regex match")
def test_subscription_regex_match():
    sub = Subscription(
        subscriber_id='sub-5',
        topic_pattern=r'user\.\d+\.created',
        handler=lambda x: None,
        match_mode=MatchMode.REGEX
    )
    assert sub.matches('user.123.created')
    assert sub.matches('user.1.created')
    assert not sub.matches('user.admin.created')
    assert not sub.matches('user.created')


@test("Subscription: Filter function")
def test_subscription_filter():
    def filter_high_priority(msg: Message) -> bool:
        return msg.payload.get('priority', 0) > 5
    
    sub = Subscription(
        subscriber_id='sub-6',
        topic_pattern='test',
        handler=lambda x: None,
        filter_func=filter_high_priority
    )
    
    msg_high = Message(topic='test', payload={'priority': 10})
    msg_low = Message(topic='test', payload={'priority': 2})
    
    assert sub.should_handle(msg_high)
    assert not sub.should_handle(msg_low)


@test("Subscription: Inactive subscription")
def test_subscription_inactive():
    sub = Subscription(
        subscriber_id='sub-7',
        topic_pattern='test',
        handler=lambda x: None,
        active=False
    )
    msg = Message(topic='test', payload=None)
    assert not sub.should_handle(msg)


# ============== PubSub Tests ==============

@test("PubSub: Subscribe and publish - exact match")
def test_pubsub_exact_match():
    broker = PubSub()
    received = []
    
    sub_id = broker.subscribe('test', lambda x: received.append(x))
    broker.publish('test', 'hello')
    broker.publish('other', 'ignored')
    
    assert received == ['hello']
    assert broker.unsubscribe(sub_id)


@test("PubSub: Subscribe and publish - prefix match")
def test_pubsub_prefix_match():
    broker = PubSub()
    received = []
    
    broker.subscribe('user.', lambda x: received.append(x), match_mode=MatchMode.PREFIX)
    broker.publish('user.created', 'data1')
    broker.publish('user.updated', 'data2')
    broker.publish('order.created', 'data3')
    
    assert received == ['data1', 'data2']


@test("PubSub: Subscribe and publish - wildcard match")
def test_pubsub_wildcard_match():
    broker = PubSub()
    received = []
    
    broker.subscribe('user.*', lambda x: received.append(x), match_mode=MatchMode.WILDCARD)
    broker.publish('user.created', 'a')
    broker.publish('user.updated', 'b')
    broker.publish('user.deleted', 'c')
    broker.publish('user.created.admin', 'd')  # Should NOT match
    
    assert received == ['a', 'b', 'c']


@test("PubSub: Subscribe and publish - multi-level wildcard")
def test_pubsub_wildcard_multi():
    broker = PubSub()
    received = []
    
    broker.subscribe('user.>', lambda x: received.append(x), match_mode=MatchMode.WILDCARD)
    broker.publish('user.created', 'a')
    broker.publish('user.1.created', 'b')
    broker.publish('user.1.2.3', 'c')
    broker.publish('order.created', 'd')  # Should NOT match
    
    assert received == ['a', 'b', 'c']


@test("PubSub: Multiple subscribers")
def test_pubsub_multiple_subscribers():
    broker = PubSub()
    received1 = []
    received2 = []
    
    broker.subscribe('test', lambda x: received1.append(x))
    broker.subscribe('test', lambda x: received2.append(x))
    
    broker.publish('test', 'data')
    
    assert received1 == ['data']
    assert received2 == ['data']


@test("PubSub: Priority ordering")
def test_pubsub_priority():
    broker = PubSub()
    order = []
    
    def make_handler(name):
        return lambda x: order.append(name)
    
    broker.subscribe('test', make_handler('low'), priority=0)
    broker.subscribe('test', make_handler('high'), priority=10)
    broker.subscribe('test', make_handler('mid'), priority=5)
    
    broker.publish('test', 'data')
    
    assert order == ['high', 'mid', 'low']


@test("PubSub: Unsubscribe")
def test_pubsub_unsubscribe():
    broker = PubSub()
    received = []
    
    sub_id = broker.subscribe('test', lambda x: received.append(x))
    broker.publish('test', 'first')
    
    broker.unsubscribe(sub_id)
    broker.publish('test', 'second')  # Should not be received
    
    assert received == ['first']
    assert not broker.unsubscribe(sub_id)  # Already unsubscribed


@test("PubSub: Pause and resume subscription")
def test_pubsub_pause_resume():
    broker = PubSub()
    received = []
    
    sub_id = broker.subscribe('test', lambda x: received.append(x))
    broker.publish('test', 'first')
    
    broker.pause_subscription(sub_id)
    broker.publish('test', 'paused')  # Should not be received
    
    broker.resume_subscription(sub_id)
    broker.publish('test', 'resumed')
    
    assert received == ['first', 'resumed']


@test("PubSub: Message headers")
def test_pubsub_headers():
    broker = PubSub()
    received_headers = []
    
    def handler_with_headers(payload):
        # Headers are not passed to handler by default in sync mode
        received_headers.append(payload)
    
    broker.subscribe('test', handler_with_headers)
    broker.publish('test', {'data': 1}, headers={'source': 'sender'})
    
    assert received_headers == [{'data': 1}]


@test("PubSub: Statistics tracking")
def test_pubsub_stats():
    broker = PubSub()
    broker.subscribe('test', lambda x: None)
    
    broker.publish('test', 'a')
    broker.publish('test', 'b')
    broker.publish('other', 'c')  # No subscribers
    
    stats = broker.get_stats()
    assert stats['messages_published'] == 3
    assert stats['messages_delivered'] == 2
    assert stats['delivery_rate'] >= 0.5


@test("PubSub: Clear all subscriptions")
def test_pubsub_clear_all():
    broker = PubSub()
    
    broker.subscribe('test1', lambda x: None)
    broker.subscribe('test2', lambda x: None)
    
    count = broker.clear_all()
    
    assert count == 2
    stats = broker.get_stats()
    assert stats['total_subscriptions'] == 0


@test("PubSub: Get subscriptions for topic")
def test_pubsub_get_subscriptions():
    broker = PubSub()
    
    broker.subscribe('user.created', lambda x: None)
    broker.subscribe('user.*', lambda x: None, match_mode=MatchMode.WILDCARD)
    broker.subscribe('order', lambda x: None)
    
    subs = broker.get_subscriptions_for_topic('user.created')
    assert len(subs) == 2
    
    subs = broker.get_subscriptions_for_topic('order')
    assert len(subs) == 1


@test("PubSub: Error handling")
def test_pubsub_error_handling():
    broker = PubSub()
    errors = []
    
    def error_handler(exc, msg, handler):
        errors.append(str(exc))
    
    broker.error_handler = error_handler
    broker.subscribe('test', lambda x: exec("raise ValueError('test error')"))
    
    broker.publish('test', 'data')
    
    assert len(errors) == 1
    assert 'test error' in errors[0]


# ============== Topic Tests ==============

@test("Topic: Publish with prefix")
def test_topic_publish():
    broker = PubSub()
    received = []
    
    topic = Topic('user', broker)
    broker.subscribe('user.created', lambda x: received.append(x))
    
    topic.publish('created', {'id': 1})
    
    assert received == [{'id': 1}]


@test("Topic: Subscribe with prefix")
def test_topic_subscribe():
    broker = PubSub()
    received = []
    
    topic = Topic('user', broker)
    topic.subscribe('created', lambda x: received.append(x))
    
    broker.publish('user.created', 'data')
    
    assert received == ['data']


@test("Topic: Child topic")
def test_topic_child():
    broker = PubSub()
    received = []
    
    user_topic = Topic('user', broker)
    admin_topic = user_topic.child('admin')
    
    admin_topic.subscribe('created', lambda x: received.append(x))
    broker.publish('user.admin.created', 'data')
    
    assert received == ['data']


# ============== EventEmitter Tests ==============

@test("EventEmitter: Basic emit")
def test_emitter_basic():
    emitter = EventEmitter()
    received = []
    
    emitter.on('data', lambda x: received.append(x))
    emitter.emit('data', 'hello')
    
    assert received == ['hello']


@test("EventEmitter: Decorator syntax")
def test_emitter_decorator():
    emitter = EventEmitter()
    received = []
    
    @emitter.on('event')
    def handler(data):
        received.append(data)
    
    emitter.emit('event', 'test')
    assert received == ['test']


@test("EventEmitter: Once listener")
def test_emitter_once():
    emitter = EventEmitter()
    received = []
    
    emitter.once('init', lambda x: received.append(x))
    emitter.emit('init', 'first')
    emitter.emit('init', 'second')
    
    assert received == ['first']


@test("EventEmitter: Remove listener")
def test_emitter_off():
    emitter = EventEmitter()
    received = []
    
    handler_id = emitter.on('test', lambda x: received.append(x))
    emitter.emit('test', 'a')
    
    emitter.off(handler_id)
    emitter.emit('test', 'b')
    
    assert received == ['a']


@test("EventEmitter: Multiple arguments")
def test_emitter_multiple_args():
    emitter = EventEmitter()
    received = []
    
    emitter.on('multi', lambda a, b: received.append((a, b)))
    emitter.emit('multi', 'x', 'y')
    
    assert received == [('x', 'y')]


@test("EventEmitter: Keyword arguments")
def test_emitter_kwargs():
    emitter = EventEmitter()
    received = []
    
    emitter.on('kwargs', lambda **kw: received.append(kw))
    emitter.emit('kwargs', a=1, b=2)
    
    assert received == [{'a': 1, 'b': 2}]


@test("EventEmitter: List listeners")
def test_emitter_listeners():
    emitter = EventEmitter()
    
    emitter.on('test', lambda x: x)
    emitter.on('test', lambda x: x * 2)
    
    listeners = emitter.listeners('test')
    assert len(listeners) == 2


@test("EventEmitter: Remove all listeners")
def test_emitter_remove_all():
    emitter = EventEmitter()
    
    emitter.on('test', lambda x: x)
    emitter.on('test', lambda x: x * 2)
    
    count = emitter.remove_all_listeners('test')
    assert count == 2
    assert emitter.listeners('test') == []


# ============== Global Broker Tests ==============

@test("Global broker: Publish and subscribe")
def test_global_broker():
    reset_global_stats()
    broker = get_global_broker()
    received = []
    
    sub_id = broker.subscribe('global.test', lambda x: received.append(x))
    publish('global.test', 'data')
    
    assert received == ['data']
    
    broker.unsubscribe(sub_id)
    broker.clear_all()


@test("Subscribe decorator")
def test_subscribe_decorator():
    reset_global_stats()
    broker = get_global_broker()
    received = []
    
    @subscribe('decorated.test')
    def handler(payload):
        received.append(payload)
    
    publish('decorated.test', 'decorated data')
    
    assert received == ['decorated data']
    
    broker.clear_all()


# ============== MatchMode Tests ==============

@test("MatchMode: All modes available")
def test_match_modes():
    modes = [MatchMode.EXACT, MatchMode.PREFIX, MatchMode.WILDCARD, MatchMode.REGEX]
    for mode in modes:
        assert mode.value in ['exact', 'prefix', 'wildcard', 'regex']


# ============== DeliveryMode Tests ==============

@test("DeliveryMode: All modes available")
def test_delivery_modes():
    modes = [DeliveryMode.SYNC, DeliveryMode.ASYNC, DeliveryMode.FIRE_FORGET]
    for mode in modes:
        assert mode.value in ['sync', 'async', 'fire_forget']


# ============== Thread Safety Tests ==============

@test("PubSub: Thread-safe subscribe")
def test_pubsub_thread_safe_subscribe():
    broker = PubSub()
    sub_ids = []
    
    def subscribe_thread(i):
        sub_id = broker.subscribe(f'topic.{i}', lambda x: None)
        sub_ids.append(sub_id)
    
    threads = [threading.Thread(target=subscribe_thread, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # 10 unique subscription IDs
    assert len(sub_ids) == 10
    stats = broker.get_stats()
    assert stats['total_subscriptions'] == 10


@test("PubSub: Thread-safe publish")
def test_pubsub_thread_safe_publish():
    broker = PubSub()
    received = []
    
    broker.subscribe('counter', lambda x: received.append(x))
    
    def publish_thread(i):
        broker.publish('counter', i)
    
    threads = [threading.Thread(target=publish_thread, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # All values should be received
    assert len(received) == 10
    assert set(received) == set(range(10))


# ============== Edge Cases Tests ==============

@test("PubSub: Empty topic")
def test_pubsub_empty_topic():
    broker = PubSub()
    received = []
    
    broker.subscribe('', lambda x: received.append(x))
    broker.publish('', 'empty')
    
    assert received == ['empty']


@test("PubSub: None payload")
def test_pubsub_none_payload():
    broker = PubSub()
    received = []
    
    broker.subscribe('test', lambda x: received.append(x))
    broker.publish('test', None)
    
    assert received == [None]


@test("PubSub: No subscribers")
def test_pubsub_no_subscribers():
    broker = PubSub()
    
    deliveries, failures = broker.publish('no.subscribers', 'data')
    
    assert deliveries == 0
    assert failures == 0


@test("PubSub: Invalid regex pattern")
def test_pubsub_invalid_regex():
    sub = Subscription(
        subscriber_id='sub-invalid',
        topic_pattern='[invalid',
        handler=lambda x: None,
        match_mode=MatchMode.REGEX
    )
    # Should not crash, just return False for matches
    assert not sub.matches('test')


@test("PubSub: Stats reset")
def test_pubsub_stats_reset():
    broker = PubSub()
    broker.subscribe('test', lambda x: None)
    broker.publish('test', 'a')
    
    broker.reset_stats()
    stats = broker.get_stats()
    
    assert stats['messages_published'] == 0


@test("EventEmitter: Emit with no listeners")
def test_emitter_emit_no_listeners():
    emitter = EventEmitter()
    
    count = emitter.emit('no.listeners', 'data')
    
    assert count == 0


@test("EventEmitter: Remove non-existent listener")
def test_emitter_remove_nonexistent():
    emitter = EventEmitter()
    
    result = emitter.off('nonexistent-id')
    
    assert not result


# ============== Complex Tests ==============

@test("PubSub: Complex wildcard pattern")
def test_pubsub_complex_wildcard():
    broker = PubSub()
    received = []
    
    broker.subscribe('app.*.*.error', lambda x: received.append(x), match_mode=MatchMode.WILDCARD)
    
    broker.publish('app.module.service.error', 'a')  # Match
    broker.publish('app.module.error', 'b')          # No match
    broker.publish('app.a.b.error', 'c')             # Match
    broker.publish('app.x.y.z.error', 'd')           # No match
    
    assert received == ['a', 'c']


@test("PubSub: Mixed wildcard and exact")
def test_pubsub_mixed_patterns():
    broker = PubSub()
    exact_received = []
    wildcard_received = []
    
    broker.subscribe('user.created', lambda x: exact_received.append(x))
    broker.subscribe('user.*', lambda x: wildcard_received.append(x), match_mode=MatchMode.WILDCARD)
    
    broker.publish('user.created', 'data')
    
    # Both should receive
    assert exact_received == ['data']
    assert wildcard_received == ['data']


@test("PubSub: Subscription call count tracking")
def test_pubsub_call_count():
    broker = PubSub()
    
    sub_id = broker.subscribe('test', lambda x: None)
    
    broker.publish('test', 'a')
    broker.publish('test', 'b')
    broker.publish('test', 'c')
    
    sub = broker.get_subscription(sub_id)
    assert sub.call_count == 3
    assert sub.last_called is not None


@test("PubSub: Clear specific topic")
def test_pubsub_clear_topic():
    broker = PubSub()
    
    broker.subscribe('topic.a', lambda x: None)
    broker.subscribe('topic.b', lambda x: None)
    broker.subscribe('other', lambda x: None)
    
    count = broker.clear_topic('topic.a')
    
    assert count == 1
    stats = broker.get_stats()
    assert stats['total_subscriptions'] == 2


# Run all tests
if __name__ == '__main__':
    print("\n" + "="*60)
    print("AllToolkit - Pub/Sub Utilities Tests")
    print("="*60 + "\n")
    
    # Collect and run all test functions
    test_functions = [
        v for k, v in globals().items()
        if callable(v) and hasattr(v, '_test_name')
    ]
    
    print(f"Running {len(test_functions)} tests...\n")
    
    for test_func in sorted(test_functions, key=lambda f: f._test_name):
        test_func()
    
    success = results.summary()
    sys.exit(0 if success else 1)