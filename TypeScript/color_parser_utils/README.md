# Color Parser Utilities

A comprehensive color parsing, conversion, and manipulation library for TypeScript.

## Features

- **Parse multiple formats**: HEX, RGB, RGBA, HSL, HSLA, CSS named colors
- **Color space conversions**: RGB ↔ HSL ↔ HSV ↔ CMYK ↔ LAB ↔ XYZ
- **Color manipulation**: lighten, darken, saturate, desaturate, adjust hue, set alpha, mix, invert
- **Color harmony**: complementary, analogous, triadic, tetradic, split complementary
- **Accessibility**: luminance, contrast ratio, WCAG compliance checks
- **Palette generation**: gradients, monochromatic, shades, tints
- **Color distance**: RGB Euclidean distance, CIE Delta E 2000
- **Zero external dependencies**

## Installation

```typescript
import { ... } from './color_parser';
```

## Quick Start

```typescript
import { parseColor, rgbToHex, lighten, getContrastRatio } from './color_parser';

// Parse any color format
const info = parseColor('#FF5733');
console.log(info.rgb);  // { r: 255, g: 87, b: 33, a: 1 }
console.log(info.hsl);  // { h: 10, s: 100, l: 60 }

// Convert between formats
const hsl = rgbToHsl({ r: 255, g: 87, b: 33 });
const hex = rgbToHex(hslToRgb(hsl));

// Manipulate colors
console.log(lighten('#FF5733', 20));  // Lighter version
console.log(darken('#FF5733', 20));   // Darker version

// Check accessibility
const ratio = getContrastRatio('#FFFFFF', '#000000');  // 21:1
const passes = meetsWCAG('#FFFFFF', '#000000', 'AA');   // true
```

## API Reference

### Parsing

| Function | Description |
|----------|-------------|
| `parseHex(hex)` | Parse HEX string to RGB |
| `parseRgbString(rgb)` | Parse RGB/RGBA string |
| `parseHslString(hsl)` | Parse HSL/HSLA string |
| `parseColor(color)` | Parse any color format |

### Conversion

| Function | Description |
|----------|-------------|
| `rgbToHex(rgb)` | RGB → HEX |
| `hexToRgb(hex)` | HEX → RGB |
| `rgbToHsl(rgb)` | RGB → HSL |
| `hslToRgb(hsl)` | HSL → RGB |
| `rgbToHsv(rgb)` | RGB → HSV |
| `hsvToRgb(hsv)` | HSV → RGB |
| `rgbToCmyk(rgb)` | RGB → CMYK |
| `cmykToRgb(cmyk)` | CMYK → RGB |
| `rgbToLab(rgb)` | RGB → LAB |
| `labToRgb(lab)` | LAB → RGB |
| `rgbToXyz(rgb)` | RGB → XYZ |
| `xyzToRgb(xyz)` | XYZ → RGB |

### Manipulation

| Function | Description |
|----------|-------------|
| `lighten(color, amount)` | Increase lightness |
| `darken(color, amount)` | Decrease lightness |
| `saturate(color, amount)` | Increase saturation |
| `desaturate(color, amount)` | Decrease saturation |
| `adjustHue(color, degrees)` | Rotate hue |
| `setAlpha(color, alpha)` | Set alpha channel |
| `mix(color1, color2, weight)` | Blend two colors |
| `invert(color)` | Invert color |
| `grayscale(color)` | Convert to grayscale |
| `sepia(color)` | Apply sepia tone |

### Harmony

| Function | Description |
|----------|-------------|
| `complement(color)` | Get complementary color |
| `analogous(color, angle)` | Get analogous colors |
| `triadic(color)` | Get triadic colors |
| `tetradic(color)` | Get tetradic colors |
| `splitComplementary(color)` | Get split complementary colors |

### Accessibility

| Function | Description |
|----------|-------------|
| `getLuminance(color)` | Calculate relative luminance |
| `getContrastRatio(color1, color2)` | Calculate contrast ratio |
| `meetsWCAG(color1, color2, level)` | Check WCAG compliance |
| `getWCAGRating(color1, color2)` | Get WCAG rating |
| `isLight(color)` | Check if color is light |

### Palette Generation

| Function | Description |
|----------|-------------|
| `gradient(start, end, steps)` | Generate gradient palette |
| `monochromatic(color, steps)` | Generate monochromatic palette |
| `shades(color, count)` | Generate shades |
| `tints(color, count)` | Generate tints |
| `random()` | Generate random color |
| `randomPastel()` | Generate random pastel |
| `randomVibrant()` | Generate random vibrant |

### Distance & Analysis

| Function | Description |
|----------|-------------|
| `rgbDistance(color1, color2)` | RGB Euclidean distance |
| `deltaE2000(color1, color2)` | CIE Delta E 2000 |
| `closestNamedColor(color)` | Find closest CSS named color |
| `getColorInfo(color)` | Get complete color information |

### Utility

| Function | Description |
|----------|-------------|
| `toString(color, format)` | Convert to specified format |
| `isValidColor(color)` | Validate color string |
| `equals(color1, color2)` | Check color equality |
| `modify(color, options)` | Modify color properties |

## Constants

- `CSS_NAMED_COLORS` - Object containing all CSS named colors (147+ entries)

## Supported Formats

- **HEX**: `#RGB`, `#RRGGBB`, `#RRGGBBAA`, `RRGGBB`
- **RGB**: `rgb(r, g, b)`, `rgba(r, g, b, a)`
- **HSL**: `hsl(h, s%, l%)`, `hsla(h, s%, l%, a)`
- **Named**: All CSS named colors (e.g., `red`, `Cornflower Blue`)

## WCAG Levels

| Level | Normal Text | Large Text |
|-------|-------------|------------|
| AA | 4.5:1 | 3:1 |
| AAA | 7:1 | 4.5:1 |

## Example Output

```
parseColor('#FF5733')
{
  format: 'hex',
  rgb: { r: 255, g: 87, b: 33, a: 1 },
  hsl: { h: 10, s: 100, l: 60 },
  hsv: { h: 10, s: 87, v: 100 },
  hex: '#FF5733',
  alpha: 1
}
```

## License

MIT