#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - NaN Handler Utilities Module
==========================================
A comprehensive NaN/None value handling utility module for Python with zero external dependencies.

Features:
    - Detect NaN/None values in various data types
    - Convert NaN to None or custom default values
    - Fill NaN values with strategies (mean, median, mode, constant, interpolate)
    - Drop rows/columns containing NaN values
    - Replace NaN in nested structures (lists, dicts, tuples)
    - Batch processing for collections
    - Custom NaN detection patterns
    - Statistics on NaN occurrences
    - Safe serialization handling

Author: AllToolkit Contributors
License: MIT
"""

import math
import re
from typing import Any, Dict, List, Optional, Union, Callable, Tuple, Set
from collections import Counter
from functools import wraps


# ============================================================================
# Constants
# ============================================================================

# Common NaN string representations
NaN_STRING_PATTERNS = [
    'nan', 'NaN', 'NAN', 'NA', 'N/A', 'na', 'n/a',
    'null', 'NULL', 'Null', 'none', 'NONE', 'None',
    'undefined', 'UNDEFINED', 'Undefined',
    '-', '--', '---', '.', '..', '...',
    '#N/A', '#NA', '#NULL', '#N/A N/A',
    'missing', 'MISSING', 'Missing',
    'empty', 'EMPTY', 'Empty',
    'inf', '-inf', 'Infinity', '-Infinity',
]

# Numeric values considered as NaN-equivalent
NaN_NUMERIC_VALUES = [
    float('nan'),
    float('inf'),
    float('-inf'),
]


# ============================================================================
# NaN Detection
# ============================================================================

def is_nan(value: Any, include_strings: bool = True, include_none: bool = True,
           include_inf: bool = False, custom_patterns: Optional[List[str]] = None) -> bool:
    """
    Check if a value is NaN or NaN-like.
    
    Args:
        value: Value to check
        include_strings: Include NaN string representations
        include_none: Include None as NaN
        include_inf: Include infinity as NaN
        custom_patterns: Additional custom NaN patterns
    
    Returns:
        True if value is NaN or NaN-like, False otherwise
    
    Examples:
        >>> is_nan(float('nan'))
        True
        >>> is_nan(None)
        True
        >>> is_nan('N/A')
        True
        >>> is_nan(42)
        False
    """
    # Check None
    if include_none and value is None:
        return True
    
    # Check float NaN
    if isinstance(value, float):
        if math.isnan(value):
            return True
        if include_inf and math.isinf(value):
            return True
    
    # Check string NaN patterns
    if include_strings and isinstance(value, str):
        patterns = NaN_STRING_PATTERNS.copy()
        if custom_patterns:
            patterns.extend(custom_patterns)
        return value.strip() in patterns
    
    # Check custom patterns for non-string values
    if custom_patterns and value in custom_patterns:
        return True
    
    return False


def is_not_nan(value: Any, **kwargs) -> bool:
    """Check if a value is NOT NaN or NaN-like. Opposite of is_nan."""
    return not is_nan(value, **kwargs)


def detect_nan_indices(data: List[Any], **kwargs) -> List[int]:
    """
    Detect indices of NaN values in a list.
    
    Args:
        data: List to check
        **kwargs: Additional arguments for is_nan
    
    Returns:
        List of indices where NaN values occur
    
    Examples:
        >>> detect_nan_indices([1, None, 3, float('nan'), 5])
        [1, 3]
    """
    return [i for i, v in enumerate(data) if is_nan(v, **kwargs)]


def detect_nan_keys(data: Dict[Any, Any], **kwargs) -> List[Any]:
    """
    Detect keys with NaN values in a dictionary.
    
    Args:
        data: Dictionary to check
        **kwargs: Additional arguments for is_nan
    
    Returns:
        List of keys where NaN values occur
    
    Examples:
        >>> detect_nan_keys({'a': 1, 'b': None, 'c': 3})
        ['b']
    """
    return [k for k, v in data.items() if is_nan(v, **kwargs)]


# ============================================================================
# NaN Statistics
# ============================================================================

def nan_count(data: Union[List[Any], Dict[Any, Any]], **kwargs) -> int:
    """
    Count NaN values in a collection.
    
    Args:
        data: List or dictionary to count
        **kwargs: Additional arguments for is_nan
    
    Returns:
        Number of NaN values
    
    Examples:
        >>> nan_count([1, None, 3, float('nan')])
        2
    """
    if isinstance(data, dict):
        return sum(1 for v in data.values() if is_nan(v, **kwargs))
    return sum(1 for v in data if is_nan(v, **kwargs))


def nan_percentage(data: Union[List[Any], Dict[Any, Any]], **kwargs) -> float:
    """
    Calculate percentage of NaN values in a collection.
    
    Args:
        data: List or dictionary
        **kwargs: Additional arguments for is_nan
    
    Returns:
        Percentage of NaN values (0.0 to 100.0)
    
    Examples:
        >>> nan_percentage([1, None, 3, float('nan')])
        50.0
    """
    count = nan_count(data, **kwargs)
    total = len(data) if isinstance(data, (list, dict)) else 0
    return (count / total * 100) if total > 0 else 0.0


def nan_summary(data: Union[List[Any], Dict[Any, Any]], **kwargs) -> Dict[str, Any]:
    """
    Generate a summary of NaN occurrences.
    
    Args:
        data: List or dictionary
        **kwargs: Additional arguments for is_nan
    
    Returns:
        Dictionary with NaN statistics
    
    Examples:
        >>> nan_summary([1, None, 3, float('nan'), 5])
        {'total': 5, 'nan_count': 2, 'valid_count': 3, 'nan_percentage': 40.0}
    """
    count = nan_count(data, **kwargs)
    total = len(data) if isinstance(data, (list, dict)) else 0
    return {
        'total': total,
        'nan_count': count,
        'valid_count': total - count,
        'nan_percentage': (count / total * 100) if total > 0 else 0.0,
    }


# ============================================================================
# NaN Conversion
# ============================================================================

def nan_to_none(value: Any, **kwargs) -> Optional[Any]:
    """
    Convert NaN value to None.
    
    Args:
        value: Value to convert
        **kwargs: Additional arguments for is_nan
    
    Returns:
        None if value is NaN, otherwise original value
    
    Examples:
        >>> nan_to_none(float('nan'))
        None
        >>> nan_to_none('N/A')
        None
        >>> nan_to_none(42)
        42
    """
    if is_nan(value, **kwargs):
        return None
    return value


def nan_to_default(value: Any, default: Any = 0, **kwargs) -> Any:
    """
    Convert NaN value to a default value.
    
    Args:
        value: Value to convert
        default: Default value to use (default: 0)
        **kwargs: Additional arguments for is_nan
    
    Returns:
        Default value if NaN, otherwise original value
    
    Examples:
        >>> nan_to_default(float('nan'), default=-1)
        -1
        >>> nan_to_default('N/A', default='missing')
        'missing'
    """
    if is_nan(value, **kwargs):
        return default
    return value


def convert_nan_list(data: List[Any], target: str = 'none', default: Any = 0, **kwargs) -> List[Any]:
    """
    Convert all NaN values in a list.
    
    Args:
        data: List to convert
        target: Target conversion ('none', 'default', 'remove')
        default: Default value for 'default' target
        **kwargs: Additional arguments for is_nan
    
    Returns:
        Converted list
    
    Examples:
        >>> convert_nan_list([1, None, 3, float('nan')], target='default', default=0)
        [1, 0, 3, 0]
    """
    if target == 'none':
        return [nan_to_none(v, **kwargs) for v in data]
    elif target == 'default':
        return [nan_to_default(v, default, **kwargs) for v in data]
    elif target == 'remove':
        return [v for v in data if not is_nan(v, **kwargs)]
    return data


def convert_nan_dict(data: Dict[Any, Any], target: str = 'none', default: Any = 0, 
                     remove_keys: bool = False, **kwargs) -> Dict[Any, Any]:
    """
    Convert all NaN values in a dictionary.
    
    Args:
        data: Dictionary to convert
        target: Target conversion ('none', 'default')
        default: Default value for 'default' target
        remove_keys: Remove keys with NaN values instead of converting
        **kwargs: Additional arguments for is_nan
    
    Returns:
        Converted dictionary
    
    Examples:
        >>> convert_nan_dict({'a': 1, 'b': None}, target='default', default=0)
        {'a': 1, 'b': 0}
    """
    if remove_keys:
        return {k: v for k, v in data.items() if not is_nan(v, **kwargs)}
    
    if target == 'none':
        return {k: nan_to_none(v, **kwargs) for k, v in data.items()}
    elif target == 'default':
        return {k: nan_to_default(v, default, **kwargs) for k, v in data.items()}
    return data


# ============================================================================
# NaN Filling Strategies
# ============================================================================

def fill_nan_mean(data: List[Union[int, float]], default: float = 0.0, **kwargs) -> List[Union[int, float]]:
    """
    Fill NaN values with the mean of non-NaN values.
    
    Args:
        data: Numeric list to fill
        default: Default if no valid values exist
        **kwargs: Additional arguments for is_nan
    
    Returns:
        List with NaN values replaced by mean
    
    Examples:
        >>> fill_nan_mean([1, float('nan'), 3, float('nan')])
        [1, 2.0, 3, 2.0]
    """
    valid_values = [v for v in data if isinstance(v, (int, float)) and not is_nan(v, **kwargs)]
    mean = sum(valid_values) / len(valid_values) if valid_values else default
    return [mean if is_nan(v, **kwargs) and isinstance(v, (int, float)) else v for v in data]


def fill_nan_median(data: List[Union[int, float]], default: float = 0.0, **kwargs) -> List[Union[int, float]]:
    """
    Fill NaN values with the median of non-NaN values.
    
    Args:
        data: Numeric list to fill
        default: Default if no valid values exist
        **kwargs: Additional arguments for is_nan
    
    Returns:
        List with NaN values replaced by median
    
    Examples:
        >>> fill_nan_median([1, float('nan'), 2, float('nan'), 100])
        [1, 2.0, 2, 2.0, 100]
    """
    valid_values = [v for v in data if isinstance(v, (int, float)) and not is_nan(v, **kwargs)]
    if not valid_values:
        return [default if is_nan(v, **kwargs) else v for v in data]
    
    sorted_values = sorted(valid_values)
    n = len(sorted_values)
    median = sorted_values[n // 2] if n % 2 == 1 else (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
    
    return [median if is_nan(v, **kwargs) and isinstance(v, (int, float)) else v for v in data]


def fill_nan_mode(data: List[Any], default: Any = None, **kwargs) -> List[Any]:
    """
    Fill NaN values with the most frequent non-NaN value.
    
    Args:
        data: List to fill
        default: Default if no valid values exist
        **kwargs: Additional arguments for is_nan
    
    Returns:
        List with NaN values replaced by mode
    
    Examples:
        >>> fill_nan_mode([1, None, 1, None, 2])
        [1, 1, 1, 1, 2]
    """
    valid_values = [v for v in data if not is_nan(v, **kwargs)]
    if not valid_values:
        return [default if is_nan(v, **kwargs) else v for v in data]
    
    counter = Counter(valid_values)
    mode = counter.most_common(1)[0][0]
    
    return [mode if is_nan(v, **kwargs) else v for v in data]


def fill_nan_constant(data: List[Any], constant: Any, **kwargs) -> List[Any]:
    """
    Fill NaN values with a constant value.
    
    Args:
        data: List to fill
        constant: Constant value to use
        **kwargs: Additional arguments for is_nan
    
    Returns:
        List with NaN values replaced by constant
    
    Examples:
        >>> fill_nan_constant([1, None, 3], constant=-999)
        [1, -999, 3]
    """
    return [constant if is_nan(v, **kwargs) else v for v in data]


def fill_nan_interpolate(data: List[Union[int, float]], method: str = 'linear', 
                         default: float = 0.0, **kwargs) -> List[Union[int, float]]:
    """
    Fill NaN values with interpolated values.
    
    Args:
        data: Numeric list to fill
        method: Interpolation method ('linear', 'forward', 'backward')
        default: Default for edge NaN values
        **kwargs: Additional arguments for is_nan
    
    Returns:
        List with NaN values interpolated
    
    Examples:
        >>> fill_nan_interpolate([1, float('nan'), 3], method='linear')
        [1, 2.0, 3]
    """
    result = list(data)
    nan_indices = detect_nan_indices(result, **kwargs)
    
    if not nan_indices:
        return result
    
    if method == 'forward':
        # Fill with previous valid value
        last_valid = default
        for i, v in enumerate(result):
            if not is_nan(v, **kwargs):
                last_valid = v
            else:
                result[i] = last_valid
        return result
    
    elif method == 'backward':
        # Fill with next valid value
        next_valid = default
        for i in range(len(result) - 1, -1, -1):
            if not is_nan(result[i], **kwargs):
                next_valid = result[i]
            else:
                result[i] = next_valid
        return result
    
    elif method == 'linear':
        # Linear interpolation between valid values
        for idx in nan_indices:
            # Find previous valid value
            prev_idx = idx - 1
            prev_val = None
            while prev_idx >= 0:
                if not is_nan(result[prev_idx], **kwargs):
                    prev_val = result[prev_idx]
                    break
                prev_idx -= 1
            
            # Find next valid value
            next_idx = idx + 1
            next_val = None
            while next_idx < len(result):
                if not is_nan(result[next_idx], **kwargs):
                    next_val = result[next_idx]
                    break
                next_idx += 1
            
            if prev_val is not None and next_val is not None:
                # Interpolate
                result[idx] = prev_val + (next_val - prev_val) * (idx - prev_idx) / (next_idx - prev_idx)
            elif prev_val is not None:
                result[idx] = prev_val
            elif next_val is not None:
                result[idx] = next_val
            else:
                result[idx] = default
        
        return result
    
    return result


def fill_nan_custom(data: List[Any], func: Callable[[Any, int, List[Any]], Any], **kwargs) -> List[Any]:
    """
    Fill NaN values using a custom function.
    
    Args:
        data: List to fill
        func: Custom function (value, index, full_list) -> replacement
        **kwargs: Additional arguments for is_nan
    
    Returns:
        List with NaN values replaced by custom function result
    
    Examples:
        >>> fill_nan_custom([1, None, 3], lambda v, i, lst: i * 10)
        [1, 10, 3]
    """
    return [func(v, i, data) if is_nan(v, **kwargs) else v for i, v in enumerate(data)]


# ============================================================================
# NaN Dropping
# ============================================================================

def drop_nan_values(data: List[Any], **kwargs) -> List[Any]:
    """
    Drop all NaN values from a list.
    
    Args:
        data: List to process
        **kwargs: Additional arguments for is_nan
    
    Returns:
        List without NaN values
    
    Examples:
        >>> drop_nan_values([1, None, 3, float('nan')])
        [1, 3]
    """
    return [v for v in data if not is_nan(v, **kwargs)]


def drop_nan_rows(data: List[List[Any]], how: str = 'any', threshold: Optional[int] = None, 
                  **kwargs) -> List[List[Any]]:
    """
    Drop rows containing NaN values from a 2D list (table-like).
    
    Args:
        data: 2D list (table)
        how: 'any' (drop if any NaN) or 'all' (drop if all NaN)
        threshold: Minimum number of NaN to drop
        **kwargs: Additional arguments for is_nan
    
    Returns:
        2D list with NaN rows removed
    
    Examples:
        >>> drop_nan_rows([[1, 2], [None, 4], [None, None]], how='any')
        [[1, 2]]
    """
    result = []
    for row in data:
        nan_in_row = sum(1 for v in row if is_nan(v, **kwargs))
        
        if how == 'any' and nan_in_row > 0:
            if threshold is not None and nan_in_row < threshold:
                result.append(row)
        elif how == 'all' and nan_in_row == len(row):
            continue
        else:
            result.append(row)
    
    return result


def drop_nan_columns(data: List[List[Any]], how: str = 'any', threshold: Optional[int] = None,
                     **kwargs) -> List[List[Any]]:
    """
    Drop columns containing NaN values from a 2D list (table-like).
    
    Args:
        data: 2D list (table)
        how: 'any' (drop if any NaN) or 'all' (drop if all NaN)
        threshold: Minimum number of NaN to drop
        **kwargs: Additional arguments for is_nan
    
    Returns:
        2D list with NaN columns removed
    
    Examples:
        >>> drop_nan_columns([[1, None], [2, None], [3, 4]], how='all')
        [[1], [2], [3]]
    """
    if not data:
        return data
    
    num_cols = len(data[0]) if data else 0
    cols_to_keep = []
    
    for col_idx in range(num_cols):
        column = [row[col_idx] if col_idx < len(row) else None for row in data]
        nan_in_col = sum(1 for v in column if is_nan(v, **kwargs))
        
        if how == 'any' and nan_in_col > 0:
            if threshold is not None and nan_in_col < threshold:
                cols_to_keep.append(col_idx)
        elif how == 'all' and nan_in_col == len(column):
            continue
        else:
            cols_to_keep.append(col_idx)
    
    return [[row[i] for i in cols_to_keep if i < len(row)] for row in data]


def drop_nan_dict_keys(data: Dict[Any, Any], **kwargs) -> Dict[Any, Any]:
    """
    Drop dictionary entries with NaN values.
    
    Args:
        data: Dictionary to process
        **kwargs: Additional arguments for is_nan
    
    Returns:
        Dictionary without NaN entries
    
    Examples:
        >>> drop_nan_dict_keys({'a': 1, 'b': None, 'c': 3})
        {'a': 1, 'c': 3}
    """
    return {k: v for k, v in data.items() if not is_nan(v, **kwargs)}


# ============================================================================
# Nested Structure Handling
# ============================================================================

def convert_nan_nested(data: Any, target: str = 'none', default: Any = 0, **kwargs) -> Any:
    """
    Convert NaN values in nested structures (lists, dicts, tuples).
    
    Args:
        data: Nested structure to convert
        target: Target conversion ('none', 'default', 'remove')
        default: Default value for 'default' target
        **kwargs: Additional arguments for is_nan
    
    Returns:
        Converted nested structure
    
    Examples:
        >>> convert_nan_nested([1, [None, 3], {'a': float('nan')}], target='default', default=0)
        [1, [0, 3], {'a': 0}]
    """
    if isinstance(data, dict):
        result = {}
        for k, v in data.items():
            converted = convert_nan_nested(v, target, default, **kwargs)
            if target != 'remove' or not is_nan(converted, **kwargs):
                result[k] = converted
        return result
    elif isinstance(data, list):
        result = []
        for v in data:
            converted = convert_nan_nested(v, target, default, **kwargs)
            if target != 'remove' or not is_nan(converted, **kwargs):
                result.append(converted)
        return result
    elif isinstance(data, tuple):
        result = []
        for v in data:
            converted = convert_nan_nested(v, target, default, **kwargs)
            if target != 'remove' or not is_nan(converted, **kwargs):
                result.append(converted)
        return tuple(result)
    else:
        if is_nan(data, **kwargs):
            if target == 'none':
                return None
            elif target == 'default':
                return default
            elif target == 'remove':
                return None  # Will be filtered by parent
        return data


def count_nan_nested(data: Any, **kwargs) -> int:
    """
    Count NaN values in nested structures.
    
    Args:
        data: Nested structure
        **kwargs: Additional arguments for is_nan
    
    Returns:
        Total count of NaN values
    
    Examples:
        >>> count_nan_nested([1, [None, 3], {'a': float('nan')}])
        2
    """
    count = 0
    if isinstance(data, dict):
        for v in data.values():
            count += count_nan_nested(v, **kwargs)
    elif isinstance(data, (list, tuple)):
        for v in data:
            count += count_nan_nested(v, **kwargs)
    elif is_nan(data, **kwargs):
        count = 1
    return count


# ============================================================================
# Batch Processing
# ============================================================================

def batch_nan_to_none(data: Union[List[Any], Dict[Any, Any]], **kwargs) -> Union[List[Any], Dict[Any, Any]]:
    """
    Batch convert all NaN values to None.
    
    Args:
        data: List or dictionary
        **kwargs: Additional arguments for is_nan
    
    Returns:
        Data with all NaN converted to None
    """
    if isinstance(data, dict):
        return convert_nan_dict(data, target='none', **kwargs)
    return convert_nan_list(data, target='none', **kwargs)


def batch_fill_nan(data: Union[List[Any], Dict[Any, Any]], strategy: str = 'constant', 
                   value: Any = 0, **kwargs) -> Union[List[Any], Dict[Any, Any]]:
    """
    Batch fill NaN values using specified strategy.
    
    Args:
        data: List or dictionary
        strategy: Fill strategy ('constant', 'mean', 'median', 'mode')
        value: Value for 'constant' strategy
        **kwargs: Additional arguments for is_nan
    
    Returns:
        Data with NaN filled
    
    Examples:
        >>> batch_fill_nan([1, None, 3, None], strategy='constant', value=0)
        [1, 0, 3, 0]
    """
    if isinstance(data, dict):
        values = list(data.values())
        if strategy == 'mean':
            filled = fill_nan_mean(values, default=value, **kwargs)
        elif strategy == 'median':
            filled = fill_nan_median(values, default=value, **kwargs)
        elif strategy == 'mode':
            filled = fill_nan_mode(values, default=value, **kwargs)
        else:
            filled = fill_nan_constant(values, value, **kwargs)
        return dict(zip(data.keys(), filled))
    
    if strategy == 'mean':
        return fill_nan_mean(data, default=value, **kwargs)
    elif strategy == 'median':
        return fill_nan_median(data, default=value, **kwargs)
    elif strategy == 'mode':
        return fill_nan_mode(data, default=value, **kwargs)
    return fill_nan_constant(data, value, **kwargs)


# ============================================================================
# Safe Serialization
# ============================================================================

def safe_serialize(data: Any, nan_replacement: Any = None, **kwargs) -> Any:
    """
    Safely serialize data by replacing NaN values (JSON-compatible).
    
    Args:
        data: Data to serialize
        nan_replacement: Replacement for NaN values (must be JSON-compatible)
        **kwargs: Additional arguments for is_nan
    
    Returns:
        JSON-safe data
    
    Examples:
        >>> safe_serialize({'a': float('nan'), 'b': 2})
        {'a': None, 'b': 2}
    """
    return convert_nan_nested(data, target='default', default=nan_replacement, **kwargs)


def safe_json_dumps(data: Any, nan_replacement: Any = None, **kwargs) -> str:
    """
    Convert data to JSON string safely (replacing NaN values).
    
    Args:
        data: Data to convert
        nan_replacement: Replacement for NaN values
        **kwargs: Additional arguments for is_nan
    
    Returns:
        JSON string
    
    Note: Uses simple JSON serialization without json module for zero dependencies.
    
    Examples:
        >>> safe_json_dumps({'a': float('nan')})
        '{"a": null}'
    """
    safe_data = safe_serialize(data, nan_replacement, **kwargs)
    return _simple_json_encode(safe_data)


def _simple_json_encode(data: Any) -> str:
    """Simple JSON encoder without external dependencies."""
    if data is None:
        return 'null'
    elif isinstance(data, bool):
        return 'true' if data else 'false'
    elif isinstance(data, (int, float)):
        if isinstance(data, float) and (math.isnan(data) or math.isinf(data)):
            return 'null'
        return str(data)
    elif isinstance(data, str):
        # Escape special characters
        escaped = data.replace('\\', '\\\\').replace('"', '\\"')
        escaped = escaped.replace('\n', '\\n').replace('\r', '\\r')
        escaped = escaped.replace('\t', '\\t')
        return f'"{escaped}"'
    elif isinstance(data, list):
        items = [_simple_json_encode(v) for v in data]
        return '[' + ', '.join(items) + ']'
    elif isinstance(data, dict):
        pairs = []
        for k, v in data.items():
            key_str = _simple_json_encode(str(k))
            val_str = _simple_json_encode(v)
            pairs.append(f'{key_str}: {val_str}')
        return '{' + ', '.join(pairs) + '}'
    else:
        return _simple_json_encode(str(data))


# ============================================================================
# Validator Decorators
# ============================================================================

def validate_no_nan(func: Callable) -> Callable:
    """
    Decorator to validate that function arguments contain no NaN values.
    
    Args:
        func: Function to decorate
    
    Returns:
        Decorated function
    
    Examples:
        >>> @validate_no_nan
        >>> def add(a, b):
        >>>     return a + b
        >>> add(1, float('nan'))  # Raises ValueError
    """
    @wraps(func)
    def wrapper(*args, **kwargs_func):
        for i, arg in enumerate(args):
            if is_nan(arg):
                raise ValueError(f"Argument {i} contains NaN value")
        for key, val in kwargs_func.items():
            if is_nan(val):
                raise ValueError(f"Argument '{key}' contains NaN value")
        return func(*args, **kwargs_func)
    return wrapper


def nan_safe(func: Optional[Callable] = None, default: Any = None) -> Callable:
    """
    Decorator to make function NaN-safe (return default for NaN inputs).
    
    Args:
        func: Function to decorate (optional for factory usage)
        default: Default return value when NaN encountered
    
    Returns:
        Decorated function
    
    Examples:
        >>> @nan_safe(default=0)
        >>> def square(x):
        >>>     return x * x
        >>> square(float('nan'))
        0
        
        >>> @nan_safe
        >>> def process(x):
        >>>     return x + 1
        >>> process(None)  # Returns None
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs_func):
            if any(is_nan(arg) for arg in args) or any(is_nan(v) for v in kwargs_func.values()):
                return default
            return f(*args, **kwargs_func)
        return wrapper
    
    if func is not None:
        # Direct usage: @nan_safe
        return decorator(func)
    else:
        # Factory usage: @nan_safe(default=0)
        return decorator


