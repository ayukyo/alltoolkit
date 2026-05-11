#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Color Utilities Module
====================================
A comprehensive color processing utility module for Python with zero external dependencies.

Features:
    - Color format conversion (HEX, RGB, HSL, HSV, CMYK, LAB)
    - Color validation and parsing
    - Color mixing and blending
    - Contrast ratio calculation (WCAG compliance)
    - Color palette generation
    - Color harmony (complementary, triadic, analogous, etc.)
    - Color temperature and perceived lightness
    - Color distance and similarity
    - Gradient generation

Author: AllToolkit Contributors
License: MIT
"""

import math
import random
from typing import Union, Tuple, List, Optional, Dict
from dataclasses import dataclass


# ============================================================================
# Constants
# ============================================================================

# Predefined named colors (CSS Color Module Level 4 subset)
CSS_COLORS = {
    # Basic colors
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 128, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    # Extended colors
    'orange': (255, 165, 0),
    'pink': (255, 192, 203),
    'purple': (128, 0, 128),
    'brown': (165, 42, 42),
    'gray': (128, 128, 128),
    'grey': (128, 128, 128),
    'silver': (192, 192, 192),
    'gold': (255, 215, 0),
    'navy': (0, 0, 128),
    'teal': (0, 128, 128),
    'olive': (128, 128, 0),
    'maroon': (128, 0, 0),
    'lime': (0, 255, 0),
    'aqua': (0, 255, 255),
    'fuchsia': (255, 0, 255),
    'coral': (255, 127, 80),
    'salmon': (250, 128, 114),
    'khaki': (240, 230, 140),
    'violet': (238, 130, 238),
    'indigo': (75, 0, 130),
    'crimson': (220, 20, 60),
    'chocolate': (210, 105, 30),
    'turquoise': (64, 224, 208),
    'forestgreen': (34, 139, 34),
    'slateblue': (106, 90, 205),
    'tomato': (255, 99, 71),
    'sienna': (160, 82, 45),
    'orchid': (218, 112, 214),
    'peru': (205, 133, 63),
    'plum': (221, 160, 221),
    'wheat': (245, 222, 179),
    'tan': (210, 180, 140),
    'steelblue': (70, 130, 180),
    'royalblue': (65, 105, 225),
    'seagreen': (46, 139, 87),
    'sandybrown': (244, 164, 96),
    'powderblue': (176, 224, 230),
    'papayawhip': (255, 239, 213),
    'paleturquoise': (175, 238, 238),
    'palegreen': (152, 251, 152),
    'palegoldenrod': (238, 232, 170),
    'navajowhite': (255, 222, 173),
    'mediumvioletred': (199, 21, 133),
    'mediumturquoise': (72, 209, 204),
    'mediumspringgreen': (0, 250, 154),
    'mediumseagreen': (60, 179, 113),
    'mediumpurple': (147, 112, 219),
    'mediumorchid': (186, 85, 211),
    'mediumblue': (0, 0, 205),
    'mediumaquamarine': (102, 205, 170),
    'maroon': (128, 0, 0),
    'limegreen': (50, 205, 50),
    'lightyellow': (255, 255, 224),
    'lightsteelblue': (176, 196, 222),
    'lightslategray': (119, 136, 153),
    'lightslategrey': (119, 136, 153),
    'lightsalmon': (255, 160, 122),
    'lightseagreen': (32, 178, 170),
    'lightskyblue': (135, 206, 250),
    'lightpink': (255, 182, 193),
    'lightgreen': (144, 238, 144),
    'lightgray': (211, 211, 211),
    'lightgrey': (211, 211, 211),
    'lightgoldenrodyellow': (250, 250, 210),
    'lightcyan': (224, 255, 255),
    'lightcoral': (240, 128, 128),
    'lightblue': (173, 216, 230),
    'lemonchiffon': (255, 250, 205),
    'lavenderblush': (255, 240, 245),
    'lavender': (230, 230, 250),
    'lawngreen': (124, 252, 0),
    'ivory': (255, 255, 240),
    'hotpink': (255, 105, 180),
    'honeydew': (240, 255, 240),
    'greenyellow': (173, 255, 47),
    'gainsboro': (220, 220, 220),
    'floralwhite': (255, 250, 240),
    'firebrick': (178, 34, 34),
    'dodgerblue': (30, 144, 255),
    'dimgray': (105, 105, 105),
    'dimgrey': (105, 105, 105),
    'deepskyblue': (0, 191, 255),
    'deeppink': (255, 20, 147),
    'darkviolet': (148, 0, 211),
    'darkturquoise': (0, 206, 209),
    'darkslategray': (47, 79, 79),
    'darkslategrey': (47, 79, 79),
    'darkslateblue': (72, 61, 139),
    'darkseagreen': (143, 188, 143),
    'darksalmon': (233, 150, 122),
    'darkred': (139, 0, 0),
    'darkorchid': (153, 50, 204),
    'darkorange': (255, 140, 0),
    'darkolivegreen': (85, 107, 47),
    'darkmagenta': (139, 0, 139),
    'darkkhaki': (189, 183, 107),
    'darkgreen': (0, 100, 0),
    'darkgray': (169, 169, 169),
    'darkgrey': (169, 169, 169),
    'darkgoldenrod': (184, 134, 11),
    'darkcyan': (0, 139, 139),
    'darkblue': (0, 0, 139),
    'cornsilk': (255, 248, 220),
    'cornflowerblue': (100, 149, 237),
    'chartreuse': (127, 255, 0),
    'burlywood': (222, 184, 135),
    'bisque': (255, 228, 196),
    'beige': (245, 245, 220),
    'azure': (240, 255, 255),
    'aquamarine': (127, 255, 212),
    'antiquewhite': (250, 235, 215),
    'aliceblue': (240, 248, 255),
    ' BlanchedAlmond': (255, 235, 205),
    'blueviolet': (138, 43, 226),
    'cadetblue': (95, 158, 160),
    'chocolate': (210, 105, 30),
    'darkgray': (169, 169, 169),
    'darkolivegreen': (85, 107, 47),
    'darkorange': (255, 140, 0),
    'firebrick': (178, 34, 34),
    'goldenrod': (218, 165, 32),
    'green': (0, 128, 0),
    'hotpink': (255, 105, 180),
    ' indianred': (205, 92, 92),
    'lavender': (230, 230, 250),
    'lightblue': (173, 216, 230),
    'lightgreen': (144, 238, 144),
    'lightsalmon': (255, 160, 122),
    'mediumblue': (0, 0, 205),
    'midnightblue': (25, 25, 112),
    'navajowhite': (255, 222, 173),
    'orangered': (255, 69, 0),
    'palegreen': (152, 251, 152),
    'rebeccapurple': (102, 51, 153),
    'rosybrown': (188, 143, 143),
    'saddlebrown': (139, 69, 19),
    'skyblue': (135, 206, 235),
    'springgreen': (0, 255, 127),
    'thistle': (216, 191, 216),
    'yellowgreen': (154, 205, 50),
}

# D65 illuminant reference white point
D65_WHITE = (95.047, 100.0, 108.883)


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class RGB:
    """RGB color representation."""
    r: int  # 0-255
    g: int  # 0-255
    b: int  # 0-255
    
    def __post_init__(self):
        """Validate RGB values."""
        self.r = max(0, min(255, int(self.r)))
        self.g = max(0, min(255, int(self.g)))
        self.b = max(0, min(255, int(self.b)))
    
    def to_hex(self) -> str:
        """Convert to HEX string."""
        return f'#{self.r:02x}{self.g:02x}{self.b:02x}'
    
    def to_hsl(self) -> Tuple[float, float, float]:
        """Convert to HSL."""
        return rgb_to_hsl(self.r, self.g, self.b)
    
    def to_hsv(self) -> Tuple[float, float, float]:
        """Convert to HSV."""
        return rgb_to_hsv(self.r, self.g, self.b)
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert to tuple."""
        return (self.r, self.g, self.b)


