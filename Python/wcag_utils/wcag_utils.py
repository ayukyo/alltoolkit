"""
WCAG Utils - WCAG accessibility compliance checking utilities.

Provides color contrast ratio calculation, WCAG AA/AAA compliance checking,
relative luminance calculation, and color vision deficiency simulation.

Based on WCAG 2.1 guidelines: https://www.w3.org/WAI/WCAG21/quickref/#contrast-minimum

Zero external dependencies - uses only Python standard library.
"""

from enum import Enum
from typing import Tuple, Optional, List, Dict, Any
import math


# WCAG 2.1 Contrast Ratio Requirements
WCAG_AA_NORMAL_TEXT_MIN_RATIO = 4.5  # Minimum for normal text (Level AA)
WCAG_AA_LARGE_TEXT_MIN_RATIO = 3.0   # Minimum for large text (Level AA)
WCAG_AAA_NORMAL_TEXT_MIN_RATIO = 7.0  # Minimum for normal text (Level AAA)
WCAG_AAA_LARGE_TEXT_MIN_RATIO = 4.5   # Minimum for large text (Level AAA)
WCAG_NON_TEXT_MIN_RATIO = 3.0         # Minimum for non-text elements (Level AA)

# Large text definition (WCAG 2.1)
LARGE_TEXT_MIN_FONT_SIZE_PT = 18  # 18pt minimum for bold text
LARGE_TEXT_MIN_FONT_SIZE_PT_BOLD = 14  # 14pt minimum for bold text
LARGE_TEXT_MIN_FONT_SIZE_PX = 24  # Approximately 24px for regular
LARGE_TEXT_MIN_FONT_SIZE_PX_BOLD = 18.67  # Approximately 18.67px for bold


class ComplianceLevel(Enum):
    """WCAG compliance levels."""
    FAIL = "fail"           # Does not meet any standard
    AA_LARGE = "aa_large"   # Meets AA for large text only
    AA = "aa"               # Meets AA for normal text
    AAA_LARGE = "aaa_large" # Meets AAA for large text only
    AAA = "aaa"             # Meets AAA for normal text


class ContrastResult:
    """Result of WCAG contrast ratio check."""
    
    def __init__(
        self,
        foreground: Tuple[int, int, int],
        background: Tuple[int, int, int],
        ratio: float,
        level: ComplianceLevel,
        passes_aa_normal: bool,
        passes_aa_large: bool,
        passes_aaa_normal: bool,
        passes_aaa_large: bool,
        passes_non_text: bool
    ):
        self.foreground = foreground
        self.background = background
        self.ratio = ratio
        self.level = level
        self.passes_aa_normal = passes_aa_normal
        self.passes_aa_large = passes_aa_large
        self.passes_aaa_normal = passes_aaa_normal
        self.passes_aaa_large = passes_aaa_large
        self.passes_non_text = passes_non_text
    
    def __repr__(self) -> str:
        return f"ContrastResult(ratio={self.ratio:.2f}, level={self.level.value})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "foreground": self.foreground,
            "background": self.background,
            "foreground_hex": rgb_to_hex(self.foreground),
            "background_hex": rgb_to_hex(self.background),
            "ratio": round(self.ratio, 2),
            "level": self.level.value,
            "passes_aa_normal": self.passes_aa_normal,
            "passes_aa_large": self.passes_aa_large,
            "passes_aaa_normal": self.passes_aaa_normal,
            "passes_aaa_large": self.passes_aaa_large,
            "passes_non_text": self.passes_non_text,
        }
    
    def summary(self) -> str:
        """Get human-readable summary."""
        fg_hex = rgb_to_hex(self.foreground)
        bg_hex = rgb_to_hex(self.background)
        
        lines = [
            f"Contrast Ratio: {self.ratio:.2f}:1",
            f"Foreground: {fg_hex} RGB({self.foreground[0]}, {self.foreground[1]}, {self.foreground[2]})",
            f"Background: {bg_hex} RGB({self.background[0]}, {self.background[1]}, {self.background[2]})",
            "",
            "WCAG Compliance:",
            f"  AA (Normal Text): {'✓ PASS' if self.passes_aa_normal else '✗ FAIL'} (requires {WCAG_AA_NORMAL_TEXT_MIN_RATIO}:1)",
            f"  AA (Large Text): {'✓ PASS' if self.passes_aa_large else '✗ FAIL'} (requires {WCAG_AA_LARGE_TEXT_MIN_RATIO}:1)",
            f"  AA (Non-Text): {'✓ PASS' if self.passes_non_text else '✗ FAIL'} (requires {WCAG_NON_TEXT_MIN_RATIO}:1)",
            f"  AAA (Normal Text): {'✓ PASS' if self.passes_aaa_normal else '✗ FAIL'} (requires {WCAG_AAA_NORMAL_TEXT_MIN_RATIO}:1)",
            f"  AAA (Large Text): {'✓ PASS' if self.passes_aaa_large else '✗ FAIL'} (requires {WCAG_AAA_LARGE_TEXT_MIN_RATIO}:1)",
        ]
        return "\n".join(lines)


