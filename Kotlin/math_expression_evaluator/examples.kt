/**
 * MathExpressionEvaluator 使用示例
 * 
 * @author AllToolkit
 * @date 2026-05-15
 */

package com.alltoolkit.math

fun main() {
    val evaluator = MathExpressionEvaluator()
    
    println("=" .repeat(60))
    println("MathExpressionEvaluator 使用示例")
    println("=" .repeat(60))
    
    // ==================== 1. 基础运算 ====================
    println("\n【1. 基础运算】")
    println("-".repeat(40))
    
    println("加法: 2 + 3 = ${evaluator.eval("2 + 3")}")
    println("减法: 10 - 4 = ${evaluator.eval("10 - 4")}")
    println("乘法: 6 * 7 = ${evaluator.eval("6 * 7")}")
    println("除法: 15 / 3 = ${evaluator.eval("15 / 3")}")
    println("取模: 17 % 5 = ${evaluator.eval("17 % 5")}")
    println("幂运算: 2 ^ 10 = ${evaluator.eval("2 ^ 10")}")
    
    // ==================== 2. 运算优先级 ====================
    println("\n【2. 运算优先级】")
    println("-".repeat(40))
    
    println("2 + 3 * 4 = ${evaluator.eval("2 + 3 * 4")} (先乘后加)")
    println("(2 + 3) * 4 = ${evaluator.eval("(2 + 3) * 4")} (括号优先)")
    println("2 ^ 3 ^ 2 = ${evaluator.eval("2 ^ 3 ^ 2")} (幂运算右结合: 2^9)")
    println("10 - 2 * 3 + 4 = ${evaluator.eval("10 - 2 * 3 + 4")}")
    
    // ==================== 3. 一元运算符 ====================
    println("\n【3. 一元运算符】")
    println("-".repeat(40))
    
    println("-5 = ${evaluator.eval("-5")}")
    println("--5 = ${evaluator.eval("--5")} (负负得正)")
    println("-(-5) = ${evaluator.eval("-(-5)")}")
    println("2 * -3 = ${evaluator.eval("2 * -3")}")
    
    // ==================== 4. 数学函数 ====================
    println("\n【4. 数学函数】")
    println("-".repeat(40))
    
    println("三角函数:")
    println("  sin(pi/2) = ${evaluator.eval("sin(pi/2)")}")
    println("  cos(0) = ${evaluator.eval("cos(0)")}")
    println("  tan(pi/4) = ${evaluator.eval("tan(pi/4)")}")
    
    println("\n指数对数:")
    println("  sqrt(16) = ${evaluator.eval("sqrt(16)")}")
    println("  exp(1) = ${evaluator.eval("exp(1)")}")
    println("  ln(e) = ${evaluator.eval("ln(e)")}")
    println("  log(100) = ${evaluator.eval("log(100)")}")
    
    println("\n取整函数:")
    println("  floor(3.7) = ${evaluator.eval("floor(3.7)")}")
    println("  ceil(3.2) = ${evaluator.eval("ceil(3.2)")}")
    println("  round(3.5) = ${evaluator.eval("round(3.5)")}")
    println("  abs(-42) = ${evaluator.eval("abs(-42)")}")
    
    // ==================== 5. 多参数函数 ====================
    println("\n【5. 多参数函数】")
    println("-".repeat(40))
    
    println("pow(2, 10) = ${evaluator.eval("pow(2, 10)")}")
    println("max(3, 7, 2, 9, 1) = ${evaluator.eval("max(3, 7, 2, 9, 1)")}")
    println("min(3, 7, 2, 9, 1) = ${evaluator.eval("min(3, 7, 2, 9, 1)")}")
    println("avg(1, 2, 3, 4, 5) = ${evaluator.eval("avg(1, 2, 3, 4, 5)")}")
    println("sum(1, 2, 3, 4, 5) = ${evaluator.eval("sum(1, 2, 3, 4, 5)")}")
    
    // ==================== 6. 常量 ====================
    println("\n【6. 数学常量】")
    println("-".repeat(40))
    
    println("pi = ${evaluator.eval("pi")}")
    println("e = ${evaluator.eval("e")}")
    println("2 * pi * r (r=5) = ${evaluator.evaluate("2 * pi * r", mapOf("r" to 5.0))}")
    
    // ==================== 7. 变量 ====================
    println("\n【7. 变量绑定】")
    println("-".repeat(40))
    
    val variables = mapOf(
        "x" to 10.0,
        "y" to 20.0,
        "z" to 30.0
    )
    
    println("x + y = ${evaluator.evaluate("x + y", variables)}")
    println("x * y + z = ${evaluator.evaluate("x * y + z", variables)}")
    println("sqrt(x^2 + y^2) = ${evaluator.evaluate("sqrt(x^2 + y^2)", variables)}")
    
    // ==================== 8. 实际应用示例 ====================
    println("\n【8. 实际应用示例】")
    println("-".repeat(40))
    
    // 8.1 物理公式 - 自由落体
    println("自由落体 h = 0.5 * g * t^2")
    val g = 9.8
    val t = 3.0
    val h = evaluator.evaluate("0.5 * g * t^2", mapOf("g" to g, "t" to t))
    println("  g=9.8, t=3: h = $h 米")
    
    // 8.2 二次方程求根
    println("\n二次方程求根: x = (-b ± sqrt(b^2 - 4ac)) / 2a")
    val a = 1.0
    val b = -5.0
    val c = 6.0
    val discriminant = evaluator.evaluate("b^2 - 4*a*c", mapOf("a" to a, "b" to b, "c" to c))
    val x1 = evaluator.evaluate("(-b + sqrt(d)) / (2*a)", mapOf("a" to a, "b" to b, "d" to discriminant))
    val x2 = evaluator.evaluate("(-b - sqrt(d)) / (2*a)", mapOf("a" to a, "b" to b, "d" to discriminant))
    println("  方程 x^2 - 5x + 6 = 0")
    println("  x1 = $x1, x2 = $x2")
    
    // 8.3 几何计算
    println("\n圆的面积和周长:")
    val radius = 5.0
    val area = evaluator.evaluate("pi * r^2", mapOf("r" to radius))
    val circumference = evaluator.evaluate("2 * pi * r", mapOf("r" to radius))
    println("  半径 r=5: 面积 = $area, 周长 = $circumference")
    
    // 8.4 金融计算 - 复利
    println("\n复利公式: A = P * (1 + r/n)^(n*t)")
    val P = 10000.0  // 本金
    val r = 0.05    // 年利率
    val n = 12.0    // 年复利次数
    val years = 10.0
    val A = evaluator.evaluate(
        "P * (1 + r/n)^(n*t)",
        mapOf("P" to P, "r" to r, "n" to n, "t" to years)
    )
    println("  本金10000, 年利率5%, 月复利, 10年: $${String.format("%.2f", A)}")
    
    // 8.5 温度转换
    println("\n温度转换:")
    val celsius = 25.0
    val fahrenheit = evaluator.evaluate("c * 9/5 + 32", mapOf("c" to celsius))
    val kelvin = evaluator.evaluate("c + 273.15", mapOf("c" to celsius))
    println("  25°C = ${fahrenheit}°F = ${kelvin}K")
    
    // ==================== 9. 扩展函数使用 ====================
    println("\n【9. 扩展函数（简化调用）】")
    println("-".repeat(40))
    
    // 直接在字符串上调用
    println("\"2 + 3\".evalMath() = ${"2 + 3".evalMath()}")
    println("\"sqrt(16)\".evalMath() = ${"sqrt(16)".evalMath()}")
    
    // 使用 Pair 传变量
    println("\"x + y\".evalMath(\"x\" to 10, \"y\" to 20) = ${"x + y".evalMath("x" to 10, "y" to 20)}")
    println("\"a * b + c\".evalMath(\"a\" to 2, \"b\" to 3, \"c\" to 4) = ${"a * b + c".evalMath("a" to 2, "b" to 3, "c" to 4)}")
    
    // ==================== 10. 表达式验证 ====================
    println("\n【10. 表达式验证】")
    println("-".repeat(40))
    
    val expressions = listOf(
        "2 + 3",
        "sin(pi/2)",
        "(2 + 3",
        "unknown_func(5)",
        "x + y"
    )
    
    for (expr in expressions) {
        val isValid = ExpressionValidator.isValid(expr)
        println("  \"$expr\" -> ${if (isValid) "✓ 有效" else "✗ 无效"}")
    }
    
    // ==================== 11. 变量提取 ====================
    println("\n【11. 从表达式中提取变量】")
    println("-".repeat(40))
    
    val exprWithVars = "a*x^2 + b*x + c"
    val vars = ExpressionValidator.extractVariables(exprWithVars)
    println("表达式: $exprWithVars")
    println("变量: $vars")
    
    // ==================== 12. 复杂表达式 ====================
    println("\n【12. 复杂表达式示例】")
    println("-".repeat(40))
    
    // 嵌套函数调用
    val complex1 = "sqrt(sin(pi/6)^2 + cos(pi/6)^2)"
    println("$complex1 = ${evaluator.eval(complex1)}")
    
    // 多层括号
    val complex2 = "((1 + 2) * (3 + 4)) / (5 - 2)"
    println("$complex2 = ${evaluator.eval(complex2)}")
    
    // 混合运算
    val complex3 = "max(sin(pi/4), cos(pi/4))^2 + min(1, 2, 3)"
    println("$complex3 = ${evaluator.eval(complex3)}")
    
    println("\n" + "=".repeat(60))
    println("示例演示完成!")
    println("=".repeat(60))
}