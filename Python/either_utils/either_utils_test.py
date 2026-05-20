# -*- coding: utf-8 -*-
"""
AllToolkit - Either Utils 测试模块

完整的单元测试，覆盖所有核心功能。
"""

import unittest
from typing import List, Optional
from mod import (
    Either, Left, Right, left, right,
    from_optional, from_exception, try_catch,
    sequence, sequence_first_error, traverse, partition_eithers,
    cond_either, bimap, ensure, ensure_pred,
    EitherChain, chain, chain_error,
    all_rights, all_lefts, is_left, is_right, get_or_else
)


class TestEitherBasics(unittest.TestCase):
    """测试 Either 基础功能"""
    
    def test_left_creation(self):
        """测试 Left 创建"""
        e = Left("error")
        self.assertTrue(e.is_left())
        self.assertFalse(e.is_right())
        self.assertEqual(str(e), "Left('error')")
    
    def test_right_creation(self):
        """测试 Right 创建"""
        e = Right(42)
        self.assertTrue(e.is_right())
        self.assertFalse(e.is_left())
        self.assertEqual(str(e), "Right(42)")
    
    def test_left_value(self):
        """测试 Left 获取值"""
        e: Either[str, int] = Left("error")
        self.assertEqual(e.left()._value, "error")
        self.assertIsNone(e.right())
    
    def test_right_value(self):
        """测试 Right 获取值"""
        e: Either[str, int] = Right(42)
        self.assertEqual(e.right()._value, 42)
        self.assertIsNone(e.left())
    
    def test_bool_conversion(self):
        """测试布尔转换"""
        self.assertFalse(Left("error"))
        self.assertTrue(Right(42))
    
    def test_equality(self):
        """测试相等性"""
        self.assertEqual(Left("a"), Left("a"))
        self.assertNotEqual(Left("a"), Left("b"))
        self.assertEqual(Right(1), Right(1))
        self.assertNotEqual(Right(1), Right(2))
        self.assertNotEqual(Left("a"), Right(1))
    
    def test_hash(self):
        """测试哈希"""
        e1 = Left("a")
        e2 = Left("a")
        self.assertEqual(hash(e1), hash(e2))
        
        r1 = Right(1)
        r2 = Right(1)
        self.assertEqual(hash(r1), hash(r2))
        
        # 可以放入集合
        s = {Left("a"), Right(1), Left("a")}
        self.assertEqual(len(s), 2)
    
    def test_immutability(self):
        """测试不可变性"""
        e1 = Right(5)
        e2 = e1.map(lambda x: x * 2)
        # 原值不变
        self.assertEqual(e1._value, 5)
        self.assertEqual(e2._value, 10)


class TestEitherMap(unittest.TestCase):
    """测试 Either 映射功能"""
    
    def test_map_on_right(self):
        """测试 map 在 Right 上"""
        e = Right(5).map(lambda x: x * 2)
        self.assertTrue(e.is_right())
        self.assertEqual(e._value, 10)
    
    def test_map_on_left(self):
        """测试 map 在 Left 上"""
        e: Either[str, int] = Left("error").map(lambda x: x * 2)
        self.assertTrue(e.is_left())
        self.assertEqual(e._value, "error")
    
    def test_map_left_on_left(self):
        """测试 map_left 在 Left 上"""
        e = Left(5).map_left(lambda x: x * 2)
        self.assertTrue(e.is_left())
        self.assertEqual(e._value, 10)
    
    def test_map_left_on_right(self):
        """测试 map_left 在 Right 上"""
        e: Either[int, str] = Right("success").map_left(lambda x: x * 2)
        self.assertTrue(e.is_right())
        self.assertEqual(e._value, "success")
    
    def test_flat_map_on_right(self):
        """测试 flat_map 在 Right 上"""
        def safe_divide(n: int) -> Either[str, float]:
            return Right(10 / n) if n != 0 else Left("Division by zero")
        
        e1 = Right(2).flat_map(safe_divide)
        self.assertEqual(e1._value, 5.0)
        
        e2: Either[str, float] = Right(0).flat_map(safe_divide)
        self.assertTrue(e2.is_left())
        self.assertEqual(e2._value, "Division by zero")
    
    def test_flat_map_on_left(self):
        """测试 flat_map 在 Left 上"""
        def safe_divide(n: int) -> Either[str, float]:
            return Right(10 / n)
        
        e: Either[str, float] = Left("error").flat_map(safe_divide)
        self.assertTrue(e.is_left())
        self.assertEqual(e._value, "error")
    
    def test_flatten(self):
        """测试 flatten"""
        nested_right: Either[str, Either[str, int]] = Right(Right(5))
        e = nested_right.flatten()
        self.assertEqual(e._value, 5)
        
        nested_left: Either[str, Either[str, int]] = Right(Left("inner error"))
        e2 = nested_left.flatten()
        self.assertTrue(e2.is_left())


