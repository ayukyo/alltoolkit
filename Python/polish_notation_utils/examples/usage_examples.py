#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Polish Notation Utilities Examples
================================================
示例展示波兰表达式工具的各种用法。

Author: AllToolkit Contributors
License: MIT
"""

import sys
sys.path.insert(0, '..')

from mod import (
    PolishNotation,
    infix_to_postfix,
    infix_to_prefix,
    evaluate_postfix,
    evaluate_prefix,
    evaluate_infix,
)


def example_basic_conversion():
    """基础转换示例"""
    print("=" * 50)
    print("基础表达式转换示例")
    print("=" * 50)
    
    expressions = [
        "3 + 4",
        "3 + 4 * 2",
        "(3 + 4) * 2",
        "a + b * c - d",
        "2 ^ 3 ^ 2",
        "10 / 2 + 3 * 4 - 5",
    ]
    
    pn = PolishNotation()
    
    for expr in expressions:
        postfix = pn.infix_to_postfix(expr)
        prefix = pn.infix_to_prefix(expr)
        print(f"\n中缀表达式: {expr}")
        print(f"后缀表达式 (RPN): {postfix}")
        print(f"前缀表达式 (波兰): {prefix}")


def example_evaluation():
    """求值示例"""
    print("\n" + "=" * 50)
    print("表达式求值示例")
    print("=" * 50)
    
    pn = PolishNotation()
    
    # 中缀求值
    expressions = [
        "3 + 4 * 2",
        "(3 + 4) * 2",
        "10 / 2 + 3 * 4 - 5",
        "2 ^ 10",
        "2 ^ 3 ^ 2",
    ]
    
    print("\n中缀表达式求值:")
    for expr in expressions:
        result = pn.evaluate_infix(expr)
        print(f"  {expr} = {result}")
    
    # 后缀表达式求值
    print("\n后缀表达式求值:")
    postfix_exprs = [
        "3 4 2 * +",
        "3 4 + 2 *",
        "10 2 / 3 4 * + 5 -",
    ]
    for expr in postfix_exprs:
        result = pn.evaluate_postfix(expr)
        print(f"  {expr} = {result}")
    
    # 前缀表达式求值
    print("\n前缀表达式求值:")
    prefix_exprs = [
        "+ 3 * 4 2",
        "* + 3 4 2",
    ]
    for expr in prefix_exprs:
        result = pn.evaluate_prefix(expr)
        print(f"  {expr} = {result}")


def example_variables():
    """变量使用示例"""
    print("\n" + "=" * 50)
    print("带变量的表达式示例")
    print("=" * 50)
    
    pn = PolishNotation()
    
    expressions = [
        ("x + y", {'x': 10, 'y': 20}),
        ("x * y + z", {'x': 2, 'y': 3, 'z': 4}),
        ("a ^ 2 + b ^ 2", {'a': 3, 'b': 4}),
        ("price * quantity - discount", {'price': 100, 'quantity': 5, 'discount': 50}),
    ]
    
    print("\n带变量的表达式求值:")
    for expr, vars in expressions:
        result = pn.evaluate_infix(expr, vars)
        vars_str = ', '.join(f"{k}={v}" for k, v in vars.items())
        print(f"  {expr} (变量: {vars_str}) = {result}")


def example_constants():
    """数学常量示例"""
    print("\n" + "=" * 50)
    print("数学常量示例")
    print("=" * 50)
    
    pn = PolishNotation()
    
    expressions = [
        "pi * 2",
        "e ^ 2",
        "pi * r ^ 2",  # 圆面积公式
        "2 * pi * r",  # 圆周长公式
    ]
    
    print("\n使用数学常量:")
    for expr in expressions:
        if 'r' in expr:
            result = pn.evaluate_infix(expr, {'r': 5})
            print(f"  {expr} (r=5) = {result:.4f}")
        else:
            result = pn.evaluate_infix(expr)
            print(f"  {expr} = {result:.4f}")


def example_custom_operators():
    """自定义运算符示例"""
    print("\n" + "=" * 50)
    print("自定义运算符示例")
    print("=" * 50)
    
    pn = PolishNotation()
    
    # 添加整除运算符
    pn.add_operator('//', 3, 'left', lambda a, b: a // b)
    pn.add_operator('&', 3, 'left', lambda a, b: a & b)
    pn.add_operator('|', 2, 'left', lambda a, b: a | b)
    
    # 注意：tokenizer 需要能识别这些符号
    # 这里演示概念，实际需要更新 tokenizer
    
    print("\n添加自定义运算符后：")
    print("  整除运算符 '//': a // b")
    print("  位运算符 '&': a & b")
    print("  位运算符 '|': a | b")


def example_expression_validation():
    """表达式验证示例"""
    print("\n" + "=" * 50)
    print("表达式验证示例")
    print("=" * 50)
    
    pn = PolishNotation()
    
    expressions = [
        "3 + 4 * 2",
        "(3 + 4) * 2",
        "3 + )",
        "(3 + 4",
        "3 + + 4",
        "3 + 4 *",
    ]
    
    print("\n验证表达式语法:")
    for expr in expressions:
        is_valid, error = pn.validate_expression(expr)
        if is_valid:
            print(f"  '{expr}' ✓ 有效")
        else:
            print(f"  '{expr}' ✗ 无效: {error}")


def example_postfix_to_infix():
    """后缀转中缀示例"""
    print("\n" + "=" * 50)
    print("后缀转中缀示例")
    print("=" * 50)
    
    pn = PolishNotation()
    
    postfix_exprs = [
        "3 4 +",
        "3 4 2 * +",
        "3 4 + 2 *",
        "a b c * + d e / -",
    ]
    
    print("\n后缀表达式转中缀:")
    for expr in postfix_exprs:
        infix = pn.postfix_to_infix(expr)
        print(f"  {expr} → {infix}")


def example_calculator_scenario():
    """计算器应用场景"""
    print("\n" + "=" * 50)
    print("计算器应用场景")
    print("=" * 50)
    
    pn = PolishNotation()
    
    print("\n模拟计算器输入处理:")
    
    # 用户输入
    user_inputs = [
        "1 + 2 + 3 + 4 + 5",
        "100 * 0.05 + 100",  # 利息计算
        "5000 / 12",  # 月供计算
        "(100 - 20) * 0.8",  # 折扣计算
    ]
    
    for input_expr in user_inputs:
        # 转换为后缀（计算器内部处理）
        postfix = pn.infix_to_postfix(input_expr)
        # 求值
        result = pn.evaluate_infix(input_expr)
        print(f"\n  用户输入: {input_expr}")
        print(f"  内部处理: {postfix}")
        print(f"  计算结果: {result}")


def example_compiler_scenario():
    """编译器应用场景"""
    print("\n" + "=" * 50)
    print("编译器应用场景")
    print("=" * 50)
    
    pn = PolishNotation()
    
    print("\n表达式编译示例（生成前缀表达式）:")
    
    expressions = [
        "x + y * z",
        "a * b + c * d",
        "(a + b) * (c + d)",
        "x ^ 2 + 2 * x * y + y ^ 2",  # (x+y)^2
    ]
    
    for expr in expressions:
        prefix = pn.infix_to_prefix(expr)
        tokens = pn.tokenize(expr)
        print(f"\n  源表达式: {expr}")
        print(f"  编译结果: {prefix}")
        print(f"  Token序列: {[t.value for t in tokens]}")


def example_stack_based_calculation():
    """栈式计算演示"""
    print("\n" + "=" * 50)
    print("栈式计算演示")
    print("=" * 50)
    
    print("\n演示后缀表达式的栈式计算过程:")
    print("表达式: 3 + 4 * 2 → 后缀: 3 4 2 * +")
    
    steps = [
        ("读入 3", [3]),
        ("读入 4", [3, 4]),
        ("读入 2", [3, 4, 2]),
        ("遇到 *，弹出 2 和 4，计算 4*2=8，压入 8", [3, 8]),
        ("遇到 +，弹出 8 和 3，计算 3+8=11，压入 11", [11]),
        ("结束，结果为 11", [11]),
    ]
    
    print("\n计算步骤:")
    for step, stack in steps:
        print(f"  {step}")
        print(f"    栈状态: {stack}")
    
    # 验证
    pn = PolishNotation()
    result = pn.evaluate_postfix("3 4 2 * +")
    print(f"\n验证结果: {result}")


def example_comparison():
    """中缀、前缀、后缀对比"""
    print("\n" + "=" * 50)
    print("三种表达式形式对比")
    print("=" * 50)
    
    pn = PolishNotation()
    
    print("\n以 '3 + 4 * (2 - 1)' 为例:")
    
    expr = "3 + 4 * (2 - 1)"
    
    infix = expr
    postfix = pn.infix_to_postfix(expr)
    prefix = pn.infix_to_prefix(expr)
    result = pn.evaluate_infix(expr)
    
    print(f"\n  中缀表达式: {infix}")
    print(f"  前缀表达式: {prefix}")
    print(f"  后缀表达式: {postfix}")
    print(f"  计算结果:   {result}")
    
    print("\n特点对比:")
    print("  中缀: 人类易读，需要括号和优先级规则")
    print("  前缀: 运算符在前，适合递归求值")
    print("  后缀: 运算符在后，适合栈式求值，无括号")


def example_all_operators():
    """所有运算符演示"""
    print("\n" + "=" * 50)
    print("所有运算符演示")
    print("=" * 50)
    
    pn = PolishNotation()
    
    operators = {
        '+': "加法",
        '-': "减法",
        '*': "乘法",
        '/': "除法",
        '%': "模运算",
        '^': "幂运算",
    }
    
    print("\n支持的运算符:")
    for op, desc in operators.items():
        expr = f"10 {op} 3"
        try:
            result = pn.evaluate_infix(expr)
            print(f"  {op} ({desc}): {expr} = {result}")
        except Exception as e:
            print(f"  {op} ({desc}): {expr} = 错误: {e}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("AllToolkit - 波兰表达式工具示例")
    print("=" * 60)
    
    example_basic_conversion()
    example_evaluation()
    example_variables()
    example_constants()
    example_custom_operators()
    example_expression_validation()
    example_postfix_to_infix()
    example_calculator_scenario()
    example_compiler_scenario()
    example_stack_based_calculation()
    example_comparison()
    example_all_operators()
    
    print("\n" + "=" * 60)
    print("示例演示完成")
    print("=" * 60)


if __name__ == '__main__':
    main()