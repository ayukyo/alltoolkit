package color_utils

import "math"

// ColorScheme represents a color harmony/scheme
type ColorScheme int

const (
	Mono      ColorScheme = iota // Monochromatic
	Complementary_                // Complementary (2 colors)
	Analogous                     // Analogous (3 colors)
	Triadic                       // Triadic (3 colors)
	SplitComp                     // Split-complementary (3 colors)
	Tetradic                      // Tetradic/Square (4 colors)
)

// Palette represents a color palette
type Palette struct {
	Name   string
	Colors []RGB
}

// GenerateScheme generates colors based on a color harmony
func GenerateScheme(base RGB, scheme ColorScheme) []RGB {
	hsl := RGBToHSL(base)

	switch scheme {
	case Mono:
		return generateMonochromatic(hsl)
	case Complementary_:
		return generateComplementary(base)
	case Analogous:
		return generateAnalogous(hsl)
	case Triadic:
		return generateTriadic(hsl)
	case SplitComp:
		return generateSplitComplementary(hsl)
	case Tetradic:
		return generateTetradic(hsl)
	default:
		return []RGB{base}
	}
}

// generateMonochromatic creates a monochromatic palette
func generateMonochromatic(hsl HSL) []RGB {
	return []RGB{
		HSLToRGB(HSL{H: hsl.H, S: hsl.S, L: clamp(hsl.L-20, 0, 100)}),
		HSLToRGB(HSL{H: hsl.H, S: hsl.S, L: clamp(hsl.L-10, 0, 100)}),
		HSLToRGB(hsl),
		HSLToRGB(HSL{H: hsl.H, S: hsl.S, L: clamp(hsl.L+10, 0, 100)}),
		HSLToRGB(HSL{H: hsl.H, S: hsl.S, L: clamp(hsl.L+20, 0, 100)}),
	}
}

// generateComplementary creates a complementary color pair
func generateComplementary(base RGB) []RGB {
	hsl := RGBToHSL(base)
	return []RGB{
		base,
		HSLToRGB(HSL{H: math.Mod(hsl.H+180, 360), S: hsl.S, L: hsl.L}),
	}
}

// generateAnalogous creates an analogous color scheme
func generateAnalogous(hsl HSL) []RGB {
	return []RGB{
		HSLToRGB(HSL{H: math.Mod(hsl.H-30+360, 360), S: hsl.S, L: hsl.L}),
		HSLToRGB(hsl),
		HSLToRGB(HSL{H: math.Mod(hsl.H+30, 360), S: hsl.S, L: hsl.L}),
	}
}

// generateTriadic creates a triadic color scheme
func generateTriadic(hsl HSL) []RGB {
	return []RGB{
		HSLToRGB(hsl),
		HSLToRGB(HSL{H: math.Mod(hsl.H+120, 360), S: hsl.S, L: hsl.L}),
		HSLToRGB(HSL{H: math.Mod(hsl.H+240, 360), S: hsl.S, L: hsl.L}),
	}
}

// generateSplitComplementary creates a split-complementary scheme
func generateSplitComplementary(hsl HSL) []RGB {
	return []RGB{
		HSLToRGB(hsl),
		HSLToRGB(HSL{H: math.Mod(hsl.H+150, 360), S: hsl.S, L: hsl.L}),
		HSLToRGB(HSL{H: math.Mod(hsl.H+210, 360), S: hsl.S, L: hsl.L}),
	}
}

// generateTetradic creates a tetradic/square color scheme
func generateTetradic(hsl HSL) []RGB {
	return []RGB{
		HSLToRGB(hsl),
		HSLToRGB(HSL{H: math.Mod(hsl.H+90, 360), S: hsl.S, L: hsl.L}),
		HSLToRGB(HSL{H: math.Mod(hsl.H+180, 360), S: hsl.S, L: hsl.L}),
		HSLToRGB(HSL{H: math.Mod(hsl.H+270, 360), S: hsl.S, L: hsl.L}),
	}
}

