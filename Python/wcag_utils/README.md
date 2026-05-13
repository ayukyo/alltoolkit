# WCAG Utils - WCAG Accessibility Compliance Utilities

A comprehensive Python library for WCAG (Web Content Accessibility Guidelines) color contrast checking and accessibility compliance. Zero external dependencies - uses only Python standard library.

## Features

- **Contrast Ratio Calculation**: Calculate WCAG-compliant contrast ratios between colors
- **WCAG Compliance Checking**: Validate colors against AA and AAA standards
- **Relative Luminance**: Calculate relative luminance according to WCAG 2.1 formula
- **Color Parsing**: Parse hex colors (#RGB, #RRGGBB) and RGB strings
- **Text Size Compliance**: Check compliance considering font size (large vs normal text)
- **Accessible Color Suggestions**: Get suggested colors that meet target contrast ratios
- **Color Vision Deficiency Simulation**: Simulate how colors appear to people with:
  - Protanopia (red-blindness)
  - Deuteranopia (green-blindness)
  - Tritanopia (blue-blindness)
  - Achromatopsia (complete color blindness)
- **CVD Contrast Checking**: Verify contrast ratios for all color blindness types

## Installation

```python
from wcag_utils import (
    calculate_contrast_ratio,
    check_wcag_compliance,
    is_accessible,
    quick_check,
    # ... and more
)
```

## Quick Start

```python
from wcag_utils import quick_check, is_accessible

# Quick check
print(quick_check("#000000", "#FFFFFF"))
# Output: Contrast: 21.00:1 - PASS (AAA)

# Boolean check for AA compliance
if is_accessible("#767676", "#FFFFFF", "aa"):
    print("Color combination passes WCAG AA!")
```

## Core Functions

### Contrast Ratio Calculation

```python
from wcag_utils import calculate_contrast_ratio

# Calculate ratio between two RGB colors
ratio = calculate_contrast_ratio((0, 0, 0), (255, 255, 255))
print(f"Ratio: {ratio}:1")  # Output: Ratio: 21.0:1

# Using hex colors (parse first)
from wcag_utils import parse_hex_color
fg = parse_hex_color("#767676")
bg = parse_hex_color("#FFFFFF")
ratio = calculate_contrast_ratio(fg, bg)
```

### WCAG Compliance Checking

```python
from wcag_utils import check_wcag_compliance

result = check_wcag_compliance((0, 0, 0), (255, 255, 255))

print(f"Ratio: {result.ratio:.2f}:1")
print(f"AA Normal Text: {result.passes_aa_normal}")  # True
print(f"AAA Normal Text: {result.passes_aaa_normal}")  # True
print(f"Level: {result.level.value}")  # "aaa"

# Get detailed summary
print(result.summary())
```

### Compliance Levels

| Level | Ratio | Description |
|-------|-------|-------------|
| AAA | ≥ 7.0 | Passes all WCAG requirements |
| AA | ≥ 4.5 | Passes AA for normal text |
| AA_LARGE | ≥ 3.0 | Passes AA for large text only |
| FAIL | < 3.0 | Does not pass any standard |

### Text Size Consideration

```python
from wcag_utils import get_contrast_ratio_for_text_size

# Check compliance for specific text size
# 18pt regular is "large" text (lower requirement)
result = get_contrast_ratio_for_text_size(
    (128, 128, 128),  # foreground
    (255, 255, 255),  # background
    font_size_pt=18,
    is_bold=False
)
```

### Accessible Color Suggestions

```python
from wcag_utils import suggest_accessible_color, WCAG_AA_NORMAL_TEXT_MIN_RATIO

# Get suggested color that meets target ratio
suggested = suggest_accessible_color(
    (200, 200, 200),  # Light gray - fails AA
    (255, 255, 255),  # White background
    target_ratio=WCAG_AA_NORMAL_TEXT_MIN_RATIO
)
print(f"Suggested: {suggested}")  # Darker gray that passes AA
```

## Color Vision Deficiency

### Simulation

```python
from wcag_utils import (
    simulate_protanopia,
    simulate_deuteranopia,
    simulate_tritanopia,
    simulate_achromatopsia
)

# See how colors appear to people with CVD
red = (255, 0, 0)
print(f"Normal: {red}")
print(f"Protanopia: {simulate_protanopia(red)}")
print(f"Deuteranopia: {simulate_deuteranopia(red)}")
print(f"Achromatopsia: {simulate_achromatopsia(red)}")
```

### CVD Contrast Checking

```python
from wcag_utils import check_contrast_for_all_cvd

# Check if contrast is maintained for all CVD types
results = check_contrast_for_all_cvd((220, 53, 69), (255, 255, 255))

for cvd_type, passes in results.items():
    print(f"{cvd_type}: {'PASS' if passes else 'FAIL'}")
```

## WCAG Standards Reference

### Contrast Ratio Requirements

| Standard | Normal Text | Large Text | Non-Text |
|----------|-------------|------------|----------|
| AA | 4.5:1 | 3.0:1 | 3.0:1 |
| AAA | 7.0:1 | 4.5:1 | - |

### Large Text Definition

- **Regular**: ≥ 18pt (≈ 24px)
- **Bold**: ≥ 14pt (≈ 18.67px)

## License

MIT License - Free for personal and commercial use.

## References

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Contrast Minimum (1.4.3)](https://www.w3.org/WAI/WCAG21/quickref/#contrast-minimum)
- [Contrast Enhanced (1.4.6)](https://www.w3.org/WAI/WCAG21/quickref/#contrast-enhanced)
- [Brettel, Viénot, Mollon (1997) - CVD Simulation Algorithm](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2631568/)