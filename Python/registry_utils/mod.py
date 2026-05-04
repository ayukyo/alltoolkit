#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Registry Pattern Utilities Module
================================================

A comprehensive implementation of the Registry Pattern for flexible
registration, lookup, and management of objects, services, handlers,
factories, and types.

Features:
- Generic registry with type-safe operations
- Service registry with lazy initialization
- Plugin registry with metadata support
- Handler registry for event/command handling
- Factory registry with automatic instantiation
- Type registry for dynamic type lookup
- Namespace support for organization
- Priority-based ordering
- Thread-safe operations
- Decorator-based registration
- Zero external dependencies

Author: AllToolkit
License: MIT
"""

import threading
import functools
from typing import (
    TypeVar, Generic, Dict, List, Optional, Callable, Any,
    Type, Set, Tuple, Union
)
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod
from collections import defaultdict
import inspect


# =============================================================================
# Type Variables
# =============================================================================

T = TypeVar('T')


# =============================================================================
# Exceptions
# =============================================================================

class RegistryError(Exception):
    """Base exception for registry errors."""
    pass


class AlreadyRegisteredError(RegistryError):
    """Raised when attempting to register an already registered item."""
    pass


class NotRegisteredError(RegistryError):
    """Raised when attempting to access an unregistered item."""
    pass


class RegistrationConflictError(RegistryError):
    """Raised when there's a conflict in registration."""
    pass


# =============================================================================
# Priority Enum
# =============================================================================

class Priority(Enum):
    """Priority levels for ordered registration."""
    LOWEST = 0
    LOW = 25
    NORMAL = 50
    HIGH = 75
    HIGHEST = 100


# =============================================================================
# Registry Item Dataclass
# =============================================================================

@dataclass
class RegistryItem(Generic[T]):
    """Container for a registered item with metadata."""
    name: str
    item: T
    priority: int = Priority.NORMAL.value
    namespace: str = "default"
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)
    registered_at: float = field(default_factory=lambda: threading.get_ident())
    lazy: bool = False
    factory: Optional[Callable[[], T]] = None
    
    def __lt__(self, other: 'RegistryItem') -> bool:
        """Compare by priority (higher priority comes first)."""
        return self.priority > other.priority


# =============================================================================
# Base Registry
# =============================================================================

