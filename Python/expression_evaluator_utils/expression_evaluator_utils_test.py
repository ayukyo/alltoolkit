"""
expression_evaluator_utils 测试套件

测试覆盖：
- 基础数学运算
- 比较和逻辑运算
- 三元表达式
- 变量和函数
- 错误处理
- 边界情况
"""

import sys
import os
import math
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    ExpressionEvaluator,
    evaluate,
    validate,
    get_variables,
    Lexer,
    Parser,
    TokenType,
)


class TestLexer(unittest.TestCase):
    """词法分析器测试"""
    
    def test_tokenize_number(self):
        """测试数字Tokenize"""
        lexer = Lexer("42")
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 2)  # NUMBER + EOF
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, 42)
    
    def test_tokenize_float(self):
        """测试浮点数Tokenize"""
        lexer = Lexer("3.14159")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertAlmostEqual(tokens[0].value, 3.14159)
    
    def test_tokenize_scientific_notation(self):
        """测试科学计数法"""
        lexer = Lexer("1.5e10")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].value, 1.5e10)
    
    def test_tokenize_string(self):
        """测试字符串Tokenize"""
        lexer = Lexer('"hello world"')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, "hello world")
    
    def test_tokenize_single_quotes(self):
        """测试单引号字符串"""
        lexer = Lexer("'hello'")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].value, "hello")
    
    def test_tokenize_identifier(self):
        """测试标识符Tokenize"""
        lexer = Lexer("variable_name")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].value, "variable_name")
    
    def test_tokenize_operators(self):
        """测试运算符Tokenize"""
        lexer = Lexer("+-*/%^")
        tokens = lexer.tokenize()
        operators = [t.value for t in tokens[:-1]]  # 排除EOF
        self.assertEqual(operators, ['+', '-', '*', '/', '%', '^'])
    
    def test_tokenize_comparison(self):
        """测试比较运算符Tokenize"""
        lexer = Lexer("== != < > <= >=")
        tokens = lexer.tokenize()
        operators = [t.value for t in tokens[:-1]]
        self.assertEqual(operators, ['==', '!=', '<', '>', '<=', '>='])
    
    def test_tokenize_logical(self):
        """测试逻辑运算符Tokenize"""
        lexer = Lexer("&& ||")
        tokens = lexer.tokenize()
        operators = [t.value for t in tokens[:-1]]
        self.assertEqual(operators, ['&&', '||'])
    
    def test_tokenize_parentheses(self):
        """测试括号Tokenize"""
        lexer = Lexer("(a + b)")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.LPAREN)
        self.assertEqual(tokens[4].type, TokenType.RPAREN)


class TestParser(unittest.TestCase):
    """语法分析器测试"""
    
    def test_parse_simple_expression(self):
        """测试简单表达式解析"""
        lexer = Lexer("2 + 3")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)
    
    def test_parse_function_call(self):
        """测试函数调用解析"""
        lexer = Lexer("sin(x)")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)
    
    def test_parse_ternary(self):
        """测试三元表达式解析"""
        lexer = Lexer("a ? b : c")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)


