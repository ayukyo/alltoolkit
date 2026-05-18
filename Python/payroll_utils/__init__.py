#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Payroll Utilities Module
======================================
薪资计算工具模块

提供全面的薪资计算功能，包括个人所得税、社保公积金、加班费、年终奖计算等。
"""

from .mod import (
    # Enums
    SalaryType,
    CityCode,
    OvertimeType,
    BonusTaxMethod,
    
    # Data Classes
    SalaryParams,
    TaxResult,
    SocialInsuranceResult,
    HousingFundResult,
    PayrollResult,
    YearEndBonusResult,
    
    # Basic Functions
    calculate_hourly_rate,
    calculate_daily_rate,
    convert_salary,
    
    # Overtime Functions
    calculate_overtime_pay,
    calculate_overtime_pay_from_monthly,
    
    # Social Insurance Functions
    get_social_insurance_base,
    calculate_social_insurance,
    
    # Housing Fund Functions
    get_housing_fund_base,
    calculate_housing_fund,
    
    # Tax Functions
    find_tax_rate,
    calculate_monthly_tax,
    calculate_simple_monthly_tax,
    
    # Year-End Bonus Functions
    calculate_year_end_bonus_separate,
    calculate_year_end_bonus_combined,
    compare_year_end_bonus_methods,
    find_year_end_bonus_optimal_split,
    
    # Payroll Functions
    calculate_payroll,
    calculate_payroll_from_params,
    
    # Summary Functions
    calculate_annual_summary,
    
    # Utility Functions
    format_salary_report,
    calculate_salary_increase_effect,
    
    # Constants
    BASIC_DEDUCTION,
    IIT_ANNUAL_RATES,
    YEAR_END_BONUS_RATES,
    OVERTIME_MULTIPLIERS,
    SOCIAL_INSURANCE_RATES,
)

__version__ = '1.0.0'
__author__ = 'AllToolkit Contributors'
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