#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - JSON Utilities Module
====================================
A comprehensive JSON utility module for Python with zero external dependencies.

Features:
    - Safe JSON parsing with fallback values
    - JSON manipulation utilities (merge, filter, flatten)
    - Pretty printing with customizable formatting
    - JSONPath-like query support
    - Type conversion helpers

Author: AllToolkit Contributors
License: MIT
"""

import json
import os
from typing import Any, Dict, List, Optional, Union, Callable, TypeVar
from datetime import datetime, date
from decimal import Decimal
from copy import deepcopy

T = TypeVar('T')

# ============================================================================
# Safe Parsing Functions
# ============================================================================

def safe_loads(json_str: str, default: Any = None, encoding: str = 'utf-8') -> Any:
    """
    Safely parse a JSON string with a fallback default value.
    
    Args:
        json_str: The JSON string to parse
        default: The default value to return if parsing fails (default: None)
        encoding: The encoding of the string (default: 'utf-8')
    
    Returns:
        The parsed JSON object, or the default value if parsing fails
    
    Example:
        >>> safe_loads('{"name": "John"}', default={})
        {'name': 'John'}
        >>> safe_loads('invalid json', default={})
        {}
    """
    if json_str is None:
        return default
    try:
        if isinstance(json_str, bytes):
            json_str = json_str.decode(encoding)
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError, ValueError):
        return default


def safe_load(file_path: str, default: Any = None, encoding: str = 'utf-8') -> Any:
    """
    Safely load JSON from a file with a fallback default value.
    
    Args:
        file_path: Path to the JSON file
        default: The default value to return if loading fails (default: None)
        encoding: The file encoding (default: 'utf-8')
    
    Returns:
        The parsed JSON object, or the default value if loading fails
    
    Example:
        >>> safe_load('config.json', default={})
        {'setting': 'value'}
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, IOError, PermissionError):
        return default


# ============================================================================
# Serialization Functions
# ============================================================================

def dumps_compact(obj: Any, ensure_ascii: bool = False) -> str:
    """
    Serialize object to a compact JSON string (no whitespace).
    
    Args:
        obj: The object to serialize
        ensure_ascii: Whether to escape non-ASCII characters (default: False)
    
    Returns:
        A compact JSON string
    
    Example:
        >>> dumps_compact({'name': 'John', 'age': 30})
        '{"name":"John","age":30}'
    """
    return json.dumps(obj, separators=(',', ':'), ensure_ascii=ensure_ascii)


def dumps_pretty(obj: Any, indent: int = 2, ensure_ascii: bool = False, 
                 sort_keys: bool = False) -> str:
    """
    Serialize object to a pretty-printed JSON string.
    
    Args:
        obj: The object to serialize
        indent: The indentation level (default: 2)
        ensure_ascii: Whether to escape non-ASCII characters (default: False)
        sort_keys: Whether to sort dictionary keys (default: False)
    
    Returns:
        A pretty-printed JSON string
    
    Example:
        >>> print(dumps_pretty({'name': 'John', 'age': 30}))
        {
          "name": "John",
          "age": 30
        }
    """
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii, 
                      sort_keys=sort_keys, default=_json_default)


def save(obj: Any, file_path: str, indent: int = 2, ensure_ascii: bool = False,
         encoding: str = 'utf-8', sort_keys: bool = False) -> bool:
    """
    Save an object to a JSON file.
    
    Args:
        obj: The object to serialize
        file_path: Path to the output file
        indent: The indentation level (default: 2)
        ensure_ascii: Whether to escape non-ASCII characters (default: False)
        encoding: The file encoding (default: 'utf-8')
        sort_keys: Whether to sort dictionary keys (default: False)
    
    Returns:
        True if successful, False otherwise
    
    Example:
        >>> save({'config': 'value'}, 'config.json')
        True
    """
    try:
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'w', encoding=encoding) as f:
            json.dump(obj, f, indent=indent, ensure_ascii=ensure_ascii,
                     sort_keys=sort_keys, default=_json_default)
        return True
    except (IOError, PermissionError, TypeError, OSError):
        return False


