// Package color_utils provides color conversion and manipulation utilities
// Supports RGB, HEX, HSL, HSV, CMYK color formats with zero external dependencies
package color_utils

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

// RGB represents a color in Red, Green, Blue format
type RGB struct {
	R uint8 // Red component (0-255)
	G uint8 // Green component (0-255)
	B uint8 // Blue component (0-255)
}

// HSL represents a color in Hue, Saturation, Lightness format
type HSL struct {
	H float64 // Hue (0-360)
	S float64 // Saturation (0-100)
	L float64 // Lightness (0-100)
}

// HSV represents a color in Hue, Saturation, Value format
type HSV struct {
	H float64 // Hue (0-360)
	S float64 // Saturation (0-100)
	V float64 // Value (0-100)
}

// CMYK represents a color in Cyan, Magenta, Yellow, Key (Black) format
type CMYK struct {
	C float64 // Cyan (0-100)
	M float64 // Magenta (0-100)
	Y float64 // Yellow (0-100)
	K float64 // Key/Black (0-100)
}

// Color represents a color with RGB and optional Alpha
type Color struct {
	RGB   RGB
	Alpha uint8 // Alpha channel (0-255), 255 = fully opaque
}

// NewRGB creates a new RGB color
func NewRGB(r, g, b uint8) RGB {
	return RGB{R: r, G: g, B: b}
}

// NewHSL creates a new HSL color
func NewHSL(h, s, l float64) HSL {
	// Normalize values
	h = math.Mod(h, 360)
	if h < 0 {
		h += 360
	}
	s = clamp(s, 0, 100)
	l = clamp(l, 0, 100)
	return HSL{H: h, S: s, L: l}
}

// NewHSV creates a new HSV color
func NewHSV(h, s, v float64) HSV {
	h = math.Mod(h, 360)
	if h < 0 {
		h += 360
	}
	s = clamp(s, 0, 100)
	v = clamp(v, 0, 100)
	return HSV{H: h, S: s, V: v}
}

// NewCMYK creates a new CMYK color
func NewCMYK(c, m, y, k float64) CMYK {
	return CMYK{
		C: clamp(c, 0, 100),
		M: clamp(m, 0, 100),
		Y: clamp(y, 0, 100),
		K: clamp(k, 0, 100),
	}
}

// --- RGB Conversions ---

// RGBToHex converts RGB to hex string (e.g., "#ff0000")
func RGBToHex(rgb RGB) string {
	return fmt.Sprintf("#%02x%02x%02x", rgb.R, rgb.G, rgb.B)
}

