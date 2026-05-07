"""
SWIFT/BIC Utilities - SWIFT银行代码验证工具模块

提供SWIFT/BIC代码的完整验证、解析和生成功能。
零依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0
"""

from .mod import (
    SwiftUtils, BicUtils, SwiftCodeType, SwiftNetworkStatus,
    validate_swift, validate_bic, parse_swift, parse_bic,
    get_swift_bank_code, get_swift_country, is_swift_primary, format_swift
)

__version__ = "1.0.0"
__author__ = "AllToolkit"

__all__ = [
    "SwiftUtils",
    "BicUtils",
    "SwiftCodeType",
    "SwiftNetworkStatus",
    "validate_swift",
    "validate_bic",
    "parse_swift",
    "parse_bic",
    "get_swift_bank_code",
    "get_swift_country",
    "is_swift_primary",
    "format_swift",
]