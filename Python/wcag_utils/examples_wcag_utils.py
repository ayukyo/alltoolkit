"""
WCAG Utils Examples - Practical examples for WCAG accessibility compliance.

This file demonstrates how to use wcag_utils for:
- Color contrast checking
- WCAG compliance validation
- Color vision deficiency simulation
- Accessible color suggestions
"""

from wcag_utils import (
    # Core functions
    calculate_relative_luminance,
    calculate_contrast_ratio,
    check_wcag_compliance,
    get_compliance_level,
    
    # Color parsing
    parse_hex_color,
    parse_rgb_color,
    rgb_to_hex,
    
    # Contrast helpers
    suggest_accessible_color,
    get_contrast_ratio_for_text_size,
    
    # Color vision deficiency simulation
    simulate_protanopia,
    simulate_deuteranopia,
    simulate_tritanopia,
    simulate_achromatopsia,
    
    # Additional functions
    check_contrast_for_all_cvd,
    get_all_cvd_contrast_ratios,
    is_accessible,
    quick_check,
    
    # Constants
    WCAG_AA_NORMAL_TEXT_MIN_RATIO,
    WCAG_AAA_NORMAL_TEXT_MIN_RATIO,
    
    # Classes
    ComplianceLevel,
)


def example_1_basic_contrast_check():
    """Example 1: Basic contrast ratio calculation."""
    print("=" * 60)
    print("Example 1: Basic Contrast Ratio Calculation")
    print("=" * 60)
    
    # Black text on white background
    black = (0, 0, 0)
    white = (255, 255, 255)
    
    ratio = calculate_contrast_ratio(black, white)
    print(f"Black on White: {ratio:.2f}:1")
    
    # White text on black background (same ratio)
    ratio2 = calculate_contrast_ratio(white, black)
    print(f"White on Black: {ratio2:.2f}:1")
    
    # Gray on white
    gray = (128, 128, 128)
    ratio3 = calculate_contrast_ratio(gray, white)
    print(f"Gray (128,128,128) on White: {ratio3:.2f}:1")
    
    # Same color (minimum ratio)
    ratio4 = calculate_contrast_ratio(gray, gray)
    print(f"Gray on Gray: {ratio4:.2f}:1")


def example_2_wcag_compliance_check():
    """Example 2: WCAG compliance checking."""
    print("\n" + "=" * 60)
    print("Example 2: WCAG Compliance Checking")
    print("=" * 60)
    
    # Check various color combinations
    test_cases = [
        ("#000000", "#FFFFFF", "Black on White"),
        ("#767676", "#FFFFFF", "Dark Gray on White"),
        ("#959595", "#FFFFFF", "Medium Gray on White"),
        ("#CCCCCC", "#FFFFFF", "Light Gray on White"),
        ("#FF0000", "#FFFFFF", "Red on White"),
        ("#00FF00", "#FFFFFF", "Green on White"),
    ]
    
    for fg_hex, bg_hex, description in test_cases:
        fg = parse_hex_color(fg_hex)
        bg = parse_hex_color(bg_hex)
        result = check_wcag_compliance(fg, bg)
        
        print(f"\n{description}:")
        print(f"  Ratio: {result.ratio:.2f}:1")
        print(f"  AA Normal: {'✓' if result.passes_aa_normal else '✗'}")
        print(f"  AA Large: {'✓' if result.passes_aa_large else '✗'}")
        print(f"  AAA Normal: {'✓' if result.passes_aaa_normal else '✗'}")
        print(f"  Level: {result.level.value}")


def example_3_color_parsing():
    """Example 3: Parsing different color formats."""
    print("\n" + "=" * 60)
    print("Example 3: Color Parsing")
    print("=" * 60)
    
    # Hex colors
    print("\nHex Color Parsing:")
    hex_colors = ["#FF0000", "#F00", "FFFFFF", "#808080"]
    for hex_color in hex_colors:
        rgb = parse_hex_color(hex_color)
        print(f"  {hex_color} → RGB({rgb[0]}, {rgb[1]}, {rgb[2]})")
    
    # RGB strings
    print("\nRGB String Parsing:")
    rgb_strings = ["rgb(255, 0, 0)", "rgb(128 128 128)", "0, 255, 128"]
    for rgb_str in rgb_strings:
        rgb = parse_rgb_color(rgb_str)
        print(f"  '{rgb_str}' → RGB({rgb[0]}, {rgb[1]}, {rgb[2]})")
    
    # RGB to Hex conversion
    print("\nRGB to Hex Conversion:")
    rgb_values = [(255, 0, 0), (128, 128, 128), (0, 255, 0)]
    for rgb in rgb_values:
        hex_color = rgb_to_hex(rgb)
        print(f"  RGB({rgb[0]}, {rgb[1]}, {rgb[2]}) → {hex_color}")


