"""
Color Utils - 颜色处理工具模块

提供颜色格式转换、调色板生成、对比度计算等功能。
零外部依赖，纯 Python 标准库实现。

功能列表:
- RGB/HSL/HSV/HEX 颜色格式互转
- 颜色名称查询 (CSS 颜色标准)
- 随机颜色生成
- 调色板生成 (互补色、类似色、三元组等)
- 颜色对比度计算 (WCAG 标准)
- 颜色混合
- 颜色亮度调整
- 颜色饱和度调整
"""

import math
import random
from typing import Tuple, List, Optional, Dict, Union

# CSS 标准颜色名称
CSS_COLORS = {
    # 基础颜色
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 128, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    
    # 灰度
    'gray': (128, 128, 128),
    'grey': (128, 128, 128),
    'silver': (192, 192, 192),
    'dimgray': (105, 105, 105),
    'dimgrey': (105, 105, 105),
    'darkgray': (169, 169, 169),
    'darkgrey': (169, 169, 169),
    'lightgray': (211, 211, 211),
    'lightgrey': (211, 211, 211),
    'gainsboro': (220, 220, 220),
    
    # 红色系
    'crimson': (220, 20, 60),
    'firebrick': (178, 34, 34),
    'indianred': (205, 92, 92),
    'lightcoral': (240, 128, 128),
    'darkred': (139, 0, 0),
    'maroon': (128, 0, 0),
    'orangered': (255, 69, 0),
    'tomato': (255, 99, 71),
    'coral': (255, 127, 80),
    'salmon': (250, 128, 114),
    'lightsalmon': (255, 160, 122),
    
    # 橙色系
    'orange': (255, 165, 0),
    'darkorange': (255, 140, 0),
    'coral': (255, 127, 80),
    
    # 黄色系
    'gold': (255, 215, 0),
    'khaki': (240, 230, 140),
    'lightyellow': (255, 255, 224),
    'lemonchiffon': (255, 250, 205),
    'papayawhip': (255, 239, 213),
    'moccasin': (255, 228, 181),
    'peachpuff': (255, 218, 185),
    'palegoldenrod': (238, 232, 170),
    'darkkhaki': (189, 183, 107),
    
    # 绿色系
    'lime': (0, 255, 0),
    'limegreen': (50, 205, 50),
    'forestgreen': (34, 139, 34),
    'darkgreen': (0, 100, 0),
    'lightgreen': (144, 238, 144),
    'palegreen': (152, 251, 152),
    'seagreen': (46, 139, 87),
    'mediumseagreen': (60, 179, 113),
    'springgreen': (0, 255, 127),
    'mediumspringgreen': (0, 250, 154),
    'darkseagreen': (143, 188, 143),
    'yellowgreen': (154, 205, 50),
    'olive': (128, 128, 0),
    'olivedrab': (107, 142, 35),
    'lawngreen': (124, 252, 0),
    'chartreuse': (127, 255, 0),
    'greenyellow': (173, 255, 47),
    
    # 青色系
    'aqua': (0, 255, 255),
    'teal': (0, 128, 128),
    'darkcyan': (0, 139, 139),
    'lightcyan': (224, 255, 255),
    'darkturquoise': (0, 206, 209),
    'turquoise': (64, 224, 208),
    'mediumturquoise': (72, 209, 204),
    'paleturquoise': (175, 238, 238),
    'aquamarine': (127, 255, 212),
    'mediumaquamarine': (102, 205, 170),
    
    # 蓝色系
    'navy': (0, 0, 128),
    'darkblue': (0, 0, 139),
    'mediumblue': (0, 0, 205),
    'royalblue': (65, 105, 225),
    'dodgerblue': (30, 144, 255),
    'deepskyblue': (0, 191, 255),
    'lightskyblue': (135, 206, 250),
    'skyblue': (135, 206, 235),
    'lightblue': (173, 216, 230),
    'powderblue': (176, 224, 230),
    'steelblue': (70, 130, 180),
    'lightsteelblue': (176, 196, 222),
    'cornflowerblue': (100, 149, 237),
    'cadetblue': (95, 158, 160),
    'mediumslateblue': (123, 104, 238),
    'slateblue': (106, 90, 205),
    'darkslateblue': (72, 61, 139),
    
    # 紫色系
    'purple': (128, 0, 128),
    'violet': (238, 130, 238),
    'indigo': (75, 0, 130),
    'darkviolet': (148, 0, 211),
    'blueviolet': (138, 43, 226),
    'mediumvioletred': (199, 21, 133),
    'palevioletred': (219, 112, 147),
    'darkmagenta': (139, 0, 139),
    'darkorchid': (153, 50, 204),
    'orchid': (218, 112, 214),
    'mediumorchid': (186, 85, 211),
    'plum': (221, 160, 221),
    'thistle': (216, 191, 216),
    'lavender': (230, 230, 250),
    
    # 粉色系
    'pink': (255, 192, 203),
    'lightpink': (255, 182, 193),
    'hotpink': (255, 105, 180),
    'deeppink': (255, 20, 147),
    'fuchsia': (255, 0, 255),
    
    # 棕色系
    'brown': (165, 42, 42),
    'saddlebrown': (139, 69, 19),
    'sienna': (160, 82, 45),
    'chocolate': (210, 105, 30),
    'peru': (205, 133, 63),
    'sandybrown': (244, 164, 96),
    'burlywood': (222, 184, 135),
    'tan': (210, 180, 140),
    'rosybrown': (188, 143, 143),
    'darksalmon': (233, 150, 122),
    'bisque': (255, 228, 196),
    'wheat': (245, 222, 179),
    'navajowhite': (255, 222, 173),
    'blanchedalmond': (255, 235, 205),
    'cornsilk': (255, 248, 220),
    
    # 其他
    'beige': (245, 245, 220),
    'ivory': (255, 255, 240),
    'linen': (250, 240, 230),
    'lavenderblush': (255, 240, 245),
    'mistyrose': (255, 228, 225),
    'seashell': (255, 245, 238),
    'oldlace': (253, 245, 230),
    'floralwhite': (255, 250, 240),
    'honeydew': (240, 255, 240),
    'mintcream': (245, 255, 250),
    'snow': (255, 250, 250),
    'aliceblue': (240, 248, 255),
    'ghostwhite': (248, 248, 255),
    'whitesmoke': (245, 245, 245),
    'antiquewhite': (250, 235, 215),
    'papayawhip': (255, 239, 213),
}

