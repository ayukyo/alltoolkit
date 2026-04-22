"""
Interval Tree Utils - 区间树工具模块
=====================================

提供高效的区间查询数据结构，支持：
- 区间插入和删除
- 查询与指定区间重叠的所有区间
- 查询包含指定点的所有区间
- 查询完全包含指定区间的区间

零外部依赖，纯 Python 实现。

作者: AllToolkit
日期: 2026-04-22
"""

from .interval_tree import IntervalTree, Interval
from .node import IntervalNode

__all__ = ['IntervalTree', 'Interval', 'IntervalNode']
__version__ = '1.0.0'