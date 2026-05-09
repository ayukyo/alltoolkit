package temperature_utils

import (
	"math"
	"testing"
)

// Test basic conversions
func TestCelsiusToFahrenheit(t *testing.T) {
	tests := []struct {
		celsius    float64
		fahrenheit float64
	}{
		{0, 32},
		{100, 212},
		{-40, -40},
		{37, 98.6},
		{-273.15, -459.67},
	}

	for _, tt := range tests {
		result := CelsiusTo(tt.celsius, Fahrenheit)
		if math.Abs(result-tt.fahrenheit) > 0.01 {
			t.Errorf("CelsiusTo(%f, Fahrenheit) = %f, want %f", tt.celsius, result, tt.fahrenheit)
		}
	}
}

func TestCelsiusToKelvin(t *testing.T) {
	tests := []struct {
		celsius float64
		kelvin  float64
	}{
		{0, 273.15},
		{100, 373.15},
		{-273.15, 0},
		{-100, 173.15},
	}

	for _, tt := range tests {
		result := CelsiusTo(tt.celsius, Kelvin)
		if math.Abs(result-tt.kelvin) > 0.01 {
			t.Errorf("CelsiusTo(%f, Kelvin) = %f, want %f", tt.celsius, result, tt.kelvin)
		}
	}
}

func TestFahrenheitToCelsius(t *testing.T) {
	tests := []struct {
		fahrenheit float64
		celsius    float64
	}{
		{32, 0},
		{212, 100},
		{-40, -40},
		{98.6, 37},
	}

	for _, tt := range tests {
		result := FahrenheitTo(tt.fahrenheit, Celsius)
		if math.Abs(result-tt.celsius) > 0.01 {
			t.Errorf("FahrenheitTo(%f, Celsius) = %f, want %f", tt.fahrenheit, result, tt.celsius)
		}
	}
}

func TestKelvinToCelsius(t *testing.T) {
	tests := []struct {
		kelvin  float64
		celsius float64
	}{
		{0, -273.15},
		{273.15, 0},
		{373.15, 100},
	}

	for _, tt := range tests {
		result := KelvinTo(tt.kelvin, Celsius)
		if math.Abs(result-tt.celsius) > 0.01 {
			t.Errorf("KelvinTo(%f, Celsius) = %f, want %f", tt.kelvin, result, tt.celsius)
		}
	}
}

func TestRankineConversions(t *testing.T) {
	// Test Rankine to Fahrenheit and back
	rankine := RankineTo(491.67, Fahrenheit) // 491.67 R = 32 F
	if math.Abs(rankine-32) > 0.01 {
		t.Errorf("RankineTo(491.67, Fahrenheit) = %f, want 32", rankine)
	}

	// Test Rankine to Celsius
	rankineToC := RankineTo(491.67, Celsius) // 491.67 R = 0 C
	if math.Abs(rankineToC) > 0.01 {
		t.Errorf("RankineTo(491.67, Celsius) = %f, want 0", rankineToC)
	}
}

func TestDelisleConversions(t *testing.T) {
	// Delisle scale: boiling point of water is 0, freezing point is 150
	// 0 De = 100 C (boiling)
	// 150 De = 0 C (freezing)

	boiling := DelisleTo(0, Celsius)
	if math.Abs(boiling-100) > 0.01 {
		t.Errorf("DelisleTo(0, Celsius) = %f, want 100", boiling)
	}

	freezing := DelisleTo(150, Celsius)
	if math.Abs(freezing) > 0.01 {
		t.Errorf("DelisleTo(150, Celsius) = %f, want 0", freezing)
	}
}

func TestNewtonConversions(t *testing.T) {
	// Newton scale: 0 N = 0 C, 33 N = 100 C
	boiling := NewtonTo(33, Celsius)
	if math.Abs(boiling-100) > 0.01 {
		t.Errorf("NewtonTo(33, Celsius) = %f, want 100", boiling)
	}

	freezing := NewtonTo(0, Celsius)
	if math.Abs(freezing) > 0.01 {
		t.Errorf("NewtonTo(0, Celsius) = %f, want 0", freezing)
	}
}

