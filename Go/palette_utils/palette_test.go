package palette

import (
	"math"
	"testing"
)

func TestRGB(t *testing.T) {
	c := RGB(255, 128, 0)
	if c.R != 255 || c.G != 128 || c.B != 0 {
		t.Errorf("RGB(255, 128, 0) = %v, want {R:255, G:128, B:0}", c)
	}
}

func TestHex(t *testing.T) {
	tests := []struct {
		hex   string
		r, g, b uint8
		err   bool
	}{
		{"#FF8000", 255, 128, 0, false},
		{"FF8000", 255, 128, 0, false},
		{"#f80", 255, 136, 0, false},
		{"f80", 255, 136, 0, false},
		{"", 0, 0, 0, true},
		{"#GGGGGG", 0, 0, 0, false}, // Invalid hex digits become 0
	}
	
	for _, tt := range tests {
		c, err := Hex(tt.hex)
		if tt.err && err == nil {
			t.Errorf("Hex(%q) expected error", tt.hex)
		}
		if !tt.err && err != nil {
			t.Errorf("Hex(%q) unexpected error: %v", tt.hex, err)
		}
		if !tt.err && (c.R != tt.r || c.G != tt.g || c.B != tt.b) {
			t.Errorf("Hex(%q) = %v, want {R:%d, G:%d, B:%d}", tt.hex, c, tt.r, tt.g, tt.b)
		}
	}
}

func TestMustHex(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("MustHex with invalid hex should panic")
		}
	}()
	MustHex("invalid")
}

func TestColorHex(t *testing.T) {
	c := RGB(255, 128, 0)
	if c.Hex() != "#FF8000" {
		t.Errorf("Color.Hex() = %s, want #FF8000", c.Hex())
	}
}

func TestColorRGBString(t *testing.T) {
	c := RGB(255, 128, 0)
	if c.RGBString() != "rgb(255, 128, 0)" {
		t.Errorf("Color.RGBString() = %s, want rgb(255, 128, 0)", c.RGBString())
	}
}

func TestColorHSL(t *testing.T) {
	tests := []struct {
		r, g, b uint8
		h        float64
	}{
		{255, 0, 0, 0},     // Red
		{0, 255, 0, 120},   // Green
		{0, 0, 255, 240},   // Blue
		{255, 255, 255, 0}, // White
		{0, 0, 0, 0},       // Black
		{128, 128, 128, 0}, // Gray
	}
	
	for _, tt := range tests {
		c := RGB(tt.r, tt.g, tt.b)
		h, s, l := c.HSL()
		
		// For achromatic colors, saturation should be 0
		if tt.r == tt.g && tt.g == tt.b {
			if s != 0 {
				t.Errorf("HSL(%d, %d, %d) saturation = %f, want 0", tt.r, tt.g, tt.b, s)
			}
		} else {
			// Allow some tolerance for hue
			if math.Abs(h-tt.h) > 1 && math.Abs(h-tt.h-360) > 1 {
				t.Errorf("HSL(%d, %d, %d) hue = %f, want %f", tt.r, tt.g, tt.b, h, tt.h)
			}
		}
		
		// Luminance should be between 0 and 1
		if l < 0 || l > 1 {
			t.Errorf("HSL luminance = %f, want 0 <= l <= 1", l)
		}
	}
}

func TestColorHSV(t *testing.T) {
	c := RGB(255, 0, 0)
	h, s, v := c.HSV()
	
	if math.Abs(h-0) > 1 && math.Abs(h-360) > 1 {
		t.Errorf("HSV red hue = %f, want 0 or 360", h)
	}
	if math.Abs(s-1) > 0.01 {
		t.Errorf("HSV red saturation = %f, want 1", s)
	}
	if math.Abs(v-1) > 0.01 {
		t.Errorf("HSV red value = %f, want 1", v)
	}
}

func TestColorLuminance(t *testing.T) {
	tests := []struct {
		r, g, b uint8
		light   bool
	}{
		{255, 255, 255, true},  // White
		{0, 0, 0, false},       // Black
		{255, 255, 0, true},    // Yellow
		{0, 0, 255, false},     // Blue
		{200, 200, 200, true},  // Light gray
		{50, 50, 50, false},    // Dark gray
	}
	
	for _, tt := range tests {
		c := RGB(tt.r, tt.g, tt.b)
		if c.IsLight() != tt.light {
			t.Errorf("RGB(%d, %d, %d).IsLight() = %v, want %v", tt.r, tt.g, tt.b, c.IsLight(), tt.light)
		}
	}
}

