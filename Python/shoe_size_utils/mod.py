#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Shoe Size Conversion Utilities Module
=====================================================
A comprehensive shoe size conversion and validation module for Python with zero external dependencies.

Features:
    - International shoe size conversion (CN, EU, US, UK, JP, AU, KR, BR, MX, TW)
    - Adult and children shoe size support
    - Men's and women's shoe size differentiation
    - Shoe size validation and range checking
    - Foot length to shoe size conversion
    - Size chart generation
    - Size recommendation based on foot measurements
    - Brand-specific size adjustment

Shoe Size Systems:
    - CN (China): Uses foot length in cm (e.g., 24.5)
    - EU (Europe): Uses Paris point system (e.g., 39)
    - US (United States): Separate men/women scales (e.g., US 7, US 8.5)
    - UK (United Kingdom): Based on barleycorn (e.g., UK 6)
    - JP (Japan): Uses foot length in cm (e.g., 24.5)
    - AU (Australia): Same as UK for adults
    - KR (Korea): Uses mm measurement (e.g., 245)
    - BR (Brazil): Uses a unique scale (e.g., 38)
    - MX (Mexico): Based on US scale (e.g., 24)
    - TW (Taiwan): Uses EU-like scale

Author: AllToolkit Contributors
License: MIT
Date: 2026-05-07
"""

from typing import Union, Tuple, Optional, List, Dict
from dataclasses import dataclass
from enum import Enum
import math


# ============================================================================
# Constants
# ============================================================================

# Foot length conversion constants
CM_TO_INCH = 0.393701
INCH_TO_CM = 2.54
MM_TO_CM = 0.1
CM_TO_MM = 10

# Paris point (European sizing unit): 2/3 cm
PARIS_POINT = 2 / 3  # cm

# Barleycorn (UK sizing unit): 1/3 inch
BARLEYCORN = 1 / 3  # inch

# Size ranges for validation
SIZE_RANGES = {
    'adult': {
        'CN': (22.0, 30.0),  # cm
        'EU': (35, 48),
        'US_men': (4, 14),
        'US_women': (5, 15),
        'UK': (2, 13),
        'JP': (22.0, 30.0),  # cm
        'KR': (220, 300),  # mm
    },
    'child': {
        'CN': (14.0, 22.0),  # cm
        'EU': (18, 34),
        'US': (1, 13),  # children scale
        'UK': (0, 12),  # children scale
        'JP': (14.0, 22.0),  # cm
        'KR': (140, 220),  # mm
    },
    'infant': {
        'CN': (8.0, 14.0),  # cm
        'EU': (10, 18),
        'US': (0, 5),  # infant scale
        'UK': (0, 4),  # infant scale
        'JP': (8.0, 14.0),  # cm
        'KR': (80, 140),  # mm
    },
    'toddler': {
        'CN': (14.0, 18.0),  # cm
        'EU': (18, 22),
        'US': (5, 10),  # toddler scale
        'UK': (4, 8),  # toddler scale
        'JP': (14.0, 18.0),  # cm
        'KR': (140, 180),  # mm
    }
}

# Brand-specific size adjustments (relative to standard)
BRAND_ADJUSTMENTS = {
    'Nike': {'US_men': 0.5, 'US_women': 0.5},
    'Adidas': {'US_men': 0, 'US_women': 0},
    'Puma': {'US_men': 0.5, 'US_women': 0.5},
    'Converse': {'US_men': 0.5, 'US_women': 0.5},
    'Vans': {'US_men': 0.5, 'US_women': 0.5},
    'NewBalance': {'US_men': 0, 'US_women': 0},
    'Asics': {'US_men': 0.5, 'US_women': 0.5},
    'Reebok': {'US_men': 0, 'US_women': 0},
    'Saucony': {'US_men': 0.5, 'US_women': 0.5},
    'Hoka': {'US_men': -0.5, 'US_women': -0.5},
    'Clarks': {'UK': 0},
    'DrMartens': {'UK': -1},
    'Timberland': {'US_men': 0.5, 'US_women': 0.5},
    'UGG': {'US_women': 1},
    'Crocs': {'US_men': 0.5, 'US_women': 0.5},
    'Skechers': {'US_men': 0.5, 'US_women': 0.5},
}

# Size category labels
SIZE_CATEGORY_LABELS = {
    'extra_small': {'cn': '特小', 'en': 'Extra Small'},
    'small': {'cn': '小', 'en': 'Small'},
    'medium': {'cn': '中', 'en': 'Medium'},
    'large': {'cn': '大', 'en': 'Large'},
    'extra_large': {'cn': '特大', 'en': 'Extra Large'},
}


# ============================================================================
# Enums
# ============================================================================

class SizeSystem(Enum):
    """鞋码系统枚举"""
    CN = 'CN'      # China (foot length in cm)
    EU = 'EU'      # Europe (Paris point)
    US = 'US'      # United States
    UK = 'UK'      # United Kingdom
    JP = 'JP'      # Japan (foot length in cm)
    AU = 'AU'      # Australia (same as UK)
    KR = 'KR'      # Korea (foot length in mm)
    BR = 'BR'      # Brazil
    MX = 'MX'      # Mexico
    TW = 'TW'      # Taiwan


class Gender(Enum):
    """性别枚举"""
    MALE = 'male'
    FEMALE = 'female'
    UNISEX = 'unisex'


class AgeGroup(Enum):
    """年龄组枚举"""
    ADULT = 'adult'
    CHILD = 'child'
    INFANT = 'infant'
    TODDLER = 'toddler'


class SizeCategory(Enum):
    """尺码分类枚举"""
    EXTRA_SMALL = 'extra_small'
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    EXTRA_LARGE = 'extra_large'


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class ShoeSize:
    """鞋码数据类"""
    system: str
    size: float
    gender: str
    age_group: str
    foot_length_cm: Optional[float] = None
    
    def __str__(self):
        return f"{self.system} {self.size} ({self.gender}, {self.age_group})"


@dataclass
class SizeConversionResult:
    """尺码转换结果"""
    original_system: str
    original_size: float
    original_gender: str
    original_age_group: str
    conversions: Dict[str, float]
    foot_length_cm: float
    foot_length_inch: float
    size_category: str
    size_category_cn: str
    size_category_en: str
    in_range: bool
    recommendations: List[str]


@dataclass
class SizeRecommendation:
    """尺码推荐"""
    recommended_size: float
    recommended_system: str
    foot_length_cm: float
    comfort_margin_cm: float
    size_range: Tuple[float, float]
    notes: List[str]


# ============================================================================
# Core Conversion Functions
# ============================================================================

def foot_length_to_cn(foot_length_cm: float) -> float:
    """
    脚长转中国鞋码 (CN).
    
    中国鞋码直接使用脚长厘米数，如 24.5cm = CN 24.5
    
    Args:
        foot_length_cm: 脚长 (厘米)
    
    Returns:
        CN 鞋码
    
    Examples:
        >>> foot_length_to_cn(24.5)
        24.5
        >>> foot_length_to_cn(26.0)
        26.0
    """
    return round(foot_length_cm, 1)


def foot_length_to_eu(foot_length_cm: float) -> float:
    """
    脚长转欧洲鞋码 (EU).
    
    EU 鞋码公式: EU = (foot_length_cm * 1.5) + 2
    基于 Paris point 系统 (2/3 cm)
    
    Args:
        foot_length_cm: 脚长 (厘米)
    
    Returns:
        EU 鞋码
    
    Examples:
        >>> foot_length_to_eu(24.5)
        38.75
        >>> foot_length_to_eu(26.0)
        41.0
    """
    # EU = 3/2 * foot_length + 2 (simplified formula)
    eu_size = (foot_length_cm * 1.5) + 2
    return round(eu_size, 0)


def foot_length_to_us_men(foot_length_cm: float) -> float:
    """
    脚长转美国男鞋码.
    
    US Men 鞋码公式: US = (foot_length_inch * 3) - 24
    基于 barleycorn 系统 (1/3 inch)
    
    Args:
        foot_length_cm: 脚长 (厘米)
    
    Returns:
        US 男鞋码
    
    Examples:
        >>> foot_length_to_us_men(26.0)
        8.5
    """
    foot_length_inch = foot_length_cm * CM_TO_INCH
    us_size = (foot_length_inch * 3) - 24
    return round(us_size, 1)


def foot_length_to_us_women(foot_length_cm: float) -> float:
    """
    脚长转美国女鞋码.
    
    US Women 鞋码公式: US = (foot_length_inch * 3) - 21.5
    女鞋码比男鞋码大约 1.5
    
    Args:
        foot_length_cm: 脚长 (厘米)
    
    Returns:
        US 女鞋码
    
    Examples:
        >>> foot_length_to_us_women(24.5)
        7.5
    """
    foot_length_inch = foot_length_cm * CM_TO_INCH
    us_size = (foot_length_inch * 3) - 21.5
    return round(us_size, 1)


def foot_length_to_us_child(foot_length_cm: float) -> float:
    """
    脚长转美国儿童鞋码.
    
    US Children 鞋码公式: US = (foot_length_inch * 3) - 12
    
    Args:
        foot_length_cm: 脚长 (厘米)
    
    Returns:
        US 儿童鞋码
    
    Examples:
        >>> foot_length_to_us_child(18.0)
        9.5
    """
    foot_length_inch = foot_length_cm * CM_TO_INCH
    us_size = (foot_length_inch * 3) - 12
    return round(us_size, 1)


def foot_length_to_uk(foot_length_cm: float) -> float:
    """
    脚长转英国鞋码.
    
    UK 鞋码公式: UK = (foot_length_inch * 3) - 25
    UK 成人鞋码
    
    Args:
        foot_length_cm: 脚长 (厘米)
    
    Returns:
        UK 鞋码
    
    Examples:
        >>> foot_length_to_uk(26.0)
        7.5
    """
    foot_length_inch = foot_length_cm * CM_TO_INCH
    uk_size = (foot_length_inch * 3) - 25
    return round(uk_size, 1)


def foot_length_to_uk_child(foot_length_cm: float) -> float:
    """
    脚长转英国儿童鞋码.
    
    UK Children 鞋码公式: UK = (foot_length_inch * 3) - 13
    
    Args:
        foot_length_cm: 脚长 (厘米)
    
    Returns:
        UK 儿童鞋码
    
    Examples:
        >>> foot_length_to_uk_child(18.0)
        8.5
    """
    foot_length_inch = foot_length_cm * CM_TO_INCH
    uk_size = (foot_length_inch * 3) - 13
    return round(uk_size, 1)


def foot_length_to_jp(foot_length_cm: float) -> float:
    """
    脚长转日本鞋码 (JP).
    
    日本鞋码直接使用脚长厘米数，与中国相同
    
    Args:
        foot_length_cm: 脚长 (厘米)
    
    Returns:
        JP 鞋码
    
    Examples:
        >>> foot_length_to_jp(24.5)
        24.5
    """
    return round(foot_length_cm, 1)


def foot_length_to_kr(foot_length_cm: float) -> int:
    """
    脚长转韩国鞋码 (KR).
    
    韩国鞋码使用毫米数
    
    Args:
        foot_length_cm: 脚长 (厘米)
    
    Returns:
        KR 鞋码 (毫米)
    
    Examples:
        >>> foot_length_to_kr(24.5)
        245
    """
    return round(foot_length_cm * 10)


def foot_length_to_br(foot_length_cm: float) -> float:
    """
    脚长转巴西鞋码 (BR).
    
    BR 鞋码公式: BR = (foot_length_cm * 1.5) + 2 - 32 = foot_length_cm * 1.5 - 30
    
    Args:
        foot_length_cm: 脚长 (厘米)
    
    Returns:
        BR 鞋码
    
    Examples:
        >>> foot_length_to_br(24.5)
        7.0
    """
    br_size = foot_length_cm * 1.5 - 30
    return round(br_size, 0)


def foot_length_to_mx(foot_length_cm: float) -> float:
    """
    脚长转墨西哥鞋码 (MX).
    
    MX 鞋码公式: MX = US + 17
    
    Args:
        foot_length_cm: 脚长 (厘米)
    
    Returns:
        MX 鞋码
    
    Examples:
        >>> foot_length_to_mx(26.0)
        26.5
    """
    us_size = foot_length_to_us_men(foot_length_cm)
    mx_size = us_size + 17
    return round(mx_size, 1)


def foot_length_to_tw(foot_length_cm: float) -> float:
    """
    脚长转台湾鞋码 (TW).
    
    TW 鞋码公式: TW = EU + 1
    
    Args:
        foot_length_cm: 脚长 (厘米)
    
    Returns:
        TW 鞋码
    
    Examples:
        >>> foot_length_to_tw(24.5)
        40.0
    """
    eu_size = foot_length_to_eu(foot_length_cm)
    tw_size = eu_size + 1
    return round(tw_size, 0)


# ============================================================================
# Size to Foot Length Functions (Reverse Conversion)
# ============================================================================

def cn_to_foot_length(cn_size: float) -> float:
    """
    中国鞋码转脚长.
    
    Args:
        cn_size: CN 鞋码
    
    Returns:
        脚长 (厘米)
    
    Examples:
        >>> cn_to_foot_length(24.5)
        24.5
    """
    return cn_size


def eu_to_foot_length(eu_size: float) -> float:
    """
    欧洲鞋码转脚长.
    
    Args:
        eu_size: EU 鞋码
    
    Returns:
        脚长 (厘米)
    
    Examples:
        >>> eu_to_foot_length(39)
        24.67
    """
    foot_length_cm = (eu_size - 2) / 1.5
    return round(foot_length_cm, 2)


def us_men_to_foot_length(us_size: float) -> float:
    """
    美国男鞋码转脚长.
    
    Args:
        us_size: US 男鞋码
    
    Returns:
        脚长 (厘米)
    
    Examples:
        >>> us_men_to_foot_length(8.5)
        26.0
    """
    foot_length_inch = (us_size + 24) / 3
    foot_length_cm = foot_length_inch * INCH_TO_CM
    return round(foot_length_cm, 2)


def us_women_to_foot_length(us_size: float) -> float:
    """
    美国女鞋码转脚长.
    
    Args:
        us_size: US 女鞋码
    
    Returns:
        脚长 (厘米)
    
    Examples:
        >>> us_women_to_foot_length(7.5)
        24.5
    """
    foot_length_inch = (us_size + 21.5) / 3
    foot_length_cm = foot_length_inch * INCH_TO_CM
    return round(foot_length_cm, 2)


def us_child_to_foot_length(us_size: float) -> float:
    """
    美国儿童鞋码转脚长.
    
    Args:
        us_size: US 儿童鞋码
    
    Returns:
        脚长 (厘米)
    
    Examples:
        >>> us_child_to_foot_length(9.5)
        18.0
    """
    foot_length_inch = (us_size + 12) / 3
    foot_length_cm = foot_length_inch * INCH_TO_CM
    return round(foot_length_cm, 2)


def uk_to_foot_length(uk_size: float) -> float:
    """
    英国鞋码转脚长.
    
    Args:
        uk_size: UK 鞋码
    
    Returns:
        脚长 (厘米)
    
    Examples:
        >>> uk_to_foot_length(7.5)
        26.0
    """
    foot_length_inch = (uk_size + 25) / 3
    foot_length_cm = foot_length_inch * INCH_TO_CM
    return round(foot_length_cm, 2)


def uk_child_to_foot_length(uk_size: float) -> float:
    """
    英国儿童鞋码转脚长.
    
    Args:
        uk_size: UK 儿童鞋码
    
    Returns:
        脚长 (厘米)
    
    Examples:
        >>> uk_child_to_foot_length(8.5)
        18.0
    """
    foot_length_inch = (uk_size + 13) / 3
    foot_length_cm = foot_length_inch * INCH_TO_CM
    return round(foot_length_cm, 2)


def jp_to_foot_length(jp_size: float) -> float:
    """
    日本鞋码转脚长.
    
    Args:
        jp_size: JP 鞋码
    
    Returns:
        脚长 (厘米)
    
    Examples:
        >>> jp_to_foot_length(24.5)
        24.5
    """
    return jp_size


def kr_to_foot_length(kr_size: int) -> float:
    """
    韩国鞋码转脚长.
    
    Args:
        kr_size: KR 鞋码 (毫米)
    
    Returns:
        脚长 (厘米)
    
    Examples:
        >>> kr_to_foot_length(245)
        24.5
    """
    return kr_size * MM_TO_CM


def br_to_foot_length(br_size: float) -> float:
    """
    巴西鞋码转脚长.
    
    Args:
        br_size: BR 鞋码
    
    Returns:
        諄长 (厘米)
    
    Examples:
        >>> br_to_foot_length(7)
        24.5
    """
    foot_length_cm = (br_size + 30) / 1.5
    return round(foot_length_cm, 2)


def mx_to_foot_length(mx_size: float) -> float:
    """
    墨西哥鞋码转脚长.
    
    Args:
        mx_size: MX 鞋码
    
    Returns:
        諄长 (厘米)
    
    Examples:
        >>> mx_to_foot_length(26.5)
        26.0
    """
    us_size = mx_size - 17
    return us_men_to_foot_length(us_size)


def tw_to_foot_length(tw_size: float) -> float:
    """
    台湾鞋码转脚长.
    
    Args:
        tw_size: TW 鞋码
    
    Returns:
        諄长 (厘米)
    
    Examples:
        >>> tw_to_foot_length(40)
        24.5
    """
    eu_size = tw_size - 1
    return eu_to_foot_length(eu_size)


# ============================================================================
# Main Conversion Function
# ============================================================================

def convert_size(
    size: float,
    from_system: SizeSystem,
    to_system: SizeSystem,
    gender: Gender = Gender.MALE,
    age_group: AgeGroup = AgeGroup.ADULT,
    brand: Optional[str] = None
) -> float:
    """
    转换鞋码.
    
    Args:
        size: 原始鞋码
        from_system: 原始鞋码系统
        to_system: 目标鞋码系统
        gender: 性别
        age_group: 年龄组
        brand: 品牌名称 (用于品牌调整)
    
    Returns:
        转换后的鞋码
    
    Raises:
        ValueError: 如果无效的系统或参数
    
    Examples:
        >>> convert_size(39, SizeSystem.EU, SizeSystem.US, Gender.MALE)
        6.5
        >>> convert_size(8, SizeSystem.US, SizeSystem.EU, Gender.FEMALE)
        39.0
    """
    # 先转换为脚长
    foot_length_cm = size_to_foot_length(size, from_system, gender, age_group)
    
    # 应用品牌调整
    if brand and brand in BRAND_ADJUSTMENTS:
        adjustments = BRAND_ADJUSTMENTS[brand]
        adj_key = f"US_{gender.value}" if from_system == SizeSystem.US else from_system.value
        if adj_key in adjustments:
            # 品牌调整会影响原始尺码的实际脚长
            adj_size = size - adjustments[adj_key]
            foot_length_cm = size_to_foot_length(adj_size, from_system, gender, age_group)
    
    # 从脚长转换为目标尺码
    return foot_length_to_size(foot_length_cm, to_system, gender, age_group)


def size_to_foot_length(
    size: float,
    system: SizeSystem,
    gender: Gender = Gender.MALE,
    age_group: AgeGroup = AgeGroup.ADULT
) -> float:
    """
    鞋码转脚长.
    
    Args:
        size: 鞋码
        system: 鞋码系统
        gender: 性别
        age_group: 年龄组
    
    Returns:
        諄长 (厘米)
    
    Examples:
        >>> size_to_foot_length(39, SizeSystem.EU)
        24.67
    """
    if system == SizeSystem.CN:
        return cn_to_foot_length(size)
    elif system == SizeSystem.EU:
        return eu_to_foot_length(size)
    elif system == SizeSystem.US:
        if age_group == AgeGroup.CHILD:
            return us_child_to_foot_length(size)
        elif gender == Gender.FEMALE:
            return us_women_to_foot_length(size)
        else:
            return us_men_to_foot_length(size)
    elif system == SizeSystem.UK:
        if age_group == AgeGroup.CHILD:
            return uk_child_to_foot_length(size)
        else:
            return uk_to_foot_length(size)
    elif system == SizeSystem.JP:
        return jp_to_foot_length(size)
    elif system == SizeSystem.KR:
        return kr_to_foot_length(int(size))
    elif system == SizeSystem.BR:
        return br_to_foot_length(size)
    elif system == SizeSystem.MX:
        return mx_to_foot_length(size)
    elif system == SizeSystem.TW:
        return tw_to_foot_length(size)
    elif system == SizeSystem.AU:
        # AU 与 UK 相同
        if age_group == AgeGroup.CHILD:
            return uk_child_to_foot_length(size)
        else:
            return uk_to_foot_length(size)
    else:
        raise ValueError(f"Unknown size system: {system}")


def foot_length_to_size(
    foot_length_cm: float,
    system: SizeSystem,
    gender: Gender = Gender.MALE,
    age_group: AgeGroup = AgeGroup.ADULT
) -> float:
    """
    諄长转鞋码.
    
    Args:
        foot_length_cm: 諄长 (厘米)
        system: 鞋码系统
        gender: 性别
        age_group: 年龄组
    
    Returns:
        鞋码
    
    Examples:
        >>> foot_length_to_size(24.5, SizeSystem.EU)
        39.0
    """
    if system == SizeSystem.CN:
        return foot_length_to_cn(foot_length_cm)
    elif system == SizeSystem.EU:
        return foot_length_to_eu(foot_length_cm)
    elif system == SizeSystem.US:
        if age_group == AgeGroup.CHILD:
            return foot_length_to_us_child(foot_length_cm)
        elif gender == Gender.FEMALE:
            return foot_length_to_us_women(foot_length_cm)
        else:
            return foot_length_to_us_men(foot_length_cm)
    elif system == SizeSystem.UK:
        if age_group == AgeGroup.CHILD:
            return foot_length_to_uk_child(foot_length_cm)
        else:
            return foot_length_to_uk(foot_length_cm)
    elif system == SizeSystem.JP:
        return foot_length_to_jp(foot_length_cm)
    elif system == SizeSystem.KR:
        return foot_length_to_kr(foot_length_cm)
    elif system == SizeSystem.BR:
        return foot_length_to_br(foot_length_cm)
    elif system == SizeSystem.MX:
        return foot_length_to_mx(foot_length_cm)
    elif system == SizeSystem.TW:
        return foot_length_to_tw(foot_length_cm)
    elif system == SizeSystem.AU:
        # AU 与 UK 相同
        if age_group == AgeGroup.CHILD:
            return foot_length_to_uk_child(foot_length_cm)
        else:
            return foot_length_to_uk(foot_length_cm)
    else:
        raise ValueError(f"Unknown size system: {system}")


# ============================================================================
# Full Conversion Result
# ============================================================================

def get_all_conversions(
    size: float,
    from_system: SizeSystem,
    gender: Gender = Gender.MALE,
    age_group: AgeGroup = AgeGroup.ADULT,
    brand: Optional[str] = None
) -> SizeConversionResult:
    """
    获取所有鞋码转换结果.
    
    Args:
        size: 原始鞋码
        from_system: 原始鞋码系统
        gender: 性别
        age_group: 年龄组
        brand: 品牌名称
    
    Returns:
        SizeConversionResult 对象，包含所有转换结果
    
    Examples:
        >>> result = get_all_conversions(39, SizeSystem.EU, Gender.MALE)
        >>> result.conversions['US']
        6.5
    """
    # 计算脚长
    foot_length_cm = size_to_foot_length(size, from_system, gender, age_group)
    
    # 应用品牌调整
    if brand and brand in BRAND_ADJUSTMENTS:
        adjustments = BRAND_ADJUSTMENTS[brand]
        adj_key = f"US_{gender.value}" if from_system == SizeSystem.US else from_system.value
        if adj_key in adjustments:
            adj_size = size - adjustments[adj_key]
            foot_length_cm = size_to_foot_length(adj_size, from_system, gender, age_group)
    
    # 计算所有转换
    conversions = {}
    
    # CN
    conversions['CN'] = foot_length_to_cn(foot_length_cm)
    
    # EU
    conversions['EU'] = foot_length_to_eu(foot_length_cm)
    
    # US (men and women)
    if age_group == AgeGroup.CHILD:
        conversions['US'] = foot_length_to_us_child(foot_length_cm)
        conversions['US_men'] = conversions['US']
        conversions['US_women'] = conversions['US']
    else:
        conversions['US_men'] = foot_length_to_us_men(foot_length_cm)
        conversions['US_women'] = foot_length_to_us_women(foot_length_cm)
        conversions['US'] = conversions['US_men'] if gender == Gender.MALE else conversions['US_women']
    
    # UK
    if age_group == AgeGroup.CHILD:
        conversions['UK'] = foot_length_to_uk_child(foot_length_cm)
    else:
        conversions['UK'] = foot_length_to_uk(foot_length_cm)
    
    # JP
    conversions['JP'] = foot_length_to_jp(foot_length_cm)
    
    # AU (same as UK)
    conversions['AU'] = conversions['UK']
    
    # KR
    conversions['KR'] = foot_length_to_kr(foot_length_cm)
    
    # BR
    conversions['BR'] = foot_length_to_br(foot_length_cm)
    
    # MX
    conversions['MX'] = foot_length_to_mx(foot_length_cm)
    
    # TW
    conversions['TW'] = foot_length_to_tw(foot_length_cm)
    
    # 计算脚长英寸
    foot_length_inch = round(foot_length_cm * CM_TO_INCH, 2)
    
    # 获取尺码分类
    category = get_size_category(foot_length_cm, gender, age_group)
    category_cn = SIZE_CATEGORY_LABELS[category]['cn']
    category_en = SIZE_CATEGORY_LABELS[category]['en']
    
    # 检查是否在合理范围
    in_range = is_size_in_range(foot_length_cm, age_group)
    
    # 生成推荐
    recommendations = generate_recommendations(foot_length_cm, gender, age_group, brand)
    
    return SizeConversionResult(
        original_system=from_system.value,
        original_size=size,
        original_gender=gender.value,
        original_age_group=age_group.value,
        conversions=conversions,
        foot_length_cm=foot_length_cm,
        foot_length_inch=foot_length_inch,
        size_category=category,
        size_category_cn=category_cn,
        size_category_en=category_en,
        in_range=in_range,
        recommendations=recommendations
    )


# ============================================================================
# Size Category and Range Functions
# ============================================================================

def get_size_category(
    foot_length_cm: float,
    gender: Gender,
    age_group: AgeGroup
) -> str:
    """
    根据脚长获取尺码分类.
    
    Args:
        foot_length_cm: 諄长 (厘米)
        gender: 性别
        age_group: 年龄组
    
    Returns:
        尺码分类
    
    Examples:
        >>> get_size_category(24.5, Gender.MALE, AgeGroup.ADULT)
        'medium'
    """
    # 成人尺码分类
    if age_group == AgeGroup.ADULT:
        if gender == Gender.MALE:
            if foot_length_cm < 23.0:
                return 'extra_small'
            elif foot_length_cm < 24.0:
                return 'small'
            elif foot_length_cm < 26.0:
                return 'medium'
            elif foot_length_cm < 28.0:
                return 'large'
            else:
                return 'extra_large'
        else:  # Female
            if foot_length_cm < 21.5:
                return 'extra_small'
            elif foot_length_cm < 22.5:
                return 'small'
            elif foot_length_cm < 24.5:
                return 'medium'
            elif foot_length_cm < 26.0:
                return 'large'
            else:
                return 'extra_large'
    else:  # Child
        if foot_length_cm < 16.0:
            return 'extra_small'
        elif foot_length_cm < 18.0:
            return 'small'
        elif foot_length_cm < 20.0:
            return 'medium'
        elif foot_length_cm < 22.0:
            return 'large'
        else:
            return 'extra_large'


def is_size_in_range(
    foot_length_cm: float,
    age_group: AgeGroup
) -> bool:
    """
    检查脚长是否在合理范围.
    
    Args:
        foot_length_cm: 諄长 (厘米)
        age_group: 年龄组
    
    Returns:
        是否在合理范围
    
    Examples:
        >>> is_size_in_range(24.5, AgeGroup.ADULT)
        True
        >>> is_size_in_range(35.0, AgeGroup.ADULT)
        False
    """
    if age_group == AgeGroup.ADULT:
        return 22.0 <= foot_length_cm <= 30.0
    elif age_group == AgeGroup.CHILD:
        return 14.0 <= foot_length_cm <= 22.0
    elif age_group == AgeGroup.INFANT:
        return 8.0 <= foot_length_cm <= 14.0
    else:  # Toddler
        return 14.0 <= foot_length_cm <= 18.0


def validate_size(
    size: float,
    system: SizeSystem,
    gender: Gender = Gender.MALE,
    age_group: AgeGroup = AgeGroup.ADULT
) -> Tuple[bool, str]:
    """
    验证鞋码是否有效.
    
    Args:
        size: 鞋码
        system: 鞋码系统
        gender: 性别
        age_group: 年龄组
    
    Returns:
        (是否有效, 原因说明)
    
    Examples:
        >>> validate_size(39, SizeSystem.EU, Gender.MALE)
        (True, '有效尺码')
        >>> validate_size(100, SizeSystem.EU)
        (False, '尺码超出成人有效范围')
    """
    # 获取该系统该年龄组的有效范围
    ranges = SIZE_RANGES.get(age_group.value, SIZE_RANGES['adult'])
    
    if system == SizeSystem.US:
        if age_group == AgeGroup.CHILD:
            range_key = 'US'
        elif gender == Gender.FEMALE:
            range_key = 'US_women'
        else:
            range_key = 'US_men'
    elif system == SizeSystem.UK:
        range_key = 'UK'
    elif system == SizeSystem.KR:
        range_key = 'KR'
    else:
        range_key = system.value
    
    if range_key not in ranges:
        return False, f"未知尺码系统: {system.value}"
    
    min_size, max_size = ranges[range_key]
    
    if min_size <= size <= max_size:
        return True, "有效尺码"
    elif size < min_size:
        return False, f"尺码低于{age_group.value}有效范围 ({min_size}-{max_size})"
    else:
        return False, f"尺码超出{age_group.value}有效范围 ({min_size}-{max_size})"


# ============================================================================
# Recommendation Functions
# ============================================================================

def generate_recommendations(
    foot_length_cm: float,
    gender: Gender,
    age_group: AgeGroup,
    brand: Optional[str] = None
) -> List[str]:
    """
    生成购买推荐.
    
    Args:
        foot_length_cm: 諄长 (厘米)
        gender: 性别
        age_group: 年龄组
        brand: 品牌
    
    Returns:
        推荐列表
    
    Examples:
        >>> generate_recommendations(26.0, Gender.MALE, AgeGroup.ADULT)
        ['建议选择稍大尺码以增加舒适度', ...]
    """
    recommendations = []
    
    # 基本推荐
    comfort_margin = 0.5  # cm
    recommended_length = foot_length_cm + comfort_margin
    
    recommendations.append(f"建议鞋内长度比脚长多 {comfort_margin}cm 以保证舒适")
    
    # 尺码分类推荐
    category = get_size_category(foot_length_cm, gender, age_group)
    if category == 'extra_small':
        recommendations.append("小尺码款式可能选择较少，建议关注小码专区")
    elif category == 'extra_large':
        recommendations.append("大尺码款式可能选择较少，建议关注大码专区")
    
    # 儿童推荐
    if age_group == AgeGroup.CHILD:
        recommendations.append("儿童脚部发育快，建议预留更大空间")
        recommendations.append("建议每3-6个月测量脚长并更换鞋码")
    
    # 品牌推荐
    if brand and brand in BRAND_ADJUSTMENTS:
        adj = BRAND_ADJUSTMENTS[brand]
        if gender == Gender.MALE:
            brand_adj = adj.get('US_men', 0)
        else:
            brand_adj = adj.get('US_women', 0)
        
        if brand_adj > 0:
            recommendations.append(f"{brand}品牌尺码偏小，建议选择大 {abs(brand_adj)} 号")
        elif brand_adj < 0:
            recommendations.append(f"{brand}品牌尺码偏大，建议选择小 {abs(brand_adj)} 号")
    
    return recommendations


def recommend_size(
    foot_length_cm: float,
    target_system: SizeSystem,
    gender: Gender = Gender.MALE,
    age_group: AgeGroup = AgeGroup.ADULT,
    comfort_margin_cm: float = 0.5,
    brand: Optional[str] = None
) -> SizeRecommendation:
    """
    根据脚长推荐鞋码.
    
    Args:
        foot_length_cm: 諄长 (厘米)
        target_system: 目标鞋码系统
        gender: 性别
        age_group: 年龄组
        comfort_margin_cm: 舒适余量 (厘米)
        brand: 品牌
    
    Returns:
        SizeRecommendation 对象
    
    Examples:
        >>> rec = recommend_size(25.5, SizeSystem.US, Gender.MALE)
        >>> rec.recommended_size
        8.5
    """
    # 计算推荐脚长 (加舒适余量)
    recommended_length = foot_length_cm + comfort_margin_cm
    
    # 转换为目标尺码
    recommended_size = foot_length_to_size(recommended_length, target_system, gender, age_group)
    
    # 应用品牌调整
    if brand and brand in BRAND_ADJUSTMENTS:
        adj = BRAND_ADJUSTMENTS[brand]
        if target_system == SizeSystem.US:
            if gender == Gender.MALE:
                recommended_size += adj.get('US_men', 0)
            else:
                recommended_size += adj.get('US_women', 0)
    
    # 计算尺码范围 (上下半码)
    size_range = (
        round(recommended_size - 0.5, 1),
        round(recommended_size + 0.5, 1)
    )
    
    # 生成提示
    notes = []
    if brand:
        notes.append(f"品牌 {brand} 的尺码调整已考虑")
    notes.append(f"舒适余量: {comfort_margin_cm}cm")
    
    return SizeRecommendation(
        recommended_size=round(recommended_size, 1),
        recommended_system=target_system.value,
        foot_length_cm=foot_length_cm,
        comfort_margin_cm=comfort_margin_cm,
        size_range=size_range,
        notes=notes
    )


# ============================================================================
# Size Chart Functions
# ============================================================================

def generate_size_chart(
    age_group: AgeGroup = AgeGroup.ADULT,
    gender: Gender = Gender.MALE,
    start_cm: Optional[float] = None,
    end_cm: Optional[float] = None,
    step_cm: float = 0.5
) -> List[Dict[str, Union[float, str]]]:
    """
    生成鞋码对照表.
    
    Args:
        age_group: 年龄组
        gender: 性别
        start_cm: 起始脚长 (厘米)
        end_cm: 结束脚长 (厘米)
        step_cm: 步长 (厘米)
    
    Returns:
        鞋码对照表列表
    
    Examples:
        >>> chart = generate_size_chart()
        >>> len(chart)
        17
    """
    # 设置默认范围
    if start_cm is None:
        start_cm = SIZE_RANGES[age_group.value]['CN'][0]
    if end_cm is None:
        end_cm = SIZE_RANGES[age_group.value]['CN'][1]
    
    chart = []
    current_cm = start_cm
    
    while current_cm <= end_cm:
        row = {
            'foot_length_cm': round(current_cm, 1),
            'CN': foot_length_to_cn(current_cm),
            'EU': foot_length_to_eu(current_cm),
            'JP': foot_length_to_jp(current_cm),
            'KR': foot_length_to_kr(current_cm),
        }
        
        if age_group == AgeGroup.CHILD:
            row['US'] = foot_length_to_us_child(current_cm)
            row['UK'] = foot_length_to_uk_child(current_cm)
        else:
            row['US_men'] = foot_length_to_us_men(current_cm)
            row['US_women'] = foot_length_to_us_women(current_cm)
            row['UK'] = foot_length_to_uk(current_cm)
        
        row['AU'] = row['UK']
        row['BR'] = foot_length_to_br(current_cm)
        row['MX'] = foot_length_to_mx(current_cm)
        row['TW'] = foot_length_to_tw(current_cm)
        
        # 添加分类
        row['category'] = get_size_category(current_cm, gender, age_group)
        
        chart.append(row)
        current_cm += step_cm
    
    return chart


def get_size_by_category(
    category: SizeCategory,
    gender: Gender = Gender.MALE,
    age_group: AgeGroup = AgeGroup.ADULT,
    system: SizeSystem = SizeSystem.US
) -> Tuple[float, float]:
    """
    获取某分类的尺码范围.
    
    Args:
        category: 尺码分类
        gender: 性别
        age_group: 年龄组
        system: 鞋码系统
    
    Returns:
        (最小尺码, 最大尺码)
    
    Examples:
        >>> get_size_by_category(SizeCategory.MEDIUM, Gender.MALE)
        (7.5, 10.5)
    """
    # 获取脚长范围
    if age_group == AgeGroup.ADULT:
        if gender == Gender.MALE:
            foot_ranges = {
                SizeCategory.EXTRA_SMALL: (22.0, 23.5),
                SizeCategory.SMALL: (23.5, 24.5),
                SizeCategory.MEDIUM: (24.5, 26.5),
                SizeCategory.LARGE: (26.5, 28.0),
                SizeCategory.EXTRA_LARGE: (28.0, 30.0),
            }
        else:
            foot_ranges = {
                SizeCategory.EXTRA_SMALL: (20.5, 22.0),
                SizeCategory.SMALL: (22.0, 23.0),
                SizeCategory.MEDIUM: (23.0, 25.0),
                SizeCategory.LARGE: (25.0, 26.5),
                SizeCategory.EXTRA_LARGE: (26.5, 29.0),
            }
    else:
        foot_ranges = {
            SizeCategory.EXTRA_SMALL: (14.0, 16.0),
            SizeCategory.SMALL: (16.0, 18.0),
            SizeCategory.MEDIUM: (18.0, 20.0),
            SizeCategory.LARGE: (20.0, 22.0),
            SizeCategory.EXTRA_LARGE: (22.0, 24.0),
        }
    
    min_foot, max_foot = foot_ranges.get(category, (24.5, 26.5))
    
    min_size = foot_length_to_size(min_foot, system, gender, age_group)
    max_size = foot_length_to_size(max_foot, system, gender, age_group)
    
    return round(min_size, 1), round(max_size, 1)


# ============================================================================
# Utility Functions
# ============================================================================

def format_size_string(
    size: float,
    system: SizeSystem,
    gender: Optional[Gender] = None
) -> str:
    """
    格式化鞋码字符串.
    
    Args:
        size: 鞋码
        system: 鞋码系统
        gender: 性别 (仅用于 US 系统)
    
    Returns:
        格式化后的鞋码字符串
    
    Examples:
        >>> format_size_string(8.5, SizeSystem.US, Gender.MALE)
        'US 8.5 (Men)'
        >>> format_size_string(39, SizeSystem.EU)
        'EU 39'
    """
    if system == SizeSystem.US and gender:
        return f"US {size} ({gender.value.capitalize()})"
    elif system == SizeSystem.KR:
        return f"KR {int(size)}mm"
    elif system == SizeSystem.CN or system == SizeSystem.JP:
        return f"{system.value} {size}cm"
    else:
        return f"{system.value} {size}"


def compare_sizes(
    size1: float,
    system1: SizeSystem,
    size2: float,
    system2: SizeSystem,
    gender: Gender = Gender.MALE,
    age_group: AgeGroup = AgeGroup.ADULT
) -> str:
    """
    比较两个鞋码.
    
    Args:
        size1: 第一个鞋码
        system1: 第一个鞋码系统
        size2: 第二个鞋码
        system2: 第二个鞋码系统
        gender: 性别
        age_group: 年龄组
    
    Returns:
        比较结果描述
    
    Examples:
        >>> compare_sizes(39, SizeSystem.EU, 8, SizeSystem.US, Gender.MALE)
        'EU 39 ≈ US 8.5 (Men)'
    """
    foot1 = size_to_foot_length(size1, system1, gender, age_group)
    foot2 = size_to_foot_length(size2, system2, gender, age_group)
    
    diff = abs(foot1 - foot2)
    
    if diff < 0.2:
        return f"{format_size_string(size1, system1, gender)} ≈ {format_size_string(size2, system2, gender)}"
    elif foot1 > foot2:
        return f"{format_size_string(size1, system1, gender)} > {format_size_string(size2, system2, gender)} (+{round(diff, 1)}cm)"
    else:
        return f"{format_size_string(size1, system1, gender)} < {format_size_string(size2, system2, gender)} (-{round(diff, 1)}cm)"


def get_common_sizes(
    gender: Gender = Gender.MALE,
    age_group: AgeGroup = AgeGroup.ADULT
) -> List[float]:
    """
    获取常见鞋码列表.
    
    Args:
        gender: 性别
        age_group: 年龄组
    
    Returns:
        常见鞋码列表 (EU尺码)
    
    Examples:
        >>> get_common_sizes(Gender.MALE)
        [39, 40, 41, 42, 43, 44]
    """
    if age_group == AgeGroup.ADULT:
        if gender == Gender.MALE:
            return [39, 40, 41, 42, 43, 44]
        else:
            return [36, 37, 38, 39, 40]
    else:
        return [24, 26, 28, 30, 32]


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Shoe Size Conversion Demo")
    print("=" * 60)
    
    # 单个转换
    print("\n--- 单个转换示例 ---")
    us_size = convert_size(39, SizeSystem.EU, SizeSystem.US, Gender.MALE)
    print(f"EU 39 → US (Men): {us_size}")
    
    uk_size = convert_size(39, SizeSystem.EU, SizeSystem.UK)
    print(f"EU 39 → UK: {uk_size}")
    
    cn_size = convert_size(8.5, SizeSystem.US, SizeSystem.CN, Gender.MALE)
    print(f"US 8.5 (Men) → CN: {cn_size}cm")
    
    # 完整转换
    print("\n--- 完整转换示例 ---")
    result = get_all_conversions(42, SizeSystem.EU, Gender.MALE)
    print(f"EU 42 (男性成人):")
    print(f"  CN: {result.conversions['CN']}cm")
    print(f"  EU: {result.conversions['EU']}")
    print(f"  US Men: {result.conversions['US_men']}")
    print(f"  US Women: {result.conversions['US_women']}")
    print(f"  UK: {result.conversions['UK']}")
    print(f"  JP: {result.conversions['JP']}cm")
    print(f"  KR: {result.conversions['KR']}mm")
    print(f"  分类: {result.size_category_cn} ({result.size_category_en})")
    print(f"  推荐:")
    for rec in result.recommendations:
        print(f"    - {rec}")
    
    # 儿童尺码
    print("\n--- 儿童尺码示例 ---")
    child_result = get_all_conversions(30, SizeSystem.EU, Gender.MALE, AgeGroup.CHILD)
    print(f"EU 30 (儿童):")
    print(f"  CN: {child_result.conversions['CN']}cm")
    print(f"  US: {child_result.conversions['US']}")
    print(f"  UK: {child_result.conversions['UK']}")
    
    # 尺码推荐
    print("\n--- 尺码推荐示例 ---")
    rec = recommend_size(26.0, SizeSystem.US, Gender.MALE, brand='Nike')
    print(f"脚长 26cm → US 推荐:")
    print(f"  推荐尺码: {rec.recommended_size}")
    print(f"  尺码范围: {rec.size_range[0]}-{rec.size_range[1]}")
    print(f"  提示:")
    for note in rec.notes:
        print(f"    - {note}")
    
    # 尺码对照表
    print("\n--- 尺码对照表 (部分) ---")
    chart = generate_size_chart()[:5]
    print("脚长(cm) | CN | EU | US(Men) | US(Women) | UK | JP | KR(mm)")
    print("-" * 65)
    for row in chart:
        print(f"{row['foot_length_cm']} | {row['CN']} | {row['EU']} | {row['US_men']} | {row['US_women']} | {row['UK']} | {row['JP']} | {row['KR']}")
    
    # 验证尺码
    print("\n--- 验证尺码示例 ---")
    valid, reason = validate_size(39, SizeSystem.EU)
    print(f"EU 39: {reason}")
    
    valid, reason = validate_size(100, SizeSystem.EU)
    print(f"EU 100: {reason}")
    
    print("\n" + "=" * 60)