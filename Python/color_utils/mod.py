"""
Color Utilities - 颜色工具

提供完整的颜色处理功能，包括：
- 多格式颜色解析 (HEX, RGB, HSL, HSV, CMYK)
- 格式互转 (HEX ↔ RGB ↔ HSL ↔ HSV ↔ CMYK)
- 颜色混合与渐变
- 对比度计算 (WCAG 标准)
- 互补色、类似色、三角色等配色方案
- 颜色亮度判断与调整
- 随机颜色生成
- 颜色名称查找

零外部依赖，纯 Python 实现。
"""

from typing import Tuple, List, Optional, Union, Dict
from dataclasses import dataclass
import random
import re
import math


@dataclass
class Color:
    """
    颜色对象
    
    内部使用 RGB 存储颜色，提供多种格式转换
    """
    r: int  # 0-255
    g: int  # 0-255
    b: int  # 0-255
    a: float = 1.0  # 0.0-1.0 alpha 通道
    
    def __post_init__(self):
        """验证颜色值范围"""
        self.r = max(0, min(255, int(self.r)))
        self.g = max(0, min(255, int(self.g)))
        self.b = max(0, min(255, int(self.b)))
        self.a = max(0.0, min(1.0, float(self.a)))
    
    @property
    def hex(self) -> str:
        """返回 HEX 格式 (#RRGGBB)"""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    @property
    def hex_alpha(self) -> str:
        """返回带 Alpha 的 HEX 格式 (#RRGGBBAA)"""
        alpha_hex = int(self.a * 255)
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}{alpha_hex:02x}"
    
    @property
    def rgb(self) -> Tuple[int, int, int]:
        """返回 RGB 元组"""
        return (self.r, self.g, self.b)
    
    @property
    def rgba(self) -> Tuple[int, int, int, float]:
        """返回 RGBA 元组"""
        return (self.r, self.g, self.b, self.a)
    
    @property
    def hsl(self) -> Tuple[int, int, int]:
        """返回 HSL 元组 (H: 0-360, S/L: 0-100%)"""
        return rgb_to_hsl(self.r, self.g, self.b)
    
    @property
    def hsv(self) -> Tuple[int, int, int]:
        """返回 HSV 元组 (H: 0-360, S/V: 0-100%)"""
        return rgb_to_hsv(self.r, self.g, self.b)
    
    @property
    def cmyk(self) -> Tuple[int, int, int, int]:
        """返回 CMYK 元组 (0-100%)"""
        return rgb_to_cmyk(self.r, self.g, self.b)
    
    @property
    def luminance(self) -> float:
        """返回相对亮度 (0.0-1.0)，WCAG 标准"""
        return calculate_luminance(self.r, self.g, self.b)
    
    @property
    def is_light(self) -> bool:
        """判断是否为浅色"""
        return self.luminance > 0.5
    
    @property
    def is_dark(self) -> bool:
        """判断是否为深色"""
        return self.luminance <= 0.5
    
    def contrast_ratio(self, other: 'Color') -> float:
        """计算与另一个颜色的对比度"""
        return calculate_contrast_ratio(self, other)
    
    def mix(self, other: 'Color', ratio: float = 0.5) -> 'Color':
        """与另一个颜色混合"""
        return mix_colors(self, other, ratio)
    
    def complement(self) -> 'Color':
        """获取互补色"""
        return get_complement_color(self)
    
    def lighter(self, amount: float = 0.1) -> 'Color':
        """变亮"""
        return adjust_lightness(self, amount)
    
    def darker(self, amount: float = 0.1) -> 'Color':
        """变暗"""
        return adjust_lightness(self, -amount)
    
    def saturate(self, amount: float = 0.1) -> 'Color':
        """增加饱和度"""
        return adjust_saturation(self, amount)
    
    def desaturate(self, amount: float = 0.1) -> 'Color':
        """降低饱和度"""
        return adjust_saturation(self, -amount)
    
    def rotate_hue(self, degrees: int) -> 'Color':
        """旋转色相"""
        h, s, l = self.hsl
        h = (h + degrees) % 360
        return Color.from_hsl(h, s, l)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'hex': self.hex,
            'rgb': self.rgb,
            'rgba': self.rgba,
            'hsl': self.hsl,
            'hsv': self.hsv,
            'cmyk': self.cmyk,
            'luminance': round(self.luminance, 4),
            'is_light': self.is_light,
            'is_dark': self.is_dark,
        }
    
    @classmethod
    def from_hex(cls, hex_color: str) -> 'Color':
        """从 HEX 字符串创建"""
        r, g, b, a = parse_hex(hex_color)
        return cls(r, g, b, a)
    
    @classmethod
    def from_rgb(cls, r: int, g: int, b: int, a: float = 1.0) -> 'Color':
        """从 RGB 值创建"""
        return cls(r, g, b, a)
    
    @classmethod
    def from_hsl(cls, h: int, s: int, l: int, a: float = 1.0) -> 'Color':
        """从 HSL 值创建"""
        r, g, b = hsl_to_rgb(h, s, l)
        return cls(r, g, b, a)
    
    @classmethod
    def from_hsv(cls, h: int, s: int, v: int, a: float = 1.0) -> 'Color':
        """从 HSV 值创建"""
        r, g, b = hsv_to_rgb(h, s, v)
        return cls(r, g, b, a)
    
    @classmethod
    def from_cmyk(cls, c: int, m: int, y: int, k: int, a: float = 1.0) -> 'Color':
        """从 CMYK 值创建"""
        r, g, b = cmyk_to_rgb(c, m, y, k)
        return cls(r, g, b, a)
    
    def __repr__(self) -> str:
        return f"Color({self.hex})"


