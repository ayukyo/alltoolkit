"""
Color Palette Utils - 颜色调色板工具集

完整的颜色操作工具，零外部依赖。

功能:
- 颜色空间转换 (RGB, HSL, HSV, HEX, CMYK, LAB)
- 调色板生成 (互补色、类似色、三色、四色等)
- 渐变色生成
- 对比度计算 (WCAG 标准)
- 色盲模拟
- 色彩和谐度分析

Author: AllToolkit
Version: 1.0.0
License: MIT
"""

import math
import random
import colorsys
from typing import List, Tuple, Optional, Union, Dict
from dataclasses import dataclass
from enum import Enum


class ColorSpace(Enum):
    """颜色空间类型"""
    RGB = "rgb"
    HSL = "hsl"
    HSV = "hsv"
    HEX = "hex"
    CMYK = "cmyk"
    LAB = "lab"


@dataclass
class RGB:
    """RGB 颜色表示"""
    r: int  # 0-255
    g: int  # 0-255
    b: int  # 0-255
    a: float = 1.0  # 0.0-1.0
    
    def __post_init__(self):
        self.r = max(0, min(255, int(self.r)))
        self.g = max(0, min(255, int(self.g)))
        self.b = max(0, min(255, int(self.b)))
        self.a = max(0.0, min(1.0, float(self.a)))
    
    def to_hex(self, include_alpha: bool = False) -> str:
        """转换为 HEX 格式"""
        if include_alpha:
            return f"#{self.r:02x}{self.g:02x}{self.b:02x}{int(self.a * 255):02x}"
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    def to_hsl(self) -> 'HSL':
        """转换为 HSL"""
        r, g, b = self.r / 255.0, self.g / 255.0, self.b / 255.0
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return HSL(h * 360, s * 100, l * 100, self.a)
    
    def to_hsv(self) -> 'HSV':
        """转换为 HSV"""
        r, g, b = self.r / 255.0, self.g / 255.0, self.b / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return HSV(h * 360, s * 100, v * 100, self.a)
    
    def to_cmyk(self) -> 'CMYK':
        """转换为 CMYK"""
        if self.r == 0 and self.g == 0 and self.b == 0:
            return CMYK(0, 0, 0, 100)
        
        r, g, b = self.r / 255.0, self.g / 255.0, self.b / 255.0
        k = 1 - max(r, g, b)
        c = (1 - r - k) / (1 - k) if k < 1 else 0
        m = (1 - g - k) / (1 - k) if k < 1 else 0
        y = (1 - b - k) / (1 - k) if k < 1 else 0
        
        return CMYK(c * 100, m * 100, y * 100, k * 100)
    
    def to_lab(self) -> 'LAB':
        """转换为 LAB 颜色空间"""
        # First convert RGB to XYZ
        r, g, b = self.r / 255.0, self.g / 255.0, self.b / 255.0
        
        # Gamma correction
        r = r / 12.92 if r <= 0.04045 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.04045 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.04045 else ((b + 0.055) / 1.055) ** 2.4
        
        # RGB to XYZ (D65 illuminant)
        x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
        y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
        z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
        
        # XYZ to LAB
        # Reference white D65
        x_ref, y_ref, z_ref = 0.95047, 1.0, 1.08883
        
        x /= x_ref
        y /= y_ref
        z /= z_ref
        
        def f(t):
            return t ** (1/3) if t > 0.008856 else (7.787 * t) + (16 / 116)
        
        L = (116 * f(y)) - 16
        a = 500 * (f(x) - f(y))
        b_val = 200 * (f(y) - f(z))
        
        return LAB(L, a, b_val, self.a)
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """返回 RGB 元组"""
        return (self.r, self.g, self.b)
    
    def luminance(self) -> float:
        """计算相对亮度 (0.0-1.0)"""
        r = self.r / 255.0
        g = self.g / 255.0
        b = self.b / 255.0
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    def __str__(self) -> str:
        if self.a < 1.0:
            return f"rgba({self.r}, {self.g}, {self.b}, {self.a:.2f})"
        return f"rgb({self.r}, {self.g}, {self.b})"


