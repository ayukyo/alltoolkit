#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Color Utilities Module
====================================
A comprehensive color processing utility module for Python with zero external dependencies.

Features:
    - Color format conversion (RGB, HEX, HSL, HSV, CMYK, XYZ, LAB)
    - Color parsing from various string formats
    - Color mixing, blending, and manipulation
    - Complementary, analogous, triadic color generation
    - Brightness and contrast calculations
    - Color name lookup (CSS named colors)
    - Color distance calculation (Delta E approximation)
    - Gradient generation

Author: AllToolkit Contributors
License: MIT
"""

import math
import re
from typing import Union, Tuple, List, Optional, Dict
from dataclasses import dataclass


# ============================================================================
# Constants
# ============================================================================

# CSS named colors (subset of most common)
CSS_COLORS: Dict[str, Tuple[int, int, int]] = {
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

# Pre-compiled regex patterns for color parsing
_HEX_PATTERN = re.compile(r'^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$')
_RGB_PATTERN = re.compile(
    r'^rgb\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$',
    re.IGNORECASE
)
_RGBA_PATTERN = re.compile(
    r'^rgba\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*([01]?\.?\d*)\s*\)$',
    re.IGNORECASE
)
_HSL_PATTERN = re.compile(
    r'^hsl\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})%?\s*,\s*(\d{1,3})%?\s*\)$',
    re.IGNORECASE
)


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class RGB:
    """RGB color representation."""
    r: int  # 0-255
    g: int  # 0-255
    b: int  # 0-255
    a: float = 1.0  # 0.0-1.0 (alpha)
    
    def __post_init__(self):
        """Validate RGB values."""
        self.r = max(0, min(255, int(self.r)))
        self.g = max(0, min(255, int(self.g)))
        self.b = max(0, min(255, int(self.b)))
        self.a = max(0.0, min(1.0, float(self.a)))
    
    def to_hex(self, include_alpha: bool = False) -> str:
        """Convert to hex string."""
        if include_alpha and self.a < 1.0:
            alpha = round(self.a * 255)
            return f"#{self.r:02x}{self.g:02x}{self.b:02x}{alpha:02x}"
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    def to_hsl(self) -> 'HSL':
        """Convert to HSL."""
        h, s, l = rgb_to_hsl(self.r, self.g, self.b)
        return HSL(h, s, l)
    
    def to_hsv(self) -> 'HSV':
        """Convert to HSV."""
        h, s, v = rgb_to_hsv(self.r, self.g, self.b)
        return HSV(h, s, v)
    
    def to_cmyk(self) -> 'CMYK':
        """Convert to CMYK."""
        c, m, y, k = rgb_to_cmyk(self.r, self.g, self.b)
        return CMYK(c, m, y, k)
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert to tuple (r, g, b)."""
        return (self.r, self.g, self.b)
    
    def to_tuple_alpha(self) -> Tuple[int, int, int, float]:
        """Convert to tuple with alpha (r, g, b, a)."""
        return (self.r, self.g, self.b, self.a)


@dataclass
class HSL:
    """HSL color representation."""
    h: int  # 0-360 (hue)
    s: int  # 0-100 (saturation)
    l: int  # 0-100 (lightness)
    
    def __post_init__(self):
        """Validate HSL values."""
        self.h = int(self.h) % 360
        self.s = max(0, min(100, int(self.s)))
        self.l = max(0, min(100, int(self.l)))
    
    def to_rgb(self) -> RGB:
        """Convert to RGB."""
        r, g, b = hsl_to_rgb(self.h, self.s, self.l)
        return RGB(r, g, b)
    
    def to_hsv(self) -> 'HSV':
        """Convert to HSV via RGB."""
        return self.to_rgb().to_hsv()
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert to tuple (h, s, l)."""
        return (self.h, self.s, self.l)


@dataclass
class HSV:
    """HSV color representation."""
    h: int  # 0-360 (hue)
    s: int  # 0-100 (saturation)
    v: int  # 0-100 (value/brightness)
    
    def __post_init__(self):
        """Validate HSV values."""
        self.h = int(self.h) % 360
        self.s = max(0, min(100, int(self.s)))
        self.v = max(0, min(100, int(self.v)))
    
    def to_rgb(self) -> RGB:
        """Convert to RGB."""
        r, g, b = hsv_to_rgb(self.h, self.s, self.v)
        return RGB(r, g, b)
    
    def to_hsl(self) -> HSL:
        """Convert to HSL via RGB."""
        return self.to_rgb().to_hsl()
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert to tuple (h, s, v)."""
        return (self.h, self.s, self.v)


@dataclass
class CMYK:
    """CMYK color representation."""
    c: int  # 0-100 (cyan)
    m: int  # 0-100 (magenta)
    y: int  # 0-100 (yellow)
    k: int  # 0-100 (key/black)
    
    def __post_init__(self):
        """Validate CMYK values."""
        self.c = max(0, min(100, int(self.c)))
        self.m = max(0, min(100, int(self.m)))
        self.y = max(0, min(100, int(self.y)))
        self.k = max(0, min(100, int(self.k)))
    
    def to_rgb(self) -> RGB:
        """Convert to RGB."""
        r, g, b = cmyk_to_rgb(self.c, self.m, self.y, self.k)
        return RGB(r, g, b)
    
    def to_tuple(self) -> Tuple[int, int, int, int]:
        """Convert to tuple (c, m, y, k)."""
        return (self.c, self.m, self.y, self.k)


