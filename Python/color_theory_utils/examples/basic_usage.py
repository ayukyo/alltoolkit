#!/usr/bin/env python3
"""
Color Theory Utils 使用示例

演示颜色理论工具库的各种功能
"""

import sys
import os

# 将父目录添加到路径
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from mod import (
    RGB, HSL, HSV, CMYK, LAB,
    HarmonyType, WCAGLevel, ColorTemperature,
    hex_to_rgb, get_harmony, get_contrast_ratio,
    get_wcag_level, is_accessible, mix_colors, generate_gradient,
    lighten, darken, saturate, desaturate,
    random_color, random_hue, generate_palette,
    color_distance, lab_distance, find_closest_color,
    get_color_name, invert_color, grayscale, sepia,
    get_accessible_color, generate_random_palette, interpolate_colors,
    suggest_text_color, create_color_scheme, analyze_color
)


def print_color(color, name=""):
    """打印颜色信息"""
    if isinstance(color, RGB):
        print(f"  {name}: {color.to_hex()} (RGB: {color.r}, {color.g}, {color.b})")
    elif isinstance(color, str):
        print(f"  {name}: {color}")


def demo_color_conversions():
    """演示颜色空间转换"""
    print("\n" + "=" * 60)
    print("🎨 颜色空间转换演示")
    print("=" * 60)
    
    # 从 RGB 开始
    rgb = RGB(255, 100, 50)
    print(f"\n原始颜色: RGB({rgb.r}, {rgb.g}, {rgb.b})")
    
    # 转换到各种颜色空间
    hex_color = rgb.to_hex()
    hsl = rgb.to_hsl()
    hsv = rgb.to_hsv()
    cmyk = rgb.to_cmyk()
    lab = rgb.to_lab()
    
    print(f"  HEX:  {hex_color}")
    print(f"  HSL:  {hsl}")
    print(f"  HSV:  {hsv}")
    print(f"  CMYK: {cmyk}")
    print(f"  LAB:  {lab}")
    
    # 从 HEX 转换回来
    rgb_back = hex_to_rgb(hex_color)
    print(f"\n从 HEX 转回 RGB: RGB({rgb_back.r}, {rgb_back.g}, {rgb_back.b})")
    
    # 从 HSL 创建颜色
    hsl_color = HSL(180, 80, 50).to_rgb()
    print(f"\nHSL(180°, 80%, 50%) = {hsl_color.to_hex()}")
    
    # 从 HSV 创建颜色
    hsv_color = HSV(300, 60, 80).to_rgb()
    print(f"HSV(300°, 60%, 80%) = {hsv_color.to_hex()}")


def demo_color_harmony():
    """演示颜色和谐"""
    print("\n" + "=" * 60)
    print("🌈 颜色和谐方案演示")
    print("=" * 60)
    
    base_color = RGB(255, 100, 0)  # 橙色
    print(f"\n基准颜色: {base_color.to_hex()}")
    
    # 互补色
    complementary = get_harmony(base_color, HarmonyType.COMPLEMENTARY)
    print(f"\n互补色配色:")
    for i, color in enumerate(complementary, 1):
        print_color(color, f"颜色 {i}")
    
    # 类似色
    analogous = get_harmony(base_color, HarmonyType.ANALOGOUS)
    print(f"\n类似色配色:")
    for i, color in enumerate(analogous, 1):
        print_color(color, f"颜色 {i}")
    
    # 三角色
    triadic = get_harmony(base_color, HarmonyType.TRIADIC)
    print(f"\n三角色配色:")
    for i, color in enumerate(triadic, 1):
        print_color(color, f"颜色 {i}")
    
    # 四角色
    tetradic = get_harmony(base_color, HarmonyType.TETRADIC)
    print(f"\n四角色配色:")
    for i, color in enumerate(tetradic, 1):
        print_color(color, f"颜色 {i}")
    
    # 分裂互补色
    split_comp = get_harmony(base_color, HarmonyType.SPLIT_COMPLEMENTARY)
    print(f"\n分裂互补色配色:")
    for i, color in enumerate(split_comp, 1):
        print_color(color, f"颜色 {i}")


