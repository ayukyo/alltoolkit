# Biorhythm Utils


AllToolkit - Biorhythm Utilities Module
========================================
A comprehensive biorhythm calculation and analysis utility module for Python
with zero external dependencies.

Biorhythms are hypothetical cyclic patterns that supposedly regulate human
behavior. While scientifically unproven, they remain popular in some circles
for entertainment and self-reflection purposes.

Features:
    - Calculate three main biorhythm cycles (Physical, Emotional, Intellectual)
    - Calculate secondary cycles (Intuitive, Aesthetic, Awareness, Spiritual)
    - Find critical days (zero crossings)
    - Find peak and low days
    - Biorhythm chart generation (ASCII)
    - Compatibility analysis between two individuals
    - Batch date analysis
    - Chinese zodiac integration

Author: AllToolkit Contributors
License: MIT


## 功能

### 类

- **CycleType**: Biorhythm cycle types
- **BiorhythmValue**: Single biorhythm cycle value
- **BiorhythmResult**: Complete biorhythm calculation result
  方法: get_cycle, get_all_cycles, get_summary
- **CriticalDay**: A critical day (zero crossing) event
- **PeakDay**: A peak or low day event

### 函数

- **calculate_days_alive(birth_date, target_date**) - Calculate the number of days between birth date and target date.
- **calculate_biorhythm(days, period**) - Calculate biorhythm value for a given period.
- **calculate_phase(days, period**) - Calculate the phase angle of the biorhythm cycle.
- **calculate_days_in_cycle(days, period**) - Calculate the number of days into the current cycle.
- **get_biorhythm_value(cycle_type, days_alive**) - Calculate complete biorhythm value for a cycle type.
- **calculate_biorhythms(birth_date, target_date, include_secondary**) - Calculate all biorhythm values for a given date.
- **find_critical_days(birth_date, start_date, days**, ...) - Find critical days (zero crossings) within a date range.
- **find_peak_days(birth_date, start_date, days**, ...) - Find peak and low days within a date range.
- **generate_ascii_chart(birth_date, start_date, days**, ...) - Generate an ASCII art chart of biorhythm cycles.
- **calculate_compatibility(birth_date1, birth_date2, target_date**) - Calculate biorhythm compatibility between two individuals.

... 共 19 个函数

## 使用示例

```python
from mod import calculate_days_alive

# 使用 calculate_days_alive
result = calculate_days_alive()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
