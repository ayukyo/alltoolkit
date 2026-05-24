# -*- coding: utf-8 -*-
"""
Aspect Ratio Utilities 测试文件

测试宽高比计算工具的所有功能。

Author: AllToolkit
Version: 1.0.0
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aspect_ratio_utils.mod import (
    # 枚举
    AspectRatioPreset,
    
    # 数据类
    Resolution,
    AspectRatio,
    
    # 核心函数
    gcd,
    simplify_ratio,
    calculate_aspect_ratio,
    is_same_ratio,
    scale_to_width,
    scale_to_height,
    scale_to_fit,
    scale_to_fill,
    calculate_crop,
    calculate_letterbox,
    find_common_resolutions,
    match_preset,
    get_resolution_name,
    calculate_print_size,
    get_optimal_resolution,
    
    # 常量
    COMMON_RESOLUTIONS,
)


class TestGCD(unittest.TestCase):
    """测试最大公约数计算"""
    
    def test_basic_gcd(self):
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(1920, 1080), 120)
        self.assertEqual(gcd(100, 50), 50)
    
    def test_coprime(self):
        self.assertEqual(gcd(17, 13), 1)
        self.assertEqual(gcd(16, 9), 1)
    
    def test_same_number(self):
        self.assertEqual(gcd(100, 100), 100)
    
    def test_one(self):
        self.assertEqual(gcd(1, 100), 1)


class TestSimplifyRatio(unittest.TestCase):
    """测试宽高比简化"""
    
    def test_full_hd(self):
        self.assertEqual(simplify_ratio(1920, 1080), (16, 9))
    
    def test_4k(self):
        self.assertEqual(simplify_ratio(3840, 2160), (16, 9))
    
    def test_square(self):
        self.assertEqual(simplify_ratio(1000, 1000), (1, 1))
    
    def test_portrait(self):
        self.assertEqual(simplify_ratio(1080, 1920), (9, 16))
    
    def test_iphone_ratio(self):
        result = simplify_ratio(1170, 2532)
        self.assertEqual(result, (195, 422))
    
    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            simplify_ratio(0, 100)
        with self.assertRaises(ValueError):
            simplify_ratio(100, 0)
        with self.assertRaises(ValueError):
            simplify_ratio(-100, 100)


class TestResolution(unittest.TestCase):
    """测试分辨率类"""
    
    def test_creation(self):
        res = Resolution(1920, 1080)
        self.assertEqual(res.width, 1920)
        self.assertEqual(res.height, 1080)
    
    def test_invalid_creation(self):
        with self.assertRaises(ValueError):
            Resolution(0, 100)
        with self.assertRaises(ValueError):
            Resolution(100, -1)
    
    def test_pixels(self):
        res = Resolution(1920, 1080)
        self.assertEqual(res.pixels, 2073600)
    
    def test_megapixels(self):
        res = Resolution(3840, 2160)
        self.assertAlmostEqual(res.megapixels, 8.2944, places=4)
    
    def test_aspect_ratio(self):
        res = Resolution(1920, 1080)
        self.assertEqual(res.aspect_ratio, (16, 9))
    
    def test_aspect_ratio_float(self):
        res = Resolution(16, 9)
        self.assertAlmostEqual(res.aspect_ratio_float, 16/9, places=5)
    
    def test_orientation(self):
        self.assertEqual(Resolution(1920, 1080).orientation, "landscape")
        self.assertEqual(Resolution(1080, 1920).orientation, "portrait")
        self.assertEqual(Resolution(1000, 1000).orientation, "square")
    
    def test_is_4k(self):
        self.assertTrue(Resolution(3840, 2160).is_4k)
        self.assertTrue(Resolution(4096, 2160).is_4k)
        self.assertFalse(Resolution(1920, 1080).is_4k)
    
    def test_is_hd(self):
        self.assertTrue(Resolution(1280, 720).is_hd)
        self.assertTrue(Resolution(1920, 1080).is_hd)
        self.assertFalse(Resolution(640, 480).is_hd)
    
    def test_is_full_hd(self):
        self.assertTrue(Resolution(1920, 1080).is_full_hd)
        self.assertFalse(Resolution(1280, 720).is_full_hd)
    
    def test_scale_to_width(self):
        res = Resolution(1920, 1080)
        scaled = res.scale_to_width(3840)
        self.assertEqual(scaled.width, 3840)
        self.assertEqual(scaled.height, 2160)
    
    def test_scale_to_height(self):
        res = Resolution(1920, 1080)
        scaled = res.scale_to_height(2160)
        self.assertEqual(scaled.width, 3840)
        self.assertEqual(scaled.height, 2160)
    
    def test_scale_to_fit(self):
        res = Resolution(1920, 1080)
        # 缩放到更大的区域
        scaled = res.scale_to_fit(3840, 2160)
        self.assertEqual(scaled.width, 3840)
        self.assertEqual(scaled.height, 2160)
        
        # 缩放到更小的区域
        scaled = res.scale_to_fit(960, 540)
        self.assertEqual(scaled.width, 960)
        self.assertEqual(scaled.height, 540)
    
    def test_scale_to_fill(self):
        res = Resolution(1920, 1080)
        # 填充更大的区域
        scaled = res.scale_to_fill(3840, 2160)
        self.assertEqual(scaled.width, 3840)
        self.assertEqual(scaled.height, 2160)
    
    def test_to_tuple(self):
        res = Resolution(1920, 1080)
        self.assertEqual(res.to_tuple(), (1920, 1080))
    
    def test_to_string(self):
        res = Resolution(1920, 1080)
        self.assertEqual(res.to_string(), "1920x1080")
    
    def test_from_string(self):
        res = Resolution.from_string("1920x1080")
        self.assertEqual(res.width, 1920)
        self.assertEqual(res.height, 1080)
        
        res = Resolution.from_string("1920*1080")
        self.assertEqual(res.width, 1920)
        
        res = Resolution.from_string("1920:1080")
        self.assertEqual(res.width, 1920)


class TestAspectRatio(unittest.TestCase):
    """测试宽高比类"""
    
    def test_creation(self):
        ratio = AspectRatio(16, 9)
        self.assertEqual(ratio.width_ratio, 16)
        self.assertEqual(ratio.height_ratio, 9)
    
    def test_ratio_float(self):
        ratio = AspectRatio(16, 9)
        self.assertAlmostEqual(ratio.ratio, 16/9, places=5)
    
    def test_inverse(self):
        ratio = AspectRatio(16, 9)
        inverse = ratio.inverse
        self.assertEqual(inverse.width_ratio, 9)
        self.assertEqual(inverse.height_ratio, 16)
    
    def test_from_float(self):
        ratio = AspectRatio.from_float(1.7778)
        # 应该接近 16:9
        self.assertAlmostEqual(ratio.ratio, 16/9, places=2)
    
    def test_from_resolution(self):
        ratio = AspectRatio.from_resolution(1920, 1080)
        self.assertEqual(ratio.width_ratio, 16)
        self.assertEqual(ratio.height_ratio, 9)
    
    def test_from_preset(self):
        ratio = AspectRatio.from_preset(AspectRatioPreset.WIDESCREEN)
        self.assertEqual(ratio.width_ratio, 16)
        self.assertEqual(ratio.height_ratio, 9)
    
    def test_from_string(self):
        ratio = AspectRatio.from_string("21:9")
        self.assertEqual(ratio.width_ratio, 21)
        self.assertEqual(ratio.height_ratio, 9)
    
    def test_get_resolution_for_width(self):
        ratio = AspectRatio(16, 9)
        res = ratio.get_resolution_for_width(1920)
        self.assertEqual(res.width, 1920)
        self.assertEqual(res.height, 1080)
    
    def test_get_resolution_for_height(self):
        ratio = AspectRatio(16, 9)
        res = ratio.get_resolution_for_height(1080)
        self.assertEqual(res.width, 1920)
        self.assertEqual(res.height, 1080)
    
    def test_equality(self):
        ratio1 = AspectRatio(16, 9)
        ratio2 = AspectRatio(32, 18)  # 等价
        ratio3 = AspectRatio(4, 3)
        
        self.assertEqual(ratio1, ratio2)
        self.assertNotEqual(ratio1, ratio3)


class TestScaleFunctions(unittest.TestCase):
    """测试缩放函数"""
    
    def test_scale_to_width(self):
        new_w, new_h = scale_to_width(1920, 1080, 3840)
        self.assertEqual(new_w, 3840)
        self.assertEqual(new_h, 2160)
    
    def test_scale_to_height(self):
        new_w, new_h = scale_to_height(1920, 1080, 540)
        self.assertEqual(new_w, 960)
        self.assertEqual(new_h, 540)
    
    def test_scale_to_fit_larger(self):
        # 1920x1080 缩放到 3840x2160 区域
        new_w, new_h = scale_to_fit(1920, 1080, 3840, 2160)
        self.assertEqual(new_w, 3840)
        self.assertEqual(new_h, 2160)
    
    def test_scale_to_fit_smaller(self):
        # 1920x1080 缩放到 960x540 区域
        new_w, new_h = scale_to_fit(1920, 1080, 960, 540)
        self.assertEqual(new_w, 960)
        self.assertEqual(new_h, 540)
    
    def test_scale_to_fit_constrained_by_width(self):
        # 1920x1080 缩放到 1000x1000 区域（约束在宽度）
        new_w, new_h = scale_to_fit(1920, 1080, 1000, 1000)
        self.assertEqual(new_w, 1000)
        self.assertEqual(new_h, 562)  # 保持比例
    
    def test_scale_to_fit_constrained_by_height(self):
        # 1080x1920 (竖屏) 缩放到 1000x1000 区域（约束在高度）
        new_w, new_h = scale_to_fit(1080, 1920, 1000, 1000)
        self.assertEqual(new_w, 562)
        self.assertEqual(new_h, 1000)
    
    def test_scale_to_fill(self):
        # 填充到更大区域
        new_w, new_h = scale_to_fill(1920, 1080, 3840, 2160)
        self.assertEqual(new_w, 3840)
        self.assertEqual(new_h, 2160)


class TestCropCalculation(unittest.TestCase):
    """测试裁剪计算"""
    
    def test_crop_wider_image_to_16_9(self):
        # 2560x1080 (21:9) 裁剪到 16:9
        crop = calculate_crop(2560, 1080, "16:9")
        self.assertEqual(crop['height'], 1080)
        self.assertLess(crop['width'], 2560)
        self.assertEqual(crop['y'], 0)  # 居中
    
    def test_crop_taller_image_to_16_9(self):
        # 1080x1920 (9:16) 裁剪到 16:9
        crop = calculate_crop(1080, 1920, "16:9")
        self.assertEqual(crop['width'], 1080)
        self.assertLess(crop['height'], 1920)
        self.assertEqual(crop['x'], 0)  # 居中
    
    def test_crop_square_to_16_9(self):
        # 1000x1000 裁剪到 16:9
        crop = calculate_crop(1000, 1000, "16:9")
        self.assertEqual(crop['width'], 1000)
        self.assertEqual(crop['height'], 562)  # 1000 / (16/9) ≈ 562.5
    
    def test_crop_to_square(self):
        # 1920x1080 裁剪到正方形
        crop = calculate_crop(1920, 1080, "1:1")
        self.assertEqual(crop['height'], 1080)
        self.assertEqual(crop['width'], 1080)
        self.assertEqual(crop['x'], 420)  # (1920-1080)/2
        self.assertEqual(crop['y'], 0)


class TestLetterboxCalculation(unittest.TestCase):
    """测试黑边计算"""
    
    def test_letterbox_wider_source(self):
        # 1920x1080 放入 1080x1920 容器
        result = calculate_letterbox(1920, 1080, 1080, 1920)
        self.assertTrue(result['is_letterbox'])  # 上下黑边
        self.assertEqual(result['video_width'], 1080)
        self.assertEqual(result['video_height'], 608)
    
    def test_letterbox_taller_source(self):
        # 1080x1920 放入 1920x1080 容器
        result = calculate_letterbox(1080, 1920, 1920, 1080)
        self.assertTrue(result['is_pillarbox'])  # 左右黑边
        self.assertEqual(result['video_width'], 608)
        self.assertEqual(result['video_height'], 1080)
    
    def test_no_letterbox_same_ratio(self):
        # 1920x1080 放入 3840x2160 容器（相同比例）
        result = calculate_letterbox(1920, 1080, 3840, 2160)
        self.assertFalse(result['is_letterbox'])
        self.assertFalse(result['is_pillarbox'])
        self.assertEqual(result['video_width'], 3840)
        self.assertEqual(result['video_height'], 2160)


class TestMatchPreset(unittest.TestCase):
    """测试预设匹配"""
    
    def test_match_16_9(self):
        preset = match_preset(1920, 1080)
        self.assertEqual(preset, AspectRatioPreset.WIDESCREEN)
    
    def test_match_4_3(self):
        preset = match_preset(1024, 768)
        self.assertEqual(preset, AspectRatioPreset.CLASSIC_FILM)
    
    def test_match_21_9(self):
        # 2560x1080 实际比例 ≈ 2.37，接近 CINEMA_SCOPE (2.39:1)
        preset = match_preset(2560, 1080)
        # 2560/1080 ≈ 2.37，这与 21:9 (≈2.33) 和 2.39:1 都接近
        # 具体匹配哪个取决于容差计算
        self.assertIsNotNone(preset)
    
    def test_match_square(self):
        preset = match_preset(1080, 1080)
        self.assertEqual(preset, AspectRatioPreset.SQUARE)
    
    def test_no_match(self):
        preset = match_preset(100, 77)  # 奇怪的比例
        self.assertIsNone(preset)
    
    def test_match_with_tolerance(self):
        # 1920x1079 (稍微偏离 16:9)
        preset = match_preset(1920, 1079, tolerance=0.01)
        self.assertEqual(preset, AspectRatioPreset.WIDESCREEN)


class TestResolutionName(unittest.TestCase):
    """测试分辨率名称"""
    
    def test_standard_names(self):
        self.assertIn("1080", get_resolution_name(1920, 1080))
        self.assertIn("720", get_resolution_name(1280, 720))
        self.assertIn("4K", get_resolution_name(3840, 2160))
    
    def test_sd_names(self):
        self.assertIn("480", get_resolution_name(640, 480))
    
    def test_unknown_resolution(self):
        name = get_resolution_name(1234, 567)
        self.assertIn("567", name)


class TestPrintSize(unittest.TestCase):
    """测试打印尺寸计算"""
    
    def test_print_size_300_dpi(self):
        result = calculate_print_size(3000, 2400, dpi=300)
        self.assertEqual(result['inches'], (10.0, 8.0))
        self.assertEqual(result['centimeters'], (25.4, 20.32))
    
    def test_print_size_72_dpi(self):
        result = calculate_print_size(720, 720, dpi=72)
        self.assertEqual(result['inches'], (10.0, 10.0))
    
    def test_print_size_4k(self):
        result = calculate_print_size(3840, 2160, dpi=300)
        self.assertAlmostEqual(result['inches'][0], 12.8, places=1)
        self.assertAlmostEqual(result['inches'][1], 7.2, places=1)


class TestOptimalResolution(unittest.TestCase):
    """测试最优分辨率计算"""
    
    def test_optimal_16_9(self):
        res = get_optimal_resolution("16:9")
        # 由于偶数调整，比例可能不是精确的 16:9，但应该等价
        # 检查比例是否接近 16:9
        actual_ratio = res.width / res.height
        expected_ratio = 16 / 9
        self.assertAlmostEqual(actual_ratio, expected_ratio, places=2)
        self.assertGreaterEqual(res.pixels, 2073600)  # 至少 1080p
        self.assertLessEqual(res.pixels, 8294400)     # 最多 4K
    
    def test_optimal_4_3(self):
        res = get_optimal_resolution("4:3")
        # 检查比例是否接近 4:3
        actual_ratio = res.width / res.height
        expected_ratio = 4 / 3
        self.assertAlmostEqual(actual_ratio, expected_ratio, places=2)
    
    def test_optimal_1_1(self):
        res = get_optimal_resolution("1:1")
        self.assertEqual(res.width, res.height)
    
    def test_optimal_is_even(self):
        # 确保宽高都是偶数（视频编码要求）
        res = get_optimal_resolution("16:9")
        self.assertEqual(res.width % 2, 0)
        self.assertEqual(res.height % 2, 0)


class TestCommonResolutions(unittest.TestCase):
    """测试常见分辨率常量"""
    
    def test_common_resolutions_exist(self):
        self.assertIn('1080p', COMMON_RESOLUTIONS)
        self.assertIn('4k', COMMON_RESOLUTIONS)
        self.assertIn('720p', COMMON_RESOLUTIONS)
    
    def test_common_resolutions_values(self):
        self.assertEqual(COMMON_RESOLUTIONS['1080p'].width, 1920)
        self.assertEqual(COMMON_RESOLUTIONS['1080p'].height, 1080)
        self.assertEqual(COMMON_RESOLUTIONS['4k'].width, 3840)
        self.assertEqual(COMMON_RESOLUTIONS['4k'].height, 2160)
    
    def test_instagram_resolutions(self):
        self.assertEqual(COMMON_RESOLUTIONS['instagram_square'].width, 1080)
        self.assertEqual(COMMON_RESOLUTIONS['instagram_square'].height, 1080)


class TestAspectRatioPreset(unittest.TestCase):
    """测试宽高比预设枚举"""
    
    def test_preset_values(self):
        self.assertEqual(AspectRatioPreset.WIDESCREEN.value, "16:9")
        self.assertEqual(AspectRatioPreset.CLASSIC_FILM.value, "4:3")
        self.assertEqual(AspectRatioPreset.SQUARE.value, "1:1")
    
    def test_preset_count(self):
        # 确保预设数量合理
        self.assertGreater(len(list(AspectRatioPreset)), 10)


class TestFindCommonResolutions(unittest.TestCase):
    """测试查找常见分辨率"""
    
    def test_find_16_9_resolutions(self):
        resolutions = find_common_resolutions("16:9", max_pixels=2073600)
        self.assertGreater(len(resolutions), 0)
        
        # 检查所有分辨率都是 16:9
        for res in resolutions:
            self.assertEqual(simplify_ratio(res.width, res.height), (16, 9))
    
    def test_find_respects_max_pixels(self):
        resolutions = find_common_resolutions("16:9", max_pixels=1000000)
        for res in resolutions:
            self.assertLessEqual(res.pixels, 1000000)
    
    def test_find_4_3_resolutions(self):
        resolutions = find_common_resolutions("4:3")
        self.assertGreater(len(resolutions), 0)
        
        for res in resolutions:
            ratio = simplify_ratio(res.width, res.height)
            self.assertEqual(ratio, (4, 3))


class TestIsSameRatio(unittest.TestCase):
    """测试宽高比比较"""
    
    def test_same_ratio(self):
        self.assertTrue(is_same_ratio(1920, 1080, 3840, 2160))
        self.assertTrue(is_same_ratio(16, 9, 1920, 1080))
    
    def test_different_ratio(self):
        self.assertFalse(is_same_ratio(1920, 1080, 1024, 768))
        self.assertFalse(is_same_ratio(16, 9, 4, 3))
    
    def test_inverse_ratio(self):
        self.assertFalse(is_same_ratio(1920, 1080, 1080, 1920))


if __name__ == '__main__':
    unittest.main(verbosity=2)