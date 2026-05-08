"""
Reflection Utils - Usage Examples

This file demonstrates various use cases for the reflection utilities module.
"""

from typing import Optional, List, Dict, Generic, TypeVar
from dataclasses import dataclass, field
from functools import wraps
from enum import Enum
import json

# Import the module
import sys
sys.path.insert(0, '..')
from mod import (
    ReflectionUtils,
    AttributeInspector,
    TypeAnalyzer,
    get_obj_info,
    describe,
)


# ==================== Example Classes ====================

class Status(Enum):
    """User status enum."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


@dataclass
class Address:
    """Address dataclass."""
    street: str
    city: str
    country: str = "USA"
    zipcode: Optional[str] = None


@dataclass
class User:
    """User dataclass with various types."""
    id: int
    name: str
    email: str
    age: int
    status: Status = Status.PENDING
    address: Optional[Address] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    
    def greet(self) -> str:
        """Greet the user."""
        return f"Hello, {self.name}!"
    
    def is_adult(self) -> bool:
        """Check if user is an adult."""
        return self.age >= 18
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the user."""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def update_metadata(self, key: str, value: str) -> None:
        """Update user metadata."""
        self.metadata[key] = value
    
    @property
    def display_name(self) -> str:
        """Get display name."""
        return self.name.upper()
    
    @property
    def is_verified(self) -> bool:
        """Check if user is verified."""
        return self.status == Status.ACTIVE


