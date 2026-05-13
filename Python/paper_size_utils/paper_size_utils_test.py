"""
AllToolkit - Python Paper Size Utilities 测试文件

测试纸张尺寸工具模块的所有功能。

Author: AllToolkit
License: MIT
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    PaperSize, PaperSeries,
    get_paper_size, get_all_paper_sizes, get_paper_sizes_by_series,
    search_paper_sizes, list_available_papers,
    mm_to_pixels, pixels_to_mm, inch_to_mm, mm_to_inch,
    calculate_pixels_for_paper, calculate_dpi_for_paper,
    find_paper_by_dimensions, find_paper_by_area, find_paper_by_aspect_ratio,
    calculate_iso_paper_size, scale_paper_to_fit, get_best_fit_paper,
    compare_paper_sizes, print_paper_info, get_version, get_module_info
)


class TestPaperSizeDataClass(unittest.TestCase):
    """测试 PaperSize 数据类。"""
    
    def test_paper_size_creation(self):
        """测试创建纸张尺寸。"""
        paper = PaperSize("Test", 100, 200, PaperSeries.ISO_A, "测试纸张")
        self.assertEqual(paper.name, "Test")
        self.assertEqual(paper.width_mm, 100)
        self.assertEqual(paper.height_mm, 200)
        self.assertEqual(paper.series, PaperSeries.ISO_A)
    
    def test_paper_size_properties(self):
        """测试纸张尺寸属性。"""
        paper = PaperSize("A4", 210, 297, PaperSeries.ISO_A)
        
        # 测试厘米转换
        self.assertEqual(paper.width_cm, 21.0)
        self.assertEqual(paper.height_cm, 29.7)
        
        # 测试英寸转换
        self.assertAlmostEqual(paper.width_inch, 8.2677, places=3)
        self.assertAlmostEqual(paper.height_inch, 11.6929, places=3)
        
        # 测试面积
        self.assertEqual(paper.area_mm2, 210 * 297)
        self.assertEqual(paper.area_cm2, 210 * 297 / 100)
        
        # 测试宽高比
        self.assertAlmostEqual(paper.aspect_ratio, 210 / 297, places=3)
    
    def test_to_pixels(self):
        """测试像素转换。"""
        paper = PaperSize("A4", 210, 297, PaperSeries.ISO_A)
        
        # 300 DPI - 使用近似匹配
        width, height = paper.to_pixels(300)
        self.assertAlmostEqual(width, 2480, delta=5)
        self.assertAlmostEqual(height, 3507, delta=5)
        
        # 72 DPI
        width, height = paper.to_pixels(72)
        self.assertAlmostEqual(width, 595, delta=3)
        self.assertAlmostEqual(height, 842, delta=3)
    
    def test_orientation(self):
        """测试纸张方向。"""
        portrait = PaperSize("A4", 210, 297, PaperSeries.ISO_A)
        landscape = PaperSize("Ledger", 431.8, 279.4, PaperSeries.NORTH_AMERICAN)
        
        self.assertEqual(portrait.get_orientation(), "portrait")
        self.assertEqual(landscape.get_orientation(), "landscape")
    
    def test_flip(self):
        """测试翻转纸张。"""
        paper = PaperSize("A4", 210, 297, PaperSeries.ISO_A)
        flipped = paper.flip()
        
        self.assertEqual(flipped.width_mm, 297)
        self.assertEqual(flipped.height_mm, 210)
    
    def test_to_dict(self):
        """测试字典转换。"""
        paper = PaperSize("A4", 210, 297, PaperSeries.ISO_A)
        d = paper.to_dict()
        
        self.assertEqual(d["name"], "A4")
        self.assertEqual(d["width_mm"], 210)
        self.assertEqual(d["height_mm"], 297)
        self.assertEqual(d["series"], "ISO A")


class TestGetPaperSize(unittest.TestCase):
    """测试获取纸张尺寸功能。"""
    
    def test_get_paper_size_iso_a(self):
        """测试获取 ISO A 系列纸张。"""
        a4 = get_paper_size("A4")
        self.assertIsNotNone(a4)
        self.assertEqual(a4.name, "A4")
        self.assertEqual(a4.width_mm, 210)
        self.assertEqual(a4.height_mm, 297)
        self.assertEqual(a4.series, PaperSeries.ISO_A)
    
    def test_get_paper_size_north_american(self):
        """测试获取北美纸张。"""
        letter = get_paper_size("Letter")
        self.assertIsNotNone(letter)
        self.assertEqual(letter.name, "Letter")
        self.assertAlmostEqual(letter.width_mm, 215.9, places=1)
        self.assertAlmostEqual(letter.height_mm, 279.4, places=1)
    
    def test_get_paper_size_case_insensitive(self):
        """测试大小写不敏感。"""
        a4_upper = get_paper_size("A4")
        a4_lower = get_paper_size("a4")
        
        self.assertIsNotNone(a4_upper)
        self.assertIsNotNone(a4_lower)
        self.assertEqual(a4_upper.name, a4_lower.name)
    
    def test_get_paper_size_unknown(self):
        """测试未知纸张。"""
        unknown = get_paper_size("UnknownPaper")
        self.assertIsNone(unknown)
    
    def test_get_all_paper_sizes(self):
        """测试获取所有纸张。"""
        all_sizes = get_all_paper_sizes()
        self.assertGreater(len(all_sizes), 50)
        self.assertIn("A4", all_sizes)
        self.assertIn("Letter", all_sizes)


class TestPaperSeriesFilter(unittest.TestCase):
    """测试纸张系列过滤。"""
    
    def test_get_iso_a_series(self):
        """测试获取 ISO A 系列。"""
        a_series = get_paper_sizes_by_series(PaperSeries.ISO_A)
        
        # 至少有 A 系列纸张
        self.assertGreaterEqual(len(a_series), 8)
        self.assertIn("A4", a_series)
    
    def test_get_north_american_series(self):
        """测试获取北美系列。"""
        na_series = get_paper_sizes_by_series(PaperSeries.NORTH_AMERICAN)
        
        self.assertIn("Letter", na_series)
        self.assertIn("Legal", na_series)
        self.assertIn("Tabloid", na_series)


class TestSearch(unittest.TestCase):
    """测试搜索功能。"""
    
    def test_search_by_name(self):
        """测试按名称搜索。"""
        results = search_paper_sizes("A4")
        self.assertGreater(len(results), 0)
        
        found_a4 = any(p.name == "A4" for p in results)
        self.assertTrue(found_a4)
    
    def test_search_by_description(self):
        """测试按描述搜索。"""
        results = search_paper_sizes("信封")
        self.assertGreater(len(results), 0)
        
        # 应包含信封尺寸
        found_envelope = any(p.series == PaperSeries.ENVELOPE for p in results)
        self.assertTrue(found_envelope)
    
    def test_search_empty(self):
        """测试搜索无结果。"""
        results = search_paper_sizes("xxx不存在xxx")
        self.assertEqual(len(results), 0)


class TestUnitConversion(unittest.TestCase):
    """测试单位转换功能。"""
    
    def test_mm_to_pixels(self):
        """测试毫米转像素。"""
        # 210mm at 300 DPI ≈ 2480 pixels
        pixels = mm_to_pixels(210, 300)
        self.assertAlmostEqual(pixels, 2480, delta=3)
        
        # 210mm at 72 DPI ≈ 595 pixels
        pixels = mm_to_pixels(210, 72)
        self.assertAlmostEqual(pixels, 595, delta=2)
    
    def test_pixels_to_mm(self):
        """测试像素转毫米。"""
        mm = pixels_to_mm(2480, 300)
        self.assertAlmostEqual(mm, 210.0, delta=1)
        
        mm = pixels_to_mm(595, 72)
        self.assertAlmostEqual(mm, 210.0, delta=1)
    
    def test_inch_to_mm(self):
        """测试英寸转毫米。"""
        mm = inch_to_mm(1)
        self.assertAlmostEqual(mm, 25.4, places=1)
        
        mm = inch_to_mm(8.5)
        self.assertAlmostEqual(mm, 215.9, places=1)
    
    def test_mm_to_inch(self):
        """测试毫米转英寸。"""
        inch = mm_to_inch(25.4)
        self.assertAlmostEqual(inch, 1.0, places=1)
        
        inch = mm_to_inch(210)
        self.assertAlmostEqual(inch, 8.2677, places=2)
    
    def test_conversion_roundtrip(self):
        """测试转换往返。"""
        # mm -> pixels -> mm
        original_mm = 210.5
        dpi = 300
        
        pixels = mm_to_pixels(original_mm, dpi)
        back_mm = pixels_to_mm(pixels, dpi)
        
        self.assertAlmostEqual(original_mm, back_mm, delta=1)


class TestCalculatePixelsForPaper(unittest.TestCase):
    """测试纸张像素计算。"""
    
    def test_calculate_a4_pixels(self):
        """测试计算 A4 像素。"""
        width, height = calculate_pixels_for_paper("A4", 300)
        self.assertAlmostEqual(width, 2480, delta=3)
        self.assertAlmostEqual(height, 3507, delta=3)
    
    def test_calculate_letter_pixels(self):
        """测试计算 Letter 像素。"""
        width, height = calculate_pixels_for_paper("Letter", 300)
        self.assertAlmostEqual(width, 2550, delta=3)
        self.assertAlmostEqual(height, 3300, delta=3)
    
    def test_calculate_unknown_paper(self):
        """测试未知纸张抛出异常。"""
        with self.assertRaises(ValueError):
            calculate_pixels_for_paper("Unknown", 300)


class TestCalculateDPI(unittest.TestCase):
    """测试 DPI 计算。"""
    
    def test_calculate_dpi(self):
        """测试计算 DPI。"""
        # A4 要达到 1920×1080 像素
        dpi = calculate_dpi_for_paper("A4", 1920, 1080)
        
        # DPI 应为正数
        self.assertGreater(dpi, 0)


class TestFindByDimensions(unittest.TestCase):
    """测试按尺寸查找。"""
    
    def test_find_exact_dimensions(self):
        """测试精确尺寸匹配。"""
        papers = find_paper_by_dimensions(210, 297, "mm")
        
        found_a4 = any(p.name == "A4" for p in papers)
        self.assertTrue(found_a4)
    
    def test_find_with_tolerance(self):
        """测试容差匹配。"""
        # 略小于 A4
        papers = find_paper_by_dimensions(208, 295, "mm", tolerance=3)
        
        found_a4 = any(p.name == "A4" for p in papers)
        self.assertTrue(found_a4)
    
    def test_find_different_units(self):
        """测试不同单位。"""
        # 用厘米查找 A4
        papers = find_paper_by_dimensions(21, 29.7, "cm")
        
        found_a4 = any(p.name == "A4" for p in papers)
        self.assertTrue(found_a4)
        
        # 用英寸查找 Letter
        papers = find_paper_by_dimensions(8.5, 11, "inch")
        
        found_letter = any(p.name == "Letter" for p in papers)
        self.assertTrue(found_letter)
    
    def test_find_landscape(self):
        """测试横向查找。"""
        # A4 纵向是 210×297，横向是 297×210
        papers = find_paper_by_dimensions(297, 210, "mm")
        
        found_a4 = any(p.name == "A4" for p in papers)
        self.assertTrue(found_a4)


class TestFindByArea(unittest.TestCase):
    """测试按面积查找。"""
    
    def test_find_by_area_mm2(self):
        """测试按平方毫米查找。"""
        # A4 面积约 62370 mm²
        papers = find_paper_by_area(62370, "mm2")
        
        found_a4 = any(p.name == "A4" for p in papers)
        self.assertTrue(found_a4)
    
    def test_find_by_area_cm2(self):
        """测试按平方厘米查找。"""
        # A4 面积约 623.7 cm²
        papers = find_paper_by_area(623.7, "cm2", tolerance=100)
        
        found_a4 = any(p.name == "A4" for p in papers)
        self.assertTrue(found_a4)


class TestFindByAspectRatio(unittest.TestCase):
    """测试按宽高比查找。"""
    
    def test_find_iso_a_series_by_ratio(self):
        """测试按 ISO A 系列宽高比查找。"""
        # ISO A 系列宽高比为 √2 的倒数 ≈ 0.707
        papers = find_paper_by_aspect_ratio(0.707, tolerance=0.01)
        
        # 应包含 A 系列纸张
        found_a = any(p.series == PaperSeries.ISO_A for p in papers)
        self.assertTrue(found_a)


class TestCalculateISOPaperSize(unittest.TestCase):
    """测试 ISO 纸张尺寸计算。"""
    
    def test_calculate_a4(self):
        """测试计算 A4。"""
        paper = calculate_iso_paper_size("A", 4)
        
        self.assertEqual(paper.name, "A4")
        self.assertAlmostEqual(paper.width_mm, 210, delta=1)
        self.assertAlmostEqual(paper.height_mm, 297, delta=1)
    
    def test_calculate_a0(self):
        """测试计算 A0。"""
        paper = calculate_iso_paper_size("A", 0)
        
        self.assertEqual(paper.name, "A0")
        self.assertEqual(paper.width_mm, 841)
        self.assertEqual(paper.height_mm, 1189)
    
    def test_calculate_extended_sizes(self):
        """测试计算扩展尺寸。"""
        # A11 (超出预定义范围)
        paper = calculate_iso_paper_size("A", 11)
        
        self.assertEqual(paper.name, "A11")
        # A11 应很小
        self.assertLess(paper.width_mm, 30)
        self.assertLess(paper.height_mm, 40)
    
    def test_invalid_series(self):
        """测试无效系列。"""
        with self.assertRaises(ValueError):
            calculate_iso_paper_size("X", 4)
    
    def test_negative_number_not_allowed(self):
        """测试负号数不允许。"""
        # 负数会抛出异常
        with self.assertRaises(ValueError):
            calculate_iso_paper_size("A", -1)


class TestScaleToFit(unittest.TestCase):
    """测试缩放计算。"""
    
    def test_scale_paper_to_fit(self):
        """测试纸张缩放比例。"""
        scale_w, scale_h = scale_paper_to_fit("A4", 400, 400, "mm")
        
        # A4 是 210×297，要缩放到 400×400
        self.assertAlmostEqual(scale_w, 400 / 210, places=1)
        self.assertAlmostEqual(scale_h, 400 / 297, places=1)
    
    def test_scale_unknown_paper(self):
        """测试未知纸张。"""
        with self.assertRaises(ValueError):
            scale_paper_to_fit("Unknown", 400, 400)


class TestGetBestFitPaper(unittest.TestCase):
    """测试最佳匹配纸张。"""
    
    def test_best_fit_for_a4_content(self):
        """测试 A4 内容的最佳匹配。"""
        paper = get_best_fit_paper(200, 280, "mm")
        
        self.assertIsNotNone(paper)
        # 应能容纳 200×280
        self.assertGreaterEqual(paper.width_mm, 200)
        self.assertGreaterEqual(paper.height_mm, 280)
    
    def test_best_fit_for_large_content(self):
        """测试大内容的最佳匹配。"""
        paper = get_best_fit_paper(800, 1100, "mm")
        
        self.assertIsNotNone(paper)
        # A0 或其他大纸张
        self.assertGreaterEqual(paper.width_mm, 800)
        self.assertGreaterEqual(paper.height_mm, 1100)
    
    def test_best_fit_no_match(self):
        """测试无匹配。"""
        # 超大的尺寸
        paper = get_best_fit_paper(5000, 5000, "mm")
        self.assertIsNone(paper)


class TestComparePaperSizes(unittest.TestCase):
    """测试纸张比较。"""
    
    def test_compare_a4_letter(self):
        """测试比较 A4 和 Letter。"""
        result = compare_paper_sizes("A4", "Letter")
        
        self.assertIn("paper1", result)
        self.assertIn("paper2", result)
        self.assertIn("area_ratio", result)
        
        # 面积比例应接近 1
        self.assertAlmostEqual(result["area_ratio"], 1.0, delta=0.1)
    
    def test_compare_same_paper(self):
        """测试比较同一纸张。"""
        result = compare_paper_sizes("A4", "A4")
        
        self.assertEqual(result["area_ratio"], 1.0)
        self.assertEqual(result["larger"], "相同")
    
    def test_compare_unknown_paper(self):
        """测试未知纸张。"""
        with self.assertRaises(ValueError):
            compare_paper_sizes("Unknown", "A4")


class TestPrintPaperInfo(unittest.TestCase):
    """测试打印纸张信息。"""
    
    def test_print_a4_info(self):
        """测试打印 A4 信息。"""
        info = print_paper_info("A4")
        
        self.assertIn("A4", info)
        self.assertIn("210", info)
        self.assertIn("297", info)
        self.assertIn("ISO A", info)
    
    def test_print_unknown_info(self):
        """测试打印未知纸张。"""
        info = print_paper_info("Unknown")
        
        self.assertIn("未知", info)


class TestMiscellaneous(unittest.TestCase):
    """测试杂项功能。"""
    
    def test_get_version(self):
        """测试获取版本。"""
        version = get_version()
        self.assertEqual(version, "1.0.0")
    
    def test_get_module_info(self):
        """测试获取模块信息。"""
        info = get_module_info()
        
        self.assertIn("name", info)
        self.assertIn("version", info)
        self.assertIn("total_paper_sizes", info)
        self.assertGreater(info["total_paper_sizes"], 50)
    
    def test_list_available_papers(self):
        """测试列出可用纸张。"""
        papers = list_available_papers()
        
        self.assertGreater(len(papers), 50)
        self.assertIn("A4", papers)
        self.assertIn("Letter", papers)


class TestPhotoSizes(unittest.TestCase):
    """测试照片尺寸。"""
    
    def test_get_4r(self):
        """测试获取 4R 照片尺寸。"""
        photo = get_paper_size("4R")
        
        self.assertIsNotNone(photo)
        self.assertEqual(photo.series, PaperSeries.PHOTO)
        self.assertEqual(photo.width_mm, 101.6)
        self.assertEqual(photo.height_mm, 152.4)
    
    def test_photo_pixels(self):
        """测试照片像素计算。"""
        width, height = calculate_pixels_for_paper("4R", 300)
        
        # 4R 是 4×6 英寸，300 DPI 应约为 1200×1800
        self.assertAlmostEqual(width, 1200, delta=5)
        self.assertAlmostEqual(height, 1800, delta=5)


class TestBusinessCardSizes(unittest.TestCase):
    """测试名片尺寸。"""
    
    def test_standard_card(self):
        """测试标准名片。"""
        card = get_paper_size("标准名片")
        
        self.assertIsNotNone(card)
        self.assertEqual(card.series, PaperSeries.BUSINESS_CARD)
        self.assertEqual(card.width_mm, 90)
        self.assertEqual(card.height_mm, 55)


class TestEnvelopeSizes(unittest.TestCase):
    """测试信封尺寸。"""
    
    def test_dl_envelope(self):
        """测试 DL 信封。"""
        envelope = get_paper_size("DL")
        
        self.assertIsNotNone(envelope)
        self.assertEqual(envelope.series, PaperSeries.ENVELOPE)
        self.assertEqual(envelope.width_mm, 110)
        self.assertEqual(envelope.height_mm, 220)
    
    def test_envelope_capacity(self):
        """测试信封容纳 A4。"""
        # C4 信封应能容纳 A4
        c4 = get_paper_size("C4")
        a4 = get_paper_size("A4")
        
        self.assertGreater(c4.width_mm, a4.width_mm)
        self.assertGreater(c4.height_mm, a4.height_mm)


if __name__ == '__main__':
    unittest.main(verbosity=2)