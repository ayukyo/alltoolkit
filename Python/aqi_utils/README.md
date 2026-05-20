# AQI Utils - 空气质量指数计算工具

计算多种污染物的 AQI（空气质量指数），支持中国和美国 EPA 标准，提供健康建议和活动推荐。

## 功能特性

- ✅ 支持多种污染物：PM2.5、PM10、臭氧(O3)、一氧化碳(CO)、二氧化硫(SO2)、二氧化氮(NO2)
- ✅ 双标准支持：中国标准和美国 EPA 标准
- ✅ AQI等级分类：优、良、轻度污染、中度污染、重度污染、严重污染
- ✅ 健康建议：针对不同 AQI 等级提供详细健康指导
- ✅ 活动建议：户外运动、口罩佩戴、通风等建议
- ✅ 综合AQI：多污染物综合评估，识别首要污染物
- ✅ 双向转换：浓度 ↔ AQI 相互转换
- ✅ 能见度估算：根据能见度粗略估算 PM2.5
- ✅ 污染物信息：详细的污染物来源和健康影响说明

## 快速开始

```python
from aqi_utils.mod import calculate_aqi, PollutantType

# 计算 PM2.5 的 AQI（中国标准）
result = calculate_aqi(75, PollutantType.PM25, "cn")
print(f"AQI: {result.aqi}")
print(f"等级: {result.level.value}")
print(f"健康建议: {result.health_advice}")
```

## API 参考

### 基础计算

#### `calculate_aqi(concentration, pollutant, standard)`
计算单个污染物的 AQI 值。

```python
from aqi_utils.mod import calculate_aqi, PollutantType

result = calculate_aqi(
    concentration=75,           # 浓度值
    pollutant=PollutantType.PM25,  # 污染物类型
    standard="cn"               # 标准: "cn" 或 "us"
)

# 返回 AQIResult 对象
print(result.aqi)               # AQI 值
print(result.level)             # AQILevel 枚举
print(result.level.value)       # 等级名称（如"良"）
print(result.concentration)     # 浓度值
print(result.unit)              # 浓度单位
print(result.color)             # 颜色代码 (hex)
print(result.health_advice)     # 健康建议
print(result.activity_suggestion)  # 活动建议
```

#### `calculate_comprehensive_aqi(concentrations, standard)`
计算综合 AQI（取各污染物 AQI 最大值）。

```python
from aqi_utils.mod import calculate_comprehensive_aqi

# 提供多个污染物浓度
concentrations = {
    "pm25": 68,
    "pm10": 95,
    "o3": 120,
    "co": 1.2,
    "so2": 25,
    "no2": 45
}

result = calculate_comprehensive_aqi(concentrations, "cn")

print(result.aqi)                    # 综合 AQI 值
print(result.primary_pollutant)      # 首要污染物
print(result.all_results)            # 所有污染物结果字典
```

### 便捷函数

```python
from aqi_utils.mod import (
    pm25_to_aqi, pm10_to_aqi, o3_to_aqi,
    co_to_aqi, so2_to_aqi, no2_to_aqi
)

# 快速计算各污染物 AQI
aqi = pm25_to_aqi(50)   # PM2.5
aqi = pm10_to_aqi(100)  # PM10
aqi = o3_to_aqi(150)    # 臭氧
aqi = co_to_aqi(2.5)    # CO
aqi = so2_to_aqi(80)    # SO2
aqi = no2_to_aqi(60)    # NO2
```

### AQI 转浓度

```python
from aqi_utils.mod import aqi_to_concentration, PollutantType

# AQI 值转浓度
concentration = aqi_to_concentration(100, PollutantType.PM25, "cn")
print(f"PM2.5 浓度约 {concentration} μg/m³")
```

### 健康建议

```python
from aqi_utils.mod import get_health_recommendations

recommendations = get_health_recommendations(150)

print(recommendations['general'])          # 总体建议
print(recommendations['activity'])         # 活动建议
print(recommendations['sensitive_groups']) # 敏感人群建议
print(recommendations['outdoor'])          # 户外活动建议
print(recommendations['mask'])             # 口罩佩戴建议
print(recommendations['ventilation'])      # 通风建议
```

