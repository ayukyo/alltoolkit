// Package colorname_utils provides utilities for mapping colors to human-readable names.
// It supports RGB, HEX, and HSL color formats and provides color categorization.
// Zero external dependencies - uses only Go standard library.
package colorname_utils

import (
	"encoding/hex"
	"errors"
	"fmt"
	"math"
	"sort"
	"strconv"
	"strings"
	"time"
)

// RGB represents a color in Red, Green, Blue format
type RGB struct {
	R, G, B uint8
}

// HSL represents a color in Hue, Saturation, Lightness format
type HSL struct {
	H, S, L float64 // H: 0-360, S: 0-100, L: 0-100
}

// ColorInfo contains detailed information about a color
type ColorInfo struct {
	Name        string
	Hex         string
	RGB         RGB
	HSL         HSL
	Category    string // e.g., "Red", "Blue", "Green", "Neutral"
	Brightness  string // "Dark", "Medium", "Light"
	Temperature string // "Warm", "Cool", "Neutral"
}

// ColorMatch represents a color match with distance
type ColorMatch struct {
	Name     string
	Hex      string
	Distance float64
}

// Common color definitions with their RGB values
var colorDatabase = []struct {
	Name string
	RGB  RGB
}{
	// Reds
	{"Red", RGB{255, 0, 0}},
	{"Crimson", RGB{220, 20, 60}},
	{"Crimson Red", RGB{220, 20, 60}},
	{"Fire Brick", RGB{178, 34, 34}},
	{"Dark Red", RGB{139, 0, 0}},
	{"Maroon", RGB{128, 0, 0}},
	{"Indian Red", RGB{205, 92, 92}},
	{"Light Coral", RGB{240, 128, 128}},
	{"Salmon", RGB{250, 128, 114}},
	{"Light Salmon", RGB{255, 160, 122}},
	{"Tomato", RGB{255, 99, 71}},
	{"Orange Red", RGB{255, 69, 0}},
	{"Ruby", RGB{224, 17, 95}},
	{"Scarlet", RGB{255, 36, 0}},
	{"Cherry", RGB{222, 49, 99}},
	{"Rose", RGB{255, 0, 127}},
	{"Carmine", RGB{150, 0, 24}},

	// Pinks
	{"Pink", RGB{255, 192, 203}},
	{"Light Pink", RGB{255, 182, 193}},
	{"Hot Pink", RGB{255, 105, 180}},
	{"Deep Pink", RGB{255, 20, 147}},
	{"Pale Violet Red", RGB{219, 112, 147}},
	{"Medium Violet Red", RGB{199, 21, 133}},
	{"Magenta", RGB{255, 0, 255}},
	{"Fuchsia", RGB{255, 0, 255}},
	{"Dark Magenta", RGB{139, 0, 139}},
	{"Violet Red", RGB{199, 21, 133}},
	{"Blush", RGB{255, 181, 189}},
	{"Coral Pink", RGB{255, 127, 80}},
	{"Orchid", RGB{218, 112, 214}},
	{"Plum", RGB{221, 160, 221}},

	// Oranges
	{"Orange", RGB{255, 165, 0}},
	{"Dark Orange", RGB{255, 140, 0}},
	{"Light Orange", RGB{255, 204, 92}},
	{"Coral", RGB{255, 127, 80}},
	{"Peach", RGB{255, 218, 185}},
	{"Apricot", RGB{255, 195, 111}},
	{"Tangerine", RGB{255, 144, 0}},
	{"Amber", RGB{255, 191, 0}},
	{"Carrot Orange", RGB{237, 145, 33}},
	{"Burnt Orange", RGB{204, 85, 0}},
	{"Pumpkin", RGB{255, 117, 24}},

	// Yellows
	{"Yellow", RGB{255, 255, 0}},
	{"Light Yellow", RGB{255, 255, 224}},
	{"Lemon", RGB{255, 247, 0}},
	{"Lemon Chiffon", RGB{255, 250, 205}},
	{"Light Goldenrod Yellow", RGB{250, 250, 210}},
	{"Papaya Whip", RGB{255, 239, 213}},
	{"Moccasin", RGB{255, 228, 181}},
	{"Peach Puff", RGB{255, 218, 185}},
	{"Pale Goldenrod", RGB{238, 232, 170}},
	{"Khaki", RGB{240, 230, 140}},
	{"Dark Khaki", RGB{189, 183, 107}},
	{"Gold", RGB{255, 215, 0}},
	{"Goldenrod", RGB{218, 165, 32}},
	{"Dark Goldenrod", RGB{184, 134, 11}},
	{"Canary", RGB{255, 255, 115}},
	{"Mustard", RGB{255, 219, 88}},
	{"Cream", RGB{255, 253, 208}},
	{"Beige", RGB{245, 245, 220}},
	{"Banana", RGB{255, 225, 53}},

	// Greens
	{"Green", RGB{0, 128, 0}},
	{"Lime", RGB{0, 255, 0}},
	{"Lime Green", RGB{50, 205, 50}},
	{"Lawn Green", RGB{124, 252, 0}},
	{"Chartreuse", RGB{127, 255, 0}},
	{"Green Yellow", RGB{173, 255, 47}},
	{"Yellow Green", RGB{154, 205, 50}},
	{"Spring Green", RGB{0, 255, 127}},
	{"Medium Spring Green", RGB{0, 250, 154}},
	{"Light Green", RGB{144, 238, 144}},
	{"Pale Green", RGB{152, 251, 152}},
	{"Dark Green", RGB{0, 100, 0}},
	{"Forest Green", RGB{34, 139, 34}},
	{"Sea Green", RGB{46, 139, 87}},
	{"Medium Sea Green", RGB{60, 179, 113}},
	{"Dark Sea Green", RGB{143, 188, 143}},
	{"Light Sea Green", RGB{32, 178, 170}},
	{"Olive", RGB{128, 128, 0}},
	{"Olive Drab", RGB{107, 142, 35}},
	{"Dark Olive Green", RGB{85, 107, 47}},
	{"Tea Green", RGB{208, 240, 192}},
	{"Mint", RGB{189, 252, 201}},
	{"Emerald", RGB{80, 200, 120}},
	{"Jade", RGB{0, 168, 107}},
	{"Forest", RGB{34, 139, 34}},
	{"Moss Green", RGB{138, 154, 91}},
	{"Sage", RGB{188, 184, 138}},
	{"Seafoam", RGB{93, 171, 147}},

	// Cyans
	{"Cyan", RGB{0, 255, 255}},
	{"Aqua", RGB{0, 255, 255}},
	{"Light Cyan", RGB{224, 255, 255}},
	{"Pale Turquoise", RGB{175, 238, 238}},
	{"Aquamarine", RGB{127, 255, 212}},
	{"Turquoise", RGB{64, 224, 208}},
	{"Medium Turquoise", RGB{72, 209, 204}},
	{"Dark Turquoise", RGB{0, 206, 209}},
	{"Cadet Blue", RGB{95, 158, 160}},
	{"Steel Blue", RGB{70, 130, 180}},
	{"Teal", RGB{0, 128, 128}},
	{"Dark Cyan", RGB{0, 139, 139}},

	// Blues
	{"Blue", RGB{0, 0, 255}},
	{"Light Blue", RGB{173, 216, 230}},
	{"Powder Blue", RGB{176, 224, 230}},
	{"Sky Blue", RGB{135, 206, 235}},
	{"Light Sky Blue", RGB{135, 206, 250}},
	{"Deep Sky Blue", RGB{0, 191, 255}},
	{"Dodger Blue", RGB{30, 144, 255}},
	{"Cornflower Blue", RGB{100, 149, 237}},
	{"Medium Slate Blue", RGB{123, 104, 238}},
	{"Royal Blue", RGB{65, 105, 225}},
	{"Blue Violet", RGB{138, 43, 226}},
	{"Indigo", RGB{75, 0, 130}},
	{"Dark Blue", RGB{0, 0, 139}},
	{"Medium Blue", RGB{0, 0, 205}},
	{"Navy", RGB{0, 0, 128}},
	{"Midnight Blue", RGB{25, 25, 112}},
	{"Slate Blue", RGB{106, 90, 205}},
	{"Dark Slate Blue", RGB{72, 61, 139}},
	{"Sapphire", RGB{15, 82, 186}},
	{"Cobalt", RGB{0, 71, 171}},
	{"Azure", RGB{0, 127, 255}},
	{"Baby Blue", RGB{137, 207, 240}},
	{"Periwinkle", RGB{204, 204, 255}},
	{"Electric Blue", RGB{125, 249, 255}},

	// Purples
	{"Purple", RGB{128, 0, 128}},
	{"Light Purple", RGB{180, 96, 208}},
	{"Medium Purple", RGB{147, 112, 219}},
	{"Dark Purple", RGB{99, 0, 139}},
	{"Dark Violet", RGB{148, 0, 211}},
	{"Violet", RGB{238, 130, 238}},
	{"Lavender", RGB{230, 230, 250}},
	{"Thistle", RGB{216, 191, 216}},
	{"Medium Orchid", RGB{186, 85, 211}},
	{"Dark Orchid", RGB{153, 50, 204}},
	{"Heliotrope", RGB{223, 115, 255}},
	{"Lilac", RGB{200, 162, 200}},
	{"Grape", RGB{111, 45, 168}},
	{"Amethyst", RGB{153, 102, 204}},
	{"Mauve", RGB{224, 176, 255}},
	{"Wisteria", RGB{201, 160, 220}},

	// Browns
	{"Brown", RGB{165, 42, 42}},
	{"Saddle Brown", RGB{139, 69, 19}},
	{"Sienna", RGB{160, 82, 45}},
	{"Chocolate", RGB{210, 105, 30}},
	{"Peru", RGB{205, 133, 63}},
	{"Sandy Brown", RGB{244, 164, 96}},
	{"Rosy Brown", RGB{188, 143, 143}},
	{"Tan", RGB{210, 180, 140}},
	{"Light Tan", RGB{238, 213, 183}},
	{"Burlywood", RGB{222, 184, 135}},
	{"Wheat", RGB{245, 222, 179}},
	{"Navajo White", RGB{255, 222, 173}},
	{"Bisque", RGB{255, 228, 196}},
	{"Blanched Almond", RGB{255, 235, 205}},
	{"Cornsilk", RGB{255, 248, 220}},
	{"Copper", RGB{184, 115, 51}},
	{"Bronze", RGB{205, 127, 50}},
	{"Rust", RGB{183, 65, 14}},
	{"Coffee", RGB{111, 78, 55}},
	{"Mahogany", RGB{192, 64, 0}},
	{"Chestnut", RGB{149, 69, 53}},
	{"Cinnamon", RGB{210, 105, 30}},

	// Neutrals
	{"White", RGB{255, 255, 255}},
	{"Snow", RGB{255, 250, 250}},
	{"Honeydew", RGB{240, 255, 240}},
	{"Mint Cream", RGB{245, 255, 250}},
	{"Ghost White", RGB{248, 248, 255}},
	{"White Smoke", RGB{245, 245, 245}},
	{"Seashell", RGB{255, 245, 238}},
	{"Old Lace", RGB{253, 245, 230}},
	{"Floral White", RGB{255, 250, 240}},
	{"Ivory", RGB{255, 255, 240}},
	{"Antique White", RGB{250, 235, 215}},
	{"Linen", RGB{250, 240, 230}},
	{"Lavender Blush", RGB{255, 240, 245}},
	{"Misty Rose", RGB{255, 228, 225}},
	{"Gainsboro", RGB{220, 220, 220}},
	{"Light Gray", RGB{211, 211, 211}},
	{"Silver", RGB{192, 192, 192}},
	{"Dark Gray", RGB{169, 169, 169}},
	{"Gray", RGB{128, 128, 128}},
	{"Dim Gray", RGB{105, 105, 105}},
	{"Light Slate Gray", RGB{119, 136, 153}},
	{"Slate Gray", RGB{112, 128, 144}},
	{"Dark Slate Gray", RGB{47, 79, 79}},
	{"Black", RGB{0, 0, 0}},
	{"Charcoal", RGB{54, 69, 79}},
	{"Slate", RGB{112, 128, 144}},
	{"Ash Gray", RGB{178, 190, 181}},
	{"Taupe", RGB{72, 60, 50}},
	{"Gunmetal", RGB{42, 52, 57}},

	// Additional common colors
	{"Dark Teal", RGB{0, 102, 102}},
	{"Light Teal", RGB{0, 153, 153}},
	{"Mint Green", RGB{152, 255, 152}},
	{"Army Green", RGB{75, 83, 32}},
	{"Hunter Green", RGB{53, 94, 59}},
	{"Fern Green", RGB{79, 121, 66}},
	{"Kelly Green", RGB{76, 187, 23}},
	{"Irish Green", RGB{0, 158, 96}},
	{"Shamrock", RGB{68, 214, 44}},
	{"Avocado", RGB{86, 130, 3}},
	{"Electric Lime", RGB{204, 255, 0}},
	{"Acid Green", RGB{176, 255, 56}},
	{"Neon Green", RGB{57, 255, 20}},
	{"Harlequin", RGB{63, 255, 0}},
	{"Spring Bud", RGB{167, 252, 0}},
	{"Bright Green", RGB{102, 255, 0}},
	{"Pine Green", RGB{1, 121, 111}},
	{"Fern", RGB{113, 146, 103}},
	{"Celadon", RGB{172, 225, 175}},
	{"Pear", RGB{209, 226, 49}},
	{"Moss", RGB{138, 154, 91}},
	{"Seaweed", RGB{24, 87, 42}},
	{"Pine", RGB{43, 74, 41}},
	{"Racing Green", RGB{26, 68, 31}},
	{"British Racing Green", RGB{0, 66, 37}},
	{"Brunswick Green", RGB{27, 77, 46}},
	{"Laurel Green", RGB{169, 186, 157}},
	{"Cambridge Blue", RGB{163, 193, 173}},
	{"Eton Blue", RGB{150, 200, 162}},
	{"Verdigris", RGB{67, 179, 174}},
	{"Viridian", RGB{64, 130, 109}},
	{"Malachite", RGB{11, 218, 81}},
	{"Ivy Green", RGB{0, 111, 60}},
	{"Spinach Green", RGB{24, 83, 44}},
	{"Parrot Green", RGB{0, 165, 103}},
	{"Amazon", RGB{59, 122, 87}},
	{"Bottle Green", RGB{0, 106, 78}},
	{"Evergreen", RGB{1, 95, 63}},
	{"Christmas Green", RGB{0, 128, 0}},
}

