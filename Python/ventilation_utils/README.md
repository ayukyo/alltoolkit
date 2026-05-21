# Ventilation Utils - 室内通风计算工具

专业的室内通风计算工具库，用于评估和设计建筑通风系统。

## 功能特性

### 核心计算功能

- **换气次数计算** (ACH - Air Changes per Hour)
- **CO2浓度预测与评估**
- **通风量需求计算**
- **通风时间估算**
- **空气质量等级评估**

### 高级功能

- **自然通风计算** - 风压和热压通风量
- **机械通风设计** - 风量和管道尺寸
- **污染物衰减计算** - 浓度随时间变化
- **人数估算** - 根据CO2反推室内人数
- **HVAC热负荷计算** - 通风热负荷估算

## 安装

```bash
# 无需外部依赖，直接使用
from ventilation_utils import mod as vent
```

## 快速开始

### 创建房间信息

```python
from ventilation_utils.mod import RoomInfo, analyze_room_ventilation

# 创建房间：10m x 8m x 3m，有20人
room = RoomInfo(length=10, width=8, height=3, occupants=20)

print(f"房间体积: {room.volume}m³")
print(f"地板面积: {room.floor_area}m²")
```

### 分析通风需求

```python
# 分析办公室通风
result = analyze_room_ventilation(room, room_type="office")

print(f"所需换气次数: {result.required_ach} ACH")
print(f"所需风量: {result.required_airflow:.1f} m³/h")
print(f"推荐风量: {result.recommended_airflow:.1f} m³/h")
print(f"稳态CO2浓度: {result.co2_steady_state:.0f} ppm")
print(f"空气质量: {result.quality_level.value}")
```

### 快速检查

```python
from ventilation_utils.mod import quick_ventilation_check

# 一键检查
result = quick_ventilation_check(
    room_length=10,
    room_width=8,
    room_height=3,
    occupants=20,
    room_type="office"
)

for key, value in result.items():
    print(f"{key}: {value}")
```

## 详细用法

### CO2浓度计算

```python
from ventilation_utils.mod import (
    calculate_co2_steady_state,
    predict_co2_decay,
    calculate_ventilation_time
)

# 计算稳态CO2浓度
room = RoomInfo(length=10, width=8, height=3, occupants=20)
co2 = calculate_co2_steady_state(room, airflow=600)
print(f"稳态CO2: {co2:.0f} ppm")

# 预测CO2衰减
prediction = predict_co2_decay(
    volume=240,
    initial_co2=1500,
    airflow=600,
    time_minutes=30
)
print(f"30分钟后CO2: {prediction.final_ppm:.0f} ppm")

# 计算通风时间
time_needed = calculate_ventilation_time(
    volume=240,
    initial_co2=1500,
    target_co2=800,
    airflow=600
)
print(f"降至800ppm需要: {time_needed:.1f} 分钟")
```

### 自然通风计算

```python
from ventilation_utils.mod import calculate_natural_ventilation

# 计算自然通风量
result = calculate_natural_ventilation(
    opening_area=2.0,      # 开口面积 2m²
    wind_speed=3.0,        # 风速 3m/s
    temperature_diff=5,    # 温差 5°C
    height=3.0             # 高度差 3m
)

print(f"风压通风: {result['wind_airflow']:.1f} m³/h")
print(f"热压通风: {result['stack_airflow']:.1f} m³/h")
print(f"总通风量: {result['total_airflow']:.1f} m³/h")
print(f"主要驱动: {result['primary_driver']}")
```

### 管道尺寸计算

```python
from ventilation_utils.mod import calculate_fresh_air_duct_size

# 计算新风管道尺寸
duct = calculate_fresh_air_duct_size(
    airflow=600,           # 风量 600m³/h
    air_velocity=4.0       # 风速 4m/s
)

print(f"圆管直径: {duct['diameter_mm']:.1f} mm")
print(f"方管边长: {duct['square_side_mm']:.1f} mm")
print(f"推荐标准直径: {duct['recommended_diameter_mm']} mm")
```

### 人数估算

