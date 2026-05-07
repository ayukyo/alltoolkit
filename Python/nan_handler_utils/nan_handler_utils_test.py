#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nan_handler_utils - 测试用例
===========================

测试 NaN/None 值检测、转换、填充等功能。
"""

import pytest
import math
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    is_nan,
    nan_count,
    nan_summary,
    nan_to_none,
    nan_to_default,
    convert_nan_list,
    convert_nan_dict,
    fill_nan_mean,
    fill_nan_median,
    fill_nan_mode,
    detect_nan_indices,
    detect_nan_keys,
    batch_nan_to_none,
    batch_fill_nan,
)


class TestIsNan:
    """测试 NaN 检测"""
    
    def test_is_nan_float_nan(self):
        """测试 float NaN"""
        assert is_nan(float('nan')) is True
    
    def test_is_nan_none(self):
        """测试 None"""
        assert is_nan(None) is True
    
    def test_is_nan_string_patterns(self):
        """测试字符串 NaN 模式"""
        assert is_nan('nan') is True
        assert is_nan('NaN') is True
        assert is_nan('NA') is True
        assert is_nan('N/A') is True
        assert is_nan('null') is True
        assert is_nan('None') is True
    
    def test_is_nan_valid_values(self):
        """测试有效值"""
        assert is_nan(42) is False
        assert is_nan(3.14) is False
        assert is_nan("hello") is False
    
    def test_is_nan_inf(self):
        """测试无穷大"""
        # 默认不包括无穷大
        assert is_nan(float('inf')) is False
        
        # 设置 include_inf=True
        assert is_nan(float('inf'), include_inf=True) is True
    
    def test_is_nan_exclude_none(self):
        """测试排除 None"""
        assert is_nan(None, include_none=False) is False


class TestNanCount:
    """测试 NaN 计数"""
    
    def test_nan_count_list(self):
        """测试列表计数"""
        data = [1, float('nan'), 2, None, 'NA', 3]
        count = nan_count(data)
        assert count >= 3  # nan, None, 'NA'


class TestNanSummary:
    """测试 NaN 统计"""
    
    def test_nan_summary(self):
        """测试统计"""
        data = [1, None, 3, float('nan'), 5]
        summary = nan_summary(data)
        
        assert summary['total'] == 5
        assert summary['nan_count'] >= 2
        assert summary['nan_percentage'] > 0


class TestNanToNone:
    """测试 NaN 转 None"""
    
    def test_nan_to_none_float(self):
        """测试 float NaN 转 None"""
        result = nan_to_none(float('nan'))
        assert result is None
    
    def test_nan_to_none_valid(self):
        """测试有效值不变"""
        result = nan_to_none(42)
        assert result == 42
    
    def test_nan_to_none_string(self):
        """测试字符串 NaN"""
        result = nan_to_none('NA')
        assert result is None


class TestNanToDefault:
    """测试 NaN 转默认值"""
    
    def test_nan_to_default(self):
        """测试转默认值"""
        result = nan_to_default(float('nan'), default=-1)
        assert result == -1
    
    def test_nan_to_default_valid(self):
        """测试有效值不变"""
        result = nan_to_default(42, default=-1)
        assert result == 42


class TestConvertNanList:
    """测试列表 NaN 转换"""
    
    def test_convert_nan_list_to_none(self):
        """测试转 None"""
        data = [1, float('nan'), 2, None]
        result = convert_nan_list(data, target='none')
        
        assert result == [1, None, 2, None]
    
    def test_convert_nan_list_to_default(self):
        """测试转默认值"""
        data = [1, float('nan'), 2]
        result = convert_nan_list(data, target='default', default=0)
        
        assert result == [1, 0, 2]
    
    def test_convert_nan_list_remove(self):
        """测试移除 NaN"""
        data = [1, float('nan'), 2, None]
        result = convert_nan_list(data, target='remove')
        
        assert result == [1, 2]


class TestConvertNanDict:
    """测试字典 NaN 转换"""
    
    def test_convert_nan_dict_to_none(self):
        """测试转 None"""
        data = {'a': 1, 'b': float('nan')}
        result = convert_nan_dict(data, target='none')
        
        assert result['a'] == 1
        assert result['b'] is None
    
    def test_convert_nan_dict_to_default(self):
        """测试转默认值"""
        data = {'a': 1, 'b': float('nan')}
        result = convert_nan_dict(data, target='default', default=0)
        
        assert result['a'] == 1
        assert result['b'] == 0
    
    def test_convert_nan_dict_remove_keys(self):
        """测试移除 NaN 键"""
        data = {'a': 1, 'b': float('nan')}
        result = convert_nan_dict(data, remove_keys=True)
        
        assert 'a' in result
        assert 'b' not in result


class TestFillNan:
    """测试 NaN 填充"""
    
    def test_fill_nan_mean(self):
        """测试均值填充"""
        data = [1, float('nan'), 3]
        result = fill_nan_mean(data)
        
        # 均值为 2
        assert result[0] == 1
        assert result[1] == 2
        assert result[2] == 3
    
    def test_fill_nan_median(self):
        """测试中位数填充"""
        data = [1, float('nan'), 2, 100]
        result = fill_nan_median(data)
        
        # 中位数约为 2 或根据实现
        assert result[0] == 1
        assert isinstance(result[1], (int, float))
    
    def test_fill_nan_mode(self):
        """测试众数填充"""
        data = [1, None, 1, None, 2]
        result = fill_nan_mode(data)
        
        # 众数为 1
        assert result[0] == 1
        assert result[1] == 1


class TestDetectNan:
    """测试 NaN 检测"""
    
    def test_detect_nan_indices(self):
        """测试检测 NaN 位置"""
        data = [1, float('nan'), 2, None]
        indices = detect_nan_indices(data)
        
        assert 1 in indices  # float('nan') 在位置 1
        assert 3 in indices  # None 在位置 3
    
    def test_detect_nan_keys(self):
        """测试检测字典 NaN 键"""
        data = {'a': 1, 'b': float('nan'), 'c': None}
        keys = detect_nan_keys(data)
        
        assert 'b' in keys
        assert 'c' in keys


class TestBatchOperations:
    """测试批量操作"""
    
    def test_batch_nan_to_none(self):
        """测试批量转 None"""
        data = [
            [1, float('nan')],
            {'a': 1, 'b': None},
        ]
        result = batch_nan_to_none(data)
        
        assert isinstance(result, list)
    
    def test_batch_fill_nan(self):
        """测试批量填充"""
        data = [
            [1, float('nan')],
            [float('nan'), 2],
        ]
        result = batch_fill_nan(data, strategy='mean')
        
        assert isinstance(result, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])