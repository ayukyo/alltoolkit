# AllToolkit - Python Finance Utils 💰

**零依赖金融计算工具 - 功能完整的生产就绪工具**

---

## 📖 概述

`finance_utils` 提供全面的金融计算功能，包括货币时间价值、年金计算、贷款分析、投资评估、债券估值、折旧计算、财务比率和风险指标。完全使用 Python 标准库实现，无需任何外部依赖。

---

## ✨ 特性

- **货币时间价值** - 复利、现值、终值、有效年利率
- **年金计算** - 普通年金、预付年金、年金现值/终值
- **贷款计算** - 房贷/车贷还款、摊销计划、剩余本金
- **投资分析** - NPV、IRR、投资回收期、盈利指数
- **债券估值** - 债券价格、到期收益率、久期、修正久期
- **折旧计算** - 直线法、双倍余额递减法、年数总和法
- **财务比率** - ROI、ROE、ROA、流动比率、负债权益比、EPS、P/E
- **风险分析** - β系数、夏普比率、在险价值 (VaR)
- **投资汇总** - 一键生成投资预测报告

---

## 🚀 快速开始

### 基础使用

```python
from mod import future_value, present_value, compound_interest

# 计算复利终值：1 万元，年利率 5%，10 年后
fv = future_value(10000, 0.05, 10)
print(f"10 年后终值：{fv:.2f}元")  # 16288.95 元

# 计算现值：10 年后 1 万元的现值（5% 折现率）
pv = present_value(10000, 0.05, 10)
print(f"现值：{pv:.2f}元")  # 6139.13 元

# 计算复利利息
interest = compound_interest(10000, 0.05, 10, 12)  # 月复利
print(f"利息：{interest:.2f}元")  # 6470.09 元
```

### 贷款计算

```python
from mod import loan_payment, loan_amortization_schedule, loan_total_interest

# 房贷计算：100 万，年利率 4.5%，30 年，月供
monthly_payment = loan_payment(1000000, 0.045, 30, 12)
print(f"月供：{monthly_payment:.2f}元")  # 5066.85 元

# 总利息
total_interest = loan_total_interest(1000000, 0.045, 30, 12)
print(f"总利息：{total_interest:.2f}元")  # 824066.80 元

# 生成摊销计划
schedule = loan_amortization_schedule(1000000, 0.045, 30, 12)
print(f"第 1 期：本金{schedule[0]['principal']:.2f}，利息{schedule[0]['interest']:.2f}")
print(f"最后 1 期：本金{schedule[-1]['principal']:.2f}，利息{schedule[-1]['interest']:.2f}")
```

### 投资分析

```python
from mod import net_present_value, internal_rate_of_return, payback_period

# 投资项目：初始投资 10 万，未来 5 年每年回报 2.5 万
cash_flows = [-100000, 25000, 25000, 25000, 25000, 25000]

# 净现值（折现率 8%）
npv = net_present_value(cash_flows, 0.08)
print(f"NPV: {npv:.2f}元")  # -180.24 元（略亏）

# 内部收益率
irr = internal_rate_of_return(cash_flows)
print(f"IRR: {irr*100:.2f}%")  # 7.93%

# 投资回收期
pb = payback_period(cash_flows)
print(f"回收期：{pb:.2f}年")  # 4.00 年
```

### 债券估值

```python
from mod import bond_price, bond_yield_to_maturity, bond_duration

# 债券定价：面值 1000，票息 5%，YTM 6%，10 年期，半年付息
price = bond_price(1000, 0.05, 0.06, 10, 2)
print(f"债券价格：{price:.2f}元")  # 925.61 元（折价）

# 计算到期收益率
ytm = bond_yield_to_maturity(1000, 0.05, 950, 10, 2)
print(f"YTM: {ytm*100:.2f}%")  # 5.66%

# 久期
duration = bond_duration(1000, 0.05, 0.06, 10, 2)
print(f"麦考利久期：{duration:.2f}年")
```

### 财务比率

```python
from mod import (
    return_on_equity, current_ratio, debt_to_equity,
    earnings_per_share, price_to_earnings_ratio
)

# ROE：净利润 100 万，股东权益 500 万
roe = return_on_equity(1000000, 5000000)
print(f"ROE: {roe*100:.2f}%")  # 20%

# 流动比率：流动资产 50 万，流动负债 25 万
current = current_ratio(500000, 250000)
print(f"流动比率：{current:.2f}")  # 2.0

# EPS：净利润 100 万，优先股股利 10 万，流通股 50 万
eps = earnings_per_share(1000000, 100000, 500000)
print(f"EPS: {eps:.2f}元")  # 1.80 元

# P/E：股价 50 元，EPS 5 元
pe = price_to_earnings_ratio(50, 5)
print(f"P/E: {pe:.2f}")  # 10.00
```

---

## 📚 API 参考

### 货币时间价值

