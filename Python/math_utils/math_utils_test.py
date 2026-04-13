"""
数学工具模块测试
"""

import unittest
import math
from math_utils import MathUtils


class TestBasicOperations(unittest.TestCase):
    """基础运算测试"""
    
    def test_factorial(self):
        self.assertEqual(MathUtils.factorial(0), 1)
        self.assertEqual(MathUtils.factorial(1), 1)
        self.assertEqual(MathUtils.factorial(5), 120)
        self.assertEqual(MathUtils.factorial(10), 3628800)
        with self.assertRaises(ValueError):
            MathUtils.factorial(-1)
    
    def test_fibonacci(self):
        self.assertEqual(MathUtils.fibonacci(0), 0)
        self.assertEqual(MathUtils.fibonacci(1), 1)
        self.assertEqual(MathUtils.fibonacci(10), 55)
        self.assertEqual(MathUtils.fibonacci(20), 6765)
        with self.assertRaises(ValueError):
            MathUtils.fibonacci(-1)
    
    def test_fibonacci_sequence(self):
        self.assertEqual(MathUtils.fibonacci_sequence(0), [])
        self.assertEqual(MathUtils.fibonacci_sequence(1), [0])
        self.assertEqual(MathUtils.fibonacci_sequence(10), 
                         [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])
    
    def test_gcd(self):
        self.assertEqual(MathUtils.gcd(48, 18), 6)
        self.assertEqual(MathUtils.gcd(48, 18, 12), 6)
        self.assertEqual(MathUtils.gcd(17, 23), 1)
        with self.assertRaises(ValueError):
            MathUtils.gcd()
    
    def test_lcm(self):
        self.assertEqual(MathUtils.lcm(4, 6), 12)
        self.assertEqual(MathUtils.lcm(4, 6, 8), 24)
        self.assertEqual(MathUtils.lcm(3, 5), 15)
        with self.assertRaises(ValueError):
            MathUtils.lcm()
    
    def test_power(self):
        self.assertEqual(MathUtils.power(2, 10), 1024)
        self.assertEqual(MathUtils.power(3, 4), 81)
        self.assertAlmostEqual(MathUtils.power(4, 0.5), 2.0)
    
    def test_sqrt(self):
        self.assertEqual(MathUtils.sqrt(16), 4.0)
        self.assertEqual(MathUtils.sqrt(0), 0.0)
        self.assertAlmostEqual(MathUtils.sqrt(2), 1.4142135623730951)
        with self.assertRaises(ValueError):
            MathUtils.sqrt(-1)
    
    def test_cbrt(self):
        self.assertEqual(MathUtils.cbrt(27), 3.0)
        self.assertEqual(MathUtils.cbrt(-27), -3.0)
        self.assertAlmostEqual(MathUtils.cbrt(2), 1.2599210498948732)
    
    def test_root(self):
        self.assertEqual(MathUtils.root(16, 4), 2.0)
        self.assertEqual(MathUtils.root(8, 3), 2.0)
        with self.assertRaises(ValueError):
            MathUtils.root(4, 0)
        with self.assertRaises(ValueError):
            MathUtils.root(-4, 2)
    
    def test_abs(self):
        self.assertEqual(MathUtils.abs(-5), 5)
        self.assertEqual(MathUtils.abs(5), 5)
        self.assertEqual(MathUtils.abs(0), 0)
    
    def test_sign(self):
        self.assertEqual(MathUtils.sign(-5), -1)
        self.assertEqual(MathUtils.sign(0), 0)
        self.assertEqual(MathUtils.sign(5), 1)


