package main

import (
	"fmt"
	"math"

	"statistics_utils"
)

func main() {
	fmt.Println("=== Statistics Utils Examples ===")
	fmt.Println()

	// Sample dataset
	data := []float64{23, 45, 67, 89, 12, 34, 56, 78, 90, 11, 22, 33, 44, 55, 66, 77, 88, 99}
	
	// === Basic Statistics ===
	fmt.Println("=== Basic Statistics ===")
	
	sum, _ := statistics_utils.Sum(data)
	fmt.Printf("Sum: %.2f\n", sum)
	
	mean, _ := statistics_utils.Mean(data)
	fmt.Printf("Mean: %.2f\n", mean)
	
	median, _ := statistics_utils.Median(data)
	fmt.Printf("Median: %.2f\n", median)
	
	mode, _ := statistics_utils.Mode(data)
	fmt.Printf("Mode: %.2f\n", mode)
	
	minVal, _ := statistics_utils.Min(data)
	maxVal, _ := statistics_utils.Max(data)
	fmt.Printf("Min: %.2f, Max: %.2f\n", minVal, maxVal)
	
	rangeVal, _ := statistics_utils.Range(data)
	fmt.Printf("Range: %.2f\n", rangeVal)
	fmt.Println()
	
	// === Variance and Standard Deviation ===
	fmt.Println("=== Variance and Standard Deviation ===")
	
	variance, _ := statistics_utils.Variance(data)
	fmt.Printf("Sample Variance: %.2f\n", variance)
	
	stdDev, _ := statistics_utils.StdDev(data)
	fmt.Printf("Sample Std Dev: %.2f\n", stdDev)
	
	popVariance, _ := statistics_utils.PopVariance(data)
	fmt.Printf("Population Variance: %.2f\n", popVariance)
	
	popStdDev, _ := statistics_utils.PopStdDev(data)
	fmt.Printf("Population Std Dev: %.2f\n", popStdDev)
	fmt.Println()
	
	// === Percentiles and Quartiles ===
	fmt.Println("=== Percentiles and Quartiles ===")
	
	p25, _ := statistics_utils.Percentile(data, 25)
	p50, _ := statistics_utils.Percentile(data, 50)
	p75, _ := statistics_utils.Percentile(data, 75)
	p95, _ := statistics_utils.Percentile(data, 95)
	fmt.Printf("25th percentile: %.2f\n", p25)
	fmt.Printf("50th percentile (median): %.2f\n", p50)
	fmt.Printf("75th percentile: %.2f\n", p75)
	fmt.Printf("95th percentile: %.2f\n", p95)
	
	q1, q2, q3, _ := statistics_utils.Quartiles(data)
	fmt.Printf("Q1: %.2f, Q2: %.2f, Q3: %.2f\n", q1, q2, q3)
	
	iqr, _ := statistics_utils.IQR(data)
	fmt.Printf("Interquartile Range (IQR): %.2f\n", iqr)
	fmt.Println()
	
	// === Different Types of Means ===
	fmt.Println("=== Different Types of Means ===")
	
	// For geometric and harmonic mean, all values must be positive
	positiveData := []float64{2, 4, 8, 16, 32}
	
	arithmeticMean, _ := statistics_utils.Mean(positiveData)
	geometricMean, _ := statistics_utils.GeometricMean(positiveData)
	harmonicMean, _ := statistics_utils.HarmonicMean(positiveData)
	
	fmt.Printf("Arithmetic Mean: %.2f\n", arithmeticMean)
	fmt.Printf("Geometric Mean: %.2f\n", geometricMean)
	fmt.Printf("Harmonic Mean: %.2f\n", harmonicMean)
	fmt.Println()
	
	// === Weighted Mean ===
	fmt.Println("=== Weighted Mean ===")
	
	values := []float64{80, 90, 70, 85, 95}
	weights := []float64{3, 4, 2, 3, 4} // e.g., credit weights
	weightedMean, _ := statistics_utils.WeightedMean(values, weights)
	fmt.Printf("Weighted Mean: %.2f\n", weightedMean)
	fmt.Println()
	
	// === Skewness and Kurtosis ===
	fmt.Println("=== Skewness and Kurtosis ===")
	
	skewness, _ := statistics_utils.Skewness(data)
	kurtosis, _ := statistics_utils.Kurtosis(data)
	
	fmt.Printf("Skewness: %.4f", skewness)
	if skewness < -0.5 {
		fmt.Println(" (left-skewed)")
	} else if skewness > 0.5 {
		fmt.Println(" (right-skewed)")
	} else {
		fmt.Println(" (approximately symmetric)")
	}
	
	fmt.Printf("Excess Kurtosis: %.4f", kurtosis)
	if kurtosis < -0.5 {
		fmt.Println(" (platykurtic - light tails)")
	} else if kurtosis > 0.5 {
		fmt.Println(" (leptokurtic - heavy tails)")
	} else {
		fmt.Println(" (mesokurtic - normal-like)")
	}
	fmt.Println()
	
	// === Coefficient of Variation ===
	fmt.Println("=== Coefficient of Variation ===")
	cv, _ := statistics_utils.CoeffVar(data)
	fmt.Printf("Coefficient of Variation: %.2f%%\n", cv)
	fmt.Println()
	
	// === Outlier Detection ===
	fmt.Println("=== Outlier Detection ===")
	
	dataWithOutlier := []float64{10, 12, 13, 14, 15, 16, 17, 18, 19, 100} // 100 is an outlier
	lowerOutliers, upperOutliers, _ := statistics_utils.Outliers(dataWithOutlier)
	
	fmt.Printf("Data: %v\n", dataWithOutlier)
	fmt.Printf("Lower outliers: %v\n", lowerOutliers)
	fmt.Printf("Upper outliers: %v\n", upperOutliers)
	fmt.Println()
	
	// === Z-Score Normalization ===
	fmt.Println("=== Z-Score Normalization ===")
	
	zScores, _ := statistics_utils.ZScores(data[:5]) // First 5 values
	fmt.Printf("Original: %v\n", data[:5])
	fmt.Printf("Z-scores: [")
	for i, z := range zScores {
		if i > 0 {
			fmt.Printf(", ")
		}
		fmt.Printf("%.2f", z)
	}
	fmt.Println("]")
	fmt.Println()
	
	// === Min-Max Normalization ===
	fmt.Println("=== Min-Max Normalization ===")
	
	normalized, _ := statistics_utils.Normalize(data[:5])
	fmt.Printf("Original: %v\n", data[:5])
	fmt.Printf("Normalized to [0, 1]: [")
	for i, n := range normalized {
		if i > 0 {
			fmt.Printf(", ")
		}
		fmt.Printf("%.2f", n)
	}
	fmt.Println("]")
	fmt.Println()
	
	// === Correlation ===
	fmt.Println("=== Correlation ===")
	
	x := []float64{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	y1 := []float64{2, 4, 6, 8, 10, 12, 14, 16, 18, 20} // Perfect positive correlation
	y2 := []float64{10, 9, 8, 7, 6, 5, 4, 3, 2, 1}     // Perfect negative correlation
	y3 := []float64{1, 3, 2, 4, 3, 5, 4, 6, 5, 7}      // Moderate positive correlation
	
	corr1, _ := statistics_utils.Correlation(x, y1)
	corr2, _ := statistics_utils.Correlation(x, y2)
	corr3, _ := statistics_utils.Correlation(x, y3)
	
	fmt.Printf("Perfect positive correlation: %.4f\n", corr1)
	fmt.Printf("Perfect negative correlation: %.4f\n", corr2)
	fmt.Printf("Moderate positive correlation: %.4f\n", corr3)
	fmt.Println()
	
	// === Moving Averages ===
	fmt.Println("=== Moving Averages ===")
	
	timeSeries := []float64{10, 12, 14, 16, 18, 20, 22, 24, 26, 28}
	
	sma, _ := statistics_utils.MovingAverage(timeSeries, 3)
	fmt.Printf("Original: %v\n", timeSeries)
	fmt.Printf("3-period SMA: [")
	for i, v := range sma {
		if i > 0 {
			fmt.Printf(", ")
		}
		fmt.Printf("%.1f", v)
	}
	fmt.Println("]")
	
	ema, _ := statistics_utils.ExponentialMovingAverage(timeSeries, 0.3)
	fmt.Printf("EMA (α=0.3): [")
	for i, v := range ema {
		if i > 0 {
			fmt.Printf(", ")
		}
		fmt.Printf("%.1f", v)
	}
	fmt.Println("]")
	fmt.Println()
	
	// === Median Absolute Deviation ===
	fmt.Println("=== Median Absolute Deviation ===")
	
	mad, _ := statistics_utils.MedianAbsoluteDeviation(data)
	fmt.Printf("MAD: %.2f\n", mad)
	fmt.Println("MAD is a robust measure of variability (less sensitive to outliers)")
	fmt.Println()
	
	// === Trimmed Mean ===
	fmt.Println("=== Trimmed Mean ===")
	
	trimmedData := []float64{1, 100, 100, 100, 100, 100, 100, 100, 100, 200}
	trimmedMean, _ := statistics_utils.TrimmedMean(trimmedData, 10)
	regularMean, _ := statistics_utils.Mean(trimmedData)
	
	fmt.Printf("Data with outliers: %v\n", trimmedData)
	fmt.Printf("Regular mean: %.2f\n", regularMean)
	fmt.Printf("10%% trimmed mean: %.2f\n", trimmedMean)
	fmt.Println("Trimmed mean is more robust against outliers")
	fmt.Println()
	
	// === Comprehensive Statistics ===
	fmt.Println("=== Comprehensive Statistics (Describe) ===")
	
	stats, err := statistics_utils.Describe(data)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	
	fmt.Printf("Count: %d\n", stats.Count)
	fmt.Printf("Sum: %.2f\n", stats.Sum)
	fmt.Printf("Mean: %.2f\n", stats.Mean)
	fmt.Printf("Median: %.2f\n", stats.Median)
	fmt.Printf("Mode: %.2f\n", stats.Mode)
	fmt.Printf("Min: %.2f\n", stats.Min)
	fmt.Printf("Max: %.2f\n", stats.Max)
	fmt.Printf("Range: %.2f\n", stats.Range)
	fmt.Printf("Sample Variance: %.2f\n", stats.Variance)
	fmt.Printf("Sample Std Dev: %.2f\n", stats.StdDev)
	fmt.Printf("Population Variance: %.2f\n", stats.PopVariance)
	fmt.Printf("Population Std Dev: %.2f\n", stats.PopStdDev)
	fmt.Printf("Skewness: %.4f\n", stats.Skewness)
	fmt.Printf("Excess Kurtosis: %.4f\n", stats.Kurtosis)
	fmt.Printf("Q1: %.2f\n", stats.Quartile1)
	fmt.Printf("Q3: %.2f\n", stats.Quartile3)
	fmt.Printf("IQR: %.2f\n", stats.IQR)
	fmt.Printf("Lower Fence: %.2f\n", stats.LowerFence)
	fmt.Printf("Upper Fence: %.2f\n", stats.UpperFence)
	fmt.Printf("Coefficient of Variation: %.2f%%\n", stats.CoeffVar)
	fmt.Println()
	
	// === Interpreting Statistics ===
	fmt.Println("=== Interpreting Statistics ===")
	
	// Coefficient of Variation interpretation
	if cv < 15 {
		fmt.Println("Low variability (CV < 15%): Data points are close to the mean")
	} else if cv < 30 {
		fmt.Println("Moderate variability (15% ≤ CV < 30%)")
	} else {
		fmt.Println("High variability (CV ≥ 30%): Data points are spread out")
	}
	
	// Skewness interpretation
	if math.Abs(skewness) < 0.5 {
		fmt.Println("Symmetric distribution (|skewness| < 0.5)")
	} else if skewness < 0 {
		fmt.Println("Left-skewed distribution (tail on the left)")
	} else {
		fmt.Println("Right-skewed distribution (tail on the right)")
	}
	
	// Kurtosis interpretation
	if math.Abs(kurtosis) < 0.5 {
		fmt.Println("Mesokurtic distribution (similar to normal)")
	} else if kurtosis > 0 {
		fmt.Println("Leptokurtic distribution (heavy tails, more outliers)")
	} else {
		fmt.Println("Platykurtic distribution (light tails, fewer outliers)")
	}
}