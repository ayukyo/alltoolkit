"""
中国剩余定理工具模块测试

测试覆盖：
1. 扩展欧几里得算法
2. 模逆运算
3. 中国剩余定理求解
4. Garner方法
5. 干支纪年应用
6. RSA解密加速
7. 边界条件和异常处理
"""

import unittest
import math
from mod import (
    extended_gcd,
    modular_inverse,
    crt_two_equations,
    chinese_remainder_theorem,
    crt_garner_method,
    is_solvable,
    all_solutions,
    ganzhi_year,
    ganzhi_from_crt,
    year_from_ganzhi,
    rsa_decrypt_crt,
    lcm,
    lcm_list,
    solve_linear_congruence,
    count_solutions,
    ChineseRemainder
)


class TestExtendedGCD(unittest.TestCase):
    """扩展欧几里得算法测试"""
    
    def test_basic_cases(self):
        """基本测试用例"""
        # gcd(35, 15) = 5, 35*1 + 15*(-2) = 5
        gcd, x, y = extended_gcd(35, 15)
        self.assertEqual(gcd, 5)
        self.assertEqual(35 * x + 15 * y, 5)
        
        # gcd(240, 46) = 2
        gcd, x, y = extended_gcd(240, 46)
        self.assertEqual(gcd, 2)
        self.assertEqual(240 * x + 46 * y, 2)
    
    def test_coprime(self):
        """互质数测试"""
        gcd, x, y = extended_gcd(17, 13)
        self.assertEqual(gcd, 1)
        self.assertEqual(17 * x + 13 * y, 1)
    
    def test_one_is_zero(self):
        """其中一个为零"""
        gcd, x, y = extended_gcd(5, 0)
        self.assertEqual(gcd, 5)
        self.assertEqual(x, 1)
        self.assertEqual(y, 0)
        
        gcd, x, y = extended_gcd(0, 7)
        self.assertEqual(gcd, 7)
        self.assertEqual(x, 0)
        self.assertEqual(y, 1)
    
    def test_same_number(self):
        """相同数字"""
        gcd, x, y = extended_gcd(12, 12)
        self.assertEqual(gcd, 12)
    
    def test_negative_numbers(self):
        """负数处理"""
        # 扩展欧几里得算法对负数的处理
        gcd, x, y = extended_gcd(-15, 10)
        self.assertEqual(gcd, 5)


class TestModularInverse(unittest.TestCase):
    """模逆运算测试"""
    
    def test_basic_inverse(self):
        """基本逆元测试"""
        # 3 * 5 = 15 ≡ 1 (mod 7)
        inv = modular_inverse(3, 7)
        self.assertEqual(inv, 5)
        self.assertEqual((3 * inv) % 7, 1)
        
        # 7 * 15 = 105 ≡ 1 (mod 26)
        inv = modular_inverse(7, 26)
        self.assertEqual((7 * inv) % 26, 1)
    
    def test_no_inverse(self):
        """逆元不存在的情况"""
        # gcd(2, 4) = 2 ≠ 1，无逆元
        inv = modular_inverse(2, 4)
        self.assertIsNone(inv)
        
        # gcd(6, 9) = 3 ≠ 1，无逆元
        inv = modular_inverse(6, 9)
        self.assertIsNone(inv)
    
    def test_identity(self):
        """1的逆元是1"""
        inv = modular_inverse(1, 7)
        self.assertEqual(inv, 1)
    
    def test_prime_modulus(self):
        """素数模数下非零元素都有逆元"""
        for a in range(1, 7):
            inv = modular_inverse(a, 7)
            self.assertIsNotNone(inv)
            self.assertEqual((a * inv) % 7, 1)


