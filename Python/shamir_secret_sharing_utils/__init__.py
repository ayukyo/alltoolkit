#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Shamir's Secret Sharing Utilities
================================================
A comprehensive Shamir's Secret Sharing (SSS) implementation.

This module provides secure secret splitting and reconstruction capabilities
using Shamir's Secret Sharing algorithm with information-theoretic security.

Quick Start:
    >>> from shamir_secret_sharing_utils import split_string, reconstruct_secret_string
    >>> shares = split_string("my secret", threshold=3, num_shares=5)
    >>> secret = reconstruct_secret_string(shares.shares[:3])
    
    >>> # Or use the class interface
    >>> from shamir_secret_sharing_utils import ShamirSecretSharing
    >>> sss = ShamirSecretSharing(threshold=3, num_shares=5)
    >>> shares = sss.split("my secret")
    >>> recovered = sss.reconstruct_string(shares.shares[:3])

Features:
    - Split secrets into shares with configurable threshold
    - Reconstruct secrets from shares
    - Support for integers, strings, and binary data
    - GF(2^8) operations for arbitrary-length binary data
    - Share encoding/decoding for storage/transmission
    - SHA-256 hash verification
    - Information-theoretic security (k-1 shares reveal nothing)

Author: AllToolkit Contributors
License: MIT
"""

from .mod import (
    # Core functions
    split_secret,
    reconstruct_secret,
    reconstruct_secret_bytes,
    reconstruct_secret_string,
    verify_secret_hash,
    
    # Convenience functions
    split_string,
    split_int,
    split_bytes,
    
    # Class interface
    ShamirSecretSharing,
    
    # Data classes
    Share,
    ShareSet,
    
    # GF(2^8) functions for binary data
    split_bytes_gf256,
    reconstruct_bytes_gf256,
    
    # Encoding utilities
    encode_shares_compact,
    decode_shares_compact,
    get_share_info,
    validate_share_set,
    
    # Constants
    PRIME_128,
    PRIME_256,
    PRIME_512,
    PRIME_1024,
    DEFAULT_PRIME,
)

__all__ = [
    # Core functions
    'split_secret',
    'reconstruct_secret',
    'reconstruct_secret_bytes',
    'reconstruct_secret_string',
    'verify_secret_hash',
    
    # Convenience functions
    'split_string',
    'split_int',
    'split_bytes',
    
    # Class interface
    'ShamirSecretSharing',
    
    # Data classes
    'Share',
    'ShareSet',
    
    # GF(2^8) functions
    'split_bytes_gf256',
    'reconstruct_bytes_gf256',
    
    # Encoding utilities
    'encode_shares_compact',
    'decode_shares_compact',
    'get_share_info',
    'validate_share_set',
    
    # Constants
    'PRIME_128',
    'PRIME_256',
    'PRIME_512',
    'PRIME_1024',
    'DEFAULT_PRIME',
]

__version__ = '1.0.0'