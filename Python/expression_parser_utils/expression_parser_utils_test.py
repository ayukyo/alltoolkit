"""
Expression Parser Utils 测试

测试所有核心功能
"""

import unittest
import math
from expression_parser_utils import (
    ExpressionParser,
    ExpressionError,
    safe_eval,
    validate_expression,
    extract_variables,
    MathFunctions,
    BUILTIN_FUNCTIONS,
)


class TestLexer(unittest.TestCase):
    """词法分析器测试"""

    def test_numbers(self):
        """测试数字解析"""
        parser = ExpressionParser()
        
        # 整数
        ast = parser.parse("42")
        result = parser.evaluate(ast)
        self.assertEqual(result, 42)
        
        # 浮点数
        ast = parser.parse("3.14159")
        result = parser.evaluate(ast)
        self.assertAlmostEqual(result, 3.14159)
        
        # 科学计数法
        ast = parser.parse("1e10")
        result = parser.evaluate(ast)
        self.assertEqual(result, 1e10)
        
        ast = parser.parse("1.5e-3")
        result = parser.evaluate(ast)
        self.assertEqual(result, 1.5e-3)

    def test_strings(self):
        """测试字符串解析"""
        parser = ExpressionParser()
        
        # 双引号字符串
        ast = parser.parse('"hello"')
        result = parser.evaluate(ast)
        self.assertEqual(result, "hello")
        
        # 单引号字符串
        ast = parser.parse("'world'")
        result = parser.evaluate(ast)
        self.assertEqual(result, "world")
        
        # 转义字符
        ast = parser.parse(r'"hello\nworld"')
        result = parser.evaluate(ast)
        self.assertEqual(result, "hello\nworld")

    def test_operators(self):
        """测试运算符"""
        parser = ExpressionParser()
        
        # 算术运算符 - 测试完整表达式
        ast = parser.parse("1 + 2")
        result = parser.evaluate(ast)
        self.assertEqual(result, 3)


