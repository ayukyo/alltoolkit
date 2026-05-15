"""
Loan Calculator Utils - 贷款计算工具模块

提供全面的贷款和金融计算功能，包括：
- 贷款月供计算（等额本息、等额本金）
- 房贷计算器
- 分期还款计划生成
- 利息计算（单利、复利）
- 提前还款分析
- APR 计算
- 贷款比较工具

零外部依赖，纯 Python 实现。

Author: AllToolkit
License: MIT
"""

from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass
from enum import Enum
import math


# =============================================================================
# Enums
# =============================================================================

class PaymentFrequency(Enum):
    """还款频率"""
    MONTHLY = "monthly"          # 每月
    BI_WEEKLY = "bi_weekly"      # 每两周
    WEEKLY = "weekly"            # 每周
    QUARTERLY = "quarterly"      # 每季度
    SEMI_ANNUAL = "semi_annual"  # 每半年
    ANNUAL = "annual"            # 每年


class PaymentType(Enum):
    """还款方式"""
    EQUAL_PAYMENT = "equal_payment"       # 等额本息
    EQUAL_PRINCIPAL = "equal_principal"   # 等额本金
    INTEREST_ONLY = "interest_only"       # 只还利息


class InterestType(Enum):
    """利息类型"""
    SIMPLE = "simple"      # 单利
    COMPOUND = "compound"  # 复利


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class LoanParams:
    """贷款参数"""
    principal: float           # 贷款本金
    annual_rate: float         # 年利率（百分比，如 5.5 表示 5.5%）
    term_months: int           # 贷款期限（月）
    payment_type: PaymentType = PaymentType.EQUAL_PAYMENT
    payment_frequency: PaymentFrequency = PaymentFrequency.MONTHLY
    down_payment: float = 0.0  # 首付款
    fees: float = 0.0          # 贷款费用
    
    def __post_init__(self):
        """参数校验"""
        if self.principal <= 0:
            raise ValueError("贷款本金必须大于 0")
        if self.annual_rate < 0:
            raise ValueError("年利率不能为负数")
        if self.term_months <= 0:
            raise ValueError("贷款期限必须大于 0")
        if self.down_payment < 0:
            raise ValueError("首付款不能为负数")
        if self.fees < 0:
            raise ValueError("贷款费用不能为负数")


@dataclass
class PaymentScheduleItem:
    """单期还款详情"""
    period: int              # 期数
    payment: float           # 还款总额
    principal: float         # 本金部分
    interest: float          # 利息部分
    balance: float           # 剩余本金
    cumulative_interest: float  # 累计利息
    cumulative_principal: float  # 累计本金
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'period': self.period,
            'payment': round(self.payment, 2),
            'principal': round(self.principal, 2),
            'interest': round(self.interest, 2),
            'balance': round(self.balance, 2),
            'cumulative_interest': round(self.cumulative_interest, 2),
            'cumulative_principal': round(self.cumulative_principal, 2),
        }


@dataclass
class LoanSummary:
    """贷款汇总信息"""
    principal: float              # 贷款本金
    total_payments: float         # 还款总额
    total_interest: float         # 利息总额
    total_principal: float        # 本金总额
    number_of_payments: int       # 还款期数
    monthly_payment: float        # 月供
    effective_rate: float         # 有效年利率
    apr: float                    # APR（年化利率）
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'principal': round(self.principal, 2),
            'total_payments': round(self.total_payments, 2),
            'total_interest': round(self.total_interest, 2),
            'total_principal': round(self.total_principal, 2),
            'number_of_payments': self.number_of_payments,
            'monthly_payment': round(self.monthly_payment, 2),
            'effective_rate': round(self.effective_rate * 100, 4),
            'apr': round(self.apr * 100, 4),
        }


@dataclass
class EarlyPayoffResult:
    """提前还款分析结果"""
    original_term_months: int          # 原期限
    new_term_months: int               # 新期限
    months_saved: int                  # 提前还款节省的月数
    original_total_interest: float     # 原利息总额
    new_total_interest: float          # 新利息总额
    interest_saved: float              # 利息节省
    payoff_date_original: str          # 原还款结束日期
    payoff_date_new: str               # 新还款结束日期
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'original_term_months': self.original_term_months,
            'new_term_months': self.new_term_months,
            'months_saved': self.months_saved,
            'original_total_interest': round(self.original_total_interest, 2),
            'new_total_interest': round(self.new_total_interest, 2),
            'interest_saved': round(self.interest_saved, 2),
            'payoff_date_original': self.payoff_date_original,
            'payoff_date_new': self.payoff_date_new,
        }


