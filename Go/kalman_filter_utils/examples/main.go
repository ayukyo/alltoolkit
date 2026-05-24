// Example usage of Kalman Filter Utilities
package main

import (
	"fmt"
	"math"
	"math/rand"
	"time"

	kalman_filter_utils "github.com/yourpackage/kalman_filter_utils"
)

func main() {
	fmt.Println("=== Kalman Filter Utilities Examples ===")
	fmt.Println()

	// Example 1: Temperature tracking
	example1TemperatureTracking()

	// Example 2: Position tracking
	example2PositionTracking()

	// Example 3: Noisy signal smoothing
	example3NoisySignalSmoothing()

	// Example 4: Moving average comparison
	example4MovingAverageComparison()

	// Example 5: Exponential smoothing
	example5ExponentialSmoothing()
}

// Example 1: Temperature tracking with 1D Kalman filter
func example1TemperatureTracking() {
	fmt.Println("--- Example 1: Temperature Tracking ---")

	// Create a Kalman filter for temperature tracking
	// Initial temperature: 25°C
	// Initial uncertainty: 1
	// Process noise: 0.1 (temperature changes slowly)
	// Measurement noise: 0.5 (sensor has moderate noise)
	kf := kalman_filter_utils.NewKalmanFilter1D(25.0, 1.0, 0.1, 0.5)

	// Simulate noisy temperature readings
	measurements := []float64{24.5, 25.2, 24.8, 25.1, 24.9, 25.3, 24.7, 25.0}

	fmt.Println("Processing temperature measurements:")
	for i, m := range measurements {
		estimate := kf.Update(m)
		covariance := kf.GetCovariance()
		fmt.Printf("  [%d] Measurement: %.1f°C, Estimate: %.2f°C, Uncertainty: %.4f\n",
			i+1, m, estimate, covariance)
	}

	fmt.Printf("Final estimate: %.2f°C\n", kf.GetState())
	fmt.Println()
}

// Example 2: 2D position tracking
func example2PositionTracking() {
	fmt.Println("--- Example 2: 2D Position Tracking ---")

	// Create a 2D Kalman filter for position tracking
	initialState := []float64{0.0, 0.0}
	kf := kalman_filter_utils.NewKalmanFilterND(initialState, 1.0, 0.1, 0.5)

	// Simulate position measurements (moving in a line)
	measurements := [][]float64{
		{1.0, 0.5},
		{1.5, 1.0},
		{2.0, 1.5},
		{2.5, 2.0},
		{3.0, 2.5},
		{3.5, 3.0},
	}

	fmt.Println("Tracking position:")
	for i, m := range measurements {
		state := kf.Update(m)
		fmt.Printf("  [%d] Measured: [%.1f, %.1f], Estimated: [%.2f, %.2f]\n",
			i+1, m[0], m[1], state[0], state[1])
	}

	fmt.Printf("Final position: [%.2f, %.2f]\n", kf.GetState()[0], kf.GetState()[1])
	fmt.Println()
}

// Example 3: Smoothing a noisy signal
func example3NoisySignalSmoothing() {
	fmt.Println("--- Example 3: Noisy Signal Smoothing ---")

	// Generate a noisy signal (true value = 50)
	rand.Seed(time.Now().UnixNano())

	kf := kalman_filter_utils.NewKalmanFilter1D(50.0, 10.0, 0.01, 5.0)

	trueValue := 50.0
	measurements := make([]float64, 20)
	estimates := make([]float64, 20)

	fmt.Println("Processing noisy measurements (true value = 50):")
	for i := 0; i < 20; i++ {
		// Add noise to true value
		noise := (rand.Float64() - 0.5) * 10.0
		measurements[i] = trueValue + noise

		// Update Kalman filter
		estimates[i] = kf.Update(measurements[i])

		if i < 5 || i >= 15 {
			fmt.Printf("  [%d] Measurement: %.2f, Estimate: %.2f (error: %.2f)\n",
				i+1, measurements[i], estimates[i], math.Abs(estimates[i]-trueValue))
		} else if i == 5 {
			fmt.Println("  ... (skipping middle values)")
		}
	}

	// Calculate error statistics
	meanMeasError := 0.0
	meanEstError := 0.0
	for i := range measurements {
		meanMeasError += math.Abs(measurements[i] - trueValue)
		meanEstError += math.Abs(estimates[i] - trueValue)
	}
	meanMeasError /= float64(len(measurements))
	meanEstError /= float64(len(estimates))

	fmt.Printf("\nAverage measurement error: %.2f\n", meanMeasError)
	fmt.Printf("Average estimate error: %.2f\n", meanEstError)
	fmt.Printf("Error reduction: %.1f%%\n", (1-meanEstError/meanMeasError)*100)
	fmt.Println()
}

// Example 4: Comparing Kalman filter with moving average
func example4MovingAverageComparison() {
	fmt.Println("--- Example 4: Kalman Filter vs Moving Average ---")

	// Generate noisy signal
	rand.Seed(42)
	trueValue := 100.0

	measurements := make([]float64, 50)
	for i := range measurements {
		noise := (rand.Float64() - 0.5) * 20.0
		measurements[i] = trueValue + noise
	}

	// Kalman filter
	kf := kalman_filter_utils.NewKalmanFilter1D(100.0, 5.0, 0.01, 10.0)
	kfEstimates := kf.BatchUpdate(measurements)

	// Moving average
	maf := kalman_filter_utils.NewMovingAverageFilter(5)
	mafEstimates := make([]float64, len(measurements))
	for i, m := range measurements {
		mafEstimates[i] = maf.Update(m)
	}

	// Calculate errors
	kfError := 0.0
	mafError := 0.0
	for i := range measurements {
		kfError += math.Abs(kfEstimates[i] - trueValue)
		mafError += math.Abs(mafEstimates[i] - trueValue)
	}
	kfError /= float64(len(measurements))
	mafError /= float64(len(measurements))

	fmt.Printf("Measurements range: %.2f - %.2f\n",
		minSlice(measurements), maxSlice(measurements))
	fmt.Printf("Kalman filter average error: %.2f\n", kfError)
	fmt.Printf("Moving average average error: %.2f\n", mafError)
	fmt.Printf("Kalman filter is %.1f%% better\n", (1-kfError/mafError)*100)
	fmt.Println()
}

// Example 5: Exponential smoothing
func example5ExponentialSmoothing() {
	fmt.Println("--- Example 5: Exponential Smoothing ---")

	// Test different smoothing factors
	data := []float64{10.0, 12.0, 15.0, 14.0, 16.0, 18.0, 17.0, 20.0}

	fmt.Println("Original data:", data)

	// Low alpha (smooth)
	esfLow := kalman_filter_utils.NewExponentialSmoothingFilter(0.2)
	smoothLow := make([]float64, len(data))
	for i, v := range data {
		smoothLow[i] = esfLow.Update(v)
	}
	fmt.Printf("Alpha=0.2 (smooth): %.2f\n", smoothLow)

	// High alpha (responsive)
	esfHigh := kalman_filter_utils.NewExponentialSmoothingFilter(0.8)
	smoothHigh := make([]float64, len(data))
	for i, v := range data {
		smoothHigh[i] = esfHigh.Update(v)
	}
	fmt.Printf("Alpha=0.8 (responsive): %.2f\n", smoothHigh)

	fmt.Println()
}

// Helper functions
func minSlice(s []float64) float64 {
	min := s[0]
	for _, v := range s {
		if v < min {
			min = v
		}
	}
	return min
}

func maxSlice(s []float64) float64 {
	max := s[0]
	for _, v := range s {
		if v > max {
			max = v
		}
	}
	return max
}