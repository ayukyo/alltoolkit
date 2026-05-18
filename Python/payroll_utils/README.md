# Payroll Utilities Module - 薪资计算工具

## 概述

提供全面的薪资计算功能，包括个人所得税、社保公积金、加班费、年终奖计算等。适用于中国薪资体系，零外部依赖。

## 功能列表

### 基础薪资计算
- **小时工资率计算** - `calculate_hourly_rate()`
- **日工资率计算** - `calculate_daily_rate()`
- **薪资类型转换** - `convert_salary()` (月薪/日薪/时薪转换)

### 加班费计算
- **加班费计算** - `calculate_overtime_pay()` (支持工作日/周末/节假日)
- **从月薪计算加班费** - `calculate_overtime_pay_from_monthly()`
- 加班倍数：工作日 1.5x，周末 2x，节假日 3x（符合中国劳动法）

### 社保计算（五险）
- **社保基数计算** - `get_social_insurance_base()` (自动处理上下限)
- **社保计算** - `calculate_social_insurance()`
- 支持城市：北京、上海、广州、深圳
- 包含养老、医疗、失业、工伤保险

### 公积金计算
- **公积金基数计算** - `get_housing_fund_base()`
- **公积金计算** - `calculate_housing_fund()`
- 支持自定义缴纳比例

### 个人所得税计算（2019版）
- **税率查询** - `find_tax_rate()`
- **月度个税计算** - `calculate_monthly_tax()` (累计预扣预缴法)
- **简化个税计算** - `calculate_simple_monthly_tax()`
- 基本减除费用：5000元/月
- 支持专项附加扣除

### 年终奖计算
- **单独计税** - `calculate_year_end_bonus_separate()`
- **合并计税** - `calculate_year_end_bonus_combined()`
- **计税方式比较** - `compare_year_end_bonus_methods()`
- **临界点优化** - `find_year_end_bonus_optimal_split()` (避免税率陷阱)

### 完整薪资计算
- **完整计算** - `calculate_payroll()` (包含所有扣除项)
- **便捷计算** - `calculate_payroll_from_params()` (简化参数)

### 年度汇总
- **年度汇总** - `calculate_annual_summary()` (含年终奖分析)

### 辅助功能
- **薪资报告格式化** - `format_salary_report()`
- **涨薪效果分析** - `calculate_salary_increase_effect()`

## 使用示例

### 基础薪资计算

```python
from payroll_utils.mod import *

# 计算小时工资率
hourly = calculate_hourly_rate(10000)  # 月薪10000 -> 57.47元/小时

# 计算日工资率
daily = calculate_daily_rate(10000)    # 月薪10000 -> 459.77元/天

# 薪资类型转换
monthly = convert_salary(50, SalaryType.HOURLY, SalaryType.MONTHLY)  # 8700元
```

### 加班费计算

```python
# 计算加班费
overtime = calculate_overtime_pay(50, {
    'weekday': 20,    # 20小时工作日加班
    'weekend': 10,    # 10小时周末加班
    'holiday': 8,     # 8小时节假日加班
})
# 结果: 50 * (20*1.5 + 10*2 + 8*3) = 2300元

# 从月薪直接计算
overtime = calculate_overtime_pay_from_monthly(10000, {'weekday': 10})
```

### 社保和公积金计算

```python
# 上海社保计算
si = calculate_social_insurance(10000, CityCode.SHANGHAI)
print(f"个人社保: ¥{si.total_employee}")  # 1050元 (养老800+医疗200+失业50)
print(f"单位社保: ¥{si.total_employer}")

# 上海公积金计算
hf = calculate_housing_fund(10000, CityCode.SHANGHAI)
print(f"个人公积金: ¥{hf.amount_employee}")  # 700元
print(f"单位公积金: ¥{hf.amount_employer}")  # 700元

# 不同城市对比
for city in [CityCode.BEIJING, CityCode.SHANGHAI, CityCode.GUANGZHOU]:
    si = calculate_social_insurance(10000, city)
    hf = calculate_housing_fund(10000, city)
    print(f"{city.value}: 社保¥{si.total_employee}, 公积金¥{hf.amount_employee}")
```

### 个税计算

```python
# 简化个税计算
tax = calculate_simple_monthly_tax(15000)  # 790元

# 含扣除项计算
tax = calculate_simple_monthly_tax(
    gross_salary=20000,
    social_insurance=1600,
    housing_fund=1400,
    special_deductions=1000  # 专项附加扣除
)

# 累计预扣预缴
result = calculate_monthly_tax(
    monthly_income=15000,
    cumulative_income=30000,  # 已累计收入
    cumulative_tax=790,       # 已累计税额
    social_insurance=1050,
    housing_fund=700,
)
print(f"本期应纳税额: ¥{result.tax_amount}")
```

