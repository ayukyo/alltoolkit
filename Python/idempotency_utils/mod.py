"""
AllToolkit - Python Idempotency Utilities

A zero-dependency, production-ready idempotency key management module.
Supports in-memory storage with TTL, result caching, and request deduplication.

Author: AllToolkit
License: MIT
"""

import hashlib
import json
import threading
import time
from typing import Any, Callable, Dict, Generic, Optional, Tuple, TypeVar, Union
from dataclasses import dataclass, field
from functools import wraps
from enum import Enum
import uuid

T = TypeVar('T')
R = TypeVar('R')


class IdempotencyStatus(Enum):
    """Status of an idempotency key."""
    PENDING = "pending"
    COMPLETED = "completed"
    EXPIRED = "expired"
    IN_PROGRESS = "in_progress"


@dataclass
class IdempotencyRecord(Generic[T]):
    """Record stored for an idempotency key."""
    key: str
    status: IdempotencyStatus
    result: Optional[T] = None
    error: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    expires_at: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if the record has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def is_complete(self) -> bool:
        """Check if the operation is complete."""
        return self.status == IdempotencyStatus.COMPLETED
    
    def age(self) -> float:
        """Get the age of the record in seconds."""
        return time.time() - self.created_at
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert record to dictionary."""
        return {
            'key': self.key,
            'status': self.status.value,
            'result': self.result,
            'error': self.error,
            'created_at': self.created_at,
            'completed_at': self.completed_at,
            'expires_at': self.expires_at,
            'metadata': self.metadata,
        }


class IdempotencyStore(Generic[T]):
    """
    Thread-safe in-memory store for idempotency keys with TTL support.
    
    Example:
        store = IdempotencyStore(default_ttl=3600)  # 1 hour TTL
        
        # Check if key exists and is complete
        record = store.get("operation-123")
        if record and record.is_complete():
            return record.result
        
        # Mark as in progress
        store.set_pending("operation-123")
        
        # Complete with result
        store.set_completed("operation-123", result={"data": "value"})
    """
    
    def __init__(
        self,
        default_ttl: Optional[float] = None,
        max_size: Optional[int] = None,
        cleanup_interval: float = 60.0,
    ):
        """
        Initialize the idempotency store.
        
        Args:
            default_ttl: Default time-to-live in seconds (None = no expiry)
            max_size: Maximum number of records (None = unlimited)
            cleanup_interval: Interval for automatic cleanup of expired records
        """
        self._store: Dict[str, IdempotencyRecord[T]] = {}
        self._lock = threading.RLock()
        self._default_ttl = default_ttl
        self._max_size = max_size
        self._cleanup_interval = cleanup_interval
        self._last_cleanup = time.time()
    
    def get(self, key: str) -> Optional[IdempotencyRecord[T]]:
        """
        Get record for a key.
        
        Args:
            key: Idempotency key
        
        Returns:
            IdempotencyRecord if found and not expired, None otherwise
        """
        with self._lock:
            self._maybe_cleanup()
            record = self._store.get(key)
            if record is None:
                return None
            if record.is_expired():
                del self._store[key]
                return None
            return record
    
    def set_pending(
        self,
        key: str,
        metadata: Optional[Dict[str, Any]] = None,
        ttl: Optional[float] = None,
    ) -> IdempotencyRecord[T]:
        """
        Mark a key as pending (operation in progress).
        
        Args:
            key: Idempotency key
            metadata: Optional metadata to store
            ttl: Time-to-live in seconds (uses default if not specified)
        
        Returns:
            The created record
        """
        with self._lock:
            self._maybe_cleanup()
            
            # Handle TTL: None means no expiry, 0/negative means immediate expiry
            effective_ttl = ttl if ttl is not None else self._default_ttl
            expires_at = time.time() + effective_ttl if effective_ttl is not None else None
            
            record = IdempotencyRecord[T](
                key=key,
                status=IdempotencyStatus.IN_PROGRESS,
                metadata=metadata or {},
                expires_at=expires_at,
            )
            self._store[key] = record
            return record
    
    def set_completed(
        self,
        key: str,
        result: T,
        ttl: Optional[float] = None,
    ) -> IdempotencyRecord[T]:
        """
        Mark a key as completed with a result.
        
        Args:
            key: Idempotency key
            result: The result to cache
            ttl: Time-to-live in seconds (uses default if not specified)
        
        Returns:
            The updated record
        
        Raises:
            KeyError: If key doesn't exist
        """
        with self._lock:
            if key not in self._store:
                # Create new record if doesn't exist
                effective_ttl = ttl if ttl is not None else self._default_ttl
                expires_at = time.time() + effective_ttl if effective_ttl is not None else None
                record = IdempotencyRecord[T](
                    key=key,
                    status=IdempotencyStatus.COMPLETED,
                    result=result,
                    completed_at=time.time(),
                    expires_at=expires_at,
                )
                self._store[key] = record
                return record
            
            record = self._store[key]
            record.status = IdempotencyStatus.COMPLETED
            record.result = result
            record.completed_at = time.time()
            
            # Update TTL if specified
            if ttl is not None:
                record.expires_at = time.time() + ttl if ttl is not None else None
            
            return record
    
    def set_error(
        self,
        key: str,
        error: str,
        ttl: Optional[float] = None,
    ) -> IdempotencyRecord[T]:
        """
        Mark a key as having an error (allows retry).
        
        Args:
            key: Idempotency key
            error: Error message
            ttl: Time-to-live in seconds
        
        Returns:
            The updated record
        """
        with self._lock:
            if key not in self._store:
                ttl = ttl if ttl is not None else self._default_ttl
                expires_at = time.time() + ttl if ttl else None
                record = IdempotencyRecord[T](
                    key=key,
                    status=IdempotencyStatus.PENDING,
                    error=error,
                    expires_at=expires_at,
                )
                self._store[key] = record
                return record
            
            record = self._store[key]
            record.status = IdempotencyStatus.PENDING
            record.error = error
            record.completed_at = None
            
            if ttl is not None:
                record.expires_at = time.time() + ttl if ttl else None
            
            return record
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from the store.
        
        Args:
            key: Idempotency key
        
        Returns:
            True if key was deleted, False if it didn't exist
        """
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False
    
    def exists(self, key: str) -> bool:
        """Check if a key exists and is not expired."""
        return self.get(key) is not None
    
    def is_in_progress(self, key: str) -> bool:
        """Check if an operation is in progress."""
        record = self.get(key)
        return record is not None and record.status == IdempotencyStatus.IN_PROGRESS
    
    def is_completed(self, key: str) -> bool:
        """Check if an operation is completed."""
        record = self.get(key)
        return record is not None and record.status == IdempotencyStatus.COMPLETED
    
    def get_result(self, key: str) -> Optional[T]:
        """Get the cached result for a completed key."""
        record = self.get(key)
        if record and record.is_complete():
            return record.result
        return None
    
    def clear(self) -> int:
        """
        Clear all records.
        
        Returns:
            Number of records cleared
        """
        with self._lock:
            count = len(self._store)
            self._store.clear()
            return count
    
    def cleanup_expired(self) -> int:
        """
        Remove all expired records.
        
        Returns:
            Number of records removed
        """
        with self._lock:
            now = time.time()
            expired_keys = [
                key for key, record in self._store.items()
                if record.is_expired()
            ]
            for key in expired_keys:
                del self._store[key]
            return len(expired_keys)
    
    def _maybe_cleanup(self) -> None:
        """Perform cleanup if interval has passed."""
        now = time.time()
        if now - self._last_cleanup > self._cleanup_interval:
            self._last_cleanup = now
            # Clean expired records
            self._cleanup_expired_unlocked()
            # Enforce max size
            self._enforce_max_size_unlocked()
    
    def _cleanup_expired_unlocked(self) -> None:
        """Remove expired records (no lock)."""
        now = time.time()
        expired_keys = [
            key for key, record in self._store.items()
            if record.is_expired()
        ]
        for key in expired_keys:
            del self._store[key]
    
    def _enforce_max_size_unlocked(self) -> None:
        """Enforce max size by removing oldest records."""
        if self._max_size is None or len(self._store) <= self._max_size:
            return
        
        # Sort by created_at and remove oldest
        sorted_items = sorted(
            self._store.items(),
            key=lambda x: x[1].created_at
        )
        to_remove = len(self._store) - self._max_size
        for key, _ in sorted_items[:to_remove]:
            del self._store[key]
    
    def stats(self) -> Dict[str, Any]:
        """Get store statistics."""
        with self._lock:
            total = len(self._store)
            pending = sum(1 for r in self._store.values() if r.status == IdempotencyStatus.PENDING)
            in_progress = sum(1 for r in self._store.values() if r.status == IdempotencyStatus.IN_PROGRESS)
            completed = sum(1 for r in self._store.values() if r.status == IdempotencyStatus.COMPLETED)
            expired = sum(1 for r in self._store.values() if r.is_expired())
            
            return {
                'total': total,
                'pending': pending,
                'in_progress': in_progress,
                'completed': completed,
                'expired': expired,
                'max_size': self._max_size,
            }