func TestContrastRatio(t *testing.T) {
	// White vs Black should have maximum contrast (21:1)
	white := RGB(255, 255, 255)
	black := RGB(0, 0, 0)
	
	ratio := ContrastRatio(white, black)
	if math.Abs(ratio-21) > 0.1 {
		t.Errorf("ContrastRatio(white, black) = %f, want ~21", ratio)
	}
	
	// Same color should have minimum contrast (1:1)
	ratio = ContrastRatio(white, white)
	if math.Abs(ratio-1) > 0.01 {
		t.Errorf("ContrastRatio(white, white) = %f, want 1", ratio)
	}
}

func TestLightenDarken(t *testing.T) {
	c := RGB(100, 100, 100)
	_, _, l1 := c.HSL()
	
	light := c.Lighten(0.3)
	_, _, l2 := light.HSL()
	
	if l2 <= l1 {
		t.Error("Lightened color should have higher lightness")
	}
	
	dark := c.Darken(0.3)
	_, _, l3 := dark.HSL()
	
	if l3 >= l1 {
		t.Error("Darkened color should have lower lightness")
	}
}

func TestSaturateDesaturate(t *testing.T) {
	c := RGB(255, 0, 0)
	_, s1, _ := c.HSL()
	
	saturated := c.Saturate(0.1)
	_, s2, _ := saturated.HSL()
	
	if s2 < s1 {
		t.Error("Saturated color should have higher saturation")
	}
	
	desaturated := c.Desaturate(0.5)
	_, s3, _ := desaturated.HSL()
	
	if s3 > s1 {
		t.Error("Desaturated color should have lower saturation")
	}
}

func TestRotateHue(t *testing.T) {
	red := RGB(255, 0, 0)
	
	// Rotate 120 degrees should give green-ish
	green := red.RotateHue(120)
	h, _, _ := green.HSL()
	if math.Abs(h-120) > 1 {
		t.Errorf("RotateHue(120) hue = %f, want 120", h)
	}
	
	// Rotate 180 degrees should give cyan
	cyan := red.RotateHue(180)
	h, _, _ = cyan.HSL()
	if math.Abs(h-180) > 1 {
		t.Errorf("RotateHue(180) hue = %f, want 180", h)
	}
}

func TestComplement(t *testing.T) {
	red := RGB(255, 0, 0)
	cyan := red.Complement()
	
	h, _, _ := cyan.HSL()
	if math.Abs(h-180) > 1 {
		t.Errorf("Complement hue = %f, want 180", h)
	}
}

func TestAnalogous(t *testing.T) {
	red := RGB(255, 0, 0)
	colors := red.Analogous()
	
	if len(colors) != 3 {
		t.Errorf("Analogous() returned %d colors, want 3", len(colors))
	}
}

func TestTriadic(t *testing.T) {
	red := RGB(255, 0, 0)
	colors := red.Triadic()
	
	if len(colors) != 3 {
		t.Errorf("Triadic() returned %d colors, want 3", len(colors))
	}
	
	for i, c := range colors {
		h, _, _ := c.HSL()
		expected := float64(i * 120)
		if math.Abs(h-expected) > 1 && math.Abs(h-expected-360) > 1 {
			t.Errorf("Triadic color %d hue = %f, want %f", i, h, expected)
		}
	}
}

func TestMonochromatic(t *testing.T) {
	red := RGB(255, 0, 0)
	palette := Monochromatic(red, 5)
	
	if len(palette.Colors) != 5 {
		t.Errorf("Monochromatic() returned %d colors, want 5", len(palette.Colors))
	}
	
	h, _, _ := red.HSL()
	for _, c := range palette.Colors {
		ch, _, _ := c.HSL()
		if math.Abs(ch-h) > 1 && math.Abs(ch-h-360) > 1 && math.Abs(ch-h+360) > 1 {
			t.Errorf("Monochromatic color hue %f differs from base hue %f", ch, h)
		}
	}
}

func TestShades(t *testing.T) {
	red := RGB(255, 0, 0)
	palette := Shades(red, 5)
	
	if len(palette.Colors) != 5 {
		t.Errorf("Shades() returned %d colors, want 5", len(palette.Colors))
	}
}

func TestTints(t *testing.T) {
	red := RGB(255, 0, 0)
	palette := Tints(red, 5)
	
	if len(palette.Colors) != 5 {
		t.Errorf("Tints() returned %d colors, want 5", len(palette.Colors))
	}
	
	// Last tint should be close to white
	last := palette.Colors[len(palette.Colors)-1]
	if last.R < 250 || last.G < 250 || last.B < 250 {
		t.Errorf("Last tint should be close to white, got %v", last)
	}
}

