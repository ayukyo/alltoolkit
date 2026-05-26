// Example usage of palette_utils package
package main

import (
	"fmt"
	"strings"
	
	palette "github.com/ayukyo/alltoolkit/Go/palette_utils"
)

func main() {
	fmt.Println("🎨 Color Palette Utils - Examples")
	fmt.Println(strings.Repeat("=", 50))
	
	// 1. Creating colors
	fmt.Println("\n1. Creating Colors")
	fmt.Println(strings.Repeat("-", 30))
	
	// From RGB
	red := palette.RGB(255, 0, 0)
	fmt.Printf("RGB(255, 0, 0): %s\n", red.Hex())
	
	// From Hex
	blue, _ := palette.Hex("#0066FF")
	fmt.Printf("Hex('#0066FF'): %s\n", blue.Hex())
	
	// MustHex (panics on error)
	green := palette.MustHex("#00FF00")
	fmt.Printf("MustHex('#00FF00'): %s\n", green.Hex())
	
	// 2. Color properties
	fmt.Println("\n2. Color Properties")
	fmt.Println(strings.Repeat("-", 30))
	
	h, s, l := red.HSL()
	fmt.Printf("Red HSL: H=%.1f°, S=%.2f, L=%.2f\n", h, s, l)
	
	h, s, v := red.HSV()
	fmt.Printf("Red HSV: H=%.1f°, S=%.2f, V=%.2f\n", h, s, v)
	
	fmt.Printf("Red Luminance: %.4f\n", red.Luminance())
	fmt.Printf("Red is light: %v\n", red.IsLight())
	fmt.Printf("Red is dark: %v\n", red.IsDark())
	
	// 3. Color manipulation
	fmt.Println("\n3. Color Manipulation")
	fmt.Println(strings.Repeat("-", 30))
	
	orange := palette.RGB(255, 128, 0)
	fmt.Printf("Original: %s\n", orange.Hex())
	fmt.Printf("Lighten: %s\n", orange.Lighten(0.2).Hex())
	fmt.Printf("Darken: %s\n", orange.Darken(0.2).Hex())
	fmt.Printf("Saturate: %s\n", orange.Saturate(0.3).Hex())
	fmt.Printf("Desaturate: %s\n", orange.Desaturate(0.5).Hex())
	fmt.Printf("Rotate 60°: %s\n", orange.RotateHue(60).Hex())
	fmt.Printf("Complement: %s\n", orange.Complement().Hex())
	
	// 4. Color harmonies
	fmt.Println("\n4. Color Harmonies")
	fmt.Println(strings.Repeat("-", 30))
	
	baseColor := palette.MustHex("#3498DB")
	fmt.Printf("Base color: %s\n", baseColor.Hex())
	
	fmt.Println("\nAnalogous:")
	for _, c := range baseColor.Analogous() {
		fmt.Printf("  %s\n", c.Hex())
	}
	
	fmt.Println("\nTriadic:")
	for _, c := range baseColor.Triadic() {
		fmt.Printf("  %s\n", c.Hex())
	}
	
	fmt.Println("\nSplit Complementary:")
	for _, c := range baseColor.SplitComplementary() {
		fmt.Printf("  %s\n", c.Hex())
	}
	
	fmt.Println("\nTetradic:")
	for _, c := range baseColor.Tetradic() {
		fmt.Printf("  %s\n", c.Hex())
	}
	
	// 5. Palette generation
	fmt.Println("\n5. Palette Generation")
	fmt.Println(strings.Repeat("-", 30))
	
	// Monochromatic
	mono := palette.Monochromatic(baseColor, 5)
	fmt.Printf("\nMonochromatic (%s):\n", mono.Name)
	printPalette(mono)
	
	// Shades
	shades := palette.Shades(baseColor, 5)
	fmt.Printf("\nShades:\n")
	printPalette(shades)
	
	// Tints
	tints := palette.Tints(baseColor, 5)
	fmt.Printf("\nTints:\n")
	printPalette(tints)
	
	// Gradient
	gradient := palette.Gradient(red, blue, 7)
	fmt.Printf("\nGradient (Red to Blue):\n")
	printPalette(gradient)
	
	// Harmony
	harmony := palette.Harmony(baseColor)
	fmt.Printf("\nHarmony:\n")
	printPalette(harmony)
	
	// 6. WCAG contrast
	fmt.Println("\n6. WCAG Contrast Accessibility")
	fmt.Println(strings.Repeat("-", 30))
	
	bg := palette.MustHex("#FFFFFF")
	fg1 := palette.MustHex("#333333")
	fg2 := palette.MustHex("#CCCCCC")
	
	passes, ratio := palette.WCAGAA(fg1, bg)
	fmt.Printf("%s on white: AA %s (ratio: %.2f:1)\n", fg1.Hex(), passStr(passes), ratio)
	
	passes, ratio = palette.WCAGAA(fg2, bg)
	fmt.Printf("%s on white: AA %s (ratio: %.2f:1)\n", fg2.Hex(), passStr(passes), ratio)
	
	passes, ratio = palette.WCAGAAA(fg1, bg)
	fmt.Printf("%s on white: AAA %s (ratio: %.2f:1)\n", fg1.Hex(), passStr(passes), ratio)
	
	// Text color suggestion
	bg = palette.MustHex("#2C3E50")
	text := palette.SuggestTextColor(bg)
	fmt.Printf("\nSuggested text color for %s: %s (%s)\n", bg.Hex(), text.Hex(), text.Name)
	
	// 7. Color distance
	fmt.Println("\n7. Color Distance")
	fmt.Println(strings.Repeat("-", 30))
	
	c1 := palette.MustHex("#FF0000")
	c2 := palette.MustHex("#FF3333")
	c3 := palette.MustHex("#00FF00")
	
	fmt.Printf("Distance %s to %s: %.2f\n", c1.Hex(), c2.Hex(), palette.ColorDistance(c1, c2))
	fmt.Printf("Distance %s to %s: %.2f\n", c1.Hex(), c3.Hex(), palette.ColorDistance(c1, c3))
	
	// 8. Sorting colors
	fmt.Println("\n8. Sorting Colors")
	fmt.Println(strings.Repeat("-", 30))
	
	colors := []palette.Color{
		palette.MustHex("#FF0000"), // Red
		palette.MustHex("#00FF00"), // Green
		palette.MustHex("#0000FF"), // Blue
		palette.MustHex("#FFFF00"), // Yellow
		palette.MustHex("#FF00FF"), // Magenta
	}
	
	fmt.Println("Original order:")
	for _, c := range colors {
		fmt.Printf("  %s\n", c.Hex())
	}
	
	palette.SortByHue(colors)
	fmt.Println("\nSorted by hue:")
	for _, c := range colors {
		fmt.Printf("  %s\n", c.Hex())
	}
	
	palette.SortByLuminance(colors)
	fmt.Println("\nSorted by luminance (light to dark):")
	for _, c := range colors {
		fmt.Printf("  %s (lum: %.3f)\n", c.Hex(), c.Luminance())
	}
	
	// 9. Random colors
	fmt.Println("\n9. Random Colors")
	fmt.Println(strings.Repeat("-", 30))
	
	palette.SetRandomSeed(42)
	
	fmt.Println("Random colors:")
	for i := 0; i < 5; i++ {
		c := palette.Random()
		fmt.Printf("  %s\n", c.Hex())
	}
	
	fmt.Println("\nRandom pastels:")
	for i := 0; i < 5; i++ {
		c := palette.RandomPastel()
		fmt.Printf("  %s\n", c.Hex())
	}
	
	fmt.Println("\nRandom vibrant:")
	for i := 0; i < 5; i++ {
		c := palette.RandomVibrant()
		fmt.Printf("  %s\n", c.Hex())
	}
	
	// 10. Complete palette example
	fmt.Println("\n10. Complete UI Palette Example")
	fmt.Println(strings.Repeat("-", 30))
	
	primary := palette.MustHex("#3498DB")
	
	uiPalette := []struct {
		name  string
		color palette.Color
	}{
		{"Primary", primary},
		{"Primary Light", primary.Lighten(0.2)},
		{"Primary Dark", primary.Darken(0.2)},
		{"Accent", primary.Complement()},
		{"Success", palette.MustHex("#2ECC71")},
		{"Warning", palette.MustHex("#F1C40F")},
		{"Error", palette.MustHex("#E74C3C")},
		{"Info", palette.MustHex("#3498DB")},
	}
	
	fmt.Println("UI Color Palette:")
	for _, item := range uiPalette {
		text := palette.SuggestTextColor(item.color)
		fmt.Printf("  %-15s %-10s (text: %s)\n", item.name+":", item.color.Hex(), text.Hex())
	}
}

func printPalette(p palette.Palette) {
	for _, c := range p.Colors {
		name := c.Name
		if name == "" {
			name = "Color"
		}
		fmt.Printf("  %-12s %s\n", name+":", c.Hex())
	}
}

func passStr(passes bool) string {
	if passes {
		return "✓ PASS"
	}
	return "✗ FAIL"
}