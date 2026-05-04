package color_utils

import (
	"math"
	"testing"
)

// --- RGB Conversion Tests ---

func TestRGBToHex(t *testing.T) {
	tests := []struct {
		rgb  RGB
		want string
	}{
		{RGB{255, 0, 0}, "#ff0000"},
		{RGB{0, 255, 0}, "#00ff00"},
		{RGB{0, 0, 255}, "#0000ff"},
		{RGB{255, 255, 255}, "#ffffff"},
		{RGB{0, 0, 0}, "#000000"},
		{RGB{128, 128, 128}, "#808080"},
	}

	for _, tt := range tests {
		got := RGBToHex(tt.rgb)
		if got != tt.want {
			t.Errorf("RGBToHex(%v) = %s, want %s", tt.rgb, got, tt.want)
		}
	}
}

func TestHexToRGB(t *testing.T) {
	tests := []struct {
		hex     string
		want    RGB
		wantErr bool
	}{
		{"#ff0000", RGB{255, 0, 0}, false},
		{"ff0000", RGB{255, 0, 0}, false},
		{"#f00", RGB{255, 0, 0}, false},
		{"f00", RGB{255, 0, 0}, false},
		{"#00ff00", RGB{0, 255, 0}, false},
		{"#0000ff", RGB{0, 0, 255}, false},
		{"#ffffff", RGB{255, 255, 255}, false},
		{"#000000", RGB{0, 0, 0}, false},
		{"#808080", RGB{128, 128, 128}, false},
		{"invalid", RGB{}, true},
		{"#xyz", RGB{}, true},
	}

	for _, tt := range tests {
		got, err := HexToRGB(tt.hex)
		if (err != nil) != tt.wantErr {
			t.Errorf("HexToRGB(%s) error = %v, wantErr %v", tt.hex, err, tt.wantErr)
		}
		if !tt.wantErr && got != tt.want {
			t.Errorf("HexToRGB(%s) = %v, want %v", tt.hex, got, tt.want)
		}
	}
}

func TestRGBToHSL(t *testing.T) {
	tests := []struct {
		rgb      RGB
		wantHMin float64
		wantHMax float64
		wantSMin float64
		wantSMax float64
		wantLMin float64
		wantLMax float64
	}{
		// Red
		{RGB{255, 0, 0}, 0, 0, 99, 101, 49, 51},
		// Green
		{RGB{0, 255, 0}, 119, 121, 99, 101, 49, 51},
		// Blue
		{RGB{0, 0, 255}, 239, 241, 99, 101, 49, 51},
		// White (achromatic)
		{RGB{255, 255, 255}, 0, 360, -1, 1, 99, 101},
		// Black (achromatic)
		{RGB{0, 0, 0}, 0, 360, -1, 1, -1, 1},
		// Gray
		{RGB{128, 128, 128}, 0, 360, -1, 1, 49, 51},
	}

	for _, tt := range tests {
		hsl := RGBToHSL(tt.rgb)
		if hsl.H < tt.wantHMin || hsl.H > tt.wantHMax {
			t.Errorf("RGBToHSL(%v).H = %v, want range [%v, %v]", tt.rgb, hsl.H, tt.wantHMin, tt.wantHMax)
		}
		if hsl.S < tt.wantSMin || hsl.S > tt.wantSMax {
			t.Errorf("RGBToHSL(%v).S = %v, want range [%v, %v]", tt.rgb, hsl.S, tt.wantSMin, tt.wantSMax)
		}
		if hsl.L < tt.wantLMin || hsl.L > tt.wantLMax {
			t.Errorf("RGBToHSL(%v).L = %v, want range [%v, %v]", tt.rgb, hsl.L, tt.wantLMin, tt.wantLMax)
		}
	}
}

