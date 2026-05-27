/**
 * AllToolkit - Kotlin Probability Utilities Test Suite
 *
 * 全面测试概率分布函数的正确性
 *
 * @author AllToolkit
 * @version 1.0.0
 */

package probability_utils

import kotlin.math.*

// ==================== 测试辅助函数 ====================

private val EPSILON = 1e-6
private val LOOSE_EPSILON = 1e-4
private var testsPassed = 0
private var testsFailed = 0

fun assertEquals(expected: Double, actual: Double, tolerance: Double = 0.0, name: String = "") {
    if (abs(expected - actual) > tolerance) {
        testsFailed++
        println("✗ FAIL: $name - Expected $expected but got $actual (tolerance: $tolerance)")
    } else {
        testsPassed++
        println("✓ PASS: $name")
    }
}

fun assertEquals(expected: Int, actual: Int, name: String = "") {
    if (expected != actual) {
        testsFailed++
        println("✗ FAIL: $name - Expected $expected but got $actual")
    } else {
        testsPassed++
        println("✓ PASS: $name")
    }
}

fun assertTrue(condition: Boolean, name: String = "") {
    if (!condition) {
        testsFailed++
        println("✗ FAIL: $name - Condition was false")
    } else {
        testsPassed++
        println("✓ PASS: $name")
    }
}

fun assertFailsWith(block: () -> Unit, name: String = "") {
    try {
        block()
        testsFailed++
        println("✗ FAIL: $name - Expected an exception but none was thrown")
    } catch (e: IllegalArgumentException) {
        testsPassed++
        println("✓ PASS: $name - Expected exception thrown")
    } catch (e: Exception) {
        testsFailed++
        println("✗ FAIL: $name - Expected IllegalArgumentException but got ${e::class}")
    }
}

// ==================== 均匀分布测试 ====================

fun testUniformPdf() {
    assertEquals(0.5, ProbabilityUtils.uniformPdf(0.5, 0.0, 2.0), EPSILON, "uniformPdf(0.5, 0, 2)")
    assertEquals(1.0, ProbabilityUtils.uniformPdf(0.0, 0.0, 1.0), EPSILON, "uniformPdf(0, 0, 1)")
    assertEquals(0.0, ProbabilityUtils.uniformPdf(-1.0, 0.0, 1.0), EPSILON, "uniformPdf(-1, 0, 1)")
    assertEquals(0.0, ProbabilityUtils.uniformPdf(2.0, 0.0, 1.0), EPSILON, "uniformPdf(2, 0, 1)")
}

fun testUniformCdf() {
    assertEquals(0.0, ProbabilityUtils.uniformCdf(-1.0, 0.0, 1.0), EPSILON, "uniformCdf(-1)")
    assertEquals(0.5, ProbabilityUtils.uniformCdf(0.5, 0.0, 1.0), EPSILON, "uniformCdf(0.5)")
    assertEquals(1.0, ProbabilityUtils.uniformCdf(2.0, 0.0, 1.0), EPSILON, "uniformCdf(2)")
    assertEquals(0.25, ProbabilityUtils.uniformCdf(0.5, 0.0, 2.0), EPSILON, "uniformCdf(0.5, 0, 2)")
}

fun testUniformQuantile() {
    assertEquals(0.0, ProbabilityUtils.uniformQuantile(0.0, 0.0, 1.0), EPSILON, "uniformQuantile(0)")
    assertEquals(0.5, ProbabilityUtils.uniformQuantile(0.5, 0.0, 1.0), EPSILON, "uniformQuantile(0.5)")
    assertEquals(1.0, ProbabilityUtils.uniformQuantile(1.0, 0.0, 1.0), EPSILON, "uniformQuantile(1)")
    assertEquals(2.0, ProbabilityUtils.uniformQuantile(0.5, 0.0, 4.0), EPSILON, "uniformQuantile(0.5, 0, 4)")
}

fun testUniformRandomRange() {
    ProbabilityUtils.setSeed(12345L)
    var allInRange = true
    for (i in 1..100) {
        val r = ProbabilityUtils.uniformRandom(0.0, 10.0)
        if (r < 0.0 || r > 10.0) allInRange = false
    }
    assertTrue(allInRange, "uniformRandom range check")
}

