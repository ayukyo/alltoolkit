"""
房贷计算工具 - 高级用法示例

演示提前还款计算、组合贷款等高级功能。
"""

import sys
import os
# 添加正确的路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mortgage_utils.mod import (
    calculate_mortgage,
    calculate_prepayment,
    calculate_affordable_loan,
    calculate_combined_loan,
    generate_payment_schedule,
    estimate_payoff_time,
    RepaymentMethod,
    PrepaymentType
)
from datetime import date


def example_prepayment_reduce_term():
    """示例: 提前还款 - 缩短年限"""
    print("\n" + "=" * 60)
    print("示例: 提前还款 - 缩短年限模式")
    print("=" * 60)
    
    # 原贷款：100 万，4.2%，30 年
    result = calculate_mortgage(1000000, 4.2, 30, RepaymentMethod.EQUAL_PRINCIPAL_INTEREST)
    print(f"\n原贷款信息:")
    print(f"  本金: {result.principal:,} 元")
    print(f"  月供: {result.first_month_payment:,.2f} 元")
    print(f"  总期数: {result.total_months} 期")
    print(f"  总利息: {result.total_interest:,.2f} 元")
    
    # 模拟不同时间点提前还款
    scenarios = [
        (12, 100000, "第 1 年末提前还款 10 万"),
        (36, 200000, "第 3 年末提前还款 20 万"),
        (60, 300000, "第 5 年末提前还款 30 万"),
    ]
    
    print("\n提前还款方案对比:")
    for month, amount, desc in scenarios:
        prepay = calculate_prepayment(result, month, amount, PrepaymentType.REDUCE_TERM)
        
        print(f"\n【{desc}】")
        print(f"  原剩余本金: {prepay.original_remaining:,.2f} 元")
        print(f"  新剩余本金: {prepay.new_remaining:,.2f} 元")
        print(f"  原剩余期数: {result.total_months - month} 期")
        print(f"  新剩余期数: {prepay.new_total_months - month} 期")
        print(f"  节省月数: {prepay.months_saved} 个月 ({prepay.months_saved // 12} 年 {prepay.months_saved % 12} 个月)")
        print(f"  节省利息: {prepay.interest_saved_term:,.2f} 元")


def example_prepayment_reduce_payment():
    """示例: 提前还款 - 减少月供"""
    print("\n" + "=" * 60)
    print("示例: 提前还款 - 减少月供模式")
    print("=" * 60)
    
    # 原贷款
    result = calculate_mortgage(1000000, 4.2, 30, RepaymentMethod.EQUAL_PRINCIPAL_INTEREST)
    
    # 第 12 个月提前还款 10 万
    prepay = calculate_prepayment(result, 12, 100000, PrepaymentType.REDUCE_PAYMENT)
    
    print(f"\n原贷款:")
    print(f"  月供: {prepay.payment_before:,.2f} 元")
    
    print(f"\n提前还款后:")
    print(f"  还款金额: {prepay.prepayment_amount:,} 元")
    print(f"  新月供: {prepay.new_monthly_payment:,.2f} 元")
    print(f"  月供减少: {prepay.payment_before - prepay.new_monthly_payment:,.2f} 元")
    print(f"  节省利息: {prepay.interest_saved_payment:,.2f} 元")


def example_combined_loan():
    """示例: 组合贷款计算"""
    print("\n" + "=" * 60)
    print("示例: 组合贷款（公积金 + 商业贷款）")
    print("=" * 60)
    
    # 房价 200 万，首付 30%，贷款 140 万
    # 公积金最高 60 万，利率 3.1%
    # 商业贷款 80 万，利率 4.2%
    
    fund_principal = 600000      # 公积金贷款
    fund_rate = 3.1               # 公积金利率
    commercial_principal = 800000 # 商业贷款
    commercial_rate = 4.2         # 商业利率
    years = 30
    
    combined = calculate_combined_loan(
        commercial_principal, commercial_rate,
        fund_principal, fund_rate,
        years
    )
    
    print(f"\n【贷款构成】")
    print(f"  公积金贷款: {fund_principal:,} 元，利率 {fund_rate}%")
    print(f"  商业贷款: {commercial_principal:,} 元，利率 {commercial_rate}%")
    print(f"  贷款总额: {combined['combined']['total_principal']:,} 元")
    print(f"  贷款年限: {years} 年")
    
    print(f"\n【还款明细】")
    print(f"  公积金月供: {combined['fund']['first_month_payment']:,.2f} 元")
    print(f"  商业贷月供: {combined['commercial']['first_month_payment']:,.2f} 元")
    print(f"  总月供: {combined['combined']['first_month_payment']:,.2f} 元")
    
    print(f"\n【利息明细】")
    print(f"  公积金利息: {combined['fund']['total_interest']:,.2f} 元")
    print(f"  商业贷利息: {combined['commercial']['total_interest']:,.2f} 元")
    print(f"  总利息: {combined['combined']['total_interest']:,.2f} 元")
    
    # 对比纯商业贷款
    print(f"\n【对比纯商业贷款】")
    pure_commercial = calculate_mortgage(
        combined['combined']['total_principal'],
        commercial_rate,
        years
    )
    interest_saved = pure_commercial.total_interest - combined['combined']['total_interest']
    print(f"  纯商业贷利息: {pure_commercial.total_interest:,.2f} 元")
    print(f"  组合贷利息: {combined['combined']['total_interest']:,.2f} 元")
    print(f"  节省利息: {interest_saved:,.2f} 元")


