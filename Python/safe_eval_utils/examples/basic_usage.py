"""
Safe Expression Evaluator - 基础使用示例

演示安全表达式求值的基本用法。

作者：AllToolkit 自动生成
日期：2026-04-16
"""

import sys
sys.path.insert(0, '..')
from mod import (
    safe_eval,
    safe_eval_with_result,
    SafeEvaluator,
    validate_expression,
)


def main():
    print("=" * 60)
    print("Safe Expression Evaluator - 基础使用示例")
    print("=" * 60)
    
    # ==================== 简单数学运算 ====================
    print("\n【1. 简单数学运算】")
    
    expressions = [
        "2 + 3",
        "10 - 4",
        "3 * 4",
        "15 / 3",
        "17 // 3",
        "17 % 3",
        "2 ** 10",
        "sqrt(16)",
        "sin(pi/2)",
    ]
    
    for expr in expressions:
        result = safe_eval(expr)
        print(f"  {expr} = {result}")
    
    # ==================== 使用变量 ====================
    print("\n【2. 使用变量】")
    
    variables = {"x": 10, "y": 5, "name": "'Alice'", "age": 25}
    
    expressions = [
        ("x + y", "x + y"),
        ("x * y + x", "x * y + x"),
        ("x ** y", "x ** y"),
        ("x > y", "x > y"),
        ("age >= 18", "age >= 18"),
    ]
    
    for desc, expr in expressions:
        result = safe_eval(expr, variables=variables)
        print(f"  {expr} ({desc}) = {result}")
    
    # ==================== 布尔表达式 ====================
    print("\n【3. 布尔表达式】")
    
    expressions = [
        "True and False",
        "True or False",
        "not True",
        "5 > 3 and 2 < 4",
        "1 == 1 or 2 == 3",
        "True is True",
        "False is not True",
    ]
    
    for expr in expressions:
        result = safe_eval(expr)
        print(f"  {expr} = {result}")
    
    # ==================== 条件表达式 ====================
    print("\n【4. 条件表达式（三元运算符）】")
    
    expressions = [
        "5 if True else 3",
        "'yes' if 10 > 5 else 'no'",
        "1 if 1 > 2 else 2",
    ]
    
    for expr in expressions:
        result = safe_eval(expr)
        print(f"  {expr} = {result}")
    
    # ==================== 数据结构 ====================
    print("\n【5. 数据结构】")
    
    expressions = [
        "[1, 2, 3]",
        "(1, 2, 3)",
        "{'a': 1, 'b': 2}",
        "{1, 2, 3}",
        "[1, 2, 3][0]",
        "[1, 2, 3][1:3]",
        "'hello'[0]",
        "'hello'[1:4]",
    ]
    
    for expr in expressions:
        result = safe_eval(expr)
        print(f"  {expr} = {result}")
    
    # ==================== 函数调用 ====================
    print("\n【6. 函数调用】")
    
    expressions = [
        "max(1, 2, 3, 4, 5)",
        "min(1, 2, 3)",
        "abs(-10)",
        "round(3.14159, 2)",
        "len([1, 2, 3, 4])",
        "int(3.7)",
        "float('3.14')",
        "str(123)",
        "upper('hello')",
        "replace('hello world', 'world', 'python')",
    ]
    
    for expr in expressions:
        result = safe_eval(expr)
        print(f"  {expr} = {result}")
    
    # ==================== 创建求值器 ====================
    print("\n【7. 创建自定义求值器】")
    
    evaluator = SafeEvaluator()
    
    # 链式设置变量
    evaluator.set_variable("a", 10)
    evaluator.set_variable("b", 5)
    evaluator.set_variable("c", 2)
    
    # 自定义函数
    evaluator.set_function("cube", lambda x: x**3)
    evaluator.set_function("add", lambda x, y: x + y)
    
    print(f"  a + b + c = {evaluator.eval('a + b + c')}")
    print(f"  a * b - c = {evaluator.eval('a * b - c')}")
    print(f"  cube(a) = {evaluator.eval('cube(a)')}")
    print(f"  add(a, b) = {evaluator.eval('add(a, b)')}")
    
    # ==================== 安全求值 ====================
    print("\n【8. 安全求值（不抛出异常）】")
    
    test_cases = [
        "2 + 3",
        "unknown_variable",
        "1 / 0",
        "2 +",
    ]
    
    for expr in test_cases:
        result = safe_eval_with_result(expr)
        if result.success:
            print(f"  {expr} → 成功: {result.value}")
        else:
            print(f"  {expr} → 失败: {result.error} ({result.error_type})")
    
    # ==================== 表达式验证 ====================
    print("\n【9. 表达式验证】")
    
    expressions = [
        "2 + 3",
        "x + y",
        "2 +",
        "sin(pi/2)",
        "",
    ]
    
    for expr in expressions:
        valid, error = validate_expression(expr)
        status = "✓ 有效" if valid else f"✗ 无效: {error}"
        print(f"  '{expr}' → {status}")
    
    # ==================== 安全特性 ====================
    print("\n【10. 安全特性】")
    
    # 默认情况下不允许属性访问
    print("  属性访问禁用:")
    result = safe_eval_with_result("'hello'.upper()")
    print(f"    'hello'.upper() → {result.error}")
    
    # 启用属性访问
    print("  属性访问启用:")
    result = safe_eval("'hello'.upper()", allow_attributes=True)
    print(f"    'hello'.upper() → {result}")
    
    # 无法执行任意代码
    print("  代码执行保护:")
    result = safe_eval_with_result("exec('print(1)')")
    print(f"    exec('print(1)') → {result.error}")
    
    print("\n" + "=" * 60)
    print("示例完成")
    print("=" * 60)


if __name__ == "__main__":
    main()