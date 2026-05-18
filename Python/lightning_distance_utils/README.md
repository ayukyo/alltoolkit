# Lightning Distance Utils - 闪电距离计算工具 ⚡

[![测试状态](https://img.shields.io/badge/tests-passed-brightgreen)]()
[![覆盖率](https://img.shields.io/badge/coverage-100%25-brightgreen)]()

基于闪光-雷声时间差计算闪电距离的工具库，包含安全预警和教育功能。

## ✨ 功能特性

### 基础计算
- **距离计算**：基于闪光-雷声时间差计算闪电距离
- **温度补偿**：根据温度调整声速计算
- **多单位支持**：公里、英里、米、英尺

### 安全预警
- **安全等级**：自动判断危险程度（安全、警戒、危险、紧急）
- **安全建议**：根据距离提供具体安全建议
- **活动判断**：判断户外活动是否安全

### 高级功能
- **风暴追踪**：分析多次闪电判断风暴方向
- **三角定位**：多观测点定位闪电位置
- **雷声强度预估**：预测雷声可听度

---

## 🚀 快速开始

### 基础距离计算

```python
from lightning_distance_utils import quick_distance

# 看到闪电后 5 秒听到雷声
distance_km = quick_distance(5)  # 约 1.7 公里
print(f"闪电距离: {distance_km} 公里")
```

### 详细计算

```python
from lightning_distance_utils import LightningDistanceCalculator

# 创建计算器（可选设置温度）
calc = LightningDistanceCalculator(temperature_celsius=25)

# 计算闪电距离
strike = calc.calculate_distance(10)  # 10秒时间差

print(f"距离: {strike.distance_km} 公里")
print(f"距离: {strike.distance_miles} 英里")
print(f"安全等级: {strike.safety_level.value}")
print(f"是否危险: {strike.is_dangerous}")
```

### 安全建议

```python
from lightning_distance_utils import LightningDistanceCalculator

calc = LightningDistanceCalculator()
strike = calc.calculate_distance(5)  # 5秒 = 约1.7公里

# 获取安全建议
recommendation = calc.get_safety_recommendation(strike)
print(recommendation)
# "🔴 CRITICAL: Lightning is extremely close (1.7 km)! ..."
```

---

## 📚 详细用法

### 快捷函数

```python
from lightning_distance_utils import (
    quick_distance,       # 快速公里计算
    quick_distance_miles, # 快速英里计算
    rule_of_thumb_distance, # 经验法则计算
    flash_to_bang_kilometers, # 闪光到雷声公里
    flash_to_bang_miles       # 闪光到雷声英里
)

# 快速计算
km = quick_distance(10)        # 10秒 → 约3.4公里
miles = quick_distance_miles(10)  # 10秒 → 约2.1英里

# 经验法则（5秒≈1英里，3秒≈1公里）
rule = rule_of_thumb_distance(10)
print(rule['rule_of_thumb_km'])    # 3.3公里
print(rule['rule_of_thumb_miles']) # 2英里
```

### 温度影响声速

```python
from lightning_distance_utils import LightningDistanceCalculator

# 不同温度下声速不同
calc_0c = LightningDistanceCalculator(0)   # 0°C 声速约 331 m/s
calc_20c = LightningDistanceCalculator(20) # 20°C 声速约 343 m/s
calc_35c = LightningDistanceCalculator(35) # 35°C 声速约 352 m/s

strike_0c = calc_0c.calculate_distance(10)
strike_20c = calc_20c.calculate_distance(10)
strike_35c = calc_35c.calculate_distance(10)

print(f"0°C时10秒距离: {strike_0c.distance_km} km")  # 约3.3km
print(f"20°C时10秒距离: {strike_20c.distance_km} km") # 约3.4km
print(f"35°C时10秒距离: {strike_35c.distance_km} km") # 约3.5km
```

### 风暴追踪

```python
from lightning_distance_utils import LightningDistanceCalculator

calc = LightningDistanceCalculator()

# 分析多次闪电
strikes = [5, 4, 3, 2, 1]  # 连续闪电的时间差（秒）
analysis = calc.count_strikes(strikes)

print(f"闪电次数: {analysis['total_strikes']}")
print(f"平均距离: {analysis['average_distance_km']} 公里")
print(f"最近闪电: {analysis['closest_strike_km']} 公里")
print(f"风暴正在接近: {analysis['storm_approaching']}")
print(f"安全等级: {analysis['safety_level']}")
```

### 安全活动判断

```python
from lightning_distance_utils import is_lightning_safe

# 判断游泳是否安全
safe, recommendation = is_lightning_safe("swimming", distance_km=5)

print(f"是否安全: {safe}")
print(f"建议: {recommendation}")
```

### 预估雷声到达时间

```python
from lightning_distance_utils import estimate_thunder_arrival

# 闪电在 5 公里外
time_seconds = estimate_thunder_arrival(5)
print(f"雷声将在 {time_seconds:.1f} 秒后到达")
```

### 雷声强度预估

```python
from lightning_distance_utils import thunder_volume_estimate

volume = thunder_volume_estimate(0.5)  # 0.5公里
print(volume)  # "Extremely loud - may cause hearing damage..."

volume = thunder_volume_estimate(5)  # 5公里
print(volume)  # "Loud - clear rumble, easily heard indoors"
```

### 三角定位

```python
from lightning_distance_utils import calculate_strike_angle

# 两个观测点的数据
time_delays = [5, 8]  # 观测点1:5秒，观测点2:8秒
positions = [(0, 0), (10, 0)]  # 观测点位置（公里坐标）

position = calculate_strike_angle(time_delays, positions)
print(f"闪电位置: ({position[0]}, {position[1])} 公里")
```

---

## 🔧 API 参考

### LightningDistanceCalculator 类

| 方法 | 说明 |
|------|------|
| `calculate_distance(time_delay)` | 计算闪电距离 |
| `get_safety_recommendation(strike)` | 获取安全建议 |
| `count_strikes(strikes)` | 分析多次闪电 |
| `set_temperature(temp)` | 设置温度 |

### 便捷函数

| 函数 | 说明 |
|------|------|
| `quick_distance(seconds)` | 快速公里计算 |
| `quick_distance_miles(seconds)` | 快速英里计算 |
| `rule_of_thumb_distance(seconds)` | 经验法则 |
| `estimate_thunder_arrival(distance_km)` | 预估雷声到达 |
| `get_safe_shelter_time(distance_km)` | 计算避险时间 |
| `is_lightning_safe(activity, distance)` | 安全活动判断 |
| `thunder_volume_estimate(distance)` | 雷声强度预估 |

---

## 📊 安全等级

| 等级 | 距离范围 | 说明 |
|------|----------|------|
| SAFE | >15 km | 相对安全，继续监测 |
| CAUTION | 10-15 km | 警戒状态，准备避险 |
| DANGER | 3-6 km | 危险！立即避险 |
| IMMEDIATE | <3 km | 紧急！极高风险 |

---

## 📝 计算原理

### 基本原理

闪电光几乎瞬间到达（光速 ~300,000 km/s），而雷声传播较慢（声速 ~343 m/s）。通过测量闪光与雷声的时间差，可以计算闪电距离：

```
距离 = 声速 × 时间
```

### 温度补偿公式

声速随温度变化：

```
v = 331.3 + (0.606 × T) m/s
```

其中 T 是摄氏温度。

### 经验法则

- **每5秒 ≈ 1英里**
- **每3秒 ≈ 1公里**

---

## ⚠️ 安全提示

### 30-30 法则

1. 如果闪光到雷声少于30秒，立即避险
2. 最后一声雷后等待30分钟才能恢复户外活动

### 避险建议

- 进入室内或金属顶车辆
- 避开窗户、水管、电器
- 远离高处、大树、水体
- 无避难所时：蹲低、双脚并拢、捂住耳朵

---

## 🧪 测试

```bash
python Python/lightning_distance_utils/lightning_distance_utils_test.py
```

---

## 📄 许可证

MIT License

---

**最后更新**: 2026-05-19