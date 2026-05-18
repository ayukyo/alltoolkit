"""
AllToolkit - Python Deep Clone Utilities

A zero-dependency, production-ready deep cloning utility module.
Supports deep copying of complex nested data structures including
custom objects, circular references, and special Python types.

Author: AllToolkit
License: MIT
"""

import copy
import types
from typing import Any, Dict, Set, List, Tuple, Optional, Callable, TypeVar, Pattern
from collections import deque, defaultdict, OrderedDict, Counter, namedtuple
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from fractions import Fraction
from functools import partial
import re

# For Python 3.6 compatibility
try:
    RE_PATTERN_TYPE = re.Pattern
except AttributeError:
    RE_PATTERN_TYPE = type(re.compile(''))

T = TypeVar('T')

# Types that should NOT be deep cloned (immutable built-ins)
_IMMUTABLE_TYPES = (
    type(None), bool, int, float, complex, str, bytes,
    type, range, slice, frozenset,
    type(Ellipsis), type(NotImplemented),
)

# Types that can be safely shallow copied
_SHALLOW_COPYABLE = (
    bytearray, memoryview,
)


class CloneError(Exception):
    """Exception raised when cloning fails."""
    pass


class CloneConfig:
    """Configuration options for deep cloning."""
    
    def __init__(
        self,
        preserve_singletons: bool = True,
        copy_functions: bool = False,
        copy_classes: bool = False,
        copy_modules: bool = False,
        max_depth: Optional[int] = None,
        custom_handlers: Optional[Dict[type, Callable]] = None,
        memo: Optional[Dict[int, Any]] = None,
    ):
        """
        Initialize clone configuration.
        
        Args:
            preserve_singletons: Keep singleton objects as-is (True)
            copy_functions: Whether to deep copy functions (False)
            copy_classes: Whether to deep copy class objects (False)
            copy_modules: Whether to deep copy module objects (False)
            max_depth: Maximum depth for recursive cloning (None = unlimited)
            custom_handlers: Dict mapping types to custom clone handlers
            memo: Internal memo dict for handling circular references
        """
        self.preserve_singletons = preserve_singletons
        self.copy_functions = copy_functions
        self.copy_classes = copy_classes
        self.copy_modules = copy_modules
        self.max_depth = max_depth
        self.custom_handlers = custom_handlers or {}
        self.memo = memo if memo is not None else {}


# Singleton pattern for default config
DEFAULT_CONFIG = CloneConfig()


def _get_object_id(obj: Any) -> int:
    """Get object id, handling special cases."""
    return id(obj)


def _is_immutable(obj: Any) -> bool:
    """Check if an object is immutable and doesn't need deep cloning."""
    return isinstance(obj, _IMMUTABLE_TYPES)


def _clone_tuple(obj: tuple, config: CloneConfig, depth: int) -> tuple:
    """Clone a tuple, potentially preserving immutability."""
    # Empty or single-element tuples with immutable elements
    if not obj:
        return ()
    
    # Check if all elements are immutable
    try:
        for item in obj:
            if not _is_immutable(item):
                raise TypeError
        return obj  # Return original if all elements immutable
    except TypeError:
        pass
    
    # Deep clone elements
    cloned = tuple(deep_clone(item, config, depth + 1) for item in obj)
    
    # Check for namedtuple
    if hasattr(obj, '_fields'):
        return type(obj)(*cloned)
    
    return cloned


def _clone_list(obj: list, config: CloneConfig, depth: int) -> list:
    """Clone a list with deep cloning of elements."""
    return [deep_clone(item, config, depth) for item in obj]


def _clone_dict(obj: dict, config: CloneConfig, depth: int) -> dict:
    """Clone a dict with deep cloning of keys and values."""
    # Handle dict subclasses
    original_class = type(obj)
    
    if original_class is dict:
        return {
            deep_clone(k, config, depth + 1): deep_clone(v, config, depth + 1)
            for k, v in obj.items()
        }
    elif original_class is OrderedDict:
        return OrderedDict(
            (deep_clone(k, config, depth + 1), deep_clone(v, config, depth + 1))
            for k, v in obj.items()
        )
    elif original_class is defaultdict:
        cloned = defaultdict(
            obj.default_factory,
            (
                (deep_clone(k, config, depth + 1), deep_clone(v, config, depth + 1))
                for k, v in obj.items()
            )
        )
        return cloned
    elif original_class is Counter:
        return Counter({
            deep_clone(k, config, depth + 1): deep_clone(v, config, depth + 1)
            for k, v in obj.items()
        })
    else:
        # Generic dict subclass
        try:
            cloned = original_class()
            for k, v in obj.items():
                cloned[deep_clone(k, config, depth + 1)] = deep_clone(v, config, depth + 1)
            return cloned
        except TypeError:
            # Fall back to regular dict if subclass doesn't support it
            return {
                deep_clone(k, config, depth + 1): deep_clone(v, config, depth + 1)
                for k, v in obj.items()
            }


