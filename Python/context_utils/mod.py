"""
AllToolkit - Python Context Utilities

A zero-dependency, production-ready context management utility module.
Provides thread-safe scoped context storage, request context management,
context propagation across call chains, and nested scope support.

Author: AllToolkit
License: MIT
"""

import threading
import uuid
import time
import copy
from typing import (
    Any, Dict, List, Optional, TypeVar, Generic, Callable,
    ContextManager, Iterator, Type, Union
)
from dataclasses import dataclass, field
from contextlib import contextmanager
from functools import wraps

T = TypeVar('T')


# =============================================================================
# Exceptions
# =============================================================================

class ContextError(Exception):
    """Base exception for context operations."""
    pass


class ContextNotFoundError(ContextError):
    """Raised when a context variable is not found."""
    pass


class ScopeNotFoundError(ContextError):
    """Raised when a scope is not found."""
    pass


class InvalidScopeError(ContextError):
    """Raised when scope operation is invalid."""
    pass


# =============================================================================
# Scoped Context
# =============================================================================

@dataclass
class Scope:
    """
    Represents a single scope in the context hierarchy.
    
    Each scope has its own dictionary of variables and can have
    a parent scope for lookups.
    """
    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    parent: Optional['Scope'] = None
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    readonly: bool = False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from this scope or parent scopes."""
        if key in self.data:
            return self.data[key]
        if self.parent:
            return self.parent.get(key, default)
        return default
    
    def get_local(self, key: str, default: Any = None) -> Any:
        """Get a value only from this scope (not parents)."""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in this scope."""
        if self.readonly:
            raise InvalidScopeError(f"Scope '{self.name}' is readonly")
        self.data[key] = value
    
    def delete(self, key: str) -> bool:
        """Delete a key from this scope."""
        if self.readonly:
            raise InvalidScopeError(f"Scope '{self.name}' is readonly")
        if key in self.data:
            del self.data[key]
            return True
        return False
    
    def has(self, key: str) -> bool:
        """Check if key exists in this scope or parent scopes."""
        if key in self.data:
            return True
        if self.parent:
            return self.parent.has(key)
        return False
    
    def has_local(self, key: str) -> bool:
        """Check if key exists only in this scope."""
        return key in self.data
    
    def keys(self, include_parents: bool = True) -> List[str]:
        """Get all keys in this scope (and optionally parents)."""
        keys = list(self.data.keys())
        if include_parents and self.parent:
            # Add parent keys that aren't overridden
            for key in self.parent.keys(include_parents=True):
                if key not in keys:
                    keys.append(key)
        return keys
    
    def items(self, include_parents: bool = True) -> Dict[str, Any]:
        """Get all items as a dictionary."""
        result = {}
        if include_parents and self.parent:
            result.update(self.parent.items(include_parents=True))
        result.update(self.data)
        return result
    
    def clear(self) -> None:
        """Clear all data in this scope."""
        if self.readonly:
            raise InvalidScopeError(f"Scope '{self.name}' is readonly")
        self.data.clear()
    
    def depth(self) -> int:
        """Get the depth of this scope in the hierarchy."""
        if self.parent is None:
            return 0
        return 1 + self.parent.depth()
    
    def path(self) -> List[str]:
        """Get the path from root to this scope."""
        if self.parent is None:
            return [self.name]
        return self.parent.path() + [self.name]
    
    def age(self) -> float:
        """Get the age of this scope in seconds."""
        return time.time() - self.created_at


