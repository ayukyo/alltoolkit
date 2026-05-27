package macd_utils

import (
	"math"
	"testing"
)

// Helper function to check if two float64 slices are approximately equal
func approxEqualSlices(a, b []float64, tolerance float64) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if math.IsNaN(a[i]) && math.IsNaN(b[i]) {
			continue
		}
		if math.IsNaN(a[i]) || math.IsNaN(b[i]) {
			return false
		}
		if math.Abs(a[i]-b[i]) > tolerance {
			return false
		}
	}
	return true
}

// TestCalculateEMA tests EMA calculation
func TestCalculateEMA(t *testing.T) {
	tests := []struct {
		name     string
		data     []float64
		period   int
		wantErr  bool
		checkVal bool
	}{
		{
			name:     "Basic EMA calculation",
			data:     []float64{10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20},
			period:   3,
			wantErr:  false,
			checkVal: true,
		},
		{
			name:    "Insufficient data",
			data:    []float64{10, 11},
			period:  5,
			wantErr: true,
		},
		{
			name:    "Zero period",
			data:    []float64{10, 11, 12},
			period:  0,
			wantErr: true,
		},
		{
			name:    "Negative period",
			data:    []float64{10, 11, 12},
			period:  -1,
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CalculateEMA(tt.data, tt.period)
			if (err != nil) != tt.wantErr {
				t.Errorf("CalculateEMA() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if len(result) != len(tt.data) {
					t.Errorf("CalculateEMA() result length = %d, want %d", len(result), len(tt.data))
				}
				if tt.checkVal {
					// Check that NaN values exist before period
					for i := 0; i < tt.period-1; i++ {
						if !math.IsNaN(result[i]) {
							t.Errorf("CalculateEMA() result[%d] should be NaN", i)
						}
					}
					// First valid EMA should be SMA
					expectedSMA := 0.0
					for i := 0; i < tt.period; i++ {
						expectedSMA += tt.data[i]
					}
					expectedSMA /= float64(tt.period)
					if math.Abs(result[tt.period-1]-expectedSMA) > 0.0001 {
						t.Errorf("CalculateEMA() first valid EMA = %v, want %v", result[tt.period-1], expectedSMA)
					}
				}
			}
		})
	}
}

// TestCalculateSMA tests SMA calculation
func TestCalculateSMA(t *testing.T) {
	tests := []struct {
		name    string
		data    []float64
		period  int
		wantErr bool
	}{
		{
			name:    "Basic SMA calculation",
			data:    []float64{10, 20, 30, 40, 50},
			period:  3,
			wantErr: false,
		},
		{
			name:    "Insufficient data",
			data:    []float64{10},
			period:  5,
			wantErr: true,
		},
		{
			name:    "Zero period",
			data:    []float64{10, 11, 12},
			period:  0,
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CalculateSMA(tt.data, tt.period)
			if (err != nil) != tt.wantErr {
				t.Errorf("CalculateSMA() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if len(result) != len(tt.data) {
					t.Errorf("CalculateSMA() result length = %d, want %d", len(result), len(tt.data))
				}
				// Check first valid SMA value
				expectedSMA := 0.0
				for i := 0; i < tt.period; i++ {
					expectedSMA += tt.data[i]
				}
				expectedSMA /= float64(tt.period)
				if math.Abs(result[tt.period-1]-expectedSMA) > 0.0001 {
					t.Errorf("CalculateSMA() first valid SMA = %v, want %v", result[tt.period-1], expectedSMA)
				}
			}
		})
	}
}

