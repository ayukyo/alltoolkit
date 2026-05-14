# Sleep Cycle Utilities - 睡眠周期计算工具库

💤 **基于睡眠科学的周期计算工具，零外部依赖**

---

## 📋 功能特性

- **睡眠周期计算** - 基于90分钟周期计算最佳入睡/起床时间
- **睡眠质量评估** - 五级质量评估（优秀/良好/一般/较差/不足）
- **睡眠债务追踪** - 计算累计睡眠债务和恢复计划
- **昼夜节律分析** - 判断睡眠类型（早起型/晚睡型等）
- **小睡建议** - 不同类型小睡的时间和时长建议
- **睡眠阶段时间线** - 浅睡/深睡/REM阶段分布
- **睡眠窗口优化** - 计算最佳睡眠时段
- **JSON 序列化** - 支持数据持久化
- **零依赖** - 仅使用 Python 标准库

---

## 🚀 快速开始

### 计算起床时间

```python
from sleep_cycle_utils.mod import SleepCycleCalculator
from datetime import datetime

calc = SleepCycleCalculator()

# 如果现在22:00入睡，计算推荐的起床时间
bed_time = datetime.now().replace(hour=22, minute=0, second=0)
wake_times = calc.calculate_wake_times(bed_time)

for result in wake_times:
    print(f"{result.target_time.strftime('%H:%M')} - {result.quality.value}")
    print(f"  {result.recommendation}")
```

### 计算入睡时间

```python
# 如果需要7:00起床，计算推荐的入睡时间
wake_time = datetime.now().replace(hour=7, minute=0)
bed_times = calc.calculate_bed_times(wake_time)

for result in bed_times:
    print(f"{result.target_time.strftime('%H:%M')} - {result.quality.value}")
```

### 小睡建议

```python
# 获取适合当前时间的小睡建议
nap = calc.get_nap_recommendation()
print(f"推荐小睡时长: {nap.duration_minutes}分钟")
print(f"好处: {nap.benefits}")
print(f"警告: {nap.warnings}")
```

---

## 📚 API 文档

### SleepCycleCalculator 类

#### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `cycle_duration` | int | 90 | 睡眠周期时长（分钟） |
| `fall_asleep_time` | int | 15 | 平均入睡时间（分钟） |
| `target_sleep_hours` | float | 8 | 目标睡眠时长（小时） |

#### 主要方法

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `calculate_wake_times(bed_time)` | List[SleepCycleResult] | 计算推荐起床时间 |
| `calculate_bed_times(wake_time)` | List[SleepCycleResult] | 计算推荐入睡时间 |
| `calculate_optimal_sleep_window(wake_time)` | SleepWindow | 计算最佳睡眠窗口 |
| `calculate_sleep_debt(sleep_records)` | SleepDebt | 计算睡眠债务 |
| `get_nap_recommendation(time)` | NapRecommendation | 获取小睡建议 |
| `analyze_circadian_rhythm(wake, bed, age)` | Dict | 分析昼夜节律 |
| `get_sleep_stages_timeline(bed_time)` | List[Dict] | 获取睡眠阶段时间线 |

### SleepQuality 枚举

| 值 | 说明 | 周期数 |
|------|------|--------|
| `EXCELLENT` | 优秀 | 5+ 周期 |
| `GOOD` | 良好 | 4 周期 |
| `FAIR` | 一般 | 3 周期 |
| `POOR` | 较差 | 2 周期 |
| `INSUFFICIENT` | 不足 | 1 周期 |

### NapType 枚举

| 值 | 说明 | 时长 |
|------|------|------|
| `POWER` | 能量小睡 | 20分钟 |
| `SHORT` | 短小睡 | 30分钟 |
| `IDEAL` | 理想小睡 | 90分钟（完整周期） |
| `LONG` | 长小睡 | 最多3小时 |

---

## 📊 数据结构

### SleepCycleResult

```python
result = wake_times[0]

result.target_time          # 推荐时间
result.cycle_count          # 周期数
result.duration_minutes     # 总时长（分钟）
result.actual_sleep_minutes # 实际睡眠时长
result.quality              # 睡眠质量
result.recommendation       # 建议
```

### SleepDebt

```python
debt = calc.calculate_sleep_debt(records)

debt.target_hours           # 目标时长
debt.actual_hours           # 实际平均时长
debt.debt_hours             # 睡眠债务（小时）
debt.debt_minutes           # 睡眠债务（分钟）
debt.accumulated_days       # 累计天数
debt.recovery_plan          # 恢复计划
```

### NapRecommendation

