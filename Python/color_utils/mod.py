#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Color Utilities Module
====================================
A comprehensive color conversion, manipulation, and palette generation utility module
for Python with zero external dependencies.

Features:
    - Color format conversion (HEX, RGB, HSL, HSV, CMYK, LAB)
    - Color parsing from various string formats
    - Color manipulation (lighten, darken, saturate, desaturate)
    - Color mixing and blending
    - Contrast ratio calculation (WCAG)
    - Complementary, analogous, triadic color generation
    - Palette generation (random, gradient, harmonious)
    - Color name lookup
    - Accessibility helpers

Author: AllToolkit Contributors
License: MIT
"""

import re
import math
import random
from typing import Tuple, List, Dict, Optional, Union, NamedTuple
from dataclasses import dataclass


# ============================================================================
# Type Aliases
# ============================================================================

RGB = Tuple[int, int, int]  # (0-255, 0-255, 0-255)
RGBA = Tuple[int, int, int, float]  # (0-255, 0-255, 0-255, 0.0-1.0)
HSL = Tuple[float, float, float]  # (0-360, 0-100%, 0-100%)
HSV = Tuple[float, float, float]  # (0-360, 0-100%, 0-100%)
CMYK = Tuple[float, float, float, float]  # (0-100%, 0-100%, 0-100%, 0-100%)
LAB = Tuple[float, float, float]  # (L: 0-100, a: -128 to 127, b: -128 to 127)
XYZ = Tuple[float, float, float]  # (X, Y, Z)


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Color:
    """
    Represents a color with multiple format access.
    
    Attributes:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)
        a: Alpha component (0.0-1.0)
    """
    r: int
    g: int
    b: int
    a: float = 1.0
    
    def __post_init__(self):
        """Validate and clamp color values."""
        self.r = max(0, min(255, int(self.r)))
        self.g = max(0, min(255, int(self.g)))
        self.b = max(0, min(255, int(self.b)))
        self.a = max(0.0, min(1.0, float(self.a)))
    
    @property
    def rgb(self) -> RGB:
        """Get RGB tuple."""
        return (self.r, self.g, self.b)
    
    @property
    def rgba(self) -> RGBA:
        """Get RGBA tuple."""
        return (self.r, self.g, self.b, self.a)
    
    @property
    def hex(self) -> str:
        """Get HEX string (without #)."""
        return f"{self.r:02X}{self.g:02X}{self.b:02X}"
    
    @property
    def hex_with_hash(self) -> str:
        """Get HEX string (with #)."""
        return f"#{self.hex}"
    
    @property
    def hsl(self) -> HSL:
        """Get HSL tuple."""
        return rgb_to_hsl(self.rgb)
    
    @property
    def hsv(self) -> HSV:
        """Get HSV tuple."""
        return rgb_to_hsv(self.rgb)
    
    @property
    def cmyk(self) -> CMYK:
        """Get CMYK tuple."""
        return rgb_to_cmyk(self.rgb)
    
    @property
    def lab(self) -> LAB:
        """Get LAB tuple."""
        return rgb_to_lab(self.rgb)
    
    @property
    def luminance(self) -> float:
        """Get relative luminance (0.0-1.0)."""
        return calculate_luminance(self.rgb)
    
    @property
    def is_light(self) -> bool:
        """Check if color is light."""
        return self.luminance > 0.5
    
    @property
    def is_dark(self) -> bool:
        """Check if color is dark."""
        return not self.is_light
    
    def __str__(self) -> str:
        """String representation."""
        if self.a < 1.0:
            return f"rgba({self.r}, {self.g}, {self.b}, {self.a:.2f})"
        return self.hex_with_hash
    
    def __repr__(self) -> str:
        """Repr representation."""
        return f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})"


# ============================================================================
# Color Name Dictionary (CSS Color Names)
# ============================================================================