# ============================================================
# 颜色解析
# ============================================================

def parse_hex(hex_color: str) -> Tuple[int, int, int, float]:
    """
    解析 HEX 颜色字符串
    
    支持格式：
    - #RGB
    - #RGBA
    - #RRGGBB
    - #RRGGBBAA
    - RGB
    - RRGGBB
    - RRGGBBAA
    
    Args:
        hex_color: HEX 颜色字符串
        
    Returns:
        (r, g, b, a) 元组
        
    Example:
        >>> parse_hex('#FF0000')
        (255, 0, 0, 1.0)
        >>> parse_hex('#F00')
        (255, 0, 0, 1.0)
        >>> parse_hex('#FF000080')
        (255, 0, 0, 0.5)
    """
    # 移除 # 前缀
    hex_color = hex_color.strip('#').strip()
    
    # 根据长度解析
    length = len(hex_color)
    
    if length == 3:
        # #RGB -> #RRGGBB
        r = int(hex_color[0] * 2, 16)
        g = int(hex_color[1] * 2, 16)
        b = int(hex_color[2] * 2, 16)
        a = 1.0
    elif length == 4:
        # #RGBA
        r = int(hex_color[0] * 2, 16)
        g = int(hex_color[1] * 2, 16)
        b = int(hex_color[2] * 2, 16)
        a = int(hex_color[3] * 2, 16) / 255
    elif length == 6:
        # #RRGGBB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        a = 1.0
    elif length == 8:
        # #RRGGBBAA
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        a = int(hex_color[6:8], 16) / 255
    else:
        raise ValueError(f"Invalid HEX color: #{hex_color}")
    
    return (r, g, b, a)


def parse_color(color: Union[str, Tuple, 'Color']) -> Color:
    """
    通用颜色解析
    
    支持多种输入格式：
    - HEX 字符串: "#FF0000", "FF0000", "#F00"
    - RGB 元组: (255, 0, 0), (255, 0, 0, 0.5)
    - HSL 元组: 需要指定 format='hsl'
    - Color 对象: 直接返回
    
    Args:
        color: 颜色值
        
    Returns:
        Color 对象
        
    Example:
        >>> parse_color('#FF0000')
        Color(#ff0000)
        >>> parse_color((255, 0, 0))
        Color(#ff0000)
    """
    if isinstance(color, Color):
        return color
    
    if isinstance(color, str):
        return Color.from_hex(color)
    
    if isinstance(color, (tuple, list)):
        if len(color) == 3:
            return Color(color[0], color[1], color[2])
        elif len(color) >= 4:
            return Color(color[0], color[1], color[2], color[3])
    
    raise ValueError(f"Cannot parse color: {color}")


# ============================================================
# RGB ↔ HSL 转换
# ============================================================