func TestGradient(t *testing.T) {
	red := RGB(255, 0, 0)
	blue := RGB(0, 0, 255)
	palette := Gradient(red, blue, 5)
	
	if len(palette.Colors) != 5 {
		t.Errorf("Gradient() returned %d colors, want 5", len(palette.Colors))
	}
	
	// First color should be red
	if palette.Colors[0].R < 250 {
		t.Error("First gradient color should be close to red")
	}
	
	// Last color should be blue
	if palette.Colors[4].B < 250 {
		t.Error("Last gradient color should be close to blue")
	}
}

func TestBlend(t *testing.T) {
	white := RGB(255, 255, 255)
	black := RGB(0, 0, 0)
	
	// 50% blend should be gray
	gray := Blend(white, black, 0.5)
	if gray.R < 125 || gray.R > 130 {
		t.Errorf("Blend 50%% gray = %d, want ~127", gray.R)
	}
	
	// 0% blend should be first color
	result := Blend(white, black, 0)
	if result.R != 255 {
		t.Errorf("Blend 0%% R = %d, want 255", result.R)
	}
	
	// 100% blend should be second color
	result = Blend(white, black, 1)
	if result.R != 0 {
		t.Errorf("Blend 100%% R = %d, want 0", result.R)
	}
}

func TestComplementaryPalette(t *testing.T) {
	red := RGB(255, 0, 0)
	palette := Complementary(red)
	
	if palette.Name != "Complementary" {
		t.Errorf("Palette name = %s, want Complementary", palette.Name)
	}
	
	if len(palette.Colors) != 2 {
		t.Errorf("Complementary() returned %d colors, want 2", len(palette.Colors))
	}
}

func TestAnalogousPalette(t *testing.T) {
	red := RGB(255, 0, 0)
	palette := Analogous(red)
	
	if len(palette.Colors) != 3 {
		t.Errorf("Analogous() returned %d colors, want 3", len(palette.Colors))
	}
}

func TestTriadicPalette(t *testing.T) {
	red := RGB(255, 0, 0)
	palette := Triadic(red)
	
	if len(palette.Colors) != 3 {
		t.Errorf("Triadic() returned %d colors, want 3", len(palette.Colors))
	}
}

func TestSplitComplementaryPalette(t *testing.T) {
	red := RGB(255, 0, 0)
	palette := SplitComplementary(red)
	
	if len(palette.Colors) != 3 {
		t.Errorf("SplitComplementary() returned %d colors, want 3", len(palette.Colors))
	}
}

func TestTetradicPalette(t *testing.T) {
	red := RGB(255, 0, 0)
	palette := Tetradic(red)
	
	if len(palette.Colors) != 4 {
		t.Errorf("Tetradic() returned %d colors, want 4", len(palette.Colors))
	}
}

func TestHarmonyPalette(t *testing.T) {
	red := RGB(255, 0, 0)
	palette := Harmony(red)
	
	if len(palette.Colors) != 6 {
		t.Errorf("Harmony() returned %d colors, want 6", len(palette.Colors))
	}
}

func TestWCAGAA(t *testing.T) {
	white := RGB(255, 255, 255)
	black := RGB(0, 0, 0)
	lightGray := RGB(200, 200, 200)
	
	// White on black should pass
	passes, ratio := WCAGAA(white, black)
	if !passes {
		t.Error("WCAGAA(white, black) should pass")
	}
	if ratio < 20 {
		t.Errorf("WCAGAA ratio = %f, want >= 20", ratio)
	}
	
	// Light gray on white should not pass
	passes, _ = WCAGAA(lightGray, white)
	if passes {
		t.Error("WCAGAA(lightGray, white) should not pass")
	}
}

func TestWCAGAAA(t *testing.T) {
	white := RGB(255, 255, 255)
	black := RGB(0, 0, 0)
	
	passes, ratio := WCAGAAA(white, black)
	if !passes {
		t.Error("WCAGAAA(white, black) should pass")
	}
	if ratio < 20 {
		t.Errorf("WCAGAAA ratio = %f, want >= 20", ratio)
	}
}

