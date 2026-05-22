"""
Metrics Utilities 测试套件

测试 Counter、Gauge、Histogram、Summary、Meter 和 MetricsRegistry。
"""

import sys
import os
import time
import threading
import unittest

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Counter, Gauge, Histogram, Summary, Meter,
    MetricsRegistry, MetricPoint, MetricSnapshot,
    GaugeContext, GaugeTimer, HistogramTimer, SummaryTimer,
    counter, gauge, histogram, summary, meter,
    export_prometheus, export_json, get_default_registry, set_default_registry
)


class TestCounter(unittest.TestCase):
    """Counter 测试"""
    
    def test_create_counter(self):
        """测试创建计数器"""
        c = Counter('test_counter', 'A test counter')
        self.assertEqual(c.name, 'test_counter')
        self.assertEqual(c.description, 'A test counter')
        self.assertEqual(c.value, 0.0)
    
    def test_increment(self):
        """测试增量"""
        c = Counter('test')
        c.inc()
        self.assertEqual(c.value, 1.0)
        
        c.inc(5)
        self.assertEqual(c.value, 6.0)
        
        c.inc(0.5)
        self.assertEqual(c.value, 6.5)
    
    def test_negative_increment_raises(self):
        """测试负增量抛出异常"""
        c = Counter('test')
        with self.assertRaises(ValueError):
            c.inc(-1)
    
    def test_labels(self):
        """测试标签"""
        c = Counter('test', labels={'method': 'GET'})
        c.inc()
        self.assertEqual(c.value, 1.0)
        
        c2 = c.with_labels(path='/api')
        self.assertEqual(c2.labels, {'method': 'GET', 'path': '/api'})
    
    def test_reset(self):
        """测试重置"""
        c = Counter('test')
        c.inc(10)
        c.reset()
        self.assertEqual(c.value, 0.0)
    
    def test_snapshot(self):
        """测试快照"""
        c = Counter('test', 'description', {'label': 'value'})
        c.inc(42)
        snapshot = c.snapshot()
        
        self.assertEqual(snapshot.name, 'test')
        self.assertEqual(snapshot.metric_type, 'counter')
        self.assertEqual(snapshot.value, 42)
        self.assertEqual(snapshot.labels, {'label': 'value'})
    
    def test_thread_safety(self):
        """测试线程安全"""
        c = Counter('test')
        threads = []
        
        def increment():
            for _ in range(100):
                c.inc()
        
        for _ in range(10):
            t = threading.Thread(target=increment)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        self.assertEqual(c.value, 1000)


class TestGauge(unittest.TestCase):
    """Gauge 测试"""
    
    def test_create_gauge(self):
        """测试创建仪表盘"""
        g = Gauge('test_gauge', 'A test gauge')
        self.assertEqual(g.name, 'test_gauge')
        self.assertEqual(g.description, 'A test gauge')
        self.assertEqual(g.value, 0.0)
    
    def test_set(self):
        """测试设置值"""
        g = Gauge('test')
        g.set(42)
        self.assertEqual(g.value, 42)
        
        g.set(100)
        self.assertEqual(g.value, 100)
        
        g.set(-10)
        self.assertEqual(g.value, -10)
    
    def test_increment_decrement(self):
        """测试增减"""
        g = Gauge('test')
        g.set(10)
        g.inc(5)
        self.assertEqual(g.value, 15)
        
        g.dec(3)
        self.assertEqual(g.value, 12)
    
    def test_set_to_current_time(self):
        """测试设置当前时间戳"""
        g = Gauge('test')
        g.set_to_current_time()
        now = time.time()
        self.assertLess(abs(g.value - now), 1.0)
    
    def test_context_manager(self):
        """测试上下文管理器"""
        g = Gauge('test')
        
        self.assertEqual(g.value, 0)
        
        with g.track_inprogress():
            self.assertEqual(g.value, 1)
        
        self.assertEqual(g.value, 0)
    
    def test_time_context(self):
        """测试计时上下文"""
        g = Gauge('test')
        
        with g.time():
            time.sleep(0.1)
        
        self.assertGreater(g.value, 0.09)
        self.assertLess(g.value, 0.2)
    
    def test_history(self):
        """测试历史记录"""
        g = Gauge('test')
        g.set(1)
        g.set(2)
        g.set(3)
        
        history = g.get_history()
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0].value, 1)
        self.assertEqual(history[1].value, 2)
        self.assertEqual(history[2].value, 3)
    
    def test_history_with_since(self):
        """测试带时间过滤的历史记录"""
        g = Gauge('test')
        
        g.set(1)
        time.sleep(0.01)
        cutoff = time.time()
        time.sleep(0.01)
        g.set(2)
        g.set(3)
        
        history = g.get_history(since=cutoff)
        self.assertEqual(len(history), 2)
    
    def test_snapshot(self):
        """测试快照"""
        g = Gauge('test', 'description', {'label': 'value'})
        g.set(42)
        snapshot = g.snapshot()
        
        self.assertEqual(snapshot.name, 'test')
        self.assertEqual(snapshot.metric_type, 'gauge')
        self.assertEqual(snapshot.value, 42)
        self.assertEqual(snapshot.labels, {'label': 'value'})


