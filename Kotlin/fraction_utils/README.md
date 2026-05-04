# Fraction Utils - 分数计算工具库

精确分数计算工具库，避免浮点数精度问题。零外部依赖，纯 Kotlin 标准库实现。

## 功能特性

### 核心功能
- **分数创建**：从分子分母、整数、小数、字符串创建
- **自动约分**：分数始终以最简形式存储
- **负数处理**：负号自动规范化到分子

### 算术运算
- 加法 (+)
- 减法 (-)
- 乘法 (*)
- 除法 (/)
- 取负 (unaryMinus)
- 幂运算 (pow)
- 倒数 (reciprocal)
- 绝对值 (abs)

### 舍入操作
- 向上取整 (ceil)
- 向下取整 (floor)
- 四舍五入 (round)

### 比较操作
- Comparable 接口支持
- 等值判断（基于值）
- hashCode 支持

### 字符串转换
- 普通分数格式 (toString)
- 带分数格式 (toMixedString)
- 小数格式 (toDecimalString)

### 工具函数 (FractionUtils)
- GCD/LCM 计算
- 聚合函数（sum, product, average, max, min）
- 连分数展开与还原
- 埃及分数表示
- 通分操作

### 扩展函数
- `Int.toFraction()`
- `Long.toFraction()`
- `Double.toFraction()`
- `String.toFraction()`

## 快速开始

### 创建分数

```kotlin
// 从分子分母
val f1 = Fraction.of(3, 4)  // 3/4

// 从整数
val f2 = Fraction.fromInt(5)  // 5

// 从小数
val f3 = Fraction.fromDouble(0.5)  // 1/2

// 从字符串
val f4 = Fraction.parse("2/3")  // 2/3
val f5 = Fraction.parse("1 1/2")  // 1 1/2 (带分数)

// 使用扩展函数
val f6 = 3.toFraction()
val f7 = 0.25.toFraction()
val f8 = "4/5".toFraction()
```

### 算术运算

```kotlin
val a = Fraction.of(1, 2)
val b = Fraction.of(1, 3)

val sum = a + b        // 5/6
val diff = a - b       // 1/6
val prod = a * b       // 1/6
val quot = a / b       // 3/2
val neg = -a           // -1/2
val square = a.pow(2)  // 1/4
val recip = a.reciprocal()  // 2
val absVal = Fraction.of(-3, 4).abs()  // 3/4
```

### 舍入操作

```kotlin
val f = Fraction.of(7, 3)  // ≈ 2.33

f.ceil()   // 3
f.floor()  // 2
f.round()  // 2
```

### 字符串转换

```kotlin
val f = Fraction.of(5, 2)  // 2.5

f.toString()          // "5/2"
f.toMixedString()     // "2 1/2"
f.toDecimalString(2)  // "2.50"
```

### 工具函数

```kotlin
// GCD/LCM
FractionUtils.gcd(12, 18)  // 6
FractionUtils.lcm(12, 18)  // 36

// 聚合
FractionUtils.sum(Fraction.of(1, 2), Fraction.of(1, 3))  // 5/6
FractionUtils.average(Fraction.of(1, 4), Fraction.of(3, 4))  // 1/2

// 连分数
val cf = FractionUtils.continuedFraction(Fraction.of(355, 113))  // [3, 7, 16]
FractionUtils.fromContinuedFraction(cf)  // 355/113

// 埃及分数
FractionUtils.egyptianFraction(Fraction.of(2, 3))  // [1/2, 1/6]
```

## 精度优势

分数运算完全精确，避免浮点数精度问题：

```kotlin
// 浮点数不精确
val floatSum = 0.1 + 0.1 + 0.1  // ≈ 0.30000000000000004

// 分数精确
val fracSum = Fraction.of(1, 10) + Fraction.of(1, 10) + Fraction.of(1, 10)  // 3/10
fracSum == Fraction.of(3, 10)  // true
```

## 预定义常量

```kotlin
Fraction.ZERO          // 0
Fraction.ONE           // 1
Fraction.HALF          // 1/2
Fraction.QUARTER       // 1/4
Fraction.NEGATIVE_ONE  // -1
```

## 文件结构

```
fraction_utils/
├── Fraction.kt       # 分数类和工具函数
├── FractionTest.kt   # 单元测试 (145 测试)
├── Examples.kt       # 使用示例
└── README.md         # 本文档
```

## 测试覆盖

- 基础创建：正/负分数、自动约分、零处理
- 工厂方法：fromInt、fromLong、fromDouble、parse
- 属性查询：doubleValue、intValue、isNegative 等
- 算术运算：加减乘除、幂、倒数、绝对值
- 舍入操作：ceil、floor、round
- 比较操作：compareTo、equals、hashCode
- 字符串转换：toString、toMixedString、toDecimalString
- 工具函数：GCD/LCM、聚合、连分数、埃及分数
- 边界情况：大数、极小数、链式运算

## 作者

AllToolkit 自动生成

## 日期

2026-05-05