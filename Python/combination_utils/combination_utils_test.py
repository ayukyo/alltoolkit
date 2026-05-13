"""
Combination Utilities 测试

测试所有组合数学功能：
- 组合数和排列数计算
- 排列和组合生成
- 幂集生成
- 康托编码
- 特殊数（卡特兰数、斯特林数、贝尔数）
"""

import unittest
from mod import (
    CombinationCalculator,
    PermutationGenerator,
    CantorEncoder,
    SpecialNumbers,
    CombinationUtils,
    C,
    P,
    factorial,
    catalan,
    generate_permutations,
    generate_combinations,
    generate_powerset,
)


class TestCombinationCalculator(unittest.TestCase):
    """组合数计算器测试"""
    
    def setUp(self):
        self.calc = CombinationCalculator()
    
    def test_factorial(self):
        """测试阶乘"""
        self.assertEqual(self.calc.factorial(0), 1)
        self.assertEqual(self.calc.factorial(1), 1)
        self.assertEqual(self.calc.factorial(5), 120)
        self.assertEqual(self.calc.factorial(10), 3628800)
    
    def test_factorial_negative(self):
        """测试负数阶乘"""
        with self.assertRaises(ValueError):
            self.calc.factorial(-1)
    
    def test_permutation(self):
        """测试排列数"""
        self.assertEqual(self.calc.permutation(5, 0), 1)
        self.assertEqual(self.calc.permutation(5, 1), 5)
        self.assertEqual(self.calc.permutation(5, 3), 60)
        self.assertEqual(self.calc.permutation(5, 5), 120)
        self.assertEqual(self.calc.permutation(10, 3), 720)
    
    def test_permutation_invalid(self):
        """测试无效排列数"""
        self.assertEqual(self.calc.permutation(5, 6), 0)  # k > n
        with self.assertRaises(ValueError):
            self.calc.permutation(-1, 3)
        with self.assertRaises(ValueError):
            self.calc.permutation(5, -1)
    
    def test_combination(self):
        """测试组合数"""
        self.assertEqual(self.calc.combination(5, 0), 1)
        self.assertEqual(self.calc.combination(5, 1), 5)
        self.assertEqual(self.calc.combination(5, 2), 10)
        self.assertEqual(self.calc.combination(5, 3), 10)
        self.assertEqual(self.calc.combination(5, 5), 1)
        self.assertEqual(self.calc.combination(10, 3), 120)
    
    def test_combination_symmetry(self):
        """测试组合数对称性 C(n, k) = C(n, n-k)"""
        self.assertEqual(self.calc.combination(10, 3), self.calc.combination(10, 7))
        self.assertEqual(self.calc.combination(20, 5), self.calc.combination(20, 15))
    
    def test_combination_invalid(self):
        """测试无效组合数"""
        self.assertEqual(self.calc.combination(5, 6), 0)  # k > n
        with self.assertRaises(ValueError):
            self.calc.combination(-1, 3)
        with self.assertRaises(ValueError):
            self.calc.combination(5, -1)
    
    def test_multinomial(self):
        """测试多重组合数"""
        self.assertEqual(self.calc.multinomial(2, 2), 6)  # 4! / (2! * 2!)
        self.assertEqual(self.calc.multinomial(3, 2, 1), 60)  # 6! / (3! * 2! * 1!)
        self.assertEqual(self.calc.multinomial(1, 1, 1, 1), 24)  # 4! / (1! * 1! * 1! * 1!)
    
    def test_cache(self):
        """测试缓存"""
        calc_with_cache = CombinationCalculator(use_cache=True)
        calc_no_cache = CombinationCalculator(use_cache=False)
        
        # 结果应该相同
        self.assertEqual(calc_with_cache.combination(20, 10), calc_no_cache.combination(20, 10))
        
        # 清空缓存
        calc_with_cache.clear_cache()
        self.assertEqual(calc_with_cache.combination(20, 10), calc_no_cache.combination(20, 10))


