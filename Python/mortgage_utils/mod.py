"""
Mortgage Calculator Utils - 房贷计算工具模块

提供房贷计算功能，包括等额本息、等额本金计算，
支持提前还款模拟、还款计划生成等功能。

零外部依赖，纯 Python 标准库实现。
"""

from typing import List, Dict, Tuple, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import date, timedelta
from calendar import monthrange
import math


class RepaymentMethod(Enum):
    """还款方式枚举"""
    EQUAL_PRINCIPAL_INTEREST = "equal_principal_interest"  # 等额本息
    EQUAL_PRINCIPAL = "equal_principal"  # 等额本金


class PrepaymentType(Enum):
    """提前还款类型"""
    REDUCE_TERM = "reduce_term"  # 缩短年限，月供不变
    REDUCE_PAYMENT = "reduce_payment"  # 减少月供，年限不变


@dataclass
class MonthlyPayment:
    """月供详情"""
    period: int  # 期数（第几月）
    payment: float  # 月供金额
    principal: float  # 本金部分
    interest: float  # 利息部分
    remaining_principal: float  # 剩余本金
    date: Optional[date] = None  # 还款日期（可选）


@dataclass
class MortgageResult:
    """房贷计算结果"""
    principal: float  # 贷款本金
    annual_rate: float  # 年利率（百分比）
    years: int  # 贷款年限
    method: RepaymentMethod  # 还款方式
    
    # 计算结果
    total_months: int  # 总期数
    total_payment: float  # 还款总额
    total_interest: float  # 总利息
    first_month_payment: float  # 首月月供
    last_month_payment: float  # 末月月供
    monthly_payments: List[MonthlyPayment]  # 每月还款详情
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "principal": self.principal,
            "annual_rate": self.annual_rate,
            "years": self.years,
            "method": self.method.value,
            "total_months": self.total_months,
            "total_payment": round(self.total_payment, 2),
            "total_interest": round(self.total_interest, 2),
            "first_month_payment": round(self.first_month_payment, 2),
            "last_month_payment": round(self.last_month_payment, 2),
            "payment_count": len(self.monthly_payments)
        }
    
    def get_summary(self) -> str:
        """获取摘要文本"""
        method_name = "等额本息" if self.method == RepaymentMethod.EQUAL_PRINCIPAL_INTEREST else "等额本金"
        summary = f"""
房贷计算结果 ({method_name})
=====================================
贷款本金: {self.principal:,.2f} 元
年利率: {self.annual_rate:.2f}%
贷款年限: {self.years} 年 ({self.total_months} 期)
-------------------------------------
还款总额: {self.total_payment:,.2f} 元
利息总额: {self.total_interest:,.2f} 元
利息占比: {(self.total_interest / self.principal * 100):.2f}%
-------------------------------------
首月月供: {self.first_month_payment:,.2f} 元
末月月供: {self.last_month_payment:,.2f} 元
=====================================
"""
        return summary.strip()


@dataclass
class PrepaymentResult:
    """提前还款计算结果"""
    prepayment_amount: float  # 提前还款金额
    prepayment_month: int  # 提前还款月份
    original_remaining: float  # 原剩余本金
    new_remaining: float  # 新剩余本金
    
    # 选择缩短年限
    new_total_months: Optional[int] = None  # 新总期数
    months_saved: Optional[int] = None  # 节省月数
    interest_saved_term: Optional[float] = None  # 节省利息
    
    # 选择减少月供
    new_monthly_payment: Optional[float] = None  # 新月供
    payment_before: Optional[float] = None  # 原月供
    interest_saved_payment: Optional[float] = None  # 节省利息
    
    prepayment_type: PrepaymentType = PrepaymentType.REDUCE_TERM
    
    def to_dict(self) -> dict:
        """转换为字典"""
        result = {
            "prepayment_amount": self.prepayment_amount,
            "prepayment_month": self.prepayment_month,
            "original_remaining": round(self.original_remaining, 2),
            "new_remaining": round(self.new_remaining, 2),
            "prepayment_type": self.prepayment_type.value
        }
        if self.prepayment_type == PrepaymentType.REDUCE_TERM:
            result.update({
                "new_total_months": self.new_total_months,
                "months_saved": self.months_saved,
                "interest_saved": round(self.interest_saved_term, 2) if self.interest_saved_term else 0
            })
        else:
            result.update({
                "new_monthly_payment": round(self.new_monthly_payment, 2) if self.new_monthly_payment else 0,
                "payment_before": round(self.payment_before, 2) if self.payment_before else 0,
                "interest_saved": round(self.interest_saved_payment, 2) if self.interest_saved_payment else 0
            })
        return result