class ScopedContext:
    """
    Thread-safe scoped context manager.
    
    Provides hierarchical scopes for storing context data.
    Each thread has its own scope stack.
    
    Features:
    - Thread-safe storage
    - Hierarchical scopes with inheritance
    - Context propagation
    - Scope lifecycle management
    
    Example:
        >>> ctx = ScopedContext()
        >>> with ctx.scope('request'):
        ...     ctx.set('user_id', 123)
        ...     with ctx.scope('transaction'):
        ...         ctx.set('transaction_id', 'abc')
        ...         print(ctx.get('user_id'))  # Inherited from parent
    """
    
    def __init__(self, name: str = 'root'):
        """Initialize scoped context."""
        self._name = name
        self._lock = threading.RLock()
        self._local = threading.local()
        
        # Initialize root scope
        self._init_thread()
    
    def _init_thread(self) -> None:
        """Initialize thread-local storage."""
        if not hasattr(self._local, 'scope_stack'):
            root_scope = Scope(name=self._name, readonly=False)
            self._local.scope_stack = [root_scope]
    
    @property
    def current_scope(self) -> Scope:
        """Get the current scope."""
        self._init_thread()
        return self._local.scope_stack[-1]
    
    @property
    def root_scope(self) -> Scope:
        """Get the root scope."""
        self._init_thread()
        return self._local.scope_stack[0]
    
    @property
    def scope_depth(self) -> int:
        """Get the current scope depth."""
        self._init_thread()
        return len(self._local.scope_stack) - 1
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the current scope chain."""
        with self._lock:
            return self.current_scope.get(key, default)
    
    def get_local(self, key: str, default: Any = None) -> Any:
        """Get a value only from the current scope."""
        with self._lock:
            return self.current_scope.get_local(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in the current scope."""
        with self._lock:
            self.current_scope.set(key, value)
    
    def delete(self, key: str) -> bool:
        """Delete a key from the current scope."""
        with self._lock:
            return self.current_scope.delete(key)
    
    def has(self, key: str) -> bool:
        """Check if key exists in scope chain."""
        with self._lock:
            return self.current_scope.has(key)
    
    def has_local(self, key: str) -> bool:
        """Check if key exists only in current scope."""
        with self._lock:
            return self.current_scope.has_local(key)
    
    def keys(self) -> List[str]:
        """Get all keys in the current scope chain."""
        with self._lock:
            return self.current_scope.keys()
    
    def items(self) -> Dict[str, Any]:
        """Get all items in the current scope chain."""
        with self._lock:
            return self.current_scope.items()
    
    def clear(self) -> None:
        """Clear the current scope."""
        with self._lock:
            self.current_scope.clear()
    
    @contextmanager
    def scope(self, name: str, readonly: bool = False) -> Iterator[Scope]:
        """
        Create a new nested scope.
        
        Args:
            name: Scope name
            readonly: Whether the scope is readonly
            
        Yields:
            The new scope
        """
        self._init_thread()
        with self._lock:
            parent = self.current_scope
            new_scope = Scope(name=name, parent=parent, readonly=readonly)
            self._local.scope_stack.append(new_scope)
        
        try:
            yield new_scope
        finally:
            with self._lock:
                self._local.scope_stack.pop()
    
    @contextmanager
    def override(self, **kwargs) -> Iterator[None]:
        """
        Temporarily override values in the current scope.
        
        Args:
            **kwargs: Key-value pairs to override
            
        Example:
            >>> with ctx.override(user='admin', role='superuser'):
            ...     print(ctx.get('user'))  # 'admin'
            >>> print(ctx.get('user'))  # Original value
        """
        self._init_thread()
        old_values = {}
        
        with self._lock:
            scope = self.current_scope
            
            # Save old values
            for key, value in kwargs.items():
                if scope.has_local(key):
                    old_values[key] = scope.get_local(key)
                else:
                    old_values[key] = ...  # Mark as not existing
            
            # Set new values
            for key, value in kwargs.items():
                scope.set(key, value)
        
        try:
            yield
        finally:
            with self._lock:
                scope = self.current_scope
                for key, old_value in old_values.items():
                    if old_value is ...:
                        scope.delete(key)
                    else:
                        scope.set(key, old_value)
    
    def snapshot(self) -> Dict[str, Any]:
        """Take a snapshot of the current context state."""
        with self._lock:
            return copy.deepcopy(self.items())
    
    def restore(self, snapshot: Dict[str, Any]) -> None:
        """Restore context from a snapshot."""
        with self._lock:
            self.current_scope.clear()
            for key, value in snapshot.items():
                self.current_scope.set(key, value)
    
    def scope_path(self) -> List[str]:
        """Get the path from root to current scope."""
        with self._lock:
            return self.current_scope.path()
    
    def get_scope_by_name(self, name: str) -> Optional[Scope]:
        """Find a scope by name in the current stack."""
        self._init_thread()
        with self._lock:
            for scope in reversed(self._local.scope_stack):
                if scope.name == name:
                    return scope
        return None
    
    def __getitem__(self, key: str) -> Any:
        """Get item using bracket notation."""
        value = self.get(key, default=...)
        if value is ...:
            raise ContextNotFoundError(f"Key '{key}' not found in context")
        return value
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set item using bracket notation."""
        self.set(key, value)
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists."""
        return self.has(key)
    
    def __repr__(self) -> str:
        return f"ScopedContext(name='{self._name}', depth={self.scope_depth})"


