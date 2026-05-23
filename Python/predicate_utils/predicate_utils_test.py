# -*- coding: utf-8 -*-
"""
Predicate Utilities 测试模块

Author: AllToolkit
"""

import unittest
import sys
import math

sys.path.insert(0, '/home/admin/.openclaw/workspace/AllToolkit/Python')

from predicate_utils.mod import (
    # 核心类
    Predicate,
    
    # 复合谓词
    AndPredicate, OrPredicate, NotPredicate, XorPredicate,
    NandPredicate, NorPredicate, ImplicationPredicate,
    ExactlyPredicate, AtLeastPredicate, AtMostPredicate,
    
    # 比较谓词
    EqualsPredicate, NotEqualsPredicate, LessThanPredicate,
    LessThanOrEqualPredicate, GreaterThanPredicate,
    GreaterThanOrEqualPredicate, BetweenPredicate, InPredicate,
    
    # 类型谓词
    IsNonePredicate, IsNotNonePredicate, IsInstancePredicate,
    
    # 字符串谓词
    StartsWithPredicate, EndsWithPredicate, ContainsPredicate,
    MatchesPredicate, LengthPredicate, IsEmptyPredicate,
    
    # 数值谓词
    IsPositivePredicate, IsNegativePredicate, IsZeroPredicate,
    IsEvenPredicate, IsOddPredicate, DivisibleByPredicate,
    
    # 集合谓词
    ContainsAllPredicate, ContainsAnyPredicate, HasSizePredicate,
    
    # 字典谓词
    HasKeyPredicate, KeyValuePredicate,
    
    # 属性/项谓词
    AttrPredicate, ItemPredicate,
    
    # 函数谓词
    FunctionPredicate,
    
    # 常用谓词实例
    is_none, is_not_none, is_empty, is_not_empty,
    is_positive, is_negative, is_zero, is_even, is_odd,
    
    # 构建器函数
    eq, ne, lt, le, gt, ge, between, in_, not_in,
    isinstance_of, starts_with, ends_with, contains, matches,
    length, divisible_by, contains_all, contains_any, has_size,
    has_key, key_value, attr, item, predicate,
    all_of, any_of, none_of, exactly, at_least, at_most,
    implies,
)


class TestEqualsPredicate(unittest.TestCase):
    """测试等于谓词"""
    
    def test_basic(self):
        p = eq(5)
        self.assertTrue(p(5))
        self.assertFalse(p(3))
        self.assertFalse(p(None))
    
    def test_string(self):
        p = eq("hello")
        self.assertTrue(p("hello"))
        self.assertFalse(p("Hello"))
        self.assertFalse(p("world"))
    
    def test_none(self):
        p = eq(None)
        self.assertTrue(p(None))
        self.assertFalse(p(0))
        self.assertFalse(p(""))


class TestComparisonPredicates(unittest.TestCase):
    """测试比较谓词"""
    
    def test_less_than(self):
        p = lt(10)
        self.assertTrue(p(5))
        self.assertTrue(p(9))
        self.assertFalse(p(10))
        self.assertFalse(p(15))
    
    def test_less_than_or_equal(self):
        p = le(10)
        self.assertTrue(p(5))
        self.assertTrue(p(10))
        self.assertFalse(p(15))
    
    def test_greater_than(self):
        p = gt(10)
        self.assertFalse(p(5))
        self.assertFalse(p(10))
        self.assertTrue(p(15))
    
    def test_greater_than_or_equal(self):
        p = ge(10)
        self.assertFalse(p(5))
        self.assertTrue(p(10))
        self.assertTrue(p(15))
    
    def test_between(self):
        p = between(1, 10)
        self.assertFalse(p(0))
        self.assertTrue(p(1))
        self.assertTrue(p(5))
        self.assertTrue(p(10))
        self.assertFalse(p(11))
    
    def test_between_exclusive(self):
        p = between(1, 10, inclusive=False)
        self.assertFalse(p(1))
        self.assertTrue(p(5))
        self.assertFalse(p(10))


class TestInPredicate(unittest.TestCase):
    """测试包含于谓词"""
    
    def test_in_list(self):
        p = in_([1, 2, 3, 4, 5])
        self.assertTrue(p(3))
        self.assertFalse(p(6))
    
    def test_in_set(self):
        p = in_({'a', 'b', 'c'})
        self.assertTrue(p('a'))
        self.assertFalse(p('d'))
    
    def test_not_in(self):
        p = not_in([1, 2, 3])
        self.assertFalse(p(2))
        self.assertTrue(p(4))


