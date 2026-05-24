# -*- coding: utf-8 -*-
"""
Aspect Ratio Utilities - 宽高比计算工具

提供图片、视频宽高比计算和处理功能。
支持宽高比简化、分辨率计算、缩放、裁剪等操作。
零外部依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0
"""

from typing import Tuple, List, Optional, Dict, Union
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
import math


class AspectRatioPreset(Enum):
    """常见宽高比预设"""
    SQUARE = "1:1"                  # 正方形
    CLASSIC_FILM = "4:3"            # 经典电影/电视
    WIDESCREEN = "16:9"             # 宽屏
    ULTRAWIDE = "21:9"              # 超宽屏
    CINEMA_SCOPE = "2.39:1"         # 电影宽银幕
    IMAX = "1.43:1"                 # IMAX
    INSTAGRAM_SQUARE = "1:1"        # Instagram 正方形
    INSTAGRAM_PORTRAIT = "4:5"      # Instagram 竖版
    INSTAGRAM_STORY = "9:16"        # Instagram Story
    YOUTUBE_THUMBNAIL = "16:9"     # YouTube 缩略图
    TWITTER_CARD = "2:1"           # Twitter 卡片
    FACEBOOK_COVER = "2.05:1"       # Facebook 封面
    LINKEDIN_BANNER = "4:1"        # LinkedIn 横幅
    IPHONE = "19.5:9"              # iPhone
    IPAD = "4:3"                   # iPad
    ANDROID_STANDARD = "16:9"      # Android 标准
    ANDROID_TALL = "20:9"          # Android 长屏
    A4_PAPER = "1.414:1"           # A4 纸张
    GOLDEN_RATIO = "1.618:1"       # 黄金比例


@dataclass
class Resolution:
    """分辨率数据结构"""
    width: int
    height: int
    
    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Width and height must be positive integers")
    
    @property
    def pixels(self) -> int:
        """总像素数"""
        return self.width * self.height
    
    @property
    def megapixels(self) -> float:
        """百万像素"""
        return self.pixels / 1_000_000
    
    @property
    def aspect_ratio(self) -> Tuple[int, int]:
        """宽高比（简化后）"""
        return simplify_ratio(self.width, self.height)
    
    @property
    def aspect_ratio_float(self) -> float:
        """宽高比（浮点数）"""
        return self.width / self.height
    
    @property
    def orientation(self) -> str:
        """方向：landscape（横屏）、portrait（竖屏）、square（正方形）"""
        if self.width > self.height:
            return "landscape"
        elif self.width < self.height:
            return "portrait"
        else:
            return "square"
    
    @property
    def is_4k(self) -> bool:
        """是否为 4K 分辨率"""
        return self.width >= 3840 or self.height >= 2160
    
    @property
    def is_hd(self) -> bool:
        """是否为 HD 分辨率（720p 或更高）"""
        return self.height >= 720
    
    @property
    def is_full_hd(self) -> bool:
        """是否为 Full HD 分辨率（1080p）"""
        return self.height >= 1080
    
    def scale_to_width(self, new_width: int) -> 'Resolution':
        """缩放到指定宽度"""
        scale = new_width / self.width
        new_height = round(self.height * scale)
        return Resolution(new_width, new_height)
    
    def scale_to_height(self, new_height: int) -> 'Resolution':
        """缩放到指定高度"""
        scale = new_height / self.height
        new_width = round(self.width * scale)
        return Resolution(new_width, new_height)
    
    def scale_to_fit(self, max_width: int, max_height: int) -> 'Resolution':
        """缩放以适应指定尺寸（保持比例）"""
        scale = min(max_width / self.width, max_height / self.height)
        new_width = round(self.width * scale)
        new_height = round(self.height * scale)
        return Resolution(new_width, new_height)
    
    def scale_to_fill(self, min_width: int, min_height: int) -> 'Resolution':
        """缩放以填充指定尺寸（保持比例）"""
        scale = max(min_width / self.width, min_height / self.height)
        new_width = round(self.width * scale)
        new_height = round(self.height * scale)
        return Resolution(new_width, new_height)
    
    def to_tuple(self) -> Tuple[int, int]:
        """转换为元组"""
        return (self.width, self.height)
    
    def to_string(self) -> str:
        """转换为字符串（如 1920x1080）"""
        return f"{self.width}x{self.height}"
    
    @classmethod
    def from_string(cls, s: str) -> 'Resolution':
        """从字符串创建（支持 1920x1080、1920*1080、1920:1080 格式）"""
        for sep in ['x', 'X', '*', '×', ':']:
            if sep in s:
                parts = s.split(sep)
                if len(parts) == 2:
                    return cls(int(parts[0]), int(parts[1]))
        raise ValueError(f"Invalid resolution string: {s}")
    
    def __str__(self) -> str:
        return self.to_string()
    
    def __repr__(self) -> str:
        return f"Resolution({self.width}, {self.height})"