class TestEitherGet(unittest.TestCase):
    """测试 Either 获取值功能"""
    
    def test_get_or_else_right(self):
        """测试 get_or_else 在 Right 上"""
        self.assertEqual(Right(5).get_or_else(0), 5)
    
    def test_get_or_else_left(self):
        """测试 get_or_else 在 Left 上"""
        self.assertEqual(Left("error").get_or_else(0), 0)
    
    def test_get_or_else_with_function(self):
        """测试 get_or_else 使用函数"""
        self.assertEqual(Left("error").get_or_else(lambda: len("error")), 5)
    
    def test_get_or_raise_right(self):
        """测试 get_or_raise 在 Right 上"""
        self.assertEqual(Right(5).get_or_raise(), 5)
    
    def test_get_or_raise_left(self):
        """测试 get_or_raise 在 Left 上"""
        with self.assertRaises(ValueError):
            Left("error").get_or_raise()
    
    def test_get_or_raise_with_exception(self):
        """测试 get_or_raise 使用异常"""
        exc = ValueError("custom error")
        with self.assertRaises(ValueError) as cm:
            Left(exc).get_or_raise()
        self.assertEqual(str(cm.exception), "custom error")


class TestEitherOperations(unittest.TestCase):
    """测试 Either 其他操作"""
    
    def test_or_else(self):
        """测试 or_else"""
        e1 = Right(5).or_else(Right(10))
        self.assertEqual(e1._value, 5)
        
        e2: Either[str, int] = Left("error").or_else(Right(10))
        self.assertTrue(e2.is_right())
        self.assertEqual(e2._value, 10)
    
    def test_swap(self):
        """测试 swap"""
        r = Right(5).swap()
        self.assertTrue(r.is_left())
        self.assertEqual(r._value, 5)
        
        l = Left("error").swap()
        self.assertTrue(l.is_right())
        self.assertEqual(l._value, "error")
    
    def test_fold(self):
        """测试 fold"""
        e = Right(5).fold(
            lambda e: f"Error: {e}",
            lambda v: f"Value: {v}"
        )
        self.assertEqual(e, "Value: 5")
        
        e2 = Left("oops").fold(
            lambda e: f"Error: {e}",
            lambda v: f"Value: {v}"
        )
        self.assertEqual(e2, "Error: oops")
    
    def test_filter(self):
        """测试 filter"""
        e1 = Right(5).filter(lambda x: x > 3, "Too small")
        self.assertTrue(e1.is_right())
        
        e2: Either[str, int] = Right(2).filter(lambda x: x > 3, "Too small")
        self.assertTrue(e2.is_left())
        self.assertEqual(e2._value, "Too small")
        
        e3: Either[str, int] = Right(2).filter(lambda x: x > 3, lambda v: f"Got {v}")
        self.assertEqual(e3._value, "Got 2")
    
    def test_exists(self):
        """测试 exists"""
        self.assertTrue(Right(5).exists(lambda x: x > 3))
        self.assertFalse(Right(2).exists(lambda x: x > 3))
        self.assertFalse(Left("error").exists(lambda x: True))
    
    def test_for_all(self):
        """测试 for_all"""
        self.assertTrue(Right(5).for_all(lambda x: x > 3))
        self.assertFalse(Right(2).for_all(lambda x: x > 3))
        self.assertTrue(Left("error").for_all(lambda x: False))
    
    def test_to_optional(self):
        """测试 to_optional"""
        self.assertEqual(Right(5).to_optional(), 5)
        self.assertIsNone(Left("error").to_optional())
    
    def test_to_list(self):
        """测试 to_list"""
        self.assertEqual(Right(5).to_list(), [5])
        self.assertEqual(Left("error").to_list(), [])
    
    def test_iteration(self):
        """测试迭代"""
        self.assertEqual(list(Right(5)), [5])
        self.assertEqual(list(Left("error")), [])


class TestHelperFunctions(unittest.TestCase):
    """测试辅助函数"""
    
    def test_left_function(self):
        """测试 left 函数"""
        e = left("error")
        self.assertTrue(e.is_left())
    
    def test_right_function(self):
        """测试 right 函数"""
        e = right(42)
        self.assertTrue(e.is_right())
    
    def test_from_optional(self):
        """测试 from_optional"""
        e1 = from_optional(5, "Not found")
        self.assertTrue(e1.is_right())
        
        e2 = from_optional(None, "Not found")
        self.assertTrue(e2.is_left())
    
    def test_from_exception(self):
        """测试 from_exception"""
        e1 = from_exception(lambda: int("42"))
        self.assertTrue(e1.is_right())
        self.assertEqual(e1._value, 42)
        
        e2 = from_exception(lambda: int("abc"))
        self.assertTrue(e2.is_left())
        self.assertIsInstance(e2._value, ValueError)
        
        e3 = from_exception(lambda: int("abc"), str)
        self.assertTrue(e3.is_left())
        self.assertIsInstance(e3._value, str)
    
    def test_try_catch(self):
        """测试 try_catch 装饰器"""
        @try_catch
        def safe_divide(a: int, b: int) -> float:
            return a / b
        
        e1 = safe_divide(10, 2)
        self.assertTrue(e1.is_right())
        self.assertEqual(e1._value, 5.0)
        
        e2 = safe_divide(10, 0)
        self.assertTrue(e2.is_left())
        self.assertIsInstance(e2._value, ZeroDivisionError)


