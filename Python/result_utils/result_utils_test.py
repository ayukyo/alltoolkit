# -*- coding: utf-8 -*-
"""
AllToolkit - Result Utils 测试

测试 Result/Either 类型及其相关功能。
"""

import unittest
from mod import (
    Ok, Error, Result, Left, Right, Either,
    UnwrapError,
    ok, error, left, right,
    from_optional, from_exception, from_exception_async,
    result_to_either, either_to_result, flatten_result,
    try_call, try_call_with, try_call_async,
    collect_results, partition_results, first_ok,
    safe_get, safe_index, safe_divide,
    safe_parse_int, safe_parse_float,
    ResultContext,
    result_trace, pretty_result,
    is_ok, is_error, is_result, is_left, is_right, is_either
)


class TestOk(unittest.TestCase):
    """测试 Ok 类型"""
    
    def test_creation(self):
        """测试创建 Ok"""
        r = Ok(42)
        self.assertTrue(r.is_ok())
        self.assertFalse(r.is_error())
        self.assertEqual(r.unwrap(), 42)
    
    def test_unwrap_or(self):
        """测试 unwrap_or"""
        r = Ok(42)
        self.assertEqual(r.unwrap_or(0), 42)
    
    def test_unwrap_or_else(self):
        """测试 unwrap_or_else"""
        r = Ok(42)
        self.assertEqual(r.unwrap_or_else(lambda e: 0), 42)
    
    def test_unwrap_error_raises(self):
        """测试 unwrap_error 抛出异常"""
        r = Ok(42)
        with self.assertRaises(UnwrapError):
            r.unwrap_error()
    
    def test_map(self):
        """测试 map"""
        r = Ok(42)
        mapped = r.map(lambda x: x * 2)
        self.assertTrue(mapped.is_ok())
        self.assertEqual(mapped.unwrap(), 84)
    
    def test_map_error(self):
        """测试 map_error"""
        r = Ok(42)
        mapped = r.map_error(lambda e: f"error: {e}")
        self.assertTrue(mapped.is_ok())
        self.assertEqual(mapped.unwrap(), 42)
    
    def test_and_then(self):
        """测试 and_then"""
        r = Ok(42)
        chained = r.and_then(lambda x: Ok(x * 2))
        self.assertTrue(chained.is_ok())
        self.assertEqual(chained.unwrap(), 84)
        
        # 返回 Error
        chained2 = r.and_then(lambda x: Error("failed"))
        self.assertTrue(chained2.is_error())
    
    def test_or_else(self):
        """测试 or_else"""
        r = Ok(42)
        chained = r.or_else(lambda e: Ok(0))
        self.assertTrue(chained.is_ok())
        self.assertEqual(chained.unwrap(), 42)
    
    def test_expect(self):
        """测试 expect"""
        r = Ok(42)
        self.assertEqual(r.expect("should be ok"), 42)
    
    def test_expect_error_raises(self):
        """测试 expect_error 抛出异常"""
        r = Ok(42)
        with self.assertRaises(UnwrapError):
            r.expect_error("should be error")
    
    def test_ok_and_error_methods(self):
        """测试 ok() 和 err() 方法"""
        r = Ok(42)
        self.assertEqual(r.ok(), 42)
        self.assertIsNone(r.err())
    
    def test_repr(self):
        """测试 repr"""
        r = Ok(42)
        self.assertEqual(repr(r), "Ok(42)")
    
    def test_equality(self):
        """测试相等性"""
        r1 = Ok(42)
        r2 = Ok(42)
        r3 = Ok(43)
        self.assertEqual(r1, r2)
        self.assertNotEqual(r1, r3)
        self.assertNotEqual(r1, Error("error"))
    
    def test_hash(self):
        """测试哈希"""
        r1 = Ok(42)
        r2 = Ok(42)
        self.assertEqual(hash(r1), hash(r2))
        # 可以放入集合
        s = {Ok(1), Ok(2), Ok(1)}
        self.assertEqual(len(s), 2)


