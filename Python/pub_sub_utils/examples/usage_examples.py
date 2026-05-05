"""
AllToolkit - Python Publish/Subscribe Usage Examples

Practical examples demonstrating pub/sub pattern usage.
"""

import sys
import os
import time

# Add the parent directory (pub_sub_utils) to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    PubSub, MatchMode, DeliveryMode, Topic, EventEmitter,
    subscribe, publish, get_global_broker,
)


def example_basic_pubsub():
    """Basic publish/subscribe example."""
    print("\n" + "="*50)
    print("Example 1: Basic Pub/Sub")
    print("="*50)
    
    broker = PubSub()
    
    # Subscribe to a topic
    def handle_user_created(payload):
        print(f"  User created: {payload}")
    
    sub_id = broker.subscribe('user.created', handle_user_created)
    
    # Publish messages
    broker.publish('user.created', {'id': 1, 'name': 'Alice'})
    broker.publish('user.created', {'id': 2, 'name': 'Bob'})
    
    # Unsubscribe
    broker.unsubscribe(sub_id)
    print("  Unsubscribed - no more messages will be received")
    
    # Statistics
    stats = broker.get_stats()
    print(f"  Stats: {stats['messages_published']} published, {stats['messages_delivered']} delivered")


def example_wildcard_subscription():
    """Wildcard subscription patterns."""
    print("\n" + "="*50)
    print("Example 2: Wildcard Subscriptions")
    print("="*50)
    
    broker = PubSub()
    
    # Single-level wildcard (*)
    broker.subscribe(
        'user.*',
        lambda payload: print(f"  [user.*] Received: {payload}"),
        match_mode=MatchMode.WILDCARD
    )
    
    # Multi-level wildcard (>)
    broker.subscribe(
        'order.>',
        lambda payload: print(f"  [order.>] Received: {payload}"),
        match_mode=MatchMode.WILDCARD
    )
    
    # Publish various topics
    broker.publish('user.created', 'User created')
    broker.publish('user.updated', 'User updated')
    broker.publish('order.created', 'Order created')
    broker.publish('order.created.shipped', 'Order shipped')
    
    print("  user.created  -> matches user.*")
    print("  user.updated  -> matches user.*")
    print("  order.created -> matches order.>")
    print("  order.created.shipped -> matches order.>")


def example_prefix_matching():
    """Prefix matching example."""
    print("\n" + "="*50)
    print("Example 3: Prefix Matching")
    print("="*50)
    
    broker = PubSub()
    
    # Subscribe to all topics starting with 'log.'
    broker.subscribe(
        'log.',
        lambda payload: print(f"  Log: {payload}"),
        match_mode=MatchMode.PREFIX
    )
    
    broker.publish('log.error', 'Critical error')
    broker.publish('log.warning', 'Warning message')
    broker.publish('log.info', 'Info message')
    broker.publish('user.created', 'Not a log')


def example_regex_matching():
    """Regular expression matching."""
    print("\n" + "="*50)
    print("Example 4: Regex Matching")
    print("="*50)
    
    broker = PubSub()
    
    # Subscribe to topics matching pattern
    broker.subscribe(
        r'user\.\d+\.created',  # user.{number}.created
        lambda payload: print(f"  Numeric user ID: {payload}"),
        match_mode=MatchMode.REGEX
    )
    
    broker.publish('user.123.created', 'User 123 created')
    broker.publish('user.456.created', 'User 456 created')
    broker.publish('user.admin.created', 'Admin user (not matched)')


def example_message_filtering():
    """Message filtering with filter function."""
    print("\n" + "="*50)
    print("Example 5: Message Filtering")
    print("="*50)
    
    broker = PubSub()
    
    # Only process high-priority messages
    def is_high_priority(msg):
        return msg.payload.get('priority', 0) >= 10
    
    broker.subscribe(
        'alert',
        lambda payload: print(f"  HIGH ALERT: {payload['message']}"),
        filter_func=is_high_priority
    )
    
    broker.publish('alert', {'message': 'Low alert', 'priority': 5})
    broker.publish('alert', {'message': 'High alert', 'priority': 10})
    broker.publish('alert', {'message': 'Critical alert', 'priority': 20})
    
    print("  Only priority >= 10 messages are processed")