class TestNumberTheory(unittest.TestCase):
    """数论测试"""
    
    def test_is_prime(self):
        self.assertFalse(MathUtils.is_prime(0))
        self.assertFalse(MathUtils.is_prime(1))
        self.assertTrue(MathUtils.is_prime(2))
        self.assertTrue(MathUtils.is_prime(17))
        self.assertTrue(MathUtils.is_prime(97))
        self.assertFalse(MathUtils.is_prime(18))
        self.assertFalse(MathUtils.is_prime(100))
    
    def test_primes_up_to(self):
        self.assertEqual(MathUtils.primes_up_to(0), [])
        self.assertEqual(MathUtils.primes_up_to(1), [])
        self.assertEqual(MathUtils.primes_up_to(10), [2, 3, 5, 7])
        self.assertEqual(MathUtils.primes_up_to(20), 
                         [2, 3, 5, 7, 11, 13, 17, 19])
    
    def test_prime_factors(self):
        self.assertEqual(MathUtils.prime_factors(2), [2])
        self.assertEqual(MathUtils.prime_factors(12), [2, 2, 3])
        self.assertEqual(MathUtils.prime_factors(60), [2, 2, 3, 5])
        self.assertEqual(MathUtils.prime_factors(97), [97])
        with self.assertRaises(ValueError):
            MathUtils.prime_factors(1)
    
    def test_divisors(self):
        self.assertEqual(MathUtils.divisors(1), [1])
        self.assertEqual(MathUtils.divisors(12), [1, 2, 3, 4, 6, 12])
        self.assertEqual(MathUtils.divisors(17), [1, 17])
        with self.assertRaises(ValueError):
            MathUtils.divisors(0)
    
    def test_count_divisors(self):
        self.assertEqual(MathUtils.count_divisors(12), 6)
        self.assertEqual(MathUtils.count_divisors(17), 2)
    
    def test_euler_totient(self):
        self.assertEqual(MathUtils.euler_totient(1), 1)
        self.assertEqual(MathUtils.euler_totient(9), 6)
        self.assertEqual(MathUtils.euler_totient(10), 4)
        with self.assertRaises(ValueError):
            MathUtils.euler_totient(0)
    
    def test_is_perfect_number(self):
        self.assertFalse(MathUtils.is_perfect_number(1))
        self.assertTrue(MathUtils.is_perfect_number(6))
        self.assertTrue(MathUtils.is_perfect_number(28))
        self.assertTrue(MathUtils.is_perfect_number(496))
        self.assertFalse(MathUtils.is_perfect_number(12))


