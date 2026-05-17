"""
Unit tests for Armstrong Number Utilities
"""

import unittest
from mod import (
    is_armstrong, get_armstrong_digits, find_armstrong_numbers,
    generate_armstrong_numbers, get_next_armstrong, count_armstrong_digits,
    sum_of_squares_of_digits, is_happy, get_happy_sequence, find_happy_numbers,
    is_kaprekar, find_kaprekar_numbers, kaprekar_routine,
    get_proper_divisors, is_perfect, find_perfect_numbers, is_abundant, is_deficient,
    is_palindrome, find_palindrome_numbers, reverse_number, is_lychrel, get_lychrel_sequence,
    analyze_number, find_special_numbers, is_narcissistic, is_pluperfect,
    digital_root, is_harshad, find_harshad_numbers
)


class TestArmstrongNumber(unittest.TestCase):
    """阿姆斯特朗数测试"""
    
    def test_single_digit_armstrong(self):
        """测试 0-9 都是阿姆斯特朗数"""
        for i in range(10):
            self.assertTrue(is_armstrong(i), f"{i} should be Armstrong number")
    
    def test_known_armstrong_numbers(self):
        """测试已知的阿姆斯特朗数"""
        known_armstrong = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634, 8208, 9474]
        for num in known_armstrong:
            self.assertTrue(is_armstrong(num), f"{num} should be Armstrong number")
    
    def test_non_armstrong_numbers(self):
        """测试非阿姆斯特朗数"""
        non_armstrong = [10, 154, 200, 500, 1000, 2000]
        for num in non_armstrong:
            self.assertFalse(is_armstrong(num), f"{num} should not be Armstrong number")
    
    def test_negative_numbers(self):
        """测试负数"""
        self.assertFalse(is_armstrong(-1))
        self.assertFalse(is_armstrong(-153))
    
    def test_get_armstrong_digits(self):
        """测试获取阿姆斯特朗数的位数和幂和"""
        self.assertEqual(get_armstrong_digits(153), (3, 153, 0))
        self.assertEqual(get_armstrong_digits(154), (3, 190, 36))
        self.assertEqual(get_armstrong_digits(0), (1, 0, 0))
        self.assertEqual(get_armstrong_digits(-1), (0, 0, 0))
    
    def test_find_armstrong_numbers(self):
        """测试查找阿姆斯特朗数"""
        result = find_armstrong_numbers(500)
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407]
        self.assertEqual(result, expected)
    
    def test_generate_armstrong_numbers(self):
        """测试生成阿姆斯特朗数"""
        gen = generate_armstrong_numbers()
        first_15 = [next(gen) for _ in range(15)]
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634]
        self.assertEqual(first_15, expected)
    
    def test_get_next_armstrong(self):
        """测试获取下一个阿姆斯特朗数"""
        self.assertEqual(get_next_armstrong(150), 153)
        self.assertEqual(get_next_armstrong(200), 370)
        self.assertEqual(get_next_armstrong(400), 407)
    
    def test_count_armstrong_digits(self):
        """测试计算位数"""
        self.assertEqual(count_armstrong_digits(0), 1)
        self.assertEqual(count_armstrong_digits(9), 1)
        self.assertEqual(count_armstrong_digits(10), 2)
        self.assertEqual(count_armstrong_digits(153), 3)
        self.assertEqual(count_armstrong_digits(9474), 4)
        self.assertEqual(count_armstrong_digits(-123), 3)


class TestHappyNumber(unittest.TestCase):
    """快乐数测试"""
    
    def test_known_happy_numbers(self):
        """测试已知的快乐数"""
        happy_numbers = [1, 7, 10, 13, 19, 23, 28, 31, 32, 44, 49, 68, 70, 79, 82, 86, 91, 94, 97, 100]
        for num in happy_numbers[:10]:
            self.assertTrue(is_happy(num), f"{num} should be happy number")
    
    def test_unhappy_numbers(self):
        """测试不快乐的数"""
        unhappy = [2, 3, 4, 5, 6, 8, 9, 11, 12, 14]
        for num in unhappy:
            self.assertFalse(is_happy(num), f"{num} should not be happy number")
    
    def test_sum_of_squares_of_digits(self):
        """测试各位数字的平方和"""
        self.assertEqual(sum_of_squares_of_digits(19), 82)
        self.assertEqual(sum_of_squares_of_digits(100), 1)
        self.assertEqual(sum_of_squares_of_digits(0), 0)
        self.assertEqual(sum_of_squares_of_digits(123), 14)
    
    def test_get_happy_sequence(self):
        """测试快乐数变换序列"""
        self.assertEqual(get_happy_sequence(19), [19, 82, 68, 100, 1])
        self.assertEqual(get_happy_sequence(1), [1])
    
    def test_find_happy_numbers(self):
        """测试查找快乐数"""
        result = find_happy_numbers(20)
        expected = [1, 7, 10, 13, 19]
        self.assertEqual(result, expected)
    
    def test_non_positive_numbers(self):
        """测试非正整数"""
        self.assertFalse(is_happy(0))
        self.assertFalse(is_happy(-1))