func TestHSLToRGB(t *testing.T) {
	tests := []struct {
		hsl  HSL
		want RGB
	}{
		{HSL{0, 100, 50}, RGB{255, 0, 0}},          // Red
		{HSL{120, 100, 50}, RGB{0, 255, 0}},       // Green
		{HSL{240, 100, 50}, RGB{0, 0, 255}},       // Blue
		{HSL{0, 0, 100}, RGB{255, 255, 255}},      // White
		{HSL{0, 0, 0}, RGB{0, 0, 0}},              // Black
		{HSL{0, 0, 50}, RGB{128, 128, 128}},      // Gray
	}

	for _, tt := range tests {
		got := HSLToRGB(tt.hsl)
		if !colorEqual(got, tt.want, 2) {
			t.Errorf("HSLToRGB(%v) = %v, want %v", tt.hsl, got, tt.want)
		}
	}
}

func TestRGBToHSV(t *testing.T) {
	tests := []struct {
		rgb RGB
		h   float64
		s   float64
		v   float64
	}{
		{RGB{255, 0, 0}, 0, 100, 100},       // Red
		{RGB{0, 255, 0}, 120, 100, 100},     // Green
		{RGB{0, 0, 255}, 240, 100, 100},     // Blue
		{RGB{255, 255, 255}, 0, 0, 100},    // White
		{RGB{0, 0, 0}, 0, 0, 0},            // Black
	}

	for _, tt := range tests {
		hsv := RGBToHSV(tt.rgb)
		if math.Abs(hsv.H-tt.h) > 1 || math.Abs(hsv.S-tt.s) > 1 || math.Abs(hsv.V-tt.v) > 1 {
			t.Errorf("RGBToHSV(%v) = HSL{%.1f, %.1f, %.1f}, want {%.1f, %.1f, %.1f}",
				tt.rgb, hsv.H, hsv.S, hsv.V, tt.h, tt.s, tt.v)
		}
	}
}

func TestHSVToRGB(t *testing.T) {
	tests := []struct {
		hsv  HSV
		want RGB
	}{
		{HSV{0, 100, 100}, RGB{255, 0, 0}},      // Red
		{HSV{120, 100, 100}, RGB{0, 255, 0}},    // Green
		{HSV{240, 100, 100}, RGB{0, 0, 255}},    // Blue
		{HSV{0, 0, 100}, RGB{255, 255, 255}},    // White
		{HSV{0, 0, 0}, RGB{0, 0, 0}},           // Black
	}

	for _, tt := range tests {
		got := HSVToRGB(tt.hsv)
		if !colorEqual(got, tt.want, 2) {
			t.Errorf("HSVToRGB(%v) = %v, want %v", tt.hsv, got, tt.want)
		}
	}
}

func TestRGBToCMYK(t *testing.T) {
	tests := []struct {
		rgb     RGB
		wantC   float64
		wantM   float64
		wantY   float64
		wantK   float64
	}{
		{RGB{255, 0, 0}, 0, 100, 100, 0},       // Red
		{RGB{0, 255, 0}, 100, 0, 100, 0},      // Green
		{RGB{0, 0, 255}, 100, 100, 0, 0},      // Blue
		{RGB{255, 255, 255}, 0, 0, 0, 0},      // White
		{RGB{0, 0, 0}, 0, 0, 0, 100},          // Black
	}

	for _, tt := range tests {
		cmyk := RGBToCMYK(tt.rgb)
		if math.Abs(cmyk.C-tt.wantC) > 1 || math.Abs(cmyk.M-tt.wantM) > 1 ||
			math.Abs(cmyk.Y-tt.wantY) > 1 || math.Abs(cmyk.K-tt.wantK) > 1 {
			t.Errorf("RGBToCMYK(%v) = CMYK{%.1f, %.1f, %.1f, %.1f}, want {%.1f, %.1f, %.1f, %.1f}",
				tt.rgb, cmyk.C, cmyk.M, cmyk.Y, cmyk.K, tt.wantC, tt.wantM, tt.wantY, tt.wantK)
		}
	}
}

func TestCMYKToRGB(t *testing.T) {
	tests := []struct {
		cmyk CMYK
		want RGB
	}{
		{CMYK{0, 100, 100, 0}, RGB{255, 0, 0}},     // Red
		{CMYK{100, 0, 100, 0}, RGB{0, 255, 0}},     // Green
		{CMYK{100, 100, 0, 0}, RGB{0, 0, 255}},     // Blue
		{CMYK{0, 0, 0, 0}, RGB{255, 255, 255}},     // White
		{CMYK{0, 0, 0, 100}, RGB{0, 0, 0}},         // Black
	}

	for _, tt := range tests {
		got := CMYKToRGB(tt.cmyk)
		if !colorEqual(got, tt.want, 2) {
			t.Errorf("CMYKToRGB(%v) = %v, want %v", tt.cmyk, got, tt.want)
		}
	}
}

