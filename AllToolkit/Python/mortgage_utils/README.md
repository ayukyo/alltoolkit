# Mortgage Utils - 房贷计算工具

一个零外部依赖的房贷计算工具库，支持等额本息、等额本金、提前还款计算等功能。

## 功能特性

- **等额本息计算** - 每月还款金额固定
- **等额本金计算** - 每月本金固定，利息递减
- **提前还款模拟** - 支持缩短年限和减少月供两种模式
- **组合贷款计算** - 公积金贷款 + 商业贷款组合
- **贷款额度反算** - 根据月供计算可承受贷款额度
- **还款计划生成** - 支持文本和 CSV 格式导出
- **还清时间估算** - 根据月供估算还清时间

## 安装使用

```python
# 直接导入使用，无需安装依赖
from mortgage_utils.mod import (
    calculate_mortgage,
    RepaymentMethod
)
```

## 快速开始

### 基本计算

```python
from mortgage_utils.mod import calculate_mortgage, RepaymentMethod

# 等额本息（默认）
result = calculate_mortgage(1000000, 4.2, 30)  # 100万，4.2%，30年
print(result.get_summary())

# 等额本金
result = calculate_mortgage(
    1000000, 4.2, 30,
    RepaymentMethod.EQUAL_PRINCIPAL
)
print(result.get_summary())
```

### 对比两种还款方式

```python
from mortgage_utils.mod import compare_methods

comparison = compare_methods(1000000, 4.2, 30)
# 等额本金总利息更少，但前期月供更高
```

### 提前还款计算

```python
from mortgage_utils.mod import calculate_mortgage, calculate_prepayment, PrepaymentType

result = calculate_mortgage(1000000, 4.2, 30)

# 第 12 个月提前还款 10 万，缩短年限
prepay = calculate_prepayment(
    result, 12, 100000,
    PrepaymentType.REDUCE_TERM
)
print(f"节省利息: {prepay.interest_saved_term:,.2f}")
print(f"节省月数: {prepay.months_saved}")

# 或者选择减少月供
prepay = calculate_prepayment(
    result, 12, 100000,
    PrepaymentType.REDUCE_PAYMENT
)
print(f"新月供: {prepay.new_monthly_payment:,.2f}")
```

### 组合贷款

```python
from mortgage_utils.mod import calculate_combined_loan

combined = calculate_combined_loan(
    commercial_principal=700000,  # 商业贷款 70 万
    commercial_rate=4.2,           # 商业利率 4.2%
    fund_principal=300000,         # 公积金 30 万
    fund_rate=3.1,                 # 公积金利率 3.1%
    years=30
)
print(f"总月供: {combined['combined']['first_month_payment']:,.2f}")
```

### 反算贷款额度

```python
from mortgage_utils.mod import calculate_affordable_loan

# 月供 5000，利率 4.2%，30 年
loan = calculate_affordable_loan(5000, 4.2, 30)
print(f"可贷款: {loan:,.2f}")
```

### 生成还款计划

```python
from mortgage_utils.mod import calculate_mortgage, generate_payment_schedule
from datetime import date

result = calculate_mortgage(
    1000000, 4.2, 30,
    start_date=date(2024, 1, 15)
)

# 文本格式
print(generate_payment_schedule(result, "text"))

# CSV 格式
print(generate_payment_schedule(result, "csv"))
```

## API 参考

### 主要函数

| 函数 | 说明 |
|------|------|
| `calculate_mortgage()` | 房贷计算主函数 |
| `calculate_equal_principal_interest()` | 等额本息计算 |
| `calculate_equal_principal()` | 等额本金计算 |
| `calculate_prepayment()` | 提前还款计算 |
| `calculate_affordable_loan()` | 反算贷款额度 |
| `compare_methods()` | 对比两种还款方式 |
| `calculate_combined_loan()` | 组合贷款计算 |
| `generate_payment_schedule()` | 生成还款计划表 |
| `estimate_payoff_time()` | 估算还清时间 |

### 枚举类型

```python
class RepaymentMethod(Enum):
    EQUAL_PRINCIPAL_INTEREST = "equal_principal_interest"  # 等额本息
    EQUAL_PRINCIPAL = "equal_principal"  # 等额本金

class PrepaymentType(Enum):
    REDUCE_TERM = "reduce_term"  # 缩短年限
    REDUCE_PAYMENT = "reduce_payment"  # 减少月供
```

### 数据类

```python
@dataclass
class MortgageResult:
    principal: float          # 贷款本金
    annual_rate: float        # 年利率
    years: int               # 贷款年限
    method: RepaymentMethod  # 还款方式
    total_months: int        # 总期数
    total_payment: float     # 还款总额
    total_interest: float    # 总利息
    first_month_payment: float  # 首月月供
    last_month_payment: float   # 末月月供
    monthly_payments: List[MonthlyPayment]  # 每月详情

@dataclass
class MonthlyPayment:
    period: int            # 期数
    payment: float         # 月供
    principal: float       # 本金部分
    interest: float        # 利息部分
    remaining_principal: float  # 剩余本金
    date: Optional[date]   # 还款日期
```

## 示例运行

```bash
# 运行测试
python mortgage_utils_test.py

# 运行基础示例
python examples/basic_usage.py

# 运行高级示例
python examples/advanced_usage.py
```

## 常见问题

**Q: 为什么等额本金首月月供比等额本息高？**  
A: 等额本金每月偿还固定本金，利息按剩余本金计算，所以前期利息多、月供高，后期逐渐减少。总利息比等额本息少。

**Q: 提前还款选缩短年限还是减少月供？**  
A: 缩短年限能节省更多利息；减少月供能降低每月压力。根据个人财务情况选择。

**Q: 计算结果和银行有细微差异？**  
A: 银行可能有不同的计息规则（如按实际天数、四舍五入规则等）。本工具使用标准公式计算，供参考。

## 许可证

MIT License