@dataclass
class RefinanceResult:
    """再融资分析结果"""
    original_loan: LoanSummary         # 原贷款
    new_loan: LoanSummary              # 新贷款
    monthly_savings: float             # 月供节省
    total_savings: float               # 总节省
    break_even_months: int             # 盈亏平衡点（月）
    closing_costs: float               # 再融资成本
    net_savings: float                 # 净节省（扣除成本后）
    is_worth_it: bool                  # 是否值得再融资
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'monthly_savings': round(self.monthly_savings, 2),
            'total_savings': round(self.total_savings, 2),
            'break_even_months': self.break_even_months,
            'closing_costs': round(self.closing_costs, 2),
            'net_savings': round(self.net_savings, 2),
            'is_worth_it': self.is_worth_it,
        }


# =============================================================================
# 基础计算函数
# =============================================================================

def monthly_rate(annual_rate: float) -> float:
    """
    将年利率转换为月利率
    
    Args:
        annual_rate: 年利率（百分比形式，如 5.5 表示 5.5%）
    
    Returns:
        月利率（小数形式）
    
    Example:
        >>> monthly_rate(12)
        0.01
    """
    return (annual_rate / 100) / 12


def periodic_rate(annual_rate: float, frequency: PaymentFrequency) -> float:
    """
    将年利率转换为周期利率
    
    Args:
        annual_rate: 年利率（百分比形式）
        frequency: 还款频率
    
    Returns:
        周期利率（小数形式）
    """
    periods_per_year = {
        PaymentFrequency.MONTHLY: 12,
        PaymentFrequency.BI_WEEKLY: 26,
        PaymentFrequency.WEEKLY: 52,
        PaymentFrequency.QUARTERLY: 4,
        PaymentFrequency.SEMI_ANNUAL: 2,
        PaymentFrequency.ANNUAL: 1,
    }
    
    return (annual_rate / 100) / periods_per_year[frequency]


def periods_per_year(frequency: PaymentFrequency) -> int:
    """获取每年还款期数"""
    mapping = {
        PaymentFrequency.MONTHLY: 12,
        PaymentFrequency.BI_WEEKLY: 26,
        PaymentFrequency.WEEKLY: 52,
        PaymentFrequency.QUARTERLY: 4,
        PaymentFrequency.SEMI_ANNUAL: 2,
        PaymentFrequency.ANNUAL: 1,
    }
    return mapping[frequency]


# =============================================================================
# 月供计算
# =============================================================================

def calculate_equal_payment(params: LoanParams) -> float:
    """
    计算等额本息月供
    
    公式: M = P * [r(1+r)^n] / [(1+r)^n - 1]
    
    Args:
        params: 贷款参数
    
    Returns:
        月供金额
    
    Example:
        >>> params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        >>> calculate_equal_payment(params)
        8560.7488...
    """
    P = params.principal - params.down_payment
    r = monthly_rate(params.annual_rate)
    n = params.term_months
    
    if r == 0:
        # 无利率时，直接分摊本金
        return P / n
    
    # 等额本息公式
    M = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    
    return M


def calculate_equal_principal_payment(params: LoanParams) -> List[float]:
    """
    计算等额本金每期还款
    
    每期本金固定，利息递减
    
    Args:
        params: 贉款参数
    
    Returns:
        每期还款列表
    
    Example:
        >>> params = LoanParams(principal=120000, annual_rate=6, term_months=12, 
        ...                      payment_type=PaymentType.EQUAL_PRINCIPAL)
        >>> payments = calculate_equal_principal_payment(params)
        >>> payments[0] > payments[-1]  # 第一期 > 最后一期
        True
    """
    P = params.principal - params.down_payment
    r = monthly_rate(params.annual_rate)
    n = params.term_months
    
    # 每期本金固定
    principal_per_period = P / n
    
    payments = []
    remaining_balance = P
    
    for period in range(1, n + 1):
        # 当期利息
        interest = remaining_balance * r
        # 当期还款
        payment = principal_per_period + interest
        payments.append(payment)
        # 更新剩余本金
        remaining_balance -= principal_per_period
    
    return payments


def calculate_interest_only_payment(params: LoanParams) -> float:
    """
    计算只还利息期间的还款
    
    Args:
        params: 贉款参数
    
    Returns:
        每期还款（仅利息）
    
    Example:
        >>> params = LoanParams(principal=100000, annual_rate=6, term_months=12,
        ...                      payment_type=PaymentType.INTEREST_ONLY)
        >>> calculate_interest_only_payment(params)
        500.0
    """
    P = params.principal - params.down_payment
    r = monthly_rate(params.annual_rate)
    
    return P * r


