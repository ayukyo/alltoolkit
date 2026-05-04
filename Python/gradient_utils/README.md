# Gradient Utils

A comprehensive toolkit for generating color gradients with zero external dependencies.

## Features

- **Linear Gradients**: Create smooth transitions between multiple colors
- **Radial Gradients**: Generate circular gradients from center to edge
- **HSL Gradients**: Create gradients in HSL color space for natural color transitions
- **Multiple Color Formats**: Support for hex strings, RGB tuples, and HSL values
- **CSS Integration**: Generate CSS linear-gradient strings
- **Palette Generation**: Create color palettes from a base color

## Installation

No installation required. This module uses only Python standard library.

## Quick Start

```python
from mod import LinearGradient, hex_gradient, css_linear_gradient

# Simple two-color gradient
gradient = LinearGradient.from_colors("#FF0000", "#0000FF")
colors = gradient.generate_hex(5)
print(colors)  # ['#FF0000', '#BF0040', '#7F0080', '#3F00BF', '#0000FF']

# Multi-stop gradient
gradient = LinearGradient.from_colors("#FF0000", "#FFFF00", "#00FF00")
colors = gradient.generate_hex(7)

# CSS output
css = css_linear_gradient(["#FF0000", "#00FF00", "#0000FF"])
print(css)  # 'linear-gradient(to right, #FF0000, #00FF00, #0000FF)'
```

## API Reference

### Color Class

Represents a color in RGB format.

```python
from mod import Color

# Create from RGB values
color = Color(255, 128, 0)

# Create from hex string
color = Color.from_hex("#FF8000")
color = Color.from_hex("FF8000")
color = Color.from_hex("#F80")  # 3-digit shorthand

# Create from HSL
color = Color.from_hsl(30, 100, 50)  # hue (0-360), saturation (0-100), lightness (0-100)

# Convert to other formats
hex_str = color.to_hex()    # "#FF8000"
rgb = color.to_rgb()        # (255, 128, 0)
hsl = color.to_hsl()        # (30.0, 100.0, 50.0)
```

### LinearGradient Class

Create linear gradients with multiple color stops.

```python
from mod import LinearGradient, GradientStop

# Simple two-color gradient
gradient = LinearGradient.from_colors("#FF0000", "#0000FF")

# Multi-color gradient
gradient = LinearGradient.from_colors("#FF0000", "#FFFF00", "#00FF00", "#00FFFF")

# Custom stops
stops = [
    GradientStop(0, "#FF0000"),
    GradientStop(0.3, "#FFFF00"),
    GradientStop(0.7, "#00FFFF"),
    GradientStop(1, "#0000FF")
]
gradient = LinearGradient(stops)

# Generate colors
colors = gradient.generate(10)        # List of Color instances
hex_colors = gradient.generate_hex(10)  # List of hex strings
rgb_colors = gradient.generate_rgb(10)  # List of RGB tuples

# Get color at specific position
color = gradient.color_at(0.5)  # Color at 50% position
```

### RadialGradient Class

Create radial (circular) gradients.

```python
from mod import RadialGradient

# Create radial gradient
gradient = RadialGradient("#FFFFFF", "#000000")

# Get color at specific distance from center
color = gradient.color_at(0.0)  # Center color (white)
color = gradient.color_at(0.5)  # Middle gray
color = gradient.color_at(1.0)  # Edge color (black)

# Generate list of colors
colors = gradient.generate(10)  # 10 colors from center to edge
```

### HSLGradient Class

Create gradients in HSL color space for more natural color transitions.

```python
from mod import HSLGradient

# Rainbow gradient (full hue spectrum)
colors = HSLGradient.rainbow(12)

# Hue range (e.g., warm colors)
colors = HSLGradient.hue_range(0, 60, 6)  # Red to Yellow

# Saturation gradient
colors = HSLGradient.saturation_gradient(hue=200, lightness=50, steps=5)

# Lightness gradient
colors = HSLGradient.lightness_gradient(hue=200, saturation=100, steps=5)
```

### Convenience Functions

Quick helpers for common tasks.

```python
from mod import create_gradient, hex_gradient, css_linear_gradient, palette_from_base_color

# Create gradient from colors
colors = create_gradient(["#FF0000", "#00FF00", "#0000FF"], steps=10)

# Create hex gradient
hex_colors = hex_gradient(["#FF0000", "#0000FF"], steps=5)

# Generate CSS
css = css_linear_gradient(["#FF0000", "#00FF00", "#0000FF"], direction="45deg")
# Output: 'linear-gradient(45deg, #FF0000, #00FF00, #0000FF)'

# Generate palette from base color
palette = palette_from_base_color("#3498DB", variations=5)
```

## Examples

### Generate a Warm Color Palette

```python
from mod import HSLGradient

# Generate warm colors (red to yellow)
warm_colors = HSLGradient.hue_range(0, 60, 6, saturation=100, lightness=50)
for color in warm_colors:
    print(color.to_hex())
```

### Create Smooth Gradients for Data Visualization

```python
from mod import LinearGradient

# Temperature gradient (blue to red through white)
gradient = LinearGradient.from_colors("#0000FF", "#FFFFFF", "#FF0000")
colors = gradient.generate_hex(20)

# Use in your visualization
for i, value in enumerate(data):
    color_index = int((value - min_value) / (max_value - min_value) * 19)
    color = colors[color_index]
```

### Generate CSS for Web Development

```python
from mod import css_linear_gradient

# Create multiple CSS gradients
gradients = [
    css_linear_gradient(["#667eea", "#764ba2"], direction="135deg"),
    css_linear_gradient(["#f093fb", "#f5576c"], direction="to right"),
    css_linear_gradient(["#4facfe", "#00f2fe"], direction="to bottom")
]

for css in gradients:
    print(f"background: {css};")
```

### Create Color Palette from Photo

```python
from mod import palette_from_base_color

# Generate 5 variations of a base color
base = "#2ecc71"  # Green
palette = palette_from_base_color(base, variations=5)

# Output palette
for i, color in enumerate(palette):
    print(f"Color {i+1}: {color.to_hex()}")
```

## Use Cases

- **Data Visualization**: Create smooth color scales for charts and graphs
- **UI Design**: Generate color palettes and gradients for interfaces
- **Web Development**: Export CSS gradient strings
- **Game Development**: Create color transitions for effects
- **Image Processing**: Generate color lookup tables
- **Art & Design**: Create harmonious color schemes

## Testing

Run the test suite:

```bash
python gradient_utils_test.py
```

## License

This module is part of the AllToolkit project and follows its licensing terms.