class AdminUser(User):
    """Admin user with additional permissions."""
    
    def __init__(self, *args, permissions: List[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.permissions = permissions or []
    
    def has_permission(self, permission: str) -> bool:
        """Check if admin has a permission."""
        return permission in self.permissions or "admin" in self.permissions
    
    def grant_permission(self, permission: str) -> None:
        """Grant a permission."""
        if permission not in self.permissions:
            self.permissions.append(permission)


def log_call(func):
    """Decorator that logs function calls."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} returned: {result}")
        return result
    wrapper._log_decorator = True
    return wrapper


@log_call
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers."""
    return a + b


T = TypeVar('T')


class Container(Generic[T]):
    """Generic container class."""
    
    def __init__(self, value: T):
        self.value = value
    
    def get(self) -> T:
        return self.value


# ==================== Example Functions ====================

def example_object_introspection():
    """Example: Object introspection."""
    print("\n" + "=" * 60)
    print("Example: Object Introspection")
    print("=" * 60)
    
    user = User(
        id=1,
        name="Alice",
        email="alice@example.com",
        age=25,
        status=Status.ACTIVE,
        address=Address("123 Main St", "New York"),
        tags=["developer", "python"]
    )
    
    # Get all attributes
    print("\n1. All Public Attributes:")
    attrs = ReflectionUtils.get_all_attributes(user)
    print(f"   Found {len(attrs)} attributes")
    print(f"   Sample: {list(attrs.keys())[:5]}")
    
    # Get methods
    print("\n2. Methods:")
    methods = ReflectionUtils.get_methods(user)
    for name in sorted(methods.keys()):
        if not name.startswith('_'):
            print(f"   - {name}()")
    
    # Get properties
    print("\n3. Properties:")
    properties = ReflectionUtils.get_properties(user)
    for name in sorted(properties.keys()):
        print(f"   - {name}")
    
    # Get instance attributes
    print("\n4. Instance Attributes:")
    instance_attrs = ReflectionUtils.get_instance_attributes(user)
    print(f"   {list(instance_attrs.keys())}")


def example_function_introspection():
    """Example: Function introspection."""
    print("\n" + "=" * 60)
    print("Example: Function Introspection")
    print("=" * 60)
    
    # Analyze a function
    print("\n1. Function Info for 'calculate_sum':")
    info = ReflectionUtils.get_function_info(calculate_sum)
    print(f"   Name: {info['name']}")
    print(f"   Docstring: {info['doc']}")
    print(f"   Signature: {info['signature']}")
    print(f"   Parameters: {info['parameters']}")
    print(f"   Return annotation: {info['return_annotation']}")
    
    # Get parameters
    print("\n2. Parameter Details:")
    params = ReflectionUtils.get_parameters(calculate_sum)
    for param in params:
        print(f"   - {param['name']}: {param}")
    
    # Get return type
    print("\n3. Return Type:")
    return_type = ReflectionUtils.get_return_type(calculate_sum)
    print(f"   {return_type}")


def example_class_introspection():
    """Example: Class introspection."""
    print("\n" + "=" * 60)
    print("Example: Class Introspection")
    print("=" * 60)
    
    # Get class hierarchy
    print("\n1. AdminUser Class Hierarchy (MRO):")
    hierarchy = ReflectionUtils.get_class_hierarchy(AdminUser)
    for cls in hierarchy:
        print(f"   - {cls.__name__}")
    
    # Get base classes
    print("\n2. Direct Base Classes:")
    bases = ReflectionUtils.get_base_classes(AdminUser)
    for base in bases:
        print(f"   - {base.__name__}")
    
    # Check subclass relationship
    print("\n3. Subclass Relationships:")
    admin = AdminUser(id=1, name="Admin", email="admin@example.com", age=30)
    print(f"   AdminUser is subclass of User: {ReflectionUtils.is_subclass_of(AdminUser, User)}")
    print(f"   admin instance is subclass of User: {ReflectionUtils.is_subclass_of(admin, User)}")


def example_type_utilities():
    """Example: Type utilities."""
    print("\n" + "=" * 60)
    print("Example: Type Utilities")
    print("=" * 60)
    
    # Get type name
    print("\n1. Type Names:")
    user = User(id=1, name="Alice", email="alice@example.com", age=25)
    print(f"   User instance: {ReflectionUtils.get_type_name(user)}")
    print(f"   List: {ReflectionUtils.get_type_name([1, 2, 3])}")
    print(f"   Dict: {ReflectionUtils.get_type_name({'a': 1})}")
    
    # Check optional type
    print("\n2. Optional Type Checking:")
    print(f"   Optional[str] is Optional: {ReflectionUtils.is_optional_type(Optional[str])}")
    print(f"   str is Optional: {ReflectionUtils.is_optional_type(str)}")
    
    # Get optional inner type
    print("\n3. Extract Optional Inner Type:")
    inner = ReflectionUtils.get_optional_type(Optional[int])
    print(f"   Optional[int] inner type: {inner}")
    
    # Check generic type
    print("\n4. Generic Type Checking:")
    print(f"   List[int] is generic: {ReflectionUtils.is_generic_type(List[int])}")
    print(f"   list is generic: {ReflectionUtils.is_generic_type(list)}")


def example_dynamic_operations():
    """Example: Dynamic operations."""
    print("\n" + "=" * 60)
    print("Example: Dynamic Operations")
    print("=" * 60)
    
    user = User(id=1, name="Alice", email="alice@example.com", age=25)
    
    # Safe attribute access
    print("\n1. Safe Attribute Access:")
    print(f"   name: {ReflectionUtils.safe_getattr(user, 'name')}")
    print(f"   nonexistent (default): {ReflectionUtils.safe_getattr(user, 'nonexistent', 'N/A')}")
    
    # Safe attribute setting
    print("\n2. Safe Attribute Setting:")
    success = ReflectionUtils.safe_setattr(user, 'name', 'Bob')
    print(f"   Set name to 'Bob': {success}")
    print(f"   New name: {user.name}")
    
    # Check attribute existence
    print("\n3. Attribute Existence:")
    print(f"   Has 'name': {ReflectionUtils.has_attribute(user, 'name')}")
    print(f"   Has 'nonexistent': {ReflectionUtils.has_attribute(user, 'nonexistent')}")
    
    # Dynamic method calling
    print("\n4. Dynamic Method Calling:")
    result = ReflectionUtils.call_method(user, 'greet')
    print(f"   greet() result: {result}")
    
    ReflectionUtils.call_method(user, 'add_tag', 'admin')
    print(f"   After add_tag: {user.tags}")


def example_dataclass_utilities():
    """Example: Dataclass utilities."""
    print("\n" + "=" * 60)
    print("Example: Dataclass Utilities")
    print("=" * 60)
    
    user = User(
        id=1,
        name="Alice",
        email="alice@example.com",
        age=25,
        tags=["developer"]
    )
    
    # Check if dataclass
    print("\n1. Is Dataclass:")
    print(f"   User instance: {ReflectionUtils.is_dataclass_instance(user)}")
    print(f"   String: {ReflectionUtils.is_dataclass_instance('hello')}")
    
    # Get dataclass fields
    print("\n2. Dataclass Fields:")
    fields = ReflectionUtils.get_dataclass_fields(user)
    for f in fields:
        print(f"   - {f['name']}: type={f['type'].__name__ if hasattr(f['type'], '__name__') else f['type']}")
    
    # Convert to dict
    print("\n3. Dataclass to Dict:")
    d = ReflectionUtils.dataclass_to_dict(user)
    print(f"   {json.dumps(d, indent=2, default=str)[:200]}...")


def example_protocol_detection():
    """Example: Protocol detection."""
    print("\n" + "=" * 60)
    print("Example: Protocol Detection")
    print("=" * 60)
    
    test_objects = [
        ([1, 2, 3], "list"),
        ("hello", "string"),
        (42, "integer"),
        ({"a": 1}, "dict"),
        (lambda x: x, "lambda"),
    ]
    
    protocols = ['iterable', 'callable', 'hashable', 'sized', 'container']
    
    print("\nProtocol Support:")
    print(f"{'Object':<15} " + " ".join(f"{p:<10}" for p in protocols))
    print("-" * 70)
    
    for obj, name in test_objects:
        results = []
        for protocol in protocols:
            supported = ReflectionUtils.supports_protocol(obj, protocol)
            results.append("✓" if supported else "✗")
        print(f"{name:<15} " + " ".join(f"{r:<10}" for r in results))


def example_attribute_inspector():
    """Example: AttributeInspector usage."""
    print("\n" + "=" * 60)
    print("Example: AttributeInspector")
    print("=" * 60)
    
    user = User(
        id=1,
        name="Alice",
        email="alice@example.com",
        age=25,
        tags=["developer"]
    )
    
    # Find attributes by type
    print("\n1. Find String Attributes:")
    str_attrs = AttributeInspector.find_attributes_by_type(user, str)
    print(f"   {list(str_attrs.keys())}")
    
    print("\n2. Find Integer Attributes:")
    int_attrs = AttributeInspector.find_attributes_by_type(user, int)
    print(f"   {list(int_attrs.keys())}")
    
    # Get attribute chain
    print("\n3. Get Nested Attribute:")
    user.address = Address("123 Main St", "New York", "USA", "10001")
    zipcode = AttributeInspector.get_attribute_chain(user, 'address.zipcode')
    print(f"   user.address.zipcode: {zipcode}")
    
    # Set attribute chain
    print("\n4. Set Nested Attribute:")
    success = AttributeInspector.set_attribute_chain(user, 'address.city', 'Boston')
    print(f"   Set address.city to 'Boston': {success}")
    print(f"   New city: {user.address.city}")


def example_type_analyzer():
    """Example: TypeAnalyzer usage."""
    print("\n" + "=" * 60)
    print("Example: TypeAnalyzer")
    print("=" * 60)
    
    test_objects = [
        (User(id=1, name="A", email="a@b.com", age=25), "User instance"),
        (User, "User class"),
        (calculate_sum, "function"),
        ([1, 2, 3], "list"),
        (Color.RED, "Enum"),
    ]
    
    print("\nType Analysis:")
    for obj, description in test_objects:
        analysis = TypeAnalyzer.analyze(obj)
        print(f"\n   {description}:")
        print(f"     Type: {analysis['type_name']}")
        print(f"     Module: {analysis['module']}")
        print(f"     Is callable: {analysis['is_callable']}")
        print(f"     Is dataclass: {analysis['is_dataclass']}")
        print(f"     Is enum: {analysis['is_enum']}")


def example_describe_function():
    """Example: Using the describe function."""
    print("\n" + "=" * 60)
    print("Example: Describe Function")
    print("=" * 60)
    
    user = User(
        id=1,
        name="Alice",
        email="alice@example.com",
        age=25,
        tags=["developer", "python"]
    )
    
    print("\n" + describe(user))


def example_get_obj_info():
    """Example: Using get_obj_info."""
    print("\n" + "=" * 60)
    print("Example: get_obj_info Function")
    print("=" * 60)
    
    user = User(
        id=1,
        name="Alice",
        email="alice@example.com",
        age=25
    )
    
    info = get_obj_info(user)
    
    print("\nObject Information:")
    print(f"  Type: {info['type']}")
    print(f"  Module: {info['module']}")
    print(f"  Is callable: {info['is_callable']}")
    print(f"  Is dataclass: {info['is_dataclass']}")
    print(f"  Methods: {info['methods']}")
    print(f"  Properties: {info['properties']}")
    print(f"  Instance attrs: {info['instance_attrs']}")


def example_decorator_analysis():
    """Example: Analyzing decorated functions."""
    print("\n" + "=" * 60)
    print("Example: Decorator Analysis")
    print("=" * 60)
    
    # Get function info of decorated function
    print("\n1. Decorated Function Info:")
    info = ReflectionUtils.get_function_info(calculate_sum)
    print(f"   Name: {info['name']}")
    print(f"   Docstring: {info['doc']}")
    
    # Check for decorator marker
    print("\n2. Check for Decorator Marker:")
    has_marker = hasattr(calculate_sum, '_log_decorator')
    print(f"   Has _log_decorator: {has_marker}")


def example_special_methods():
    """Example: Special methods detection."""
    print("\n" + "=" * 60)
    print("Example: Special Methods Detection")
    print("=" * 60)
    
    # List special methods
    print("\n1. List Special Methods:")
    methods = ReflectionUtils.get_special_methods([1, 2, 3])
    for name in sorted(methods.keys())[:10]:
        print(f"   - {name}")
    print(f"   ... and {len(methods) - 10} more" if len(methods) > 10 else "")


def example_instance_creation():
    """Example: Dynamic instance creation."""
    print("\n" + "=" * 60)
    print("Example: Dynamic Instance Creation")
    print("=" * 60)
    
    # Create instance
    print("\n1. Create Instance:")
    user = ReflectionUtils.create_instance(
        User,
        id=2,
        name="Bob",
        email="bob@example.com",
        age=30
    )
    print(f"   Created: {user}")
    print(f"   Name: {user.name}, Age: {user.age}")
    
    # Get default constructor args
    print("\n2. Default Constructor Arguments:")
    defaults = ReflectionUtils.get_default_constructor_args(User)
    print(f"   {defaults}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Reflection Utils - Usage Examples")
    print("=" * 60)
    
    example_object_introspection()
    example_function_introspection()
    example_class_introspection()
    example_type_utilities()
    example_dynamic_operations()
    example_dataclass_utilities()
    example_protocol_detection()
    example_attribute_inspector()
    example_type_analyzer()
    example_describe_function()
    example_get_obj_info()
    example_decorator_analysis()
    example_special_methods()
    example_instance_creation()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()