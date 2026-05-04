/**
 * Fraction Utils 单元测试 - Kotlin 原生测试
 * 
 * 无外部依赖，使用 println 和手动断言验证
 */

package fraction_utils

import kotlin.math.abs

object FractionTest {
    
    private var testCount = 0
    private var passCount = 0
    
    private fun assertEq(expected: Any?, actual: Any?, message: String = "") {
        testCount++
        if (expected == actual) {
            passCount++
            println("✓ PASS: $message (expected=$expected, actual=$actual)")
        } else {
            println("✗ FAIL: $message (expected=$expected, actual=$actual)")
        }
    }
    
    private fun assertBool(condition: Boolean, message: String = "") {
        testCount++
        if (condition) {
            passCount++
            println("✓ PASS: $message")
        } else {
            println("✗ FAIL: $message (expected=true, actual=false)")
        }
    }
    
    private fun assertThrows(block: () -> Unit, exceptionType: String, message: String = "") {
        testCount++
        try {
            block()
            println("✗ FAIL: $message (expected $exceptionType)")
        } catch (e: Exception) {
            val name = e::class.simpleName ?: ""
            if (name == exceptionType || name.contains(exceptionType)) {
                passCount++
                println("✓ PASS: $message (caught $exceptionType)")
            } else {
                println("✗ FAIL: $message (expected $exceptionType, got $name)")
            }
        }
    }
    
    // ========== 基础创建测试 ==========
    
    fun testCreateBasicFraction() {
        println("\n--- 基础创建测试 ---")
        val f = Fraction.of(3, 4)
        assertEq(3L, f.numerator, "创建正分数-分子")
        assertEq(4L, f.denominator, "创建正分数-分母")
    }
    
    fun testCreateNegativeFraction() {
        val f = Fraction.of(-3, 4)
        assertEq(-3L, f.numerator, "创建负分数-分子")
        assertEq(4L, f.denominator, "创建负分数-分母")
    }
    
    fun testCreateNegativeDenominator() {
        val f = Fraction.of(3, -4)
        assertEq(-3L, f.numerator, "负分母转为负分子")
        assertEq(4L, f.denominator, "负分母转为正分母")
    }
    
    fun testCreateBothNegative() {
        val f = Fraction.of(-3, -4)
        assertEq(3L, f.numerator, "双负转为正分子")
        assertEq(4L, f.denominator, "双负转为正分母")
    }
    
    fun testCreateWithZeroDenominator() {
        assertThrows({ Fraction.of(1, 0) }, "IllegalArgumentException", "零分母抛异常")
    }
    
    fun testCreateSimplified() {
        val f = Fraction.of(6, 8)
        assertEq(3L, f.numerator, "自动约分-分子")
        assertEq(4L, f.denominator, "自动约分-分母")
    }
    
    fun testCreateZero() {
        val f = Fraction.of(0, 5)
        assertEq(0L, f.numerator, "零的分子")
        assertEq(1L, f.denominator, "零的分母归一")
    }
    
    // ========== 工厂方法测试 ==========
    
    fun testFromInt() {
        println("\n--- 工厂方法测试 ---")
        val f = Fraction.fromInt(5)
        assertEq(5L, f.numerator, "fromInt-分子")
        assertEq(1L, f.denominator, "fromInt-分母")
    }
    
    fun testFromLong() {
        val f = Fraction.fromLong(123456789L)
        assertEq(123456789L, f.numerator, "fromLong-分子")
        assertEq(1L, f.denominator, "fromLong-分母")
    }
    
    fun testFromDouble() {
        val f = Fraction.fromDouble(0.5)
        assertEq(1L, f.numerator, "fromDouble(0.5)-分子")
        assertEq(2L, f.denominator, "fromDouble(0.5)-分母")
    }
    
    fun testFromDoubleRepeating() {
        val f = Fraction.fromDouble(1.0 / 3.0)
        assertEq(1L, f.numerator, "fromDouble(1/3)-分子")
        assertEq(3L, f.denominator, "fromDouble(1/3)-分母")
    }
    
    fun testFromDoubleNegative() {
        val f = Fraction.fromDouble(-0.25)
        assertEq(-1L, f.numerator, "fromDouble(-0.25)-分子")
        assertEq(4L, f.denominator, "fromDouble(-0.25)-分母")
    }
    
    fun testFromDoubleNaN() {
        assertThrows({ Fraction.fromDouble(Double.NaN) }, "IllegalArgumentException", "NaN抛异常")
    }
    
