"""
Prime Number Utilities - 测试用例

测试所有素数工具函数的正确性。
"""

import unittest
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prime_utils import (
    is_prime,
    is_prime_simple,
    generate_primes,
    prime_factors,
    euler_phi,
    gcd,
    lcm,
    next_prime,
    prev_prime,
    count_primes,
    nth_prime,
    is_coprime,
    extended_gcd,
    mod_inverse,
    primes_up_to,
)


class TestIsPrime(unittest.TestCase):
    """测试素数判断函数"""
    
    def test_small_primes(self):
        """测试小素数"""
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        for p in primes:
            self.assertTrue(is_prime(p), f"{p} should be prime")
            self.assertTrue(is_prime_simple(p), f"{p} should be prime (simple)")
    
    def test_small_composites(self):
        """测试小合数"""
        composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25]
        for c in composites:
            self.assertFalse(is_prime(c), f"{c} should not be prime")
            self.assertFalse(is_prime_simple(c), f"{c} should not be prime (simple)")
    
    def test_special_cases(self):
        """测试特殊值"""
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(-5))
        self.assertFalse(is_prime_simple(0))
        self.assertFalse(is_prime_simple(1))
    
    def test_large_primes(self):
        """测试大素数"""
        # 梅森素数
        self.assertTrue(is_prime(2**31 - 1))  # 第8个梅森素数
        # 大素数
        self.assertTrue(is_prime(999999999989))
    
    def test_large_composites(self):
        """测试大合数"""
        self.assertFalse(is_prime(2**32))
        self.assertFalse(is_prime(999999999990))
    
    def test_carmichael_numbers(self):
        """测试卡迈克尔数（伪素数）"""
        # 561, 1105, 1729 是卡迈克尔数
        self.assertFalse(is_prime(561))
        self.assertFalse(is_prime(1105))
        self.assertFalse(is_prime(1729))


class TestGeneratePrimes(unittest.TestCase):
    """测试素数生成函数"""
    
    def test_generate_primes_small(self):
        """测试生成小范围素数"""
        self.assertEqual(generate_primes(10), [2, 3, 5, 7])
        self.assertEqual(generate_primes(20), [2, 3, 5, 7, 11, 13, 17, 19])
    
    def test_generate_primes_edge(self):
        """测试边界情况"""
        self.assertEqual(generate_primes(1), [])
        self.assertEqual(generate_primes(2), [2])
        self.assertEqual(generate_primes(0), [])
        self.assertEqual(generate_primes(-5), [])
    
    def test_generate_primes_count(self):
        """测试生成素数的数量"""
        primes_100 = generate_primes(100)
        self.assertEqual(len(primes_100), 25)  # 100以内有25个素数
        
        primes_1000 = generate_primes(1000)
        self.assertEqual(len(primes_1000), 168)  # 1000以内有168个素数


class TestPrimeFactors(unittest.TestCase):
    """测试素因数分解函数"""
    
    def test_prime_factors_small(self):
        """测试小数分解"""
        self.assertEqual(prime_factors(12), [(2, 2), (3, 1)])
        self.assertEqual(prime_factors(60), [(2, 2), (3, 1), (5, 1)])
        self.assertEqual(prime_factors(17), [(17, 1)])
    
    def test_prime_factors_special(self):
        """测试特殊值"""
        self.assertEqual(prime_factors(1), [])
        self.assertEqual(prime_factors(2), [(2, 1)])
    
    def test_prime_factors_perfect_powers(self):
        """测试完全幂"""
        self.assertEqual(prime_factors(8), [(2, 3)])
        self.assertEqual(prime_factors(27), [(3, 3)])
        self.assertEqual(prime_factors(1024), [(2, 10)])
    
    def test_prime_factors_large(self):
        """测试大数分解"""
        factors = prime_factors(123456789)
        # 验证：乘积应该等于原数
        product = 1
        for p, e in factors:
            product *= p ** e
        self.assertEqual(product, 123456789)
    
    def test_prime_factors_negative(self):
        """测试负数输入"""
        with self.assertRaises(ValueError):
            prime_factors(-5)
        with self.assertRaises(ValueError):
            prime_factors(0)


