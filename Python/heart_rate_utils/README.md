# Heart Rate Utils - 心率工具库

提供心率计算、训练区间、燃脂心率、卡路里消耗等功能，零外部依赖，纯 Python 实现。

## 功能特性

- **最大心率计算**: 支持 8 种计算公式（Tanaka、Gellish、Arena、Inbar、NES、Gellish二次公式等）
- **心率训练区间**: Zone 1-5 五个区间，含详细描述和持续时间建议
- **Karvonen 公式**: 心率储备计算，更精准的目标心率
- **燃脂区间**: 最佳燃脂心率计算
- **有氧/无氧区间**: 有氧耐力和无氧阈值心率
- **卡路里消耗**: 基于 Keytel 公式的卡路里估算
- **恢复心率评估**: 心脏健康恢复能力评估
- **心血管健康**: 基于静息心率的健康水平评估
- **训练强度**: 实时强度百分比和区间判断
- **乳酸阈值**: 估算乳酸阈值心率
- **配速估算**: 根据心率估算跑步/骑行/游泳配速
- **心率趋势分析**: 心率统计分析（平均值、标准差、RMSSD、趋势方向）

## 安装使用

```python
from heart_rate_utils.mod import HeartRateUtils, MaxHrFormula, calculate_max_hr, get_zones
```

## 快速开始

### 最大心率计算

```python
from heart_rate_utils.mod import HeartRateUtils, MaxHrFormula

# Tanaka公式（最推荐）
max_hr = HeartRateUtils.calculate_max_hr(30, MaxHrFormula.TANAKA)
print(f"最大心率: {max_hr} bpm")  # 187

# 传统公式 (220 - age)
max_hr = HeartRateUtils.calculate_max_hr(30, MaxHrFormula.STANDARD)
print(f"最大心率: {max_hr} bpm")  # 190

# 所有公式对比
ranges = HeartRateUtils.calculate_max_hr_range(30)
print(ranges)
# {
#   'standard': 190, 'tanaka': 187, 'gellish': 179,
#   'arena': 191, 'inbar': 182, 'nes': 182,
#   'gellish2': 185, 'average': 184
# }
```

### 心率训练区间

```python
from heart_rate_utils.mod import HeartRateUtils

# 计算所有心率区间
result = HeartRateUtils.calculate_zones(30)
print(f"最大心率: {result.max_hr} bpm")

for zone_name, zone_info in result.zones.items():
    print(f"{zone_name} ({zone_info.name}): {zone_info.hr_range.min_hr}-{zone_info.hr_range.max_hr} bpm")
# Zone 1 (恢复区间): 93-112 bpm
# Zone 2 (有氧基础): 112-130 bpm
# Zone 3 (有氧耐力): 130-149 bpm
# Zone 4 (无氧阈值): 149-168 bpm
# Zone 5 (最大努力): 168-187 bpm

# 使用 Karvonen 公式（更精准）
result = HeartRateUtils.calculate_zones(30, resting_hr=60, use_karvonen=True)
print(f"心率储备: {result.heart_rate_reserve} bpm")  # 127
```

### 燃脂区间

```python
from heart_rate_utils.mod import HeartRateUtils

fat_zone = HeartRateUtils.calculate_fat_burning_zone(30)
print(f"燃脂心率范围: {fat_zone['hr_range']['min']}-{fat_zone['hr_range']['max']} bpm")
print(f"最佳燃脂心率: {fat_zone['optimal_hr']} bpm")  # 121
```

### 卡路里消耗

```python
from heart_rate_utils.mod import HeartRateUtils

# 估算卡路里消耗
calories = HeartRateUtils.estimate_calories_burned(
    hr=150,           # 平均心率
    duration_minutes=45,  # 运动时长
    weight_kg=70,     # 体重
    age=30,           # 年龄
    gender="male"     # 性别
)
print(f"消耗卡路里: {calories['calories']} kcal")
print(f"运动强度: {calories['intensity']}")
```

### 恢复心率评估