# ============================================================================
# Utility Functions
# ============================================================================

def replace_nan_strings(data: Any, replacement: Any = None, 
                        patterns: Optional[List[str]] = None) -> Any:
    """
    Replace NaN-like strings in data.
    
    Args:
        data: Data to process
        replacement: Replacement value
        patterns: Custom NaN string patterns
    
    Returns:
        Data with NaN strings replaced
    
    Examples:
        >>> replace_nan_strings('N/A', replacement='missing')
        'missing'
    """
    if isinstance(data, str):
        check_patterns = patterns if patterns else NaN_STRING_PATTERNS
        if data.strip() in check_patterns:
            return replacement
        return data
    elif isinstance(data, dict):
        return {k: replace_nan_strings(v, replacement, patterns) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_nan_strings(v, replacement, patterns) for v in data]
    elif isinstance(data, tuple):
        return tuple(replace_nan_strings(v, replacement, patterns) for v in data)
    return data


def get_valid_values(data: List[Any], **kwargs) -> List[Any]:
    """
    Extract all valid (non-NaN) values from a list.
    
    Args:
        data: List to process
        **kwargs: Additional arguments for is_nan
    
    Returns:
        List of valid values
    
    Examples:
        >>> get_valid_values([1, None, 3, float('nan'), 5])
        [1, 3, 5]
    """
    return [v for v in data if not is_nan(v, **kwargs)]


