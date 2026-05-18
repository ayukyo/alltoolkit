"""
Age Calculator Utilities - 年龄计算工具模块

提供完整的年龄计算功能，包括精确年龄、生日倒计时、年龄里程碑、
代际分类、年龄差计算等。

Usage:
    from age_calculator_utils import calculate_age, format_age
    
    # 计算年龄
    age = calculate_age("1990-05-15")
    print(f"年龄: {age}岁")
    
    # 格式化年龄
    formatted = format_age("1990-05-15")
    print(f"精确年龄: {formatted}")  # 输出: 34岁2个月5天
"""

from .mod import (
    AgeCalculatorUtils,
    Generation,
    calculate_age,
    calculate_exact_age,
    days_until_birthday,
    get_generation,
    format_age
)

__version__ = "1.0.0"
__all__ = [
    "AgeCalculatorUtils",
    "Generation",
    "calculate_age",
    "calculate_exact_age",
    "days_until_birthday",
    "get_generation",
    "format_age"
]