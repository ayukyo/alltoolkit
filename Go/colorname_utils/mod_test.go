package colorname_utils

import (
	"math"
	"strings"
	"testing"
)

func TestParseHex(t *testing.T) {
	tests := []struct {
		input    string
		expected RGB
		hasError bool
	}{
		{"#FF0000", RGB{255, 0, 0}, false},
		{"ff0000", RGB{255, 0, 0}, false},
		{"F00", RGB{255, 0, 0}, false},
		{"#00FF00", RGB{0, 255, 0}, false},
		{"#0000FF", RGB{0, 0, 255}, false},
		{"FFFFFF", RGB{255, 255, 255}, false},
		{"000000", RGB{0, 0, 0}, false},
		{"#123456", RGB{0x12, 0x34, 0x56}, false},
		{"invalid", RGB{}, true},
		{"#GGG", RGB{}, true},
	}

	for _, tt := range tests {
		result, err := ParseHex(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("ParseHex(%q) expected error, got none", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("ParseHex(%q) unexpected error: %v", tt.input, err)
			}
			if result != tt.expected {
				t.Errorf("ParseHex(%q) = %v, want %v", tt.input, result, tt.expected)
			}
		}
	}
}

func TestParseRGB(t *testing.T) {
	tests := []struct {
		input    string
		expected RGB
		hasError bool
	}{
		{"rgb(255, 0, 0)", RGB{255, 0, 0}, false},
		{"RGB(0, 255, 0)", RGB{0, 255, 0}, false},
		{"0, 0, 255", RGB{0, 0, 255}, false},
		{"255,255,255", RGB{255, 255, 255}, false},
		{" 128 , 64 , 32 ", RGB{128, 64, 32}, false},
		{"256, 0, 0", RGB{}, true},
		{"-1, 0, 0", RGB{}, true},
		{"invalid", RGB{}, true},
	}

	for _, tt := range tests {
		result, err := ParseRGB(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("ParseRGB(%q) expected error, got none", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("ParseRGB(%q) unexpected error: %v", tt.input, err)
			}
			if result != tt.expected {
				t.Errorf("ParseRGB(%q) = %v, want %v", tt.input, result, tt.expected)
			}
		}
	}
}

func TestRGBToHex(t *testing.T) {
	tests := []struct {
		rgb      RGB
		expected string
	}{
		{RGB{255, 0, 0}, "#FF0000"},
		{RGB{0, 255, 0}, "#00FF00"},
		{RGB{0, 0, 255}, "#0000FF"},
		{RGB{255, 255, 255}, "#FFFFFF"},
		{RGB{0, 0, 0}, "#000000"},
		{RGB{18, 52, 86}, "#123456"},
	}

	for _, tt := range tests {
		result := RGBToHex(tt.rgb)
		if result != tt.expected {
			t.Errorf("RGBToHex(%v) = %s, want %s", tt.rgb, result, tt.expected)
		}
	}
}

func TestRGBToHSL(t *testing.T) {
	tests := []struct {
		rgb          RGB
		expectedHMin float64
		expectedHMax float64
		expectedSMin float64
		expectedSMax float64
		expectedLMin float64
		expectedLMax float64
	}{
		{RGB{255, 0, 0}, 0, 0, 99, 101, 49, 51},         // Red: H=0, S=100, L=50
		{RGB{0, 255, 0}, 119, 121, 99, 101, 49, 51},     // Green: H=120, S=100, L=50
		{RGB{0, 0, 255}, 239, 241, 99, 101, 49, 51},     // Blue: H=240, S=100, L=50
		{RGB{255, 255, 255}, 0, 360, 0, 1, 99, 101},     // White: S=0, L=100
		{RGB{0, 0, 0}, 0, 360, 0, 1, 0, 1},              // Black: S=0, L=0
		{RGB{128, 128, 128}, 0, 360, 0, 1, 49, 51},      // Gray: S=0, L=50
	}

	for _, tt := range tests {
		result := RGBToHSL(tt.rgb)
		if result.H < tt.expectedHMin || result.H > tt.expectedHMax {
			t.Errorf("RGBToHSL(%v).H = %v, want between %v and %v", tt.rgb, result.H, tt.expectedHMin, tt.expectedHMax)
		}
		if result.S < tt.expectedSMin || result.S > tt.expectedSMax {
			t.Errorf("RGBToHSL(%v).S = %v, want between %v and %v", tt.rgb, result.S, tt.expectedSMin, tt.expectedSMax)
		}
		if result.L < tt.expectedLMin || result.L > tt.expectedLMax {
			t.Errorf("RGBToHSL(%v).L = %v, want between %v and %v", tt.rgb, result.L, tt.expectedLMin, tt.expectedLMax)
		}
	}
}

