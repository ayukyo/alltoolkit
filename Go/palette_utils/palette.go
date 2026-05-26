// Package palette provides color palette generation utilities.
// Generates harmonious color palettes from base colors using various color theory rules.
package palette

import (
	"fmt"
	"math"
	"sort"
)

// Color represents an RGB color with optional name.
type Color struct {
	R    uint8  // Red component (0-255)
	G    uint8  // Green component (0-255)
	B    uint8  // Blue component (0-255)
	Name string // Optional color name
}

// Palette represents a collection of colors with a name.
type Palette struct {
	Name   string  // Palette name
	Colors []Color // Colors in the palette
}

// RGB creates a new Color from RGB values.
func RGB(r, g, b uint8) Color {
	return Color{R: r, G: g, B: b}
}

// Hex creates a Color from a hex string (e.g., "#FF5500" or "FF5500").
func Hex(hex string) (Color, error) {
	if len(hex) == 0 {
		return Color{}, fmt.Errorf("empty hex string")
	}
	
	// Remove leading #
	if hex[0] == '#' {
		hex = hex[1:]
	}
	
	if len(hex) != 6 && len(hex) != 3 {
		return Color{}, fmt.Errorf("invalid hex length: %s", hex)
	}
	
	var r, g, b uint8
	if len(hex) == 3 {
		// Short form: #RGB -> #RRGGBB
		r = parseHexDigit(hex[0]) * 17
		g = parseHexDigit(hex[1]) * 17
		b = parseHexDigit(hex[2]) * 17
	} else {
		r = parseHexDigit(hex[0])*16 + parseHexDigit(hex[1])
		g = parseHexDigit(hex[2])*16 + parseHexDigit(hex[3])
		b = parseHexDigit(hex[4])*16 + parseHexDigit(hex[5])
	}
	
	return Color{R: r, G: g, B: b}, nil
}

// MustHex creates a Color from hex string, panics on error.
func MustHex(hex string) Color {
	c, err := Hex(hex)
	if err != nil {
		panic(err)
	}
	return c
}

func parseHexDigit(c byte) uint8 {
	switch {
	case c >= '0' && c <= '9':
		return c - '0'
	case c >= 'a' && c <= 'f':
		return c - 'a' + 10
	case c >= 'A' && c <= 'F':
		return c - 'A' + 10
	default:
		return 0
	}
}

// Hex returns the hex string representation of the color.
func (c Color) Hex() string {
	return fmt.Sprintf("#%02X%02X%02X", c.R, c.G, c.B)
}

// RGBString returns the RGB string representation.
func (c Color) RGBString() string {
	return fmt.Sprintf("rgb(%d, %d, %d)", c.R, c.G, c.B)
}

// HSL returns the HSL representation (hue 0-360, saturation 0-1, lightness 0-1).
func (c Color) HSL() (h, s, l float64) {
	r := float64(c.R) / 255
	g := float64(c.G) / 255
	b := float64(c.B) / 255
	
	maxVal := math.Max(math.Max(r, g), b)
	minVal := math.Min(math.Min(r, g), b)
	l = (maxVal + minVal) / 2
	
	if maxVal == minVal {
		return 0, 0, l
	}
	
	d := maxVal - minVal
	s = d / (1 - math.Abs(2*l-1))
	
	switch maxVal {
	case r:
		h = (g - b) / d
		if g < b {
			h += 6
		}
	case g:
		h = (b-r)/d + 2
	case b:
		h = (r-g)/d + 4
	}
	
	h *= 60
	if h < 0 {
		h += 360
	}
	
	return h, s, l
}

// HSV returns the HSV representation (hue 0-360, saturation 0-1, value 0-1).
func (c Color) HSV() (h, s, v float64) {
	r := float64(c.R) / 255
	g := float64(c.G) / 255
	b := float64(c.B) / 255
	
	maxVal := math.Max(math.Max(r, g), b)
	minVal := math.Min(math.Min(r, g), b)
	v = maxVal
	
	if maxVal == minVal {
		return 0, 0, v
	}
	
	d := maxVal - minVal
	s = d / maxVal
	
	switch maxVal {
	case r:
		h = (g - b) / d
		if g < b {
			h += 6
		}
	case g:
		h = (b-r)/d + 2
	case b:
		h = (r-g)/d + 4
	}
	
	h *= 60
	if h < 0 {
		h += 360
	}
	
	return h, s, v
}