def _clone_set(obj: set, config: CloneConfig, depth: int) -> set:
    """Clone a set with deep cloning of elements."""
    original_class = type(obj)
    
    if original_class is set:
        return {deep_clone(item, config, depth + 1) for item in obj}
    elif original_class is frozenset:
        # frozenset is immutable, but elements might not be
        try:
            for item in obj:
                if not _is_immutable(item):
                    raise TypeError
            return obj  # Return original if all elements immutable
        except TypeError:
            return frozenset(deep_clone(item, config, depth + 1) for item in obj)
    else:
        # Handle set subclasses
        try:
            return original_class(deep_clone(item, config, depth + 1) for item in obj)
        except TypeError:
            return {deep_clone(item, config, depth + 1) for item in obj}


def _clone_deque(obj: deque, config: CloneConfig, depth: int) -> deque:
    """Clone a deque with deep cloning of elements."""
    return deque(
        (deep_clone(item, config, depth + 1) for item in obj),
        maxlen=obj.maxlen
    )


def _clone_datetime(obj: Any, config: CloneConfig, depth: int) -> Any:
    """Clone datetime objects."""
    # datetime objects are immutable, return as-is
    return obj


def _clone_decimal(obj: Decimal, config: CloneConfig, depth: int) -> Decimal:
    """Clone Decimal objects."""
    # Decimal is immutable, but let's create a copy for safety
    return Decimal(str(obj))


def _clone_fraction(obj: Fraction, config: CloneConfig, depth: int) -> Fraction:
    """Clone Fraction objects."""
    # Fraction is immutable, return as-is
    return obj


def _clone_re_pattern(obj: Any, config: CloneConfig, depth: int) -> Any:
    """Clone compiled regex patterns."""
    # Recompile the pattern
    return re.compile(obj.pattern, obj.flags)


def _clone_function(obj: Callable, config: CloneConfig, depth: int) -> Callable:
    """Clone function objects (shallow copy by default)."""
    if not config.copy_functions:
        return obj  # Functions are usually shared by reference
    
    # For lambda and regular functions, we can try to create a new function
    # with the same code object and closure
    try:
        return types.FunctionType(
            obj.__code__,
            obj.__globals__,
            name=obj.__name__,
            argdefs=obj.__defaults__,
            closure=obj.__closure__
        )
    except (TypeError, AttributeError):
        return obj


def _clone_object(obj: Any, config: CloneConfig, depth: int) -> Any:
    """Clone arbitrary objects using __dict__ or __slots__."""
    original_class = type(obj)
    
    # Try to create a new instance
    try:
        # First, try to create an empty instance
        cloned = object.__new__(original_class)
    except TypeError:
        # Can't create instance without __new__
        return obj
    
    # Register in memo before copying attributes to handle circular refs
    obj_id = _get_object_id(obj)
    config.memo[obj_id] = cloned
    
    # Copy __dict__ if present
    if hasattr(obj, '__dict__'):
        cloned_dict = {}
        for k, v in obj.__dict__.items():
            cloned_dict[k] = deep_clone(v, config, depth + 1)
        try:
            cloned.__dict__ = cloned_dict
        except AttributeError:
            pass  # Read-only __dict__
    
    # Copy __slots__ if present
    for cls in original_class.__mro__:
        if hasattr(cls, '__slots__'):
            for slot in cls.__slots__:
                if slot == '__dict__':
                    continue
                if slot == '__weakref__':
                    continue
                if hasattr(obj, slot):
                    try:
                        setattr(cloned, slot, deep_clone(getattr(obj, slot), config, depth + 1))
                    except AttributeError:
                        pass  # Read-only slot
    
    return cloned


