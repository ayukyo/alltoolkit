# Nautical Utilities

航海和海事工具集 - 提供航海相关的转换和计算功能。

## 功能列表

### 速度转换
- `knots_to_mph(knots)` - 节转英里/小时
- `knots_to_kph(knots)` - 节转公里/小时
- `knots_to_ms(knots)` - 节转米/秒
- `mph_to_knots(mph)` - 英里/小时转节
- `kph_to_knots(kph)` - 公里/小时转节
- `ms_to_knots(ms)` - 米/秒转节
- `convert_speed(value, from_unit, to_unit)` - 通用速度转换

### 距离转换
- `nautical_miles_to_miles(nm)` - 海里转英里
- `nautical_miles_to_km(nm)` - 海里转公里
- `miles_to_nautical_miles(miles)` - 英里转海里
- `km_to_nautical_miles(km)` - 公里转海里
- `convert_distance(value, from_unit, to_unit)` - 通用距离转换

### 深度转换
- `fathoms_to_feet(fathoms)` - 英寻转英尺
- `fathoms_to_meters(fathoms)` - 英寻转米
- `feet_to_fathoms(feet)` - 英尺转英寻
- `meters_to_fathoms(meters)` - 米转英寻

### 蒲福风级 (Beaufort Scale)
- `get_beaufort_scale(knots)` - 获取风速对应的风级
- `get_beaufort_range(scale)` - 获取风级对应的风速范围
- `describe_wind(knots)` - 获取风速详细信息（含风级、描述、海况）

### 罗盘方位
- `degrees_to_cardinal(degrees)` - 度数转方位缩写 (N, NNE, NE, etc.)
- `degrees_to_full_name(degrees)` - 度数转方位全名 (North, Northeast, etc.)
- `cardinal_to_degrees(cardinal)` - 方位转度数
- `normalize_heading(degrees)` - 标准化航向 (0-360度)
- `heading_difference(heading1, heading2)` - 计算两航向间最小角度

### 经纬度处理
- `Coordinate` - 坐标类，支持度分秒和十进制度数转换
- `parse_coordinate(coord_string)` - 解析坐标字符串
- `format_latitude(decimal, format)` - 格式化纬度
- `format_longitude(decimal, format)` - 格式化经度

### 海事旗语
- `get_maritime_flag_meaning(letter)` - 获取海事旗语含义
- `encode_maritime_message(message)` - 用海事旗语编码消息
- `get_distress_signals()` - 获取遇险信号列表

### 导航计算
- `calculate_distance_nm(lat1, lon1, lat2, lon2)` - 计算两点间大圆距离（海里）
- `calculate_bearing(lat1, lon1, lat2, lon2)` - 计算两点间航向
- `time_to_destination(distance_nm, speed_knots)` - 计算航行时间
- `fuel_consumption(distance_nm, consumption_rate, speed_knots)` - 计算燃油消耗

## 使用示例

```python
from mod import *

# 速度转换
print(f"10节 = {knots_to_mph(10):.2f} 英里/小时")  # 11.51 mph

# 蒲福风级
wind = describe_wind(25)
print(f"25节风速: 风级 {wind['beaufort']} ({wind['description']})")
# 25节风速: 风级 6 (Strong Breeze)

# 罗盘方位
print(f"45度 = {degrees_to_cardinal(45)}")  # NE
print(f"北方的度数 = {cardinal_to_degrees('N')}")  # 0.0

# 经纬度格式化
print(format_latitude(37.7749))  # 37°46'29.6"N

# 海事旗语
print(get_maritime_flag_meaning('A'))  # Alpha - Diver below; keep clear

# 导航计算
distance = calculate_distance_nm(37.7749, -122.4194, 34.0522, -118.2437)
print(f"旧金山到洛杉矶距离: {distance} 海里")  # ~298 海里

# 航行时间
time = time_to_destination(100, 20)
print(f"100海里以20节速度航行需要 {time} 小时")  # 5 小时
```

## 测试

```bash
python test.py
```

## 常量

```python
KNOTS_TO_MPH = 1.15078      # 节到英里/小时
KNOTS_TO_KPH = 1.852        # 节到公里/小时
KNOTS_TO_MS = 0.514444      # 节到米/秒
NAUTICAL_MILE_TO_KM = 1.852 # 海里到公里
FATHOM_TO_FEET = 6         # 英寻到英尺
EARTH_RADIUS_NM = 3440.065 # 地球半径（海里）
```

## 零依赖

本模块仅使用 Python 标准库，无需安装任何外部依赖。