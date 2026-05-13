"""
Color Theory Utils - 颜色理论工具库

零依赖的颜色理论库，支持：
- 多种颜色空间转换（RGB, HSL, HSV, CMYK, HEX, LAB）
- 颜色和谐方案（互补色、类似色、三角色、四角色、分裂互补色）
- WCAG 对比度计算与可访问性检查
- 颜色混合与渐变生成
- 色温计算（暖色/冷色）
- 调色板生成（随机、基于规则）
- 颜色命名与匹配

Author: AllToolkit
License: MIT
"""

from typing import Tuple, List, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum
import math
import random


class ColorSpace(Enum):
    """颜色空间类型"""
    RGB = "rgb"
    HSL = "hsl"
    HSV = "hsv"
    CMYK = "cmyk"
    LAB = "lab"
    HEX = "hex"


class HarmonyType(Enum):
    """颜色和谐类型"""
    COMPLEMENTARY = "complementary"          # 互补色
    ANALOGOUS = "analogous"                  # 类似色
    TRIADIC = "triadic"                      # 三角色
    TETRADIC = "tetradic"                    # 四角色
    SPLIT_COMPLEMENTARY = "split_complementary"  # 分裂互补色
    SQUARE = "square"                        # 方形配色
    COMPOUND = "compound"                    # 复合配色


class WCAGLevel(Enum):
    """WCAG 对比度等级"""
    FAIL = "fail"           # < 3:1
    AA_LARGE = "aa_large"   # >= 3:1 (大文本)
    AA = "aa"               # >= 4.5:1
    AAA = "aaa"             # >= 7:1


class ColorTemperature(Enum):
    """色温类型"""
    WARM = "warm"           # 暖色 (红、橙、黄)
    NEUTRAL = "neutral"     # 中性色
    COOL = "cool"           # 冷色 (蓝、绿、紫)


@dataclass
class RGB:
    """RGB 颜色"""
    r: int  # 0-255
    g: int  # 0-255
    b: int  # 0-255
    
    def __post_init__(self):
        self.r = max(0, min(255, int(self.r)))
        self.g = max(0, min(255, int(self.g)))
        self.b = max(0, min(255, int(self.b)))
    
    def to_hex(self) -> str:
        """转换为 HEX 格式"""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    def to_hsl(self) -> 'HSL':
        """转换为 HSL"""
        r, g, b = self.r / 255, self.g / 255, self.b / 255
        max_c, min_c = max(r, g, b), min(r, g, b)
        l = (max_c + min_c) / 2
        
        if max_c == min_c:
            h = s = 0
        else:
            d = max_c - min_c
            s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
            
            if max_c == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_c == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4
            h /= 6
        
        return HSL(h=int(h * 360), s=int(s * 100), l=int(l * 100))
    
    def to_hsv(self) -> 'HSV':
        """转换为 HSV"""
        r, g, b = self.r / 255, self.g / 255, self.b / 255
        max_c, min_c = max(r, g, b), min(r, g, b)
        v = max_c
        
        if max_c == min_c:
            h = s = 0
        else:
            d = max_c - min_c
            s = d / max_c
            
            if max_c == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_c == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4
            h /= 6
        
        return HSV(h=int(h * 360), s=int(s * 100), v=int(v * 100))
    
    def to_cmyk(self) -> 'CMYK':
        """转换为 CMYK"""
        if self.r == 0 and self.g == 0 and self.b == 0:
            return CMYK(c=0, m=0, y=0, k=100)
        
        r, g, b = self.r / 255, self.g / 255, self.b / 255
        k = 1 - max(r, g, b)
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
        
        return CMYK(
            c=int(c * 100), m=int(m * 100),
            y=int(y * 100), k=int(k * 100)
        )
    
    def to_lab(self) -> 'LAB':
        """转换为 LAB 颜色空间"""
        # 先转换到 XYZ
        r = self.r / 255
        g = self.g / 255
        b = self.b / 255
        
        # Gamma 校正
        r = r if r > 0.04045 else r / 12.92
        g = g if g > 0.04045 else g / 12.92
        b = b if b > 0.04045 else b / 12.92
        
        r = ((r + 0.055) / 1.055) ** 2.4 if r > 0.04045 else r
        g = ((g + 0.055) / 1.055) ** 2.4 if g > 0.04045 else g
        b = ((b + 0.055) / 1.055) ** 2.4 if b > 0.04045 else b
        
        r, g, b = r * 100, g * 100, b * 100
        
        # RGB -> XYZ (D65 白点)
        x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
        y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
        z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
        
        # XYZ -> LAB
        x /= 95.047
        y /= 100.0
        z /= 108.883
        
        def f(t):
            return t ** (1/3) if t > 0.008856 else (7.787 * t) + (16 / 116)
        
        L = (116 * f(y)) - 16
        a = 500 * (f(x) - f(y))
        b_val = 200 * (f(y) - f(z))
        
        return LAB(L=round(L, 2), a=round(a, 2), b=round(b_val, 2))
    
    def get_luminance(self) -> float:
        """计算相对亮度（0-1）"""
        r = self.r / 255
        g = self.g / 255
        b = self.b / 255
        
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    def get_temperature(self) -> ColorTemperature:
        """获取颜色温度"""
        hsl = self.to_hsl()
        h = hsl.h
        
        # 暖色: 0-60 (红到黄) 和 300-360 (红紫)
        # 冷色: 120-240 (绿到蓝)
        # 中性: 60-120 (黄绿) 和 240-300 (蓝紫)
        
        if (0 <= h <= 60) or (h >= 300):
            return ColorTemperature.WARM
        elif 120 <= h <= 240:
            return ColorTemperature.COOL
        else:
            # 边界区域，根据饱和度和亮度判断
            s, l = hsl.s, hsl.l
            if s < 20 or l < 20 or l > 80:
                return ColorTemperature.NEUTRAL
            if 60 < h < 90:
                return ColorTemperature.WARM  # 偏暖的黄绿
            else:
                return ColorTemperature.COOL  # 偏冷的蓝紫
    
    def is_light(self) -> bool:
        """判断是否为浅色"""
        hsl = self.to_hsl()
        return hsl.l > 50
    
    def __repr__(self) -> str:
        return f"RGB({self.r}, {self.g}, {self.b})"


