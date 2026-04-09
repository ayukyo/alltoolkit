#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Color Utilities Basic Usage Examples
==================================================
演示 color_utils 模块的基础用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mod import *


def demo_color_conversion():
    """演示颜色格式转换"""
    print("\n" + "="*60)
    print("1. 颜色格式转换")
    print("="*60)
    
    hex_color = "#FF5733"
    print(f"\n原始颜色：{hex_color}")
    
    # 转换为各种格式
    rgb = hex_to_rgb(hex_color)
    print(f"  RGB:  {rgb}")
    
    hsl = hex_to_hsl(hex_color)
    print(f"  HSL:  {hsl[0]}°, {hsl[1]}%, {hsl[2]}%")
    
    hsv = hex_to_hsv(hex_color)
    print(f"  HSV:  {hsv[0]}°, {hsv[1]}%, {hsv[2]}%")
    
    cmyk = hex_to_cmyk(hex_color)
    print(f"  CMYK: C{cmyk[0]}% M{cmyk[1]}% Y{cmyk[2]}% K{cmyk[3]}%")
    
    # 反向转换
    print(f"\n反向转换验证:")
    print(f"  RGB → HEX: {rgb_to_hex(rgb)}")
    print(f"  HSL → HEX: {hsl_to_hex(hsl)}")
    print(f"  HSV → HEX: {hsv_to_hex(hsv)}")
    print(f"  CMYK → HEX: {rgb_to_hex(cmyk_to_rgb(cmyk))}")


def demo_color_manipulation():
    """演示颜色操作"""
    print("\n" + "="*60)
    print("2. 颜色操作")
    print("="*60)
    
    base = "#3498DB"
    print(f"\n基色：{base} (蓝色)")
    
    # 调亮/调暗
    print(f"\n明暗调整:")
    print(f"  调亮 20%:  {lighten(base, 0.2)}")
    print(f"  调亮 40%:  {lighten(base, 0.4)}")
    print(f"  调暗 20%:  {darken(base, 0.2)}")
    print(f"  调暗 40%:  {darken(base, 0.4)}")
    
    # 饱和度
    print(f"\n饱和度调整:")
    print(f"  增加饱和：{saturate(base, 0.3)}")
    print(f"  降低饱和：{desaturate(base, 0.5)}")
    
    # 反转
    print(f"\n颜色反转:")
    print(f"  反转色：   {invert_color(base)}")
    
    # 色相旋转
    print(f"\n色相旋转:")
    print(f"  +60°:  {adjust_hue(base, 60)}")
    print(f"  +120°: {adjust_hue(base, 120)}")
    print(f"  +180°: {adjust_hue(base, 180)} (互补色)")
    print(f"  +240°: {adjust_hue(base, 240)}")
    
    # 颜色混合
    print(f"\n颜色混合:")
    orange = "#FF5733"
    print(f"  {base} + {orange}:")
    for ratio in [0.25, 0.5, 0.75]:
        mixed = mix_colors(base, orange, ratio)
        print(f"    {ratio*100:.0f}% {orange}: {mixed}")


def demo_color_palettes():
    """演示调色板生成"""
    print("\n" + "="*60)
    print("3. 调色板生成")
    print("="*60)
    
    base = "#9B59B6"
    print(f"\n基色：{base} (紫色)")
    
    # 互补色
    print(f"\n互补色方案:")
    print(f"  {complementary_color(base)}")
    
    # 类似色
    print(f"\n类似色方案:")
    analogous = analogous_colors(base, 2)
    for i, color in enumerate(analogous, 1):
        print(f"  颜色{i}: {color}")
    
    # 三元色
    print(f"\n三元色方案:")
    triadic = triadic_colors(base)
    for i, color in enumerate(triadic, 1):
        print(f"  颜色{i}: {color}")
    
    # 分裂互补色
    print(f"\n分裂互补色方案:")
    split = split_complementary(base)
    for i, color in enumerate(split, 1):
        print(f"  颜色{i}: {color}")
    
    # 四元色
    print(f"\n四元色方案:")
    tetradic = tetradic_colors(base)
    for i, color in enumerate(tetradic, 1):
        print(f"  颜色{i}: {color}")
    
    # 单色系
    print(f"\n单色系方案:")
    mono = monochromatic_colors(base, 5)
    for i, color in enumerate(mono, 1):
        print(f"  颜色{i}: {color}")
    
    # 渐变色
    print(f"\n渐变色方案 ({base} → #2ECC71):")
    gradient = generate_gradient(base, "#2ECC71", 7)
    for i, color in enumerate(gradient, 1):
        print(f"  步骤{i}: {color}")