def _json_default(obj: Any) -> Any:
    """Default JSON encoder for custom types."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, bytes):
        return obj.decode('utf-8', errors='replace')
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


# ============================================================================
# Query and Navigation Functions
# ============================================================================

def get_path(obj: Dict[str, Any], path: str, default: Any = None, 
             separator: str = '.') -> Any:
    """
    Get a value from a nested dictionary using a dot-separated path.
    
    Args:
        obj: The dictionary to query
        path: The dot-separated path (e.g., 'user.address.city')
        default: The default value if path not found (default: None)
        separator: The path separator (default: '.')
    
    Returns:
        The value at the path, or the default value if not found
    
    Example:
        >>> data = {'user': {'name': 'John', 'address': {'city': 'NYC'}}}
        >>> get_path(data, 'user.address.city')
        'NYC'
        >>> get_path(data, 'user.phone', 'N/A')
        'N/A'
    """
    if obj is None or not path:
        return default
    
    keys = path.split(separator)
    current = obj
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        elif isinstance(current, list) and key.isdigit():
            idx = int(key)
            if 0 <= idx < len(current):
                current = current[idx]
            else:
                return default
        else:
            return default
    
    return current


def set_path(obj: Dict[str, Any], path: str, value: Any, 
             separator: str = '.', create_intermediate: bool = True) -> bool:
    """
    Set a value in a nested dictionary using a dot-separated path.
    
    Args:
        obj: The dictionary to modify
        path: The dot-separated path (e.g., 'user.address.city')
        value: The value to set
        separator: The path separator (default: '.')
        create_intermediate: Whether to create intermediate dictionaries (default: True)
    
    Returns:
        True if successful, False otherwise
    
    Example:
        >>> data = {'user': {'name': 'John'}}
        >>> set_path(data, 'user.address.city', 'NYC')
        True
        >>> data
        {'user': {'name': 'John', 'address': {'city': 'NYC'}}}
    """
    if obj is None or not path:
        return False
    
    keys = path.split(separator)
    current = obj
    
    for i, key in enumerate(keys[:-1]):
        if key not in current:
            if not create_intermediate:
                return False
            current[key] = {}
        current = current[key]
        if not isinstance(current, dict):
            return False
    
    current[keys[-1]] = value
    return True


def has_path(obj: Dict[str, Any], path: str, separator: str = '.') -> bool:
    """
    Check if a path exists in a nested dictionary.
    
    Args:
        obj: The dictionary to check
        path: The dot-separated path
        separator: The path separator (default: '.')
    
    Returns:
        True if the path exists, False otherwise
    
    Example:
        >>> data = {'user': {'name': 'John'}}
        >>> has_path(data, 'user.name')
        True
        >>> has_path(data, 'user.age')
        False
    """
    return get_path(obj, path, default=None, separator=separator) is not None


def delete_path(obj: Dict[str, Any], path: str, separator: str = '.') -> bool:
    """
    Delete a key from a nested dictionary using a dot-separated path.
    
    Args:
        obj: The dictionary to modify
        path: The dot-separated path
        separator: The path separator (default: '.')
    
    Returns:
        True if the key was deleted, False otherwise
    
    Example:
        >>> data = {'user': {'name': 'John', 'age': 30}}
        >>> delete_path(data, 'user.age')
        True
        >>> data
        {'user': {'name': 'John'}}
    """
    if obj is None or not path:
        return False
    
    keys = path.split(separator)
    current = obj
    
    for key in keys[:-1]:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return False
    
    if isinstance(current, dict) and keys[-1] in current:
        del current[keys[-1]]
        return True
    return False


# ============================================================================
# Merge and Manipulation Functions
# ============================================================================

def merge(base: Dict[str, Any], *updates: Dict[str, Any], 
          deep: bool = True) -> Dict[str, Any]:
    """
    Merge multiple dictionaries into a new dictionary.
    
    Args:
        base: The base dictionary
        *updates: Dictionaries to merge into base
        deep: Whether to perform deep merge (default: True)
    
    Returns:
        A new merged dictionary
    
    Example:
        >>> base = {'a': 1, 'b': {'c': 2}}
        >>> update = {'b': {'d': 3}, 'e': 4}
        >>> merge(base, update)
        {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}
    """
    result = deepcopy(base) if deep else dict(base)
    
    for update in updates:
        if deep:
            _deep_merge(result, update)
        else:
            result.update(update)
    
    return result


def _deep_merge(base: Dict[str, Any], update: Dict[str, Any]) -> None:
    """Recursively merge update into base."""
    for key, value in update.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = deepcopy(value) if isinstance(value, (dict, list)) else value


def flatten(obj: Dict[str, Any], separator: str = '.', parent_key: str = '') -> Dict[str, Any]:
    """
    Flatten a nested dictionary into a single-level dictionary.
    
    Args:
        obj: The dictionary to flatten
        separator: The separator for nested keys (default: '.')
        parent_key: The parent key prefix (used internally)
    
    Returns:
        A flattened dictionary
    
    Example:
        >>> data = {'user': {'name': 'John', 'address': {'city': 'NYC'}}}
        >>> flatten(data)
        {'user.name': 'John', 'user.address.city': 'NYC'}
    """
    items: Dict[str, Any] = {}
    for key, value in obj.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            items.update(flatten(value, separator, new_key))
        else:
            items[new_key] = value
    return items


def unflatten(obj: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
    """
    Unflatten a single-level dictionary into a nested dictionary.
    
    Args:
        obj: The dictionary to unflatten
        separator: The separator for nested keys (default: '.')
    
    Returns:
        An unflattened dictionary
    
    Example:
        >>> data = {'user.name': 'John', 'user.age': 30}
        >>> unflatten(data)
        {'user': {'name': 'John', 'age': 30}}
    """
    result: Dict[str, Any] = {}
    for key, value in obj.items():
        set_path(result, key, value, separator=separator)
    return result


def filter_by_key(obj: Dict[str, Any], predicate: Callable[[str], bool]) -> Dict[str, Any]:
    """
    Filter dictionary entries by key using a predicate function.
    
    Args:
        obj: The dictionary to filter
        predicate: A function that takes a key and returns True to keep it
    
    Returns:
        A new filtered dictionary
    
    Example:
        >>> data = {'name': 'John', 'age': 30, 'email': 'john@example.com'}
        >>> filter_by_key(data, lambda k: k.startswith('a'))
        {'age': 30}
    """
    return {k: v for k, v in obj.items() if predicate(k)}


def filter_by_value(obj: Dict[str, Any], predicate: Callable[[Any], bool]) -> Dict[str, Any]:
    """
    Filter dictionary entries by value using a predicate function.
    
    Args:
        obj: The dictionary to filter
        predicate: A function that takes a value and returns True to keep it
    
    Returns:
        A new filtered dictionary
    
    Example:
        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> filter_by_value(data, lambda v: v > 1)
        {'b': 2, 'c': 3}
    """
    return {k: v for k, v in obj.items() if predicate(v)}


def pick(obj: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """
    Pick specific keys from a dictionary.
    
    Args:
        obj: The dictionary to pick from
        keys: List of keys to pick
    
    Returns:
        A new dictionary with only the picked keys
    
    Example:
        >>> data = {'name': 'John', 'age': 30, 'email': 'john@example.com'}
        >>> pick(data, ['name', 'email'])
        {'name': 'John', 'email': 'john@example.com'}
    """
    return {k: obj[k] for k in keys if k in obj}


def omit(obj: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """
    Omit specific keys from a dictionary.
    
    Args:
        obj: The dictionary to omit from
        keys: List of keys to omit
    
    Returns:
        A new dictionary without the omitted keys
    
    Example:
        >>> data = {'name': 'John', 'age': 30, 'email': 'john@example.com'}
        >>> omit(data, ['age'])
        {'name': 'John', 'email': 'john@example.com'}
    """
    keys_set = set(keys)
    return {k: v for k, v in obj.items() if k not in keys_set}


# ============================================================================
# Validation Functions
# ============================================================================

def is_valid(json_str: str) -> bool:
    """
    Check if a string is valid JSON.
    
    Args:
        json_str: The string to validate
    
    Returns:
        True if valid JSON, False otherwise
    
    Example:
        >>> is_valid('{"name": "John"}')
        True
        >>> is_valid('invalid')
        False
    """
    try:
        json.loads(json_str)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def is_valid_file(file_path: str, encoding: str = 'utf-8') -> bool:
    """
    Check if a file contains valid JSON.
    
    Args:
        file_path: Path to the file to validate
        encoding: The file encoding (default: 'utf-8')
    
    Returns:
        True if valid JSON, False otherwise
    
    Example:
        >>> is_valid_file('config.json')
        True
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            json.load(f)
        return True
    except (FileNotFoundError, json.JSONDecodeError, IOError, PermissionError):
        return False


