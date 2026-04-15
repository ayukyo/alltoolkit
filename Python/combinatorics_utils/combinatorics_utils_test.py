"""
Combinatorics Utils - 测试文件

测试组合数学工具集的所有功能。
"""

import unittest
from mod import (
    # 基础计算
    factorial, factorial_range, binomial, multinomial,
    # 排列
    permutations, permutations_count, permutations_with_replacement,
    # 组合
    combinations, combinations_count, combinations_with_replacement,
    combinations_with_replacement_count,
    # 笛卡尔积
    cartesian_product, cartesian_product_count,
    # 幂集
    powerset, powerset_count, subsets_of_size,
    # 特殊数列
    catalan, stirling_first, stirling_second, bell_number,
    partition_number, partitions,
    # 抽屉原理
    pigeonhole_count, pigeonhole_min_max, check_pigeonhole_violation,
    # 组合搜索
    nth_combination, nth_permutation, combination_index,
    # 实用函数
    generate_random_combination, generate_random_permutation,
    count_anagrams, derangements, permutations_with_sign,
    subset_sum,
    # 预计算表
    generate_pascal_triangle, generate_catalan_sequence,
    generate_stirling_first_table, generate_stirling_second_table,
)


class TestFactorial(unittest.TestCase):
    """阶乘测试"""
    
    def test_basic_factorial(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(10), 3628800)
    
    def test_negative_factorial(self):
        with self.assertRaises(ValueError):
            factorial(-1)
    
    def test_factorial_range(self):
        self.assertEqual(factorial_range(5, 3), 60)  # 5*4*3
        self.assertEqual(factorial_range(10, 2), 90)  # 10*9
        self.assertEqual(factorial_range(5, 0), 1)
        self.assertEqual(factorial_range(5, 5), 120)


class TestBinomial(unittest.TestCase):
    """二项式系数测试"""
    
    def test_basic_binomial(self):
        self.assertEqual(binomial(5, 2), 10)
        self.assertEqual(binomial(10, 5), 252)
        self.assertEqual(binomial(6, 3), 20)
        self.assertEqual(binomial(4, 0), 1)
        self.assertEqual(binomial(4, 4), 1)
    
    def test_edge_cases(self):
        self.assertEqual(binomial(5, 0), 1)
        self.assertEqual(binomial(5, 5), 1)
        self.assertEqual(binomial(5, 6), 0)
        self.assertEqual(binomial(5, -1), 0)
    
    def test_symmetry(self):
        self.assertEqual(binomial(10, 3), binomial(10, 7))
        self.assertEqual(binomial(20, 8), binomial(20, 12))
    
    def test_pascal_identity(self):
        # C(n, k) = C(n-1, k-1) + C(n-1, k)
        for n in range(5, 15):
            for k in range(1, n):
                self.assertEqual(
                    binomial(n, k),
                    binomial(n - 1, k - 1) + binomial(n - 1, k)
                )


class TestMultinomial(unittest.TestCase):
    """多项式系数测试"""
    
    def test_basic_multinomial(self):
        # (a+b+c)^3 的系数
        self.assertEqual(multinomial(3, 0, 0), 1)
        self.assertEqual(multinomial(2, 1, 0), 3)
        self.assertEqual(multinomial(1, 1, 1), 6)


class TestPermutations(unittest.TestCase):
    """排列测试"""
    
    def test_full_permutations(self):
        result = list(permutations([1, 2, 3]))
        self.assertEqual(len(result), 6)
        self.assertIn((1, 2, 3), result)
        self.assertIn((3, 2, 1), result)
    
    def test_partial_permutations(self):
        result = list(permutations([1, 2, 3], 2))
        self.assertEqual(len(result), 6)
        self.assertIn((1, 2), result)
        self.assertIn((3, 1), result)
    
    def test_permutations_count(self):
        self.assertEqual(permutations_count(5, 3), 60)
        self.assertEqual(permutations_count(5, 5), 120)
        self.assertEqual(permutations_count(5, 0), 1)
    
    def test_permutations_with_replacement(self):
        result = list(permutations_with_replacement([1, 2], 2))
        self.assertEqual(len(result), 4)
        self.assertIn((1, 1), result)
        self.assertIn((2, 2), result)


class TestCombinations(unittest.TestCase):
    """组合测试"""
    
    def test_basic_combinations(self):
        result = list(combinations([1, 2, 3, 4], 2))
        self.assertEqual(len(result), 6)
        self.assertIn((1, 2), result)
        self.assertNotIn((2, 1), result)  # 顺序不重要
    
    def test_combinations_count(self):
        self.assertEqual(combinations_count(5, 2), 10)
        self.assertEqual(combinations_count(10, 3), 120)
    
    def test_combinations_with_replacement(self):
        result = list(combinations_with_replacement([1, 2], 3))
        self.assertEqual(len(result), 4)
        self.assertIn((1, 1, 1), result)
        self.assertIn((2, 2, 2), result)
    
    def test_combinations_with_replacement_count(self):
        self.assertEqual(combinations_with_replacement_count(3, 2), 6)
        self.assertEqual(combinations_with_replacement_count(5, 3), 35)