class TestGeometry(unittest.TestCase):
    """几何计算测试"""
    
    def test_distance_2d(self):
        self.assertEqual(MathUtils.distance_2d((0, 0), (3, 4)), 5.0)
        self.assertEqual(MathUtils.distance_2d((1, 1), (4, 5)), 5.0)
        self.assertAlmostEqual(MathUtils.distance_2d((0, 0), (1, 1)), 1.4142135623730951)
    
    def test_distance_3d(self):
        self.assertEqual(MathUtils.distance_3d((0, 0, 0), (1, 2, 2)), 3.0)
        self.assertEqual(MathUtils.distance_3d((0, 0, 0), (0, 3, 4)), 5.0)
    
    def test_circle_area(self):
        self.assertAlmostEqual(MathUtils.circle_area(1), math.pi)
        self.assertEqual(MathUtils.circle_area(0), 0)
        with self.assertRaises(ValueError):
            MathUtils.circle_area(-1)
    
    def test_circle_circumference(self):
        self.assertAlmostEqual(MathUtils.circle_circumference(1), 2 * math.pi)
        self.assertEqual(MathUtils.circle_circumference(0), 0)
    
    def test_sphere_volume(self):
        self.assertAlmostEqual(MathUtils.sphere_volume(1), 4/3 * math.pi)
        self.assertEqual(MathUtils.sphere_volume(2), 32/3 * math.pi)
    
    def test_sphere_surface_area(self):
        self.assertAlmostEqual(MathUtils.sphere_surface_area(1), 4 * math.pi)
        self.assertEqual(MathUtils.sphere_surface_area(2), 16 * math.pi)
    
    def test_rectangle_area(self):
        self.assertEqual(MathUtils.rectangle_area(5, 3), 15)
        self.assertEqual(MathUtils.rectangle_area(2.5, 4), 10)
        with self.assertRaises(ValueError):
            MathUtils.rectangle_area(-1, 5)
    
    def test_triangle_area(self):
        self.assertEqual(MathUtils.triangle_area(6, 4), 12.0)
        self.assertEqual(MathUtils.triangle_area(10, 5), 25.0)
    
    def test_triangle_area_heron(self):
        self.assertEqual(MathUtils.triangle_area_heron(3, 4, 5), 6.0)
        self.assertAlmostEqual(MathUtils.triangle_area_heron(5, 5, 5), 10.825317547305483)
        with self.assertRaises(ValueError):
            MathUtils.triangle_area_heron(1, 1, 10)  # 无法构成三角形
    
    def test_cylinder_volume(self):
        self.assertAlmostEqual(MathUtils.cylinder_volume(3, 5), 
                              math.pi * 9 * 5)
    
    def test_cone_volume(self):
        self.assertAlmostEqual(MathUtils.cone_volume(3, 5), 
                              math.pi * 9 * 5 / 3)
    
    def test_angle_between_vectors(self):
        angle = MathUtils.angle_between_vectors((1, 0), (0, 1))
        self.assertAlmostEqual(angle, math.pi / 2)
        
        angle = MathUtils.angle_between_vectors((1, 0), (1, 0))
        self.assertAlmostEqual(angle, 0)
        
        angle = MathUtils.angle_between_vectors((1, 0), (-1, 0))
        self.assertAlmostEqual(angle, math.pi)
        
        with self.assertRaises(ValueError):
            MathUtils.angle_between_vectors((0, 0), (1, 1))