class TestKaprekarNumber(unittest.TestCase):
    """卡普雷卡尔数测试"""
    
    def test_known_kaprekar_numbers(self):
        """测试已知的卡普雷卡尔数"""
        kaprekar_numbers = [1, 9, 45, 55, 99, 297, 703, 999, 2223, 2728, 4879, 4950]
        for num in kaprekar_numbers[:6]:
            self.assertTrue(is_kaprekar(num), f"{num} should be Kaprekar number")
    
    def test_non_kaprekar_numbers(self):
        """测试非卡普雷卡尔数"""
        non_kaprekar = [2, 3, 4, 5, 6, 7, 8, 10, 11, 12]
        for num in non_kaprekar:
            self.assertFalse(is_kaprekar(num), f"{num} should not be Kaprekar number")
    
    def test_find_kaprekar_numbers(self):
        """测试查找卡普雷卡尔数"""
        result = find_kaprekar_numbers(100)
        expected = [1, 9, 45, 55, 99]
        self.assertEqual(result, expected)
    
    def test_kaprekar_routine(self):
        """测试卡普雷卡尔程序（达到 6174）"""
        sequence, reached = kaprekar_routine(3524)
        self.assertTrue(reached)
        self.assertEqual(sequence[-1], 6174)
        self.assertIn(6174, sequence)
    
    def test_kaprekar_routine_same_digits(self):
        """测试所有数字相同的情况"""
        sequence, reached = kaprekar_routine(1111)
        self.assertFalse(reached)
        self.assertEqual(len(sequence), 1)
    
    def test_kaprekar_routine_not_4_digits(self):
        """测试非 4 位数"""
        sequence, reached = kaprekar_routine(123)
        self.assertFalse(reached)
        self.assertEqual(len(sequence), 1)


class TestPerfectNumber(unittest.TestCase):
    """完全数测试"""
    
    def test_known_perfect_numbers(self):
        """测试已知的完全数"""
        perfect_numbers = [6, 28, 496, 8128]
        for num in perfect_numbers:
            self.assertTrue(is_perfect(num), f"{num} should be perfect number")
    
    def test_non_perfect_numbers(self):
        """测试非完全数"""
        non_perfect = [1, 2, 3, 4, 5, 7, 8, 9, 10, 12]
        for num in non_perfect:
            self.assertFalse(is_perfect(num), f"{num} should not be perfect number")
    
    def test_get_proper_divisors(self):
        """测试获取真约数"""
        self.assertEqual(get_proper_divisors(6), [1, 2, 3])
        self.assertEqual(get_proper_divisors(28), [1, 2, 4, 7, 14])
        self.assertEqual(get_proper_divisors(1), [])
        self.assertEqual(get_proper_divisors(0), [])
    
    def test_find_perfect_numbers(self):
        """测试查找完全数"""
        result = find_perfect_numbers(10000)
        expected = [6, 28, 496, 8128]
        self.assertEqual(result, expected)
    
    def test_is_abundant(self):
        """测试盈数"""
        self.assertTrue(is_abundant(12))  # 1+2+3+4+6 = 16 > 12
        self.assertTrue(is_abundant(18))  # 1+2+3+6+9 = 21 > 18
        self.assertFalse(is_abundant(6))   # 完全数
        self.assertFalse(is_abundant(4))    # 亏数
    
    def test_is_deficient(self):
        """测试亏数"""
        self.assertTrue(is_deficient(8))   # 1+2+4 = 7 < 8
        self.assertTrue(is_deficient(1))    # 1 没有真约数（除了1本身）
        self.assertFalse(is_deficient(6))   # 完全数
        self.assertFalse(is_deficient(12))  # 盈数


class TestPalindromeNumber(unittest.TestCase):
    """回文数测试"""
    
    def test_known_palindromes(self):
        """测试已知的回文数"""
        palindromes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 121, 12321, 9999]
        for num in palindromes:
            self.assertTrue(is_palindrome(num), f"{num} should be palindrome")
    
    def test_non_palindromes(self):
        """测试非回文数"""
        non_palindromes = [10, 12, 13, 123, 1234]
        for num in non_palindromes:
            self.assertFalse(is_palindrome(num), f"{num} should not be palindrome")
    
    def test_negative_numbers_not_palindrome(self):
        """测试负数不是回文数"""
        self.assertFalse(is_palindrome(-121))
        self.assertFalse(is_palindrome(-1))
    
    def test_find_palindrome_numbers(self):
        """测试查找回文数"""
        result = find_palindrome_numbers(50)
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44]
        self.assertEqual(result, expected)
    
    def test_reverse_number(self):
        """测试数字反转"""
        self.assertEqual(reverse_number(123), 321)
        self.assertEqual(reverse_number(100), 1)
        self.assertEqual(reverse_number(0), 0)
        self.assertEqual(reverse_number(-123), -321)
    
    def test_is_lychrel(self):
        """测试 Lychrel 数"""
        self.assertTrue(is_lychrel(196))   # 已知的 Lychrel 数候选
        self.assertFalse(is_lychrel(47))   # 47 + 74 = 121
        self.assertFalse(is_lychrel(56))    # 56 + 65 = 121
    
    def test_get_lychrel_sequence(self):
        """测试 Lychrel 变换序列"""
        sequence, found = get_lychrel_sequence(47)
        self.assertTrue(found)
        self.assertEqual(sequence, [47, 121])


