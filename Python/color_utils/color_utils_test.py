#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Color Utilities Test Suite
=========================================
Comprehensive tests for color_utils module.

Run with: python -m pytest color_utils_test.py -v
Or directly: python color_utils_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Data classes
    RGB, HSL, ColorInfo,
    
    # Validation and parsing
    is_valid_hex, parse_hex, parse_rgb_string, parse_color, get_color_name,
    
    # Color conversions
    rgb_to_hex, hex_to_rgb, rgb_to_hsl, hsl_to_rgb, rgb_to_hsv, hsv_to_rgb,
    rgb_to_cmyk, cmyk_to_rgb, rgb_to_lab, lab_to_rgb,
    
    # Color analysis
    get_luminance, get_contrast_ratio, get_wcag_level, get_perceived_brightness,
    is_light_color, get_color_temperature,
    
    # Color manipulation
    lighten, darken, saturate, desaturate, grayscale, invert, complement,
    mix_colors, blend_colors,
    
    # Color distance
    color_distance, color_distance_lab, are_colors_similar,
    
    # Color harmony
    get_complementary, get_analogous, get_triadic, get_split_complementary,
    get_tetradic, get_square,
    
    # Palette generation
    generate_shades, generate_tints, generate_tones, generate_palette,
    generate_gradient, generate_random_palette,
    
    # Comprehensive info
    get_color_info,
    
    # Constants
    CSS_COLORS
)

import unittest


class TestColorValidation(unittest.TestCase):
    """Test color validation functions."""
    
    def test_is_valid_hex_valid(self):
        """Test valid HEX colors."""
        valid_hex = [
            '#FF0000',
            'FF0000',
            '#F00',
            'F00',
            '#ffffff',
            'FFFFFF',
            '#abc',
            'ABC',
            '#000000',
            '000000',
        ]
        for hex_color in valid_hex:
            with self.subTest(hex=hex_color):
                self.assertTrue(is_valid_hex(hex_color))
    
    def test_is_valid_hex_invalid(self):
        """Test invalid HEX colors."""
        invalid_hex = [
            '#FF',
            'FF',
            '#FFFF',
            'FFFF',
            '#FFFFFFF',
            'FFFFFFF',
            'invalid',
            '#GGGGGG',
            '#FF-000',
            '',
            None,
            '#',
            '#FF00',
            'FF00',
        ]
        for hex_color in invalid_hex:
            with self.subTest(hex=hex_color):
                self.assertFalse(is_valid_hex(hex_color))
    
    def test_parse_hex_6_digit(self):
        """Test parsing 6-digit HEX."""
        result = parse_hex('#FF0000')
        self.assertEqual(result.r, 255)
        self.assertEqual(result.g, 0)
        self.assertEqual(result.b, 0)
        
        result = parse_hex('FF0000')
        self.assertEqual(result.r, 255)
        self.assertEqual(result.g, 0)
        self.assertEqual(result.b, 0)
    
    def test_parse_hex_3_digit(self):
        """Test parsing 3-digit HEX."""
        result = parse_hex('#F00')
        self.assertEqual(result.r, 255)
        self.assertEqual(result.g, 0)
        self.assertEqual(result.b, 0)
        
        result = parse_hex('#FFF')
        self.assertEqual(result.r, 255)
        self.assertEqual(result.g, 255)
        self.assertEqual(result.b, 255)
    
    def test_parse_hex_invalid(self):
        """Test parsing invalid HEX."""
        with self.assertRaises(ValueError):
            parse_hex('invalid')
        with self.assertRaises(ValueError):
            parse_hex('#FF')
    
    def test_parse_rgb_string(self):
        """Test parsing RGB strings."""
        result = parse_rgb_string('rgb(255, 0, 0)')
        self.assertEqual(result.r, 255)
        self.assertEqual(result.g, 0)
        self.assertEqual(result.b, 0)
        
        result = parse_rgb_string('255, 0, 0')
        self.assertEqual(result.r, 255)
        self.assertEqual(result.g, 0)
        self.assertEqual(result.b, 0)
    
    def test_parse_color_various_formats(self):
        """Test parsing colors in various formats."""
        # HEX
        result = parse_color('#FF0000')
        self.assertEqual(result.r, 255)
        
        # Tuple
        result = parse_color((255, 0, 0))
        self.assertEqual(result.r, 255)
        
        # RGB object
        rgb = RGB(255, 0, 0)
        result = parse_color(rgb)
        self.assertEqual(result.r, 255)
        
        # Named color
        result = parse_color('red')
        self.assertEqual(result.r, 255)
        self.assertEqual(result.g, 0)
        self.assertEqual(result.b, 0)
        
        result = parse_color('white')
        self.assertEqual(result.r, 255)
        self.assertEqual(result.g, 255)
        self.assertEqual(result.b, 255)
    
    def test_get_color_name(self):
        """Test getting color name."""
        self.assertEqual(get_color_name((255, 0, 0)), 'red')
        self.assertEqual(get_color_name((255, 255, 255)), 'white')
        self.assertEqual(get_color_name((0, 0, 0)), 'black')


