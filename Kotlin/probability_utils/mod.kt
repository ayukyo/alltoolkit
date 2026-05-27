/**
 * AllToolkit - Kotlin Probability Utilities
 *
 * 零依赖的概率分布工具模块，仅使用 Kotlin/Java 标准库
 * 支持：常见分布的概率密度、累积分布、分位数、随机数生成
 * 
 * 分布：均匀分布、正态分布、指数分布、泊松分布、二项分布、
 *       Beta分布、Gamma分布、卡方分布、t分布、F分布
 *
 * @author AllToolkit
 * @version 1.0.0
 */

package probability_utils

import kotlin.math.*
import java.util.Random

// 辅助函数：使用 Java Math.pow
private fun pow(a: Double, b: Double): Double = Math.pow(a, b)

/**
 * 概率分布工具类
 */
object ProbabilityUtils {
    
    private val random = Random()
    
    // ==================== 数学常量 ====================
    
    const val PI = 3.14159265358979323846
    const val E = 2.71828182845904523536
    const val SQRT2 = 1.41421356237309504880
    const val SQRT2PI = 2.50662827463100050242
    
    // ==================== 均匀分布 ====================
    
    /**
     * 均匀分布概率密度函数
     * PDF(x) = 1/(b-a) for a <= x <= b
     */
    fun uniformPdf(x: Double, a: Double = 0.0, b: Double = 1.0): Double {
        if (b <= a) throw IllegalArgumentException("b must be greater than a")
        return if (x >= a && x <= b) 1.0 / (b - a) else 0.0
    }
    
    /**
     * 均匀分布累积分布函数
     * CDF(x) = (x-a)/(b-a) for a <= x <= b
     */
    fun uniformCdf(x: Double, a: Double = 0.0, b: Double = 1.0): Double {
        if (b <= a) throw IllegalArgumentException("b must be greater than a")
        return when {
            x < a -> 0.0
            x > b -> 1.0
            else -> (x - a) / (b - a)
        }
    }
    
    /**
     * 均匀分布分位数函数（逆CDF）
     */
    fun uniformQuantile(p: Double, a: Double = 0.0, b: Double = 1.0): Double {
        if (p < 0.0 || p > 1.0) throw IllegalArgumentException("p must be in [0, 1]")
        if (b <= a) throw IllegalArgumentException("b must be greater than a")
        return a + p * (b - a)
    }
    
    /**
     * 生成均匀分布随机数
     */
    fun uniformRandom(a: Double = 0.0, b: Double = 1.0): Double {
        if (b <= a) throw IllegalArgumentException("b must be greater than a")
        return a + random.nextDouble() * (b - a)
    }
    
    // ==================== 正态分布 ====================
    
    /**
     * 正态分布概率密度函数
     * PDF(x) = (1/(σ√(2π))) * exp(-(x-μ)^2/(2σ^2))
     */
    fun normalPdf(x: Double, mean: Double = 0.0, stdDev: Double = 1.0): Double {
        if (stdDev <= 0) throw IllegalArgumentException("stdDev must be positive")
        val z = (x - mean) / stdDev
        return exp(-z * z / 2.0) / (stdDev * SQRT2PI)
    }
    
    /**
     * 正态分布累积分布函数（近似计算）
     * 使用 Abramowitz 和 Stegun 近似
     */
    fun normalCdf(x: Double, mean: Double = 0.0, stdDev: Double = 1.0): Double {
        if (stdDev <= 0) throw IllegalArgumentException("stdDev must be positive")
        val z = (x - mean) / stdDev
        
        // Abramowitz 和 Stegun 近似系数
        val b0 = 0.2316419
        val b1 = 0.319381530
        val b2 = -0.356563782
        val b3 = 1.781477937
        val b4 = -1.821255978
        val b5 = 1.330274429
        
        val sign = if (z < 0) -1 else 1
        val absZ = abs(z)
        
        if (absZ > 8.0) return if (z < 0) 0.0 else 1.0
        
        val t = 1.0 / (1.0 + b0 * absZ)
        val pdf = normalPdf(absZ, 0.0, 1.0)
        val cdf = 1.0 - pdf * t * (b1 + t * (b2 + t * (b3 + t * (b4 + t * b5))))
        
        return if (z < 0) 1.0 - cdf else cdf
    }
    