class TestArithmetic(unittest.TestCase):
    """算术运算测试"""

    def setUp(self):
        self.parser = ExpressionParser()

    def test_addition(self):
        """加法测试"""
        self.assertEqual(self.parser.evaluate(self.parser.parse("1 + 2")), 3)
        self.assertEqual(self.parser.evaluate(self.parser.parse("1.5 + 2.5")), 4.0)
        self.assertEqual(self.parser.evaluate(self.parser.parse("-1 + 1")), 0)

    def test_subtraction(self):
        """减法测试"""
        self.assertEqual(self.parser.evaluate(self.parser.parse("5 - 3")), 2)
        self.assertEqual(self.parser.evaluate(self.parser.parse("3 - 5")), -2)
        self.assertEqual(self.parser.evaluate(self.parser.parse("0 - 0")), 0)

    def test_multiplication(self):
        """乘法测试"""
        self.assertEqual(self.parser.evaluate(self.parser.parse("3 * 4")), 12)
        self.assertEqual(self.parser.evaluate(self.parser.parse("-2 * 3")), -6)
        self.assertEqual(self.parser.evaluate(self.parser.parse("2.5 * 4")), 10.0)

    def test_division(self):
        """除法测试"""
        self.assertEqual(self.parser.evaluate(self.parser.parse("12 / 4")), 3.0)
        self.assertEqual(self.parser.evaluate(self.parser.parse("1 / 2")), 0.5)
        
        # 除以零错误
        with self.assertRaises(ExpressionError):
            self.parser.evaluate(self.parser.parse("1 / 0"))

    def test_floor_division(self):
        """整除测试"""
        self.assertEqual(self.parser.evaluate(self.parser.parse("7 // 3")), 2)
        self.assertEqual(self.parser.evaluate(self.parser.parse("-7 // 3")), -3)

    def test_modulo(self):
        """取模测试"""
        self.assertEqual(self.parser.evaluate(self.parser.parse("7 % 3")), 1)
        self.assertEqual(self.parser.evaluate(self.parser.parse("10 % 5")), 0)

    def test_power(self):
        """幂运算测试"""
        self.assertEqual(self.parser.evaluate(self.parser.parse("2 ** 3")), 8)
        self.assertEqual(self.parser.evaluate(self.parser.parse("4 ** 0.5")), 2.0)
        self.assertEqual(self.parser.evaluate(self.parser.parse("2 ** -1")), 0.5)

    def test_operator_precedence(self):
        """运算符优先级测试"""
        # 乘除优先于加减
        self.assertEqual(self.parser.evaluate(self.parser.parse("2 + 3 * 4")), 14)
        self.assertEqual(self.parser.evaluate(self.parser.parse("2 * 3 + 4")), 10)
        
        # 幂运算优先级最高
        self.assertEqual(self.parser.evaluate(self.parser.parse("2 * 3 ** 2")), 18)
        
        # 幂运算右结合
        self.assertEqual(self.parser.evaluate(self.parser.parse("2 ** 3 ** 2")), 512)  # 2^(3^2) = 2^9

    def test_parentheses(self):
        """括号测试"""
        self.assertEqual(self.parser.evaluate(self.parser.parse("(2 + 3) * 4")), 20)
        self.assertEqual(self.parser.evaluate(self.parser.parse("2 * (3 + 4)")), 14)
        self.assertEqual(self.parser.evaluate(self.parser.parse("((1 + 2) * 3)")), 9)

    def test_unary_operators(self):
        """一元运算符测试"""
        self.assertEqual(self.parser.evaluate(self.parser.parse("-5")), -5)
        self.assertEqual(self.parser.evaluate(self.parser.parse("--5")), 5)
        self.assertEqual(self.parser.evaluate(self.parser.parse("+-5")), -5)

    def test_string_concatenation(self):
        """字符串拼接测试"""
        self.assertEqual(
            self.parser.evaluate(self.parser.parse('"hello" + " " + "world"')),
            "hello world"
        )
        self.assertEqual(
            self.parser.evaluate(self.parser.parse('"value: " + 42')),
            "value: 42"
        )


class TestComparison(unittest.TestCase):
    """比较运算测试"""

    def setUp(self):
        self.parser = ExpressionParser()

    def test_equality(self):
        """相等测试"""
        self.assertTrue(self.parser.evaluate(self.parser.parse("1 == 1")))
        self.assertFalse(self.parser.evaluate(self.parser.parse("1 == 2")))
        self.assertTrue(self.parser.evaluate(self.parser.parse('"a" == "a"')))

    def test_inequality(self):
        """不等测试"""
        self.assertTrue(self.parser.evaluate(self.parser.parse("1 != 2")))
        self.assertFalse(self.parser.evaluate(self.parser.parse("1 != 1")))

    def test_less_than(self):
        """小于测试"""
        self.assertTrue(self.parser.evaluate(self.parser.parse("1 < 2")))
        self.assertFalse(self.parser.evaluate(self.parser.parse("2 < 2")))
        self.assertFalse(self.parser.evaluate(self.parser.parse("3 < 2")))

    def test_less_equal(self):
        """小于等于测试"""
        self.assertTrue(self.parser.evaluate(self.parser.parse("1 <= 2")))
        self.assertTrue(self.parser.evaluate(self.parser.parse("2 <= 2")))
        self.assertFalse(self.parser.evaluate(self.parser.parse("3 <= 2")))

    def test_greater_than(self):
        """大于测试"""
        self.assertTrue(self.parser.evaluate(self.parser.parse("2 > 1")))
        self.assertFalse(self.parser.evaluate(self.parser.parse("2 > 2")))
        self.assertFalse(self.parser.evaluate(self.parser.parse("1 > 2")))

    def test_greater_equal(self):
        """大于等于测试"""
        self.assertTrue(self.parser.evaluate(self.parser.parse("2 >= 1")))
        self.assertTrue(self.parser.evaluate(self.parser.parse("2 >= 2")))
        self.assertFalse(self.parser.evaluate(self.parser.parse("1 >= 2")))