class TestPermutationGenerator(unittest.TestCase):
    """排列生成器测试"""
    
    def setUp(self):
        self.gen = PermutationGenerator()
    
    def test_generate_permutations(self):
        """测试全排列生成"""
        perms = self.gen.generate_permutations([1, 2, 3])
        self.assertEqual(len(perms), 6)  # 3! = 6
        
        # 检查所有排列存在
        expected = [
            [1, 2, 3], [1, 3, 2], [2, 1, 3],
            [2, 3, 1], [3, 1, 2], [3, 2, 1]
        ]
        for p in expected:
            self.assertIn(p, perms)
    
    def test_iter_permutations(self):
        """测试迭代排列"""
        count = 0
        for _ in self.gen.iter_permutations([1, 2, 3]):
            count += 1
        self.assertEqual(count, 6)
    
    def test_generate_k_permutations(self):
        """测试 k-排列生成"""
        perms = self.gen.generate_k_permutations([1, 2, 3, 4], 2)
        self.assertEqual(len(perms), 12)  # P(4, 2) = 12
    
    def test_generate_combinations(self):
        """测试组合生成"""
        combs = self.gen.generate_combinations([1, 2, 3, 4], 2)
        self.assertEqual(len(combs), 6)  # C(4, 2) = 6
        
        expected = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
        for c in expected:
            self.assertIn(c, combs)
    
    def test_iter_combinations(self):
        """测试迭代组合"""
        count = 0
        for _ in self.gen.iter_combinations([1, 2, 3, 4], 2):
            count += 1
        self.assertEqual(count, 6)
    
    def test_generate_all_combinations(self):
        """测试所有组合生成"""
        all_combs = self.gen.generate_all_combinations([1, 2, 3])
        self.assertEqual(len(all_combs), 8)  # 2^3 = 8
        
        # 检查包含空组合
        self.assertIn([], all_combs)
    
    def test_generate_powerset(self):
        """测试幂集生成"""
        power = self.gen.generate_powerset([1, 2])
        self.assertEqual(len(power), 4)  # 2^2 = 4
        
        # 检查所有子集存在
        self.assertIn([], power)
        self.assertIn([1], power)
        self.assertIn([2], power)
        self.assertIn([1, 2], power)
    
    def test_iter_powerset(self):
        """测试迭代幂集"""
        count = 0
        for _ in self.gen.iter_powerset([1, 2, 3]):
            count += 1
        self.assertEqual(count, 8)
    
    def test_count_powerset(self):
        """测试幂集计数"""
        self.assertEqual(self.gen.count_powerset(0), 1)
        self.assertEqual(self.gen.count_powerset(3), 8)
        self.assertEqual(self.gen.count_powerset(10), 1024)
    
    def test_permutations_with_repetition(self):
        """测试有重复的排列"""
        perms = self.gen.generate_permutations_with_repetition([1, 2], 2)
        self.assertEqual(len(perms), 4)  # 2^2 = 4
        
        expected = [[1, 1], [1, 2], [2, 1], [2, 2]]
        for p in expected:
            self.assertIn(p, perms)
    
    def test_combinations_with_repetition(self):
        """测试有重复的组合"""
        combs = self.gen.generate_combinations_with_repetition([1, 2], 2)
        self.assertEqual(len(combs), 3)  # C(2+2-1, 2) = C(3, 2) = 3
        
        expected = [[1, 1], [1, 2], [2, 2]]
        for c in expected:
            self.assertIn(c, combs)
    
    def test_empty_input(self):
        """测试空输入"""
        self.assertEqual(self.gen.generate_permutations([]), [[]])
        self.assertEqual(self.gen.generate_combinations([], 0), [[]])
        self.assertEqual(self.gen.generate_powerset([]), [[]])