# ============================================================================
# Color Parsing Functions
# ============================================================================

def parse_hex(hex_str: str) -> RGB:
    """
    Parse a hex color string to RGB.
    
    Args:
        hex_str: Hex color string (e.g., '#ff0000', 'ff0000', '#f00', '#ff000080')
    
    Returns:
        RGB object
    
    Raises:
        ValueError: If invalid hex color format
    
    Examples:
        >>> parse_hex('#ff0000')
        RGB(r=255, g=0, b=0, a=1.0)
        >>> parse_hex('#f00')
        RGB(r=255, g=0, b=0, a=1.0)
        >>> parse_hex('#ff000080')
        RGB(r=255, g=0, b=0, a=0.5)
    """
    hex_str = hex_str.strip().lower()
    
    match = _HEX_PATTERN.match(hex_str)
    if not match:
        raise ValueError(f"Invalid hex color format: {hex_str}")
    
    hex_val = match.group(1)
    
    if len(hex_val) == 3:
        # Short format #RGB
        r = int(hex_val[0] * 2, 16)
        g = int(hex_val[1] * 2, 16)
        b = int(hex_val[2] * 2, 16)
        a = 1.0
    elif len(hex_val) == 6:
        # Standard format #RRGGBB
        r = int(hex_val[0:2], 16)
        g = int(hex_val[2:4], 16)
        b = int(hex_val[4:6], 16)
        a = 1.0
    elif len(hex_val) == 8:
        # With alpha #RRGGBBAA
        r = int(hex_val[0:2], 16)
        g = int(hex_val[2:4], 16)
        b = int(hex_val[4:6], 16)
        a = int(hex_val[6:8], 16) / 255.0
    else:
        raise ValueError(f"Invalid hex color format: {hex_str}")
    
    return RGB(r, g, b, a)


def parse_rgb(rgb_str: str) -> RGB:
    """
    Parse an rgb() or rgba() color string to RGB.
    
    Args:
        rgb_str: RGB color string (e.g., 'rgb(255, 0, 0)', 'rgba(255, 0, 0, 0.5)')
    
    Returns:
        RGB object
    
    Raises:
        ValueError: If invalid RGB color format or values out of range
    
    Examples:
        >>> parse_rgb('rgb(255, 0, 0)')
        RGB(r=255, g=0, b=0, a=1.0)
        >>> parse_rgb('rgba(255, 0, 0, 0.5)')
        RGB(r=255, g=0, b=0, a=0.5)
    """
    rgb_str = rgb_str.strip()
    
    # Try rgba first
    match = _RGBA_PATTERN.match(rgb_str)
    if match:
        r = int(match.group(1))
        g = int(match.group(2))
        b = int(match.group(3))
        a = float(match.group(4)) if match.group(4) else 1.0
        # Validate range
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError(f"RGB values must be 0-255: {rgb_str}")
        return RGB(r, g, b, a)
    
    # Try rgb
    match = _RGB_PATTERN.match(rgb_str)
    if match:
        r = int(match.group(1))
        g = int(match.group(2))
        b = int(match.group(3))
        # Validate range
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError(f"RGB values must be 0-255: {rgb_str}")
        return RGB(r, g, b, 1.0)
    
    raise ValueError(f"Invalid RGB color format: {rgb_str}")


def parse_hsl(hsl_str: str) -> HSL:
    """
    Parse an hsl() color string to HSL.
    
    Args:
        hsl_str: HSL color string (e.g., 'hsl(0, 100%, 50%)')
    
    Returns:
        HSL object
    
    Raises:
        ValueError: If invalid HSL color format
    
    Examples:
        >>> parse_hsl('hsl(0, 100%, 50%)')
        HSL(h=0, s=100, l=50)
    """
    hsl_str = hsl_str.strip()
    
    match = _HSL_PATTERN.match(hsl_str)
    if not match:
        raise ValueError(f"Invalid HSL color format: {hsl_str}")
    
    h = int(match.group(1))
    s = int(match.group(2))
    l = int(match.group(3))
    
    return HSL(h, s, l)