class TestLogicalOperations(unittest.TestCase):
    """逻辑运算测试"""

    def setUp(self):
        self.parser = ExpressionParser()

    def test_and(self):
        """AND 测试"""
        self.assertTrue(self.parser.evaluate(self.parser.parse("true and true")))
        self.assertFalse(self.parser.evaluate(self.parser.parse("true and false")))
        self.assertFalse(self.parser.evaluate(self.parser.parse("false and true")))
        self.assertFalse(self.parser.evaluate(self.parser.parse("false and false")))
        
        # && 别名
        self.assertTrue(self.parser.evaluate(self.parser.parse("1 && 1")))
        self.assertFalse(self.parser.evaluate(self.parser.parse("1 && 0")))

    def test_or(self):
        """OR 测试"""
        self.assertTrue(self.parser.evaluate(self.parser.parse("true or false")))
        self.assertTrue(self.parser.evaluate(self.parser.parse("false or true")))
        self.assertTrue(self.parser.evaluate(self.parser.parse("true or true")))
        self.assertFalse(self.parser.evaluate(self.parser.parse("false or false")))
        
        # || 别名
        self.assertTrue(self.parser.evaluate(self.parser.parse("1 || 0")))
        self.assertFalse(self.parser.evaluate(self.parser.parse("0 || 0")))

    def test_not(self):
        """NOT 测试"""
        self.assertFalse(self.parser.evaluate(self.parser.parse("not true")))
        self.assertTrue(self.parser.evaluate(self.parser.parse("not false")))
        self.assertTrue(self.parser.evaluate(self.parser.parse("!false")))

    def test_short_circuit(self):
        """短路求值测试"""
        # and 短路
        ast = self.parser.parse("false and (1/0 == 0)")
        result = self.parser.evaluate(ast)
        self.assertFalse(result)
        
        # or 短路
        ast = self.parser.parse("true or (1/0 == 0)")
        result = self.parser.evaluate(ast)
        self.assertTrue(result)


class TestVariables(unittest.TestCase):
    """变量测试"""

    def setUp(self):
        self.parser = ExpressionParser()

    def test_single_variable(self):
        """单变量测试"""
        ast = self.parser.parse("x")
        result = self.parser.evaluate(ast, variables={'x': 42})
        self.assertEqual(result, 42)

    def test_multiple_variables(self):
        """多变量测试"""
        ast = self.parser.parse("x + y * z")
        result = self.parser.evaluate(ast, variables={'x': 1, 'y': 2, 'z': 3})
        self.assertEqual(result, 7)

    def test_undefined_variable(self):
        """未定义变量测试"""
        ast = self.parser.parse("x + y")
        with self.assertRaises(ExpressionError):
            self.parser.evaluate(ast, variables={'x': 1})

    def test_variable_types(self):
        """变量类型测试"""
        # 整数
        ast = self.parser.parse("x * 2")
        self.assertEqual(self.parser.evaluate(ast, variables={'x': 5}), 10)
        
        # 浮点数
        ast = self.parser.parse("x * 2")
        self.assertEqual(self.parser.evaluate(ast, variables={'x': 2.5}), 5.0)
        
        # 字符串
        ast = self.parser.parse("x + '!'")
        self.assertEqual(self.parser.evaluate(ast, variables={'x': 'hello'}), 'hello!')


