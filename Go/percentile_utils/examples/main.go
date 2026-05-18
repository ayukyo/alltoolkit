// Example usage of percentile_utils package
package main

import (
	"fmt"
	"math"

	percentile_utils "github.com/ayukyo/alltoolkit/Go/percentile_utils"
)

func main() {
	fmt.Println("=== Percentile Utils Examples ===\n")

	// Sample data
	data := []float64{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	dataWithOutlier := []float64{1, 2, 3, 4, 5, 6, 7, 8, 9, 100}

	// 1. Basic percentile calculation
	fmt.Println("--- Basic Percentile ---")
	fmt.Printf("Data: %v\n", data)

	p50, err := percentile_utils.Percentile(data, 50, percentile_utils.Linear, false)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	}
	fmt.Printf("P50 (Median): %.2f\n", p50)

	p25, _ := percentile_utils.Percentile(data, 25, percentile_utils.Linear, false)
	fmt.Printf("P25: %.2f\n", p25)

	p75, _ := percentile_utils.Percentile(data, 75, percentile_utils.Linear, false)
	fmt.Printf("P75: %.2f\n", p75)

	// 2. Different interpolation methods
	fmt.Println("\n--- Interpolation Methods ---")
	methods := []percentile_utils.InterpolationMethod{
		percentile_utils.Linear,
		percentile_utils.Lower,
		percentile_utils.Higher,
		percentile_utils.Nearest,
		percentile_utils.Midpoint,
	}

	for _, method := range methods {
		result, _ := percentile_utils.Percentile(data, 30, method, false)
		fmt.Printf("P30 with %s method: %.2f\n", method.String(), result)
	}

	// 3. Quartiles
	fmt.Println("\n--- Quartiles ---")
	qs, err := percentile_utils.CalculateQuartiles(data, percentile_utils.Linear, false)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	}
	fmt.Printf("Q1: %.2f\n", qs.Q1)
	fmt.Printf("Q2 (Median): %.2f\n", qs.Q2)
	fmt.Printf("Q3: %.2f\n", qs.Q3)
	fmt.Printf("IQR: %.2f\n", qs.IQR)

	// 4. Percentile Rank
	fmt.Println("\n--- Percentile Rank ---")
	rank, _ := percentile_utils.PercentileRank(data, 5.5, false)
	fmt.Printf("Percentile rank of 5.5: %.1f%%\n", rank)

	rank2, _ := percentile_utils.PercentileRank(data, 3, false)
	fmt.Printf("Percentile rank of 3: %.1f%%\n", rank2)

	// 5. Boxplot Statistics
	fmt.Println("\n--- Boxplot Statistics ---")
	fmt.Printf("Data with outlier: %v\n", dataWithOutlier)
	stats, _ := percentile_utils.CalculateBoxplotStats(dataWithOutlier, percentile_utils.Linear, false, 1.5)
	fmt.Printf("Min: %.2f\n", stats.Min)
	fmt.Printf("Q1: %.2f\n", stats.Q1)
	fmt.Printf("Median: %.2f\n", stats.Median)
	fmt.Printf("Q3: %.2f\n", stats.Q3)
	fmt.Printf("Max: %.2f\n", stats.Max)
	fmt.Printf("IQR: %.2f\n", stats.IQR)
	fmt.Printf("Lower Whisker: %.2f\n", stats.LowerWhisker)
	fmt.Printf("Upper Whisker: %.2f\n", stats.UpperWhisker)
	fmt.Printf("Lower Bound: %.2f\n", stats.LowerBound)
	fmt.Printf("Upper Bound: %.2f\n", stats.UpperBound)
	fmt.Printf("Outliers: %v\n", stats.Outliers)

	// 6. Deciles
	fmt.Println("\n--- Deciles ---")
	deciles, _ := percentile_utils.CalculateDeciles(data, percentile_utils.Linear, false)
	fmt.Printf("Deciles: %v\n", formatDeciles(deciles))

	// 7. Multiple Percentiles
	fmt.Println("\n--- Multiple Percentiles ---")
	pList := []float64{5, 10, 25, 50, 75, 90, 95}
	ps, _ := percentile_utils.CalculatePercentiles(data, pList, percentile_utils.Linear, false)
	for p, val := range ps {
		fmt.Printf("P%.0f: %.2f\n", p, val)
	}

	// 8. Outlier Detection
	fmt.Println("\n--- Outlier Detection ---")
	isOutlier, _ := percentile_utils.IsOutlier(100, data, percentile_utils.Linear, 1.5)
	fmt.Printf("Is 100 an outlier in %v? %v\n", data, isOutlier)

	isOutlier2, _ := percentile_utils.IsOutlier(5, data, percentile_utils.Linear, 1.5)
	fmt.Printf("Is 5 an outlier in %v? %v\n", data, isOutlier2)

	// 9. Winsorization
	fmt.Println("\n--- Winsorization ---")
	winsorized, _ := percentile_utils.Winsorize(dataWithOutlier, 10, 90, percentile_utils.Linear)
	fmt.Printf("Original: %v\n", dataWithOutlier)
	fmt.Printf("Winsorized (P10-P90): %v\n", formatSlice(winsorized))

	// 10. Normalization
	fmt.Println("\n--- Normalization by Percentile ---")
	normalized, _ := percentile_utils.NormalizeByPercentile(data, 25, 75, percentile_utils.Linear)
	fmt.Printf("Original: %v\n", data)
	fmt.Printf("Normalized (IQR): %v\n", formatSlice(normalized))

	// 11. Summary Statistics
	fmt.Println("\n--- Summary Statistics ---")
	summary, _ := percentile_utils.CalculateSummary(data, percentile_utils.Linear)
	fmt.Printf("Count: %d\n", summary.Count)
	fmt.Printf("Min: %.2f\n", summary.Min)
	fmt.Printf("Max: %.2f\n", summary.Max)
	fmt.Printf("Sum: %.2f\n", summary.Sum)
	fmt.Printf("Mean: %.2f\n", summary.Mean)
	fmt.Printf("Variance: %.2f\n", summary.Variance)
	fmt.Printf("Std Dev: %.2f\n", summary.StdDev)
	fmt.Printf("Range: %.2f\n", summary.Range)
	fmt.Printf("Median: %.2f\n", summary.Median)

	// 12. Must functions (panic on error)
	fmt.Println("\n--- Must Functions ---")
	median := percentile_utils.MustMedian(data)
	fmt.Printf("MustMedian: %.2f\n", median)

	mustP50 := percentile_utils.MustPercentile(data, 50, percentile_utils.Linear)
	fmt.Printf("MustPercentile(P50): %.2f\n", mustP50)

	mustSummary := percentile_utils.MustSummary(data)
	fmt.Printf("MustSummary - Count: %d, Mean: %.2f\n", mustSummary.Count, mustSummary.Mean)

	// 13. Real-world example: Performance metrics
	fmt.Println("\n--- Real-world Example: API Response Times ---")
	responseTimes := []float64{45, 52, 38, 61, 55, 48, 72, 42, 59, 51, 63, 47, 39, 58, 44}

	rtSummary, _ := percentile_utils.CalculateSummary(responseTimes, percentile_utils.Linear)
	fmt.Printf("Response Times: %v\n", responseTimes)
	fmt.Printf("Mean: %.2f ms\n", rtSummary.Mean)
	fmt.Printf("Median: %.2f ms\n", rtSummary.Median)
	fmt.Printf("P95: %.2f ms (SLA threshold)\n", rtSummary.Percentiles[95])
	fmt.Printf("Std Dev: %.2f ms\n", rtSummary.StdDev)

	// Check if 100ms response time is an outlier
	isOutlierRT, _ := percentile_utils.IsOutlier(100, responseTimes, percentile_utils.Linear, 1.5)
	fmt.Printf("Is 100ms an outlier? %v\n", isOutlierRT)

	// 14. Basic statistics functions
	fmt.Println("\n--- Basic Statistics ---")
	fmt.Printf("Mean: %.2f\n", percentile_utils.Mean(data))
	fmt.Printf("Variance: %.2f\n", percentile_utils.Variance(data))
	fmt.Printf("Std Dev: %.2f\n", percentile_utils.StdDev(data))

	fmt.Println("\n=== All Examples Complete ===")
}

// Helper functions
func formatDeciles(d []float64) string {
	result := "["
	for i, v := range d {
		if i > 0 {
			result += ", "
		}
		result += fmt.Sprintf("D%d=%.1f", i, v)
	}
	result += "]"
	return result
}

func formatSlice(s []float64) string {
	result := "["
	for i, v := range s {
		if i > 0 {
			result += ", "
		}
		result += fmt.Sprintf("%.2f", round(v, 2))
	}
	result += "]"
	return result
}

// Round helper
func round(val float64, places int) float64 {
	mult := math.Pow(10, float64(places))
	return math.Round(val*mult) / mult
}