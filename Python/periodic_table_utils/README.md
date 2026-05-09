# Periodic Table Utils - 化学元素周期表工具

一个完整的化学元素周期表工具包，支持元素查询、分子量计算、周期表操作等功能。

## 特性

- ✅ **完整元素数据**: 包含全部118种元素的详细信息
- ✅ **多方式查询**: 支持原子序数、符号、中文名、英文名查询
- ✅ **分子量计算**: 自动解析化学式并计算分子量
- ✅ **周期表操作**: 按周期、族、分类获取元素
- ✅ **元素比较**: 比较两个元素的属性差异
- ✅ **相邻元素**: 获取元素在周期表中的邻居
- ✅ **常见化合物**: 获取元素的常见化合物列表
- ✅ **零外部依赖**: 纯Python实现

## 安装

无需安装，直接导入使用：

```python
from periodic_table_utils.mod import get_element, calculate_molecular_weight
```

## 快速开始

### 1. 查询元素信息

```python
from periodic_table_utils.mod import get_element, format_element_info

# 按原子序数查询
element = get_element(79)  # 金

# 按符号查询
element = get_element("Fe")  # 铁

# 按中文名查询
element = get_element("碳")  # Carbon

# 按英文名查询
element = get_element("oxygen")  # Oxygen

# 格式化输出
print(format_element_info(element))
```

输出示例：
```
╔══════════════════════════════╗
║           金 (Au)            ║
╠══════════════════════════════╣
║ 原子序数: 79                 ║
║ 英文名: Gold                 ║
║ 原子量: 196.97               ║
║ 分类: 过渡金属               ║
║ 周期: 6  族: 11             ║
║ 电子排布: [Xe]4f14 5d10 6s1  ║
║ 常温状态: 固态               ║
║ 密度: 19.282 g/cm³          ║
║ 熔点: 1337.33 K             ║
║ 沸点: 3129 K                ║
╚══════════════════════════════╝
```

### 2. 计算分子量

```python
from periodic_table_utils.mod import calculate_molecular_weight

# 计算 H2O 分子量
mass, composition = calculate_molecular_weight("H2O")
print(f"分子量: {mass} g/mol")  # 18.015
print(f"组成: {composition}")   # {'H': 2, 'O': 1}

# 计算葡萄糖分子量
mass, composition = calculate_molecular_weight("C6H12O6")
print(f"分子量: {mass} g/mol")  # 180.156

# 计算硫酸分子量
mass, composition = calculate_molecular_weight("H2SO4")
print(f"分子量: {mass} g/mol")  # 98.079
```

### 3. 获取周期/族元素

```python
from periodic_table_utils.mod import get_elements_by_period, get_elements_by_group

# 第一周期元素
elements = get_elements_by_period(1)
print([e.symbol for e in elements])  # ['H', 'He']

# 第一族（碱金属）
elements = get_elements_by_group(1)
print([e.symbol for e in elements])  # ['Li', 'Na', 'K', 'Rb', 'Cs', 'Fr']

# 第18族（稀有气体）
elements = get_elements_by_group(18)
print([e.symbol for e in elements])  # ['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn', 'Og']
```

### 4. 按分类获取元素

```python
from periodic_table_utils.mod import get_elements_by_category, ElementCategory

# 稀有气体
noble_gases = get_elements_by_category(ElementCategory.NOBLE_GAS)
print([e.symbol for e in noble_gases])  # ['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn', 'Og']

# 碱金属
alkali_metals = get_elements_by_category(ElementCategory.ALKALI_METAL)
print([e.symbol for e in alkali_metals])  # ['Li', 'Na', 'K', 'Rb', 'Cs', 'Fr']

# 镧系元素
lanthanides = get_elements_by_category(ElementCategory.LANTHANIDE)
print(len(lanthanides))  # 15 (La-Lu)
```

### 5. 搜索元素

```python
from periodic_table_utils.mod import search_elements

# 按中文名搜索
elements = search_elements("氧")
print([e.symbol for e in elements])  # ['O']

# 按英文名部分搜索
elements = search_elements("gen")
print([e.symbol for e in elements])  # ['H', 'N', 'O'] (Hydrogen, Nitrogen, Oxygen)
```

### 6. 比较元素

```python
from periodic_table_utils.mod import compare_elements

comparison = compare_elements("Fe", "Cu")
print(comparison)
# {
#     '元素1': '铁 (Fe)',
#     '元素2': '铜 (Cu)',
#     '原子序数差异': 3,
#     '原子量差异': 8.125,
#     '同周期': True,
#     '同族': False,
#     '同类': True,
#     ...
# }
```

### 7. 获取相邻元素

```python
from periodic_table_utils.mod import get_element_neighbors

neighbors = get_element_neighbors("C")  # 碳
print(f"左侧: {neighbors['left'].symbol}")   # B
print(f"右侧: {neighbors['right'].symbol}")  # N
```

### 8. 获取常见化合物

```python
from periodic_table_utils.mod import get_common_compounds

compounds = get_common_compounds("Fe")
print(compounds)  # ['Fe2O3', 'Fe3O4', 'FeSO4', 'FeCl3', 'Fe(OH)3']

compounds = get_common_compounds("H")
print(compounds)  # ['H2O', 'H2', 'HCl', 'H2SO4', 'HNO3', 'NH3', 'CH4', 'H2O2']
```

## 元素数据

每个元素包含以下信息：

| 属性 | 描述 | 示例 |
|------|------|------|
| atomic_number | 原子序数 | 79 |
| symbol | 元素符号 | Au |
| name | 中文名称 | 金 |
| name_en | 英文名称 | Gold |
| atomic_mass | 原子量 | 196.97 |
| category | 分类 | 过渡金属 |
| period | 周期 | 6 |
| group | 族 | 11 |
| electron_configuration | 电子排布 | [Xe]4f14 5d10 6s1 |
| state | 常温状态 | 固态/液态/气态 |
| melting_point | 熔点(K) | 1337.33 |
| boiling_point | 沸点(K) | 3129 |
| density | 密度(g/cm³) | 19.282 |
| discovery_year | 发现年份 | None（古代已知） |
| discoverer | 发现者 | None |

## 元素分类

支持以下元素分类：

- `ALKALI_METAL` - 碱金属
- `ALKALINE_EARTH_METAL` - 碱土金属
- `TRANSITION_METAL` - 过渡金属
- `POST_TRANSITION_METAL` - 后过渡金属
- `METALLOID` - 准金属
- `NONMETAL` - 非金属
- `HALOGEN` - 卤素
- `NOBLE_GAS` - 稀有气体
- `LANTHANIDE` - 镧系元素
- `ACTINIDE` - 锕系元素

## 测试

运行测试：

```bash
cd Python/periodic_table_utils
python test.py
```

## 许可

MIT License