class TestBasicArithmetic(unittest.TestCase):
    """基础算术运算测试"""
    
    def setUp(self):
        self.evaluator = ExpressionEvaluator()
    
    def test_addition(self):
        """测试加法"""
        self.assertEqual(self.evaluator.evaluate("2 + 3"), 5)
        self.assertEqual(self.evaluator.evaluate("0 + 0"), 0)
        self.assertEqual(self.evaluator.evaluate("-5 + 10"), 5)
    
    def test_subtraction(self):
        """测试减法"""
        self.assertEqual(self.evaluator.evaluate("10 - 3"), 7)
        self.assertEqual(self.evaluator.evaluate("5 - 5"), 0)
        self.assertEqual(self.evaluator.evaluate("3 - 10"), -7)
    
    def test_multiplication(self):
        """测试乘法"""
        self.assertEqual(self.evaluator.evaluate("4 * 5"), 20)
        self.assertEqual(self.evaluator.evaluate("0 * 100"), 0)
        self.assertEqual(self.evaluator.evaluate("-3 * 4"), -12)
    
    def test_division(self):
        """测试除法"""
        self.assertEqual(self.evaluator.evaluate("10 / 2"), 5)
        self.assertEqual(self.evaluator.evaluate("7 / 2"), 3.5)
        self.assertAlmostEqual(self.evaluator.evaluate("1 / 3"), 0.333333333, places=6)
    
    def test_modulo(self):
        """测试取模"""
        self.assertEqual(self.evaluator.evaluate("10 % 3"), 1)
        self.assertEqual(self.evaluator.evaluate("15 % 5"), 0)
        self.assertEqual(self.evaluator.evaluate("7 % 2"), 1)
    
    def test_power(self):
        """测试幂运算"""
        self.assertEqual(self.evaluator.evaluate("2 ^ 3"), 8)
        self.assertEqual(self.evaluator.evaluate("3 ^ 2"), 9)
        self.assertAlmostEqual(self.evaluator.evaluate("2 ^ 0.5"), 1.414213562, places=6)
    
    def test_operator_precedence(self):
        """测试运算符优先级"""
        self.assertEqual(self.evaluator.evaluate("2 + 3 * 4"), 14)
        self.assertEqual(self.evaluator.evaluate("(2 + 3) * 4"), 20)
        self.assertEqual(self.evaluator.evaluate("10 - 2 * 3"), 4)
        self.assertEqual(self.evaluator.evaluate("2 ^ 3 * 2"), 16)  # 右结合: 2^(3*2) -> 64? No, ^ has higher precedence
        self.assertEqual(self.evaluator.evaluate("4 * 2 ^ 3"), 32)  # 4 * 8
    
    def test_unary_minus(self):
        """测试一元负号"""
        self.assertEqual(self.evaluator.evaluate("-5"), -5)
        self.assertEqual(self.evaluator.evaluate("--5"), 5)
        self.assertEqual(self.evaluator.evaluate("-(-5)"), 5)
    
    def test_unary_plus(self):
        """测试一元正号"""
        self.assertEqual(self.evaluator.evaluate("+5"), 5)
        self.assertEqual(self.evaluator.evaluate("+-5"), -5)


class TestComparisonOperators(unittest.TestCase):
    """比较运算符测试"""
    
    def setUp(self):
        self.evaluator = ExpressionEvaluator()
    
    def test_equal(self):
        """测试相等比较"""
        self.assertTrue(self.evaluator.evaluate("5 == 5"))
        self.assertFalse(self.evaluator.evaluate("5 == 6"))
        self.assertTrue(self.evaluator.evaluate("'hello' == 'hello'"))
    
    def test_not_equal(self):
        """测试不等比较"""
        self.assertTrue(self.evaluator.evaluate("5 != 6"))
        self.assertFalse(self.evaluator.evaluate("5 != 5"))
    
    def test_less_than(self):
        """测试小于比较"""
        self.assertTrue(self.evaluator.evaluate("3 < 5"))
        self.assertFalse(self.evaluator.evaluate("5 < 5"))
        self.assertFalse(self.evaluator.evaluate("6 < 5"))
    
    def test_greater_than(self):
        """测试大于比较"""
        self.assertTrue(self.evaluator.evaluate("5 > 3"))
        self.assertFalse(self.evaluator.evaluate("5 > 5"))
        self.assertFalse(self.evaluator.evaluate("3 > 5"))
    
    def test_less_equal(self):
        """测试小于等于"""
        self.assertTrue(self.evaluator.evaluate("3 <= 5"))
        self.assertTrue(self.evaluator.evaluate("5 <= 5"))
        self.assertFalse(self.evaluator.evaluate("6 <= 5"))
    
    def test_greater_equal(self):
        """测试大于等于"""
        self.assertTrue(self.evaluator.evaluate("5 >= 3"))
        self.assertTrue(self.evaluator.evaluate("5 >= 5"))
        self.assertFalse(self.evaluator.evaluate("3 >= 5"))


