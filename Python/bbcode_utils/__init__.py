"""
BBCode Utilities Package

Zero-dependency BBCode parser and converter.
"""

from .bbcode_utils import (
    BBCodeParser,
    BBCodeNode,
    BBCodeNodeType,
    parse,
    to_html,
    to_text,
    validate,
    get_supported_tags,
    create_safe_parser,
    bbcode,
    DEFAULT_TAGS,
)

__all__ = [
    'BBCodeParser',
    'BBCodeNode',
    'BBCodeNodeType',
    'parse',
    'to_html',
    'to_text',
    'validate',
    'get_supported_tags',
    'create_safe_parser',
    'bbcode',
    'DEFAULT_TAGS',
]

__version__ = '1.0.0'
__author__ = 'AllToolkit'