class TestLogicalPredicates(unittest.TestCase):
    """测试逻辑组合谓词"""
    
    def test_and(self):
        p = gt(5) & lt(10)
        self.assertFalse(p(3))
        self.assertTrue(p(7))
        self.assertFalse(p(15))
    
    def test_or(self):
        p = lt(0) | gt(10)
        self.assertTrue(p(-5))
        self.assertFalse(p(5))
        self.assertTrue(p(15))
    
    def test_not(self):
        p = ~eq(5)
        self.assertFalse(p(5))
        self.assertTrue(p(3))
        self.assertTrue(p(10))
    
    def test_xor(self):
        p = is_even ^ is_positive
        # 奇数正数: True (False XOR True)
        # 奇数负数: False (False XOR False)
        # 偶数正数: False (True XOR True)
        # 偶数负数: True (True XOR False)
        self.assertTrue(p(1))  # 奇数正数
        self.assertFalse(p(2))  # 偶数正数
        self.assertTrue(p(-2))  # 偶数负数
        self.assertFalse(p(-1))  # 奇数负数
    
    def test_all_of(self):
        p = all_of(is_positive, is_even, divisible_by(4))
        self.assertTrue(p(8))
        self.assertTrue(p(12))
        self.assertFalse(p(6))  # 不被4整除
        self.assertFalse(p(-4))  # 不是正数
    
    def test_any_of(self):
        p = any_of(eq('a'), eq('b'), eq('c'))
        self.assertTrue(p('a'))
        self.assertTrue(p('b'))
        self.assertFalse(p('d'))
    
    def test_none_of(self):
        p = none_of(eq(1), eq(2), eq(3))
        self.assertTrue(p(4))
        self.assertFalse(p(2))
    
    def test_exactly(self):
        p = exactly(2, gt(0), gt(5), gt(10))
        # gt(0): True, gt(5): True, gt(10): False => 2 True => True
        self.assertTrue(p(8))
        self.assertFalse(p(15))  # 3 True
        self.assertFalse(p(3))  # 1 True
    
    def test_at_least(self):
        p = at_least(2, gt(0), gt(5), gt(10))
        self.assertTrue(p(8))  # 2 True
        self.assertTrue(p(15))  # 3 True
        self.assertFalse(p(3))  # 1 True
    
    def test_at_most(self):
        p = at_most(2, gt(0), gt(5), gt(10))
        self.assertTrue(p(8))  # 2 True
        self.assertFalse(p(15))  # 3 True
        self.assertTrue(p(3))  # 1 True
    
    def test_implies(self):
        # "如果是偶数，则能被4整除"
        p = implies(is_even, divisible_by(4))
        self.assertTrue(p(4))  # 偶数且被4整除
        self.assertTrue(p(8))  # 偶数且被4整除
        self.assertFalse(p(6))  # 偶数但不被4整除
        self.assertTrue(p(3))  # 不是偶数，蕴涵自动成立
    
    def test_chained_and(self):
        p = gt(0).and_(is_even).and_(lt(100))
        self.assertTrue(p(50))
        self.assertFalse(p(101))
        self.assertFalse(p(3))
    
    def test_chained_or(self):
        p = lt(0).or_(gt(100))
        self.assertTrue(p(-5))
        self.assertTrue(p(150))
        self.assertFalse(p(50))


class TestTypePredicates(unittest.TestCase):
    """测试类型谓词"""
    
    def test_is_none(self):
        self.assertTrue(is_none(None))
        self.assertFalse(is_none(0))
        self.assertFalse(is_none(""))
    
    def test_is_not_none(self):
        self.assertFalse(is_not_none(None))
        self.assertTrue(is_not_none(0))
        self.assertTrue(is_not_none(""))
    
    def test_isinstance(self):
        p = isinstance_of(int)
        self.assertTrue(p(5))
        self.assertFalse(p("5"))
        self.assertFalse(p(5.0))
    
    def test_isinstance_multiple(self):
        p = isinstance_of((int, float))
        self.assertTrue(p(5))
        self.assertTrue(p(5.0))
        self.assertFalse(p("5"))


