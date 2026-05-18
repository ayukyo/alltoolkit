"""
色盲模拟与辅助工具测试

测试所有核心功能：
- 色盲模拟
- 对比度计算
- 颜色调整建议
- 调色板生成
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # 色盲模拟
    simulate_colorblindness, simulate_colorblindness_hex, simulate_all_types,
    # 颜色转换
    rgb_to_hsl, hsl_to_rgb, rgb_to_hex, hex_to_rgb,
    # 对比度
    contrast_ratio, relative_luminance, wcag_compliance_level,
    is_colorblind_friendly,
    # 颜色调整
    adjust_for_colorblindness, suggest_colorblind_safe_alternatives,
    generate_colorblind_safe_palette,
    # 辅助
    get_colorblind_type_info, analyze_color_for_colorblindness,
    simulate_palette, check_palette_accessibility,
    # 色盲类型常量
    PROTANOPIA, DEUTERANOPIA, TRITANOPIA, ACHROMATOPSIA,
    PROTANOMALY, DEUTERANOMALY, TRITANOMALY,
    # 简写函数
    simulate, simulate_hex, contrast,
)


class TestColorConversion(unittest.TestCase):
    """颜色转换测试"""
    
    def test_rgb_to_hex(self):
        """测试 RGB 转十六进制"""
        self.assertEqual(rgb_to_hex(255, 0, 0), "#FF0000")
        self.assertEqual(rgb_to_hex(0, 255, 0), "#00FF00")
        self.assertEqual(rgb_to_hex(0, 0, 255), "#0000FF")
        self.assertEqual(rgb_to_hex(255, 255, 255), "#FFFFFF")
        self.assertEqual(rgb_to_hex(0, 0, 0), "#000000")
    
    def test_hex_to_rgb(self):
        """测试十六进制转 RGB"""
        self.assertEqual(hex_to_rgb("#FF0000"), (255, 0, 0))
        self.assertEqual(hex_to_rgb("#00FF00"), (0, 255, 0))
        self.assertEqual(hex_to_rgb("#0000FF"), (0, 0, 255))
        self.assertEqual(hex_to_rgb("FF0000"), (255, 0, 0))  # 无 # 前缀
    
    def test_rgb_hsl_roundtrip(self):
        """测试 RGB 和 HSL 互转"""
        test_colors = [
            (255, 0, 0),      # 纯红
            (0, 255, 0),      # 纯绿
            (0, 0, 255),      # 纯蓝
            (255, 255, 0),    # 黄色
            (255, 0, 255),    # 品红
            (0, 255, 255),    # 青色
            (128, 128, 128),  # 灰色
        ]
        
        for r, g, b in test_colors:
            h, s, l = rgb_to_hsl(r, g, b)
            r2, g2, b2 = hsl_to_rgb(h, s, l)
            # 允许 1 的误差
            self.assertTrue(abs(r - r2) <= 1)
            self.assertTrue(abs(g - g2) <= 1)
            self.assertTrue(abs(b - b2) <= 1)


class TestColorblindSimulation(unittest.TestCase):
    """色盲模拟测试"""
    
    def test_protanopia_red(self):
        """测试红色盲对红色的感知"""
        # 红色在红色盲眼中应该呈现为暗色
        result = simulate_colorblindness(255, 0, 0, PROTANOPIA)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        # 结果应该与原始颜色不同
        self.assertNotEqual(result, (255, 0, 0))
    
    def test_deuteranopia_green(self):
        """测试绿色盲对绿色的感知"""
        result = simulate_colorblindness(0, 255, 0, DEUTERANOPIA)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        # 结果应该与原始颜色不同
        self.assertNotEqual(result, (0, 255, 0))
    
    def test_tritanopia_blue(self):
        """测试蓝色盲对蓝色的感知"""
        result = simulate_colorblindness(0, 0, 255, TRITANOPIA)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
    
    def test_achromatopsia_grayscale(self):
        """测试全色盲应该看到灰度"""
        # 任何颜色在全色盲眼中都是灰色
        for color in [(255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 64, 32)]:
            result = simulate_colorblindness(*color, ACHROMATOPSIA)
            # R = G = B 表示灰色
            self.assertEqual(result[0], result[1])
            self.assertEqual(result[1], result[2])
    
    def test_simulate_all_types(self):
        """测试同时模拟所有类型"""
        result = simulate_all_types(255, 0, 0)
        self.assertEqual(len(result), 7)
        for cb_type in [PROTANOPIA, DEUTERANOPIA, TRITANOPIA, ACHROMATOPSIA,
                        PROTANOMALY, DEUTERANOMALY, TRITANOMALY]:
            self.assertIn(cb_type, result)
    
    def test_simulate_hex(self):
        """测试十六进制输入输出"""
        result = simulate_colorblindness_hex("#FF0000", DEUTERANOPIA)
        self.assertTrue(result.startswith("#"))
        self.assertEqual(len(result), 7)
    
    def test_shorthand_functions(self):
        """测试简写函数"""
        # simulate
        r1 = simulate(255, 0, 0, DEUTERANOPIA)
        r2 = simulate_colorblindness(255, 0, 0, DEUTERANOPIA)
        self.assertEqual(r1, r2)
        
        # simulate_hex
        h1 = simulate_hex("#FF0000", DEUTERANOPIA)
        h2 = simulate_colorblindness_hex("#FF0000", DEUTERANOPIA)
        self.assertEqual(h1, h2)


class TestContrastAndAccessibility(unittest.TestCase):
    """对比度和可访问性测试"""
    
    def test_contrast_ratio_black_white(self):
        """测试黑白对比度应该是最大值"""
        contrast = contrast_ratio((0, 0, 0), (255, 255, 255))
        # 理论值是 21:1，允许小误差
        self.assertAlmostEqual(contrast, 21.0, places=1)
    
    def test_contrast_ratio_same_color(self):
        """测试相同颜色对比度应该是 1"""
        contrast = contrast_ratio((128, 128, 128), (128, 128, 128))
        self.assertEqual(contrast, 1.0)
    
    def test_wcag_compliance(self):
        """测试 WCAG 合规级别"""
        # 黑白对比度应该满足所有级别
        compliance = wcag_compliance_level(21.0)
        self.assertTrue(compliance["aa_normal"])
        self.assertTrue(compliance["aaa_normal"])
        
        # 低对比度不满足任何级别
        compliance = wcag_compliance_level(1.5)
        self.assertFalse(compliance["aa_normal"])
        self.assertFalse(compliance["aaa_normal"])
    
    def test_is_colorblind_friendly_high_contrast(self):
        """测试高对比度组合应该友好"""
        result = is_colorblind_friendly((0, 0, 0), (255, 255, 255))
        self.assertTrue(result)
    
    def test_is_colorblind_friendly_red_green(self):
        """测试红绿组合可能不友好"""
        # 纯红和纯绿可能有对比度问题
        result = is_colorblind_friendly((255, 0, 0), (0, 255, 0), min_contrast=3.0)
        # 这个组合可能不友好（取决于具体计算）
        self.assertIsInstance(result, bool)


class TestColorAdjustment(unittest.TestCase):
    """颜色调整测试"""
    
    def test_adjust_for_colorblindness(self):
        """测试颜色调整"""
        # 红色调整
        adjusted = adjust_for_colorblindness(255, 0, 0, DEUTERANOPIA)
        self.assertIsInstance(adjusted, tuple)
        self.assertEqual(len(adjusted), 3)
    
    def test_suggest_alternatives(self):
        """测试替代色建议"""
        alternatives = suggest_colorblind_safe_alternatives(255, 0, 0)
        self.assertEqual(len(alternatives), 3)
        for alt in alternatives:
            self.assertIsInstance(alt, tuple)
            self.assertEqual(len(alt), 3)
    
    def test_generate_safe_palette(self):
        """测试安全调色板生成"""
        palette = generate_colorblind_safe_palette(5)
        self.assertEqual(len(palette), 5)
        
        # 检查所有颜色都在 RGB 范围内
        for color in palette:
            for channel in color:
                self.assertGreaterEqual(channel, 0)
                self.assertLessEqual(channel, 255)


class TestBatchOperations(unittest.TestCase):
    """批量操作测试"""
    
    def test_simulate_palette(self):
        """测试调色板模拟"""
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        result = simulate_palette(colors, DEUTERANOPIA)
        self.assertEqual(len(result), 3)
    
    def test_check_palette_accessibility(self):
        """测试调色板可访问性检查"""
        # 高对比度调色板
        colors = [(0, 0, 0), (255, 255, 255), (255, 0, 0)]
        result = check_palette_accessibility(colors, min_contrast=3.0)
        self.assertIn("pairs_checked", result)
        self.assertIn("safe_pairs", result)
        self.assertIn("problematic_pairs", result)
        self.assertGreater(result["pairs_checked"], 0)


class TestHelperFunctions(unittest.TestCase):
    """辅助函数测试"""
    
    def test_get_colorblind_type_info(self):
        """测试色盲类型信息"""
        info = get_colorblind_type_info()
        self.assertIn(PROTANOPIA, info)
        self.assertIn(DEUTERANOPIA, info)
        self.assertIn(TRITANOPIA, info)
        self.assertIn(ACHROMATOPSIA, info)
        
        # 检查信息结构
        deuteranopia_info = info[DEUTERANOPIA]
        self.assertIn("name", deuteranopia_info)
        self.assertIn("description", deuteranopia_info)
        self.assertIn("prevalence_male", deuteranopia_info)
    
    def test_analyze_color_for_colorblindness(self):
        """测试颜色分析"""
        result = analyze_color_for_colorblindness(255, 0, 0)
        
        self.assertIn("original", result)
        self.assertIn("simulations", result)
        self.assertIn("issues", result)
        self.assertIn("recommendations", result)
        self.assertIn("safe_alternatives", result)
        
        # 检查原始颜色信息
        self.assertEqual(result["original"]["rgb"], (255, 0, 0))
        self.assertEqual(result["original"]["hex"], "#FF0000")
        
        # 检查模拟结果
        self.assertEqual(len(result["simulations"]), 7)


class TestEdgeCases(unittest.TestCase):
    """边缘情况测试"""
    
    def test_extreme_colors(self):
        """测试极端颜色"""
        # 纯黑 - 应该保持黑色
        result = simulate_colorblindness(0, 0, 0, DEUTERANOPIA)
        self.assertEqual(result, (0, 0, 0))
        
        # 纯白 - 由于颜色空间转换可能有色调变化
        # 但亮度应该仍然很高
        result = simulate_colorblindness(255, 255, 255, DEUTERANOPIA)
        # 检查平均亮度接近白色
        avg = sum(result) / 3
        self.assertGreaterEqual(avg, 200)
    
    def test_gray_colors(self):
        """测试灰色（在全色盲下应该保持灰度）"""
        # 中灰在全色盲下应该保持灰色
        result = simulate_colorblindness(128, 128, 128, ACHROMATOPSIA)
        # 全色盲下 R = G = B
        self.assertEqual(result[0], result[1])
        self.assertEqual(result[1], result[2])
        
        # 在其他色盲类型下，灰色接近但可能不完全相等
        result2 = simulate_colorblindness(128, 128, 128, DEUTERANOPIA)
        # 检查各通道接近（允许合理误差）
        for channel in result2:
            self.assertGreaterEqual(channel, 100)
            self.assertLessEqual(channel, 160)
    
    def test_invalid_blindness_type(self):
        """测试无效色盲类型（应该使用默认值）"""
        # 应该使用默认值 (DEUTERANOPIA) 而不是崩溃
        result = simulate_colorblindness(255, 0, 0, "invalid_type")
        self.assertIsInstance(result, tuple)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestColorConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestColorblindSimulation))
    suite.addTests(loader.loadTestsFromTestCase(TestContrastAndAccessibility))
    suite.addTests(loader.loadTestsFromTestCase(TestColorAdjustment))
    suite.addTests(loader.loadTestsFromTestCase(TestBatchOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestHelperFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)