func TestHSLToRGB(t *testing.T) {
	tests := []struct {
		hsl      HSL
		expected RGB
	}{
		{HSL{0, 100, 50}, RGB{255, 0, 0}},       // Red
		{HSL{120, 100, 50}, RGB{0, 255, 0}},     // Green
		{HSL{240, 100, 50}, RGB{0, 0, 255}},     // Blue
		{HSL{0, 0, 100}, RGB{255, 255, 255}},    // White
		{HSL{0, 0, 0}, RGB{0, 0, 0}},            // Black
		{HSL{0, 0, 50}, RGB{128, 128, 128}},     // Gray
	}

	for _, tt := range tests {
		result := HSLToRGB(tt.hsl)
		// Allow small tolerance due to rounding
		if math.Abs(float64(result.R)-float64(tt.expected.R)) > 1 ||
			math.Abs(float64(result.G)-float64(tt.expected.G)) > 1 ||
			math.Abs(float64(result.B)-float64(tt.expected.B)) > 1 {
			t.Errorf("HSLToRGB(%v) = %v, want %v", tt.hsl, result, tt.expected)
		}
	}
}

func TestColorDistance(t *testing.T) {
	// Same color should have distance 0
	dist := ColorDistance(RGB{255, 0, 0}, RGB{255, 0, 0})
	if dist != 0 {
		t.Errorf("ColorDistance of same color = %v, want 0", dist)
	}

	// Different colors should have positive distance
	dist = ColorDistance(RGB{255, 0, 0}, RGB{0, 0, 255})
	if dist <= 0 {
		t.Errorf("ColorDistance of different colors = %v, want > 0", dist)
	}

	// Similar colors should have small distance
	dist = ColorDistance(RGB{255, 0, 0}, RGB{250, 0, 0})
	if dist > 10 {
		t.Errorf("ColorDistance of similar colors = %v, want < 10", dist)
	}
}