class TestCRTTwoEquations(unittest.TestCase):
    """两个同余方程求解测试"""
    
    def test_basic(self):
        """基本测试"""
        # x ≡ 2 (mod 3)
        # x ≡ 3 (mod 5)
        # 解: x ≡ 8 (mod 15)
        result = crt_two_equations(2, 3, 3, 5)
        self.assertIsNotNone(result)
        x, M = result
        self.assertEqual(x, 8)
        self.assertEqual(M, 15)
    
    def test_coprime_moduli(self):
        """互质模数"""
        # x ≡ 1 (mod 4)
        # x ≡ 2 (mod 5)
        result = crt_two_equations(1, 4, 2, 5)
        self.assertIsNotNone(result)
        x, M = result
        self.assertEqual(x % 4, 1)
        self.assertEqual(x % 5, 2)
        self.assertEqual(M, 20)
    
    def test_non_coprime_solvable(self):
        """非互质模数但有解"""
        # x ≡ 2 (mod 4)
        # x ≡ 4 (mod 6)
        # gcd(4,6)=2, 2≡4 (mod 2)，有解
        result = crt_two_equations(2, 4, 4, 6)
        self.assertIsNotNone(result)
        x, M = result
        self.assertEqual(x % 4, 2)
        self.assertEqual(x % 6, 4)
    
    def test_non_coprime_no_solution(self):
        """非互质模数且无解"""
        # x ≡ 1 (mod 4)
        # x ≡ 2 (mod 6)
        # gcd(4,6)=2, 1≠2 (mod 2)，无解
        result = crt_two_equations(1, 4, 2, 6)
        self.assertIsNone(result)


class TestChineseRemainderTheorem(unittest.TestCase):
    """中国剩余定理测试"""
    
    def test_sunzi_problem(self):
        """孙子算经经典问题"""
        # 三三数之剩二，五五数之剩三，七七数之剩二
        result = chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
        self.assertIsNotNone(result)
        x, M = result
        self.assertEqual(x, 23)
        self.assertEqual(M, 105)
        
        # 验证
        self.assertEqual(x % 3, 2)
        self.assertEqual(x % 5, 3)
        self.assertEqual(x % 7, 2)
    
    def test_simple_case(self):
        """简单测试"""
        result = chinese_remainder_theorem([1, 2, 3], [2, 3, 5])
        self.assertIsNotNone(result)
        x, M = result
        self.assertEqual(x % 2, 1)
        self.assertEqual(x % 3, 2)
        self.assertEqual(x % 5, 3)
    
    def test_single_equation(self):
        """单个方程"""
        result = chinese_remainder_theorem([7], [11])
        self.assertIsNotNone(result)
        x, M = result
        self.assertEqual(x, 7)
        self.assertEqual(M, 11)
    
    def test_large_numbers(self):
        """大数测试"""
        result = chinese_remainder_theorem([1, 2, 3, 4], [5, 7, 9, 11])
        self.assertIsNotNone(result)
        x, M = result
        self.assertEqual(x % 5, 1)
        self.assertEqual(x % 7, 2)
        self.assertEqual(x % 9, 3)
        self.assertEqual(x % 11, 4)
    
    def test_invalid_input(self):
        """无效输入"""
        with self.assertRaises(ValueError):
            chinese_remainder_theorem([1, 2], [3])  # 长度不匹配
        
        with self.assertRaises(ValueError):
            chinese_remainder_theorem([], [])  # 空列表


class TestGarnerMethod(unittest.TestCase):
    """Garner方法测试"""
    
    def test_basic(self):
        """基本测试"""
        result = crt_garner_method([2, 3, 2], [3, 5, 7])
        self.assertEqual(result, 23)
    
    def test_consistency_with_crt(self):
        """与标准CRT结果一致性"""
        test_cases = [
            ([1, 2, 3], [2, 3, 5]),
            ([0, 0, 0], [3, 5, 7]),
            ([2, 4, 6], [3, 5, 7]),
        ]
        
        for remainders, moduli in test_cases:
            crt_result = chinese_remainder_theorem(remainders, moduli)
            garner_result = crt_garner_method(remainders, moduli)
            
            self.assertIsNotNone(crt_result)
            self.assertIsNotNone(garner_result)
            self.assertEqual(crt_result[0], garner_result)


