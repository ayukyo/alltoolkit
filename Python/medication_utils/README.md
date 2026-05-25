# medication_utils - 药物剂量计算工具

用于安全计算和管理药物剂量的实用工具集，零外部依赖。

⚠️ **警告**: 此工具仅供学习和参考用途，不应替代专业医疗建议。实际用药请遵医嘱。

## 功能特性

- **按体重计算剂量** - 根据体重计算合适剂量
- **儿童剂量计算** - 多种儿童剂量计算方法
- **药物浓度转换** - 单位转换（mg/g/mcg等）
- **给药间隔验证** - 检查给药频率是否合理
- **剂量范围检查** - 安全剂量范围验证
- **输液速度计算** - IV输液滴速计算
- **半衰期估算** - 药物半衰期和稳态浓度

## 主要类

### DoseUnit
剂量单位枚举：`MG`, `G`, `MCG`, `ML`, `UNITS`

### WeightUnit
体重单位枚举：`KG`, `LB`

### Route
给药途径枚举：`ORAL`, `IV`, `IM`, `SC`, `TOPICAL`, `INHALATION`

### DoseRange
剂量范围类，包含最小和最大安全剂量。

### MedicationInfo
药物信息类，包含药物名称、剂量范围等。

### MedicationCalculator
主要计算器类，提供完整剂量计算功能。

### InfusionCalculator
输液计算器，计算滴速和输液时间。

### HalfLifeCalculator
半衰期计算器，估算药物代谢。

### DoseConverter
剂量转换器，处理单位转换。

### RenalDoseAdjuster
肾功能剂量调整器。

### DrugInteractionChecker
药物相互作用检查器。

## 使用示例

```python
from medication_utils import MedicationCalculator, DoseUnit, WeightUnit

# 创建计算器
calc = MedicationCalculator()

# 按体重计算剂量
weight_kg = 70
dose_per_kg = 10  # mg/kg
dose = calc.calculate_weight_based_dose(weight_kg, dose_per_kg)
print(f"推荐剂量: {dose} mg")

# 儿童剂量计算（Young's规则）
adult_dose = 500  # mg
child_age_years = 8
child_dose = calc.calculate_child_dose_young(adult_dose, child_age_years)
print(f"儿童剂量: {child_dose} mg")

# 检查剂量范围
from medication_utils import DoseRange
range = DoseRange(min_dose=100, max_dose=400, unit=DoseUnit.MG)
is_safe = range.contains(250)  # True
```

## API 参考

### calculate_weight_based_dose(weight, dose_per_kg)
按体重计算剂量。

### calculate_child_dose_young(adult_dose, age)
使用Young's规则计算儿童剂量。

### calculate_child_dose_clark(adult_dose, weight_kg)
使用Clark's规则计算儿童剂量。

### convert_dose(dose, from_unit, to_unit)
剂量单位转换。

### calculate_infusion_rate(volume_ml, time_hours)
计算输液速度（mL/h）。

## 测试

运行测试：
```bash
python medication_utils/medication_utils_test.py
```

测试覆盖率：63 个测试用例，100% 通过。

---

*最后更新: 2026-05-26*