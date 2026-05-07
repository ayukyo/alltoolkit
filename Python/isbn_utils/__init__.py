"""
ISBN Utils - 国际标准书号(ISBN)验证与处理工具库

功能:
- ISBN-10/ISBN-13 验证
- 格式转换 (ISBN-10 ↔ ISBN-13)
- 检验位计算
- 格式化输出
- 信息解析
- 批量操作
- 文本中提取ISBN
- 出版商/注册组识别

零外部依赖，纯Python标准库实现
"""

from .isbn_utils import (
    # 核心类
    ISBN,
    ISBNType,
    ISBNInfo,
    
    # 验证函数
    is_valid_isbn10,
    is_valid_isbn13,
    is_valid_isbn,
    
    # 计算函数
    calculate_isbn10_check_digit,
    calculate_isbn13_check_digit,
    
    # 转换函数
    isbn10_to_isbn13,
    isbn13_to_isbn10,
    
    # 格式化函数
    format_isbn,
    normalize_isbn,
    
    # 解析函数
    parse_isbn,
    extract_isbns,
    
    # 批量操作
    batch_validate,
    
    # 信息函数
    get_isbn_info,
    identify_prefix,
)

__version__ = "1.0.0"
__author__ = "AllToolkit"

__all__ = [
    # 核心类
    "ISBN",
    "ISBNType",
    "ISBNInfo",
    
    # 验证函数
    "is_valid_isbn10",
    "is_valid_isbn13",
    "is_valid_isbn",
    
    # 计算函数
    "calculate_isbn10_check_digit",
    "calculate_isbn13_check_digit",
    
    # 转换函数
    "isbn10_to_isbn13",
    "isbn13_to_isbn10",
    
    # 格式化函数
    "format_isbn",
    "normalize_isbn",
    
    # 解析函数
    "parse_isbn",
    "extract_isbns",
    
    # 批量操作
    "batch_validate",
    
    # 信息函数
    "get_isbn_info",
    "identify_prefix",
]