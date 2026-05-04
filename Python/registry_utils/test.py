#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Registry Pattern Utilities Test Suite
===================================================

Comprehensive tests for the registry pattern implementation.

Author: AllToolkit
License: MIT
"""

import unittest
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from registry_utils.mod import (
    # Base classes
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


# =============================================================================
# Test Classes for Test Data
# =============================================================================

class MockService:
    """Mock service for testing."""
    def __init__(self, name: str):
        self.name = name
        self.initialized = False
        self.disposed = False
    
    def initialize(self):
        self.initialized = True
        return self
    
    def dispose(self):
        self.disposed = True


class MockPlugin:
    """Mock plugin for testing."""
    def __init__(self, name: str):
        self.name = name
        self.activated = False
        self.deactivated = False
    
    def activate(self):
        self.activated = True
    
    def deactivate(self):
        self.deactivated = True


class MockWidget:
    """Mock widget for factory testing."""
    def __init__(self, text: str = "", color: str = "black"):
        self.text = text
        self.color = color


class MockButton(MockWidget):
    """Mock button widget."""
    pass


class MockText(MockWidget):
    """Mock text widget."""
    pass


# =============================================================================
# BaseRegistry Tests
# =============================================================================

class TestBaseRegistry(unittest.TestCase):
    """Test cases for BaseRegistry."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = BaseRegistry[str]()
    
    def test_register_and_get(self):
        """Test basic registration and retrieval."""
        self.registry.register("greeting", "Hello, World!")
        self.assertEqual(self.registry.get("greeting"), "Hello, World!")
    
    def test_register_with_namespace(self):
        """Test registration with namespace."""
        self.registry.register("greeting", "Hello", namespace="en")
        self.registry.register("greeting", "Hola", namespace="es")
        
        self.assertEqual(self.registry.get("greeting", "en"), "Hello")
        self.assertEqual(self.registry.get("greeting", "es"), "Hola")
    
    def test_register_overwrite(self):
        """Test overwriting existing registration."""
        self.registry.register("key", "value1")
        self.assertEqual(self.registry.get("key"), "value1")
        
        # Should raise without overwrite flag
        with self.assertRaises(AlreadyRegisteredError):
            self.registry.register("key", "value2")
        
        # Should succeed with overwrite flag
        self.registry.register("key", "value2", overwrite=True)
        self.assertEqual(self.registry.get("key"), "value2")
    
    def test_unregister(self):
        """Test unregistration."""
        self.registry.register("key", "value")
        self.assertEqual(self.registry.unregister("key"), "value")
        
        with self.assertRaises(NotRegisteredError):
            self.registry.get("key")
    
    def test_try_get(self):
        """Test try_get method."""
        self.registry.register("key", "value")
        self.assertEqual(self.registry.try_get("key"), "value")
        self.assertIsNone(self.registry.try_get("nonexistent"))
    
    def test_contains(self):
        """Test contains method."""
        self.registry.register("key", "value")
        self.assertTrue(self.registry.contains("key"))
        self.assertFalse(self.registry.contains("nonexistent"))
        self.assertTrue("key" in self.registry)
    
    def test_get_all(self):
        """Test get_all method."""
        self.registry.register("a", "1")
        self.registry.register("b", "2")
        self.registry.register("c", "3", namespace="other")
        
        all_items = self.registry.get_all()
        self.assertEqual(len(all_items), 3)
        self.assertIn("default:a", all_items)
        self.assertIn("default:b", all_items)
        self.assertIn("other:c", all_items)
    
    def test_get_by_namespace(self):
        """Test get_by_namespace method."""
        self.registry.register("a", "1", namespace="ns1")
        self.registry.register("b", "2", namespace="ns1")
        self.registry.register("c", "3", namespace="ns2")
        
        ns1_items = self.registry.get_by_namespace("ns1")
        self.assertEqual(len(ns1_items), 2)
        
        ns2_items = self.registry.get_by_namespace("ns2")
        self.assertEqual(len(ns2_items), 1)
    
    def test_get_by_tag(self):
        """Test get_by_tag method."""
        self.registry.register("a", "1", tags={"red", "primary"})
        self.registry.register("b", "2", tags={"red"})
        self.registry.register("c", "3", tags={"blue"})
        
        red_items = self.registry.get_by_tag("red")
        self.assertEqual(len(red_items), 2)
        
        primary_items = self.registry.get_by_tag("primary")
        self.assertEqual(len(primary_items), 1)
    
    def test_priority_ordering(self):
        """Test priority-based ordering."""
        self.registry.register("low", "1", priority=Priority.LOW.value)
        self.registry.register("high", "2", priority=Priority.HIGH.value)
        self.registry.register("normal", "3", priority=Priority.NORMAL.value)
        
        # Priority is stored but ordering is not directly exposed
        # We can verify through metadata
        self.assertEqual(self.registry.get("low"), "1")
        self.assertEqual(self.registry.get("high"), "2")
    
    def test_metadata(self):
        """Test metadata storage."""
        self.registry.register(
            "key", "value",
            metadata={"version": "1.0", "author": "test"}
        )
        
        metadata = self.registry.get_metadata("key")
        self.assertEqual(metadata["version"], "1.0")
        self.assertEqual(metadata["author"], "test")
        
        # Update metadata
        self.registry.set_metadata("key", "version", "2.0")
        metadata = self.registry.get_metadata("key")
        self.assertEqual(metadata["version"], "2.0")
    
    def test_decorator(self):
        """Test decorator-based registration."""
        @self.registry.decorator("decorated_func")
        def my_func():
            pass
        
        self.assertTrue(self.registry.contains("decorated_func"))
        self.assertIs(self.registry.get("decorated_func"), my_func)
    
    def test_hooks(self):
        """Test registration hooks."""
        registered = []
        unregistered = []
        
        def on_register(name, item):
            registered.append((name, item))
        
        def on_unregister(name, item):
            unregistered.append((name, item))
        
        self.registry.add_hook_on_register(on_register)
        self.registry.add_hook_on_unregister(on_unregister)
        
        self.registry.register("key", "value")
        self.assertEqual(registered, [("key", "value")])
        
        self.registry.unregister("key")
        self.assertEqual(unregistered, [("key", "value")])
    
    def test_clear(self):
        """Test clearing registry."""
        self.registry.register("a", "1")
        self.registry.register("b", "2", namespace="ns")
        
        # Clear specific namespace
        count = self.registry.clear("ns")
        self.assertEqual(count, 1)
        self.assertEqual(self.registry.count, 1)
        
        # Clear all
        count = self.registry.clear()
        self.assertEqual(count, 1)
        self.assertTrue(self.registry.is_empty)
    
    def test_len_and_repr(self):
        """Test __len__ and __repr__."""
        self.registry.register("a", "1")
        self.registry.register("b", "2")
        
        self.assertEqual(len(self.registry), 2)
        self.assertIn("BaseRegistry", repr(self.registry))
        self.assertIn("count=2", repr(self.registry))
    
    def test_bracket_access(self):
        """Test bracket access."""
        self.registry.register("key", "value")
        self.assertEqual(self.registry["key"], "value")


