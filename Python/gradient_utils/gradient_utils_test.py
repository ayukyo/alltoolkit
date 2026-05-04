"""
Unit tests for gradient_utils module.
"""

import unittest
import sys
import os

# Add parent directory to path to import module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Color, GradientStop, LinearGradient, RadialGradient, HSLGradient,
    create_gradient, hex_gradient, css_linear_gradient, palette_from_base_color
)


class TestColor(unittest.TestCase):
    """Test cases for Color class."""
    
    def test_color_creation(self):
        """Test basic color creation."""
        color = Color(255, 128, 0)
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 128)
        self.assertEqual(color.b, 0)
    
    def test_color_clamping(self):
        """Test that color values are clamped to valid range."""
        color = Color(300, -50, 128)
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 0)
        self.assertEqual(color.b, 128)
    
    def test_from_hex_6digit(self):
        """Test creating color from 6-digit hex."""
        color = Color.from_hex("#FF8000")
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 128)
        self.assertEqual(color.b, 0)
    
    def test_from_hex_3digit(self):
        """Test creating color from 3-digit hex."""
        color = Color.from_hex("#F80")
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 136)
        self.assertEqual(color.b, 0)
    
    def test_from_hex_no_hash(self):
        """Test creating color from hex without hash."""
        color = Color.from_hex("FF8000")
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 128)
        self.assertEqual(color.b, 0)
    
    def test_from_hex_invalid(self):
        """Test that invalid hex raises ValueError."""
        with self.assertRaises(ValueError):
            Color.from_hex("INVALID")
        with self.assertRaises(ValueError):
            Color.from_hex("#FF")
    
    def test_from_hsl(self):
        """Test creating color from HSL."""
        # Pure red in HSL
        color = Color.from_hsl(0, 100, 50)
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 0)
        self.assertEqual(color.b, 0)
    
    def test_to_hex(self):
        """Test converting color to hex."""
        color = Color(255, 128, 0)
        self.assertEqual(color.to_hex(), "#FF8000")
    
    def test_to_rgb(self):
        """Test converting color to RGB tuple."""
        color = Color(255, 128, 0)
        self.assertEqual(color.to_rgb(), (255, 128, 0))
    
    def test_to_hsl(self):
        """Test converting color to HSL."""
        # Pure red
        color = Color(255, 0, 0)
        h, s, l = color.to_hsl()
        self.assertAlmostEqual(h, 0, places=1)
        self.assertAlmostEqual(s, 100, places=1)
        self.assertAlmostEqual(l, 50, places=1)
    
    def test_equality(self):
        """Test color equality."""
        color1 = Color(255, 128, 0)
        color2 = Color(255, 128, 0)
        color3 = Color(255, 0, 0)
        self.assertEqual(color1, color2)
        self.assertNotEqual(color1, color3)


class TestGradientStop(unittest.TestCase):
    """Test cases for GradientStop class."""
    
    def test_stop_creation(self):
        """Test creating a gradient stop."""
        stop = GradientStop(0.5, Color(255, 0, 0))
        self.assertEqual(stop.position, 0.5)
        self.assertEqual(stop.color, Color(255, 0, 0))
    
    def test_stop_with_hex(self):
        """Test creating a gradient stop with hex string."""
        stop = GradientStop(0.5, "#FF0000")
        self.assertEqual(stop.color, Color(255, 0, 0))
    
    def test_stop_with_tuple(self):
        """Test creating a gradient stop with RGB tuple."""
        stop = GradientStop(0.5, (255, 0, 0))
        self.assertEqual(stop.color, Color(255, 0, 0))
    
    def test_invalid_position(self):
        """Test that invalid position raises ValueError."""
        with self.assertRaises(ValueError):
            GradientStop(-0.5, Color(255, 0, 0))
        with self.assertRaises(ValueError):
            GradientStop(1.5, Color(255, 0, 0))