def example_affordable_loan():
    """示例: 根据月供反算可贷款额度"""
    print("\n" + "=" * 60)
    print("示例: 根据月供反算可贷款额度")
    print("=" * 60)
    
    scenarios = [
        (3000, 4.2, 20, "月供 3000"),
        (5000, 4.2, 25, "月供 5000"),
        (8000, 3.5, 30, "月供 8000，公积金利率"),
        (10000, 4.2, 30, "月供 10000"),
    ]
    
    print("\n根据不同月供计算的贷款额度:\n")
    print(f"{'场景':^20} | {'利率':^8} | {'年限':^6} | {'可贷款额':^14}")
    print("-" * 60)
    
    for monthly, rate, years, desc in scenarios:
        loan = calculate_affordable_loan(monthly, rate, years)
        print(f"{desc:^20} | {rate:^8.1f}% | {years:^6}年 | {loan:>14,.2f}")


def example_payment_schedule():
    """示例: 生成还款计划表"""
    print("\n" + "=" * 60)
    print("示例: 生成还款计划表")
    print("=" * 60)
    
    # 带起始日期的贷款计算
    start_date = date(2024, 1, 15)
    result = calculate_mortgage(
        1000000, 4.2, 30,
        RepaymentMethod.EQUAL_PRINCIPAL_INTEREST,
        start_date
    )
    
    # 显示前 6 期还款计划
    print(f"\n前 6 期还款计划:\n")
    print(f"{'期数':^4} | {'还款日':^12} | {'月供':^10} | {'本金':^10} | {'利息':^10} | {'剩余本金':^14}")
    print("-" * 75)
    
    for p in result.monthly_payments[:6]:
        date_str = p.date.strftime("%Y-%m-%d") if p.date else "-"
        print(f"{p.period:^4} | {date_str:^12} | {p.payment:>10,.2f} | {p.principal:>10,.2f} | {p.interest:>10,.2f} | {p.remaining_principal:>14,.2f}")
    
    # 导出 CSV 格式
    print(f"\nCSV 格式导出（前 3 行）:")
    csv = generate_payment_schedule(result, "csv")
    print(csv.split('\n')[0])
    print(csv.split('\n')[1])
    print(csv.split('\n')[2])


def example_payoff_estimation():
    """示例: 估算还清时间"""
    print("\n" + "=" * 60)
    print("示例: 估算还清时间")
    print("=" * 60)
    
    # 贷款 100 万，利率 4.2%
    # 不同月供下的还清时间
    
    print(f"\n贷款 100 万，利率 4.2%\n")
    print(f"{'月供':^12} | {'还清时间':^15} | {'总还款':^14} | {'总利息':^14}")
    print("-" * 65)
    
    for monthly in [4000, 5000, 6000, 8000, 10000]:
        result = estimate_payoff_time(1000000, 4.2, monthly)
        if result["status"] == "可还清":
            years = result["years"]
            months = result["months"]
            print(f"{monthly:>12,} | {years:>7.1f}年({months}月) | {result['total_payment']:>14,.2f} | {result['total_interest']:>14,.2f}")
        else:
            print(f"{monthly:>12,} | {result['status']}")
    
    # 月供不足的情况
    print("\n月供不足的情况:")
    result = estimate_payoff_time(1000000, 4.2, 3000)
    print(f"  月供 3000: {result['status']}")


if __name__ == "__main__":
    example_prepayment_reduce_term()
    example_prepayment_reduce_payment()
    example_combined_loan()
    example_affordable_loan()
    example_payment_schedule()
    example_payoff_estimation()
    
    print("\n" + "=" * 60)
    print("高级示例运行完成")
    print("=" * 60)