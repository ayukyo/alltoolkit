"""
颜色和谐示例

展示如何使用 ColorName Utils 生成颜色方案。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from colorname_utils.mod import (
    RGB, parse_hex,
    complementary_color, analogous_colors, triadic_colors,
    split_complementary_colors, tetradic_colors,
    get_color_name
)


def print_colors(title: str, colors: list):
    """打印颜色列表"""
    print(f"\n{title}")
    for c in colors:
        name = get_color_name(c)
        print(f"  {c.to_hex()} → {name}")


def main():
    print("ColorName Utils 颜色和谐示例")
    print("=" * 50)
    
    # 基础颜色
    base_color = parse_hex("#3498DB")  # 蓝色
    print(f"\n基础颜色: {base_color.to_hex()} → {get_color_name(base_color)}")
    
    # 互补色 - 色轮上 180 度对面
    comp = complementary_color(base_color)
    print_colors("互补色", [base_color, comp])
    
    # 类似色 - 色轮上相邻的颜色（±30 度）
    analogs = analogous_colors(base_color)
    print_colors("类似色", analogs)
    
    # 三角色 - 色轮上 120 度间隔
    triadic = triadic_colors(base_color)
    print_colors("三角色", triadic)
    
    # 分裂互补色 - 互补色 ±30 度
    split = split_complementary_colors(base_color)
    print_colors("分裂互补色", split)
    
    # 四角色 - 色轮上 90 度间隔
    tetra = tetradic_colors(base_color)
    print_colors("四角色", tetra)
    
    # 实际应用：为品牌生成配色方案
    print("\n" + "=" * 50)
    print("实际应用：品牌配色方案")
    print("-" * 30)
    
    # 品牌主色
    brand_color = parse_hex("#E74C3C")  # 红色
    print(f"主色: {brand_color.to_hex()} → {get_color_name(brand_color)}")
    
    # 生成配色方案
    scheme = split_complementary_colors(brand_color)
    print("\n配色方案:")
    for i, c in enumerate(scheme, 1):
        name = get_color_name(c)
        print(f"  颜色 {i}: {c.to_hex()} → {name}")
    
    # 变亮变暗版本
    from colorname_utils.mod import lighten, darken
    
    light = lighten(brand_color, 20)
    dark = darken(brand_color, 20)
    print("\n亮度变化:")
    print(f"  浅色: {light.to_hex()} → {get_color_name(light)}")
    print(f"  主色: {brand_color.to_hex()} → {get_color_name(brand_color)}")
    print(f"  深色: {dark.to_hex()} → {get_color_name(dark)}")


if __name__ == "__main__":
    main()