COLOR_NAMES = {
    # Basic colors
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 128, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    
    # Extended CSS colors
    'aliceblue': (240, 248, 255),
    'antiquewhite': (250, 235, 215),
    'aqua': (0, 255, 255),
    'aquamarine': (127, 255, 212),
    'azure': (240, 255, 255),
    'beige': (245, 245, 220),
    'bisque': (255, 228, 196),
    'blanchedalmond': (255, 235, 205),
    'blueviolet': (138, 43, 226),
    'brown': (165, 42, 42),
    'burlywood': (222, 184, 135),
    'cadetblue': (95, 158, 160),
    'chartreuse': (127, 255, 0),
    'chocolate': (210, 105, 30),
    'coral': (255, 127, 80),
    'cornflowerblue': (100, 149, 237),
    'cornsilk': (255, 248, 220),
    'crimson': (220, 20, 60),
    'darkblue': (0, 0, 139),
    'darkcyan': (0, 139, 139),
    'darkgoldenrod': (184, 134, 11),
    'darkgray': (169, 169, 169),
    'darkgreen': (0, 100, 0),
    'darkgrey': (169, 169, 169),
    'darkkhaki': (189, 183, 107),
    'darkmagenta': (139, 0, 139),
    'darkolivegreen': (85, 107, 47),
    'darkorange': (255, 140, 0),
    'darkorchid': (153, 50, 204),
    'darkred': (139, 0, 0),
    'darksalmon': (233, 150, 122),
    'darkseagreen': (143, 188, 143),
    'darkslateblue': (72, 61, 139),
    'darkslategray': (47, 79, 79),
    'darkslategrey': (47, 79, 79),
    'darkturquoise': (0, 206, 209),
    'darkviolet': (148, 0, 211),
    'deeppink': (255, 20, 147),
    'deepskyblue': (0, 191, 255),
    'dimgray': (105, 105, 105),
    'dimgrey': (105, 105, 105),
    'dodgerblue': (30, 144, 255),
    'firebrick': (178, 34, 34),
    'floralwhite': (255, 250, 240),
    'forestgreen': (34, 139, 34),
    'fuchsia': (255, 0, 255),
    'gainsboro': (220, 220, 220),
    'ghostwhite': (248, 248, 255),
    'gold': (255, 215, 0),
    'goldenrod': (218, 165, 32),
    'gray': (128, 128, 128),
    'grey': (128, 128, 128),
    'greenyellow': (173, 255, 47),
    'honeydew': (240, 255, 240),
    'hotpink': (255, 105, 180),
    'indianred': (205, 92, 92),
    'indigo': (75, 0, 130),
    'ivory': (255, 255, 240),
    'khaki': (240, 230, 140),
    'lavender': (230, 230, 250),
    'lavenderblush': (255, 240, 245),
    'lawngreen': (124, 252, 0),
    'lemonchiffon': (255, 250, 205),
    'lightblue': (173, 216, 230),
    'lightcoral': (240, 128, 128),
    'lightcyan': (224, 255, 255),
    'lightgoldenrodyellow': (250, 250, 210),
    'lightgray': (211, 211, 211),
    'lightgreen': (144, 238, 144),
    'lightgrey': (211, 211, 211),
    'lightpink': (255, 182, 193),
    'lightsalmon': (255, 160, 122),
    'lightseagreen': (32, 178, 170),
    'lightskyblue': (135, 206, 250),
    'lightslategray': (119, 136, 153),
    'lightslategrey': (119, 136, 153),
    'lightsteelblue': (176, 196, 222),
    'lightyellow': (255, 255, 224),
    'lime': (0, 255, 0),
    'limegreen': (50, 205, 50),
    'linen': (250, 240, 230),
    'maroon': (128, 0, 0),
    'mediumaquamarine': (102, 205, 170),
    'mediumblue': (0, 0, 205),
    'mediumorchid': (186, 85, 211),
    'mediumpurple': (147, 112, 219),
    'mediumseagreen': (60, 179, 113),
    'mediumslateblue': (123, 104, 238),
    'mediumspringgreen': (0, 250, 154),
    'mediumturquoise': (72, 209, 204),
    'mediumvioletred': (199, 21, 133),
    'midnightblue': (25, 25, 112),
    'mintcream': (245, 255, 250),
    'mistyrose': (255, 228, 225),
    'moccasin': (255, 228, 181),
    'navajowhite': (255, 222, 173),
    'navy': (0, 0, 128),
    'oldlace': (253, 245, 230),
    'olive': (128, 128, 0),
    'olivedrab': (107, 142, 35),
    'orange': (255, 165, 0),
    'orangered': (255, 69, 0),
    'orchid': (218, 112, 214),
    'palegoldenrod': (238, 232, 170),
    'palegreen': (152, 251, 152),
    'paleturquoise': (175, 238, 238),
    'palevioletred': (219, 112, 147),
    'papayawhip': (255, 239, 213),
    'peachpuff': (255, 218, 185),
    'peru': (205, 133, 63),
    'pink': (255, 192, 203),
    'plum': (221, 160, 221),
    'powderblue': (176, 224, 230),
    'purple': (128, 0, 128),
    'rebeccapurple': (102, 51, 153),
    'rosybrown': (188, 143, 143),
    'royalblue': (65, 105, 225),
    'saddlebrown': (139, 69, 19),
    'salmon': (250, 128, 114),
    'sandybrown': (244, 164, 96),
    'seagreen': (46, 139, 87),
    'seashell': (255, 245, 238),
    'sienna': (160, 82, 45),
    'silver': (192, 192, 192),
    'skyblue': (135, 206, 235),
    'slateblue': (106, 90, 205),
    'slategray': (112, 128, 144),
    'slategrey': (112, 128, 144),
    'snow': (255, 250, 250),
    'springgreen': (0, 255, 127),
    'steelblue': (70, 130, 180),
    'tan': (210, 180, 140),
    'teal': (0, 128, 128),
    'thistle': (216, 191, 216),
    'tomato': (255, 99, 71),
    'turquoise': (64, 224, 208),
    'violet': (238, 130, 238),
    'wheat': (245, 222, 179),
    'whitesmoke': (245, 245, 245),
    'yellowgreen': (154, 205, 50),
}

# Reverse lookup: RGB to name
RGB_TO_NAME = {rgb: name for name, rgb in COLOR_NAMES.items()}


# ============================================================================
# Color Parsing
# ============================================================================

def parse_color(color_str: str) -> Color:
    """
    Parse a color string into a Color object.
    
    Supports:
        - HEX: "#FF0000", "FF0000", "#F00", "F00"
        - RGB: "rgb(255, 0, 0)", "rgb(255,0,0)"
        - RGBA: "rgba(255, 0, 0, 0.5)", "rgba(255,0,0,0.5)"
        - HSL: "hsl(0, 100%, 50%)", "hsl(0,100%,50%)"
        - HSLA: "hsla(0, 100%, 50%, 0.5)"
        - Names: "red", "blue", "cornflowerblue"
    
    Args:
        color_str: Color string to parse
        
    Returns:
        Color object
        
    Raises:
        ValueError: If color string cannot be parsed
        
    Example:
        >>> parse_color("#FF0000")
        Color(r=255, g=0, b=0, a=1.0)
        >>> parse_color("red")
        Color(r=255, g=0, b=0, a=1.0)
    """
    color_str = color_str.strip()
    
    # Handle color names
    name_lower = color_str.lower()
    if name_lower in COLOR_NAMES:
        rgb = COLOR_NAMES[name_lower]
        return Color(*rgb)
    
    # Handle HEX colors
    if color_str.startswith('#'):
        return _parse_hex(color_str)
    
    # Try HEX without hash
    if re.match(r'^[0-9A-Fa-f]{3,8}$', color_str):
        return _parse_hex('#' + color_str)
    
    # Handle rgb()
    rgb_match = re.match(
        r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)',
        color_str, re.IGNORECASE
    )
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
        return Color(r, g, b)
    
    # Handle rgba()
    rgba_match = re.match(
        r'rgba\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)',
        color_str, re.IGNORECASE
    )
    if rgba_match:
        r, g, b, a = rgba_match.groups()
        return Color(int(r), int(g), int(b), float(a))
    
    # Handle hsl()
    hsl_match = re.match(
        r'hsl\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)%?\s*\)',
        color_str, re.IGNORECASE
    )
    if hsl_match:
        h, s, l = map(float, hsl_match.groups())
        rgb = hsl_to_rgb((h, s, l))
        return Color(*rgb)
    
    # Handle hsla()
    hsla_match = re.match(
        r'hsla\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)\s*\)',
        color_str, re.IGNORECASE
    )
    if hsla_match:
        h, s, l, a = hsla_match.groups()
        rgb = hsl_to_rgb((float(h), float(s), float(l)))
        return Color(*rgb, float(a))
    
    raise ValueError(f"Cannot parse color: {color_str}")


