# Sleep Utils - 睡眠周期与质量计算工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

基于科学睡眠周期理论的睡眠时间计算和优化工具。零依赖，仅使用Python标准库。

## 功能特性

- **睡眠周期计算** - 基于90分钟周期计算最佳起床/就寝时间
- **质量评分** - 根据周期数和时间段计算睡眠质量分数
- **睡眠负债追踪** - 分析累积的睡眠不足情况
- **小睡建议** - 科学的小睡时长和时间建议
- **昼夜节律分析** - 分析作息时型（早鸟/夜猫子/中间型）
- **睡眠阶段分布** - 计算浅睡、深睡、REM时间分布
- **睡眠效率分析** - 评估实际睡眠与在床时间比例

## 快速开始

### 基本用法

```python
from datetime import datetime
from sleep_utils.mod import when_to_wake, when_to_sleep

# 如果23:00就寝，几点起床最佳？
bedtime = datetime(2024, 1, 1, 23, 0)
wake_options = when_to_wake(bedtime)
for opt in wake_options:
    print(f"{opt['wake_time']}起床 - {opt['cycles']}周期 - 质量{opt['quality']}/10")

# 如果7:00起床，几点就寝最佳？
wake_time = datetime(2024, 1, 1, 7, 0)
bed_options = when_to_sleep(wake_time)
for opt in bed_options:
    print(f"{opt['bedtime']}就寝 - {opt['cycles']}周期 - 质量{opt['quality']}/10")
```

### 睡眠负债计算

```python
from sleep_utils.mod import calculate_sleep_debt

# 过去一周的睡眠数据（小时）
sleep_data = [6, 7, 5, 8, 6.5, 7, 6]
debt = calculate_sleep_debt(target_hours=7.5, actual_hours_list=sleep_data)

print(f"累计负债: {debt['debt_hours']}小时")
print(f"平均睡眠: {debt['average_actual']}小时/天")
print(f"状态: {debt['status']}")
```

### 小睡建议

```python
from sleep_utils.mod import suggest_nap

# 20分钟小睡建议
result = suggest_nap(duration_minutes=20)
print(result['suggestions'][0]['description'])  # 强力小睡：快速恢复警觉性

# 下午2点适合小睡吗？
result = suggest_nap(current_hour=14)
print(result['suggestions'][0]['time_advice']['suitability'])  # 最佳
```

## 核心概念

### 睡眠周期

一个完整的睡眠周期约为90分钟，包含：
1. **浅睡眠（N1/N2）** - 身体放松，容易被唤醒
2. **深度睡眠（N3）** - 身体修复，免疫系统增强
3. **REM睡眠** - 梦境发生，记忆巩固

推荐的睡眠周期数为**4-6个**（约6-9小时），最佳为**5个周期**（约7.5小时）。

### 睡眠质量评分

质量分数基于三个因素：
- **周期数** - 5个周期最优（4分）
- **起床时间** - 6-8点最佳（3分）
- **总睡眠时长** - 7-9小时最优（3分）

满分10分，评级：
- 9-10分：优秀（excellent）
- 7-8分：良好（good）
- 5-6分：一般（fair）
- 3-4分：较差（poor）
- 1-2分：很差（very_poor）

### 昼夜节律时型

根据起床时间自动判断：
- **早鸟型** - 6点前起床，自然偏向早睡早起
- **夜猫子型** - 9点后起床，适合晚睡晚起
- **中间型** - 6-9点起床，可灵活适应

## API 参考

### 计算函数

| 函数 | 用途 |
|------|------|
| `calculate_wake_times(bedtime)` | 根据就寝时间计算起床时间 |
| `calculate_bedtimes(wake_time)` | 根据起床时间计算就寝时间 |
| `calculate_quality_score(cycles, wake_time)` | 计算睡眠质量分数 |
| `calculate_sleep_debt(target_hours, actual_hours_list)` | 计算睡眠负债 |
| `suggest_nap(duration_minutes, current_hour)` | 小睡建议 |
| `analyze_circadian_rhythm(wake_time, bedtime)` | 昼夜节律分析 |
| `get_sleep_stage_distribution(cycles)` | 睡眠阶段分布 |
| `calculate_sleep_efficiency(in_bed, actual_sleep)` | 睡眠效率 |

### 便捷函数

| 函数 | 用途 |
|------|------|
| `when_to_wake(bedtime)` | 快速获取起床时间列表 |
| `when_to_sleep(wake_time)` | 快速获取就寝时间列表 |

### 类

| 类 | 用途 |
|----|------|
| `SleepCycleResult` | 睡眠周期计算结果对象 |
| `SleepQuality` | 睡眠质量等级常量 |
| `CircadianRhythm` | 昼夜节律时间段分析 |

## 运行测试

```bash
python Python/sleep_utils/sleep_utils_test.py
```

测试覆盖：
- 睡眠周期计算（起床/就寝时间）
- 质量评分算法
- 睡眠负债计算
- 小睡建议（时长、时间、疲劳度）
- 昼夜节律分析（时型、年龄段）
- 睡眠阶段分布
- 睡眠效率分析
- 边界情况（午夜、极端值）
- 一致性验证

## 运行示例

```bash
python Python/sleep_utils/examples/usage_examples.py
```

## 常量配置

| 常量 | 默认值 | 说明 |
|------|--------|------|
| `SLEEP_CYCLE_MINUTES` | 90 | 一个睡眠周期时长 |
| `FALL_ASLEEP_MINUTES` | 15 | 平均入睡时间 |
| `OPTIMAL_CYCLES` | 5 | 最佳睡眠周期数 |
| `RECOMMENDED_CYCLES_MIN` | 4 | 最少推荐周期数 |
| `RECOMMENDED_CYCLES_MAX` | 6 | 最多推荐周期数 |

## 科学依据

- 美国国家睡眠基金会推荐成人睡眠时长：7-9小时
- 睡眠周期理论：每个周期约90分钟
- 昼夜节律：褪黑素分泌高峰在22:00-02:00
- 睡眠效率：健康成年人应达到85%以上

## 许可证

MIT License