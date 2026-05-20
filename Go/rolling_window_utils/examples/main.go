// Example demonstrating the rolling_window_utils package
package main

import (
	"fmt"
	"rolling_window_utils"
)

func main() {
	fmt.Println("=== Rolling Window Examples ===")
	fmt.Println()

	// Basic rolling window
	basicExample()
	
	// Moving statistics
	movingStatsExample()
	
	// Integer rolling window
	intExample()
	
	// Exponential Moving Average
	emaExample()
	
	// Counter and Cumulative Sum
	counterExample()
}

func basicExample() {
	fmt.Println("--- Basic Rolling Window ---")
	
	// Create a window of size 5
	rw := rolling_window_utils.NewRollingWindow(5)
	
	// Add values
	values := []float64{10, 20, 30, 40, 50, 60, 70}
	for _, v := range values {
		rw.Add(v)
		fmt.Printf("Added %.0f -> Window: %v\n", v, rw.Values())
	}
	
	fmt.Printf("Sum: %.0f\n", rw.Sum())
	fmt.Printf("Average: %.2f\n", rw.Average())
	fmt.Println()
}

func movingStatsExample() {
	fmt.Println("--- Moving Statistics ---")
	
	// Simulate streaming data
	data := []float64{100, 102, 98, 105, 110, 108, 115, 120, 118, 125}
	
	// Create a window for 5-period moving average
	rw := rolling_window_utils.NewRollingWindow(5)
	
	fmt.Println("Stock Price | 5-Period MA | Min | Max | Range")
	fmt.Println("------------|-------------|-----|-----|------")
	
	for _, price := range data {
		rw.Add(price)
		avg := rw.Average()
		min, _ := rw.Min()
		max, _ := rw.Max()
		rng, _ := rw.Range()
		
		fmt.Printf("  %-9.0f| %-11.2f| %-4.0f| %-4.0f| %-5.0f\n", 
			price, avg, min, max, rng)
	}
	
	// Get comprehensive statistics
	stats, _ := rw.Stats()
	fmt.Printf("\nFinal Statistics:\n")
	fmt.Printf("  Count: %d, Sum: %.0f, Avg: %.2f\n", stats.Count, stats.Sum, stats.Average)
	fmt.Printf("  Min: %.0f, Max: %.0f, Range: %.0f\n", stats.Min, stats.Max, stats.Range)
	fmt.Printf("  StdDev: %.2f, Variance: %.2f\n", stats.StdDev, stats.Variance)
	fmt.Printf("  P25: %.2f, Median: %.2f, P75: %.2f\n", stats.P25, stats.Median, stats.P75)
	fmt.Println()
}

func intExample() {
	fmt.Println("--- Integer Rolling Window ---")
	
	// Create integer window for counting
	ri := rolling_window_utils.NewRollingInt(10)
	
	// Simulate request counts per second
	requests := []int{45, 52, 48, 61, 55, 58, 62, 70, 65, 68, 72, 75}
	
	fmt.Println("Requests | Window Count | Sum | Average")
	fmt.Println("---------|--------------|-----|--------")
	
	for _, r := range requests {
		ri.Add(r)
		fmt.Printf("  %-6d| %-12d| %-4d| %.2f\n", 
			r, ri.Count(), ri.Sum(), ri.Average())
	}
	fmt.Println()
}

func emaExample() {
	fmt.Println("--- Exponential Moving Average ---")
	
	// EMA is more weight-sensitive to recent data
	// Higher alpha = more responsive, lower alpha = more smoothing
	
	ema := rolling_window_utils.NewEMA(0.3)
	ema2 := rolling_window_utils.NewEMAFromPeriod(5) // alpha = 2/(5+1) = 0.333
	
	data := []float64{100, 105, 103, 108, 112, 110, 115, 120, 118, 125}
	
	fmt.Println("Value | EMA (α=0.3) | EMA (period=5)")
	fmt.Println("------|-------------|---------------")
	
	for _, v := range data {
		ema.Add(v)
		ema2.Add(v)
		fmt.Printf("%-5.0f| %-11.2f| %.2f\n", v, ema.Value(), ema2.Value())
	}
	fmt.Println()
}

func counterExample() {
	fmt.Println("--- Counter and Cumulative Sum ---")
	
	// Simple counter
	counter := rolling_window_utils.NewCounter()
	fmt.Println("Counter operations:")
	fmt.Printf("  Initial: %d\n", counter.Value())
	fmt.Printf("  After increment: %d\n", counter.Increment())
	fmt.Printf("  After increment: %d\n", counter.Increment())
	fmt.Printf("  After add(10): %d\n", counter.Add(10))
	fmt.Printf("  After decrement: %d\n", counter.Decrement())
	
	// Cumulative sum
	sum := rolling_window_utils.NewCumulativeSum()
	fmt.Println("\nCumulative Sum:")
	sum.Add(100)
	sum.Add(200)
	sum.Add(150)
	fmt.Printf("  Current sum: %.0f\n", sum.Sum())
	fmt.Printf("  Reset and get: %.0f\n", sum.Reset())
	fmt.Printf("  After reset: %.0f\n", sum.Sum())
}