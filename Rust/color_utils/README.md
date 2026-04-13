# Color Utils

A comprehensive color manipulation library for Rust with **zero external dependencies**.

## Features

- **Multiple Color Spaces**: RGB, RGBA, HSL, HSV, CMYK, HEX
- **Color Conversion**: Convert between all supported color spaces
- **Color Manipulation**: Lighten, darken, saturate, desaturate, grayscale, invert
- **Color Analysis**: Luminance calculation, contrast checking, WCAG compliance
- **Color Schemes**: Triadic, analogous, split-complementary, complementary
- **Named Colors**: CSS color name lookup for common colors
- **Color Mixing**: Blend two colors with adjustable weight

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
color_utils = "1.0.0"
```

## Quick Start

```rust
use color_utils::{Color, ContrastLevel};

fn main() {
    // Create colors from different formats
    let red = Color::rgb(255, 0, 0);
    let orange = Color::from_hex("#FF8040").unwrap();
    let teal = Color::hsl(180, 100, 25);
    let cyan = Color::hsv(180, 100, 100);
    
    // Convert between formats
    println!("HEX: {}", orange.to_hex());        // #FF8040
    println!("HSL: {:?}", orange.to_hsl());      // (24, 100, 94)
    println!("CMYK: {:?}", orange.to_cmyk());   // (0, 50, 75, 0)
    
    // Check contrast for accessibility
    let text = Color::rgb(0, 0, 0);
    let bg = Color::rgb(255, 255, 255);
    println!("Contrast: {:.2}:1", text.contrast_ratio(&bg)); // 21:1
    println!("WCAG Level: {}", text.contrast_level(&bg));    // AAA
    
    // Generate color schemes
    let triadic = red.triadic();
    let analogous = red.analogous();
    let complement = red.complementary();
}
```

## API Reference

### Creating Colors

```rust
// From RGB values (0-255)
let color = Color::rgb(r, g, b);
let color = Color::rgba(r, g, b, a);

// From HSL (H: 0-360, S: 0-100, L: 0-100)
let color = Color::hsl(h, s, l);

// From HSV (H: 0-360, S: 0-100, V: 0-100)
let color = Color::hsv(h, s, v);

// From CMYK (all values 0-100)
let color = Color::cmyk(c, m, y, k);

// From hex string
let color = Color::from_hex("#FF8040")?;
let color = Color::from_hex("FF8040")?;
let color = Color::from_hex("#F80")?;      // 3-digit shorthand
let color = Color::from_hex("#FF804080")?; // With alpha
```

### Color Conversion

```rust
// Get RGB values
let (r, g, b) = color.as_rgb();
let (r, g, b, a) = color.as_rgba();

// Convert to other formats
let hex = color.to_hex();           // "#FF8040"
let hex_rgb = color.to_hex_rgb();   // "#FF8040" (ignores alpha)
let (h, s, l) = color.to_hsl();     // Hue: 0-360, S/L: 0-100
let (h, s, v) = color.to_hsv();     // Hue: 0-360, S/V: 0-100
let (c, m, y, k) = color.to_cmyk(); // All values 0-100
```

### Color Properties

```rust
// Luminance (0.0 - 1.0)
let lum = color.luminance();

// Is light/dark
if color.is_light() { /* ... */ }
if color.is_dark() { /* ... */ }

// Named color lookup (CSS colors)
if let Some(name) = color.name() {
    println!("This is {}", name); // e.g., "red", "blue", "navy"
}
```

### Contrast & Accessibility

```rust
// Contrast ratio (1.0 - 21.0)
let ratio = text.contrast_ratio(&background);

// WCAG compliance level
match text.contrast_level(&background) {
    ContrastLevel::AAA => println!("Passes AAA (≥7:1)"),
    ContrastLevel::AA => println!("Passes AA (≥4.5:1)"),
    ContrastLevel::AA_Large => println!("Passes AA for large text (≥3:1)"),
    ContrastLevel::Fail => println!("Fails WCAG"),
}
```

### Color Manipulation

```rust
// Lighten/darken by percentage (0-100)
let lighter = color.lighten(20);
let darker = color.darken(20);

// Saturate/desaturate
let more_saturated = color.saturate(30);
let less_saturated = color.desaturate(30);

// Grayscale
let gray = color.grayscale();

// Invert
let inverted = color.invert();

// Complementary color
let comp = color.complementary();

// Mix two colors (weight: 0.0 = 100% self, 1.0 = 100% other)
let mixed = color1.mix(&color2, 0.5);
```

### Color Schemes

```rust
// Triadic (3 colors, 120° apart)
let [c1, c2, c3] = color.triadic();

// Analogous (3 colors, 30° apart)
let [c1, c2, c3] = color.analogous();

// Split-complementary
let [c1, c2, c3] = color.split_complementary();
```

## Examples

Run the included examples:

```bash
# Basic usage
cargo run --example basic_usage

# Color scheme generation
cargo run --example color_schemes

# WCAG contrast checker
cargo run --example contrast_checker
```

## Zero Dependencies

This crate uses only the Rust standard library. No external crates required.

## License

MIT License