// ParseHex parses a hex color string to RGB
func ParseHex(hexColor string) (RGB, error) {
	hexColor = strings.TrimSpace(hexColor)
	hexColor = strings.TrimPrefix(hexColor, "#")
	hexColor = strings.TrimPrefix(hexColor, "0x")

	if len(hexColor) == 3 {
		hexColor = string(hexColor[0]) + string(hexColor[0]) +
			string(hexColor[1]) + string(hexColor[1]) +
			string(hexColor[2]) + string(hexColor[2])
	}

	if len(hexColor) != 6 {
		return RGB{}, errors.New("invalid hex color format")
	}

	b, err := hex.DecodeString(hexColor)
	if err != nil {
		return RGB{}, fmt.Errorf("invalid hex color: %v", err)
	}

	return RGB{R: b[0], G: b[1], B: b[2]}, nil
}

// ParseRGB parses an RGB string like "rgb(255, 0, 0)" or "255, 0, 0"
func ParseRGB(rgbStr string) (RGB, error) {
	rgbStr = strings.TrimSpace(rgbStr)
	rgbStr = strings.TrimPrefix(rgbStr, "rgb(")
	rgbStr = strings.TrimPrefix(rgbStr, "RGB(")
	rgbStr = strings.TrimSuffix(rgbStr, ")")

	parts := strings.Split(rgbStr, ",")
	if len(parts) != 3 {
		return RGB{}, errors.New("invalid RGB format, expected 'r, g, b'")
	}

	r, err := strconv.Atoi(strings.TrimSpace(parts[0]))
	if err != nil {
		return RGB{}, fmt.Errorf("invalid red value: %v", err)
	}

	g, err := strconv.Atoi(strings.TrimSpace(parts[1]))
	if err != nil {
		return RGB{}, fmt.Errorf("invalid green value: %v", err)
	}

	b, err := strconv.Atoi(strings.TrimSpace(parts[2]))
	if err != nil {
		return RGB{}, fmt.Errorf("invalid blue value: %v", err)
	}

	if r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255 {
		return RGB{}, errors.New("RGB values must be between 0 and 255")
	}

	return RGB{R: uint8(r), G: uint8(g), B: uint8(b)}, nil
}

