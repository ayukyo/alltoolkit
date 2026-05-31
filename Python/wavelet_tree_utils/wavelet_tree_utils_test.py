#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wavelet Tree Utils 测试模块

作者: AllToolkit
日期: 2026-06-01
"""

import pytest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    WaveletTree,
    WaveletTreeCompact,
    create_wavelet_tree,
    wavelet_rank,
    wavelet_quantile,
    wavelet_range_count,
)


class TestWaveletTree:
    """WaveletTree 测试类"""
    
    def test_basic_creation(self):
        """测试基本创建"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTree(data, min_val=1, max_val=4)
        assert wt.size == 8
        assert len(wt) == 8
    
    def test_rank(self):
        """测试 rank 操作"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTree(data, min_val=1, max_val=4)
        
        # 统计 1 出现的次数
        assert wt.rank(1, 0, 7) == 3
        # 统计 2 出现的次数
        assert wt.rank(2, 0, 7) == 3
        # 统计 3 出现的次数
        assert wt.rank(3, 0, 7) == 1
        # 统计 4 出现的次数
        assert wt.rank(4, 0, 7) == 1
    
    def test_rank_partial_range(self):
        """测试部分区间的 rank"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTree(data, min_val=1, max_val=4)
        
        # 统计 [0, 3] 区间内 1 出现的次数
        assert wt.rank(1, 0, 3) == 2
        # 统计 [2, 5] 区间内 2 出现的次数
        assert wt.rank(2, 2, 5) == 1
    
    def test_quantize(self):
        """测试 quantize 操作"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTree(data, min_val=1, max_val=4)
        
        # 第 1 小的值
        assert wt.quantize(0, 7, 1) == 1
        # 第 2 小的值
        assert wt.quantize(0, 7, 2) == 1
        # 第 4 小的值
        assert wt.quantize(0, 7, 4) == 2
    
    def test_quantize_partial_range(self):
        """测试部分区间的 quantize"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTree(data, min_val=1, max_val=4)
        
        # [0, 2] 区间内第 2 小的值
        assert wt.quantize(0, 2, 2) == 1
        # [3, 6] 区间内第 2 小的值
        assert wt.quantize(3, 6, 2) == 2
    
    def test_range_count(self):
        """测试 range_count 操作"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTree(data, min_val=1, max_val=4)
        
        # 统计 [2, 3] 范围内的元素个数
        assert wt.range_count(0, 7, 2, 3) == 4
        # 统计 [1, 2] 范围内的元素个数
        assert wt.range_count(0, 7, 1, 2) == 6
    
    def test_get(self):
        """测试 get 操作"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTree(data, min_val=1, max_val=4)
        
        assert wt.get(0) == 1
        assert wt.get(1) == 2
        assert wt.get(2) == 1
        assert wt.get(3) == 3
    
    def test_getitem(self):
        """测试 __getitem__ 操作"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTree(data, min_val=1, max_val=4)
        
        assert wt[0] == 1
        assert wt[1] == 2
        assert wt[3] == 3
    
    def test_to_list(self):
        """测试 to_list 操作"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTree(data, min_val=1, max_val=4)
        
        assert wt.to_list() == data
    
    def test_empty_data(self):
        """测试空数据"""
        wt = WaveletTree([], min_val=1, max_val=4)
        assert wt.size == 0
        assert len(wt) == 0
    
    def test_value_range(self):
        """测试 value_range 属性"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTree(data, min_val=1, max_val=4)
        
        assert wt.value_range == (1, 4)
    
    def test_is_leaf(self):
        """测试 is_leaf 属性"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTree(data, min_val=1, max_val=4)
        
        # 根节点不是叶子
        assert wt.is_leaf == False
    
    def test_error_handling(self):
        """测试错误处理"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTree(data, min_val=1, max_val=4)
        
        # 测试越界索引
        with pytest.raises(IndexError):
            wt.rank(1, -1, 7)
        
        with pytest.raises(IndexError):
            wt.rank(1, 0, 10)
        
        # 测试越界值
        with pytest.raises(ValueError):
            wt.rank(10, 0, 7)
        
        with pytest.raises(ValueError):
            wt.quantize(0, 7, 0)
        
        with pytest.raises(ValueError):
            wt.quantize(0, 7, 10)


class TestWaveletTreeCompact:
    """WaveletTreeCompact 测试类"""
    
    def test_basic_creation(self):
        """测试基本创建"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTreeCompact(data, min_val=1, max_val=4)
        assert wt.size == 8
    
    def test_rank(self):
        """测试 rank 操作"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTreeCompact(data, min_val=1, max_val=4)
        
        assert wt.rank(1, 0, 7) == 3
        assert wt.rank(2, 0, 7) == 3
    
    def test_quantize(self):
        """测试 quantize 操作"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = WaveletTreeCompact(data, min_val=1, max_val=4)
        
        assert wt.quantize(0, 7, 1) == 1
        assert wt.quantize(0, 7, 2) == 1


class TestConvenienceFunctions:
    """便捷函数测试类"""
    
    def test_create_wavelet_tree(self):
        """测试 create_wavelet_tree"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = create_wavelet_tree(data)
        assert wt.size == 8
    
    def test_create_wavelet_tree_auto_range(self):
        """测试自动计算范围"""
        data = [5, 3, 7, 1, 9, 3, 5, 7]
        wt = create_wavelet_tree(data)
        assert wt.value_range == (1, 9)
    
    def test_wavelet_rank(self):
        """测试 wavelet_rank"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = create_wavelet_tree(data)
        assert wavelet_rank(wt, 1, 0, 7) == 3
    
    def test_wavelet_quantile(self):
        """测试 wavelet_quantile"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = create_wavelet_tree(data)
        assert wavelet_quantile(wt, 0, 7, 2) == 1
    
    def test_wavelet_range_count(self):
        """测试 wavelet_range_count"""
        data = [1, 2, 1, 3, 2, 1, 4, 2]
        wt = create_wavelet_tree(data)
        assert wavelet_range_count(wt, 0, 7, 2, 3) == 4
    
    def test_empty_data_error(self):
        """测试空数据错误"""
        with pytest.raises(ValueError):
            create_wavelet_tree([])


class TestEdgeCases:
    """边界情况测试类"""
    
    def test_single_value(self):
        """测试单一值"""
        data = [5, 5, 5, 5, 5]
        wt = create_wavelet_tree(data)
        assert wt.rank(5, 0, 4) == 5
        assert wt.quantize(0, 4, 3) == 5
    
    def test_two_values(self):
        """测试两个值"""
        data = [1, 2, 1, 2, 1, 2]
        wt = create_wavelet_tree(data)
        assert wt.rank(1, 0, 5) == 3
        assert wt.rank(2, 0, 5) == 3
    
    def test_large_range(self):
        """测试大范围值"""
        data = [1, 1000, 500, 2000, 100]
        wt = create_wavelet_tree(data)
        assert wt.size == 5
        assert wt.range_count(0, 4, 100, 1000) == 3


def run_tests():
    """运行所有测试"""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_tests()