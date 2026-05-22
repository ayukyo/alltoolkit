"""
Metrics Utilities 基础使用示例

展示 Counter、Gauge、Histogram、Summary、Meter 的基本用法。
"""

from metrics_utils.mod import (
    Counter, Gauge, Histogram, Summary, Meter,
    MetricsRegistry, export_prometheus, export_json
)
import time


def example_counter():
    """Counter 示例"""
    print("\n=== Counter 示例 ===\n")
    
    # 创建计数器
    counter = Counter('requests_total', 'Total HTTP requests')
    
    # 增加计数
    counter.inc()
    counter.inc(5)
    counter.inc(10)
    
    print(f"计数器名称: {counter.name}")
    print(f"当前值: {counter.value}")
    print(f"描述: {counter.description}")
    
    # 使用标签
    labeled_counter = counter.with_labels(method='GET', endpoint='/api')
    labeled_counter.inc(20)
    print(f"带标签的值: {labeled_counter.value}")
    
    # 快照
    snapshot = counter.snapshot()
    print(f"快照: {snapshot}")


def example_gauge():
    """Gauge 示例"""
    print("\n=== Gauge 示例 ===\n")
    
    # 创建仪表盘
    gauge = Gauge('memory_usage_bytes', 'Current memory usage in bytes')
    
    # 设置值
    gauge.set(1024 * 1024)  # 1MB
    print(f"设置为 1MB: {gauge.value}")
    
    # 增减值
    gauge.inc(512 * 1024)  # 增加 512KB
    print(f"增加 512KB: {gauge.value} bytes")
    
    gauge.dec(256 * 1024)  # 减少 256KB
    print(f"减少 256KB: {gauge.value} bytes")
    
    # 设置为当前时间戳
    gauge.set_to_current_time()
    print(f"当前时间戳: {gauge.value}")
    
    # 跟踪进行中的任务
    print("\n跟踪进行中的任务:")
    print(f"初始值: {gauge.value}")
    
    with gauge.track_inprogress():
        gauge.set(10)
        print(f"进入上下文后: {gauge.value}")
    
    print(f"离开上下文后: {gauge.value}")
    
    # 计时
    print("\n计时示例:")
    timing_gauge = Gauge('execution_time', 'Execution time')
    
    with timing_gauge.time():
        time.sleep(0.1)
    
    print(f"执行时间: {timing_gauge.value:.3f}秒")


def example_histogram():
    """Histogram 示例"""
    print("\n=== Histogram 示例 ===\n")
    
    # 创建直方图（自定义桶）
    hist = Histogram(
        'response_size_bytes',
        'Response size in bytes',
        buckets=[100, 500, 1000, 5000, 10000, float('inf')]
    )
    
    # 记录观测值
    sizes = [150, 320, 800, 1200, 3000, 5000, 8000, 15000]
    for size in sizes:
        hist.observe(size)
    
    print(f"观测次数: {hist.get_count()}")
    print(f"总和: {hist.get_sum()} bytes")
    print(f"平均值: {hist.get_mean():.1f} bytes")
    
    # 分位数
    print("\n分位数:")
    print(f"  P50: {hist.get_quantile(0.5):.1f} bytes")
    print(f"  P90: {hist.get_quantile(0.9):.1f} bytes")
    print(f"  P95: {hist.get_quantile(0.95):.1f} bytes")
    
    # 百分位数
    percentiles = hist.get_percentiles([50, 75, 90, 95, 99])
    print(f"\n百分位数: {percentiles}")
    
    # 桶计数
    buckets = hist.get_bucket_counts()
    print(f"\n桶计数: {buckets}")
    
    # 计时示例
    print("\n计时示例:")
    timing_hist = Histogram('latency_seconds', 'Request latency')
    
    for _ in range(5):
        with timing_hist.time():
            time.sleep(0.05 + 0.03 * (hash(str(time.time())) % 3))
    
    print(f"平均延迟: {timing_hist.get_mean():.3f}秒")
    print(f"P95 延迟: {timing_hist.get_quantile(0.95):.3f}秒")