    /**
     * 正态分布分位数函数（近似计算）
     * 使用 Beasley-Springer-Moro 算法
     */
    fun normalQuantile(p: Double, mean: Double = 0.0, stdDev: Double = 1.0): Double {
        if (p <= 0.0 || p >= 1.0) throw IllegalArgumentException("p must be in (0, 1)")
        if (stdDev <= 0) throw IllegalArgumentException("stdDev must be positive")
        
        val a0 = 2.50662823884
        val a1 = -18.61500062529
        val a2 = 41.39119773534
        val a3 = -25.44106049637
        
        val b0 = -8.47351093090
        val b1 = 23.08336743743
        val b2 = -21.06224101826
        val b3 = 3.13082909833
        
        val c0 = 0.3374754822726147
        val c1 = 0.9761690190917186
        val c2 = 0.1607979714918209
        val c3 = 0.0276438810333863
        val c4 = 0.0038405729373609
        val c5 = 0.0003951896511919
        val c6 = 0.0000321767881768
        val c7 = 0.0000002888167364
        val c8 = 0.0000003960315187
        
        val q = min(p, 1.0 - p)
        val sign = if (p < 0.5) -1 else 1
        
        var z: Double
        
        if (q > 0.08) {
            val r = sqrt(-2.0 * ln(q))
            z = r - (a0 + r * (a1 + r * (a2 + r * a3))) / 
                (1.0 + r * (b0 + r * (b1 + r * (b2 + r * b3))))
        } else {
            val r = ln(-ln(q))
            z = c0 + r * (c1 + r * (c2 + r * (c3 + r * (c4 + r * (c5 + r * (c6 + r * (c7 + r * c8)))))))
        }
        
        return mean + sign * stdDev * z
    }
    
    /**
     * 生成正态分布随机数（Box-Muller 变换）
     */
    fun normalRandom(mean: Double = 0.0, stdDev: Double = 1.0): Double {
        if (stdDev <= 0) throw IllegalArgumentException("stdDev must be positive")
        
        val u1 = random.nextDouble()
        val u2 = random.nextDouble()
        
        val z0 = sqrt(-2.0 * ln(u1)) * cos(2.0 * PI * u2)
        
        return mean + stdDev * z0
    }
    
    /**
     * 生成多个正态分布随机数
     */
    fun normalRandoms(n: Int, mean: Double = 0.0, stdDev: Double = 1.0): List<Double> {
        if (n <= 0) throw IllegalArgumentException("n must be positive")
        return (1..n).map { normalRandom(mean, stdDev) }
    }
    
    // ==================== 指数分布 ====================
    
    /**
     * 指数分布概率密度函数
     * PDF(x) = λ * exp(-λx) for x >= 0
     */
    fun exponentialPdf(x: Double, lambda: Double = 1.0): Double {
        if (lambda <= 0) throw IllegalArgumentException("lambda must be positive")
        return if (x >= 0) lambda * exp(-lambda * x) else 0.0
    }
    
    /**
     * 指数分布累积分布函数
     * CDF(x) = 1 - exp(-λx) for x >= 0
     */
    fun exponentialCdf(x: Double, lambda: Double = 1.0): Double {
        if (lambda <= 0) throw IllegalArgumentException("lambda must be positive")
        return if (x >= 0) 1.0 - exp(-lambda * x) else 0.0
    }
    
    /**
     * 指数分布分位数函数
     */
    fun exponentialQuantile(p: Double, lambda: Double = 1.0): Double {
        if (p < 0.0 || p > 1.0) throw IllegalArgumentException("p must be in [0, 1)")
        if (lambda <= 0) throw IllegalArgumentException("lambda must be positive")
        return -ln(1.0 - p) / lambda
    }
    