### 年终奖计算

```python
# 单独计税
bonus = calculate_year_end_bonus_separate(36000)
print(f"税额: ¥{bonus.tax_amount}")  # 1080元
print(f"税后: ¥{bonus.net_bonus}")   # 34920元

# 比较两种计税方式
comparison = compare_year_end_bonus_methods(50000, 15000)
print(f"单独计税税额: ¥{comparison['separate']['tax_amount']}")
print(f"合并计税税额: ¥{comparison['combined']['tax_amount']}")
print(f"推荐方式: {comparison['recommended_method']}")

# 检查临界点陷阱
# 年终奖36001比36000多交约2300元税
optimal = find_year_end_bonus_optimal_split(36001, 10000)
if not optimal.get('no_split_needed'):
    print(f"建议拆分: ¥{optimal['split_amount']}")
    print(f"节省税额: ¥{optimal['tax_saved']}")
```

### 完整薪资计算

```python
# 使用SalaryParams对象
params = SalaryParams(
    basic_salary=15000,
    overtime_hours={'weekday': 10, 'weekend': 8},
    bonus=2000,
    allowances=500,
    city=CityCode.SHANGHAI,
    special_deductions=1000,
)
result = calculate_payroll(params)

print(f"税前工资: ¥{result.gross_salary}")
print(f"社保(个人): ¥{result.social_insurance}")
print(f"公积金(个人): ¥{result.housing_fund}")
print(f"个人所得税: ¥{result.income_tax}")
print(f"税后工资: ¥{result.net_salary}")
print(f"单位用工成本: ¥{result.employer_cost}")

# 格式化报告
print(format_salary_report(result))
```

### 便捷函数

```python
# 简化参数计算
result = calculate_payroll_from_params(
    basic_salary=15000,
    overtime_hours={'weekday': 10},
    bonus=1000,
    city='shanghai',
    special_deductions=1000,
)
print(result)  # 返回字典格式
```

### 年度汇总

```python
# 年度收入汇总
annual = calculate_annual_summary(15000, 30000)
print(f"年度税前: ¥{annual['annual_gross']}")
print(f"年度税后: ¥{annual['annual_net']}")
print(f"年度个税: ¥{annual['income_tax']}")
print(f"年终奖税后: ¥{annual['year_end_bonus_net']}")
```

### 涨薪效果分析

```python
# 分析涨薪实际效果
effect = calculate_salary_increase_effect(15000, 5000)
print(f"税前增加: ¥{effect['gross_increase']}")
print(f"税后增加: ¥{effect['net_increase']}")
print(f"实际到手比例: {effect['net_ratio']}%")
```

## 常数和配置

### 个人所得税税率表（2019）

| 月应纳税所得额 | 税率 | 速算扣除数 |
|--------------|------|-----------|
| ≤3000        | 3%   | 0         |
| ≤12000       | 10%  | 210       |
| ≤25000       | 20%  | 1410      |
| ≤35000       | 25%  | 2660      |
| ≤55000       | 30%  | 4410      |
| ≤80000       | 35%  | 7160      |
| >80000       | 45%  | 15160     |

### 社保公积金比例（典型值）

| 城市   | 个人社保 | 单位社保 | 个人公积金 | 单位公积金 |
|-------|---------|---------|-----------|-----------|
| 上海   | 10.5%   | 26.26%  | 7%        | 7%        |
| 北京   | 10.2%   | 26.8%   | 12%       | 12%       |
| 广州   | 10.2%   | 19.5%   | 12%       | 12%       |
| 深圳   | 10.3%   | 21.4%   | 5%        | 5%        |

### 加班费倍数

| 加班类型   | 倍数 |
|-----------|-----|
| 工作日延时 | 1.5x |
| 周末加班   | 2.0x |
| 法定节假日 | 3.0x |

## 注意事项

1. **社保公积金基数**：实际基数需查询当地社保局最新规定，本模块提供典型值仅供参考。
2. **专项附加扣除**：需根据个人实际情况填写（子女教育、住房贷款、赡养老人等）。
3. **年终奖临界点**：年终奖金额处于税率临界点附近时（如36000-36001），税额差异显著，建议优化分配。
4. **城市差异**：不同城市的社保公积金比例和基数上下限不同，请选择正确城市代码。

## 测试

运行测试：

```bash
python test.py
```

## 版本

- 版本：1.0.0
- 日期：2026-05-19
- 作者：AllToolkit Contributors
- 许可：MIT