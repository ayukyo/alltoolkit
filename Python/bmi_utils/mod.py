#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Body Mass Index (BMI) Utilities Module
=====================================================
A comprehensive BMI and health metrics utility module for Python with zero external dependencies.

Features:
    - BMI calculation (metric and imperial units)
    - BMI category classification (WHO standards)
    - Ideal weight range calculation
    - BMI Prime calculation
    - Body fat percentage estimation (BMI-based formulas)
    - Weight loss/gain recommendations
    - Children BMI percentile calculation (CDC data)
    - Health risk assessment based on BMI
    - Waist-to-height ratio calculation
    - BMR (Basal Metabolic Rate) estimation

Author: AllToolkit Contributors
License: MIT
Date: 2026-05-07
"""

from typing import Union, Tuple, Optional, List
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Constants
# ============================================================================

# WHO BMI Categories (adults)
BMI_CATEGORIES = {
    'severe_underweight': (0, 16.0),
    'underweight': (16.0, 18.5),
    'normal': (18.5, 25.0),
    'overweight': (25.0, 30.0),
    'obese_class_I': (30.0, 35.0),
    'obese_class_II': (35.0, 40.0),
    'obese_class_III': (40.0, float('inf')),
}

# BMI category labels with health risk levels
BMI_CATEGORY_INFO = {
    'severe_underweight': {
        'label': '严重偏瘦',
        'label_en': 'Severe Underweight',
        'risk': 'high',
        'risk_desc': '营养不良风险、骨质疏松、免疫力低下',
    },
    'underweight': {
        'label': '偏瘦',
        'label_en': 'Underweight',
        'risk': 'moderate',
        'risk_desc': '可能的营养不足、免疫力下降',
    },
    'normal': {
        'label': '正常',
        'label_en': 'Normal',
        'risk': 'low',
        'risk_desc': '健康的体重范围',
    },
    'overweight': {
        'label': '超重',
        'label_en': 'Overweight',
        'risk': 'moderate',
        'risk_desc': '心血管疾病风险增加',
    },
    'obese_class_I': {
        'label': '肥胖 I 级',
        'label_en': 'Obese Class I',
        'risk': 'high',
        'risk_desc': '高血压、糖尿病风险增加',
    },
    'obese_class_II': {
        'label': '肥胖 II 级',
        'label_en': 'Obese Class II',
        'risk': 'very_high',
        'risk_desc': '严重健康风险',
    },
    'obese_class_III': {
        'label': '肥胖 III 级',
        'label_en': 'Obese Class III',
        'risk': 'extremely_high',
        'risk_desc': '极高健康风险，建议就医',
    },
}

# CDC BMI-for-age percentiles data (simplified reference values for boys)
# Age 2-20, median BMI values at 50th percentile
CDC_BOYS_MEDIAN_BMI = {
    2: 16.3, 3: 15.7, 4: 15.3, 5: 15.0, 6: 14.8, 7: 14.9, 8: 15.2,
    9: 15.5, 10: 16.0, 11: 16.5, 12: 17.1, 13: 17.8, 14: 18.5,
    15: 19.2, 16: 19.9, 17: 20.5, 18: 21.0, 19: 21.4, 20: 21.7,
}

# CDC BMI-for-age percentiles data (simplified reference values for girls)
CDC_GIRLS_MEDIAN_BMI = {
    2: 16.2, 3: 15.6, 4: 15.2, 5: 15.0, 6: 14.9, 7: 15.1, 8: 15.5,
    9: 15.9, 10: 16.4, 11: 17.0, 12: 17.6, 13: 18.2, 14: 18.9,
    15: 19.5, 16: 20.1, 17: 20.6, 18: 21.0, 19: 21.3, 20: 21.5,
}

# Standard deviation approximations for BMI percentiles
CDC_BMI_SD = {
    2: 1.5, 3: 1.4, 4: 1.3, 5: 1.2, 6: 1.2, 7: 1.3, 8: 1.4,
    9: 1.5, 10: 1.7, 11: 1.9, 12: 2.1, 13: 2.3, 14: 2.5,
    15: 2.7, 16: 2.8, 17: 2.9, 18: 3.0, 19: 3.1, 20: 3.1,
}

# Pound to kilogram conversion factor
LB_TO_KG = 0.45359237

# Inch to meter conversion factor
INCH_TO_M = 0.0254

# Foot to meter conversion factor
FOOT_TO_M = 0.3048


# ============================================================================
# Enums
# ============================================================================

class Gender(Enum):
    """性别枚举"""
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'


class UnitSystem(Enum):
    """单位系统枚举"""
    METRIC = 'metric'      # kg, m
    IMPERIAL = 'imperial'  # lb, ft/in


class RiskLevel(Enum):
    """健康风险等级枚举"""
    LOW = 'low'
    MODERATE = 'moderate'
    HIGH = 'high'
    VERY_HIGH = 'very_high'
    EXTREMELY_HIGH = 'extremely_high'


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class BMIResult:
    """BMI 计算结果"""
    bmi: float
    category: str
    category_label: str
    category_label_en: str
    risk_level: str
    risk_description: str
    bmi_prime: float
    ideal_weight_min: float
    ideal_weight_max: float
    weight_difference: float  # 当前体重与理想体重范围的差距
    weight_status: str  # 'under', 'normal', 'over'


@dataclass
class ChildBMIResult:
    """儿童 BMI 计算结果"""
    bmi: float
    percentile: float
    percentile_category: str
    percentile_category_label: str
    category_label_en: str
    risk_level: str
    risk_description: str
    ideal_weight_range: Tuple[float, float]


@dataclass
class BodyFatEstimate:
    """体脂率估算结果"""
    body_fat_percent: float
    method: str
    category: str
    category_label: str
    healthy_range: Tuple[float, float]


@dataclass
class BMRResult:
    """基础代谢率计算结果"""
    bmr: float  # kcal/day
    tdee: float  # Total Daily Energy Expenditure
    method: str
    activity_level: str


# ============================================================================
# Core BMI Functions
# ============================================================================

def calculate_bmi(
    weight: float,
    height: float,
    unit_system: UnitSystem = UnitSystem.METRIC,
    height_inches: Optional[int] = None
) -> float:
    """
    计算 BMI (Body Mass Index).
    
    Args:
        weight: 体重 (metric: kg, imperial: lb)
        height: 身高 (metric: m, imperial: ft)
        unit_system: 单位系统 (metric 或 imperial)
        height_inches: imperial 单位下的额外英寸 (如身高 5'10" = height=5, height_inches=10)
    
    Returns:
        BMI 值
    
    Raises:
        ValueError: 如果输入值无效
    
    Examples:
        >>> calculate_bmi(70, 1.75)  # 70kg, 1.75m
        22.857...
        >>> calculate_bmi(154, 5, UnitSystem.IMPERIAL, 10)  # 154lb, 5'10"
        22.0...
    """
    # 验证输入
    if weight <= 0:
        raise ValueError("体重必须为正数")
    if height <= 0:
        raise ValueError("身高必须为正数")
    
    # 转换为 metric 单位
    if unit_system == UnitSystem.IMPERIAL:
        weight_kg = weight * LB_TO_KG
        height_m = height * FOOT_TO_M
        if height_inches is not None:
            height_m += height_inches * INCH_TO_M
    else:
        weight_kg = weight
        height_m = height
    
    # 计算 BMI
    if height_m <= 0:
        raise ValueError("身高必须为正数")
    
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def get_bmi_category(bmi: float) -> str:
    """
    根据 BMI 值获取分类.
    
    Args:
        bmi: BMI 值
    
    Returns:
        BMI 分类键名
    
    Examples:
        >>> get_bmi_category(22.5)
        'normal'
        >>> get_bmi_category(32.0)
        'obese_class_I'
    """
    if bmi < 16.0:
        return 'severe_underweight'
    elif bmi < 18.5:
        return 'underweight'
    elif bmi < 25.0:
        return 'normal'
    elif bmi < 30.0:
        return 'overweight'
    elif bmi < 35.0:
        return 'obese_class_I'
    elif bmi < 40.0:
        return 'obese_class_II'
    else:
        return 'obese_class_III'


def get_bmi_category_info(bmi: float) -> Tuple[str, str, str, str]:
    """
    获取 BMI 分类的详细信息.
    
    Args:
        bmi: BMI 值
    
    Returns:
        (分类键名, 中文标签, 英文标签, 风险描述)
    
    Examples:
        >>> get_bmi_category_info(22.5)
        ('normal', '正常', 'Normal', '健康的体重范围')
    """
    category = get_bmi_category(bmi)
    info = BMI_CATEGORY_INFO[category]
    return category, info['label'], info['label_en'], info['risk_desc']


def calculate_bmi_prime(bmi: float) -> float:
    """
    计算 BMI Prime (BMI / 25).
    
    BMI Prime 是 BMI 与上限正常值 (25) 的比值。
    - < 0.74: 偏瘦
    - 0.74-1.0: 正常
    - > 1.0: 超重
    
    Args:
        bmi: BMI 值
    
    Returns:
        BMI Prime 值
    
    Examples:
        >>> calculate_bmi_prime(22.5)
        0.9
        >>> calculate_bmi_prime(30.0)
        1.2
    """
    return round(bmi / 25.0, 2)


def calculate_ideal_weight_range(
    height: float,
    unit_system: UnitSystem = UnitSystem.METRIC,
    height_inches: Optional[int] = None
) -> Tuple[float, float]:
    """
    计算理想体重范围 (BMI 18.5-25).
    
    Args:
        height: 身高
        unit_system: 单位系统
        height_inches: imperial 单位下的额外英寸
    
    Returns:
        (最小理想体重, 最大理想体重)，单位与输入一致
    
    Examples:
        >>> calculate_ideal_weight_range(1.75)  # 1.75m
        (56.65..., 77.18...)
    """
    # 转换为 metric 单位
    if unit_system == UnitSystem.IMPERIAL:
        height_m = height * FOOT_TO_M
        if height_inches is not None:
            height_m += height_inches * INCH_TO_M
    else:
        height_m = height
    
    # 计算理想体重范围 (BMI 18.5-25)
    min_weight_kg = 18.5 * (height_m ** 2)
    max_weight_kg = 25.0 * (height_m ** 2)
    
    # 转换回原始单位
    if unit_system == UnitSystem.IMPERIAL:
        min_weight = round(min_weight_kg / LB_TO_KG, 1)
        max_weight = round(max_weight_kg / LB_TO_KG, 1)
    else:
        min_weight = round(min_weight_kg, 1)
        max_weight = round(max_weight_kg, 1)
    
    return min_weight, max_weight


def calculate_weight_difference(
    weight: float,
    height: float,
    unit_system: UnitSystem = UnitSystem.METRIC,
    height_inches: Optional[int] = None
) -> Tuple[float, str]:
    """
    计算当前体重与理想体重范围的差距.
    
    Args:
        weight: 当前体重
        height: 身高
        unit_system: 单位系统
        height_inches: imperial 单位下的额外英寸
    
    Returns:
        (差距值, 状态)，差距为负表示低于理想范围，正表示高于
    
    Examples:
        >>> calculate_weight_difference(70, 1.75)
        (0.0, 'normal')  # 在理想范围内
    """
    ideal_min, ideal_max = calculate_ideal_weight_range(height, unit_system, height_inches)
    
    if weight < ideal_min:
        difference = round(ideal_min - weight, 1)
        status = 'under'
    elif weight > ideal_max:
        difference = round(weight - ideal_max, 1)
        status = 'over'
    else:
        difference = 0.0
        status = 'normal'
    
    return difference, status


def calculate_full_bmi(
    weight: float,
    height: float,
    unit_system: UnitSystem = UnitSystem.METRIC,
    height_inches: Optional[int] = None
) -> BMIResult:
    """
    完整的 BMI 计算与分析.
    
    Args:
        weight: 体重
        height: 身高
        unit_system: 单位系统
        height_inches: imperial 单位下的额外英寸
    
    Returns:
        BMIResult 对象，包含完整分析结果
    
    Examples:
        >>> result = calculate_full_bmi(70, 1.75)
        >>> result.bmi
        22.86
        >>> result.category
        'normal'
    """
    bmi = calculate_bmi(weight, height, unit_system, height_inches)
    category, label, label_en, risk_desc = get_bmi_category_info(bmi)
    bmi_prime = calculate_bmi_prime(bmi)
    ideal_min, ideal_max = calculate_ideal_weight_range(height, unit_system, height_inches)
    weight_diff, weight_status = calculate_weight_difference(weight, height, unit_system, height_inches)
    
    # 获取风险等级
    info = BMI_CATEGORY_INFO[category]
    risk_level = info['risk']
    
    return BMIResult(
        bmi=bmi,
        category=category,
        category_label=label,
        category_label_en=label_en,
        risk_level=risk_level,
        risk_description=risk_desc,
        bmi_prime=bmi_prime,
        ideal_weight_min=ideal_min,
        ideal_weight_max=ideal_max,
        weight_difference=weight_diff,
        weight_status=weight_status
    )


# ============================================================================
# Body Fat Estimation Functions
# ============================================================================

def estimate_body_fat_bmi(
    bmi: float,
    age: int,
    gender: Gender
) -> float:
    """
    使用 BMI 估算体脂率 (Deurenberg 公式).
    
    公式: Body Fat % = (1.20 × BMI) + (0.23 × Age) - (10.8 × gender) - 5.4
    其中 gender: 男=1, 女=0
    
    Args:
        bmi: BMI 值
        age: 年龄 (岁)
        gender: 性别
    
    Returns:
        估算的体脂率 (%)
    
    Examples:
        >>> estimate_body_fat_bmi(25.0, 30, Gender.MALE)
        21.7
    """
    gender_factor = 1 if gender == Gender.MALE else 0
    
    body_fat = (1.20 * bmi) + (0.23 * age) - (10.8 * gender_factor) - 5.4
    return round(max(0, body_fat), 1)


def estimate_body_fat_bmi_alternative(
    bmi: float,
    age: int,
    gender: Gender
) -> float:
    """
    使用 BMI 估算体脂率 (改良 Deurenberg 公式).
    
    公式: Body Fat % = (1.39 × BMI) + (0.16 × Age) - (10.34 × gender) - 9
    其中 gender: 男=1, 女=0
    
    Args:
        bmi: BMI 值
        age: 年龄 (岁)
        gender: 性别
    
    Returns:
        估算的体脂率 (%)
    
    Examples:
        >>> estimate_body_fat_bmi_alternative(25.0, 30, Gender.MALE)
        20.25
    """
    gender_factor = 1 if gender == Gender.MALE else 0
    
    body_fat = (1.39 * bmi) + (0.16 * age) - (10.34 * gender_factor) - 9
    return round(max(0, body_fat), 1)


def get_body_fat_category(
    body_fat: float,
    gender: Gender,
    age: int
) -> Tuple[str, str]:
    """
    获取体脂率分类.
    
    Args:
        body_fat: 体脂率 (%)
        gender: 性别
        age: 年龄
    
    Returns:
        (分类键名, 中文标签)
    
    Examples:
        >>> get_body_fat_category(15.0, Gender.MALE, 30)
        ('fitness', '健美')
    """
    # 根据年龄调整分类标准
    if age < 40:
        male_ranges = {
            'essential': (2, 5),
            'athletes': (6, 13),
            'fitness': (14, 17),
            'average': (18, 24),
            'obese': (25, float('inf')),
        }
        female_ranges = {
            'essential': (10, 13),
            'athletes': (14, 20),
            'fitness': (21, 24),
            'average': (25, 31),
            'obese': (32, float('inf')),
        }
    elif age < 60:
        male_ranges = {
            'essential': (2, 5),
            'athletes': (6, 15),
            'fitness': (16, 20),
            'average': (21, 27),
            'obese': (28, float('inf')),
        }
        female_ranges = {
            'essential': (10, 13),
            'athletes': (14, 22),
            'fitness': (23, 27),
            'average': (28, 34),
            'obese': (35, float('inf')),
        }
    else:
        male_ranges = {
            'essential': (2, 5),
            'athletes': (6, 17),
            'fitness': (18, 22),
            'average': (23, 29),
            'obese': (30, float('inf')),
        }
        female_ranges = {
            'essential': (10, 13),
            'athletes': (14, 24),
            'fitness': (25, 29),
            'average': (30, 36),
            'obese': (37, float('inf')),
        }
    
    ranges = male_ranges if gender == Gender.MALE else female_ranges
    
    labels = {
        'essential': '必需脂肪',
        'athletes': '运动员',
        'fitness': '健美',
        'average': '平均水平',
        'obese': '肥胖',
    }
    
    for category, (min_val, max_val) in ranges.items():
        if min_val <= body_fat <= max_val:
            return category, labels[category]
    
    # 如果低于必需脂肪
    if body_fat < ranges['essential'][0]:
        return 'under_essential', '低于必需脂肪'
    
    return 'obese', labels['obese']


def estimate_full_body_fat(
    bmi: float,
    age: int,
    gender: Gender,
    method: str = 'deurenberg'
) -> BodyFatEstimate:
    """
    完整的体脂率估算.
    
    Args:
        bmi: BMI 值
        age: 年龄
        gender: 性别
        method: 估算方法 ('deurenberg' 或 'alternative')
    
    Returns:
        BodyFatEstimate 对象
    
    Examples:
        >>> result = estimate_full_body_fat(25.0, 30, Gender.MALE)
        >>> result.body_fat_percent
        21.7
    """
    if method == 'alternative':
        body_fat = estimate_body_fat_bmi_alternative(bmi, age, gender)
    else:
        body_fat = estimate_body_fat_bmi(bmi, age, gender)
    
    category, label = get_body_fat_category(body_fat, gender, age)
    
    # 计算健康范围
    if gender == Gender.MALE:
        if age < 40:
            healthy_min, healthy_max = 14, 24
        elif age < 60:
            healthy_min, healthy_max = 16, 27
        else:
            healthy_min, healthy_max = 18, 29
    else:
        if age < 40:
            healthy_min, healthy_max = 21, 31
        elif age < 60:
            healthy_min, healthy_max = 23, 34
        else:
            healthy_min, healthy_max = 25, 36
    
    return BodyFatEstimate(
        body_fat_percent=body_fat,
        method=method,
        category=category,
        category_label=label,
        healthy_range=(healthy_min, healthy_max)
    )


# ============================================================================
# Children BMI Functions
# ============================================================================

def calculate_child_bmi_percentile(
    bmi: float,
    age: int,
    gender: Gender
) -> float:
    """
    计算儿童 BMI 百分位数 (基于 CDC 数据).
    
    Args:
        bmi: BMI 值
        age: 年龄 (2-20 岁)
        gender: 性别
    
    Returns:
        百分位数 (0-100)
    
    Raises:
        ValueError: 如果年龄不在有效范围
    
    Examples:
        >>> calculate_child_bmi_percentile(18.0, 10, Gender.MALE)
        87.5  # 大约
    """
    if age < 2 or age > 20:
        raise ValueError("儿童 BMI 百分位数计算仅适用于 2-20 岁")
    
    # 获取中位数 BMI
    if gender == Gender.MALE:
        median_bmi = CDC_BOYS_MEDIAN_BMI.get(age, 21.0)
    else:
        median_bmi = CDC_GIRLS_MEDIAN_BMI.get(age, 21.0)
    
    # 获取标准差
    sd = CDC_BMI_SD.get(age, 2.0)
    
    # 使用 Z-score 计算百分位数
    z_score = (bmi - median_bmi) / sd
    
    # 将 Z-score 转换为百分位数 (使用简化公式)
    # 实际应用中应使用精确的统计表
    percentile = 50 + (z_score * 16)  # 简化计算
    
    # 限制在 0-100 范围内
    return round(max(0, min(100, percentile)), 1)


def get_child_bmi_category(percentile: float) -> Tuple[str, str, str, str]:
    """
    获取儿童 BMI 分类 (基于百分位数).
    
    Args:
        percentile: 百分位数
    
    Returns:
        (分类键名, 中文标签, 英文标签, 风险描述)
    
    Examples:
        >>> get_child_bmi_category(85)
        ('overweight', '超重', 'Overweight', '体重超过健康范围')
    """
    if percentile < 5:
        return (
            'underweight',
            '偏瘦',
            'Underweight',
            '体重低于健康范围，建议咨询医生'
        )
    elif percentile < 85:
        return (
            'normal',
            '正常',
            'Healthy Weight',
            '健康的体重范围'
        )
    elif percentile < 95:
        return (
            'overweight',
            '超重',
            'Overweight',
            '体重超过健康范围，建议调整饮食和运动'
        )
    else:
        return (
            'obese',
            '肥胖',
            'Obese',
            '体重严重超标，建议咨询医生'
        )


def calculate_child_full_bmi(
    weight: float,
    height: float,
    age: int,
    gender: Gender,
    unit_system: UnitSystem = UnitSystem.METRIC,
    height_inches: Optional[int] = None
) -> ChildBMIResult:
    """
    完整的儿童 BMI 计算与分析.
    
    Args:
        weight: 体重
        height: 身高
        age: 年龄 (2-20 岁)
        gender: 性别
        unit_system: 单位系统
        height_inches: imperial 单位下的额外英寸
    
    Returns:
        ChildBMIResult 对象
    
    Examples:
        >>> result = calculate_child_full_bmi(35, 1.4, 10, Gender.MALE)
        >>> result.bmi
        17.86
    """
    bmi = calculate_bmi(weight, height, unit_system, height_inches)
    percentile = calculate_child_bmi_percentile(bmi, age, gender)
    category, label, label_en, risk_desc = get_child_bmi_category(percentile)
    
    # 确定风险等级
    if percentile < 5:
        risk_level = 'moderate'
    elif percentile < 85:
        risk_level = 'low'
    elif percentile < 95:
        risk_level = 'moderate'
    else:
        risk_level = 'high'
    
    # 计算理想体重范围 (基于 5-85 百分位)
    if gender == Gender.MALE:
        median_bmi = CDC_BOYS_MEDIAN_BMI.get(age, 21.0)
    else:
        median_bmi = CDC_GIRLS_MEDIAN_BMI.get(age, 21.0)
    
    # 转换身高为 metric
    if unit_system == UnitSystem.IMPERIAL:
        height_m = height * FOOT_TO_M
        if height_inches is not None:
            height_m += height_inches * INCH_TO_M
    else:
        height_m = height
    
    # 使用 BMI 15-21 作为儿童的简化理想范围
    ideal_min_kg = 15 * (height_m ** 2)
    ideal_max_kg = 21 * (height_m ** 2)
    
    if unit_system == UnitSystem.IMPERIAL:
        ideal_min = round(ideal_min_kg / LB_TO_KG, 1)
        ideal_max = round(ideal_max_kg / LB_TO_KG, 1)
    else:
        ideal_min = round(ideal_min_kg, 1)
        ideal_max = round(ideal_max_kg, 1)
    
    return ChildBMIResult(
        bmi=bmi,
        percentile=percentile,
        percentile_category=category,
        percentile_category_label=label,
        category_label_en=label_en,
        risk_level=risk_level,
        risk_description=risk_desc,
        ideal_weight_range=(ideal_min, ideal_max)
    )


# ============================================================================
# BMR (Basal Metabolic Rate) Functions
# ============================================================================

def calculate_bmr_mifflin(
    weight: float,
    height: float,
    age: int,
    gender: Gender,
    unit_system: UnitSystem = UnitSystem.METRIC,
    height_inches: Optional[int] = None
) -> float:
    """
    使用 Mifflin-St Jeor 公式计算基础代谢率.
    
    公式:
        男: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) + 5
        女: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) - 161
    
    Args:
        weight: 体重
        height: 身高
        age: 年龄
        gender: 性别
        unit_system: 单位系统
        height_inches: imperial 单位下的额外英寸
    
    Returns:
        BMR (kcal/day)
    
    Examples:
        >>> calculate_bmr_mifflin(70, 1.75, 30, Gender.MALE)
        1675.0
    """
    # 转换为 metric 单位
    if unit_system == UnitSystem.IMPERIAL:
        weight_kg = weight * LB_TO_KG
        height_cm = (height * FOOT_TO_M + (height_inches or 0) * INCH_TO_M) * 100
    else:
        weight_kg = weight
        height_cm = height * 100
    
    # 计算 BMR
    if gender == Gender.MALE:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    
    return round(bmr, 0)


def calculate_bmr_harris_benedict(
    weight: float,
    height: float,
    age: int,
    gender: Gender,
    unit_system: UnitSystem = UnitSystem.METRIC,
    height_inches: Optional[int] = None
) -> float:
    """
    使用 Harris-Benedict 公式计算基础代谢率 (原始版本).
    
    公式:
        男: BMR = 66.5 + (13.75 × weight_kg) + (5.003 × height_cm) - (6.75 × age)
        女: BMR = 655.1 + (9.563 × weight_kg) + (1.85 × height_cm) - (4.676 × age)
    
    Args:
        weight: 体重
        height: 身高
        age: 年龄
        gender: 性别
        unit_system: 单位系统
        height_inches: imperial 单位下的额外英寸
    
    Returns:
        BMR (kcal/day)
    
    Examples:
        >>> calculate_bmr_harris_benedict(70, 1.75, 30, Gender.MALE)
        1696.0
    """
    # 转换为 metric 单位
    if unit_system == UnitSystem.IMPERIAL:
        weight_kg = weight * LB_TO_KG
        height_cm = (height * FOOT_TO_M + (height_inches or 0) * INCH_TO_M) * 100
    else:
        weight_kg = weight
        height_cm = height * 100
    
    # 计算 BMR
    if gender == Gender.MALE:
        bmr = 66.5 + (13.75 * weight_kg) + (5.003 * height_cm) - (6.75 * age)
    else:
        bmr = 655.1 + (9.563 * weight_kg) + (1.85 * height_cm) - (4.676 * age)
    
    return round(bmr, 0)


def calculate_tdee(
    bmr: float,
    activity_level: str
) -> float:
    """
    计算总每日能量消耗 (TDEE).
    
    Activity levels:
        - sedentary: 久坐 (1.2)
        - light: 轻度活动 (1.375)
        - moderate: 中度活动 (1.55)
        - active: 高度活动 (1.725)
        - very_active: 非常活跃 (1.9)
    
    Args:
        bmr: 基础代谢率
        activity_level: 活动水平
    
    Returns:
        TDEE (kcal/day)
    
    Examples:
        >>> calculate_tdee(1700, 'moderate')
        2635.0
    """
    activity_factors = {
        'sedentary': 1.2,       # 久坐，几乎不运动
        'light': 1.375,         # 轻度活动，每周 1-3 天运动
        'moderate': 1.55,       # 中度活动，每周 3-5 天运动
        'active': 1.725,        # 高度活动，每周 6-7 天运动
        'very_active': 1.9,     # 非常活跃，体力劳动或每天两次训练
    }
    
    factor = activity_factors.get(activity_level, 1.2)
    return round(bmr * factor, 0)


def calculate_full_bmr(
    weight: float,
    height: float,
    age: int,
    gender: Gender,
    activity_level: str = 'sedentary',
    unit_system: UnitSystem = UnitSystem.METRIC,
    height_inches: Optional[int] = None,
    method: str = 'mifflin'
) -> BMRResult:
    """
    完整的代谢率计算.
    
    Args:
        weight: 体重
        height: 身高
        age: 年龄
        gender: 性别
        activity_level: 活动水平
        unit_system: 单位系统
        height_inches: imperial 单位下的额外英寸
        method: 计算方法 ('mifflin' 或 'harris_benedict')
    
    Returns:
        BMRResult 对象
    
    Examples:
        >>> result = calculate_full_bmr(70, 1.75, 30, Gender.MALE, 'moderate')
        >>> result.bmr
        1675
        >>> result.tdee
        2596
    """
    if method == 'harris_benedict':
        bmr = calculate_bmr_harris_benedict(weight, height, age, gender, unit_system, height_inches)
    else:
        bmr = calculate_bmr_mifflin(weight, height, age, gender, unit_system, height_inches)
    
    tdee = calculate_tdee(bmr, activity_level)
    
    activity_labels = {
        'sedentary': '久坐',
        'light': '轻度活动',
        'moderate': '中度活动',
        'active': '高度活动',
        'very_active': '非常活跃',
    }
    
    return BMRResult(
        bmr=bmr,
        tdee=tdee,
        method=method,
        activity_level=activity_labels.get(activity_level, activity_level)
    )


# ============================================================================
# Waist-to-Height Ratio Functions
# ============================================================================

def calculate_waist_height_ratio(
    waist: float,
    height: float,
    unit_system: UnitSystem = UnitSystem.METRIC
) -> float:
    """
    计算腰围身高比 (WHtR).
    
    Args:
        waist: 腰围 (metric: cm, imperial: in)
        height: 身高 (metric: cm, imperial: in)
        unit_system: 单位系统
    
    Returns:
        腰围身高比
    
    Examples:
        >>> calculate_waist_height_ratio(80, 175)
        0.46
    """
    ratio = waist / height
    return round(ratio, 2)


def get_waist_height_category(ratio: float, gender: Gender) -> Tuple[str, str, str]:
    """
    获取腰围身高比分类.
    
    Args:
        ratio: 腰围身高比
        gender: 性别
    
    Returns:
        (分类键名, 中文标签, 健康建议)
    
    Examples:
        >>> get_waist_height_category(0.5, Gender.MALE)
        ('increased_risk', '风险增加', '建议控制饮食和增加运动')
    """
    # WHtR 分类标准 (不分性别，使用 0.5 作为阈值)
    if ratio < 0.4:
        return ('underweight', '偏瘦', '可能需要增加体重')
    elif ratio < 0.5:
        return ('healthy', '健康', '继续保持')
    elif ratio < 0.6:
        return ('increased_risk', '风险增加', '建议控制饮食和增加运动')
    else:
        return ('high_risk', '高风险', '建议咨询医生并制定减重计划')


# ============================================================================
# Weight Recommendations Functions
# ============================================================================

def calculate_weight_recommendation(
    weight: float,
    height: float,
    unit_system: UnitSystem = UnitSystem.METRIC,
    height_inches: Optional[int] = None,
    target_bmi: Optional[float] = None,
    timeframe_weeks: int = 12
) -> dict:
    """
    计算减重/增重建议.
    
    Args:
        weight: 当前体重
        height: 身高
        unit_system: 单位系统
        height_inches: imperial 单位下的额外英寸
        target_bmi: 目标 BMI (默认 22)
        timeframe_weeks: 目标达成时间 (周)
    
    Returns:
        包含减重建议的字典
    
    Examples:
        >>> calculate_weight_recommendation(80, 1.75)
        {'target_weight': 67.4, 'weight_change': -12.6, 'weekly_change': -1.05, ...}
    """
    if target_bmi is None:
        target_bmi = 22.0  # 健康中值
    
    # 转换为 metric
    if unit_system == UnitSystem.IMPERIAL:
        height_m = height * FOOT_TO_M
        if height_inches is not None:
            height_m += height_inches * INCH_TO_M
    else:
        height_m = height
    
    # 计算目标体重
    target_weight_kg = target_bmi * (height_m ** 2)
    
    if unit_system == UnitSystem.IMPERIAL:
        current_weight_kg = weight * LB_TO_KG
        target_weight = round(target_weight_kg / LB_TO_KG, 1)
        weight_change = round(target_weight - weight, 1)
    else:
        target_weight = round(target_weight_kg, 1)
        weight_change = round(target_weight - weight, 1)
    
    # 计算每周变化
    weekly_change = round(weight_change / timeframe_weeks, 2)
    
    # 判断是否健康减重速度
    # 建议每周减重不超过 0.5-1 kg (1-2 lb)
    if unit_system == UnitSystem.IMPERIAL:
        healthy_rate = abs(weekly_change) <= 2.0  # lb/week
    else:
        healthy_rate = abs(weekly_change) <= 1.0  # kg/week
    
    return {
        'target_weight': target_weight,
        'weight_change': weight_change,
        'weekly_change': weekly_change,
        'timeframe_weeks': timeframe_weeks,
        'is_healthy_rate': healthy_rate,
        'recommendation': '增重' if weight_change > 0 else ('减重' if weight_change < 0 else '保持'),
    }


# ============================================================================
# Utility Functions
# ============================================================================

def convert_weight(value: float, from_system: UnitSystem, to_system: UnitSystem) -> float:
    """
    转换体重单位.
    
    Args:
        value: 体重值
        from_system: 原单位系统
        to_system: 目标单位系统
    
    Returns:
        转换后的体重值
    
    Examples:
        >>> convert_weight(70, UnitSystem.METRIC, UnitSystem.IMPERIAL)
        154.32
    """
    if from_system == to_system:
        return value
    
    if from_system == UnitSystem.METRIC and to_system == UnitSystem.IMPERIAL:
        return round(value / LB_TO_KG, 2)
    else:
        return round(value * LB_TO_KG, 2)


def convert_height(
    value: float,
    from_system: UnitSystem,
    to_system: UnitSystem,
    inches: Optional[int] = None
) -> Union[float, Tuple[float, int]]:
    """
    转换身高单位.
    
    Args:
        value: 身高值 (metric: m, imperial: ft)
        from_system: 原单位系统
        to_system: 目标单位系统
        inches: imperial 单位下的额外英寸
    
    Returns:
        转换后的身高值 (metric 返回 m, imperial 返回 (ft, inches))
    
    Examples:
        >>> convert_height(1.75, UnitSystem.METRIC, UnitSystem.IMPERIAL)
        (5, 9)
    """
    if from_system == to_system:
        return value
    
    if from_system == UnitSystem.METRIC:
        # metric (m) -> imperial (ft, in)
        total_inches = round(value / INCH_TO_M)
        feet = total_inches // 12
        inches = total_inches % 12
        return feet, inches
    else:
        # imperial (ft, in) -> metric (m)
        total_m = value * FOOT_TO_M
        if inches is not None:
            total_m += inches * INCH_TO_M
        return round(total_m, 2)


def get_bmi_summary(bmi: float) -> str:
    """
    获取 BMI 简要说明.
    
    Args:
        bmi: BMI 值
    
    Returns:
        简要说明字符串
    
    Examples:
        >>> get_bmi_summary(22.5)
        'BMI 22.5 - 正常范围，健康的体重'
    """
    category, label, label_en, risk_desc = get_bmi_category_info(bmi)
    return f"BMI {bmi:.1f} - {label}，{risk_desc}"


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - BMI Utilities Demo")
    print("=" * 60)
    
    # 成人 BMI 计算
    print("\n--- 成人 BMI 计算 ---")
    result = calculate_full_bmi(70, 1.75)
    print(f"体重: 70kg, 身高: 1.75m")
    print(f"BMI: {result.bmi}")
    print(f"分类: {result.category_label} ({result.category_label_en})")
    print(f"风险: {result.risk_level} - {result.risk_description}")
    print(f"BMI Prime: {result.bmi_prime}")
    print(f"理想体重范围: {result.ideal_weight_min}-{result.ideal_weight_max} kg")
    
    # 体脂率估算
    print("\n--- 体脂率估算 ---")
    fat_result = estimate_full_body_fat(22.86, 30, Gender.MALE)
    print(f"估算体脂率: {fat_result.body_fat_percent}%")
    print(f"分类: {fat_result.category_label}")
    print(f"健康范围: {fat_result.healthy_range[0]}-{fat_result.healthy_range[1]}%")
    
    # 基础代谢率
    print("\n--- 基础代谢率 ---")
    bmr_result = calculate_full_bmr(70, 1.75, 30, Gender.MALE, 'moderate')
    print(f"BMR: {bmr_result.bmr} kcal/day")
    print(f"TDEE: {bmr_result.tdee} kcal/day")
    print(f"活动水平: {bmr_result.activity_level}")
    
    # 儿童 BMI
    print("\n--- 儿童 BMI 计算 ---")
    child_result = calculate_child_full_bmi(35, 1.4, 10, Gender.MALE)
    print(f"体重: 35kg, 身高: 1.4m, 年龄: 10岁, 性别: 男")
    print(f"BMI: {child_result.bmi}")
    print(f"百分位数: {child_result.percentile}%")
    print(f"分类: {child_result.percentile_category_label}")
    
    # Imperial 单位
    print("\n--- Imperial 单位 ---")
    imp_result = calculate_full_bmi(154, 5, UnitSystem.IMPERIAL, 10)
    print(f"体重: 154lb, 身高: 5'10\"")
    print(f"BMI: {imp_result.bmi}")
    print(f"理想体重范围: {imp_result.ideal_weight_min}-{imp_result.ideal_weight_max} lb")
    
    # 减重建议
    print("\n--- 减重建议 ---")
    rec = calculate_weight_recommendation(80, 1.75)
    print(f"当前体重: 80kg, 身高: 1.75m")
    print(f"目标体重: {rec['target_weight']}kg")
    print(f"需要{rec['recommendation']}: {abs(rec['weight_change'])}kg")
    print(f"每周变化: {rec['weekly_change']}kg")
    print(f"是否健康速度: {rec['is_healthy_rate']}")
    
    print("\n" + "=" * 60)