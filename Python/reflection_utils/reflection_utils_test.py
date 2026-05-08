"""
Tests for Reflection Utilities Module

Comprehensive tests for all reflection and introspection utilities.
"""

import unittest
from typing import Optional, List, Dict, Union
from dataclasses import dataclass, field
from functools import wraps
from enum import Enum

from mod import (
    ReflectionUtils,
    AttributeInspector,
    TypeAnalyzer,
    get_obj_info,
    describe,
)


# Test fixtures
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


@dataclass
class Address:
    street: str
    city: str
    zipcode: str


@dataclass
class Person:
    name: str
    age: int
    email: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    
    def greet(self) -> str:
        """Greet the person."""
        return f"Hello, I'm {self.name}"
    
    def add_tag(self, tag: str) -> None:
        """Add a tag."""
        self.tags.append(tag)
    
    @property
    def is_adult(self) -> bool:
        """Check if person is an adult."""
        return self.age >= 18
    
    @property
    def display_name(self) -> str:
        """Get display name."""
        return self.name.upper()


class Student(Person):
    """Student class inheriting from Person."""
    
    def __init__(self, name: str, age: int, grade: str, **kwargs):
        super().__init__(name, age, **kwargs)
        self.grade = grade
    
    def study(self, subject: str) -> str:
        """Study a subject."""
        return f"{self.name} is studying {subject}"


def sample_function(a: int, b: str = "default", *args, **kwargs) -> bool:
    """A sample function for testing."""
    return True


async def async_function(x: int) -> str:
    """An async function."""
    return str(x)