// --- Round-trip Tests ---

func TestRGBHSLRoundTrip(t *testing.T) {
	colors := []RGB{
		{255, 0, 0},
		{0, 255, 0},
		{0, 0, 255},
		{255, 128, 0},
		{128, 128, 128},
		{255, 255, 255},
		{0, 0, 0},
	}

	for _, original := range colors {
		hsl := RGBToHSL(original)
		roundTrip := HSLToRGB(hsl)
		if !colorEqual(original, roundTrip, 1) {
			t.Errorf("RGB->HSL->RGB round trip failed: %v -> %v -> %v", original, hsl, roundTrip)
		}
	}
}

func TestRGBHSVRoundTrip(t *testing.T) {
	colors := []RGB{
		{255, 0, 0},
		{0, 255, 0},
		{0, 0, 255},
		{255, 128, 0},
		{128, 128, 128},
	}

	for _, original := range colors {
		hsv := RGBToHSV(original)
		roundTrip := HSVToRGB(hsv)
		if !colorEqual(original, roundTrip, 1) {
			t.Errorf("RGB->HSV->RGB round trip failed: %v -> %v -> %v", original, hsv, roundTrip)
		}
	}
}

func TestRGBCMYKRoundTrip(t *testing.T) {
	colors := []RGB{
		{255, 0, 0},
		{0, 255, 0},
		{0, 0, 255},
		{255, 128, 0},
		{128, 128, 128},
		{255, 255, 255},
		{0, 0, 0},
	}

	for _, original := range colors {
		cmyk := RGBToCMYK(original)
		roundTrip := CMYKToRGB(cmyk)
		if !colorEqual(original, roundTrip, 1) {
			t.Errorf("RGB->CMYK->RGB round trip failed: %v -> %v -> %v", original, cmyk, roundTrip)
		}
	}
}

// --- Color Manipulation Tests ---

func TestComplementary(t *testing.T) {
	tests := []struct {
		rgb  RGB
		want RGB
	}{
		{RGB{0, 0, 0}, RGB{255, 255, 255}},
		{RGB{255, 255, 255}, RGB{0, 0, 0}},
		{RGB{255, 0, 0}, RGB{0, 255, 255}},
		{RGB{0, 255, 0}, RGB{255, 0, 255}},
		{RGB{0, 0, 255}, RGB{255, 255, 0}},
	}

	for _, tt := range tests {
		got := Complementary(tt.rgb)
		if got != tt.want {
			t.Errorf("Complementary(%v) = %v, want %v", tt.rgb, got, tt.want)
		}
	}
}

func TestMix(t *testing.T) {
	tests := []struct {
		c1     RGB
		c2     RGB
		weight float64
		want   RGB
	}{
		{RGB{0, 0, 0}, RGB{255, 255, 255}, 0.0, RGB{0, 0, 0}},
		{RGB{0, 0, 0}, RGB{255, 255, 255}, 1.0, RGB{255, 255, 255}},
		{RGB{0, 0, 0}, RGB{255, 255, 255}, 0.5, RGB{128, 128, 128}},
		{RGB{255, 0, 0}, RGB{0, 0, 255}, 0.5, RGB{128, 0, 128}},
	}

	for _, tt := range tests {
		got := Mix(tt.c1, tt.c2, tt.weight)
		if !colorEqual(got, tt.want, 1) {
			t.Errorf("Mix(%v, %v, %.1f) = %v, want %v", tt.c1, tt.c2, tt.weight, got, tt.want)
		}
	}
}

func TestGrayscale(t *testing.T) {
	tests := []struct {
		rgb  RGB
	}{
		{RGB{255, 0, 0}},
		{RGB{0, 255, 0}},
		{RGB{0, 0, 255}},
		{RGB{255, 255, 255}},
		{RGB{0, 0, 0}},
	}

	for _, tt := range tests {
		gray := Grayscale(tt.rgb)
		// Grayscale should have equal R, G, B values
		if gray.R != gray.G || gray.G != gray.B {
			t.Errorf("Grayscale(%v) = %v, not grayscale", tt.rgb, gray)
		}
	}
}

