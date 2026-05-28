"""
基本使用示例

展示 ColorName Utils 的基本功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from colorname_utils.mod import (
    get_color_name, get_color_info, get_n_closest_colors,
    RGB, parse_hex, get_color_category, get_brightness, get_temperature
)


def main():
    print("ColorName Utils 基本使用示例")
    print("=" * 50)
    
    # 1. 颜色名称查找
    print("\n1. 颜色名称查找")
    print("-" * 30)
    
    colors = [
        "#FF0000",  # 红色
        "#FFA500",  # 橙色
        "#FFFF00",  # 黄色
        "#00FF00",  # 绿色
        "#00FFFF",  # 青色
        "#0000FF",  # 蓝色
        "#800080",  # 紫色
        "#FFC0CB",  # 粉色
    ]
    
    for hex_color in colors:
        rgb = parse_hex(hex_color)
        name = get_color_name(rgb)
        print(f"  {hex_color} → {name}")
    
    # 2. 颜色详细信息
    print("\n2. 颜色详细信息")
    print("-" * 30)
    
    rgb = RGB(255, 165, 0)  # 橙色
    info = get_color_info(rgb)
    
    print(f"  RGB: {info.rgb}")
    print(f"  名称: {info.name}")
    print(f"  十六进制: {info.hex}")
    print(f"  HSL: {info.hsl}")
    print(f"  类别: {info.category}")
    print(f"  亮度: {info.brightness}")
    print(f"  温度: {info.temperature}")
    
    # 3. 最近颜色匹配
    print("\n3. 最近颜色匹配")
    print("-" * 30)
    
    # 一个不在数据库中的颜色
    custom_color = RGB(255, 100, 50)
    matches = get_n_closest_colors(custom_color, 5)
    
    print(f"  颜色 {custom_color.to_hex()} 最接近的颜色:")
    for m in matches:
        print(f"    {m.name}: {m.hex} (距离: {m.distance:.2f})")
    
    # 4. 颜色分类
    print("\n4. 颜色分类")
    print("-" * 30)
    
    test_colors = [
        RGB(255, 0, 0),      # 红
        RGB(255, 165, 0),    # 橙
        RGB(255, 255, 0),    # 黄
        RGB(0, 255, 0),      # 绿
        RGB(0, 255, 255),    # 青
        RGB(0, 0, 255),      # 蓝
        RGB(128, 0, 128),    # 紫
        RGB(0, 0, 0),        # 黑
        RGB(255, 255, 255),  # 白
        RGB(128, 128, 128),  # 灰
    ]
    
    for c in test_colors:
        cat = get_color_category(c)
        bright = get_brightness(c)
        temp = get_temperature(c)
        print(f"  {c.to_hex()} → 类别: {cat}, 亮度: {bright}, 温度: {temp}")


if __name__ == "__main__":
    main()