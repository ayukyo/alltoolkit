"""
Reflection Utilities Module

A comprehensive toolkit for Python introspection and reflection operations.
Provides utilities for inspecting objects, types, functions, and classes.

Features:
- Object introspection (attributes, methods, properties)
- Function signature analysis
- Type checking and validation
- Dynamic attribute access and manipulation
- Class hierarchy inspection
- Decorator helpers
- Dynamic code generation helpers

Zero external dependencies - uses only Python standard library.
"""

import inspect
import types
import sys
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    get_type_hints,
)
from dataclasses import fields, is_dataclass
from functools import wraps
from enum import Enum

# Python 3.6 compatibility for get_origin and get_args
if sys.version_info >= (3, 8):
    from typing import get_origin, get_args
else:
    # Fallback for Python 3.6/3.7
    def get_origin(tp):
        """Get the origin of a generic type (compatibility for Python 3.6)."""
        if hasattr(tp, '__origin__'):
            return tp.__origin__
        return None
    
    def get_args(tp):
        """Get the arguments of a generic type (compatibility for Python 3.6)."""
        if hasattr(tp, '__args__'):
            return tp.__args__
        return ()


class ReflectionUtils:
    """
    A collection of utilities for Python reflection and introspection.
    
    This class provides static methods for analyzing and manipulating
    Python objects, classes, and functions at runtime.
    """
    
    # ==================== Object Introspection ====================
    
    @staticmethod
    def get_all_attributes(obj: Any, include_private: bool = False) -> Dict[str, Any]:
        """
        Get all attributes of an object.
        
        Args:
            obj: The object to inspect
            include_private: Whether to include private attributes (starting with _)
            
        Returns:
            Dictionary of attribute names to values
        """
        attrs = {}
        for name in dir(obj):
            if not include_private and name.startswith('_'):
                continue
            try:
                attrs[name] = getattr(obj, name)
            except Exception:
                attrs[name] = f"<Error accessing attribute '{name}'>"
        return attrs
    
    @staticmethod
    def get_methods(obj: Any, include_private: bool = False) -> Dict[str, Callable]:
        """
        Get all methods of an object.
        
        Args:
            obj: The object to inspect
            include_private: Whether to include private methods
            
        Returns:
            Dictionary of method names to callable objects
        """
        methods = {}
        for name in dir(obj):
            if not include_private and name.startswith('_'):
                continue
            attr = getattr(obj, name, None)
            if callable(attr):
                methods[name] = attr
        return methods
    
    @staticmethod
    def get_properties(obj: Any, include_private: bool = False) -> Dict[str, property]:
        """
        Get all properties of a class.
        
        Args:
            obj: The object or class to inspect
            include_private: Whether to include private properties
            
        Returns:
            Dictionary of property names to property objects
        """
        if isinstance(obj, type):
            cls = obj
        else:
            cls = obj.__class__
        
        properties = {}
        for name in dir(cls):
            if not include_private and name.startswith('_'):
                continue
            attr = getattr(cls, name, None)
            if isinstance(attr, property):
                properties[name] = attr
        return properties
    
    @staticmethod
    def get_instance_attributes(obj: Any) -> Dict[str, Any]:
        """
        Get instance attributes (stored in __dict__).
        
        Args:
            obj: The object to inspect
            
        Returns:
            Dictionary of instance attribute names to values
        """
        if hasattr(obj, '__dict__'):
            return dict(obj.__dict__)
        return {}
    
    @staticmethod
    def get_class_attributes(cls: Type) -> Dict[str, Any]:
        """
        Get class-level attributes (not inherited).
        
        Args:
            cls: The class to inspect
            
        Returns:
            Dictionary of class attribute names to values
        """
        if not isinstance(cls, type):
            cls = cls.__class__
        
        attrs = {}
        for name, value in cls.__dict__.items():
            if not name.startswith('__'):
                attrs[name] = value
        return attrs
    
    # ==================== Function Introspection ====================
    
    @staticmethod
    def get_function_info(func: Callable) -> Dict[str, Any]:
        """
        Get detailed information about a function.
        
        Args:
            func: The function to inspect
            
        Returns:
            Dictionary containing function metadata
        """
        info = {
            'name': func.__name__,
            'module': func.__module__,
            'doc': inspect.getdoc(func),
            'is_builtin': inspect.isbuiltin(func),
            'is_function': inspect.isfunction(func),
            'is_method': inspect.ismethod(func),
            'is_coroutine': inspect.iscoroutinefunction(func),
            'is_generator': inspect.isgeneratorfunction(func),
        }
        
        # Get signature
        try:
            sig = inspect.signature(func)
            info['signature'] = str(sig)
            info['parameters'] = {}
            for name, param in sig.parameters.items():
                info['parameters'][name] = {
                    'kind': str(param.kind),
                    'default': param.default if param.default is not param.empty else None,
                    'has_default': param.default is not param.empty,
                    'annotation': str(param.annotation) if param.annotation is not param.empty else None,
                }
            info['return_annotation'] = str(sig.return_annotation) if sig.return_annotation is not sig.empty else None
        except (ValueError, TypeError):
            info['signature'] = None
            info['parameters'] = None
            info['return_annotation'] = None
        
        # Get source
        try:
            source = inspect.getsource(func)
            info['source_lines'] = len(source.splitlines())
            info['source_file'] = inspect.getfile(func)
            info['source_line_number'] = inspect.getsourcelines(func)[1]
        except (OSError, TypeError):
            info['source_lines'] = None
            info['source_file'] = None
            info['source_line_number'] = None
        
        return info
    
    @staticmethod
    def get_parameters(func: Callable) -> List[Dict[str, Any]]:
        """
        Get parameter details of a function.
        
        Args:
            func: The function to inspect
            
        Returns:
            List of parameter information dictionaries
        """
        params = []
        try:
            sig = inspect.signature(func)
            for name, param in sig.parameters.items():
                params.append({
                    'name': name,
                    'kind': str(param.kind.name),
                    'default': param.default if param.default is not param.empty else None,
                    'has_default': param.default is not param.empty,
                    'annotation': param.annotation if param.annotation is not param.empty else None,
                })
        except (ValueError, TypeError):
            pass
        return params
    
    @staticmethod
    def get_return_type(func: Callable) -> Optional[Type]:
        """
        Get the return type annotation of a function.
        
        Args:
            func: The function to inspect
            
        Returns:
            The return type or None if not annotated
        """
        try:
            sig = inspect.signature(func)
            if sig.return_annotation is not sig.empty:
                return sig.return_annotation
        except (ValueError, TypeError):
            pass
        return None
    
    @staticmethod
    def get_type_hints_safe(obj: Any) -> Dict[str, Type]:
        """
        Safely get type hints from an object.
        
        Args:
            obj: The object to get type hints from
            
        Returns:
            Dictionary of name to type annotations
        """
        try:
            return get_type_hints(obj)
        except Exception:
            return {}
    
    # ==================== Class Introspection ====================
    
    @staticmethod
    def get_class_hierarchy(cls: Type) -> List[Type]:
        """
        Get the class hierarchy (MRO - Method Resolution Order).
        
        Args:
            cls: The class to inspect
            
        Returns:
            List of classes in MRO order
        """
        if not isinstance(cls, type):
            cls = cls.__class__
        return list(cls.__mro__)
    
    @staticmethod
    def get_base_classes(cls: Type) -> Tuple[Type, ...]:
        """
        Get direct base classes of a class.
        
        Args:
            cls: The class to inspect
            
        Returns:
            Tuple of base classes
        """
        if not isinstance(cls, type):
            cls = cls.__class__
        return cls.__bases__
    
    @staticmethod
    def get_subclasses(cls: Type) -> List[Type]:
        """
        Get all subclasses of a class.
        
        Args:
            cls: The class to inspect
            
        Returns:
            List of all subclasses (recursively)
        """
        return cls.__subclasses__()
    
    @staticmethod
    def is_subclass_of(obj: Any, parent_class: Type) -> bool:
        """
        Check if an object or class is a subclass of another class.
        
        Args:
            obj: The object or class to check
            parent_class: The potential parent class
            
        Returns:
            True if obj is a subclass of parent_class
        """
        if isinstance(obj, type):
            return issubclass(obj, parent_class)
        return isinstance(obj, parent_class)
    
    @staticmethod
    def get_class_source(cls: Type) -> Optional[str]:
        """
        Get the source code of a class.
        
        Args:
            cls: The class to get source for
            
        Returns:
            Source code string or None if unavailable
        """
        try:
            return inspect.getsource(cls)
        except (OSError, TypeError):
            return None
    
    # ==================== Type Utilities ====================
    
    @staticmethod
    def get_type_name(obj: Any) -> str:
        """
        Get the fully qualified type name of an object.
        
        Args:
            obj: The object to get type name for
            
        Returns:
            Fully qualified type name string
        """
        cls = obj if isinstance(obj, type) else type(obj)
        module = cls.__module__
        name = cls.__qualname__
        if module == 'builtins':
            return name
        return f"{module}.{name}"
    
    @staticmethod
    def get_origin_type(hint: Any) -> Optional[Type]:
        """
        Get the origin type from a type hint (e.g., List[int] -> list).
        
        Args:
            hint: The type hint to analyze
            
        Returns:
            The origin type or None
        """
        return get_origin(hint)
    
    @staticmethod
    def get_type_args(hint: Any) -> Tuple[Any, ...]:
        """
        Get type arguments from a generic type (e.g., List[int] -> (int,)).
        
        Args:
            hint: The type hint to analyze
            
        Returns:
            Tuple of type arguments
        """
        return get_args(hint)
    
    @staticmethod
    def is_optional_type(hint: Any) -> bool:
        """
        Check if a type hint is Optional[T] (Union[T, None]).
        
        Args:
            hint: The type hint to check
            
        Returns:
            True if the hint is Optional
        """
        origin = get_origin(hint)
        if origin is Union:
            args = get_args(hint)
            return type(None) in args
        return False
    
    @staticmethod
    def get_optional_type(hint: Any) -> Optional[Type]:
        """
        Get the wrapped type from Optional[T].
        
        Args:
            hint: The Optional type hint
            
        Returns:
            The inner type or None if not Optional
        """
        if not ReflectionUtils.is_optional_type(hint):
            return None
        args = get_args(hint)
        for arg in args:
            if arg is not type(None):
                return arg
        return None
    
    @staticmethod
    def is_generic_type(obj: Any) -> bool:
        """
        Check if an object is a generic type.
        
        Args:
            obj: The object to check
            
        Returns:
            True if the object is a generic type
        """
        origin = get_origin(obj)
        return origin is not None
    
    # ==================== Dynamic Operations ====================
    
    @staticmethod
    def safe_getattr(obj: Any, name: str, default: Any = None) -> Any:
        """
        Safely get an attribute, returning default on error.
        
        Args:
            obj: The object to get attribute from
            name: The attribute name
            default: Default value if attribute doesn't exist or raises error
            
        Returns:
            The attribute value or default
        """
        try:
            return getattr(obj, name, default)
        except Exception:
            return default
    
    @staticmethod
    def safe_setattr(obj: Any, name: str, value: Any) -> bool:
        """
        Safely set an attribute, returning success status.
        
        Args:
            obj: The object to set attribute on
            name: The attribute name
            value: The value to set
            
        Returns:
            True if successful, False otherwise
        """
        try:
            setattr(obj, name, value)
            return True
        except Exception:
            return False
    
    @staticmethod
    def safe_delattr(obj: Any, name: str) -> bool:
        """
        Safely delete an attribute, returning success status.
        
        Args:
            obj: The object to delete attribute from
            name: The attribute name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            delattr(obj, name)
            return True
        except Exception:
            return False
    
    @staticmethod
    def has_attribute(obj: Any, name: str) -> bool:
        """
        Check if an object has an attribute.
        
        Args:
            obj: The object to check
            name: The attribute name
            
        Returns:
            True if attribute exists
        """
        return hasattr(obj, name)
    
    @staticmethod
    def call_method(obj: Any, method_name: str, *args, **kwargs) -> Any:
        """
        Dynamically call a method on an object.
        
        Args:
            obj: The object to call method on
            method_name: The method name
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            The method's return value
            
        Raises:
            AttributeError: If method doesn't exist
            TypeError: If attribute is not callable
        """
        method = getattr(obj, method_name)
        if not callable(method):
            raise TypeError(f"'{method_name}' is not callable")
        return method(*args, **kwargs)
    
    # ==================== Dataclass Utilities ====================
    
    @staticmethod
    def is_dataclass_instance(obj: Any) -> bool:
        """
        Check if an object is a dataclass instance.
        
        Args:
            obj: The object to check
            
        Returns:
            True if obj is a dataclass instance
        """
        return is_dataclass(obj) and not isinstance(obj, type)
    
    @staticmethod
    def get_dataclass_fields(obj: Any) -> List[Dict[str, Any]]:
        """
        Get field information from a dataclass.
        
        Args:
            obj: The dataclass instance or class
            
        Returns:
            List of field information dictionaries
        """
        if not is_dataclass(obj):
            return []
        
        result = []
        for field in fields(obj):
            result.append({
                'name': field.name,
                'type': field.type,
                'default': field.default if field.default is not field.default else None,
                'default_factory': field.default_factory if field.default_factory is not field.default_factory else None,
                'init': field.init,
                'repr': field.repr,
                'hash': field.hash,
                'compare': field.compare,
            })
        return result
    
    @staticmethod
    def dataclass_to_dict(obj: Any) -> Dict[str, Any]:
        """
        Convert a dataclass instance to a dictionary.
        
        Args:
            obj: The dataclass instance
            
        Returns:
            Dictionary representation
        """
        if hasattr(obj, 'asdict'):
            return obj.asdict()
        elif is_dataclass(obj):
            from dataclasses import asdict
            return asdict(obj)
        return {}
    
    # ==================== Decorator Helpers ====================
    
    @staticmethod
    def preserve_signature(func: Callable) -> Callable:
        """
        Decorator to preserve the original function's signature.
        
        Args:
            func: The function to wrap
            
        Returns:
            Wrapped function with preserved signature
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    
    @staticmethod
    def get_decorator_stack(func: Callable) -> List[str]:
        """
        Get the stack of decorators applied to a function.
        
        Note: This is a best-effort approach and may not work for all cases.
        
        Args:
            func: The decorated function
            
        Returns:
            List of decorator names
        """
        decorators = []
        current = func
        
        while hasattr(current, '__wrapped__'):
            # Try to get decorator name
            if hasattr(current, '__name__'):
                decorators.append(current.__name__)
            current = current.__wrapped__
        
        return decorators
    
    # ==================== Special Method Detection ====================
    
    @staticmethod
    def get_special_methods(obj: Any) -> Dict[str, Callable]:
        """
        Get all special methods (__magic__) of an object.
        
        Args:
            obj: The object to inspect
            
        Returns:
            Dictionary of special method names to callables
        """
        methods = {}
        for name in dir(obj):
            if name.startswith('__') and name.endswith('__'):
                try:
                    attr = getattr(obj, name)
                    if callable(attr):
                        methods[name] = attr
                except Exception:
                    pass
        return methods
    
    @staticmethod
    def supports_protocol(obj: Any, protocol: str) -> bool:
        """
        Check if an object supports a specific protocol.
        
        Args:
            obj: The object to check
            protocol: The protocol name (e.g., 'iterable', 'callable', 'context')
            
        Returns:
            True if the object supports the protocol
        """
        protocol_checks = {
            'iterable': lambda o: hasattr(o, '__iter__'),
            'iterator': lambda o: hasattr(o, '__iter__') and hasattr(o, '__next__'),
            'callable': lambda o: callable(o),
            'context': lambda o: hasattr(o, '__enter__') and hasattr(o, '__exit__'),
            'hashable': lambda o: hasattr(o, '__hash__') and o.__hash__ is not None,
            'comparable': lambda o: hasattr(o, '__eq__'),
            'orderable': lambda o: all(hasattr(o, m) for m in ['__lt__', '__gt__']),
            'sized': lambda o: hasattr(o, '__len__'),
            'container': lambda o: hasattr(o, '__contains__'),
            'sequence': lambda o: hasattr(o, '__getitem__') and hasattr(o, '__len__'),
            'mapping': lambda o: hasattr(o, '__getitem__') and hasattr(o, '__iter__') and hasattr(o, '__len__'),
            'mutable_sequence': lambda o: hasattr(o, '__setitem__') and hasattr(o, '__delitem__'),
            'async_iterable': lambda o: hasattr(o, '__aiter__'),
            'async_context': lambda o: hasattr(o, '__aenter__') and hasattr(o, '__aexit__'),
        }
        
        check_func = protocol_checks.get(protocol.lower())
        if check_func:
            try:
                return check_func(obj)
            except Exception:
                return False
        return False
    
    # ==================== Instance Creation ====================
    
    @staticmethod
    def create_instance(cls: Type, *args, **kwargs) -> Any:
        """
        Create an instance of a class.
        
        Args:
            cls: The class to instantiate
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            New instance
        """
        return cls(*args, **kwargs)
    
    @staticmethod
    def get_default_constructor_args(cls: Type) -> Dict[str, Any]:
        """
        Get default arguments for a class constructor.
        
        Args:
            cls: The class to inspect
            
        Returns:
            Dictionary of parameter names to default values
        """
        defaults = {}
        try:
            sig = inspect.signature(cls)
            for name, param in sig.parameters.items():
                if param.default is not param.empty:
                    defaults[name] = param.default
        except (ValueError, TypeError):
            pass
        return defaults