@dataclass
class HSL:
    """HSL 颜色"""
    h: int  # 0-360 色相
    s: int  # 0-100 饱和度
    l: int  # 0-100 亮度
    
    def __post_init__(self):
        self.h = self.h % 360
        self.s = max(0, min(100, int(self.s)))
        self.l = max(0, min(100, int(self.l)))
    
    def to_rgb(self) -> RGB:
        """转换为 RGB"""
        h, s, l = self.h / 360, self.s / 100, self.l / 100
        
        if s == 0:
            v = int(l * 255)
            return RGB(r=v, g=v, b=v)
        
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
        
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)
        
        return RGB(r=int(r * 255), g=int(g * 255), b=int(b * 255))
    
    def to_hex(self) -> str:
        return self.to_rgb().to_hex()
    
    def __repr__(self) -> str:
        return f"HSL({self.h}°, {self.s}%, {self.l}%)"


@dataclass
class HSV:
    """HSV 颜色"""
    h: int  # 0-360 色相
    s: int  # 0-100 饱和度
    v: int  # 0-100 明度
    
    def __post_init__(self):
        self.h = self.h % 360
        self.s = max(0, min(100, int(self.s)))
        self.v = max(0, min(100, int(self.v)))
    
    def to_rgb(self) -> RGB:
        """转换为 RGB"""
        h, s, v = self.h / 360, self.s / 100, self.v / 100
        
        i = int(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        
        i %= 6
        
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
        
        return RGB(r=int(r * 255), g=int(g * 255), b=int(b * 255))
    
    def to_hex(self) -> str:
        return self.to_rgb().to_hex()
    
    def __repr__(self) -> str:
        return f"HSV({self.h}°, {self.s}%, {self.v}%)"


@dataclass
class CMYK:
    """CMYK 颜色"""
    c: int  # 0-100 青色
    m: int  # 0-100 品红
    y: int  # 0-100 黄色
    k: int  # 0-100 黑色
    
    def __post_init__(self):
        self.c = max(0, min(100, int(self.c)))
        self.m = max(0, min(100, int(self.m)))
        self.y = max(0, min(100, int(self.y)))
        self.k = max(0, min(100, int(self.k)))
    
    def to_rgb(self) -> RGB:
        """转换为 RGB"""
        c, m, y, k = self.c / 100, self.m / 100, self.y / 100, self.k / 100
        
        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)
        
        return RGB(r=int(r), g=int(g), b=int(b))
    
    def to_hex(self) -> str:
        return self.to_rgb().to_hex()
    
    def __repr__(self) -> str:
        return f"CMYK({self.c}%, {self.m}%, {self.y}%, {self.k}%)"


