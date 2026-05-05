"""
Blood Type Utilities - 血型工具模块

提供血型兼容性检测、遗传计算、分布统计等功能。
"""

from .mod import (
    BloodType,
    ABOType,
    RhFactor,
    BloodTypeInfo,
    BloodTypeUtils,
    parse_blood_type,
    can_donate,
    get_compatible_donors,
    get_compatible_recipients,
    child_blood_types,
    get_blood_type_info,
)

__all__ = [
    "BloodType",
    "ABOType",
    "RhFactor",
    "BloodTypeInfo",
    "BloodTypeUtils",
    "parse_blood_type",
    "can_donate",
    "get_compatible_donors",
    "get_compatible_recipients",
    "child_blood_types",
    "get_blood_type_info",
]

__version__ = "1.0.0"