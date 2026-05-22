# Dew Point Utilities (露点计算工具)

提供露点、湿球温度、饱和蒸汽压等气象计算功能。使用 Magnus 公式进行精确计算，零外部依赖。

## 功能列表

### 核心计算
- `dew_point()` - 露点温度计算
- `frost_point()` - 霜点温度计算
- `saturation_vapor_pressure()` - 饱和水蒸气压计算
- `vapor_pressure()` - 实际水蒸气分压计算
- `absolute_humidity()` - 绝对湿度计算
- `relative_humidity_from_dew_point()` - 从露点反算相对湿度
- `wet_bulb_temperature()` - 湿球温度计算
- `heat_index()` - 热指数（体感温度）计算

### 高级分析
- `analyze_humidity()` - 综合湿度分析，返回所有相关数据
- `comfort_level()` - 体感舒适度评估
- `dew_point_depression()` - 露点差计算
- `fog_risk()` - 雾形成风险评估
- `condensation_prediction()` - 表面结露预测
- `temperature_for_target_rh()` - 计算达到目标湿度的温度

### 气象参数
- `mixing_ratio()` - 混合比计算
- `specific_humidity()` - 比湿计算
- `humidity_ratio()` - 湿度比计算
- `enthalpy()` - 湿空气焓值计算

## 使用示例

```python
from dew_point_utils import dew_point, analyze_humidity, comfort_level, fog_risk

# 基本露点计算
dp = dew_point(25, 60)  # 25°C, 60%相对湿度
print(f"露点温度: {dp:.1f}°C")

# 综合湿度分析
data = analyze_humidity(22, 55)
print(f"露点: {data.dew_point:.1f}°C")
print(f"绝对湿度: {data.absolute_humidity:.2f} g/m³")
print(f"舒适度: {data.comfort_level.value}")

# 雾风险评估
risk = fog_risk(15, 95)
print(f"雾风险: {risk}")

# 结露预测
will_condense, msg = condensation_prediction(28, 75, 18)
print(msg)
```

## 舒适度等级

| 露点温度 | 等级 | 描述 |
|---------|------|------|
| < 10°C  | VERY_DRY | 非常干燥 |
| 10-13°C | DRY | 干燥 |
| 13-16°C | COMFORTABLE | 舒适 |
| 16-18°C | HUMID | 潮湿 |
| 18-24°C | VERY_HUMID | 非常潮湿 |
| > 24°C  | OPPRESSIVE | 闷热 |

## 技术细节

- 使用 Magnus-Tetens 公式计算饱和蒸汽压
- 使用 Stull 近似公式计算湿球温度
- 使用 Rothfusz 回归公式计算热指数
- 舒适度分级基于美国国家气象局标准

## 运行测试

```bash
python test_dew_point_utils.py
```

## 应用场景

- 暖通空调系统设计
- 气象数据分析
- 建筑结露风险评估
- 农业气象监测
- 工业过程控制
- 健康舒适度评估