| 函数 | 描述 |
|------|------|
| `future_value(pv, rate, periods)` | 复利终值 |
| `present_value(fv, rate, periods)` | 现值（折现） |
| `compound_interest(principal, rate, time, compounds_per_year)` | 复利利息 |
| `continuous_compound_interest(principal, rate, time)` | 连续复利 |
| `effective_annual_rate(nominal_rate, compounds_per_year)` | 有效年利率 |
| `nominal_rate(effective_rate, compounds_per_year)` | 名义利率 |

### 年金

```python
from mod import annuity_future_value, annuity_present_value, annuity_payment

# 年金终值：每年存 1 万，存 20 年，年利率 5%
fv = annuity_future_value(10000, 0.05, 20)  # 330659.54 元

# 年金现值：每年领 1 万，领 20 年，折现率 5%
pv = annuity_present_value(10000, 0.05, 20)  # 124622.10 元

# 预付年金（期初付款）
fv_due = annuity_future_value(10000, 0.05, 20, annuity_due=True)
```

### 贷款计算

```python
from mod import (
    loan_payment, loan_amortization_schedule, loan_total_interest,
    remaining_loan_balance
)

# 车贷：30 万，年利率 6%，5 年
payment = loan_payment(300000, 0.06, 5, 12)  # 5799.82 元/月

# 剩余本金：5 年后
remaining = remaining_loan_balance(300000, 0.06, 5, 3, 12)
```

### 投资分析

| 函数 | 描述 |
|------|------|
| `net_present_value(cash_flows, discount_rate)` | 净现值 (NPV) |
| `internal_rate_of_return(cash_flows)` | 内部收益率 (IRR) |
| `profitability_index(cash_flows, discount_rate)` | 盈利指数 (PI) |
| `payback_period(cash_flows)` | 投资回收期 |
| `discounted_payback_period(cash_flows, discount_rate)` | 折现回收期 |

### 债券估值

```python
from mod import (
    bond_price, bond_yield_to_maturity, bond_current_yield,
    bond_duration, bond_modified_duration
)

# 债券价格
price = bond_price(face_value, coupon_rate, ytm, years, payments_per_year)

# 久期（利率风险度量）
duration = bond_duration(1000, 0.05, 0.06, 10, 2)
mod_duration = bond_modified_duration(1000, 0.05, 0.06, 10, 2)
```

### 折旧计算

```python
from mod import (
    straight_line_depreciation,
    declining_balance_depreciation,
    sum_of_years_digits_depreciation
)

# 直线法
schedule = straight_line_depreciation(cost=10000, salvage_value=1000, useful_life=5)

# 双倍余额递减法
schedule = declining_balance_depreciation(10000, 1000, 5)

# 年数总和法
schedule = sum_of_years_digits_depreciation(10000, 1000, 5)
```

### 财务比率

| 函数 | 公式 | 描述 |
|------|------|------|
| `return_on_investment(gain, cost)` | (收益 - 成本)/成本 | 投资回报率 |
| `return_on_equity(net_income, equity)` | 净利润/股东权益 | 净资产收益率 |
| `return_on_assets(net_income, assets)` | 净利润/总资产 | 总资产收益率 |
| `current_ratio(current_assets, current_liabilities)` | 流动资产/流动负债 | 流动比率 |
| `quick_ratio(cash, securities, ar, current_liabilities)` | 速动资产/流动负债 | 速动比率 |
| `debt_to_equity(total_debt, equity)` | 总负债/股东权益 | 负债权益比 |
| `gross_profit_margin(revenue, cogs)` | (收入 -COGS)/收入 | 毛利率 |
| `net_profit_margin(revenue, net_income)` | 净利润/收入 | 净利率 |
| `earnings_per_share(net_income, pref_div, shares)` | (净利润 - 优先股股利)/股数 | 每股收益 |
| `price_to_earnings_ratio(price, eps)` | 股价/EPS | 市盈率 |
| `dividend_yield(dividend, price)` | 年股利/股价 | 股息率 |

### 风险分析

```python
from mod import (
    expected_return, variance_returns, std_dev_returns,
    covariance_returns, correlation_returns, beta,
    sharpe_ratio, value_at_loss
)

# 预期收益率
er = expected_return([0.1, 0.2, 0.3], [0.3, 0.4, 0.3])

# 波动率（标准差）
volatility = std_dev_returns([0.1, 0.15, 0.05, -0.02, 0.08])

# β系数（系统性风险）
b = beta(asset_returns, market_returns)

# 夏普比率
sharpe = sharpe_ratio(portfolio_return=0.12, risk_free_rate=0.03, portfolio_std_dev=0.15)

# 在险价值 (VaR)
var = value_at_loss(historical_returns, confidence_level=0.95)
```

### 便捷函数

```python
from mod import investment_summary, compare_loans, rule_of_72

# 投资汇总报告
summary = investment_summary(
    initial_investment=10000,
    annual_return=0.07,
    years=10,
    annual_contribution=5000
)
print(summary)
# {'initial_investment': 10000, 'final_value': ..., 'total_gain': ..., ...}

# 贷款方案比较
options = [
    {'annual_rate': 0.05, 'years': 30},
    {'annual_rate': 0.04, 'years': 30},
    {'annual_rate': 0.05, 'years': 15},
]
comparison = compare_loans(200000, options)

# 72 法则（翻倍时间估算）
years = rule_of_72(8)  # 年利率 8%，约 9 年翻倍
exact_years = rule_of_72_exact(0.08)  # 精确计算
```