def example_4_text_size_compliance():
    """Example 4: Compliance with text size consideration."""
    print("\n" + "=" * 60)
    print("Example 4: Text Size Compliance")
    print("=" * 60)
    
    # Test medium gray on white with different text sizes
    fg = (149, 149, 149)  # #959595 - ratio ~3:1
    bg = (255, 255, 255)
    
    print(f"\nForeground: {rgb_to_hex(fg)}")
    print(f"Background: {rgb_to_hex(bg)}")
    
    # Small text (12pt regular)
    result_small = get_contrast_ratio_for_text_size(fg, bg, 12, is_bold=False)
    print(f"\n12pt Regular Text:")
    print(f"  Ratio: {result_small.ratio:.2f}:1")
    print(f"  AA Pass: {'✓' if result_small.passes_aa_normal else '✗'}")
    
    # Large text (18pt regular)
    result_large = get_contrast_ratio_for_text_size(fg, bg, 18, is_bold=False)
    print(f"\n18pt Regular Text (Large):")
    print(f"  Ratio: {result_large.ratio:.2f}:1")
    print(f"  AA Large Pass: {'✓' if result_large.passes_aa_large else '✗'}")
    
    # Bold text (14pt bold is considered large)
    result_bold = get_contrast_ratio_for_text_size(fg, bg, 14, is_bold=True)
    print(f"\n14pt Bold Text (Large):")
    print(f"  Ratio: {result_bold.ratio:.2f}:1")
    print(f"  AA Large Pass: {'✓' if result_bold.passes_aa_large else '✗'}")


def example_5_accessible_color_suggestions():
    """Example 5: Getting accessible color suggestions."""
    print("\n" + "=" * 60)
    print("Example 5: Accessible Color Suggestions")
    print("=" * 60)
    
    # Light gray on white - fails AA
    original_fg = (200, 200, 200)
    bg = (255, 255, 255)
    
    print(f"\nOriginal: {rgb_to_hex(original_fg)} on {rgb_to_hex(bg)}")
    original_ratio = calculate_contrast_ratio(original_fg, bg)
    print(f"  Ratio: {original_ratio:.2f}:1 - Fails AA")
    
    # Get suggestion for AA
    suggested = suggest_accessible_color(original_fg, bg, WCAG_AA_NORMAL_TEXT_MIN_RATIO)
    if suggested:
        print(f"\nSuggested for AA: {rgb_to_hex(suggested)}")
        suggested_ratio = calculate_contrast_ratio(suggested, bg)
        print(f"  Ratio: {suggested_ratio:.2f}:1 - Passes AA ✓")
    
    # Get suggestion for AAA
    suggested_aaa = suggest_accessible_color(original_fg, bg, WCAG_AAA_NORMAL_TEXT_MIN_RATIO)
    if suggested_aaa:
        print(f"\nSuggested for AAA: {rgb_to_hex(suggested_aaa)}")
        suggested_aaa_ratio = calculate_contrast_ratio(suggested_aaa, bg)
        print(f"  Ratio: {suggested_aaa_ratio:.2f}:1 - Passes AAA ✓")


def example_6_color_vision_deficiency():
    """Example 6: Color vision deficiency simulation."""
    print("\n" + "=" * 60)
    print("Example 6: Color Vision Deficiency Simulation")
    print("=" * 60)
    
    # Test colors
    colors = [
        ((255, 0, 0), "Red"),
        ((0, 255, 0), "Green"),
        ((0, 0, 255), "Blue"),
        ((255, 255, 0), "Yellow"),
        ((255, 0, 255), "Magenta"),
        ((0, 255, 255), "Cyan"),
    ]
    
    print("\nHow colors appear to people with different CVD types:")
    print("(Protanopia=red-blind, Deuteranopia=green-blind, Tritanopia=blue-blind)")
    
    for rgb, name in colors:
        print(f"\n{name} {rgb_to_hex(rgb)}:")
        
        proto = simulate_protanopia(rgb)
        deut = simulate_deuteranopia(rgb)
        tri = simulate_tritanopia(rgb)
        achro = simulate_achromatopsia(rgb)
        
        print(f"  Protanopia: {rgb_to_hex(proto)}")
        print(f"  Deuteranopia: {rgb_to_hex(deut)}")
        print(f"  Tritanopia: {rgb_to_hex(tri)}")
        print(f"  Achromatopsia: {rgb_to_hex(achro)} (grayscale)")