def calculate_payment(params: LoanParams) -> Union[float, List[float]]:
    """
    根据还款方式计算月供
    
    Args:
        params: 贉款参数
    
    Returns:
        等额本息返回单值，等额本金返回列表
    
    Example:
        >>> params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        >>> calculate_payment(params)  # 等额本息
        8560.7488...
    """
    if params.payment_type == PaymentType.EQUAL_PAYMENT:
        return calculate_equal_payment(params)
    elif params.payment_type == PaymentType.EQUAL_PRINCIPAL:
        return calculate_equal_principal_payment(params)
    elif params.payment_type == PaymentType.INTEREST_ONLY:
        return calculate_interest_only_payment(params)
    else:
        raise ValueError(f"未知还款方式: {params.payment_type}")


# =============================================================================
# 还款计划生成
# =============================================================================

def generate_amortization_schedule(params: LoanParams) -> List[PaymentScheduleItem]:
    """
    生成分期还款计划表
    
    Args:
        params: 贉款参数
    
    Returns:
        还款计划列表
    
    Example:
        >>> params = LoanParams(principal=10000, annual_rate=6, term_months=12)
        >>> schedule = generate_amortization_schedule(params)
        >>> len(schedule) == 12
        True
        >>> schedule[0].interest > schedule[-1].interest  # 利息递减
        True
    """
    P = params.principal - params.down_payment
    r = monthly_rate(params.annual_rate)
    n = params.term_months
    
    if params.payment_type == PaymentType.EQUAL_PAYMENT:
        # 等额本息
        monthly_payment = calculate_equal_payment(params)
        remaining_balance = P
        cumulative_interest = 0.0
        cumulative_principal = 0.0
        
        schedule = []
        for period in range(1, n + 1):
            # 当期利息
            interest = remaining_balance * r
            # 当期本金
            principal_payment = monthly_payment - interest
            # 更新剩余本金
            remaining_balance -= principal_payment
            # 确保最后一期余额为 0
            if period == n:
                remaining_balance = 0
                principal_payment = P - cumulative_principal
            
            cumulative_interest += interest
            cumulative_principal += principal_payment
            
            schedule.append(PaymentScheduleItem(
                period=period,
                payment=monthly_payment,
                principal=principal_payment,
                interest=interest,
                balance=max(0, remaining_balance),
                cumulative_interest=cumulative_interest,
                cumulative_principal=cumulative_principal,
            ))
        
        return schedule
    
    elif params.payment_type == PaymentType.EQUAL_PRINCIPAL:
        # 等额本金
        principal_per_period = P / n
        remaining_balance = P
        cumulative_interest = 0.0
        cumulative_principal = 0.0
        
        schedule = []
        for period in range(1, n + 1):
            # 当期利息
            interest = remaining_balance * r
            # 当期还款
            payment = principal_per_period + interest
            # 更新剩余本金
            remaining_balance -= principal_per_period
            
            cumulative_interest += interest
            cumulative_principal += principal_per_period
            
            schedule.append(PaymentScheduleItem(
                period=period,
                payment=payment,
                principal=principal_per_period,
                interest=interest,
                balance=max(0, remaining_balance),
                cumulative_interest=cumulative_interest,
                cumulative_principal=cumulative_principal,
            ))
        
        return schedule
    
    elif params.payment_type == PaymentType.INTEREST_ONLY:
        # 只还利息
        interest_payment = P * r
        cumulative_interest = 0.0
        
        schedule = []
        for period in range(1, n + 1):
            cumulative_interest += interest_payment
            
            # 最后一期需要归还本金
            if period == n:
                payment = interest_payment + P
                principal_payment = P
                balance = 0
            else:
                payment = interest_payment
                principal_payment = 0
                balance = P
            
            schedule.append(PaymentScheduleItem(
                period=period,
                payment=payment,
                principal=principal_payment,
                interest=interest_payment,
                balance=balance,
                cumulative_interest=cumulative_interest,
                cumulative_principal=principal_payment * period,
            ))
        
        return schedule
    
    else:
        raise ValueError(f"未知还款方式: {params.payment_type}")


# =============================================================================
# 贷款汇总
# =============================================================================

def calculate_loan_summary(params: LoanParams) -> LoanSummary:
    """
    计算贷款汇总信息
    
    Args:
        params: 贉款参数
    
    Returns:
        贉款汇总
    
    Example:
        >>> params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        >>> summary = calculate_loan_summary(params)
        >>> summary.total_interest > 0
        True
    """
    P = params.principal - params.down_payment
    schedule = generate_amortization_schedule(params)
    
    total_payments = sum(item.payment for item in schedule)
    total_interest = sum(item.interest for item in schedule)
    total_principal = P
    
    # 月供（等额本息时为固定值，等额本金时为第一期）
    if params.payment_type == PaymentType.EQUAL_PAYMENT:
        monthly_payment = calculate_equal_payment(params)
    else:
        monthly_payment = schedule[0].payment
    
    # 有效年利率
    effective_rate = params.annual_rate / 100
    
    # APR 计算（考虑费用）
    if params.fees > 0:
        apr = calculate_apr(P, monthly_payment, params.term_months, params.fees)
    else:
        apr = effective_rate
    
    return LoanSummary(
        principal=params.principal,
        total_payments=total_payments,
        total_interest=total_interest,
        total_principal=total_principal,
        number_of_payments=len(schedule),
        monthly_payment=monthly_payment,
        effective_rate=effective_rate,
        apr=apr,
    )


