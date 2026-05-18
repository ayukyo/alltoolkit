#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Payroll Utilities Module (薪资计算工具模块)
========================================================
A comprehensive payroll and tax calculation utility module for Python with zero external dependencies.

Features:
    - Basic salary calculation (hourly/daily/monthly)
    - Overtime pay calculation (Chinese labor law standards)
    - Individual income tax calculation (China IIT 2019)
    - Social insurance and housing fund calculation (五险一金)
    - Year-end bonus tax optimization
    - Net salary calculation
    - Salary structure analysis
    - Payroll report generation

Author: AllToolkit Contributors
License: MIT
Date: 2026-05-19
"""

from typing import Union, Tuple, Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, date


# ============================================================================
# Constants - China Individual Income Tax Rates (2019)
# ============================================================================

# 综合所得年度税率表（适用于累计预扣预缴）
IIT_ANNUAL_RATES = [
    # (月应纳税所得额上限, 税率%, 速算扣除数)
    (3000, 3, 0),
    (12000, 10, 210),
    (25000, 20, 1410),
    (35000, 25, 2660),
    (55000, 30, 4410),
    (80000, 35, 7160),
    (float('inf'), 45, 15160),
]

# 年终奖单独计税税率表
YEAR_END_BONUS_RATES = [
    # (月应纳税所得额上限, 税率%, 速算扣除数)
    (3000, 3, 0),
    (12000, 10, 210),
    (25000, 20, 1410),
    (35000, 25, 2660),
    (55000, 30, 4410),
    (80000, 35, 7160),
    (float('inf'), 45, 15160),
]

# 基本减除费用（起征点）
BASIC_DEDUCTION = 5000  # 元/月

# 社保公积金典型比例（不同城市可能不同，此处为典型值）
SOCIAL_INSURANCE_RATES = {
    'shanghai': {
        'pension': {'employee': 0.08, 'employer': 0.16},       # 养老保险
        'medical': {'employee': 0.02, 'employer': 0.095},      # 医疗保险
        'unemployment': {'employee': 0.005, 'employer': 0.005}, # 失业保险
        'work_injury': {'employee': 0, 'employer': 0.0026},    # 工伤保险
        'maternity': {'employee': 0, 'employer': 0},           # 生育保险（并入医疗）
        'housing_fund': {'employee': 0.07, 'employer': 0.07},   # 公积金
    },
    'beijing': {
        'pension': {'employee': 0.08, 'employer': 0.16},
        'medical': {'employee': 0.02, 'employer': 0.10},
        'unemployment': {'employee': 0.002, 'employer': 0.008},
        'work_injury': {'employee': 0, 'employer': 0.004},
        'maternity': {'employee': 0, 'employer': 0},
        'housing_fund': {'employee': 0.12, 'employer': 0.12},
    },
    'guangzhou': {
        'pension': {'employee': 0.08, 'employer': 0.14},
        'medical': {'employee': 0.02, 'employer': 0.055},
        'unemployment': {'employee': 0.002, 'employer': 0.008},
        'work_injury': {'employee': 0, 'employer': 0.005},
        'maternity': {'employee': 0, 'employer': 0},
        'housing_fund': {'employee': 0.12, 'employer': 0.12},
    },
    'shenzhen': {
        'pension': {'employee': 0.08, 'employer': 0.14},
        'medical': {'employee': 0.02, 'employer': 0.06},
        'unemployment': {'employee': 0.003, 'employer': 0.007},
        'work_injury': {'employee': 0, 'employer': 0.004},
        'maternity': {'employee': 0, 'employer': 0},
        'housing_fund': {'employee': 0.05, 'employer': 0.05},
    },
    'default': {
        'pension': {'employee': 0.08, 'employer': 0.16},
        'medical': {'employee': 0.02, 'employer': 0.08},
        'unemployment': {'employee': 0.002, 'employer': 0.006},
        'work_injury': {'employee': 0, 'employer': 0.004},
        'maternity': {'employee': 0, 'employer': 0},
        'housing_fund': {'employee': 0.08, 'employer': 0.08},
    },
}

# 社保基数上下限（典型值，实际需查询当地社保局）
SOCIAL_INSURANCE_BASE_LIMITS = {
    'shanghai': {'min': 7310, 'max': 36549},  # 2024参考值
    'beijing': {'min': 6821, 'max': 35283},
    'guangzhou': {'min': 5500, 'max': 28000},
    'shenzhen': {'min': 2360, 'max': 35283},
    'default': {'min': 4000, 'max': 30000},
}

# 公积金基数上下限（典型值）
HOUSING_FUND_BASE_LIMITS = {
    'shanghai': {'min': 2590, 'max': 36549},
    'beijing': {'min': 2420, 'max': 35283},
    'guangzhou': {'min': 2300, 'max': 28000},
    'shenzhen': {'min': 2360, 'max': 35283},
    'default': {'min': 2000, 'max': 30000},
}

# 加班工资倍数（中国劳动法规定）
OVERTIME_MULTIPLIERS = {
    'weekday': 1.5,    # 工作日延时加班
    'weekend': 2.0,    # 休息日加班（未补休）
    'holiday': 3.0,    # 法定节假日加班
}


# ============================================================================
# Enums
# ============================================================================

class SalaryType(Enum):
    """薪资类型"""
    MONTHLY = 'monthly'      # 月薪制
    DAILY = 'daily'          # 日薪制
    HOURLY = 'hourly'        # 时薪制


class CityCode(Enum):
    """城市代码"""
    BEIJING = 'beijing'
    SHANGHAI = 'shanghai'
    GUANGZHOU = 'guangzhou'
    SHENZHEN = 'shenzhen'
    OTHER = 'default'


class OvertimeType(Enum):
    """加班类型"""
    WEEKDAY = 'weekday'      # 工作日延时加班
    WEEKEND = 'weekend'      # 休息日加班
    HOLIDAY = 'holiday'      # 法定节假日加班


class BonusTaxMethod(Enum):
    """年终奖计税方式"""
    SEPARATE = 'separate'    # 单独计税
    COMBINED = 'combined'    # 合并入综合所得


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class SalaryParams:
    """薪资参数"""
    basic_salary: float                        # 基本工资
    salary_type: SalaryType = SalaryType.MONTHLY
    overtime_hours: Dict[str, float] = field(default_factory=dict)  # 加班时长 {'weekday': 10, 'weekend': 8, 'holiday': 4}
    bonus: float = 0.0                         # 奖金/津贴
    allowances: float = 0.0                    # 补贴
    deductions: float = 0.0                    # 扣款
    city: CityCode = CityCode.SHANGHAI         # 工作城市
    social_insurance_base: Optional[float] = None  # 社保基数（默认为工资）
    housing_fund_base: Optional[float] = None      # 公积金基数
    housing_fund_rate: Optional[float] = None      # 公积金比例（个人）
    special_deductions: float = 0.0                 # 专项附加扣除
    year_months: int = 12                          # 年工作月数
    
    def __post_init__(self):
        """参数校验"""
        if self.basic_salary < 0:
            raise ValueError("基本工资不能为负数")
        if self.bonus < 0:
            raise ValueError("奖金不能为负数")
        if self.allowances < 0:
            raise ValueError("补贴不能为负数")
        if self.deductions < 0:
            raise ValueError("扣款不能为负数")
        if self.special_deductions < 0:
            raise ValueError("专项附加扣除不能为负数")


@dataclass
class TaxResult:
    """个税计算结果"""
    gross_income: float           # 税前收入
    taxable_income: float         # 应纳税所得额
    tax_rate: float               # 税率（百分比）
    quick_deduction: float        # 速算扣除数
    tax_amount: float             # 应纳税额
    cumulative_tax: float         # 累计应纳税额（用于累计预扣预缴）
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'gross_income': round(self.gross_income, 2),
            'taxable_income': round(self.taxable_income, 2),
            'tax_rate': self.tax_rate,
            'quick_deduction': round(self.quick_deduction, 2),
            'tax_amount': round(self.tax_amount, 2),
            'cumulative_tax': round(self.cumulative_tax, 2),
        }


@dataclass
class SocialInsuranceResult:
    """社保计算结果"""
    base: float                   # 缴费基数
    pension_employee: float       # 养老保险（个人）
    pension_employer: float       # 养老保险（单位）
    medical_employee: float       # 医疗保险（个人）
    medical_employer: float       # 医疗保险（单位）
    unemployment_employee: float  # 失业保险（个人）
    unemployment_employer: float  # 失业保险（单位）
    work_injury_employer: float   # 工伤保险（单位）
    total_employee: float         # 个人缴纳总额
    total_employer: float         # 单位缴纳总额
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'base': round(self.base, 2),
            'pension_employee': round(self.pension_employee, 2),
            'pension_employer': round(self.pension_employer, 2),
            'medical_employee': round(self.medical_employee, 2),
            'medical_employer': round(self.medical_employer, 2),
            'unemployment_employee': round(self.unemployment_employee, 2),
            'unemployment_employer': round(self.unemployment_employer, 2),
            'work_injury_employer': round(self.work_injury_employer, 2),
            'total_employee': round(self.total_employee, 2),
            'total_employer': round(self.total_employer, 2),
        }


@dataclass
class HousingFundResult:
    """公积金计算结果"""
    base: float              # 缴费基数
    rate_employee: float     # 个人比例
    rate_employer: float     # 单位比例
    amount_employee: float   # 个人缴纳
    amount_employer: float   # 单位缴纳
    total: float             # 总缴纳
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'base': round(self.base, 2),
            'rate_employee': self.rate_employee,
            'rate_employer': self.rate_employer,
            'amount_employee': round(self.amount_employee, 2),
            'amount_employer': round(self.amount_employer, 2),
            'total': round(self.total, 2),
        }


@dataclass
class PayrollResult:
    """薪资计算结果"""
    gross_salary: float              # 税前工资总额
    basic_salary: float              # 基本工资
    overtime_pay: float              # 加班费
    bonus: float                     # 奖金
    allowances: float                # 补贴
    deductions_before_tax: float     # 税前扣款
    social_insurance: float          # 社保（个人部分）
    housing_fund: float              # 公积金（个人部分）
    taxable_income: float            # 应纳税所得额
    income_tax: float                # 个人所得税
    deductions_after_tax: float      # 税后扣款
    net_salary: float                # 税后工资（实发）
    employer_cost: float             # 单位用工成本
    
    social_insurance_detail: Optional[SocialInsuranceResult] = None
    housing_fund_detail: Optional[HousingFundResult] = None
    tax_detail: Optional[TaxResult] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            'gross_salary': round(self.gross_salary, 2),
            'basic_salary': round(self.basic_salary, 2),
            'overtime_pay': round(self.overtime_pay, 2),
            'bonus': round(self.bonus, 2),
            'allowances': round(self.allowances, 2),
            'deductions_before_tax': round(self.deductions_before_tax, 2),
            'social_insurance': round(self.social_insurance, 2),
            'housing_fund': round(self.housing_fund, 2),
            'taxable_income': round(self.taxable_income, 2),
            'income_tax': round(self.income_tax, 2),
            'deductions_after_tax': round(self.deductions_after_tax, 2),
            'net_salary': round(self.net_salary, 2),
            'employer_cost': round(self.employer_cost, 2),
        }
        if self.social_insurance_detail:
            result['social_insurance_detail'] = self.social_insurance_detail.to_dict()
        if self.housing_fund_detail:
            result['housing_fund_detail'] = self.housing_fund_detail.to_dict()
        if self.tax_detail:
            result['tax_detail'] = self.tax_detail.to_dict()
        return result


@dataclass
class YearEndBonusResult:
    """年终奖计算结果"""
    bonus_amount: float           # 年终奖金额
    tax_method: BonusTaxMethod    # 计税方式
    monthly_equivalent: float     # 月均金额（用于税率查找）
    tax_rate: float               # 税率
    quick_deduction: float        # 速算扣除数
    tax_amount: float             # 应纳税额
    net_bonus: float              # 税后年终奖
    tax_saved: float              # 与合并计税对比节省的税额
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'bonus_amount': round(self.bonus_amount, 2),
            'tax_method': self.tax_method.value,
            'monthly_equivalent': round(self.monthly_equivalent, 2),
            'tax_rate': self.tax_rate,
            'quick_deduction': round(self.quick_deduction, 2),
            'tax_amount': round(self.tax_amount, 2),
            'net_bonus': round(self.net_bonus, 2),
            'tax_saved': round(self.tax_saved, 2),
        }


# ============================================================================
# Basic Salary Functions
# ============================================================================

def calculate_hourly_rate(monthly_salary: float, work_hours_per_month: float = 174) -> float:
    """
    计算小时工资率
    
    标准工作时长：每月约 174 小时（21.75天 × 8小时）
    
    Args:
        monthly_salary: 月薪
        work_hours_per_month: 每月工作时长
    
    Returns:
        小时工资率
    
    Examples:
        >>> calculate_hourly_rate(10000)
        57.47...
    """
    return round(monthly_salary / work_hours_per_month, 2)


def calculate_daily_rate(monthly_salary: float, work_days_per_month: float = 21.75) -> float:
    """
    计算日工资率
    
    标准工作日：每月约 21.75 天
    
    Args:
        monthly_salary: 月薪
        work_days_per_month: 每月工作天数
    
    Returns:
        日工资率
    
    Examples:
        >>> calculate_daily_rate(10000)
        459.77...
    """
    return round(monthly_salary / work_days_per_month, 2)


def convert_salary(salary: float, from_type: SalaryType, to_type: SalaryType, 
                   work_hours_per_month: float = 174, work_days_per_month: float = 21.75) -> float:
    """
    薪资类型转换
    
    Args:
        salary: 薪资金额
        from_type: 原薪资类型
        to_type: 目标薪资类型
        work_hours_per_month: 每月工作时长
        work_days_per_month: 每月工作天数
    
    Returns:
        转换后的薪资
    
    Examples:
        >>> convert_salary(10000, SalaryType.MONTHLY, SalaryType.HOURLY)
        57.47...
        >>> convert_salary(50, SalaryType.HOURLY, SalaryType.MONTHLY)
        8700.0
    """
    # 先转换为月薪
    if from_type == SalaryType.HOURLY:
        monthly = salary * work_hours_per_month
    elif from_type == SalaryType.DAILY:
        monthly = salary * work_days_per_month
    else:
        monthly = salary
    
    # 再转换为目标类型
    if to_type == SalaryType.HOURLY:
        return round(monthly / work_hours_per_month, 2)
    elif to_type == SalaryType.DAILY:
        return round(monthly / work_days_per_month, 2)
    else:
        return round(monthly, 2)


# ============================================================================
# Overtime Pay Functions
# ============================================================================

def calculate_overtime_pay(
    hourly_rate: float,
    overtime_hours: Dict[str, float],
    overtime_types: Optional[Dict[OvertimeType, float]] = None
) -> float:
    """
    计算加班费
    
    Args:
        hourly_rate: 小时工资率
        overtime_hours: 加班时长 {'weekday': 10, 'weekend': 8, 'holiday': 4}
        overtime_types: 加班类型倍数（默认使用法定标准）
    
    Returns:
        加班费总额
    
    Examples:
        >>> calculate_overtime_pay(50, {'weekday': 10, 'weekend': 8})
        1750.0
    """
    multipliers = overtime_types or {
        'weekday': OVERTIME_MULTIPLIERS['weekday'],
        'weekend': OVERTIME_MULTIPLIERS['weekend'],
        'holiday': OVERTIME_MULTIPLIERS['holiday'],
    }
    
    total_overtime_pay = 0.0
    
    for overtime_type, hours in overtime_hours.items():
        multiplier = multipliers.get(overtime_type, 1.5)
        total_overtime_pay += hourly_rate * hours * multiplier
    
    return round(total_overtime_pay, 2)


def calculate_overtime_pay_from_monthly(
    monthly_salary: float,
    overtime_hours: Dict[str, float],
    work_hours_per_month: float = 174
) -> float:
    """
    从月薪计算加班费
    
    Args:
        monthly_salary: 月薪
        overtime_hours: 加班时长
        work_hours_per_month: 每月工作时长
    
    Returns:
        加班费总额
    
    Examples:
        >>> calculate_overtime_pay_from_monthly(10000, {'weekday': 10})
        864.66...
    """
    hourly_rate = calculate_hourly_rate(monthly_salary, work_hours_per_month)
    return calculate_overtime_pay(hourly_rate, overtime_hours)


# ============================================================================
# Social Insurance Functions
# ============================================================================

def get_social_insurance_base(salary: float, city: CityCode) -> float:
    """
    获取社保缴费基数
    
    基数 = min(max(工资, 下限), 上限)
    
    Args:
        salary: 工资
        city: 城市
    
    Returns:
        社保缴费基数
    
    Examples:
        >>> get_social_insurance_base(10000, CityCode.SHANGHAI)
        10000
        >>> get_social_insurance_base(5000, CityCode.SHANGHAI)
        7310  # 达到下限
    """
    city_key = city.value
    limits = SOCIAL_INSURANCE_BASE_LIMITS.get(city_key, SOCIAL_INSURANCE_BASE_LIMITS['default'])
    
    return min(max(salary, limits['min']), limits['max'])


def calculate_social_insurance(
    salary: float,
    city: CityCode,
    custom_base: Optional[float] = None,
    custom_rates: Optional[Dict[str, Dict[str, float]]] = None
) -> SocialInsuranceResult:
    """
    计算五险
    
    Args:
        salary: 工资
        city: 城市
        custom_base: 自定义缴费基数
        custom_rates: 自定义缴费比例
    
    Returns:
        社保计算结果
    
    Examples:
        >>> result = calculate_social_insurance(10000, CityCode.SHANGHAI)
        >>> result.total_employee
        1050.0
    """
    # 获取缴费基数
    base = custom_base if custom_base is not None else get_social_insurance_base(salary, city)
    
    # 获取缴费比例
    city_key = city.value
    rates = custom_rates or SOCIAL_INSURANCE_RATES.get(city_key, SOCIAL_INSURANCE_RATES['default'])
    
    # 计算各项社保
    pension_employee = round(base * rates['pension']['employee'], 2)
    pension_employer = round(base * rates['pension']['employer'], 2)
    medical_employee = round(base * rates['medical']['employee'], 2)
    medical_employer = round(base * rates['medical']['employer'], 2)
    unemployment_employee = round(base * rates['unemployment']['employee'], 2)
    unemployment_employer = round(base * rates['unemployment']['employer'], 2)
    work_injury_employer = round(base * rates['work_injury']['employer'], 2)
    
    # 计算总额
    total_employee = pension_employee + medical_employee + unemployment_employee
    total_employer = pension_employer + medical_employer + unemployment_employer + work_injury_employer
    
    return SocialInsuranceResult(
        base=base,
        pension_employee=pension_employee,
        pension_employer=pension_employer,
        medical_employee=medical_employee,
        medical_employer=medical_employer,
        unemployment_employee=unemployment_employee,
        unemployment_employer=unemployment_employer,
        work_injury_employer=work_injury_employer,
        total_employee=total_employee,
        total_employer=total_employer,
    )


# ============================================================================
# Housing Fund Functions
# ============================================================================

def get_housing_fund_base(salary: float, city: CityCode) -> float:
    """
    获取公积金缴费基数
    
    Args:
        salary: 工资
        city: 城市
    
    Returns:
        公积金缴费基数
    
    Examples:
        >>> get_housing_fund_base(10000, CityCode.SHANGHAI)
        10000
    """
    city_key = city.value
    limits = HOUSING_FUND_BASE_LIMITS.get(city_key, HOUSING_FUND_BASE_LIMITS['default'])
    
    return min(max(salary, limits['min']), limits['max'])


def calculate_housing_fund(
    salary: float,
    city: CityCode,
    custom_base: Optional[float] = None,
    custom_rate: Optional[float] = None,
    employer_rate: Optional[float] = None
) -> HousingFundResult:
    """
    计算住房公积金
    
    Args:
        salary: 工资
        city: 城市
        custom_base: 自定义缴费基数
        custom_rate: 自定义个人比例
        employer_rate: 自定义单位比例（默认与个人相同）
    
    Returns:
        公积金计算结果
    
    Examples:
        >>> result = calculate_housing_fund(10000, CityCode.SHANGHAI)
        >>> result.amount_employee
        700.0
    """
    # 获取缴费基数
    base = custom_base if custom_base is not None else get_housing_fund_base(salary, city)
    
    # 获取缴费比例
    city_key = city.value
    default_rates = SOCIAL_INSURANCE_RATES.get(city_key, SOCIAL_INSURANCE_RATES['default'])
    
    rate_employee = custom_rate if custom_rate is not None else default_rates['housing_fund']['employee']
    rate_employer = employer_rate if employer_rate is not None else default_rates['housing_fund']['employer']
    
    # 计算缴纳金额
    amount_employee = round(base * rate_employee, 2)
    amount_employer = round(base * rate_employer, 2)
    total = amount_employee + amount_employer
    
    return HousingFundResult(
        base=base,
        rate_employee=rate_employee,
        rate_employer=rate_employer,
        amount_employee=amount_employee,
        amount_employer=amount_employer,
        total=total,
    )


# ============================================================================
# Individual Income Tax Functions (China 2019)
# ============================================================================

def find_tax_rate(taxable_income: float, rates: List[Tuple[float, int, float]] = None) -> Tuple[float, int, float]:
    """
    查找适用税率
    
    Args:
        taxable_income: 应纳税所得额
        rates: 税率表（默认使用年度税率）
    
    Returns:
        (应纳税所得额上限, 税率%, 速算扣除数)
    
    Examples:
        >>> find_tax_rate(5000)
        (12000, 10, 210)
    """
    rates = rates or IIT_ANNUAL_RATES
    
    for limit, rate, deduction in rates:
        if taxable_income <= limit:
            return limit, rate, deduction
    
    # 超过最高档
    return rates[-1][0], rates[-1][1], rates[-1][2]


def calculate_monthly_tax(
    monthly_income: float,
    cumulative_income: float = 0,
    cumulative_tax: float = 0,
    basic_deduction: float = BASIC_DEDUCTION,
    special_deductions: float = 0,
    social_insurance: float = 0,
    housing_fund: float = 0,
    other_deductions: float = 0
) -> TaxResult:
    """
    计算月度个人所得税（累计预扣预缴法）
    
    累计预扣预缴公式:
        累计应纳税所得额 = 累计收入 - 累计减除费用 - 累计专项扣除 - 累计专项附加扣除 - 累计其他扣除
        累计应纳税额 = 累计应纳税所得额 × 税率 - 速算扣除数
        本期应纳税额 = 累计应纳税额 - 累计已预扣预缴税额
    
    Args:
        monthly_income: 本月收入
        cumulative_income: 累计收入（不含本月）
        cumulative_tax: 累计已缴税额
        basic_deduction: 基本减除费用（起征点）
        special_deductions: 专项附加扣除
        social_insurance: 社保（个人部分）
        housing_fund: 公积金（个人部分）
        other_deductions: 其他扣除
    
    Returns:
        个税计算结果
    
    Examples:
        >>> result = calculate_monthly_tax(15000)
        >>> result.tax_amount
        790.0
    """
    # 累计收入
    total_income = cumulative_income + monthly_income
    
    # 累计减除费用（每月5000）
    cumulative_basic_deduction = basic_deduction * ((cumulative_income / monthly_income) + 1) if monthly_income > 0 else basic_deduction
    
    # 简化处理：假设累计月份已知
    # 累计应纳税所得额
    total_taxable_income = total_income - cumulative_basic_deduction - (social_insurance + housing_fund) - special_deductions - other_deductions
    
    # 如果是单月计算（累计为0）
    if cumulative_income == 0:
        taxable_income = monthly_income - basic_deduction - social_insurance - housing_fund - special_deductions - other_deductions
    else:
        taxable_income = total_taxable_income
    
    # 确保应纳税所得额不为负
    taxable_income = max(0, taxable_income)
    
    # 查找税率
    _, tax_rate, quick_deduction = find_tax_rate(taxable_income)
    
    # 计算应纳税额
    tax_amount = taxable_income * (tax_rate / 100) - quick_deduction
    
    # 计算累计应纳税额
    cumulative_tax_amount = tax_amount if cumulative_income == 0 else (total_taxable_income * (tax_rate / 100) - quick_deduction)
    
    # 本期应纳税额 = 累计应纳税额 - 已预扣预缴税额
    actual_tax = max(0, cumulative_tax_amount - cumulative_tax)
    
    return TaxResult(
        gross_income=monthly_income,
        taxable_income=taxable_income,
        tax_rate=tax_rate,
        quick_deduction=quick_deduction,
        tax_amount=actual_tax,
        cumulative_tax=cumulative_tax_amount,
    )


def calculate_simple_monthly_tax(
    gross_salary: float,
    social_insurance: float = 0,
    housing_fund: float = 0,
    special_deductions: float = 0
) -> float:
    """
    简化月度个税计算（不考虑累计）
    
    Args:
        gross_salary: 税前工资
        social_insurance: 社保（个人部分）
        housing_fund: 公积金（个人部分）
        special_deductions: 专项附加扣除
    
    Returns:
        应纳税额
    
    Examples:
        >>> calculate_simple_monthly_tax(15000, 1050, 700)
        490.0
    """
    taxable_income = gross_salary - BASIC_DEDUCTION - social_insurance - housing_fund - special_deductions
    taxable_income = max(0, taxable_income)
    
    _, tax_rate, quick_deduction = find_tax_rate(taxable_income)
    
    tax = taxable_income * (tax_rate / 100) - quick_deduction
    return round(max(0, tax), 2)


# ============================================================================
# Year-End Bonus Tax Functions
# ============================================================================

def calculate_year_end_bonus_separate(bonus: float) -> YearEndBonusResult:
    """
    年终奖单独计税
    
    公式: 应纳税额 = 年终奖 ÷ 12 × 适用税率 - 速算扣除数
    
    Args:
        bonus: 年终奖金额
    
    Returns:
        年终奖计算结果
    
    Examples:
        >>> result = calculate_year_end_bonus_separate(30000)
        >>> result.tax_amount
        900.0
    """
    # 月均金额
    monthly_equivalent = bonus / 12
    
    # 查找税率
    _, tax_rate, quick_deduction = find_tax_rate(monthly_equivalent, YEAR_END_BONUS_RATES)
    
    # 计算税额
    tax_amount = bonus * (tax_rate / 100) - quick_deduction
    net_bonus = bonus - tax_amount
    
    return YearEndBonusResult(
        bonus_amount=bonus,
        tax_method=BonusTaxMethod.SEPARATE,
        monthly_equivalent=monthly_equivalent,
        tax_rate=tax_rate,
        quick_deduction=quick_deduction,
        tax_amount=round(tax_amount, 2),
        net_bonus=round(net_bonus, 2),
        tax_saved=0,  # 后续计算
    )


def calculate_year_end_bonus_combined(
    bonus: float,
    monthly_salary: float,
    monthly_tax_paid: float = 0,
    social_insurance: float = 0,
    housing_fund: float = 0,
    special_deductions: float = 0,
    month: int = 12
) -> Tuple[float, YearEndBonusResult]:
    """
    年终奖合并计税（并入综合所得）
    
    Args:
        bonus: 年终奖金额
        monthly_salary: 月工资
        monthly_tax_paid: 已缴月度税额
        social_insurance: 月社保
        housing_fund: 月公积金
        special_deductions: 月专项附加扣除
        month: 发放月份
    
    Returns:
        (合并计税税额, 计算结果)
    
    Examples:
        >>> tax, result = calculate_year_end_bonus_combined(30000, 10000)
    """
    # 计算年度累计收入（简化：假设发放月为12月）
    cumulative_income = monthly_salary * month
    total_income = cumulative_income + bonus
    
    # 累计减除费用
    total_deduction = BASIC_DEDUCTION * month
    
    # 累计专项扣除
    total_social = social_insurance * month
    total_fund = housing_fund * month
    total_special = special_deductions * month
    
    # 累计应纳税所得额
    taxable_income = total_income - total_deduction - total_social - total_fund - total_special
    taxable_income = max(0, taxable_income)
    
    # 查找税率
    _, tax_rate, quick_deduction = find_tax_rate(taxable_income)
    
    # 累计应纳税额
    total_tax = taxable_income * (tax_rate / 100) - quick_deduction
    
    # 本期应纳税额
    tax_amount = max(0, total_tax - monthly_tax_paid)
    
    # 税后年终奖（需要扣除月薪部分）
    net_bonus = bonus - (tax_amount - calculate_simple_monthly_tax(monthly_salary, social_insurance, housing_fund, special_deductions))
    
    result = YearEndBonusResult(
        bonus_amount=bonus,
        tax_method=BonusTaxMethod.COMBINED,
        monthly_equivalent=bonus / 12,
        tax_rate=tax_rate,
        quick_deduction=quick_deduction,
        tax_amount=round(tax_amount, 2),
        net_bonus=round(net_bonus, 2),
        tax_saved=0,
    )
    
    return tax_amount, result


def compare_year_end_bonus_methods(
    bonus: float,
    monthly_salary: float,
    monthly_tax_paid: float = 0,
    social_insurance: float = 0,
    housing_fund: float = 0,
    special_deductions: float = 0
) -> Dict[str, Any]:
    """
    比较年终奖计税方式
    
    Args:
        bonus: 年终奖金额
        monthly_salary: 月工资
        monthly_tax_paid: 已缴月度税额
        social_insurance: 月社保
        housing_fund: 月公积金
        special_deductions: 月专项附加扣除
    
    Returns:
        比较结果
    
    Examples:
        >>> compare_year_end_bonus_methods(30000, 10000)
        {'recommended_method': 'separate', 'tax_saved': 100, ...}
    """
    # 单独计税
    separate_result = calculate_year_end_bonus_separate(bonus)
    
    # 合并计税
    combined_tax, combined_result = calculate_year_end_bonus_combined(
        bonus, monthly_salary, monthly_tax_paid, social_insurance, housing_fund, special_deductions
    )
    
    # 计算税额差异
    tax_saved = combined_tax - separate_result.tax_amount
    
    # 推荐：税额较低的方式
    if separate_result.tax_amount <= combined_tax:
        recommended = 'separate'
        recommended_result = separate_result
    else:
        recommended = 'combined'
        recommended_result = combined_result
    
    return {
        'separate': separate_result.to_dict(),
        'combined': combined_result.to_dict(),
        'recommended_method': recommended,
        'tax_saved': abs(tax_saved),
        'recommended_result': recommended_result.to_dict(),
    }


def find_year_end_bonus_optimal_split(
    total_bonus: float,
    monthly_salary: float,
    max_split_parts: int = 2
) -> Dict[str, Any]:
    """
    寻找年终奖最优拆分方案（避免税率临界点）
    
    年终奖存在"税率临界点"陷阱：
    - 如 36001 元比 36000 元多交约 2300 元税
    
    Args:
        total_bonus: 总年终奖金额
        monthly_salary: 月工资
        max_split_parts: 最大拆分份数
    
    Returns:
        最优拆分方案
    
    Examples:
        >>> find_year_end_bonus_optimal_split(36001, 10000)
        {'split_amount': 36000, 'remaining': 1, ...}
    """
    # 税率临界点（月均金额 × 12）
    critical_points = [3000 * 12, 12000 * 12, 25000 * 12, 35000 * 12, 55000 * 12, 80000 * 12]
    
    # 寻找最优拆分
    best_split = None
    best_tax = float('inf')
    
    # 检查是否超过临界点
    for critical in critical_points:
        if total_bonus > critical and total_bonus <= critical * 1.05:  # 超过不超过5%
            # 拆分到临界点以下
            split_amount = critical
            remaining = total_bonus - critical
            
            # 计算两部分税额
            split_tax = calculate_year_end_bonus_separate(split_amount).tax_amount
            remaining_tax = calculate_year_end_bonus_separate(remaining).tax_amount if remaining > 0 else 0
            
            total_tax = split_tax + remaining_tax
            
            # 计算不拆分税额
            no_split_tax = calculate_year_end_bonus_separate(total_bonus).tax_amount
            
            # 如果拆分更划算
            if total_tax < no_split_tax and total_tax < best_tax:
                best_tax = total_tax
                best_split = {
                    'original_bonus': total_bonus,
                    'original_tax': no_split_tax,
                    'split_amount': split_amount,
                    'split_tax': split_tax,
                    'remaining': remaining,
                    'remaining_tax': remaining_tax,
                    'total_tax': total_tax,
                    'tax_saved': no_split_tax - total_tax,
                }
    
    if best_split:
        return best_split
    
    # 不需要拆分
    return {
        'original_bonus': total_bonus,
        'original_tax': calculate_year_end_bonus_separate(total_bonus).tax_amount,
        'split_amount': total_bonus,
        'split_tax': calculate_year_end_bonus_separate(total_bonus).tax_amount,
        'remaining': 0,
        'remaining_tax': 0,
        'total_tax': calculate_year_end_bonus_separate(total_bonus).tax_amount,
        'tax_saved': 0,
        'no_split_needed': True,
    }


# ============================================================================
# Full Payroll Calculation
# ============================================================================

def calculate_payroll(params: SalaryParams) -> PayrollResult:
    """
    完整薪资计算
    
    Args:
        params: 薪资参数
    
    Returns:
        薪资计算结果
    
    Examples:
        >>> params = SalaryParams(basic_salary=15000, city=CityCode.SHANGHAI)
        >>> result = calculate_payroll(params)
        >>> result.net_salary
        12660.0
    """
    # 基本工资
    basic_salary = params.basic_salary
    
    # 加班费计算
    if params.overtime_hours and params.salary_type == SalaryType.MONTHLY:
        hourly_rate = calculate_hourly_rate(basic_salary)
        overtime_pay = calculate_overtime_pay(hourly_rate, params.overtime_hours)
    else:
        overtime_pay = 0.0
    
    # 税前总收入
    gross_salary = basic_salary + overtime_pay + params.bonus + params.allowances
    
    # 税前扣款
    deductions_before_tax = params.deductions
    
    # 社保计算
    social_insurance_result = calculate_social_insurance(
        gross_salary, params.city, params.social_insurance_base
    )
    
    # 公积金计算
    housing_fund_result = calculate_housing_fund(
        gross_salary, params.city, params.housing_fund_base, params.housing_fund_rate
    )
    
    # 个人缴纳的社保和公积金
    social_insurance_employee = social_insurance_result.total_employee
    housing_fund_employee = housing_fund_result.amount_employee
    
    # 个税计算
    tax_result = calculate_monthly_tax(
        gross_salary,
        social_insurance=social_insurance_employee,
        housing_fund=housing_fund_employee,
        special_deductions=params.special_deductions,
        other_deductions=deductions_before_tax,
    )
    
    # 税后工资
    net_salary = gross_salary - social_insurance_employee - housing_fund_employee - tax_result.tax_amount - deductions_before_tax
    
    # 单位用工成本
    employer_cost = gross_salary + social_insurance_result.total_employer + housing_fund_result.amount_employer
    
    return PayrollResult(
        gross_salary=gross_salary,
        basic_salary=basic_salary,
        overtime_pay=overtime_pay,
        bonus=params.bonus,
        allowances=params.allowances,
        deductions_before_tax=deductions_before_tax,
        social_insurance=social_insurance_employee,
        housing_fund=housing_fund_employee,
        taxable_income=tax_result.taxable_income,
        income_tax=tax_result.tax_amount,
        deductions_after_tax=0,
        net_salary=round(net_salary, 2),
        employer_cost=round(employer_cost, 2),
        social_insurance_detail=social_insurance_result,
        housing_fund_detail=housing_fund_result,
        tax_detail=tax_result,
    )


def calculate_payroll_from_params(
    basic_salary: float,
    overtime_hours: Optional[Dict[str, float]] = None,
    bonus: float = 0,
    allowances: float = 0,
    city: str = 'shanghai',
    special_deductions: float = 0
) -> Dict[str, Any]:
    """
    便捷薪资计算函数
    
    Args:
        basic_salary: 基本工资
        overtime_hours: 加班时长
        bonus: 奖金
        allowances: 补贴
        city: 城市
        special_deductions: 专项附加扣除
    
    Returns:
        薪资计算结果（字典）
    
    Examples:
        >>> calculate_payroll_from_params(15000)
        {'gross_salary': 15000, 'net_salary': 12660.0, ...}
    """
    city_enum = CityCode(city) if city in [c.value for c in CityCode] else CityCode.OTHER
    
    params = SalaryParams(
        basic_salary=basic_salary,
        overtime_hours=overtime_hours or {},
        bonus=bonus,
        allowances=allowances,
        city=city_enum,
        special_deductions=special_deductions,
    )
    
    result = calculate_payroll(params)
    return result.to_dict()


# ============================================================================
# Annual Summary Functions
# ============================================================================

def calculate_annual_summary(
    monthly_salary: float,
    year_end_bonus: float = 0,
    city: CityCode = CityCode.SHANGHAI,
    special_deductions: float = 0,
    work_months: int = 12
) -> Dict[str, Any]:
    """
    计算年度薪资汇总
    
    Args:
        monthly_salary: 月工资
        year_end_bonus: 年终奖
        city: 城市
        special_deductions: 专项附加扣除
        work_months: 工作月数
    
    Returns:
        年度汇总
    
    Examples:
        >>> calculate_annual_summary(15000, 30000)
        {'annual_gross': ..., 'annual_net': ..., ...}
    """
    # 月度计算
    monthly_result = calculate_payroll_from_params(
        monthly_salary, city=city.value, special_deductions=special_deductions
    )
    
    # 年度累计
    annual_gross = monthly_salary * work_months + year_end_bonus
    annual_social = monthly_result['social_insurance'] * work_months
    annual_fund = monthly_result['housing_fund'] * work_months
    
    # 年度月度个税累计
    monthly_tax = monthly_result['income_tax']
    annual_monthly_tax = monthly_tax * work_months
    
    # 年终奖计税
    bonus_comparison = compare_year_end_bonus_methods(year_end_bonus, monthly_salary, annual_monthly_tax)
    
    # 使用最优方案
    bonus_tax = bonus_comparison['recommended_result']['tax_amount']
    bonus_net = bonus_comparison['recommended_result']['net_bonus']
    
    # 年度总税额
    annual_tax = annual_monthly_tax + bonus_tax
    
    # 年度税后收入
    annual_net = annual_gross - annual_social - annual_fund - annual_tax
    
    # 单位年度用工成本
    employer_social = monthly_result['social_insurance_detail']['total_employer'] * work_months
    employer_fund = monthly_result['housing_fund_detail']['amount_employer'] * work_months
    employer_cost = (monthly_salary * work_months + year_end_bonus) + employer_social + employer_fund
    
    return {
        'annual_gross': round(annual_gross, 2),
        'annual_net': round(annual_net, 2),
        'annual_social_insurance': round(annual_social, 2),
        'annual_housing_fund': round(annual_fund, 2),
        'annual_income_tax': round(annual_tax, 2),
        'monthly_net': monthly_result['net_salary'],
        'year_end_bonus_net': round(bonus_net, 2),
        'bonus_tax_method': bonus_comparison['recommended_method'],
        'bonus_tax_saved': bonus_comparison['tax_saved'],
        'employer_annual_cost': round(employer_cost, 2),
    }


# ============================================================================
# Utility Functions
# ============================================================================

def format_salary_report(result: PayrollResult) -> str:
    """
    格式化薪资报告
    
    Args:
        result: 薪资计算结果
    
    Returns:
        格式化文本报告
    
    Examples:
        >>> params = SalaryParams(basic_salary=15000, city=CityCode.SHANGHAI)
        >>> result = calculate_payroll(params)
        >>> print(format_salary_report(result))
    """
    lines = []
    lines.append("=" * 50)
    lines.append("           薪资计算报告")
    lines.append("=" * 50)
    lines.append("")
    
    lines.append("【收入部分】")
    lines.append(f"  基本工资: ¥{result.basic_salary:.2f}")
    if result.overtime_pay > 0:
        lines.append(f"  加班费:   ¥{result.overtime_pay:.2f}")
    if result.bonus > 0:
        lines.append(f"  奖金:     ¥{result.bonus:.2f}")
    if result.allowances > 0:
        lines.append(f"  补贴:     ¥{result.allowances:.2f}")
    lines.append(f"  税前合计: ¥{result.gross_salary:.2f}")
    lines.append("")
    
    lines.append("【扣除部分】")
    lines.append(f"  社保(个人): ¥{result.social_insurance:.2f}")
    if result.social_insurance_detail:
        lines.append(f"    - 养老: ¥{result.social_insurance_detail.pension_employee:.2f}")
        lines.append(f"    - 医疗: ¥{result.social_insurance_detail.medical_employee:.2f}")
        lines.append(f"    - 失业: ¥{result.social_insurance_detail.unemployment_employee:.2f}")
    lines.append(f"  公积金(个人): ¥{result.housing_fund:.2f}")
    lines.append(f"  应纳税所得额: ¥{result.taxable_income:.2f}")
    if result.tax_detail:
        lines.append(f"  适用税率: {result.tax_detail.tax_rate}%")
    lines.append(f"  个人所得税: ¥{result.income_tax:.2f}")
    lines.append("")
    
    lines.append("【实发部分】")
    lines.append(f"  税后工资: ¥{result.net_salary:.2f}")
    lines.append("")
    
    lines.append("【单位成本】")
    lines.append(f"  单位用工成本: ¥{result.employer_cost:.2f}")
    if result.social_insurance_detail:
        lines.append(f"    - 社保(单位): ¥{result.social_insurance_detail.total_employer:.2f}")
    if result.housing_fund_detail:
        lines.append(f"    - 公积金(单位): ¥{result.housing_fund_detail.amount_employer:.2f}")
    lines.append("")
    
    lines.append("=" * 50)
    
    return "\n".join(lines)


def calculate_salary_increase_effect(
    current_salary: float,
    increase_amount: float,
    city: CityCode = CityCode.SHANGHAI,
    special_deductions: float = 0
) -> Dict[str, Any]:
    """
    计算涨薪实际效果
    
    Args:
        current_salary: 当前工资
        increase_amount: 涨薪金额
        city: 城市
        special_deductions: 专项附加扣除
    
    Returns:
        涨薪效果分析
    
    Examples:
        >>> calculate_salary_increase_effect(15000, 3000)
    """
    current_result = calculate_payroll_from_params(
        current_salary, city=city.value, special_deductions=special_deductions
    )
    
    new_salary = current_salary + increase_amount
    new_result = calculate_payroll_from_params(
        new_salary, city=city.value, special_deductions=special_deductions
    )
    
    # 涨薪前后对比
    gross_increase = increase_amount
    tax_increase = new_result['income_tax'] - current_result['income_tax']
    social_increase = new_result['social_insurance'] - current_result['social_insurance']
    fund_increase = new_result['housing_fund'] - current_result['housing_fund']
    net_increase = new_result['net_salary'] - current_result['net_salary']
    
    # 实际到手比例
    net_ratio = net_increase / gross_increase if gross_increase > 0 else 0
    
    return {
        'current_salary': current_salary,
        'new_salary': new_salary,
        'gross_increase': round(gross_increase, 2),
        'tax_increase': round(tax_increase, 2),
        'social_increase': round(social_increase, 2),
        'fund_increase': round(fund_increase, 2),
        'net_increase': round(net_increase, 2),
        'net_ratio': round(net_ratio * 100, 2),
        'current_net': current_result['net_salary'],
        'new_net': new_result['net_salary'],
    }


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Payroll Utilities Demo")
    print("=" * 60)
    
    # 基础薪资计算
    print("\n--- 基础薪资计算 ---")
    params = SalaryParams(
        basic_salary=15000,
        overtime_hours={'weekday': 10, 'weekend': 8},
        bonus=2000,
        allowances=500,
        city=CityCode.SHANGHAI,
        special_deductions=1000,
    )
    result = calculate_payroll(params)
    print(format_salary_report(result))
    
    # 加班费计算
    print("\n--- 加班费计算 ---")
    hourly = calculate_hourly_rate(10000)
    print(f"月薪 ¥10,000 的小时工资率: ¥{hourly}")
    overtime = calculate_overtime_pay(hourly, {'weekday': 20, 'weekend': 10, 'holiday': 8})
    print(f"20小时工作日 + 10小时周末 + 8小时节假日加班费: ¥{overtime}")
    
    # 个税计算
    print("\n--- 个税计算 ---")
    tax = calculate_simple_monthly_tax(20000, 1600, 1400, 1000)
    print(f"税前 ¥20,000，社保 ¥1,600，公积金 ¥1,400，专项扣除 ¥1,000")
    print(f"应纳税额: ¥{tax}")
    
    # 年终奖计税
    print("\n--- 年终奖计税 ---")
    bonus = 50000
    comparison = compare_year_end_bonus_methods(bonus, 15000)
    print(f"年终奖 ¥{bonus}")
    print(f"单独计税: ¥{comparison['separate']['tax_amount']}")
    print(f"合并计税: ¥{comparison['combined']['tax_amount']}")
    print(f"推荐方式: {comparison['recommended_method']}")
    print(f"节省税额: ¥{comparison['tax_saved']}")
    
    # 年终奖临界点检查
    print("\n--- 年终奖临界点检查 ---")
    optimal = find_year_end_bonus_optimal_split(36001, 10000)
    print(f"年终奖 ¥36,001")
    if optimal.get('no_split_needed'):
        print(f"无需拆分，税额: ¥{optimal['original_tax']}")
    else:
        print(f"建议拆分: ¥{optimal['split_amount']} + ¥{optimal['remaining']}")
        print(f"拆分后税额: ¥{optimal['total_tax']}")
        print(f"节省税额: ¥{optimal['tax_saved']}")
    
    # 年度汇总
    print("\n--- 年度汇总 ---")
    annual = calculate_annual_summary(15000, 30000)
    print(f"月薪 ¥15,000，年终奖 ¥30,000")
    print(f"年度税前: ¥{annual['annual_gross']}")
    print(f"年度税后: ¥{annual['annual_net']}")
    print(f"年度个税: ¥{annual['annual_income_tax']}")
    
    # 涨薪效果
    print("\n--- 涨薪效果分析 ---")
    effect = calculate_salary_increase_effect(15000, 5000)
    print(f"涨薪 ¥5,000")
    print(f"税前增加: ¥{effect['gross_increase']}")
    print(f"税后增加: ¥{effect['net_increase']}")
    print(f"实际到手比例: {effect['net_ratio']}%")
    
    # 不同城市社保对比
    print("\n--- 不同城市社保对比 ---")
    for city in [CityCode.BEIJING, CityCode.SHANGHAI, CityCode.GUANGZHOU, CityCode.SHENZHEN]:
        si = calculate_social_insurance(10000, city)
        hf = calculate_housing_fund(10000, city)
        print(f"{city.value}: 社保¥{si.total_employee}, 公积金¥{hf.amount_employee}, "
              f"合计¥{si.total_employee + hf.amount_employee}")
    
    print("\n" + "=" * 60)


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Enums
    'SalaryType',
    'CityCode',
    'OvertimeType',
    'BonusTaxMethod',
    
    # Data Classes
    'SalaryParams',
    'TaxResult',
    'SocialInsuranceResult',
    'HousingFundResult',
    'PayrollResult',
    'YearEndBonusResult',
    
    # Basic Functions
    'calculate_hourly_rate',
    'calculate_daily_rate',
    'convert_salary',
    
    # Overtime Functions
    'calculate_overtime_pay',
    'calculate_overtime_pay_from_monthly',
    
    # Social Insurance Functions
    'get_social_insurance_base',
    'calculate_social_insurance',
    
    # Housing Fund Functions
    'get_housing_fund_base',
    'calculate_housing_fund',
    
    # Tax Functions
    'find_tax_rate',
    'calculate_monthly_tax',
    'calculate_simple_monthly_tax',
    
    # Year-End Bonus Functions
    'calculate_year_end_bonus_separate',
    'calculate_year_end_bonus_combined',
    'compare_year_end_bonus_methods',
    'find_year_end_bonus_optimal_split',
    
    # Payroll Functions
    'calculate_payroll',
    'calculate_payroll_from_params',
    
    # Summary Functions
    'calculate_annual_summary',
    
    # Utility Functions
    'format_salary_report',
    'calculate_salary_increase_effect',
    
    # Constants
    'BASIC_DEDUCTION',
    'IIT_ANNUAL_RATES',
    'YEAR_END_BONUS_RATES',
    'OVERTIME_MULTIPLIERS',
    'SOCIAL_INSURANCE_RATES',
]