class TestCantorEncoder(unittest.TestCase):
    """康托编码测试"""
    
    def setUp(self):
        self.encoder = CantorEncoder()
    
    def test_encode(self):
        """测试康托展开"""
        # 第一个排列索引为 0
        self.assertEqual(self.encoder.encode([0, 1, 2]), 0)
        self.assertEqual(self.encoder.encode([1, 2, 3]), 0)
        
        # 最后一个排列索引为 n! - 1
        self.assertEqual(self.encoder.encode([2, 1, 0]), 5)  # 3! - 1
        self.assertEqual(self.encoder.encode([3, 2, 1]), 5)
        
        # 中间排列
        self.assertEqual(self.encoder.encode([1, 0, 2]), 2)
    
    def test_decode(self):
        """测试康托逆展开"""
        elements = [0, 1, 2]
        
        self.assertEqual(self.encoder.decode(0, elements), [0, 1, 2])
        self.assertEqual(self.encoder.decode(5, elements), [2, 1, 0])
        self.assertEqual(self.encoder.decode(2, elements), [1, 0, 2])
    
    def test_encode_decode_roundtrip(self):
        """测试编码解码往返"""
        elements = [0, 1, 2, 3]
        
        for i in range(24):  # 4! = 24
            decoded = self.encoder.decode(i, elements)
            encoded = self.encoder.encode(decoded)
            self.assertEqual(encoded, i)
    
    def test_encode_with_elements(self):
        """测试任意元素编码"""
        elements = ['a', 'b', 'c']
        perm = ['b', 'a', 'c']
        
        idx = self.encoder.encode_with_elements(perm, elements)
        decoded = self.encoder.decode_with_elements(idx, elements)
        
        self.assertEqual(decoded, perm)
    
    def test_invalid_index(self):
        """测试无效索引"""
        with self.assertRaises(ValueError):
            self.encoder.decode(100, [0, 1, 2])  # 超出范围
    
    def test_empty_permutation(self):
        """测试空排列"""
        self.assertEqual(self.encoder.encode([]), 0)


class TestSpecialNumbers(unittest.TestCase):
    """特殊数测试"""
    
    def setUp(self):
        self.special = SpecialNumbers()
    
    def test_catalan(self):
        """测试卡特兰数"""
        expected = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862]
        
        for i, val in enumerate(expected):
            self.assertEqual(self.special.catalan(i), val)
    
    def test_catalan_formula(self):
        """测试卡特兰数公式"""
        # Catalan(n) = C(2n, n) / (n+1)
        calc = CombinationCalculator()
        
        for n in range(10):
            expected = calc.combination(2 * n, n) // (n + 1)
            self.assertEqual(self.special.catalan(n), expected)
    
    def test_catalan_invalid(self):
        """测试无效卡特兰数"""
        with self.assertRaises(ValueError):
            self.special.catalan(-1)
    
    def test_stirling_first(self):
        """测试第一类斯特林数"""
        # S(4, 2) = 11
        self.assertEqual(self.special.stirling_first(4, 2), 11)
        
        # S(n, n) = 1
        self.assertEqual(self.special.stirling_first(5, 5), 1)
        self.assertEqual(self.special.stirling_first(10, 10), 1)
        
        # S(n, 1) = (n-1)!
        self.assertEqual(self.special.stirling_first(5, 1), 24)  # 4!
    
    def test_stirling_second(self):
        """测试第二类斯特林数"""
        # S(4, 2) = 7
        self.assertEqual(self.special.stirling_second(4, 2), 7)
        
        # S(5, 3) = 25
        self.assertEqual(self.special.stirling_second(5, 3), 25)
        
        # S(n, n) = 1
        self.assertEqual(self.special.stirling_second(5, 5), 1)
        
        # S(n, 1) = 1
        self.assertEqual(self.special.stirling_second(5, 1), 1)
    
    def test_stirling_invalid(self):
        """测试无效斯特林数"""
        self.assertEqual(self.special.stirling_first(5, 6), 0)  # k > n
        self.assertEqual(self.special.stirling_second(5, 6), 0)
        
        with self.assertRaises(ValueError):
            self.special.stirling_first(-1, 3)
    
    def test_bell(self):
        """测试贝尔数"""
        expected = [1, 1, 2, 5, 15, 52, 203, 877, 4140]
        
        for i, val in enumerate(expected):
            self.assertEqual(self.special.bell(i), val)
    
    def test_bell_formula(self):
        """测试贝尔数公式"""
        # B(n) = sum(S(n, k) for k in 0..n)
        for n in range(10):
            expected = sum(self.special.stirling_second(n, k) for k in range(n + 1))
            self.assertEqual(self.special.bell(n), expected)
    
    def test_derangement(self):
        """测试错位排列数"""
        # D(0) = 1
        self.assertEqual(self.special.derangement(0), 1)
        
        # D(1) = 0
        self.assertEqual(self.special.derangement(1), 0)
        
        # D(4) = 9
        self.assertEqual(self.special.derangement(4), 9)
        
        # D(5) = 44
        self.assertEqual(self.special.derangement(5), 44)
    
    def test_derangement_invalid(self):
        """测试无效错位排列"""
        with self.assertRaises(ValueError):
            self.special.derangement(-1)