class TestRGB(unittest.TestCase):
    """Test RGB dataclass."""
    
    def test_rgb_creation(self):
        """Test RGB creation."""
        rgb = RGB(255, 128, 0)
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 128)
        self.assertEqual(rgb.b, 0)
    
    def test_rgb_clamping(self):
        """Test RGB value clamping."""
        rgb = RGB(300, -10, 128)
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 0)
        self.assertEqual(rgb.b, 128)
    
    def test_rgb_to_hex(self):
        """Test RGB to HEX conversion."""
        rgb = RGB(255, 128, 0)
        self.assertEqual(rgb.to_hex(), '#ff8000')
    
    def test_rgb_to_hsl(self):
        """Test RGB to HSL conversion."""
        rgb = RGB(255, 0, 0)
        h, s, l = rgb.to_hsl()
        self.assertEqual(h, 0.0)
        self.assertEqual(s, 100.0)
        self.assertEqual(l, 50.0)
    
    def test_rgb_to_tuple(self):
        """Test RGB to tuple conversion."""
        rgb = RGB(255, 128, 0)
        self.assertEqual(rgb.to_tuple(), (255, 128, 0))


class TestColorConversions(unittest.TestCase):
    """Test color conversion functions."""
    
    def test_rgb_to_hex(self):
        """Test RGB to HEX conversion."""
        self.assertEqual(rgb_to_hex(255, 0, 0), '#ff0000')
        self.assertEqual(rgb_to_hex(0, 255, 0), '#00ff00')
        self.assertEqual(rgb_to_hex(0, 0, 255), '#0000ff')
        self.assertEqual(rgb_to_hex(255, 255, 255), '#ffffff')
        self.assertEqual(rgb_to_hex(0, 0, 0), '#000000')
    
    def test_hex_to_rgb(self):
        """Test HEX to RGB conversion."""
        self.assertEqual(hex_to_rgb('#FF0000'), (255, 0, 0))
        self.assertEqual(hex_to_rgb('#00FF00'), (0, 255, 0))
        self.assertEqual(hex_to_rgb('#0000FF'), (0, 0, 255))
    
    def test_rgb_hex_roundtrip(self):
        """Test RGB <-> HEX roundtrip."""
        test_colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (128, 128, 128),
            (255, 255, 255),
            (0, 0, 0),
        ]
        for r, g, b in test_colors:
            with self.subTest(color=(r, g, b)):
                hex_color = rgb_to_hex(r, g, b)
                result = hex_to_rgb(hex_color)
                self.assertEqual(result, (r, g, b))
    
    def test_rgb_to_hsl(self):
        """Test RGB to HSL conversion."""
        # Red
        h, s, l = rgb_to_hsl(255, 0, 0)
        self.assertEqual(h, 0.0)
        self.assertEqual(s, 100.0)
        self.assertEqual(l, 50.0)
        
        # Green
        h, s, l = rgb_to_hsl(0, 255, 0)
        self.assertEqual(h, 120.0)
        self.assertEqual(s, 100.0)
        self.assertEqual(l, 50.0)
        
        # Blue
        h, s, l = rgb_to_hsl(0, 0, 255)
        self.assertEqual(h, 240.0)
        self.assertEqual(s, 100.0)
        self.assertEqual(l, 50.0)
        
        # White
        h, s, l = rgb_to_hsl(255, 255, 255)
        self.assertEqual(s, 0.0)
        self.assertEqual(l, 100.0)
        
        # Black
        h, s, l = rgb_to_hsl(0, 0, 0)
        self.assertEqual(s, 0.0)
        self.assertEqual(l, 0.0)
    
    def test_hsl_to_rgb(self):
        """Test HSL to RGB conversion."""
        # Red
        self.assertEqual(hsl_to_rgb(0, 100, 50), (255, 0, 0))
        
        # Green
        self.assertEqual(hsl_to_rgb(120, 100, 50), (0, 255, 0))
        
        # Blue
        self.assertEqual(hsl_to_rgb(240, 100, 50), (0, 0, 255))
        
        # White
        r, g, b = hsl_to_rgb(0, 0, 100)
        self.assertEqual(r, 255)
        self.assertEqual(g, 255)
        self.assertEqual(b, 255)
        
        # Black
        r, g, b = hsl_to_rgb(0, 0, 0)
        self.assertEqual(r, 0)
        self.assertEqual(g, 0)
        self.assertEqual(b, 0)
    
    def test_rgb_hsl_roundtrip(self):
        """Test RGB <-> HSL roundtrip."""
        test_colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (128, 128, 128),
            (255, 255, 255),
            (0, 0, 0),
        ]
        for r, g, b in test_colors:
            with self.subTest(color=(r, g, b)):
                h, s, l = rgb_to_hsl(r, g, b)
                result = hsl_to_rgb(h, s, l)
                self.assertEqual(result, (r, g, b))
    
    def test_rgb_to_hsv(self):
        """Test RGB to HSV conversion."""
        # Red
        h, s, v = rgb_to_hsv(255, 0, 0)
        self.assertEqual(h, 0.0)
        self.assertEqual(s, 100.0)
        self.assertEqual(v, 100.0)
        
        # White
        h, s, v = rgb_to_hsv(255, 255, 255)
        self.assertEqual(s, 0.0)
        self.assertEqual(v, 100.0)
    
    def test_hsv_to_rgb(self):
        """Test HSV to RGB conversion."""
        # Red
        self.assertEqual(hsv_to_rgb(0, 100, 100), (255, 0, 0))
        
        # Green
        self.assertEqual(hsv_to_rgb(120, 100, 100), (0, 255, 0))
    
    def test_rgb_to_cmyk(self):
        """Test RGB to CMYK conversion."""
        # White
        c, m, y, k = rgb_to_cmyk(255, 255, 255)
        self.assertEqual(c, 0.0)
        self.assertEqual(m, 0.0)
        self.assertEqual(y, 0.0)
        self.assertEqual(k, 0.0)
        
        # Black
        c, m, y, k = rgb_to_cmyk(0, 0, 0)
        self.assertEqual(c, 0.0)
        self.assertEqual(m, 0.0)
        self.assertEqual(y, 0.0)
        self.assertEqual(k, 100.0)
    
    def test_cmyk_to_rgb(self):
        """Test CMYK to RGB conversion."""
        # White
        self.assertEqual(cmyk_to_rgb(0, 0, 0, 0), (255, 255, 255))
        
        # Black
        self.assertEqual(cmyk_to_rgb(0, 0, 0, 100), (0, 0, 0))
    
    def test_rgb_to_lab(self):
        """Test RGB to LAB conversion."""
        # White
        L, a, b = rgb_to_lab(255, 255, 255)
        self.assertAlmostEqual(L, 100.0, places=1)
        self.assertAlmostEqual(a, 0.0, places=1)
        self.assertAlmostEqual(b, 0.0, places=1)
        
        # Black
        L, a, b = rgb_to_lab(0, 0, 0)
        self.assertAlmostEqual(L, 0.0, places=1)
    
    def test_lab_to_rgb(self):
        """Test LAB to RGB conversion."""
        # White
        r, g, b = lab_to_rgb(100, 0, 0)
        self.assertEqual(r, 255)
        self.assertEqual(g, 255)
        self.assertEqual(b, 255)
        
        # Black
        r, g, b = lab_to_rgb(0, 0, 0)
        self.assertEqual(r, 0)
        self.assertEqual(g, 0)
        self.assertEqual(b, 0)


