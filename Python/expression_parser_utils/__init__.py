"""
Expression Parser Utils - 安全的数学表达式解析和求值工具

功能:
- 安全解析和计算数学表达式（不使用 eval）
- 支持变量替换
- 支持自定义函数
- 支持常用数学函数（sin, cos, tan, sqrt, log, abs 等）
- 支持比较运算符和布尔逻辑
- 表达式验证和语法检查
- 变量提取

作者: AllToolkit Auto-Generator
日期: 2026-04-29
"""

from .parser import ExpressionParser, ExpressionError
from .evaluator import (
    safe_eval, 
    validate_expression, 
    extract_variables, 
    MathFunctions
)
from .functions import BUILTIN_FUNCTIONS

__all__ = [
    'ExpressionParser',
    'ExpressionError',
    'safe_eval',
    'validate_expression',
    'extract_variables',
    'MathFunctions',
    'BUILTIN_FUNCTIONS'
]

__version__ = '1.0.0'