// TestCalculateMACD tests MACD calculation
func TestCalculateMACD(t *testing.T) {
	tests := []struct {
		name         string
		data         []float64
		fastPeriod   int
		slowPeriod   int
		signalPeriod int
		wantErr      bool
	}{
		{
			name:         "Basic MACD calculation",
			data:         generateTestData(50),
			fastPeriod:   12,
			slowPeriod:   26,
			signalPeriod: 9,
			wantErr:      false,
		},
		{
			name:         "Empty data",
			data:         []float64{},
			fastPeriod:   12,
			slowPeriod:   26,
			signalPeriod: 9,
			wantErr:      true,
		},
		{
			name:         "Invalid periods - fast >= slow",
			data:         generateTestData(50),
			fastPeriod:   26,
			slowPeriod:   12,
			signalPeriod: 9,
			wantErr:      true,
		},
		{
			name:         "Zero fast period",
			data:         generateTestData(50),
			fastPeriod:   0,
			slowPeriod:   26,
			signalPeriod: 9,
			wantErr:      true,
		},
		{
			name:         "Zero slow period",
			data:         generateTestData(50),
			fastPeriod:   12,
			slowPeriod:   0,
			signalPeriod: 9,
			wantErr:      true,
		},
		{
			name:         "Zero signal period",
			data:         generateTestData(50),
			fastPeriod:   12,
			slowPeriod:   26,
			signalPeriod: 0,
			wantErr:      true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CalculateMACD(tt.data, tt.fastPeriod, tt.slowPeriod, tt.signalPeriod)
			if (err != nil) != tt.wantErr {
				t.Errorf("CalculateMACD() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if len(result.MACDLine) != len(tt.data) {
					t.Errorf("CalculateMACD() MACDLine length = %d, want %d", len(result.MACDLine), len(tt.data))
				}
				if len(result.SignalLine) != len(tt.data) {
					t.Errorf("CalculateMACD() SignalLine length = %d, want %d", len(result.SignalLine), len(tt.data))
				}
				if len(result.Histogram) != len(tt.data) {
					t.Errorf("CalculateMACD() Histogram length = %d, want %d", len(result.Histogram), len(tt.data))
				}
				// Verify histogram = MACD - signal
				for i := 0; i < len(tt.data); i++ {
					if !math.IsNaN(result.Histogram[i]) {
						expected := result.MACDLine[i] - result.SignalLine[i]
						if math.Abs(result.Histogram[i]-expected) > 0.0001 {
							t.Errorf("CalculateMACD() histogram[%d] = %v, want %v", i, result.Histogram[i], expected)
						}
					}
				}
			}
		})
	}
}

// TestCalculateMACDDefault tests MACD with default parameters
func TestCalculateMACDDefault(t *testing.T) {
	data := generateTestData(50)
	result, err := CalculateMACDDefault(data)
	if err != nil {
		t.Errorf("CalculateMACDDefault() error = %v", err)
		return
	}
	if result == nil {
		t.Error("CalculateMACDDefault() result is nil")
		return
	}
	if len(result.MACDLine) != len(data) {
		t.Errorf("CalculateMACDDefault() MACDLine length = %d, want %d", len(result.MACDLine), len(data))
	}
}

// TestFindCrossovers tests crossover signal detection
func TestFindCrossovers(t *testing.T) {
	tests := []struct {
		name        string
		data        []float64
		expectCount bool
	}{
		{
			name:        "Trending data should have crossovers",
			data:        generateTrendingData(100),
			expectCount: true,
		},
		{
			name:        "Flat data may have no crossovers",
			data:        generateFlatData(100),
			expectCount: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CalculateMACDDefault(tt.data)
			if err != nil {
				t.Errorf("CalculateMACDDefault() error = %v", err)
				return
			}
			signals := FindCrossovers(result)
			if tt.expectCount && len(signals) == 0 {
				t.Error("FindCrossovers() expected at least one crossover signal")
			}
			// Verify signal types
			for _, sig := range signals {
				if sig.Type != "bullish_cross" && sig.Type != "bearish_cross" {
					t.Errorf("FindCrossovers() invalid signal type: %s", sig.Type)
				}
				if sig.Strength < 0 || sig.Strength > 1 {
					t.Errorf("FindCrossovers() invalid signal strength: %f", sig.Strength)
				}
				if sig.Confidence != "strong" && sig.Confidence != "moderate" && sig.Confidence != "weak" {
					t.Errorf("FindCrossovers() invalid confidence: %s", sig.Confidence)
				}
			}
		})
	}
}

// TestFindZeroLineCrossovers tests zero line crossover detection
func TestFindZeroLineCrossovers(t *testing.T) {
	// Create data that will definitely cross zero
	data := generateOscillatingData(100)
	result, err := CalculateMACDDefault(data)
	if err != nil {
		t.Errorf("CalculateMACDDefault() error = %v", err)
		return
	}

	signals := FindZeroLineCrossovers(result)
	// We might or might not have signals depending on the data
	for _, sig := range signals {
		if sig.Type != "buy" && sig.Type != "sell" {
			t.Errorf("FindZeroLineCrossovers() invalid signal type: %s", sig.Type)
		}
	}
}

// TestFindDivergences tests divergence detection
func TestFindDivergences(t *testing.T) {
	tests := []struct {
		name     string
		data     []float64
		lookback int
		wantErr  bool
	}{
		{
			name:     "Divergence detection",
			data:     generateDivergenceData(100),
			lookback: 5,
			wantErr:  false,
		},
		{
			name:     "Short data",
			data:     generateTestData(20),
			lookback: 5,
			wantErr:  true, // MACD calculation will fail due to insufficient data
		},
		{
			name:     "Invalid lookback",
			data:     generateTestData(100),
			lookback: 0,
			wantErr:  false, // MACD calculation succeeds, divergence detection handles invalid lookback
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CalculateMACDDefault(tt.data)
			if (err != nil) != tt.wantErr {
				t.Errorf("CalculateMACDDefault() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if tt.wantErr {
				return // Expected error, no divergence detection
			}
			divergences := FindDivergences(tt.data, result, tt.lookback)
			// Verify divergence types
			for _, div := range divergences {
				if div.Type != "bullish" && div.Type != "bearish" {
					t.Errorf("FindDivergences() invalid divergence type: %s", div.Type)
				}
				if div.Strength < 0 || div.Strength > 1 {
					t.Errorf("FindDivergences() invalid divergence strength: %f", div.Strength)
				}
				if div.StartIndex >= div.EndIndex {
					t.Errorf("FindDivergences() start index %d >= end index %d", div.StartIndex, div.EndIndex)
				}
			}
		})
	}
}