def _parse_hex(hex_str: str) -> Color:
    """Parse a HEX color string."""
    hex_str = hex_str.lstrip('#')
    
    if len(hex_str) == 3:
        # Short form: #RGB -> #RRGGBB
        r = int(hex_str[0] * 2, 16)
        g = int(hex_str[1] * 2, 16)
        b = int(hex_str[2] * 2, 16)
    elif len(hex_str) == 6:
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
    elif len(hex_str) == 8:
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        a = int(hex_str[6:8], 16) / 255
        return Color(r, g, b, a)
    else:
        raise ValueError(f"Invalid HEX color: #{hex_str}")
    
    return Color(r, g, b)


def name_to_rgb(name: str) -> Optional[RGB]:
    """
    Convert a color name to RGB.
    
    Args:
        name: Color name (case-insensitive)
        
    Returns:
        RGB tuple or None if not found
        
    Example:
        >>> name_to_rgb("cornflowerblue")
        (100, 149, 237)
    """
    return COLOR_NAMES.get(name.lower())


def rgb_to_name(rgb: RGB) -> Optional[str]:
    """
    Convert RGB to the closest named color.
    
    Args:
        rgb: RGB tuple
        
    Returns:
        Color name or None if no close match
        
    Example:
        >>> rgb_to_name((255, 0, 0))
        'red'
    """
    # Exact match
    if rgb in RGB_TO_NAME:
        return RGB_TO_NAME[rgb]
    
    # Find closest named color
    min_distance = float('inf')
    closest_name = None
    
    for name, named_rgb in COLOR_NAMES.items():
        distance = color_distance(rgb, named_rgb)
        if distance < min_distance:
            min_distance = distance
            closest_name = name
    
    # Only return if reasonably close
    if min_distance < 50:  # Threshold for "close enough"
        return closest_name
    return None


# ============================================================================
# Color Format Conversions
# ============================================================================

def rgb_to_hex(rgb: RGB, include_hash: bool = True) -> str:
    """
    Convert RGB to HEX string.
    
    Args:
        rgb: RGB tuple (0-255, 0-255, 0-255)
        include_hash: Whether to include # prefix
        
    Returns:
        HEX color string
        
    Example:
        >>> rgb_to_hex((255, 0, 0))
        "#FF0000"
    """
    r, g, b = rgb
    hex_str = f"{r:02X}{g:02X}{b:02X}"
    return f"#{hex_str}" if include_hash else hex_str


def hex_to_rgb(hex_str: str) -> RGB:
    """
    Convert HEX string to RGB.
    
    Args:
        hex_str: HEX color string (with or without #)
        
    Returns:
        RGB tuple
        
    Example:
        >>> hex_to_rgb("#FF0000")
        (255, 0, 0)
    """
    color = parse_color(hex_str)
    return color.rgb


def rgb_to_hsl(rgb: RGB) -> HSL:
    """
    Convert RGB to HSL.
    
    Args:
        rgb: RGB tuple (0-255, 0-255, 0-255)
        
    Returns:
        HSL tuple (0-360, 0-100, 0-100)
        
    Example:
        >>> rgb_to_hsl((255, 0, 0))
        (0.0, 100.0, 50.0)
    """
    r, g, b = [x / 255.0 for x in rgb]
    
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    delta = max_c - min_c
    
    # Lightness
    l = (max_c + min_c) / 2
    
    # Saturation
    if delta == 0:
        s = 0
        h = 0
    else:
        s = delta / (1 - abs(2 * l - 1))
        
        # Hue
        if max_c == r:
            h = 60 * (((g - b) / delta) % 6)
        elif max_c == g:
            h = 60 * (((b - r) / delta) + 2)
        else:
            h = 60 * (((r - g) / delta) + 4)
    
    return (h, s * 100, l * 100)


def hsl_to_rgb(hsl: HSL) -> RGB:
    """
    Convert HSL to RGB.
    
    Args:
        hsl: HSL tuple (0-360, 0-100, 0-100)
        
    Returns:
        RGB tuple (0-255, 0-255, 0-255)
        
    Example:
        >>> hsl_to_rgb((0, 100, 50))
        (255, 0, 0)
    """
    h, s, l = hsl
    s /= 100
    l /= 100
    
    if s == 0:
        r = g = b = l
    else:
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
        
        r = hue_to_rgb(p, q, h/360 + 1/3)
        g = hue_to_rgb(p, q, h/360)
        b = hue_to_rgb(p, q, h/360 - 1/3)
    
    return (round(r * 255), round(g * 255), round(b * 255))


def rgb_to_hsv(rgb: RGB) -> HSV:
    """
    Convert RGB to HSV.
    
    Args:
        rgb: RGB tuple (0-255, 0-255, 0-255)
        
    Returns:
        HSV tuple (0-360, 0-100, 0-100)
        
    Example:
        >>> rgb_to_hsv((255, 0, 0))
        (0.0, 100.0, 100.0)
    """
    r, g, b = [x / 255.0 for x in rgb]
    
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    delta = max_c - min_c
    
    # Value
    v = max_c
    
    # Saturation
    s = 0 if max_c == 0 else delta / max_c
    
    # Hue
    if delta == 0:
        h = 0
    elif max_c == r:
        h = 60 * (((g - b) / delta) % 6)
    elif max_c == g:
        h = 60 * (((b - r) / delta) + 2)
    else:
        h = 60 * (((r - g) / delta) + 4)
    
    return (h, s * 100, v * 100)