def demo_contrast_and_accessibility():
    """演示对比度和可访问性"""
    print("\n" + "=" * 60)
    print("👁️ 对比度与可访问性演示")
    print("=" * 60)
    
    # 测试几组颜色对比度
    test_pairs = [
        (RGB(255, 255, 255), RGB(0, 0, 0), "白色/黑色"),
        (RGB(255, 255, 255), RGB(128, 128, 128), "白色/灰色"),
        (RGB(255, 0, 0), RGB(0, 0, 255), "红色/蓝色"),
        (RGB(0, 128, 255), RGB(255, 255, 255), "蓝色背景/白色文字"),
    ]
    
    for fg, bg, desc in test_pairs:
        ratio = get_contrast_ratio(fg, bg)
        level = get_wcag_level(ratio)
        accessible_aa = is_accessible(fg, bg, WCAGLevel.AA)
        accessible_aaa = is_accessible(fg, bg, WCAGLevel.AAA)
        
        print(f"\n{desc}:")
        print(f"  对比度: {ratio:.2f}:1")
        print(f"  WCAG 等级: {level.value}")
        print(f"  AA 合格: {'✓' if accessible_aa else '✗'}")
        print(f"  AAA 合格: {'✓' if accessible_aaa else '✗'}")
    
    # 建议文字颜色
    print("\n" + "-" * 40)
    print("文字颜色建议:")
    
    backgrounds = [
        RGB(255, 255, 255),  # 白色
        RGB(0, 0, 0),        # 黑色
        RGB(0, 100, 200),    # 蓝色
        RGB(200, 50, 50),    # 红色
    ]
    
    for bg in backgrounds:
        suggestion = suggest_text_color(bg)
        print(f"\n背景色 {bg.to_hex()}:")
        print(f"  推荐文字色: {suggestion['recommended'].to_hex()}")
        print(f"  对比度: {suggestion['contrast_ratio']:.2f}:1")
        print(f"  WCAG 等级: {suggestion['wcag_level']}")


def demo_color_manipulation():
    """演示颜色操作"""
    print("\n" + "=" * 60)
    print("🔧 颜色操作演示")
    print("=" * 60)
    
    base = RGB(255, 100, 50)
    print(f"\n基准颜色: {base.to_hex()}")
    
    # 变亮和变暗
    lighter = lighten(base, 20)
    darker = darken(base, 20)
    print(f"\n变亮 20%: {lighter.to_hex()}")
    print(f"变暗 20%: {darker.to_hex()}")
    
    # 饱和度调整
    saturated = saturate(base, 30)
    desaturated = desaturate(base, 30)
    print(f"\n增加饱和度 30%: {saturated.to_hex()}")
    print(f"降低饱和度 30%: {desaturated.to_hex()}")
    
    # 颜色混合
    red = RGB(255, 0, 0)
    blue = RGB(0, 0, 255)
    purple = mix_colors(red, blue, 0.5)
    print(f"\n红色 {red.to_hex()} + 蓝色 {blue.to_hex()} = {purple.to_hex()}")
    
    # 反色
    inverted = invert_color(base)
    print(f"\n反色: {inverted.to_hex()}")
    
    # 灰度
    gray = grayscale(base)
    print(f"灰度: {gray.to_hex()}")
    
    # 怀旧
    vintage = sepia(base)
    print(f"怀旧: {vintage.to_hex()}")


def demo_gradient_generation():
    """演示渐变生成"""
    print("\n" + "=" * 60)
    print("🌅 渐变生成演示")
    print("=" * 60)
    
    # 简单渐变
    red = RGB(255, 0, 0)
    blue = RGB(0, 0, 255)
    
    print(f"\n从 {red.to_hex()} 到 {blue.to_hex()} 的渐变:")
    gradient = generate_gradient(red, blue, 7)
    for i, color in enumerate(gradient):
        print(f"  步骤 {i+1}: {color.to_hex()}")
    
    # 多色渐变
    print(f"\n多色渐变 (彩虹):")
    rainbow_colors = [
        RGB(255, 0, 0),     # 红
        RGB(255, 165, 0),   # 橙
        RGB(255, 255, 0),   # 黄
        RGB(0, 255, 0),     # 绿
        RGB(0, 0, 255),     # 蓝
        RGB(128, 0, 128),   # 紫
    ]
    smooth_rainbow = interpolate_colors(rainbow_colors, 12)
    for i, color in enumerate(smooth_rainbow):
        print(f"  步骤 {i+1:2d}: {color.to_hex()}")


def demo_palette_generation():
    """演示调色板生成"""
    print("\n" + "=" * 60)
    print("🎨 调色板生成演示")
    print("=" * 60)
    
    base = RGB(0, 128, 255)  # 蓝色
    print(f"\n基准颜色: {base.to_hex()}")
    
    # 生成调色板
    palette = generate_palette(base, variations=4)
    print(f"\n完整调色板 ({len(palette)} 色):")
    
    shades = palette[:5]  # 包含原色和暗色调
    tints = palette[5:10]
    tones = palette[10:15]
    
    print("\n暗色调:")
    for color in shades:
        print(f"  {color.to_hex()}")
    
    print("\n亮色调:")
    for color in tints:
        print(f"  {color.to_hex()}")
    
    print("\n灰色调:")
    for color in tones:
        print(f"  {color.to_hex()}")
    
    # 随机调色板
    print("\n" + "-" * 40)
    print("随机调色板:")
    random_palette = generate_random_palette(5)
    for i, color in enumerate(random_palette, 1):
        print(f"  颜色 {i}: {color.to_hex()}")
    
    # 基于和谐的调色板
    print("\n和谐调色板 (三角色):")
    harmony_palette = generate_random_palette(3, HarmonyType.TRIADIC)
    for i, color in enumerate(harmony_palette, 1):
        print(f"  颜色 {i}: {color.to_hex()}")


