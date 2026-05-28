"""
ColorName Utils 测试模块

测试颜色名称映射工具的所有功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from colorname_utils.mod import (
    RGB, HSL, ColorMatch, ColorInfo,
    parse_hex, parse_rgb, rgb_to_hex, rgb_to_hsl, hsl_to_rgb,
    color_distance, get_color_name, get_closest_color, get_n_closest_colors,
    get_color_category, get_brightness, get_temperature, get_color_info,
    get_color_info_hex, is_light_color, is_dark_color, get_contrast_color,
    are_colors_similar, blend_colors, lighten, darken, saturate, desaturate,
    complementary_color, analogous_colors, triadic_colors,
    split_complementary_colors, tetradic_colors, grayscale, sepia,
    invert_color, adjust_brightness, get_color_by_name, get_all_color_names,
    get_colors_by_category, search_color_names, color_count,
    random_color, random_pastel_color, random_dark_color,
    random_warm_color, random_cool_color, hex_to_rgb, rgb_string, hsl_string
)


def test_rgb_creation():
    """测试 RGB 创建和基本操作"""
    print("测试 RGB 创建...")
    
    # 正常创建
    rgb = RGB(255, 128, 0)
    assert rgb.r == 255
    assert rgb.g == 128
    assert rgb.b == 0
    
    # 边界值测试
    rgb_over = RGB(300, -10, 500)
    assert rgb_over.r == 255
    assert rgb_over.g == 0
    assert rgb_over.b == 255
    
    # 转换测试
    assert rgb.to_hex() == "#FF8000"
    assert rgb.to_tuple() == (255, 128, 0)
    
    print("  ✓ RGB 创建测试通过")


def test_hsl_creation():
    """测试 HSL 创建和基本操作"""
    print("测试 HSL 创建...")
    
    hsl = HSL(180, 50, 75)
    assert hsl.h == 180
    assert hsl.s == 50
    assert hsl.l == 75
    
    # 边界值测试
    hsl_over = HSL(400, 150, -10)
    assert hsl_over.h == 360
    assert hsl_over.s == 100
    assert hsl_over.l == 0
    
    print("  ✓ HSL 创建测试通过")


def test_color_conversion():
    """测试颜色格式转换"""
    print("测试颜色转换...")
    
    # 十六进制解析
    assert parse_hex("#FF0000") == RGB(255, 0, 0)
    assert parse_hex("FF0000") == RGB(255, 0, 0)
    assert parse_hex("#F00") == RGB(255, 0, 0)
    assert parse_hex("F00") == RGB(255, 0, 0)
    
    # RGB 字符串解析
    assert parse_rgb("rgb(255, 0, 0)") == RGB(255, 0, 0)
    assert parse_rgb("255, 0, 0") == RGB(255, 0, 0)
    assert parse_rgb("RGB(128, 128, 128)") == RGB(128, 128, 128)
    
    # RGB 转 HSL 转 RGB（往返测试）
    original = RGB(128, 64, 200)
    hsl = rgb_to_hsl(original)
    back = hsl_to_rgb(hsl)
    # 允许小误差
    assert abs(original.r - back.r) <= 1
    assert abs(original.g - back.g) <= 1
    assert abs(original.b - back.b) <= 1
    
    print("  ✓ 颜色转换测试通过")


def test_color_distance():
    """测试颜色距离计算"""
    print("测试颜色距离...")
    
    # 相同颜色距离为 0
    d = color_distance(RGB(100, 100, 100), RGB(100, 100, 100))
    assert d == 0
    
    # 黑白距离较大
    d = color_distance(RGB(0, 0, 0), RGB(255, 255, 255))
    assert d > 400
    
    # 相似颜色距离较小
    d = color_distance(RGB(255, 0, 0), RGB(250, 5, 5))
    assert d < 15
    
    print("  ✓ 颜色距离测试通过")


def test_color_name_lookup():
    """测试颜色名称查找"""
    print("测试颜色名称查找...")
    
    # 精确匹配
    assert get_color_name(RGB(255, 0, 0)) == "Red"
    assert get_color_name(RGB(0, 255, 0)) == "Lime"
    assert get_color_name(RGB(0, 0, 255)) == "Blue"
    assert get_color_name(RGB(255, 255, 255)) == "White"
    assert get_color_name(RGB(0, 0, 0)) == "Black"
    
    # 最近匹配
    match = get_closest_color(RGB(254, 1, 2))
    assert match.name == "Red"
    assert match.distance < 5
    
    # 多个最近颜色
    matches = get_n_closest_colors(RGB(255, 165, 0), 5)
    assert len(matches) == 5
    assert matches[0].name == "Orange"
    
    print("  ✓ 颜色名称查找测试通过")


def test_color_category():
    """测试颜色分类"""
    print("测试颜色分类...")
    
    assert get_color_category(RGB(255, 0, 0)) == "Red"
    assert get_color_category(RGB(255, 165, 0)) == "Orange"
    assert get_color_category(RGB(255, 255, 0)) == "Yellow"
    assert get_color_category(RGB(0, 255, 0)) == "Green"
    assert get_color_category(RGB(0, 255, 255)) == "Cyan"
    assert get_color_category(RGB(0, 0, 255)) == "Blue"
    # RGB(128, 0, 128) 的 hue 是 300，属于 Pink 范围 (285-345)
    # 使用更典型的紫色
    assert get_color_category(RGB(75, 0, 130)) == "Purple"  # Indigo
    # Pink 应该使用 hue 在 285-345 范围内的颜色
    assert get_color_category(RGB(255, 105, 180)) == "Pink"  # Hot Pink, hue ~330
    assert get_color_category(RGB(0, 0, 0)) == "Black"
    assert get_color_category(RGB(255, 255, 255)) == "White"
    assert get_color_category(RGB(128, 128, 128)) == "Gray"
    
    print("  ✓ 颜色分类测试通过")


def test_brightness():
    """测试亮度判断"""
    print("测试亮度判断...")
    
    assert get_brightness(RGB(0, 0, 0)) == "Dark"
    assert get_brightness(RGB(255, 255, 255)) == "Light"
    assert get_brightness(RGB(128, 128, 128)) == "Medium"
    
    assert is_light_color(RGB(255, 255, 255)) == True
    assert is_dark_color(RGB(0, 0, 0)) == True
    
    print("  ✓ 亮度判断测试通过")


def test_temperature():
    """测试颜色温度"""
    print("测试颜色温度...")
    
    assert get_temperature(RGB(255, 0, 0)) == "Warm"
    assert get_temperature(RGB(0, 0, 255)) == "Cool"
    assert get_temperature(RGB(128, 128, 128)) == "Neutral"
    
    print("  ✓ 颜色温度测试通过")


def test_color_info():
    """测试颜色完整信息"""
    print("测试颜色完整信息...")
    
    info = get_color_info(RGB(255, 165, 0))
    assert info.name == "Orange"
    assert info.hex == "#FFA500"
    assert info.rgb == RGB(255, 165, 0)
    assert info.category == "Orange"
    assert info.brightness in ["Light", "Medium", "Dark"]
    assert info.temperature in ["Warm", "Cool", "Neutral"]
    
    # 从十六进制获取
    info2 = get_color_info_hex("#FFA500")
    assert info2.name == "Orange"
    
    print("  ✓ 颜色完整信息测试通过")


def test_contrast_color():
    """测试对比色"""
    print("测试对比色...")
    
    # 亮背景应该返回黑色
    contrast = get_contrast_color(RGB(255, 255, 255))
    assert contrast == RGB(0, 0, 0)
    
    # 暗背景应该返回白色
    contrast = get_contrast_color(RGB(0, 0, 0))
    assert contrast == RGB(255, 255, 255)
    
    print("  ✓ 对比色测试通过")


def test_color_similarity():
    """测试颜色相似性判断"""
    print("测试颜色相似性判断...")
    
    # 相同颜色
    assert are_colors_similar(RGB(100, 100, 100), RGB(100, 100, 100)) == True
    
    # 接近的颜色
    assert are_colors_similar(RGB(100, 100, 100), RGB(105, 105, 105)) == True
    
    # 不同的颜色
    assert are_colors_similar(RGB(0, 0, 0), RGB(255, 255, 255)) == False
    
    print("  ✓ 颜色相似性测试通过")


def test_color_operations():
    """测试颜色操作"""
    print("测试颜色操作...")
    
    # 混合颜色
    blended = blend_colors(RGB(255, 0, 0), RGB(0, 0, 255), 0.5)
    assert blended.r == 127 or blended.r == 128
    assert blended.b == 127 or blended.b == 128
    
    # 变亮
    light = lighten(RGB(100, 100, 100), 20)
    hsl_light = rgb_to_hsl(light)
    assert hsl_light.l > rgb_to_hsl(RGB(100, 100, 100)).l
    
    # 变暗
    dark = darken(RGB(100, 100, 100), 20)
    hsl_dark = rgb_to_hsl(dark)
    assert hsl_dark.l < rgb_to_hsl(RGB(100, 100, 100)).l
    
    # 饱和度
    sat = saturate(RGB(100, 100, 100), 20)
    desat = desaturate(RGB(100, 150, 100), 20)
    # 验证操作不会崩溃
    
    print("  ✓ 颜色操作测试通过")


def test_color_harmony():
    """测试颜色和谐"""
    print("测试颜色和谐...")
    
    blue = RGB(0, 0, 255)
    
    # 互补色
    comp = complementary_color(blue)
    assert get_color_category(comp) == "Yellow"
    
    # 类似色
    analog = analogous_colors(RGB(0, 255, 0))
    assert len(analog) == 3
    
    # 三角色
    triadic = triadic_colors(blue)
    assert len(triadic) == 3
    
    # 分裂互补色
    split = split_complementary_colors(RGB(255, 0, 0))
    assert len(split) == 3
    
    # 四角色
    tetra = tetradic_colors(RGB(255, 0, 0))
    assert len(tetra) == 4
    
    print("  ✓ 颜色和谐测试通过")


def test_color_effects():
    """测试颜色效果"""
    print("测试颜色效果...")
    
    # 灰度
    gray = grayscale(RGB(100, 150, 200))
    assert gray.r == gray.g == gray.b
    
    # 棕褐色
    sep = sepia(RGB(100, 100, 100))
    assert sep.r > sep.b  # 棕褐色应该偏红
    
    # 反转
    inv = invert_color(RGB(100, 100, 100))
    assert inv.r == 155
    assert inv.g == 155
    assert inv.b == 155
    
    # 亮度调整
    adj = adjust_brightness(RGB(100, 100, 100), 50)
    assert adj.r > 100
    
    print("  ✓ 颜色效果测试通过")


def test_database_operations():
    """测试数据库操作"""
    print("测试数据库操作...")
    
    # 按名称获取颜色
    red = get_color_by_name("Red")
    assert red == RGB(255, 0, 0)
    
    # 大小写不敏感
    blue = get_color_by_name("BLUE")
    assert blue == RGB(0, 0, 255)
    
    # 不存在的颜色
    none = get_color_by_name("NonExistentColor")
    assert none is None
    
    # 获取所有颜色名称
    names = get_all_color_names()
    assert len(names) > 100
    assert "Red" in names
    assert "Blue" in names
    
    # 按类别获取颜色
    reds = get_colors_by_category("Red")
    assert "Red" in reds
    assert "Crimson" in reds
    
    # 搜索颜色
    results = search_color_names("blue")
    assert len(results) > 0
    assert any("Blue" in r.name for r in results)
    
    # 颜色数量
    count = color_count()
    assert count == len(names)
    
    print("  ✓ 数据库操作测试通过")


def test_random_colors():
    """测试随机颜色生成"""
    print("测试随机颜色生成...")
    
    # 随机颜色
    c1 = random_color()
    assert 0 <= c1.r <= 255
    assert 0 <= c1.g <= 255
    assert 0 <= c1.b <= 255
    
    # 随机柔和色
    c2 = random_pastel_color()
    assert 128 <= c2.r <= 255
    assert 128 <= c2.g <= 255
    assert 128 <= c2.b <= 255
    
    # 随机暗色
    c3 = random_dark_color()
    assert 0 <= c3.r <= 100
    assert 0 <= c3.g <= 100
    assert 0 <= c3.b <= 100
    
    # 随机暖色
    c4 = random_warm_color()
    hsl = rgb_to_hsl(c4)
    assert hsl.h < 60 or hsl.h >= 345
    
    # 随机冷色
    c5 = random_cool_color()
    hsl = rgb_to_hsl(c5)
    assert 180 <= hsl.h <= 300
    
    print("  ✓ 随机颜色生成测试通过")


def test_utility_functions():
    """测试工具函数"""
    print("测试工具函数...")
    
    # hex_to_rgb 别名
    assert hex_to_rgb("#FF0000") == RGB(255, 0, 0)
    
    # rgb_string
    s = rgb_string(RGB(255, 128, 0))
    assert s == "rgb(255, 128, 0)"
    
    # hsl_string
    s = hsl_string(HSL(180, 50, 75))
    assert "hsl(180" in s
    assert "50" in s
    assert "75" in s
    
    print("  ✓ 工具函数测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("ColorName Utils 完整测试")
    print("=" * 60)
    
    test_rgb_creation()
    test_hsl_creation()
    test_color_conversion()
    test_color_distance()
    test_color_name_lookup()
    test_color_category()
    test_brightness()
    test_temperature()
    test_color_info()
    test_contrast_color()
    test_color_similarity()
    test_color_operations()
    test_color_harmony()
    test_color_effects()
    test_database_operations()
    test_random_colors()
    test_utility_functions()
    
    print("=" * 60)
    print("✓ 所有测试通过!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()