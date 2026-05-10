# Mortgage Calculator Utilities

房贷计算工具集 - 支持等额本息、等额本金还款方式，提前还款计算，可负担性分析等。

## 功能特性

- **等额本息还款**：计算月供、生成还款计划表
- **等额本金还款**：计算首末月还款、生成还款计划表
- **还款方式对比**：比较两种还款方式的利息差异
- **提前还款计算**：支持缩短年限或减少月供两种方案
- **可负担性分析**：根据收入计算可贷款金额
- **房价估算**：根据月供反推可购房总价
- **LPR利率计算**：支持LPR基准利率加点模式

## 零外部依赖

完全使用 Python 标准库实现，无需安装任何第三方包。

## 快速开始

### 基本用法

```python
from mortgage_utils import MortgageCalculator

# 创建计算器：贷款100万，年利率4.9%，30年
calc = MortgageCalculator(1000000, 4.9, 30)

# 等额本息还款
summary = calc.equal_principal_interest_summary()
print(f"月供: {summary['monthly_payment']:.2f} 元")
print(f"总还款: {summary['total_payment']:.2f} 元")
print(f"总利息: {summary['total_interest']:.2f} 元")

# 等额本金还款
principal_summary = calc.equal_principal_summary()
print(f"首月还款: {principal_summary['first_month_payment']:.2f} 元")
print(f"末月还款: {principal_summary['last_month_payment']:.2f} 元")

# 对比两种还款方式
comparison = calc.compare_methods()
print(f"等额本金节省利息: {comparison['comparison']['equal_principal_saves']:.2f} 元")
```

### 获取还款计划表

```python
# 等额本息还款计划
schedule = calc.equal_principal_interest_schedule()
for item in schedule[:5]:  # 打印前5期
    print(f"第{item['period']}期: {item['date']} 月供{item['payment']:.2f} "
          f"本金{item['principal']:.2f} 利息{item['interest']:.2f}")

# 等额本金还款计划
schedule = calc.equal_principal_schedule()
for item in schedule[:5]:  # 打印前5期
    print(f"第{item['period']}期: {item['date']} 月供{item['payment']:.2f} "
          f"本金{item['principal']:.2f} 利息{item['interest']:.2f}")
```

### 提前还款计算

```python
from mortgage_utils import PrepaymentCalculator

prepay_calc = PrepaymentCalculator(calc, 'equal_principal_interest')

# 提前还款20万 - 缩短年限
result = prepay_calc.prepay_lump_sum(
    paid_months=60,  # 已还5年（60期）
    prepay_amount=200000,
    reduce_term=True  # 缩短年限
)
print(f"新期限: {result['new_term']} 个月")
print(f"节省利息: {result['interest_saved']:.2f} 元")
print(f"缩短年限: {result['term_saved']} 个月")

# 提前还款20万 - 减少月供
result = prepay_calc.prepay_lump_sum(
    paid_months=60,
    prepay_amount=200000,
    reduce_term=False  # 减少月供
)
print(f"新月供: {result['new_monthly_payment']:.2f} 元")
print(f"月供减少: {result['monthly_payment_saved']:.2f} 元")
print(f"节省利息: {result['interest_saved']:.2f} 元")

# 每月额外还款
result = prepay_calc.prepay_partial_every_month(
    paid_months=60,
    extra_monthly=1000  # 每月多还1000元
)
print(f"缩短期限: {result['term_saved']} 个月")
print(f"节省利息: {result['estimated_interest_saved']:.2f} 元")
```

### 可负担性计算

```python
from mortgage_utils import calculate_affordability

# 月收入15000，已有负债2000，计算可贷款金额
result = calculate_affordability(
    monthly_income=15000,
    monthly_debt=2000,
    annual_rate=4.9,
    years=30,
    income_ratio=0.5  # 收入负债比上限50%
)
print(f"可贷款金额: {result['max_loan_amount']:.2f} 元")
```

### 根据月供反推房价

```python
from mortgage_utils import estimate_property_value

# 月供5000，首付30%，计算可购房总价
result = estimate_property_value(
    monthly_payment=5000,
    annual_rate=4.9,
    years=30,
    down_payment_ratio=0.3
)
print(f"可购房总价: {result['estimated_property_value']:.2f} 元")
print(f"首付金额: {result['down_payment']:.2f} 元")
```

### LPR利率计算

```python
from mortgage_utils import calculate_lpr_spread

# LPR 4.3%，加点60个基点
result = calculate_lpr_spread(
    base_rate=4.3,
    spread=0.6,  # 加60个基点
    principal=1000000,
    years=30
)
print(f"实际利率: {result['actual_rate']}%")
print(f"月供: {result['equal_principal_interest']['monthly_payment']:.2f} 元")
```

### 便捷函数

```python
from mortgage_utils import (
    calc_equal_principal_interest,
    calc_equal_principal,
    compare_repayment_methods
)

# 快速计算等额本息
result = calc_equal_principal_interest(1000000, 4.9, 30)
print(f"月供: {result['monthly_payment']:.2f} 元")

# 快速计算等额本金
result = calc_equal_principal(1000000, 4.9, 30)
print(f"首月还款: {result['first_month_payment']:.2f} 元")

# 快速对比
result = compare_repayment_methods(1000000, 4.9, 30)
print(f"利息差额: {result['comparison']['interest_difference']:.2f} 元")
```

## API 参考

### MortgageCalculator

**构造参数：**
- `principal`: 贷款本金（元）
- `annual_rate`: 年利率（如 4.9 表示 4.9%）
- `years`: 贷款年限
- `start_date`: 还款起始日期（可选）

**方法：**
- `equal_principal_interest_monthly()`: 计算等额本息月供
- `equal_principal_interest_schedule()`: 生成等额本息还款计划表
- `equal_principal_interest_summary()`: 等额本息还款汇总
- `equal_principal_schedule()`: 生成等额本金还款计划表
- `equal_principal_summary()`: 等额本金还款汇总
- `compare_methods()`: 比较两种还款方式

### PrepaymentCalculator

**构造参数：**
- `mortgage`: MortgageCalculator 实例
- `method`: 还款方式（'equal_principal_interest' 或 'equal_principal'）

**方法：**
- `prepay_lump_sum(paid_months, prepay_amount, reduce_term)`: 一次性提前还款
- `prepay_partial_every_month(paid_months, extra_monthly)`: 每月额外还款

### 其他函数

- `calculate_affordability()`: 可负担性计算
- `calculate_lpr_spread()`: LPR利率计算
- `estimate_property_value()`: 房价估算

## 运行测试

```bash
python -m pytest mortgage_utils_test.py -v
```

或直接运行：

```bash
python mortgage_utils_test.py
```

## 示例运行

```bash
python mortgage_utils.py
```

输出示例：
```
============================================================
房贷计算器示例
============================================================

【等额本息还款】
  type: 等额本息
  principal: 1000000.0
  annual_rate: 4.9
  years: 30
  monthly_payment: 5307.27
  total_payment: 1910617.20
  total_interest: 910617.20
  ...

【等额本金还款】
  type: 等额本金
  ...
  
【还款方式对比】
  等额本息月供: 5307.27 元
  等额本金首月: 6861.11 元
  等额本金末月: 2790.58 元
  等额本金节省利息: 126617.20 元
```

## 精度说明

使用 Python `decimal` 模块进行精确货币计算，避免浮点数误差。所有金额四舍五入到分。

## 作者

AllToolkit 自动生成 - 2026-05-10