def demo_color_analysis():
    """演示颜色分析"""
    print("\n" + "=" * 60)
    print("🔍 颜色分析演示")
    print("=" * 60)
    
    colors = [
        RGB(255, 0, 0),      # 红色
        RGB(0, 150, 255),    # 蓝色
        RGB(100, 200, 100),  # 绿色
        RGB(255, 200, 50),   # 金色
        RGB(150, 50, 200),   # 紫色
    ]
    
    for color in colors:
        analysis = analyze_color(color)
        print(f"\n颜色 {color.to_hex()}:")
        print(f"  名称: {analysis['name']}")
        print(f"  HSL: {analysis['hsl']['h']}°, {analysis['hsl']['s']}%, {analysis['hsl']['l']}%")
        print(f"  温度: {analysis['temperature']}")
        print(f"  类别: {analysis['categories']['hue']}, {analysis['categories']['saturation']}, {analysis['categories']['lightness']}")
        print(f"  浅色: {'是' if analysis['is_light'] else '否'}")
        print(f"  推荐文字色: {analysis['text_suggestion']['recommended'].to_hex()} (对比度 {analysis['text_suggestion']['contrast_ratio']:.1f}:1)")


def demo_color_scheme():
    """演示完整配色方案"""
    print("\n" + "=" * 60)
    print("🎭 完整配色方案演示")
    print("=" * 60)
    
    base = RGB(0, 120, 200)  # 品牌蓝色
    print(f"\n基准颜色: {base.to_hex()}")
    
    scheme = create_color_scheme(base)
    
    print("\n主色:")
    for color in scheme['primary']:
        print(f"  {color.to_hex()}")
    
    print("\n互补色:")
    for color in scheme['complementary']:
        print(f"  {color.to_hex()}")
    
    print("\n类似色:")
    for color in scheme['analogous']:
        print(f"  {color.to_hex()}")
    
    print("\n三角色:")
    for color in scheme['triadic']:
        print(f"  {color.to_hex()}")
    
    print("\n暗色调:")
    for color in scheme['shades']:
        print(f"  {color.to_hex()}")
    
    print("\n亮色调:")
    for color in scheme['tints']:
        print(f"  {color.to_hex()}")
    
    print("\n中性色:")
    for color in scheme['neutrals']:
        print(f"  {color.to_hex()}")


def demo_color_matching():
    """演示颜色匹配"""
    print("\n" + "=" * 60)
    print("🎯 颜色匹配演示")
    print("=" * 60)
    
    # 查找最接近的颜色
    target = RGB(200, 80, 80)  # 浅红色
    candidates = [
        RGB(255, 0, 0),     # 红色
        RGB(0, 255, 0),     # 绿色
        RGB(0, 0, 255),     # 蓝色
        RGB(255, 165, 0),   # 橙色
        RGB(255, 255, 0),   # 黄色
    ]
    
    print(f"\n目标颜色: {target.to_hex()}")
    print("\n候选颜色:")
    for color in candidates:
        dist = color_distance(target, color)
        lab_dist = lab_distance(target, color)
        print(f"  {color.to_hex()}: RGB 距离={dist:.1f}, LAB 距离={lab_dist:.1f}")
    
    closest_rgb = find_closest_color(target, candidates)
    closest_lab = find_closest_color(target, candidates, use_lab=True)
    
    print(f"\n最接近的颜色 (RGB 距离): {closest_rgb.to_hex()}")
    print(f"最接近的颜色 (LAB 距离): {closest_lab.to_hex()}")


def demo_random_colors():
    """演示随机颜色生成"""
    print("\n" + "=" * 60)
    print("🎲 随机颜色生成演示")
    print("=" * 60)
    
    # 随机颜色
    print("\n随机颜色:")
    for i in range(5):
        color = random_color()
        print(f"  {color.to_hex()}")
    
    # 暖色系随机
    print("\n暖色系随机 (色相 0-60):")
    for i in range(5):
        color = random_hue(hue_range=(0, 60), saturation_range=(70, 100), lightness_range=(40, 70))
        print(f"  {color.to_hex()}")
    
    # 冷色系随机
    print("\n冷色系随机 (色相 180-270):")
    for i in range(5):
        color = random_hue(hue_range=(180, 270), saturation_range=(60, 90), lightness_range=(30, 60))
        print(f"  {color.to_hex()}")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🎨 Color Theory Utils - 颜色理论工具库演示")
    print("=" * 60)
    
    demo_color_conversions()
    demo_color_harmony()
    demo_contrast_and_accessibility()
    demo_color_manipulation()
    demo_gradient_generation()
    demo_palette_generation()
    demo_color_analysis()
    demo_color_scheme()
    demo_color_matching()
    demo_random_colors()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()