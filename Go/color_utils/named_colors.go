package color_utils

import (
	"strings"
)

// NamedColor represents a named color with its RGB value
type NamedColor struct {
	Name string
	RGB  RGB
}

// NamedColors is a map of CSS color names to RGB values
var NamedColors = map[string]RGB{
	// Reds
	"red":           {255, 0, 0},
	"crimson":       {220, 20, 60},
	"firebrick":     {178, 34, 34},
	"indianred":     {205, 92, 92},
	"darkred":       {139, 0, 0},
	"lightsalmon":   {255, 160, 122},
	"salmon":        {250, 128, 114},
	"darksalmon":    {233, 150, 122},
	"coral":         {255, 127, 80},
	"tomato":        {255, 99, 71},
	"orangered":     {255, 69, 0},
	"palevioletred": {219, 112, 147},
	"mediumvioletred": {199, 21, 133},

	// Pinks
	"pink":        {255, 192, 203},
	"lightpink":   {255, 182, 193},
	"hotpink":     {255, 105, 180},
	"deeppink":    {255, 20, 147},
	"fuchsia":     {255, 0, 255},
	"magenta":     {255, 0, 255},

	// Oranges/Yellows
	"orange":       {255, 165, 0},
	"darkorange":   {255, 140, 0},
	"gold":         {255, 215, 0},
	"goldenrod":    {218, 165, 32},
	"lightgoldenrod": {250, 250, 210},
	"yellow":       {255, 255, 0},
	"lightyellow":  {255, 255, 224},

	// Greens
	"green":           {0, 128, 0},
	"lime":            {0, 255, 0},
	"limegreen":       {50, 205, 50},
	"forestgreen":     {34, 139, 34},
	"darkgreen":       {0, 100, 0},
	"lightgreen":      {144, 238, 144},
	"palegreen":       {152, 251, 152},
	"seagreen":        {46, 139, 87},
	"mediumseagreen":  {60, 179, 113},
	"springgreen":     {0, 255, 127},
	"mediumspringgreen": {0, 250, 154},
	"yellowgreen":     {154, 205, 50},
	"olive":           {128, 128, 0},
	"olivedrab":       {107, 142, 35},
	"darkolivegreen":  {85, 107, 47},
	"chartreuse":      {127, 255, 0},
	"lawngreen":       {124, 252, 0},

	// Cyans
	"cyan":            {0, 255, 255},
	"aqua":            {0, 255, 255},
	"lightcyan":       {224, 255, 255},
	"darkcyan":        {0, 139, 139},
	"teal":            {0, 128, 128},

	// Blues
	"blue":            {0, 0, 255},
	"navy":            {0, 0, 128},
	"darkblue":        {0, 0, 139},
	"mediumblue":      {0, 0, 205},
	"lightblue":       {173, 216, 230},
	"powderblue":      {176, 224, 230},
	"skyblue":         {135, 206, 235},
	"lightskyblue":    {135, 206, 250},
	"deepskyblue":     {0, 191, 255},
	"dodgerblue":      {30, 144, 255},
	"cornflowerblue":  {100, 149, 237},
	"steelblue":       {70, 130, 180},
	"lightsteelblue":  {176, 196, 222},
	"royalblue":       {65, 105, 225},
	"mediumslateblue": {123, 104, 238},
	"slateblue":       {106, 90, 205},
	"darkslateblue":   {72, 61, 139},
	"midnightblue":    {25, 25, 112},

	// Purples
	"purple":          {128, 0, 128},
	"violet":          {238, 130, 238},
	"darkviolet":      {148, 0, 211},
	"blueviolet":      {138, 43, 226},
	"mediumpurple":    {147, 112, 219},
	"mediumorchid":    {186, 85, 211},
	"orchid":          {218, 112, 214},
	"darkorchid":      {153, 50, 204},
	"darkmagenta":     {139, 0, 139},
	"plum":            {221, 160, 221},
	"thistle":         {216, 191, 216},
	"lavender":        {230, 230, 250},
	"indigo":          {75, 0, 130},

	// Browns
	"brown":           {165, 42, 42},
	"saddlebrown":     {139, 69, 19},
	"sienna":          {160, 82, 45},
	"chocolate":       {210, 105, 30},
	"peru":            {205, 133, 63},
	"sandybrown":      {244, 164, 96},
	"burlywood":       {222, 184, 135},
	"tan":             {210, 180, 140},
	"rosybrown":       {188, 143, 143},
	"wheat":           {245, 222, 179},
	"navajowhite":     {255, 222, 173},
	"bisque":          {255, 228, 196},
	"blanchedalmond":  {255, 235, 205},
	"cornsilk":        {255, 248, 220},

	// Grays
	"gray":            {128, 128, 128},
	"grey":            {128, 128, 128},
	"lightgray":       {211, 211, 211},
	"lightgrey":       {211, 211, 211},
	"darkgray":        {169, 169, 169},
	"darkgrey":        {169, 169, 169},
	"dimgray":         {105, 105, 105},
	"dimgrey":         {105, 105, 105},
	"silver":          {192, 192, 192},
	"gainsboro":       {220, 220, 220},
	"whitesmoke":      {245, 245, 245},
	"snow":            {255, 250, 250},

	// Whites
	"white":           {255, 255, 255},
	"ghostwhite":      {248, 248, 255},
	"floralwhite":     {255, 250, 240},
	"ivory":           {255, 255, 240},
	"seashell":        {255, 245, 238},
	"mintcream":       {245, 255, 250},
	"honeydew":        {240, 255, 240},
	"azure":           {240, 255, 255},
	"aliceblue":       {240, 248, 255},
	"lavenderblush":   {255, 240, 245},

	// Blacks
	"black":           {0, 0, 0},
	"charcoal":        {54, 69, 79},

	// Others
	"beige":           {245, 245, 220},
	"linen":           {250, 240, 230},
	"oldlace":         {253, 245, 230},
	"antiquewhite":    {250, 235, 215},
	"papayawhip":      {255, 239, 213},
	"peachpuff":       {255, 218, 185},
	"lemonchiffon":    {255, 250, 205},
	"moccasin":        {255, 228, 181},
	"khaki":           {240, 230, 140},
	"darkkhaki":       {189, 183, 107},
	"maroon":          {128, 0, 0},
	"aquamarine":      {127, 255, 212},
	"turquoise":       {64, 224, 208},
	"mediumturquoise": {72, 209, 204},
	"darkturquoise":   {0, 206, 209},
	"lightseagreen":   {32, 178, 170},
	"cadetblue":       {95, 158, 160},
	"darkseagreen":    {143, 188, 143},
}

