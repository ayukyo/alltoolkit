"""
Safe Expression Evaluator - 测试套件

测试安全表达式求值功能。

作者：AllToolkit 自动生成
日期：2026-04-16
"""

import pytest
import math
from mod import (
    SafeEvaluator,
    safe_eval,
    safe_eval_with_result,
    validate_expression,
    create_evaluator,
    ExpressionParser,
    TemplateEvaluator,
    BatchEvaluator,
    ConditionEvaluator,
    MathEvaluator,
    StringEvaluator,
    EvalResult,
    EvalError,
    SyntaxError,
    NameError,
    TypeError_,
    SecurityError,
    DivisionByZeroError,
)


class TestSafeEvaluator:
    """SafeEvaluator 测试"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.evaluator = SafeEvaluator()
    
    # ==================== 基础运算测试 ====================
    
    def test_basic_arithmetic(self):
        """测试基础算术运算"""
        assert self.evaluator.eval("2 + 3") == 5
        assert self.evaluator.eval("10 - 4") == 6
        assert self.evaluator.eval("3 * 4") == 12
        assert self.evaluator.eval("15 / 3") == 5.0
        assert self.evaluator.eval("17 // 3") == 5
        assert self.evaluator.eval("17 % 3") == 2
        assert self.evaluator.eval("2 ** 3") == 8
    
    def test_operator_precedence(self):
        """测试运算符优先级"""
        assert self.evaluator.eval("2 + 3 * 4") == 14
        assert self.evaluator.eval("(2 + 3) * 4") == 20
        assert self.evaluator.eval("2 ** 3 ** 2") == 512  # 右结合
        assert self.evaluator.eval("10 - 4 - 2") == 4  # 左结合
    
    def test_unary_operators(self):
        """测试一元运算符"""
        assert self.evaluator.eval("-5") == -5
        assert self.evaluator.eval("+-5") == -5
        assert self.evaluator.eval("--5") == 5
        assert self.evaluator.eval("not True") is False
        assert self.evaluator.eval("not False") is True
        assert self.evaluator.eval("~5") == -6
    
    # ==================== 布尔运算测试 ====================
    
    def test_boolean_operators(self):
        """测试布尔运算符"""
        assert self.evaluator.eval("True and True") is True
        assert self.evaluator.eval("True and False") is False
        assert self.evaluator.eval("False and True") is False
        assert self.evaluator.eval("False or True") is True
        assert self.evaluator.eval("False or False") is False
        assert self.evaluator.eval("not True") is False
        assert self.evaluator.eval("not False") is True
    
    def test_boolean_short_circuit(self):
        """测试布尔短路求值"""
        # 如果短路，不会报错
        assert self.evaluator.eval("False and (1/0)") is False
        assert self.evaluator.eval("True or (1/0)") is True
    
    # ==================== 比较运算测试 ====================
    
    def test_comparison_operators(self):
        """测试比较运算符"""
        assert self.evaluator.eval("5 > 3") is True
        assert self.evaluator.eval("5 < 3") is False
        assert self.evaluator.eval("5 >= 5") is True
        assert self.evaluator.eval("5 <= 5") is True
        assert self.evaluator.eval("5 == 5") is True
        assert self.evaluator.eval("5 != 3") is True
    
    def test_chained_comparisons(self):
        """测试链式比较"""
        assert self.evaluator.eval("1 < 2 < 3") is True
        assert self.evaluator.eval("1 < 2 > 1") is True
        assert self.evaluator.eval("3 > 2 > 1") is True
        assert self.evaluator.eval("1 > 2 < 3") is False
    
    def test_is_isnot_operators(self):
        """测试 is 和 is not 运算符"""
        assert self.evaluator.eval("True is True") is True
        assert self.evaluator.eval("False is False") is True
        assert self.evaluator.eval("None is None") is True
        assert self.evaluator.eval("True is not False") is True
    
    def test_in_notin_operators(self):
        """测试 in 和 not in 运算符"""
        assert self.evaluator.eval("1 in [1, 2, 3]") is True
        assert self.evaluator.eval("4 in [1, 2, 3]") is False
        assert self.evaluator.eval("4 not in [1, 2, 3]") is True
        assert self.evaluator.eval("'a' in 'abc'") is True
    
    # ==================== 条件表达式测试 ====================
    
    def test_conditional_expression(self):
        """测试条件表达式（三元运算符）"""
        assert self.evaluator.eval("5 if True else 3") == 5
        assert self.evaluator.eval("5 if False else 3") == 3
        assert self.evaluator.eval("'yes' if 1 > 0 else 'no'") == 'yes'
    
    # ==================== 数据结构测试 ====================
    
    def test_list_literal(self):
        """测试列表字面量"""
        assert self.evaluator.eval("[1, 2, 3]") == [1, 2, 3]
        assert self.evaluator.eval("[]") == []
        assert self.evaluator.eval("[1, [2, 3], 4]") == [1, [2, 3], 4]
    
    def test_tuple_literal(self):
        """测试元组字面量"""
        assert self.evaluator.eval("(1, 2, 3)") == (1, 2, 3)
        assert self.evaluator.eval("(1,)") == (1,)
        assert self.evaluator.eval("()") == ()
    
    def test_dict_literal(self):
        """测试字典字面量"""
        assert self.evaluator.eval("{'a': 1, 'b': 2}") == {'a': 1, 'b': 2}
        assert self.evaluator.eval("{}") == {}
    
    def test_set_literal(self):
        """测试集合字面量"""
        assert self.evaluator.eval("{1, 2, 3}") == {1, 2, 3}
    
    def test_subscript_access(self):
        """测试下标访问"""
        assert self.evaluator.eval("[1, 2, 3][0]") == 1
        assert self.evaluator.eval("[1, 2, 3][-1]") == 3
        assert self.evaluator.eval("{'a': 1}['a']") == 1
        assert self.evaluator.eval("'hello'[0]") == 'h'
    
    def test_slice_access(self):
        """测试切片访问"""
        assert self.evaluator.eval("[1, 2, 3, 4, 5][1:3]") == [2, 3]
        assert self.evaluator.eval("[1, 2, 3, 4, 5][::2]") == [1, 3, 5]
        assert self.evaluator.eval("'hello'[1:4]") == 'ell'
    
    # ==================== 变量测试 ====================
    
    def test_variable_substitution(self):
        """测试变量替换"""
        assert self.evaluator.eval("x + y", variables={"x": 5, "y": 3}) == 8
        assert self.evaluator.eval("name", variables={"name": "test"}) == "test"
        assert self.evaluator.eval("items[0]", variables={"items": [1, 2, 3]}) == 1
    
    def test_set_variable(self):
        """测试设置变量"""
        ev = SafeEvaluator()
        ev.set_variable("x", 10)
        assert ev.eval("x") == 10
        
        # 链式调用
        ev.set_variable("y", 20).set_variable("z", 30)
        assert ev.eval("x + y + z") == 60
    
    def test_unknown_variable_error(self):
        """测试未知变量错误"""
        with pytest.raises(NameError):
            self.evaluator.eval("unknown_var")
    
    # ==================== 函数测试 ====================
    
    def test_builtin_math_functions(self):
        """测试内置数学函数"""
        assert self.evaluator.eval("abs(-5)") == 5
        assert self.evaluator.eval("round(3.7)") == 4
        assert self.evaluator.eval("min(1, 2, 3)") == 1
        assert self.evaluator.eval("max(1, 2, 3)") == 3
        assert self.evaluator.eval("sum(1, 2, 3)") == 6
    
    def test_trigonometric_functions(self):
        """测试三角函数"""
        assert abs(self.evaluator.eval("sin(0)") - 0) < 1e-10
        assert abs(self.evaluator.eval("cos(0)") - 1) < 1e-10
        assert abs(self.evaluator.eval("tan(0)") - 0) < 1e-10
    
    def test_log_functions(self):
        """测试对数函数"""
        assert abs(self.evaluator.eval("log(e)") - 1) < 1e-10
        assert abs(self.evaluator.eval("log10(100)") - 2) < 1e-10
        assert abs(self.evaluator.eval("log2(8)") - 3) < 1e-10
    
    def test_type_conversion_functions(self):
        """测试类型转换函数"""
        assert self.evaluator.eval("int(3.7)") == 3
        assert self.evaluator.eval("float('3.14')") == 3.14
        assert self.evaluator.eval("str(123)") == "123"
        assert self.evaluator.eval("bool(1)") is True
        assert self.evaluator.eval("len([1, 2, 3])") == 3
    
    def test_custom_function(self):
        """测试自定义函数"""
        ev = SafeEvaluator(functions={"square": lambda x: x**2})
        assert ev.eval("square(5)") == 25
        
        ev.set_function("cube", lambda x: x**3)
        assert ev.eval("cube(3)") == 27
    
    def test_unknown_function_error(self):
        """测试未知函数错误"""
        with pytest.raises(NameError):
            self.evaluator.eval("unknown_func(1)")
    
    # ==================== 常量测试 ====================
    
    def test_builtin_constants(self):
        """测试内置常量"""
        assert abs(self.evaluator.eval("pi") - math.pi) < 1e-10
        assert abs(self.evaluator.eval("e") - math.e) < 1e-10
        assert self.evaluator.eval("True") is True
        assert self.evaluator.eval("False") is False
        assert self.evaluator.eval("None") is None
    
    def test_custom_constant(self):
        """测试自定义常量"""
        ev = SafeEvaluator(constants={"MY_CONST": 42})
        assert ev.eval("MY_CONST") == 42
    
    # ==================== 安全性测试 ====================
    
    def test_no_code_execution(self):
        """测试不执行代码"""
        # 尝试执行代码应该失败
        with pytest.raises(EvalError):
            self.evaluator.eval("exec('print(1)')")
        
        with pytest.raises(EvalError):
            self.evaluator.eval("eval('1+1')")
        
        with pytest.raises(EvalError):
            self.evaluator.eval("import os")
    
    def test_attribute_access_disabled(self):
        """测试属性访问禁用"""
        with pytest.raises(SecurityError):
            self.evaluator.eval("'hello'.upper()")
        
        with pytest.raises(SecurityError):
            self.evaluator.eval("(1).__class__")
    
    def test_attribute_access_enabled(self):
        """测试属性访问启用"""
        ev = SafeEvaluator(allow_attributes=True)
        assert ev.eval("'hello'.upper()") == 'HELLO'
        assert ev.eval("'hello'.replace('l', 'L')") == 'heLLo'
    
    # ==================== 错误处理测试 ====================
    
    def test_division_by_zero(self):
        """测试除零错误"""
        with pytest.raises(DivisionByZeroError):
            self.evaluator.eval("1 / 0")
        
        with pytest.raises(DivisionByZeroError):
            self.evaluator.eval("1 // 0")
        
        with pytest.raises(DivisionByZeroError):
            self.evaluator.eval("1 % 0")
    
    def test_syntax_error(self):
        """测试语法错误"""
        from mod import EvalSyntaxError as SyntaxError
        with pytest.raises(SyntaxError):
            self.evaluator.eval("2 +")
        
        with pytest.raises(SyntaxError):
            self.evaluator.eval("import os")  # import is invalid in eval mode
        
        with pytest.raises(SyntaxError):
            self.evaluator.eval("")
    
    def test_type_error(self):
        """测试类型错误"""
        with pytest.raises(TypeError_):
            self.evaluator.eval("'a' + 1")
    
    # ==================== eval_safe 测试 ====================
    
    def test_eval_safe_success(self):
        """测试安全求值成功"""
        result = self.evaluator.eval_safe("2 + 3")
        assert result.success is True
        assert result.value == 5
        assert result.error is None
    
    def test_eval_safe_failure(self):
        """测试安全求值失败"""
        result = self.evaluator.eval_safe("unknown_var")
        assert result.success is False
        assert result.value is None
        assert result.error is not None
        assert result.error_type == "EvalNameError"


class TestConvenienceFunctions:
    """便捷函数测试"""
    
    def test_safe_eval(self):
        """测试 safe_eval 函数"""
        assert safe_eval("2 + 3") == 5
        assert safe_eval("x * y", variables={"x": 2, "y": 3}) == 6
    
    def test_safe_eval_custom_function(self):
        """测试 safe_eval 自定义函数"""
        result = safe_eval("square(5)", functions={"square": lambda x: x**2})
        assert result == 25
    
    def test_safe_eval_with_result(self):
        """测试 safe_eval_with_result 函数"""
        result = safe_eval_with_result("2 + 3")
        assert result.success is True
        assert result.value == 5
        
        result = safe_eval_with_result("unknown")
        assert result.success is False
    
    def test_validate_expression(self):
        """测试 validate_expression 函数"""
        valid, error = validate_expression("2 + 3")
        assert valid is True
        assert error is None
        
        valid, error = validate_expression("2 +")
        assert valid is False
        assert error is not None
    
    def test_create_evaluator(self):
        """测试 create_evaluator 函数"""
        ev = create_evaluator(variables={"x": 10})
        assert ev.eval("x + 5") == 15


class TestExpressionParser:
    """表达式解析器测试"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.parser = ExpressionParser()
    
    def test_get_variables(self):
        """测试获取变量"""
        vars = self.parser.get_variables("x + y * z")
        assert vars == {"x", "y", "z"}
        
        vars = self.parser.get_variables("pi + e")
        assert "pi" not in vars  # 内置常量
        assert "e" not in vars
    
    def test_get_functions(self):
        """测试获取函数"""
        funcs = self.parser.get_functions("sin(x) + cos(y)")
        assert funcs == {"sin", "cos"}
        
        funcs = self.parser.get_functions("max(1, 2, 3)")
        assert funcs == {"max"}
    
    def test_get_operators(self):
        """测试获取运算符"""
        ops = self.parser.get_operators("1 + 2 * 3")
        assert "+" in ops
        assert "*" in ops
        
        ops = self.parser.get_operators("a > b and c < d")
        assert ">" in ops
        assert "<" in ops
        assert "and" in ops
    
    def test_analyze(self):
        """测试表达式分析"""
        analysis = self.parser.analyze("sin(x) + cos(y)")
        assert analysis["valid"] is True
        assert "sin" in analysis["functions"]
        assert "cos" in analysis["functions"]
        assert "x" in analysis["variables"]
        assert "y" in analysis["variables"]