// ==================== 正态分布测试 ====================

fun testNormalPdf() {
    assertEquals(1.0 / sqrt(2.0 * PI), ProbabilityUtils.normalPdf(0.0), EPSILON, "normalPdf(0)")
    assertEquals(ProbabilityUtils.normalPdf(1.0), ProbabilityUtils.normalPdf(-1.0), EPSILON, "normalPdf symmetry")
    val pdf = ProbabilityUtils.normalPdf(0.0, 5.0, 2.0)
    assertTrue(pdf > 0 && pdf < 1, "normalPdf(0, 5, 2) range")
}

fun testNormalCdf() {
    assertEquals(0.5, ProbabilityUtils.normalCdf(0.0), LOOSE_EPSILON, "normalCdf(0) = 0.5")
    assertEquals(ProbabilityUtils.normalCdf(1.0), 1.0 - ProbabilityUtils.normalCdf(-1.0), LOOSE_EPSILON, "normalCdf symmetry")
    assertTrue(ProbabilityUtils.normalCdf(-10.0) < 0.001, "normalCdf(-10) small")
    assertTrue(ProbabilityUtils.normalCdf(10.0) > 0.999, "normalCdf(10) large")
}

fun testNormalQuantile() {
    assertEquals(0.0, ProbabilityUtils.normalQuantile(0.5), LOOSE_EPSILON, "normalQuantile(0.5) = 0")
    assertEquals(-ProbabilityUtils.normalQuantile(0.95), ProbabilityUtils.normalQuantile(0.05), LOOSE_EPSILON, "normalQuantile symmetry")
    
    val p = 0.8
    val q = ProbabilityUtils.normalQuantile(p)
    assertEquals(p, ProbabilityUtils.normalCdf(q), LOOSE_EPSILON, "normalQuantile inverse")
}

fun testNormalRandomDistribution() {
    ProbabilityUtils.setSeed(42L)
    val samples = ProbabilityUtils.normalRandoms(10000, 0.0, 1.0)
    
    val mean = samples.sum() / samples.size
    val variance = samples.map { (it - mean) * (it - mean) }.sum() / samples.size
    
    assertTrue(abs(mean) < 0.05, "normalRandom mean near 0")
    assertTrue(abs(variance - 1.0) < 0.1, "normalRandom variance near 1")
}

// ==================== 指数分布测试 ====================

fun testExponentialPdf() {
    assertEquals(1.0, ProbabilityUtils.exponentialPdf(0.0, 1.0), EPSILON, "expPdf(0, λ=1)")
    val expected = 2.0 * exp(-2.0 * 1.0)
    assertEquals(expected, ProbabilityUtils.exponentialPdf(1.0, 2.0), EPSILON, "expPdf(1, λ=2)")
    assertEquals(0.0, ProbabilityUtils.exponentialPdf(-1.0), EPSILON, "expPdf(-1) = 0")
}

fun testExponentialCdf() {
    assertEquals(0.0, ProbabilityUtils.exponentialCdf(-1.0), EPSILON, "expCdf(-1) = 0")
    val expected = 1.0 - exp(-1.0)
    assertEquals(expected, ProbabilityUtils.exponentialCdf(1.0, 1.0), EPSILON, "expCdf(1, λ=1)")
    assertTrue(ProbabilityUtils.exponentialCdf(10.0, 1.0) > 0.999, "expCdf(10) near 1")
}

fun testExponentialQuantile() {
    assertEquals(0.0, ProbabilityUtils.exponentialQuantile(0.0, 1.0), EPSILON, "expQuantile(0) = 0")
    val p = 0.5
    val q = ProbabilityUtils.exponentialQuantile(p, 1.0)
    assertEquals(p, ProbabilityUtils.exponentialCdf(q, 1.0), LOOSE_EPSILON, "expQuantile inverse")
}

fun testExponentialRandomMean() {
    ProbabilityUtils.setSeed(100L)
    val lambda = 2.0
    val samples = (1..1000).map { ProbabilityUtils.exponentialRandom(lambda) }
    
    val mean = samples.sum() / samples.size
    assertTrue(abs(mean - 1.0 / lambda) < 0.1, "expRandom mean = 1/λ")
}