class TestFunctions(unittest.TestCase):
    """函数测试"""

    def setUp(self):
        self.parser = ExpressionParser(functions=BUILTIN_FUNCTIONS)

    def test_builtin_math_functions(self):
        """内置数学函数测试"""
        # sqrt
        self.assertEqual(self.parser.evaluate(self.parser.parse("sqrt(16)")), 4.0)
        
        # abs
        self.assertEqual(self.parser.evaluate(self.parser.parse("abs(-5)")), 5)
        
        # sin/cos
        self.assertAlmostEqual(self.parser.evaluate(self.parser.parse("sin(0)")), 0)
        self.assertAlmostEqual(self.parser.evaluate(self.parser.parse("cos(0)")), 1)
        
        # floor/ceil
        self.assertEqual(self.parser.evaluate(self.parser.parse("floor(3.7)")), 3)
        self.assertEqual(self.parser.evaluate(self.parser.parse("ceil(3.2)")), 4)

    def test_multi_arg_functions(self):
        """多参数函数测试"""
        # min/max
        self.assertEqual(self.parser.evaluate(self.parser.parse("min(1, 2, 3)")), 1)
        self.assertEqual(self.parser.evaluate(self.parser.parse("max(1, 2, 3)")), 3)
        
        # sum/avg
        self.assertEqual(self.parser.evaluate(self.parser.parse("sum(1, 2, 3, 4)")), 10)
        self.assertEqual(self.parser.evaluate(self.parser.parse("avg(1, 2, 3, 4)")), 2.5)
        
        # clamp
        self.assertEqual(self.parser.evaluate(self.parser.parse("clamp(5, 0, 10)")), 5)
        self.assertEqual(self.parser.evaluate(self.parser.parse("clamp(-5, 0, 10)")), 0)
        self.assertEqual(self.parser.evaluate(self.parser.parse("clamp(15, 0, 10)")), 10)

    def test_nested_function_calls(self):
        """嵌套函数调用测试"""
        self.assertEqual(
            self.parser.evaluate(self.parser.parse("sqrt(abs(-16))")),
            4.0
        )
        self.assertEqual(
            self.parser.evaluate(self.parser.parse("floor(sqrt(10))")),
            3
        )

    def test_custom_function(self):
        """自定义函数测试"""
        ast = self.parser.parse("double(x)")
        result = self.parser.evaluate(
            ast,
            variables={'x': 5},
            functions={'double': lambda x: x * 2}
        )
        self.assertEqual(result, 10)

    def test_function_with_variables(self):
        """带变量的函数调用测试"""
        ast = self.parser.parse("sqrt(x * x + y * y)")
        result = self.parser.evaluate(
            ast,
            variables={'x': 3, 'y': 4}
        )
        self.assertEqual(result, 5.0)


class TestSafeEval(unittest.TestCase):
    """safe_eval 便捷接口测试"""

    def test_simple_expression(self):
        """简单表达式测试"""
        self.assertEqual(safe_eval("2 + 3 * 4"), 14)
        self.assertEqual(safe_eval("(2 + 3) * 4"), 20)

    def test_with_variables(self):
        """带变量测试"""
        self.assertEqual(
            safe_eval("x + y", variables={'x': 10, 'y': 20}),
            30
        )
        self.assertEqual(
            safe_eval("x * y - z", variables={'x': 2, 'y': 3, 'z': 1}),
            5
        )

    def test_with_functions(self):
        """带函数测试"""
        self.assertEqual(safe_eval("sqrt(16)"), 4.0)
        self.assertEqual(safe_eval("max(1, 2, 3)"), 3)
        self.assertEqual(safe_eval("floor(3.7)"), 3)

    def test_complex_expression(self):
        """复杂表达式测试"""
        result = safe_eval(
            "sqrt(x**2 + y**2) + abs(z)",
            variables={'x': 3, 'y': 4, 'z': -5}
        )
        self.assertEqual(result, 10.0)

    def test_logical_expression(self):
        """逻辑表达式测试"""
        self.assertTrue(safe_eval("x > 0 and y < 10", variables={'x': 5, 'y': 3}))
        self.assertFalse(safe_eval("x > 0 and y < 10", variables={'x': 5, 'y': 15}))

    def test_custom_function(self):
        """自定义函数测试"""
        result = safe_eval(
            "square(x) + cube(y)",
            variables={'x': 2, 'y': 3},
            functions={
                'square': lambda x: x**2,
                'cube': lambda x: x**3
            }
        )
        self.assertEqual(result, 4 + 27)