class TestTemplateEvaluator:
    """模板求值器测试"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.evaluator = TemplateEvaluator()
    
    def test_basic_template(self):
        """测试基础模板"""
        result = self.evaluator.eval("Result: ${2 + 3}")
        assert result == "Result: 5"
    
    def test_multiple_expressions(self):
        """测试多个表达式"""
        result = self.evaluator.eval("${1 + 2} + ${3 + 4} = ${1 + 2 + 3 + 4}")
        assert result == "3 + 7 = 10"
    
    def test_template_with_variables(self):
        """测试带变量的模板"""
        result = self.evaluator.eval("Hello, ${name}!", variables={"name": "World"})
        assert result == "Hello, World!"
    
    def test_template_error_handling(self):
        """测试模板错误处理"""
        result = self.evaluator.eval("Value: ${unknown_var}")
        assert "Error" in result


class TestBatchEvaluator:
    """批量求值器测试"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.evaluator = BatchEvaluator()
    
    def test_set_and_get(self):
        """测试设置和获取变量"""
        self.evaluator.set("x", 10)
        assert self.evaluator.get("x") == 10
    
    def test_eval_single(self):
        """测试单个求值"""
        self.evaluator.set("x", 10)
        assert self.evaluator.eval("x + 5") == 15
    
    def test_eval_all(self):
        """测试批量求值"""
        self.evaluator.set("x", 10)
        results = self.evaluator.eval_all(["x + 1", "x * 2", "x - 5"])
        assert results == [11, 20, 5]
    
    def test_eval_all_safe(self):
        """测试批量安全求值"""
        results = self.evaluator.eval_all_safe(["2 + 3", "unknown", "4 * 5"])
        assert results[0].success is True
        assert results[0].value == 5
        assert results[1].success is False
        assert results[2].success is True
        assert results[2].value == 20
    
    def test_chain_operations(self):
        """测试链式操作"""
        result = self.evaluator.set("x", 5).set("y", 3).eval("x + y")
        assert result == 8


