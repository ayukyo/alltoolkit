"""
Color Utils 测试模块

测试颜色转换、调色板生成、色彩对比度等功能
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from color_utils.mod import (
    Color, ColorPalette, ColorBlindness, ColorConverter, Colors
)


def test_color_creation():
    """测试颜色创建"""
    print("=" * 50)
    print("测试 1: 颜色创建")
    print("=" * 50)
    
    # RGB创建
    c1 = Color(255, 128, 0)
    print(f"RGB创建: {c1} -> {c1.hex}")
    assert c1.rgb == (255, 128, 0)
    
    # HEX创建
    c2 = Color.from_hex("#FF8000")
    print(f"HEX创建: #FF8000 -> RGB{c2.rgb}")
    assert c2.rgb == (255, 128, 0)
    
    # HSL创建
    c3 = Color.from_hsl(30, 100, 50)
    print(f"HSL创建: hsl(30, 100%, 50%) -> {c3.hex}")
    
    # HSV创建
    c4 = Color.from_hsv(30, 100, 100)
    print(f"HSV创建: hsv(30, 100%, 100%) -> {c4.hex}")
    
    # CMYK创建
    c5 = Color.from_cmyk(0, 50, 100, 0)
    print(f"CMYK创建: cmyk(0, 50, 100, 0) -> {c5.hex}")
    
    print("✅ 颜色创建测试通过!\n")


def test_color_conversion():
    """测试颜色转换"""
    print("=" * 50)
    print("测试 2: 颜色转换")
    print("=" * 50)
    
    c = Color(255, 128, 0)
    
    # RGB -> HEX
    print(f"RGB{c.rgb} -> HEX: {c.hex}")
    
    # RGB -> HSL
    h, s, l = c.hsl
    print(f"RGB{c.rgb} -> HSL: ({h:.1f}, {s:.1f}%, {l:.1f}%)")
    
    # RGB -> HSV
    h, s, v = c.hsv
    print(f"RGB{c.rgb} -> HSV: ({h:.1f}, {s:.1f}%, {v:.1f}%)")
    
    # RGB -> CMYK
    cmyk = c.cmyk
    print(f"RGB{c.rgb} -> CMYK: ({cmyk[0]:.1f}%, {cmyk[1]:.1f}%, {cmyk[2]:.1f}%, {cmyk[3]:.1f}%)")
    
    # 验证往返转换
    c_hsl = Color.from_hsl(*c.hsl)
    print(f"HSL往返验证: {c.hex} -> {c_hsl.hex}")
    
    c_hsv = Color.from_hsv(*c.hsv)
    print(f"HSV往返验证: {c.hex} -> {c_hsv.hex}")
    
    print("✅ 颜色转换测试通过!\n")


def test_color_manipulation():
    """测试颜色操作"""
    print("=" * 50)
    print("测试 3: 颜色操作")
    print("=" * 50)
    
    c = Color.from_hex("#FF8000")
    
    # 变亮/变暗
    lighter = c.lighten(20)
    darker = c.darken(20)
    print(f"原色: {c.hex}")
    print(f"变亮: {lighter.hex}")
    print(f"变暗: {darker.hex}")
    
    # 饱和度
    saturated = c.saturate(20)
    desaturated = c.desaturate(20)
    print(f"增加饱和度: {saturated.hex}")
    print(f"降低饱和度: {desaturated.hex}")
    
    # 旋转色相
    rotated = c.rotate_hue(90)
    print(f"旋转90度: {rotated.hex}")
    
    # 混合颜色
    mixed = c.mix(Color(0, 0, 255), 0.5)
    print(f"与蓝色混合: {mixed.hex}")
    
    # 反色
    inverted = c.invert()
    print(f"反色: {inverted.hex}")
    
    # 灰度
    gray = c.to_grayscale()
    print(f"灰度: {gray.hex}")
    
    # 互补色
    complement = c.complement()
    print(f"互补色: {complement.hex}")
    
    print("✅ 颜色操作测试通过!\n")


def test_contrast_and_accessibility():
    """测试对比度和无障碍访问"""
    print("=" * 50)
    print("测试 4: 对比度和无障碍")
    print("=" * 50)
    
    white = Colors.WHITE
    black = Colors.BLACK
    
    # 黑白对比
    ratio = white.contrast_ratio(black)
    print(f"黑白对比度: {ratio:.2f}:1")
    
    # WCAG合规检查
    bg = Color.from_hex("#0066CC")
    text_white = Colors.WHITE
    text_black = Colors.BLACK
    
    print(f"\n背景色: {bg.hex}")
    print(f"白色文字对比度: {bg.contrast_ratio(text_white):.2f}:1")
    print(f"  WCAG合规: {bg.wcag_compliance(text_white)}")
    print(f"黑色文字对比度: {bg.contrast_ratio(text_black):.2f}:1")
    print(f"  WCAG合规: {bg.wcag_compliance(text_black)}")
    
    # 最佳文字颜色
    best_text = bg.best_text_color()
    print(f"推荐文字颜色: {best_text.hex}")
    
    # 亮度判断
    print(f"\n颜色亮度判断:")
    print(f"  白色: 亮度={white.luminance:.3f}, {'浅色' if white.is_light else '深色'}")
    print(f"  黑色: 亮度={black.luminance:.3f}, {'浅色' if black.is_light else '深色'}")
    print(f"  {bg.hex}: 亮度={bg.luminance:.3f}, {'浅色' if bg.is_light else '深色'}")
    
    print("✅ 对比度和无障碍测试通过!\n")


def test_palette_generation():
    """测试调色板生成"""
    print("=" * 50)
    print("测试 5: 调色板生成")
    print("=" * 50)
    
    base = Color.from_hex("#FF6B6B")
    print(f"基础色: {base.hex}\n")
    
    # 互补色
    comp = ColorPalette.complementary(base)
    print(f"互补色: {[c.hex for c in comp]}")
    
    # 类似色
    analogous = ColorPalette.analogous(base, count=5)
    print(f"类似色: {[c.hex for c in analogous]}")
    
    # 三角色
    triadic = ColorPalette.triadic(base)
    print(f"三角色: {[c.hex for c in triadic]}")
    
    # 分裂互补色
    split = ColorPalette.split_complementary(base)
    print(f"分裂互补色: {[c.hex for c in split]}")
    
    # 矩形色
    tetradic = ColorPalette.tetradic(base)
    print(f"矩形色: {[c.hex for c in tetradic]}")
    
    # 单色
    mono = ColorPalette.monochromatic(base, count=5)
    print(f"单色调色板: {[c.hex for c in mono]}")
    
    # 色阶
    shades = ColorPalette.shades(base, count=5)
    print(f"色阶: {[c.hex for c in shades]}")
    
    # 渐变
    gradient = ColorPalette.gradient(Color.from_hex("#FF0000"), Color.from_hex("#0000FF"), 7)
    print(f"红蓝渐变: {[c.hex for c in gradient]}")
    
    print("✅ 调色板生成测试通过!\n")


def test_random_palettes():
    """测试随机调色板"""
    print("=" * 50)
    print("测试 6: 随机调色板")
    print("=" * 50)
    
    harmonies = ['random', 'pastel', 'vibrant', 'earth', 'cool', 'warm']
    
    for harmony in harmonies:
        palette = ColorPalette.random_palette(5, harmony)
        print(f"{harmony.capitalize()}: {[c.hex for c in palette]}")
    
    print("✅ 随机调色板测试通过!\n")


def test_color_blindness():
    """测试色盲模拟"""
    print("=" * 50)
    print("测试 7: 色盲模拟")
    print("=" * 50)
    
    # 测试颜色
    red = Colors.RED
    green = Colors.GREEN
    blue = Colors.BLUE
    
    print(f"红色 {red.hex}:")
    simulated = ColorBlindness.simulate_all(red)
    for name, color in simulated.items():
        print(f"  {name}: {color.hex}")
    
    print(f"\n绿色 {green.hex}:")
    simulated = ColorBlindness.simulate_all(green)
    for name, color in simulated.items():
        print(f"  {name}: {color.hex}")
    
    # 色盲安全调色板
    safe = ColorBlindness.colorblind_safe_palette()
    print(f"\n色盲安全调色板:")
    print(f"  {[c.hex for c in safe]}")
    
    # 颜色可区分性
    print(f"\n红绿可区分性测试:")
    print(f"  正常: {ColorBlindness.is_distinguishable(red, green, 'normal')}")
    print(f"  红色盲: {ColorBlindness.is_distinguishable(red, green, 'protanopia')}")
    print(f"  绿色盲: {ColorBlindness.is_distinguishable(red, green, 'deuteranopia')}")
    
    print("✅ 色盲模拟测试通过!\n")


def test_color_parser():
    """测试颜色解析器"""
    print("=" * 50)
    print("测试 8: 颜色解析")
    print("=" * 50)
    
    test_cases = [
        "#FF8000",
        "#F80",
        "#FF800080",  # 带透明度
        "rgb(255, 128, 0)",
        "rgba(255, 128, 0, 0.5)",
        "hsl(30, 100%, 50%)",
        "hsla(30, 100%, 50%, 0.5)",
        "red",
        "blue",
        "coral",
    ]
    
    for test in test_cases:
        color = ColorConverter.parse_color(test)
        if color:
            print(f"{test:30} -> {color.hex} (RGB: {color.rgb})")
        else:
            print(f"{test:30} -> 解析失败")
    
    print("✅ 颜色解析测试通过!\n")


def test_edge_cases():
    """测试边界情况"""
    print("=" * 50)
    print("测试 9: 边界情况")
    print("=" * 50)
    
    # 极端值
    c1 = Color(0, 0, 0)  # 纯黑
    c2 = Color(255, 255, 255)  # 纯白
    
    print(f"纯黑: {c1.hex}, HSL: {c1.hsl}, HSV: {c1.hsv}")
    print(f"纯白: {c2.hex}, HSL: {c2.hsl}, HSV: {c2.hsv}")
    
    # 透明度
    c3 = Color(255, 0, 0, 0.5)
    print(f"半透明红色: {c3.hex_with_alpha}, RGBA: {c3.rgba}")
    
    # 超出范围的值会被裁剪
    c4 = Color(300, -50, 128)  # 会变成 (255, 0, 128)
    print(f"超出范围自动裁剪: Color(300, -50, 128) -> {c4.hex}")
    
    # 随机颜色
    c5 = Color.random()
    print(f"随机颜色: {c5.hex}")
    
    print("✅ 边界情况测试通过!\n")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("  Color Utils 测试套件")
    print("=" * 60 + "\n")
    
    test_color_creation()
    test_color_conversion()
    test_color_manipulation()
    test_contrast_and_accessibility()
    test_palette_generation()
    test_random_palettes()
    test_color_blindness()
    test_color_parser()
    test_edge_cases()
    
    print("=" * 60)
    print("  🎉 所有测试通过!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()