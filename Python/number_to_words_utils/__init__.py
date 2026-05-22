"""
Number to Words Utility Module

Convert numbers to their word representation in multiple languages.
Supports integers, decimals, currency, and ordinal numbers.
Zero external dependencies.
"""

from .converter import (
    number_to_words,
    number_to_currency_words,
    number_to_ordinal_words,
    get_supported_languages,
)

__version__ = "1.0.0"
__all__ = [
    "number_to_words",
    "number_to_currency_words", 
    "number_to_ordinal_words",
    "get_supported_languages",
]