class TestSequence(unittest.TestCase):
    """测试序列操作"""
    
    def test_sequence_all_rights(self):
        """测试 sequence 全 Right"""
        eithers = [Right(1), Right(2), Right(3)]
        result = sequence(eithers)
        self.assertTrue(result.is_right())
        self.assertEqual(result._value, [1, 2, 3])
    
    def test_sequence_with_lefts(self):
        """测试 sequence 有 Left"""
        eithers: List[Either[str, int]] = [Right(1), Left("a"), Left("b")]
        result = sequence(eithers)
        self.assertTrue(result.is_left())
        self.assertEqual(result._value, ["a", "b"])
    
    def test_sequence_first_error(self):
        """测试 sequence_first_error"""
        eithers: List[Either[str, int]] = [Right(1), Left("a"), Right(3)]
        result = sequence_first_error(eithers)
        self.assertTrue(result.is_left())
        self.assertEqual(result._value, "a")
    
    def test_traverse(self):
        """测试 traverse"""
        def safe_int(s: str) -> Either[str, int]:
            try:
                return Right(int(s))
            except ValueError:
                return Left(f"Invalid: {s}")
        
        result1 = traverse(safe_int, ["1", "2", "3"])
        self.assertTrue(result1.is_right())
        self.assertEqual(result1._value, [1, 2, 3])
        
        result2 = traverse(safe_int, ["1", "abc", "3"])
        self.assertTrue(result2.is_left())
        self.assertEqual(result2._value, "Invalid: abc")
    
    def test_partition_eithers(self):
        """测试 partition_eithers"""
        eithers = [Right(1), Left("a"), Right(2), Left("b")]
        lefts, rights = partition_eithers(eithers)
        self.assertEqual(lefts, ["a", "b"])
        self.assertEqual(rights, [1, 2])


class TestCondEither(unittest.TestCase):
    """测试 cond_either"""
    
    def test_cond_either_match(self):
        """测试 cond_either 匹配"""
        classify = cond_either(
            (lambda x: x > 0, lambda x: Right("positive")),
            (lambda x: x < 0, lambda x: Right("negative")),
            (lambda x: True, lambda x: Left("zero is not allowed")),
        )
        
        self.assertEqual(classify(5)._value, "positive")
        self.assertEqual(classify(-5)._value, "negative")
        self.assertEqual(classify(0)._value, "zero is not allowed")


class TestBimap(unittest.TestCase):
    """测试 bimap"""
    
    def test_bimap_on_right(self):
        """测试 bimap 在 Right 上"""
        transform = bimap(str.upper, lambda x: x * 2)
        result = transform(Right(5))
        self.assertEqual(result._value, 10)
    
    def test_bimap_on_left(self):
        """测试 bimap 在 Left 上"""
        transform = bimap(str.upper, lambda x: x * 2)
        result = transform(Left("error"))
        self.assertEqual(result._value, "ERROR")


class TestEnsure(unittest.TestCase):
    """测试 ensure 函数"""
    
    def test_ensure_true(self):
        """测试 ensure 条件满足"""
        e = ensure(5, 5 > 0, "Must be positive")
        self.assertTrue(e.is_right())
    
    def test_ensure_false(self):
        """测试 ensure 条件不满足"""
        e = ensure(-5, -5 > 0, "Must be positive")
        self.assertTrue(e.is_left())
    
    def test_ensure_pred_true(self):
        """测试 ensure_pred 条件满足"""
        e = ensure_pred(5, lambda x: x > 0, "Must be positive")
        self.assertTrue(e.is_right())
    
    def test_ensure_pred_false(self):
        """测试 ensure_pred 条件不满足"""
        e: Either[str, int] = ensure_pred(-5, lambda x: x > 0, lambda x: f"Got {x}")
        self.assertTrue(e.is_left())
        self.assertEqual(e._value, "Got -5")


