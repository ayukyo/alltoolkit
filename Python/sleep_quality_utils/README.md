# Sleep Quality Utils


Sleep Quality Utils - 睡眠质量分析工具

零依赖的睡眠质量分析库，支持：
- 睡眠记录和评分
- 睡眠效率计算
- 睡眠债务计算
- 最佳睡眠时间建议
- 睡眠周期分析
- 睡眠趋势分析
- 睡眠阶段分布

Author: AllToolkit
License: MIT


## 功能

### 枚举类

- **SleepStage**: 睡眠阶段枚举 (AWAKE/LIGHT/DEEP/REM)
- **SleepQuality**: 睡眠质量等级 (EXCELLENT/GOOD/FAIR/POOR/VERY_POOR)

### 数据类

- **SleepSession**: 单次睡眠记录
- **SleepAnalysis**: 睡眠分析结果
- **SleepTracker**: 睡眠追踪器（管理多日记录）

### 核心函数

- **calculate_sleep_quality_score(session, age_group)** - 计算睡眠质量评分 (0-100)
- **get_quality_level(score)** - 根据评分获取睡眠质量等级
- **calculate_sleep_debt(sessions, target_hours, days)** - 计算睡眠债务
- **calculate_sleep_efficiency(session)** - 计算睡眠效率
- **suggest_optimal_sleep_time(wake_time, target_hours, num_cycles)** - 建议最佳睡眠时间
- **analyze_sleep_patterns(sessions)** - 分析睡眠模式
- **analyze_sleep_cycles(sleep_duration_hours)** - 分析睡眠周期
- **generate_sleep_recommendations(analysis, age_group)** - 生成睡眠改进建议
- **analyze_sleep_session(session, age_group, target_hours)** - 综合分析单次睡眠
- **calculate_optimal_wake_times(bedtime, min_cycles, max_cycles)** - 计算最佳醒来时间
- **format_sleep_duration(duration)** - 格式化睡眠时长
- **get_sleep_stage_distribution(session)** - 获取睡眠阶段分布
- **estimate_sleep_stages(total_sleep_minutes, age)** - 根据总睡眠时长估算各阶段时长
- **calculate_sleep_onset_latency(hours_in_bed_before_sleep)** - 评估入睡潜伏期
- **get_nap_recommendation(nap_duration_minutes)** - 获取小睡建议
- **calculate_ideal_nap_time(last_night_sleep_hours, sleep_debt_hours)** - 计算理想小睡时长

### 常量

- **OPTIMAL_SLEEP_HOURS**: 各年龄组最佳睡眠时长
- **SLEEP_CYCLE_DURATION**: 睡眠周期时长 (90分钟)
- **IDEAL_SLEEP_STAGE_PERCENTAGES**: 理想睡眠阶段占比

## 使用示例

```python
from datetime import datetime, timedelta
from mod import (
    SleepSession, SleepStage, SleepTracker,
    analyze_sleep_session, suggest_optimal_sleep_time,
    calculate_optimal_wake_times, analyze_sleep_cycles
)

# 创建睡眠记录
session = SleepSession(
    start_time=datetime(2026, 4, 29, 23, 0),
    end_time=datetime(2026, 4, 30, 7, 0),
    awakenings=1,
    awakening_duration_minutes=15,
    sleep_stages={
        SleepStage.DEEP: 90,
        SleepStage.LIGHT: 250,
        SleepStage.REM: 85
    }
)

# 综合分析
analysis = analyze_sleep_session(session, "adult", 8.0)
print(f"质量评分: {analysis.quality_score:.2f}")
print(f"质量等级: {analysis.quality_level.value}")
print(f"睡眠效率: {analysis.efficiency:.2f}%")

# 建议最佳睡眠时间
bedtime, wake_time = suggest_optimal_sleep_time(
    datetime(2026, 4, 30, 7, 0), num_cycles=5
)
print(f"建议入睡时间: {bedtime.strftime('%H:%M')}")

# 使用追踪器
tracker = SleepTracker(target_hours=8.0)
tracker.add_session(session)
print(f"睡眠债务: {tracker.get_sleep_debt(7):.2f} 小时")
```

## 测试

运行测试：

```bash
python sleep_quality_utils_test.py
```

## 文件结构

```
sleep_quality_utils/
├── mod.py                      # 主模块
├── sleep_quality_utils_test.py # 测试文件
├── README.md                   # 本文档
└── examples/                   # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-30