def demo_accessibility():
    """演示无障碍检测"""
    print("\n" + "="*60)
    print("4. 无障碍检测 (WCAG)")
    print("="*60)
    
    test_cases = [
        ("#000000", "#FFFFFF", "黑底白字"),
        ("#FFFFFF", "#000000", "白底黑字"),
        ("#3498DB", "#FFFFFF", "蓝底白字"),
        ("#FF5733", "#FFFFFF", "橙底白字"),
        ("#95A5A6", "#FFFFFF", "灰底白字"),
        ("#2ECC71", "#000000", "绿底黑字"),
    ]
    
    print(f"\n{'背景':<12} {'文字':<12} {'对比度':<10} {'AA':<6} {'AAA':<6}")
    print("-" * 50)
    
    for bg, fg, desc in test_cases:
        ratio = contrast_ratio(bg, fg)
        aa = "✓" if is_wcag_aa(bg, fg) else "✗"
        aaa = "✓" if is_wcag_aaa(bg, fg) else "✗"
        print(f"{bg:<12} {fg:<12} {ratio:>6.2f}:1  {aa:<6} {aaa:<6}  ({desc})")
    
    # 获取可读文字颜色
    print(f"\n自动选择可读文字颜色:")
    backgrounds = ["#3498DB", "#FF5733", "#2ECC71", "#F39C12", "#9B59B6"]
    for bg in backgrounds:
        text = get_accessible_text_color(bg)
        print(f"  {bg} → 文字颜色：{text}")


def demo_color_naming():
    """演示颜色命名"""
    print("\n" + "="*60)
    print("5. 颜色命名和识别")
    print("="*60)
    
    # 已知颜色
    known_colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#000000", "#FFFFFF"]
    print(f"\n已知颜色识别:")
    for color in known_colors:
        name = get_color_name(color)
        print(f"  {color} → {name}")
    
    # 相似度检测
    print(f"\n颜色相似度检测:")
    base = "#FF5733"
    similar = ["#FF5834", "#FF5632", "#FF6040", "#0000FF", "#00FF00"]
    for color in similar:
        is_sim = is_similar_color(base, color, threshold=10)
        distance = color_distance(hex_to_rgb(base), hex_to_rgb(color))
        status = "✓ 相似" if is_sim else "✗ 不同"
        print(f"  {color}: 距离={distance:.2f} {status}")
    
    # 颜色解析
    print(f"\n颜色解析:")
    inputs = ["#FF5733", "Red", (0, 255, 0), "Blue"]
    for inp in inputs:
        try:
            rgb = parse_color(inp)
            print(f"  {str(inp):<15} → RGB{rgb}")
        except ValueError as e:
            print(f"  {str(inp):<15} → 错误：{e}")


def demo_format_output():
    """演示格式化输出"""
    print("\n" + "="*60)
    print("6. 颜色格式化输出")
    print("="*60)
    
    rgb = (255, 87, 51)
    print(f"\nRGB{rgb} 的各种格式:")
    
    formats = ["hex", "rgb", "rgba", "hsl", "hsv", "cmyk"]
    for fmt in formats:
        output = format_color(rgb, fmt)
        print(f"  {fmt:>6}: {output}")
    
    # 随机颜色
    print(f"\n随机颜色生成:")
    for i in range(5):
        color = random_color()
        name = get_color_name(color) or "未知"
        print(f"  {color} ({name})")


def main():
    """运行所有演示"""
    print("\n" + "#"*60)
    print("# AllToolkit - Color Utilities 基础使用演示")
    print("#"*60)
    
    demo_color_conversion()
    demo_color_manipulation()
    demo_color_palettes()
    demo_accessibility()
    demo_color_naming()
    demo_format_output()
    
    print("\n" + "="*60)
    print("演示完成!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
