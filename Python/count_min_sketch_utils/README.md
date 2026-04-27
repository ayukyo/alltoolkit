# Count Min Sketch Utils


Count-Min Sketch 工具模块

Count-Min Sketch 是一种概率数据结构，用于估计数据流中元素的频率。
它使用固定的内存空间，提供 O(1) 的更新和查询操作。

特点:
- 空间效率高：使用固定的内存空间
- 时间效率高：O(1) 的更新和查询
- 可合并：多个 sketch 可以合并
- 支持多种哈希函数

应用场景:
- 网络流量分析（Top-K 元素）
- 热点检测
- 频繁项集挖掘
- 流式数据处理
- 大数据近似统计

作者: AllToolkit
日期: 2026-04-19


## 功能

### 类

- **CountMinSketch**: Count-Min Sketch 数据结构实现

用于估计元素在数据流中出现频率的概率数据结构。
提供上界估计，误差取决于宽度参数。

示例:
    >>> cms = CountMinSketch(width=1000, depth=5)
    >>> cms
  方法: width, depth, total_count, memory_usage, add ... (15 个方法)
- **CountMinSketchBuilder**: Count-Min Sketch 构建器

根据期望的误差和置信度自动计算最优参数。

示例:
    >>> builder = CountMinSketchBuilder()
    >>> builder
  方法: with_error_rate, with_confidence, with_seed, build
- **TopKTracker**: Top-K 频繁元素追踪器

结合 Count-Min Sketch 和最小堆来追踪数据流中的 Top-K 元素。

示例:
    >>> tracker = TopKTracker(k=5)
    >>> for word in ["a", "b", "a", "c", "a", "b", "d"]:
    
  方法: k, total_count, add, estimate, get_top_k ... (6 个方法)

### 函数

- **create_optimal_sketch(expected_items, max_error, confidence**) - 创建最优参数的 Count-Min Sketch
- **frequency_analysis(items, width, depth**, ...) - 对数据列表进行频率分析
- **count_min_sketch(width, depth, seed**) - 创建 Count-Min Sketch 的便捷函数
- **width(self**) - 返回每行的宽度
- **depth(self**) - 返回行数
- **total_count(self**) - 返回已添加的元素总数
- **memory_usage(self**) - 返回内存使用量（字节数）
- **add(self, item, count**) - 添加元素到 sketch
- **estimate(self, item**) - 估计元素的频率
- **estimate_error(self, confidence**) - 计算误差范围

... 共 28 个函数

## 使用示例

```python
from mod import create_optimal_sketch

# 使用 create_optimal_sketch
result = create_optimal_sketch()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
