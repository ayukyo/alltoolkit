"""
Mortgage Calculator Utilities

A comprehensive mortgage calculation toolkit with zero external dependencies.
Supports equal principal and interest (等额本息), equal principal (等额本金),
prepayment calculations, and amortization schedule generation.

Author: AllToolkit
Date: 2026-05-10
"""

from typing import List, Dict, Tuple, Optional
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
import math


class MortgageCalculator:
    """房贷计算器 - 支持等额本息和等额本金两种还款方式"""
    
    def __init__(self, principal: float, annual_rate: float, years: int, 
                 start_date: Optional[datetime] = None):
        """
        初始化房贷计算器
        
        Args:
            principal: 贷款本金（元）
            annual_rate: 年利率（如 4.9 表示 4.9%）
            years: 贷款年限
            start_date: 还款起始日期，默认为当前月份的下个月
        """
        self.principal = Decimal(str(principal))
        self.annual_rate = Decimal(str(annual_rate)) / 100  # 转换为小数
        self.monthly_rate = self.annual_rate / 12
        self.years = years
        self.months = years * 12
        self.start_date = start_date or datetime.now()
        # 调整到下个月1号作为首次还款日
        self.first_payment_date = self._get_first_payment_date()
    
    def _add_months(self, dt: datetime, months: int) -> datetime:
        """添加月份（纯Python实现）"""
        month = dt.month - 1 + months
        year = dt.year + month // 12
        month = month % 12 + 1
        day = min(dt.day, self._days_in_month(year, month))
        return datetime(year, month, day)
    
    def _days_in_month(self, year: int, month: int) -> int:
        """获取某月的天数"""
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        return (next_month - timedelta(days=1)).day
    
    def _get_first_payment_date(self) -> datetime:
        """获取首次还款日期（下个月1号）"""
        if self.start_date.day >= 15:
            # 如果在月中之后，从再下个月开始
            return self._add_months(datetime(self.start_date.year, self.start_date.month, 1), 2)
        return self._add_months(datetime(self.start_date.year, self.start_date.month, 1), 1)
    
    def _round_money(self, value: Decimal) -> Decimal:
        """金额四舍五入到分"""
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def equal_principal_interest_monthly(self) -> Decimal:
        """
        计算等额本息每月还款额
        
        公式：月供 = 本金 × [月利率 × (1+月利率)^还款月数] ÷ [(1+月利率)^还款月数 - 1]
        
        Returns:
            每月还款金额
        """
        if self.monthly_rate == 0:
            return self._round_money(self.principal / self.months)
        
        factor = (1 + self.monthly_rate) ** self.months
        monthly_payment = self.principal * self.monthly_rate * factor / (factor - 1)
        return self._round_money(monthly_payment)
    
    def equal_principal_interest_schedule(self) -> List[Dict]:
        """
        生成等额本息还款计划表
        
        Returns:
            还款计划列表，每项包含：期数、还款日期、月供、本金、利息、剩余本金
        """
        monthly_payment = self.equal_principal_interest_monthly()
        schedule = []
        remaining_principal = self.principal
        
        for month in range(1, self.months + 1):
            # 计算当期利息
            interest = self._round_money(remaining_principal * self.monthly_rate)
            # 计算当期本金
            principal_paid = self._round_money(monthly_payment - interest)
            # 处理最后一期的尾差
            if month == self.months:
                principal_paid = remaining_principal
                monthly_payment = principal_paid + interest
            
            remaining_principal = self._round_money(remaining_principal - principal_paid)
            if remaining_principal < 0:
                remaining_principal = Decimal('0')
            
            payment_date = self._add_months(self.first_payment_date, month-1)
            
            schedule.append({
                'period': month,
                'date': payment_date.strftime('%Y-%m-%d'),
                'payment': float(monthly_payment),
                'principal': float(principal_paid),
                'interest': float(interest),
                'remaining': float(remaining_principal)
            })
        
        return schedule
    
    def equal_principal_interest_summary(self) -> Dict:
        """
        等额本息还款汇总
        
        Returns:
            包含月供、总还款、总利息、还款总额等信息的字典
        """
        schedule = self.equal_principal_interest_schedule()
        total_payment = sum(item['payment'] for item in schedule)
        total_interest = sum(item['interest'] for item in schedule)
        
        return {
            'type': '等额本息',
            'principal': float(self.principal),
            'annual_rate': float(self.annual_rate * 100),
            'years': self.years,
            'monthly_payment': float(self.equal_principal_interest_monthly()),
            'total_payment': round(total_payment, 2),
            'total_interest': round(total_interest, 2),
            'first_payment_date': self.first_payment_date.strftime('%Y-%m-%d'),
            'last_payment_date': schedule[-1]['date'] if schedule else None
        }
    
    def equal_principal_schedule(self) -> List[Dict]:
        """
        生成等额本金还款计划表
        
        等额本金：每月偿还相同本金，利息逐月递减
        
        Returns:
            还款计划列表
        """
        monthly_principal = self._round_money(self.principal / self.months)
        schedule = []
        remaining_principal = self.principal
        
        for month in range(1, self.months + 1):
            # 当期利息 = 剩余本金 × 月利率
            interest = self._round_money(remaining_principal * self.monthly_rate)
            # 当期还款 = 当期本金 + 当期利息
            payment = monthly_principal + interest
            
            remaining_principal = self._round_money(remaining_principal - monthly_principal)
            if remaining_principal < 0:
                remaining_principal = Decimal('0')
            
            payment_date = self._add_months(self.first_payment_date, month-1)
            
            schedule.append({
                'period': month,
                'date': payment_date.strftime('%Y-%m-%d'),
                'payment': float(payment),
                'principal': float(monthly_principal),
                'interest': float(interest),
                'remaining': float(remaining_principal)
            })
        
        return schedule
    
    def equal_principal_summary(self) -> Dict:
        """
        等额本金还款汇总
        
        Returns:
            包含首月还款、末月还款、总还款、总利息等信息的字典
        """
        schedule = self.equal_principal_schedule()
        total_payment = sum(item['payment'] for item in schedule)
        total_interest = sum(item['interest'] for item in schedule)
        
        return {
            'type': '等额本金',
            'principal': float(self.principal),
            'annual_rate': float(self.annual_rate * 100),
            'years': self.years,
            'monthly_principal': float(self._round_money(self.principal / self.months)),
            'first_month_payment': round(schedule[0]['payment'], 2) if schedule else 0,
            'last_month_payment': round(schedule[-1]['payment'], 2) if schedule else 0,
            'total_payment': round(total_payment, 2),
            'total_interest': round(total_interest, 2),
            'first_payment_date': self.first_payment_date.strftime('%Y-%m-%d'),
            'last_payment_date': schedule[-1]['date'] if schedule else None
        }
    
    def compare_methods(self) -> Dict:
        """
        比较等额本息和等额本金两种还款方式
        
        Returns:
            两种方式的对比分析
        """
        interest_summary = self.equal_principal_interest_summary()
        principal_summary = self.equal_principal_summary()
        
        interest_diff = interest_summary['total_interest'] - principal_summary['total_interest']
        
        return {
            'principal': float(self.principal),
            'annual_rate': float(self.annual_rate * 100),
            'years': self.years,
            'equal_principal_interest': {
                'monthly_payment': interest_summary['monthly_payment'],
                'total_payment': interest_summary['total_payment'],
                'total_interest': interest_summary['total_interest']
            },
            'equal_principal': {
                'first_month_payment': principal_summary['first_month_payment'],
                'last_month_payment': principal_summary['last_month_payment'],
                'total_payment': principal_summary['total_payment'],
                'total_interest': principal_summary['total_interest']
            },
            'comparison': {
                'interest_difference': round(interest_diff, 2),
                'equal_principal_saves': round(interest_diff, 2),
                'equal_principal_interest_monthly_fixed': True,
                'equal_principal_monthly_decreasing': True
            },
            'recommendation': '等额本金总利息更少，但初期还款压力较大；等额本息每月还款固定，适合收入稳定人群'
        }


