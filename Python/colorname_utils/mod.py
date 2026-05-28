"""
ColorName Utils - 颜色名称映射工具模块

提供颜色到人类可读名称的映射功能。
零外部依赖，纯 Python 实现。

功能：
- RGB/HEX/HSL 颜色格式转换
- 颜色名称查找（最近匹配）
- 颜色分类（红/蓝/绿等）
- 亮度/温度分析
- 颜色混合/调整
- 颜色方案生成

作者：AllToolkit
日期：2026-05-28
"""

from typing import Tuple, List, Dict, Optional, NamedTuple
from dataclasses import dataclass
import math
import random


@dataclass
class RGB:
    """RGB 颜色表示"""
    r: int
    g: int
    b: int
    
    def __post_init__(self):
        self.r = max(0, min(255, int(self.r)))
        self.g = max(0, min(255, int(self.g)))
        self.b = max(0, min(255, int(self.b)))
    
    def to_hex(self) -> str:
        """转换为十六进制格式"""
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"
    
    def to_hsl(self) -> 'HSL':
        """转换为 HSL"""
        return rgb_to_hsl(self)
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """转换为元组"""
        return (self.r, self.g, self.b)
    
    def __repr__(self) -> str:
        return f"RGB({self.r}, {self.g}, {self.b})"


@dataclass
class HSL:
    """HSL 颜色表示"""
    h: float  # 0-360
    s: float  # 0-100
    l: float  # 0-100
    
    def __post_init__(self):
        self.h = max(0, min(360, float(self.h)))
        self.s = max(0, min(100, float(self.s)))
        self.l = max(0, min(100, float(self.l)))
    
    def to_rgb(self) -> RGB:
        """转换为 RGB"""
        return hsl_to_rgb(self)
    
    def __repr__(self) -> str:
        return f"HSL({self.h:.1f}, {self.s:.1f}%, {self.l:.1f}%)"


class ColorMatch(NamedTuple):
    """颜色匹配结果"""
    name: str
    hex: str
    distance: float


class ColorInfo(NamedTuple):
    """颜色详细信息"""
    name: str
    hex: str
    rgb: RGB
    hsl: HSL
    category: str
    brightness: str
    temperature: str


