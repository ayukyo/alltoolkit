# ColorName Utils - 颜色名称映射工具

将 RGB/HEX 颜色转换为人类可读的颜色名称。

## 功能特性

- 🎨 **颜色名称查找** - 将任意颜色映射到最接近的命名颜色
- 🔄 **格式转换** - 支持 RGB、HEX、HSL 格式互转
- 📊 **颜色分类** - 按红/橙/黄/绿/蓝/紫等分类
- ☀️ **亮度分析** - 判断颜色是亮色、中等还是暗色
- 🔥 **温度分析** - 判断颜色是暖色、冷色还是中性
- 🎭 **颜色操作** - 混合、变亮、变暗、饱和度调整
- 🌈 **颜色和谐** - 互补色、类似色、三角色等
- 📦 **丰富数据库** - 包含 200+ 种命名颜色

## 安装使用

```python
from colorname_utils.mod import *
```

零外部依赖，纯 Python 实现。

## 快速开始

### 颜色名称查找

```python
from colorname_utils.mod import get_color_name, RGB, parse_hex

# 通过 RGB 查找
name = get_color_name(RGB(255, 165, 0))
print(name)  # "Orange"

# 通过 HEX 查找
rgb = parse_hex("#FFA500")
name = get_color_name(rgb)
print(name)  # "Orange"
```

### 获取详细颜色信息

```python
from colorname_utils.mod import get_color_info, RGB

info = get_color_info(RGB(255, 165, 0))
print(f"名称: {info.name}")         # Orange
print(f"十六进制: {info.hex}")      # #FFA500
print(f"RGB: {info.rgb}")           # RGB(255, 165, 0)
print(f"类别: {info.category}")     # Orange
print(f"亮度: {info.brightness}")   # Medium
print(f"温度: {info.temperature}")  # Warm
```

### 查找最近的颜色

```python
from colorname_utils.mod import get_n_closest_colors, RGB

matches = get_n_closest_colors(RGB(255, 100, 50), 5)
for m in matches:
    print(f"{m.name}: {m.hex} (距离: {m.distance:.2f})")
```

### 颜色分类

```python
from colorname_utils.mod import get_color_category, RGB

print(get_color_category(RGB(255, 0, 0)))    # Red
print(get_color_category(RGB(255, 165, 0)))  # Orange
print(get_color_category(RGB(0, 255, 255)))  # Cyan
print(get_color_category(RGB(128, 128, 128))) # Gray
```

### 颜色格式转换

```python
from colorname_utils.mod import parse_hex, rgb_to_hsl, hsl_to_rgb

# HEX → RGB
rgb = parse_hex("#FF0000")

# RGB → HSL
hsl = rgb_to_hsl(rgb)
print(hsl)  # HSL(0.0, 100.0%, 50.0%)

# HSL → RGB
rgb_back = hsl_to_rgb(hsl)
```

### 颜色和谐

```python
from colorname_utils.mod import complementary_color, analogous_colors, RGB

blue = RGB(0, 0, 255)

# 互补色
comp = complementary_color(blue)
print(comp.to_hex())  # #FFFF00 (黄色)

# 类似色
analogs = analogous_colors(RGB(0, 255, 0))
for c in analogs:
    print(c.to_hex())
```

### 颜色效果

```python
from colorname_utils.mod import grayscale, sepia, invert_color, RGB

# 灰度
gray = grayscale(RGB(100, 150, 200))

# 棕褐色调
sep = sepia(RGB(100, 150, 200))

# 反转
inv = invert_color(RGB(100, 150, 200))
```

### 随机颜色生成

```python
from colorname_utils.mod import (
    random_color, random_pastel_color, 
    random_dark_color, random_warm_color, random_cool_color
)

# 随机颜色
c1 = random_color()

# 随机柔和色（适合 UI）
c2 = random_pastel_color()

# 随机暗色
c3 = random_dark_color()

# 随机暖色
c4 = random_warm_color()

# 随机冷色
c5 = random_cool_color()
```

### 数据库搜索

```python
from colorname_utils.mod import (
    get_color_by_name, get_all_color_names,
    get_colors_by_category, search_color_names
)

# 按名称获取颜色
red = get_color_by_name("Red")
print(red.to_hex())  # #FF0000

# 获取所有颜色名称
names = get_all_color_names()
print(f"共有 {len(names)} 种颜色")

# 按类别获取颜色
reds = get_colors_by_category("Red")
print(reds)  # ['Red', 'Crimson', 'Fire Brick', ...]

# 搜索颜色名称
results = search_color_names("blue")
for r in results:
    print(f"{r.name}: {r.hex}")
```

## API 参考

### RGB 类

```python
RGB(r, g, b)           # 创建 RGB 颜色
rgb.to_hex()           # 转换为十六进制
rgb.to_hsl()           # 转换为 HSL
rgb.to_tuple()         # 转换为元组
```

### HSL 类

```python
HSL(h, s, l)           # 创建 HSL 颜色 (h: 0-360, s/l: 0-100)
hsl.to_rgb()           # 转换为 RGB
```

### 颜色解析

```python
parse_hex(hex_str)     # 解析十六进制字符串
parse_rgb(rgb_str)     # 解析 RGB 字符串
rgb_to_hex(rgb)        # RGB 转十六进制
rgb_to_hsl(rgb)        # RGB 转 HSL
hsl_to_rgb(hsl)        # HSL 转 RGB
```

### 颜色名称查找

```python
get_color_name(rgb)              # 获取颜色名称
get_closest_color(rgb)           # 获取最接近的颜色匹配
get_n_closest_colors(rgb, n)     # 获取 n 个最接近的颜色
```

### 颜色分析

```python
get_color_category(rgb)          # 获取颜色类别
get_brightness(rgb)              # 获取亮度类别
get_temperature(rgb)             # 获取温度类别
get_color_info(rgb)              # 获取完整颜色信息
```

### 颜色判断

```python
is_light_color(rgb)              # 是否为亮色
is_dark_color(rgb)               # 是否为暗色
get_contrast_color(rgb)          # 获取对比色（黑或白）
are_colors_similar(c1, c2, th)   # 判断颜色是否相似
```

### 颜色操作

```python
blend_colors(c1, c2, ratio)      # 混合颜色
lighten(rgb, amount)             # 变亮
darken(rgb, amount)              # 变暗
saturate(rgb, amount)            # 增加饱和度
desaturate(rgb, amount)          # 降低饱和度
grayscale(rgb)                   # 灰度转换
sepia(rgb)                       # 棕褐色调
invert_color(rgb)                # 反转颜色
adjust_brightness(rgb, factor)   # 调整亮度
```

### 颜色和谐

```python
complementary_color(rgb)         # 互补色
analogous_colors(rgb)            # 类似色
triadic_colors(rgb)              # 三角色
split_complementary_colors(rgb)  # 分裂互补色
tetradic_colors(rgb)             # 四角色
```

### 数据库操作

```python
get_color_by_name(name)          # 按名称获取颜色
get_all_color_names()            # 获取所有颜色名称
get_colors_by_category(cat)      # 按类别获取颜色
search_color_names(query)        # 搜索颜色名称
color_count()                    # 颜色数量
```

### 随机颜色

```python
random_color()                   # 随机颜色
random_pastel_color()            # 随机柔和色
random_dark_color()              # 随机暗色
random_warm_color()              # 随机暖色
random_cool_color()              # 随机冷色
```

## 运行测试

```bash
python colorname_utils_test.py
```

## 作者

AllToolkit

## 日期

2026-05-28