func TestReaumurConversions(t *testing.T) {
	// Réaumur scale: 0 Ré = 0 C, 80 Ré = 100 C
	boiling := ReaumurTo(80, Celsius)
	if math.Abs(boiling-100) > 0.01 {
		t.Errorf("ReaumurTo(80, Celsius) = %f, want 100", boiling)
	}

	freezing := ReaumurTo(0, Celsius)
	if math.Abs(freezing) > 0.01 {
		t.Errorf("ReaumurTo(0, Celsius) = %f, want 0", freezing)
	}
}

func TestRomerConversions(t *testing.T) {
	// Rømer scale: 7.5 Rø = 0 C, 60 Rø = 100 C
	freezing := RomerTo(7.5, Celsius)
	if math.Abs(freezing) > 0.01 {
		t.Errorf("RomerTo(7.5, Celsius) = %f, want 0", freezing)
	}

	boiling := RomerTo(60, Celsius)
	if math.Abs(boiling-100) > 0.01 {
		t.Errorf("RomerTo(60, Celsius) = %f, want 100", boiling)
	}
}

// Test Temperature type
func TestNewTemperature(t *testing.T) {
	temp := NewTemperature(25, Celsius)
	if temp.Value != 25 || temp.Unit != Celsius {
		t.Errorf("NewTemperature(25, Celsius) = %v, want {25, Celsius}", temp)
	}
}

func TestTemperatureConvertTo(t *testing.T) {
	temp := NewTemperature(0, Celsius)
	fahrenheit := temp.ConvertTo(Fahrenheit)

	if math.Abs(fahrenheit.Value-32) > 0.01 {
		t.Errorf("0°C in Fahrenheit = %f, want 32", fahrenheit.Value)
	}
}

func TestTemperatureString(t *testing.T) {
	temp := NewTemperature(25.5, Celsius)
	str := temp.String()
	expected := "25.50° Celsius"
	if str != expected {
		t.Errorf("Temperature.String() = %s, want %s", str, expected)
	}
}

func TestTemperatureIsAboveAbsoluteZero(t *testing.T) {
	atAbsoluteZero := NewTemperature(0, Kelvin)
	above := NewTemperature(1, Kelvin)
	below := NewTemperature(-1, Kelvin)

	// 0 K is at absolute zero, not above it
	if atAbsoluteZero.IsAboveAbsoluteZero() {
		t.Error("0 K should not be above absolute zero")
	}

	// Above absolute zero
	if !above.IsAboveAbsoluteZero() {
		t.Error("1 K should be above absolute zero")
	}

	// Below absolute zero (physically invalid)
	if below.IsAboveAbsoluteZero() {
		t.Error("-1 K should be below absolute zero")
	}
}

func TestTemperatureIsValid(t *testing.T) {
	valid := NewTemperature(273.15, Kelvin)  // 0°C
	invalid := NewTemperature(-1, Kelvin)      // Below absolute zero

	if !valid.IsValid() {
		t.Error("273.15 K should be valid")
	}

	if invalid.IsValid() {
		t.Error("-1 K should be invalid")
	}
}

func TestTemperatureEquals(t *testing.T) {
	t1 := NewTemperature(0, Celsius)
	t2 := NewTemperature(32, Fahrenheit)

	if !t1.Equals(t2, 0.01) {
		t.Errorf("%s should equal %s", t1, t2)
	}
}

func TestTemperatureComparisons(t *testing.T) {
	t1 := NewTemperature(0, Celsius)
	t2 := NewTemperature(100, Celsius)

	if !t1.LessThan(t2) {
		t.Errorf("%s should be less than %s", t1, t2)
	}

	if !t2.GreaterThan(t1) {
		t.Errorf("%s should be greater than %s", t2, t1)
	}
}

// Test Range
func TestNewRange(t *testing.T) {
	r := NewRange(0, 100, Celsius)

	if r.Min.Value != 0 || r.Max.Value != 100 {
		t.Errorf("NewRange(0, 100, Celsius) = %v", r)
	}
}