@dataclass
class HSL:
    """HSL 颜色表示"""
    h: float  # 0-360
    s: float  # 0-100
    l: float  # 0-100
    a: float = 1.0  # 0.0-1.0
    
    def __post_init__(self):
        self.h = self.h % 360
        self.s = max(0, min(100, float(self.s)))
        self.l = max(0, min(100, float(self.l)))
        self.a = max(0.0, min(1.0, float(self.a)))
    
    def to_rgb(self) -> RGB:
        """转换为 RGB"""
        r, g, b = colorsys.hls_to_rgb(self.h / 360, self.l / 100, self.s / 100)
        return RGB(int(r * 255), int(g * 255), int(b * 255), self.a)
    
    def to_hsv(self) -> 'HSV':
        """转换为 HSV"""
        return self.to_rgb().to_hsv()
    
    def to_hex(self) -> str:
        """转换为 HEX"""
        return self.to_rgb().to_hex()
    
    def __str__(self) -> str:
        if self.a < 1.0:
            return f"hsla({self.h:.1f}, {self.s:.1f}%, {self.l:.1f}%, {self.a:.2f})"
        return f"hsl({self.h:.1f}, {self.s:.1f}%, {self.l:.1f}%)"


@dataclass
class HSV:
    """HSV 颜色表示"""
    h: float  # 0-360
    s: float  # 0-100
    v: float  # 0-100
    a: float = 1.0  # 0.0-1.0
    
    def __post_init__(self):
        self.h = self.h % 360
        self.s = max(0, min(100, float(self.s)))
        self.v = max(0, min(100, float(self.v)))
        self.a = max(0.0, min(1.0, float(self.a)))
    
    def to_rgb(self) -> RGB:
        """转换为 RGB"""
        r, g, b = colorsys.hsv_to_rgb(self.h / 360, self.s / 100, self.v / 100)
        return RGB(int(r * 255), int(g * 255), int(b * 255), self.a)
    
    def to_hsl(self) -> HSL:
        """转换为 HSL"""
        return self.to_rgb().to_hsl()
    
    def to_hex(self) -> str:
        """转换为 HEX"""
        return self.to_rgb().to_hex()
    
    def __str__(self) -> str:
        if self.a < 1.0:
            return f"hsva({self.h:.1f}, {self.s:.1f}%, {self.v:.1f}%, {self.a:.2f})"
        return f"hsv({self.h:.1f}, {self.s:.1f}%, {self.v:.1f}%)"


@dataclass
class CMYK:
    """CMYK 颜色表示"""
    c: float  # 0-100
    m: float  # 0-100
    y: float  # 0-100
    k: float  # 0-100
    
    def __post_init__(self):
        self.c = max(0, min(100, float(self.c)))
        self.m = max(0, min(100, float(self.m)))
        self.y = max(0, min(100, float(self.y)))
        self.k = max(0, min(100, float(self.k)))
    
    def to_rgb(self) -> RGB:
        """转换为 RGB"""
        c, m, y, k = self.c / 100, self.m / 100, self.y / 100, self.k / 100
        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)
        return RGB(int(r), int(g), int(b))
    
    def to_hex(self) -> str:
        """转换为 HEX"""
        return self.to_rgb().to_hex()
    
    def __str__(self) -> str:
        return f"cmyk({self.c:.1f}%, {self.m:.1f}%, {self.y:.1f}%, {self.k:.1f}%)"


@dataclass
class LAB:
    """LAB 颜色表示"""
    L: float  # 0-100
    a: float  # -128 to 127
    b: float  # -128 to 127
    alpha: float = 1.0  # 0.0-1.0
    
    def __post_init__(self):
        self.L = max(0, min(100, float(self.L)))
        self.a = max(-128, min(127, float(self.a)))
        self.b = max(-128, min(127, float(self.b)))
        self.alpha = max(0.0, min(1.0, float(self.alpha)))
    
    def to_rgb(self) -> RGB:
        """转换为 RGB"""
        # LAB to XYZ
        y = (self.L + 16) / 116
        x = self.a / 500 + y
        z = y - self.b / 200
        
        def f_inv(t):
            t3 = t ** 3
            return t3 if t3 > 0.008856 else (t - 16 / 116) / 7.787
        
        x = f_inv(x) * 0.95047
        y = f_inv(y)
        z = f_inv(z) * 1.08883
        
        # XYZ to RGB
        r = x * 3.2404542 - y * 1.5371385 - z * 0.4985314
        g = -x * 0.9692660 + y * 1.8760108 + z * 0.0415560
        b = x * 0.0556434 - y * 0.2040259 + z * 1.0572252
        
        # Gamma correction
        r = 12.92 * r if r <= 0.0031308 else 1.055 * (r ** (1 / 2.4)) - 0.055
        g = 12.92 * g if g <= 0.0031308 else 1.055 * (g ** (1 / 2.4)) - 0.055
        b = 12.92 * b if b <= 0.0031308 else 1.055 * (b ** (1 / 2.4)) - 0.055
        
        return RGB(
            max(0, min(255, int(r * 255))),
            max(0, min(255, int(g * 255))),
            max(0, min(255, int(b * 255))),
            self.alpha
        )
    
    def delta_e(self, other: 'LAB') -> float:
        """计算两个颜色的色差 (Delta E76)"""
        return math.sqrt(
            (self.L - other.L) ** 2 +
            (self.a - other.a) ** 2 +
            (self.b - other.b) ** 2
        )
    
    def __str__(self) -> str:
        return f"lab({self.L:.1f}, {self.a:.1f}, {self.b:.1f})"


