# Colorblind Utils

色盲友好颜色工具，帮助创建色盲用户可辨识的颜色方案。

## 功能特性

- **色盲模拟**: 模拟不同类型色盲视觉效果
- **颜色转换**: 转换为色盲友好颜色
- **对比检查**: 检查颜色在色盲下的区分度
- **方案生成**: 生成色盲友好的颜色方案
- **类型支持**: 红-绿盲、蓝-黄盲、全色盲

## 快速开始

```python
from colorblind_utils.mod import simulate_colorblindness, get_colorblind_safe_color

# 模拟色盲效果
original_color = (255, 0, 0)  # 红色
protanopia_color = simulate_colorblindness(original_color, "protanopia")

# 获取色盲友好替代色
safe_color = get_colorblind_safe_color("red", "protanopia")
```

## 使用示例

### 色盲模拟

```python
from colorblind_utils.mod import simulate_colorblindness, simulate_image

# 模拟单色
red = (255, 0, 0)
protanopia_red = simulate_colorblindness(red, "protanopia")
deuteranopia_red = simulate_colorblindness(red, "deuteranopia")
tritanopia_red = simulate_colorblindness(red, "tritanopia")

# 色盲类型
# - protanopia: 红色盲（约 1% 男性）
# - deuteranopia: 绿色盲（约 5% 男性）
# - tritanopia: 蓝色盲（约 0.01%）
# - achromatopsia: 全色盲（极罕见）
```

### 色盲友好颜色

```python
from colorblind_utils.mod import get_colorblind_safe_palette

# 获取色盲友好配色方案
palette = get_colorblind_safe_palette(n=5)
print(palette)  # [(230, 159, 0), (86, 180, 233), ...]

# 使用预定义安全色
safe_colors = {
    "orange": (230, 159, 0),
    "sky_blue": (86, 180, 233),
    "bluish_green": (0, 158, 115),
    "yellow": (240, 228, 66),
    "vermillion": (213, 94, 0),
}
```

### 对比度检查

```python
from colorblind_utils.mod import check_color_contrast, are_colors_distinguishable

# 检查两个颜色在色盲下的区分度
color1 = (255, 0, 0)
color2 = (0, 255, 0)

# 正常视力下明显不同，但在红-绿盲下可能混淆
is_distinct = are_colors_distinguishable(color1, color2, "deuteranopia")
print(is_distinct)  # False（在绿盲下红色和绿色相似）
```

### 图表配色

```python
from colorblind_utils.mod import get_chart_palette

# 为数据图表生成色盲友好配色
palette = get_chart_palette(n=8, type="categorical")

# 连续色阶
gradient = get_chart_palette(type="sequential", n=10)
```

### 验证设计

```python
from colorblind_utils.mod import validate_design_for_colorblind

# 验证一组颜色是否色盲友好
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
report = validate_design_for_colorblind(colors)

print(report['protanopia_safe'])  # True/False
print(report['recommendations'])  # 改进建议
```

## API 参考

| 函数 | 说明 |
|------|------|
| `simulate_colorblindness(color, type)` | 模拟色盲效果 |
| `get_colorblind_safe_color(color, type)` | 获取安全替代色 |
| `get_colorblind_safe_palette(n)` | 获取安全配色方案 |
| `check_color_contrast(c1, c2, type)` | 检查对比度 |
| `are_colors_distinguishable(c1, c2, type)` | 检查区分度 |
| `get_chart_palette(n, type)` | 图表配色 |
| `validate_design_for_colorblind(colors)` | 验证设计 |

## 色盲类型

| 类型 | 中文名 | 受影响颜色 | 发生率 |
|------|--------|------------|--------|
| protanopia | 红色盲 | 红/橙/绿 | ~1% 男性 |
| deuteranopia | 绿色盲 | 红/绿 | ~5% 男性 |
| tritanopia | 蓝色盲 | 蓝/黄 | ~0.01% |
| achromatopsia | 全色盲 | 所有颜色 | 极罕见 |

## 推荐配色原则

1. **避免红绿组合**: 最常见的色盲类型
2. **使用蓝色**: 蓝色在所有色盲类型中保持辨识
3. **增加亮度对比**: 亮度差异能辅助区分
4. **使用纹理**: 用不同纹理区分类别
5. **标注文字**: 用文字标注补充颜色信息

## 应用场景

- **数据可视化**: 图表、仪表盘
- **UI 设计**: 用户界面配色
- **文档设计**: 演示文稿、报告
- **网站设计**: 网页配色
- **地图设计**: 地图颜色方案

---

**测试覆盖**: 完整测试套件，覆盖色盲模拟、颜色转换、对比检查等