class TestStringPredicates(unittest.TestCase):
    """测试字符串谓词"""
    
    def test_starts_with(self):
        p = starts_with("Hello")
        self.assertTrue(p("Hello World"))
        self.assertFalse(p("World Hello"))
    
    def test_starts_with_case_insensitive(self):
        p = starts_with("hello", case_sensitive=False)
        self.assertTrue(p("Hello World"))
        self.assertTrue(p("HELLO world"))
    
    def test_ends_with(self):
        p = ends_with(".txt")
        self.assertTrue(p("file.txt"))
        self.assertFalse(p("file.csv"))
    
    def test_contains(self):
        p = contains("Python")
        self.assertTrue(p("I love Python"))
        self.assertFalse(p("I love Java"))
    
    def test_matches(self):
        p = matches(r'^\d{3}-\d{4}$')
        self.assertTrue(p("123-4567"))
        self.assertFalse(p("1234567"))
        self.assertFalse(p("abc-defg"))
    
    def test_length(self):
        p = length(min_len=3, max_len=10)
        self.assertFalse(p("ab"))
        self.assertTrue(p("abc"))
        self.assertTrue(p("abcdefghij"))
        self.assertFalse(p("abcdefghijk"))
    
    def test_length_min_only(self):
        p = length(min_len=5)
        self.assertFalse(p("abc"))
        self.assertTrue(p("abcdef"))
    
    def test_length_max_only(self):
        p = length(max_len=5)
        self.assertTrue(p("abc"))
        self.assertFalse(p("abcdef"))
    
    def test_is_empty(self):
        self.assertTrue(is_empty(""))
        self.assertTrue(is_empty([]))
        self.assertTrue(is_empty({}))
        self.assertTrue(is_empty(None))
        self.assertFalse(is_empty("a"))
        self.assertFalse(is_empty([1]))
    
    def test_is_not_empty(self):
        self.assertFalse(is_not_empty(""))
        self.assertTrue(is_not_empty("a"))
        self.assertTrue(is_not_empty([1]))


class TestNumberPredicates(unittest.TestCase):
    """测试数值谓词"""
    
    def test_is_positive(self):
        self.assertTrue(is_positive(5))
        self.assertFalse(is_positive(0))
        self.assertFalse(is_positive(-5))
    
    def test_is_negative(self):
        self.assertFalse(is_negative(5))
        self.assertFalse(is_negative(0))
        self.assertTrue(is_negative(-5))
    
    def test_is_zero(self):
        self.assertFalse(is_zero(5))
        self.assertTrue(is_zero(0))
        self.assertFalse(is_zero(-5))
    
    def test_is_even(self):
        self.assertTrue(is_even(4))
        self.assertFalse(is_even(3))
        self.assertTrue(is_even(0))
        self.assertTrue(is_even(-4))
    
    def test_is_odd(self):
        self.assertFalse(is_odd(4))
        self.assertTrue(is_odd(3))
        self.assertFalse(is_odd(0))
        self.assertTrue(is_odd(-3))
    
    def test_divisible_by(self):
        p = divisible_by(3)
        self.assertTrue(p(9))
        self.assertTrue(p(12))
        self.assertFalse(p(10))
    
    def test_divisible_by_zero(self):
        with self.assertRaises(ValueError):
            divisible_by(0)


class TestCollectionPredicates(unittest.TestCase):
    """测试集合谓词"""
    
    def test_contains_all(self):
        p = contains_all([1, 2])
        self.assertTrue(p([1, 2, 3]))
        self.assertFalse(p([1, 3]))
    
    def test_contains_any(self):
        p = contains_any([1, 2])
        self.assertTrue(p([1, 3]))
        self.assertTrue(p([2, 3]))
        self.assertFalse(p([3, 4]))
    
    def test_has_size(self):
        p = has_size(3)
        self.assertTrue(p([1, 2, 3]))
        self.assertFalse(p([1, 2]))
        self.assertTrue(p("abc"))


class TestDictPredicates(unittest.TestCase):
    """测试字典谓词"""
    
    def test_has_key(self):
        p = has_key('name')
        self.assertTrue(p({'name': 'John'}))
        self.assertFalse(p({'age': 25}))
    
    def test_key_value(self):
        p = key_value('age', gt(18))
        self.assertTrue(p({'age': 25}))
        self.assertFalse(p({'age': 15}))
        self.assertFalse(p({'name': 'John'}))


class TestAttrPredicate(unittest.TestCase):
    """测试属性谓词"""
    
    def test_attr(self):
        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age
        
        p = attr('age', gt(18))
        self.assertTrue(p(Person('John', 25)))
        self.assertFalse(p(Person('Jane', 15)))


class TestItemPredicate(unittest.TestCase):
    """测试项谓词"""
    
    def test_item_dict(self):
        p = item('score', ge(60))
        self.assertTrue(p({'score': 80}))
        self.assertFalse(p({'score': 50}))
    
    def test_item_list(self):
        p = item(0, eq('first'))
        self.assertTrue(p(['first', 'second']))
        self.assertFalse(p(['second', 'first']))


class TestFunctionPredicate(unittest.TestCase):
    """测试函数包装谓词"""
    
    def test_lambda(self):
        p = predicate(lambda x: x % 7 == 0)
        self.assertTrue(p(7))
        self.assertTrue(p(14))
        self.assertFalse(p(8))
    
    def test_named_function(self):
        def is_palindrome(s):
            return s == s[::-1]
        
        p = predicate(is_palindrome)
        self.assertTrue(p("radar"))
        self.assertTrue(p("level"))
        self.assertFalse(p("hello"))