class TestEitherChain(unittest.TestCase):
    """测试 EitherChain"""
    
    def test_chain_from_value(self):
        """测试从值创建链"""
        result = chain(10).map(lambda x: x * 2).build()
        self.assertEqual(result._value, 20)
    
    def test_chain_from_error(self):
        """测试从错误创建链"""
        result = chain_error("oops").map(lambda x: x * 2).build()
        self.assertTrue(result.is_left())
    
    def test_chain_filter(self):
        """测试链式过滤"""
        result1 = (chain(10)
            .map(lambda x: x * 2)
            .filter(lambda x: x > 15, "Too small")
            .build())
        self.assertTrue(result1.is_right())
        
        result2 = (chain(5)
            .map(lambda x: x * 2)
            .filter(lambda x: x > 15, "Too small")
            .build())
        self.assertTrue(result2.is_left())
    
    def test_chain_recover(self):
        """测试链式恢复"""
        result = (chain_error("oops")
            .recover(Right(10))
            .build())
        self.assertTrue(result.is_right())
    
    def test_chain_tap(self):
        """测试链式 tap"""
        side_effect = []
        result = (chain(10)
            .tap(lambda x: side_effect.append(x))
            .map(lambda x: x * 2)
            .build())
        self.assertEqual(side_effect, [10])
        self.assertEqual(result._value, 20)
    
    def test_chain_on_success_failure(self):
        """测试 on_success 和 on_failure"""
        success_log = []
        failure_log = []
        
        (chain(10)
            .on_success(lambda x: success_log.append(x))
            .build())
        self.assertEqual(success_log, [10])
        
        (chain_error("oops")
            .on_failure(lambda e: failure_log.append(e))
            .build())
        self.assertEqual(failure_log, ["oops"])


class TestUtilityFunctions(unittest.TestCase):
    """测试实用工具函数"""
    
    def test_all_rights(self):
        """测试 all_rights"""
        eithers = [Right(1), Left("a"), Right(2)]
        self.assertEqual(all_rights(eithers), [1, 2])
    
    def test_all_lefts(self):
        """测试 all_lefts"""
        eithers = [Right(1), Left("a"), Left("b")]
        self.assertEqual(all_lefts(eithers), ["a", "b"])
    
    def test_is_left_is_right(self):
        """测试 is_left 和 is_right"""
        self.assertTrue(is_left(Left("a")))
        self.assertFalse(is_left(Right(1)))
        self.assertTrue(is_right(Right(1)))
        self.assertFalse(is_right(Left("a")))
    
    def test_get_or_else(self):
        """测试 get_or_else"""
        self.assertEqual(get_or_else(Right(5), 0), 5)
        self.assertEqual(get_or_else(Left("error"), 0), 0)


class TestRealWorldScenarios(unittest.TestCase):
    """测试真实世界场景"""
    
    def test_parse_user_input(self):
        """测试解析用户输入"""
        def parse_int(s: str) -> Either[str, int]:
            try:
                n = int(s)
                if n < 0:
                    return Left("Number must be positive")
                return Right(n)
            except ValueError:
                return Left(f"Invalid number: {s}")
        
        result1 = parse_int("42").map(lambda x: x * 2)
        self.assertEqual(result1._value, 84)
        
        result2 = parse_int("abc")
        self.assertTrue(result2.is_left())
        
        result3: Either[str, int] = parse_int("-5")
        self.assertTrue(result3.is_left())
    
    def test_division_chain(self):
        """测试除法链式操作"""
        def safe_divide(a: float, b: float) -> Either[str, float]:
            if b == 0:
                return Left("Division by zero")
            return Right(a / b)
        
        def safe_sqrt(n: float) -> Either[str, float]:
            if n < 0:
                return Left("Cannot sqrt negative number")
            import math
            return Right(math.sqrt(n))
        
        result = (safe_divide(100, 4)
            .flat_map(safe_sqrt)
            .map(lambda x: round(x, 2)))
        self.assertEqual(result._value, 5.0)
        
        result2 = (safe_divide(100, 0)
            .flat_map(safe_sqrt))
        self.assertTrue(result2.is_left())
    
    def test_validation_chain(self):
        """测试验证链"""
        def validate_name(name: str) -> Either[str, str]:
            if not name:
                return Left("Name is required")
            if len(name) < 2:
                return Left("Name must be at least 2 characters")
            return Right(name)
        
        def validate_age(age: int) -> Either[str, int]:
            if age < 0:
                return Left("Age cannot be negative")
            if age > 150:
                return Left("Age is too high")
            return Right(age)
        
        # 验证成功
        name = validate_name("Alice")
        age = validate_age(25)
        
        result = sequence_first_error([name, age])
        self.assertTrue(result.is_right())
        
        # 验证失败
        bad_name: Either[str, str] = validate_name("")
        bad_age: Either[str, int] = validate_age(200)
        
        result2 = sequence_first_error([bad_name, bad_age])
        self.assertTrue(result2.is_left())


if __name__ == '__main__':
    unittest.main(verbosity=2)