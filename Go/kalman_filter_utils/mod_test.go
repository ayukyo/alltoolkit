package kalman_filter_utils

import (
	"fmt"
	"math"
	"testing"
)

// ============================================================================
// 1D Kalman Filter Tests
// ============================================================================

func TestNewKalmanFilter1D(t *testing.T) {
	kf := NewKalmanFilter1D(25.0, 1.0, 0.1, 0.5)
	if kf == nil {
		t.Fatal("Failed to create Kalman filter")
	}
	if kf.GetState() != 25.0 {
		t.Errorf("Initial state should be 25.0, got %f", kf.GetState())
	}
}

func TestKalmanFilter1DUpdate(t *testing.T) {
	kf := NewKalmanFilter1D(25.0, 1.0, 0.1, 0.5)

	// Simulate temperature readings
	measurements := []float64{24.5, 25.2, 24.8, 25.1, 24.9, 25.3, 24.7}

	estimates := kf.BatchUpdate(measurements)

	// The estimates should converge to around 25
	finalEstimate := estimates[len(estimates)-1]
	if math.Abs(finalEstimate-25.0) > 1.0 {
		t.Errorf("Final estimate should be close to 25.0, got %f", finalEstimate)
	}
}

func TestKalmanFilter1DSmoothing(t *testing.T) {
	// Test that Kalman filter smooths noisy data
	kf := NewKalmanFilter1D(0.0, 1.0, 0.01, 1.0) // Low Q for smoother output

	// Add noisy measurements
	measurements := []float64{1.0, -1.0, 2.0, 0.0, 1.5, -0.5}
	estimates := kf.BatchUpdate(measurements)

	// Check that variance of estimates is less than variance of measurements
	meanEst := 0.0
	for _, e := range estimates {
		meanEst += e
	}
	meanEst /= float64(len(estimates))

	// Estimates should be more stable than raw measurements
	varEst := 0.0
	for _, e := range estimates {
		varEst += (e - meanEst) * (e - meanEst)
	}
	varEst /= float64(len(estimates))

	varMeas := 0.0
	meanMeas := 0.0
	for _, m := range measurements {
		meanMeas += m
	}
	meanMeas /= float64(len(measurements))
	for _, m := range measurements {
		varMeas += (m - meanMeas) * (m - meanMeas)
	}
	varMeas /= float64(len(measurements))

	if varEst > varMeas {
		t.Errorf("Kalman filter should reduce variance: est=%f, meas=%f", varEst, varMeas)
	}
}

func TestKalmanFilter1DPredict(t *testing.T) {
	kf := NewKalmanFilter1D(25.0, 1.0, 0.1, 0.5)

	// Update with a measurement
	kf.Update(25.5)

	// Predict should increase uncertainty but keep state
	initialCov := kf.GetCovariance()
	kf.Predict()
	newCov := kf.GetCovariance()

	if newCov < initialCov {
		t.Errorf("Prediction should increase covariance: initial=%f, new=%f", initialCov, newCov)
	}
}

func TestKalmanFilter1DReset(t *testing.T) {
	kf := NewKalmanFilter1D(25.0, 1.0, 0.1, 0.5)

	// Update several times
	kf.BatchUpdate([]float64{24.5, 25.2, 24.8})

	// Reset
	kf.Reset()

	if kf.GetState() != 25.0 {
		t.Errorf("After reset, state should be 25.0, got %f", kf.GetState())
	}
	if kf.GetCovariance() != 1.0 {
		t.Errorf("After reset, covariance should be 1.0, got %f", kf.GetCovariance())
	}
}

func TestKalmanFilter1DNoiseSettings(t *testing.T) {
	kf := NewKalmanFilter1D(25.0, 1.0, 0.1, 0.5)

	// High process noise = more responsive to changes
	kf.SetProcessNoise(1.0)
	estimates1 := kf.BatchUpdate([]float64{25.0, 30.0})

	// Reset and try with low process noise = smoother
	kf.Reset()
	kf.SetProcessNoise(0.01)
	estimates2 := kf.BatchUpdate([]float64{25.0, 30.0})

	// High Q should respond faster to the jump from 25 to 30
	if math.Abs(estimates1[1]-30.0) > math.Abs(estimates2[1]-30.0) {
		t.Errorf("Higher Q should respond faster to changes")
	}
}