def example_priority_ordering():
    """Priority-based message handling."""
    print("\n" + "="*50)
    print("Example 6: Priority Ordering")
    print("="*50)
    
    broker = PubSub()
    order = []
    
    broker.subscribe('event', lambda p: order.append('low'), priority=0)
    broker.subscribe('event', lambda p: order.append('high'), priority=10)
    broker.subscribe('event', lambda p: order.append('medium'), priority=5)
    
    broker.publish('event', 'test')
    
    print(f"  Handler call order: {order}")
    print("  Higher priority handlers are called first")


def example_topic_wrapper():
    """Using Topic wrapper for hierarchical topics."""
    print("\n" + "="*50)
    print("Example 7: Topic Wrapper")
    print("="*50)
    
    broker = PubSub()
    
    # Create topic with prefix
    user_topic = Topic('user', broker)
    order_topic = Topic('order', broker)
    
    # Subscribe using topic wrapper
    user_topic.subscribe('created', lambda p: print(f"  User created: {p}"))
    
    # Child topic
    admin_topic = user_topic.child('admin')
    admin_topic.subscribe('created', lambda p: print(f"  Admin created: {p}"))
    
    # Publish using topic wrapper
    user_topic.publish('created', {'id': 1})
    admin_topic.publish('created', {'id': 100, 'role': 'admin'})
    order_topic.publish('created', {'id': 'ORD-001'})
    
    print("  Topic wrapper provides convenient hierarchical topic management")


def example_event_emitter():
    """EventEmitter pattern example."""
    print("\n" + "="*50)
    print("Example 8: EventEmitter")
    print("="*50)
    
    emitter = EventEmitter()
    
    # Register listeners
    emitter.on('data', lambda d: print(f"  Data received: {d}"))
    
    # One-time listener
    emitter.once('init', lambda: print("  Initialized!"))
    
    # Decorator syntax
    @emitter.on('status')
    def handle_status(status):
        print(f"  Status changed: {status}")
    
    # Emit events
    emitter.emit('init')
    emitter.emit('init')  # Second call won't trigger (once)
    emitter.emit('data', {'value': 42})
    emitter.emit('status', 'running')


def example_decorator_subscription():
    """Using @subscribe decorator."""
    print("\n" + "="*50)
    print("Example 9: Decorator Subscription")
    print("="*50)
    
    broker = get_global_broker()
    
    @subscribe('app.event')
    def handle_app_event(payload):
        print(f"  App event: {payload}")
    
    @subscribe('app.*', match_mode=MatchMode.WILDCARD)
    def handle_all_app_events(payload):
        print(f"  All app events: {payload}")
    
    publish('app.event', 'Main event')
    publish('app.event.secondary', 'Secondary event')
    
    # Clean up
    broker.clear_all()


def example_error_handling():
    """Error handling in handlers."""
    print("\n" + "="*50)
    print("Example 10: Error Handling")
    print("="*50)
    
    errors = []
    
    def error_handler(exc, msg, handler):
        errors.append(f"Error in handler: {exc}")
    
    broker = PubSub(error_handler=error_handler)
    
    def bad_handler(payload):
        raise ValueError("Handler error!")
    
    broker.subscribe('test', bad_handler)
    broker.publish('test', 'data')
    
    print(f"  Captured errors: {errors}")


