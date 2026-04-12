#!/usr/bin/env python3
"""
AllToolkit - Finance Utils Demo

演示 finance_utils 模块的各种功能。
运行：python examples/demo.py
"""

import sys
import os

# Add module to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    # 货币时间价值
    future_value, present_value, compound_interest, effective_annual_rate,
    
    # 年金
    annuity_future_value, annuity_present_value,
    
    # 贷款
    loan_payment, loan_amortization_schedule, loan_total_interest,
    
    # 投资分析
    net_present_value, internal_rate_of_return, payback_period,
    
    # 债券
    bond_price, bond_duration,
    
    # 财务比率
    return_on_equity, current_ratio, price_to_earnings_ratio,
    
    # 风险
    sharpe_ratio, beta,
    
    # 便捷函数
    investment_summary, rule_of_72,
)


def print_section(title):
    """打印章节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_time_value_of_money():
    """演示货币时间价值"""
    print_section("💰 货币时间价值")
    
    print("\n📈 复利奇迹：")
    print("   scenario: 1 万元投资，年利率 8%")
    
    for years in [5, 10, 20, 30]:
        fv = future_value(10000, 0.08, years)
        print(f"  {years:2d}年后：{fv:10,.2f}元")
    
    print("\n📊 不同复利频率对比（10 万元，5%，10 年）：")
    frequencies = [
        (1, "年复利"),
        (4, "季复利"),
        (12, "月复利"),
        (365, "日复利"),
    ]
    
    for freq, name in frequencies:
        fv = future_value(100000, 0.05, 10)  # 简化计算
        interest = compound_interest(100000, 0.05, 10, freq)
        print(f"  {name}: 利息 {interest:,.2f}元")
    
    print("\n📉 现值计算：")
    print("  10 年后的 100 万元，在 5% 折现率下的现值：")
    pv = present_value(1000000, 0.05, 10)
    print(f"  现值：{pv:,.2f}元")
    
    print("\n📐 有效年利率 (EAR)：")
    nominal = 0.12
    print(f"  名义利率：{nominal*100}%")
    for freq, name in [(1, "年"), (2, "半年"), (4, "季"), (12, "月"), (365, "日")]:
        ear = effective_annual_rate(nominal, freq)
        print(f"  {name}复利：EAR = {ear*100:.4f}%")


def demo_annuities():
    """演示年金计算"""
    print_section("💵 年金计算")
    
    print("\n🎯 退休储蓄计划：")
    print("  每月存 2000 元，年利率 6%，存 30 年")
    
    monthly_payment = 2000
    annual_rate = 0.06
    years = 30
    
    # 年金终值
    fv = annuity_future_value(monthly_payment * 12, annual_rate, years)
    total_contributed = monthly_payment * 12 * years
    
    print(f"  总投入：{total_contributed:,.2f}元")
    print(f"  退休时资产：{fv:,.2f}元")
    print(f"  投资收益：{fv - total_contributed:,.2f}元")
    
    print("\n🏦 养老金领取：")
    print("  退休后每年领取 10 万元，领 20 年，折现率 4%")
    
    pv = annuity_present_value(100000, 0.04, 20)
    print(f"  需要准备的养老金：{pv:,.2f}元")


def demo_loan_calculations():
    """演示贷款计算"""
    print_section("🏠 贷款计算")
    
    print("\n🏡 房贷计算：")
    print("  贷款 200 万元，年利率 4.5%，30 年期")
    
    principal = 2000000
    rate = 0.045
    years = 30
    
    monthly_payment = loan_payment(principal, rate, years, 12)
    total_interest = loan_total_interest(principal, rate, years, 12)
    
    print(f"  月供：{monthly_payment:,.2f}元")
    print(f"  总利息：{total_interest:,.2f}元")
    print(f"  总还款：{principal + total_interest:,.2f}元")
    print(f"  利息占比：{total_interest/(principal+total_interest)*100:.1f}%")
    
    print("\n📋 前 3 期还款明细：")
    schedule = loan_amortization_schedule(principal, rate, years, 12)
    
    for i in range(3):
        p = schedule[i]
        print(f"  第{p['payment_number']:3d}期：月供{p['payment']:,.2f}元 "
              f"(本金{p['principal']:,.2f} + 利息{p['interest']:,.2f})")
    
    print("\n🚗 车贷对比：")
    car_price = 300000
    
    options = [
        (0.03, 3, "3 年 3%"),
        (0.04, 4, "4 年 4%"),
        (0.05, 5, "5 年 5%"),
    ]
    
    for rate, years, label in options:
        payment = loan_payment(car_price, rate, years, 12)
        total_int = loan_total_interest(car_price, rate, years, 12)
        print(f"  {label}: 月供{payment:,.2f}元，总利息{total_int:,.2f}元")


def demo_investment_analysis():
    """演示投资分析"""
    print_section("📊 投资分析")
    
    print("\n💼 项目评估：")
    print("  初始投资 100 万元，未来 5 年现金流：20 万、25 万、30 万、35 万、40 万")
    
    cash_flows = [-100, 25, 30, 35, 40, 45]
    discount_rate = 0.10
    
    npv = net_present_value(cash_flows, discount_rate)
    irr = internal_rate_of_return(cash_flows)
    pb = payback_period(cash_flows)
    
    print(f"\n  评估结果（折现率{discount_rate*100}%）：")
    print(f"  NPV: {npv:.2f}万元 {'✓ 可行' if npv > 0 else '✗ 不可行'}")
    print(f"  IRR: {irr*100:.2f}% {'✓ 可行' if irr > discount_rate else '✗ 不可行'}")
    print(f"  回收期：{pb:.2f}年")
    
    print("\n📈 72 法则：")
    for rate in [4, 6, 8, 10, 12]:
        years = rule_of_72(rate)
        print(f"  年利率{rate}%: 约{years:.1f}年翻倍")


def demo_bond_valuation():
    """演示债券估值"""
    print_section("💹 债券估值")
    
    print("\n📜 债券定价：")
    print("  面值 1000 元，票息 5%，10 年期，半年付息")
    
    face_value = 1000
    coupon_rate = 0.05
    years = 10
    
    print("\n  不同 YTM 下的债券价格：")
    for ytm in [0.03, 0.04, 0.05, 0.06, 0.07]:
        price = bond_price(face_value, coupon_rate, ytm, years, 2)
        status = "溢价" if price > face_value else "折价" if price < face_value else "平价"
        print(f"  YTM {ytm*100:.1f}%: 价格{price:.2f}元 ({status})")
    
    print("\n⏱️  久期分析：")
    duration = bond_duration(face_value, coupon_rate, 0.06, years, 2)
    print(f"  YTM 6% 时的麦考利久期：{duration:.2f}年")
    print(f"  含义：利率变化 1%，债券价格变化约{duration:.1f}%")


def demo_financial_ratios():
    """演示财务比率"""
    print_section("📐 财务比率")
    
    print("\n🏢 公司财务分析：")
    
    # 假设数据
    net_income = 50000000      # 净利润 5000 万
    shareholders_equity = 250000000  # 股东权益 2.5 亿
    total_assets = 500000000   # 总资产 5 亿
    current_assets = 150000000 # 流动资产 1.5 亿
    current_liabilities = 100000000  # 流动负债 1 亿
    revenue = 300000000        # 收入 3 亿
    cogs = 180000000           # 成本 1.8 亿
    shares_outstanding = 10000000  # 1000 万股
    stock_price = 25           # 股价 25 元
    
    roe = return_on_equity(net_income, shareholders_equity)
    roa = net_income / total_assets
    current = current_ratio(current_assets, current_liabilities)
    gross_margin = (revenue - cogs) / revenue
    eps = net_income / shares_outstanding
    pe = price_to_earnings_ratio(stock_price, eps)
    
    print(f"  盈利能力:")
    print(f"    ROE: {roe*100:.2f}%")
    print(f"    ROA: {roa*100:.2f}%")
    print(f"    毛利率：{gross_margin*100:.2f}%")
    
    print(f"\n  偿债能力:")
    print(f"    流动比率：{current:.2f}")
    
    print(f"\n  估值指标:")
    print(f"    EPS: {eps:.2f}元")
    print(f"    P/E: {pe:.2f}倍")


def demo_risk_metrics():
    """演示风险指标"""
    print_section("⚠️  风险指标")
    
    print("\n📊 投资组合分析：")
    
    # 假设数据
    portfolio_return = 0.12    # 组合年化收益 12%
    risk_free_rate = 0.03      # 无风险利率 3%
    portfolio_std_dev = 0.15   # 波动率 15%
    
    sharpe = sharpe_ratio(portfolio_return, risk_free_rate, portfolio_std_dev)
    
    print(f"  组合年化收益：{portfolio_return*100}%")
    print(f"  无风险利率：{risk_free_rate*100}%")
    print(f"  波动率：{portfolio_std_dev*100}%")
    print(f"\n  夏普比率：{sharpe:.3f}")
    print(f"  解读：每承担 1 单位风险，获得{sharpe:.3f}单位超额收益")
    
    print("\n🎯 β系数含义：")
    betas = [
        (0.5, "防御型股票，波动小于市场"),
        (1.0, "与市场同步"),
        (1.5, "进攻型股票，波动大于市场"),
        (2.0, "高波动股票"),
    ]
    
    for b, desc in betas:
        print(f"  β={b}: {desc}")


def demo_comprehensive_planning():
    """演示综合规划"""
    print_section("🎯 综合财务规划")
    
    print("\n💰 教育金规划：")
    print("  孩子现在 5 岁，18 岁上大学，预计需要 100 万教育金")
    
    years_to_college = 13
    target_amount = 1000000
    expected_return = 0.06
    
    # 计算需要每月存多少
    # 使用年金终值公式反推
    fv_factor = ((1 + expected_return) ** years_to_college - 1) / expected_return
    annual_contribution = target_amount / fv_factor
    monthly_contribution = annual_contribution / 12
    
    print(f"  距离大学：{years_to_college}年")
    print(f"  目标金额：{target_amount:,.2f}元")
    print(f"  预期收益：{expected_return*100}%")
    print(f"  需要每月存：{monthly_contribution:,.2f}元")
    
    print("\n🏖️  提前退休规划：")
    print("  目标：45 岁退休，每年花费 30 万，活到 85 岁")
    
    current_age = 30
    retirement_age = 45
    life_expectancy = 85
    annual_expense = 300000
    
    years_to_save = retirement_age - current_age
    years_in_retirement = life_expectancy - retirement_age
    
    # 退休时需要的总额（简化：不考虑通胀和投资收益）
    retirement_needed = annual_expense * years_in_retirement
    
    # 每年需要存多少
    fv_factor = ((1 + 0.07) ** years_to_save - 1) / 0.07
    annual_save = retirement_needed / fv_factor
    
    print(f"  当前年龄：{current_age}岁")
    print(f"  退休年龄：{retirement_age}岁")
    print(f"  储蓄期：{years_to_save}年")
    print(f"  退休期：{years_in_retirement}年")
    print(f"  需要总额：{retirement_needed:,.2f}元")
    print(f"  每年需存：{annual_save:,.2f}元")
    print(f"  每月需存：{annual_save/12:,.2f}元")


def main():
    """运行所有演示"""
    print("\n" + "💰" * 30)
    print("   AllToolkit - Finance Utils 功能演示")
    print("💰" * 30)
    
    demo_time_value_of_money()
    demo_annuities()
    demo_loan_calculations()
    demo_investment_analysis()
    demo_bond_valuation()
    demo_financial_ratios()
    demo_risk_metrics()
    demo_comprehensive_planning()
    
    print_section("✅ 演示完成")
    print("\n💡 提示：运行 'python finance_utils_test.py -v' 执行完整测试套件")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