def get_nan_values(data: List[Any], **kwargs) -> List[Any]:
    """
    Extract all NaN values from a list.
    
    Args:
        data: List to process
        **kwargs: Additional arguments for is_nan
    
    Returns:
        List of NaN values (preserving original representation)
    
    Examples:
        >>> get_nan_values([1, None, 3, float('nan')])
        [None, nan]
    """
    return [v for v in data if is_nan(v, **kwargs)]


def first_valid_index(data: List[Any], **kwargs) -> Optional[int]:
    """
    Find the index of the first valid (non-NaN) value.
    
    Args:
        data: List to search
        **kwargs: Additional arguments for is_nan
    
    Returns:
        Index of first valid value, or None if all NaN
    
    Examples:
        >>> first_valid_index([None, None, 3, 4])
        2
    """
    for i, v in enumerate(data):
        if not is_nan(v, **kwargs):
            return i
    return None


def last_valid_index(data: List[Any], **kwargs) -> Optional[int]:
    """
    Find the index of the last valid (non-NaN) value.
    
    Args:
        data: List to search
        **kwargs: Additional arguments for is_nan
    
    Returns:
        Index of last valid value, or None if all NaN
    
    Examples:
        >>> last_valid_index([1, 2, None, None])
        1
    """
    for i in range(len(data) - 1, -1, -1):
        if not is_nan(data[i], **kwargs):
            return i
    return None