# =============================================================================
# Request Context (Global-like Flask's g)
# =============================================================================

class RequestContext:
    """
    Request-scoped context manager.
    
    Similar to Flask's 'g' object, provides per-request storage
    that is automatically cleaned up after the request ends.
    
    Thread-safe and can be used as a context manager or decorator.
    
    Example:
        >>> req_ctx = RequestContext()
        >>> with req_ctx:
        ...     req_ctx.user_id = 123
        ...     req_ctx.request_id = 'abc-123'
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._local = threading.local()
        self._active = threading.local()
    
    def _ensure_data(self) -> None:
        """Ensure thread-local data exists."""
        if not hasattr(self._local, 'data'):
            self._local.data = {}
        if not hasattr(self._local, 'request_id'):
            self._local.request_id = None
        if not hasattr(self._local, 'start_time'):
            self._local.start_time = None
    
    @property
    def active(self) -> bool:
        """Check if a request context is active."""
        return getattr(self._active, 'value', False)
    
    @property
    def request_id(self) -> Optional[str]:
        """Get the current request ID."""
        self._ensure_data()
        return self._local.request_id
    
    @property
    def elapsed(self) -> Optional[float]:
        """Get elapsed time since context start."""
        self._ensure_data()
        if self._local.start_time:
            return time.time() - self._local.start_time
        return None
    
    def start(self, request_id: Optional[str] = None) -> 'RequestContext':
        """Start a new request context."""
        self._ensure_data()
        self._active.value = True
        self._local.request_id = request_id or str(uuid.uuid4())[:12]
        self._local.start_time = time.time()
        self._local.data = {}
        return self
    
    def end(self) -> None:
        """End the current request context."""
        self._ensure_data()
        self._active.value = False
        self._local.request_id = None
        self._local.start_time = None
        self._local.data.clear()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the request context."""
        self._ensure_data()
        return self._local.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in the request context."""
        self._ensure_data()
        self._local.data[key] = value
    
    def delete(self, key: str) -> bool:
        """Delete a key from the request context."""
        self._ensure_data()
        if key in self._local.data:
            del self._local.data[key]
            return True
        return False
    
    def has(self, key: str) -> bool:
        """Check if key exists in request context."""
        self._ensure_data()
        return key in self._local.data
    
    def clear(self) -> None:
        """Clear all data in the request context."""
        self._ensure_data()
        self._local.data.clear()
    
    def items(self) -> Dict[str, Any]:
        """Get all items in the request context."""
        self._ensure_data()
        return dict(self._local.data)
    
    def __enter__(self) -> 'RequestContext':
        return self.start()
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.end()
    
    def __call__(self, func: Callable) -> Callable:
        """Use as a decorator."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper
    
    def __getattr__(self, name: str) -> Any:
        """Allow attribute-style access."""
        if name.startswith('_'):
            return super().__getattribute__(name)
        return self.get(name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Allow attribute-style setting."""
        if name.startswith('_') or name in ('_initialized', '_local', '_active', '_instance', '_lock'):
            super().__setattr__(name, value)
        else:
            self.set(name, value)
    
    def __delattr__(self, name: str) -> None:
        """Allow attribute-style deletion."""
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            self.delete(name)
    
    def __repr__(self) -> str:
        self._ensure_data()
        status = "active" if self.active else "inactive"
        return f"RequestContext({status}, request_id={self.request_id})"


# =============================================================================
# Context Variable (like contextvars.ContextVar)
# =============================================================================

class ContextVar(Generic[T]):
    """
    A context variable that can have different values in different contexts.
    
    Similar to Python's contextvars.ContextVar but with additional features
    like default values, type hints, and change callbacks.
    
    Example:
        >>> user_id = ContextVar('user_id', default=None)
        >>> user_id.set(123)
        >>> print(user_id.get())  # 123
    """
    
    def __init__(
        self,
        name: str,
        default: Any = ...,
        on_change: Optional[Callable[[Any, Any], None]] = None
    ):
        """
        Initialize context variable.
        
        Args:
            name: Variable name
            default: Default value (default: no default, raises on missing)
            on_change: Callback called when value changes (old_value, new_value)
        """
        self._name = name
        self._default = default
        self._on_change = on_change
        self._local = threading.local()
    
    def _ensure_data(self) -> None:
        """Ensure thread-local storage exists."""
        if not hasattr(self._local, 'stack'):
            self._local.stack = []
    
    def get(self, default: Any = ...) -> T:
        """
        Get the current value.
        
        Args:
            default: Default value if not set (overrides instance default)
            
        Returns:
            Current value
            
        Raises:
            ContextNotFoundError: If no value and no default
        """
        self._ensure_data()
        if self._local.stack:
            return self._local.stack[-1]
        
        # Use provided default or instance default
        if default is not ...:
            return default
        if self._default is not ...:
            return self._default
        
        raise ContextNotFoundError(f"Context variable '{self._name}' has no value")
    
    def set(self, value: T) -> None:
        """
        Set the current value.
        
        Args:
            value: New value
        """
        self._ensure_data()
        old_value = self._local.stack[-1] if self._local.stack else ...
        self._local.stack.append(value)
        
        if self._on_change:
            self._on_change(old_value, value)
    
    def reset(self) -> bool:
        """
        Reset to previous value.
        
        Returns:
            True if reset, False if no previous value
        """
        self._ensure_data()
        if len(self._local.stack) > 1:
            old_value = self._local.stack.pop()
            new_value = self._local.stack[-1] if self._local.stack else ...
            if self._on_change:
                self._on_change(old_value, new_value if new_value is not ... else None)
            return True
        elif self._local.stack:
            old_value = self._local.stack.pop()
            if self._on_change:
                self._on_change(old_value, self._default if self._default is not ... else None)
            return True
        return False
    
    def clear(self) -> None:
        """Clear all values."""
        self._ensure_data()
        self._local.stack.clear()
    
    def is_set(self) -> bool:
        """Check if a value is set."""
        self._ensure_data()
        return bool(self._local.stack)
    
    @contextmanager
    def using(self, value: T) -> Iterator[T]:
        """
        Context manager to temporarily set a value.
        
        Args:
            value: Temporary value
            
        Yields:
            The temporary value
        """
        self.set(value)
        try:
            yield value
        finally:
            self.reset()
    
    @property
    def name(self) -> str:
        """Get the variable name."""
        return self._name
    
    def __repr__(self) -> str:
        try:
            value = self.get()
            return f"ContextVar('{self._name}', value={value!r})"
        except ContextNotFoundError:
            return f"ContextVar('{self._name}', <no value>)"


# =============================================================================
# Context Propagator
# =============================================================================

class ContextPropagator:
    """
    Propagate context across boundaries (threads, tasks, etc.).
    
    Captures the current context state and can apply it elsewhere.
    
    Example:
        >>> propagator = ContextPropagator()
        >>> propagator.capture()  # Capture current context
        >>> # In another thread:
        >>> propagator.apply()  # Apply captured context
    """
    
    def __init__(self, context: Optional[ScopedContext] = None):
        """
        Initialize propagator.
        
        Args:
            context: ScopedContext to propagate (default: global context)
        """
        self._context = context
        self._captured: Dict[str, Any] = {}
        self._timestamp: Optional[float] = None
    
    def capture(self, keys: Optional[List[str]] = None) -> 'ContextPropagator':
        """
        Capture current context state.
        
        Args:
            keys: Specific keys to capture (default: all)
            
        Returns:
            Self for chaining
        """
        ctx = self._context or _global_context
        if keys:
            self._captured = {k: ctx.get(k) for k in keys if ctx.has(k)}
        else:
            self._captured = ctx.snapshot()
        self._timestamp = time.time()
        return self
    
    def apply(self, override: bool = False) -> 'ContextPropagator':
        """
        Apply captured context to current context.
        
        Args:
            override: Whether to override existing values
            
        Returns:
            Self for chaining
        """
        ctx = self._context or _global_context
        for key, value in self._captured.items():
            if override or not ctx.has(key):
                ctx.set(key, value)
        return self
    
    @property
    def captured_items(self) -> Dict[str, Any]:
        """Get captured items."""
        return dict(self._captured)
    
    @property
    def age(self) -> Optional[float]:
        """Get age of captured context in seconds."""
        if self._timestamp:
            return time.time() - self._timestamp
        return None
    
    @contextmanager
    def propagate(self, keys: Optional[List[str]] = None) -> Iterator[Dict[str, Any]]:
        """
        Context manager for propagation.
        
        Captures context on enter, restores on exit.
        
        Args:
            keys: Specific keys to propagate (default: all)
            
        Yields:
            Captured items
        """
        self.capture(keys)
        try:
            yield self._captured
        finally:
            # Use override=True to restore captured values
            self.apply(override=True)
    
    def __repr__(self) -> str:
        return f"ContextPropagator(keys={len(self._captured)}, age={self.age:.2f}s)"


# =============================================================================
# Global Context Instance
# =============================================================================

_global_context = ScopedContext(name='global')
_global_request_context = RequestContext()


# =============================================================================
# Convenience Functions
# =============================================================================

def get_context() -> ScopedContext:
    """Get the global scoped context."""
    return _global_context


def get_request_context() -> RequestContext:
    """Get the global request context."""
    return _global_request_context


def ctx_get(key: str, default: Any = None) -> Any:
    """Get a value from the global context."""
    return _global_context.get(key, default)


def ctx_set(key: str, value: Any) -> None:
    """Set a value in the global context."""
    _global_context.set(key, value)


def ctx_has(key: str) -> bool:
    """Check if key exists in global context."""
    return _global_context.has(key)


def ctx_delete(key: str) -> bool:
    """Delete a key from global context."""
    return _global_context.delete(key)


def ctx_scope(name: str, readonly: bool = False):
    """Create a new scope in the global context."""
    return _global_context.scope(name, readonly)


def ctx_snapshot() -> Dict[str, Any]:
    """Take a snapshot of the global context."""
    return _global_context.snapshot()


def ctx_restore(snapshot: Dict[str, Any]) -> None:
    """Restore global context from a snapshot."""
    _global_context.restore(snapshot)


# =============================================================================
# Decorators
# =============================================================================

def with_context(**kwargs):
    """
    Decorator to set context values for a function.
    
    Args:
        **kwargs: Key-value pairs to set in context
        
    Example:
        >>> @with_context(user='admin', role='superuser')
        ... def my_function():
        ...     print(ctx_get('user'))  # 'admin'
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **fkwargs):
            with _global_context.override(**kwargs):
                return func(*args, **fkwargs)
        return wrapper
    return decorator


def with_scope(name: str, readonly: bool = False):
    """
    Decorator to run a function in a new scope.
    
    Args:
        name: Scope name
        readonly: Whether scope is readonly
        
    Example:
        >>> @with_scope('transaction')
        ... def my_function():
        ...     ctx_set('transaction_id', 'abc')
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            with _global_context.scope(name, readonly):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def request_context(func: Callable) -> Callable:
    """
    Decorator to run a function with a request context.
    
    Example:
        >>> @request_context
        ... def handle_request():
        ...     print(req.request_id)
    """
    return _global_request_context(func)


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Exceptions
    'ContextError',
    'ContextNotFoundError',
    'ScopeNotFoundError',
    'InvalidScopeError',
    # Classes
    'Scope',
    'ScopedContext',
    'RequestContext',
    'ContextVar',
    'ContextPropagator',
    # Decorators
    'with_context',
    'with_scope',
    'request_context',
    # Convenience functions
    'get_context',
    'get_request_context',
    'ctx_get',
    'ctx_set',
    'ctx_has',
    'ctx_delete',
    'ctx_scope',
    'ctx_snapshot',
    'ctx_restore',
]