def deep_clone(obj: T, config: Optional[CloneConfig] = None, depth: int = 0) -> T:
    """
    Deep clone an object recursively.
    
    Creates a completely independent copy of the object and all nested
    objects, handling circular references and various Python types.
    
    Args:
        obj: The object to clone
        config: CloneConfig with options (uses defaults if None)
        depth: Current recursion depth (internal use)
    
    Returns:
        A deep copy of the object
    
    Raises:
        CloneError: If cloning fails
        RecursionError: If max_depth is exceeded
    
    Example:
        >>> data = {'a': [1, 2, 3], 'b': {'c': 4}}
        >>> cloned = deep_clone(data)
        >>> cloned['a'].append(4)
        >>> data['a']  # Original unchanged
        [1, 2, 3]
    """
    if config is None:
        config = CloneConfig()  # Create fresh config for each call
    
    # Check depth limit
    if config.max_depth is not None and depth > config.max_depth:
        raise CloneError(f"Maximum clone depth {config.max_depth} exceeded")
    
    # Handle None and immutable types
    if obj is None or isinstance(obj, (type(None), bool, int, float, complex, str, bytes, type, range, slice)):
        return obj
    
    # Handle Ellipsis and NotImplemented
    if obj is Ellipsis or obj is NotImplemented:
        return obj
    
    # Check for circular reference
    obj_id = _get_object_id(obj)
    if obj_id in config.memo:
        return config.memo[obj_id]
    
    # Check custom handlers first
    obj_type = type(obj)
    if obj_type in config.custom_handlers:
        config.memo[obj_id] = obj  # Register before handler to avoid infinite recursion
        return config.custom_handlers[obj_type](obj, config, depth)
    
    # Handle tuple (including namedtuple)
    if isinstance(obj, tuple):
        cloned = _clone_tuple(obj, config, depth)
        config.memo[obj_id] = cloned
        return cloned
    
    # Handle list
    if isinstance(obj, list):
        # Create placeholder list and register before populating to handle circular refs
        placeholder = []
        config.memo[obj_id] = placeholder
        # Populate placeholder by cloning each element
        for item in obj:
            placeholder.append(deep_clone(item, config, depth + 1))
        return placeholder
    
    # Handle dict and dict subclasses
    if isinstance(obj, dict):
        # Create placeholder dict and register before populating to handle circular refs
        placeholder = {}
        config.memo[obj_id] = placeholder
        # Populate placeholder by cloning each key-value pair
        for k, v in obj.items():
            placeholder[deep_clone(k, config, depth + 1)] = deep_clone(v, config, depth + 1)
        # Handle dict subclasses
        original_class = type(obj)
        if original_class is not dict:
            try:
                converted = original_class()
                for k, v in placeholder.items():
                    converted[k] = v
                if original_class is OrderedDict:
                    converted = OrderedDict(placeholder.items())
                elif original_class is defaultdict:
                    converted = defaultdict(obj.default_factory, placeholder.items())
                elif original_class is Counter:
                    converted = Counter(placeholder)
                placeholder = converted
            except TypeError:
                pass  # Keep as regular dict
        return placeholder
    
    # Handle set and frozenset
    if isinstance(obj, (set, frozenset)):
        config.memo[obj_id] = obj
        cloned = _clone_set(obj, config, depth)
        config.memo[obj_id] = cloned
        return cloned
    
    # Handle deque
    if isinstance(obj, deque):
        config.memo[obj_id] = obj
        cloned = _clone_deque(obj, config, depth)
        config.memo[obj_id] = cloned
        return cloned
    
    # Handle datetime objects (immutable)
    if isinstance(obj, (datetime, date, time, timedelta)):
        return obj
    
    # Handle Decimal
    if isinstance(obj, Decimal):
        return _clone_decimal(obj, config, depth)
    
    # Handle Fraction
    if isinstance(obj, Fraction):
        return obj
    
    # Handle compiled regex patterns
    if isinstance(obj, RE_PATTERN_TYPE):
        return _clone_re_pattern(obj, config, depth)
    
    # Handle functions and lambdas
    if isinstance(obj, types.FunctionType):
        if config.copy_functions:
            return _clone_function(obj, config, depth)
        return obj
    
    # Handle methods (bound, unbound, class method, static method)
    if isinstance(obj, (types.MethodType, types.BuiltinFunctionType, types.BuiltinMethodType)):
        return obj
    
    # Handle classes
    if isinstance(obj, type):
        if config.copy_classes:
            return obj  # Class copying is complex and rarely needed
        return obj
    
    # Handle modules
    if isinstance(obj, types.ModuleType):
        if config.copy_modules:
            return obj
        return obj
    
    # Handle bytearray
    if isinstance(obj, bytearray):
        return bytearray(obj)
    
    # Handle memoryview
    if isinstance(obj, memoryview):
        return memoryview(bytes(obj))
    
    # Handle generators (can't be cloned)
    if isinstance(obj, types.GeneratorType):
        return obj  # Return as-is, can't clone
    
    # Handle other objects with __dict__ or __slots__
    if hasattr(obj, '__dict__') or hasattr(type(obj), '__slots__'):
        config.memo[obj_id] = obj
        cloned = _clone_object(obj, config, depth)
        config.memo[obj_id] = cloned
        return cloned
    
    # Fallback: try copy.copy
    try:
        return copy.copy(obj)
    except Exception:
        # Last resort: return as-is
        return obj


