"""
TSV Utilities - Tab-Separated Values processing toolkit.

A comprehensive, zero-dependency library for reading, writing, and 
manipulating TSV (Tab-Separated Values) files and data.
"""

from .tsv_utils import (
    # Exceptions
    TSVError,
    TSVParseError,
    TSVWriteError,
    # Reading functions
    read_tsv,
    read_tsv_as_dicts,
    read_tsv_streaming,
    parse_tsv_string,
    # Writing functions
    write_tsv,
    write_tsv_from_dicts,
    to_tsv_string,
    dicts_to_tsv_string,
    # Utility functions
    validate_tsv,
    get_tsv_info,
    merge_tsv_files,
    # Helper functions
    _detect_bom,
    _normalize_line_endings,
    _parse_tsv_line,
    _serialize_field,
    _infer_type,
)

__version__ = '1.0.0'
__author__ = 'AllToolkit'

__all__ = [
    # Exceptions
    'TSVError',
    'TSVParseError',
    'TSVWriteError',
    # Reading functions
    'read_tsv',
    'read_tsv_as_dicts',
    'read_tsv_streaming',
    'parse_tsv_string',
    # Writing functions
    'write_tsv',
    'write_tsv_from_dicts',
    'to_tsv_string',
    'dicts_to_tsv_string',
    # Utility functions
    'validate_tsv',
    'get_tsv_info',
    'merge_tsv_files',
]