class AttributeInspector:
    """
    A utility class for inspecting attributes in detail.
    """
    
    @staticmethod
    def find_attributes_by_type(obj: Any, attr_type: Type) -> Dict[str, Any]:
        """
        Find all attributes of a specific type.
        
        Args:
            obj: The object to inspect
            attr_type: The type to search for
            
        Returns:
            Dictionary of attribute names to values
        """
        result = {}
        for name in dir(obj):
            if name.startswith('_'):
                continue
            try:
                value = getattr(obj, name)
                if isinstance(value, attr_type):
                    result[name] = value
            except Exception:
                pass
        return result
    
    @staticmethod
    def find_methods_by_decorator(obj: Any, decorator_name: str) -> List[str]:
        """
        Find methods decorated with a specific decorator.
        
        Note: This relies on the decorator setting a marker attribute.
        
        Args:
            obj: The object to inspect
            decorator_name: The decorator marker to look for
            
        Returns:
            List of method names
        """
        methods = []
        for name in dir(obj):
            if name.startswith('_'):
                continue
            try:
                attr = getattr(obj, name)
                if callable(attr) and hasattr(attr, decorator_name):
                    methods.append(name)
            except Exception:
                pass
        return methods
    
    @staticmethod
    def get_attribute_chain(obj: Any, path: str, default: Any = None) -> Any:
        """
        Get a nested attribute using dot notation.
        
        Args:
            obj: The root object
            path: Dot-separated attribute path (e.g., 'a.b.c')
            default: Default value if path doesn't exist
            
        Returns:
            The attribute value or default
        """
        current = obj
        for part in path.split('.'):
            try:
                current = getattr(current, part)
            except AttributeError:
                return default
        return current
    
    @staticmethod
    def set_attribute_chain(obj: Any, path: str, value: Any) -> bool:
        """
        Set a nested attribute using dot notation.
        
        Args:
            obj: The root object
            path: Dot-separated attribute path (e.g., 'a.b.c')
            value: The value to set
            
        Returns:
            True if successful
        """
        parts = path.split('.')
        current = obj
        
        for part in parts[:-1]:
            try:
                current = getattr(current, part)
            except AttributeError:
                return False
        
        try:
            setattr(current, parts[-1], value)
            return True
        except Exception:
            return False