def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    RGB 转 HSL
    
    Args:
        r, g, b: RGB 值 (0-255)
        
    Returns:
        (h, s, l) 元组 (h: 0-360, s/l: 0-100%)
        
    Example:
        >>> rgb_to_hsl(255, 0, 0)
        (0, 100, 50)
        >>> rgb_to_hsl(0, 255, 0)
        (120, 100, 50)
    """
    r_norm = r / 255
    g_norm = g / 255
    b_norm = b / 255
    
    max_val = max(r_norm, g_norm, b_norm)
    min_val = min(r_norm, g_norm, b_norm)
    delta = max_val - min_val
    
    # Lightness
    l = (max_val + min_val) / 2
    
    # Saturation
    if delta == 0:
        s = 0
        h = 0  # 灰色时色相未定义
    else:
        s = delta / (1 - abs(2 * l - 1))
        
        # Hue
        if max_val == r_norm:
            h = ((g_norm - b_norm) / delta) % 6
        elif max_val == g_norm:
            h = (b_norm - r_norm) / delta + 2
        else:
            h = (r_norm - g_norm) / delta + 4
        
        h *= 60
        if h < 0:
            h += 360
    
    return (int(round(h)), int(round(s * 100)), int(round(l * 100)))


def hsl_to_rgb(h: int, s: int, l: int) -> Tuple[int, int, int]:
    """
    HSL 转 RGB
    
    Args:
        h: 色相 (0-360)
        s: 饱和度 (0-100%)
        l: 明度 (0-100%)
        
    Returns:
        (r, g, b) 元组 (0-255)
        
    Example:
        >>> hsl_to_rgb(0, 100, 50)
        (255, 0, 0)
        >>> hsl_to_rgb(120, 100, 50)
        (0, 255, 0)
    """
    s_norm = s / 100
    l_norm = l / 100
    
    if s_norm == 0:
        # 灰色
        v = int(round(l_norm * 255))
        return (v, v, v)
    
    def hue_to_rgb(p: float, q: float, t: float) -> float:
        """色相转 RGB 分量"""
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
    
    q = l_norm * (1 + s_norm) if l_norm < 0.5 else l_norm + s_norm - l_norm * s_norm
    p = 2 * l_norm - q
    
    h_norm = h / 360
    
    r = hue_to_rgb(p, q, h_norm + 1/3)
    g = hue_to_rgb(p, q, h_norm)
    b = hue_to_rgb(p, q, h_norm - 1/3)
    
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


# ============================================================
# RGB ↔ HSV 转换
# ============================================================

def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    RGB 转 HSV
    
    Args:
        r, g, b: RGB 值 (0-255)
        
    Returns:
        (h, s, v) 元组 (h: 0-360, s/v: 0-100%)
        
    Example:
        >>> rgb_to_hsv(255, 0, 0)
        (0, 100, 100)
        >>> rgb_to_hsv(255, 255, 0)
        (60, 100, 100)
    """
    r_norm = r / 255
    g_norm = g / 255
    b_norm = b / 255
    
    max_val = max(r_norm, g_norm, b_norm)
    min_val = min(r_norm, g_norm, b_norm)
    delta = max_val - min_val
    
    # Value
    v = max_val
    
    # Saturation
    if max_val == 0:
        s = 0
        h = 0
    else:
        s = delta / max_val
        
        # Hue
        if delta == 0:
            h = 0
        elif max_val == r_norm:
            h = ((g_norm - b_norm) / delta) % 6
        elif max_val == g_norm:
            h = (b_norm - r_norm) / delta + 2
        else:
            h = (r_norm - g_norm) / delta + 4
        
        h *= 60
        if h < 0:
            h += 360
    
    return (int(round(h)), int(round(s * 100)), int(round(v * 100)))


def hsv_to_rgb(h: int, s: int, v: int) -> Tuple[int, int, int]:
    """
    HSV 转 RGB
    
    Args:
        h: 色相 (0-360)
        s: 饱和度 (0-100%)
        v: 明度 (0-100%)
        
    Returns:
        (r, g, b) 元组 (0-255)
        
    Example:
        >>> hsv_to_rgb(0, 100, 100)
        (255, 0, 0)
        >>> hsv_to_rgb(60, 100, 100)
        (255, 255, 0)
    """
    s_norm = s / 100
    v_norm = v / 100
    
    if s_norm == 0:
        # 灰色
        val = int(round(v_norm * 255))
        return (val, val, val)
    
    h_norm = h / 60
    i = int(h_norm)
    f = h_norm - i
    p = v_norm * (1 - s_norm)
    q = v_norm * (1 - s_norm * f)
    t = v_norm * (1 - s_norm * (1 - f))
    
    if i == 0:
        r, g, b = v_norm, t, p
    elif i == 1:
        r, g, b = q, v_norm, p
    elif i == 2:
        r, g, b = p, v_norm, t
    elif i == 3:
        r, g, b = p, q, v_norm
    elif i == 4:
        r, g, b = t, p, v_norm
    else:
        r, g, b = v_norm, p, q
    
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


# ============================================================
# RGB ↔ CMYK 转换
# ============================================================

def rgb_to_cmyk(r: int, g: int, b: int) -> Tuple[int, int, int, int]:
    """
    RGB 转 CMYK
    
    Args:
        r, g, b: RGB 值 (0-255)
        
    Returns:
        (c, m, y, k) 元组 (0-100%)
        
    Example:
        >>> rgb_to_cmyk(255, 0, 0)
        (0, 100, 100, 0)
        >>> rgb_to_cmyk(0, 0, 0)
        (0, 0, 0, 100)
        >>> rgb_to_cmyk(255, 255, 255)
        (0, 0, 0, 0)
    """
    r_norm = r / 255
    g_norm = g / 255
    b_norm = b / 255
    
    # Black key
    k = 1 - max(r_norm, g_norm, b_norm)
    
    if k == 1:
        # 纯黑
        return (0, 0, 0, 100)
    
    c = (1 - r_norm - k) / (1 - k)
    m = (1 - g_norm - k) / (1 - k)
    y = (1 - b_norm - k) / (1 - k)
    
    return (
        int(round(c * 100)),
        int(round(m * 100)),
        int(round(y * 100)),
        int(round(k * 100))
    )