class Color:
    """
    统一颜色类，支持多种颜色空间转换和操作
    
    Example:
        >>> c = Color.from_hex("#ff6b6b")
        >>> c.complementary()
        <Color #6bffff>
        >>> c.lighten(20)
        <Color #ff9b9b>
    """
    
    def __init__(self, rgb: RGB):
        self._rgb = rgb
    
    @classmethod
    def from_rgb(cls, r: int, g: int, b: int, a: float = 1.0) -> 'Color':
        """从 RGB 创建颜色"""
        return cls(RGB(r, g, b, a))
    
    @classmethod
    def from_hex(cls, hex_str: str) -> 'Color':
        """从 HEX 字符串创建颜色"""
        hex_str = hex_str.lstrip('#')
        if len(hex_str) == 3:
            hex_str = ''.join(c * 2 for c in hex_str)
        if len(hex_str) == 8:
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            a = int(hex_str[6:8], 16) / 255
        else:
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            a = 1.0
        return cls(RGB(r, g, b, a))
    
    @classmethod
    def from_hsl(cls, h: float, s: float, l: float, a: float = 1.0) -> 'Color':
        """从 HSL 创建颜色"""
        hsl = HSL(h, s, l, a)
        return cls(hsl.to_rgb())
    
    @classmethod
    def from_hsv(cls, h: float, s: float, v: float, a: float = 1.0) -> 'Color':
        """从 HSV 创建颜色"""
        hsv = HSV(h, s, v, a)
        return cls(hsv.to_rgb())
    
    @classmethod
    def from_cmyk(cls, c: float, m: float, y: float, k: float) -> 'Color':
        """从 CMYK 创建颜色"""
        cmyk = CMYK(c, m, y, k)
        return cls(cmyk.to_rgb())
    
    @classmethod
    def from_lab(cls, L: float, a: float, b: float, alpha: float = 1.0) -> 'Color':
        """从 LAB 创建颜色"""
        lab = LAB(L, a, b, alpha)
        return cls(lab.to_rgb())
    
    @classmethod
    def random(cls) -> 'Color':
        """生成随机颜色"""
        return cls(RGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    
    @property
    def rgb(self) -> RGB:
        return self._rgb
    
    @property
    def hsl(self) -> HSL:
        return self._rgb.to_hsl()
    
    @property
    def hsv(self) -> HSV:
        return self._rgb.to_hsv()
    
    @property
    def cmyk(self) -> CMYK:
        return self._rgb.to_cmyk()
    
    @property
    def lab(self) -> LAB:
        return self._rgb.to_lab()
    
    @property
    def hex(self) -> str:
        return self._rgb.to_hex()
    
    @property
    def luminance(self) -> float:
        return self._rgb.luminance()
    
    # === 色彩操作 ===
    
    def lighten(self, amount: float = 10) -> 'Color':
        """变亮"""
        hsl = self.hsl
        new_l = min(100, hsl.l + amount)
        return Color.from_hsl(hsl.h, hsl.s, new_l, hsl.a)
    
    def darken(self, amount: float = 10) -> 'Color':
        """变暗"""
        hsl = self.hsl
        new_l = max(0, hsl.l - amount)
        return Color.from_hsl(hsl.h, hsl.s, new_l, hsl.a)
    
    def saturate(self, amount: float = 10) -> 'Color':
        """增加饱和度"""
        hsl = self.hsl
        new_s = min(100, hsl.s + amount)
        return Color.from_hsl(hsl.h, new_s, hsl.l, hsl.a)
    
    def desaturate(self, amount: float = 10) -> 'Color':
        """降低饱和度"""
        hsl = self.hsl
        new_s = max(0, hsl.s - amount)
        return Color.from_hsl(hsl.h, new_s, hsl.l, hsl.a)
    
    def grayscale(self) -> 'Color':
        """转为灰度"""
        return Color.from_hsl(self.hsl.h, 0, self.hsl.l, self.hsl.a)
    
    def invert(self) -> 'Color':
        """反转颜色"""
        return Color.from_rgb(255 - self.rgb.r, 255 - self.rgb.g, 255 - self.rgb.b)
    
    def rotate(self, degrees: float) -> 'Color':
        """旋转色相"""
        hsl = self.hsl
        new_h = (hsl.h + degrees) % 360
        return Color.from_hsl(new_h, hsl.s, hsl.l, hsl.a)
    
    def mix(self, other: 'Color', weight: float = 0.5) -> 'Color':
        """混合两种颜色"""
        w = max(0, min(1, weight))
        r = int(self.rgb.r * (1 - w) + other.rgb.r * w)
        g = int(self.rgb.g * (1 - w) + other.rgb.g * w)
        b = int(self.rgb.b * (1 - w) + other.rgb.b * w)
        a = self.rgb.a * (1 - w) + other.rgb.a * w
        return Color.from_rgb(r, g, b, a)
    
    # === 色彩和谐 ===
    
    def complementary(self) -> 'Color':
        """获取互补色"""
        return self.rotate(180)
    
    def analogous(self, angle: float = 30) -> List['Color']:
        """获取类似色 (相邻色)"""
        return [self.rotate(-angle), self, self.rotate(angle)]
    
    def triadic(self) -> List['Color']:
        """获取三色组合"""
        return [self, self.rotate(120), self.rotate(240)]
    
    def tetradic(self) -> List['Color']:
        """获取四色组合"""
        return [self, self.rotate(90), self.rotate(180), self.rotate(270)]
    
    def split_complementary(self) -> List['Color']:
        """获取分裂互补色"""
        return [self, self.rotate(150), self.rotate(210)]
    
    def double_complementary(self) -> List['Color']:
        """获取双互补色"""
        return [self, self.complementary(), self.rotate(30), self.rotate(210)]
    
    # === 对比度 ===
    
    def contrast_ratio(self, other: 'Color') -> float:
        """
        计算与另一颜色的对比度
        
        返回值范围: 1-21
        WCAG 标准:
        - AA 标准: 最小 4.5 (普通文本), 3 (大文本)
        - AAA 标准: 最小 7 (普通文本), 4.5 (大文本)
        """
        l1 = self.luminance
        l2 = other.luminance
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)
    
    def wcag_level(self, other: 'Color', large_text: bool = False) -> str:
        """
        获取 WCAG 对比度等级
        
        Returns:
            "AAA", "AA", "AA Large" 或 "Fail"
        """
        ratio = self.contrast_ratio(other)
        
        if large_text:
            if ratio >= 4.5:
                return "AAA"
            elif ratio >= 3:
                return "AA"
        else:
            if ratio >= 7:
                return "AAA"
            elif ratio >= 4.5:
                return "AA"
        
        return "Fail"
    
    def readable_text_color(self, dark: str = "#000000", light: str = "#ffffff") -> 'Color':
        """返回适合在此颜色上显示的文本颜色"""
        dark_color = Color.from_hex(dark)
        light_color = Color.from_hex(light)
        
        # 使用 WCAG 标准选择更可读的颜色
        dark_contrast = self.contrast_ratio(dark_color)
        light_contrast = self.contrast_ratio(light_color)
        
        return dark_color if dark_contrast > light_contrast else light_color
    
    # === 色盲模拟 ===
    
    def simulate_protanopia(self) -> 'Color':
        """模拟红色盲"""
        # 简化的红色盲模拟矩阵
        r = self.rgb.r * 0.567 + self.rgb.g * 0.433 + self.rgb.b * 0.0
        g = self.rgb.r * 0.558 + self.rgb.g * 0.442 + self.rgb.b * 0.0
        b = self.rgb.r * 0.0 + self.rgb.g * 0.242 + self.rgb.b * 0.758
        return Color.from_rgb(int(r), int(g), int(b))
    
    def simulate_deuteranopia(self) -> 'Color':
        """模拟绿色盲"""
        r = self.rgb.r * 0.625 + self.rgb.g * 0.375 + self.rgb.b * 0.0
        g = self.rgb.r * 0.7 + self.rgb.g * 0.3 + self.rgb.b * 0.0
        b = self.rgb.r * 0.0 + self.rgb.g * 0.3 + self.rgb.b * 0.7
        return Color.from_rgb(int(r), int(g), int(b))
    
    def simulate_tritanopia(self) -> 'Color':
        """模拟蓝色盲"""
        r = self.rgb.r * 0.95 + self.rgb.g * 0.05 + self.rgb.b * 0.0
        g = self.rgb.r * 0.0 + self.rgb.g * 0.433 + self.rgb.b * 0.567
        b = self.rgb.r * 0.0 + self.rgb.g * 0.475 + self.rgb.b * 0.525
        return Color.from_rgb(int(r), int(g), int(b))
    
    def __repr__(self) -> str:
        return f"<Color {self.hex}>"
    
    def __str__(self) -> str:
        return self.hex
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Color):
            return self.rgb.to_tuple() == other.rgb.to_tuple()
        return False
    
    def __hash__(self) -> int:
        return hash(self.rgb.to_tuple())