@dataclass
class HSL:
    """HSL color representation."""
    h: float  # 0-360
    s: float  # 0-100
    l: float  # 0-100
    
    def __post_init__(self):
        """Normalize HSL values."""
        self.h = self.h % 360
        self.s = max(0, min(100, self.s))
        self.l = max(0, min(100, self.l))
    
    def to_rgb(self) -> RGB:
        """Convert to RGB."""
        r, g, b = hsl_to_rgb(self.h, self.s, self.l)
        return RGB(r, g, b)
    
    def to_hex(self) -> str:
        """Convert to HEX."""
        return self.to_rgb().to_hex()


@dataclass
class ColorInfo:
    """Comprehensive color information container."""
    hex: str
    rgb: RGB
    hsl: HSL
    hsv: Tuple[float, float, float]
    cmyk: Tuple[float, float, float, float]
    lab: Tuple[float, float, float]
    name: Optional[str]
    luminance: float
    temperature: str  # 'warm', 'cool', or 'neutral'


# ============================================================================
# Color Validation and Parsing
# ============================================================================

def is_valid_hex(hex_color: str) -> bool:
    """
    Validate a HEX color string.
    
    Args:
        hex_color: HEX color string (e.g., '#FF0000', 'FF0000', '#F00', 'F00')
    
    Returns:
        True if valid HEX color, False otherwise
    
    Examples:
        >>> is_valid_hex('#FF0000')
        True
        >>> is_valid_hex('FF0000')
        True
        >>> is_valid_hex('#F00')
        True
        >>> is_valid_hex('invalid')
        False
    """
    if not hex_color or not isinstance(hex_color, str):
        return False
    
    hex_color = hex_color.strip()
    
    # Remove leading #
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    
    # Check valid characters
    if not all(c in '0123456789abcdefABCDEF' for c in hex_color):
        return False
    
    # Check length (3 or 6)
    return len(hex_color) in (3, 6)


def parse_hex(hex_color: str) -> RGB:
    """
    Parse a HEX color string to RGB.
    
    Args:
        hex_color: HEX color string
    
    Returns:
        RGB object
    
    Raises:
        ValueError: If invalid HEX color
    
    Examples:
        >>> parse_hex('#FF0000')
        RGB(r=255, g=0, b=0)
        >>> parse_hex('#F00')
        RGB(r=255, g=0, b=0)
    """
    if not is_valid_hex(hex_color):
        raise ValueError(f"Invalid HEX color: {hex_color}")
    
    hex_color = hex_color.strip().lstrip('#')
    
    if len(hex_color) == 3:
        hex_color = ''.join([c * 2 for c in hex_color])
    
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    return RGB(r, g, b)


def parse_rgb_string(rgb_string: str) -> RGB:
    """
    Parse an RGB string (e.g., 'rgb(255, 0, 0)').
    
    Args:
        rgb_string: RGB string in format 'rgb(r, g, b)' or 'r, g, b'
    
    Returns:
        RGB object
    
    Raises:
        ValueError: If invalid RGB string
    
    Examples:
        >>> parse_rgb_string('rgb(255, 0, 0)')
        RGB(r=255, g=0, b=0)
        >>> parse_rgb_string('255, 0, 0')
        RGB(r=255, g=0, b=0)
    """
    rgb_string = rgb_string.strip()
    
    # Remove 'rgb(' and ')'
    if rgb_string.startswith('rgb('):
        rgb_string = rgb_string[4:]
    if rgb_string.endswith(')'):
        rgb_string = rgb_string[:-1]
    
    parts = [p.strip() for p in rgb_string.split(',')]
    
    if len(parts) != 3:
        raise ValueError(f"Invalid RGB string: {rgb_string}")
    
    try:
        r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        raise ValueError(f"Invalid RGB values: {rgb_string}")
    
    return RGB(r, g, b)