class TestColorAnalysis(unittest.TestCase):
    """Test color analysis functions."""
    
    def test_get_luminance(self):
        """Test luminance calculation."""
        self.assertEqual(get_luminance('#FFFFFF'), 1.0)
        self.assertEqual(get_luminance('#000000'), 0.0)
        self.assertAlmostEqual(get_luminance('#FF0000'), 0.2126, places=3)
    
    def test_get_contrast_ratio(self):
        """Test contrast ratio calculation."""
        self.assertEqual(get_contrast_ratio('#FFFFFF', '#000000'), 21.0)
        # Allow for slight variation in contrast ratio
        ratio = get_contrast_ratio('#FFFFFF', '#777777')
        self.assertTrue(4.4 <= ratio <= 4.7)
    
    def test_get_wcag_level(self):
        """Test WCAG level determination."""
        # Perfect contrast
        level = get_wcag_level(21.0)
        self.assertEqual(level['AA_normal'], 'Pass')
        self.assertEqual(level['AAA_normal'], 'Pass')
        
        # Good contrast
        level = get_wcag_level(7.0)
        self.assertEqual(level['AA_normal'], 'Pass')
        self.assertEqual(level['AAA_normal'], 'Pass')
        
        # Moderate contrast
        level = get_wcag_level(4.5)
        self.assertEqual(level['AA_normal'], 'Pass')
        self.assertEqual(level['AAA_normal'], 'Fail')
        
        # Poor contrast
        level = get_wcag_level(2.0)
        self.assertEqual(level['AA_normal'], 'Fail')
        self.assertEqual(level['AA_large'], 'Fail')
    
    def test_get_perceived_brightness(self):
        """Test perceived brightness calculation."""
        self.assertAlmostEqual(get_perceived_brightness('#FFFFFF'), 255.0, places=1)
        self.assertAlmostEqual(get_perceived_brightness('#000000'), 0.0, places=1)
    
    def test_is_light_color(self):
        """Test light color detection."""
        self.assertTrue(is_light_color('#FFFFFF'))
        self.assertTrue(is_light_color('#CCCCCC'))
        self.assertFalse(is_light_color('#000000'))
        self.assertFalse(is_light_color('#333333'))
    
    def test_get_color_temperature(self):
        """Test color temperature detection."""
        self.assertEqual(get_color_temperature('#FF0000'), 'warm')
        self.assertEqual(get_color_temperature('#FF8000'), 'warm')
        self.assertEqual(get_color_temperature('#0000FF'), 'cool')
        self.assertEqual(get_color_temperature('#00FFFF'), 'cool')
        self.assertEqual(get_color_temperature('#808080'), 'neutral')