    fun testFromDoubleInfinite() {
        assertThrows({ Fraction.fromDouble(Double.POSITIVE_INFINITY) }, "IllegalArgumentException", "Infinity抛异常")
    }
    
    // ========== 解析测试 ==========
    
    fun testParseFraction() {
        println("\n--- 解析测试 ---")
        val f = Fraction.parse("3/4")
        assertEq(3L, f.numerator, "解析'3/4'-分子")
        assertEq(4L, f.denominator, "解析'3/4'-分母")
    }
    
    fun testParseNegativeFraction() {
        val f = Fraction.parse("-5/6")
        assertEq(-5L, f.numerator, "解析'-5/6'-分子")
        assertEq(6L, f.denominator, "解析'-5/6'-分母")
    }
    
    fun testParseInteger() {
        val f = Fraction.parse("42")
        assertEq(42L, f.numerator, "解析'42'-分子")
        assertEq(1L, f.denominator, "解析'42'-分母")
    }
    
    fun testParseDecimal() {
        val f = Fraction.parse("0.75")
        assertEq(3L, f.numerator, "解析'0.75'-分子")
        assertEq(4L, f.denominator, "解析'0.75'-分母")
    }
    
    fun testParseMixedNumber() {
        val f = Fraction.parse("1 1/2")
        assertEq(3L, f.numerator, "解析'1 1/2'-分子")
        assertEq(2L, f.denominator, "解析'1 1/2'-分母")
    }
    
    fun testParseNegativeMixedNumber() {
        val f = Fraction.parse("-2 3/4")
        assertEq(-11L, f.numerator, "解析'-2 3/4'-分子")
        assertEq(4L, f.denominator, "解析'-2 3/4'-分母")
    }
    
    // ========== 属性测试 ==========
    
    fun testDoubleValue() {
        println("\n--- 属性测试 ---")
        val f = Fraction.of(3, 4)
        assertBool(abs(0.75 - f.doubleValue) < 0.0001, "doubleValue正确")
    }
    
    fun testIntValue() {
        val f = Fraction.of(7, 3)
        assertEq(2, f.intValue, "intValue-正数")
    }
    
    fun testIntValueNegative() {
        val f = Fraction.of(-7, 3)
        assertEq(-2, f.intValue, "intValue-负数")
    }
    
    fun testIsNegative() {
        assertBool(Fraction.of(-3, 4).isNegative, "负分数isNegative")
        assertBool(!Fraction.of(3, 4).isNegative, "正分数isNegative=false")
        assertBool(!Fraction.ZERO.isNegative, "零isNegative=false")
    }
    
    fun testIsPositive() {
        assertBool(Fraction.of(3, 4).isPositive, "正分数isPositive")
        assertBool(!Fraction.of(-3, 4).isPositive, "负分数isPositive=false")
        assertBool(!Fraction.ZERO.isPositive, "零isPositive=false")
    }
    
    fun testIsZero() {
        assertBool(Fraction.ZERO.isZero, "零isZero")
        assertBool(!Fraction.of(1, 2).isZero, "非零isZero=false")
    }
    
    fun testIsInteger() {
        assertBool(Fraction.of(5, 1).isInteger, "整数isInteger")
        assertBool(!Fraction.of(5, 2).isInteger, "非整数isInteger=false")
    }
    
    fun testIsProperFraction() {
        assertBool(Fraction.of(3, 4).isProperFraction, "真分数")
        assertBool(!Fraction.of(5, 4).isProperFraction, "假分数")
    }
    
    fun testWholePart() {
        assertEq(2L, Fraction.of(7, 3).wholePart, "wholePart-正数")
        assertEq(-2L, Fraction.of(-7, 3).wholePart, "wholePart-负数")
    }
    
    fun testFractionalPart() {
        val f = Fraction.of(7, 3)
        assertEq(1L, f.fractionalPart.numerator, "fractionalPart-分子")
        assertEq(3L, f.fractionalPart.denominator, "fractionalPart-分母")
    }
    
    // ========== 算术运算测试 ==========
    
    fun testAddition() {
        println("\n--- 算术运算测试 ---")
        val a = Fraction.of(1, 2)
        val b = Fraction.of(1, 3)
        val result = a + b
        assertEq(5L, result.numerator, "加法-分子")
        assertEq(6L, result.denominator, "加法-分母")
    }
    
    fun testAdditionWithNegative() {
        val a = Fraction.of(1, 2)
        val b = Fraction.of(-1, 3)
        val result = a + b
        assertEq(1L, result.numerator, "加法(含负)-分子")
        assertEq(6L, result.denominator, "加法(含负)-分母")
    }
    