def calculate_monthly_rate(annual_rate: float) -> float:
    """
    将年利率转换为月利率
    
    Args:
        annual_rate: 年利率（百分比，如 4.2 表示 4.2%）
    
    Returns:
        月利率（小数形式）
    """
    return annual_rate / 100 / 12


def calculate_equal_principal_interest(
    principal: float,
    annual_rate: float,
    years: int,
    start_date: Optional[date] = None
) -> MortgageResult:
    """
    等额本息计算
    
    每月还款金额固定，包含本金和利息。
    适合收入稳定、计划长期还款的借款人。
    
    公式：月供 = 本金 × [月利率 × (1+月利率)^期数] / [(1+月利率)^期数 - 1]
    
    Args:
        principal: 贷款本金（元）
        annual_rate: 年利率（百分比）
        years: 贷款年限
        start_date: 开始还款日期（可选，用于生成还款计划表）
    
    Returns:
        MortgageResult 计算结果
    """
    if principal <= 0:
        raise ValueError("贷款本金必须大于0")
    if annual_rate < 0:
        raise ValueError("年利率不能为负")
    if years <= 0:
        raise ValueError("贷款年限必须大于0")
    
    total_months = years * 12
    monthly_rate = calculate_monthly_rate(annual_rate)
    
    # 计算月供
    if monthly_rate == 0:
        # 零利率情况
        monthly_payment = principal / total_months
    else:
        monthly_payment = principal * (
            monthly_rate * math.pow(1 + monthly_rate, total_months)
        ) / (
            math.pow(1 + monthly_rate, total_months) - 1
        )
    
    # 生成还款计划
    monthly_payments = []
    remaining_principal = principal
    current_date = start_date
    
    for period in range(1, total_months + 1):
        # 计算当期利息
        interest = remaining_principal * monthly_rate
        # 计算当期本金
        principal_part = monthly_payment - interest
        # 更新剩余本金
        remaining_principal -= principal_part
        if remaining_principal < 0:
            remaining_principal = 0
        
        # 计算还款日期
        payment_date = None
        if current_date:
            if period == 1:
                payment_date = current_date
            else:
                # 下个月同一天
                year = current_date.year
                month = current_date.month + 1
                if month > 12:
                    year += 1
                    month = 1
                day = min(current_date.day, monthrange(year, month)[1])
                payment_date = date(year, month, day)
            current_date = payment_date
        
        monthly_payments.append(MonthlyPayment(
            period=period,
            payment=round(monthly_payment, 2),
            principal=round(principal_part, 2),
            interest=round(interest, 2),
            remaining_principal=round(remaining_principal, 2),
            date=payment_date
        ))
    
    # 计算总额
    total_payment = monthly_payment * total_months
    total_interest = total_payment - principal
    
    return MortgageResult(
        principal=principal,
        annual_rate=annual_rate,
        years=years,
        method=RepaymentMethod.EQUAL_PRINCIPAL_INTEREST,
        total_months=total_months,
        total_payment=round(total_payment, 2),
        total_interest=round(total_interest, 2),
        first_month_payment=round(monthly_payment, 2),
        last_month_payment=round(monthly_payment, 2),
        monthly_payments=monthly_payments
    )


