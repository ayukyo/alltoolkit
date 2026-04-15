# Memory Profile Utils - Python 内存分析工具集

**版本**: 1.0.0  
**作者**: AllToolkit  
**日期**: 2026-04-15  
**零外部依赖**: 仅使用 Python 标准库

## 简介

Memory Profile Utils 是一个功能完整的 Python 内存分析工具集，提供内存监控、对象分析、泄漏检测和优化建议等功能。无需安装任何第三方依赖，开箱即用。

## 功能特性

### 1. 内存监控 (Memory Monitor)
- 实时内存使用监控
- 内存快照捕获和比较
- 内存使用统计报告
- 超阈值告警回调
- 上下文管理器和装饰器

### 2. 对象分析 (Object Analyzer)
- 对象浅层/深层大小计算
- 对象类型和结构分析
- 引用关系追踪（referents/referrers）
- 批量对象大小比较
- 内存效率评估

### 3. 泄漏检测 (Leak Detector)
- 内存泄漏自动检测
- 快照对比分析
- 对象类型增长追踪
- 泄漏严重程度评估
- 优化建议生成

### 4. 内存优化 (Optimizer)
- 内存效率分析
- 优化潜力估算
- 字符串内部化
- `__slots__` 优化
- 缓存清理
- 优化建议

## 安装

无需安装，直接复制 `memory_profile_utils` 目录到项目中即可使用。

## 快速开始

### 基本内存监控

```python
from memory_profile_utils import get_memory_usage, MemorySnapshot

# 获取当前内存使用
mem = get_memory_usage()
print(f"RSS: {mem['rss']:.2f} MB")
print(f"虚拟内存: {mem['vms']:.2f} MB")
print(f"使用率: {mem['percent']:.1f}%")

# 捕获内存快照
snapshot = MemorySnapshot.capture()
print(f"GC 对象数: {snapshot.gc_objects}")
```

### 使用内存监控器

```python
from memory_profile_utils import MemoryMonitor

# 创建监控器
monitor = MemoryMonitor(
    interval=1.0,       # 每秒采样
    max_samples=1000,   # 最大样本数
    threshold_mb=100,   # 内存警告阈值
    callback=lambda info: print(f"警告: 内存超过阈值!")
)

monitor.start()

# 你的代码...
for i in range(10):
    data = [i] * 1000000
    monitor.sample()

monitor.stop()

# 获取报告
report = monitor.get_report()
print(f"内存变化: {report['statistics']['rss']['delta']:.2f} MB")
```

### 上下文管理器

```python
from memory_profile_utils import memory_context

with memory_context("处理大数据", threshold_mb=50) as monitor:
    data = [i for i in range(1000000)]
    # 退出时自动报告内存使用情况
```

### 装饰器

```python
from memory_profile_utils import track_memory

@track_memory
def process_large_data():
    return [i for i in range(1000000)]
```

### 对象大小分析

```python
from memory_profile_utils import get_object_size, get_object_size_deep, analyze_object

# 浅层大小
size = get_object_size([1, 2, 3, 4, 5])
print(f"浅层大小: {size} 字节")

# 深层大小分析
data = {"list": [i for i in range(1000)], "dict": {i: str(i) for i in range(100)}}
info = get_object_size_deep(data)
print(f"总大小: {info['total_size_kb']:.2f} KB")
print(f"唯一对象数: {info['unique_objects']}")

# 完整分析
analysis = analyze_object(data)
print(f"类型: {analysis.object_type}")
print(f"引用计数: {analysis.reference_count}")
print(f"容器元素数: {analysis.container_items}")
```

### 批量对象分析

```python
from memory_profile_utils import ObjectSizeAnalyzer

analyzer = ObjectSizeAnalyzer()

analyzer.add("大数据列表", [i for i in range(100000)])
analyzer.add("配置字典", {"key" + str(i): i for i in range(1000)})
analyzer.add("字符串", "hello world" * 1000)

report = analyzer.get_report()
print(f"总内存: {report['total_size_human']}")

# 找出最大的对象
largest = analyzer.find_largest(3)
for item in largest:
    print(f"{item['name']}: {item['size_human']}")
```

### 内存泄漏检测