### 标准对比

```python
from aqi_utils.mod import compare_standards, PollutantType

# 比较中国和美国标准
results = compare_standards(35, PollutantType.PM25)
print(f"中国标准: AQI {results['cn'].aqi}")
print(f"美国标准: AQI {results['us'].aqi}")
```

### 污染物信息

```python
from aqi_utils.mod import get_pollutant_info, PollutantType

info = get_pollutant_info(PollutantType.PM25)
print(info['name'])          # 名称
print(info['description'])   # 描述
print(info['source'])        # 来源
print(info['health_effect']) # 健康影响
```

### AQI 范围计算

```python
from aqi_utils.mod import calculate_aqi_range, PollutantType

# 计算浓度范围的 AQI 变化
results = calculate_aqi_range(
    concentration_low=0,
    concentration_high=150,
    pollutant=PollutantType.PM25,
    steps=10
)

for r in results:
    print(f"浓度 {r['concentration']} -> AQI {r['aqi']} ({r['level']})")
```

### 能见度估算

```python
from aqi_utils.mod import estimate_pm25_from_visibility

# 根据能见度估算 PM2.5（粗略估算）
pm25 = estimate_pm25_from_visibility(5)  # 5 公里能见度
print(f"估算 PM2.5 浓度: {pm25} μg/m³")
```

## AQI 分级标准

### 中国标准

| AQI 范围 | 等级 | 颜色 |
|----------|------|------|
| 0-50 | 优 | 绿色 |
| 51-100 | 良 | 黄色 |
| 101-150 | 轻度污染 | 橙色 |
| 151-200 | 中度污染 | 红色 |
| 201-300 | 重度污染 | 紫色 |
| >300 | 严重污染 | 褐红色 |

### 美国 EPA 标准

美国标准的 AQI 分级范围相同，但各污染物的浓度断点不同，通常更严格。

## 污染物浓度单位

| 污染物 | 单位 |
|--------|------|
| PM2.5 | μg/m³ |
| PM10 | μg/m³ |
| O3 | μg/m³ |
| CO | mg/m³ |
| SO2 | μg/m³ |
| NO2 | μg/m³ |

## 使用示例

### 基础使用

```python
from aqi_utils.mod import calculate_aqi, PollutantType

# PM2.5 浓度 75 μg/m³
result = calculate_aqi(75, PollutantType.PM25, "cn")
print(f"空气质量: {result.level.value}")
print(f"健康建议: {result.health_advice}")
```

### 综合评估

```python
from aqi_utils.mod import calculate_comprehensive_aqi

# 查看今日空气质量
today_data = {
    "pm25": 45,
    "pm10": 80,
    "o3": 95
}

result = calculate_comprehensive_aqi(today_data)
print(f"今日 AQI: {result.aqi}")
print(f"首要污染物: {result.primary_pollutant.value}")
```

### 健康指导

```python
from aqi_utils.mod import get_health_recommendations, get_aqi_level

aqi = 150
level = get_aqi_level(aqi)
rec = get_health_recommendations(aqi)

print(f"AQI {aqi} ({level.value})")
print(f"建议佩戴口罩: {rec['mask']}")
print(f"户外活动建议: {rec['outdoor']}")
```

## 测试

```bash
python Python/aqi_utils/aqi_utils_test.py
```

测试覆盖：
- 各污染物 AQI 计算（中国/美国标准）
- 综合 AQI 计算
- AQI 转浓度
- 健康建议
- 边界值处理
- 污染物信息

## 注意事项

1. **能见度估算**：`estimate_pm25_from_visibility()` 为粗略估算，高湿度条件下不准确
2. **AQI 上限**：计算结果限制在 0-500 范围内
3. **臭氧标准**：臭氧有 1 小时和 8 小时两种标准，通常 8 小时标准更常用
4. **标准差异**：中国和美国标准的浓度断点不同，美国标准通常更严格

## 许可证

MIT License