// Luminance returns the perceived luminance of the color (0-1).
func (c Color) Luminance() float64 {
	r := float64(c.R) / 255
	g := float64(c.G) / 255
	b := float64(c.B) / 255
	
	// Apply gamma correction
	r = linearize(r)
	g = linearize(g)
	b = linearize(b)
	
	return 0.2126*r + 0.7152*g + 0.0722*b
}

func linearize(c float64) float64 {
	if c <= 0.03928 {
		return c / 12.92
	}
	return math.Pow((c+0.055)/1.055, 2.4)
}

// IsLight returns true if the color is considered light.
func (c Color) IsLight() bool {
	return c.Luminance() > 0.5
}

// IsDark returns true if the color is considered dark.
func (c Color) IsDark() bool {
	return !c.IsLight()
}

// ContrastRatio calculates the contrast ratio between two colors.
func ContrastRatio(c1, c2 Color) float64 {
	l1 := c1.Luminance()
	l2 := c2.Luminance()
	
	lighter := math.Max(l1, l2)
	darker := math.Min(l1, l2)
	
	return (lighter + 0.05) / (darker + 0.05)
}

// WithLuminance creates a new color with adjusted luminance.
func (c Color) WithLuminance(target float64) Color {
	h, s, _ := c.HSL()
	return hslToColor(h, s, target)
}

// Lighten returns a lighter version of the color.
func (c Color) Lighten(amount float64) Color {
	h, s, l := c.HSL()
	l = math.Min(1, l+amount)
	return hslToColor(h, s, l)
}

// Darken returns a darker version of the color.
func (c Color) Darken(amount float64) Color {
	h, s, l := c.HSL()
	l = math.Max(0, l-amount)
	return hslToColor(h, s, l)
}

// Saturate increases the saturation of the color.
func (c Color) Saturate(amount float64) Color {
	h, s, l := c.HSL()
	s = math.Min(1, s+amount)
	return hslToColor(h, s, l)
}

// Desaturate decreases the saturation of the color.
func (c Color) Desaturate(amount float64) Color {
	h, s, l := c.HSL()
	s = math.Max(0, s-amount)
	return hslToColor(h, s, l)
}

// RotateHue rotates the hue by degrees.
func (c Color) RotateHue(degrees float64) Color {
	h, s, l := c.HSL()
	h = math.Mod(h+degrees+360, 360)
	return hslToColor(h, s, l)
}

// Complement returns the complementary color.
func (c Color) Complement() Color {
	return c.RotateHue(180)
}

// Analogous returns analogous colors (adjacent on color wheel).
func (c Color) Analogous() []Color {
	return []Color{
		c.RotateHue(-30),
		c,
		c.RotateHue(30),
	}
}

// Triadic returns triadic colors (evenly spaced on color wheel).
func (c Color) Triadic() []Color {
	return []Color{
		c,
		c.RotateHue(120),
		c.RotateHue(240),
	}
}

// SplitComplementary returns split complementary colors.
func (c Color) SplitComplementary() []Color {
	return []Color{
		c,
		c.RotateHue(150),
		c.RotateHue(210),
	}
}

// Tetradic returns tetradic (double complementary) colors.
func (c Color) Tetradic() []Color {
	return []Color{
		c,
		c.RotateHue(90),
		c.RotateHue(180),
		c.RotateHue(270),
	}
}

// Square returns square color scheme (4 evenly spaced colors).
func (c Color) Square() []Color {
	return c.Tetradic()
}

