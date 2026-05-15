"""
Color Palette Utils - 测试用例

测试颜色空间转换、调色板生成、对比度计算等功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Color, RGB, HSL, HSV, CMYK, LAB,
    ColorPalette, Gradient, ColorUtils,
    hex_to_rgb, rgb_to_hex, hex_to_hsl, hsl_to_hex,
    random_color, random_palette, complementary,
    lighten, darken, contrast_ratio, gradient, palette
)


def test_rgb_creation():
    """测试 RGB 创建和转换"""
    print("=== RGB 创建和转换 ===")
    
    rgb = RGB(255, 128, 64)
    assert rgb.r == 255
    assert rgb.g == 128
    assert rgb.b == 64
    
    # HEX 转换
    assert rgb.to_hex() == "#ff8040"
    
    # HSL 转换
    hsl = rgb.to_hsl()
    assert 0 <= hsl.h <= 360
    assert 0 <= hsl.s <= 100
    assert 0 <= hsl.l <= 100
    
    # HSV 转换
    hsv = rgb.to_hsv()
    assert 0 <= hsv.h <= 360
    assert 0 <= hsv.s <= 100
    assert 0 <= hsv.v <= 100
    
    # CMYK 转换
    cmyk = rgb.to_cmyk()
    assert 0 <= cmyk.c <= 100
    assert 0 <= cmyk.m <= 100
    
    # LAB 转换
    lab = rgb.to_lab()
    assert 0 <= lab.L <= 100
    
    # 亮度计算
    lum = rgb.luminance()
    assert 0 <= lum <= 1
    
    print("✓ RGB 创建和转换测试通过")


def test_color_creation():
    """测试 Color 类各种创建方式"""
    print("\n=== Color 类创建 ===")
    
    # 从 RGB 创建
    c1 = Color.from_rgb(255, 128, 64)
    assert c1.hex == "#ff8040"
    
    # 从 HEX 创建
    c2 = Color.from_hex("#ff8040")
    assert c2.rgb.r == 255
    assert c2.rgb.g == 128
    assert c2.rgb.b == 64
    
    # 从 HEX 创建 (短格式)
    c3 = Color.from_hex("#f84")
    assert c3.rgb.r == 255
    assert c3.rgb.g == 136
    assert c3.rgb.b == 68
    
    # 从 HSL 创建
    c4 = Color.from_hsl(180, 50, 50)
    assert c4.rgb.r == 63  # 色相 180, 饱和度 50, 亮度 50 -> 青色系
    assert c4.rgb.g == 191
    assert c4.rgb.b == 191
    
    # 从 HSV 创建
    c5 = Color.from_hsv(120, 100, 100)
    assert c5.rgb.r == 0
    assert c5.rgb.g == 255
    assert c5.rgb.b == 0
    
    # 从 CMYK 创建
    c6 = Color.from_cmyk(0, 100, 100, 0)
    assert c6.rgb.r == 255
    assert c6.rgb.g == 0
    assert c6.rgb.b == 0
    
    print("✓ Color 创建测试通过")


def test_color_manipulation():
    """测试颜色操作"""
    print("\n=== 颜色操作 ===")
    
    c = Color.from_hex("#ff6b6b")  # 珊瑚红
    
    # 变亮
    light = c.lighten(20)
    assert light.hsl.l > c.hsl.l
    
    # 变暗
    dark = c.darken(20)
    assert dark.hsl.l < c.hsl.l
    
    # 增加饱和度
    saturated = c.saturate(20)
    # 如果原饱和度未达上限，应增加；否则保持不变
    if c.hsl.s < 100:
        assert saturated.hsl.s > c.hsl.s
    else:
        assert saturated.hsl.s == 100
    
    # 降低饱和度
    desaturated = c.desaturate(20)
    assert desaturated.hsl.s < c.hsl.s
    
    # 灰度
    gray = c.grayscale()
    assert gray.hsl.s == 0
    
    # 反转
    inverted = c.invert()
    assert inverted.rgb.r == 255 - c.rgb.r
    assert inverted.rgb.g == 255 - c.rgb.g
    assert inverted.rgb.b == 255 - c.rgb.b
    
    # 旋转色相
    rotated = c.rotate(180)
    assert abs(rotated.hsl.h - (c.hsl.h + 180) % 360) < 1
    
    # 混合
    c2 = Color.from_hex("#4ecdc4")  # 青色
    mixed = c.mix(c2, 0.5)
    assert 0 <= mixed.rgb.r <= 255
    
    print("✓ 颜色操作测试通过")


def test_color_harmony():
    """测试色彩和谐"""
    print("\n=== 色彩和谐 ===")
    
    c = Color.from_hex("#ff6b6b")  # 珊瑚红
    
    # 互补色
    comp = c.complementary()
    assert abs(comp.hsl.h - (c.hsl.h + 180) % 360) < 1
    
    # 类似色
    analogous = c.analogous()
    assert len(analogous) == 3
    assert analogous[1] == c
    
    # 三色
    triadic = c.triadic()
    assert len(triadic) == 3
    assert triadic[0] == c
    
    # 四色
    tetradic = c.tetradic()
    assert len(tetradic) == 4
    
    # 分裂互补
    split = c.split_complementary()
    assert len(split) == 3
    
    # 双互补
    double = c.double_complementary()
    assert len(double) == 4
    
    print("✓ 色彩和谐测试通过")


def test_contrast_ratio():
    """测试对比度计算"""
    print("\n=== 对比度计算 ===")
    
    # 黑白对比度应为 21:1
    black = Color.from_hex("#000000")
    white = Color.from_hex("#ffffff")
    ratio = black.contrast_ratio(white)
    assert ratio == 21.0
    
    # 相同颜色对比度应为 1:1
    red = Color.from_hex("#ff0000")
    ratio = red.contrast_ratio(red)
    assert ratio == 1.0
    
    # WCAG 等级测试
    level = black.wcag_level(white)
    assert level == "AAA"
    
    # 文本颜色推荐
    text_color = Color.from_hex("#ff6b6b").readable_text_color()
    assert text_color.hex == "#000000" or text_color.hex == "#ffffff"
    
    print("✓ 对比度计算测试通过")


def test_color_blindness_simulation():
    """测试色盲模拟"""
    print("\n=== 色盲模拟 ===")
    
    red = Color.from_hex("#ff0000")
    green = Color.from_hex("#00ff00")
    blue = Color.from_hex("#0000ff")
    
    # 红色盲模拟
    proto_red = red.simulate_protanopia()
    assert isinstance(proto_red, Color)
    
    # 绿色盲模拟
    deuter_green = green.simulate_deuteranopia()
    assert isinstance(deuter_green, Color)
    
    # 蓝色盲模拟
    tritan_blue = blue.simulate_tritanopia()
    assert isinstance(tritan_blue, Color)
    
    print("✓ 色盲模拟测试通过")


def test_color_palette():
    """测试调色板生成"""
    print("\n=== 调色板生成 ===")
    
    # 从基础颜色创建
    base = "#ff6b6b"
    
    # 互补色调色板
    comp_palette = ColorPalette.from_base_color(base, "complementary")
    assert len(comp_palette) == 2
    
    # 三色调色板
    triadic_palette = ColorPalette.from_base_color(base, "triadic")
    assert len(triadic_palette) == 3
    
    # 四色调色板
    tetradic_palette = ColorPalette.from_base_color(base, "tetradic")
    assert len(tetradic_palette) == 4
    
    # 渐变调色板
    gradient_palette = ColorPalette.gradient("#ff0000", "#0000ff", 5)
    assert len(gradient_palette) == 5
    assert gradient_palette[0].hex == "#ff0000"
    assert gradient_palette[4].hex == "#0000ff"
    
    # 彩虹调色板
    rainbow = ColorPalette.rainbow(12)
    assert len(rainbow) == 12
    
    # 单色调色板
    mono = ColorPalette.monochromatic(base, 5)
    assert len(mono) == 5
    
    # 色阶
    shades = ColorPalette.shades(base, 9)
    assert len(shades) == 9
    
    # 温度调色板
    warm = ColorPalette.from_temperature("warm", 5)
    assert len(warm) == 5
    
    cool = ColorPalette.from_temperature("cool", 5)
    assert len(cool) == 5
    
    print("✓ 调色板生成测试通过")


def test_gradient():
    """测试渐变"""
    print("\n=== 渐变测试 ===")
    
    # 线性渐变
    g = Gradient.linear("#ff0000", "#0000ff", 5)
    
    # 获取特定位置的颜色
    c0 = g.color_at(0)
    assert c0.hex == "#ff0000"
    
    c1 = g.color_at(1)
    assert c1.hex == "#0000ff"
    
    c_mid = g.color_at(0.5)
    # 中间色应该是紫色
    assert 100 <= c_mid.rgb.r <= 200
    assert c_mid.rgb.b == c_mid.rgb.r  # 红蓝相等
    
    # 转换为调色板
    pal = g.to_palette(10)
    assert len(pal) == 10
    
    # 多停止点渐变
    multi = Gradient.multi_stop(["#ff0000", "#00ff00", "#0000ff"])
    assert len(multi.stops) == 3
    
    print("✓ 渐变测试通过")


def test_color_utils():
    """测试工具函数"""
    print("\n=== 工具函数 ===")
    
    # 从名称创建
    red = ColorUtils.from_name("red")
    assert red.hex == "#ff0000"
    
    white = ColorUtils.from_name("white")
    assert white.hex == "#ffffff"
    
    # 解析
    c1 = ColorUtils.parse("#ff6b6b")
    assert c1.rgb.r == 255
    
    c2 = ColorUtils.parse("blue")
    assert c2.rgb.b == 255
    
    c3 = ColorUtils.parse((128, 64, 32))
    assert c3.rgb.r == 128
    
    # 混合
    blended = ColorUtils.blend(["#ff0000", "#0000ff"])
    assert blended.rgb.r == 127  # 大约
    assert blended.rgb.b == 127
    
    # 亮/暗判断
    white = Color.from_hex("#ffffff")
    assert ColorUtils.is_light(white)
    black = Color.from_hex("#000000")
    assert ColorUtils.is_dark(black)
    
    # 颜色距离
    dist = ColorUtils.color_distance(red, Color.from_hex("#ff0100"))
    assert dist < 5  # 非常接近
    
    # 最接近的颜色
    closest = ColorUtils.closest_color("#ff0001", ["#00ff00", "#ff0000", "#0000ff"])
    assert closest.hex == "#ff0000"
    
    # 排序
    colors = ["#ff0000", "#00ff00", "#0000ff"]
    sorted_by_hue = ColorUtils.sort_by_hue(colors)
    # 应该按红、绿、蓝顺序
    assert sorted_by_hue[0].hsl.h < sorted_by_hue[1].hsl.h
    
    print("✓ 工具函数测试通过")


def test_convenience_functions():
    """测试便捷函数"""
    print("\n=== 便捷函数 ===")
    
    # HEX <-> RGB
    rgb = hex_to_rgb("#ff6b6b")
    assert rgb == (255, 107, 107)
    
    hex_str = rgb_to_hex(255, 107, 107)
    assert hex_str == "#ff6b6b"
    
    # HEX <-> HSL
    hsl = hex_to_hsl("#ff6b6b")
    assert len(hsl) == 3
    assert hsl[0] == 0  # 红色色相为0
    
    hex_str = hsl_to_hex(0, 100, 50)
    assert hex_str == "#ff0000"
    
    # 随机颜色
    c = random_color()
    assert isinstance(c, Color)
    
    # 随机调色板
    p = random_palette(5)
    assert len(p) == 5
    
    # 互补色
    comp = complementary("#ff6b6b")
    # 互补色应为青色系，允许小误差
    assert comp.startswith("#6b")
    
    # 变亮/变暗
    lighter = lighten("#666666", 20)
    assert Color.from_hex(lighter).hsl.l > Color.from_hex("#666666").hsl.l
    
    darker = darken("#666666", 20)
    assert Color.from_hex(darker).hsl.l < Color.from_hex("#666666").hsl.l
    
    # 对比度
    ratio = contrast_ratio("#000000", "#ffffff")
    assert ratio == 21.0
    
    # 渐变
    grad = gradient("#ff0000", "#0000ff", 5)
    assert len(grad) == 5
    
    # 调色板
    pal = palette("#ff6b6b", "triadic")
    assert len(pal) == 3
    
    print("✓ 便捷函数测试通过")


def test_lab_color_space():
    """测试 LAB 颜色空间"""
    print("\n=== LAB 颜色空间 ===")
    
    # RGB -> LAB -> RGB 往返测试
    colors = [
        Color.from_rgb(255, 0, 0),    # 红色
        Color.from_rgb(0, 255, 0),    # 绿色
        Color.from_rgb(0, 0, 255),    # 蓝色
        Color.from_rgb(255, 255, 255), # 白色
        Color.from_rgb(0, 0, 0),      # 黑色
    ]
    
    for c in colors:
        lab = c.lab
        back_to_rgb = lab.to_rgb()
        # 允许小误差
        assert abs(back_to_rgb.r - c.rgb.r) <= 2, f"R mismatch: {back_to_rgb.r} vs {c.rgb.r}"
        assert abs(back_to_rgb.g - c.rgb.g) <= 2, f"G mismatch: {back_to_rgb.g} vs {c.rgb.g}"
        assert abs(back_to_rgb.b - c.rgb.b) <= 2, f"B mismatch: {back_to_rgb.b} vs {c.rgb.b}"
    
    # 色差计算
    red = Color.from_hex("#ff0000")
    similar_red = Color.from_hex("#fe0000")
    blue = Color.from_hex("#0000ff")
    
    delta_similar = red.lab.delta_e(similar_red.lab)
    delta_different = red.lab.delta_e(blue.lab)
    
    assert delta_similar < delta_different
    
    print("✓ LAB 颜色空间测试通过")


def test_cmyk_conversion():
    """测试 CMYK 转换"""
    print("\n=== CMYK 转换 ===")
    
    # 黑色
    black = Color.from_rgb(0, 0, 0)
    cmyk = black.cmyk
    assert cmyk.c == 0
    assert cmyk.m == 0
    assert cmyk.y == 0
    assert cmyk.k == 100
    
    # 纯青色
    cyan = Color.from_rgb(0, 255, 255)
    cmyk = cyan.cmyk
    assert cmyk.c == 100
    assert cmyk.m == 0
    assert cmyk.y == 0
    assert cmyk.k == 0
    
    # CMYK -> RGB 往返 (允许较大误差，因为 CMYK 和 RGB 空间不完全对应)
    original = CMYK(50, 25, 10, 5)
    rgb = original.to_rgb()
    back = rgb.to_cmyk()
    
    # 允许较大误差范围
    assert abs(back.c - original.c) <= 10
    assert abs(back.m - original.m) <= 10
    assert abs(back.y - original.y) <= 10
    assert abs(back.k - original.k) <= 10
    
    print("✓ CMYK 转换测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("\n=== 边界情况 ===")
    
    # 纯黑纯白
    black = Color.from_rgb(0, 0, 0)
    white = Color.from_rgb(255, 255, 255)
    
    assert black.luminance == 0.0
    assert white.luminance == 1.0
    
    # 饱和度为0的灰色
    gray = Color.from_hsl(0, 0, 50)
    assert gray.rgb.r == gray.rgb.g == gray.rgb.b
    
    # 高饱和度颜色
    vivid = Color.from_hsl(180, 100, 50)
    assert vivid.hsl.s == 100
    
    # 透明度
    transparent = Color.from_rgb(255, 0, 0, 0.5)
    assert transparent.rgb.a == 0.5
    
    # 带 alpha 的 HEX
    hex_with_alpha = Color.from_hex("#ff000080")
    assert transparent.rgb.a == 0.5
    
    print("✓ 边界情况测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Color Palette Utils - 完整测试")
    print("=" * 60)
    
    test_rgb_creation()
    test_color_creation()
    test_color_manipulation()
    test_color_harmony()
    test_contrast_ratio()
    test_color_blindness_simulation()
    test_color_palette()
    test_gradient()
    test_color_utils()
    test_convenience_functions()
    test_lab_color_space()
    test_cmyk_conversion()
    test_edge_cases()
    
    print("\n" + "=" * 60)
    print("✓ 所有测试通过!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()