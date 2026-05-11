"""
自然语言日期解析工具库
Natural Language Date Parser Utilities

解析中文自然语言日期表达式，转换为精确的 datetime 对象。
"""

from .natural_date_utils import (
    NaturalDateParser,
    ParseResult,
    DateType,
    parse,
    parse_with_info,
    is_valid,
    get_date_type,
    parse_range,
    parse_batch,
    extract_dates,
)

__all__ = [
    'NaturalDateParser',
    'ParseResult',
    'DateType',
    'parse',
    'parse_with_info',
    'is_valid',
    'get_date_type',
    'parse_range',
    'parse_batch',
    'extract_dates',
]

__version__ = '1.0.0'