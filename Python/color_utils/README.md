# AllToolkit - Color Utilities 🎨

**零依赖 Python 颜色处理工具库**

---

## 📖 概述

`color_utils` 是一个功能全面的颜色处理工具模块，提供颜色格式转换、颜色操作、调色板生成、无障碍检测等功能。完全使用 Python 标准库实现，无需任何外部依赖。

### 核心功能

- 🔄 **格式转换**: HEX ↔ RGB ↔ HSL ↔ HSV ↔ CMYK
- 🎨 **颜色操作**: 调亮、调暗、混合、反转、饱和度调整、色相旋转
- 🌈 **调色板生成**: 互补色、类似色、三元色、分裂互补色、四元色、单色系
- ♿ **无障碍检测**: 对比度计算、WCAG AA/AAA 合规检查
- 🏷️ **颜色识别**: 颜色命名、相似度检测
- 📊 **实用工具**: 颜色解析、格式化、随机生成、验证

---

## 🚀 快速开始

### 安装

无需安装！直接复制 `mod.py` 到你的项目：

```bash
cp AllToolkit/Python/color_utils/mod.py your_project/
```

### 基础使用

```python
from mod import *

# 颜色转换
hex_color = "#FF5733"
rgb = hex_to_rgb(hex_color)        # (255, 87, 51)
hsl = hex_to_hsl(hex_color)        # (11, 100, 60)
hsv = hex_to_hsv(hex_color)        # (11, 80, 100)
cmyk = hex_to_cmyk(hex_color)      # (0, 66, 80, 0)

# 反向转换
hex_back = rgb_to_hex(rgb)         # "#FF5733"
rgb_back = hsl_to_rgb(hsl)         # (255, 87, 51)
```

---

## 📚 API 参考

### 颜色转换

| 函数 | 描述 | 示例 |
|------|------|------|
| `hex_to_rgb(hex)` | HEX 转 RGB | `hex_to_rgb("#FF5733")` → `(255, 87, 51)` |
| `rgb_to_hex(rgb)` | RGB 转 HEX | `rgb_to_hex((255, 87, 51))` → `"#FF5733"` |
| `rgb_to_hsl(rgb)` | RGB 转 HSL | `rgb_to_hsl((255, 0, 0))` → `(0, 100, 50)` |
| `hsl_to_rgb(hsl)` | HSL 转 RGB | `hsl_to_rgb((0, 100, 50))` → `(255, 0, 0)` |
| `rgb_to_hsv(rgb)` | RGB 转 HSV | `rgb_to_hsv((255, 0, 0))` → `(0, 100, 100)` |
| `hsv_to_rgb(hsv)` | HSV 转 RGB | `hsv_to_rgb((0, 100, 100))` → `(255, 0, 0)` |
| `rgb_to_cmyk(rgb)` | RGB 转 CMYK | `rgb_to_cmyk((255, 0, 0))` → `(0, 100, 100, 0)` |
| `cmyk_to_rgb(cmyk)` | CMYK 转 RGB | `cmyk_to_rgb((0, 100, 100, 0))` → `(255, 0, 0)` |

### 颜色操作

| 函数 | 描述 | 示例 |
|------|------|------|
| `lighten(color, amount)` | 调亮颜色 | `lighten("#FF5733", 0.2)` → `"#FF8C6F"` |
| `darken(color, amount)` | 调暗颜色 | `darken("#FF5733", 0.2)` → `"#CC3A1A"` |
| `mix_colors(c1, c2, ratio)` | 混合两种颜色 | `mix_colors("#FF0000", "#0000FF", 0.5)` → `"#800080"` |
| `invert_color(color)` | 反转颜色 | `invert_color("#FF5733")` → `"#00A8CC"` |
| `saturate(color, amount)` | 增加饱和度 | `saturate("#FF5733", 0.2)` → `"#FF4D22"` |
| `desaturate(color, amount)` | 降低饱和度 | `desaturate("#FF5733", 0.5)` → `"#997A66"` |
| `adjust_hue(color, degrees)` | 旋转色相 | `adjust_hue("#FF5733", 180)` → `"#33CCFF"` |

### 调色板生成

| 函数 | 描述 | 返回 |
|------|------|------|
| `complementary_color(color)` | 互补色 | 单个颜色 |
| `analogous_colors(color, count)` | 类似色 | 颜色列表 |
| `triadic_colors(color)` | 三元色 | 3 个颜色的列表 |
| `split_complementary(color)` | 分裂互补色 | 3 个颜色的列表 |
| `tetradic_colors(color)` | 四元色 | 4 个颜色的列表 |
| `monochromatic_colors(color, count)` | 单色系 | 颜色列表 |
| `generate_gradient(c1, c2, steps)` | 渐变色 | 颜色列表 |