class BaseRegistry(Generic[T]):
    """
    Base registry implementation with common operations.
    
    Provides thread-safe registration, lookup, and management of items.
    
    Example:
        >>> registry = BaseRegistry[str]()
        >>> registry.register("greeting", "Hello, World!")
        >>> registry.get("greeting")
        'Hello, World!'
    """
    
    def __init__(self, name: str = "default"):
        """
        Initialize the registry.
        
        Args:
            name: Registry name for identification
        """
        self._name = name
        self._items: Dict[str, RegistryItem[T]] = {}
        self._namespaces: Dict[str, Set[str]] = defaultdict(set)
        self._tags: Dict[str, Set[str]] = defaultdict(set)
        self._lock = threading.RLock()
        self._on_register_hooks: List[Callable[[str, T], None]] = []
        self._on_unregister_hooks: List[Callable[[str, T], None]] = []
    
    @property
    def name(self) -> str:
        """Get registry name."""
        return self._name
    
    @property
    def count(self) -> int:
        """Get number of registered items."""
        return len(self._items)
    
    @property
    def is_empty(self) -> bool:
        """Check if registry is empty."""
        return len(self._items) == 0
    
    def register(
        self,
        name: str,
        item: T,
        *,
        priority: int = Priority.NORMAL.value,
        namespace: str = "default",
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[Set[str]] = None,
        overwrite: bool = False
    ) -> None:
        """
        Register an item.
        
        Args:
            name: Unique name for the item
            item: The item to register
            priority: Priority level (higher = more important)
            namespace: Namespace for organization
            metadata: Additional metadata
            tags: Tags for categorization
            overwrite: Whether to overwrite existing registration
            
        Raises:
            AlreadyRegisteredError: If item exists and overwrite=False
        """
        with self._lock:
            full_name = self._get_full_name(name, namespace)
            
            if full_name in self._items and not overwrite:
                raise AlreadyRegisteredError(
                    f"Item '{name}' already registered in namespace '{namespace}'"
                )
            
            registry_item = RegistryItem(
                name=name,
                item=item,
                priority=priority,
                namespace=namespace,
                metadata=metadata or {},
                tags=tags or set()
            )
            
            # Remove old item from indices if overwriting
            if full_name in self._items:
                old_item = self._items[full_name]
                self._namespaces[namespace].discard(full_name)
                for tag in old_item.tags:
                    self._tags[tag].discard(full_name)
            
            self._items[full_name] = registry_item
            self._namespaces[namespace].add(full_name)
            
            for tag in registry_item.tags:
                self._tags[tag].add(full_name)
            
            # Call hooks
            for hook in self._on_register_hooks:
                hook(name, item)
    
    def unregister(self, name: str, namespace: str = "default") -> T:
        """
        Unregister an item.
        
        Args:
            name: Name of the item
            namespace: Namespace of the item
            
        Returns:
            The unregistered item
            
        Raises:
            NotRegisteredError: If item is not registered
        """
        with self._lock:
            full_name = self._get_full_name(name, namespace)
            
            if full_name not in self._items:
                raise NotRegisteredError(
                    f"Item '{name}' not registered in namespace '{namespace}'"
                )
            
            registry_item = self._items.pop(full_name)
            self._namespaces[namespace].discard(full_name)
            
            for tag in registry_item.tags:
                self._tags[tag].discard(full_name)
            
            # Call hooks
            for hook in self._on_unregister_hooks:
                hook(name, registry_item.item)
            
            return registry_item.item
    
    def get(self, name: str, namespace: str = "default") -> T:
        """
        Get a registered item.
        
        Args:
            name: Name of the item
            namespace: Namespace of the item
            
        Returns:
            The registered item
            
        Raises:
            NotRegisteredError: If item is not registered
        """
        with self._lock:
            full_name = self._get_full_name(name, namespace)
            
            if full_name not in self._items:
                raise NotRegisteredError(
                    f"Item '{name}' not registered in namespace '{namespace}'"
                )
            
            return self._items[full_name].item
    
    def try_get(self, name: str, namespace: str = "default") -> Optional[T]:
        """
        Try to get a registered item.
        
        Args:
            name: Name of the item
            namespace: Namespace of the item
            
        Returns:
            The registered item or None if not found
        """
        with self._lock:
            full_name = self._get_full_name(name, namespace)
            item = self._items.get(full_name)
            return item.item if item else None
    
    def contains(self, name: str, namespace: str = "default") -> bool:
        """Check if an item is registered."""
        with self._lock:
            full_name = self._get_full_name(name, namespace)
            return full_name in self._items
    
    def get_all(self) -> Dict[str, T]:
        """Get all registered items."""
        with self._lock:
            return {k: v.item for k, v in self._items.items()}
    
    def get_by_namespace(self, namespace: str) -> Dict[str, T]:
        """Get all items in a namespace."""
        with self._lock:
            return {
                name: self._items[full_name].item
                for full_name in self._namespaces.get(namespace, set())
                for name in [self._items[full_name].name]
            }
    
    def get_by_tag(self, tag: str) -> Dict[str, T]:
        """Get all items with a specific tag."""
        with self._lock:
            return {
                self._items[full_name].name: self._items[full_name].item
                for full_name in self._tags.get(tag, set())
            }
    
    def get_namespaces(self) -> Set[str]:
        """Get all namespaces."""
        with self._lock:
            return set(self._namespaces.keys())
    
    def get_tags(self) -> Set[str]:
        """Get all tags."""
        with self._lock:
            return set(self._tags.keys())
    
    def get_names(self, namespace: Optional[str] = None) -> List[str]:
        """
        Get all registered names.
        
        Args:
            namespace: Optional namespace filter
            
        Returns:
            List of registered names
        """
        with self._lock:
            if namespace:
                return [
                    self._items[full_name].name
                    for full_name in self._namespaces.get(namespace, set())
                ]
            return [v.name for v in self._items.values()]
    
    def clear(self, namespace: Optional[str] = None) -> int:
        """
        Clear items from registry.
        
        Args:
            namespace: Optional namespace to clear (None = clear all)
            
        Returns:
            Number of items cleared
        """
        with self._lock:
            if namespace is None:
                count = len(self._items)
                self._items.clear()
                self._namespaces.clear()
                self._tags.clear()
                return count
            
            if namespace not in self._namespaces:
                return 0
            
            count = 0
            for full_name in list(self._namespaces[namespace]):
                self.unregister(self._items[full_name].name, namespace)
                count += 1
            
            return count
    
    def get_metadata(self, name: str, namespace: str = "default") -> Dict[str, Any]:
        """Get metadata for a registered item."""
        with self._lock:
            full_name = self._get_full_name(name, namespace)
            if full_name not in self._items:
                raise NotRegisteredError(
                    f"Item '{name}' not registered in namespace '{namespace}'"
                )
            return self._items[full_name].metadata.copy()
    
    def set_metadata(
        self, name: str, key: str, value: Any, namespace: str = "default"
    ) -> None:
        """Set metadata for a registered item."""
        with self._lock:
            full_name = self._get_full_name(name, namespace)
            if full_name not in self._items:
                raise NotRegisteredError(
                    f"Item '{name}' not registered in namespace '{namespace}'"
                )
            self._items[full_name].metadata[key] = value
    
    def add_hook_on_register(self, hook: Callable[[str, T], None]) -> None:
        """Add a hook to be called on registration."""
        self._on_register_hooks.append(hook)
    
    def add_hook_on_unregister(self, hook: Callable[[str, T], None]) -> None:
        """Add a hook to be called on unregistration."""
        self._on_unregister_hooks.append(hook)
    
    def decorator(
        self,
        name: Optional[str] = None,
        *,
        priority: int = Priority.NORMAL.value,
        namespace: str = "default",
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[Set[str]] = None
    ) -> Callable[[T], T]:
        """
        Create a decorator for registration.
        
        Args:
            name: Optional name (defaults to function/class name)
            priority: Priority level
            namespace: Namespace for organization
            metadata: Additional metadata
            tags: Tags for categorization
            
        Returns:
            Decorator function
        """
        def decorator_func(item: T) -> T:
            reg_name = name or getattr(item, '__name__', str(item))
            self.register(
                reg_name, item,
                priority=priority,
                namespace=namespace,
                metadata=metadata,
                tags=tags
            )
            return item
        
        return decorator_func
    
    def _get_full_name(self, name: str, namespace: str) -> str:
        """Get fully qualified name."""
        return f"{namespace}:{name}"
    
    def __contains__(self, name: str) -> bool:
        """Support 'in' operator."""
        return self.contains(name)
    
    def __getitem__(self, name: str) -> T:
        """Support bracket access."""
        return self.get(name)
    
    def __len__(self) -> int:
        """Support len()."""
        return self.count
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self._name!r}, count={self.count})"


