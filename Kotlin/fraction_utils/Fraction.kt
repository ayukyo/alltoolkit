/**
 * Fraction Utils - 精确分数计算工具库
 * 
 * 提供分数的创建、运算、比较和转换功能，避免浮点数精度问题
 * 零外部依赖，纯 Kotlin 标准库实现
 * 
 * @author AllToolkit
 * @date 2026-05-05
 */

package fraction_utils

import kotlin.math.abs
import kotlin.math.sqrt

/**
 * 分数类 - 表示一个精确的分数值
 * 
 * 分数始终以最简形式存储（分子和分母互质）
 * 支持负数分数，负号始终存储在分子上
 */
class Fraction private constructor(
    val numerator: Long,
    val denominator: Long
) : Comparable<Fraction> {
    
    companion object {
        /** 零 */
        val ZERO = Fraction(0L, 1L)
        
        /** 一 */
        val ONE = Fraction(1L, 1L)
        
        /** 二分之一 */
        val HALF = Fraction(1L, 2L)
        
        /** 四分之一 */
        val QUARTER = Fraction(1L, 4L)
        
        /** 负一 */
        val NEGATIVE_ONE = Fraction(-1L, 1L)
        
        /**
         * 从分子和分母创建分数
         * 
         * @param numerator 分子
         * @param denominator 分母（不能为零）
         * @return 分数实例
         * @throws IllegalArgumentException 如果分母为零
         */
        fun of(numerator: Long, denominator: Long): Fraction {
            if (denominator == 0L) {
                throw IllegalArgumentException("分母不能为零")
            }
            
            // 负号移到分子上
            var num = numerator
            var den = denominator
            if (den < 0) {
                num = -num
                den = -den
            }
            
            // 约分
            val gcd = gcd(abs(num), den)
            return Fraction(num / gcd, den / gcd)
        }
        
        /**
         * 从整数创建分数
         * 
         * @param value 整数值
         * @return 分数实例
         */
        fun fromInt(value: Int): Fraction = fromLong(value.toLong())
        
        /**
         * 从长整数创建分数
         * 
         * @param value 长整数值
         * @return 分数实例
         */
        fun fromLong(value: Long): Fraction = Fraction(value, 1L)
        
        /**
         * 从浮点数创建分数（精确转换）
         * 
         * @param value 浮点数值
         * @param maxDenominator 最大分母限制（默认10000）
         * @return 分数实例
         * @throws IllegalArgumentException 如果值为 NaN 或 Infinite
         */
        fun fromDouble(value: Double, maxDenominator: Long = 10000L): Fraction {
            if (value.isNaN() || value.isInfinite()) {
                throw IllegalArgumentException("无法将 NaN 或 Infinite 转换为分数")
            }
            
            if (value == 0.0) return ZERO
            
            val sign = if (value < 0) -1L else 1L
            val absValue = abs(value)
            
            // 使用连分数算法找到最佳近似
            return approximateFraction(absValue, maxDenominator).let {
                Fraction(sign * it.numerator, it.denominator)
            }
        }
        
        /**
         * 从字符串解析分数
         * 支持格式：
         * - "3/4" - 分数
         * - "-5/6" - 负分数
         * - "2" - 整数
         * - "2.5" - 小数
         * - "1 1/2" - 带分数
         * 
         * @param str 字符串
         * @return 分数实例
         * @throws IllegalArgumentException 如果格式无效
         */
        fun parse(str: String): Fraction {
            val trimmed = str.trim()
            
            // 尝试解析带分数 "1 1/2"
            if (' ' in trimmed) {
                val parts = trimmed.split(' ', limit = 2)
                if (parts.size == 2) {
                    val whole = parts[0].toLongOrNull()
                        ?: throw IllegalArgumentException("无效的带分数格式: $str")
                    val fraction = parse(parts[1])
                    return fromLong(whole) + fraction
                }
            }
            
            // 尝试解析普通分数 "3/4"
            if ('/' in trimmed) {
                val parts = trimmed.split('/', limit = 2)
                if (parts.size == 2) {
                    val num = parts[0].toLongOrNull()
                        ?: throw IllegalArgumentException("无效的分子: ${parts[0]}")
                    val den = parts[1].toLongOrNull()
                        ?: throw IllegalArgumentException("无效的分母: ${parts[1]}")
                    return of(num, den)
                }
            }
            
            // 尝试解析整数
            trimmed.toLongOrNull()?.let { return fromLong(it) }
            
            // 尝试解析小数
            trimmed.toDoubleOrNull()?.let { return fromDouble(it) }
            
            throw IllegalArgumentException("无效的分数格式: $str")
        }
        
        /**
         * 使用连分数算法近似
         */
        private fun approximateFraction(value: Double, maxDenominator: Long): Fraction {
            var a = value.toLong()
            var remainder = value - a
            var h0 = 1L
            var h1 = 0L
            var k0 = 0L
            var k1 = 1L
            
            for (i in 0 until 100) {
                val h = a * h1 + h0
                val k = a * k1 + k0
                
                if (k > maxDenominator) {
                    // 使用前一个近似
                    return Fraction(h1, k1)
                }
                
                h0 = h1
                h1 = h
                k0 = k1
                k1 = k
                
                if (remainder < 1e-15) break
                
                val inv = 1.0 / remainder
                a = inv.toLong()
                remainder = inv - a
            }
            
            return Fraction(h1, k1)
        }
        
        /**
         * 计算最大公约数
         */
        private fun gcd(a: Long, b: Long): Long {
            var x = a
            var y = b
            while (y != 0L) {
                val temp = y
                y = x % y
                x = temp
            }
            return x
        }
    }
    
    /**
     * 分数的浮点数值
     */
    val doubleValue: Double
        get() = numerator.toDouble() / denominator.toDouble()
    
    /**
     * 分数的整数值（向零取整）
     */
    val intValue: Int
        get() = (numerator / denominator).toInt()
    
    /**
     * 分数的长整数值（向零取整）
     */
    val longValue: Long
        get() = numerator / denominator
    
    /**
     * 是否为负数
     */
    val isNegative: Boolean
        get() = numerator < 0
    
    /**
     * 是否为正数
     */
    val isPositive: Boolean
        get() = numerator > 0
    
    /**
     * 是否为零
     */
    val isZero: Boolean
        get() = numerator == 0L
    
    /**
     * 是否为整数（分母为1）
     */
    val isInteger: Boolean
        get() = denominator == 1L
    
    /**
     * 是否为真分数（绝对值小于1）
     */
    val isProperFraction: Boolean
        get() = abs(numerator) < denominator
    
    /**
     * 获取整数部分
     */
    val wholePart: Long
        get() = numerator / denominator
    
    /**
     * 获取分数部分
     */
    val fractionalPart: Fraction
        get() = Fraction(abs(numerator) % denominator, denominator).let {
            if (numerator < 0 && !it.isZero) Fraction(-it.numerator, it.denominator) else it
        }
    
    /**
     * 加法
     */
    operator fun plus(other: Fraction): Fraction {
        val num = numerator * other.denominator + other.numerator * denominator
        val den = denominator * other.denominator
        return of(num, den)
    }
    
    /**
     * 减法
     */
    operator fun minus(other: Fraction): Fraction {
        val num = numerator * other.denominator - other.numerator * denominator
        val den = denominator * other.denominator
        return of(num, den)
    }
    
    /**
     * 乘法
     */
    operator fun times(other: Fraction): Fraction {
        return of(numerator * other.numerator, denominator * other.denominator)
    }
    
    /**
     * 除法
     */
    operator fun div(other: Fraction): Fraction {
        if (other.isZero) {
            throw ArithmeticException("除数不能为零")
        }
        return of(numerator * other.denominator, denominator * other.numerator)
    }
    
    /**
     * 取负
     */
    operator fun unaryMinus(): Fraction = Fraction(-numerator, denominator)
    
    /**
     * 幂运算
     * 
     * @param exponent 指数（整数）
     * @return 结果
     */
    fun pow(exponent: Int): Fraction {
        if (exponent == 0) return ONE
        if (isZero) return ZERO
        
        return when {
            exponent > 0 -> {
                var result = ONE
                repeat(exponent) { result = result * this }
                result
            }
            else -> {
                if (isZero) throw ArithmeticException("零不能有负指数")
                reciprocal().pow(-exponent)
            }
        }
    }
    
    /**
     * 倒数
     */
    fun reciprocal(): Fraction {
        if (isZero) {
            throw ArithmeticException("零没有倒数")
        }
        return Fraction(denominator * if (numerator < 0) -1 else 1, abs(numerator))
    }
    
    /**
     * 绝对值
     */
    fun abs(): Fraction = Fraction(kotlin.math.abs(numerator), denominator)
    
    /**
     * 向上取整
     */
    fun ceil(): Fraction {
        if (isInteger) return this
        return if (isPositive) {
            Fraction(numerator / denominator + 1, 1L)
        } else {
            Fraction(numerator / denominator, 1L)
        }
    }
    
    /**
     * 向下取整
     */
    fun floor(): Fraction {
        if (isInteger) return this
        return if (isPositive) {
            Fraction(numerator / denominator, 1L)
        } else {
            Fraction(numerator / denominator - 1, 1L)
        }
    }
    
    /**
     * 四舍五入
     */
    fun round(): Fraction {
        return (this + Fraction(1, 2)).floor()
    }
    
    /**
     * 比较运算符
     */
    override fun compareTo(other: Fraction): Int {
        val diff = numerator * other.denominator - other.numerator * denominator
        return when {
            diff > 0 -> 1
            diff < 0 -> -1
            else -> 0
        }
    }
    
    /**
     * 相等判断（基于值）
     */
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is Fraction) return false
        return numerator == other.numerator && denominator == other.denominator
    }
    
    override fun hashCode(): Int {
        return 31 * numerator.hashCode() + denominator.hashCode()
    }
    
    /**
     * 转换为字符串（如 "3/4"）
     */
    override fun toString(): String {
        return if (denominator == 1L) {
            numerator.toString()
        } else {
            "$numerator/$denominator"
        }
    }
    
    /**
     * 转换为带分数字符串（如 "1 1/2"）
     */
    fun toMixedString(): String {
        if (isInteger || isProperFraction) {
            return toString()
        }
        val whole = abs(wholePart)
        val frac = fractionalPart.abs()
        val sign = if (isNegative) "-" else ""
        return if (frac.isZero) {
            "$sign$whole"
        } else {
            "$sign$whole $frac"
        }
    }
    
    /**
     * 转换为小数字符串
     * 
     * @param decimals 小数位数
     * @return 小数字符串
     */
    fun toDecimalString(decimals: Int = 6): String {
        val formatStr = "%.${decimals}f"
        return formatStr.format(doubleValue)
    }
}