class TestLinearGradient(unittest.TestCase):
    """Test cases for LinearGradient class."""
    
    def test_two_color_gradient(self):
        """Test creating a simple two-color gradient."""
        gradient = LinearGradient.from_colors("#FF0000", "#0000FF")
        colors = gradient.generate(3)
        
        self.assertEqual(colors[0], Color(255, 0, 0))
        self.assertEqual(colors[2], Color(0, 0, 255))
        # Middle color should be purple-ish
        self.assertEqual(colors[1].r, 127)
        self.assertEqual(colors[1].g, 0)
        self.assertEqual(colors[1].b, 127)
    
    def test_multi_color_gradient(self):
        """Test creating a multi-color gradient."""
        gradient = LinearGradient.from_colors("#FF0000", "#FFFF00", "#00FF00")
        colors = gradient.generate(5)
        
        self.assertEqual(colors[0], Color(255, 0, 0))
        self.assertEqual(colors[4], Color(0, 255, 0))
    
    def test_color_at_position(self):
        """Test getting color at specific position."""
        gradient = LinearGradient.from_colors("#000000", "#FFFFFF")
        
        # At start
        color = gradient.color_at(0)
        self.assertEqual(color, Color(0, 0, 0))
        
        # At end
        color = gradient.color_at(1)
        self.assertEqual(color, Color(255, 255, 255))
        
        # At middle
        color = gradient.color_at(0.5)
        self.assertEqual(color.r, 127)
        self.assertEqual(color.g, 127)
        self.assertEqual(color.b, 127)
    
    def test_generate_hex(self):
        """Test generating hex color strings."""
        gradient = LinearGradient.from_colors("#FF0000", "#0000FF")
        hex_colors = gradient.generate_hex(3)
        
        self.assertEqual(hex_colors[0], "#FF0000")
        self.assertEqual(hex_colors[2], "#0000FF")
    
    def test_generate_rgb(self):
        """Test generating RGB tuples."""
        gradient = LinearGradient.from_colors("#FF0000", "#0000FF")
        rgb_colors = gradient.generate_rgb(3)
        
        self.assertEqual(rgb_colors[0], (255, 0, 0))
        self.assertEqual(rgb_colors[2], (0, 0, 255))
    
    def test_minimum_stops(self):
        """Test that less than 2 colors raises error."""
        with self.assertRaises(ValueError):
            LinearGradient.from_colors("#FF0000")
    
    def test_clamped_position(self):
        """Test that position is clamped to valid range."""
        gradient = LinearGradient.from_colors("#FF0000", "#0000FF")
        
        # Below 0
        color = gradient.color_at(-0.5)
        self.assertEqual(color, Color(255, 0, 0))
        
        # Above 1
        color = gradient.color_at(1.5)
        self.assertEqual(color, Color(0, 0, 255))
    
    def test_custom_stops(self):
        """Test creating gradient with custom stops."""
        stops = [
            GradientStop(0, "#FF0000"),
            GradientStop(0.3, "#FFFF00"),
            GradientStop(0.7, "#00FFFF"),
            GradientStop(1, "#0000FF")
        ]
        gradient = LinearGradient(stops)
        colors = gradient.generate(5)
        
        self.assertEqual(len(colors), 5)


class TestRadialGradient(unittest.TestCase):
    """Test cases for RadialGradient class."""
    
    def test_radial_gradient(self):
        """Test basic radial gradient."""
        gradient = RadialGradient("#000000", "#FFFFFF")
        
        # At center
        color = gradient.color_at(0)
        self.assertEqual(color, Color(0, 0, 0))
        
        # At edge
        color = gradient.color_at(1)
        self.assertEqual(color, Color(255, 255, 255))
        
        # At 50%
        color = gradient.color_at(0.5)
        self.assertEqual(color.r, 127)
        self.assertEqual(color.g, 127)
        self.assertEqual(color.b, 127)
    
    def test_generate_colors(self):
        """Test generating list of colors."""
        gradient = RadialGradient("#FF0000", "#0000FF")
        colors = gradient.generate(3)
        
        self.assertEqual(len(colors), 3)
        self.assertEqual(colors[0], Color(255, 0, 0))
        self.assertEqual(colors[2], Color(0, 0, 255))


