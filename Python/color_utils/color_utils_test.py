#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Color Utilities Test Module
=========================================
Comprehensive tests for the color_utils module.

Author: AllToolkit Contributors
License: MIT
"""

import unittest
import math
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from color_utils.mod import (
    # Types
    Color,
    
    # Parsing
    parse_color, name_to_rgb, rgb_to_name,
    
    # Conversions
    rgb_to_hex, hex_to_rgb, rgb_to_hsl, hsl_to_rgb,
    rgb_to_hsv, hsv_to_rgb, rgb_to_cmyk, cmyk_to_rgb,
    rgb_to_lab, lab_to_rgb,
    
    # Manipulation
    lighten, darken, saturate, desaturate, grayscale,
    invert, rotate_hue, complement,
    
    # Mixing
    mix, blend_multiply, blend_screen, blend_overlay,
    
    # Comparison
    color_distance, color_distance_lab, calculate_luminance,
    contrast_ratio, wcag_rating,
    
    # Harmony
    complementary_palette, analogous_palette, triadic_palette,
    split_complementary_palette, tetradic_palette,
    
    # Palette generation
    random_color, random_palette, gradient_palette,
    monochromatic_palette, shades_palette, tints_palette,
    harmonious_palette,
    
    # Accessibility
    get_accessible_text_color, find_accessible_colors,
    
    # Utilities
    is_valid_hex, rgb_to_int, int_to_rgb,
    get_color_brightness, interpolate_color,
    temperature_to_rgb, css_gradient,
    
    # Convenience
    create_color, create_color_from_hex, create_color_from_name,
    
    # Data
    COLOR_NAMES,
)


class TestColorParsing(unittest.TestCase):
    """Tests for color parsing functions."""
    
    def test_parse_hex_with_hash(self):
        """Test parsing HEX colors with # prefix."""
        color = parse_color("#FF0000")
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 0)
        self.assertEqual(color.b, 0)
        self.assertEqual(color.a, 1.0)
    
    def test_parse_hex_without_hash(self):
        """Test parsing HEX colors without # prefix."""
        color = parse_color("FF0000")
        self.assertEqual(color.rgb, (255, 0, 0))
    
    def test_parse_hex_short(self):
        """Test parsing short HEX colors (#RGB)."""
        color = parse_color("#F00")
        self.assertEqual(color.rgb, (255, 0, 0))
        
        color = parse_color("#FFF")
        self.assertEqual(color.rgb, (255, 255, 255))
    
    def test_parse_rgb(self):
        """Test parsing rgb() format."""
        color = parse_color("rgb(255, 0, 0)")
        self.assertEqual(color.rgb, (255, 0, 0))
        
        color = parse_color("rgb(255,255,255)")
        self.assertEqual(color.rgb, (255, 255, 255))
    
    def test_parse_rgba(self):
        """Test parsing rgba() format."""
        color = parse_color("rgba(255, 0, 0, 0.5)")
        self.assertEqual(color.rgb, (255, 0, 0))
        self.assertAlmostEqual(color.a, 0.5)
    
    def test_parse_hsl(self):
        """Test parsing hsl() format."""
        color = parse_color("hsl(0, 100%, 50%)")
        self.assertEqual(color.rgb, (255, 0, 0))
    
    def test_parse_named_color(self):
        """Test parsing named colors."""
        color = parse_color("red")
        self.assertEqual(color.rgb, (255, 0, 0))
        
        color = parse_color("cornflowerblue")
        self.assertEqual(color.rgb, (100, 149, 237))
    
    def test_parse_invalid(self):
        """Test parsing invalid color strings."""
        with self.assertRaises(ValueError):
            parse_color("invalidcolor")
    
    def test_name_to_rgb(self):
        """Test name to RGB conversion."""
        self.assertEqual(name_to_rgb("red"), (255, 0, 0))
        self.assertEqual(name_to_rgb("blue"), (0, 0, 255))
        self.assertIsNone(name_to_rgb("notacolor"))
    
    def test_rgb_to_name(self):
        """Test RGB to name conversion."""
        self.assertEqual(rgb_to_name((255, 0, 0)), "red")
        self.assertEqual(rgb_to_name((0, 0, 255)), "blue")


