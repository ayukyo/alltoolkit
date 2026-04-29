# svg_utils - SVG 图形生成工具

[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](./test_svg_utils.py)

零依赖的纯 Python SVG 图形生成库。

## 特性

- **基础形状**: 圆形、矩形、椭圆、线条、多边形
- **路径绘制**: 贝塞尔曲线、弧线、自定义路径
- **文本渲染**: 支持字体、大小、对齐
- **变换操作**: 平移、旋转、缩放、倾斜
- **渐变填充**: 线性渐变、径向渐变
- **样式控制**: 颜色、透明度、描边
- **零依赖**: 纯 Python 实现，无需外部库

## 安装

```python
from svg_utils import SVG, SVGElement
```

## 快速开始

### 创建基础 SVG

```python
from svg_utils import SVG

# 创建 200x200 的 SVG
svg = SVG(width=200, height=200)

# 添加一个红色圆形
svg.circle(cx=100, cy=100, r=50, fill="red")

# 输出 SVG 字符串
print(svg.to_string())

# 保存为文件
svg.save("circle.svg")
```

### 添加多个形状

```python
from svg_utils import SVG

svg = SVG(width=300, height=200)

# 矩形
svg.rect(x=10, y=10, width=80, height=60, fill="blue")

# 圆形
svg.circle(cx=150, cy=50, r=30, fill="green")

# 椭圆
svg.ellipse(cx=250, cy=50, rx=40, ry=20, fill="orange")

# 线条
svg.line(x1=10, y1=100, x2=290, y2=100, stroke="black", stroke_width=2)

# 文本
svg.text(x=150, y=150, content="Hello SVG", font_size=20, fill="purple")

svg.save("shapes.svg")
```

### 使用渐变

```python
from svg_utils import SVG, LinearGradient

svg = SVG(width=200, height=100)

# 定义线性渐变
gradient = LinearGradient(id="my_gradient", x1=0, y1=0, x2=1, y2=0)
gradient.add_stop(offset=0, color="red")
gradient.add_stop(offset=1, color="blue")
svg.add_def(gradient)

# 使用渐变填充
svg.rect(x=10, y=10, width=180, height=80, fill="url(#my_gradient)")

svg.save("gradient.svg")
```

### 变换操作

```python
from svg_utils import SVG

svg = SVG(width=200, height=200)

# 旋转的矩形
svg.rect(x=50, y=50, width=100, height=60, fill="blue", transform="rotate(45 100 80)")

# 平移的圆形
svg.circle(cx=0, cy=0, r=30, fill="red", transform="translate(100, 100)")

svg.save("transform.svg")
```

### 自定义路径

```python
from svg_utils import SVG

svg = SVG(width=200, height=200)

# 使用路径绘制三角形
path_d = "M 100 10 L 190 190 L 10 190 Z"
svg.path(d=path_d, fill="green", stroke="black")

# 贝塞尔曲线
bezier_d = "M 10 100 Q 100 10 190 100"
svg.path(d=bezier_d, stroke="red", stroke_width=3, fill="none")

svg.save("paths.svg")
```

## API 参考

### SVG 类

#### 构造函数
```python
SVG(width=100, height=100, viewBox=None)
```

#### 基础形状方法

| 方法 | 参数 | 说明 |
|-----|------|------|
| `rect(x, y, width, height, ...)` | 位置和尺寸 | 添加矩形 |
| `circle(cx, cy, r, ...)` | 圆心和半径 | 添加圆形 |
| `ellipse(cx, cy, rx, ry, ...)` | 圆心和半轴 | 添加椭圆 |
| `line(x1, y1, x2, y2, ...)` | 起点和终点 | 添加线条 |
| `polygon(points, ...)` | 点列表 | 添加多边形 |
| `polyline(points, ...)` | 点列表 | 添加折线 |
| `path(d, ...)` | 路径字符串 | 添加路径 |

#### 文本方法

```python
text(x, y, content, font_size=12, font_family="Arial", ...)
```

#### 输出方法

| 方法 | 说明 |
|-----|------|
| `to_string()` | 返回 SVG XML 字符串 |
| `save(filename)` | 保存到文件 |
| `add_def(element)` | 添加定义元素（渐变等） |
| `add(element)` | 添加任意 SVG 元素 |

### 渐变类

#### LinearGradient
```python
LinearGradient(id, x1=0, y1=0, x2=1, y2=0)
gradient.add_stop(offset, color, opacity=None)
```

#### RadialGradient
```python
RadialGradient(id, cx=0.5, cy=0.5, r=0.5)
gradient.add_stop(offset, color, opacity=None)
```

## 常用属性

### 填充和描边

- `fill`: 填充颜色（"red", "#ff0000", "rgb(255,0,0)", "url(#gradient)"）
- `stroke`: 描边颜色
- `stroke_width`: 描边宽度
- `stroke_linecap`: 线端样式（"butt", "round", "square"）
- `stroke_linejoin`: 线连接样式（"miter", "round", "bevel"）

### 透明度

- `opacity`: 元素整体透明度（0-1）
- `fill_opacity`: 填充透明度
- `stroke_opacity`: 描边透明度

### 变换

- `transform`: 变换字符串
  - `translate(tx, ty)`: 平移
  - `rotate(angle, cx, cy)`: 旋转
  - `scale(sx, sy)`: 缩放
  - `skewX(angle)`: X 轴倾斜
  - `skewY(angle)`: Y 轴倾斜

## 测试

```bash
python test_svg_utils.py
```

## 许可证

MIT License