# Event Emitter Utilities

A comprehensive event emitter/pub-sub implementation for Python with zero external dependencies.

## Features

- **Event Registration & Emission** - Register listeners and emit events with data
- **Wildcard Patterns** - Use `*` for single-level and `**` for multi-level matching
- **Once-Only Listeners** - Auto-remove after first invocation
- **Priority Ordering** - Control listener execution order
- **Async Support** - Native async/await listener support
- **Thread-Safe** - Safe for concurrent access
- **Event History** - Record and replay historical events
- **Namespacing** - Organize events with dot notation (e.g., `user.created`)
- **Global Event Bus** - Singleton pattern for app-wide events
- **Decorators** - `@on_event` and `@emits_event` decorators

## Installation

No installation needed - just copy the `event_emitter_utils` folder to your project.

## Quick Start

```python
from event_emitter_utils.mod import EventEmitter

# Create an emitter
emitter = EventEmitter()

# Register a listener
emitter.on("user.created", lambda data: print(f"New user: {data}"))

# Emit an event
emitter.emit("user.created", {"id": 1, "name": "Alice"})
```

## API Reference

### EventEmitter

#### Constructor

```python
emitter = EventEmitter(max_history=100, enable_history=True)
```

- `max_history`: Maximum events to keep in history (default: 100)
- `enable_history`: Whether to record event history (default: True)

#### Methods

##### on(event_name, callback, priority=0, once=False)

Register a listener for an event.

```python
# Basic listener
emitter.on("user.created", handle_user)

# With priority (higher = called first)
emitter.on("user.created", handle_urgent, priority=10)

# Once-only (auto-removes after first call)
emitter.on("config.loaded", handle_startup, once=True)
```

##### once(event_name, callback, priority=0)

Register a one-time listener (shorthand for `on(..., once=True)`).

```python
emitter.once("app.startup", handle_startup)
```

##### off(event_name, callback=None)

Remove listener(s).

```python
# Remove all listeners for an event
emitter.off("user.created")

# Remove specific listener
emitter.off("user.created", specific_handler)

# Remove ALL listeners
emitter.off("*")
```

##### emit(event_name, data=None, async_mode=False)

Emit an event to all matching listeners.

```python
# Simple emit
emitter.emit("user.created", {"id": 1})

# Async emit (for async listeners)
emitter.emit("data.processed", result, async_mode=True)
```

##### emit_async(event_name, data=None)

Emit an event with async support enabled.

```python
emitter.emit_async("async.event", data)
```

##### has_listener(event_name)

Check if an event has any listeners.

```python
if emitter.has_listener("error"):
    emitter.emit("error", error_msg)
```

##### get_listener_count(event_name)

Get the number of listeners for an event.

```python
count = emitter.get_listener_count("user.created")
```

##### get_events()

Get all registered event names.

```python
events = emitter.get_events()
```

##### get_stats()

Get emitter statistics.

```python
stats = emitter.get_stats()
print(f"Events: {stats['event_count']}")
print(f"Listeners: {stats['total_listeners']}")
```

##### pause(event_name) / resume(event_name)

Pause/resume event emission.

```python
emitter.pause("noisy.event")  # Temporarily disable
# ... do work ...
emitter.resume("noisy.event")  # Re-enable
```

##### get_history(event_name=None, limit=10)

Get event history.

```python
# Get last 10 events
history = emitter.get_history(limit=10)

# Get history for specific event
log_history = emitter.get_history("log.info", limit=50)
```

##### replay(event_name, callback, from_index=0)

Replay historical events.

```python
def replay_handler(data):
    print(f"Replayed: {data}")

emitter.replay("user.created", replay_handler)
```

##### clear_history(event_name=None)

Clear event history.

```python
# Clear all history
emitter.clear_history()

# Clear specific event history
emitter.clear_history("debug.log")
```

##### clear()

Remove all listeners and clear history.

```python
emitter.clear()
```

### Wildcard Patterns