```python
from heart_rate_utils.mod import HeartRateUtils

# 评估心脏恢复能力
recovery = HeartRateUtils.calculate_recovery_hr(
    hr_exercise=160,      # 运动时心率
    hr_recovery_1min=130,  # 1分钟后心率
    hr_recovery_2min=110   # 2分钟后心率（可选）
)
print(f"1分钟下降: {recovery['hr_drop_1min']} bpm")
print(f"恢复评级: {recovery['recovery_rating']}")
print(f"健康风险: {recovery['health_risk']}")
```

### 心血管健康评估

```python
from heart_rate_utils.mod import HeartRateUtils

# 基于静息心率评估心血管健康
fitness = HeartRateUtils.assess_cardiovascular_fitness(
    resting_hr=55,
    age=30,
    gender="male"
)
print(f"健康水平: {fitness['fitness_level']}")
print(f"评级: {fitness['rating']}")
```

### 训练强度计算

```python
from heart_rate_utils.mod import HeartRateUtils

# 实时训练强度
intensity = HeartRateUtils.calculate_training_intensity(
    hr=140,
    age=30,
    resting_hr=60
)
print(f"心率百分比: {intensity['percentage_of_max']}%")
print(f"强度等级: {intensity['intensity_level']}")
print(f"当前区间: {intensity['zone']}")
print(f"颜色编码: {intensity['color_code']}")
```

### 配速估算

```python
from heart_rate_utils.mod import HeartRateUtils

# 跑步配速估算
pace = HeartRateUtils.hr_to_pace_estimate(150, 30, 70, "running")
print(f"估算配速: {pace['estimated_pace_min_per_km']} min/km")
print(f"强度: {pace['intensity']}")

# 骑行速度估算
speed = HeartRateUtils.hr_to_pace_estimate(150, 30, 70, "cycling")
print(f"估算速度: {speed['estimated_speed_kmh']} km/h")

# 游泳配速估算
swim = HeartRateUtils.hr_to_pace_estimate(150, 30, 70, "swimming")
print(f"估算配速: {swim['estimated_pace_min_per_100m']} min/100m")
```

## API 参考

### 最大心率计算

| 方法 | 描述 |
|------|------|
| `calculate_max_hr(age, formula)` | 计算最大心率 |
| `calculate_max_hr_average(age)` | 多公式平均值 |
| `calculate_max_hr_range(age)` | 所有公式对比 |

**支持的公式:**

| 公式 | 代码 | 适用人群 |
|------|------|----------|
| Tanaka (推荐) | `tanaka` | 一般健康成年人 |
| Gellish | `gellish` | 一般健康成年人 |
| Arena | `arena` | 最大摄氧量相关 |
| Inbar | `inbar` | 一般人群 |
| NES/Hunt | `nes` | 健康成年人 |
| Standard (220-age) | `standard` | 传统公式，误差较大 |
| Gellish二次 | `gellish2` | 更精准的二次公式 |

### 心率区间

| 方法 | 描述 |
|------|------|
| `calculate_zones(age, resting_hr, formula, use_karvonen)` | 计算所有心率区间 |
| `get_zone_for_hr(hr, age, resting_hr)` | 根据心率获取当前区间 |

**心率区间定义:**

| Zone | 名称 | 心率百分比 | 描述 | 持续时间 |
|------|------|-----------|------|----------|
| Zone 1 | 恢复区间 | 50-60% | 热身、冷身、恢复 | 20-60分钟 |
| Zone 2 | 有氧基础 | 60-70% | 燃脂区间 | 30-120分钟 |
| Zone 3 | 有氧耐力 | 70-80% | 提高有氧能力 | 20-60分钟 |
| Zone 4 | 无氧阈值 | 80-90% | 乳酸阈值训练 | 2-10分钟 |
| Zone 5 | 最大努力 | 90-100% | 极量训练 | 0-5分钟 |

### 目标心率

| 方法 | 描述 |
|------|------|
| `calculate_target_hr_karvonen(max_hr, resting_hr, intensity)` | Karvonen公式 |
| `calculate_target_hr_simple(max_hr, percentage)` | 简单百分比 |
| `calculate_heart_rate_reserve(max_hr, resting_hr)` | 心率储备 |

### 专项区间

| 方法 | 描述 |
|------|------|
| `calculate_fat_burning_zone(age)` | 燃脂区间 |
| `calculate_cardio_zone(age)` | 有氧区间 |
| `calculate_anaerobic_zone(age)` | 无氧区间 |
| `calculate_lactate_threshold_hr(age, method)` | 乳酸阈值 |