# ============================================================================
# Module Entry Point
# ============================================================================

if __name__ == '__main__':
    # Demo usage
    print("NaN Handler Utilities Demo")
    print("=" * 40)
    
    # Detection
    data = [1, None, 3, float('nan'), 'N/A', 5]
    print(f"Data: {data}")
    print(f"NaN count: {nan_count(data)}")
    print(f"NaN indices: {detect_nan_indices(data)}")
    print(f"NaN percentage: {nan_percentage(data):.1f}%")
    
    # Conversion
    print(f"\nConverted to None: {convert_nan_list(data, target='none')}")
    print(f"Converted to 0: {convert_nan_list(data, target='default', default=0)}")
    print(f"NaN removed: {convert_nan_list(data, target='remove')}")
    
    # Filling
    numeric_data = [1, float('nan'), 3, float('nan'), 5]
    print(f"\nNumeric data: {numeric_data}")
    print(f"Filled with mean: {fill_nan_mean(numeric_data)}")
    print(f"Filled with median: {fill_nan_median(numeric_data)}")
    print(f"Linear interpolated: {fill_nan_interpolate(numeric_data)}")
    
    # Nested structures
    nested = {'a': 1, 'b': [None, 3], 'c': {'x': float('nan')}}
    print(f"\nNested structure: {nested}")
    print(f"Converted nested: {convert_nan_nested(nested, target='default', default=0)}")
    print(f"NaN count in nested: {count_nan_nested(nested)}")
    
    # Safe serialization
    print(f"\nSafe JSON: {safe_json_dumps(nested)}")
    
    print("\n" + "=" * 40)
    print("Demo complete!")