# =============================================================================
# Service Registry
# =============================================================================

class ServiceRegistry(Generic[T]):
    """
    Service registry with lazy initialization support.
    
    Provides service registration with lazy initialization,
    singleton pattern, and dependency management.
    
    Example:
        >>> registry = ServiceRegistry[Database]()
        >>> registry.register_factory("db", lambda: Database("localhost"))
        >>> db = registry.get("db")  # Created on first access
    """
    
    def __init__(self, name: str = "services"):
        """Initialize the service registry."""
        self._name = name
        self._services: Dict[str, RegistryItem[T]] = {}
        self._instances: Dict[str, T] = {}
        self._lock = threading.RLock()
        self._initializing: Set[str] = set()
    
    def register(
        self,
        name: str,
        instance: T,
        *,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[Set[str]] = None
    ) -> None:
        """
        Register a service instance.
        
        Args:
            name: Service name
            instance: Service instance
            metadata: Additional metadata
            tags: Tags for categorization
        """
        with self._lock:
            self._services[name] = RegistryItem(
                name=name,
                item=instance,
                metadata=metadata or {},
                tags=tags or set()
            )
            self._instances[name] = instance
    
    def register_factory(
        self,
        name: str,
        factory: Callable[[], T],
        *,
        singleton: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[Set[str]] = None
    ) -> None:
        """
        Register a service factory.
        
        Args:
            name: Service name
            factory: Factory function to create the service
            singleton: Whether to cache the instance
            metadata: Additional metadata
            tags: Tags for categorization
        """
        with self._lock:
            self._services[name] = RegistryItem(
                name=name,
                item=None,  # Will be created lazily
                factory=factory,
                lazy=True,
                metadata=metadata or {},
                tags=tags or set()
            )
            if not singleton:
                self._services[name].metadata["singleton"] = False
    
    def get(self, name: str) -> T:
        """
        Get a service instance.
        
        For factory-registered services, creates the instance on first access.
        
        Args:
            name: Service name
            
        Returns:
            Service instance
            
        Raises:
            NotRegisteredError: If service is not registered
        """
        with self._lock:
            if name not in self._services:
                raise NotRegisteredError(f"Service '{name}' is not registered")
            
            item = self._services[name]
            
            # Return cached instance if available
            if name in self._instances:
                return self._instances[name]
            
            # Not a lazy service, return the instance
            if not item.lazy:
                return item.item
            
            # Detect circular dependencies
            if name in self._initializing:
                raise RegistryError(
                    f"Circular dependency detected while initializing '{name}'"
                )
            
            # Create instance from factory
            self._initializing.add(name)
            try:
                instance = item.factory()  # type: ignore
                
                # Cache if singleton
                if item.metadata.get("singleton", True):
                    self._instances[name] = instance
                
                return instance
            finally:
                self._initializing.discard(name)
    
    def try_get(self, name: str) -> Optional[T]:
        """Try to get a service instance."""
        try:
            return self.get(name)
        except NotRegisteredError:
            return None
    
    def contains(self, name: str) -> bool:
        """Check if a service is registered."""
        with self._lock:
            return name in self._services
    
    def unregister(self, name: str, dispose: bool = True) -> Optional[T]:
        """
        Unregister a service.
        
        Args:
            name: Service name
            dispose: Whether to dispose the instance if possible
            
        Returns:
            The service instance or None
        """
        with self._lock:
            if name not in self._services:
                return None
            
            instance = self._instances.pop(name, None)
            del self._services[name]
            
            # Dispose if supported
            if dispose and instance is not None:
                if hasattr(instance, 'dispose'):
                    instance.dispose()
                elif hasattr(instance, 'close'):
                    instance.close()
                elif hasattr(instance, 'shutdown'):
                    instance.shutdown()
            
            return instance
    
    def get_names(self) -> List[str]:
        """Get all registered service names."""
        with self._lock:
            return list(self._services.keys())
    
    def get_by_tag(self, tag: str) -> Dict[str, T]:
        """Get all services with a specific tag."""
        with self._lock:
            return {
                name: self.get(name)
                for name, item in self._services.items()
                if tag in item.tags
            }
    
    def clear(self, dispose: bool = True) -> int:
        """
        Clear all services.
        
        Args:
            dispose: Whether to dispose instances
            
        Returns:
            Number of services cleared
        """
        with self._lock:
            count = len(self._services)
            
            if dispose:
                for name in list(self._services.keys()):
                    self.unregister(name, dispose=True)
            else:
                self._services.clear()
                self._instances.clear()
            
            return count
    
    def __contains__(self, name: str) -> bool:
        return self.contains(name)
    
    def __getitem__(self, name: str) -> T:
        return self.get(name)
    
    def __len__(self) -> int:
        return len(self._services)


