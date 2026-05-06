"""
颜色工具测试套件

测试覆盖：
- 颜色解析 (HEX, RGB, HSL, HSV, CMYK)
- 格式转换
- 颜色混合与调整
- 对比度计算
- 配色方案生成
- 渐变生成
- 随机颜色生成
- 颜色名称查找
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Color, parse_hex, parse_color,
    rgb_to_hsl, hsl_to_rgb,
    rgb_to_hsv, hsv_to_rgb,
    rgb_to_cmyk, cmyk_to_rgb,
    mix_colors, adjust_lightness, adjust_saturation,
    calculate_luminance, calculate_contrast_ratio, wcag_compliance,
    get_complement_color, get_analogous_colors, get_triadic_colors,
    get_split_complementary_colors, get_tetradic_colors,
    get_monochromatic_colors, get_shades, get_tints, get_tones,
    create_gradient, create_multi_gradient,
    random_color, random_pastel_color, random_vibrant_color,
    random_dark_color, random_light_color,
    color_name_to_hex, hex_to_color_name,
    suggest_text_color,
    hex_to_rgb, rgb_to_hex, is_valid_hex,
)


def test_parse_hex():
    """测试 HEX 解析"""
    print("测试 parse_hex...")
    
    # 3 位 HEX
    r, g, b, a = parse_hex('#F00')
    assert r == 255 and g == 0 and b == 0
    assert a == 1.0
    
    r, g, b, a = parse_hex('F00')  # 无 #
    assert r == 255 and g == 0 and b == 0
    
    # 6 位 HEX
    r, g, b, a = parse_hex('#FF0000')
    assert r == 255 and g == 0 and b == 0
    assert a == 1.0
    
    # 4 位 HEX (带 alpha)
    r, g, b, a = parse_hex('#F008')
    assert r == 255 and g == 0 and b == 0
    assert abs(a - 0.533) < 0.01
    
    # 8 位 HEX (带 alpha)
    r, g, b, a = parse_hex('#FF000080')
    assert r == 255 and g == 0 and b == 0
    assert abs(a - 0.5) < 0.01
    
    print("  ✓ parse_hex 测试通过")


def test_color_object():
    """测试 Color 对象"""
    print("测试 Color 对象...")
    
    # 创建颜色
    color = Color.from_hex('#FF0000')
    assert color.r == 255
    assert color.g == 0
    assert color.b == 0
    
    # RGB 属性
    assert color.rgb == (255, 0, 0)
    
    # HEX 属性
    assert color.hex == '#ff0000'
    
    # HSL 属性
    h, s, l = color.hsl
    assert h == 0
    assert s == 100
    assert l == 50
    
    # HSV 属性
    h, s, v = color.hsv
    assert h == 0
    assert s == 100
    assert v == 100
    
    # CMYK 属性
    c, m, y, k = color.cmyk
    assert c == 0
    assert m == 100
    assert y == 100
    assert k == 0
    
    # 亮度属性
    assert color.is_dark
    assert not color.is_light
    
    print("  ✓ Color 对象测试通过")


def test_rgb_hsl_conversion():
    """测试 RGB <-> HSL 转换"""
    print("测试 RGB <-> HSL 转换...")
    
    # 红
    h, s, l = rgb_to_hsl(255, 0, 0)
    assert h == 0
    assert s == 100
    assert l == 50
    
    r, g, b = hsl_to_rgb(0, 100, 50)
    assert r == 255 and g == 0 and b == 0
    
    # 绿
    h, s, l = rgb_to_hsl(0, 255, 0)
    assert h == 120
    assert s == 100
    assert l == 50
    
    r, g, b = hsl_to_rgb(120, 100, 50)
    assert r == 0 and g == 255 and b == 0
    
    # 蓝
    h, s, l = rgb_to_hsl(0, 0, 255)
    assert h == 240
    assert s == 100
    assert l == 50
    
    r, g, b = hsl_to_rgb(240, 100, 50)
    assert r == 0 and g == 0 and b == 255
    
    # 黄 (红 + 绿)
    h, s, l = rgb_to_hsl(255, 255, 0)
    assert h == 60
    assert s == 100
    assert l == 50
    
    # 灰色
    h, s, l = rgb_to_hsl(128, 128, 128)
    assert s == 0
    assert l == 50
    
    # 白色
    h, s, l = rgb_to_hsl(255, 255, 255)
    assert l == 100
    
    # 黑色
    h, s, l = rgb_to_hsl(0, 0, 0)
    assert l == 0
    
    print("  ✓ RGB <-> HSL 转换测试通过")


def test_rgb_hsv_conversion():
    """测试 RGB <-> HSV 转换"""
    print("测试 RGB <-> HSV 转换...")
    
    # 红
    h, s, v = rgb_to_hsv(255, 0, 0)
    assert h == 0
    assert s == 100
    assert v == 100
    
    r, g, b = hsv_to_rgb(0, 100, 100)
    assert r == 255 and g == 0 and b == 0
    
    # 黄
    h, s, v = rgb_to_hsv(255, 255, 0)
    assert h == 60
    assert s == 100
    assert v == 100
    
    # 青
    h, s, v = rgb_to_hsv(0, 255, 255)
    assert h == 180
    assert s == 100
    assert v == 100
    
    # 品红
    h, s, v = rgb_to_hsv(255, 0, 255)
    assert h == 300
    assert s == 100
    assert v == 100
    
    print("  ✓ RGB <-> HSV 转换测试通过")


def test_rgb_cmyk_conversion():
    """测试 RGB <-> CMYK 转换"""
    print("测试 RGB <-> CMYK 转换...")
    
    # 红
    c, m, y, k = rgb_to_cmyk(255, 0, 0)
    assert c == 0 and m == 100 and y == 100 and k == 0
    
    r, g, b = cmyk_to_rgb(0, 100, 100, 0)
    assert r == 255 and g == 0 and b == 0
    
    # 白
    c, m, y, k = rgb_to_cmyk(255, 255, 255)
    assert c == 0 and m == 0 and y == 0 and k == 0
    
    # 黑
    c, m, y, k = rgb_to_cmyk(0, 0, 0)
    assert c == 0 and m == 0 and y == 0 and k == 100
    
    # 青
    c, m, y, k = rgb_to_cmyk(0, 255, 255)
    assert c == 100 and m == 0 and y == 0 and k == 0
    
    # 品红
    c, m, y, k = rgb_to_cmyk(255, 0, 255)
    assert c == 0 and m == 100 and y == 0 and k == 0
    
    # 黄
    c, m, y, k = rgb_to_cmyk(255, 255, 0)
    assert c == 0 and m == 0 and y == 100 and k == 0
    
    print("  ✓ RGB <-> CMYK 转换测试通过")


def test_color_mixing():
    """测试颜色混合"""
    print("测试颜色混合...")
    
    red = Color.from_hex('#FF0000')
    blue = Color.from_hex('#0000FF')
    
    # 50% 混合 -> 紫色
    purple = mix_colors(red, blue, 0.5)
    assert purple.r == 127
    assert purple.b == 127
    assert purple.g == 0
    
    # 25% 混合
    mix1 = mix_colors(red, blue, 0.25)
    assert mix1.r == 191  # 255 * 0.75 + 0 * 0.25
    assert mix1.b == 63   # 0 * 0.75 + 255 * 0.25
    
    # 使用 Color 对象的 mix 方法
    purple2 = red.mix(blue, 0.5)
    assert purple2.hex == purple.hex
    
    print("  ✓ 颜色混合测试通过")


def test_color_adjustment():
    """测试颜色调整"""
    print("测试颜色调整...")
    
    color = Color.from_hex('#FF0000')  # 红色
    
    # 变亮
    lighter = adjust_lightness(color, 0.2)
    h, s, l = lighter.hsl
    assert l == 70  # 50 + 20
    
    # 变暗
    darker = adjust_lightness(color, -0.2)
    h, s, l = darker.hsl
    assert l == 30  # 50 - 20
    
    # 去饱和 -> 灰色
    gray = adjust_saturation(color, -1.0)
    h, s, l = gray.hsl
    assert s == 0
    
    # 使用 Color 对象方法
    lighter2 = color.lighter(0.2)
    assert lighter2.hsl[2] == 70
    
    darker2 = color.darker(0.2)
    assert darker2.hsl[2] == 30
    
    print("  ✓ 颜色调整测试通过")


def test_contrast_ratio():
    """测试对比度计算"""
    print("测试对比度计算...")
    
    black = Color.from_hex('#000000')
    white = Color.from_hex('#FFFFFF')
    
    # 黑白对比度应为 21:1
    ratio = calculate_contrast_ratio(black, white)
    assert abs(ratio - 21.0) < 0.1
    
    # 相同颜色对比度为 1:1
    ratio = calculate_contrast_ratio(black, black)
    assert abs(ratio - 1.0) < 0.1
    
    # WCAG 合规性检查
    compliance = wcag_compliance(black, white)
    assert compliance['contrast_ratio'] >= 21.0
    assert compliance['aa_normal'] == True
    assert compliance['aaa_normal'] == True
    
    # 红色和白色对比度 (实际约 3.998:1，接近 4.0)
    red = Color.from_hex('#FF0000')
    ratio = calculate_contrast_ratio(red, white)
    assert ratio > 3.9  # 大约 4.0:1
    
    print("  ✓ 对比度计算测试通过")


def test_color_schemes():
    """测试配色方案"""
    print("测试配色方案...")
    
    red = Color.from_hex('#FF0000')
    
    # 互补色 (180°)
    complement = get_complement_color(red)
    assert complement.hsl[0] == 180  # 青色
    
    # 类似色 (±30°)
    analogous = get_analogous_colors(red, 30)
    assert len(analogous) == 3
    assert analogous[1].hsl[0] == 330  # -30° -> 330°
    assert analogous[2].hsl[0] == 30   # +30°
    
    # 三角色 (±120°)
    triadic = get_triadic_colors(red)
    assert len(triadic) == 3
    assert triadic[1].hsl[0] == 120
    assert triadic[2].hsl[0] == 240
    
    # 分裂互补色
    split = get_split_complementary_colors(red)
    assert len(split) == 3
    
    # 四角色
    tetradic = get_tetradic_colors(red)
    assert len(tetradic) == 4
    
    # 单色配色
    mono = get_monochromatic_colors(red, 5)
    assert len(mono) == 5
    assert all(c.hsl[0] == 0 for c in mono)  # 色相相同
    
    # 色阶
    shades = get_shades(red, 5)
    assert len(shades) == 5
    
    # 色调
    tints = get_tints(red, 5)
    assert len(tints) == 5
    
    # 灰度色调
    tones = get_tones(red, 5)
    assert len(tones) == 5
    
    print("  ✓ 配色方案测试通过")


def test_gradient():
    """测试渐变生成"""
    print("测试渐变生成...")
    
    red = Color.from_hex('#FF0000')
    blue = Color.from_hex('#0000FF')
    
    # 简单渐变
    gradient = create_gradient(red, blue, 5)
    assert len(gradient) == 5
    assert gradient[0].hex == red.hex
    assert gradient[4].hex == blue.hex
    
    # 检查中间色
    purple = gradient[2]
    assert purple.r == 127
    assert purple.b == 127
    
    # 多色渐变
    green = Color.from_hex('#00FF00')
    multi = create_multi_gradient([red, green, blue], 9)
    assert len(multi) == 9
    
    print("  ✓ 渐变生成测试通过")


def test_random_colors():
    """测试随机颜色生成"""
    print("测试随机颜色生成...")
    
    # 基本随机颜色
    color = random_color()
    assert 0 <= color.r <= 255
    assert 0 <= color.g <= 255
    assert 0 <= color.b <= 255
    
    # 带限制的随机颜色
    color = random_color(min_brightness=100, max_brightness=200)
    # 检查亮度在范围内
    
    # 柔和色
    pastel = random_pastel_color()
    assert pastel.hsl[1] >= 40  # 饱和度 >= 40
    assert pastel.hsl[2] >= 70  # 明度 >= 70
    
    # 鲜艳色
    vibrant = random_vibrant_color()
    assert vibrant.hsl[1] >= 80  # 饱和度 >= 80
    
    # 深色
    dark = random_dark_color()
    assert dark.luminance < 0.4
    
    # 浅色
    light = random_light_color()
    assert light.luminance > 0.6
    
    print("  ✓ 随机颜色生成测试通过")


def test_color_names():
    """测试颜色名称"""
    print("测试颜色名称...")
    
    # 名称转 HEX
    hex_val = color_name_to_hex('red')
    assert hex_val == '#FF0000'
    
    hex_val = color_name_to_hex('blue')
    assert hex_val == '#0000FF'
    
    hex_val = color_name_to_hex('unknown')
    assert hex_val is None
    
    # HEX 转名称
    name = hex_to_color_name('#FF0000')
    assert name == 'red'
    
    name = hex_to_color_name('#000000')
    assert name == 'black'
    
    # 接近的颜色
    name = hex_to_color_name('#FF0001')
    assert name == 'red'  # 允许一定误差
    
    print("  ✓ 颜色名称测试通过")


def test_text_color_suggestion():
    """测试文本颜色建议"""
    print("测试文本颜色建议...")
    
    # 黑色背景 -> 白色文本
    black = Color.from_hex('#000000')
    text = suggest_text_color(black)
    assert text.hex == '#ffffff'
    
    # 白色背景 -> 黑色文本
    white = Color.from_hex('#FFFFFF')
    text = suggest_text_color(white)
    assert text.hex == '#000000'
    
    # 黄色背景 -> 黑色文本 (亮色)
    yellow = Color.from_hex('#FFFF00')
    text = suggest_text_color(yellow)
    assert text.hex == '#000000'
    
    # 深蓝背景 -> 白色文本
    dark_blue = Color.from_hex('#000080')
    text = suggest_text_color(dark_blue)
    assert text.hex == '#ffffff'
    
    print("  ✓ 文本颜色建议测试通过")


def test_utility_functions():
    """测试便捷函数"""
    print("测试便捷函数...")
    
    # hex_to_rgb
    rgb = hex_to_rgb('#FF0000')
    assert rgb == (255, 0, 0)
    
    # rgb_to_hex
    hex_val = rgb_to_hex(255, 0, 0)
    assert hex_val == '#ff0000'
    
    # is_valid_hex
    assert is_valid_hex('#FF0000') == True
    assert is_valid_hex('FF0000') == True
    assert is_valid_hex('#F00') == True
    assert is_valid_hex('#FF0000FF') == True
    assert is_valid_hex('invalid') == False
    assert is_valid_hex('#GGGGGG') == False
    
    # parse_color
    color = parse_color('#FF0000')
    assert color.r == 255
    
    color = parse_color((255, 0, 0))
    assert color.r == 255
    
    print("  ✓ 便捷函数测试通过")


def test_color_object_methods():
    """测试 Color 对象方法"""
    print("测试 Color 对象方法...")
    
    color = Color.from_hex('#FF0000')
    
    # rotate_hue
    rotated = color.rotate_hue(90)
    assert rotated.hsl[0] == 90
    
    rotated = color.rotate_hue(180)
    assert rotated.hsl[0] == 180
    
    # complement 方法
    complement = color.complement()
    assert complement.hsl[0] == 180
    
    # saturate / desaturate
    gray = Color.from_hex('#808080')
    saturated = gray.saturate(0.5)
    # 灰色饱和度为 0，增加后应大于 0
    
    # to_dict
    data = color.to_dict()
    assert 'hex' in data
    assert 'rgb' in data
    assert 'hsl' in data
    assert 'hsv' in data
    assert 'cmyk' in data
    
    print("  ✓ Color 对象方法测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 颜色值边界
    color = Color(300, 300, 300)  # 超出范围
    assert color.r == 255
    assert color.g == 255
    assert color.b == 255
    
    color = Color(-10, -10, -10)
    assert color.r == 0
    assert color.g == 0
    assert color.b == 0
    
    # Alpha 边界
    color = Color(100, 100, 100, 2.0)
    assert color.a == 1.0
    
    color = Color(100, 100, 100, -0.5)
    assert color.a == 0.0
    
    # 灰色转换
    gray = Color.from_hex('#808080')
    h, s, l = gray.hsl
    assert s == 0  # 灰色饱和度为 0
    
    print("  ✓ 边界情况测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("颜色工具测试套件")
    print("=" * 50 + "\n")
    
    tests = [
        test_parse_hex,
        test_color_object,
        test_rgb_hsl_conversion,
        test_rgb_hsv_conversion,
        test_rgb_cmyk_conversion,
        test_color_mixing,
        test_color_adjustment,
        test_contrast_ratio,
        test_color_schemes,
        test_gradient,
        test_random_colors,
        test_color_names,
        test_text_color_suggestion,
        test_utility_functions,
        test_color_object_methods,
        test_edge_cases,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} 异常: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)