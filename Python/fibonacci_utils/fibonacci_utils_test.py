"""
Fibonacci Utils 测试套件

测试所有斐波那契工具函数
"""

import unittest
from mod import FibonacciUtils, generate, nth, is_fibonacci, zeckendorf, golden_ratio


class TestFibonacciGenerate(unittest.TestCase):
    """测试斐波那契数列生成"""
    
    def test_generate_zero(self):
        """测试生成0个"""
        self.assertEqual(FibonacciUtils.generate(0), [])
    
    def test_generate_one(self):
        """测试生成1个"""
        self.assertEqual(FibonacciUtils.generate(1), [0])
    
    def test_generate_ten(self):
        """测试生成10个"""
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        self.assertEqual(FibonacciUtils.generate(10), expected)
    
    def test_generate_negative(self):
        """测试负数输入"""
        self.assertEqual(FibonacciUtils.generate(-5), [])


class TestFibonacciNth(unittest.TestCase):
    """测试第N个斐波那契数计算"""
    
    def test_nth_iterative_basic(self):
        """测试迭代法基本用例"""
        self.assertEqual(FibonacciUtils.nth_iterative(0), 0)
        self.assertEqual(FibonacciUtils.nth_iterative(1), 1)
        self.assertEqual(FibonacciUtils.nth_iterative(10), 55)
        self.assertEqual(FibonacciUtils.nth_iterative(20), 6765)
    
    def test_nth_recursive_basic(self):
        """测试递归法基本用例"""
        self.assertEqual(FibonacciUtils.nth_recursive(0), 0)
        self.assertEqual(FibonacciUtils.nth_recursive(1), 1)
        self.assertEqual(FibonacciUtils.nth_recursive(10), 55)
    
    def test_nth_matrix_basic(self):
        """测试矩阵法基本用例"""
        self.assertEqual(FibonacciUtils.nth_matrix(0), 0)
        self.assertEqual(FibonacciUtils.nth_matrix(1), 1)
        self.assertEqual(FibonacciUtils.nth_matrix(10), 55)
        self.assertEqual(FibonacciUtils.nth_matrix(20), 6765)
    
    def test_nth_binet_basic(self):
        """测试比内公式基本用例"""
        self.assertEqual(FibonacciUtils.nth_binet(0), 0)
        self.assertEqual(FibonacciUtils.nth_binet(1), 1)
        self.assertEqual(FibonacciUtils.nth_binet(10), 55)
    
    def test_all_methods_consistent(self):
        """测试所有方法结果一致"""
        for n in range(30):
            iterative = FibonacciUtils.nth_iterative(n)
            recursive = FibonacciUtils.nth_recursive(n)
            matrix = FibonacciUtils.nth_matrix(n)
            binet = FibonacciUtils.nth_binet(n)
            self.assertEqual(iterative, recursive)
            self.assertEqual(iterative, matrix)
            self.assertEqual(iterative, binet)
    
    def test_nth_negative(self):
        """测试负数输入"""
        with self.assertRaises(ValueError):
            FibonacciUtils.nth_iterative(-1)
        with self.assertRaises(ValueError):
            FibonacciUtils.nth_recursive(-1)
        with self.assertRaises(ValueError):
            FibonacciUtils.nth_matrix(-1)
        with self.assertRaises(ValueError):
            FibonacciUtils.nth_binet(-1)
    
    def test_large_n(self):
        """测试大数计算"""
        # F(50) = 12586269025
        self.assertEqual(FibonacciUtils.nth_iterative(50), 12586269025)
        self.assertEqual(FibonacciUtils.nth_matrix(50), 12586269025)


class TestIsFibonacci(unittest.TestCase):
    """测试斐波那契数判断"""
    
    def test_is_fibonacci_true(self):
        """测试是斐波那契数"""
        fibs = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
        for fib in fibs:
            with self.subTest(fib=fib):
                self.assertTrue(FibonacciUtils.is_fibonacci(fib))
    
    def test_is_fibonacci_false(self):
        """测试不是斐波那契数"""
        non_fibs = [4, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 22]
        for num in non_fibs:
            with self.subTest(num=num):
                self.assertFalse(FibonacciUtils.is_fibonacci(num))
    
    def test_is_fibonacci_negative(self):
        """测试负数"""
        self.assertFalse(FibonacciUtils.is_fibonacci(-1))
        self.assertFalse(FibonacciUtils.is_fibonacci(-100))