# 反向映射：RGB -> 颜色名称
RGB_TO_NAME = {v: k for k, v in CSS_COLORS.items()}


class Color:
    """
    颜色类，支持多种格式转换和操作。
    """
    
    def __init__(self, r: int, g: int, b: int, a: float = 1.0):
        """
        初始化颜色。
        
        Args:
            r: 红色分量 (0-255)
            g: 绿色分量 (0-255)
            b: 蓝色分量 (0-255)
            a: 透明度 (0.0-1.0)
        """
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))
        self.a = max(0.0, min(1.0, a))
    
    def __repr__(self) -> str:
        return f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Color):
            return (self.r, self.g, self.b, self.a) == (other.r, other.g, other.b, other.a)
        return False
    
    def __hash__(self) -> int:
        return hash((self.r, self.g, self.b, self.a))
    
    @property
    def rgb(self) -> Tuple[int, int, int]:
        """返回 RGB 元组。"""
        return (self.r, self.g, self.b)
    
    @property
    def rgba(self) -> Tuple[int, int, int, float]:
        """返回 RGBA 元组。"""
        return (self.r, self.g, self.b, self.a)
    
    @property
    def hex(self) -> str:
        """返回十六进制颜色字符串 (#RRGGBB)。"""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    @property
    def hex_with_alpha(self) -> str:
        """返回带透明度的十六进制颜色字符串 (#RRGGBBAA)。"""
        alpha_hex = int(self.a * 255)
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}{alpha_hex:02x}"
    
    @property
    def hsl(self) -> Tuple[float, float, float]:
        """返回 HSL 元组 (色相0-360, 饱和度0-100%, 亮度0-100%)。"""
        return rgb_to_hsl(self.r, self.g, self.b)
    
    @property
    def hsv(self) -> Tuple[float, float, float]:
        """返回 HSV 元组 (色相0-360, 饱和度0-100%, 明度0-100%)。"""
        return rgb_to_hsv(self.r, self.g, self.b)
    
    @property
    def luminance(self) -> float:
        """返回相对亮度 (0.0-1.0)。"""
        return calculate_luminance(self.r, self.g, self.b)
    
    @property
    def name(self) -> Optional[str]:
        """返回最接近的 CSS 颜色名称。"""
        return find_closest_color_name(self.r, self.g, self.b)
    
    # ===== 静态工厂方法 =====
    
    @staticmethod
    def from_hex(hex_str: str) -> 'Color':
        """从十六进制字符串创建颜色。"""
        r, g, b, a = hex_to_rgb(hex_str)
        return Color(r, g, b, a)
    
    @staticmethod
    def from_hsl(h: float, s: float, l: float, a: float = 1.0) -> 'Color':
        """从 HSL 创建颜色。"""
        r, g, b = hsl_to_rgb(h, s, l)
        return Color(r, g, b, a)
    
    @staticmethod
    def from_hsv(h: float, s: float, v: float, a: float = 1.0) -> 'Color':
        """从 HSV 创建颜色。"""
        r, g, b = hsv_to_rgb(h, s, v)
        return Color(r, g, b, a)
    
    @staticmethod
    def from_name(name: str, a: float = 1.0) -> 'Color':
        """从 CSS 颜色名称创建颜色。"""
        r, g, b = name_to_rgb(name)
        return Color(r, g, b, a)
    
    @staticmethod
    def random(hue: Optional[float] = None, saturation: Optional[float] = None,
               lightness: Optional[float] = None) -> 'Color':
        """生成随机颜色。"""
        h = hue if hue is not None else random.uniform(0, 360)
        s = saturation if saturation is not None else random.uniform(50, 100)
        l = lightness if lightness is not None else random.uniform(30, 70)
        return Color.from_hsl(h, s, l)
    
    # ===== 颜色操作方法 =====
    
    def lighten(self, amount: float = 10.0) -> 'Color':
        """
        增加亮度。
        
        Args:
            amount: 增加的亮度百分比 (0-100)
        
        Returns:
            新的 Color 对象
        """
        h, s, l = self.hsl
        l = min(100, l + amount)
        return Color.from_hsl(h, s, l, self.a)
    
    def darken(self, amount: float = 10.0) -> 'Color':
        """
        降低亮度。
        
        Args:
            amount: 降低的亮度百分比 (0-100)
        
        Returns:
            新的 Color 对象
        """
        h, s, l = self.hsl
        l = max(0, l - amount)
        return Color.from_hsl(h, s, l, self.a)
    
    def saturate(self, amount: float = 10.0) -> 'Color':
        """
        增加饱和度。
        
        Args:
            amount: 增加的饱和度百分比 (0-100)
        
        Returns:
            新的 Color 对象
        """
        h, s, l = self.hsl
        s = min(100, s + amount)
        return Color.from_hsl(h, s, l, self.a)
    
    def desaturate(self, amount: float = 10.0) -> 'Color':
        """
        降低饱和度。
        
        Args:
            amount: 降低的饱和度百分比 (0-100)
        
        Returns:
            新的 Color 对象
        """
        h, s, l = self.hsl
        s = max(0, s - amount)
        return Color.from_hsl(h, s, l, self.a)
    
    def grayscale(self) -> 'Color':
        """转换为灰度颜色。"""
        gray = int(0.299 * self.r + 0.587 * self.g + 0.114 * self.b)
        return Color(gray, gray, gray, self.a)
    
    def invert(self) -> 'Color':
        """返回反色。"""
        return Color(255 - self.r, 255 - self.g, 255 - self.b, self.a)
    
    def rotate_hue(self, degrees: float) -> 'Color':
        """
        旋转色相。
        
        Args:
            degrees: 旋转的角度 (-360 到 360)
        
        Returns:
            新的 Color 对象
        """
        h, s, l = self.hsl
        h = (h + degrees) % 360
        if h < 0:
            h += 360
        return Color.from_hsl(h, s, l, self.a)
    
    def complement(self) -> 'Color':
        """返回互补色。"""
        return self.rotate_hue(180)
    
    def mix(self, other: 'Color', weight: float = 0.5) -> 'Color':
        """
        与另一种颜色混合。
        
        Args:
            other: 另一种颜色
            weight: 本颜色的权重 (0.0-1.0)
        
        Returns:
            混合后的新颜色
        """
        w = max(0, min(1, weight))
        r = int(self.r * w + other.r * (1 - w))
        g = int(self.g * w + other.g * (1 - w))
        b = int(self.b * w + other.b * (1 - w))
        a = self.a * w + other.a * (1 - w)
        return Color(r, g, b, a)
    
    def contrast_ratio(self, other: 'Color') -> float:
        """
        计算与另一种颜色的对比度。
        
        Args:
            other: 另一种颜色
        
        Returns:
            对比度 (1.0-21.0)
        """
        return calculate_contrast_ratio(self.rgb, other.rgb)
    
    def wcag_compliance(self, other: 'Color') -> Dict[str, bool]:
        """
        检查 WCAG 对比度合规性。
        
        Args:
            other: 另一种颜色（通常是背景色）
        
        Returns:
            包含各级别合规性的字典
        """
        ratio = self.contrast_ratio(other)
        return {
            'aa_normal': ratio >= 4.5,
            'aa_large': ratio >= 3.0,
            'aaa_normal': ratio >= 7.0,
            'aaa_large': ratio >= 4.5,
            'ratio': ratio
        }
    
    def is_light(self) -> bool:
        """判断是否为浅色。"""
        return self.luminance > 0.5
    
    def is_dark(self) -> bool:
        """判断是否为深色。"""
        return self.luminance <= 0.5
    
    def text_color(self, light_color: Optional['Color'] = None, 
                   dark_color: Optional['Color'] = None) -> 'Color':
        """
        返回适合此背景的文本颜色。
        
        Args:
            light_color: 浅色文本颜色（默认白色）
            dark_color: 深色文本颜色（默认黑色）
        
        Returns:
            适合的文本颜色
        """
        light = light_color or Color(255, 255, 255)
        dark = dark_color or Color(0, 0, 0)
        return light if self.is_dark() else dark