---

## 🧪 运行测试

```bash
cd /home/admin/.openclaw/workspace/AllToolkit/Python/finance_utils
python finance_utils_test.py -v
```

测试覆盖：
- ✅ 所有金融计算函数
- ✅ 边界情况（零利率、空数据、异常值）
- ✅ 错误处理
- ✅ 数值精度验证

---

## 📝 使用示例

### 示例 1：房贷决策分析

```python
from mod import loan_payment, loan_total_interest, compare_loans

# 比较不同贷款方案
principal = 2000000  # 200 万房贷

options = [
    {'annual_rate': 0.045, 'years': 30, 'label': '30 年 4.5%'},
    {'annual_rate': 0.040, 'years': 30, 'label': '30 年 4.0%'},
    {'annual_rate': 0.045, 'years': 15, 'label': '15 年 4.5%'},
]

print("房贷方案比较：")
print("-" * 60)

for opt in options:
    payment = loan_payment(principal, opt['annual_rate'], opt['years'], 12)
    total_int = loan_total_interest(principal, opt['annual_rate'], opt['years'], 12)
    
    print(f"{opt['label']}:")
    print(f"  月供：{payment:.2f}元")
    print(f"  总利息：{total_int:,.2f}元")
    print()
```

### 示例 2：投资项目评估

```python
from mod import net_present_value, internal_rate_of_return, profitability_index

# 项目现金流（单位：万元）
# 初始投资 100 万，未来 5 年回报
cash_flows = [-100, 25, 30, 35, 40, 45]

discount_rate = 0.10  # 要求回报率 10%

npv = net_present_value(cash_flows, discount_rate)
irr = internal_rate_of_return(cash_flows)
pi = profitability_index(cash_flows, discount_rate)

print("投资项目评估：")
print(f"  NPV: {npv:.2f}万元 {'✓ 可行' if npv > 0 else '✗ 不可行'}")
print(f"  IRR: {irr*100:.2f}% {'✓ 可行' if irr > discount_rate else '✗ 不可行'}")
print(f"  PI:  {pi:.3f} {'✓ 可行' if pi > 1 else '✗ 不可行'}")
```

### 示例 3：投资组合分析

```python
from mod import expected_return, std_dev_returns, sharpe_ratio, beta

# 历史收益率数据（月度）
portfolio_returns = [0.02, 0.03, -0.01, 0.04, 0.02, -0.02, 0.05, 0.01, 0.03, -0.01]
market_returns = [0.015, 0.02, -0.01, 0.03, 0.015, -0.015, 0.04, 0.01, 0.02, -0.01]

# 预期收益率
er = expected_return(portfolio_returns)

# 波动率
vol = std_dev_returns(portfolio_returns)

# 夏普比率（无风险利率 3% 年化，转换为月度约 0.25%）
sharpe = sharpe_ratio(er, 0.0025, vol)

# β系数
b = beta(portfolio_returns, market_returns)

print("投资组合分析：")
print(f"  预期月收益率：{er*100:.2f}%")
print(f"  年化波动率：{vol*100:.2f}%")
print(f"  夏普比率：{sharpe:.3f}")
print(f"  β系数：{b:.3f}")
```

### 示例 4：退休规划

```python
from mod import investment_summary, annuity_present_value, rule_of_72

# 退休规划：当前 35 岁，计划 65 岁退休
current_age = 35
retirement_age = 65
years_to_retire = retirement_age - current_age

# 现有存款 20 万，每年追加 5 万，预期年化 7%
summary = investment_summary(
    initial_investment=200000,
    annual_return=0.07,
    years=years_to_retire,
    annual_contribution=50000
)

print("退休规划预测：")
print(f"  当前年龄：{current_age}岁")
print(f"  退休年龄：{retirement_age}岁")
print(f"  投资年限：{years_to_retire}年")
print(f"  总投入：{summary['total_contributed']:,.2f}元")
print(f"  退休时资产：{summary['final_value']:,.2f}元")
print(f"  投资收益：{summary['total_gain']:,.2f}元")
print(f"  总回报率：{summary['total_return_pct']:.2f}%")

# 翻倍时间
double_time = rule_of_72(7)
print(f"\n  72 法则：年利率 7%，资产约{double_time:.1f}年翻倍")
```

---

## ⚠️ 注意事项

1. **利率格式**：所有利率使用小数格式（0.05 表示 5%）
2. **现金流符号**：投资/支出为负，收入为正
3. **期间一致性**：确保利率、付款频率、期限单位一致
4. **IRR 收敛**：IRR 计算可能在某些现金流模式下无法收敛
5. **数值精度**：极大或极小值可能存在浮点精度限制

---

## 📄 许可证

MIT License - 详见 AllToolkit 主项目许可证

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
