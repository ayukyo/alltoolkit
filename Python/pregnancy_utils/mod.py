#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Pregnancy Utilities Module
========================================
A comprehensive pregnancy and due date calculation utility module for Python with zero external dependencies.

Features:
    - Due date calculation (Naegele's rule, conception date, IVF)
    - Gestational age calculation
    - Trimester determination
    - Pregnancy milestones tracking
    - Fetal development information
    - Prenatal checkup schedule
    - Pregnancy progress tracking
    - Key dates and reminders

Author: AllToolkit Contributors
License: MIT
Date: 2026-05-29
"""

from typing import Union, Tuple, Optional, List, Dict
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta, date


# ============================================================================
# Constants
# ============================================================================

# Average pregnancy length (280 days from LMP)
PREGNANCY_DAYS = 280

# Average pregnancy length in weeks
PREGNANCY_WEEKS = 40

# Trimester boundaries (in weeks)
TRIMESTER_BOUNDARIES = {
    'first': (0, 13),      # Week 1-12 (0-13 weeks inclusive of start)
    'second': (13, 27),    # Week 13-26
    'third': (27, 40),     # Week 27-40+
}

# Key pregnancy milestones (in weeks)
PREGNANCY_MILESTONES = {
    4: {'name': '着床期', 'name_en': 'Implantation', 'desc': '受精卵着床，hCG开始分泌'},
    6: {'name': '胎心初现', 'name_en': 'Heartbeat Detected', 'desc': '可检测到胎心搏动'},
    8: {'name': '胚胎期结束', 'name_en': 'Embryonic Period Ends', 'desc': '主要器官开始形成'},
    10: {'name': '胎儿期开始', 'name_en': 'Fetal Period Begins', 'desc': '器官继续发育'},
    12: {'name': '早孕期结束', 'name_en': 'First Trimester Ends', 'desc': '流产风险大幅降低'},
    16: {'name': '胎动感', 'name_en': 'Quickening', 'desc': '可能开始感受胎动'},
    20: {'name': '大排畸', 'name_en': 'Anatomy Scan', 'desc': '详细超声波检查'},
    24: {'name': '存活期', 'name_en': 'Viability', 'desc': '胎儿可能存活（有医疗支持）'},
    28: {'name': '晚孕期开始', 'name_en': 'Third Trimester Begins', 'desc': '快速生长期'},
    32: {'name': '肺部发育', 'name_en': 'Lung Development', 'desc': '肺部接近成熟'},
    36: {'name': '近足月', 'name_en': 'Late Preterm', 'desc': '如果出生通常健康'},
    37: {'name': '足月', 'name_en': 'Full Term', 'desc': '被认为是足月妊娠'},
    40: {'name': '预产期', 'name_en': 'Due Date', 'desc': '预期分娩日期'},
    42: {'name': '过期妊娠', 'name_en': 'Post Term', 'desc': '超过预产期，需要监测'},
}

# Fetal development milestones (approximate size)
FETAL_SIZES = {
    4: {'length_cm': 0.1, 'weight_g': 0, 'size_ref': '罂粟籽', 'size_ref_en': 'Poppy seed'},
    8: {'length_cm': 1.6, 'weight_g': 1, 'size_ref': '覆盆子', 'size_ref_en': 'Raspberry'},
    12: {'length_cm': 5.4, 'weight_g': 14, 'size_ref': '酸橙', 'size_ref_en': 'Lime'},
    16: {'length_cm': 11.6, 'weight_g': 100, 'size_ref': '鳄梨', 'size_ref_en': 'Avocado'},
    20: {'length_cm': 16.4, 'weight_g': 300, 'size_ref': '香蕉', 'size_ref_en': 'Banana'},
    24: {'length_cm': 21.2, 'weight_g': 600, 'size_ref': '玉米棒', 'size_ref_en': 'Corn cob'},
    28: {'length_cm': 25.5, 'weight_g': 1000, 'size_ref': '茄子', 'size_ref_en': 'Eggplant'},
    32: {'length_cm': 29.2, 'weight_g': 1700, 'size_ref': '南瓜', 'size_ref_en': 'Squash'},
    36: {'length_cm': 32.6, 'weight_g': 2600, 'size_ref': '生菜', 'size_ref_en': 'Romaine lettuce'},
    40: {'length_cm': 35.5, 'weight_g': 3400, 'size_ref': '小西瓜', 'size_ref_en': 'Small watermelon'},
}

# Prenatal checkup schedule
PRENATAL_SCHEDULE = [
    {'week': 8, 'name': '首次产检', 'name_en': 'First Prenatal Visit', 'items': ['确认妊娠', '基础体检', '血常规', '血型', '尿常规', 'B超']},
    {'week': 12, 'name': 'NT检查', 'name_en': 'NT Scan', 'items': ['颈项透明层测量', '早唐筛查']},
    {'week': 16, 'name': '中唐筛查', 'name_en': 'Quad Screen', 'items': ['唐氏综合征筛查', '血常规']},
    {'week': 20, 'name': '大排畸', 'name_en': 'Anatomy Scan', 'items': ['详细B超', '胎儿发育评估']},
    {'week': 24, 'name': '糖耐量测试', 'name_en': 'Glucose Tolerance Test', 'items': ['妊娠糖尿病筛查']},
    {'week': 28, 'name': '晚孕期开始', 'name_en': 'Third Trimester Start', 'items': ['产检', '血常规', '尿常规']},
    {'week': 30, 'name': '定期产检', 'name_en': 'Regular Checkup', 'items': ['产检', '胎心监护']},
    {'week': 32, 'name': '定期产检', 'name_en': 'Regular Checkup', 'items': ['产检', 'B超', '胎位检查']},
    {'week': 34, 'name': '定期产检', 'name_en': 'Regular Checkup', 'items': ['产检', '胎心监护']},
    {'week': 36, 'name': '每周产检', 'name_en': 'Weekly Checkup', 'items': ['产检', '胎心监护', 'B超']},
    {'week': 37, 'name': '足月评估', 'name_en': 'Full Term Assessment', 'items': ['产检', '胎心监护', '骨盆测量']},
    {'week': 38, 'name': '每周产检', 'name_en': 'Weekly Checkup', 'items': ['产检', '胎心监护']},
    {'week': 39, 'name': '每周产检', 'name_en': 'Weekly Checkup', 'items': ['产检', '胎心监护', '分娩准备']},
    {'week': 40, 'name': '预产期', 'name_en': 'Due Date', 'items': ['产检', '胎心监护', '过期监测']},
    {'week': 41, 'name': '过期监测', 'name_en': 'Post Term Monitoring', 'items': ['胎心监护', '羊水检查', '考虑引产']},
]


# ============================================================================
# Enums
# ============================================================================

class Trimester(Enum):
    """孕期三孕期枚举"""
    FIRST = 'first'
    SECOND = 'second'
    THIRD = 'third'


class PregnancyStatus(Enum):
    """妊娠状态枚举"""
    EARLY = 'early'           # 早孕 (<12周)
    NORMAL = 'normal'         # 正常妊娠
    FULL_TERM = 'full_term'   # 足月 (≥37周)
    POST_TERM = 'post_term'   # 过期 (≥42周)


class CalculationMethod(Enum):
    """计算方法枚举"""
    LMP = 'lmp'               # 末次月经日期
    CONCEPTION = 'conception'  # 受孕日期
    IVF = 'ivf'               # IVF移植日期
    ULTRASOUND = 'ultrasound'  # B超测量


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class DueDateResult:
    """预产期计算结果"""
    due_date: date
    conception_date: Optional[date]
    lmp_date: Optional[date]
    current_week: int
    current_day: int
    days_remaining: int
    trimester: str
    trimester_label: str
    status: str
    status_label: str
    progress_percent: float


@dataclass
class PregnancyMilestone:
    """孕期里程碑"""
    week: int
    name: str
    name_en: str
    description: str
    date: Optional[date]
    is_passed: bool
    days_until: Optional[int]


@dataclass
class FetalDevelopment:
    """胎儿发育信息"""
    week: int
    length_cm: float
    weight_g: float
    size_reference: str
    size_reference_en: str
    developments: List[str]


@dataclass
class CheckupSchedule:
    """产检安排"""
    week: int
    name: str
    name_en: str
    items: List[str]
    date: Optional[date]
    is_past: bool
    is_upcoming: bool


# ============================================================================
# Core Calculation Functions
# ============================================================================

def calculate_due_date_from_lmp(lmp_date: Union[date, datetime, str]) -> date:
    """
    使用 Naegele 规则从末次月经日期计算预产期.
    
    Naegele 规则：末次月经日期 + 1年 - 3个月 + 7天
    
    Args:
        lmp_date: 末次月经第一天的日期 (date, datetime 或 'YYYY-MM-DD' 格式字符串)
    
    Returns:
        预产期日期
    
    Raises:
        ValueError: 如果日期格式无效
    
    Examples:
        >>> calculate_due_date_from_lmp('2024-01-01')
        datetime.date(2024, 10, 8)
        >>> calculate_due_date_from_lmp(date(2024, 1, 15))
        datetime.date(2024, 10, 22)
    """
    lmp = _parse_date(lmp_date)
    
    # Naegele's rule: LMP + 1 year - 3 months + 7 days
    due_date = lmp + timedelta(days=280)
    
    return due_date


def calculate_due_date_from_conception(conception_date: Union[date, datetime, str]) -> date:
    """
    从受孕日期计算预产期.
    
    受孕日期 + 266天 (38周) = 预产期
    
    Args:
        conception_date: 受孕日期
    
    Returns:
        预产期日期
    
    Examples:
        >>> calculate_due_date_from_conception('2024-01-15')
        datetime.date(2024, 10, 8)
    """
    conception = _parse_date(conception_date)
    
    # Conception date + 266 days (38 weeks)
    due_date = conception + timedelta(days=266)
    
    return due_date


def calculate_due_date_from_ivf(
    transfer_date: Union[date, datetime, str],
    embryo_age_days: int = 3
) -> date:
    """
    从 IVF 移植日期计算预产期.
    
    Args:
        transfer_date: 胚胎移植日期
        embryo_age_days: 胚胎天数 (通常为 3 天或 5 天囊胚)
    
    Returns:
        预产期日期
    
    Examples:
        >>> calculate_due_date_from_ivf('2024-01-20', 3)  # 3天胚胎
        datetime.date(2024, 10, 7)
        >>> calculate_due_date_from_ivf('2024-01-22', 5)  # 5天囊胚
        datetime.date(2024, 10, 7)
    """
    transfer = _parse_date(transfer_date)
    
    # IVF due date: Transfer date + (280 - embryo_age_days - 14) days
    # For day 3 embryo: +263 days
    # For day 5 blastocyst: +261 days
    days_to_add = 280 - embryo_age_days - 14
    due_date = transfer + timedelta(days=days_to_add)
    
    return due_date


def calculate_gestational_age(
    reference_date: Union[date, datetime, str],
    current_date: Optional[Union[date, datetime, str]] = None,
    method: CalculationMethod = CalculationMethod.LMP
) -> Tuple[int, int]:
    """
    计算孕周和孕天.
    
    Args:
        reference_date: 参考日期 (LMP 或受孕日期)
        current_date: 当前日期，默认为今天
        method: 计算方法 (LMP 或 CONCEPTION)
    
    Returns:
        (孕周, 孕天) 元组
    
    Examples:
        >>> calculate_gestational_age('2024-01-01', '2024-03-01')
        (8, 6)  # 8周6天
    """
    ref_date = _parse_date(reference_date)
    curr_date = _parse_date(current_date) if current_date else date.today()
    
    # Calculate days since reference
    delta = curr_date - ref_date
    total_days = delta.days
    
    # Adjust based on method
    if method == CalculationMethod.CONCEPTION:
        total_days += 14  # Add 14 days to convert from conception to LMP
    
    # Calculate weeks and days
    weeks = total_days // 7
    days = total_days % 7
    
    return weeks, days


def get_trimester(weeks: int) -> Tuple[Trimester, str]:
    """
    根据孕周获取孕期.
    
    Args:
        weeks: 孕周数
    
    Returns:
        (Trimester 枚举, 中文标签) 元组
    
    Examples:
        >>> get_trimester(8)
        (<Trimester.FIRST: 'first'>, '第一孕期')
        >>> get_trimester(20)
        (<Trimester.SECOND: 'second'>, '第二孕期')
    """
    if weeks < 13:
        return Trimester.FIRST, '第一孕期 (1-12周)'
    elif weeks < 27:
        return Trimester.SECOND, '第二孕期 (13-26周)'
    else:
        return Trimester.THIRD, '第三孕期 (27-40+周)'


def get_pregnancy_status(weeks: int) -> Tuple[PregnancyStatus, str]:
    """
    获取妊娠状态.
    
    Args:
        weeks: 孕周数
    
    Returns:
        (PregnancyStatus 枚举, 中文描述) 元组
    
    Examples:
        >>> get_pregnancy_status(10)
        (<PregnancyStatus.EARLY: 'early'>, '早孕期')
        >>> get_pregnancy_status(38)
        (<PregnancyStatus.FULL_TERM: 'full_term'>, '足月妊娠')
    """
    if weeks < 12:
        return PregnancyStatus.EARLY, '早孕期'
    elif weeks < 37:
        return PregnancyStatus.NORMAL, '正常妊娠'
    elif weeks < 42:
        return PregnancyStatus.FULL_TERM, '足月妊娠'
    else:
        return PregnancyStatus.POST_TERM, '过期妊娠'


def calculate_progress_percentage(weeks: int, days: int = 0) -> float:
    """
    计算孕期进度百分比.
    
    Args:
        weeks: 孕周数
        days: 额外天数
    
    Returns:
        进度百分比 (0-100)
    
    Examples:
        >>> calculate_progress_percentage(20)
        50.0
        >>> calculate_progress_percentage(40)
        100.0
    """
    total_days = weeks * 7 + days
    max_days = PREGNANCY_DAYS
    
    percentage = (total_days / max_days) * 100
    return round(min(percentage, 100), 1)


# ============================================================================
# Full Calculation Functions
# ============================================================================

def calculate_full_pregnancy(
    lmp_date: Union[date, datetime, str],
    current_date: Optional[Union[date, datetime, str]] = None
) -> DueDateResult:
    """
    完整的孕期计算.
    
    Args:
        lmp_date: 末次月经日期
        current_date: 当前日期，默认为今天
    
    Returns:
        DueDateResult 对象，包含完整信息
    
    Examples:
        >>> result = calculate_full_pregnancy('2024-01-01')
        >>> result.due_date
        datetime.date(2024, 10, 8)
    """
    lmp = _parse_date(lmp_date)
    curr_date = _parse_date(current_date) if current_date else date.today()
    
    # Calculate due date
    due_date = calculate_due_date_from_lmp(lmp)
    
    # Calculate conception date (approximately 14 days after LMP)
    conception_date = lmp + timedelta(days=14)
    
    # Calculate current gestational age
    weeks, days = calculate_gestational_age(lmp, curr_date)
    
    # Calculate days remaining
    days_remaining = (due_date - curr_date).days
    
    # Get trimester
    trimester, trimester_label = get_trimester(weeks)
    
    # Get status
    status, status_label = get_pregnancy_status(weeks)
    
    # Calculate progress
    progress = calculate_progress_percentage(weeks, days)
    
    return DueDateResult(
        due_date=due_date,
        conception_date=conception_date,
        lmp_date=lmp,
        current_week=weeks,
        current_day=days,
        days_remaining=max(0, days_remaining),
        trimester=trimester.value,
        trimester_label=trimester_label,
        status=status.value,
        status_label=status_label,
        progress_percent=progress
    )


def get_milestones(
    lmp_date: Union[date, datetime, str],
    current_date: Optional[Union[date, datetime, str]] = None
) -> List[PregnancyMilestone]:
    """
    获取孕期里程碑列表.
    
    Args:
        lmp_date: 末次月经日期
        current_date: 当前日期
    
    Returns:
        PregnancyMilestone 对象列表
    
    Examples:
        >>> milestones = get_milestones('2024-01-01')
        >>> milestones[0].name
        '着床期'
    """
    lmp = _parse_date(lmp_date)
    curr_date = _parse_date(current_date) if current_date else date.today()
    
    milestones = []
    
    for week, info in PREGNANCY_MILESTONES.items():
        milestone_date = lmp + timedelta(weeks=week)
        is_passed = curr_date >= milestone_date
        days_until = (milestone_date - curr_date).days if not is_passed else None
        
        milestones.append(PregnancyMilestone(
            week=week,
            name=info['name'],
            name_en=info['name_en'],
            description=info['desc'],
            date=milestone_date,
            is_passed=is_passed,
            days_until=days_until
        ))
    
    return milestones


def get_next_milestone(
    lmp_date: Union[date, datetime, str],
    current_date: Optional[Union[date, datetime, str]] = None
) -> Optional[PregnancyMilestone]:
    """
    获取下一个里程碑.
    
    Args:
        lmp_date: 末次月经日期
        current_date: 当前日期
    
    Returns:
        下一个 PregnancyMilestone，如果已过所有里程碑则返回 None
    
    Examples:
        >>> milestone = get_next_milestone('2024-01-01', '2024-03-01')
        >>> milestone.name
        '早孕期结束'
    """
    milestones = get_milestones(lmp_date, current_date)
    
    for milestone in milestones:
        if not milestone.is_passed:
            return milestone
    
    return None


def get_fetal_development(weeks: int) -> FetalDevelopment:
    """
    获取指定孕周的胎儿发育信息.
    
    Args:
        weeks: 孕周数
    
    Returns:
        FetalDevelopment 对象
    
    Examples:
        >>> dev = get_fetal_development(20)
        >>> dev.size_reference
        '香蕉'
    """
    # Find the closest size reference
    size_keys = sorted(FETAL_SIZES.keys())
    closest_week = max(k for k in size_keys if k <= weeks) if weeks >= min(size_keys) else min(size_keys)
    
    size_info = FETAL_SIZES[closest_week]
    
    # Get development milestones for the week
    developments = _get_developments_for_week(weeks)
    
    return FetalDevelopment(
        week=weeks,
        length_cm=size_info['length_cm'],
        weight_g=size_info['weight_g'],
        size_reference=size_info['size_ref'],
        size_reference_en=size_info['size_ref_en'],
        developments=developments
    )


def _get_developments_for_week(weeks: int) -> List[str]:
    """获取指定孕周的发育里程碑"""
    all_developments = {
        4: ['受精卵着床', '细胞开始分化'],
        6: ['心脏开始跳动', '神经管形成'],
        8: ['面部特征开始形成', '四肢可见'],
        10: ['主要器官已形成', '胎儿开始活动'],
        12: ['手指脚趾已分离', '肾脏开始工作'],
        14: ['可以吸吮拇指', '眉毛开始生长'],
        16: ['可能感受胎动', '骨骼开始硬化'],
        18: ['可以听到声音', '有睡眠周期'],
        20: ['有吞咽动作', '味蕾发育'],
        22: ['眼睛已形成', '有触觉反应'],
        24: ['肺部开始产生表面活性物质', '可能有存活能力'],
        26: ['眼睛可以睁开', '有呼吸运动'],
        28: ['可以眨眼', '有睫毛'],
        30: ['大脑快速发育', '可以调节体温'],
        32: ['皮下脂肪增加', '肺部接近成熟'],
        34: ['中枢神经系统发育', '免疫系统增强'],
        36: ['体重快速增加', '头部可能入盆'],
        38: ['器官功能完善', '准备分娩'],
        40: ['发育完成', '准备出生'],
    }
    
    developments = []
    for week, devs in sorted(all_developments.items()):
        if week <= weeks:
            developments = devs
    
    return developments


def get_checkup_schedule(
    lmp_date: Union[date, datetime, str],
    current_date: Optional[Union[date, datetime, str]] = None
) -> List[CheckupSchedule]:
    """
    获取产检时间表.
    
    Args:
        lmp_date: 末次月经日期
        current_date: 当前日期
    
    Returns:
        CheckupSchedule 对象列表
    
    Examples:
        >>> schedule = get_checkup_schedule('2024-01-01')
        >>> schedule[0].name
        '首次产检'
    """
    lmp = _parse_date(lmp_date)
    curr_date = _parse_date(current_date) if current_date else date.today()
    
    schedules = []
    
    for item in PRENATAL_SCHEDULE:
        week = item['week']
        checkup_date = lmp + timedelta(weeks=week)
        is_past = curr_date >= checkup_date
        is_upcoming = not is_past and (checkup_date - curr_date).days <= 14
        
        schedules.append(CheckupSchedule(
            week=week,
            name=item['name'],
            name_en=item['name_en'],
            items=item['items'],
            date=checkup_date,
            is_past=is_past,
            is_upcoming=is_upcoming
        ))
    
    return schedules


def get_upcoming_checkups(
    lmp_date: Union[date, datetime, str],
    current_date: Optional[Union[date, datetime, str]] = None,
    limit: int = 3
) -> List[CheckupSchedule]:
    """
    获取即将到来的产检.
    
    Args:
        lmp_date: 末次月经日期
        current_date: 当前日期
        limit: 返回数量限制
    
    Returns:
        CheckupSchedule 对象列表
    
    Examples:
        >>> checkups = get_upcoming_checkups('2024-01-01', '2024-03-01')
        >>> checkups[0].name
        '中唐筛查'
    """
    schedule = get_checkup_schedule(lmp_date, current_date)
    
    upcoming = [s for s in schedule if not s.is_past]
    
    return upcoming[:limit]


# ============================================================================
# Utility Functions
# ============================================================================

def _parse_date(date_input: Union[date, datetime, str]) -> date:
    """
    解析日期输入.
    
    Args:
        date_input: 日期对象或字符串
    
    Returns:
        date 对象
    
    Raises:
        ValueError: 如果日期格式无效
    """
    if isinstance(date_input, date):
        return date_input
    elif isinstance(date_input, datetime):
        return date_input.date()
    elif isinstance(date_input, str):
        # Try common formats
        formats = ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']
        for fmt in formats:
            try:
                return datetime.strptime(date_input, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"无法解析日期: {date_input}，请使用 YYYY-MM-DD 格式")
    else:
        raise ValueError(f"无效的日期类型: {type(date_input)}")


def format_gestational_age(weeks: int, days: int = 0) -> str:
    """
    格式化孕周显示.
    
    Args:
        weeks: 孕周数
        days: 额外天数
    
    Returns:
        格式化的字符串
    
    Examples:
        >>> format_gestational_age(20, 4)
        '20周+4天'
    """
    if days > 0:
        return f"{weeks}周+{days}天"
    else:
        return f"{weeks}周"


def get_pregnancy_summary(
    lmp_date: Union[date, datetime, str],
    current_date: Optional[Union[date, datetime, str]] = None
) -> Dict:
    """
    获取孕期摘要信息.
    
    Args:
        lmp_date: 末次月经日期
        current_date: 当前日期
    
    Returns:
        包含摘要信息的字典
    
    Examples:
        >>> summary = get_pregnancy_summary('2024-01-01', '2024-05-01')
        >>> summary['weeks']
        17
    """
    result = calculate_full_pregnancy(lmp_date, current_date)
    next_milestone = get_next_milestone(lmp_date, current_date)
    fetal = get_fetal_development(result.current_week)
    upcoming = get_upcoming_checkups(lmp_date, current_date, 1)
    
    return {
        'weeks': result.current_week,
        'days': result.current_day,
        'gestational_age': format_gestational_age(result.current_week, result.current_day),
        'due_date': result.due_date.strftime('%Y-%m-%d'),
        'days_remaining': result.days_remaining,
        'trimester': result.trimester_label,
        'status': result.status_label,
        'progress': f"{result.progress_percent}%",
        'next_milestone': next_milestone.name if next_milestone else None,
        'next_milestone_date': next_milestone.date.strftime('%Y-%m-%d') if next_milestone else None,
        'fetal_size': fetal.size_reference,
        'fetal_weight': f"{fetal.weight_g}g" if fetal.weight_g > 0 else '<1g',
        'upcoming_checkup': upcoming[0].name if upcoming else None,
        'upcoming_checkup_date': upcoming[0].date.strftime('%Y-%m-%d') if upcoming else None,
    }


def estimate_lmp_from_due_date(due_date: Union[date, datetime, str]) -> date:
    """
    从预产期估算末次月经日期.
    
    Args:
        due_date: 预产期
    
    Returns:
        估算的末次月经日期
    
    Examples:
        >>> estimate_lmp_from_due_date('2024-10-08')
        datetime.date(2024, 1, 1)
    """
    due = _parse_date(due_date)
    lmp = due - timedelta(days=280)
    return lmp


def estimate_conception_from_due_date(due_date: Union[date, datetime, str]) -> date:
    """
    从预产期估算受孕日期.
    
    Args:
        due_date: 预产期
    
    Returns:
        估算的受孕日期
    
    Examples:
        >>> estimate_conception_from_due_date('2024-10-08')
        datetime.date(2024, 1, 15)
    """
    due = _parse_date(due_date)
    conception = due - timedelta(days=266)
    return conception


def is_high_risk_pregnancy(
    age: Optional[int] = None,
    pre_existing_conditions: Optional[List[str]] = None,
    pregnancy_complications: Optional[List[str]] = None
) -> Tuple[bool, List[str]]:
    """
    判断是否为高危妊娠.
    
    Args:
        age: 孕妇年龄
        pre_existing_conditions: 既存疾病列表
        pregnancy_complications: 妊娠并发症列表
    
    Returns:
        (是否高危, 风险因素列表) 元组
    
    Examples:
        >>> is_high_risk_pregnancy(age=38)
        (True, ['年龄≥35岁'])
    """
    risk_factors = []
    
    # Age-related risks
    if age is not None:
        if age < 18:
            risk_factors.append('年龄<18岁')
        elif age >= 35:
            risk_factors.append('年龄≥35岁')
        if age >= 40:
            risk_factors.append('年龄≥40岁')
    
    # Pre-existing conditions
    high_risk_conditions = {
        '高血压': '慢性高血压',
        '糖尿病': '糖尿病',
        '心脏病': '心脏病',
        '肾病': '肾脏疾病',
        '哮喘': '哮喘',
        '甲状腺疾病': '甲状腺疾病',
        '自身免疫病': '自身免疫疾病',
        '癫痫': '癫痫',
        '抑郁症': '精神健康问题',
    }
    
    if pre_existing_conditions:
        for condition in pre_existing_conditions:
            if condition in high_risk_conditions:
                risk_factors.append(high_risk_conditions[condition])
    
    # Pregnancy complications
    high_risk_complications = {
        '妊娠高血压': '妊娠期高血压',
        '妊娠糖尿病': '妊娠期糖尿病',
        '前置胎盘': '前置胎盘',
        '胎盘早剥': '胎盘早剥',
        '羊水过多': '羊水过多',
        '羊水过少': '羊水过少',
        '多胎': '多胎妊娠',
        '宫内发育迟缓': '胎儿宫内发育迟缓',
        '先兆流产': '先兆流产史',
        '前置血管': '前置血管',
    }
    
    if pregnancy_complications:
        for complication in pregnancy_complications:
            if complication in high_risk_complications:
                risk_factors.append(high_risk_complications[complication])
    
    is_high_risk = len(risk_factors) > 0
    
    return is_high_risk, risk_factors


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Pregnancy Utilities Demo")
    print("=" * 60)
    
    # 使用示例日期
    lmp = '2024-01-01'
    today = '2024-05-15'
    
    # 完整孕期计算
    print("\n--- 孕期计算 ---")
    result = calculate_full_pregnancy(lmp, today)
    print(f"末次月经: {result.lmp_date}")
    print(f"预产期: {result.due_date}")
    print(f"受孕日期: {result.conception_date}")
    print(f"当前孕周: {format_gestational_age(result.current_week, result.current_day)}")
    print(f"剩余天数: {result.days_remaining} 天")
    print(f"孕期: {result.trimester_label}")
    print(f"状态: {result.status_label}")
    print(f"进度: {result.progress_percent}%")
    
    # 下一个里程碑
    print("\n--- 下一个里程碑 ---")
    next_milestone = get_next_milestone(lmp, today)
    if next_milestone:
        print(f"里程碑: {next_milestone.name} ({next_milestone.name_en})")
        print(f"日期: {next_milestone.date}")
        print(f"描述: {next_milestone.description}")
        print(f"还有 {next_milestone.days_until} 天")
    
    # 胎儿发育
    print("\n--- 胎儿发育 ---")
    fetal = get_fetal_development(result.current_week)
    print(f"大小参考: {fetal.size_reference} ({fetal.size_reference_en})")
    print(f"身长: {fetal.length_cm} cm")
    print(f"体重: {fetal.weight_g} g")
    print(f"发育特征: {', '.join(fetal.developments)}")
    
    # 即将到来的产检
    print("\n--- 即将到来的产检 ---")
    checkups = get_upcoming_checkups(lmp, today, 2)
    for checkup in checkups:
        print(f"第{checkup.week}周 - {checkup.name}: {checkup.date}")
        print(f"  检查项目: {', '.join(checkup.items)}")
    
    # 孕期摘要
    print("\n--- 孕期摘要 ---")
    summary = get_pregnancy_summary(lmp, today)
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # 高危妊娠评估
    print("\n--- 高危妊娠评估 ---")
    is_high_risk, factors = is_high_risk_pregnancy(age=36, pre_existing_conditions=['高血压'])
    print(f"高危妊娠: {'是' if is_high_risk else '否'}")
    if factors:
        print(f"风险因素: {', '.join(factors)}")
    
    # 从预产期推算
    print("\n--- 从预产期推算 ---")
    due = '2024-10-08'
    estimated_lmp = estimate_lmp_from_due_date(due)
    estimated_conception = estimate_conception_from_due_date(due)
    print(f"预产期: {due}")
    print(f"估算末次月经: {estimated_lmp}")
    print(f"估算受孕日期: {estimated_conception}")
    
    print("\n" + "=" * 60)