    /**
     * 生成指数分布随机数
     */
    fun exponentialRandom(lambda: Double = 1.0): Double {
        if (lambda <= 0) throw IllegalArgumentException("lambda must be positive")
        return -ln(random.nextDouble()) / lambda
    }
    
    // ==================== 泊松分布 ====================
    
    /**
     * 泊松分布概率质量函数
     * PMF(k) = (λ^k * exp(-λ)) / k!
     */
    fun poissonPmf(k: Int, lambda: Double): Double {
        if (lambda <= 0) throw IllegalArgumentException("lambda must be positive")
        if (k < 0) return 0.0
        return exp(-lambda) * pow(lambda, k.toDouble()) / factorial(k)
    }
    
    /**
     * 泊松分布累积分布函数
     */
    fun poissonCdf(k: Int, lambda: Double): Double {
        if (lambda <= 0) throw IllegalArgumentException("lambda must be positive")
        if (k < 0) return 0.0
        var sum = 0.0
        for (i in 0..k) {
            sum += poissonPmf(i, lambda)
        }
        return sum
    }
    
    /**
     * 生成泊松分布随机数（Knuth 算法）
     */
    fun poissonRandom(lambda: Double): Int {
        if (lambda <= 0) throw IllegalArgumentException("lambda must be positive")
        val L = exp(-lambda)
        var k = 0
        var p = 1.0
        
        do {
            k++
            p *= random.nextDouble()
        } while (p > L)
        
        return k - 1
    }
    
    // ==================== 二项分布 ====================
    
    /**
     * 二项分布概率质量函数
     * PMF(k) = C(n,k) * p^k * (1-p)^(n-k)
     */
    fun binomialPmf(k: Int, n: Int, p: Double): Double {
        if (n < 0) throw IllegalArgumentException("n must be non-negative")
        if (p < 0.0 || p > 1.0) throw IllegalArgumentException("p must be in [0, 1]")
        if (k < 0 || k > n) return 0.0
        
        return binomialCoefficient(n, k) * pow(p, k.toDouble()) * pow(1.0 - p, (n - k).toDouble())
    }
    
    /**
     * 二项分布累积分布函数
     */
    fun binomialCdf(k: Int, n: Int, p: Double): Double {
        if (n < 0) throw IllegalArgumentException("n must be non-negative")
        if (p < 0.0 || p > 1.0) throw IllegalArgumentException("p must be in [0, 1]")
        if (k < 0) return 0.0
        if (k >= n) return 1.0
        
        var sum = 0.0
        for (i in 0..min(k, n)) {
            sum += binomialPmf(i, n, p)
        }
        return sum
    }
    
    /**
     * 生成二项分布随机数
     */
    fun binomialRandom(n: Int, p: Double): Int {
        if (n < 0) throw IllegalArgumentException("n must be non-negative")
        if (p < 0.0 || p > 1.0) throw IllegalArgumentException("p must be in [0, 1]")
        
        var successes = 0
        for (i in 0 until n) {
            if (random.nextDouble() < p) successes++
        }
        return successes
    }
    
    // ==================== Beta 分布 ====================
    
    /**
     * Beta 分布概率密度函数（简化近似）
     * 使用 Gamma 函数比值
     */
    fun betaPdf(x: Double, alpha: Double, beta: Double): Double {
        if (alpha <= 0 || beta <= 0) throw IllegalArgumentException("alpha and beta must be positive")
        if (x < 0.0 || x > 1.0) return 0.0
        
        val logPdf = (alpha - 1.0) * ln(x) + (beta - 1.0) * ln(1.0 - x) - 
                     logBeta(alpha, beta)
        return exp(logPdf)
    }
    
    /**
     * Beta 分布累积分布函数（近似）
     */
    fun betaCdf(x: Double, alpha: Double, beta: Double): Double {
        if (alpha <= 0 || beta <= 0) throw IllegalArgumentException("alpha and beta must be positive")
        if (x < 0.0) return 0.0
        if (x > 1.0) return 1.0
        
        // 使用不完全 Beta 函数近似
        return incompleteBeta(x, alpha, beta)
    }
    
