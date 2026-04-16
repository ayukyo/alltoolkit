"""
expression_evaluator_utils 使用示例

展示表达式求值器的各种用法：
1. 基础数学运算
2. 变量和常量
3. 内置函数
4. 自定义函数
5. 三元条件表达式
6. 实际应用场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import ExpressionEvaluator, evaluate, validate, get_variables


def example_basic_arithmetic():
    """示例1：基础数学运算"""
    print("=" * 60)
    print("示例1：基础数学运算")
    print("=" * 60)
    
    evaluator = ExpressionEvaluator()
    
    expressions = [
        "2 + 3",
        "10 - 4",
        "6 * 7",
        "20 / 4",
        "17 % 5",
        "2 ^ 10",
        "2 + 3 * 4",
        "(2 + 3) * 4",
    ]
    
    for expr in expressions:
        result = evaluator.evaluate(expr)
        print(f"  {expr} = {result}")
    
    print()


def example_variables():
    """示例2：变量和常量"""
    print("=" * 60)
    print("示例2：变量和常量")
    print("=" * 60)
    
    evaluator = ExpressionEvaluator()
    
    # 设置变量
    evaluator.set_variable("x", 10)
    evaluator.set_variable("y", 5)
    evaluator.set_variable("name", "Alice")
    
    print(f"  x + y = {evaluator.evaluate('x + y')}")
    print(f"  x * y = {evaluator.evaluate('x * y')}")
    print(f"  x ^ y = {evaluator.evaluate('x ^ y')}")
    
    # 使用内联变量
    result = evaluator.evaluate("a + b + c", a=1, b=2, c=3)
    print(f"  a + b + c (内联) = {result}")
    
    # 字符串变量
    print(f"  'Hello, ' + name + '!' = {evaluator.evaluate(\"'Hello, ' + name + '!'\")}")
    
    # 内置常量
    print(f"\n  内置常量:")
    print(f"  pi = {evaluator.evaluate('pi')}")
    print(f"  e = {evaluator.evaluate('e')}")
    print(f"  true = {evaluator.evaluate('true')}")
    print(f"  false = {evaluator.evaluate('false')}")
    
    print()


def example_comparison_and_logical():
    """示例3：比较和逻辑运算"""
    print("=" * 60)
    print("示例3：比较和逻辑运算")
    print("=" * 60)
    
    evaluator = ExpressionEvaluator()
    
    # 比较运算
    comparisons = [
        "5 == 5",
        "5 != 3",
        "10 > 5",
        "3 < 7",
        "5 >= 5",
        "4 <= 6",
    ]
    
    print("  比较运算:")
    for expr in comparisons:
        result = evaluator.evaluate(expr)
        print(f"    {expr} = {result}")
    
    # 逻辑运算
    logical = [
        "true && true",
        "true && false",
        "false || true",
        "!false",
        "(5 > 3) && (10 < 20)",
        "(x > 0) && (x < 100)",
    ]
    
    print("\n  逻辑运算:")
    for expr in logical:
        result = evaluator.evaluate(expr, x=50)
        print(f"    {expr} = {result}")
    
    print()


def example_builtin_functions():
    """示例4：内置函数"""
    print("=" * 60)
    print("示例4：内置函数")
    print("=" * 60)
    
    evaluator = ExpressionEvaluator()
    
    # 三角函数
    print("  三角函数:")
    print(f"    sin(pi / 2) = {evaluator.evaluate('sin(pi / 2)')}")
    print(f"    cos(0) = {evaluator.evaluate('cos(0)')}")
    print(f"    tan(pi / 4) = {evaluator.evaluate('tan(pi / 4)')}")
    
    # 数学函数
    print("\n  数学函数:")
    print(f"    sqrt(16) = {evaluator.evaluate('sqrt(16)')}")
    print(f"    abs(-42) = {evaluator.evaluate('abs(-42)')}")
    print(f"    floor(3.7) = {evaluator.evaluate('floor(3.7)')}")
    print(f"    ceil(3.2) = {evaluator.evaluate('ceil(3.2)')}")
    print(f"    round(3.5) = {evaluator.evaluate('round(3.5)')}")
    
    # 指数对数
    print("\n  指数对数:")
    print(f"    exp(1) = {evaluator.evaluate('exp(1)')}")
    print(f"    log(e) = {evaluator.evaluate('log(e)')}")
    print(f"    log10(100) = {evaluator.evaluate('log10(100)')}")
    print(f"    log2(8) = {evaluator.evaluate('log2(8)')}")
    
    # 最值
    print("\n  最值:")
    print(f"    min(3, 1, 4, 1, 5) = {evaluator.evaluate('min(3, 1, 4, 1, 5)')}")
    print(f"    max(3, 1, 4, 1, 5) = {evaluator.evaluate('max(3, 1, 4, 1, 5)')}")
    
    # 类型转换
    print("\n  类型转换:")
    print(f"    int(3.7) = {evaluator.evaluate('int(3.7)')}")
    print(f"    float(42) = {evaluator.evaluate('float(42)')}")
    print(f"    str(123) = '{evaluator.evaluate(\"str(123)\")}'")
    print(f"    bool(1) = {evaluator.evaluate('bool(1)')}")
    
    print()


def example_custom_functions():
    """示例5：自定义函数"""
    print("=" * 60)
    print("示例5：自定义函数")
    print("=" * 60)
    
    evaluator = ExpressionEvaluator()
    
    # 定义简单函数
    evaluator.set_function("double", lambda x: x * 2)
    evaluator.set_function("triple", lambda x: x * 3)
    evaluator.set_function("square", lambda x: x ** 2)
    
    print("  自定义数学函数:")
    print(f"    double(5) = {evaluator.evaluate('double(5)')}")
    print(f"    triple(4) = {evaluator.evaluate('triple(4)')}")
    print(f"    square(7) = {evaluator.evaluate('square(7)')}")
    
    # 定义多参数函数
    evaluator.set_function("add", lambda a, b: a + b)
    evaluator.set_function("greet", lambda name: f"Hello, {name}!")
    
    print("\n  多参数函数:")
    print(f"    add(10, 20) = {evaluator.evaluate('add(10, 20)')}")
    print(f"    greet('World') = '{evaluator.evaluate(\"greet('World')\")}'")
    
    # 定义复杂函数
    def fibonacci(n):
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b
    
    evaluator.set_function("fib", fibonacci)
    
    print("\n  斐波那契函数:")
    for i in range(10):
        result = evaluator.evaluate(f"fib({i})")
        print(f"    fib({i}) = {result}")
    
    print()


def example_ternary_expressions():
    """示例6：三元条件表达式"""
    print("=" * 60)
    print("示例6：三元条件表达式")
    print("=" * 60)
    
    evaluator = ExpressionEvaluator()
    
    # 简单三元表达式
    print("  简单条件:")
    print(f"    1 ? 'yes' : 'no' = '{evaluator.evaluate(\"1 ? 'yes' : 'no'\")}'")
    print(f"    0 ? 'yes' : 'no' = '{evaluator.evaluate(\"0 ? 'yes' : 'no'\")}'")
    
    # 带比较的三元表达式
    print("\n  带比较:")
    for score in [95, 75, 55]:
        result = evaluator.evaluate("score >= 60 ? 'Pass' : 'Fail'", score=score)
        print(f"    score={score}: {result}")
    
    # 嵌套三元表达式（成绩等级）
    expr = "score >= 90 ? 'A' : (score >= 80 ? 'B' : (score >= 70 ? 'C' : (score >= 60 ? 'D' : 'F')))"
    
    print("\n  成绩等级:")
    for score in [95, 85, 75, 65, 55]:
        grade = evaluator.evaluate(expr, score=score)
        print(f"    score={score}: Grade {grade}")
    
    # 最大值
    max_expr = "a > b ? a : b"
    print(f"\n  最大值: max(10, 5) = {evaluator.evaluate(max_expr, a=10, b=5)}")
    
    # 绝对值
    abs_expr = "x >= 0 ? x : -x"
    print(f"  绝对值: |{-7}| = {evaluator.evaluate(abs_expr, x=-7)}")
    
    print()


def example_practical_applications():
    """示例7：实际应用场景"""
    print("=" * 60)
    print("示例7：实际应用场景")
    print("=" * 60)
    
    evaluator = ExpressionEvaluator()
    
    # 1. 计算器
    print("  1. 科学计算器:")
    calculations = [
        "2 + 3 * 4",
        "sqrt(2) + sqrt(3)",
        "sin(pi / 6) + cos(pi / 3)",
        "log(100) + log10(1000)",
    ]
    for expr in calculations:
        print(f"    {expr} = {evaluator.evaluate(expr):.4f}")
    
    # 2. 单位转换
    print("\n  2. 单位转换:")
    # 温度: C to F
    celsius = 25
    fahrenheit = evaluator.evaluate("c * 9 / 5 + 32", c=celsius)
    print(f"    {celsius}°C = {fahrenheit}°F")
    
    # 长度: km to miles
    km = 100
    miles = evaluator.evaluate("km * 0.621371", km=km)
    print(f"    {km} km = {miles:.2f} miles")
    
    # 3. 金融计算
    print("\n  3. 金融计算:")
    # BMI
    weight, height = 70, 1.75
    bmi = evaluator.evaluate("weight / (height ^ 2)", weight=weight, height=height)
    print(f"    BMI: {bmi:.2f} (weight={weight}kg, height={height}m)")
    
    # 复利
    P, r, n, t = 1000, 0.05, 12, 10
    amount = evaluator.evaluate("P * (1 + r/n) ^ (n*t)", P=P, r=r, n=n, t=t)
    print(f"    复利: ${amount:.2f} (本金=${P}, 年利率={r*100}%, 月复利, {t}年)")
    
    # 月供
    principal, annual_rate, years = 200000, 0.06, 30
    monthly_payment = evaluator.evaluate(
        "P * (r/12 * (1 + r/12)^(n*12)) / ((1 + r/12)^(n*12) - 1)",
        P=principal, r=annual_rate, n=years
    )
    print(f"    月供: ${monthly_payment:.2f} (贷款=${principal}, 年利率={annual_rate*100}%, {years}年)")
    
    # 4. 几何计算
    print("\n  4. 几何计算:")
    # 圆面积
    radius = 5
    area = evaluator.evaluate("pi * r ^ 2", r=radius)
    print(f"    圆面积: {area:.2f} (半径={radius})")
    
    # 球体积
    volume = evaluator.evaluate("4/3 * pi * r ^ 3", r=radius)
    print(f"    球体积: {volume:.2f} (半径={radius})")
    
    # 5. 数据验证
    print("\n  5. 数据验证:")
    validations = [
        ("age >= 18 && age <= 65", {"age": 25}),
        ("email contains '@' ? 'valid' : 'invalid'", {"email": "test@example.com"}),
        ("score >= 0 && score <= 100", {"score": 85}),
    ]
    
    # 注意：contains不是内置函数，我们用其他方式演示
    age = 25
    is_valid_age = evaluator.evaluate("age >= 18 && age <= 65", age=age)
    print(f"    年龄{age}是否在18-65范围: {is_valid_age}")
    
    score = 85
    is_valid_score = evaluator.evaluate("score >= 0 && score <= 100", score=score)
    print(f"    分数{score}是否在0-100范围: {is_valid_score}")
    
    print()


def example_validation_and_analysis():
    """示例8：验证和分析"""
    print("=" * 60)
    print("示例8：表达式验证和分析")
    print("=" * 60)
    
    # 验证表达式
    expressions = [
        "2 + 3 * 4",
        "sin(pi / 2)",
        "x + y * z",
        "(2 + 3",
        "2 + + 3",
    ]
    
    print("  表达式验证:")
    for expr in expressions:
        is_valid, error = validate(expr)
        if is_valid:
            print(f"    ✓ '{expr}' - 有效")
        else:
            print(f"    ✗ '{expr}' - 无效: {error}")
    
    # 分析表达式
    print("\n  变量分析:")
    expr = "sqrt(a) + sin(b) * c - d"
    variables = get_variables(expr)
    print(f"    表达式: {expr}")
    print(f"    变量: {variables}")
    
    print()


def example_convenience_functions():
    """示例9：便捷函数"""
    print("=" * 60)
    print("示例9：便捷函数")
    print("=" * 60)
    
    # 使用evaluate便捷函数
    print("  evaluate() 函数:")
    print(f"    evaluate('2 + 3') = {evaluate('2 + 3')}")
    print(f"    evaluate('x * y', x=5, y=3) = {evaluate('x * y', x=5, y=3)}")
    
    # 使用validate便捷函数
    print("\n  validate() 函数:")
    is_valid, error = validate("sqrt(x) + y")
    print(f"    validate('sqrt(x) + y') = {is_valid}")
    
    # 使用get_variables便捷函数
    print("\n  get_variables() 函数:")
    variables = get_variables("a + b * c - d")
    print(f"    get_variables('a + b * c - d') = {variables}")
    
    print()


def example_formula_calculator():
    """示例10：公式计算器"""
    print("=" * 60)
    print("示例10：公式计算器")
    print("=" * 60)
    
    evaluator = ExpressionEvaluator()
    
    # 定义常用公式
    formulas = {
        "勾股定理": "sqrt(a^2 + b^2)",
        "二次方程根": "(-b + sqrt(b^2 - 4*a*c)) / (2*a)",
        "圆面积": "pi * r^2",
        "圆周长": "2 * pi * r",
        "球体积": "4/3 * pi * r^3",
        "BMI": "weight / height^2",
        "摄氏转华氏": "c * 9/5 + 32",
        "华氏转摄氏": "(f - 32) * 5/9",
    }
    
    print("  公式计算器演示:")
    
    # 勾股定理
    result = evaluator.evaluate(formulas["勾股定理"], a=3, b=4)
    print(f"    勾股定理 (a=3, b=4): c = {result}")
    
    # 二次方程
    a, b, c = 1, -5, 6
    root = evaluator.evaluate(formulas["二次方程根"], a=a, b=b, c=c)
    print(f"    二次方程 (a={a}, b={b}, c={c}): x = {root}")
    
    # 圆
    r = 5
    area = evaluator.evaluate(formulas["圆面积"], r=r)
    circumference = evaluator.evaluate(formulas["圆周长"], r=r)
    print(f"    圆 (r={r}): 面积={area:.2f}, 周长={circumference:.2f}")
    
    # 球
    volume = evaluator.evaluate(formulas["球体积"], r=r)
    print(f"    球 (r={r}): 体积={volume:.2f}")
    
    # BMI
    weight, height = 70, 1.75
    bmi = evaluator.evaluate(formulas["BMI"], weight=weight, height=height)
    print(f"    BMI (weight={weight}kg, height={height}m): {bmi:.2f}")
    
    # 温度转换
    celsius = 25
    fahrenheit = evaluator.evaluate(formulas["摄氏转华氏"], c=celsius)
    print(f"    摄氏转华氏 ({celsius}°C): {fahrenheit}°F")
    
    f = 77
    c = evaluator.evaluate(formulas["华氏转摄氏"], f=f)
    print(f"    华氏转摄氏 ({f}°F): {c:.1f}°C")
    
    print()


def main():
    """运行所有示例"""
    example_basic_arithmetic()
    example_variables()
    example_comparison_and_logical()
    example_builtin_functions()
    example_custom_functions()
    example_ternary_expressions()
    example_practical_applications()
    example_validation_and_analysis()
    example_convenience_functions()
    example_formula_calculator()
    
    print("=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()