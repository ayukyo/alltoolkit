#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Color Utilities Usage Examples
=============================================
Practical examples demonstrating the color_utils module capabilities.

Run with: python usage_examples.py
"""

import sys
import os

# Import directly from the module file
mod_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mod.py')
import importlib.util
spec = importlib.util.spec_from_file_location("color_utils_mod", mod_path)
color_utils_mod = importlib.util.module_from_spec(spec)
sys.modules['color_utils_mod'] = color_utils_mod
spec.loader.exec_module(color_utils_mod)

# Import functions
RGB = color_utils_mod.RGB
HSL = color_utils_mod.HSL
HSV = color_utils_mod.HSV
CMYK = color_utils_mod.CMYK
parse_color = color_utils_mod.parse_color
parse_hex = color_utils_mod.parse_hex
parse_rgb = color_utils_mod.parse_rgb
parse_hsl = color_utils_mod.parse_hsl
rgb_to_hex = color_utils_mod.rgb_to_hex
rgb_to_hsl = color_utils_mod.rgb_to_hsl
hsl_to_rgb = color_utils_mod.hsl_to_rgb
rgb_to_hsv = color_utils_mod.rgb_to_hsv
hsv_to_rgb = color_utils_mod.hsv_to_rgb
rgb_to_cmyk = color_utils_mod.rgb_to_cmyk
cmyk_to_rgb = color_utils_mod.cmyk_to_rgb
lighten = color_utils_mod.lighten
darken = color_utils_mod.darken
saturate = color_utils_mod.saturate
desaturate = color_utils_mod.desaturate
grayscale = color_utils_mod.grayscale
invert = color_utils_mod.invert
complement = color_utils_mod.complement
mix = color_utils_mod.mix
blend = color_utils_mod.blend
analogous = color_utils_mod.analogous
triadic = color_utils_mod.triadic
split_complement = color_utils_mod.split_complement
tetradic = color_utils_mod.tetradic
monochromatic = color_utils_mod.monochromatic
luminance = color_utils_mod.luminance
contrast_ratio = color_utils_mod.contrast_ratio
wcag_rating = color_utils_mod.wcag_rating
brightness = color_utils_mod.brightness
is_light = color_utils_mod.is_light
is_dark = color_utils_mod.is_dark
text_color_for_bg = color_utils_mod.text_color_for_bg
color_distance = color_utils_mod.color_distance
closest_color = color_utils_mod.closest_color
gradient = color_utils_mod.gradient
multi_gradient = color_utils_mod.multi_gradient
random_color = color_utils_mod.random_color
random_hue = color_utils_mod.random_hue
random_pastel = color_utils_mod.random_pastel
color_name_to_rgb = color_utils_mod.color_name_to_rgb
rgb_to_color_name = color_utils_mod.rgb_to_color_name


def example_color_parsing():
    """Demonstrate color parsing from various formats."""
    print("\n" + "="*60)
    print("颜色解析示例 (Color Parsing Examples)")
    print("="*60)
    
    # Hex parsing
    print("\n1. Hex 格式解析:")
    colors = ['#ff0000', '#f00', '#ff000080', '00ff00']
    for hex_str in colors:
        rgb = parse_hex(hex_str)
        print(f"   {hex_str} → {rgb}")
    
    # RGB string parsing
    print("\n2. RGB/RGBA 字符串解析:")
    rgb_strings = ['rgb(255, 0, 0)', 'rgba(255, 0, 0, 0.5)', 'rgb( 128, 64, 192 )']
    for rgb_str in rgb_strings:
        rgb = parse_rgb(rgb_str)
        print(f"   {rgb_str} → {rgb}")
    
    # HSL string parsing
    print("\n3. HSL 字符串解析:")
    hsl_strings = ['hsl(0, 100%, 50%)', 'hsl(180, 50%, 75%)']
    for hsl_str in hsl_strings:
        hsl = parse_hsl(hsl_str)
        rgb = hsl.to_rgb()
        print(f"   {hsl_str} → {hsl} → RGB: {rgb.to_hex()}")
    
    # Named color parsing
    print("\n4. CSS 颜色名称解析:")
    named_colors = ['red', 'coral', 'aliceblue', 'rebeccapurple']
    for name in named_colors:
        rgb = color_name_to_rgb(name)
        print(f"   {name} → {rgb.to_hex()}")
    
    # Universal parse_color
    print("\n5. 通用颜色解析 (parse_color):")
    any_format = ['#ff0000', 'rgb(0, 255, 0)', 'hsl(240, 100%, 50%)', 'blue']
    for color in any_format:
        rgb = parse_color(color)
        print(f"   {color} → {rgb.to_hex()}")


def example_color_conversion():
    """Demonstrate color format conversions."""
    print("\n" + "="*60)
    print("颜色转换示例 (Color Conversion Examples)")
    print("="*60)
    
    # RGB ↔ Hex
    print("\n1. RGB ↔ Hex:")
    print(f"   RGB(255, 0, 0) → Hex: {rgb_to_hex(255, 0, 0)}")
    print(f"   RGB(255, 0, 0) → Hex (无#): {rgb_to_hex(255, 0, 0, include_hash=False)}")
    
    # RGB ↔ HSL
    print("\n2. RGB ↔ HSL:")
    r, g, b = 255, 0, 0
    h, s, l = rgb_to_hsl(r, g, b)
    print(f"   RGB({r}, {g}, {b}) → HSL({h}, {s}, {l})")
    r2, g2, b2 = hsl_to_rgb(h, s, l)
    print(f"   HSL({h}, {s}, {l}) → RGB({r2}, {g2}, {b2})")
    
    # RGB ↔ HSV
    print("\n3. RGB ↔ HSV:")
    h, s, v = rgb_to_hsv(255, 128, 64)
    print(f"   RGB(255, 128, 64) → HSV({h}, {s}, {v})")
    r, g, b = hsv_to_rgb(h, s, v)
    print(f"   HSV({h}, {s}, {v}) → RGB({r}, {g}, {b})")
    
    # RGB ↔ CMYK
    print("\n4. RGB ↔ CMYK:")
    c, m, y, k = rgb_to_cmyk(255, 0, 0)
    print(f"   RGB(255, 0, 0) → CMYK({c}, {m}, {y}, {k})")
    r, g, b = cmyk_to_rgb(c, m, y, k)
    print(f"   CMYK({c}, {m}, {y}, {k}) → RGB({r}, {g}, {b})")
    
    # Using data classes
    print("\n5. 使用数据类转换:")
    rgb = RGB(100, 150, 200)
    print(f"   原始 RGB: {rgb}")
    hsl = rgb.to_hsl()
    print(f"   → HSL: {hsl}")
    hsv = rgb.to_hsv()
    print(f"   → HSV: {hsv}")
    cmyk = rgb.to_cmyk()
    print(f"   → CMYK: {cmyk}")


def example_color_manipulation():
    """Demonstrate color manipulation operations."""
    print("\n" + "="*60)
    print("颜色操作示例 (Color Manipulation Examples)")
    print("="*60)
    
    base_color = '#ff6600'
    
    # Lighten/Darken
    print("\n1. 亮度调整:")
    print(f"   原色: {base_color}")
    print(f"   加亮 20%: {lighten(base_color, 20).to_hex()}")
    print(f"   加亮 40%: {lighten(base_color, 40).to_hex()}")
    print(f"   加暗 20%: {darken(base_color, 20).to_hex()}")
    print(f"   加暗 40%: {darken(base_color, 40).to_hex()}")
    
    # Saturate/Desaturate
    print("\n2. 饱和度调整:")
    print(f"   原色: {base_color}")
    print(f"   增饱和 30%: {saturate(base_color, 30).to_hex()}")
    print(f"   降饱和 50%: {desaturate(base_color, 50).to_hex()}")
    print(f"   完全去色: {grayscale(base_color).to_hex()}")
    
    # Invert
    print("\n3. 颜色反转:")
    colors = ['#ff0000', '#00ff00', '#0000ff', '#ffffff', '#000000']
    for c in colors:
        inv = invert(c).to_hex()
        print(f"   {c} → {inv}")
    
    # Complement
    print("\n4. 补色:")
    for c in ['#ff0000', '#00ff00', '#0000ff', '#ff6600']:
        comp = complement(c).to_hex()
        print(f"   {c} 补色 → {comp}")
    
    # Mix
    print("\n5. 颜色混合:")
    print(f"   #ff0000 + #0000ff (50%) → {mix('#ff0000', '#0000ff', 0.5).to_hex()}")
    print(f"   #ff0000 + #0000ff (25%) → {mix('#ff0000', '#0000ff', 0.25).to_hex()}")
    print(f"   #ff0000 + #0000ff (75%) → {mix('#ff0000', '#0000ff', 0.75).to_hex()}")
    
    # Blend modes
    print("\n6. 混合模式:")
    blend_modes = ['multiply', 'screen', 'overlay', 'hard_light']
    for mode in blend_modes:
        result = blend('#ff6600', '#0066ff', mode).to_hex()
        print(f"   #ff6600 + #0066ff ({mode}) → {result}")


def example_color_harmony():
    """Demonstrate color harmony generation."""
    print("\n" + "="*60)
    print("色彩和谐示例 (Color Harmony Examples)")
    print("="*60)
    
    base_color = '#ff6600'
    
    # Analogous
    print("\n1. 类似色 (Analogous):")
    colors = analogous(base_color)
    print(f"   基色: {base_color}")
    for i, c in enumerate(colors):
        print(f"   [{i}] {c.to_hex()}")
    
    # Triadic
    print("\n2. 三等分色 (Triadic):")
    colors = triadic(base_color)
    for i, c in enumerate(colors):
        h, s, l = rgb_to_hsl(c.r, c.g, c.b)
        print(f"   [{i}] {c.to_hex()} (H={h}°)")
    
    # Split Complement
    print("\n3. 分裂补色 (Split Complement):")
    colors = split_complement(base_color)
    for i, c in enumerate(colors):
        print(f"   [{i}] {c.to_hex()}")
    
    # Tetradic
    print("\n4. 四等分色 (Tetradic):")
    colors = tetradic(base_color)
    for i, c in enumerate(colors):
        h, s, l = rgb_to_hsl(c.r, c.g, c.b)
        print(f"   [{i}] {c.to_hex()} (H={h}°)")
    
    # Monochromatic
    print("\n5. 单色变化 (Monochromatic):")
    colors = monochromatic(base_color, 5)
    for i, c in enumerate(colors):
        h, s, l = rgb_to_hsl(c.r, c.g, c.b)
        print(f"   [{i}] {c.to_hex()} (L={l}%)")


def example_accessibility():
    """Demonstrate accessibility-related functions."""
    print("\n" + "="*60)
    print("可访问性示例 (Accessibility Examples)")
    print("="*60)
    
    # Luminance
    print("\n1. 相对亮度:")
    colors = ['#ffffff', '#000000', '#ff0000', '#00ff00', '#0000ff']
    for c in colors:
        lum = luminance(c)
        print(f"   {c} 亮度 = {lum:.3f}")
    
    # Contrast ratio
    print("\n2. 对比度:")
    bg_fg_pairs = [
        ('#ffffff', '#000000'),
        ('#ffffff', '#333333'),
        ('#ffffff', '#777777'),
        ('#ffcc00', '#000000'),
        ('#ffcc00', '#333333'),
    ]
    for bg, fg in bg_fg_pairs:
        ratio = contrast_ratio(bg, fg)
        rating = wcag_rating(ratio)
        print(f"   {bg} / {fg} → 对比度 {ratio:.1f}:1 [{rating}]")
    
    # WCAG ratings
    print("\n3. WCAG 等级说明:")
    print("   AAA  ≥ 7:1   (最高要求，适合小文本)")
    print("   AA   ≥ 4.5:1 (标准要求，适合正文)")
    print("   AA Large ≥ 3:1 (大文本)")
    print("   Fail < 3:1   (不合格)")
    
    # Text color selection
    print("\n4. 自动文本颜色选择:")
    backgrounds = ['#ffffff', '#000000', '#ff0000', '#00ff00', '#ffcc00']
    for bg in backgrounds:
        text = text_color_for_bg(bg)
        ratio = contrast_ratio(bg, text)
        print(f"   背景 {bg} → 文本颜色 {text} (对比度 {ratio:.1f}:1)")
    
    # Brightness
    print("\n5. 感知亮度:")
    colors = ['#ffffff', '#cccccc', '#999999', '#666666', '#333333', '#000000']
    for c in colors:
        bri = brightness(c)
        status = "亮" if is_light(c) else "暗"
        print(f"   {c} 亮度值 = {bri} ({status})")


def example_gradients():
    """Demonstrate gradient generation."""
    print("\n" + "="*60)
    print("渐变示例 (Gradient Examples)")
    print("="*60)
    
    # Simple gradient
    print("\n1. 简单渐变 (黑到白):")
    colors = gradient('#000000', '#ffffff', 5)
    for i, c in enumerate(colors):
        print(f"   [{i}] {c.to_hex()}")
    
    # Color gradient
    print("\n2. 颜色渐变 (红到蓝):")
    colors = gradient('#ff0000', '#0000ff', 10)
    for i, c in enumerate(colors):
        print(f"   [{i}] {c.to_hex()}")
    
    # Multi-color gradient
    print("\n3. 多色渐变:")
    multi_colors = ['#ff0000', '#00ff00', '#0000ff']
    result = multi_gradient(multi_colors, 4)
    print(f"   路径: 红 → 绿 → 蓝")
    for i, c in enumerate(result):
        print(f"   [{i}] {c.to_hex()}")


def example_random_colors():
    """Demonstrate random color generation."""
    print("\n" + "="*60)
    print("随机颜色示例 (Random Color Examples)")
    print("="*60)
    
    # Random colors
    print("\n1. 完全随机:")
    for i in range(5):
        rgb = random_color()
        print(f"   [{i}] {rgb.to_hex()}")
    
    # Random with seed
    print("\n2. 可重复随机 (使用种子):")
    for seed in [42, 42, 100]:
        rgb = random_color(seed=seed)
        print(f"   seed={seed} → {rgb.to_hex()}")
    
    # Random hue with fixed saturation/lightness
    print("\n3. 固定饱和度/亮度的随机色相:")
    for i in range(5):
        rgb = random_hue(70, 50)
        h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
        print(f"   [{i}] {rgb.to_hex()} (H={h}°, S={s}%, L={l}%)")
    
    # Random pastel
    print("\n4. 随机粉彩色:")
    for i in range(5):
        rgb = random_pastel()
        h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
        print(f"   [{i}] {rgb.to_hex()} (S={s}%, L={l}%)")


def example_practical_use():
    """Demonstrate practical use cases."""
    print("\n" + "="*60)
    print("实际应用示例 (Practical Use Examples)")
    print("="*60)
    
    # Color palette generation
    print("\n1. 生成配色方案:")
    base = '#3498db'
    print(f"   基色: {base}")
    print(f"   加亮变体: {lighten(base, 20).to_hex()}, {lighten(base, 40).to_hex()}")
    print(f"   加暗变体: {darken(base, 20).to_hex()}, {darken(base, 40).to_hex()}")
    print(f"   补色: {complement(base).to_hex()}")
    triad = triadic(base)
    print(f"   三等分色: {triad[1].to_hex()}, {triad[2].to_hex()}")
    
    # UI color validation
    print("\n2. UI 对比度验证:")
    ui_pairs = [
        ('按钮背景', '#3498db', '按钮文字', '#ffffff'),
        ('警告背景', '#f1c40f', '警告文字', '#000000'),
        ('错误背景', '#e74c3c', '错误文字', '#ffffff'),
    ]
    for bg_name, bg, fg_name, fg in ui_pairs:
        ratio = contrast_ratio(bg, fg)
        rating = wcag_rating(ratio)
        status = "✓" if ratio >= 4.5 else "✗"
        print(f"   {status} {bg_name}/{fg_name}: 对比度 {ratio:.1f}:1 [{rating}]")
    
    # Closest named color
    print("\n3. 找最近的 CSS 颜色名:")
    test_colors = ['#e74c3c', '#3498db', '#f39c12', '#9b59b6']
    for c in test_colors:
        rgb = parse_color(c)
        name = rgb_to_color_name(rgb)
        closest = closest_color(c, [parse_color(n).to_hex() for n in ['red', 'blue', 'green', 'yellow']])
        print(f"   {c} → CSS名: {name or '无匹配'}, 最接近基础色索引: {closest}")
    
    # Color distance
    print("\n4. 颜色相似度计算:")
    ref = '#ff0000'
    others = ['#ff1010', '#ff2020', '#ee0000', '#00ff00']
    print(f"   参考: {ref}")
    for c in others:
        dist = color_distance(ref, c)
        print(f"   {c} → 距离: {dist:.1f}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("AllToolkit Color Utilities - 使用示例")
    print("="*60)
    
    example_color_parsing()
    example_color_conversion()
    example_color_manipulation()
    example_color_harmony()
    example_accessibility()
    example_gradients()
    example_random_colors()
    example_practical_use()
    
    print("\n" + "="*60)
    print("示例完成!")
    print("="*60)


if __name__ == '__main__':
    main()