def hsv_to_rgb(hsv: HSV) -> RGB:
    """
    Convert HSV to RGB.
    
    Args:
        hsv: HSV tuple (0-360, 0-100, 0-100)
        
    Returns:
        RGB tuple (0-255, 0-255, 0-255)
        
    Example:
        >>> hsv_to_rgb((0, 100, 100))
        (255, 0, 0)
    """
    h, s, v = hsv
    s /= 100
    v /= 100
    
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
    
    return (round((r + m) * 255), round((g + m) * 255), round((b + m) * 255))


def rgb_to_cmyk(rgb: RGB) -> CMYK:
    """
    Convert RGB to CMYK.
    
    Args:
        rgb: RGB tuple (0-255, 0-255, 0-255)
        
    Returns:
        CMYK tuple (0-100, 0-100, 0-100, 0-100)
        
    Example:
        >>> rgb_to_cmyk((0, 0, 0))
        (0.0, 0.0, 0.0, 100.0)
    """
    r, g, b = [x / 255.0 for x in rgb]
    
    if r == g == b == 0:
        return (0.0, 0.0, 0.0, 100.0)
    
    k = 1 - max(r, g, b)
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    
    return (c * 100, m * 100, y * 100, k * 100)


def cmyk_to_rgb(cmyk: CMYK) -> RGB:
    """
    Convert CMYK to RGB.
    
    Args:
        cmyk: CMYK tuple (0-100, 0-100, 0-100, 0-100)
        
    Returns:
        RGB tuple (0-255, 0-255, 0-255)
        
    Example:
        >>> cmyk_to_rgb((0, 0, 0, 100))
        (0, 0, 0)
    """
    c, m, y, k = [x / 100.0 for x in cmyk]
    
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    
    return (round(r), round(g), round(b))


def rgb_to_lab(rgb: RGB) -> LAB:
    """
    Convert RGB to LAB color space.
    
    Uses D65 illuminant reference white.
    
    Args:
        rgb: RGB tuple (0-255, 0-255, 0-255)
        
    Returns:
        LAB tuple (L: 0-100, a: -128 to 127, b: -128 to 127)
        
    Example:
        >>> rgb_to_lab((255, 0, 0))
        (53.23288178584245, 80.10930952982204, 67.22006831026425)
    """
    # RGB to XYZ
    r, g, b = [x / 255.0 for x in rgb]
    
    # Apply gamma correction
    r = r ** 2.4 if r > 0.04045 else r / 12.92
    g = g ** 2.4 if g > 0.04045 else g / 12.92
    b = b ** 2.4 if b > 0.04045 else b / 12.92
    
    r *= 100
    g *= 100
    b *= 100
    
    # RGB to XYZ matrix (sRGB)
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
    
    # Reference white D65
    ref_x = 95.047
    ref_y = 100.000
    ref_z = 108.883
    
    x /= ref_x
    y /= ref_y
    z /= ref_z
    
    # XYZ to LAB
    def f(t):
        delta = 6/29
        if t > delta ** 3:
            return t ** (1/3)
        return t / (3 * delta ** 2) + 4/29
    
    L = 116 * f(y) - 16
    a = 500 * (f(x) - f(y))
    b_lab = 200 * (f(y) - f(z))
    
    return (L, a, b_lab)


def lab_to_rgb(lab: LAB) -> RGB:
    """
    Convert LAB to RGB color space.
    
    Args:
        lab: LAB tuple (L: 0-100, a: -128 to 127, b: -128 to 127)
        
    Returns:
        RGB tuple (0-255, 0-255, 0-255)
        
    Example:
        >>> lab_to_rgb((53.23, 80.11, 67.22))
        (255, 0, 0)
    """
    L, a, b = lab
    
    # Reference white D65
    ref_x = 95.047
    ref_y = 100.000
    ref_z = 108.883
    
    # LAB to XYZ
    def f(t):
        delta = 6/29
        if t > delta:
            return t ** 3
        return 3 * delta ** 2 * (t - 4/29)
    
    x = ref_x * f((L + 16) / 116 + a / 500)
    y = ref_y * f((L + 16) / 116)
    z = ref_z * f((L + 16) / 116 - b / 200)
    
    x /= 100
    y /= 100
    z /= 100
    
    # XYZ to RGB matrix (sRGB)
    r = x * 3.2404542 + y * -1.5371385 + z * -0.4985314
    g = x * -0.9692660 + y * 1.8760108 + z * 0.0415560
    b = x * 0.0556434 + y * -0.2040259 + z * 1.0572252
    
    # Apply inverse gamma correction
    def gamma_correct(c):
        if c > 0.0031308:
            return 1.055 * (c ** (1/2.4)) - 0.055
        return 12.92 * c
    
    r = gamma_correct(r)
    g = gamma_correct(g)
    b = gamma_correct(b)
    
    return (
        max(0, min(255, round(r * 255))),
        max(0, min(255, round(g * 255))),
        max(0, min(255, round(b * 255)))
    )


# ============================================================================
# Color Manipulation
# ============================================================================

def lighten(rgb: RGB, amount: float = 10) -> RGB:
    """
    Lighten a color.
    
    Args:
        rgb: RGB tuple
        amount: Amount to lighten (0-100)
        
    Returns:
        Lightened RGB tuple
        
    Example:
        >>> lighten((128, 128, 128), 50)
        (192, 192, 192)
    """
    h, s, l = rgb_to_hsl(rgb)
    l = min(100, l + amount)
    return hsl_to_rgb((h, s, l))


def darken(rgb: RGB, amount: float = 10) -> RGB:
    """
    Darken a color.
    
    Args:
        rgb: RGB tuple
        amount: Amount to darken (0-100)
        
    Returns:
        Darkened RGB tuple
        
    Example:
        >>> darken((128, 128, 128), 50)
        (64, 64, 64)
    """
    h, s, l = rgb_to_hsl(rgb)
    l = max(0, l - amount)
    return hsl_to_rgb((h, s, l))