# =============================================================================
# Plugin Registry
# =============================================================================

@dataclass
class PluginInfo:
    """Information about a registered plugin."""
    name: str
    version: str
    description: str = ""
    author: str = ""
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True


class PluginRegistry:
    """
    Plugin registry with lifecycle management.
    
    Provides plugin registration, enabling/disabling,
    dependency checking, and lifecycle hooks.
    
    Example:
        >>> registry = PluginRegistry()
        >>> @registry.register_plugin("auth", "1.0.0")
        ... class AuthPlugin:
        ...     def activate(self): pass
        ...     def deactivate(self): pass
    """
    
    def __init__(self, name: str = "plugins"):
        """Initialize the plugin registry."""
        self._name = name
        self._plugins: Dict[str, Tuple[Any, PluginInfo]] = {}
        self._lock = threading.RLock()
        self._on_enable_hooks: List[Callable[[str, Any], None]] = []
        self._on_disable_hooks: List[Callable[[str, Any], None]] = []
    
    def register(
        self,
        name: str,
        plugin: Any,
        *,
        version: str = "1.0.0",
        description: str = "",
        author: str = "",
        dependencies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        enabled: bool = True
    ) -> None:
        """
        Register a plugin.
        
        Args:
            name: Plugin name
            plugin: Plugin instance
            version: Plugin version
            description: Plugin description
            author: Plugin author
            dependencies: List of required plugin names
            metadata: Additional metadata
            enabled: Whether plugin is enabled initially
        """
        with self._lock:
            info = PluginInfo(
                name=name,
                version=version,
                description=description,
                author=author,
                dependencies=dependencies or [],
                metadata=metadata or {},
                enabled=enabled
            )
            self._plugins[name] = (plugin, info)
    
    def decorator(
        self,
        name: str,
        version: str = "1.0.0",
        **kwargs: Any
    ) -> Callable[[T], T]:
        """
        Decorator for registering a plugin.
        
        Args:
            name: Plugin name
            version: Plugin version
            **kwargs: Additional plugin info
            
        Returns:
            Decorator function
        """
        def decorator_func(cls: T) -> T:
            self.register(name, cls, version=version, **kwargs)
            return cls
        return decorator_func
    
    def unregister(self, name: str) -> Optional[Tuple[Any, PluginInfo]]:
        """
        Unregister a plugin.
        
        Args:
            name: Plugin name
            
        Returns:
            Tuple of (plugin, info) or None
        """
        with self._lock:
            if name not in self._plugins:
                return None
            
            plugin, info = self._plugins.pop(name)
            
            # Deactivate if enabled
            if info.enabled:
                self._call_lifecycle(plugin, "deactivate")
            
            return plugin, info
    
    def get(self, name: str) -> Any:
        """
        Get a plugin instance.
        
        Args:
            name: Plugin name
            
        Returns:
            Plugin instance
            
        Raises:
            NotRegisteredError: If plugin is not registered
        """
        with self._lock:
            if name not in self._plugins:
                raise NotRegisteredError(f"Plugin '{name}' is not registered")
            return self._plugins[name][0]
    
    def get_info(self, name: str) -> PluginInfo:
        """Get plugin information."""
        with self._lock:
            if name not in self._plugins:
                raise NotRegisteredError(f"Plugin '{name}' is not registered")
            return self._plugins[name][1]
    
    def enable(self, name: str) -> bool:
        """
        Enable a plugin.
        
        Args:
            name: Plugin name
            
        Returns:
            True if plugin was enabled
        """
        with self._lock:
            if name not in self._plugins:
                raise NotRegisteredError(f"Plugin '{name}' is not registered")
            
            plugin, info = self._plugins[name]
            
            if info.enabled:
                return False
            
            # Check dependencies
            for dep in info.dependencies:
                if dep not in self._plugins:
                    raise RegistryError(
                        f"Missing dependency '{dep}' for plugin '{name}'"
                    )
                if not self._plugins[dep][1].enabled:
                    raise RegistryError(
                        f"Dependency '{dep}' is not enabled for plugin '{name}'"
                    )
            
            info.enabled = True
            self._call_lifecycle(plugin, "activate")
            
            for hook in self._on_enable_hooks:
                hook(name, plugin)
            
            return True
    
    def disable(self, name: str) -> bool:
        """
        Disable a plugin.
        
        Args:
            name: Plugin name
            
        Returns:
            True if plugin was disabled
        """
        with self._lock:
            if name not in self._plugins:
                raise NotRegisteredError(f"Plugin '{name}' is not registered")
            
            plugin, info = self._plugins[name]
            
            if not info.enabled:
                return False
            
            # Check if other plugins depend on this one
            for other_name, (other_plugin, other_info) in self._plugins.items():
                if name in other_info.dependencies and other_info.enabled:
                    raise RegistryError(
                        f"Cannot disable '{name}': plugin '{other_name}' depends on it"
                    )
            
            info.enabled = False
            self._call_lifecycle(plugin, "deactivate")
            
            for hook in self._on_disable_hooks:
                hook(name, plugin)
            
            return True
    
    def is_enabled(self, name: str) -> bool:
        """Check if a plugin is enabled."""
        with self._lock:
            if name not in self._plugins:
                return False
            return self._plugins[name][1].enabled
    
    def contains(self, name: str) -> bool:
        """Check if a plugin is registered."""
        with self._lock:
            return name in self._plugins
    
    def get_all(self) -> Dict[str, Any]:
        """Get all plugin instances."""
        with self._lock:
            return {name: plugin for name, (plugin, _) in self._plugins.items()}
    
    def get_enabled(self) -> Dict[str, Any]:
        """Get all enabled plugin instances."""
        with self._lock:
            return {
                name: plugin
                for name, (plugin, info) in self._plugins.items()
                if info.enabled
            }
    
    def get_names(self) -> List[str]:
        """Get all registered plugin names."""
        with self._lock:
            return list(self._plugins.keys())
    
    def check_dependencies(self, name: str) -> Tuple[bool, List[str]]:
        """
        Check if all dependencies are satisfied.
        
        Args:
            name: Plugin name
            
        Returns:
            Tuple of (all_satisfied, missing_dependencies)
        """
        with self._lock:
            if name not in self._plugins:
                return False, []
            
            info = self._plugins[name][1]
            missing = [
                dep for dep in info.dependencies
                if dep not in self._plugins
            ]
            return len(missing) == 0, missing
    
    def add_hook_on_enable(self, hook: Callable[[str, Any], None]) -> None:
        """Add a hook to be called when a plugin is enabled."""
        self._on_enable_hooks.append(hook)
    
    def add_hook_on_disable(self, hook: Callable[[str, Any], None]) -> None:
        """Add a hook to be called when a plugin is disabled."""
        self._on_disable_hooks.append(hook)
    
    def _call_lifecycle(self, plugin: Any, method: str) -> None:
        """Call a lifecycle method on a plugin if it exists."""
        if hasattr(plugin, method):
            getattr(plugin, method)()
    
    def __contains__(self, name: str) -> bool:
        return self.contains(name)
    
    def __getitem__(self, name: str) -> Any:
        return self.get(name)
    
    def __len__(self) -> int:
        return len(self._plugins)