class TestColorConversions(unittest.TestCase):
    """Tests for color format conversion functions."""
    
    def test_rgb_to_hex(self):
        """Test RGB to HEX conversion."""
        self.assertEqual(rgb_to_hex((255, 0, 0)), "#FF0000")
        self.assertEqual(rgb_to_hex((0, 255, 0)), "#00FF00")
        self.assertEqual(rgb_to_hex((0, 0, 255)), "#0000FF")
        
        # Without hash
        self.assertEqual(rgb_to_hex((255, 0, 0), False), "FF0000")
    
    def test_hex_to_rgb(self):
        """Test HEX to RGB conversion."""
        self.assertEqual(hex_to_rgb("#FF0000"), (255, 0, 0))
        self.assertEqual(hex_to_rgb("FF0000"), (255, 0, 0))
        self.assertEqual(hex_to_rgb("#F00"), (255, 0, 0))
    
    def test_rgb_to_hsl(self):
        """Test RGB to HSL conversion."""
        # Red
        hsl = rgb_to_hsl((255, 0, 0))
        self.assertEqual(hsl[0], 0)  # Hue
        self.assertEqual(hsl[1], 100)  # Saturation
        self.assertEqual(hsl[2], 50)  # Lightness
        
        # Gray
        hsl = rgb_to_hsl((128, 128, 128))
        self.assertEqual(hsl[1], 0)  # No saturation
    
    def test_hsl_to_rgb(self):
        """Test HSL to RGB conversion."""
        # Red
        rgb = hsl_to_rgb((0, 100, 50))
        self.assertEqual(rgb, (255, 0, 0))
        
        # White
        rgb = hsl_to_rgb((0, 0, 100))
        self.assertEqual(rgb, (255, 255, 255))
        
        # Black
        rgb = hsl_to_rgb((0, 0, 0))
        self.assertEqual(rgb, (0, 0, 0))
    
    def test_rgb_hsl_roundtrip(self):
        """Test RGB-HSL roundtrip conversion."""
        test_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
                       (255, 255, 0), (0, 255, 255), (255, 0, 255),
                       (128, 64, 32), (50, 100, 150)]
        
        for rgb in test_colors:
            hsl = rgb_to_hsl(rgb)
            rgb_back = hsl_to_rgb(hsl)
            self.assertEqual(rgb, rgb_back, f"Roundtrip failed for {rgb}")
    
    def test_rgb_to_hsv(self):
        """Test RGB to HSV conversion."""
        # Red
        hsv = rgb_to_hsv((255, 0, 0))
        self.assertEqual(hsv[0], 0)  # Hue
        self.assertEqual(hsv[1], 100)  # Saturation
        self.assertEqual(hsv[2], 100)  # Value
    
    def test_hsv_to_rgb(self):
        """Test HSV to RGB conversion."""
        # Red
        rgb = hsv_to_rgb((0, 100, 100))
        self.assertEqual(rgb, (255, 0, 0))
    
    def test_rgb_to_cmyk(self):
        """Test RGB to CMYK conversion."""
        # Black
        cmyk = rgb_to_cmyk((0, 0, 0))
        self.assertEqual(cmyk[3], 100)  # K = 100%
        
        # White
        cmyk = rgb_to_cmyk((255, 255, 255))
        self.assertEqual(cmyk[0], 0)  # All zeros
    
    def test_cmyk_to_rgb(self):
        """Test CMYK to RGB conversion."""
        # Black
        rgb = cmyk_to_rgb((0, 0, 0, 100))
        self.assertEqual(rgb, (0, 0, 0))
        
        # White
        rgb = cmyk_to_rgb((0, 0, 0, 0))
        self.assertEqual(rgb, (255, 255, 255))
    
    def test_rgb_to_lab(self):
        """Test RGB to LAB conversion."""
        # White
        lab = rgb_to_lab((255, 255, 255))
        self.assertAlmostEqual(lab[0], 100, places=1)  # L = 100
        
        # Black
        lab = rgb_to_lab((0, 0, 0))
        self.assertAlmostEqual(lab[0], 0, places=1)  # L = 0
    
    def test_lab_to_rgb(self):
        """Test LAB to RGB conversion."""
        # White
        rgb = lab_to_rgb((100, 0, 0))
        self.assertEqual(rgb, (255, 255, 255))
        
        # Black
        rgb = lab_to_rgb((0, 0, 0))
        self.assertEqual(rgb, (0, 0, 0))