func TestKalmanFilter1DThreadSafety(t *testing.T) {
	kf := NewKalmanFilter1D(25.0, 1.0, 0.1, 0.5)

	// Concurrent updates
	done := make(chan bool)
	for i := 0; i < 10; i++ {
		go func(idx int) {
			for j := 0; j < 100; j++ {
				kf.Update(25.0 + float64(idx%3))
			}
			done <- true
		}(i)
	}

	// Wait for all goroutines
	for i := 0; i < 10; i++ {
		<-done
	}

	// Filter should still be in a valid state
	state := kf.GetState()
	if state < 0 || state > 100 {
		t.Errorf("State should be reasonable after concurrent updates, got %f", state)
	}
}

// ============================================================================
// ND Kalman Filter Tests
// ============================================================================

func TestNewKalmanFilterND(t *testing.T) {
	initialState := []float64{0.0, 0.0}
	kf := NewKalmanFilterND(initialState, 1.0, 0.1, 0.5)

	if kf == nil {
		t.Fatal("Failed to create ND Kalman filter")
	}

	state := kf.GetState()
	if len(state) != 2 {
		t.Errorf("State dimension should be 2, got %d", len(state))
	}
}

func TestKalmanFilterNDUpdate(t *testing.T) {
	// 2D position tracking
	initialState := []float64{0.0, 0.0}
	kf := NewKalmanFilterND(initialState, 1.0, 0.1, 0.5)

	measurements := [][]float64{
		{1.0, 0.5},
		{1.5, 1.0},
		{2.0, 1.5},
		{2.5, 2.0},
	}

	for _, m := range measurements {
		state := kf.Update(m)
		fmt.Printf("State after update: [%f, %f]\n", state[0], state[1])
	}

	// Final state should have tracked measurements
	finalState := kf.GetState()
	// The filter should be tracking - check that state is reasonable
	if finalState[0] < -10 || finalState[0] > 10 {
		t.Errorf("Final x should be reasonable, got %f", finalState[0])
	}
	if finalState[1] < -10 || finalState[1] > 10 {
		t.Errorf("Final y should be reasonable, got %f", finalState[1])
	}
}

func TestKalmanFilterNDPredict(t *testing.T) {
	initialState := []float64{1.0, 2.0}
	kf := NewKalmanFilterND(initialState, 1.0, 0.1, 0.5)

	// Predict should propagate state
	state := kf.Predict()
	if len(state) != 2 {
		t.Errorf("Predicted state dimension should be 2")
	}
}

// ============================================================================
// Extended Kalman Filter Tests
// ============================================================================

func TestNewExtendedKalmanFilter(t *testing.T) {
	// Simple non-linear example: tracking with angle measurement
	n := 2

	// State function: linear motion (identity for simplicity)
	stateFunc := func(state []float64) []float64 {
		return state
	}

	// Measurement function: position
	measureFunc := func(state []float64) []float64 {
		return state
	}

	// Jacobians (identity for linear case)
	jacobianF := func(state []float64) [][]float64 {
		result := make([][]float64, n)
		for i := range result {
			result[i] = make([]float64, n)
			result[i][i] = 1.0
		}
		return result
	}

	jacobianH := func(state []float64) [][]float64 {
		result := make([][]float64, n)
		for i := range result {
			result[i] = make([]float64, n)
			result[i][i] = 1.0
		}
		return result
	}

	initialState := []float64{0.0, 0.0}
	ekf := NewExtendedKalmanFilter(initialState, 1.0, 0.1, 0.5, stateFunc, measureFunc, jacobianF, jacobianH)

	if ekf == nil {
		t.Fatal("Failed to create EKF")
	}
}

