# Chart Utils 📊

**Python 图表生成工具模块 - 零依赖，纯 SVG 输出**

---

## 📖 概述

`chart_utils` 是一个全面的 Python 图表生成模块，提供折线图、柱状图、饼图、散点图、面积图等多种图表类型。所有实现均使用 Python 标准库，零外部依赖，输出标准 SVG 格式。

### ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **多种图表** - 折线图、柱状图、饼图、散点图、面积图
- **SVG 输出** - 标准 SVG 格式，可直接在浏览器中查看
- **高度可配置** - 颜色、尺寸、网格、图例等完全可定制
- **类型安全** - 完整的类型注解
- **生产就绪** - 完整的错误处理和边界检查
- **全面测试** - 60+ 测试用例覆盖所有功能

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 从 AllToolkit 复制
cp AllToolkit/Python/chart_utils/mod.py your_project/

# 或者克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

---

## 🚀 快速开始

```python
from mod import line_chart, bar_chart, pie_chart, DataSeries

# 创建数据
data = [
    DataSeries(name="2025 年", data=[120, 150, 180, 220, 190, 240]),
    DataSeries(name="2026 年", data=[140, 170, 200, 250, 230, 280])
]

# 生成折线图
svg = line_chart(data, title="月度销售对比", x_labels=["1 月", "2 月", "3 月", "4 月", "5 月", "6 月"])

# 保存为文件
with open("chart.svg", "w") as f:
    f.write(svg)

# 或在 HTML 中直接使用
print(svg)
```

---

## 📚 API 参考

### 数据类

#### `DataSeries`

表示一个数据系列。

```python
from mod import DataSeries

series = DataSeries(
    name="销售额",           # 系列名称
    data=[10, 20, 30, 40],  # 数据值
    color="#3498db",        # 颜色（可选）
    labels=["A", "B", "C", "D"]  # 标签（可选）
)
```

#### `ChartConfig`

图表配置。

```python
from mod import ChartConfig

config = ChartConfig(
    width=800,              # 宽度（像素）
    height=600,             # 高度（像素）
    margin_top=60,          # 上边距
    margin_right=60,        # 右边距
    margin_bottom=80,       # 下边距
    margin_left=80,         # 左边距
    background_color="#ffffff",   # 背景色
    grid_color="#e0e0e0",         # 网格颜色
    text_color="#333333",         # 文字颜色
    font_family="Arial",          # 字体
    font_size=12,                 # 字体大小
    title_font_size=16,           # 标题字体大小
    show_grid=True,               # 显示网格
    show_legend=True,             # 显示图例
    legend_position="top-right"   # 图例位置
)
```

---

### 图表函数

#### `line_chart(data, title="", x_labels=None, y_label="", config=None)`

创建折线图。

```python
from mod import line_chart, DataSeries

data = [
    DataSeries(name="产品 A", data=[10, 15, 20, 25, 30]),
    DataSeries(name="产品 B", data=[8, 12, 18, 22, 28])
]

svg = line_chart(
    data,
    title="产品销售趋势",
    x_labels=["Q1", "Q2", "Q3", "Q4", "Q5"],
    y_label="销售额 (万元)"
)
```

**参数:**
- `data`: 数据系列列表
- `title`: 图表标题
- `x_labels`: X 轴标签
- `y_label`: Y 轴标签
- `config`: 图表配置

---

#### `bar_chart(data, title="", x_labels=None, y_label="", config=None, horizontal=False)`

创建柱状图。

```python
from mod import bar_chart, DataSeries

data = [
    DataSeries(name="第一季度", data=[100, 150, 200]),
    DataSeries(name="第二季度", data=[120, 170, 220])
]

# 垂直柱状图
svg = bar_chart(data, title="季度销售", x_labels=["产品 A", "产品 B", "产品 C"])

# 水平柱状图
svg = bar_chart(data, horizontal=True)
```

**参数:**
- `data`: 数据系列列表
- `title`: 图表标题
- `x_labels`: X 轴标签
- `y_label`: Y 轴标签
- `config`: 图表配置
- `horizontal`: 是否水平显示

---

#### `pie_chart(data, title="", show_percentages=True, show_labels=True, config=None, explode=None)`