class PrepaymentCalculator:
    """提前还款计算器"""
    
    def __init__(self, mortgage: MortgageCalculator, method: str = 'equal_principal_interest'):
        """
        初始化提前还款计算器
        
        Args:
            mortgage: 房贷计算器实例
            method: 还款方式，'equal_principal_interest' 或 'equal_principal'
        """
        self.mortgage = mortgage
        self.method = method
    
    def prepay_lump_sum(self, paid_months: int, prepay_amount: float, 
                        reduce_term: bool = False) -> Dict:
        """
        计算一次性提前还款
        
        Args:
            paid_months: 已还期数
            prepay_amount: 提前还款金额
            reduce_term: True=缩短年限保持月供不变，False=减少月供保持年限不变
        
        Returns:
            提前还款方案详情
        """
        prepay_amount = Decimal(str(prepay_amount))
        
        if self.method == 'equal_principal_interest':
            schedule = self.mortgage.equal_principal_interest_schedule()
        else:
            schedule = self.mortgage.equal_principal_schedule()
        
        # 获取当前剩余本金
        if paid_months >= len(schedule):
            return {'error': '已还期数超过总期数'}
        
        remaining_principal = Decimal(str(schedule[paid_months]['remaining']))
        
        if prepay_amount > remaining_principal:
            return {'error': '提前还款金额超过剩余本金'}
        
        # 提前还款后的新本金
        new_principal = remaining_principal - prepay_amount
        
        # 计算提前还款节省的利息
        future_interest = sum(
            Decimal(str(item['interest'])) 
            for item in schedule[paid_months:]
        )
        
        if reduce_term:
            # 缩短年限：保持月供不变，计算新期限
            if self.method == 'equal_principal_interest':
                monthly_payment = self.mortgage.equal_principal_interest_monthly()
                # 反推新期限
                if self.mortgage.monthly_rate == 0:
                    new_months = int(new_principal / monthly_payment)
                else:
                    r = self.mortgage.monthly_rate
                    # n = log(payment / (payment - P*r)) / log(1+r)
                    factor = monthly_payment / (monthly_payment - new_principal * r)
                    if factor > 0:
                        new_months = math.ceil(math.log(float(factor)) / math.log(1 + float(r)))
                    else:
                        new_months = 0
                new_months = max(1, new_months)
            else:
                # 等额本金缩短年限
                monthly_principal = self.mortgage.principal / self.mortgage.months
                new_months = int(new_principal / monthly_principal)
                new_months = max(1, new_months)
            
            # 创建新的计算器
            new_calc = MortgageCalculator(
                float(new_principal),
                float(self.mortgage.annual_rate * 100),
                max(1, new_months // 12 + (1 if new_months % 12 else 0)),
                self.mortgage.start_date
            )
            
            new_interest = sum(
                Decimal(str(item['interest'])) 
                for item in (new_calc.equal_principal_interest_schedule() 
                           if self.method == 'equal_principal_interest' 
                           else new_calc.equal_principal_schedule())
            )
            
            return {
                'type': '一次性提前还款 - 缩短年限',
                'paid_months': paid_months,
                'original_remaining': float(remaining_principal),
                'prepay_amount': float(prepay_amount),
                'new_principal': float(new_principal),
                'original_term': self.mortgage.months,
                'new_term': new_months,
                'term_saved': self.mortgage.months - paid_months - new_months,
                'original_future_interest': float(future_interest),
                'new_future_interest': float(new_interest),
                'interest_saved': float(future_interest - new_interest),
                'original_monthly_payment': float(monthly_payment) if self.method == 'equal_principal_interest' else None,
                'new_monthly_payment': float(new_calc.equal_principal_interest_monthly()) if self.method == 'equal_principal_interest' else None
            }
        else:
            # 减少月供：保持剩余期限不变
            remaining_months = self.mortgage.months - paid_months
            new_calc = MortgageCalculator(
                float(new_principal),
                float(self.mortgage.annual_rate * 100),
                max(1, remaining_months // 12 + (1 if remaining_months % 12 else 0)),
                self.mortgage.start_date
            )
            
            if self.method == 'equal_principal_interest':
                new_interest = sum(
                    Decimal(str(item['interest'])) 
                    for item in new_calc.equal_principal_interest_schedule()[:remaining_months]
                )
                original_payment = float(self.mortgage.equal_principal_interest_monthly())
                new_payment = float(new_calc.equal_principal_interest_monthly())
            else:
                new_interest = sum(
                    Decimal(str(item['interest'])) 
                    for item in new_calc.equal_principal_schedule()[:remaining_months]
                )
                original_payment = float(schedule[paid_months]['payment'])
                new_payment = float(new_calc.equal_principal_schedule()[0]['payment'])
            
            return {
                'type': '一次性提前还款 - 减少月供',
                'paid_months': paid_months,
                'original_remaining': float(remaining_principal),
                'prepay_amount': float(prepay_amount),
                'new_principal': float(new_principal),
                'remaining_term': remaining_months,
                'original_future_interest': float(future_interest),
                'new_future_interest': float(new_interest),
                'interest_saved': float(future_interest - new_interest),
                'original_monthly_payment': original_payment,
                'new_monthly_payment': round(new_payment, 2),
                'monthly_payment_saved': round(original_payment - new_payment, 2)
            }
    
    def prepay_partial_every_month(self, paid_months: int, extra_monthly: float) -> Dict:
        """
        计算每月额外还款的效果
        
        Args:
            paid_months: 已还期数
            extra_monthly: 每月额外还款金额
        
        Returns:
            提前还清效果分析
        """
        extra_monthly = Decimal(str(extra_monthly))
        
        if self.method == 'equal_principal_interest':
            schedule = self.mortgage.equal_principal_interest_schedule()
        else:
            schedule = self.mortgage.equal_principal_schedule()
        
        if paid_months >= len(schedule):
            return {'error': '已还期数超过总期数'}
        
        remaining_principal = Decimal(str(schedule[paid_months]['remaining']))
        remaining_months = self.mortgage.months - paid_months
        
        # 模拟额外还款
        new_principal = remaining_principal
        new_months = 0
        monthly_payment = self.mortgage.equal_principal_interest_monthly() if self.method == 'equal_principal_interest' else Decimal(str(schedule[paid_months]['principal']))
        total_extra = Decimal('0')
        interest_saved = Decimal('0')
        
        while new_principal > 0 and new_months < remaining_months:
            interest = new_principal * self.mortgage.monthly_rate
            principal_paid = monthly_payment - interest if self.method == 'equal_principal_interest' else monthly_payment
            total_payment = principal_paid + extra_monthly
            
            if total_payment >= new_principal:
                # 最后一期
                interest_saved += new_principal * self.mortgage.monthly_rate
                new_principal = Decimal('0')
            else:
                new_principal -= total_payment
                interest_saved += interest
            
            total_extra += extra_monthly
            new_months += 1
        
        return {
            'type': '每月额外还款',
            'paid_months': paid_months,
            'original_remaining': float(remaining_principal),
            'extra_monthly': float(extra_monthly),
            'original_remaining_term': remaining_months,
            'new_term': new_months,
            'term_saved': remaining_months - new_months,
            'total_extra_payment': float(total_extra),
            'estimated_interest_saved': float(interest_saved)
        }


def calculate_affordability(monthly_income: float, monthly_debt: float = 0,
                           annual_rate: float = 4.9, years: int = 30,
                           income_ratio: float = 0.5) -> Dict:
    """
    计算可负担的贷款金额
    
    Args:
        monthly_income: 月收入
        monthly_debt: 月负债（其他贷款月供）
        annual_rate: 年利率
        years: 贷款年限
        income_ratio: 收入负债比上限（默认50%）
    
    Returns:
        可负担贷款金额及相关信息
    """
    monthly_rate = Decimal(str(annual_rate)) / 100 / 12
    available_for_mortgage = Decimal(str(monthly_income * income_ratio - monthly_debt))
    
    if available_for_mortgage <= 0:
        return {
            'error': '当前收入不足以支持新的贷款',
            'monthly_income': monthly_income,
            'monthly_debt': monthly_debt,
            'income_ratio': income_ratio
        }
    
    if monthly_rate == 0:
        max_principal = available_for_mortgage * years * 12
    else:
        # P = M * [(1+r)^n - 1] / [r * (1+r)^n]
        months = years * 12
        factor = (1 + monthly_rate) ** months
        max_principal = available_for_mortgage * (factor - 1) / (monthly_rate * factor)
    
    return {
        'monthly_income': monthly_income,
        'monthly_debt': monthly_debt,
        'available_for_mortgage': float(available_for_mortgage),
        'income_ratio': income_ratio,
        'annual_rate': annual_rate,
        'years': years,
        'max_loan_amount': round(float(max_principal), 2),
        'estimated_monthly_payment': float(available_for_mortgage),
        'note': f'按收入{income_ratio*100:.0f}%作为还款上限计算'
    }


def calculate_lpr_spread(base_rate: float, spread: float, principal: float, 
                          years: int) -> Dict:
    """
    计算LPR利率下的房贷
    
    Args:
        base_rate: LPR基准利率（如 4.3）
        spread: 加点数（如 0.6 表示加60个基点）
        principal: 贷款本金
        years: 贷款年限
    
    Returns:
        LPR利率房贷计算结果
    """
    actual_rate = base_rate + spread
    calc = MortgageCalculator(principal, actual_rate, years)
    
    return {
        'lpr_base_rate': base_rate,
        'spread_bp': spread * 100,  # 基点
        'actual_rate': actual_rate,
        'principal': principal,
        'years': years,
        'equal_principal_interest': calc.equal_principal_interest_summary(),
        'equal_principal': calc.equal_principal_summary()
    }


def estimate_property_value(monthly_payment: float, annual_rate: float, 
                           years: int, down_payment_ratio: float = 0.3) -> Dict:
    """
    根据月供反推可购房总价
    
    Args:
        monthly_payment: 可承受的月供
        annual_rate: 年利率
        years: 贷款年限
        down_payment_ratio: 首付比例（默认30%）
    
    Returns:
        可购房总价估算
    """
    monthly_rate = Decimal(str(annual_rate)) / 100 / 12
    months = years * 12
    
    if monthly_rate == 0:
        loan_amount = Decimal(str(monthly_payment)) * months
    else:
        # P = M * [(1+r)^n - 1] / [r * (1+r)^n]
        factor = (1 + monthly_rate) ** months
        loan_amount = Decimal(str(monthly_payment)) * (factor - 1) / (monthly_rate * factor)
    
    # 房产总价 = 贷款金额 / (1 - 首付比例)
    property_value = loan_amount / (1 - Decimal(str(down_payment_ratio)))
    down_payment = property_value - loan_amount
    
    return {
        'monthly_payment': monthly_payment,
        'annual_rate': annual_rate,
        'years': years,
        'down_payment_ratio': down_payment_ratio,
        'max_loan_amount': round(float(loan_amount), 2),
        'estimated_property_value': round(float(property_value), 2),
        'down_payment': round(float(down_payment), 2),
        'note': f'假设首付{down_payment_ratio*100:.0f}%，计算可购房总价'
    }


# 便捷函数
def calc_equal_principal_interest(principal: float, annual_rate: float, 
                                  years: int) -> Dict:
    """计算等额本息还款（便捷函数）"""
    calc = MortgageCalculator(principal, annual_rate, years)
    return calc.equal_principal_interest_summary()


def calc_equal_principal(principal: float, annual_rate: float, 
                         years: int) -> Dict:
    """计算等额本金还款（便捷函数）"""
    calc = MortgageCalculator(principal, annual_rate, years)
    return calc.equal_principal_summary()


def compare_repayment_methods(principal: float, annual_rate: float, 
                              years: int) -> Dict:
    """比较两种还款方式（便捷函数）"""
    calc = MortgageCalculator(principal, annual_rate, years)
    return calc.compare_methods()


if __name__ == '__main__':
    # 示例用法
    print("=" * 60)
    print("房贷计算器示例")
    print("=" * 60)
    
    # 创建计算器：贷款100万，年利率4.9%，30年
    calc = MortgageCalculator(1000000, 4.9, 30)
    
    print("\n【等额本息还款】")
    interest_summary = calc.equal_principal_interest_summary()
    for key, value in interest_summary.items():
        print(f"  {key}: {value}")
    
    print("\n【等额本金还款】")
    principal_summary = calc.equal_principal_summary()
    for key, value in principal_summary.items():
        print(f"  {key}: {value}")
    
    print("\n【还款方式对比】")
    comparison = calc.compare_methods()
    print(f"  等额本息月供: {comparison['equal_principal_interest']['monthly_payment']:.2f} 元")
    print(f"  等额本金首月: {comparison['equal_principal']['first_month_payment']:.2f} 元")
    print(f"  等额本金末月: {comparison['equal_principal']['last_month_payment']:.2f} 元")
    print(f"  等额本金节省利息: {comparison['comparison']['equal_principal_saves']:.2f} 元")
    
    print("\n【可负担性计算】")
    affordability = calculate_affordability(15000, 2000, 4.9, 30)
    for key, value in affordability.items():
        print(f"  {key}: {value}")
    
    print("\n【根据月供反推房价】")
    estimate = estimate_property_value(5000, 4.9, 30, 0.3)
    for key, value in estimate.items():
        print(f"  {key}: {value}")