class TestError(unittest.TestCase):
    """测试 Error 类型"""
    
    def test_creation(self):
        """测试创建 Error"""
        r = Error("something went wrong")
        self.assertFalse(r.is_ok())
        self.assertTrue(r.is_error())
        self.assertEqual(r.unwrap_error(), "something went wrong")
    
    def test_unwrap_raises(self):
        """测试 unwrap 抛出异常"""
        r = Error("error")
        with self.assertRaises(UnwrapError):
            r.unwrap()
    
    def test_unwrap_or(self):
        """测试 unwrap_or"""
        r = Error("error")
        self.assertEqual(r.unwrap_or(42), 42)
    
    def test_unwrap_or_else(self):
        """测试 unwrap_or_else"""
        r = Error("error")
        self.assertEqual(r.unwrap_or_else(lambda e: f"default: {e}"), "default: error")
    
    def test_map(self):
        """测试 map（Error 不变）"""
        r = Error("error")
        mapped = r.map(lambda x: x * 2)
        self.assertTrue(mapped.is_error())
        self.assertEqual(mapped.unwrap_error(), "error")
    
    def test_map_error(self):
        """测试 map_error"""
        r = Error("error")
        mapped = r.map_error(lambda e: f"wrapped: {e}")
        self.assertTrue(mapped.is_error())
        self.assertEqual(mapped.unwrap_error(), "wrapped: error")
    
    def test_and_then(self):
        """测试 and_then（Error 不变）"""
        r = Error("error")
        chained = r.and_then(lambda x: Ok(x * 2))
        self.assertTrue(chained.is_error())
        self.assertEqual(chained.unwrap_error(), "error")
    
    def test_or_else(self):
        """测试 or_else"""
        r = Error("error")
        chained = r.or_else(lambda e: Ok(42))
        self.assertTrue(chained.is_ok())
        self.assertEqual(chained.unwrap(), 42)
        
        chained2 = r.or_else(lambda e: Error(f"new: {e}"))
        self.assertTrue(chained2.is_error())
        self.assertEqual(chained2.unwrap_error(), "new: error")
    
    def test_expect_raises(self):
        """测试 expect 抛出异常"""
        r = Error("error")
        with self.assertRaises(UnwrapError):
            r.expect("should be ok")
    
    def test_expect_error(self):
        """测试 expect_error"""
        r = Error("error")
        self.assertEqual(r.expect_error("msg"), "error")
    
    def test_ok_and_error_methods(self):
        """测试 ok() 和 err() 方法"""
        r = Error("error")
        self.assertIsNone(r.ok())
        self.assertEqual(r.err(), "error")
    
    def test_repr(self):
        """测试 repr"""
        r = Error("error")
        self.assertEqual(repr(r), "Error('error')")
    
    def test_equality(self):
        """测试相等性"""
        r1 = Error("error")
        r2 = Error("error")
        r3 = Error("different")
        self.assertEqual(r1, r2)
        self.assertNotEqual(r1, r3)
    
    def test_hash(self):
        """测试哈希"""
        r1 = Error("error")
        r2 = Error("error")
        self.assertEqual(hash(r1), hash(r2))


class TestLeft(unittest.TestCase):
    """测试 Left 类型"""
    
    def test_creation(self):
        """测试创建 Left"""
        e = Left("error")
        self.assertTrue(e.is_left())
        self.assertFalse(e.is_right())
        self.assertEqual(e.unwrap_left(), "error")
    
    def test_unwrap_right_raises(self):
        """测试 unwrap_right 抛出异常"""
        e = Left("error")
        with self.assertRaises(UnwrapError):
            e.unwrap_right()
    
    def test_map_left(self):
        """测试 map_left"""
        e = Left("error")
        mapped = e.map_left(lambda x: f"mapped: {x}")
        self.assertTrue(mapped.is_left())
        self.assertEqual(mapped.unwrap_left(), "mapped: error")
    
    def test_map_right(self):
        """测试 map_right（Left 不变）"""
        e = Left("error")
        mapped = e.map_right(lambda x: x * 2)
        self.assertTrue(mapped.is_left())
        self.assertEqual(mapped.unwrap_left(), "error")
    
    def test_fold(self):
        """测试 fold"""
        e = Left("error")
        result = e.fold(
            left_fn=lambda x: f"left: {x}",
            right_fn=lambda x: f"right: {x}"
        )
        self.assertEqual(result, "left: error")
    
    def test_swap(self):
        """测试 swap"""
        e = Left("error")
        swapped = e.swap()
        self.assertTrue(swapped.is_right())
        self.assertEqual(swapped.unwrap_right(), "error")
    
    def test_left_and_right_methods(self):
        """测试 left() 和 right() 方法"""
        e = Left("error")
        self.assertEqual(e.left(), "error")
        self.assertIsNone(e.right())