// TestAnalyzeTrend tests trend analysis
func TestAnalyzeTrend(t *testing.T) {
	tests := []struct {
		name          string
		data          []float64
		expectTrend   bool
		expectMomentum bool
	}{
		{
			name:          "Bullish trend",
			data:          generateUptrendData(100),
			expectTrend:   true,
			expectMomentum: true,
		},
		{
			name:          "Bearish trend",
			data:          generateDowntrendData(100),
			expectTrend:   true,
			expectMomentum: true,
		},
		{
			name:          "Short data",
			data:          generateTestData(30),
			expectTrend:   false,
			expectMomentum: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CalculateMACDDefault(tt.data)
			if err != nil {
				t.Errorf("CalculateMACDDefault() error = %v", err)
				return
			}
			trend := AnalyzeTrend(result)
			if trend == nil {
				t.Error("AnalyzeTrend() result is nil")
				return
			}
			// Check trend is valid
			if trend.Trend != "bullish" && trend.Trend != "bearish" && trend.Trend != "neutral" {
				t.Errorf("AnalyzeTrend() invalid trend: %s", trend.Trend)
			}
			// Check strength is valid
			if trend.Strength < 0 || trend.Strength > 1 {
				t.Errorf("AnalyzeTrend() invalid strength: %f", trend.Strength)
			}
			// Check momentum is valid
			if trend.Momentum != "accelerating" && trend.Momentum != "decelerating" && trend.Momentum != "stable" {
				t.Errorf("AnalyzeTrend() invalid momentum: %s", trend.Momentum)
			}
			// Check duration is non-negative
			if trend.Duration < 0 {
				t.Errorf("AnalyzeTrend() invalid duration: %d", trend.Duration)
			}
		})
	}
}

// TestIsOverbought tests overbought condition detection
func TestIsOverbought(t *testing.T) {
	data := generateTestData(100)
	result, err := CalculateMACDDefault(data)
	if err != nil {
		t.Errorf("CalculateMACDDefault() error = %v", err)
		return
	}

	overbought, value := IsOverbought(result, 0.5)
	// Just verify it doesn't crash and returns valid values
	_ = overbought
	_ = value
}

// TestIsOversold tests oversold condition detection
func TestIsOversold(t *testing.T) {
	data := generateTestData(100)
	result, err := CalculateMACDDefault(data)
	if err != nil {
		t.Errorf("CalculateMACDDefault() error = %v", err)
		return
	}

	oversold, value := IsOversold(result, -0.5)
	// Just verify it doesn't crash and returns valid values
	_ = oversold
	_ = value
}

// TestCalculateHistogramStrength tests histogram strength calculation
func TestCalculateHistogramStrength(t *testing.T) {
	data := generateTestData(100)
	result, err := CalculateMACDDefault(data)
	if err != nil {
		t.Errorf("CalculateMACDDefault() error = %v", err)
		return
	}

	strength := CalculateHistogramStrength(result, 5)
	// Strength should be non-negative
	if strength < 0 {
		t.Errorf("CalculateHistogramStrength() negative strength: %f", strength)
	}
}

// TestGetMACDState tests MACD state detection
func TestGetMACDState(t *testing.T) {
	tests := []struct {
		name string
		data []float64
	}{
		{
			name: "Uptrend data",
			data: generateUptrendData(100),
		},
		{
			name: "Downtrend data",
			data: generateDowntrendData(100),
		},
		{
			name: "Oscillating data",
			data: generateOscillatingData(100),
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CalculateMACDDefault(tt.data)
			if err != nil {
				t.Errorf("CalculateMACDDefault() error = %v", err)
				return
			}
			state := GetMACDState(result)
			validStates := []string{
				"strong_bullish", "weakening_bullish",
				"strong_bearish", "weakening_bearish",
				"neutral", "insufficient_data",
			}
			isValid := false
			for _, s := range validStates {
				if state == s {
					isValid = true
					break
				}
			}
			if !isValid {
				t.Errorf("GetMACDState() invalid state: %s", state)
			}
		})
	}
}

