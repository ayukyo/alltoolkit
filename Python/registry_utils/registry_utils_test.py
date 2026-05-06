#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Registry Utils Test Suite
Tests for registry pattern implementations
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from registry_utils.mod import (
    RegistryError, AlreadyRegisteredError, NotRegisteredError,
    Priority, RegistryItem,
    BaseRegistry, ServiceRegistry, PluginRegistry, HandlerRegistry,
    FactoryRegistry, TypeRegistry,
    create_registry, create_service_registry, create_plugin_registry,
    create_handler_registry, create_factory_registry, create_type_registry,
    global_registry, global_services, global_plugins, global_handlers,
    global_factories, global_types
)


class TestResultCollector:
    """Collects test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_result(self, name, passed, message=""):
        self.tests.append((name, passed, message))
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Registry Utils Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}")
        if self.failed > 0:
            print("Failed tests:")
            for name, passed, msg in self.tests:
                if not passed:
                    print(f"  - {name}: {msg}")
        return self.failed == 0


results = TestResultCollector()


def test_exceptions():
    """Test registry exceptions"""
    try:
        assert RegistryError is not None
        assert AlreadyRegisteredError is not None
        assert NotRegisteredError is not None
        
        # Test inheritance
        assert issubclass(AlreadyRegisteredError, RegistryError)
        assert issubclass(NotRegisteredError, RegistryError)
        
        results.add_result("exceptions", True)
    except Exception as e:
        results.add_result("exceptions", False, str(e))


def test_priority_enum():
    """Test Priority enum"""
    try:
        assert Priority.LOWEST.value == 0
        assert Priority.HIGHEST.value == 100
        assert Priority.NORMAL.value == 50
        
        results.add_result("priority_enum", True)
    except Exception as e:
        results.add_result("priority_enum", False, str(e))


def test_registry_item():
    """Test RegistryItem dataclass"""
    try:
        item = RegistryItem(name="test", item="value", priority=50)
        assert item.name == "test"
        assert item.item == "value"
        assert item.priority == 50
        
        # Test comparison (higher priority comes first)
        item1 = RegistryItem(name="a", item=1, priority=100)
        item2 = RegistryItem(name="b", item=2, priority=50)
        assert item1 < item2
        
        results.add_result("registry_item", True)
    except Exception as e:
        results.add_result("registry_item", False, str(e))


def test_base_registry():
    """Test BaseRegistry class"""
    try:
        registry = BaseRegistry[str]()
        
        # Register
        registry.register("key1", "value1")
        assert registry.count == 1
        
        # Get
        assert registry.get("key1") == "value1"
        
        # Contains
        assert registry.contains("key1") == True
        assert registry.contains("key2") == False
        
        # Try get
        assert registry.try_get("key1") == "value1"
        assert registry.try_get("key2") is None
        
        # Unregister
        val = registry.unregister("key1")
        assert val == "value1"
        assert registry.count == 0
        
        # Duplicate registration
        registry.register("key1", "value1")
        try:
            registry.register("key1", "value2")
            results.add_result("base_registry", False, "Should raise for duplicate")
        except AlreadyRegisteredError:
            pass
        
        # Overwrite
        registry.register("key1", "value2", overwrite=True)
        assert registry.get("key1") == "value2"
        
        # Not registered error
        try:
            registry.get("not_exist")
            results.add_result("base_registry", False, "Should raise for not registered")
        except NotRegisteredError:
            pass
        
        results.add_result("base_registry", True)
    except Exception as e:
        results.add_result("base_registry", False, str(e))


def test_base_registry_namespaces():
    """Test BaseRegistry namespaces"""
    try:
        registry = BaseRegistry[str]()
        
        # Register in different namespaces
        registry.register("key", "value1", namespace="ns1")
        registry.register("key", "value2", namespace="ns2")
        
        assert registry.get("key", namespace="ns1") == "value1"
        assert registry.get("key", namespace="ns2") == "value2"
        
        # Get namespaces
        namespaces = registry.get_namespaces()
        assert "ns1" in namespaces
        assert "ns2" in namespaces
        
        # Get by namespace
        items = registry.get_by_namespace("ns1")
        assert items["key"] == "value1"
        
        # Clear namespace
        count = registry.clear(namespace="ns1")
        assert count == 1
        assert registry.contains("key", namespace="ns1") == False
        
        results.add_result("base_registry_namespaces", True)
    except Exception as e:
        results.add_result("base_registry_namespaces", False, str(e))


def test_base_registry_tags():
    """Test BaseRegistry tags"""
    try:
        registry = BaseRegistry[str]()
        
        registry.register("key1", "value1", tags={"tag1", "tag2"})
        registry.register("key2", "value2", tags={"tag1"})
        
        # Get by tag
        items = registry.get_by_tag("tag1")
        assert len(items) == 2
        
        items2 = registry.get_by_tag("tag2")
        assert len(items2) == 1
        
        # Get tags
        tags = registry.get_tags()
        assert "tag1" in tags
        assert "tag2" in tags
        
        results.add_result("base_registry_tags", True)
    except Exception as e:
        results.add_result("base_registry_tags", False, str(e))


def test_base_registry_decorator():
    """Test BaseRegistry decorator"""
    try:
        registry = BaseRegistry[str]()
        
        @registry.decorator("decorated")
        def my_func():
            return "test"
        
        assert registry.contains("decorated")
        assert registry.get("decorated") == my_func
        
        results.add_result("base_registry_decorator", True)
    except Exception as e:
        results.add_result("base_registry_decorator", False, str(e))


def test_base_registry_hooks():
    """Test BaseRegistry hooks"""
    try:
        registry = BaseRegistry[str]()
        register_calls = []
        unregister_calls = []
        
        def on_register(name, item):
            register_calls.append((name, item))
        
        def on_unregister(name, item):
            unregister_calls.append((name, item))
        
        registry.add_hook_on_register(on_register)
        registry.add_hook_on_unregister(on_unregister)
        
        registry.register("key1", "value1")
        assert len(register_calls) == 1
        
        registry.unregister("key1")
        assert len(unregister_calls) == 1
        
        results.add_result("base_registry_hooks", True)
    except Exception as e:
        results.add_result("base_registry_hooks", False, str(e))


def test_service_registry():
    """Test ServiceRegistry class"""
    try:
        registry = ServiceRegistry[str]()
        
        # Direct registration
        registry.register("service1", "instance1")
        assert registry.get("service1") == "instance1"
        
        # Factory registration
        registry.register_factory("service2", lambda: "factory_instance")
        instance = registry.get("service2")
        assert instance == "factory_instance"
        
        # Singleton behavior
        instance2 = registry.get("service2")
        assert instance is instance2
        
        # Non-singleton factory - returns different instances each time
        counter = [0]
        def make_counted():
            counter[0] += 1
            return f"instance_{counter[0]}"
        
        registry.register_factory("service3", make_counted, singleton=False)
        inst1 = registry.get("service3")
        inst2 = registry.get("service3")
        # Different instances since not singleton
        assert inst1 != inst2
        
        # Unregister
        result = registry.unregister("service1")
        assert result == "instance1"
        
        results.add_result("service_registry", True)
    except Exception as e:
        results.add_result("service_registry", False, str(e))


def test_plugin_registry():
    """Test PluginRegistry class"""
    try:
        registry = PluginRegistry()
        
        # Register plugin
        class TestPlugin:
            def activate(self):
                pass
            def deactivate(self):
                pass
        
        registry.register("plugin1", TestPlugin(), version="1.0.0")
        
        # Get
        assert registry.contains("plugin1")
        assert registry.get("plugin1") is not None
        
        # Get info
        info = registry.get_info("plugin1")
        assert info.version == "1.0.0"
        assert info.enabled == True
        
        # Enable/disable
        assert registry.is_enabled("plugin1") == True
        registry.disable("plugin1")
        assert registry.is_enabled("plugin1") == False
        registry.enable("plugin1")
        assert registry.is_enabled("plugin1") == True
        
        # Decorator
        @registry.decorator("plugin2", version="2.0.0")
        class DecoratedPlugin:
            pass
        
        assert registry.contains("plugin2")
        
        results.add_result("plugin_registry", True)
    except Exception as e:
        results.add_result("plugin_registry", False, str(e))


def test_plugin_registry_dependencies():
    """Test PluginRegistry dependencies"""
    try:
        registry = PluginRegistry()
        
        class Plugin:
            pass
        
        # Register with dependency
        registry.register("base", Plugin())
        registry.register("dependent", Plugin(), dependencies=["base"])
        
        # Check dependencies
        satisfied, missing = registry.check_dependencies("dependent")
        assert satisfied == True
        
        # Disable base should fail
        try:
            registry.disable("base")
            results.add_result("plugin_registry_dependencies", False, "Should fail with dependent")
        except RegistryError:
            pass
        
        results.add_result("plugin_registry_dependencies", True)
    except Exception as e:
        results.add_result("plugin_registry_dependencies", False, str(e))


def test_handler_registry():
    """Test HandlerRegistry class"""
    try:
        registry = HandlerRegistry[callable]()
        
        # Register handlers
        def handler1(event):
            return "handler1"
        
        def handler2(event):
            return "handler2"
        
        registry.register("event.type1", handler1, priority=100)
        registry.register("event.type1", handler2, priority=50)
        
        # Get handlers (sorted by priority)
        handlers = registry.get_handlers("event.type1")
        assert len(handlers) == 2
        assert handlers[0] == handler1  # Higher priority first
        
        # Has handlers
        assert registry.has_handlers("event.type1") == True
        
        # Unregister
        registry.unregister("event.type1", handler1)
        assert len(registry.get_handlers("event.type1")) == 1
        
        # Decorator
        @registry.decorator("event.type2")
        def decorated_handler(event):
            return "decorated"
        
        assert registry.has_handlers("event.type2")
        
        results.add_result("handler_registry", True)
    except Exception as e:
        results.add_result("handler_registry", False, str(e))


def test_factory_registry():
    """Test FactoryRegistry class"""
    try:
        registry = FactoryRegistry[str]()
        
        # Register factory (function)
        def make_uppercase(text):
            return text.upper()
        
        registry.register("uppercase", make_uppercase)
        
        # Create instance (pass positional args)
        result = registry.create("uppercase", "hello")
        assert result == "HELLO"
        
        # Singleton factory
        class Widget:
            def __init__(self, name=None):
                self.name = name if name else "default"
        
        registry.register("widget", Widget, singleton=True)
        w1 = registry.create("widget")
        w2 = registry.create("widget")
        assert w1 is w2
        
        # Contains
        assert registry.contains("uppercase")
        
        # Decorator
        @registry.decorator("gadget", singleton=False)
        class Gadget:
            pass
        
        assert registry.contains("gadget")
        
        results.add_result("factory_registry", True)
    except Exception as e:
        results.add_result("factory_registry", False, str(e))


def test_type_registry():
    """Test TypeRegistry class"""
    try:
        registry = TypeRegistry()
        
        # Register type
        class User:
            def __init__(self, name):
                self.name = name
        
        registry.register("user", User)
        
        # Get type
        assert registry.get("user") == User
        
        # Create instance
        instance = registry.create("user", name="John")
        assert instance.name == "John"
        
        # Get name
        assert registry.get_name(User) == "user"
        
        # Contains
        assert registry.contains("user")
        assert registry.contains_type(User)
        
        # Decorator
        @registry.decorator("product")
        class Product:
            pass
        
        assert registry.contains("product")
        
        results.add_result("type_registry", True)
    except Exception as e:
        results.add_result("type_registry", False, str(e))


def test_type_registry_aliases():
    """Test TypeRegistry aliases"""
    try:
        registry = TypeRegistry()
        
        class User:
            pass
        
        registry.register("user", User, aliases=["person", "member"])
        
        assert registry.get("user") == User
        assert registry.get("person") == User
        assert registry.get("member") == User
        
        results.add_result("type_registry_aliases", True)
    except Exception as e:
        results.add_result("type_registry_aliases", False, str(e))


def test_convenience_functions():
    """Test convenience functions"""
    try:
        registry = create_registry("test")
        assert registry.name == "test"
        
        service_reg = create_service_registry("services")
        assert service_reg._name == "services"
        
        plugin_reg = create_plugin_registry("plugins")
        assert plugin_reg._name == "plugins"
        
        handler_reg = create_handler_registry("handlers")
        assert handler_reg._name == "handlers"
        
        factory_reg = create_factory_registry("factories")
        assert factory_reg._name == "factories"
        
        type_reg = create_type_registry("types")
        assert type_reg._name == "types"
        
        results.add_result("convenience_functions", True)
    except Exception as e:
        results.add_result("convenience_functions", False, str(e))


def test_global_registries():
    """Test global registries"""
    try:
        g_reg = global_registry()
        assert g_reg is not None
        
        g_services = global_services()
        assert g_services is not None
        
        g_plugins = global_plugins()
        assert g_plugins is not None
        
        g_handlers = global_handlers()
        assert g_handlers is not None
        
        g_factories = global_factories()
        assert g_factories is not None
        
        g_types = global_types()
        assert g_types is not None
        
        results.add_result("global_registries", True)
    except Exception as e:
        results.add_result("global_registries", False, str(e))


def test_operators():
    """Test registry operators"""
    try:
        registry = BaseRegistry[str]()
        registry.register("key", "value")
        
        # __contains__
        assert "key" in registry
        
        # __getitem__
        assert registry["key"] == "value"
        
        # __len__
        assert len(registry) == 1
        
        # __repr__
        repr_str = repr(registry)
        assert "BaseRegistry" in repr_str
        
        results.add_result("operators", True)
    except Exception as e:
        results.add_result("operators", False, str(e))


def test_metadata():
    """Test registry metadata"""
    try:
        registry = BaseRegistry[str]()
        registry.register("key", "value", metadata={"desc": "test"})
        
        # Get metadata
        meta = registry.get_metadata("key")
        assert meta["desc"] == "test"
        
        # Set metadata
        registry.set_metadata("key", "extra", "data")
        meta = registry.get_metadata("key")
        assert meta["extra"] == "data"
        
        results.add_result("metadata", True)
    except Exception as e:
        results.add_result("metadata", False, str(e))


def test_clear():
    """Test registry clearing"""
    try:
        registry = BaseRegistry[str]()
        registry.register("key1", "value1")
        registry.register("key2", "value2")
        
        count = registry.clear()
        assert count == 2
        assert registry.is_empty
        
        results.add_result("clear", True)
    except Exception as e:
        results.add_result("clear", False, str(e))


def test_get_all():
    """Test get_all functionality"""
    try:
        registry = BaseRegistry[str]()
        registry.register("key1", "value1")
        registry.register("key2", "value2")
        
        all_items = registry.get_all()
        assert len(all_items) == 2
        assert all_items["default:key1"] == "value1"
        
        names = registry.get_names()
        assert len(names) == 2
        
        results.add_result("get_all", True)
    except Exception as e:
        results.add_result("get_all", False, str(e))


def test_edge_cases():
    """Test edge cases"""
    try:
        registry = BaseRegistry[str]()
        
        # Empty registry
        assert registry.is_empty
        assert registry.count == 0
        
        # Get from empty
        assert registry.try_get("nonexistent") is None
        
        # Unregister from empty
        try:
            registry.unregister("nonexistent")
        except NotRegisteredError:
            pass
        
        results.add_result("edge_cases", True)
    except Exception as e:
        results.add_result("edge_cases", False, str(e))


# Run all tests
def run_tests():
    """Run all test functions"""
    test_exceptions()
    test_priority_enum()
    test_registry_item()
    test_base_registry()
    test_base_registry_namespaces()
    test_base_registry_tags()
    test_base_registry_decorator()
    test_base_registry_hooks()
    test_service_registry()
    test_plugin_registry()
    test_plugin_registry_dependencies()
    test_handler_registry()
    test_factory_registry()
    test_type_registry()
    test_type_registry_aliases()
    test_convenience_functions()
    test_global_registries()
    test_operators()
    test_metadata()
    test_clear()
    test_get_all()
    test_edge_cases()
    
    return results.summary()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)