func TestRangeContains(t *testing.T) {
	r := NewRange(0, 100, Celsius)

	within := NewTemperature(50, Celsius)
	outside := NewTemperature(150, Celsius)

	if !r.Contains(within) {
		t.Errorf("%s should be within %s", within, r)
	}

	if r.Contains(outside) {
		t.Errorf("%s should not be within %s", outside, r)
	}
}

func TestRangeContainsDifferentUnit(t *testing.T) {
	r := NewRange(32, 212, Fahrenheit) // 0°C to 100°C

	temp := NewTemperature(50, Celsius) // Within range

	if !r.Contains(temp) {
		t.Errorf("50°C should be within 32°F to 212°F range")
	}
}

// Test utility functions
func TestWindChill(t *testing.T) {
	// Test at 0°C with 10 km/h wind
	windChill := WindChill(0, 10)
	expected := -3.32 // Approximate expected value

	if math.Abs(windChill-expected) > 0.5 {
		t.Errorf("WindChill(0, 10) = %f, want approximately %f", windChill, expected)
	}

	// Test above 10°C - should return original temperature
	windChill = WindChill(20, 10)
	if math.Abs(windChill-20) > 0.01 {
		t.Errorf("WindChill(20, 10) = %f, want 20 (no wind chill above 10°C)", windChill)
	}

	// Test low wind speed - should return original temperature
	windChill = WindChill(0, 3)
	if math.Abs(windChill) > 0.01 {
		t.Errorf("WindChill(0, 3) = %f, want 0 (no wind chill below 4.8 km/h)", windChill)
	}
}

func TestHeatIndex(t *testing.T) {
	// Test at 30°C with 50% humidity
	heatIndex := HeatIndex(30, 50)
	
	// Heat index should be higher than actual temperature
	if heatIndex <= 30 {
		t.Errorf("HeatIndex(30, 50) = %f, should be higher than 30", heatIndex)
	}

	// Test below 27°C - should return original temperature
	heatIndex = HeatIndex(20, 50)
	if math.Abs(heatIndex-20) > 0.01 {
		t.Errorf("HeatIndex(20, 50) = %f, want 20 (no heat index below 27°C)", heatIndex)
	}
}

func TestAverage(t *testing.T) {
	t1 := NewTemperature(0, Celsius)
	t2 := NewTemperature(100, Celsius)
	t3 := NewTemperature(50, Celsius)

	avg := Average(t1, t2, t3)
	expected := 50.0

	if math.Abs(avg.Value-expected) > 0.01 {
		t.Errorf("Average = %f, want %f", avg.Value, expected)
	}
}

func TestMin(t *testing.T) {
	t1 := NewTemperature(0, Celsius)
	t2 := NewTemperature(-10, Celsius)
	t3 := NewTemperature(50, Celsius)

	min := Min(t1, t2, t3)
	if min.Value != -10 {
		t.Errorf("Min = %f, want -10", min.Value)
	}
}

func TestMax(t *testing.T) {
	t1 := NewTemperature(0, Celsius)
	t2 := NewTemperature(-10, Celsius)
	t3 := NewTemperature(50, Celsius)

	max := Max(t1, t2, t3)
	if max.Value != 50 {
		t.Errorf("Max = %f, want 50", max.Value)
	}
}

func TestDelta(t *testing.T) {
	t1 := NewTemperature(0, Celsius)
	t2 := NewTemperature(100, Celsius)

	delta := Delta(t1, t2)
	if math.Abs(delta.Value-100) > 0.01 {
		t.Errorf("Delta = %f, want 100", delta.Value)
	}

	// Test with different units
	t3 := NewTemperature(32, Fahrenheit) // 0°C
	delta2 := Delta(t1, t3)
	if math.Abs(delta2.Value) > 0.01 {
		t.Errorf("Delta between 0°C and 32°F = %f, want 0", delta2.Value)
	}
}