class TestHarshadNumber(unittest.TestCase):
    """Harshad 数测试"""
    
    def test_known_harshad_numbers(self):
        """测试已知的 Harshad 数"""
        harshad = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 18, 20, 21, 24, 27, 30]
        for num in harshad:
            self.assertTrue(is_harshad(num), f"{num} should be Harshad number")
    
    def test_non_harshad_numbers(self):
        """测试非 Harshad 数"""
        non_harshad = [11, 13, 14, 16, 19, 22, 25]
        for num in non_harshad:
            self.assertFalse(is_harshad(num), f"{num} should not be Harshad number")
    
    def test_find_harshad_numbers(self):
        """测试查找 Harshad 数"""
        result = find_harshad_numbers(25)
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 18, 20, 21, 24]
        self.assertEqual(result, expected)
    
    def test_non_positive_numbers(self):
        """测试非正整数"""
        self.assertFalse(is_harshad(0))
        self.assertFalse(is_harshad(-18))


class TestDigitalRoot(unittest.TestCase):
    """数字根测试"""
    
    def test_digital_root(self):
        """测试数字根计算"""
        self.assertEqual(digital_root(0), 0)
        self.assertEqual(digital_root(1), 1)
        self.assertEqual(digital_root(9), 9)
        self.assertEqual(digital_root(10), 1)
        self.assertEqual(digital_root(38), 2)      # 3 + 8 = 11, 1 + 1 = 2
        self.assertEqual(digital_root(12345), 6)  # 1+2+3+4+5 = 15, 1+5 = 6
        self.assertEqual(digital_root(999), 9)    # 9+9+9 = 27, 2+7 = 9
    
    def test_digital_root_large_numbers(self):
        """测试大数的数字根"""
        self.assertEqual(digital_root(999999999), 9)
        self.assertEqual(digital_root(123456789), 9)


class TestAnalyzeNumber(unittest.TestCase):
    """综合分析测试"""
    
    def test_analyze_153(self):
        """测试分析 153"""
        result = analyze_number(153)
        self.assertEqual(result['number'], 153)
        self.assertTrue(result['is_armstrong'])
        self.assertEqual(result['digits'], 3)
        self.assertEqual(result['digit_sum'], 9)
    
    def test_analyze_6(self):
        """测试分析 6（完全数）"""
        result = analyze_number(6)
        self.assertTrue(result['is_perfect'])
        self.assertFalse(result['is_abundant'])
        self.assertFalse(result['is_deficient'])
    
    def test_analyze_12(self):
        """测试分析 12（盈数）"""
        result = analyze_number(12)
        self.assertTrue(result['is_abundant'])
        self.assertFalse(result['is_perfect'])
        self.assertFalse(result['is_deficient'])


class TestFindSpecialNumbers(unittest.TestCase):
    """查找特殊数测试"""
    
    def test_find_armstrong_type(self):
        """测试查找阿姆斯特朗数"""
        result = find_special_numbers(500, 'armstrong')
        self.assertIn('armstrong', result)
        self.assertEqual(len(result), 1)
    
    def test_find_all_types(self):
        """测试查找所有类型"""
        result = find_special_numbers(100, 'all')
        self.assertIn('armstrong', result)
        self.assertIn('happy', result)
        self.assertIn('kaprekar', result)
        self.assertIn('perfect', result)
        self.assertIn('palindrome', result)
    
    def test_find_happy_type(self):
        """测试查找快乐数"""
        result = find_special_numbers(20, 'happy')
        self.assertEqual(result['happy'], [1, 7, 10, 13, 19])


class TestAliases(unittest.TestCase):
    """别名测试"""
    
    def test_narcissistic_alias(self):
        """测试自恋数别名"""
        self.assertEqual(is_narcissistic(153), is_armstrong(153))
        self.assertEqual(is_narcissistic(154), is_armstrong(154))
    
    def test_pluperfect_alias(self):
        """测试完全数字不变数别名"""
        self.assertEqual(is_pluperfect(370), is_armstrong(370))
        self.assertEqual(is_pluperfect(371), is_armstrong(371))


if __name__ == '__main__':
    unittest.main(verbosity=2)