@dataclass
class LAB:
    """LAB 颜色空间"""
    L: float  # 0-100 亮度
    a: float  # -128 to 127 绿到红
    b: float  # -128 to 127 蓝到黄
    
    def __post_init__(self):
        self.L = max(0, min(100, self.L))
        self.a = max(-128, min(127, self.a))
        self.b = max(-128, min(127, self.b))
    
    def to_rgb(self) -> RGB:
        """转换为 RGB"""
        # LAB -> XYZ
        y = (self.L + 16) / 116
        x = self.a / 500 + y
        z = y - self.b / 200
        
        def f(t):
            delta = 6/29
            if t > delta:
                return t ** 3
            else:
                return 3 * delta ** 2 * (t - 4/29)
        
        x = f(x)
        y = f(y)
        z = f(z)
        
        # D65 白点
        x *= 95.047
        y *= 100.0
        z *= 108.883
        
        # XYZ -> RGB (使用标准转换矩阵)
        # | R |   |  3.2404542  -1.5371385  -0.4985314 |   | X |
        # | G | = | -0.9692660   1.8760108   0.0415560 | * | Y |
        # | B |   |  0.0556434  -0.2040259   1.0572252 |   | Z |
        r = (x * 3.2404542 - y * 1.5371385 - z * 0.4985314) / 100
        g = (-x * 0.9692660 + y * 1.8760108 + z * 0.0415560) / 100
        b = (x * 0.0556434 - y * 0.2040259 + z * 1.0572252) / 100
        
        # Gamma 校正 (sRGB)
        def gamma(t):
            if t <= 0.0031308:
                return t * 12.92
            return 1.055 * (t ** (1/2.4)) - 0.055
        
        r = gamma(max(0, r))
        g = gamma(max(0, g))
        b = gamma(max(0, b))
        
        return RGB(
            r=max(0, min(255, int(r * 255))),
            g=max(0, min(255, int(g * 255))),
            b=max(0, min(255, int(b * 255)))
        )
    
    def to_hex(self) -> str:
        return self.to_rgb().to_hex()
    
    def __repr__(self) -> str:
        return f"LAB(L={self.L:.1f}, a={self.a:.1f}, b={self.b:.1f})"


# ============ 工具函数 ============