def calculate_equal_principal(
    principal: float,
    annual_rate: float,
    years: int,
    start_date: Optional[date] = None
) -> MortgageResult:
    """
    等额本金计算
    
    每月还款本金固定，利息逐月递减。
    前期还款压力大，总利息较少。
    
    公式：
    每月本金 = 贷款本金 / 期数
    每月利息 = 剩余本金 × 月利率
    每月还款 = 每月本金 + 每月利息
    
    Args:
        principal: 贷款本金（元）
        annual_rate: 年利率（百分比）
        years: 贷款年限
        start_date: 开始还款日期（可选）
    
    Returns:
        MortgageResult 计算结果
    """
    if principal <= 0:
        raise ValueError("贷款本金必须大于0")
    if annual_rate < 0:
        raise ValueError("年利率不能为负")
    if years <= 0:
        raise ValueError("贷款年限必须大于0")
    
    total_months = years * 12
    monthly_rate = calculate_monthly_rate(annual_rate)
    
    # 每月固定本金
    monthly_principal = principal / total_months
    
    # 生成还款计划
    monthly_payments = []
    remaining_principal = principal
    current_date = start_date
    total_interest = 0
    
    for period in range(1, total_months + 1):
        # 计算当期利息
        interest = remaining_principal * monthly_rate
        total_interest += interest
        
        # 计算当期还款
        payment = monthly_principal + interest
        
        # 更新剩余本金
        remaining_principal -= monthly_principal
        if remaining_principal < 0:
            remaining_principal = 0
        
        # 计算还款日期
        payment_date = None
        if current_date:
            if period == 1:
                payment_date = current_date
            else:
                year = current_date.year
                month = current_date.month + 1
                if month > 12:
                    year += 1
                    month = 1
                day = min(current_date.day, monthrange(year, month)[1])
                payment_date = date(year, month, day)
            current_date = payment_date
        
        monthly_payments.append(MonthlyPayment(
            period=period,
            payment=round(payment, 2),
            principal=round(monthly_principal, 2),
            interest=round(interest, 2),
            remaining_principal=round(remaining_principal, 2),
            date=payment_date
        ))
    
    # 计算总额
    total_payment = principal + total_interest
    first_payment = monthly_payments[0].payment if monthly_payments else 0
    last_payment = monthly_payments[-1].payment if monthly_payments else 0
    
    return MortgageResult(
        principal=principal,
        annual_rate=annual_rate,
        years=years,
        method=RepaymentMethod.EQUAL_PRINCIPAL,
        total_months=total_months,
        total_payment=round(total_payment, 2),
        total_interest=round(total_interest, 2),
        first_month_payment=round(first_payment, 2),
        last_month_payment=round(last_payment, 2),
        monthly_payments=monthly_payments
    )


def calculate_mortgage(
    principal: float,
    annual_rate: float,
    years: int,
    method: RepaymentMethod = RepaymentMethod.EQUAL_PRINCIPAL_INTEREST,
    start_date: Optional[date] = None
) -> MortgageResult:
    """
    房贷计算主函数
    
    Args:
        principal: 贷款本金（元）
        annual_rate: 年利率（百分比）
        years: 贷款年限
        method: 还款方式（等额本息/等额本金）
        start_date: 开始还款日期（可选）
    
    Returns:
        MortgageResult 计算结果
    
    Examples:
        >>> result = calculate_mortgage(1000000, 4.2, 30)
        >>> print(f"月供: {result.first_month_payment:.2f}")
    """
    if method == RepaymentMethod.EQUAL_PRINCIPAL_INTEREST:
        return calculate_equal_principal_interest(principal, annual_rate, years, start_date)
    else:
        return calculate_equal_principal(principal, annual_rate, years, start_date)