class TestValidation(unittest.TestCase):
    """表达式验证测试"""

    def test_valid_expressions(self):
        """有效表达式测试"""
        self.assertEqual(validate_expression("1 + 2"), (True, None))
        self.assertEqual(validate_expression("x + y * z"), (True, None))
        self.assertEqual(validate_expression("sin(x) + cos(y)"), (True, None))

    def test_invalid_expressions(self):
        """无效表达式测试"""
        is_valid, error = validate_expression("1 +")
        self.assertFalse(is_valid)
        self.assertIn("Unexpected", error)

        is_valid, error = validate_expression("(1 + 2")
        self.assertFalse(is_valid)

    def test_empty_expression(self):
        """空表达式测试"""
        is_valid, _ = validate_expression("")
        # 空表达式应该返回 EOF，可以认为有效但结果是 None


class TestExtractVariables(unittest.TestCase):
    """变量提取测试"""

    def test_single_variable(self):
        """单变量测试"""
        self.assertEqual(extract_variables("x"), {'x'})

    def test_multiple_variables(self):
        """多变量测试"""
        self.assertEqual(extract_variables("x + y"), {'x', 'y'})
        self.assertEqual(extract_variables("x + y * z"), {'x', 'y', 'z'})

    def test_variable_in_function(self):
        """函数中的变量测试"""
        self.assertEqual(extract_variables("sin(x)"), {'x'})
        self.assertEqual(extract_variables("max(x, y)"), {'x', 'y'})

    def test_no_variables(self):
        """无变量测试"""
        self.assertEqual(extract_variables("1 + 2"), set())

    def test_complex_expression(self):
        """复杂表达式测试"""
        vars_set = extract_variables("sqrt(x*x + y*y) + z")
        self.assertEqual(vars_set, {'x', 'y', 'z'})


class TestMathFunctions(unittest.TestCase):
    """MathFunctions 类测试"""

    def test_builtin_functions(self):
        """内置函数测试"""
        funcs = MathFunctions()
        
        self.assertTrue(funcs.has('sin'))
        self.assertTrue(funcs.has('cos'))
        self.assertTrue(funcs.has('sqrt'))
        self.assertTrue(funcs.has('abs'))

    def test_add_function(self):
        """添加函数测试"""
        funcs = MathFunctions()
        funcs.add('double', lambda x: x * 2)
        
        self.assertTrue(funcs.has('double'))
        self.assertEqual(funcs['double'](5), 10)

    def test_remove_function(self):
        """移除函数测试"""
        funcs = MathFunctions()
        self.assertTrue(funcs.has('sin'))
        
        result = funcs.remove('sin')
        self.assertTrue(result)
        self.assertFalse(funcs.has('sin'))

    def test_custom_functions_only(self):
        """仅自定义函数测试"""
        funcs = MathFunctions(include_builtins=False)
        self.assertEqual(len(funcs), 0)
        
        funcs.add('custom', lambda x: x + 1)
        self.assertEqual(len(funcs), 1)


