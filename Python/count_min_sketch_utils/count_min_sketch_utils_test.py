"""
Count-Min Sketch 工具模块测试

测试覆盖:
- 基本功能（添加、估计、清空）
- 参数验证
- 合并操作
- 序列化/反序列化
- Top-K 追踪
- Builder 模式
- 边界条件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import unittest
from mod import (
    CountMinSketch,
    CountMinSketchBuilder,
    TopKTracker,
    create_optimal_sketch,
    frequency_analysis,
    count_min_sketch
)


class TestCountMinSketch(unittest.TestCase):
    """CountMinSketch 基础测试"""
    
    def test_basic_add_and_estimate(self):
        """测试基本添加和估计功能"""
        cms = CountMinSketch(width=1000, depth=5)
        
        # 添加单个元素
        cms.add("test")
        self.assertEqual(cms.estimate("test"), 1)
        
        # 多次添加
        cms.add("test", 5)
        self.assertGreaterEqual(cms.estimate("test"), 6)
        
        # 未添加的元素估计为 0
        self.assertEqual(cms.estimate("nonexistent"), 0)
    
    def test_add_with_count(self):
        """测试批量添加"""
        cms = CountMinSketch(width=1000, depth=5)
        cms.add("item", 100)
        self.assertGreaterEqual(cms.estimate("item"), 100)
    
    def test_total_count(self):
        """测试总计数"""
        cms = CountMinSketch(width=1000, depth=5)
        cms.add("a", 10)
        cms.add("b", 20)
        cms.add("c", 30)
        self.assertEqual(cms.total_count, 60)
    
    def test_clear(self):
        """测试清空功能"""
        cms = CountMinSketch(width=1000, depth=5)
        cms.add("test", 100)
        cms.clear()
        self.assertEqual(cms.estimate("test"), 0)
        self.assertEqual(cms.total_count, 0)
    
    def test_contains(self):
        """测试 __contains__ 方法"""
        cms = CountMinSketch(width=1000, depth=5)
        cms.add("exists")
        self.assertIn("exists", cms)
        self.assertNotIn("not_exists", cms)
    
    def test_len(self):
        """测试 __len__ 方法"""
        cms = CountMinSketch(width=1000, depth=5)
        self.assertEqual(len(cms), 0)
        cms.add("a", 10)
        self.assertEqual(len(cms), 10)
    
    def test_repr(self):
        """测试 __repr__ 方法"""
        cms = CountMinSketch(width=100, depth=3)
        repr_str = repr(cms)
        self.assertIn("CountMinSketch", repr_str)
        self.assertIn("width=100", repr_str)
        self.assertIn("depth=3", repr_str)
    
    def test_memory_usage(self):
        """测试内存使用计算"""
        cms = CountMinSketch(width=1000, depth=5)
        # 1000 * 5 * 8 bytes (假设 int 为 8 字节)
        self.assertEqual(cms.memory_usage, 1000 * 5 * 8)
    
    def test_properties(self):
        """测试属性访问"""
        cms = CountMinSketch(width=500, depth=7)
        self.assertEqual(cms.width, 500)
        self.assertEqual(cms.depth, 7)
    
    def test_invalid_parameters(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            CountMinSketch(width=0, depth=5)
        with self.assertRaises(ValueError):
            CountMinSketch(width=100, depth=0)
        with self.assertRaises(ValueError):
            CountMinSketch(width=-1, depth=5)
    
    def test_negative_count(self):
        """测试负数计数"""
        cms = CountMinSketch()
        with self.assertRaises(ValueError):
            cms.add("test", -1)
    
    def test_different_types(self):
        """测试不同类型元素"""
        cms = CountMinSketch(width=1000, depth=5)
        
        # 字符串
        cms.add("string")
        self.assertGreaterEqual(cms.estimate("string"), 1)
        
        # 数字
        cms.add(123)
        self.assertGreaterEqual(cms.estimate(123), 1)
        
        # 字节
        cms.add(b"bytes")
        self.assertGreaterEqual(cms.estimate(b"bytes"), 1)
        
        # 元组
        cms.add((1, 2, 3))
        self.assertGreaterEqual(cms.estimate((1, 2, 3)), 1)


class TestCountMinSketchMerge(unittest.TestCase):
    """测试合并功能"""
    
    def test_basic_merge(self):
        """测试基本合并"""
        cms1 = CountMinSketch(width=100, depth=5)
        cms2 = CountMinSketch(width=100, depth=5)
        
        cms1.add("a", 10)
        cms2.add("a", 5)
        
        merged = cms1.merge(cms2)
        self.assertEqual(merged.estimate("a"), 15)
        self.assertEqual(merged.total_count, 15)
    
    def test_merge_different_items(self):
        """测试不同元素合并"""
        cms1 = CountMinSketch(width=100, depth=5)
        cms2 = CountMinSketch(width=100, depth=5)
        
        cms1.add("a", 10)
        cms1.add("b", 20)
        cms2.add("c", 30)
        cms2.add("d", 40)
        
        merged = cms1.merge(cms2)
        self.assertEqual(merged.estimate("a"), 10)
        self.assertEqual(merged.estimate("b"), 20)
        self.assertEqual(merged.estimate("c"), 30)
        self.assertEqual(merged.estimate("d"), 40)
        self.assertEqual(merged.total_count, 100)
    
    def test_merge_incompatible(self):
        """测试不兼容参数的合并"""
        cms1 = CountMinSketch(width=100, depth=5)
        cms2 = CountMinSketch(width=200, depth=5)
        
        with self.assertRaises(ValueError):
            cms1.merge(cms2)


class TestCountMinSketchSerialization(unittest.TestCase):
    """测试序列化功能"""
    
    def test_to_dict_and_from_dict(self):
        """测试字典序列化"""
        cms1 = CountMinSketch(width=100, depth=5)
        cms1.add("a", 10)
        cms1.add("b", 20)
        
        data = cms1.to_dict()
        self.assertEqual(data['width'], 100)
        self.assertEqual(data['depth'], 5)
        self.assertEqual(data['count'], 30)
        
        cms2 = CountMinSketch.from_dict(data)
        self.assertEqual(cms2.estimate("a"), 10)
        self.assertEqual(cms2.estimate("b"), 20)
        self.assertEqual(cms2.total_count, 30)
    
    def test_to_json_and_from_json(self):
        """测试 JSON 序列化"""
        cms1 = CountMinSketch(width=100, depth=5)
        cms1.add("test", 50)
        
        json_str = cms1.to_json()
        self.assertIsInstance(json_str, str)
        
        cms2 = CountMinSketch.from_json(json_str)
        self.assertEqual(cms2.estimate("test"), 50)
        self.assertEqual(cms2.width, 100)
        self.assertEqual(cms2.depth, 5)


class TestHeavyHitters(unittest.TestCase):
    """测试频繁元素检测"""
    
    def test_check_heavy_hitters(self):
        """测试频繁元素筛选"""
        cms = CountMinSketch(width=1000, depth=5)
        
        # 添加元素
        for _ in range(100):
            cms.add("frequent")
        for _ in range(50):
            cms.add("medium")
        for _ in range(10):
            cms.add("rare")
        
        # 检测频繁元素（> 20% 的频率）
        candidates = ["frequent", "medium", "rare", "nonexistent"]
        heavy = cms.check_heavy_hitters(candidates, 0.2)
        
        # frequent 和 medium 应该被检测到
        items = [item for item, count in heavy]
        self.assertIn("frequent", items)
        self.assertIn("medium", items)
    
    def test_check_heavy_hitters_invalid_threshold(self):
        """测试无效阈值"""
        cms = CountMinSketch()
        with self.assertRaises(ValueError):
            cms.check_heavy_hitters(["a"], 0)
        with self.assertRaises(ValueError):
            cms.check_heavy_hitters(["a"], 1.5)


class TestCountMinSketchBuilder(unittest.TestCase):
    """测试 Builder 模式"""
    
    def test_build_with_default_params(self):
        """测试默认参数构建"""
        builder = CountMinSketchBuilder()
        cms = builder.build()
        
        self.assertIsInstance(cms, CountMinSketch)
        self.assertGreater(cms.width, 0)
        self.assertGreater(cms.depth, 0)
    
    def test_build_with_error_rate(self):
        """测试误差率参数"""
        builder = CountMinSketchBuilder()
        builder.with_error_rate(0.001)
        cms = builder.build()
        
        # 误差率越小，width 应该越大
        self.assertGreater(cms.width, 1000)
    
    def test_build_with_confidence(self):
        """测试置信度参数"""
        builder = CountMinSketchBuilder()
        builder.with_confidence(0.99)
        cms = builder.build()
        
        # 置信度越高，depth 应该越大
        self.assertGreaterEqual(cms.depth, 3)
    
    def test_invalid_error_rate(self):
        """测试无效误差率"""
        builder = CountMinSketchBuilder()
        with self.assertRaises(ValueError):
            builder.with_error_rate(0)
        with self.assertRaises(ValueError):
            builder.with_error_rate(1)
    
    def test_invalid_confidence(self):
        """测试无效置信度"""
        builder = CountMinSketchBuilder()
        with self.assertRaises(ValueError):
            builder.with_confidence(0)
        with self.assertRaises(ValueError):
            builder.with_confidence(1)
    
    def test_with_seed(self):
        """测试种子设置"""
        builder = CountMinSketchBuilder()
        builder.with_seed(12345)
        cms = builder.build()
        
        # 相同种子应该产生相同的哈希
        cms2 = CountMinSketchBuilder().with_seed(12345).build()
        cms.add("test")
        cms2.add("test")
        # 估计值应该相同
        self.assertEqual(cms.estimate("test"), cms2.estimate("test"))


class TestTopKTracker(unittest.TestCase):
    """测试 Top-K 追踪器"""
    
    def test_basic_tracking(self):
        """测试基本追踪功能"""
        tracker = TopKTracker(k=3)
        
        tracker.add("a")
        tracker.add("b")
        tracker.add("a")
        tracker.add("c")
        tracker.add("a")
        
        top_k = tracker.get_top_k()
        self.assertEqual(len(top_k), 3)
        
        # a 应该是第一个（最高频）
        self.assertEqual(top_k[0][0], "a")
        self.assertEqual(top_k[0][1], 3)
    
    def test_k_limit(self):
        """测试 K 值限制"""
        tracker = TopKTracker(k=2)
        
        tracker.add("a")
        tracker.add("b")
        tracker.add("c")  # 应该被忽略或替换
        
        top_k = tracker.get_top_k()
        self.assertLessEqual(len(top_k), 2)
    
    def test_estimate(self):
        """测试估计功能"""
        tracker = TopKTracker(k=5)
        
        tracker.add("test", 10)
        self.assertEqual(tracker.estimate("test"), 10)
    
    def test_total_count(self):
        """测试总计数"""
        tracker = TopKTracker(k=5)
        
        tracker.add("a", 10)
        tracker.add("b", 20)
        
        self.assertEqual(tracker.total_count, 30)
    
    def test_clear(self):
        """测试清空功能"""
        tracker = TopKTracker(k=5)
        
        tracker.add("a", 10)
        tracker.clear()
        
        self.assertEqual(tracker.total_count, 0)
        self.assertEqual(len(tracker.get_top_k()), 0)
    
    def test_invalid_k(self):
        """测试无效 K 值"""
        with self.assertRaises(ValueError):
            TopKTracker(k=0)
        with self.assertRaises(ValueError):
            TopKTracker(k=-1)
    
    def test_repr(self):
        """测试 __repr__ 方法"""
        tracker = TopKTracker(k=3)
        repr_str = repr(tracker)
        self.assertIn("TopKTracker", repr_str)
        self.assertIn("k=3", repr_str)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_create_optimal_sketch(self):
        """测试创建最优 sketch"""
        cms = create_optimal_sketch(
            expected_items=1000000,
            max_error=0.001,
            confidence=0.95
        )
        
        self.assertIsInstance(cms, CountMinSketch)
        self.assertGreater(cms.width, 0)
        self.assertGreater(cms.depth, 0)
    
    def test_count_min_sketch_function(self):
        """测试便捷创建函数"""
        cms = count_min_sketch(width=100, depth=3, seed=42)
        
        self.assertIsInstance(cms, CountMinSketch)
        self.assertEqual(cms.width, 100)
        self.assertEqual(cms.depth, 3)
    
    def test_frequency_analysis(self):
        """测试频率分析函数"""
        items = ["a", "b", "a", "c", "a", "b"]
        result = frequency_analysis(items, width=100, depth=3)
        
        self.assertEqual(result['total_count'], 6)
        self.assertEqual(result['unique_count'], 3)
        self.assertIn('sketch', result)
        self.assertIn('error_bound', result)
    
    def test_frequency_analysis_with_threshold(self):
        """测试带阈值的频率分析"""
        items = ["a"] * 100 + ["b"] * 50 + ["c"] * 10
        result = frequency_analysis(
            items,
            width=1000,
            depth=5,
            threshold=0.2
        )
        
        self.assertIn('heavy_hitters', result)
        # a 和 b 应该是 heavy hitters
        heavy_items = [item for item, count in result['heavy_hitters']]
        self.assertIn("a", heavy_items)
    
    def test_frequency_analysis_with_top_k(self):
        """测试带 Top-K 的频率分析"""
        items = ["a", "b", "a", "c", "a", "b", "d", "a", "b", "e"]
        result = frequency_analysis(
            items,
            width=100,
            depth=3,
            top_k=3
        )
        
        self.assertIn('top_k', result)
        self.assertLessEqual(len(result['top_k']), 3)
        # a 应该是第一个
        self.assertEqual(result['top_k'][0][0], "a")


class TestEdgeCases(unittest.TestCase):
    """测试边界条件"""
    
    def test_empty_sketch(self):
        """测试空 sketch"""
        cms = CountMinSketch()
        self.assertEqual(cms.estimate("anything"), 0)
        self.assertEqual(cms.total_count, 0)
    
    def test_large_count(self):
        """测试大计数"""
        cms = CountMinSketch(width=1000, depth=5)
        cms.add("item", 1000000)
        
        self.assertEqual(cms.estimate("item"), 1000000)
        self.assertEqual(cms.total_count, 1000000)
    
    def test_single_width(self):
        """测试最小 width"""
        cms = CountMinSketch(width=1, depth=5)
        cms.add("a")
        cms.add("b")
        
        # 所有元素映射到同一个位置
        self.assertGreater(cms.estimate("a"), 0)
        self.assertGreater(cms.estimate("b"), 0)
    
    def test_single_depth(self):
        """测试最小 depth"""
        cms = CountMinSketch(width=100, depth=1)
        cms.add("test")
        
        self.assertGreater(cms.estimate("test"), 0)
    
    def test_unicode_strings(self):
        """测试 Unicode 字符串"""
        cms = CountMinSketch()
        
        cms.add("你好")
        cms.add("世界")
        cms.add("你好")
        
        self.assertGreaterEqual(cms.estimate("你好"), 2)
        self.assertGreaterEqual(cms.estimate("世界"), 1)
    
    def test_estimate_error(self):
        """测试误差估计"""
        cms = CountMinSketch(width=1000, depth=5)
        
        # 空 sketch 的误差应该很小
        error = cms.estimate_error()
        self.assertEqual(error, 0)
        
        # 添加元素后误差增加
        cms.add("test", 1000)
        error = cms.estimate_error()
        self.assertGreater(error, 0)


class TestConsistency(unittest.TestCase):
    """测试一致性"""
    
    def test_repeated_adds(self):
        """测试重复添加的一致性"""
        cms = CountMinSketch(width=1000, depth=5)
        
        for _ in range(100):
            cms.add("consistent")
        
        estimate = cms.estimate("consistent")
        self.assertGreaterEqual(estimate, 100)
    
    def test_deterministic(self):
        """测试相同种子产生相同结果"""
        cms1 = CountMinSketch(width=100, depth=5, seed=42)
        cms2 = CountMinSketch(width=100, depth=5, seed=42)
        
        items = ["a", "b", "c", "a", "b", "a"]
        for item in items:
            cms1.add(item)
            cms2.add(item)
        
        for item in items:
            self.assertEqual(cms1.estimate(item), cms2.estimate(item))


if __name__ == "__main__":
    unittest.main(verbosity=2)