def calculate_prepayment(
    mortgage_result: MortgageResult,
    prepayment_month: int,
    prepayment_amount: float,
    prepayment_type: PrepaymentType = PrepaymentType.REDUCE_TERM
) -> PrepaymentResult:
    """
    提前还款计算
    
    Args:
        mortgage_result: 原房贷计算结果
        prepayment_month: 提前还款的月份（从1开始）
        prepayment_amount: 提前还款金额
        prepayment_type: 提前还款类型（缩短年限/减少月供）
    
    Returns:
        PrepaymentResult 提前还款计算结果
    """
    if prepayment_month < 1 or prepayment_month > mortgage_result.total_months:
        raise ValueError(f"提前还款月份必须在 1-{mortgage_result.total_months} 之间")
    if prepayment_amount <= 0:
        raise ValueError("提前还款金额必须大于0")
    
    # 获取提前还款前的剩余本金
    if prepayment_month <= len(mortgage_result.monthly_payments):
        remaining_principal = mortgage_result.monthly_payments[prepayment_month - 1].remaining_principal
    else:
        remaining_principal = 0
    
    if remaining_principal <= 0:
        raise ValueError("该月份已无剩余本金可提前还款")
    
    # 限制提前还款金额不超过剩余本金
    actual_prepayment = min(prepayment_amount, remaining_principal)
    new_remaining = remaining_principal - actual_prepayment
    
    if prepayment_type == PrepaymentType.REDUCE_TERM:
        # 缩短年限模式：月供不变，计算新期限
        monthly_payment = mortgage_result.monthly_payments[0].payment
        monthly_rate = calculate_monthly_rate(mortgage_result.annual_rate)
        
        if new_remaining > 0:
            # 反向计算新期限
            # 月供 = 剩余本金 × [月利率 × (1+月利率)^期数] / [(1+月利率)^期数 - 1]
            if monthly_rate > 0:
                # 试算新期数
                new_months = 0
                for n in range(1, mortgage_result.total_months - prepayment_month + 1):
                    calc_payment = new_remaining * (
                        monthly_rate * math.pow(1 + monthly_rate, n)
                    ) / (
                        math.pow(1 + monthly_rate, n) - 1
                    )
                    if calc_payment <= monthly_payment:
                        new_months = n
                        break
                if new_months == 0:
                    new_months = mortgage_result.total_months - prepayment_month
            else:
                new_months = int(math.ceil(new_remaining / monthly_payment))
        else:
            new_months = 0
        
        original_remaining_months = mortgage_result.total_months - prepayment_month
        months_saved = original_remaining_months - new_months
        
        # 计算节省的利息
        # 原计划剩余利息 = 原剩余月供 × 原剩余月数 - 原剩余本金
        original_remaining_interest = monthly_payment * original_remaining_months - remaining_principal
        # 新计划剩余利息
        if new_months > 0 and monthly_rate > 0:
            new_remaining_interest = monthly_payment * new_months - new_remaining
        else:
            new_remaining_interest = 0
        interest_saved = original_remaining_interest - new_remaining_interest
        
        return PrepaymentResult(
            prepayment_amount=actual_prepayment,
            prepayment_month=prepayment_month,
            original_remaining=remaining_principal,
            new_remaining=new_remaining,
            new_total_months=prepayment_month + new_months,
            months_saved=months_saved,
            interest_saved_term=max(0, interest_saved),
            prepayment_type=prepayment_type
        )
    else:
        # 减少月供模式：期限不变，计算新月供
        remaining_months = mortgage_result.total_months - prepayment_month
        monthly_rate = calculate_monthly_rate(mortgage_result.annual_rate)
        
        if new_remaining > 0 and remaining_months > 0:
            if monthly_rate > 0:
                new_monthly_payment = new_remaining * (
                    monthly_rate * math.pow(1 + monthly_rate, remaining_months)
                ) / (
                    math.pow(1 + monthly_rate, remaining_months) - 1
                )
            else:
                new_monthly_payment = new_remaining / remaining_months
        else:
            new_monthly_payment = 0
        
        # 原月供
        payment_before = mortgage_result.monthly_payments[0].payment
        
        # 计算节省的利息
        # 原计划剩余利息
        original_remaining_interest = payment_before * remaining_months - remaining_principal
        # 新计划剩余利息
        new_remaining_interest = new_monthly_payment * remaining_months - new_remaining
        interest_saved = original_remaining_interest - new_remaining_interest
        
        return PrepaymentResult(
            prepayment_amount=actual_prepayment,
            prepayment_month=prepayment_month,
            original_remaining=remaining_principal,
            new_remaining=new_remaining,
            new_monthly_payment=new_monthly_payment,
            payment_before=payment_before,
            interest_saved_payment=max(0, interest_saved),
            prepayment_type=prepayment_type
        )


def calculate_affordable_loan(
    monthly_payment: float,
    annual_rate: float,
    years: int
) -> float:
    """
    根据月供反算可承受贷款额度
    
    Args:
        monthly_payment: 每月可承受还款金额
        annual_rate: 年利率（百分比）
        years: 贷款年限
    
    Returns:
        可承受贷款额度
    
    Examples:
        >>> loan = calculate_affordable_loan(5000, 4.2, 30)
        >>> print(f"可贷款: {loan:.2f}")
    """
    if monthly_payment <= 0:
        raise ValueError("月供必须大于0")
    if annual_rate < 0:
        raise ValueError("年利率不能为负")
    if years <= 0:
        raise ValueError("贷款年限必须大于0")
    
    total_months = years * 12
    monthly_rate = calculate_monthly_rate(annual_rate)
    
    if monthly_rate == 0:
        return monthly_payment * total_months
    
    # 反推公式：本金 = 月供 × [(1+月利率)^期数 - 1] / [月利率 × (1+月利率)^期数]
    principal = monthly_payment * (
        math.pow(1 + monthly_rate, total_months) - 1
    ) / (
        monthly_rate * math.pow(1 + monthly_rate, total_months)
    )
    
    return round(principal, 2)