class ColorPalette:
    """
    颜色调色板
    
    Example:
        >>> palette = ColorPalette.from_base_color("#ff6b6b")
        >>> print(palette)
        ColorPalette(5 colors)
        >>> palette.colors
        [<Color #ff6b6b>, <Color #6bffff>, ...]
    """
    
    def __init__(self, colors: List[Color], name: str = ""):
        self.colors = colors
        self.name = name
    
    @classmethod
    def from_base_color(cls, base: Union[str, Color], scheme: str = "complementary") -> 'ColorPalette':
        """
        从基础颜色创建调色板
        
        Args:
            base: 基础颜色
            scheme: 配色方案
                - "complementary": 互补色
                - "analogous": 类似色
                - "triadic": 三色
                - "tetradic": 四色
                - "split_complementary": 分裂互补
                - "double_complementary": 双互补
        """
        if isinstance(base, str):
            base = Color.from_hex(base)
        
        scheme_map = {
            "complementary": lambda c: [c, c.complementary()],
            "analogous": lambda c: c.analogous(),
            "triadic": lambda c: c.triadic(),
            "tetradic": lambda c: c.tetradic(),
            "split_complementary": lambda c: c.split_complementary(),
            "double_complementary": lambda c: c.double_complementary(),
        }
        
        if scheme not in scheme_map:
            raise ValueError(f"Unknown scheme: {scheme}")
        
        colors = scheme_map[scheme](base)
        return cls(colors, name=scheme)
    
    @classmethod
    def from_harmony(cls, base: Union[str, Color], harmony_type: str = "triadic") -> 'ColorPalette':
        """from_base_color 的别名，使用 harmony_type 参数名"""
        return cls.from_base_color(base, harmony_type)
    
    @classmethod
    def gradient(cls, start: Union[str, Color], end: Union[str, Color], steps: int = 5) -> 'ColorPalette':
        """
        创建渐变调色板
        
        Args:
            start: 起始颜色
            end: 结束颜色
            steps: 步数
        """
        if isinstance(start, str):
            start = Color.from_hex(start)
        if isinstance(end, str):
            end = Color.from_hex(end)
        
        colors = [start]
        for i in range(1, steps - 1):
            weight = i / (steps - 1)
            colors.append(start.mix(end, weight))
        colors.append(end)
        
        return cls(colors, name="gradient")
    
    @classmethod
    def from_hue_range(cls, start_hue: float, end_hue: float, steps: int = 12,
                       saturation: float = 70, lightness: float = 50) -> 'ColorPalette':
        """
        从色相范围创建调色板
        
        Args:
            start_hue: 起始色相 (0-360)
            end_hue: 结束色相 (0-360)
            steps: 步数
            saturation: 饱和度 (0-100)
            lightness: 亮度 (0-100)
        """
        colors = []
        hue_step = (end_hue - start_hue) / (steps - 1) if steps > 1 else 0
        
        for i in range(steps):
            hue = (start_hue + i * hue_step) % 360
            colors.append(Color.from_hsl(hue, saturation, lightness))
        
        return cls(colors, name="hue_range")
    
    @classmethod
    def rainbow(cls, steps: int = 12, saturation: float = 70, lightness: float = 50) -> 'ColorPalette':
        """创建彩虹调色板"""
        return cls.from_hue_range(0, 360, steps, saturation, lightness)
    
    @classmethod
    def from_temperature(cls, temperature: str = "warm", steps: int = 5) -> 'ColorPalette':
        """
        从温度创建调色板
        
        Args:
            temperature: "warm", "cool", "neutral"
            steps: 步数
        """
        if temperature == "warm":
            # 红色到黄色的暖色调
            return cls.from_hue_range(0, 60, steps, 70, 50)
        elif temperature == "cool":
            # 蓝色到紫色的冷色调
            return cls.from_hue_range(180, 300, steps, 70, 50)
        elif temperature == "neutral":
            # 灰色调
            colors = [Color.from_hsl(0, 0, i * 100 / (steps - 1)) for i in range(steps)]
            return cls(colors, name="neutral")
        else:
            raise ValueError(f"Unknown temperature: {temperature}")
    
    @classmethod
    def monochromatic(cls, base: Union[str, Color], steps: int = 5) -> 'ColorPalette':
        """
        创建单色调色板
        
        Args:
            base: 基础颜色
            steps: 步数
        """
        if isinstance(base, str):
            base = Color.from_hex(base)
        
        hsl = base.hsl
        colors = []
        
        # 从暗到亮
        for i in range(steps):
            lightness = 20 + (60 * i / (steps - 1)) if steps > 1 else 50
            colors.append(Color.from_hsl(hsl.h, hsl.s, lightness))
        
        return cls(colors, name="monochromatic")
    
    @classmethod
    def shades(cls, base: Union[str, Color], steps: int = 9) -> 'ColorPalette':
        """
        创建色阶调色板 (从深到浅)
        
        Args:
            base: 基础颜色
            steps: 步数
        """
        if isinstance(base, str):
            base = Color.from_hex(base)
        
        colors = []
        for i in range(steps):
            # 从 100 (最亮) 到 0 (最暗)
            lightness = 95 - (i * 95 / (steps - 1)) if steps > 1 else 50
            colors.append(Color.from_hsl(base.hsl.h, base.hsl.s, lightness))
        
        return cls(colors, name="shades")
    
    def to_hex_list(self) -> List[str]:
        """转换为 HEX 字符串列表"""
        return [c.hex for c in self.colors]
    
    def to_rgb_list(self) -> List[Tuple[int, int, int]]:
        """转换为 RGB 元组列表"""
        return [c.rgb.to_tuple() for c in self.colors]
    
    def to_hsl_list(self) -> List[Tuple[float, float, float]]:
        """转换为 HSL 元组列表"""
        return [(c.hsl.h, c.hsl.s, c.hsl.l) for c in self.colors]
    
    def with_contrast_check(self, background: Union[str, Color], min_ratio: float = 4.5) -> 'ColorPalette':
        """
        过滤掉对比度不足的颜色
        
        Args:
            background: 背景色
            min_ratio: 最小对比度
        """
        if isinstance(background, str):
            background = Color.from_hex(background)
        
        filtered = [c for c in self.colors if c.contrast_ratio(background) >= min_ratio]
        return ColorPalette(filtered, name=self.name + "_filtered")
    
    def __len__(self) -> int:
        return len(self.colors)
    
    def __getitem__(self, index: int) -> Color:
        return self.colors[index]
    
    def __iter__(self):
        return iter(self.colors)
    
    def __repr__(self) -> str:
        return f"ColorPalette({len(self)} colors)"
    
    def __str__(self) -> str:
        return f"ColorPalette: {', '.join(c.hex for c in self.colors)}"