# =============================================================================
# APR 计算
# =============================================================================

def calculate_apr(principal: float, payment: float, term_months: int, fees: float = 0) -> float:
    """
    计算 APR（年化百分比利率）
    
    考虑贷款费用后的真实年利率
    
    Args:
        principal: 贉款本金
        payment: 每期还款
        term_months: 期限（月）
        fees: 贉款费用
    
    Returns:
        APR（小数形式）
    
    Example:
        >>> calculate_apr(100000, 8560.75, 12, 1000)  # 有费用时 APR > 原利率
        0.0599...
    """
    # 实际获得的金额（扣除费用）
    actual_principal = principal - fees
    if actual_principal <= 0:
        raise ValueError("费用不能超过本金")
    
    # 使用二分法求解 APR
    # 目标: 找到 r 使得 PV(payment, r, n) = actual_principal
    # PV = payment * (1 - (1+r)^(-n)) / r
    
    def present_value(payment: float, r: float, n: int) -> float:
        """计算现值"""
        if r <= 0:
            return payment * n
        return payment * (1 - (1 + r) ** (-n)) / r
    
    # 二分搜索范围
    r_low = 0.00001 / 12  # 月利率下限
    r_high = 0.5 / 12     # 月利率上限 (50% 年利率)
    tolerance = 1e-8
    
    for _ in range(100):
        r_mid = (r_low + r_high) / 2
        pv_mid = present_value(payment, r_mid, term_months)
        
        if abs(pv_mid - actual_principal) < tolerance:
            return r_mid * 12
        
        if pv_mid > actual_principal:
            # PV too high, need higher rate
            r_low = r_mid
        else:
            # PV too low, need lower rate
            r_high = r_mid
    
    return r_mid * 12


# =============================================================================
# 提前还款分析
# =============================================================================

def analyze_early_payoff(
    params: LoanParams,
    extra_payment: float = 0,
    lump_sum: float = 0,
    lump_sum_period: int = 1,
    start_date: str = "2024-01-01"
) -> EarlyPayoffResult:
    """
    分析提前还款影响
    
    Args:
        params: 贉款参数
        extra_payment: 每期额外还款
        lump_sum: 一次性提前还款金额
        lump_sum_period: 一次性还款的期数
        start_date: 开始日期
    
    Returns:
        提前还款分析结果
    
    Example:
        >>> params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        >>> result = analyze_early_payoff(params, extra_payment=1000)
        >>> result.months_saved > 0
        True
    """
    # 原贷款分析
    original_schedule = generate_amortization_schedule(params)
    original_interest = sum(item.interest for item in original_schedule)
    
    # 模拟提前还款
    P = params.principal - params.down_payment
    r = monthly_rate(params.annual_rate)
    
    if params.payment_type == PaymentType.EQUAL_PAYMENT:
        base_payment = calculate_equal_payment(params)
    else:
        base_payment = original_schedule[0].payment
    
    remaining_balance = P
    period = 0
    new_total_interest = 0.0
    
    while remaining_balance > 0 and period < params.term_months:
        period += 1
        
        # 计算利息
        interest = remaining_balance * r
        
        # 计算还款
        payment = base_payment + extra_payment
        
        # 添加一次性还款
        if period == lump_sum_period and lump_sum > 0:
            payment += lump_sum
        
        # 计算本金部分
        principal_payment = payment - interest
        
        # 确保不超过剩余本金
        if principal_payment > remaining_balance:
            principal_payment = remaining_balance
            payment = principal_payment + interest
        
        # 更新余额和累计利息
        remaining_balance -= principal_payment
        new_total_interest += interest
    
    # 计算新期限（考虑提前还清）
    new_term_months = period
    
    # 计算节省
    months_saved = params.term_months - new_term_months
    interest_saved = original_interest - new_total_interest
    
    # 计算还款日期
    def add_months(date_str: str, months: int) -> str:
        """计算 N 个月后的日期"""
        from datetime import datetime
        date = datetime.strptime(date_str, "%Y-%m-%d")
        year = date.year + (date.month + months - 1) // 12
        month = (date.month + months - 1) % 12 + 1
        return f"{year}-{month:02d}-{date.day:02d}"
    
    payoff_date_original = add_months(start_date, params.term_months)
    payoff_date_new = add_months(start_date, new_term_months)
    
    return EarlyPayoffResult(
        original_term_months=params.term_months,
        new_term_months=new_term_months,
        months_saved=months_saved,
        original_total_interest=original_interest,
        new_total_interest=new_total_interest,
        interest_saved=interest_saved,
        payoff_date_original=payoff_date_original,
        payoff_date_new=payoff_date_new,
    )