@dataclass
class AspectRatio:
    """宽高比数据结构"""
    width_ratio: int
    height_ratio: int
    
    def __post_init__(self):
        if self.width_ratio <= 0 or self.height_ratio <= 0:
            raise ValueError("Ratio values must be positive integers")
    
    @property
    def ratio(self) -> float:
        """宽高比浮点数"""
        return self.width_ratio / self.height_ratio
    
    @property
    def inverse(self) -> 'AspectRatio':
        """反向宽高比"""
        return AspectRatio(self.height_ratio, self.width_ratio)
    
    @classmethod
    def from_float(cls, ratio: float, max_denominator: int = 100) -> 'AspectRatio':
        """从浮点数创建宽高比"""
        fraction = Fraction(ratio).limit_denominator(max_denominator)
        return cls(fraction.numerator, fraction.denominator)
    
    @classmethod
    def from_resolution(cls, width: int, height: int) -> 'AspectRatio':
        """从分辨率创建宽高比"""
        w, h = simplify_ratio(width, height)
        return cls(w, h)
    
    @classmethod
    def from_preset(cls, preset: AspectRatioPreset) -> 'AspectRatio':
        """从预设创建宽高比"""
        return cls.from_string(preset.value)
    
    @classmethod
    def from_string(cls, s: str) -> 'AspectRatio':
        """从字符串创建（如 16:9，支持小数如 2.39:1）"""
        if ':' in s:
            parts = s.split(':')
            if len(parts) == 2:
                # 支持整数和小数
                try:
                    w = float(parts[0])
                    h = float(parts[1])
                    # 如果是整数，直接使用
                    if w == int(w) and h == int(h):
                        return cls(int(w), int(h))
                    # 如果是小数，转换为分数
                    fraction = Fraction(w / h).limit_denominator(1000)
                    return cls(fraction.numerator, fraction.denominator)
                except ValueError:
                    raise ValueError(f"Invalid aspect ratio string: {s}")
        raise ValueError(f"Invalid aspect ratio string: {s}")
    
    def to_string(self) -> str:
        """转换为字符串"""
        return f"{self.width_ratio}:{self.height_ratio}"
    
    def get_resolution_for_width(self, width: int) -> Resolution:
        """根据宽度计算分辨率"""
        height = round(width * self.height_ratio / self.width_ratio)
        return Resolution(width, height)
    
    def get_resolution_for_height(self, height: int) -> Resolution:
        """根据高度计算分辨率"""
        width = round(height * self.width_ratio / self.height_ratio)
        return Resolution(width, height)
    
    def __str__(self) -> str:
        return self.to_string()
    
    def __repr__(self) -> str:
        return f"AspectRatio({self.width_ratio}, {self.height_ratio})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, AspectRatio):
            return (self.width_ratio * other.height_ratio == 
                    self.height_ratio * other.width_ratio)
        return False


# ============================================================================
# 核心函数
# ============================================================================

def gcd(a: int, b: int) -> int:
    """计算最大公约数"""
    while b:
        a, b = b, a % b
    return a


