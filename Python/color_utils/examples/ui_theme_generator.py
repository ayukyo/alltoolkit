#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Color Utilities Advanced Example: UI Theme Generator
==================================================================
高级示例：生成完整的 UI 主题配色方案。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mod import *


def generate_ui_theme(base_color: str, theme_name: str = "Custom") -> dict:
    """
    生成完整的 UI 主题配色方案。
    
    Args:
        base_color: 主题基色 (HEX)
        theme_name: 主题名称
    
    Returns:
        包含所有主题色的字典
    """
    # 主色系
    primary = base_color
    primary_light = lighten(base_color, 0.15)
    primary_dark = darken(base_color, 0.15)
    primary_lighter = lighten(base_color, 0.3)
    primary_darker = darken(base_color, 0.3)
    
    # 辅助色（互补色）
    accent = complementary_color(base_color)
    accent_light = lighten(accent, 0.1)
    accent_dark = darken(accent, 0.1)
    
    # 中性色
    neutral_50 = "#FAFAFA"
    neutral_100 = "#F5F5F5"
    neutral_200 = "#EEEEEE"
    neutral_300 = "#E0E0E0"
    neutral_400 = "#BDBDBD"
    neutral_500 = "#9E9E9E"
    neutral_600 = "#757575"
    neutral_700 = "#616161"
    neutral_800 = "#424242"
    neutral_900 = "#212121"
    
    # 状态色
    success = "#4CAF50"
    warning = "#FF9800"
    error = "#F44336"
    info = base_color
    
    # 根据背景自动选择文字颜色
    def get_text_on(bg_color):
        return get_accessible_text_color(bg_color)
    
    theme = {
        "name": theme_name,
        "base": base_color,
        
        "primary": {
            "main": primary,
            "light": primary_light,
            "dark": primary_dark,
            "lighter": primary_lighter,
            "darker": primary_darker,
            "text": get_text_on(primary),
        },
        
        "accent": {
            "main": accent,
            "light": accent_light,
            "dark": accent_dark,
            "text": get_text_on(accent),
        },
        
        "neutral": {
            "50": neutral_50,
            "100": neutral_100,
            "200": neutral_200,
            "300": neutral_300,
            "400": neutral_400,
            "500": neutral_500,
            "600": neutral_600,
            "700": neutral_700,
            "800": neutral_800,
            "900": neutral_900,
        },
        
        "background": {
            "default": neutral_50,
            "paper": neutral_100,
            "elevated": "#FFFFFF",
        },
        
        "text": {
            "primary": neutral_900,
            "secondary": neutral_700,
            "disabled": neutral_500,
            "inverse": "#FFFFFF",
        },
        
        "status": {
            "success": {
                "main": success,
                "light": lighten(success, 0.2),
                "dark": darken(success, 0.2),
                "text": get_text_on(success),
            },
            "warning": {
                "main": warning,
                "light": lighten(warning, 0.2),
                "dark": darken(warning, 0.2),
                "text": get_text_on(warning),
            },
            "error": {
                "main": error,
                "light": lighten(error, 0.2),
                "dark": darken(error, 0.2),
                "text": get_text_on(error),
            },
            "info": {
                "main": info,
                "light": lighten(info, 0.2),
                "dark": darken(info, 0.2),
                "text": get_text_on(info),
            },
        },
        
        "gradient": {
            "primary": generate_gradient(primary_light, primary_dark, 5),
            "sunset": generate_gradient("#FF5733", "#9B59B6", 5),
            "ocean": generate_gradient("#3498DB", "#2ECC71", 5),
        },
        
        "palette": {
            "analogous": analogous_colors(base_color, 3),
            "triadic": triadic_colors(base_color),
            "monochromatic": monochromatic_colors(base_color, 5),
        },
    }
    
    return theme