class TestColorManipulation(unittest.TestCase):
    """Tests for color manipulation functions."""
    
    def test_lighten(self):
        """Test lightening colors."""
        # Lighten black
        lighter = lighten((0, 0, 0), 50)
        self.assertEqual(lighter, (128, 128, 128))
        
        # Lighten gray
        lighter = lighten((128, 128, 128), 25)
        self.assertEqual(lighter, (192, 192, 192))
    
    def test_darken(self):
        """Test darkening colors."""
        # Darken white
        darker = darken((255, 255, 255), 50)
        self.assertEqual(darker, (128, 128, 128))
        
        # Darken gray
        darker = darken((128, 128, 128), 25)
        self.assertEqual(darker, (64, 64, 64))
    
    def test_saturate(self):
        """Test saturating colors."""
        # Cannot fully saturate pure colors
        saturated = saturate((255, 0, 0), 50)
        self.assertEqual(saturated, (255, 0, 0))
    
    def test_desaturate(self):
        """Test desaturating colors."""
        # Desaturate red
        desaturated = desaturate((255, 0, 0), 100)
        self.assertEqual(desaturated, (128, 128, 128))
    
    def test_grayscale(self):
        """Test grayscale conversion."""
        gray = grayscale((255, 0, 0))
        self.assertEqual(gray[0], gray[1])
        self.assertEqual(gray[1], gray[2])
        
        # Verify different colors give different grays
        gray1 = grayscale((255, 0, 0))
        gray2 = grayscale((0, 255, 0))
        gray3 = grayscale((0, 0, 255))
        self.assertNotEqual(gray1, gray2)
        self.assertNotEqual(gray2, gray3)
    
    def test_invert(self):
        """Test color inversion."""
        # Invert red
        inverted = invert((255, 0, 0))
        self.assertEqual(inverted, (0, 255, 255))
        
        # Invert black
        inverted = invert((0, 0, 0))
        self.assertEqual(inverted, (255, 255, 255))
    
    def test_rotate_hue(self):
        """Test hue rotation."""
        # Rotate red 180 degrees -> cyan
        rotated = rotate_hue((255, 0, 0), 180)
        self.assertEqual(rotated, (0, 255, 255))
    
    def test_complement(self):
        """Test complementary color."""
        comp = complement((255, 0, 0))
        self.assertEqual(comp, (0, 255, 255))
        
        comp = complement((0, 255, 0))
        self.assertEqual(comp, (255, 0, 255))


class TestColorMixing(unittest.TestCase):
    """Tests for color mixing and blending functions."""
    
    def test_mix_equal(self):
        """Test equal mixing of colors."""
        # Mix red and blue -> purple
        mixed = mix((255, 0, 0), (0, 0, 255), 0.5)
        self.assertEqual(mixed, (128, 0, 128))
    
    def test_mix_unequal(self):
        """Test unequal mixing of colors."""
        # 75% red, 25% blue
        mixed = mix((255, 0, 0), (0, 0, 255), 0.25)
        self.assertEqual(mixed, (191, 0, 64))
    
    def test_blend_multiply(self):
        """Test multiply blend mode."""
        # White * gray = gray
        result = blend_multiply((255, 255, 255), (128, 128, 128))
        self.assertEqual(result, (128, 128, 128))
    
    def test_blend_screen(self):
        """Test screen blend mode."""
        # Black screen gray = gray
        result = blend_screen((0, 0, 0), (128, 128, 128))
        self.assertEqual(result, (128, 128, 128))
    
    def test_blend_overlay(self):
        """Test overlay blend mode."""
        # Gray overlay gray = gray
        result = blend_overlay((128, 128, 128), (128, 128, 128))
        self.assertEqual(result, (128, 128, 128))


