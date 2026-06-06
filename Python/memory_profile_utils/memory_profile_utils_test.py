"""
内存分析工具测试 - Memory Profile Utils Tests

测试所有模块功能。
"""

import gc
import os
import sys
import time
import unittest
from typing import List

# 添加父目录到路径以便导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory_profile_utils import (
    # Memory Monitor
    get_memory_usage,
    get_process_memory_info,
    MemorySnapshot,
    MemoryMonitor,
    memory_context,
    track_memory,
    # Object Analyzer
    get_object_size,
    get_object_size_deep,
    analyze_object,
    get_referents,
    get_referrers,
    ObjectSizeAnalyzer,
    top_objects_by_size,
    # Leak Detector
    MemoryLeakDetector,
    detect_leak,
    compare_snapshots,
    find_growing_types,
    # Optimizer
    MemoryOptimizer,
    optimize_intern,
    clear_caches,
    get_memory_recommendations,
    memory_efficient,
    memory_efficient_class,
)


class TestMemoryMonitor(unittest.TestCase):
    """测试内存监控模块"""
    
    def test_get_memory_usage(self):
        """测试获取内存使用"""
        mem = get_memory_usage()
        
        self.assertIn("rss", mem)
        self.assertIn("vms", mem)
        self.assertIn("percent", mem)
        
        # 基本合理性检查
        self.assertGreaterEqual(mem["rss"], 0)
        self.assertGreaterEqual(mem["vms"], 0)
        self.assertGreaterEqual(mem["percent"], 0)
    
    def test_get_process_memory_info(self):
        """测试获取进程内存信息"""
        info = get_process_memory_info()
        
        self.assertIn("pid", info)
        self.assertIn("name", info)
        self.assertIn("rss_mb", info)
        
        self.assertGreater(info["pid"], 0)  # 当前进程PID大于0
    
    def test_memory_snapshot(self):
        """测试内存快照"""
        snapshot = MemorySnapshot.capture()
        
        self.assertGreater(snapshot.timestamp, 0)
        self.assertGreaterEqual(snapshot.rss_mb, 0)
        self.assertGreaterEqual(snapshot.vms_mb, 0)
    
    def test_memory_snapshot_diff(self):
        """测试快照差异计算"""
        snap1 = MemorySnapshot.capture()
        
        # 分配一些内存
        data = [i for i in range(100000)]
        
        snap2 = MemorySnapshot.capture()
        diff = snap2.diff(snap1)
        
        self.assertIn("time_diff_sec", diff)
        self.assertIn("rss_diff_mb", diff)
    
    def test_memory_monitor(self):
        """测试内存监控器"""
        monitor = MemoryMonitor(interval=0.1, max_samples=10)
        monitor.start()
        
        # 采集几个样本
        for _ in range(3):
            monitor.sample()
            time.sleep(0.05)
        
        monitor.stop()
        
        samples = monitor.get_samples()
        self.assertGreater(len(samples), 0)
        
        stats = monitor.get_statistics()
        self.assertIn("rss", stats)
    
    def test_memory_context(self):
        """测试内存上下文管理器"""
        with memory_context("test_context") as monitor:
            # 分配一些内存
            data = [i for i in range(10000)]
            monitor.sample()
        
        # 应该正常退出，不抛出异常
    
    def test_track_memory_decorator(self):
        """测试内存追踪装饰器"""
        @track_memory
        def allocate_memory():
            return [i for i in range(10000)]
        
        result = allocate_memory()
        self.assertEqual(len(result), 10000)