```python
from ventilation_utils.mod import estimate_occupancy_from_co2

# 根据CO2反推人数
room = RoomInfo(length=10, width=8, height=3)
occupancy = estimate_occupancy_from_co2(
    room=room,
    current_co2=1200,      # 当前CO2浓度
    airflow=500            # 已知通风量
)
print(f"估算人数: {occupancy} 人")
```

### 污染物衰减计算

```python
from ventilation_utils.mod import calculate_pollutant_decay

# 计算污染物衰减
result = calculate_pollutant_decay(
    volume=240,
    initial_concentration=100,  # 初始浓度
    airflow=600,                # 通风量
    decay_rate=0.1,             # 自然衰减率
    time_hours=1.0              # 时间
)

print(f"最终浓度: {result['final_concentration']:.2f}")
print(f"半衰期: {result['half_life_hours']:.2f} 小时")
print(f"去除率: {result['removal_percentage']:.1f}%")
```

### HVAC热负荷计算

```python
from ventilation_utils.mod import calculate_hvac_requirements

room = RoomInfo(length=10, width=8, height=3)

# 夏季制冷
result = calculate_hvac_requirements(
    room=room,
    outdoor_temp=35,           # 室外35°C
    indoor_temp_target=24,     # 目标24°C
    ventilation_rate=2         # 2 ACH
)

print(f"通风热负荷: {result['ventilation_heat_load_kw']:.2f} kW")
print(f"模式: {result['mode']}")
print(f"BTU/h: {result['btu_per_hour']:.0f}")
```

## 空气质量等级

| 等级 | CO2范围 (ppm) | 说明 |
|------|---------------|------|
| Excellent | < 600 | 优秀，空气清新 |
| Good | 600-800 | 良好，适合长期停留 |
| Moderate | 800-1000 | 中等，可接受 |
| Poor | 1000-1500 | 较差，需要通风 |
| Very Poor | > 1500 | 很差，必须通风 |

## 标准换气次数 (ACH)

| 房间类型 | 推荐ACH |
|----------|---------|
| 卧室 | 0.5 |
| 客厅 | 0.5 |
| 办公室 | 1.0 |
| 教室 | 2.0 |
| 医院 | 6.0 |
| 厨房 | 3.0 |
| 卫生间 | 5.0 |
| 健身房 | 4.0 |
| 餐厅 | 6.0 |

## 新风标准 (每人m³/h)

| 标准 | 风量 |
|------|------|
| 最低 | 25 |
| 标准 | 30 |
| 舒适 | 40 |
| 高端 | 50 |

## 运行测试

```bash
cd Python/ventilation_utils
python -m pytest ventilation_utils_test.py -v
```

## 示例输出

```
=== 室内通风计算工具示例 ===

房间信息: 10m x 8m x 3m
体积: 240m³, 面积: 80m², 人数: 20

所需换气次数: 0.83 ACH
所需风量: 600.0 m³/h
推荐风量: 720.0 m³/h
通风类型: hybrid
稳态CO2浓度: 620 ppm
空气质量: good
备注: 可采用自然通风与机械通风结合; 每人新风量: 36.0 立方米/小时

=== CO2浓度衰减预测 ===
初始CO2: 1500 ppm
30分钟后: 574 ppm
换气次数: 3.00 ACH

=== 通风时间计算 ===
从2000ppm降至800ppm需要: 19.8 分钟

=== 自然通风计算 ===
风压通风量: 8640.0 m³/h
热压通风量: 2065.3 m³/h
总通风量: 8640.0 m³/h
主要驱动: wind

=== 新风管道尺寸 ===
所需面积: 50000 mm²
圆管直径: 252.3 mm
方管边长: 223.6 mm
推荐标准直径: 315 mm
```

## 应用场景

- **建筑设计师** - 计算通风系统需求
- **暖通工程师** - 设计新风系统
- **室内空气质量评估** - CO2监测与分析
- **绿色建筑认证** - 满足通风标准
- **智能家居** - 自动通风控制算法
- **健康建筑评估** - 空气质量预测

## 许可证

MIT License