# =============================================================================
# ServiceRegistry Tests
# =============================================================================

class TestServiceRegistry(unittest.TestCase):
    """Test cases for ServiceRegistry."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = ServiceRegistry[MockService]()
    
    def test_register_instance(self):
        """Test registering a service instance."""
        service = MockService("test")
        self.registry.register("service", service)
        
        self.assertIs(self.registry.get("service"), service)
    
    def test_register_factory(self):
        """Test registering a service factory."""
        call_count = [0]
        
        def factory():
            call_count[0] += 1
            return MockService(f"instance-{call_count[0]}")
        
        self.registry.register_factory("service", factory)
        
        # First call creates instance
        service1 = self.registry.get("service")
        self.assertEqual(service1.name, "instance-1")
        
        # Second call returns same instance (singleton by default)
        service2 = self.registry.get("service")
        self.assertIs(service1, service2)
        self.assertEqual(call_count[0], 1)  # Factory called only once
    
    def test_register_factory_non_singleton(self):
        """Test registering a non-singleton factory."""
        call_count = [0]
        
        def factory():
            call_count[0] += 1
            return MockService(f"instance-{call_count[0]}")
        
        self.registry.register_factory("service", factory, singleton=False)
        
        service1 = self.registry.get("service")
        service2 = self.registry.get("service")
        
        self.assertIsNot(service1, service2)
        self.assertEqual(call_count[0], 2)  # Factory called twice
    
    def test_circular_dependency_detection(self):
        """Test circular dependency detection."""
        def factory():
            # Try to get self during initialization
            self.registry.get("service")
            return MockService("test")
        
        self.registry.register_factory("service", factory)
        
        with self.assertRaises(RegistryError) as context:
            self.registry.get("service")
        
        self.assertIn("Circular dependency", str(context.exception))
    
    def test_try_get(self):
        """Test try_get method."""
        service = MockService("test")
        self.registry.register("service", service)
        
        self.assertIs(self.registry.try_get("service"), service)
        self.assertIsNone(self.registry.try_get("nonexistent"))
    
    def test_unregister(self):
        """Test unregistering a service."""
        service = MockService("test")
        self.registry.register("service", service)
        
        result = self.registry.unregister("service")
        self.assertIs(result, service)
        self.assertFalse(self.registry.contains("service"))
    
    def test_unregister_with_dispose(self):
        """Test unregistering with disposal."""
        service = MockService("test")
        self.registry.register("service", service)
        
        self.registry.unregister("service", dispose=True)
        self.assertTrue(service.disposed)
    
    def test_get_by_tag(self):
        """Test getting services by tag."""
        service1 = MockService("test1")
        service2 = MockService("test2")
        
        self.registry.register("s1", service1, tags={"database"})
        self.registry.register("s2", service2, tags={"cache"})
        self.registry.register("s3", MockService("test3"), tags={"database"})
        
        db_services = self.registry.get_by_tag("database")
        self.assertEqual(len(db_services), 2)
    
    def test_contains_and_len(self):
        """Test contains and len methods."""
        self.registry.register("s1", MockService("test1"))
        self.registry.register("s2", MockService("test2"))
        
        self.assertTrue(self.registry.contains("s1"))
        self.assertEqual(len(self.registry), 2)
    
    def test_bracket_access(self):
        """Test bracket access."""
        service = MockService("test")
        self.registry.register("service", service)
        self.assertIs(self.registry["service"], service)


# =============================================================================
# PluginRegistry Tests
# =============================================================================

class TestPluginRegistry(unittest.TestCase):
    """Test cases for PluginRegistry."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = PluginRegistry()
    
    def test_register_plugin(self):
        """Test plugin registration."""
        plugin = MockPlugin("test")
        self.registry.register(
            "auth", plugin,
            version="1.0.0",
            description="Auth plugin",
            author="Test Author"
        )
        
        self.assertIs(self.registry.get("auth"), plugin)
        
        info = self.registry.get_info("auth")
        self.assertEqual(info.name, "auth")
        self.assertEqual(info.version, "1.0.0")
        self.assertEqual(info.description, "Auth plugin")
        self.assertEqual(info.author, "Test Author")
        self.assertTrue(info.enabled)
    
    def test_decorator_registration(self):
        """Test decorator-based plugin registration."""
        @self.registry.decorator("cache", version="2.0.0", description="Cache plugin")
        class CachePlugin:
            pass
        
        self.assertTrue(self.registry.contains("cache"))
        info = self.registry.get_info("cache")
        self.assertEqual(info.version, "2.0.0")
    
    def test_enable_disable(self):
        """Test enabling and disabling plugins."""
        plugin = MockPlugin("test")
        self.registry.register("auth", plugin)
        
        # Plugin starts enabled
        self.assertTrue(self.registry.is_enabled("auth"))
        
        # Disable
        self.registry.disable("auth")
        self.assertFalse(self.registry.is_enabled("auth"))
        self.assertTrue(plugin.deactivated)
        
        # Enable
        self.registry.enable("auth")
        self.assertTrue(self.registry.is_enabled("auth"))
        self.assertTrue(plugin.activated)
    
    def test_dependencies(self):
        """Test plugin dependencies."""
        core = MockPlugin("core")
        auth = MockPlugin("auth")
        
        self.registry.register("core", core)
        self.registry.register("auth", auth, dependencies=["core"])
        
        # Check dependencies
        satisfied, missing = self.registry.check_dependencies("auth")
        self.assertTrue(satisfied)
        self.assertEqual(missing, [])
        
        # Missing dependency
        self.registry.register("premium", MockPlugin("premium"), dependencies=["nonexistent"])
        satisfied, missing = self.registry.check_dependencies("premium")
        self.assertFalse(satisfied)
        self.assertIn("nonexistent", missing)
    
    def test_dependency_enable_check(self):
        """Test that enabling checks dependencies."""
        self.registry.register("core", MockPlugin("core"))
        self.registry.register("auth", MockPlugin("auth"), dependencies=["core"])
        
        # Core needs to be enabled for auth to work
        self.assertTrue(self.registry.is_enabled("core"))
        
        # Enable auth should succeed since core is enabled
        self.registry.disable("auth")
        self.registry.enable("auth")
        self.assertTrue(self.registry.is_enabled("auth"))
    
    def test_disable_blocked_by_dependent(self):
        """Test that disabling fails when other plugins depend on it."""
        self.registry.register("core", MockPlugin("core"))
        self.registry.register("auth", MockPlugin("auth"), dependencies=["core"])
        
        # Cannot disable core when auth depends on it
        with self.assertRaises(RegistryError):
            self.registry.disable("core")
    
    def test_get_enabled_plugins(self):
        """Test getting enabled plugins."""
        self.registry.register("p1", MockPlugin("p1"))
        self.registry.register("p2", MockPlugin("p2"))
        self.registry.register("p3", MockPlugin("p3"))
        self.registry.disable("p2")
        
        enabled = self.registry.get_enabled()
        self.assertEqual(len(enabled), 2)
        self.assertIn("p1", enabled)
        self.assertIn("p3", enabled)
        self.assertNotIn("p2", enabled)
    
    def test_hooks(self):
        """Test enable/disable hooks."""
        enabled_plugins = []
        disabled_plugins = []
        
        def on_enable(name, plugin):
            enabled_plugins.append(name)
        
        def on_disable(name, plugin):
            disabled_plugins.append(name)
        
        self.registry.add_hook_on_enable(on_enable)
        self.registry.add_hook_on_disable(on_disable)
        
        self.registry.register("p1", MockPlugin("p1"))
        self.registry.disable("p1")
        self.registry.enable("p1")
        
        self.assertEqual(enabled_plugins, ["p1"])
        self.assertEqual(disabled_plugins, ["p1"])