# =============================================================================
# 再融资分析
# =============================================================================

def analyze_refinance(
    original_params: LoanParams,
    new_rate: float,
    new_term_months: int,
    closing_costs: float = 0,
    remaining_balance: Optional[float] = None,
    periods_paid: int = 0
) -> RefinanceResult:
    """
    分析再融资（转贷）是否划算
    
    Args:
        original_params: 原贷款参数
        new_rate: 新贷款年利率
        new_term_months: 新贷款期限
        closing_costs: 再融资成本（手续费等）
        remaining_balance: 当前剩余本金（默认为原本金）
        periods_paid: 已还款期数
    
    Returns:
        再融资分析结果
    
    Example:
        >>> original = LoanParams(principal=200000, annual_rate=6, term_months=360)
        >>> result = analyze_refinance(original, new_rate=4.5, new_term_months=360,
        ...                             closing_costs=5000)
        >>> result.monthly_savings > 0  # 利率下降，月供减少
        True
    """
    # 计算剩余本金
    if remaining_balance is None:
        if periods_paid > 0:
            schedule = generate_amortization_schedule(original_params)
            remaining_balance = schedule[periods_paid - 1].balance
        else:
            remaining_balance = original_params.principal
    
    # 原贷款剩余利息
    remaining_original_schedule = []
    P_orig = remaining_balance
    r_orig = monthly_rate(original_params.annual_rate)
    n_remaining = original_params.term_months - periods_paid
    
    if original_params.payment_type == PaymentType.EQUAL_PAYMENT:
        orig_payment = calculate_equal_payment(original_params)
        for p in range(n_remaining):
            interest = P_orig * r_orig
            principal = orig_payment - interest
            P_orig -= principal
            remaining_original_schedule.append({'interest': interest, 'payment': orig_payment})
    else:
        # 等额本金
        principal_per = remaining_balance / n_remaining
        for p in range(n_remaining):
            interest = P_orig * r_orig
            payment = principal_per + interest
            P_orig -= principal_per
            remaining_original_schedule.append({'interest': interest, 'payment': payment})
    
    original_remaining_interest = sum(s['interest'] for s in remaining_original_schedule)
    original_payment = remaining_original_schedule[0]['payment']
    
    # 新贷款分析
    new_params = LoanParams(
        principal=remaining_balance,
        annual_rate=new_rate,
        term_months=new_term_months,
        payment_type=original_params.payment_type,
    )
    
    new_summary = calculate_loan_summary(new_params)
    new_payment = new_summary.monthly_payment
    
    # 计算节省
    monthly_savings = original_payment - new_payment
    total_savings = original_remaining_interest - new_summary.total_interest
    
    # 盈亏平衡点（考虑成本）
    if monthly_savings > 0:
        break_even_months = int(closing_costs / monthly_savings) if monthly_savings > 0 else 0
    else:
        break_even_months = float('inf')
    
    net_savings = total_savings - closing_costs
    is_worth_it = net_savings > 0 and break_even_months < new_term_months
    
    # 原贷款汇总（基于剩余部分）
    original_summary = LoanSummary(
        principal=remaining_balance,
        total_payments=sum(s['payment'] for s in remaining_original_schedule),
        total_interest=original_remaining_interest,
        total_principal=remaining_balance,
        number_of_payments=n_remaining,
        monthly_payment=original_payment,
        effective_rate=original_params.annual_rate / 100,
        apr=original_params.annual_rate / 100,
    )
    
    return RefinanceResult(
        original_loan=original_summary,
        new_loan=new_summary,
        monthly_savings=monthly_savings,
        total_savings=total_savings,
        break_even_months=break_even_months,
        closing_costs=closing_costs,
        net_savings=net_savings,
        is_worth_it=is_worth_it,
    )


# =============================================================================
# 利息计算
# =============================================================================

def calculate_simple_interest(
    principal: float,
    rate: float,
    time_years: float
) -> float:
    """
    计算单利
    
    公式: I = P * r * t
    
    Args:
        principal: 本金
        rate: 年利率（百分比）
        time_years: 时间（年）
    
    Returns:
        利息
    
    Example:
        >>> calculate_simple_interest(10000, 5, 2)
        1000.0
    """
    return principal * (rate / 100) * time_years