func TestParseUnit(t *testing.T) {
	tests := []struct {
		input    string
		expected TemperatureUnit
		hasError bool
	}{
		{"C", Celsius, false},
		{"c", Celsius, false},
		{"Celsius", Celsius, false},
		{"F", Fahrenheit, false},
		{"Fahrenheit", Fahrenheit, false},
		{"K", Kelvin, false},
		{"Kelvin", Kelvin, false},
		{"R", Rankine, false},
		{"Rankine", Rankine, false},
		{"De", Delisle, false},
		{"N", Newton, false},
		{"Re", Reaumur, false},
		{"Ro", Romer, false},
		{"X", "", true},
	}

	for _, tt := range tests {
		result, err := ParseUnit(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("ParseUnit(%s) should return error", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("ParseUnit(%s) returned error: %v", tt.input, err)
			}
			if result != tt.expected {
				t.Errorf("ParseUnit(%s) = %s, want %s", tt.input, result, tt.expected)
			}
		}
	}
}

func TestFormatWithSymbol(t *testing.T) {
	tests := []struct {
		value    float64
		unit     TemperatureUnit
		expected string
	}{
		{25.5, Celsius, "25.50°C"},
		{77, Fahrenheit, "77.00°F"},
		{298.15, Kelvin, "298.15 K"},
		{491.67, Rankine, "491.67°R"},
	}

	for _, tt := range tests {
		result := FormatWithSymbol(tt.value, tt.unit)
		if result != tt.expected {
			t.Errorf("FormatWithSymbol(%f, %s) = %s, want %s", tt.value, tt.unit, result, tt.expected)
		}
	}
}

// Test round-trip conversions
func TestRoundTrip(t *testing.T) {
	// Test that converting to another unit and back gives the original value
	original := 25.0
	
	// Celsius -> Fahrenheit -> Celsius
	fahrenheit := CelsiusTo(original, Fahrenheit)
	backToCelsius := FahrenheitTo(fahrenheit, Celsius)
	if math.Abs(original-backToCelsius) > 0.0001 {
		t.Errorf("Round trip conversion failed: %f -> %f -> %f", original, fahrenheit, backToCelsius)
	}

	// Celsius -> Kelvin -> Celsius
	kelvin := CelsiusTo(original, Kelvin)
	backToCelsius = KelvinTo(kelvin, Celsius)
	if math.Abs(original-backToCelsius) > 0.0001 {
		t.Errorf("Round trip conversion failed: %f -> %f -> %f", original, kelvin, backToCelsius)
	}
}

// Test CommonRanges
func TestCommonRanges(t *testing.T) {
	// Test that water freezing is in the water freezing to boiling range
	freezing := NewTemperature(0, Celsius)
	if !CommonRanges.WaterFreezingToBoiling.Contains(freezing) {
		t.Error("0°C should be in WaterFreezingToBoiling range")
	}

	// Test that room temperature is in human comfort range
	room := NewTemperature(20, Celsius)
	if !CommonRanges.HumanComfortRange.Contains(room) {
		t.Error("20°C should be in HumanComfortRange")
	}

	// Test that boiling is in the range
	boiling := NewTemperature(100, Celsius)
	if !CommonRanges.WaterFreezingToBoiling.Contains(boiling) {
		t.Error("100°C should be in WaterFreezingToBoiling range")
	}
}

// Benchmark tests
func BenchmarkCelsiusToFahrenheit(b *testing.B) {
	for i := 0; i < b.N; i++ {
		CelsiusTo(25.0, Fahrenheit)
	}
}

func BenchmarkTemperatureConversion(b *testing.B) {
	temp := NewTemperature(25, Celsius)
	for i := 0; i < b.N; i++ {
		temp.ConvertTo(Fahrenheit)
	}
}

func BenchmarkHeatIndex(b *testing.B) {
	for i := 0; i < b.N; i++ {
		HeatIndex(30, 50)
	}
}

func BenchmarkWindChill(b *testing.B) {
	for i := 0; i < b.N; i++ {
		WindChill(0, 15)
	}
}