class TypeAnalyzer:
    """
    A utility class for detailed type analysis.
    """
    
    @staticmethod
    def analyze(obj: Any) -> Dict[str, Any]:
        """
        Perform a comprehensive type analysis.
        
        Args:
            obj: The object to analyze
            
        Returns:
            Dictionary with type analysis results
        """
        actual_type = type(obj)
        
        return {
            'type': actual_type,
            'type_name': actual_type.__name__,
            'module': actual_type.__module__,
            'is_class': isinstance(obj, type),
            'is_instance': not isinstance(obj, type),
            'is_callable': callable(obj),
            'is_module': isinstance(obj, types.ModuleType),
            'is_function': isinstance(obj, types.FunctionType),
            'is_method': isinstance(obj, types.MethodType),
            'is_builtin': isinstance(obj, (int, float, str, list, dict, set, tuple, bool, bytes, type(None))),
            'is_dataclass': is_dataclass(obj),
            'is_enum': isinstance(obj, Enum),
            'mro': [c.__name__ for c in actual_type.__mro__] if isinstance(obj, type) else [c.__name__ for c in actual_type.__mro__],
        }
    
    @staticmethod
    def get_all_bases(cls: Type) -> Set[Type]:
        """
        Get all base classes recursively.
        
        Args:
            cls: The class to analyze
            
        Returns:
            Set of all base classes
        """
        bases = set()
        
        def collect_bases(c):
            for base in c.__bases__:
                if base is not object:
                    bases.add(base)
                    collect_bases(base)
        
        collect_bases(cls if isinstance(cls, type) else cls.__class__)
        return bases
    
    @staticmethod
    def implements_interface(cls: Type, interface: Type) -> bool:
        """
        Check if a class implements an interface (is subclass or has required methods).
        
        Args:
            cls: The class to check
            interface: The interface to check against
            
        Returns:
            True if the class implements the interface
        """
        if isinstance(cls, type) and issubclass(cls, interface):
            return True
        
        # Check if all methods of interface are present
        interface_methods = set()
        for name in dir(interface):
            if not name.startswith('_'):
                attr = getattr(interface, name, None)
                if callable(attr):
                    interface_methods.add(name)
        
        if not interface_methods:
            return False
        
        for method in interface_methods:
            if not hasattr(cls, method):
                return False
            attr = getattr(cls, method)
            if not callable(attr):
                return False
        
        return True