def example_summary():
    """Summary 示例"""
    print("\n=== Summary 示例 ===\n")
    
    # 创建摘要
    summary = Summary(
        'request_duration_seconds',
        'Request duration in seconds',
        quantiles=[0.5, 0.75, 0.9, 0.95, 0.99],
        max_age=60.0  # 观测值最多保留 60 秒
    )
    
    # 记录观测值
    durations = [0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0]
    for d in durations:
        summary.observe(d)
    
    print(f"观测次数: {summary.get_count()}")
    print(f"平均值: {summary.get_mean():.3f}秒")
    
    # 分位数
    quantiles = summary.get_quantiles()
    print("\n分位数:")
    for q, v in quantiles.items():
        print(f"  {q}: {v:.3f}秒")


def example_meter():
    """Meter 示例"""
    print("\n=== Meter 示例 ===\n")
    
    # 创建计量器
    meter = Meter('requests_per_second', 'Request rate', window_size=5.0)
    
    # 模拟请求
    print("模拟请求...")
    for i in range(20):
        meter.mark()
        time.sleep(0.1)
        if i % 5 == 4:
            print(f"  当前速率: {meter.get_rate():.2f}/s")
    
    print(f"\n总事件数: {meter.get_count()}")
    print(f"时间窗口内事件数: {meter.get_window_count()}")
    print(f"最终速率: {meter.get_rate():.2f}/s")


def example_registry():
    """MetricsRegistry 示例"""
    print("\n=== MetricsRegistry 示例 ===\n")
    
    # 创建注册表（带命名空间）
    registry = MetricsRegistry(namespace='myapp', subsystem='http')
    
    # 注册各种指标
    requests = registry.counter('requests_total', 'Total requests')
    errors = registry.counter('errors_total', 'Total errors')
    latency = registry.histogram('latency_seconds', 'Request latency')
    connections = registry.gauge('active_connections', 'Active connections')
    
    # 使用指标
    requests.inc(100)
    errors.inc(5)
    
    for _ in range(50):
        latency.observe(0.05 + 0.1 * (hash(str(time.time())) % 10))
    
    connections.set(10)
    
    # 获取所有指标
    print("所有指标:")
    for name, metric in registry.get_all_metrics().items():
        print(f"  {name}: {metric}")
    
    # Prometheus 格式导出
    print("\n--- Prometheus 格式 ---")
    print(registry.export_prometheus())
    
    # JSON 格式导出
    print("\n--- JSON 格式 ---")
    import json
    print(json.dumps(registry.export_json(), indent=2, default=str))


def example_convenience_functions():
    """便捷函数示例"""
    print("\n=== 便捷函数示例 ===\n")
    
    # 使用默认注册表的便捷函数
    from metrics_utils.mod import counter, gauge, histogram, meter
    
    c = counter('simple_requests', 'Simple request counter')
    c.inc(10)
    
    g = gauge('simple_memory', 'Simple memory gauge')
    g.set(1024)
    
    h = histogram('simple_latency', 'Simple latency histogram')
    h.observe(0.5)
    
    m = meter('simple_rate', 'Simple rate meter')
    m.mark(5)
    
    print("使用便捷函数创建的指标:")
    print(f"  Counter: {c.value}")
    print(f"  Gauge: {g.value}")
    print(f"  Histogram mean: {h.get_mean()}")
    print(f"  Meter rate: {m.get_rate()}")
    
    print("\n--- 导出默认注册表 ---")
    print(export_prometheus())


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Metrics Utilities 使用示例")
    print("=" * 60)
    
    example_counter()
    example_gauge()
    example_histogram()
    example_summary()
    example_meter()
    example_registry()
    example_convenience_functions()
    
    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()