class TestEulerPhi(unittest.TestCase):
    """测试欧拉函数"""
    
    def test_euler_phi_basic(self):
        """测试基本欧拉函数值"""
        self.assertEqual(euler_phi(1), 1)
        self.assertEqual(euler_phi(9), 6)  # 1,2,4,5,7,8
        self.assertEqual(euler_phi(12), 4)  # 1,5,7,11
        self.assertEqual(euler_phi(17), 16)  # 素数
    
    def test_euler_phi_prime(self):
        """测试素数的欧拉函数"""
        primes = [2, 3, 5, 7, 11, 13, 17, 19]
        for p in primes:
            self.assertEqual(euler_phi(p), p - 1)
    
    def test_euler_phi_prime_power(self):
        """测试素数幂的欧拉函数"""
        self.assertEqual(euler_phi(4), 2)   # φ(2^2) = 2^2 - 2^1 = 2
        self.assertEqual(euler_phi(8), 4)   # φ(2^3) = 2^3 - 2^2 = 4
        self.assertEqual(euler_phi(9), 6)   # φ(3^2) = 3^2 - 3^1 = 6
        self.assertEqual(euler_phi(27), 18) # φ(3^3) = 3^3 - 3^2 = 18
    
    def test_euler_phi_negative(self):
        """测试负数输入"""
        with self.assertRaises(ValueError):
            euler_phi(0)
        with self.assertRaises(ValueError):
            euler_phi(-5)


class TestGcdLcm(unittest.TestCase):
    """测试最大公约数和最小公倍数"""
    
    def test_gcd_basic(self):
        """测试基本GCD"""
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(17, 13), 1)
        self.assertEqual(gcd(100, 25), 25)
        self.assertEqual(gcd(0, 5), 5)
        self.assertEqual(gcd(5, 0), 5)
    
    def test_gcd_negative(self):
        """测试负数的GCD"""
        self.assertEqual(gcd(-48, 18), 6)
        self.assertEqual(gcd(48, -18), 6)
        self.assertEqual(gcd(-48, -18), 6)
    
    def test_lcm_basic(self):
        """测试基本LCM"""
        self.assertEqual(lcm(12, 18), 36)
        self.assertEqual(lcm(17, 13), 221)
        self.assertEqual(lcm(4, 6), 12)
    
    def test_lcm_error(self):
        """测试LCM错误情况"""
        with self.assertRaises(ValueError):
            lcm(0, 5)
        with self.assertRaises(ValueError):
            lcm(5, 0)


class TestExtendedGcd(unittest.TestCase):
    """测试扩展欧几里得算法"""
    
    def test_extended_gcd_basic(self):
        """测试基本扩展GCD"""
        g, x, y = extended_gcd(35, 15)
        self.assertEqual(g, 5)
        self.assertEqual(35 * x + 15 * y, 5)
        
        g, x, y = extended_gcd(17, 13)
        self.assertEqual(g, 1)
        self.assertEqual(17 * x + 13 * y, 1)
    
    def test_extended_gcd_special(self):
        """测试特殊值"""
        g, x, y = extended_gcd(5, 0)
        self.assertEqual(g, 5)
        self.assertEqual(x, 1)
        self.assertEqual(y, 0)


class TestModInverse(unittest.TestCase):
    """测试模逆元"""
    
    def test_mod_inverse_basic(self):
        """测试基本模逆元"""
        self.assertEqual(mod_inverse(3, 11), 4)  # 3*4 = 12 ≡ 1 (mod 11)
        self.assertEqual(mod_inverse(7, 11), 8)  # 7*8 = 56 ≡ 1 (mod 11)
    
    def test_mod_inverse_no_solution(self):
        """测试无解情况"""
        self.assertIsNone(mod_inverse(6, 9))  # gcd(6,9)=3
        self.assertIsNone(mod_inverse(4, 8))  # gcd(4,8)=4
    
    def test_mod_inverse_error(self):
        """测试错误输入"""
        with self.assertRaises(ValueError):
            mod_inverse(3, 0)
        with self.assertRaises(ValueError):
            mod_inverse(3, -5)


class TestNextPrevPrime(unittest.TestCase):
    """测试寻找相邻素数"""
    
    def test_next_prime(self):
        """测试下一个素数"""
        self.assertEqual(next_prime(10), 11)
        self.assertEqual(next_prime(17), 19)
        self.assertEqual(next_prime(1), 2)
        self.assertEqual(next_prime(0), 2)
    
    def test_prev_prime(self):
        """测试前一个素数"""
        self.assertEqual(prev_prime(10), 7)
        self.assertEqual(prev_prime(17), 13)
        self.assertEqual(prev_prime(3), 2)
        self.assertIsNone(prev_prime(2))
        self.assertIsNone(prev_prime(1))


