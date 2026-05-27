# Kotlin Probability Utilities Module

**Comprehensive probability distribution library for Kotlin - Zero Dependencies**

## Overview

This module provides a complete suite of probability distribution functions using only Kotlin/Java standard library. It covers PDF/CDF calculations, quantile functions, and random number generation for common distributions.

## Supported Distributions

| Distribution | PDF/PMF | CDF | Quantile | Random |
|--------------|---------|-----|----------|--------|
| Uniform | ✓ | ✓ | ✓ | ✓ |
| Normal | ✓ | ✓ | ✓ | ✓ |
| Exponential | ✓ | ✓ | ✓ | ✓ |
| Poisson | ✓ | ✓ | - | ✓ |
| Binomial | ✓ | ✓ | - | ✓ |
| Beta | ✓ | ✓ | ✓ | ✓ |
| Gamma | ✓ | ✓ | ✓ | ✓ |
| Chi-Squared | ✓ | ✓ | - | ✓ |
| t | ✓ | ✓ | - | ✓ |
| F | ✓ | ✓ | - | ✓ |
| Geometric | ✓ | ✓ | - | ✓ |
| Negative Binomial | ✓ | - | - | ✓ |

## Installation

```kotlin
// Import the module
import probability_utils.ProbabilityUtils
```

## Quick Start

```kotlin
import probability_utils.ProbabilityUtils

// Normal distribution
val pdf = ProbabilityUtils.normalPdf(0.0)  // ≈ 0.3989
val cdf = ProbabilityUtils.normalCdf(1.96)  // ≈ 0.975
val q95 = ProbabilityUtils.normalQuantile(0.95)  // ≈ 1.645

// Generate random samples
val samples = ProbabilityUtils.normalRandoms(100, mean = 5.0, stdDev = 2.0)

// Exponential distribution
val expPdf = ProbabilityUtils.exponentialPdf(1.0, lambda = 2.0)
val expCdf = ProbabilityUtils.exponentialCdf(0.5, lambda = 1.0)

// Poisson distribution
val poisPmf = ProbabilityUtils.poissonPmf(5, lambda = 5.0)
val poisRandom = ProbabilityUtils.poissonRandom(lambda = 5.0)

// Binomial distribution
val binomPmf = ProbabilityUtils.binomialPmf(5, n = 10, p = 0.5)
val binomRandom = ProbabilityUtils.binomialRandom(n = 10, p = 0.5)
```

## API Reference

### Uniform Distribution

```kotlin
// PDF: 1/(b-a) for x ∈ [a, b]
fun uniformPdf(x: Double, a: Double = 0.0, b: Double = 1.0): Double

// CDF: (x-a)/(b-a) for x ∈ [a, b]
fun uniformCdf(x: Double, a: Double = 0.0, b: Double = 1.0): Double

// Quantile: a + p*(b-a)
fun uniformQuantile(p: Double, a: Double = 0.0, b: Double = 1.0): Double

// Random number
fun uniformRandom(a: Double = 0.0, b: Double = 1.0): Double
```

### Normal Distribution

```kotlin
// PDF: (1/(σ√(2π))) * exp(-(x-μ)^2/(2σ^2))
fun normalPdf(x: Double, mean: Double = 0.0, stdDev: Double = 1.0): Double

// CDF (Abramowitz-Stegun approximation)
fun normalCdf(x: Double, mean: Double = 0.0, stdDev: Double = 1.0): Double

// Quantile (Beasley-Springer-Moro algorithm)
fun normalQuantile(p: Double, mean: Double = 0.0, stdDev: Double = 1.0): Double

// Random (Box-Muller transform)
fun normalRandom(mean: Double = 0.0, stdDev: Double = 1.0): Double
fun normalRandoms(n: Int, mean: Double = 0.0, stdDev: Double = 1.0): List<Double>
```

### Exponential Distribution

```kotlin
// PDF: λ * exp(-λx)
fun exponentialPdf(x: Double, lambda: Double = 1.0): Double

// CDF: 1 - exp(-λx)
fun exponentialCdf(x: Double, lambda: Double = 1.0): Double

// Quantile: -ln(1-p)/λ
fun exponentialQuantile(p: Double, lambda: Double = 1.0): Double

// Random: -ln(U)/λ
fun exponentialRandom(lambda: Double = 1.0): Double
```

### Poisson Distribution

```kotlin
// PMF: (λ^k * exp(-λ)) / k!
fun poissonPmf(k: Int, lambda: Double): Double

// CDF: sum of PMF from 0 to k
fun poissonCdf(k: Int, lambda: Double): Double

// Random (Knuth algorithm)
fun poissonRandom(lambda: Double): Int
```

### Binomial Distribution

```kotlin
// PMF: C(n,k) * p^k * (1-p)^(n-k)
fun binomialPmf(k: Int, n: Int, p: Double): Double

// CDF: sum of PMF from 0 to k
fun binomialCdf(k: Int, n: Int, p: Double): Double

// Random: count successes in n trials
fun binomialRandom(n: Int, p: Double): Int
```

### Beta Distribution

```kotlin
// PDF: x^(α-1) * (1-x)^(β-1) / B(α,β)
fun betaPdf(x: Double, alpha: Double, beta: Double): Double

// CDF (incomplete beta function)
fun betaCdf(x: Double, alpha: Double, beta: Double): Double

// Random: ratio of gamma variates
fun betaRandom(alpha: Double, beta: Double): Double
```