def saturate(rgb: RGB, amount: float = 10) -> RGB:
    """
    Increase saturation of a color.
    
    Args:
        rgb: RGB tuple
        amount: Amount to saturate (0-100)
        
    Returns:
        Saturated RGB tuple
        
    Example:
        >>> saturate((128, 128, 128), 50)
        (128, 128, 128)  # Gray cannot be saturated
    """
    h, s, l = rgb_to_hsl(rgb)
    s = min(100, s + amount)
    return hsl_to_rgb((h, s, l))


def desaturate(rgb: RGB, amount: float = 10) -> RGB:
    """
    Decrease saturation of a color.
    
    Args:
        rgb: RGB tuple
        amount: Amount to desaturate (0-100)
        
    Returns:
        Desaturated RGB tuple
        
    Example:
        >>> desaturate((255, 0, 0), 50)
        (191, 64, 64)
    """
    h, s, l = rgb_to_hsl(rgb)
    s = max(0, s - amount)
    return hsl_to_rgb((h, s, l))


def grayscale(rgb: RGB) -> RGB:
    """
    Convert a color to grayscale.
    
    Args:
        rgb: RGB tuple
        
    Returns:
        Grayscale RGB tuple
        
    Example:
        >>> grayscale((255, 0, 0))
        (76, 76, 76)
    """
    # Use luminosity method for better perceptual grayscale
    r, g, b = rgb
    gray = round(0.299 * r + 0.587 * g + 0.114 * b)
    return (gray, gray, gray)


def invert(rgb: RGB) -> RGB:
    """
    Invert a color.
    
    Args:
        rgb: RGB tuple
        
    Returns:
        Inverted RGB tuple
        
    Example:
        >>> invert((255, 0, 0))
        (0, 255, 255)
    """
    return (255 - rgb[0], 255 - rgb[1], 255 - rgb[2])


def rotate_hue(rgb: RGB, degrees: float) -> RGB:
    """
    Rotate the hue of a color.
    
    Args:
        rgb: RGB tuple
        degrees: Degrees to rotate (-360 to 360)
        
    Returns:
        RGB tuple with rotated hue
        
    Example:
        >>> rotate_hue((255, 0, 0), 180)
        (0, 255, 255)  # Cyan
    """
    h, s, l = rgb_to_hsl(rgb)
    h = (h + degrees) % 360
    if h < 0:
        h += 360
    return hsl_to_rgb((h, s, l))


def complement(rgb: RGB) -> RGB:
    """
    Get the complementary color.
    
    Args:
        rgb: RGB tuple
        
    Returns:
        Complementary RGB tuple
        
    Example:
        >>> complement((255, 0, 0))
        (0, 255, 255)  # Cyan
    """
    return rotate_hue(rgb, 180)


# ============================================================================
# Color Mixing and Blending
# ============================================================================

def mix(color1: RGB, color2: RGB, ratio: float = 0.5) -> RGB:
    """
    Mix two colors together.
    
    Args:
        color1: First RGB tuple
        color2: Second RGB tuple
        ratio: Mix ratio (0.0 = all color1, 1.0 = all color2)
        
    Returns:
        Mixed RGB tuple
        
    Example:
        >>> mix((255, 0, 0), (0, 0, 255), 0.5)
        (128, 0, 128)  # Purple
    """
    r = round(color1[0] * (1 - ratio) + color2[0] * ratio)
    g = round(color1[1] * (1 - ratio) + color2[1] * ratio)
    b = round(color1[2] * (1 - ratio) + color2[2] * ratio)
    return (r, g, b)


def blend_multiply(color1: RGB, color2: RGB) -> RGB:
    """
    Multiply blend two colors.
    
    Args:
        color1: First RGB tuple
        color2: Second RGB tuple
        
    Returns:
        Blended RGB tuple
        
    Example:
        >>> blend_multiply((255, 255, 255), (128, 128, 128))
        (128, 128, 128)
    """
    return (
        round(color1[0] * color2[0] / 255),
        round(color1[1] * color2[1] / 255),
        round(color1[2] * color2[2] / 255)
    )


def blend_screen(color1: RGB, color2: RGB) -> RGB:
    """
    Screen blend two colors.
    
    Args:
        color1: First RGB tuple
        color2: Second RGB tuple
        
    Returns:
        Blended RGB tuple
        
    Example:
        >>> blend_screen((0, 0, 0), (128, 128, 128))
        (128, 128, 128)
    """
    return (
        255 - round((255 - color1[0]) * (255 - color2[0]) / 255),
        255 - round((255 - color1[1]) * (255 - color2[1]) / 255),
        255 - round((255 - color1[2]) * (255 - color2[2]) / 255)
    )


def blend_overlay(color1: RGB, color2: RGB) -> RGB:
    """
    Overlay blend two colors.
    
    Args:
        color1: First RGB tuple (base)
        color2: Second RGB tuple (overlay)
        
    Returns:
        Blended RGB tuple
        
    Example:
        >>> blend_overlay((128, 128, 128), (128, 128, 128))
        (128, 128, 128)
    """
    def overlay(c1, c2):
        if c1 < 128:
            return 2 * c1 * c2 / 255
        return 255 - 2 * (255 - c1) * (255 - c2) / 255
    
    return (
        round(overlay(color1[0], color2[0])),
        round(overlay(color1[1], color2[1])),
        round(overlay(color1[2], color2[2]))
    )


# ============================================================================
# Color Distance and Comparison
# ============================================================================

def color_distance(color1: RGB, color2: RGB) -> float:
    """
    Calculate Euclidean distance between two colors.
    
    Args:
        color1: First RGB tuple
        color2: Second RGB tuple
        
    Returns:
        Distance (0-441.67, where 0 = identical)
        
    Example:
        >>> color_distance((255, 0, 0), (0, 0, 255))
        359.16...
    """
    return math.sqrt(
        (color1[0] - color2[0]) ** 2 +
        (color1[1] - color2[1]) ** 2 +
        (color1[2] - color2[2]) ** 2
    )