// ==================== 泊松分布测试 ====================

fun testPoissonPmf() {
    assertEquals(exp(-1.0), ProbabilityUtils.poissonPmf(0, 1.0), EPSILON, "poisPmf(0, λ=1)")
    assertEquals(1.0 * exp(-1.0), ProbabilityUtils.poissonPmf(1, 1.0), EPSILON, "poisPmf(1, λ=1)")
    
    var sum = 0.0
    for (k in 0..50) {
        sum += ProbabilityUtils.poissonPmf(k, 5.0)
    }
    assertTrue(abs(sum - 1.0) < 0.001, "poisPmf sum = 1")
}

fun testPoissonCdf() {
    assertEquals(0.0, ProbabilityUtils.poissonCdf(-1, 5.0), EPSILON, "poisCdf(-1) = 0")
    assertTrue(ProbabilityUtils.poissonCdf(20, 5.0) > 0.99, "poisCdf(20, λ=5) near 1")
}

fun testPoissonRandomMean() {
    ProbabilityUtils.setSeed(200L)
    val lambda = 5.0
    val samples = (1..1000).map { ProbabilityUtils.poissonRandom(lambda) }
    
    val mean = samples.sum().toDouble() / samples.size
    assertTrue(abs(mean - lambda) < 0.5, "poisRandom mean = λ")
}

// ==================== 二项分布测试 ====================

fun testBinomialPmf() {
    val pmf5 = ProbabilityUtils.binomialPmf(5, 10, 0.5)
    assertTrue(abs(pmf5 - 0.246) < 0.01, "binomPmf(5, 10, 0.5)")
    
    var sum = 0.0
    for (k in 0..10) {
        sum += ProbabilityUtils.binomialPmf(k, 10, 0.5)
    }
    assertEquals(1.0, sum, EPSILON, "binomPmf sum = 1")
    
    assertEquals(0.0, ProbabilityUtils.binomialPmf(-1, 10, 0.5), EPSILON, "binomPmf(-1) = 0")
    assertEquals(0.0, ProbabilityUtils.binomialPmf(11, 10, 0.5), EPSILON, "binomPmf(11) = 0")
}

fun testBinomialCdf() {
    assertTrue(ProbabilityUtils.binomialCdf(0, 10, 0.5) > 0 && ProbabilityUtils.binomialCdf(0, 10, 0.5) < 0.01, "binomCdf(0)")
    assertEquals(1.0, ProbabilityUtils.binomialCdf(10, 10, 0.5), EPSILON, "binomCdf(10) = 1")
}

fun testBinomialRandomMean() {
    ProbabilityUtils.setSeed(300L)
    val n = 100
    val p = 0.3
    val samples = (1..1000).map { ProbabilityUtils.binomialRandom(n, p) }
    
    val mean = samples.sum().toDouble() / samples.size
    assertTrue(abs(mean - n * p) < 5, "binomRandom mean = np")
}

// ==================== Gamma 函数测试 ====================

fun testGamma() {
    assertEquals(1.0, ProbabilityUtils.gamma(1.0), EPSILON, "Γ(1) = 1")
    assertEquals(1.0, ProbabilityUtils.gamma(2.0), EPSILON, "Γ(2) = 1")
    assertEquals(6.0, ProbabilityUtils.gamma(4.0), EPSILON, "Γ(4) = 6")
    assertEquals(sqrt(PI), ProbabilityUtils.gamma(0.5), LOOSE_EPSILON, "Γ(0.5) = √π")
}

fun testBeta() {
    assertEquals(1.0, ProbabilityUtils.beta(1.0, 1.0), EPSILON, "B(1,1) = 1")
    
    val a = 2.0
    val b = 3.0
    val expected = ProbabilityUtils.gamma(a) * ProbabilityUtils.gamma(b) / ProbabilityUtils.gamma(a + b)
    assertEquals(expected, ProbabilityUtils.beta(a, b), EPSILON, "B(a,b) formula")
}