class TestRight(unittest.TestCase):
    """测试 Right 类型"""
    
    def test_creation(self):
        """测试创建 Right"""
        e = Right(42)
        self.assertFalse(e.is_left())
        self.assertTrue(e.is_right())
        self.assertEqual(e.unwrap_right(), 42)
    
    def test_unwrap_left_raises(self):
        """测试 unwrap_left 抛出异常"""
        e = Right(42)
        with self.assertRaises(UnwrapError):
            e.unwrap_left()
    
    def test_map_left(self):
        """测试 map_left（Right 不变）"""
        e = Right(42)
        mapped = e.map_left(lambda x: f"mapped: {x}")
        self.assertTrue(mapped.is_right())
        self.assertEqual(mapped.unwrap_right(), 42)
    
    def test_map_right(self):
        """测试 map_right"""
        e = Right(42)
        mapped = e.map_right(lambda x: x * 2)
        self.assertTrue(mapped.is_right())
        self.assertEqual(mapped.unwrap_right(), 84)
    
    def test_fold(self):
        """测试 fold"""
        e = Right(42)
        result = e.fold(
            left_fn=lambda x: f"left: {x}",
            right_fn=lambda x: f"right: {x}"
        )
        self.assertEqual(result, "right: 42")
    
    def test_swap(self):
        """测试 swap"""
        e = Right(42)
        swapped = e.swap()
        self.assertTrue(swapped.is_left())
        self.assertEqual(swapped.unwrap_left(), 42)
    
    def test_left_and_right_methods(self):
        """测试 left() 和 right() 方法"""
        e = Right(42)
        self.assertIsNone(e.left())
        self.assertEqual(e.right(), 42)


class TestHelperFunctions(unittest.TestCase):
    """测试辅助函数"""
    
    def test_ok_function(self):
        """测试 ok 函数"""
        r = ok(42)
        self.assertTrue(isinstance(r, Ok))
        self.assertEqual(r.unwrap(), 42)
    
    def test_error_function(self):
        """测试 error 函数"""
        r = error("failed")
        self.assertTrue(isinstance(r, Error))
        self.assertEqual(r.unwrap_error(), "failed")
    
    def test_left_function(self):
        """测试 left 函数"""
        e = left("error")
        self.assertTrue(isinstance(e, Left))
        self.assertEqual(e.unwrap_left(), "error")
    
    def test_right_function(self):
        """测试 right 函数"""
        e = right(42)
        self.assertTrue(isinstance(e, Right))
        self.assertEqual(e.unwrap_right(), 42)
    
    def test_from_optional(self):
        """测试 from_optional"""
        r1 = from_optional(42, "not found")
        self.assertTrue(r1.is_ok())
        self.assertEqual(r1.unwrap(), 42)
        
        r2 = from_optional(None, "not found")
        self.assertTrue(r2.is_error())
        self.assertEqual(r2.unwrap_error(), "not found")
    
    def test_from_exception(self):
        """测试 from_exception"""
        @from_exception
        def divide(a, b):
            return a / b
        
        r1 = divide(10, 2)
        self.assertTrue(r1.is_ok())
        self.assertEqual(r1.unwrap(), 5.0)
        
        r2 = divide(10, 0)
        self.assertTrue(r2.is_error())
        self.assertTrue(isinstance(r2.unwrap_error(), ZeroDivisionError))
    
    def test_try_call(self):
        """测试 try_call"""
        r1 = try_call(int, "42")
        self.assertTrue(r1.is_ok())
        self.assertEqual(r1.unwrap(), 42)
        
        r2 = try_call(int, "abc")
        self.assertTrue(r2.is_error())
        self.assertTrue(isinstance(r2.unwrap_error(), ValueError))
    
    def test_try_call_with(self):
        """测试 try_call_with"""
        r1 = try_call_with(ValueError, int, "abc")
        self.assertTrue(r1.is_error())
        self.assertTrue(isinstance(r1.unwrap_error(), ValueError))
        
        # 其他异常类型不会被捕获，会在unwrap时抛出原始异常
        # 注意：try_call_with 只捕获指定类型的异常


