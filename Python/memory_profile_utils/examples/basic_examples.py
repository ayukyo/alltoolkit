"""
Memory Profile Utils - 使用示例

演示各种功能的使用方法。
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory_profile_utils import (
    # 内存监控
    get_memory_usage,
    MemorySnapshot,
    MemoryMonitor,
    memory_context,
    track_memory,
    
    # 对象分析
    get_object_size,
    get_object_size_deep,
    analyze_object,
    ObjectSizeAnalyzer,
    top_objects_by_size,
    
    # 泄漏检测
    MemoryLeakDetector,
    detect_leak,
    find_growing_types,
    
    # 优化
    MemoryOptimizer,
    optimize_intern,
    get_memory_recommendations,
    clear_caches,
    memory_efficient,
    memory_efficient_class,
)


def example_basic_memory_usage():
    """示例：基本内存使用查询"""
    print("\n=== 基本内存使用 ===\n")
    
    mem = get_memory_usage()
    print(f"当前内存状态:")
    print(f"  RSS (常驻内存): {mem['rss']:.2f} MB")
    print(f"  VMS (虚拟内存): {mem['vms']:.2f} MB")
    print(f"  使用百分比: {mem['percent']:.1f}%")
    print(f"  可用内存: {mem['available']:.2f} MB")
    print(f"  总内存: {mem['total']:.2f} MB")


def example_memory_snapshot():
    """示例：内存快照"""
    print("\n=== 内存快照 ===\n")
    
    # 捕获初始快照
    snap1 = MemorySnapshot.capture()
    print(f"初始快照: RSS = {snap1.rss_mb:.2f} MB, GC对象 = {snap1.gc_objects}")
    
    # 分配一些内存
    data = [i for i in range(100000)]
    print(f"分配了 {len(data)} 个元素的列表")
    
    # 捕获结束快照
    snap2 = MemorySnapshot.capture()
    print(f"结束快照: RSS = {snap2.rss_mb:.2f} MB, GC对象 = {snap2.gc_objects}")
    
    # 计算差异
    diff = snap2.diff(snap1)
    print(f"内存变化: RSS +{diff['rss_diff_mb']:.2f} MB, GC对象 +{diff['gc_objects_diff']}")


def example_memory_monitor():
    """示例：内存监控器"""
    print("\n=== 内存监控器 ===\n")
    
    # 创建监控器，设置回调
    def on_threshold(info):
        print(f"⚠️ 警告: 内存超过阈值! 当前 {info['current_mb']:.2f} MB")
    
    monitor = MemoryMonitor(
        interval=0.5,
        max_samples=20,
        threshold_mb=100,  # 设置阈值
        callback=on_threshold,
    )
    
    monitor.start()
    print("开始监控...")
    
    # 模拟内存分配
    for i in range(5):
        data = [i] * 50000
        monitor.sample()
        print(f"  第 {i+1} 次采样: RSS = {monitor.get_samples()[-1].rss_mb:.2f} MB")
    
    monitor.stop()
    
    # 获取统计信息
    stats = monitor.get_statistics()
    print(f"\n监控统计:")
    print(f"  采样数: {stats['count']}")
    print(f"  RSS 最小: {stats['rss']['min']:.2f} MB")
    print(f"  RSS 最大: {stats['rss']['max']:.2f} MB")
    print(f"  RSS 平均: {stats['rss']['avg']:.2f} MB")
    print(f"  RSS 变化: {stats['rss']['delta']:.2f} MB")


def example_memory_context():
    """示例：内存上下文管理器"""
    print("\n=== 内存上下文管理器 ===\n")
    
    with memory_context("大数据处理", threshold_mb=10) as monitor:
        # 分配内存
        data1 = [i for i in range(50000)]
        data2 = {i: str(i) for i in range(5000)}
        
        # 中途采样
        monitor.sample()
        print(f"中途采样: RSS = {monitor.get_samples()[-1].rss_mb:.2f} MB")
    
    print("上下文结束，自动生成报告")


def example_track_memory_decorator():
    """示例：内存追踪装饰器"""
    print("\n=== 内存追踪装饰器 ===\n")
    
    @track_memory
    def create_large_data():
        """创建大量数据"""
        data = [i**2 for i in range(100000)]
        return data
    
    result = create_large_data()
    print(f"创建了 {len(result)} 个元素的列表")


def example_object_size():
    """示例：对象大小分析"""
    print("\n=== 对象大小分析 ===\n")
    
    # 简单对象
    num = 42
    str_obj = "Hello, World!"
    lst = [1, 2, 3, 4, 5]
    
    print(f"整数 {num}: {get_object_size(num)} 字节")
    print(f"字符串 '{str_obj}': {get_object_size(str_obj)} 字节")
    print(f"列表 {lst}: {get_object_size(lst)} 字节")
    
    # 嵌套对象
    nested = {
        "numbers": [i for i in range(100)],
        "strings": ["text" * 10 for _ in range(20)],
        "nested_dict": {i: i**2 for i in range(50)},
    }
    
    info = get_object_size_deep(nested)
    print(f"\n嵌套字典分析:")
    print(f"  总大小: {info['total_size_kb']:.2f} KB")
    print(f"  唯一对象数: {info['unique_objects']}")
    print(f"  是否容器: {info['is_container']}")


def example_object_analysis():
    """示例：完整对象分析"""
    print("\n=== 完整对象分析 ===\n")
    
    # 创建复杂对象
    class DataRecord:
        def __init__(self, id, name, values):
            self.id = id
            self.name = name
            self.values = values
    
    record = DataRecord(
        1,
        "测试记录",
        [i for i in range(100)]
    )
    
    analysis = analyze_object(record)
    
    print(f"对象类型: {analysis.object_type}")
    print(f"浅层大小: {analysis.shallow_size_human}")
    print(f"深层大小: {analysis.deep_size_human}")
    print(f"引用计数: {analysis.reference_count}")
    print(f"属性数: {len(analysis.attributes)}")
    
    print("\n属性大小:")
    for attr, size in analysis.attributes.items():
        print(f"  {attr}: {size} 字节")


def example_object_analyzer():
    """示例：批量对象分析"""
    print("\n=== 批量对象分析 ===\n")
    
    analyzer = ObjectSizeAnalyzer()
    
    # 添加多个对象
    analyzer.add("大型列表", [i for i in range(100000)])
    analyzer.add("字典", {i: f"value_{i}" for i in range(5000)})
    analyzer.add("字符串集合", ["text" * 50 for _ in range(100)])
    
    # 获取报告
    report = analyzer.get_report()
    
    print(f"总对象数: {report['total_objects']}")
    print(f"总内存: {report['total_size_human']}")
    
    print("\n各对象详情:")
    for item in report['items']:
        print(f"  {item['name']}: {item['deep_size']/1024:.2f} KB ({item['type']})")
    
    # 找出最大的
    largest = analyzer.find_largest(2)
    print("\n最大的 2 个对象:")
    for obj in largest:
        print(f"  {obj['name']}: {obj['size_human']}")


def example_top_objects():
    """示例：按大小排序对象"""
    print("\n=== 按大小排序对象 ===\n")
    
    objects = [
        [i for i in range(10000)],    # 大列表
        "small string",                # 小字符串
        {i: i**2 for i in range(1000)}, # 中等字典
        (1, 2, 3, 4, 5),               # 小元组
        set(range(5000)),              # 大集合
    ]
    
    top = top_objects_by_size(objects, limit=3)
    
    print("最大的 3 个对象:")
    for obj in top:
        print(f"  #{obj['index']}: {obj['type']} - {obj['size_human']}")


def example_leak_detector():
    """示例：内存泄漏检测"""
    print("\n=== 内存泄漏检测 ===\n")
    
    detector = MemoryLeakDetector(threshold_mb=1.0)
    detector.start()
    
    print("开始检测...")
    
    # 模拟可能泄漏的代码
    data_store = []
    for _ in range(100):
        data_store.append([i for i in range(100)])
    
    # 创建检查点
    checkpoint = detector.checkpoint()
    print(f"检查点: RSS = {checkpoint['rss_mb']:.2f} MB, 对象变化 = {checkpoint['diff_from_start']['gc_objects_diff']}")
    
    # 停止检测并生成报告
    report = detector.stop()
    print(f"\n泄漏报告:")
    print(f"  严重程度: {report.severity}")
    print(f"  内存增长: {report.memory_growth_mb:.2f} MB")
    print(f"  对象增长: {report.object_growth}")
    print(f"  潜在泄漏点: {len(report.potential_leaks)}")
    
    if report.recommendations:
        print("\n建议:")
        for rec in report.recommendations[:3]:
            print(f"  - {rec}")


def example_leak_context():
    """示例：泄漏检测上下文"""
    print("\n=== 泄漏检测上下文 ===\n")
    
    with detect_leak(threshold_mb=5.0, auto_report=True) as detector:
        # 执行代码
        data = [i for i in range(100000)]
        # 退出时自动生成报告


def example_optimizer():
    """示例：内存优化"""
    print("\n=== 内存优化 ===\n")
    
    optimizer = MemoryOptimizer()
    
    # 分析对象效率
    obj = [i for i in range(1000)]
    efficiency = optimizer.analyze_efficiency(obj)
    print(f"列表效率分析:")
    print(f"  效率分数: {efficiency['efficiency_score']}/100")
    if efficiency['issues']:
        print(f"  问题: {efficiency['issues']}")
    
    # 获取优化建议
    recommendations = get_memory_recommendations()
    print(f"\n优化建议 (共 {len(recommendations)} 条):")
    for rec in recommendations[:5]:
        print(f"  - {rec}")
    
    # 清理缓存
    result = clear_caches()
    print(f"\n缓存清理:")
    print(f"  GC 回收: {result['gc_collected']} 个对象")


def example_string_intern():
    """示例：字符串内部化"""
    print("\n=== 字符串内部化 ===\n")
    
    # 创建重复字符串列表
    raw_strings = ["active", "inactive", "pending", "active", "inactive"] * 100
    print(f"原始字符串列表: {len(raw_strings)} 个元素")
    
    # 内部化
    mapping = optimize_intern(raw_strings)
    print(f"内部化后唯一字符串: {len(mapping)} 个")
    
    # 检查是否同一对象
    a1 = mapping["active"]
    a2 = mapping["active"]
    print(f"'active' 是否同一对象: {a1 is a2}")


def example_memory_efficient_class():
    """示例：内存高效类"""
    print("\n=== 内存高效类 ===\n")
    
    @memory_efficient_class
    class Point:
        def __init__(self, x, y, label):
            self.x = x
            self.y = y
            self.label = label
    
    # 创建对象
    p = Point(1, 2, "A")
    
    print(f"类属性:")
    print(f"  __slots__: {Point.__slots__}")
    print(f"  有 __memclear__: {hasattr(p, '__memclear__')}")
    
    # 测试内存清理
    print(f"\n原始状态: x={p.x}, y={p.y}")
    p.__memclear__()
    print(f"清理后: 是否有 x = {hasattr(p, 'x')}")


def example_memory_efficient_context():
    """示例：内存高效上下文"""
    print("\n=== 内存高效上下文 ===\n")
    
    import gc
    
    gc_count_before = len(gc.get_objects())
    
    with memory_efficient():
        # 执行内存密集操作
        data = [i for i in range(100000)]
        result = sum(data)
    
    gc_count_after = len(gc.get_objects())
    
    print(f"GC 对象数变化: {gc_count_after - gc_count_before}")
    print(f"计算结果: {result}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Memory Profile Utils - 使用示例演示")
    print("=" * 60)
    
    # 按类别运行示例
    example_basic_memory_usage()
    example_memory_snapshot()
    example_memory_monitor()
    example_memory_context()
    example_track_memory_decorator()
    
    example_object_size()
    example_object_analysis()
    example_object_analyzer()
    example_top_objects()
    
    example_leak_detector()
    example_leak_context()
    
    example_optimizer()
    example_string_intern()
    example_memory_efficient_class()
    example_memory_efficient_context()
    
    print("\n" + "=" * 60)
    print("所有示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()