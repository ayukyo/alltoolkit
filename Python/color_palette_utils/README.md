# color_palette_utils - 颜色调色板工具模块

颜色调色板生成、颜色和谐、颜色转换等功能。零外部依赖，纯 Python 实现。

## 功能列表

| 功能 | 说明 |
|------|------|
| 多种调色板生成算法 | 互补、类似、三角、分裂互补、四角、五角 |
| HSL/RGB/HEX 颜色空间转换 | 相互转换 |
| 颜色亮度调整 | 亮化、暗化 |
| 调色板导出 | CSS 变量、JSON、SCSS |
| 随机调色板生成 | 基于种子或随机 |
| 渐变色生成 | 多色渐变 |

## 快速使用

```python
from color_palette_utils.mod import (
    create_palette,
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_hsl,
    hsl_to_rgb,
    lighten,
    darken,
    complementary_palette,
    analogous_palette,
    triadic_palette,
    random_palette,
    gradient_colors,
    export_css_variables
)

# 创建调色板
palette = create_palette(base_color="#FF5733", scheme="complementary")
print(palette)  # ['#FF5733', '#33A1FF']

# 颜色转换
rgb = hex_to_rgb("#FF5733")  # (255, 87, 51)
hex_color = rgb_to_hex(255, 87, 51)  # '#FF5733'
hsl = rgb_to_hsl(255, 87, 51)  # (11.0, 100.0, 60.0)

# 亮化/暗化
lighter = lighten("#FF5733", amount=20)  # 亮化20%
darker = darken("#FF5733", amount=20)    # 暗化20%

# 调色板类型
complementary = complementary_palette("#FF5733")  # 互补色
analogous = analogous_palette("#FF5733")         # 类似色
triadic = triadic_palette("#FF5733")             # 三角色

# 随机调色板
random_pal = random_palette(count=5)

# 渐变色
gradient = gradient_colors("#FF5733", "#33A1FF", steps=10)

# 导出CSS变量
css_vars = export_css_variables(palette, prefix="color")
print(css_vars)
```

## 调色板类型说明

| 类型 | 颜色数 | 说明 |
|------|--------|------|
| **互补色** (`complementary`) | 2 | 对比强烈，视觉冲击 |
| **类似色** (`analogous`) | 3-5 | 柔和协调，自然感 |
| **三角色** (`triadic`) | 3 | 平衡对比 |
| **分裂互补** (`split_complementary`) | 3 | 互补色的柔和版本 |
| **四角色** (`tetradic`) | 4 |丰富变化 |
| **五角色** (`pentadic`) | 5 | 多彩组合 |

## 详细示例

### UI 主题调色板

```python
from color_palette_utils.mod import create_palette, export_css_variables

# 创建UI主题调色板
base = "#3498DB"
ui_palette = create_palette(base, scheme="analogous", count=5)

# 生成CSS变量
css = export_css_variables(
    colors=ui_palette,
    prefix="primary",
    names=["primary", "secondary", "accent", "background", "text"]
)
print(css)
```

### 渐变色生成

```python
from color_palette_utils.mod import gradient_colors

# 生成渐变色序列
gradient = gradient_colors(
    start="#FF5733",
    end="#33A1FF",
    steps=20
)

# 用于热力图或进度条
for i, color in enumerate(gradient):
    print(f"Step {i}: {color}")
```

### 随机调色板

```python
from color_palette_utils.mod import random_palette, ensure_accessible

# 生成随机调色板
palette = random_palette(count=5, seed=42)

# 确保无障碍访问（对比度）
accessible = ensure_accessible(palette, min_contrast=4.5)
```

## API 参考

### 调色板生成

| 函数 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `create_palette(base_color, scheme, count)` | 基色、方案、数量 | List[str] | 创建调色板 |
| `complementary_palette(base_color)` | 基色 | List[str] | 互补调色板 |
| `analogous_palette(base_color, count)` | 基色、数量 | List[str] | 类似调色板 |
| `triadic_palette(base_color)` | 基色 | List[str] | 三角调色板 |
| `random_palette(count, seed)` | 数量、种子 | List[str] | 随机调色板 |

### 颜色转换

| 函数 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `hex_to_rgb(hex_color)` | HEX字符串 | Tuple[int,int,int] | HEX→RGB |
| `rgb_to_hex(r, g, b)` | RGB值 | str | RGB→HEX |
| `rgb_to_hsl(r, g, b)` | RGB值 | Tuple[float,float,float] | RGB→HSL |
| `hsl_to_rgb(h, s, l)` | HSL值 | Tuple[int,int,int] | HSL→RGB |

### 颜色调整

| 函数 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `lighten(color, amount)` | 颜色、百分比 | str | 亮化 |
| `darken(color, amount)` | 颜色、百分比 | str | 暗化 |
| `gradient_colors(start, end, steps)` | 起、终点、步数 | List[str] | 渐变色 |

### 导出

| 函数 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `export_css_variables(colors, prefix)` | 颜色、前缀 | str | CSS变量 |
| `export_json(colors)` | 颜色 | str | JSON格式 |
| `export_scss(colors, prefix)` | 颜色、前缀 | str | SCSS变量 |

## 测试

运行测试：

```bash
python color_palette_utils/color_palette_utils_test.py
```

---

**最后更新**: 2026-05-11