    /**
     * 生成 Beta 分布随机数
     */
    fun betaRandom(alpha: Double, beta: Double): Double {
        if (alpha <= 0 || beta <= 0) throw IllegalArgumentException("alpha and beta must be positive")
        
        val x = gammaRandom(alpha, 1.0)
        val y = gammaRandom(beta, 1.0)
        
        return x / (x + y)
    }
    
    // ==================== Gamma 分布 ====================
    
    /**
     * Gamma 分布概率密度函数
     */
    fun gammaPdf(x: Double, alpha: Double, beta: Double = 1.0): Double {
        if (alpha <= 0 || beta <= 0) throw IllegalArgumentException("alpha and beta must be positive")
        if (x < 0.0) return 0.0
        
        val logPdf = (alpha - 1.0) * ln(x) - x / beta - alpha * ln(beta) - logGamma(alpha)
        return exp(logPdf)
    }
    
    /**
     * Gamma 分布累积分布函数（近似）
     */
    fun gammaCdf(x: Double, alpha: Double, beta: Double = 1.0): Double {
        if (alpha <= 0 || beta <= 0) throw IllegalArgumentException("alpha and beta must be positive")
        if (x < 0.0) return 0.0
        
        return lowerIncompleteGamma(x / beta, alpha) / gamma(alpha)
    }
    
    /**
     * 生成 Gamma 分布随机数（Marsaglia 方法）
     */
    fun gammaRandom(alpha: Double, beta: Double = 1.0): Double {
        if (alpha <= 0 || beta <= 0) throw IllegalArgumentException("alpha and beta must be positive")
        
        if (alpha < 1.0) {
            // 使用 alpha + 1 的方法并调整
            val u = random.nextDouble()
            return gammaRandom(alpha + 1.0, beta) * pow(u, 1.0 / alpha)
        }
        
        val d = alpha - 1.0 / 3.0
        val c = 1.0 / sqrt(9.0 * d)
        
        while (true) {
            var x = normalRandom(0.0, 1.0)
            var v = 1.0 + c * x
            
            while (v <= 0) {
                x = normalRandom(0.0, 1.0)
                v = 1.0 + c * x
            }
            
            v = v * v * v
            val u = random.nextDouble()
            
            if (u < 1.0 - 0.0331 * (x * x) * (x * x)) {
                return d * v * beta
            }
            
            if (ln(u) < 0.5 * x * x + d * (1.0 - v + ln(v))) {
                return d * v * beta
            }
        }
    }
    
    // ==================== 卡方分布 ====================
    
    /**
     * 卡方分布概率密度函数
     * PDF(x) = (x^(k/2-1) * exp(-x/2)) / (2^(k/2) * Γ(k/2))
     */
    fun chiSquaredPdf(x: Double, df: Int): Double {
        if (df <= 0) throw IllegalArgumentException("df must be positive")
        if (x < 0.0) return 0.0
        
        return gammaPdf(x, df.toDouble() / 2.0, 2.0)
    }
    
    /**
     * 卡方分布累积分布函数
     */
    fun chiSquaredCdf(x: Double, df: Int): Double {
        if (df <= 0) throw IllegalArgumentException("df must be positive")
        if (x < 0.0) return 0.0
        
        return gammaCdf(x, df.toDouble() / 2.0, 2.0)
    }
    
    /**
     * 生成卡方分布随机数
     */
    fun chiSquaredRandom(df: Int): Double {
        if (df <= 0) throw IllegalArgumentException("df must be positive")
        
        var sum = 0.0
        for (i in 0 until df) {
            val z = normalRandom(0.0, 1.0)
            sum += z * z
        }
        return sum
    }
    
    // ==================== t 分布 ====================
    
    /**
     * t 分布概率密度函数
     */
    fun tPdf(x: Double, df: Int): Double {
        if (df <= 0) throw IllegalArgumentException("df must be positive")
        
        val coef = gamma((df + 1.0) / 2.0) / (sqrt(df * PI) * gamma(df.toDouble() / 2.0))
        val term = pow(1.0 + x * x / df, -(df + 1.0) / 2.0)
        
        return coef * term
    }
    