// Monochromatic generates a monochromatic palette with n colors.
func Monochromatic(base Color, n int) Palette {
	if n < 2 {
		n = 2
	}
	
	h, s, _ := base.HSL()
	colors := make([]Color, n)
	
	step := 1.0 / float64(n-1)
	for i := 0; i < n; i++ {
		lightness := step * float64(i)
		colors[i] = hslToColor(h, s, lightness)
		colors[i].Name = fmt.Sprintf("Shade %d", i+1)
	}
	
	return Palette{
		Name:   "Monochromatic",
		Colors: colors,
	}
}

// Shades generates n shades of a color (varying lightness).
func Shades(base Color, n int) Palette {
	return Monochromatic(base, n)
}

// Tints generates n tints of a color (mixing with white).
func Tints(base Color, n int) Palette {
	if n < 2 {
		n = 2
	}
	
	colors := make([]Color, n)
	step := 1.0 / float64(n-1)
	
	for i := 0; i < n; i++ {
		ratio := step * float64(i)
		colors[i] = blendColors(base, Color{R: 255, G: 255, B: 255}, ratio)
		colors[i].Name = fmt.Sprintf("Tint %d", i+1)
	}
	
	return Palette{
		Name:   "Tints",
		Colors: colors,
	}
}

// Tones generates n tones of a color (mixing with gray).
func Tones(base Color, n int) Palette {
	if n < 2 {
		n = 2
	}
	
	gray := Color{R: 128, G: 128, B: 128}
	colors := make([]Color, n)
	step := 1.0 / float64(n-1)
	
	for i := 0; i < n; i++ {
		ratio := step * float64(i)
		colors[i] = blendColors(base, gray, ratio)
		colors[i].Name = fmt.Sprintf("Tone %d", i+1)
	}
	
	return Palette{
		Name:   "Tones",
		Colors: colors,
	}
}

// Blend returns a blend of two colors (0 = c1, 1 = c2).
func Blend(c1, c2 Color, ratio float64) Color {
	return blendColors(c1, c2, ratio)
}

func blendColors(c1, c2 Color, ratio float64) Color {
	ratio = math.Max(0, math.Min(1, ratio))
	
	return Color{
		R: uint8(float64(c1.R)*(1-ratio) + float64(c2.R)*ratio),
		G: uint8(float64(c1.G)*(1-ratio) + float64(c2.G)*ratio),
		B: uint8(float64(c1.B)*(1-ratio) + float64(c2.B)*ratio),
	}
}

// Gradient generates a gradient palette between two colors.
func Gradient(start, end Color, steps int) Palette {
	if steps < 2 {
		steps = 2
	}
	
	colors := make([]Color, steps)
	step := 1.0 / float64(steps-1)
	
	for i := 0; i < steps; i++ {
		ratio := step * float64(i)
		colors[i] = blendColors(start, end, ratio)
		colors[i].Name = fmt.Sprintf("Step %d", i+1)
	}
	
	return Palette{
		Name:   "Gradient",
		Colors: colors,
	}
}

// MultiGradient generates a gradient through multiple colors.
func MultiGradient(colors []Color, steps int) Palette {
	if len(colors) < 2 {
		return Palette{Colors: colors}
	}
	if steps < len(colors) {
		steps = len(colors)
	}
	
	result := make([]Color, steps)
	segments := len(colors) - 1
	stepsPerSegment := float64(steps-1) / float64(segments)
	
	for i := 0; i < steps; i++ {
		segment := float64(i) / stepsPerSegment
		segIndex := int(segment)
		
		if segIndex >= segments {
			result[i] = colors[len(colors)-1]
			continue
		}
		
		ratio := segment - float64(segIndex)
		result[i] = blendColors(colors[segIndex], colors[segIndex+1], ratio)
	}
	
	return Palette{
		Name:   "MultiGradient",
		Colors: result,
	}
}

// Complementary generates a complementary palette.
func Complementary(base Color) Palette {
	return Palette{
		Name: "Complementary",
		Colors: []Color{
			{Name: "Primary", R: base.R, G: base.G, B: base.B},
			{Name: "Complement", R: base.Complement().R, G: base.Complement().G, B: base.Complement().B},
		},
	}
}

