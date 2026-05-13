"""
WCAG Utils - WCAG accessibility compliance checking utilities.

Provides color contrast ratio calculation, WCAG AA/AAA compliance checking,
relative luminance calculation, and color vision deficiency simulation.

Zero external dependencies - uses only Python standard library.
"""

from .wcag_utils import (
    # Core functions
    calculate_relative_luminance,
    calculate_contrast_ratio,
    check_wcag_compliance,
    get_compliance_level,
    
    # Color parsing
    parse_hex_color,
    parse_rgb_color,
    rgb_to_hex,
    hex_to_rgb,
    
    # Contrast helpers
    suggest_accessible_color,
    get_min_contrast_color,
    get_contrast_ratio_for_text_size,
    
    # Color vision deficiency simulation
    simulate_protanopia,
    simulate_deuteranopia,
    simulate_tritanopia,
    simulate_achromatopsia,
    
    # WCAG constants
    WCAG_AA_NORMAL_TEXT_MIN_RATIO,
    WCAG_AA_LARGE_TEXT_MIN_RATIO,
    WCAG_AAA_NORMAL_TEXT_MIN_RATIO,
    WCAG_AAA_LARGE_TEXT_MIN_RATIO,
    WCAG_NON_TEXT_MIN_RATIO,
    
    # Compliance levels
    ComplianceLevel,
    ContrastResult,
)

__version__ = "1.0.0"
__all__ = [
    # Core functions
    "calculate_relative_luminance",
    "calculate_contrast_ratio",
    "check_wcag_compliance",
    "get_compliance_level",
    
    # Color parsing
    "parse_hex_color",
    "parse_rgb_color",
    "rgb_to_hex",
    "hex_to_rgb",
    
    # Contrast helpers
    "suggest_accessible_color",
    "get_min_contrast_color",
    "get_contrast_ratio_for_text_size",
    
    # Color vision deficiency simulation
    "simulate_protanopia",
    "simulate_deuteranopia",
    "simulate_tritanopia",
    "simulate_achromatopsia",
    
    # Constants
    "WCAG_AA_NORMAL_TEXT_MIN_RATIO",
    "WCAG_AA_LARGE_TEXT_MIN_RATIO",
    "WCAG_AAA_NORMAL_TEXT_MIN_RATIO",
    "WCAG_AAA_LARGE_TEXT_MIN_RATIO",
    "WCAG_NON_TEXT_MIN_RATIO",
    
    # Classes
    "ComplianceLevel",
    "ContrastResult",
]