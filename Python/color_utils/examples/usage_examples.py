#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Color Utilities Usage Examples
============================================
Comprehensive examples demonstrating color_utils module capabilities.

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os

# Add module directory to path
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module_dir)

# Import directly from mod.py
import importlib.util
spec = importlib.util.spec_from_file_location("color_utils_mod", 
    os.path.join(module_dir, "mod.py"))
color_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(color_utils)

# Extract functions
Color = color_utils.Color
parse_color = color_utils.parse_color
rgb_to_hex = color_utils.rgb_to_hex
hex_to_rgb = color_utils.hex_to_rgb
rgb_to_hsl = color_utils.rgb_to_hsl
hsl_to_rgb = color_utils.hsl_to_rgb
rgb_to_hsv = color_utils.rgb_to_hsv
hsv_to_rgb = color_utils.hsv_to_rgb
rgb_to_cmyk = color_utils.rgb_to_cmyk
cmyk_to_rgb = color_utils.cmyk_to_rgb
rgb_to_lab = color_utils.rgb_to_lab
lab_to_rgb = color_utils.lab_to_rgb
lighten = color_utils.lighten
darken = color_utils.darken
saturate = color_utils.saturate
desaturate = color_utils.desaturate
grayscale = color_utils.grayscale
invert = color_utils.invert
rotate_hue = color_utils.rotate_hue
complement = color_utils.complement
mix = color_utils.mix
blend_multiply = color_utils.blend_multiply
blend_screen = color_utils.blend_screen
blend_overlay = color_utils.blend_overlay
color_distance = color_utils.color_distance
color_distance_lab = color_utils.color_distance_lab
calculate_luminance = color_utils.calculate_luminance
contrast_ratio = color_utils.contrast_ratio
wcag_rating = color_utils.wcag_rating
complementary_palette = color_utils.complementary_palette
analogous_palette = color_utils.analogous_palette
triadic_palette = color_utils.triadic_palette
split_complementary_palette = color_utils.split_complementary_palette
tetradic_palette = color_utils.tetradic_palette
random_color = color_utils.random_color
random_palette = color_utils.random_palette
gradient_palette = color_utils.gradient_palette
monochromatic_palette = color_utils.monochromatic_palette
shades_palette = color_utils.shades_palette
tints_palette = color_utils.tints_palette
harmonious_palette = color_utils.harmonious_palette
get_accessible_text_color = color_utils.get_accessible_text_color
find_accessible_colors = color_utils.find_accessible_colors
is_valid_hex = color_utils.is_valid_hex
rgb_to_int = color_utils.rgb_to_int
int_to_rgb = color_utils.int_to_rgb
interpolate_color = color_utils.interpolate_color
temperature_to_rgb = color_utils.temperature_to_rgb
css_gradient = color_utils.css_gradient
create_color = color_utils.create_color
create_color_from_hex = color_utils.create_color_from_hex
create_color_from_name = color_utils.create_color_from_name
rgb_to_name = color_utils.rgb_to_name
name_to_rgb = color_utils.name_to_rgb
get_color_brightness = color_utils.get_color_brightness