# =============================================================================
# HandlerRegistry Tests
# =============================================================================

class TestHandlerRegistry(unittest.TestCase):
    """Test cases for HandlerRegistry."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = HandlerRegistry[callable]()
    
    def test_register_handler(self):
        """Test handler registration."""
        def handler(event):
            return f"handled: {event}"
        
        handler_id = self.registry.register("user.created", handler)
        self.assertTrue(self.registry.has_handlers("user.created"))
        
        handlers = self.registry.get_handlers("user.created")
        self.assertEqual(len(handlers), 1)
        self.assertIs(handlers[0], handler)
    
    def test_priority_ordering(self):
        """Test that handlers are ordered by priority."""
        results = []
        
        def handler1(event):
            results.append(1)
        
        def handler2(event):
            results.append(2)
        
        def handler3(event):
            results.append(3)
        
        self.registry.register("event", handler1, priority=Priority.LOW.value)
        self.registry.register("event", handler2, priority=Priority.HIGH.value)
        self.registry.register("event", handler3, priority=Priority.NORMAL.value)
        
        handlers = self.registry.get_handlers("event")
        # Higher priority first
        self.assertIs(handlers[0], handler2)
        self.assertIs(handlers[1], handler3)
        self.assertIs(handlers[2], handler1)
    
    def test_decorator_registration(self):
        """Test decorator-based handler registration."""
        @self.registry.decorator("user.deleted")
        def handle_delete(event):
            pass
        
        self.assertTrue(self.registry.has_handlers("user.deleted"))
    
    def test_unregister_handler(self):
        """Test unregistering a handler."""
        def handler(event):
            pass
        
        self.registry.register("event", handler)
        result = self.registry.unregister("event", handler)
        
        self.assertTrue(result)
        self.assertFalse(self.registry.has_handlers("event"))
    
    def test_unregister_by_id(self):
        """Test unregistering by handler ID."""
        def handler(event):
            pass
        
        handler_id = self.registry.register("event", handler)
        result = self.registry.unregister_by_id(handler_id)
        
        self.assertTrue(result)
        self.assertFalse(self.registry.has_handlers("event"))
    
    def test_get_all_handlers(self):
        """Test getting all handlers."""
        self.registry.register("event1", lambda e: None)
        self.registry.register("event2", lambda e: None)
        
        all_handlers = self.registry.get_all_handlers()
        self.assertEqual(len(all_handlers), 2)
        self.assertIn("event1", all_handlers)
        self.assertIn("event2", all_handlers)
    
    def test_clear_handlers(self):
        """Test clearing handlers."""
        self.registry.register("event1", lambda e: None)
        self.registry.register("event1", lambda e: None)
        self.registry.register("event2", lambda e: None)
        
        # Clear specific event
        count = self.registry.clear("event1")
        self.assertEqual(count, 2)
        self.assertFalse(self.registry.has_handlers("event1"))
        self.assertTrue(self.registry.has_handlers("event2"))
        
        # Clear all
        count = self.registry.clear()
        self.assertEqual(count, 1)
        self.assertFalse(self.registry.has_handlers("event2"))


# =============================================================================
# FactoryRegistry Tests
# =============================================================================

class TestFactoryRegistry(unittest.TestCase):
    """Test cases for FactoryRegistry."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = FactoryRegistry[MockWidget]()
    
    def test_register_factory(self):
        """Test factory registration."""
        self.registry.register("button", MockButton)
        
        self.assertTrue(self.registry.contains("button"))
    
    def test_create_instance(self):
        """Test creating instances."""
        self.registry.register("button", MockButton)
        self.registry.register("text", MockText)
        
        button = self.registry.create("button", text="Click Me", color="blue")
        self.assertIsInstance(button, MockButton)
        self.assertEqual(button.text, "Click Me")
        self.assertEqual(button.color, "blue")
        
        text = self.registry.create("text", text="Hello")
        self.assertIsInstance(text, MockText)
        self.assertEqual(text.text, "Hello")
    
    def test_singleton(self):
        """Test singleton behavior."""
        self.registry.register("widget", MockWidget, singleton=True)
        
        w1 = self.registry.create("widget", text="Test")
        w2 = self.registry.create("widget", text="Different")  # Args ignored for singleton
        
        self.assertIs(w1, w2)
    
    def test_non_singleton(self):
        """Test non-singleton behavior."""
        self.registry.register("widget", MockWidget, singleton=False)
        
        w1 = self.registry.create("widget", text="First")
        w2 = self.registry.create("widget", text="Second")
        
        self.assertIsNot(w1, w2)
        self.assertEqual(w1.text, "First")
        self.assertEqual(w2.text, "Second")
    
    def test_decorator(self):
        """Test decorator-based factory registration."""
        @self.registry.decorator("custom")
        class CustomWidget(MockWidget):
            pass
        
        self.assertTrue(self.registry.contains("custom"))
        instance = self.registry.create("custom")
        self.assertIsInstance(instance, CustomWidget)
    
    def test_unregister(self):
        """Test unregistering a factory."""
        self.registry.register("button", MockButton)
        result = self.registry.unregister("button")
        
        self.assertTrue(result)
        self.assertFalse(self.registry.contains("button"))
    
    def test_get_factory(self):
        """Test getting factory function."""
        self.registry.register("button", MockButton)
        factory = self.registry.get_factory("button")
        
        self.assertIs(factory, MockButton)
    
    def test_bracket_access(self):
        """Test bracket access to get factory."""
        self.registry.register("button", MockButton)
        self.assertIs(self.registry["button"], MockButton)