# 颜色数据库 - 常见颜色及其 RGB 值
_COLOR_DATABASE: List[Tuple[str, RGB]] = [
    # 红色系
    ("Red", RGB(255, 0, 0)),
    ("Crimson", RGB(220, 20, 60)),
    ("Fire Brick", RGB(178, 34, 34)),
    ("Dark Red", RGB(139, 0, 0)),
    ("Maroon", RGB(128, 0, 0)),
    ("Indian Red", RGB(205, 92, 92)),
    ("Light Coral", RGB(240, 128, 128)),
    ("Salmon", RGB(250, 128, 114)),
    ("Light Salmon", RGB(255, 160, 122)),
    ("Tomato", RGB(255, 99, 71)),
    ("Orange Red", RGB(255, 69, 0)),
    ("Ruby", RGB(224, 17, 95)),
    ("Scarlet", RGB(255, 36, 0)),
    ("Cherry", RGB(222, 49, 99)),
    ("Rose", RGB(255, 0, 127)),
    ("Carmine", RGB(150, 0, 24)),
    
    # 粉色系
    ("Pink", RGB(255, 192, 203)),
    ("Light Pink", RGB(255, 182, 193)),
    ("Hot Pink", RGB(255, 105, 180)),
    ("Deep Pink", RGB(255, 20, 147)),
    ("Pale Violet Red", RGB(219, 112, 147)),
    ("Medium Violet Red", RGB(199, 21, 133)),
    ("Magenta", RGB(255, 0, 255)),
    ("Fuchsia", RGB(255, 0, 255)),
    ("Dark Magenta", RGB(139, 0, 139)),
    ("Violet Red", RGB(199, 21, 133)),
    ("Blush", RGB(255, 181, 189)),
    ("Coral Pink", RGB(255, 127, 80)),
    ("Orchid", RGB(218, 112, 214)),
    ("Plum", RGB(221, 160, 221)),
    
    # 橙色系
    ("Orange", RGB(255, 165, 0)),
    ("Dark Orange", RGB(255, 140, 0)),
    ("Light Orange", RGB(255, 204, 92)),
    ("Coral", RGB(255, 127, 80)),
    ("Peach", RGB(255, 218, 185)),
    ("Apricot", RGB(255, 195, 111)),
    ("Tangerine", RGB(255, 144, 0)),
    ("Amber", RGB(255, 191, 0)),
    ("Carrot Orange", RGB(237, 145, 33)),
    ("Burnt Orange", RGB(204, 85, 0)),
    ("Pumpkin", RGB(255, 117, 24)),
    
    # 黄色系
    ("Yellow", RGB(255, 255, 0)),
    ("Light Yellow", RGB(255, 255, 224)),
    ("Lemon", RGB(255, 247, 0)),
    ("Lemon Chiffon", RGB(255, 250, 205)),
    ("Light Goldenrod Yellow", RGB(250, 250, 210)),
    ("Papaya Whip", RGB(255, 239, 213)),
    ("Moccasin", RGB(255, 228, 181)),
    ("Peach Puff", RGB(255, 218, 185)),
    ("Pale Goldenrod", RGB(238, 232, 170)),
    ("Khaki", RGB(240, 230, 140)),
    ("Dark Khaki", RGB(189, 183, 107)),
    ("Gold", RGB(255, 215, 0)),
    ("Goldenrod", RGB(218, 165, 32)),
    ("Dark Goldenrod", RGB(184, 134, 11)),
    ("Canary", RGB(255, 255, 115)),
    ("Mustard", RGB(255, 219, 88)),
    ("Cream", RGB(255, 253, 208)),
    ("Beige", RGB(245, 245, 220)),
    ("Banana", RGB(255, 225, 53)),
    
    # 绿色系
    ("Green", RGB(0, 128, 0)),
    ("Lime", RGB(0, 255, 0)),
    ("Lime Green", RGB(50, 205, 50)),
    ("Lawn Green", RGB(124, 252, 0)),
    ("Chartreuse", RGB(127, 255, 0)),
    ("Green Yellow", RGB(173, 255, 47)),
    ("Yellow Green", RGB(154, 205, 50)),
    ("Spring Green", RGB(0, 255, 127)),
    ("Medium Spring Green", RGB(0, 250, 154)),
    ("Light Green", RGB(144, 238, 144)),
    ("Pale Green", RGB(152, 251, 152)),
    ("Dark Green", RGB(0, 100, 0)),
    ("Forest Green", RGB(34, 139, 34)),
    ("Sea Green", RGB(46, 139, 87)),
    ("Medium Sea Green", RGB(60, 179, 113)),
    ("Dark Sea Green", RGB(143, 188, 143)),
    ("Light Sea Green", RGB(32, 178, 170)),
    ("Olive", RGB(128, 128, 0)),
    ("Olive Drab", RGB(107, 142, 35)),
    ("Dark Olive Green", RGB(85, 107, 47)),
    ("Tea Green", RGB(208, 240, 192)),
    ("Mint", RGB(189, 252, 201)),
    ("Emerald", RGB(80, 200, 120)),
    ("Jade", RGB(0, 168, 107)),
    ("Moss Green", RGB(138, 154, 91)),
    ("Sage", RGB(188, 184, 138)),
    ("Seafoam", RGB(93, 171, 147)),
    
    # 青色系
    ("Cyan", RGB(0, 255, 255)),
    ("Aqua", RGB(0, 255, 255)),
    ("Light Cyan", RGB(224, 255, 255)),
    ("Pale Turquoise", RGB(175, 238, 238)),
    ("Aquamarine", RGB(127, 255, 212)),
    ("Turquoise", RGB(64, 224, 208)),
    ("Medium Turquoise", RGB(72, 209, 204)),
    ("Dark Turquoise", RGB(0, 206, 209)),
    ("Cadet Blue", RGB(95, 158, 160)),
    ("Steel Blue", RGB(70, 130, 180)),
    ("Teal", RGB(0, 128, 128)),
    ("Dark Cyan", RGB(0, 139, 139)),
    
    # 蓝色系
    ("Blue", RGB(0, 0, 255)),
    ("Light Blue", RGB(173, 216, 230)),
    ("Powder Blue", RGB(176, 224, 230)),
    ("Sky Blue", RGB(135, 206, 235)),
    ("Light Sky Blue", RGB(135, 206, 250)),
    ("Deep Sky Blue", RGB(0, 191, 255)),
    ("Dodger Blue", RGB(30, 144, 255)),
    ("Cornflower Blue", RGB(100, 149, 237)),
    ("Medium Slate Blue", RGB(123, 104, 238)),
    ("Royal Blue", RGB(65, 105, 225)),
    ("Blue Violet", RGB(138, 43, 226)),
    ("Indigo", RGB(75, 0, 130)),
    ("Dark Blue", RGB(0, 0, 139)),
    ("Medium Blue", RGB(0, 0, 205)),
    ("Navy", RGB(0, 0, 128)),
    ("Midnight Blue", RGB(25, 25, 112)),
    ("Slate Blue", RGB(106, 90, 205)),
    ("Dark Slate Blue", RGB(72, 61, 139)),
    ("Sapphire", RGB(15, 82, 186)),
    ("Cobalt", RGB(0, 71, 171)),
    ("Azure", RGB(0, 127, 255)),
    ("Baby Blue", RGB(137, 207, 240)),
    ("Periwinkle", RGB(204, 204, 255)),
    ("Electric Blue", RGB(125, 249, 255)),
    
    # 紫色系
    ("Purple", RGB(128, 0, 128)),
    ("Light Purple", RGB(180, 96, 208)),
    ("Medium Purple", RGB(147, 112, 219)),
    ("Dark Purple", RGB(99, 0, 139)),
    ("Dark Violet", RGB(148, 0, 211)),
    ("Violet", RGB(238, 130, 238)),
    ("Lavender", RGB(230, 230, 250)),
    ("Thistle", RGB(216, 191, 216)),
    ("Medium Orchid", RGB(186, 85, 211)),
    ("Dark Orchid", RGB(153, 50, 204)),
    ("Heliotrope", RGB(223, 115, 255)),
    ("Lilac", RGB(200, 162, 200)),
    ("Grape", RGB(111, 45, 168)),
    ("Amethyst", RGB(153, 102, 204)),
    ("Mauve", RGB(224, 176, 255)),
    ("Wisteria", RGB(201, 160, 220)),
    
    # 棕色系
    ("Brown", RGB(165, 42, 42)),
    ("Saddle Brown", RGB(139, 69, 19)),
    ("Sienna", RGB(160, 82, 45)),
    ("Chocolate", RGB(210, 105, 30)),
    ("Peru", RGB(205, 133, 63)),
    ("Sandy Brown", RGB(244, 164, 96)),
    ("Rosy Brown", RGB(188, 143, 143)),
    ("Tan", RGB(210, 180, 140)),
    ("Light Tan", RGB(238, 213, 183)),
    ("Burlywood", RGB(222, 184, 135)),
    ("Wheat", RGB(245, 222, 179)),
    ("Navajo White", RGB(255, 222, 173)),
    ("Bisque", RGB(255, 228, 196)),
    ("Blanched Almond", RGB(255, 235, 205)),
    ("Cornsilk", RGB(255, 248, 220)),
    ("Copper", RGB(184, 115, 51)),
    ("Bronze", RGB(205, 127, 50)),
    ("Rust", RGB(183, 65, 14)),
    ("Coffee", RGB(111, 78, 55)),
    ("Mahogany", RGB(192, 64, 0)),
    ("Chestnut", RGB(149, 69, 53)),
    ("Cinnamon", RGB(210, 105, 30)),
    
    # 中性色
    ("White", RGB(255, 255, 255)),
    ("Snow", RGB(255, 250, 250)),
    ("Honeydew", RGB(240, 255, 240)),
    ("Mint Cream", RGB(245, 255, 250)),
    ("Ghost White", RGB(248, 248, 255)),
    ("White Smoke", RGB(245, 245, 245)),
    ("Seashell", RGB(255, 245, 238)),
    ("Old Lace", RGB(253, 245, 230)),
    ("Floral White", RGB(255, 250, 240)),
    ("Ivory", RGB(255, 255, 240)),
    ("Antique White", RGB(250, 235, 215)),
    ("Linen", RGB(250, 240, 230)),
    ("Lavender Blush", RGB(255, 240, 245)),
    ("Misty Rose", RGB(255, 228, 225)),
    ("Gainsboro", RGB(220, 220, 220)),
    ("Light Gray", RGB(211, 211, 211)),
    ("Silver", RGB(192, 192, 192)),
    ("Dark Gray", RGB(169, 169, 169)),
    ("Gray", RGB(128, 128, 128)),
    ("Dim Gray", RGB(105, 105, 105)),
    ("Light Slate Gray", RGB(119, 136, 153)),
    ("Slate Gray", RGB(112, 128, 144)),
    ("Dark Slate Gray", RGB(47, 79, 79)),
    ("Black", RGB(0, 0, 0)),
    ("Charcoal", RGB(54, 69, 79)),
    ("Slate", RGB(112, 128, 144)),
    ("Ash Gray", RGB(178, 190, 181)),
    ("Taupe", RGB(72, 60, 50)),
    ("Gunmetal", RGB(42, 52, 57)),
    
    # 额外常用颜色
    ("Dark Teal", RGB(0, 102, 102)),
    ("Light Teal", RGB(0, 153, 153)),
    ("Mint Green", RGB(152, 255, 152)),
    ("Army Green", RGB(75, 83, 32)),
    ("Hunter Green", RGB(53, 94, 59)),
    ("Fern Green", RGB(79, 121, 66)),
    ("Kelly Green", RGB(76, 187, 23)),
    ("Irish Green", RGB(0, 158, 96)),
    ("Shamrock", RGB(68, 214, 44)),
    ("Avocado", RGB(86, 130, 3)),
    ("Electric Lime", RGB(204, 255, 0)),
    ("Acid Green", RGB(176, 255, 56)),
    ("Neon Green", RGB(57, 255, 20)),
    ("Harlequin", RGB(63, 255, 0)),
    ("Spring Bud", RGB(167, 252, 0)),
    ("Bright Green", RGB(102, 255, 0)),
    ("Pine Green", RGB(1, 121, 111)),
    ("Fern", RGB(113, 146, 103)),
    ("Celadon", RGB(172, 225, 175)),
    ("Pear", RGB(209, 226, 49)),
    ("Moss", RGB(138, 154, 91)),
    ("Seaweed", RGB(24, 87, 42)),
    ("Pine", RGB(43, 74, 41)),
    ("Racing Green", RGB(26, 68, 31)),
    ("British Racing Green", RGB(0, 66, 37)),
    ("Brunswick Green", RGB(27, 77, 46)),
    ("Laurel Green", RGB(169, 186, 157)),
    ("Cambridge Blue", RGB(163, 193, 173)),
    ("Eton Blue", RGB(150, 200, 162)),
    ("Verdigris", RGB(67, 179, 174)),
    ("Viridian", RGB(64, 130, 109)),
    ("Malachite", RGB(11, 218, 81)),
    ("Ivy Green", RGB(0, 111, 60)),
    ("Spinach Green", RGB(24, 83, 44)),
    ("Parrot Green", RGB(0, 165, 103)),
    ("Amazon", RGB(59, 122, 87)),
    ("Bottle Green", RGB(0, 106, 78)),
    ("Evergreen", RGB(1, 95, 63)),
    ("Christmas Green", RGB(0, 128, 0)),
    ("Christmas Red", RGB(220, 0, 0)),
]