// RGBToHSL converts RGB to HSL
func RGBToHSL(rgb RGB) HSL {
	r := float64(rgb.R) / 255.0
	g := float64(rgb.G) / 255.0
	b := float64(rgb.B) / 255.0

	max := math.Max(math.Max(r, g), b)
	min := math.Min(math.Min(r, g), b)
	l := (max + min) / 2.0

	var h, s float64

	if max == min {
		h = 0
		s = 0
	} else {
		d := max - min
		s = d / (1 - math.Abs(2*l-1))

		switch max {
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
	}

	return HSL{H: h, S: s * 100, L: l * 100}
}

// RGBToHSV converts RGB to HSV
func RGBToHSV(rgb RGB) HSV {
	r := float64(rgb.R) / 255.0
	g := float64(rgb.G) / 255.0
	b := float64(rgb.B) / 255.0

	max := math.Max(math.Max(r, g), b)
	min := math.Min(math.Min(r, g), b)
	v := max

	var h, s float64

	if max == min {
		h = 0
		s = 0
	} else {
		d := max - min
		s = d / max

		switch max {
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
	}

	return HSV{H: h, S: s * 100, V: v * 100}
}

// RGBToCMYK converts RGB to CMYK
func RGBToCMYK(rgb RGB) CMYK {
	r := float64(rgb.R) / 255.0
	g := float64(rgb.G) / 255.0
	b := float64(rgb.B) / 255.0

	k := 1 - math.Max(math.Max(r, g), b)

	if k == 1 {
		return CMYK{C: 0, M: 0, Y: 0, K: 100}
	}

	c := (1 - r - k) / (1 - k)
	m := (1 - g - k) / (1 - k)
	y := (1 - b - k) / (1 - k)

	return CMYK{
		C: c * 100,
		M: m * 100,
		Y: y * 100,
		K: k * 100,
	}
}

// --- Reverse Conversions ---

// HexToRGB converts hex string to RGB
func HexToRGB(hex string) (RGB, error) {
	hex = strings.TrimSpace(hex)
	hex = strings.TrimPrefix(hex, "#")

	if len(hex) == 3 {
		hex = string(hex[0]) + string(hex[0]) + string(hex[1]) + string(hex[1]) + string(hex[2]) + string(hex[2])
	}

	if len(hex) != 6 {
		return RGB{}, fmt.Errorf("invalid hex color: %s", hex)
	}

	r, err := strconv.ParseUint(hex[0:2], 16, 8)
	if err != nil {
		return RGB{}, fmt.Errorf("invalid hex color: %s", hex)
	}
	g, err := strconv.ParseUint(hex[2:4], 16, 8)
	if err != nil {
		return RGB{}, fmt.Errorf("invalid hex color: %s", hex)
	}
	b, err := strconv.ParseUint(hex[4:6], 16, 8)
	if err != nil {
		return RGB{}, fmt.Errorf("invalid hex color: %s", hex)
	}

	return RGB{R: uint8(r), G: uint8(g), B: uint8(b)}, nil
}

// HSLToRGB converts HSL to RGB
func HSLToRGB(hsl HSL) RGB {
	h := hsl.H
	s := hsl.S / 100
	l := hsl.L / 100

	var r, g, b float64

	if s == 0 {
		r, g, b = l, l, l
	} else {
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
	}

	return RGB{
		R: uint8(math.Round(r * 255)),
		G: uint8(math.Round(g * 255)),
		B: uint8(math.Round(b * 255)),
	}
}

func hueToRGB(p, q, t float64) float64 {
	if t < 0 {
		t += 1
	}
	if t > 1 {
		t -= 1
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

// HSVToRGB converts HSV to RGB
func HSVToRGB(hsv HSV) RGB {
	h := hsv.H
	s := hsv.S / 100
	v := hsv.V / 100

	var r, g, b float64

	i := math.Floor(h / 60)
	f := h/60 - i
	p := v * (1 - s)
	q := v * (1 - f*s)
	t := v * (1 - (1-f)*s)

	switch int(i) % 6 {
	case 0:
		r, g, b = v, t, p
	case 1:
		r, g, b = q, v, p
	case 2:
		r, g, b = p, v, t
	case 3:
		r, g, b = p, q, v
	case 4:
		r, g, b = t, p, v
	case 5:
		r, g, b = v, p, q
	}

	return RGB{
		R: uint8(math.Round(r * 255)),
		G: uint8(math.Round(g * 255)),
		B: uint8(math.Round(b * 255)),
	}
}

// CMYKToRGB converts CMYK to RGB
func CMYKToRGB(cmyk CMYK) RGB {
	c := cmyk.C / 100
	m := cmyk.M / 100
	y := cmyk.Y / 100
	k := cmyk.K / 100

	r := 255 * (1 - c) * (1 - k)
	g := 255 * (1 - m) * (1 - k)
	b := 255 * (1 - y) * (1 - k)

	return RGB{
		R: uint8(math.Round(r)),
		G: uint8(math.Round(g)),
		B: uint8(math.Round(b)),
	}
}

// --- Color Manipulation ---

// Complementary returns the complementary color
func Complementary(rgb RGB) RGB {
	return RGB{
		R: 255 - rgb.R,
		G: 255 - rgb.G,
		B: 255 - rgb.B,
	}
}

// Lighten increases the lightness of a color by the given percentage
func Lighten(rgb RGB, percent float64) RGB {
	hsl := RGBToHSL(rgb)
	hsl.L = clamp(hsl.L+hsl.L*(percent/100), 0, 100)
	return HSLToRGB(hsl)
}

// Darken decreases the lightness of a color by the given percentage
func Darken(rgb RGB, percent float64) RGB {
	hsl := RGBToHSL(rgb)
	hsl.L = clamp(hsl.L-hsl.L*(percent/100), 0, 100)
	return HSLToRGB(hsl)
}

// Saturate increases the saturation of a color by the given percentage
func Saturate(rgb RGB, percent float64) RGB {
	hsl := RGBToHSL(rgb)
	hsl.S = clamp(hsl.S+hsl.S*(percent/100), 0, 100)
	return HSLToRGB(hsl)
}

// Desaturate decreases the saturation of a color by the given percentage
func Desaturate(rgb RGB, percent float64) RGB {
	hsl := RGBToHSL(rgb)
	hsl.S = clamp(hsl.S-hsl.S*(percent/100), 0, 100)
	return HSLToRGB(hsl)
}

// Mix blends two colors by a given weight (0-1)
// weight 0 = 100% color1, weight 1 = 100% color2
func Mix(color1, color2 RGB, weight float64) RGB {
	w := clamp(weight, 0, 1)
	return RGB{
		R: uint8(math.Round(float64(color1.R)*(1-w) + float64(color2.R)*w)),
		G: uint8(math.Round(float64(color1.G)*(1-w) + float64(color2.G)*w)),
		B: uint8(math.Round(float64(color1.B)*(1-w) + float64(color2.B)*w)),
	}
}

// Grayscale converts a color to grayscale
func Grayscale(rgb RGB) RGB {
	// Using luminosity method: 0.21 R + 0.72 G + 0.07 B
	gray := uint8(math.Round(0.21*float64(rgb.R) + 0.72*float64(rgb.G) + 0.07*float64(rgb.B)))
	return RGB{R: gray, G: gray, B: gray}
}

// Invert inverts a color
func Invert(rgb RGB) RGB {
	return RGB{
		R: 255 - rgb.R,
		G: 255 - rgb.G,
		B: 255 - rgb.B,
	}
}

// IsLight returns true if the color is considered light
func IsLight(rgb RGB) bool {
	// Calculate relative luminance
	luminance := (0.299*float64(rgb.R) + 0.587*float64(rgb.G) + 0.114*float64(rgb.B)) / 255
	return luminance > 0.5
}

// IsDark returns true if the color is considered dark
func IsDark(rgb RGB) bool {
	return !IsLight(rgb)
}

// Luminance returns the relative luminance of a color (0-1)
func Luminance(rgb RGB) float64 {
	r := linearize(float64(rgb.R) / 255)
	g := linearize(float64(rgb.G) / 255)
	b := linearize(float64(rgb.B) / 255)
	return 0.2126*r + 0.7152*g + 0.0722*b
}

func linearize(c float64) float64 {
	if c <= 0.03928 {
		return c / 12.92
	}
	return math.Pow((c+0.055)/1.055, 2.4)
}

// ContrastRatio calculates the contrast ratio between two colors (WCAG)
func ContrastRatio(color1, color2 RGB) float64 {
	l1 := Luminance(color1)
	l2 := Luminance(color2)
	if l1 > l2 {
		return (l1 + 0.05) / (l2 + 0.05)
	}
	return (l2 + 0.05) / (l1 + 0.05)
}

// String returns the hex representation of the color
func (rgb RGB) String() string {
	return RGBToHex(rgb)
}

// String returns a formatted HSL representation
func (hsl HSL) String() string {
	return fmt.Sprintf("hsl(%.1f, %.1f%%, %.1f%%)", hsl.H, hsl.S, hsl.L)
}

// String returns a formatted HSV representation
func (hsv HSV) String() string {
	return fmt.Sprintf("hsv(%.1f, %.1f%%, %.1f%%)", hsv.H, hsv.S, hsv.V)
}

// String returns a formatted CMYK representation
func (cmyk CMYK) String() string {
	return fmt.Sprintf("cmyk(%.1f%%, %.1f%%, %.1f%%, %.1f%%)", cmyk.C, cmyk.M, cmyk.Y, cmyk.K)
}

// Helper function to clamp a value between min and max
func clamp(value, min, max float64) float64 {
	if value < min {
		return min
	}
	if value > max {
		return max
	}
	return value
}