def parse_color(color: Union[str, Tuple[int, int, int], RGB]) -> RGB:
    """
    Parse a color from various formats.
    
    Args:
        color: Color in any supported format (HEX string, RGB tuple, RGB object, or named color)
    
    Returns:
        RGB object
    
    Raises:
        ValueError: If color format is not recognized
    
    Examples:
        >>> parse_color('#FF0000')
        RGB(r=255, g=0, b=0)
        >>> parse_color((255, 0, 0))
        RGB(r=255, g=0, b=0)
        >>> parse_color('red')
        RGB(r=255, g=0, b=0)
    """
    if isinstance(color, RGB):
        return color
    
    if isinstance(color, tuple):
        if len(color) == 3:
            return RGB(color[0], color[1], color[2])
        raise ValueError(f"Invalid tuple length: {len(color)}")
    
    if isinstance(color, str):
        color = color.strip()
        
        # HEX format
        if color.startswith('#') or (len(color) in (3, 6) and all(c in '0123456789abcdefABCDEF' for c in color)):
            return parse_hex(color)
        
        # rgb() format
        if color.startswith('rgb('):
            return parse_rgb_string(color)
        
        # Named color
        color_lower = color.lower()
        if color_lower in CSS_COLORS:
            r, g, b = CSS_COLORS[color_lower]
            return RGB(r, g, b)
        
        # Try as hex without #
        if is_valid_hex(color):
            return parse_hex(color)
        
        raise ValueError(f"Unknown color: {color}")
    
    raise ValueError(f"Invalid color type: {type(color)}")


def get_color_name(rgb: Union[RGB, Tuple[int, int, int]]) -> Optional[str]:
    """
    Find the closest named CSS color for an RGB value.
    
    Args:
        rgb: RGB color
    
    Returns:
        Name of the closest CSS color, or None if no match
    
    Examples:
        >>> get_color_name((255, 0, 0))
        'red'
        >>> get_color_name((255, 255, 255))
        'white'
    """
    if isinstance(rgb, tuple):
        rgb = RGB(rgb[0], rgb[1], rgb[2])
    
    min_distance = float('inf')
    closest_name = None
    
    for name, color in CSS_COLORS.items():
        distance = color_distance(rgb.to_tuple(), color)
        if distance < min_distance:
            min_distance = distance
            closest_name = name
    
    # Only return name if close enough
    if min_distance < 50:
        return closest_name
    return None


# ============================================================================
# Color Format Conversions
# ============================================================================

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB values to HEX string.
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
    
    Returns:
        HEX color string
    
    Examples:
        >>> rgb_to_hex(255, 0, 0)
        '#ff0000'
        >>> rgb_to_hex(0, 128, 255)
        '#0080ff'
    """
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    return f'#{r:02x}{g:02x}{b:02x}'


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert HEX string to RGB tuple.
    
    Args:
        hex_color: HEX color string
    
    Returns:
        Tuple of (r, g, b)
    
    Examples:
        >>> hex_to_rgb('#FF0000')
        (255, 0, 0)
        >>> hex_to_rgb('FF0000')
        (255, 0, 0)
    """
    rgb = parse_hex(hex_color)
    return rgb.to_tuple()


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    Convert RGB to HSL.
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
    
    Returns:
        Tuple of (h, s, l) where h is 0-360, s and l are 0-100
    
    Examples:
        >>> rgb_to_hsl(255, 0, 0)
        (0.0, 100.0, 50.0)
        >>> rgb_to_hsl(0, 255, 0)
        (120.0, 100.0, 50.0)
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    diff = max_val - min_val
    
    # Lightness
    l = (max_val + min_val) / 2
    
    # Saturation
    if diff == 0:
        s = 0
        h = 0
    else:
        s = diff / (1 - abs(2 * l - 1))
        
        # Hue
        if max_val == r:
            h = ((g - b) / diff) % 6
        elif max_val == g:
            h = (b - r) / diff + 2
        else:
            h = (r - g) / diff + 4
        
        h *= 60
        if h < 0:
            h += 360
    
    return (h, s * 100, l * 100)


def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    """
    Convert HSL to RGB.
    
    Args:
        h: Hue (0-360)
        s: Saturation (0-100)
        l: Lightness (0-100)
    
    Returns:
        Tuple of (r, g, b) where each is 0-255
    
    Examples:
        >>> hsl_to_rgb(0, 100, 50)
        (255, 0, 0)
        >>> hsl_to_rgb(120, 100, 50)
        (0, 255, 0)
    """
    h = h % 360
    s = max(0, min(100, s)) / 100
    l = max(0, min(100, l)) / 100
    
    if s == 0:
        r = g = b = int(l * 255)
        return (r, g, b)
    
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
    
    r = hue_to_rgb(p, q, h / 360 + 1/3)
    g = hue_to_rgb(p, q, h / 360)
    b = hue_to_rgb(p, q, h / 360 - 1/3)
    
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    Convert RGB to HSV.
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
    
    Returns:
        Tuple of (h, s, v) where h is 0-360, s and v are 0-100
    
    Examples:
        >>> rgb_to_hsv(255, 0, 0)
        (0.0, 100.0, 100.0)
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    diff = max_val - min_val
    
    # Value
    v = max_val
    
    # Saturation
    s = 0 if max_val == 0 else diff / max_val
    
    # Hue
    if diff == 0:
        h = 0
    else:
        if max_val == r:
            h = ((g - b) / diff) % 6
        elif max_val == g:
            h = (b - r) / diff + 2
        else:
            h = (r - g) / diff + 4
        
        h *= 60
        if h < 0:
            h += 360
    
    return (h, s * 100, v * 100)


def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
    """
    Convert HSV to RGB.
    
    Args:
        h: Hue (0-360)
        s: Saturation (0-100)
        v: Value (0-100)
    
    Returns:
        Tuple of (r, g, b) where each is 0-255
    
    Examples:
        >>> hsv_to_rgb(0, 100, 100)
        (255, 0, 0)
    """
    h = h % 360
    s = max(0, min(100, s)) / 100
    v = max(0, min(100, v)) / 100
    
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    return (int(round((r + m) * 255)), int(round((g + m) * 255)), int(round((b + m) * 255)))