def calculate_compound_interest(
    principal: float,
    rate: float,
    time_years: float,
    compounds_per_year: int = 12
) -> float:
    """
    计算复利
    
    公式: A = P * (1 + r/n)^(n*t)
    
    Args:
        principal: 本金
        rate: 年利率（百分比）
        time_years: 时间（年）
        compounds_per_year: 每年复利次数
    
    Returns:
        总利息
    
    Example:
        >>> calculate_compound_interest(10000, 5, 2)
        1049.41...
    """
    r = rate / 100
    n = compounds_per_year
    t = time_years
    
    amount = principal * (1 + r / n) ** (n * t)
    return amount - principal


def calculate_future_value(
    principal: float,
    rate: float,
    time_years: float,
    compounds_per_year: int = 12,
    contributions: float = 0
) -> float:
    """
    计算未来价值
    
    Args:
        principal: 初始本金
        rate: 年利率（百分比）
        time_years: 时间（年）
        compounds_per_year: 每年复利次数
        contributions: 每期额外投入
    
    Returns:
        未来价值
    
    Example:
        >>> calculate_future_value(10000, 5, 10, contributions=100)
        30356.6...
    """
    r = rate / 100
    n = compounds_per_year
    t = time_years
    
    # 本金的复利增长
    fv_principal = principal * (1 + r / n) ** (n * t)
    
    # 定期投入的未来价值
    if contributions > 0:
        # 使用年金公式
        fv_contributions = contributions * ((1 + r / n) ** (n * t) - 1) / (r / n)
        return fv_principal + fv_contributions
    
    return fv_principal


def calculate_present_value(
    future_value: float,
    rate: float,
    time_years: float,
    compounds_per_year: int = 12
) -> float:
    """
    计算现值
    
    Args:
        future_value: 未来价值
        rate: 年利率（百分比）
        time_years: 时间（年）
        compounds_per_year: 每年复利次数
    
    Returns:
        现值
    
    Example:
        >>> calculate_present_value(10000, 5, 2)
        9057.3...
    """
    r = rate / 100
    n = compounds_per_year
    t = time_years
    
    return future_value / (1 + r / n) ** (n * t)


# =============================================================================
# 贷款比较
# =============================================================================

def compare_loans(loans: List[LoanParams]) -> Dict[str, Any]:
    """
    比较多个贷款方案
    
    Args:
        loans: 贉款参数列表
    
    Returns:
        比较结果
    
    Example:
        >>> loan1 = LoanParams(principal=100000, annual_rate=5, term_months=12)
        >>> loan2 = LoanParams(principal=100000, annual_rate=4.5, term_months=24)
        >>> result = compare_loans([loan1, loan2])
        >>> result['cheapest_total']['index']
        0
    """
    summaries = [calculate_loan_summary(loan) for loan in loans]
    
    # 找出最低月供
    min_payment_idx = min(range(len(summaries)), key=lambda i: summaries[i].monthly_payment)
    
    # 找出最低总利息
    min_interest_idx = min(range(len(summaries)), key=lambda i: summaries[i].total_interest)
    
    # 找出最低总成本
    min_total_idx = min(range(len(summaries)), key=lambda i: summaries[i].total_payments)
    
    # 最短期限
    min_term_idx = min(range(len(loans)), key=lambda i: loans[i].term_months)
    
    return {
        'loans': [s.to_dict() for s in summaries],
        'lowest_monthly_payment': {
            'index': min_payment_idx,
            'payment': summaries[min_payment_idx].monthly_payment,
        },
        'lowest_interest': {
            'index': min_interest_idx,
            'interest': summaries[min_interest_idx].total_interest,
        },
        'cheapest_total': {
            'index': min_total_idx,
            'total': summaries[min_total_idx].total_payments,
        },
        'shortest_term': {
            'index': min_term_idx,
            'months': loans[min_term_idx].term_months,
        },
    }


# =============================================================================
# 房贷专用计算器
# =============================================================================