class TestCollectFunctions(unittest.TestCase):
    """测试收集函数"""
    
    def test_collect_results_all_ok(self):
        """测试 collect_results 全成功"""
        results = [Ok(1), Ok(2), Ok(3)]
        collected = collect_results(results)
        self.assertTrue(collected.is_ok())
        self.assertEqual(collected.unwrap(), [1, 2, 3])
    
    def test_collect_results_some_error(self):
        """测试 collect_results 有失败"""
        results = [Ok(1), Error("e1"), Error("e2")]
        collected = collect_results(results)
        self.assertTrue(collected.is_error())
        self.assertEqual(collected.unwrap_error(), ["e1", "e2"])
    
    def test_partition_results(self):
        """测试 partition_results"""
        results = [Ok(1), Error("e1"), Ok(2), Error("e2")]
        values, errors = partition_results(results)
        self.assertEqual(values, [1, 2])
        self.assertEqual(errors, ["e1", "e2"])
    
    def test_first_ok(self):
        """测试 first_ok"""
        results = [Error("e1"), Ok(42), Ok(43)]
        r = first_ok(results)
        self.assertTrue(r.is_ok())
        self.assertEqual(r.unwrap(), 42)
        
        # 全失败
        results2 = [Error("e1"), Error("e2")]
        r2 = first_ok(results2)
        self.assertTrue(r2.is_error())
        self.assertEqual(r2.unwrap_error(), ["e1", "e2"])


class TestConversionFunctions(unittest.TestCase):
    """测试转换函数"""
    
    def test_result_to_either(self):
        """测试 result_to_either"""
        r1 = result_to_either(Ok(42))
        self.assertTrue(r1.is_right())
        self.assertEqual(r1.unwrap_right(), 42)
        
        r2 = result_to_either(Error("error"))
        self.assertTrue(r2.is_left())
        self.assertEqual(r2.unwrap_left(), "error")
    
    def test_either_to_result(self):
        """测试 either_to_result"""
        r1 = either_to_result(Right(42))
        self.assertTrue(r1.is_ok())
        self.assertEqual(r1.unwrap(), 42)
        
        r2 = either_to_result(Left("error"))
        self.assertTrue(r2.is_error())
        self.assertEqual(r2.unwrap_error(), "error")
    
    def test_flatten_result(self):
        """测试 flatten_result"""
        r1 = flatten_result(Ok(Ok(42)))
        self.assertTrue(r1.is_ok())
        self.assertEqual(r1.unwrap(), 42)
        
        r2 = flatten_result(Ok(Error("inner error")))
        self.assertTrue(r2.is_error())
        self.assertEqual(r2.unwrap_error(), "inner error")
        
        r3 = flatten_result(Error("outer error"))
        self.assertTrue(r3.is_error())
        self.assertEqual(r3.unwrap_error(), "outer error")