# ============================================================================
# Type Checking Functions
# ============================================================================

def is_json_object(obj: Any) -> bool:
    """
    Check if an object is a JSON object (dictionary).
    
    Args:
        obj: The object to check
    
    Returns:
        True if the object is a dictionary, False otherwise
    """
    return isinstance(obj, dict)


def is_json_array(obj: Any) -> bool:
    """
    Check if an object is a JSON array (list).
    
    Args:
        obj: The object to check
    
    Returns:
        True if the object is a list, False otherwise
    """
    return isinstance(obj, list)


def is_json_primitive(obj: Any) -> bool:
    """
    Check if an object is a JSON primitive (string, number, boolean, or null).
    
    Args:
        obj: The object to check
    
    Returns:
        True if the object is a JSON primitive, False otherwise
    """
    return obj is None or isinstance(obj, (str, int, float, bool))


# ============================================================================
# Utility Functions
# ============================================================================

def clone(obj: Any) -> Any:
    """
    Create a deep copy of a JSON-compatible object.
    
    Args:
        obj: The object to clone
    
    Returns:
        A deep copy of the object
    
    Example:
        >>> data = {'user': {'name': 'John'}}
        >>> cloned = clone(data)
        >>> cloned['user']['name'] = 'Jane'
        >>> data['user']['name']  # Original unchanged
        'John'
    """
    return deepcopy(obj)


