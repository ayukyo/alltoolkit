// Package macd_utils provides MACD (Moving Average Convergence Divergence) technical indicator utilities.
// MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a security's price.
package macd_utils

import (
	"errors"
	"math"
)

// MACDResult contains the result of MACD calculation
type MACDResult struct {
	MACDLine   []float64 // MACD line (fast EMA - slow EMA)
	SignalLine []float64 // Signal line (EMA of MACD line)
	Histogram  []float64 // Histogram (MACD line - signal line)
}

// MACDSignal represents a trading signal
type MACDSignal struct {
	Index      int     // Index in the data series
	Type       string  // "buy", "sell", "bullish_cross", "bearish_cross"
	Value      float64 // MACD value at signal
	Strength   float64 // Signal strength (0-1)
	Price      float64 // Price at signal
	Confidence string  // "strong", "moderate", "weak"
}

// Divergence represents a divergence between price and MACD
type Divergence struct {
	StartIndex int     // Start index of divergence
	EndIndex   int     // End index of divergence
	Type       string  // "bullish" (price lower lows, MACD higher lows) or "bearish" (price higher highs, MACD lower highs)
	Strength   float64 // Divergence strength (0-1)
}

// TrendAnalysis contains trend analysis results
type TrendAnalysis struct {
	Trend         string  // "bullish", "bearish", "neutral"
	Strength      float64 // Trend strength (0-1)
	Momentum      string  // "accelerating", "decelerating", "stable"
	MomentumValue float64 // Momentum value
	Duration      int     // Duration of current trend (in periods)
}

// DefaultMACDParams returns default MACD parameters (12, 26, 9)
func DefaultMACDParams() (fastPeriod, slowPeriod, signalPeriod int) {
	return 12, 26, 9
}

// CalculateEMA calculates Exponential Moving Average
func CalculateEMA(data []float64, period int) ([]float64, error) {
	if len(data) < period {
		return nil, errors.New("insufficient data for EMA calculation")
	}
	if period <= 0 {
		return nil, errors.New("period must be positive")
	}

	ema := make([]float64, len(data))
	multiplier := 2.0 / float64(period+1)

	// First EMA is SMA of first 'period' elements
	sum := 0.0
	for i := 0; i < period; i++ {
		sum += data[i]
	}
	ema[period-1] = sum / float64(period)

	// Calculate EMA for remaining elements
	for i := period; i < len(data); i++ {
		ema[i] = (data[i]-ema[i-1])*multiplier + ema[i-1]
	}

	// Set values before period to NaN (or could use partial calculation)
	for i := 0; i < period-1; i++ {
		ema[i] = math.NaN()
	}

	return ema, nil
}

// CalculateSMA calculates Simple Moving Average
func CalculateSMA(data []float64, period int) ([]float64, error) {
	if len(data) < period {
		return nil, errors.New("insufficient data for SMA calculation")
	}
	if period <= 0 {
		return nil, errors.New("period must be positive")
	}

	sma := make([]float64, len(data))
	for i := 0; i < period-1; i++ {
		sma[i] = math.NaN()
	}

	for i := period - 1; i < len(data); i++ {
		sum := 0.0
		for j := 0; j < period; j++ {
			sum += data[i-j]
		}
		sma[i] = sum / float64(period)
	}

	return sma, nil
}