class Gradient:
    """
    渐变色生成器
    
    Example:
        >>> gradient = Gradient.linear("#ff0000", "#0000ff", steps=10)
        >>> for color in gradient:
        ...     print(color.hex)
    """
    
    def __init__(self, stops: List[Tuple[float, Color]]):
        """
        初始化渐变
        
        Args:
            stops: 停止点列表 [(position, Color), ...]
                   position 范围 0.0-1.0
        """
        self.stops = sorted(stops, key=lambda x: x[0])
    
    @classmethod
    def linear(cls, start: Union[str, Color], end: Union[str, Color], steps: int = 10) -> 'Gradient':
        """创建线性渐变"""
        if isinstance(start, str):
            start = Color.from_hex(start)
        if isinstance(end, str):
            end = Color.from_hex(end)
        
        return cls([(0.0, start), (1.0, end)])
    
    @classmethod
    def multi_stop(cls, colors: List[Union[str, Color]], positions: Optional[List[float]] = None) -> 'Gradient':
        """
        创建多停止点渐变
        
        Args:
            colors: 颜色列表
            positions: 位置列表 (可选，自动均匀分布)
        """
        parsed_colors = [Color.from_hex(c) if isinstance(c, str) else c for c in colors]
        
        if positions is None:
            positions = [i / (len(colors) - 1) for i in range(len(colors))]
        
        return cls(list(zip(positions, parsed_colors)))
    
    @classmethod
    def radial(cls, center: Union[str, Color], edge: Union[str, Color], steps: int = 10) -> 'Gradient':
        """创建径向渐变 (简化版，效果同线性)"""
        return cls.linear(center, edge, steps)
    
    def color_at(self, position: float) -> Color:
        """获取指定位置的颜色"""
        position = max(0.0, min(1.0, position))
        
        # 找到相邻的两个停止点
        if position <= self.stops[0][0]:
            return self.stops[0][1]
        if position >= self.stops[-1][0]:
            return self.stops[-1][1]
        
        for i in range(len(self.stops) - 1):
            pos1, color1 = self.stops[i]
            pos2, color2 = self.stops[i + 1]
            
            if pos1 <= position <= pos2:
                # 线性插值
                t = (position - pos1) / (pos2 - pos1) if pos2 != pos1 else 0
                return color1.mix(color2, t)
        
        return self.stops[-1][1]
    
    def to_palette(self, steps: int = 10) -> ColorPalette:
        """转换为调色板"""
        colors = [self.color_at(i / (steps - 1)) for i in range(steps)]
        return ColorPalette(colors, name="gradient")
    
    def __iter__(self):
        for i in range(10):
            yield self.color_at(i / 9)
    
    def __repr__(self) -> str:
        return f"Gradient({len(self.stops)} stops)"