    /**
     * t 分布累积分布函数（近似）
     */
    fun tCdf(x: Double, df: Int): Double {
        if (df <= 0) throw IllegalArgumentException("df must be positive")
        
        // 使用正态近似对于大 df
        if (df >= 30) {
            return normalCdf(x, 0.0, 1.0)
        }
        
        // 使用不完全 Beta 函数
        val t = abs(x)
        val p = incompleteBeta(df.toDouble() / (df + t * t), df.toDouble() / 2.0, 0.5)
        
        return if (x < 0) p else 1.0 - p
    }
    
    /**
     * 生成 t 分布随机数
     */
    fun tRandom(df: Int): Double {
        if (df <= 0) throw IllegalArgumentException("df must be positive")
        
        val z = normalRandom(0.0, 1.0)
        val v = chiSquaredRandom(df)
        
        return z / sqrt(v / df)
    }
    
    // ==================== F 分布 ====================
    
    /**
     * F 分布概率密度函数
     */
    fun fPdf(x: Double, df1: Int, df2: Int): Double {
        if (df1 <= 0 || df2 <= 0) throw IllegalArgumentException("df must be positive")
        if (x < 0.0) return 0.0
        
        val coef = gamma((df1 + df2) / 2.0) / 
                   (gamma(df1.toDouble() / 2.0) * gamma(df2.toDouble() / 2.0))
        val term1 = pow(df1.toDouble() / df2, df1.toDouble() / 2.0)
        val term2 = pow(x, (df1 - 2) / 2.0)
        val term3 = pow(1.0 + df1.toDouble() * x / df2, -(df1 + df2) / 2.0)
        
        return coef * term1 * term2 * term3
    }
    
    /**
     * F 分布累积分布函数（近似）
     */
    fun fCdf(x: Double, df1: Int, df2: Int): Double {
        if (df1 <= 0 || df2 <= 0) throw IllegalArgumentException("df must be positive")
        if (x < 0.0) return 0.0
        
        val p = df2.toDouble() / (df2 + df1.toDouble() * x)
        return incompleteBeta(p, df2.toDouble() / 2.0, df1.toDouble() / 2.0)
    }
    
    /**
     * 生成 F 分布随机数
     */
    fun fRandom(df1: Int, df2: Int): Double {
        if (df1 <= 0 || df2 <= 0) throw IllegalArgumentException("df must be positive")
        
        val u1 = chiSquaredRandom(df1) / df1
        val u2 = chiSquaredRandom(df2) / df2
        
        return u1 / u2
    }
    
    // ==================== 几何分布 ====================
    
    /**
     * 几何分布概率质量函数（首次成功在第 k 次试验）
     * PMF(k) = (1-p)^(k-1) * p
     */
    fun geometricPmf(k: Int, p: Double): Double {
        if (p <= 0.0 || p > 1.0) throw IllegalArgumentException("p must be in (0, 1]")
        if (k < 1) return 0.0
        
        return pow(1.0 - p, (k - 1).toDouble()) * p
    }
    
    /**
     * 几何分布累积分布函数
     */
    fun geometricCdf(k: Int, p: Double): Double {
        if (p <= 0.0 || p > 1.0) throw IllegalArgumentException("p must be in (0, 1]")
        if (k < 1) return 0.0
        
        return 1.0 - pow(1.0 - p, k.toDouble())
    }
    
    /**
     * 生成几何分布随机数
     */
    fun geometricRandom(p: Double): Int {
        if (p <= 0.0 || p > 1.0) throw IllegalArgumentException("p must be in (0, 1]")
        
        var k = 1
        while (random.nextDouble() > p) k++
        return k
    }
    
    // ==================== 负二项分布 ====================
    
    /**
     * 负二项分布概率质量函数
     * 在第 k 次试验时达到 r 次成功的概率
     */
    fun negativeBinomialPmf(k: Int, r: Int, p: Double): Double {
        if (r <= 0) throw IllegalArgumentException("r must be positive")
        if (p <= 0.0 || p > 1.0) throw IllegalArgumentException("p must be in (0, 1]")
        if (k < r) return 0.0
        
        return binomialCoefficient(k - 1, r - 1) * 
               pow(p, r.toDouble()) * pow(1.0 - p, (k - r).toDouble())
    }
    