class TestPredicateMethods(unittest.TestCase):
    """测试谓词的辅助方法"""
    
    def test_filter(self):
        p = is_even
        result = p.filter([1, 2, 3, 4, 5, 6])
        self.assertEqual(result, [2, 4, 6])
    
    def test_any(self):
        p = gt(10)
        self.assertTrue(p.any([5, 15, 8]))
        self.assertFalse(p.any([5, 8, 9]))
    
    def test_all(self):
        p = gt(0)
        self.assertTrue(p.all([1, 2, 3]))
        self.assertFalse(p.all([1, -1, 2]))
    
    def test_count(self):
        p = is_positive
        self.assertEqual(p.count([-1, 0, 1, 2, -3]), 2)
    
    def test_first(self):
        p = gt(5)
        self.assertEqual(p.first([1, 3, 7, 9, 2]), 7)
        self.assertIsNone(p.first([1, 2, 3]))
    
    def test_first_with_default(self):
        p = gt(100)
        self.assertEqual(p.first([1, 2, 3], default=0), 0)
    
    def test_reject(self):
        p = is_even
        result = p.reject([1, 2, 3, 4, 5, 6])
        self.assertEqual(result, [1, 3, 5])


class TestComplexPredicates(unittest.TestCase):
    """测试复杂组合谓词"""
    
    def test_email_validation(self):
        # 简化的邮箱验证
        p = all_of(
            contains('@'),
            contains('.', case_sensitive=True),
            length(min_len=5, max_len=100),
            starts_with('@', case_sensitive=False).__invert__(),  # 不以@开头
            ends_with('.', case_sensitive=False).__invert__(),  # 不以.结尾
            matches(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0.9.-]+\.[a-zA-Z]{2,}$')
        )
        self.assertTrue(p("test@example.com"))
        self.assertFalse(p("invalid"))
        self.assertFalse(p("@example.com"))
        self.assertFalse(p("test@"))
    
    def test_password_validation(self):
        # 密码验证：长度>=8，包含字母和数字
        p = all_of(
            length(min_len=8),
            matches(r'[A-Za-z]'),
            matches(r'[0-9]')
        )
        self.assertTrue(p("password123"))
        self.assertFalse(p("short"))
        self.assertFalse(p("nodigits"))
    
    def test_range_check(self):
        # 检查温度是否在合理范围内
        p = between(-50, 50)
        values = [-60, -20, 0, 25, 60]
        filtered = p.filter(values)
        self.assertEqual(filtered, [-20, 0, 25])
    
    def test_multi_condition(self):
        # 筛选有效用户数据
        user_data = [
            {'name': 'John', 'age': 25, 'active': True},
            {'name': '', 'age': 30, 'active': True},
            {'name': 'Jane', 'age': 15, 'active': False},
            {'name': 'Bob', 'age': 40, 'active': True},
        ]
        
        p = all_of(
            key_value('name', length(min_len=1)),
            key_value('age', ge(18)),
            key_value('active', eq(True))
        )
        
        valid_users = p.filter(user_data)
        self.assertEqual(len(valid_users), 2)
        self.assertEqual(valid_users[0]['name'], 'John')
        self.assertEqual(valid_users[1]['name'], 'Bob')


class TestPredicateRepr(unittest.TestCase):
    """测试谓词的字符串表示"""
    
    def test_eq_repr(self):
        p = eq(5)
        self.assertIn('5', repr(p))
    
    def test_gt_repr(self):
        p = gt(10)
        self.assertIn('10', repr(p))
    
    def test_and_repr(self):
        p = gt(5) & lt(10)
        self.assertIn('AND', repr(p))
    
    def test_or_repr(self):
        p = lt(0) | gt(100)
        self.assertIn('OR', repr(p))
    
    def test_not_repr(self):
        p = ~eq(5)
        self.assertIn('NOT', repr(p))


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def test_empty_list_filter(self):
        p = gt(0)
        self.assertEqual(p.filter([]), [])
    
    def test_none_handling(self):
        p = is_not_none
        values = [None, 1, None, 2, None]
        filtered = p.filter(values)
        self.assertEqual(filtered, [1, 2])
    
    def test_nested_logical(self):
        p = (gt(0) & lt(10)) | (gt(100) & lt(200))
        self.assertTrue(p(5))
        self.assertTrue(p(150))
        self.assertFalse(p(50))
        self.assertFalse(p(250))
    
    def test_type_mismatch(self):
        # 比较谓词对不同类型的处理
        p = lt(10)
        # Python 允许不同类型比较，但结果可能不一致
        # 这里只测试基本行为
        self.assertTrue(p(5))


if __name__ == '__main__':
    unittest.main(verbosity=2)