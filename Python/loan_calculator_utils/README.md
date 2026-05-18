# Loan Calculator Utils - 贷款计算工具模块 💰

[![测试状态](https://img.shields.io/badge/tests-65%20passed-brightgreen)]()
[![覆盖率](https://img.shields.io/badge/coverage-100%25-brightgreen)]()

全面的贷款和金融计算工具库，零外部依赖，纯 Python 实现。

## ✨ 功能特性

### 基础计算
- **月供计算**：等额本息、等额本金、只还利息三种方式
- **利息计算**：单利、复利、未来价值、现值计算
- **还款计划生成**：完整分期还款表

### 高级分析
- **APR 计算**：考虑费用后的真实年化利率
- **提前还款分析**：分析额外还款对期限和利息的影响
- **再融资分析**：判断转贷是否划算

### 房贷专用
- **房贷资格计算**：基于收入和 DTI 限制
- **首付方案比较**：不同首付比例下的贷款方案

### 贷款比较
- 多方案对比，找出最优选择

---

## 🚀 快速开始

### 基础月供计算

```python
from loan_calculator_utils import monthly_payment, total_interest

# 等额本息月供
payment = monthly_payment(100000, 5, 12)  # 10万，年利率5%，12期
print(f"月供: ¥{payment:.2f}")  # ¥8560.75

# 总利息
interest = total_interest(100000, 5, 12)
print(f"总利息: ¥{interest:.2f}")  # ¥2728.98
```

### 贷款汇总

```python
from loan_calculator_utils import LoanParams, calculate_loan_summary

params = LoanParams(
    principal=100000,      # 贷款本金
    annual_rate=5,         # 年利率 5%
    term_months=12,        # 期限 12 个月
)

summary = calculate_loan_summary(params)
print(f"总还款: ¥{summary.total_payments:.2f}")
print(f"总利息: ¥{summary.total_interest:.2f}")
print(f"APR: {summary.apr * 100:.2f}%")
```

### 还款计划表

```python
from loan_calculator_utils import loan_table

# 生成还款计划
table = loan_table(10000, 6, 12)

for item in table[:3]:
    print(f"第{item['period']}期: 还款¥{item['payment']:.2f}, "
          f"本金¥{item['principal']:.2f}, 利息¥{item['interest']:.2f}")
```

---

## 📚 详细用法

### 还款方式对比

```python
from loan_calculator_utils import (
    LoanParams, PaymentType,
    calculate_equal_payment,
    calculate_equal_principal_payment,
    calculate_loan_summary
)

# 等额本息
params_equal = LoanParams(
    principal=100000, annual_rate=5, term_months=12,
    payment_type=PaymentType.EQUAL_PAYMENT
)
payment_equal = calculate_equal_payment(params_equal)
summary_equal = calculate_loan_summary(params_equal)

# 等额本金
params_principal = LoanParams(
    principal=100000, annual_rate=5, term_months=12,
    payment_type=PaymentType.EQUAL_PRINCIPAL
)
payments_principal = calculate_equal_principal_payment(params_principal)
summary_principal = calculate_loan_summary(params_principal)

print("等额本息:")
print(f"  月供固定: ¥{payment_equal:.2f}")
print(f"  总利息: ¥{summary_equal.total_interest:.2f}")

print("等额本金:")
print(f"  首期还款: ¥{payments_principal[0]:.2f}")
print(f"  末期还款: ¥{payments_principal[-1]:.2f}")
print(f"  总利息: ¥{summary_principal.total_interest:.2f}")
```

### 提前还款分析

```python
from loan_calculator_utils import LoanParams, analyze_early_payoff

params = LoanParams(principal=200000, annual_rate=5, term_months=360)

# 每月额外还款 200 元
result = analyze_early_payoff(params, extra_payment=200)

print(f"节省期限: {result.months_saved} 个月")
print(f"节省利息: ¥{result.interest_saved:.2f}")
print(f"新还款结束日期: {result.payoff_date_new}")
```

### 再融资分析

```python
from loan_calculator_utils import LoanParams, analyze_refinance

original = LoanParams(principal=200000, annual_rate=6, term_months=360)

# 利率从 6% 降到 4.5%，再融资成本 5000 元
result = analyze_refinance(
    original,
    new_rate=4.5,
    new_term_months=360,
    closing_costs=5000
)

print(f"月供节省: ¥{result.monthly_savings:.2f}")
print(f"总利息节省: ¥{result.total_savings:.2f}")
print(f"盈亏平衡点: {result.break_even_months} 个月")
print(f"是否划算: {result.is_worth_it}")
```

### 房贷资格计算

```python
from loan_calculator_utils import mortgage_qualification

qualification = mortgage_qualification(
    annual_income=120000,    # 年收入 12 万
    monthly_debt=500,        # 现有月债务 500 元
    down_payment=50000,      # 首付 5 万
    interest_rate=5,         # 年利率 5%
)

print(f"最大贷款: ¥{qualification['max_loan_amount']:.2f}")
print(f"最大房价: ¥{qualification['max_home_price']:.2f}")
print(f"月供: ¥{qualification['actual_monthly_payment']:.2f}")
print(f"债务收入比: {qualification['debt_to_income_ratio']}%")
print(f"是否合格: {qualification['qualified']}")
```

### 首付方案比较

```python
from loan_calculator_utils import calculate_down_payment_options

options = calculate_down_payment_options(
    home_price=500000,       # 房价 50 万
    interest_rate=5,         # 年利率 5%
    down_payment_percentages=[5, 10, 15, 20]
)

for opt in options:
    print(f"{opt['down_payment_percent']}%首付:")
    print(f"  首付金额: ¥{opt['down_payment']:.0f}")
    print(f"  月供: ¥{opt['monthly_payment']:.0f}")
    print(f"  总利息: ¥{opt['total_interest']:.0f}")
```

### 利息计算

```python
from loan_calculator_utils import (
    calculate_simple_interest,
    calculate_compound_interest,
    calculate_future_value,
    calculate_present_value
)

# 单利
interest_simple = calculate_simple_interest(10000, 5, 2)  # ¥1000.00

# 复利
interest_compound = calculate_compound_interest(10000, 5, 2)  # ¥1049.41

# 未来价值
fv = calculate_future_value(10000, 5, 10, contributions=100)

# 现值
pv = calculate_present_value(10000, 5, 2)  # ¥9057.31
```

---

## 📊 数据结构

### LoanParams 贷款参数

| 字段 | 类型 | 说明 |
|------|------|------|
| principal | float | 贷款本金 |
| annual_rate | float | 年利率（百分比） |
| term_months | int | 期限（月） |
| payment_type | PaymentType | 还款方式 |
| down_payment | float | 首付款 |
| fees | float | 贷款费用 |

### PaymentType 还款方式

- `EQUAL_PAYMENT` - 等额本息（月供固定）
- `EQUAL_PRINCIPAL` - 等额本金（本金固定，利息递减）
- `INTEREST_ONLY` - 只还利息

### PaymentFrequency 还款频率

- `MONTHLY` - 每月
- `BI_WEEKLY` - 每两周
- `WEEKLY` - 每周
- `QUARTERLY` - 每季度
- `SEMI_ANNUAL` - 每半年
- `ANNUAL` - 每年

---

## 🔧 API 参考

### 便捷函数

| 函数 | 说明 |
|------|------|
| `monthly_payment(principal, rate, months)` | 快速计算月供 |
| `total_interest(principal, rate, months)` | 快速计算总利息 |
| `loan_table(principal, rate, months)` | 快速生成还款表 |

### 计算函数

| 函数 | 说明 |
|------|------|
| `calculate_equal_payment(params)` | 等额本息月供 |
| `calculate_equal_principal_payment(params)` | 等额本金还款列表 |
| `calculate_interest_only_payment(params)` | 只还利息金额 |
| `generate_amortization_schedule(params)` | 还款计划表 |
| `calculate_loan_summary(params)` | 贷款汇总 |
| `calculate_apr(principal, payment, months, fees)` | APR 计算 |

### 分析函数

| 函数 | 说明 |
|------|------|
| `analyze_early_payoff(params, extra_payment)` | 提前还款分析 |
| `analyze_refinance(params, new_rate, new_term)` | 再融资分析 |
| `compare_loans(loans)` | 多贷款比较 |

### 房贷函数

| 函数 | 说明 |
|------|------|
| `mortgage_qualification(...)` | 房贷资格计算 |
| `calculate_down_payment_options(...)` | 首付方案比较 |

---

## 🧪 测试

模块包含 65 个测试用例，覆盖：

- 等额本息/等额本金月供计算
- 还款计划生成
- APR 计算
- 提前还款分析
- 再融资分析
- 房贷资格计算
- 边界值（零利率、超大贷款、负数处理等）

```bash
python Python/loan_calculator_utils/loan_calculator_utils_test.py
```

---

## 📝 计算公式

### 等额本息月供

```
M = P × [r(1+r)^n] / [(1+r)^n - 1]
```

其中：
- M = 月供
- P = 贷款本金
- r = 月利率
- n = 总期数

### APR 计算

使用二分法求解使现值等于实际贷款金额的利率。

---

## 📄 许可证

MIT License

---

**最后更新**: 2026-05-19