# Convenience functions for quick use

def get_obj_info(obj: Any) -> Dict[str, Any]:
    """
    Get comprehensive information about any object.
    
    This is a convenience function that combines multiple inspection methods.
    
    Args:
        obj: The object to inspect
        
    Returns:
        Dictionary with object information
    """
    return {
        'type': type(obj).__name__,
        'module': type(obj).__module__,
        'attributes': ReflectionUtils.get_all_attributes(obj, include_private=False),
        'methods': list(ReflectionUtils.get_methods(obj, include_private=False).keys()),
        'properties': list(ReflectionUtils.get_properties(obj).keys()),
        'instance_attrs': list(ReflectionUtils.get_instance_attributes(obj).keys()),
        'is_callable': callable(obj),
        'is_dataclass': is_dataclass(obj),
        'type_analysis': TypeAnalyzer.analyze(obj),
    }


def describe(obj: Any, include_private: bool = False, max_depth: int = 1) -> str:
    """
    Generate a human-readable description of an object.
    
    Args:
        obj: The object to describe
        include_private: Whether to include private attributes
        max_depth: Maximum depth for nested descriptions
        
    Returns:
        Human-readable description string
    """
    lines = []
    obj_type = type(obj).__name__
    
    lines.append(f"Object: {obj_type}")
    lines.append("=" * (len(lines[-1])))
    
    # Type info
    lines.append(f"\nType: {ReflectionUtils.get_type_name(obj)}")
    lines.append(f"Module: {type(obj).__module__}")
    lines.append(f"Callable: {callable(obj)}")
    
    # Methods
    methods = ReflectionUtils.get_methods(obj, include_private)
    if methods:
        lines.append(f"\nMethods ({len(methods)}):")
        for name in sorted(methods.keys())[:10]:  # Limit to first 10
            lines.append(f"  - {name}()")
        if len(methods) > 10:
            lines.append(f"  ... and {len(methods) - 10} more")
    
    # Properties
    properties = ReflectionUtils.get_properties(obj)
    if properties:
        lines.append(f"\nProperties ({len(properties)}):")
        for name in sorted(properties.keys()):
            lines.append(f"  - {name}")
    
    # Instance attributes
    attrs = ReflectionUtils.get_instance_attributes(obj)
    if attrs:
        lines.append(f"\nInstance Attributes ({len(attrs)}):")
        for name, value in sorted(attrs.items())[:10]:
            value_str = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
            lines.append(f"  - {name}: {value_str}")
        if len(attrs) > 10:
            lines.append(f"  ... and {len(attrs) - 10} more")
    
    return "\n".join(lines)


