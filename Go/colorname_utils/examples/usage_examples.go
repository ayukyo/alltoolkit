// Example usage of colorname_utils package
package main

import (
	"fmt"

	colorname "github.com/ayukyo/alltoolkit/Go/colorname_utils"
)

func main() {
	fmt.Println("=== Color Name Utils Examples ===")
	fmt.Println()

	// Example 1: Parse hex color and get name
	fmt.Println("--- Example 1: Parse Hex Color ---")
	hexColors := []string{"#FF0000", "#00FF00", "#0000FF", "#FFA500", "#808080"}
	for _, hex := range hexColors {
		rgb, err := colorname.ParseHex(hex)
		if err != nil {
			fmt.Printf("Error parsing %s: %v\n", hex, err)
			continue
		}
		name := colorname.GetColorName(rgb)
		fmt.Printf("Hex %s -> RGB(%d, %d, %d) -> Name: %s\n", hex, rgb.R, rgb.G, rgb.B, name)
	}
	fmt.Println()

	// Example 2: Get comprehensive color info
	fmt.Println("--- Example 2: Get Color Info ---")
	rgb := colorname.RGB{255, 128, 0}
	info := colorname.GetColorInfo(rgb)
	fmt.Printf("Color: %s\n", info.Hex)
	fmt.Printf("  Name: %s\n", info.Name)
	fmt.Printf("  RGB: (%d, %d, %d)\n", info.RGB.R, info.RGB.G, info.RGB.B)
	fmt.Printf("  HSL: (H=%.1f, S=%.1f%%, L=%.1f%%)\n", info.HSL.H, info.HSL.S, info.HSL.L)
	fmt.Printf("  Category: %s\n", info.Category)
	fmt.Printf("  Brightness: %s\n", info.Brightness)
	fmt.Printf("  Temperature: %s\n", info.Temperature)
	fmt.Println()

	// Example 3: Find closest colors
	fmt.Println("--- Example 3: Find Closest Colors ---")
	testColor := colorname.RGB{200, 50, 50} // Dark reddish
	closest := colorname.GetNClosestColors(testColor, 5)
	fmt.Printf("Test color: RGB(%d, %d, %d)\n", testColor.R, testColor.G, testColor.B)
	fmt.Println("Closest matches:")
	for i, match := range closest {
		fmt.Printf("  %d. %s (%s) - Distance: %.2f\n", i+1, match.Name, match.Hex, match.Distance)
	}
	fmt.Println()

	// Example 4: Color transformations
	fmt.Println("--- Example 4: Color Transformations ---")
	original := colorname.RGB{128, 64, 32}
	fmt.Printf("Original: RGB(%d, %d, %d)\n", original.R, original.G, original.B)

	lighter := colorname.Lighten(original, 30)
	fmt.Printf("Lightened (+30): RGB(%d, %d, %d) = %s\n", lighter.R, lighter.G, lighter.B, colorname.RGBToHex(lighter))

	darker := colorname.Darken(original, 30)
	fmt.Printf("Darkened (-30): RGB(%d, %d, %d) = %s\n", darker.R, darker.G, darker.B, colorname.RGBToHex(darker))

	inverted := colorname.InvertColor(original)
	fmt.Printf("Inverted: RGB(%d, %d, %d) = %s\n", inverted.R, inverted.G, inverted.B, colorname.RGBToHex(inverted))

	grayscale := colorname.Grayscale(original)
	fmt.Printf("Grayscale: RGB(%d, %d, %d) = %s\n", grayscale.R, grayscale.G, grayscale.B, colorname.RGBToHex(grayscale))

	sepia := colorname.Sepia(original)
	fmt.Printf("Sepia: RGB(%d, %d, %d) = %s\n", sepia.R, sepia.G, sepia.B, colorname.RGBToHex(sepia))
	fmt.Println()

	// Example 5: Color harmonies
	fmt.Println("--- Example 5: Color Harmonies ---")
	base := colorname.RGB{255, 0, 0} // Red
	fmt.Printf("Base color: %s (%s)\n", colorname.GetColorName(base), colorname.RGBToHex(base))

	complementary := colorname.ComplementaryColor(base)
	fmt.Printf("Complementary: %s (%s)\n", colorname.GetColorName(complementary), colorname.RGBToHex(complementary))

	analogous := colorname.AnalogousColors(base)
	fmt.Println("Analogous colors:")
	for _, c := range analogous {
		fmt.Printf("  %s (%s)\n", colorname.GetColorName(c), colorname.RGBToHex(c))
	}

	triadic := colorname.TriadicColors(base)
	fmt.Println("Triadic colors:")
	for _, c := range triadic {
		fmt.Printf("  %s (%s)\n", colorname.GetColorName(c), colorname.RGBToHex(c))
	}

	split := colorname.SplitComplementaryColors(base)
	fmt.Println("Split complementary colors:")
	for _, c := range split {
		fmt.Printf("  %s (%s)\n", colorname.GetColorName(c), colorname.RGBToHex(c))
	}

	tetradic := colorname.TetradicColors(base)
	fmt.Println("Tetradic colors:")
	for _, c := range tetradic {
		fmt.Printf("  %s (%s)\n", colorname.GetColorName(c), colorname.RGBToHex(c))
	}
	fmt.Println()

	// Example 6: Color blending
	fmt.Println("--- Example 6: Color Blending ---")
	color1 := colorname.RGB{255, 0, 0}   // Red
	color2 := colorname.RGB{0, 0, 255}   // Blue

	for ratio := 0.0; ratio <= 1.0; ratio += 0.25 {
		blended := colorname.BlendColors(color1, color2, ratio)
		fmt.Printf("Blend %.0f%% Red + %.0f%% Blue = %s (%s)\n",
			(1-ratio)*100, ratio*100,
			colorname.GetColorName(blended),
			colorname.RGBToHex(blended))
	}
	fmt.Println()

	// Example 7: Contrast color for UI
	fmt.Println("--- Example 7: Contrast Colors for UI ---")
	backgrounds := []colorname.RGB{
		{255, 255, 255}, // White
		{0, 0, 0},       // Black
		{30, 144, 255},  // Dodger Blue
		{255, 69, 0},    // Orange Red
		{128, 128, 128}, // Gray
	}

	for _, bg := range backgrounds {
		contrast := colorname.GetContrastColor(bg)
		fmt.Printf("Background: %s (%s) -> Text color: %s\n",
			colorname.GetColorName(bg),
			colorname.RGBToHex(bg),
			colorname.RGBToHex(contrast))
	}
	fmt.Println()

	// Example 8: Color categories
	fmt.Println("--- Example 8: Color Categories ---")
	categories := []string{"Red", "Blue", "Green", "Yellow"}
	for _, cat := range categories {
		colors := colorname.ColorNamesByCategory(cat)
		fmt.Printf("%s category: %d colors\n", cat, len(colors))
		if len(colors) > 0 && len(colors) <= 10 {
			fmt.Printf("  Examples: %v\n", colors[:min(5, len(colors))])
		}
	}
	fmt.Println()

	// Example 9: Search color names
	fmt.Println("--- Example 9: Search Color Names ---")
	searchTerms := []string{"blue", "green", "pink"}
	for _, term := range searchTerms {
		results := colorname.SearchColorNames(term)
		fmt.Printf("Search '%s': %d results\n", term, len(results))
		for i, r := range results {
			if i < 5 {
				fmt.Printf("  %s (%s)\n", r.Name, r.Hex)
			}
		}
	}
	fmt.Println()

	// Example 10: Color by name lookup
	fmt.Println("--- Example 10: Get Color by Name ---")
	names := []string{"Red", "Emerald", "Cobalt", "Peach"}
	for _, name := range names {
		rgb, found := colorname.GetColorByName(name)
		if found {
			fmt.Printf("%s: RGB(%d, %d, %d) = %s\n", name, rgb.R, rgb.G, rgb.B, colorname.RGBToHex(rgb))
		} else {
			fmt.Printf("%s: Not found\n", name)
		}
	}
	fmt.Println()

	// Example 11: Random colors
	fmt.Println("--- Example 11: Random Colors ---")
	for i := 0; i < 3; i++ {
		random := colorname.RandomColor()
		fmt.Printf("Random color: %s (%s)\n", colorname.GetColorName(random), colorname.RGBToHex(random))
	}

	for i := 0; i < 3; i++ {
		pastel := colorname.RandomPastelColor()
		fmt.Printf("Pastel color: %s (%s)\n", colorname.GetColorName(pastel), colorname.RGBToHex(pastel))
	}

	for i := 0; i < 3; i++ {
		dark := colorname.RandomDarkColor()
		fmt.Printf("Dark color: %s (%s)\n", colorname.GetColorName(dark), colorname.RGBToHex(dark))
	}
	fmt.Println()

	// Example 12: Color comparison
	fmt.Println("--- Example 12: Color Comparison ---")
	colors := []colorname.RGB{
		{255, 0, 0},
		{250, 0, 0},
		{0, 0, 255},
		{0, 0, 250},
	}

	for i := 0; i < len(colors); i++ {
		for j := i + 1; j < len(colors); j++ {
			dist := colorname.ColorDistance(colors[i], colors[j])
			similar := colorname.AreColorsSimilar(colors[i], colors[j], 50)
			fmt.Printf("Distance between %s and %s: %.2f (Similar: %v)\n",
				colorname.RGBToHex(colors[i]),
				colorname.RGBToHex(colors[j]),
				dist, similar)
		}
	}
	fmt.Println()

	// Example 13: HSL conversions
	fmt.Println("--- Example 13: HSL Conversions ---")
	rgbColors := []colorname.RGB{
		{255, 0, 0},   // Red
		{0, 255, 0},   // Green
		{0, 0, 255},   // Blue
		{255, 255, 0}, // Yellow
	}

	for _, rgb := range rgbColors {
		hsl := colorname.RGBToHSL(rgb)
		fmt.Printf("RGB(%d, %d, %d) -> HSL(H=%.1f°, S=%.1f%%, L=%.1f%%)\n",
			rgb.R, rgb.G, rgb.B, hsl.H, hsl.S, hsl.L)
	}

	hslColors := []colorname.HSL{
		{0, 100, 50},   // Red
		{120, 100, 50}, // Green
		{240, 100, 50}, // Blue
		{60, 100, 50},  // Yellow
	}

	for _, hsl := range hslColors {
		rgb := colorname.HSLToRGB(hsl)
		fmt.Printf("HSL(H=%.1f°, S=%.1f%%, L=%.1f%%) -> RGB(%d, %d, %d)\n",
			hsl.H, hsl.S, hsl.L, rgb.R, rgb.G, rgb.B)
	}
	fmt.Println()

	// Example 14: Statistics
	fmt.Println("--- Example 14: Statistics ---")
	fmt.Printf("Total colors in database: %d\n", colorname.ColorCount())
	fmt.Printf("All color names count: %d\n", len(colorname.GetAllColorNames()))
	fmt.Println()

	fmt.Println("=== All Examples Completed ===")
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}