func TestSuggestTextColor(t *testing.T) {
	white := RGB(255, 255, 255)
	black := RGB(0, 0, 0)
	
	// White background should suggest black text
	text := SuggestTextColor(white)
	if text.R != 0 || text.G != 0 || text.B != 0 {
		t.Errorf("SuggestTextColor(white) = %v, want black", text)
	}
	
	// Black background should suggest white text
	text = SuggestTextColor(black)
	if text.R != 255 || text.G != 255 || text.B != 255 {
		t.Errorf("SuggestTextColor(black) = %v, want white", text)
	}
}

func TestColorDistance(t *testing.T) {
	red := RGB(255, 0, 0)
	darkRed := RGB(200, 0, 0)
	blue := RGB(0, 0, 255)
	
	// Same color distance should be 0
	d := ColorDistance(red, red)
	if d != 0 {
		t.Errorf("ColorDistance(red, red) = %f, want 0", d)
	}
	
	// Red should be closer to dark red than to blue
	d1 := ColorDistance(red, darkRed)
	d2 := ColorDistance(red, blue)
	if d1 >= d2 {
		t.Errorf("ColorDistance(red, darkRed) = %f should be < ColorDistance(red, blue) = %f", d1, d2)
	}
}

func TestSortByHue(t *testing.T) {
	colors := []Color{
		RGB(0, 255, 0),   // Green (hue ~120)
		RGB(255, 0, 0),   // Red (hue 0)
		RGB(0, 0, 255),   // Blue (hue ~240)
	}
	
	SortByHue(colors)
	
	// Should be sorted by hue: Red, Green, Blue
	h1, _, _ := colors[0].HSL()
	h2, _, _ := colors[1].HSL()
	h3, _, _ := colors[2].HSL()
	
	if h1 > h2 || h2 > h3 {
		t.Errorf("SortByHue failed: hues %f, %f, %f not in order", h1, h2, h3)
	}
}

func TestSortByLuminance(t *testing.T) {
	colors := []Color{
		RGB(128, 128, 128), // Gray
		RGB(255, 255, 255), // White
		RGB(0, 0, 0),       // Black
	}
	
	SortByLuminance(colors)
	
	// Should be sorted light to dark
	if colors[0].Luminance() < colors[1].Luminance() || colors[1].Luminance() < colors[2].Luminance() {
		t.Error("SortByLuminance failed: colors not sorted by luminance")
	}
}

func TestRandom(t *testing.T) {
	SetRandomSeed(12345)
	c1 := Random()
	c2 := Random()
	
	// Different seed should produce different colors
	SetRandomSeed(12345)
	c3 := Random()
	
	// Same seed should produce same color
	if c1 != c3 {
		t.Error("Random with same seed should produce same color")
	}
	
	// Different calls should produce different colors
	if c1 == c2 {
		t.Error("Random calls should produce different colors")
	}
}

func TestRandomWithHue(t *testing.T) {
	SetRandomSeed(12345)
	c := RandomWithHue(180) // Cyan
	
	h, _, _ := c.HSL()
	if math.Abs(h-180) > 0.01 {
		t.Errorf("RandomWithHue(180) hue = %f, want 180", h)
	}
}

func TestRandomPastel(t *testing.T) {
	SetRandomSeed(12345)
	c := RandomPastel()
	
	_, s, l := c.HSL()
	
	// Pastels should have low saturation and high lightness
	if s > 0.7 {
		t.Errorf("Pastel saturation = %f, want <= 0.7", s)
	}
	if l < 0.6 {
		t.Errorf("Pastel lightness = %f, want >= 0.6", l)
	}
}

func TestRandomVibrant(t *testing.T) {
	SetRandomSeed(12345)
	c := RandomVibrant()
	
	_, s, l := c.HSL()
	
	// Vibrant colors should have high saturation
	if s < 0.7 {
		t.Errorf("Vibrant saturation = %f, want >= 0.7", s)
	}
	if l < 0.3 || l > 0.7 {
		t.Errorf("Vibrant lightness = %f, want 0.3-0.7", l)
	}
}

func TestMultiGradient(t *testing.T) {
	colors := []Color{
		RGB(255, 0, 0),   // Red
		RGB(0, 255, 0),   // Green
		RGB(0, 0, 255),   // Blue
	}
	
	palette := MultiGradient(colors, 7)
	
	if len(palette.Colors) != 7 {
		t.Errorf("MultiGradient() returned %d colors, want 7", len(palette.Colors))
	}
	
	// First should be red
	if palette.Colors[0].R < 250 {
		t.Error("First color should be close to red")
	}
	
	// Last should be blue
	if palette.Colors[6].B < 250 {
		t.Error("Last color should be close to blue")
	}
}