// ==================== Beta 分布测试 ====================

fun testBetaPdf() {
    assertEquals(1.0, ProbabilityUtils.betaPdf(0.5, 1.0, 1.0), EPSILON, "betaPdf(0.5, 1, 1)")
    assertEquals(0.0, ProbabilityUtils.betaPdf(-0.5, 1.0, 1.0), EPSILON, "betaPdf(-0.5) = 0")
    assertEquals(0.0, ProbabilityUtils.betaPdf(1.5, 1.0, 1.0), EPSILON, "betaPdf(1.5) = 0")
    assertTrue(ProbabilityUtils.betaPdf(0.2, 2.0, 5.0) > 0, "betaPdf positive")
}

fun testBetaRandom() {
    ProbabilityUtils.setSeed(400L)
    val alpha = 2.0
    val beta = 5.0
    
    val samples = (1..1000).map { ProbabilityUtils.betaRandom(alpha, beta) }
    
    assertTrue(samples.all { it >= 0.0 && it <= 1.0 }, "betaRandom in [0,1]")
    
    val expectedMean = alpha / (alpha + beta)
    val mean = samples.sum() / samples.size
    assertTrue(abs(mean - expectedMean) < 0.05, "betaRandom mean")
}

// ==================== Gamma 分布测试 ====================

fun testGammaPdf() {
    assertEquals(0.0, ProbabilityUtils.gammaPdf(-1.0, 1.0, 1.0), EPSILON, "gammaPdf(-1) = 0")
    assertEquals(1.0, ProbabilityUtils.gammaPdf(0.0, 1.0, 1.0), EPSILON, "gammaPdf(0, α=1) = exp PDF")
}

fun testGammaRandomMean() {
    ProbabilityUtils.setSeed(500L)
    val alpha = 3.0
    val beta = 2.0
    
    val samples = (1..1000).map { ProbabilityUtils.gammaRandom(alpha, beta) }
    
    val mean = samples.sum() / samples.size
    assertTrue(abs(mean - alpha * beta) < 0.5, "gammaRandom mean = αβ")
}

// ==================== 卡方分布测试 ====================

fun testChiSquaredPdf() {
    assertEquals(0.0, ProbabilityUtils.chiSquaredPdf(-1.0, 5), EPSILON, "chiPdf(-1) = 0")
    assertTrue(ProbabilityUtils.chiSquaredPdf(1.0, 2) > 0, "chiPdf(1, df=2)")
}

fun testChiSquaredRandomMean() {
    ProbabilityUtils.setSeed(600L)
    val df = 10
    
    val samples = (1..1000).map { ProbabilityUtils.chiSquaredRandom(df) }
    
    val mean = samples.sum() / samples.size
    assertTrue(abs(mean - df) < 1.0, "chiRandom mean = df")
}

// ==================== t 分布测试 ====================

fun testTPdf() {
    assertTrue(ProbabilityUtils.tPdf(0.0, 10) > 0, "tPdf(0) > 0")
    assertEquals(ProbabilityUtils.tPdf(1.0, 10), ProbabilityUtils.tPdf(-1.0, 10), EPSILON, "tPdf symmetry")
}

fun testTCdf() {
    assertEquals(0.5, ProbabilityUtils.tCdf(0.0, 10), LOOSE_EPSILON, "tCdf(0) = 0.5")
    assertEquals(ProbabilityUtils.tCdf(1.0, 10), 1.0 - ProbabilityUtils.tCdf(-1.0, 10), LOOSE_EPSILON, "tCdf symmetry")
}

// ==================== F 分布测试 ====================

fun testFPdf() {
    assertEquals(0.0, ProbabilityUtils.fPdf(-1.0, 5, 10), EPSILON, "fPdf(-1) = 0")
    assertTrue(ProbabilityUtils.fPdf(1.0, 5, 10) > 0, "fPdf(1) > 0")
}

fun testFCdf() {
    assertEquals(0.0, ProbabilityUtils.fCdf(-1.0, 5, 10), EPSILON, "fCdf(-1) = 0")
    val cdf = ProbabilityUtils.fCdf(1.0, 5, 10)
    assertTrue(cdf > 0 && cdf < 1, "fCdf(1) in (0,1)")
}