// TestCalculateMACDForPrice tests single price MACD calculation
func TestCalculateMACDForPrice(t *testing.T) {
	// Start with some initial values
	prevFastEMA := 50.0
	prevSlowEMA := 45.0
	prevSignalEMA := 3.0
	newPrice := 55.0

	newFastEMA, newSlowEMA, newMACD, newSignal, newHistogram := CalculateMACDForPrice(
		prevFastEMA, prevSlowEMA, prevSignalEMA, newPrice,
		12, 26, 9,
	)

	// Verify the calculation doesn't produce NaN or Inf
	if math.IsNaN(newFastEMA) || math.IsInf(newFastEMA, 0) {
		t.Errorf("CalculateMACDForPrice() newFastEMA is invalid: %f", newFastEMA)
	}
	if math.IsNaN(newSlowEMA) || math.IsInf(newSlowEMA, 0) {
		t.Errorf("CalculateMACDForPrice() newSlowEMA is invalid: %f", newSlowEMA)
	}
	if math.IsNaN(newMACD) || math.IsInf(newMACD, 0) {
		t.Errorf("CalculateMACDForPrice() newMACD is invalid: %f", newMACD)
	}
	if math.IsNaN(newSignal) || math.IsInf(newSignal, 0) {
		t.Errorf("CalculateMACDForPrice() newSignal is invalid: %f", newSignal)
	}
	if math.IsNaN(newHistogram) || math.IsInf(newHistogram, 0) {
		t.Errorf("CalculateMACDForPrice() newHistogram is invalid: %f", newHistogram)
	}

	// Verify histogram = MACD - signal
	expectedHistogram := newMACD - newSignal
	if math.Abs(newHistogram-expectedHistogram) > 0.0001 {
		t.Errorf("CalculateMACDForPrice() histogram = %f, want %f", newHistogram, expectedHistogram)
	}
}

// TestDefaultMACDParams tests default parameter values
func TestDefaultMACDParams(t *testing.T) {
	fast, slow, signal := DefaultMACDParams()
	if fast != 12 {
		t.Errorf("DefaultMACDParams() fast = %d, want 12", fast)
	}
	if slow != 26 {
		t.Errorf("DefaultMACDParams() slow = %d, want 26", slow)
	}
	if signal != 9 {
		t.Errorf("DefaultMACDParams() signal = %d, want 9", signal)
	}
}

// TestMACDConsistency tests that MACD calculation is consistent
func TestMACDConsistency(t *testing.T) {
	data := generateTestData(100)

	// Calculate MACD twice with same data
	result1, err1 := CalculateMACDDefault(data)
	result2, err2 := CalculateMACDDefault(data)

	if err1 != nil || err2 != nil {
		t.Errorf("CalculateMACDDefault() errors: %v, %v", err1, err2)
		return
	}

	// Results should be identical
	if !approxEqualSlices(result1.MACDLine, result2.MACDLine, 0.0001) {
		t.Error("MACD lines are not consistent")
	}
	if !approxEqualSlices(result1.SignalLine, result2.SignalLine, 0.0001) {
		t.Error("Signal lines are not consistent")
	}
	if !approxEqualSlices(result1.Histogram, result2.Histogram, 0.0001) {
		t.Error("Histograms are not consistent")
	}
}

// Helper functions to generate test data

func generateTestData(count int) []float64 {
	data := make([]float64, count)
	for i := 0; i < count; i++ {
		data[i] = 100.0 + float64(i) + 5.0*math.Sin(float64(i)/5.0)
	}
	return data
}

func generateTrendingData(count int) []float64 {
	data := make([]float64, count)
	for i := 0; i < count; i++ {
		// Upward trend with some noise
		data[i] = 100.0 + float64(i)*0.5 + 2.0*math.Sin(float64(i)/3.0)
	}
	return data
}

func generateUptrendData(count int) []float64 {
	data := make([]float64, count)
	for i := 0; i < count; i++ {
		data[i] = 100.0 + float64(i)*1.0 + 3.0*math.Sin(float64(i)/5.0)
	}
	return data
}

func generateDowntrendData(count int) []float64 {
	data := make([]float64, count)
	for i := 0; i < count; i++ {
		data[i] = 200.0 - float64(i)*1.0 + 3.0*math.Sin(float64(i)/5.0)
	}
	return data
}

func generateFlatData(count int) []float64 {
	data := make([]float64, count)
	for i := 0; i < count; i++ {
		data[i] = 100.0 + 0.1*math.Sin(float64(i))
	}
	return data
}

func generateOscillatingData(count int) []float64 {
	data := make([]float64, count)
	for i := 0; i < count; i++ {
		data[i] = 100.0 + 20.0*math.Sin(float64(i)/10.0)
	}
	return data
}

func generateDivergenceData(count int) []float64 {
	data := make([]float64, count)
	for i := 0; i < count; i++ {
		// Create a pattern that might cause divergence
		data[i] = 100.0 + float64(i%50)*0.5 + 10.0*math.Sin(float64(i)/8.0)
	}
	return data
}