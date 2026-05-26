"""
Color Utils 使用示例

展示颜色工具的各种应用场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from color_utils.mod import (
    Color, ColorPalette, ColorBlindness, ColorConverter, Colors
)


def example_basic_color_manipulation():
    """示例1: 基础颜色操作"""
    print("\n" + "=" * 50)
    print("示例1: 基础颜色操作")
    print("=" * 50)
    
    # 创建颜色
    orange = Color.from_hex("#FF6B35")
    print(f"原始颜色: {orange.hex}")
    
    # 颜色变体
    print(f"变亮: {orange.lighten(20).hex}")
    print(f"变暗: {orange.darken(20).hex}")
    print(f"增加饱和度: {orange.saturate(20).hex}")
    print(f"降低饱和度: {orange.desaturate(20).hex}")
    print(f"互补色: {orange.complement().hex}")
    print(f"反色: {orange.invert().hex}")
    print(f"灰度: {orange.to_grayscale().hex}")
    
    # 颜色混合
    blue = Color.from_hex("#4ECDC4")
    mixed = orange.mix(blue, 0.5)
    print(f"\n橙色 {orange.hex} + 蓝绿 {blue.hex} = {mixed.hex}")


def example_color_conversion():
    """示例2: 颜色格式转换"""
    print("\n" + "=" * 50)
    print("示例2: 颜色格式转换")
    print("=" * 50)
    
    hex_color = "#3498DB"
    print(f"HEX: {hex_color}")
    
    # 创建颜色对象
    color = Color.from_hex(hex_color)
    
    # 转换为各种格式
    print(f"RGB: rgb{color.rgb}")
    h, s, l = color.hsl
    print(f"HSL: hsl({h:.1f}, {s:.1f}%, {l:.1f}%)")
    h, s, v = color.hsv
    print(f"HSV: hsv({h:.1f}, {s:.1f}%, {v:.1f}%)")
    c, m, y, k = color.cmyk
    print(f"CMYK: cmyk({c:.1f}%, {m:.1f}%, {y:.1f}%, {k:.1f}%)")
    
    # 使用转换器工具函数
    print("\n使用工具函数:")
    print(f"HEX转RGB: {ColorConverter.hex_to_rgb('#E74C3C')}")
    print(f"RGB转HEX: {ColorConverter.rgb_to_hex(231, 76, 60)}")
    print(f"HSL转RGB: {ColorConverter.hsl_to_rgb(210, 100, 60)}")


def example_palette_generation():
    """示例3: 调色板生成"""
    print("\n" + "=" * 50)
    print("示例3: 调色板生成")
    print("=" * 50)
    
    base_color = Color.from_hex("#9B59B6")  # 紫色
    print(f"基础色: {base_color.hex}\n")
    
    # 各种调色板
    print("互补色调色板:")
    for c in ColorPalette.complementary(base_color):
        print(f"  {c.hex}")
    
    print("\n类似色调色板:")
    for c in ColorPalette.analogous(base_color):
        print(f"  {c.hex}")
    
    print("\n三角色调色板:")
    for c in ColorPalette.triadic(base_color):
        print(f"  {c.hex}")
    
    print("\n分裂互补色调色板:")
    for c in ColorPalette.split_complementary(base_color):
        print(f"  {c.hex}")
    
    print("\n单色调色板:")
    for c in ColorPalette.monochromatic(base_color):
        print(f"  {c.hex}")


def example_ui_color_system():
    """示例4: UI颜色系统设计"""
    print("\n" + "=" * 50)
    print("示例4: UI颜色系统设计")
    print("=" * 50)
    
    # 品牌主色
    primary = Color.from_hex("#4A90D9")
    print(f"品牌主色: {primary.hex}")
    
    # 自动生成色阶
    print("\n色阶 (用于UI状态):")
    tints = ColorPalette.tints(primary, 5)
    shades = ColorPalette.shades(primary, 5)
    
    print("  亮色调 (hover等):")
    for i, c in enumerate(tints):
        print(f"    tint-{i+1}: {c.hex}")
    
    print("  暗色调 (active等):")
    for i, c in enumerate(shades):
        print(f"    shade-{i+1}: {c.hex}")
    
    # 状态色
    print("\n状态色示例:")
    success = Color.from_hex("#27AE60")
    warning = Color.from_hex("#F39C12")
    error = Color.from_hex("#E74C3C")
    info = Color.from_hex("#3498DB")
    
    for name, color in [("成功", success), ("警告", warning), ("错误", error), ("信息", info)]:
        text_color = color.best_text_color()
        ratio = color.contrast_ratio(text_color)
        print(f"  {name}: 背景色 {color.hex}, 文字色 {text_color.hex}, 对比度 {ratio:.2f}:1")


def example_accessibility_check():
    """示例5: 无障碍访问检查"""
    print("\n" + "=" * 50)
    print("示例5: 无障碍访问检查")
    print("=" * 50)
    
    # 模拟一个按钮的颜色方案
    backgrounds = [
        ("深蓝按钮", "#1A5276"),
        ("红色警告", "#C0392B"),
        ("绿色成功", "#1E8449"),
        ("浅灰背景", "#ECF0F1"),
        ("深色模式", "#2C3E50"),
    ]
    
    print("按钮文字对比度检查:\n")
    for name, bg_hex in backgrounds:
        bg = Color.from_hex(bg_hex)
        white = Colors.WHITE
        black = Colors.BLACK
        
        white_ratio = bg.contrast_ratio(white)
        black_ratio = bg.contrast_ratio(black)
        
        best = bg.best_text_color()
        compliance = bg.wcag_compliance(best)
        
        print(f"{name} ({bg.hex}):")
        print(f"  白字对比度: {white_ratio:.2f}:1 {'✓' if white_ratio >= 4.5 else '✗'}")
        print(f"  黑字对比度: {black_ratio:.2f}:1 {'✓' if black_ratio >= 4.5 else '✗'}")
        print(f"  推荐文字色: {best.hex}")
        print(f"  WCAG AA合规: {'✓' if compliance['AA_normal'] else '✗'}")
        print()


def example_gradient_generator():
    """示例6: 渐变色生成"""
    print("\n" + "=" * 50)
    print("示例6: 渐变色生成")
    print("=" * 50)
    
    # 线性渐变
    start = Color.from_hex("#FF6B6B")
    end = Color.from_hex("#4ECDC4")
    
    print(f"渐变: {start.hex} -> {end.hex}")
    gradient = ColorPalette.gradient(start, end, 7)
    for i, c in enumerate(gradient):
        print(f"  步骤{i+1}: {c.hex}")
    
    # 多色渐变
    print("\n多色渐变:")
    colors = [
        Color.from_hex("#FF0000"),
        Color.from_hex("#FFFF00"),
        Color.from_hex("#00FF00"),
        Color.from_hex("#00FFFF"),
        Color.from_hex("#0000FF"),
    ]
    multi = ColorPalette.multi_gradient(colors, 3)
    print(f"  彩虹渐变: {[c.hex for c in multi]}")


def example_color_blindness():
    """示例7: 色盲友好设计"""
    print("\n" + "=" * 50)
    print("示例7: 色盲友好设计")
    print("=" * 50)
    
    # 色盲安全调色板
    safe_palette = ColorBlindness.colorblind_safe_palette()
    print("色盲安全调色板 (推荐用于图表):")
    for c in safe_palette:
        print(f"  {c.hex}")
    
    # 检查颜色区分性
    print("\n颜色对区分性检查:")
    red = Color.from_hex("#E74C3C")
    green = Color.from_hex("#2ECC71")
    
    print(f"红色 {red.hex} vs 绿色 {green.hex}:")
    for cb_type in ['protanopia', 'deuteranopia', 'tritanopia']:
        distinguishable = ColorBlindness.is_distinguishable(red, green, cb_type)
        print(f"  {cb_type}: {'可区分 ✓' if distinguishable else '不可区分 ✗'}")
    
    # 色盲模拟
    print(f"\n色盲模拟 (红色 {red.hex}):")
    simulated = ColorBlindness.simulate_all(red)
    for name, color in simulated.items():
        if name != 'normal':
            print(f"  {name}: {color.hex}")


def example_css_color_parser():
    """示例8: CSS颜色解析"""
    print("\n" + "=" * 50)
    print("示例8: CSS颜色解析")
    print("=" * 50)
    
    css_colors = [
        "#FF6B6B",
        "rgb(255, 107, 107)",
        "rgba(255, 107, 107, 0.8)",
        "hsl(0, 100%, 71%)",
        "hsla(0, 100%, 71%, 0.8)",
        "red",
        "coral",
        "turquoise",
    ]
    
    print("解析各种CSS颜色格式:\n")
    for css in css_colors:
        color = ColorConverter.parse_color(css)
        if color:
            print(f"  {css:30} -> {color.hex} {color.rgb}")


def example_random_palette_generation():
    """示例9: 随机调色板生成"""
    print("\n" + "=" * 50)
    print("示例9: 随机调色板生成")
    print("=" * 50)
    
    print("不同风格的随机调色板:\n")
    
    styles = ['pastel', 'vibrant', 'earth', 'cool', 'warm']
    for style in styles:
        palette = ColorPalette.random_palette(5, style)
        print(f"{style.capitalize()}: {[c.hex for c in palette]}")


def example_data_visualization_colors():
    """示例10: 数据可视化配色"""
    print("\n" + "=" * 50)
    print("示例10: 数据可视化配色")
    print("=" * 50)
    
    # 分类数据配色
    print("分类数据配色 (10色):")
    categorical = ColorPalette.random_palette(10, 'vibrant')
    for i, c in enumerate(categorical):
        print(f"  类别{i+1}: {c.hex}")
    
    # 顺序数据配色
    print("\n顺序数据配色 (蓝色系):")
    sequential = ColorPalette.gradient(
        Color.from_hex("#E3F2FD"),
        Color.from_hex("#0D47A1"),
        7
    )
    for i, c in enumerate(sequential):
        print(f"  级别{i+1}: {c.hex}")
    
    # 发散数据配色
    print("\n发散数据配色 (红-白-蓝):")
    diverging = ColorPalette.multi_gradient([
        Color.from_hex("#D32F2F"),
        Color.from_hex("#FFFFFF"),
        Color.from_hex("#1976D2")
    ], 4)
    for i, c in enumerate(diverging):
        print(f"  级别{i+1}: {c.hex}")


def main():
    """运行所有示例"""
    examples = [
        example_basic_color_manipulation,
        example_color_conversion,
        example_palette_generation,
        example_ui_color_system,
        example_accessibility_check,
        example_gradient_generator,
        example_color_blindness,
        example_css_color_parser,
        example_random_palette_generation,
        example_data_visualization_colors,
    ]
    
    print("\n" + "=" * 60)
    print("  Color Utils 使用示例")
    print("=" * 60)
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n示例执行出错: {e}")
    
    print("\n" + "=" * 60)
    print("  示例演示完成!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()