// Analogous generates an analogous palette.
func Analogous(base Color) Palette {
	colors := base.Analogous()
	return Palette{
		Name: "Analogous",
		Colors: []Color{
			{Name: "Cool", R: colors[0].R, G: colors[0].G, B: colors[0].B},
			{Name: "Base", R: colors[1].R, G: colors[1].G, B: colors[1].B},
			{Name: "Warm", R: colors[2].R, G: colors[2].G, B: colors[2].B},
		},
	}
}

// Triadic generates a triadic palette.
func Triadic(base Color) Palette {
	colors := base.Triadic()
	return Palette{
		Name: "Triadic",
		Colors: []Color{
			{Name: "Color 1", R: colors[0].R, G: colors[0].G, B: colors[0].B},
			{Name: "Color 2", R: colors[1].R, G: colors[1].G, B: colors[1].B},
			{Name: "Color 3", R: colors[2].R, G: colors[2].G, B: colors[2].B},
		},
	}
}

// SplitComplementary generates a split complementary palette.
func SplitComplementary(base Color) Palette {
	colors := base.SplitComplementary()
	return Palette{
		Name: "SplitComplementary",
		Colors: []Color{
			{Name: "Base", R: colors[0].R, G: colors[0].G, B: colors[0].B},
			{Name: "Split 1", R: colors[1].R, G: colors[1].G, B: colors[1].B},
			{Name: "Split 2", R: colors[2].R, G: colors[2].G, B: colors[2].B},
		},
	}
}

// Tetradic generates a tetradic palette.
func Tetradic(base Color) Palette {
	colors := base.Tetradic()
	return Palette{
		Name: "Tetradic",
		Colors: []Color{
			{Name: "Color 1", R: colors[0].R, G: colors[0].G, B: colors[0].B},
			{Name: "Color 2", R: colors[1].R, G: colors[1].G, B: colors[1].B},
			{Name: "Color 3", R: colors[2].R, G: colors[2].G, B: colors[2].B},
			{Name: "Color 4", R: colors[3].R, G: colors[3].G, B: colors[3].B},
		},
	}
}

// Compound is an alias for Tetradic.
func Compound(base Color) Palette {
	return Tetradic(base)
}

// Harmony generates a complete harmonious palette with multiple variations.
func Harmony(base Color) Palette {
	comp := base.Complement()
	
	return Palette{
		Name: "Harmony",
		Colors: []Color{
			{Name: "Base", R: base.R, G: base.G, B: base.B},
			{Name: "Light", R: base.Lighten(0.2).R, G: base.Lighten(0.2).G, B: base.Lighten(0.2).B},
			{Name: "Dark", R: base.Darken(0.2).R, G: base.Darken(0.2).G, B: base.Darken(0.2).B},
			{Name: "Complement", R: comp.R, G: comp.G, B: comp.B},
			{Name: "Comp Light", R: comp.Lighten(0.2).R, G: comp.Lighten(0.2).G, B: comp.Lighten(0.2).B},
			{Name: "Comp Dark", R: comp.Darken(0.2).R, G: comp.Darken(0.2).G, B: comp.Darken(0.2).B},
		},
	}
}

// WCAGAA checks if two colors meet WCAG AA contrast requirements.
func WCAGAA(fg, bg Color) (passes bool, ratio float64) {
	ratio = ContrastRatio(fg, bg)
	return ratio >= 4.5, ratio
}

// WCAGAAA checks if two colors meet WCAG AAA contrast requirements.
func WCAGAAA(fg, bg Color) (passes bool, ratio float64) {
	ratio = ContrastRatio(fg, bg)
	return ratio >= 7, ratio
}

// WCAGAALarge checks if two colors meet WCAG AA large text requirements.
func WCAGAALarge(fg, bg Color) (passes bool, ratio float64) {
	ratio = ContrastRatio(fg, bg)
	return ratio >= 3, ratio
}

