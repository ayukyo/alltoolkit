#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Registry Pattern Utilities Examples
================================================

This file demonstrates various use cases for the registry pattern utilities.

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from registry_utils import (
    BaseRegistry,
    ServiceRegistry,
    PluginRegistry,
    HandlerRegistry,
    FactoryRegistry,
    TypeRegistry,
    Priority,
    create_registry,
    global_registry,
    global_services,
    global_plugins,
    global_handlers,
    global_factories,
    global_types,
)


# =============================================================================
# Example 1: Basic Registry Usage
# =============================================================================

def example_basic_registry():
    """Demonstrate basic registry operations."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Registry")
    print("=" * 60)
    
    # Create a registry for string values
    registry = BaseRegistry[str](name="config")
    
    # Register items
    registry.register("api_url", "https://api.example.com")
    registry.register("timeout", "30")
    registry.register("debug", "true", namespace="settings")
    
    # Retrieve items
    print(f"api_url: {registry.get('api_url')}")
    print(f"timeout: {registry.get('timeout')}")
    print(f"debug: {registry.get('debug', 'settings')}")
    
    # Check if item exists
    print(f"\nContains 'api_url': {registry.contains('api_url')}")
    print(f"'api_url' in registry: {'api_url' in registry}")
    
    # Get all items
    print(f"\nAll items: {registry.get_all()}")
    
    # List names
    print(f"Registered names: {registry.get_names()}")
    
    # Unregister
    registry.unregister("timeout")
    print(f"\nAfter unregistering 'timeout', count: {registry.count}")


# =============================================================================
# Example 2: Registry with Tags and Metadata
# =============================================================================

def example_tags_and_metadata():
    """Demonstrate tags and metadata usage."""
    print("\n" + "=" * 60)
    print("Example 2: Tags and Metadata")
    print("=" * 60)
    
    registry = BaseRegistry[str]()
    
    # Register with tags
    registry.register(
        "mysql", "MySQL Database",
        tags={"database", "sql", "production"}
    )
    registry.register(
        "redis", "Redis Cache",
        tags={"cache", "production"}
    )
    registry.register(
        "mongodb", "MongoDB",
        tags={"database", "nosql", "development"}
    )
    
    # Query by tag
    print("Items with 'database' tag:")
    for name, item in registry.get_by_tag("database").items():
        print(f"  - {name}: {item}")
    
    print("\nItems with 'production' tag:")
    for name, item in registry.get_by_tag("production").items():
        print(f"  - {name}: {item}")
    
    # Register with metadata
    registry.register(
        "api_key", "sk-12345",
        metadata={
            "created_by": "admin",
            "created_at": "2024-01-15",
            "expires_at": "2024-12-31",
            "environment": "production"
        }
    )
    
    # Access metadata
    metadata = registry.get_metadata("api_key")
    print(f"\napi_key metadata:")
    for key, value in metadata.items():
        print(f"  - {key}: {value}")
    
    # Update metadata
    registry.set_metadata("api_key", "environment", "staging")
    print(f"\nUpdated environment: {registry.get_metadata('api_key')['environment']}")


# =============================================================================
# Example 3: Decorator-based Registration
# =============================================================================

def example_decorator_registration():
    """Demonstrate decorator-based registration."""
    print("\n" + "=" * 60)
    print("Example 3: Decorator-based Registration")
    print("=" * 60)
    
    registry = BaseRegistry[callable]()
    
    # Register functions using decorator
    @registry.decorator("process_data")
    def process_data(data):
        return f"Processed: {data}"
    
    @registry.decorator("validate_input")
    def validate_input(data):
        return f"Validated: {data}"
    
    @registry.decorator(
        "log_event",
        priority=Priority.HIGH.value,
        tags={"logging", "monitoring"}
    )
    def log_event(event):
        return f"Logged: {event}"
    
    # Use registered functions
    print(f"process_data result: {registry['process_data']('test data')}")
    print(f"validate_input result: {registry['validate_input']('test input')}")
    print(f"log_event result: {registry['log_event']('test event')}")
    
    # List registered functions
    print(f"\nRegistered functions: {registry.get_names()}")
    
    # Check tags
    print(f"Functions with 'logging' tag: {registry.get_by_tag('logging')}")


# =============================================================================
# Example 4: Service Registry with Lazy Initialization
# =============================================================================

def example_service_registry():
    """Demonstrate service registry with lazy initialization."""
    print("\n" + "=" * 60)
    print("Example 4: Service Registry")
    print("=" * 60)
    
    # Mock database service
    class Database:
        def __init__(self, host, port=5432):
            self.host = host
            self.port = port
            self.connected = False
            print(f"  [Database created: {host}:{port}]")
        
        def connect(self):
            self.connected = True
            print(f"  [Connected to {self.host}]")
        
        def dispose(self):
            self.connected = False
            print(f"  [Disconnected from {self.host}]")
    
    # Mock cache service
    class Cache:
        def __init__(self, host):
            self.host = host
            print(f"  [Cache created: {host}]")
    
    registry = ServiceRegistry()
    
    # Register instance directly
    cache = Cache("redis.example.com")
    registry.register("cache", cache)
    
    # Register factory for lazy initialization
    registry.register_factory(
        "database",
        lambda: Database("db.example.com"),
        singleton=True
    )
    
    print("Getting cache (already created):")
    c = registry.get("cache")
    print(f"Cache host: {c.host}")
    
    print("\nGetting database (created on demand):")
    db1 = registry.get("database")
    db1.connect()
    
    print("\nGetting database again (singleton, no new creation):")
    db2 = registry.get("database")
    print(f"Same instance: {db1 is db2}")
    
    # List services
    print(f"\nRegistered services: {registry.get_names()}")
    
    # Unregister with disposal
    print("\nUnregistering database (dispose called):")
    registry.unregister("database", dispose=True)


# =============================================================================
# Example 5: Plugin Registry with Dependencies
# =============================================================================

def example_plugin_registry():
    """Demonstrate plugin registry with dependency management."""
    print("\n" + "=" * 60)
    print("Example 5: Plugin Registry")
    print("=" * 60)
    
    class CorePlugin:
        def __init__(self):
            self.name = "Core"
        
        def activate(self):
            print(f"  [{self.name} activated]")
        
        def deactivate(self):
            print(f"  [{self.name} deactivated]")
    
    class AuthPlugin:
        def __init__(self):
            self.name = "Auth"
        
        def activate(self):
            print(f"  [{self.name} activated]")
        
        def deactivate(self):
            print(f"  [{self.name} deactivated]")
    
    class LoggingPlugin:
        def __init__(self):
            self.name = "Logging"
        
        def activate(self):
            print(f"  [{self.name} activated]")
        
        def deactivate(self):
            print(f"  [{self.name} deactivated]")
    
    registry = PluginRegistry()
    
    # Register plugins with dependencies
    registry.register(
        "core", CorePlugin(),
        version="1.0.0",
        description="Core functionality"
    )
    
    registry.register(
        "auth", AuthPlugin(),
        version="2.0.0",
        description="Authentication",
        dependencies=["core"]
    )
    
    registry.register(
        "logging", LoggingPlugin(),
        version="1.5.0",
        description="Logging service",
        dependencies=["core"]
    )
    
    # Check registration
    print("Registered plugins:")
    for name in registry.get_names():
        info = registry.get_info(name)
        print(f"  - {name}: v{info.version} - {info.description}")
    
    # Check dependencies
    print("\nChecking dependencies for 'auth':")
    satisfied, missing = registry.check_dependencies("auth")
    print(f"  Satisfied: {satisfied}, Missing: {missing}")
    
    # Disable a plugin
    print("\nDisabling 'auth':")
    registry.disable("auth")
    print(f"  auth enabled: {registry.is_enabled('auth')}")
    
    # Enable a plugin (will call activate)
    print("\nEnabling 'auth':")
    registry.enable("auth")
    print(f"  auth enabled: {registry.is_enabled('auth')}")
    
    # Try to disable a plugin that has dependents
    print("\nTrying to disable 'core' (auth depends on it):")
    try:
        registry.disable("core")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Get enabled plugins
    print("\nEnabled plugins:")
    for name in registry.get_enabled():
        print(f"  - {name}")


# =============================================================================
# Example 6: Handler Registry
# =============================================================================

def example_handler_registry():
    """Demonstrate handler registry for event handling."""
    print("\n" + "=" * 60)
    print("Example 6: Handler Registry")
    print("=" * 60)
    
    registry = HandlerRegistry[callable]()
    
    # Register handlers with different priorities
    @registry.decorator("user.created", priority=Priority.HIGH.value)
    def send_welcome_email(event):
        print(f"  [HIGH] Sending welcome email to {event['email']}")
        return "email_sent"
    
    @registry.decorator("user.created")
    def log_user_creation(event):
        print(f"  [NORMAL] Logging user creation: {event['name']}")
        return "logged"
    
    @registry.decorator("user.created", priority=Priority.LOW.value)
    def update_statistics(event):
        print(f"  [LOW] Updating statistics")
        return "stats_updated"
    
    # Register handlers for another event
    @registry.decorator("user.deleted")
    def cleanup_user_data(event):
        print(f"  Cleaning up data for {event['user_id']}")
    
    # Show registered events
    print("Registered event types:")
    for event_type, handlers in registry.get_all_handlers().items():
        print(f"  - {event_type}: {len(handlers)} handlers")
    
    # Simulate event dispatch
    print("\nDispatching 'user.created' event:")
    event = {"name": "John Doe", "email": "john@example.com"}
    handlers = registry.get_handlers("user.created")
    results = []
    for handler in handlers:
        results.append(handler(event))
    
    print(f"\nHandler results: {results}")


# =============================================================================
# Example 7: Factory Registry
# =============================================================================

def example_factory_registry():
    """Demonstrate factory registry for object creation."""
    print("\n" + "=" * 60)
    print("Example 7: Factory Registry")
    print("=" * 60)
    
    class Button:
        def __init__(self, text="", color="blue"):
            self.text = text
            self.color = color
        
        def __repr__(self):
            return f"Button(text='{self.text}', color='{self.color}')"
    
    class Text:
        def __init__(self, content="", size=12):
            self.content = content
            self.size = size
        
        def __repr__(self):
            return f"Text(content='{self.content}', size={self.size})"
    
    class Image:
        def __init__(self, url=""):
            self.url = url
        
        def __repr__(self):
            return f"Image(url='{self.url}')"
    
    registry = FactoryRegistry()
    
    # Register factories
    registry.register("button", Button)
    registry.register("text", Text)
    registry.register("image", Image, singleton=False)
    
    # Create instances
    print("Creating widgets:")
    
    btn1 = registry.create("button", text="Submit", color="green")
    print(f"  button 1: {btn1}")
    
    btn2 = registry.create("button", text="Cancel", color="red")
    print(f"  button 2: {btn2}")
    
    txt = registry.create("text", content="Hello World", size=14)
    print(f"  text: {txt}")
    
    img1 = registry.create("image", url="photo1.jpg")
    img2 = registry.create("image", url="photo2.jpg")
    print(f"  image 1: {img1}")
    print(f"  image 2: {img2}")
    
    # List registered factories
    print(f"\nRegistered factories: {registry.get_names()}")


# =============================================================================
# Example 8: Type Registry
# =============================================================================

def example_type_registry():
    """Demonstrate type registry for dynamic type lookup."""
    print("\n" + "=" * 60)
    print("Example 8: Type Registry")
    print("=" * 60)
    
    class User:
        def __init__(self, name, email):
            self.name = name
            self.email = email
        
        def __repr__(self):
            return f"User(name='{self.name}', email='{self.email}')"
    
    class Product:
        def __init__(self, name, price):
            self.name = name
            self.price = price
        
        def __repr__(self):
            return f"Product(name='{self.name}', price={self.price})"
    
    class Order:
        def __init__(self, user, product):
            self.user = user
            self.product = product
        
        def __repr__(self):
            return f"Order(user={self.user.name}, product={self.product.name})"
    
    registry = TypeRegistry()
    
    # Register types with aliases
    registry.register("user", User, aliases=["person", "customer"])
    registry.register("product", Product, aliases=["item"])
    registry.register("order", Order)
    
    # Lookup types
    print("Type lookup:")
    print(f"  'user': {registry.get('user')}")
    print(f"  'person' (alias): {registry.get('person')}")
    print(f"  'item' (alias): {registry.get('item')}")
    
    # Get name for type
    print(f"\nName for User type: {registry.get_name(User)}")
    
    # Create instances dynamically
    print("\nCreating instances from type names:")
    
    user = registry.create("user", name="John", email="john@example.com")
    print(f"  user: {user}")
    
    product = registry.create("product", name="Widget", price=99.99)
    print(f"  product: {product}")
    
    order = registry.create("order", user=user, product=product)
    print(f"  order: {order}")


# =============================================================================
# Example 9: Global Registries
# =============================================================================

def example_global_registries():
    """Demonstrate global registry usage."""
    print("\n" + "=" * 60)
    print("Example 9: Global Registries")
    print("=" * 60)
    
    # Access global registries
    registry = global_registry()
    services = global_services()
    plugins = global_plugins()
    handlers = global_handlers()
    factories = global_factories()
    types = global_types()
    
    # Use global registry for app-wide configuration
    registry.register("app_name", "AllToolkit Demo")
    registry.register("version", "1.0.0")
    
    print(f"App: {registry['app_name']}")
    print(f"Version: {registry['version']}")


# =============================================================================
# Run All Examples
# =============================================================================

def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Registry Pattern Utilities - Examples")
    print("=" * 60)
    
    example_basic_registry()
    example_tags_and_metadata()
    example_decorator_registration()
    example_service_registry()
    example_plugin_registry()
    example_handler_registry()
    example_factory_registry()
    example_type_registry()
    example_global_registries()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()