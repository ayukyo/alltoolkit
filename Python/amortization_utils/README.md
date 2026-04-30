# Amortization Utils

零依赖的摊销计算工具模块，支持贷款分期还款计划、利息/本金分解、提前还款分析等功能。

## 功能特性

- 📊 **月供计算** - 标准摊销公式计算固定利率贷款月供
- 📅 **分期计划生成** - 生成完整的摊销计划表
- 💰 **提前还款分析** - 分析一次性额外付款的影响
- 📈 **额外月供分析** - 计算每月额外还款的节省效果
- 🔄 **再融资比较** - 比较当前贷款与再融资方案
- 📉 **APR计算** - 包含费用的实际年化利率计算
- 🏠 **购房能力评估** - 根据月供计算可负担的贷款金额
- ⏱️ **还款期限计算** - 根据目标月供计算所需还款期限

## 安装

```python
# 零外部依赖，使用 Python 标准库
from amortization_utils.mod import AmortizationUtils, calculate_mortgage_payment, generate_mortgage_schedule
```

## 快速开始

### 基础月供计算

```python
from amortization_utils.mod import AmortizationUtils

# 计算月供
# 贷款金额: 200,000美元，年利率: 5%，期限: 30年(360个月)
monthly_payment = AmortizationUtils.calculate_monthly_payment(
    principal=200000,
    annual_rate=0.05,
    term_months=360
)
print(f"月供: ${monthly_payment:.2f}")  # 月供: $1073.64
```

### 快捷房贷计算函数

```python
from amortization_utils.mod import calculate_mortgage_payment

# 注意：利率以百分比形式传入（如 6.5 表示 6.5%）
payment = calculate_mortgage_payment(
    principal=300000,
    annual_rate=6.5,  # 6.5%
    years=30
)
print(f"月供: ${payment:.2f}")  # 月供: $1896.20
```

### 生成分期还款计划

```python
from amortization_utils.mod import AmortizationUtils
from datetime import date

schedule = AmortizationUtils.generate_schedule(
    principal=100000,
    annual_rate=0.05,
    term_months=120,  # 10年
    start_date=date(2024, 1, 1)
)

print(f"月供: ${schedule.monthly_payment:.2f}")
print(f"总还款: ${schedule.total_payment:.2f}")
print(f"总利息: ${schedule.total_interest:.2f}")

# 查看每期还款详情
for payment in schedule.payments[:5]:
    print(f"第{payment.payment_number}期: 还款${payment.payment_amount:.2f}, "
          f"本金${payment.principal:.2f}, 利息${payment.interest:.2f}, "
          f"剩余${payment.remaining_balance:.2f}")
```

### 提前还款分析

```python
# 分析一次性额外付款的影响
result = AmortizationUtils.calculate_early_payoff(
    principal=200000,
    annual_rate=0.05,
    term_months=360,
    months_paid=60,  # 已还款5年
    extra_payment=50000  # 一次性额外付款5万
)

print(f"剩余余额: ${result['remaining_balance']:,.2f}")
print(f"节省月数: {result['months_saved']}个月")
print(f"节省利息: ${result['interest_saved']:,.2f}")
```

### 额外月供分析

```python
# 分析每月额外还款$200的影响
impact = AmortizationUtils.calculate_extra_payment_impact(
    principal=200000,
    annual_rate=0.05,
    term_months=360,
    extra_monthly=200
)

print(f"原始期限: {impact['original_term_months']}个月")
print(f"新期限: {impact['new_term_months']}个月")
print(f"节省月数: {impact['months_saved']}个月 ({impact['years_saved']}年)")
print(f"节省利息: ${impact['interest_saved']:,.2f}")
```

### 再融资比较

```python
comparison = AmortizationUtils.calculate_refinance_comparison(
    current_balance=180000,
    current_rate=0.06,
    current_remaining_months=300,
    new_rate=0.045,
    new_term_months=360,
    closing_costs=5000
)

print(f"当前月供: ${comparison['current']['monthly_payment']:,.2f}")
print(f"新月供: ${comparison['refinance']['monthly_payment']:,.2f}")
print(f"月供差额: ${comparison['comparison']['monthly_payment_difference']:,.2f}")
print(f"净节省: ${comparison['comparison']['net_savings']:,.2f}")
print(f"是否值得: {'是' if comparison['comparison']['is_worth_it'] else '否'}")
```