class TestNearestFibonacci(unittest.TestCase):
    """测试最近斐波那契数查找"""
    
    def test_nearest_exact(self):
        """测试精确匹配"""
        self.assertEqual(FibonacciUtils.nearest_fibonacci(55), (55, 10))
        self.assertEqual(FibonacciUtils.nearest_fibonacci(89), (89, 11))
    
    def test_nearest_between(self):
        """测试在两个斐波那契数之间"""
        # 50 在 34 和 55 之间，更接近 55
        self.assertEqual(FibonacciUtils.nearest_fibonacci(50), (55, 10))
        # 60 在 55 和 89 之间，更接近 55
        self.assertEqual(FibonacciUtils.nearest_fibonacci(60), (55, 10))
        # 72 在 55 和 89 之间，更接近 55 (72-55=17, 89-72=17，相等时返回较小的)
        self.assertEqual(FibonacciUtils.nearest_fibonacci(72), (55, 10))
    
    def test_nearest_zero(self):
        """测试零"""
        self.assertEqual(FibonacciUtils.nearest_fibonacci(0), (0, 0))


class TestFindIndex(unittest.TestCase):
    """测试斐波那契数索引查找"""
    
    def test_find_index_valid(self):
        """测试有效斐波那契数"""
        self.assertEqual(FibonacciUtils.find_index(0), 0)
        self.assertEqual(FibonacciUtils.find_index(1), 1)
        self.assertEqual(FibonacciUtils.find_index(55), 10)
        self.assertEqual(FibonacciUtils.find_index(6765), 20)
    
    def test_find_index_invalid(self):
        """测试无效斐波那契数"""
        self.assertEqual(FibonacciUtils.find_index(4), -1)
        self.assertEqual(FibonacciUtils.find_index(56), -1)
    
    def test_find_index_negative(self):
        """测试负数"""
        self.assertEqual(FibonacciUtils.find_index(-1), -1)


class TestRange(unittest.TestCase):
    """测试范围生成"""
    
    def test_range_basic(self):
        """测试基本范围"""
        result = FibonacciUtils.range(10, 100)
        self.assertEqual(result, [13, 21, 34, 55, 89])
    
    def test_range_empty(self):
        """测试空范围"""
        self.assertEqual(FibonacciUtils.range(100, 10), [])
        self.assertEqual(FibonacciUtils.range(10, 10), [])
    
    def test_range_small(self):
        """测试小范围"""
        self.assertEqual(FibonacciUtils.range(0, 10), [0, 1, 1, 2, 3, 5, 8])
        self.assertEqual(FibonacciUtils.range(5, 20), [5, 8, 13])


class TestSumFirstN(unittest.TestCase):
    """测试前N个斐波那契数求和"""
    
    def test_sum_basic(self):
        """测试基本求和"""
        # F(0..9) = 0+1+1+2+3+5+8+13+21+34 = 88
        self.assertEqual(FibonacciUtils.sum_first_n(10), 88)
    
    def test_sum_zero(self):
        """测试零项求和"""
        self.assertEqual(FibonacciUtils.sum_first_n(0), 0)
    
    def test_sum_one(self):
        """测试一项求和"""
        self.assertEqual(FibonacciUtils.sum_first_n(1), 0)
    
    def test_sum_verification(self):
        """手动验证求和"""
        fibs = FibonacciUtils.generate(15)
        manual_sum = sum(fibs)
        self.assertEqual(FibonacciUtils.sum_first_n(15), manual_sum)


