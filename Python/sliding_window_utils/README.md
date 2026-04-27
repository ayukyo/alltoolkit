# Sliding Window Utils


滑动窗口统计工具模块 (Sliding Window Statistics Utils)

提供高效的滑动窗口数据结构和统计计算功能，适用于实时数据流分析、
监控指标计算、性能测量等场景。零外部依赖，纯 Python 标准库实现。

主要功能：
- 滑动窗口最大值/最小值（单调队列实现，O(1) 查询）
- 滑动窗口平均值/总和/计数
- 滑动窗口标准差/方差
- 滑动窗口中位数（双堆实现）
- 滑动窗口百分位数
- 时间窗口统计（基于时间戳的数据）


## 功能

### 类

- **SlidingWindowMax**: 滑动窗口最大值计算器

使用单调递减队列实现，支持 O(1) 的最大值查询，
O(n) 的整体时间复杂度处理 n 个元素。

示例:
    >>> swm = SlidingWindowMax(3)
    >>> for val in [1, 3, 2, 5, 4]:
    
  方法: push, max, is_empty, is_full, clear
- **SlidingWindowMin**: 滑动窗口最小值计算器

使用单调递增队列实现，支持 O(1) 的最小值查询。

示例:
    >>> swm = SlidingWindowMin(3)
    >>> for val in [5, 3, 2, 4, 1]:
    
  方法: push, min, is_empty, is_full, clear
- **SlidingWindowStats**: 滑动窗口统计计算器

提供滑动窗口内的平均值、总和、标准差、方差等统计量计算。

示例:
    >>> stats = SlidingWindowStats(3)
    >>> for val in [1, 2, 3, 4, 5]:
    
  方法: push, sum, mean, variance, std_dev ... (12 个方法)
- **SlidingWindowMedian**: 滑动窗口中位数计算器

使用双堆（大顶堆 + 小顶堆）实现，支持 O(log n) 的中位数查询。

示例:
    >>> swm = SlidingWindowMedian(3)
    >>> for val in [1, 2, 3, 4, 5]:
    
  方法: push, median, is_empty, is_full, clear
- **SlidingWindowPercentile**: 滑动窗口百分位数计算器

支持任意百分位数的计算，使用两个有序列表实现。

示例:
    >>> swp = SlidingWindowPercentile(5, percentile=75)
    >>> for val in [1, 2, 3, 4, 5, 6, 7]:
    
  方法: push, percentile_value, set_percentile, is_empty, is_full ... (6 个方法)
- **TimeWindowStats**: 时间窗口统计计算器

基于时间戳的滑动窗口，自动清理过期数据。

示例:
    >>> import time
    >>> tws = TimeWindowStats(window_seconds=10)
    >>> tws
  方法: push, refresh, sum, mean, min ... (11 个方法)
- **SlidingWindowCounter**: 滑动窗口计数器

统计滑动窗口内的事件数量，支持任意类型的键。

示例:
    >>> counter = SlidingWindowCounter(window_size=5)
    >>> for event in ['a', 'b', 'a', 'c', 'a', 'b']:
    
  方法: push, count, total, unique_count, most_common ... (9 个方法)

### 函数

- **sliding_max(data, window_size**) - 计算滑动窗口最大值
- **sliding_min(data, window_size**) - 计算滑动窗口最小值
- **sliding_mean(data, window_size**) - 计算滑动窗口平均值
- **sliding_sum(data, window_size**) - 计算滑动窗口总和
- **sliding_median(data, window_size**) - 计算滑动窗口中位数
- **push(self, value**) - 添加新值到窗口
- **max(self**) - 获取当前窗口的最大值
- **is_empty(self**)
- **is_full(self**)
- **clear(self**) - 清空窗口

... 共 58 个函数

## 使用示例

```python
from mod import sliding_max

# 使用 sliding_max
result = sliding_max()
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
