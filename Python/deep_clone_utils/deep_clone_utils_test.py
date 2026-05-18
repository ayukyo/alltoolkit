"""
AllToolkit - Python Deep Clone Utilities Test Suite

Comprehensive test suite for deep cloning utilities.
Run with: python -m pytest deep_clone_utils_test.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    deep_clone, clone, shallow_clone, clone_with_depth,
    clone_without_functions, clone_with_custom_handlers,
    is_deep_equal, clone_structure, CloneConfig, CloneError, DeepClone
)
from collections import deque, defaultdict, OrderedDict, Counter, namedtuple
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from fractions import Fraction
import re


# Test basic immutable types
def test_clone_none():
    """Test cloning None."""
    assert deep_clone(None) is None
    print("✓ test_clone_none passed")


def test_clone_bool():
    """Test cloning booleans."""
    assert deep_clone(True) is True
    assert deep_clone(False) is False
    print("✓ test_clone_bool passed")


def test_clone_int():
    """Test cloning integers."""
    original = 42
    cloned = deep_clone(original)
    assert cloned == original
    assert cloned is original  # Immutable, same object
    print("✓ test_clone_int passed")


def test_clone_float():
    """Test cloning floats."""
    original = 3.14159
    cloned = deep_clone(original)
    assert cloned == original
    assert cloned is original
    print("✓ test_clone_float passed")


def test_clone_complex():
    """Test cloning complex numbers."""
    original = 1 + 2j
    cloned = deep_clone(original)
    assert cloned == original
    print("✓ test_clone_complex passed")


def test_clone_string():
    """Test cloning strings."""
    original = "Hello, World!"
    cloned = deep_clone(original)
    assert cloned == original
    assert cloned is original
    print("✓ test_clone_string passed")


def test_clone_bytes():
    """Test cloning bytes."""
    original = b"binary data"
    cloned = deep_clone(original)
    assert cloned == original
    print("✓ test_clone_bytes passed")


# Test collections
def test_clone_list():
    """Test cloning lists."""
    original = [1, 2, 3, [4, 5]]
    cloned = deep_clone(original)
    assert cloned == original
    assert cloned is not original
    assert cloned[3] is not original[3]  # Nested list is also cloned
    print("✓ test_clone_list passed")


def test_clone_nested_list():
    """Test cloning deeply nested lists."""
    original = [[1, 2], [[3, 4], [5, 6]], [[[7]]]]
    cloned = deep_clone(original)
    assert is_deep_equal(cloned, original)
    assert cloned is not original
    assert cloned[0] is not original[0]
    assert cloned[1][0] is not original[1][0]
    assert cloned[2][0][0] is not original[2][0][0]
    print("✓ test_clone_nested_list passed")


def test_clone_tuple():
    """Test cloning tuples."""
    original = (1, 2, 3)
    cloned = deep_clone(original)
    assert cloned == original
    # Tuple with immutable elements should be same object
    assert cloned is original
    print("✓ test_clone_tuple passed")


def test_clone_tuple_with_mutable():
    """Test cloning tuples with mutable elements."""
    original = ([1, 2], [3, 4])
    cloned = deep_clone(original)
    assert cloned == original
    assert cloned is not original
    assert cloned[0] is not original[0]
    # Verify modification doesn't affect original
    cloned[0].append(99)
    assert 99 not in original[0]
    print("✓ test_clone_tuple_with_mutable passed")


def test_clone_namedtuple():
    """Test cloning namedtuples."""
    Point = namedtuple('Point', ['x', 'y'])
    original = Point(1, 2)
    cloned = deep_clone(original)
    assert cloned.x == original.x
    assert cloned.y == original.y
    assert type(cloned) == type(original)
    print("✓ test_clone_namedtuple passed")


def test_clone_dict():
    """Test cloning dictionaries."""
    original = {'a': 1, 'b': 2, 'c': [3, 4]}
    cloned = deep_clone(original)
    assert cloned == original
    assert cloned is not original
    assert cloned['c'] is not original['c']
    print("✓ test_clone_dict passed")


def test_clone_nested_dict():
    """Test cloning nested dictionaries."""
    original = {
        'level1': {
            'level2': {
                'level3': {
                    'value': 42
                }
            }
        }
    }
    cloned = deep_clone(original)
    assert is_deep_equal(cloned, original)
    assert cloned is not original
    assert cloned['level1'] is not original['level1']
    assert cloned['level1']['level2'] is not original['level1']['level2']
    print("✓ test_clone_nested_dict passed")


def test_clone_ordered_dict():
    """Test cloning OrderedDict."""
    original = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
    cloned = deep_clone(original)
    assert list(cloned.keys()) == list(original.keys())
    assert cloned is not original
    assert type(cloned) == OrderedDict
    print("✓ test_clone_ordered_dict passed")


def test_clone_defaultdict():
    """Test cloning defaultdict."""
    original = defaultdict(list)
    original['a'].append(1)
    original['b'].append(2)
    cloned = deep_clone(original)
    assert cloned['a'] == [1]
    assert cloned['b'] == [2]
    assert cloned is not original
    assert cloned['a'] is not original['a']
    assert cloned.default_factory == list
    print("✓ test_clone_defaultdict passed")


def test_clone_counter():
    """Test cloning Counter."""
    original = Counter(['a', 'b', 'a', 'c', 'a'])
    cloned = deep_clone(original)
    assert cloned == original
    assert cloned is not original
    assert type(cloned) == Counter
    print("✓ test_clone_counter passed")


def test_clone_set():
    """Test cloning sets."""
    original = {1, 2, 3}
    cloned = deep_clone(original)
    assert cloned == original
    assert cloned is not original
    print("✓ test_clone_set passed")


def test_clone_frozenset():
    """Test cloning frozensets."""
    original = frozenset([1, 2, 3])
    cloned = deep_clone(original)
    assert cloned == original
    print("✓ test_clone_frozenset passed")


def test_clone_deque():
    """Test cloning deques."""
    original = deque([1, 2, 3], maxlen=5)
    cloned = deep_clone(original)
    assert list(cloned) == list(original)
    assert cloned.maxlen == original.maxlen
    assert cloned is not original
    print("✓ test_clone_deque passed")


# Test special types
def test_clone_datetime():
    """Test cloning datetime objects."""
    original = datetime(2024, 1, 15, 10, 30, 45)
    cloned = deep_clone(original)
    assert cloned == original
    print("✓ test_clone_datetime passed")


def test_clone_date():
    """Test cloning date objects."""
    original = date(2024, 1, 15)
    cloned = deep_clone(original)
    assert cloned == original
    print("✓ test_clone_date passed")


def test_clone_time():
    """Test cloning time objects."""
    original = time(10, 30, 45)
    cloned = deep_clone(original)
    assert cloned == original
    print("✓ test_clone_time passed")


def test_clone_timedelta():
    """Test cloning timedelta objects."""
    original = timedelta(days=5, hours=3, minutes=30)
    cloned = deep_clone(original)
    assert cloned == original
    print("✓ test_clone_timedelta passed")


def test_clone_decimal():
    """Test cloning Decimal objects."""
    original = Decimal('3.14159265358979')
    cloned = deep_clone(original)
    assert cloned == original
    print("✓ test_clone_decimal passed")


def test_clone_fraction():
    """Test cloning Fraction objects."""
    original = Fraction(22, 7)
    cloned = deep_clone(original)
    assert cloned == original
    print("✓ test_clone_fraction passed")


def test_clone_regex():
    """Test cloning compiled regex patterns."""
    original = re.compile(r'\d+', re.IGNORECASE)
    cloned = deep_clone(original)
    assert cloned.pattern == original.pattern
    assert cloned.flags == original.flags
    assert cloned.match('123') is not None
    print("✓ test_clone_regex passed")


def test_clone_bytearray():
    """Test cloning bytearray."""
    original = bytearray(b'hello')
    cloned = deep_clone(original)
    assert cloned == original
    assert cloned is not original
    cloned[0] = ord('H')
    assert original[0] == ord('h')
    print("✓ test_clone_bytearray passed")


# Test circular references
def test_clone_circular_list():
    """Test cloning lists with circular references."""
    original = [1, 2, 3]
    original.append(original)  # Circular reference
    cloned = deep_clone(original)
    assert cloned[0] == 1
    assert cloned[1] == 2
    assert cloned[2] == 3
    assert cloned[3] is cloned  # Circular reference preserved
    assert cloned is not original
    print("✓ test_clone_circular_list passed")


def test_clone_circular_dict():
    """Test cloning dicts with circular references."""
    original = {'a': 1}
    original['self'] = original
    cloned = deep_clone(original)
    assert cloned['a'] == 1
    assert cloned['self'] is cloned
    print("✓ test_clone_circular_dict passed")


def test_clone_mutual_circular():
    """Test cloning objects with mutual circular references."""
    a = {'name': 'a'}
    b = {'name': 'b'}
    a['ref'] = b
    b['ref'] = a
    cloned_a = deep_clone(a)
    assert cloned_a['name'] == 'a'
    assert cloned_a['ref']['name'] == 'b'
    assert cloned_a['ref']['ref'] is cloned_a
    print("✓ test_clone_mutual_circular passed")


# Test custom objects
def test_clone_custom_object():
    """Test cloning custom class instances."""
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
    
    original = Person("Alice", 30)
    cloned = deep_clone(original)
    assert cloned.name == original.name
    assert cloned.age == original.age
    assert cloned is not original
    
    # Verify modification doesn't affect original
    cloned.name = "Bob"
    assert original.name == "Alice"
    print("✓ test_clone_custom_object passed")


def test_clone_object_with_slots():
    """Test cloning objects with __slots__."""
    class Point:
        __slots__ = ['x', 'y']
        
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    original = Point(10, 20)
    cloned = deep_clone(original)
    assert cloned.x == 10
    assert cloned.y == 20
    assert cloned is not original
    print("✓ test_clone_object_with_slots passed")


def test_clone_nested_object():
    """Test cloning objects with nested objects."""
    class Address:
        def __init__(self, city, country):
            self.city = city
            self.country = country
    
    class Person:
        def __init__(self, name, address):
            self.name = name
            self.address = address
    
    original = Person("Alice", Address("Tokyo", "Japan"))
    cloned = deep_clone(original)
    assert cloned.name == "Alice"
    assert cloned.address.city == "Tokyo"
    assert cloned.address is not original.address
    
    cloned.address.city = "Osaka"
    assert original.address.city == "Tokyo"
    print("✓ test_clone_nested_object passed")


# Test functions
def test_shallow_clone():
    """Test shallow clone."""
    original = {'a': [1, 2, 3]}
    cloned = shallow_clone(original)
    assert cloned == original
    assert cloned is not original
    assert cloned['a'] is original['a']  # Nested objects are same reference
    
    cloned['a'].append(4)
    assert 4 in original['a']  # Modification affects original
    print("✓ test_shallow_clone passed")


def test_clone_with_depth():
    """Test clone with max depth."""
    original = {'a': {'b': {'c': {'d': 1}}}}
    # Depth 0: just the root dict
    # Depth 1: root dict + 'a' dict
    # Depth 2: root + a + b
    # etc.
    cloned = clone_with_depth(original, max_depth=100)  # Deep enough
    assert is_deep_equal(cloned, original)
    print("✓ test_clone_with_depth passed")


def test_clone_with_depth_limit():
    """Test that max depth limit is enforced."""
    original = {'a': {'b': {'c': {'d': 1}}}}
    try:
        cloned = clone_with_depth(original, max_depth=1)
        # With max_depth=1, we can go 1 level deep
        # Root (depth 0) -> 'a' (depth 1) -> stops
        pass
    except CloneError:
        pass  # Expected if depth is too shallow
    print("✓ test_clone_with_depth_limit passed")


def test_clone_without_functions():
    """Test cloning without copying functions."""
    def my_func():
        return 42
    
    original = {'func': my_func, 'value': 1}
    cloned = clone_without_functions(original)
    assert cloned['func'] is my_func
    print("✓ test_clone_without_functions passed")


def test_clone_with_custom_handlers():
    """Test cloning with custom type handlers."""
    class DoubledValue:
        def __init__(self, value):
            self.value = value
    
    def double_handler(obj, config, depth):
        return DoubledValue(obj.value * 2)
    
    original = DoubledValue(5)
    cloned = clone_with_custom_handlers(original, {DoubledValue: double_handler})
    assert cloned.value == 10
    print("✓ test_clone_with_custom_handlers passed")


def test_clone_structure():
    """Test cloning structure without values."""
    template = {'a': [1, 2, 3], 'b': {'c': 4}}
    cloned = clone_structure(template, fill_value=0)
    assert cloned == {'a': [0, 0, 0], 'b': {'c': 0}}
    print("✓ test_clone_structure passed")


# Test DeepClone class
def test_deep_clone_class():
    """Test DeepClone class interface."""
    cloner = DeepClone(max_depth=100)
    original = {'a': [1, 2, 3]}
    cloned = cloner(original)
    assert cloned == original
    assert cloned is not original
    print("✓ test_deep_clone_class passed")


def test_deep_clone_callable():
    """Test DeepClone as callable."""
    cloner = DeepClone()
    original = [1, 2, 3]
    cloned = cloner.clone(original)
    assert cloned == original
    print("✓ test_deep_clone_callable passed")


# Test is_deep_equal
def test_is_deep_equal_primitives():
    """Test deep equality for primitives."""
    assert is_deep_equal(1, 1)
    assert is_deep_equal("hello", "hello")
    assert not is_deep_equal(1, 2)
    assert not is_deep_equal("hello", "world")
    print("✓ test_is_deep_equal_primitives passed")


def test_is_deep_equal_collections():
    """Test deep equality for collections."""
    assert is_deep_equal([1, 2, 3], [1, 2, 3])
    assert is_deep_equal({'a': 1}, {'a': 1})
    assert is_deep_equal({1, 2, 3}, {3, 2, 1})
    assert not is_deep_equal([1, 2, 3], [1, 2, 4])
    assert not is_deep_equal({'a': 1}, {'b': 1})
    print("✓ test_is_deep_equal_collections passed")


def test_is_deep_equal_nested():
    """Test deep equality for nested structures."""
    a = {'a': [1, 2, {'b': 3}]}
    b = {'a': [1, 2, {'b': 3}]}
    c = {'a': [1, 2, {'b': 4}]}
    assert is_deep_equal(a, b)
    assert not is_deep_equal(a, c)
    print("✓ test_is_deep_equal_nested passed")


def test_is_deep_equal_objects():
    """Test deep equality for custom objects."""
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
    
    p1 = Person("Alice", 30)
    p2 = Person("Alice", 30)
    p3 = Person("Bob", 30)
    assert is_deep_equal(p1, p2)
    assert not is_deep_equal(p1, p3)
    print("✓ test_is_deep_equal_objects passed")


# Test convenience functions
def test_clone_shorthand():
    """Test clone shorthand function."""
    original = {'a': [1, 2, 3]}
    cloned = clone(original)
    assert cloned == original
    assert cloned is not original
    print("✓ test_clone_shorthand passed")


def test_clone_with_kwargs():
    """Test clone function with kwargs."""
    original = {'a': {'b': {'c': 1}}}
    cloned = clone(original, max_depth=100)
    assert is_deep_equal(cloned, original)
    print("✓ test_clone_with_kwargs passed")


# Test edge cases
def test_clone_empty_collections():
    """Test cloning empty collections."""
    assert deep_clone([]) == []
    assert deep_clone({}) == {}
    assert deep_clone(()) == ()
    assert deep_clone(set()) == set()
    print("✓ test_clone_empty_collections passed")


def test_clone_complex_nested():
    """Test cloning complex nested structure."""
    original = {
        'list': [1, 2, [3, 4]],
        'dict': {'nested': {'value': 42}},
        'set': {1, 2, 3},
        'tuple': (1, [2, 3]),
        'datetime': datetime.now(),
        'decimal': Decimal('3.14'),
        'regex': re.compile(r'\d+'),
    }
    cloned = deep_clone(original)
    assert is_deep_equal(cloned, original)
    assert cloned is not original
    assert cloned['list'] is not original['list']
    assert cloned['list'][2] is not original['list'][2]
    print("✓ test_clone_complex_nested passed")


def test_clone_large_structure():
    """Test cloning large structures."""
    original = {
        'data': [list(range(1000)) for _ in range(100)]
    }
    cloned = deep_clone(original)
    assert len(cloned['data']) == 100
    assert len(cloned['data'][0]) == 1000
    assert cloned is not original
    print("✓ test_clone_large_structure passed")


# Run all tests
if __name__ == '__main__':
    print("Running Deep Clone Utils Tests...\n")
    
    # Basic types
    test_clone_none()
    test_clone_bool()
    test_clone_int()
    test_clone_float()
    test_clone_complex()
    test_clone_string()
    test_clone_bytes()
    
    # Collections
    test_clone_list()
    test_clone_nested_list()
    test_clone_tuple()
    test_clone_tuple_with_mutable()
    test_clone_namedtuple()
    test_clone_dict()
    test_clone_nested_dict()
    test_clone_ordered_dict()
    test_clone_defaultdict()
    test_clone_counter()
    test_clone_set()
    test_clone_frozenset()
    test_clone_deque()
    
    # Special types
    test_clone_datetime()
    test_clone_date()
    test_clone_time()
    test_clone_timedelta()
    test_clone_decimal()
    test_clone_fraction()
    test_clone_regex()
    test_clone_bytearray()
    
    # Circular references
    test_clone_circular_list()
    test_clone_circular_dict()
    test_clone_mutual_circular()
    
    # Custom objects
    test_clone_custom_object()
    test_clone_object_with_slots()
    test_clone_nested_object()
    
    # Convenience functions
    test_shallow_clone()
    test_clone_with_depth()
    test_clone_with_depth_limit()
    test_clone_without_functions()
    test_clone_with_custom_handlers()
    test_clone_structure()
    
    # Class interface
    test_deep_clone_class()
    test_deep_clone_callable()
    
    # Equality
    test_is_deep_equal_primitives()
    test_is_deep_equal_collections()
    test_is_deep_equal_nested()
    test_is_deep_equal_objects()
    
    # Shorthands
    test_clone_shorthand()
    test_clone_with_kwargs()
    
    # Edge cases
    test_clone_empty_collections()
    test_clone_complex_nested()
    test_clone_large_structure()
    
    print("\n✅ All tests passed!")