/**
 * 分数工具类 - 提供静态方法
 */
object FractionUtils {
    
    /**
     * 最大公约数
     */
    fun gcd(a: Long, b: Long): Long {
        var x = abs(a)
        var y = abs(b)
        while (y != 0L) {
            val temp = y
            y = x % y
            x = temp
        }
        return x
    }
    
    /**
     * 最小公倍数
     */
    fun lcm(a: Long, b: Long): Long {
        if (a == 0L || b == 0L) return 0L
        return abs(a / gcd(a, b) * b)
    }
    
    /**
     * 求多个分数的和
     */
    fun sum(vararg fractions: Fraction): Fraction {
        return fractions.fold(Fraction.ZERO) { acc, f -> acc + f }
    }
    
    /**
     * 求多个分数的积
     */
    fun product(vararg fractions: Fraction): Fraction {
        return fractions.fold(Fraction.ONE) { acc, f -> acc * f }
    }
    
    /**
     * 求分数的平均值
     */
    fun average(vararg fractions: Fraction): Fraction {
        if (fractions.isEmpty()) return Fraction.ZERO
        return sum(*fractions) / Fraction.fromInt(fractions.size)
    }
    
    /**
     * 找出最大分数
     */
    fun max(vararg fractions: Fraction): Fraction {
        if (fractions.isEmpty()) throw IllegalArgumentException("至少需要一个分数")
        return fractions.reduce { max, f -> if (f > max) f else max }
    }
    