def parse_color(color: str) -> RGB:
    """
    Parse a color string in any supported format.
    
    Supports:
        - Hex: '#ff0000', 'ff0000', '#f00', '#ff000080'
        - RGB: 'rgb(255, 0, 0)', 'rgba(255, 0, 0, 0.5)'
        - HSL: 'hsl(0, 100%, 50%)'
        - Named: 'red', 'blue', 'coral', etc.
    
    Args:
        color: Color string in any supported format
    
    Returns:
        RGB object
    
    Raises:
        ValueError: If color format is not recognized
    
    Examples:
        >>> parse_color('#ff0000')
        RGB(r=255, g=0, b=0, a=1.0)
        >>> parse_color('red')
        RGB(r=255, g=0, b=0, a=1.0)
        >>> parse_color('hsl(0, 100%, 50%)')
        RGB(r=255, g=0, b=0, a=1.0)
    """
    color = color.strip()
    
    # Try hex
    if color.startswith('#') or _HEX_PATTERN.match(color):
        return parse_hex(color)
    
    # Try rgb/rgba
    if color.lower().startswith('rgb'):
        return parse_rgb(color)
    
    # Try hsl
    if color.lower().startswith('hsl'):
        hsl = parse_hsl(color)
        return hsl.to_rgb()
    
    # Try named color
    color_lower = color.lower()
    if color_lower in CSS_COLORS:
        r, g, b = CSS_COLORS[color_lower]
        return RGB(r, g, b)
    
    raise ValueError(f"Unrecognized color format: {color}")


def color_name_to_rgb(name: str) -> Optional[RGB]:
    """
    Convert a CSS color name to RGB.
    
    Args:
        name: CSS color name (e.g., 'red', 'coral', 'aliceblue')
    
    Returns:
        RGB object if found, None otherwise
    
    Examples:
        >>> color_name_to_rgb('red')
        RGB(r=255, g=0, b=0, a=1.0)
        >>> color_name_to_rgb('nonexistent')
        None
    """
    name_lower = name.lower().strip()
    if name_lower in CSS_COLORS:
        r, g, b = CSS_COLORS[name_lower]
        return RGB(r, g, b)
    return None


def rgb_to_color_name(rgb: RGB) -> Optional[str]:
    """
    Find the CSS color name for an RGB value.
    
    Args:
        rgb: RGB object
    
    Returns:
        CSS color name if found, None otherwise
    
    Examples:
        >>> rgb_to_color_name(RGB(255, 0, 0))
        'red'
        >>> rgb_to_color_name(RGB(123, 123, 123))
        None
    """
    target = (rgb.r, rgb.g, rgb.b)
    for name, values in CSS_COLORS.items():
        if values == target:
            return name
    return None


# ============================================================================
# Color Conversion Functions
# ============================================================================

def rgb_to_hex(r: int, g: int, b: int, include_hash: bool = True) -> str:
    """
    Convert RGB values to hex string.
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        include_hash: Whether to include '#' prefix
    
    Returns:
        Hex color string
    
    Examples:
        >>> rgb_to_hex(255, 0, 0)
        '#ff0000'
        >>> rgb_to_hex(255, 0, 0, include_hash=False)
        'ff0000'
    """
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    
    hex_str = f"{r:02x}{g:02x}{b:02x}"
    return f"#{hex_str}" if include_hash else hex_str


def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """
    Convert hex string to RGB tuple.
    
    Args:
        hex_str: Hex color string
    
    Returns:
        Tuple of (r, g, b)
    
    Raises:
        ValueError: If invalid hex format
    
    Examples:
        >>> hex_to_rgb('#ff0000')
        (255, 0, 0)
    """
    rgb = parse_hex(hex_str)
    return (rgb.r, rgb.g, rgb.b)


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[int, int, int]:
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
        (0, 100, 50)
        >>> rgb_to_hsl(0, 255, 0)
        (120, 100, 50)
    """
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0
    
    max_val = max(r_norm, g_norm, b_norm)
    min_val = min(r_norm, g_norm, b_norm)
    delta = max_val - min_val
    
    # Lightness
    l = (max_val + min_val) / 2.0
    
    # Saturation
    if delta == 0:
        s = 0.0
    else:
        s = delta / (1 - abs(2 * l - 1))
    
    # Hue
    if delta == 0:
        h = 0.0
    elif max_val == r_norm:
        h = 60 * (((g_norm - b_norm) / delta) % 6)
    elif max_val == g_norm:
        h = 60 * (((b_norm - r_norm) / delta) + 2)
    else:  # max_val == b_norm
        h = 60 * (((r_norm - g_norm) / delta) + 4)
    
    return (int(round(h)) % 360, int(round(s * 100)), int(round(l * 100)))


def hsl_to_rgb(h: int, s: int, l: int) -> Tuple[int, int, int]:
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
    s = max(0, min(100, s)) / 100.0
    l = max(0, min(100, l)) / 100.0
    
    if s == 0:
        # Grayscale
        val = int(round(l * 255))
        return (val, val, val)
    
    def hue_to_rgb(p: float, q: float, t: float) -> float:
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
    
    return (
        int(round(r * 255)),
        int(round(g * 255)),
        int(round(b * 255))
    )


def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[int, int, int]:
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
        (0, 100, 100)
    """
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0
    
    max_val = max(r_norm, g_norm, b_norm)
    min_val = min(r_norm, g_norm, b_norm)
    delta = max_val - min_val
    
    # Value
    v = max_val
    
    # Saturation
    if max_val == 0:
        s = 0.0
    else:
        s = delta / max_val
    
    # Hue
    if delta == 0:
        h = 0.0
    elif max_val == r_norm:
        h = 60 * (((g_norm - b_norm) / delta) % 6)
    elif max_val == g_norm:
        h = 60 * (((b_norm - r_norm) / delta) + 2)
    else:  # max_val == b_norm
        h = 60 * (((r_norm - g_norm) / delta) + 4)
    
    return (int(round(h)) % 360, int(round(s * 100)), int(round(v * 100)))