class TestLogicalOperators(unittest.TestCase):
    """逻辑运算符测试"""
    
    def setUp(self):
        self.evaluator = ExpressionEvaluator()
    
    def test_and(self):
        """测试逻辑与"""
        self.assertTrue(self.evaluator.evaluate("true && true"))
        self.assertFalse(self.evaluator.evaluate("true && false"))
        self.assertFalse(self.evaluator.evaluate("false && true"))
        self.assertFalse(self.evaluator.evaluate("false && false"))
    
    def test_or(self):
        """测试逻辑或"""
        self.assertTrue(self.evaluator.evaluate("true || true"))
        self.assertTrue(self.evaluator.evaluate("true || false"))
        self.assertTrue(self.evaluator.evaluate("false || true"))
        self.assertFalse(self.evaluator.evaluate("false || false"))
    
    def test_not(self):
        """测试逻辑非"""
        self.assertFalse(self.evaluator.evaluate("!true"))
        self.assertTrue(self.evaluator.evaluate("!false"))
        self.assertTrue(self.evaluator.evaluate("!0"))
        self.assertFalse(self.evaluator.evaluate("!1"))
    
    def test_short_circuit_and(self):
        """测试逻辑与短路求值"""
        # 在Python中，and/or会返回最后一个求值的值
        result = self.evaluator.evaluate("false && (1/0)")
        self.assertFalse(result)
    
    def test_short_circuit_or(self):
        """测试逻辑或短路求值"""
        result = self.evaluator.evaluate("true || (1/0)")
        self.assertTrue(result)


class TestTernaryExpression(unittest.TestCase):
    """三元表达式测试"""
    
    def setUp(self):
        self.evaluator = ExpressionEvaluator()
    
    def test_simple_ternary(self):
        """测试简单三元表达式"""
        self.assertEqual(self.evaluator.evaluate("1 ? 'yes' : 'no'"), "yes")
        self.assertEqual(self.evaluator.evaluate("0 ? 'yes' : 'no'"), "no")
    
    def test_nested_ternary(self):
        """测试嵌套三元表达式"""
        expr = "x > 90 ? 'A' : (x > 80 ? 'B' : 'C')"
        self.assertEqual(self.evaluator.evaluate(expr, x=95), "A")
        self.assertEqual(self.evaluator.evaluate(expr, x=85), "B")
        self.assertEqual(self.evaluator.evaluate(expr, x=70), "C")
    
    def test_ternary_with_comparison(self):
        """测试带比较的三元表达式"""
        expr = "a > b ? a : b"
        self.assertEqual(self.evaluator.evaluate(expr, a=10, b=5), 10)
        self.assertEqual(self.evaluator.evaluate(expr, a=3, b=7), 7)


class TestVariables(unittest.TestCase):
    """变量测试"""
    
    def setUp(self):
        self.evaluator = ExpressionEvaluator()
    
    def test_single_variable(self):
        """测试单个变量"""
        self.evaluator.set_variable("x", 10)
        self.assertEqual(self.evaluator.evaluate("x"), 10)
    
    def test_multiple_variables(self):
        """测试多个变量"""
        self.evaluator.set_variable("x", 10)
        self.evaluator.set_variable("y", 5)
        self.assertEqual(self.evaluator.evaluate("x + y"), 15)
        self.assertEqual(self.evaluator.evaluate("x * y"), 50)
    
    def test_inline_variables(self):
        """测试内联变量"""
        result = self.evaluator.evaluate("a + b * c", a=2, b=3, c=4)
        self.assertEqual(result, 14)
    
    def test_builtin_constants(self):
        """测试内置常量"""
        self.assertAlmostEqual(self.evaluator.evaluate("pi"), math.pi)
        self.assertAlmostEqual(self.evaluator.evaluate("e"), math.e)
        self.assertTrue(self.evaluator.evaluate("true"))
        self.assertFalse(self.evaluator.evaluate("false"))
        self.assertIsNone(self.evaluator.evaluate("null"))
    
    def test_undefined_variable(self):
        """测试未定义变量"""
        with self.assertRaises(NameError):
            self.evaluator.evaluate("undefined_var")


