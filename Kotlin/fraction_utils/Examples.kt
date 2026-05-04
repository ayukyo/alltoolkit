/**
 * Fraction Utils 使用示例
 * 
 * 展示分数工具库的各种功能
 */

package fraction_utils

fun main() {
    println("=" .repeat(60))
    println("Fraction Utils - 分数计算工具库示例")
    println("=" .repeat(60))
    
    // ========== 1. 基础创建 ==========
    println("\n【1. 基础创建】")
    println("-".repeat(40))
    
    // 从分子分母创建
    val f1 = Fraction.of(3, 4)
    println("从分子分母创建: Fraction.of(3, 4) = $f1")
    
    // 从整数创建
    val f2 = Fraction.fromInt(5)
    println("从整数创建: Fraction.fromInt(5) = $f2")
    
    // 从小数创建（精确转换）
    val f3 = Fraction.fromDouble(0.75)
    println("从小数创建: Fraction.fromDouble(0.75) = $f3")
    
    // 从字符串解析
    val f4 = Fraction.parse("2/3")
    println("从字符串解析: Fraction.parse(\"2/3\") = $f4")
    
    // 解析带分数
    val f5 = Fraction.parse("1 1/2")
    println("解析带分数: Fraction.parse(\"1 1/2\") = $f5 (=${f5.doubleValue})")
    
    // 使用扩展函数
    val f6 = 3.toFraction()
    val f7 = 0.5.toFraction()
    val f8 = "4/5".toFraction()
    println("扩展函数: 3.toFraction() = $f6, 0.5.toFraction() = $f7, \"4/5\".toFraction() = $f8")
    
    // 预定义常量
    println("预定义常量: ZERO=${Fraction.ZERO}, ONE=${Fraction.ONE}, HALF=${Fraction.HALF}")
    
    // ========== 2. 属性查询 ==========
    println("\n【2. 属性查询】")
    println("-".repeat(40))
    
    val sample = Fraction.of(7, 4)
    println("示例分数: $sample")
    println("  双精度值: ${sample.doubleValue}")
    println("  整数值: ${sample.intValue}")
    println("  是否为负: ${sample.isNegative}")
    println("  是否为正: ${sample.isPositive}")
    println("  是否为零: ${sample.isZero}")
    println("  是否为整数: ${sample.isInteger}")
    println("  是否为真分数: ${sample.isProperFraction}")
    println("  整数部分: ${sample.wholePart}")
    println("  分数部分: ${sample.fractionalPart}")
    
    // ========== 3. 算术运算 ==========
    println("\n【3. 算术运算】")
    println("-".repeat(40))
    
    val a = Fraction.of(1, 2)
    val b = Fraction.of(1, 3)
    
    println("a = $a, b = $b")
    println("a + b = ${a + b}")
    println("a - b = ${a - b}")
    println("a * b = ${a * b}")
    println("a / b = ${a / b}")
    println("-a = ${-a}")
    println("a² = ${a.pow(2)}")
    println("a⁻¹ (倒数) = ${a.reciprocal()}")
    println("|${Fraction.of(-3, 4)}| = ${Fraction.of(-3, 4).abs()}")
    
    // ========== 4. 舍入操作 ==========
    println("\n【4. 舍入操作】")
    println("-".repeat(40))
    
    val toRound = Fraction.of(7, 3)
    println("分数: $toRound ≈ ${toRound.doubleValue}")
    println("  向上取整 (ceil): ${toRound.ceil()}")
    println("  向下取整 (floor): ${toRound.floor()}")
    println("  四舍五入 (round): ${toRound.round()}")
    
    // ========== 5. 比较操作 ==========
    println("\n【5. 比较操作】")
    println("-".repeat(40))
    
    val c = Fraction.of(1, 2)
    val d = Fraction.of(2, 4)
    val e = Fraction.of(2, 3)
    
    println("c = $c, d = $d, e = $e")
    println("c == d: ${c == d} (值相等)")
    println("c < e: ${c < e}")
    println("c > e: ${c > e}")
    println("max(c, d, e) = ${FractionUtils.max(c, d, e)}")
    println("min(c, d, e) = ${FractionUtils.min(c, d, e)}")
    println("e 在 c 和 1 之间: ${FractionUtils.isBetween(e, c, Fraction.ONE)}")
    
    // ========== 6. 字符串转换 ==========
    println("\n【6. 字符串转换】")
    println("-".repeat(40))
    
    val mixed = Fraction.of(5, 2)
    println("分数: $mixed")
    println("  普通字符串: ${mixed.toString()}")
    println("  带分数字符串: ${mixed.toMixedString()}")
    println("  小数字符串(2位): ${mixed.toDecimalString(2)}")
    println("  小数字符串(4位): ${mixed.toDecimalString(4)}")
    
    // ========== 7. 工具函数 ==========
    println("\n【7. 工具函数】")
    println("-".repeat(40))
    
    println("GCD(12, 18) = ${FractionUtils.gcd(12, 18)}")
    println("LCM(12, 18) = ${FractionUtils.lcm(12, 18)}")
    
    val sum = FractionUtils.sum(
        Fraction.of(1, 2),
        Fraction.of(1, 3),
        Fraction.of(1, 6)
    )
    println("sum(1/2 + 1/3 + 1/6) = $sum")
    
    val product = FractionUtils.product(
        Fraction.of(1, 2),
        Fraction.of(2, 3),
        Fraction.of(3, 4)
    )
    println("product(1/2 * 2/3 * 3/4) = $product")
    
    val avg = FractionUtils.average(
        Fraction.of(1, 4),
        Fraction.of(1, 2),
        Fraction.of(3, 4)
    )
    println("average(1/4, 1/2, 3/4) = $avg")
    
    // ========== 8. 连分数 ==========
    println("\n【8. 连分数展开】")
    println("-".repeat(40))
    
    val piApprox = Fraction.of(355, 113)
    println("355/113 ≈ π = ${piApprox.doubleValue}")
    val cf = FractionUtils.continuedFraction(piApprox)
    println("连分数展开: $cf")
    println("还原: ${FractionUtils.fromContinuedFraction(cf)}")
    
    // 黄金比例近似
    val goldenRatio = Fraction.of(144, 89)
    println("\n144/89 ≈ φ = ${goldenRatio.doubleValue}")
    println("连分数: ${FractionUtils.continuedFraction(goldenRatio)}")
    
    // ========== 9. 埃及分数 ==========
    println("\n【9. 埃及分数表示】")
    println("-".repeat(40))
    
    val eg = Fraction.of(5, 6)
    println("$eg 的埃及分数表示:")
    val egyptian = FractionUtils.egyptianFraction(eg)
    println("  ${egyptian.joinToString(" + ") { it.toString() }}")
    
    val eg2 = Fraction.of(2, 3)
    println("\n$eg2 的埃及分数表示:")
    println("  ${FractionUtils.egyptianFraction(eg2).joinToString(" + ") { it.toString() }}")
    
    // ========== 10. 精度对比 ==========
    println("\n【10. 精度对比：分数 vs 浮点数】")
    println("-".repeat(40))
    
    // 浮点数精度问题
    val floatSum = 0.1 + 0.1 + 0.1
    println("浮点数: 0.1 + 0.1 + 0.1 = $floatSum")
    println("浮点数 == 0.3: ${floatSum == 0.3}")
    
    // 分数精确计算
    val fracSum = Fraction.of(1, 10) + Fraction.of(1, 10) + Fraction.of(1, 10)
    println("\n分数: 1/10 + 1/10 + 1/10 = $fracSum")
    println("分数 == 3/10: ${fracSum == Fraction.of(3, 10)}")
    
    // 更多精度示例
    println("\n循环小数 1/3:")
    println("  浮点数: ${1.0/3.0}")
    println("  分数: ${Fraction.of(1, 3)}")
    println("  三次相加:")
    println("    浮点数: ${1.0/3.0 + 1.0/3.0 + 1.0/3.0}")
    println("    分数: ${FractionUtils.sum(Fraction.of(1, 3), Fraction.of(1, 3), Fraction.of(1, 3))}")
    
    // ========== 11. 实际应用 ==========
    println("\n【11. 实际应用示例】")
    println("-".repeat(40))
    
    // 食谱配比计算
    println("食谱配比计算:")
    val recipe = Fraction.of(2, 3)  // 原配方需要 2/3 杯糖
    val scaled = recipe * Fraction.of(3, 2)  // 放大1.5倍
    println("  原配方: ${recipe.toMixedString()} 杯糖")
    println("  放大1.5倍: ${scaled.toMixedString()} 杯糖")
    
    // 金融计算
    println("\n利息计算:")
    val principal = Fraction.of(10000, 1)
    val rate = Fraction.of(3, 100)  // 3% 年利率
    val months = 12
    var total = principal
    repeat(months) {
        total = total + total * rate / Fraction.fromInt(12)
    }
    println("  本金: 10000")
    println("  年利率: 3%")
    println("  12个月后: ${total.toDecimalString(2)}")
    
    // 几何计算
    println("\n矩形面积:")
    val width = Fraction.of(3, 4)  // 3/4 米
    val height = Fraction.of(2, 3) // 2/3 米
    val area = width * height
    println("  宽: ${width} 米")
    println("  高: ${height} 米")
    println("  面积: ${area} 平方米 = ${area.toDecimalString(4)} 平方米")
    
    // ========== 12. 完整计算示例 ==========
    println("\n【12. 完整计算示例】")
    println("-".repeat(40))
    
    // 复杂表达式
    val expr = (Fraction.of(1, 2) + Fraction.of(1, 3)) *
                (Fraction.of(2, 3) - Fraction.of(1, 4)) /
                Fraction.of(1, 6)
    println("(1/2 + 1/3) × (2/3 - 1/4) ÷ (1/6) = $expr")
    println("  = ${expr.toDecimalString(6)}")
    
    // 阶梯计算
    println("\n阶梯求和:")
    var sumN = Fraction.ZERO
    for (i in 1..10) {
        sumN = sumN + Fraction.of(1, i.toLong())
    }
    println("  1 + 1/2 + 1/3 + ... + 1/10 = $sumN")
    println("  ≈ ${sumN.toDecimalString(6)}")
    
    println("\n" + "=".repeat(60))
    println("示例完成!")
    println("=".repeat(60))
}