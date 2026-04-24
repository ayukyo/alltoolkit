"""
Cuckoo Filter - A probabilistic data structure for testing set membership.

Supports insertion, lookup, and deletion with configurable false positive rate.
"""

from .mod import (
    CuckooFilter,
    create_optimal_filter,
    calculate_false_positive_rate,
)

__all__ = [
    'CuckooFilter',
    'create_optimal_filter',
    'calculate_false_positive_rate',
]

__version__ = '1.0.0'