class TestHistogram(unittest.TestCase):
    """Histogram 测试"""
    
    def test_create_histogram(self):
        """测试创建直方图"""
        h = Histogram('test_histogram', 'A test histogram')
        self.assertEqual(h.name, 'test_histogram')
        self.assertEqual(h.description, 'A test histogram')
    
    def test_default_buckets(self):
        """测试默认桶"""
        h = Histogram('test')
        buckets = h._buckets
        self.assertIn(0.1, buckets)
        self.assertIn(1.0, buckets)
        self.assertIn(float('inf'), buckets)
    
    def test_custom_buckets(self):
        """测试自定义桶"""
        h = Histogram('test', buckets=[0.1, 0.5, 1.0])
        self.assertEqual(h._buckets[:3], [0.1, 0.5, 1.0])
        self.assertEqual(h._buckets[-1], float('inf'))
    
    def test_observe(self):
        """测试观测"""
        h = Histogram('test')
        
        h.observe(0.05)
        h.observe(0.15)
        h.observe(0.3)
        
        self.assertEqual(h.get_count(), 3)
        self.assertAlmostEqual(h.get_sum(), 0.5, places=2)
    
    def test_mean(self):
        """测试平均值"""
        h = Histogram('test')
        
        h.observe(1)
        h.observe(2)
        h.observe(3)
        
        self.assertEqual(h.get_mean(), 2.0)
    
    def test_quantile(self):
        """测试分位数"""
        h = Histogram('test')
        
        for i in range(1, 101):
            h.observe(i)
        
        # 使用 nearest rank 方法：
        # P50: ceil(100 * 0.5) - 1 = 49, sorted_obs[49] = 50
        # P90: ceil(100 * 0.9) - 1 = 89, sorted_obs[89] = 90
        self.assertEqual(h.get_quantile(0.5), 50)
        self.assertEqual(h.get_quantile(0.9), 90)
        self.assertEqual(h.get_quantile(0.95), 95)
    
    def test_percentiles(self):
        """测试百分位数"""
        h = Histogram('test')
        
        for i in range(1, 101):
            h.observe(i)
        
        percentiles = h.get_percentiles([50, 90, 95, 99])
        # 使用 nearest rank 方法
        self.assertEqual(percentiles['p50'], 50)
        self.assertEqual(percentiles['p90'], 90)
        self.assertEqual(percentiles['p95'], 95)
        self.assertEqual(percentiles['p99'], 99)
    
    def test_bucket_counts(self):
        """测试桶计数"""
        h = Histogram('test', buckets=[0.1, 0.5, 1.0])
        
        h.observe(0.05)  # <= 0.1
        h.observe(0.15)  # <= 0.5
        h.observe(0.6)   # <= 1.0
        h.observe(1.5)   # <= inf
        
        counts = h.get_bucket_counts()
        # 桶计数是累积的：每个桶包含所有 <= 边界的观测值
        self.assertEqual(counts['le_0.1'], 1)  # 1 个 <= 0.1
        self.assertEqual(counts['le_0.5'], 2)  # 2 个 <= 0.5 (0.05, 0.15)
        self.assertEqual(counts['le_1.0'], 3)  # 3 个 <= 1.0 (0.05, 0.15, 0.6)
        self.assertEqual(counts['le_inf'], 4)  # 4 个 <= inf
    
    def test_time_context(self):
        """测试计时上下文"""
        h = Histogram('test')
        
        with h.time():
            time.sleep(0.1)
        
        self.assertEqual(h.get_count(), 1)
        self.assertGreater(h.get_sum(), 0.09)
    
    def test_reset(self):
        """测试重置"""
        h = Histogram('test')
        
        h.observe(1)
        h.observe(2)
        h.reset()
        
        self.assertEqual(h.get_count(), 0)
        self.assertEqual(h.get_sum(), 0.0)
    
    def test_snapshot(self):
        """测试快照"""
        h = Histogram('test')
        h.observe(1)
        h.observe(2)
        
        snapshot = h.snapshot()
        self.assertEqual(snapshot.name, 'test')
        self.assertEqual(snapshot.metric_type, 'histogram')
        self.assertEqual(snapshot.count, 2)
        self.assertEqual(snapshot.sum_value, 3.0)


