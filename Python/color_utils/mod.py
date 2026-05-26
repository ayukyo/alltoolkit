"""
Color Utils - 颜色工具模块

提供颜色转换、调色板生成、色彩对比度计算等功能。
零外部依赖，纯 Python 实现。

功能：
- 颜色格式转换（HEX、RGB、HSL、HSV、CMYK）
- 调色板生成（互补色、类似色、三角色、分裂互补色、矩形色）
- 色彩对比度计算（WCAG AA/AAA 标准）
- 颜色混合和渐变生成
- 颜色亮度调整
- 色盲安全色转换

作者：AllToolkit
日期：2026-05-27
"""

from typing import Tuple, List, Dict, Optional, Union
import math
import colorsys


class Color:
    """颜色类，支持多种格式转换和操作"""
    
    def __init__(self, r: int, g: int, b: int, a: float = 1.0):
        """
        初始化颜色（RGB格式）
        
        Args:
            r: 红色分量 (0-255)
            g: 绿色分量 (0-255)
            b: 蓝色分量 (0-255)
            a: 透明度 (0.0-1.0)
        """
        self.r = max(0, min(255, int(r)))
        self.g = max(0, min(255, int(g)))
        self.b = max(0, min(255, int(b)))
        self.a = max(0.0, min(1.0, float(a)))
    
    @classmethod
    def from_hex(cls, hex_color: str) -> 'Color':
        """从十六进制颜色创建"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join(c*2 for c in hex_color)
        elif len(hex_color) == 4:  # #RGBA
            hex_color = hex_color[0]*2 + hex_color[1]*2 + hex_color[2]*2
        elif len(hex_color) == 8:  # #RRGGBBAA
            r, g, b, a = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16), int(hex_color[6:8], 16) / 255
            return cls(r, g, b, a)
        
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return cls(r, g, b)
    
    @classmethod
    def from_rgb(cls, r: int, g: int, b: int, a: float = 1.0) -> 'Color':
        """从RGB创建"""
        return cls(r, g, b, a)
    
    @classmethod
    def from_hsl(cls, h: float, s: float, l: float, a: float = 1.0) -> 'Color':
        """从HSL创建 (h: 0-360, s: 0-100, l: 0-100)"""
        h = h % 360
        s = max(0, min(100, s)) / 100
        l = max(0, min(100, l)) / 100
        r, g, b = colorsys.hls_to_rgb(h / 360, l, s)
        return cls(int(r * 255), int(g * 255), int(b * 255), a)
    
    @classmethod
    def from_hsv(cls, h: float, s: float, v: float, a: float = 1.0) -> 'Color':
        """从HSV创建 (h: 0-360, s: 0-100, v: 0-100)"""
        h = h % 360
        s = max(0, min(100, s)) / 100
        v = max(0, min(100, v)) / 100
        r, g, b = colorsys.hsv_to_rgb(h / 360, s, v)
        return cls(int(r * 255), int(g * 255), int(b * 255), a)
    
    @classmethod
    def from_cmyk(cls, c: float, m: float, y: float, k: float) -> 'Color':
        """从CMYK创建 (0-100)"""
        c = max(0, min(100, c)) / 100
        m = max(0, min(100, m)) / 100
        y = max(0, min(100, y)) / 100
        k = max(0, min(100, k)) / 100
        
        r = int(255 * (1 - c) * (1 - k))
        g = int(255 * (1 - m) * (1 - k))
        b = int(255 * (1 - y) * (1 - k))
        return cls(r, g, b)
    
    @classmethod
    def random(cls) -> 'Color':
        """生成随机颜色"""
        import random
        return cls(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    @property
    def hex(self) -> str:
        """返回十六进制格式 #RRGGBB"""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    @property
    def hex_with_alpha(self) -> str:
        """返回带透明度的十六进制格式 #RRGGBBAA"""
        alpha = int(self.a * 255)
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}{alpha:02x}"
    
    @property
    def rgb(self) -> Tuple[int, int, int]:
        """返回RGB元组"""
        return (self.r, self.g, self.b)
    
    @property
    def rgba(self) -> Tuple[int, int, int, float]:
        """返回RGBA元组"""
        return (self.r, self.g, self.b, self.a)
    
    @property
    def hsl(self) -> Tuple[float, float, float]:
        """返回HSL元组 (h: 0-360, s: 0-100, l: 0-100)"""
        h, l, s = colorsys.rgb_to_hls(self.r / 255, self.g / 255, self.b / 255)
        return (h * 360, s * 100, l * 100)
    
    @property
    def hsv(self) -> Tuple[float, float, float]:
        """返回HSV元组 (h: 0-360, s: 0-100, v: 0-100)"""
        h, s, v = colorsys.rgb_to_hsv(self.r / 255, self.g / 255, self.b / 255)
        return (h * 360, s * 100, v * 100)
    
    @property
    def cmyk(self) -> Tuple[float, float, float, float]:
        """返回CMYK元组 (0-100)"""
        if self.r == 0 and self.g == 0 and self.b == 0:
            return (0, 0, 0, 100)
        
        r_prime = self.r / 255
        g_prime = self.g / 255
        b_prime = self.b / 255
        
        k = 1 - max(r_prime, g_prime, b_prime)
        c = (1 - r_prime - k) / (1 - k) if k < 1 else 0
        m = (1 - g_prime - k) / (1 - k) if k < 1 else 0
        y = (1 - b_prime - k) / (1 - k) if k < 1 else 0
        
        return (c * 100, m * 100, y * 100, k * 100)
    
    @property
    def luminance(self) -> float:
        """计算相对亮度 (0.0-1.0)"""
        def adjust(c):
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        
        r = adjust(self.r / 255)
        g = adjust(self.g / 255)
        b = adjust(self.b / 255)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    @property
    def is_light(self) -> bool:
        """判断是否为浅色"""
        return self.luminance > 0.5
    
    @property
    def is_dark(self) -> bool:
        """判断是否为深色"""
        return self.luminance <= 0.5
    
    def contrast_ratio(self, other: 'Color') -> float:
        """计算与另一个颜色的对比度 (1:1 到 21:1)"""
        l1 = self.luminance
        l2 = other.luminance
        
        if l1 > l2:
            return (l1 + 0.05) / (l2 + 0.05)
        else:
            return (l2 + 0.05) / (l1 + 0.05)
    
    def wcag_compliance(self, other: 'Color') -> Dict[str, bool]:
        """
        检查WCAG对比度合规性
        
        Returns:
            Dict: 包含 AA_normal, AA_large, AAA_normal, AAA_large 合规状态
        """
        ratio = self.contrast_ratio(other)
        return {
            'AA_normal': ratio >= 4.5,
            'AA_large': ratio >= 3.0,
            'AAA_normal': ratio >= 7.0,
            'AAA_large': ratio >= 4.5,
            'ratio': round(ratio, 2)
        }
    
    def best_text_color(self) -> 'Color':
        """返回最佳文字颜色（黑或白）"""
        # 使用WCAG标准，选择对比度更高的
        black = Color(0, 0, 0)
        white = Color(255, 255, 255)
        
        black_ratio = self.contrast_ratio(black)
        white_ratio = self.contrast_ratio(white)
        
        return white if white_ratio > black_ratio else black
    
    def lighten(self, amount: float = 10.0) -> 'Color':
        """变亮"""
        h, s, l = self.hsl
        l = min(100, l + amount)
        return Color.from_hsl(h, s, l, self.a)
    
    def darken(self, amount: float = 10.0) -> 'Color':
        """变暗"""
        h, s, l = self.hsl
        l = max(0, l - amount)
        return Color.from_hsl(h, s, l, self.a)
    
    def saturate(self, amount: float = 10.0) -> 'Color':
        """增加饱和度"""
        h, s, l = self.hsl
        s = min(100, s + amount)
        return Color.from_hsl(h, s, l, self.a)
    
    def desaturate(self, amount: float = 10.0) -> 'Color':
        """降低饱和度"""
        h, s, l = self.hsl
        s = max(0, s - amount)
        return Color.from_hsl(h, s, l, self.a)
    
    def rotate_hue(self, degrees: float) -> 'Color':
        """旋转色相"""
        h, s, l = self.hsl
        h = (h + degrees) % 360
        return Color.from_hsl(h, s, l, self.a)
    
    def mix(self, other: 'Color', weight: float = 0.5) -> 'Color':
        """
        混合两个颜色
        
        Args:
            other: 另一个颜色
            weight: 权重 (0.0=完全other, 1.0=完全self)
        """
        weight = max(0, min(1, weight))
        r = int(self.r * weight + other.r * (1 - weight))
        g = int(self.g * weight + other.g * (1 - weight))
        b = int(self.b * weight + other.b * (1 - weight))
        a = self.a * weight + other.a * (1 - weight)
        return Color(r, g, b, a)
    
    def to_grayscale(self) -> 'Color':
        """转换为灰度"""
        gray = int(0.299 * self.r + 0.587 * self.g + 0.114 * self.b)
        return Color(gray, gray, gray, self.a)
    
    def invert(self) -> 'Color':
        """反色"""
        return Color(255 - self.r, 255 - self.g, 255 - self.b, self.a)
    
    def complement(self) -> 'Color':
        """互补色"""
        return self.rotate_hue(180)
    
    def __eq__(self, other):
        if not isinstance(other, Color):
            return False
        return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a
    
    def __repr__(self):
        if self.a < 1.0:
            return f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a:.2f})"
        return f"Color(r={self.r}, g={self.g}, b={self.b})"
    
    def __str__(self):
        return self.hex


