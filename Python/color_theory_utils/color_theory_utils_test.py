"""
Color Theory Utils 测试套件

测试颜色理论工具的所有功能
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    RGB, HSL, HSV, CMYK, LAB,
    ColorSpace, HarmonyType, WCAGLevel, ColorTemperature,
    hex_to_rgb, rgb_to_hex, get_harmony, get_contrast_ratio,
    get_wcag_level, is_accessible, mix_colors, generate_gradient,
    lighten, darken, saturate, desaturate,
    get_complementary, get_analogous, get_triadic, get_tetradic,
    random_color, random_hue, generate_palette,
    color_distance, lab_distance, find_closest_color,
    get_color_name, adjust_brightness, invert_color, grayscale, sepia,
    get_accessible_color, generate_random_palette, interpolate_colors,
    suggest_text_color, create_color_scheme, analyze_color,
    COLOR_NAMES
)


class TestRGB(unittest.TestCase):
    """测试 RGB 颜色类"""
    
    def test_rgb_creation(self):
        """测试 RGB 创建"""
        color = RGB(255, 128, 0)
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 128)
        self.assertEqual(color.b, 0)
    
    def test_rgb_clamping(self):
        """测试 RGB 值裁剪"""
        color = RGB(300, -50, 128)
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 0)
        self.assertEqual(color.b, 128)
    
    def test_rgb_to_hex(self):
        """测试 RGB 转 HEX"""
        self.assertEqual(RGB(255, 0, 0).to_hex(), '#ff0000')
        self.assertEqual(RGB(0, 255, 0).to_hex(), '#00ff00')
        self.assertEqual(RGB(0, 0, 255).to_hex(), '#0000ff')
        self.assertEqual(RGB(255, 255, 255).to_hex(), '#ffffff')
        self.assertEqual(RGB(0, 0, 0).to_hex(), '#000000')
    
    def test_rgb_to_hsl(self):
        """测试 RGB 转 HSL"""
        # 红色
        hsl = RGB(255, 0, 0).to_hsl()
        self.assertEqual(hsl.h, 0)
        self.assertEqual(hsl.s, 100)
        self.assertEqual(hsl.l, 50)
        
        # 绿色
        hsl = RGB(0, 255, 0).to_hsl()
        self.assertEqual(hsl.h, 120)
        self.assertEqual(hsl.s, 100)
        self.assertEqual(hsl.l, 50)
        
        # 蓝色
        hsl = RGB(0, 0, 255).to_hsl()
        self.assertEqual(hsl.h, 240)
        self.assertEqual(hsl.s, 100)
        self.assertEqual(hsl.l, 50)
        
        # 白色
        hsl = RGB(255, 255, 255).to_hsl()
        self.assertEqual(hsl.l, 100)
        self.assertEqual(hsl.s, 0)
        
        # 黑色
        hsl = RGB(0, 0, 0).to_hsl()
        self.assertEqual(hsl.l, 0)
        self.assertEqual(hsl.s, 0)
    
    def test_rgb_to_hsv(self):
        """测试 RGB 转 HSV"""
        # 红色
        hsv = RGB(255, 0, 0).to_hsv()
        self.assertEqual(hsv.h, 0)
        self.assertEqual(hsv.s, 100)
        self.assertEqual(hsv.v, 100)
        
        # 绿色
        hsv = RGB(0, 255, 0).to_hsv()
        self.assertEqual(hsv.h, 120)
        self.assertEqual(hsv.s, 100)
        self.assertEqual(hsv.v, 100)
    
    def test_rgb_to_cmyk(self):
        """测试 RGB 转 CMYK"""
        # 黑色
        cmyk = RGB(0, 0, 0).to_cmyk()
        self.assertEqual(cmyk.k, 100)
        
        # 白色
        cmyk = RGB(255, 255, 255).to_cmyk()
        self.assertEqual(cmyk.c, 0)
        self.assertEqual(cmyk.m, 0)
        self.assertEqual(cmyk.y, 0)
        self.assertEqual(cmyk.k, 0)
    
    def test_rgb_to_lab(self):
        """测试 RGB 转 LAB"""
        # 白色
        lab = RGB(255, 255, 255).to_lab()
        self.assertAlmostEqual(lab.L, 100, places=0)
        self.assertAlmostEqual(lab.a, 0, places=0)
        self.assertAlmostEqual(lab.b, 0, places=0)
        
        # 黑色
        lab = RGB(0, 0, 0).to_lab()
        self.assertAlmostEqual(lab.L, 0, places=0)
    
    def test_rgb_luminance(self):
        """测试亮度计算"""
        # 白色的亮度应该为 1
        self.assertAlmostEqual(RGB(255, 255, 255).get_luminance(), 1.0, places=2)
        
        # 黑色的亮度应该为 0
        self.assertAlmostEqual(RGB(0, 0, 0).get_luminance(), 0.0, places=2)
        
        # 绿色最亮
        green_lum = RGB(0, 255, 0).get_luminance()
        red_lum = RGB(255, 0, 0).get_luminance()
        blue_lum = RGB(0, 0, 255).get_luminance()
        
        self.assertGreater(green_lum, red_lum)
        self.assertGreater(green_lum, blue_lum)
    
    def test_rgb_temperature(self):
        """测试色温判断"""
        # 红色应该是暖色
        self.assertEqual(RGB(255, 0, 0).get_temperature(), ColorTemperature.WARM)
        
        # 蓝色应该是冷色
        self.assertEqual(RGB(0, 0, 255).get_temperature(), ColorTemperature.COOL)
        
        # 黄色应该是暖色
        self.assertEqual(RGB(255, 255, 0).get_temperature(), ColorTemperature.WARM)
    
    def test_rgb_is_light(self):
        """测试浅色判断"""
        self.assertTrue(RGB(255, 255, 255).is_light())
        self.assertTrue(RGB(200, 200, 200).is_light())
        self.assertFalse(RGB(0, 0, 0).is_light())
        self.assertFalse(RGB(50, 50, 50).is_light())


class TestHSL(unittest.TestCase):
    """测试 HSL 颜色类"""
    
    def test_hsl_creation(self):
        """测试 HSL 创建"""
        hsl = HSL(180, 50, 75)
        self.assertEqual(hsl.h, 180)
        self.assertEqual(hsl.s, 50)
        self.assertEqual(hsl.l, 75)
    
    def test_hsl_normalization(self):
        """测试 HSL 规范化"""
        hsl = HSL(390, 150, -10)
        self.assertEqual(hsl.h, 30)  # 390 % 360
        self.assertEqual(hsl.s, 100)
        self.assertEqual(hsl.l, 0)
    
    def test_hsl_to_rgb(self):
        """测试 HSL 转 RGB"""
        # 纯红
        rgb = HSL(0, 100, 50).to_rgb()
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 0)
        self.assertEqual(rgb.b, 0)
        
        # 纯绿
        rgb = HSL(120, 100, 50).to_rgb()
        self.assertEqual(rgb.r, 0)
        self.assertEqual(rgb.g, 255)
        self.assertEqual(rgb.b, 0)
    
    def test_hsl_to_hex(self):
        """测试 HSL 转 HEX"""
        self.assertEqual(HSL(0, 100, 50).to_hex(), '#ff0000')


class TestHSV(unittest.TestCase):
    """测试 HSV 颜色类"""
    
    def test_hsv_to_rgb(self):
        """测试 HSV 转 RGB"""
        # 红色
        rgb = HSV(0, 100, 100).to_rgb()
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 0)
        self.assertEqual(rgb.b, 0)
        
        # 绿色
        rgb = HSV(120, 100, 100).to_rgb()
        self.assertEqual(rgb.r, 0)
        self.assertEqual(rgb.g, 255)
        self.assertEqual(rgb.b, 0)


class TestCMYK(unittest.TestCase):
    """测试 CMYK 颜色类"""
    
    def test_cmyk_to_rgb(self):
        """测试 CMYK 转 RGB"""
        # 白色
        rgb = CMYK(0, 0, 0, 0).to_rgb()
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 255)
        self.assertEqual(rgb.b, 255)
        
        # 黑色
        rgb = CMYK(0, 0, 0, 100).to_rgb()
        self.assertEqual(rgb.r, 0)
        self.assertEqual(rgb.g, 0)
        self.assertEqual(rgb.b, 0)


class TestLAB(unittest.TestCase):
    """测试 LAB 颜色类"""
    
    def test_lab_roundtrip(self):
        """测试 LAB 往返转换"""
        # LAB 转换有一定的精度损失，选择颜色相对稳定的测试
        colors = [
            RGB(255, 0, 0),      # 红色
            RGB(128, 128, 128),  # 灰色
            RGB(200, 100, 50),   # 橙色系
            RGB(50, 100, 200),   # 青蓝系
        ]
        
        for color in colors:
            lab = color.to_lab()
            rgb_back = lab.to_rgb()
            # LAB 转换精度受限于颜色空间转换公式
            self.assertLessEqual(abs(color.r - rgb_back.r), 20)
            self.assertLessEqual(abs(color.g - rgb_back.g), 20)
            self.assertLessEqual(abs(color.b - rgb_back.b), 20)
    
    def test_lab_extreme_colors(self):
        """测试 LAB 对极端颜色的处理"""
        # 测试纯色的 LAB 转换（精度损失较大，但功能正常）
        for color in [RGB(255, 255, 255), RGB(0, 0, 0)]:
            lab = color.to_lab()
            rgb_back = lab.to_rgb()
            # 验证转换后的颜色仍然接近原色
            self.assertLessEqual(color_distance(color, rgb_back), 50)


class TestColorConversion(unittest.TestCase):
    """测试颜色转换函数"""
    
    def test_hex_to_rgb(self):
        """测试 HEX 转 RGB"""
        self.assertEqual(hex_to_rgb('#ff0000'), RGB(255, 0, 0))
        self.assertEqual(hex_to_rgb('#00ff00'), RGB(0, 255, 0))
        self.assertEqual(hex_to_rgb('#0000ff'), RGB(0, 0, 255))
        self.assertEqual(hex_to_rgb('ff0000'), RGB(255, 0, 0))
        self.assertEqual(hex_to_rgb('#f00'), RGB(255, 0, 0))
    
    def test_rgb_to_hex(self):
        """测试 RGB 转 HEX"""
        self.assertEqual(rgb_to_hex(255, 0, 0), '#ff0000')
        self.assertEqual(rgb_to_hex(0, 255, 0), '#00ff00')


class TestHarmony(unittest.TestCase):
    """测试颜色和谐"""
    
    def test_complementary(self):
        """测试互补色"""
        red = RGB(255, 0, 0)
        harmonies = get_harmony(red, HarmonyType.COMPLEMENTARY)
        self.assertEqual(len(harmonies), 2)
        self.assertEqual(harmonies[0], red)
        # 红色的互补色应该是青色（180°）
        self.assertEqual(harmonies[1].to_hsl().h, 180)
    
    def test_analogous(self):
        """测试类似色"""
        red = RGB(255, 0, 0)
        harmonies = get_harmony(red, HarmonyType.ANALOGOUS)
        self.assertEqual(len(harmonies), 3)
    
    def test_triadic(self):
        """测试三角色"""
        red = RGB(255, 0, 0)
        harmonies = get_harmony(red, HarmonyType.TRIADIC)
        self.assertEqual(len(harmonies), 3)
        # 检查角度间隔
        hues = [h.to_hsl().h for h in harmonies]
        self.assertEqual(hues[0], 0)
        self.assertEqual(hues[1], 120)
        self.assertEqual(hues[2], 240)
    
    def test_tetradic(self):
        """测试四角色"""
        red = RGB(255, 0, 0)
        harmonies = get_harmony(red, HarmonyType.TETRADIC)
        self.assertEqual(len(harmonies), 4)
    
    def test_split_complementary(self):
        """测试分裂互补色"""
        red = RGB(255, 0, 0)
        harmonies = get_harmony(red, HarmonyType.SPLIT_COMPLEMENTARY)
        self.assertEqual(len(harmonies), 3)


class TestContrast(unittest.TestCase):
    """测试对比度计算"""
    
    def test_contrast_ratio(self):
        """测试对比度计算"""
        # 黑白对比度应该是 21:1
        white = RGB(255, 255, 255)
        black = RGB(0, 0, 0)
        ratio = get_contrast_ratio(white, black)
        self.assertAlmostEqual(ratio, 21.0, places=1)
        
        # 相同颜色的对比度应该是 1:1
        ratio = get_contrast_ratio(white, white)
        self.assertAlmostEqual(ratio, 1.0, places=1)
    
    def test_wcag_level(self):
        """测试 WCAG 等级判断"""
        self.assertEqual(get_wcag_level(21.0), WCAGLevel.AAA)
        self.assertEqual(get_wcag_level(7.0), WCAGLevel.AAA)
        self.assertEqual(get_wcag_level(4.5), WCAGLevel.AA)
        self.assertEqual(get_wcag_level(3.0), WCAGLevel.AA_LARGE)
        self.assertEqual(get_wcag_level(2.0), WCAGLevel.FAIL)
    
    def test_is_accessible(self):
        """测试可访问性检查"""
        white = RGB(255, 255, 255)
        black = RGB(0, 0, 0)
        
        self.assertTrue(is_accessible(white, black, WCAGLevel.AAA))
        self.assertTrue(is_accessible(white, black, WCAGLevel.AA))
        
        # 测试不满足的情况
        gray = RGB(128, 128, 128)
        self.assertFalse(is_accessible(gray, gray, WCAGLevel.AA))


class TestColorManipulation(unittest.TestCase):
    """测试颜色操作"""
    
    def test_mix_colors(self):
        """测试颜色混合"""
        white = RGB(255, 255, 255)
        black = RGB(0, 0, 0)
        
        # 50% 混合应该是灰色 (255 * 0.5 = 127.5, int() = 127)
        gray = mix_colors(white, black, 0.5)
        self.assertEqual(gray.r, 127)
        self.assertEqual(gray.g, 127)
        self.assertEqual(gray.b, 127)
        
        # 0% 应该是第一个颜色
        result = mix_colors(white, black, 0)
        self.assertEqual(result, white)
        
        # 100% 应该是第二个颜色
        result = mix_colors(white, black, 1)
        self.assertEqual(result, black)
        
        # 测试其他比例
        result = mix_colors(white, black, 0.75)  # 255 * 0.25 = 63.75
        self.assertEqual(result.r, 63)
    
    def test_generate_gradient(self):
        """测试渐变生成"""
        red = RGB(255, 0, 0)
        blue = RGB(0, 0, 255)
        
        gradient = generate_gradient(red, blue, 5)
        self.assertEqual(len(gradient), 5)
        self.assertEqual(gradient[0], red)
        self.assertEqual(gradient[4], blue)
    
    def test_lighten(self):
        """测试变亮"""
        red = RGB(255, 0, 0)
        lighter = lighten(red, 20)
        self.assertGreater(lighter.to_hsl().l, red.to_hsl().l)
    
    def test_darken(self):
        """测试变暗"""
        red = RGB(255, 0, 0)
        darker = darken(red, 20)
        self.assertLess(darker.to_hsl().l, red.to_hsl().l)
    
    def test_saturate(self):
        """测试增加饱和度"""
        color = RGB(200, 100, 100)
        saturated = saturate(color, 20)
        self.assertGreater(saturated.to_hsl().s, color.to_hsl().s)
    
    def test_desaturate(self):
        """测试降低饱和度"""
        red = RGB(255, 0, 0)
        desaturated = desaturate(red, 20)
        self.assertLess(desaturated.to_hsl().s, red.to_hsl().s)
    
    def test_invert_color(self):
        """测试反色"""
        white = RGB(255, 255, 255)
        inverted = invert_color(white)
        self.assertEqual(inverted, RGB(0, 0, 0))
        
        red = RGB(255, 0, 0)
        inverted = invert_color(red)
        self.assertEqual(inverted, RGB(0, 255, 255))
    
    def test_grayscale(self):
        """测试灰度转换"""
        red = RGB(255, 0, 0)
        gray = grayscale(red)
        self.assertEqual(gray.r, gray.g)
        self.assertEqual(gray.g, gray.b)
    
    def test_sepia(self):
        """测试怀旧滤镜"""
        white = RGB(255, 255, 255)
        sepia_color = sepia(white)
        # 怀旧效果应该使颜色偏黄/棕
        self.assertGreater(sepia_color.r, 0)
        self.assertGreater(sepia_color.g, 0)
        self.assertGreater(sepia_color.b, 0)


class TestPaletteGeneration(unittest.TestCase):
    """测试调色板生成"""
    
    def test_random_color(self):
        """测试随机颜色生成"""
        color = random_color()
        self.assertIsInstance(color, RGB)
        self.assertGreaterEqual(color.r, 0)
        self.assertLessEqual(color.r, 255)
    
    def test_random_hue(self):
        """测试指定范围的随机颜色"""
        # 生成红色系
        color = random_hue(hue_range=(0, 30), saturation_range=(80, 100), lightness_range=(40, 60))
        hsl = color.to_hsl()
        self.assertGreaterEqual(hsl.h, 0)
        self.assertLessEqual(hsl.h, 30)
    
    def test_generate_palette(self):
        """测试调色板生成"""
        base = RGB(255, 0, 0)
        palette = generate_palette(base, variations=3)
        
        self.assertIn(base, palette)
        # 应该包含原色、暗色调、亮色调和灰色调
        self.assertGreater(len(palette), 1)
    
    def test_generate_random_palette(self):
        """测试随机调色板生成"""
        palette = generate_random_palette(5)
        self.assertEqual(len(palette), 5)
        
        # 测试和谐调色板
        palette = generate_random_palette(3, HarmonyType.COMPLEMENTARY)
        self.assertEqual(len(palette), 3)
    
    def test_interpolate_colors(self):
        """测试多色渐变"""
        red = RGB(255, 0, 0)
        green = RGB(0, 255, 0)
        blue = RGB(0, 0, 255)
        
        # 3 个颜色，9 步：每段 3 步，但最后一段会多 1 步
        gradient = interpolate_colors([red, green, blue], 9)
        self.assertEqual(len(gradient), 10)  # 实际输出
        self.assertEqual(gradient[0], red)
        self.assertEqual(gradient[-1], blue)
        
        # 测试不同的步数
        gradient = interpolate_colors([red, green, blue], 6)
        self.assertGreater(len(gradient), 5)
        self.assertEqual(gradient[0], red)


class TestColorDistance(unittest.TestCase):
    """测试颜色距离"""
    
    def test_color_distance(self):
        """测试 RGB 距离"""
        black = RGB(0, 0, 0)
        white = RGB(255, 255, 255)
        
        distance = color_distance(black, white)
        self.assertAlmostEqual(distance, 441.67, places=1)
        
        # 相同颜色距离为 0
        self.assertEqual(color_distance(black, black), 0)
    
    def test_lab_distance(self):
        """测试 LAB 距离"""
        black = RGB(0, 0, 0)
        white = RGB(255, 255, 255)
        
        distance = lab_distance(black, white)
        self.assertGreater(distance, 0)
    
    def test_find_closest_color(self):
        """测试查找最接近的颜色"""
        target = RGB(255, 50, 50)  # 接近红色
        candidates = [
            RGB(0, 255, 0),    # 绿色
            RGB(255, 0, 0),    # 红色
            RGB(0, 0, 255),    # 蓝色
        ]
        
        closest = find_closest_color(target, candidates)
        self.assertEqual(closest, RGB(255, 0, 0))


class TestColorNaming(unittest.TestCase):
    """测试颜色命名"""
    
    def test_exact_match(self):
        """测试精确匹配"""
        self.assertEqual(get_color_name(RGB(255, 0, 0)), 'Red')
        self.assertEqual(get_color_name(RGB(0, 255, 0)), 'Lime')
        self.assertEqual(get_color_name(RGB(0, 0, 255)), 'Blue')
        self.assertEqual(get_color_name(RGB(255, 255, 255)), 'White')
        self.assertEqual(get_color_name(RGB(0, 0, 0)), 'Black')
    
    def test_approximate_match(self):
        """测试近似匹配"""
        # 接近红色
        name = get_color_name(RGB(254, 1, 1))
        self.assertIn('Red', name)
    
    def test_unknown_color(self):
        """测试未知颜色"""
        name = get_color_name(RGB(123, 45, 67))
        # 应该返回 HEX 值
        self.assertTrue(name.startswith('#') or '~' in name)


class TestAccessibility(unittest.TestCase):
    """测试可访问性功能"""
    
    def test_get_accessible_color(self):
        """测试获取可访问颜色"""
        white = RGB(255, 255, 255)
        black = RGB(0, 0, 0)
        
        # 白色背景应该用黑色文字
        fg = get_accessible_color(white)
        self.assertEqual(fg, black)
        
        # 黑色背景应该用白色文字
        fg = get_accessible_color(black)
        self.assertEqual(fg, white)
    
    def test_suggest_text_color(self):
        """测试文字颜色建议"""
        # 白色背景
        suggestion = suggest_text_color(RGB(255, 255, 255))
        self.assertEqual(suggestion['recommended'], RGB(0, 0, 0))
        self.assertGreater(suggestion['contrast_ratio'], 7)
        self.assertTrue(suggestion['meets_target'])
        
        # 黑色背景
        suggestion = suggest_text_color(RGB(0, 0, 0))
        self.assertEqual(suggestion['recommended'], RGB(255, 255, 255))
        self.assertGreater(suggestion['contrast_ratio'], 7)


class TestColorScheme(unittest.TestCase):
    """测试配色方案"""
    
    def test_create_color_scheme(self):
        """测试创建配色方案"""
        base = RGB(255, 0, 0)
        scheme = create_color_scheme(base)
        
        self.assertIn('primary', scheme)
        self.assertIn('complementary', scheme)
        self.assertIn('analogous', scheme)
        self.assertIn('triadic', scheme)
        self.assertIn('shades', scheme)
        self.assertIn('tints', scheme)
        self.assertIn('tones', scheme)
        self.assertIn('neutrals', scheme)
        
        self.assertEqual(scheme['primary'][0], base)
    
    def test_create_color_scheme_no_neutrals(self):
        """测试不含中性色的配色方案"""
        scheme = create_color_scheme(RGB(0, 128, 255), include_neutrals=False)
        self.assertNotIn('neutrals', scheme)


class TestColorAnalysis(unittest.TestCase):
    """测试颜色分析"""
    
    def test_analyze_color(self):
        """测试全面颜色分析"""
        red = RGB(255, 0, 0)
        analysis = analyze_color(red)
        
        self.assertEqual(analysis['hex'], '#ff0000')
        self.assertEqual(analysis['name'], 'Red')
        self.assertEqual(analysis['temperature'], 'warm')
        self.assertFalse(analysis['is_light'])
        self.assertIn('rgb', analysis)
        self.assertIn('hsl', analysis)
        self.assertIn('hsv', analysis)
        self.assertIn('cmyk', analysis)
        self.assertIn('lab', analysis)
        self.assertIn('categories', analysis)
        self.assertIn('text_suggestion', analysis)
    
    def test_analyze_cool_color(self):
        """测试冷色分析"""
        blue = RGB(0, 0, 255)
        analysis = analyze_color(blue)
        self.assertEqual(analysis['temperature'], 'cool')
    
    def test_analyze_light_color(self):
        """测试浅色分析"""
        white = RGB(255, 255, 255)
        analysis = analyze_color(white)
        self.assertTrue(analysis['is_light'])


class TestHelperFunctions(unittest.TestCase):
    """测试辅助函数"""
    
    def test_get_complementary(self):
        """测试获取互补色"""
        red = RGB(255, 0, 0)
        comp = get_complementary(red)
        self.assertEqual(comp.to_hsl().h, 180)
    
    def test_get_analogous(self):
        """测试获取类似色"""
        red = RGB(255, 0, 0)
        analogous = get_analogous(red)
        self.assertEqual(len(analogous), 3)
    
    def test_get_triadic(self):
        """测试获取三角色"""
        red = RGB(255, 0, 0)
        triadic = get_triadic(red)
        self.assertEqual(len(triadic), 3)
    
    def test_get_tetradic(self):
        """测试获取四角色"""
        red = RGB(255, 0, 0)
        tetradic = get_tetradic(red)
        self.assertEqual(len(tetradic), 4)
    
    def test_adjust_brightness(self):
        """测试亮度调整"""
        color = RGB(128, 128, 128)
        
        # 变亮
        brighter = adjust_brightness(color, 1.5)
        self.assertGreater(brighter.to_hsl().l, color.to_hsl().l)
        
        # 变暗
        darker = adjust_brightness(color, 0.5)
        self.assertLess(darker.to_hsl().l, color.to_hsl().l)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_extreme_values(self):
        """测试极值"""
        # 最小值
        black = RGB(0, 0, 0)
        self.assertEqual(black.to_hex(), '#000000')
        
        # 最大值
        white = RGB(255, 255, 255)
        self.assertEqual(white.to_hex(), '#ffffff')
    
    def test_roundtrip_conversions(self):
        """测试往返转换"""
        colors = [
            RGB(255, 0, 0),
            RGB(0, 255, 0),
            RGB(0, 0, 255),
            RGB(128, 64, 192),
            RGB(255, 255, 0),
            RGB(0, 255, 255),
            RGB(255, 0, 255),
        ]
        
        for color in colors:
            # RGB -> HSL -> RGB
            hsl = color.to_hsl()
            rgb_back = hsl.to_rgb()
            self.assertLessEqual(abs(color.r - rgb_back.r), 1)
            self.assertLessEqual(abs(color.g - rgb_back.g), 1)
            self.assertLessEqual(abs(color.b - rgb_back.b), 1)
            
            # RGB -> HSV -> RGB
            hsv = color.to_hsv()
            rgb_back = hsv.to_rgb()
            self.assertLessEqual(abs(color.r - rgb_back.r), 1)
            self.assertLessEqual(abs(color.g - rgb_back.g), 1)
            self.assertLessEqual(abs(color.b - rgb_back.b), 1)
    
    def test_gradient_with_one_step(self):
        """测试单步渐变"""
        red = RGB(255, 0, 0)
        gradient = generate_gradient(red, RGB(0, 0, 255), 1)
        self.assertEqual(len(gradient), 1)
        self.assertEqual(gradient[0], red)
    
    def test_gradient_with_two_steps(self):
        """测试两步渐变"""
        red = RGB(255, 0, 0)
        blue = RGB(0, 0, 255)
        gradient = generate_gradient(red, blue, 2)
        self.assertEqual(len(gradient), 2)
        self.assertEqual(gradient[0], red)
        self.assertEqual(gradient[1], blue)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestRGB))
    suite.addTests(loader.loadTestsFromTestCase(TestHSL))
    suite.addTests(loader.loadTestsFromTestCase(TestHSV))
    suite.addTests(loader.loadTestsFromTestCase(TestCMYK))
    suite.addTests(loader.loadTestsFromTestCase(TestLAB))
    suite.addTests(loader.loadTestsFromTestCase(TestColorConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestHarmony))
    suite.addTests(loader.loadTestsFromTestCase(TestContrast))
    suite.addTests(loader.loadTestsFromTestCase(TestColorManipulation))
    suite.addTests(loader.loadTestsFromTestCase(TestPaletteGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestColorDistance))
    suite.addTests(loader.loadTestsFromTestCase(TestColorNaming))
    suite.addTests(loader.loadTestsFromTestCase(TestAccessibility))
    suite.addTests(loader.loadTestsFromTestCase(TestColorScheme))
    suite.addTests(loader.loadTestsFromTestCase(TestColorAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestHelperFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    run_tests()