### 无障碍检测

| 函数 | 描述 | 示例 |
|------|------|------|
| `get_luminance(rgb)` | 计算相对亮度 | `get_luminance((255, 255, 255))` → `1.0` |
| `contrast_ratio(c1, c2)` | 计算对比度 | `contrast_ratio("#000", "#FFF")` → `21.0` |
| `is_wcag_aa(c1, c2, large_text)` | 检查 WCAG AA 合规 | `is_wcag_aa("#000", "#FFF")` → `True` |
| `is_wcag_aaa(c1, c2, large_text)` | 检查 WCAG AAA 合规 | `is_wcag_aaa("#000", "#FFF")` → `True` |
| `get_accessible_text_color(bg)` | 获取可读文本颜色 | `get_accessible_text_color("#FFF")` → `"#000"` |

### 颜色识别

| 函数 | 描述 | 示例 |
|------|------|------|
| `get_color_name(color)` | 获取颜色名称 | `get_color_name("#FF0000")` → `"Red"` |
| `color_distance(c1, c2)` | 计算颜色距离 | `color_distance((255,0,0), (0,0,0))` → `255.0` |
| `is_similar_color(c1, c2, threshold)` | 检查颜色相似度 | `is_similar_color("#FF5733", "#FF5834", 5)` → `True` |

### 实用工具

| 函数 | 描述 | 示例 |
|------|------|------|
| `parse_color(color)` | 解析颜色为 RGB | `parse_color("Red")` → `(255, 0, 0)` |
| `format_color(rgb, format)` | 格式化颜色 | `format_color((255,87,51), "rgb")` → `"rgb(255, 87, 51)"` |
| `random_color()` | 生成随机颜色 | `random_color()` → `"#A3F2B1"` |
| `is_valid_hex(color)` | 验证 HEX 颜色 | `is_valid_hex("#FF5733")` → `True` |
| `is_valid_rgb(r, g, b)` | 验证 RGB 值 | `is_valid_rgb(255, 87, 51)` → `True` |

---

## 💡 使用示例

### 示例 1: 设计配色方案

```python
from mod import (
    triadic_colors, complementary_color, 
    lighten, darken, mix_colors
)

base_color = "#3498DB"  # 蓝色

# 生成三元配色
triadic = triadic_colors(base_color)
print(f"三元配色：{triadic}")

# 生成深浅变化
palette = [
    darken(base_color, 0.3),  # 深色
    darken(base_color, 0.15), # 中深色
    base_color,               # 基色
    lighten(base_color, 0.15),# 中浅色
    lighten(base_color, 0.3), # 浅色
]
print(f"单色渐变：{palette}")
```

### 示例 2: 检查无障碍合规性

```python
from mod import (
    contrast_ratio, is_wcag_aa, is_wcag_aaa,
    get_accessible_text_color
)

# 检查按钮颜色和文字的对比度
bg_color = "#3498DB"
text_color = "#FFFFFF"

ratio = contrast_ratio(bg_color, text_color)
print(f"对比度：{ratio}:1")

if is_wcag_aaa(bg_color, text_color):
    print("✓ 符合 WCAG AAA 标准")
elif is_wcag_aa(bg_color, text_color):
    print("✓ 符合 WCAG AA 标准")
else:
    print("✗ 不符合无障碍标准")
    # 获取更好的文字颜色
    better_text = get_accessible_text_color(bg_color)
    print(f"建议使用：{better_text}")
```

### 示例 3: 生成渐变色

```python
from mod import generate_gradient, format_color

# 生成从橙到蓝的渐变
gradient = generate_gradient("#FF5733", "#33CCFF", 10)

for i, color in enumerate(gradient):
    rgb = hex_to_rgb(color)
    print(f"Step {i}: {color} = {format_color(rgb, 'rgb')}")
```

### 示例 4: 颜色识别和匹配

```python
from mod import get_color_name, is_similar_color, color_distance

# 识别颜色
color = "#FF5733"
name = get_color_name(color)
print(f"{color} 是 {name}")

# 检查颜色相似度
target = "#FF5834"
if is_similar_color(color, target, threshold=5):
    print(f"{color} 和 {target} 非常相似")

# 计算颜色距离
distance = color_distance(
    hex_to_rgb(color),
    hex_to_rgb(target)
)
print(f"颜色距离：{distance:.2f}")
```