class TestCartesianProduct(unittest.TestCase):
    """笛卡尔积测试"""
    
    def test_basic_cartesian(self):
        result = list(cartesian_product([1, 2], ['a', 'b']))
        self.assertEqual(len(result), 4)
        self.assertIn((1, 'a'), result)
        self.assertIn((2, 'b'), result)
    
    def test_cartesian_with_repeat(self):
        result = list(cartesian_product([1, 2], repeat=2))
        self.assertEqual(len(result), 4)
    
    def test_cartesian_count(self):
        self.assertEqual(cartesian_product_count(2, 3), 6)
        self.assertEqual(cartesian_product_count(2, 3, repeat=2), 36)


class TestPowerset(unittest.TestCase):
    """幂集测试"""
    
    def test_basic_powerset(self):
        result = list(powerset([1, 2]))
        self.assertEqual(len(result), 4)
        self.assertIn((), result)
        self.assertIn((1,), result)
        self.assertIn((2,), result)
        self.assertIn((1, 2), result)
    
    def test_powerset_count(self):
        self.assertEqual(powerset_count(0), 1)
        self.assertEqual(powerset_count(3), 8)
        self.assertEqual(powerset_count(10), 1024)
    
    def test_subsets_of_size(self):
        result = list(subsets_of_size([1, 2, 3, 4], 2))
        self.assertEqual(len(result), 6)