class TestColorComparison(unittest.TestCase):
    """Tests for color comparison functions."""
    
    def test_color_distance(self):
        """Test Euclidean color distance."""
        # Same color = 0 distance
        dist = color_distance((255, 0, 0), (255, 0, 0))
        self.assertEqual(dist, 0)
        
        # Black to white = sqrt(3 * 255^2)
        dist = color_distance((0, 0, 0), (255, 255, 255))
        self.assertAlmostEqual(dist, 441.67, places=1)
    
    def test_color_distance_lab(self):
        """Test perceptual LAB color distance."""
        dist = color_distance_lab((255, 0, 0), (255, 0, 0))
        self.assertEqual(dist, 0)
    
    def test_calculate_luminance(self):
        """Test luminance calculation."""
        # White luminance = 1.0
        lum = calculate_luminance((255, 255, 255))
        self.assertAlmostEqual(lum, 1.0)
        
        # Black luminance = 0.0
        lum = calculate_luminance((0, 0, 0))
        self.assertAlmostEqual(lum, 0.0)
    
    def test_contrast_ratio(self):
        """Test contrast ratio calculation."""
        # Black/White = 21.0
        ratio = contrast_ratio((0, 0, 0), (255, 255, 255))
        self.assertAlmostEqual(ratio, 21.0)
        
        # Same color = 1.0
        ratio = contrast_ratio((128, 128, 128), (128, 128, 128))
        self.assertAlmostEqual(ratio, 1.0)
    
    def test_wcag_rating(self):
        """Test WCAG accessibility rating."""
        self.assertEqual(wcag_rating(7.0), "AAA")
        self.assertEqual(wcag_rating(4.5), "AA")
        self.assertEqual(wcag_rating(3.0), "AA Large")
        self.assertEqual(wcag_rating(2.0), "Fail")


class TestColorHarmony(unittest.TestCase):
    """Tests for color harmony functions."""
    
    def test_complementary_palette(self):
        """Test complementary palette."""
        palette = complementary_palette((255, 0, 0))
        self.assertEqual(len(palette), 2)
        self.assertEqual(palette[0], (255, 0, 0))
        self.assertEqual(palette[1], (0, 255, 255))
    
    def test_analogous_palette(self):
        """Test analogous palette."""
        palette = analogous_palette((255, 0, 0))
        self.assertEqual(len(palette), 3)
        self.assertEqual(palette[1], (255, 0, 0))
    
    def test_triadic_palette(self):
        """Test triadic palette."""
        palette = triadic_palette((255, 0, 0))
        self.assertEqual(len(palette), 3)
        
        # Verify 120-degree spacing
        h1 = rgb_to_hsl(palette[0])[0]
        h2 = rgb_to_hsl(palette[1])[0]
        h3 = rgb_to_hsl(palette[2])[0]
        
        self.assertAlmostEqual(abs(h2 - h1), 120, places=0)
        self.assertAlmostEqual(abs(h3 - h2), 120, places=0)
    
    def test_split_complementary_palette(self):
        """Test split-complementary palette."""
        palette = split_complementary_palette((255, 0, 0))
        self.assertEqual(len(palette), 3)
    
    def test_tetradic_palette(self):
        """Test tetradic palette."""
        palette = tetradic_palette((255, 0, 0))
        self.assertEqual(len(palette), 4)