# ===== 转换函数 =====

def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    将 RGB 转换为 HSL。
    
    Args:
        r, g, b: RGB 分量 (0-255)
    
    Returns:
        (h, s, l) - 色相(0-360), 饱和度(0-100), 亮度(0-100)
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    diff = max_c - min_c
    
    l = (max_c + min_c) / 2
    
    if diff == 0:
        h = s = 0.0
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
    将 HSL 转换为 RGB。
    
    Args:
        h: 色相 (0-360)
        s: 饱和度 (0-100)
        l: 亮度 (0-100)
    
    Returns:
        (r, g, b) - RGB 分量 (0-255)
    """
    s /= 100
    l /= 100
    
    if s == 0:
        r = g = b = l
    else:
        def hue_to_rgb(p, q, t):
            if t < 0:
                t += 1
            elif t > 1:
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
        
        h = h / 360
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)
    
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    将 RGB 转换为 HSV。
    
    Args:
        r, g, b: RGB 分量 (0-255)
    
    Returns:
        (h, s, v) - 色相(0-360), 饱和度(0-100), 明度(0-100)
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    diff = max_c - min_c
    
    v = max_c
    
    if diff == 0:
        h = s = 0.0
    else:
        s = diff / max_c
        
        if max_c == r:
            h = (g - b) / diff + (6 if g < b else 0)
        elif max_c == g:
            h = (b - r) / diff + 2
        else:
            h = (r - g) / diff + 4
        
        h *= 60
    
    return (h, s * 100, v * 100)


def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
    """
    将 HSV 转换为 RGB。
    
    Args:
        h: 色相 (0-360)
        s: 饱和度 (0-100)
        v: 明度 (0-100)
    
    Returns:
        (r, g, b) - RGB 分量 (0-255)
    """
    s /= 100
    v /= 100
    
    if s == 0:
        r = g = b = v
    else:
        h = h / 60
        i = int(h)
        f = h - i
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))
        
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q
    
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


def hex_to_rgb(hex_str: str) -> Tuple[int, int, int, float]:
    """
    将十六进制字符串转换为 RGB。
    
    Args:
        hex_str: 十六进制颜色字符串 (#RGB, #RRGGBB, #RRGGBBAA, RGB, RRGGBB, RRGGBBAA)
    
    Returns:
        (r, g, b, a) - RGB 分量 (0-255) 和透明度 (0.0-1.0)
    """
    hex_str = hex_str.strip().lstrip('#')
    
    if len(hex_str) == 3:
        hex_str = ''.join(c * 2 for c in hex_str)
    elif len(hex_str) == 4:
        hex_str = ''.join(c * 2 for c in hex_str)
    
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    
    if len(hex_str) >= 8:
        a = int(hex_str[6:8], 16) / 255.0
    else:
        a = 1.0
    
    return (r, g, b, a)


def rgb_to_hex(r: int, g: int, b: int, include_alpha: bool = False, 
               a: float = 1.0) -> str:
    """
    将 RGB 转换为十六进制字符串。
    
    Args:
        r, g, b: RGB 分量 (0-255)
        include_alpha: 是否包含透明度
        a: 透明度 (0.0-1.0)
    
    Returns:
        十六进制颜色字符串
    """
    if include_alpha:
        alpha_hex = int(a * 255)
        return f"#{r:02x}{g:02x}{b:02x}{alpha_hex:02x}"
    return f"#{r:02x}{g:02x}{b:02x}"


def name_to_rgb(name: str) -> Tuple[int, int, int]:
    """
    将 CSS 颜色名称转换为 RGB。
    
    Args:
        name: CSS 颜色名称
    
    Returns:
        (r, g, b) - RGB 分量
    
    Raises:
        ValueError: 颜色名称不存在
    """
    name_lower = name.lower().replace(' ', '')
    if name_lower not in CSS_COLORS:
        raise ValueError(f"Unknown color name: {name}")
    return CSS_COLORS[name_lower]


def rgb_to_name(r: int, g: int, b: int, exact: bool = True) -> Optional[str]:
    """
    将 RGB 转换为颜色名称。
    
    Args:
        r, g, b: RGB 分量
        exact: 是否要求精确匹配
    
    Returns:
        颜色名称，如果没有匹配则返回 None
    """
    if exact:
        return RGB_TO_NAME.get((r, g, b))
    return find_closest_color_name(r, g, b)


def find_closest_color_name(r: int, g: int, b: int) -> str:
    """
    找到最接近的颜色名称。
    
    Args:
        r, g, b: RGB 分量
    
    Returns:
        最接近的颜色名称
    """
    min_distance = float('inf')
    closest_name = 'gray'
    
    for name, (nr, ng, nb) in CSS_COLORS.items():
        distance = math.sqrt((r - nr) ** 2 + (g - ng) ** 2 + (b - nb) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_name = name
    
    return closest_name


# ===== 对比度和亮度计算 =====

def calculate_luminance(r: int, g: int, b: int) -> float:
    """
    计算颜色的相对亮度 (WCAG 标准)。
    
    Args:
        r, g, b: RGB 分量 (0-255)
    
    Returns:
        相对亮度 (0.0-1.0)
    """
    def adjust(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)


def calculate_contrast_ratio(rgb1: Tuple[int, int, int], 
                            rgb2: Tuple[int, int, int]) -> float:
    """
    计算两种颜色的对比度 (WCAG 标准)。
    
    Args:
        rgb1: 第一种颜色的 RGB 元组
        rgb2: 第二种颜色的 RGB 元组
    
    Returns:
        对比度 (1.0-21.0)
    """
    l1 = calculate_luminance(*rgb1)
    l2 = calculate_luminance(*rgb2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


# ===== 调色板生成 =====

def generate_complementary(color: Color) -> Tuple[Color, Color]:
    """
    生成互补色对。
    
    Args:
        color: 基础颜色
    
    Returns:
        (原色, 互补色)
    """
    return (color, color.complement())


def generate_analogous(color: Color, angle: float = 30.0) -> List[Color]:
    """
    生成类似色 (相邻色)。
    
    Args:
        color: 基础颜色
        angle: 相邻色之间的角度 (默认 30 度)
    
    Returns:
        [左相邻色, 原色, 右相邻色]
    """
    return [
        color.rotate_hue(-angle),
        color,
        color.rotate_hue(angle)
    ]


def generate_triadic(color: Color) -> List[Color]:
    """
    生成三元组色 (三角对立色)。
    
    Args:
        color: 基础颜色
    
    Returns:
        [原色, 120度色, 240度色]
    """
    return [
        color,
        color.rotate_hue(120),
        color.rotate_hue(240)
    ]


def generate_split_complementary(color: Color, angle: float = 30.0) -> List[Color]:
    """
    生成分裂互补色。
    
    Args:
        color: 基础颜色
        angle: 偏离互补色的角度 (默认 30 度)
    
    Returns:
        [原色, 互补色左侧, 互补色右侧]
    """
    complement = color.complement()
    return [
        color,
        complement.rotate_hue(-angle),
        complement.rotate_hue(angle)
    ]


def generate_tetradic(color: Color) -> List[Color]:
    """
    生成四元组色 (方形色)。
    
    Args:
        color: 基础颜色
    
    Returns:
        [原色, 90度色, 180度色, 270度色]
    """
    return [
        color,
        color.rotate_hue(90),
        color.rotate_hue(180),
        color.rotate_hue(270)
    ]


def generate_square(color: Color) -> List[Color]:
    """
    生成方形色 (同 tetradic)。
    
    Args:
        color: 基础颜色
    
    Returns:
        四个等距颜色
    """
    return generate_tetradic(color)


def generate_shades(color: Color, count: int = 5) -> List[Color]:
    """
    生成同色系的深浅变化。
    
    Args:
        color: 基础颜色
        count: 生成的颜色数量
    
    Returns:
        颜色列表 (从浅到深)
    """
    h, s, l = color.hsl
    step = l / (count + 1)
    
    return [Color.from_hsl(h, s, step * (i + 1)) for i in range(count)]


def generate_tints(color: Color, count: int = 5) -> List[Color]:
    """
    生成颜色的浅色调变化 (混入白色)。
    
    Args:
        color: 基础颜色
        count: 生成的颜色数量
    
    Returns:
        颜色列表 (从原色到白色)
    """
    white = Color(255, 255, 255)
    step = 1.0 / (count + 1)
    
    return [color.mix(white, 1 - step * (i + 1)) for i in range(count)]


def generate_tones(color: Color, count: int = 5) -> List[Color]:
    """
    生成颜色的色调变化 (混入灰色)。
    
    Args:
        color: 基础颜色
        count: 生成的颜色数量
    
    Returns:
        颜色列表
    """
    h, s, l = color.hsl
    step = s / (count + 1)
    
    return [Color.from_hsl(h, s - step * (i + 1), l) for i in range(count)]


def generate_gradient(start: Color, end: Color, steps: int) -> List[Color]:
    """
    生成两个颜色之间的渐变。
    
    Args:
        start: 起始颜色
        end: 结束颜色
        steps: 步数
    
    Returns:
        颜色列表
    """
    if steps < 2:
        return [start]
    
    step_size = 1.0 / (steps - 1)
    return [start.mix(end, 1 - step_size * i) for i in range(steps)]


def generate_monochromatic(color: Color, count: int = 5) -> List[Color]:
    """
    生成单色调色板 (同色相的不同饱和度和亮度)。
    
    Args:
        color: 基础颜色
        count: 生成的颜色数量
    
    Returns:
        颜色列表
    """
    h, s, l = color.hsl
    result = []
    
    for i in range(count):
        # 变化饱和度和亮度
        new_s = max(20, min(100, s + (i - count // 2) * 15))
        new_l = max(20, min(80, l + (i - count // 2) * 10))
        result.append(Color.from_hsl(h, new_s, new_l))
    
    return result


def generate_palette(color: Color, palette_type: str = 'complementary') -> List[Color]:
    """
    根据类型生成调色板。
    
    Args:
        color: 基础颜色
        palette_type: 调色板类型 
                      ('complementary', 'analogous', 'triadic', 
                       'split', 'tetradic', 'monochromatic')
    
    Returns:
        颜色列表
    """
    generators = {
        'complementary': lambda c: list(generate_complementary(c)),
        'analogous': generate_analogous,
        'triadic': generate_triadic,
        'split': generate_split_complementary,
        'tetradic': generate_tetradic,
        'monochromatic': generate_monochromatic,
    }
    
    if palette_type not in generators:
        raise ValueError(f"Unknown palette type: {palette_type}")
    
    return generators[palette_type](color)


# ===== 实用函数 =====

def random_color(hue: Optional[float] = None, saturation: Optional[float] = None,
                 lightness: Optional[float] = None) -> Color:
    """
    生成随机颜色。
    
    Args:
        hue: 指定色相 (可选)
        saturation: 指定饱和度 (可选)
        lightness: 指定亮度 (可选)
    
    Returns:
        Color 对象
    """
    return Color.random(hue, saturation, lightness)


def random_pastel() -> Color:
    """生成随机柔和色。"""
    return Color.random(lightness=70, saturation=60)


def random_vibrant() -> Color:
    """生成随机鲜艳色。"""
    return Color.random(saturation=90, lightness=50)


def random_dark() -> Color:
    """生成随机深色。"""
    return Color.random(lightness=30, saturation=70)


def random_light() -> Color:
    """生成随机浅色。"""
    return Color.random(lightness=80, saturation=50)


def blend_colors(colors: List[Color], weights: Optional[List[float]] = None) -> Color:
    """
    混合多个颜色。
    
    Args:
        colors: 颜色列表
        weights: 权重列表 (可选)
    
    Returns:
        混合后的颜色
    """
    if not colors:
        raise ValueError("Colors list cannot be empty")
    
    if weights is None:
        weights = [1.0 / len(colors)] * len(colors)
    
    if len(colors) != len(weights):
        raise ValueError("Colors and weights must have the same length")
    
    total_weight = sum(weights)
    weights = [w / total_weight for w in weights]
    
    r = sum(c.r * w for c, w in zip(colors, weights))
    g = sum(c.g * w for c, w in zip(colors, weights))
    b = sum(c.b * w for c, w in zip(colors, weights))
    a = sum(c.a * w for c, w in zip(colors, weights))
    
    return Color(int(r), int(g), int(b), a)


def parse_color(color_str: str) -> Color:
    """
    解析颜色字符串。
    
    支持格式:
    - 十六进制: #RGB, #RRGGBB, #RRGGBBAA
    - CSS 名称: red, blue, etc.
    - RGB: rgb(255, 0, 0), rgba(255, 0, 0, 0.5)
    - HSL: hsl(0, 100%, 50%), hsla(0, 100%, 50%, 0.5)
    
    Args:
        color_str: 颜色字符串
    
    Returns:
        Color 对象
    """
    color_str = color_str.strip().lower()
    
    # 十六进制
    if color_str.startswith('#'):
        return Color.from_hex(color_str)
    
    # RGB/RGBA
    if color_str.startswith('rgb'):
        import re
        match = re.match(r'rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)', color_str)
        if match:
            r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
            a = float(match.group(4)) if match.group(4) else 1.0
            return Color(r, g, b, a)
    
    # HSL/HSLA
    if color_str.startswith('hsl'):
        import re
        match = re.match(r'hsla?\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)%?\s*(?:,\s*([\d.]+)\s*)?\)', color_str)
        if match:
            h, s, l = float(match.group(1)), float(match.group(2)), float(match.group(3))
            a = float(match.group(4)) if match.group(4) else 1.0
            return Color.from_hsl(h, s, l, a)
    
    # CSS 名称
    try:
        return Color.from_name(color_str)
    except ValueError:
        pass
    
    raise ValueError(f"Unable to parse color: {color_str}")


def get_color_suggestions(color: Color, purpose: str = 'ui') -> Dict[str, Color]:
    """
    获取颜色建议。
    
    Args:
        color: 基础颜色
        purpose: 用途 ('ui', 'text', 'background')
    
    Returns:
        包含建议颜色的字典
    """
    suggestions = {
        'original': color,
        'text_on_bg': color.text_color(),
        'complement': color.complement(),
        'lighter': color.lighten(20),
        'darker': color.darken(20),
        'saturated': color.saturate(20),
        'desaturated': color.desaturate(20),
    }
    
    if purpose == 'ui':
        suggestions.update({
            'hover': color.darken(10),
            'active': color.darken(20),
            'disabled': color.desaturate(50).lighten(20),
            'border': color.darken(30),
        })
    elif purpose == 'text':
        suggestions.update({
            'primary': color,
            'secondary': color.desaturate(30),
            'muted': color.desaturate(50).lighten(10),
        })
    
    return suggestions


# 导出
__all__ = [
    'Color',
    'CSS_COLORS',
    'RGB_TO_NAME',
    'rgb_to_hsl',
    'hsl_to_rgb',
    'rgb_to_hsv',
    'hsv_to_rgb',
    'hex_to_rgb',
    'rgb_to_hex',
    'name_to_rgb',
    'rgb_to_name',
    'find_closest_color_name',
    'calculate_luminance',
    'calculate_contrast_ratio',
    'generate_complementary',
    'generate_analogous',
    'generate_triadic',
    'generate_split_complementary',
    'generate_tetradic',
    'generate_square',
    'generate_shades',
    'generate_tints',
    'generate_tones',
    'generate_gradient',
    'generate_monochromatic',
    'generate_palette',
    'random_color',
    'random_pastel',
    'random_vibrant',
    'random_dark',
    'random_light',
    'blend_colors',
    'parse_color',
    'get_color_suggestions',
]