def hex_to_rgb(hex_color: str) -> RGB:
    """
    将 HEX 颜色转换为 RGB
    
    Args:
        hex_color: 十六进制颜色，如 '#ff0000' 或 'ff0000'
    
    Returns:
        RGB 对象
    
    Example:
        >>> hex_to_rgb('#ff0000')
        RGB(255, 0, 0)
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c * 2 for c in hex_color])
    
    return RGB(
        r=int(hex_color[0:2], 16),
        g=int(hex_color[2:4], 16),
        b=int(hex_color[4:6], 16)
    )


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """RGB 转 HEX"""
    return RGB(r, g, b).to_hex()


def get_harmony(color: Union[str, RGB, HSL], harmony_type: HarmonyType) -> List[RGB]:
    """
    获取颜色的和谐配色方案
    
    Args:
        color: 输入颜色（HEX 字符串、RGB 或 HSL 对象）
        harmony_type: 和谐类型
    
    Returns:
        和谐配色列表（包含原色）
    
    Example:
        >>> get_harmony('#ff0000', HarmonyType.COMPLEMENTARY)
        [RGB(255, 0, 0), RGB(0, 255, 255)]
    """
    # 统一转换为 HSL
    if isinstance(color, str):
        color = hex_to_rgb(color)
    
    if isinstance(color, RGB):
        hsl = color.to_hsl()
    else:
        hsl = color
    
    h = hsl.h
    
    if harmony_type == HarmonyType.COMPLEMENTARY:
        # 互补色（180° 相对）
        angles = [0, 180]
    elif harmony_type == HarmonyType.ANALOGOUS:
        # 类似色（相邻 30°）
        angles = [-30, 0, 30]
    elif harmony_type == HarmonyType.TRIADIC:
        # 三角色（120° 间隔）
        angles = [0, 120, 240]
    elif harmony_type == HarmonyType.TETRADIC:
        # 四角色（90° 间隔）
        angles = [0, 90, 180, 270]
    elif harmony_type == HarmonyType.SPLIT_COMPLEMENTARY:
        # 分裂互补色（±150°）
        angles = [0, 150, 210]
    elif harmony_type == HarmonyType.SQUARE:
        # 方形配色（90° 间隔）
        angles = [0, 90, 180, 270]
    elif harmony_type == HarmonyType.COMPOUND:
        # 复合配色
        angles = [0, 60, 180, 240]
    else:
        angles = [0]
    
    colors = []
    for angle in angles:
        new_h = (h + angle) % 360
        new_hsl = HSL(h=new_h, s=hsl.s, l=hsl.l)
        colors.append(new_hsl.to_rgb())
    
    return colors


def get_contrast_ratio(color1: RGB, color2: RGB) -> float:
    """
    计算两个颜色之间的对比度（WCAG 标准）
    
    Args:
        color1: 第一个颜色
        color2: 第二个颜色
    
    Returns:
        对比度比值（1:1 到 21:1）
    
    Example:
        >>> get_contrast_ratio(RGB(255, 255, 255), RGB(0, 0, 0))
        21.0
    """
    l1 = color1.get_luminance()
    l2 = color2.get_luminance()
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


def get_wcag_level(contrast_ratio: float) -> WCAGLevel:
    """
    根据对比度判断 WCAG 等级
    
    Args:
        contrast_ratio: 对比度比值
    
    Returns:
        WCAGLevel 枚举值
    """
    if contrast_ratio >= 7:
        return WCAGLevel.AAA
    elif contrast_ratio >= 4.5:
        return WCAGLevel.AA
    elif contrast_ratio >= 3:
        return WCAGLevel.AA_LARGE
    else:
        return WCAGLevel.FAIL


def is_accessible(foreground: RGB, background: RGB, level: WCAGLevel = WCAGLevel.AA) -> bool:
    """
    检查颜色组合是否满足 WCAG 可访问性要求
    
    Args:
        foreground: 前景色
        background: 背景色
        level: 目标 WCAG 等级
    
    Returns:
        是否满足要求
    """
    ratio = get_contrast_ratio(foreground, background)
    current_level = get_wcag_level(ratio)
    
    levels = [WCAGLevel.FAIL, WCAGLevel.AA_LARGE, WCAGLevel.AA, WCAGLevel.AAA]
    return levels.index(current_level) >= levels.index(level)


def mix_colors(color1: RGB, color2: RGB, ratio: float = 0.5) -> RGB:
    """
    混合两个颜色
    
    Args:
        color1: 第一个颜色
        color2: 第二个颜色
        ratio: 混合比例（0.0 = 全 color1, 1.0 = 全 color2）
    
    Returns:
        混合后的颜色
    
    Example:
        >>> mix_colors(RGB(255, 0, 0), RGB(0, 0, 255), 0.5)
        RGB(128, 0, 128)
    """
    ratio = max(0, min(1, ratio))
    
    r = int(color1.r * (1 - ratio) + color2.r * ratio)
    g = int(color1.g * (1 - ratio) + color2.g * ratio)
    b = int(color1.b * (1 - ratio) + color2.b * ratio)
    
    return RGB(r=r, g=g, b=b)


def generate_gradient(start_color: RGB, end_color: RGB, steps: int) -> List[RGB]:
    """
    生成两个颜色之间的渐变
    
    Args:
        start_color: 起始颜色
        end_color: 结束颜色
        steps: 渐变步数
    
    Returns:
        颜色列表
    
    Example:
        >>> gradient = generate_gradient(RGB(255, 0, 0), RGB(0, 0, 255), 5)
        >>> [c.to_hex() for c in gradient]
        ['#ff0000', '#bf003f', '#7f007f', '#3f00bf', '#0000ff']
    """
    if steps < 2:
        return [start_color]
    
    return [
        mix_colors(start_color, end_color, i / (steps - 1))
        for i in range(steps)
    ]


def lighten(color: RGB, amount: int = 10) -> RGB:
    """
    使颜色变亮
    
    Args:
        color: 输入颜色
        amount: 变亮量（0-100）
    
    Returns:
        变亮后的颜色
    """
    hsl = color.to_hsl()
    new_l = min(100, hsl.l + amount)
    return HSL(h=hsl.h, s=hsl.s, l=new_l).to_rgb()


def darken(color: RGB, amount: int = 10) -> RGB:
    """
    使颜色变暗
    
    Args:
        color: 输入颜色
        amount: 变暗量（0-100）
    
    Returns:
        变暗后的颜色
    """
    hsl = color.to_hsl()
    new_l = max(0, hsl.l - amount)
    return HSL(h=hsl.h, s=hsl.s, l=new_l).to_rgb()


def saturate(color: RGB, amount: int = 10) -> RGB:
    """
    增加颜色饱和度
    
    Args:
        color: 输入颜色
        amount: 增加量（0-100）
    
    Returns:
        增加饱和度后的颜色
    """
    hsl = color.to_hsl()
    new_s = min(100, hsl.s + amount)
    return HSL(h=hsl.h, s=new_s, l=hsl.l).to_rgb()


def desaturate(color: RGB, amount: int = 10) -> RGB:
    """
    降低颜色饱和度
    
    Args:
        color: 输入颜色
        amount: 降低量（0-100）
    
    Returns:
        降低饱和度后的颜色
    """
    hsl = color.to_hsl()
    new_s = max(0, hsl.s - amount)
    return HSL(h=hsl.h, s=new_s, l=hsl.l).to_rgb()


def get_complementary(color: RGB) -> RGB:
    """获取互补色"""
    harmonies = get_harmony(color, HarmonyType.COMPLEMENTARY)
    return harmonies[1]


def get_analogous(color: RGB) -> List[RGB]:
    """获取类似色（相邻色）"""
    return get_harmony(color, HarmonyType.ANALOGOUS)


def get_triadic(color: RGB) -> List[RGB]:
    """获取三角色"""
    return get_harmony(color, HarmonyType.TRIADIC)


def get_tetradic(color: RGB) -> List[RGB]:
    """获取四角色"""
    return get_harmony(color, HarmonyType.TETRADIC)


def random_color() -> RGB:
    """生成随机颜色"""
    return RGB(
        r=random.randint(0, 255),
        g=random.randint(0, 255),
        b=random.randint(0, 255)
    )


def random_hue(hue_range: Tuple[int, int] = (0, 360),
               saturation_range: Tuple[int, int] = (50, 100),
               lightness_range: Tuple[int, int] = (30, 70)) -> RGB:
    """
    在指定范围内生成随机颜色
    
    Args:
        hue_range: 色相范围（0-360）
        saturation_range: 饱和度范围（0-100）
        lightness_range: 亮度范围（0-100）
    
    Returns:
        RGB 颜色对象
    """
    h = random.randint(*hue_range) % 360
    s = random.randint(*saturation_range)
    s = max(0, min(100, s))
    l = random.randint(*lightness_range)
    l = max(0, min(100, l))
    
    return HSL(h=h, s=s, l=l).to_rgb()


def generate_palette(base_color: RGB, 
                     variations: int = 5,
                     include_shades: bool = True,
                     include_tints: bool = True,
                     include_tones: bool = True) -> List[RGB]:
    """
    基于基准色生成调色板
    
    Args:
        base_color: 基准颜色
        variations: 每种变体数量
        include_shades: 包含暗色调
        include_tints: 包含亮色调
        include_tones: 包含灰色调
    
    Returns:
        颜色列表
    """
    palette = [base_color]
    
    if include_shades:
        for i in range(1, variations + 1):
            amount = int(80 / variations) * i
            palette.append(darken(base_color, amount))
    
    if include_tints:
        for i in range(1, variations + 1):
            amount = int(80 / variations) * i
            palette.append(lighten(base_color, amount))
    
    if include_tones:
        for i in range(1, variations + 1):
            amount = int(80 / variations) * i
            palette.append(desaturate(base_color, amount))
    
    return palette


def color_distance(color1: RGB, color2: RGB) -> float:
    """
    计算两个颜色之间的欧几里得距离
    
    Args:
        color1: 第一个颜色
        color2: 第二个颜色
    
    Returns:
        距离值（0-441.67，0 表示完全相同）
    """
    return math.sqrt(
        (color1.r - color2.r) ** 2 +
        (color1.g - color2.g) ** 2 +
        (color1.b - color2.b) ** 2
    )


def lab_distance(color1: RGB, color2: RGB) -> float:
    """
    计算 LAB 空间中的颜色距离（更符合人眼感知）
    
    Args:
        color1: 第一个颜色
        color2: 第二个颜色
    
    Returns:
        LAB 距离值
    """
    lab1 = color1.to_lab()
    lab2 = color2.to_lab()
    
    return math.sqrt(
        (lab1.L - lab2.L) ** 2 +
        (lab1.a - lab2.a) ** 2 +
        (lab1.b - lab2.b) ** 2
    )


def find_closest_color(target: RGB, colors: List[RGB], use_lab: bool = False) -> RGB:
    """
    在颜色列表中找到最接近的颜色
    
    Args:
        target: 目标颜色
        colors: 候选颜色列表
        use_lab: 是否使用 LAB 空间计算距离
    
    Returns:
        最接近的颜色
    """
    distance_func = lab_distance if use_lab else color_distance
    return min(colors, key=lambda c: distance_func(target, c))


# 常用颜色名称映射
COLOR_NAMES = {
    '#000000': 'Black',
    '#FFFFFF': 'White',
    '#FF0000': 'Red',
    '#00FF00': 'Lime',
    '#0000FF': 'Blue',
    '#FFFF00': 'Yellow',
    '#00FFFF': 'Cyan',
    '#FF00FF': 'Magenta',
    '#808080': 'Gray',
    '#C0C0C0': 'Silver',
    '#800000': 'Maroon',
    '#808000': 'Olive',
    '#008000': 'Green',
    '#800080': 'Purple',
    '#008080': 'Teal',
    '#000080': 'Navy',
    '#FFA500': 'Orange',
    '#FFC0CB': 'Pink',
    '#A52A2A': 'Brown',
    '#FFD700': 'Gold',
    '#4B0082': 'Indigo',
    '#F5F5DC': 'Beige',
    '#FA8072': 'Salmon',
    '#7FFFD4': 'Aquamarine',
    '#DDA0DD': 'Plum',
    '#FF6347': 'Tomato',
    '#9370DB': 'MediumPurple',
    '#32CD32': 'LimeGreen',
    '#FF1493': 'DeepPink',
    '#1E90FF': 'DodgerBlue',
}


def get_color_name(color: RGB) -> str:
    """
    获取颜色名称（如果匹配已知颜色）
    
    Args:
        color: 输入颜色
    
    Returns:
        颜色名称或 HEX 值
    """
    hex_color = color.to_hex().upper()
    
    if hex_color in COLOR_NAMES:
        return COLOR_NAMES[hex_color]
    
    # 查找最接近的颜色
    closest_hex = min(
        COLOR_NAMES.keys(),
        key=lambda h: color_distance(color, hex_to_rgb(h))
    )
    
    closest_distance = color_distance(color, hex_to_rgb(closest_hex))
    
    # 如果距离很近，返回近似名称
    if closest_distance < 30:
        return f"~{COLOR_NAMES[closest_hex]}"
    
    return hex_color


def adjust_brightness(color: RGB, factor: float) -> RGB:
    """
    调整颜色亮度
    
    Args:
        color: 输入颜色
        factor: 亮度因子（> 1 变亮，< 1 变暗）
    
    Returns:
        调整后的颜色
    """
    hsl = color.to_hsl()
    new_l = min(100, max(0, hsl.l * factor))
    return HSL(h=hsl.h, s=hsl.s, l=int(new_l)).to_rgb()


def invert_color(color: RGB) -> RGB:
    """
    获取反色
    
    Args:
        color: 输入颜色
    
    Returns:
        反色
    """
    return RGB(r=255 - color.r, g=255 - color.g, b=255 - color.b)


def grayscale(color: RGB) -> RGB:
    """
    转换为灰度色
    
    Args:
        color: 输入颜色
    
    Returns:
        灰度色
    """
    # 使用加权平均（人眼对绿色最敏感）
    gray = int(0.299 * color.r + 0.587 * color.g + 0.114 * color.b)
    return RGB(r=gray, g=gray, b=gray)


def sepia(color: RGB) -> RGB:
    """
    应用怀旧棕褐色滤镜
    
    Args:
        color: 输入颜色
    
    Returns:
        棕褐色调颜色
    """
    r = min(255, int(0.393 * color.r + 0.769 * color.g + 0.189 * color.b))
    g = min(255, int(0.349 * color.r + 0.686 * color.g + 0.168 * color.b))
    b = min(255, int(0.272 * color.r + 0.534 * color.g + 0.131 * color.b))
    return RGB(r=r, g=g, b=b)


def get_accessible_color(background: RGB, prefer_light: bool = True) -> RGB:
    """
    获取与背景形成良好对比的前景色
    
    Args:
        background: 背景色
        prefer_light: 是否优先选择浅色前景
    
    Returns:
        适合的前景色（黑色或白色）
    """
    white = RGB(255, 255, 255)
    black = RGB(0, 0, 0)
    
    white_contrast = get_contrast_ratio(white, background)
    black_contrast = get_contrast_ratio(black, background)
    
    if prefer_light:
        return white if white_contrast >= black_contrast else black
    else:
        return black if black_contrast >= 4.5 else white


def generate_random_palette(count: int = 5, 
                           harmony: Optional[HarmonyType] = None) -> List[RGB]:
    """
    生成随机调色板
    
    Args:
        count: 颜色数量
        harmony: 可选的和谐类型（如果指定，则基于一个随机色生成和谐色）
    
    Returns:
        颜色列表
    """
    if harmony:
        base = random_color()
        harmonies = get_harmony(base, harmony)
        
        if len(harmonies) >= count:
            return harmonies[:count]
        
        # 补充随机色
        result = harmonies.copy()
        while len(result) < count:
            result.append(random_color())
        return result
    
    return [random_color() for _ in range(count)]


def interpolate_colors(colors: List[RGB], steps: int) -> List[RGB]:
    """
    在多个颜色之间生成平滑渐变
    
    Args:
        colors: 颜色列表
        steps: 总步数
    
    Returns:
        渐变颜色列表
    """
    if len(colors) < 2:
        return colors * steps
    
    result = []
    segment_steps = steps // (len(colors) - 1)
    extra = steps % (len(colors) - 1)
    
    for i in range(len(colors) - 1):
        current_steps = segment_steps
        if i < extra:
            current_steps += 1
        
        gradient = generate_gradient(colors[i], colors[i + 1], current_steps + 1)
        result.extend(gradient[:-1] if i < len(colors) - 2 else gradient)
    
    return result


# ============ 高级功能 ============

def suggest_text_color(background: RGB, 
                       wcag_level: WCAGLevel = WCAGLevel.AA) -> Dict[str, any]:
    """
    建议适合背景的文字颜色
    
    Args:
        background: 背景色
        wcag_level: 目标 WCAG 等级
    
    Returns:
        包含建议颜色和对比度信息的字典
    """
    white = RGB(255, 255, 255)
    black = RGB(0, 0, 0)
    
    white_contrast = get_contrast_ratio(white, background)
    black_contrast = get_contrast_ratio(black, background)
    
    white_level = get_wcag_level(white_contrast)
    black_level = get_wcag_level(black_contrast)
    
    levels = [WCAGLevel.FAIL, WCAGLevel.AA_LARGE, WCAGLevel.AA, WCAGLevel.AAA]
    target_idx = levels.index(wcag_level)
    
    if levels.index(white_level) >= target_idx and white_contrast >= black_contrast:
        recommended = white
        contrast = white_contrast
    elif levels.index(black_level) >= target_idx:
        recommended = black
        contrast = black_contrast
    elif white_contrast > black_contrast:
        recommended = white
        contrast = white_contrast
    else:
        recommended = black
        contrast = black_contrast
    
    return {
        'recommended': recommended,
        'contrast_ratio': round(contrast, 2),
        'wcag_level': get_wcag_level(contrast).value,
        'meets_target': levels.index(get_wcag_level(contrast)) >= target_idx,
        'white_contrast': round(white_contrast, 2),
        'black_contrast': round(black_contrast, 2),
    }


def create_color_scheme(base_color: RGB, 
                        include_neutrals: bool = True) -> Dict[str, List[RGB]]:
    """
    创建完整的配色方案
    
    Args:
        base_color: 基准颜色
        include_neutrals: 是否包含中性色
    
    Returns:
        包含各种变体的配色方案字典
    """
    scheme = {
        'primary': [base_color],
        'complementary': get_harmony(base_color, HarmonyType.COMPLEMENTARY),
        'analogous': get_harmony(base_color, HarmonyType.ANALOGOUS),
        'triadic': get_harmony(base_color, HarmonyType.TRIADIC),
        'shades': [darken(base_color, i * 10) for i in range(1, 6)],
        'tints': [lighten(base_color, i * 10) for i in range(1, 6)],
        'tones': [desaturate(base_color, i * 10) for i in range(1, 6)],
    }
    
    if include_neutrals:
        scheme['neutrals'] = [
            RGB(255, 255, 255),  # White
            RGB(245, 245, 245),  # Light gray
            RGB(189, 189, 189),  # Medium gray
            RGB(115, 115, 115),  # Dark gray
            RGB(66, 66, 66),     # Charcoal
            RGB(33, 33, 33),     # Near black
            RGB(0, 0, 0),        # Black
        ]
    
    return scheme


def analyze_color(color: RGB) -> Dict[str, any]:
    """
    全面分析一个颜色
    
    Args:
        color: 要分析的颜色
    
    Returns:
        包含各种颜色信息的字典
    """
    hsl = color.to_hsl()
    hsv = color.to_hsv()
    cmyk = color.to_cmyk()
    lab = color.to_lab()
    
    # 确定色相类别
    h = hsl.h
    if h < 15 or h >= 345:
        hue_name = '红色'
    elif h < 45:
        hue_name = '橙色'
    elif h < 75:
        hue_name = '黄色'
    elif h < 150:
        hue_name = '绿色'
    elif h < 195:
        hue_name = '青色'
    elif h < 255:
        hue_name = '蓝色'
    elif h < 285:
        hue_name = '紫色'
    elif h < 345:
        hue_name = '品红'
    else:
        hue_name = '红色'
    
    # 饱和度类别
    if hsl.s < 10:
        saturation_name = '灰色'
    elif hsl.s < 30:
        saturation_name = '低饱和'
    elif hsl.s < 60:
        saturation_name = '中等饱和'
    elif hsl.s < 85:
        saturation_name = '高饱和'
    else:
        saturation_name = '鲜艳'
    
    # 亮度类别
    if hsl.l < 20:
        lightness_name = '极暗'
    elif hsl.l < 40:
        lightness_name = '暗'
    elif hsl.l < 60:
        lightness_name = '中等亮度'
    elif hsl.l < 80:
        lightness_name = '亮'
    else:
        lightness_name = '极亮'
    
    return {
        'hex': color.to_hex(),
        'name': get_color_name(color),
        'rgb': {'r': color.r, 'g': color.g, 'b': color.b},
        'hsl': {'h': hsl.h, 's': hsl.s, 'l': hsl.l},
        'hsv': {'h': hsv.h, 's': hsv.s, 'v': hsv.v},
        'cmyk': {'c': cmyk.c, 'm': cmyk.m, 'y': cmyk.y, 'k': cmyk.k},
        'lab': {'L': lab.L, 'a': lab.a, 'b': lab.b},
        'temperature': color.get_temperature().value,
        'is_light': color.is_light(),
        'luminance': round(color.get_luminance(), 4),
        'categories': {
            'hue': hue_name,
            'saturation': saturation_name,
            'lightness': lightness_name,
        },
        'text_suggestion': suggest_text_color(color),
    }