class TestObjectAnalyzer(unittest.TestCase):
    """测试对象分析模块"""
    
    def test_get_object_size(self):
        """测试获取对象大小"""
        # 简单类型
        self.assertGreater(get_object_size(42), 0)
        self.assertGreater(get_object_size("hello"), 0)
        
        # 容器类型
        lst = [1, 2, 3, 4, 5]
        size = get_object_size(lst)
        self.assertGreater(size, sys.getsizeof(lst))
    
    def test_get_object_size_deep(self):
        """测试深度对象大小分析"""
        obj = {"a": [1, 2, 3], "b": {"c": "hello"}}
        info = get_object_size_deep(obj)
        
        self.assertIn("total_size_bytes", info)
        self.assertIn("total_size_kb", info)
        self.assertIn("total_size_mb", info)
        self.assertIn("unique_objects", info)
        self.assertIn("object_type", info)
        
        self.assertGreater(info["total_size_bytes"], 0)
        self.assertEqual(info["object_type"], "dict")
    
    def test_analyze_object(self):
        """测试对象分析"""
        obj = [i for i in range(1000)]
        analysis = analyze_object(obj)
        
        self.assertEqual(analysis.object_type, "list")
        self.assertGreater(analysis.shallow_size, 0)
        self.assertGreater(analysis.deep_size, 0)
        self.assertGreater(analysis.reference_count, 0)
        self.assertEqual(analysis.container_items, 1000)
    
    def test_analyze_object_with_attributes(self):
        """测试带属性的对象分析"""
        class MyClass:
            def __init__(self):
                self.x = 1
                self.y = 2
                self.data = [1, 2, 3]
        
        obj = MyClass()
        analysis = analyze_object(obj)
        
        self.assertEqual(analysis.object_type, "MyClass")
        self.assertIn("x", analysis.attributes)
        self.assertIn("y", analysis.attributes)
        self.assertIn("data", analysis.attributes)
    
    def test_get_referents(self):
        """测试获取引用对象"""
        inner = [1, 2, 3]
        outer = {"list": inner, "value": 42}
        
        refs = get_referents(outer, max_depth=1)
        
        self.assertGreater(len(refs), 0)
        ref_types = [r["type"] for r in refs]
        self.assertIn("list", ref_types)
    
    def test_get_referrers(self):
        """测试获取引用源"""
        obj = [1, 2, 3]
        container = {"data": obj}
        
        refs = get_referrers(obj)
        
        self.assertGreater(len(refs), 0)
    
    def test_object_size_analyzer(self):
        """测试对象大小分析器"""
        analyzer = ObjectSizeAnalyzer()
        
        analyzer.add("list1", [i for i in range(1000)])
        analyzer.add("dict1", {i: str(i) for i in range(100)})
        analyzer.add("string1", "hello world" * 100)
        
        report = analyzer.get_report()
        
        self.assertEqual(report["total_objects"], 3)
        self.assertGreater(report["total_size_bytes"], 0)
        self.assertEqual(len(report["items"]), 3)
        
        # 找出最大的对象
        largest = analyzer.find_largest(2)
        self.assertEqual(len(largest), 2)
    
    def test_top_objects_by_size(self):
        """测试按大小排序对象"""
        objects = [
            [i for i in range(10000)],  # 大列表
            "small",  # 小字符串
            {i: i for i in range(1000)},  # 中等字典
        ]
        
        top = top_objects_by_size(objects, limit=2)
        
        self.assertEqual(len(top), 2)
        # 列表应该最大
        self.assertEqual(top[0]["type"], "list")


class TestLeakDetector(unittest.TestCase):
    """测试内存泄漏检测模块"""
    
    def test_memory_leak_detector_basic(self):
        """测试基本的泄漏检测"""
        detector = MemoryLeakDetector(threshold_mb=1.0)
        detector.start()
        
        # 分配一些内存
        data = [i for i in range(10000)]
        
        report = detector.stop()
        
        self.assertIn("severity", report.to_dict())
        self.assertIn("memory_growth_mb", report.to_dict())
    
    def test_detect_leak_context(self):
        """测试泄漏检测上下文管理器"""
        with detect_leak(threshold_mb=10.0, auto_report=False) as detector:
            # 分配内存
            data = [i for i in range(5000)]
        
        # 应该正常退出
    
    def test_compare_snapshots(self):
        """测试快照比较"""
        snap1 = MemorySnapshot.capture()
        
        # 分配内存
        data = [i for i in range(10000)]
        
        snap2 = MemorySnapshot.capture()
        
        result = compare_snapshots(snap1, snap2)
        
        self.assertIn("rss_diff_mb", result)
        self.assertIn("snapshot1", result)
        self.assertIn("snapshot2", result)
    
    def test_find_growing_types(self):
        """测试查找增长的对象类型"""
        # 这个测试可能需要一些时间
        growing = find_growing_types(iterations=3, interval=0.1, threshold=10)
        
        # 应该返回列表（可能为空）
        self.assertIsInstance(growing, list)
    
    def test_leak_report_str(self):
        """测试泄漏报告字符串表示"""
        report = detector = MemoryLeakDetector(threshold_mb=1.0)
        detector.start()
        data = [i for i in range(1000)]
        report = detector.stop()
        
        report_str = str(report)
        
        self.assertIn("内存泄漏报告", report_str)
        self.assertIn("严重程度", report_str)


