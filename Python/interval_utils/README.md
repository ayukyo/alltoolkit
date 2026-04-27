# Interval Utils


区间操作工具模块 (Interval Utilities)

提供高效的区间数据结构操作，包括：
- 区间合并、交集、差集
- 区间插入、删除
- 区间查找（点查询、范围查询）
- 区间覆盖检测

零外部依赖，纯 Python 实现。

作者: AllToolkit
日期: 2026-04-18


## 功能

### 类

- **Interval**: 区间类，表示一个闭区间 [start, end]

属性:
    start: 区间起始值（包含）
    end: 区间结束值（包含）
  方法: length, overlaps, adjacent, merge, intersection ... (8 个方法)
- **IntervalSet**: 区间集合类

维护一组不相交的有序区间，支持高效的各种区间操作。
使用基于排序数组的实现，适合中等规模的区间集合。
  方法: total_length, is_empty, min_value, max_value, add ... (22 个方法)
- **IntervalMap**: 区间映射类

将值映射到区间，支持区间作为键存储任意值。
  方法: set, get, get_range, remove, items ... (6 个方法)
- **RangeSet**: 范围集合类

专为快速成员检测优化的整数集合实现。
使用区间存储连续值，空间效率高。
  方法: add, add_range, update, remove, discard ... (19 个方法)

### 函数

- **merge_intervals(intervals**) - 合并重叠或相邻的区间
- **interval_intersection(intervals1, intervals2**) - 计算两组区间的交集
- **interval_difference(intervals1, intervals2**) - 计算两组区间的差集
- **interval_union(intervals1, intervals2**) - 计算两组区间的并集
- **find_gaps(intervals**) - 找出区间之间的空隙
- **is_covered(intervals, value**) - 检查值是否被区间覆盖
- **find_containing_interval(intervals, value**) - 找到包含指定值的区间
- **get_total_coverage(intervals**) - 计算区间覆盖的总长度
- **length(self**) - 区间长度（元素个数）
- **overlaps(self, other**) - 检查两个区间是否重叠

... 共 63 个函数

## 使用示例

```python
from mod import merge_intervals

# 使用 merge_intervals
result = merge_intervals()
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
