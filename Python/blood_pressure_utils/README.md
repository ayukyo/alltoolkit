# Blood Pressure Utils - 血压分析工具

血压分析工具模块，提供完整的血压分析功能，零外部依赖。

## 功能特性

- **血压分类** - WHO 和中国高血压分类标准
- **年龄特定范围** - 儿童(1-17岁)和成人年龄对应的正常血压范围
- **脉压差分析** - 脉压差计算和分类
- **平均动脉压(MAP)** - MAP 计算和状态评估
- **风险评估** - 血压风险等级评估
- **统计分析** - 血压统计数据和趋势分析
- **儿童血压** - 儿童血压百分位数计算

## 安装使用

```python
from blood_pressure_utils.mod import analyze_bp, calculate_pulse_pressure, calculate_map

# 完整血压分析
result = analyze_bp(120, 80, age=35)
print(result.category_label)  # '理想血压'
print(result.pulse_pressure)  # 40 mmHg
print(result.map)  # 93.33 mmHg

# 脉压差计算
pp = calculate_pulse_pressure(120, 80)  # 40

# MAP 计算
map_value = calculate_map(120, 80)  # 93.33
```

## 主要函数

### analyze_bp(systolic, diastolic, age)
完整血压分析，返回 `BPResult` 对象，包含：
- `category` - 血压分类
- `category_label` - 中文分类标签
- `risk_level` - 风险等级
- `pulse_pressure` - 脉压差
- `map` - 平均动脉压
- `recommendations` - 健康建议列表

### classify_bp(systolic, diastolic)
WHO 标准血压分类，返回分类信息。

### calculate_bp_statistics(readings)
计算血压统计数据，支持趋势分析。

### analyze_child_bp(systolic, diastolic, age, gender)
儿童血压分析，计算百分位数。

## 血压分类标准

| 分类 | 收缩压 | 舒张压 | 说明 |
|------|--------|--------|------|
| 理想血压 | <120 | <80 | 心血管风险最低 |
| 正常血压 | 120-129 | 80-84 | 正常范围 |
| 正常高值 | 130-139 | 85-89 | 建议改善生活方式 |
| 高血压1级 | 140-159 | 90-99 | 可能需要药物治疗 |
| 高血压2级 | 160-179 | 100-109 | 需要药物治疗 |
| 高血压3级 | ≥180 | ≥110 | 需立即就医 |

## 单位转换

支持 mmHg 和 kPa 单位转换：
- `mmhg_to_kpa(120)` → 15.96 kPa
- `kpa_to_mmhg(16)` → 120.09 mmHg

## 测试

```bash
python blood_pressure_utils/blood_pressure_utils_test.py
```

## 许可证

MIT License