### 卡路里和健康

| 方法 | 描述 |
|------|------|
| `estimate_calories_burned(hr, duration, weight, age, gender)` | 卡路里估算 |
| `calculate_recovery_hr(hr_exercise, hr_1min, hr_2min)` | 恢复心率评估 |
| `assess_cardiovascular_fitness(resting_hr, age, gender)` | 心血管健康评估 |

### 其他功能

| 方法 | 描述 |
|------|------|
| `calculate_training_intensity(hr, age, resting_hr)` | 训练强度计算 |
| `hr_to_pace_estimate(hr, age, weight, activity)` | 配速估算 |
| `analyze_hr_trend(hr_readings, timestamps)` | 心率趋势分析 |

### 便捷函数

```python
from heart_rate_utils.mod import (
    calculate_max_hr,     # 计算最大心率
    get_zones,            # 获取心率区间
    get_fat_burning_hr,   # 获取燃脂心率
    get_current_zone,     # 获取当前区间
    estimate_calories,    # 估算卡路里
    assess_fitness        # 评估心血管健康
)
```

## 训练区间详解

### Zone 1 - 恢复区间 (50-60%)

- **用途**: 热身、冷身、恢复训练
- **感觉**: 极轻松，几乎不累
- **脂肪燃烧**: 约 85% 脂肪供能
- **适用**: 初学者、恢复日、伤病后恢复

### Zone 2 - 有氧基础 (60-70%)

- **用途**: 长时间有氧训练，燃脂
- **感觉**: 轻松，可以说话
- **脂肪燃烧**: 约 65-85% 脂肪供能
- **适用**: 减脂、基础耐力训练、马拉松基础训练

### Zone 3 - 有氧耐力 (70-80%)

- **用途**: 提高有氧能力
- **感觉**: 中等强度，有些喘但能保持
- **脂肪燃烧**: 约 40-55% 脂肪供能
- **适用**: 10公里/半马配速训练

### Zone 4 - 无氧阈值 (80-90%)

- **用途**: 提高乳酸阈值
- **感觉**: 较高强度，喘不过气
- **适用**: 间歇训练、速度耐力提升

### Zone 5 - 最大努力 (90-100%)

- **用途**: 竞技训练、爆发力
- **感觉**: 极度喘息，无法维持
- **适用**: 比赛冲刺、短间歇

## 最大心率公式对比

| 年龄 | Standard | Tanaka | Gellish | Arena | Average |
|------|----------|--------|---------|-------|---------|
| 20 | 200 | 194 | 193 | 195 | 193 |
| 30 | 190 | 187 | 186 | 191 | 185 |
| 40 | 180 | 180 | 179 | 181 | 179 |
| 50 | 170 | 173 | 172 | 173 | 173 |
| 60 | 160 | 166 | 165 | 166 | 165 |

**推荐**: Tanaka 公式适用于大多数健康成年人，误差较小。

## 恢复心率评级标准

| 1分钟下降 | 评级 | 健康风险 |
|-----------|------|----------|
| ≥25 bpm | 优秀 | 低风险 |
| 15-24 bpm | 良好 | 较低风险 |
| 10-14 bpm | 一般 | 中等风险 |
| <10 bpm | 较差 | 较高风险 |

## 心血管健康评级（静息心率）

### 男性

| 静息心率 | 评级 |
|----------|------|
| <50 bpm | 运动员级别 |
| 50-59 bpm | 优秀 |
| 60-69 bpm | 良好 |
| 70-79 bpm | 一般 |
| 80-89 bpm | 需改善 |
| ≥90 bpm | 建议就医 |

### 女性

| 静息心率 | 评级 |
|----------|------|
| <54 bpm | 运动员级别 |
| 54-63 bpm | 优秀 |
| 64-73 bpm | 良好 |
| 74-83 bpm | 一般 |
| 84-93 bpm | 需改善 |
| ≥94 bpm | 建议就医 |

## 测试

```bash
python heart_rate_utils_test.py
```

## 依赖

无外部依赖，仅使用 Python 标准库。

## 作者

AllToolkit

## 版本

1.0.0