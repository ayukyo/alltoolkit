"""
BWT (Burrows-Wheeler Transform) Utilities Package

Provides Burrows-Wheeler Transform and related compression utilities.
"""

from .mod import (
    bwt_transform,
    bwt_inverse,
    mtf_encode,
    mtf_decode,
    bwt_mtf_compress,
    bwt_mtf_decompress,
    bwt_search,
    bwt_compress_ratio,
    BWT,
    transform,
    inverse,
)

__all__ = [
    'bwt_transform',
    'bwt_inverse',
    'mtf_encode',
    'mtf_decode',
    'bwt_mtf_compress',
    'bwt_mtf_decompress',
    'bwt_search',
    'bwt_compress_ratio',
    'BWT',
    'transform',
    'inverse',
]

__version__ = '1.0.0'