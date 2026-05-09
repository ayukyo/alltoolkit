"""
颜色调色板工具模块

提供颜色调色板生成、颜色和谐、颜色转换等功能。
零外部依赖，纯 Python 实现。

功能：
- 多种调色板生成算法（互补、类似、三角、分裂互补、四角、五角）
- HSL/RGB/HEX 颜色空间转换
- 颜色亮度调整
- 调色板导出（CSS 变量、JSON、SCSS）
- 随机调色板生成
- 渐变色生成
"""

import math
import random
from typing import List, Tuple, Dict, Optional, Union


# ============ 颜色空间转换 ============

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    将十六进制颜色转换为 RGB 值。
    
    Args:
        hex_color: 十六进制颜色字符串，如 '#FF0000' 或 'FF0000'
    
    Returns:
        RGB 元组 (r, g, b)，每个值在 0-255 范围内
    
    Example:
        >>> hex_to_rgb('#FF0000')
        (255, 0, 0)
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int, include_hash: bool = True) -> str:
    """
    将 RGB 值转换为十六进制颜色字符串。
    
    Args:
        r: 红色值 (0-255)
        g: 绿色值 (0-255)
        b: 蓝色值 (0-255)
        include_hash: 是否包含 '#' 前缀
    
    Returns:
        十六进制颜色字符串
    
    Example:
        >>> rgb_to_hex(255, 0, 0)
        '#FF0000'
    """
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    hex_str = f'{r:02X}{g:02X}{b:02X}'
    return f'#{hex_str}' if include_hash else hex_str


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    将 RGB 转换为 HSL 颜色空间。
    
    Args:
        r: 红色值 (0-255)
        g: 绿色值 (0-255)
        b: 蓝色值 (0-255)
    
    Returns:
        HSL 元组 (h, s, l)，h 为 0-360 度，s 和 l 为 0-100%
    
    Example:
        >>> rgb_to_hsl(255, 0, 0)
        (0.0, 100.0, 50.0)
    """
    r, g, b = r / 255, g / 255, b / 255
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    diff = max_c - min_c
    
    l = (max_c + min_c) / 2
    
    if diff == 0:
        h = s = 0
    else:
        s = diff / (2 - max_c - min_c) if l > 0.5 else diff / (max_c + min_c)
        
        if max_c == r:
            h = (g - b) / diff + (6 if g < b else 0)
        elif max_c == g:
            h = (b - r) / diff + 2
        else:
            h = (r - g) / diff + 4
        
        h *= 60
    
    return (h, s * 100, l * 100)


def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    """
    将 HSL 转换为 RGB 颜色空间。
    
    Args:
        h: 色相 (0-360 度)
        s: 饱和度 (0-100%)
        l: 亮度 (0-100%)
    
    Returns:
        RGB 元组 (r, g, b)，每个值在 0-255 范围内
    
    Example:
        >>> hsl_to_rgb(0, 100, 50)
        (255, 0, 0)
    """
    s /= 100
    l /= 100
    
    if s == 0:
        v = int(l * 255)
        return (v, v, v)
    
    def hue_to_rgb(p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1/6:
            return p + (q - p) * 6 * t
        if t < 1/2:
            return q
        if t < 2/3:
            return p + (q - p) * (2/3 - t) * 6
        return p
    
    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q
    
    r = int(round(hue_to_rgb(p, q, h/360 + 1/3) * 255))
    g = int(round(hue_to_rgb(p, q, h/360) * 255))
    b = int(round(hue_to_rgb(p, q, h/360 - 1/3) * 255))
    
    return (r, g, b)


def hex_to_hsl(hex_color: str) -> Tuple[float, float, float]:
    """将十六进制颜色转换为 HSL。"""
    return rgb_to_hsl(*hex_to_rgb(hex_color))


def hsl_to_hex(h: float, s: float, l: float, include_hash: bool = True) -> str:
    """将 HSL 转换为十六进制颜色。"""
    return rgb_to_hex(*hsl_to_rgb(h, s, l), include_hash)


# ============ 颜色调整 ============

def adjust_lightness(hex_color: str, amount: float) -> str:
    """
    调整颜色的亮度。
    
    Args:
        hex_color: 十六进制颜色
        amount: 亮度调整量 (-100 到 100)，正值变亮，负值变暗
    
    Returns:
        调整后的十六进制颜色
    
    Example:
        >>> adjust_lightness('#FF0000', 20)
        '#FF6666'
    """
    h, s, l = hex_to_hsl(hex_color)
    l = max(0, min(100, l + amount))
    return hsl_to_hex(h, s, l)


def adjust_saturation(hex_color: str, amount: float) -> str:
    """
    调整颜色的饱和度。
    
    Args:
        hex_color: 十六进制颜色
        amount: 饱和度调整量 (-100 到 100)
    
    Returns:
        调整后的十六进制颜色
    """
    h, s, l = hex_to_hsl(hex_color)
    s = max(0, min(100, s + amount))
    return hsl_to_hex(h, s, l)


def get_complementary(hex_color: str) -> str:
    """
    获取互补色。
    
    Args:
        hex_color: 十六进制颜色
    
    Returns:
        互补色的十六进制值
    
    Example:
        >>> get_complementary('#FF0000')  # 红色的互补色是青色
        '#00FFFF'
    """
    h, s, l = hex_to_hsl(hex_color)
    return hsl_to_hex((h + 180) % 360, s, l)


# ============ 调色板生成 ============

def generate_complementary_palette(base_color: str) -> List[str]:
    """
    生成互补色调色板（2色）。
    
    Args:
        base_color: 基础颜色（十六进制）
    
    Returns:
        包含基础色和互补色的列表
    """
    return [base_color, get_complementary(base_color)]


def generate_analogous_palette(base_color: str, angle: float = 30) -> List[str]:
    """
    生成类似色调色板（3色）。
    
    类似色是在色轮上相邻的颜色，通常相差 30 度。
    
    Args:
        base_color: 基础颜色（十六进制）
        angle: 色相角度差（默认 30 度）
    
    Returns:
        包含基础色和两个类似色的列表
    """
    h, s, l = hex_to_hsl(base_color)
    return [
        hsl_to_hex((h - angle) % 360, s, l),
        base_color,
        hsl_to_hex((h + angle) % 360, s, l)
    ]


def generate_triadic_palette(base_color: str) -> List[str]:
    """
    生成三角色调色板（3色）。
    
    三角色在色轮上均匀分布，相差 120 度。
    
    Args:
        base_color: 基础颜色（十六进制）
    
    Returns:
        包含三个颜色的列表
    """
    h, s, l = hex_to_hsl(base_color)
    return [
        base_color,
        hsl_to_hex((h + 120) % 360, s, l),
        hsl_to_hex((h + 240) % 360, s, l)
    ]


def generate_split_complementary_palette(base_color: str, angle: float = 30) -> List[str]:
    """
    生成分裂互补色调色板（3色）。
    
    分裂互补色是互补色两侧的颜色。
    
    Args:
        base_color: 基础颜色（十六进制）
        angle: 与互补色的角度差（默认 30 度）
    
    Returns:
        包含三个颜色的列表
    """
    h, s, l = hex_to_hsl(base_color)
    comp_h = (h + 180) % 360
    return [
        base_color,
        hsl_to_hex((comp_h - angle) % 360, s, l),
        hsl_to_hex((comp_h + angle) % 360, s, l)
    ]


def generate_tetradic_palette(base_color: str) -> List[str]:
    """
    生成四角色调色板（4色）。
    
    四角色在色轮上均匀分布，相差 90 度。
    
    Args:
        base_color: 基础颜色（十六进制）
    
    Returns:
        包含四个颜色的列表
    """
    h, s, l = hex_to_hsl(base_color)
    return [
        base_color,
        hsl_to_hex((h + 90) % 360, s, l),
        hsl_to_hex((h + 180) % 360, s, l),
        hsl_to_hex((h + 270) % 360, s, l)
    ]


def generate_pentadic_palette(base_color: str) -> List[str]:
    """
    生成五角色调色板（5色）。
    
    五角色在色轮上均匀分布，相差 72 度。
    
    Args:
        base_color: 基础颜色（十六进制）
    
    Returns:
        包含五个颜色的列表
    """
    h, s, l = hex_to_hsl(base_color)
    return [
        base_color,
        hsl_to_hex((h + 72) % 360, s, l),
        hsl_to_hex((h + 144) % 360, s, l),
        hsl_to_hex((h + 216) % 360, s, l),
        hsl_to_hex((h + 288) % 360, s, l)
    ]


def generate_square_palette(base_color: str) -> List[str]:
    """
    生成方形调色板（4色）。
    
    方形调色板与四角调色板相同。
    
    Args:
        base_color: 基础颜色（十六进制）
    
    Returns:
        包含四个颜色的列表
    """
    return generate_tetradic_palette(base_color)


def generate_monochromatic_palette(base_color: str, steps: int = 5) -> List[str]:
    """
    生成单色调色板。
    
    通过调整基础色的亮度生成多个颜色。
    
    Args:
        base_color: 基础颜色（十六进制）
        steps: 颜色数量（默认 5）
    
    Returns:
        包含不同亮度变体的列表
    """
    h, s, l = hex_to_hsl(base_color)
    palette = []
    
    for i in range(steps):
        new_l = (i + 1) * (100 / (steps + 1))
        palette.append(hsl_to_hex(h, s, new_l))
    
    return palette


def generate_shades(base_color: str, steps: int = 5) -> List[str]:
    """
    生成基础色的阴影色（变暗）。
    
    Args:
        base_color: 基础颜色（十六进制）
        steps: 阴影数量
    
    Returns:
        阴影色列表
    """
    h, s, l = hex_to_hsl(base_color)
    palette = []
    
    for i in range(steps):
        factor = i / steps
        new_l = l * (1 - factor)
        palette.append(hsl_to_hex(h, s, max(0, new_l)))
    
    return palette


def generate_tints(base_color: str, steps: int = 5) -> List[str]:
    """
    生成基础色的着色色（变亮）。
    
    Args:
        base_color: 基础颜色（十六进制）
        steps: 着色数量
    
    Returns:
        着色色列表
    """
    h, s, l = hex_to_hsl(base_color)
    palette = []
    
    for i in range(steps):
        factor = i / steps
        new_l = l + (100 - l) * factor
        palette.append(hsl_to_hex(h, s, min(100, new_l)))
    
    return palette


def generate_tones(base_color: str, steps: int = 5) -> List[str]:
    """
    生成基础色的色调色（降低饱和度）。
    
    Args:
        base_color: 基础颜色（十六进制）
        steps: 色调数量
    
    Returns:
        色调色列表
    """
    h, s, l = hex_to_hsl(base_color)
    palette = []
    
    for i in range(steps):
        factor = i / steps
        new_s = s * (1 - factor)
        palette.append(hsl_to_hex(h, max(0, new_s), l))
    
    return palette


def generate_gradient(start_color: str, end_color: str, steps: int = 10) -> List[str]:
    """
    生成两个颜色之间的渐变。
    
    Args:
        start_color: 起始颜色（十六进制）
        end_color: 结束颜色（十六进制）
        steps: 渐变步数
    
    Returns:
        渐变色列表
    """
    h1, s1, l1 = hex_to_hsl(start_color)
    h2, s2, l2 = hex_to_hsl(end_color)
    
    # 处理色相的最短路径
    if abs(h2 - h1) > 180:
        if h1 > h2:
            h2 += 360
        else:
            h1 += 360
    
    palette = []
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0
        h = (h1 + (h2 - h1) * t) % 360
        s = s1 + (s2 - s1) * t
        l = l1 + (l2 - l1) * t
        palette.append(hsl_to_hex(h, s, l))
    
    return palette


def generate_multi_gradient(colors: List[str], steps_per_segment: int = 5) -> List[str]:
    """
    生成多色渐变。
    
    Args:
        colors: 颜色列表
        steps_per_segment: 每段渐变的步数
    
    Returns:
        完整渐变色列表
    """
    if len(colors) < 2:
        return colors.copy()
    
    palette = [colors[0]]
    for i in range(len(colors) - 1):
        segment = generate_gradient(colors[i], colors[i+1], steps_per_segment + 1)
        palette.extend(segment[1:])  # 避免重复端点
    
    return palette


# ============ 随机调色板 ============

def random_color(saturation: float = 70, lightness: float = 50) -> str:
    """
    生成随机颜色。
    
    Args:
        saturation: 饱和度 (0-100)
        lightness: 亮度 (0-100)
    
    Returns:
        随机颜色的十六进制值
    """
    h = random.uniform(0, 360)
    return hsl_to_hex(h, saturation, lightness)


def random_palette(count: int = 5, 
                   saturation_range: Tuple[float, float] = (60, 90),
                   lightness_range: Tuple[float, float] = (40, 60)) -> List[str]:
    """
    生成随机调色板。
    
    Args:
        count: 颜色数量
        saturation_range: 饱和度范围
        lightness_range: 亮度范围
    
    Returns:
        随机颜色列表
    """
    palette = []
    for _ in range(count):
        h = random.uniform(0, 360)
        s = random.uniform(*saturation_range)
        l = random.uniform(*lightness_range)
        palette.append(hsl_to_hex(h, s, l))
    return palette


def random_harmonious_palette(harmony_type: str = 'triadic') -> List[str]:
    """
    生成随机和谐调色板。
    
    Args:
        harmony_type: 和谐类型 ('complementary', 'analogous', 'triadic', 
                                'split_complementary', 'tetradic', 'pentadic')
    
    Returns:
        和谐调色板
    """
    base = random_color()
    
    generators = {
        'complementary': generate_complementary_palette,
        'analogous': generate_analogous_palette,
        'triadic': generate_triadic_palette,
        'split_complementary': generate_split_complementary_palette,
        'tetradic': generate_tetradic_palette,
        'pentadic': generate_pentadic_palette,
    }
    
    generator = generators.get(harmony_type, generate_triadic_palette)
    return generator(base)


def random_warm_palette(count: int = 5) -> List[str]:
    """生成暖色调随机调色板（红、橙、黄区域）。"""
    palette = []
    for _ in range(count):
        h = random.uniform(0, 60)  # 暖色区域
        s = random.uniform(60, 90)
        l = random.uniform(40, 60)
        palette.append(hsl_to_hex(h, s, l))
    return palette


def random_cool_palette(count: int = 5) -> List[str]:
    """生成冷色调随机调色板（蓝、绿、紫区域）。"""
    palette = []
    for _ in range(count):
        h = random.uniform(180, 300)  # 冷色区域
        s = random.uniform(60, 90)
        l = random.uniform(40, 60)
        palette.append(hsl_to_hex(h, s, l))
    return palette


def random_pastel_palette(count: int = 5) -> List[str]:
    """生成柔和色调随机调色板。"""
    palette = []
    for _ in range(count):
        h = random.uniform(0, 360)
        s = random.uniform(30, 50)
        l = random.uniform(70, 85)
        palette.append(hsl_to_hex(h, s, l))
    return palette


# ============ 调色板导出 ============

def palette_to_css_variables(palette: List[str], 
                             prefix: str = 'color',
                             variable_names: Optional[List[str]] = None) -> str:
    """
    将调色板转换为 CSS 变量格式。
    
    Args:
        palette: 颜色列表
        prefix: 变量前缀
        variable_names: 自定义变量名列表
    
    Returns:
        CSS 变量字符串
    
    Example:
        >>> palette_to_css_variables(['#FF0000', '#00FF00'])
        ':root {\\n  --color-1: #FF0000;\\n  --color-2: #00FF00;\\n}'
    """
    if variable_names is None:
        variable_names = [f'{prefix}-{i+1}' for i in range(len(palette))]
    
    lines = [':root {']
    for name, color in zip(variable_names, palette):
        lines.append(f'  --{name}: {color};')
    lines.append('}')
    
    return '\n'.join(lines)


def palette_to_scss_variables(palette: List[str],
                              prefix: str = 'color',
                              variable_names: Optional[List[str]] = None) -> str:
    """
    将调色板转换为 SCSS 变量格式。
    
    Args:
        palette: 颜色列表
        prefix: 变量前缀
        variable_names: 自定义变量名列表
    
    Returns:
        SCSS 变量字符串
    """
    if variable_names is None:
        variable_names = [f'{prefix}-{i+1}' for i in range(len(palette))]
    
    lines = []
    for name, color in zip(variable_names, palette):
        lines.append(f'${name}: {color};')
    
    return '\n'.join(lines)


def palette_to_json(palette: List[str], 
                    name: str = 'palette',
                    include_rgb: bool = False) -> Dict:
    """
    将调色板转换为 JSON 格式。
    
    Args:
        palette: 颜色列表
        name: 调色板名称
        include_rgb: 是否包含 RGB 值
    
    Returns:
        JSON 兼容的字典
    """
    colors = []
    for i, hex_color in enumerate(palette):
        color_data = {'index': i + 1, 'hex': hex_color}
        if include_rgb:
            color_data['rgb'] = hex_to_rgb(hex_color)
        colors.append(color_data)
    
    return {
        'name': name,
        'count': len(palette),
        'colors': colors
    }


def palette_to_tailwind_config(palette: List[str], 
                               name: str = 'custom') -> str:
    """
    将调色板转换为 Tailwind CSS 配置格式。
    
    Args:
        palette: 颜色列表
        name: 调色板名称
    
    Returns:
        Tailwind 配置字符串
    """
    lines = [f'{name}: {{']
    
    # Tailwind 标准色阶名称
    scale_names = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900', '950']
    
    for i, color in enumerate(palette):
        # 如果颜色数量与标准色阶匹配，使用标准名称
        if len(palette) <= len(scale_names):
            idx = i * (len(scale_names) - 1) // max(1, len(palette) - 1) if len(palette) > 1 else 5
            name_part = scale_names[idx]
        else:
            name_part = str(i + 1)
        
        lines.append(f"    '{name_part}': '{color}',")
    
    lines.append('  }')
    
    return '\n'.join(lines)


# ============ 色彩对比度和可访问性 ============

def get_luminance(hex_color: str) -> float:
    """
    计算颜色的相对亮度。
    
    Args:
        hex_color: 十六进制颜色
    
    Returns:
        相对亮度值 (0-1)
    """
    r, g, b = hex_to_rgb(hex_color)
    
    def channel_luminance(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    return 0.2126 * channel_luminance(r) + 0.7152 * channel_luminance(g) + 0.0722 * channel_luminance(b)


def get_contrast_ratio(color1: str, color2: str) -> float:
    """
    计算两个颜色之间的对比度比率。
    
    Args:
        color1: 第一个颜色（十六进制）
        color2: 第二个颜色（十六进制）
    
    Returns:
        对比度比率 (1-21)
    
    Example:
        >>> get_contrast_ratio('#FFFFFF', '#000000')
        21.0
    """
    l1 = get_luminance(color1)
    l2 = get_luminance(color2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


def meets_wcag_aa(foreground: str, background: str, large_text: bool = False) -> bool:
    """
    检查颜色组合是否满足 WCAG AA 标准。
    
    Args:
        foreground: 前景色（十六进制）
        background: 背景色（十六进制）
        large_text: 是否为大文本
    
    Returns:
        是否满足 WCAG AA 标准
    """
    ratio = get_contrast_ratio(foreground, background)
    threshold = 3.0 if large_text else 4.5
    return ratio >= threshold


def meets_wcag_aaa(foreground: str, background: str, large_text: bool = False) -> bool:
    """
    检查颜色组合是否满足 WCAG AAA 标准。
    
    Args:
        foreground: 前景色（十六进制）
        background: 背景色（十六进制）
        large_text: 是否为大文本
    
    Returns:
        是否满足 WCAG AAA 标准
    """
    ratio = get_contrast_ratio(foreground, background)
    threshold = 4.5 if large_text else 7.0
    return ratio >= threshold


def suggest_accessible_color(base_color: str, 
                             background: str = '#FFFFFF',
                             target_ratio: float = 4.5) -> str:
    """
    建议一个满足对比度要求的颜色调整。
    
    Args:
        base_color: 基础颜色（十六进制）
        background: 背景色（十六进制）
        target_ratio: 目标对比度比率
    
    Returns:
        调整后的颜色
    """
    h, s, l = hex_to_hsl(base_color)
    bg_luminance = get_luminance(background)
    need_darker = bg_luminance > 0.5
    
    # 尝试调整亮度
    for adjustment in range(0, 100, 5):
        new_l = l - adjustment if need_darker else l + adjustment
        new_l = max(0, min(100, new_l))
        new_color = hsl_to_hex(h, s, new_l)
        
        if get_contrast_ratio(new_color, background) >= target_ratio:
            return new_color
    
    # 如果亮度调整不够，尝试调整饱和度
    for sat_adj in range(0, 100, 10):
        new_s = s - sat_adj if need_darker else s + sat_adj
        new_s = max(0, min(100, new_s))
        new_color = hsl_to_hex(h, new_s, l)
        
        if get_contrast_ratio(new_color, background) >= target_ratio:
            return new_color
    
    # 如果都不行，返回纯黑或纯白
    return '#000000' if need_darker else '#FFFFFF'


# ============ 颜色名称 ============

# 常见颜色名称映射
COLOR_NAMES = {
    '#FF0000': 'Red',
    '#00FF00': 'Lime',
    '#0000FF': 'Blue',
    '#FFFF00': 'Yellow',
    '#00FFFF': 'Cyan',
    '#FF00FF': 'Magenta',
    '#FFFFFF': 'White',
    '#000000': 'Black',
    '#808080': 'Gray',
    '#C0C0C0': 'Silver',
    '#800000': 'Maroon',
    '#008000': 'Green',
    '#000080': 'Navy',
    '#808000': 'Olive',
    '#800080': 'Purple',
    '#008080': 'Teal',
    '#FFA500': 'Orange',
    '#FFC0CB': 'Pink',
    '#A52A2A': 'Brown',
    '#D2691E': 'Chocolate',
    '#FFD700': 'Gold',
    '#4B0082': 'Indigo',
    '#F0E68C': 'Khaki',
    '#E6E6FA': 'Lavender',
    '#FF00FF': 'Fuchsia',
    '#ADD8E6': 'LightBlue',
    '#90EE90': 'LightGreen',
    '#FFB6C1': 'LightPink',
    '#FFA07A': 'LightSalmon',
    '#20B2AA': 'LightSeaGreen',
    '#87CEEB': 'SkyBlue',
    '#778899': 'LightSlateGray',
    '#B0C4DE': 'LightSteelBlue',
    '#FFFFE0': 'LightYellow',
    '#32CD32': 'LimeGreen',
    '#FAFAD2': 'LightGoldenrodYellow',
    '#D3D3D3': 'LightGray',
    '#FF69B4': 'HotPink',
    '#CD5C5C': 'IndianRed',
    '#4169E1': 'RoyalBlue',
    '#8B4513': 'SaddleBrown',
    '#FA8072': 'Salmon',
    '#F4A460': 'SandyBrown',
    '#2E8B57': 'SeaGreen',
    '#6A5ACD': 'SlateBlue',
    '#708090': 'SlateGray',
    '#D2B48C': 'Tan',
    '#00CED1': 'DarkTurquoise',
    '#9400D3': 'DarkViolet',
    '#FF1493': 'DeepPink',
    '#00BFFF': 'DeepSkyBlue',
    '#696969': 'DimGray',
    '#1E90FF': 'DodgerBlue',
    '#B22222': 'FireBrick',
    '#228B22': 'ForestGreen',
    '#DCDCDC': 'Gainsboro',
    '#F8F8FF': 'GhostWhite',
    '#FFDAB9': 'PeachPuff',
    '#FFE4B5': 'Moccasin',
    '#FFE4C4': 'Bisque',
    '#FFEBCD': 'BlanchedAlmond',
    '#FFE4E1': 'MistyRose',
    '#FFEFD5': 'PapayaWhip',
    '#FFF0F5': 'LavenderBlush',
    '#FFF5EE': 'Seashell',
    '#FFF8DC': 'Cornsilk',
    '#FFFACD': 'LemonChiffon',
    '#FDF5E6': 'OldLace',
    '#FAF0E6': 'Linen',
    '#F5F5DC': 'Beige',
    '#F5F5F5': 'WhiteSmoke',
    '#F5FFFA': 'MintCream',
    '#F0FFF0': 'Honeydew',
    '#F0FFFF': 'Azure',
    '#E0FFFF': 'LightCyan',
    '#7FFFD4': 'Aquamarine',
}


def get_color_name(hex_color: str) -> str:
    """
    获取颜色的名称（如果存在）。
    
    Args:
        hex_color: 十六进制颜色
    
    Returns:
        颜色名称或十六进制值
    """
    hex_upper = hex_color.upper()
    if hex_upper in COLOR_NAMES:
        return COLOR_NAMES[hex_upper]
    
    # 尝试不带 # 查找
    hex_no_hash = hex_upper.lstrip('#')
    for key, name in COLOR_NAMES.items():
        if key.lstrip('#') == hex_no_hash:
            return name
    
    return hex_color


# ============ 工具函数 ============

def blend_colors(color1: str, color2: str, ratio: float = 0.5) -> str:
    """
    混合两个颜色。
    
    Args:
        color1: 第一个颜色（十六进制）
        color2: 第二个颜色（十六进制）
        ratio: 混合比例 (0-1)，0 为全 color1，1 为全 color2
    
    Returns:
        混合后的颜色
    """
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    
    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)
    
    return rgb_to_hex(r, g, b)


def is_light_color(hex_color: str, threshold: float = 50) -> bool:
    """
    判断颜色是否为浅色。
    
    Args:
        hex_color: 十六进制颜色
        threshold: 亮度阈值 (0-100)
    
    Returns:
        是否为浅色
    """
    _, _, l = hex_to_hsl(hex_color)
    return l > threshold


def is_warm_color(hex_color: str) -> bool:
    """
    判断颜色是否为暖色。
    
    Args:
        hex_color: 十六进制颜色
    
    Returns:
        是否为暖色
    """
    h, _, _ = hex_to_hsl(hex_color)
    # 暖色区域：0-60 (红橙黄) 和 300-360 (红紫)
    return h <= 60 or h >= 300


def color_temperature(hex_color: str) -> str:
    """
    获取颜色的温度描述。
    
    Args:
        hex_color: 十六进制颜色
    
    Returns:
        温度描述 ('warm', 'cool', 'neutral')
    """
    h, s, _ = hex_to_hsl(hex_color)
    
    if s < 10:
        return 'neutral'
    
    if is_warm_color(hex_color):
        return 'warm'
    return 'cool'


def get_palette_harmony_type(palette: List[str]) -> str:
    """
    分析调色板的和谐类型。
    
    Args:
        palette: 颜色列表
    
    Returns:
        和谐类型描述
    """
    if len(palette) < 2:
        return 'single'
    
    hues = [hex_to_hsl(c)[0] for c in palette]
    hues.sort()
    
    # 计算相邻颜色的色相差异
    diffs = []
    for i in range(len(hues)):
        diff = hues[(i + 1) % len(hues)] - hues[i]
        if diff < 0:
            diff += 360
        diffs.append(diff)
    
    avg_diff = sum(diffs) / len(diffs)
    
    # 判断和谐类型
    if len(palette) == 2:
        return 'complementary' if 160 <= avg_diff <= 200 else 'custom'
    
    if len(palette) == 3:
        if all(abs(d - 30) < 15 for d in diffs):
            return 'analogous'
        if all(abs(d - 120) < 15 for d in diffs):
            return 'triadic'
        return 'custom'
    
    if len(palette) == 4:
        if all(abs(d - 90) < 15 for d in diffs):
            return 'tetradic'
    
    if len(palette) == 5:
        if all(abs(d - 72) < 10 for d in diffs):
            return 'pentadic'
    
    return 'custom'


# ============ 完整调色板生成器 ============

class ColorPalette:
    """
    颜色调色板类，提供完整的调色板生成和管理功能。
    """
    
    def __init__(self, colors: Optional[List[str]] = None, name: str = 'Custom'):
        """
        初始化调色板。
        
        Args:
            colors: 颜色列表
            name: 调色板名称
        """
        self.colors = colors or []
        self.name = name
    
    @classmethod
    def from_base_color(cls, base_color: str, harmony_type: str = 'triadic', 
                        name: str = 'Harmony') -> 'ColorPalette':
        """
        从基础颜色生成和谐调色板。
        
        Args:
            base_color: 基础颜色
            harmony_type: 和谐类型
            name: 调色板名称
        
        Returns:
            ColorPalette 实例
        """
        generators = {
            'complementary': generate_complementary_palette,
            'analogous': generate_analogous_palette,
            'triadic': generate_triadic_palette,
            'split_complementary': generate_split_complementary_palette,
            'tetradic': generate_tetradic_palette,
            'pentadic': generate_pentadic_palette,
            'square': generate_square_palette,
            'monochromatic': generate_monochromatic_palette,
        }
        
        generator = generators.get(harmony_type, generate_triadic_palette)
        colors = generator(base_color)
        
        return cls(colors, name)
    
    @classmethod
    def random(cls, count: int = 5, name: str = 'Random') -> 'ColorPalette':
        """生成随机调色板。"""
        return cls(random_palette(count), name)
    
    @classmethod
    def gradient(cls, start: str, end: str, steps: int = 10, 
                 name: str = 'Gradient') -> 'ColorPalette':
        """生成渐变调色板。"""
        return cls(generate_gradient(start, end, steps), name)
    
    def add_color(self, color: str) -> 'ColorPalette':
        """添加颜色。"""
        self.colors.append(color)
        return self
    
    def remove_color(self, index: int) -> 'ColorPalette':
        """移除颜色。"""
        if 0 <= index < len(self.colors):
            self.colors.pop(index)
        return self
    
    def get_color(self, index: int) -> Optional[str]:
        """获取指定索引的颜色。"""
        if 0 <= index < len(self.colors):
            return self.colors[index]
        return None
    
    def __len__(self) -> int:
        return len(self.colors)
    
    def __iter__(self):
        return iter(self.colors)
    
    def __getitem__(self, index: int) -> str:
        return self.colors[index]
    
    def to_css(self, prefix: str = 'color') -> str:
        """导出为 CSS 变量。"""
        return palette_to_css_variables(self.colors, prefix)
    
    def to_scss(self, prefix: str = 'color') -> str:
        """导出为 SCSS 变量。"""
        return palette_to_scss_variables(self.colors, prefix)
    
    def to_json(self, include_rgb: bool = False) -> Dict:
        """导出为 JSON。"""
        return palette_to_json(self.colors, self.name, include_rgb)
    
    def to_tailwind(self) -> str:
        """导出为 Tailwind 配置。"""
        return palette_to_tailwind_config(self.colors, self.name.lower())
    
    def with_shades(self, steps: int = 3) -> 'ColorPalette':
        """为每个颜色添加阴影。"""
        new_colors = []
        for color in self.colors:
            new_colors.append(color)
            new_colors.extend(generate_shades(color, steps))
        return ColorPalette(new_colors, f'{self.name}_with_shades')
    
    def with_tints(self, steps: int = 3) -> 'ColorPalette':
        """为每个颜色添加着色。"""
        new_colors = []
        for color in self.colors:
            new_colors.append(color)
            new_colors.extend(generate_tints(color, steps))
        return ColorPalette(new_colors, f'{self.name}_with_tints')
    
    def __repr__(self) -> str:
        return f"ColorPalette(name='{self.name}', colors={self.colors})"


# 便捷函数
def create_palette(base_color: str, harmony_type: str = 'triadic') -> ColorPalette:
    """
    创建和谐调色板的便捷函数。
    
    Args:
        base_color: 基础颜色
        harmony_type: 和谐类型
    
    Returns:
        ColorPalette 实例
    """
    return ColorPalette.from_base_color(base_color, harmony_type)