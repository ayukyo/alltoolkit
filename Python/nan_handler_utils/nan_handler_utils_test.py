#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - NaN Handler Utilities Test Suite
===============================================
Comprehensive test suite for nan_handler_utils module.
"""

import math
import sys
sys.path.insert(0, '.')

from mod import (
    # Detection
    is_nan, is_not_nan, detect_nan_indices, detect_nan_keys,
    # Statistics
    nan_count, nan_percentage, nan_summary,
    # Conversion
    nan_to_none, nan_to_default, convert_nan_list, convert_nan_dict,
    # Filling
    fill_nan_mean, fill_nan_median, fill_nan_mode, fill_nan_constant,
    fill_nan_interpolate, fill_nan_custom,
    # Dropping
    drop_nan_values, drop_nan_rows, drop_nan_columns, drop_nan_dict_keys,
    # Nested
    convert_nan_nested, count_nan_nested,
    # Batch
    batch_nan_to_none, batch_fill_nan,
    # Serialization
    safe_serialize, safe_json_dumps,
    # Decorators
    validate_no_nan, nan_safe,
    # Utilities
    replace_nan_strings, get_valid_values, get_nan_values,
    first_valid_index, last_valid_index,
    # Constants
    NaN_STRING_PATTERNS,
)


def test_is_nan():
    """Test NaN detection."""
    print("Testing is_nan()...")
    
    # Float NaN
    assert is_nan(float('nan')) == True
    assert is_nan(float('inf'), include_inf=True) == True
    assert is_nan(float('inf'), include_inf=False) == False
    
    # None
    assert is_nan(None) == True
    assert is_nan(None, include_none=False) == False
    
    # Strings
    assert is_nan('nan') == True
    assert is_nan('N/A') == True
    assert is_nan('NULL') == True
    assert is_nan('') == False  # Empty string not considered NaN by default
    assert is_nan('normal') == False
    assert is_nan('N/A', include_strings=False) == False
    
    # Valid values
    assert is_nan(42) == False
    assert is_nan(0) == False
    assert is_nan('hello') == False
    assert is_nan([1, 2, 3]) == False
    
    # Custom patterns
    assert is_nan('CUSTOM_NAN', custom_patterns=['CUSTOM_NAN']) == True
    
    print("  ✓ is_nan tests passed")


def test_is_not_nan():
    """Test is_not_nan function."""
    print("Testing is_not_nan()...")
    
    assert is_not_nan(42) == True
    assert is_not_nan(float('nan')) == False
    assert is_not_nan(None) == False
    assert is_not_nan('hello') == True
    
    print("  ✓ is_not_nan tests passed")


def test_detect_nan_indices():
    """Test NaN index detection."""
    print("Testing detect_nan_indices()...")
    
    data = [1, None, 3, float('nan'), 5]
    indices = detect_nan_indices(data)
    assert indices == [1, 3]
    
    # No NaN
    assert detect_nan_indices([1, 2, 3]) == []
    
    # All NaN
    assert detect_nan_indices([None, None, None]) == [0, 1, 2]
    
    print("  ✓ detect_nan_indices tests passed")


def test_detect_nan_keys():
    """Test NaN key detection in dicts."""
    print("Testing detect_nan_keys()...")
    
    data = {'a': 1, 'b': None, 'c': 3, 'd': float('nan')}
    keys = detect_nan_keys(data)
    assert 'b' in keys
    assert 'd' in keys
    assert 'a' not in keys
    assert 'c' not in keys
    
    print("  ✓ detect_nan_keys tests passed")


def test_nan_count():
    """Test NaN counting."""
    print("Testing nan_count()...")
    
    assert nan_count([1, None, 3, float('nan')]) == 2
    assert nan_count([1, 2, 3]) == 0
    assert nan_count([None, None, None]) == 3
    assert nan_count({'a': 1, 'b': None}) == 1
    
    print("  ✓ nan_count tests passed")


def test_nan_percentage():
    """Test NaN percentage calculation."""
    print("Testing nan_percentage()...")
    
    assert nan_percentage([1, None, 3, float('nan')]) == 50.0
    assert nan_percentage([1, 2, 3, 4]) == 0.0
    assert nan_percentage([None, None]) == 100.0
    
    print("  ✓ nan_percentage tests passed")


def test_nan_summary():
    """Test NaN summary generation."""
    print("Testing nan_summary()...")
    
    summary = nan_summary([1, None, 3, float('nan'), 5])
    assert summary['total'] == 5
    assert summary['nan_count'] == 2
    assert summary['valid_count'] == 3
    assert summary['nan_percentage'] == 40.0
    
    print("  ✓ nan_summary tests passed")


def test_nan_to_none():
    """Test NaN to None conversion."""
    print("Testing nan_to_none()...")
    
    assert nan_to_none(float('nan')) is None
    assert nan_to_none(None) is None
    assert nan_to_none('N/A') is None
    assert nan_to_none(42) == 42
    assert nan_to_none('hello') == 'hello'
    
    print("  ✓ nan_to_none tests passed")


def test_nan_to_default():
    """Test NaN to default conversion."""
    print("Testing nan_to_default()...")
    
    assert nan_to_default(float('nan'), default=-1) == -1
    assert nan_to_default('N/A', default='missing') == 'missing'
    assert nan_to_default(42, default=0) == 42
    
    print("  ✓ nan_to_default tests passed")


def test_convert_nan_list():
    """Test list NaN conversion."""
    print("Testing convert_nan_list()...")
    
    data = [1, None, 3, float('nan')]
    
    # To None
    result = convert_nan_list(data, target='none')
    assert result == [1, None, 3, None]
    
    # To default
    result = convert_nan_list(data, target='default', default=0)
    assert result == [1, 0, 3, 0]
    
    # Remove
    result = convert_nan_list(data, target='remove')
    assert result == [1, 3]
    
    print("  ✓ convert_nan_list tests passed")


def test_convert_nan_dict():
    """Test dictionary NaN conversion."""
    print("Testing convert_nan_dict()...")
    
    data = {'a': 1, 'b': None, 'c': float('nan')}
    
    # To None
    result = convert_nan_dict(data, target='none')
    assert result['a'] == 1
    assert result['b'] is None
    assert result['c'] is None
    
    # To default
    result = convert_nan_dict(data, target='default', default=0)
    assert result['b'] == 0
    assert result['c'] == 0
    
    # Remove keys
    result = convert_nan_dict(data, remove_keys=True)
    assert result == {'a': 1}
    
    print("  ✓ convert_nan_dict tests passed")


def test_fill_nan_mean():
    """Test mean filling."""
    print("Testing fill_nan_mean()...")
    
    data = [1, float('nan'), 3, float('nan')]
    result = fill_nan_mean(data)
    
    # Mean of [1, 3] is 2
    assert result[0] == 1
    assert result[1] == 2.0
    assert result[2] == 3
    assert result[3] == 2.0
    
    # No valid values
    result = fill_nan_mean([float('nan'), float('nan')], default=100)
    assert result == [100, 100]
    
    print("  ✓ fill_nan_mean tests passed")


def test_fill_nan_median():
    """Test median filling."""
    print("Testing fill_nan_median()...")
    
    data = [1, float('nan'), 2, float('nan'), 100]
    result = fill_nan_median(data)
    
    # Median of [1, 2, 100] is 2
    assert result[0] == 1
    assert result[1] == 2.0
    assert result[2] == 2
    assert result[3] == 2.0
    assert result[4] == 100
    
    print("  ✓ fill_nan_median tests passed")


def test_fill_nan_mode():
    """Test mode filling."""
    print("Testing fill_nan_mode()...")
    
    data = [1, None, 1, None, 2, 1]
    result = fill_nan_mode(data)
    
    # Mode of [1, 1, 2, 1] is 1
    assert result[0] == 1
    assert result[1] == 1
    assert result[2] == 1
    assert result[3] == 1
    assert result[4] == 2
    assert result[5] == 1
    
    print("  ✓ fill_nan_mode tests passed")


def test_fill_nan_constant():
    """Test constant filling."""
    print("Testing fill_nan_constant()...")
    
    data = [1, None, 3]
    result = fill_nan_constant(data, constant=-999)
    assert result == [1, -999, 3]
    
    print("  ✓ fill_nan_constant tests passed")


def test_fill_nan_interpolate():
    """Test interpolation filling."""
    print("Testing fill_nan_interpolate()...")
    
    # Linear interpolation
    data = [1, float('nan'), 3]
    result = fill_nan_interpolate(data, method='linear')
    assert result == [1, 2.0, 3]
    
    # Forward fill
    data = [1, float('nan'), float('nan'), 4]
    result = fill_nan_interpolate(data, method='forward')
    assert result == [1, 1, 1, 4]
    
    # Backward fill
    data = [float('nan'), float('nan'), 3, 4]
    result = fill_nan_interpolate(data, method='backward')
    assert result == [3, 3, 3, 4]
    
    print("  ✓ fill_nan_interpolate tests passed")


def test_fill_nan_custom():
    """Test custom filling function."""
    print("Testing fill_nan_custom()...")
    
    data = [1, None, 3, None]
    result = fill_nan_custom(data, lambda v, i, lst: i * 10)
    assert result == [1, 10, 3, 30]
    
    print("  ✓ fill_nan_custom tests passed")


def test_drop_nan_values():
    """Test dropping NaN values."""
    print("Testing drop_nan_values()...")
    
    data = [1, None, 3, float('nan'), 5]
    result = drop_nan_values(data)
    assert result == [1, 3, 5]
    
    print("  ✓ drop_nan_values tests passed")


def test_drop_nan_rows():
    """Test dropping NaN rows."""
    print("Testing drop_nan_rows()...")
    
    data = [[1, 2], [None, 4], [None, None]]
    
    # Drop if any NaN
    result = drop_nan_rows(data, how='any')
    assert result == [[1, 2]]
    
    # Drop if all NaN
    result = drop_nan_rows(data, how='all')
    assert result == [[1, 2], [None, 4]]
    
    print("  ✓ drop_nan_rows tests passed")


def test_drop_nan_columns():
    """Test dropping NaN columns."""
    print("Testing drop_nan_columns()...")
    
    data = [[1, None], [2, None], [3, 4]]
    
    # Drop if any NaN
    result = drop_nan_columns(data, how='any')
    assert result == [[1], [2], [3]]
    
    # Drop if all NaN
    result = drop_nan_columns(data, how='all')
    assert result == [[1, None], [2, None], [3, 4]]
    
    print("  ✓ drop_nan_columns tests passed")


def test_drop_nan_dict_keys():
    """Test dropping NaN dict keys."""
    print("Testing drop_nan_dict_keys()...")
    
    data = {'a': 1, 'b': None, 'c': 3, 'd': float('nan')}
    result = drop_nan_dict_keys(data)
    assert result == {'a': 1, 'c': 3}
    
    print("  ✓ drop_nan_dict_keys tests passed")


def test_convert_nan_nested():
    """Test nested structure conversion."""
    print("Testing convert_nan_nested()...")
    
    nested = {'a': 1, 'b': [None, 3], 'c': {'x': float('nan')}}
    result = convert_nan_nested(nested, target='default', default=0)
    
    assert result['a'] == 1
    assert result['b'] == [0, 3]
    assert result['c']['x'] == 0
    
    # Remove
    result = convert_nan_nested([1, None, [None, 3]], target='remove')
    assert result == [1, [3]]
    
    print("  ✓ convert_nan_nested tests passed")


def test_count_nan_nested():
    """Test counting NaN in nested structures."""
    print("Testing count_nan_nested()...")
    
    nested = {'a': 1, 'b': [None, 3], 'c': {'x': float('nan')}}
    count = count_nan_nested(nested)
    assert count == 2
    
    print("  ✓ count_nan_nested tests passed")


def test_batch_nan_to_none():
    """Test batch NaN to None conversion."""
    print("Testing batch_nan_to_none()...")
    
    # List
    result = batch_nan_to_none([1, None, 3])
    assert result == [1, None, 3]
    
    # Dict
    result = batch_nan_to_none({'a': 1, 'b': float('nan')})
    assert result['b'] is None
    
    print("  ✓ batch_nan_to_none tests passed")


def test_batch_fill_nan():
    """Test batch NaN filling."""
    print("Testing batch_fill_nan()...")
    
    result = batch_fill_nan([1, None, 3, None], strategy='constant', value=0)
    assert result == [1, 0, 3, 0]
    
    result = batch_fill_nan([1, float('nan'), 3], strategy='mean')
    assert result == [1, 2.0, 3]
    
    print("  ✓ batch_fill_nan tests passed")


def test_safe_serialize():
    """Test safe serialization."""
    print("Testing safe_serialize()...")
    
    data = {'a': float('nan'), 'b': 2, 'c': None}
    result = safe_serialize(data, nan_replacement='N/A')
    assert result['a'] == 'N/A'
    assert result['b'] == 2
    assert result['c'] == 'N/A'
    
    print("  ✓ safe_serialize tests passed")


def test_safe_json_dumps():
    """Test safe JSON dumps."""
    print("Testing safe_json_dumps()...")
    
    data = {'a': float('nan'), 'b': 2}
    result = safe_json_dumps(data)
    assert 'null' in result
    assert '"b": 2' in result
    
    # Nested
    data = {'list': [1, float('nan'), 3]}
    result = safe_json_dumps(data)
    assert '[1, null, 3]' in result
    
    print("  ✓ safe_json_dumps tests passed")


def test_validate_no_nan():
    """Test validate_no_nan decorator."""
    print("Testing validate_no_nan decorator...")
    
    @validate_no_nan
    def add(a, b):
        return a + b
    
    # Valid inputs
    assert add(1, 2) == 3
    
    # NaN input should raise
    try:
        add(1, float('nan'))
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("  ✓ validate_no_nan tests passed")


def test_nan_safe():
    """Test nan_safe decorator."""
    print("Testing nan_safe decorator...")
    
    @nan_safe(default=0)
    def square(x):
        return x * x
    
    assert square(4) == 16
    assert square(float('nan')) == 0
    assert square(None) == 0
    
    print("  ✓ nan_safe tests passed")


def test_replace_nan_strings():
    """Test NaN string replacement."""
    print("Testing replace_nan_strings()...")
    
    data = 'N/A'
    result = replace_nan_strings(data, replacement='missing')
    assert result == 'missing'
    
    # List
    data = ['hello', 'N/A', 'world']
    result = replace_nan_strings(data, replacement='MISSING')
    assert result == ['hello', 'MISSING', 'world']
    
    print("  ✓ replace_nan_strings tests passed")


def test_get_valid_values():
    """Test getting valid values."""
    print("Testing get_valid_values()...")
    
    data = [1, None, 3, float('nan'), 5]
    result = get_valid_values(data)
    assert result == [1, 3, 5]
    
    print("  ✓ get_valid_values tests passed")


def test_get_nan_values():
    """Test getting NaN values."""
    print("Testing get_nan_values()...")
    
    data = [1, None, 3, float('nan'), 5]
    result = get_nan_values(data)
    assert len(result) == 2
    assert None in result
    assert any(math.isnan(v) for v in result if isinstance(v, float))
    
    print("  ✓ get_nan_values tests passed")


def test_first_valid_index():
    """Test finding first valid index."""
    print("Testing first_valid_index()...")
    
    data = [None, None, 3, 4]
    assert first_valid_index(data) == 2
    
    data = [1, 2, 3]
    assert first_valid_index(data) == 0
    
    data = [None, None, None]
    assert first_valid_index(data) is None
    
    print("  ✓ first_valid_index tests passed")


def test_last_valid_index():
    """Test finding last valid index."""
    print("Testing last_valid_index()...")
    
    data = [1, 2, None, None]
    assert last_valid_index(data) == 1
    
    data = [1, 2, 3]
    assert last_valid_index(data) == 2
    
    data = [None, None, None]
    assert last_valid_index(data) is None
    
    print("  ✓ last_valid_index tests passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("NaN Handler Utilities - Test Suite")
    print("=" * 50 + "\n")
    
    tests = [
        test_is_nan,
        test_is_not_nan,
        test_detect_nan_indices,
        test_detect_nan_keys,
        test_nan_count,
        test_nan_percentage,
        test_nan_summary,
        test_nan_to_none,
        test_nan_to_default,
        test_convert_nan_list,
        test_convert_nan_dict,
        test_fill_nan_mean,
        test_fill_nan_median,
        test_fill_nan_mode,
        test_fill_nan_constant,
        test_fill_nan_interpolate,
        test_fill_nan_custom,
        test_drop_nan_values,
        test_drop_nan_rows,
        test_drop_nan_columns,
        test_drop_nan_dict_keys,
        test_convert_nan_nested,
        test_count_nan_nested,
        test_batch_nan_to_none,
        test_batch_fill_nan,
        test_safe_serialize,
        test_safe_json_dumps,
        test_validate_no_nan,
        test_nan_safe,
        test_replace_nan_strings,
        test_get_valid_values,
        test_get_nan_values,
        test_first_valid_index,
        test_last_valid_index,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  ✗ Test failed: {test.__name__}")
            print(f"    Error: {e}")
    
    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)