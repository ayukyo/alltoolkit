"""
Reservoir Sampling Utils 测试套件

测试覆盖:
- 基本功能测试
- 统计均匀性测试
- 边界条件测试
- 加权采样测试
"""

import sys
import os
import unittest
import math
import random
from collections import Counter

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    ReservoirSampler,
    FastReservoirSampler,
    WeightedReservoirSampler,
    ReservoirSamplerWithReplacement,
    reservoir_sample,
    weighted_sample,
    stratified_reservoir_sample,
    two_pass_reservoir_sample,
    analyze_sample_distribution,
    SamplingStats
)


class TestReservoirSampler(unittest.TestCase):
    """经典水库采样测试"""
    
    def test_basic_sampling(self):
        """测试基本采样功能"""
        sampler = ReservoirSampler(5, seed=42)
        for i in range(100):
            sampler.add(i)
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 5)
        self.assertTrue(all(0 <= x < 100 for x in sample))
    
    def test_small_population(self):
        """测试总体小于采样大小的情况"""
        sampler = ReservoirSampler(10)
        for i in range(5):
            sampler.add(i)
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 5)
        self.assertEqual(sorted(sample), [0, 1, 2, 3, 4])
    
    def test_exact_fit(self):
        """测试总体等于采样大小的情况"""
        sampler = ReservoirSampler(5)
        for i in range(5):
            sampler.add(i)
        
        sample = sampler.sample()
        self.assertEqual(sorted(sample), [0, 1, 2, 3, 4])
    
    def test_add_all(self):
        """测试批量添加"""
        sampler = ReservoirSampler(3, seed=123)
        sampler.add_all(range(50))
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 3)
    
    def test_reset(self):
        """测试重置功能"""
        sampler = ReservoirSampler(3, seed=42)
        sampler.add_all(range(10))
        self.assertEqual(len(sampler.sample()), 3)
        
        sampler.reset(seed=42)
        self.assertEqual(len(sampler.sample()), 0)
        self.assertEqual(sampler.count, 0)
    
    def test_reproducibility(self):
        """测试结果可复现"""
        sampler1 = ReservoirSampler(5, seed=999)
        sampler1.add_all(range(100))
        
        sampler2 = ReservoirSampler(5, seed=999)
        sampler2.add_all(range(100))
        
        self.assertEqual(sampler1.sample(), sampler2.sample())
    
    def test_invalid_k(self):
        """测试无效采样大小"""
        with self.assertRaises(ValueError):
            ReservoirSampler(0)
        with self.assertRaises(ValueError):
            ReservoirSampler(-1)
    
    def test_properties(self):
        """测试属性"""
        sampler = ReservoirSampler(5)
        self.assertEqual(sampler.size, 5)
        self.assertEqual(sampler.count, 0)
        self.assertFalse(sampler.is_ready)
        
        sampler.add_all(range(5))
        self.assertTrue(sampler.is_ready)
        self.assertEqual(sampler.count, 5)


class TestFastReservoirSampler(unittest.TestCase):
    """高效水库采样测试"""
    
    def test_basic_sampling(self):
        """测试基本采样功能"""
        sampler = FastReservoirSampler(5, seed=42)
        for i in range(100):
            sampler.add(i)
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 5)
        self.assertTrue(all(0 <= x < 100 for x in sample))
    
    def test_small_population(self):
        """测试小总体情况"""
        sampler = FastReservoirSampler(10)
        for i in range(5):
            sampler.add(i)
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 5)
    
    def test_large_dataset(self):
        """测试大数据集"""
        sampler = FastReservoirSampler(100, seed=42)
        for i in range(100000):
            sampler.add(i)
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 100)
        unique = len(set(sample))
        self.assertEqual(unique, 100)  # 无重复（对于均匀采样）


class TestWeightedReservoirSampler(unittest.TestCase):
    """加权水库采样测试"""
    
    def test_basic_weighted(self):
        """测试基本加权采样"""
        sampler = WeightedReservoirSampler(2, seed=42)
        sampler.add('a', weight=1.0)
        sampler.add('b', weight=2.0)
        sampler.add('c', weight=3.0)
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 2)
    
    def test_weight_distribution(self):
        """测试权重分布正确性"""
        # 高权重元素应更常被选中
        results = Counter()
        for seed in range(100):
            sampler = WeightedReservoirSampler(1, seed=seed)
            sampler.add('low', weight=1.0)
            sampler.add('high', weight=9.0)
            results[sampler.sample()[0]] += 1
        
        # 'high' 应该被选中更多次
        self.assertGreater(results['high'], results['low'])
    
    def test_equal_weights(self):
        """测试等权重情况"""
        sampler = WeightedReservoirSampler(3, seed=42)
        for i in range(10):
            sampler.add(i, weight=1.0)
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 3)
    
    def test_invalid_weight(self):
        """测试无效权重"""
        sampler = WeightedReservoirSampler(2)
        with self.assertRaises(ValueError):
            sampler.add('item', weight=0)
        with self.assertRaises(ValueError):
            sampler.add('item', weight=-1)
    
    def test_add_all_weighted(self):
        """测试批量添加加权元素"""
        sampler = WeightedReservoirSampler(3, seed=42)
        items = [('a', 1.0), ('b', 2.0), ('c', 3.0), ('d', 4.0)]
        sampler.add_all(iter(items))
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 3)