def cmyk_to_rgb(c: int, m: int, y: int, k: int) -> Tuple[int, int, int]:
    """
    CMYK 转 RGB
    
    Args:
        c, m, y, k: CMYK 值 (0-100%)
        
    Returns:
        (r, g, b) 元组 (0-255)
        
    Example:
        >>> cmyk_to_rgb(0, 100, 100, 0)
        (255, 0, 0)
        >>> cmyk_to_rgb(0, 0, 0, 100)
        (0, 0, 0)
    """
    c_norm = c / 100
    m_norm = m / 100
    y_norm = y / 100
    k_norm = k / 100
    
    r = 255 * (1 - c_norm) * (1 - k_norm)
    g = 255 * (1 - m_norm) * (1 - k_norm)
    b = 255 * (1 - y_norm) * (1 - k_norm)
    
    return (int(round(r)), int(round(g)), int(round(b)))


# ============================================================
# 颜色混合与调整
# ============================================================

def mix_colors(color1: Color, color2: Color, ratio: float = 0.5) -> Color:
    """
    混合两个颜色
    
    Args:
        color1: 第一个颜色
        color2: 第二个颜色
        ratio: 混合比例 (0.0 = 100% color1, 1.0 = 100% color2)
        
    Returns:
        混合后的颜色
        
    Example:
        >>> red = Color.from_hex('#FF0000')
        >>> blue = Color.from_hex('#0000FF')
        >>> mix_colors(red, blue, 0.5)  # 紫色
        Color(#800080)
    """
    r = int(color1.r * (1 - ratio) + color2.r * ratio)
    g = int(color1.g * (1 - ratio) + color2.g * ratio)
    b = int(color1.b * (1 - ratio) + color2.b * ratio)
    a = color1.a * (1 - ratio) + color2.a * ratio
    
    return Color(r, g, b, a)


def adjust_lightness(color: Color, amount: float) -> Color:
    """
    调整明度
    
    Args:
        color: 颜色对象
        amount: 调整量 (-1.0 到 1.0)
        
    Returns:
        调整后的颜色
        
    Example:
        >>> color = Color.from_hex('#FF0000')
        >>> adjust_lightness(color, 0.2)  # 变亮 20%
        Color(#ff6666)
        >>> adjust_lightness(color, -0.2)  # 变暗 20%
        Color(#990000)
    """
    h, s, l = color.hsl
    l = max(0, min(100, l + amount * 100))
    return Color.from_hsl(h, s, l, color.a)


def adjust_saturation(color: Color, amount: float) -> Color:
    """
    调整饱和度
    
    Args:
        color: 颜色对象
        amount: 调整量 (-1.0 到 1.0)
        
    Returns:
        调整后的颜色
        
    Example:
        >>> color = Color.from_hex('#FF0000')
        >>> adjust_saturation(color, -1.0)  # 完全去饱和
        Color(#808080)
    """
    h, s, l = color.hsl
    s = max(0, min(100, s + amount * 100))
    return Color.from_hsl(h, s, l, color.a)


# ============================================================
# 对比度计算 (WCAG 标准)
# ============================================================

def calculate_luminance(r: int, g: int, b: int) -> float:
    """
    计算相对亮度 (WCAG 标准)
    
    Args:
        r, g, b: RGB 值 (0-255)
        
    Returns:
        相对亮度 (0.0-1.0)
        
    Example:
        >>> calculate_luminance(255, 255, 255)  # 白色
        1.0
        >>> calculate_luminance(0, 0, 0)  # 黑色
        0.0
    """
    def linearize(value: int) -> float:
        """sRGB -> linear RGB"""
        v = value / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    
    lr = linearize(r)
    lg = linearize(g)
    lb = linearize(b)
    
    return 0.2126 * lr + 0.7152 * lg + 0.0722 * lb


def calculate_contrast_ratio(color1: Color, color2: Color) -> float:
    """
    计算两个颜色的对比度 (WCAG 标准)
    
    Args:
        color1: 第一个颜色
        color2: 第二个颜色
        
    Returns:
        对比度 (1:1 到 21:1)
        
    Example:
        >>> black = Color.from_hex('#000000')
        >>> white = Color.from_hex('#FFFFFF')
        >>> calculate_contrast_ratio(black, white)
        21.0
    """
    l1 = color1.luminance
    l2 = color2.luminance
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