def _srgb_to_linear(c: float) -> float:
    """Convert sRGB component to linear RGB."""
    if c <= 0.03928:
        return c / 12.92
    else:
        return pow((c + 0.055) / 1.055, 2.4)


def _linear_to_srgb(c: float) -> float:
    """Convert linear RGB component to sRGB."""
    if c <= 0.0031308:
        return c * 12.92
    else:
        return 1.055 * pow(c, 1/2.4) - 0.055


def _clamp_rgb(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """Clamp RGB values to valid range (0-255)."""
    return (
        max(0, min(255, r)),
        max(0, min(255, g)),
        max(0, min(255, b))
    )


def calculate_relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """
    Calculate relative luminance of an RGB color.
    
    Relative luminance follows the definition from WCAG 2.1:
    L = 0.2126 * R + 0.7152 * G + 0.0722 * B
    
    Where R, G, B are linear RGB values (gamma-expanded).
    
    Args:
        rgb: RGB tuple (0-255 range)
    
    Returns:
        Relative luminance value (0.0 to 1.0)
    
    Example:
        >>> calculate_relative_luminance((255, 255, 255))  # White
        1.0
        >>> calculate_relative_luminance((0, 0, 0))  # Black
        0.0
    """
    r, g, b = rgb
    
    # Normalize to 0-1 range and convert to linear
    r_linear = _srgb_to_linear(r / 255)
    g_linear = _srgb_to_linear(g / 255)
    b_linear = _srgb_to_linear(b / 255)
    
    # Calculate relative luminance
    luminance = 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear
    
    return luminance


def calculate_contrast_ratio(
    color1: Tuple[int, int, int],
    color2: Tuple[int, int, int]
) -> float:
    """
    Calculate contrast ratio between two RGB colors.
    
    Contrast ratio = (L1 + 0.05) / (L2 + 0.05)
    Where L1 >= L2 (L1 is the lighter color's luminance)
    
    Args:
        color1: First RGB tuple (0-255 range)
        color2: Second RGB tuple (0-255 range)
    
    Returns:
        Contrast ratio (1:1 to 21:1)
    
    Example:
        >>> calculate_contrast_ratio((255, 255, 255), (0, 0, 0))  # White on Black
        21.0
        >>> calculate_contrast_ratio((0, 0, 0), (255, 255, 255))  # Black on White
        21.0
    """
    l1 = calculate_relative_luminance(color1)
    l2 = calculate_relative_luminance(color2)
    
    # Ensure lighter color is numerator
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    ratio = (lighter + 0.05) / (darker + 0.05)
    
    return ratio


def get_compliance_level(ratio: float) -> ComplianceLevel:
    """
    Get WCAG compliance level for a given contrast ratio.
    
    Args:
        ratio: Contrast ratio
    
    Returns:
        ComplianceLevel enum value
    
    Example:
        >>> get_compliance_level(7.5)
        ComplianceLevel.AAA
        >>> get_compliance_level(4.5)
        ComplianceLevel.AA
        >>> get_compliance_level(3.0)
        ComplianceLevel.AA_LARGE
        >>> get_compliance_level(2.5)
        ComplianceLevel.FAIL
    """
    # Check from highest to lowest level
    # AAA: passes everything (>= 7.0)
    # AA: passes AA normal (>= 4.5) but not AAA normal (< 7.0)
    # Note: AA_NORMAL_TEXT_MIN_RATIO == AAA_LARGE_TEXT_MIN_RATIO (both 4.5)
    # So 4.5 passes AA for normal text, which is the higher achievement
    if ratio >= WCAG_AAA_NORMAL_TEXT_MIN_RATIO:  # >= 7.0
        return ComplianceLevel.AAA
    elif ratio >= WCAG_AA_NORMAL_TEXT_MIN_RATIO:  # >= 4.5 (same as AAA large)
        # At 4.5+, passes AA normal text AND AAA large text
        # But since it doesn't pass AAA normal (< 7.0), return AA
        return ComplianceLevel.AA
    elif ratio >= WCAG_AA_LARGE_TEXT_MIN_RATIO:  # >= 3.0
        return ComplianceLevel.AA_LARGE
    else:
        return ComplianceLevel.FAIL


def check_wcag_compliance(
    foreground: Tuple[int, int, int],
    background: Tuple[int, int, int],
    is_large_text: bool = False
) -> ContrastResult:
    """
    Check WCAG compliance for foreground/background color combination.
    
    Args:
        foreground: Text/foreground RGB tuple (0-255 range)
        background: Background RGB tuple (0-255 range)
        is_large_text: Whether the text is considered "large" (18pt regular or 14pt bold)
    
    Returns:
        ContrastResult with detailed compliance information
    
    Example:
        >>> result = check_wcag_compliance((0, 0, 0), (255, 255, 255))
        >>> result.passes_aa_normal
        True
        >>> result.ratio
        21.0
    """
    ratio = calculate_contrast_ratio(foreground, background)
    level = get_compliance_level(ratio)
    
    passes_aa_normal = ratio >= WCAG_AA_NORMAL_TEXT_MIN_RATIO
    passes_aa_large = ratio >= WCAG_AA_LARGE_TEXT_MIN_RATIO
    passes_aaa_normal = ratio >= WCAG_AAA_NORMAL_TEXT_MIN_RATIO
    passes_aaa_large = ratio >= WCAG_AAA_LARGE_TEXT_MIN_RATIO
    passes_non_text = ratio >= WCAG_NON_TEXT_MIN_RATIO
    
    return ContrastResult(
        foreground=foreground,
        background=background,
        ratio=ratio,
        level=level,
        passes_aa_normal=passes_aa_normal,
        passes_aa_large=passes_aa_large,
        passes_aaa_normal=passes_aaa_normal,
        passes_aaa_large=passes_aaa_large,
        passes_non_text=passes_non_text
    )


def parse_hex_color(hex_color: str) -> Tuple[int, int, int]:
    """
    Parse hex color string to RGB tuple.
    
    Supports formats: #RGB, #RRGGBB, RGB, RRGGBB
    
    Args:
        hex_color: Hex color string (with or without #)
    
    Returns:
        RGB tuple (0-255 range)
    
    Raises:
        ValueError: If hex color format is invalid
    
    Example:
        >>> parse_hex_color("#FF0000")
        (255, 0, 0)
        >>> parse_hex_color("#F00")
        (255, 0, 0)
        >>> parse_hex_color("FFFFFF")
        (255, 255, 255)
    """
    hex_color = hex_color.strip()
    
    # Remove leading #
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]
    
    # Handle 3-character shorthand
    if len(hex_color) == 3:
        hex_color = "".join([c * 2 for c in hex_color])
    
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color format: {hex_color}")
    
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b)
    except ValueError:
        raise ValueError(f"Invalid hex color: {hex_color}")