class TestReservoirSamplerWithReplacement(unittest.TestCase):
    """有放回采样测试"""
    
    def test_basic(self):
        """测试基本功能"""
        sampler = ReservoirSamplerWithReplacement(5, seed=42)
        for i in range(100):
            sampler.add(i)
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 5)
    
    def test_allows_duplicates(self):
        """测试允许重复"""
        # 在大数据集上，有放回采样应该允许重复
        sampler = ReservoirSamplerWithReplacement(10, seed=42)
        for i in range(1000):
            sampler.add(i)
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 10)
        # 检查是否有重复（对于大数据集和小采样数，重复概率较低但存在可能）
        # 此处只验证长度正确


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_reservoir_sample_func(self):
        """测试 reservoir_sample 函数"""
        sample = reservoir_sample(range(100), 10, seed=42)
        self.assertEqual(len(sample), 10)
        self.assertTrue(all(0 <= x < 100 for x in sample))
    
    def test_weighted_sample_func(self):
        """测试 weighted_sample 函数"""
        items = [('a', 1.0), ('b', 2.0), ('c', 3.0), ('d', 4.0)]
        sample = weighted_sample(iter(items), 2, seed=42)
        self.assertEqual(len(sample), 2)
    
    def test_stratified_sample(self):
        """测试分层采样"""
        items = [
            ('a', 1), ('b', 1), ('c', 2), ('d', 2), ('e', 3)
        ]
        result = stratified_reservoir_sample(
            (x for x in items),
            k=2,
            strata_func=lambda x: x[1],
            seed=42
        )
        
        # 应该有 3 个层级
        self.assertEqual(len(result), 3)
    
    def test_two_pass_sample(self):
        """测试两遍扫描采样"""
        items = list(range(100))
        sample = two_pass_reservoir_sample(items, 10, seed=42)
        self.assertEqual(len(sample), 10)


class TestDistributionAnalysis(unittest.TestCase):
    """分布分析测试"""
    
    def test_analyze_empty(self):
        """测试空样本分析"""
        result = analyze_sample_distribution([])
        self.assertTrue(result['empty'])
    
    def test_analyze_uniform(self):
        """测试均匀分布分析"""
        sample = list(range(100))
        result = analyze_sample_distribution(sample)
        
        self.assertEqual(result['total'], 100)
        self.assertEqual(result['unique'], 100)
        self.assertEqual(result['duplicates'], 0)
    
    def test_analyze_with_duplicates(self):
        """测试有重复的分析"""
        sample = [1, 1, 1, 2, 2, 3]
        result = analyze_sample_distribution(sample)
        
        self.assertEqual(result['total'], 6)
        self.assertEqual(result['unique'], 3)
        self.assertEqual(result['duplicates'], 3)
    
    def test_stats_dataclass(self):
        """测试统计信息数据类"""
        stats = SamplingStats(
            total_items=100,
            sample_size=10,
            unique_items=10,
            duplicates=0
        )
        
        d = stats.to_dict()
        self.assertEqual(d['total_items'], 100)
        self.assertEqual(d['sample_size'], 10)


class TestStatisticalProperties(unittest.TestCase):
    """统计属性测试"""
    
    def test_uniformity(self):
        """测试采样均匀性"""
        # 统计每个元素被选中的频率
        counts = Counter()
        n_items = 20
        k = 10
        n_trials = 1000
        
        for seed in range(n_trials):
            sampler = ReservoirSampler(k, seed=seed)
            sampler.add_all(range(n_items))
            for item in sampler.sample():
                counts[item] += 1
        
        # 每个元素大约应该被选中 n_trials * k / n_items 次
        expected = n_trials * k / n_items
        tolerance = expected * 0.15  # 15% 容差
        
        for i in range(n_items):
            self.assertAlmostEqual(counts[i], expected, delta=tolerance,
                                  msg=f"Element {i} count {counts[i]} not close to expected {expected}")
    
    def test_independence(self):
        """测试采样独立性"""
        # 多次采样应该产生不同结果
        samples = set()
        for seed in range(100):
            sample = tuple(sorted(reservoir_sample(range(100), 5, seed=seed)))
            samples.add(sample)
        
        # 应该有大量不同的组合
        self.assertGreater(len(samples), 90)


class TestEdgeCases(unittest.TestCase):
    """边界条件测试"""
    
    def test_single_element(self):
        """测试单个元素"""
        sampler = ReservoirSampler(5)
        sampler.add(42)
        
        self.assertEqual(sampler.sample(), [42])
    
    def test_k_equals_one(self):
        """测试 k=1 的情况"""
        sampler = ReservoirSampler(1, seed=42)
        sampler.add_all(range(100))
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 1)
    
    def test_large_k(self):
        """测试大采样大小"""
        sampler = ReservoirSampler(1000, seed=42)
        sampler.add_all(range(500))
        
        # 应返回所有元素
        sample = sampler.sample()
        self.assertEqual(len(sample), 500)
    
    def test_string_elements(self):
        """测试字符串元素"""
        sampler = ReservoirSampler(3, seed=42)
        sampler.add_all(['a', 'b', 'c', 'd', 'e'])
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 3)
        self.assertTrue(all(s in 'abcde' for s in sample))
    
    def test_mixed_types(self):
        """测试混合类型"""
        sampler = ReservoirSampler(3, seed=42)
        sampler.add_all([1, 'a', None, 2.5, (1, 2)])
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)