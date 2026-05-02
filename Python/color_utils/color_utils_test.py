#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Color Utilities Test Suite
========================================
Comprehensive tests for the color_utils module.

Run with: python color_utils_test.py
"""

import sys
import os
import unittest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from color_utils.mod import (
    RGB, HSL, HSV, CMYK,
    parse_hex, parse_rgb, parse_hsl, parse_color,
    color_name_to_rgb, rgb_to_color_name,
    rgb_to_hex, hex_to_rgb,
    rgb_to_hsl, hsl_to_rgb,
    rgb_to_hsv, hsv_to_rgb,
    rgb_to_cmyk, cmyk_to_rgb,
    lighten, darken, saturate, desaturate,
    grayscale, invert, complement, mix, blend,
    analogous, triadic, split_complement, tetradic, monochromatic,
    luminance, contrast_ratio, wcag_rating,
    brightness, is_light, is_dark, text_color_for_bg,
    color_distance, closest_color,
    gradient, multi_gradient,
    random_color, random_hue, random_pastel,
    CSS_COLORS
)


class TestColorDataClasses(unittest.TestCase):
    """Test color data classes."""
    
    def test_rgb_creation(self):
        """Test RGB creation and validation."""
        rgb = RGB(255, 128, 64)
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 128)
        self.assertEqual(rgb.b, 64)
        self.assertEqual(rgb.a, 1.0)
    
    def test_rgb_validation_clamping(self):
        """Test RGB value clamping."""
        rgb = RGB(300, -10, 500)
        self.assertEqual(rgb.r, 255)  # Clamped
        self.assertEqual(rgb.g, 0)    # Clamped
        self.assertEqual(rgb.b, 255)  # Clamped
    
    def test_rgb_alpha_validation(self):
        """Test RGB alpha validation."""
        rgb = RGB(100, 100, 100, 2.0)
        self.assertEqual(rgb.a, 1.0)  # Clamped
        
        rgb = RGB(100, 100, 100, -0.5)
        self.assertEqual(rgb.a, 0.0)  # Clamped
    
    def test_rgb_to_hex(self):
        """Test RGB to hex conversion."""
        rgb = RGB(255, 0, 0)
        self.assertEqual(rgb.to_hex(), '#ff0000')
        
        rgb = RGB(255, 0, 0, 0.5)
        self.assertEqual(rgb.to_hex(include_alpha=True), '#ff000080')
    
    def test_rgb_to_hsl(self):
        """Test RGB to HSL conversion."""
        rgb = RGB(255, 0, 0)
        hsl = rgb.to_hsl()
        self.assertEqual(hsl.h, 0)
        self.assertEqual(hsl.s, 100)
        self.assertEqual(hsl.l, 50)
    
    def test_hsl_creation(self):
        """Test HSL creation and validation."""
        hsl = HSL(120, 50, 75)
        self.assertEqual(hsl.h, 120)
        self.assertEqual(hsl.s, 50)
        self.assertEqual(hsl.l, 75)
    
    def test_hsl_hue_modulo(self):
        """Test HSL hue modulo operation."""
        hsl = HSL(400, 50, 50)
        self.assertEqual(hsl.h, 40)  # 400 % 360
    
    def test_hsv_creation(self):
        """Test HSV creation."""
        hsv = HSV(180, 75, 90)
        self.assertEqual(hsv.h, 180)
        self.assertEqual(hsv.s, 75)
        self.assertEqual(hsv.v, 90)
    
    def test_cmyk_creation(self):
        """Test CMYK creation."""
        cmyk = CMYK(50, 30, 20, 10)
        self.assertEqual(cmyk.c, 50)
        self.assertEqual(cmyk.m, 30)
        self.assertEqual(cmyk.y, 20)
        self.assertEqual(cmyk.k, 10)


class TestColorParsing(unittest.TestCase):
    """Test color parsing functions."""
    
    def test_parse_hex_6_digit(self):
        """Test parsing 6-digit hex."""
        rgb = parse_hex('#ff0000')
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 0)
        self.assertEqual(rgb.b, 0)
    
    def test_parse_hex_3_digit(self):
        """Test parsing 3-digit hex."""
        rgb = parse_hex('#f00')
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 0)
        self.assertEqual(rgb.b, 0)
    
    def test_parse_hex_8_digit_with_alpha(self):
        """Test parsing 8-digit hex with alpha."""
        rgb = parse_hex('#ff000080')
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 0)
        self.assertEqual(rgb.b, 0)
        self.assertAlmostEqual(rgb.a, 0.5, places=2)
    
    def test_parse_hex_without_hash(self):
        """Test parsing hex without hash."""
        rgb = parse_hex('ff0000')
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 0)
        self.assertEqual(rgb.b, 0)
    
    def test_parse_hex_invalid(self):
        """Test parsing invalid hex."""
        with self.assertRaises(ValueError):
            parse_hex('#xyz')
        with self.assertRaises(ValueError):
            parse_hex('#ff')
    
    def test_parse_rgb(self):
        """Test parsing rgb() string."""
        rgb = parse_rgb('rgb(255, 0, 0)')
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 0)
        self.assertEqual(rgb.b, 0)
    
    def test_parse_rgb_with_spaces(self):
        """Test parsing rgb() with various spacing."""
        rgb = parse_rgb('rgb( 255, 0, 0 )')
        self.assertEqual(rgb.r, 255)
        
        rgb = parse_rgb('rgb(255,0,0)')
        self.assertEqual(rgb.r, 255)
    
    def test_parse_rgba(self):
        """Test parsing rgba() string."""
        rgb = parse_rgb('rgba(255, 0, 0, 0.5)')
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 0)
        self.assertEqual(rgb.b, 0)
        self.assertAlmostEqual(rgb.a, 0.5)
    
    def test_parse_rgb_invalid(self):
        """Test parsing invalid rgb."""
        with self.assertRaises(ValueError):
            parse_rgb('rgb(256, 0, 0)')
    
    def test_parse_hsl(self):
        """Test parsing hsl() string."""
        hsl = parse_hsl('hsl(0, 100%, 50%)')
        self.assertEqual(hsl.h, 0)
        self.assertEqual(hsl.s, 100)
        self.assertEqual(hsl.l, 50)
    
    def test_parse_hsl_without_percent(self):
        """Test parsing hsl() without percent signs."""
        hsl = parse_hsl('hsl(0, 100, 50)')
        self.assertEqual(hsl.s, 100)
        self.assertEqual(hsl.l, 50)
    
    def test_parse_color_named(self):
        """Test parsing named color."""
        rgb = parse_color('red')
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 0)
        self.assertEqual(rgb.b, 0)
        
        rgb = parse_color('CORAL')
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 127)
        self.assertEqual(rgb.b, 80)
    
    def test_parse_color_invalid(self):
        """Test parsing invalid color."""
        with self.assertRaises(ValueError):
            parse_color('nonexistentcolor')
    
    def test_color_name_to_rgb(self):
        """Test color name lookup."""
        rgb = color_name_to_rgb('aliceblue')
        self.assertEqual(rgb.r, 240)
        self.assertEqual(rgb.g, 248)
        self.assertEqual(rgb.b, 255)
        
        rgb = color_name_to_rgb('nonexistent')
        self.assertIsNone(rgb)
    
    def test_rgb_to_color_name(self):
        """Test finding color name."""
        name = rgb_to_color_name(RGB(255, 0, 0))
        self.assertEqual(name, 'red')
        
        name = rgb_to_color_name(RGB(123, 123, 123))
        self.assertIsNone(name)


class TestColorConversion(unittest.TestCase):
    """Test color conversion functions."""
    
    def test_rgb_to_hex(self):
        """Test RGB to hex conversion."""
        self.assertEqual(rgb_to_hex(255, 0, 0), '#ff0000')
        self.assertEqual(rgb_to_hex(0, 255, 0), '#00ff00')
        self.assertEqual(rgb_to_hex(0, 0, 255), '#0000ff')
    
    def test_rgb_to_hex_no_hash(self):
        """Test RGB to hex without hash."""
        self.assertEqual(rgb_to_hex(255, 0, 0, include_hash=False), 'ff0000')
    
    def test_hex_to_rgb(self):
        """Test hex to RGB conversion."""
        self.assertEqual(hex_to_rgb('#ff0000'), (255, 0, 0))
        self.assertEqual(hex_to_rgb('#f00'), (255, 0, 0))
    
    def test_rgb_to_hsl_red(self):
        """Test RGB to HSL for red."""
        h, s, l = rgb_to_hsl(255, 0, 0)
        self.assertEqual(h, 0)
        self.assertEqual(s, 100)
        self.assertEqual(l, 50)
    
    def test_rgb_to_hsl_green(self):
        """Test RGB to HSL for green."""
        h, s, l = rgb_to_hsl(0, 255, 0)
        self.assertEqual(h, 120)
        self.assertEqual(s, 100)
        self.assertEqual(l, 50)
    
    def test_rgb_to_hsl_blue(self):
        """Test RGB to HSL for blue."""
        h, s, l = rgb_to_hsl(0, 0, 255)
        self.assertEqual(h, 240)
        self.assertEqual(s, 100)
        self.assertEqual(l, 50)
    
    def test_rgb_to_hsl_gray(self):
        """Test RGB to HSL for gray."""
        h, s, l = rgb_to_hsl(128, 128, 128)
        self.assertEqual(s, 0)
    
    def test_hsl_to_rgb_red(self):
        """Test HSL to RGB for red."""
        r, g, b = hsl_to_rgb(0, 100, 50)
        self.assertEqual(r, 255)
        self.assertEqual(g, 0)
        self.assertEqual(b, 0)
    
    def test_hsl_to_rgb_roundtrip(self):
        """Test HSL to RGB roundtrip."""
        for color in [(255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 64, 192)]:
            h, s, l = rgb_to_hsl(*color)
            r, g, b = hsl_to_rgb(h, s, l)
            # Allow small rounding differences
            self.assertTrue(abs(r - color[0]) <= 1)
            self.assertTrue(abs(g - color[1]) <= 1)
            self.assertTrue(abs(b - color[2]) <= 1)
    
    def test_rgb_to_hsv(self):
        """Test RGB to HSV conversion."""
        h, s, v = rgb_to_hsv(255, 0, 0)
        self.assertEqual(h, 0)
        self.assertEqual(s, 100)
        self.assertEqual(v, 100)
    
    def test_hsv_to_rgb(self):
        """Test HSV to RGB conversion."""
        r, g, b = hsv_to_rgb(0, 100, 100)
        self.assertEqual(r, 255)
        self.assertEqual(g, 0)
        self.assertEqual(b, 0)
    
    def test_rgb_to_cmyk_red(self):
        """Test RGB to CMYK for red."""
        c, m, y, k = rgb_to_cmyk(255, 0, 0)
        self.assertEqual(c, 0)
        self.assertEqual(m, 100)
        self.assertEqual(y, 100)
        self.assertEqual(k, 0)
    
    def test_rgb_to_cmyk_black(self):
        """Test RGB to CMYK for black."""
        c, m, y, k = rgb_to_cmyk(0, 0, 0)
        self.assertEqual(c, 0)
        self.assertEqual(m, 0)
        self.assertEqual(y, 0)
        self.assertEqual(k, 100)
    
    def test_rgb_to_cmyk_white(self):
        """Test RGB to CMYK for white."""
        c, m, y, k = rgb_to_cmyk(255, 255, 255)
        self.assertEqual(c, 0)
        self.assertEqual(m, 0)
        self.assertEqual(y, 0)
        self.assertEqual(k, 0)
    
    def test_cmyk_to_rgb(self):
        """Test CMYK to RGB conversion."""
        r, g, b = cmyk_to_rgb(0, 100, 100, 0)
        self.assertEqual(r, 255)
        self.assertEqual(g, 0)
        self.assertEqual(b, 0)


class TestColorManipulation(unittest.TestCase):
    """Test color manipulation functions."""
    
    def test_lighten(self):
        """Test lighten function."""
        rgb = lighten('#ff0000', 20)
        h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
        self.assertEqual(l, 70)  # 50 + 20
    
    def test_darken(self):
        """Test darken function."""
        rgb = darken('#ff0000', 20)
        h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
        self.assertEqual(l, 30)  # 50 - 20
    
    def test_saturate(self):
        """Test saturate function."""
        rgb = saturate('#cc6666', 20)
        h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
        self.assertTrue(s > 50)
    
    def test_desaturate(self):
        """Test desaturate function."""
        rgb = desaturate('#ff0000', 50)
        h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
        self.assertEqual(s, 50)
    
    def test_grayscale(self):
        """Test grayscale function."""
        rgb = grayscale('#ff0000')
        self.assertEqual(rgb.r, rgb.g)
        self.assertEqual(rgb.g, rgb.b)
    
    def test_invert(self):
        """Test invert function."""
        rgb = invert('#000000')
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 255)
        self.assertEqual(rgb.b, 255)
        
        rgb = invert('#ff0000')
        self.assertEqual(rgb.r, 0)
        self.assertEqual(rgb.g, 255)
        self.assertEqual(rgb.b, 255)
    
    def test_complement(self):
        """Test complement function."""
        rgb = complement('#ff0000')  # Red
        h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
        self.assertEqual(h, 180)  # Cyan
    
    def test_mix(self):
        """Test mix function."""
        rgb = mix('#ff0000', '#0000ff', 0.5)
        self.assertEqual(rgb.r, 128)
        self.assertEqual(rgb.g, 0)
        self.assertEqual(rgb.b, 128)
    
    def test_mix_weight(self):
        """Test mix with different weights."""
        rgb = mix('#ff0000', '#0000ff', 0.0)
        self.assertEqual(rgb.r, 0)
        self.assertEqual(rgb.b, 255)
        
        rgb = mix('#ff0000', '#0000ff', 1.0)
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.b, 0)
    
    def test_blend_multiply(self):
        """Test multiply blend mode."""
        rgb = blend('#ff0000', '#0000ff', 'multiply')
        self.assertEqual(rgb.r, 0)
        self.assertEqual(rgb.g, 0)
        self.assertEqual(rgb.b, 0)
    
    def test_blend_screen(self):
        """Test screen blend mode."""
        rgb = blend('#000000', '#ffffff', 'screen')
        self.assertEqual(rgb.r, 255)
        self.assertEqual(rgb.g, 255)
        self.assertEqual(rgb.b, 255)
    
    def test_blend_normal(self):
        """Test normal blend mode."""
        rgb = blend('#ff0000', '#0000ff', 'normal')
        self.assertEqual(rgb.b, 255)


class TestColorHarmony(unittest.TestCase):
    """Test color harmony functions."""
    
    def test_analogous(self):
        """Test analogous colors."""
        colors = analogous('#ff0000')
        self.assertEqual(len(colors), 3)
    
    def test_triadic(self):
        """Test triadic colors."""
        colors = triadic('#ff0000')
        self.assertEqual(len(colors), 3)
        # Check colors are 120 degrees apart
        for i, color in enumerate(colors):
            h, s, l = rgb_to_hsl(color.r, color.g, color.b)
            self.assertEqual(h, i * 120)
    
    def test_split_complement(self):
        """Test split complementary colors."""
        colors = split_complement('#ff0000')
        self.assertEqual(len(colors), 3)
    
    def test_tetradic(self):
        """Test tetradic colors."""
        colors = tetradic('#ff0000')
        self.assertEqual(len(colors), 4)
    
    def test_monochromatic(self):
        """Test monochromatic colors."""
        colors = monochromatic('#ff0000', 5)
        self.assertEqual(len(colors), 5)
        # All should have same hue
        for color in colors:
            h, s, l = rgb_to_hsl(color.r, color.g, color.b)
            self.assertEqual(h, 0)


class TestColorUtility(unittest.TestCase):
    """Test color utility functions."""
    
    def test_luminance(self):
        """Test luminance calculation."""
        self.assertAlmostEqual(luminance('#ffffff'), 1.0)
        self.assertAlmostEqual(luminance('#000000'), 0.0)
    
    def test_contrast_ratio(self):
        """Test contrast ratio calculation."""
        ratio = contrast_ratio('#ffffff', '#000000')
        self.assertAlmostEqual(ratio, 21.0, places=1)
        
        ratio = contrast_ratio('#ffffff', '#ffffff')
        self.assertAlmostEqual(ratio, 1.0, places=1)
    
    def test_wcag_rating(self):
        """Test WCAG rating."""
        self.assertEqual(wcag_rating(7.0), 'AAA')
        self.assertEqual(wcag_rating(4.5), 'AA')
        self.assertEqual(wcag_rating(3.0), 'AA Large')
        self.assertEqual(wcag_rating(2.0), 'Fail')
    
    def test_brightness(self):
        """Test brightness calculation."""
        self.assertEqual(brightness('#ffffff'), 255)
        self.assertEqual(brightness('#000000'), 0)
    
    def test_is_light(self):
        """Test is_light function."""
        self.assertTrue(is_light('#ffffff'))
        self.assertTrue(is_light('#cccccc'))
        self.assertFalse(is_light('#000000'))
        self.assertFalse(is_light('#333333'))
    
    def test_is_dark(self):
        """Test is_dark function."""
        self.assertTrue(is_dark('#000000'))
        self.assertFalse(is_dark('#ffffff'))
    
    def test_text_color_for_bg(self):
        """Test text color selection."""
        self.assertEqual(text_color_for_bg('#ffffff'), '#000000')
        self.assertEqual(text_color_for_bg('#000000'), '#ffffff')
    
    def test_color_distance(self):
        """Test color distance calculation."""
        dist = color_distance('#ff0000', '#ff0000')
        self.assertEqual(dist, 0)
        
        dist = color_distance('#000000', '#ffffff')
        self.assertAlmostEqual(dist, 441.67, places=1)
    
    def test_closest_color(self):
        """Test closest color finding."""
        idx = closest_color('#ff0000', ['#ff0000', '#00ff00', '#0000ff'])
        self.assertEqual(idx, 0)
        
        idx = closest_color('#ff1010', ['#ff0000', '#00ff00', '#0000ff'])
        self.assertEqual(idx, 0)


class TestGradient(unittest.TestCase):
    """Test gradient functions."""
    
    def test_gradient(self):
        """Test gradient generation."""
        colors = gradient('#000000', '#ffffff', 5)
        self.assertEqual(len(colors), 5)
        self.assertEqual(colors[0].r, 0)
        self.assertEqual(colors[4].r, 255)
    
    def test_gradient_two_steps(self):
        """Test gradient with minimum steps."""
        colors = gradient('#ff0000', '#0000ff', 2)
        self.assertEqual(len(colors), 2)
        self.assertEqual(colors[0].r, 255)
        self.assertEqual(colors[1].b, 255)
    
    def test_multi_gradient(self):
        """Test multi-color gradient."""
        colors = multi_gradient(['#ff0000', '#00ff00', '#0000ff'], 5)
        self.assertTrue(len(colors) >= 9)


class TestRandomColors(unittest.TestCase):
    """Test random color generation."""
    
    def test_random_color(self):
        """Test random color generation."""
        rgb = random_color()
        self.assertIsInstance(rgb, RGB)
        self.assertTrue(0 <= rgb.r <= 255)
        self.assertTrue(0 <= rgb.g <= 255)
        self.assertTrue(0 <= rgb.b <= 255)
    
    def test_random_color_with_seed(self):
        """Test random color with seed."""
        rgb1 = random_color(seed=42)
        rgb2 = random_color(seed=42)
        self.assertEqual(rgb1.r, rgb2.r)
        self.assertEqual(rgb1.g, rgb2.g)
        self.assertEqual(rgb1.b, rgb2.b)
    
    def test_random_hue(self):
        """Test random hue generation."""
        rgb = random_hue(70, 50)
        h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
        self.assertEqual(s, 70)
        self.assertEqual(l, 50)
    
    def test_random_pastel(self):
        """Test random pastel generation."""
        rgb = random_pastel()
        h, s, l = rgb_to_hsl(rgb.r, rgb.g, rgb.b)
        self.assertTrue(s >= 40)
        self.assertTrue(l >= 75)


class TestCSSColors(unittest.TestCase):
    """Test CSS color constants."""
    
    def test_css_colors_exist(self):
        """Test that CSS colors dictionary exists."""
        self.assertTrue(len(CSS_COLORS) > 100)
    
    def test_css_colors_format(self):
        """Test CSS colors format."""
        for name, rgb in CSS_COLORS.items():
            self.assertTrue(0 <= rgb[0] <= 255)
            self.assertTrue(0 <= rgb[1] <= 255)
            self.assertTrue(0 <= rgb[2] <= 255)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestColorDataClasses))
    suite.addTests(loader.loadTestsFromTestCase(TestColorParsing))
    suite.addTests(loader.loadTestsFromTestCase(TestColorConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestColorManipulation))
    suite.addTests(loader.loadTestsFromTestCase(TestColorHarmony))
    suite.addTests(loader.loadTestsFromTestCase(TestColorUtility))
    suite.addTests(loader.loadTestsFromTestCase(TestGradient))
    suite.addTests(loader.loadTestsFromTestCase(TestRandomColors))
    suite.addTests(loader.loadTestsFromTestCase(TestCSSColors))
    
    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)