class TestCatalan(unittest.TestCase):
    """卡塔兰数测试"""
    
    def test_catalan_sequence(self):
        expected = [1, 1, 2, 5, 14, 42, 132, 429]
        for i, val in enumerate(expected):
            self.assertEqual(catalan(i), val)
    
    def test_catalan_formula(self):
        # C_n = C(2n, n) / (n+1)
        for n in range(10):
            self.assertEqual(catalan(n), binomial(2 * n, n) // (n + 1))


class TestStirlingNumbers(unittest.TestCase):
    """斯特林数测试"""
    
    def test_stirling_first(self):
        # s(4, 2) = 11
        self.assertEqual(stirling_first(4, 2), 11)
        # s(5, 1) = 24 = 4!
        self.assertEqual(stirling_first(5, 1), 24)
    
    def test_stirling_second(self):
        # S(4, 2) = 7
        self.assertEqual(stirling_second(4, 2), 7)
        # S(5, 3) = 25
        self.assertEqual(stirling_second(5, 3), 25)
    
    def test_stirling_recursion(self):
        # s(n, k) = s(n-1, k-1) + (n-1)*s(n-1, k)
        for n in range(2, 10):
            for k in range(1, n):
                self.assertEqual(
                    stirling_first(n, k),
                    stirling_first(n - 1, k - 1) + (n - 1) * stirling_first(n - 1, k)
                )


class TestBellNumber(unittest.TestCase):
    """贝尔数测试"""
    
    def test_bell_sequence(self):
        expected = [1, 1, 2, 5, 15, 52, 203]
        for i, val in enumerate(expected):
            self.assertEqual(bell_number(i), val)
    
    def test_bell_stirling_relation(self):
        # B_n = sum(S(n, k))
        for n in range(10):
            self.assertEqual(
                bell_number(n),
                sum(stirling_second(n, k) for k in range(n + 1))
            )


class TestPartitionNumber(unittest.TestCase):
    """分拆数测试"""
    
    def test_partition_sequence(self):
        expected = [1, 1, 2, 3, 5, 7, 11, 15, 22, 30]
        for i, val in enumerate(expected):
            self.assertEqual(partition_number(i), val)
    
    def test_partitions_generator(self):
        result = list(partitions(4))
        self.assertEqual(len(result), 5)
        self.assertIn([4], result)
        self.assertIn([3, 1], result)
        self.assertIn([2, 2], result)
        self.assertIn([2, 1, 1], result)
        self.assertIn([1, 1, 1, 1], result)


class TestPigeonhole(unittest.TestCase):
    """抽屉原理测试"""
    
    def test_pigeonhole_count(self):
        self.assertEqual(pigeonhole_count(13, 12), 2)
        self.assertEqual(pigeonhole_count(25, 5), 5)
        self.assertEqual(pigeonhole_count(10, 3), 4)
    
    def test_pigeonhole_min_max(self):
        min_count, max_count = pigeonhole_min_max(10, 3)
        self.assertEqual(min_count, 3)
        self.assertEqual(max_count, 4)
    
    def test_pigeonhole_violation(self):
        self.assertTrue(check_pigeonhole_violation([1, 2, 3, 4, 5], 2, 2))
        self.assertFalse(check_pigeonhole_violation([1, 2, 3, 4], 2, 2))


class TestNthCombination(unittest.TestCase):
    """第N个组合测试"""
    
    def test_nth_combination_basic(self):
        elements = [1, 2, 3, 4, 5]
        self.assertEqual(nth_combination(elements, 3, 0), (1, 2, 3))
        self.assertEqual(nth_combination(elements, 3, 1), (1, 2, 4))
    
    def test_nth_combination_all(self):
        elements = [1, 2, 3, 4]
        all_combs = list(combinations(elements, 2))
        for i, comb in enumerate(all_combs):
            self.assertEqual(nth_combination(elements, 2, i), comb)
    
    def test_nth_combination_index_error(self):
        with self.assertRaises(IndexError):
            nth_combination([1, 2, 3], 2, 10)


class TestNthPermutation(unittest.TestCase):
    """第N个排列测试"""
    
    def test_nth_permutation_basic(self):
        elements = [1, 2, 3, 4]
        self.assertEqual(nth_permutation(elements, 4, 0), (1, 2, 3, 4))
    
    def test_nth_permutation_all(self):
        elements = [1, 2, 3]
        all_perms = list(permutations(elements))
        for i, perm in enumerate(all_perms):
            self.assertEqual(nth_permutation(elements, 3, i), perm)


class TestRandomFunctions(unittest.TestCase):
    """随机函数测试"""
    
    def test_random_combination(self):
        comb = generate_random_combination(10, 3, seed=42)
        self.assertEqual(len(comb), 3)
        self.assertEqual(len(set(comb)), 3)  # 无重复
    
    def test_random_permutation(self):
        perm = generate_random_permutation(5, seed=42)
        self.assertEqual(len(perm), 5)
        self.assertEqual(set(perm), set(range(5)))


class TestAnagrams(unittest.TestCase):
    """变位词测试"""
    
    def test_unique_chars(self):
        self.assertEqual(count_anagrams('abc'), 6)
        self.assertEqual(count_anagrams('abcd'), 24)
    
    def test_repeated_chars(self):
        self.assertEqual(count_anagrams('aab'), 3)
        self.assertEqual(count_anagrams('aabb'), 6)


class TestDerangements(unittest.TestCase):
    """错排数测试"""
    
    def test_derangement_sequence(self):
        expected = [1, 0, 1, 2, 9, 44, 265]
        for i, val in enumerate(expected):
            self.assertEqual(derangements(i), val)


class TestSubsetSum(unittest.TestCase):
    """子集和测试"""
    
    def test_subset_sum_basic(self):
        numbers = [3, 34, 4, 12, 5, 2]
        result = subset_sum(numbers, 9)
        self.assertIsNotNone(result)
        self.assertEqual(sum(result), 9)
    
    def test_subset_sum_no_solution(self):
        numbers = [1, 2, 4]
        result = subset_sum(numbers, 7)
        # 1 + 2 + 4 = 7, 所以这个应该有解
        self.assertIsNotNone(result)
        self.assertEqual(sum(result), 7)
    
    def test_subset_sum_truly_no_solution(self):
        numbers = [5, 10, 15]
        result = subset_sum(numbers, 7)
        self.assertIsNone(result)
    
    def test_subset_sum_exact(self):
        result = subset_sum([1, 2, 3], 6)
        self.assertEqual(sum(result), 6)


class TestPascalTriangle(unittest.TestCase):
    """帕斯卡三角形测试"""
    
    def test_pascal_triangle(self):
        triangle = generate_pascal_triangle(5)
        self.assertEqual(triangle[0], [1])
        self.assertEqual(triangle[1], [1, 1])
        self.assertEqual(triangle[2], [1, 2, 1])
        self.assertEqual(triangle[3], [1, 3, 3, 1])
        self.assertEqual(triangle[4], [1, 4, 6, 4, 1])


class TestCatalanSequence(unittest.TestCase):
    """卡塔兰序列测试"""
    
    def test_catalan_sequence(self):
        seq = generate_catalan_sequence(8)
        expected = [1, 1, 2, 5, 14, 42, 132, 429]
        self.assertEqual(seq, expected)


class TestStirlingTables(unittest.TestCase):
    """斯特林数表测试"""
    
    def test_stirling_first_table(self):
        table = generate_stirling_first_table(5)
        self.assertEqual(table[4][2], 11)  # s(4, 2) = 11
    
    def test_stirling_second_table(self):
        table = generate_stirling_second_table(5)
        self.assertEqual(table[4][2], 7)   # S(4, 2) = 7
        self.assertEqual(table[5][3], 25)  # S(5, 3) = 25


class TestLargeNumbers(unittest.TestCase):
    """大数测试"""
    
    def test_large_factorial(self):
        result = factorial(100)
        self.assertTrue(result > 0)
        # 验证末尾零的数量
        zeros = 0
        n = 100
        while n >= 5:
            zeros += n // 5
            n //= 5
        self.assertTrue(str(result).endswith('0' * zeros))
    
    def test_large_binomial(self):
        result = binomial(100, 50)
        self.assertTrue(result > 0)
        # C(100, 50) 应该是一个很大的数
        self.assertTrue(result > 10**29)
    
    def test_large_catalan(self):
        result = catalan(20)
        self.assertTrue(result > 0)
        # C_20 = 6564120420
        self.assertEqual(result, 6564120420)


if __name__ == '__main__':
    unittest.main()