### 示例 5: 完整的 UI 配色生成器

```python
from mod import *

def generate_ui_theme(base_hex: str):
    """生成完整的 UI 主题配色"""
    base_rgb = hex_to_rgb(base_hex)
    
    theme = {
        # 主色
        'primary': base_hex,
        'primary_light': lighten(base_hex, 0.2),
        'primary_dark': darken(base_hex, 0.2),
        
        # 辅助色（互补色）
        'accent': complementary_color(base_hex),
        
        # 中性色
        'background': '#FFFFFF',
        'surface': '#F5F5F5',
        'text_primary': '#212121',
        'text_secondary': '#757575',
        
        # 状态色
        'success': '#4CAF50',
        'warning': '#FF9800',
        'error': '#F44336',
        'info': base_hex,
    }
    
    # 确保文字可读性
    theme['primary_text'] = get_accessible_text_color(base_hex)
    
    return theme

# 使用示例
theme = generate_ui_theme("#3498DB")
for key, value in theme.items():
    print(f"{key}: {value}")
```

---

## 🧪 运行测试

```bash
cd AllToolkit/Python/color_utils
python color_utils_test.py
```

### 测试覆盖

- ✅ HEX/RGB/HSL/HSV/CMYK 转换
- ✅ 颜色操作（调亮/调暗/混合/反转）
- ✅ 调色板生成（互补/类似/三元/四元）
- ✅ 渐变生成
- ✅ 亮度计算和对比度
- ✅ WCAG AA/AAA 合规检查
- ✅ 颜色命名和相似度
- ✅ 边界值和错误处理

---

## 📊 颜色格式说明

### RGB (Red, Green, Blue)
- 范围：0-255
- 示例：`(255, 87, 51)`
- 用途：屏幕显示、图像处理

### HEX (Hexadecimal)
- 格式：`#RRGGBB` 或 `#RGB`
- 示例：`"#FF5733"`
- 用途：Web CSS、设计工具

### HSL (Hue, Saturation, Lightness)
- H: 0-360°（色相）
- S: 0-100%（饱和度）
- L: 0-100%（亮度）
- 示例：`(11, 100, 60)`
- 用途：颜色调整、 intuitive 编辑

### HSV (Hue, Saturation, Value)
- H: 0-360°（色相）
- S: 0-100%（饱和度）
- V: 0-100%（明度）
- 示例：`(11, 80, 100)`
- 用途：颜色选择器

### CMYK (Cyan, Magenta, Yellow, Key/Black)
- 范围：0-100%
- 示例：`(0, 66, 80, 0)`
- 用途：印刷

---

## ♿ WCAG 无障碍标准

### 对比度要求

| 级别 | 正常文字 | 大文字 (18pt+) |
|------|----------|----------------|
| AA | 4.5:1 | 3.0:1 |
| AAA | 7.0:1 | 4.5:1 |

### 使用建议

```python
# 检查文字可读性
if is_wcag_aa(bg_color, text_color):
    # 符合 AA 标准，适合大多数场景
    pass

# 大文字要求更低
if is_wcag_aa(bg_color, text_color, large_text=True):
    # 适合标题等大文字
    pass
```

---

## 🔧 扩展和自定义

### 添加自定义颜色名称

```python
from mod import COLOR_NAMES

# 添加公司品牌色
COLOR_NAMES["#3498DB"] = "Company Blue"
COLOR_NAMES["#2ECC71"] = "Company Green"

# 现在可以识别这些颜色
name = get_color_name("#3498DB")  # "Company Blue"
```

### 创建自定义调色板函数

```python
from mod import adjust_hue, hex_to_rgb, rgb_to_hex

def custom_palette(base_color, angles):
    """根据自定义角度生成调色板"""
    return [adjust_hue(base_color, angle) for angle in angles]

# 使用
palette = custom_palette("#FF5733", [0, 45, 90, 135, 180, 225, 270, 315])
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

仓库：https://github.com/ayukyo/alltoolkit

---

## 📝 更新日志

### v1.0.0 (2026-04-09)
- ✨ 初始版本
- 🔄 完整的颜色格式转换
- 🎨 丰富的颜色操作函数
- 🌈 多种调色板生成算法
- ♿ WCAG 无障碍支持
- 🏷️ 颜色命名和识别
- 🧪 完整的测试套件