// CalculateMACD calculates MACD, Signal line, and Histogram
func CalculateMACD(data []float64, fastPeriod, slowPeriod, signalPeriod int) (*MACDResult, error) {
	if len(data) == 0 {
		return nil, errors.New("empty data")
	}
	if fastPeriod <= 0 || slowPeriod <= 0 || signalPeriod <= 0 {
		return nil, errors.New("all periods must be positive")
	}
	if fastPeriod >= slowPeriod {
		return nil, errors.New("fast period must be less than slow period")
	}

	// Calculate EMAs
	fastEMA, err := CalculateEMA(data, fastPeriod)
	if err != nil {
		return nil, err
	}

	slowEMA, err := CalculateEMA(data, slowPeriod)
	if err != nil {
		return nil, err
	}

	// Calculate MACD line (fast EMA - slow EMA)
	macdLine := make([]float64, len(data))
	startIdx := slowPeriod - 1

	for i := 0; i < startIdx; i++ {
		macdLine[i] = math.NaN()
	}

	for i := startIdx; i < len(data); i++ {
		macdLine[i] = fastEMA[i] - slowEMA[i]
	}

	// Calculate Signal line (EMA of MACD line)
	signalLine := make([]float64, len(data))
	for i := 0; i < len(data); i++ {
		signalLine[i] = math.NaN()
	}

	// Need signalPeriod valid MACD values to calculate signal
	signalStartIdx := startIdx + signalPeriod - 1
	if signalStartIdx < len(data) {
		// Calculate EMA of MACD line (only for valid values)
		validMACD := make([]float64, 0)
		for i := startIdx; i < len(data); i++ {
			validMACD = append(validMACD, macdLine[i])
		}

		signalEMA, err := CalculateEMA(validMACD, signalPeriod)
		if err == nil {
			for i, v := range signalEMA {
				if !math.IsNaN(v) {
					signalLine[startIdx+i] = v
				}
			}
		}
	}

	// Calculate Histogram (MACD line - signal line)
	histogram := make([]float64, len(data))
	for i := 0; i < len(data); i++ {
		histogram[i] = math.NaN()
		if !math.IsNaN(macdLine[i]) && !math.IsNaN(signalLine[i]) {
			histogram[i] = macdLine[i] - signalLine[i]
		}
	}

	return &MACDResult{
		MACDLine:   macdLine,
		SignalLine: signalLine,
		Histogram:  histogram,
	}, nil
}

// CalculateMACDDefault calculates MACD with default parameters (12, 26, 9)
func CalculateMACDDefault(data []float64) (*MACDResult, error) {
	return CalculateMACD(data, 12, 26, 9)
}

// FindCrossovers finds MACD crossover points (buy/sell signals)
func FindCrossovers(macdResult *MACDResult) []MACDSignal {
	var signals []MACDSignal

	macdLine := macdResult.MACDLine
	signalLine := macdResult.SignalLine
	histogram := macdResult.Histogram

	for i := 1; i < len(macdLine); i++ {
		if math.IsNaN(macdLine[i]) || math.IsNaN(signalLine[i]) ||
			math.IsNaN(macdLine[i-1]) || math.IsNaN(signalLine[i-1]) {
			continue
		}

		// Bullish crossover: MACD crosses above signal line
		if macdLine[i-1] < signalLine[i-1] && macdLine[i] > signalLine[i] {
			strength := calculateSignalStrength(histogram, i, true)
			confidence := "moderate"
			if strength > 0.7 {
				confidence = "strong"
			} else if strength < 0.3 {
				confidence = "weak"
			}

			signals = append(signals, MACDSignal{
				Index:      i,
				Type:       "bullish_cross",
				Value:      macdLine[i],
				Strength:   strength,
				Confidence: confidence,
			})
		}

		// Bearish crossover: MACD crosses below signal line
		if macdLine[i-1] > signalLine[i-1] && macdLine[i] < signalLine[i] {
			strength := calculateSignalStrength(histogram, i, false)
			confidence := "moderate"
			if strength > 0.7 {
				confidence = "strong"
			} else if strength < 0.3 {
				confidence = "weak"
			}

			signals = append(signals, MACDSignal{
				Index:      i,
				Type:       "bearish_cross",
				Value:      macdLine[i],
				Strength:   strength,
				Confidence: confidence,
			})
		}
	}

	return signals
}

// FindZeroLineCrossovers finds MACD zero line crossovers
func FindZeroLineCrossovers(macdResult *MACDResult) []MACDSignal {
	var signals []MACDSignal

	macdLine := macdResult.MACDLine
	histogram := macdResult.Histogram

	for i := 1; i < len(macdLine); i++ {
		if math.IsNaN(macdLine[i]) || math.IsNaN(macdLine[i-1]) {
			continue
		}

		// Positive crossover: MACD crosses above zero (bullish)
		if macdLine[i-1] < 0 && macdLine[i] > 0 {
			strength := calculateSignalStrength(histogram, i, true)
			signals = append(signals, MACDSignal{
				Index:      i,
				Type:       "buy",
				Value:      macdLine[i],
				Strength:   strength,
				Confidence: getConfidence(strength),
			})
		}

		// Negative crossover: MACD crosses below zero (bearish)
		if macdLine[i-1] > 0 && macdLine[i] < 0 {
			strength := calculateSignalStrength(histogram, i, false)
			signals = append(signals, MACDSignal{
				Index:      i,
				Type:       "sell",
				Value:      macdLine[i],
				Strength:   strength,
				Confidence: getConfidence(strength),
			})
		}
	}

	return signals
}