    fun testSubtraction() {
        val a = Fraction.of(1, 2)
        val b = Fraction.of(1, 3)
        val result = a - b
        assertEq(1L, result.numerator, "减法-分子")
        assertEq(6L, result.denominator, "减法-分母")
    }
    
    fun testMultiplication() {
        val a = Fraction.of(2, 3)
        val b = Fraction.of(3, 4)
        val result = a * b
        assertEq(1L, result.numerator, "乘法-分子")
        assertEq(2L, result.denominator, "乘法-分母")
    }
    
    fun testDivision() {
        val a = Fraction.of(2, 3)
        val b = Fraction.of(3, 4)
        val result = a / b
        assertEq(8L, result.numerator, "除法-分子")
        assertEq(9L, result.denominator, "除法-分母")
    }
    
    fun testDivisionByZero() {
        assertThrows({ Fraction.of(1, 2) / Fraction.ZERO }, "ArithmeticException", "除以零抛异常")
    }
    
    fun testUnaryMinus() {
        val f = Fraction.of(3, 4)
        val negated = -f
        assertEq(-3L, negated.numerator, "取负-分子")
        assertEq(4L, negated.denominator, "取负-分母")
    }
    
    fun testPow() {
        val f = Fraction.of(2, 3)
        val squared = f.pow(2)
        assertEq(4L, squared.numerator, "平方-分子")
        assertEq(9L, squared.denominator, "平方-分母")
    }
    
    fun testPowZero() {
        val f = Fraction.of(2, 3)
        val result = f.pow(0)
        assertEq(Fraction.ONE, result, "0次幂=1")
    }
    
    fun testPowNegative() {
        val f = Fraction.of(2, 3)
        val result = f.pow(-1)
        assertEq(3L, result.numerator, "负幂(倒数)-分子")
        assertEq(2L, result.denominator, "负幂(倒数)-分母")
    }
    
    fun testReciprocal() {
        val f = Fraction.of(3, 4)
        val reciprocal = f.reciprocal()
        assertEq(4L, reciprocal.numerator, "倒数-分子")
        assertEq(3L, reciprocal.denominator, "倒数-分母")
    }
    
    fun testReciprocalOfZero() {
        assertThrows({ Fraction.ZERO.reciprocal() }, "ArithmeticException", "零的倒数抛异常")
    }
    
    fun testAbs() {
        assertEq(Fraction.of(3, 4), Fraction.of(-3, 4).abs(), "绝对值-负数")
        assertEq(Fraction.of(3, 4), Fraction.of(3, 4).abs(), "绝对值-正数")
    }
    
    // ========== 舍入测试 ==========
    
    fun testCeil() {
        println("\n--- 舍入测试 ---")
        assertEq(Fraction.of(2, 1), Fraction.of(7, 4).ceil(), "ceil-正数")
        assertEq(Fraction.of(-1, 1), Fraction.of(-7, 4).ceil(), "ceil-负数")
    }
    
    fun testFloor() {
        assertEq(Fraction.of(1, 1), Fraction.of(7, 4).floor(), "floor-正数")
        assertEq(Fraction.of(-2, 1), Fraction.of(-7, 4).floor(), "floor-负数")
    }
    
    fun testRound() {
        assertEq(Fraction.of(2, 1), Fraction.of(7, 4).round(), "round-7/4")
        assertEq(Fraction.of(1, 1), Fraction.of(5, 4).round(), "round-5/4")
    }
    
    // ========== 比较测试 ==========
    
    fun testCompareTo() {
        println("\n--- 比较测试 ---")
        val a = Fraction.of(1, 2)
        val b = Fraction.of(1, 3)
        assertBool(a > b, "a > b")
        assertBool(b < a, "b < a")
    }
    
    fun testEquals() {
        val a = Fraction.of(1, 2)
        val b = Fraction.of(2, 4)
        assertEq(a, b, "1/2 == 2/4")
    }
    
    fun testNotEquals() {
        val a = Fraction.of(1, 2)
        val b = Fraction.of(1, 3)
        assertBool(a != b, "1/2 != 1/3")
    }
    
    fun testHashCode() {
        val a = Fraction.of(1, 2)
        val b = Fraction.of(2, 4)
        assertEq(a.hashCode(), b.hashCode(), "相等分数hashCode相同")
    }
    
    // ========== 字符串转换测试 ==========
    