class TestSafeOperations(unittest.TestCase):
    """测试安全操作"""
    
    def test_safe_get(self):
        """测试 safe_get"""
        d = {"a": 1, "b": 2}
        
        r1 = safe_get(d, "a", "not found")
        self.assertTrue(r1.is_ok())
        self.assertEqual(r1.unwrap(), 1)
        
        r2 = safe_get(d, "c", "not found")
        self.assertTrue(r2.is_error())
        self.assertEqual(r2.unwrap_error(), "not found")
    
    def test_safe_index(self):
        """测试 safe_index"""
        lst = [1, 2, 3]
        
        r1 = safe_index(lst, 1, "out of bounds")
        self.assertTrue(r1.is_ok())
        self.assertEqual(r1.unwrap(), 2)
        
        r2 = safe_index(lst, 10, "out of bounds")
        self.assertTrue(r2.is_error())
        self.assertEqual(r2.unwrap_error(), "out of bounds")
        
        # 负索引
        r3 = safe_index(lst, -1, "out of bounds")
        self.assertTrue(r3.is_ok())
        self.assertEqual(r3.unwrap(), 3)
    
    def test_safe_divide(self):
        """测试 safe_divide"""
        r1 = safe_divide(10, 2)
        self.assertTrue(r1.is_ok())
        self.assertEqual(r1.unwrap(), 5.0)
        
        r2 = safe_divide(10, 0)
        self.assertTrue(r2.is_error())
        self.assertEqual(r2.unwrap_error(), "division by zero")
        
        # 自定义错误
        r3 = safe_divide(10, 0, Error("zero error"))
        self.assertEqual(r3.unwrap_error(), Error("zero error"))
    
    def test_safe_parse_int(self):
        """测试 safe_parse_int"""
        r1 = safe_parse_int("42")
        self.assertTrue(r1.is_ok())
        self.assertEqual(r1.unwrap(), 42)
        
        r2 = safe_parse_int("abc")
        self.assertTrue(r2.is_error())
        self.assertEqual(r2.unwrap_error(), "invalid integer")
    
    def test_safe_parse_float(self):
        """测试 safe_parse_float"""
        r1 = safe_parse_float("3.14")
        self.assertTrue(r1.is_ok())
        self.assertEqual(r1.unwrap(), 3.14)
        
        r2 = safe_parse_float("abc")
        self.assertTrue(r2.is_error())
        self.assertEqual(r2.unwrap_error(), "invalid float")


class TestResultContext(unittest.TestCase):
    """测试 ResultContext"""
    
    def test_success_context(self):
        """测试成功上下文"""
        with ResultContext() as ctx:
            value = int("42")
            ctx.set_ok(value)
        
        r = ctx.result
        self.assertTrue(r is not None)
        self.assertTrue(r.is_ok())
        self.assertEqual(r.unwrap(), 42)
    
    def test_exception_context(self):
        """测试异常上下文"""
        with ResultContext() as ctx:
            value = int("abc")  # 会抛出 ValueError
            ctx.set_ok(value)
        
        r = ctx.result
        self.assertTrue(r is not None)
        self.assertTrue(r.is_error())
        self.assertTrue(isinstance(r.unwrap_error(), ValueError))
    
    def test_get_result(self):
        """测试 get_result"""
        with ResultContext() as ctx:
            # 不设置任何值
            pass
        
        r = ctx.get_result("no value")
        self.assertTrue(r.is_error())
        self.assertEqual(r.unwrap_error(), "no value")


class TestDebugTools(unittest.TestCase):
    """测试调试工具"""
    
    def test_result_trace_ok(self):
        """测试 result_trace Ok"""
        r = Ok(42)
        trace = result_trace(r)
        self.assertEqual(trace["type"], "Ok")
        self.assertEqual(trace["value"], 42)
    
    def test_result_trace_error(self):
        """测试 result_trace Error"""
        r = Error("error")
        trace = result_trace(r, include_stack=False)
        self.assertEqual(trace["type"], "Error")
        self.assertEqual(trace["value"], "error")
    
    def test_result_trace_with_stack(self):
        """测试 result_trace 包含堆栈"""
        try:
            raise ValueError("test error")
        except ValueError as e:
            r = Error(e)
            trace = result_trace(r, include_stack=True)
            self.assertEqual(trace["type"], "Error")
            self.assertIn("stack_trace", trace)
    
    def test_pretty_result(self):
        """测试 pretty_result"""
        r1 = Ok(42)
        self.assertEqual(pretty_result(r1), "✓ Ok: 42")
        
        r2 = Error("failed")
        self.assertEqual(pretty_result(r2), "✗ Error: 'failed'")