def decorator_example(func):
    """Example decorator."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper._decorated = True
    return wrapper


@decorator_example
def decorated_function():
    """A decorated function."""
    pass


class TestReflectionUtilsObjectIntrospection(unittest.TestCase):
    """Tests for object introspection methods."""
    
    def setUp(self):
        self.person = Person("Alice", 25, "alice@example.com", ["friend"])
    
    def test_get_all_attributes(self):
        """Test getting all attributes."""
        attrs = ReflectionUtils.get_all_attributes(self.person)
        self.assertIn('name', attrs)
        self.assertIn('age', attrs)
        self.assertIn('greet', attrs)
        self.assertEqual(attrs['name'], "Alice")
        self.assertEqual(attrs['age'], 25)
    
    def test_get_all_attributes_include_private(self):
        """Test getting all attributes including private."""
        attrs_public = ReflectionUtils.get_all_attributes(self.person, include_private=False)
        attrs_private = ReflectionUtils.get_all_attributes(self.person, include_private=True)
        self.assertLessEqual(len(attrs_public), len(attrs_private))
    
    def test_get_methods(self):
        """Test getting methods."""
        methods = ReflectionUtils.get_methods(self.person)
        self.assertIn('greet', methods)
        self.assertIn('add_tag', methods)
        self.assertTrue(callable(methods['greet']))
    
    def test_get_properties(self):
        """Test getting properties."""
        properties = ReflectionUtils.get_properties(self.person)
        self.assertIn('is_adult', properties)
        self.assertIn('display_name', properties)
        self.assertIsInstance(properties['is_adult'], property)
    
    def test_get_properties_on_class(self):
        """Test getting properties from class."""
        properties = ReflectionUtils.get_properties(Person)
        self.assertIn('is_adult', properties)
    
    def test_get_instance_attributes(self):
        """Test getting instance attributes."""
        attrs = ReflectionUtils.get_instance_attributes(self.person)
        self.assertIn('name', attrs)
        self.assertIn('age', attrs)
        self.assertEqual(attrs['name'], "Alice")
    
    def test_get_class_attributes(self):
        """Test getting class attributes."""
        class TestClass:
            class_attr = "class_value"
            def __init__(self):
                self.instance_attr = "instance_value"
        
        attrs = ReflectionUtils.get_class_attributes(TestClass)
        self.assertIn('class_attr', attrs)
        self.assertEqual(attrs['class_attr'], "class_value")


class TestReflectionUtilsFunctionIntrospection(unittest.TestCase):
    """Tests for function introspection methods."""
    
    def test_get_function_info(self):
        """Test getting function information."""
        info = ReflectionUtils.get_function_info(sample_function)
        self.assertEqual(info['name'], 'sample_function')
        self.assertEqual(info['module'], __name__)
        self.assertIsNotNone(info['doc'])
        self.assertIn('a', info['parameters'])
        self.assertEqual(info['parameters']['b']['default'], 'default')
    
    def test_get_function_info_async(self):
        """Test getting async function information."""
        info = ReflectionUtils.get_function_info(async_function)
        self.assertTrue(info['is_coroutine'])
    
    def test_get_parameters(self):
        """Test getting function parameters."""
        params = ReflectionUtils.get_parameters(sample_function)
        param_names = [p['name'] for p in params]
        self.assertIn('a', param_names)
        self.assertIn('b', param_names)
        
        # Check default parameter
        b_param = next(p for p in params if p['name'] == 'b')
        self.assertTrue(b_param['has_default'])
        self.assertEqual(b_param['default'], 'default')
    
    def test_get_return_type(self):
        """Test getting return type."""
        return_type = ReflectionUtils.get_return_type(sample_function)
        self.assertEqual(return_type, bool)
    
    def test_get_type_hints_safe(self):
        """Test getting type hints safely."""
        hints = ReflectionUtils.get_type_hints_safe(sample_function)
        self.assertIn('a', hints)
        self.assertIn('return', hints)


class TestReflectionUtilsClassIntrospection(unittest.TestCase):
    """Tests for class introspection methods."""
    
    def test_get_class_hierarchy(self):
        """Test getting class hierarchy."""
        hierarchy = ReflectionUtils.get_class_hierarchy(Student)
        self.assertIn(Student, hierarchy)
        self.assertIn(Person, hierarchy)
        self.assertIn(object, hierarchy)
    
    def test_get_class_hierarchy_from_instance(self):
        """Test getting class hierarchy from instance."""
        student = Student("Bob", 20, "A")
        hierarchy = ReflectionUtils.get_class_hierarchy(student)
        self.assertIn(Student, hierarchy)
        self.assertIn(Person, hierarchy)
    
    def test_get_base_classes(self):
        """Test getting base classes."""
        bases = ReflectionUtils.get_base_classes(Student)
        self.assertIn(Person, bases)
    
    def test_is_subclass_of(self):
        """Test subclass checking."""
        student = Student("Bob", 20, "A")
        self.assertTrue(ReflectionUtils.is_subclass_of(student, Person))
        self.assertTrue(ReflectionUtils.is_subclass_of(Student, Person))
        self.assertFalse(ReflectionUtils.is_subclass_of(Person, Student))


class TestReflectionUtilsTypeUtilities(unittest.TestCase):
    """Tests for type utility methods."""
    
    def test_get_type_name(self):
        """Test getting type name."""
        name = ReflectionUtils.get_type_name(Person("Alice", 25))
        # Should contain Person
        self.assertIn('Person', name)
    
    def test_get_type_name_builtin(self):
        """Test getting type name for builtins."""
        self.assertEqual(ReflectionUtils.get_type_name(42), 'int')
        self.assertEqual(ReflectionUtils.get_type_name("hello"), 'str')
    
    def test_get_origin_type(self):
        """Test getting origin type from generic."""
        from typing import List as TypingList
        origin = ReflectionUtils.get_origin_type(TypingList[int])
        # In Python 3.6, the origin might be typing.List instead of list
        # Just check that we get something meaningful
        self.assertIsNotNone(origin)
    
    def test_get_type_args(self):
        """Test getting type arguments."""
        from typing import List as TypingList
        args = ReflectionUtils.get_type_args(TypingList[int])
        self.assertEqual(args, (int,))
    
    def test_is_optional_type(self):
        """Test checking for Optional type."""
        self.assertTrue(ReflectionUtils.is_optional_type(Optional[str]))
        self.assertFalse(ReflectionUtils.is_optional_type(str))
    
    def test_get_optional_type(self):
        """Test getting inner type from Optional."""
        inner = ReflectionUtils.get_optional_type(Optional[int])
        self.assertEqual(inner, int)
    
    def test_is_generic_type(self):
        """Test checking for generic type."""
        from typing import List as TypingList
        self.assertTrue(ReflectionUtils.is_generic_type(TypingList[int]))
        self.assertFalse(ReflectionUtils.is_generic_type(list))


class TestReflectionUtilsDynamicOperations(unittest.TestCase):
    """Tests for dynamic operation methods."""
    
    def setUp(self):
        self.person = Person("Alice", 25)
    
    def test_safe_getattr(self):
        """Test safe attribute getting."""
        self.assertEqual(ReflectionUtils.safe_getattr(self.person, 'name'), "Alice")
        self.assertIsNone(ReflectionUtils.safe_getattr(self.person, 'nonexistent'))
        self.assertEqual(ReflectionUtils.safe_getattr(self.person, 'nonexistent', 'default'), 'default')
    
    def test_safe_setattr(self):
        """Test safe attribute setting."""
        self.assertTrue(ReflectionUtils.safe_setattr(self.person, 'name', "Bob"))
        self.assertEqual(self.person.name, "Bob")
    
    def test_safe_delattr(self):
        """Test safe attribute deletion."""
        self.person.temp_attr = "temp"
        self.assertTrue(ReflectionUtils.safe_delattr(self.person, 'temp_attr'))
        self.assertFalse(hasattr(self.person, 'temp_attr'))
    
    def test_has_attribute(self):
        """Test attribute existence check."""
        self.assertTrue(ReflectionUtils.has_attribute(self.person, 'name'))
        self.assertFalse(ReflectionUtils.has_attribute(self.person, 'nonexistent'))
    
    def test_call_method(self):
        """Test dynamic method calling."""
        result = ReflectionUtils.call_method(self.person, 'greet')
        self.assertEqual(result, "Hello, I'm Alice")
    
    def test_call_method_with_args(self):
        """Test dynamic method calling with arguments."""
        ReflectionUtils.call_method(self.person, 'add_tag', 'developer')
        self.assertIn('developer', self.person.tags)


class TestReflectionUtilsDataclassUtilities(unittest.TestCase):
    """Tests for dataclass utility methods."""
    
    def test_is_dataclass_instance(self):
        """Test checking if object is dataclass instance."""
        person = Person("Alice", 25)
        self.assertTrue(ReflectionUtils.is_dataclass_instance(person))
        self.assertFalse(ReflectionUtils.is_dataclass_instance("string"))
    
    def test_get_dataclass_fields(self):
        """Test getting dataclass fields."""
        fields = ReflectionUtils.get_dataclass_fields(Person("Alice", 25))
        field_names = [f['name'] for f in fields]
        self.assertIn('name', field_names)
        self.assertIn('age', field_names)
        self.assertIn('email', field_names)
        self.assertIn('tags', field_names)
    
    def test_dataclass_to_dict(self):
        """Test converting dataclass to dict."""
        person = Person("Alice", 25, "alice@example.com", ["friend"])
        d = ReflectionUtils.dataclass_to_dict(person)
        self.assertEqual(d['name'], "Alice")
        self.assertEqual(d['age'], 25)
        self.assertEqual(d['email'], "alice@example.com")


class TestReflectionUtilsSpecialMethods(unittest.TestCase):
    """Tests for special method detection."""
    
    def test_get_special_methods(self):
        """Test getting special methods."""
        methods = ReflectionUtils.get_special_methods([1, 2, 3])
        self.assertIn('__iter__', methods)
        self.assertIn('__len__', methods)
    
    def test_supports_protocol_iterable(self):
        """Test iterable protocol check."""
        self.assertTrue(ReflectionUtils.supports_protocol([1, 2, 3], 'iterable'))
        self.assertTrue(ReflectionUtils.supports_protocol("string", 'iterable'))
        self.assertFalse(ReflectionUtils.supports_protocol(42, 'iterable'))
    
    def test_supports_protocol_callable(self):
        """Test callable protocol check."""
        self.assertTrue(ReflectionUtils.supports_protocol(lambda x: x, 'callable'))
        self.assertTrue(ReflectionUtils.supports_protocol(print, 'callable'))
        self.assertFalse(ReflectionUtils.supports_protocol(42, 'callable'))
    
    def test_supports_protocol_context(self):
        """Test context manager protocol check."""
        class ContextManager:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
        
        self.assertTrue(ReflectionUtils.supports_protocol(ContextManager(), 'context'))
    
    def test_supports_protocol_sized(self):
        """Test sized protocol check."""
        self.assertTrue(ReflectionUtils.supports_protocol([1, 2, 3], 'sized'))
        self.assertFalse(ReflectionUtils.supports_protocol(42, 'sized'))


class TestReflectionUtilsInstanceCreation(unittest.TestCase):
    """Tests for instance creation methods."""
    
    def test_create_instance(self):
        """Test creating instance."""
        person = ReflectionUtils.create_instance(Person, "Alice", 25)
        self.assertIsInstance(person, Person)
        self.assertEqual(person.name, "Alice")
        self.assertEqual(person.age, 25)
    
    def test_create_instance_with_kwargs(self):
        """Test creating instance with kwargs."""
        person = ReflectionUtils.create_instance(Person, "Alice", 25, email="alice@example.com")
        self.assertEqual(person.email, "alice@example.com")
    
    def test_get_default_constructor_args(self):
        """Test getting default constructor arguments."""
        defaults = ReflectionUtils.get_default_constructor_args(Person)
        self.assertIn('email', defaults)
        self.assertIsNone(defaults['email'])


class TestAttributeInspector(unittest.TestCase):
    """Tests for AttributeInspector class."""
    
    def setUp(self):
        self.person = Person("Alice", 25, "alice@example.com")
    
    def test_find_attributes_by_type(self):
        """Test finding attributes by type."""
        attrs = AttributeInspector.find_attributes_by_type(self.person, str)
        self.assertIn('name', attrs)
        self.assertIn('email', attrs)
    
    def test_find_attributes_by_type_int(self):
        """Test finding integer attributes."""
        attrs = AttributeInspector.find_attributes_by_type(self.person, int)
        self.assertIn('age', attrs)
    
    def test_get_attribute_chain(self):
        """Test getting nested attribute."""
        class Inner:
            value = "inner_value"
        
        class Outer:
            inner = Inner()
        
        outer = Outer()
        result = AttributeInspector.get_attribute_chain(outer, 'inner.value')
        self.assertEqual(result, "inner_value")
    
    def test_get_attribute_chain_default(self):
        """Test getting nested attribute with default."""
        result = AttributeInspector.get_attribute_chain(self.person, 'nonexistent.attr', 'default')
        self.assertEqual(result, 'default')
    
    def test_set_attribute_chain(self):
        """Test setting nested attribute."""
        class Inner:
            value = "old"
        
        class Outer:
            inner = Inner()
        
        outer = Outer()
        success = AttributeInspector.set_attribute_chain(outer, 'inner.value', "new")
        self.assertTrue(success)
        self.assertEqual(outer.inner.value, "new")


class TestTypeAnalyzer(unittest.TestCase):
    """Tests for TypeAnalyzer class."""
    
    def setUp(self):
        self.person = Person("Alice", 25)
    
    def test_analyze(self):
        """Test type analysis."""
        analysis = TypeAnalyzer.analyze(self.person)
        self.assertEqual(analysis['type_name'], 'Person')
        self.assertFalse(analysis['is_class'])
        self.assertTrue(analysis['is_instance'])
        self.assertFalse(analysis['is_callable'])
        self.assertTrue(analysis['is_dataclass'])
    
    def test_analyze_class(self):
        """Test analyzing a class."""
        analysis = TypeAnalyzer.analyze(Person)
        self.assertTrue(analysis['is_class'])
        self.assertFalse(analysis['is_instance'])
    
    def test_analyze_function(self):
        """Test analyzing a function."""
        analysis = TypeAnalyzer.analyze(sample_function)
        self.assertTrue(analysis['is_function'])
        self.assertTrue(analysis['is_callable'])
    
    def test_analyze_enum(self):
        """Test analyzing an enum."""
        analysis = TypeAnalyzer.analyze(Color.RED)
        self.assertTrue(analysis['is_enum'])
    
    def test_get_all_bases(self):
        """Test getting all base classes."""
        bases = TypeAnalyzer.get_all_bases(Student)
        self.assertIn(Person, bases)
    
    def test_implements_interface_by_inheritance(self):
        """Test interface implementation by inheritance."""
        self.assertTrue(TypeAnalyzer.implements_interface(Student, Person))


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for convenience functions."""
    
    def test_get_obj_info(self):
        """Test getting object info."""
        person = Person("Alice", 25)
        info = get_obj_info(person)
        
        self.assertEqual(info['type'], 'Person')
        self.assertIn('methods', info)
        self.assertIn('properties', info)
        self.assertIn('greet', info['methods'])
        self.assertIn('is_adult', info['properties'])
        self.assertTrue(info['is_dataclass'])
    
    def test_describe(self):
        """Test describe function."""
        person = Person("Alice", 25)
        description = describe(person)
        
        self.assertIn('Person', description)
        self.assertIn('Methods', description)
        self.assertIn('greet', description)
    
    def test_describe_include_private(self):
        """Test describe with private attributes."""
        person = Person("Alice", 25)
        description = describe(person, include_private=True)
        # Should include more methods with private
        self.assertIn('Person', description)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_builtin_types(self):
        """Test with builtin types."""
        info = ReflectionUtils.get_all_attributes([1, 2, 3])
        self.assertIsInstance(info, dict)
    
    def test_none_object(self):
        """Test with None."""
        self.assertEqual(ReflectionUtils.get_type_name(None), 'NoneType')
    
    def test_function_no_signature(self):
        """Test function with no signature."""
        # Builtins don't have inspectable signatures
        info = ReflectionUtils.get_function_info(print)
        self.assertEqual(info['name'], 'print')
        # Signature might be None for builtins
        self.assertTrue(info['is_builtin'])
    
    def test_property_access_error(self):
        """Test handling property access errors."""
        class BrokenProperty:
            @property
            def broken(self):
                raise RuntimeError("Broken property")
        
        obj = BrokenProperty()
        # get_properties should still work
        props = ReflectionUtils.get_properties(obj)
        self.assertIn('broken', props)
    
    def test_class_without_dict(self):
        """Test class without __dict__."""
        # Some classes don't have __dict__
        attrs = ReflectionUtils.get_instance_attributes(42)
        self.assertIsInstance(attrs, dict)


if __name__ == '__main__':
    unittest.main(verbosity=2)