def example_01_basic_parsing():
    """Example 1: Basic color parsing."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Color Parsing")
    print("=" * 60)
    
    # Parse from various formats
    formats = [
        "#FF0000",           # HEX with hash
        "FF0000",            # HEX without hash
        "#F00",              # Short HEX
        "rgb(255, 0, 0)",    # RGB notation
        "rgba(255, 0, 0, 0.5)",  # RGBA notation
        "hsl(0, 100%, 50%)",  # HSL notation
        "red",               # Named color
        "cornflowerblue",    # Extended named color
    ]
    
    for fmt in formats:
        try:
            color = parse_color(fmt)
            print(f"  {fmt:25} → {color}")
        except ValueError as e:
            print(f"  {fmt:25} → Error: {e}")


def example_02_color_class():
    """Example 2: Color class usage."""
    print("\n" + "=" * 60)
    print("Example 2: Color Class Usage")
    print("=" * 60)
    
    # Create Color objects
    red = create_color(255, 0, 0)
    green = create_color(0, 255, 0)
    blue = create_color(0, 0, 255)
    purple = create_color(128, 0, 128, 0.8)  # With alpha
    
    print(f"  Red:      {red}")
    print(f"    HEX:    {red.hex_with_hash}")
    print(f"    HSL:    H={red.hsl[0]:.1f}° S={red.hsl[1]:.1f}% L={red.hsl[2]:.1f}%")
    print(f"    HSV:    H={red.hsv[0]:.1f}° S={red.hsv[1]:.1f}% V={red.hsv[2]:.1f}%")
    print(f"    CMYK:   C={red.cmyk[0]:.1f}% M={red.cmyk[1]:.1f}% Y={red.cmyk[2]:.1f}% K={red.cmyk[3]:.1f}%")
    print(f"    Luminance: {red.luminance:.4f}")
    print(f"    Is light: {red.is_light}")
    
    print(f"\n  Green:    {green}")
    print(f"  Blue:     {blue}")
    print(f"  Purple:   {purple} (with alpha={purple.a})")


def example_03_format_conversions():
    """Example 3: Format conversion examples."""
    print("\n" + "=" * 60)
    print("Example 3: Format Conversions")
    print("=" * 60)
    
    # RGB ↔ HEX
    rgb = (255, 128, 64)
    hex_str = rgb_to_hex(rgb)
    rgb_back = hex_to_rgb(hex_str)
    print(f"  RGB → HEX: {rgb} → {hex_str} → {rgb_back}")
    
    # RGB ↔ HSL
    rgb = (255, 0, 0)
    hsl = rgb_to_hsl(rgb)
    rgb_back = hsl_to_rgb(hsl)
    print(f"  RGB → HSL: {rgb} → H={hsl[0]:.1f}° S={hsl[1]:.1f}% L={hsl[2]:.1f}% → {rgb_back}")
    
    # RGB ↔ HSV
    hsv = rgb_to_hsv(rgb)
    rgb_back = hsv_to_rgb(hsv)
    print(f"  RGB → HSV: {rgb} → H={hsv[0]:.1f}° S={hsv[1]:.1f}% V={hsv[2]:.1f}% → {rgb_back}")
    
    # RGB ↔ CMYK
    rgb = (0, 0, 0)  # Black
    cmyk = rgb_to_cmyk(rgb)
    rgb_back = cmyk_to_rgb(cmyk)
    print(f"  RGB → CMYK: {rgb} → C={cmyk[0]:.1f}% M={cmyk[1]:.1f}% Y={cmyk[2]:.1f}% K={cmyk[3]:.1f}% → {rgb_back}")
    
    # RGB ↔ LAB
    rgb = (255, 255, 255)  # White
    lab = rgb_to_lab(rgb)
    rgb_back = lab_to_rgb(lab)
    print(f"  RGB → LAB: {rgb} → L={lab[0]:.1f} a={lab[1]:.1f} b={lab[2]:.1f} → {rgb_back}")


def example_04_color_manipulation():
    """Example 4: Color manipulation."""
    print("\n" + "=" * 60)
    print("Example 4: Color Manipulation")
    print("=" * 60)
    
    base_color = (200, 100, 50)
    print(f"  Base color: {rgb_to_hex(base_color)}")
    
    # Lighten and darken
    lighter = lighten(base_color, 30)
    darker = darken(base_color, 30)
    print(f"  Lightened by 30%: {rgb_to_hex(lighter)}")
    print(f"  Darkened by 30%:  {rgb_to_hex(darker)}")
    
    # Saturate and desaturate
    saturated = saturate(base_color, 50)
    desaturated = desaturate(base_color, 50)
    print(f"  Saturated by 50%:   {rgb_to_hex(saturated)}")
    print(f"  Desaturated by 50%: {rgb_to_hex(desaturated)}")
    
    # Grayscale
    gray = grayscale(base_color)
    print(f"  Grayscale: {rgb_to_hex(gray)}")
    
    # Invert
    inverted = invert(base_color)
    print(f"  Inverted:  {rgb_to_hex(inverted)}")
    
    # Complement
    comp = complement(base_color)
    print(f"  Complement: {rgb_to_hex(comp)}")
    
    # Rotate hue
    rotated_90 = rotate_hue(base_color, 90)
    rotated_180 = rotate_hue(base_color, 180)
    rotated_270 = rotate_hue(base_color, 270)
    print(f"  Hue +90°:  {rgb_to_hex(rotated_90)}")
    print(f"  Hue +180°: {rgb_to_hex(rotated_180)}")
    print(f"  Hue +270°: {rgb_to_hex(rotated_270)}")


def example_05_color_mixing():
    """Example 5: Color mixing and blending."""
    print("\n" + "=" * 60)
    print("Example 5: Color Mixing and Blending")
    print("=" * 60)
    
    red = (255, 0, 0)
    blue = (0, 0, 255)
    gray = (128, 128, 128)
    
    # Simple mixing
    print(f"  Colors: Red={rgb_to_hex(red)}, Blue={rgb_to_hex(blue)}")
    
    mix_25 = mix(red, blue, 0.25)
    mix_50 = mix(red, blue, 0.50)
    mix_75 = mix(red, blue, 0.75)
    print(f"  Mix 25% (more red):   {rgb_to_hex(mix_25)}")
    print(f"  Mix 50% (equal):      {rgb_to_hex(mix_50)}")
    print(f"  Mix 75% (more blue):  {rgb_to_hex(mix_75)}")
    
    # Blend modes
    print(f"\n  Blend modes (base={rgb_to_hex(gray)}, overlay={rgb_to_hex(red)}):")
    multiply = blend_multiply(gray, red)
    screen = blend_screen(gray, red)
    overlay = blend_overlay(gray, red)
    print(f"  Multiply: {rgb_to_hex(multiply)}")
    print(f"  Screen:   {rgb_to_hex(screen)}")
    print(f"  Overlay:  {rgb_to_hex(overlay)}")


def example_06_color_comparison():
    """Example 6: Color comparison and contrast."""
    print("\n" + "=" * 60)
    print("Example 6: Color Comparison and Contrast")
    print("=" * 60)
    
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (0, 255, 255),  # Cyan
    ]
    
    print("  Color luminances:")
    for c in colors:
        lum = calculate_luminance(c)
        print(f"    {rgb_to_hex(c):7} → luminance = {lum:.4f}")
    
    print("\n  Contrast ratios:")
    pairs = [
        ((0, 0, 0), (255, 255, 255)),      # Black/White
        ((255, 255, 255), (200, 200, 200)), # White/Light gray
        ((0, 0, 0), (50, 50, 50)),          # Black/Dark gray
        ((255, 0, 0), (255, 255, 255)),     # Red/White
        ((255, 0, 0), (0, 255, 255)),       # Red/Cyan
    ]
    for c1, c2 in pairs:
        ratio = contrast_ratio(c1, c2)
        rating = wcag_rating(ratio)
        print(f"    {rgb_to_hex(c1)} / {rgb_to_hex(c2)} → ratio={ratio:.2f}, rating={rating}")
    
    print("\n  Color distances:")
    print(f"    RGB distance (red to blue): {color_distance((255, 0, 0), (0, 0, 255)):.2f}")
    print(f"    LAB distance (red to blue): {color_distance_lab((255, 0, 0), (0, 0, 255)):.2f}")


def example_07_color_harmony():
    """Example 7: Color harmony palettes."""
    print("\n" + "=" * 60)
    print("Example 7: Color Harmony Palettes")
    print("=" * 60)
    
    base = (255, 128, 0)  # Orange
    print(f"  Base color: {rgb_to_hex(base)} (orange)")
    
    # Complementary
    comp = complementary_palette(base)
    print(f"  Complementary:     {', '.join(rgb_to_hex(c) for c in comp)}")
    
    # Analogous
    analog = analogous_palette(base)
    print(f"  Analogous:         {', '.join(rgb_to_hex(c) for c in analog)}")
    
    # Triadic
    triadic = triadic_palette(base)
    print(f"  Triadic:           {', '.join(rgb_to_hex(c) for c in triadic)}")
    
    # Split-complementary
    split = split_complementary_palette(base)
    print(f"  Split-complement:  {', '.join(rgb_to_hex(c) for c in split)}")
    
    # Tetradic
    tetrad = tetradic_palette(base)
    print(f"  Tetradic:          {', '.join(rgb_to_hex(c) for c in tetrad)}")


def example_08_palette_generation():
    """Example 8: Palette generation."""
    print("\n" + "=" * 60)
    print("Example 8: Palette Generation")
    print("=" * 60)
    
    base = (100, 150, 200)
    print(f"  Base color: {rgb_to_hex(base)}")
    
    # Monochromatic
    mono = monochromatic_palette(base, 7)
    print(f"  Monochromatic (7): {', '.join(rgb_to_hex(c) for c in mono)}")
    
    # Shades (darker)
    shades = shades_palette(base, 5)
    print(f"  Shades (5):        {', '.join(rgb_to_hex(c) for c in shades)}")
    
    # Tints (lighter)
    tints = tints_palette(base, 5)
    print(f"  Tints (5):         {', '.join(rgb_to_hex(c) for c in tints)}")
    
    # Gradient
    gradient = gradient_palette((255, 0, 0), (0, 0, 255), 7)
    print(f"  Gradient (red→blue, 7): {', '.join(rgb_to_hex(c) for c in gradient)}")
    
    # Random palette
    random = random_palette(5)
    print(f"  Random (5):        {', '.join(rgb_to_hex(c) for c in random)}")


def example_09_accessibility():
    """Example 9: Accessibility helpers."""
    print("\n" + "=" * 60)
    print("Example 9: Accessibility Helpers")
    print("=" * 60)
    
    backgrounds = [
        (0, 0, 0),          # Black
        (255, 255, 255),    # White
        (50, 50, 50),       # Dark gray
        (200, 200, 200),    # Light gray
        (100, 149, 237),    # Cornflower blue
        (255, 0, 0),        # Red
    ]
    
    print("  Accessible text colors for backgrounds:")
    for bg in backgrounds:
        text = get_accessible_text_color(bg)
        ratio = contrast_ratio(bg, text)
        rating = wcag_rating(ratio)
        print(f"    BG: {rgb_to_hex(bg):7} → Text: {rgb_to_hex(text):7} (ratio={ratio:.2f}, {rating})")
    
    # Find accessible colors
    print("\n  Accessible colors for gray background (128, 128, 128):")
    accessible = find_accessible_colors((128, 128, 128), 8)
    for c in accessible:
        ratio = contrast_ratio((128, 128, 128), c)
        print(f"    {rgb_to_hex(c):7} → ratio={ratio:.2f}")


def example_10_temperature_colors():
    """Example 10: Color temperature."""
    print("\n" + "=" * 60)
    print("Example 10: Color Temperature (Kelvin)")
    print("=" * 60)
    
    temperatures = [
        1000,   # Candle flame
        2700,   # Warm white light
        3000,   # Incandescent bulb
        4000,   # Cool white fluorescent
        5000,   # Daylight
        6500,   # Daylight (overcast)
        8000,   # Blue sky
        10000,  # Clear blue sky
    ]
    
    print("  Color temperatures:")
    for temp in temperatures:
        rgb = temperature_to_rgb(temp)
        print(f"    {temp:5}K → {rgb_to_hex(rgb)}")
    
    # Gradient from warm to cool
    warm_cool = gradient_palette(
        temperature_to_rgb(2700),
        temperature_to_rgb(6500),
        5
    )
    print(f"\n  Warm (2700K) to Cool (6500K) gradient:")
    print(f"    {', '.join(rgb_to_hex(c) for c in warm_cool)}")


def example_11_css_gradient():
    """Example 11: CSS gradient generation."""
    print("\n" + "=" * 60)
    print("Example 11: CSS Gradient Generation")
    print("=" * 60)
    
    # Simple horizontal gradient
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    gradient = css_gradient(colors, 'to right')
    print(f"  Horizontal gradient:")
    print(f"    {gradient}")
    
    # Vertical gradient
    gradient = css_gradient(colors, 'to bottom')
    print(f"\n  Vertical gradient:")
    print(f"    {gradient}")
    
    # Rainbow gradient
    rainbow = [
        (255, 0, 0),      # Red
        (255, 127, 0),    # Orange
        (255, 255, 0),    # Yellow
        (0, 255, 0),      # Green
        (0, 0, 255),      # Blue
        (75, 0, 130),     # Indigo
        (148, 0, 211),    # Violet
    ]
    gradient = css_gradient(rainbow, 'to right')
    print(f"\n  Rainbow gradient (7 colors):")
    print(f"    {gradient}")


def example_12_utility_functions():
    """Example 12: Utility functions."""
    print("\n" + "=" * 60)
    print("Example 12: Utility Functions")
    print("=" * 60)
    
    # HEX validation
    test_hex = ["#FF0000", "FF0000", "#F00", "FFF", "FF", "invalid"]
    print("  HEX validation:")
    for h in test_hex:
        valid = is_valid_hex(h)
        print(f"    '{h}' → {valid}")
    
    # RGB ↔ Integer
    rgb = (255, 128, 64)
    int_val = rgb_to_int(rgb)
    rgb_back = int_to_rgb(int_val)
    print(f"\n  RGB ↔ Integer:")
    print(f"    {rgb} → {int_val} → {rgb_back}")
    
    # Interpolation
    start = (255, 0, 0)
    end = (0, 0, 255)
    print(f"\n  Interpolation (red → blue):")
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        interp = interpolate_color(start, end, t)
        print(f"    t={t:.2f} → {rgb_to_hex(interp)}")
    
    # Brightness
    print(f"\n  Color brightness:")
    for c in [(255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]:
        brightness = get_color_brightness(c)
        print(f"    {rgb_to_hex(c):7} → brightness = {brightness:.1f}")


def example_13_named_colors():
    """Example 13: Named color lookup."""
    print("\n" + "=" * 60)
    print("Example 13: Named Color Lookup")
    print("=" * 60)
    
    # Name to RGB
    names = ['red', 'cornflowerblue', 'rebeccapurple', 'chartreuse', 'hotpink']
    print("  Name → RGB:")
    for name in names:
        rgb = name_to_rgb(name)
        if rgb:
            print(f"    {name:18} → {rgb_to_hex(rgb)}")
    
    # RGB to Name (closest match)
    print("\n  RGB → Name (closest match):")
    test_colors = [
        (255, 0, 0),       # Exact red
        (0, 0, 255),       # Exact blue
        (100, 149, 237),   # Exact cornflowerblue
        (250, 128, 114),   # Close to salmon
    ]
    for rgb in test_colors:
        name = rgb_to_name(rgb)
        print(f"    {rgb_to_hex(rgb):7} → {name}")


def example_14_practical_application():
    """Example 14: Practical application - UI theme generation."""
    print("\n" + "=" * 60)
    print("Example 14: Practical Application - UI Theme")
    print("=" * 60)
    
    # Generate a UI theme from a primary color
    primary = (75, 130, 195)  # Blue-ish
    
    print(f"  Primary: {rgb_to_hex(primary)}")
    
    # Primary variations
    primary_light = lighten(primary, 15)
    primary_dark = darken(primary, 15)
    print(f"    Light variant: {rgb_to_hex(primary_light)}")
    print(f"    Dark variant:  {rgb_to_hex(primary_dark)}")
    
    # Secondary (complementary)
    secondary = complement(primary)
    secondary_light = lighten(secondary, 15)
    secondary_dark = darken(secondary, 15)
    print(f"\n  Secondary (complement): {rgb_to_hex(secondary)}")
    print(f"    Light variant: {rgb_to_hex(secondary_light)}")
    print(f"    Dark variant:  {rgb_to_hex(secondary_dark)}")
    
    # Background colors
    bg_light = (250, 250, 250)
    bg_dark = darken(bg_light, 95)
    print(f"\n  Backgrounds:")
    print(f"    Light: {rgb_to_hex(bg_light)}")
    print(f"    Dark:  {rgb_to_hex(bg_dark)}")
    
    # Text colors (accessible)
    text_on_light = get_accessible_text_color(bg_light)
    text_on_dark = get_accessible_text_color(bg_dark)
    print(f"\n  Text colors:")
    print(f"    On light: {rgb_to_hex(text_on_light)}")
    print(f"    On dark:  {rgb_to_hex(text_on_dark)}")
    
    # Accent colors (analogous)
    accents = analogous_palette(primary)
    print(f"\n  Accent colors (analogous):")
    for c in accents:
        print(f"    {rgb_to_hex(c)}")
    
    # Status colors
    success = (46, 139, 87)    # SeaGreen
    warning = (255, 165, 0)    # Orange
    error = (220, 20, 60)      # Crimson
    info = (30, 144, 255)      # DodgerBlue
    print(f"\n  Status colors:")
    print(f"    Success: {rgb_to_hex(success)}")
    print(f"    Warning: {rgb_to_hex(warning)}")
    print(f"    Error:   {rgb_to_hex(error)}")
    print(f"    Info:    {rgb_to_hex(info)}")
    
    # Verify contrast
    print(f"\n  Contrast verification:")
    print(f"    Primary on light: {contrast_ratio(primary, bg_light):.2f} ({wcag_rating(contrast_ratio(primary, bg_light))})")
    print(f"    Primary on dark:  {contrast_ratio(primary, bg_dark):.2f} ({wcag_rating(contrast_ratio(primary, bg_dark))})")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("AllToolkit - Color Utilities Examples")
    print("=" * 60)
    
    example_01_basic_parsing()
    example_02_color_class()
    example_03_format_conversions()
    example_04_color_manipulation()
    example_05_color_mixing()
    example_06_color_comparison()
    example_07_color_harmony()
    example_08_palette_generation()
    example_09_accessibility()
    example_10_temperature_colors()
    example_11_css_gradient()
    example_12_utility_functions()
    example_13_named_colors()
    example_14_practical_application()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()