    /**
     * 找出最小分数
     */
    fun min(vararg fractions: Fraction): Fraction {
        if (fractions.isEmpty()) throw IllegalArgumentException("至少需要一个分数")
        return fractions.reduce { min, f -> if (f < min) f else min }
    }
    
    /**
     * 检查两个分数是否等价（值相等）
     */
    fun areEquivalent(a: Fraction, b: Fraction): Boolean = a == b
    
    /**
     * 检查一个值是否在两个分数之间
     */
    fun isBetween(value: Fraction, lower: Fraction, upper: Fraction): Boolean {
        return value >= min(lower, upper) && value <= max(lower, upper)
    }
    
    /**
     * 创建分数范围
     */
    fun range(start: Fraction, endInclusive: Fraction): FractionRange {
        return FractionRange(min(start, endInclusive), max(start, endInclusive))
    }
    
    /**
     * 分数范围类
     */
    class FractionRange(
        override val start: Fraction,
        override val endInclusive: Fraction
    ) : ClosedRange<Fraction>
    
    /**
     * 连分数展开
     * 返回连分数的各项系数
     */
    fun continuedFraction(fraction: Fraction): List<Long> {
        if (fraction.isZero) return listOf(0L)
        
        val result = mutableListOf<Long>()
        var num = abs(fraction.numerator)
        var den = fraction.denominator
        
        while (den != 0L) {
            result.add(num / den)
            val remainder = num % den
            num = den
            den = remainder
            if (remainder == 0L) break
        }
        
        return result
    }
    