class TestPaletteGeneration(unittest.TestCase):
    """Tests for palette generation functions."""
    
    def test_random_color(self):
        """Test random color generation."""
        color = random_color()
        self.assertIsInstance(color, tuple)
        self.assertEqual(len(color), 3)
        for c in color:
            self.assertGreaterEqual(c, 0)
            self.assertLessEqual(c, 255)
    
    def test_random_palette(self):
        """Test random palette generation."""
        palette = random_palette(5)
        self.assertEqual(len(palette), 5)
    
    def test_gradient_palette(self):
        """Test gradient palette generation."""
        palette = gradient_palette((255, 0, 0), (0, 0, 255), 5)
        self.assertEqual(len(palette), 5)
        
        # First should be start, last should be end
        self.assertEqual(palette[0], (255, 0, 0))
        self.assertEqual(palette[4], (0, 0, 255))
    
    def test_monochromatic_palette(self):
        """Test monochromatic palette generation."""
        palette = monochromatic_palette((255, 0, 0), 5)
        self.assertEqual(len(palette), 5)
        
        # All should have same hue
        for color in palette:
            h = rgb_to_hsl(color)[0]
            self.assertAlmostEqual(h, 0, places=0)
    
    def test_shades_palette(self):
        """Test shades palette generation."""
        palette = shades_palette((255, 0, 0), 5)
        self.assertEqual(len(palette), 5)
        self.assertEqual(palette[0], (255, 0, 0))
        
        # Each should be darker
        for i in range(1, len(palette)):
            self.assertLessEqual(palette[i][0], palette[i-1][0])
    
    def test_tints_palette(self):
        """Test tints palette generation."""
        palette = tints_palette((255, 0, 0), 5)
        self.assertEqual(len(palette), 5)
        self.assertEqual(palette[0], (255, 0, 0))
        
        # Each should be lighter
        for i in range(1, len(palette)):
            self.assertGreaterEqual(palette[i][0], palette[i-1][0])
    
    def test_harmonious_palette(self):
        """Test harmonious palette generation."""
        for harmony in ['complementary', 'analogous', 'triadic', 
                        'split-complementary', 'tetradic', 'monochromatic']:
            palette = harmonious_palette((255, 0, 0), harmony)
            self.assertGreater(len(palette), 0)


class TestAccessibility(unittest.TestCase):
    """Tests for accessibility helper functions."""
    
    def test_get_accessible_text_color(self):
        """Test accessible text color selection."""
        # Black background -> white text
        text_color = get_accessible_text_color((0, 0, 0))
        self.assertEqual(text_color, (255, 255, 255))
        
        # White background -> black text
        text_color = get_accessible_text_color((255, 255, 255))
        self.assertEqual(text_color, (0, 0, 0))
    
    def test_find_accessible_colors(self):
        """Test finding accessible colors."""
        colors = find_accessible_colors((128, 128, 128), 5)
        self.assertGreater(len(colors), 0)
        
        # Verify all meet contrast requirement
        for color in colors:
            ratio = contrast_ratio((128, 128, 128), color)
            self.assertGreaterEqual(ratio, 4.5)


class TestUtilityFunctions(unittest.TestCase):
    """Tests for utility functions."""
    
    def test_is_valid_hex(self):
        """Test HEX validation."""
        self.assertTrue(is_valid_hex("#FF0000"))
        self.assertTrue(is_valid_hex("FF0000"))
        self.assertTrue(is_valid_hex("#F00"))
        self.assertTrue(is_valid_hex("F00"))
        self.assertFalse(is_valid_hex("FF"))
        self.assertFalse(is_valid_hex("invalid"))
    
    def test_rgb_to_int(self):
        """Test RGB to integer conversion."""
        self.assertEqual(rgb_to_int((255, 0, 0)), 16711680)
        self.assertEqual(rgb_to_int((0, 255, 0)), 65280)
        self.assertEqual(rgb_to_int((0, 0, 255)), 255)
    
    def test_int_to_rgb(self):
        """Test integer to RGB conversion."""
        self.assertEqual(int_to_rgb(16711680), (255, 0, 0))
        self.assertEqual(int_to_rgb(65280), (0, 255, 0))
        self.assertEqual(int_to_rgb(255), (0, 0, 255))
    
    def test_get_color_brightness(self):
        """Test color brightness calculation."""
        # White = max brightness
        brightness = get_color_brightness((255, 255, 255))
        self.assertEqual(brightness, 255)
        
        # Black = min brightness
        brightness = get_color_brightness((0, 0, 0))
        self.assertEqual(brightness, 0)
    
    def test_interpolate_color(self):
        """Test color interpolation."""
        # 50% between red and blue
        result = interpolate_color((255, 0, 0), (0, 0, 255), 0.5)
        self.assertEqual(result, (128, 0, 128))
        
        # 0% = start color
        result = interpolate_color((255, 0, 0), (0, 0, 255), 0)
        self.assertEqual(result, (255, 0, 0))
        
        # 100% = end color
        result = interpolate_color((255, 0, 0), (0, 0, 255), 1)
        self.assertEqual(result, (0, 0, 255))
    
    def test_temperature_to_rgb(self):
        """Test color temperature to RGB conversion."""
        # Warm light (2700K)
        warm = temperature_to_rgb(2700)
        self.assertGreater(warm[0], warm[2])  # More red than blue
        
        # Cool daylight (6500K)
        cool = temperature_to_rgb(6500)
        self.assertGreater(cool[2], 0)  # Has some blue
    
    def test_css_gradient(self):
        """Test CSS gradient generation."""
        gradient = css_gradient([(255, 0, 0), (0, 0, 255)])
        self.assertIn("linear-gradient", gradient)
        self.assertIn("#FF0000", gradient)
        self.assertIn("#0000FF", gradient)