// FindDivergences finds divergences between price and MACD
func FindDivergences(data []float64, macdResult *MACDResult, lookback int) []Divergence {
	var divergences []Divergence

	if len(data) < lookback || lookback < 5 {
		return divergences
	}

	macdLine := macdResult.MACDLine

	// Find local extremes in price and MACD
	priceHighs := findLocalHighs(data, lookback)
	priceLows := findLocalLows(data, lookback)
	macdHighs := findLocalHighs(macdLine, lookback)
	macdLows := findLocalLows(macdLine, lookback)

	// Check for bullish divergence (price makes lower lows, MACD makes higher lows)
	for i := 1; i < len(priceLows); i++ {
		for j := 1; j < len(macdLows); j++ {
			// If the lows are close enough in time
			if absInt(priceLows[i]-macdLows[j]) <= 2 {
				prevPriceIdx := priceLows[i-1]
				currPriceIdx := priceLows[i]
				prevMACDIdx := macdLows[j-1]
				currMACDIdx := macdLows[j]

				if currPriceIdx > 0 && prevPriceIdx > 0 && currMACDIdx > 0 && prevMACDIdx > 0 {
					if !math.IsNaN(data[currPriceIdx]) && !math.IsNaN(data[prevPriceIdx]) &&
						!math.IsNaN(macdLine[currMACDIdx]) && !math.IsNaN(macdLine[prevMACDIdx]) {
						// Price lower low, MACD higher low
						if data[currPriceIdx] < data[prevPriceIdx] && macdLine[currMACDIdx] > macdLine[prevMACDIdx] {
							strength := calculateDivergenceStrength(data, macdLine, prevPriceIdx, currPriceIdx)
							divergences = append(divergences, Divergence{
								StartIndex: min(prevPriceIdx, prevMACDIdx),
								EndIndex:   max(currPriceIdx, currMACDIdx),
								Type:       "bullish",
								Strength:   strength,
							})
						}
					}
				}
			}
		}
	}

	// Check for bearish divergence (price makes higher highs, MACD makes lower highs)
	for i := 1; i < len(priceHighs); i++ {
		for j := 1; j < len(macdHighs); j++ {
			if absInt(priceHighs[i]-macdHighs[j]) <= 2 {
				prevPriceIdx := priceHighs[i-1]
				currPriceIdx := priceHighs[i]
				prevMACDIdx := macdHighs[j-1]
				currMACDIdx := macdHighs[j]

				if currPriceIdx > 0 && prevPriceIdx > 0 && currMACDIdx > 0 && prevMACDIdx > 0 {
					if !math.IsNaN(data[currPriceIdx]) && !math.IsNaN(data[prevPriceIdx]) &&
						!math.IsNaN(macdLine[currMACDIdx]) && !math.IsNaN(macdLine[prevMACDIdx]) {
						// Price higher high, MACD lower high
						if data[currPriceIdx] > data[prevPriceIdx] && macdLine[currMACDIdx] < macdLine[prevMACDIdx] {
							strength := calculateDivergenceStrength(data, macdLine, prevPriceIdx, currPriceIdx)
							divergences = append(divergences, Divergence{
								StartIndex: min(prevPriceIdx, prevMACDIdx),
								EndIndex:   max(currPriceIdx, currMACDIdx),
								Type:       "bearish",
								Strength:   strength,
							})
						}
					}
				}
			}
		}
	}

	return divergences
}