    fun testToString() {
        println("\n--- 字符串转换测试 ---")
        assertEq("3/4", Fraction.of(3, 4).toString(), "toString-分数")
        assertEq("5", Fraction.of(5, 1).toString(), "toString-整数")
        assertEq("-2/3", Fraction.of(-2, 3).toString(), "toString-负分数")
    }
    
    fun testToMixedString() {
        assertEq("1 1/2", Fraction.of(3, 2).toMixedString(), "toMixedString-正数")
        assertEq("-1 1/2", Fraction.of(-3, 2).toMixedString(), "toMixedString-负数")
        assertEq("1/2", Fraction.of(1, 2).toMixedString(), "toMixedString-真分数")
    }
    
    fun testToDecimalString() {
        assertEq("0.750000", Fraction.of(3, 4).toDecimalString(), "toDecimalString-默认")
        assertEq("0.75", Fraction.of(3, 4).toDecimalString(2), "toDecimalString-2位")
    }
    
    // ========== 预定义常量测试 ==========
    
    fun testPredefinedConstants() {
        println("\n--- 预定义常量测试 ---")
        assertEq(0L, Fraction.ZERO.numerator, "ZERO-分子")
        assertEq(1L, Fraction.ONE.numerator, "ONE-分子")
        assertEq(1L, Fraction.HALF.numerator, "HALF-分子")
        assertEq(2L, Fraction.HALF.denominator, "HALF-分母")
        assertEq(-1L, Fraction.NEGATIVE_ONE.numerator, "NEGATIVE_ONE-分子")
    }
    
    // ========== FractionUtils测试 ==========
    
    fun testGcd() {
        println("\n--- FractionUtils测试 ---")
        assertEq(6L, FractionUtils.gcd(12, 18), "gcd(12,18)")
        assertEq(1L, FractionUtils.gcd(7, 11), "gcd(7,11)")
        assertEq(5L, FractionUtils.gcd(0, 5), "gcd(0,5)")
    }
    
    fun testLcm() {
        assertEq(36L, FractionUtils.lcm(12, 18), "lcm(12,18)")
        assertEq(77L, FractionUtils.lcm(7, 11), "lcm(7,11)")
        assertEq(0L, FractionUtils.lcm(0, 5), "lcm(0,5)")
    }
    
    fun testSum() {
        val result = FractionUtils.sum(
            Fraction.of(1, 2),
            Fraction.of(1, 3),
            Fraction.of(1, 6)
        )
        assertEq(Fraction.ONE, result, "sum(1/2+1/3+1/6)")
    }
    
    fun testProduct() {
        val result = FractionUtils.product(
            Fraction.of(1, 2),
            Fraction.of(2, 3),
            Fraction.of(3, 4)
        )
        assertEq(Fraction.of(1, 4), result, "product(1/2*2/3*3/4)")
    }
    
    fun testAverage() {
        val result = FractionUtils.average(
            Fraction.of(1, 2),
            Fraction.of(1, 2)
        )
        assertEq(Fraction.of(1, 2), result, "average(1/2,1/2)")
    }
    
    fun testMax() {
        val result = FractionUtils.max(
            Fraction.of(1, 3),
            Fraction.of(1, 2),
            Fraction.of(1, 4)
        )
        assertEq(Fraction.of(1, 2), result, "max")
    }
    
    fun testMin() {
        val result = FractionUtils.min(
            Fraction.of(1, 3),
            Fraction.of(1, 2),
            Fraction.of(1, 4)
        )
        assertEq(Fraction.of(1, 4), result, "min")
    }
    
    fun testAreEquivalent() {
        assertBool(FractionUtils.areEquivalent(Fraction.of(1, 2), Fraction.of(2, 4)), "等价判定-相等")
        assertBool(!FractionUtils.areEquivalent(Fraction.of(1, 2), Fraction.of(1, 3)), "等价判定-不等")
    }
    
    fun testIsBetween() {
        val lower = Fraction.of(1, 4)
        val upper = Fraction.of(3, 4)
        assertBool(FractionUtils.isBetween(Fraction.HALF, lower, upper), "isBetween-在范围内")
        assertBool(!FractionUtils.isBetween(Fraction.ONE, lower, upper), "isBetween-超出范围")
    }
    
    // ========== 连分数测试 ==========
    
    fun testContinuedFraction() {
        println("\n--- 连分数测试 ---")
        val cf = FractionUtils.continuedFraction(Fraction.of(355, 113))
        assertEq(listOf(3L, 7L, 16L), cf, "连分数展开(355/113)")
    }
    