func TestGetColorName(t *testing.T) {
	tests := []struct {
		rgb           RGB
		expectedNames []string // Should match one of these
	}{
		{RGB{255, 0, 0}, []string{"Red"}},
		{RGB{0, 255, 0}, []string{"Lime", "Green"}},
		{RGB{0, 0, 255}, []string{"Blue"}},
		{RGB{255, 255, 255}, []string{"White"}},
		{RGB{0, 0, 0}, []string{"Black"}},
		{RGB{255, 165, 0}, []string{"Orange"}},
		{RGB{255, 255, 0}, []string{"Yellow"}},
	}

	for _, tt := range tests {
		result := GetColorName(tt.rgb)
		found := false
		for _, name := range tt.expectedNames {
			if result == name {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("GetColorName(%v) = %s, want one of %v", tt.rgb, result, tt.expectedNames)
		}
	}
}

func TestGetClosestColor(t *testing.T) {
	result := GetClosestColor(RGB{255, 0, 0})
	if result.Name != "Red" {
		t.Errorf("GetClosestColor(Red) = %s, want Red", result.Name)
	}
	if result.Distance != 0 {
		t.Errorf("GetClosestColor exact match distance = %v, want 0", result.Distance)
	}
}

func TestGetNClosestColors(t *testing.T) {
	results := GetNClosestColors(RGB{255, 0, 0}, 5)
	if len(results) != 5 {
		t.Errorf("GetNClosestColors returned %d colors, want 5", len(results))
	}

	// First should be exact match
	if results[0].Name != "Red" {
		t.Errorf("GetNClosestColors[0] = %s, want Red", results[0].Name)
	}

	// Should be sorted by distance
	for i := 1; i < len(results); i++ {
		if results[i].Distance < results[i-1].Distance {
			t.Errorf("GetNClosestColors not sorted: results[%d].Distance < results[%d].Distance", i, i-1)
		}
	}
}

func TestGetColorCategory(t *testing.T) {
	tests := []struct {
		rgb          RGB
		expected     string
	}{
		{RGB{255, 0, 0}, "Red"},
		{RGB{255, 165, 0}, "Orange"},
		{RGB{255, 255, 0}, "Yellow"},
		{RGB{0, 255, 0}, "Green"},
		{RGB{0, 255, 255}, "Cyan"},
		{RGB{0, 0, 255}, "Blue"},
		{RGB{255, 255, 255}, "White"},
		{RGB{0, 0, 0}, "Black"},
		{RGB{128, 128, 128}, "Gray"},
	}

	for _, tt := range tests {
		result := GetColorCategory(tt.rgb)
		if result != tt.expected {
			t.Errorf("GetColorCategory(%v) = %s, want %s", tt.rgb, result, tt.expected)
		}
	}
}

func TestGetBrightness(t *testing.T) {
	tests := []struct {
		rgb      RGB
		expected string
	}{
		{RGB{0, 0, 0}, "Dark"},
		{RGB{50, 50, 50}, "Dark"},
		{RGB{128, 128, 128}, "Medium"},
		{RGB{200, 200, 200}, "Light"},
		{RGB{255, 255, 255}, "Light"},
		{RGB{255, 0, 0}, "Medium"}, // Luminance: 0.299*255 ≈ 76
		{RGB{0, 0, 255}, "Dark"},   // Luminance: 0.114*255 ≈ 29
	}

	for _, tt := range tests {
		result := GetBrightness(tt.rgb)
		if result != tt.expected {
			t.Errorf("GetBrightness(%v) = %s, want %s", tt.rgb, result, tt.expected)
		}
	}
}

func TestGetTemperature(t *testing.T) {
	tests := []struct {
		rgb      RGB
		expected string
	}{
		{RGB{255, 0, 0}, "Warm"},       // R-B = 255
		{RGB{0, 0, 255}, "Cool"},       // R-B = -255
		{RGB{128, 128, 128}, "Neutral"}, // R-B = 0
		{RGB{255, 128, 0}, "Warm"},     // Orange: R-B = 255
		{RGB{0, 128, 255}, "Cool"},     // Light blue: R-B = -255
	}

	for _, tt := range tests {
		result := GetTemperature(tt.rgb)
		if result != tt.expected {
			t.Errorf("GetTemperature(%v) = %s, want %s", tt.rgb, result, tt.expected)
		}
	}
}

func TestGetColorInfo(t *testing.T) {
	info := GetColorInfo(RGB{255, 0, 0})

	if info.Name != "Red" {
		t.Errorf("GetColorInfo.Name = %s, want Red", info.Name)
	}
	if info.Hex != "#FF0000" {
		t.Errorf("GetColorInfo.Hex = %s, want #FF0000", info.Hex)
	}
	if info.RGB != (RGB{255, 0, 0}) {
		t.Errorf("GetColorInfo.RGB = %v, want {255, 0, 0}", info.RGB)
	}
	if info.Category != "Red" {
		t.Errorf("GetColorInfo.Category = %s, want Red", info.Category)
	}
}

func TestGetColorInfoHex(t *testing.T) {
	info, err := GetColorInfoHex("#FF0000")
	if err != nil {
		t.Errorf("GetColorInfoHex unexpected error: %v", err)
	}
	if info.Name != "Red" {
		t.Errorf("GetColorInfoHex.Name = %s, want Red", info.Name)
	}

	_, err = GetColorInfoHex("invalid")
	if err == nil {
		t.Error("GetColorInfoHex expected error for invalid input")
	}
}

func TestIsLightColor(t *testing.T) {
	if !IsLightColor(RGB{255, 255, 255}) {
		t.Error("IsLightColor(White) = false, want true")
	}
	if IsLightColor(RGB{0, 0, 0}) {
		t.Error("IsLightColor(Black) = true, want false")
	}
}

func TestIsDarkColor(t *testing.T) {
	if !IsDarkColor(RGB{0, 0, 0}) {
		t.Error("IsDarkColor(Black) = false, want true")
	}
	if IsDarkColor(RGB{255, 255, 255}) {
		t.Error("IsDarkColor(White) = true, want false")
	}
}

func TestGetContrastColor(t *testing.T) {
	// Dark background should get white contrast
	contrast := GetContrastColor(RGB{0, 0, 0})
	if contrast != (RGB{255, 255, 255}) {
		t.Errorf("GetContrastColor(Black) = %v, want White", contrast)
	}

	// Light background should get black contrast
	contrast = GetContrastColor(RGB{255, 255, 255})
	if contrast != (RGB{0, 0, 0}) {
		t.Errorf("GetContrastColor(White) = %v, want Black", contrast)
	}
}

func TestBlendColors(t *testing.T) {
	tests := []struct {
		c1       RGB
		c2       RGB
		ratio    float64
		expected RGB
	}{
		{RGB{255, 0, 0}, RGB{0, 0, 255}, 0, RGB{255, 0, 0}},
		{RGB{255, 0, 0}, RGB{0, 0, 255}, 1, RGB{0, 0, 255}},
		{RGB{255, 0, 0}, RGB{0, 0, 255}, 0.5, RGB{128, 0, 128}},
		{RGB{0, 0, 0}, RGB{255, 255, 255}, 0.5, RGB{128, 128, 128}},
	}

	for _, tt := range tests {
		result := BlendColors(tt.c1, tt.c2, tt.ratio)
		if math.Abs(float64(result.R)-float64(tt.expected.R)) > 1 ||
			math.Abs(float64(result.G)-float64(tt.expected.G)) > 1 ||
			math.Abs(float64(result.B)-float64(tt.expected.B)) > 1 {
			t.Errorf("BlendColors(%v, %v, %v) = %v, want %v", tt.c1, tt.c2, tt.ratio, result, tt.expected)
		}
	}
}

func TestLighten(t *testing.T) {
	result := Lighten(RGB{128, 128, 128}, 20)
	// Should be lighter
	if result.R <= 128 || result.G <= 128 || result.B <= 128 {
		t.Errorf("Lighten should produce lighter color, got %v", result)
	}
}

func TestDarken(t *testing.T) {
	result := Darken(RGB{128, 128, 128}, 20)
	// Should be darker
	if result.R >= 128 || result.G >= 128 || result.B >= 128 {
		t.Errorf("Darken should produce darker color, got %v", result)
	}
}

func TestSaturate(t *testing.T) {
	result := Saturate(RGB{128, 100, 100}, 20)
	// Saturation should increase
	hslOrig := RGBToHSL(RGB{128, 100, 100})
	hslNew := RGBToHSL(result)
	if hslNew.S <= hslOrig.S {
		t.Errorf("Saturate should increase saturation: %v -> %v", hslOrig.S, hslNew.S)
	}
}

func TestDesaturate(t *testing.T) {
	result := Desaturate(RGB{128, 100, 100}, 20)
	// Saturation should decrease
	hslOrig := RGBToHSL(RGB{128, 100, 100})
	hslNew := RGBToHSL(result)
	if hslNew.S >= hslOrig.S {
		t.Errorf("Desaturate should decrease saturation: %v -> %v", hslOrig.S, hslNew.S)
	}
}

func TestComplementaryColor(t *testing.T) {
	tests := []struct {
		rgb          RGB
		expectedHMin float64
		expectedHMax float64
	}{
		{RGB{255, 0, 0}, 175, 185}, // Red -> Cyan (H ~= 180)
		{RGB{0, 255, 0}, 295, 305}, // Green -> Purple (H ~= 300)
		{RGB{0, 0, 255}, 55, 65},   // Blue -> Yellow (H ~= 60)
	}

	for _, tt := range tests {
		result := ComplementaryColor(tt.rgb)
		hsl := RGBToHSL(result)
		if hsl.H < tt.expectedHMin || hsl.H > tt.expectedHMax {
			t.Errorf("ComplementaryColor(%v) H = %v, want between %v and %v", tt.rgb, hsl.H, tt.expectedHMin, tt.expectedHMax)
		}
	}
}

func TestAnalogousColors(t *testing.T) {
	colors := AnalogousColors(RGB{255, 0, 0})
	if len(colors) != 3 {
		t.Errorf("AnalogousColors returned %d colors, want 3", len(colors))
	}

	// Middle color should be the original
	if colors[1] != (RGB{255, 0, 0}) {
		t.Error("AnalogousColors middle should be original color")
	}
}

func TestTriadicColors(t *testing.T) {
	colors := TriadicColors(RGB{255, 0, 0})
	if len(colors) != 3 {
		t.Errorf("TriadicColors returned %d colors, want 3", len(colors))
	}

	// First color should be the original
	if colors[0] != (RGB{255, 0, 0}) {
		t.Error("TriadicColors first should be original color")
	}
}

func TestSplitComplementaryColors(t *testing.T) {
	colors := SplitComplementaryColors(RGB{255, 0, 0})
	if len(colors) != 3 {
		t.Errorf("SplitComplementaryColors returned %d colors, want 3", len(colors))
	}
}

func TestTetradicColors(t *testing.T) {
	colors := TetradicColors(RGB{255, 0, 0})
	if len(colors) != 4 {
		t.Errorf("TetradicColors returned %d colors, want 4", len(colors))
	}
}

func TestSearchColorNames(t *testing.T) {
	// Search for "blue"
	results := SearchColorNames("blue")
	if len(results) == 0 {
		t.Error("SearchColorNames('blue') returned no results")
	}

	// All results should contain "blue" (case insensitive)
	for _, r := range results {
		if !strings.Contains(strings.ToLower(r.Name), "blue") {
			t.Errorf("SearchColorNames result '%s' doesn't contain 'blue'", r.Name)
		}
	}
}

func TestSearchColorNamesPartial(t *testing.T) {
	// Search for "green"
	results := SearchColorNames("green")
	if len(results) == 0 {
		t.Error("SearchColorNames('green') returned no results")
	}

	// Should find colors like "Green", "Forest Green", etc.
	for _, r := range results {
		if !strings.Contains(strings.ToLower(r.Name), "green") {
			t.Errorf("SearchColorNames result '%s' doesn't contain 'green'", r.Name)
		}
	}
}

func TestGetColorByName(t *testing.T) {
	// Test exact match
	rgb, found := GetColorByName("Red")
	if !found {
		t.Error("GetColorByName('Red') not found")
	}
	if rgb != (RGB{255, 0, 0}) {
		t.Errorf("GetColorByName('Red') = %v, want {255, 0, 0}", rgb)
	}

	// Test case insensitive
	rgb, found = GetColorByName("red")
	if !found {
		t.Error("GetColorByName('red') not found")
	}

	// Test not found
	_, found = GetColorByName("nonexistentcolor")
	if found {
		t.Error("GetColorByName('nonexistentcolor') should not be found")
	}
}

func TestColorCount(t *testing.T) {
	count := ColorCount()
	if count < 100 {
		t.Errorf("ColorCount() = %d, want at least 100", count)
	}
}

func TestGetAllColorNames(t *testing.T) {
	names := GetAllColorNames()
	if len(names) != ColorCount() {
		t.Errorf("GetAllColorNames() length = %d, want %d", len(names), ColorCount())
	}
}

func TestInvertColor(t *testing.T) {
	tests := []struct {
		rgb      RGB
		expected RGB
	}{
		{RGB{255, 0, 0}, RGB{0, 255, 255}},         // Red -> Cyan
		{RGB{0, 255, 0}, RGB{255, 0, 255}},         // Green -> Magenta
		{RGB{0, 0, 255}, RGB{255, 255, 0}},         // Blue -> Yellow
		{RGB{255, 255, 255}, RGB{0, 0, 0}},         // White -> Black
		{RGB{0, 0, 0}, RGB{255, 255, 255}},         // Black -> White
		{RGB{128, 128, 128}, RGB{127, 127, 127}},   // Gray
	}

	for _, tt := range tests {
		result := InvertColor(tt.rgb)
		if result != tt.expected {
			t.Errorf("InvertColor(%v) = %v, want %v", tt.rgb, result, tt.expected)
		}
	}
}

func TestGrayscale(t *testing.T) {
	result := Grayscale(RGB{255, 0, 0})
	// Should be gray (all channels equal)
	if result.R != result.G || result.G != result.B {
		t.Errorf("Grayscale should produce equal channels, got %v", result)
	}
}

func TestSepia(t *testing.T) {
	result := Sepia(RGB{255, 255, 255})
	// Sepia white should have specific warm tone
	if result.R < result.G || result.G < result.B {
		t.Errorf("Sepia should produce warm tone (R>=G>=B), got %v", result)
	}
}

func TestAdjustBrightness(t *testing.T) {
	// Lighten
	result := AdjustBrightness(RGB{128, 128, 128}, 50)
	if result.R <= 128 {
		t.Errorf("AdjustBrightness with positive factor should lighten, got %v", result)
	}

	// Darken
	result = AdjustBrightness(RGB{128, 128, 128}, -50)
	if result.R >= 128 {
		t.Errorf("AdjustBrightness with negative factor should darken, got %v", result)
	}
}

func TestAreColorsSimilar(t *testing.T) {
	// Same colors
	if !AreColorsSimilar(RGB{255, 0, 0}, RGB{255, 0, 0}, 0) {
		t.Error("AreColorsSimilar: same colors should be similar with threshold 0")
	}

	// Close colors
	if !AreColorsSimilar(RGB{255, 0, 0}, RGB{250, 0, 0}, 10) {
		t.Error("AreColorsSimilar: close colors should be similar with threshold 10")
	}

	// Distant colors
	if AreColorsSimilar(RGB{255, 0, 0}, RGB{0, 0, 255}, 10) {
		t.Error("AreColorsSimilar: distant colors should not be similar with threshold 10")
	}
}

func TestRGBString(t *testing.T) {
	result := RGBString(RGB{255, 128, 0})
	expected := "rgb(255, 128, 0)"
	if result != expected {
		t.Errorf("RGBString = %s, want %s", result, expected)
	}
}

func TestHSLString(t *testing.T) {
	result := HSLString(HSL{180, 50, 75})
	// Should contain hsl(180, 50%, 75%)
	if result == "" {
		t.Error("HSLString returned empty string")
	}
}

func TestRandomColor(t *testing.T) {
	color := RandomColor()
	// Should produce valid RGB values (0-255)
	if color.R > 255 || color.G > 255 || color.B > 255 {
		t.Errorf("RandomColor produced invalid color: %v", color)
	}
}

func TestRandomPastelColor(t *testing.T) {
	color := RandomPastelColor()
	// Pastel colors should have values >= 128
	if color.R < 128 || color.G < 128 || color.B < 128 {
		t.Errorf("RandomPastelColor should have values >= 128, got %v", color)
	}
}

func TestRandomDarkColor(t *testing.T) {
	color := RandomDarkColor()
	// Dark colors should have values < 100
	if color.R >= 100 || color.G >= 100 || color.B >= 100 {
		t.Errorf("RandomDarkColor should have values < 100, got %v", color)
	}
}

// Benchmark tests
func BenchmarkGetColorName(b *testing.B) {
	for i := 0; i < b.N; i++ {
		GetColorName(RGB{255, 0, 0})
	}
}

func BenchmarkColorDistance(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ColorDistance(RGB{255, 0, 0}, RGB{128, 128, 128})
	}
}

func BenchmarkRGBToHSL(b *testing.B) {
	for i := 0; i < b.N; i++ {
		RGBToHSL(RGB{255, 128, 64})
	}
}

func BenchmarkHSLToRGB(b *testing.B) {
	for i := 0; i < b.N; i++ {
		HSLToRGB(HSL{180, 50, 75})
	}
}