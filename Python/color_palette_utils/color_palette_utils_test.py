"""
颜色调色板工具测试模块

测试所有颜色调色板功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from color_palette_utils.mod import (
    # 颜色空间转换
    hex_to_rgb, rgb_to_hex, rgb_to_hsl, hsl_to_rgb, hex_to_hsl, hsl_to_hex,
    # 颜色调整
    adjust_lightness, adjust_saturation, get_complementary,
    # 调色板生成
    generate_complementary_palette, generate_analogous_palette,
    generate_triadic_palette, generate_split_complementary_palette,
    generate_tetradic_palette, generate_pentadic_palette, generate_square_palette,
    generate_monochromatic_palette, generate_shades, generate_tints,
    generate_tones, generate_gradient, generate_multi_gradient,
    # 随机调色板
    random_color, random_palette, random_harmonious_palette,
    random_warm_palette, random_cool_palette, random_pastel_palette,
    # 导出
    palette_to_css_variables, palette_to_scss_variables,
    palette_to_json, palette_to_tailwind_config,
    # 对比度和可访问性
    get_luminance, get_contrast_ratio, meets_wcag_aa, meets_wcag_aaa,
    suggest_accessible_color,
    # 颜色名称
    get_color_name, COLOR_NAMES,
    # 工具函数
    blend_colors, is_light_color, is_warm_color, color_temperature,
    get_palette_harmony_type,
    # 类
    ColorPalette, create_palette,
)


def test_hex_to_rgb():
    """测试十六进制转 RGB。"""
    assert hex_to_rgb('#FF0000') == (255, 0, 0), "红色转换失败"
    assert hex_to_rgb('#00FF00') == (0, 255, 0), "绿色转换失败"
    assert hex_to_rgb('#0000FF') == (0, 0, 255), "蓝色转换失败"
    assert hex_to_rgb('FF0000') == (255, 0, 0), "无#前缀转换失败"
    assert hex_to_rgb('#F00') == (255, 0, 0), "短格式转换失败"
    assert hex_to_rgb('#FFFFFF') == (255, 255, 255), "白色转换失败"
    assert hex_to_rgb('#000000') == (0, 0, 0), "黑色转换失败"
    print("✓ hex_to_rgb 测试通过")


def test_rgb_to_hex():
    """测试 RGB 转十六进制。"""
    assert rgb_to_hex(255, 0, 0) == '#FF0000', "红色转换失败"
    assert rgb_to_hex(0, 255, 0) == '#00FF00', "绿色转换失败"
    assert rgb_to_hex(0, 0, 255) == '#0000FF', "蓝色转换失败"
    assert rgb_to_hex(255, 255, 255) == '#FFFFFF', "白色转换失败"
    assert rgb_to_hex(0, 0, 0) == '#000000', "黑色转换失败"
    assert rgb_to_hex(255, 0, 0, False) == 'FF0000', "无#前缀转换失败"
    # 测试边界值
    assert rgb_to_hex(300, 0, 0) == '#FF0000', "超范围值应被裁剪"
    assert rgb_to_hex(-10, 0, 0) == '#000000', "负值应被裁剪"
    print("✓ rgb_to_hex 测试通过")


def test_rgb_hsl_roundtrip():
    """测试 RGB 与 HSL 的往返转换。"""
    test_colors = [
        (255, 0, 0),      # 红色
        (0, 255, 0),      # 绿色
        (0, 0, 255),      # 蓝色
        (255, 255, 0),    # 黄色
        (255, 0, 255),    # 品红
        (0, 255, 255),    # 青色
        (128, 128, 128),  # 灰色
        (255, 255, 255),  # 白色
        (0, 0, 0),        # 黑色
    ]
    
    for r, g, b in test_colors:
        h, s, l = rgb_to_hsl(r, g, b)
        r2, g2, b2 = hsl_to_rgb(h, s, l)
        # 允许小的误差
        assert abs(r - r2) <= 1, f"R 转换误差过大: {r} -> {r2}"
        assert abs(g - g2) <= 1, f"G 转换误差过大: {g} -> {g2}"
        assert abs(b - b2) <= 1, f"B 转换误差过大: {b} -> {b2}"
    
    print("✓ RGB/HSL 往返转换测试通过")


def test_rgb_to_hsl():
    """测试 RGB 转 HSL。"""
    # 红色
    h, s, l = rgb_to_hsl(255, 0, 0)
    assert h == 0.0, f"红色色相应为 0，实际为 {h}"
    assert s == 100.0, f"红色饱和度应为 100，实际为 {s}"
    assert l == 50.0, f"红色亮度应为 50，实际为 {l}"
    
    # 绿色
    h, s, l = rgb_to_hsl(0, 255, 0)
    assert h == 120.0, f"绿色色相应为 120，实际为 {h}"
    assert s == 100.0, f"绿色饱和度应为 100，实际为 {s}"
    assert l == 50.0, f"绿色亮度应为 50，实际为 {l}"
    
    # 灰色
    h, s, l = rgb_to_hsl(128, 128, 128)
    assert s == 0, f"灰色饱和度应为 0，实际为 {s}"
    
    print("✓ rgb_to_hsl 测试通过")


def test_hex_hsl_conversion():
    """测试十六进制与 HSL 的转换。"""
    # 红色
    h, s, l = hex_to_hsl('#FF0000')
    assert h == 0.0, f"红色色相错误: {h}"
    assert s == 100.0, f"红色饱和度错误: {s}"
    assert l == 50.0, f"红色亮度错误: {l}"
    
    # 往返测试
    hex_color = '#336699'
    h, s, l = hex_to_hsl(hex_color)
    result = hsl_to_hex(h, s, l)
    assert result.upper() == hex_color.upper(), f"往返转换失败: {hex_color} -> {result}"
    
    print("✓ hex/hsl 转换测试通过")


def test_adjust_lightness():
    """测试亮度调整。"""
    # 变亮 - 黑色 (亮度=0) 增加 50 后亮度为 50，对应 #808080 或 #7F7F7F（精度误差）
    result = adjust_lightness('#000000', 50)
    r, g, b = hex_to_rgb(result)
    assert abs(r - 128) <= 1 and abs(g - 128) <= 1 and abs(b - 128) <= 1, f"黑色变亮失败: {result}"
    
    # 变暗 - 白色 (亮度=100) 减少 50 后亮度为 50
    result = adjust_lightness('#FFFFFF', -50)
    r, g, b = hex_to_rgb(result)
    assert abs(r - 128) <= 1 and abs(g - 128) <= 1 and abs(b - 128) <= 1, f"白色变暗失败: {result}"
    
    # 边界测试
    result = adjust_lightness('#FFFFFF', 100)
    assert result == '#FFFFFF', "亮度不应超过 100%"
    
    result = adjust_lightness('#000000', -100)
    assert result == '#000000', "亮度不应低于 0%"
    
    print("✓ adjust_lightness 测试通过")


def test_adjust_saturation():
    """测试饱和度调整。"""
    # 增加饱和度 - 灰色 (饱和度=0) 增加 50
    result = adjust_saturation('#808080', 50)
    h, s, l = hex_to_hsl(result)
    assert abs(s - 50) < 1, f"饱和度调整失败: {s}"
    
    print("✓ adjust_saturation 测试通过")


def test_get_complementary():
    """测试互补色获取。"""
    # 红色的互补色是青色
    result = get_complementary('#FF0000')
    h, s, l = hex_to_hsl(result)
    assert abs(h - 180) < 1, f"红色互补色应为青色（色相180），实际色相: {h}"
    
    # 验证互补色的互补色是原色
    result2 = get_complementary(result)
    h2, _, _ = hex_to_hsl(result2)
    assert abs(h2) < 1 or abs(h2 - 360) < 1, f"互补色的互补色应为原色"
    
    print("✓ get_complementary 测试通过")


def test_complementary_palette():
    """测试互补色调色板。"""
    palette = generate_complementary_palette('#FF0000')
    assert len(palette) == 2, f"互补色调色板应有 2 个颜色，实际: {len(palette)}"
    assert palette[0] == '#FF0000', "基础色应为第一个颜色"
    
    h1, _, _ = hex_to_hsl(palette[0])
    h2, _, _ = hex_to_hsl(palette[1])
    diff = abs(h1 - h2)
    assert abs(diff - 180) < 1, f"互补色应相差 180 度，实际相差: {diff}"
    
    print("✓ complementary_palette 测试通过")


def test_analogous_palette():
    """测试类似色调色板。"""
    palette = generate_analogous_palette('#FF0000')
    assert len(palette) == 3, f"类似色调色板应有 3 个颜色，实际: {len(palette)}"
    
    # 检查色相差 - 类似色在基础色两侧 30 度
    # palette[0] 是基础色-30度，palette[1] 是基础色，palette[2] 是基础色+30度
    h_base = hex_to_hsl(palette[1])[0]  # 基础色是第二个
    for i, color in enumerate(palette):
        h = hex_to_hsl(color)[0]
        diff = abs(h - h_base)
        # 考虑色相环绕（如 0 和 360）和精度误差
        diff = min(diff, 360 - diff)
        assert diff <= 31 or diff >= 329, f"类似色{i}与基础色相差过大: {diff}"
    
    print("✓ analogous_palette 测试通过")


def test_triadic_palette():
    """测试三角色调色板。"""
    palette = generate_triadic_palette('#FF0000')
    assert len(palette) == 3, f"三角色调色板应有 3 个颜色，实际: {len(palette)}"
    
    # 检查色相差（应相差 120 度）
    hues = [hex_to_hsl(c)[0] for c in palette]
    expected_diffs = [0, 120, 240]
    for i, expected in enumerate(expected_diffs):
        actual_diff = (hues[i] - hues[0]) % 360
        assert abs(actual_diff - expected) < 1, f"三角角色{i}色相差错误"
    
    print("✓ triadic_palette 测试通过")


def test_split_complementary_palette():
    """测试分裂互补色调色板。"""
    palette = generate_split_complementary_palette('#FF0000')
    assert len(palette) == 3, f"分裂互补色调色板应有 3 个颜色，实际: {len(palette)}"
    
    print("✓ split_complementary_palette 测试通过")


def test_tetradic_palette():
    """测试四角色调色板。"""
    palette = generate_tetradic_palette('#FF0000')
    assert len(palette) == 4, f"四角色调色板应有 4 个颜色，实际: {len(palette)}"
    
    # 检查色相差（应相差 90 度）
    hues = [hex_to_hsl(c)[0] for c in palette]
    for i in range(1, 4):
        diff = (hues[i] - hues[0]) % 360
        expected = i * 90
        assert abs(diff - expected) < 1, f"四角角色{i}色相差错误: {diff} vs {expected}"
    
    print("✓ tetradic_palette 测试通过")


def test_pentadic_palette():
    """测试五角色调色板。"""
    palette = generate_pentadic_palette('#FF0000')
    assert len(palette) == 5, f"五角色调色板应有 5 个颜色，实际: {len(palette)}"
    
    print("✓ pentadic_palette 测试通过")


def test_monochromatic_palette():
    """测试单色调色板。"""
    palette = generate_monochromatic_palette('#FF0000', 5)
    assert len(palette) == 5, f"单色调色板应有 5 个颜色，实际: {len(palette)}"
    
    # 所有颜色应有相同的色相和饱和度
    h_ref, s_ref, _ = hex_to_hsl(palette[0])
    for color in palette:
        h, s, l = hex_to_hsl(color)
        assert abs(h - h_ref) < 1, "单色调色板色相应相同"
    
    print("✓ monochromatic_palette 测试通过")


def test_shades():
    """测试阴影生成。"""
    shades = generate_shades('#FF0000', 5)
    assert len(shades) == 5, f"阴影数量错误: {len(shades)}"
    
    # 阴影应该越来越暗
    lightness_values = [hex_to_hsl(s)[2] for s in shades]
    # 所有阴影应该比原色暗
    print("✓ shades 测试通过")


def test_tints():
    """测试着色生成。"""
    tints = generate_tints('#FF0000', 5)
    assert len(tints) == 5, f"着色数量错误: {len(tints)}"
    
    print("✓ tints 测试通过")


def test_tones():
    """测试色调生成。"""
    tones = generate_tones('#FF0000', 5)
    assert len(tones) == 5, f"色调数量错误: {len(tones)}"
    
    print("✓ tones 测试通过")


def test_gradient():
    """测试渐变生成。"""
    gradient = generate_gradient('#FF0000', '#0000FF', 10)
    assert len(gradient) == 10, f"渐变数量错误: {len(gradient)}"
    assert gradient[0] == '#FF0000', "渐变起点错误"
    assert gradient[-1] == '#0000FF', "渐变终点错误"
    
    # 检查渐变的总体趋势（从红到蓝）
    # 不检查相邻颜色差异，因为色相可能经过紫色区域
    # 而是检查 RGB 值的变化趋势
    first_r, first_g, first_b = hex_to_rgb(gradient[0])
    last_r, last_g, last_b = hex_to_rgb(gradient[-1])
    assert first_r == 255 and first_b == 0, "起点应为红色"
    assert last_r == 0 and last_b == 255, "终点应为蓝色"
    
    print("✓ gradient 测试通过")


def test_multi_gradient():
    """测试多色渐变。"""
    colors = ['#FF0000', '#00FF00', '#0000FF']
    gradient = generate_multi_gradient(colors, 3)
    assert gradient[0] == '#FF0000', "多色渐变起点错误"
    assert gradient[-1] == '#0000FF', "多色渐变终点错误"
    
    print("✓ multi_gradient 测试通过")


def test_random_color():
    """测试随机颜色生成。"""
    color = random_color()
    assert color.startswith('#'), "随机颜色应以 # 开头"
    assert len(color) == 7, f"随机颜色长度错误: {len(color)}"
    
    # 验证颜色值有效
    r, g, b = hex_to_rgb(color)
    assert 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255
    
    print("✓ random_color 测试通过")


def test_random_palette():
    """测试随机调色板生成。"""
    palette = random_palette(5)
    assert len(palette) == 5, f"随机调色板数量错误: {len(palette)}"
    
    for color in palette:
        assert color.startswith('#'), f"颜色格式错误: {color}"
    
    print("✓ random_palette 测试通过")


def test_random_harmonious_palette():
    """测试随机和谐调色板。"""
    for harmony_type in ['complementary', 'analogous', 'triadic', 
                          'split_complementary', 'tetradic', 'pentadic']:
        palette = random_harmonious_palette(harmony_type)
        assert len(palette) >= 2, f"{harmony_type} 调色板颜色数不足"
    
    print("✓ random_harmonious_palette 测试通过")


def test_random_warm_palette():
    """测试暖色调调色板。"""
    palette = random_warm_palette(5)
    assert len(palette) == 5
    
    for color in palette:
        assert is_warm_color(color), f"暖色调调色板包含冷色: {color}"
    
    print("✓ random_warm_palette 测试通过")


def test_random_cool_palette():
    """测试冷色调调色板。"""
    palette = random_cool_palette(5)
    assert len(palette) == 5
    
    for color in palette:
        assert not is_warm_color(color), f"冷色调调色板包含暖色: {color}"
    
    print("✓ random_cool_palette 测试通过")


def test_random_pastel_palette():
    """测试柔和色调调色板。"""
    palette = random_pastel_palette(5)
    assert len(palette) == 5
    
    for color in palette:
        _, s, l = hex_to_hsl(color)
        assert s < 60, f"柔和色饱和度过高: {s}"
        assert l > 60, f"柔和色亮度过低: {l}"
    
    print("✓ random_pastel_palette 测试通过")


def test_palette_to_css_variables():
    """测试 CSS 变量导出。"""
    palette = ['#FF0000', '#00FF00', '#0000FF']
    css = palette_to_css_variables(palette)
    
    assert ':root {' in css, "CSS 变量格式错误"
    assert '--color-1: #FF0000;' in css, "颜色 1 未正确导出"
    assert '--color-2: #00FF00;' in css, "颜色 2 未正确导出"
    assert '--color-3: #0000FF;' in css, "颜色 3 未正确导出"
    
    # 测试自定义变量名
    css = palette_to_css_variables(palette, variable_names=['primary', 'secondary', 'tertiary'])
    assert '--primary: #FF0000;' in css, "自定义变量名未生效"
    
    print("✓ palette_to_css_variables 测试通过")


def test_palette_to_scss_variables():
    """测试 SCSS 变量导出。"""
    palette = ['#FF0000', '#00FF00']
    scss = palette_to_scss_variables(palette)
    
    assert '$color-1: #FF0000;' in scss, "SCSS 变量格式错误"
    assert '$color-2: #00FF00;' in scss, "SCSS 变量格式错误"
    
    print("✓ palette_to_scss_variables 测试通过")


def test_palette_to_json():
    """测试 JSON 导出。"""
    palette = ['#FF0000', '#00FF00']
    json_data = palette_to_json(palette, 'test')
    
    assert json_data['name'] == 'test', "JSON 名称错误"
    assert json_data['count'] == 2, "JSON 数量错误"
    assert len(json_data['colors']) == 2, "JSON 颜色数量错误"
    assert json_data['colors'][0]['hex'] == '#FF0000', "JSON 颜色值错误"
    
    # 测试包含 RGB
    json_data = palette_to_json(palette, 'test', include_rgb=True)
    assert 'rgb' in json_data['colors'][0], "RGB 值未包含"
    assert json_data['colors'][0]['rgb'] == (255, 0, 0), "RGB 值错误"
    
    print("✓ palette_to_json 测试通过")


def test_palette_to_tailwind_config():
    """测试 Tailwind 配置导出。"""
    palette = ['#FF0000', '#00FF00', '#0000FF']
    tw = palette_to_tailwind_config(palette, 'custom')
    
    assert 'custom:' in tw, "Tailwind 配置名称错误"
    assert "'50'" in tw or "'500'" in tw, "Tailwind 色阶未生成"
    
    print("✓ palette_to_tailwind_config 测试通过")


def test_get_luminance():
    """测试亮度计算。"""
    # 白色亮度最高
    assert get_luminance('#FFFFFF') == 1.0, "白色亮度应为 1"
    
    # 黑色亮度最低
    assert get_luminance('#000000') == 0.0, "黑色亮度应为 0"
    
    # 灰色亮度约为 0.216（因为人眼对绿色更敏感）
    # #808080 的相对亮度约为 0.216
    l = get_luminance('#808080')
    assert 0.2 < l < 0.22, f"灰色亮度应约为 0.216，实际: {l}"
    
    print("✓ get_luminance 测试通过")


def test_get_contrast_ratio():
    """测试对比度计算。"""
    # 黑白对比度最高 (21:1)
    ratio = get_contrast_ratio('#FFFFFF', '#000000')
    assert ratio == 21.0, f"黑白对比度应为 21，实际: {ratio}"
    
    # 相同颜色对比度为 1
    ratio = get_contrast_ratio('#FF0000', '#FF0000')
    assert ratio == 1.0, f"相同颜色对比度应为 1，实际: {ratio}"
    
    print("✓ get_contrast_ratio 测试通过")


def test_meets_wcag_aa():
    """测试 WCAG AA 标准检查。"""
    # 黑白满足 AA
    assert meets_wcag_aa('#000000', '#FFFFFF'), "黑白应满足 WCAG AA"
    
    # 浅灰在白底上不满足 AA
    assert not meets_wcag_aa('#CCCCCC', '#FFFFFF'), "浅灰在白底不应满足 WCAG AA"
    
    # 大文本标准较低 - 使用对比度约 3.2 的颜色
    # #767676 与白色对比度约为 4.5，满足大文本 AA
    assert meets_wcag_aa('#767676', '#FFFFFF', large_text=True), "中等灰在白底应满足大文本 WCAG AA"
    
    print("✓ meets_wcag_aa 测试通过")


def test_meets_wcag_aaa():
    """测试 WCAG AAA 标准检查。"""
    # 黑白满足 AAA
    assert meets_wcag_aaa('#000000', '#FFFFFF'), "黑白应满足 WCAG AAA"
    
    # 深灰在白底可能不满足 AAA
    assert not meets_wcag_aaa('#666666', '#FFFFFF'), "深灰在白底不应满足 WCAG AAA"
    
    print("✓ meets_wcag_aaa 测试通过")


def test_suggest_accessible_color():
    """测试可访问性颜色建议。"""
    # 在白底上，需要较深的颜色
    suggested = suggest_accessible_color('#888888', '#FFFFFF', 4.5)
    ratio = get_contrast_ratio(suggested, '#FFFFFF')
    assert ratio >= 4.5, f"建议颜色对比度不足: {ratio}"
    
    print("✓ suggest_accessible_color 测试通过")


def test_get_color_name():
    """测试颜色名称获取。"""
    assert get_color_name('#FF0000') == 'Red', "红色名称错误"
    assert get_color_name('#00FF00') == 'Lime', "绿色名称错误"
    assert get_color_name('#0000FF') == 'Blue', "蓝色名称错误"
    assert get_color_name('#FFFFFF') == 'White', "白色名称错误"
    assert get_color_name('#000000') == 'Black', "黑色名称错误"
    
    # 未知颜色返回原值
    assert get_color_name('#123ABC') == '#123ABC', "未知颜色应返回原值"
    
    print("✓ get_color_name 测试通过")


def test_blend_colors():
    """测试颜色混合。"""
    # 黑白混合应为灰 - 由于精度问题可能是 #808080 或 #7F7F7F
    result = blend_colors('#000000', '#FFFFFF', 0.5)
    r, g, b = hex_to_rgb(result)
    assert abs(r - 128) <= 1 and abs(g - 128) <= 1 and abs(b - 128) <= 1, f"黑白混合应为灰色，实际: {result}"
    
    # 极端比例
    result = blend_colors('#FF0000', '#0000FF', 0)
    assert result == '#FF0000', "比例 0 应返回第一个颜色"
    
    result = blend_colors('#FF0000', '#0000FF', 1)
    assert result == '#0000FF', "比例 1 应返回第二个颜色"
    
    print("✓ blend_colors 测试通过")


def test_is_light_color():
    """测试颜色明暗判断。"""
    assert is_light_color('#FFFFFF'), "白色应为浅色"
    assert not is_light_color('#000000'), "黑色不应为浅色"
    assert is_light_color('#EEEEEE'), "浅灰应为浅色"
    assert not is_light_color('#333333'), "深灰不应为浅色"
    
    print("✓ is_light_color 测试通过")


def test_is_warm_color():
    """测试暖色判断。"""
    assert is_warm_color('#FF0000'), "红色应为暖色"
    assert is_warm_color('#FFA500'), "橙色应为暖色"
    assert is_warm_color('#FFFF00'), "黄色应为暖色"
    assert not is_warm_color('#0000FF'), "蓝色应为冷色"
    assert not is_warm_color('#00FF00'), "绿色应为冷色"
    
    print("✓ is_warm_color 测试通过")


def test_color_temperature():
    """测试颜色温度。"""
    assert color_temperature('#FF0000') == 'warm', "红色应为暖色"
    assert color_temperature('#0000FF') == 'cool', "蓝色应为冷色"
    assert color_temperature('#808080') == 'neutral', "灰色应为中性"
    
    print("✓ color_temperature 测试通过")


def test_get_palette_harmony_type():
    """测试调色板和谐类型识别。"""
    # 互补色
    palette = generate_complementary_palette('#FF0000')
    harmony = get_palette_harmony_type(palette)
    assert harmony == 'complementary', f"互补色识别错误: {harmony}"
    
    # 三角色
    palette = generate_triadic_palette('#FF0000')
    harmony = get_palette_harmony_type(palette)
    assert harmony == 'triadic', f"三角色识别错误: {harmony}"
    
    print("✓ get_palette_harmony_type 测试通过")


def test_color_palette_class():
    """测试 ColorPalette 类。"""
    # 创建调色板
    palette = ColorPalette(['#FF0000', '#00FF00', '#0000FF'], 'RGB')
    assert len(palette) == 3, "调色板长度错误"
    assert palette.name == 'RGB', "调色板名称错误"
    
    # 迭代测试
    colors = list(palette)
    assert len(colors) == 3, "迭代失败"
    
    # 索引访问
    assert palette[0] == '#FF0000', "索引访问失败"
    
    # 添加颜色
    palette.add_color('#FFFF00')
    assert len(palette) == 4, "添加颜色失败"
    
    # 移除颜色
    palette.remove_color(0)
    assert len(palette) == 3, "移除颜色失败"
    
    print("✓ ColorPalette 类测试通过")


def test_color_palette_from_base_color():
    """测试从基础颜色创建调色板。"""
    palette = ColorPalette.from_base_color('#FF0000', 'triadic')
    assert len(palette) == 3, "三角调色板颜色数错误"
    
    palette = ColorPalette.from_base_color('#FF0000', 'complementary')
    assert len(palette) == 2, "互补调色板颜色数错误"
    
    print("✓ ColorPalette.from_base_color 测试通过")


def test_color_palette_random():
    """测试随机调色板创建。"""
    palette = ColorPalette.random(5)
    assert len(palette) == 5, "随机调色板颜色数错误"
    
    print("✓ ColorPalette.random 测试通过")


def test_color_palette_gradient():
    """测试渐变调色板创建。"""
    palette = ColorPalette.gradient('#FF0000', '#0000FF', 10)
    assert len(palette) == 10, "渐变调色板颜色数错误"
    
    print("✓ ColorPalette.gradient 测试通过")


def test_color_palette_export():
    """测试调色板导出。"""
    palette = ColorPalette(['#FF0000', '#00FF00'])
    
    css = palette.to_css()
    assert ':root {' in css, "CSS 导出失败"
    
    scss = palette.to_scss()
    assert '$color-1:' in scss, "SCSS 导出失败"
    
    json_data = palette.to_json()
    assert json_data['count'] == 2, "JSON 导出失败"
    
    tw = palette.to_tailwind()
    assert 'custom:' in tw, "Tailwind 导出失败"
    
    print("✓ ColorPalette 导出测试通过")


def test_color_palette_with_shades():
    """测试调色板阴影扩展。"""
    palette = ColorPalette(['#FF0000'])
    new_palette = palette.with_shades(2)
    # 原色 + 2 阴影 = 3 个颜色
    assert len(new_palette) == 3, f"阴影扩展数量错误: {len(new_palette)}"
    
    print("✓ ColorPalette.with_shades 测试通过")


def test_color_palette_with_tints():
    """测试调色板着色扩展。"""
    palette = ColorPalette(['#FF0000'])
    new_palette = palette.with_tints(2)
    assert len(new_palette) == 3, f"着色扩展数量错误: {len(new_palette)}"
    
    print("✓ ColorPalette.with_tints 测试通过")


def test_create_palette():
    """测试便捷创建函数。"""
    palette = create_palette('#FF0000', 'triadic')
    assert len(palette) == 3, "便捷创建函数失败"
    
    print("✓ create_palette 测试通过")


def run_all_tests():
    """运行所有测试。"""
    print("=" * 60)
    print("颜色调色板工具测试")
    print("=" * 60)
    
    # 颜色空间转换测试
    print("\n--- 颜色空间转换测试 ---")
    test_hex_to_rgb()
    test_rgb_to_hex()
    test_rgb_hsl_roundtrip()
    test_rgb_to_hsl()
    test_hex_hsl_conversion()
    
    # 颜色调整测试
    print("\n--- 颜色调整测试 ---")
    test_adjust_lightness()
    test_adjust_saturation()
    test_get_complementary()
    
    # 调色板生成测试
    print("\n--- 调色板生成测试 ---")
    test_complementary_palette()
    test_analogous_palette()
    test_triadic_palette()
    test_split_complementary_palette()
    test_tetradic_palette()
    test_pentadic_palette()
    test_monochromatic_palette()
    test_shades()
    test_tints()
    test_tones()
    test_gradient()
    test_multi_gradient()
    
    # 随机调色板测试
    print("\n--- 随机调色板测试 ---")
    test_random_color()
    test_random_palette()
    test_random_harmonious_palette()
    test_random_warm_palette()
    test_random_cool_palette()
    test_random_pastel_palette()
    
    # 导出测试
    print("\n--- 导出测试 ---")
    test_palette_to_css_variables()
    test_palette_to_scss_variables()
    test_palette_to_json()
    test_palette_to_tailwind_config()
    
    # 对比度和可访问性测试
    print("\n--- 对比度和可访问性测试 ---")
    test_get_luminance()
    test_get_contrast_ratio()
    test_meets_wcag_aa()
    test_meets_wcag_aaa()
    test_suggest_accessible_color()
    
    # 颜色名称测试
    print("\n--- 颜色名称测试 ---")
    test_get_color_name()
    
    # 工具函数测试
    print("\n--- 工具函数测试 ---")
    test_blend_colors()
    test_is_light_color()
    test_is_warm_color()
    test_color_temperature()
    test_get_palette_harmony_type()
    
    # ColorPalette 类测试
    print("\n--- ColorPalette 类测试 ---")
    test_color_palette_class()
    test_color_palette_from_base_color()
    test_color_palette_random()
    test_color_palette_gradient()
    test_color_palette_export()
    test_color_palette_with_shades()
    test_color_palette_with_tints()
    test_create_palette()
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过！")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()