    fun testFromContinuedFraction() {
        val cf = listOf(3L, 7L, 16L)
        val f = FractionUtils.fromContinuedFraction(cf)
        assertEq(355L, f.numerator, "连分数还原-分子")
        assertEq(113L, f.denominator, "连分数还原-分母")
    }
    
    fun testContinuedFractionRoundTrip() {
        val original = Fraction.of(22, 7)
        val cf = FractionUtils.continuedFraction(original)
        val restored = FractionUtils.fromContinuedFraction(cf)
        assertEq(original, restored, "连分数往返")
    }
    
    // ========== 埃及分数测试 ==========
    
    fun testEgyptianFraction() {
        println("\n--- 埃及分数测试 ---")
        val f = Fraction.of(2, 3)
        val egyptian = FractionUtils.egyptianFraction(f)
        
        var sum = Fraction.ZERO
        for (ef in egyptian) {
            assertEq(1L, ef.numerator, "埃及分数分子=1")
            sum = sum + ef
        }
        assertEq(f, sum, "埃及分数之和等于原分数")
    }
    
    fun testEgyptianFractionSimple() {
        val egyptian = FractionUtils.egyptianFraction(Fraction.of(5, 6))
        assertBool(egyptian.contains(Fraction.of(1, 2)), "5/6包含1/2")
        assertBool(egyptian.contains(Fraction.of(1, 3)), "5/6包含1/3")
    }
    
    // ========== 其他工具测试 ==========
    
    fun testDoubleToFraction() {
        println("\n--- 其他工具测试 ---")
        val f = FractionUtils.doubleToFraction(0.33333333)
        assertBool(abs(1.0 / 3.0 - f.doubleValue) < 0.0001, "doubleToFraction精度")
    }
    
    fun testIsPerfectSquare() {
        assertBool(FractionUtils.isPerfectSquare(Fraction.of(4, 9)), "完全平方-4/9")
        assertBool(!FractionUtils.isPerfectSquare(Fraction.of(2, 3)), "非完全平方-2/3")
        assertBool(!FractionUtils.isPerfectSquare(Fraction.of(-4, 9)), "负数非完全平方")
    }
    
    fun testSimplify() {
        val f = FractionUtils.simplify(8, 12)
        assertEq(2L, f.numerator, "simplify-分子")
        assertEq(3L, f.denominator, "simplify-分母")
    }
    
    fun testFindCommonDenominator() {
        val a = Fraction.of(1, 2)
        val b = Fraction.of(1, 3)
        val result = FractionUtils.findCommonDenominator(a, b)
        val (pairA, pairB) = result
        val (aNum, aDen) = pairA
        val (bNum, bDen) = pairB
        assertEq(aDen, bDen, "通分后分母相同")
        assertEq(3L, aNum, "a的新分子")
        assertEq(2L, bNum, "b的新分子")
    }
    
    // ========== 扩展函数测试 ==========
    
    fun testIntToFraction() {
        println("\n--- 扩展函数测试 ---")
        val f = 5.toFraction()
        assertEq(5L, f.numerator, "Int.toFraction")
        assertEq(1L, f.denominator, "Int.toFraction")
    }
    
    fun testLongToFraction() {
        val f = 123456789L.toFraction()
        assertEq(123456789L, f.numerator, "Long.toFraction")
        assertEq(1L, f.denominator, "Long.toFraction")
    }
    
    fun testDoubleToFractionExtension() {
        val f = 0.25.toFraction()
        assertEq(1L, f.numerator, "Double.toFraction")
        assertEq(4L, f.denominator, "Double.toFraction")
    }
    
    fun testStringToFractionExtension() {
        val f = "3/4".toFraction()
        assertEq(3L, f.numerator, "String.toFraction")
        assertEq(4L, f.denominator, "String.toFraction")
    }
    
    // ========== 边界情况测试 ==========
    
    fun testLargeNumbers() {
        println("\n--- 边界情况测试 ---")
        val a = Fraction.of(Long.MAX_VALUE / 2, 1)
        val b = Fraction.of(1, 2)
        val result = a + b
        assertBool(result.numerator > 0, "大数运算-正结果")
    }
    
    fun testVerySmallFraction() {
        val f = Fraction.of(1, 1000000)
        assertBool(abs(0.000001 - f.doubleValue) < 0.0000001, "极小分数精度")
    }
    