// RandomPalette generates a random harmonious palette
func RandomPalette(count int) []RGB {
	if count < 2 {
		count = 2
	}
	if count > 10 {
		count = 10
	}

	// Generate a random base color
	h := randomFloat(0, 360)
	s := randomFloat(40, 80)
	l := randomFloat(40, 60)

	base := HSLToRGB(HSL{H: h, S: s, L: l})
	hsl := RGBToHSL(base)

	palette := []RGB{base}

	for i := 1; i < count; i++ {
		offset := float64(i) * (360.0 / float64(count))
		newH := math.Mod(hsl.H+offset, 360)
		newS := clamp(hsl.S+randomFloat(-10, 10), 30, 90)
		newL := clamp(hsl.L+randomFloat(-10, 10), 30, 70)

		palette = append(palette, HSLToRGB(HSL{
			H: newH,
			S: newS,
			L: newL,
		}))
	}

	return palette
}

// Gradient generates a gradient between two colors
func Gradient(start, end RGB, steps int) []RGB {
	if steps < 2 {
		steps = 2
	}

	gradient := make([]RGB, steps)
	for i := 0; i < steps; i++ {
		t := float64(i) / float64(steps-1)
		gradient[i] = Mix(start, end, t)
	}
	return gradient
}

// MultiGradient generates a gradient through multiple colors
func MultiGradient(colors []RGB, totalSteps int) []RGB {
	if len(colors) < 2 {
		return colors
	}
	if totalSteps < len(colors) {
		totalSteps = len(colors)
	}

	stepsPerSegment := totalSteps / (len(colors) - 1)
	remainder := totalSteps % (len(colors) - 1)

	var gradient []RGB
	for i := 0; i < len(colors)-1; i++ {
		steps := stepsPerSegment
		if i < remainder {
			steps++
		}

		segment := Gradient(colors[i], colors[i+1], steps+1)
		if i > 0 {
			segment = segment[1:] // Avoid duplicates
		}
		gradient = append(gradient, segment...)
	}

	return gradient
}

// Shades generates lighter and darker shades of a color
func Shades(rgb RGB, count int) []RGB {
	if count < 1 {
		count = 1
	}

	shades := make([]RGB, count)
	hsl := RGBToHSL(rgb)

	for i := 0; i < count; i++ {
		l := float64(i) / float64(count-1) * 100
		shades[i] = HSLToRGB(HSL{H: hsl.H, S: hsl.S, L: l})
	}

	return shades
}

// Tints generates tints of a color (mixed with white)
func Tints(rgb RGB, count int) []RGB {
	if count < 1 {
		count = 1
	}

	white := RGB{R: 255, G: 255, B: 255}
	tints := make([]RGB, count)

	for i := 0; i < count; i++ {
		t := float64(i) / float64(count - 1)
		tints[i] = Mix(rgb, white, t)
	}

	return tints
}

// Tones generates tones of a color (mixed with gray)
func Tones(rgb RGB, count int) []RGB {
	if count < 1 {
		count = 1
	}

	gray := Grayscale(rgb)
	tones := make([]RGB, count)

	for i := 0; i < count; i++ {
		t := float64(i) / float64(count - 1)
		tones[i] = Mix(rgb, gray, t)
	}

	return tones
}

// Warm generates a warm color palette
func Warm(count int) []RGB {
	return PaletteFromRange(0, 60, count)
}

// Cool generates a cool color palette
func Cool(count int) []RGB {
	return PaletteFromRange(180, 270, count)
}

// PaletteFromRange generates colors within a hue range
func PaletteFromRange(hueStart, hueEnd float64, count int) []RGB {
	if count < 1 {
		count = 1
	}

	palette := make([]RGB, count)
	hueRange := hueEnd - hueStart

	for i := 0; i < count; i++ {
		h := hueStart + (hueRange * float64(i) / float64(count-1))
		s := randomFloat(50, 80)
		l := randomFloat(40, 60)
		palette[i] = HSLToRGB(HSL{H: h, S: s, L: l})
	}

	return palette
}

// Helper for random float generation
func randomFloat(min, max float64) float64 {
	// Simple deterministic "random" based on counter
	// In production, use crypto/rand or math/rand
	return min + (max-min)*0.5
}