def mortgage_qualification(
    annual_income: float,
    monthly_debt: float,
    down_payment: float,
    interest_rate: float,
    term_years: int = 30,
    dti_limit: float = 0.36,  # 债务收入比上限
    ltv_limit: float = 0.80,  # 贷款价值比上限
) -> Dict[str, Any]:
    """
    房贷资格计算
    
    Args:
        annual_income: 年收入
        monthly_debt: 每月现有债务
        down_payment: 首付款
        interest_rate: 年利率
        term_years: 贉款年限
        dti_limit: 债务收入比上限
        ltv_limit: 贉款价值比上限
    
    Returns:
        贉款资格信息
    
    Example:
        >>> result = mortgage_qualification(120000, 500, 50000, 5)
        >>> result['max_loan_amount'] > 0
        True
    """
    monthly_income = annual_income / 12
    
    # 根据债务收入比计算最大月供
    max_monthly_payment = monthly_income * dti_limit - monthly_debt
    
    # 计算最大贷款金额
    r = monthly_rate(interest_rate)
    n = term_years * 12
    
    if r == 0:
        max_loan_by_dti = max_monthly_payment * n
    else:
        max_loan_by_dti = max_monthly_payment * ((1 + r) ** n - 1) / (r * (1 + r) ** n)
    
    # 根据首付计算最大房价（假设 LTV 限制）
    max_home_price_by_down = down_payment / (1 - ltv_limit)
    max_loan_by_ltv = max_home_price_by_down * ltv_limit
    
    # 取两者最小值
    max_loan_amount = min(max_loan_by_dti, max_loan_by_ltv)
    max_home_price = max_loan_amount + down_payment
    
    # 计算实际月供
    actual_monthly_payment = calculate_equal_payment(LoanParams(
        principal=max_loan_amount,
        annual_rate=interest_rate,
        term_months=n,
    ))
    
    # 计算 DTI
    actual_dti = (actual_monthly_payment + monthly_debt) / monthly_income
    
    return {
        'max_loan_amount': round(max_loan_amount, 2),
        'max_home_price': round(max_home_price, 2),
        'max_monthly_payment': round(max_monthly_payment, 2),
        'actual_monthly_payment': round(actual_monthly_payment, 2),
        'debt_to_income_ratio': round(actual_dti * 100, 2),
        'loan_to_value_ratio': round((max_loan_amount / max_home_price) * 100, 2),
        'qualified': actual_dti <= dti_limit,
    }


def calculate_down_payment_options(
    home_price: float,
    interest_rate: float,
    term_years: int = 30,
    down_payment_percentages: List[float] = [5, 10, 15, 20]
) -> List[Dict[str, Any]]:
    """
    计算不同首付比例下的贷款方案
    
    Args:
        home_price: 房价
        interest_rate: 年利率
        term_years: 贉款年限
        down_payment_percentages: 首付比例列表
    
    Returns:
        不同首付方案列表
    
    Example:
        >>> options = calculate_down_payment_options(500000, 5)
        >>> len(options) == 4
        True
        >>> options[-1]['down_payment'] > options[0]['down_payment']
        True
    """
    options = []
    
    for pct in down_payment_percentages:
        down_payment = home_price * (pct / 100)
        loan_amount = home_price - down_payment
        
        params = LoanParams(
            principal=home_price,
            annual_rate=interest_rate,
            term_months=term_years * 12,
            down_payment=down_payment,
        )
        
        summary = calculate_loan_summary(params)
        
        options.append({
            'down_payment_percent': pct,
            'down_payment': round(down_payment, 2),
            'loan_amount': round(loan_amount, 2),
            'monthly_payment': round(summary.monthly_payment, 2),
            'total_interest': round(summary.total_interest, 2),
            'total_cost': round(summary.total_payments + down_payment, 2),
        })
    
    return options


# =============================================================================
# 便捷函数
# =============================================================================

def monthly_payment(principal: float, annual_rate: float, term_months: int) -> float:
    """
    快速计算月供（等额本息）
    
    Args:
        principal: 贉款本金
        annual_rate: 年利率（百分比）
        term_months: 期限（月）
    
    Returns:
        月供
    
    Example:
        >>> monthly_payment(100000, 5, 12)
        8560.7488...
    """
    params = LoanParams(principal=principal, annual_rate=annual_rate, term_months=term_months)
    return calculate_equal_payment(params)


def total_interest(principal: float, annual_rate: float, term_months: int) -> float:
    """
    快速计算总利息
    
    Args:
        principal: 贉款本金
        annual_rate: 年利率（百分比）
        term_months: 期限（月）
    
    Returns:
        总利息
    
    Example:
        >>> total_interest(100000, 5, 12)
        2728.98...
    """
    params = LoanParams(principal=principal, annual_rate=annual_rate, term_months=term_months)
    summary = calculate_loan_summary(params)
    return summary.total_interest


def loan_table(principal: float, annual_rate: float, term_months: int) -> List[Dict]:
    """
    快速生成还款计划表
    
    Args:
        principal: 贉款本金
        annual_rate: 年利率（百分比）
        term_months: 期限（月）
    
    Returns:
        还款计划列表（字典形式）
    
    Example:
        >>> table = loan_table(10000, 6, 12)
        >>> len(table) == 12
        True
    """
    params = LoanParams(principal=principal, annual_rate=annual_rate, term_months=term_months)
    schedule = generate_amortization_schedule(params)
    return [item.to_dict() for item in schedule]


# =============================================================================
# 导出
# =============================================================================