// NameToRGB converts a color name to RGB
// Returns the RGB color and true if found, or black and false if not found
func NameToRGB(name string) (RGB, bool) {
	name = strings.ToLower(strings.TrimSpace(name))
	rgb, ok := NamedColors[name]
	return rgb, ok
}

// RGBToName finds the closest named color for an RGB value
// Uses Euclidean distance in RGB color space
func RGBToName(rgb RGB) string {
	var closestName string
	minDistance := float64(1<<63 - 1) // Max float64

	for name, namedRGB := range NamedColors {
		distance := colorDistance(rgb, namedRGB)
		if distance < minDistance {
			minDistance = distance
			closestName = name
		}
	}

	return closestName
}

// RGBToNameWithThreshold finds a named color if within threshold distance
// Returns the name and true if found within threshold, or empty string and false
func RGBToNameWithThreshold(rgb RGB, threshold float64) (string, bool) {
	var closestName string
	minDistance := float64(1<<64 - 1)

	for name, namedRGB := range NamedColors {
		distance := colorDistance(rgb, namedRGB)
		if distance < minDistance {
			minDistance = distance
			closestName = name
		}
	}

	if minDistance <= threshold {
		return closestName, true
	}
	return "", false
}

// GetAllNamedColors returns all named colors as a slice
func GetAllNamedColors() []NamedColor {
	colors := make([]NamedColor, 0, len(NamedColors))
	for name, rgb := range NamedColors {
		colors = append(colors, NamedColor{Name: name, RGB: rgb})
	}
	return colors
}

// SearchColorsByName searches for colors by partial name match
func SearchColorsByName(query string) []NamedColor {
	query = strings.ToLower(strings.TrimSpace(query))
	var results []NamedColor

	for name, rgb := range NamedColors {
		if strings.Contains(name, query) {
			results = append(results, NamedColor{Name: name, RGB: rgb})
		}
	}

	return results
}

// colorDistance calculates Euclidean distance between two RGB colors
func colorDistance(c1, c2 RGB) float64 {
	dr := float64(c1.R) - float64(c2.R)
	dg := float64(c1.G) - float64(c2.G)
	db := float64(c1.B) - float64(c2.B)
	return dr*dr + dg*dg + db*db
}