### Gamma Distribution

```kotlin
// PDF: x^(α-1) * exp(-x/β) / (β^α * Γ(α))
fun gammaPdf(x: Double, alpha: Double, beta: Double = 1.0): Double

// CDF: lower incomplete gamma / gamma
fun gammaCdf(x: Double, alpha: Double, beta: Double = 1.0): Double

// Random (Marsaglia method)
fun gammaRandom(alpha: Double, beta: Double = 1.0): Double
```

### Chi-Squared Distribution

```kotlin
// PDF (derived from gamma)
fun chiSquaredPdf(x: Double, df: Int): Double

// CDF
fun chiSquaredCdf(x: Double, df: Int): Double

// Random: sum of squared normal variates
fun chiSquaredRandom(df: Int): Double
```

### t Distribution

```kotlin
// PDF: Γ((df+1)/2) / (√(dfπ) * Γ(df/2)) * (1 + x²/df)^(-(df+1)/2)
fun tPdf(x: Double, df: Int): Double

// CDF (incomplete beta based)
fun tCdf(x: Double, df: Int): Double

// Random: normal / √(chi-squared/df)
fun tRandom(df: Int): Double
```

### F Distribution

```kotlin
// PDF
fun fPdf(x: Double, df1: Int, df2: Int): Double

// CDF
fun fCdf(x: Double, df1: Int, df2: Int): Double

// Random: (chi1/df1) / (chi2/df2)
fun fRandom(df1: Int, df2: Int): Double
```

### Geometric Distribution

```kotlin
// PMF: (1-p)^(k-1) * p
fun geometricPmf(k: Int, p: Double): Double

// CDF: 1 - (1-p)^k
fun geometricCdf(k: Int, p: Double): Double

// Random: count trials until success
fun geometricRandom(p: Double): Int
```

### Negative Binomial Distribution

```kotlin
// PMF: C(k-1, r-1) * p^r * (1-p)^(k-r)
fun negativeBinomialPmf(k: Int, r: Int, p: Double): Double

// Random: trials until r successes
fun negativeBinomialRandom(r: Int, p: Double): Int
```

### Helper Functions

```kotlin
// Gamma function (Lanczos approximation)
fun gamma(x: Double): Double
fun logGamma(x: Double): Double

// Beta function
fun beta(alpha: Double, beta: Double): Double
fun logBeta(alpha: Double, beta: Double): Double

// Factorial and combinations
fun factorial(n: Int): Double
fun logFactorial(n: Int): Double
fun binomialCoefficient(n: Int, k: Int): Double

// Statistical functions
fun zScore(x: Double, mean: Double, stdDev: Double): Double
fun pValueTwoTailed(z: Double): Double
fun confidenceInterval(mean: Double, stdDev: Double, n: Int, confidence: Double): Pair<Double, Double>

// Random seed control
fun setSeed(seed: Long)
```

## Examples

### Normal Distribution Probabilities

```kotlin
// Probability of value between -1 and 1 (≈ 68.27%)
val prob68 = ProbabilityUtils.normalCdf(1.0) - ProbabilityUtils.normalCdf(-1.0)

// Probability of value between -2 and 2 (≈ 95.45%)
val prob95 = ProbabilityUtils.normalCdf(2.0) - ProbabilityUtils.normalCdf(-2.0)

// Z-score and p-value
val z = ProbabilityUtils.zScore(75.0, mean = 50.0, stdDev = 10.0)
val pValue = ProbabilityUtils.pValueTwoTailed(z)
```

### Confidence Intervals

```kotlin
// 95% confidence interval
val ci = ProbabilityUtils.confidenceInterval(
    mean = 100.0,
    stdDev = 15.0,
    n = 50,
    confidence = 0.95
)
println("CI: (${ci.first}, ${ci.second})")
```

### Sampling from Distributions

```kotlin
// Generate 1000 normal samples
ProbabilityUtils.setSeed(42L)
val normalSamples = ProbabilityUtils.normalRandoms(1000, 0.0, 1.0)

// Generate Poisson samples
val poissonSamples = (1..100).map { ProbabilityUtils.poissonRandom(5.0) }

// Generate Beta samples
val betaSamples = (1..100).map { ProbabilityUtils.betaRandom(2.0, 5.0) }
```

## Testing

```bash
# Run tests (requires Kotlin compiler)
kotlinc probability_utils_test.kt -include-runtime -d test.jar
java -jar test.jar
```

## Mathematical Notes

- **Normal CDF**: Uses Abramowitz-Stegun approximation (error < 7.5e-8)
- **Normal Quantile**: Uses Beasley-Springer-Moro algorithm
- **Gamma Function**: Uses Lanczos approximation with g=7
- **Gamma Random**: Uses Marsaglia's method for α ≥ 1
- **Beta Random**: Generated as ratio of gamma variates

## Dependencies

**Zero external dependencies** - uses only:
- Kotlin standard library
- Java standard library (Random, Math)

## Version

- **Version**: 1.0.0
- **Author**: AllToolkit
- **License**: MIT

## Related Modules

- `crypto_utils` - Cryptographic utilities
- `math_expression_evaluator` - Expression evaluation
- `fraction_utils` - Fraction operations