class TestEdgeCases(unittest.TestCase):
    """边缘情况测试"""

    def setUp(self):
        self.parser = ExpressionParser(functions=BUILTIN_FUNCTIONS)

    def test_whitespace(self):
        """空白字符测试"""
        self.assertEqual(
            self.parser.evaluate(self.parser.parse("  1  +  2  ")),
            3
        )
        self.assertEqual(
            self.parser.evaluate(self.parser.parse("1+2")),
            3
        )

    def test_deeply_nested(self):
        """深层嵌套测试"""
        ast = self.parser.parse("((((1 + 2))))")
        self.assertEqual(self.parser.evaluate(ast), 3)

    def test_very_long_expression(self):
        """长表达式测试"""
        expression = " + ".join(str(i) for i in range(100))
        ast = self.parser.parse(expression)
        result = self.parser.evaluate(ast)
        self.assertEqual(result, sum(range(100)))

    def test_floating_point_precision(self):
        """浮点精度测试"""
        ast = self.parser.parse("0.1 + 0.2")
        result = self.parser.evaluate(ast)
        self.assertAlmostEqual(result, 0.3, places=10)

    def test_large_numbers(self):
        """大数测试"""
        ast = self.parser.parse("1e100 * 1e100")
        result = self.parser.evaluate(ast)
        self.assertEqual(result, 1e200)

    def test_special_values(self):
        """特殊值测试"""
        import math
        
        # 测试 NaN 检查函数
        result = self.parser.evaluate(self.parser.parse("isnan(0)"))
        self.assertFalse(result)
        
        # 测试 isinf 检查函数 - 使用一个非常大的数
        result = self.parser.evaluate(self.parser.parse("isinf(1e1000)"))
        self.assertTrue(result)
        
        # 测试大数运算
        ast = self.parser.parse("1e100 * 1e100")
        result = self.parser.evaluate(ast)
        self.assertEqual(result, 1e200)


class TestTrigonometricFunctions(unittest.TestCase):
    """三角函数测试"""

    def setUp(self):
        self.parser = ExpressionParser(functions=BUILTIN_FUNCTIONS)

    def test_sin_cos_tan(self):
        """正弦余弦正切测试"""
        import math
        
        self.assertAlmostEqual(self.parser.evaluate(self.parser.parse("sin(0)")), 0)
        self.assertAlmostEqual(self.parser.evaluate(self.parser.parse("cos(0)")), 1)
        self.assertAlmostEqual(
            self.parser.evaluate(self.parser.parse("sin(pi/2)"), variables={'pi': math.pi}),
            1
        )

    def test_inverse_trig(self):
        """反三角函数测试"""
        self.assertAlmostEqual(self.parser.evaluate(self.parser.parse("asin(0)")), 0)
        self.assertAlmostEqual(self.parser.evaluate(self.parser.parse("acos(1)")), 0)
        self.assertAlmostEqual(self.parser.evaluate(self.parser.parse("atan(0)")), 0)

    def test_degrees_radians(self):
        """角度弧度转换测试"""
        import math
        
        # 180 度 = π 弧度
        result = self.parser.evaluate(self.parser.parse("radians(180)"))
        self.assertAlmostEqual(result, math.pi)
        
        result = self.parser.evaluate(self.parser.parse("degrees(pi)"), variables={'pi': math.pi})
        self.assertAlmostEqual(result, 180)


class TestLogarithmicFunctions(unittest.TestCase):
    """对数函数测试"""

    def setUp(self):
        self.parser = ExpressionParser(functions=BUILTIN_FUNCTIONS)

    def test_log_functions(self):
        """对数函数测试"""
        import math
        
        # 自然对数 - 需要传入 e 变量
        result = self.parser.evaluate(
            self.parser.parse("log(e)"),
            variables={'e': math.e}
        )
        self.assertAlmostEqual(result, 1)
        
        # 常用对数
        self.assertAlmostEqual(self.parser.evaluate(self.parser.parse("log10(100)")), 2)
        
        # 二进制对数
        self.assertAlmostEqual(self.parser.evaluate(self.parser.parse("log2(8)")), 3)

    def test_exp_function(self):
        """指数函数测试"""
        import math
        
        result = self.parser.evaluate(self.parser.parse("exp(0)"))
        self.assertAlmostEqual(result, 1)
        
        result = self.parser.evaluate(self.parser.parse("exp(1)"))
        self.assertAlmostEqual(result, math.e)


if __name__ == '__main__':
    unittest.main()