### 计算购房能力

```python
affordability = AmortizationUtils.calculate_affordable_principal(
    monthly_payment=2000,  # 每月可承受的还款额
    annual_rate=0.05,
    term_months=360,
    down_payment=50000  # 首付
)

print(f"可贷款金额: ${affordability['loan_amount']:,.2f}")
print(f"首付: ${affordability['down_payment']:,.2f}")
print(f"可购房总价: ${affordability['total_home_price']:,.2f}")
```

### APR计算

```python
# 计算实际年化利率（包含手续费）
apr = AmortizationUtils.calculate_apr(
    principal=200000,
    monthly_payment=1073.64,
    term_months=360,
    fees=5000
)

print(f"APR: {apr * 100:.2f}%")  # APR: 5.27%
```

### 根据目标月供计算期限

```python
result = AmortizationUtils.find_term_for_payment(
    principal=100000,
    annual_rate=0.05,
    target_payment=1500
)

if result['possible']:
    print(f"需要{result['term_months']}个月 ({result['years']}年)")
    print(f"实际月供: ${result['monthly_payment']:,.2f}")
    print(f"总利息: ${result['total_interest']:,.2f}")
else:
    print(f"月供过低，最低需要: ${result['minimum_payment']:,.2f}")
```

## API参考

### AmortizationUtils 类

#### 静态方法

| 方法 | 说明 |
|------|------|
| `calculate_monthly_payment(principal, annual_rate, term_months)` | 计算月供 |
| `calculate_interest_portion(remaining_balance, annual_rate)` | 计算当期利息 |
| `generate_schedule(principal, annual_rate, term_months, start_date, extra_monthly)` | 生成完整分期计划 |
| `calculate_remaining_balance(principal, annual_rate, term_months, months_paid)` | 计算剩余本金 |
| `calculate_early_payoff(principal, annual_rate, term_months, months_paid, extra_payment)` | 提前还款分析 |
| `calculate_extra_payment_impact(principal, annual_rate, term_months, extra_monthly)` | 额外月供影响分析 |
| `calculate_refinance_comparison(current_balance, current_rate, current_remaining_months, new_rate, new_term_months, closing_costs)` | 再融资比较 |
| `calculate_apr(principal, monthly_payment, term_months, fees)` | APR计算 |
| `find_term_for_payment(principal, annual_rate, target_payment)` | 计算所需期限 |
| `calculate_affordable_principal(monthly_payment, annual_rate, term_months, down_payment)` | 计算可负担本金 |

### AmortizationSchedule 类

| 属性 | 说明 |
|------|------|
| `principal` | 贷款本金 |
| `annual_rate` | 年利率 |
| `term_months` | 期限（月） |
| `start_date` | 开始日期 |
| `payments` | 还款计划列表 |
| `monthly_payment` | 月供金额 |
| `total_payment` | 总还款金额 |
| `total_interest` | 总利息 |
| `interest_to_principal_ratio` | 利息/本金比 |

### AmortizationPayment 类

| 属性 | 说明 |
|------|------|
| `payment_number` | 期数 |
| `payment_date` | 还款日期 |
| `payment_amount` | 还款金额 |
| `principal` | 本金部分 |
| `interest` | 利息部分 |
| `remaining_balance` | 剩余本金 |
| `cumulative_principal` | 累计已还本金 |
| `cumulative_interest` | 累计已还利息 |

## 使用场景

- 🏠 房贷计算器
- 🚗 车贷规划
- 💳 个人贷款分析
- 📊 投资回报计算
- 📱 金融应用开发
- 📖 财务教育工具

## 注意事项

1. 利率以小数形式传入（如 0.05 表示 5%）
2. 快捷函数 `calculate_mortgage_payment` 和 `generate_mortgage_schedule` 利率以百分比形式传入（如 6.5 表示 6.5%）
3. 所有金额计算结果保留两位小数
4. 使用 `dateutil.relativedelta` 进行日期计算

## 许可证

MIT License