class TestStatistics(unittest.TestCase):
    """统计测试"""
    
    def test_mean(self):
        self.assertEqual(MathUtils.mean([1, 2, 3, 4, 5]), 3.0)
        self.assertEqual(MathUtils.mean([1, 2, 3, 4]), 2.5)
        with self.assertRaises(ValueError):
            MathUtils.mean([])
    
    def test_median(self):
        self.assertEqual(MathUtils.median([1, 2, 3, 4, 5]), 3)
        self.assertEqual(MathUtils.median([1, 2, 3, 4]), 2.5)
        self.assertEqual(MathUtils.median([5, 1, 3, 2, 4]), 3)
        with self.assertRaises(ValueError):
            MathUtils.median([])
    
    def test_mode(self):
        self.assertEqual(MathUtils.mode([1, 2, 2, 3, 3, 3]), [3])
        self.assertEqual(MathUtils.mode([1, 1, 2, 2]), [1, 2])
        self.assertEqual(MathUtils.mode([1]), [1])
        with self.assertRaises(ValueError):
            MathUtils.mode([])
    
    def test_variance(self):
        self.assertEqual(MathUtils.variance([1, 2, 3, 4, 5]), 2.0)
        self.assertAlmostEqual(MathUtils.variance([1, 2, 3], population=False), 
                              1.0)
    
    def test_standard_deviation(self):
        result = MathUtils.standard_deviation([1, 2, 3, 4, 5])
        self.assertAlmostEqual(result, 1.4142135623730951)
    
    def test_range_value(self):
        self.assertEqual(MathUtils.range_value([1, 2, 3, 4, 5]), 4)
        self.assertEqual(MathUtils.range_value([10, 5, 20, 15]), 15)
        with self.assertRaises(ValueError):
            MathUtils.range_value([])
    
    def test_percentile(self):
        self.assertEqual(MathUtils.percentile([1, 2, 3, 4, 5], 50), 3.0)
        self.assertEqual(MathUtils.percentile([1, 2, 3, 4, 5], 0), 1.0)
        self.assertEqual(MathUtils.percentile([1, 2, 3, 4, 5], 100), 5.0)
        with self.assertRaises(ValueError):
            MathUtils.percentile([], 50)
        with self.assertRaises(ValueError):
            MathUtils.percentile([1, 2, 3], 150)
    
    def test_quartiles(self):
        q1, q2, q3 = MathUtils.quartiles([1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(q2, 4.0)  # 中位数
        # Q1 和 Q3 使用百分位数方法计算
        self.assertTrue(q1 < q2 and q3 > q2)
    
    def test_iqr(self):
        iqr = MathUtils.iqr([1, 2, 3, 4, 5, 6, 7])
        self.assertGreater(iqr, 0)  # IQR 应为正值
    
    def test_covariance(self):
        cov = MathUtils.covariance([1, 2, 3], [4, 5, 6])
        self.assertAlmostEqual(cov, 2/3)
        
        cov = MathUtils.covariance([1, 2, 3], [4, 5, 6], population=False)
        self.assertEqual(cov, 1.0)
        
        with self.assertRaises(ValueError):
            MathUtils.covariance([1, 2], [1, 2, 3])
    
    def test_correlation(self):
        corr = MathUtils.correlation([1, 2, 3], [2, 4, 6])
        self.assertEqual(corr, 1.0)
        
        corr = MathUtils.correlation([1, 2, 3], [6, 4, 2])
        self.assertEqual(corr, -1.0)
        
        with self.assertRaises(ValueError):
            MathUtils.correlation([1, 2], [1, 2, 3])


class TestNumericOperations(unittest.TestCase):
    """数值处理测试"""
    
    def test_round_to(self):
        self.assertEqual(MathUtils.round_to(3.14159, 2), 3.14)
        self.assertEqual(MathUtils.round_to(3.14159, 4), 3.1416)
        self.assertEqual(MathUtils.round_to(3.5), 4)
    
    def test_round_up(self):
        self.assertEqual(MathUtils.round_up(3.14, 1), 3.2)
        self.assertEqual(MathUtils.round_up(3.1), 4)
    
    def test_round_down(self):
        self.assertEqual(MathUtils.round_down(3.19, 1), 3.1)
        self.assertEqual(MathUtils.round_down(3.9), 3)
    
    def test_truncate(self):
        self.assertEqual(MathUtils.truncate(3.14159, 2), 3.14)
        self.assertEqual(MathUtils.truncate(3.999, 2), 3.99)
    
    def test_clamp(self):
        self.assertEqual(MathUtils.clamp(10, 0, 5), 5)
        self.assertEqual(MathUtils.clamp(-1, 0, 5), 0)
        self.assertEqual(MathUtils.clamp(3, 0, 5), 3)
    
    def test_percentage(self):
        self.assertEqual(MathUtils.percentage(25, 200), 12.5)
        self.assertEqual(MathUtils.percentage(1, 3, 4), 33.3333)
        with self.assertRaises(ValueError):
            MathUtils.percentage(50, 0)
    
    def test_percentage_change(self):
        self.assertEqual(MathUtils.percentage_change(100, 150), 50.0)
        self.assertEqual(MathUtils.percentage_change(100, 80), -20.0)
        with self.assertRaises(ValueError):
            MathUtils.percentage_change(0, 100)
    
    def test_ratio_to_percentage(self):
        self.assertEqual(MathUtils.ratio_to_percentage(0.75), 75.0)
        self.assertEqual(MathUtils.ratio_to_percentage(0.5, 1), 50.0)


class TestVectorOperations(unittest.TestCase):
    """向量运算测试"""
    
    def test_vector_add(self):
        self.assertEqual(MathUtils.vector_add((1, 2, 3), (4, 5, 6)), (5, 7, 9))
        self.assertEqual(MathUtils.vector_add((1, 2), (3, 4)), (4, 6))
        with self.assertRaises(ValueError):
            MathUtils.vector_add((1, 2), (1, 2, 3))
    
    def test_vector_subtract(self):
        self.assertEqual(MathUtils.vector_subtract((4, 5, 6), (1, 2, 3)), (3, 3, 3))
        self.assertEqual(MathUtils.vector_subtract((3, 4), (1, 2)), (2, 2))
    
    def test_vector_scale(self):
        self.assertEqual(MathUtils.vector_scale((1, 2, 3), 2), (2, 4, 6))
        self.assertEqual(MathUtils.vector_scale((1, 2, 3), 0), (0, 0, 0))
    
    def test_vector_dot(self):
        self.assertEqual(MathUtils.vector_dot((1, 2, 3), (4, 5, 6)), 32)
        self.assertEqual(MathUtils.vector_dot((1, 0), (0, 1)), 0)
    
    def test_vector_cross_3d(self):
        result = MathUtils.vector_cross_3d((1, 0, 0), (0, 1, 0))
        self.assertEqual(result, (0, 0, 1))
        
        result = MathUtils.vector_cross_3d((1, 2, 3), (4, 5, 6))
        self.assertEqual(result, (-3, 6, -3))
    
    def test_vector_magnitude(self):
        self.assertEqual(MathUtils.vector_magnitude((3, 4)), 5.0)
        self.assertEqual(MathUtils.vector_magnitude((1, 0, 0)), 1.0)
        self.assertEqual(MathUtils.vector_magnitude((0, 0, 0)), 0.0)
    
    def test_vector_normalize(self):
        result = MathUtils.vector_normalize((3, 4))
        self.assertAlmostEqual(result[0], 0.6)
        self.assertAlmostEqual(result[1], 0.8)
        
        with self.assertRaises(ValueError):
            MathUtils.vector_normalize((0, 0, 0))


class TestSequenceGeneration(unittest.TestCase):
    """序列生成测试"""
    
    def test_arithmetic_sequence(self):
        self.assertEqual(MathUtils.arithmetic_sequence(1, 2, 5), [1, 3, 5, 7, 9])
        self.assertEqual(MathUtils.arithmetic_sequence(10, -2, 5), [10, 8, 6, 4, 2])
        self.assertEqual(MathUtils.arithmetic_sequence(1, 1, 3), [1, 2, 3])
        self.assertEqual(MathUtils.arithmetic_sequence(1, 2, 0), [])
    
    def test_arithmetic_sum(self):
        self.assertEqual(MathUtils.arithmetic_sum(1, 2, 5), 25)
        self.assertEqual(MathUtils.arithmetic_sum(1, 1, 100), 5050)
        self.assertEqual(MathUtils.arithmetic_sum(1, 2, 0), 0)
    
    def test_geometric_sequence(self):
        self.assertEqual(MathUtils.geometric_sequence(1, 2, 5), [1, 2, 4, 8, 16])
        self.assertEqual(MathUtils.geometric_sequence(1, 0.5, 4), [1, 0.5, 0.25, 0.125])
        self.assertEqual(MathUtils.geometric_sequence(2, 1, 3), [2, 2, 2])
    
    def test_geometric_sum(self):
        self.assertEqual(MathUtils.geometric_sum(1, 2, 5), 31)
        self.assertEqual(MathUtils.geometric_sum(1, 0.5, 4), 1.875)
        self.assertEqual(MathUtils.geometric_sum(2, 1, 3), 6)
    
    def test_range_float(self):
        result = MathUtils.range_float(0, 1, 0.2)
        self.assertEqual(len(result), 5)
        self.assertAlmostEqual(result[0], 0.0)
        self.assertAlmostEqual(result[-1], 0.8)
        
        with self.assertRaises(ValueError):
            MathUtils.range_float(0, 1, 0)
    
    def test_linspace(self):
        result = MathUtils.linspace(0, 10, 5)
        self.assertEqual(result, [0.0, 2.5, 5.0, 7.5, 10.0])
        
        result = MathUtils.linspace(0, 1, 2)
        self.assertEqual(result, [0.0, 1.0])
        
        result = MathUtils.linspace(5, 5, 1)
        self.assertEqual(result, [5.0])


class TestNumericChecks(unittest.TestCase):
    """数值检查测试"""
    
    def test_is_even(self):
        self.assertTrue(MathUtils.is_even(0))
        self.assertTrue(MathUtils.is_even(2))
        self.assertTrue(MathUtils.is_even(-4))
        self.assertFalse(MathUtils.is_even(1))
        self.assertFalse(MathUtils.is_even(-3))
    
    def test_is_odd(self):
        self.assertTrue(MathUtils.is_odd(1))
        self.assertTrue(MathUtils.is_odd(-3))
        self.assertFalse(MathUtils.is_odd(0))
        self.assertFalse(MathUtils.is_odd(2))
    
    def test_is_integer(self):
        self.assertTrue(MathUtils.is_integer(5.0))
        self.assertTrue(MathUtils.is_integer(5))
        self.assertTrue(MathUtils.is_integer(5.0000000001, tolerance=1e-8))
        self.assertFalse(MathUtils.is_integer(5.1))
    
    def test_is_power_of(self):
        self.assertTrue(MathUtils.is_power_of(8, 2))
        self.assertTrue(MathUtils.is_power_of(27, 3))
        self.assertFalse(MathUtils.is_power_of(10, 2))
        self.assertFalse(MathUtils.is_power_of(0, 2))
    
    def test_is_perfect_square(self):
        self.assertTrue(MathUtils.is_perfect_square(4))
        self.assertTrue(MathUtils.is_perfect_square(100))
        self.assertFalse(MathUtils.is_perfect_square(5))
        self.assertFalse(MathUtils.is_perfect_square(-4))
    
    def test_is_perfect_cube(self):
        self.assertTrue(MathUtils.is_perfect_cube(27))
        self.assertTrue(MathUtils.is_perfect_cube(8))
        self.assertFalse(MathUtils.is_perfect_cube(9))
    
    def test_is_armstrong(self):
        self.assertTrue(MathUtils.is_armstrong(153))
        self.assertTrue(MathUtils.is_armstrong(370))
        self.assertTrue(MathUtils.is_armstrong(371))
        self.assertFalse(MathUtils.is_armstrong(123))
    
    def test_is_palindrome_number(self):
        self.assertTrue(MathUtils.is_palindrome_number(121))
        self.assertTrue(MathUtils.is_palindrome_number(12321))
        self.assertFalse(MathUtils.is_palindrome_number(123))
        self.assertFalse(MathUtils.is_palindrome_number(-121))


class TestRandomFunctions(unittest.TestCase):
    """随机函数测试"""
    
    def test_random_int(self):
        for _ in range(100):
            result = MathUtils.random_int(1, 10)
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 10)
    
    def test_random_float(self):
        for _ in range(100):
            result = MathUtils.random_float(0, 1)
            self.assertGreaterEqual(result, 0)
            self.assertLessEqual(result, 1)
    
    def test_random_choice(self):
        values = [1, 2, 3, 4, 5]
        for _ in range(100):
            result = MathUtils.random_choice(values)
            self.assertIn(result, values)
        
        with self.assertRaises(ValueError):
            MathUtils.random_choice([])
    
    def test_random_sample(self):
        values = [1, 2, 3, 4, 5]
        result = MathUtils.random_sample(values, 3)
        self.assertEqual(len(result), 3)
        for item in result:
            self.assertIn(item, values)
        
        with self.assertRaises(ValueError):
            MathUtils.random_sample(values, 10)
    
    def test_shuffle(self):
        values = [1, 2, 3, 4, 5]
        result = MathUtils.shuffle(values)
        self.assertEqual(len(result), 5)
        self.assertEqual(sorted(result), sorted(values))
        self.assertEqual(values, [1, 2, 3, 4, 5])  # 原列表不变


if __name__ == '__main__':
    unittest.main(verbosity=2)