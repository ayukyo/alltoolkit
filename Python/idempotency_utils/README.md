# Idempotency Utilities

**Zero-dependency idempotency key management for distributed systems.**

Prevent duplicate operations, cache results, and handle request deduplication with ease.

## Features

- ✅ **Idempotency Key Store** - In-memory storage with TTL support
- ✅ **Key Generation** - Multiple methods for generating unique keys
- ✅ **Result Caching** - Automatic caching of operation results
- ✅ **Request Deduplication** - Short-window duplicate detection
- ✅ **Thread-Safe** - Safe for concurrent use
- ✅ **Decorator Support** - Easy `@idempotent` decorator
- ✅ **Zero Dependencies** - Uses only Python standard library

## Installation

Copy the `idempotency_utils` folder to your project.

```python
from idempotency_utils.mod import IdempotencyStore, idempotent
```

## Quick Start

### Basic Usage

```python
from idempotency_utils.mod import IdempotencyStore

store = IdempotencyStore(default_ttl=3600)  # 1 hour TTL

# Check for cached result
key = "payment:user:123:amount:100"
cached = store.get_result(key)

if cached:
    return cached  # Return cached result

# Mark as in progress
store.set_pending(key)

# Execute operation
result = {"transaction_id": "tx-001", "status": "success"}

# Cache result
store.set_completed(key, result)
```

### Using the Decorator

```python
from idempotency_utils.mod import idempotent

@idempotent()
def process_payment(amount: float, user_id: str):
    # This will only execute once for the same arguments
    return {"transaction_id": "tx-001", "amount": amount}

# First call - executes
result1 = process_payment(100.0, "user:123")

# Duplicate call - returns cached result
result2 = process_payment(100.0, "user:123")  # Same arguments
```

### Custom Key Function

```python
from idempotency_utils.mod import idempotent, IdempotencyStore

store = IdempotencyStore()

@idempotent(
    key_func=lambda order_id, **kwargs: f"order:{order_id}",
    store=store,
)
def create_order(order_id: str, items: list):
    return {"order_id": order_id, "status": "created"}
```

### IdempotencyManager

```python
from idempotency_utils.mod import IdempotencyManager

manager = IdempotencyManager(default_ttl=3600)

# Execute with idempotency
result = manager.execute("operation-123", lambda: {
    "processed": True,
    "data": "value"
})

# Check for cached result
if manager.has_result("operation-123"):
    return manager.get_result("operation-123")
```

### Request Deduplicator

```python
from idempotency_utils.mod import RequestDeduplicator

deduper = RequestDeduplicator(window_seconds=5.0)

# Atomic check and mark
if deduper.check_and_mark(request_id):
    return {"error": "duplicate_request"}

# Process request
result = process_request()
```

## API Reference

### IdempotencyStore

Thread-safe in-memory store for idempotency keys.

```python
store = IdempotencyStore(
    default_ttl=3600,      # Default TTL in seconds (None = no expiry)
    max_size=10000,        # Maximum records (None = unlimited)
    cleanup_interval=60.0, # Cleanup interval in seconds
)

# Operations
store.set_pending(key, metadata=None, ttl=None)      # Mark as in progress
store.set_completed(key, result, ttl=None)           # Mark completed with result
store.set_error(key, error_message, ttl=None)        # Record error (allows retry)
store.get(key)                                       # Get record
store.get_result(key)                                # Get cached result
store.delete(key)                                    # Delete key
store.exists(key)                                    # Check if exists
store.is_in_progress(key)                            # Check if in progress
store.is_completed(key)                              # Check if completed
store.clear()                                        # Clear all records
store.cleanup_expired()                              # Remove expired records
store.stats()                                        # Get statistics
```

### IdempotencyKeyGenerator

Generate idempotency keys in various ways.