class TestZeckendorf(unittest.TestCase):
    """测试Zeckendorf表示"""
    
    def test_zeckendorf_basic(self):
        """测试基本Zeckendorf表示"""
        self.assertEqual(FibonacciUtils.zeckendorf(100), [89, 8, 3])
        self.assertEqual(FibonacciUtils.zeckendorf(50), [34, 13, 3])
    
    def test_zeckendorf_fibonacci_number(self):
        """测试本身就是斐波那契数"""
        self.assertEqual(FibonacciUtils.zeckendorf(55), [55])
        self.assertEqual(FibonacciUtils.zeckendorf(89), [89])
    
    def test_zeckendorf_small(self):
        """测试小数字"""
        self.assertEqual(FibonacciUtils.zeckendorf(1), [1])
        self.assertEqual(FibonacciUtils.zeckendorf(2), [2])
        self.assertEqual(FibonacciUtils.zeckendorf(3), [3])
    
    def test_zeckendorf_zero(self):
        """测试零"""
        self.assertEqual(FibonacciUtils.zeckendorf(0), [])
    
    def test_zeckendorf_negative(self):
        """测试负数"""
        self.assertEqual(FibonacciUtils.zeckendorf(-1), [])
    
    def test_zeckendorf_no_adjacent(self):
        """验证不使用相邻的斐波那契数"""
        fibs = FibonacciUtils.generate(30)[2:]  # 跳过前两个0,1，从1开始
        for n in range(1, 100):
            z = FibonacciUtils.zeckendorf(n)
            # 检查和正确
            self.assertEqual(sum(z), n)
            # 检查没有相邻的斐波那契数
            for i in range(len(z) - 1):
                idx1 = FibonacciUtils.find_index(z[i])
                idx2 = FibonacciUtils.find_index(z[i + 1])
                self.assertGreater(abs(idx1 - idx2), 1, 
                    f"Found adjacent Fibonacci numbers in Zeckendorf of {n}: {z}")


class TestGoldenRatio(unittest.TestCase):
    """测试黄金比例计算"""
    
    def test_golden_ratio_approximation(self):
        """测试黄金比例近似值"""
        phi = FibonacciUtils.golden_ratio(50)
        expected = (1 + 5 ** 0.5) / 2
        self.assertAlmostEqual(phi, expected, places=6)
    
    def test_golden_ratio_precision(self):
        """测试精度随迭代增加"""
        low_precision = FibonacciUtils.golden_ratio(5)
        high_precision = FibonacciUtils.golden_ratio(50)
        expected = (1 + 5 ** 0.5) / 2
        self.assertLess(abs(high_precision - expected), abs(low_precision - expected))


class TestIterator(unittest.TestCase):
    """测试斐波那契迭代器"""
    
    def test_iterator_basic(self):
        """测试迭代器基本功能"""
        it = FibonacciUtils.fibonacci_iterator()
        result = [next(it) for _ in range(10)]
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        self.assertEqual(result, expected)
    
    def test_iterator_consistency(self):
        """测试迭代器与generate一致"""
        it = FibonacciUtils.fibonacci_iterator()
        from_iterator = [next(it) for _ in range(20)]
        from_generate = FibonacciUtils.generate(20)
        self.assertEqual(from_iterator, from_generate)


class TestLucasNumber(unittest.TestCase):
    """测试卢卡斯数"""
    
    def test_lucas_basic(self):
        """测试卢卡斯数基本用例"""
        # L(0)=2, L(1)=1, L(2)=3, L(3)=4, L(4)=7, L(5)=11, L(6)=18...
        expected = [2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123]
        for i, exp in enumerate(expected):
            with self.subTest(i=i):
                self.assertEqual(FibonacciUtils.lucas_number(i), exp)
    
    def test_lucas_negative(self):
        """测试负数输入"""
        with self.assertRaises(ValueError):
            FibonacciUtils.lucas_number(-1)


class TestPisanoPeriod(unittest.TestCase):
    """测试皮萨诺周期"""
    
    def test_pisano_small_moduli(self):
        """测试小模数的皮萨诺周期"""
        # 已知的皮萨诺周期
        test_cases = [
            (2, 3),   # 0,1,1 重复
            (3, 8),   # 已知周期为8
            (5, 20),  # 已知周期为20
            (10, 60), # 已知周期为60
        ]
        for m, expected_period in test_cases:
            with self.subTest(m=m):
                self.assertEqual(FibonacciUtils.pisano_period(m), expected_period)
    
    def test_pisano_negative(self):
        """测试负数输入"""
        with self.assertRaises(ValueError):
            FibonacciUtils.pisano_period(-1)
        with self.assertRaises(ValueError):
            FibonacciUtils.pisano_period(0)


