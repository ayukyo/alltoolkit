# Blood Type Utilities - 血型工具模块

提供血型兼容性检测、遗传计算、分布统计等功能。

## 功能特性

### 🩸 血型兼容性检测

- **献血者匹配**: 判断献血者是否可以向受血者献血
- **受血者匹配**: 获取所有可献血给指定血型的献血者列表
- **万能献血者**: O- 型血可献血给所有血型
- **万能受血者**: AB+ 型血可接受所有血型

### 🧬 血型遗传计算

- **孩子血型预测**: 根据父母血型计算孩子可能的血型及概率
- **父母血型推断**: 根据孩子血型推断可能的父母血型组合
- **父母关系验证**: 判断指定血型是否可能是孩子的父母

### 📊 血型分布统计

- **全球分布**: 全球人群血型分布数据
- **中国分布**: 中国人群血型分布数据（Rh阴性更稀有）
- **美国分布**: 美国人群血型分布数据
- **稀有血型检测**: 判断血型是否为稀有血型

### 🔬 血型详细信息

- **抗原抗体**: 查询血型的抗原和抗体信息
- **基因型**: 查询血型可能的基因型组合
- **格式化**: 多种格式显示血型（简短、完整、中文）

## 快速使用

```python
from blood_type_utils import BloodType, BloodTypeUtils, can_donate, parse_blood_type

# 解析血型
bt = parse_blood_type("A+")
print(bt)  # BloodType.A_POSITIVE

# 血型兼容性
print(can_donate("O-", "A+"))  # True - O- 可以献血给 A+
print(can_donate("A+", "O-"))  # False - A+ 不能献血给 O-

# 获取兼容献血者
donors = BloodTypeUtils.get_compatible_donors(BloodType.O_NEGATIVE)
print([d.value for d in donors])  # ['O-'] - O- 只能接受 O-

# 获取可献血对象
recipients = BloodTypeUtils.get_compatible_recipients(BloodType.O_NEGATIVE)
print(len(recipients))  # 8 - O- 可以献血给所有血型

# 遗传计算
children = BloodTypeUtils.calculate_child_blood_types(
    BloodType.A_POSITIVE, BloodType.B_POSITIVE
)
for bt, prob in children.items():
    print(f"{bt.value}: {prob:.1f}%")

# 血型详细信息
info = BloodTypeUtils.get_blood_type_info(BloodType.O_NEGATIVE)
print(f"抗原: {info.antigens}")      # []
print(f"抗体: {info.antibodies}")    # ['Anti-A', 'Anti-B', 'Anti-D']
print(f"基因型: {info.possible_genotypes}")  # ['OO']
```

## 主要函数

| 函数 | 说明 |
|------|------|
| `parse_blood_type(str)` | 解析血型字符串 |
| `can_donate(donor, recipient)` | 判断是否可以献血 |
| `get_compatible_donors(recipient)` | 获取兼容献血者 |
| `get_compatible_recipients(donor)` | 获取可献血对象 |
| `child_blood_types(parent1, parent2)` | 计算孩子可能的血型 |
| `get_blood_type_info(blood_type)` | 获取血型详细信息 |
| `is_rare_blood_type(blood_type)` | 判断是否稀有血型 |
| `get_population_percentage(bt, population)` | 获取人群分布比例 |

## 血型兼容规则

### ABO 血型系统

| 献血者 | 可献血给 |
|--------|----------|
| O | O, A, B, AB |
| A | A, AB |
| B | B, AB |
| AB | AB |

### Rh 血型系统

- Rh 阴性 (−) 可以献血给 Rh 阳性 (+)
- Rh 阳性 (+) 不能献血给 Rh 阴性 (−)

### 完整兼容矩阵

| 献血者 | 可献血给 |
|--------|----------|
| O- | 所有血型 (万能献血者) |
| O+ | O+, A+, B+, AB+ |
| A- | A+, A-, AB+, AB- |
| A+ | A+, AB+ |
| B- | B+, B-, AB+, AB- |
| B+ | B+, AB+ |
| AB- | AB+, AB- |
| AB+ | AB+ (万能受血者) |

## 血型分布数据

### 全球分布

| 血型 | 比例 |
|------|------|
| O+ | 38% |
| A+ | 27% |
| B+ | 12% |
| AB+ | 4% |
| O- | 7% |
| A- | 5% |
| B- | 3% |
| AB- | 1% |

### 中国分布特点

- Rh 阴性血型在中国非常稀有（< 1%）
- O 型、A 型、B 型分布相对均匀

## 遗传规则

### ABO 遗传

| 父母组合 | 可能的孩子血型 |
|----------|----------------|
| O + O | O |
| A + A | A, O |
| A + B | A, B, AB, O |
| A + AB | A, B, AB |
| A + O | A, O |
| B + B | B, O |
| B + AB | A, B, AB |
| B + O | B, O |
| AB + AB | A, B, AB |
| AB + O | A, B |

### Rh 遗传

- Rh+ 父母 + Rh+ 父母 → 可能 Rh+ 或 Rh-
- Rh+ 父母 + Rh- 父母 → 可能 Rh+ 或 Rh-
- Rh- 父母 + Rh- 父母 → 只能 Rh-

## 零依赖

本模块仅使用 Python 标准库，无需安装任何外部依赖。

## 作者

AllToolkit

## 许可证

MIT