def wcag_compliance(color1: Color, color2: Color) -> Dict:
    """
    检查 WCAG 对比度合规性
    
    Args:
        color1: 第一个颜色
        color2: 第二个颜色
        
    Returns:
        包含对比度和合规性级别的字典
        
    Example:
        >>> wcag_compliance(Color.from_hex('#000'), Color.from_hex('#FFF'))
        {
            'contrast_ratio': 21.0,
            'aa_normal': True,
            'aa_large': True,
            'aaa_normal': True,
            'aaa_large': True
        }
    """
    ratio = calculate_contrast_ratio(color1, color2)
    
    return {
        'contrast_ratio': round(ratio, 2),
        'aa_normal': ratio >= 4.5,     # AA 级别普通文本
        'aa_large': ratio >= 3.0,      # AA 级别大文本
        'aaa_normal': ratio >= 7.0,    # AAA 级别普通文本
        'aaa_large': ratio >= 4.5,     # AAA 级别大文本
    }


# ============================================================
# 配色方案
# ============================================================

def get_complement_color(color: Color) -> Color:
    """
    获取互补色 (色轮上 180° 对面的颜色)
    
    Args:
        color: 输入颜色
        
    Returns:
        互补色
        
    Example:
        >>> get_complement_color(Color.from_hex('#FF0000'))  # 红色 -> 青色
        Color(#00ffff)
    """
    h, s, l = color.hsl
    return Color.from_hsl((h + 180) % 360, s, l, color.a)


def get_analogous_colors(color: Color, angle: int = 30) -> List[Color]:
    """
    获取类似色 (色轮上相邻的颜色)
    
    Args:
        color: 输入颜色
        angle: 角度间隔 (默认 30°)
        
    Returns:
        [原色, 左侧类似色, 右侧类似色]
        
    Example:
        >>> red = Color.from_hex('#FF0000')
        >>> get_analogous_colors(red)  # 红, 橙红, 品红
    """
    h, s, l = color.hsl
    return [
        color,
        Color.from_hsl((h - angle) % 360, s, l, color.a),
        Color.from_hsl((h + angle) % 360, s, l, color.a),
    ]


def get_triadic_colors(color: Color) -> List[Color]:
    """
    获取三角色 (色轮上等距的三个颜色)
    
    Args:
        color: 输入颜色
        
    Returns:
        [原色, 120° 色相, 240° 色相]
        
    Example:
        >>> red = Color.from_hex('#FF0000')
        >>> get_triadic_colors(red)  # 红, 绿, 蓝
    """
    h, s, l = color.hsl
    return [
        color,
        Color.from_hsl((h + 120) % 360, s, l, color.a),
        Color.from_hsl((h + 240) % 360, s, l, color.a),
    ]


def get_split_complementary_colors(color: Color) -> List[Color]:
    """
    获取分裂互补色
    
    Args:
        color: 输入颜色
        
    Returns:
        [原色, 150° 色相, 210° 色相]
        
    Example:
        >>> red = Color.from_hex('#FF0000')
        >>> get_split_complementary_colors(red)
    """
    h, s, l = color.hsl
    return [
        color,
        Color.from_hsl((h + 150) % 360, s, l, color.a),
        Color.from_hsl((h + 210) % 360, s, l, color.a),
    ]


def get_tetradic_colors(color: Color) -> List[Color]:
    """
    获取四角色 (矩形配色方案)
    
    Args:
        color: 输入颜色
        
    Returns:
        [原色, 90°, 180°, 270°]
        
    Example:
        >>> red = Color.from_hex('#FF0000')
        >>> get_tetradic_colors(red)
    """
    h, s, l = color.hsl
    return [
        color,
        Color.from_hsl((h + 90) % 360, s, l, color.a),
        Color.from_hsl((h + 180) % 360, s, l, color.a),
        Color.from_hsl((h + 270) % 360, s, l, color.a),
    ]


def get_monochromatic_colors(color: Color, steps: int = 5) -> List[Color]:
    """
    获取单色配色方案 (同一色相的不同明度)
    
    Args:
        color: 输入颜色
        steps: 步数
        
    Returns:
        颜色列表
        
    Example:
        >>> red = Color.from_hex('#FF0000')
        >>> get_monochromatic_colors(red, 5)  # 从暗红到亮红
    """
    h, s, l = color.hsl
    colors = []
    
    for i in range(steps):
        new_l = (i / (steps - 1)) * 100
        colors.append(Color.from_hsl(h, s, new_l, color.a))
    
    return colors