def compare_methods(
    principal: float,
    annual_rate: float,
    years: int
) -> Dict:
    """
    对比等额本息和等额本金两种还款方式
    
    Args:
        principal: 贷款本金
        annual_rate: 年利率（百分比）
        years: 贷款年限
    
    Returns:
        对比结果字典
    """
    equal_pi = calculate_equal_principal_interest(principal, annual_rate, years)
    equal_p = calculate_equal_principal(principal, annual_rate, years)
    
    return {
        "loan_amount": principal,
        "annual_rate": annual_rate,
        "years": years,
        "equal_principal_interest": {
            "monthly_payment": equal_pi.first_month_payment,
            "total_payment": equal_pi.total_payment,
            "total_interest": equal_pi.total_interest,
            "interest_ratio": round(equal_pi.total_interest / principal * 100, 2)
        },
        "equal_principal": {
            "first_month_payment": equal_p.first_month_payment,
            "last_month_payment": equal_p.last_month_payment,
            "monthly_decrease": round(
                equal_p.first_month_payment - equal_p.last_month_payment, 2
            ),
            "total_payment": equal_p.total_payment,
            "total_interest": equal_p.total_interest,
            "interest_ratio": round(equal_p.total_interest / principal * 100, 2)
        },
        "difference": {
            "total_interest_saved": round(
                equal_pi.total_interest - equal_p.total_interest, 2
            ),
            "first_month_difference": round(
                equal_p.first_month_payment - equal_pi.first_month_payment, 2
            )
        },
        "recommendation": "等额本金总利息更少，但前期月供更高" if equal_p.total_interest < equal_pi.total_interest else "两种方式利息相同"
    }


def calculate_combined_loan(
    commercial_principal: float,
    commercial_rate: float,
    fund_principal: float,
    fund_rate: float,
    years: int,
    method: RepaymentMethod = RepaymentMethod.EQUAL_PRINCIPAL_INTEREST
) -> Dict:
    """
    组合贷款计算（公积金贷款 + 商业贷款）
    
    Args:
        commercial_principal: 商业贷款本金
        commercial_rate: 商业贷款年利率（百分比）
        fund_principal: 公积金贷款本金
        fund_rate: 公积金贷款年利率（百分比）
        years: 贷款年限
        method: 还款方式
    
    Returns:
        组合贷款计算结果
    """
    commercial = calculate_mortgage(
        commercial_principal, commercial_rate, years, method
    )
    fund = calculate_mortgage(
        fund_principal, fund_rate, years, method
    )
    
    total_principal = commercial_principal + fund_principal
    total_interest = commercial.total_interest + fund.total_interest
    total_payment = commercial.total_payment + fund.total_payment
    
    return {
        "commercial": commercial.to_dict(),
        "fund": fund.to_dict(),
        "combined": {
            "total_principal": total_principal,
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_interest, 2),
            "first_month_payment": round(
                commercial.first_month_payment + fund.first_month_payment, 2
            ),
            "last_month_payment": round(
                commercial.last_month_payment + fund.last_month_payment, 2
            )
        }
    }


def generate_payment_schedule(
    mortgage_result: MortgageResult,
    output_format: str = "text"
) -> str:
    """
    生成还款计划表
    
    Args:
        mortgage_result: 房贷计算结果
        output_format: 输出格式（"text" 或 "csv"）
    
    Returns:
        还款计划表文本
    """
    lines = []
    
    if output_format == "csv":
        lines.append("期数,月供,本金,利息,剩余本金")
        for p in mortgage_result.monthly_payments:
            lines.append(
                f"{p.period},{p.payment:.2f},{p.principal:.2f},"
                f"{p.interest:.2f},{p.remaining_principal:.2f}"
            )
    else:
        method_name = "等额本息" if mortgage_result.method == RepaymentMethod.EQUAL_PRINCIPAL_INTEREST else "等额本金"
        lines.append(f"\n还款计划表 ({method_name})")
        lines.append("=" * 65)
        lines.append(
            f"{'期数':^6} | {'月供':^12} | {'本金':^12} | {'利息':^12} | {'剩余本金':^12}"
        )
        lines.append("-" * 65)
        
        for p in mortgage_result.monthly_payments[:12]:  # 只显示前12期
            lines.append(
                f"{p.period:^6} | {p.payment:>12,.2f} | {p.principal:>12,.2f} | "
                f"{p.interest:>12,.2f} | {p.remaining_principal:>12,.2f}"
            )
        
        if len(mortgage_result.monthly_payments) > 12:
            lines.append("..." + f" (共 {len(mortgage_result.monthly_payments)} 期)")
        
        lines.append("=" * 65)
    
    return "\n".join(lines)