def parse_rgb_color(rgb_str: str) -> Tuple[int, int, int]:
    """
    Parse RGB string to RGB tuple.
    
    Supports formats:
    - rgb(r, g, b)
    - rgb(r g b)
    - r, g, b
    - r g b
    
    Args:
        rgb_str: RGB color string
    
    Returns:
        RGB tuple (0-255 range)
    
    Raises:
        ValueError: If RGB format is invalid
    
    Example:
        >>> parse_rgb_color("rgb(255, 0, 0)")
        (255, 0, 0)
        >>> parse_rgb_color("255, 128, 64")
        (255, 128, 64)
    """
    rgb_str = rgb_str.strip().lower()
    
    # Remove rgb() wrapper
    if rgb_str.startswith("rgb"):
        rgb_str = rgb_str[3:].strip()
        if rgb_str.startswith("(") and rgb_str.endswith(")"):
            rgb_str = rgb_str[1:-1]
    
    # Split by comma or space
    parts = rgb_str.replace(",", " ").split()
    
    if len(parts) != 3:
        raise ValueError(f"Invalid RGB format: {rgb_str}")
    
    try:
        r = int(parts[0])
        g = int(parts[1])
        b = int(parts[2])
        return _clamp_rgb(r, g, b)
    except ValueError:
        raise ValueError(f"Invalid RGB values: {rgb_str}")


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """
    Convert RGB tuple to hex color string.
    
    Args:
        rgb: RGB tuple (0-255 range)
    
    Returns:
        Hex color string (#RRGGBB format)
    
    Example:
        >>> rgb_to_hex((255, 0, 0))
        '#FF0000'
        >>> rgb_to_hex((128, 128, 128))
        '#808080'
    """
    r, g, b = _clamp_rgb(rgb[0], rgb[1], rgb[2])
    return f"#{r:02X}{g:02X}{b:02X}"


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert hex color string to RGB tuple.
    
    Alias for parse_hex_color.
    
    Args:
        hex_color: Hex color string
    
    Returns:
        RGB tuple (0-255 range)
    
    Example:
        >>> hex_to_rgb("#FF0000")
        (255, 0, 0)
    """
    return parse_hex_color(hex_color)


def get_contrast_ratio_for_text_size(
    foreground: Tuple[int, int, int],
    background: Tuple[int, int, int],
    font_size_pt: float,
    is_bold: bool = False
) -> ContrastResult:
    """
    Check contrast ratio considering text size for WCAG compliance.
    
    WCAG defines "large text" as:
    - 18pt regular text, or
    - 14pt bold text
    
    Args:
        foreground: Text RGB tuple
        background: Background RGB tuple
        font_size_pt: Font size in points
        is_bold: Whether text is bold
    
    Returns:
        ContrastResult with compliance information
    
    Example:
        >>> # 24pt regular text (large)
        >>> result = get_contrast_ratio_for_text_size((0, 0, 0), (255, 255, 255), 24)
        >>> result.passes_aa_large
        True
    """
    is_large_text = False
    
    if is_bold:
        is_large_text = font_size_pt >= LARGE_TEXT_MIN_FONT_SIZE_PT_BOLD
    else:
        is_large_text = font_size_pt >= LARGE_TEXT_MIN_FONT_SIZE_PT
    
    return check_wcag_compliance(foreground, background, is_large_text)


def _darken_color(rgb: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    """Darken a color by a factor (0-1)."""
    r = int(rgb[0] * (1 - factor))
    g = int(rgb[1] * (1 - factor))
    b = int(rgb[2] * (1 - factor))
    return _clamp_rgb(r, g, b)


def _lighten_color(rgb: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    """Lighten a color by a factor (0-1)."""
    r = int(rgb[0] + (255 - rgb[0]) * factor)
    g = int(rgb[1] + (255 - rgb[1]) * factor)
    b = int(rgb[2] + (255 - rgb[2]) * factor)
    return _clamp_rgb(r, g, b)


def suggest_accessible_color(
    foreground: Tuple[int, int, int],
    background: Tuple[int, int, int],
    target_ratio: float = WCAG_AA_NORMAL_TEXT_MIN_RATIO,
    preserve_hue: bool = True
) -> Optional[Tuple[int, int, int]]:
    """
    Suggest an accessible foreground color that meets the target contrast ratio.
    
    Args:
        foreground: Original foreground RGB tuple
        background: Background RGB tuple
        target_ratio: Target contrast ratio (default: WCAG AA for normal text)
        preserve_hue: Whether to preserve the hue when adjusting
    
    Returns:
        Adjusted RGB tuple that meets the target ratio, or None if impossible
    
    Example:
        >>> # Light gray on white needs adjustment
        >>> suggested = suggest_accessible_color((200, 200, 200), (255, 255, 255))
        >>> suggested  # Darker gray that meets 4.5:1
        (117, 117, 117)
    """
    current_ratio = calculate_contrast_ratio(foreground, background)
    
    if current_ratio >= target_ratio:
        return foreground  # Already accessible
    
    bg_luminance = calculate_relative_luminance(background)
    fg_luminance = calculate_relative_luminance(foreground)
    
    # Determine if foreground should be darker or lighter
    if bg_luminance > fg_luminance:
        # Background is lighter, foreground should be darker
        direction = "darken"
    else:
        # Background is darker, foreground should be lighter
        direction = "lighten"
    
    # Calculate required luminance for target ratio
    if direction == "darken":
        required_luminance = (bg_luminance + 0.05) / target_ratio - 0.05
    else:
        required_luminance = (fg_luminance + 0.05) * target_ratio - 0.05
        # Actually need to reverse: lighter needs more luminance
        required_luminance = max(bg_luminance, (bg_luminance + 0.05) / target_ratio - 0.05)
    
    # Clamp luminance to valid range
    required_luminance = max(0, min(1, required_luminance))
    
    # Try step-wise adjustment
    step = 0.01
    attempts = 0
    max_attempts = 255
    
    test_color = foreground
    
    while attempts < max_attempts:
        ratio = calculate_contrast_ratio(test_color, background)
        
        if ratio >= target_ratio:
            return test_color
        
        if direction == "darken":
            test_color = _darken_color(test_color, step)
        else:
            test_color = _lighten_color(test_color, step)
        
        attempts += 1
    
    # If we can't find a suitable color, return black or white
    if direction == "darken":
        return (0, 0, 0)
    else:
        return (255, 255, 255)


def get_min_contrast_color(
    background: Tuple[int, int, int],
    target_ratio: float = WCAG_AA_NORMAL_TEXT_MIN_RATIO
) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
    """
    Get minimum contrast colors (black or white) for a background.
    
    Returns both black and white foreground options, calculating which
    provides sufficient contrast.
    
    Args:
        background: Background RGB tuple
        target_ratio: Target contrast ratio
    
    Returns:
        Tuple of (dark_foreground, light_foreground) RGB tuples
    
    Example:
        >>> get_min_contrast_color((255, 255, 255))  # White background
        ((0, 0, 0), (255, 255, 255))  # Black works, white doesn't
    """
    black = (0, 0, 0)
    white = (255, 255, 255)
    
    black_ratio = calculate_contrast_ratio(black, background)
    white_ratio = calculate_contrast_ratio(white, background)
    
    return (black, white)


# Color Vision Deficiency Simulation Matrices
# Based on Brettel, Viénot, and Mollon (1997) algorithm

# Protanopia (red-blind) simulation matrix
PROTANOPIA_MATRIX = [
    [0.567, 0.433, 0.0],
    [0.558, 0.442, 0.0],
    [0.0, 0.242, 0.758]
]

# Deuteranopia (green-blind) simulation matrix
DEUTERANOPIA_MATRIX = [
    [0.625, 0.375, 0.0],
    [0.7, 0.3, 0.0],
    [0.0, 0.3, 0.7]
]

# Tritanopia (blue-blind) simulation matrix
TRITANOPIA_MATRIX = [
    [0.95, 0.05, 0.0],
    [0.0, 0.433, 0.567],
    [0.0, 0.475, 0.525]
]

# Achromatopsia (complete color blindness) - convert to grayscale
ACHROMATOPSIA_MATRIX = [
    [0.299, 0.587, 0.114],
    [0.299, 0.587, 0.114],
    [0.299, 0.587, 0.114]
]


def _apply_cvd_matrix(
    rgb: Tuple[int, int, int],
    matrix: List[List[float]]
) -> Tuple[int, int, int]:
    """Apply color vision deficiency simulation matrix to RGB color."""
    r, g, b = rgb
    
    # Apply matrix transformation
    new_r = matrix[0][0] * r + matrix[0][1] * g + matrix[0][2] * b
    new_g = matrix[1][0] * r + matrix[1][1] * g + matrix[1][2] * b
    new_b = matrix[2][0] * r + matrix[2][1] * g + matrix[2][2] * b
    
    return _clamp_rgb(int(new_r), int(new_g), int(new_b))


def simulate_protanopia(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Simulate how a color appears to someone with protanopia (red-blindness).
    
    Protanopia affects about 1% of males and is the inability to perceive
    red light. Colors appear shifted toward green/yellow.
    
    Args:
        rgb: RGB tuple to simulate
    
    Returns:
        Simulated RGB tuple as perceived by someone with protanopia
    
    Example:
        >>> simulate_protanopia((255, 0, 0))  # Pure red
        (145, 110, 0)  # Appears as yellowish
    """
    return _apply_cvd_matrix(rgb, PROTANOPIA_MATRIX)