class ColorPalette:
    """调色板生成器"""
    
    @staticmethod
    def complementary(color: Color) -> List[Color]:
        """互补色调色板（2色）"""
        return [color, color.complement()]
    
    @staticmethod
    def analogous(color: Color, count: int = 3, spread: float = 30.0) -> List[Color]:
        """
        类似色调色板
        
        Args:
            color: 基础色
            count: 颜色数量
            spread: 色相间隔角度
        """
        colors = [color]
        for i in range(1, count):
            angle = spread * (i if i % 2 == 0 else -i)
            colors.append(color.rotate_hue(angle))
        colors.sort(key=lambda c: c.hsl[0])
        return colors
    
    @staticmethod
    def triadic(color: Color) -> List[Color]:
        """三角色调色板（3色）"""
        return [color, color.rotate_hue(120), color.rotate_hue(240)]
    
    @staticmethod
    def split_complementary(color: Color) -> List[Color]:
        """分裂互补色调色板（3色）"""
        return [color, color.rotate_hue(150), color.rotate_hue(210)]
    
    @staticmethod
    def tetradic(color: Color) -> List[Color]:
        """矩形色调色板（4色）"""
        return [color, color.rotate_hue(90), color.rotate_hue(180), color.rotate_hue(270)]
    
    @staticmethod
    def square(color: Color) -> List[Color]:
        """正方形色调色板（4色）"""
        return ColorPalette.tetradic(color)
    
    @staticmethod
    def monochromatic(color: Color, count: int = 5) -> List[Color]:
        """单色调色板"""
        h, s, l = color.hsl
        l_step = 80.0 / (count - 1) if count > 1 else 0
        colors = []
        for i in range(count):
            new_l = 10 + l_step * i
            colors.append(Color.from_hsl(h, s, new_l))
        return colors
    
    @staticmethod
    def shades(color: Color, count: int = 5) -> List[Color]:
        """色阶调色板（从浅到深）"""
        colors = []
        step = 1.0 / (count - 1) if count > 1 else 0
        for i in range(count):
            weight = i * step
            colors.append(color.mix(Color(0, 0, 0), 1 - weight))
        return colors
    
    @staticmethod
    def tints(color: Color, count: int = 5) -> List[Color]:
        """色调调色板（从深到浅）"""
        colors = []
        step = 1.0 / (count - 1) if count > 1 else 0
        for i in range(count):
            weight = i * step
            colors.append(color.mix(Color(255, 255, 255), 1 - weight))
        return colors
    
    @staticmethod
    def gradient(start: Color, end: Color, steps: int = 10) -> List[Color]:
        """渐变色"""
        if steps < 2:
            return [start]
        
        colors = []
        for i in range(steps):
            weight = i / (steps - 1)
            colors.append(start.mix(end, weight))
        return colors
    
    @staticmethod
    def multi_gradient(colors: List[Color], steps_per_segment: int = 10) -> List[Color]:
        """多色渐变"""
        if len(colors) < 2:
            return colors
        
        result = []
        for i in range(len(colors) - 1):
            segment = ColorPalette.gradient(colors[i], colors[i+1], steps_per_segment)
            result.extend(segment[:-1] if i < len(colors) - 2 else segment)
        return result
    
    @staticmethod
    def random_palette(count: int = 5, harmony: str = 'random') -> List[Color]:
        """
        生成随机调色板
        
        Args:
            count: 颜色数量
            harmony: 和谐类型 ('random', 'pastel', 'vibrant', 'earth', 'cool', 'warm')
        """
        import random
        
        palettes = []
        
        if harmony == 'pastel':
            for _ in range(count):
                h = random.random() * 360
                s = random.uniform(30, 60)
                l = random.uniform(70, 90)
                palettes.append(Color.from_hsl(h, s, l))
        elif harmony == 'vibrant':
            for _ in range(count):
                h = random.random() * 360
                s = random.uniform(70, 100)
                l = random.uniform(45, 55)
                palettes.append(Color.from_hsl(h, s, l))
        elif harmony == 'earth':
            earth_hues = [random.uniform(0, 40) for _ in range(count)]  # 棕色系
            for h in earth_hues:
                s = random.uniform(30, 60)
                l = random.uniform(30, 60)
                palettes.append(Color.from_hsl(h, s, l))
        elif harmony == 'cool':
            for _ in range(count):
                h = random.uniform(180, 270)  # 蓝绿紫
                s = random.uniform(40, 80)
                l = random.uniform(35, 65)
                palettes.append(Color.from_hsl(h, s, l))
        elif harmony == 'warm':
            for _ in range(count):
                h = random.uniform(0, 60)  # 红橙黄
                s = random.uniform(50, 90)
                l = random.uniform(45, 65)
                palettes.append(Color.from_hsl(h, s, l))
        else:  # random
            for _ in range(count):
                palettes.append(Color.random())
        
        return palettes