def example_stats_tracking():
    """Statistics tracking example."""
    print("\n" + "="*50)
    print("Example 11: Statistics Tracking")
    print("="*50)
    
    broker = PubSub()
    
    broker.subscribe('metric', lambda p: None)
    broker.subscribe('metric.*', lambda p: None, match_mode=MatchMode.WILDCARD)
    
    # Publish messages
    for i in range(5):
        broker.publish('metric', f'value-{i}')
    
    broker.publish('metric.cpu', 'cpu-data')
    broker.publish('metric.memory', 'mem-data')
    broker.publish('no.subscribers', 'ignored')
    
    stats = broker.get_stats()
    print(f"  Messages published: {stats['messages_published']}")
    print(f"  Messages delivered: {stats['messages_delivered']}")
    print(f"  Delivery rate: {stats['delivery_rate']:.2%}")
    print(f"  Active subscriptions: {stats['active_subscriptions']}")


def example_pause_resume():
    """Pause and resume subscriptions."""
    print("\n" + "="*50)
    print("Example 12: Pause & Resume")
    print("="*50)
    
    broker = PubSub()
    received = []
    
    sub_id = broker.subscribe('test', lambda p: received.append(p))
    
    broker.publish('test', 'before-pause')
    print(f"  Received: {received}")
    
    broker.pause_subscription(sub_id)
    broker.publish('test', 'during-pause')
    print(f"  After pause (still {received})")
    
    broker.resume_subscription(sub_id)
    broker.publish('test', 'after-resume')
    print(f"  After resume: {received}")


def example_multiple_brokers():
    """Using multiple broker instances."""
    print("\n" + "="*50)
    print("Example 13: Multiple Brokers")
    print("="*50)
    
    # System broker
    system_broker = PubSub()
    system_broker.subscribe('system.health', lambda p: print(f"  System: {p}"))
    
    # User broker
    user_broker = PubSub()
    user_broker.subscribe('user.action', lambda p: print(f"  User: {p}"))
    
    # Publish to each
    system_broker.publish('system.health', 'CPU 80%')
    user_broker.publish('user.action', 'Login')
    
    print("  Isolated brokers for different domains")


def example_real_world_simulation():
    """Real-world application simulation."""
    print("\n" + "="*50)
    print("Example 14: Real-World Application Simulation")
    print("="*50)
    
    broker = PubSub()
    
    # Simulate a microservice architecture
    orders = []
    notifications = []
    logs = []
    
    # Order service
    broker.subscribe('order.created', lambda p: orders.append(p))
    broker.subscribe('order.cancelled', lambda p: orders.remove(p) if p in orders else None)
    
    # Notification service
    broker.subscribe('order.>', lambda p: notifications.append(f"Notify about: {p}"), 
                    match_mode=MatchMode.WILDCARD)
    
    # Logging service
    broker.subscribe('log.', lambda p: logs.append(p), match_mode=MatchMode.PREFIX)
    
    # Simulate events
    broker.publish('order.created', {'id': 'ORD-001', 'user': 'Alice'})
    broker.publish('log.info', 'Order ORD-001 created')
    broker.publish('order.created', {'id': 'ORD-002', 'user': 'Bob'})
    broker.publish('log.info', 'Order ORD-002 created')
    broker.publish('order.cancelled', {'id': 'ORD-001', 'user': 'Alice'})
    broker.publish('log.warning', 'Order ORD-001 cancelled')
    
    print(f"  Orders: {orders}")
    print(f"  Notifications sent: {len(notifications)}")
    print(f"  Logs: {logs}")


# Run all examples
if __name__ == '__main__':
    print("\n" + "="*60)
    print("AllToolkit - Pub/Sub Utilities Usage Examples")
    print("="*60)
    
    example_basic_pubsub()
    example_wildcard_subscription()
    example_prefix_matching()
    example_regex_matching()
    example_message_filtering()
    example_priority_ordering()
    example_topic_wrapper()
    example_event_emitter()
    example_decorator_subscription()
    example_error_handling()
    example_stats_tracking()
    example_pause_resume()
    example_multiple_brokers()
    example_real_world_simulation()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60 + "\n")