class TestSummary(unittest.TestCase):
    """Summary 测试"""
    
    def test_create_summary(self):
        """测试创建摘要"""
        s = Summary('test_summary', 'A test summary')
        self.assertEqual(s.name, 'test_summary')
        self.assertEqual(s.description, 'A test summary')
    
    def test_default_quantiles(self):
        """测试默认分位数"""
        s = Summary('test')
        self.assertEqual(s._quantiles, [0.5, 0.9, 0.95, 0.99])
    
    def test_custom_quantiles(self):
        """测试自定义分位数"""
        s = Summary('test', quantiles=[0.25, 0.5, 0.75])
        self.assertEqual(s._quantiles, [0.25, 0.5, 0.75])
    
    def test_observe(self):
        """测试观测"""
        s = Summary('test')
        
        s.observe(1)
        s.observe(2)
        s.observe(3)
        
        self.assertEqual(s.get_count(), 3)
        self.assertEqual(s.get_sum(), 6)
        self.assertEqual(s.get_mean(), 2.0)
    
    def test_quantile(self):
        """测试分位数"""
        s = Summary('test')
        
        for i in range(1, 101):
            s.observe(i)
        
        self.assertEqual(s.get_quantile(0.5), 50)
        self.assertEqual(s.get_quantile(0.9), 90)
    
    def test_get_quantiles(self):
        """测试获取所有分位数"""
        s = Summary('test')
        
        for i in range(1, 101):
            s.observe(i)
        
        quantiles = s.get_quantiles()
        self.assertEqual(quantiles[0.5], 50)
        self.assertEqual(quantiles[0.9], 90)
        self.assertEqual(quantiles[0.95], 95)
        self.assertEqual(quantiles[0.99], 99)
    
    def test_time_context(self):
        """测试计时上下文"""
        s = Summary('test')
        
        with s.time():
            time.sleep(0.1)
        
        self.assertEqual(s.get_count(), 1)
        self.assertGreater(s.get_sum(), 0.09)
    
    def test_max_age(self):
        """测试过期观测值"""
        s = Summary('test', max_age=0.1)
        
        s.observe(1)
        time.sleep(0.15)
        s.observe(2)
        
        # 旧观测值应该被清理
        self.assertEqual(s.get_count(), 2)  # 总计数不变
    
    def test_snapshot(self):
        """测试快照"""
        s = Summary('test')
        s.observe(1)
        s.observe(2)
        
        snapshot = s.snapshot()
        self.assertEqual(snapshot.name, 'test')
        self.assertEqual(snapshot.metric_type, 'summary')
        self.assertEqual(snapshot.count, 2)
        self.assertEqual(snapshot.sum_value, 3.0)