func TestInvert(t *testing.T) {
	tests := []struct {
		rgb  RGB
		want RGB
	}{
		{RGB{0, 0, 0}, RGB{255, 255, 255}},
		{RGB{255, 255, 255}, RGB{0, 0, 0}},
		{RGB{128, 128, 128}, RGB{127, 127, 127}},
		{RGB{255, 0, 128}, RGB{0, 255, 127}},
	}

	for _, tt := range tests {
		got := Invert(tt.rgb)
		if !colorEqual(got, tt.want, 1) {
			t.Errorf("Invert(%v) = %v, want %v", tt.rgb, got, tt.want)
		}
	}
}

func TestIsLightIsDark(t *testing.T) {
	lightColors := []RGB{
		{255, 255, 255},
		{255, 255, 200},
		{200, 200, 200},
	}

	darkColors := []RGB{
		{0, 0, 0},
		{50, 50, 50},
		{0, 0, 100},
	}

	for _, c := range lightColors {
		if !IsLight(c) {
			t.Errorf("IsLight(%v) = false, want true", c)
		}
		if IsDark(c) {
			t.Errorf("IsDark(%v) = true, want false", c)
		}
	}

	for _, c := range darkColors {
		if IsLight(c) {
			t.Errorf("IsLight(%v) = true, want false", c)
		}
		if !IsDark(c) {
			t.Errorf("IsDark(%v) = false, want true", c)
		}
	}
}

func TestContrastRatio(t *testing.T) {
	// Black vs White should be 21:1
	ratio := ContrastRatio(RGB{0, 0, 0}, RGB{255, 255, 255})
	if ratio < 20.9 || ratio > 21.1 {
		t.Errorf("ContrastRatio(black, white) = %.2f, want ~21", ratio)
	}

	// Same color should be 1:1
	ratio = ContrastRatio(RGB{128, 128, 128}, RGB{128, 128, 128})
	if ratio < 0.9 || ratio > 1.1 {
		t.Errorf("ContrastRatio(same, same) = %.2f, want ~1", ratio)
	}
}

// --- Named Colors Tests ---

func TestNameToRGB(t *testing.T) {
	tests := []struct {
		name    string
		want    RGB
		wantOk  bool
	}{
		{"red", RGB{255, 0, 0}, true},
		{"blue", RGB{0, 0, 255}, true},
		{"green", RGB{0, 128, 0}, true},
		{"white", RGB{255, 255, 255}, true},
		{"black", RGB{0, 0, 0}, true},
		{"RED", RGB{255, 0, 0}, true},  // Case insensitive
		{" Red ", RGB{255, 0, 0}, true}, // Trims whitespace
		{"notacolor", RGB{}, false},
	}

	for _, tt := range tests {
		got, ok := NameToRGB(tt.name)
		if ok != tt.wantOk {
			t.Errorf("NameToRGB(%q) ok = %v, want %v", tt.name, ok, tt.wantOk)
		}
		if ok && got != tt.want {
			t.Errorf("NameToRGB(%q) = %v, want %v", tt.name, got, tt.want)
		}
	}
}

func TestRGBToName(t *testing.T) {
	// Exact matches
	tests := []struct {
		rgb  RGB
		want string
	}{
		{RGB{255, 0, 0}, "red"},
		{RGB{0, 0, 255}, "blue"},
		{RGB{255, 255, 255}, "white"},
		{RGB{0, 0, 0}, "black"},
	}

	for _, tt := range tests {
		got := RGBToName(tt.rgb)
		if got != tt.want {
			t.Errorf("RGBToName(%v) = %q, want %q", tt.rgb, got, tt.want)
		}
	}

	// Close colors should return closest match
	closeToRed := RGB{254, 1, 1}
	name := RGBToName(closeToRed)
	if name != "red" {
		t.Errorf("RGBToName(%v) = %q, want %q", closeToRed, name, "red")
	}
}

