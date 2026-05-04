"""
Gradient Utilities - A comprehensive toolkit for generating color gradients.

This module provides utilities for creating various types of color gradients
with zero external dependencies. Supports multiple color formats and gradient types.

Features:
- Linear gradients (single or multi-stop)
- Radial gradients
- Color format conversions (hex, rgb, hsl)
- Gradient interpolation in different color spaces
- Export to various formats
"""

import math
import colorsys
from typing import List, Tuple, Union, Optional


class Color:
    """Represents a color in RGB format with conversion utilities."""
    
    def __init__(self, r: int, g: int, b: int):
        """
        Initialize a color with RGB values.
        
        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
        """
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))
    
    @classmethod
    def from_hex(cls, hex_color: str) -> 'Color':
        """
        Create a Color from a hex string.
        
        Args:
            hex_color: Hex color string (e.g., "#FF0000" or "FF0000")
        
        Returns:
            Color instance
        
        Raises:
            ValueError: If hex string is invalid
        """
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        if len(hex_color) != 6:
            raise ValueError(f"Invalid hex color: {hex_color}")
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return cls(r, g, b)
        except ValueError:
            raise ValueError(f"Invalid hex color: {hex_color}")
    
    @classmethod
    def from_hsl(cls, h: float, s: float, l: float) -> 'Color':
        """
        Create a Color from HSL values.
        
        Args:
            h: Hue (0-360)
            s: Saturation (0-100)
            l: Lightness (0-100)
        
        Returns:
            Color instance
        """
        # Normalize to 0-1 range for colorsys
        h_norm = h / 360.0
        s_norm = s / 100.0
        l_norm = l / 100.0
        
        r, g, b = colorsys.hls_to_rgb(h_norm, l_norm, s_norm)
        return cls(int(r * 255), int(g * 255), int(b * 255))
    
    def to_hex(self) -> str:
        """Convert color to hex string (e.g., "#FF0000")."""
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"
    
    def to_rgb(self) -> Tuple[int, int, int]:
        """Get RGB tuple."""
        return (self.r, self.g, self.b)
    
    def to_hsl(self) -> Tuple[float, float, float]:
        """Convert to HSL values."""
        r_norm = self.r / 255.0
        g_norm = self.g / 255.0
        b_norm = self.b / 255.0
        
        h, l, s = colorsys.rgb_to_hls(r_norm, g_norm, b_norm)
        return (h * 360, s * 100, l * 100)
    
    def __repr__(self):
        return f"Color(r={self.r}, g={self.g}, b={self.b})"
    
    def __eq__(self, other):
        if isinstance(other, Color):
            return self.r == other.r and self.g == other.g and self.b == other.b
        return False


class GradientStop:
    """Represents a color stop in a gradient."""
    
    def __init__(self, position: float, color: Union[Color, str, Tuple[int, int, int]]):
        """
        Initialize a gradient stop.
        
        Args:
            position: Position in gradient (0.0 to 1.0)
            color: Color (Color instance, hex string, or RGB tuple)
        """
        if position < 0 or position > 1:
            raise ValueError(f"Position must be between 0 and 1, got {position}")
        self.position = position
        self.color = self._normalize_color(color)
    
    def _normalize_color(self, color: Union[Color, str, Tuple[int, int, int]]) -> Color:
        """Convert various color formats to Color instance."""
        if isinstance(color, Color):
            return color
        elif isinstance(color, str):
            return Color.from_hex(color)
        elif isinstance(color, tuple) and len(color) == 3:
            return Color(*color)
        else:
            raise ValueError(f"Invalid color format: {color}")
    
    def __repr__(self):
        return f"GradientStop(position={self.position}, color={self.color})"