class IdempotencyKeyGenerator:
    """Utilities for generating idempotency keys."""
    
    @staticmethod
    def random() -> str:
        """Generate a random idempotency key."""
        return str(uuid.uuid4())
    
    @staticmethod
    def from_uuid(uuid_value: Union[str, uuid.UUID]) -> str:
        """Create key from UUID."""
        return str(uuid_value)
    
    @staticmethod
    def from_hash(*args: Any, **kwargs: Any) -> str:
        """
        Create key from hashing input values.
        
        Args:
            *args: Values to hash
            **kwargs: Additional key-value pairs to include in hash
        
        Returns:
            SHA-256 hash of the inputs
        """
        # Convert to JSON-serializable format
        data = {
            'args': args,
            'kwargs': kwargs,
        }
        json_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    @staticmethod
    def from_request(
        method: str,
        url: str,
        body: Any = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Create key from HTTP request parameters.
        
        Args:
            method: HTTP method
            url: Request URL
            body: Request body
            headers: Relevant headers to include
        
        Returns:
            SHA-256 hash of the request
        """
        data = {
            'method': method.upper(),
            'url': url,
            'body': body,
        }
        if headers:
            # Only include specific headers
            relevant_headers = {k.lower(): v for k, v in headers.items()
                               if k.lower() in ('content-type', 'authorization')}
            if relevant_headers:
                data['headers'] = relevant_headers
        
        json_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    @staticmethod
    def from_function_call(
        func_name: str,
        args: tuple,
        kwargs: Dict[str, Any],
    ) -> str:
        """
        Create key from function call parameters.
        
        Args:
            func_name: Function name
            args: Positional arguments
            kwargs: Keyword arguments
        
        Returns:
            SHA-256 hash of the call
        """
        return IdempotencyKeyGenerator.from_hash(func_name, *args, **kwargs)
    
    @staticmethod
    def prefix(prefix: str, key: str) -> str:
        """Add a prefix to a key."""
        return f"{prefix}:{key}"
    
    @staticmethod
    def with_timestamp(key: str, timestamp: Optional[float] = None) -> str:
        """Add timestamp to key."""
        ts = timestamp or time.time()
        return f"{key}:{int(ts)}"


class IdempotencyError(Exception):
    """Error related to idempotency operations."""
    pass


class DuplicateOperationError(IdempotencyError):
    """Raised when a duplicate operation is detected."""
    
    def __init__(self, key: str, record: Optional[IdempotencyRecord] = None):
        self.key = key
        self.record = record
        super().__init__(f"Duplicate operation detected for key: {key}")


class OperationInProgressError(IdempotencyError):
    """Raised when an operation is already in progress."""
    
    def __init__(self, key: str, record: Optional[IdempotencyRecord] = None):
        self.key = key
        self.record = record
        super().__init__(f"Operation already in progress for key: {key}")


def idempotent(
    key_func: Optional[Callable[..., str]] = None,
    store: Optional[IdempotencyStore] = None,
    ttl: Optional[float] = None,
    raise_on_duplicate: bool = False,
    return_cached: bool = True,
):
    """
    Decorator to make a function idempotent.
    
    Args:
        key_func: Function to generate idempotency key from args/kwargs
        store: IdempotencyStore instance (default: global store)
        ttl: Time-to-live in seconds
        raise_on_duplicate: Raise error if duplicate detected
        return_cached: Return cached result if available
    
    Returns:
        Decorated function
    
    Example:
        # Using auto-generated key from args
        @idempotent()
        def process_payment(amount: float, user_id: str):
            # This will only execute once for same args
            return {"transaction_id": "123"}
        
        # Using custom key function
        @idempotent(key_func=lambda order_id, **kwargs: f"order:{order_id}")
        def create_order(order_id: str, items: list):
            return {"order_id": order_id}
        
        # Using global store
        store = IdempotencyStore(default_ttl=3600)
        @idempotent(store=store)
        def send_email(to: str, subject: str):
            return {"sent": True}
    """
    _store = store or _global_store
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # Generate key
            if key_func:
                key = key_func(*args, **kwargs)
            else:
                key = IdempotencyKeyGenerator.from_function_call(
                    func.__name__, args, kwargs
                )
            
            # Check for cached result
            cached_result = _store.get_result(key)
            if cached_result is not None:
                if raise_on_duplicate:
                    raise DuplicateOperationError(key, _store.get(key))
                if return_cached:
                    return cached_result
            
            # Check if in progress
            if _store.is_in_progress(key):
                if raise_on_duplicate:
                    raise OperationInProgressError(key, _store.get(key))
                # Wait and return cached result
                # Simple polling implementation
                max_wait = 30  # seconds
                poll_interval = 0.1
                waited = 0.0
                while waited < max_wait:
                    time.sleep(poll_interval)
                    waited += poll_interval
                    cached_result = _store.get_result(key)
                    if cached_result is not None:
                        return cached_result
                    if not _store.is_in_progress(key):
                        # Operation failed, check for error
                        record = _store.get(key)
                        if record and record.error:
                            raise IdempotencyError(f"Previous operation failed: {record.error}")
                        break
                raise IdempotencyError("Timeout waiting for operation to complete")
            
            # Mark as in progress
            _store.set_pending(key, ttl=ttl)
            
            try:
                result = func(*args, **kwargs)
                _store.set_completed(key, result, ttl=ttl)
                return result
            except Exception as e:
                _store.set_error(key, str(e), ttl=ttl)
                raise
        
        return wrapper
    
    return decorator


class IdempotencyManager:
    """
    High-level manager for idempotent operations.
    
    Example:
        manager = IdempotencyManager(default_ttl=3600)
        
        # Execute with deduplication
        result = manager.execute(
            "payment:123",
            lambda: process_payment(100.0, "user:456"),
        )
        
        # Check if operation exists
        if manager.has_result("payment:123"):
            return manager.get_result("payment:123")
    """
    
    def __init__(
        self,
        default_ttl: Optional[float] = None,
        max_size: Optional[int] = None,
    ):
        """
        Initialize the manager.
        
        Args:
            default_ttl: Default TTL for records in seconds
            max_size: Maximum number of records to store
        """
        self._store = IdempotencyStore[T](
            default_ttl=default_ttl,
            max_size=max_size,
        )
    
    @property
    def store(self) -> IdempotencyStore[T]:
        """Get the underlying store."""
        return self._store
    
    def execute(
        self,
        key: str,
        func: Callable[[], T],
        ttl: Optional[float] = None,
    ) -> T:
        """
        Execute a function with idempotency.
        
        Args:
            key: Idempotency key
            func: Function to execute
            ttl: TTL for this operation
        
        Returns:
            The function result (cached or fresh)
        """
        # Check for cached result
        cached_result = self._store.get_result(key)
        if cached_result is not None:
            return cached_result
        
        # Check if in progress
        if self._store.is_in_progress(key):
            raise OperationInProgressError(key, self._store.get(key))
        
        # Execute
        self._store.set_pending(key, ttl=ttl)
        try:
            result = func()
            self._store.set_completed(key, result, ttl=ttl)
            return result
        except Exception as e:
            self._store.set_error(key, str(e), ttl=ttl)
            raise
    
    def has_result(self, key: str) -> bool:
        """Check if a result exists for the key."""
        return self._store.is_completed(key)
    
    def get_result(self, key: str) -> Optional[T]:
        """Get the cached result for a key."""
        return self._store.get_result(key)
    
    def is_in_progress(self, key: str) -> bool:
        """Check if an operation is in progress."""
        return self._store.is_in_progress(key)
    
    def cancel(self, key: str) -> bool:
        """Cancel an in-progress operation."""
        record = self._store.get(key)
        if record and record.status == IdempotencyStatus.IN_PROGRESS:
            return self._store.delete(key)
        return False
    
    def clear(self) -> int:
        """Clear all records."""
        return self._store.clear()
    
    def cleanup(self) -> int:
        """Remove expired records."""
        return self._store.cleanup_expired()
    
    def stats(self) -> Dict[str, Any]:
        """Get statistics."""
        return self._store.stats()


class RequestDeduplicator:
    """
    Simple request deduplicator for preventing duplicate requests.
    
    Example:
        deduper = RequestDeduplicator(window_seconds=5.0)
        
        if deduper.is_duplicate("request-123"):
            return {"error": "duplicate request"}
        
        deduper.mark("request-123")
        # Process request
    """
    
    def __init__(self, window_seconds: float = 5.0, max_requests: int = 10000):
        """
        Initialize the deduplicator.
        
        Args:
            window_seconds: Time window in seconds for duplicate detection
            max_requests: Maximum number of request IDs to track
        """
        self._requests: Dict[str, float] = {}
        self._window = window_seconds
        self._max_requests = max_requests
        self._lock = threading.Lock()
    
    def is_duplicate(self, request_id: str) -> bool:
        """
        Check if a request ID is a duplicate.
        
        Args:
            request_id: Request identifier
        
        Returns:
            True if duplicate within window, False otherwise
        """
        with self._lock:
            now = time.time()
            
            # Clean old entries
            self._cleanup_unlocked(now)
            
            if request_id in self._requests:
                return True
            
            return False
    
    def mark(self, request_id: str) -> None:
        """
        Mark a request ID as seen.
        
        Args:
            request_id: Request identifier
        """
        with self._lock:
            now = time.time()
            
            # Clean old entries
            self._cleanup_unlocked(now)
            
            # Enforce max size
            if len(self._requests) >= self._max_requests:
                # Remove oldest
                oldest_key = min(self._requests, key=self._requests.get)
                del self._requests[oldest_key]
            
            self._requests[request_id] = now
    
    def check_and_mark(self, request_id: str) -> bool:
        """
        Check and mark atomically.
        
        Args:
            request_id: Request identifier
        
        Returns:
            True if duplicate (already seen), False if new
        """
        with self._lock:
            now = time.time()
            
            # Clean old entries
            self._cleanup_unlocked(now)
            
            if request_id in self._requests:
                return True  # Is duplicate
            
            # Enforce max size
            if len(self._requests) >= self._max_requests:
                oldest_key = min(self._requests, key=self._requests.get)
                del self._requests[oldest_key]
            
            self._requests[request_id] = now
            return False  # Not duplicate, now marked
    
    def _cleanup_unlocked(self, now: float) -> None:
        """Clean up old entries (no lock)."""
        cutoff = now - self._window
        expired_keys = [k for k, v in self._requests.items() if v < cutoff]
        for k in expired_keys:
            del self._requests[k]
    
    def clear(self) -> int:
        """Clear all tracked requests."""
        with self._lock:
            count = len(self._requests)
            self._requests.clear()
            return count
    
    def stats(self) -> Dict[str, Any]:
        """Get statistics."""
        with self._lock:
            return {
                'tracked_requests': len(self._requests),
                'window_seconds': self._window,
                'max_requests': self._max_requests,
            }


# Global store instance
_global_store = IdempotencyStore[Any]()
_global_deduplicator = RequestDeduplicator()


def get_global_store() -> IdempotencyStore[Any]:
    """Get the global idempotency store."""
    return _global_store


def get_global_deduplicator() -> RequestDeduplicator:
    """Get the global request deduplicator."""
    return _global_deduplicator


def reset_global_store() -> None:
    """Reset the global idempotency store."""
    _global_store.clear()


def reset_global_deduplicator() -> None:
    """Reset the global request deduplicator."""
    _global_deduplicator.clear()