class TestFunctions(unittest.TestCase):
    """函数测试"""
    
    def setUp(self):
        self.evaluator = ExpressionEvaluator()
    
    def test_trigonometric_functions(self):
        """测试三角函数"""
        self.assertAlmostEqual(self.evaluator.evaluate("sin(0)"), 0)
        self.assertAlmostEqual(self.evaluator.evaluate("cos(0)"), 1)
        self.assertAlmostEqual(self.evaluator.evaluate("sin(pi / 2)"), 1, places=6)
        self.assertAlmostEqual(self.evaluator.evaluate("cos(pi)"), -1, places=6)
    
    def test_sqrt(self):
        """测试平方根"""
        self.assertEqual(self.evaluator.evaluate("sqrt(4)"), 2)
        self.assertEqual(self.evaluator.evaluate("sqrt(9)"), 3)
        self.assertAlmostEqual(self.evaluator.evaluate("sqrt(2)"), 1.414213562, places=6)
    
    def test_abs(self):
        """测试绝对值"""
        self.assertEqual(self.evaluator.evaluate("abs(-5)"), 5)
        self.assertEqual(self.evaluator.evaluate("abs(5)"), 5)
        self.assertEqual(self.evaluator.evaluate("abs(0)"), 0)
    
    def test_floor_ceil_round(self):
        """测试取整函数"""
        self.assertEqual(self.evaluator.evaluate("floor(3.7)"), 3)
        self.assertEqual(self.evaluator.evaluate("ceil(3.2)"), 4)
        self.assertEqual(self.evaluator.evaluate("round(3.5)"), 4)
        self.assertEqual(self.evaluator.evaluate("round(3.4)"), 3)
    
    def test_min_max(self):
        """测试最小最大值"""
        self.assertEqual(self.evaluator.evaluate("min(1, 2, 3)"), 1)
        self.assertEqual(self.evaluator.evaluate("max(1, 2, 3)"), 3)
        self.assertEqual(self.evaluator.evaluate("min(5, 2)"), 2)
        self.assertEqual(self.evaluator.evaluate("max(5, 2)"), 5)
    
    def test_log_functions(self):
        """测试对数函数"""
        self.assertAlmostEqual(self.evaluator.evaluate("log(e)"), 1, places=6)
        self.assertAlmostEqual(self.evaluator.evaluate("log10(100)"), 2)
        self.assertAlmostEqual(self.evaluator.evaluate("log2(8)"), 3)
    
    def test_exp(self):
        """测试指数函数"""
        self.assertAlmostEqual(self.evaluator.evaluate("exp(0)"), 1)
        self.assertAlmostEqual(self.evaluator.evaluate("exp(1)"), math.e, places=6)
    
    def test_pow_function(self):
        """测试pow函数"""
        self.assertEqual(self.evaluator.evaluate("pow(2, 3)"), 8)
        self.assertEqual(self.evaluator.evaluate("pow(3, 2)"), 9)
    
    def test_type_conversion(self):
        """测试类型转换"""
        self.assertEqual(self.evaluator.evaluate("int(3.7)"), 3)
        self.assertEqual(self.evaluator.evaluate("float(3)"), 3.0)
        self.assertEqual(self.evaluator.evaluate("str(123)"), "123")
        self.assertTrue(self.evaluator.evaluate("bool(1)"))
        self.assertFalse(self.evaluator.evaluate("bool(0)"))
    
    def test_custom_function(self):
        """测试自定义函数"""
        self.evaluator.set_function("double", lambda x: x * 2)
        self.assertEqual(self.evaluator.evaluate("double(5)"), 10)
        
        self.evaluator.set_function("add", lambda a, b: a + b)
        self.assertEqual(self.evaluator.evaluate("add(3, 4)"), 7)
    
    def test_nested_function_calls(self):
        """测试嵌套函数调用"""
        result = self.evaluator.evaluate("sqrt(abs(-16))")
        self.assertEqual(result, 4)
        
        result = self.evaluator.evaluate("round(sin(pi / 2))")
        self.assertEqual(result, 1)
    
    def test_function_in_expression(self):
        """测试函数在表达式中"""
        result = self.evaluator.evaluate("sqrt(x) + sqrt(y)", x=16, y=25)
        self.assertEqual(result, 9)


