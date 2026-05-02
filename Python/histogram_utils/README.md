# Histogram Utils - 直方图生成工具

零依赖的 Python 直方图生成工具，支持多种输出格式和统计计算。

## 功能特性

- 📊 **自动分组计算** - 使用 Sturges 规则自动确定最佳分组数
- 🎯 **手动控制** - 支持自定义分组数量或分组宽度
- 📈 **多种输出格式** - 文本报告、ASCII 图表、数据字典
- 🔢 **完整统计** - 均值、中位数、标准差、方差等
- 📋 **频率分析** - 相对频率、密度、累积频率
- 🎲 **示例数据生成** - 正态分布、均匀分布、指数分布
- 🚫 **零依赖** - 仅使用 Python 标准库

## 安装

无需安装，直接导入使用：

```python
from histogram_utils import Histogram, create_histogram
```

## 快速使用

### 基础直方图

```python
from histogram_utils import Histogram

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
hist = Histogram(data, bins=5)

# 获取分组信息
for bin in hist.bins:
    print(f"范围 [{bin.lower}, {bin.upper}): {bin.count} 个数据")
```

### 文本报告

```python
print(hist.to_text())
```

输出示例：
```
============================================================
直方图统计报告
============================================================

数据统计:
  数据量: 10
  最小值: 1.0000
  最大值: 10.0000
  平均值: 5.5000
  中位数: 5.5000
  标准差: 2.8723

分组数量: 5
分组宽度: 1.8000

直方图:
------------------------------------------------------------
[1.00, 2.80)          |      2 | ██
[2.80, 4.60)          |      2 | ██
[4.60, 6.40)          |      2 | ██
[6.40, 8.20)          |      2 | ██
[8.20, 10.00)         |      2 | ██
------------------------------------------------------------
```

### ASCII 图表

```python
print(hist.to_ascii_chart(height=10, width=50))
```

### 统计信息

```python
stats = hist.statistics()
print(f"均值: {stats['mean']}")
print(f"标准差: {stats['std_dev']}")
```

### 频率分析

```python
# 相对频率
freqs = hist.frequencies()

# 密度 (频率/宽度)
densities = hist.densities()

# 累积频率
cum_freqs = hist.cumulative_frequencies()
```

### 便捷函数

```python
from histogram_utils import (
    create_histogram,
    frequency_table,
    ascii_histogram,
    text_histogram
)

# 快速创建
hist = create_histogram(data, bins=10)

# 获取频率表
table = frequency_table(data)  # [(lower, upper, count), ...]

# 快速 ASCII 图
print(ascii_histogram(data))

# 快速文本报告
print(text_histogram(data))
```

## 示例数据生成

```python
from histogram_utils import generate_sample_data

# 正态分布
normal_data = generate_sample_data(100, 'normal', mean=50, std_dev=10)

# 均匀分布
uniform_data = generate_sample_data(100, 'uniform', mean=50)

# 指数分布
exp_data = generate_sample_data(100, 'exponential', mean=5)
```

## API 参考

### Histogram 类

```python
Histogram(data, bins=None, bin_width=None, range_min=None, range_max=None)
```

参数：
- `data`: 数值数据列表
- `bins`: 分组数量 (可选，自动计算若为 None)
- `bin_width`: 分组宽度 (可选，优先于 bins)
- `range_min`: 数据范围最小值 (可选)
- `range_max`: 数据范围最大值 (可选)

方法：
- `bins`: 获取所有分组对象
- `frequencies()`: 获取相对频率列表
- `densities()`: 获取密度列表
- `cumulative_counts()`: 获取累积计数
- `cumulative_frequencies()`: 获取累积频率
- `statistics()`: 获取统计信息字典
- `to_dict()`: 转换为字典格式
- `to_text()`: 生成文本报告
- `to_ascii_chart()`: 生成 ASCII 图表

### HistogramBin 类

属性：
- `lower`: 分组下界
- `upper`: 分组上界
- `count`: 分组内数据计数
- `width`: 分组宽度
- `midpoint`: 分组中点值

## 测试

```bash
python histogram_utils_test.py
```

## 许可证

MIT License

## 作者

AllToolkit 自动生成 - 2026-05-02