// AnalyzeTrend analyzes the current trend based on MACD
func AnalyzeTrend(macdResult *MACDResult) *TrendAnalysis {
	macdLine := macdResult.MACDLine
	signalLine := macdResult.SignalLine
	histogram := macdResult.Histogram

	// Find the last valid index
	lastIdx := -1
	for i := len(macdLine) - 1; i >= 0; i-- {
		if !math.IsNaN(macdLine[i]) && !math.IsNaN(signalLine[i]) {
			lastIdx = i
			break
		}
	}

	if lastIdx < 5 {
		return &TrendAnalysis{
			Trend:     "neutral",
			Strength:  0,
			Momentum:  "stable",
			Duration:  0,
		}
	}

	// Determine trend
	var trend string
	var strength float64

	if macdLine[lastIdx] > signalLine[lastIdx] {
		trend = "bullish"
		strength = (macdLine[lastIdx] - signalLine[lastIdx]) / (abs(macdLine[lastIdx]) + abs(signalLine[lastIdx]) + 0.001)
		if strength > 1 {
			strength = 1
		}
	} else if macdLine[lastIdx] < signalLine[lastIdx] {
		trend = "bearish"
		strength = (signalLine[lastIdx] - macdLine[lastIdx]) / (abs(macdLine[lastIdx]) + abs(signalLine[lastIdx]) + 0.001)
		if strength > 1 {
			strength = 1
		}
	} else {
		trend = "neutral"
		strength = 0
	}

	// Determine momentum
	momentum := "stable"
	var momentumValue float64
	validHistograms := 0
	sumHistogram := 0.0

	for i := lastIdx - 3; i <= lastIdx; i++ {
		if i >= 0 && !math.IsNaN(histogram[i]) {
			sumHistogram += histogram[i]
			validHistograms++
		}
	}

	if validHistograms > 0 {
		momentumValue = sumHistogram / float64(validHistograms)
		if momentumValue > 0.01 {
			momentum = "accelerating"
		} else if momentumValue < -0.01 {
			momentum = "decelerating"
		}
	}

	// Calculate trend duration
	duration := 0
	if trend == "bullish" {
		for i := lastIdx; i >= 0; i-- {
			if math.IsNaN(macdLine[i]) || math.IsNaN(signalLine[i]) {
				break
			}
			if macdLine[i] > signalLine[i] {
				duration++
			} else {
				break
			}
		}
	} else if trend == "bearish" {
		for i := lastIdx; i >= 0; i-- {
			if math.IsNaN(macdLine[i]) || math.IsNaN(signalLine[i]) {
				break
			}
			if macdLine[i] < signalLine[i] {
				duration++
			} else {
				break
			}
		}
	}

	return &TrendAnalysis{
		Trend:         trend,
		Strength:      strength,
		Momentum:      momentum,
		MomentumValue: momentumValue,
		Duration:      duration,
	}
}

// IsOverbought checks if MACD indicates overbought conditions
func IsOverbought(macdResult *MACDResult, threshold float64) (bool, float64) {
	macdLine := macdResult.MACDLine

	// Find last valid value
	lastValid := -1.0
	for i := len(macdLine) - 1; i >= 0; i-- {
		if !math.IsNaN(macdLine[i]) {
			lastValid = macdLine[i]
			break
		}
	}

	if math.IsNaN(lastValid) {
		return false, 0
	}

	return lastValid > threshold, lastValid
}

// IsOversold checks if MACD indicates oversold conditions
func IsOversold(macdResult *MACDResult, threshold float64) (bool, float64) {
	macdLine := macdResult.MACDLine

	// Find last valid value
	lastValid := -1.0
	for i := len(macdLine) - 1; i >= 0; i-- {
		if !math.IsNaN(macdLine[i]) {
			lastValid = macdLine[i]
			break
		}
	}

	if math.IsNaN(lastValid) {
		return false, 0
	}

	return lastValid < threshold, lastValid
}

// CalculateHistogramStrength calculates the strength of histogram bars
func CalculateHistogramStrength(macdResult *MACDResult, periods int) float64 {
	histogram := macdResult.Histogram

	if len(histogram) < periods {
		periods = len(histogram)
	}

	sum := 0.0
	count := 0
	for i := len(histogram) - periods; i < len(histogram); i++ {
		if i >= 0 && !math.IsNaN(histogram[i]) {
			sum += abs(histogram[i])
			count++
		}
	}

	if count == 0 {
		return 0
	}

	return sum / float64(count)
}

// GetMACDState returns the current MACD state description
func GetMACDState(macdResult *MACDResult) string {
	macdLine := macdResult.MACDLine
	signalLine := macdResult.SignalLine
	histogram := macdResult.Histogram

	// Find last valid values
	var macdVal, histVal float64
	found := false

	for i := len(macdLine) - 1; i >= 0; i-- {
		if !math.IsNaN(macdLine[i]) && !math.IsNaN(signalLine[i]) && !math.IsNaN(histogram[i]) {
			macdVal = macdLine[i]
			histVal = histogram[i]
			found = true
			break
		}
	}

	if !found {
		return "insufficient_data"
	}

	// Determine state
	if macdVal > 0 && histVal > 0 {
		return "strong_bullish"
	} else if macdVal > 0 && histVal < 0 {
		return "weakening_bullish"
	} else if macdVal < 0 && histVal < 0 {
		return "strong_bearish"
	} else if macdVal < 0 && histVal > 0 {
		return "weakening_bearish"
	}

	return "neutral"
}