class TestCombinationUtils(unittest.TestCase):
    """高级接口测试"""
    
    def test_static_methods(self):
        """测试静态方法"""
        self.assertEqual(CombinationUtils.C(10, 3), 120)
        self.assertEqual(CombinationUtils.P(10, 3), 720)
        self.assertEqual(CombinationUtils.factorial(5), 120)
        self.assertEqual(CombinationUtils.catalan(5), 42)
    
    def test_generation_methods(self):
        """测试生成方法"""
        perms = CombinationUtils.permutations([1, 2])
        self.assertEqual(len(perms), 2)
        
        combs = CombinationUtils.combinations([1, 2, 3], 2)
        self.assertEqual(len(combs), 3)
        
        power = CombinationUtils.powerset([1, 2])
        self.assertEqual(len(power), 4)
    
    def test_special_numbers_methods(self):
        """测试特殊数方法"""
        self.assertEqual(CombinationUtils.stirling(5, 3), 25)
        self.assertEqual(CombinationUtils.stirling(4, 2, kind=1), 11)
        self.assertEqual(CombinationUtils.bell(5), 52)
        self.assertEqual(CombinationUtils.derangement(4), 9)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_C(self):
        """测试组合数便捷函数"""
        self.assertEqual(C(10, 3), 120)
        self.assertEqual(C(5, 0), 1)
        self.assertEqual(C(5, 5), 1)
    
    def test_P(self):
        """测试排列数便捷函数"""
        self.assertEqual(P(10, 3), 720)
        self.assertEqual(P(5, 0), 1)
        self.assertEqual(P(5, 5), 120)
    
    def test_factorial(self):
        """测试阶乘便捷函数"""
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(5), 120)
    
    def test_catalan(self):
        """测试卡特兰数便捷函数"""
        self.assertEqual(catalan(0), 1)
        self.assertEqual(catalan(5), 42)
    
    def test_generate_permutations(self):
        """测试排列生成便捷函数"""
        perms = generate_permutations([1, 2, 3])
        self.assertEqual(len(perms), 6)
    
    def test_generate_combinations(self):
        """测试组合生成便捷函数"""
        combs = generate_combinations([1, 2, 3, 4], 2)
        self.assertEqual(len(combs), 6)
    
    def test_generate_powerset(self):
        """测试幂集生成便捷函数"""
        power = generate_powerset([1, 2, 3])
        self.assertEqual(len(power), 8)


class TestLargeNumbers(unittest.TestCase):
    """大数测试"""
    
    def test_large_combination(self):
        """测试大组合数"""
        calc = CombinationCalculator()
        
        # C(100, 50) 是一个大数
        result = calc.combination(100, 50)
        self.assertGreater(result, 0)
        self.assertEqual(len(str(result)), 30)  # 约有 30 位
    
    def test_large_factorial(self):
        """测试大阶乘"""
        calc = CombinationCalculator()
        
        result = calc.factorial(20)
        self.assertEqual(result, 2432902008176640000)
    
    def test_large_catalan(self):
        """测试大卡特兰数"""
        special = SpecialNumbers()
        
        result = special.catalan(20)
        self.assertGreater(result, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)