def rgb_to_cmyk(r: int, g: int, b: int) -> Tuple[float, float, float, float]:
    """
    Convert RGB to CMYK.
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
    
    Returns:
        Tuple of (c, m, y, k) where each is 0-100
    
    Examples:
        >>> rgb_to_cmyk(255, 255, 255)
        (0.0, 0.0, 0.0, 0.0)
        >>> rgb_to_cmyk(0, 0, 0)
        (0.0, 0.0, 0.0, 100.0)
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    
    if r == g == b == 0:
        return (0.0, 0.0, 0.0, 100.0)
    
    k = 1 - max(r, g, b)
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    
    return (c * 100, m * 100, y * 100, k * 100)


def cmyk_to_rgb(c: float, m: float, y: float, k: float) -> Tuple[int, int, int]:
    """
    Convert CMYK to RGB.
    
    Args:
        c: Cyan (0-100)
        m: Magenta (0-100)
        y: Yellow (0-100)
        k: Black (0-100)
    
    Returns:
        Tuple of (r, g, b) where each is 0-255
    
    Examples:
        >>> cmyk_to_rgb(0, 0, 0, 0)
        (255, 255, 255)
        >>> cmyk_to_rgb(0, 0, 0, 100)
        (0, 0, 0)
    """
    c, m, y, k = c / 100, m / 100, y / 100, k / 100
    
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    
    return (int(round(r)), int(round(g)), int(round(b)))


def rgb_to_lab(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    Convert RGB to LAB color space.
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
    
    Returns:
        Tuple of (L, a, b) where L is 0-100, a and b are typically -128 to 128
    
    Examples:
        >>> rgb_to_lab(255, 255, 255)
        (100.0, 0.0, 0.0)
        >>> rgb_to_lab(0, 0, 0)
        (0.0, 0.0, 0.0)
    """
    # RGB to XYZ
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    
    # Apply gamma correction
    def gamma_correct(c):
        if c > 0.04045:
            return ((c + 0.055) / 1.055) ** 2.4
        return c / 12.92
    
    r = gamma_correct(r)
    g = gamma_correct(g)
    b = gamma_correct(b)
    
    # Multiply by transformation matrix
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
    
    # Normalize by D65 white point
    x = x * 100 / D65_WHITE[0]
    y = y * 100 / D65_WHITE[1]
    z = z * 100 / D65_WHITE[2]
    
    # XYZ to LAB
    def f(t):
        if t > 0.008856:
            return t ** (1/3)
        return (903.3 * t + 16) / 116
    
    L = 116 * f(y) - 16
    a = 500 * (f(x) - f(y))
    b_val = 200 * (f(y) - f(z))
    
    return (L, a, b_val)


def lab_to_rgb(L: float, a: float, b_val: float) -> Tuple[int, int, int]:
    """
    Convert LAB to RGB color space.
    
    Args:
        L: Lightness (0-100)
        a: a component (typically -128 to 128)
        b_val: b component (typically -128 to 128)
    
    Returns:
        Tuple of (r, g, b) where each is 0-255
    
    Examples:
        >>> lab_to_rgb(100, 0, 0)
        (255, 255, 255)
        >>> lab_to_rgb(0, 0, 0)
        (0, 0, 0)
    """
    # LAB to XYZ
    def f_inv(t):
        if t > 0.206893:
            return t ** 3
        return (t - 16/116) / 7.787
    
    y = (L + 16) / 116
    x = a / 500 + y
    z = y - b_val / 200
    
    x = f_inv(x) * D65_WHITE[0] / 100
    y = f_inv(y) * D65_WHITE[1] / 100
    z = f_inv(z) * D65_WHITE[2] / 100
    
    # XYZ to RGB
    r = x * 3.2404542 + y * -1.5371385 + z * -0.4985314
    g = x * -0.9692660 + y * 1.8760108 + z * 0.0415560
    b = x * 0.0556434 + y * -0.2040259 + z * 1.0572252
    
    # Apply inverse gamma correction
    def gamma_uncorrect(c):
        if c > 0.0031308:
            return 1.055 * (c ** (1/2.4)) - 0.055
        return c * 12.92
    
    r = gamma_uncorrect(r)
    g = gamma_uncorrect(g)
    b = gamma_uncorrect(b)
    
    # Clamp to 0-1 range
    r = max(0, min(1, r))
    g = max(0, min(1, g))
    b = max(0, min(1, b))
    
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


# ============================================================================
# Color Analysis Functions
# ============================================================================

