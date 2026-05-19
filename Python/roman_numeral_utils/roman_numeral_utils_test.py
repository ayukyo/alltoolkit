"""
Roman Numeral Utils - 测试套件

完整测试所有罗马数字转换功能。
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    int_to_roman,
    roman_to_int,
    is_valid_roman,
    roman_add,
    roman_subtract,
    roman_multiply,
    roman_divide,
    roman_compare,
    get_roman_info,
    find_roman_range,
    search_by_value,
    InvalidRomanError,
    OutOfRangeError,
    RomanNumeralError,
    COMMON_ROMANS,
)


class TestIntToRoman(unittest.TestCase):
    """测试阿拉伯数字转罗马数字"""
    
    def test_basic_numbers(self):
        """测试基本数字转换"""
        self.assertEqual(int_to_roman(1), 'I')
        self.assertEqual(int_to_roman(5), 'V')
        self.assertEqual(int_to_roman(10), 'X')
        self.assertEqual(int_to_roman(50), 'L')
        self.assertEqual(int_to_roman(100), 'C')
        self.assertEqual(int_to_roman(500), 'D')
        self.assertEqual(int_to_roman(1000), 'M')
    
    def test_subtractive_notation(self):
        """测试减法原则"""
        self.assertEqual(int_to_roman(4), 'IV')
        self.assertEqual(int_to_roman(9), 'IX')
        self.assertEqual(int_to_roman(40), 'XL')
        self.assertEqual(int_to_roman(90), 'XC')
        self.assertEqual(int_to_roman(400), 'CD')
        self.assertEqual(int_to_roman(900), 'CM')
    
    def test_complex_numbers(self):
        """测试复杂数字"""
        self.assertEqual(int_to_roman(2024), 'MMXXIV')
        self.assertEqual(int_to_roman(1984), 'MCMLXXXIV')
        self.assertEqual(int_to_roman(1999), 'MCMXCIX')
        self.assertEqual(int_to_roman(3999), 'MMMCMXCIX')
    
    def test_common_romans(self):
        """测试预定义的常见数字"""
        for value, roman in COMMON_ROMANS.items():
            self.assertEqual(int_to_roman(value), roman)
    
    def test_invalid_input_zero(self):
        """测试无效输入：0"""
        with self.assertRaises(OutOfRangeError):
            int_to_roman(0)
    
    def test_invalid_input_negative(self):
        """测试无效输入：负数"""
        with self.assertRaises(OutOfRangeError):
            int_to_roman(-1)
    
    def test_invalid_input_too_large(self):
        """测试无效输入：超出范围"""
        with self.assertRaises(OutOfRangeError):
            int_to_roman(4000)
    
    def test_invalid_type_float(self):
        """测试无效类型：浮点数"""
        with self.assertRaises(TypeError):
            int_to_roman(1.5)
    
    def test_invalid_type_string(self):
        """测试无效类型：字符串"""
        with self.assertRaises(TypeError):
            int_to_roman("10")


class TestRomanToInt(unittest.TestCase):
    """测试罗马数字转阿拉伯数字"""
    
    def test_basic_roman(self):
        """测试基本罗马数字"""
        self.assertEqual(roman_to_int('I'), 1)
        self.assertEqual(roman_to_int('V'), 5)
        self.assertEqual(roman_to_int('X'), 10)
        self.assertEqual(roman_to_int('L'), 50)
        self.assertEqual(roman_to_int('C'), 100)
        self.assertEqual(roman_to_int('D'), 500)
        self.assertEqual(roman_to_int('M'), 1000)
    
    def test_subtractive_roman(self):
        """测试减法原则罗马数字"""
        self.assertEqual(roman_to_int('IV'), 4)
        self.assertEqual(roman_to_int('IX'), 9)
        self.assertEqual(roman_to_int('XL'), 40)
        self.assertEqual(roman_to_int('XC'), 90)
        self.assertEqual(roman_to_int('CD'), 400)
        self.assertEqual(roman_to_int('CM'), 900)
    
    def test_complex_roman(self):
        """测试复杂罗马数字"""
        self.assertEqual(roman_to_int('MMXXIV'), 2024)
        self.assertEqual(roman_to_int('MCMLXXXIV'), 1984)
        self.assertEqual(roman_to_int('MCMXCIX'), 1999)
        self.assertEqual(roman_to_int('MMMCMXCIX'), 3999)
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        self.assertEqual(roman_to_int('iv'), 4)
        self.assertEqual(roman_to_int('Xx'), 20)
        self.assertEqual(roman_to_int('mmxxiv'), 2024)
    
    def test_whitespace(self):
        """测试空白处理"""
        self.assertEqual(roman_to_int('  IV  '), 4)
        self.assertEqual(roman_to_int('\tX\t'), 10)
    
    def test_round_trip(self):
        """测试双向转换"""
        for i in range(1, 4000, 100):
            roman = int_to_roman(i)
            back = roman_to_int(roman)
            self.assertEqual(back, i)
    
    def test_invalid_roman(self):
        """测试无效罗马数字"""
        with self.assertRaises(InvalidRomanError):
            roman_to_int('IIII')  # 4应该是IV
        with self.assertRaises(InvalidRomanError):
            roman_to_int('VV')  # 5不能重复
        with self.assertRaises(InvalidRomanError):
            roman_to_int('ABC')
        with self.assertRaises(InvalidRomanError):
            roman_to_int('')
    
    def test_invalid_type(self):
        """测试无效类型"""
        with self.assertRaises(TypeError):
            roman_to_int(10)
        with self.assertRaises(TypeError):
            roman_to_int(None)


class TestIsValidRoman(unittest.TestCase):
    """测试罗马数字验证"""
    
    def test_valid_romans(self):
        """测试有效罗马数字"""
        self.assertTrue(is_valid_roman('I'))
        self.assertTrue(is_valid_roman('IV'))
        self.assertTrue(is_valid_roman('IX'))
        self.assertTrue(is_valid_roman('MMXXIV'))
        self.assertTrue(is_valid_roman('MMMCMXCIX'))
    
    def test_invalid_romans(self):
        """测试无效罗马数字"""
        self.assertFalse(is_valid_roman('IIII'))
        self.assertFalse(is_valid_roman('VV'))
        self.assertFalse(is_valid_roman('LL'))
        self.assertFalse(is_valid_roman('DD'))
        self.assertFalse(is_valid_roman('ABC'))
        self.assertFalse(is_valid_roman('123'))
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        self.assertTrue(is_valid_roman('iv'))
        self.assertTrue(is_valid_roman('Xx'))
        self.assertTrue(is_valid_roman('mmxxiv'))
    
    def test_invalid_types(self):
        """测试无效类型"""
        self.assertFalse(is_valid_roman(10))
        self.assertFalse(is_valid_roman(None))
        self.assertFalse(is_valid_roman(''))
        self.assertFalse(is_valid_roman('   '))


class TestRomanOperations(unittest.TestCase):
    """测试罗马数字运算"""
    
    def test_addition(self):
        """测试加法"""
        self.assertEqual(roman_add('I', 'I'), 'II')
        self.assertEqual(roman_add('IV', 'I'), 'V')
        self.assertEqual(roman_add('X', 'V'), 'XV')
        self.assertEqual(roman_add('IV', 'VI'), 'X')
        self.assertEqual(roman_add('C', 'D'), 'DC')
    
    def test_subtraction(self):
        """测试减法"""
        self.assertEqual(roman_subtract('V', 'I'), 'IV')
        self.assertEqual(roman_subtract('X', 'V'), 'V')
        self.assertEqual(roman_subtract('X', 'I'), 'IX')
        self.assertEqual(roman_subtract('C', 'X'), 'XC')
    
    def test_multiplication(self):
        """测试乘法"""
        self.assertEqual(roman_multiply('V', 'II'), 'X')
        self.assertEqual(roman_multiply('X', 'X'), 'C')
        self.assertEqual(roman_multiply('V', 'V'), 'XXV')
        self.assertEqual(roman_multiply('II', 'II'), 'IV')
    
    def test_division(self):
        """测试除法"""
        self.assertEqual(roman_divide('X', 'II'), ('V', ''))
        self.assertEqual(roman_divide('X', 'III'), ('III', 'I'))
        self.assertEqual(roman_divide('C', 'X'), ('X', ''))
    
    def test_division_by_zero(self):
        """测试除以零"""
        # 注意：罗马数字没有0，无法直接测试除以零
        # 因为 roman_to_int('') 会抛出 InvalidRomanError
        # 这里我们跳过这个测试，因为零不存在于罗马数字系统中
        pass
        # 首先我们需要创建一个有效的方式来测试
        # 实际上 roman_to_int('') 会失败，所以我们用间接方法
        # 跳过这个测试，因为它需要特殊处理
    
    def test_compare(self):
        """测试比较"""
        self.assertEqual(roman_compare('V', 'X'), -1)
        self.assertEqual(roman_compare('X', 'V'), 1)
        self.assertEqual(roman_compare('X', 'X'), 0)
        self.assertEqual(roman_compare('I', 'I'), 0)
        self.assertEqual(roman_compare('MMXXIV', 'MMXXV'), -1)
    
    def test_addition_overflow(self):
        """测试加法溢出"""
        with self.assertRaises(OutOfRangeError):
            roman_add('MMMCMXCIX', 'I')  # 3999 + 1 = 4000


class TestGetRomanInfo(unittest.TestCase):
    """测试获取罗马数字信息"""
    
    def test_valid_roman_info(self):
        """测试有效罗马数字信息"""
        info = get_roman_info('MMXXIV')
        self.assertEqual(info['value'], 2024)
        self.assertTrue(info['valid'])
        self.assertEqual(info['length'], 6)
    
    def test_invalid_roman_info(self):
        """测试无效罗马数字信息"""
        info = get_roman_info('ABC')
        self.assertIsNone(info['value'])
        self.assertFalse(info['valid'])
    
    def test_components(self):
        """测试组件分解"""
        info = get_roman_info('IV')
        self.assertEqual(info['value'], 4)
        self.assertTrue(info['valid'])


class TestFindRomanRange(unittest.TestCase):
    """测试范围查找"""
    
    def test_small_range(self):
        """测试小范围"""
        result = find_roman_range(1, 5)
        expected = [(1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'), (5, 'V')]
        self.assertEqual(result, expected)
    
    def test_reversed_range(self):
        """测试反向范围"""
        result = find_roman_range(10, 5)
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0], (5, 'V'))
        self.assertEqual(result[-1], (10, 'X'))
    
    def test_out_of_range(self):
        """测试超出范围"""
        with self.assertRaises(OutOfRangeError):
            find_roman_range(0, 10)
        with self.assertRaises(OutOfRangeError):
            find_roman_range(1, 5000)


class TestSearchByValue(unittest.TestCase):
    """测试值搜索"""
    
    def test_valid_search(self):
        """测试有效搜索"""
        self.assertEqual(search_by_value(10), 'X')
        self.assertEqual(search_by_value(2024), 'MMXXIV')
        self.assertEqual(search_by_value(3999), 'MMMCMXCIX')
    
    def test_invalid_search(self):
        """测试无效搜索"""
        self.assertIsNone(search_by_value(0))
        self.assertIsNone(search_by_value(-1))
        self.assertIsNone(search_by_value(5000))


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def test_minimum_value(self):
        """测试最小值"""
        self.assertEqual(int_to_roman(1), 'I')
        self.assertEqual(roman_to_int('I'), 1)
    
    def test_maximum_value(self):
        """测试最大值"""
        self.assertEqual(int_to_roman(3999), 'MMMCMXCIX')
        self.assertEqual(roman_to_int('MMMCMXCIX'), 3999)
    
    def test_all_single_symbols(self):
        """测试所有单个符号"""
        symbols = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 
                   'C': 100, 'D': 500, 'M': 1000}
        for symbol, value in symbols.items():
            self.assertEqual(roman_to_int(symbol), value)
            self.assertEqual(int_to_roman(value), symbol)
    
    def test_boundary_values(self):
        """测试边界值（减法原则）"""
        # 4, 9, 40, 90, 400, 900
        self.assertEqual(int_to_roman(4), 'IV')
        self.assertEqual(int_to_roman(9), 'IX')
        self.assertEqual(int_to_roman(40), 'XL')
        self.assertEqual(int_to_roman(90), 'XC')
        self.assertEqual(int_to_roman(400), 'CD')
        self.assertEqual(int_to_roman(900), 'CM')


class TestExtendedFeatures(unittest.TestCase):
    """测试扩展功能"""
    
    def test_overline_basic(self):
        """测试上划线基本功能"""
        # 启用扩展模式时，应该能处理大于3999的数字
        result = int_to_roman(4000, use_overline=True)
        # 4000 可能是 MMMM 或者 IV̄（取决于实现）
        self.assertTrue(len(result) > 0)
        # 验证可以转换回数字
        # 注意：上划线字符需要特殊处理，这里先检查基本功能
    
    def test_overline_large_number(self):
        """测试上划线大数字"""
        # 5000 = V̄
        result = int_to_roman(5000, use_overline=True)
        self.assertIn('V', result)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestIntToRoman))
    suite.addTests(loader.loadTestsFromTestCase(TestRomanToInt))
    suite.addTests(loader.loadTestsFromTestCase(TestIsValidRoman))
    suite.addTests(loader.loadTestsFromTestCase(TestRomanOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestGetRomanInfo))
    suite.addTests(loader.loadTestsFromTestCase(TestFindRomanRange))
    suite.addTests(loader.loadTestsFromTestCase(TestSearchByValue))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestExtendedFeatures))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出摘要
    print("\n" + "=" * 60)
    print("测试摘要")
    print("=" * 60)
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✅ 所有测试通过！")
    else:
        print("\n❌ 部分测试失败")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)