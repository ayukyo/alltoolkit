"""
区间操作工具模块 (Interval Utilities)

提供高效的区间数据结构操作。
"""

from .mod import (
    Interval, IntervalSet, IntervalMap, RangeSet,
    merge_intervals, interval_intersection, interval_difference,
    interval_union, find_gaps, is_covered, find_containing_interval,
    get_total_coverage
)

__all__ = [
    'Interval',
    'IntervalSet',
    'IntervalMap',
    'RangeSet',
    'merge_intervals',
    'interval_intersection',
    'interval_difference',
    'interval_union',
    'find_gaps',
    'is_covered',
    'find_containing_interval',
    'get_total_coverage',
]