class TestConditionEvaluator:
    """条件求值器测试"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.evaluator = ConditionEvaluator()
    
    def test_simple_condition(self):
        """测试简单条件"""
        assert self.evaluator.eval("True") is True
        assert self.evaluator.eval("False") is False
        assert self.evaluator.eval("5 > 3") is True
    
    def test_complex_condition(self):
        """测试复杂条件"""
        variables = {"age": 25, "score": 85, "status": "'active'"}
        assert self.evaluator.eval("age >= 18 and score > 60", variables) is True
        assert self.evaluator.eval("age < 18 or score < 60", variables) is False
    
    def test_check_all(self):
        """测试多条件检查"""
        conditions = ["x > 0", "x < 10", "x % 2 == 0"]
        
        assert self.evaluator.check_all(conditions, {"x": 4}, mode="and") is True
        assert self.evaluator.check_all(conditions, {"x": 12}, mode="and") is False
        assert self.evaluator.check_all(conditions, {"x": 5}, mode="or") is True
    
    def test_filter_list(self):
        """测试列表过滤"""
        items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = self.evaluator.filter_list(items, "item > 5")
        assert result == [6, 7, 8, 9, 10]
        
        result = self.evaluator.filter_list(items, "item % 2 == 0")
        assert result == [2, 4, 6, 8, 10]


class TestMathEvaluator:
    """数学求值器测试"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.evaluator = MathEvaluator()
    
    def test_math_constants(self):
        """测试数学常量"""
        assert abs(self.evaluator.eval("pi") - math.pi) < 1e-10
        assert abs(self.evaluator.eval("e") - math.e) < 1e-10
    
    def test_math_functions(self):
        """测试数学函数"""
        assert abs(self.evaluator.eval("sqrt(16)") - 4) < 1e-10
        assert abs(self.evaluator.eval("pow(2, 10)") - 1024) < 1e-10
        assert self.evaluator.eval("factorial(5)") == 120
        assert self.evaluator.eval("gcd(12, 8)") == 4
        assert self.evaluator.eval("lcm(4, 6)") == 12
    
    def test_complex_expression(self):
        """测试复杂表达式"""
        # 斜边计算
        result = self.evaluator.eval("sqrt(3**2 + 4**2)")
        assert abs(result - 5) < 1e-10
        
        # 复利公式
        ev = MathEvaluator(variables={"p": 1000, "r": 0.05, "n": 12, "t": 1})
        result = ev.eval("p * pow(1 + r/n, n*t)")
        assert abs(result - 1051.16) < 0.01