def get_shades(color: Color, steps: int = 5) -> List[Color]:
    """
    获取色阶 (混合黑色的变体)
    
    Args:
        color: 输入颜色
        steps: 步数
        
    Returns:
        颜色列表
        
    Example:
        >>> red = Color.from_hex('#FF0000')
        >>> get_shades(red, 5)  # 红色到黑色的渐变
    """
    black = Color(0, 0, 0)
    colors = []
    
    for i in range(steps):
        ratio = i / (steps - 1)
        colors.append(mix_colors(color, black, ratio))
    
    return colors


def get_tints(color: Color, steps: int = 5) -> List[Color]:
    """
    获取色调 (混合白色的变体)
    
    Args:
        color: 输入颜色
        steps: 步数
        
    Returns:
        颜色列表
        
    Example:
        >>> red = Color.from_hex('#FF0000')
        >>> get_tints(red, 5)  # 红色到白色的渐变
    """
    white = Color(255, 255, 255)
    colors = []
    
    for i in range(steps):
        ratio = i / (steps - 1)
        colors.append(mix_colors(color, white, ratio))
    
    return colors


def get_tones(color: Color, steps: int = 5) -> List[Color]:
    """
    获取色调 (混合灰色的变体)
    
    Args:
        color: 输入颜色
        steps: 步数
        
    Returns:
        颜色列表
        
    Example:
        >>> red = Color.from_hex('#FF0000')
        >>> get_tones(red, 5)  # 红色到灰色的渐变
    """
    gray = Color(128, 128, 128)
    colors = []
    
    for i in range(steps):
        ratio = i / (steps - 1)
        colors.append(mix_colors(color, gray, ratio))
    
    return colors


# ============================================================
# 渐变生成
# ============================================================

def create_gradient(start: Color, end: Color, steps: int) -> List[Color]:
    """
    创建颜色渐变
    
    Args:
        start: 起始颜色
        end: 结束颜色
        steps: 步数
        
    Returns:
        颜色列表
        
    Example:
        >>> red = Color.from_hex('#FF0000')
        >>> blue = Color.from_hex('#0000FF')
        >>> create_gradient(red, blue, 5)  # 红到蓝的渐变
    """
    if steps < 2:
        return [start]
    
    colors = []
    for i in range(steps):
        ratio = i / (steps - 1)
        colors.append(mix_colors(start, end, ratio))
    
    return colors


def create_multi_gradient(colors: List[Color], total_steps: int) -> List[Color]:
    """
    创建多色渐变
    
    Args:
        colors: 颜色列表
        total_steps: 总步数
        
    Returns:
        渐变颜色列表
        
    Example:
        >>> red = Color.from_hex('#FF0000')
        >>> green = Color.from_hex('#00FF00')
        >>> blue = Color.from_hex('#0000FF')
        >>> create_multi_gradient([red, green, blue], 9)  # 红->绿->蓝
    """
    if len(colors) < 2:
        return colors * total_steps if colors else []
    
    if total_steps < 2:
        return [colors[0]]
    
    # 计算每段步数
    segments = len(colors) - 1
    # 每段包含的颜色数（不包括起始颜色）
    steps_per_segment = (total_steps - 1) // segments
    extra = (total_steps - 1) % segments
    
    gradient = [colors[0]]
    
    for i in range(segments):
        # 每段生成的颜色数（包括起始和结束颜色）
        segment_steps = steps_per_segment + 1
        if i < extra:
            segment_steps += 1
        
        # 生成渐变（包括起始颜色），去掉起始颜色避免重复
        segment = create_gradient(colors[i], colors[i + 1], segment_steps)[1:]
        gradient.extend(segment)
    
    return gradient


# ============================================================
# 随机颜色生成
# ============================================================

def random_color(
    min_brightness: int = 0,
    max_brightness: int = 255,
    min_saturation: int = 0,
    max_saturation: int = 100,
    hue_range: Optional[Tuple[int, int]] = None,
) -> Color:
    """
    生成随机颜色
    
    Args:
        min_brightness: 最小亮度 (0-255)
        max_brightness: 最大亮度 (0-255)
        min_saturation: 最小饱和度 (0-100)
        max_saturation: 最大饱和度 (0-100)
        hue_range: 色相范围 (可选)
        
    Returns:
        随机颜色
        
    Example:
        >>> random_color()  # 完全随机
        >>> random_color(hue_range=(0, 60))  # 随机暖色
    """
    if hue_range:
        h = random.randint(hue_range[0], hue_range[1])
    else:
        h = random.randint(0, 360)
    
    s = random.randint(min_saturation, max_saturation)
    
    # 根据亮度范围反推明度
    min_l = min_brightness / 255 * 100
    max_l = max_brightness / 255 * 100
    l = random.randint(int(min_l), int(max_l))
    
    return Color.from_hsl(h, s, l)