def example_7_cvd_contrast_check():
    """Example 7: Checking contrast for color blind users."""
    print("\n" + "=" * 60)
    print("Example 7: Contrast for Color Blind Users")
    print("=" * 60)
    
    # Red error message on white background
    red = (220, 53, 69)  # Bootstrap danger color
    white = (255, 255, 255)
    
    print(f"\nBootstrap Danger Red {rgb_to_hex(red)} on White")
    
    # Check all CVD types
    ratios = get_all_cvd_contrast_ratios(red, white)
    
    print("\nContrast Ratios:")
    for cvd_type, ratio in ratios.items():
        pass_fail = "✓ PASS" if ratio >= WCAG_AA_NORMAL_TEXT_MIN_RATIO else "✗ FAIL"
        print(f"  {cvd_type}: {ratio:.2f}:1 {pass_fail}")
    
    # Alternative: green on white for error messages
    green = (40, 167, 69)  # Bootstrap success color
    print(f"\nBootstrap Success Green {rgb_to_hex(green)} on White")
    
    ratios2 = get_all_cvd_contrast_ratios(green, white)
    for cvd_type, ratio in ratios2.items():
        pass_fail = "✓ PASS" if ratio >= WCAG_AA_NORMAL_TEXT_MIN_RATIO else "✗ FAIL"
        print(f"  {cvd_type}: {ratio:.2f}:1 {pass_fail}")


def example_8_quick_checks():
    """Example 8: Using convenience functions for quick checks."""
    print("\n" + "=" * 60)
    print("Example 8: Quick Accessibility Checks")
    print("=" * 60)
    
    # Quick check with hex colors
    test_pairs = [
        ("#000000", "#FFFFFF"),
        ("#767676", "#FFFFFF"),
        ("#CCCCCC", "#FFFFFF"),
        ("#FF5722", "#FFFFFF"),  # Material Design Deep Orange 500
        ("#2196F3", "#FFFFFF"),  # Material Design Blue 500
    ]
    
    print("\nQuick Checks:")
    for fg, bg in test_pairs:
        result = quick_check(fg, bg)
        accessible = is_accessible(fg, bg, "aa")
        print(f"  {fg} on {bg}: {result}")
    
    print("\nAA Level Checks:")
    for fg, bg in test_pairs:
        accessible = is_accessible(fg, bg, "aa")
        print(f"  {fg} on {bg}: {'✓ Accessible' if accessible else '✗ Not accessible'}")


def example_9_detailed_result():
    """Example 9: Using detailed ContrastResult."""
    print("\n" + "=" * 60)
    print("Example 9: Detailed Contrast Result")
    print("=" * 60)
    
    # Check a color combination
    result = check_wcag_compliance((33, 150, 243), (255, 255, 255))
    
    # Print detailed summary
    print(result.summary())
    
    # Access individual attributes
    print(f"\nSerialized result: {result.to_dict()}")


def example_10_design_workflow():
    """Example 10: Complete design workflow for accessibility."""
    print("\n" + "=" * 60)
    print("Example 10: Complete Design Workflow")
    print("=" * 60)
    
    # Scenario: Designer wants to use a custom brand color
    brand_color = (65, 105, 225)  # Royal Blue
    bg = (255, 255, 255)  # White background
    
    print("\nStep 1: Check current contrast")
    ratio = calculate_contrast_ratio(brand_color, bg)
    print(f"Brand Color {rgb_to_hex(brand_color)} on White: {ratio:.2f}:1")
    
    print("\nStep 2: Check WCAG compliance")
    result = check_wcag_compliance(brand_color, bg)
    print(f"AA Normal Text: {'✓ PASS' if result.passes_aa_normal else '✗ FAIL'}")
    print(f"AAA Normal Text: {'✓ PASS' if result.passes_aaa_normal else '✗ FAIL'}")
    
    print("\nStep 3: Check contrast for color blind users")
    cvd_results = check_contrast_for_all_cvd(brand_color, bg)
    all_pass = all(cvd_results.values())
    print(f"All CVD types pass AA: {'✓' if all_pass else '✗'}")
    for cvd_type, passes in cvd_results.items():
        print(f"  {cvd_type}: {'✓' if passes else '✗'}")
    
    if not all_pass or not result.passes_aaa_normal:
        print("\nStep 4: Suggest accessible alternatives")
        suggested = suggest_accessible_color(brand_color, bg, WCAG_AAA_NORMAL_TEXT_MIN_RATIO)
        if suggested:
            print(f"Suggested: {rgb_to_hex(suggested)}")
            suggested_result = check_wcag_compliance(suggested, bg)
            print(f"  AAA Normal Text: {'✓ PASS' if suggested_result.passes_aaa_normal else '✗ FAIL'}")


def main():
    """Run all examples."""
    example_1_basic_contrast_check()
    example_2_wcag_compliance_check()
    example_3_color_parsing()
    example_4_text_size_compliance()
    example_5_accessible_color_suggestions()
    example_6_color_vision_deficiency()
    example_7_cvd_contrast_check()
    example_8_quick_checks()
    example_9_detailed_result()
    example_10_design_workflow()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()