```python
from idempotency_utils.mod import IdempotencyKeyGenerator

gen = IdempotencyKeyGenerator

# Random UUID key
key = gen.random()                                   # "550e8400-e29b-..."

# From hash of arguments (SHA-256)
key = gen.from_hash("arg1", "arg2", kwarg="value")   # "a1b2c3..."

# From HTTP request
key = gen.from_request(
    method="POST",
    url="/api/payments",
    body={"amount": 100},
)

# From function call
key = gen.from_function_call("func_name", args, kwargs)

# Prefix and suffix
key = gen.prefix("payment", "123")                   # "payment:123"
key = gen.with_timestamp("base-key")                 # "base-key:1700000000"
```

### IdempotencyManager

High-level manager for idempotent operations.

```python
manager = IdempotencyManager(default_ttl=3600, max_size=10000)

manager.execute(key, func, ttl=None)                 # Execute with idempotency
manager.has_result(key)                              # Check if result exists
manager.get_result(key)                              # Get cached result
manager.is_in_progress(key)                          # Check if in progress
manager.cancel(key)                                  # Cancel in-progress operation
manager.clear()                                      # Clear all records
manager.cleanup()                                    # Remove expired records
manager.stats()                                      # Get statistics
```

### RequestDeduplicator

Short-window request deduplication.

```python
deduper = RequestDeduplicator(
    window_seconds=5.0,   # Time window for duplicate detection
    max_requests=10000,   # Maximum tracked requests
)

deduper.is_duplicate(request_id)                     # Check if duplicate
deduper.mark(request_id)                             # Mark as seen
deduper.check_and_mark(request_id)                   # Atomic check and mark
deduper.clear()                                      # Clear all
deduper.stats()                                      # Get statistics
```

### @idempotent Decorator

Make functions idempotent.

```python
@idempotent(
    key_func=None,               # Custom key function (default: hash from args)
    store=None,                  # IdempotencyStore (default: global store)
    ttl=None,                    # TTL in seconds
    raise_on_duplicate=False,    # Raise error on duplicate
    return_cached=True,          # Return cached result on duplicate
)
def my_function(arg1, arg2):
    # Function body
    return result
```

## Use Cases

### API Endpoints

```python
from idempotency_utils.mod import IdempotencyKeyGenerator, IdempotencyManager

manager = IdempotencyManager(default_ttl=86400)  # 24 hours

def handle_payment_request(request):
    # Generate key from request
    key = IdempotencyKeyGenerator.from_request(
        method=request.method,
        url=request.path,
        body=request.body,
    )
    
    # Execute with idempotency
    result = manager.execute(key, lambda: process_payment(request))
    return result
```

### Preventing Double Charges

```python
from idempotency_utils.mod import idempotent

@idempotent(key_func=lambda user_id, amount, **kw: f"charge:{user_id}:{amount}")
def charge_user(user_id: str, amount: float):
    # Will only execute once per unique (user_id, amount) combination
    return charge_card(user_id, amount)
```

### Email Sending

```python
from idempotency_utils.mod import IdempotencyManager

manager = IdempotencyManager(default_ttl=86400)

def send_email(to: str, subject: str, body: str):
    key = f"email:{to}:{subject}:{hash(body)}"
    
    if manager.has_result(key):
        return manager.get_result(key)  # Already sent
    
    result = manager.execute(key, lambda: {
        "sent": True,
        "message_id": "...",
    })
    return result
```

### Database Operations

```python
from idempotency_utils.mod import IdempotencyStore

store = IdempotencyStore()

def insert_if_not_exists(table, data):
    key = f"insert:{table}:{data['id']}"
    
    if store.is_completed(key):
        return store.get_result(key)
    
    store.set_pending(key)
    # Check database first
    if exists_in_db(table, data['id']):
        result = {"status": "exists", "id": data['id']}
    else:
        insert_to_db(table, data)
        result = {"status": "inserted", "id": data['id']}
    
    store.set_completed(key, result)
    return result
```

## Testing

Run the test suite:

```bash
python idempotency_utils/idempotency_utils_test.py
```

## Examples

Run usage examples:

```bash
python idempotency_utils/examples/usage_examples.py
```

## License

MIT License - See LICENSE file for details.

## Author

AllToolkit - https://github.com/ayukyo/alltoolkit