# =============================================================================
# Handler Registry
# =============================================================================

class HandlerRegistry(Generic[T]):
    """
    Handler registry for event/command handling.
    
    Provides handler registration with priority-based execution,
    and support for multiple handlers per event type.
    
    Example:
        >>> registry = HandlerRegistry[Callable[[Event], None]]()
        >>> @registry.handler("user.created", priority=Priority.HIGH.value)
        ... def on_user_created(event):
        ...     print(f"User created: {event}")
    """
    
    def __init__(self, name: str = "handlers"):
        """Initialize the handler registry."""
        self._name = name
        self._handlers: Dict[str, List[RegistryItem[T]]] = defaultdict(list)
        self._lock = threading.RLock()
    
    def register(
        self,
        event_type: str,
        handler: T,
        *,
        priority: int = Priority.NORMAL.value,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Register a handler for an event type.
        
        Args:
            event_type: Event type to handle
            handler: Handler function/object
            priority: Priority level (higher = executed first)
            metadata: Additional metadata
            
        Returns:
            Handler ID for unregistration
        """
        with self._lock:
            handler_id = f"{event_type}:{id(handler)}"
            
            item = RegistryItem(
                name=handler_id,
                item=handler,
                priority=priority,
                metadata=metadata or {}
            )
            
            self._handlers[event_type].append(item)
            # Sort by priority (higher first)
            self._handlers[event_type].sort()
            
            return handler_id
    
    def decorator(
        self,
        event_type: str,
        *,
        priority: int = Priority.NORMAL.value,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Callable[[T], T]:
        """
        Decorator for registering a handler.
        
        Args:
            event_type: Event type to handle
            priority: Priority level
            metadata: Additional metadata
            
        Returns:
            Decorator function
        """
        def decorator_func(handler: T) -> T:
            self.register(event_type, handler, priority=priority, metadata=metadata)
            return handler
        return decorator_func
    
    def unregister(self, event_type: str, handler: T) -> bool:
        """
        Unregister a handler.
        
        Args:
            event_type: Event type
            handler: Handler to unregister
            
        Returns:
            True if handler was unregistered
        """
        with self._lock:
            handlers = self._handlers.get(event_type, [])
            for i, item in enumerate(handlers):
                if item.item is handler:
                    handlers.pop(i)
                    return True
            return False
    
    def unregister_by_id(self, handler_id: str) -> bool:
        """
        Unregister a handler by ID.
        
        Args:
            handler_id: Handler ID returned from register()
            
        Returns:
            True if handler was unregistered
        """
        with self._lock:
            for event_type, handlers in self._handlers.items():
                for i, item in enumerate(handlers):
                    if item.name == handler_id:
                        handlers.pop(i)
                        return True
            return False
    
    def get_handlers(self, event_type: str) -> List[T]:
        """
        Get all handlers for an event type.
        
        Args:
            event_type: Event type
            
        Returns:
            List of handlers sorted by priority
        """
        with self._lock:
            return [item.item for item in self._handlers.get(event_type, [])]
    
    def get_all_handlers(self) -> Dict[str, List[T]]:
        """Get all handlers grouped by event type."""
        with self._lock:
            return {
                event_type: [item.item for item in handlers]
                for event_type, handlers in self._handlers.items()
            }
    
    def has_handlers(self, event_type: str) -> bool:
        """Check if there are handlers for an event type."""
        with self._lock:
            return len(self._handlers.get(event_type, [])) > 0
    
    def clear(self, event_type: Optional[str] = None) -> int:
        """
        Clear handlers.
        
        Args:
            event_type: Optional event type to clear (None = clear all)
            
        Returns:
            Number of handlers cleared
        """
        with self._lock:
            if event_type:
                count = len(self._handlers.get(event_type, []))
                self._handlers[event_type] = []
                return count
            
            count = sum(len(h) for h in self._handlers.values())
            self._handlers.clear()
            return count
    
    def __contains__(self, event_type: str) -> bool:
        return self.has_handlers(event_type)


# =============================================================================
# Factory Registry
# =============================================================================

class FactoryRegistry(Generic[T]):
    """
    Factory registry for object creation.
    
    Provides factory registration and object instantiation
    with support for different creation strategies.
    
    Example:
        >>> registry = FactoryRegistry[Widget]()
        >>> registry.register("button", ButtonWidget)
        >>> registry.register("text", TextWidget)
        >>> button = registry.create("button", text="Click Me")
    """
    
    def __init__(self, name: str = "factories"):
        """Initialize the factory registry."""
        self._name = name
        self._factories: Dict[str, Callable[..., T]] = {}
        self._singletons: Dict[str, T] = {}
        self._is_singleton: Dict[str, bool] = {}
        self._lock = threading.RLock()
    
    def register(
        self,
        name: str,
        factory: Union[Type[T], Callable[..., T]],
        *,
        singleton: bool = False
    ) -> None:
        """
        Register a factory.
        
        Args:
            name: Factory name
            factory: Factory function or class
            singleton: Whether to create only one instance
        """
        with self._lock:
            self._factories[name] = factory
            self._is_singleton[name] = singleton
    
    def decorator(
        self,
        name: str,
        *,
        singleton: bool = False
    ) -> Callable[[Type[T]], Type[T]]:
        """
        Decorator for registering a factory.
        
        Args:
            name: Factory name
            singleton: Whether to create only one instance
            
        Returns:
            Decorator function
        """
        def decorator_func(cls: Type[T]) -> Type[T]:
            self.register(name, cls, singleton=singleton)
            return cls
        return decorator_func
    
    def unregister(self, name: str) -> bool:
        """
        Unregister a factory.
        
        Args:
            name: Factory name
            
        Returns:
            True if factory was unregistered
        """
        with self._lock:
            if name in self._factories:
                del self._factories[name]
                self._singletons.pop(name, None)
                self._is_singleton.pop(name, None)
                return True
            return False
    
    def create(self, name: str, *args: Any, **kwargs: Any) -> T:
        """
        Create an instance using a factory.
        
        Args:
            name: Factory name
            *args: Positional arguments for factory
            **kwargs: Keyword arguments for factory
            
        Returns:
            Created instance
            
        Raises:
            NotRegisteredError: If factory is not registered
        """
        with self._lock:
            if name not in self._factories:
                raise NotRegisteredError(f"Factory '{name}' is not registered")
            
            # Return cached singleton if available
            if self._is_singleton[name] and name in self._singletons:
                return self._singletons[name]
            
            factory = self._factories[name]
            instance = factory(*args, **kwargs)
            
            # Cache if singleton
            if self._is_singleton[name]:
                self._singletons[name] = instance
            
            return instance
    
    def get_factory(self, name: str) -> Callable[..., T]:
        """Get the factory function."""
        with self._lock:
            if name not in self._factories:
                raise NotRegisteredError(f"Factory '{name}' is not registered")
            return self._factories[name]
    
    def contains(self, name: str) -> bool:
        """Check if a factory is registered."""
        with self._lock:
            return name in self._factories
    
    def get_names(self) -> List[str]:
        """Get all registered factory names."""
        with self._lock:
            return list(self._factories.keys())
    
    def clear(self) -> int:
        """Clear all factories."""
        with self._lock:
            count = len(self._factories)
            self._factories.clear()
            self._singletons.clear()
            self._is_singleton.clear()
            return count
    
    def __contains__(self, name: str) -> bool:
        return self.contains(name)
    
    def __getitem__(self, name: str) -> Callable[..., T]:
        return self.get_factory(name)
    
    def __len__(self) -> int:
        return len(self._factories)


# =============================================================================
# Type Registry
# =============================================================================

class TypeRegistry:
    """
    Registry for types with serialization support.
    
    Provides type registration with name-based lookup,
    useful for serialization and plugin systems.
    
    Example:
        >>> registry = TypeRegistry()
        >>> registry.register("user", User)
        >>> registry.register("product", Product)
        >>> cls = registry.get("user")
        >>> instance = registry.create("user", name="John")
    """
    
    def __init__(self, name: str = "types"):
        """Initialize the type registry."""
        self._name = name
        self._types: Dict[str, Type[Any]] = {}
        self._names: Dict[Type[Any], str] = {}
        self._lock = threading.RLock()
    
    def register(
        self,
        name: str,
        cls: Type[Any],
        *,
        aliases: Optional[List[str]] = None
    ) -> None:
        """
        Register a type.
        
        Args:
            name: Type name
            cls: Type class
            aliases: Optional aliases for the type
        """
        with self._lock:
            self._types[name] = cls
            self._names[cls] = name
            
            if aliases:
                for alias in aliases:
                    self._types[alias] = cls
    
    def decorator(
        self,
        name: str,
        *,
        aliases: Optional[List[str]] = None
    ) -> Callable[[Type[T]], Type[T]]:
        """
        Decorator for registering a type.
        
        Args:
            name: Type name
            aliases: Optional aliases
            
        Returns:
            Decorator function
        """
        def decorator_func(cls: Type[T]) -> Type[T]:
            self.register(name, cls, aliases=aliases)
            return cls
        return decorator_func
    
    def unregister(self, name: str) -> Optional[Type[Any]]:
        """
        Unregister a type.
        
        Args:
            name: Type name
            
        Returns:
            The unregistered type or None
        """
        with self._lock:
            if name not in self._types:
                return None
            
            cls = self._types.pop(name)
            
            # Remove from names dict if this was the primary name
            if self._names.get(cls) == name:
                del self._names[cls]
            
            return cls
    
    def get(self, name: str) -> Type[Any]:
        """
        Get a type by name.
        
        Args:
            name: Type name
            
        Returns:
            The registered type
            
        Raises:
            NotRegisteredError: If type is not registered
        """
        with self._lock:
            if name not in self._types:
                raise NotRegisteredError(f"Type '{name}' is not registered")
            return self._types[name]
    
    def get_name(self, cls: Type[Any]) -> Optional[str]:
        """
        Get the name for a type.
        
        Args:
            cls: Type class
            
        Returns:
            Type name or None
        """
        with self._lock:
            return self._names.get(cls)
    
    def contains(self, name: str) -> bool:
        """Check if a type is registered."""
        with self._lock:
            return name in self._types
    
    def contains_type(self, cls: Type[Any]) -> bool:
        """Check if a type class is registered."""
        with self._lock:
            return cls in self._names
    
    def create(
        self,
        type_name: str,
        *args: Any,
        **kwargs: Any
    ) -> Any:
        """
        Create an instance of a registered type.
        
        Args:
            type_name: Type name
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            New instance
        """
        cls = self.get(type_name)
        return cls(*args, **kwargs)
    
    def get_all(self) -> Dict[str, Type[Any]]:
        """Get all registered types."""
        with self._lock:
            return dict(self._types)
    
    def get_names(self) -> List[str]:
        """Get all registered type names."""
        with self._lock:
            return list(self._types.keys())
    
    def clear(self) -> int:
        """Clear all registered types."""
        with self._lock:
            count = len(self._types)
            self._types.clear()
            self._names.clear()
            return count
    
    def __contains__(self, name: str) -> bool:
        return self.contains(name)
    
    def __getitem__(self, name: str) -> Type[Any]:
        return self.get(name)
    
    def __len__(self) -> int:
        return len(self._types)


# =============================================================================
# Convenience Functions
# =============================================================================

def create_registry(name: str = "default") -> BaseRegistry[Any]:
    """Create a new base registry."""
    return BaseRegistry[Any](name)


def create_service_registry(name: str = "services") -> ServiceRegistry[Any]:
    """Create a new service registry."""
    return ServiceRegistry[Any](name)


def create_plugin_registry(name: str = "plugins") -> PluginRegistry:
    """Create a new plugin registry."""
    return PluginRegistry(name)


def create_handler_registry(name: str = "handlers") -> HandlerRegistry[Any]:
    """Create a new handler registry."""
    return HandlerRegistry[Any](name)


def create_factory_registry(name: str = "factories") -> FactoryRegistry[Any]:
    """Create a new factory registry."""
    return FactoryRegistry[Any](name)


def create_type_registry(name: str = "types") -> TypeRegistry:
    """Create a new type registry."""
    return TypeRegistry(name)


# =============================================================================
# Global Registries (Convenience)
# =============================================================================

_global_registry: BaseRegistry[Any] = BaseRegistry("global")
_global_services: ServiceRegistry[Any] = ServiceRegistry("global_services")
_global_plugins: PluginRegistry = PluginRegistry("global_plugins")
_global_handlers: HandlerRegistry[Any] = HandlerRegistry("global_handlers")
_global_factories: FactoryRegistry[Any] = FactoryRegistry("global_factories")
_global_types: TypeRegistry = TypeRegistry("global_types")


def global_registry() -> BaseRegistry[Any]:
    """Get the global registry."""
    return _global_registry


def global_services() -> ServiceRegistry[Any]:
    """Get the global service registry."""
    return _global_services


def global_plugins() -> PluginRegistry:
    """Get the global plugin registry."""
    return _global_plugins


def global_handlers() -> HandlerRegistry[Any]:
    """Get the global handler registry."""
    return _global_handlers


def global_factories() -> FactoryRegistry[Any]:
    """Get the global factory registry."""
    return _global_factories


def global_types() -> TypeRegistry:
    """Get the global type registry."""
    return _global_types