def diff(obj1: Dict[str, Any], obj2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the difference between two dictionaries.
    
    Args:
        obj1: The first dictionary
        obj2: The second dictionary
    
    Returns:
        A dictionary showing added, removed, and changed keys
    
    Example:
        >>> obj1 = {'a': 1, 'b': 2}
        >>> obj2 = {'b': 3, 'c': 4}
        >>> diff(obj1, obj2)
        {'added': {'c': 4}, 'removed': {'a': 1}, 'changed': {'b': (2, 3)}}
    """
    result = {'added': {}, 'removed': {}, 'changed': {}}
    
    all_keys = set(obj1.keys()) | set(obj2.keys())
    
    for key in all_keys:
        if key in obj1 and key not in obj2:
            result['removed'][key] = obj1[key]
        elif key not in obj1 and key in obj2:
            result['added'][key] = obj2[key]
        elif obj1[key] != obj2[key]:
            result['changed'][key] = (obj1[key], obj2[key])
    
    return result


def size(obj: Any) -> int:
    """
    Get the size of a JSON object or array.
    
    Args:
        obj: The JSON object or array
    
    Returns:
        The number of elements (for arrays) or keys (for objects)
    
    Example:
        >>> size({'a': 1, 'b': 2})
        2
        >>> size([1, 2, 3])
        3
    """
    if isinstance(obj, (dict, list)):
        return len(obj)
    return 0


def sort_keys(obj: Dict[str, Any], recursive: bool = True) -> Dict[str, Any]:
    """
    Sort dictionary keys alphabetically.
    
    Args:
        obj: The dictionary to sort
        recursive: Whether to sort nested dictionaries (default: True)
    
    Returns:
        A new dictionary with sorted keys
    
    Example:
        >>> data = {'z': 1, 'a': 2, 'm': 3}
        >>> sort_keys(data)
        {'a': 2, 'm': 3, 'z': 1}
    """
    result = {}
    for key in sorted(obj.keys()):
        value = obj[key]
        if recursive and isinstance(value, dict):
            result[key] = sort_keys(value, recursive=True)
        else:
            result[key] = value
    return result


# ============================================================================
# Advanced Query Functions
# ============================================================================

def find_all(obj: Any, key: str) -> List[Any]:
    """
    Find all values with a specific key in a nested structure.
    
    Uses iterative breadth-first traversal to find all matching values,
    avoiding recursion stack overflow for deeply nested structures.
    
    Args:
        obj: The object to search
        key: The key to find
    
    Returns:
        A list of all values with the matching key
    
    Example:
        >>> data = {'users': [{'name': 'John'}, {'name': 'Jane'}]}
        >>> find_all(data, 'name')
        ['John', 'Jane']
    """
    results = []
    
    # Use iterative approach with a stack to avoid recursion depth limits
    stack = [obj]
    
    while stack:
        current = stack.pop()
        
        if isinstance(current, dict):
            for k, v in current.items():
                if k == key:
                    results.append(v)
                # Only push dict/list values for further processing
                if isinstance(v, (dict, list)):
                    stack.append(v)
        elif isinstance(current, list):
            # Iterate in reverse order to maintain original order in results
            for item in reversed(current):
                if isinstance(item, (dict, list)):
                    stack.append(item)
    
    return results


def find_first(obj: Any, key: str, default: Any = None) -> Any:
    """
    Find the first value with a specific key in a nested structure.
    
    Args:
        obj: The object to search
        key: The key to find
        default: The default value if not found
    
    Returns:
        The first matching value, or the default
    
    Example:
        >>> data = {'users': [{'name': 'John'}, {'name': 'Jane'}]}
        >>> find_first(data, 'name')
        'John'
    """
    results = find_all(obj, key)
    return results[0] if results else default


def map_values(obj: Dict[str, Any], func: Callable[[Any], Any]) -> Dict[str, Any]:
    """
    Apply a function to all values in a dictionary.
    
    Args:
        obj: The dictionary to map
        func: The function to apply to each value
    
    Returns:
        A new dictionary with mapped values
    
    Example:
        >>> data = {'a': 1, 'b': 2}
        >>> map_values(data, lambda x: x * 2)
        {'a': 2, 'b': 4}
    """
    return {k: func(v) for k, v in obj.items()}


def map_keys(obj: Dict[str, Any], func: Callable[[str], str]) -> Dict[str, Any]:
    """
    Apply a function to all keys in a dictionary.
    
    Args:
        obj: The dictionary to map
        func: The function to apply to each key
    
    Returns:
        A new dictionary with mapped keys
    
    Example:
        >>> data = {'a': 1, 'b': 2}
        >>> map_keys(data, lambda k: k.upper())
        {'A': 1, 'B': 2}
    """
    return {func(k): v for k, v in obj.items()}


# ============================================================================
# Comparison Functions
# ============================================================================

def equals(obj1: Any, obj2: Any) -> bool:
    """
    Deep compare two JSON objects for equality.
    
    Args:
        obj1: The first object
        obj2: The second object
    
    Returns:
        True if the objects are equal, False otherwise
    
    Example:
        >>> equals({'a': 1}, {'a': 1})
        True
        >>> equals({'a': 1}, {'a': 2})
        False
    """
    return obj1 == obj2


def hash_code(obj: Any) -> int:
    """
    Generate a hash code for a JSON object.
    
    Args:
        obj: The object to hash
    
    Returns:
        A hash code for the object
    
    Example:
        >>> hash_code({'a': 1})
        -123456789  # Some integer hash value
    """
    return hash(json.dumps(obj, sort_keys=True, separators=(',', ':')))