```python
# Single level wildcard (*)
emitter.on("user.*", handler)  # Matches: user.created, user.deleted
                                # NOT: user.profile.updated

# Multi-level wildcard (**)
emitter.on("data.**", handler)  # Matches: data.sync, data.users.sync,
                                 #          data.config.db.changed

# Exact match
emitter.on("exact.event", handler)  # Only matches exact name
```

### Priority Ordering

Listeners are called in priority order (highest first).

```python
emitter.on("event", lambda: print("Third"), priority=0)
emitter.on("event", lambda: print("First"), priority=10)
emitter.on("event", lambda: print("Second"), priority=5)

# Output: First, Second, Third
```

### Async Listeners

```python
import asyncio

emitter = EventEmitter()

async def async_handler(data):
    await asyncio.sleep(0.1)
    print(f"Processed: {data}")

emitter.on("async.event", async_handler)

# Emit with async support
emitter.emit_async("async.event", {"key": "value"})
```

### Global Event Bus

Singleton pattern for application-wide events.

```python
from event_emitter_utils.mod import EventBus

# Get singleton instance
bus = EventBus.get_instance()

# Use like a normal emitter
bus.on("app.error", handle_error)
bus.emit("app.error", {"message": "Something went wrong"})

# All instances share state
bus2 = EventBus.get_instance()
assert bus is bus2  # True
```

### Channels

Create named event channels for organization.

```python
from event_emitter_utils.mod import create_channel

user_channel = create_channel("user")

# Events are auto-prefixed
user_channel.on("created", handler)  # Listens to "user.created"
user_channel.emit("created", data)   # Emits "user.created"
```

### Decorators

```python
from event_emitter_utils.mod import EventEmitter, on_event, emits_event

emitter = EventEmitter()

# Register handler with decorator
@on_event(emitter, "user.created")
def handle_user_created(data):
    print(f"User created: {data}")

# Mark function as emitting an event
@emits_event("user.created")
def create_user(name, _emitter=None):
    user = {"name": name}
    return user

# Use with emitter context
user = create_user("Alice", _emitter=emitter)
```

## Examples

### Example 1: Simple Pub-Sub

```python
from event_emitter_utils.mod import EventEmitter

emitter = EventEmitter()

# Subscribe
emitter.on("message", lambda msg: print(f"Received: {msg}"))

# Publish
emitter.emit("message", "Hello, World!")
```

### Example 2: Event Namespacing

```python
emitter = EventEmitter()

# Organize events with namespaces
emitter.on("user.created", on_user_created)
emitter.on("user.deleted", on_user_deleted)
emitter.on("user.updated", on_user_updated)

# Catch all user events
emitter.on("user.*", on_any_user_event)
```

### Example 3: Event History & Replay

```python
emitter = EventEmitter(max_history=100)

# Record events
for i in range(50):
    emitter.emit("log.info", f"Message {i}")

# Get history
history = emitter.get_history("log.info", limit=10)
for record in history:
    print(f"[{record.timestamp}] {record.data}")

# Replay to new listener
def catch_up(data):
    print(f"Catch up: {data}")

emitter.replay("log.info", catch_up)
```

### Example 4: Thread-Safe Event Handling

```python
import threading
from event_emitter_utils.mod import EventEmitter

emitter = EventEmitter()

def worker(worker_id):
    emitter.emit("worker.done", {"id": worker_id})

# Start multiple threads
threads = []
for i in range(10):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads
for t in threads:
    t.join()
```

### Example 5: Application Event Bus

```python
from event_emitter_utils.mod import EventBus

# In module A
bus = EventBus.get_instance()
bus.on("app.shutdown", cleanup_resources)

# In module B (anywhere in app)
bus.emit("app.shutdown")

# All modules receive the event
```

## Testing

Run the test suite:

```bash
cd event_emitter_utils
python event_emitter_utils_test.py
```

## License

MIT License - See main AllToolkit LICENSE file.

## Author

AllToolkit Contributors