__all__ = [
    # Enums
    'PaymentFrequency',
    'PaymentType',
    'InterestType',
    # Data Classes
    'LoanParams',
    'PaymentScheduleItem',
    'LoanSummary',
    'EarlyPayoffResult',
    'RefinanceResult',
    # 基础计算
    'monthly_rate',
    'periodic_rate',
    'periods_per_year',
    # 月供计算
    'calculate_equal_payment',
    'calculate_equal_principal_payment',
    'calculate_interest_only_payment',
    'calculate_payment',
    # 还款计划
    'generate_amortization_schedule',
    'calculate_loan_summary',
    # APR
    'calculate_apr',
    # 提前还款
    'analyze_early_payoff',
    # 再融资
    'analyze_refinance',
    # 利息计算
    'calculate_simple_interest',
    'calculate_compound_interest',
    'calculate_future_value',
    'calculate_present_value',
    # 贷款比较
    'compare_loans',
    # 房贷专用
    'mortgage_qualification',
    'calculate_down_payment_options',
    # 便捷函数
    'monthly_payment',
    'total_interest',
    'loan_table',
]


# =============================================================================
# 示例
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Loan Calculator Utils - 贷款计算工具")
    print("=" * 60)
    
    # 基础月供计算
    print("\n1. 等额本息月供计算:")
    params = LoanParams(principal=100000, annual_rate=5, term_months=12)
    payment = calculate_equal_payment(params)
    print(f"  贉款 10 万，年利率 5%，12 期")
    print(f"  月供: ¥{payment:.2f}")
    
    # 贉款汇总
    print("\n2. 贉款汇总:")
    summary = calculate_loan_summary(params)
    print(f"  总还款: ¥{summary.total_payments:.2f}")
    print(f"  总利息: ¥{summary.total_interest:.2f}")
    print(f"  期数: {summary.number_of_payments}")
    
    # 还款计划
    print("\n3. 前 3 期还款计划:")
    schedule = generate_amortization_schedule(params)
    for item in schedule[:3]:
        print(f"  第 {item.period} 期: 还款 ¥{item.payment:.2f}, "
              f"本金 ¥{item.principal:.2f}, 利息 ¥{item.interest:.2f}, "
              f"余额 ¥{item.balance:.2f}")
    
    # 等额本金
    print("\n4. 等额本金还款:")
    params_equal = LoanParams(
        principal=100000, annual_rate=5, term_months=12,
        payment_type=PaymentType.EQUAL_PRINCIPAL
    )
    payments = calculate_equal_principal_payment(params_equal)
    print(f"  第一期: ¥{payments[0]:.2f}")
    print(f"  最后一期: ¥{payments[-1]:.2f}")
    summary_equal = calculate_loan_summary(params_equal)
    print(f"  总利息: ¥{summary_equal.total_interest:.2f} (比等额本息少)")
    
    # 提前还款分析
    print("\n5. 提前还款分析:")
    params_30yr = LoanParams(principal=200000, annual_rate=5, term_months=360)
    result = analyze_early_payoff(params_30yr, extra_payment=200)
    print(f"  每月额外还款 ¥200")
    print(f"  节省期限: {result.months_saved} 个月")
    print(f"  节省利息: ¥{result.interest_saved:.2f}")
    
    # 再融资分析
    print("\n6. 再融资分析:")
    original = LoanParams(principal=200000, annual_rate=6, term_months=360)
    refinance = analyze_refinance(original, new_rate=4.5, new_term_months=360, closing_costs=5000)
    print(f"  月供节省: ¥{refinance.monthly_savings:.2f}")
    print(f"  总利息节省: ¥{refinance.total_savings:.2f}")
    print(f"  盈亏平衡点: {refinance.break_even_months} 个月")
    print(f"  是否划算: {refinance.is_worth_it}")
    
    # 房贷资格
    print("\n7. 房贷资格计算:")
    qualification = mortgage_qualification(
        annual_income=120000, monthly_debt=500, down_payment=50000, interest_rate=5
    )
    print(f"  年收入 ¥120,000, 首付 ¥50,000")
    print(f"  最大贷款: ¥{qualification['max_loan_amount']:.2f}")
    print(f"  最大房价: ¥{qualification['max_home_price']:.2f}")
    print(f"  月供: ¥{qualification['actual_monthly_payment']:.2f}")
    print(f"  DTI: {qualification['debt_to_income_ratio']}%")
    
    # 首付方案比较
    print("\n8. 不同首付方案:")
    options = calculate_down_payment_options(500000, 5)
    for opt in options:
        print(f"  {opt['down_payment_percent']}% 首付: ¥{opt['down_payment']:.0f}, "
              f"月供 ¥{opt['monthly_payment']:.0f}, 总利息 ¥{opt['total_interest']:.0f}")
    
    print("\n" + "=" * 60)