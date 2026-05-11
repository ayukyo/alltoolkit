#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Color Utilities Examples
======================================
Practical examples demonstrating color_utils module features.

Run: python examples/usage_examples.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    RGB, HSL,
    is_valid_hex, parse_hex, parse_color,
    rgb_to_hex, hex_to_rgb, rgb_to_hsl, hsl_to_rgb,
    rgb_to_hsv, hsv_to_rgb, rgb_to_cmyk, cmyk_to_rgb,
    rgb_to_lab, lab_to_rgb,
    get_luminance, get_contrast_ratio, get_wcag_level,
    is_light_color, get_color_temperature,
    lighten, darken, saturate, desaturate, grayscale, invert, complement,
    mix_colors, blend_colors,
    color_distance, color_distance_lab, are_colors_similar,
    get_complementary, get_analogous, get_triadic, get_split_complementary,
    get_tetradic,
    generate_shades, generate_tints, generate_tones,
    generate_gradient, generate_random_palette,
    get_color_info, get_color_name
)


def print_separator(title):
    """Print a section separator."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)


def example_validation():
    """Example: Color validation."""
    print_separator("1. Color Validation")
    
    # Validate HEX colors
    hex_colors = ['#FF0000', 'FF0000', '#F00', 'F00', 'invalid', '#FFFF']
    print("HEX validation:")
    for hex_color in hex_colors:
        valid = is_valid_hex(hex_color)
        print(f"  {hex_color!r}: {'Valid' if valid else 'Invalid'}")
    
    # Parse various color formats
    print("\nParsing colors:")
    colors = ['#FF0000', 'rgb(255, 0, 0)', (255, 0, 0), 'red']
    for color in colors:
        rgb = parse_color(color)
        print(f"  {color!r} -> RGB({rgb.r}, {rgb.g}, {rgb.b})")


def example_conversions():
    """Example: Color conversions."""
    print_separator("2. Color Format Conversions")
    
    # RGB <-> HEX
    print("RGB <-> HEX:")
    rgb = (255, 128, 0)
    hex_color = rgb_to_hex(*rgb)
    print(f"  RGB{rgb} -> {hex_color}")
    back = hex_to_rgb(hex_color)
    print(f"  {hex_color} -> RGB{back}")
    
    # RGB <-> HSL
    print("\nRGB <-> HSL:")
    rgb = (255, 0, 0)  # Red
    hsl = rgb_to_hsl(*rgb)
    print(f"  RGB{rgb} -> HSL({hsl[0]:.1f}°, {hsl[1]:.1f}%, {hsl[2]:.1f}%)")
    back = hsl_to_rgb(*hsl)
    print(f"  HSL({hsl[0]}°, {hsl[1]}%, {hsl[2]}%) -> RGB{back}")
    
    # RGB <-> HSV
    print("\nRGB <-> HSV:")
    hsv = rgb_to_hsv(*rgb)
    print(f"  RGB{rgb} -> HSV({hsv[0]:.1f}°, {hsv[1]:.1f}%, {hsv[2]:.1f}%)")
    
    # RGB <-> CMYK
    print("\nRGB <-> CMYK:")
    rgb = (255, 255, 255)
    cmyk = rgb_to_cmyk(*rgb)
    print(f"  RGB{rgb} -> CMYK({cmyk[0]:.1f}%, {cmyk[1]:.1f}%, {cmyk[2]:.1f}%, {cmyk[3]:.1f}%)")
    back = cmyk_to_rgb(*cmyk)
    print(f"  CMYK({cmyk[0]}%, {cmyk[1]}%, {cmyk[2]}%, {cmyk[3]}%) -> RGB{back}")
    
    # RGB <-> LAB
    print("\nRGB <-> LAB:")
    rgb = (255, 0, 0)
    lab = rgb_to_lab(*rgb)
    print(f"  RGB{rgb} -> LAB(L={lab[0]:.1f}, a={lab[1]:.1f}, b={lab[2]:.1f})")


def example_analysis():
    """Example: Color analysis."""
    print_separator("3. Color Analysis")
    
    # Luminance
    print("Luminance:")
    colors = ['#FFFFFF', '#000000', '#FF0000', '#00FF00', '#0000FF']
    for color in colors:
        lum = get_luminance(color)
        print(f"  {color}: {lum:.4f}")
    
    # Contrast ratio
    print("\nContrast ratios (for accessibility):")
    pairs = [
        ('#FFFFFF', '#000000'),  # Black on white
        ('#FFFFFF', '#777777'),  # Gray on white
        ('#FFFF00', '#000000'),  # Black on yellow
    ]
    for fg, bg in pairs:
        ratio = get_contrast_ratio(fg, bg)
        level = get_wcag_level(ratio)
        print(f"  {fg} on {bg}: {ratio:.2f}")
        print(f"    AA normal: {level['AA_normal']}, AAA normal: {level['AAA_normal']}")
    
    # Light/Dark detection
    print("\nLight/Dark detection:")
    colors = ['#FFFFFF', '#000000', '#CCCCCC', '#333333', '#FF5733']
    for color in colors:
        is_light = is_light_color(color)
        print(f"  {color}: {'Light' if is_light else 'Dark'}")
    
    # Color temperature
    print("\nColor temperature:")
    colors = ['#FF0000', '#FF8000', '#FFFF00', '#00FF00', '#00FFFF', '#0000FF', '#808080']
    for color in colors:
        temp = get_color_temperature(color)
        print(f"  {color}: {temp}")


def example_manipulation():
    """Example: Color manipulation."""
    print_separator("4. Color Manipulation")
    
    base_color = '#FF5733'
    print(f"Base color: {base_color}")
    
    # Lighten/Darken
    print("\nLighten/Darken:")
    lighter = lighten(base_color, 20)
    darker = darken(base_color, 20)
    print(f"  +20% lighter: {lighter.to_hex()}")
    print(f"  -20% darker: {darker.to_hex()}")
    
    # Saturate/Desaturate
    print("\nSaturate/Desaturate:")
    more_saturated = saturate(base_color, 30)
    less_saturated = desaturate(base_color, 30)
    print(f"  +30% saturation: {more_saturated.to_hex()}")
    print(f"  -30% saturation: {less_saturated.to_hex()}")
    
    # Grayscale
    print("\nGrayscale:")
    gray = grayscale(base_color)
    print(f"  Grayscale: {gray.to_hex()}")
    
    # Invert
    print("\nInvert:")
    inverted = invert(base_color)
    print(f"  Inverted: {inverted.to_hex()}")
    
    # Complement
    print("\nComplement:")
    comp = complement(base_color)
    print(f"  Complement: {comp.to_hex()}")
    
    # Mix colors
    print("\nMix colors:")
    color1 = '#FF0000'  # Red
    color2 = '#0000FF'  # Blue
    mixed_50 = mix_colors(color1, color2, 0.5)  # Equal mix
    mixed_75 = mix_colors(color1, color2, 0.75)  # More red
    print(f"  {color1} + {color2} (50/50): {mixed_50.to_hex()}")
    print(f"  {color1} + {color2} (75/25): {mixed_75.to_hex()}")


def example_harmony():
    """Example: Color harmony."""
    print_separator("5. Color Harmony")
    
    base_color = '#FF5733'
    print(f"Base color: {base_color}")
    
    # Complementary
    print("\nComplementary:")
    comp = get_complementary(base_color)
    print(f"  Complement: {comp.to_hex()}")
    
    # Analogous
    print("\nAnalogous:")
    analogous = get_analogous(base_color)
    print(f"  Analogous 1: {analogous[0].to_hex()}")
    print(f"  Analogous 2: {analogous[1].to_hex()}")
    
    # Triadic
    print("\nTriadic:")
    triadic = get_triadic(base_color)
    print(f"  Triadic 1: {triadic[0].to_hex()}")
    print(f"  Triadic 2: {triadic[1].to_hex()}")
    
    # Split-complementary
    print("\nSplit-complementary:")
    split = get_split_complementary(base_color)
    print(f"  Split 1: {split[0].to_hex()}")
    print(f"  Split 2: {split[1].to_hex()}")
    
    # Tetradic
    print("\nTetradic:")
    tetradic = get_tetradic(base_color)
    for i, color in enumerate(tetradic):
        print(f"  Tetradic {i+1}: {color.to_hex()}")


def example_distance():
    """Example: Color distance."""
    print_separator("6. Color Distance & Similarity")
    
    # RGB distance
    print("RGB distance:")
    pairs = [
        ('#FF0000', '#FF0000'),  # Same
        ('#FF0000', '#FF0101'),  # Very similar
        ('#FF0000', '#00FF00'),  # Very different
    ]
    for c1, c2 in pairs:
        dist = color_distance(c1, c2)
        print(f"  {c1} <-> {c2}: {dist:.2f}")
    
    # LAB distance (perceptual)
    print("\nLAB distance (perceptual):")
    for c1, c2 in pairs:
        dist = color_distance_lab(c1, c2)
        print(f"  {c1} <-> {c2}: {dist:.2f}")
    
    # Similarity check
    print("\nSimilarity check:")
    similar_pairs = [
        ('#FF0000', '#FF0101'),
        ('#FF0000', '#00FF00'),
        ('#FF0000', '#E60000'),
    ]
    for c1, c2 in similar_pairs:
        is_similar = are_colors_similar(c1, c2, threshold=10)
        print(f"  {c1} vs {c2}: {'Similar' if is_similar else 'Different'}")


def example_palettes():
    """Example: Palette generation."""
    print_separator("7. Palette Generation")
    
    base_color = '#FF5733'
    
    # Shades
    print("Shades (darker):")
    shades = generate_shades(base_color, 5)
    for i, shade in enumerate(shades):
        print(f"  Shade {i+1}: {shade.to_hex()}")
    
    # Tints
    print("\nTints (lighter):")
    tints = generate_tints(base_color, 5)
    for i, tint in enumerate(tints):
        print(f"  Tint {i+1}: {tint.to_hex()}")
    
    # Tones
    print("\nTones (mixed with gray):")
    tones = generate_tones(base_color, 5)
    for i, tone in enumerate(tones):
        print(f"  Tone {i+1}: {tone.to_hex()}")
    
    # Gradient
    print("\nGradient from red to blue:")
    gradient = generate_gradient('#FF0000', '#0000FF', 5)
    for i, color in enumerate(gradient):
        print(f"  Step {i+1}: {color.to_hex()}")
    
    # Random palette
    print("\nRandom harmonious palette:")
    random_pal = generate_random_palette(5, harmonize=True)
    for i, color in enumerate(random_pal):
        print(f"  Color {i+1}: {color.to_hex()}")


def example_comprehensive_info():
    """Example: Comprehensive color info."""
    print_separator("8. Comprehensive Color Info")
    
    colors = ['#FF5733', '#00FF88', '#8844FF']
    
    for color in colors:
        info = get_color_info(color)
        print(f"\nColor: {color}")
        print(f"  HEX: {info.hex}")
        print(f"  RGB: ({info.rgb.r}, {info.rgb.g}, {info.rgb.b})")
        print(f"  HSL: H={info.hsl.h:.1f}°, S={info.hsl.s:.1f}%, L={info.hsl.l:.1f}%")
        print(f"  HSV: H={info.hsv[0]:.1f}°, S={info.hsv[1]:.1f}%, V={info.hsv[2]:.1f}%")
        print(f"  CMYK: C={info.cmyk[0]:.1f}%, M={info.cmyk[1]:.1f}%, Y={info.cmyk[2]:.1f}%, K={info.cmyk[3]:.1f}%")
        print(f"  LAB: L={info.lab[0]:.1f}, a={info.lab[1]:.1f}, b={info.lab[2]:.1f}")
        print(f"  Luminance: {info.luminance:.4f}")
        print(f"  Temperature: {info.temperature}")
        print(f"  Closest named color: {info.name}")


def example_practical_use_cases():
    """Example: Practical use cases."""
    print_separator("9. Practical Use Cases")
    
    # Use case 1: Find best text color for accessibility
    print("Use case 1: Find accessible text colors")
    bg_color = '#3498DB'  # Blue background
    ratio = get_contrast_ratio(bg_color, '#FFFFFF')
    print(f"  White on blue: contrast = {ratio:.2f}")
    level = get_wcag_level(ratio)
    print(f"    AA normal: {level['AA_normal']}")
    
    # Use case 2: Generate button color variations
    print("\nUse case 2: Generate button color palette")
    button_color = '#FF5733'
    hover = lighten(button_color, 10)
    active = darken(button_color, 10)
    disabled = grayscale(button_color)
    print(f"  Normal: {button_color}")
    print(f"  Hover: {hover.to_hex()}")
    print(f"  Active: {active.to_hex()}")
    print(f"  Disabled: {disabled.to_hex()}")
    
    # Use case 3: Create brand color scheme
    print("\nUse case 3: Create brand color scheme")
    brand_primary = '#FF5733'
    secondary = complement(brand_primary)
    analogous = get_analogous(brand_primary)
    print(f"  Primary: {brand_primary}")
    print(f"  Secondary (complement): {secondary.to_hex()}")
    print(f"  Accent 1: {analogous[0].to_hex()}")
    print(f"  Accent 2: {analogous[1].to_hex()}")
    
    # Use case 4: Validate user input
    print("\nUse case 4: Validate color input")
    user_inputs = ['#FF0000', 'FF0000', '#F00', 'rgb(255,0,0)', 'red', 'invalid']
    for input_color in user_inputs:
        try:
            rgb = parse_color(input_color)
            print(f"  {input_color!r}: Valid -> {rgb.to_hex()}")
        except ValueError:
            print(f"  {input_color!r}: Invalid")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print(" AllToolkit - Color Utilities Examples")
    print("="*60)
    
    example_validation()
    example_conversions()
    example_analysis()
    example_manipulation()
    example_harmony()
    example_distance()
    example_palettes()
    example_comprehensive_info()
    example_practical_use_cases()
    
    print("\n" + "="*60)
    print(" Examples completed!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()