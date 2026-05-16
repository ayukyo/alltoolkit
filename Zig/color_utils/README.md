# Color Utils

A comprehensive color manipulation library for Zig with zero external dependencies.

## Features

### Color Formats
- **RGB** - Red, Green, Blue (0-255 each)
- **RGBA** - RGB with Alpha (0-255)
- **HSL** - Hue (0-360°), Saturation (0-100%), Lightness (0-100%)
- **HSV** - Hue (0-360°), Saturation (0-100%), Value (0-100%)
- **Hex** - #RGB, #RRGGBB, #RGBA, #RRGGBBAA formats

### Parsing
- Parse hex color strings (#RGB, #RRGGBB, #RGBA, #RRGGBBAA)
- Named CSS colors (red, blue, coral, etc.)
- Case-insensitive parsing

### Conversion
- RGB ↔ HSL
- RGB ↔ HSV
- RGB ↔ Hex
- RGBA ↔ Hex (with alpha)

### Manipulation
- **lighten** - Increase brightness by percentage
- **darken** - Decrease brightness by percentage
- **saturate** - Increase color saturation
- **desaturate** - Decrease color saturation
- **grayscale** - Convert to grayscale
- **invert** - Invert colors
- **rotateHue** - Rotate hue by degrees
- **complement** - Get complementary color (opposite on wheel)
- **mix** - Blend two colors

### Color Schemes
- **analogous** - Adjacent colors on wheel
- **triadic** - Three colors evenly spaced (120°)
- **splitComplementary** - Base + two colors adjacent to complement
- **tetradic** - Four colors forming a square (90° steps)

### Analysis
- **luminance** - Calculate relative luminance (WCAG)
- **contrastRatio** - WCAG contrast ratio between two colors
- **isLight** / **isDark** - Determine color brightness category
- **getContrastingText** - Get best text color (black/white) for background

### Utilities
- 30+ named CSS colors
- Reverse lookup: find closest named color for RGB
- Random color generation
- Random color with specific hue

## Usage

### Import

```zig
const color_utils = @import("color_utils");
```

### Parse Hex Color

```zig
const hex_rgb = color_utils.parseHex("#FF5733");
const rgb = hex_rgb.rgb; // Rgb{ .r = 255, .g = 87, .b = 51 }

const hex_rgba = color_utils.parseHex("#FF573380");
const rgba = hex_rgba.rgba; // Rgba{ .r = 255, .g = 87, .b = 51, .a = 128 }
```

### RGB to HSL

```zig
const rgb = color_utils.Rgb.init(255, 0, 0);
const hsl = color_utils.rgbToHsl(rgb);
// Hsl{ .h = 0, .s = 100, .l = 50 } (pure red)
```

### Lighten / Darken

```zig
const base = color_utils.Rgb.init(100, 100, 100);
const light = color_utils.lighten(base, 30); // 30% lighter
const dark = color_utils.darken(base, 30);   // 30% darker
```

### Color Mixing

```zig
const black = color_utils.Rgb.init(0, 0, 0);
const white = color_utils.Rgb.init(255, 255, 255);
const gray = color_utils.mix(black, white, 50); // 50% mix
```

### Complementary Color

```zig
const red = color_utils.Rgb.init(255, 0, 0);
const cyan = color_utils.complement(red); // opposite on wheel
```

### Triadic Color Scheme

```zig
const colors = color_utils.triadic(red);
// Returns 3 colors: red, green-ish, blue-ish (120° apart)
```

### Contrast Ratio (WCAG)

```zig
const white = color_utils.Rgb.init(255, 255, 255);
const black = color_utils.Rgb.init(0, 0, 0);
const ratio = color_utils.contrastRatio(white, black);
// Returns 21.0 (maximum contrast)
```

### Named Colors

```zig
const coral = color_utils.namedColor("coral"); // Rgb{ .r = 255, .g = 127, .b = 80 }
const navy = color_utils.namedColor("navy");   // Rgb{ .r = 0, .g = 0, .b = 128 }
```

### Random Color

```zig
const random = color_utils.randomRgb();
const random_hex = color_utils.rgbToHex(allocator, random);
```

## Build

```bash
# Run tests
zig build test

# Run example
zig build example
```

## Test Results

All 30+ unit tests pass covering:
- Hex parsing (3, 4, 6, 8 digit formats)
- RGB ↔ HSL conversion
- RGB ↔ HSV conversion
- Color manipulation (lighten, darken, saturate, invert, etc.)
- Color mixing
- Hue rotation and complementary
- Color schemes (triadic, analogous, etc.)
- Luminance and contrast calculations
- Named colors lookup
- Random color generation

## Zero Dependencies

This library uses only Zig's standard library (`std`). No external dependencies required.

## License

MIT