class TestStringOperations(unittest.TestCase):
    """字符串操作测试"""
    
    def setUp(self):
        self.evaluator = ExpressionEvaluator()
    
    def test_string_literal(self):
        """测试字符串字面量"""
        self.assertEqual(self.evaluator.evaluate("'hello'"), "hello")
        self.assertEqual(self.evaluator.evaluate('"world"'), "world")
    
    def test_string_comparison(self):
        """测试字符串比较"""
        self.assertTrue(self.evaluator.evaluate("'hello' == 'hello'"))
        self.assertFalse(self.evaluator.evaluate("'hello' == 'world'"))
    
    def test_string_concatenation(self):
        """测试字符串拼接"""
        result = self.evaluator.evaluate("'hello' + ' ' + 'world'")
        self.assertEqual(result, "hello world")
    
    def test_string_variable(self):
        """测试字符串变量"""
        self.evaluator.set_variable("name", "Alice")
        self.assertEqual(self.evaluator.evaluate("'Hello, ' + name + '!'"), "Hello, Alice!")


class TestErrorHandling(unittest.TestCase):
    """错误处理测试"""
    
    def setUp(self):
        self.evaluator = ExpressionEvaluator()
    
    def test_syntax_error(self):
        """测试语法错误"""
        with self.assertRaises(SyntaxError):
            self.evaluator.evaluate("(2 + 3")
        
        # 注意：解析器允许一元运算符，所以 "2 + + 3" 实际上是有效的（= 5）
        # 测试其他语法错误
        with self.assertRaises(SyntaxError):
            self.evaluator.evaluate("2 + * 3")
    
    def test_division_by_zero(self):
        """测试除零错误"""
        with self.assertRaises(ZeroDivisionError):
            self.evaluator.evaluate("1 / 0")
    
    def test_undefined_function(self):
        """测试未定义函数"""
        with self.assertRaises(NameError):
            self.evaluator.evaluate("unknown_func()")
    
    def test_wrong_argument_count(self):
        """测试参数数量错误"""
        with self.assertRaises(TypeError):
            self.evaluator.evaluate("sqrt(1, 2)")


class TestValidateFunction(unittest.TestCase):
    """验证函数测试"""
    
    def test_valid_expression(self):
        """测试有效表达式"""
        is_valid, error = validate("2 + 3 * 4")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_invalid_expression(self):
        """测试无效表达式"""
        # 注意："2 + + 3" 实际上是有效的（一元加号）
        is_valid, error = validate("2 + * 3")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_valid_complex_expression(self):
        """测试复杂有效表达式"""
        is_valid, error = validate("x > 0 ? sqrt(x) : 0")
        self.assertTrue(is_valid)


class TestGetVariables(unittest.TestCase):
    """获取变量测试"""
    
    def test_get_variables_simple(self):
        """测试获取简单变量"""
        variables = get_variables("x + y")
        self.assertEqual(set(variables), {"x", "y"})
    
    def test_get_variables_complex(self):
        """测试获取复杂变量"""
        # 注意："e" 是内置常量，不会被收集为变量
        variables = get_variables("a * b + c / d - f")
        self.assertEqual(set(variables), {"a", "b", "c", "d", "f"})
    
    def test_get_variables_with_functions(self):
        """测试获取带函数的变量"""
        variables = get_variables("sqrt(x) + sin(y)")
        self.assertEqual(set(variables), {"x", "y"})
    
    def test_get_variables_ignores_builtins(self):
        """测试忽略内置常量"""
        variables = get_variables("pi * r ^ 2")
        self.assertEqual(set(variables), {"r"})
    
    def test_get_variables_no_variables(self):
        """测试无变量"""
        variables = get_variables("2 + 3 * 4")
        self.assertEqual(variables, [])


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_evaluate_function(self):
        """测试evaluate便捷函数"""
        result = evaluate("2 + 3 * 4")
        self.assertEqual(result, 14)
        
        result = evaluate("x + y", x=10, y=5)
        self.assertEqual(result, 15)