// ==================== 几何分布测试 ====================

fun testGeometricPmf() {
    assertEquals(0.5, ProbabilityUtils.geometricPmf(1, 0.5), EPSILON, "geomPmf(1, p=0.5) = p")
    assertEquals(0.25, ProbabilityUtils.geometricPmf(2, 0.5), EPSILON, "geomPmf(2, p=0.5)")
    
    var sum = 0.0
    for (k in 1..100) {
        sum += ProbabilityUtils.geometricPmf(k, 0.3)
    }
    assertTrue(abs(sum - 1.0) < 0.001, "geomPmf sum = 1")
}

fun testGeometricCdf() {
    assertEquals(0.0, ProbabilityUtils.geometricCdf(0, 0.5), EPSILON, "geomCdf(0) = 0")
    assertEquals(0.5, ProbabilityUtils.geometricCdf(1, 0.5), EPSILON, "geomCdf(1) = p")
    assertEquals(0.75, ProbabilityUtils.geometricCdf(2, 0.5), EPSILON, "geomCdf(2)")
}

fun testGeometricRandomMean() {
    ProbabilityUtils.setSeed(700L)
    val p = 0.3
    
    val samples = (1..1000).map { ProbabilityUtils.geometricRandom(p) }
    
    val mean = samples.sum().toDouble() / samples.size
    assertTrue(abs(mean - 1.0 / p) < 0.5, "geomRandom mean = 1/p")
}

// ==================== 负二项分布测试 ====================

fun testNegativeBinomialPmf() {
    val pmf = ProbabilityUtils.negativeBinomialPmf(5, 3, 0.5)
    assertTrue(pmf > 0 && pmf < 1, "negBinomPmf valid")
    assertEquals(0.0, ProbabilityUtils.negativeBinomialPmf(2, 5, 0.5), EPSILON, "negBinomPmf(k<r) = 0")
}

fun testNegativeBinomialRandom() {
    ProbabilityUtils.setSeed(800L)
    val r = 3
    val p = 0.5
    
    val samples = (1..1000).map { ProbabilityUtils.negativeBinomialRandom(r, p) }
    assertTrue(samples.all { it >= r }, "negBinomRandom >= r")
}

// ==================== 辅助函数测试 ====================

fun testFactorial() {
    assertEquals(1.0, ProbabilityUtils.factorial(0), EPSILON, "factorial(0) = 1")
    assertEquals(1.0, ProbabilityUtils.factorial(1), EPSILON, "factorial(1) = 1")
    assertEquals(2.0, ProbabilityUtils.factorial(2), EPSILON, "factorial(2) = 2")
    assertEquals(6.0, ProbabilityUtils.factorial(3), EPSILON, "factorial(3) = 6")
    assertEquals(24.0, ProbabilityUtils.factorial(4), EPSILON, "factorial(4) = 24")
    assertEquals(120.0, ProbabilityUtils.factorial(5), EPSILON, "factorial(5) = 120")
}

fun testBinomialCoefficient() {
    assertEquals(1.0, ProbabilityUtils.binomialCoefficient(5, 0), EPSILON, "C(5,0) = 1")
    assertEquals(5.0, ProbabilityUtils.binomialCoefficient(5, 1), EPSILON, "C(5,1) = 5")
    assertEquals(10.0, ProbabilityUtils.binomialCoefficient(5, 2), EPSILON, "C(5,2) = 10")
    assertEquals(10.0, ProbabilityUtils.binomialCoefficient(5, 3), EPSILON, "C(5,3) = 10")
    assertEquals(1.0, ProbabilityUtils.binomialCoefficient(5, 5), EPSILON, "C(5,5) = 1")
}

fun testZScore() {
    assertEquals(0.0, ProbabilityUtils.zScore(5.0, 5.0, 2.0), EPSILON, "zScore(x=mean) = 0")
    assertEquals(1.0, ProbabilityUtils.zScore(7.0, 5.0, 2.0), EPSILON, "zScore = 1")
    assertEquals(-1.0, ProbabilityUtils.zScore(3.0, 5.0, 2.0), EPSILON, "zScore = -1")
}

