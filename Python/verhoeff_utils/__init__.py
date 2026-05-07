#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Verhoeff Utilities Module

Verhoeff check digit algorithm implementation.
A powerful checksum formula that detects all single-digit errors
and all transposition errors in numeric identifiers.
"""

from .mod import (
    # Core functions
    compute_check_digit,
    compute_check_digit_int,
    validate,
    validate_int,
    append_check_digit,
    append_check_digit_int,
    get_check_digit_position,
    extract_data_digits,
    extract_data_digits_int,
    
    # Error detection
    detect_single_error,
    detect_transposition_error,
    analyze_error,
    
    # Comparison
    compare_with_luhn,
    
    # Batch operations
    validate_batch,
    generate_with_check_digits,
    
    # Educational
    explain_algorithm,
    show_computation_steps,
    
    # Tables
    D5_MULTIPLICATION,
    PERMUTATION,
    INVERSE,
)

__all__ = [
    'compute_check_digit',
    'compute_check_digit_int',
    'validate',
    'validate_int',
    'append_check_digit',
    'append_check_digit_int',
    'get_check_digit_position',
    'extract_data_digits',
    'extract_data_digits_int',
    'detect_single_error',
    'detect_transposition_error',
    'analyze_error',
    'compare_with_luhn',
    'validate_batch',
    'generate_with_check_digits',
    'explain_algorithm',
    'show_computation_steps',
    'D5_MULTIPLICATION',
    'PERMUTATION',
    'INVERSE',
]

__version__ = "1.0.0"