```python
from memory_profile_utils import MemoryLeakDetector

detector = MemoryLeakDetector(threshold_mb=1.0)
detector.start()

# 执行可能泄漏内存的代码
for _ in range(1000):
    create_objects()

report = detector.stop()
print(report)  # 打印泄漏报告

# 或使用上下文管理器
from memory_profile_utils import detect_leak

with detect_leak(threshold_mb=5.0) as detector:
    # 执行代码
    data = [i for i in range(1000000)]
```

### 查找内存增长类型

```python
from memory_profile_utils import find_growing_types

# 查找增长的对象类型
growing = find_growing_types(iterations=10, interval=1.0, threshold=100)

for item in growing:
    print(f"{item['type']}: 初始 {item['initial']}, 最终 {item['final']}, 增长 {item['growth']}")
```

### 内存优化

```python
from memory_profile_utils import MemoryOptimizer, optimize_intern

optimizer = MemoryOptimizer()

# 分析对象效率
obj = [i for i in range(10000)]
efficiency = optimizer.analyze_efficiency(obj)
print(f"效率分数: {efficiency['efficiency_score']}/100")

# 估算优化潜力
potential = optimizer.estimate_optimization_potential(obj)
print(f"可节省: {potential['total_potential_human']}")

# 获取优化建议
recommendations = optimizer.get_recommendations()
for rec in recommendations:
    print(f"- {rec}")

# 清理内存
result = optimizer.cleanup()
print(f"回收了 {result['collected']} 个对象")

# 字符串内部化优化
strings = ["status_active", "status_inactive", "status_active"] * 1000
mapping = optimize_intern(strings)  # 重复字符串只存储一次
```

### 内存高效类装饰器

```python
from memory_profile_utils import memory_efficient_class

@memory_efficient_class
class DataPoint:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label

# 自动添加 __slots__ 和内存清理方法
point = DataPoint(1, 2, "A")
point.__memclear__()  # 清理对象内存
```

### 内存高效上下文

```python
from memory_profile_utils import memory_efficient

with memory_efficient():
    # 在此块中执行内存密集操作
    data = process_large_file()
    # 退出时自动垃圾回收
```

## API 参考

### 内存监控模块

| 函数/类 | 描述 |
|---------|------|
| `get_memory_usage()` | 获取当前进程内存使用情况 |
| `get_process_memory_info(pid)` | 获取指定进程内存信息 |
| `MemorySnapshot` | 内存快照类 |
| `MemoryMonitor` | 内存监控器类 |
| `memory_context()` | 内存监控上下文管理器 |
| `track_memory` | 内存追踪装饰器 |

### 对象分析模块

| 函数/类 | 描述 |
|---------|------|
| `get_object_size(obj)` | 获取对象浅层大小 |
| `get_object_size_deep(obj)` | 深度分析对象大小 |
| `analyze_object(obj)` | 全面分析对象 |
| `get_referents(obj)` | 获取对象引用的对象 |
| `get_referrers(obj)` | 获取引用该对象的对象 |
| `ObjectSizeAnalyzer` | 批量对象分析器 |
| `top_objects_by_size(objs)` | 找出最大对象 |

### 泄漏检测模块

| 函数/类 | 描述 |
|---------|------|
| `MemoryLeakDetector` | 内存泄漏检测器 |
| `LeakReport` | 泄漏报告类 |
| `detect_leak()` | 泄漏检测上下文管理器 |
| `compare_snapshots(s1, s2)` | 比较两个快照 |
| `find_growing_types()` | 查找增长的对象类型 |

### 优化模块

| 函数/类 | 描述 |
|---------|------|
| `MemoryOptimizer` | 内存优化器类 |
| `optimize_intern(strings)` | 字符串内部化优化 |
| `optimize_slots(cls)` | 类 slots 优化装饰器 |
| `get_memory_recommendations()` | 获取优化建议 |
| `clear_caches()` | 清理缓存 |
| `memory_efficient()` | 内存高效上下文 |
| `memory_efficient_class` | 类内存优化装饰器 |

## 运行测试

```bash
cd memory_profile_utils
python test_memory_profile.py
```

## 注意事项

1. **兼容性**: 支持 Python 3.7+
2. **零依赖**: 仅使用 Python 标准库
3. **psutil 可选**: 如需更详细的进程信息，可安装 psutil（非必须）
4. **tracemalloc**: 某些功能使用 tracemalloc，可能影响性能

## 许可证

MIT License

## 更新日志

### v1.0.0 (2026-04-15)
- 初始版本
- 内存监控功能
- 对象分析功能
- 泄漏检测功能
- 内存优化功能