# AllToolkit - Python Sparkline Utils 📊

**零依赖迷你图表工具 - 终端可视化利器**

---

## 📖 概述

`sparkline_utils` 提供文本迷你图表功能，专为终端/命令行应用设计。使用 Unicode 字符、Braille 盲文模式和 ASCII 符号创建简洁美观的数据可视化，无需任何外部依赖。

---

## ✨ 特性

- **单行迷你图** - Unicode/Braille/ASCII 三种风格
- **多行图表** - 带 Y 轴标签的详细可视化
- **柱状图** - 垂直/水平两种方向
- **仪表盘** - 进度条和百分比显示
- **趋势指示器** - 自动判断上升/下降趋势
- **胜负图** - 游戏/比赛结果可视化
- **直方图** - 数据分布可视化
- **统计摘要** - 快速数据概览
- **零依赖** - 仅使用 Python 标准库

---

## 🚀 快速开始

### 基础迷你图

```python
from sparkline_utils.mod import sparkline

# 基本使用
data = [1, 2, 3, 4, 5, 6, 7, 8]
print(sparkline(data))  # ▁▂▃▄▅▆▇█

# ASCII 风格（兼容性更好）
print(sparkline(data, style='ascii'))  # .:|+*#@W

# 自定义范围
print(sparkline(data, min_val=0, max_val=20))  # ▁▁▁▂▂▃▃▄
```

### Braille 高分辨率迷你图

```python
from sparkline_utils.mod import sparkline_braille

# Braille 模式提供更高分辨率
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(sparkline_braille(data))  # ⡇⣤⣶⣾⣿
```

### 多行图表

```python
from sparkline_utils.mod import sparkline_multiline

data = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45]
print(sparkline_multiline(data, width=20, height=4))
# 输出:
# 45 ┤   ▄▆███
# 23 ┤  ▂▄▆███
# 11 ┤ ▁▃▅▇███
#  1 ┤█▂▄▆████
```

### 柱状图

```python
from sparkline_utils.mod import bar_chart, horizontal_bar_chart

# 垂直柱状图
data = [3, 7, 2, 5, 9]
print(bar_chart(data, labels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri']))

# 水平柱状图
labels = ['Sales', 'Costs', 'Profit', 'Tax']
values = [450, 200, 250, 50]
print(horizontal_bar_chart(labels, values))
```

### 趋势指示器

```python
from sparkline_utils.mod import trend_indicator, trend_sparkline, delta_indicator

# 趋势判断
data = [1, 2, 3, 4, 5]
print(trend_indicator(data))  # ↑

# 带迷你图的趋势
print(trend_sparkline(data))  # ▁▂▃▄▅ 5 ↑

# 变化指标
print(delta_indicator(100, 120))  # +20 (+20.0%) ↑
```

### 仪表盘

```python
from sparkline_utils.mod import gauge, gauge_with_value

# 简单仪表
print(gauge(75, 100, 10))  # ███████░░░

# 带数值显示
print(gauge_with_value(75, 100, 20))  # [███████████████░░░░░] 75%
```

### 胜负图

```python
from sparkline_utils.mod import win_loss_sparkline

# 1=赢, 0=平, -1=输
results = [1, 1, -1, 0, 1, -1, 1, 1]
print(win_loss_sparkline(results))  # ██▄─█▄██
```

### 直方图

```python
from sparkline_utils.mod import histogram

data = [1, 1, 2, 2, 2, 3, 3, 4, 5, 5, 5, 5, 6, 7, 8]
print(histogram(data, bins=5))
```

### 统计摘要

```python
from sparkline_utils.mod import sparkline_stats

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(sparkline_stats(data))  # ▁▂▃▄▅▆▇█ n=10 min=1 max=10 avg=5.5
```

---

## 📚 API 参考

### 核心函数

| 函数 | 说明 | 返回 |
|------|------|------|
| `sparkline(data, ...)` | 单行迷你图 | `str` |
| `sparkline_braille(data, ...)` | Braille 高分辨率迷你图 | `str` |
| `sparkline_multiline(data, ...)` | 多行详细图表 | `str` |

### 图表函数

| 函数 | 说明 | 返回 |
|------|------|------|
| `bar_chart(data, ...)` | 垂直柱状图 | `str` |
| `horizontal_bar_chart(labels, data, ...)` | 水平柱状图 | `str` |
| `histogram(data, ...)` | 直方图 | `str` |

### 指标函数

| 函数 | 说明 | 返回 |
|------|------|------|
| `trend_indicator(data)` | 趋势箭头 | `str` |
| `trend_sparkline(data)` | 带趋势的迷你图 | `str` |
| `delta_indicator(old, new)` | 变化指标 | `str` |
| `gauge(value, max, width)` | 进度条 | `str` |
| `gauge_with_value(value, max, ...)` | 带数值的进度条 | `str` |
| `win_loss_sparkline(data)` | 胜负可视化 | `str` |

### 快捷函数

| 函数 | 说明 | 返回 |
|------|------|------|
| `sparkline_stats(data)` | 统计摘要+迷你图 | `str` |
| `mini_chart(data, type)` | 快速迷你图 | `str` |

### 样式选项

```python
from sparkline_utils.mod import SparklineStyle

# UNICODE - Unicode 块字符 (推荐)
# BRAILLE - Braille 盲文模式 (高分辨率)
# ASCII   - ASCII 字符 (最大兼容性)
# BAR     - 垂直块字符
```

---

## 🎨 示例

### 命令行仪表板

```python
from sparkline_utils.mod import *

# CPU 使用率
cpu_history = [20, 35, 50, 75, 80, 65, 45, 30]
print(f"CPU: {gauge_with_value(cpu_history[-1], 100, 20)}")
print(f"     Trend: {trend_sparkline(cpu_history)}")

# 内存使用
print(f"MEM: {gauge_with_value(62, 100, 20)}")

# 网络流量
traffic = [10, 25, 40, 55, 70, 85, 100, 90]
print(f"NET: {sparkline(traffic)}")
```

### 股票走势

```python
from sparkline_utils.mod import *

prices = [100, 102, 98, 105, 110, 108, 115, 120]
print(f"Price: {sparkline_stats(prices)}")
print(f"Change: {delta_indicator(prices[0], prices[-1])}")
```

### 比赛记录

```python
from sparkline_utils.mod import *

results = [1, 1, 1, -1, 1, 0, 1, -1, 1, 1]  # 8胜 1平 1负
print(f"Record: {win_loss_sparkline(results)}")
print(f"Stats: 8W 1D 1L")
```

---

## 🔧 安装

无需安装，直接导入使用：

```python
from sparkline_utils.mod import sparkline
```

---

## 📝 设计理念

- **极简主义** - 一行代码，一个图表
- **终端友好** - 所有输出适配命令行显示
- **零依赖** - 纯 Python 标准库实现
- **Unicode 优先** - 支持块字符、Braille、箭头等符号
- **ASCII 备选** - 兼容不支持 Unicode 的环境

---

## 📄 License

MIT License - 自由使用，无需授权。

---

## 👤 Author

AllToolkit - https://github.com/ayukyo/alltoolkit