    fun testChainOperations() {
        val result = Fraction.of(1, 2) + Fraction.of(1, 3) - Fraction.of(1, 6)
        assertEq(Fraction.of(2, 3), result, "链式运算")
    }
    
    fun testComplexExpression() {
        val result = (Fraction.of(1, 2) + Fraction.of(1, 3)) *
                     (Fraction.of(2, 3) - Fraction.of(1, 4)) /
                     Fraction.of(1, 6)
        assertEq(Fraction.of(35, 12), result, "复杂表达式")
    }
    
    fun testZeroOperations() {
        assertEq(Fraction.of(1, 2), Fraction.of(1, 2) + Fraction.ZERO, "加零不变")
        assertEq(Fraction.of(1, 2), Fraction.of(1, 2) - Fraction.ZERO, "减零不变")
        assertEq(Fraction.ZERO, Fraction.of(1, 2) * Fraction.ZERO, "乘零得零")
    }
    
    fun testNegativeOperations() {
        val a = Fraction.of(-1, 2)
        val b = Fraction.of(-1, 3)
        assertEq(Fraction.of(-5, 6), a + b, "负数加法")
        assertEq(Fraction.of(-1, 6), a - b, "负数减法")
        assertEq(Fraction.of(1, 6), a * b, "负数乘法")
        assertEq(Fraction.of(3, 2), a / b, "负数除法")
    }
    
    fun testPrecisionConsistency() {
        val fractions = listOf(
            Fraction.of(1, 3),
            Fraction.of(1, 3),
            Fraction.of(1, 3)
        )
        val sum = FractionUtils.sum(*fractions.toTypedArray())
        assertEq(Fraction.ONE, sum, "分数精确相加")
        
        val doubleSum = 1.0 / 3.0 + 1.0 / 3.0 + 1.0 / 3.0
        assertBool(abs(1.0 - doubleSum) > 0.0, "浮点数不精确")
        assertBool(abs(1.0 - sum.doubleValue) < 0.0001, "分数精确=1")
    }
    
    // 运行所有测试
    fun runAllTests() {
        println("=" .repeat(60))
        println("Fraction Utils 单元测试")
        println("=" .repeat(60))
        
        testCreateBasicFraction()
        testCreateNegativeFraction()
        testCreateNegativeDenominator()
        testCreateBothNegative()
        testCreateWithZeroDenominator()
        testCreateSimplified()
        testCreateZero()
        
        testFromInt()
        testFromLong()
        testFromDouble()
        testFromDoubleRepeating()
        testFromDoubleNegative()
        testFromDoubleNaN()
        testFromDoubleInfinite()
        
        testParseFraction()
        testParseNegativeFraction()
        testParseInteger()
        testParseDecimal()
        testParseMixedNumber()
        testParseNegativeMixedNumber()
        
        testDoubleValue()
        testIntValue()
        testIntValueNegative()
        testIsNegative()
        testIsPositive()
        testIsZero()
        testIsInteger()
        testIsProperFraction()
        testWholePart()
        testFractionalPart()
        
        testAddition()
        testAdditionWithNegative()
        testSubtraction()
        testMultiplication()
        testDivision()
        testDivisionByZero()
        testUnaryMinus()
        testPow()
        testPowZero()
        testPowNegative()
        testReciprocal()
        testReciprocalOfZero()
        testAbs()
        
        testCeil()
        testFloor()
        testRound()
        
        testCompareTo()
        testEquals()
        testNotEquals()
        testHashCode()
        
        testToString()
        testToMixedString()
        testToDecimalString()
        
        testPredefinedConstants()
        
        testGcd()
        testLcm()
        testSum()
        testProduct()
        testAverage()
        testMax()
        testMin()
        testAreEquivalent()
        testIsBetween()
        
        testContinuedFraction()
        testFromContinuedFraction()
        testContinuedFractionRoundTrip()
        
        testEgyptianFraction()
        testEgyptianFractionSimple()
        
        testDoubleToFraction()
        testIsPerfectSquare()
        testSimplify()
        testFindCommonDenominator()
        
        testIntToFraction()
        testLongToFraction()
        testDoubleToFractionExtension()
        testStringToFractionExtension()
        
        testLargeNumbers()
        testVerySmallFraction()
        testChainOperations()
        testComplexExpression()
        testZeroOperations()
        testNegativeOperations()
        testPrecisionConsistency()
        
        println("\n" + "=" .repeat(60))
        println("测试结果: $passCount/$testCount 通过")
        println("=" .repeat(60))
    }
}

fun main() {
    FractionTest.runAllTests()
}