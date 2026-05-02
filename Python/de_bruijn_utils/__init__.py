"""
De Bruijn Sequence Utilities

A comprehensive module for generating and working with De Bruijn sequences.
"""

from .de_bruijn import (
    de_bruijn,
    de_bruijn_generator,
    is_de_bruijn,
    get_all_substrings,
    find_substring_position,
    sequence_to_numbers,
    binary_de_bruijn,
    decimal_de_bruijn,
    hexadecimal_de_bruijn,
    dna_de_bruijn,
    alphabet_de_bruijn,
    find_shortest_containing,
    DeBruijnSequence
)

__all__ = [
    'de_bruijn',
    'de_bruijn_generator',
    'is_de_bruijn',
    'get_all_substrings',
    'find_substring_position',
    'sequence_to_numbers',
    'binary_de_bruijn',
    'decimal_de_bruijn',
    'hexadecimal_de_bruijn',
    'dna_de_bruijn',
    'alphabet_de_bruijn',
    'find_shortest_containing',
    'DeBruijnSequence'
]

__version__ = '1.0.0'