class TestComplexExpressions(unittest.TestCase):
    """复杂表达式测试"""
    
    def setUp(self):
        self.evaluator = ExpressionEvaluator()
    
    def test_quadratic_formula(self):
        """测试二次方程求根公式"""
        # x = (-b + sqrt(b^2 - 4ac)) / 2a
        a, b, c = 1, -5, 6
        self.evaluator.set_variable("a", a)
        self.evaluator.set_variable("b", b)
        self.evaluator.set_variable("c", c)
        
        discriminant_expr = "b ^ 2 - 4 * a * c"
        discriminant = self.evaluator.evaluate(discriminant_expr)
        self.assertEqual(discriminant, 1)
        
        root_expr = "(-b + sqrt(b ^ 2 - 4 * a * c)) / (2 * a)"
        root = self.evaluator.evaluate(root_expr)
        self.assertEqual(root, 3)
    
    def test_bmi_calculation(self):
        """测试BMI计算"""
        # BMI = weight / height^2
        self.evaluator.set_variable("weight", 70)
        self.evaluator.set_variable("height", 1.75)
        
        bmi = self.evaluator.evaluate("weight / (height ^ 2)")
        self.assertAlmostEqual(bmi, 22.857, places=3)
    
    def test_temperature_conversion(self):
        """测试温度转换"""
        # F = C * 9/5 + 32
        self.evaluator.set_variable("celsius", 25)
        fahrenheit = self.evaluator.evaluate("celsius * 9 / 5 + 32")
        self.assertEqual(fahrenheit, 77)
    
    def test_compound_interest(self):
        """测试复利计算"""
        # A = P * (1 + r/n)^(n*t)
        self.evaluator.set_variable("P", 1000)
        self.evaluator.set_variable("r", 0.05)
        self.evaluator.set_variable("n", 12)
        self.evaluator.set_variable("t", 10)
        
        amount = self.evaluator.evaluate("P * (1 + r / n) ^ (n * t)")
        self.assertAlmostEqual(amount, 1647.009, places=2)
    
    def test_grade_assignment(self):
        """测试成绩等级"""
        expr = "score >= 90 ? 'A' : (score >= 80 ? 'B' : (score >= 70 ? 'C' : (score >= 60 ? 'D' : 'F')))"
        
        self.assertEqual(self.evaluator.evaluate(expr, score=95), "A")
        self.assertEqual(self.evaluator.evaluate(expr, score=85), "B")
        self.assertEqual(self.evaluator.evaluate(expr, score=75), "C")
        self.assertEqual(self.evaluator.evaluate(expr, score=65), "D")
        self.assertEqual(self.evaluator.evaluate(expr, score=55), "F")


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def setUp(self):
        self.evaluator = ExpressionEvaluator()
    
    def test_empty_expression(self):
        """测试空表达式"""
        with self.assertRaises((SyntaxError, IndexError)):
            self.evaluator.evaluate("")
    
    def test_whitespace_only(self):
        """测试只有空格"""
        with self.assertRaises((SyntaxError, IndexError)):
            self.evaluator.evaluate("   ")
    
    def test_very_long_expression(self):
        """测试超长表达式"""
        expr = " + ".join([str(i) for i in range(100)])
        result = self.evaluator.evaluate(expr)
        self.assertEqual(result, sum(range(100)))
    
    def test_deeply_nested_parentheses(self):
        """测试深层嵌套括号"""
        expr = "((((" + " + ".join([str(i) for i in range(10)]) + "))))"
        result = self.evaluator.evaluate(expr)
        self.assertEqual(result, sum(range(10)))
    
    def test_negative_numbers(self):
        """测试负数"""
        self.assertEqual(self.evaluator.evaluate("-1"), -1)
        self.assertEqual(self.evaluator.evaluate("-1 + -2"), -3)
        self.assertEqual(self.evaluator.evaluate("5 + -3"), 2)
    
    def test_floating_point_precision(self):
        """测试浮点精度"""
        result = self.evaluator.evaluate("0.1 + 0.2")
        self.assertAlmostEqual(result, 0.3, places=10)
    
    def test_very_large_numbers(self):
        """测试大数"""
        result = self.evaluator.evaluate("1e100")
        self.assertEqual(result, 1e100)
    
    def test_infinity(self):
        """测试无穷大"""
        result = self.evaluator.evaluate("inf")
        self.assertTrue(math.isinf(result))


if __name__ == "__main__":
    unittest.main(verbosity=2)