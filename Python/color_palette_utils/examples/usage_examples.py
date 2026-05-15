"""
Color Palette Utils - 使用示例

演示颜色操作、调色板生成、渐变等功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Color, RGB, HSL, HSV, CMYK, LAB,
    ColorPalette, Gradient, ColorUtils,
    hex_to_rgb, rgb_to_hex, hex_to_hsl, hsl_to_hex,
    random_color, random_palette, complementary,
    lighten, darken, contrast_ratio, gradient, palette
)


def example_color_creation():
    """示例：颜色创建方式"""
    print("=" * 60)
    print("示例：颜色创建方式")
    print("=" * 60)
    
    # 从 HEX 创建
    c1 = Color.from_hex("#ff6b6b")
    print(f"从 HEX 创建: {c1}")
    
    # 从 RGB 创建
    c2 = Color.from_rgb(78, 205, 196)
    print(f"从 RGB 创建: {c2}")
    
    # 从 HSL 创建
    c3 = Color.from_hsl(180, 70, 50)
    print(f"从 HSL 创建: {c3}")
    
    # 从 HSV 创建
    c4 = Color.from_hsv(300, 80, 90)
    print(f"从 HSV 创建: {c4}")
    
    # 从 CMYK 创建
    c5 = Color.from_cmyk(100, 0, 0, 0)
    print(f"从 CMYK 创建 (青色): {c5}")
    
    # 从颜色名称创建
    c6 = ColorUtils.from_name("coral")
    print(f"从名称创建: {c6}")
    
    # 随机颜色
    c7 = random_color()
    print(f"随机颜色: {c7}")
    
    print()


def example_color_conversion():
    """示例：颜色空间转换"""
    print("=" * 60)
    print("示例：颜色空间转换")
    print("=" * 60)
    
    color = Color.from_hex("#ff6b6b")
    print(f"原始颜色: {color}")
    
    # RGB
    print(f"RGB: rgb({color.rgb.r}, {color.rgb.g}, {color.rgb.b})")
    
    # HSL
    print(f"HSL: hsl({color.hsl.h:.1f}, {color.hsl.s:.1f}%, {color.hsl.l:.1f}%)")
    
    # HSV
    print(f"HSV: hsv({color.hsv.h:.1f}, {color.hsv.s:.1f}%, {color.hsv.v:.1f}%)")
    
    # CMYK
    print(f"CMYK: cmyk({color.cmyk.c:.1f}%, {color.cmyk.m:.1f}%, {color.cmyk.y:.1f}%, {color.cmyk.k:.1f}%)")
    
    # LAB
    print(f"LAB: lab({color.lab.L:.1f}, {color.lab.a:.1f}, {color.lab.b:.1f})")
    
    # 亮度
    print(f"相对亮度: {color.luminance:.4f}")
    
    print()


def example_color_manipulation():
    """示例：颜色操作"""
    print("=" * 60)
    print("示例：颜色操作")
    print("=" * 60)
    
    base = Color.from_hex("#ff6b6b")
    print(f"基础颜色: {base}")
    
    # 变亮
    lighter = base.lighten(20)
    print(f"变亮 20%: {lighter}")
    
    # 变暗
    darker = base.darken(20)
    print(f"变暗 20%: {darker}")
    
    # 增加饱和度
    more_saturated = base.saturate(30)
    print(f"增加饱和度 30%: {more_saturated}")
    
    # 降低饱和度
    less_saturated = base.desaturate(30)
    print(f"降低饱和度 30%: {less_saturated}")
    
    # 灰度
    gray = base.grayscale()
    print(f"灰度: {gray}")
    
    # 反转
    inverted = base.invert()
    print(f"反转: {inverted}")
    
    # 旋转色相 60 度
    rotated = base.rotate(60)
    print(f"旋转色相 60°: {rotated}")
    
    # 混合两种颜色
    other = Color.from_hex("#4ecdc4")
    mixed = base.mix(other, 0.5)
    print(f"混合 {base} 和 {other}: {mixed}")
    
    print()


def example_color_harmony():
    """示例：色彩和谐"""
    print("=" * 60)
    print("示例：色彩和谐")
    print("=" * 60)
    
    base = Color.from_hex("#ff6b6b")
    print(f"基础颜色: {base}")
    
    # 互补色
    comp = base.complementary()
    print(f"互补色: {comp}")
    
    # 类似色
    analogous = base.analogous()
    print(f"类似色: {[str(c) for c in analogous]}")
    
    # 三色
    triadic = base.triadic()
    print(f"三色组合: {[str(c) for c in triadic]}")
    
    # 四色
    tetradic = base.tetradic()
    print(f"四色组合: {[str(c) for c in tetradic]}")
    
    # 分裂互补
    split = base.split_complementary()
    print(f"分裂互补: {[str(c) for c in split]}")
    
    # 双互补
    double = base.double_complementary()
    print(f"双互补: {[str(c) for c in double]}")
    
    print()


def example_contrast():
    """示例：对比度计算"""
    print("=" * 60)
    print("示例：对比度计算 (WCAG)")
    print("=" * 60)
    
    # 常见背景色
    backgrounds = [
        ("白色", "#ffffff"),
        ("黑色", "#000000"),
        ("深灰", "#333333"),
        ("浅灰", "#f0f0f0"),
        ("深蓝", "#1a1a2e"),
    ]
    
    text_color = Color.from_hex("#ff6b6b")
    print(f"文本颜色: {text_color}\n")
    
    for name, bg_hex in backgrounds:
        bg = Color.from_hex(bg_hex)
        ratio = text_color.contrast_ratio(bg)
        level = text_color.wcag_level(bg)
        level_large = text_color.wcag_level(bg, large_text=True)
        print(f"{name} ({bg_hex}):")
        print(f"  对比度: {ratio:.2f}:1")
        print(f"  普通文本: {level} | 大文本: {level_large}")
    
    # 推荐文本颜色
    print(f"\n在 {text_color} 上推荐使用: {text_color.readable_text_color()}")
    
    print()


def example_color_blindness():
    """示例：色盲模拟"""
    print("=" * 60)
    print("示例：色盲模拟")
    print("=" * 60)
    
    colors = [
        ("红色", "#ff0000"),
        ("绿色", "#00ff00"),
        ("蓝色", "#0000ff"),
        ("黄色", "#ffff00"),
        ("紫色", "#800080"),
    ]
    
    print("原始颜色 -> 红色盲 -> 绿色盲 -> 蓝色盲")
    print("-" * 60)
    
    for name, hex_color in colors:
        c = Color.from_hex(hex_color)
        proto = c.simulate_protanopia()
        deuter = c.simulate_deuteranopia()
        tritan = c.simulate_tritanopia()
        print(f"{name:6} {hex_color} -> {proto} -> {deuter} -> {tritan}")
    
    print()


def example_palettes():
    """示例：调色板生成"""
    print("=" * 60)
    print("示例：调色板生成")
    print("=" * 60)
    
    base = "#ff6b6b"
    print(f"基础颜色: {base}\n")
    
    # 各种配色方案
    schemes = [
        ("互补色", "complementary"),
        ("类似色", "analogous"),
        ("三色", "triadic"),
        ("四色", "tetradic"),
        ("分裂互补", "split_complementary"),
        ("双互补", "double_complementary"),
    ]
    
    for name, scheme in schemes:
        pal = ColorPalette.from_base_color(base, scheme)
        print(f"{name}: {pal.to_hex_list()}")
    
    print()
    
    # 渐变调色板
    gradient_pal = ColorPalette.gradient("#ff6b6b", "#4ecdc4", 5)
    print(f"渐变 (5 步): {gradient_pal.to_hex_list()}")
    
    # 彩虹调色板
    rainbow = ColorPalette.rainbow(6)
    print(f"彩虹 (6 色): {rainbow.to_hex_list()}")
    
    # 单色调色板
    mono = ColorPalette.monochromatic(base, 5)
    print(f"单色 (5 阶): {mono.to_hex_list()}")
    
    # 色阶
    shades = ColorPalette.shades(base, 5)
    print(f"色阶 (5 阶): {shades.to_hex_list()}")
    
    # 温度调色板
    warm = ColorPalette.from_temperature("warm", 5)
    print(f"暖色调: {warm.to_hex_list()}")
    
    cool = ColorPalette.from_temperature("cool", 5)
    print(f"冷色调: {cool.to_hex_list()}")
    
    # 随机调色板
    random_pal = random_palette(5)
    print(f"随机 (5 色): {random_pal.to_hex_list()}")
    
    print()


def example_gradient():
    """示例：渐变生成"""
    print("=" * 60)
    print("示例：渐变生成")
    print("=" * 60)
    
    # 简单渐变
    print("简单渐变 (红 -> 蓝):")
    grad = Gradient.linear("#ff0000", "#0000ff")
    for i in range(10):
        pos = i / 9
        color = grad.color_at(pos)
        print(f"  {pos:.0%}: {color}")
    
    print()
    
    # 多停止点渐变
    print("多停止点渐变 (彩虹):")
    rainbow_grad = Gradient.multi_stop([
        "#ff0000",  # 红
        "#ffff00",  # 黄
        "#00ff00",  # 绿
        "#00ffff",  # 青
        "#0000ff",  # 蓝
        "#ff00ff",  # 紫
    ])
    for i in range(6):
        pos = i / 5
        color = rainbow_grad.color_at(pos)
        print(f"  {pos:.0%}: {color}")
    
    print()
    
    # 转换为调色板
    print("渐变转调色板 (7 步):")
    pal = grad.to_palette(7)
    print(f"  {pal.to_hex_list()}")
    
    print()


def example_color_utils():
    """示例：工具函数"""
    print("=" * 60)
    print("示例：工具函数")
    print("=" * 60)
    
    # 解析各种格式
    print("解析颜色:")
    print(f"  HEX: {ColorUtils.parse('#ff6b6b')}")
    print(f"  名称: {ColorUtils.parse('coral')}")
    print(f"  RGB 元组: {ColorUtils.parse((255, 107, 107))}")
    
    print()
    
    # 混合多种颜色
    print("混合多种颜色:")
    blended = ColorUtils.blend(["#ff0000", "#00ff00", "#0000ff"])
    print(f"  红 + 绿 + 蓝 = {blended}")
    
    print()
    
    # 颜色比较
    print("颜色比较:")
    red = Color.from_hex("#ff0000")
    similar_red = Color.from_hex("#fe0101")
    blue = Color.from_hex("#0000ff")
    
    print(f"  #ff0000 与 #fe0101 距离: {ColorUtils.color_distance(red, similar_red):.2f}")
    print(f"  #ff0000 与 #0000ff 距离: {ColorUtils.color_distance(red, blue):.2f}")
    
    print()
    
    # 最接近的颜色
    print("查找最接近的颜色:")
    candidates = ["#ff0000", "#00ff00", "#0000ff", "#ffff00"]
    target = "#ff0001"
    closest = ColorUtils.closest_color(target, candidates)
    print(f"  最接近 {target} 的颜色是: {closest}")
    
    print()
    
    # 排序颜色
    print("排序颜色:")
    unsorted = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff"]
    sorted_colors = ColorUtils.sort_by_hue(unsorted)
    print(f"  按色相排序: {[str(c) for c in sorted_colors]}")
    
    print()


def example_ux_design():
    """示例：UI/UX 设计场景"""
    print("=" * 60)
    print("示例：UI/UX 设计场景")
    print("=" * 60)
    
    # 场景1：生成按钮颜色
    print("场景1：按钮颜色方案")
    primary = Color.from_hex("#3498db")
    print(f"主色: {primary}")
    print(f"悬停色 (变亮): {primary.lighten(10)}")
    print(f"按下色 (变暗): {primary.darken(10)}")
    print(f"禁用色 (降低饱和度): {primary.desaturate(50)}")
    
    print()
    
    # 场景2：确保文字可读性
    print("场景2：确保文字可读性")
    background = Color.from_hex("#2c3e50")
    text_color = background.readable_text_color()
    print(f"背景色: {background}")
    print(f"推荐文字色: {text_color}")
    print(f"对比度: {background.contrast_ratio(text_color):.2f}:1")
    print(f"WCAG 等级: {background.wcag_level(text_color)}")
    
    print()
    
    # 场景3：生成配色方案
    print("场景3：网站配色方案")
    brand_color = "#e74c3c"
    scheme = ColorPalette.from_base_color(brand_color, "tetradic")
    print(f"品牌色: {brand_color}")
    print(f"完整配色方案: {scheme.to_hex_list()}")
    
    print()
    
    # 场景4：色盲友好的调色板
    print("场景4：色盲友好检查")
    palette_colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00"]
    print("原始调色板:", palette_colors)
    print("红色盲视图:")
    for hex_c in palette_colors:
        c = Color.from_hex(hex_c)
        print(f"  {hex_c} -> {c.simulate_protanopia()}")
    
    print()


def example_data_visualization():
    """示例：数据可视化配色"""
    print("=" * 60)
    print("示例：数据可视化配色")
    print("=" * 60)
    
    # 分类数据调色板
    print("分类数据调色板 (10 类):")
    categorical = ColorPalette.rainbow(10, saturation=70, lightness=50)
    for i, color in enumerate(categorical):
        print(f"  类别 {i+1}: {color}")
    
    print()
    
    # 序列数据调色板
    print("序列数据调色板 (蓝色渐变):")
    sequential = ColorPalette.gradient("#f7fbff", "#08306b", 7)
    for i, color in enumerate(sequential):
        print(f"  级别 {i+1}: {color}")
    
    print()
    
    # 发散数据调色板
    print("发散数据调色板 (红-白-蓝):")
    diverging = Gradient.multi_stop(["#b2182b", "#f7f7f7", "#2166ac"])
    for i in range(7):
        pos = i / 6
        color = diverging.color_at(pos)
        print(f"  级别 {i+1}: {color}")
    
    print()


def example_quick_functions():
    """示例：便捷函数"""
    print("=" * 60)
    print("示例：便捷函数")
    print("=" * 60)
    
    # 快速转换
    print("快速转换:")
    print(f"  HEX -> RGB: hex_to_rgb('#ff6b6b') = {hex_to_rgb('#ff6b6b')}")
    print(f"  RGB -> HEX: rgb_to_hex(255, 107, 107) = {rgb_to_hex(255, 107, 107)}")
    print(f"  HEX -> HSL: hex_to_hsl('#ff6b6b') = {hex_to_hsl('#ff6b6b')}")
    print(f"  HSL -> HEX: hsl_to_hex(0, 100, 100) = {hsl_to_hex(0, 100, 100)}")
    
    print()
    
    # 快速操作
    print("快速操作:")
    print(f"  互补色: complementary('#ff6b6b') = {complementary('#ff6b6b')}")
    print(f"  变亮: lighten('#666666', 30) = {lighten('#666666', 30)}")
    print(f"  变暗: darken('#666666', 30) = {darken('#666666', 30)}")
    print(f"  对比度: contrast_ratio('#000000', '#ffffff') = {contrast_ratio('#000000', '#ffffff'):.1f}")
    
    print()
    
    # 快速生成
    print("快速生成:")
    print(f"  渐变: gradient('#ff0000', '#0000ff', 5) = {gradient('#ff0000', '#0000ff', 5)}")
    print(f"  三色: palette('#ff6b6b', 'triadic') = {palette('#ff6b6b', 'triadic')}")
    
    print()


def main():
    """运行所有示例"""
    example_color_creation()
    example_color_conversion()
    example_color_manipulation()
    example_color_harmony()
    example_contrast()
    example_color_blindness()
    example_palettes()
    example_gradient()
    example_color_utils()
    example_ux_design()
    example_data_visualization()
    example_quick_functions()
    
    print("=" * 60)
    print("✓ 示例演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()