"""
fractal_utils 测试用例

Author: AllToolkit
Date: 2026-05-24
"""

import unittest
from math import log, sqrt
from mod import (
    Point, FractalConfig,
    MandelbrotSet, JuliaSet, SierpinskiTriangle, KochCurve,
    BarnsleyFern, DragonCurve, HilbertCurve, CantorSet,
    FractalDimension, CellularAutomaton,
    mandelbrot_ascii, julia_ascii, sierpinski_ascii,
    koch_snowflake_ascii, barnsley_fern_ascii, dragon_curve_ascii,
    hilbert_curve_ascii, cantor_set_ascii, cellular_automaton_ascii,
    get_fractal_info
)


class TestPoint(unittest.TestCase):
    """测试 Point 类"""
    
    def test_point_creation(self):
        """测试点创建"""
        p = Point(1.0, 2.0)
        self.assertEqual(p.x, 1.0)
        self.assertEqual(p.y, 2.0)
    
    def test_point_addition(self):
        """测试点加法"""
        p1 = Point(1.0, 2.0)
        p2 = Point(3.0, 4.0)
        result = p1 + p2
        self.assertEqual(result.x, 4.0)
        self.assertEqual(result.y, 6.0)
    
    def test_point_subtraction(self):
        """测试点减法"""
        p1 = Point(5.0, 7.0)
        p2 = Point(2.0, 3.0)
        result = p1 - p2
        self.assertEqual(result.x, 3.0)
        self.assertEqual(result.y, 4.0)
    
    def test_point_multiplication(self):
        """测试点与标量乘法"""
        p = Point(2.0, 3.0)
        result = p * 2
        self.assertEqual(result.x, 4.0)
        self.assertEqual(result.y, 6.0)
    
    def test_distance(self):
        """测试距离计算"""
        p1 = Point(0.0, 0.0)
        p2 = Point(3.0, 4.0)
        distance = p1.distance_to(p2)
        self.assertEqual(distance, 5.0)