class TestStringEvaluator:
    """字符串求值器测试"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.evaluator = StringEvaluator()
    
    def test_string_functions(self):
        """测试字符串函数"""
        assert self.evaluator.eval("upper('hello')") == 'HELLO'
        assert self.evaluator.eval("lower('HELLO')") == 'hello'
        assert self.evaluator.eval("strip('  hello  ')") == 'hello'
    
    def test_string_replace(self):
        """测试字符串替换"""
        result = self.evaluator.eval("replace('hello world', 'world', 'python')")
        assert result == 'hello python'
    
    def test_string_split_join(self):
        """测试字符串分割和连接"""
        result = self.evaluator.eval("split('a,b,c', ',')")
        assert result == ['a', 'b', 'c']
        
        result = self.evaluator.eval("join('-', ['a', 'b', 'c'])")
        assert result == 'a-b-c'


class TestEdgeCases:
    """边界情况测试"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.evaluator = SafeEvaluator()
    
    def test_large_numbers(self):
        """测试大数"""
        result = self.evaluator.eval("10 ** 100")
        assert result == 10 ** 100
    
    def test_negative_numbers(self):
        """测试负数"""
        assert self.evaluator.eval("-5 + 3") == -2
        assert self.evaluator.eval("5 * -3") == -15
        assert self.evaluator.eval("-(-5)") == 5
    
    def test_floating_point_precision(self):
        """测试浮点精度"""
        result = self.evaluator.eval("0.1 + 0.2")
        assert abs(result - 0.3) < 1e-10
    
    def test_empty_expression(self):
        """测试空表达式"""
        with pytest.raises(SyntaxError):
            self.evaluator.eval("")
        
        with pytest.raises(SyntaxError):
            self.evaluator.eval("   ")
    
    def test_whitespace_handling(self):
        """测试空白处理"""
        assert self.evaluator.eval("  2  +  3  ") == 5
        assert self.evaluator.eval("\n2\n+\n3\n") == 5
    
    def test_unicode_strings(self):
        """测试 Unicode 字符串"""
        assert self.evaluator.eval("'你好'") == '你好'
        assert self.evaluator.eval("'hello' + '世界'") == 'hello世界'


class TestRecursionAndDepth:
    """递归和深度测试"""
    
    def test_deeply_nested_expression(self):
        """测试深层嵌套表达式"""
        expr = "1" + " + 1" * 50
        result = SafeEvaluator(max_recursion_depth=200).eval(expr)
        assert result == 51
    
    def test_max_recursion_depth(self):
        """测试最大递归深度"""
        # 创建一个中等深度的嵌套列表，超过自定义递归深度限制
        expr = "[" * 60 + "1" + "]" * 60
        with pytest.raises(EvalError):
            SafeEvaluator(max_recursion_depth=30, max_list_length=10000).eval(expr)


class TestListAndStringLength:
    """列表和字符串长度测试"""
    
    def test_max_list_length(self):
        """测试最大列表长度"""
        # 创建一个超出限制的列表
        expr = "[" + ", ".join(["1"] * 101) + "]"
        with pytest.raises(SecurityError):
            SafeEvaluator(max_list_length=100).eval(expr)
    
    def test_max_string_length(self):
        """测试最大字符串长度"""
        # 创建一个超出限制的字符串
        long_str = "a" * 1000001
        with pytest.raises(SecurityError):
            SafeEvaluator(max_string_length=1000000).eval(f"'{long_str}'")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])