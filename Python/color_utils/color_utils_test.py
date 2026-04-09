#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Color Utilities Test Suite
========================================
Comprehensive test suite for the color_utils module.

Run: python color_utils_test.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Conversion functions
    hex_to_rgb, rgb_to_hex,
    rgb_to_hsl, hsl_to_rgb,
    rgb_to_hsv, hsv_to_rgb,
    rgb_to_cmyk, cmyk_to_rgb,
    hex_to_hsl, hsl_to_hex,
    hex_to_hsv, hsv_to_hex,
    
    # Manipulation functions
    lighten, darken, mix_colors, invert_color,
    saturate, desaturate, adjust_hue,
    
    # Palette functions
    complementary_color, analogous_colors, triadic_colors,
    split_complementary, tetradic_colors, monochromatic_colors,
    generate_gradient,
    
    # Accessibility functions
    get_luminance, contrast_ratio,
    is_wcag_aa, is_wcag_aaa, get_accessible_text_color,
    
    # Naming functions
    get_color_name, color_distance, is_similar_color,
    
    # Utility functions
    parse_color, format_color, random_color,
    is_valid_hex, is_valid_rgb,
)


# ============================================================================
# Test Results Tracking
# ============================================================================

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def record(self, name: str, passed: bool, error: str = None):
        if passed:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            self.errors.append((name, error))
            print(f"  ✗ {name}: {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"\nFailed tests:")
            for name, error in self.errors:
                print(f"  - {name}: {error}")
        print(f"{'='*60}")
        return self.failed == 0


results = TestResults()


# ============================================================================
# Helper Functions
# ============================================================================

def assert_equal(actual, expected, tolerance: float = 0):
    """Assert equality with optional tolerance for floats."""
    if tolerance > 0:
        if isinstance(actual, tuple):
            return all(abs(a - e) <= tolerance for a, e in zip(actual, expected))
        return abs(actual - expected) <= tolerance
    
    return actual == expected


def test_section(name: str):
    """Print test section header."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")


# ============================================================================
# Conversion Tests
# ============================================================================

def test_hex_to_rgb():
    test_section("hex_to_rgb")
    
    # Standard 6-digit hex
    results.record("FF5733", 
        assert_equal(hex_to_rgb("#FF5733"), (255, 87, 51)))
    results.record("000000", 
        assert_equal(hex_to_rgb("#000000"), (0, 0, 0)))
    results.record("FFFFFF", 
        assert_equal(hex_to_rgb("#FFFFFF"), (255, 255, 255)))
    
    # 3-digit shorthand
    results.record("F53 shorthand", 
        assert_equal(hex_to_rgb("#F53"), (255, 85, 51)))
    results.record("FFF shorthand", 
        assert_equal(hex_to_rgb("#FFF"), (255, 255, 255)))
    
    # Without # prefix
    results.record("No hash prefix", 
        assert_equal(hex_to_rgb("FF5733"), (255, 87, 51)))
    
    # Invalid hex
    try:
        hex_to_rgb("#GGGGGG")
        results.record("Invalid hex raises error", False)
    except ValueError:
        results.record("Invalid hex raises error", True)


def test_rgb_to_hex():
    test_section("rgb_to_hex")
    
    results.record("FF5733", 
        assert_equal(rgb_to_hex((255, 87, 51)), "#FF5733"))
    results.record("000000", 
        assert_equal(rgb_to_hex((0, 0, 0)), "#000000"))
    results.record("FFFFFF", 
        assert_equal(rgb_to_hex((255, 255, 255)), "#FFFFFF"))
    
    # Invalid RGB
    try:
        rgb_to_hex((300, 0, 0))
        results.record("Invalid RGB raises error", False)
    except ValueError:
        results.record("Invalid RGB raises error", True)


def test_rgb_hsl_conversion():
    test_section("rgb_to_hsl and hsl_to_rgb")
    
    # Test round-trip conversions
    test_colors = [
        (255, 87, 51),    # Orange-red
        (0, 0, 0),        # Black
        (255, 255, 255),  # White
        (128, 128, 128),  # Gray
        (255, 0, 0),      # Red
        (0, 255, 0),      # Green
        (0, 0, 255),      # Blue
    ]
    
    for rgb in test_colors:
        hsl = rgb_to_hsl(rgb)
        rgb_back = hsl_to_rgb(hsl)
        results.record(f"Round-trip {rgb}", 
            assert_equal(rgb_back, rgb, tolerance=2))
    
    # Specific known values
    results.record("Red HSL", 
        assert_equal(rgb_to_hsl((255, 0, 0)), (0, 100, 50), tolerance=2))
    results.record("Green HSL", 
        assert_equal(rgb_to_hsl((0, 255, 0)), (120, 100, 50), tolerance=2))
    results.record("Blue HSL", 
        assert_equal(rgb_to_hsl((0, 0, 255)), (240, 100, 50), tolerance=2))


def test_rgb_hsv_conversion():
    test_section("rgb_to_hsv and hsv_to_rgb")
    
    test_colors = [
        (255, 87, 51),
        (0, 0, 0),
        (255, 255, 255),
        (255, 0, 0),
    ]
    
    for rgb in test_colors:
        hsv = rgb_to_hsv(rgb)
        rgb_back = hsv_to_rgb(hsv)
        results.record(f"Round-trip {rgb}", 
            assert_equal(rgb_back, rgb, tolerance=2))


def test_rgb_cmyk_conversion():
    test_section("rgb_to_cmyk and cmyk_to_rgb")
    
    test_colors = [
        (255, 87, 51),
        (0, 0, 0),
        (255, 255, 255),
        (255, 0, 0),
    ]
    
    for rgb in test_colors:
        cmyk = rgb_to_cmyk(rgb)
        rgb_back = cmyk_to_rgb(cmyk)
        results.record(f"Round-trip {rgb}", 
            assert_equal(rgb_back, rgb, tolerance=5))


def test_cross_format_conversion():
    test_section("Cross-format conversions")
    
    hex_color = "#FF5733"
    
    # hex -> hsl -> hex
    hsl = hex_to_hsl(hex_color)
    hex_back = hsl_to_hex(hsl)
    # Allow small differences due to rounding
    results.record("HEX -> HSL -> HEX", 
        hex_back.upper() == hex_color.upper() or 
        color_distance(hex_to_rgb(hex_back), hex_to_rgb(hex_color)) < 5)
    
    # hex -> hsv -> hex
    hsv = hex_to_hsv(hex_color)
    hex_back = hsv_to_hex(hsv)
    results.record("HEX -> HSV -> HEX", 
        hex_back.upper() == hex_color.upper() or
        color_distance(hex_to_rgb(hex_back), hex_to_rgb(hex_color)) < 5)


# ============================================================================
# Manipulation Tests
# ============================================================================

def test_lighten():
    test_section("lighten")
    
    # Lighten should increase lightness
    original = "#FF5733"
    lightened = lighten(original, 0.2)
    orig_l = rgb_to_hsl(hex_to_rgb(original))[2]
    light_l = rgb_to_hsl(hex_to_rgb(lightened))[2]
    
    results.record("Lighten increases L", light_l > orig_l)
    results.record("Lighten returns hex", isinstance(lightened, str) and lightened.startswith('#'))
    
    # Test with RGB input
    rgb_orig = (255, 87, 51)
    rgb_light = lighten(rgb_orig, 0.1)
    results.record("Lighten with RGB input", isinstance(rgb_light, tuple))


def test_darken():
    test_section("darken")
    
    original = "#FF5733"
    darkened = darken(original, 0.2)
    orig_l = rgb_to_hsl(hex_to_rgb(original))[2]
    dark_l = rgb_to_hsl(hex_to_rgb(darkened))[2]
    
    results.record("Darken decreases L", dark_l < orig_l)
    
    # Edge cases
    results.record("Darken black stays black", 
        darken("#000000", 0.5) == "#000000")
    results.record("Lighten white stays white", 
        lighten("#FFFFFF", 0.5) == "#FFFFFF")


def test_mix_colors():
    test_section("mix_colors")
    
    # Mix red and blue
    result = mix_colors("#FF0000", "#0000FF", 0.5)
    results.record("Mix red+blue at 50%", 
        assert_equal(hex_to_rgb(result), (128, 0, 128), tolerance=5))
    
    # Mix at 0% (all first color)
    result = mix_colors("#FF0000", "#0000FF", 0.0)
    results.record("Mix at 0% ratio", result.upper() == "#FF0000")
    
    # Mix at 100% (all second color)
    result = mix_colors("#FF0000", "#0000FF", 1.0)
    results.record("Mix at 100% ratio", result.upper() == "#0000FF")


def test_invert_color():
    test_section("invert_color")
    
    results.record("Invert black", invert_color("#000000").upper() == "#FFFFFF")
    results.record("Invert white", invert_color("#FFFFFF").upper() == "#000000")
    results.record("Invert red", invert_color("#FF0000").upper() == "#00FFFF")
    
    # Double invert should return original
    original = "#FF5733"
    inverted = invert_color(original)
    double_inverted = invert_color(inverted)
    results.record("Double invert", double_inverted.upper() == original.upper())


def test_saturate_desaturate():
    test_section("saturate and desaturate")
    
    # Start with a desaturated color
    original = "#808080"  # Gray (0% saturation)
    
    # Desaturating gray should stay gray
    desat = desaturate(original, 0.5)
    results.record("Desaturate gray", desat.upper() == "#808080")
    
    # Saturate a colored color
    original = "#FF5733"
    sat = saturate(original, 0.2)
    orig_s = rgb_to_hsl(hex_to_rgb(original))[1]
    sat_s = rgb_to_hsl(hex_to_rgb(sat))[1]
    results.record("Saturate increases S", sat_s >= orig_s)


def test_adjust_hue():
    test_section("adjust_hue")
    
    # Rotate red (0°) by 120° should give green
    result = adjust_hue("#FF0000", 120)
    results.record("Rotate red to green", 
        abs(rgb_to_hsl(hex_to_rgb(result))[0] - 120) < 5)
    
    # Rotate by 360° should return same color
    original = "#FF5733"
    result = adjust_hue(original, 360)
    # Allow small differences due to rounding
    results.record("Rotate 360 degrees", 
        result.upper() == original.upper() or
        color_distance(hex_to_rgb(result), hex_to_rgb(original)) < 5)


# ============================================================================
# Palette Tests
# ============================================================================

def test_complementary_color():
    test_section("complementary_color")
    
    # Complementary is 180° rotation
    result = complementary_color("#FF5733")
    expected = adjust_hue("#FF5733", 180)
    results.record("Complementary = 180° rotation", 
        result.upper() == expected.upper())


def test_analogous_colors():
    test_section("analogous_colors")
    
    colors = analogous_colors("#FF5733", 2)
    results.record("Returns 2 colors", len(colors) == 2)
    results.record("All colors are hex", all(isinstance(c, str) for c in colors))


def test_triadic_colors():
    test_section("triadic_colors")
    
    colors = triadic_colors("#FF5733")
    results.record("Returns 3 colors", len(colors) == 3)
    results.record("First color is original", colors[0].upper() == "#FF5733")
    
    # Check hue spacing
    hues = [rgb_to_hsl(hex_to_rgb(c))[0] for c in colors]
    results.record("Hues ~120° apart", 
        abs(hues[1] - hues[0] - 120) < 10 or abs(hues[1] - hues[0] + 240) < 10)


def test_split_complementary():
    test_section("split_complementary")
    
    colors = split_complementary("#FF5733")
    results.record("Returns 3 colors", len(colors) == 3)
    results.record("First color is original", colors[0].upper() == "#FF5733")


def test_tetradic_colors():
    test_section("tetradic_colors")
    
    colors = tetradic_colors("#FF5733")
    results.record("Returns 4 colors", len(colors) == 4)


def test_monochromatic_colors():
    test_section("monochromatic_colors")
    
    colors = monochromatic_colors("#FF5733", 4)
    results.record("Returns 4 colors", len(colors) == 4)
    
    # All should have same hue
    hues = [rgb_to_hsl(hex_to_rgb(c))[0] for c in colors]
    results.record("Same hue", all(abs(h - hues[0]) < 5 for h in hues))
    
    # Lightness should vary
    lights = [rgb_to_hsl(hex_to_rgb(c))[2] for c in colors]
    results.record("Varying lightness", len(set(lights)) > 1)


def test_generate_gradient():
    test_section("generate_gradient")
    
    gradient = generate_gradient("#FF0000", "#0000FF", 5)
    results.record("Returns 5 colors", len(gradient) == 5)
    results.record("First is start color", gradient[0].upper() == "#FF0000")
    results.record("Last is end color", gradient[4].upper() == "#0000FF")


# ============================================================================
# Accessibility Tests
# ============================================================================

def test_get_luminance():
    test_section("get_luminance")
    
    results.record("White luminance = 1.0", 
        assert_equal(get_luminance((255, 255, 255)), 1.0, tolerance=0.01))
    results.record("Black luminance = 0.0", 
        assert_equal(get_luminance((0, 0, 0)), 0.0, tolerance=0.01))
    
    # Green should be brighter than blue (human eye sensitivity)
    green_lum = get_luminance((0, 255, 0))
    blue_lum = get_luminance((0, 0, 255))
    results.record("Green > Blue luminance", green_lum > blue_lum)


def test_contrast_ratio():
    test_section("contrast_ratio")
    
    # Maximum contrast
    results.record("Black/White = 21.0", 
        assert_equal(contrast_ratio("#000000", "#FFFFFF"), 21.0, tolerance=0.1))
    
    # Same color = 1.0
    results.record("Same color = 1.0", 
        assert_equal(contrast_ratio("#FF5733", "#FF5733"), 1.0, tolerance=0.1))
    
    # Known values
    ratio = contrast_ratio("#FF5733", "#FFFFFF")
    results.record("Orange/White contrast", 2.0 < ratio < 5.0)


def test_wcag_compliance():
    test_section("WCAG compliance")
    
    # Black/White passes everything
    results.record("B/W passes AA", is_wcag_aa("#000000", "#FFFFFF"))
    results.record("B/W passes AAA", is_wcag_aaa("#000000", "#FFFFFF"))
    
    # Low contrast fails
    results.record("Low contrast fails AA", 
        not is_wcag_aa("#FF5733", "#FF6B4D"))
    
    # Large text has lower requirements
    low_contrast = "#777777"
    results.record("Large text AA easier", 
        is_wcag_aa(low_contrast, "#FFFFFF", large_text=True) or 
        not is_wcag_aa(low_contrast, "#FFFFFF", large_text=False))


def test_get_accessible_text_color():
    test_section("get_accessible_text_color")
    
    results.record("White bg -> black text", 
        get_accessible_text_color("#FFFFFF").upper() == "#000000")
    results.record("Black bg -> white text", 
        get_accessible_text_color("#000000").upper() == "#FFFFFF")
    
    # Test with RGB input
    result = get_accessible_text_color((255, 255, 255))
    results.record("RGB input works", result.upper() == "#000000")


# ============================================================================
# Naming Tests
# ============================================================================

def test_get_color_name():
    test_section("get_color_name")
    
    results.record("Exact match Red", get_color_name("#FF0000") == "Red")
    results.record("Exact match White", get_color_name("#FFFFFF") == "White")
    results.record("Exact match Black", get_color_name("#000000") == "Black")
    
    # Unknown color returns None or closest match
    result = get_color_name("#123456")
    results.record("Unknown color handled", result is None or isinstance(result, str))


def test_color_distance():
    test_section("color_distance")
    
    # Same color = 0 distance
    results.record("Same color distance = 0", 
        color_distance((255, 87, 51), (255, 87, 51)) == 0)
    
    # Different colors have positive distance
    dist = color_distance((255, 0, 0), (0, 0, 0))
    results.record("Different colors > 0", dist > 0)
    
    # Known distance
    results.record("Red to Black distance", 
        assert_equal(dist, 255.0, tolerance=0.1))


def test_is_similar_color():
    test_section("is_similar_color")
    
    # Same color is similar
    results.record("Same color is similar", 
        is_similar_color("#FF5733", "#FF5733"))
    
    # Very different colors are not similar
    results.record("Red vs Blue not similar", 
        not is_similar_color("#FF0000", "#0000FF"))
    
    # Similar shades
    results.record("Similar shades", 
        is_similar_color("#FF5733", "#FF5834", threshold=5))


# ============================================================================
# Utility Tests
# ============================================================================

def test_parse_color():
    test_section("parse_color")
    
    # HEX input
    results.record("Parse HEX", 
        assert_equal(parse_color("#FF5733"), (255, 87, 51)))
    
    # RGB input
    results.record("Parse RGB tuple", 
        assert_equal(parse_color((255, 87, 51)), (255, 87, 51)))
    
    # Named color
    results.record("Parse named color", 
        assert_equal(parse_color("Red"), (255, 0, 0)))
    
    # Invalid color
    try:
        parse_color("InvalidColor123")
        results.record("Invalid color raises error", False)
    except ValueError:
        results.record("Invalid color raises error", True)


def test_format_color():
    test_section("format_color")
    
    rgb = (255, 87, 51)
    
    results.record("Format as hex", format_color(rgb, "hex").upper() == "#FF5733")
    results.record("Format as rgb", format_color(rgb, "rgb") == "rgb(255, 87, 51)")
    results.record("Format as hsl", "hsl" in format_color(rgb, "hsl"))
    results.record("Format as hsv", "hsv" in format_color(rgb, "hsv"))
    results.record("Format as cmyk", "cmyk" in format_color(rgb, "cmyk"))


def test_random_color():
    test_section("random_color")
    
    color = random_color()
    results.record("Random color is valid hex", is_valid_hex(color))
    
    # Generate multiple and check they're different
    colors = [random_color() for _ in range(10)]
    results.record("Random colors vary", len(set(colors)) > 1)


def test_is_valid_hex():
    test_section("is_valid_hex")
    
    results.record("Valid 6-digit", is_valid_hex("#FF5733"))
    results.record("Valid 3-digit", is_valid_hex("#F53"))
    results.record("Valid no hash", is_valid_hex("FF5733"))
    results.record("Invalid chars", not is_valid_hex("#GGGGGG"))
    results.record("Invalid length", not is_valid_hex("#FFFF"))
    results.record("Empty string", not is_valid_hex(""))


def test_is_valid_rgb():
    test_section("is_valid_rgb")
    
    results.record("Valid RGB", is_valid_rgb(255, 87, 51))
    results.record("Zero values", is_valid_rgb(0, 0, 0))
    results.record("Max values", is_valid_rgb(255, 255, 255))
    results.record("Negative invalid", not is_valid_rgb(-1, 0, 0))
    results.record("Over 255 invalid", not is_valid_rgb(256, 0, 0))


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================

def test_edge_cases():
    test_section("Edge Cases")
    
    # Empty/None handling
    try:
        # Test with boundary values
        edge_colors = [
            "#000000",  # Black
            "#FFFFFF",  # White
            "#000001",  # Near black
            "#FFFFFE",  # Near white
        ]
        
        for color in edge_colors:
            rgb = hex_to_rgb(color)
            hsl = rgb_to_hsl(rgb)
            hsv = rgb_to_hsv(rgb)
            cmyk = rgb_to_cmyk(rgb)
            
            # Round trip
            back = rgb_to_hex(rgb)
            if back.upper() != color.upper():
                results.record(f"Edge case {color}", False)
                break
        else:
            results.record("Edge cases handled", True)
            
    except Exception as e:
        results.record("Edge cases handled", False, str(e))
    
    # Test bounds on manipulation
    results.record("Lighten at max", 
        lighten("#FFFFFF", 1.0).upper() == "#FFFFFF")
    results.record("Darken at max", 
        darken("#000000", 1.0).upper() == "#000000")


# ============================================================================
# Main Test Runner
# ============================================================================

def run_all_tests():
    """Run all test suites."""
    print("\n" + "="*60)
    print("AllToolkit - Color Utilities Test Suite")
    print("="*60)
    
    # Conversion tests
    test_hex_to_rgb()
    test_rgb_to_hex()
    test_rgb_hsl_conversion()
    test_rgb_hsv_conversion()
    test_rgb_cmyk_conversion()
    test_cross_format_conversion()
    
    # Manipulation tests
    test_lighten()
    test_darken()
    test_mix_colors()
    test_invert_color()
    test_saturate_desaturate()
    test_adjust_hue()
    
    # Palette tests
    test_complementary_color()
    test_analogous_colors()
    test_triadic_colors()
    test_split_complementary()
    test_tetradic_colors()
    test_monochromatic_colors()
    test_generate_gradient()
    
    # Accessibility tests
    test_get_luminance()
    test_contrast_ratio()
    test_wcag_compliance()
    test_get_accessible_text_color()
    
    # Naming tests
    test_get_color_name()
    test_color_distance()
    test_is_similar_color()
    
    # Utility tests
    test_parse_color()
    test_format_color()
    test_random_color()
    test_is_valid_hex()
    test_is_valid_rgb()
    
    # Edge cases
    test_edge_cases()
    
    # Summary
    success = results.summary()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