class TestIsSolvable(unittest.TestCase):
    """可解性判断测试"""
    
    def test_solvable_cases(self):
        """有解情况"""
        self.assertTrue(is_solvable([2, 3, 2], [3, 5, 7]))
        # gcd(3,6)=3, 需要 (a1-a2) % gcd == 0
        # 3 ≡ 6 (mod 3) 因为 (3-6)=-3, -3 % 3 = 0
        self.assertTrue(is_solvable([3, 6], [3, 6]))  # gcd(3,6)=3, 3≡6 (mod 3)
        self.assertTrue(is_solvable([4, 10], [3, 6]))  # gcd(3,6)=3, 4≡10 (mod 3)
    
    def test_unsolvable_cases(self):
        """无解情况"""
        self.assertFalse(is_solvable([2, 3], [4, 6]))  # gcd(4,6)=2, 2≠3 (mod 2)
        self.assertFalse(is_solvable([1, 0], [2, 4]))  # gcd(2,4)=2, 1≠0 (mod 2)
    
    def test_length_mismatch(self):
        """长度不匹配"""
        self.assertFalse(is_solvable([1, 2], [3, 4, 5]))


class TestAllSolutions(unittest.TestCase):
    """多解测试"""
    
    def test_basic(self):
        """基本测试"""
        solutions = all_solutions([2, 3], [3, 5], limit=5)
        self.assertEqual(len(solutions), 5)
        
        # 验证每个解
        for sol in solutions:
            self.assertEqual(sol % 3, 2)
            self.assertEqual(sol % 5, 3)
        
        # 验证解的间隔
        for i in range(len(solutions) - 1):
            self.assertEqual(solutions[i + 1] - solutions[i], 15)
    
    def test_no_solution(self):
        """无解情况"""
        solutions = all_solutions([1, 2], [4, 6], limit=5)
        self.assertEqual(len(solutions), 0)


class TestGanzhiYear(unittest.TestCase):
    """干支纪年测试"""
    
    def test_known_years(self):
        """已知年份测试"""
        # 1984年是甲子年
        gan, zhi = ganzhi_year(1984)
        self.assertEqual(gan, '甲')
        self.assertEqual(zhi, '子')
        
        # 2000年是庚辰年
        gan, zhi = ganzhi_year(2000)
        self.assertEqual(gan, '庚')
        self.assertEqual(zhi, '辰')
        
        # 2024年是甲辰年
        gan, zhi = ganzhi_year(2024)
        self.assertEqual(gan, '甲')
        self.assertEqual(zhi, '辰')
        
        # 2025年是乙巳年
        gan, zhi = ganzhi_year(2025)
        self.assertEqual(gan, '乙')
        self.assertEqual(zhi, '巳')
    
    def test_cycle(self):
        """60年周期测试"""
        # 相差60年应该有相同的干支
        for year in [1900, 1950, 2000]:
            gan1, zhi1 = ganzhi_year(year)
            gan2, zhi2 = ganzhi_year(year + 60)
            self.assertEqual(gan1, gan2)
            self.assertEqual(zhi1, zhi2)
    
    def test_consistency(self):
        """ganzhi_year 和 ganzhi_from_crt 一致性"""
        for year in range(2000, 2030):
            gan1, zhi1 = ganzhi_year(year)
            gan2, zhi2 = ganzhi_from_crt(year)
            self.assertEqual(gan1, gan2, f"Year {year} mismatch")
            self.assertEqual(zhi1, zhi2, f"Year {year} mismatch")


