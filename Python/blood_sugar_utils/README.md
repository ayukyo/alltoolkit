# Blood Sugar Utils - 血糖计算工具

一个实用的血糖计算和评估工具，支持血糖单位转换、状态评估、HbA1c转换、胰岛素剂量计算等功能。

## 功能特性

- ✅ **血糖单位转换** - mg/dL ↔ mmol/L 双向转换
- ✅ **血糖状态评估** - 根据空腹/餐后血糖评估健康状态
- ✅ **HbA1c转换** - 糖化血红蛋白与平均血糖双向转换
- ✅ **平均血糖估算** - 多次读数的统计分析
- ✅ **血糖趋势分析** - 分析血糖变化趋势和预测
- ✅ **胰岛素剂量计算** - 餐时胰岛素和校正剂量计算
- ✅ **血糖报告生成** - 完整的血糖分析报告

## 零外部依赖

纯 Python 实现，无需任何第三方依赖。

## 安装使用

```python
from blood_sugar_utils import mgdl_to_mmol, assess_glucose

# 单位转换
print(mgdl_to_mmol(100))  # 5.55 mmol/L

# 血糖评估
result = assess_glucose(5.5, fasting=True)
print(result['status'])  # 正常（空腹）
```

## API 参考

### 单位转换

```python
from blood_sugar_utils import convert_glucose, mgdl_to_mmol, mmol_to_mgdl, GlucoseUnit

# 通用转换函数
convert_glucose(value, from_unit, to_unit)

# 便捷函数
mgdl_to_mmol(100)  # -> 5.55
mmol_to_mgdl(5.5)  # -> 99.1
```

### 血糖评估

```python
from blood_sugar_utils import assess_glucose, GlucoseUnit

# 空腹血糖评估
result = assess_glucose(6.5, GlucoseUnit.MMOL_L, fasting=True)
# 返回: status, risk_level, recommendation 等

# 餐后血糖评估
result = assess_glucose(8.5, GlucoseUnit.MMOL_L, fasting=False)

# 年龄调整评估（老年人标准稍宽）
result = assess_glucose(6.0, GlucoseUnit.MMOL_L, fasting=True, age=70)
```

### HbA1c 转换

```python
from blood_sugar_utils import hba1c_to_average_glucose, average_glucose_to_hba1c

# HbA1c 转平均血糖
result = hba1c_to_average_glucose(6.5)
print(result['avg_glucose_mmol'])  # 7.75 mmol/L

# 平均血糖转 HbA1c
result = average_glucose_to_hba1c(7.8, GlucoseUnit.MMOL_L)
print(result['hba1c'])  # 6.53%
```

### 平均血糖估算

```python
from blood_sugar_utils import estimate_average_glucose, GlucoseUnit

readings = [
    (5.5, GlucoseUnit.MMOL_L),
    (6.0, GlucoseUnit.MMOL_L),
    (5.8, GlucoseUnit.MMOL_L),
]

result = estimate_average_glucose(readings)
# 返回: avg_mmol, std_dev, cv_percent, time_in_range_percent, estimated_hba1c 等
```

### 血糖趋势分析

```python
from blood_sugar_utils import analyze_glucose_trend, GlucoseUnit
from datetime import datetime, timedelta

now = datetime.now()
readings = [
    (5.5, GlucoseUnit.MMOL_L, now - timedelta(hours=2)),
    (6.0, GlucoseUnit.MMOL_L, now - timedelta(hours=1)),
    (6.5, GlucoseUnit.MMOL_L, now),
]

result = analyze_glucose_trend(readings)
# 返回: trend, trend_arrow, slope, predicted_next_mmol 等
```

### 胰岛素剂量计算

```python
from blood_sugar_utils import calculate_insulin_sensitivity, carbohydrate_to_insulin

# 校正剂量计算
result = calculate_insulin_sensitivity(
    current_glucose=10.0,  # 当前血糖 mmol/L
    target_glucose=6.0,    # 目标血糖 mmol/L
    correction_factor=2.0  # ISF 每单位胰岛素降血糖值
)

# 餐时胰岛素计算
result = carbohydrate_to_insulin(
    carbs=60,  # 碳水化合物克数
    icr=10     # 胰岛素与碳水比
)

# 综合：餐时 + 校正
result = carbohydrate_to_insulin(
    carbs=60, icr=10,
    current_glucose=10.0, target_glucose=6.0, isf=2.0
)
```

### 血糖报告生成

```python
from blood_sugar_utils import glucose_report, GlucoseUnit
from datetime import datetime, timedelta

now = datetime.now()
readings = [
    (5.5, GlucoseUnit.MMOL_L, now - timedelta(hours=i))
    for i in range(10)
]

report = glucose_report(readings)
# 返回完整报告: summary, statistics, time_in_range, hba1c_estimate, assessment
```

## 血糖标准参考

### 空腹血糖标准 (mmol/L)

| 状态 | 范围 | 风险等级 |
|------|------|----------|
| 严重低血糖 | < 2.8 | critical |
| 低血糖 | 2.8 - 3.9 | high |
| 正常 | 3.9 - 5.6 | low |
| 糖尿病前期 | 5.6 - 6.9 | medium |
| 糖尿病 | ≥ 7.0 | high |

### 餐后血糖标准 (mmol/L)

| 状态 | 范围 | 风险等级 |
|------|------|----------|
| 正常 | < 7.8 | low |
| 糖尿病前期 | 7.8 - 11.0 | medium |
| 糖尿病 | ≥ 11.1 | high |

### HbA1c 标准

| 状态 | HbA1c (%) | 风险等级 |
|------|-----------|----------|
| 正常 | < 5.7 | low |
| 糖尿病前期 | 5.7 - 6.4 | medium |
| 糖尿病 | ≥ 6.5 | high |

## 使用示例

完整示例请参考 `examples/usage_examples.py`。

```bash
python -m blood_sugar_utils.examples.usage_examples
```

## 测试

```bash
cd Python/blood_sugar_utils
python -m pytest blood_sugar_utils_test.py -v
```

## 注意事项

⚠️ **本工具仅供参考，不替代专业医疗诊断。实际胰岛素剂量应遵医嘱。**

血糖标准可能因年龄、健康状况等因素有所调整。本工具提供的是通用参考标准。

## 版本

- v1.0.0 - 初始版本