# Convenience functions

def clone(obj: T, **kwargs) -> T:
    """
    Shorthand for deep_clone with optional configuration.
    
    Args:
        obj: Object to clone
        **kwargs: CloneConfig options (max_depth, copy_functions, etc.)
    
    Returns:
        Deep cloned copy of obj
    
    Example:
        >>> data = {'nested': {'value': 1}}
        >>> cloned = clone(data)
    """
    if kwargs:
        config = CloneConfig(**kwargs)
        return deep_clone(obj, config)
    return deep_clone(obj)


def shallow_clone(obj: T) -> T:
    """
    Create a shallow copy of an object.
    
    Args:
        obj: Object to shallow copy
    
    Returns:
        Shallow copy of obj
    
    Example:
        >>> data = {'nested': {'value': 1}}
        >>> cloned = shallow_clone(data)
        >>> cloned['nested']['value'] = 2
        >>> data['nested']['value']  # Also changed!
        2
    """
    return copy.copy(obj)


def clone_with_depth(obj: T, max_depth: int) -> T:
    """
    Deep clone with a maximum depth limit.
    
    Args:
        obj: Object to clone
        max_depth: Maximum depth for recursive cloning
    
    Returns:
        Deep cloned copy of obj
    
    Example:
        >>> data = {'a': {'b': {'c': {'d': 1}}}}
        >>> cloned = clone_with_depth(data, max_depth=2)
    """
    config = CloneConfig(max_depth=max_depth)
    return deep_clone(obj, config)


def clone_without_functions(obj: T) -> T:
    """
    Deep clone preserving function references (not copying functions).
    
    Args:
        obj: Object to clone
    
    Returns:
        Deep cloned copy with function references preserved
    
    Example:
        >>> def my_func(): pass
        >>> data = {'func': my_func}
        >>> cloned = clone_without_functions(data)
        >>> cloned['func'] is my_func
        True
    """
    config = CloneConfig(copy_functions=False)
    return deep_clone(obj, config)


def clone_with_custom_handlers(obj: T, handlers: Dict[type, Callable]) -> T:
    """
    Deep clone with custom handlers for specific types.
    
    Args:
        obj: Object to clone
        handlers: Dict mapping types to custom clone functions
    
    Returns:
        Deep cloned copy with custom type handling
    
    Example:
        >>> class MyClass:
        ...     def __init__(self, value):
        ...         self.value = value
        >>> def my_handler(obj, config, depth):
        ...     return MyClass(obj.value * 2)
        >>> data = MyClass(5)
        >>> cloned = clone_with_custom_handlers(data, {MyClass: my_handler})
        >>> cloned.value
        10
    """
    config = CloneConfig(custom_handlers=handlers)
    return deep_clone(obj, config)