    /**
     * 生成负二项分布随机数
     */
    fun negativeBinomialRandom(r: Int, p: Double): Int {
        if (r <= 0) throw IllegalArgumentException("r must be positive")
        if (p <= 0.0 || p > 1.0) throw IllegalArgumentException("p must be in (0, 1]")
        
        var successes = 0
        var trials = 0
        
        while (successes < r) {
            trials++
            if (random.nextDouble() < p) successes++
        }
        
        return trials
    }
    
    // ==================== 辅助函数 ====================
    
    /**
     * 阶乘计算
     */
    fun factorial(n: Int): Double {
        if (n < 0) throw IllegalArgumentException("n must be non-negative")
        if (n <= 1) return 1.0
        
        var result = 1.0
        for (i in 2..n) result *= i
        return result
    }
    
    /**
     * 阶乘的对数（避免大数溢出）
     */
    fun logFactorial(n: Int): Double {
        if (n < 0) throw IllegalArgumentException("n must be non-negative")
        if (n <= 1) return 0.0
        
        var result = 0.0
        for (i in 2..n) result += ln(i.toDouble())
        return result
    }
    
    /**
     * 组合数 C(n, k)
     */
    fun binomialCoefficient(n: Int, k: Int): Double {
        if (n < 0 || k < 0 || k > n) throw IllegalArgumentException("invalid n, k values")
        
        val k2 = min(k, n - k)
        
        var result = 1.0
        for (i in 0 until k2) {
            result = result * (n - i) / (k2 - i)
        }
        return result
    }
    
    /**
     * Gamma 函数（近似计算）
     */
    fun gamma(x: Double): Double {
        if (x <= 0) throw IllegalArgumentException("x must be positive")
        
        // Lanczos 近似
        val g = 7
        val coefficients = doubleArrayOf(
            0.99999999999980993,
            676.5203681218851,
            -1259.1392167224028,
            771.32342877765313,
            -176.61502916214059,
            12.507343278686905,
            -0.13857109526572012,
            9.9843695780195716e-6,
            1.5056327351493116e-7
        )
        
        val x2 = if (x < 0.5) 1.0 - x else x
        
        var a = coefficients[0]
        for (i in 1..g + 1) {
            a += coefficients[i] / (x2 + i - 1)
        }
        
        val t = x2 + g + 0.5
        
        val result = sqrt(2.0 * PI) * pow(t, x2 + 0.5) * exp(-t) * a
        
        return if (x < 0.5) PI / (sin(PI * x) * result) else result
    }
    
    /**
     * Gamma 函数的对数
     */
    fun logGamma(x: Double): Double {
        if (x <= 0) throw IllegalArgumentException("x must be positive")
        return ln(gamma(x))
    }
    
    /**
     * Beta 函数
     */
    fun beta(alpha: Double, beta: Double): Double {
        if (alpha <= 0 || beta <= 0) throw IllegalArgumentException("alpha and beta must be positive")
        return gamma(alpha) * gamma(beta) / gamma(alpha + beta)
    }
    
    /**
     * Beta 函数的对数
     */
    fun logBeta(alpha: Double, beta: Double): Double {
        if (alpha <= 0 || beta <= 0) throw IllegalArgumentException("alpha and beta must be positive")
        return logGamma(alpha) + logGamma(beta) - logGamma(alpha + beta)
    }
    