    /**
     * 从连分数还原分数
     */
    fun fromContinuedFraction(coefficients: List<Long>): Fraction {
        if (coefficients.isEmpty()) return Fraction.ZERO
        
        var numerator = coefficients.last()
        var denominator = 1L
        
        for (i in coefficients.size - 2 downTo 0) {
            val temp = denominator
            denominator = numerator
            numerator = coefficients[i] * numerator + temp
        }
        
        return Fraction.of(numerator, denominator)
    }
    
    /**
     * 求分数的埃及分数表示
     * 埃及分数：分子为1的分数之和
     * 使用贪婪算法
     */
    fun egyptianFraction(fraction: Fraction): List<Fraction> {
        if (fraction.isZero) return emptyList()
        
        val result = mutableListOf<Fraction>()
        var num = abs(fraction.numerator)
        var den = fraction.denominator
        
        while (num != 0L) {
            // 找最小的整数 x 使得 1/x <= num/den
            val x = (den + num - 1) / num  // 向上取整
            result.add(Fraction.ONE / Fraction.of(x, 1L))
            
            // num/den - 1/x = (num*x - den) / (den*x)
            val newNum = num * x - den
            val newDen = den * x
            
            // 约分
            val g = gcd(newNum, newDen)
            num = newNum / g
            den = newDen / g
        }
        
        return result
    }
    
    /**
     * 将小数转换为分数（指定精度范围）
     */
    fun doubleToFraction(value: Double, tolerance: Double = 1e-10): Fraction {
        if (value == 0.0) return Fraction.ZERO
        
        val sign = if (value < 0) -1 else 1
        var num = abs(value)
        var den = 1L
        
        while (abs(num - num.toLong().toDouble()) > tolerance && den < Long.MAX_VALUE / 10) {
            num *= 10
            den *= 10
        }
        
        return Fraction.of(sign * num.toLong(), den)
    }
    
    /**
     * 判断是否为完全平方数的分数
     */
    fun isPerfectSquare(fraction: Fraction): Boolean {
        if (fraction.isNegative) return false
        
        val numSqrt = sqrt(fraction.numerator.toDouble())
        val denSqrt = sqrt(fraction.denominator.toDouble())
        
        val numSq = numSqrt.toLong()
        val denSq = denSqrt.toLong()
        
        return numSq * numSq == fraction.numerator && denSq * denSq == fraction.denominator
    }
    
    /**
     * 约分到最简
     */
    fun simplify(numerator: Long, denominator: Long): Fraction {
        return Fraction.of(numerator, denominator)
    }
    
    /**
     * 通分
     * 返回两个分数通分后的新分子分母对
     */
    fun findCommonDenominator(a: Fraction, b: Fraction): Pair<Pair<Long, Long>, Pair<Long, Long>> {
        val lcm = lcm(a.denominator, b.denominator)
        val aNewNum = a.numerator * (lcm / a.denominator)
        val bNewNum = b.numerator * (lcm / b.denominator)
        return (aNewNum to lcm) to (bNewNum to lcm)
    }
}

// 扩展函数 - 方便从数字创建分数

/**
 * Int 转 Fraction
 */
fun Int.toFraction(): Fraction = Fraction.fromInt(this)

/**
 * Long 转 Fraction
 */
fun Long.toFraction(): Fraction = Fraction.fromLong(this)

/**
 * Double 转 Fraction
 */
fun Double.toFraction(maxDenominator: Long = 10000L): Fraction = Fraction.fromDouble(this, maxDenominator)

/**
 * String 转 Fraction
 */
fun String.toFraction(): Fraction = Fraction.parse(this)