class TestColorManipulation(unittest.TestCase):
    """Test color manipulation functions."""
    
    def test_lighten(self):
        """Test lightening colors."""
        result = lighten('#FF0000', 20)
        h, s, l = rgb_to_hsl(result.r, result.g, result.b)
        self.assertEqual(h, 0.0)
        self.assertEqual(l, 70.0)
    
    def test_darken(self):
        """Test darkening colors."""
        result = darken('#FF0000', 20)
        h, s, l = rgb_to_hsl(result.r, result.g, result.b)
        self.assertEqual(h, 0.0)
        self.assertEqual(l, 30.0)
    
    def test_saturate(self):
        """Test saturating colors."""
        result = saturate('#CC3333', 20)
        h, s, l = rgb_to_hsl(result.r, result.g, result.b)
        # Due to RGB-HSL roundtrip, allow for slight precision loss
        self.assertTrue(s >= 80.0)  # Should be more saturated than original
    
    def test_desaturate(self):
        """Test desaturating colors."""
        result = desaturate('#FF0000', 50)
        h, s, l = rgb_to_hsl(result.r, result.g, result.b)
        # Due to RGB-HSL roundtrip, allow for precision loss (around 50%)
        self.assertTrue(abs(s - 50.0) < 1.0)
    
    def test_grayscale(self):
        """Test grayscale conversion."""
        result = grayscale('#FF0000')
        h, s, l = rgb_to_hsl(result.r, result.g, result.b)
        self.assertEqual(s, 0.0)
    
    def test_invert(self):
        """Test color inversion."""
        self.assertEqual(invert('#FFFFFF'), RGB(0, 0, 0))
        self.assertEqual(invert('#000000'), RGB(255, 255, 255))
        self.assertEqual(invert('#FF0000'), RGB(0, 255, 255))
    
    def test_complement(self):
        """Test complementary color."""
        result = complement('#FF0000')
        h, s, l = rgb_to_hsl(result.r, result.g, result.b)
        self.assertEqual(h, 180.0)
    
    def test_mix_colors_equal(self):
        """Test mixing colors equally."""
        result = mix_colors('#FF0000', '#0000FF', 0.5)
        self.assertEqual(result.r, 128)
        self.assertEqual(result.g, 0)
        self.assertEqual(result.b, 128)
    
    def test_mix_colors_unequal(self):
        """Test mixing colors with different weights."""
        result = mix_colors('#FF0000', '#0000FF', 0.75)
        # Allow for rounding differences
        self.assertTrue(abs(result.r - 192) <= 1)
        self.assertTrue(abs(result.b - 64) <= 1)
    
    def test_blend_colors(self):
        """Test blending multiple colors."""
        result = blend_colors(['#FF0000', '#00FF00', '#0000FF'])
        self.assertEqual(result.r, 85)
        self.assertEqual(result.g, 85)
        self.assertEqual(result.b, 85)


