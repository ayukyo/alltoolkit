#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NaN Handler Utilities - Basic Usage Examples
==============================================
Demonstrates common use cases for nan_handler_utils module.
"""

import sys
sys.path.insert(0, '..')

from mod import (
    is_nan, nan_count, nan_percentage, nan_summary,
    nan_to_none, nan_to_default, convert_nan_list, convert_nan_dict,
    fill_nan_mean, fill_nan_median, fill_nan_mode, fill_nan_interpolate,
    drop_nan_values, drop_nan_rows, drop_nan_columns,
    convert_nan_nested, count_nan_nested,
    safe_json_dumps, nan_safe,
)


def example_detection():
    """Example: NaN detection."""
    print("\n" + "=" * 40)
    print("Example 1: NaN Detection")
    print("=" * 40)
    
    data = [10, None, 20, float('nan'), 'N/A', 30, 'null']
    
    print(f"Data: {data}")
    print(f"NaN count: {nan_count(data)}")
    print(f"NaN percentage: {nan_percentage(data):.1f}%")
    print(f"Summary: {nan_summary(data)}")
    
    # Check individual values
    print("\nIndividual checks:")
    for v in data:
        print(f"  is_nan({repr(v)}) = {is_nan(v)}")


def example_conversion():
    """Example: NaN conversion."""
    print("\n" + "=" * 40)
    print("Example 2: NaN Conversion")
    print("=" * 40)
    
    data = [1, None, 2, float('nan'), 3]
    
    print(f"Original: {data}")
    print(f"To None: {convert_nan_list(data, target='none')}")
    print(f"To 0: {convert_nan_list(data, target='default', default=0)}")
    print(f"Removed: {convert_nan_list(data, target='remove')}")
    
    # Dictionary conversion
    config = {'timeout': 30, 'retries': None, 'cache': float('nan')}
    print(f"\nDict original: {config}")
    print(f"Dict converted: {convert_nan_dict(config, target='default', default=10)}")


def example_filling():
    """Example: Filling strategies."""
    print("\n" + "=" * 40)
    print("Example 3: NaN Filling Strategies")
    print("=" * 40)
    
    # Numeric data
    data = [1, float('nan'), 3, float('nan'), 5]
    
    print(f"Original: {data}")
    print(f"Mean fill: {fill_nan_mean(data)}")
    print(f"Median fill: {fill_nan_median(data)}")
    
    # Mixed data with mode
    mixed = ['apple', None, 'apple', float('nan'), 'banana']
    print(f"\nMixed data: {mixed}")
    print(f"Mode fill: {fill_nan_mode(mixed)}")
    
    # Interpolation
    series = [10, float('nan'), float('nan'), 40]
    print(f"\nSeries: {series}")
    print(f"Linear interpolate: {fill_nan_interpolate(series, method='linear')}")
    print(f"Forward fill: {fill_nan_interpolate(series, method='forward')}")
    print(f"Backward fill: {fill_nan_interpolate(series, method='backward')}")


def example_dropping():
    """Example: Dropping NaN values."""
    print("\n" + "=" * 40)
    print("Example 4: Dropping NaN Values")
    print("=" * 40)
    
    # Simple drop
    data = [1, None, 2, float('nan'), 3]
    print(f"Original: {data}")
    print(f"Dropped: {drop_nan_values(data)}")
    
    # Table operations
    table = [
        [1, 2, 3],
        [None, 5, 6],
        [7, 8, None],
        [None, None, None],
    ]
    print(f"\nTable: {table}")
    print(f"Drop rows (any NaN): {drop_nan_rows(table, how='any')}")
    print(f"Drop rows (all NaN): {drop_nan_rows(table, how='all')}")
    print(f"Drop columns (any NaN): {drop_nan_columns(table, how='any')}")


def example_nested():
    """Example: Nested structure handling."""
    print("\n" + "=" * 40)
    print("Example 5: Nested Structure Handling")
    print("=" * 40)
    
    nested_data = {
        'user': {
            'name': 'Alice',
            'age': None,
            'scores': [90, float('nan'), 85]
        },
        'metadata': {
            'version': '1.0',
            'timestamp': float('nan')
        }
    }
    
    print(f"Original nested: {nested_data}")
    print(f"NaN count: {count_nan_nested(nested_data)}")
    
    converted = convert_nan_nested(nested_data, target='default', default='N/A')
    print(f"Converted: {converted}")


def example_serialization():
    """Example: Safe JSON serialization."""
    print("\n" + "=" * 40)
    print("Example 6: Safe JSON Serialization")
    print("=" * 40)
    
    data = {
        'temperature': 25.5,
        'humidity': float('nan'),
        'pressure': None,
        'readings': [1.2, float('nan'), 3.4]
    }
    
    print(f"Data with NaN: {data}")
    json_str = safe_json_dumps(data)
    print(f"Safe JSON: {json_str}")


def example_decorator():
    """Example: Using decorators."""
    print("\n" + "=" * 40)
    print("Example 7: NaN-Safe Decorators")
    print("=" * 40)
    
    @nan_safe(default=0)
    def safe_divide(a, b):
        return a / b
    
    print(f"safe_divide(10, 2) = {safe_divide(10, 2)}")
    print(f"safe_divide(float('nan'), 2) = {safe_divide(float('nan'), 2)}")
    print(f"safe_divide(10, None) = {safe_divide(10, None)}")
    
    @nan_safe(default='ERROR')
    def process_data(data):
        return f"Processed: {data}"
    
    print(f"\nprocess_data('valid') = {process_data('valid')}")
    print(f"process_data(float('nan')) = {process_data(float('nan'))}")


def example_real_world():
    """Example: Real-world data cleaning."""
    print("\n" + "=" * 40)
    print("Example 8: Real-World Data Cleaning")
    print("=" * 40)
    
    # Sensor readings with missing data
    readings = [
        {'sensor': 'A', 'value': 23.5},
        {'sensor': 'B', 'value': float('nan')},
        {'sensor': 'C', 'value': None},
        {'sensor': 'A', 'value': 24.1},
        {'sensor': 'B', 'value': 'N/A'},
    ]
    
    print("Raw readings:")
    for r in readings:
        print(f"  {r}")
    
    # Extract values and fill with mean
    values = [r['value'] for r in readings]
    filled_values = fill_nan_mean([v if isinstance(v, (int, float)) else float('nan') for v in values])
    
    print("\nFilled readings (with mean):")
    for i, r in enumerate(readings):
        r['value'] = filled_values[i]
        print(f"  {r}")
    
    # Safe JSON output
    print("\nJSON output:")
    print(safe_json_dumps(readings))


def main():
    """Run all examples."""
    print("\n" + "=" * 50)
    print("NaN Handler Utilities - Examples")
    print("=" * 50)
    
    example_detection()
    example_conversion()
    example_filling()
    example_dropping()
    example_nested()
    example_serialization()
    example_decorator()
    example_real_world()
    
    print("\n" + "=" * 50)
    print("All examples completed!")
    print("=" * 50)


if __name__ == '__main__':
    main()