class ColorUtils:
    """颜色工具类"""
    
    # 常用颜色名称映射
    NAMED_COLORS = {
        "black": "#000000",
        "white": "#ffffff",
        "red": "#ff0000",
        "green": "#00ff00",
        "blue": "#0000ff",
        "yellow": "#ffff00",
        "cyan": "#00ffff",
        "magenta": "#ff00ff",
        "orange": "#ffa500",
        "pink": "#ffc0cb",
        "purple": "#800080",
        "brown": "#a52a2a",
        "gray": "#808080",
        "grey": "#808080",
        "silver": "#c0c0c0",
        "gold": "#ffd700",
        "navy": "#000080",
        "teal": "#008080",
        "olive": "#808000",
        "maroon": "#800000",
        "lime": "#00ff00",
        "aqua": "#00ffff",
        "fuchsia": "#ff00ff",
        "coral": "#ff7f50",
        "crimson": "#dc143c",
        "indigo": "#4b0082",
        "violet": "#ee82ee",
        "turquoise": "#40e0d0",
        "salmon": "#fa8072",
        "khaki": "#f0e68c",
        "beige": "#f5f5dc",
        "ivory": "#fffff0",
        "mint": "#98ff98",
        "peach": "#ffcba4",
        "lavender": "#e6e6fa",
    }
    
    @classmethod
    def from_name(cls, name: str) -> Color:
        """从颜色名称创建颜色"""
        name_lower = name.lower().strip()
        if name_lower not in cls.NAMED_COLORS:
            raise ValueError(f"Unknown color name: {name}")
        return Color.from_hex(cls.NAMED_COLORS[name_lower])
    
    @classmethod
    def parse(cls, value: Union[str, Tuple, List]) -> Color:
        """
        解析各种格式的颜色值
        
        Args:
            value: 颜色值
                - HEX 字符串: "#ff6b6b"
                - 颜色名称: "red", "blue"
                - RGB 元组: (255, 107, 107)
                - RGBA 元组: (255, 107, 107, 0.5)
        """
        if isinstance(value, str):
            if value.startswith("#"):
                return Color.from_hex(value)
            return cls.from_name(value)
        elif isinstance(value, (tuple, list)):
            if len(value) == 3:
                return Color.from_rgb(*value)
            elif len(value) == 4:
                return Color.from_rgb(*value[:3], value[3])
        
        raise ValueError(f"Cannot parse color: {value}")
    
    @classmethod
    def suggest_text_color(cls, background: Union[str, Color]) -> Color:
        """建议文本颜色 (黑色或白色)"""
        if isinstance(background, str):
            background = Color.from_hex(background)
        return background.readable_text_color()
    
    @classmethod
    def blend(cls, colors: List[Union[str, Color]], weights: Optional[List[float]] = None) -> Color:
        """
        混合多种颜色
        
        Args:
            colors: 颜色列表
            weights: 权重列表 (可选)
        """
        if not colors:
            raise ValueError("Need at least one color")
        
        parsed = [Color.from_hex(c) if isinstance(c, str) else c for c in colors]
        
        if weights is None:
            weights = [1.0 / len(colors)] * len(colors)
        
        if len(weights) != len(colors):
            raise ValueError("Weights must match colors length")
        
        # 归一化权重
        total = sum(weights)
        weights = [w / total for w in weights]
        
        # 加权平均
        r = sum(c.rgb.r * w for c, w in zip(parsed, weights))
        g = sum(c.rgb.g * w for c, w in zip(parsed, weights))
        b = sum(c.rgb.b * w for c, w in zip(parsed, weights))
        
        return Color.from_rgb(int(r), int(g), int(b))
    
    @classmethod
    def is_light(cls, color: Union[str, Color]) -> bool:
        """判断颜色是否为亮色"""
        if isinstance(color, str):
            color = Color.from_hex(color)
        return color.luminance > 0.5
    
    @classmethod
    def is_dark(cls, color: Union[str, Color]) -> bool:
        """判断颜色是否为暗色"""
        return not cls.is_light(color)
    
    @classmethod
    def color_distance(cls, c1: Union[str, Color], c2: Union[str, Color]) -> float:
        """
        计算两个颜色之间的距离 (使用 LAB 空间)
        
        返回值越小，颜色越相似
        """
        if isinstance(c1, str):
            c1 = Color.from_hex(c1)
        if isinstance(c2, str):
            c2 = Color.from_hex(c2)
        
        return c1.lab.delta_e(c2.lab)
    
    @classmethod
    def closest_color(cls, target: Union[str, Color], candidates: List[Union[str, Color]]) -> Color:
        """从候选颜色中找到最接近目标颜色的颜色"""
        if isinstance(target, str):
            target = Color.from_hex(target)
        
        parsed = [Color.from_hex(c) if isinstance(c, str) else c for c in candidates]
        
        min_dist = float('inf')
        closest = parsed[0]
        
        for c in parsed:
            dist = target.lab.delta_e(c.lab)
            if dist < min_dist:
                min_dist = dist
                closest = c
        
        return closest
    
    @classmethod
    def sort_by_hue(cls, colors: List[Union[str, Color]]) -> List[Color]:
        """按色相排序颜色"""
        parsed = [Color.from_hex(c) if isinstance(c, str) else c for c in colors]
        return sorted(parsed, key=lambda c: c.hsl.h)
    
    @classmethod
    def sort_by_lightness(cls, colors: List[Union[str, Color]]) -> List[Color]:
        """按亮度排序颜色"""
        parsed = [Color.from_hex(c) if isinstance(c, str) else c for c in colors]
        return sorted(parsed, key=lambda c: c.hsl.l)
    
    @classmethod
    def sort_by_saturation(cls, colors: List[Union[str, Color]]) -> List[Color]:
        """按饱和度排序颜色"""
        parsed = [Color.from_hex(c) if isinstance(c, str) else c for c in colors]
        return sorted(parsed, key=lambda c: c.hsl.s)