def random_pastel_color() -> Color:
    """生成随机柔和色"""
    return random_color(min_saturation=40, max_saturation=80, min_brightness=200)


def random_vibrant_color() -> Color:
    """生成随机鲜艳色"""
    return random_color(min_saturation=80, max_saturation=100, min_brightness=150)


def random_dark_color() -> Color:
    """生成随机深色"""
    return random_color(max_brightness=100, min_saturation=50)


def random_light_color() -> Color:
    """生成随机浅色"""
    return random_color(min_brightness=200)


# ============================================================
# 颜色名称
# ============================================================

# 常用颜色名称映射
CSS_COLORS = {
    'black': '#000000',
    'white': '#FFFFFF',
    'red': '#FF0000',
    'green': '#008000',
    'blue': '#0000FF',
    'yellow': '#FFFF00',
    'cyan': '#00FFFF',
    'magenta': '#FF00FF',
    'orange': '#FFA500',
    'purple': '#800080',
    'pink': '#FFC0CB',
    'brown': '#A52A2A',
    'gray': '#808080',
    'grey': '#808080',
    'silver': '#C0C0C0',
    'gold': '#FFD700',
    'navy': '#000080',
    'teal': '#008080',
    'olive': '#808000',
    'maroon': '#800000',
    'lime': '#00FF00',
    'aqua': '#00FFFF',
    'fuchsia': '#FF00FF',
    'coral': '#FF7F50',
    'salmon': '#FA8072',
    'tomato': '#FF6347',
    'crimson': '#DC143C',
    'indigo': '#4B0082',
    'violet': '#EE82EE',
    'turquoise': '#40E0D0',
    'plum': '#DDA0DD',
    'khaki': '#F0E68C',
    'beige': '#F5F5DC',
    'ivory': '#FFFFF0',
    'mint': '#98FF98',
    'peach': '#FFDAB9',
    'lavender': '#E6E6FA',
    'skyblue': '#87CEEB',
    'chocolate': '#D2691E',
    'firebrick': '#B22222',
    'forestgreen': '#228B22',
    'darkgreen': '#006400',
    'darkblue': '#00008B',
    'darkred': '#8B0000',
    'darkorange': '#FF8C00',
    'darkviolet': '#9400D3',
    'deeppink': '#FF1493',
    'deepskyblue': '#00BFFF',
    'dodgerblue': '#1E90FF',
    'goldenrod': '#DAA520',
    'hotpink': '#FF69B4',
    'lightblue': '#ADD8E6',
    'lightgreen': '#90EE90',
    'lightgray': '#D3D3D3',
    'lightpink': '#FFB6C1',
    'lightsalmon': '#FFA07A',
    'lightseagreen': '#20B2AA',
    'lightskyblue': '#87CEFA',
    'lightsteelblue': '#B0C4DE',
    'lightyellow': '#FFFFE0',
    'limegreen': '#32CD32',
    'mediumblue': '#0000CD',
    'mediumorchid': '#BA55D3',
    'mediumpurple': '#9370DB',
    'mediumseagreen': '#3CB371',
    'mediumslateblue': '#7B68EE',
    'mediumspringgreen': '#00FA9A',
    'mediumturquoise': '#48D1CC',
    'mediumvioletred': '#C71585',
    'midnightblue': '#191970',
    'olivedrab': '#6B8E23',
    'orangered': '#FF4500',
    'orchid': '#DA70D6',
    'palegoldenrod': '#EEE8AA',
    'palegreen': '#98FB98',
    'paleturquoise': '#AFEEEE',
    'palevioletred': '#DB7093',
    'powderblue': '#B0E0E6',
    'rosybrown': '#BC8F8F',
    'royalblue': '#4169E1',
    'saddlebrown': '#8B4513',
    'sandybrown': '#F4A460',
    'seagreen': '#2E8B57',
    'sienna': '#A0522D',
    'slateblue': '#6A5ACD',
    'slategray': '#708090',
    'springgreen': '#00FF7F',
    'steelblue': '#4682B4',
    'tan': '#D2B48C',
    'thistle': '#D8BFD8',
    'wheat': '#F5DEB3',
    'whitesmoke': '#F5F5F5',
    'yellowgreen': '#9ACD32',
}


def color_name_to_hex(name: str) -> Optional[str]:
    """
    颜色名称转 HEX
    
    Args:
        name: 颜色名称
        
    Returns:
        HEX 字符串，如果找不到返回 None
        
    Example:
        >>> color_name_to_hex('red')
        '#FF0000'
        >>> color_name_to_hex('unknown')
        None
    """
    return CSS_COLORS.get(name.lower())


