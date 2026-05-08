package converter_utils

import (
	"math"
	"testing"
)

// ============================================================
// Length Conversion Tests
// ============================================================

func TestConvertLength(t *testing.T) {
	tests := []struct {
		value    float64
		from     LengthUnit
		to       LengthUnit
		expected float64
		delta    float64
	}{
		{1, Kilometer, Meter, 1000, 0},
		{1, Mile, Kilometer, 1.609344, 0.000001},
		{1, Foot, Inch, 12, 0.0001},
		{1, Yard, Foot, 3, 0},
		{100, Centimeter, Meter, 1, 0},
		{1, NauticalMile, Kilometer, 1.852, 0},
		{1000, Millimeter, Meter, 1, 0},
	}

	for _, tt := range tests {
		result, err := ConvertLength(tt.value, tt.from, tt.to)
		if err != nil {
			t.Errorf("ConvertLength(%v, %s, %s) error: %v", tt.value, tt.from, tt.to, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ConvertLength(%v, %s, %s) = %v, want %v", tt.value, tt.from, tt.to, result, tt.expected)
		}
	}
}

func TestLengthConverter(t *testing.T) {
	lc := Length(1, Mile)
	
	if km := lc.Kilometers(); math.Abs(km-1.609344) > 0.000001 {
		t.Errorf("Length(1, Mile).Kilometers() = %v, want 1.609344", km)
	}
	
	if m := lc.Meters(); math.Abs(m-1609.344) > 0.000001 {
		t.Errorf("Length(1, Mile).Meters() = %v, want 1609.344", m)
	}
	
	if ft := Length(1, Meter).Feet(); math.Abs(ft-3.28084) > 0.0001 {
		t.Errorf("Length(1, Meter).Feet() = %v, want ~3.28084", ft)
	}
}

func TestInvalidLengthUnit(t *testing.T) {
	_, err := ConvertLength(1, LengthUnit("invalid"), Meter)
	if err == nil {
		t.Error("Expected error for invalid length unit")
	}
}

// ============================================================
// Weight Conversion Tests
// ============================================================

func TestConvertWeight(t *testing.T) {
	tests := []struct {
		value    float64
		from     WeightUnit
		to       WeightUnit
		expected float64
		delta    float64
	}{
		{1, Kilogram, Gram, 1000, 0},
		{1, Pound, Kilogram, 0.45359237, 0},
		{1, Kilogram, Pound, 2.20462262, 0.000001},
		{1, Ounce, Gram, 28.349523125, 0.000001},
		{1000, Gram, Kilogram, 1, 0},
		{1, MetricTon, Kilogram, 1000, 0},
		{1, Stone, Pound, 14, 0.000001},
		{5, CarGram, Gram, 1, 0},
	}

	for _, tt := range tests {
		result, err := ConvertWeight(tt.value, tt.from, tt.to)
		if err != nil {
			t.Errorf("ConvertWeight(%v, %s, %s) error: %v", tt.value, tt.from, tt.to, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ConvertWeight(%v, %s, %s) = %v, want %v", tt.value, tt.from, tt.to, result, tt.expected)
		}
	}
}

func TestWeightConverter(t *testing.T) {
	wc := Weight(1, Pound)
	
	if kg := wc.Kilograms(); math.Abs(kg-0.45359237) > 0.000001 {
		t.Errorf("Weight(1, Pound).Kilograms() = %v, want 0.45359237", kg)
	}
	
	if oz := Weight(1, Pound).Ounces(); math.Abs(oz-16) > 0.0001 {
		t.Errorf("Weight(1, Pound).Ounces() = %v, want 16", oz)
	}
}

// ============================================================
// Temperature Conversion Tests
// ============================================================

func TestConvertTemperature(t *testing.T) {
	tests := []struct {
		value    float64
		from     TemperatureUnit
		to       TemperatureUnit
		expected float64
		delta    float64
	}{
		{0, Celsius, Fahrenheit, 32, 0},
		{100, Celsius, Fahrenheit, 212, 0},
		{0, Celsius, Kelvin, 273.15, 0},
		{32, Fahrenheit, Celsius, 0, 0.0001},
		{212, Fahrenheit, Celsius, 100, 0.0001},
		{273.15, Kelvin, Celsius, 0, 0.0001},
		{373.15, Kelvin, Celsius, 100, 0.0001},
		{-40, Celsius, Fahrenheit, -40, 0.0001}, // Special case: -40C = -40F
	}

	for _, tt := range tests {
		result, err := ConvertTemperature(tt.value, tt.from, tt.to)
		if err != nil {
			t.Errorf("ConvertTemperature(%v, %s, %s) error: %v", tt.value, tt.from, tt.to, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ConvertTemperature(%v, %s, %s) = %v, want %v", tt.value, tt.from, tt.to, result, tt.expected)
		}
	}
}

func TestTemperatureConverter(t *testing.T) {
	tc := Temperature(0, Celsius)
	
	if f := tc.Fahrenheit(); math.Abs(f-32) > 0.0001 {
		t.Errorf("Temperature(0, Celsius).Fahrenheit() = %v, want 32", f)
	}
	
	if k := tc.Kelvin(); math.Abs(k-273.15) > 0.0001 {
		t.Errorf("Temperature(0, Celsius).Kelvin() = %v, want 273.15", k)
	}
}

// ============================================================
// Time Conversion Tests
// ============================================================

func TestConvertTime(t *testing.T) {
	tests := []struct {
		value    float64
		from     TimeUnit
		to       TimeUnit
		expected float64
		delta    float64
	}{
		{1, Hour, Minute, 60, 0},
		{1, Day, Hour, 24, 0},
		{1, Week, Day, 7, 0},
		{1000, Millisecond, Second, 1, 0},
		{60, Minute, Hour, 1, 0},
		{1, Year, Day, 365.2425, 0.01},
	}

	for _, tt := range tests {
		result, err := ConvertTime(tt.value, tt.from, tt.to)
		if err != nil {
			t.Errorf("ConvertTime(%v, %s, %s) error: %v", tt.value, tt.from, tt.to, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ConvertTime(%v, %s, %s) = %v, want %v", tt.value, tt.from, tt.to, result, tt.expected)
		}
	}
}

func TestTimeConverter(t *testing.T) {
	tc := Duration(1, Hour)
	
	if min := tc.Minutes(); math.Abs(min-60) > 0.0001 {
		t.Errorf("Duration(1, Hour).Minutes() = %v, want 60", min)
	}
	
	if sec := tc.Seconds(); math.Abs(sec-3600) > 0.0001 {
		t.Errorf("Duration(1, Hour).Seconds() = %v, want 3600", sec)
	}
	
	if days := Duration(24, Hour).Days(); math.Abs(days-1) > 0.0001 {
		t.Errorf("Duration(24, Hour).Days() = %v, want 1", days)
	}
}

// ============================================================
// Data Conversion Tests
// ============================================================

func TestConvertData(t *testing.T) {
	tests := []struct {
		value    float64
		from     DataUnit
		to       DataUnit
		expected float64
		delta    float64
	}{
		{1, Kilobyte, Byte, 1000, 0},
		{1, Megabyte, Kilobyte, 1000, 0},
		{1, Gigabyte, Megabyte, 1000, 0},
		{1, Kibibyte, Byte, 1024, 0},
		{1, Mebibyte, Kibibyte, 1024, 0},
		{8, Bit, Byte, 1, 0},
		{1, Terabyte, Gigabyte, 1000, 0},
		{1024, Mebibyte, Gibibyte, 1, 0.0001},
	}

	for _, tt := range tests {
		result, err := ConvertData(tt.value, tt.from, tt.to)
		if err != nil {
			t.Errorf("ConvertData(%v, %s, %s) error: %v", tt.value, tt.from, tt.to, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ConvertData(%v, %s, %s) = %v, want %v", tt.value, tt.from, tt.to, result, tt.expected)
		}
	}
}

func TestDataConverter(t *testing.T) {
	dc := Data(1, Megabyte)
	
	if kb := dc.Kilobytes(); math.Abs(kb-1000) > 0.0001 {
		t.Errorf("Data(1, Megabyte).Kilobytes() = %v, want 1000", kb)
	}
	
	if bytes := dc.Bytes(); math.Abs(bytes-1000000) > 0.0001 {
		t.Errorf("Data(1, Megabyte).Bytes() = %v, want 1000000", bytes)
	}
}

// ============================================================
// Volume Conversion Tests
// ============================================================

func TestConvertVolume(t *testing.T) {
	tests := []struct {
		value    float64
		from     VolumeUnit
		to       VolumeUnit
		expected float64
		delta    float64
	}{
		{1, Liter, Milliliter, 1000, 0},
		{1, Gallon, Liter, 3.785411784, 0.000001},
		{1, CubicMeter, Liter, 1000, 0},
		{1, Quart, Pint, 2, 0.0001},
		{1, Cup, FluidOunce, 8, 0.0001},
		{2, Tablespoon, FluidOunce, 1, 0.0001},
		{3, Teaspoon, Tablespoon, 1, 0.0001},
	}

	for _, tt := range tests {
		result, err := ConvertVolume(tt.value, tt.from, tt.to)
		if err != nil {
			t.Errorf("ConvertVolume(%v, %s, %s) error: %v", tt.value, tt.from, tt.to, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ConvertVolume(%v, %s, %s) = %v, want %v", tt.value, tt.from, tt.to, result, tt.expected)
		}
	}
}

func TestVolumeConverter(t *testing.T) {
	vc := Volume(1, Gallon)
	
	if l := vc.Liters(); math.Abs(l-3.785411784) > 0.000001 {
		t.Errorf("Volume(1, Gallon).Liters() = %v, want 3.785411784", l)
	}
	
	if ml := Volume(1, Liter).Milliliters(); math.Abs(ml-1000) > 0.0001 {
		t.Errorf("Volume(1, Liter).Milliliters() = %v, want 1000", ml)
	}
}

// ============================================================
// Area Conversion Tests
// ============================================================

func TestConvertArea(t *testing.T) {
	tests := []struct {
		value    float64
		from     AreaUnit
		to       AreaUnit
		expected float64
		delta    float64
	}{
		{1, SquareKilometer, SquareMeter, 1000000, 0},
		{1, Hectare, SquareMeter, 10000, 0},
		{1, Acre, SquareMeter, 4046.8564224, 0.0001},
		{1, SquareMile, Acre, 640, 0.01},
		{10000, SquareMeter, Hectare, 1, 0.0001},
		{1, SquareFoot, SquareInch, 144, 0.0001},
	}

	for _, tt := range tests {
		result, err := ConvertArea(tt.value, tt.from, tt.to)
		if err != nil {
			t.Errorf("ConvertArea(%v, %s, %s) error: %v", tt.value, tt.from, tt.to, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ConvertArea(%v, %s, %s) = %v, want %v", tt.value, tt.from, tt.to, result, tt.expected)
		}
	}
}

func TestAreaConverter(t *testing.T) {
	ac := Area(1, Acre)
	
	if sqm := ac.SquareMeters(); math.Abs(sqm-4046.8564224) > 0.001 {
		t.Errorf("Area(1, Acre).SquareMeters() = %v, want 4046.8564224", sqm)
	}
	
	if ha := Area(10000, SquareMeter).Hectares(); math.Abs(ha-1) > 0.0001 {
		t.Errorf("Area(10000, SquareMeter).Hectares() = %v, want 1", ha)
	}
}

// ============================================================
// Speed Conversion Tests
// ============================================================

func TestConvertSpeed(t *testing.T) {
	tests := []struct {
		value    float64
		from     SpeedUnit
		to       SpeedUnit
		expected float64
		delta    float64
	}{
		{1, KilometerPerHour, MeterPerSecond, 1000.0/3600.0, 0.000001},
		{1, MilePerHour, KilometerPerHour, 1.609344, 0.000001},
		{1, Knot, KilometerPerHour, 1.852, 0.0001},
		{1, Mach, MeterPerSecond, 340.29, 0.01},
		{60, MilePerHour, KilometerPerHour, 96.56064, 0.0001},
	}

	for _, tt := range tests {
		result, err := ConvertSpeed(tt.value, tt.from, tt.to)
		if err != nil {
			t.Errorf("ConvertSpeed(%v, %s, %s) error: %v", tt.value, tt.from, tt.to, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ConvertSpeed(%v, %s, %s) = %v, want %v", tt.value, tt.from, tt.to, result, tt.expected)
		}
	}
}

func TestSpeedConverter(t *testing.T) {
	sc := Speed(100, KilometerPerHour)
	
	if ms := sc.MetersPerSecond(); math.Abs(ms-27.777777) > 0.001 {
		t.Errorf("Speed(100, km/h).MetersPerSecond() = %v, want ~27.78", ms)
	}
	
	if mph := sc.MilesPerHour(); math.Abs(mph-62.1371) > 0.01 {
		t.Errorf("Speed(100, km/h).MilesPerHour() = %v, want ~62.14", mph)
	}
}

// ============================================================
// Pressure Conversion Tests
// ============================================================

func TestConvertPressure(t *testing.T) {
	tests := []struct {
		value    float64
		from     PressureUnit
		to       PressureUnit
		expected float64
		delta    float64
	}{
		{1, Atmosphere, Pascal, 101325, 0.1},
		{1, Bar, Kilopascal, 100, 0},
		{1, PSI, Kilopascal, 6.894757, 0.0001},
		{760, MmHg, Atmosphere, 1, 0.001},
		{1, Atmosphere, PSI, 14.6959, 0.001},
	}

	for _, tt := range tests {
		result, err := ConvertPressure(tt.value, tt.from, tt.to)
		if err != nil {
			t.Errorf("ConvertPressure(%v, %s, %s) error: %v", tt.value, tt.from, tt.to, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ConvertPressure(%v, %s, %s) = %v, want %v", tt.value, tt.from, tt.to, result, tt.expected)
		}
	}
}

func TestPressureConverter(t *testing.T) {
	pc := Pressure(1, Atmosphere)
	
	if bar := pc.Bars(); math.Abs(bar-1.01325) > 0.0001 {
		t.Errorf("Pressure(1, atm).Bars() = %v, want 1.01325", bar)
	}
	
	if psi := pc.PSI(); math.Abs(psi-14.6959) > 0.01 {
		t.Errorf("Pressure(1, atm).PSI() = %v, want ~14.7", psi)
	}
}

// ============================================================
// Angle Conversion Tests
// ============================================================

func TestAngleConversion(t *testing.T) {
	// Test degrees to radians
	if r := ConvertDegreesToRadians(180); math.Abs(r-math.Pi) > 0.0001 {
		t.Errorf("ConvertDegreesToRadians(180) = %v, want π", r)
	}
	
	// Test radians to degrees
	if d := ConvertRadiansToDegrees(math.Pi); math.Abs(d-180) > 0.0001 {
		t.Errorf("ConvertRadiansToDegrees(π) = %v, want 180", d)
	}
	
	// Test full circle
	if r := ConvertDegreesToRadians(360); math.Abs(r-2*math.Pi) > 0.0001 {
		t.Errorf("ConvertDegreesToRadians(360) = %v, want 2π", r)
	}
}

func TestAngleConverter(t *testing.T) {
	ac := Angle(90)
	
	if r := ac.Radians(); math.Abs(r-math.Pi/2) > 0.0001 {
		t.Errorf("Angle(90).Radians() = %v, want π/2", r)
	}
	
	if d := AngleFromRadians(math.Pi).Degrees(); math.Abs(d-180) > 0.0001 {
		t.Errorf("AngleFromRadians(π).Degrees() = %v, want 180", d)
	}
}

// ============================================================
// Fuel Consumption Conversion Tests
// ============================================================

func TestConvertFuelConsumption(t *testing.T) {
	tests := []struct {
		value    float64
		from     FuelUnit
		to       FuelUnit
		expected float64
		delta    float64
	}{
		{10, LitersPer100km, KilometersPerLiter, 10, 0.0001}, // 100/10 = 10 km/L
		{10, LitersPer100km, MilesPerGallonUS, 23.5215, 0.01},
		{30, MilesPerGallonUS, LitersPer100km, 7.84, 0.01},
	}

	for _, tt := range tests {
		result, err := ConvertFuelConsumption(tt.value, tt.from, tt.to)
		if err != nil {
			t.Errorf("ConvertFuelConsumption(%v, %s, %s) error: %v", tt.value, tt.from, tt.to, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ConvertFuelConsumption(%v, %s, %s) = %v, want %v", tt.value, tt.from, tt.to, result, tt.expected)
		}
	}
}

// ============================================================
// Generic Converter Tests
// ============================================================

func TestNewConverter(t *testing.T) {
	c := NewConverter(100)
	
	// Test as length
	lc := c.AsLength(Meter)
	if km, _ := lc.To(Kilometer); math.Abs(km-0.1) > 0.0001 {
		t.Errorf("NewConverter(100).AsLength(Meter).To(Km) = %v, want 0.1", km)
	}
	
	// Test as weight
	wc := c.AsWeight(Kilogram)
	if lb := wc.Pounds(); math.Abs(lb-220.462) > 0.01 {
		t.Errorf("NewConverter(100).AsWeight(Kg).Pounds() = %v, want ~220.46", lb)
	}
	
	// Test as temperature
	tc := c.AsTemperature(Celsius)
	if f := tc.Fahrenheit(); math.Abs(f-212) > 0.01 {
		t.Errorf("NewConverter(100).AsTemperature(C).Fahrenheit() = %v, want 212", f)
	}
}

// ============================================================
// Parsing Tests
// ============================================================

func TestParseLength(t *testing.T) {
	tests := []struct {
		input    string
		expected float64 // in meters
		delta    float64
	}{
		{"100 m", 100, 0},
		{"1 km", 1000, 0},
		{"1.5 mi", 2414.016, 0.01},
		{"10 km", 10000, 0},
		{"5.5 ft", 1.6764, 0.0001},
	}

	for _, tt := range tests {
		result, err := ParseLength(tt.input)
		if err != nil {
			t.Errorf("ParseLength(%q) error: %v", tt.input, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ParseLength(%q) = %v, want %v", tt.input, result, tt.expected)
		}
	}
}

func TestParseWeight(t *testing.T) {
	tests := []struct {
		input    string
		expected float64 // in kilograms
		delta    float64
	}{
		{"100 kg", 100, 0},
		{"1 lb", 0.45359237, 0.000001},
		{"500 g", 0.5, 0},
		{"2.5 lb", 1.13398, 0.0001},
	}

	for _, tt := range tests {
		result, err := ParseWeight(tt.input)
		if err != nil {
			t.Errorf("ParseWeight(%q) error: %v", tt.input, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ParseWeight(%q) = %v, want %v", tt.input, result, tt.expected)
		}
	}
}

func TestParseTemperature(t *testing.T) {
	tests := []struct {
		input    string
		expected float64 // in Celsius
		delta    float64
	}{
		{"0 C", 0, 0},
		{"32 F", 0, 0.01},
		{"273.15 K", 0, 0.01},
		{"100 C", 100, 0},
		{"212 F", 100, 0.01},
	}

	for _, tt := range tests {
		result, err := ParseTemperature(tt.input)
		if err != nil {
			t.Errorf("ParseTemperature(%q) error: %v", tt.input, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ParseTemperature(%q) = %v, want %v", tt.input, result, tt.expected)
		}
	}
}

func TestParseDuration(t *testing.T) {
	tests := []struct {
		input    string
		expected float64 // in seconds
		delta    float64
	}{
		{"1 s", 1, 0},
		{"1 min", 60, 0},
		{"1 h", 3600, 0},
		{"1000 ms", 1, 0},
		{"2.5 h", 9000, 0},
	}

	for _, tt := range tests {
		result, err := ParseDuration(tt.input)
		if err != nil {
			t.Errorf("ParseDuration(%q) error: %v", tt.input, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ParseDuration(%q) = %v, want %v", tt.input, result, tt.expected)
		}
	}
}

func TestParseData(t *testing.T) {
	tests := []struct {
		input    string
		expected float64 // in bytes
		delta    float64
	}{
		{"1 KB", 1000, 0},
		{"1 MB", 1000000, 0},
		{"512 KB", 512000, 0},
		{"2.5 GB", 2500000000, 0},
	}

	for _, tt := range tests {
		result, err := ParseData(tt.input)
		if err != nil {
			t.Errorf("ParseData(%q) error: %v", tt.input, err)
			continue
		}
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("ParseData(%q) = %v, want %v", tt.input, result, tt.expected)
		}
	}
}

// ============================================================
// Formatting Tests
// ============================================================

func TestFormatNumber(t *testing.T) {
	tests := []struct {
		value    float64
		decimals int
		expected string
	}{
		{3.14159, 2, "3.14"},
		{3.14159, 4, "3.1416"},
		{100.0, 0, "100"},
		{0.123, 2, "0.12"},
	}

	for _, tt := range tests {
		result := FormatNumber(tt.value, tt.decimals)
		if result != tt.expected {
			t.Errorf("FormatNumber(%v, %d) = %q, want %q", tt.value, tt.decimals, result, tt.expected)
		}
	}
}

func TestFormatWithCommas(t *testing.T) {
	tests := []struct {
		value    float64
		decimals int
		expected string
	}{
		{1000, 0, "1,000"},
		{1234567.89, 2, "1,234,567.88"},
		{-1234567.89, 2, "-1,234,567.88"},
		{100.5, 1, "100.5"},
	}

	for _, tt := range tests {
		result := FormatWithCommas(tt.value, tt.decimals)
		if result != tt.expected {
			t.Errorf("FormatWithCommas(%v, %d) = %q, want %q", tt.value, tt.decimals, result, tt.expected)
		}
	}
}

func TestSmartFormatData(t *testing.T) {
	tests := []struct {
		bytes    float64
		contains string
	}{
		{500, "500 B"},
		{1024, "1.00 KB"},
		{1048576, "1.00 MB"},
		{1073741824, "1.00 GB"},
		{1099511627776, "1.00 TB"},
	}

	for _, tt := range tests {
		result := SmartFormatData(tt.bytes)
		if result != tt.contains {
			t.Errorf("SmartFormatData(%v) = %q, want %q", tt.bytes, result, tt.contains)
		}
	}
}

func TestSmartFormatDuration(t *testing.T) {
	tests := []struct {
		seconds  float64
		contains string
	}{
		{0.000001, "ns"},
		{0.001, "ms"},
		{1, "s"},
		{60, "min"},
		{3600, "h"},
		{86400, "days"},
	}

	for _, tt := range tests {
		result := SmartFormatDuration(tt.seconds)
		if !contains(result, tt.contains) {
			t.Errorf("SmartFormatDuration(%v) = %q, should contain %q", tt.seconds, result, tt.contains)
		}
	}
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(substr) == 0 || 
		(len(s) > 0 && len(substr) > 0 && findSubstring(s, substr)))
}

func findSubstring(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}

// ============================================================
// Error Tests
// ============================================================

func TestInvalidUnits(t *testing.T) {
	// Test invalid length unit
	_, err := ConvertLength(1, LengthUnit("invalid"), Meter)
	if err == nil {
		t.Error("Expected error for invalid length unit")
	}
	
	// Test invalid weight unit
	_, err = ConvertWeight(1, WeightUnit("invalid"), Kilogram)
	if err == nil {
		t.Error("Expected error for invalid weight unit")
	}
	
	// Test invalid temperature unit
	_, err = ConvertTemperature(1, TemperatureUnit("invalid"), Celsius)
	if err == nil {
		t.Error("Expected error for invalid temperature unit")
	}
	
	// Test invalid time unit
	_, err = ConvertTime(1, TimeUnit("invalid"), Second)
	if err == nil {
		t.Error("Expected error for invalid time unit")
	}
	
	// Test invalid data unit
	_, err = ConvertData(1, DataUnit("invalid"), Byte)
	if err == nil {
		t.Error("Expected error for invalid data unit")
	}
	
	// Test invalid volume unit
	_, err = ConvertVolume(1, VolumeUnit("invalid"), Liter)
	if err == nil {
		t.Error("Expected error for invalid volume unit")
	}
	
	// Test invalid area unit
	_, err = ConvertArea(1, AreaUnit("invalid"), SquareMeter)
	if err == nil {
		t.Error("Expected error for invalid area unit")
	}
	
	// Test invalid speed unit
	_, err = ConvertSpeed(1, SpeedUnit("invalid"), MeterPerSecond)
	if err == nil {
		t.Error("Expected error for invalid speed unit")
	}
	
	// Test invalid pressure unit
	_, err = ConvertPressure(1, PressureUnit("invalid"), Pascal)
	if err == nil {
		t.Error("Expected error for invalid pressure unit")
	}
	
	// Test invalid fuel unit
	_, err = ConvertFuelConsumption(1, FuelUnit("invalid"), KilometersPerLiter)
	if err == nil {
		t.Error("Expected error for invalid fuel consumption unit")
	}
}

// ============================================================
// Benchmark Tests
// ============================================================

func BenchmarkConvertLength(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ConvertLength(1, Mile, Kilometer)
	}
}

func BenchmarkConvertWeight(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ConvertWeight(1, Pound, Kilogram)
	}
}

func BenchmarkConvertTemperature(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ConvertTemperature(100, Celsius, Fahrenheit)
	}
}

func BenchmarkSmartFormatData(b *testing.B) {
	for i := 0; i < b.N; i++ {
		SmartFormatData(1234567890)
	}
}

func BenchmarkSmartFormatDuration(b *testing.B) {
	for i := 0; i < b.N; i++ {
		SmartFormatDuration(123456.789)
	}
}