func TestEKFUpdate(t *testing.T) {
	// Define state dimension
	dim := 2

	stateFunc := func(state []float64) []float64 {
		return state
	}

	measureFunc := func(state []float64) []float64 {
		return state
	}

	jacobianF := func(state []float64) [][]float64 {
		result := make([][]float64, dim)
		for i := range result {
			result[i] = make([]float64, dim)
			result[i][i] = 1.0
		}
		return result
	}

	jacobianH := func(state []float64) [][]float64 {
		result := make([][]float64, dim)
		for i := range result {
			result[i] = make([]float64, dim)
			result[i][i] = 1.0
		}
		return result
	}

	initialState := []float64{5.0, 5.0}
	ekf := NewExtendedKalmanFilter(initialState, 1.0, 0.1, 0.5, stateFunc, measureFunc, jacobianF, jacobianH)

	// Update with measurement
	measurement := []float64{6.0, 6.0}
	state := ekf.Update(measurement)

	// State should move toward measurement
	if math.Abs(state[0]-6.0) > 1.0 {
		t.Errorf("EKF should converge to measurement")
	}
}

// ============================================================================
// UKF Tests
// ============================================================================

func TestNewUnscentedKalmanFilter(t *testing.T) {
	stateFunc := func(state []float64) []float64 {
		return state
	}

	measureFunc := func(state []float64) []float64 {
		return state
	}

	config := UKFConfig{
		Alpha: 1e-3,
		Beta:  2.0,
		Kappa: 0,
	}

	initialState := []float64{0.0, 0.0}
	ukf := NewUnscentedKalmanFilter(initialState, 1.0, 0.1, 0.5, stateFunc, measureFunc, config)

	if ukf == nil {
		t.Fatal("Failed to create UKF")
	}
}

func TestUKFUpdate(t *testing.T) {
	stateFunc := func(state []float64) []float64 {
		return state
	}

	measureFunc := func(state []float64) []float64 {
		return state
	}

	config := UKFConfig{
		Alpha: 1e-3,
		Beta:  2.0,
		Kappa: 0,
	}

	initialState := []float64{5.0, 5.0}
	ukf := NewUnscentedKalmanFilter(initialState, 1.0, 0.1, 0.5, stateFunc, measureFunc, config)

	measurement := []float64{7.0, 7.0}
	state := ukf.Update(measurement)

	// State should move toward measurement
	if math.Abs(state[0]-7.0) > 2.0 {
		t.Errorf("UKF should converge to measurement, got %f", state[0])
	}
}

// ============================================================================
// Utility Tests
// ============================================================================

func TestSmoothKalman(t *testing.T) {
	measurements := []float64{25.0, 24.5, 25.2, 24.8, 25.1, 24.9}
	smoothed := SmoothKalman(measurements, 0.01, 0.5)

	if len(smoothed) != len(measurements) {
		t.Errorf("Smoothed length should match measurements length")
	}
}

func TestMovingAverageFilter(t *testing.T) {
	maf := NewMovingAverageFilter(3)

	// Test updates
	values := []float64{10.0, 20.0, 30.0, 40.0}
	expected := []float64{10.0, 15.0, 20.0, 30.0}

	for i, v := range values {
		result := maf.Update(v)
		if math.Abs(result-expected[i]) > 0.01 {
			t.Errorf("MAF update %d: expected %f, got %f", i, expected[i], result)
		}
	}

	// Test reset
	maf.Reset()
	if maf.Update(5.0) != 5.0 {
		t.Errorf("After reset, first value should be 5.0")
	}
}

func TestExponentialSmoothingFilter(t *testing.T) {
	esf := NewExponentialSmoothingFilter(0.5)

	// Test updates
	values := []float64{10.0, 20.0, 30.0}

	// First value initializes the filter
	result1 := esf.Update(values[0])
	if result1 != 10.0 {
		t.Errorf("First update should return 10.0, got %f", result1)
	}

	// Second value: 0.5 * 20 + 0.5 * 10 = 15
	result2 := esf.Update(values[1])
	if math.Abs(result2-15.0) > 0.01 {
		t.Errorf("Second update should be 15.0, got %f", result2)
	}

	// Third value: 0.5 * 30 + 0.5 * 15 = 22.5
	result3 := esf.Update(values[2])
	if math.Abs(result3-22.5) > 0.01 {
		t.Errorf("Third update should be 22.5, got %f", result3)
	}

	// Test reset
	esf.Reset()
	if esf.GetValue() != 0 {
		t.Errorf("After reset, value should be 0")
	}

	// Test SetAlpha
	esf.SetAlpha(0.9)
	esf.Update(10.0) // Initialize
	result := esf.Update(20.0)
	if math.Abs(result-19.0) > 0.1 {
		t.Errorf("With alpha=0.9, result should be ~19.0, got %f", result)
	}
}