class ColorBlindness:
    """色盲模拟和辅助"""
    
    # 色盲类型转换矩阵（简化版）
    PROTANOPIA = [
        [0.567, 0.433, 0],
        [0.558, 0.442, 0],
        [0, 0.242, 0.758]
    ]
    
    DEUTERANOPIA = [
        [0.625, 0.375, 0],
        [0.7, 0.3, 0],
        [0, 0.3, 0.7]
    ]
    
    TRITANOPIA = [
        [0.95, 0.05, 0],
        [0, 0.433, 0.567],
        [0, 0.475, 0.525]
    ]
    
    @staticmethod
    def _apply_matrix(color: Color, matrix: List[List[float]]) -> Color:
        """应用转换矩阵"""
        r = matrix[0][0] * color.r + matrix[0][1] * color.g + matrix[0][2] * color.b
        g = matrix[1][0] * color.r + matrix[1][1] * color.g + matrix[1][2] * color.b
        b = matrix[2][0] * color.r + matrix[2][1] * color.g + matrix[2][2] * color.b
        return Color(int(r), int(g), int(b))
    
    @classmethod
    def protanopia(cls, color: Color) -> Color:
        """红色盲模拟"""
        return cls._apply_matrix(color, cls.PROTANOPIA)
    
    @classmethod
    def deuteranopia(cls, color: Color) -> Color:
        """绿色盲模拟"""
        return cls._apply_matrix(color, cls.DEUTERANOPIA)
    
    @classmethod
    def tritanopia(cls, color: Color) -> Color:
        """蓝色盲模拟"""
        return cls._apply_matrix(color, cls.TRITANOPIA)
    
    @classmethod
    def simulate_all(cls, color: Color) -> Dict[str, Color]:
        """模拟所有色盲类型"""
        return {
            'normal': color,
            'protanopia': cls.protanopia(color),
            'deuteranopia': cls.deuteranopia(color),
            'tritanopia': cls.tritanopia(color)
        }
    
    @staticmethod
    def is_distinguishable(color1: Color, color2: Color, color_blind_type: str = 'deuteranopia') -> bool:
        """检查两个颜色在色盲情况下是否可区分"""
        if color_blind_type == 'protanopia':
            c1 = ColorBlindness.protanopia(color1)
            c2 = ColorBlindness.protanopia(color2)
        elif color_blind_type == 'tritanopia':
            c1 = ColorBlindness.tritanopia(color1)
            c2 = ColorBlindness.tritanopia(color2)
        else:  # deuteranopia (最常见)
            c1 = ColorBlindness.deuteranopia(color1)
            c2 = ColorBlindness.deuteranopia(color2)
        
        # 计算色差
        diff = math.sqrt((c1.r - c2.r)**2 + (c1.g - c2.g)**2 + (c1.b - c2.b)**2)
        return diff > 30  # 经验阈值
    
    @staticmethod
    def colorblind_safe_palette() -> List[Color]:
        """返回色盲友好的调色板"""
        return [
            Color.from_hex('#E69F00'),  # 橙色
            Color.from_hex('#56B4E9'),  # 天蓝
            Color.from_hex('#009E73'),  # 青绿
            Color.from_hex('#F0E442'),  # 黄色
            Color.from_hex('#0072B2'),  # 深蓝
            Color.from_hex('#D55E00'),  # 朱红
            Color.from_hex('#CC79A7'),  # 粉紫
            Color.from_hex('#000000'),  # 黑色
        ]