def is_deep_equal(a: Any, b: Any) -> bool:
    """
    Deep equality comparison for complex objects.
    
    Args:
        a: First object
        b: Second object
    
    Returns:
        True if objects are deeply equal
    
    Example:
        >>> is_deep_equal({'a': [1, 2]}, {'a': [1, 2]})
        True
        >>> is_deep_equal({'a': [1, 2]}, {'a': [1, 3]})
        False
    """
    # Fast path for same object
    if a is b:
        return True
    
    # Handle None
    if a is None or b is None:
        return a is b
    
    # Check types
    if type(a) != type(b):
        return False
    
    # Handle primitives
    if isinstance(a, (bool, int, float, complex, str, bytes)):
        return a == b
    
    # Handle tuples
    if isinstance(a, tuple):
        if len(a) != len(b):
            return False
        return all(is_deep_equal(x, y) for x, y in zip(a, b))
    
    # Handle lists
    if isinstance(a, list):
        if len(a) != len(b):
            return False
        return all(is_deep_equal(x, y) for x, y in zip(a, b))
    
    # Handle sets
    if isinstance(a, (set, frozenset)):
        if len(a) != len(b):
            return False
        # For sets with unhashable items, we need special handling
        try:
            return a == b
        except TypeError:
            # Convert to lists and compare
            return is_deep_equal(sorted(a, key=lambda x: str(x)), sorted(b, key=lambda x: str(x)))
    
    # Handle dicts
    if isinstance(a, dict):
        if set(a.keys()) != set(b.keys()):
            return False
        return all(is_deep_equal(a[k], b[k]) for k in a.keys())
    
    # Handle datetime
    if isinstance(a, (datetime, date, time, timedelta)):
        return a == b
    
    # Handle Decimal and Fraction
    if isinstance(a, (Decimal, Fraction)):
        return a == b
    
    # Handle regex patterns
    if isinstance(a, RE_PATTERN_TYPE):
        return a.pattern == b.pattern and a.flags == b.flags
    
    # Handle deque
    if isinstance(a, deque):
        if len(a) != len(b) or a.maxlen != b.maxlen:
            return False
        return all(is_deep_equal(x, y) for x, y in zip(a, b))
    
    # Handle objects with __dict__
    if hasattr(a, '__dict__') and hasattr(b, '__dict__'):
        return is_deep_equal(a.__dict__, b.__dict__)
    
    # Handle objects with __slots__
    if hasattr(type(a), '__slots__'):
        for slot in type(a).__slots__:
            if slot in ('__dict__', '__weakref__'):
                continue
            if hasattr(a, slot) != hasattr(b, slot):
                return False
            if hasattr(a, slot) and not is_deep_equal(getattr(a, slot), getattr(b, slot)):
                return False
        return True
    
    # Fallback to ==
    try:
        return a == b
    except Exception:
        return False


def clone_structure(template: Any, fill_value: Any = None) -> Any:
    """
    Clone the structure of a nested object without values.
    
    Creates a new object with the same structure but all leaf values
    replaced by fill_value.
    
    Args:
        template: Object to clone structure from
        fill_value: Value to fill at leaf positions
    
    Returns:
        New object with same structure but filled values
    
    Example:
        >>> template = {'a': [1, 2], 'b': {'c': 3}}
        >>> clone_structure(template, fill_value=0)
        {'a': [0, 0], 'b': {'c': 0}}
    """
    if isinstance(template, dict):
        return {k: clone_structure(v, fill_value) for k, v in template.items()}
    elif isinstance(template, list):
        return [clone_structure(item, fill_value) for item in template]
    elif isinstance(template, tuple):
        # Handle namedtuple
        if hasattr(template, '_fields'):
            return type(template)(*[clone_structure(item, fill_value) for item in template])
        return tuple(clone_structure(item, fill_value) for item in template)
    elif isinstance(template, set):
        return set()  # Can't clone structure of set
    elif isinstance(template, frozenset):
        return frozenset()  # Can't clone structure of frozenset
    else:
        return fill_value


# Main class for object-oriented interface
class DeepClone:
    """
    Object-oriented interface for deep cloning.
    
    Example:
        >>> cloner = DeepClone(max_depth=5)
        >>> cloned = cloner.clone({'nested': {'value': 1}})
    """
    
    def __init__(self, **kwargs):
        """
        Initialize DeepClone with configuration options.
        
        Args:
            **kwargs: CloneConfig options
        """
        self.config = CloneConfig(**kwargs)
    
    def clone(self, obj: T) -> T:
        """
        Deep clone an object using this instance's configuration.
        
        Args:
            obj: Object to clone
        
        Returns:
            Deep cloned copy
        """
        # Reset memo for each clone operation
        self.config.memo = {}
        return deep_clone(obj, self.config)
    
    def __call__(self, obj: T) -> T:
        """Allow using DeepClone instance as a callable."""
        return self.clone(obj)


# Exports
__all__ = [
    'deep_clone',
    'clone',
    'shallow_clone',
    'clone_with_depth',
    'clone_without_functions',
    'clone_with_custom_handlers',
    'is_deep_equal',
    'clone_structure',
    'CloneConfig',
    'CloneError',
    'DeepClone',
]