```python
nap = calc.get_nap_recommendation()

nap.nap_type                # 小睡类型
nap.duration_minutes        # 建议时长
nap.best_time_start         # 最佳开始时间
nap.best_time_end           # 最佳结束时间
nap.benefits                # 好处列表
nap.warnings                # 注意事项
```

---

## 🎯 使用场景

### 日常睡眠规划

```python
# 设置目标起床时间，获取建议入睡时间
wake_time = datetime.now().replace(hour=7, minute=0)
bed_times = calc.calculate_bed_times(wake_time, min_cycles=4, max_cycles=5)

# 选择最佳方案（5个周期）
best = bed_times[0]  # 通常第一个是最推荐的
print(f"建议 {best.target_time.strftime('%H:%M')} 入睡")
```

### 睡眠债务追踪

```python
# 记录一周的睡眠情况
sleep_records = [
    {"date": "2024-01-01", "hours": 6.5},
    {"date": "2024-01-02", "hours": 5.0},
    {"date": "2024-01-03", "hours": 7.0},
    {"date": "2024-01-04", "hours": 6.0},
    {"date": "2024-01-05", "hours": 7.5},
]

debt = calc.calculate_sleep_debt(sleep_records, target_hours=8, recovery_days=3)
print(f"累计睡眠债务: {debt.debt_hours}小时")
print(f"建议恢复计划: {debt.recovery_plan}")
```

### 昼夜节律分析

```python
from datetime import time

# 分析自己的睡眠类型
analysis = calc.analyze_circadian_rhythm(
    preferred_wake_time=time(6, 30),   # 习惯6:30起床
    preferred_bed_time=time(22, 30),   # 习惯22:30入睡
    age=30
)

print(f"你的睡眠类型: {analysis['chronotype_name']}")
print(f"最佳工作时段: {analysis['peak_performance_hours']}")
print(f"能量低谷时段: {analysis['energy_low_hours']}")
```

### 睡眠阶段时间线

```python
# 了解夜间睡眠阶段分布
bed_time = datetime.now().replace(hour=22, minute=0)
timeline = calc.get_sleep_stages_timeline(bed_time, cycle_count=5)

for cycle in timeline:
    print(f"周期 {cycle['cycle']}: {cycle['start_time']} - {cycle['end_time']}")
    for stage in cycle['stages']:
        print(f"  {stage['stage']}: {stage['duration_minutes']}分钟 ({stage['percentage']}%)")
```

### 数据持久化

```python
import json

# 保存计算器配置
calc = SleepCycleCalculator(cycle_duration=85, fall_asleep_time=20)
with open("sleep_config.json", "w") as f:
    f.write(calc.to_json())

# 恢复配置
with open("sleep_config.json", "r") as f:
    calc = SleepCycleCalculator.from_json(f.read())
```

---

## 🧪 测试

```bash
python sleep_cycle_utils/sleep_cycle_utils_test.py
```

测试覆盖：
- 起床/入睡时间计算
- 睡眠质量评估
- 睡眠债务计算
- 小睡建议
- 昼夜节律分析
- 睡眠阶段时间线
- JSON 序列化
- 边界值处理

---

## 📝 示例运行

```bash
python sleep_cycle_utils/examples/usage_examples.py
```

---

## 🔬 睡眠科学背景

### 睡眠周期

一个完整的睡眠周期约**90分钟**，包含：
- **浅睡期 (N1/N2)** - 容易被唤醒，身体开始放松
- **深睡期 (N3)** - 最难唤醒，身体修复，记忆巩固
- **REM睡眠** - 快速眼动期，做梦，记忆整合

### 最佳起床时机

在周期**末尾**醒来最清醒，在周期**中间**醒来会有睡眠惯性（昏昏沉沉）。

### 周期建议

| 周期数 | 睡眠时长 | 适用人群 |
|--------|----------|----------|
| 6周期 | ~9小时 | 长睡眠者、青少年 |
| 5周期 | ~7.5小时 | 大多数成年人（推荐） |
| 4周期 | ~6小时 | 短睡眠者、临时情况 |
| 3周期 | ~4.5小时 | 紧急情况，不推荐长期 |

---

## 📦 模块结构

```
sleep_cycle_utils/
├── mod.py                 # 主模块
├── sleep_cycle_utils_test.py  # 测试文件
├── README.md              # 本文档
└── examples/
    └── usage_examples.py  # 使用示例
```

---

## 🔗 相关模块

- `pomodoro_utils` - 番茄钟时间管理
- `clock_utils` - 时钟/闹钟
- `datetime_utils` - 日期时间处理
- `timer_utils` - 通用计时器

---

## 📄 许可证

MIT License - 零依赖，自由使用

---

**最后更新**: 2026-05-14