    /**
     * 不完全 Beta 函数（近似）
     */
    fun incompleteBeta(x: Double, a: Double, b: Double): Double {
        if (x < 0.0 || x > 1.0) throw IllegalArgumentException("x must be in [0, 1]")
        if (a <= 0 || b <= 0) throw IllegalArgumentException("a and b must be positive")
        
        // 使用连分式展开近似
        val maxIterations = 200
        val epsilon = 1e-10
        
        val bt = if (x == 0.0 || x == 1.0) 0.0 else
            exp(logGamma(a + b) - logGamma(a) - logGamma(b) + 
                a * ln(x) + b * ln(1.0 - x))
        
        if (x < (a + 1.0) / (a + b + 2.0)) {
            // 使用前向递推
            var a0 = 1.0
            var a1 = 1.0
            var b0 = 0.0
            var b1 = 1.0
            
            val qab = a + b
            val qap = a + 1.0
            val qam = a - 1.0
            var c = 1.0
            var d = 1.0 - qab * x / qap
            
            if (abs(d) < epsilon) d = epsilon
            d = 1.0 / d
            var h = d
            
            for (m in 1..maxIterations) {
                val m2 = 2 * m
                val aa = m * (b - m) * x / ((qam + m2) * (a + m2))
                
                d = 1.0 + aa * d
                if (abs(d) < epsilon) d = epsilon
                d = 1.0 / d
                
                c = 1.0 + aa * c
                if (abs(c) < epsilon) c = epsilon
                
                h *= d * c
                val aaa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
                
                d = 1.0 + aaa * d
                if (abs(d) < epsilon) d = epsilon
                d = 1.0 / d
                
                c = 1.0 + aaa * c
                if (abs(c) < epsilon) c = epsilon
                
                val delta = d * c
                h *= delta
                
                if (abs(delta - 1.0) < epsilon) break
            }
            
            return bt * h / a
        } else {
            // 使用后向递推
            return 1.0 - incompleteBeta(1.0 - x, b, a)
        }
    }
    
    /**
     * 下不完全 Gamma 函数（近似）
     */
    fun lowerIncompleteGamma(x: Double, a: Double): Double {
        if (x < 0) throw IllegalArgumentException("x must be non-negative")
        if (a <= 0) throw IllegalArgumentException("a must be positive")
        
        // 使用连分式展开
        val maxIterations = 200
        val epsilon = 1e-10
        
        var sum = 1.0 / a
        var term = 1.0 / a
        
        for (n in 1..maxIterations) {
            term *= x / (a + n)
            sum += term
            
            if (abs(term) < abs(sum) * epsilon) break
        }
        
        return sum * x.pow(a) * exp(-x)
    }
    
    // ==================== 统计分析辅助 ====================
    
    /**
     * 计算置信区间（正态分布）
     */
    fun confidenceInterval(mean: Double, stdDev: Double, n: Int, confidence: Double = 0.95): Pair<Double, Double> {
        if (stdDev <= 0) throw IllegalArgumentException("stdDev must be positive")
        if (n <= 0) throw IllegalArgumentException("n must be positive")
        if (confidence <= 0 || confidence >= 1) throw IllegalArgumentException("confidence must be in (0, 1)")
        
        val alpha = 1.0 - confidence
        val z = normalQuantile(1.0 - alpha / 2.0)
        val margin = z * stdDev / sqrt(n.toDouble())
        
        return Pair(mean - margin, mean + margin)
    }
    
    /**
     * 计算 Z 分数
     */
    fun zScore(x: Double, mean: Double, stdDev: Double): Double {
        if (stdDev <= 0) throw IllegalArgumentException("stdDev must be positive")
        return (x - mean) / stdDev
    }
    
    /**
     * 计算 p 值（双尾检验）
     */
    fun pValueTwoTailed(z: Double): Double {
        return 2.0 * (1.0 - normalCdf(abs(z)))
    }
    
    /**
     * 设置随机种子
     */
    fun setSeed(seed: Long) {
        random.setSeed(seed)
    }
}

/**
 * 分布结果类
 */
data class DistributionResult(
    val pdf: Double,
    val cdf: Double,
    val mean: Double,
    val variance: Double,
    val stdDev: Double
)

/**
 * 主函数 - 模块信息
 */
fun main() {
    println("Kotlin Probability Utils Module v1.0.0 loaded")
    println("Author: AllToolkit")
    println("Supported distributions: Uniform, Normal, Exponential, Poisson, Binomial,")
    println("                          Beta, Gamma, Chi-Squared, t, F, Geometric, Negative Binomial")
}