# 便捷函数
def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """HEX 转 RGB"""
    return Color.from_hex(hex_str).rgb.to_tuple()


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """RGB 转 HEX"""
    return Color.from_rgb(r, g, b).hex


def hex_to_hsl(hex_str: str) -> Tuple[float, float, float]:
    """HEX 转 HSL"""
    hsl = Color.from_hex(hex_str).hsl
    return (hsl.h, hsl.s, hsl.l)


def hsl_to_hex(h: float, s: float, l: float) -> str:
    """HSL 转 HEX"""
    return Color.from_hsl(h, s, l).hex


def random_color() -> Color:
    """生成随机颜色"""
    return Color.random()


def random_palette(size: int = 5) -> ColorPalette:
    """生成随机调色板"""
    colors = [Color.random() for _ in range(size)]
    return ColorPalette(colors, name="random")


def complementary(hex_str: str) -> str:
    """获取互补色 HEX"""
    return Color.from_hex(hex_str).complementary().hex


def lighten(hex_str: str, amount: float = 10) -> str:
    """变亮颜色"""
    return Color.from_hex(hex_str).lighten(amount).hex


def darken(hex_str: str, amount: float = 10) -> str:
    """变暗颜色"""
    return Color.from_hex(hex_str).darken(amount).hex


def contrast_ratio(color1: str, color2: str) -> float:
    """计算两个颜色的对比度"""
    c1 = Color.from_hex(color1)
    c2 = Color.from_hex(color2)
    return c1.contrast_ratio(c2)


def gradient(start: str, end: str, steps: int = 5) -> List[str]:
    """生成渐变色列表"""
    return ColorPalette.gradient(start, end, steps).to_hex_list()


def palette(base: str, scheme: str = "triadic") -> List[str]:
    """生成配色方案"""
    return ColorPalette.from_base_color(base, scheme).to_hex_list()