"""
Origami Utils 测试模块

测试折纸工具的核心功能
"""



import sys
import os

# Ensure the module directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    OrigamiUtils,
    FoldType,
    PaperSize,
    Crease,
    CreasePattern,
    FoldStep,
    create_square_from_a4,
    classic_crane_creases,
    classic_frog_creases,
    classic_waterbomb_creases,
)


class TestPaperSize(unittest.TestCase):
    """测试纸张尺寸"""
    
    def test_a4_dimensions(self):
        """测试 A4 尺寸"""
        width, height = PaperSize.A4.value
        self.assertEqual(width, 210)
        self.assertEqual(height, 297)
    
    def test_a_series_ratio(self):
        """测试 A 系列宽高比"""
        # A 系列宽高比应为 1:√2
        sqrt2 = math.sqrt(2)
        for paper_size in [PaperSize.A4, PaperSize.A3, PaperSize.A5]:
            width, height = paper_size.value
            ratio = height / width
            self.assertAlmostEqual(ratio, sqrt2, places=2)
    
    def test_letter_dimensions(self):
        """测试 Letter 尺寸"""
        width, height = PaperSize.LETTER.value
        self.assertEqual(width, 216)
        self.assertEqual(height, 279)
    
    def test_square_sizes(self):
        """测试正方形纸张"""
        for paper_size in [PaperSize.SQUARE_15, PaperSize.SQUARE_20, PaperSize.SQUARE_25]:
            width, height = paper_size.value
            self.assertEqual(width, height)


class TestCrease(unittest.TestCase):
    """测试折痕"""
    
    def test_crease_length(self):
        """测试折痕长度计算"""
        crease = Crease((0, 0), (3, 4), FoldType.VALLEY)
        self.assertEqual(crease.length, 5)
    
    def test_crease_midpoint(self):
        """测试折痕中点"""
        crease = Crease((0, 0), (4, 6), FoldType.MOUNTAIN)
        mid = crease.midpoint
        self.assertEqual(mid, (2, 3))
    
    def test_crease_angle(self):
        """测试折痕角度"""
        # 水平折痕
        horizontal = Crease((0, 0), (10, 0), FoldType.VALLEY)
        self.assertAlmostEqual(horizontal.angle, 0, places=2)
        
        # 垂直折痕
        vertical = Crease((0, 0), (0, 10), FoldType.VALLEY)
        self.assertAlmostEqual(vertical.angle, 90, places=2)
        
        # 对角线
        diagonal = Crease((0, 0), (10, 10), FoldType.VALLEY)
        self.assertAlmostEqual(diagonal.angle, 45, places=2)
    
    def test_fold_type(self):
        """测试折叠类型"""
        mountain = Crease((0, 0), (10, 10), FoldType.MOUNTAIN)
        valley = Crease((0, 0), (10, 10), FoldType.VALLEY)
        
        self.assertEqual(mountain.fold_type, FoldType.MOUNTAIN)
        self.assertEqual(valley.fold_type, FoldType.VALLEY)


class TestCreasePattern(unittest.TestCase):
    """测试折痕模式"""
    
    def test_crease_pattern_creation(self):
        """测试创建折痕模式"""
        creases = [
            Crease((0, 0), (10, 10), FoldType.VALLEY),
            Crease((0, 10), (10, 0), FoldType.MOUNTAIN),
        ]
        pattern = CreasePattern(10, 10, creases)
        
        self.assertEqual(pattern.width, 10)
        self.assertEqual(pattern.height, 10)
        self.assertEqual(len(pattern.creases), 2)
    
    def test_get_creases_by_type(self):
        """测试按类型筛选折痕"""
        creases = [
            Crease((0, 0), (10, 10), FoldType.VALLEY),
            Crease((0, 10), (10, 0), FoldType.MOUNTAIN),
            Crease((0, 5), (10, 5), FoldType.VALLEY),
        ]
        pattern = CreasePattern(10, 10, creases)
        
        valley = pattern.get_creases_by_type(FoldType.VALLEY)
        mountain = pattern.get_creases_by_type(FoldType.MOUNTAIN)
        
        self.assertEqual(len(valley), 2)
        self.assertEqual(len(mountain), 1)
    
    def test_total_crease_length(self):
        """测试总折痕长度"""
        creases = [
            Crease((0, 0), (3, 4), FoldType.VALLEY),  # 长度 5
            Crease((0, 0), (6, 8), FoldType.VALLEY),  # 长度 10
        ]
        pattern = CreasePattern(10, 10, creases)
        
        self.assertEqual(pattern.total_crease_length(), 15)
    
    def test_complexity_score(self):
        """测试复杂度评分"""
        # 简单模式
        simple = CreasePattern(10, 10, [Crease((0, 0), (10, 10), FoldType.VALLEY)])
        self.assertEqual(simple.complexity_score(), 1)  # 1 条折痕
        
        # 复杂模式
        creases = [Crease((0, 0), (100, 100), FoldType.VALLEY) for _ in range(10)]
        complex_pattern = CreasePattern(100, 100, creases)
        self.assertGreater(complex_pattern.complexity_score(), 10)


