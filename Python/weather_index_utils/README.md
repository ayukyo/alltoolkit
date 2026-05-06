# Weather Index Utils - 天气指数计算工具

**零依赖、生产就绪的天气指数计算库**

## 📋 功能列表

### 核心指数计算

| 指数 | 函数 | 说明 |
|------|------|------|
| 热指数 | `heat_index()` | 高温高湿体感温度 (Rothfusz 公式) |
| 风寒指数 | `wind_chill()` | 低温风冷体感温度 (NWS 公式) |
| 露点 | `dew_point()` | 空气饱和凝结温度 (Magnus 公式) |
| 体感温度 | `apparent_temperature()` | 综合温度、湿度、风速的体感 |
| WBGT | `wbgt()` | 湿球黑球温度，热应激综合指标 |

### 舒适度评估

| 指数 | 函数 | 说明 |
|------|------|------|
| THI | `comfort_index()` | 温湿度指数，舒适度评估 |
| 湿球温度 | `wet_bulb_temperature()` | 空气冷却到饱和时的温度 |
| 紫外线指数 | `uv_index()` | UV 辐射强度计算 |

### 农业气象

| 指数 | 函数 | 说明 |
|------|------|------|
| 蒸散量 | `evapotranspiration()` | Penman-Monteith 参考蒸散 |
| VPD | `vapor_pressure_deficit()` | 饱和水汽压差 |
| GDD | `growing_degree_days()` | 生长度日，作物发育预测 |

### 气压与海拔

| 指数 | 函数 | 说明 |
|------|------|------|
| 海拔计算 | `pressure_altitude()` | 从气压推算海拔 |
| 海平面气压 | `sea_level_pressure()` | 站点气压订正 |
| 空气密度 | `air_density()` | 考虑温度、气压、湿度 |

## 🚀 快速开始

```python
from weather_index_utils.mod import heat_index, wind_chill, dew_point

# 热指数 - 35°C, 70% 湿度
hi = heat_index(35, 70)  # 50.4°C

# 风寒指数 - -10°C, 30 km/h 风速
wc = wind_chill(-10, 30)  # -20.2°C

# 露点 - 30°C, 70% 湿度
dp = dew_point(30, 70)  # 24.0°C
```

## 📊 使用示例

### 夏季高温评估

```python
from weather_index_utils.mod import heat_index, wbgt, WeatherIndexCalculator

# 计算热指数
hi = heat_index(35, 80)  # 高温高湿
print(f"热指数: {hi}°C")

# 计算 WBGT
wbgt_val = wbgt(35, 80, 800)  # 800 W/m² 太阳辐射
risk = WeatherIndexCalculator.heat_risk_level(wbgt_val)
print(f"风险等级: {risk[1]}")
print(f"建议: {risk[2]}")
```

### 冬季寒冷评估

```python
from weather_index_utils.mod import wind_chill

# 计算风寒指数
wc = wind_chill(-15, 40)  # -15°C, 40 km/h
print(f"风寒指数: {wc}°C")

# 防寒建议
if wc < -30:
    print("⚠️ 极端寒冷！避免任何户外活动")
elif wc < -20:
    print("⚠️ 非常寒冷！穿戴多层保暖衣物")
```

### 完整天气报告

```python
from weather_index_utils.mod import WeatherIndexCalculator

report = WeatherIndexCalculator.full_weather_report(
    temperature=28,
    humidity=65,
    wind_speed=15,
    pressure=1013,
    solar_radiation=500
)

print(f"热指数: {report['indices']['heat_index']}°C")
print(f"WBGT: {report['indices']['wbgt']}°C")
print(f"舒适度: {report['assessments']['comfort_level'][1]}")
print(f"热风险: {report['assessments']['heat_risk'][1]}")
```

### 农业气象应用

```python
from weather_index_utils.mod import WeatherIndexCalculator

# 蒸散量
et = WeatherIndexCalculator.evapotranspiration(28, 60, 2, 20)
print(f"参考蒸散量: {et} mm/day")

# 生长度日
gdd = WeatherIndexCalculator.growing_degree_days(18, 32, 10)
print(f"生长度日: {gdd}")
```

## 📐 计算公式

### 热指数 (Heat Index)

使用 Rothfusz 回归方程：

```
HI = -42.379 + 2.04901523*T + 10.14333127*RH 
     - 0.22475541*T*RH - 0.00683783*T² 
     - 0.05481717*RH² + 0.00122874*T²*RH 
     + 0.00085282*T*RH² - 0.00000199*T²*RH²
```

适用范围：温度 ≥ 80°F (26.7°C)，湿度 ≥ 40%

### 风寒指数 (Wind Chill)

使用 NWS 公式：

```
WC = 35.74 + 0.6215*T - 35.75*V^0.16 + 0.4275*T*V^0.16
```

适用范围：温度 ≤ 50°F (10°C)，风速 ≥ 3 mph

### 露点 (Dew Point)

使用 Magnus 公式：

```
α = ln(RH/100) + (b*T)/(c+T)
Td = c*α/(b-α)
```

其中 b = 17.67, c = 243.5°C

### WBGT

```
室外: WBGT = 0.7*Tnw + 0.2*Tg + 0.1*T
室内: WBGT = 0.7*Tnw + 0.3*T
```

其中 Tnw 为自然湿球温度，Tg 为黑球温度

## ⚠️ 热风险等级

| WBGT (°C) | 风险等级 | 建议 |
|-----------|----------|------|
| < 25 | 白色 | 正常活动 |
| 25-27 | 绿色 | 注意补水 |
| 28-29 | 黄色 | 限制高强度活动 |
| 30-31 | 橙色 | 限制高强度运动，增加休息 |
| 32-34 | 红色 | 取消非必要户外活动 |
| ≥ 35 | 黑色 | 禁止户外活动 |

## 🧪 单位支持

- **温度**: Celsius (°C) 或 Fahrenheit (°F)
- **风速**: km/h, mph, 或 m/s
- **气压**: hPa (默认 1013.25)

```python
# 华氏度示例
hi = heat_index(95, 70, 'fahrenheit')

# 不同风速单位
wc = wind_chill(14, 18.6, 'fahrenheit', 'mph')
```

## 📁 文件结构

```
weather_index_utils/
├── mod.py                   # 主模块
├── weather_index_utils_test.py  # 测试文件
├── README.md                # 本文档
└── examples/
    └── usage_examples.py    # 使用示例
```

## 🔬 测试

```bash
python weather_index_utils/weather_index_utils_test.py
```

测试覆盖：
- 基本指数计算
- 边界值测试（零度、零风速、极端温度）
- 单位转换准确性
- 数值稳定性测试
- 完整报告生成

## 📖 参考文献

1. Rothfusz, L.P. (1990). The Heat Index Equation. NWS.
2. Steadman, R.G. (1979). Indices of Apparent Temperature.
3. Magnus, D. (1844). Versuche über die Expansivkraft des Wasserdampfs.
4. Stull, R. (2011). Wet-Bulb Temperature from Relative Humidity and Air Temperature.
5. FAO (1998). Crop Evapotranspiration - Guidelines for Computing Crop Water Requirements.

## 📄 许可证

MIT License

---

**作者**: AllToolkit 自动化生成  
**日期**: 2026-05-06  
**版本**: 1.0.0