#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
color_utils - 测试用例
=====================

测试 Color 类、颜色转换、对比度计算、配色方案等功能。
"""

import pytest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Color,
    parse_hex,
    parse_color,
    rgb_to_hsl,
    hsl_to_rgb,
    rgb_to_hsv,
    hsv_to_rgb,
    rgb_to_cmyk,
    cmyk_to_rgb,
    mix_colors,
    adjust_lightness,
    adjust_saturation,
    calculate_luminance,
    calculate_contrast_ratio,
    wcag_compliance,
    get_complement_color,
    get_analogous_colors,
    get_triadic_colors,
    get_split_complementary_colors,
    get_tetradic_colors,
    get_monochromatic_colors,
    get_shades,
    get_tints,
    get_tones,
    create_gradient,
    create_multi_gradient,
    random_color,
    random_pastel_color,
    random_vibrant_color,
    random_dark_color,
    random_light_color,
    color_name_to_hex,
    hex_to_color_name,
    suggest_text_color,
    hex_to_rgb,
    rgb_to_hex,
    is_valid_hex,
)


class TestColorCreation:
    """测试 Color 类创建"""
    
    def test_from_hex_6_digit(self):
        """测试 6 位 HEX 创建"""
        color = Color.from_hex('#FF0000')
        assert color.r == 255
        assert color.g == 0
        assert color.b == 0
        assert color.hex == '#ff0000'
    
    def test_from_hex_3_digit(self):
        """测试 3 位 HEX 创建"""
        color = Color.from_hex('#F00')
        assert color.r == 255
        assert color.g == 0
        assert color.b == 0
    
    def test_from_hex_8_digit(self):
        """测试 8 位 HEX (带 Alpha)"""
        color = Color.from_hex('#FF000080')
        assert color.r == 255
        assert color.g == 0
        assert color.b == 0
        assert abs(color.a - 0.5) < 0.01
    
    def test_from_rgb(self):
        """测试 RGB 创建"""
        color = Color.from_rgb(0, 255, 0)
        assert color.r == 0
        assert color.g == 255
        assert color.b == 0
    
    def test_from_hsl(self):
        """测试 HSL 创建"""
        # 红色: H=0, S=100, L=50
        color = Color.from_hsl(0, 100, 50)
        assert color.r == 255
        assert color.g == 0
        assert color.b == 0
    
    def test_from_hsv(self):
        """测试 HSV 创建"""
        # 红色: H=0, S=100, V=100
        color = Color.from_hsv(0, 100, 100)
        assert color.r == 255
        assert color.g == 0
        assert color.b == 0
    
    def test_from_cmyk(self):
        """测试 CMYK 创建"""
        # 红色: C=0, M=100, Y=100, K=0
        color = Color.from_cmyk(0, 100, 100, 0)
        assert color.r == 255
        assert color.g == 0
        assert color.b == 0
    
    def test_color_validation(self):
        """测试颜色值验证"""
        # 超出范围的值应该被限制
        color = Color(300, -10, 500)
        assert color.r == 255
        assert color.g == 0
        assert color.b == 255


class TestColorProperties:
    """测试 Color 属性"""
    
    def test_hex_property(self):
        """测试 HEX 属性"""
        color = Color(255, 128, 64)
        assert color.hex == '#ff8040'
    
    def test_rgb_property(self):
        """测试 RGB 属性"""
        color = Color(100, 150, 200)
        assert color.rgb == (100, 150, 200)
    
    def test_rgba_property(self):
        """测试 RGBA 属性"""
        color = Color(100, 150, 200, 0.5)
        assert color.rgba == (100, 150, 200, 0.5)
    
    def test_hsl_property(self):
        """测试 HSL 属性"""
        color = Color.from_hex('#FF0000')
        h, s, l = color.hsl
        assert h == 0
        assert s == 100
        assert l == 50
    
    def test_hsv_property(self):
        """测试 HSV 属性"""
        color = Color.from_hex('#FF0000')
        h, s, v = color.hsv
        assert h == 0
        assert s == 100
        assert v == 100
    
    def test_cmyk_property(self):
        """测试 CMYK 属性"""
        color = Color.from_hex('#FF0000')
        c, m, y, k = color.cmyk
        assert c == 0
        assert m == 100
        assert y == 100
        assert k == 0
    
    def test_luminance_property(self):
        """测试亮度属性"""
        white = Color.from_hex('#FFFFFF')
        black = Color.from_hex('#000000')
        
        assert white.luminance == 1.0
        assert black.luminance == 0.0
    
    def test_is_light_is_dark(self):
        """测试亮度判断"""
        white = Color.from_hex('#FFFFFF')
        black = Color.from_hex('#000000')
        
        assert white.is_light is True
        assert white.is_dark is False
        assert black.is_light is False
        assert black.is_dark is True
    
    def test_to_dict(self):
        """测试字典转换"""
        color = Color.from_hex('#FF0000')
        d = color.to_dict()
        
        assert d['hex'] == '#ff0000'
        assert d['rgb'] == (255, 0, 0)
        assert 'hsl' in d
        assert 'hsv' in d
        assert 'cmyk' in d


class TestColorParsing:
    """测试颜色解析"""
    
    def test_parse_hex_6_digit(self):
        """测试 6 位 HEX 解析"""
        r, g, b, a = parse_hex('#FF0000')
        assert r == 255
        assert g == 0
        assert b == 0
        assert a == 1.0
    
    def test_parse_hex_3_digit(self):
        """测试 3 位 HEX 解析"""
        r, g, b, a = parse_hex('#F00')
        assert r == 255
        assert g == 0
        assert b == 0
    
    def test_parse_hex_with_alpha(self):
        """测试带 Alpha 的 HEX 解析"""
        r, g, b, a = parse_hex('#FF0000FF')
        assert a == 1.0
        
        r, g, b, a = parse_hex('#FF000000')
        assert a == 0.0
    
    def test_parse_hex_no_prefix(self):
        """测试无前缀 HEX 解析"""
        r, g, b, a = parse_hex('FF0000')
        assert r == 255
        assert g == 0
        assert b == 0
    
    def test_parse_color_from_hex(self):
        """测试从 HEX 字符串解析"""
        color = parse_color('#00FF00')
        assert color.g == 255
    
    def test_parse_color_from_tuple(self):
        """测试从元组解析"""
        color = parse_color((255, 0, 0))
        assert color.r == 255
    
    def test_parse_color_from_color(self):
        """测试从 Color 对象解析"""
        original = Color.from_hex('#FF0000')
        color = parse_color(original)
        assert color.r == 255
    
    def test_invalid_hex(self):
        """测试无效 HEX"""
        with pytest.raises(ValueError):
            parse_hex('#FF')


class TestColorConversion:
    """测试颜色转换"""
    
    def test_rgb_to_hsl_red(self):
        """测试红色 RGB 到 HSL"""
        h, s, l = rgb_to_hsl(255, 0, 0)
        assert h == 0
        assert s == 100
        assert l == 50
    
    def test_rgb_to_hsl_green(self):
        """测试绿色 RGB 到 HSL"""
        h, s, l = rgb_to_hsl(0, 255, 0)
        assert h == 120
        assert s == 100
        assert l == 50
    
    def test_rgb_to_hsl_blue(self):
        """测试蓝色 RGB 到 HSL"""
        h, s, l = rgb_to_hsl(0, 0, 255)
        assert h == 240
        assert s == 100
        assert l == 50
    
    def test_rgb_to_hsl_gray(self):
        """测试灰色 RGB 到 HSL"""
        h, s, l = rgb_to_hsl(128, 128, 128)
        assert s == 0  # 灰色饱和度为 0
    
    def test_hsl_to_rgb(self):
        """测试 HSL 到 RGB"""
        r, g, b = hsl_to_rgb(0, 100, 50)
        assert r == 255
        assert g == 0
        assert b == 0
    
    def test_rgb_to_hsv(self):
        """测试 RGB 到 HSV"""
        h, s, v = rgb_to_hsv(255, 0, 0)
        assert h == 0
        assert s == 100
        assert v == 100
    
    def test_hsv_to_rgb(self):
        """测试 HSV 到 RGB"""
        r, g, b = hsv_to_rgb(0, 100, 100)
        assert r == 255
        assert g == 0
        assert b == 0
    
    def test_rgb_to_cmyk(self):
        """测试 RGB 到 CMYK"""
        c, m, y, k = rgb_to_cmyk(255, 0, 0)
        assert c == 0
        assert m == 100
        assert y == 100
        assert k == 0
    
    def test_cmyk_to_rgb(self):
        """测试 CMYK 到 RGB"""
        r, g, b = cmyk_to_rgb(0, 100, 100, 0)
        assert r == 255
        assert g == 0
        assert b == 0
    
    def test_rgb_to_cmyk_black(self):
        """测试黑色 RGB 到 CMYK"""
        c, m, y, k = rgb_to_cmyk(0, 0, 0)
        assert k == 100
    
    def test_rgb_to_cmyk_white(self):
        """测试白色 RGB 到 CMYK"""
        c, m, y, k = rgb_to_cmyk(255, 255, 255)
        assert k == 0
    
    def test_conversion_roundtrip(self):
        """测试转换往返"""
        # RGB -> HSL -> RGB
        original = (200, 100, 50)
        h, s, l = rgb_to_hsl(*original)
        r, g, b = hsl_to_rgb(h, s, l)
        assert abs(r - original[0]) <= 1
        assert abs(g - original[1]) <= 1
        assert abs(b - original[2]) <= 1


class TestColorManipulation:
    """测试颜色操作"""
    
    def test_mix_colors(self):
        """测试颜色混合"""
        red = Color.from_hex('#FF0000')
        blue = Color.from_hex('#0000FF')
        
        purple = mix_colors(red, blue, 0.5)
        assert purple.r == 127
        assert purple.g == 0
        assert purple.b == 127
    
    def test_mix_colors_extreme_ratios(self):
        """测试极端比例混合"""
        red = Color.from_hex('#FF0000')
        blue = Color.from_hex('#0000FF')
        
        # 0% blue = red
        result = mix_colors(red, blue, 0)
        assert result.r == 255
        
        # 100% blue = blue
        result = mix_colors(red, blue, 1)
        assert result.b == 255
    
    def test_adjust_lightness_lighter(self):
        """测试变亮"""
        color = Color.from_hex('#800000')
        lighter = adjust_lightness(color, 0.2)
        
        h, s, l = color.hsl
        h2, s2, l2 = lighter.hsl
        
        assert l2 > l
    
    def test_adjust_lightness_darker(self):
        """测试变暗"""
        color = Color.from_hex('#800000')
        darker = adjust_lightness(color, -0.2)
        
        h, s, l = color.hsl
        h2, s2, l2 = darker.hsl
        
        assert l2 < l
    
    def test_adjust_saturation(self):
        """测试饱和度调整"""
        color = Color.from_hex('#FF0000')
        desaturated = adjust_saturation(color, -1.0)
        
        h, s, l = desaturated.hsl
        assert s == 0  # 完全去饱和
    
    def test_rotate_hue(self):
        """测试色相旋转"""
        red = Color.from_hex('#FF0000')
        
        # 旋转 180° 得到青色
        cyan = red.rotate_hue(180)
        h, s, l = cyan.hsl
        assert h == 180
    
    def test_lighter_darker_methods(self):
        """测试 lighter/darker 方法"""
        color = Color.from_hex('#FF0000')
        
        lighter = color.lighter(0.1)
        darker = color.darker(0.1)
        
        assert lighter.luminance > color.luminance
        assert darker.luminance < color.luminance


class TestContrastRatio:
    """测试对比度计算"""
    
    def test_contrast_black_white(self):
        """测试黑白对比度"""
        black = Color.from_hex('#000000')
        white = Color.from_hex('#FFFFFF')
        
        ratio = calculate_contrast_ratio(black, white)
        assert ratio == 21.0  # 最大对比度
    
    def test_contrast_same_color(self):
        """测试相同颜色对比度"""
        color = Color.from_hex('#FF0000')
        ratio = calculate_contrast_ratio(color, color)
        assert ratio == 1.0  # 最小对比度
    
    def test_wcag_compliance(self):
        """测试 WCAG 合规性"""
        black = Color.from_hex('#000000')
        white = Color.from_hex('#FFFFFF')
        
        compliance = wcag_compliance(black, white)
        
        assert compliance['contrast_ratio'] == 21.0
        assert compliance['aa_normal'] is True
        assert compliance['aa_large'] is True
        assert compliance['aaa_normal'] is True
        assert compliance['aaa_large'] is True
    
    def test_wcag_fail(self):
        """测试 WCAG 不合规"""
        # 灰色对灰色
        gray1 = Color.from_hex('#808080')
        gray2 = Color.from_hex('#909090')
        
        compliance = wcag_compliance(gray1, gray2)
        
        assert compliance['contrast_ratio'] < 4.5
        assert compliance['aa_normal'] is False


class TestColorSchemes:
    """测试配色方案"""
    
    def test_complement(self):
        """测试互补色"""
        red = Color.from_hex('#FF0000')
        complement = get_complement_color(red)
        
        h, s, l = complement.hsl
        assert h == 180  # 红色 + 180° = 青色
    
    def test_analogous(self):
        """测试类似色"""
        red = Color.from_hex('#FF0000')
        analogous = get_analogous_colors(red)
        
        assert len(analogous) == 3
        # 原色 + 左右 30°
        h1, _, _ = analogous[0].hsl
        h2, _, _ = analogous[1].hsl
        h3, _, _ = analogous[2].hsl
        
        assert h1 == 0
        assert abs(h2 - 330) <= 1 or h2 == 330  # 0 - 30 = -30 -> 330
        assert h3 == 30
    
    def test_triadic(self):
        """测试三角色"""
        red = Color.from_hex('#FF0000')
        triadic = get_triadic_colors(red)
        
        assert len(triadic) == 3
        
        h1, _, _ = triadic[0].hsl
        h2, _, _ = triadic[1].hsl
        h3, _, _ = triadic[2].hsl
        
        assert h1 == 0
        assert h2 == 120
        assert h3 == 240
    
    def test_split_complementary(self):
        """测试分裂互补色"""
        red = Color.from_hex('#FF0000')
        split = get_split_complementary_colors(red)
        
        assert len(split) == 3
    
    def test_tetradic(self):
        """测试四角色"""
        red = Color.from_hex('#FF0000')
        tetradic = get_tetradic_colors(red)
        
        assert len(tetradic) == 4
    
    def test_monochromatic(self):
        """测试单色方案"""
        red = Color.from_hex('#FF0000')
        mono = get_monochromatic_colors(red, 5)
        
        assert len(mono) == 5
        
        # 所有颜色色相相同
        for color in mono:
            h, _, _ = color.hsl
            assert h == 0
    
    def test_shades(self):
        """测试色阶（混黑）"""
        red = Color.from_hex('#FF0000')
        shades = get_shades(red, 5)
        
        assert len(shades) == 5
        
        # 从红色到黑色
        assert shades[0].r > shades[-1].r
    
    def test_tints(self):
        """测试色调（混白）"""
        red = Color.from_hex('#FF0000')
        tints = get_tints(red, 5)
        
        assert len(tints) == 5
        
        # 从红色到白色
        assert tints[0].r < tints[-1].r or tints[-1].r == 255
    
    def test_tones(self):
        """测试色调（混灰）"""
        red = Color.from_hex('#FF0000')
        tones = get_tones(red, 5)
        
        assert len(tones) == 5


class TestGradient:
    """测试渐变"""
    
    def test_create_gradient(self):
        """测试创建渐变"""
        red = Color.from_hex('#FF0000')
        blue = Color.from_hex('#0000FF')
        
        gradient = create_gradient(red, blue, 5)
        
        assert len(gradient) == 5
        assert gradient[0] == red
        assert gradient[-1] == blue
    
    def test_create_gradient_two_colors(self):
        """测试两色渐变"""
        red = Color.from_hex('#FF0000')
        blue = Color.from_hex('#0000FF')
        
        gradient = create_gradient(red, blue, 2)
        
        assert len(gradient) == 2
        assert gradient[0] == red
        assert gradient[1] == blue
    
    def test_create_multi_gradient(self):
        """测试多色渐变"""
        red = Color.from_hex('#FF0000')
        green = Color.from_hex('#00FF00')
        blue = Color.from_hex('#0000FF')
        
        gradient = create_multi_gradient([red, green, blue], 9)
        
        assert len(gradient) == 9


class TestRandomColors:
    """测试随机颜色"""
    
    def test_random_color(self):
        """测试随机颜色生成"""
        color = random_color()
        
        assert 0 <= color.r <= 255
        assert 0 <= color.g <= 255
        assert 0 <= color.b <= 255
    
    def test_random_color_with_constraints(self):
        """测试带约束的随机颜色"""
        color = random_color(
            min_brightness=100,
            max_brightness=200,
            min_saturation=50,
            max_saturation=100,
        )
        
        # 验证亮度范围（近似）
        assert 100 <= color.r <= 200 or 100 <= color.g <= 200 or 100 <= color.b <= 200
    
    def test_random_color_hue_range(self):
        """测试色相范围的随机颜色"""
        color = random_color(hue_range=(0, 60))  # 暖色
        
        h, _, _ = color.hsl
        assert 0 <= h <= 60
    
    def test_random_pastel(self):
        """测试柔和色"""
        color = random_pastel_color()
        
        # 柔和色应该较亮
        assert color.is_light or color.luminance > 0.3
    
    def test_random_vibrant(self):
        """测试鲜艳色"""
        color = random_vibrant_color()
        
        h, s, v = color.hsl
        # 鲜艳色饱和度高
        assert s >= 80
    
    def test_random_dark(self):
        """测试深色"""
        color = random_dark_color()
        
        assert color.is_dark
    
    def test_random_light(self):
        """测试浅色"""
        color = random_light_color()
        
        # 浅色应该较亮，但可能有例外
        assert color.luminance >= 0.3 or color.is_light or not color.is_dark


class TestColorNames:
    """测试颜色名称"""
    
    def test_color_name_to_hex(self):
        """测试颜色名称转 HEX"""
        assert color_name_to_hex('red') == '#FF0000'
        assert color_name_to_hex('blue') == '#0000FF'
        assert color_name_to_hex('white') == '#FFFFFF'
        assert color_name_to_hex('black') == '#000000'
    
    def test_color_name_to_hex_unknown(self):
        """测试未知颜色名称"""
        assert color_name_to_hex('unknowncolor') is None
    
    def test_hex_to_color_name(self):
        """测试 HEX 转颜色名称"""
        assert hex_to_color_name('#FF0000') == 'red'
        assert hex_to_color_name('#000000') == 'black'
    
    def test_suggest_text_color_dark_bg(self):
        """测试深色背景的文本颜色建议"""
        black = Color.from_hex('#000000')
        text_color = suggest_text_color(black)
        
        assert text_color.hex == '#ffffff'  # 白色文本
    
    def test_suggest_text_color_light_bg(self):
        """测试浅色背景的文本颜色建议"""
        white = Color.from_hex('#FFFFFF')
        text_color = suggest_text_color(white)
        
        assert text_color.hex == '#000000'  # 黑色文本


class TestUtilityFunctions:
    """测试便捷函数"""
    
    def test_hex_to_rgb(self):
        """测试 hex_to_rgb"""
        r, g, b = hex_to_rgb('#FF0000')
        assert r == 255
        assert g == 0
        assert b == 0
    
    def test_rgb_to_hex(self):
        """测试 rgb_to_hex"""
        hex_color = rgb_to_hex(255, 0, 0)
        assert hex_color == '#ff0000'
    
    def test_is_valid_hex(self):
        """测试 HEX 验证"""
        assert is_valid_hex('#FF0000') is True
        assert is_valid_hex('#F00') is True
        assert is_valid_hex('FF0000') is True
        assert is_valid_hex('#FF0000FF') is True
        assert is_valid_hex('#FF') is False
        assert is_valid_hex('#FFFFF') is False  # 5 位
        assert is_valid_hex('#GGGGGG') is False  # 无效字符


if __name__ == "__main__":
    pytest.main([__file__, "-v"])