class TestHSLGradient(unittest.TestCase):
    """Test cases for HSLGradient class."""
    
    def test_rainbow(self):
        """Test rainbow gradient generation."""
        colors = HSLGradient.rainbow(6)
        
        self.assertEqual(len(colors), 6)
        # First color should be red (hue 0)
        self.assertEqual(colors[0].r, 255)
        self.assertEqual(colors[0].g, 0)
        self.assertEqual(colors[0].b, 0)
    
    def test_hue_range(self):
        """Test gradient across hue range."""
        colors = HSLGradient.hue_range(0, 180, 3)
        
        self.assertEqual(len(colors), 3)
        # First color should be red
        self.assertEqual(colors[0].r, 255)
        self.assertEqual(colors[0].g, 0)
        self.assertEqual(colors[0].b, 0)
    
    def test_saturation_gradient(self):
        """Test saturation gradient."""
        colors = HSLGradient.saturation_gradient(0, 50, 3)
        
        self.assertEqual(len(colors), 3)
        # Middle color should have 50% saturation (with some tolerance for HSL conversion)
        h, s, l = colors[1].to_hsl()
        self.assertAlmostEqual(s, 50, places=0)
    
    def test_lightness_gradient(self):
        """Test lightness gradient."""
        colors = HSLGradient.lightness_gradient(0, 100, 3)
        
        self.assertEqual(len(colors), 3)
        # First should be darkest
        h1, s1, l1 = colors[0].to_hsl()
        h3, s3, l3 = colors[2].to_hsl()
        self.assertLess(l1, l3)


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for convenience functions."""
    
    def test_create_gradient(self):
        """Test create_gradient function."""
        colors = create_gradient(["#FF0000", "#0000FF"], 5)
        
        self.assertEqual(len(colors), 5)
        self.assertEqual(colors[0], Color(255, 0, 0))
        self.assertEqual(colors[4], Color(0, 0, 255))
    
    def test_hex_gradient(self):
        """Test hex_gradient function."""
        hex_colors = hex_gradient(["#FF0000", "#0000FF"], 5)
        
        self.assertEqual(len(hex_colors), 5)
        self.assertEqual(hex_colors[0], "#FF0000")
        self.assertEqual(hex_colors[4], "#0000FF")
    
    def test_css_linear_gradient(self):
        """Test CSS gradient generation."""
        css = css_linear_gradient(["#FF0000", "#00FF00", "#0000FF"])
        
        self.assertEqual(css, "linear-gradient(to right, #FF0000, #00FF00, #0000FF)")
    
    def test_css_linear_gradient_custom_direction(self):
        """Test CSS gradient with custom direction."""
        css = css_linear_gradient(["#FF0000", "#0000FF"], "45deg")
        
        self.assertEqual(css, "linear-gradient(45deg, #FF0000, #0000FF)")
    
    def test_palette_from_base_color(self):
        """Test palette generation from base color."""
        palette = palette_from_base_color("#3498DB", 5)
        
        self.assertEqual(len(palette), 5)
        # All colors should have similar hue
        base_hue = palette[2].to_hsl()[0]  # Middle color
        for color in palette:
            hue = color.to_hsl()[0]
            # Hues should be within a reasonable range
            self.assertLess(abs(hue - base_hue), 10)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_minimum_steps(self):
        """Test gradient with minimum steps."""
        gradient = LinearGradient.from_colors("#FF0000", "#0000FF")
        colors = gradient.generate(2)
        
        self.assertEqual(len(colors), 2)
        self.assertEqual(colors[0], Color(255, 0, 0))
        self.assertEqual(colors[1], Color(0, 0, 255))
    
    def test_single_step(self):
        """Test gradient with single step (should default to 2)."""
        gradient = LinearGradient.from_colors("#FF0000", "#0000FF")
        colors = gradient.generate(1)
        
        self.assertEqual(len(colors), 2)
    
    def test_same_color_gradient(self):
        """Test gradient with same start and end color."""
        gradient = LinearGradient.from_colors("#FF0000", "#FF0000")
        colors = gradient.generate(5)
        
        for color in colors:
            self.assertEqual(color, Color(255, 0, 0))
    
    def test_position_out_of_range(self):
        """Test position outside 0-1 range."""
        gradient = LinearGradient.from_colors("#000000", "#FFFFFF")
        
        # Should clamp to 0
        color = gradient.color_at(-10)
        self.assertEqual(color, Color(0, 0, 0))
        
        # Should clamp to 1
        color = gradient.color_at(10)
        self.assertEqual(color, Color(255, 255, 255))
    
    def test_unsorted_stops(self):
        """Test that stops are automatically sorted."""
        stops = [
            GradientStop(1, "#0000FF"),
            GradientStop(0, "#FF0000"),
            GradientStop(0.5, "#00FF00")
        ]
        gradient = LinearGradient(stops)
        
        # Should work correctly despite unsorted input
        color = gradient.color_at(0)
        self.assertEqual(color, Color(255, 0, 0))
        
        color = gradient.color_at(1)
        self.assertEqual(color, Color(0, 0, 255))


if __name__ == "__main__":
    unittest.main(verbosity=2)