def print_theme_report(theme: dict):
    """打印主题报告"""
    print("\n" + "="*70)
    print(f"🎨 UI 主题：{theme['name']}")
    print(f"   基色：{theme['base']}")
    print("="*70)
    
    # 主色系
    print("\n📌 主色系 Primary")
    print("-" * 50)
    for key, value in theme['primary'].items():
        if isinstance(value, str):
            rgb = hex_to_rgb(value)
            lum = get_luminance(rgb)
            print(f"  {key:<10} {value}  (亮度：{lum:.2f})")
    
    # 辅助色
    print("\n🌟 辅助色 Accent")
    print("-" * 50)
    for key, value in theme['accent'].items():
        print(f"  {key:<10} {value}")
    
    # 中性色
    print("\n⚪ 中性色 Neutral")
    print("-" * 50)
    for key, value in theme['neutral'].items():
        print(f"  {key:<10} {value}")
    
    # 背景色
    print("\n📄 背景色 Background")
    print("-" * 50)
    for key, value in theme['background'].items():
        print(f"  {key:<12} {value}")
    
    # 文字色
    print("\n📝 文字色 Text")
    print("-" * 50)
    for key, value in theme['text'].items():
        print(f"  {key:<12} {value}")
    
    # 状态色
    print("\n🚦 状态色 Status")
    print("-" * 50)
    for status, colors in theme['status'].items():
        print(f"  {status.upper()}:")
        for key, value in colors.items():
            print(f"    {key:<10} {value}")
    
    # 渐变色
    print("\n🌈 渐变色 Gradients")
    print("-" * 50)
    for name, gradient in theme['gradient'].items():
        print(f"  {name}: {' → '.join(gradient)}")
    
    # 调色板
    print("\n🎨 调色板 Palettes")
    print("-" * 50)
    for name, palette in theme['palette'].items():
        print(f"  {name}: {', '.join(palette)}")
    
    # 无障碍报告
    print("\n♿ 无障碍检查 Accessibility")
    print("-" * 50)
    
    checks = [
        ("主色背景 + 主色文字", theme['primary']['main'], theme['primary']['text']),
        ("辅助色背景 + 辅助色文字", theme['accent']['main'], theme['accent']['text']),
        ("成功色背景 + 成功色文字", theme['status']['success']['main'], theme['status']['success']['text']),
        ("警告色背景 + 警告色文字", theme['status']['warning']['main'], theme['status']['warning']['text']),
        ("错误色背景 + 错误色文字", theme['status']['error']['main'], theme['status']['error']['text']),
    ]
    
    all_pass = True
    for desc, bg, fg in checks:
        ratio = contrast_ratio(bg, fg)
        aa = is_wcag_aa(bg, fg)
        aaa = is_wcag_aaa(bg, fg)
        
        status = "✓✓" if aaa else ("✓" if aa else "✗")
        if not aa:
            all_pass = False
        
        print(f"  {desc}:")
        print(f"    对比度：{ratio:.2f}:1  [{status}]")
        if not aa:
            suggested = get_accessible_text_color(bg)
            print(f"    ⚠️  建议文字色：{suggested}")
    
    print(f"\n  总体评估：{'✓ 通过所有 AA 检查' if all_pass else '⚠️ 部分未通过 AA 检查'}")


def generate_css_variables(theme: dict) -> str:
    """生成 CSS 变量代码"""
    css = ":root {\n"
    
    # 主色
    css += f"  --color-primary: {theme['primary']['main']};\n"
    css += f"  --color-primary-light: {theme['primary']['light']};\n"
    css += f"  --color-primary-dark: {theme['primary']['dark']};\n"
    css += f"  --color-primary-text: {theme['primary']['text']};\n"
    
    # 辅助色
    css += f"  --color-accent: {theme['accent']['main']};\n"
    css += f"  --color-accent-text: {theme['accent']['text']};\n"
    
    # 中性色
    for key, value in theme['neutral'].items():
        css += f"  --color-neutral-{key}: {value};\n"
    
    # 背景
    css += f"  --color-background: {theme['background']['default']};\n"
    css += f"  --color-surface: {theme['background']['paper']};\n"
    
    # 文字
    css += f"  --color-text-primary: {theme['text']['primary']};\n"
    css += f"  --color-text-secondary: {theme['text']['secondary']};\n"
    
    # 状态色
    for status, colors in theme['status'].items():
        css += f"  --color-{status}: {colors['main']};\n"
        css += f"  --color-{status}-text: {colors['text']};\n"
    
    css += "}\n"
    return css


def main():
    """主函数"""
    print("\n" + "#"*70)
    print("# AllToolkit - Color Utilities 高级示例：UI 主题生成器")
    print("#"*70)
    
    # 预定义主题
    themes = [
        ("海洋蓝", "#3498DB"),
        ("翡翠绿", "#2ECC71"),
        ("葡萄紫", "#9B59B6"),
        ("珊瑚橙", "#FF5733"),
        ("玫瑰红", "#E91E63"),
        ("午夜黑", "#2C3E50"),
    ]
    
    for name, color in themes:
        theme = generate_ui_theme(color, name)
        print_theme_report(theme)
        
        # 生成 CSS 变量
        print("\n💻 CSS 变量代码:")
        print("-" * 50)
        css = generate_css_variables(theme)
        print(css)
    
    # 交互式主题生成示例
    print("\n" + "="*70)
    print("💡 提示：你可以用任何 HEX 颜色生成主题!")
    print("="*70)
    
    # 示例：从图片主色生成主题
    print("\n📸 场景：从品牌 Logo 主色生成完整 UI 主题")
    brand_color = "#FF6B35"  # 假设从 Logo 提取的颜色
    theme = generate_ui_theme(brand_color, "Brand Theme")
    
    print(f"\n品牌色：{brand_color}")
    print(f"\n生成的主色板:")
    for i, color in enumerate(theme['palette']['monochromatic']):
        print(f"  {i+1}. {color}")
    
    print(f"\n互补色（用于 CTA 按钮）: {theme['accent']['main']}")
    
    # 验证所有组合的对比度
    print("\n🔍 关键 UI 组合对比度检查:")
    ui_combinations = [
        ("主按钮", theme['primary']['main'], theme['primary']['text']),
        ("次要按钮", theme['accent']['main'], theme['accent']['text']),
        ("卡片背景", theme['background']['paper'], theme['text']['primary']),
        ("警告提示", theme['status']['warning']['main'], theme['status']['warning']['text']),
    ]
    
    for name, bg, fg in ui_combinations:
        ratio = contrast_ratio(bg, fg)
        aa = is_wcag_aa(bg, fg)
        print(f"  {name}: {ratio:.2f}:1 {'✓' if aa else '✗'}")
    
    print("\n" + "#"*70)
    print("# 示例完成!")
    print("#"*70 + "\n")


if __name__ == "__main__":
    main()