// --- Palette Tests ---

func TestGenerateScheme(t *testing.T) {
	red := RGB{255, 0, 0}

	// Complementary should return 2 colors
	comp := GenerateScheme(red, Complementary_)
	if len(comp) != 2 {
		t.Errorf("Complementary scheme should have 2 colors, got %d", len(comp))
	}

	// Triadic should return 3 colors
	triadic := GenerateScheme(red, Triadic)
	if len(triadic) != 3 {
		t.Errorf("Triadic scheme should have 3 colors, got %d", len(triadic))
	}

	// Tetradic should return 4 colors
	tetradic := GenerateScheme(red, Tetradic)
	if len(tetradic) != 4 {
		t.Errorf("Tetradic scheme should have 4 colors, got %d", len(tetradic))
	}
}

func TestGradient(t *testing.T) {
	start := RGB{0, 0, 0}
	end := RGB{255, 255, 255}

	gradient := Gradient(start, end, 5)
	if len(gradient) != 5 {
		t.Errorf("Gradient should have 5 colors, got %d", len(gradient))
	}

	// First color should be start
	if gradient[0] != start {
		t.Errorf("Gradient[0] = %v, want %v", gradient[0], start)
	}

	// Last color should be end
	if gradient[4] != end {
		t.Errorf("Gradient[4] = %v, want %v", gradient[4], end)
	}

	// Middle should be gray
	middle := gradient[2]
	if middle.R < 125 || middle.R > 130 || middle.G < 125 || middle.G > 130 || middle.B < 125 || middle.B > 130 {
		t.Errorf("Gradient[2] = %v, want approximately (128, 128, 128)", middle)
	}
}

func TestShades(t *testing.T) {
	rgb := RGB{255, 0, 0}
	shades := Shades(rgb, 5)

	if len(shades) != 5 {
		t.Errorf("Shades should have 5 colors, got %d", len(shades))
	}

	// First should be black (or very dark)
	if shades[0].R > 10 || shades[0].G > 10 || shades[0].B > 10 {
		t.Errorf("Shades[0] should be black, got %v", shades[0])
	}

	// Last should be white (or very light)
	if shades[4].R < 245 || shades[4].G < 245 || shades[4].B < 245 {
		t.Errorf("Shades[4] should be white, got %v", shades[4])
	}
}

// --- Helper Functions ---

func colorEqual(c1, c2 RGB, tolerance int) bool {
	return math.Abs(float64(c1.R)-float64(c2.R)) <= float64(tolerance) &&
		math.Abs(float64(c1.G)-float64(c2.G)) <= float64(tolerance) &&
		math.Abs(float64(c1.B)-float64(c2.B)) <= float64(tolerance)
}

// --- Benchmark Tests ---

func BenchmarkRGBToHSL(b *testing.B) {
	rgb := RGB{255, 128, 64}
	for i := 0; i < b.N; i++ {
		RGBToHSL(rgb)
	}
}

func BenchmarkHSLToRGB(b *testing.B) {
	hsl := HSL{180, 50, 75}
	for i := 0; i < b.N; i++ {
		HSLToRGB(hsl)
	}
}

func BenchmarkHexToRGB(b *testing.B) {
	for i := 0; i < b.N; i++ {
		HexToRGB("#ff8040")
	}
}

func BenchmarkRGBToHex(b *testing.B) {
	rgb := RGB{255, 128, 64}
	for i := 0; i < b.N; i++ {
		RGBToHex(rgb)
	}
}

func BenchmarkMix(b *testing.B) {
	c1 := RGB{255, 0, 0}
	c2 := RGB{0, 0, 255}
	for i := 0; i < b.N; i++ {
		Mix(c1, c2, 0.5)
	}
}

func BenchmarkGrayscale(b *testing.B) {
	rgb := RGB{255, 128, 64}
	for i := 0; i < b.N; i++ {
		Grayscale(rgb)
	}
}

func BenchmarkContrastRatio(b *testing.B) {
	c1 := RGB{0, 0, 0}
	c2 := RGB{255, 255, 255}
	for i := 0; i < b.N; i++ {
		ContrastRatio(c1, c2)
	}
}