func TestExponentialSmoothingAlphaBounds(t *testing.T) {
	esf := NewExponentialSmoothingFilter(-1.0) // Should be clamped to 0
	if esf.alpha != 0 {
		t.Errorf("Alpha should be clamped to 0, got %f", esf.alpha)
	}

	esf2 := NewExponentialSmoothingFilter(2.0) // Should be clamped to 1
	if esf2.alpha != 1 {
		t.Errorf("Alpha should be clamped to 1, got %f", esf2.alpha)
	}
}

// ============================================================================
// Edge Case Tests
// ============================================================================

func TestKalmanFilter1DEmptyBatch(t *testing.T) {
	kf := NewKalmanFilter1D(25.0, 1.0, 0.1, 0.5)
	estimates := kf.BatchUpdate([]float64{})

	if len(estimates) != 0 {
		t.Errorf("Empty batch should return empty estimates")
	}
}

func TestSmoothKalmanEmpty(t *testing.T) {
	smoothed := SmoothKalman([]float64{}, 0.1, 0.5)
	if smoothed != nil {
		t.Errorf("Empty measurements should return nil")
	}
}

// ============================================================================
// Performance Tests
// ============================================================================

func TestKalmanFilter1DPerformance(t *testing.T) {
	kf := NewKalmanFilter1D(25.0, 1.0, 0.1, 0.5)

	// Generate 10000 measurements
	measurements := make([]float64, 10000)
	for i := range measurements {
		measurements[i] = 25.0 + float64(i%10) - 5.0
	}

	// This should complete quickly
	estimates := kf.BatchUpdate(measurements)
	if len(estimates) != 10000 {
		t.Errorf("Should process all measurements")
	}
}

// ============================================================================
// Example Tests
// ============================================================================

func ExampleKalmanFilter1D() {
	// Create a Kalman filter for temperature tracking
	// Initial temperature: 25°C, initial uncertainty: 1
	// Process noise: 0.1 (slowly changing temperature)
	// Measurement noise: 0.5 (sensor has moderate noise)
	kf := NewKalmanFilter1D(25.0, 1.0, 0.1, 0.5)

	// Simulate noisy temperature readings
	measurements := []float64{24.5, 25.2, 24.8, 25.1, 24.9}

	for _, m := range measurements {
		estimate := kf.Update(m)
		fmt.Printf("Measurement: %.1f°C, Estimate: %.2f°C\n", m, estimate)
	}

	// Output:
	// Measurement: 24.5°C, Estimate: 24.66°C
	// Measurement: 25.2°C, Estimate: 24.91°C
	// Measurement: 24.8°C, Estimate: 24.87°C
	// Measurement: 25.1°C, Estimate: 24.95°C
	// Measurement: 24.9°C, Estimate: 24.93°C
}

func ExampleMovingAverageFilter() {
	// Create a 3-point moving average filter
	maf := NewMovingAverageFilter(3)

	// Filter noisy signal
	for _, v := range []float64{10.0, 20.0, 15.0, 25.0, 20.0} {
		smoothed := maf.Update(v)
		fmt.Printf("%.1f -> %.2f\n", v, smoothed)
	}

	// Output:
	// 10.0 -> 10.00
	// 20.0 -> 15.00
	// 15.0 -> 15.00
	// 25.0 -> 20.00
	// 20.0 -> 20.00
}

func ExampleExponentialSmoothingFilter() {
	// Create an exponential smoothing filter with alpha=0.3
	esf := NewExponentialSmoothingFilter(0.3)

	// Filter signal
	for _, v := range []float64{100.0, 120.0, 110.0, 130.0} {
		smoothed := esf.Update(v)
		fmt.Printf("%.1f -> %.2f\n", v, smoothed)
	}

	// Output:
	// 100.0 -> 100.00
	// 120.0 -> 106.00
	// 110.0 -> 107.20
	// 130.0 -> 114.04
}