// SuggestTextColor suggests a text color (black or white) for a given background.
func SuggestTextColor(bg Color) Color {
	if bg.IsLight() {
		return Color{R: 0, G: 0, B: 0, Name: "Black"}
	}
	return Color{R: 255, G: 255, B: 255, Name: "White"}
}

// ColorDistance calculates the perceptual distance between two colors.
func ColorDistance(c1, c2 Color) float64 {
	// Using weighted Euclidean distance for perceptual uniformity
	dr := float64(c1.R) - float64(c2.R)
	dg := float64(c1.G) - float64(c2.G)
	db := float64(c1.B) - float64(c2.B)
	
	// Weighted for human perception
	return math.Sqrt(0.299*dr*dr + 0.587*dg*dg + 0.114*db*db)
}

// SortByHue sorts colors by hue.
func SortByHue(colors []Color) {
	sort.Slice(colors, func(i, j int) bool {
		h1, _, _ := colors[i].HSL()
		h2, _, _ := colors[j].HSL()
		return h1 < h2
	})
}

// SortByLuminance sorts colors by luminance (light to dark).
func SortByLuminance(colors []Color) {
	sort.Slice(colors, func(i, j int) bool {
		return colors[i].Luminance() > colors[j].Luminance()
	})
}

// SortBySaturation sorts colors by saturation (high to low).
func SortBySaturation(colors []Color) {
	sort.Slice(colors, func(i, j int) bool {
		_, s1, _ := colors[i].HSL()
		_, s2, _ := colors[j].HSL()
		return s1 > s2
	})
}

// Random generates a random color.
func Random() Color {
	return Color{
		R: uint8(randInt(256)),
		G: uint8(randInt(256)),
		B: uint8(randInt(256)),
	}
}

// RandomWithHue generates a random color with a specific hue.
func RandomWithHue(hue float64) Color {
	s := randFloat(0.5, 1.0)
	l := randFloat(0.3, 0.7)
	return hslToColor(hue, s, l)
}

// RandomPastel generates a random pastel color.
func RandomPastel() Color {
	h := randFloat(0, 360)
	s := randFloat(0.3, 0.6)
	l := randFloat(0.7, 0.9)
	return hslToColor(h, s, l)
}

// RandomVibrant generates a random vibrant color.
func RandomVibrant() Color {
	h := randFloat(0, 360)
	s := randFloat(0.8, 1.0)
	l := randFloat(0.4, 0.6)
	return hslToColor(h, s, l)
}

// hslToColor converts HSL to Color.
func hslToColor(h, s, l float64) Color {
	if s == 0 {
		v := uint8(l * 255)
		return Color{R: v, G: v, B: v}
	}
	
	var r, g, b float64
	
	h = h / 360
	
	var q float64
	if l < 0.5 {
		q = l * (1 + s)
	} else {
		q = l + s - l*s
	}
	
	p := 2*l - q
	
	r = hueToRGB(p, q, h+1.0/3.0)
	g = hueToRGB(p, q, h)
	b = hueToRGB(p, q, h-1.0/3.0)
	
	return Color{
		R: uint8(math.Round(r * 255)),
		G: uint8(math.Round(g * 255)),
		B: uint8(math.Round(b * 255)),
	}
}

func hueToRGB(p, q, t float64) float64 {
	if t < 0 {
		t++
	}
	if t > 1 {
		t--
	}
	if t < 1.0/6.0 {
		return p + (q-p)*6*t
	}
	if t < 1.0/2.0 {
		return q
	}
	if t < 2.0/3.0 {
		return p + (q-p)*(2.0/3.0-t)*6
	}
	return p
}

// Simple random helpers (no external dependencies)
var seed = uint64(1)

func randInt(max int) int {
	seed = seed*6364136223846793005 + 1442695040888963407
	return int((seed >> 33) % uint64(max))
}

func randFloat(min, max float64) float64 {
	return min + float64(randInt(1000000))/1000000.0*(max-min)
}

// SetRandomSeed sets the seed for random color generation.
func SetRandomSeed(s uint64) {
	seed = s
}