class TestCountPrimes(unittest.TestCase):
    """测试素数计数函数"""
    
    def test_count_primes(self):
        """测试素数计数"""
        self.assertEqual(count_primes(10), 4)
        self.assertEqual(count_primes(100), 25)
        self.assertEqual(count_primes(1), 0)
        self.assertEqual(count_primes(0), 0)


class TestNthPrime(unittest.TestCase):
    """测试第n个素数"""
    
    def test_nth_prime(self):
        """测试第n个素数"""
        self.assertEqual(nth_prime(1), 2)
        self.assertEqual(nth_prime(5), 11)
        self.assertEqual(nth_prime(10), 29)
        self.assertEqual(nth_prime(100), 541)
    
    def test_nth_prime_error(self):
        """测试错误输入"""
        with self.assertRaises(ValueError):
            nth_prime(0)
        with self.assertRaises(ValueError):
            nth_prime(-5)


class TestIsCoprime(unittest.TestCase):
    """测试互质判断"""
    
    def test_is_coprime(self):
        """测试互质判断"""
        self.assertTrue(is_coprime(15, 28))
        self.assertTrue(is_coprime(17, 13))
        self.assertFalse(is_coprime(12, 18))
        self.assertFalse(is_coprime(6, 9))
    
    def test_is_coprime_with_one(self):
        """测试与1的关系"""
        self.assertTrue(is_coprime(1, 5))
        self.assertTrue(is_coprime(7, 1))


class TestPrimesUpTo(unittest.TestCase):
    """测试素数生成器"""
    
    def test_primes_up_to(self):
        """测试生成器"""
        self.assertEqual(list(primes_up_to(10)), [2, 3, 5, 7])
        self.assertEqual(list(primes_up_to(2)), [2])
        self.assertEqual(list(primes_up_to(1)), [])
    
    def test_primes_up_to_memory(self):
        """测试生成器内存效率"""
        # 生成器不应该立即创建列表
        gen = primes_up_to(1000000)
        self.assertTrue(hasattr(gen, '__iter__'))


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_factorize_then_reconstruct(self):
        """测试分解后重构"""
        for n in [60, 12345, 999983]:
            factors = prime_factors(n)
            product = 1
            for p, e in factors:
                product *= p ** e
            self.assertEqual(product, n)
    
    def test_euler_phi_from_factors(self):
        """测试欧拉函数与因子的关系"""
        for n in range(2, 50):
            factors = prime_factors(n)
            phi_from_factors = n
            for p, _ in factors:
                phi_from_factors = phi_from_factors // p * (p - 1)
            self.assertEqual(euler_phi(n), phi_from_factors)
    
    def test_coprime_via_gcd(self):
        """测试互质与GCD的关系"""
        for a in range(1, 20):
            for b in range(1, 20):
                self.assertEqual(is_coprime(a, b), gcd(a, b) == 1)
    
    def test_prime_consistency(self):
        """测试不同方法的一致性"""
        primes = generate_primes(1000)
        for p in primes:
            self.assertTrue(is_prime(p))
            self.assertTrue(is_prime_simple(p))
        
        for i in range(1, 101):
            self.assertEqual(nth_prime(i), primes[i-1])


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestIsPrime))
    suite.addTests(loader.loadTestsFromTestCase(TestGeneratePrimes))
    suite.addTests(loader.loadTestsFromTestCase(TestPrimeFactors))
    suite.addTests(loader.loadTestsFromTestCase(TestEulerPhi))
    suite.addTests(loader.loadTestsFromTestCase(TestGcdLcm))
    suite.addTests(loader.loadTestsFromTestCase(TestExtendedGcd))
    suite.addTests(loader.loadTestsFromTestCase(TestModInverse))
    suite.addTests(loader.loadTestsFromTestCase(TestNextPrevPrime))
    suite.addTests(loader.loadTestsFromTestCase(TestCountPrimes))
    suite.addTests(loader.loadTestsFromTestCase(TestNthPrime))
    suite.addTests(loader.loadTestsFromTestCase(TestIsCoprime))
    suite.addTests(loader.loadTestsFromTestCase(TestPrimesUpTo))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    run_tests()