"""
Safe Expression Evaluator - 高级使用示例

演示安全表达式求值的高级功能。

作者：AllToolkit 自动生成
日期：2026-04-16
"""

import sys
sys.path.insert(0, '..')
from mod import (
    MathEvaluator,
    StringEvaluator,
    ConditionEvaluator,
    TemplateEvaluator,
    BatchEvaluator,
    ExpressionParser,
    safe_eval,
)


def main():
    print("=" * 60)
    print("Safe Expression Evaluator - 高级使用示例")
    print("=" * 60)
    
    # ==================== MathEvaluator ====================
    print("\n【1. MathEvaluator - 数学专用求值器】")
    
    math_ev = MathEvaluator()
    
    expressions = [
        "sin(pi/2)",
        "cos(pi)",
        "tan(pi/4)",
        "sqrt(144)",
        "pow(2, 8)",
        "log(e)",
        "log10(1000)",
        "log2(1024)",
        "factorial(10)",
        "gcd(48, 18)",
        "lcm(12, 15)",
        "floor(3.7)",
        "ceil(3.2)",
        "abs(-25)",
    ]
    
    for expr in expressions:
        result = math_ev.eval(expr)
        print(f"  {expr} = {result}")
    
    # 复杂数学表达式
    print("\n  复杂表达式:")
    result = math_ev.eval("sqrt(3**2 + 4**2)")
    print(f"    sqrt(3² + 4²) = {result}")
    
    # ==================== StringEvaluator ====================
    print("\n【2. StringEvaluator - 字符串专用求值器】")
    
    str_ev = StringEvaluator()
    
    expressions = [
        "upper('hello world')",
        "lower('HELLO WORLD')",
        "capitalize('hello world')",
        "strip('  hello  ')",
        "replace('hello world', 'world', 'python')",
    ]
    
    for expr in expressions:
        result = str_ev.eval(expr)
        print(f"  {expr} = {result}")
    
    # ==================== ConditionEvaluator ====================
    print("\n【3. ConditionEvaluator - 条件专用求值器】")
    
    cond_ev = ConditionEvaluator()
    
    conditions = [
        ("age >= 18", {"age": 25}),
        ("score > 90", {"score": 85}),
        ("age >= 18 and score > 60", {"age": 25, "score": 85}),
    ]
    
    for condition, variables in conditions:
        result = cond_ev.eval(condition, variables)
        print(f"  {condition} = {result}")
    
    # 列表过滤
    print("\n  列表过滤:")
    items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    filtered = cond_ev.filter_list(items, "item > 5")
    print(f"    item > 5 → {filtered}")
    
    # ==================== TemplateEvaluator ====================
    print("\n【4. TemplateEvaluator - 模板求值器】")
    
    template_ev = TemplateEvaluator()
    
    templates = [
        "Result: ${2 + 3}",
        "${1 + 2} + ${3 + 4} = ${1 + 2 + 3 + 4}",
    ]
    
    for template in templates:
        result = template_ev.eval(template)
        print(f"  '{template}' → '{result}'")
    
    # ==================== BatchEvaluator ====================
    print("\n【5. BatchEvaluator - 批量求值器】")
    
    batch_ev = BatchEvaluator()
    batch_ev.set("x", 10).set("y", 5)
    
    expressions = ["x + y", "x * y", "x - y"]
    results = batch_ev.eval_all(expressions)
    for expr, result in zip(expressions, results):
        print(f"  {expr} = {result}")
    
    # ==================== ExpressionParser ====================
    print("\n【6. ExpressionParser - 表达式分析器】")
    
    parser = ExpressionParser()
    
    expr = "sin(x) + cos(y)"
    analysis = parser.analyze(expr)
    print(f"  分析: {expr}")
    print(f"    变量: {analysis['variables']}")
    print(f"    函数: {analysis['functions']}")
    
    print("\n" + "=" * 60)
    print("示例完成")
    print("=" * 60)


if __name__ == "__main__":
    main()