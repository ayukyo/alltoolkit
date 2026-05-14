# BMI Utils ⚖️

BMI（身体质量指数）健康计算工具模块，提供全面的体重和健康指标计算。

## 功能特性

- **BMI 计算** - 公制和英制单位支持
- **BMI 分类** - WHO 标准分类
- **理想体重范围** - 根据身高计算
- **BMI Prime** - 相对 BMI 指标
- **体脂率估算** - 基于 BMI 的估算公式
- **儿童 BMI 百分位数** - CDC 数据支持
- **健康风险评估** - 基于 BMI 的风险判断
- **腰高比计算** - 腰围身高比指标
- **BMR 估算** - 基础代谢率计算

## 快速开始

```python
from bmi_utils.mod import calculate_bmi, get_bmi_category, BMIClassifier

# 基础 BMI 计算
bmi = calculate_bmi(weight=70, height=1.75)  # 公制单位
print(f"BMI: {bmi:.1f}")  # 22.9

# 英制单位
bmi = calculate_bmi(weight=154, height=70, unit='imperial')  # 磅和英寸

# BMI 分类
category = get_bmi_category(bmi)
# 'underweight', 'normal', 'overweight', 'obese_class_I', etc.
```

## 核心类

### BMIClassifier

```python
from bmi_utils.mod import BMIClassifier

classifier = BMIClassifier()

# 获取详细信息
info = classifier.get_bmi_info(bmi=22.5)
# {
#     'bmi': 22.5,
#     'category': 'normal',
#     'label': '正常',
#     'label_en': 'Normal',
#     'risk': 'low',
#     'risk_desc': '健康的体重范围'
# }

# 计算理想体重范围
ideal = classifier.get_ideal_weight_range(height=1.75)
# {'min': 56.7, 'max': 76.6}
```

## 主要函数

| 函数 | 说明 |
|------|------|
| `calculate_bmi(weight, height, unit)` | 计算 BMI |
| `get_bmi_category(bmi)` | 获取 BMI 分类 |
| `get_ideal_weight(height)` | 计算理想体重 |
| `estimate_body_fat(bmi, age, gender)` | 估算体脂率 |
| `calculate_bmr(weight, height, age, gender)` | 计算基础代谢率 |
| `calculate_waist_to_height_ratio(waist, height)` | 计算腰高比 |

## BMI 分类标准 (WHO)

| 分类 | BMI 范围 | 健康风险 |
|------|----------|----------|
| 严重偏瘦 | < 16.0 | 高 |
| 偏瘦 | 16.0 - 18.5 | 中等 |
| 正常 | 18.5 - 25.0 | 低 |
| 超重 | 25.0 - 30.0 | 中等 |
| 肥胖 I 级 | 30.0 - 35.0 | 高 |
| 肥胖 II 级 | 35.0 - 40.0 | 很高 |
| 肥胖 III 级 | ≥ 40.0 | 极高 |

## 儿童青少年 BMI

```python
from bmi_utils.mod import calculate_child_bmi_percentile

# 计算 10 岁男孩的 BMI 百分位数
percentile = calculate_child_bmi_percentile(bmi=18.5, age=10, gender='male')
# 返回百分位数 (0-100)
```

## 健康建议

```python
from bmi_utils.mod import get_weight_recommendation

recommendation = get_weight_recommendation(bmi=28, height=1.75)
# {
#     'current_status': 'overweight',
#     'target_weight': {'min': 56.7, 'max': 76.6},
#     'weight_to_lose': 14.0,
#     'weekly_goal': '0.5-1 kg',
#     'time_estimate': '14-28 weeks'
# }
```

## 测试

```bash
python Python/bmi_utils/bmi_utils_test.py
```

## 许可证

MIT License