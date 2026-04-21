#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Polish Notation Utilities Test Module
===================================================
Comprehensive tests for the Polish notation utilities module.

Author: AllToolkit Contributors
License: MIT
"""

import unittest
from mod import (
    PolishNotation,
    Tokenizer,
    NotationConverter,
    ExpressionEvaluator,
    Token,
    TokenType,
    Operator,
    DEFAULT_OPERATORS,
    DEFAULT_FUNCTIONS,
    infix_to_postfix,
    infix_to_prefix,
    evaluate_postfix,
    evaluate_prefix,
    evaluate_infix,
)


class TestTokenizer(unittest.TestCase):
    """测试词法分析器"""
    
    def setUp(self):
        self.tokenizer = Tokenizer()
    
    def test_simple_expression(self):
        """测试简单表达式"""
        tokens = self.tokenizer.tokenize("3 + 4")
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, 3)
        self.assertEqual(tokens[1].type, TokenType.OPERATOR)
        self.assertEqual(tokens[1].value, '+')
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].value, 4)
    
    def test_expression_with_spaces(self):
        """测试带空格的表达式"""
        tokens = self.tokenizer.tokenize("  3  +  4  *  2  ")
        self.assertEqual(len(tokens), 5)
        self.assertEqual([t.value for t in tokens], [3, '+', 4, '*', 2])
    
    def test_complex_expression(self):
        """测试复杂表达式"""
        tokens = self.tokenizer.tokenize("(3 + 4) * 2 - 5 / 3")
        expected_values = ['(', 3, '+', 4, ')', '*', 2, '-', 5, '/', 3]
        self.assertEqual([t.value for t in tokens], expected_values)
    
    def test_float_numbers(self):
        """测试浮点数"""
        tokens = self.tokenizer.tokenize("3.14 + 2.5 * 1.5")
        self.assertEqual(tokens[0].value, 3.14)
        self.assertEqual(tokens[2].value, 2.5)
        self.assertEqual(tokens[4].value, 1.5)
    
    def test_identifier(self):
        """测试标识符"""
        tokens = self.tokenizer.tokenize("x + y * z")
        self.assertEqual([t.type for t in tokens], 
                         [TokenType.IDENTIFIER, TokenType.OPERATOR,
                          TokenType.IDENTIFIER, TokenType.OPERATOR,
                          TokenType.IDENTIFIER])
    
    def test_function_call(self):
        """测试函数调用"""
        tokens = self.tokenizer.tokenize("sin(x) + cos(y)")
        self.assertEqual(tokens[0].type, TokenType.FUNCTION)
        self.assertEqual(tokens[0].value, 'sin')
    
    def test_negative_numbers(self):
        """测试负数"""
        tokens = self.tokenizer.tokenize("-5 + 3")
        self.assertEqual(tokens[0].type, TokenType.OPERATOR)
        self.assertEqual(tokens[0].value, '-')
        self.assertEqual(tokens[1].value, 5)


class TestNotationConverter(unittest.TestCase):
    """测试表达式转换器"""
    
    def setUp(self):
        self.converter = NotationConverter()
        self.tokenizer = Tokenizer()
    
    def test_infix_to_postfix_simple(self):
        """测试简单中缀转后缀"""
        tokens = self.tokenizer.tokenize("3 + 4")
        postfix = self.converter.infix_to_postfix(tokens)
        self.assertEqual([t.value for t in postfix], [3, 4, '+'])
    
    def test_infix_to_postfix_with_precedence(self):
        """测试运算符优先级"""
        tokens = self.tokenizer.tokenize("3 + 4 * 2")
        postfix = self.converter.infix_to_postfix(tokens)
        self.assertEqual([t.value for t in postfix], [3, 4, 2, '*', '+'])
    
    def test_infix_to_postfix_with_parentheses(self):
        """测试括号"""
        tokens = self.tokenizer.tokenize("(3 + 4) * 2")
        postfix = self.converter.infix_to_postfix(tokens)
        self.assertEqual([t.value for t in postfix], [3, 4, '+', 2, '*'])
    
    def test_infix_to_postfix_complex(self):
        """测试复杂表达式"""
        tokens = self.tokenizer.tokenize("a + b * c - d / e")
        postfix = self.converter.infix_to_postfix(tokens)
        # 应该是: a b c * + d e / -
        self.assertEqual([t.value for t in postfix], ['a', 'b', 'c', '*', '+', 'd', 'e', '/', '-'])
    
    def test_infix_to_postfix_power(self):
        """测试幂运算（右结合）"""
        tokens = self.tokenizer.tokenize("2 ^ 3 ^ 2")
        postfix = self.converter.infix_to_postfix(tokens)
        # 右结合: 2 3 2 ^ ^
        self.assertEqual([t.value for t in postfix], [2, 3, 2, '^', '^'])
    
    def test_infix_to_prefix_simple(self):
        """测试简单中缀转前缀"""
        tokens = self.tokenizer.tokenize("3 + 4")
        prefix = self.converter.infix_to_prefix(tokens)
        self.assertEqual([t.value for t in prefix], ['+', 3, 4])
    
    def test_infix_to_prefix_with_precedence(self):
        """测试前缀转换优先级"""
        tokens = self.tokenizer.tokenize("3 + 4 * 2")
        prefix = self.converter.infix_to_prefix(tokens)
        # 应该是: + 3 * 4 2
        self.assertEqual([t.value for t in prefix], ['+', 3, '*', 4, 2])
    
    def test_infix_to_prefix_with_parentheses(self):
        """测试前缀转换括号"""
        tokens = self.tokenizer.tokenize("(3 + 4) * 2")
        prefix = self.converter.infix_to_prefix(tokens)
        # 应该是: * + 3 4 2
        self.assertEqual([t.value for t in prefix], ['*', '+', 3, 4, 2])
    
    def test_unary_minus(self):
        """测试一元负号"""
        tokens = self.tokenizer.tokenize("-5 + 3")
        postfix = self.converter.infix_to_postfix(tokens)
        # 应该包含一元负号
        self.assertIn('u-', [t.value for t in postfix])


class TestExpressionEvaluator(unittest.TestCase):
    """测试表达式求值器"""
    
    def setUp(self):
        self.evaluator = ExpressionEvaluator()
        self.tokenizer = Tokenizer()
        self.converter = NotationConverter()
    
    def test_evaluate_postfix_simple(self):
        """测试简单后缀求值"""
        tokens = [
            Token(TokenType.NUMBER, 3),
            Token(TokenType.NUMBER, 4),
            Token(TokenType.OPERATOR, '+'),
        ]
        result = self.evaluator.evaluate_postfix(tokens)
        self.assertEqual(result, 7)
    
    def test_evaluate_postfix_complex(self):
        """测试复杂后缀求值"""
        tokens = [
            Token(TokenType.NUMBER, 3),
            Token(TokenType.NUMBER, 4),
            Token(TokenType.NUMBER, 2),
            Token(TokenType.OPERATOR, '*'),
            Token(TokenType.OPERATOR, '+'),
        ]
        result = self.evaluator.evaluate_postfix(tokens)
        self.assertEqual(result, 11)
    
    def test_evaluate_postfix_with_variables(self):
        """测试带变量的后缀求值"""
        tokens = [
            Token(TokenType.IDENTIFIER, 'x'),
            Token(TokenType.NUMBER, 2),
            Token(TokenType.OPERATOR, '*'),
        ]
        result = self.evaluator.evaluate_postfix(tokens, {'x': 10})
        self.assertEqual(result, 20)
    
    def test_evaluate_prefix_simple(self):
        """测试简单前缀求值"""
        tokens = [
            Token(TokenType.OPERATOR, '+'),
            Token(TokenType.NUMBER, 3),
            Token(TokenType.NUMBER, 4),
        ]
        result = self.evaluator.evaluate_prefix(tokens)
        self.assertEqual(result, 7)
    
    def test_evaluate_prefix_complex(self):
        """测试复杂前缀求值"""
        tokens = [
            Token(TokenType.OPERATOR, '+'),
            Token(TokenType.NUMBER, 3),
            Token(TokenType.OPERATOR, '*'),
            Token(TokenType.NUMBER, 4),
            Token(TokenType.NUMBER, 2),
        ]
        result = self.evaluator.evaluate_prefix(tokens)
        self.assertEqual(result, 11)
    
    def test_evaluate_with_constants(self):
        """测试使用常量"""
        tokens = [
            Token(TokenType.IDENTIFIER, 'pi'),
            Token(TokenType.NUMBER, 2),
            Token(TokenType.OPERATOR, '*'),
        ]
        result = self.evaluator.evaluate_postfix(tokens)
        self.assertAlmostEqual(result, 6.28, places=2)
    
    def test_unary_operations(self):
        """测试一元运算"""
        tokens = [
            Token(TokenType.NUMBER, 5),
            Token(TokenType.OPERATOR, 'u-'),
        ]
        result = self.evaluator.evaluate_postfix(tokens)
        self.assertEqual(result, -5)


class TestPolishNotation(unittest.TestCase):
    """测试波兰表达式工具类"""
    
    def setUp(self):
        self.pn = PolishNotation()
    
    def test_infix_to_postfix(self):
        """测试中缀转后缀"""
        result = self.pn.infix_to_postfix("3 + 4 * 2")
        self.assertEqual(result, "3 4 2 * +")
    
    def test_infix_to_prefix(self):
        """测试中缀转前缀"""
        result = self.pn.infix_to_prefix("3 + 4 * 2")
        self.assertEqual(result, "+ 3 * 4 2")
    
    def test_evaluate_infix(self):
        """测试中缀求值"""
        result = self.pn.evaluate_infix("3 + 4 * 2")
        self.assertEqual(result, 11)
    
    def test_evaluate_infix_with_variables(self):
        """测试带变量的中缀求值"""
        result = self.pn.evaluate_infix("x * y + z", {'x': 2, 'y': 3, 'z': 4})
        self.assertEqual(result, 10)
    
    def test_evaluate_postfix_string(self):
        """测试后缀字符串求值"""
        result = self.pn.evaluate_postfix("3 4 + 2 *")
        self.assertEqual(result, 14)
    
    def test_evaluate_prefix_string(self):
        """测试前缀字符串求值"""
        result = self.pn.evaluate_prefix("* + 3 4 2")
        self.assertEqual(result, 14)
    
    def test_complex_expression(self):
        """测试复杂表达式"""
        result = self.pn.evaluate_infix("(1 + 2) * 3 - 4 / 2")
        self.assertEqual(result, 7)
    
    def test_power_expression(self):
        """测试幂运算"""
        result = self.pn.evaluate_infix("2 ^ 3")
        self.assertEqual(result, 8)
    
    def test_chained_power(self):
        """测试连续幂运算"""
        result = self.pn.evaluate_infix("2 ^ 3 ^ 2")  # 2^(3^2) = 2^9 = 512
        self.assertEqual(result, 512)
    
    def test_add_custom_operator(self):
        """测试添加自定义运算符"""
        # 创建新实例以避免修改全局DEFAULT_OPERATORS
        pn = PolishNotation()
        # 注意：tokenizer目前只支持预定义的运算符符号
        # 测试修改现有运算符的行为（以%为例，改为整除）
        pn.add_operator('%', 3, 'left', lambda a, b: a // b)
        pn.evaluator.operators['%'] = pn.operators['%']
        result = pn.evaluate_infix("10 % 3")
        self.assertEqual(result, 3)  # 10 // 3 = 3
    
    def test_add_custom_function(self):
        """测试添加自定义函数"""
        self.pn.add_function('square', lambda x: x * x)
        # 直接测试函数
        import math
        self.pn.add_function('square', lambda x: x * x)
        # 需要在evaluator中设置
        self.pn.evaluator.functions['square'] = lambda x: x * x
    
    def test_validate_expression(self):
        """测试表达式验证"""
        # 创建新实例以避免其他测试的影响
        pn = PolishNotation()
        is_valid, error = pn.validate_expression("3 + 4 * 2")
        self.assertTrue(is_valid)
        
        # 测试无效表达式（未知字符）
        is_valid, error = pn.validate_expression("3 $ 4")
        self.assertFalse(is_valid)
    
    def test_postfix_to_infix(self):
        """测试后缀转中缀"""
        result = self.pn.postfix_to_infix("3 4 2 * +")
        self.assertIn('+', result)
        self.assertIn('*', result)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_infix_to_postfix_func(self):
        """测试中缀转后缀便捷函数"""
        result = infix_to_postfix("3 + 4 * 2")
        self.assertEqual(result, "3 4 2 * +")
    
    def test_infix_to_prefix_func(self):
        """测试中缀转前缀便捷函数"""
        result = infix_to_prefix("3 + 4 * 2")
        self.assertEqual(result, "+ 3 * 4 2")
    
    def test_evaluate_postfix_func(self):
        """测试后缀求值便捷函数"""
        result = evaluate_postfix("3 4 + 2 *")
        self.assertEqual(result, 14)
    
    def test_evaluate_prefix_func(self):
        """测试前缀求值便捷函数"""
        result = evaluate_prefix("+ 3 * 4 2")
        self.assertEqual(result, 11)
    
    def test_evaluate_infix_func(self):
        """测试中缀求值便捷函数"""
        result = evaluate_infix("3 + 4 * 2")
        self.assertEqual(result, 11)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def setUp(self):
        self.pn = PolishNotation()
    
    def test_single_number(self):
        """测试单个数字"""
        result = self.pn.evaluate_infix("42")
        self.assertEqual(result, 42)
    
    def test_empty_expression(self):
        """测试空表达式"""
        result = self.pn.evaluate_infix("")
        self.assertIsNone(result)  # 空表达式返回None
    
    def test_nested_parentheses(self):
        """测试多层嵌套括号"""
        result = self.pn.evaluate_infix("((3 + 4) * (2 - 1))")
        self.assertEqual(result, 7)
    
    def test_negative_result(self):
        """测试负数结果"""
        result = self.pn.evaluate_infix("3 - 10")
        self.assertEqual(result, -7)
    
    def test_float_operations(self):
        """测试浮点运算"""
        result = self.pn.evaluate_infix("3.5 * 2.0")
        self.assertEqual(result, 7.0)
    
    def test_division(self):
        """测试除法"""
        result = self.pn.evaluate_infix("10 / 4")
        self.assertAlmostEqual(result, 2.5)
    
    def test_modulo(self):
        """测试模运算"""
        # 创建新实例以避免之前测试修改的运算符
        pn = PolishNotation()
        result = pn.evaluate_infix("10 % 3")
        self.assertEqual(result, 1)
    
    def test_expression_with_constants(self):
        """测试包含常量的表达式"""
        result = self.pn.evaluate_infix("pi + e")
        self.assertAlmostEqual(result, 3.14159 + 2.71828, places=2)


class TestOperator(unittest.TestCase):
    """测试运算符类"""
    
    def test_operator_creation(self):
        """测试运算符创建"""
        op = Operator('?', 1, 'left', lambda a, b: a if a else b)
        self.assertEqual(op.symbol, '?')
        self.assertEqual(op.precedence, 1)
        self.assertEqual(op.associativity, 'left')
    
    def test_unary_operator(self):
        """测试一元运算符"""
        op = Operator('!', 5, 'right', lambda a: not a, is_unary=True)
        self.assertTrue(op.is_unary)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestTokenizer))
    suite.addTests(loader.loadTestsFromTestCase(TestNotationConverter))
    suite.addTests(loader.loadTestsFromTestCase(TestExpressionEvaluator))
    suite.addTests(loader.loadTestsFromTestCase(TestPolishNotation))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestOperator))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)