class TestOrigamiUtils(unittest.TestCase):
    """测试折纸工具类"""
    
    def test_paper_dimensions(self):
        """测试获取纸张尺寸"""
        width, height = OrigamiUtils.paper_dimensions(PaperSize.A4)
        self.assertEqual((width, height), (210, 297))
    
    def test_is_square(self):
        """测试判断正方形"""
        self.assertTrue(OrigamiUtils.is_square(10, 10))
        self.assertFalse(OrigamiUtils.is_square(10, 15))
        self.assertTrue(OrigamiUtils.is_square(10.001, 10.001))  # 容差内
    
    def test_make_square_crop(self):
        """测试裁剪为正方形"""
        width, height = OrigamiUtils.make_square(210, 297, 'crop')
        self.assertEqual(width, 210)
        self.assertEqual(height, 210)
    
    def test_make_square_extend(self):
        """测试扩展为正方形"""
        width, height = OrigamiUtils.make_square(210, 297, 'extend')
        self.assertEqual(width, 297)
        self.assertEqual(height, 297)
    
    def test_fold_line_horizontal(self):
        """测试水平折痕"""
        crease = OrigamiUtils.fold_line_coordinate(100, 100, 'horizontal', 0.5)
        self.assertEqual(crease.start, (0, 50))
        self.assertEqual(crease.end, (100, 50))
    
    def test_fold_line_vertical(self):
        """测试垂直折痕"""
        crease = OrigamiUtils.fold_line_coordinate(100, 100, 'vertical', 0.5)
        self.assertEqual(crease.start, (50, 0))
        self.assertEqual(crease.end, (50, 100))
    
    def test_fold_line_diagonal(self):
        """测试对角线折痕"""
        crease = OrigamiUtils.fold_line_coordinate(100, 100, 'diagonal')
        self.assertEqual(crease.start, (0, 0))
        self.assertEqual(crease.end, (100, 100))
        
        crease2 = OrigamiUtils.fold_line_coordinate(100, 100, 'diagonal2')
        self.assertEqual(crease2.start, (100, 0))
        self.assertEqual(crease2.end, (0, 100))
    
    def test_divide_paper(self):
        """测试等分折痕"""
        # 三等分
        creases = OrigamiUtils.divide_paper(100, 100, 3, 'horizontal')
        self.assertEqual(len(creases), 2)
        self.assertAlmostEqual(creases[0].start[1], 100/3, places=2)
        self.assertAlmostEqual(creases[1].start[1], 200/3, places=2)
        
        # 四等分
        creases = OrigamiUtils.divide_paper(100, 100, 4, 'vertical')
        self.assertEqual(len(creases), 3)
    
    def test_grid_creases(self):
        """测试网格折痕"""
        # 3x3 网格
        creases = OrigamiUtils.grid_creases(100, 100, 3, 3)
        self.assertEqual(len(creases), 4)  # 2 水平 + 2 垂直
        
        # 4x4 网格
        creases = OrigamiUtils.grid_creases(100, 100, 4, 4)
        self.assertEqual(len(creases), 6)  # 3 水平 + 3 垂直
    
    def test_rabbit_ear_crease(self):
        """测试兔耳折法"""
        creases = OrigamiUtils.rabbit_ear_crease(100, 100)
        self.assertGreater(len(creases), 0)
    
    def test_waterbomb_base_creases(self):
        """测试水弹基础折痕"""
        pattern = OrigamiUtils.waterbomb_base_creases(100, 100)
        self.assertEqual(pattern.width, 100)
        self.assertEqual(pattern.height, 100)
        self.assertGreater(len(pattern.creases), 0)
    
    def test_preliminary_base_creases(self):
        """测试初步基础折痕"""
        pattern = OrigamiUtils.preliminary_base_creases(100, 100)
        self.assertEqual(len(pattern.creases), 4)  # 2 对角线 + 2 中线
    
    def test_blintz_fold_creases(self):
        """测试 Blintz 折法"""
        pattern = OrigamiUtils.blintz_fold_creases(100, 100)
        self.assertEqual(len(pattern.creases), 4)  # 四角到中心
    
    def test_fish_base_creases(self):
        """测试鱼基础折痕"""
        pattern = OrigamiUtils.fish_base_creases(100, 100)
        self.assertGreater(len(pattern.creases), 0)
    
    def test_bird_base_creases(self):
        """测试鸟基础折痕"""
        pattern = OrigamiUtils.bird_base_creases(100, 100)
        self.assertGreater(len(pattern.creases), 0)
    
    def test_frog_base_creases(self):
        """测试青蛙基础折痕"""
        pattern = OrigamiUtils.frog_base_creases(100, 100)
        self.assertGreater(len(pattern.creases), 0)
    
    def test_fold_angle(self):
        """测试折叠角度计算"""
        # 单层折叠
        angle = OrigamiUtils.fold_angle(1)
        self.assertEqual(angle, 90)  # 单层折成两层，角度 90°
        
        # 多层折叠
        angle = OrigamiUtils.fold_angle(3)
        self.assertEqual(angle, 45)  # 180 / 4 = 45
    
    def test_paper_thickness_after_fold(self):
        """测试折叠后厚度"""
        # 假设纸张厚度 0.1mm
        initial = 0.1
        
        # 折叠 1 次
        self.assertEqual(OrigamiUtils.paper_thickness_after_fold(initial, 1), 0.2)
        
        # 折叠 5 次
        self.assertEqual(OrigamiUtils.paper_thickness_after_fold(initial, 5), 3.2)
        
        # 折叠 10 次
        self.assertAlmostEqual(OrigamiUtils.paper_thickness_after_fold(initial, 10), 102.4, places=2)
    
    def test_max_folds(self):
        """测试最大折叠次数估算"""
        # A4 纸 (厚度约 0.1mm, 长边 297mm)
        max_folds = OrigamiUtils.max_folds(0.1, 297)
        self.assertGreater(max_folds, 5)
        self.assertLess(max_folds, 15)  # 理论估算值范围
    
    def test_mito_creases(self):
        """测试放射状折痕"""
        # 每 30 度一条折痕
        creases = OrigamiUtils.mito_creases(100, 100, 30)
        self.assertEqual(len(creases), 12)  # 360 / 30 = 12
    
    def test_squash_fold_creases(self):
        """测试压折折痕"""
        for corner in ['tl', 'tr', 'bl', 'br']:
            pattern = OrigamiUtils.squash_fold_creases(100, 100, corner)
            self.assertGreater(len(pattern.creases), 0)
    
    def test_reverse_fold_creases(self):
        """测试翻折折痕"""
        pattern_inside = OrigamiUtils.reverse_fold_creases(100, 100, 'inside')
        pattern_outside = OrigamiUtils.reverse_fold_creases(100, 100, 'outside')
        
        self.assertGreater(len(pattern_inside.creases), 0)
        self.assertGreater(len(pattern_outside.creases), 0)
    
    def test_petal_fold_creases(self):
        """测试花瓣折折痕"""
        pattern = OrigamiUtils.petal_fold_creases(100, 100)
        self.assertGreater(len(pattern.creases), 0)
    
    def test_sink_fold_creases(self):
        """测试沉折折痕"""
        pattern = OrigamiUtils.sink_fold_creases(100, 100)
        self.assertGreater(len(pattern.creases), 0)
    
    def test_generate_fold_sequence(self):
        """测试生成折叠步骤"""
        pattern = OrigamiUtils.bird_base_creases(100, 100)
        steps = OrigamiUtils.generate_fold_sequence(pattern)
        
        self.assertGreater(len(steps), 0)
        for step in steps:
            self.assertIsInstance(step, FoldStep)
            self.assertGreater(step.step_number, 0)
            self.assertIsNotNone(step.description)
    
    def test_paper_area(self):
        """测试纸张面积"""
        area = OrigamiUtils.paper_area(10, 20)
        self.assertEqual(area, 200)
    
    def test_paper_perimeter(self):
        """测试纸张周长"""
        perimeter = OrigamiUtils.paper_perimeter(10, 20)
        self.assertEqual(perimeter, 60)
    
    def test_diagonal_length(self):
        """测试对角线长度"""
        diagonal = OrigamiUtils.diagonal_length(3, 4)
        self.assertEqual(diagonal, 5)
    
    def test_aspect_ratio(self):
        """测试宽高比"""
        ratio = OrigamiUtils.aspect_ratio(10, 20)
        self.assertEqual(ratio, 0.5)
    
    def test_is_a_series(self):
        """测试判断 A 系列纸张"""
        # A4 应该被识别
        width, height = PaperSize.A4.value
        self.assertTrue(OrigamiUtils.is_a_series(width, height))
        self.assertTrue(OrigamiUtils.is_a_series(height, width))
        
        # 正方形不应被识别
        self.assertFalse(OrigamiUtils.is_a_series(100, 100))


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_create_square_from_a4(self):
        """测试从 A4 创建正方形"""
        width, height = create_square_from_a4()
        self.assertEqual(width, 210)
        self.assertEqual(height, 210)
    
    def test_classic_crane_creases(self):
        """测试经典千纸鹤折痕"""
        pattern = classic_crane_creases()
        self.assertEqual(pattern.width, 150)
        self.assertEqual(pattern.height, 150)
        self.assertGreater(len(pattern.creases), 0)
    
    def test_classic_frog_creases(self):
        """测试经典青蛙折痕"""
        pattern = classic_frog_creases()
        self.assertEqual(pattern.width, 150)
        self.assertEqual(pattern.height, 150)
        self.assertGreater(len(pattern.creases), 0)
    
    def test_classic_waterbomb_creases(self):
        """测试经典水弹折痕"""
        pattern = classic_waterbomb_creases()
        self.assertEqual(pattern.width, 150)
        self.assertEqual(pattern.height, 150)
        self.assertGreater(len(pattern.creases), 0)


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def test_zero_dimensions(self):
        """测试零尺寸"""
        self.assertEqual(OrigamiUtils.paper_area(0, 10), 0)
        self.assertEqual(OrigamiUtils.paper_area(10, 0), 0)
        self.assertEqual(OrigamiUtils.diagonal_length(0, 10), 10)
        self.assertEqual(OrigamiUtils.max_folds(0.1, 0), 0)
    
    def test_negative_dimensions(self):
        """测试负尺寸"""
        self.assertEqual(OrigamiUtils.paper_area(-10, 10), -100)
    
    def test_empty_crease_pattern(self):
        """测试空折痕模式"""
        pattern = CreasePattern(100, 100, [])
        self.assertEqual(len(pattern.creases), 0)
        self.assertEqual(pattern.total_crease_length(), 0)
        self.assertEqual(pattern.complexity_score(), 0)
    
    def test_single_crease_pattern(self):
        """测试单折痕模式"""
        pattern = CreasePattern(100, 100, [Crease((0, 0), (100, 100), FoldType.VALLEY)])
        self.assertEqual(len(pattern.creases), 1)
        self.assertAlmostEqual(pattern.total_crease_length(), 100 * math.sqrt(2), places=2)
    
    def test_large_divisions(self):
        """测试大等分数"""
        creases = OrigamiUtils.divide_paper(100, 100, 100, 'horizontal')
        self.assertEqual(len(creases), 99)


if __name__ == '__main__':
    unittest.main(verbosity=2)