def color_distance_lab(color1: RGB, color2: RGB) -> float:
    """
    Calculate perceptual distance between two colors using LAB space.
    
    More accurate for human perception than RGB distance.
    
    Args:
        color1: First RGB tuple
        color2: Second RGB tuple
        
    Returns:
        Perceptual distance
        
    Example:
        >>> color_distance_lab((255, 0, 0), (0, 0, 255))
        173.58...
    """
    lab1 = rgb_to_lab(color1)
    lab2 = rgb_to_lab(color2)
    
    return math.sqrt(
        (lab1[0] - lab2[0]) ** 2 +
        (lab1[1] - lab2[1]) ** 2 +
        (lab1[2] - lab2[2]) ** 2
    )


def calculate_luminance(rgb: RGB) -> float:
    """
    Calculate relative luminance of a color (WCAG).
    
    Args:
        rgb: RGB tuple
        
    Returns:
        Relative luminance (0.0-1.0)
        
    Example:
        >>> calculate_luminance((255, 255, 255))
        1.0
        >>> calculate_luminance((0, 0, 0))
        0.0
    """
    r, g, b = rgb
    
    def channel_luminance(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    r = channel_luminance(r)
    g = channel_luminance(g)
    b = channel_luminance(b)
    
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(color1: RGB, color2: RGB) -> float:
    """
    Calculate contrast ratio between two colors (WCAG).
    
    Args:
        color1: First RGB tuple
        color2: Second RGB tuple
        
    Returns:
        Contrast ratio (1.0-21.0)
        
    Example:
        >>> contrast_ratio((0, 0, 0), (255, 255, 255))
        21.0
    """
    l1 = calculate_luminance(color1)
    l2 = calculate_luminance(color2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


def wcag_rating(ratio: float) -> str:
    """
    Get WCAG accessibility rating for contrast ratio.
    
    Args:
        ratio: Contrast ratio
        
    Returns:
        Rating string ('AAA', 'AA', 'AA Large', 'Fail')
        
    Example:
        >>> wcag_rating(7.0)
        'AAA'
    """
    if ratio >= 7.0:
        return 'AAA'
    elif ratio >= 4.5:
        return 'AA'
    elif ratio >= 3.0:
        return 'AA Large'
    return 'Fail'


# ============================================================================
# Color Harmony
# ============================================================================

def complementary_palette(rgb: RGB) -> List[RGB]:
    """
    Generate complementary color palette.
    
    Args:
        rgb: Base RGB color
        
    Returns:
        List of 2 RGB colors (base + complement)
        
    Example:
        >>> complementary_palette((255, 0, 0))
        [(255, 0, 0), (0, 255, 255)]
    """
    return [rgb, complement(rgb)]


def analogous_palette(rgb: RGB, angle: float = 30) -> List[RGB]:
    """
    Generate analogous color palette.
    
    Args:
        rgb: Base RGB color
        angle: Angle between colors (default 30 degrees)
        
    Returns:
        List of 3 RGB colors
        
    Example:
        >>> analogous_palette((255, 0, 0))
        [(255, 0, 128), (255, 0, 0), (255, 128, 0)]
    """
    return [
        rotate_hue(rgb, -angle),
        rgb,
        rotate_hue(rgb, angle)
    ]


def triadic_palette(rgb: RGB) -> List[RGB]:
    """
    Generate triadic color palette.
    
    Args:
        rgb: Base RGB color
        
    Returns:
        List of 3 RGB colors evenly spaced
        
    Example:
        >>> triadic_palette((255, 0, 0))
        [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    """
    return [
        rgb,
        rotate_hue(rgb, 120),
        rotate_hue(rgb, 240)
    ]


def split_complementary_palette(rgb: RGB) -> List[RGB]:
    """
    Generate split-complementary color palette.
    
    Args:
        rgb: Base RGB color
        
    Returns:
        List of 3 RGB colors
        
    Example:
        >>> split_complementary_palette((255, 0, 0))
        [(255, 0, 0), (0, 255, 128), (0, 128, 255)]
    """
    return [
        rgb,
        rotate_hue(rgb, 150),
        rotate_hue(rgb, 210)
    ]


def tetradic_palette(rgb: RGB) -> List[RGB]:
    """
    Generate tetradic (square) color palette.
    
    Args:
        rgb: Base RGB color
        
    Returns:
        List of 4 RGB colors
        
    Example:
        >>> tetradic_palette((255, 0, 0))
        [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    """
    return [
        rgb,
        rotate_hue(rgb, 90),
        rotate_hue(rgb, 180),
        rotate_hue(rgb, 270)
    ]


# ============================================================================
# Palette Generation
# ============================================================================

def random_color() -> RGB:
    """
    Generate a random color.
    
    Returns:
        Random RGB tuple
        
    Example:
        >>> random_color()  # doctest: +SKIP
        (123, 45, 67)
    """
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def random_palette(count: int = 5) -> List[RGB]:
    """
    Generate a random color palette.
    
    Args:
        count: Number of colors to generate
        
    Returns:
        List of random RGB tuples
        
    Example:
        >>> random_palette(3)  # doctest: +SKIP
        [(123, 45, 67), (200, 100, 50), (50, 150, 200)]
    """
    return [random_color() for _ in range(count)]


def gradient_palette(start: RGB, end: RGB, steps: int = 5) -> List[RGB]:
    """
    Generate a gradient palette between two colors.
    
    Args:
        start: Starting RGB color
        end: Ending RGB color
        steps: Number of steps (minimum 2)
        
    Returns:
        List of RGB tuples forming gradient
        
    Example:
        >>> gradient_palette((255, 0, 0), (0, 0, 255), 5)
        [(255, 0, 0), (191, 0, 64), (128, 0, 128), (64, 0, 191), (0, 0, 255)]
    """
    if steps < 2:
        return [start]
    
    return [mix(start, end, i / (steps - 1)) for i in range(steps)]


def monochromatic_palette(rgb: RGB, count: int = 5) -> List[RGB]:
    """
    Generate monochromatic palette (variations in lightness).
    
    Args:
        rgb: Base RGB color
        count: Number of colors
        
    Returns:
        List of RGB tuples with varying lightness
        
    Example:
        >>> monochromatic_palette((255, 0, 0), 5)
        [(128, 0, 0), (191, 0, 0), (255, 0, 0), (255, 64, 64), (255, 128, 128)]
    """
    h, s, l = rgb_to_hsl(rgb)
    
    # Distribute lightness values around the base
    values = []
    step = 50 / (count - 1) if count > 1 else 0
    
    for i in range(count):
        new_l = max(0, min(100, l - 25 + (i * step)))
        values.append(hsl_to_rgb((h, s, new_l)))
    
    return values


def shades_palette(rgb: RGB, count: int = 5) -> List[RGB]:
    """
    Generate shades (darker variations) of a color.
    
    Args:
        rgb: Base RGB color
        count: Number of shades
        
    Returns:
        List of RGB tuples (base to darkest)
        
    Example:
        >>> shades_palette((255, 0, 0), 5)
        [(255, 0, 0), (204, 0, 0), (153, 0, 0), (102, 0, 0), (51, 0, 0)]
    """
    result = [rgb]
    for i in range(1, count):
        result.append(darken(rgb, (100 / count) * i))
    return result


def tints_palette(rgb: RGB, count: int = 5) -> List[RGB]:
    """
    Generate tints (lighter variations) of a color.
    
    Args:
        rgb: Base RGB color
        count: Number of tints
        
    Returns:
        List of RGB tuples (base to lightest)
        
    Example:
        >>> tints_palette((255, 0, 0), 5)
        [(255, 0, 0), (255, 51, 51), (255, 102, 102), (255, 153, 153), (255, 204, 204)]
    """
    result = [rgb]
    for i in range(1, count):
        result.append(lighten(rgb, (100 / count) * i))
    return result


def harmonious_palette(rgb: RGB, harmony: str = 'complementary') -> List[RGB]:
    """
    Generate harmonious color palette.
    
    Args:
        rgb: Base RGB color
        harmony: Harmony type ('complementary', 'analogous', 'triadic', 
                 'split-complementary', 'tetradic', 'monochromatic')
        
    Returns:
        List of RGB tuples
        
    Example:
        >>> harmonious_palette((255, 0, 0), 'triadic')
        [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    """
    harmonies = {
        'complementary': complementary_palette,
        'analogous': analogous_palette,
        'triadic': triadic_palette,
        'split-complementary': split_complementary_palette,
        'tetradic': tetradic_palette,
        'monochromatic': lambda c: monochromatic_palette(c, 5),
    }
    
    func = harmonies.get(harmony.lower(), complementary_palette)
    return func(rgb)


# ============================================================================
# Accessibility Helpers
# ============================================================================

def get_accessible_text_color(background: RGB, dark_color: RGB = (0, 0, 0), 
                              light_color: RGB = (255, 255, 255),
                              min_ratio: float = 4.5) -> RGB:
    """
    Get accessible text color for a given background.
    
    Args:
        background: Background RGB color
        dark_color: Dark text color option
        light_color: Light text color option
        min_ratio: Minimum contrast ratio (default 4.5 for AA)
        
    Returns:
        RGB tuple of best text color
        
    Example:
        >>> get_accessible_text_color((0, 0, 0))
        (255, 255, 255)
        >>> get_accessible_text_color((255, 255, 255))
        (0, 0, 0)
    """
    dark_ratio = contrast_ratio(background, dark_color)
    light_ratio = contrast_ratio(background, light_color)
    
    if dark_ratio >= min_ratio:
        return dark_color
    if light_ratio >= min_ratio:
        return light_color
    
    # Return the one with better contrast
    return dark_color if dark_ratio > light_ratio else light_color


def find_accessible_colors(background: RGB, count: int = 10, 
                          min_ratio: float = 4.5) -> List[RGB]:
    """
    Find accessible foreground colors for a background.
    
    Args:
        background: Background RGB color
        count: Number of colors to return
        min_ratio: Minimum contrast ratio
        
    Returns:
        List of accessible RGB colors
        
    Example:
        >>> find_accessible_colors((128, 128, 128), 5)
        [(255, 255, 255), (0, 0, 0), ...]
    """
    colors = []
    
    # Try common colors first
    common = [
        (0, 0, 0), (255, 255, 255), (0, 0, 255), (255, 0, 0),
        (0, 255, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255)
    ]
    
    for color in common:
        if contrast_ratio(background, color) >= min_ratio:
            colors.append(color)
            if len(colors) >= count:
                return colors
    
    # Generate random colors
    attempts = 0
    while len(colors) < count and attempts < 1000:
        color = random_color()
        if contrast_ratio(background, color) >= min_ratio:
            colors.append(color)
        attempts += 1
    
    return colors


# ============================================================================
# Utility Functions
# ============================================================================

def is_valid_hex(hex_str: str) -> bool:
    """
    Check if a string is a valid HEX color.
    
    Args:
        hex_str: String to check
        
    Returns:
        True if valid HEX color
        
    Example:
        >>> is_valid_hex("#FF0000")
        True
        >>> is_valid_hex("FF0000")
        True
        >>> is_valid_hex("#FF0")
        True
    """
    hex_str = hex_str.lstrip('#')
    return bool(re.match(r'^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$', hex_str))


def rgb_to_int(rgb: RGB) -> int:
    """
    Convert RGB to integer representation.
    
    Args:
        rgb: RGB tuple
        
    Returns:
        Integer representation (0xRRGGBB)
        
    Example:
        >>> rgb_to_int((255, 0, 0))
        16711680
    """
    return (rgb[0] << 16) | (rgb[1] << 8) | rgb[2]


def int_to_rgb(value: int) -> RGB:
    """
    Convert integer to RGB.
    
    Args:
        value: Integer value (0xRRGGBB)
        
    Returns:
        RGB tuple
        
    Example:
        >>> int_to_rgb(16711680)
        (255, 0, 0)
    """
    r = (value >> 16) & 0xFF
    g = (value >> 8) & 0xFF
    b = value & 0xFF
    return (r, g, b)


def get_color_brightness(rgb: RGB) -> float:
    """
    Calculate perceived brightness of a color.
    
    Args:
        rgb: RGB tuple
        
    Returns:
        Brightness value (0-255)
        
    Example:
        >>> get_color_brightness((255, 255, 255))
        255.0
        >>> get_color_brightness((0, 0, 0))
        0.0
    """
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def interpolate_color(start: RGB, end: RGB, t: float) -> RGB:
    """
    Interpolate between two colors.
    
    Args:
        start: Starting RGB color
        end: Ending RGB color
        t: Interpolation factor (0.0-1.0)
        
    Returns:
        Interpolated RGB tuple
        
    Example:
        >>> interpolate_color((255, 0, 0), (0, 0, 255), 0.5)
        (128, 0, 128)
    """
    t = max(0, min(1, t))
    return (
        round(start[0] + (end[0] - start[0]) * t),
        round(start[1] + (end[1] - start[1]) * t),
        round(start[2] + (end[2] - start[2]) * t)
    )


def temperature_to_rgb(kelvin: float) -> RGB:
    """
    Convert color temperature (Kelvin) to RGB.
    
    Based on algorithm by Tanner Helland.
    
    Args:
        kelvin: Color temperature in Kelvin (1000-40000)
        
    Returns:
        RGB tuple approximating the color temperature
        
    Example:
        >>> temperature_to_rgb(6500)  # Daylight
        (255, 249, 253)
    """
    kelvin = max(1000, min(40000, kelvin))
    temp = kelvin / 100
    
    # Calculate red
    if temp <= 66:
        red = 255
    else:
        red = temp - 60
        red = 329.698727446 * (red ** -0.1332047592)
        red = max(0, min(255, red))
    
    # Calculate green
    if temp <= 66:
        green = temp
        green = 99.4708025861 * math.log(green) - 161.1195681661
        green = max(0, min(255, green))
    else:
        green = temp - 60
        green = 288.1221695283 * (green ** -0.0755148492)
        green = max(0, min(255, green))
    
    # Calculate blue
    if temp >= 66:
        blue = 255
    elif temp <= 19:
        blue = 0
    else:
        blue = temp - 10
        blue = 138.5177312231 * math.log(blue) - 305.0447927307
        blue = max(0, min(255, blue))
    
    return (round(red), round(green), round(blue))


def css_gradient(colors: List[RGB], direction: str = 'to right') -> str:
    """
    Generate CSS linear gradient string.
    
    Args:
        colors: List of RGB colors
        direction: Gradient direction ('to right', 'to left', 'to bottom', 'to top', etc.)
        
    Returns:
        CSS gradient string
        
    Example:
        >>> css_gradient([(255, 0, 0), (0, 0, 255)])
        'linear-gradient(to right, #FF0000 0%, #0000FF 100%)'
    """
    stops = []
    n = len(colors) - 1
    for i, color in enumerate(colors):
        percent = round((i / n) * 100) if n > 0 else 0
        stops.append(f"{rgb_to_hex(color)} {percent}%")
    
    return f"linear-gradient({direction}, {', '.join(stops)})"


# ============================================================================
# Convenience Functions
# ============================================================================

def create_color(r: int, g: int, b: int, a: float = 1.0) -> Color:
    """
    Create a Color object.
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        a: Alpha (0.0-1.0)
        
    Returns:
        Color object
        
    Example:
        >>> create_color(255, 0, 0)
        Color(r=255, g=0, b=0, a=1.0)
    """
    return Color(r, g, b, a)


def create_color_from_hex(hex_str: str) -> Color:
    """
    Create a Color object from HEX string.
    
    Args:
        hex_str: HEX color string
        
    Returns:
        Color object
        
    Example:
        >>> create_color_from_hex("#FF0000")
        Color(r=255, g=0, b=0, a=1.0)
    """
    return parse_color(hex_str)


def create_color_from_name(name: str) -> Optional[Color]:
    """
    Create a Color object from a named color.
    
    Args:
        name: Color name
        
    Returns:
        Color object or None if not found
        
    Example:
        >>> create_color_from_name("cornflowerblue")
        Color(r=100, g=149, b=237, a=1.0)
    """
    rgb = name_to_rgb(name)
    if rgb:
        return Color(*rgb)
    return None


if __name__ == "__main__":
    # Demo usage
    print("Color Utilities Demo")
    print("=" * 50)
    
    # Create colors
    red = create_color_from_hex("#FF0000")
    print(f"Red: {red}")
    print(f"  HEX: {red.hex_with_hash}")
    print(f"  HSL: {red.hsl}")
    print(f"  HSV: {red.hsv}")
    print(f"  CMYK: {red.cmyk}")
    
    # Color manipulation
    lighter = lighten(red.rgb, 30)
    darker = darken(red.rgb, 30)
    print(f"\nLighter: {rgb_to_hex(lighter)}")
    print(f"Darker: {rgb_to_hex(darker)}")
    
    # Complementary
    comp = complement(red.rgb)
    print(f"\nComplementary: {rgb_to_hex(comp)}")
    
    # Triadic palette
    triadic = triadic_palette(red.rgb)
    print(f"\nTriadic palette: {[rgb_to_hex(c) for c in triadic]}")
    
    # Contrast ratio
    contrast = contrast_ratio(red.rgb, (255, 255, 255))
    print(f"\nContrast with white: {contrast:.2f} ({wcag_rating(contrast)})")
    
    # Gradient
    gradient = gradient_palette((255, 0, 0), (0, 0, 255), 5)
    print(f"\nGradient: {[rgb_to_hex(c) for c in gradient]}")
    
    # Temperature
    warm = temperature_to_rgb(2700)  # Warm light
    cool = temperature_to_rgb(6500)  # Cool daylight
    print(f"\nWarm (2700K): {rgb_to_hex(warm)}")
    print(f"Cool (6500K): {rgb_to_hex(cool)}")