def estimate_payoff_time(
    principal: float,
    annual_rate: float,
    monthly_payment: float,
    method: RepaymentMethod = RepaymentMethod.EQUAL_PRINCIPAL_INTEREST
) -> Dict:
    """
    根据月供估算还清时间
    
    Args:
        principal: 贷款本金
        annual_rate: 年利率
        monthly_payment: 每月还款金额
        method: 还款方式
    
    Returns:
        估算结果
    """
    monthly_rate = calculate_monthly_rate(annual_rate)
    
    if monthly_rate > 0:
        # 等额本息反向计算
        if monthly_payment <= principal * monthly_rate:
            return {
                "status": "月供不足以覆盖月利息",
                "months": None,
                "years": None,
                "total_interest": None
            }
        
        # 计算期数：月供 = 本金 × [月利率 × (1+月利率)^期数] / [(1+月利率)^期数 - 1]
        # 反推：期数 = log(月供 / (月供 - 本金 × 月利率)) / log(1 + 月利率)
        months = math.log(
            monthly_payment / (monthly_payment - principal * monthly_rate)
        ) / math.log(1 + monthly_rate)
        months = math.ceil(months)
    else:
        months = math.ceil(principal / monthly_payment)
    
    years = months / 12
    total_payment = monthly_payment * months
    total_interest = total_payment - principal
    
    return {
        "status": "可还清",
        "months": months,
        "years": round(years, 1),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
        "last_payment": round(total_payment - monthly_payment * (months - 1), 2)
    }


if __name__ == "__main__":
    # 示例用法
    print("=" * 60)
    print("房贷计算工具示例")
    print("=" * 60)
    
    # 1. 等额本息计算
    print("\n【等额本息】贷款 100 万，利率 4.2%，30 年")
    result1 = calculate_mortgage(1000000, 4.2, 30, RepaymentMethod.EQUAL_PRINCIPAL_INTEREST)
    print(result1.get_summary())
    
    # 2. 等额本金计算
    print("\n【等额本金】贷款 100 万，利率 4.2%，30 年")
    result2 = calculate_mortgage(1000000, 4.2, 30, RepaymentMethod.EQUAL_PRINCIPAL)
    print(result2.get_summary())
    
    # 3. 两种方式对比
    print("\n【还款方式对比】")
    comparison = compare_methods(1000000, 4.2, 30)
    print(f"等额本息总利息: {comparison['equal_principal_interest']['total_interest']:,.2f}")
    print(f"等额本金总利息: {comparison['equal_principal']['total_interest']:,.2f}")
    print(f"利息差额: {comparison['difference']['total_interest_saved']:,.2f}")
    
    # 4. 提前还款计算
    print("\n【提前还款】第 12 期提前还款 10 万（缩短年限）")
    prepay = calculate_prepayment(result1, 12, 100000, PrepaymentType.REDUCE_TERM)
    print(f"提前还款金额: {prepay.prepayment_amount:,.2f}")
    print(f"节省利息: {prepay.interest_saved_term:,.2f}")
    print(f"节省月数: {prepay.months_saved}")
    
    # 5. 反算可贷款额度
    print("\n【反算贷款额度】月供 5000，利率 4.2%，30 年")
    loan = calculate_affordable_loan(5000, 4.2, 30)
    print(f"可贷款额度: {loan:,.2f}")
    
    # 6. 组合贷款
    print("\n【组合贷款】商业贷 70 万(4.2%) + 公积金 30 万(3.1%)，30 年")
    combined = calculate_combined_loan(700000, 4.2, 300000, 3.1, 30)
    print(f"首月月供: {combined['combined']['first_month_payment']:,.2f}")
    print(f"总利息: {combined['combined']['total_interest']:,.2f}")
    
    # 7. 还款计划表
    print("\n【还款计划表（前 12 期）】")
    print(generate_payment_schedule(result1))