创建饼图。

```python
from mod import pie_chart, DataSeries

data = [DataSeries(
    name="市场份额",
    data=[30, 45, 15, 10],
    labels=["产品 A", "产品 B", "产品 C", "产品 D"]
)]

# 基本饼图
svg = pie_chart(data, title="市场份额分布")

# 带爆炸效果
svg = pie_chart(data, explode=[0, 0.1, 0, 0])

# 只显示百分比
svg = pie_chart(data, show_labels=False, show_percentages=True)
```

**参数:**
- `data`: 数据系列（通常一个系列）
- `title`: 图表标题
- `show_percentages`: 显示百分比
- `show_labels`: 显示标签
- `config`: 图表配置
- `explode`: 爆炸效果（每个扇区的突出距离 0-0.5）

---

#### `scatter_plot(x_data, y_data, title="", x_label="", y_label="", point_labels=None, trend_line=False, config=None)`

创建散点图。

```python
from mod import scatter_plot

# 基本散点图
x_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y_vals = [2.3, 3.8, 5.1, 7.2, 8.9, 11.2, 13.5, 15.1, 17.8, 20.1]

svg = scatter_plot(
    x_vals, y_vals,
    title="相关性分析",
    x_label="广告投入 (万元)",
    y_label="销售额 (万元)"
)

# 带趋势线
svg = scatter_plot(x_vals, y_vals, trend_line=True)

# 带点标签
svg = scatter_plot(x_vals, y_vals, point_labels=["A", "B", "C", "D", "E"])
```

**参数:**
- `x_data`: X 轴数据
- `y_data`: Y 轴数据
- `title`: 图表标题
- `x_label`: X 轴标签
- `y_label`: Y 轴标签
- `point_labels`: 数据点标签
- `trend_line`: 显示趋势线
- `config`: 图表配置

---

#### `area_chart(data, title="", x_labels=None, y_label="", config=None, stacked=False)`

创建面积图。

```python
from mod import area_chart, DataSeries

data = [
    DataSeries(name="线上", data=[10, 20, 30, 40, 50]),
    DataSeries(name="线下", data=[15, 25, 35, 45, 55])
]

# 普通面积图
svg = area_chart(data, title="销售渠道")

# 堆叠面积图
svg = area_chart(data, stacked=True)
```

**参数:**
- `data`: 数据系列列表
- `title`: 图表标题
- `x_labels`: X 轴标签
- `y_label`: Y 轴标签
- `config`: 图表配置
- `stacked`: 是否堆叠

---

### 工具函数

#### `save_svg(svg_content, filepath)`

保存 SVG 到文件。

```python
from mod import save_svg, line_chart, DataSeries

data = [DataSeries(name="Test", data=[1, 2, 3, 4, 5])]
svg = line_chart(data)
save_svg(svg, "output.svg")
```

---

#### `svg_to_data_uri(svg_content)`

将 SVG 转换为 Data URI。

```python
from mod import svg_to_data_uri

svg = '<svg>...</svg>'
data_uri = svg_to_data_uri(svg)
# 可直接用于 HTML: <img src="{data_uri}">
```

---

#### `create_sample_data()`

创建示例数据用于测试。

```python
from mod import create_sample_data, line_chart

data = create_sample_data()  # 12 个月的销售数据
svg = line_chart(data, title="示例图表")
```

---

## 📝 示例

### 1. 销售趋势对比

```python
from mod import line_chart, DataSeries, save_svg

data = [
    DataSeries(name="2025 年", 
               data=[120, 150, 180, 220, 190, 240, 280, 260, 300, 320, 350, 380],
               labels=["1 月", "2 月", "3 月", "4 月", "5 月", "6 月", 
                      "7 月", "8 月", "9 月", "10 月", "11 月", "12 月"]),
    DataSeries(name="2026 年", 
               data=[140, 170, 200, 250, 230, 280, 320, 300, 350, 380, 400, 420])
]

svg = line_chart(data, title="年度销售对比", y_label="销售额 (万元)")
save_svg(svg, "sales_trend.svg")
```

### 2. 产品市场份额