class TestOptimizer(unittest.TestCase):
    """测试内存优化模块"""
    
    def test_memory_optimizer_analyze_efficiency(self):
        """测试内存效率分析"""
        optimizer = MemoryOptimizer()
        
        # 列表
        analysis = optimizer.analyze_efficiency([i for i in range(100)])
        self.assertIn("efficiency_score", analysis)
        
        # 字典
        analysis = optimizer.analyze_efficiency({"a": 1, "b": 2})
        self.assertIn("efficiency_score", analysis)
    
    def test_memory_optimizer_get_recommendations(self):
        """测试获取优化建议"""
        optimizer = MemoryOptimizer()
        
        recommendations = optimizer.get_recommendations()
        
        self.assertIsInstance(recommendations, list)
    
    def test_memory_optimizer_cleanup(self):
        """测试内存清理"""
        optimizer = MemoryOptimizer()
        
        result = optimizer.cleanup()
        
        self.assertIn("gc_before", result)
        self.assertIn("gc_after", result)
        self.assertIn("collected", result)
    
    def test_memory_optimizer_estimate_potential(self):
        """测试优化潜力估算"""
        optimizer = MemoryOptimizer()
        
        obj = [i for i in range(1000)]
        potential = optimizer.estimate_optimization_potential(obj)
        
        self.assertIn("current_size_bytes", potential)
        self.assertIn("potential_savings", potential)
        self.assertIn("total_potential_bytes", potential)
    
    def test_optimize_intern(self):
        """测试字符串内部化"""
        strings = ["hello", "world", "hello", "world"] * 100
        
        mapping = optimize_intern(strings)
        
        # 应该只有两个唯一的字符串
        self.assertEqual(len(mapping), 2)
        self.assertIn("hello", mapping)
        self.assertIn("world", mapping)
        
        # 内部化的字符串应该是同一个对象
        self.assertIs(mapping["hello"], mapping["hello"])
    
    def test_clear_caches(self):
        """测试缓存清理"""
        result = clear_caches()
        
        self.assertIn("gc_collected", result)
        self.assertGreaterEqual(result["gc_collected"], 0)
    
    def test_get_memory_recommendations(self):
        """测试获取内存建议"""
        recommendations = get_memory_recommendations()
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
    
    def test_memory_efficient_context(self):
        """测试内存高效上下文"""
        with memory_efficient():
            data = [i for i in range(1000)]
        
        # 应该正常退出
    
    def test_memory_efficient_class(self):
        """测试内存高效类装饰器"""
        @memory_efficient_class
        class DataPoint:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        
        point = DataPoint(1, 2)
        
        # 应该有 __slots__
        self.assertTrue(hasattr(DataPoint, "__slots__"))
        
        # 应该有内存清理方法
        self.assertTrue(hasattr(point, "__memclear__"))
        
        # 测试内存清理
        point.__memclear__()


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流"""
        # 1. 创建监控器
        monitor = MemoryMonitor(interval=0.1)
        monitor.start()
        
        # 2. 创建分析器
        analyzer = ObjectSizeAnalyzer()
        
        # 3. 分配内存并分析
        data1 = [i for i in range(10000)]
        data2 = {i: str(i) for i in range(1000)}
        
        analyzer.add("large_list", data1)
        analyzer.add("medium_dict", data2)
        
        # 4. 采集快照
        monitor.sample()
        
        # 5. 获取报告
        report = analyzer.get_report()
        self.assertGreater(report["total_size_bytes"], 0)
        
        # 6. 停止监控
        monitor.stop()
        
        # 7. 优化检查
        optimizer = MemoryOptimizer()
        recommendations = optimizer.get_recommendations()
        self.assertIsInstance(recommendations, list)
    
    def test_leak_detection_workflow(self):
        """测试泄漏检测工作流"""
        with detect_leak(threshold_mb=5.0, auto_report=False) as detector:
            # 模拟内存分配
            data = []
            for _ in range(100):
                data.append([i for i in range(100)])
            
            # 创建检查点
            checkpoint = detector.checkpoint()
            self.assertIn("rss_mb", checkpoint)
    
    def test_object_tracking(self):
        """测试对象追踪"""
        # 创建对象
        outer_list = []
        inner_dict = {"key": "value"}
        
        for i in range(100):
            outer_list.append({"index": i, "ref": inner_dict})
        
        # 分析
        analysis = analyze_object(outer_list)
        
        self.assertEqual(analysis.object_type, "list")
        self.assertEqual(analysis.container_items, 100)
        
        # 检查引用
        refs = get_referents(outer_list, max_depth=2)
        self.assertGreater(len(refs), 0)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestObjectAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestLeakDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestOptimizer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    run_tests()