fun testPValueTwoTailed() {
    assertEquals(1.0, ProbabilityUtils.pValueTwoTailed(0.0), LOOSE_EPSILON, "pValue(Z=0) = 1")
    assertTrue(ProbabilityUtils.pValueTwoTailed(3.0) < 0.01, "pValue(Z=3) small")
}

fun testConfidenceInterval() {
    val ci = ProbabilityUtils.confidenceInterval(10.0, 2.0, 100, 0.95)
    assertTrue(ci.first < 10.0 && ci.second > 10.0, "CI contains mean")
    
    val width = ci.second - ci.first
    assertTrue(width > 0 && width < 1.0, "CI width reasonable")
}

// ==================== 错误处理测试 ====================

fun testInvalidParameters() {
    assertFailsWith({ ProbabilityUtils.uniformPdf(0.5, 1.0, 0.0) }, "uniform invalid params")
    assertFailsWith({ ProbabilityUtils.normalPdf(0.0, 0.0, -1.0) }, "normal negative std")
    assertFailsWith({ ProbabilityUtils.poissonPmf(1, -1.0) }, "poisson negative lambda")
    assertFailsWith({ ProbabilityUtils.betaPdf(0.5, -1.0, 1.0) }, "beta negative alpha")
    assertFailsWith({ ProbabilityUtils.normalQuantile(0.0) }, "quantile p=0")
    assertFailsWith({ ProbabilityUtils.normalQuantile(1.0) }, "quantile p=1")
}

// ==================== 运行所有测试 ====================

fun main() {
    println("\n========================================")
    println("Probability Utils Test Suite")
    println("========================================\n")
    
    println("=== Uniform Distribution ===")
    testUniformPdf()
    testUniformCdf()
    testUniformQuantile()
    testUniformRandomRange()
    
    println("\n=== Normal Distribution ===")
    testNormalPdf()
    testNormalCdf()
    testNormalQuantile()
    testNormalRandomDistribution()
    
    println("\n=== Exponential Distribution ===")
    testExponentialPdf()
    testExponentialCdf()
    testExponentialQuantile()
    testExponentialRandomMean()
    
    println("\n=== Poisson Distribution ===")
    testPoissonPmf()
    testPoissonCdf()
    testPoissonRandomMean()
    
    println("\n=== Binomial Distribution ===")
    testBinomialPmf()
    testBinomialCdf()
    testBinomialRandomMean()
    
    println("\n=== Gamma/Beta Functions ===")
    testGamma()
    testBeta()
    
    println("\n=== Beta Distribution ===")
    testBetaPdf()
    testBetaRandom()
    
    println("\n=== Gamma Distribution ===")
    testGammaPdf()
    testGammaRandomMean()
    
    println("\n=== Chi-Squared Distribution ===")
    testChiSquaredPdf()
    testChiSquaredRandomMean()
    
    println("\n=== t Distribution ===")
    testTPdf()
    testTCdf()
    
    println("\n=== F Distribution ===")
    testFPdf()
    testFCdf()
    
    println("\n=== Geometric Distribution ===")
    testGeometricPmf()
    testGeometricCdf()
    testGeometricRandomMean()
    
    println("\n=== Negative Binomial Distribution ===")
    testNegativeBinomialPmf()
    testNegativeBinomialRandom()
    
    println("\n=== Helper Functions ===")
    testFactorial()
    testBinomialCoefficient()
    testZScore()
    testPValueTwoTailed()
    testConfidenceInterval()
    
    println("\n=== Error Handling ===")
    testInvalidParameters()
    
    println("\n========================================")
    println("Test Summary")
    println("========================================")
    println("Passed: $testsPassed")
    println("Failed: $testsFailed")
    println("Total: ${testsPassed + testsFailed}")
    println("Success Rate: ${if (testsPassed + testsFailed > 0) (testsPassed * 100.0 / (testsPassed + testsFailed)) else 0}%")
    println("========================================\n")
    
    if (testsFailed > 0) {
        println("Some tests failed!")
        kotlin.system.exitProcess(1)
    } else {
        println("All tests passed!")
    }
}