```python
from mod import pie_chart, DataSeries, save_svg

data = [DataSeries(
    name="市场份额",
    data=[35, 25, 20, 12, 8],
    labels=["产品 A", "产品 B", "产品 C", "产品 D", "其他"]
)]

svg = pie_chart(data, title="产品市场份额", show_percentages=True, explode=[0.05, 0, 0, 0, 0])
save_svg(svg, "market_share.svg")
```

### 3. 相关性分析

```python
from mod import scatter_plot, save_svg
import random

# 生成模拟数据
random.seed(42)
x_vals = [random.uniform(0, 100) for _ in range(100)]
y_vals = [x * 0.8 + random.uniform(-10, 10) for x in x_vals]

svg = scatter_plot(
    x_vals, y_vals,
    title="广告投入与销售相关性",
    x_label="广告投入 (万元)",
    y_label="销售额 (万元)",
    trend_line=True
)
save_svg(svg, "correlation.svg")
```

### 4. 堆叠面积图

```python
from mod import area_chart, DataSeries, save_svg

data = [
    DataSeries(name="移动端", data=[30, 40, 50, 60, 70, 80]),
    DataSeries(name="桌面端", data=[50, 45, 40, 35, 30, 25]),
    DataSeries(name="平板", data=[20, 25, 30, 35, 40, 45])
]

svg = area_chart(data, title="访问设备分布", stacked=True, y_label="访问量 (千)")
save_svg(svg, "device_distribution.svg")
```

### 5. 自定义样式

```python
from mod import bar_chart, DataSeries, ChartConfig, save_svg

config = ChartConfig(
    width=1000,
    height=600,
    background_color="#1a1a2e",
    grid_color="#16213e",
    text_color="#eaeaea",
    show_grid=True,
    show_legend=True
)

data = [DataSeries(name="数据", data=[10, 25, 40, 55, 70], color="#e94560")]

svg = bar_chart(data, title="深色主题图表", config=config)
save_svg(svg, "dark_theme.svg")
```

---

## 🧪 运行测试

```bash
cd chart_utils
python chart_utils_test.py
```

测试覆盖：
- 颜色工具函数
- 数学工具函数
- SVG 构建器
- 数据系列和配置
- 所有 5 种图表类型
- 工具函数
- 边界情况（空数据、单值、负值等）
- Unicode 支持
- 集成测试

---

## 🎨 颜色配置

模块内置 15 种默认颜色：

```python
DEFAULT_COLORS = [
    "#3498db",  # 蓝色
    "#e74c3c",  # 红色
    "#2ecc71",  # 绿色
    "#f39c12",  # 橙色
    "#9b59b6",  # 紫色
    "#1abc9c",  # 青色
    "#e67e22",  # 深橙
    "#34495e",  # 深蓝灰
    "#95a5a6",  # 灰色
    "#d35400",  # 深橙红
    "#27ae60",  # 深绿
    "#2980b9",  # 深蓝
    "#8e44ad",  # 深紫
    "#f1c40f",  # 金黄
    "#16a085"   # 深青
]
```

---

## 🔧 高级用法

### SVG 构建器直接使用

```python
from mod import SVGBuilder

svg = SVGBuilder(400, 300)
svg.rect(0, 0, 400, 300, fill="#f0f0f0")
svg.circle(200, 150, 50, fill="#3498db")
svg.text(200, 100, "Hello", text_anchor="middle")
content = svg.build("My Chart")

with open("custom.svg", "w") as f:
    f.write(content)
```

### 在 HTML 中嵌入

```python
from mod import line_chart, DataSeries, svg_to_data_uri

data = [DataSeries(name="Test", data=[1, 2, 3, 4, 5])]
svg = line_chart(data)
data_uri = svg_to_data_uri(svg)

html = f"""
<!DOCTYPE html>
<html>
<head><title>Chart</title></head>
<body>
    <img src="{data_uri}" alt="Chart">
</body>
</html>
"""

with open("chart.html", "w") as f:
    f.write(html)
```

---

## 📊 性能提示

- SVG 文件大小与数据点数量成正比
- 对于大数据集（>1000 点），考虑抽样或聚合
- 多个图表可复用相同配置对象
- 批量生成时建议复用 ChartConfig 实例

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License