// RGBToHex converts RGB to hex string
func RGBToHex(rgb RGB) string {
	return fmt.Sprintf("#%02X%02X%02X", rgb.R, rgb.G, rgb.B)
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

// HSLToRGB converts HSL to RGB
func HSLToRGB(hsl HSL) RGB {
	h := hsl.H / 360.0
	s := hsl.S / 100.0
	l := hsl.L / 100.0

	var r, g, b float64

	if s == 0 {
		r, g, b = l, l, l
	} else {
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

// ColorDistance calculates the perceptual distance between two colors
// Uses weighted Euclidean distance for better perceptual accuracy
func ColorDistance(c1, c2 RGB) float64 {
	rMean := (float64(c1.R) + float64(c2.R)) / 2.0
	r := float64(c1.R) - float64(c2.R)
	g := float64(c1.G) - float64(c2.G)
	b := float64(c1.B) - float64(c2.B)

	// Weighted formula for better perceptual accuracy
	return math.Sqrt((2+rMean/256)*r*r + 4*g*g + (2+(255-rMean)/256)*b*b)
}

// GetColorName finds the closest color name for the given RGB value
func GetColorName(rgb RGB) string {
	match := GetClosestColor(rgb)
	return match.Name
}

// GetClosestColor finds the closest matching color from the database
func GetClosestColor(rgb RGB) ColorMatch {
	var bestMatch ColorMatch
	minDistance := math.MaxFloat64

	for _, c := range colorDatabase {
		dist := ColorDistance(rgb, c.RGB)
		if dist < minDistance {
			minDistance = dist
			bestMatch = ColorMatch{
				Name:     c.Name,
				Hex:      RGBToHex(c.RGB),
				Distance: dist,
			}
		}
	}

	return bestMatch
}

// GetNClosestColors returns the n closest matching colors
func GetNClosestColors(rgb RGB, n int) []ColorMatch {
	type scoredColor struct {
		Name     string
		Hex      string
		Distance float64
	}

	var scored []scoredColor
	for _, c := range colorDatabase {
		dist := ColorDistance(rgb, c.RGB)
		scored = append(scored, scoredColor{
			Name:     c.Name,
			Hex:      RGBToHex(c.RGB),
			Distance: dist,
		})
	}

	sort.Slice(scored, func(i, j int) bool {
		return scored[i].Distance < scored[j].Distance
	})

	if n > len(scored) {
		n = len(scored)
	}

	result := make([]ColorMatch, n)
	for i := 0; i < n; i++ {
		result[i] = ColorMatch{
			Name:     scored[i].Name,
			Hex:      scored[i].Hex,
			Distance: scored[i].Distance,
		}
	}

	return result
}

// GetColorCategory returns the general category of a color
func GetColorCategory(rgb RGB) string {
	hsl := RGBToHSL(rgb)

	// Handle achromatic colors (low saturation)
	if hsl.S < 10 {
		if hsl.L < 20 {
			return "Black"
		} else if hsl.L > 80 {
			return "White"
		}
		return "Gray"
	}

	// Determine hue-based category
	h := hsl.H

	switch {
	case h < 15 || h >= 345:
		return "Red"
	case h < 45:
		return "Orange"
	case h < 70:
		return "Yellow"
	case h < 165:
		return "Green"
	case h < 195:
		return "Cyan"
	case h < 255:
		return "Blue"
	case h < 285:
		return "Purple"
	case h < 345:
		return "Pink"
	default:
		return "Red"
	}
}

// GetBrightness returns the brightness category
func GetBrightness(rgb RGB) string {
	// Calculate relative luminance
	luminance := 0.299*float64(rgb.R) + 0.587*float64(rgb.G) + 0.114*float64(rgb.B)

	switch {
	case luminance < 60:
		return "Dark"
	case luminance < 180:
		return "Medium"
	default:
		return "Light"
	}
}

// GetTemperature returns the color temperature
func GetTemperature(rgb RGB) string {
	// Warm colors tend to have more red/orange, cool colors have more blue
	warmth := float64(rgb.R) - float64(rgb.B)

	switch {
	case warmth > 40:
		return "Warm"
	case warmth < -40:
		return "Cool"
	default:
		return "Neutral"
	}
}

// GetColorInfo returns comprehensive color information
func GetColorInfo(rgb RGB) ColorInfo {
	match := GetClosestColor(rgb)
	hsl := RGBToHSL(rgb)

	return ColorInfo{
		Name:        match.Name,
		Hex:         RGBToHex(rgb),
		RGB:         rgb,
		HSL:         hsl,
		Category:    GetColorCategory(rgb),
		Brightness:  GetBrightness(rgb),
		Temperature: GetTemperature(rgb),
	}
}

// GetColorInfoHex returns color info from hex string
func GetColorInfoHex(hexColor string) (ColorInfo, error) {
	rgb, err := ParseHex(hexColor)
	if err != nil {
		return ColorInfo{}, err
	}
	return GetColorInfo(rgb), nil
}

// IsLightColor returns true if the color is considered light
func IsLightColor(rgb RGB) bool {
	return GetBrightness(rgb) == "Light"
}

// IsDarkColor returns true if the color is considered dark
func IsDarkColor(rgb RGB) bool {
	return GetBrightness(rgb) == "Dark"
}

// GetContrastColor returns black or white depending on which provides better contrast
func GetContrastColor(rgb RGB) RGB {
	luminance := 0.299*float64(rgb.R) + 0.587*float64(rgb.G) + 0.114*float64(rgb.B)
	if luminance > 128 {
		return RGB{0, 0, 0} // Black for light backgrounds
	}
	return RGB{255, 255, 255} // White for dark backgrounds
}

// BlendColors blends two colors with the given ratio (0-1)
// ratio 0 = 100% color1, ratio 1 = 100% color2
func BlendColors(c1, c2 RGB, ratio float64) RGB {
	ratio = math.Max(0, math.Min(1, ratio))

	return RGB{
		R: uint8(math.Round(float64(c1.R)*(1-ratio) + float64(c2.R)*ratio)),
		G: uint8(math.Round(float64(c1.G)*(1-ratio) + float64(c2.G)*ratio)),
		B: uint8(math.Round(float64(c1.B)*(1-ratio) + float64(c2.B)*ratio)),
	}
}

// Lighten lightens a color by the given amount (0-100)
func Lighten(rgb RGB, amount float64) RGB {
	hsl := RGBToHSL(rgb)
	hsl.L = math.Min(100, hsl.L+amount)
	return HSLToRGB(hsl)
}

// Darken darkens a color by the given amount (0-100)
func Darken(rgb RGB, amount float64) RGB {
	hsl := RGBToHSL(rgb)
	hsl.L = math.Max(0, hsl.L-amount)
	return HSLToRGB(hsl)
}

// Saturate increases the saturation of a color (0-100)
func Saturate(rgb RGB, amount float64) RGB {
	hsl := RGBToHSL(rgb)
	hsl.S = math.Min(100, hsl.S+amount)
	return HSLToRGB(hsl)
}

// Desaturate decreases the saturation of a color (0-100)
func Desaturate(rgb RGB, amount float64) RGB {
	hsl := RGBToHSL(rgb)
	hsl.S = math.Max(0, hsl.S-amount)
	return HSLToRGB(hsl)
}

// ComplementaryColor returns the complementary color
func ComplementaryColor(rgb RGB) RGB {
	hsl := RGBToHSL(rgb)
	hsl.H = math.Mod(hsl.H+180, 360)
	return HSLToRGB(hsl)
}

// AnalogousColors returns analogous colors (adjacent on color wheel)
func AnalogousColors(rgb RGB) []RGB {
	hsl := RGBToHSL(rgb)
	return []RGB{
		HSLToRGB(HSL{H: math.Mod(hsl.H-30+360, 360), S: hsl.S, L: hsl.L}),
		rgb,
		HSLToRGB(HSL{H: math.Mod(hsl.H+30, 360), S: hsl.S, L: hsl.L}),
	}
}

// TriadicColors returns triadic colors (120 degrees apart)
func TriadicColors(rgb RGB) []RGB {
	hsl := RGBToHSL(rgb)
	return []RGB{
		rgb,
		HSLToRGB(HSL{H: math.Mod(hsl.H+120, 360), S: hsl.S, L: hsl.L}),
		HSLToRGB(HSL{H: math.Mod(hsl.H+240, 360), S: hsl.S, L: hsl.L}),
	}
}

// SplitComplementaryColors returns split complementary colors
func SplitComplementaryColors(rgb RGB) []RGB {
	hsl := RGBToHSL(rgb)
	return []RGB{
		rgb,
		HSLToRGB(HSL{H: math.Mod(hsl.H+150, 360), S: hsl.S, L: hsl.L}),
		HSLToRGB(HSL{H: math.Mod(hsl.H+210, 360), S: hsl.S, L: hsl.L}),
	}
}

// TetradicColors returns tetradic colors (square on color wheel)
func TetradicColors(rgb RGB) []RGB {
	hsl := RGBToHSL(rgb)
	return []RGB{
		rgb,
		HSLToRGB(HSL{H: math.Mod(hsl.H+90, 360), S: hsl.S, L: hsl.L}),
		HSLToRGB(HSL{H: math.Mod(hsl.H+180, 360), S: hsl.S, L: hsl.L}),
		HSLToRGB(HSL{H: math.Mod(hsl.H+270, 360), S: hsl.S, L: hsl.L}),
	}
}

// ColorNamesByCategory returns all color names in a category
func ColorNamesByCategory(category string) []string {
	category = strings.ToLower(strings.TrimSpace(category))
	var names []string

	for _, c := range colorDatabase {
		cat := strings.ToLower(GetColorCategory(c.RGB))
		if cat == category {
			names = append(names, c.Name)
		}
	}

	return names
}

// SearchColorNames searches for colors matching the query
func SearchColorNames(query string) []ColorMatch {
	query = strings.ToLower(strings.TrimSpace(query))
	var matches []ColorMatch

	for _, c := range colorDatabase {
		if strings.Contains(strings.ToLower(c.Name), query) {
			matches = append(matches, ColorMatch{
				Name:     c.Name,
				Hex:      RGBToHex(c.RGB),
				Distance: 0, // Exact name match
			})
		}
	}

	return matches
}

// RandomColor returns a random RGB color
func RandomColor() RGB {
	return RGB{
		R: uint8(time.Now().UnixNano() % 256),
		G: uint8((time.Now().UnixNano() / 3) % 256),
		B: uint8((time.Now().UnixNano() / 7) % 256),
	}
}

// RandomPastelColor returns a random pastel color
func RandomPastelColor() RGB {
	return RGB{
		R: uint8(128 + (time.Now().UnixNano()%128)),
		G: uint8(128 + ((time.Now().UnixNano()/3)%128)),
		B: uint8(128 + ((time.Now().UnixNano()/7)%128)),
	}
}

// RandomDarkColor returns a random dark color
func RandomDarkColor() RGB {
	return RGB{
		R: uint8(time.Now().UnixNano() % 100),
		G: uint8((time.Now().UnixNano() / 3) % 100),
		B: uint8((time.Now().UnixNano() / 7) % 100),
	}
}

// InvertColor returns the inverse of a color
func InvertColor(rgb RGB) RGB {
	return RGB{
		R: 255 - rgb.R,
		G: 255 - rgb.G,
		B: 255 - rgb.B,
	}
}

// Grayscale converts a color to grayscale
func Grayscale(rgb RGB) RGB {
	gray := uint8(0.299*float64(rgb.R) + 0.587*float64(rgb.G) + 0.114*float64(rgb.B))
	return RGB{R: gray, G: gray, B: gray}
}

// Sepia applies sepia tone to a color
func Sepia(rgb RGB) RGB {
	r := 0.393*float64(rgb.R) + 0.769*float64(rgb.G) + 0.189*float64(rgb.B)
	g := 0.349*float64(rgb.R) + 0.686*float64(rgb.G) + 0.168*float64(rgb.B)
	b := 0.272*float64(rgb.R) + 0.534*float64(rgb.G) + 0.131*float64(rgb.B)

	return RGB{
		R: uint8(math.Min(255, r)),
		G: uint8(math.Min(255, g)),
		B: uint8(math.Min(255, b)),
	}
}

// AdjustBrightness adjusts brightness by a factor (-100 to 100)
func AdjustBrightness(rgb RGB, factor float64) RGB {
	adjustment := factor * 2.55 // Convert to 0-255 range
	r := math.Max(0, math.Min(255, float64(rgb.R)+adjustment))
	g := math.Max(0, math.Min(255, float64(rgb.G)+adjustment))
	b := math.Max(0, math.Min(255, float64(rgb.B)+adjustment))

	return RGB{
		R: uint8(r),
		G: uint8(g),
		B: uint8(b),
	}
}

// AreColorsSimilar checks if two colors are within a certain distance threshold
func AreColorsSimilar(c1, c2 RGB, threshold float64) bool {
	return ColorDistance(c1, c2) <= threshold
}

// HexToRGB converts hex string to RGB (alias for ParseHex)
func HexToRGB(hexColor string) (RGB, error) {
	return ParseHex(hexColor)
}

// RGBString returns a string representation of RGB
func RGBString(rgb RGB) string {
	return fmt.Sprintf("rgb(%d, %d, %d)", rgb.R, rgb.G, rgb.B)
}

// HSLString returns a string representation of HSL
func HSLString(hsl HSL) string {
	return fmt.Sprintf("hsl(%.1f, %.1f%%, %.1f%%)", hsl.H, hsl.S, hsl.L)
}

// ColorCount returns the number of colors in the database
func ColorCount() int {
	return len(colorDatabase)
}

// GetAllColorNames returns all color names in the database
func GetAllColorNames() []string {
	names := make([]string, len(colorDatabase))
	for i, c := range colorDatabase {
		names[i] = c.Name
	}
	return names
}

// GetColorByName returns RGB for a given color name
func GetColorByName(name string) (RGB, bool) {
	name = strings.ToLower(strings.TrimSpace(name))
	for _, c := range colorDatabase {
		if strings.ToLower(c.Name) == name {
			return c.RGB, true
		}
	}
	return RGB{}, false
}