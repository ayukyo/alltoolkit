# Chemical Formula Utils

化学公式解析和计算工具，零依赖。

## 功能特性

- **公式解析**: 解析化学式为元素组成
- **分子量计算**: 计算化合物分子量
- **元素计数**: 统计各元素原子数
- **公式验证**: 验证化学式合法性
- **公式简化**: 简化和规范化化学式

## 快速开始

```python
from chemical_formula_utils.mod import parse_formula, calculate_molecular_weight

# 解析化学式
composition = parse_formula("H2O")
print(composition)  # {'H': 2, 'O': 1}

# 计算分子量
weight = calculate_molecular_weight("H2SO4")
print(weight)  # 98.079
```

## 使用示例

### 公式解析

```python
from chemical_formula_utils.mod import parse_formula, parse_and_validate

# 解析化学式
result = parse_formula("C6H12O6")  # 葡萄糖
print(result.elements)  # {'C': 6, 'H': 12, 'O': 6}
print(result.total_atoms)  # 24

# 复杂公式
result = parse_formula("Fe2(SO4)3")  # 硫酸铁
print(result.elements)  # {'Fe': 2, 'S': 3, 'O': 12}

# 解析并验证
result, is_valid = parse_and_validate("NaCl")
```

### 分子量计算

```python
from chemical_formula_utils.mod import calculate_molecular_weight

# 常见化合物
print(calculate_molecular_weight("H2O"))      # 18.015 (水)
print(calculate_molecular_weight("CO2"))      # 44.009 (二氧化碳)
print(calculate_molecular_weight("CH4"))      # 16.043 (甲烷)
print(calculate_molecular_weight("H2SO4"))    # 98.079 (硫酸)
print(calculate_molecular_weight("NaCl"))     # 58.443 (氯化钠)
print(calculate_molecular_weight("C6H12O6"))  # 180.156 (葡萄糖)
```

### 元素计数

```python
from chemical_formula_utils.mod import count_elements

# 统计元素
counts = count_elements("Al2(SO4)3")
print(counts)  # {'Al': 2, 'S': 3, 'O': 12}

# 总原子数
total = sum(counts.values())
```

### 公式比较

```python
from chemical_formula_utils.mod import compare_formulas, are_equivalent

# 比较两个化学式
result = compare_formulas("H2O", "OH2")
print(result.is_equivalent)  # True（相同元素组成）

# 检查等价性
are_equivalent("C6H6", "C6H6")  # True
```

### 公式简化

```python
from chemical_formula_utils.mod import simplify_formula

# 简化/规范化化学式
simplified = simplify_formula("H2O1")  # "H2O"
simplified = simplify_formula("C1H4")  # "CH4"
```

### 摩尔计算

```python
from chemical_formula_utils.mod import moles_to_mass, mass_to_moles

# 摩尔转质量
mass = moles_to_mass("H2O", moles=2.0)
print(mass)  # 36.03 g

# 转摩尔数
moles = mass_to_moles("H2O", mass=18.015)
print(moles)  # 1.0 mol
```

## API 参考

| 函数 | 说明 |
|------|------|
| `parse_formula(formula)` | 解析化学式 |
| `parse_and_validate(formula)` | 解析并验证 |
| `calculate_molecular_weight(formula)` | 计算分子量 |
| `count_elements(formula)` | 统计元素 |
| `compare_formulas(f1, f2)` | 比较化学式 |
| `simplify_formula(formula)` | 简化化学式 |
| `moles_to_mass(formula, moles)` | 摩尔转质量 |
| `mass_to_moles(formula, mass)` | 质量转摩尔 |

### FormulaResult 类

```python
@dataclass
class FormulaResult:
    formula: str              # 原化学式
    elements: Dict[str, int]  # 元素组成
    molecular_weight: float   # 分子量
    total_atoms: int          # 总原子数
    is_valid: bool            # 是否有效
```

## 支持的元素

支持所有标准元素符号，如：
- H, He, Li, Be, B, C, N, O, F, Ne...
- Na, Mg, Al, Si, P, S, Cl, Ar, K, Ca...
- Fe, Cu, Ag, Au, Pt, Pb...

## 应用场景

- **化学教育**: 分子量计算辅助
- **实验室**: 化合物分析
- **数据处理**: 化学数据解析
- **质量计算**: 摩尔换算

---

**测试覆盖**: 完整测试套件，覆盖公式解析、分子量计算、元素统计等