# ============ 颜色格式转换 ============

def parse_hex(hex_color: str) -> RGB:
    """
    解析十六进制颜色字符串
    
    Args:
        hex_color: 十六进制颜色字符串，如 "#FF0000", "FF0000", "#F00", "F00"
    
    Returns:
        RGB 对象
    
    Raises:
        ValueError: 无效的颜色格式
    """
    hex_color = hex_color.strip()
    # Remove '#' prefix
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    # Remove '0x' prefix
    if hex_color.startswith('0x') or hex_color.startswith('0X'):
        hex_color = hex_color[2:]
    
    # Handle 3-character shorthand (e.g., "F00" -> "FF0000")
    if len(hex_color) == 3:
        hex_color = hex_color[0] * 2 + hex_color[1] * 2 + hex_color[2] * 2
    # Handle 4-character shorthand with alpha (ignore alpha)
    elif len(hex_color) == 4:
        hex_color = hex_color[0] * 2 + hex_color[1] * 2 + hex_color[2] * 2
    
    if len(hex_color) != 6:
        raise ValueError(f"无效的十六进制颜色格式: {hex_color}")
    
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return RGB(r, g, b)
    except ValueError as e:
        raise ValueError(f"无效的十六进制颜色: {hex_color}") from e


def parse_rgb(rgb_str: str) -> RGB:
    """
    解析 RGB 字符串
    
    Args:
        rgb_str: RGB 字符串，如 "rgb(255, 0, 0)" 或 "255, 0, 0"
    
    Returns:
        RGB 对象
    
    Raises:
        ValueError: 无效的颜色格式
    """
    rgb_str = rgb_str.strip()
    rgb_str = rgb_str.replace('rgb(', '').replace('RGB(', '').replace(')', '')
    
    parts = [p.strip() for p in rgb_str.split(',')]
    if len(parts) != 3:
        raise ValueError(f"无效的 RGB 格式，期望 'r, g, b': {rgb_str}")
    
    try:
        r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
        if not all(0 <= v <= 255 for v in [r, g, b]):
            raise ValueError("RGB 值必须在 0-255 范围内")
        return RGB(r, g, b)
    except ValueError as e:
        raise ValueError(f"无效的 RGB 值: {rgb_str}") from e