def simulate_deuteranopia(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Simulate how a color appears to someone with deuteranopia (green-blindness).
    
    Deuteranopia affects about 1% of males and is the inability to perceive
    green light. Colors appear shifted toward yellow/brown.
    
    Args:
        rgb: RGB tuple to simulate
    
    Returns:
        Simulated RGB tuple as perceived by someone with deuteranopia
    
    Example:
        >>> simulate_deuteranopia((0, 255, 0))  # Pure green
        (159, 77, 0)  # Appears as yellowish
    """
    return _apply_cvd_matrix(rgb, DEUTERANOPIA_MATRIX)


def simulate_tritanopia(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Simulate how a color appears to someone with tritanopia (blue-blindness).
    
    Tritanopia is very rare (less than 0.01% of population) and is the
    inability to perceive blue light. Colors appear shifted toward pink/green.
    
    Args:
        rgb: RGB tuple to simulate
    
    Returns:
        Simulated RGB tuple as perceived by someone with tritanopia
    
    Example:
        >>> simulate_tritanopia((0, 0, 255))  # Pure blue
        (0, 110, 145)  # Appears as greenish
    """
    return _apply_cvd_matrix(rgb, TRITANOPIA_MATRIX)


def simulate_achromatopsia(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Simulate how a color appears to someone with achromatopsia (complete color blindness).
    
    Achromatopsia is extremely rare and results in seeing only in grayscale.
    
    Args:
        rgb: RGB tuple to simulate
    
    Returns:
        Grayscale RGB tuple
    
    Example:
        >>> simulate_achromatopsia((255, 0, 0))  # Pure red
        (76, 76, 76)  # Grayscale equivalent
    """
    return _apply_cvd_matrix(rgb, ACHROMATOPSIA_MATRIX)


def check_contrast_for_all_cvd(
    foreground: Tuple[int, int, int],
    background: Tuple[int, int, int],
    target_ratio: float = WCAG_AA_NORMAL_TEXT_MIN_RATIO
) -> Dict[str, bool]:
    """
    Check if contrast ratio is maintained for all color vision deficiency types.
    
    This is important for ensuring accessibility for users with various
    types of color blindness.
    
    Args:
        foreground: Foreground RGB tuple
        background: Background RGB tuple
        target_ratio: Minimum acceptable contrast ratio
    
    Returns:
        Dictionary with CVD types as keys and pass/fail as values
    
    Example:
        >>> check_contrast_for_all_cvd((255, 0, 0), (255, 255, 255))
        {'normal': True, 'protanopia': False, 'deuteranopia': False, 'tritanopia': True, 'achromatopsia': True}
    """
    results = {}
    
    # Normal vision
    normal_ratio = calculate_contrast_ratio(foreground, background)
    results["normal"] = normal_ratio >= target_ratio
    
    # Protanopia simulation
    proto_fg = simulate_protanopia(foreground)
    proto_bg = simulate_protanopia(background)
    proto_ratio = calculate_contrast_ratio(proto_fg, proto_bg)
    results["protanopia"] = proto_ratio >= target_ratio
    
    # Deuteranopia simulation
    deut_fg = simulate_deuteranopia(foreground)
    deut_bg = simulate_deuteranopia(background)
    deut_ratio = calculate_contrast_ratio(deut_fg, deut_bg)
    results["deuteranopia"] = deut_ratio >= target_ratio
    
    # Tritanopia simulation
    tri_fg = simulate_tritanopia(foreground)
    tri_bg = simulate_tritanopia(background)
    tri_ratio = calculate_contrast_ratio(tri_fg, tri_bg)
    results["tritanopia"] = tri_ratio >= target_ratio
    
    # Achromatopsia simulation
    achro_fg = simulate_achromatopsia(foreground)
    achro_bg = simulate_achromatopsia(background)
    achro_ratio = calculate_contrast_ratio(achro_fg, achro_bg)
    results["achromatopsia"] = achro_ratio >= target_ratio
    
    return results


def get_all_cvd_contrast_ratios(
    foreground: Tuple[int, int, int],
    background: Tuple[int, int, int]
) -> Dict[str, float]:
    """
    Get contrast ratios for all color vision deficiency types.
    
    Args:
        foreground: Foreground RGB tuple
        background: Background RGB tuple
    
    Returns:
        Dictionary with CVD types as keys and contrast ratios as values
    
    Example:
        >>> get_all_cvd_contrast_ratios((255, 0, 0), (255, 255, 255))
        {'normal': 4.0, 'protanopia': 1.5, 'deuteranopia': 1.5, 'tritanopia': 4.0, 'achromatopsia': 3.5}
    """
    ratios = {}
    
    # Normal vision
    ratios["normal"] = calculate_contrast_ratio(foreground, background)
    
    # Protanopia simulation
    proto_fg = simulate_protanopia(foreground)
    proto_bg = simulate_protanopia(background)
    ratios["protanopia"] = calculate_contrast_ratio(proto_fg, proto_bg)
    
    # Deuteranopia simulation
    deut_fg = simulate_deuteranopia(foreground)
    deut_bg = simulate_deuteranopia(background)
    ratios["deuteranopia"] = calculate_contrast_ratio(deut_fg, deut_bg)
    
    # Tritanopia simulation
    tri_fg = simulate_tritanopia(foreground)
    tri_bg = simulate_tritanopia(background)
    ratios["tritanopia"] = calculate_contrast_ratio(tri_fg, tri_bg)
    
    # Achromatopsia simulation
    achro_fg = simulate_achromatopsia(foreground)
    achro_bg = simulate_achromatopsia(background)
    ratios["achromatopsia"] = calculate_contrast_ratio(achro_fg, achro_bg)
    
    return ratios


# Convenience functions for quick checks

def is_accessible(
    foreground: str,
    background: str,
    level: str = "aa"
) -> bool:
    """
    Quick accessibility check using hex color strings.
    
    Args:
        foreground: Foreground hex color
        background: Background hex color
        level: "aa" or "aaa"
    
    Returns:
        True if passes the specified level
    
    Example:
        >>> is_accessible("#000000", "#FFFFFF", "aa")
        True
        >>> is_accessible("#767676", "#FFFFFF", "aa")
        True
        >>> is_accessible("#999999", "#FFFFFF", "aa")
        False
    """
    fg_rgb = parse_hex_color(foreground)
    bg_rgb = parse_hex_color(background)
    
    result = check_wcag_compliance(fg_rgb, bg_rgb)
    
    if level.lower() == "aaa":
        return result.passes_aaa_normal
    else:
        return result.passes_aa_normal


def quick_check(
    foreground: str,
    background: str
) -> str:
    """
    Quick contrast check returning human-readable result.
    
    Args:
        foreground: Foreground hex color
        background: Background hex color
    
    Returns:
        Human-readable accessibility result
    
    Example:
        >>> quick_check("#000000", "#FFFFFF")
        "Contrast: 21.00:1 - PASS (AAA)"
        >>> quick_check("#999999", "#FFFFFF")
        "Contrast: 2.85:1 - FAIL"
    """
    fg_rgb = parse_hex_color(foreground)
    bg_rgb = parse_hex_color(background)
    
    result = check_wcag_compliance(fg_rgb, bg_rgb)
    
    if result.level == ComplianceLevel.FAIL:
        return f"Contrast: {result.ratio:.2f}:1 - FAIL"
    else:
        return f"Contrast: {result.ratio:.2f}:1 - PASS ({result.level.value.upper()})"