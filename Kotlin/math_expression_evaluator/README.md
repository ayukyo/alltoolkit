# MathExpressionEvaluator - 数学表达式计算器

一个纯 Kotlin 实现的数学表达式解析器和计算器，零外部依赖。

## 功能特性

- ✅ **基础运算**: 加、减、乘、除、取模
- ✅ **幂运算**: 支持右结合的幂运算符 `^`
- ✅ **括号**: 支持任意嵌套的括号
- ✅ **一元运算符**: 正号 `+` 和负号 `-`
- ✅ **三角函数**: sin, cos, tan, asin, acos, atan, sinh, cosh, tanh
- ✅ **数学函数**: sqrt, abs, log, log10, ln, exp, floor, ceil, round, sign
- ✅ **多参数函数**: pow, max, min, avg, sum
- ✅ **数学常量**: pi, e
- ✅ **变量绑定**: 支持动态变量替换
- ✅ **表达式验证**: 验证表达式有效性
- ✅ **变量提取**: 从表达式中提取变量名

## 快速开始

### 基本使用

```kotlin
import com.alltoolkit.math.MathExpressionEvaluator

val evaluator = MathExpressionEvaluator()

// 简单计算
evaluator.eval("2 + 3")           // 5.0
evaluator.eval("10 * 5 - 3")      // 47.0
evaluator.eval("2 ^ 10")          // 1024.0

// 数学函数
evaluator.eval("sqrt(16)")        // 4.0
evaluator.eval("sin(pi/2)")       // 1.0
evaluator.eval("max(1, 2, 3)")     // 3.0

// 变量绑定
evaluator.evaluate("x + y", mapOf("x" to 10.0, "y" to 20.0))  // 30.0
```

### 扩展函数

```kotlin
import com.alltoolkit.math.evalMath

// 直接在字符串上调用
"2 + 3".evalMath()                // 5.0
"sqrt(16)".evalMath()             // 4.0

// 使用 Pair 传递变量
"x + y".evalMath("x" to 5, "y" to 3)  // 8.0
```

### 表达式验证

```kotlin
import com.alltoolkit.math.ExpressionValidator

// 验证表达式有效性
ExpressionValidator.isValid("2 + 3")           // true
ExpressionValidator.isValid("2 +")             // false

// 提取变量名
ExpressionValidator.extractVariables("a*x + b")  // ["a", "x", "b"]

// 检查括号匹配
ExpressionValidator.hasBalancedParentheses("(2+3)")  // true
ExpressionValidator.hasBalancedParentheses("(2+3")   // false
```

## 支持的运算符

| 运算符 | 描述 | 优先级 |
|--------|------|--------|
| `^` | 幂运算 | 最高 |
| `*` | 乘法 | 高 |
| `/` | 除法 | 高 |
| `%` | 取模 | 高 |
| `+` | 加法 | 中 |
| `-` | 减法 | 中 |
| `+` (一元) | 正号 | 最高 |
| `-` (一元) | 负号 | 最高 |

## 支持的函数

### 单参数函数

| 函数 | 描述 |
|------|------|
| `sin(x)` | 正弦 |
| `cos(x)` | 余弦 |
| `tan(x)` | 正切 |
| `asin(x)` | 反正弦 |
| `acos(x)` | 反余弦 |
| `atan(x)` | 反正切 |
| `sinh(x)` | 双曲正弦 |
| `cosh(x)` | 双曲余弦 |
| `tanh(x)` | 双曲正切 |
| `sqrt(x)` | 平方根 |
| `abs(x)` | 绝对值 |
| `log(x)` | 以10为底对数 |
| `ln(x)` | 自然对数 |
| `exp(x)` | e的x次幂 |
| `floor(x)` | 向下取整 |
| `ceil(x)` | 向上取整 |
| `round(x)` | 四舍五入 |
| `sign(x)` | 符号函数 |
| `deg(x)` | 弧度转角度 |
| `rad(x)` | 角度转弧度 |

### 多参数函数

| 函数 | 描述 |
|------|------|
| `pow(x, y)` | x的y次幂 |
| `max(a, b, ...)` | 最大值 |
| `min(a, b, ...)` | 最小值 |
| `avg(a, b, ...)` | 平均值 |
| `sum(a, b, ...)` | 求和 |

## 应用示例

### 物理公式

```kotlin
// 自由落体: h = 0.5 * g * t^2
val h = evaluator.evaluate("0.5 * g * t^2", mapOf("g" to 9.8, "t" to 3.0))
// h = 44.1 米
```

### 二次方程求根

```kotlin
// x = (-b ± sqrt(b^2 - 4ac)) / 2a
val vars = mapOf("a" to 1.0, "b" to -5.0, "c" to 6.0)
val d = evaluator.evaluate("b^2 - 4*a*c", vars)
val x1 = evaluator.evaluate("(-b + sqrt(d)) / (2*a)", vars + ("d" to d))
// x1 = 3.0
```

### 金融计算

```kotlin
// 复利公式: A = P * (1 + r/n)^(n*t)
val A = evaluator.evaluate(
    "P * (1 + r/n)^(n*t)",
    mapOf("P" to 10000.0, "r" to 0.05, "n" to 12.0, "t" to 10.0)
)
// A ≈ 16470.09
```

## 编译和运行

```bash
# 编译
kotlinc MathExpressionEvaluator.kt -include-runtime -d MathExpressionEvaluator.jar

# 运行示例
kotlin -cp MathExpressionEvaluator.jar com.alltoolkit.math.MainKt examples.kt

# 运行测试
kotlinc -cp MathExpressionEvaluator.jar -script MathExpressionEvaluatorTest.kt
```

## 许可证

MIT License

## 作者

AllToolkit

## 日期

2026-05-15