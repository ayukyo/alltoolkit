#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Registry Pattern Utilities
========================================

A comprehensive implementation of the Registry Pattern for flexible
registration, lookup, and management of objects, services, handlers,
factories, and types.

Quick Start:
    >>> from registry_utils import BaseRegistry, ServiceRegistry
    >>> 
    >>> # Basic registry
    >>> registry = BaseRegistry[str]()
    >>> registry.register("greeting", "Hello, World!")
    >>> print(registry.get("greeting"))
    Hello, World!
    >>> 
    >>> # Service registry with lazy initialization
    >>> services = ServiceRegistry[Database]()
    >>> services.register_factory("db", lambda: Database("localhost"))
    >>> db = services.get("db")  # Created on first access
    >>> 
    >>> # Plugin registry
    >>> plugins = PluginRegistry()
    >>> plugins.register("auth", AuthPlugin(), dependencies=["core"])
    >>> plugins.register("core", CorePlugin())
    >>> plugins.enable("auth")  # Dependencies checked automatically
    >>> 
    >>> # Handler registry
    >>> handlers = HandlerRegistry[Callable]()
    >>> @handlers.decorator("user.created")
    >>> def on_user_created(event):
    >>>     print(f"User created: {event}")
    >>> 
    >>> # Factory registry
    >>> factories = FactoryRegistry[Widget]()
    >>> factories.register("button", ButtonWidget)
    >>> button = factories.create("button", text="Click Me")
    >>> 
    >>> # Type registry
    >>> types = TypeRegistry()
    >>> types.register("user", User, aliases=["person"])
    >>> cls = types.get("user")

Features:
    - Generic registry with type-safe operations
    - Service registry with lazy initialization
    - Plugin registry with dependency management
    - Handler registry for event/command handling
    - Factory registry with singleton support
    - Type registry for dynamic type lookup
    - Namespace support for organization
    - Priority-based ordering
    - Thread-safe operations
    - Decorator-based registration
    - Zero external dependencies

Author: AllToolkit Contributors
License: MIT
"""

from .mod import (
    # Core classes
    BaseRegistry,
    ServiceRegistry,
    PluginRegistry,
    HandlerRegistry,
    FactoryRegistry,
    TypeRegistry,
    
    # Data classes
    RegistryItem,
    PluginInfo,
    
    # Enums
    Priority,
    
    # Exceptions
    RegistryError,
    AlreadyRegisteredError,
    NotRegisteredError,
    RegistrationConflictError,
    
    # Convenience functions
    create_registry,
    create_service_registry,
    create_plugin_registry,
    create_handler_registry,
    create_factory_registry,
    create_type_registry,
    
    # Global registries
    global_registry,
    global_services,
    global_plugins,
    global_handlers,
    global_factories,
    global_types,
)

__all__ = [
    # Core classes
    'BaseRegistry',
    'ServiceRegistry',
    'PluginRegistry',
    'HandlerRegistry',
    'FactoryRegistry',
    'TypeRegistry',
    
    # Data classes
    'RegistryItem',
    'PluginInfo',
    
    # Enums
    'Priority',
    
    # Exceptions
    'RegistryError',
    'AlreadyRegisteredError',
    'NotRegisteredError',
    'RegistrationConflictError',
    
    # Convenience functions
    'create_registry',
    'create_service_registry',
    'create_plugin_registry',
    'create_handler_registry',
    'create_factory_registry',
    'create_type_registry',
    
    # Global registries
    'global_registry',
    'global_services',
    'global_plugins',
    'global_handlers',
    'global_factories',
    'global_types',
]

__version__ = '1.0.0'