// CalculateMACDForPrice calculates MACD values for a single new price point
func CalculateMACDForPrice(prevFastEMA, prevSlowEMA, prevSignalEMA, newPrice float64, fastPeriod, slowPeriod, signalPeriod int) (newFastEMA, newSlowEMA, newMACD, newSignal, newHistogram float64) {
	fastMultiplier := 2.0 / float64(fastPeriod+1)
	slowMultiplier := 2.0 / float64(slowPeriod+1)
	signalMultiplier := 2.0 / float64(signalPeriod+1)

	newFastEMA = (newPrice-prevFastEMA)*fastMultiplier + prevFastEMA
	newSlowEMA = (newPrice-prevSlowEMA)*slowMultiplier + prevSlowEMA
	newMACD = newFastEMA - newSlowEMA
	newSignal = (newMACD-prevSignalEMA)*signalMultiplier + prevSignalEMA
	newHistogram = newMACD - newSignal

	return
}

// Helper functions

func abs(x float64) float64 {
	if x < 0 {
		return -x
	}
	return x
}

func absInt(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func calculateSignalStrength(histogram []float64, index int, isBullish bool) float64 {
	if index < 0 || index >= len(histogram) {
		return 0.5
	}

	// Look at recent histogram values
	lookback := min(5, index)
	sum := 0.0
	count := 0

	for i := index - lookback; i <= index; i++ {
		if i >= 0 && !math.IsNaN(histogram[i]) {
			sum += abs(histogram[i])
			count++
		}
	}

	if count == 0 {
		return 0.5
	}

	avgStrength := sum / float64(count)

	// Normalize to 0-1 range (adjust threshold as needed)
	strength := math.Min(avgStrength/0.5, 1.0)

	return strength
}

func getConfidence(strength float64) string {
	if strength > 0.7 {
		return "strong"
	} else if strength < 0.3 {
		return "weak"
	}
	return "moderate"
}

func findLocalHighs(data []float64, lookback int) []int {
	var highs []int

	for i := lookback; i < len(data)-lookback; i++ {
		if math.IsNaN(data[i]) {
			continue
		}

		isHigh := true
		for j := i - lookback; j <= i+lookback; j++ {
			if j != i && j >= 0 && j < len(data) && !math.IsNaN(data[j]) {
				if data[j] >= data[i] {
					isHigh = false
					break
				}
			}
		}

		if isHigh {
			highs = append(highs, i)
		}
	}

	return highs
}

func findLocalLows(data []float64, lookback int) []int {
	var lows []int

	for i := lookback; i < len(data)-lookback; i++ {
		if math.IsNaN(data[i]) {
			continue
		}

		isLow := true
		for j := i - lookback; j <= i+lookback; j++ {
			if j != i && j >= 0 && j < len(data) && !math.IsNaN(data[j]) {
				if data[j] <= data[i] {
					isLow = false
					break
				}
			}
		}

		if isLow {
			lows = append(lows, i)
		}
	}

	return lows
}

func calculateDivergenceStrength(data, macdLine []float64, startIdx, endIdx int) float64 {
	if startIdx < 0 || endIdx >= len(data) || startIdx >= endIdx {
		return 0.5
	}

	// Calculate price change percentage
	priceChange := 0.0
	if data[startIdx] != 0 {
		priceChange = abs(data[endIdx]-data[startIdx]) / abs(data[startIdx])
	}

	// Calculate MACD change percentage
	macdChange := 0.0
	if !math.IsNaN(macdLine[startIdx]) && !math.IsNaN(macdLine[endIdx]) && macdLine[startIdx] != 0 {
		macdChange = abs(macdLine[endIdx]-macdLine[startIdx]) / abs(macdLine[startIdx])
	}

	// Combined strength
	strength := (priceChange + macdChange) / 2
	if strength > 1 {
		strength = 1
	}

	return strength
}