class TestColorDistance(unittest.TestCase):
    """Test color distance functions."""
    
    def test_color_distance_rgb(self):
        """Test RGB distance calculation."""
        # Same color
        self.assertEqual(color_distance('#FF0000', '#FF0000'), 0.0)
        
        # Black to white
        self.assertAlmostEqual(color_distance('#000000', '#FFFFFF'), 441.67, places=2)
        
        # Red to blue
        self.assertAlmostEqual(color_distance('#FF0000', '#0000FF'), 360.62, places=2)
    
    def test_color_distance_lab(self):
        """Test LAB distance calculation."""
        # Same color
        self.assertEqual(color_distance_lab('#FF0000', '#FF0000'), 0.0)
        
        # Should be more perceptual than RGB
        dist = color_distance_lab('#FF0000', '#00FF00')
        self.assertTrue(dist > 0)
    
    def test_are_colors_similar(self):
        """Test color similarity check."""
        self.assertTrue(are_colors_similar('#FF0000', '#FF0101', threshold=5))
        self.assertFalse(are_colors_similar('#FF0000', '#00FF00', threshold=10))


class TestColorHarmony(unittest.TestCase):
    """Test color harmony functions."""
    
    def test_get_complementary(self):
        """Test complementary color."""
        result = get_complementary('#FF0000')
        h, s, l = rgb_to_hsl(result.r, result.g, result.b)
        self.assertEqual(h, 180.0)
    
    def test_get_analogous(self):
        """Test analogous colors."""
        analogous = get_analogous('#FF0000')
        self.assertEqual(len(analogous), 2)
    
    def test_get_triadic(self):
        """Test triadic colors."""
        triadic = get_triadic('#FF0000')
        self.assertEqual(len(triadic), 2)
        
        # Triadic colors should be 120 degrees apart
        for color in triadic:
            h, s, l = rgb_to_hsl(color.r, color.g, color.b)
            self.assertIn(h, [120.0, 240.0])
    
    def test_get_split_complementary(self):
        """Test split-complementary colors."""
        split = get_split_complementary('#FF0000')
        self.assertEqual(len(split), 2)
    
    def test_get_tetradic(self):
        """Test tetradic colors."""
        tetradic = get_tetradic('#FF0000')
        self.assertEqual(len(tetradic), 3)