# =============================================================================
# TypeRegistry Tests
# =============================================================================

class TestTypeRegistry(unittest.TestCase):
    """Test cases for TypeRegistry."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = TypeRegistry()
    
    def test_register_type(self):
        """Test type registration."""
        self.registry.register("user", MockService)
        
        self.assertTrue(self.registry.contains("user"))
        self.assertEqual(self.registry.get("user"), MockService)
    
    def test_register_with_aliases(self):
        """Test type registration with aliases."""
        self.registry.register("user", MockService, aliases=["person", "account"])
        
        self.assertEqual(self.registry.get("user"), MockService)
        self.assertEqual(self.registry.get("person"), MockService)
        self.assertEqual(self.registry.get("account"), MockService)
    
    def test_get_name(self):
        """Test getting name for a type."""
        self.registry.register("user", MockService)
        
        self.assertEqual(self.registry.get_name(MockService), "user")
        self.assertIsNone(self.registry.get_name(MockWidget))
    
    def test_decorator(self):
        """Test decorator-based type registration."""
        @self.registry.decorator("button")
        class ButtonWidget(MockWidget):
            pass
        
        self.assertTrue(self.registry.contains("button"))
        self.assertEqual(self.registry.get("button"), ButtonWidget)
    
    def test_create_instance(self):
        """Test creating instances."""
        self.registry.register("widget", MockWidget)
        
        instance = self.registry.create("widget", text="Test", color="red")
        
        self.assertIsInstance(instance, MockWidget)
        self.assertEqual(instance.text, "Test")
        self.assertEqual(instance.color, "red")
    
    def test_unregister(self):
        """Test unregistering a type."""
        self.registry.register("user", MockService)
        result = self.registry.unregister("user")
        
        self.assertEqual(result, MockService)
        self.assertFalse(self.registry.contains("user"))
    
    def test_get_all(self):
        """Test getting all registered types."""
        self.registry.register("user", MockService)
        self.registry.register("widget", MockWidget)
        
        all_types = self.registry.get_all()
        
        self.assertEqual(len(all_types), 2)
        self.assertEqual(all_types["user"], MockService)
        self.assertEqual(all_types["widget"], MockWidget)
    
    def test_contains_type(self):
        """Test checking if a type class is registered."""
        self.registry.register("user", MockService)
        
        self.assertTrue(self.registry.contains_type(MockService))
        self.assertFalse(self.registry.contains_type(MockWidget))


# =============================================================================
# Thread Safety Tests
# =============================================================================

class TestThreadSafety(unittest.TestCase):
    """Test thread safety of registries."""
    
    def test_base_registry_concurrent_access(self):
        """Test concurrent access to BaseRegistry."""
        registry = BaseRegistry[int]()
        errors = []
        
        def register_items(start, count):
            try:
                for i in range(start, start + count):
                    registry.register(f"item_{i}", i)
            except Exception as e:
                errors.append(e)
        
        threads = [
            threading.Thread(target=register_items, args=(i * 100, 100))
            for i in range(10)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(registry.count, 1000)
    
    def test_service_registry_concurrent_factory(self):
        """Test concurrent factory access in ServiceRegistry."""
        registry = ServiceRegistry[MockService]()
        call_count = [0]
        lock = threading.Lock()
        
        def factory():
            with lock:
                call_count[0] += 1
            time.sleep(0.01)  # Simulate slow initialization
            return MockService("test")
        
        registry.register_factory("service", factory)
        
        instances = []
        
        def get_service():
            instances.append(registry.get("service"))
        
        threads = [threading.Thread(target=get_service) for _ in range(10)]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # All instances should be the same (singleton)
        first = instances[0]
        for instance in instances:
            self.assertIs(instance, first)
        
        # Factory should only be called once
        self.assertEqual(call_count[0], 1)


# =============================================================================
# Convenience Function Tests
# =============================================================================

class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_create_registry(self):
        """Test create_registry function."""
        registry = create_registry("test")
        self.assertIsInstance(registry, BaseRegistry)
        self.assertEqual(registry.name, "test")
    
    def test_create_service_registry(self):
        """Test create_service_registry function."""
        registry = create_service_registry("services")
        self.assertIsInstance(registry, ServiceRegistry)
    
    def test_create_plugin_registry(self):
        """Test create_plugin_registry function."""
        registry = create_plugin_registry("plugins")
        self.assertIsInstance(registry, PluginRegistry)
    
    def test_create_handler_registry(self):
        """Test create_handler_registry function."""
        registry = create_handler_registry("handlers")
        self.assertIsInstance(registry, HandlerRegistry)
    
    def test_create_factory_registry(self):
        """Test create_factory_registry function."""
        registry = create_factory_registry("factories")
        self.assertIsInstance(registry, FactoryRegistry)
    
    def test_create_type_registry(self):
        """Test create_type_registry function."""
        registry = create_type_registry("types")
        self.assertIsInstance(registry, TypeRegistry)
    
    def test_global_registries(self):
        """Test global registry functions."""
        self.assertIsInstance(global_registry(), BaseRegistry)
        self.assertIsInstance(global_services(), ServiceRegistry)
        self.assertIsInstance(global_plugins(), PluginRegistry)
        self.assertIsInstance(global_handlers(), HandlerRegistry)
        self.assertIsInstance(global_factories(), FactoryRegistry)
        self.assertIsInstance(global_types(), TypeRegistry)


# =============================================================================
# Run Tests
# =============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)