# Example usage and testing
if __name__ == "__main__":
    # Example class for testing
    from dataclasses import dataclass
    from typing import Optional, List
    
    @dataclass
    class Person:
        name: str
        age: int
        email: Optional[str] = None
        tags: List[str] = None
        
        def __post_init__(self):
            if self.tags is None:
                self.tags = []
        
        def greet(self) -> str:
            return f"Hello, I'm {self.name}"
        
        @property
        def is_adult(self) -> bool:
            return self.age >= 18
    
    # Test reflection utilities
    print("=" * 60)
    print("Reflection Utils Test")
    print("=" * 60)
    
    person = Person("Alice", 25, "alice@example.com", ["friend", "developer"])
    
    # Test object introspection
    print("\n1. Object Introspection:")
    print(f"   All attributes: {list(ReflectionUtils.get_all_attributes(person).keys())[:5]}...")
    print(f"   Methods: {list(ReflectionUtils.get_methods(person).keys())}")
    print(f"   Properties: {list(ReflectionUtils.get_properties(person).keys())}")
    print(f"   Instance attrs: {list(ReflectionUtils.get_instance_attributes(person).keys())}")
    
    # Test function introspection
    print("\n2. Function Introspection:")
    func_info = ReflectionUtils.get_function_info(person.greet)
    print(f"   Function name: {func_info['name']}")
    print(f"   Signature: {func_info['signature']}")
    print(f"   Parameters: {func_info['parameters']}")
    
    # Test class introspection
    print("\n3. Class Introspection:")
    print(f"   Class hierarchy: {[c.__name__ for c in ReflectionUtils.get_class_hierarchy(Person)]}")
    print(f"   Base classes: {[c.__name__ for c in ReflectionUtils.get_base_classes(Person)]}")
    
    # Test dataclass utilities
    print("\n4. Dataclass Utilities:")
    print(f"   Is dataclass: {ReflectionUtils.is_dataclass_instance(person)}")
    print(f"   Fields: {[f['name'] for f in ReflectionUtils.get_dataclass_fields(person)]}")
    
    # Test type utilities
    print("\n5. Type Utilities:")
    print(f"   Type name: {ReflectionUtils.get_type_name(person)}")
    
    # Test protocol support
    print("\n6. Protocol Support:")
    print(f"   Iterable: {ReflectionUtils.supports_protocol(person, 'iterable')}")
    print(f"   Hashable: {ReflectionUtils.supports_protocol(person, 'hashable')}")
    
    # Test describe function
    print("\n7. Describe:")
    print(describe(person))
    
    # Test TypeAnalyzer
    print("\n8. Type Analysis:")
    analysis = TypeAnalyzer.analyze(person)
    print(f"   Analysis: {analysis}")
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)