def simplify_ratio(width: int, height: int) -> Tuple[int, int]:
    """
    简化宽高比
    
    Args:
        width: 宽度
        height: 高度
        
    Returns:
        简化后的 (width, height) 元组
        
    Examples:
        >>> simplify_ratio(1920, 1080)
        (16, 9)
        >>> simplify_ratio(3840, 2160)
        (16, 9)
    """
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive")
    
    divisor = gcd(width, height)
    return (width // divisor, height // divisor)


def calculate_aspect_ratio(width: int, height: int) -> AspectRatio:
    """
    计算宽高比
    
    Args:
        width: 宽度
        height: 高度
        
    Returns:
        AspectRatio 对象
    """
    return AspectRatio.from_resolution(width, height)


def is_same_ratio(w1: int, h1: int, w2: int, h2: int) -> bool:
    """
    判断两个分辨率是否具有相同的宽高比
    
    Args:
        w1, h1: 第一个分辨率
        w2, h2: 第二个分辨率
        
    Returns:
        是否相同宽高比
    """
    return simplify_ratio(w1, h1) == simplify_ratio(w2, h2)


def scale_to_width(original_width: int, original_height: int, new_width: int) -> Tuple[int, int]:
    """
    缩放到指定宽度（保持宽高比）
    
    Args:
        original_width: 原始宽度
        original_height: 原始高度
        new_width: 目标宽度
        
    Returns:
        (新宽度, 新高度) 元组
    """
    scale = new_width / original_width
    new_height = round(original_height * scale)
    return (new_width, new_height)


def scale_to_height(original_width: int, original_height: int, new_height: int) -> Tuple[int, int]:
    """
    缩放到指定高度（保持宽高比）
    
    Args:
        original_width: 原始宽度
        original_height: 原始高度
        new_height: 目标高度
        
    Returns:
        (新宽度, 新高度) 元组
    """
    scale = new_height / original_height
    new_width = round(original_width * scale)
    return (new_width, new_height)


def scale_to_fit(
    original_width: int, 
    original_height: int, 
    max_width: int, 
    max_height: int
) -> Tuple[int, int]:
    """
    缩放以适应指定尺寸（保持宽高比，不超出边界）
    
    Args:
        original_width: 原始宽度
        original_height: 原始高度
        max_width: 最大宽度
        max_height: 最大高度
        
    Returns:
        (新宽度, 新高度) 元组
    """
    scale = min(max_width / original_width, max_height / original_height)
    new_width = round(original_width * scale)
    new_height = round(original_height * scale)
    return (new_width, new_height)


def scale_to_fill(
    original_width: int, 
    original_height: int, 
    min_width: int, 
    min_height: int
) -> Tuple[int, int]:
    """
    缩放以填充指定尺寸（保持宽高比，完全覆盖）
    
    Args:
        original_width: 原始宽度
        original_height: 原始高度
        min_width: 最小宽度
        min_height: 最小高度
        
    Returns:
        (新宽度, 新高度) 元组
    """
    scale = max(min_width / original_width, min_height / original_height)
    new_width = round(original_width * scale)
    new_height = round(original_height * scale)
    return (new_width, new_height)


def calculate_crop(
    original_width: int, 
    original_height: int, 
    target_ratio: Union[str, Tuple[int, int], AspectRatio]
) -> Dict[str, int]:
    """
    计算居中裁剪区域
    
    Args:
        original_width: 原始宽度
        original_height: 原始高度
        target_ratio: 目标宽高比（字符串如 "16:9" 或元组或 AspectRatio）
        
    Returns:
        包含 x, y, width, height 的字典，表示裁剪区域
    """
    if isinstance(target_ratio, str):
        ratio = AspectRatio.from_string(target_ratio)
    elif isinstance(target_ratio, tuple):
        ratio = AspectRatio(target_ratio[0], target_ratio[1])
    else:
        ratio = target_ratio
    
    original_ratio = original_width / original_height
    target_ratio_float = ratio.ratio
    
    if original_ratio > target_ratio_float:
        # 原图更宽，需要裁剪左右
        new_width = round(original_height * target_ratio_float)
        new_height = original_height
        x = (original_width - new_width) // 2
        y = 0
    else:
        # 原图更高，需要裁剪上下
        new_width = original_width
        new_height = round(original_width / target_ratio_float)
        x = 0
        y = (original_height - new_height) // 2
    
    return {
        'x': x,
        'y': y,
        'width': new_width,
        'height': new_height
    }


def calculate_letterbox(
    original_width: int, 
    original_height: int, 
    target_width: int, 
    target_height: int
) -> Dict[str, int]:
    """
    计算黑边（letterbox/pillarbox）区域
    
    Args:
        original_width: 原始宽度
        original_height: 原始高度
        target_width: 目标宽度
        target_height: 目标高度
        
    Returns:
        包含视频位置和黑边信息的字典
    """
    # 缩放以适应目标尺寸
    scaled_width, scaled_height = scale_to_fit(
        original_width, original_height, target_width, target_height
    )
    
    # 计算居中位置
    x = (target_width - scaled_width) // 2
    y = (target_height - scaled_height) // 2
    
    # 计算黑边
    horizontal_bars = target_height - scaled_height
    vertical_bars = target_width - scaled_width
    
    return {
        'video_x': x,
        'video_y': y,
        'video_width': scaled_width,
        'video_height': scaled_height,
        'top_bar': horizontal_bars // 2,
        'bottom_bar': horizontal_bars - horizontal_bars // 2,
        'left_bar': vertical_bars // 2,
        'right_bar': vertical_bars - vertical_bars // 2,
        'is_letterbox': horizontal_bars > 0,  # 上下黑边
        'is_pillarbox': vertical_bars > 0     # 左右黑边
    }


def find_common_resolutions(ratio: Union[str, Tuple[int, int], AspectRatio], max_pixels: int = 8294400) -> List[Resolution]:
    """
    根据宽高比找出常见的分辨率
    
    Args:
        ratio: 宽高比
        max_pixels: 最大像素数（默认 4K）
        
    Returns:
        Resolution 列表
    """
    if isinstance(ratio, str):
        aspect = AspectRatio.from_string(ratio)
    elif isinstance(ratio, tuple):
        aspect = AspectRatio(ratio[0], ratio[1])
    else:
        aspect = ratio
    
    resolutions = []
    
    # 从较小宽度开始，逐步增加
    for width in range(100, 8000, 100):
        height = round(width * aspect.height_ratio / aspect.width_ratio)
        pixels = width * height
        
        if pixels > max_pixels:
            break
        
        # 只保留合理的分辨率（高度在合理范围内）
        if 100 <= height <= 5000:
            # 检查是否与已有分辨率相同（简化后）
            simplified = simplify_ratio(width, height)
            if simplified == (aspect.width_ratio, aspect.height_ratio):
                resolutions.append(Resolution(width, height))
    
    return resolutions


def match_preset(width: int, height: int, tolerance: float = 0.01) -> Optional[AspectRatioPreset]:
    """
    匹配预设宽高比
    
    Args:
        width: 宽度
        height: 高度
        tolerance: 容差（默认 1%）
        
    Returns:
        匹配的预设，如果没有匹配则返回 None
    """
    actual_ratio = width / height
    
    for preset in AspectRatioPreset:
        preset_ratio = AspectRatio.from_string(preset.value).ratio
        if abs(actual_ratio - preset_ratio) / preset_ratio <= tolerance:
            return preset
    
    return None


def get_resolution_name(width: int, height: int) -> str:
    """
    获取分辨率的通用名称
    
    Args:
        width: 宽度
        height: 高度
        
    Returns:
        分辨率名称
    """
    # 标准分辨率映射
    standard_names = {
        (640, 480): "SD (480p)",
        (854, 480): "SD Wide (480p)",
        (1280, 720): "HD (720p)",
        (1920, 1080): "Full HD (1080p)",
        (2560, 1440): "QHD (1440p)",
        (3840, 2160): "4K UHD (2160p)",
        (4096, 2160): "4K DCI",
        (5120, 2880): "5K",
        (7680, 4320): "8K UHD",
        (1024, 768): "XGA",
        (1280, 1024): "SXGA",
        (1600, 1200): "UXGA",
        (2048, 1536): "QXGA",
        (320, 240): "QVGA",
        (176, 144): "QCIF",
        (352, 288): "CIF",
        (704, 576): "4CIF",
    }
    
    # 标准化分辨率
    key = (width, height)
    
    if key in standard_names:
        return standard_names[key]
    
    # 根据高度判断
    if height <= 480:
        return f"SD ({height}p)"
    elif height <= 720:
        return f"HD Ready ({height}p)"
    elif height <= 1080:
        return f"HD ({height}p)"
    elif height <= 1440:
        return f"QHD ({height}p)"
    elif height <= 2160:
        return f"4K ({height}p)"
    elif height <= 4320:
        return f"8K ({height}p)"
    else:
        return f"{height}p"


def calculate_print_size(
    width: int, 
    height: int, 
    dpi: int = 300
) -> Dict[str, Union[float, Tuple[float, float]]]:
    """
    计算打印尺寸
    
    Args:
        width: 像素宽度
        height: 像素高度
        dpi: 每英寸点数（默认 300）
        
    Returns:
        包含英寸和厘米尺寸的字典
    """
    inches_width = width / dpi
    inches_height = height / dpi
    
    cm_width = inches_width * 2.54
    cm_height = inches_height * 2.54
    
    return {
        'inches': (round(inches_width, 2), round(inches_height, 2)),
        'centimeters': (round(cm_width, 2), round(cm_height, 2)),
        'dpi': dpi,
        'pixels': (width, height)
    }


def get_optimal_resolution(
    target_ratio: Union[str, Tuple[int, int], AspectRatio],
    min_pixels: int = 2073600,  # 1920x1080
    max_pixels: int = 8294400    # 3840x2160
) -> Resolution:
    """
    获取最优分辨率
    
    Args:
        target_ratio: 目标宽高比
        min_pixels: 最小像素数
        max_pixels: 最大像素数
        
    Returns:
        最优分辨率
    """
    if isinstance(target_ratio, str):
        ratio = AspectRatio.from_string(target_ratio)
    elif isinstance(target_ratio, tuple):
        ratio = AspectRatio(target_ratio[0], target_ratio[1])
    else:
        ratio = target_ratio
    
    # 计算目标像素数的对应尺寸
    # 对于比例 w:h，设宽度为 W，高度为 H
    # W/H = w/h => W = H * w/h
    # 像素数 = W * H = H^2 * w/h
    # 因此 H = sqrt(pixels * h / w)
    
    target_pixels = (min_pixels + max_pixels) // 2
    
    # 根据比例和像素数计算高度
    height = int(math.sqrt(target_pixels * ratio.height_ratio / ratio.width_ratio))
    width = round(height * ratio.width_ratio / ratio.height_ratio)
    
    # 确保在范围内（调整高度）
    while width * height < min_pixels:
        height += 10
        width = round(height * ratio.width_ratio / ratio.height_ratio)
    
    while width * height > max_pixels:
        height -= 10
        width = round(height * ratio.width_ratio / ratio.height_ratio)
    
    # 确保是偶数（视频编码通常需要）
    width = width if width % 2 == 0 else width + 1
    height = height if height % 2 == 0 else height + 1
    
    return Resolution(width, height)


# ============================================================================
# 预设分辨率
# ============================================================================

COMMON_RESOLUTIONS: Dict[str, Resolution] = {
    # SD
    '480p': Resolution(640, 480),
    '480p_wide': Resolution(854, 480),
    
    # HD
    '720p': Resolution(1280, 720),
    '1080p': Resolution(1920, 1080),
    
    # QHD
    '1440p': Resolution(2560, 1440),
    
    # 4K
    '4k': Resolution(3840, 2160),
    '4k_dci': Resolution(4096, 2160),
    
    # 5K
    '5k': Resolution(5120, 2880),
    
    # 8K
    '8k': Resolution(7680, 4320),
    
    # 社交媒体
    'instagram_square': Resolution(1080, 1080),
    'instagram_portrait': Resolution(1080, 1350),
    'instagram_story': Resolution(1080, 1920),
    'youtube_thumbnail': Resolution(1280, 720),
    'twitter_card': Resolution(1200, 600),
    'facebook_cover': Resolution(820, 312),
    'linkedin_banner': Resolution(1584, 396),
    
    # 移动设备
    'iphone_14': Resolution(1170, 2532),
    'iphone_14_pro': Resolution(1179, 2556),
    'iphone_14_pro_max': Resolution(1290, 2796),
    'ipad_pro': Resolution(2048, 2732),
    
    # 显示器
    'vga': Resolution(640, 480),
    'svga': Resolution(800, 600),
    'xga': Resolution(1024, 768),
    'sxga': Resolution(1280, 1024),
    'uxga': Resolution(1600, 1200),
    'wuxga': Resolution(1920, 1200),
    'wqhd': Resolution(2560, 1440),
    'wqhd_ultrawide': Resolution(3440, 1440),
}


# ============================================================================
# 模块元数据
# ============================================================================

__version__ = "1.0.0"
__author__ = "AllToolkit"
__all__ = [
    # 枚举
    'AspectRatioPreset',
    
    # 数据类
    'Resolution',
    'AspectRatio',
    
    # 核心函数
    'gcd',
    'simplify_ratio',
    'calculate_aspect_ratio',
    'is_same_ratio',
    'scale_to_width',
    'scale_to_height',
    'scale_to_fit',
    'scale_to_fill',
    'calculate_crop',
    'calculate_letterbox',
    'find_common_resolutions',
    'match_preset',
    'get_resolution_name',
    'calculate_print_size',
    'get_optimal_resolution',
    
    # 常量
    'COMMON_RESOLUTIONS',
]