class TestPaletteGeneration(unittest.TestCase):
    """Test palette generation functions."""
    
    def test_generate_shades(self):
        """Test shade generation."""
        shades = generate_shades('#FF0000', 5)
        self.assertEqual(len(shades), 5)
        
        # First should be original color
        self.assertEqual(shades[0].r, 255)
        
        # Each shade should be darker
        prev_l = rgb_to_hsl(shades[0].r, shades[0].g, shades[0].b)[2]
        for shade in shades[1:]:
            curr_l = rgb_to_hsl(shade.r, shade.g, shade.b)[2]
            self.assertTrue(curr_l <= prev_l)
            prev_l = curr_l
    
    def test_generate_tints(self):
        """Test tint generation."""
        tints = generate_tints('#FF0000', 5)
        self.assertEqual(len(tints), 5)
        
        # First should be original color
        self.assertEqual(tints[0].r, 255)
        
        # Each tint should be lighter
        prev_l = rgb_to_hsl(tints[0].r, tints[0].g, tints[0].b)[2]
        for tint in tints[1:]:
            curr_l = rgb_to_hsl(tint.r, tint.g, tint.b)[2]
            self.assertTrue(curr_l >= prev_l)
            prev_l = curr_l
    
    def test_generate_tones(self):
        """Test tone generation."""
        tones = generate_tones('#FF0000', 5)
        self.assertEqual(len(tones), 5)
    
    def test_generate_gradient(self):
        """Test gradient generation."""
        gradient = generate_gradient('#FF0000', '#0000FF', 5)
        self.assertEqual(len(gradient), 5)
        
        # First should be start color
        self.assertEqual(gradient[0].r, 255)
        
        # Last should be end color
        self.assertEqual(gradient[4].b, 255)
    
    def test_generate_random_palette(self):
        """Test random palette generation."""
        palette = generate_random_palette(5)
        self.assertEqual(len(palette), 5)
        
        for color in palette:
            self.assertTrue(0 <= color.r <= 255)
            self.assertTrue(0 <= color.g <= 255)
            self.assertTrue(0 <= color.b <= 255)
    
    def test_generate_palette_types(self):
        """Test different palette types."""
        for palette_type in ['shades', 'tints', 'tones', 'analogous', 'complementary']:
            with self.subTest(type=palette_type):
                palette = generate_palette('#FF0000', 5, palette_type)
                self.assertEqual(len(palette), 5)


class TestColorInfo(unittest.TestCase):
    """Test comprehensive color info."""
    
    def test_get_color_info(self):
        """Test get_color_info function."""
        info = get_color_info('#FF0000')
        
        self.assertEqual(info.hex, '#ff0000')
        self.assertEqual(info.rgb.r, 255)
        self.assertEqual(info.rgb.g, 0)
        self.assertEqual(info.rgb.b, 0)
        
        self.assertEqual(info.hsl.h, 0.0)
        self.assertEqual(info.hsl.s, 100.0)
        self.assertEqual(info.hsl.l, 50.0)
        
        self.assertEqual(info.name, 'red')
        self.assertEqual(info.temperature, 'warm')
        self.assertTrue(info.luminance > 0.2)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_rgb_boundary_values(self):
        """Test RGB boundary values."""
        # Max values
        rgb = RGB(255, 255, 255)
        self.assertEqual(rgb.r, 255)
        
        # Min values
        rgb = RGB(0, 0, 0)
        self.assertEqual(rgb.r, 0)
        
        # Out of range values (should clamp)
        rgb = RGB(-1, 256, 300)
        self.assertEqual(rgb.r, 0)
        self.assertEqual(rgb.g, 255)
        self.assertEqual(rgb.b, 255)
    
    def test_hsl_boundary_values(self):
        """Test HSL boundary values."""
        # Hue wrapping
        hsl = HSL(370, 50, 50)
        self.assertEqual(hsl.h, 10)
        
        # Saturation clamping
        hsl = HSL(180, 150, 50)
        self.assertEqual(hsl.s, 100)
        
        hsl = HSL(180, -10, 50)
        self.assertEqual(hsl.s, 0)
    
    def test_empty_blend_colors(self):
        """Test blending empty color list."""
        with self.assertRaises(ValueError):
            blend_colors([])
    
    def test_mix_colors_extreme_weights(self):
        """Test mixing with extreme weights."""
        # Weight 0 (all second color)
        result = mix_colors('#FF0000', '#0000FF', 0.0)
        self.assertEqual(result.b, 255)
        
        # Weight 1 (all first color)
        result = mix_colors('#FF0000', '#0000FF', 1.0)
        self.assertEqual(result.r, 255)
    
    def test_gradient_single_step(self):
        """Test gradient with single step."""
        gradient = generate_gradient('#FF0000', '#0000FF', 1)
        self.assertEqual(len(gradient), 1)
    
    def test_named_colors_lookup(self):
        """Test named color lookup."""
        # Standard colors
        self.assertIn('red', CSS_COLORS)
        self.assertIn('blue', CSS_COLORS)
        self.assertIn('green', CSS_COLORS)
        
        # Aliases
        self.assertIn('gray', CSS_COLORS)
        self.assertIn('grey', CSS_COLORS)


if __name__ == '__main__':
    unittest.main(verbosity=2)