class LinearGradient:
    """Generates linear color gradients."""
    
    def __init__(self, stops: List[GradientStop]):
        """
        Initialize a linear gradient with color stops.
        
        Args:
            stops: List of GradientStop instances
        
        Raises:
            ValueError: If less than 2 stops provided
        """
        if len(stops) < 2:
            raise ValueError("At least 2 gradient stops are required")
        self.stops = sorted(stops, key=lambda s: s.position)
    
    @classmethod
    def from_colors(cls, *colors: Union[Color, str, Tuple[int, int, int]]) -> 'LinearGradient':
        """
        Create a linear gradient from colors with evenly spaced positions.
        
        Args:
            colors: Variable number of colors
        
        Returns:
            LinearGradient instance
        
        Example:
            >>> gradient = LinearGradient.from_colors("#FF0000", "#00FF00", "#0000FF")
        """
        if len(colors) < 2:
            raise ValueError("At least 2 colors are required")
        
        stops = []
        for i, color in enumerate(colors):
            position = i / (len(colors) - 1)
            stops.append(GradientStop(position, color))
        return cls(stops)
    
    def color_at(self, position: float) -> Color:
        """
        Get the color at a specific position in the gradient.
        
        Args:
            position: Position in gradient (0.0 to 1.0)
        
        Returns:
            Color instance at that position
        """
        position = max(0, min(1, position))
        
        # Find surrounding stops
        if position <= self.stops[0].position:
            return self.stops[0].color
        if position >= self.stops[-1].position:
            return self.stops[-1].color
        
        for i in range(len(self.stops) - 1):
            stop1 = self.stops[i]
            stop2 = self.stops[i + 1]
            
            if stop1.position <= position <= stop2.position:
                # Interpolate between stops
                if stop1.position == stop2.position:
                    return stop1.color
                
                t = (position - stop1.position) / (stop2.position - stop1.position)
                return self._interpolate_color(stop1.color, stop2.color, t)
        
        return self.stops[-1].color
    
    def _interpolate_color(self, color1: Color, color2: Color, t: float) -> Color:
        """Linearly interpolate between two colors."""
        r = int(color1.r + (color2.r - color1.r) * t)
        g = int(color1.g + (color2.g - color1.g) * t)
        b = int(color1.b + (color2.b - color1.b) * t)
        return Color(r, g, b)
    
    def generate(self, steps: int = 10) -> List[Color]:
        """
        Generate a list of colors from the gradient.
        
        Args:
            steps: Number of colors to generate
        
        Returns:
            List of Color instances
        """
        if steps < 2:
            steps = 2
        
        colors = []
        for i in range(steps):
            position = i / (steps - 1)
            colors.append(self.color_at(position))
        return colors
    
    def generate_hex(self, steps: int = 10) -> List[str]:
        """
        Generate a list of hex color strings from the gradient.
        
        Args:
            steps: Number of colors to generate
        
        Returns:
            List of hex color strings
        """
        return [color.to_hex() for color in self.generate(steps)]
    
    def generate_rgb(self, steps: int = 10) -> List[Tuple[int, int, int]]:
        """
        Generate a list of RGB tuples from the gradient.
        
        Args:
            steps: Number of colors to generate
        
        Returns:
            List of RGB tuples
        """
        return [color.to_rgb() for color in self.generate(steps)]


class RadialGradient:
    """Generates radial color gradients."""
    
    def __init__(self, inner_color: Union[Color, str, Tuple[int, int, int]], 
                 outer_color: Union[Color, str, Tuple[int, int, int]]):
        """
        Initialize a radial gradient.
        
        Args:
            inner_color: Color at the center
            outer_color: Color at the edges
        """
        self.inner_color = self._normalize_color(inner_color)
        self.outer_color = self._normalize_color(outer_color)
    
    def _normalize_color(self, color: Union[Color, str, Tuple[int, int, int]]) -> Color:
        """Convert various color formats to Color instance."""
        if isinstance(color, Color):
            return color
        elif isinstance(color, str):
            return Color.from_hex(color)
        elif isinstance(color, tuple) and len(color) == 3:
            return Color(*color)
        else:
            raise ValueError(f"Invalid color format: {color}")
    
    def color_at(self, distance: float) -> Color:
        """
        Get the color at a specific distance from center.
        
        Args:
            distance: Distance from center (0.0 at center, 1.0 at edge)
        
        Returns:
            Color instance at that distance
        """
        distance = max(0, min(1, distance))
        
        r = int(self.inner_color.r + (self.outer_color.r - self.inner_color.r) * distance)
        g = int(self.inner_color.g + (self.outer_color.g - self.inner_color.g) * distance)
        b = int(self.inner_color.b + (self.outer_color.b - self.inner_color.b) * distance)
        
        return Color(r, g, b)
    
    def generate(self, steps: int = 10) -> List[Color]:
        """
        Generate a list of colors from center to edge.
        
        Args:
            steps: Number of colors to generate
        
        Returns:
            List of Color instances
        """
        if steps < 2:
            steps = 2
        
        colors = []
        for i in range(steps):
            distance = i / (steps - 1)
            colors.append(self.color_at(distance))
        return colors


class HSLGradient:
    """Generates gradients in HSL color space for smoother color transitions."""
    
    @staticmethod
    def rainbow(steps: int = 10, saturation: float = 100, lightness: float = 50) -> List[Color]:
        """
        Generate a rainbow gradient (full hue spectrum).
        
        Args:
            steps: Number of colors to generate
            saturation: Saturation (0-100)
            lightness: Lightness (0-100)
        
        Returns:
            List of Color instances
        """
        colors = []
        for i in range(steps):
            hue = (i / steps) * 360
            colors.append(Color.from_hsl(hue, saturation, lightness))
        return colors
    
    @staticmethod
    def hue_range(start_hue: float, end_hue: float, steps: int = 10, 
                  saturation: float = 100, lightness: float = 50) -> List[Color]:
        """
        Generate a gradient across a range of hues.
        
        Args:
            start_hue: Starting hue (0-360)
            end_hue: Ending hue (0-360)
            steps: Number of colors to generate
            saturation: Saturation (0-100)
            lightness: Lightness (0-100)
        
        Returns:
            List of Color instances
        """
        colors = []
        for i in range(steps):
            hue = start_hue + (end_hue - start_hue) * (i / (steps - 1))
            colors.append(Color.from_hsl(hue, saturation, lightness))
        return colors
    
    @staticmethod
    def saturation_gradient(hue: float, lightness: float, steps: int = 10) -> List[Color]:
        """
        Generate a gradient across saturation levels.
        
        Args:
            hue: Hue (0-360)
            lightness: Lightness (0-100)
            steps: Number of colors to generate
        
        Returns:
            List of Color instances
        """
        colors = []
        for i in range(steps):
            saturation = (i / (steps - 1)) * 100
            colors.append(Color.from_hsl(hue, saturation, lightness))
        return colors
    
    @staticmethod
    def lightness_gradient(hue: float, saturation: float, steps: int = 10) -> List[Color]:
        """
        Generate a gradient across lightness levels.
        
        Args:
            hue: Hue (0-360)
            saturation: Saturation (0-100)
            steps: Number of colors to generate
        
        Returns:
            List of Color instances
        """
        colors = []
        for i in range(steps):
            lightness = (i / (steps - 1)) * 100
            colors.append(Color.from_hsl(hue, saturation, lightness))
        return colors