class ColorConverter:
    """颜色转换工具"""
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """HEX 转 RGB"""
        return Color.from_hex(hex_color).rgb
    
    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """RGB 转 HEX"""
        return Color(r, g, b).hex
    
    @staticmethod
    def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
        """RGB 转 HSL"""
        return Color(r, g, b).hsl
    
    @staticmethod
    def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
        """HSL 转 RGB"""
        return Color.from_hsl(h, s, l).rgb
    
    @staticmethod
    def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[float, float, float]:
        """RGB 转 HSV"""
        return Color(r, g, b).hsv
    
    @staticmethod
    def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
        """HSV 转 RGB"""
        return Color.from_hsv(h, s, v).rgb
    
    @staticmethod
    def rgb_to_cmyk(r: int, g: int, b: int) -> Tuple[float, float, float, float]:
        """RGB 转 CMYK"""
        return Color(r, g, b).cmyk
    
    @staticmethod
    def cmyk_to_rgb(c: float, m: float, y: float, k: float) -> Tuple[int, int, int]:
        """CMYK 转 RGB"""
        return Color.from_cmyk(c, m, y, k).rgb
    
    @staticmethod
    def hex_to_hsl(hex_color: str) -> Tuple[float, float, float]:
        """HEX 转 HSL"""
        return Color.from_hex(hex_color).hsl
    
    @staticmethod
    def hsl_to_hex(h: float, s: float, l: float) -> str:
        """HSL 转 HEX"""
        return Color.from_hsl(h, s, l).hex
    
    @staticmethod
    def css_name_to_hex(name: str) -> Optional[str]:
        """CSS颜色名称转HEX"""
        css_colors = {
            'white': '#FFFFFF', 'black': '#000000', 'red': '#FF0000',
            'green': '#008000', 'blue': '#0000FF', 'yellow': '#FFFF00',
            'cyan': '#00FFFF', 'magenta': '#FF00FF', 'orange': '#FFA500',
            'purple': '#800080', 'pink': '#FFC0CB', 'brown': '#A52A2A',
            'gray': '#808080', 'grey': '#808080', 'silver': '#C0C0C0',
            'gold': '#FFD700', 'navy': '#000080', 'teal': '#008080',
            'maroon': '#800000', 'olive': '#808000', 'lime': '#00FF00',
            'aqua': '#00FFFF', 'fuchsia': '#FF00FF', 'coral': '#FF7F50',
            'crimson': '#DC143C', 'indigo': '#4B0082', 'violet': '#EE82EE',
            'turquoise': '#40E0D0', 'salmon': '#FA8072', 'khaki': '#F0E68C',
            'lavender': '#E6E6FA', 'beige': '#F5F5DC', 'ivory': '#FFFFF0',
            'mint': '#98FF98', 'peach': '#FFDAB9', 'tan': '#D2B48C',
        }
        return css_colors.get(name.lower())
    
    @staticmethod
    def parse_color(color_str: str) -> Optional[Color]:
        """
        解析各种格式的颜色字符串
        
        支持格式:
        - HEX: #RGB, #RRGGBB, #RRGGBBAA
        - RGB: rgb(r, g, b), rgba(r, g, b, a)
        - HSL: hsl(h, s%, l%), hsla(h, s%, l%, a)
        - CSS名称: red, blue, etc.
        """
        color_str = color_str.strip()
        
        # 尝试HEX
        if color_str.startswith('#'):
            try:
                return Color.from_hex(color_str)
            except:
                pass
        
        # 尝试CSS名称
        hex_val = ColorConverter.css_name_to_hex(color_str)
        if hex_val:
            return Color.from_hex(hex_val)
        
        # 尝试RGB/RGBA
        if color_str.startswith('rgb'):
            import re
            match = re.match(r'rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)', color_str)
            if match:
                r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
                a = float(match.group(4)) if match.group(4) else 1.0
                return Color(r, g, b, a)
        
        # 尝试HSL
        if color_str.startswith('hsl'):
            import re
            match = re.match(r'hsla?\s*\(\s*(\d+)\s*,\s*(\d+)%?\s*,\s*(\d+)%?\s*(?:,\s*([\d.]+))?\s*\)', color_str)
            if match:
                h, s, l = float(match.group(1)), float(match.group(2)), float(match.group(3))
                a = float(match.group(4)) if match.group(4) else 1.0
                return Color.from_hsl(h, s, l, a)
        
        return None


# 预定义颜色常量
class Colors:
    """常用颜色常量"""
    WHITE = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)
    RED = Color(255, 0, 0)
    GREEN = Color(0, 128, 0)
    BLUE = Color(0, 0, 255)
    YELLOW = Color(255, 255, 0)
    CYAN = Color(0, 255, 255)
    MAGENTA = Color(255, 0, 255)
    ORANGE = Color(255, 165, 0)
    PURPLE = Color(128, 0, 128)
    PINK = Color(255, 192, 203)
    BROWN = Color(165, 42, 42)
    GRAY = Color(128, 128, 128)
    NAVY = Color(0, 0, 128)
    TEAL = Color(0, 128, 128)
    LIME = Color(0, 255, 0)
    TRANSPARENT = Color(0, 0, 0, 0.0)