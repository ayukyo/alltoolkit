#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Color Utilities Module
====================================
A comprehensive color manipulation utility module for Python with zero external dependencies.

Features:
    - Color format conversion (RGB, HEX, HSL, HSV, CMYK)
    - Color manipulation (lighten, darken, mix, invert)
    - Color palette generation (complementary, analogous, triadic, etc.)
    - Color accessibility (contrast ratio, WCAG compliance)
    - Color naming and identification
    - Gradient generation

Author: AllToolkit Contributors
License: MIT
"""

import math
import re
from typing import Dict, List, Optional, Tuple, Union


# ============================================================================
# Type Aliases
# ============================================================================

RGB = Tuple[int, int, int]
RGBA = Tuple[int, int, int, float]
HSL = Tuple[float, float, float]
HSV = Tuple[float, float, float]
CMYK = Tuple[float, float, float, float]
HexColor = str


# ============================================================================
# Color Conversion Functions
# ============================================================================

def hex_to_rgb(hex_color: HexColor) -> RGB:
    """
    Convert HEX color to RGB.
    
    Args:
        hex_color: Hex color string (e.g., "#FF5733", "FF5733", "#F53")
    
    Returns:
        Tuple of (R, G, B) values (0-255)
    
    Example:
        >>> hex_to_rgb("#FF5733")
        (255, 87, 51)
        >>> hex_to_rgb("#F53")
        (255, 85, 51)
    """
    hex_color = hex_color.lstrip('#')
    
    # Handle shorthand hex (e.g., #F53 -> #FF5533)
    if len(hex_color) == 3:
        hex_color = ''.join([c * 2 for c in hex_color])
    
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")
    
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b)
    except ValueError:
        raise ValueError(f"Invalid hex color: #{hex_color}")


def rgb_to_hex(rgb: RGB) -> HexColor:
    """
    Convert RGB to HEX color.
    
    Args:
        rgb: Tuple of (R, G, B) values (0-255)
    
    Returns:
        Hex color string (e.g., "#FF5733")
    
    Example:
        >>> rgb_to_hex((255, 87, 51))
        '#FF5733'
    """
    if len(rgb) != 3:
        raise ValueError("RGB must be a tuple of 3 values")
    
    r, g, b = rgb
    
    if not all(0 <= c <= 255 for c in (r, g, b)):
        raise ValueError("RGB values must be between 0 and 255")
    
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsl(rgb: RGB) -> HSL:
    """
    Convert RGB to HSL.
    
    Args:
        rgb: Tuple of (R, G, B) values (0-255)
    
    Returns:
        Tuple of (H, S, L) where H is 0-360, S and L are 0-100
    
    Example:
        >>> rgb_to_hsl((255, 87, 51))
        (11.0, 100.0, 60.0)
    """
    r, g, b = [c / 255.0 for c in rgb]
    
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    l = (max_c + min_c) / 2.0
    
    if max_c == min_c:
        h = s = 0.0
    else:
        d = max_c - min_c
        s = d / (2.0 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
        
        if max_c == r:
            h = (g - b) / d + (6.0 if g < b else 0.0)
        elif max_c == g:
            h = (b - r) / d + 2.0
        else:
            h = (r - g) / d + 4.0
        
        h /= 6.0
    
    return (round(h * 360), round(s * 100), round(l * 100))


def hsl_to_rgb(hsl: HSL) -> RGB:
    """
    Convert HSL to RGB.
    
    Args:
        hsl: Tuple of (H, S, L) where H is 0-360, S and L are 0-100
    
    Returns:
        Tuple of (R, G, B) values (0-255)
    
    Example:
        >>> hsl_to_rgb((11, 100, 60))
        (255, 87, 51)
    """
    h, s, l = hsl[0] / 360.0, hsl[1] / 100.0, hsl[2] / 100.0
    
    if s == 0:
        r = g = b = l
    else:
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
        
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)
    
    return (round(r * 255), round(g * 255), round(b * 255))


def rgb_to_hsv(rgb: RGB) -> HSV:
    """
    Convert RGB to HSV.
    
    Args:
        rgb: Tuple of (R, G, B) values (0-255)
    
    Returns:
        Tuple of (H, S, V) where H is 0-360, S and V are 0-100
    
    Example:
        >>> rgb_to_hsv((255, 87, 51))
        (11, 80, 100)
    """
    r, g, b = [c / 255.0 for c in rgb]
    
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    v = max_c
    d = max_c - min_c
    
    s = 0.0 if max_c == 0 else d / max_c
    
    if max_c == min_c:
        h = 0.0
    else:
        if max_c == r:
            h = (g - b) / d + (6.0 if g < b else 0.0)
        elif max_c == g:
            h = (b - r) / d + 2.0
        else:
            h = (r - g) / d + 4.0
        h /= 6.0
    
    return (round(h * 360), round(s * 100), round(v * 100))


def hsv_to_rgb(hsv: HSV) -> RGB:
    """
    Convert HSV to RGB.
    
    Args:
        hsv: Tuple of (H, S, V) where H is 0-360, S and V are 0-100
    
    Returns:
        Tuple of (R, G, B) values (0-255)
    
    Example:
        >>> hsv_to_rgb((11, 80, 100))
        (255, 87, 51)
    """
    h, s, v = hsv[0] / 360.0, hsv[1] / 100.0, hsv[2] / 100.0
    
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
    
    return (round(r * 255), round(g * 255), round(b * 255))


def rgb_to_cmyk(rgb: RGB) -> CMYK:
    """
    Convert RGB to CMYK.
    
    Args:
        rgb: Tuple of (R, G, B) values (0-255)
    
    Returns:
        Tuple of (C, M, Y, K) values (0-100)
    
    Example:
        >>> rgb_to_cmyk((255, 87, 51))
        (0, 66, 80, 0)
    """
    r, g, b = [c / 255.0 for c in rgb]
    
    k = 1 - max(r, g, b)
    
    if k == 1:
        return (0, 0, 0, 100)
    
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    
    return (round(c * 100), round(m * 100), round(y * 100), round(k * 100))


def cmyk_to_rgb(cmyk: CMYK) -> RGB:
    """
    Convert CMYK to RGB.
    
    Args:
        cmyk: Tuple of (C, M, Y, K) values (0-100)
    
    Returns:
        Tuple of (R, G, B) values (0-255)
    
    Example:
        >>> cmyk_to_rgb((0, 66, 80, 0))
        (255, 87, 51)
    """
    c, m, y, k = [v / 100.0 for v in cmyk]
    
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    
    return (round(r), round(g), round(b))


def hex_to_hsl(hex_color: HexColor) -> HSL:
    """Convert HEX to HSL."""
    return rgb_to_hsl(hex_to_rgb(hex_color))


def hsl_to_hex(hsl: HSL) -> HexColor:
    """Convert HSL to HEX."""
    return rgb_to_hex(hsl_to_rgb(hsl))


def hex_to_hsv(hex_color: HexColor) -> HSV:
    """Convert HEX to HSV."""
    return rgb_to_hsv(hex_to_rgb(hex_color))


def hsv_to_hex(hsv: HSV) -> HexColor:
    """Convert HSV to HEX."""
    return rgb_to_hex(hsv_to_rgb(hsv))


def hex_to_cmyk(hex_color: HexColor) -> CMYK:
    """Convert HEX to CMYK."""
    return rgb_to_cmyk(hex_to_rgb(hex_color))


def cmyk_to_hex(cmyk: CMYK) -> HexColor:
    """Convert CMYK to HEX."""
    return rgb_to_hex(cmyk_to_rgb(cmyk))


# ============================================================================
# Color Manipulation Functions
# ============================================================================

def lighten(color: Union[RGB, HexColor], amount: float = 0.1) -> Union[RGB, HexColor]:
    """
    Lighten a color by increasing lightness.
    
    Args:
        color: RGB tuple or HEX string
        amount: Amount to lighten (0.0 to 1.0)
    
    Returns:
        Lightened color in same format as input
    
    Example:
        >>> lighten("#FF5733", 0.2)
        '#FF8C6F'
    """
    is_hex = isinstance(color, str)
    rgb = hex_to_rgb(color) if is_hex else color
    hsl = rgb_to_hsl(rgb)
    
    # Increase lightness
    new_l = min(100, hsl[2] + amount * 100)
    new_hsl = (hsl[0], hsl[1], new_l)
    new_rgb = hsl_to_rgb(new_hsl)
    
    return rgb_to_hex(new_rgb) if is_hex else new_rgb


def darken(color: Union[RGB, HexColor], amount: float = 0.1) -> Union[RGB, HexColor]:
    """
    Darken a color by decreasing lightness.
    
    Args:
        color: RGB tuple or HEX string
        amount: Amount to darken (0.0 to 1.0)
    
    Returns:
        Darkened color in same format as input
    
    Example:
        >>> darken("#FF5733", 0.2)
        '#CC3A1A'
    """
    is_hex = isinstance(color, str)
    rgb = hex_to_rgb(color) if is_hex else color
    hsl = rgb_to_hsl(rgb)
    
    # Decrease lightness
    new_l = max(0, hsl[2] - amount * 100)
    new_hsl = (hsl[0], hsl[1], new_l)
    new_rgb = hsl_to_rgb(new_hsl)
    
    return rgb_to_hex(new_rgb) if is_hex else new_rgb


def mix_colors(color1: Union[RGB, HexColor], 
               color2: Union[RGB, HexColor], 
               ratio: float = 0.5) -> Union[RGB, HexColor]:
    """
    Mix two colors together.
    
    Args:
        color1: First color (RGB or HEX)
        color2: Second color (RGB or HEX)
        ratio: Mix ratio (0.0 = all color1, 1.0 = all color2)
    
    Returns:
        Mixed color in same format as color1
    
    Example:
        >>> mix_colors("#FF0000", "#0000FF", 0.5)
        '#800080'
    """
    is_hex = isinstance(color1, str)
    rgb1 = hex_to_rgb(color1) if is_hex else color1
    rgb2 = hex_to_rgb(color2) if isinstance(color2, str) else color2
    
    r = round(rgb1[0] + (rgb2[0] - rgb1[0]) * ratio)
    g = round(rgb1[1] + (rgb2[1] - rgb1[1]) * ratio)
    b = round(rgb1[2] + (rgb2[2] - rgb1[2]) * ratio)
    
    new_rgb = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    return rgb_to_hex(new_rgb) if is_hex else new_rgb


def invert_color(color: Union[RGB, HexColor]) -> Union[RGB, HexColor]:
    """
    Invert a color (get the opposite).
    
    Args:
        color: RGB tuple or HEX string
    
    Returns:
        Inverted color in same format as input
    
    Example:
        >>> invert_color("#FF5733")
        '#00A8CC'
    """
    is_hex = isinstance(color, str)
    rgb = hex_to_rgb(color) if is_hex else color
    
    inverted = (255 - rgb[0], 255 - rgb[1], 255 - rgb[2])
    
    return rgb_to_hex(inverted) if is_hex else inverted


def saturate(color: Union[RGB, HexColor], amount: float = 0.1) -> Union[RGB, HexColor]:
    """
    Increase color saturation.
    
    Args:
        color: RGB tuple or HEX string
        amount: Amount to saturate (0.0 to 1.0)
    
    Returns:
        Saturated color in same format as input
    
    Example:
        >>> saturate("#FF5733", 0.2)
        '#FF4D22'
    """
    is_hex = isinstance(color, str)
    rgb = hex_to_rgb(color) if is_hex else color
    hsl = rgb_to_hsl(rgb)
    
    # Increase saturation
    new_s = min(100, hsl[1] + amount * 100)
    new_hsl = (hsl[0], new_s, hsl[2])
    new_rgb = hsl_to_rgb(new_hsl)
    
    return rgb_to_hex(new_rgb) if is_hex else new_rgb


def desaturate(color: Union[RGB, HexColor], amount: float = 0.1) -> Union[RGB, HexColor]:
    """
    Decrease color saturation (make more gray).
    
    Args:
        color: RGB tuple or HEX string
        amount: Amount to desaturate (0.0 to 1.0)
    
    Returns:
        Desaturated color in same format as input
    
    Example:
        >>> desaturate("#FF5733", 0.5)
        '#997A66'
    """
    is_hex = isinstance(color, str)
    rgb = hex_to_rgb(color) if is_hex else color
    hsl = rgb_to_hsl(rgb)
    
    # Decrease saturation
    new_s = max(0, hsl[1] - amount * 100)
    new_hsl = (hsl[0], new_s, hsl[2])
    new_rgb = hsl_to_rgb(new_hsl)
    
    return rgb_to_hex(new_rgb) if is_hex else new_rgb


def adjust_hue(color: Union[RGB, HexColor], degrees: float) -> Union[RGB, HexColor]:
    """
    Adjust the hue of a color by rotating the color wheel.
    
    Args:
        color: RGB tuple or HEX string
        degrees: Degrees to rotate (0-360)
    
    Returns:
        Adjusted color in same format as input
    
    Example:
        >>> adjust_hue("#FF5733", 180)  # Complementary color
        '#33CCFF'
    """
    is_hex = isinstance(color, str)
    rgb = hex_to_rgb(color) if is_hex else color
    hsl = rgb_to_hsl(rgb)
    
    # Rotate hue
    new_h = (hsl[0] + degrees) % 360
    new_hsl = (new_h, hsl[1], hsl[2])
    new_rgb = hsl_to_rgb(new_hsl)
    
    return rgb_to_hex(new_rgb) if is_hex else new_rgb


# ============================================================================
# Color Palette Generation
# ============================================================================

def complementary_color(color: Union[RGB, HexColor]) -> Union[RGB, HexColor]:
    """
    Get the complementary color (opposite on color wheel).
    
    Args:
        color: RGB tuple or HEX string
    
    Returns:
        Complementary color in same format as input
    
    Example:
        >>> complementary_color("#FF5733")
        '#33CCFF'
    """
    return adjust_hue(color, 180)


def analogous_colors(color: Union[RGB, HexColor], count: int = 2) -> List[Union[RGB, HexColor]]:
    """
    Generate analogous colors (adjacent on color wheel).
    
    Args:
        color: Base color (RGB or HEX)
        count: Number of colors to generate (default: 2)
    
    Returns:
        List of analogous colors in same format as input
    
    Example:
        >>> analogous_colors("#FF5733", 2)
        ['#FF338C', '#FFA633']
    """
    is_hex = isinstance(color, str)
    colors = []
    
    # Generate colors at ±30 degrees
    step = 30
    for i in range(1, count + 1):
        # Counter-clockwise
        cc = adjust_hue(color, -step * i)
        colors.append(cc if is_hex else hex_to_rgb(cc) if isinstance(cc, str) else cc)
    
    for i in range(1, count + 1):
        # Clockwise
        cw = adjust_hue(color, step * i)
        colors.append(cw if is_hex else hex_to_rgb(cw) if isinstance(cw, str) else cw)
    
    return colors[:count] if count <= 2 else colors


def triadic_colors(color: Union[RGB, HexColor]) -> List[Union[RGB, HexColor]]:
    """
    Generate triadic color scheme (3 colors equally spaced).
    
    Args:
        color: Base color (RGB or HEX)
    
    Returns:
        List of 3 colors in same format as input
    
    Example:
        >>> triadic_colors("#FF5733")
        ['#FF5733', '#33FF57', '#5733FF']
    """
    is_hex = isinstance(color, str)
    
    c1 = color
    c2 = adjust_hue(color, 120)
    c3 = adjust_hue(color, 240)
    
    return [c if is_hex else hex_to_rgb(c) if isinstance(c, str) else c for c in [c1, c2, c3]]


def split_complementary(color: Union[RGB, HexColor]) -> List[Union[RGB, HexColor]]:
    """
    Generate split-complementary color scheme.
    
    Args:
        color: Base color (RGB or HEX)
    
    Returns:
        List of 3 colors in same format as input
    
    Example:
        >>> split_complementary("#FF5733")
        ['#FF5733', '#33FFA6', '#338CFF']
    """
    is_hex = isinstance(color, str)
    
    c1 = color
    c2 = adjust_hue(color, 150)
    c3 = adjust_hue(color, 210)
    
    return [c if is_hex else hex_to_rgb(c) if isinstance(c, str) else c for c in [c1, c2, c3]]


def tetradic_colors(color: Union[RGB, HexColor]) -> List[Union[RGB, HexColor]]:
    """
    Generate tetradic (rectangle) color scheme (4 colors).
    
    Args:
        color: Base color (RGB or HEX)
    
    Returns:
        List of 4 colors in same format as input
    
    Example:
        >>> tetradic_colors("#FF5733")
        ['#FF5733', '#CCFF33', '#33CCFF', '#6633FF']
    """
    is_hex = isinstance(color, str)
    
    c1 = color
    c2 = adjust_hue(color, 60)
    c3 = adjust_hue(color, 180)
    c4 = adjust_hue(color, 240)
    
    return [c if is_hex else hex_to_rgb(c) if isinstance(c, str) else c for c in [c1, c2, c3, c4]]


def monochromatic_colors(color: Union[RGB, HexColor], count: int = 4) -> List[Union[RGB, HexColor]]:
    """
    Generate monochromatic color scheme (variations in lightness).
    
    Args:
        color: Base color (RGB or HEX)
        count: Number of colors to generate
    
    Returns:
        List of monochromatic colors in same format as input
    
    Example:
        >>> monochromatic_colors("#FF5733", 4)
        ['#FF5733', '#FF7A5C', '#FF9C85', '#FFBFAE']
    """
    is_hex = isinstance(color, str)
    rgb = hex_to_rgb(color) if is_hex else color
    hsl = rgb_to_hsl(rgb)
    
    colors = [color]
    
    # Generate lighter variations
    for i in range(1, count):
        new_l = min(100, hsl[2] + i * 10)
        new_hsl = (hsl[0], hsl[1], new_l)
        new_rgb = hsl_to_rgb(new_hsl)
        new_color = rgb_to_hex(new_rgb) if is_hex else new_rgb
        colors.append(new_color)
    
    return colors


def generate_gradient(color1: Union[RGB, HexColor], 
                      color2: Union[RGB, HexColor], 
                      steps: int = 5) -> List[Union[RGB, HexColor]]:
    """
    Generate a gradient between two colors.
    
    Args:
        color1: Start color (RGB or HEX)
        color2: End color (RGB or HEX)
        steps: Number of steps in gradient
    
    Returns:
        List of colors forming the gradient
    
    Example:
        >>> generate_gradient("#FF0000", "#0000FF", 5)
        ['#FF0000', '#BF0040', '#800080', '#4000BF', '#0000FF']
    """
    is_hex = isinstance(color1, str)
    gradient = []
    
    for i in range(steps):
        ratio = i / (steps - 1) if steps > 1 else 0
        color = mix_colors(color1, color2, ratio)
        gradient.append(color)
    
    return gradient


# ============================================================================
# Color Accessibility Functions
# ============================================================================

def get_luminance(rgb: RGB) -> float:
    """
    Calculate relative luminance of a color (WCAG formula).
    
    Args:
        rgb: Tuple of (R, G, B) values (0-255)
    
    Returns:
        Relative luminance (0.0 to 1.0)
    
    Example:
        >>> get_luminance((255, 255, 255))
        1.0
        >>> get_luminance((0, 0, 0))
        0.0
    """
    def adjust(c: int) -> float:
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    r, g, b = [adjust(c) for c in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(color1: Union[RGB, HexColor], color2: Union[RGB, HexColor]) -> float:
    """
    Calculate contrast ratio between two colors (WCAG formula).
    
    Args:
        color1: First color (RGB or HEX)
        color2: Second color (RGB or HEX)
    
    Returns:
        Contrast ratio (1.0 to 21.0)
    
    Example:
        >>> contrast_ratio("#000000", "#FFFFFF")
        21.0
        >>> contrast_ratio("#FF5733", "#33CCFF")
        2.45
    """
    rgb1 = hex_to_rgb(color1) if isinstance(color1, str) else color1
    rgb2 = hex_to_rgb(color2) if isinstance(color2, str) else color2
    
    l1 = get_luminance(rgb1)
    l2 = get_luminance(rgb2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return round((lighter + 0.05) / (darker + 0.05), 2)


def is_wcag_aa(color1: Union[RGB, HexColor], 
               color2: Union[RGB, HexColor], 
               large_text: bool = False) -> bool:
    """
    Check if color combination meets WCAG AA standards.
    
    Args:
        color1: First color (RGB or HEX)
        color2: Second color (RGB or HEX)
        large_text: Whether this is for large text (18pt+ or 14pt bold)
    
    Returns:
        True if WCAG AA compliant
    
    Example:
        >>> is_wcag_aa("#000000", "#FFFFFF")
        True
        >>> is_wcag_aa("#FF5733", "#33CCFF")
        False
    """
    ratio = contrast_ratio(color1, color2)
    threshold = 3.0 if large_text else 4.5
    return ratio >= threshold


def is_wcag_aaa(color1: Union[RGB, HexColor], 
                color2: Union[RGB, HexColor], 
                large_text: bool = False) -> bool:
    """
    Check if color combination meets WCAG AAA standards.
    
    Args:
        color1: First color (RGB or HEX)
        color2: Second color (RGB or HEX)
        large_text: Whether this is for large text
    
    Returns:
        True if WCAG AAA compliant
    
    Example:
        >>> is_wcag_aaa("#000000", "#FFFFFF")
        True
    """
    ratio = contrast_ratio(color1, color2)
    threshold = 4.5 if large_text else 7.0
    return ratio >= threshold


def get_accessible_text_color(background: Union[RGB, HexColor]) -> HexColor:
    """
    Get an accessible text color (black or white) for a background.
    
    Args:
        background: Background color (RGB or HEX)
    
    Returns:
        "#000000" or "#FFFFFF" whichever has better contrast
    
    Example:
        >>> get_accessible_text_color("#FFFFFF")
        '#000000'
        >>> get_accessible_text_color("#000000")
        '#FFFFFF'
    """
    bg_rgb = hex_to_rgb(background) if isinstance(background, str) else background
    
    contrast_black = contrast_ratio(bg_rgb, (0, 0, 0))
    contrast_white = contrast_ratio(bg_rgb, (255, 255, 255))
    
    return "#000000" if contrast_black > contrast_white else "#FFFFFF"


# ============================================================================
# Color Naming and Identification
# ============================================================================

# Basic color name database
COLOR_NAMES: Dict[HexColor, str] = {
    "#000000": "Black",
    "#FFFFFF": "White",
    "#FF0000": "Red",
    "#00FF00": "Lime",
    "#0000FF": "Blue",
    "#FFFF00": "Yellow",
    "#00FFFF": "Cyan",
    "#FF00FF": "Magenta",
    "#808080": "Gray",
    "#800000": "Maroon",
    "#808000": "Olive",
    "#008000": "Green",
    "#800080": "Purple",
    "#008080": "Teal",
    "#000080": "Navy",
    "#FFA500": "Orange",
    "#FFC0CB": "Pink",
    "#A52A2A": "Brown",
    "#FFD700": "Gold",
    "#C0C0C0": "Silver",
    "#FF5733": "Orange Red",
    "#33CCFF": "Sky Blue",
    "#33FF57": "Spring Green",
    "#9370DB": "Medium Purple",
    "#FF6347": "Tomato",
    "#40E0D0": "Turquoise",
    "#EE82EE": "Violet",
    "#F5DEB3": "Wheat",
    "#FF4500": "Orange Red",
    "#7FFF00": "Chartreuse",
    "#DC143C": "Crimson",
    "#00CED1": "Dark Turquoise",
    "#9400D3": "Dark Violet",
    "#FF1493": "Deep Pink",
    "#00BFFF": "Deep Sky Blue",
    "#696969": "Dim Gray",
    "#1E90FF": "Dodger Blue",
    "#B22222": "Fire Brick",
    "#FFFAF0": "Floral White",
    "#228B22": "Forest Green",
    "#FF00FF": "Fuchsia",
    "#DCDCDC": "Gainsboro",
    "#F8F8FF": "Ghost White",
    "#FFD700": "Gold",
    "#DAA520": "Golden Rod",
    "#A9A9A9": "Dark Gray",
    "#006400": "Dark Green",
    "#BDB76B": "Dark Khaki",
    "#8B008B": "Dark Magenta",
    "#556B2F": "Dark Olive Green",
    "#FF8C00": "Dark Orange",
    "#9932CC": "Dark Orchid",
    "#8B0000": "Dark Red",
    "#E9967A": "Dark Salmon",
    "#8FBC8F": "Dark Sea Green",
    "#483D8B": "Dark Slate Blue",
    "#2F4F4F": "Dark Slate Gray",
    "#00CED1": "Dark Turquoise",
    "#9400D3": "Dark Violet",
}


def get_color_name(color: Union[RGB, HexColor], threshold: int = 50) -> Optional[str]:
    """
    Get the name of a color if it matches a known color.
    
    Args:
        color: Color to identify (RGB or HEX)
        threshold: Maximum distance to consider a match
    
    Returns:
        Color name or None if not found
    
    Example:
        >>> get_color_name("#FF0000")
        'Red'
    """
    hex_color = rgb_to_hex(color) if isinstance(color, tuple) else color.upper()
    
    # Exact match
    if hex_color in COLOR_NAMES:
        return COLOR_NAMES[hex_color]
    
    # Find closest match
    rgb = hex_to_rgb(hex_color)
    min_distance = threshold
    closest_name = None
    
    for known_hex, name in COLOR_NAMES.items():
        known_rgb = hex_to_rgb(known_hex)
        distance = color_distance(rgb, known_rgb)
        
        if distance < min_distance:
            min_distance = distance
            closest_name = name
    
    return closest_name


def color_distance(color1: RGB, color2: RGB) -> float:
    """
    Calculate the Euclidean distance between two colors.
    
    Args:
        color1: First RGB color
        color2: Second RGB color
    
    Returns:
        Distance value (lower = more similar)
    
    Example:
        >>> color_distance((255, 0, 0), (255, 10, 0))
        10.0
    """
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))


def is_similar_color(color1: Union[RGB, HexColor], 
                     color2: Union[RGB, HexColor], 
                     threshold: int = 30) -> bool:
    """
    Check if two colors are similar.
    
    Args:
        color1: First color (RGB or HEX)
        color2: Second color (RGB or HEX)
        threshold: Maximum distance to consider similar
    
    Returns:
        True if colors are similar
    
    Example:
        >>> is_similar_color("#FF0000", "#FF1000")
        True
    """
    rgb1 = hex_to_rgb(color1) if isinstance(color1, str) else color1
    rgb2 = hex_to_rgb(color2) if isinstance(color2, str) else color2
    
    return color_distance(rgb1, rgb2) <= threshold


# ============================================================================
# Utility Functions
# ============================================================================

def parse_color(color: Union[str, RGB]) -> RGB:
    """
    Parse a color string or tuple to RGB.
    
    Args:
        color: Color in various formats (HEX, RGB tuple, named color)
    
    Returns:
        RGB tuple
    
    Example:
        >>> parse_color("#FF5733")
        (255, 87, 51)
        >>> parse_color("Red")
        (255, 0, 0)
    """
    if isinstance(color, tuple) and len(color) == 3:
        return color
    
    if isinstance(color, str):
        # Try as hex
        if color.startswith('#') or re.match(r'^[0-9A-Fa-f]{6}$', color):
            return hex_to_rgb(color)
        
        # Try as named color
        for hex_val, name in COLOR_NAMES.items():
            if name.lower() == color.lower():
                return hex_to_rgb(hex_val)
    
    raise ValueError(f"Cannot parse color: {color}")


def format_color(rgb: RGB, format: str = "hex") -> Union[str, Tuple]:
    """
    Format a color in different formats.
    
    Args:
        rgb: RGB tuple
        format: Output format ("hex", "rgb", "hsl", "hsv", "cmyk")
    
    Returns:
        Formatted color string or tuple
    
    Example:
        >>> format_color((255, 87, 51), "hex")
        '#FF5733'
        >>> format_color((255, 87, 51), "rgb")
        'rgb(255, 87, 51)'
    """
    if format == "hex":
        return rgb_to_hex(rgb)
    elif format == "rgb":
        return f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"
    elif format == "rgba":
        return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 1.0)"
    elif format == "hsl":
        hsl = rgb_to_hsl(rgb)
        return f"hsl({hsl[0]}, {hsl[1]}%, {hsl[2]}%)"
    elif format == "hsv":
        hsv = rgb_to_hsv(rgb)
        return f"hsv({hsv[0]}, {hsv[1]}%, {hsv[2]}%)"
    elif format == "cmyk":
        cmyk = rgb_to_cmyk(rgb)
        return f"cmyk({cmyk[0]}%, {cmyk[1]}%, {cmyk[2]}%, {cmyk[3]}%)"
    else:
        raise ValueError(f"Unknown format: {format}")


def random_color() -> HexColor:
    """
    Generate a random color.
    
    Returns:
        Random HEX color
    
    Example:
        >>> random_color()  # e.g., '#A3F2B1'
    """
    import random
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return rgb_to_hex((r, g, b))


def is_valid_hex(color: str) -> bool:
    """
    Check if a string is a valid HEX color.
    
    Args:
        color: String to validate
    
    Returns:
        True if valid HEX color
    
    Example:
        >>> is_valid_hex("#FF5733")
        True
        >>> is_valid_hex("#F53")
        True
        >>> is_valid_hex("invalid")
        False
    """
    color = color.lstrip('#')
    return len(color) in [3, 6] and all(c in '0123456789ABCDEFabcdef' for c in color)


def is_valid_rgb(r: int, g: int, b: int) -> bool:
    """
    Check if RGB values are valid.
    
    Args:
        r: Red value (0-255)
        g: Green value (0-255)
        b: Blue value (0-255)
    
    Returns:
        True if valid RGB
    
    Example:
        >>> is_valid_rgb(255, 87, 51)
        True
        >>> is_valid_rgb(300, 0, 0)
        False
    """
    return all(0 <= c <= 255 for c in (r, g, b))


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Quick demo
    print("AllToolkit - Color Utilities Demo")
    print("=" * 40)
    
    # Color conversion
    hex_color = "#FF5733"
    print(f"\nOriginal: {hex_color}")
    print(f"RGB: {hex_to_rgb(hex_color)}")
    print(f"HSL: {hex_to_hsl(hex_color)}")
    print(f"HSV: {hex_to_hsv(hex_color)}")
    print(f"CMYK: {hex_to_cmyk(hex_color)}")
    
    # Color manipulation
    print(f"\nLightened: {lighten(hex_color, 0.2)}")
    print(f"Darkened: {darken(hex_color, 0.2)}")
    print(f"Inverted: {invert_color(hex_color)}")
    
    # Color palettes
    print(f"\nComplementary: {complementary_color(hex_color)}")
    print(f"Triadic: {triadic_colors(hex_color)}")
    print(f"Analogous: {analogous_colors(hex_color, 2)}")
    
    # Accessibility
    print(f"\nContrast with white: {contrast_ratio(hex_color, '#FFFFFF')}")
    print(f"WCAG AA (normal text): {is_wcag_aa(hex_color, '#FFFFFF')}")
    print(f"Accessible text color: {get_accessible_text_color(hex_color)}")
    
    # Color name
    print(f"\nColor name: {get_color_name(hex_color)}")
    
    # Gradient
    print(f"\nGradient to blue: {generate_gradient(hex_color, '#0000FF', 5)}")
