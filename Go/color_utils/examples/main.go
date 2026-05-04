// Example usage of color_utils package
package main

import (
	"fmt"
	"sort"

	color "github.com/ayukyo/alltoolkit/Go/color_utils"
)

func main() {
	fmt.Println("=== Color Utils Examples ===")
	fmt.Println()

	// 1. RGB <-> Hex Conversion
	fmt.Println("1. RGB <-> Hex Conversion")
	rgb := color.NewRGB(255, 128, 64)
	fmt.Printf("   RGB to Hex: %v -> %s\n", rgb, color.RGBToHex(rgb))

	hex := "#4a90d9"
	rgbFromHex, _ := color.HexToRGB(hex)
	fmt.Printf("   Hex to RGB: %s -> %v\n", hex, rgbFromHex)
	fmt.Println()

	// 2. Color Space Conversions
	fmt.Println("2. Color Space Conversions")
	coral := color.NewRGB(255, 127, 80)

	hsl := color.RGBToHSL(coral)
	fmt.Printf("   RGB to HSL: %v -> %s\n", coral, hsl.String())

	hsv := color.RGBToHSV(coral)
	fmt.Printf("   RGB to HSV: %v -> %s\n", coral, hsv.String())

	cmyk := color.RGBToCMYK(coral)
	fmt.Printf("   RGB to CMYK: %v -> %s\n", coral, cmyk.String())
	fmt.Println()

	// 3. Round-trip Conversions
	fmt.Println("3. Round-trip Conversions")
	original := color.NewRGB(100, 150, 200)
	hslRoundTrip := color.RGBToHSL(original)
	backToRGB := color.HSLToRGB(hslRoundTrip)
	fmt.Printf("   RGB -> HSL -> RGB: %v -> %s -> %v\n", original, hslRoundTrip.String(), backToRGB)
	fmt.Println()

	// 4. Named Colors
	fmt.Println("4. Named Colors")
	if named, ok := color.NameToRGB("coral"); ok {
		fmt.Printf("   'coral' -> %v (%s)\n", named, color.RGBToHex(named))
	}

	// Find closest named color
	custom := color.NewRGB(254, 100, 80)
	closest := color.RGBToName(custom)
	fmt.Printf("   %v closest named color: %s\n", custom, closest)

	// Search colors by name
	fmt.Print("   Colors containing 'blue': ")
	blues := color.SearchColorsByName("blue")
	var blueNames []string
	for _, c := range blues {
		blueNames = append(blueNames, c.Name)
	}
	sort.Strings(blueNames)
	fmt.Printf("%d colors found\n", len(blueNames))
	fmt.Println()

	// 5. Color Manipulation
	fmt.Println("5. Color Manipulation")
	base := color.NewRGB(100, 150, 200)

	fmt.Printf("   Base color: %v (%s)\n", base, color.RGBToHex(base))
	fmt.Printf("   Complementary: %v (%s)\n", color.Complementary(base), color.RGBToHex(color.Complementary(base)))
	fmt.Printf("   Lighter: %v (%s)\n", color.Lighten(base, 30), color.RGBToHex(color.Lighten(base, 30)))
	fmt.Printf("   Darker: %v (%s)\n", color.Darken(base, 30), color.RGBToHex(color.Darken(base, 30)))
	fmt.Printf("   Grayscale: %v (%s)\n", color.Grayscale(base), color.RGBToHex(color.Grayscale(base)))
	fmt.Printf("   Inverted: %v (%s)\n", color.Invert(base), color.RGBToHex(color.Invert(base)))
	fmt.Println()

	// 6. Color Mixing
	fmt.Println("6. Color Mixing")
	red := color.NewRGB(255, 0, 0)
	blue := color.NewRGB(0, 0, 255)

	fmt.Printf("   Mixing %s and %s:\n", color.RGBToHex(red), color.RGBToHex(blue))
	fmt.Printf("   25%%: %v (%s)\n", color.Mix(red, blue, 0.25), color.RGBToHex(color.Mix(red, blue, 0.25)))
	fmt.Printf("   50%%: %v (%s)\n", color.Mix(red, blue, 0.5), color.RGBToHex(color.Mix(red, blue, 0.5)))
	fmt.Printf("   75%%: %v (%s)\n", color.Mix(red, blue, 0.75), color.RGBToHex(color.Mix(red, blue, 0.75)))
	fmt.Println()

	// 7. Lightness Check (for text color selection)
	fmt.Println("7. Lightness Check")
	bgColor := color.NewRGB(50, 50, 100)
	textColor := color.NewRGB(255, 255, 255)

	if color.IsDark(bgColor) {
		fmt.Printf("   Background %s is dark, use light text\n", color.RGBToHex(bgColor))
	}

	ratio := color.ContrastRatio(bgColor, textColor)
	fmt.Printf("   Contrast ratio with white: %.2f:1\n", ratio)
	if ratio >= 4.5 {
		fmt.Println("   ✓ WCAG AA compliant (>= 4.5:1)")
	} else {
		fmt.Println("   ✗ Not WCAG AA compliant (needs >= 4.5:1)")
	}
	fmt.Println()

	// 8. Color Schemes
	fmt.Println("8. Color Schemes")
	baseColor := color.NewRGB(0, 128, 255)

	fmt.Printf("   Base: %s\n", color.RGBToHex(baseColor))
	fmt.Print("   Complementary: ")
	for _, c := range color.GenerateScheme(baseColor, color.Complementary_) {
		fmt.Printf("%s ", color.RGBToHex(c))
	}
	fmt.Println()

	fmt.Print("   Triadic: ")
	for _, c := range color.GenerateScheme(baseColor, color.Triadic) {
		fmt.Printf("%s ", color.RGBToHex(c))
	}
	fmt.Println()

	fmt.Print("   Analogous: ")
	for _, c := range color.GenerateScheme(baseColor, color.Analogous) {
		fmt.Printf("%s ", color.RGBToHex(c))
	}
	fmt.Println()
	fmt.Println()

	// 9. Gradients
	fmt.Println("9. Gradients")
	start := color.NewRGB(255, 0, 128)
	end := color.NewRGB(0, 255, 128)
	gradient := color.Gradient(start, end, 5)

	fmt.Printf("   Gradient from %s to %s:\n", color.RGBToHex(start), color.RGBToHex(end))
	for i, c := range gradient {
		fmt.Printf("   %d: %s\n", i+1, color.RGBToHex(c))
	}
	fmt.Println()

	// 10. Shades, Tints, and Tones
	fmt.Println("10. Shades, Tints, Tones")
	orig := color.NewRGB(200, 100, 50)

	fmt.Printf("   Original: %s\n", color.RGBToHex(orig))
	fmt.Print("   Shades (darker to lighter): ")
	for _, c := range color.Shades(orig, 5) {
		fmt.Printf("%s ", color.RGBToHex(c))
	}
	fmt.Println()

	fmt.Print("   Tints (with white): ")
	for _, c := range color.Tints(orig, 5) {
		fmt.Printf("%s ", color.RGBToHex(c))
	}
	fmt.Println()

	fmt.Print("   Tones (with gray): ")
	for _, c := range color.Tones(orig, 5) {
		fmt.Printf("%s ", color.RGBToHex(c))
	}
	fmt.Println()
	fmt.Println()

	// 11. Warm and Cool Palettes
	fmt.Println("11. Warm and Cool Palettes")
	fmt.Print("   Warm colors: ")
	for _, c := range color.Warm(5) {
		fmt.Printf("%s ", color.RGBToHex(c))
	}
	fmt.Println()

	fmt.Print("   Cool colors: ")
	for _, c := range color.Cool(5) {
		fmt.Printf("%s ", color.RGBToHex(c))
	}
	fmt.Println()
}