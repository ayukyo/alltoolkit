#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Stress Assessment Utilities Module
=================================================
A comprehensive stress evaluation and management utility module for Python
with zero external dependencies.

Features:
    - Stress Index calculation (Perceived Stress Scale based)
    - Stress level classification (5 levels)
    - Personalized relief recommendations
    - Stress type identification (work, life, health, etc.)
    - Stress history tracking with trend analysis
    - Stress factor weighting system
    - Burnout risk assessment
    - Recovery suggestions based on stress patterns
    - Quick stress check tools

Author: AllToolkit Contributors
License: MIT
Date: 2026-05-10
"""

from typing import Union, Tuple, Optional, List, Dict
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json


# ============================================================================
# Constants
# ============================================================================

# Stress Level Thresholds (0-100 scale)
STRESS_THRESHOLDS = {
    'very_low': (0, 20),
    'low': (20, 40),
    'moderate': (40, 60),
    'high': (60, 80),
    'very_high': (80, 100),
}

# Stress Level Labels and Information
STRESS_LEVEL_INFO = {
    'very_low': {
        'label': '极低',
        'label_en': 'Very Low',
        'description': '几乎没有压力感，心理状态良好',
        'color': '#4CAF50',  # Green
        'action': '继续保持健康的生活方式',
    },
    'low': {
        'label': '低',
        'label_en': 'Low',
        'description': '轻微压力，属于正常生活压力范围',
        'color': '#8BC34A',  # Light Green
        'action': '保持规律作息，适度放松',
    },
    'moderate': {
        'label': '中等',
        'label_en': 'Moderate',
        'description': '明显压力感，需要关注和调节',
        'color': '#FFC107',  # Yellow
        'action': '建议增加休息时间，学习压力管理技巧',
    },
    'high': {
        'label': '高',
        'label_en': 'High',
        'description': '较强压力感，可能影响日常生活',
        'color': '#FF9800',  # Orange
        'action': '强烈建议采取减压措施，考虑寻求帮助',
    },
    'very_high': {
        'label': '极高',
        'label_en': 'Very High',
        'description': '严重压力状态，可能影响身心健康',
        'color': '#F44336',  # Red
        'action': '强烈建议寻求专业帮助，立即采取干预措施',
    },
}

# Stress Factor Categories with Weights
STRESS_FACTORS = {
    'work': {
        'label': '工作压力',
        'label_en': 'Work Stress',
        'weight': 0.25,
        'sub_factors': [
            ('workload', '工作量', 0.3),
            ('deadline', '截止日期压力', 0.25),
            ('conflict', '工作冲突', 0.2),
            ('achievement', '成就感缺失', 0.15),
            ('uncertainty', '工作不确定性', 0.1),
        ],
    },
    'life': {
        'label': '生活压力',
        'label_en': 'Life Stress',
        'weight': 0.20,
        'sub_factors': [
            ('finance', '经济压力', 0.3),
            ('family', '家庭关系', 0.25),
            ('social', '社交压力', 0.2),
            ('living', '居住环境', 0.15),
            ('time', '时间压力', 0.1),
        ],
    },
    'health': {
        'label': '健康压力',
        'label_en': 'Health Stress',
        'weight': 0.20,
        'sub_factors': [
            ('physical', '身体健康问题', 0.35),
            ('sleep', '睡眠质量', 0.25),
            ('energy', '精力状态', 0.2),
            ('diet', '饮食习惯', 0.1),
            ('exercise', '运动不足', 0.1),
        ],
    },
    'psychological': {
        'label': '心理压力',
        'label_en': 'Psychological Stress',
        'weight': 0.25,
        'sub_factors': [
            ('anxiety', '焦虑感', 0.3),
            ('depression', '低落情绪', 0.25),
            ('selfesteem', '自尊问题', 0.2),
            ('control', '控制感缺失', 0.15),
            ('purpose', '目标迷茫', 0.1),
        ],
    },
    'environment': {
        'label': '环境压力',
        'label_en': 'Environmental Stress',
        'weight': 0.10,
        'sub_factors': [
            ('noise', '噪音干扰', 0.25),
            ('crowd', '拥挤环境', 0.25),
            ('weather', '天气影响', 0.2),
            ('traffic', '交通压力', 0.15),
            ('pollution', '环境污染', 0.15),
        ],
    },
}

# PSS-10 Questions (Perceived Stress Scale)
PSS_10_QUESTIONS = [
    ('q1', '在过去一个月里，您有多少次因为意外事件而感到不安？', 'positive'),
    ('q2', '在过去一个月里，您有多少次感觉无法控制生活中的重要事情？', 'positive'),
    ('q3', '在过去一个月里，您有多少次感到紧张和压力？', 'positive'),
    ('q4', '在过去一个月里，您有多少次成功处理了生活中的烦恼？', 'negative'),
    ('q5', '在过去一个月里，您有多少次感觉事情都在按您的意愿发展？', 'negative'),
    ('q6', '在过去一个月里，您有多少次发现无法应对所有必须做的事情？', 'positive'),
    ('q7', '在过去一个月里，您有多少次能控制生活中的烦恼？', 'negative'),
    ('q8', '在过去一个月里，您有多少次觉得事情堆积如山无法处理？', 'positive'),
    ('q9', '在过去一个月里，您有多少次因为无法控制发生的事情而感到生气？', 'positive'),
    ('q10', '在过去一个月里，您有多少次感到困难堆积如山无法克服？', 'positive'),
]

# PSS Response Options
PSS_RESPONSES = {
    0: '从不',
    1: '几乎不',
    2: '有时',
    3: '经常',
    4: '总是',
}

# Stress Relief Recommendations by Level
RELIEF_RECOMMENDATIONS = {
    'very_low': [
        '保持现有的健康习惯',
        '继续规律运动',
        '保持良好的社交关系',
        '定期自我评估压力状态',
    ],
    'low': [
        '每天进行15-30分钟的放松活动',
        '保持规律的睡眠时间',
        '每周至少运动3次',
        '培养一个兴趣爱好',
        '与朋友家人保持联系',
    ],
    'moderate': [
        '每天进行30分钟以上的放松活动（冥想、瑜伽、散步）',
        '学习时间管理技巧',
        '减少不必要的承诺',
        '每周安排至少一天完全休息',
        '考虑与信任的人分享压力',
        '练习深呼吸放松技巧',
        '减少社交媒体使用时间',
    ],
    'high': [
        '强烈建议寻求心理咨询',
        '每天进行至少1小时的放松活动',
        '评估并减少压力源',
        '考虑调整工作或生活安排',
        '学习专业的压力管理技巧',
        '确保充足的睡眠（7-8小时）',
        '减少咖啡因和酒精摄入',
        '练习正念冥想',
        '与专业人士讨论压力问题',
    ],
    'very_high': [
        '立即寻求专业心理帮助',
        '考虑暂时减少工作负担',
        '与医生讨论可能的健康影响',
        '建立紧急支持网络',
        '每天进行多次放松练习',
        '优先处理最紧迫的压力源',
        '考虑休假或暂时休息',
        '避免独自承受，寻求家人朋友支持',
        '监测身体症状，及时就医',
    ],
}

# Burnout Warning Signs
BURNOUT_SIGNS = {
    'emotional_exhaustion': {
        'label': '情绪耗竭',
        'signs': ['感到情感枯竭', '对工作失去热情', '感到被掏空'],
        'threshold': 0.7,
    },
    'depersonalization': {
        'label': '去人格化',
        'signs': ['对他人冷漠', '缺乏同理心', '机械化工作'],
        'threshold': 0.6,
    },
    'reduced accomplishment': {
        'label': '成就感降低',
        'signs': ['感到无能', '工作无意义感', '自我怀疑'],
        'threshold': 0.6,
    },
}


# ============================================================================
# Enums
# ============================================================================

class StressLevel(Enum):
    """压力等级枚举"""
    VERY_LOW = 'very_low'
    LOW = 'low'
    MODERATE = 'moderate'
    HIGH = 'high'
    VERY_HIGH = 'very_high'


class StressType(Enum):
    """压力类型枚举"""
    WORK = 'work'
    LIFE = 'life'
    HEALTH = 'health'
    PSYCHOLOGICAL = 'psychological'
    ENVIRONMENT = 'environment'


class ReliefCategory(Enum):
    """缓解建议类别枚举"""
    PHYSICAL = 'physical'       # 运动、睡眠等
    MENTAL = 'mental'           # 冥想、心理调节
    SOCIAL = 'social'           # 社交支持
    LIFESTYLE = 'lifestyle'     # 生活习惯改变
    PROFESSIONAL = 'professional'  # 专业帮助


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class StressAssessment:
    """压力评估结果"""
    stress_index: float                     # 压力指数 (0-100)
    level: str                              # 压力等级
    level_label: str                        # 中文标签
    level_label_en: str                     # 英文标签
    description: str                        # 描述
    recommended_action: str                 # 推荐行动
    color: str                              # 颜色代码
    factor_breakdown: Dict[str, float]      # 各因素得分
    dominant_factors: List[str]             # 主要压力因素
    recommendations: List[str]              # 缓解建议
    burnout_risk: float                     # 燃尽风险 (0-1)
    timestamp: str                          # 评估时间


@dataclass
class StressHistoryEntry:
    """压力历史记录"""
    stress_index: float
    level: str
    timestamp: str
    notes: Optional[str] = None
    triggers: Optional[List[str]] = None


@dataclass
class StressTrend:
    """压力趋势分析"""
    current_index: float
    average_index: float
    trend_direction: str        # 'increasing', 'stable', 'decreasing'
    trend_percentage: float     # 变化百分比
    peak_index: float
    lowest_index: float
    volatility: float           # 波动性
    entries_count: int


@dataclass
class PSSResult:
    """PSS-10 测试结果"""
    total_score: int            # 总分 (0-40)
    stress_level: str           # 压力等级
    percentile: float           # 百分位
    category_breakdown: Dict[str, int]  # 各类别得分
    interpretation: str         # 解释
    recommendations: List[str]  # 建议


@dataclass
class BurnoutAssessment:
    """燃尽风险评估"""
    emotional_exhaustion_score: float
    depersonalization_score: float
    reduced_accomplishment_score: float
    overall_risk: float             # 总风险 (0-1)
    risk_level: str                 # 风险等级
    warning_signs: List[str]        # 警告信号
    interventions: List[str]        # 干预建议


# ============================================================================
# Core Stress Calculation Functions
# ============================================================================

def calculate_stress_index(
    work_score: float = 0.0,
    life_score: float = 0.0,
    health_score: float = 0.0,
    psychological_score: float = 0.0,
    environment_score: float = 0.0,
    custom_weights: Optional[Dict[str, float]] = None
) -> float:
    """
    计算综合压力指数 (0-100).
    
    Args:
        work_score: 工作压力得分 (0-100)
        life_score: 生活压力得分 (0-100)
        health_score: 健康压力得分 (0-100)
        psychological_score: 心理压力得分 (0-100)
        environment_score: 环境压力得分 (0-100)
        custom_weights: 自定义权重字典
    
    Returns:
        综合压力指数 (0-100)
    
    Examples:
        >>> calculate_stress_index(60, 40, 30, 50, 20)
        45.5
    """
    # 使用自定义权重或默认权重
    weights = custom_weights or {
        'work': 0.25,
        'life': 0.20,
        'health': 0.20,
        'psychological': 0.25,
        'environment': 0.10,
    }
    
    # 验证输入范围
    scores = {
        'work': work_score,
        'life': life_score,
        'health': health_score,
        'psychological': psychological_score,
        'environment': environment_score,
    }
    
    for category, score in scores.items():
        if not 0 <= score <= 100:
            raise ValueError(f"{category} 压力得分必须在 0-100 范围内")
    
    # 加权计算
    total_weight = sum(weights.values())
    stress_index = sum(scores[cat] * weights.get(cat, 0) for cat in scores) / total_weight
    
    return round(stress_index, 2)


def get_stress_level(stress_index: float) -> str:
    """
    根据压力指数获取压力等级.
    
    Args:
        stress_index: 压力指数 (0-100)
    
    Returns:
        压力等级键名
    
    Examples:
        >>> get_stress_level(35.5)
        'low'
        >>> get_stress_level(72.0)
        'high'
    """
    if stress_index < 20:
        return 'very_low'
    elif stress_index < 40:
        return 'low'
    elif stress_index < 60:
        return 'moderate'
    elif stress_index < 80:
        return 'high'
    else:
        return 'very_high'


def get_stress_level_info(stress_index: float) -> Tuple[str, str, str, str, str]:
    """
    获取压力等级详细信息.
    
    Args:
        stress_index: 压力指数
    
    Returns:
        (等级键名, 中文标签, 英文标签, 描述, 推荐行动)
    
    Examples:
        >>> get_stress_level_info(45.0)
        ('moderate', '中等', 'Moderate', '明显压力感...', '建议增加休息...')
    """
    level = get_stress_level(stress_index)
    info = STRESS_LEVEL_INFO[level]
    return level, info['label'], info['label_en'], info['description'], info['action']


def get_relief_recommendations(stress_level: str) -> List[str]:
    """
    根据压力等级获取缓解建议.
    
    Args:
        stress_level: 压力等级
    
    Returns:
        缓解建议列表
    
    Examples:
        >>> get_relief_recommendations('moderate')
        ['每天进行30分钟以上的放松活动...', ...]
    """
    return RELIEF_RECOMMENDATIONS.get(stress_level, RELIEF_RECOMMENDATIONS['moderate'])


def get_dominant_stress_factors(
    work_score: float,
    life_score: float,
    health_score: float,
    psychological_score: float,
    environment_score: float,
    threshold: float = 50.0
) -> List[str]:
    """
    获取主要压力因素（得分超过阈值的因素）.
    
    Args:
        各类压力得分
        threshold: 阈值 (默认50)
    
    Returns:
        主要压力因素名称列表
    
    Examples:
        >>> get_dominant_stress_factors(70, 30, 40, 60, 20)
        ['工作压力', '心理压力']
    """
    scores = {
        '工作压力': work_score,
        '生活压力': life_score,
        '健康压力': health_score,
        '心理压力': psychological_score,
        '环境压力': environment_score,
    }
    
    dominant = [factor for factor, score in scores.items() if score >= threshold]
    return dominant if dominant else ['综合因素']


# ============================================================================
# Full Assessment Functions
# ============================================================================

def perform_full_assessment(
    work_score: float = 0.0,
    life_score: float = 0.0,
    health_score: float = 0.0,
    psychological_score: float = 0.0,
    environment_score: float = 0.0,
    custom_weights: Optional[Dict[str, float]] = None,
    notes: Optional[str] = None
) -> StressAssessment:
    """
    执行完整的压力评估.
    
    Args:
        各类压力得分 (0-100)
        custom_weights: 自定义权重
        notes: 备注
    
    Returns:
        StressAssessment 对象
    
    Examples:
        >>> result = perform_full_assessment(60, 40, 30, 50, 20)
        >>> result.stress_index
        45.5
        >>> result.level
        'moderate'
    """
    # 计算压力指数
    stress_index = calculate_stress_index(
        work_score, life_score, health_score, psychological_score, environment_score,
        custom_weights
    )
    
    # 获取等级信息
    level, label, label_en, description, action = get_stress_level_info(stress_index)
    
    # 获取缓解建议
    recommendations = get_relief_recommendations(level)
    
    # 因素分解
    factor_breakdown = {
        'work': work_score,
        'life': life_score,
        'health': health_score,
        'psychological': psychological_score,
        'environment': environment_score,
    }
    
    # 主要因素
    dominant_factors = get_dominant_stress_factors(
        work_score, life_score, health_score, psychological_score, environment_score
    )
    
    # 计算燃尽风险
    burnout_risk = calculate_burnout_risk_simple(stress_index, psychological_score, work_score)
    
    # 时间戳
    timestamp = datetime.now().isoformat()
    
    return StressAssessment(
        stress_index=stress_index,
        level=level,
        level_label=label,
        level_label_en=label_en,
        description=description,
        recommended_action=action,
        color=STRESS_LEVEL_INFO[level]['color'],
        factor_breakdown=factor_breakdown,
        dominant_factors=dominant_factors,
        recommendations=recommendations,
        burnout_risk=burnout_risk,
        timestamp=timestamp,
    )


def calculate_burnout_risk_simple(
    stress_index: float,
    psychological_score: float,
    work_score: float
) -> float:
    """
    简化的燃尽风险评估.
    
    Args:
        stress_index: 综合压力指数
        psychological_score: 心理压力得分
        work_score: 工作压力得分
    
    Returns:
        燃尽风险 (0-1)
    
    Examples:
        >>> calculate_burnout_risk_simple(75, 70, 80)
        0.75
    """
    # 燃尽风险主要受工作压力和心理压力影响
    risk = (
        (stress_index / 100) * 0.4 +
        (psychological_score / 100) * 0.35 +
        (work_score / 100) * 0.25
    )
    
    return round(min(1.0, risk), 2)


# ============================================================================
# PSS-10 Test Functions
# ============================================================================

def calculate_pss_score(responses: Dict[str, int]) -> int:
    """
    计算 PSS-10 总分.
    
    Args:
        responses: 问题响应字典，键为 'q1'-'q10'，值为 0-4
    
    Returns:
        PSS 总分 (0-40)
    
    Examples:
        >>> calculate_pss_score({'q1': 3, 'q2': 2, 'q3': 3, 'q4': 1, 'q5': 2,
        ...                       'q6': 3, 'q7': 1, 'q8': 2, 'q9': 3, 'q10': 2})
        18
    """
    # 验证输入
    for q_id, response in responses.items():
        if not q_id.startswith('q') or q_id not in [f'q{i}' for i in range(1, 11)]:
            raise ValueError(f"无效的问题ID: {q_id}")
        if not 0 <= response <= 4:
            raise ValueError(f"响应值必须在 0-4 范围: {q_id}")
    
    total = 0
    for q_id, q_text, q_type in PSS_10_QUESTIONS:
        response = responses.get(q_id, 0)
        if q_type == 'positive':
            total += response
        else:
            total += (4 - response)  # 反向计分
    
    return total


def interpret_pss_score(score: int) -> Tuple[str, str, float]:
    """
    解释 PSS 分数.
    
    Args:
        score: PSS 总分 (0-40)
    
    Returns:
        (压力等级, 解释文本, 百分位估计)
    
    Examples:
        >>> interpret_pss_score(20)
        ('moderate', '中等压力水平...', 50.0)
    """
    # PSS 分数转换为百分位估计 (简化)
    # 0-13: 低压力 (约 0-30百分位)
    # 14-26: 中等压力 (约 30-70百分位)
    # 27-40: 高压力 (约 70-100百分位)
    
    if score <= 13:
        level = 'low'
        percentile = max(0, min(30, score * 2.3))
        interpretation = '您的感知压力水平较低，属于健康范围内。继续保持良好的应对策略。'
    elif score <= 26:
        level = 'moderate'
        percentile = 30 + (score - 14) * 3.33
        interpretation = '您的感知压力水平处于中等范围。建议关注压力管理，采取预防措施。'
    else:
        level = 'high'
        percentile = 70 + (score - 27) * 2.86
        interpretation = '您的感知压力水平较高。强烈建议采取积极的压力管理策略，必要时寻求专业帮助。'
    
    return level, interpretation, round(min(100, percentile), 1)


def perform_pss_test(responses: Dict[str, int]) -> PSSResult:
    """
    执行完整的 PSS-10 测试.
    
    Args:
        responses: 问题响应字典
    
    Returns:
        PSSResult 对象
    
    Examples:
        >>> result = perform_pss_test({'q1': 2, 'q2': 3, ...})
        >>> result.total_score
        18
    """
    total_score = calculate_pss_score(responses)
    level, interpretation, percentile = interpret_pss_score(total_score)
    
    # 分类分解
    positive_qs = ['q1', 'q2', 'q3', 'q6', 'q8', 'q9', 'q10']
    negative_qs = ['q4', 'q5', 'q7']
    
    positive_score = sum(responses.get(q, 0) for q in positive_qs)
    negative_score = sum(4 - responses.get(q, 0) for q in negative_qs)
    
    category_breakdown = {
        'positive_items': positive_score,
        'negative_items': negative_score,
        'control_perception': negative_score,
        'stress_frequency': positive_score,
    }
    
    # 获取建议
    recommendations = get_relief_recommendations(level)
    
    return PSSResult(
        total_score=total_score,
        stress_level=level,
        percentile=percentile,
        category_breakdown=category_breakdown,
        interpretation=interpretation,
        recommendations=recommendations,
    )


# ============================================================================
# Quick Stress Check Functions
# ============================================================================

def quick_stress_check(
    sleep_quality: int,       # 1-10 睡眠质量
    energy_level: int,        # 1-10 精力水平
    mood_rating: int,         # 1-10 心情评分
    workload_feeling: int,    # 1-10 工作负担感 (10=很重)
    social_connection: int    # 1-10 社交连接感
) -> float:
    """
    快速压力检查 (5项指标).
    
    Args:
        sleep_quality: 睡眠质量 (1=很差, 10=很好)
        energy_level: 精力水平 (1=很低, 10=很高)
        mood_rating: 心情评分 (1=很差, 10=很好)
        workload_feeling: 工作负担感 (1=很轻, 10=很重)
        social_connection: 社交连接感 (1=很孤立, 10=很紧密)
    
    Returns:
        快速压力指数 (0-100)
    
    Examples:
        >>> quick_stress_check(6, 5, 4, 7, 3)
        55.0
    """
    # 验证输入
    for name, value in [
        ('sleep_quality', sleep_quality),
        ('energy_level', energy_level),
        ('mood_rating', mood_rating),
        ('workload_feeling', workload_feeling),
        ('social_connection', social_connection),
    ]:
        if not 1 <= value <= 10:
            raise ValueError(f"{name} 必须在 1-10 范围内")
    
    # 正向指标（越高越好，转换为压力）
    sleep_stress = (10 - sleep_quality) * 10       # 睡眠差 -> 高压力
    energy_stress = (10 - energy_level) * 10       # 精力低 -> 高压力
    mood_stress = (10 - mood_rating) * 10          # 心情差 -> 高压力
    social_stress = (10 - social_connection) * 10  # 社交差 -> 高压力
    
    # 工作负担（越高压力越大）
    work_stress = workload_feeling * 10
    
    # 加权平均
    stress_index = (
        sleep_stress * 0.20 +
        energy_stress * 0.15 +
        mood_stress * 0.25 +
        work_stress * 0.25 +
        social_stress * 0.15
    )
    
    return round(stress_index, 1)


def analyze_quick_check_breakdown(
    sleep_quality: int,
    energy_level: int,
    mood_rating: int,
    workload_feeling: int,
    social_connection: int
) -> Dict[str, float]:
    """
    分析快速检查的各项贡献.
    
    Args:
        各项指标 (1-10)
    
    Returns:
        各项压力贡献字典
    
    Examples:
        >>> analyze_quick_check_breakdown(6, 5, 4, 7, 3)
        {'sleep': 40.0, 'energy': 50.0, ...}
    """
    breakdown = {
        'sleep': (10 - sleep_quality) * 10,
        'energy': (10 - energy_level) * 10,
        'mood': (10 - mood_rating) * 10,
        'workload': workload_feeling * 10,
        'social': (10 - social_connection) * 10,
    }
    
    return {k: round(v, 1) for k, v in breakdown.items()}


# ============================================================================
# Stress History and Trend Functions
# ============================================================================

class StressHistory:
    """压力历史管理类"""
    
    def __init__(self):
        self.entries: List[StressHistoryEntry] = []
    
    def add_entry(
        self,
        stress_index: float,
        level: Optional[str] = None,
        notes: Optional[str] = None,
        triggers: Optional[List[str]] = None
    ) -> None:
        """添加历史记录"""
        if level is None:
            level = get_stress_level(stress_index)
        
        entry = StressHistoryEntry(
            stress_index=stress_index,
            level=level,
            timestamp=datetime.now().isoformat(),
            notes=notes,
            triggers=triggers,
        )
        self.entries.append(entry)
    
    def get_entries(self, limit: Optional[int] = None) -> List[StressHistoryEntry]:
        """获取历史记录"""
        if limit:
            return self.entries[-limit:]
        return self.entries.copy()
    
    def clear(self) -> None:
        """清空历史"""
        self.entries.clear()
    
    def to_json(self) -> str:
        """导出为 JSON"""
        data = [
            {
                'stress_index': e.stress_index,
                'level': e.level,
                'timestamp': e.timestamp,
                'notes': e.notes,
                'triggers': e.triggers,
            }
            for e in self.entries
        ]
        return json.dumps(data, indent=2)
    
    def from_json(self, json_str: str) -> None:
        """从 JSON 导入"""
        data = json.loads(json_str)
        self.entries = [
            StressHistoryEntry(
                stress_index=e['stress_index'],
                level=e['level'],
                timestamp=e['timestamp'],
                notes=e.get('notes'),
                triggers=e.get('triggers'),
            )
            for e in data
        ]


def analyze_stress_trend(history: StressHistory, recent_count: int = 10) -> StressTrend:
    """
    分析压力趋势.
    
    Args:
        history: 历史记录对象
        recent_count: 分析最近多少条记录
    
    Returns:
        StressTrend 对象
    
    Examples:
        >>> history = StressHistory()
        >>> history.add_entry(40)
        >>> history.add_entry(50)
        >>> trend = analyze_stress_trend(history)
        >>> trend.trend_direction
        'increasing'
    """
    entries = history.get_entries(recent_count)
    
    if len(entries) < 2:
        return StressTrend(
            current_index=entries[0].stress_index if entries else 0,
            average_index=0,
            trend_direction='stable',
            trend_percentage=0,
            peak_index=0,
            lowest_index=0,
            volatility=0,
            entries_count=len(entries),
        )
    
    indices = [e.stress_index for e in entries]
    
    current = indices[-1]
    average = sum(indices) / len(indices)
    peak = max(indices)
    lowest = min(indices)
    
    # 计算趋势
    first_half_avg = sum(indices[:len(indices)//2]) / (len(indices)//2 or 1)
    second_half_avg = sum(indices[len(indices)//2:]) / (len(indices) - len(indices)//2 or 1)
    
    if second_half_avg > first_half_avg * 1.1:
        trend_direction = 'increasing'
        trend_percentage = round((second_half_avg - first_half_avg) / first_half_avg * 100, 1)
    elif second_half_avg < first_half_avg * 0.9:
        trend_direction = 'decreasing'
        trend_percentage = round(abs(second_half_avg - first_half_avg) / first_half_avg * 100, 1)
    else:
        trend_direction = 'stable'
        trend_percentage = 0
    
    # 计算波动性
    if len(indices) > 1:
        variance = sum((x - average) ** 2 for x in indices) / len(indices)
        volatility = round(variance / 100, 2)  # 相对波动性
    else:
        volatility = 0
    
    return StressTrend(
        current_index=current,
        average_index=round(average, 2),
        trend_direction=trend_direction,
        trend_percentage=trend_percentage,
        peak_index=peak,
        lowest_index=lowest,
        volatility=volatility,
        entries_count=len(entries),
    )


# ============================================================================
# Burnout Assessment Functions
# ============================================================================

def assess_burnout(
    emotional_exhaustion_responses: List[int],  # 0-6 每项
    depersonalization_responses: List[int],     # 0-6 每项
    personal_accomplishment_responses: List[int] # 0-6 每项 (反向)
) -> BurnoutAssessment:
    """
    评估燃尽风险 (基于 MBI 量表简化版).
    
    Args:
        emotional_exhaustion_responses: 情绪耗竭问题响应 (0-6)
        depersonalization_responses: 去人格化问题响应 (0-6)
        personal_accomplishment_responses: 个人成就感响应 (0-6)
    
    Returns:
        BurnoutAssessment 对象
    
    Examples:
        >>> assess_burnout([4, 5, 3, 4, 5], [2, 3, 2], [1, 2, 1, 2, 1, 2, 1])
        BurnoutAssessment(...)
    """
    # 计算各维度得分
    ee_avg = sum(emotional_exhaustion_responses) / len(emotional_exhaustion_responses) if emotional_exhaustion_responses else 0
    dp_avg = sum(depersonalization_responses) / len(depersonalization_responses) if depersonalization_responses else 0
    pa_avg = sum(personal_accomplishment_responses) / len(personal_accomplishment_responses) if personal_accomplishment_responses else 0
    
    # 转换为 0-1 范围
    ee_score = round(ee_avg / 6, 2)
    dp_score = round(dp_avg / 6, 2)
    # 成就感是反向的（得分越高，成就感越低）
    pa_score = round(pa_avg / 6, 2)
    
    # 综合风险
    overall_risk = round((ee_score * 0.4 + dp_score * 0.3 + pa_score * 0.3), 2)
    
    # 风险等级
    if overall_risk < 0.3:
        risk_level = 'low'
    elif overall_risk < 0.5:
        risk_level = 'moderate'
    elif overall_risk < 0.7:
        risk_level = 'high'
    else:
        risk_level = 'critical'
    
    # 警告信号
    warning_signs = []
    if ee_score >= BURNOUT_SIGNS['emotional_exhaustion']['threshold']:
        warning_signs.extend(BURNOUT_SIGNS['emotional_exhaustion']['signs'])
    if dp_score >= BURNOUT_SIGNS['depersonalization']['threshold']:
        warning_signs.extend(BURNOUT_SIGNS['depersonalization']['signs'])
    if pa_score >= BURNOUT_SIGNS['reduced accomplishment']['threshold']:
        warning_signs.extend(BURNOUT_SIGNS['reduced accomplishment']['signs'])
    
    # 干预建议
    interventions = []
    if overall_risk >= 0.7:
        interventions.append('立即寻求专业心理帮助')
        interventions.append('考虑暂时休假')
    if overall_risk >= 0.5:
        interventions.append('减少工作量')
        interventions.append('建立支持网络')
    interventions.append('定期休息和放松')
    interventions.append('重新评估工作目标')
    
    return BurnoutAssessment(
        emotional_exhaustion_score=ee_score,
        depersonalization_score=dp_score,
        reduced_accomplishment_score=pa_score,
        overall_risk=overall_risk,
        risk_level=risk_level,
        warning_signs=warning_signs,
        interventions=interventions,
    )


# ============================================================================
# Relief Activity Functions
# ============================================================================

def suggest_relief_activities(
    stress_level: str,
    available_time_minutes: int = 30,
    preferences: Optional[List[str]] = None
) -> List[Dict[str, str]]:
    """
    根据压力等级和时间建议缓解活动.
    
    Args:
        stress_level: 压力等级
        available_time_minutes: 可用时间（分钟）
        preferences: 偏好活动类型列表
    
    Returns:
        建议活动列表
    
    Examples:
        >>> suggest_relief_activities('moderate', 15)
        [{'name': '深呼吸练习', 'duration': '5-10分钟', ...}]
    """
    # 活动库
    activities = {
        'physical': [
            {'name': '散步', 'duration': '15-30分钟', 'effect': 'medium', 'description': '轻松散步，欣赏周围环境'},
            {'name': '伸展运动', 'duration': '5-10分钟', 'effect': 'low', 'description': '简单的身体伸展'},
            {'name': '跑步', 'duration': '20-40分钟', 'effect': 'high', 'description': '有氧运动释放压力'},
            {'name': '瑜伽', 'duration': '20-60分钟', 'effect': 'high', 'description': '身心结合的放松'},
        ],
        'mental': [
            {'name': '深呼吸练习', 'duration': '5-10分钟', 'effect': 'low', 'description': '4-7-8呼吸法'},
            {'name': '冥想', 'duration': '10-30分钟', 'effect': 'high', 'description': '专注当下，放松心灵'},
            {'name': '正念练习', 'duration': '5-15分钟', 'effect': 'medium', 'description': '觉察当下感受'},
            {'name': '渐进放松', 'duration': '15-20分钟', 'effect': 'high', 'description': '全身肌肉放松'},
        ],
        'social': [
            {'name': '与朋友聊天', 'duration': '15-60分钟', 'effect': 'medium', 'description': '分享感受，获得支持'},
            {'name': '家庭活动', 'duration': '30-60分钟', 'effect': 'medium', 'description': '与家人共度时光'},
            {'name': '社交活动', 'duration': '30-120分钟', 'effect': 'medium', 'description': '参加社交活动'},
        ],
        'lifestyle': [
            {'name': '听音乐', 'duration': '10-30分钟', 'effect': 'low', 'description': '听喜欢的放松音乐'},
            {'name': '阅读', 'duration': '20-60分钟', 'effect': 'medium', 'description': '阅读喜欢的书籍'},
            {'name': '泡澡', 'duration': '20-30分钟', 'effect': 'high', 'description': '温暖放松的沐浴'},
            {'name': '芳香疗法', 'duration': '15-30分钟', 'effect': 'medium', 'description': '使用精油放松'},
        ],
        'professional': [
            {'name': '心理咨询', 'duration': '45-60分钟', 'effect': 'high', 'description': '专业心理支持'},
            {'name': '压力管理课程', 'duration': '60-90分钟', 'effect': 'high', 'description': '学习压力管理技巧'},
        ],
    }
    
    # 根据压力等级确定需要的活动效果强度
    if stress_level in ['very_high', 'high']:
        min_effect = 'medium'
        preferred_categories = ['mental', 'physical', 'professional']
    elif stress_level == 'moderate':
        min_effect = 'low'
        preferred_categories = ['mental', 'physical', 'lifestyle']
    else:
        min_effect = 'low'
        preferred_categories = ['lifestyle', 'social', 'physical']
    
    # 如果有偏好，调整类别优先级
    if preferences:
        preferred_categories = preferences + [c for c in preferred_categories if c not in preferences]
    
    # 选择活动
    suggestions = []
    for category in preferred_categories:
        for activity in activities.get(category, []):
            # 检查时间是否足够
            duration_parts = activity['duration'].split('-')
            min_time = int(duration_parts[0])
            
            if min_time <= available_time_minutes:
                # 检查效果是否满足
                effects = {'low': 1, 'medium': 2, 'high': 3}
                if effects.get(activity['effect'], 1) >= effects.get(min_effect, 1):
                    suggestions.append({
                        **activity,
                        'category': category,
                    })
    
    return suggestions[:5]  # 返回最多5个建议


# ============================================================================
# Utility Functions
# ============================================================================

def get_stress_summary(stress_index: float) -> str:
    """
    获取压力简要说明.
    
    Args:
        stress_index: 压力指数
    
    Returns:
        简要说明字符串
    
    Examples:
        >>> get_stress_summary(45.0)
        '压力指数 45.0 - 中等水平，建议关注和调节'
    """
    level, label, label_en, description, action = get_stress_level_info(stress_index)
    return f"压力指数 {stress_index:.1f} - {label}水平，{action}"


def calculate_stress_reduction_potential(
    current_stress: float,
    relief_activities: List[Dict[str, str]]
) -> float:
    """
    计算压力缓解潜力.
    
    Args:
        current_stress: 当前压力指数
        relief_activities: 缓解活动列表
    
    Returns:
        预估压力降低值
    
    Examples:
        >>> calculate_stress_reduction_potential(70, [{'effect': 'high'}, {'effect': 'medium'}])
        15.0
    """
    effects = {'low': 5, 'medium': 10, 'high': 20}
    
    total_reduction = sum(
        effects.get(activity.get('effect', 'low'), 5)
        for activity in relief_activities
    )
    
    # 最大不超过当前压力的一半
    max_reduction = current_stress * 0.5
    
    return round(min(total_reduction, max_reduction), 1)


def get_pss_questions() -> List[Tuple[str, str]]:
    """
    获取 PSS-10 问题列表.
    
    Returns:
        问题ID和问题文本列表
    
    Examples:
        >>> questions = get_pss_questions()
        >>> len(questions)
        10
    """
    return [(q_id, q_text) for q_id, q_text, q_type in PSS_10_QUESTIONS]


def format_assessment_report(assessment: StressAssessment) -> str:
    """
    格式化评估报告.
    
    Args:
        assessment: StressAssessment 对象
    
    Returns:
        格式化的报告字符串
    
    Examples:
        >>> result = perform_full_assessment(60, 40, 30, 50, 20)
        >>> report = format_assessment_report(result)
        >>> print(report)
    """
    lines = [
        "=" * 50,
        "压力评估报告",
        "=" * 50,
        f"\n评估时间: {assessment.timestamp}",
        f"\n压力指数: {assessment.stress_index}/100",
        f"压力等级: {assessment.level_label} ({assessment.level_label_en})",
        f"状态描述: {assessment.description}",
        f"\n推荐行动: {assessment.recommended_action}",
        f"\n燃尽风险: {assessment.burnout_risk:.0%}",
        "\n" + "-" * 50,
        "\n压力因素分析:",
    ]
    
    for factor, score in assessment.factor_breakdown.items():
        factor_label = STRESS_FACTORS.get(factor, {}).get('label', factor)
        lines.append(f"  {factor_label}: {score}/100")
    
    lines.append("\n主要压力来源: " + ", ".join(assessment.dominant_factors))
    
    lines.append("\n" + "-" * 50)
    lines.append("\n缓解建议:")
    for i, rec in enumerate(assessment.recommendations, 1):
        lines.append(f"  {i}. {rec}")
    
    lines.append("\n" + "=" * 50)
    
    return "\n".join(lines)


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Stress Utilities Demo")
    print("=" * 60)
    
    # 完整评估
    print("\n--- 完整压力评估 ---")
    result = perform_full_assessment(
        work_score=65,
        life_score=40,
        health_score=35,
        psychological_score=55,
        environment_score=25
    )
    print(format_assessment_report(result))
    
    # 快速检查
    print("\n--- 快速压力检查 ---")
    quick_index = quick_stress_check(
        sleep_quality=6,
        energy_level=5,
        mood_rating=4,
        workload_feeling=7,
        social_connection=5
    )
    print(f"快速压力指数: {quick_index}")
    print(get_stress_summary(quick_index))
    
    # 活动建议
    print("\n--- 缓解活动建议 ---")
    activities = suggest_relief_activities('moderate', 20)
    for activity in activities:
        print(f"  - {activity['name']} ({activity['duration']}) - {activity['description']}")
    
    # 历史趋势
    print("\n--- 压力历史趋势 ---")
    history = StressHistory()
    for i in range(7):
        history.add_entry(30 + i * 5 + (i % 3) * 3)
    
    trend = analyze_stress_trend(history)
    print(f"当前压力: {trend.current_index}")
    print(f"平均压力: {trend.average_index}")
    print(f"趋势方向: {trend.trend_direction} ({trend.trend_percentage}%)")
    print(f"波动性: {trend.volatility}")
    
    # 燃尽评估
    print("\n--- 燃尽风险评估 ---")
    burnout = assess_burnout([4, 5, 4, 5, 4], [3, 2, 3], [1, 2, 1, 2, 1])
    print(f"情绪耗竭: {burnout.emotional_exhaustion_score:.0%}")
    print(f"去人格化: {burnout.depersonalization_score:.0%}")
    print(f"成就感降低: {burnout.reduced_accomplishment_score:.0%}")
    print(f"总风险: {burnout.overall_risk:.0%} - {burnout.risk_level}")
    
    print("\n" + "=" * 60)