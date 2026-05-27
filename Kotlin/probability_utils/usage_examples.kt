/**
 * AllToolkit - Kotlin Probability Utilities Usage Examples
 *
 * 展示概率分布工具模块的使用方法
 *
 * @author AllToolkit
 * @version 1.0.0
 */

package probability_utils

fun main() {
    println("========================================")
    println("Probability Utils - Usage Examples")
    println("========================================\n")
    
    // ==================== 均匀分布示例 ====================
    
    println("=== Example 1: Uniform Distribution ===\n")
    
    val uniformPdf = ProbabilityUtils.uniformPdf(0.5, 0.0, 1.0)
    println("Uniform PDF at x=0.5, a=0, b=1: $uniformPdf")
    
    val uniformCdf = ProbabilityUtils.uniformCdf(0.5, 0.0, 1.0)
    println("Uniform CDF at x=0.5: $uniformCdf")
    
    val uniformQ = ProbabilityUtils.uniformQuantile(0.75, 0.0, 10.0)
    println("Uniform quantile at p=0.75, a=0, b=10: $uniformQ")
    
    ProbabilityUtils.setSeed(1L)
    val uniformSamples = (1..5).map { ProbabilityUtils.uniformRandom(0.0, 100.0) }
    println("Random uniform samples (0-100): $uniformSamples\n")
    
    // ==================== 正态分布示例 ====================
    
    println("=== Example 2: Normal Distribution ===\n")
    
    val normalPdf = ProbabilityUtils.normalPdf(0.0)
    println("Standard Normal PDF at x=0: $normalPdf (≈ 0.3989)")
    
    val normalCdf = ProbabilityUtils.normalCdf(1.96)
    println("Standard Normal CDF at x=1.96: $normalCdf (≈ 0.975)")
    
    val normalQ95 = ProbabilityUtils.normalQuantile(0.95)
    println("95th percentile of standard normal: $normalQ95 (≈ 1.645)")
    
    val normalQ99 = ProbabilityUtils.normalQuantile(0.99)
    println("99th percentile of standard normal: $normalQ99 (≈ 2.33)")
    
    ProbabilityUtils.setSeed(42L)
    val normalSamples = ProbabilityUtils.normalRandoms(5, 0.0, 1.0)
    println("Random normal samples (μ=0, σ=1): $normalSamples\n")
    
    // ==================== 指数分布示例 ====================
    
    println("=== Example 3: Exponential Distribution ===\n")
    
    val expPdf = ProbabilityUtils.exponentialPdf(1.0, 2.0)
    println("Exponential PDF at x=1, λ=2: $expPdf")
    
    val expCdf = ProbabilityUtils.exponentialCdf(0.5, 1.0)
    println("Exponential CDF at x=0.5, λ=1: $expCdf")
    
    val expQ = ProbabilityUtils.exponentialQuantile(0.5, 2.0)
    println("Exponential median (λ=2): $expQ")
    
    ProbabilityUtils.setSeed(100L)
    val expSamples = (1..5).map { ProbabilityUtils.exponentialRandom(0.5) }
    println("Random exponential samples (λ=0.5): $expSamples\n")
    
    // ==================== 泊松分布示例 ====================
    
    println("=== Example 4: Poisson Distribution ===\n")
    
    val poissonPmf0 = ProbabilityUtils.poissonPmf(0, 5.0)
    println("Poisson PMF at k=0, λ=5: $poissonPmf0")
    
    val poissonPmf5 = ProbabilityUtils.poissonPmf(5, 5.0)
    println("Poisson PMF at k=5, λ=5: $poissonPmf5")
    
    val poissonCdf = ProbabilityUtils.poissonCdf(5, 5.0)
    println("Poisson CDF at k=5, λ=5: $poissonCdf")
    
    ProbabilityUtils.setSeed(200L)
    val poissonSamples = (1..10).map { ProbabilityUtils.poissonRandom(5.0) }
    println("Random Poisson samples (λ=5): $poissonSamples\n")
    
    // ==================== 二项分布示例 ====================
    
    println("=== Example 5: Binomial Distribution ===\n")
    
    val binomPmf5 = ProbabilityUtils.binomialPmf(5, 10, 0.5)
    println("Binomial PMF at k=5, n=10, p=0.5: $binomPmf5 (≈ 0.246)")
    
    val binomCdf = ProbabilityUtils.binomialCdf(5, 10, 0.5)
    println("Binomial CDF at k=5, n=10, p=0.5: $binomCdf")
    
    ProbabilityUtils.setSeed(300L)
    val binomSamples = (1..10).map { ProbabilityUtils.binomialRandom(10, 0.5) }
    println("Random binomial samples (n=10, p=0.5): $binomSamples\n")
    
    // ==================== Beta 分布示例 ====================
    
    println("=== Example 6: Beta Distribution ===\n")
    
    val betaPdf = ProbabilityUtils.betaPdf(0.5, 2.0, 5.0)
    println("Beta PDF at x=0.5, α=2, β=5: $betaPdf")
    
    ProbabilityUtils.setSeed(400L)
    val betaSamples = (1..5).map { ProbabilityUtils.betaRandom(2.0, 5.0) }
    println("Random Beta samples (α=2, β=5): $betaSamples")
    println("Expected mean: α/(α+β) = ${2.0/7.0}\n")
    
    // ==================== Gamma 分布示例 ====================
    
    println("=== Example 7: Gamma Distribution ===\n")
    
    val gammaPdf = ProbabilityUtils.gammaPdf(2.0, 3.0, 1.0)
    println("Gamma PDF at x=2, α=3, β=1: $gammaPdf")
    
    ProbabilityUtils.setSeed(500L)
    val gammaSamples = (1..5).map { ProbabilityUtils.gammaRandom(3.0, 1.0) }
    println("Random Gamma samples (α=3, β=1): $gammaSamples")
    println("Expected mean: α*β = 3.0\n")
    
    // ==================== 卡方分布示例 ====================
    
    println("=== Example 8: Chi-Squared Distribution ===\n")
    
    val chiPdf = ProbabilityUtils.chiSquaredPdf(5.0, 10)
    println("Chi-squared PDF at x=5, df=10: $chiPdf")
    
    val chiCdf = ProbabilityUtils.chiSquaredCdf(5.0, 10)
    println("Chi-squared CDF at x=5, df=10: $chiCdf")
    
    ProbabilityUtils.setSeed(600L)
    val chiSamples = (1..5).map { ProbabilityUtils.chiSquaredRandom(10) }
    println("Random Chi-squared samples (df=10): $chiSamples\n")
    
    // ==================== t 分布示例 ====================
    
    println("=== Example 9: t Distribution ===\n")
    
    val tPdf = ProbabilityUtils.tPdf(0.0, 10)
    println("t PDF at x=0, df=10: $tPdf")
    
    val tCdf = ProbabilityUtils.tCdf(0.0, 10)
    println("t CDF at x=0, df=10: $tCdf (should be 0.5)")
    
    ProbabilityUtils.setSeed(700L)
    val tSamples = (1..5).map { ProbabilityUtils.tRandom(10) }
    println("Random t samples (df=10): $tSamples\n")
    
    // ==================== F 分布示例 ====================
    
    println("=== Example 10: F Distribution ===\n")
    
    val fPdf = ProbabilityUtils.fPdf(1.0, 5, 10)
    println("F PDF at x=1, df1=5, df2=10: $fPdf")
    
    val fCdf = ProbabilityUtils.fCdf(1.0, 5, 10)
    println("F CDF at x=1, df1=5, df2=10: $fCdf")
    
    ProbabilityUtils.setSeed(800L)
    val fSamples = (1..5).map { ProbabilityUtils.fRandom(5, 10) }
    println("Random F samples (df1=5, df2=10): $fSamples\n")
    
    // ==================== 几何分布示例 ====================
    
    println("=== Example 11: Geometric Distribution ===\n")
    
    val geomPmf = ProbabilityUtils.geometricPmf(1, 0.5)
    println("Geometric PMF at k=1, p=0.5: $geomPmf")
    
    val geomCdf = ProbabilityUtils.geometricCdf(3, 0.5)
    println("Geometric CDF at k=3, p=0.5: $geomCdf")
    
    ProbabilityUtils.setSeed(900L)
    val geomSamples = (1..10).map { ProbabilityUtils.geometricRandom(0.3) }
    println("Random geometric samples (p=0.3): $geomSamples")
    println("Expected mean: 1/p = ${1.0/0.3}\n")
    
    // ==================== 统计分析示例 ====================
    
    println("=== Example 12: Statistical Analysis ===\n")
    
    // Z 分数
    val zScore = ProbabilityUtils.zScore(75.0, 50.0, 10.0)
    println("Z-score for x=75, mean=50, std=10: $zScore")
    
    // p 值
    val pValue = ProbabilityUtils.pValueTwoTailed(2.5)
    println("Two-tailed p-value for Z=2.5: $pValue")
    
    // 95% 置信区间
    val ci = ProbabilityUtils.confidenceInterval(100.0, 15.0, 50, 0.95)
    println("95% Confidence Interval: (${ci.first}, ${ci.second})")
    println("Margin of error: ${ci.second - 100.0}\n")
    
    // ==================== Gamma 函数示例 ====================
    
    println("=== Example 13: Gamma Function ===\n")
    
    println("Γ(1) = ${ProbabilityUtils.gamma(1.0)} (should be 1)")
    println("Γ(2) = ${ProbabilityUtils.gamma(2.0)} (should be 1)")
    println("Γ(5) = ${ProbabilityUtils.gamma(5.0)} (should be 24, i.e., 4!)")
    println("Γ(0.5) = ${ProbabilityUtils.gamma(0.5)} (should be √π ≈ 1.772)")
    
    println("\nB(2,3) = ${ProbabilityUtils.beta(2.0, 3.0)}")
    
    // ==================== 验证关系示例 ====================
    
    println("\n=== Example 14: Distribution Relationships ===\n")
    
    // 正态分布分位数和 CDF 的逆关系
    val p = 0.975
    val q = ProbabilityUtils.normalQuantile(p)
    val cdfBack = ProbabilityUtils.normalCdf(q)
    println("Normal: quantile($p) = $q, then CDF($q) = $cdfBack")
    
    // 指数分布关系
    val lambda = 2.0
    val x = 1.0
    val expCdfVal = ProbabilityUtils.exponentialCdf(x, lambda)
    val expQVal = ProbabilityUtils.exponentialQuantile(expCdfVal, lambda)
    println("Exponential: CDF($x, λ=$lambda) = $expCdfVal, quantile($expCdfVal) = $expQVal")
    
    // ==================== 概率计算示例 ====================
    
    println("\n=== Example 15: Probability Calculations ===\n")
    
    // 正态分布中值落在某个范围的概率
    val probBetween = ProbabilityUtils.normalCdf(1.0) - ProbabilityUtils.normalCdf(-1.0)
    println("Probability of normal value between -1 and 1: $probBetween (≈ 68.27%)")
    
    val probBetween2 = ProbabilityUtils.normalCdf(2.0) - ProbabilityUtils.normalCdf(-2.0)
    println("Probability of normal value between -2 and 2: $probBetween2 (≈ 95.45%)")
    
    val probBetween3 = ProbabilityUtils.normalCdf(3.0) - ProbabilityUtils.normalCdf(-3.0)
    println("Probability of normal value between -3 and 3: $probBetween3 (≈ 99.73%)")
    
    println("\n========================================")
    println("All examples completed successfully!")
    println("========================================")
}