class TestFractalConfig(unittest.TestCase):
    """测试 FractalConfig 类"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = FractalConfig()
        self.assertEqual(config.width, 80)
        self.assertEqual(config.height, 40)
        self.assertEqual(config.max_iterations, 100)
        self.assertEqual(config.x_min, -2.0)
        self.assertEqual(config.x_max, 2.0)
    
    def test_custom_config(self):
        """测试自定义配置"""
        config = FractalConfig(width=100, height=50, max_iterations=200)
        self.assertEqual(config.width, 100)
        self.assertEqual(config.height, 50)
        self.assertEqual(config.max_iterations, 200)


class TestMandelbrotSet(unittest.TestCase):
    """测试 Mandelbrot 集"""
    
    def test_iterate_in_set(self):
        """测试在集合内的点"""
        # c = 0 应该在集合内
        iterations = MandelbrotSet.iterate(0.0, 0.0, 100)
        self.assertEqual(iterations, 100)
    
    def test_iterate_out_set(self):
        """测试在集合外的点"""
        # c = 2+2i 应该快速逃逸
        iterations = MandelbrotSet.iterate(2.0, 2.0, 100)
        self.assertLess(iterations, 5)
    
    def test_iterate_boundary(self):
        """测试边界附近的点"""
        # c = -0.5+0i 应该迭代一定次数
        iterations = MandelbrotSet.iterate(-0.5, 0.0, 100)
        self.assertGreater(iterations, 10)
    
    def test_generate_ascii(self):
        """测试 ASCII 艺术生成"""
        config = FractalConfig(width=20, height=10)
        ascii_art = MandelbrotSet.generate_ascii(config)
        
        # 应该是多行字符串
        lines = ascii_art.split("\n")
        self.assertEqual(len(lines), 10)
        self.assertEqual(len(lines[0]), 20)
    
    def test_generate_data(self):
        """测试数值数据生成"""
        config = FractalConfig(width=10, height=5)
        data = MandelbrotSet.generate_data(config)
        
        self.assertEqual(len(data), 5)
        self.assertEqual(len(data[0]), 10)
    
    def test_zoom(self):
        """测试缩放配置"""
        config = MandelbrotSet.zoom(-0.5, 0.0, 0.1)
        self.assertAlmostEqual(config.x_min, -0.6)
        self.assertAlmostEqual(config.x_max, -0.4)


class TestJuliaSet(unittest.TestCase):
    """测试 Julia 集"""
    
    def test_classic_params(self):
        """测试经典参数"""
        params = JuliaSet.get_classic_params("dendrite")
        self.assertEqual(params, (-0.8, 0.156))
        
        params = JuliaSet.get_classic_params("rabbit")
        self.assertEqual(params, (-0.4, 0.6))
    
    def test_invalid_params(self):
        """测试无效参数名"""
        params = JuliaSet.get_classic_params("invalid")
        self.assertIsNone(params)
    
    def test_iterate(self):
        """测试迭代"""
        # 使用经典参数
        iterations = JuliaSet.iterate(0.0, 0.0, -0.8, 0.156, 100)
        self.assertGreater(iterations, 0)
    
    def test_generate_ascii(self):
        """测试 ASCII 艺术生成"""
        config = FractalConfig(width=20, height=10)
        ascii_art = JuliaSet.generate_ascii(-0.4, 0.6, config)
        
        lines = ascii_art.split("\n")
        self.assertEqual(len(lines), 10)
    
    def test_generate_data(self):
        """测试数值数据生成"""
        config = FractalConfig(width=10, height=5)
        data = JuliaSet.generate_data(-0.4, 0.6, config)
        
        self.assertEqual(len(data), 5)
        self.assertEqual(len(data[0]), 10)


class TestSierpinskiTriangle(unittest.TestCase):
    """测试 Sierpinski 三角形"""
    
    def test_generate_ascii(self):
        """测试 ASCII 艺术生成"""
        ascii_art = SierpinskiTriangle.generate_ascii(16)
        
        lines = ascii_art.split("\n")
        self.assertEqual(len(lines), 16)
    
    def test_generate_points(self):
        """测试混沌游戏生成点"""
        points = SierpinskiTriangle.generate_points(iterations=4)
        
        # 点数应该约为 2^4
        self.assertGreater(len(points), 10)
        
        # 点应该在 [0, 1] 范围内
        for p in points:
            self.assertGreaterEqual(p.x, 0)
            self.assertLessEqual(p.x, 1)
            self.assertGreaterEqual(p.y, 0)
            self.assertLessEqual(p.y, 1)
    
    def test_area_ratio(self):
        """测试面积比例"""
        ratio = SierpinskiTriangle.calculate_area_ratio(1)
        self.assertEqual(ratio, 0.75)
        
        ratio = SierpinskiTriangle.calculate_area_ratio(2)
        self.assertEqual(ratio, 0.5625)
    
    def test_triangle_count(self):
        """测试三角形数量"""
        count = SierpinskiTriangle.calculate_triangle_count(1)
        self.assertEqual(count, 3)
        
        count = SierpinskiTriangle.calculate_triangle_count(2)
        self.assertEqual(count, 9)


class TestKochCurve(unittest.TestCase):
    """测试 Koch 曲线"""
    
    def test_generate_points(self):
        """测试点生成"""
        points = KochCurve.generate_points(iterations=2, length=100.0)
        
        # 每次迭代点数增加 4 倍（减 3）
        # iterations=2: 2 -> 5 -> 17
        self.assertGreater(len(points), 2)
    
    def test_generate_koch_snowflake(self):
        """测试 Koch 雪花"""
        points = KochCurve.generate_koch_snowflake(iterations=2, size=60.0)
        
        self.assertGreater(len(points), 3)
    
    def test_length_ratio(self):
        """测试长度比例"""
        ratio = KochCurve.calculate_length_ratio(1)
        self.assertEqual(ratio, 4 / 3)
        
        ratio = KochCurve.calculate_length_ratio(2)
        self.assertEqual(ratio, (4 / 3) ** 2)


class TestBarnsleyFern(unittest.TestCase):
    """测试 Barnsley 羊齿草"""
    
    def test_generate_points(self):
        """测试点生成"""
        points = BarnsleyFern.generate_points(num_points=1000)
        
        self.assertEqual(len(points), 1001)  # 包含初始点
        
        # 点应该在合理范围内
        x_values = [p.x for p in points]
        y_values = [p.y for p in points]
        
        # Barnsley 羊齿草的典型范围
        self.assertGreaterEqual(min(x_values), -3.0)
        self.assertLessEqual(max(x_values), 3.0)
        self.assertGreaterEqual(min(y_values), 0)
        self.assertLessEqual(max(y_values), 10)
    
    def test_generate_ascii(self):
        """测试 ASCII 艺术生成"""
        ascii_art = BarnsleyFern.generate_ascii(width=40, height=30, num_points=1000)
        
        lines = ascii_art.split("\n")
        self.assertEqual(len(lines), 30)


class TestDragonCurve(unittest.TestCase):
    """测试 Dragon 曲线"""
    
    def test_generate_turns(self):
        """测试转向序列生成"""
        turns = DragonCurve.generate_turns(1)
        self.assertEqual(turns, ["R"])
        
        turns = DragonCurve.generate_turns(2)
        # 期望: R R L
        self.assertEqual(len(turns), 3)
    
    def test_generate_points(self):
        """测试点生成"""
        points = DragonCurve.generate_points(iterations=4)
        
        # 线段数 = 2^iterations
        segment_count = DragonCurve.calculate_segments(4)
        self.assertEqual(segment_count, 16)
        
        # 点数 = 线段数 + 1
        self.assertEqual(len(points), segment_count + 1)
    
    def test_calculate_segments(self):
        """测试线段数量计算"""
        self.assertEqual(DragonCurve.calculate_segments(1), 2)
        self.assertEqual(DragonCurve.calculate_segments(2), 4)
        self.assertEqual(DragonCurve.calculate_segments(5), 32)


class TestHilbertCurve(unittest.TestCase):
    """测试 Hilbert 曲线"""
    
    def test_generate_points(self):
        """测试点生成"""
        points = HilbertCurve.generate_points(order=2)
        
        # order=2 生成 4^2 = 16 个点
        self.assertEqual(len(points), 16)
    
    def test_xy2d(self):
        """测试坐标转换"""
        n = 4
        # 测试一些坐标
        d = HilbertCurve.xy2d(n, 0, 0)
        self.assertGreaterEqual(d, 0)
        self.assertLess(d, n * n)
    
    def test_d2xy_roundtrip(self):
        """测试坐标往返转换"""
        n = 4
        for d in range(n * n):
            x, y = HilbertCurve._d2xy(n, d)
            d2 = HilbertCurve.xy2d(n, x, y)
            self.assertEqual(d, d2)
    
    def test_generate_ascii(self):
        """测试 ASCII 艺术生成"""
        ascii_art = HilbertCurve.generate_ascii(order=2)
        
        # 应该是多行字符串
        lines = ascii_art.split("\n")
        self.assertGreater(len(lines), 0)


class TestCantorSet(unittest.TestCase):
    """测试 Cantor 集"""
    
    def test_generate_segments(self):
        """测试线段生成"""
        segments = CantorSet.generate_segments(iterations=1)
        
        # iterations=1: 初始线段分成左右两段
        self.assertEqual(len(segments), 2)
    
    def test_generate_segments_deep(self):
        """测试深度迭代"""
        segments = CantorSet.generate_segments(iterations=3)
        
        # 线段数 = 2^iterations
        self.assertEqual(len(segments), 8)
    
    def test_generate_ascii(self):
        """测试 ASCII 艺术生成"""
        ascii_art = CantorSet.generate_ascii(iterations=3, width=80)
        
        lines = ascii_art.split("\n")
        self.assertEqual(len(lines), 4)  # iterations + 1 行
    
    def test_length_ratio(self):
        """测试长度比例"""
        ratio = CantorSet.calculate_length_ratio(1)
        self.assertEqual(ratio, 2 / 3)
        
        ratio = CantorSet.calculate_length_ratio(2)
        self.assertEqual(ratio, (2 / 3) ** 2)
    
    def test_segment_count(self):
        """测试线段数量"""
        self.assertEqual(CantorSet.calculate_segment_count(1), 2)
        self.assertEqual(CantorSet.calculate_segment_count(2), 4)
        self.assertEqual(CantorSet.calculate_segment_count(5), 32)


class TestFractalDimension(unittest.TestCase):
    """测试分形维度"""
    
    def test_sierpinski_dimension(self):
        """测试 Sierpinski 三角形维度"""
        # Sierpinski 三角形的理论维度 = log(3)/log(2) ≈ 1.585
        theoretical = log(3) / log(2)
        
        # 生成一些点进行测试（精度有限）
        points = SierpinskiTriangle.generate_points(iterations=8)
        dimension = FractalDimension.box_counting(points, [0.05, 0.1, 0.2, 0.4])
        
        # 由于简化算法，维度值会有误差，但应该接近理论值
        self.assertGreater(dimension, 1.3)
        self.assertLess(dimension, 1.8)


class TestCellularAutomaton(unittest.TestCase):
    """测试细胞自动机"""
    
    def test_generate_1d(self):
        """测试一维细胞自动机"""
        ascii_art = CellularAutomaton.generate_1d(rule=90, iterations=10, width=40)
        
        lines = ascii_art.split("\n")
        self.assertEqual(len(lines), 10)
        self.assertEqual(len(lines[0]), 40)
    
    def test_get_classic_rules(self):
        """测试经典规则"""
        rules = CellularAutomaton.get_classic_rules()
        
        self.assertEqual(rules["sierpinski"], 90)
        self.assertEqual(rules["triangles"], 60)
        self.assertEqual(rules["solid"], 255)
    
    def test_sierpinski_rule(self):
        """测试 Sierpinski 规则"""
        # Rule 90 应该生成类似 Sierpinski 三角形
        ascii_art = CellularAutomaton.generate_1d(rule=90, iterations=8, width=16)
        
        # 第一行应该是中心一个星号
        lines = ascii_art.split("\n")
        first_line = lines[0]
        
        # 检查中心位置
        center = len(first_line) // 2
        self.assertEqual(first_line[center], "*")


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_mandelbrot_ascii(self):
        """测试 Mandelbrot 便捷函数"""
        config = FractalConfig(width=20, height=10)
        ascii_art = mandelbrot_ascii(config)
        
        self.assertIsInstance(ascii_art, str)
        self.assertIn("\n", ascii_art)
    
    def test_julia_ascii(self):
        """测试 Julia 便捷函数"""
        ascii_art = julia_ascii(-0.4, 0.6)
        
        self.assertIsInstance(ascii_art, str)
    
    def test_sierpinski_ascii(self):
        """测试 Sierpinski 便捷函数"""
        ascii_art = sierpinski_ascii(16)
        
        self.assertIsInstance(ascii_art, str)
    
    def test_koch_snowflake_ascii(self):
        """测试 Koch 雪花便捷函数"""
        ascii_art = koch_snowflake_ascii(2)
        
        self.assertIsInstance(ascii_art, str)
    
    def test_barnsley_fern_ascii(self):
        """测试 Barnsley 羊齿草便捷函数"""
        ascii_art = barnsley_fern_ascii(width=40, height=30)
        
        self.assertIsInstance(ascii_art, str)
    
    def test_dragon_curve_ascii(self):
        """测试 Dragon 曲线便捷函数"""
        ascii_art = dragon_curve_ascii(8)
        
        self.assertIsInstance(ascii_art, str)
    
    def test_hilbert_curve_ascii(self):
        """测试 Hilbert 曲线便捷函数"""
        ascii_art = hilbert_curve_ascii(2)
        
        self.assertIsInstance(ascii_art, str)
    
    def test_cantor_set_ascii(self):
        """测试 Cantor 集便捷函数"""
        ascii_art = cantor_set_ascii(3)
        
        self.assertIsInstance(ascii_art, str)
    
    def test_cellular_automaton_ascii(self):
        """测试细胞自动机便捷函数"""
        ascii_art = cellular_automaton_ascii(rule=90, iterations=10)
        
        self.assertIsInstance(ascii_art, str)
    
    def test_get_fractal_info(self):
        """测试分形信息获取"""
        info = get_fractal_info()
        
        self.assertIn("mandelbrot", info)
        self.assertIn("julia", info)
        self.assertIn("sierpinski", info)
        self.assertIn("koch", info)
        
        # 检查维度值
        self.assertEqual(info["mandelbrot"]["dimension"], 2.0)
        self.assertAlmostEqual(info["sierpinski"]["dimension"], log(3) / log(2), places=3)
        self.assertAlmostEqual(info["cantor"]["dimension"], log(2) / log(3), places=3)


class TestPointOperations(unittest.TestCase):
    """测试点操作"""
    
    def test_chain_operations(self):
        """测试链式操作"""
        p1 = Point(1.0, 1.0)
        p2 = Point(2.0, 3.0)
        
        result = (p1 + p2) * 2
        self.assertEqual(result.x, 6.0)
        self.assertEqual(result.y, 8.0)
    
    def test_distance_chain(self):
        """测试距离计算链"""
        p1 = Point(0.0, 0.0)
        p2 = Point(1.0, 0.0)
        p3 = Point(1.0, 1.0)
        
        d1 = p1.distance_to(p2)
        d2 = p2.distance_to(p3)
        d3 = p1.distance_to(p3)
        
        self.assertEqual(d1, 1.0)
        self.assertEqual(d2, 1.0)
        self.assertEqual(d3, sqrt(2))


if __name__ == "__main__":
    # 需要导入 sqrt
    import math
    sqrt = math.sqrt
    unittest.main()