class TestNthMod(unittest.TestCase):
    """测试模运算斐波那契"""
    
    def test_nth_mod_basic(self):
        """测试基本模运算"""
        # F(10) = 55, 55 mod 7 = 6
        self.assertEqual(FibonacciUtils.nth_mod(10, 7), 55 % 7)
        # F(20) = 6765, 6765 mod 100 = 65
        self.assertEqual(FibonacciUtils.nth_mod(20, 100), 65)
    
    def test_nth_mod_large(self):
        """测试大数模运算"""
        # 使用周期优化，F(100) mod 7
        # F(100) = 354224848179261915075
        result = FibonacciUtils.nth_mod(100, 7)
        # 手动计算验证
        self.assertEqual(result, 3)  # 354224848179261915075 % 7 = 3
    
    def test_nth_mod_negative(self):
        """测试负数输入"""
        with self.assertRaises(ValueError):
            FibonacciUtils.nth_mod(-1, 10)
        with self.assertRaises(ValueError):
            FibonacciUtils.nth_mod(10, 0)


class TestCountDigits(unittest.TestCase):
    """测试位数计算"""
    
    def test_count_digits_basic(self):
        """测试基本位数计算"""
        self.assertEqual(FibonacciUtils.count_digits(0), 1)   # F(0)=0
        self.assertEqual(FibonacciUtils.count_digits(1), 1)   # F(1)=1
        self.assertEqual(FibonacciUtils.count_digits(10), 2)  # F(10)=55
        self.assertEqual(FibonacciUtils.count_digits(20), 4)  # F(20)=6765
    
    def test_count_digits_large(self):
        """测试大数位数"""
        # F(100) = 354224848179261915075 (21位)
        self.assertEqual(FibonacciUtils.count_digits(100), 21)
        # F(1000) 有209位
        self.assertEqual(FibonacciUtils.count_digits(1000), 209)


class TestGcdFibonacci(unittest.TestCase):
    """测试斐波那契数的最大公约数"""
    
    def test_gcd_fibonacci_basic(self):
        """测试基本GCD"""
        # gcd(F(6), F(9)) = F(gcd(6,9)) = F(3) = 2
        self.assertEqual(FibonacciUtils.gcd_fibonacci(6, 9), 2)
        # gcd(F(12), F(18)) = F(gcd(12,18)) = F(6) = 8
        self.assertEqual(FibonacciUtils.gcd_fibonacci(12, 18), 8)
    
    def test_gcd_fibonacci_one(self):
        """测试一个数是另一个的倍数"""
        # gcd(F(4), F(8)) = F(gcd(4,8)) = F(4) = 3
        self.assertEqual(FibonacciUtils.gcd_fibonacci(4, 8), 3)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_generate_function(self):
        """测试generate便捷函数"""
        self.assertEqual(generate(10), FibonacciUtils.generate(10))
    
    def test_nth_function(self):
        """测试nth便捷函数"""
        self.assertEqual(nth(10), 55)
        self.assertEqual(nth(20), 6765)
    
    def test_is_fibonacci_function(self):
        """测试is_fibonacci便捷函数"""
        self.assertTrue(is_fibonacci(55))
        self.assertFalse(is_fibonacci(56))
    
    def test_zeckendorf_function(self):
        """测试zeckendorf便捷函数"""
        self.assertEqual(zeckendorf(100), [89, 8, 3])
    
    def test_golden_ratio_function(self):
        """测试golden_ratio便捷函数"""
        phi = golden_ratio(50)
        expected = (1 + 5 ** 0.5) / 2
        self.assertAlmostEqual(phi, expected, places=6)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_large_fibonacci(self):
        """测试大数斐波那契"""
        # F(100) = 354224848179261915075
        self.assertEqual(FibonacciUtils.nth_iterative(100), 354224848179261915075)
    
    def test_consistency_large_n(self):
        """测试大数时各方法一致性"""
        n = 50
        iterative = FibonacciUtils.nth_iterative(n)
        matrix = FibonacciUtils.nth_matrix(n)
        self.assertEqual(iterative, matrix)


if __name__ == "__main__":
    unittest.main(verbosity=2)