class TestMeter(unittest.TestCase):
    """Meter 测试"""
    
    def test_create_meter(self):
        """测试创建计量器"""
        m = Meter('test_meter', 'A test meter')
        self.assertEqual(m.name, 'test_meter')
        self.assertEqual(m.description, 'A test meter')
    
    def test_mark(self):
        """测试标记事件"""
        m = Meter('test')
        
        m.mark()
        self.assertEqual(m.get_count(), 1)
        
        m.mark(5)
        self.assertEqual(m.get_count(), 6)
    
    def test_rate(self):
        """测试速率计算"""
        m = Meter('test', window_size=1.0)
        
        for _ in range(10):
            m.mark()
            time.sleep(0.05)
        
        rate = m.get_rate()
        self.assertGreater(rate, 0)
        self.assertLess(rate, 50)  # 应该小于 50/s
    
    def test_window_count(self):
        """测试时间窗口内的事件数"""
        m = Meter('test', window_size=0.2)
        
        m.mark(10)
        self.assertEqual(m.get_window_count(), 10)
        
        time.sleep(0.3)
        self.assertEqual(m.get_window_count(), 0)
    
    def test_reset(self):
        """测试重置"""
        m = Meter('test')
        
        m.mark(100)
        m.reset()
        
        self.assertEqual(m.get_count(), 0)
        self.assertEqual(m.get_window_count(), 0)
    
    def test_snapshot(self):
        """测试快照"""
        m = Meter('test', labels={'label': 'value'})
        m.mark(42)
        
        snapshot = m.snapshot()
        self.assertEqual(snapshot.name, 'test')
        self.assertEqual(snapshot.metric_type, 'meter')
        self.assertEqual(snapshot.count, 42)
        self.assertEqual(snapshot.labels, {'label': 'value'})