class TestColorClass(unittest.TestCase):
    """Tests for Color class."""
    
    def test_color_creation(self):
        """Test Color object creation."""
        color = Color(255, 0, 0)
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 0)
        self.assertEqual(color.b, 0)
        self.assertEqual(color.a, 1.0)
    
    def test_color_validation(self):
        """Test Color value validation/clamping."""
        # Values out of range should be clamped
        color = Color(300, -10, 128)
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 0)
        self.assertEqual(color.b, 128)
    
    def test_color_properties(self):
        """Test Color properties."""
        color = Color(255, 0, 0)
        
        self.assertEqual(color.rgb, (255, 0, 0))
        self.assertEqual(color.hex, "FF0000")
        self.assertEqual(color.hex_with_hash, "#FF0000")
        
        hsl = color.hsl
        self.assertEqual(hsl[0], 0)
        self.assertEqual(hsl[1], 100)
        self.assertEqual(hsl[2], 50)
    
    def test_color_luminance(self):
        """Test Color luminance property."""
        white = Color(255, 255, 255)
        self.assertAlmostEqual(white.luminance, 1.0)
        
        black = Color(0, 0, 0)
        self.assertAlmostEqual(black.luminance, 0.0)
    
    def test_color_is_light_is_dark(self):
        """Test Color is_light/is_dark properties."""
        white = Color(255, 255, 255)
        self.assertTrue(white.is_light)
        self.assertFalse(white.is_dark)
        
        black = Color(0, 0, 0)
        self.assertFalse(black.is_light)
        self.assertTrue(black.is_dark)
    
    def test_color_str_repr(self):
        """Test Color string representation."""
        color = Color(255, 0, 0)
        self.assertEqual(str(color), "#FF0000")
        
        # With alpha
        color = Color(255, 0, 0, 0.5)
        self.assertIn("rgba", str(color))
    
    def test_create_color(self):
        """Test create_color convenience function."""
        color = create_color(255, 0, 0)
        self.assertEqual(color.rgb, (255, 0, 0))
    
    def test_create_color_from_hex(self):
        """Test create_color_from_hex convenience function."""
        color = create_color_from_hex("#FF0000")
        self.assertEqual(color.rgb, (255, 0, 0))
    
    def test_create_color_from_name(self):
        """Test create_color_from_name convenience function."""
        color = create_color_from_name("red")
        self.assertEqual(color.rgb, (255, 0, 0))
        
        # Invalid name
        color = create_color_from_name("notacolor")
        self.assertIsNone(color)


class TestColorNames(unittest.TestCase):
    """Tests for color name dictionary."""
    
    def test_basic_colors_exist(self):
        """Test basic colors exist in dictionary."""
        basic_colors = ['black', 'white', 'red', 'green', 'blue',
                        'yellow', 'cyan', 'magenta']
        for name in basic_colors:
            self.assertIn(name, COLOR_NAMES)
    
    def test_color_count(self):
        """Test color dictionary has reasonable count."""
        # Should have at least 100 named colors
        self.assertGreater(len(COLOR_NAMES), 100)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestColorParsing))
    suite.addTests(loader.loadTestsFromTestCase(TestColorConversions))
    suite.addTests(loader.loadTestsFromTestCase(TestColorManipulation))
    suite.addTests(loader.loadTestsFromTestCase(TestColorMixing))
    suite.addTests(loader.loadTestsFromTestCase(TestColorComparison))
    suite.addTests(loader.loadTestsFromTestCase(TestColorHarmony))
    suite.addTests(loader.loadTestsFromTestCase(TestPaletteGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestAccessibility))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestColorClass))
    suite.addTests(loader.loadTestsFromTestCase(TestColorNames))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)