def hsv_to_rgb(h: int, s: int, v: int) -> Tuple[int, int, int]:
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
    s = max(0, min(100, s)) / 100.0
    v = max(0, min(100, v)) / 100.0
    
    if s == 0:
        val = int(round(v * 255))
        return (val, val, val)
    
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
    
    return (
        int(round((r + m) * 255)),
        int(round((g + m) * 255)),
        int(round((b + m) * 255))
    )


def rgb_to_cmyk(r: int, g: int, b: int) -> Tuple[int, int, int, int]:
    """
    Convert RGB to CMYK.
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
    
    Returns:
        Tuple of (c, m, y, k) where each is 0-100
    
    Examples:
        >>> rgb_to_cmyk(255, 0, 0)
        (0, 100, 100, 0)
        >>> rgb_to_cmyk(0, 0, 0)
        (0, 0, 0, 100)
        >>> rgb_to_cmyk(255, 255, 255)
        (0, 0, 0, 0)
    """
    if r == 0 and g == 0 and b == 0:
        return (0, 0, 0, 100)
    
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0
    
    k = 1 - max(r_norm, g_norm, b_norm)
    
    if k == 1:
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
    Convert CMYK to RGB.
    
    Args:
        c: Cyan (0-100)
        m: Magenta (0-100)
        y: Yellow (0-100)
        k: Key/Black (0-100)
    
    Returns:
        Tuple of (r, g, b) where each is 0-255
    
    Examples:
        >>> cmyk_to_rgb(0, 100, 100, 0)
        (255, 0, 0)
    """
    c = max(0, min(100, c)) / 100.0
    m = max(0, min(100, m)) / 100.0
    y = max(0, min(100, y)) / 100.0
    k = max(0, min(100, k)) / 100.0
    
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    
    return (
        int(round(r)),
        int(round(g)),
        int(round(b))
    )


# ============================================================================
# Color Manipulation Functions
# ============================================================================

def lighten(color: Union[str, RGB], amount: int = 10) -> RGB:
    """
    Lighten a color by increasing its lightness.
    
    Args:
        color: Color string or RGB object
        amount: Amount to lighten (0-100)
    
    Returns:
        Lightened RGB color
    
    Examples:
        >>> lighten('#ff0000', 20)
        RGB(r=255, g=102, b=102, a=1.0)
    """
    if isinstance(color, str):
        color = parse_color(color)
    
    h, s, l = rgb_to_hsl(color.r, color.g, color.b)
    l = min(100, l + amount)
    r, g, b = hsl_to_rgb(h, s, l)
    return RGB(r, g, b, color.a)


def darken(color: Union[str, RGB], amount: int = 10) -> RGB:
    """
    Darken a color by decreasing its lightness.
    
    Args:
        color: Color string or RGB object
        amount: Amount to darken (0-100)
    
    Returns:
        Darkened RGB color
    
    Examples:
        >>> darken('#ff0000', 20)
        RGB(r=204, g=0, b=0, a=1.0)
    """
    if isinstance(color, str):
        color = parse_color(color)
    
    h, s, l = rgb_to_hsl(color.r, color.g, color.b)
    l = max(0, l - amount)
    r, g, b = hsl_to_rgb(h, s, l)
    return RGB(r, g, b, color.a)


def saturate(color: Union[str, RGB], amount: int = 10) -> RGB:
    """
    Increase saturation of a color.
    
    Args:
        color: Color string or RGB object
        amount: Amount to saturate (0-100)
    
    Returns:
        Saturated RGB color
    
    Examples:
        >>> saturate('#cc6666', 20)
        RGB(r=230, g=77, b=77, a=1.0)
    """
    if isinstance(color, str):
        color = parse_color(color)
    
    h, s, l = rgb_to_hsl(color.r, color.g, color.b)
    s = min(100, s + amount)
    r, g, b = hsl_to_rgb(h, s, l)
    return RGB(r, g, b, color.a)


def desaturate(color: Union[str, RGB], amount: int = 10) -> RGB:
    """
    Decrease saturation of a color.
    
    Args:
        color: Color string or RGB object
        amount: Amount to desaturate (0-100)
    
    Returns:
        Desaturated RGB color
    
    Examples:
        >>> desaturate('#ff0000', 50)
        RGB(r=191, g=64, b=64, a=1.0)
    """
    if isinstance(color, str):
        color = parse_color(color)
    
    h, s, l = rgb_to_hsl(color.r, color.g, color.b)
    s = max(0, s - amount)
    r, g, b = hsl_to_rgb(h, s, l)
    return RGB(r, g, b, color.a)


def grayscale(color: Union[str, RGB]) -> RGB:
    """
    Convert a color to grayscale.
    
    Args:
        color: Color string or RGB object
    
    Returns:
        Grayscale RGB color
    
    Examples:
        >>> grayscale('#ff0000')
        RGB(r=76, g=76, b=76, a=1.0)
    """
    if isinstance(color, str):
        color = parse_color(color)
    
    # Use luminance formula (perceptual)
    gray = int(0.299 * color.r + 0.587 * color.g + 0.114 * color.b)
    return RGB(gray, gray, gray, color.a)


def invert(color: Union[str, RGB]) -> RGB:
    """
    Invert a color.
    
    Args:
        color: Color string or RGB object
    
    Returns:
        Inverted RGB color
    
    Examples:
        >>> invert('#000000')
        RGB(r=255, g=255, b=255, a=1.0)
        >>> invert('#ff0000')
        RGB(r=0, g=255, b=255, a=1.0)
    """
    if isinstance(color, str):
        color = parse_color(color)
    
    return RGB(
        255 - color.r,
        255 - color.g,
        255 - color.b,
        color.a
    )


def complement(color: Union[str, RGB]) -> RGB:
    """
    Get the complementary color (opposite on color wheel).
    
    Args:
        color: Color string or RGB object
    
    Returns:
        Complementary RGB color
    
    Examples:
        >>> complement('#ff0000')
        RGB(r=0, g=255, b=255, a=1.0)
    """
    if isinstance(color, str):
        color = parse_color(color)
    
    h, s, l = rgb_to_hsl(color.r, color.g, color.b)
    h = (h + 180) % 360
    r, g, b = hsl_to_rgb(h, s, l)
    return RGB(r, g, b, color.a)


def mix(color1: Union[str, RGB], color2: Union[str, RGB], weight: float = 0.5) -> RGB:
    """
    Mix two colors together.
    
    Args:
        color1: First color string or RGB object
        color2: Second color string or RGB object
        weight: Weight of first color (0.0-1.0), default 0.5
    
    Returns:
        Mixed RGB color
    
    Examples:
        >>> mix('#ff0000', '#0000ff', 0.5)
        RGB(r=128, g=0, b=128, a=1.0)
    """
    if isinstance(color1, str):
        color1 = parse_color(color1)
    if isinstance(color2, str):
        color2 = parse_color(color2)
    
    weight = max(0.0, min(1.0, weight))
    w2 = 1.0 - weight
    
    r = int(round(color1.r * weight + color2.r * w2))
    g = int(round(color1.g * weight + color2.g * w2))
    b = int(round(color1.b * weight + color2.b * w2))
    a = color1.a * weight + color2.a * w2
    
    return RGB(r, g, b, a)


def blend(color1: Union[str, RGB], color2: Union[str, RGB], mode: str = 'normal') -> RGB:
    """
    Blend two colors using a blend mode.
    
    Args:
        color1: Base color string or RGB object
        color2: Blend color string or RGB object
        mode: Blend mode ('normal', 'multiply', 'screen', 'overlay', 'soft_light', 'hard_light')
    
    Returns:
        Blended RGB color
    
    Examples:
        >>> blend('#ff0000', '#0000ff', 'multiply')
        RGB(r=0, g=0, b=0, a=1.0)
    """
    if isinstance(color1, str):
        color1 = parse_color(color1)
    if isinstance(color2, str):
        color2 = parse_color(color2)
    
    mode = mode.lower()
    
    def multiply(a: int, b: int) -> int:
        return int((a / 255.0) * (b / 255.0) * 255)
    
    def screen(a: int, b: int) -> int:
        return int(255 - (255 - a) * (255 - b) / 255.0)
    
    def overlay(a: int, b: int) -> int:
        a_norm = a / 255.0
        b_norm = b / 255.0
        if a_norm < 0.5:
            return int(2 * a_norm * b_norm * 255)
        else:
            return int((1 - 2 * (1 - a_norm) * (1 - b_norm)) * 255)
    
    if mode == 'normal':
        return color2
    elif mode == 'multiply':
        return RGB(multiply(color1.r, color2.r), multiply(color1.g, color2.g), multiply(color1.b, color2.b))
    elif mode == 'screen':
        return RGB(screen(color1.r, color2.r), screen(color1.g, color2.g), screen(color1.b, color2.b))
    elif mode == 'overlay':
        return RGB(overlay(color1.r, color2.r), overlay(color1.g, color2.g), overlay(color1.b, color2.b))
    elif mode == 'soft_light':
        # Soft light is a gentler version of overlay
        def soft_light(a: int, b: int) -> int:
            a_norm = a / 255.0
            b_norm = b / 255.0
            if b_norm < 0.5:
                return int((2 * a_norm - 1) * (b_norm - b_norm * b_norm) + a_norm * 255)
            else:
                return int((2 * a_norm - 1) * (math.sqrt(b_norm) - b_norm) + a_norm * 255)
        return RGB(soft_light(color1.r, color2.r), soft_light(color1.g, color2.g), soft_light(color1.b, color2.b))
    elif mode == 'hard_light':
        # Hard light is like overlay but with colors swapped
        return RGB(overlay(color2.r, color1.r), overlay(color2.g, color1.g), overlay(color2.b, color1.b))
    else:
        raise ValueError(f"Unknown blend mode: {mode}")


# ============================================================================
# Color Harmony Functions
# ============================================================================

def analogous(color: Union[str, RGB], angle: int = 30) -> List[RGB]:
    """
    Get analogous colors (adjacent on color wheel).
    
    Args:
        color: Color string or RGB object
        angle: Angle between colors (default 30 degrees)
    
    Returns:
        List of 3 RGB colors (original, and two adjacent)
    
    Examples:
        >>> len(analogous('#ff0000'))
        3
    """
    if isinstance(color, str):
        color = parse_color(color)
    
    h, s, l = rgb_to_hsl(color.r, color.g, color.b)
    
    colors = [color]
    
    # Left color
    h_left = (h - angle) % 360
    r, g, b = hsl_to_rgb(h_left, s, l)
    colors.append(RGB(r, g, b))
    
    # Right color
    h_right = (h + angle) % 360
    r, g, b = hsl_to_rgb(h_right, s, l)
    colors.append(RGB(r, g, b))
    
    return colors


def triadic(color: Union[str, RGB]) -> List[RGB]:
    """
    Get triadic colors (three colors equally spaced on color wheel).
    
    Args:
        color: Color string or RGB object
    
    Returns:
        List of 3 RGB colors
    
    Examples:
        >>> triadic('#ff0000')
        [RGB(r=255, g=0, b=0, a=1.0), RGB(r=0, g=255, b=0, a=1.0), RGB(r=0, g=0, b=255, a=1.0)]
    """
    if isinstance(color, str):
        color = parse_color(color)
    
    h, s, l = rgb_to_hsl(color.r, color.g, color.b)
    
    colors = [color]
    
    for i in range(1, 3):
        h_new = (h + i * 120) % 360
        r, g, b = hsl_to_rgb(h_new, s, l)
        colors.append(RGB(r, g, b))
    
    return colors


def split_complement(color: Union[str, RGB], angle: int = 30) -> List[RGB]:
    """
    Get split complementary colors.
    
    Args:
        color: Color string or RGB object
        angle: Angle from complement (default 30 degrees)
    
    Returns:
        List of 3 RGB colors
    
    Examples:
        >>> len(split_complement('#ff0000'))
        3
    """
    if isinstance(color, str):
        color = parse_color(color)
    
    h, s, l = rgb_to_hsl(color.r, color.g, color.b)
    
    colors = [color]
    
    # Split complements
    for delta in [angle, -angle]:
        h_new = (h + 180 + delta) % 360
        r, g, b = hsl_to_rgb(h_new, s, l)
        colors.append(RGB(r, g, b))
    
    return colors


def tetradic(color: Union[str, RGB]) -> List[RGB]:
    """
    Get tetradic colors (four colors forming a rectangle on color wheel).
    
    Args:
        color: Color string or RGB object
    
    Returns:
        List of 4 RGB colors
    
    Examples:
        >>> len(tetradic('#ff0000'))
        4
    """
    if isinstance(color, str):
        color = parse_color(color)
    
    h, s, l = rgb_to_hsl(color.r, color.g, color.b)
    
    colors = [color]
    
    for angle in [90, 180, 270]:
        h_new = (h + angle) % 360
        r, g, b = hsl_to_rgb(h_new, s, l)
        colors.append(RGB(r, g, b))
    
    return colors


def monochromatic(color: Union[str, RGB], steps: int = 5) -> List[RGB]:
    """
    Get monochromatic color variations.
    
    Args:
        color: Color string or RGB object
        steps: Number of variations (default 5)
    
    Returns:
        List of RGB colors
    
    Examples:
        >>> len(monochromatic('#ff0000', 5))
        5
    """
    if isinstance(color, str):
        color = parse_color(color)
    
    h, s, l = rgb_to_hsl(color.r, color.g, color.b)
    
    colors = []
    step_size = 100 / (steps + 1)
    
    for i in range(1, steps + 1):
        new_l = int(step_size * i)
        r, g, b = hsl_to_rgb(h, s, new_l)
        colors.append(RGB(r, g, b))
    
    return colors


# ============================================================================
# Color Utility Functions
# ============================================================================

def luminance(color: Union[str, RGB]) -> float:
    """
    Calculate relative luminance of a color.
    
    Args:
        color: Color string or RGB object
    
    Returns:
        Relative luminance (0.0-1.0)
    
    Examples:
        >>> round(luminance('#ffffff'), 2)
        1.0
        >>> round(luminance('#000000'), 2)
        0.0
    """
    if isinstance(color, str):
        color = parse_color(color)
    
    def convert(c: int) -> float:
        c_norm = c / 255.0
        return c_norm / 12.92 if c_norm <= 0.03928 else ((c_norm + 0.055) / 1.055) ** 2.4
    
    return 0.2126 * convert(color.r) + 0.7152 * convert(color.g) + 0.0722 * convert(color.b)


def contrast_ratio(color1: Union[str, RGB], color2: Union[str, RGB]) -> float:
    """
    Calculate contrast ratio between two colors (WCAG).
    
    Args:
        color1: First color string or RGB object
        color2: Second color string or RGB object
    
    Returns:
        Contrast ratio (1:1 to 21:1)
    
    Examples:
        >>> round(contrast_ratio('#ffffff', '#000000'), 1)
        21.0
        >>> round(contrast_ratio('#ffffff', '#ffffff'), 1)
        1.0
    """
    if isinstance(color1, str):
        color1 = parse_color(color1)
    if isinstance(color2, str):
        color2 = parse_color(color2)
    
    l1 = luminance(color1)
    l2 = luminance(color2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


def wcag_rating(ratio: float) -> str:
    """
    Get WCAG rating for a contrast ratio.
    
    Args:
        ratio: Contrast ratio
    
    Returns:
        WCAG rating string ('AAA', 'AA', 'AA Large', 'Fail')
    
    Examples:
        >>> wcag_rating(7.0)
        'AAA'
        >>> wcag_rating(4.5)
        'AA'
        >>> wcag_rating(3.0)
        'AA Large'
        >>> wcag_rating(2.0)
        'Fail'
    """
    if ratio >= 7.0:
        return 'AAA'
    elif ratio >= 4.5:
        return 'AA'
    elif ratio >= 3.0:
        return 'AA Large'
    else:
        return 'Fail'


def brightness(color: Union[str, RGB]) -> int:
    """
    Calculate perceived brightness of a color (0-255).
    
    Args:
        color: Color string or RGB object
    
    Returns:
        Brightness value (0-255)
    
    Examples:
        >>> brightness('#ffffff')
        255
        >>> brightness('#000000')
        0
    """
    if isinstance(color, str):
        color = parse_color(color)
    
    # Perceived brightness formula
    return int(0.299 * color.r + 0.587 * color.g + 0.114 * color.b)


def is_light(color: Union[str, RGB]) -> bool:
    """
    Check if a color is light.
    
    Args:
        color: Color string or RGB object
    
    Returns:
        True if light, False if dark
    
    Examples:
        >>> is_light('#ffffff')
        True
        >>> is_light('#000000')
        False
    """
    return brightness(color) > 127


def is_dark(color: Union[str, RGB]) -> bool:
    """
    Check if a color is dark.
    
    Args:
        color: Color string or RGB object
    
    Returns:
        True if dark, False if light
    
    Examples:
        >>> is_dark('#000000')
        True
        >>> is_dark('#ffffff')
        False
    """
    return brightness(color) <= 127


def text_color_for_bg(background: Union[str, RGB], light_color: str = '#ffffff', dark_color: str = '#000000') -> str:
    """
    Get appropriate text color for a background.
    
    Args:
        background: Background color string or RGB object
        light_color: Light text color (default white)
        dark_color: Dark text color (default black)
    
    Returns:
        Either light_color or dark_color based on background brightness
    
    Examples:
        >>> text_color_for_bg('#ffffff')
        '#000000'
        >>> text_color_for_bg('#000000')
        '#ffffff'
    """
    return light_color if is_dark(background) else dark_color


def color_distance(color1: Union[str, RGB], color2: Union[str, RGB]) -> float:
    """
    Calculate Euclidean distance between two colors in RGB space.
    
    Args:
        color1: First color string or RGB object
        color2: Second color string or RGB object
    
    Returns:
        Distance (0-441.67 for RGB cube diagonal)
    
    Examples:
        >>> round(color_distance('#ff0000', '#ff0000'), 1)
        0.0
        >>> round(color_distance('#000000', '#ffffff'), 1)
        441.7
    """
    if isinstance(color1, str):
        color1 = parse_color(color1)
    if isinstance(color2, str):
        color2 = parse_color(color2)
    
    return math.sqrt(
        (color1.r - color2.r) ** 2 +
        (color1.g - color2.g) ** 2 +
        (color1.b - color2.b) ** 2
    )


def closest_color(color: Union[str, RGB], color_list: List[Union[str, RGB]]) -> int:
    """
    Find the closest color in a list.
    
    Args:
        color: Target color string or RGB object
        color_list: List of colors to search
    
    Returns:
        Index of the closest color in the list
    
    Raises:
        ValueError: If color_list is empty
    
    Examples:
        >>> closest_color('#ff0000', ['#ff0000', '#00ff00', '#0000ff'])
        0
    """
    if not color_list:
        raise ValueError("color_list cannot be empty")
    
    if isinstance(color, str):
        color = parse_color(color)
    
    min_distance = float('inf')
    closest_idx = 0
    
    for i, c in enumerate(color_list):
        if isinstance(c, str):
            c = parse_color(c)
        
        dist = color_distance(color, c)
        if dist < min_distance:
            min_distance = dist
            closest_idx = i
    
    return closest_idx


# ============================================================================
# Gradient Functions
# ============================================================================

def gradient(start_color: Union[str, RGB], end_color: Union[str, RGB], steps: int = 10) -> List[RGB]:
    """
    Generate a gradient between two colors.
    
    Args:
        start_color: Starting color string or RGB object
        end_color: Ending color string or RGB object
        steps: Number of steps in gradient (default 10)
    
    Returns:
        List of RGB colors forming the gradient
    
    Examples:
        >>> len(gradient('#000000', '#ffffff', 5))
        5
        >>> gradient('#000000', '#ffffff', 3)[0]
        RGB(r=0, g=0, b=0, a=1.0)
        >>> gradient('#000000', '#ffffff', 3)[2]
        RGB(r=255, g=255, b=255, a=1.0)
    """
    if isinstance(start_color, str):
        start_color = parse_color(start_color)
    if isinstance(end_color, str):
        end_color = parse_color(end_color)
    
    if steps < 2:
        steps = 2
    
    colors = []
    for i in range(steps):
        # weight for start_color: at step 0, weight=1 (100% start); at last step, weight=0 (100% end)
        weight = 1.0 - (i / (steps - 1)) if steps > 1 else 0.5
        colors.append(mix(start_color, end_color, weight))
    
    return colors


def multi_gradient(colors: List[Union[str, RGB]], steps_per_segment: int = 10) -> List[RGB]:
    """
    Generate a gradient through multiple colors.
    
    Args:
        colors: List of color strings or RGB objects
        steps_per_segment: Steps between each color pair
    
    Returns:
        List of RGB colors forming the multi-color gradient
    
    Examples:
        >>> len(multi_gradient(['#ff0000', '#00ff00', '#0000ff'], 5))
        11
    """
    if len(colors) < 2:
        raise ValueError("At least 2 colors required for gradient")
    
    result = []
    for i in range(len(colors) - 1):
        segment = gradient(colors[i], colors[i + 1], steps_per_segment)
        # Avoid duplicating the last color of each segment (except final)
        if i < len(colors) - 2:
            segment = segment[:-1]
        result.extend(segment)
    
    return result


# ============================================================================
# Random Color Functions
# ============================================================================

def random_color(seed: Optional[int] = None) -> RGB:
    """
    Generate a random color.
    
    Args:
        seed: Optional random seed for reproducibility
    
    Returns:
        Random RGB color
    
    Examples:
        >>> isinstance(random_color(), RGB)
        True
    """
    import random as rand
    
    if seed is not None:
        rand.seed(seed)
    
    return RGB(rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255))


def random_hue(saturation: int = 70, lightness: int = 50) -> RGB:
    """
    Generate a random color with specified saturation and lightness.
    
    Args:
        saturation: Saturation (0-100)
        lightness: Lightness (0-100)
    
    Returns:
        Random RGB color with specified s and l
    
    Examples:
        >>> isinstance(random_hue(80, 60), RGB)
        True
    """
    import random as rand
    
    h = rand.randint(0, 359)
    r, g, b = hsl_to_rgb(h, saturation, lightness)
    return RGB(r, g, b)


def random_pastel() -> RGB:
    """
    Generate a random pastel color.
    
    Returns:
        Random pastel RGB color
    
    Examples:
        >>> isinstance(random_pastel(), RGB)
        True
    """
    import random as rand
    
    h = rand.randint(0, 359)
    s = rand.randint(40, 60)
    l = rand.randint(75, 90)
    r, g, b = hsl_to_rgb(h, s, l)
    return RGB(r, g, b)


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=== Color Parsing Examples ===")
    print(f"parse_hex('#ff0000'): {parse_hex('#ff0000')}")
    print(f"parse_rgb('rgb(255, 0, 0)'): {parse_rgb('rgb(255, 0, 0)')}")
    print(f"parse_hsl('hsl(0, 100%, 50%)'): {parse_hsl('hsl(0, 100%, 50%)')}")
    print(f"parse_color('red'): {parse_color('red')}")
    
    print("\n=== Color Conversion Examples ===")
    print(f"rgb_to_hex(255, 0, 0): {rgb_to_hex(255, 0, 0)}")
    print(f"rgb_to_hsl(255, 0, 0): {rgb_to_hsl(255, 0, 0)}")
    print(f"hsl_to_rgb(0, 100, 50): {hsl_to_rgb(0, 100, 50)}")
    print(f"rgb_to_hsv(255, 0, 0): {rgb_to_hsv(255, 0, 0)}")
    print(f"rgb_to_cmyk(255, 0, 0): {rgb_to_cmyk(255, 0, 0)}")
    
    print("\n=== Color Manipulation Examples ===")
    print(f"lighten('#ff0000', 20): {lighten('#ff0000', 20)}")
    print(f"darken('#ff0000', 20): {darken('#ff0000', 20)}")
    print(f"complement('#ff0000'): {complement('#ff0000')}")
    print(f"mix('#ff0000', '#0000ff', 0.5): {mix('#ff0000', '#0000ff', 0.5)}")
    
    print("\n=== Color Harmony Examples ===")
    print(f"triadic('#ff0000'): {triadic('#ff0000')}")
    print(f"analogous('#ff0000'): {analogous('#ff0000')}")
    
    print("\n=== Contrast Examples ===")
    print(f"contrast_ratio('#ffffff', '#000000'): {contrast_ratio('#ffffff', '#000000'):.2f}")
    print(f"wcag_rating(7.5): {wcag_rating(7.5)}")
    print(f"is_light('#ffffff'): {is_light('#ffffff')}")
    print(f"text_color_for_bg('#ff0000'): {text_color_for_bg('#ff0000')}")
    
    print("\n=== Gradient Examples ===")
    grad = gradient('#ff0000', '#0000ff', 5)
    print(f"5-step gradient from red to blue: {[c.to_hex() for c in grad]}")