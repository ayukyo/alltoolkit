# Cycling Utils - 骑行计算工具

骑行运动计算工具，支持功率、速度、齿轮、爬坡、训练等全方位计算。

## 功能特性

- **速度/距离/时间**: 基础骑行计算
- **功率估算**: 考虑风阻、坡度、骑行姿势
- **训练区间**: 7 区训练强度分类
- **卡路里消耗**: 功率/心率两种估算方式
- **齿轮计算**: 齿比、踏频、速度转换
- **爬坡指标**: VAM、爬坡难度评分
- **训练指标**: NP、TSS、IF

## 快速开始

```python
from cycling_utils.mod import (
    CyclingUtils,
    RiderProfile,
    GearConfig,
    calculate_speed,
    calculate_power,
    calculate_calories,
)

# 速度计算
speed = calculate_speed(100, 4)  # 100km in 4h = 25km/h

# 功率估算（75kg 骑手，30km/h，平路）
power = calculate_power(30, weight_kg=75)
print(f"所需功率: {power}W")

# 卡路里计算（200W，骑行 2 小时）
calories = calculate_calories(200, 2)
print(f"消耗卡路里: {calories}kcal")
```

## 核心类

### CyclingUtils - 骑行计算器

```python
from cycling_utils.mod import CyclingUtils, RiderProfile, RidingPosition

rider = RiderProfile(weight_kg=75, ftp_watts=250)
utils = CyclingUtils(rider=rider, bike_weight_kg=8.5)

# 功率计算（考虑风阻、坡度）
power = utils.calculate_power(
    speed_kmh=30,
    gradient_percent=5,  # 5% 爬坡
    wind_speed_kmh=10,   # 10km/h 顶风
    riding_position=RidingPosition.DROPS
)

# 从功率估算速度
speed = utils.estimate_speed_from_power(200, gradient_percent=0)

# 功率体重比
ratio = utils.calculate_power_to_weight_ratio(300)  # 4.0 W/kg

# 训练区间
zone, name, desc = utils.get_training_zone(240)
# zone=4, name="Threshold"
```

### 骑行位置影响

| 位置 | 风阻系数 | 正面面积 |
|------|----------|----------|
| TOPS | 1.15 | 0.55 m² |
| HOODS | 1.00 | 0.50 m² |
| DROPS | 0.88 | 0.45 m² |
| AERO | 0.75 | 0.35 m² |

## 齿轮计算

```python
from cycling_utils.mod import GearConfig

gear_config = GearConfig(
    front_teeth=[50, 34],  # 压盘
    rear_teeth=[11, 12, 13, 14, 15, 17, 19, 21, 24, 28],  # 飞轮
)
utils = CyclingUtils(gear_config=gear_config)

# 齿比
ratio = utils.calculate_gear_ratio(50, 11)  # 4.55

# 从踏频计算速度
speed = utils.calculate_speed_from_cadence(90, 50, 14)  # ~40km/h

# 从速度计算所需踏频
cadence = utils.calculate_cadence_from_speed(30, 50, 14)

# 所有齿比组合
ratios = utils.get_all_gear_ratios()  # [(34, 28, 1.21), ..., (50, 11, 4.55)]
```

## 爬坡计算

```python
# 坡度计算
gradient = utils.calculate_gradient(14, 1120)  # Alpe d'Huez ~8%

# 海拔增益
gain = utils.calculate_elevation_gain(10, 5)  # 10km at 5% = 500m

# VAM（爬升速度）
vam = utils.calculate_vam(1200, 0.75)  # 1200m in 45min = 1600 m/h

# 爬坡难度评分
difficulty = utils.calculate_climbing_difficulty(14, 1120)
```

## 训练指标

```python
# Normalized Power（标准化功率）
power_samples = [200, 220, 180, 250, ...]  # 功率数据
np = utils.calculate_np(power_samples, sample_interval_seconds=1.0)

# Training Stress Score（训练压力评分）
tss = utils.calculate_tss(np.value, duration_hours=2)
# 2 小时 @ FTP = 200 TSS

# Intensity Factor（强度因子）
if_val = utils.calculate_if(np.value)
# IF = NP / FTP
```

### 训练区间对照表

| 区间 | 名称 | FTP 范围 | 说明 |
|------|------|----------|------|
| 1 | Active Recovery | 0-55% | 恢复骑行 |
| 2 | Endurance | 55-75% | 有氧耐力 |
| 3 | Tempo | 75-90% | 节奏骑行 |
| 4 | Threshold | 90-105% | 门槛强度 |
| 5 | VO2 Max | 105-120% | 最大摄氧量 |
| 6 | Anaerobic | 120-150% | 无氧耐力 |
| 7 | Sprint | >150% | 最大冲刺 |

## 卡路里计算

```python
# 从功率计算（更精确）
calories = utils.calculate_calories(200, 2, efficiency_percent=24)

# 从心率估算
rider = RiderProfile(weight_kg=70, age_years=30, gender='male')
utils = CyclingUtils(rider=rider)
calories = utils.estimate_calories_from_hr(150, 1.5)
```

## 地面阻力系数

| 地面 | 阻力系数 |
|------|----------|
| Asphalt | 0.004 |
| Concrete | 0.003 |
| Gravel | 0.012 |
| Grass | 0.025 |
| Sand | 0.050 |

## 测试覆盖

28 个测试用例，覆盖：
- 速度/时间/距离计算
- 功率估算
- 齿轮齿比
- 爬坡指标
- 训练区间
- 卡路里计算
- 边界值处理

## 许可证

MIT License