def rgb_to_hex(rgb: RGB) -> str:
    """RGB 转十六进制"""
    return rgb.to_hex()


def rgb_to_hsl(rgb: RGB) -> HSL:
    """RGB 转 HSL"""
    r, g, b = rgb.r / 255.0, rgb.g / 255.0, rgb.b / 255.0
    
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    
    l = (max_val + min_val) / 2.0
    
    if max_val == min_val:
        h = s = 0
    else:
        d = max_val - min_val
        s = d / (1 - abs(2 * l - 1))
        
        if max_val == r:
            h = (g - b) / d
            if g < b:
                h += 6
        elif max_val == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        
        h *= 60
    
    return HSL(h, s * 100, l * 100)


def hsl_to_rgb(hsl: HSL) -> RGB:
    """HSL 转 RGB"""
    h = hsl.h / 360.0
    s = hsl.s / 100.0
    l = hsl.l / 100.0
    
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
    
    if s == 0:
        r = g = b = l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)
    
    return RGB(int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


# ============ 颜色距离计算 ============

def color_distance(c1: RGB, c2: RGB) -> float:
    """
    计算两个颜色之间的感知距离
    
    使用加权欧几里得距离公式，更准确地反映人眼感知
    
    Args:
        c1: 第一个颜色
        c2: 第二个颜色
    
    Returns:
        颜色距离（越小越相似）
    """
    r_mean = (c1.r + c2.r) / 2.0
    r = c1.r - c2.r
    g = c1.g - c2.g
    b = c1.b - c2.b
    
    # 加权公式提高感知准确性
    return math.sqrt((2 + r_mean/256) * r * r + 4 * g * g + (2 + (255 - r_mean)/256) * b * b)


# ============ 颜色名称查找 ============

def get_color_name(rgb: RGB) -> str:
    """
    获取颜色的最近匹配名称
    
    Args:
        rgb: RGB 颜色对象
    
    Returns:
        最接近的颜色名称
    """
    return get_closest_color(rgb).name


def get_closest_color(rgb: RGB) -> ColorMatch:
    """
    查找最接近的颜色匹配
    
    Args:
        rgb: RGB 颜色对象
    
    Returns:
        ColorMatch 包含名称、十六进制和距离
    """
    best_match = ColorMatch("Unknown", "#000000", float('inf'))
    
    for name, color in _COLOR_DATABASE:
        dist = color_distance(rgb, color)
        if dist < best_match.distance:
            best_match = ColorMatch(name, color.to_hex(), dist)
    
    return best_match


def get_n_closest_colors(rgb: RGB, n: int = 5) -> List[ColorMatch]:
    """
    获取 n 个最接近的颜色匹配
    
    Args:
        rgb: RGB 颜色对象
        n: 返回的颜色数量
    
    Returns:
        按距离排序的颜色匹配列表
    """
    scored = []
    for name, color in _COLOR_DATABASE:
        dist = color_distance(rgb, color)
        scored.append(ColorMatch(name, color.to_hex(), dist))
    
    scored.sort(key=lambda x: x.distance)
    return scored[:n]


# ============ 颜色分类 ============

def get_color_category(rgb: RGB) -> str:
    """
    获取颜色的大类
    
    Args:
        rgb: RGB 颜色对象
    
    Returns:
        颜色类别：Red, Orange, Yellow, Green, Cyan, Blue, Purple, Pink, Black, White, Gray
    """
    hsl = rgb_to_hsl(rgb)
    
    # 处理无彩色（低饱和度）
    if hsl.s < 10:
        if hsl.l < 20:
            return "Black"
        elif hsl.l > 80:
            return "White"
        return "Gray"
    
    # 根据色相确定类别
    h = hsl.h
    
    if h < 15 or h >= 345:
        return "Red"
    elif h < 45:
        return "Orange"
    elif h < 70:
        return "Yellow"
    elif h < 165:
        return "Green"
    elif h < 195:
        return "Cyan"
    elif h < 255:
        return "Blue"
    elif h < 285:
        return "Purple"
    else:
        return "Pink"


def get_brightness(rgb: RGB) -> str:
    """
    获取颜色的亮度类别
    
    Args:
        rgb: RGB 颜色对象
    
    Returns:
        亮度类别：Dark, Medium, Light
    """
    luminance = 0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b
    
    if luminance < 60:
        return "Dark"
    elif luminance < 180:
        return "Medium"
    return "Light"


def get_temperature(rgb: RGB) -> str:
    """
    获取颜色的温度
    
    Args:
        rgb: RGB 颜色对象
    
    Returns:
        温度类别：Warm, Cool, Neutral
    """
    warmth = rgb.r - rgb.b
    
    if warmth > 40:
        return "Warm"
    elif warmth < -40:
        return "Cool"
    return "Neutral"


def get_color_info(rgb: RGB) -> ColorInfo:
    """
    获取颜色的完整信息
    
    Args:
        rgb: RGB 颜色对象
    
    Returns:
        ColorInfo 包含名称、十六进制、RGB、HSL、类别、亮度和温度
    """
    match = get_closest_color(rgb)
    hsl = rgb_to_hsl(rgb)
    
    return ColorInfo(
        name=match.name,
        hex=rgb.to_hex(),
        rgb=rgb,
        hsl=hsl,
        category=get_color_category(rgb),
        brightness=get_brightness(rgb),
        temperature=get_temperature(rgb)
    )


def get_color_info_hex(hex_color: str) -> ColorInfo:
    """从十六进制字符串获取颜色信息"""
    return get_color_info(parse_hex(hex_color))


# ============ 颜色判断 ============

def is_light_color(rgb: RGB) -> bool:
    """判断是否为亮色"""
    return get_brightness(rgb) == "Light"


def is_dark_color(rgb: RGB) -> bool:
    """判断是否为暗色"""
    return get_brightness(rgb) == "Dark"


def get_contrast_color(rgb: RGB) -> RGB:
    """
    获取对比色（黑或白）
    
    Args:
        rgb: RGB 颜色对象
    
    Returns:
        RGB(0,0,0) 或 RGB(255,255,255)
    """
    luminance = 0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b
    return RGB(0, 0, 0) if luminance > 128 else RGB(255, 255, 255)


def are_colors_similar(c1: RGB, c2: RGB, threshold: float = 20.0) -> bool:
    """
    判断两个颜色是否相似
    
    Args:
        c1: 第一个颜色
        c2: 第二个颜色
        threshold: 距离阈值
    
    Returns:
        是否相似
    """
    return color_distance(c1, c2) <= threshold


# ============ 颜色操作 ============

def blend_colors(c1: RGB, c2: RGB, ratio: float = 0.5) -> RGB:
    """
    混合两个颜色
    
    Args:
        c1: 第一个颜色
        c2: 第二个颜色
        ratio: 混合比例（0=c1, 1=c2）
    
    Returns:
        混合后的颜色
    """
    ratio = max(0, min(1, ratio))
    return RGB(
        int(round(c1.r * (1 - ratio) + c2.r * ratio)),
        int(round(c1.g * (1 - ratio) + c2.g * ratio)),
        int(round(c1.b * (1 - ratio) + c2.b * ratio))
    )


def lighten(rgb: RGB, amount: float = 10.0) -> RGB:
    """
    变亮颜色
    
    Args:
        rgb: RGB 颜色对象
        amount: 变亮程度（0-100）
    
    Returns:
        变亮后的颜色
    """
    hsl = rgb_to_hsl(rgb)
    hsl = HSL(hsl.h, hsl.s, min(100, hsl.l + amount))
    return hsl_to_rgb(hsl)


def darken(rgb: RGB, amount: float = 10.0) -> RGB:
    """
    变暗颜色
    
    Args:
        rgb: RGB 颜色对象
        amount: 变暗程度（0-100）
    
    Returns:
        变暗后的颜色
    """
    hsl = rgb_to_hsl(rgb)
    hsl = HSL(hsl.h, hsl.s, max(0, hsl.l - amount))
    return hsl_to_rgb(hsl)


def saturate(rgb: RGB, amount: float = 10.0) -> RGB:
    """增加饱和度"""
    hsl = rgb_to_hsl(rgb)
    hsl = HSL(hsl.h, min(100, hsl.s + amount), hsl.l)
    return hsl_to_rgb(hsl)


def desaturate(rgb: RGB, amount: float = 10.0) -> RGB:
    """降低饱和度"""
    hsl = rgb_to_hsl(rgb)
    hsl = HSL(hsl.h, max(0, hsl.s - amount), hsl.l)
    return hsl_to_rgb(hsl)


def complementary_color(rgb: RGB) -> RGB:
    """获取互补色"""
    hsl = rgb_to_hsl(rgb)
    hsl = HSL((hsl.h + 180) % 360, hsl.s, hsl.l)
    return hsl_to_rgb(hsl)


def analogous_colors(rgb: RGB) -> List[RGB]:
    """获取类似色（色轮上相邻的颜色）"""
    hsl = rgb_to_hsl(rgb)
    return [
        hsl_to_rgb(HSL((hsl.h - 30 + 360) % 360, hsl.s, hsl.l)),
        rgb,
        hsl_to_rgb(HSL((hsl.h + 30) % 360, hsl.s, hsl.l))
    ]


def triadic_colors(rgb: RGB) -> List[RGB]:
    """获取三角色（色轮上 120 度间隔）"""
    hsl = rgb_to_hsl(rgb)
    return [
        rgb,
        hsl_to_rgb(HSL((hsl.h + 120) % 360, hsl.s, hsl.l)),
        hsl_to_rgb(HSL((hsl.h + 240) % 360, hsl.s, hsl.l))
    ]


def split_complementary_colors(rgb: RGB) -> List[RGB]:
    """获取分裂互补色"""
    hsl = rgb_to_hsl(rgb)
    return [
        rgb,
        hsl_to_rgb(HSL((hsl.h + 150) % 360, hsl.s, hsl.l)),
        hsl_to_rgb(HSL((hsl.h + 210) % 360, hsl.s, hsl.l))
    ]


def tetradic_colors(rgb: RGB) -> List[RGB]:
    """获取四角色（色轮上 90 度间隔）"""
    hsl = rgb_to_hsl(rgb)
    return [
        rgb,
        hsl_to_rgb(HSL((hsl.h + 90) % 360, hsl.s, hsl.l)),
        hsl_to_rgb(HSL((hsl.h + 180) % 360, hsl.s, hsl.l)),
        hsl_to_rgb(HSL((hsl.h + 270) % 360, hsl.s, hsl.l))
    ]


def grayscale(rgb: RGB) -> RGB:
    """转换为灰度"""
    gray = int(0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b)
    return RGB(gray, gray, gray)


def sepia(rgb: RGB) -> RGB:
    """应用棕褐色调"""
    r = min(255, int(0.393 * rgb.r + 0.769 * rgb.g + 0.189 * rgb.b))
    g = min(255, int(0.349 * rgb.r + 0.686 * rgb.g + 0.168 * rgb.b))
    b = min(255, int(0.272 * rgb.r + 0.534 * rgb.g + 0.131 * rgb.b))
    return RGB(r, g, b)


def invert_color(rgb: RGB) -> RGB:
    """反转颜色"""
    return RGB(255 - rgb.r, 255 - rgb.g, 255 - rgb.b)


def adjust_brightness(rgb: RGB, factor: float) -> RGB:
    """
    调整亮度
    
    Args:
        rgb: RGB 颜色对象
        factor: 调整因子（-100 到 100）
    
    Returns:
        调整后的颜色
    """
    adjustment = factor * 2.55  # 转换到 0-255 范围
    return RGB(
        int(max(0, min(255, rgb.r + adjustment))),
        int(max(0, min(255, rgb.g + adjustment))),
        int(max(0, min(255, rgb.b + adjustment)))
    )


# ============ 数据库操作 ============

def get_color_by_name(name: str) -> Optional[RGB]:
    """
    根据名称获取颜色
    
    Args:
        name: 颜色名称
    
    Returns:
        RGB 对象或 None
    """
    name = name.lower().strip()
    for color_name, rgb in _COLOR_DATABASE:
        if color_name.lower() == name:
            return rgb
    return None


def get_all_color_names() -> List[str]:
    """获取所有颜色名称"""
    return [name for name, _ in _COLOR_DATABASE]


def get_colors_by_category(category: str) -> List[str]:
    """
    获取某个类别下的所有颜色名称
    
    Args:
        category: 颜色类别
    
    Returns:
        该类别下的颜色名称列表
    """
    category = category.lower().strip()
    result = []
    for name, rgb in _COLOR_DATABASE:
        if get_color_category(rgb).lower() == category:
            result.append(name)
    return result


def search_color_names(query: str) -> List[ColorMatch]:
    """
    搜索颜色名称
    
    Args:
        query: 搜索关键词
    
    Returns:
        匹配的颜色列表
    """
    query = query.lower().strip()
    result = []
    for name, rgb in _COLOR_DATABASE:
        if query in name.lower():
            result.append(ColorMatch(name, rgb.to_hex(), 0))
    return result


def color_count() -> int:
    """返回数据库中的颜色数量"""
    return len(_COLOR_DATABASE)


# ============ 随机颜色生成 ============

def random_color() -> RGB:
    """生成随机颜色"""
    return RGB(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def random_pastel_color() -> RGB:
    """生成随机柔和色"""
    return RGB(
        random.randint(128, 255),
        random.randint(128, 255),
        random.randint(128, 255)
    )


def random_dark_color() -> RGB:
    """生成随机暗色"""
    return RGB(
        random.randint(0, 100),
        random.randint(0, 100),
        random.randint(0, 100)
    )


def random_warm_color() -> RGB:
    """生成随机暖色（偏红/橙/黄）"""
    h = random.uniform(0, 60)
    s = random.uniform(50, 100)
    l = random.uniform(30, 70)
    return hsl_to_rgb(HSL(h, s, l))


def random_cool_color() -> RGB:
    """生成随机冷色（偏蓝/绿/紫）"""
    h = random.uniform(180, 300)
    s = random.uniform(50, 100)
    l = random.uniform(30, 70)
    return hsl_to_rgb(HSL(h, s, l))


# ============ 便捷函数 ============

def hex_to_rgb(hex_color: str) -> RGB:
    """十六进制转 RGB（parse_hex 的别名）"""
    return parse_hex(hex_color)


def rgb_string(rgb: RGB) -> str:
    """RGB 转字符串"""
    return f"rgb({rgb.r}, {rgb.g}, {rgb.b})"


def hsl_string(hsl: HSL) -> str:
    """HSL 转字符串"""
    return f"hsl({hsl.h:.1f}, {hsl.s:.1f}%, {hsl.l:.1f}%)"


if __name__ == "__main__":
    # 简单测试
    print("ColorName Utils 测试")
    print("=" * 50)
    
    # 测试十六进制解析
    red = parse_hex("#FF0000")
    print(f"解析 #FF0000: {red}")
    
    # 测试颜色名称查找
    print(f"#FF0000 最接近的名称: {get_color_name(red)}")
    
    # 测试颜色信息
    info = get_color_info(RGB(255, 165, 0))
    print(f"\n橙色信息:")
    print(f"  名称: {info.name}")
    print(f"  十六进制: {info.hex}")
    print(f"  类别: {info.category}")
    print(f"  亮度: {info.brightness}")
    print(f"  温度: {info.temperature}")
    
    # 测试颜色操作
    print(f"\n互补色测试:")
    blue = RGB(0, 0, 255)
    print(f"  蓝色 {blue.to_hex()} 的互补色: {complementary_color(blue).to_hex()}")
    
    # 测试最近颜色
    print(f"\n最近颜色测试:")
    matches = get_n_closest_colors(RGB(255, 100, 50), 5)
    for m in matches:
        print(f"  {m.name}: {m.hex} (距离: {m.distance:.2f})")
    
    print(f"\n数据库中共有 {color_count()} 种颜色")