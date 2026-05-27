# Menstrual Cycle Utils - 月经周期计算工具

一个零外部依赖的月经周期计算工具，支持周期预测、排卵日计算、易孕期判断等功能。

## 功能特性

- ✅ **周期阶段判断** - 月经期、卵泡期、排卵期、黄体期
- ✅ **生育能力评估** - 低、中、高三档生育能力等级
- ✅ **周期预测** - 预测下次月经、排卵日、易孕期
- ✅ **安全期计算** - 经期前后安全期计算
- ✅ **规律性分析** - 基于历史数据分析周期规律性
- ✅ **多周期预测** - 支持预测多个连续周期
- ✅ **个性化建议** - 饮食、运动、生活建议

## 安装

```bash
# 无需安装，直接复制使用
```

## 快速开始

### 基础使用

```python
from datetime import datetime
from menstrual_cycle import MenstrualCycleCalculator

# 上次月经开始日期
last_period = datetime(2024, 1, 1)

# 创建计算器（周期28天，经期5天）
calc = MenstrualCycleCalculator(last_period, cycle_length=28, period_length=5)

# 预测下一个周期
pred = calc.predict()

print(f"下次月经: {pred.next_period_start.strftime('%Y-%m-%d')}")
print(f"排卵日: {pred.ovulation_date.strftime('%Y-%m-%d')}")
print(f"易孕期: {pred.fertile_window_start.strftime('%Y-%m-%d')} - {pred.fertile_window_end.strftime('%Y-%m-%d')}")
```

### 查询某天状态

```python
# 查询今天的状态
today = datetime.now()
day_info = calc.get_day_info(today)

print(f"周期第{day_info.day_of_cycle}天")
print(f"阶段: {day_info.phase.value}")
print(f"生育能力: {day_info.fertility.value}")
print(f"是否经期: {day_info.is_period}")
print(f"是否排卵日: {day_info.is_ovulation}")
print(f"是否易孕期: {day_info.is_fertile}")
print(f"是否安全期: {day_info.is_safe}")
```

### 周期规律性分析

```python
# 使用历史周期数据
history = [27, 28, 29, 28, 27, 28, 30, 28]
calc = MenstrualCycleCalculator(
    last_period,
    cycle_length=28,
    period_length=5,
    cycle_history=history
)

analysis = calc.analyze_regularity()
print(f"平均周期: {analysis.average_length} 天")
print(f"周期范围: {analysis.min_length} - {analysis.max_length} 天")
print(f"规律性评分: {analysis.regularity_score}/100")
print(f"是否规律: {'是' if analysis.is_regular else '否'}")
```

### 获取个性化建议

```python
recommendations = calc.get_recommendations(today)
for category, items in recommendations.items():
    print(f"\n{category}:")
    for item in items:
        print(f"  - {item}")
```

## 便捷函数

```python
from menstrual_cycle import calculate_next_period, get_fertile_days, get_ovulation_date

last_period = datetime(2024, 1, 1)

# 快速获取下次月经日期
next_start, next_end = calculate_next_period(last_period, cycle_length=28)

# 快速获取易孕期
fertile_start, fertile_end = get_fertile_days(last_period)

# 快速获取排卵日
ovulation = get_ovulation_date(last_period)
```

## 周期阶段说明

| 阶段 | 天数（28天周期） | 特点 |
|------|------------------|------|
| 月经期 | 第1-5天 | 子宫内膜脱落，出血 |
| 卵泡期 | 第6-11天 | 卵泡发育，雌激素上升 |
| 排卵期 | 第12-16天 | 卵子释放，最易受孕 |
| 黄体期 | 第17-28天 | 黄体形成，孕激素上升 |

## 生育能力等级

| 等级 | 说明 | 天数（28天周期） |
|------|------|------------------|
| LOW | 低（安全期） | 第1-8天, 第21-28天 |
| MEDIUM | 中等 | 第9-11天 |
| HIGH | 高（易孕期） | 第12-16天 |

## 注意事项

⚠️ **免责声明**：本工具仅供参考，不构成医疗建议。个体差异可能导致实际情况与预测结果不同。如有健康问题，请咨询专业医生。

## License

MIT License