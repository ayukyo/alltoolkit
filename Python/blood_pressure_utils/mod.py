#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Blood Pressure Utilities Module
=============================================
A comprehensive blood pressure analysis utility module for Python with zero external dependencies.

Features:
    - Blood pressure classification (WHO & Chinese guidelines)
    - Age-specific normal blood pressure ranges
    - Mean Arterial Pressure (MAP) calculation
    - Pulse pressure analysis
    - Blood pressure risk assessment
    - Blood pressure statistics and trends
    - Pediatric blood pressure percentile calculation

Author: AllToolkit Contributors
License: MIT
Date: 2026-05-08
"""

from typing import Union, Tuple, Optional, List, Dict
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


# ============================================================================
# Constants
# ============================================================================

# WHO Blood Pressure Categories (Adults)
# Unit: mmHg
BP_CATEGORIES_WHO = {
    'optimal': {
        'systolic': (0, 120),
        'diastolic': (0, 80),
        'label': '理想血压',
        'label_en': 'Optimal',
        'risk': 'low',
        'risk_desc': '心血管风险最低',
    },
    'normal': {
        'systolic': (120, 130),
        'diastolic': (80, 85),
        'label': '正常血压',
        'label_en': 'Normal',
        'risk': 'low',
        'risk_desc': '血压在正常范围',
    },
    'high_normal': {
        'systolic': (130, 140),
        'diastolic': (85, 90),
        'label': '正常高值',
        'label_en': 'High Normal',
        'risk': 'moderate',
        'risk_desc': '建议改善生活方式，定期监测',
    },
    'grade1_hypertension': {
        'systolic': (140, 160),
        'diastolic': (90, 100),
        'label': '高血压 1 级',
        'label_en': 'Grade 1 Hypertension',
        'risk': 'high',
        'risk_desc': '建议就医，可能需要药物治疗',
    },
    'grade2_hypertension': {
        'systolic': (160, 180),
        'diastolic': (100, 110),
        'label': '高血压 2 级',
        'label_en': 'Grade 2 Hypertension',
        'risk': 'very_high',
        'risk_desc': '需要药物治疗，定期随访',
    },
    'grade3_hypertension': {
        'systolic': (180, float('inf')),
        'diastolic': (110, float('inf')),
        'label': '高血压 3 级',
        'label_en': 'Grade 3 Hypertension',
        'risk': 'extremely_high',
        'risk_desc': '严重高血压，需立即就医',
    },
}

# Isolated Systolic Hypertension (ISH)
ISH_CATEGORY = {
    'systolic': (140, float('inf')),
    'diastolic': (0, 90),
    'label': '单纯收缩期高血压',
    'label_en': 'Isolated Systolic Hypertension',
    'risk': 'high',
    'risk_desc': '常见于老年人，需关注',
}

# Age-specific normal blood pressure ranges (approximate values)
AGE_BP_RANGES = {
    # Children (1-17 years)
    1: {'systolic': (80, 100), 'diastolic': (50, 70)},
    2: {'systolic': (80, 105), 'diastolic': (50, 70)},
    3: {'systolic': (85, 110), 'diastolic': (55, 75)},
    4: {'systolic': (88, 112), 'diastolic': (55, 78)},
    5: {'systolic': (90, 115), 'diastolic': (58, 80)},
    6: {'systolic': (92, 118), 'diastolic': (60, 82)},
    7: {'systolic': (95, 120), 'diastolic': (62, 85)},
    8: {'systolic': (98, 122), 'diastolic': (65, 88)},
    9: {'systolic': (100, 125), 'diastolic': (68, 90)},
    10: {'systolic': (102, 128), 'diastolic': (70, 92)},
    11: {'systolic': (105, 130), 'diastolic': (72, 94)},
    12: {'systolic': (108, 132), 'diastolic': (74, 96)},
    13: {'systolic': (110, 135), 'diastolic': (76, 98)},
    14: {'systolic': (112, 138), 'diastolic': (78, 100)},
    15: {'systolic': (115, 140), 'diastolic': (80, 102)},
    16: {'systolic': (118, 142), 'diastolic': (82, 104)},
    17: {'systolic': (120, 145), 'diastolic': (84, 106)},
    # Adults (18+)
    18: {'systolic': (90, 130), 'diastolic': (60, 85)},
    'adult_18_39': {'systolic': (90, 130), 'diastolic': (60, 85)},
    'adult_40_59': {'systolic': (90, 140), 'diastolic': (60, 90)},
    'adult_60_plus': {'systolic': (90, 150), 'diastolic': (60, 90)},
}

# Pulse pressure categories
PULSE_PRESSURE_CATEGORIES = {
    'normal': {
        'range': (30, 50),
        'label': '正常脉压差',
        'label_en': 'Normal Pulse Pressure',
        'desc': '脉压差在正常范围',
    },
    'increased': {
        'range': (50, 60),
        'label': '脉压差增大',
        'label_en': 'Increased Pulse Pressure',
        'desc': '可能提示动脉硬化，建议检查',
    },
    'high': {
        'range': (60, float('inf')),
        'label': '脉压差过高',
        'label_en': 'High Pulse Pressure',
        'desc': '动脉硬化风险增加，建议就医',
    },
    'low': {
        'range': (0, 30),
        'label': '脉压差偏低',
        'label_en': 'Low Pulse Pressure',
        'desc': '可能提示心输出量减少',
    },
}


# ============================================================================
# Enums
# ============================================================================

class BPUnit(Enum):
    """血压单位枚举"""
    MMHG = 'mmHg'
    KPA = 'kPa'


class RiskLevel(Enum):
    """健康风险等级枚举"""
    LOW = 'low'
    MODERATE = 'moderate'
    HIGH = 'high'
    VERY_HIGH = 'very_high'
    EXTREMELY_HIGH = 'extremely_high'


class Gender(Enum):
    """性别枚举"""
    MALE = 'male'
    FEMALE = 'female'


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class BPReading:
    """单次血压读数"""
    systolic: float  # 收缩压
    diastolic: float  # 舒张压
    pulse_pressure: float  # 脉压差
    map: float  # 平均动脉压
    timestamp: Optional[datetime] = None
    position: Optional[str] = None  # 'sitting', 'standing', 'lying'


@dataclass
class BPResult:
    """血压分析结果"""
    systolic: float
    diastolic: float
    category: str
    category_label: str
    category_label_en: str
    risk_level: str
    risk_description: str
    pulse_pressure: float
    pulse_pressure_category: str
    pulse_pressure_label: str
    map: float
    map_status: str  # 'normal', 'low', 'high'
    age_appropriate: bool
    recommendations: List[str]


@dataclass
class BPStatistics:
    """血压统计数据"""
    readings_count: int
    systolic_mean: float
    systolic_min: float
    systolic_max: float
    systolic_std: float
    diastolic_mean: float
    diastolic_min: float
    diastolic_max: float
    diastolic_std: float
    pulse_pressure_mean: float
    map_mean: float
    dominant_category: str
    trend: str  # 'stable', 'increasing', 'decreasing', 'fluctuating'


@dataclass
class ChildBPResult:
    """儿童血压分析结果"""
    systolic: float
    diastolic: float
    age: int
    percentile: float
    percentile_category: str
    percentile_label: str
    risk_level: str
    recommendations: List[str]


# ============================================================================
# Unit Conversion Functions
# ============================================================================

# Conversion factor: 1 mmHg = 0.133 kPa
MMHG_TO_KPA = 0.133
KPA_TO_MMHG = 7.506


def convert_bp_unit(value: float, from_unit: BPUnit, to_unit: BPUnit) -> float:
    """
    转换血压单位.
    
    Args:
        value: 血压值
        from_unit: 原单位
        to_unit: 目标单位
    
    Returns:
        转换后的血压值
    
    Examples:
        >>> convert_bp_unit(120, BPUnit.MMHG, BPUnit.KPA)
        15.96
    """
    if from_unit == to_unit:
        return value
    
    if from_unit == BPUnit.MMHG and to_unit == BPUnit.KPA:
        return round(value * MMHG_TO_KPA, 2)
    else:
        return round(value * KPA_TO_MMHG, 2)


def mmhg_to_kpa(mmhg: float) -> float:
    """将 mmHg 转换为 kPa"""
    return round(mmhg * MMHG_TO_KPA, 2)


def kpa_to_mmhg(kpa: float) -> float:
    """将 kPa 转换为 mmHg"""
    return round(kpa * KPA_TO_MMHG, 2)


# ============================================================================
# Core Blood Pressure Functions
# ============================================================================

def calculate_pulse_pressure(systolic: float, diastolic: float) -> float:
    """
    计算脉压差 (Pulse Pressure).
    
    脉压差 = 收缩压 - 舒张压
    
    Args:
        systolic: 收缩压 (mmHg)
        diastolic: 舒张压 (mmHg)
    
    Returns:
        脉压差 (mmHg)
    
    Examples:
        >>> calculate_pulse_pressure(120, 80)
        40
    """
    return round(systolic - diastolic, 1)


def calculate_map(systolic: float, diastolic: float) -> float:
    """
    计算平均动脉压 (Mean Arterial Pressure).
    
    MAP = (收缩压 + 2 × 舒张压) / 3
    或 MAP = 舒张压 + 1/3 × 脉压差
    
    Args:
        systolic: 收缩压 (mmHg)
        diastolic: 舒张压 (mmHg)
    
    Returns:
        MAP (mmHg)
    
    Examples:
        >>> calculate_map(120, 80)
        93.33
    """
    return round(diastolic + (systolic - diastolic) / 3, 2)


def get_map_status(map_value: float) -> str:
    """
    获取 MAP 状态评估.
    
    正常 MAP 范围: 70-105 mmHg
    
    Args:
        map_value: MAP 值 (mmHg)
    
    Returns:
        MAP 状态 ('low', 'normal', 'high', 'critical_low', 'critical_high')
    
    Examples:
        >>> get_map_status(93)
        'normal'
    """
    if map_value < 60:
        return 'critical_low'
    elif map_value < 70:
        return 'low'
    elif map_value <= 105:
        return 'normal'
    elif map_value <= 120:
        return 'high'
    else:
        return 'critical_high'


def classify_bp(systolic: float, diastolic: float) -> Tuple[str, str, str, str, str]:
    """
    根据 WHO 标准分类血压.
    
    Args:
        systolic: 收缩压 (mmHg)
        diastolic: 舒张压 (mmHg)
    
    Returns:
        (分类键名, 中文标签, 英文标签, 风险等级, 风险描述)
    
    Examples:
        >>> classify_bp(120, 80)
        ('optimal', '理想血压', 'Optimal', 'low', '心血管风险最低')
    """
    # 检查单纯收缩期高血压
    if systolic >= 140 and diastolic < 90:
        return (
            'isolated_systolic_hypertension',
            ISH_CATEGORY['label'],
            ISH_CATEGORY['label_en'],
            ISH_CATEGORY['risk'],
            ISH_CATEGORY['risk_desc']
        )
    
    # 根据收缩压和舒张压的最高级别分类
    systolic_category = None
    diastolic_category = None
    
    for cat_name, cat_info in BP_CATEGORIES_WHO.items():
        sys_range = cat_info['systolic']
        dia_range = cat_info['diastolic']
        
        if sys_range[0] <= systolic < sys_range[1]:
            systolic_category = cat_name
        if dia_range[0] <= diastolic < dia_range[1]:
            diastolic_category = cat_name
    
    # 如果舒张压超出范围，用舒张压分类
    if diastolic >= 90 and systolic_category in ['optimal', 'normal', 'high_normal']:
        # 收缩压正常但舒张压高
        for cat_name, cat_info in BP_CATEGORIES_WHO.items():
            if cat_info['diastolic'][0] <= diastolic < cat_info['diastolic'][1]:
                diastolic_category = cat_name
                break
    
    # 选择更严重的分类
    category_order = [
        'optimal', 'normal', 'high_normal',
        'grade1_hypertension', 'grade2_hypertension', 'grade3_hypertension'
    ]
    
    systolic_idx = category_order.index(systolic_category) if systolic_category else 0
    diastolic_idx = category_order.index(diastolic_category) if diastolic_category else 0
    
    # 取更高的分类（更严重）
    final_idx = max(systolic_idx, diastolic_idx)
    final_category = category_order[final_idx]
    
    cat_info = BP_CATEGORIES_WHO[final_category]
    return (
        final_category,
        cat_info['label'],
        cat_info['label_en'],
        cat_info['risk'],
        cat_info['risk_desc']
    )


def get_pulse_pressure_category(pulse_pressure: float) -> Tuple[str, str, str]:
    """
    获取脉压差分类.
    
    Args:
        pulse_pressure: 脉压差 (mmHg)
    
    Returns:
        (分类键名, 中文标签, 描述)
    
    Examples:
        >>> get_pulse_pressure_category(40)
        ('normal', '正常脉压差', '脉压差在正常范围')
    """
    for cat_name, cat_info in PULSE_PRESSURE_CATEGORIES.items():
        range_min, range_max = cat_info['range']
        if range_min <= pulse_pressure < range_max:
            return cat_name, cat_info['label'], cat_info['desc']
    
    # 默认返回低脉压差
    return 'low', PULSE_PRESSURE_CATEGORIES['low']['label'], PULSE_PRESSURE_CATEGORIES['low']['desc']


def get_age_normal_range(age: int) -> Tuple[float, float, float, float]:
    """
    获取年龄对应的正常血压范围.
    
    Args:
        age: 年龄 (岁)
    
    Returns:
        (收缩压最小值, 收缩压最大值, 舒张压最小值, 舒张压最大值)
    
    Examples:
        >>> get_age_normal_range(10)
        (102, 128, 70, 92)
    """
    if age <= 17:
        range_data = AGE_BP_RANGES.get(age, AGE_BP_RANGES[17])
    elif age <= 39:
        range_data = AGE_BP_RANGES['adult_18_39']
    elif age <= 59:
        range_data = AGE_BP_RANGES['adult_40_59']
    else:
        range_data = AGE_BP_RANGES['adult_60_plus']
    
    return (
        range_data['systolic'][0],
        range_data['systolic'][1],
        range_data['diastolic'][0],
        range_data['diastolic'][1]
    )


def is_bp_age_appropriate(systolic: float, diastolic: float, age: int) -> bool:
    """
    检查血压是否符合年龄正常范围.
    
    Args:
        systolic: 收缩压
        diastolic: 舒张压
        age: 年龄
    
    Returns:
        是否在正常范围内
    
    Examples:
        >>> is_bp_age_appropriate(110, 70, 10)
        True
    """
    sys_min, sys_max, dia_min, dia_max = get_age_normal_range(age)
    return sys_min <= systolic <= sys_max and dia_min <= diastolic <= dia_max


def generate_recommendations(category: str, age: int, pulse_pressure_category: str) -> List[str]:
    """
    根据血压分类生成健康建议.
    
    Args:
        category: 血压分类
        age: 年龄
        pulse_pressure_category: 脉压差分类
    
    Returns:
        建议列表
    """
    recommendations = []
    
    # 根据血压分类
    if category in ['optimal', 'normal']:
        recommendations.append("继续保持健康的生活方式")
        recommendations.append("定期监测血压（至少每年一次）")
    elif category == 'high_normal':
        recommendations.append("改善生活方式：控制体重、减少盐摄入")
        recommendations.append("增加体育锻炼（每周至少150分钟中等强度）")
        recommendations.append("戒烟限酒")
        recommendations.append("每3-6个月监测血压")
    elif category == 'grade1_hypertension':
        recommendations.append("建议就医评估")
        recommendations.append("可能需要药物治疗")
        recommendations.append("严格控制饮食，减少盐摄入（<5g/天）")
        recommendations.append("每周至少监测血压2-3次")
    elif category in ['grade2_hypertension', 'grade3_hypertension']:
        recommendations.append("尽快就医，需要药物治疗")
        recommendations.append("定期随访（至少每月一次）")
        recommendations.append("监测血压变化，记录血压日记")
        recommendations.append("警惕高血压并发症")
    elif category == 'isolated_systolic_hypertension':
        recommendations.append("常见于老年人，需特别关注")
        recommendations.append("建议就医评估心血管风险")
        recommendations.append("控制收缩压是主要目标")
    
    # 根据脉压差
    if pulse_pressure_category == 'high':
        recommendations.append("脉压差过大，提示动脉硬化风险")
        recommendations.append("建议检查血管弹性")
    elif pulse_pressure_category == 'low':
        recommendations.append("脉压差偏低，可能影响心输出量")
    
    # 根据年龄
    if age >= 60:
        recommendations.append("老年人血压控制目标可适当放宽")
    
    return recommendations


def analyze_bp(
    systolic: float,
    diastolic: float,
    age: int,
    unit: BPUnit = BPUnit.MMHG
) -> BPResult:
    """
    完整的血压分析.
    
    Args:
        systolic: 收缩压
        diastolic: 舒张压
        age: 年龄
        unit: 血压单位
    
    Returns:
        BPResult 对象，包含完整分析结果
    
    Examples:
        >>> result = analyze_bp(120, 80, 30)
        >>> result.category
        'optimal'
        >>> result.pulse_pressure
        40
    """
    # 转换为 mmHg
    if unit == BPUnit.KPA:
        systolic = kpa_to_mmhg(systolic)
        diastolic = kpa_to_mmhg(diastolic)
    
    # 计算脉压差和 MAP
    pulse_pressure = calculate_pulse_pressure(systolic, diastolic)
    map_value = calculate_map(systolic, diastolic)
    
    # 分类血压
    category, label, label_en, risk, risk_desc = classify_bp(systolic, diastolic)
    
    # 分类脉压差
    pp_cat, pp_label, pp_desc = get_pulse_pressure_category(pulse_pressure)
    
    # 获取 MAP 状态
    map_status = get_map_status(map_value)
    
    # 检查年龄适宜性
    age_appropriate = is_bp_age_appropriate(systolic, diastolic, age)
    
    # 生成建议
    recommendations = generate_recommendations(category, age, pp_cat)
    
    return BPResult(
        systolic=systolic,
        diastolic=diastolic,
        category=category,
        category_label=label,
        category_label_en=label_en,
        risk_level=risk,
        risk_description=risk_desc,
        pulse_pressure=pulse_pressure,
        pulse_pressure_category=pp_cat,
        pulse_pressure_label=pp_label,
        map=map_value,
        map_status=map_status,
        age_appropriate=age_appropriate,
        recommendations=recommendations
    )


# ============================================================================
# Blood Pressure Statistics Functions
# ============================================================================

def calculate_bp_statistics(readings: List[Tuple[float, float]]) -> BPStatistics:
    """
    计算血压统计数据.
    
    Args:
        readings: 血压读数列表 [(收缩压, 舒张压), ...]
    
    Returns:
        BPStatistics 对象
    
    Examples:
        >>> readings = [(120, 80), (122, 82), (118, 78)]
        >>> stats = calculate_bp_statistics(readings)
        >>> stats.systolic_mean
        120.0
    """
    if not readings:
        raise ValueError("读数列表不能为空")
    
    systolics = [r[0] for r in readings]
    diastolics = [r[1] for r in readings]
    
    # 计算基本统计量
    sys_mean = sum(systolics) / len(systolics)
    sys_min = min(systolics)
    sys_max = max(systolics)
    
    dia_mean = sum(diastolics) / len(diastolics)
    dia_min = min(diastolics)
    dia_max = max(diastolics)
    
    # 计算标准差
    sys_std = (sum((s - sys_mean) ** 2 for s in systolics) / len(systolics)) ** 0.5
    dia_std = (sum((d - dia_mean) ** 2 for d in diastolics) / len(diastolics)) ** 0.5
    
    # 计算脉压差和 MAP 均值
    pp_mean = calculate_pulse_pressure(sys_mean, dia_mean)
    map_mean = calculate_map(sys_mean, dia_mean)
    
    # 确定主要分类
    category, _, _, _, _ = classify_bp(sys_mean, dia_mean)
    
    # 确定趋势
    if len(readings) >= 3:
        early_sys_mean = sum(systolics[:len(systolics)//2]) / (len(systolics)//2)
        late_sys_mean = sum(systolics[len(systolics)//2:]) / (len(systolics) - len(systolics)//2)
        
        diff = late_sys_mean - early_sys_mean
        
        if abs(diff) < 5:
            trend = 'stable'
        elif diff > 5:
            trend = 'increasing'
        elif diff < -5:
            trend = 'decreasing'
        else:
            trend = 'fluctuating'
    else:
        trend = 'insufficient_data'
    
    return BPStatistics(
        readings_count=len(readings),
        systolic_mean=round(sys_mean, 1),
        systolic_min=sys_min,
        systolic_max=sys_max,
        systolic_std=round(sys_std, 2),
        diastolic_mean=round(dia_mean, 1),
        diastolic_min=dia_min,
        diastolic_max=dia_max,
        diastolic_std=round(dia_std, 2),
        pulse_pressure_mean=round(pp_mean, 1),
        map_mean=round(map_mean, 2),
        dominant_category=category,
        trend=trend
    )


def analyze_bp_trend(readings: List[Tuple[float, float, Optional[datetime]]]) -> Dict:
    """
    分析血压趋势.
    
    Args:
        readings: 血压读数列表 [(收缩压, 舒张压, 时间戳), ...]
    
    Returns:
        趋势分析字典
    
    Examples:
        >>> readings = [(120, 80, None), (122, 82, None), (125, 85, None)]
        >>> analyze_bp_trend(readings)
        {'systolic_trend': 'increasing', ...}
    """
    if not readings:
        return {'error': '无数据'}
    
    systolics = [r[0] for r in readings]
    diastolics = [r[1] for r in readings]
    
    # 计算趋势方向
    sys_first = systolics[0]
    sys_last = systolics[-1]
    sys_change = sys_last - sys_first
    
    dia_first = diastolics[0]
    dia_last = diastolics[-1]
    dia_change = dia_last - dia_first
    
    # 计算变化率（如果有时间戳）
    time_analysis = {}
    if len(readings) >= 2 and readings[0][2] and readings[-1][2]:
        time_diff = (readings[-1][2] - readings[0][2]).days
        if time_diff > 0:
            sys_rate = sys_change / time_diff
            dia_rate = dia_change / time_diff
            time_analysis = {
                'days_elapsed': time_diff,
                'systolic_daily_change': round(sys_rate, 2),
                'diastolic_daily_change': round(dia_rate, 2),
            }
    
    return {
        'systolic_trend': 'increasing' if sys_change > 5 else ('decreasing' if sys_change < -5 else 'stable'),
        'diastolic_trend': 'increasing' if dia_change > 5 else ('decreasing' if dia_change < -5 else 'stable'),
        'systolic_change': round(sys_change, 1),
        'diastolic_change': round(dia_change, 1),
        'readings_count': len(readings),
        **time_analysis
    }


# ============================================================================
# Pediatric Blood Pressure Functions
# ============================================================================

# Simplified pediatric BP percentile data (approximate)
# Based on 50th percentile values
PED_BP_DATA = {
    'male': {
        1: {'sys_50': 90, 'dia_50': 55},
        2: {'sys_50': 92, 'dia_50': 58},
        3: {'sys_50': 94, 'dia_50': 60},
        4: {'sys_50': 96, 'dia_50': 62},
        5: {'sys_50': 98, 'dia_50': 64},
        6: {'sys_50': 100, 'dia_50': 66},
        7: {'sys_50': 102, 'dia_50': 68},
        8: {'sys_50': 104, 'dia_50': 70},
        9: {'sys_50': 106, 'dia_50': 72},
        10: {'sys_50': 108, 'dia_50': 74},
        11: {'sys_50': 110, 'dia_50': 76},
        12: {'sys_50': 112, 'dia_50': 78},
        13: {'sys_50': 114, 'dia_50': 80},
        14: {'sys_50': 116, 'dia_50': 82},
        15: {'sys_50': 118, 'dia_50': 84},
        16: {'sys_50': 120, 'dia_50': 86},
        17: {'sys_50': 122, 'dia_50': 88},
    },
    'female': {
        1: {'sys_50': 88, 'dia_50': 54},
        2: {'sys_50': 90, 'dia_50': 56},
        3: {'sys_50': 92, 'dia_50': 58},
        4: {'sys_50': 94, 'dia_50': 60},
        5: {'sys_50': 96, 'dia_50': 62},
        6: {'sys_50': 98, 'dia_50': 64},
        7: {'sys_50': 100, 'dia_50': 66},
        8: {'sys_50': 102, 'dia_50': 68},
        9: {'sys_50': 104, 'dia_50': 70},
        10: {'sys_50': 106, 'dia_50': 72},
        11: {'sys_50': 108, 'dia_50': 74},
        12: {'sys_50': 110, 'dia_50': 76},
        13: {'sys_50': 112, 'dia_50': 78},
        14: {'sys_50': 114, 'dia_50': 80},
        15: {'sys_50': 116, 'dia_50': 82},
        16: {'sys_50': 118, 'dia_50': 84},
        17: {'sys_50': 120, 'dia_50': 86},
    },
}


def calculate_child_bp_percentile(
    systolic: float,
    diastolic: float,
    age: int,
    gender: Gender
) -> float:
    """
    计算儿童血压百分位数.
    
    Args:
        systolic: 收缩压 (mmHg)
        diastolic: 舒张压 (mmHg)
        age: 年龄 (1-17岁)
        gender: 性别
    
    Returns:
        百分位数 (估算值)
    
    Examples:
        >>> calculate_child_bp_percentile(100, 65, 8, Gender.MALE)
        50.0  # 大约
    """
    if age < 1 or age > 17:
        raise ValueError("儿童血压百分位数计算仅适用于 1-17 岁")
    
    gender_key = 'male' if gender == Gender.MALE else 'female'
    ref_data = PED_BP_DATA[gender_key].get(age)
    
    if not ref_data:
        ref_data = PED_BP_DATA[gender_key][17]
    
    # 使用简化公式估算百分位数
    sys_50 = ref_data['sys_50']
    dia_50 = ref_data['dia_50']
    
    # 标准差估算（约为中位值的10%）
    sys_sd = sys_50 * 0.1
    dia_sd = dia_50 * 0.1
    
    # 计算 Z-score 并转换为百分位数
    sys_z = (systolic - sys_50) / sys_sd
    dia_z = (diastolic - dia_50) / dia_sd
    
    # 使用收缩压和舒张压的平均 Z-score
    avg_z = (sys_z + dia_z) / 2
    
    # Z-score 转换为百分位数（简化）
    percentile = 50 + avg_z * 15
    
    return round(max(1, min(99, percentile)), 1)


def analyze_child_bp(
    systolic: float,
    diastolic: float,
    age: int,
    gender: Gender,
    unit: BPUnit = BPUnit.MMHG
) -> ChildBPResult:
    """
    完整的儿童血压分析.
    
    Args:
        systolic: 收缩压
        diastolic: 舒张压
        age: 年龄 (1-17岁)
        gender: 性别
        unit: 血压单位
    
    Returns:
        ChildBPResult 对象
    
    Examples:
        >>> result = analyze_child_bp(100, 65, 8, Gender.MALE)
        >>> result.percentile
        50.0
    """
    # 转换为 mmHg
    if unit == BPUnit.KPA:
        systolic = kpa_to_mmhg(systolic)
        diastolic = kpa_to_mmhg(diastolic)
    
    # 计算百分位数
    percentile = calculate_child_bp_percentile(systolic, diastolic, age, gender)
    
    # 分类
    if percentile < 90:
        category = 'normal'
        label = '正常血压'
        risk = 'low'
    elif percentile < 95:
        category = 'prehypertension'
        label = '血压偏高（临界）'
        risk = 'moderate'
    else:
        category = 'hypertension'
        label = '高血压'
        risk = 'high'
    
    # 生成建议
    recommendations = []
    if category == 'normal':
        recommendations.append("血压在正常范围")
        recommendations.append("保持健康饮食和适量运动")
    elif category == 'prehypertension':
        recommendations.append("血压偏高，建议改善生活方式")
        recommendations.append("减少高盐高脂食物")
        recommendations.append("增加户外活动")
        recommendations.append("定期监测血压")
    else:
        recommendations.append("血压偏高，建议就医")
        recommendations.append("可能需要进一步检查")
        recommendations.append("建立血压监测日记")
    
    return ChildBPResult(
        systolic=systolic,
        diastolic=diastolic,
        age=age,
        percentile=percentile,
        percentile_category=category,
        percentile_label=label,
        risk_level=risk,
        recommendations=recommendations
    )


# ============================================================================
# Utility Functions
# ============================================================================

def get_bp_summary(systolic: float, diastolic: float) -> str:
    """
    获取血压简要说明.
    
    Args:
        systolic: 收缩压 (mmHg)
        diastolic: 舒张压 (mmHg)
    
    Returns:
        简要说明字符串
    
    Examples:
        >>> get_bp_summary(120, 80)
        '血压 120/80 mmHg - 理想血压，心血管风险最低'
    """
    category, label, label_en, risk, risk_desc = classify_bp(systolic, diastolic)
    return f"血压 {systolic}/{diastolic} mmHg - {label}，{risk_desc}"


def calculate_hypertension_stage(systolic: float, diastolic: float) -> str:
    """
    计算高血压分期（美国心脏协会标准）.
    
    Args:
        systolic: 收缩压 (mmHg)
        diastolic: 舒张压 (mmHg)
    
    Returns:
        高血压分期描述
    
    Examples:
        >>> calculate_hypertension_stage(145, 95)
        'Hypertension Stage 1'
    """
    # Hypertensive Crisis
    if systolic >= 180 or diastolic >= 120:
        return 'Hypertensive Crisis'
    
    # Hypertension Stage 2 (>=140 or >=100)
    if systolic >= 140 or diastolic >= 100:
        return 'Hypertension Stage 2'
    
    # Hypertension Stage 1 (130-139 or 80-89)
    if systolic >= 130 or (diastolic >= 80 and diastolic < 90):
        return 'Hypertension Stage 1'
    
    # Elevated (120-129/<80)
    if systolic >= 120 and diastolic < 80:
        return 'Elevated'
    
    # Normal (<120/<80)
    return 'Normal'


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Blood Pressure Utilities Demo")
    print("=" * 60)
    
    # 成人血压分析
    print("\n--- 成人血压分析 ---")
    result = analyze_bp(120, 80, 35)
    print(f"血压: 120/80 mmHg")
    print(f"分类: {result.category_label} ({result.category_label_en})")
    print(f"风险: {result.risk_level} - {result.risk_description}")
    print(f"脉压差: {result.pulse_pressure} mmHg - {result.pulse_pressure_label}")
    print(f"MAP: {result.map} mmHg - {result.map_status}")
    print(f"年龄适宜: {result.age_appropriate}")
    print(f"建议: {result.recommendations[0]}")
    
    # 高血压分析
    print("\n--- 高血压分析 ---")
    result2 = analyze_bp(155, 95, 50)
    print(f"血压: 155/95 mmHg")
    print(f"分类: {result2.category_label}")
    print(f"风险: {result2.risk_level}")
    print(f"建议: {result2.recommendations[:2]}")
    
    # 血压统计
    print("\n--- 血压统计 ---")
    readings = [(120, 80), (122, 82), (118, 78), (125, 83), (119, 79)]
    stats = calculate_bp_statistics(readings)
    print(f"读数数量: {stats.readings_count}")
    print(f"收缩压均值: {stats.systolic_mean} mmHg (范围: {stats.systolic_min}-{stats.systolic_max})")
    print(f"舒张压均值: {stats.diastolic_mean} mmHg (范围: {stats.diastolic_min}-{stats.diastolic_max})")
    print(f"脉压差均值: {stats.pulse_pressure_mean} mmHg")
    print(f"MAP均值: {stats.map_mean} mmHg")
    print(f"主要分类: {stats.dominant_category}")
    print(f"趋势: {stats.trend}")
    
    # 儿童血压分析
    print("\n--- 儿童血压分析 ---")
    child_result = analyze_child_bp(105, 70, 10, Gender.MALE)
    print(f"血压: 105/70 mmHg, 年龄: 10岁, 性别: 男")
    print(f"百分位数: {child_result.percentile}%")
    print(f"分类: {child_result.percentile_label}")
    print(f"风险: {child_result.risk_level}")
    
    # 单位转换
    print("\n--- 单位转换 ---")
    kpa_value = mmhg_to_kpa(120)
    print(f"120 mmHg = {kpa_value} kPa")
    mmhg_value = kpa_to_mmhg(16)
    print(f"16 kPa = {mmhg_value} mmHg")
    
    # 简要说明
    print("\n--- 简要说明 ---")
    print(get_bp_summary(120, 80))
    print(get_bp_summary(145, 92))
    
    print("\n" + "=" * 60)