class TestYearFromGanzhi(unittest.TestCase):
    """从干支推算年份测试"""
    
    def test_roundtrip(self):
        """往返测试"""
        for year in range(2000, 2060):  # 在21世纪内测试
            gan, zhi = ganzhi_year(year)
            calculated_year = year_from_ganzhi(gan, zhi, 21)
            self.assertEqual(calculated_year, year, f"Year {year} ({gan}{zhi}) mismatch")


class TestRSADecryptCRT(unittest.TestCase):
    """RSA-CRT解密测试"""
    
    def test_small_example(self):
        """小数示例"""
        p, q = 61, 53
        n = p * q  # 3233
        e, d = 17, 2753
        
        for m in [0, 1, 42, 123, 999]:
            c = pow(m, e, n)
            decrypted = rsa_decrypt_crt(c, d, p, q)
            self.assertEqual(decrypted, m, f"Failed for m={m}")
    
    def test_medium_primes(self):
        """中等素数测试"""
        p, q = 101, 103
        n = p * q  # 10403
        phi_n = (p - 1) * (q - 1)  # 10200
        e = 7
        # 计算 d = e^(-1) mod phi(n)
        from mod import modular_inverse
        d = modular_inverse(e, phi_n)
        
        for m in [0, 1, 100, 500, 1000]:
            c = pow(m, e, n)
            decrypted = rsa_decrypt_crt(c, d, p, q)
            self.assertEqual(decrypted, m)


class TestHelperFunctions(unittest.TestCase):
    """辅助函数测试"""
    
    def test_lcm(self):
        """最小公倍数测试"""
        self.assertEqual(lcm(12, 18), 36)
        self.assertEqual(lcm(4, 6), 12)
        self.assertEqual(lcm(7, 11), 77)
        self.assertEqual(lcm(5, 0), 0)
    
    def test_lcm_list(self):
        """多数字最小公倍数测试"""
        self.assertEqual(lcm_list([2, 3, 4]), 12)
        self.assertEqual(lcm_list([3, 5, 7]), 105)
        self.assertEqual(lcm_list([4, 6, 8]), 24)
    
    def test_solve_linear_congruence(self):
        """线性同余方程测试"""
        # 3x ≡ 6 (mod 9)
        solutions = solve_linear_congruence(3, 6, 9)
        self.assertEqual(len(solutions), 3)  # gcd(3,9)=3个解
        for sol in solutions:
            self.assertEqual((3 * sol) % 9, 6)
        
        # 2x ≡ 3 (mod 4)，无解
        solutions = solve_linear_congruence(2, 3, 4)
        self.assertEqual(len(solutions), 0)
    
    def test_count_solutions(self):
        """解的计数测试"""
        count = count_solutions([2, 3, 2], [3, 5, 7], 1000)
        self.assertEqual(count, 10)  # 1000/105 ≈ 9.5，所以有10个


class TestChineseRemainderClass(unittest.TestCase):
    """ChineseRemainder类测试"""
    
    def test_basic(self):
        """基本功能测试"""
        crt = ChineseRemainder([3, 5, 7])
        result = crt.solve([2, 3, 2])
        self.assertEqual(result, 23)
        
        result = crt.solve([1, 2, 3])
        self.assertEqual(result, 52)
    
    def test_get_period(self):
        """周期测试"""
        crt = ChineseRemainder([3, 5, 7])
        self.assertEqual(crt.get_period(), 105)
    
    def test_get_all_solutions(self):
        """多解测试"""
        crt = ChineseRemainder([3, 5])
        solutions = crt.get_all_solutions([2, 3], count=5)
        self.assertEqual(len(solutions), 5)
        for sol in solutions:
            self.assertEqual(sol % 3, 2)
            self.assertEqual(sol % 5, 3)
    
    def test_invalid_input(self):
        """无效输入测试"""
        crt = ChineseRemainder([3, 5, 7])
        with self.assertRaises(ValueError):
            crt.solve([1, 2])  # 长度不匹配


if __name__ == "__main__":
    unittest.main(verbosity=2)