def get_luminance(color: Union[str, Tuple[int, int, int], RGB]) -> float:
    """
    Calculate relative luminance of a color (WCAG definition).
    
    Args:
        color: Color in any supported format
    
    Returns:
        Relative luminance (0.0 to 1.0)
    
    Examples:
        >>> get_luminance('#FFFFFF')
        1.0
        >>> get_luminance('#000000')
        0.0
        >>> round(get_luminance('#FF0000'), 2)
        0.21
    """
    rgb = parse_color(color)
    
    def linearize(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    r, g, b = linearize(rgb.r), linearize(rgb.g), linearize(rgb.b)
    
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def get_contrast_ratio(color1: Union[str, Tuple[int, int, int], RGB],
                       color2: Union[str, Tuple[int, int, int], RGB]) -> float:
    """
    Calculate contrast ratio between two colors (WCAG definition).
    
    Args:
        color1: First color
        color2: Second color
    
    Returns:
        Contrast ratio (1.0 to 21.0)
    
    Examples:
        >>> get_contrast_ratio('#FFFFFF', '#000000')
        21.0
        >>> round(get_contrast_ratio('#FFFFFF', '#FFFF00'), 1)
        1.1
    """
    l1 = get_luminance(color1)
    l2 = get_luminance(color2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


def get_wcag_level(contrast_ratio: float) -> Dict[str, str]:
    """
    Get WCAG accessibility level for a contrast ratio.
    
    Args:
        contrast_ratio: Contrast ratio (1.0 to 21.0)
    
    Returns:
        Dictionary with AA and AAA compliance levels for normal and large text
    
    Examples:
        >>> get_wcag_level(7.0)
        {'AA_normal': 'Pass', 'AA_large': 'Pass', 'AAA_normal': 'Pass', 'AAA_large': 'Pass'}
        >>> get_wcag_level(4.5)
        {'AA_normal': 'Pass', 'AA_large': 'Pass', 'AAA_normal': 'Fail', 'AAA_large': 'Pass'}
    """
    return {
        'AA_normal': 'Pass' if contrast_ratio >= 4.5 else 'Fail',
        'AA_large': 'Pass' if contrast_ratio >= 3 else 'Fail',
        'AAA_normal': 'Pass' if contrast_ratio >= 7 else 'Fail',
        'AAA_large': 'Pass' if contrast_ratio >= 4.5 else 'Fail',
    }


def get_perceived_brightness(color: Union[str, Tuple[int, int, int], RGB]) -> float:
    """
    Calculate perceived brightness of a color.
    
    Args:
        color: Color in any supported format
    
    Returns:
        Perceived brightness (0.0 to 255.0)
    
    Examples:
        >>> get_perceived_brightness('#FFFFFF')
        255.0
        >>> get_perceived_brightness('#000000')
        0.0
    """
    rgb = parse_color(color)
    # Using weighted formula (Rec. 709)
    return math.sqrt(0.299 * rgb.r ** 2 + 0.587 * rgb.g ** 2 + 0.114 * rgb.b ** 2)


def is_light_color(color: Union[str, Tuple[int, int, int], RGB]) -> bool:
    """
    Determine if a color is considered "light".
    
    Args:
        color: Color in any supported format
    
    Returns:
        True if light, False if dark
    
    Examples:
        >>> is_light_color('#FFFFFF')
        True
        >>> is_light_color('#000000')
        False
    """
    return get_perceived_brightness(color) > 127.5


def get_color_temperature(color: Union[str, Tuple[int, int, int], RGB]) -> str:
    """
    Determine the color temperature (warm, cool, or neutral).
    
    Args:
        color: Color in any supported format
    
    Returns:
        'warm', 'cool', or 'neutral'
    
    Examples:
        >>> get_color_temperature('#FF0000')
        'warm'
        >>> get_color_temperature('#0000FF')
        'cool'
        >>> get_color_temperature('#808080')
        'neutral'
    """
    rgb = parse_color(color)
    hsl = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    
    h, s, l = hsl
    
    # Low saturation colors are neutral
    if s < 10:
        return 'neutral'
    
    # Warm colors: red, orange, yellow (0-60), and red-magenta (330-360)
    if (0 <= h < 60) or (h >= 330):
        return 'warm'
    
    # Cool colors: green, cyan, blue (60-270)
    if 60 <= h < 270:
        return 'cool'
    
    # Neutral zone: purple, magenta (270-330)
    return 'neutral'


# ============================================================================
# Color Manipulation Functions
# ============================================================================

def lighten(color: Union[str, Tuple[int, int, int], RGB], amount: float = 10) -> RGB:
    """
    Lighten a color by a given amount.
    
    Args:
        color: Color in any supported format
        amount: Amount to lighten (0-100)
    
    Returns:
        Lightened RGB color
    
    Examples:
        >>> lighten('#FF0000', 20)
        RGB(r=255, g=51, b=51)
    """
    rgb = parse_color(color)
    h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    l = min(100, l + amount)
    r, g, b = hsl_to_rgb(h, s, l)
    return RGB(r, g, b)


def darken(color: Union[str, Tuple[int, int, int], RGB], amount: float = 10) -> RGB:
    """
    Darken a color by a given amount.
    
    Args:
        color: Color in any supported format
        amount: Amount to darken (0-100)
    
    Returns:
        Darkened RGB color
    
    Examples:
        >>> darken('#FF0000', 20)
        RGB(r=204, g=0, b=0)
    """
    rgb = parse_color(color)
    h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    l = max(0, l - amount)
    r, g, b = hsl_to_rgb(h, s, l)
    return RGB(r, g, b)


def saturate(color: Union[str, Tuple[int, int, int], RGB], amount: float = 10) -> RGB:
    """
    Increase saturation of a color.
    
    Args:
        color: Color in any supported format
        amount: Amount to saturate (0-100)
    
    Returns:
        Saturated RGB color
    
    Examples:
        >>> saturate('#CC3333', 20)
        RGB(r=230, g=26, b=26)
    """
    rgb = parse_color(color)
    h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    s = min(100, s + amount)
    r, g, b = hsl_to_rgb(h, s, l)
    return RGB(r, g, b)


def desaturate(color: Union[str, Tuple[int, int, int], RGB], amount: float = 10) -> RGB:
    """
    Decrease saturation of a color.
    
    Args:
        color: Color in any supported format
        amount: Amount to desaturate (0-100)
    
    Returns:
        Desaturated RGB color
    
    Examples:
        >>> desaturate('#FF0000', 50)
        RGB(r=255, g=128, b=128)
    """
    rgb = parse_color(color)
    h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    s = max(0, s - amount)
    r, g, b = hsl_to_rgb(h, s, l)
    return RGB(r, g, b)


def grayscale(color: Union[str, Tuple[int, int, int], RGB]) -> RGB:
    """
    Convert a color to grayscale.
    
    Args:
        color: Color in any supported format
    
    Returns:
        Grayscale RGB color
    
    Examples:
        >>> grayscale('#FF0000')
        RGB(r=76, g=76, b=76)
    """
    rgb = parse_color(color)
    h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    r, g, b = hsl_to_rgb(h, 0, l)
    return RGB(r, g, b)


def invert(color: Union[str, Tuple[int, int, int], RGB]) -> RGB:
    """
    Invert a color.
    
    Args:
        color: Color in any supported format
    
    Returns:
        Inverted RGB color
    
    Examples:
        >>> invert('#FFFFFF')
        RGB(r=0, g=0, b=0)
        >>> invert('#FF0000')
        RGB(r=0, g=255, b=255)
    """
    rgb = parse_color(color)
    return RGB(255 - rgb.r, 255 - rgb.g, 255 - rgb.b)


def complement(color: Union[str, Tuple[int, int, int], RGB]) -> RGB:
    """
    Get the complementary color (opposite on the color wheel).
    
    Args:
        color: Color in any supported format
    
    Returns:
        Complementary RGB color
    
    Examples:
        >>> complement('#FF0000')
        RGB(r=0, g=255, b=255)
    """
    rgb = parse_color(color)
    h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    h = (h + 180) % 360
    r, g, b = hsl_to_rgb(h, s, l)
    return RGB(r, g, b)


def mix_colors(color1: Union[str, Tuple[int, int, int], RGB],
               color2: Union[str, Tuple[int, int, int], RGB],
               weight: float = 0.5) -> RGB:
    """
    Mix two colors together.
    
    Args:
        color1: First color
        color2: Second color
        weight: Weight of first color (0.0 to 1.0)
    
    Returns:
        Mixed RGB color
    
    Examples:
        >>> mix_colors('#FF0000', '#0000FF', 0.5)
        RGB(r=128, g=0, b=128)
        >>> mix_colors('#FF0000', '#0000FF', 0.0)
        RGB(r=0, g=0, b=255)
    """
    rgb1 = parse_color(color1)
    rgb2 = parse_color(color2)
    
    weight = max(0, min(1, weight))
    w1 = weight
    w2 = 1 - weight
    
    r = int(round(rgb1.r * w1 + rgb2.r * w2))
    g = int(round(rgb1.g * w1 + rgb2.g * w2))
    b = int(round(rgb1.b * w1 + rgb2.b * w2))
    
    return RGB(r, g, b)


def blend_colors(colors: List[Union[str, Tuple[int, int, int], RGB]]) -> RGB:
    """
    Blend multiple colors together (equal weights).
    
    Args:
        colors: List of colors
    
    Returns:
        Blended RGB color
    
    Examples:
        >>> blend_colors(['#FF0000', '#00FF00', '#0000FF'])
        RGB(r=85, g=85, b=85)
    """
    if not colors:
        raise ValueError("Cannot blend empty color list")
    
    total_r, total_g, total_b = 0, 0, 0
    count = len(colors)
    
    for color in colors:
        rgb = parse_color(color)
        total_r += rgb.r
        total_g += rgb.g
        total_b += rgb.b
    
    return RGB(
        int(round(total_r / count)),
        int(round(total_g / count)),
        int(round(total_b / count))
    )


# ============================================================================
# Color Distance and Similarity
# ============================================================================

def color_distance(color1: Union[str, Tuple[int, int, int], RGB],
                   color2: Union[str, Tuple[int, int, int], RGB]) -> float:
    """
    Calculate Euclidean distance between two colors in RGB space.
    
    Args:
        color1: First color
        color2: Second color
    
    Returns:
        Distance (0.0 to 441.67 approximately)
    
    Examples:
        >>> color_distance('#000000', '#FFFFFF')
        441.67295593006337
        >>> color_distance('#FF0000', '#FF0000')
        0.0
    """
    rgb1 = parse_color(color1)
    rgb2 = parse_color(color2)
    
    return math.sqrt(
        (rgb1.r - rgb2.r) ** 2 +
        (rgb1.g - rgb2.g) ** 2 +
        (rgb1.b - rgb2.b) ** 2
    )


def color_distance_lab(color1: Union[str, Tuple[int, int, int], RGB],
                       color2: Union[str, Tuple[int, int, int], RGB]) -> float:
    """
    Calculate perceptual distance between two colors using LAB space.
    
    This is more accurate for human perception than RGB distance.
    
    Args:
        color1: First color
        color2: Second color
    
    Returns:
        Perceptual distance (lower is more similar)
    
    Examples:
        >>> round(color_distance_lab('#FF0000', '#00FF00'), 1)
        191.3
    """
    rgb1 = parse_color(color1)
    rgb2 = parse_color(color2)
    
    lab1 = rgb_to_lab(rgb1.r, rgb1.g, rgb1.b)
    lab2 = rgb_to_lab(rgb2.r, rgb2.g, rgb2.b)
    
    return math.sqrt(
        (lab1[0] - lab2[0]) ** 2 +
        (lab1[1] - lab2[1]) ** 2 +
        (lab1[2] - lab2[2]) ** 2
    )


def are_colors_similar(color1: Union[str, Tuple[int, int, int], RGB],
                       color2: Union[str, Tuple[int, int, int], RGB],
                       threshold: float = 10.0) -> bool:
    """
    Check if two colors are perceptually similar.
    
    Args:
        color1: First color
        color2: Second color
        threshold: Maximum LAB distance to be considered similar
    
    Returns:
        True if colors are similar, False otherwise
    
    Examples:
        >>> are_colors_similar('#FF0000', '#FF0101')
        True
        >>> are_colors_similar('#FF0000', '#00FF00')
        False
    """
    return color_distance_lab(color1, color2) < threshold


# ============================================================================
# Color Harmony Functions
# ============================================================================

def get_complementary(color: Union[str, Tuple[int, int, int], RGB]) -> RGB:
    """
    Get complementary color (opposite on color wheel).
    
    Args:
        color: Base color
    
    Returns:
        Complementary RGB color
    
    Examples:
        >>> get_complementary('#FF0000')
        RGB(r=0, g=255, b=255)
    """
    return complement(color)


def get_analogous(color: Union[str, Tuple[int, int, int], RGB],
                  angle: float = 30) -> Tuple[RGB, RGB]:
    """
    Get analogous colors (adjacent on color wheel).
    
    Args:
        color: Base color
        angle: Angle between colors (default 30 degrees)
    
    Returns:
        Tuple of two analogous RGB colors
    
    Examples:
        >>> get_analogous('#FF0000')
        (RGB(r=255, g=0, b=128), RGB(r=255, g=128, b=0))
    """
    rgb = parse_color(color)
    h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    
    h1 = (h - angle) % 360
    h2 = (h + angle) % 360
    
    r1, g1, b1 = hsl_to_rgb(h1, s, l)
    r2, g2, b2 = hsl_to_rgb(h2, s, l)
    
    return (RGB(r1, g1, b1), RGB(r2, g2, b2))


def get_triadic(color: Union[str, Tuple[int, int, int], RGB]) -> Tuple[RGB, RGB]:
    """
    Get triadic colors (evenly spaced on color wheel, 120 degrees apart).
    
    Args:
        color: Base color
    
    Returns:
        Tuple of two triadic RGB colors
    
    Examples:
        >>> get_triadic('#FF0000')
        (RGB(r=0, g=255, b=0), RGB(r=0, g=0, b=255))
    """
    rgb = parse_color(color)
    h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    
    h1 = (h + 120) % 360
    h2 = (h + 240) % 360
    
    r1, g1, b1 = hsl_to_rgb(h1, s, l)
    r2, g2, b2 = hsl_to_rgb(h2, s, l)
    
    return (RGB(r1, g1, b1), RGB(r2, g2, b2))


def get_split_complementary(color: Union[str, Tuple[int, int, int], RGB]) -> Tuple[RGB, RGB]:
    """
    Get split-complementary colors (adjacent to complement).
    
    Args:
        color: Base color
    
    Returns:
        Tuple of two split-complementary RGB colors
    
    Examples:
        >>> get_split_complementary('#FF0000')
        (RGB(r=0, g=255, b=128), RGB(r=0, g=128, b=255))
    """
    rgb = parse_color(color)
    h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    
    complement_h = (h + 180) % 360
    h1 = (complement_h - 30) % 360
    h2 = (complement_h + 30) % 360
    
    r1, g1, b1 = hsl_to_rgb(h1, s, l)
    r2, g2, b2 = hsl_to_rgb(h2, s, l)
    
    return (RGB(r1, g1, b1), RGB(r2, g2, b2))


def get_tetradic(color: Union[str, Tuple[int, int, int], RGB]) -> Tuple[RGB, RGB, RGB]:
    """
    Get tetradic colors (four colors, 90 degrees apart).
    
    Args:
        color: Base color
    
    Returns:
        Tuple of three tetradic RGB colors (base color + 3)
    
    Examples:
        >>> get_tetradic('#FF0000')
        (RGB(r=128, g=255, b=0), RGB(r=0, g=255, b=128), RGB(r=128, g=0, b=255))
    """
    rgb = parse_color(color)
    h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    
    h1 = (h + 90) % 360
    h2 = (h + 180) % 360
    h3 = (h + 270) % 360
    
    r1, g1, b1 = hsl_to_rgb(h1, s, l)
    r2, g2, b2 = hsl_to_rgb(h2, s, l)
    r3, g3, b3 = hsl_to_rgb(h3, s, l)
    
    return (RGB(r1, g1, b1), RGB(r2, g2, b2), RGB(r3, g3, b3))


def get_square(color: Union[str, Tuple[int, int, int], RGB]) -> Tuple[RGB, RGB, RGB]:
    """
    Get square harmony colors (four colors evenly spaced).
    
    Same as tetradic.
    
    Args:
        color: Base color
    
    Returns:
        Tuple of three RGB colors
    """
    return get_tetradic(color)


# ============================================================================
# Palette Generation
# ============================================================================

def generate_shades(color: Union[str, Tuple[int, int, int], RGB],
                    count: int = 5) -> List[RGB]:
    """
    Generate shades (darker versions) of a color.
    
    Args:
        color: Base color
        count: Number of shades to generate
    
    Returns:
        List of RGB shades (from original to darkest)
    
    Examples:
        >>> generate_shades('#FF0000', 3)
        [RGB(r=255, g=0, b=0), RGB(r=170, g=0, b=0), RGB(r=85, g=0, b=0)]
    """
    rgb = parse_color(color)
    h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    
    shades = []
    for i in range(count):
        new_l = l * (1 - i / count)
        r, g, b = hsl_to_rgb(h, s, max(0, new_l))
        shades.append(RGB(r, g, b))
    
    return shades


def generate_tints(color: Union[str, Tuple[int, int, int], RGB],
                   count: int = 5) -> List[RGB]:
    """
    Generate tints (lighter versions) of a color.
    
    Args:
        color: Base color
        count: Number of tints to generate
    
    Returns:
        List of RGB tints (from original to lightest)
    
    Examples:
        >>> generate_tints('#FF0000', 3)
        [RGB(r=255, g=0, b=0), RGB(r=255, g=85, b=85), RGB(r=255, g=170, b=170)]
    """
    rgb = parse_color(color)
    h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    
    tints = []
    for i in range(count):
        new_l = l + (100 - l) * (i / count)
        r, g, b = hsl_to_rgb(h, s, min(100, new_l))
        tints.append(RGB(r, g, b))
    
    return tints


def generate_tones(color: Union[str, Tuple[int, int, int], RGB],
                   count: int = 5) -> List[RGB]:
    """
    Generate tones (mixed with gray) of a color.
    
    Args:
        color: Base color
        count: Number of tones to generate
    
    Returns:
        List of RGB tones
    
    Examples:
        >>> generate_tones('#FF0000', 3)
        [RGB(r=255, g=0, b=0), RGB(r=213, g=42, b=42), RGB(r=170, g=85, b=85)]
    """
    rgb = parse_color(color)
    h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    
    tones = []
    for i in range(count):
        new_s = s * (1 - i / count)
        r, g, b = hsl_to_rgb(h, max(0, new_s), l)
        tones.append(RGB(r, g, b))
    
    return tones


def generate_palette(color: Union[str, Tuple[int, int, int], RGB],
                     count: int = 5,
                     palette_type: str = 'shades') -> List[RGB]:
    """
    Generate a color palette.
    
    Args:
        color: Base color
        count: Number of colors
        palette_type: 'shades', 'tints', 'tones', 'analogous', 'complementary'
    
    Returns:
        List of RGB colors
    
    Examples:
        >>> len(generate_palette('#FF0000', 5))
        5
    """
    if palette_type == 'shades':
        return generate_shades(color, count)
    elif palette_type == 'tints':
        return generate_tints(color, count)
    elif palette_type == 'tones':
        return generate_tones(color, count)
    elif palette_type == 'analogous':
        rgb = parse_color(color)
        h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
        
        colors = [rgb]
        step = 30  # 30 degree steps
        for i in range(1, count):
            new_h = (h + i * step) % 360
            r, g, b = hsl_to_rgb(new_h, s, l)
            colors.append(RGB(r, g, b))
        return colors
    elif palette_type == 'complementary':
        rgb = parse_color(color)
        complement_color = complement(color)
        
        colors = [rgb]
        for i in range(1, count):
            weight = i / count
            mixed = mix_colors(rgb, complement_color, 1 - weight)
            colors.append(mixed)
        return colors
    else:
        raise ValueError(f"Unknown palette type: {palette_type}")


def generate_gradient(start_color: Union[str, Tuple[int, int, int], RGB],
                      end_color: Union[str, Tuple[int, int, int], RGB],
                      steps: int = 10) -> List[RGB]:
    """
    Generate a gradient between two colors.
    
    Args:
        start_color: Starting color
        end_color: Ending color
        steps: Number of colors in gradient
    
    Returns:
        List of RGB colors forming the gradient
    
    Examples:
        >>> gradient = generate_gradient('#FF0000', '#0000FF', 3)
        >>> len(gradient)
        3
    """
    rgb1 = parse_color(start_color)
    rgb2 = parse_color(end_color)
    
    gradient = []
    for i in range(steps):
        weight = i / (steps - 1) if steps > 1 else 0
        gradient.append(mix_colors(rgb1, rgb2, 1 - weight))
    
    return gradient


def generate_random_palette(count: int = 5,
                            harmonize: bool = True) -> List[RGB]:
    """
    Generate a random color palette.
    
    Args:
        count: Number of colors
        harmonize: If True, generate harmonious colors (similar saturation/lightness)
    
    Returns:
        List of random RGB colors
    
    Examples:
        >>> len(generate_random_palette(5))
        5
    """
    if harmonize:
        # Generate colors with similar saturation and lightness
        base_s = random.uniform(50, 80)
        base_l = random.uniform(40, 60)
        
        colors = []
        for i in range(count):
            h = (i * 360 / count + random.uniform(-15, 15)) % 360
            s = base_s + random.uniform(-10, 10)
            l = base_l + random.uniform(-10, 10)
            r, g, b = hsl_to_rgb(h, max(0, min(100, s)), max(0, min(100, l)))
            colors.append(RGB(r, g, b))
        return colors
    else:
        return [RGB(random.randint(0, 255),
                     random.randint(0, 255),
                     random.randint(0, 255)) for _ in range(count)]


# ============================================================================
# Comprehensive Color Information
# ============================================================================

def get_color_info(color: Union[str, Tuple[int, int, int], RGB]) -> ColorInfo:
    """
    Get comprehensive information about a color.
    
    Args:
        color: Color in any supported format
    
    Returns:
        ColorInfo object with all color details
    
    Examples:
        >>> info = get_color_info('#FF0000')
        >>> info.hex
        '#ff0000'
        >>> info.luminance > 0.2
        True
    """
    rgb = parse_color(color)
    hsl = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
    hsv = rgb_to_hsv(rgb.r, rgb.g, rgb.b)
    cmyk = rgb_to_cmyk(rgb.r, rgb.g, rgb.b)
    lab = rgb_to_lab(rgb.r, rgb.g, rgb.b)
    
    return ColorInfo(
        hex=rgb.to_hex(),
        rgb=rgb,
        hsl=HSL(hsl[0], hsl[1], hsl[2]),
        hsv=hsv,
        cmyk=cmyk,
        lab=lab,
        name=get_color_name(rgb),
        luminance=get_luminance(rgb),
        temperature=get_color_temperature(rgb)
    )


if __name__ == '__main__':
    # Quick demo
    print("=== Color Conversion Examples ===")
    print(f"rgb_to_hex(255, 0, 0): {rgb_to_hex(255, 0, 0)}")
    print(f"hex_to_rgb('#FF0000'): {hex_to_rgb('#FF0000')}")
    print(f"rgb_to_hsl(255, 0, 0): {rgb_to_hsl(255, 0, 0)}")
    print(f"hsl_to_rgb(0, 100, 50): {hsl_to_rgb(0, 100, 50)}")
    
    print("\n=== Color Analysis Examples ===")
    print(f"get_luminance('#FF0000'): {get_luminance('#FF0000'):.3f}")
    print(f"get_contrast_ratio('#FFFFFF', '#000000'): {get_contrast_ratio('#FFFFFF', '#000000'):.1f}")
    print(f"is_light_color('#FFFFFF'): {is_light_color('#FFFFFF')}")
    print(f"get_color_temperature('#FF0000'): {get_color_temperature('#FF0000')}")
    
    print("\n=== Color Harmony Examples ===")
    print(f"complement('#FF0000'): {complement('#FF0000')}")
    print(f"get_triadic('#FF0000'): {get_triadic('#FF0000')}")
    
    print("\n=== Palette Examples ===")
    shades = generate_shades('#FF0000', 5)
    print(f"Shades of red: {[s.to_hex() for s in shades]}")
    
    gradient = generate_gradient('#FF0000', '#0000FF', 5)
    print(f"Gradient red to blue: {[c.to_hex() for c in gradient]}")
    
    print("\n=== Color Info ===")
    info = get_color_info('#FF5733')
    print(f"HEX: {info.hex}")
    print(f"RGB: {info.rgb}")
    print(f"HSL: H={info.hsl.h:.1f}, S={info.hsl.s:.1f}%, L={info.hsl.l:.1f}%")
    print(f"Luminance: {info.luminance:.3f}")
    print(f"Temperature: {info.temperature}")
    print(f"Closest named color: {info.name}")