def hex_to_color_name(hex_color: str, threshold: int = 10) -> Optional[str]:
    """
    HEX 转最近的颜色名称
    
    Args:
        hex_color: HEX 字符串
        threshold: 允许的最大色差 (默认 10)
        
    Returns:
        颜色名称，如果找不到接近的返回 None
        
    Example:
        >>> hex_to_color_name('#FF0000')
        'red'
    """
    target = parse_color(hex_color)
    
    best_match = None
    best_distance = float('inf')
    
    for name, hex_val in CSS_COLORS.items():
        color = parse_color(hex_val)
        
        # 计算 RGB 欧几里得距离
        distance = math.sqrt(
            (target.r - color.r) ** 2 +
            (target.g - color.g) ** 2 +
            (target.b - color.b) ** 2
        )
        
        if distance < best_distance:
            best_distance = distance
            best_match = name
    
    if best_distance <= threshold * math.sqrt(3):
        return best_match
    
    return None


def suggest_text_color(background: Color) -> Color:
    """
    根据背景色建议文本颜色
    
    Args:
        background: 背景颜色
        
    Returns:
        建议的文本颜色 (黑色或白色)
        
    Example:
        >>> suggest_text_color(Color.from_hex('#000000'))  # 黑色背景
        Color(#ffffff)  # 建议白色文本
        >>> suggest_text_color(Color.from_hex('#FFFFFF'))  # 白色背景
        Color(#000000)  # 建议黑色文本
    """
    # WCAG 推荐阈值
    if background.luminance > 0.179:
        return Color(0, 0, 0)  # 黑色文本
    else:
        return Color(255, 255, 255)  # 白色文本


# ============================================================
# 便捷函数
# ============================================================

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """HEX 转 RGB"""
    r, g, b, _ = parse_hex(hex_color)
    return (r, g, b)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """RGB 转 HEX"""
    return f"#{r:02x}{g:02x}{b:02x}"


def is_valid_hex(hex_color: str) -> bool:
    """检查是否为有效的 HEX 颜色"""
    hex_color = hex_color.strip('#')
    if len(hex_color) not in (3, 4, 6, 8):
        return False
    try:
        int(hex_color, 16)
        return True
    except ValueError:
        return False


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    print("=== 颜色工具演示 ===\n")
    
    # 1. 创建颜色
    print("--- 创建颜色 ---")
    red = Color.from_hex('#FF0000')
    green = Color.from_rgb(0, 255, 0)
    blue = Color.from_hsl(240, 100, 50)
    print(f"红色: {red}")
    print(f"绿色: {green}")
    print(f"蓝色: {blue}")
    
    # 2. 格式转换
    print("\n--- 格式转换 ---")
    color = Color.from_hex('#4A90D9')
    print(f"HEX: {color.hex}")
    print(f"RGB: {color.rgb}")
    print(f"HSL: {color.hsl}")
    print(f"HSV: {color.hsv}")
    print(f"CMYK: {color.cmyk}")
    
    # 3. 颜色混合
    print("\n--- 颜色混合 ---")
    purple = mix_colors(red, blue, 0.5)
    print(f"红 + 蓝 = {purple.hex}")
    
    # 4. 对比度
    print("\n--- 对比度 ---")
    ratio = calculate_contrast_ratio(red, Color.from_hex('#FFFFFF'))
    print(f"红/白对比度: {ratio:.2f}:1")
    
    compliance = wcag_compliance(red, Color.from_hex('#FFFFFF'))
    print(f"WCAG 合规性: {compliance}")
    
    # 5. 配色方案
    print("\n--- 配色方案 ---")
    print(f"红色的互补色: {get_complement_color(red).hex}")
    print(f"红色的类似色: {[c.hex for c in get_analogous_colors(red)]}")
    print(f"红色的三角色: {[c.hex for c in get_triadic_colors(red)]}")
    
    # 6. 渐变
    print("\n--- 渐变 ---")
    gradient = create_gradient(red, blue, 5)
    print(f"红到蓝渐变: {[c.hex for c in gradient]}")
    
    # 7. 随机颜色
    print("\n--- 随机颜色 ---")
    print(f"随机颜色: {random_color().hex}")
    print(f"柔和色: {random_pastel_color().hex}")
    print(f"鲜艳色: {random_vibrant_color().hex}")
    
    # 8. 颜色名称
    print("\n--- 颜色名称 ---")
    print(f"'red' 的 HEX: {color_name_to_hex('red')}")
    print(f"'#FF0000' 的名称: {hex_to_color_name('#FF0000')}")
    
    # 9. 文本颜色建议
    print("\n--- 文本颜色建议 ---")
    print(f"黑色背景建议: {suggest_text_color(Color.from_hex('#000000')).hex}")
    print(f"白色背景建议: {suggest_text_color(Color.from_hex('#FFFFFF')).hex}")