class TestTypeCheckFunctions(unittest.TestCase):
    """测试类型检查函数"""
    
    def test_is_ok(self):
        """测试 is_ok"""
        self.assertTrue(is_ok(Ok(42)))
        self.assertFalse(is_ok(Error("error")))
        self.assertFalse(is_ok(42))
    
    def test_is_error(self):
        """测试 is_error"""
        self.assertTrue(is_error(Error("error")))
        self.assertFalse(is_error(Ok(42)))
        self.assertFalse(is_error("error"))
    
    def test_is_result(self):
        """测试 is_result"""
        self.assertTrue(is_result(Ok(42)))
        self.assertTrue(is_result(Error("error")))
        self.assertFalse(is_result(42))
    
    def test_is_left(self):
        """测试 is_left"""
        self.assertTrue(is_left(Left("error")))
        self.assertFalse(is_left(Right(42)))
        self.assertFalse(is_left("left"))
    
    def test_is_right(self):
        """测试 is_right"""
        self.assertTrue(is_right(Right(42)))
        self.assertFalse(is_right(Left("error")))
        self.assertFalse(is_right(42))
    
    def test_is_either(self):
        """测试 is_either"""
        self.assertTrue(is_either(Left("error")))
        self.assertTrue(is_either(Right(42)))
        self.assertFalse(is_either(42))


class TestChainedOperations(unittest.TestCase):
    """测试链式操作"""
    
    def test_chained_map_and_then(self):
        """测试链式 map 和 and_then"""
        def parse_int(s: str) -> Result[int, str]:
            try:
                return Ok(int(s))
            except ValueError:
                return Error(f"invalid int: {s}")
        
        def validate_positive(n: int) -> Result[int, str]:
            if n > 0:
                return Ok(n)
            return Error(f"not positive: {n}")
        
        result = parse_int("42").and_then(validate_positive).map(lambda x: x * 2)
        self.assertTrue(result.is_ok())
        self.assertEqual(result.unwrap(), 84)
        
        result2 = parse_int("-5").and_then(validate_positive)
        self.assertTrue(result2.is_error())
        self.assertEqual(result2.unwrap_error(), "not positive: -5")
    
    def test_complex_pipeline(self):
        """测试复杂管道"""
        # 模拟用户数据处理管道
        def validate_name(name: str) -> Result[str, str]:
            if len(name) >= 2:
                return Ok(name)
            return Error("name too short")
        
        def validate_age(age_str: str) -> Result[int, str]:
            try:
                age = int(age_str)
                if age >= 0 and age <= 150:
                    return Ok(age)
                return Error("invalid age range")
            except ValueError:
                return Error("age not a number")
        
        def create_user(name: str, age: int) -> Result[dict, str]:
            return Ok({"name": name, "age": age})
        
        # 成功流程
        name_result = validate_name("John")
        age_result = validate_age("25")
        
        if name_result.is_ok() and age_result.is_ok():
            user_result = create_user(name_result.unwrap(), age_result.unwrap())
            self.assertTrue(user_result.is_ok())
            self.assertEqual(user_result.unwrap(), {"name": "John", "age": 25})
    
    def test_error_recovery(self):
        """测试错误恢复"""
        def fetch_data(id: int) -> Result[str, str]:
            if id > 0:
                return Ok(f"data-{id}")
            return Error("invalid id")
        
        def get_default(e: str) -> Result[str, str]:
            return Ok("default-data")
        
        result = fetch_data(-1).or_else(get_default)
        self.assertTrue(result.is_ok())
        self.assertEqual(result.unwrap(), "default-data")


if __name__ == "__main__":
    unittest.main(verbosity=2)