def create_gradient(colors: List[Union[Color, str, Tuple[int, int, int]]], 
                    steps: int = 10) -> List[Color]:
    """
    Convenience function to create a linear gradient from colors.
    
    Args:
        colors: List of colors (hex strings, RGB tuples, or Color instances)
        steps: Number of colors to generate
    
    Returns:
        List of Color instances
    
    Example:
        >>> colors = create_gradient(["#FF0000", "#00FF00", "#0000FF"], steps=10)
    """
    gradient = LinearGradient.from_colors(*colors)
    return gradient.generate(steps)


def hex_gradient(colors: List[str], steps: int = 10) -> List[str]:
    """
    Convenience function to create a gradient of hex color strings.
    
    Args:
        colors: List of hex color strings
        steps: Number of colors to generate
    
    Returns:
        List of hex color strings
    
    Example:
        >>> gradient = hex_gradient(["#FF0000", "#0000FF"], steps=5)
        >>> print(gradient)
        ['#FF0000', '#BF0040', '#7F0080', '#3F00BF', '#0000FF']
    """
    gradient = LinearGradient.from_colors(*colors)
    return gradient.generate_hex(steps)


def css_linear_gradient(colors: List[str], direction: str = "to right") -> str:
    """
    Generate CSS linear-gradient string.
    
    Args:
        colors: List of hex color strings
        direction: CSS gradient direction (e.g., "to right", "45deg")
    
    Returns:
        CSS linear-gradient string
    
    Example:
        >>> css = css_linear_gradient(["#FF0000", "#0000FF"])
        >>> print(css)
        'linear-gradient(to right, #FF0000, #0000FF)'
    """
    return f"linear-gradient({direction}, {', '.join(colors)})"


def palette_from_base_color(base_color: Union[Color, str, Tuple[int, int, int]], 
                            variations: int = 5) -> List[Color]:
    """
    Generate a color palette from a base color by varying lightness.
    
    Args:
        base_color: Base color to generate palette from
        variations: Number of color variations to generate
    
    Returns:
        List of Color instances with varying lightness
    """
    if isinstance(base_color, str):
        base = Color.from_hex(base_color)
    elif isinstance(base_color, tuple):
        base = Color(*base_color)
    else:
        base = base_color
    
    h, s, l = base.to_hsl()
    
    # Generate lighter and darker variations
    colors = []
    lightness_range = 30  # Range above and below base lightness
    
    for i in range(variations):
        # Calculate offset from center
        offset = (i - (variations - 1) / 2) * (lightness_range / (variations / 2))
        new_lightness = max(10, min(90, l + offset))
        colors.append(Color.from_hsl(h, s, new_lightness))
    
    return colors


if __name__ == "__main__":
    # Example usage
    print("=== Linear Gradient ===")
    gradient = LinearGradient.from_colors("#FF0000", "#0000FF")
    colors = gradient.generate_hex(5)
    print(f"Red to Blue gradient: {colors}")
    
    print("\n=== Multi-stop Gradient ===")
    gradient = LinearGradient.from_colors("#FF0000", "#FFFF00", "#00FF00")
    colors = gradient.generate_hex(7)
    print(f"Red-Yellow-Green gradient: {colors}")
    
    print("\n=== Radial Gradient ===")
    radial = RadialGradient("#FFFFFF", "#000000")
    colors = radial.color_at(0.5)
    print(f"Color at 50% distance: {colors.to_hex()}")
    
    print("\n=== HSL Rainbow ===")
    rainbow = HSLGradient.rainbow(6)
    print([c.to_hex() for c in rainbow])
    
    print("\n=== CSS Gradient ===")
    css = css_linear_gradient(["#FF0000", "#00FF00", "#0000FF"])
    print(css)
    
    print("\n=== Palette from Base Color ===")
    palette = palette_from_base_color("#3498DB", 5)
    print([c.to_hex() for c in palette])