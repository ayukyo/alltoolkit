"""
罗马数字转换工具测试模块

测试所有核心功能：
- 阿拉伯数字转罗马数字
- 罗马数字转阿拉伯数字
- 格式验证
- 加减运算
- 边界情况处理
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    to_roman, to_arabic, is_valid_roman,
    add, subtract, compare, range_to_roman,
    list_operations, quick_convert, parse_mixed,
    find_largest_smaller, get_value, get_roman
)


class TestToRoman(unittest.TestCase):
    """测试阿拉伯数字转罗马数字"""
    
    def test_basic_numbers(self):
        """测试基本数字转换"""
        self.assertEqual(to_roman(1), 'I')
        self.assertEqual(to_roman(5), 'V')
        self.assertEqual(to_roman(10), 'X')
        self.assertEqual(to_roman(50), 'L')
        self.assertEqual(to_roman(100), 'C')
        self.assertEqual(to_roman(500), 'D')
        self.assertEqual(to_roman(1000), 'M')
    
    def test_subtractive_notation(self):
        """测试减法表示法"""
        self.assertEqual(to_roman(4), 'IV')
        self.assertEqual(to_roman(9), 'IX')
        self.assertEqual(to_roman(40), 'XL')
        self.assertEqual(to_roman(90), 'XC')
        self.assertEqual(to_roman(400), 'CD')
        self.assertEqual(to_roman(900), 'CM')
    
    def test_complex_numbers(self):
        """测试复杂数字转换"""
        self.assertEqual(to_roman(14), 'XIV')
        self.assertEqual(to_roman(49), 'XLIX')
        self.assertEqual(to_roman(99), 'XCIX')
        self.assertEqual(to_roman(444), 'CDXLIV')
        self.assertEqual(to_roman(999), 'CMXCIX')
        self.assertEqual(to_roman(2024), 'MMXXIV')
        self.assertEqual(to_roman(3999), 'MMMCMXCIX')
    
    def test_bounds(self):
        """测试边界值"""
        with self.assertRaises(ValueError):
            to_roman(0)
        with self.assertRaises(ValueError):
            to_roman(-1)
        with self.assertRaises(ValueError):
            to_roman(4000)
        with self.assertRaises(ValueError):
            to_roman(3.14)
    
    def test_type_check(self):
        """测试类型检查"""
        with self.assertRaises(ValueError):
            to_roman("10")
        with self.assertRaises(ValueError):
            to_roman(None)


class TestToArabic(unittest.TestCase):
    """测试罗马数字转阿拉伯数字"""
    
    def test_basic_symbols(self):
        """测试基本符号"""
        self.assertEqual(to_arabic('I'), 1)
        self.assertEqual(to_arabic('V'), 5)
        self.assertEqual(to_arabic('X'), 10)
        self.assertEqual(to_arabic('L'), 50)
        self.assertEqual(to_arabic('C'), 100)
        self.assertEqual(to_arabic('D'), 500)
        self.assertEqual(to_arabic('M'), 1000)
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        self.assertEqual(to_arabic('xvi'), 16)
        self.assertEqual(to_arabic('XVI'), 16)
        self.assertEqual(to_arabic('XvI'), 16)
    
    def test_subtractive_notation(self):
        """测试减法表示法"""
        self.assertEqual(to_arabic('IV'), 4)
        self.assertEqual(to_arabic('IX'), 9)
        self.assertEqual(to_arabic('XL'), 40)
        self.assertEqual(to_arabic('XC'), 90)
        self.assertEqual(to_arabic('CD'), 400)
        self.assertEqual(to_arabic('CM'), 900)
    
    def test_complex_numbers(self):
        """测试复杂罗马数字"""
        self.assertEqual(to_arabic('XIV'), 14)
        self.assertEqual(to_arabic('XLIX'), 49)
        self.assertEqual(to_arabic('XCIX'), 99)
        self.assertEqual(to_arabic('CDXLIV'), 444)
        self.assertEqual(to_arabic('CMXCIX'), 999)
        self.assertEqual(to_arabic('MMXXIV'), 2024)
        self.assertEqual(to_arabic('MMMCMXCIX'), 3999)
    
    def test_invalid_input(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            to_arabic('')
        with self.assertRaises(ValueError):
            to_arabic('IIII')
        with self.assertRaises(ValueError):
            to_arabic('VV')
        with self.assertRaises(ValueError):
            to_arabic('VX')
        with self.assertRaises(ValueError):
            to_arabic('IC')
        with self.assertRaises(ValueError):
            to_arabic('ABC')


class TestIsValidRoman(unittest.TestCase):
    """测试罗马数字验证"""
    
    def test_valid_romans(self):
        """测试有效的罗马数字"""
        self.assertTrue(is_valid_roman('I'))
        self.assertTrue(is_valid_roman('IV'))
        self.assertTrue(is_valid_roman('IX'))
        self.assertTrue(is_valid_roman('XIV'))
        self.assertTrue(is_valid_roman('MMMCMXCIX'))
        self.assertTrue(is_valid_roman('mmcmxcix'))  # 小写也有效
    
    def test_invalid_romans(self):
        """测试无效的罗马数字"""
        self.assertFalse(is_valid_roman(''))
        self.assertFalse(is_valid_roman('IIII'))
        self.assertFalse(is_valid_roman('VV'))
        self.assertFalse(is_valid_roman('LL'))
        self.assertFalse(is_valid_roman('DD'))
        self.assertFalse(is_valid_roman('VX'))
        self.assertFalse(is_valid_roman('LC'))
        self.assertFalse(is_valid_roman('DM'))
        self.assertFalse(is_valid_roman('IC'))
        self.assertFalse(is_valid_roman('IM'))
        self.assertFalse(is_valid_roman('ABC'))
        self.assertFalse(is_valid_roman('123'))
    
    def test_repeat_rules(self):
        """测试重复规则"""
        # I, X, C, M 可以重复最多 3 次
        self.assertTrue(is_valid_roman('III'))
        self.assertTrue(is_valid_roman('XXX'))
        self.assertTrue(is_valid_roman('CCC'))
        self.assertTrue(is_valid_roman('MMM'))
        self.assertFalse(is_valid_roman('IIII'))
        self.assertFalse(is_valid_roman('XXXX'))
        self.assertFalse(is_valid_roman('CCCC'))
        self.assertFalse(is_valid_roman('MMMM'))
        
        # V, L, D 不能重复
        self.assertFalse(is_valid_roman('VV'))
        self.assertFalse(is_valid_roman('LL'))
        self.assertFalse(is_valid_roman('DD'))


class TestArithmeticOperations(unittest.TestCase):
    """测试算术运算"""
    
    def test_addition(self):
        """测试加法"""
        self.assertEqual(add('I', 'I'), 'II')
        self.assertEqual(add('I', 'IV'), 'V')
        self.assertEqual(add('X', 'V'), 'XV')
        self.assertEqual(add('X', 'X'), 'XX')
        self.assertEqual(add('CM', 'C'), 'M')
    
    def test_subtraction(self):
        """测试减法"""
        self.assertEqual(subtract('II', 'I'), 'I')
        self.assertEqual(subtract('V', 'I'), 'IV')
        self.assertEqual(subtract('X', 'V'), 'V')
        self.assertEqual(subtract('X', 'I'), 'IX')
        self.assertEqual(subtract('M', 'C'), 'CM')
        
        # 相等结果应该报错
        with self.assertRaises(ValueError):
            subtract('X', 'X')
        
        # 结果为负应该报错
        with self.assertRaises(ValueError):
            subtract('I', 'X')
    
    def test_compare(self):
        """测试比较"""
        self.assertEqual(compare('X', 'V'), 1)
        self.assertEqual(compare('V', 'X'), -1)
        self.assertEqual(compare('X', 'X'), 0)
        self.assertEqual(compare('MMXXIV', 'MMXXIII'), 1)


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_range_to_roman(self):
        """测试范围生成"""
        result = range_to_roman(1, 5)
        self.assertEqual(result, ['I', 'II', 'III', 'IV', 'V'])
        
        result = range_to_roman(10, 12)
        self.assertEqual(result, ['X', 'XI', 'XII'])
    
    def test_find_largest_smaller(self):
        """测试查找最大较小值"""
        result = find_largest_smaller('X', ['V', 'VII', 'XV', 'III'])
        self.assertEqual(result, 'VII')
        
        result = find_largest_smaller('I', ['V', 'X'])
        self.assertIsNone(result)
    
    def test_list_operations(self):
        """测试综合运算"""
        result = list_operations('X', 'V')
        self.assertEqual(result['add'], 'XV')
        self.assertEqual(result['subtract'], 'V')
        self.assertEqual(result['compare'], 1)
        self.assertEqual(result['sum_arabic'], 15)
        self.assertEqual(result['diff_arabic'], 5)
    
    def test_quick_convert(self):
        """测试快速转换"""
        self.assertEqual(quick_convert(10), 'X')
        self.assertEqual(quick_convert(11), 'XI')  # 不在预定义中，使用标准转换
        self.assertEqual(quick_convert(100), 'C')
    
    def test_parse_mixed(self):
        """测试混合文本解析"""
        result = parse_mixed('Chapter XII and Section IV')
        self.assertEqual(result, [('XII', 12), ('IV', 4)])
        
        result = parse_mixed('In year MMXXIV')
        self.assertEqual(result, [('MMXXIV', 2024)])
        
        result = parse_mixed('No roman numerals here')
        self.assertEqual(result, [])
    
    def test_aliases(self):
        """测试别名函数"""
        self.assertEqual(get_value('X'), 10)
        self.assertEqual(get_roman(10), 'X')


class TestRoundTrip(unittest.TestCase):
    """测试往返转换（阿拉伯 -> 罗马 -> 阿拉伯）"""
    
    def test_round_trip_all(self):
        """测试所有数字的往返转换"""
        for num in range(1, 4000):
            roman = to_roman(num)
            arabic = to_arabic(roman)
            self.assertEqual(arabic, num, 
                f"Round trip failed for {num}: got {roman} -> {arabic}")


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)