class TestMetricsRegistry(unittest.TestCase):
    """MetricsRegistry 测试"""
    
    def test_create_registry(self):
        """测试创建注册表"""
        registry = MetricsRegistry()
        self.assertEqual(len(registry.get_all_metrics()), 0)
    
    def test_namespace_subsystem(self):
        """测试命名空间和子系统前缀"""
        registry = MetricsRegistry(namespace='app', subsystem='http')
        
        c = registry.counter('requests_total')
        self.assertEqual(c.name, 'app_http_requests_total')
    
    def test_register_counter(self):
        """测试注册计数器"""
        registry = MetricsRegistry()
        c = registry.counter('requests', 'Total requests')
        
        self.assertEqual(c.name, 'requests')
        c.inc(10)
        self.assertEqual(c.value, 10)
    
    def test_register_gauge(self):
        """测试注册仪表盘"""
        registry = MetricsRegistry()
        g = registry.gauge('memory', 'Memory usage')
        
        g.set(1024)
        self.assertEqual(g.value, 1024)
    
    def test_register_histogram(self):
        """测试注册直方图"""
        registry = MetricsRegistry()
        h = registry.histogram('latency', 'Request latency')
        
        h.observe(0.1)
        self.assertEqual(h.get_count(), 1)
    
    def test_register_summary(self):
        """测试注册摘要"""
        registry = MetricsRegistry()
        s = registry.summary('duration', 'Request duration')
        
        s.observe(1.5)
        self.assertEqual(s.get_count(), 1)
    
    def test_register_meter(self):
        """测试注册计量器"""
        registry = MetricsRegistry()
        m = registry.meter('qps', 'Queries per second')
        
        m.mark(100)
        self.assertEqual(m.get_count(), 100)
    
    def test_get_metric(self):
        """测试获取指标"""
        registry = MetricsRegistry()
        registry.counter('test_counter')
        
        metric = registry.get_metric('test_counter')
        self.assertIsNotNone(metric)
        self.assertEqual(metric.name, 'test_counter')
    
    def test_get_all_metrics(self):
        """测试获取所有指标"""
        registry = MetricsRegistry()
        registry.counter('counter1')
        registry.gauge('gauge1')
        registry.histogram('hist1')
        
        metrics = registry.get_all_metrics()
        self.assertEqual(len(metrics), 3)
        self.assertIn('counter1', metrics)
        self.assertIn('gauge1', metrics)
        self.assertIn('hist1', metrics)
    
    def test_export_prometheus(self):
        """测试 Prometheus 格式导出"""
        registry = MetricsRegistry()
        
        c = registry.counter('requests_total', 'Total requests')
        c.inc(100)
        
        g = registry.gauge('memory_bytes', 'Memory usage')
        g.set(1024)
        
        output = registry.export_prometheus()
        
        self.assertIn('# HELP requests_total Total requests', output)
        self.assertIn('# TYPE requests_total counter', output)
        self.assertIn('requests_total 100', output)
        self.assertIn('# TYPE memory_bytes gauge', output)
        self.assertIn('memory_bytes 1024', output)
    
    def test_export_json(self):
        """测试 JSON 格式导出"""
        registry = MetricsRegistry()
        
        c = registry.counter('requests', 'Total requests')
        c.inc(10)
        
        data = registry.export_json()
        
        self.assertIn('timestamp', data)
        self.assertIn('metrics', data)
        self.assertIn('requests', data['metrics'])
        self.assertEqual(data['metrics']['requests']['type'], 'counter')
        self.assertEqual(data['metrics']['requests']['value'], 10)
    
    def test_reset_all(self):
        """测试重置所有指标"""
        registry = MetricsRegistry()
        
        c = registry.counter('counter')
        g = registry.gauge('gauge')
        
        c.inc(100)
        g.set(200)
        
        registry.reset_all()
        
        self.assertEqual(c.value, 0)
        self.assertEqual(g.value, 0)
    
    def test_duplicate_registration(self):
        """测试重复注册返回同一实例"""
        registry = MetricsRegistry()
        
        c1 = registry.counter('test')
        c1.inc(10)
        
        c2 = registry.counter('test')
        # 应该返回同一实例
        self.assertEqual(c2.value, 10)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_counter_function(self):
        """测试 counter 便捷函数"""
        c = counter('test_counter', 'Test')
        c.inc(5)
        self.assertEqual(c.value, 5)
    
    def test_gauge_function(self):
        """测试 gauge 便捷函数"""
        g = gauge('test_gauge', 'Test')
        g.set(42)
        self.assertEqual(g.value, 42)
    
    def test_histogram_function(self):
        """测试 histogram 便捷函数"""
        h = histogram('test_hist', 'Test')
        h.observe(1.5)
        self.assertEqual(h.get_count(), 1)
    
    def test_summary_function(self):
        """测试 summary 便捷函数"""
        s = summary('test_summary', 'Test')
        s.observe(2.5)
        self.assertEqual(s.get_count(), 1)
    
    def test_meter_function(self):
        """测试 meter 便捷函数"""
        m = meter('test_meter', 'Test')
        m.mark(10)
        self.assertEqual(m.get_count(), 10)
    
    def test_export_functions(self):
        """测试导出函数"""
        counter('test_c').inc()
        gauge('test_g').set(1)
        
        prom = export_prometheus()
        self.assertIn('test_c', prom)
        self.assertIn('test_g', prom)
        
        json_data = export_json()
        self.assertIn('test_c', json_data['metrics'])
        self.assertIn('test_g', json_data['metrics'])


class TestMetricPoint(unittest.TestCase):
    """MetricPoint 测试"""
    
    def test_create_metric_point(self):
        """测试创建数据点"""
        point = MetricPoint(
            value=42.0,
            timestamp=time.time(),
            labels={'key': 'value'}
        )
        
        self.assertEqual(point.value, 42.0)
        self.assertIn('key', point.labels)


class TestMetricSnapshot(unittest.TestCase):
    """MetricSnapshot 测试"""
    
    def test_create_metric_snapshot(self):
        """测试创建快照"""
        snapshot = MetricSnapshot(
            name='test',
            metric_type='counter',
            value=100,
            labels={'method': 'GET'},
            count=10,
            sum_value=50.0,
            buckets={'le_1': 5, 'le_inf': 10},
            quantiles={0.5: 5, 0.9: 9}
        )
        
        self.assertEqual(snapshot.name, 'test')
        self.assertEqual(snapshot.metric_type, 'counter')
        self.assertEqual(snapshot.value, 100)
        self.assertEqual(snapshot.count, 10)


if __name__ == '__main__':
    unittest.main(verbosity=2)